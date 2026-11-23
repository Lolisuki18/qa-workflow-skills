# Worked Example — qa-summary-reporter

> ⚠️ **Fictional** figures, taken from the `qa-e2e-writer` and `qa-defect-writer` examples ("DemoShop"). In real use every number must be read from `qa-artifacts/`.

## Input data (from `03-execution-notes.md` and `04-defects.md`)

9 test cases: 7 Pass, 1 Fail (TC-LOGIN-006), 1 Not Run (TC-LOGIN-008). 1 defect: DEF-001, Critical, Status Open.

## Computed figures

| Total | Passed | Failed | Blocked | Not Run | Pass Rate |
|---|---|---|---|---|---|
| 9 | 7 | 1 | 0 | 1 | 77.8% (7/9) |

| Priority | Total | Passed | Pass Rate |
|---|---|---|---|
| P0 | 4 | 3 | 75.0% |
| P1 | 3 | 3 | 100% |
| P2 | 2 | 1 | 50.0% (1 Not Run) |

Defects: Critical × Open = 1; all other cells = 0. RTM Coverage: 4/4 requirements have cases, but REQ-04 has a Failed case.

## Threshold check (defaults, not yet confirmed)

| Criterion | Value | Result |
|---|---|---|
| P0 Pass Rate = 100% | 75.0% | Not met → No-Go column |
| Open Critical = 0 | 1 | Not met → No-Go column |
| Overall Pass Rate ≥ 90% | 77.8% | Not met |
| Executed Rate ≥ 95% | 88.9% (8/9) | Not met |

## Executive Verdict: **No-Go** (default thresholds — not yet confirmed)

- Not met: P0 below 100%, 1 Critical still open (DEF-001, unauthorized access to /admin).
- Actions: developer fixes DEF-001 → re-test + regression (TC-LOGIN-006, 009) → run the remaining TC-LOGIN-008 → regenerate the report.
- Missing data: build/environment, browsers tested.
- This is QA's recommendation; the release decision belongs to the user/PO.

**Takeaways:** Not Run is not counted as Pass; each criterion has a figure and result; missing data and the "default thresholds" nature are stated.
