# Worked Example — qa-api-tester

> ⚠️ **Fictional** data and run results ("DemoShop") to illustrate the format. In real use, endpoints come from the real spec or code and every result is real output of a command you ran. Never copy these numbers into a real project.

## 1. Endpoint inventory (from `openapi.yaml`, read before writing tests)

```markdown
| Method | Path | Auth | Request | Success | Errors | Source |
|---|---|---|---|---|---|---|
| POST | /auth/login | none | email, password (both required) | 200 + token | 400 missing field, 401 bad credentials | openapi.yaml:12 |
| GET | /orders/{id} | Bearer | path id | 200 | 401 no token, 403 other user's order, 404 unknown id | openapi.yaml:41 |
| POST | /orders | Bearer | items[], qty >= 1 | 201 | 400 invalid qty, 401 | openapi.yaml:70 |

Undocumented: error body shape → `[Needs input: error body schema]`.
```

## 2. One test per case, TC ID in the title (Playwright `APIRequestContext`, shortened)

```ts
test('TC-API-003: user A cannot read user B\'s order', async ({ request }) => {
  const res = await request.get(`/orders/${process.env.ORDER_ID_OF_USER_B}`, {
    headers: { Authorization: `Bearer ${process.env.TOKEN_USER_A}` },
  });
  expect(res.status()).toBe(403);
});
```

Credentials and ids come from environment variables; nothing secret is stored in the file.

## 3. Results recorded in `03-execution-notes.md` (fictional numbers)

```markdown
### API track
Environment: staging-test (name given by the user) · Build: [Needs input] · Command: `npx playwright test --reporter=json api/` · Report file: `api-results.json`

| TC ID | Endpoint | Expected | Actual | Status | Evidence |
|---|---|---|---|---|---|
| TC-API-001 | POST /auth/login | 200 + token | 200 | Pass | api-results.json |
| TC-API-002 | POST /auth/login | 401 | 401 | Pass | api-results.json |
| TC-API-003 | GET /orders/{id} (other user) | 403 | 200 with the order body | **Fail** | api-results.json; DEF-004 |
| TC-API-004 | POST /orders qty 0 | 400 | 400 | Pass | api-results.json |
| TC-API-005 | GET /orders/{id} unknown | 404 | Not run | Blocked | test data id missing |
```

TC-API-003 reproduced by hand with the same request: a product defect (object-level access) → Phase 4, severity High.

## 4. When nothing can run

```markdown
All 5 Auto (API) cases: **Blocked**. Cause: no reachable server (`curl` to the base URL timed out, exit 28) and no environment named. 0 Pass / 0 Fail. Questions: base URL of a test environment, whether write calls are allowed there, which runner to use.
```
