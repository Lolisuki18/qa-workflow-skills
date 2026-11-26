# Worked Example — qa-defect-writer

> ⚠️ **Fictional** data ("DemoShop") to illustrate the format.

**Raw user description:** "a regular user can still open /admin by typing it, probably a permission bug."

## Consolidated questions (not piecemeal)

1. Environment/build and browser where you saw it? 2. How many attempts, how many reproduced? 3. Any screenshot/log?

User replies: "tried 3 times, every time; I have a screenshot; staging, I don't remember the build."

## Defect Report

```markdown
### DEF-001 — [Authz] Regular user can open the /admin page by typing the URL directly
| Field | Content |
|---|---|
| Title | [Authz] Regular user can open the /admin page by typing the URL directly |
| Related TC | TC-LOGIN-006 |
| Environment | Staging; build [Needs input]; browser [Needs input] |
| Severity / Priority | Critical / P0 (proposed) — Unauthorized access to the admin area, no workaround; PO to confirm Priority |
| Status | New |
| Reproducibility | Always (3/3) |
| Pre-conditions | Logged in with a User-role account |
| Steps to Reproduce | 1. Log in as a regular user 2. Type `/admin` directly in the address bar |
| Actual Result | The admin page is displayed |
| Expected Result | Redirected to `/dashboard` with a message (source: REQ-04, Phase 1 default) |
| Evidence | Screenshot provided by the user; log: none yet |
| Notes / Hypothesis (unconfirmed) | Possibly blocked only in the UI and not on the server — developers to check; QA has not verified |
```

## Re-test & Regression after the developer says "fixed"

```markdown
Build containing the fix: [Needs input]
1. Re-test the original bug: rerun DEF-001's Steps as a regular user; add a variant: call the admin API directly with the regular user's token.
2. Related regression (RTM, same REQ-04): TC-LOGIN-009 (Admin can still enter), TC-LOGIN-001.
3. Previously failed in this module: [no Closed defects yet]
Re-run in Playwright: TC-LOGIN-006, 009. Manual: the API variant.
```

Only when the user reports real results change Status to `Closed` (or `Reopened`) and add to "Re-test history".

**Takeaways:** Severity separate from Priority with a reason; missing environment as `[Needs input]`; hypothesis separated and flagged as unconfirmed.
