---
name: qa-defect-writer
description: Turns raw bug descriptions, logs and screenshots into standardized Defect Reports (title, environment, severity vs priority, pre-conditions, steps to reproduce, actual vs expected, evidence), logs them in qa-artifacts/04-defects.md, and runs Re-test and Regression Checklist mode when developers report a fix. Use when the user says 'write a bug report', 'log this defect', 'report this bug', 'severity or priority?', 're-test the fix', 'regression checklist', 'viết bug report', 'ghi nhận lỗi', 'báo lỗi chuẩn', 'tạo defect', 'đánh giá mức độ nghiêm trọng', 'kiểm tra lại sau khi dev sửa', 'regression sau khi fix'. Do NOT use for finding the root cause or fixing the code, designing test cases (use qa-test-matrix-writer), running tests (use qa-e2e-writer), summary reports (use qa-summary-reporter), or code review.
---

# QA Defect Writer — Bước 4: Quản lý lỗi

Chuẩn hoá lỗi thành báo cáo dev có thể tái hiện ngay, và theo dõi vòng đời tới khi đóng. Khi chạy trong `qa-lifecycle`, đây là Pha 4/5 (nhãn `[QA Phase 4/5: Defects]` ở dòng đầu).

## Quy tắc

- **Đọc trước:** `references/severity-priority-matrix.md` để chấm Severity và Priority.
- **Chống ảo giác tuyệt đối:** chỉ ghi điều người dùng/log/kết quả test thật cho thấy.
  - Không bịa môi trường, phiên bản browser/OS/build, bước tái hiện, tần suất, thông báo lỗi.
  - Thiếu → `[Cần bổ sung: ...]` và hỏi lại (gom thành một danh sách câu hỏi ngắn, không hỏi lắt nhắt).
  - Không suy đoán nguyên nhân gốc như thể chắc chắn. Có giả thuyết thì đặt ở mục "Ghi chú/Giả thuyết (chưa xác nhận)". Tìm và sửa nguyên nhân là việc của dev.
- **Mỗi defect một vấn đề.** Gộp nhiều triệu chứng cùng một gốc thì ghi chú liên kết; tách khi có hai hiện tượng độc lập.
- Kiểm tra trùng: so với `04-defects.md` hiện có trước khi tạo mới; nghi trùng → hỏi.
- Giữ giọng trung tính, mô tả sự kiện, không đổ lỗi.

## Chế độ 1 — Tạo Defect Report

### Quy trình
1. **Thu thập:** mô tả thô, log, ảnh/video, TC liên quan (`Defect ID` ↔ `TC ID`), thông tin môi trường.
2. **Chuẩn hoá các bước tái hiện:** đánh số, mỗi bước một hành động, kèm dữ liệu cụ thể. Người chưa biết hệ thống vẫn làm theo được. Nếu mô tả thô thiếu bước → hỏi, đừng tự lấp.
3. **Phân biệt Actual vs Expected:** Expected lấy từ đặc tả/Expected Result của TC (nêu nguồn); không có nguồn → `[Cần bổ sung: nguồn Expected]`.
4. **Chấm Severity** (tác động kỹ thuật) và **Priority** (độ gấp nghiệp vụ) **riêng biệt** theo matrix, nêu lý do một dòng. Priority là đề xuất — người dùng/PO quyết định cuối.
5. **Evidence:** liệt kê file/đường dẫn log/ảnh thật; trích dòng log liên quan (nguyên văn, không sửa). Không có → ghi "Chưa có".
6. **Ghi vào `qa-artifacts/04-defects.md`** (đầu file: bảng tổng hợp `Defect ID | Title | Severity | Priority | Status | TC liên quan`; tiếp theo là mục chi tiết theo mẫu dưới; cuối file: bảng "Lịch sử Re-test" `Defect ID | Vòng | Build | Kết quả | Regression đã kiểm`). Tiếp số Defect ID (`DEF-001`, `DEF-002`...), không đánh lại.

### Mẫu Defect Report

