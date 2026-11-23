---
name: qa-defect-writer
description: Turns raw bug descriptions, logs and screenshots into standardized Defect Reports (title, environment, severity vs priority, pre-conditions, steps to reproduce, actual vs expected, evidence), logs them in qa-artifacts/04-defects.md, and runs Re-test and Regression Checklist mode when developers report a fix. Use when the user says 'write a bug report', 'log this defect', 'report this bug', 'severity or priority?', 're-test the fix', 'regression checklist', 'viết bug report', 'ghi nhận lỗi', 'báo lỗi chuẩn', 'tạo defect', 'kiểm tra lại sau khi dev sửa'. Do NOT use for finding the root cause or fixing the code, designing test cases (use qa-test-matrix-writer), running tests (use qa-e2e-writer), summary reports (use qa-summary-reporter), or code review.
---

# QA Defect Writer — Step 4: Defect Management

Standardizes bugs into reports a developer can reproduce immediately, and tracks the lifecycle until closure. Inside `qa-lifecycle` this is Phase 4/5 (label `[QA Phase 4/5: Defects]` on the first line).

## Rules

- **Read first:** `references/severity-priority-matrix.md` to rate Severity and Priority.
- **Strict anti-hallucination:** record only what the user/logs/real test results show.
  - Never invent environment, browser/OS/build versions, reproduction steps, frequency, error messages.
  - Missing → `[Needs input: ...]` and ask (batch into one short list of questions, not piecemeal).
  - Never state a root cause as certain. A hypothesis goes in "Notes/Hypothesis (unconfirmed)". Finding and fixing the cause is the developer's job.
- **One defect, one problem.** Several symptoms of one cause → link them in notes; split when two phenomena are independent.
- Duplicate check: compare with the existing `04-defects.md` before creating; suspected duplicate → ask.
- Neutral tone: describe events, never blame.

## Mode 1 — Create a Defect Report

### Process
1. **Collect:** raw description, logs, screenshots/video, related TC (`Defect ID` ↔ `TC ID`), environment information.
2. **Normalize reproduction steps:** numbered, one action per step, with concrete data. Someone unfamiliar with the system should be able to follow. If the raw description lacks steps → ask, never fill the gap yourself.
3. **Separate Actual vs Expected:** Expected comes from the spec / the TC's Expected Result (cite the source); no source → `[Needs input: Expected source]`.
4. **Rate Severity** (technical impact) and **Priority** (business urgency) **separately** per the matrix, with a one-line reason. Priority is a proposal — the user/PO decides.
5. **Evidence:** list real files/log paths/screenshots; quote the relevant log lines verbatim. None → "None yet".
6. **Write into `qa-artifacts/04-defects.md`** (top: summary table `Defect ID | Title | Severity | Priority | Status | Related TC`; then detail sections per the template below; bottom: "Re-test history" table `Defect ID | Round | Build | Result | Regression checked`). Continue the Defect ID numbering (`DEF-001`, `DEF-002`...), never renumber.

### Defect Report template

```markdown
### DEF-001 — [Module] Symptom + Condition
| Field | Content |
|---|---|
| Title | [Checkout] Total does not update when quantity changes after applying a coupon |
| Related TC | TC-CART-012 |
| Environment | [Needs input: URL/build, OS, browser + version, role] |
| Severity / Priority | Major / P1 — <one-line reason> |
| Status | New |
| Reproducibility | [x/y attempts] or [Needs input] |
| Pre-conditions | ... |
| Steps to Reproduce | 1. ... 2. ... 3. ... |
| Actual Result | ... |
| Expected Result | ... (source: REQ-xx / TC-xx) |
| Evidence | log: ..., screenshot: ... |
| Notes / Hypothesis (unconfirmed) | ... |
```

**Title:** `[Module] Symptom + Condition` — state what is wrong and when. Good: `[Login] Shows "System error" when the email contains uppercase letters`. Avoid: `Login broken`, `Doesn't work`.

## Mode 2 — Re-test & Regression Checklist

Triggered when a developer reports a fix (or the user says "DEF-xxx is fixed").

1. Read the original defect in `04-defects.md`. Ask for the build/commit containing the fix if unknown (`[Needs input]`).
2. Produce a checklist in 3 groups:
   - **Re-test the original bug:** run the exact original Steps to Reproduce in the same environment/data; expected = the original Expected Result. Also try close variants (other boundary data, other roles) when relevant.
   - **Related regression:** flows sharing the module/function/API/data with the changed area. Use the RTM (`02-test-matrix.md`) to pick TCs sharing the Req/Module, prioritizing P0/P1; if a diff/commit is known, read the change to infer the affected area and state the basis for the inference.
   - **Previously failed:** older Closed defects in the same module — verify no recurrence.
3. State which cases run `Manual` and which re-run in Playwright (`qa-e2e-writer`).
4. After the user reports results: update Status per the lifecycle and add a row to "Re-test history" (round, build, result, regression checked). Never close a defect without real results.

### Status lifecycle
`New → Open (confirmed) → Fixed (dev reports) → Re-test → Closed` · branches: `Reopened` (re-test fails), `Won't Fix` / `Duplicate` / `Cannot Reproduce` (need a reason and the decision maker). Never skip steps; never move to `Closed` yourself.

## QA Advisor block

Explain why Severity and Priority are separate; warn about defects easily underrated (permissions, data loss, bugs that only appear on double-click/network drop); state the default (e.g. "I rated Major/P1; raise it if the bug blocks a demo").

## Worked example

See `references/worked-example.md` for a sample output format (fictional data; read only when needed; never copy the example's numbers into a real project).

## Completion checklist

- [ ] Title follows `[Module] Symptom + Condition`
- [ ] Numbered Steps, reproducible; Actual ≠ Expected clearly
- [ ] Severity and Priority separate, with reasons
- [ ] No invented environment/steps/frequency; gaps marked `[Needs input: ...]`
- [ ] Evidence is real material or "None yet"
- [ ] Written into `04-defects.md`, duplicates checked
- [ ] Re-test: 3 checklist groups present and history updated from real results
