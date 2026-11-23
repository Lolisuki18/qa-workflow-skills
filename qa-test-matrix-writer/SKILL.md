---
name: qa-test-matrix-writer
description: Designs a complete test case table (TC ID, Req/UC ID, Module, Title, Pre-condition, Steps, Test Data, Expected Result, Priority P0-P3, Execution Type) using test design techniques, plus a Requirement Traceability Matrix (RTM) proving every requirement has happy-path, negative and permission coverage, exportable as Markdown or clean CSV for Excel, Google Sheets or TestRail. Use when the user says 'write test cases', 'test matrix', 'traceability matrix', 'RTM', 'test case table', 'boundary value analysis', 'cover all requirements', 'viết test case', 'thiết kế test case', 'bảng test case', 'ma trận truy vết yêu cầu', 'xuất test case ra CSV/Excel', 'import TestRail'. Do NOT use for the test plan or requirement audit (use qa-test-plan-writer), writing Playwright code or manual run scripts (use qa-e2e-writer), logging defects (use qa-defect-writer), summary reports (use qa-summary-reporter), or developer unit tests (use test-case-writer).
---

# QA Test Matrix Writer — Bước 2: Thiết kế Test Case

Sinh bảng test case có hệ thống và RTM chứng minh phủ yêu cầu. Khi chạy trong `qa-lifecycle`, đây là Pha 2/5, kết thúc bằng Hard Stop (nhãn `[QA Phase 2/5: Test Matrix]` ở dòng đầu).

## Quy tắc

- **Đọc trước:** `references/test-design-techniques.md` (6 kỹ thuật). Áp dụng kỹ thuật phù hợp từng yêu cầu thay vì viết case theo cảm tính.
- **Đầu vào:** `qa-artifacts/01-test-plan.md` đã duyệt (ID yêu cầu, scope, rủi ro, chiến lược). Chưa có plan → cảnh báo, đề xuất chạy `qa-test-plan-writer` trước; nếu người dùng vẫn muốn đi tiếp, lập danh sách yêu cầu + ID tối thiểu và ghi chú rủi ro.
- **Chống ảo giác:** không bịa quy tắc nghiệp vụ, giới hạn, thông báo lỗi, tên field. Nếu đặc tả không nêu giá trị biên/thông báo chính xác → Expected Result ghi mô tả hành vi + `[Cần bổ sung: thông báo lỗi chính xác]`. Dữ liệu test dùng giá trị minh hoạ rõ ràng (ví dụ `user_a@example.test`), không dùng dữ liệu cá nhân thật.
- Nếu đang test codebase có sẵn: đối chiếu validate/phân quyền thực tế trong code để Expected Result đúng, nhưng nếu code mâu thuẫn đặc tả → ghi vào mục "Mâu thuẫn" và hỏi, không tự chọn.
- Mỗi test case **kiểm một ý chính**, độc lập, chạy được không phụ thuộc case khác.

## Quy trình

1. **Nạp yêu cầu:** liệt kê mọi Req/UC ID in-scope từ test plan.
2. **Chọn kỹ thuật** cho từng yêu cầu (bảng gợi ý ở file reference), tối thiểu: có happy path, ≥ 1 negative, và nếu có phân quyền thì ≥ 1 permission case.
3. **Sinh test case** theo cột chuẩn (bên dưới). Gom theo Module, đánh `TC ID` ổn định: `TC-<MODULE>-<số 3 chữ số>` (ví dụ `TC-LOGIN-001`).
4. **Gán Priority** từ Risk Analysis của plan (xem bảng dưới).
5. **Gán Execution Type** theo chiến lược của plan; nếu plan không nói, dùng gợi ý ở mục dưới và đánh dấu "đề xuất".
6. **Dựng RTM** và tự kiểm: yêu cầu nào thiếu cột Negative/Permission thì hoặc bổ sung case hoặc ghi lý do "không áp dụng".
7. **Lưu & trình bày** (mục cuối).

## Các cột bắt buộc

| Cột | Quy tắc |
|---|---|
| `TC ID` | Duy nhất, ổn định, không đánh lại số khi xoá case |
| `Req/UC ID` | ≥ 1 ID; case không truy được về yêu cầu → hỏi lại hoặc gắn `[Cần bổ sung: yêu cầu nguồn]` |
| `Module` | Khớp với module trong plan |
| `Title` | Động từ + điều kiện + kết quả mong đợi, ngắn gọn |
| `Pre-condition` | Trạng thái hệ thống/tài khoản/dữ liệu cần có trước khi chạy |
| `Test Steps` | Đánh số 1., 2., 3.; mỗi bước một hành động; người chưa biết hệ thống vẫn làm theo được |
| `Test Data` | Giá trị cụ thể cho từng input (kể cả giá trị biên); không để "dữ liệu hợp lệ" chung chung |
| `Expected Result` | Quan sát được, kiểm chứng được (hiển thị gì, lưu gì, mã trạng thái gì); không viết "hoạt động đúng" |
| `Priority` | `P0`–`P3` |
| `Execution Type` | `Manual` / `Auto (browser)` / `Auto (API)` |