```markdown
### DEF-001 — [Module] Hiện tượng + Điều kiện
| Trường | Nội dung |
|---|---|
| Title | [Checkout] Tổng tiền không cập nhật khi đổi số lượng sau khi áp mã giảm giá |
| TC liên quan | TC-CART-012 |
| Environment | [Cần bổ sung: URL/build, OS, browser + phiên bản, vai trò] |
| Severity / Priority | Major / P1 — <lý do một dòng> |
| Status | New |
| Reproducibility | [x/y lần thử] hoặc [Cần bổ sung] |
| Pre-conditions | ... |
| Steps to Reproduce | 1. ... 2. ... 3. ... |
| Actual Result | ... |
| Expected Result | ... (nguồn: REQ-xx / TC-xx) |
| Evidence | log: ..., screenshot: ... |
| Ghi chú / Giả thuyết (chưa xác nhận) | ... |
```

**Title:** `[Module] Hiện tượng + Điều kiện` — nêu cái gì sai và khi nào. Tốt: `[Login] Báo "Lỗi hệ thống" khi email chứa chữ hoa`. Tránh: `Login bị lỗi`, `Không chạy`.

## Chế độ 2 — Re-test & Regression Checklist

Kích hoạt khi dev báo đã sửa (hoặc người dùng nói "đã fix DEF-xxx").

1. Đọc defect gốc trong `04-defects.md`. Hỏi build/commit chứa bản sửa nếu chưa biết (`[Cần bổ sung]`).
2. Xuất checklist gồm 3 nhóm:
   - **Re-test lỗi gốc:** chạy đúng Steps to Reproduce gốc, đúng môi trường/dữ liệu; kết quả mong đợi = Expected Result gốc. Thử thêm biến thể gần (dữ liệu biên khác, vai trò khác) nếu liên quan.
   - **Regression liên quan:** các luồng dùng chung module/hàm/API/dữ liệu với phần vừa sửa. Dựa vào RTM (`02-test-matrix.md`) để chọn TC cùng Req/Module, ưu tiên P0/P1; nếu biết diff/commit thì đọc thay đổi để suy ra vùng ảnh hưởng, nêu rõ cơ sở suy luận.
   - **Đã từng lỗi:** các defect cũ cùng module đã Closed — kiểm tra không tái phát.
3. Nêu rõ case nào chạy `Manual`, case nào chạy lại Playwright (`qa-e2e-writer`).
4. Sau khi người dùng báo kết quả: cập nhật Status theo vòng đời, thêm dòng vào "Lịch sử Re-test" (vòng, build, kết quả, regression đã kiểm). Không đóng defect khi chưa có kết quả thật.

### Vòng đời trạng thái
`New → Open (đã xác nhận) → Fixed (dev báo) → Re-test → Closed` · nhánh: `Reopened` (re-test fail), `Won't Fix` / `Duplicate` / `Cannot Reproduce` (cần lý do và người quyết định). Không bỏ qua bước; không tự chuyển `Closed`.

## Khối Cố vấn QA

Giải thích vì sao tách Severity/Priority; cảnh báo lỗi dễ bị đánh giá thấp (phân quyền, mất dữ liệu, lỗi chỉ xảy ra khi bấm đúp/rớt mạng); nêu mặc định (ví dụ "tôi xếp Major/P1, bạn có thể nâng nếu lỗi chặn demo").

## Ví dụ minh hoạ

Xem `references/worked-example.md` để biết định dạng đầu ra mẫu (dữ liệu hư cấu, chỉ đọc khi cần; không sao chép số liệu của ví dụ vào dự án thật).

## Checklist hoàn thành

- [ ] Title theo mẫu `[Module] Hiện tượng + Điều kiện`
- [ ] Steps đánh số, tái hiện được; Actual ≠ Expected rõ ràng
- [ ] Severity và Priority tách riêng, có lý do
- [ ] Không có môi trường/bước/tần suất bịa; chỗ thiếu có `[Cần bổ sung: ...]`
- [ ] Evidence là tài liệu thật hoặc "Chưa có"
- [ ] Đã ghi `04-defects.md`, kiểm tra trùng
- [ ] Re-test: có 3 nhóm checklist và cập nhật lịch sử theo kết quả thật
