# Ví dụ chạy thật — qa-test-matrix-writer

> ⚠️ Dữ liệu **hư cấu** ("DemoShop", tính năng Đăng nhập) để minh hoạ định dạng. Giả định người dùng đã chấp nhận các mặc định của Pha 1.

## Test cases

| TC ID | Req/UC ID | Module | Title | Pre-condition | Test Steps | Test Data | Expected Result | Priority | Execution Type |
|---|---|---|---|---|---|---|---|---|---|
| TC-LOGIN-001 | REQ-01 | Login | Đăng nhập đúng chuyển tới dashboard | User `user_a@example.test` tồn tại, chưa khoá | 1. Mở /login 2. Nhập email, mật khẩu 3. Bấm Đăng nhập | email `user_a@example.test`; mật khẩu hợp lệ | Chuyển tới `/dashboard` | P0 | Auto (browser) |
| TC-LOGIN-002 | REQ-02 | Login | Sai mật khẩu hiện lỗi, ở lại trang | Như trên | 1. Mở /login 2. Nhập email đúng, mật khẩu sai 3. Bấm Đăng nhập | mật khẩu `wrong-pass-1` | Hiện thông báo lỗi `[Cần bổ sung: thông báo chính xác]`; URL vẫn `/login` | P0 | Auto (browser) |
| TC-LOGIN-003 | REQ-02 | Login | Để trống email bị chặn | Mở /login | 1. Để trống email 2. Nhập mật khẩu 3. Bấm Đăng nhập | email rỗng | Không gửi đăng nhập; báo email bắt buộc | P1 | Auto (browser) |
| TC-LOGIN-004 | REQ-03 | Lockout | Sai lần thứ 5 khoá tài khoản | Tài khoản `lock_test@example.test` sai 0 lần | 1. Gửi đăng nhập sai 5 lần liên tiếp 2. Gửi lần 6 với mật khẩu đúng | mật khẩu sai x5, rồi đúng | Lần 6 bị từ chối vì khoá | P1 | Auto (API) |
| TC-LOGIN-005 | REQ-03 | Lockout | Sai 4 lần rồi đúng vẫn vào được (biên) | Tài khoản sai 0 lần | 1. Sai 4 lần 2. Đăng nhập đúng | mật khẩu sai x4, rồi đúng | Đăng nhập thành công | P1 | Auto (API) |
| TC-LOGIN-006 | REQ-04 | Authz | User thường bị chặn vào /admin | Đã đăng nhập bằng user thường | 1. Gõ thẳng URL /admin | vai trò User | Bị chuyển về `/dashboard` kèm thông báo (mặc định đề xuất) | P0 | Auto (browser) |
| TC-LOGIN-007 | REQ-01 | Login | Bấm đúp nút Đăng nhập không tạo lỗi/phiên trùng | Mở /login, nhập đúng thông tin | 1. Bấm đúp nhanh nút Đăng nhập | — | Vào dashboard một lần, không báo lỗi | P2 | Manual |
| TC-LOGIN-008 | REQ-01 | Login | Mất mạng giữa lúc đăng nhập | Mở /login, nhập đúng thông tin | 1. Tắt mạng 2. Bấm Đăng nhập 3. Bật mạng | — | Thông báo lỗi mạng rõ ràng, không treo | P2 | Manual |
| TC-LOGIN-009 | REQ-04 | Authz | Admin vào được /admin | Đã đăng nhập bằng admin | 1. Mở /admin | vai trò Admin | Hiển thị trang quản trị | P0 | Auto (browser) |

Tóm tắt: **9 case** — P0: 4, P1: 3, P2: 2, P3: 0 · Manual: 2, Auto (browser): 5, Auto (API): 2.

## RTM

| Req/UC ID | Mô tả | Happy path | Negative | Permission | Phủ |
|---|---|---|---|---|---|
| REQ-01 | Đăng nhập đúng | TC-LOGIN-001 | TC-LOGIN-007, 008 | N/A (chưa đăng nhập) | Đủ |
| REQ-02 | Báo lỗi khi sai/trống | N/A (yêu cầu mô tả lỗi) | TC-LOGIN-002, 003 | N/A | Đủ |
| REQ-03 | Khoá sau 5 lần sai | TC-LOGIN-005 | TC-LOGIN-004 | N/A | Đủ |
| REQ-04 | Chỉ Admin vào /admin | TC-LOGIN-009 | — | TC-LOGIN-006 | Đủ |

Phủ: 4/4 yêu cầu = 100%. Case mồ côi: không có.

**Điểm cần học:** Test Data cụ thể; thông báo chưa biết giữ `[Cần bổ sung]`; có case biên (4 vs 5 lần sai) và permission; RTM tính % từ bảng thật.
