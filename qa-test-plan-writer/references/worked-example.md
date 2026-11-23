# Worked Example — qa-test-plan-writer

> ⚠️ **Fictional** data ("DemoShop", Login feature) to illustrate the format. Do not use as real figures.

**Input (summary of an imaginary spec):**
- REQ-01: Logging in with correct email + password redirects to `/dashboard`.
- REQ-02: A wrong or empty password shows an error and stays on the login page.
- REQ-03: 5 consecutive failures lock the account for 15 minutes.
- REQ-04: Only the Admin role can open `/admin`.

## Requirement Audit

| # | Requirement | Issue | Type | Clarifying question | Suggested default |
|---|---|---|---|---|---|
| 1 | REQ-03 | Does not say when the failure counter resets (on success? after 15 min?) | Ambiguity | When does the counter reset? | Reset on successful login or after 15 minutes |
| 2 | REQ-04 | No behavior stated when access is denied (redirect / 403 / 404) | Missing error flow | What does a regular user see at `/admin`? | Redirect to `/dashboard` with a message; API returns 403 |
| 3 | REQ-02 | One generic error or separate "wrong email" / "wrong password"? | Ambiguity | Choose one | One generic message (avoids revealing which emails exist) |
| 4 | REQ-01 | Session lifetime not stated | Missing non-functional | Session timeout? | [Needs input: session timeout] |

## Scope
- In-scope: REQ-01…REQ-04, desktop browsers, roles Guest / User / Admin.
- Out-of-scope: forgot password (no requirement), social login (not built yet).

## Risk Analysis
| Area | Likelihood | Impact | Test priority |
|---|---|---|---|
| /admin permissions | M | H | High |
| Account lockout | M | M | Medium |
| Main login | L | H | High |

## Strategy
| Area | Manual | Auto (browser) | Auto (API) | Reason |
|---|---|---|---|---|
| Main login, UI permissions | | ✔ | | Core flow, repeated every release |
| Account lockout | | | ✔ | Needs many fast calls, counter inspection |
| Double-click, network drop | ✔ | | | Hard to automate reliably |

## Environment & data
- Environment / build: [Needs input: URL and build]
- Browser: [Needs input: browser and version]
- Accounts: 1 regular user, 1 admin, 1 account reserved for lockout tests.

## Entry / Exit (proposed — to be confirmed)
- Entry: build runs in the test environment, smoke test passes.
- Exit: 100% of P0 cases pass, no open Blocker/Critical, RTM covers 100% of in-scope requirements.

**Takeaways:** every question has a default; unknowns use `[Needs input: ...]`; no "Chrome 120" invented for the environment.
