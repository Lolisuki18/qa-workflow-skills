# Regression selection guide

## Layers

| Layer | Purpose | Contents | When to use |
|---|---|---|---|
| Smoke | Is the build testable at all? | P0 happy paths of main flows: login, core create/read, payment or main transaction | Every new build, first |
| Targeted | Did this change break what it touches? | All cases of changed areas, fixed defects' re-tests, and direct neighbours | Default for a normal fix or small feature |
| Full | Release confidence | Whole matrix, Manual and Auto | Release candidate, large refactor, schema or framework change, or a failed targeted run |

## Mapping change to cases

1. Start from the diff: files, then modules or features.
2. Use the RTM: requirement ID → test case IDs.
3. Expand by dependency:
   - callers and importers of changed functions
   - shared components, utilities, validators, middleware
   - shared tables, queues, config and feature flags
   - API consumers (front end, other services, mobile)
4. Add the re-test case for every defect fixed in this build (from `04-defects.md`), plus a regression check of the "related regression" list recorded there.
5. Add past-defect hotspots: modules with two or more defects in earlier rounds.

## Risk levels

| Level | Typical signs |
|---|---|
| High | P0/P1 case in a directly changed area; money, permissions, personal data; area with repeated defects |
| Medium | Directly changed P2 area; neighbour of a changed P0 area |
| Low | Unchanged area with no shared code; P3 cosmetic cases |

Order of execution: High first, then Medium, then Low. Within a level, Auto cases first (cheap), Manual after.

## Config, data and environment changes

Changes with no code diff (config, feature flags, data migrations, dependency or runtime upgrades, infra) map to no test case by file. Treat them as widening the scope: at least smoke plus the flows that read that config or data. If the impact cannot be judged, recommend full.

## Exit conditions to write in the plan

- Stop and report when any smoke case fails.
- Escalate to full when more than the agreed share of targeted cases fail (ask the user for the share; suggest a small number such as 10%).
- Mark every skipped case with who decided and why.

## Output table example

```text
| Changed area | Impacted requirements | Cases | Why | Layer |
|---|---|---|---|---|
| auth/token.ts | R3, R7 | TC-LOGIN-001..006 | Direct change (diff) | Targeted |
| shared/validators.ts | R3, R9, R14 | TC-CART-010..015 | Imported by cart form (cart/form.ts:12) | Targeted |
| DEF-004 fix | R9 | TC-CART-012 | Re-test of fixed defect | Targeted |
| Login happy path | R1 | TC-LOGIN-001 | P0 main flow | Smoke |
```
