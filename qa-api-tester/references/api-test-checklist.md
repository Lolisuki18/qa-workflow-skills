# API test checklist

Use per endpoint. Skip items that do not apply, and say why for risky endpoints.

## Per request

| Area | Checks |
|---|---|
| Success | Status code matches spec; body has required fields with the right types; `Content-Type` correct |
| Validation | Missing required field, wrong type, empty string, too long, below/above min/max, invalid format (email, date, UUID), unknown extra field |
| Auth | No credentials → 401; invalid or expired token → 401; valid token but wrong role → 403 |
| Object access | User A requests user B's resource by id → 403 or 404 (never B's data) |
| Not found | Unknown id → 404 with the documented error body |
| Conflict | Duplicate unique value → 409 (or documented code) |
| Idempotency | Repeat the same PUT/DELETE → same final state; repeat POST → duplicate or rejected as documented |
| Concurrency | Two updates at once; stale version/ETag if the API uses one |
| Pagination | First page, last page, page beyond range, size 0, size above the maximum |
| Filtering/sorting | Valid, invalid field, injection-like characters treated as data |
| Error body | Stable shape (code, message), no stack trace, no internal paths or SQL |
| Side effects | Database/state change as expected; related resources updated; nothing extra created |
| Data exposure | No password hashes, tokens, internal ids or other users' PII in any response |

## Priority guide

- **P0:** auth, payments, permission checks, data deletion, anything returning personal data.
- **P1:** core CRUD happy paths and main validation rules.
- **P2:** pagination, filtering, less common errors.
- **P3:** cosmetic response differences, optional fields.

## Test data

- Create data inside the test or through a seeded fixture; remove it afterwards.
- Use unique values (suffix with a run id) to avoid collisions in shared environments.
- Never reuse production data. Mask tokens and personal data in the notes.

## Result recording

```text
| TC ID | Endpoint | Request (summary) | Expected | Actual | Status | Evidence |
```

`Status`: Pass / Fail / Blocked / Not Run. Evidence is the report file and line, or the verbatim response with secrets masked.
