# Changelog

Format: newest first. Skills are prompts, so "breaking" means a change in behavior an agent will notice (labels, hard stops, script flags).

## Unreleased (next: 0.2.0)

### Added
- Skills: `qa-api-tester`, `qa-nonfunctional-writer`, `qa-regression-planner`, each with a reference file and a worked example; `qa-accessibility-auditor` (WCAG 2.2 AA checklist, not yet run on an agent). New artifacts: `02b-nonfunctional.md`, `04b-regression-plan.md`.
- Trigger prompts for the three new skills; behaviour smoke runs recorded in `evals/README.md`.
- Optional hook `scripts/qa-gate.py` that enforces the Phase 1 and 2 hard stops from the artifact status (10 tests, see `docs/hard-stop-enforcement.md`).
- `scripts/validate.py` (names, descriptions, line counts, fences, references) and a GitHub Actions workflow.
- `scripts/install.py`: links or copies the skills into an agent's skills folder (junctions on Windows, symlinks elsewhere; never overwrites); `--only` / `--exclude` to choose skills.
- `scripts/readme-index.py`: generates the skill index in `README.md` from each `SKILL.md`; CI fails when it is out of date.
- CI also compares the shared scripts with the canonical copies in `ai-workflow-suite`.
- `.claude-plugin/plugin.json` so the repo installs as a Claude Code plugin (not yet checked with `claude plugin validate`).
- `LICENSE` (MIT).

### Changed
- `qa-lifecycle` routes API, non-functional and regression work to the new skills; `qa-e2e-writer` hands `Auto (API)` cases to `qa-api-tester` when installed.
- Every skill states that content found in repos, logs and pages is data, not instructions.
- `scripts/run-evals.py` no longer crashes on Windows consoles when printing Vietnamese prompts.

## 0.1.0

Six skills: `qa-lifecycle`, `qa-test-plan-writer`, `qa-test-matrix-writer`, `qa-e2e-writer`, `qa-defect-writer`, `qa-summary-reporter`, with worked examples, evals and `scripts/run-evals.py`.
