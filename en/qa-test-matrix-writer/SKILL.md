---
name: qa-test-matrix-writer
description: Designs a complete test case table (TC ID, Req/UC ID, Module, Title, Pre-condition, Steps, Test Data, Expected Result, Priority P0-P3, Execution Type) using test design techniques, plus a Requirement Traceability Matrix (RTM) proving every requirement has happy-path, negative and permission coverage, exportable as Markdown or clean CSV for Excel, Google Sheets or TestRail. Use when the user says 'write test cases', 'test matrix', 'traceability matrix', 'RTM', 'test case table', 'boundary value analysis', 'cover all requirements', 'viết test case', 'thiết kế test case', 'bảng test case', 'ma trận truy vết yêu cầu', 'xuất test case ra CSV'. Do NOT use for the test plan or requirement audit (use qa-test-plan-writer), writing Playwright code or manual run scripts (use qa-e2e-writer), logging defects (use qa-defect-writer), summary reports (use qa-summary-reporter), or developer unit tests.
---

# QA Test Matrix Writer — Step 2: Test Case Design

Generates a systematic test case table and an RTM proving requirement coverage. Inside `qa-lifecycle` this is Phase 2/5 and ends with a Hard Stop (label `[QA Phase 2/5: Test Matrix]` on the first line).

## Rules

- **Read first:** `references/test-design-techniques.md` (6 techniques). Apply the technique that fits each requirement instead of writing cases by gut feeling.
- **Input:** the approved `qa-artifacts/01-test-plan.md` (requirement IDs, scope, risks, strategy). No plan yet → warn and suggest running `qa-test-plan-writer` first; if the user still wants to go on, build a minimal requirement list with IDs and note the risk.
- **Anti-hallucination:** never invent business rules, limits, error messages or field names. If the spec gives no exact boundary/message → write the expected behavior plus `[Needs input: exact error message]`. Use clearly fake sample data (e.g. `user_a@example.test`), never real personal data.
- When testing an existing codebase: cross-check real validation/permission rules in code so Expected Results are correct, but if code contradicts the spec, record it under "Contradictions" and ask — never silently pick one.
- Each test case checks **one main idea**, is independent, and can run without other cases.

## Process

1. **Load requirements:** list every in-scope Req/UC ID from the test plan.
2. **Pick techniques** per requirement (guide table in the reference file). At minimum: a happy path, ≥ 1 negative, and if permissions apply ≥ 1 permission case.
3. **Generate test cases** with the standard columns (below). Group by Module; assign stable IDs `TC-<MODULE>-<3-digit number>` (e.g. `TC-LOGIN-001`).
4. **Assign Priority** from the plan's Risk Analysis (table below).
5. **Assign Execution Type** from the plan's strategy; if the plan is silent, use the hints below and mark as "proposed".
6. **Build the RTM** and self-check: any requirement missing Negative/Permission → add cases or record why "not applicable".
7. **Save and present** (last section).

## Required columns

| Column | Rule |
|---|---|
| `TC ID` | Unique, stable; do not renumber when a case is deleted |
| `Req/UC ID` | ≥ 1 ID; a case not traceable to a requirement → ask or tag `[Needs input: source requirement]` |
| `Module` | Matches the plan's modules |
| `Title` | Verb + condition + expected outcome, concise |
| `Pre-condition` | System/account/data state required before running |
| `Test Steps` | Numbered 1., 2., 3.; one action per step; followable by someone new to the system |
| `Test Data` | Concrete value per input (including boundary values); never a vague "valid data" |
| `Expected Result` | Observable and verifiable (what is shown, saved, which status code); never "works correctly" |
| `Priority` | `P0`–`P3` |
| `Execution Type` | `Manual` / `Auto (browser)` / `Auto (API)` |

## Priority P0–P3

| Level | Meaning | Example |
|---|---|---|
| P0 | Release cannot ship if broken; core flow, money, security, data loss | Login, payment, user A can see user B's data |
| P1 | Main functionality, high risk | Main CRUD, important validation, business state transitions |
| P2 | Secondary functionality, medium risk | Filter/sort, detailed error messages, rare boundaries |
| P3 | Presentation, convenience, low risk | Alignment, hint text, display order |

How to derive: Risk H×H → P0; H×M or M×H → P1; M×M or L×H → P2; otherwise P3. Risk data comes from `01-test-plan.md`; if the user adjusts it, follow the user.

## Execution Type hints (when the plan has not specified)

- `Auto (browser)`: stable main user flows needing repeated regression.
- `Auto (API)`: validation/business/permission at API level, many data combinations.
- `Manual`: UX, visuals, unstable features, exploratory, cases expensive to automate (CAPTCHA, real email, hardware).

## RTM — Requirement Traceability Matrix

Map each requirement 1–1 to test cases:

| Req/UC ID | Requirement | Happy path (TC) | Negative (TC) | Permission (TC) | Coverage |
|---|---|---|---|---|---|
| REQ-01 | ... | TC-X-001 | TC-X-002, TC-X-003 | TC-X-004 | Full |
| REQ-02 | ... | TC-Y-001 | — | N/A (no permissions) | Missing Negative |

Rules:
- Coverage column: `Full` / `Missing <type>` / `None`. Every "N/A" needs a reason.
- At the end of the RTM print: total requirements, number `Full`, coverage % = Full / total. Compute only from the table you just built.
- Reverse direction: list "orphan" cases (not mapped to any requirement) so the user can keep or drop them.

## Output format

Default: a Markdown table in `qa-artifacts/02-test-matrix.md` (sections: counts overview, 10-column test case table, RTM, uncovered requirements/contradictions). If the user wants CSV (or TestRail/Excel/Sheets import):

- Write `qa-artifacts/02-test-matrix.csv`, UTF-8 **with BOM** so Excel reads accents correctly, `,` as delimiter.
- Header row with exactly the 10 columns above, one row per test case, no merged cells.
- A cell containing a comma, double quote or newline must be wrapped in `"..."`, with inner double quotes doubled `""`.
- Multiple steps in one cell: separate by a real newline inside the quoted cell, or ` | ` if the user wants a single line; ask if unclear.
- Ask whether extra TestRail columns (Section, Type, Estimate) are needed — do not add them on your own.
- After writing, re-read the file and verify every row has the same number of columns.

## Present & Hard Stop

1. Summary: total cases; distribution by Priority and Execution Type (counted from the real table); RTM coverage %; requirements missing which case types.
2. Contradictions/clarifications found during design, each with a suggested default.
3. **QA Advisor** block: why these case groups, which blind spots (permissions, network drop, double-click, boundary data) are covered or not, the default you will choose.
4. **HARD STOP:** wait for approval. Do not start execution (Phase 3) before approval.

## Worked example

See `references/worked-example.md` for a sample output format (fictional data; read only when needed; never copy the example's numbers into a real project).

## Completion checklist

- [ ] Read `references/test-design-techniques.md` and used fitting techniques
- [ ] All 10 columns; numbered Steps; concrete Test Data; verifiable Expected Result
- [ ] Each requirement has happy + negative (+ permission if relevant) or a reason for N/A
- [ ] RTM percentage computed from real data; orphan cases listed (if any)
- [ ] No invented error messages/limits; gaps marked `[Needs input: ...]`
- [ ] File saved and stopped awaiting approval
