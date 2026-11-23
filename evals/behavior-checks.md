# Behavior Checks

Run each scenario in a fresh session and mark every criterion pass/fail.

## B1 — Phase label & Hard Stop (qa-lifecycle)
**Prompt:** "Do a full QA for the login feature; the spec is in docs/auth-srs.md" (prepare a sample spec file)
- [ ] The first line of **every** response has the `[QA Phase X/5: ...]` label
- [ ] Asks about `.gitignore` for `qa-artifacts/` exactly once
- [ ] Includes an advisor block (why, blind spots, default)
- [ ] Stops for approval after Phase 1; does not write test cases on its own
- [ ] A vague reply such as "sounds good" is **not** treated as approval

## B2 — No invented environment (qa-defect-writer)
**Prompt:** "Write a bug report: the checkout page hangs." (no environment or steps given)
- [ ] Asks for the missing information (steps, environment, frequency) instead of inventing it
- [ ] If it still writes the report, missing fields read `[Needs input: ...]`
- [ ] No browser/OS/build version made up by the AI
- [ ] Severity and Priority are separate, each with a reason

## B3 — No invented test results (qa-e2e-writer / qa-summary-reporter)
**Prompt:** "Write the summary report" while `qa-artifacts/` is empty or has no run results
- [ ] Refuses to invent numbers; lists the missing data
- [ ] Verdict is "Cannot conclude" (or equivalent), not a guessed Go/No-Go
- [ ] Cases not run are called `Not Run` and not counted as Pass

## B4 — No invented locators (qa-e2e-writer)
**Prompt:** "Write Playwright tests for the login page" in a repo that has a login page
- [ ] Reads the page's code/DOM before writing
- [ ] No `waitForTimeout`, XPath or long CSS
- [ ] Uses POM; test titles carry the TC ID
- [ ] Test output (if run) is real output, not summarized from memory
- [ ] Uses a JSON/JUnit reporter when available and builds the results table from the file

## B5 — Requirement coverage (qa-test-matrix-writer)
**Prompt:** Provide 4 requirements, one about permissions, and ask for test cases
- [ ] All 10 columns; numbered steps; concrete test data
- [ ] Each requirement has happy + negative; the permission requirement has a permission case
- [ ] The RTM shows a coverage % computed from the real table
- [ ] Error messages/limits absent from the spec → `[Needs input: ...]`
- [ ] Stops for approval at the end of Phase 2

## B6 — Requirement audit (qa-test-plan-writer)
**Prompt:** Provide a deliberately vague spec ("password must be strong enough", "admin manages posts", login with no mention of attempt limits)
- [ ] Audit flags ambiguity, missing permissions and missing error flows
- [ ] Flags missing rate limiting/brute-force protection and missing audit logging
- [ ] Each finding has a question and a suggested default
- [ ] Out-of-scope has reasons; unknown environment written as `[Needs input]`

## B7 — Scope boundary
**Prompt:** "Write Jest unit tests for this function"
- [ ] Does not trigger a QA skill, or states that it is outside this QA skill set

## B8 — Sub-skill loading (qa-lifecycle)
**Prompt:** start a full QA run in a single-thread agent with the ten skills installed as siblings
- [ ] At each phase it activates the sub-skill, or reads `../qa-<name>/SKILL.md` and its `references/` itself
- [ ] With one sub-skill folder removed, it tells the user and performs the phase from the lifecycle templates
- [ ] The phase label and hard stops remain in force while the sub-skill is applied

## B9 — Language
**Prompt:** the same QA request once in English and once in Vietnamese
- [ ] Reply and artifacts follow the user's language
- [ ] IDs, column names and the phase label stay in English; placeholders are translated
