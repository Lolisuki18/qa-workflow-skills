# qa-workflow-skills

🌐 [Tiếng Việt](README.md) · **English**

A standalone set of **Agent Skills** covering the whole software testing life cycle (STLC), following the open Anthropic Agent Skills specification. Works with Claude Code, Cursor, Gemini CLI, Codex and any other AI coding agent that reads `SKILL.md`.

Designed for developers who are not QA specialists: the AI acts as a **proactive QA advisor** — explaining why each check matters, warning about blind spots, and proposing defaults you can accept quickly.

## 5 phases, 6 skills

| Phase | Skill | Output (`qa-artifacts/`) |
|---|---|---|
| Orchestration | `qa-lifecycle` | Drives the 5 phases with approval hard stops |
| 1. Requirement audit & strategy | `qa-test-plan-writer` | `01-test-plan.md` |
| 2. Test case design | `qa-test-matrix-writer` | `02-test-matrix.md` (+ RTM) |
| 3. Execution & automation | `qa-e2e-writer` | `03-execution-notes.md` + Playwright code |
| 4. Defect management | `qa-defect-writer` | `04-defects.md` |
| 5. Reporting & acceptance | `qa-summary-reporter` | `05-summary-report.md` |

## Repository layout

```text
qa-workflow-skills/
├── README.md                 (Vietnamese)
├── README.en.md              (this file)
├── qa-lifecycle/ …           Vietnamese skills (6 folders)
├── en/                       English skills (same 6 folder names)
│   ├── qa-lifecycle/         (SKILL.md, references/phase-templates.md, worked-example.md)
│   ├── qa-test-plan-writer/  (SKILL.md, references/worked-example.md)
│   ├── qa-test-matrix-writer/(SKILL.md, references/test-design-techniques.md, worked-example.md)
│   ├── qa-e2e-writer/        (SKILL.md, references/playwright-standards.md, exploratory-charters.md, worked-example.md)
│   ├── qa-defect-writer/     (SKILL.md, references/severity-priority-matrix.md, worked-example.md)
│   └── qa-summary-reporter/  (SKILL.md, references/release-gate-criteria.md, worked-example.md)
└── evals/                    Trigger prompts and behavior checks (VI + EN)
```

> **Install only ONE language set.** Both sets use the same skill names (`name` must match the folder), so installing both would collide.

## Installation

Copy (or symlink) the six skill folders of **one** set — the `en/qa-*` folders for English — to where your agent reads skills:

| Agent | Skills folder (for reference; check your agent's docs) |
|---|---|
| Claude Code | `~/.claude/skills/` or `<project>/.claude/skills/` |
| Cursor / Gemini CLI / Codex | per each agent's skill/rules mechanism; you can also point the agent at the `SKILL.md` files |

## Usage

Just speak naturally, for example:

- "Run a full QA process for the login feature" → `qa-lifecycle`
- "Write a test plan from this SRS" → `qa-test-plan-writer`
- "Generate test cases and an RTM for the shopping cart module" → `qa-test-matrix-writer`
- "Write Playwright tests for the Auto (browser) cases" → `qa-e2e-writer`
- "Turn this raw bug description into a proper defect report" → `qa-defect-writer`
- "Is this ready to release? Write the summary report" → `qa-summary-reporter`

Every `qa-lifecycle` response starts with the label `[QA Phase X/5: Phase Name]`. Phases 1 and 2 have a **Hard Stop**: the AI waits for your approval before continuing.

## Core principles

- **Anti-hallucination:** never invents Pass/Fail numbers, environments, browser versions or reproduction steps; missing data is written as `[Needs input: ...]` (`[Cần bổ sung: ...]` in the Vietnamese set) or asked about.
- **No unit-test confusion:** these skills cover testing from the QA viewpoint (functional, E2E, API, exploratory), not developers' unit tests.
- **Progressive disclosure:** each `SKILL.md` stays short (<250 lines); long material lives in `references/`, one level deep.
- **Self-contained:** each skill works on its own; no dependency on skills outside this set.

## Worked examples

Each skill has a `references/worked-example.md` built on one fictional scenario ("DemoShop" login) so the IDs and figures stay consistent from test plan to Go/No-Go report. The data is fictional — never copy it into a real project.

## Self-check (evals)

See [evals/](evals/README.md): trigger prompts (should / should not fire each skill) and behavior checks (phase label, hard stops, anti-hallucination). Results vary by agent and model.