## Priority P0–P3

| Mức | Ý nghĩa | Ví dụ |
|---|---|---|
| P0 | Nếu hỏng thì không thể release; luồng cốt lõi, tiền, bảo mật, mất dữ liệu | Đăng nhập, thanh toán, user A xem được dữ liệu user B |
| P1 | Chức năng chính, rủi ro cao | CRUD chính, validate quan trọng, chuyển trạng thái nghiệp vụ |
| P2 | Chức năng phụ, rủi ro vừa | Lọc/sắp xếp, thông báo lỗi chi tiết, biên ít gặp |
| P3 | Trình bày, tiện ích, rủi ro thấp | Căn lề, văn bản gợi ý, thứ tự hiển thị |

Cách suy ra: Rủi ro H×H → P0; H×M hoặc M×H → P1; M×M hoặc L×H → P2; còn lại P3. Dữ liệu rủi ro lấy từ `01-test-plan.md`; nếu người dùng điều chỉnh, theo người dùng.

## Gợi ý Execution Type (khi plan chưa chỉ định)

- `Auto (browser)`: luồng người dùng chính ổn định, cần regression lặp lại.
- `Auto (API)`: validate/nghiệp vụ/phân quyền tầng API, nhiều tổ hợp dữ liệu.
- `Manual`: UX, giao diện, tính năng chưa ổn định, thăm dò, case tốn công tự động hoá (CAPTCHA, email thật, thiết bị phần cứng).

## RTM — Requirement Traceability Matrix

Đối chiếu 1–1 từng yêu cầu với test case:

| Req/UC ID | Mô tả yêu cầu | Happy path (TC) | Negative (TC) | Permission (TC) | Phủ |
|---|---|---|---|---|---|
| REQ-01 | ... | TC-X-001 | TC-X-002, TC-X-003 | TC-X-004 | Đủ |
| REQ-02 | ... | TC-Y-001 | — | N/A (không có phân quyền) | Thiếu Negative |

Quy tắc:
- Cột Phủ: `Đủ` / `Thiếu <loại>` / `Chưa có`. Mục "N/A" phải có lý do.
- Cuối RTM in: tổng yêu cầu, số yêu cầu `Đủ`, % phủ = Đủ / tổng. Chỉ tính từ bảng thật vừa dựng.
- Chiều ngược: liệt kê case "mồ côi" (không map về yêu cầu nào) để người dùng quyết định giữ/bỏ.

## Định dạng đầu ra

Mặc định: bảng Markdown trong `qa-artifacts/02-test-matrix.md` (cấu trúc ở `qa-lifecycle/references/phase-templates.md`). Nếu người dùng muốn CSV (hoặc import TestRail/Excel/Sheets):

- Ghi `qa-artifacts/02-test-matrix.csv`, mã hoá UTF-8 **có BOM** để Excel đọc đúng tiếng Việt, dấu phân cách `,`.
- Hàng tiêu đề đúng 10 cột ở trên, một hàng/test case, không gộp ô.
- Ô chứa dấu phẩy, nháy kép hoặc xuống dòng phải bọc trong `"..."`, nháy kép trong ô nhân đôi `""`.
- Nhiều bước trong một ô: ngăn bằng ký tự xuống dòng thật trong ô đã bọc nháy, hoặc ` | ` nếu người dùng muốn một dòng; hỏi nếu không rõ.
- Hỏi nếu cần cột phụ cho TestRail (Section, Type, Estimate) — không tự thêm.
- Sau khi ghi, đọc lại để kiểm số cột mỗi hàng đều bằng nhau.

## Trình bày & Hard Stop

1. Tóm tắt: tổng số case; phân bố theo Priority và Execution Type (đếm từ bảng thật); % phủ RTM; yêu cầu thiếu loại case nào.
2. Mâu thuẫn/điểm cần làm rõ phát sinh khi thiết kế, kèm mặc định đề xuất.
3. Khối **Cố vấn QA**: vì sao cần các nhóm case này, góc khuất (phân quyền, rớt mạng, bấm đúp, dữ liệu biên) đã/chưa phủ, mặc định sẽ chọn.
4. **HARD STOP:** chờ duyệt. Không sang chạy test (Pha 3) khi chưa duyệt.

## Checklist hoàn thành

- [ ] Đã đọc `references/test-design-techniques.md` và dùng kỹ thuật phù hợp
- [ ] Đủ 10 cột; Steps đánh số; Test Data cụ thể; Expected Result kiểm chứng được
- [ ] Mỗi yêu cầu có happy + negative (+ permission nếu liên quan) hoặc có lý do N/A
- [ ] RTM tính % từ dữ liệu thật; có danh sách case mồ côi (nếu có)
- [ ] Không bịa thông báo lỗi/giá trị giới hạn; chỗ thiếu có `[Cần bổ sung: ...]`
- [ ] Đã lưu file và dừng chờ duyệt
