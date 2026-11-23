# Test Design Techniques

Six techniques for generating test cases systematically. Examples use **illustrative** numbers — when applying for real, take thresholds/rules from the spec or code; if missing, write `[Needs input: ...]`.

## Quick technique picker

| Situation in the requirement | Main technique | Combine with |
|---|---|---|
| Input fields with ranges/formats/lengths | Equivalence Partitioning | Boundary Value Analysis |
| Quantities, prices, lengths, dates, paging, limits | Boundary Value Analysis | Equivalence Partitioning |
| Several conditions combine into different outcomes (discounts, approvals) | Decision Table | Boundary Value Analysis |
| Objects with lifecycle/states (orders, tickets, accounts) | State Transition | Error Guessing |
| Multiple roles with different permissions | Role-Based Access Control | State Transition |
| Every feature, as the last step | Error Guessing | — |

---

## 1. Equivalence Partitioning (EP)

**Idea:** split the input domain into partitions the system treats "the same way"; test one representative per partition. Include both **valid** and **invalid** partitions.

**How**
1. List each input and its rules.
2. Partition: valid (several partitions if handled differently) and invalid (below, above, wrong type, empty, null, wrong format).
3. ≥ 1 test case per partition. Do not merge two invalid partitions in one case (hard to tell which caused the failure).

**Illustrative example:** field "Age" requires an integer 18–60.

| Partition | Type | Representative |
|---|---|---|
| < 18 | Invalid | 10 |
| 18–60 | Valid | 30 |
| > 60 | Invalid | 75 |
| Not a number | Invalid | `abc` |
| Decimal | Invalid | `25.5` |
| Empty | Invalid | (left blank) |
| Negative | Invalid | `-5` |

**Common misses:** the empty/whitespace partition, wrong data types, special characters/Unicode (accents, emoji) in text fields.

---

## 2. Boundary Value Analysis (BVA)

**Idea:** defects cluster at boundaries (`<` vs `<=`, off-by-one). Test at and right next to each boundary.

**How (2-value or 3-value)**
- For range [min, max]: test `min-1`, `min`, `min+1`, `max-1`, `max`, `max+1`.
- Boundaries of quantities, string lengths, file sizes, dates/times, last page, number of list items (0, 1, many, max).

**Illustrative example:** password of 8–20 characters.

| Value | Length | Expected |
|---|---|---|
| min-1 | 7 | Rejected |
| min | 8 | Accepted |
| min+1 | 9 | Accepted |
| max-1 | 19 | Accepted |
| max | 20 | Accepted |
| max+1 | 21 | Rejected |

**Boundaries worth remembering:** 0 and 1 items; first/last/out-of-range page; end of month, leap year, time-zone/DST changes; money rounding (0.01, 0.005); file exactly at the size limit; multi-byte strings (count characters or bytes?).

---

## 3. Decision Table

**Idea:** when the outcome depends on a **combination** of conditions, list every combination (or a justified reduction) with its outcome; each rule column = one test case.

**How**
1. List conditions (Y/N or values) and actions/outcomes.
2. n Y/N conditions give 2ⁿ combinations; reduce impossible combinations or ones with identical outcomes — state why.
3. Each rule → 1 test case with concrete data.

**Illustrative example:** checkout discount.

| Condition | R1 | R2 | R3 | R4 |
|---|---|---|---|---|
| Is a member | Y | Y | N | N |
| Has valid coupon | Y | N | Y | N |
| **Action** | | | | |
| Apply member discount | ✔ | ✔ | — | — |
| Apply coupon | ✔* | — | ✔ | — |
| Full price | — | — | — | ✔ |

(*) Whether discounts stack is **unclear** → raise as a clarifying question, never assume.

**Common misses:** the "all false" combination; not asking about priority/stacking order of rules.

---

## 4. State Transition

**Idea:** an object has states and events that move it between states. Test **valid** transitions and deliberately attempt **invalid** ones.

**How**
1. Draw/list states, events, conditions (guards), actions.
2. Build a state × event table. Valid cells → test the correct transition. Invalid cells → test rejection and that the state is unchanged.
3. Cover at least: every valid transition (0-switch); important sequences (1-switch, e.g. Cancel then Restore); final states (no way out).

