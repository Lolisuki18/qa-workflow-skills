# Playwright Standards

Chuẩn viết test Playwright (TypeScript làm ví dụ; nếu repo dùng JS/Python thì giữ cùng nguyên tắc). **Luôn theo cấu hình và quy ước sẵn có của repo** nếu đã có Playwright.

## Luật bắt buộc

1. **Page Object Model (POM):** mỗi trang/khu vực UI = một class; spec không chứa locator trực tiếp, chỉ gọi hành động của page object.
2. **Semantic locators theo thứ tự ưu tiên:**
   1. `getByRole('button', { name: '...' })`
   2. `getByLabel('...')`
   3. `getByPlaceholder('...')`
   4. `getByText('...')` (cho nội dung tĩnh, ổn định)
   5. `getByTestId('...')` — khi 1–4 không đủ; nếu app chưa có `data-testid`, đề xuất dev thêm.
3. **Cấm** CSS dài/phụ thuộc cấu trúc (`div > div:nth-child(3) .btn`), XPath, class tự sinh (`.css-1x2y3z`), index vị trí (trừ khi test chính danh sách có thứ tự). Nếu bắt buộc dùng CSS, giải thích ngắn bằng comment.
4. **Cấm tuyệt đối `waitForTimeout(...)`** và `sleep`. Chờ bằng web-first assertions hoặc điều kiện cụ thể (`waitForResponse`, `waitForURL`).
5. **Web-first assertions:** `await expect(locator).toBeVisible()`, `toHaveText`, `toHaveValue`, `toBeEnabled`, `toHaveURL`. Không dùng `expect(await locator.isVisible()).toBe(true)` (không tự retry).
6. **Độc lập:** mỗi test tự tạo/dọn dữ liệu, không dựa vào test khác hay thứ tự chạy; chạy song song được. Không dùng biến toàn cục chia sẻ trạng thái.
7. **Một test = một TC ID**, tiêu đề bắt đầu bằng TC ID; assertion kiểm đúng Expected Result của case.
8. **Không hard-code bí mật:** tài khoản/mật khẩu lấy từ biến môi trường hoặc fixture của repo; không đưa thông tin thật vào mã nguồn.
9. **Kiểm tra DOM thật trước khi viết locator** (đọc template/component hoặc mở trang). Không đoán label/role.

## Cấu trúc gợi ý (theo repo nếu đã khác)

```text
tests/
├── e2e/
│   └── login.spec.ts
├── pages/
│   └── LoginPage.ts
├── fixtures/
│   └── test-data.ts
```

## Page Object mẫu

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
    // Tên label/role dưới đây là minh hoạ — thay bằng giá trị đọc từ DOM thật của app.
    this.email = page.getByLabel('Email');
    this.password = page.getByLabel('Mật khẩu');
    this.submit = page.getByRole('button', { name: 'Đăng nhập' });
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

## Spec mẫu

```ts
import { test, expect } from '@playwright/test';
import { LoginPage } from '../pages/LoginPage';

test.describe('Login', () => {
  test('TC-LOGIN-002: từ chối đăng nhập khi sai mật khẩu', async ({ page }) => {
    const login = new LoginPage(page);
    await login.goto();
    await login.login(process.env.TEST_USER_EMAIL!, 'wrong-password');
    await login.expectError(/.+/); // thay bằng thông báo chính xác từ đặc tả khi đã có
    await expect(page).toHaveURL(/\/login/);
  });
});
```

## Dữ liệu & độc lập

- Dùng API/fixture để tạo dữ liệu trước test và dọn sau test (`beforeEach`/`afterEach`, hoặc fixture của Playwright).
- Tên/email duy nhất theo test (ví dụ thêm hậu tố ngẫu nhiên) khi test tạo bản ghi.
- Đăng nhập bằng `storageState` cho test không nhằm kiểm đăng nhập, để nhanh và ổn định; case đăng nhập thì đi qua UI.
- Phân quyền: dùng context riêng cho từng vai trò; một test không đổi vai trò của context khác.

## Chờ và đồng bộ

| Nhu cầu | Cách đúng |
|---|---|
| Chờ phần tử xuất hiện | `await expect(loc).toBeVisible()` |
| Chờ điều hướng | `await expect(page).toHaveURL(...)` |
| Chờ API xong | `const resp = page.waitForResponse(...)` đặt **trước** hành động kích hoạt, rồi `await resp` |
| Chờ loading biến mất | `await expect(spinner).toBeHidden()` |
| Mạng chậm/rớt mạng (case Error Guessing) | `page.route()` để chặn/làm chậm có kiểm soát, `context.setOffline(true)` |

## Cấu hình khuyến nghị (nếu repo chưa có và người dùng đồng ý)

- `retries` thấp ở CI (0–2); không dùng retry để che flaky.
- `trace: 'on-first-retry'`, `screenshot: 'only-on-failure'` để có bằng chứng cho defect.
- `baseURL` từ biến môi trường; `webServer` nếu app chạy được bằng một lệnh. **Lệnh và cổng phải lấy từ repo**, không đoán.

## Chạy và báo cáo

- Chạy: lệnh của repo (thường `npx playwright test`); có thể giới hạn theo file/tiêu đề (`-g "TC-LOGIN"`).
- Dán **output thật** (số passed/failed, tên test fail, thông báo lỗi) vào `03-execution-notes.md`. Không tự cộng/trừ số liệu.
- Test fail: đính kèm đường dẫn trace/screenshot nếu có; không có thì ghi "không có".

## Tự kiểm trước khi bàn giao

- [ ] Không có `waitForTimeout`, `page.$`/`$$`, XPath, `nth-child`
- [ ] Mọi locator đối chiếu DOM/code thật
- [ ] Spec không chứa locator trực tiếp (nằm trong page object)
- [ ] Test chạy độc lập từng cái (`-g` một test vẫn pass)
- [ ] Assertion dùng web-first, kiểm đúng Expected Result của TC
- [ ] Không có credential/dữ liệu thật trong mã nguồn
