# Enforcing the QA hard stops

`qa-lifecycle` must stop after Phase 1 (test plan) and Phase 2 (test matrix). Written rules can be ignored in a long conversation, so three layers back them up.

1. **Anchor (built in):** every reply starts with `[QA Phase X/5: ...]`.
2. **Artifact status (built in):** each `qa-artifacts/[<module>/]0N-*.md` has `Status: Draft | Approved` in its header. The agent sets `Approved` only after the user says so.
3. **Hook (optional, Claude Code):** [`scripts/qa-gate.py`](../scripts/qa-gate.py) is a PreToolUse hook that refuses Write/Edit on `02-*` and `02b-*` while `01-*` is Draft, and on `03-*` and `03c-*` while `02-*` (or `02b-*`, when it exists) is Draft. Phases 4 and 5 are never blocked, a missing prerequisite is allowed (the phase was skipped at the user's request), and any error fails open.

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

### Module folders

The hook gates `qa-artifacts/<module>/` one level deep, each folder against its own prerequisites. `.no-gate` and `QA_GATE` are global (they bypass every module). Deeper paths (for example `<module>/tools/`) and Bash writes such as `cp` or `cd dir && echo > file` are not caught. The status key `Status:` must stay English, even when the artifact is written in another language.

### What the hook does not cover

- The default matcher `Write|Edit` checks only Write/Edit tool calls. A write made through Bash (`echo > file`, `tee`, `sed -i`, a Python script) is not seen by that matcher.
- Optional: add a `Bash` matcher to the same hook. For Bash the script reads `tool_input.command` and blocks only conservatively: the command must name `qa-artifacts/02-`, `02b-` or `03-` and look like a write (redirect, `tee`, `sed -i`, `Set-Content`/`Out-File`, `python` with `open(`/`write`). A script that builds the path at run time still gets through. Fails open as before.

```json
{ "matcher": "Write|Edit|Bash", "hooks": [ { "type": "command", "command": "python /path/to/qa-workflow-skills/scripts/qa-gate.py" } ] }
```

- The hook cannot tell who set `Approved`: an agent could edit the status itself. The skills forbid it, the hook does not.
- The hook does not block running tests or commands; it only guards the artifact files. Executing tests before the matrix is approved is prevented by the written rule alone.

Bypass on purpose only: set `QA_GATE=off`, or create an empty `qa-artifacts/.no-gate`. The block message tells the agent to ask you first and never to bypass by itself.

Tests: `python -m unittest discover -s tests -v`. Not yet checked with a real Claude Code session.

The docs skill set has no equivalent: its Phase 1 hard stop approves a file list in the conversation, not a stored artifact, so there is nothing for a hook to read.
