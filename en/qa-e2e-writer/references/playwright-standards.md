# Playwright Standards

Standards for writing Playwright tests (TypeScript in examples; if the repo uses JS/Python keep the same principles). **Always follow the repo's existing configuration and conventions** if Playwright is already set up.

## Mandatory rules

1. **Page Object Model (POM):** one class per page/UI area; specs contain no locators, only calls to page-object actions.
2. **Semantic locators in priority order:**
   1. `getByRole('button', { name: '...' })`
   2. `getByLabel('...')`
   3. `getByPlaceholder('...')`
   4. `getByText('...')` (for static, stable content)
   5. `getByTestId('...')` — when 1–4 are not enough; if the app has no `data-testid`, propose that developers add it.
3. **Forbidden:** long/structure-dependent CSS (`div > div:nth-child(3) .btn`), XPath, auto-generated classes (`.css-1x2y3z`), positional indexes (unless testing an ordered list itself). If CSS is unavoidable, explain in a short comment.
4. **`waitForTimeout(...)` and `sleep` are strictly forbidden.** Wait with web-first assertions or concrete conditions (`waitForResponse`, `waitForURL`).
5. **Web-first assertions:** `await expect(locator).toBeVisible()`, `toHaveText`, `toHaveValue`, `toBeEnabled`, `toHaveURL`. Do not use `expect(await locator.isVisible()).toBe(true)` (no auto-retry).
6. **Independence:** each test creates/cleans its own data, never relies on another test or run order; must be runnable in parallel. No shared global state.
7. **One test = one TC ID**; the title starts with the TC ID; assertions verify exactly the case's Expected Result.
8. **No hard-coded secrets:** take credentials from environment variables or the repo's fixtures; never put real information in source.
9. **Inspect the real DOM before writing locators** (read templates/components or open the page). Never guess labels/roles.

## Suggested structure (follow the repo if it differs)

```text
tests/
├── e2e/
│   └── login.spec.ts
├── pages/
│   └── LoginPage.ts
├── fixtures/
│   └── test-data.ts
```

## Sample Page Object

```ts
import { type Locator, type Page, expect } from '@playwright/test';

export class LoginPage {
  readonly page: Page;
  readonly email: Locator;
  readonly password: Locator;
  readonly submit: Locator;
  readonly errorAlert: Locator;

  constructor(page: Page) {
    this.page = page;
    // Label/role names below are illustrative — replace with values read from the app's real DOM.
    this.email = page.getByLabel('Email');
    this.password = page.getByLabel('Password');
    this.submit = page.getByRole('button', { name: 'Log in' });
    this.errorAlert = page.getByRole('alert');
  }

  async goto() {
    await this.page.goto('/login');
  }

  async login(email: string, password: string) {
    await this.email.fill(email);
    await this.password.fill(password);
    await this.submit.click();
  }

  async expectError(text: string | RegExp) {
    await expect(this.errorAlert).toContainText(text);
  }
}
```

## Sample spec

```ts
import { test, expect } from '@playwright/test';
import { LoginPage } from '../pages/LoginPage';

test.describe('Login', () => {
  test('TC-LOGIN-002: rejects login with a wrong password', async ({ page }) => {
    const login = new LoginPage(page);
    await login.goto();
    await login.login(process.env.TEST_USER_EMAIL!, 'wrong-password');
    await login.expectError(/.+/); // replace with the exact message once the spec provides it
    await expect(page).toHaveURL(/\/login/);
  });
});
```

## Data & independence

- Use APIs/fixtures to create data before a test and clean it after (`beforeEach`/`afterEach`, or Playwright fixtures).
- Unique names/emails per test (e.g. random suffix) when a test creates records.
- Log in via `storageState` for tests that are not about login, for speed and stability; login cases go through the UI.
- Permissions: use a separate context per role; a test never changes another context's role.

## Waiting & synchronization

| Need | Correct approach |
|---|---|
| Wait for an element to appear | `await expect(loc).toBeVisible()` |
| Wait for navigation | `await expect(page).toHaveURL(...)` |
| Wait for an API call | `const resp = page.waitForResponse(...)` placed **before** the triggering action, then `await resp` |
| Wait for a loader to disappear | `await expect(spinner).toBeHidden()` |
| Slow/lost network (Error Guessing cases) | `page.route()` to block/delay in a controlled way, `context.setOffline(true)` |

## Recommended configuration (if the repo has none and the user agrees)

- Low `retries` in CI (0–2); never use retries to hide flakiness.
- `trace: 'on-first-retry'`, `screenshot: 'only-on-failure'` to produce evidence for defects.
- `baseURL` from an environment variable; `webServer` if the app starts with one command. **The command and port must come from the repo**, never guessed.

## Running & reporting

- Run with the repo's command (usually `npx playwright test`); narrow by file/title (`-g "TC-LOGIN"`).
- Paste the **real output** (passed/failed counts, failing test names, error messages) into `03-execution-notes.md`. Never add up or adjust numbers yourself.
- Failing test: attach the trace/screenshot path if any; otherwise write "none".

## Self-check before handing over

- [ ] No `waitForTimeout`, `page.$`/`$$`, XPath, `nth-child`
- [ ] Every locator cross-checked against the real DOM/code
- [ ] Specs contain no direct locators (they live in page objects)
- [ ] Each test passes when run alone (`-g` a single test)
- [ ] Assertions are web-first and check the TC's Expected Result
- [ ] No credentials/real data in source
