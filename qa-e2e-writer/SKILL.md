---
name: qa-e2e-writer
description: Executes test cases from the approved test matrix — produces manual run scripts and exploratory charters for Manual cases, and writes and runs Playwright tests (Page Object Model, semantic locators, web-first assertions) for Auto (browser) cases, recording only real results in execution notes. Use when the user says 'run the tests', 'write Playwright tests', 'E2E test', 'browser automation', 'exploratory testing', 'manual test script', 'try to break the app', 'viết test Playwright', 'chạy test', 'kịch bản test tay', 'test thăm dò', 'phá app', 'tự động hoá test giao diện'. Do NOT use for designing the test plan or test case table (use qa-test-plan-writer or qa-test-matrix-writer), writing bug reports (use qa-defect-writer), summary reports (use qa-summary-reporter), or developer unit and integration tests.
---

# QA E2E Writer — Bước 3: Chạy test & Automation

Biến test case đã duyệt thành kịch bản chạy thật. Khi chạy trong `qa-lifecycle`, đây là Pha 3/5 (nhãn `[QA Phase 3/5: Execution]` ở dòng đầu).

## Quy tắc

- **Đầu vào:** `qa-artifacts/02-test-matrix.md` (hoặc CSV) đã duyệt. Chưa có → đề xuất chạy `qa-test-matrix-writer`; nếu người dùng vẫn muốn, hỏi danh sách case cần test.
- **Chống ảo giác:**
  - Không ghi Pass/Fail cho case chưa thực sự chạy. Case Manual người dùng chưa chạy = `Not Run`.
  - Không bịa môi trường, URL, phiên bản browser, tài khoản. Thiếu → `[Cần bổ sung: ...]` hoặc hỏi.
  - Khi dán kết quả automation, dán output thật của lệnh; không tóm tắt từ trí nhớ. Không chạy được (thiếu môi trường, app chưa lên) → ghi `Blocked` kèm nguyên nhân thật.
- **Kiểm tra code thực tế trước khi đặt locator:** đọc component/template/HTML hoặc mở app để xem cấu trúc DOM, label, role, `data-testid` có sẵn. Không đoán selector. Thiếu thuộc tính để định vị ổn định → đề xuất thêm `data-testid` cho dev, đừng viết CSS/XPath giòn.
- Agent-agnostic: dùng công cụ chạy lệnh/đọc file của môi trường hiện tại; không giả định IDE cụ thể.

## Quy trình

1. **Phân loại case** theo `Execution Type`: `Manual`, `Auto (browser)`, `Auto (API)`. Báo số lượng từng nhóm.
2. **Manual** → đọc `references/exploratory-charters.md`. Xuất:
   - Kịch bản bấm test nhanh, gom theo module/luồng để ít phải đổi ngữ cảnh (mỗi dòng: TC ID · bước · dữ liệu · kết quả mong đợi · ô để người dùng điền Pass/Fail/Blocked).
   - Các charter thăm dò theo tính năng: double-click, Back, reload giữa chừng, mất mạng, file nặng/sai định dạng...
   - Chờ người dùng báo kết quả; chỉ ghi những gì họ báo.
3. **Auto (browser)** → đọc `references/playwright-standards.md`, rồi:
   1. Kiểm tra repo: đã có Playwright chưa (`playwright.config.*`, `package.json`), cấu trúc thư mục test, baseURL, cách chạy app. Chưa có → hỏi trước khi cài đặt hay thêm dependency.
   2. Khảo sát DOM/code của trang liên quan để chọn locator.
   3. Viết Page Object và spec, mỗi test gắn TC ID trong tiêu đề (`TC-LOGIN-001: ...`).
   4. Chạy test, thu output thật. Fail → xác định là lỗi test (locator, dữ liệu, chờ) hay lỗi sản phẩm; chỉ lỗi sản phẩm mới chuyển sang Pha 4. Sửa lỗi test tối đa vài vòng hợp lý, đừng "vá" để pass bằng cách nới assertion.
4. **Auto (API)** → dùng công cụ API test đã có trong repo (hoặc hỏi). Cùng quy tắc: output thật, dữ liệu độc lập.
5. **Ghi `qa-artifacts/03-execution-notes.md`** gồm: thông tin lần chạy (build/commit và môi trường nếu biết, nếu không `[Cần bổ sung]`), bảng kết quả từng TC, lệnh chạy, output thô, phát hiện thăm dò, case Blocked.
6. **Trình bày:** số case Pass/Fail/Blocked/Not Run đếm từ bảng thật, danh sách lỗi sản phẩm nghi ngờ, và câu hỏi tiếp theo (chuyển Pha 4 ghi defect?).

## Phân loại lỗi test vs lỗi sản phẩm

| Dấu hiệu | Khả năng |
|---|---|
| Locator không tìm thấy nhưng UI hiển thị đúng khi xem tay | Lỗi test (locator/chờ) |
| Chạy riêng pass, chạy chung fail | Test phụ thuộc dữ liệu/thứ tự → sửa test |
| Kết quả thực tế khác Expected Result trong matrix, tái hiện được bằng tay | Lỗi sản phẩm → Pha 4 |
| Expected Result trong matrix mâu thuẫn đặc tả/code | Lỗi test case → hỏi người dùng, cập nhật matrix |
| Lúc pass lúc fail không rõ lý do | Flaky — điều tra, không tự đánh dấu Pass |

## Khối Cố vấn QA (cuối phản hồi)

Giải thích ngắn vì sao các case P0 được chạy trước; góc khuất chưa phủ (phân quyền, rớt mạng, bấm đúp, dữ liệu biên); phương án mặc định (ví dụ "chạy P0→P1 trước, P2/P3 nếu còn thời gian").

## Ví dụ minh hoạ

Xem `references/worked-example.md` để biết định dạng đầu ra mẫu (dữ liệu hư cấu, chỉ đọc khi cần; không sao chép số liệu của ví dụ vào dự án thật).

## Checklist hoàn thành

- [ ] Mọi case trong matrix có trạng thái thật (hoặc `Not Run`/`Blocked` kèm lý do)
- [ ] Locator dựa trên DOM/code đã đọc; không CSS/XPath giòn, không `waitForTimeout`
- [ ] Test độc lập dữ liệu, tiêu đề có TC ID
- [ ] Output chạy test là output thật
- [ ] `03-execution-notes.md` đã cập nhật; lỗi sản phẩm được chuyển sang Pha 4
