# Ví dụ chạy thật — qa-e2e-writer

> ⚠️ Dữ liệu và kết quả chạy **hư cấu** ("DemoShop") để minh hoạ định dạng. Trong thực tế, mọi output phải là output thật của lệnh đã chạy.

## 1. Khảo sát trước khi viết locator (ví dụ cách báo cáo)

```markdown
Đã đọc `src/pages/Login.tsx`: nút có chữ "Đăng nhập" (role button), input có label "Email" và "Mật khẩu". Chưa có `data-testid`. Thông báo lỗi nằm trong phần tử `role="alert"`.
→ Dùng getByLabel / getByRole, không cần CSS. Trang /admin không có phần tử nhận diện ổn định → đề xuất dev thêm `data-testid="admin-page"`.
```

## 2. Spec cho TC-LOGIN-006 (rút gọn)

```ts
test('TC-LOGIN-006: user thường bị chặn khi vào /admin', async ({ page }) => {
  const login = new LoginPage(page);
  await login.goto();
  await login.login(process.env.TEST_USER_EMAIL!, process.env.TEST_USER_PASSWORD!);
  await page.goto('/admin');
  await expect(page).toHaveURL(/\/dashboard/);
});
```

## 3. Kết quả chạy ghi vào `03-execution-notes.md` (số liệu hư cấu)

```markdown
Vòng 1 · Build/môi trường: [Cần bổ sung] · Lệnh: `npx playwright test -g "TC-LOGIN"`
Output (dán nguyên văn từ terminal): "1 failed — TC-LOGIN-006 — Expected /dashboard, Received /admin" ...

| TC ID | Execution Type | Kết quả | Defect ID | Ghi chú |
|---|---|---|---|---|
| TC-LOGIN-001 | Auto (browser) | Pass | | |
| TC-LOGIN-002 | Auto (browser) | Pass | | |
| TC-LOGIN-003 | Auto (browser) | Pass | | |
| TC-LOGIN-004 | Auto (API) | Pass | | |
| TC-LOGIN-005 | Auto (API) | Pass | | |
| TC-LOGIN-006 | Auto (browser) | **Fail** | DEF-001 | Tái hiện bằng tay: user thường vẫn thấy trang quản trị |
| TC-LOGIN-007 | Manual | Pass | | Người dùng báo |
| TC-LOGIN-008 | Manual | **Not Run** | | Chưa chạy |
| TC-LOGIN-009 | Auto (browser) | Pass | | |
```

## 4. Phân loại lỗi

TC-LOGIN-006 fail → thử tay thấy đúng hiện tượng, locator không liên quan → **lỗi sản phẩm**, chuyển Pha 4. TC-LOGIN-008 người dùng chưa chạy → giữ `Not Run`, không tự điền.

**Điểm cần học:** khảo sát DOM trước khi đặt locator; tiêu đề test mang TC ID; output dán nguyên văn; case chưa chạy là `Not Run`.
