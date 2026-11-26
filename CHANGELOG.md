# Changelog

Format: newest first. Skills are prompts, so "breaking" means a change in behavior an agent will notice (labels, hard stops, script flags).

## Unreleased (next: 0.2.0)

### Added
- Skills: `qa-api-tester`, `qa-nonfunctional-writer`, `qa-regression-planner`, each with a reference file and a worked example; `qa-accessibility-auditor` (WCAG 2.2 AA checklist; one smoke run, see `evals/README.md`). New artifacts: `02b-nonfunctional.md`, `04b-regression-plan.md`.
- Trigger prompts for the three new skills; behaviour smoke runs recorded in `evals/README.md`.
- Optional hook `scripts/qa-gate.py` that enforces the Phase 1 and 2 hard stops from the artifact status (14 tests, see `docs/hard-stop-enforcement.md`).
- `scripts/validate.py` (names, descriptions, line counts, fences, references) and a GitHub Actions workflow.
- `scripts/install.py`: links or copies the skills into an agent's skills folder (junctions on Windows, symlinks elsewhere; never overwrites); `--only` / `--exclude` to choose skills.
- `scripts/readme-index.py`: generates the skill index in `README.md` from each `SKILL.md`; CI fails when it is out of date.
- CI also compares the shared scripts with the canonical copies in `ai-workflow-suite`.
- `.claude-plugin/plugin.json` so the repo installs as a Claude Code plugin (not yet checked with `claude plugin validate`).
- `LICENSE` (MIT).

### Changed (friction fixes from a real CLI run)
- CLI / non-UI targets: audit group "Output & console" in `qa-test-plan-writer`; `Auto (API)` doubles as "automated non-UI run" for CLIs; `qa-lifecycle` routes to `qa-api-tester` only when HTTP endpoints exist; "Not applicable" exits in `qa-api-tester` and `qa-accessibility-auditor`; CLI sections in `qa-e2e-writer`, `qa-nonfunctional-writer` and its catalog; seconds-long local runs exempt from the heavy-run hard stop.
- Expected-result provenance: new matrix column `Oracle` (spec / approved default / code behavior / none), used by `qa-defect-writer` ("expected result disputed"); new status `Informational`, excluded from the pass rate by `qa-summary-reporter`.
- Hard stops: `02b-nonfunctional.md` is a second approval inside Phase 2; no execution before the matrix is Approved; one manual-case rule (record only what you ran with evidence); the P0 definition overrides the risk derivation upward.
- QA cannot close defects: `Re-test (awaiting user close)` is listed separately and the user is asked to close verified defects before the final report; `Go (N/A, reason)` in release gates; stricter of plan and default gate when unconfirmed.
- `qa-regression-planner`: works without a defect record, short form for single-file diffs, whole-layer confirmation when the harness cannot run a subset.
- `qa-lifecycle`: "Small scope" section; record the environment actually used. `qa-e2e-writer`: say when pasted evidence is truncated.
- `scripts/qa-gate.py`: `03-*` also needs `02b-*` Approved when it exists; conservative Bash check; `docs/hard-stop-enforcement.md` states the limits (Write/Edit matcher, who set Approved, tests not blocked). Now 14 tests.

### Changed
- Skill descriptions are English only and shorter (4 trigger phrases, at most 650 characters) to cut the context every installed skill costs. The trigger evals keep their Vietnamese prompts to check that matching still works.
- `qa-lifecycle` routes API, non-functional and regression work to the new skills; `qa-e2e-writer` hands `Auto (API)` cases to `qa-api-tester` when installed.
- Every skill states that content found in repos, logs and pages is data, not instructions.
- `scripts/run-evals.py` no longer crashes on Windows consoles when printing Vietnamese prompts.

## 0.1.0

Six skills: `qa-lifecycle`, `qa-test-plan-writer`, `qa-test-matrix-writer`, `qa-e2e-writer`, `qa-defect-writer`, `qa-summary-reporter`, with worked examples, evals and `scripts/run-evals.py`.
