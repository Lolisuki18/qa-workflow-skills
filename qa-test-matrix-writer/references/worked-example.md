# Worked Example — qa-test-matrix-writer

> ⚠️ **Fictional** data ("DemoShop", Login feature) to illustrate the format. Assumes the user accepted the Phase 1 defaults.

## Test cases

| TC ID | Req/UC ID | Module | Title | Pre-condition | Test Steps | Test Data | Expected Result | Oracle | Priority | Execution Type |
|---|---|---|---|---|---|---|---|---|---|---|
| TC-LOGIN-001 | REQ-01 | Login | Correct login redirects to dashboard | User `user_a@example.test` exists, not locked | 1. Open /login 2. Enter email, password 3. Click Login | email `user_a@example.test`; valid password | Redirected to `/dashboard` | `spec` | P0 | Auto (browser) |
| TC-LOGIN-002 | REQ-02 | Login | Wrong password shows error, stays on page | Same as above | 1. Open /login 2. Enter correct email, wrong password 3. Click Login | password `wrong-pass-1` | Error message shown `[Needs input: exact message]`; URL still `/login` | `none` | P0 | Auto (browser) |
| TC-LOGIN-003 | REQ-02 | Login | Empty email is blocked | /login open | 1. Leave email empty 2. Enter password 3. Click Login | empty email | Login not submitted; email-required message | `spec` | P1 | Auto (browser) |
| TC-LOGIN-004 | REQ-03 | Lockout | 5th failure locks the account | Account `lock_test@example.test` with 0 failures | 1. Send 5 consecutive wrong logins 2. Send a 6th with the correct password | wrong password x5, then correct | 6th attempt rejected due to lock | `spec` | P1 | Auto (API) |
| TC-LOGIN-005 | REQ-03 | Lockout | 4 failures then correct still succeeds (boundary) | Account with 0 failures | 1. Fail 4 times 2. Log in correctly | wrong password x4, then correct | Login succeeds | `spec` | P1 | Auto (API) |
| TC-LOGIN-006 | REQ-04 | Authz | Regular user blocked from /admin | Logged in as regular user | 1. Type /admin directly in the address bar | role User | Redirected to `/dashboard` with a message | `approved default` | P0 | Auto (browser) |
| TC-LOGIN-007 | REQ-01 | Login | Double-clicking Login causes no error/duplicate session | /login open, valid data entered | 1. Double-click Login quickly | — | Enters dashboard once, no error | `code behavior` | P2 | Manual |
| TC-LOGIN-008 | REQ-01 | Login | Network lost during login | /login open, valid data entered | 1. Turn network off 2. Click Login 3. Turn network on | — | Clear network error message, no hang | `code behavior` | P2 | Manual |
| TC-LOGIN-009 | REQ-04 | Authz | Admin can open /admin | Logged in as admin | 1. Open /admin | role Admin | Admin page displayed | `spec` | P0 | Auto (browser) |

Summary: **9 cases** — P0: 4, P1: 3, P2: 2, P3: 0 · Manual: 2, Auto (browser): 5, Auto (API): 2.

## RTM

| Req/UC ID | Requirement | Happy path | Negative | Permission | Coverage |
|---|---|---|---|---|---|
| REQ-01 | Correct login | TC-LOGIN-001 | TC-LOGIN-007, 008 | N/A (not logged in yet) | Full |
| REQ-02 | Error on wrong/empty | N/A (requirement describes errors) | TC-LOGIN-002, 003 | N/A | Full |
| REQ-03 | Lock after 5 failures | TC-LOGIN-005 | TC-LOGIN-004 | N/A | Full |
| REQ-04 | Only Admin opens /admin | TC-LOGIN-009 | — | TC-LOGIN-006 | Full |

Coverage: 4/4 requirements = 100%. Orphan cases: none.

**Takeaways:** concrete Test Data; unknown messages kept as `[Needs input]`; boundary case (4 vs 5 failures) and permission case present; RTM percentage computed from the real table.
