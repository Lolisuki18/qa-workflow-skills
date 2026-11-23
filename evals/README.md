# Evals — self-check for the skills

Two manual check sets that work on any agent:

| File | Purpose |
|---|---|
| [trigger-prompts.md](trigger-prompts.md) | Prompts that should and should not trigger each skill (EN + VI) |
| [behavior-checks.md](behavior-checks.md) | Behavior scenarios: phase label, hard stops, anti-hallucination, sub-skill loading |

## How to run

1. Install the nine `qa-*` skills side by side.
2. Open a fresh session (no earlier context) and paste each prompt.
3. Record which skill fired and whether it was the right one. Compute the hit rate for the "should" group and the false-trigger rate for the "should not" group.
4. For behavior checks, mark each criterion pass/fail.

**Suggested targets:** ≥ 90% of "should" prompts trigger the right skill; 0 "should not" prompts trigger a QA skill; every anti-hallucination criterion passes.

Results vary by agent and model; record which you used when reporting.

## Automating the trigger prompts

[`scripts/run-evals.py`](../scripts/run-evals.py) (Python 3, standard library only) parses `trigger-prompts.md`, sends each prompt to an agent CLI, detects which `qa-*` skills fired, and prints pass/fail plus the hit rate for each group. The "Ambiguous prompts" table and `behavior-checks.md` stay manual.

```powershell
python scripts/run-evals.py --dry-run                                  # list parsed cases, run nothing
python scripts/run-evals.py --only qa-defect-writer --out evals/results.md
python scripts/run-evals.py --cmd 'my-agent --prompt {prompt}' --detect-regex 'qa-[a-z0-9-]+'
```

- The default command targets Claude Code's non-interactive mode and reads `Skill` tool calls from its stream-json output. That default has **not been verified against a real CLI run**: check the flags with `claude --help`, and for other agents pass your own `--cmd` plus `--detect-regex` (the fallback just searches the raw output for skill names, so it can over-count).
- Every prompt really goes to the agent and may read files or write artifacts. Use a scratch workspace with the nine skills installed, and expect real usage costs.
- Rules: a ✅ row passes when its section's skill fires; a ❌ row passes when that skill does not fire (and, if the row ends with `→ qa-other`, when `qa-other` fires).
