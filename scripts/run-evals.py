#!/usr/bin/env python3
"""Run the trigger prompts in evals/trigger-prompts.md against an agent CLI and report hit rates.

Standard library only. Agent-agnostic: you supply the command template; the script
detects which qa-* skills fired and compares them with the expectation in the table.

Expectation rules (per section "## qa-xxx" in trigger-prompts.md):
  ✅ row                      -> skill qa-xxx must fire
  ❌ row without "→ `qa-yyy`"  -> skill qa-xxx must NOT fire
  ❌ row with    "→ `qa-yyy`"  -> qa-xxx must NOT fire and qa-yyy must fire
The "Ambiguous prompts" table is skipped (it expects a clarifying question, not a skill).

Examples
  python scripts/run-evals.py --dry-run
  python scripts/run-evals.py --only qa-defect-writer --out evals/results.md
  python scripts/run-evals.py --cmd 'my-agent --prompt {prompt}' --detect-regex 'qa-[a-z0-9-]+'

WARNING: each prompt is really sent to the agent, which may read files or write artifacts.
Run it in a scratch workspace with the six qa-* skills installed, and expect real usage costs.
"""
import argparse, json, re, shlex, subprocess, sys, time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_PROMPTS = ROOT / "evals" / "trigger-prompts.md"
# Default targets Claude Code's non-interactive mode (stream-json lists Skill tool calls).
# Verify the flags with `claude --help` for your installed version.
DEFAULT_CMD = "claude -p {prompt} --output-format stream-json --verbose"
SKILL_RE = re.compile(r"qa-[a-z0-9-]+")


def parse_cases(path):
    cases, section = [], None
    for line in path.read_text(encoding="utf-8").splitlines():
        h = re.match(r"^##\s+(qa-[a-z0-9-]+)\s*$", line)
        if h:
            section = h.group(1)
            continue
        if line.startswith("## "):
            section = None  # e.g. the ambiguous-prompts section
            continue
        m = re.match(r"^\|\s*(✅|❌)\s*\|\s*(.+?)\s*\|\s*$", line)
        if not (m and section):
            continue
        mark, text = m.groups()
        target = None
        arrow = re.search(r"→\s*`(qa-[a-z0-9-]+)`", text)
        if arrow:
            target = arrow.group(1)
            text = text[: arrow.start()].strip()
        text = re.sub(r"\s*\([^)]*\)\s*$", "", text).strip() if mark == "❌" and not target else text
        cases.append({"section": section, "should": mark == "✅", "prompt": text, "target": target})
    return cases


def detect_skills(output, detect_regex):
    """Return the set of qa-* skills the agent loaded."""
    fired = set()
    for raw in output.splitlines():
        raw = raw.strip()
        if not raw.startswith("{"):
            continue
        try:
            obj = json.loads(raw)
        except json.JSONDecodeError:
            continue
        stack = [obj]
        while stack:  # walk nested JSON for Skill tool calls
            cur = stack.pop()
            if isinstance(cur, dict):
                if cur.get("type") == "tool_use" and str(cur.get("name", "")).lower() == "skill":
                    inp = cur.get("input") or {}
                    for v in (inp.get("skill"), inp.get("name")):
                        if isinstance(v, str):
                            fired.update(SKILL_RE.findall(v))
                stack.extend(cur.values())
            elif isinstance(cur, list):
                stack.extend(cur)
    if not fired and detect_regex:  # fallback for agents without structured output
        fired.update(re.findall(detect_regex, output))
    return fired


def evaluate(case, fired):
    sec, tgt = case["section"], case["target"]
    if case["should"]:
        return sec in fired
    return sec not in fired and (tgt is None or tgt in fired)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--prompts", default=str(DEFAULT_PROMPTS))
    ap.add_argument("--cmd", default=DEFAULT_CMD, help="command template; {prompt} is replaced per argument")
    ap.add_argument("--detect-regex", default=None, help="fallback regex on raw output, e.g. 'qa-[a-z0-9-]+'")
    ap.add_argument("--only", default=None, help="run only the section of this skill name")
    ap.add_argument("--timeout", type=int, default=300, help="seconds per prompt")
    ap.add_argument("--out", default=None, help="write a markdown report to this path")
    ap.add_argument("--dry-run", action="store_true", help="parse and list cases, run nothing")
    args = ap.parse_args()

    cases = parse_cases(Path(args.prompts))
    if args.only:
        cases = [c for c in cases if c["section"] == args.only]
    if not cases:
        sys.exit("No cases parsed. Check --prompts / --only.")

    if args.dry_run:
        for i, c in enumerate(cases, 1):
            exp = ("fire " + c["section"]) if c["should"] else (
                "not " + c["section"] + (", fire " + c["target"] if c["target"] else ""))
            print(f"{i:02d} [{c['section']}] expect: {exp}\n    {c['prompt']}")
        print(f"\n{len(cases)} cases parsed (nothing executed).")
        return

    rows = []
    for i, c in enumerate(cases, 1):
        argv = [a.replace("{prompt}", c["prompt"]) for a in shlex.split(args.cmd)]
        t0 = time.time()
        try:
            res = subprocess.run(argv, capture_output=True, text=True, timeout=args.timeout, encoding="utf-8", errors="replace")
            out, err = res.stdout, res.returncode
        except (subprocess.TimeoutExpired, FileNotFoundError) as e:
            out, err = "", f"error: {e}"
        fired = detect_skills(out, args.detect_regex)
        ok = evaluate(c, fired) if err in (0, None) or out else False
        rows.append({**c, "fired": sorted(fired), "ok": ok, "status": err, "secs": round(time.time() - t0, 1)})
        print(f"{i:02d}/{len(cases)} {'PASS' if ok else 'FAIL'} [{c['section']}] fired={sorted(fired) or '-'} ({rows[-1]['secs']}s)")

    for label, grp in (("should-trigger", [r for r in rows if r["should"]]),
                       ("should-not-trigger", [r for r in rows if not r["should"]])):
        if grp:
            p = sum(r["ok"] for r in grp)
            print(f"{label}: {p}/{len(grp)} = {100 * p / len(grp):.1f}%")

    if args.out:
        lines = ["# Eval results", "", f"Command: `{args.cmd}`", "",
                 "| # | Skill section | Should fire | Fired | Result | Prompt |", "|---|---|---|---|---|---|"]
        for i, r in enumerate(rows, 1):
            lines.append(f"| {i} | {r['section']} | {'yes' if r['should'] else 'no'} | {', '.join(r['fired']) or '-'} | "
                         f"{'PASS' if r['ok'] else 'FAIL'} | {r['prompt'].replace('|', '/')} |")
        Path(args.out).write_text("\n".join(lines) + "\n", encoding="utf-8")
        print(f"Report written to {args.out}")


if __name__ == "__main__":
    main()
