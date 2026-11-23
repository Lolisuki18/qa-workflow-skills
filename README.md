# qa-workflow-skills

A standalone set of **Agent Skills** covering the whole software testing life cycle (STLC), following the open Anthropic Agent Skills specification. Works with Claude Code, Cursor, Gemini CLI, Codex and any other AI coding agent that reads `SKILL.md`.

Designed for developers who are not QA specialists: the AI acts as a **proactive QA advisor** — explaining why each check matters, warning about blind spots, and proposing defaults you can accept quickly.

The skills are written in English and reply in the language you use (English or Vietnamese). Each `description` is English only; requests in Vietnamese still match it.

## Skill index

<!-- skills:start -->
**10 skills.** This index is generated from each `SKILL.md`; run `python scripts/readme-index.py` to refresh it.

| Skill | What it does |
|---|---|
| [`qa-accessibility-auditor`](qa-accessibility-auditor/SKILL.md) | Audits a web UI for accessibility against WCAG 2.2 level AA by combining a code and DOM review, an automated scan when a tool is available |
| [`qa-api-tester`](qa-api-tester/SKILL.md) | Designs and runs API tests for the Auto (API) cases of the approved test matrix |
| [`qa-defect-writer`](qa-defect-writer/SKILL.md) | Turns raw bug descriptions, logs and screenshots into standardized Defect Reports (title, environment, severity vs priority, pre-conditions |
| [`qa-e2e-writer`](qa-e2e-writer/SKILL.md) | Executes test cases from the approved test matrix — produces manual run scripts and exploratory charters for Manual cases |
| [`qa-lifecycle`](qa-lifecycle/SKILL.md) | Orchestrates a 5-phase QA/QC workflow (STLC) — requirement audit and test plan, test case matrix with RTM, test execution and automation |
| [`qa-nonfunctional-writer`](qa-nonfunctional-writer/SKILL.md) | Designs non-functional test cases and checks from the approved test plan |
| [`qa-regression-planner`](qa-regression-planner/SKILL.md) | Selects the regression suite for a new build or fix from the RTM, the change set and defect history |
| [`qa-summary-reporter`](qa-summary-reporter/SKILL.md) | Compiles a Test Summary Report from real execution results and defect lists (or qa-artifacts/) |
| [`qa-test-matrix-writer`](qa-test-matrix-writer/SKILL.md) | Designs a complete test case table (TC ID, Req/UC ID, Module, Title, Pre-condition, Steps, Test Data, Expected Result, Priority P0-P3 |
| [`qa-test-plan-writer`](qa-test-plan-writer/SKILL.md) | Audits requirements for ambiguity, missing error flows, missing permission rules and business contradictions, then drafts a Test Plan with scope |
<!-- skills:end -->

## 5 phases, 10 skills

| Phase | Skill | Output (`qa-artifacts/`) |
|---|---|---|
| Orchestration | `qa-lifecycle` | Drives the 5 phases with approval hard stops |
| 1. Requirement audit & strategy | `qa-test-plan-writer` | `01-test-plan.md` |
| 2. Test case design | `qa-test-matrix-writer` | `02-test-matrix.md` (+ RTM) |
| 3. Execution & automation | `qa-e2e-writer` | `03-execution-notes.md` + Playwright code |
| 4. Defect management | `qa-defect-writer` | `04-defects.md` |
| 5. Reporting & acceptance | `qa-summary-reporter` | `05-summary-report.md` |

Optional specialist skills, used inside the phases above:

| Skill | Used in | Output |
|---|---|---|
| `qa-api-tester` | Phase 3, `Auto (API)` cases: endpoint inventory, API checklist, real results | API track in `03-execution-notes.md` |
| `qa-nonfunctional-writer` | Phase 2-3: performance, security basics, accessibility, compatibility with measurable thresholds | `02b-nonfunctional.md` + non-functional track in `03-execution-notes.md` |
| `qa-regression-planner` | Phase 4, every new build: smoke / targeted / full selection from the RTM and the diff | `04b-regression-plan.md` |
| `qa-accessibility-auditor` | Phase 3: WCAG 2.2 AA audit from code, an automated scan and manual keyboard / screen-reader checks | `03c-accessibility.md` |

## Repository layout

```text
qa-workflow-skills/
├── README.md
├── qa-lifecycle/            (SKILL.md, references/phase-templates.md, worked-example.md)
├── qa-test-plan-writer/     (SKILL.md, references/worked-example.md)
├── qa-test-matrix-writer/   (SKILL.md, references/test-design-techniques.md, worked-example.md)
├── qa-e2e-writer/           (SKILL.md, references/playwright-standards.md, exploratory-charters.md, worked-example.md)
├── qa-defect-writer/        (SKILL.md, references/severity-priority-matrix.md, worked-example.md)
├── qa-summary-reporter/     (SKILL.md, references/release-gate-criteria.md, worked-example.md)
├── qa-api-tester/           (SKILL.md, references/api-test-checklist.md)
├── qa-nonfunctional-writer/ (SKILL.md, references/nonfunctional-catalog.md)
├── qa-regression-planner/   (SKILL.md, references/regression-selection.md, worked-example.md)
├── qa-accessibility-auditor/ (SKILL.md, references/wcag-checklist.md)
├── docs/hard-stop-enforcement.md, tests/test_qa_gate.py
├── scripts/                 validate.py (structure checks, also run by CI), install.py, run-evals.py
├── .github/workflows/validate.yml
├── LICENSE
├── evals/                   Trigger prompts and behavior checks
```

## Installation

Copy (or symlink) the ten `qa-*` folders to where your agent reads skills. **Install them together** and keep them as siblings: in agents without automatic skill switching, `qa-lifecycle` reads `../qa-<name>/SKILL.md` directly.

| Agent | Skills folder (for reference; check your agent's docs) |
|---|---|
| Claude Code | `~/.claude/skills/` or `<project>/.claude/skills/` |
| Cursor | `.cursor/skills/` (also reads `.claude/skills/`) |
| Gemini CLI | `.gemini/skills/` or `.agents/skills/`; user-level `~/.gemini/skills/` (may need enabling; check `gemini skills list`) |
| Codex | `.agents/skills/` (older docs: `.codex/skills/`) |
| Others | any tool that reads `SKILL.md` folders, or point the agent at the `SKILL.md` files |

Paths change between agent versions; confirm against your tool's docs. The folder name of each skill must equal its `name`.

```powershell
# project-level install for Claude Code (run from the repo root)
New-Item -ItemType Directory -Force .claude\skills | Out-Null
Get-ChildItem -Directory -Filter 'qa-*' | ForEach-Object { Copy-Item -Recurse $_.FullName .claude\skills\ }
```

Each skill also works on its own; only `qa-lifecycle` expects the others to be present, and it says so when one is missing. The three specialist skills are optional.

One-command install (links on Windows via junctions, symlinks elsewhere; never overwrites):

```powershell
python scripts/install.py                        # ~/.claude/skills
python scripts/install.py --agent gemini         # other presets: --list-agents
python scripts/install.py --dry-run              # preview
```

## Usage

Just speak naturally, for example:

- "Run a full QA process for the login feature" → `qa-lifecycle`
- "Write a test plan from this SRS" → `qa-test-plan-writer`
- "Generate test cases and an RTM for the shopping cart module" → `qa-test-matrix-writer`
- "Write Playwright tests for the Auto (browser) cases" → `qa-e2e-writer`
- "Turn this raw bug description into a proper defect report" → `qa-defect-writer`
- "Is this ready to release? Write the summary report" → `qa-summary-reporter`
- "Test these REST endpoints for auth and validation" → `qa-api-tester`
- "Design performance and accessibility tests for checkout" → `qa-nonfunctional-writer`
- "The dev fixed 5 bugs, which tests should I re-run?" → `qa-regression-planner`
- "Audit the checkout page for accessibility (WCAG)" → `qa-accessibility-auditor`

Every `qa-lifecycle` response starts with the label `[QA Phase X/5: Phase Name]`. Phases 1 and 2 have a **Hard Stop**: the AI waits for your approval before continuing. For Claude Code an optional hook (`scripts/qa-gate.py`) enforces the stops with the artifact status; see [docs/hard-stop-enforcement.md](docs/hard-stop-enforcement.md).

## Core principles

- **Anti-hallucination:** never invents Pass/Fail numbers, environments, browser versions or reproduction steps; missing data is written as `[Needs input: ...]` or asked about.
- **No unit-test confusion:** these skills cover testing from the QA viewpoint (functional, E2E, API, exploratory), not developers' unit tests.
- **Progressive disclosure:** each `SKILL.md` stays short (<250 lines); long material lives in `references/`, one level deep.
- **Self-contained:** no dependency on skills outside this set.
- **Evidence over narrative:** Playwright results are read from a JSON/JUnit report when available, not retyped from terminal text.

## Worked examples

Each skill has a `references/worked-example.md` built on one fictional scenario ("DemoShop" login) so IDs and figures stay consistent from test plan to Go/No-Go report. The data is fictional — never copy it into a real project.

## Self-check (evals)

See [evals/](evals/README.md): trigger prompts (should / should not fire each skill) and behavior checks (phase label, hard stops, anti-hallucination). `scripts/run-evals.py` can run the trigger prompts automatically against an agent CLI (see the evals README for caveats). Results vary by agent and model. Status: the eval sets are written but their results are not yet recorded, and `python scripts/validate.py` (also run by GitHub Actions) checks structure only: names, descriptions, line counts, references. `scripts/run-evals.py` needs an agent CLI that is not verified here.

## Sibling repos

| Repo | Covers |
|---|---|
| [`dev-workflow-skills`](https://github.com/Lolisuki18/dev-workflow-skills) | idea → plan → code → tests → audit, bug investigation |
| [`pull-request-skills`](https://github.com/Lolisuki18/pull-request-skills) | PR description, PR review, review replies, pre-PR self-review, code comments |
| [`qa-workflow-skills`](https://github.com/Lolisuki18/qa-workflow-skills) (this one) | QA/STLC from test plan to Go/No-Go report |
| `ai-workflow-suite` | `delivery-lifecycle` orchestrator across all four repos, shared `CONVENTIONS.md`, `install-all.py` |
| [`docs-workflow-skills`](https://github.com/Lolisuki18/docs-workflow-skills) | README, diagrams, API docs, ADRs, SDLC reports, Review 2 pack |

Developers' unit tests belong to `test-case-writer` in `dev-workflow-skills`; this repo covers testing from the QA viewpoint.
