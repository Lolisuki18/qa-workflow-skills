# Enforcing the QA hard stops

`qa-lifecycle` must stop after Phase 1 (test plan) and Phase 2 (test matrix). Written rules can be ignored in a long conversation, so three layers back them up.

1. **Anchor (built in):** every reply starts with `[QA Phase X/5: ...]`.
2. **Artifact status (built in):** each `qa-artifacts/0N-*.md` has `Status: Draft | Approved` in its header. The agent sets `Approved` only after the user says so.
3. **Hook (optional, Claude Code):** [`scripts/qa-gate.py`](../scripts/qa-gate.py) is a PreToolUse hook that refuses Write/Edit on `02-*` and `02b-*` while `01-*` is Draft, and on `03-*` while `02-*` is Draft. Phases 4 and 5 are never blocked, a missing prerequisite is allowed (the phase was skipped at the user's request), and any error fails open.

Add to `.claude/settings.json` of the project under test (adjust the path; use `py` or `python3` if `python` is not on PATH):

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          { "type": "command", "command": "python /path/to/qa-workflow-skills/scripts/qa-gate.py" }
        ]
      }
    ]
  }
}
```

Bypass on purpose only: set `QA_GATE=off`, or create an empty `qa-artifacts/.no-gate`. The block message tells the agent to ask you first and never to bypass by itself.

Tests: `python -m unittest discover -s tests -v`. Not yet checked with a real Claude Code session.

The docs skill set has no equivalent: its Phase 1 hard stop approves a file list in the conversation, not a stored artifact, so there is nothing for a hook to read.
