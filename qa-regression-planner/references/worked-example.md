# Worked Example — qa-regression-planner

> ⚠️ **Fictional** data ("DemoShop") to illustrate the format. In real use, the mapping comes from the real diff, imports and RTM; effort numbers come from real past runs or stay `[Needs input]`. Never copy these into a real project.

## 1. Change set

```markdown
Build: v1.4.2 → v1.4.3 (`git diff --stat v1.4.2..v1.4.3`: 3 files)
- src/cart/total.ts: rounding rule
- src/shared/validators.ts: validateQty only (validateEmail unchanged)
- DEF-012 (cart total off by 1 cent), DEF-014 (qty accepts 0) → both Fixed
```

## 2. `04b-regression-plan.md` (excerpt)

```markdown
| Changed area | Impacted requirements | Cases | Why | Layer |
|---|---|---|---|---|
| src/cart/total.ts | REQ-05 | TC-CART-001..004 | Direct change (diff) | Targeted |
| validateQty in shared/validators.ts | REQ-05, REQ-09 | TC-CART-003, TC-ORDER-002 | Imported by cart/form.ts:12 and order/create.ts:8 | Targeted |
| DEF-012 fix | REQ-05 | TC-CART-002 | Re-test of a fixed defect (P0) | Targeted |
| DEF-014 fix | REQ-09 | TC-CART-003 | Re-test of a fixed defect (boundary qty = 0) | Targeted |
| Login happy path | REQ-01 | TC-LOGIN-001 | P0 main flow | Smoke |

Smoke (run first): TC-LOGIN-001, TC-CART-001, TC-CART-002.
Targeted (after smoke): TC-CART-003, TC-CART-004, TC-ORDER-002.
Full: not recommended (3 files, no config or schema change); escalate if any smoke case fails or more than [Needs input: agreed share] of targeted cases fail.

Excluded, with reason: TC-PROFILE-001..003 (profile code does not import the changed files: `grep -n import src/profile/*`), TC-REPORT-001..002 (unrelated module). No P0 case excluded.

Effort: [Needs input: no timings in the execution notes yet]; 6 cases, Manual/Auto split [Needs input].
Blind spots: shared code outside `src/`, config and data are not visible in the diff.
```

Default offered to the user: "smoke first, then targeted; full only if something fails".
