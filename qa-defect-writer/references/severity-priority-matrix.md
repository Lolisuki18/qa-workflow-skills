# Severity vs Priority Matrix

**Severity** = how serious the defect is **technically / in impact on the system** (how bad is it).
**Priority** = how **urgent it is for the business** (when it must be fixed). Two independent axes: a high-Severity bug can have low Priority and vice versa.

## Severity (technical)

| Level | Definition | Realistic examples (illustrative) |
|---|---|---|
| **Blocker** | Total blocker: cannot test/use further; system down; no workaround | App will not start; nobody can log in; build crashes on open |
| **Critical** | Core function broken, data loss/corruption, security hole, wrong money; no workaround | User A sees user B's data; payment charged twice; deleting another user's data |
| **Major** | Main function wrong or missing but a workaround exists, or a significant user group is affected | Date filter returns wrong results (still searchable by hand); PDF export fails but CSV works |
| **Minor** | Secondary function wrong, small impact, easy workaround | Wrong column sort on a secondary page; error message wording off but still blocks correctly |
| **Trivial** | Cosmetic/typo, no functional impact | Label typo; a few pixels of misalignment; wrong icon weight |

### Questions to decide Severity (ask in order, stop at the first "yes")
1. Is the system/main flow usable at all? No → **Blocker**.
2. Is there data loss/corruption, wrong money, data exposure, or privilege escalation? Yes → **Critical**.
3. Is a main function wrong/missing? Yes → **Major** (a workaround still counts as Major; record the workaround).
4. Is a secondary function wrong? → **Minor**.
5. Only presentation? → **Trivial**.

## Priority (business)

| Level | Meaning | Action | Example |
|---|---|---|---|
| **P0** | Urgent: fix now, blocks release/operation | Drop other work; hotfix | Payment failure in production; customer data exposure |
| **P1** | High: fix in the current release | Put into the current sprint/release | Main function bug with no clear workaround |
| **P2** | Medium: schedule it | Next release | Secondary function bug with a workaround |
| **P3** | Low: when time allows | Backlog | Cosmetic bug, very rare case |

> The P0–P3 of a **defect** uses the same names as the Priority of a **test case**, but means something different: test-case Priority = importance when running tests; defect Priority = urgency of fixing. Do not mix them up when reporting.

## Combination table (how the two axes usually pair)

| Severity \ Priority | P0 | P1 | P2 | P3 |
|---|---|---|---|---|
| Blocker | Common | Possible (blocks the test environment, not production) | Rare | Rare |
| Critical | Common | Common | Rare | Rare |
| Major | Possible (on a revenue flow/peak day) | Common | Common | Rare |
| Minor | Rare | Possible (shown to VIP customers/demo) | Common | Common |
| Trivial | Very rare | Possible (wrong logo/brand name) | Possible | Common |

### Skewed examples (to explain to users)
- **Low Severity, high Priority:** company name misspelled on the home page before a launch event → Trivial / P1.
- **High Severity, low Priority:** crash in an old feature almost nobody uses, only under an unusual configuration → Critical / P2 (the user/PO must confirm real usage).

## Factors that adjust Priority (ask if unknown)

- Number of affected users and how often they hit it.
- Whether an easy workaround exists.
- Whether it sits on a revenue/legal/security flow.
- Whether a release/demo milestone is near.
- Whether it appears in production or only in the test environment.

Final Priority belongs to the Product Owner/user. QA **proposes** it with a reason.

## One-line reason template

```text
Severity: Critical — a regular user can view another user's invoice (data exposure), no workaround.
Priority: P0 (proposed) — affects all customers, release should be blocked.
```

## Reproducibility rules

| Reproduction ratio | Record as |
|---|---|
| Always (n/n) | `Always (n/n)` |
| Sometimes | `Intermittent (x/y)` + suspected conditions if any |
| Not reproduced | `Cannot Reproduce` — keep the log/description, ask for more information |

Record a ratio only after actually trying; not tried → `[Needs input: number of attempts]`.
