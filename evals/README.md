# Evals — self-check for the skills

Two manual check sets that work on any agent:

| File | Purpose |
|---|---|
| [trigger-prompts.md](trigger-prompts.md) | Prompts that should and should not trigger each skill (EN + VI) |
| [behavior-checks.md](behavior-checks.md) | Behavior scenarios: phase label, hard stops, anti-hallucination, sub-skill loading |

## How to run

1. Install the six `qa-*` skills side by side.
2. Open a fresh session (no earlier context) and paste each prompt.
3. Record which skill fired and whether it was the right one. Compute the hit rate for the "should" group and the false-trigger rate for the "should not" group.
4. For behavior checks, mark each criterion pass/fail.

**Suggested targets:** ≥ 90% of "should" prompts trigger the right skill; 0 "should not" prompts trigger a QA skill; every anti-hallucination criterion passes.

Results vary by agent and model; record which you used when reporting.
