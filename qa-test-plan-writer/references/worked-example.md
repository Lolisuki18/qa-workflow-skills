# Ví dụ chạy thật — qa-test-plan-writer

> ⚠️ Dữ liệu **hư cấu** ("DemoShop", tính năng Đăng nhập) để minh hoạ định dạng. Không dùng làm số liệu thật.

**Đầu vào (tóm tắt đặc tả giả định):**
- REQ-01: Đăng nhập đúng email + mật khẩu thì chuyển tới `/dashboard`.
- REQ-02: Sai mật khẩu hoặc để trống thì hiện thông báo lỗi, ở lại trang đăng nhập.
- REQ-03: Sai liên tiếp 5 lần thì khoá tài khoản 15 phút.
- REQ-04: Chỉ vai trò Admin vào được `/admin`.

## Requirement Audit

| # | Yêu cầu | Vấn đề | Loại | Câu hỏi làm rõ | Mặc định đề xuất |
|---|---|---|---|---|---|
| 1 | REQ-03 | Không nói bộ đếm sai reset khi nào (đăng nhập đúng? sau 15 phút?) | Mơ hồ | Khi nào reset bộ đếm? | Reset khi đăng nhập thành công hoặc hết 15 phút |
| 2 | REQ-04 | Không nêu hành vi khi bị từ chối (chuyển trang / 403 / 404) | Thiếu luồng lỗi | Hiển thị gì khi user thường vào `/admin`? | Chuyển về `/dashboard` kèm thông báo; API trả 403 |
| 3 | REQ-02 | Thông báo lỗi chung hay tách "sai email" / "sai mật khẩu"? | Mơ hồ | Chọn một | Chung một thông báo (tránh lộ email tồn tại) |
| 4 | REQ-01 | Không nói phiên đăng nhập sống bao lâu | Thiếu phi chức năng | Thời gian hết phiên? | [Cần bổ sung: thời gian phiên] |

## Scope
- In-scope: REQ-01…REQ-04, trình duyệt desktop, vai trò Khách / User / Admin.
- Out-of-scope: quên mật khẩu (không có yêu cầu), đăng nhập mạng xã hội (chưa phát triển).

## Risk Analysis
| Khu vực | Khả năng | Tác động | Ưu tiên test |
|---|---|---|---|
| Phân quyền /admin | M | H | Cao |
| Khoá tài khoản | M | M | Trung bình |
| Đăng nhập chính | L | H | Cao |

## Chiến lược
| Khu vực | Manual | Auto (browser) | Auto (API) | Lý do |
|---|---|---|---|---|
| Đăng nhập chính, phân quyền UI | | ✔ | | Luồng cốt lõi, lặp lại mỗi release |
| Khoá tài khoản | | | ✔ | Cần nhiều lần gọi nhanh, kiểm bộ đếm |
| Bấm đúp, rớt mạng | ✔ | | | Khó tự động hoá ổn định |

## Môi trường & dữ liệu
- Môi trường / build: [Cần bổ sung: URL và build]
- Browser: [Cần bổ sung: browser và phiên bản]
- Tài khoản: 1 user thường, 1 admin, 1 tài khoản dành riêng cho test khoá.

## Entry / Exit (đề xuất — cần xác nhận)
- Entry: build chạy được trên môi trường test, smoke test pass.
- Exit: 100% case P0 pass, không còn Blocker/Critical mở, RTM phủ 100% yêu cầu in-scope.

**Điểm cần học:** mọi câu hỏi có mặc định; thông tin chưa biết dùng `[Cần bổ sung: ...]`; không điền "Chrome 120" cho môi trường.
