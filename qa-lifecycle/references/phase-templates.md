# Phase Templates — qa-lifecycle

Templates for the 5 files in `qa-artifacts/` (or `qa-artifacts/<module>/` in a module run; file names and cross references such as "see 02-test-matrix.md" are relative to that folder). Anywhere real data is missing, write `[Cần bổ sung: ...]` (or `[Needs input: ...]`). Never invent numbers.

## Common header (top of every file)

```markdown
# <Document name> — <Feature/release name>
- **Phase:** X/5 — <Phase name>
- **Date:** YYYY-MM-DD
- **Version:** v0.1
- **Status:** Draft | Approved (approved on: ...)
- **Requirement source:** <SRS / Use Case / ticket / code path>
- **Approver:** [Needs input: ...]
```

---

---

## QA Advisor block (append at the end of each phase)

```markdown
> **QA Advisor**
> - *Why it matters:* ...
> - *Blind spots to watch:* ...
> - *Default I will choose if you do not reply:* ...
```

## Hard Stop block

```markdown
**⏸ HARD STOP — awaiting approval**
I saved `qa-artifacts/[<module>/]0X-....md` (Draft). Please:
1. Answer the open questions (or accept the stated defaults).
2. Reply "approved" to move to the next phase, or tell me what to change.
```
