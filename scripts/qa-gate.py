#!/usr/bin/env python3
"""OPTIONAL Claude Code PreToolUse hook: enforce the two QA hard stops with the artifact status.

qa-lifecycle stops after Phase 1 (test plan) and Phase 2 (test matrix) and waits for approval.
The approval is stored in the artifact header (`Status: Draft | Approved`). This hook refuses
Write/Edit calls that start the next phase while the previous artifact is still Draft:

  qa-artifacts/02-*.md and 02b-*.md   need  01-*.md  with Status: Approved
  qa-artifacts/03-*.md, 03c-*.md      need  02-*.md  with Status: Approved, and 02b-*.md too when one exists

Write/Edit calls are always checked. A Bash call is checked only conservatively: when the command text
both names `qa-artifacts/02*-`/`03*-` and looks like a write (redirect, tee, sed -i, Set-Content/Out-File,
python open/write). Anything else through Bash is not seen. The hook cannot tell who set Approved and does
not block running tests.

Module folders: `qa-artifacts/<module>/` is gated one level deep, each folder on its own prerequisites;
deeper paths (e.g. `<module>/tools/`) are not checked.

Phases 4 and 5 have no hard stop and are never blocked. A missing prerequisite file is allowed (the
phase was skipped at the user's request and the skill records that). Edits to the prerequisite
itself are always allowed, so the agent can set Approved after the user says so.

Reads the hook JSON from stdin. Exit 0 = allow, exit 2 = block (stderr is shown to the agent).
Fails OPEN on any parse problem so it never bricks a session.
Bypass (ask the user first): environment variable QA_GATE=off, or an empty file qa-artifacts/.no-gate.
Opt-in: see docs/hard-stop-enforcement.md.
"""
import json
import os
import re
import sys
from pathlib import Path

STATUS_RE = re.compile(r"(?im)^[\s>*\-]*\**status\**\s*:\s*\**\s*(draft|approved)")
NEEDS = [(re.compile(r"^02b?-"), ["01-"]), (re.compile(r"^03[a-z]?-"), ["02-", "02b-"])]
BASH_TARGET_RE = re.compile(r"qa-artifacts[/\\]+(?:([\w.\-]+)[/\\]+)?(0(?:2b?|3[a-z]?)-[\w.\-]*)")
BASH_WRITE_RE = re.compile(
    r">>?\s*['\"]?\S*qa-artifacts|\btee\b[^|;&\n]*qa-artifacts|\bsed\s+(?:-\w+\s+)*-i|"
    r"\b(?:Set-Content|Add-Content|Out-File)\b|\bpython3?\b.*(?:open\(|write)", re.I | re.S)


def find_root(start: Path) -> Path:
    for p in [start, *start.parents]:
        if (p / "qa-artifacts").is_dir() or (p / ".git").exists():
            return p
    return start


def status_of(path: Path):
    m = STATUS_RE.search(path.read_text(encoding="utf-8")[:3000])
    return m.group(1).lower() if m else None


def check(art: Path, root: Path, name: str) -> int:
    for pattern, prefixes in NEEDS:
        if pattern.match(name):
            for prefix in prefixes:
                for prereq in sorted(art.glob(prefix + "*.md")):
                    if status_of(prereq) == "draft":
                        print(
                            f"BLOCKED by qa-gate: {prereq.relative_to(root).as_posix()} is still 'Status: Draft'. "
                            "Show the summary and open questions, wait for the user's explicit approval, then set "
                            "Status: Approved in that file. Never approve it yourself. If the user wants to skip the "
                            "stop, ask them to set QA_GATE=off or create qa-artifacts/.no-gate.",
                            file=sys.stderr,
                        )
                        return 2
    return 0


def main() -> int:
    try:
        data = json.load(sys.stdin)
        tool_input = data.get("tool_input") or {}
        cwd = Path(data.get("cwd") or ".").resolve()
        root = find_root(cwd)
        art = root / "qa-artifacts"
        if not art.is_dir():
            return 0
        if os.environ.get("QA_GATE", "").lower() in ("off", "0", "false") or (art / ".no-gate").exists():
            return 0
        command = tool_input.get("command")
        if isinstance(command, str):
            if not BASH_WRITE_RE.search(command):
                return 0
            for mod, name in BASH_TARGET_RE.findall(command):
                target_art = (art / mod) if mod else art
                if target_art.is_dir() and check(target_art, root, name) == 2:
                    return 2
            return 0
        file_path = tool_input.get("file_path") or tool_input.get("path")
        if not file_path:
            return 0
        target = Path(file_path)
        if not target.is_absolute():
            target = (cwd / target).resolve()
        try:
            rel = target.relative_to(art)
        except ValueError:
            return 0
        if len(rel.parts) not in (1, 2):
            return 0
        return check(target.parent, root, rel.name)
    except Exception:
        return 0


if __name__ == "__main__":
    sys.exit(main())
