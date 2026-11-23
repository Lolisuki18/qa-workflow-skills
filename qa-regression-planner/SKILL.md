---
name: qa-regression-planner
description: Selects the regression suite for a new build or fix from the RTM, the change set and defect history — maps changed files and modules to impacted requirements and test cases, ranks them by risk and priority, splits them into smoke, targeted and full regression with time estimates, and records the plan in qa-artifacts/. Use when the user says 'regression plan', 'which tests should I re-run', 'what to retest after this change', 'smoke test list', 'impact analysis for testing', 'regression suite for this release', 'chọn test hồi quy', 'kiểm thử hồi quy', 'sau khi sửa lỗi cần test lại những gì', 'phân tích ảnh hưởng thay đổi', 'danh sách smoke test'. Do NOT use for writing the initial test plan (use qa-test-plan-writer), designing new test cases (use qa-test-matrix-writer), logging one defect or its single re-test checklist (use qa-defect-writer), or running the tests (use qa-e2e-writer).
---

# QA Regression Planner — Step 4b: Regression Selection

Chooses what to re-test, from evidence, so a small fix does not trigger a full retest and a risky change does not get only a smoke run. Inside `qa-lifecycle` this belongs to Phase 4/5 whenever a new build arrives (label `[QA Phase 4/5: Regression]` on the first line).

## Rules

- **Language:** reply and write artifacts in the user's language (English or Vietnamese); keep IDs and column names in English and translate placeholders (`[Needs input: ...]` → `[Cần bổ sung: ...]` for Vietnamese).
- **Input:** `qa-artifacts/02-test-matrix.md` with its RTM, `04-defects.md`, and the change set (`git diff`, commit list, release notes or a list from the developer). No matrix → suggest `qa-test-matrix-writer`; without an RTM, say the mapping will be weaker and mark it `[Inferred from code — needs confirmation]`.
- **Anti-hallucination:** never claim a module is "not affected" without evidence from the diff, imports or the RTM. Unknown dependency → treat as possibly affected and say why. Never invent run times; estimate only from past real runs (execution notes), otherwise `[Needs input]`.
- Never decide that a P0 case can be skipped. Skipping is the user's decision, recorded as `Skipped by user`.

## Process

1. **Get the change set.** Build or release identifier, base to target (`git diff --stat <old>..<new>`), list of fixed defects (IDs from `04-defects.md`), and any known risky areas. Ask for what you cannot find.
2. **Map change → requirement.** For each changed file or module, find the requirements and test cases it serves, through the RTM, test titles, route or component names, and code references. Add the direct neighbours: callers, shared utilities, shared tables and APIs. Cite `file:line` or the RTM row.
3. **Score risk.** Per case: priority (P0-P3), whether the area changed directly or indirectly, defect history (a module with past defects scores higher), recent flakiness, and business impact. Keep the scoring visible as three levels (High / Medium / Low) with a one-line reason, not a hidden number.
4. **Build the three layers** (`references/regression-selection.md`):
   - **Smoke:** the shortest set proving the build is testable: all P0 happy paths of the main flows.
   - **Targeted:** every case for changed or defect-fixed areas, plus their direct neighbours.
   - **Full:** everything, recommended only for large changes, release candidates or when the targeted run fails.
5. **Estimate effort** from execution notes where real timings exist, split Manual vs Auto, and list what can run unattended.
6. **Write `qa-artifacts/04b-regression-plan.md`:** header (build, date, version, status), change summary, impact table (`Changed area · Impacted requirements · Cases · Why`), the layered case lists, excluded cases with reasons, effort, and entry/exit conditions (for example "stop and report if any smoke case fails").
7. **Present** the recommendation with a default: "I suggest smoke first, then targeted; full run if smoke or targeted shows a failure". Wait for the user to confirm before handing cases to `qa-e2e-writer`.

## QA Advisor block (end of response)

Explain why these layers fit this change, which blind spots remain (shared code, config and data changes that no case maps to), and the default order of execution.

## Completion checklist

- [ ] Each selected case traces to a changed area, a fixed defect or a P0 rule
- [ ] Each excluded case has a stated reason; no P0 excluded silently
- [ ] No estimate or "not affected" claim without evidence
- [ ] `04b-regression-plan.md` saved; user confirmed the layer to run
