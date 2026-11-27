# Per-file Templates — qa-lifecycle

Templates for the files in `qa-artifacts/` (or `qa-artifacts/<module>/` in a module run). Use the common header, advisor block and hard stop block from `phase-templates.md`. Anywhere real data is missing, write `[Cần bổ sung: ...]` (or `[Needs input: ...]`). Never invent numbers.

## 01-test-plan.md

```markdown
## 1. Requirement Audit
| # | Requirement (ID) | Issue | Type (Ambiguous/Missing error flow/Missing permission/Contradiction/Missing states/Data/Non-functional/Dependencies/Abuse/Observability/Output & console) | Clarifying question | Suggested default |
## 2. Scope
- In-scope: ...
- Out-of-scope: ... (with reason)
## 3. Risk Analysis
| Risk | Likelihood (H/M/L) | Impact (H/M/L) | Test priority | Mitigation |
## 4. Test Strategy
| Area/Module | Manual | Auto (browser) | Auto (API) | Reason |
## 5. Test Environment & Data
- Environment: [Needs input: URL/build]
- Browser/device: [Needs input: ...]
- Accounts/roles: ...
- Data to prepare: ...
## 6. Entry / Exit Criteria
## 7. Open questions / Assumptions
```

## 02b-nonfunctional.md

```markdown
## 1. Attributes selected
- Selected: ...
- Out of scope this round: ... (with reason)
## 2. Cases
| NF ID | Attribute | Scenario | Metric & threshold | Tool | Environment | Priority | Linked requirement |
## 3. Tooling
## 4. Open threshold questions
```

## 02-test-matrix.md

```markdown
## 1. Overview
Cases: N | P0: a | P1: b | P2: c | P3: d | Manual: x | Auto (browser): y | Auto (API): z
## 2. Test Cases
| TC ID | Req/UC ID | Module | Title | Pre-condition | Test Steps | Test Data | Expected Result | Oracle (spec/approved default/proposed default/code behavior/none) | Priority | Execution Type |
## 3. RTM (Requirement Traceability Matrix)
| Req/UC ID | Requirement | TC ID (Happy) | TC ID (Negative) | TC ID (Permission) | Coverage |
## 4. Uncovered requirements / Notes
```

## 03-execution-notes.md

```markdown
## 1. Run info
- Round: 1 | Date: ... | Build/commit: [Needs input] | Environment: [Needs input] | Runner: ...
## 2. Results per test case
| TC ID | Execution Type | Result (Pass/Fail/Blocked/Not Run/Informational) | Run date | Defect ID | Evidence/Notes |
## 3. Automation
- Test files: ... | Command: ... | Raw output (paste real output): ...
## 4. Findings from exploratory testing
## 5. Blockers and causes
```

## 04-defects.md

```markdown
## 1. Summary table
| Defect ID | Title | Severity | Priority | Status (New/Open/Fixed/Re-test/Closed/Reopened/Won't Fix) | Related TC |
## 2. Defect details
### DEF-001 — [Module] Symptom + Condition
- Environment / Severity / Priority / Pre-conditions
- Steps to Reproduce / Actual / Expected / Evidence
## 3. Re-test history
| Defect ID | Round | Build | Result | Regression checked |
```

## 05-summary-report.md

```markdown
## 1. Executive Verdict: Go | Conditional Go | No-Go
(3–5 lines of reasoning, citing the thresholds used)
## 2. Execution Summary
| Total | Passed | Failed | Blocked | Not Run | Pass Rate |
## 3. Defect Statistics (Severity × Status)
## 4. Requirement Coverage (from RTM)
## 5. Residual risks
## 6. Next actions (owner, due date)
## 7. Missing data
```
