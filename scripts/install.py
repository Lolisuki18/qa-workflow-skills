#!/usr/bin/env python3
"""Link (or copy) every skill folder of this repo into an agent's skills directory.

Usage:
  python scripts/install.py                       # link into ~/.claude/skills
  python scripts/install.py --agent gemini        # preset: claude|gemini|cursor|codex|antigravity|windsurf|cline|roo|agents
  python scripts/install.py --agent cursor --scope project   # ./.cursor/skills of the current project
  python scripts/install.py --list-agents         # show preset paths and how well each is verified
  python scripts/install.py --target ~/some/skills   # any directory
  python scripts/install.py --copy                # copy instead of link
  python scripts/install.py --dry-run             # show what would happen
  python scripts/install.py --uninstall           # remove links/copies made from this repo
  python scripts/install.py --only a,b            # install only these skills (names not in this repo are ignored)
  python scripts/install.py --exclude a,b         # install everything except these skills

A skill is any top-level folder here that contains SKILL.md. Existing entries are never
overwritten: they are reported as `exists` (or `replaced` only with --force, links only).
Windows: uses directory junctions (no admin rights). POSIX: symlinks.
Stdlib only.
"""
import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

# Skill directories per agent. `ok` = taken from the vendor's own docs when checked
# (2026-11-23); `weak` = only third-party sources or conflicting docs, verify before relying.
# Re-check in docs/maintenance.md reviews: agents change these paths between releases.
AGENTS = {
    "claude":      {"user": "~/.claude/skills",            "project": ".claude/skills",   "conf": "ok"},
    "gemini":      {"user": "~/.gemini/skills",            "project": ".gemini/skills",   "conf": "ok"},
    "cursor":      {"user": "~/.cursor/skills",            "project": ".cursor/skills",   "conf": "weak",
                    "note": "Cursor's docs confirm project .cursor/skills; the user-level ~/.cursor/skills "
                            "is only third-party confirmed. Cursor also reads ~/.claude/skills."},
    "codex":       {"user": "~/.codex/skills",             "project": ".agents/skills",   "conf": "weak",
                    "note": "~/.codex/skills is the long-standing user path; .agents/skills as project path "
                            "was not confirmed in Codex docs."},
    "antigravity": {"user": "~/.gemini/config/skills",     "project": ".agents/skills",   "conf": "weak",
                    "note": "Docs list ~/.gemini/config/skills (legacy ~/.gemini/antigravity/skills still works); "
                            "Antigravity does NOT read ~/.gemini/skills. Another page lists "
                            "~/.gemini/antigravity-cli/skills for the CLI variant."},
    "windsurf":    {"user": "~/.codeium/windsurf/skills",  "project": ".windsurf/skills", "conf": "ok"},
    "cline":       {"user": "~/.cline/skills",             "project": ".cline/skills",    "conf": "ok"},
    "roo":         {"user": "~/.roo/skills",               "project": ".roo/skills",      "conf": "ok"},
    "agents":      {"user": "~/.agents/skills",            "project": ".agents/skills",   "conf": "ok",
                    "note": "Cross-agent convention read by several tools (Gemini CLI, Roo, Cursor)."},
}


def skills():
    return sorted(p for p in REPO.iterdir() if p.is_dir() and (p / "SKILL.md").exists())


def is_link(p: Path) -> bool:
    if p.is_symlink():
        return True
    if os.name == "nt":
        try:
            # lstat does not follow the junction, so the reparse-point flag is visible
            return bool(os.lstat(p).st_file_attributes & 0x400)
        except (OSError, AttributeError):
            return False
    return False


def link_target(p: Path):
    try:
        return Path(os.path.realpath(p))
    except OSError:
        return None


def make_link(src: Path, dst: Path) -> None:
    if os.name == "nt":
        r = subprocess.run(["cmd", "/c", "mklink", "/J", str(dst), str(src)],
                           capture_output=True, text=True)
        if r.returncode != 0:
            raise OSError(r.stderr.strip() or r.stdout.strip())
    else:
        os.symlink(src, dst, target_is_directory=True)


def remove_link(p: Path) -> None:
    if os.name == "nt" and not p.is_symlink():
        subprocess.run(["cmd", "/c", "rmdir", str(p)], capture_output=True)  # removes junction only
    else:
        p.unlink()


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--agent", choices=sorted(AGENTS), default="claude",
                    help="preset skills directory for this agent (default: claude)")
    ap.add_argument("--scope", choices=["user", "project"], default="user",
                    help="user = your home directory; project = relative to the current directory")
    ap.add_argument("--target", help="explicit skills directory (overrides --agent/--scope)")
    ap.add_argument("--list-agents", action="store_true", help="show the preset paths and exit")
    ap.add_argument("--copy", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--uninstall", action="store_true")
    ap.add_argument("--force", action="store_true", help="replace an existing LINK that points elsewhere")
    ap.add_argument("--only", help="comma-separated skill names to install; others in this repo are skipped")
    ap.add_argument("--exclude", help="comma-separated skill names to skip")
    args = ap.parse_args()

    if args.list_agents:
        for name, p in sorted(AGENTS.items()):
            print(f"{name:12} user={p['user']:32} project={p['project']:18} [{p['conf']}]")
            if p["conf"] == "weak" or p.get("note"):
                print(f"{'':12} note: {p.get('note', 'verify against the agent docs')}")
        return 0

    preset = AGENTS[args.agent]
    if args.target:
        target = Path(args.target).expanduser()
    else:
        target = Path(preset[args.scope]).expanduser()
        if args.scope == "project":
            target = Path.cwd() / target
        if preset["conf"] == "weak":
            print(f"warning: path for '{args.agent}' is not fully verified: {preset.get('note', '')}",
                  file=sys.stderr)
    print(f"target: {target}")
    names = skills()
    if not names:
        print("error: no skills found", file=sys.stderr)
        return 1
    if args.only:
        wanted = {n.strip() for n in args.only.split(",") if n.strip()}
        names = [s for s in names if s.name in wanted]
    if args.exclude:
        dropped = {n.strip() for n in args.exclude.split(",") if n.strip()}
        names = [s for s in names if s.name not in dropped]
    if not names:
        print("nothing to install here (no skill matches --only/--exclude)")
        return 0
    if not args.dry_run and not args.uninstall:
        target.mkdir(parents=True, exist_ok=True)

    rc = 0
    for src in names:
        dst = target / src.name
        try:
            if args.uninstall:
                if not dst.exists() and not is_link(dst):
                    print(f"absent    {src.name}")
                elif is_link(dst) and link_target(dst) == src.resolve():
                    if not args.dry_run:
                        remove_link(dst)
                    print(f"removed   {src.name}")
                else:
                    print(f"skipped   {src.name} (not a link to this repo; remove it yourself)")
                continue

            if dst.exists() or is_link(dst):
                if is_link(dst) and link_target(dst) == src.resolve():
                    print(f"ok        {src.name} (already linked)")
                elif is_link(dst) and args.force:
                    if not args.dry_run:
                        remove_link(dst)
                        make_link(src, dst)
                    print(f"replaced  {src.name}")
                else:
                    print(f"exists    {src.name} (left untouched)")
                continue

            if args.dry_run:
                print(f"would {'copy' if args.copy else 'link'} {src.name}")
            elif args.copy:
                shutil.copytree(src, dst, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
                print(f"copied    {src.name}")
            else:
                make_link(src, dst)
                print(f"linked    {src.name}")
        except OSError as e:
            rc = 1
            print(f"error     {src.name}: {e}", file=sys.stderr)
    return rc


if __name__ == "__main__":
    sys.exit(main())
