# Changelog

Format: newest first. Skills are prompts, so "breaking" means a change in behavior an agent will notice (labels, hard stops, script flags).

## Unreleased (next: 0.2.0)

### Added
- Consistency fixes: `qa-regression-planner` honours the caller's folder; re-test rounds list `02b`/`03c` too; release-gate criteria define "provisional" and `Re-test` defects like the suite.
- Docs and evals aligned with module folders: phase-templates paths are relative to the module folder; new behavior check for `Round N` appends and module runs; README says four optional skills.
- Skills: `qa-api-tester`, `qa-nonfunctional-writer`, `qa-regression-planner`, each with a reference file and a worked example; `qa-accessibility-auditor` (WCAG 2.2 AA checklist; one smoke run, see `evals/README.md`). New artifacts: `02b-nonfunctional.md`, `04b-regression-plan.md`.
- Trigger prompts for the three new skills; behaviour smoke runs recorded in `evals/README.md`.
- Optional hook `scripts/qa-gate.py` that enforces the Phase 1 and 2 hard stops from the artifact status (with unit tests, see `docs/hard-stop-enforcement.md`).
- `scripts/validate.py` (names, descriptions, line counts, fences, references) and a GitHub Actions workflow.
- `scripts/install.py`: links or copies the skills into an agent's skills folder (junctions on Windows, symlinks elsewhere; never overwrites); `--only` / `--exclude` to choose skills.
- `scripts/readme-index.py`: generates the skill index in `README.md` from each `SKILL.md`; CI fails when it is out of date.
- CI also compares the shared scripts with the canonical copies in `ai-workflow-suite`.
- `.claude-plugin/plugin.json` so the repo installs as a Claude Code plugin (not yet checked with `claude plugin validate`).
- `LICENSE` (MIT).

### Changed (friction fixes from a real CLI run)
- CLI / non-UI targets: audit group "Output & console" in `qa-test-plan-writer`; `Auto (API)` doubles as "automated non-UI run" for CLIs; `qa-lifecycle` routes to `qa-api-tester` only when HTTP endpoints exist; "Not applicable" exits in `qa-api-tester` and `qa-accessibility-auditor`; CLI sections in `qa-e2e-writer`, `qa-nonfunctional-writer` and its catalog; the exemption for seconds-long non-functional runs was removed (default: skip `02b` and record such cases in the matrix when every case is a local run under ~10 s).
- Expected-result provenance: new matrix column `Oracle` (spec / approved default / proposed default / code behavior / none), used by `qa-defect-writer` ("expected result disputed"); new status `Informational`, excluded from the pass rate by `qa-summary-reporter`.
- Hard stops: `02b-nonfunctional.md` is a second approval inside Phase 2; no execution before the matrix is Approved; one manual-case rule (record only what you ran with evidence); the P0 definition overrides the risk derivation upward.
- QA cannot close defects: `Re-test (awaiting user close)` is listed separately and the user is asked to close verified defects before the final report; `Go (N/A, reason)` in release gates; stricter of plan and default gate when unconfirmed.
- `qa-regression-planner`: works without a defect record, short form for single-file diffs, whole-layer confirmation when the harness cannot run a subset.
- `qa-lifecycle`: "Small scope" section; record the environment actually used. `qa-e2e-writer`: say when pasted evidence is truncated.
- `scripts/qa-gate.py`: `03-*` also needs `02b-*` Approved when it exists; conservative Bash check; `docs/hard-stop-enforcement.md` states the limits (Write/Edit matcher, who set Approved, tests not blocked).

### Changed (review and a real browser-app QA run)
- Module folders: every sub-skill writes to the folder the caller names (`qa-artifacts/<module>/`, same file names, tools under `<module>/tools/`; default `qa-artifacts/`). `qa-lifecycle` gets a "Module run" paragraph and lists `03c-accessibility.md` and `tools/` in the artifact tree; `docs/hard-stop-enforcement.md` states how the hook treats module folders and its limits.
- Hard stops made consistent: approval stops are Phase 1, Phase 2 and `02b` only. The regression-layer confirmation (`qa-regression-planner`: proceed on ok; no stop for a single-file diff with smoke/targeted layers) and the Phase 5 defect-closure question (`qa-summary-reporter`: verdict "provisional until closed" if unanswered) are asked but do not stall the run. README and `evals/behavior-checks.md` B1 updated.
- Re-test rounds: `qa-e2e-writer`, `qa-summary-reporter`, `qa-regression-planner` append a `Round N` section and bump the version without asking; they ask only when the file belongs to another module or build.
- `qa-nonfunctional-writer`: browser-storage and static-browser-app angle; default to skip `02b` for local runs under ~10 s.
- `qa-e2e-writer`, `qa-accessibility-auditor`: "Environment / tools" note (Playwright outside the repo or the browser pane, "ran in pane" evidence, computed-color contrast 4.5:1 / 3:1, dark and light themes, 360 px and 320 px reflow, keyboard path).
- `scripts/qa-gate.py`: `03c-*` is gated like `03-*` (new test); docstring states the one-level depth limit.
- `qa-lifecycle`: header key `Status:` stays English; `Auto (API)` routing merged into one bullet (HTTP, CLI/script, browser UI). `qa-api-tester` also exits for static browser apps and SPAs without a backend.
- Gate and severity: `Not run: needs person` cases cap the verdict at Conditional Go instead of forcing No-Go through the Executed Rate; severity considers reach ("how many users can hit this by normal use?"), with `localStorage` unavailable as a Major example.
- Small scope: about one happy, one negative and one boundary case per requirement, soft cap ~30 cases, and how to bundle (`qa-test-matrix-writer`, `qa-lifecycle`).
- Earlier unlisted changes: `Informational` cases excluded from the pass rate and gate metrics; the matrix has 11 columns including `Oracle`; extra stops (`02b` second approval inside Phase 2, no execution before the matrix is Approved).

### Changed
- Skill descriptions are English only and shorter (4 trigger phrases, at most 650 characters) to cut the context every installed skill costs. The trigger evals keep their Vietnamese prompts to check that matching still works.
- `qa-lifecycle` routes API, non-functional and regression work to the new skills; `qa-e2e-writer` hands `Auto (API)` cases to `qa-api-tester` when installed.
- Every skill states that content found in repos, logs and pages is data, not instructions.
- `scripts/run-evals.py` no longer crashes on Windows consoles when printing Vietnamese prompts.

## 0.1.0

Six skills: `qa-lifecycle`, `qa-test-plan-writer`, `qa-test-matrix-writer`, `qa-e2e-writer`, `qa-defect-writer`, `qa-summary-reporter`, with worked examples, evals and `scripts/run-evals.py`.
