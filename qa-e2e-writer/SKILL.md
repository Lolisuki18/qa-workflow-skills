---
name: qa-e2e-writer
description: Executes test cases from the approved test matrix — produces manual run scripts and exploratory charters for Manual cases, and writes and runs Playwright tests (Page Object Model, semantic locators, web-first assertions) for Auto (browser) cases, recording only real results in execution notes. Use when the user says 'run the tests', 'write Playwright tests', 'E2E test', 'browser automation', 'exploratory testing', 'manual test script', 'try to break the app', 'viết test Playwright', 'chạy test', 'kịch bản test tay', 'test thăm dò', 'phá app'. Do NOT use for designing the test plan or test case table (use qa-test-plan-writer or qa-test-matrix-writer), writing bug reports (use qa-defect-writer), summary reports (use qa-summary-reporter), or developer unit and integration tests.
---

# QA E2E Writer — Step 3: Test Execution & Automation

Turns approved test cases into scripts that actually run. Inside `qa-lifecycle` this is Phase 3/5 (label `[QA Phase 3/5: Execution]` on the first line).

## Rules

- **Language:** reply and write artifacts in the user's language (English or Vietnamese); keep IDs and column names in English and translate placeholders (`[Needs input: ...]` → `[Cần bổ sung: ...]` for Vietnamese).
- **Input:** `qa-artifacts/02-test-matrix.md` (or CSV), approved. Missing → suggest running `qa-test-matrix-writer`; if the user insists, ask for the list of cases to test.
- **Anti-hallucination:**
  - Never record Pass/Fail for a case that was not actually run. A Manual case the user has not run = `Not Run`.
  - Never invent environments, URLs, browser versions, accounts. Missing → `[Needs input: ...]` or ask.
  - When pasting automation results, paste the real command output; never summarize from memory. If you cannot run (no environment, app not up) → record `Blocked` with the real cause.
- **Inspect real code before choosing locators:** read the component/template/HTML or open the app to see the real DOM, labels, roles and existing `data-testid`. Never guess selectors. If stable hooks are missing → propose adding `data-testid` for the developers rather than writing brittle CSS/XPath.
- Agent-agnostic: use whatever command-running/file-reading capability the current environment has; assume no specific IDE.

## Process

1. **Classify cases** by `Execution Type`: `Manual`, `Auto (browser)`, `Auto (API)`. Report the count per group.
2. **Manual** → read `references/exploratory-charters.md`. Produce:
   - A quick manual run script grouped by module/flow to minimize context switching (each row: TC ID · steps · data · expected result · a cell for the user to mark Pass/Fail/Blocked).
   - Exploratory charters per feature: double-click, Back, reload mid-flow, network loss, heavy/wrong-format files...
   - Wait for the user's results; record only what they report.
3. **Auto (browser)** → read `references/playwright-standards.md`, then:
   1. Inspect the repo: is Playwright already present (`playwright.config.*`, `package.json`), test folder layout, baseURL, how to start the app. Not present → ask before installing anything or adding dependencies.
   2. Inspect the DOM/code of the relevant pages to choose locators.
   3. Write the Page Objects and specs; put the TC ID in each test title (`TC-LOGIN-001: ...`).
   4. Run the tests and capture real output. On failure, decide whether it is a test defect (locator, data, waiting) or a product defect; only product defects go to Phase 4. Fix test defects within a reasonable number of rounds; never "patch" a test to pass by loosening assertions.
4. **Auto (API)** → when `qa-api-tester` is installed, hand these cases to it (endpoint inventory, API checklist, own results section). Otherwise use the API test tooling already in the repo (Postman/Newman, pytest, supertest...). If the repo has none and Playwright is in use or acceptable, propose Playwright's `APIRequestContext` (see `references/playwright-standards.md`, section "API testing"); ask before adding dependencies. Same rules: real output, independent data, endpoints and payloads taken from the spec/code, never guessed.
5. **Prefer machine-readable results:** when the runner supports it, run with a JSON or JUnit reporter (for Playwright see "Machine-readable results" in `references/playwright-standards.md`) and build the results table by reading that file, so no result is lost or mistyped from terminal text. Keep the report file path in the notes. If the reporter output is unavailable, fall back to the verbatim terminal output and say so.
6. **Write `qa-artifacts/03-execution-notes.md`** containing: run info (build/commit and environment if known, otherwise `[Needs input]`), per-TC results table, commands, raw output, exploratory findings, Blocked cases.
7. **Present:** counts of Pass/Fail/Blocked/Not Run taken from the real table, suspected product defects, and the next question (move to Phase 4 to log defects?).

## Test defect vs product defect

| Sign | Likely cause |
|---|---|
| Locator not found but the UI looks right when checked by hand | Test defect (locator/waiting) |
| Passes alone, fails together | Test depends on data/order → fix the test |
| Actual differs from the matrix Expected Result and reproduces by hand | Product defect → Phase 4 |
| Matrix Expected Result contradicts spec/code | Test case defect → ask the user, update the matrix |
| Passes sometimes, fails sometimes for no clear reason | Flaky — investigate; never mark Pass on faith |

## QA Advisor block (end of response)

Briefly explain why P0 cases run first; which blind spots remain uncovered (permissions, network drop, double-click, boundary data); the default plan (e.g. "run P0→P1 first, P2/P3 if time allows").

## Worked example

See `references/worked-example.md` for a sample output format (fictional data; read only when needed; never copy the example's numbers into a real project).

## Completion checklist

- [ ] Every case in the matrix has a real status (or `Not Run`/`Blocked` with a reason)
- [ ] Locators based on the DOM/code you read; no brittle CSS/XPath, no `waitForTimeout`
- [ ] Tests are data-independent; titles contain the TC ID
- [ ] Test run output is real output
- [ ] `03-execution-notes.md` updated; product defects handed to Phase 4