**Illustrative example:** an order.

| State \ Event | Pay | Ship | Cancel | Refund |
|---|---|---|---|---|
| New | Paid | ✗ | Cancelled | ✗ |
| Paid | ✗ | Shipping | Cancelled* | ✗ |
| Shipping | ✗ | Delivered | ✗ | ✗ |
| Delivered | ✗ | ✗ | ✗ | Refunded |

(✗ = invalid, must be rejected. *Does cancelling after payment auto-refund? → needs clarification.)

**Blind spots:** repeated actions (clicking "Pay" twice), two people changing state at once (race condition), calling the state-change API directly bypassing the UI, using Back after a state change.

---

## 5. Role-Based Access Control (RBAC)

**Idea:** every (role × action × resource) triple has an allow/deny outcome. Permission bugs are often serious security bugs → usually P0/P1.

**How**
1. List roles (including **guest/not logged in** and **expired session**), actions, resource types.
2. Build the expected permission matrix from the spec (missing → ask; never infer).
3. Test:
   - Each **allowed** cell → succeeds.
   - Each **denied** cell → rejected properly (hidden button **and** blocked at server/API level: hit the URL/endpoint directly).
   - **Horizontal:** user A accesses user B's resource (change the ID in the URL/request).
   - **Vertical:** a regular user calls an admin function.
   - Change role/revoke permission while logged in → when does it take effect?

**Illustrative example**

| Action | Guest | User (owner) | User (other) | Admin |
|---|---|---|---|---|
| View post | ✔ | ✔ | ✔ | ✔ |
| Edit post | ✗ | ✔ | ✗ | ✔ |
| Delete post | ✗ | ✔ | ✗ | ✔ |
| View admin page | ✗ | ✗ | ✗ | ✔ |

**On denial results:** state the expectation (redirect to login / message / 401 vs 403 vs 404) — if the spec is silent, write `[Needs input: behavior when denied]`.

---

## 6. Error Guessing

**Idea:** use experience to add cases beyond the systematic techniques. Run it last, as a safety net. Tag the source (e.g. tag `EG`) for traceability.

**Suggestion list (choose by feature, do not apply mechanically)**

| Group | Case ideas |
|---|---|
| Repeated actions | Double-click submit/pay; submit the form from two tabs at once; F5 after submit (resubmit) |
| Navigation | Back/Forward mid multi-step flow; open a deep link while logged out; close the tab mid-way |
| Network | Network loss/timeout mid-submit; slow network; server returns 500; delayed response making users click again |
| Session | Session expires while filling a form; login on two devices; log out in another tab |
| Text data | Empty, whitespace only, very long; special characters `' " < > & %`; accented text, emoji; `<script>`/SQL-like strings (check proper escaping — never attack a system that is not yours) |
| Numbers/dates | 0, negative, huge, decimals, `,` vs `.` formats; Feb 29, time zones, past/future dates |
| Files | 0-byte, oversize, wrong extension/MIME, special/very long file names, re-uploading the same file |
| Environment | Different browser, small screen, JavaScript/cookies off, 200% zoom |
| Existing data | Duplicates (already-registered email), deleted record with a lingering link, empty list, huge list |
| Concurrency | Two people editing one record; deleting a record while someone views it |

**Writing the case:** still the standard columns; Title states the situation; Priority by real risk (not default P3); mostly `Manual` or `Auto (API)`.

---

## Combined routine for one requirement

1. Identify the requirement type → pick techniques from the picker.
2. Generate cases with the main technique, then the combined ones.
3. Add permission cases if the requirement involves roles.
4. Add 1–3 feature-specific Error Guessing cases.
5. Remove duplicates (same partition, same outcome) to keep the table lean but covering.
6. Attach Req/UC ID, Priority, Execution Type; feed the RTM.

## Spotting duplicates / redundancy

- Two cases with the same Req, same EP partition, same outcome → keep one.
- Cases differing only in data but sharing the flow → consider one case with several Test Data rows (data-driven), especially for `Auto`.
- Never cut P0/P1 cases just because the table is long.
