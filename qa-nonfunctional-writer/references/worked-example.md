# Worked Example — qa-nonfunctional-writer

> ⚠️ **Fictional** data ("DemoShop") to illustrate the format. Thresholds in a real project come from the requirements, an SLA or the user; numbers below are placeholders. Never copy them into a real project.

## 1. Attribute selection (from `01-test-plan.md`)

```markdown
Selected: Performance (NF-PERF), Accessibility (NF-A11Y), Compatibility (NF-COMP).
Out of scope this round: Security basics (covered by the code review), Usability (no usability requirement).
Open: the plan says "should load fast" with no number → `[Needs input: p95 target]`. Supported browsers not stated → `[Needs input: browser matrix]`.
```

## 2. `02b-nonfunctional.md` (draft, waiting for approval)

```markdown
# Non-functional Checks — DemoShop
- **Phase:** 2/5 — Test Matrix (non-functional design)
- **Date:** 2026-11-26
- **Version:** v0.1
- **Status:** Draft

| NF ID | Attribute | Scenario | Metric & threshold | Tool | Environment | Priority | Linked requirement |
|---|---|---|---|---|---|---|---|
| NF-PERF-01 | Performance | Product list, 20 concurrent users, 5 min | p95 < [Needs input: SLA] ms, errors < 1% (suggested, not approved) | k6 | staging-test | P1 | REQ-07 |
| NF-PERF-02 | Performance | Product list, 5,000 products, filter + sort | p95 < [Needs input] ms | k6 | staging-test | P2 | REQ-07 |
| NF-A11Y-01 | Accessibility | Checkout form by keyboard only | All fields and the pay button reachable, focus visible | manual | staging-test | P1 | REQ-11 |
| NF-A11Y-02 | Accessibility | Automated scan of /cart | 0 critical issues (WCAG 2.1 AA, level confirmed by user) | axe | staging-test | P2 | REQ-11 |
| NF-COMP-01 | Compatibility | Login and checkout on [Needs input: browser matrix] | Flows complete, layout usable at 375 px | Playwright projects | staging-test | P1 | REQ-01 |

Safe-run rules: only `staging-test`; never production; start at 5 users and double.
```

HARD STOP: the user approves the table and gives the open thresholds before anything heavy runs.

## 3. Results recorded in `03-execution-notes.md` (fictional numbers)

```markdown
### Non-functional track
Tool: k6 [Needs input: version] · Command: `k6 run list-load.js` · Raw output: pasted below

| NF ID | Result | Measured | Threshold | Notes |
|---|---|---|---|---|
| NF-PERF-01 | **Fail** | p95 1,240 ms, errors 0.2% | p95 < 800 ms (approved by user) | → DEF-006 with the k6 summary as evidence |
| NF-A11Y-01 | Pass | all controls reachable | — | tested by the user |
| NF-COMP-01 | Not Run | — | — | browser matrix still open |
```
