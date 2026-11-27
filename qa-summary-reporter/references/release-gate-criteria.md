# Release Gate Criteria

Quantitative thresholds to choose **Go / Conditional Go / No-Go**. These are **proposed default thresholds**. If the Test Plan (`01-test-plan.md` Exit Criteria) or the user has fixed other thresholds, use those and cite the source. When applying defaults, say plainly "default thresholds, not yet confirmed".

## Metric definitions

| Metric | Formula |
|---|---|
| Pass Rate | Passed / Total |
| Executed Rate | (Passed + Failed) / Total |
| P0 Pass Rate | P0 Passed / P0 Total |
| RTM Coverage | In-scope requirements with full coverage / total in-scope requirements |
| Open Defect | Status ∈ {New, Open, Fixed (not yet re-tested), Re-test, Reopened}. QA cannot close defects: list `Re-test` ones separately as "Re-test (awaiting user close)" |

`Conditional Go (provisional)` means the only open items are `Not Run` cases that need a person or device. Defects in `Re-test` status are listed as "awaiting user close": once the re-test passed they do not count as open Blocker/Critical, but the verdict says "pending user close" until the user closes them.

`Not Run` and `Blocked` are **not** counted as Passed. `Informational` cases (including `Oracle: none` exploratory checks) are excluded from every rate and listed separately. Failures against an `approved default` (when no formal SRS exists) **do** count toward Pass Rate and open defects unless the user explicitly reclassifies them as `Informational`.

`Not Run` cases that need a person or device (real terminal, phone, screen reader) are listed as "Not run: needs person". They do not by themselves force No-Go through the Executed Rate; they cap the verdict at Conditional Go until run, unless the user's thresholds say otherwise.

A criterion with no applicable cases (for example no permission cases because the target has no roles) is reported as `Go (N/A, <reason>)`, not silently dropped.

If the plan's exit criteria and these defaults differ: values the user confirmed win; otherwise the stricter applies.

## Default thresholds

| Criterion | Go | Conditional Go | No-Go |
|---|---|---|---|
| P0 Pass Rate | 100% | 100% (mandatory) | < 100% |
| P1 Pass Rate | ≥ 95% | ≥ 90% | < 90% |
| Overall Pass Rate | ≥ 95% | ≥ 90% | < 90% |
| Executed Rate | 100% | ≥ 95% (rest has a reason and a plan) | < 95% |
| Blocked cases | 0 | ≤ 5%, none P0 | > 5% or any P0 Blocked |
| Open Blocker | 0 | 0 | ≥ 1 |
| Open Critical | 0 | 0 (or a mitigation accepted in writing by the user/PO) | ≥ 1 without mitigation |
| Open Major | 0 | ≤ 3, each with a recorded workaround and fix plan | > 3 or any Major without workaround |
| Open Minor/Trivial | Any, logged in backlog | Any, logged in backlog | — |
| RTM Coverage | 100% | ≥ 95%, missing requirements all P2/P3 | < 95% or missing P0/P1 requirements |
| Defects Fixed but not Re-tested | 0 | Allowed only for Minor/Trivial | Present at Major or above |
| Permissions/security | All cases run and Pass | Same as Go | Any failing or unrun case |

**Small-N rule (< ~10 cases in a priority class):** one failed case moves that class's rate by more than 10 points (1 of 7 = 85.7%), so the percentage alone is not a fair gate. For such a class, judge by the severity of the failing cases' defects instead of the rate: no open Blocker/Critical/Major and every failing case has a Minor/Trivial defect → **Conditional Go**, with the defects listed as conditions. Otherwise apply the normal cells. State the rule and the numbers in the report (for example "P1: 6/7 = 85.7%, small-N rule applied, 1 Minor defect DEF-002"). Classes with ≥ 10 cases keep the strict percentage gates. P0 stays 100% regardless of N.

> **Any No-Go cell true → No-Go.** If no No-Go cell is true but not every Go cell is met → **Conditional Go**. Only when **all** Go cells are met → **Go**.

## How to choose the verdict (algorithm)

1. Check the **No-Go** column for every criterion that has data. Any true → **No-Go**; list them all (and still list any missing data).
2. Otherwise, is there data to compute every mandatory criterion? No → `Cannot conclude`, list the missing data. (Never guess.)
3. Otherwise, all Go cells met → **Go**.
4. Otherwise → **Conditional Go**, with concrete conditions.

## Conditions for Conditional Go

Each condition must be:
- Specific and verifiable (e.g. "Re-test DEF-007 and regression of the Payment group both Pass on the next build").
- Given an owner and due date (unknown → `[Needs input: owner and due date]`).
- Stated with its consequence if unmet (becomes No-Go).

Typical condition types: fix and re-test specific Major defects; run the remaining Not Run group; written acceptance of residual risk; post-release monitoring; a rollback plan.

## Context adjustments (only with the user's agreement)

| Context | Suggested adjustment |
|---|---|
| Money/medical/high-security systems | Tighten: open Major = 0 for Go and Conditional Go; Pass Rate ≥ 98% |
| MVP/internal demo/student project | Relax: accept open Major with workaround, Pass Rate ≥ 85%; still keep P0 = 100% and Blocker/Critical = 0 |
| Hotfix | Focus: re-test of the fix + regression of the affected area at 100%; the rest per the agreed plan |
| Feature behind a feature flag | May relax conditions for that feature; state how to switch it off |

Record every adjustment in the report under "Applied thresholds" (default or adjusted, who decided).

## Sample verdict paragraph

```markdown
**Executive Verdict: Conditional Go** (default thresholds — not yet confirmed)
- Met: P0 Pass Rate 100% (a/a), open Blocker 0, open Critical 0.
- Not meeting Go column: overall Pass Rate x% (< 95%), open Major n (> 0).
- Conditions: (1) ... owner/due date ..., (2) ...
- If conditions are not met by ...: becomes No-Go.
This is QA's recommendation; the release decision belongs to the user/PO.
```

(Illustrative format only — a, x, n must come from real data.)

## Minimum data needed to report

- [ ] Results table per TC (with Priority)
- [ ] Defect list with Severity, Status
- [ ] RTM or the list of in-scope requirements
- [ ] Build/version and environment tested (missing → `[Needs input]`; the report can still be written but state the limit)
- [ ] Agreed Exit thresholds (missing → use defaults and say so)
