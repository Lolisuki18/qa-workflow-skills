# Worked Example — qa-e2e-writer

> ⚠️ **Fictional** data and run results ("DemoShop") to illustrate the format. In real use, every output must be the real output of a command you actually ran.

## 1. Inspection before writing locators (sample report)

```markdown
Read `src/pages/Login.tsx`: the button reads "Log in" (role button), inputs have labels "Email" and "Password". No `data-testid` yet. The error message sits in an element with `role="alert"`.
→ Use getByLabel / getByRole, no CSS needed. The /admin page has no stable identifying element → propose that developers add `data-testid="admin-page"`.
```

## 2. Spec for TC-LOGIN-006 (shortened)

```ts
test('TC-LOGIN-006: regular user is blocked from /admin', async ({ page }) => {
  const login = new LoginPage(page);
  await login.goto();
  await login.login(process.env.TEST_USER_EMAIL!, process.env.TEST_USER_PASSWORD!);
  await page.goto('/admin');
  await expect(page).toHaveURL(/\/dashboard/);
});
```

## 3. Run results recorded in `03-execution-notes.md` (fictional numbers)

```markdown
Round 1 · Build/environment: [Needs input] · Command: `PLAYWRIGHT_JSON_OUTPUT_NAME=test-results.json npx playwright test --reporter=json -g "TC-LOGIN"` · Report file: `test-results.json` (results table built from this file)
Output (pasted verbatim from the terminal): "1 failed — TC-LOGIN-006 — Expected /dashboard, Received /admin" ...

| TC ID | Execution Type | Result | Defect ID | Notes |
|---|---|---|---|---|
| TC-LOGIN-001 | Auto (browser) | Pass | | |
| TC-LOGIN-002 | Auto (browser) | Pass | | |
| TC-LOGIN-003 | Auto (browser) | Pass | | |
| TC-LOGIN-004 | Auto (API) | Pass | | |
| TC-LOGIN-005 | Auto (API) | Pass | | |
| TC-LOGIN-006 | Auto (browser) | **Fail** | DEF-001 | Reproduced by hand: a regular user still sees the admin page |
| TC-LOGIN-007 | Manual | Pass | | Reported by the user |
| TC-LOGIN-008 | Manual | **Not Run** | | Not yet run |
| TC-LOGIN-009 | Auto (browser) | Pass | | |
```

## 4. Classifying failures

TC-LOGIN-006 failed → checked by hand and saw the same symptom, the locator is irrelevant → **product defect**, move to Phase 4. TC-LOGIN-008 not yet run by the user → stays `Not Run`, never filled in.

**Takeaways:** inspect the DOM before choosing locators; test titles carry the TC ID; output pasted verbatim; cases not run are `Not Run`.
