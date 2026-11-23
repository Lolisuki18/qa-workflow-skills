# Ví dụ chạy thật — qa-defect-writer

> ⚠️ Dữ liệu **hư cấu** ("DemoShop") để minh hoạ định dạng.

**Mô tả thô của người dùng:** "user thường gõ /admin vẫn vào được trang quản trị, chắc lỗi phân quyền."

## Câu hỏi gom lại (không hỏi lắt nhắt)

1. Môi trường/build và browser đã gặp lỗi? 2. Thử mấy lần, mấy lần lặp lại? 3. Có ảnh/log không?

Người dùng trả lời: "thử 3 lần, lần nào cũng vậy; có ảnh; môi trường staging, build chưa nhớ."

## Defect Report

```markdown
### DEF-001 — [Authz] User thường truy cập được trang /admin khi gõ trực tiếp URL
| Trường | Nội dung |
|---|---|
| TC liên quan | TC-LOGIN-006 |
| Environment | Staging; build [Cần bổ sung]; browser [Cần bổ sung] |
| Severity / Priority | Critical / P0 (đề xuất) |
| Lý do | Vượt quyền truy cập khu quản trị, không có workaround; cần PO xác nhận Priority |
| Status | New |
| Reproducibility | Always (3/3) |
| Pre-conditions | Đã đăng nhập bằng tài khoản vai trò User |
| Steps to Reproduce | 1. Đăng nhập bằng user thường 2. Gõ thẳng `/admin` vào thanh địa chỉ |
| Actual Result | Hiển thị trang quản trị |
| Expected Result | Bị chuyển về `/dashboard` kèm thông báo (nguồn: REQ-04, mặc định Pha 1) |
| Evidence | Screenshot do người dùng cung cấp; log: Chưa có |
| Ghi chú / Giả thuyết (chưa xác nhận) | Có thể mới chặn ở UI chứ chưa chặn ở server — cần dev kiểm tra, QA chưa xác minh |
```

## Re-test & Regression sau khi dev báo "đã sửa"

```markdown
Build chứa bản sửa: [Cần bổ sung]
1. Re-test lỗi gốc: chạy lại Steps của DEF-001 bằng user thường; thêm biến thể: gọi trực tiếp API quản trị bằng token của user thường.
2. Regression liên quan (theo RTM cùng REQ-04): TC-LOGIN-009 (Admin vẫn vào được), TC-LOGIN-001.
3. Đã từng lỗi cùng module: [Chưa có defect Closed nào]
Chạy lại bằng Playwright: TC-LOGIN-006, 009. Manual: biến thể gọi API.
```

Chỉ khi người dùng báo kết quả thật mới đổi Status sang `Closed` (hoặc `Reopened`) và ghi vào "Lịch sử Re-test".

**Điểm cần học:** Severity tách Priority và có lý do; môi trường thiếu thì `[Cần bổ sung]`; giả thuyết tách riêng, nói rõ chưa xác nhận.
