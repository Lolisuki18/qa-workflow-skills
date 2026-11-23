# Worked Example — qa-lifecycle

> ⚠️ **Fictional** data to illustrate the format (imaginary app "DemoShop", Login feature). Do not use as real figures. The same scenario runs through the examples of all 6 skills.

## Turn 1 — Kickoff

**User:** "Do a proper QA for DemoShop's login feature. The spec is in `docs/auth-srs.md`."

**Sample response:**

```markdown
[QA Phase 0/5: Kickoff]

I read `docs/auth-srs.md`. Scope as I understand it: email + password login, account lockout after repeated failures, and permission control on /admin. There is no "forgot password" requirement, so I will keep it out of scope unless you say otherwise.

Two quick questions:
1. Should `qa-artifacts/` be (a) added to `.gitignore` or (b) kept in the repo? — My default is (b) if you need to share reports with your team.
2. Where will tests run (URL/build)? — [Needs input: test environment]

> **QA Advisor**
> - *Why it matters:* login is the door to every feature; a bug here blocks all users.
> - *Blind spots:* lockout (how failures are counted, when it unlocks), regular users reaching /admin, double-clicking the login button.
> - *Default:* I will keep `qa-artifacts/` in the repo and start Phase 1 as soon as you answer.
```

## Turn 2 — End of Phase 1 (Hard Stop)

```markdown
[QA Phase 1/5: Test Plan]

Saved `qa-artifacts/01-test-plan.md` (Draft). Top findings: REQ-03 does not say when the failure counter resets; REQ-04 does not say what happens when access is denied (redirect or 403).

**⏸ HARD STOP — awaiting approval**
Please answer the 2 open questions (or accept the stated defaults), then reply "approved" to start Phase 2.
```

**Takeaways:** phase label on the first line; `.gitignore` asked exactly once; advisor block with a default; a real stop, no auto-advance to Phase 2.
