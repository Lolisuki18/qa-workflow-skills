# Ví dụ chạy thật — qa-lifecycle

> ⚠️ Dữ liệu **hư cấu** để minh hoạ định dạng (ứng dụng giả định "DemoShop", tính năng Đăng nhập). Không dùng làm số liệu thật. Cùng kịch bản này xuyên suốt ví dụ của cả 6 skill.

## Lượt 1 — Khởi động

**Người dùng:** "Làm QA bài bản cho tính năng đăng nhập của DemoShop giúp tôi. Đặc tả nằm ở `docs/auth-srs.md`."

**Phản hồi mẫu:**

```markdown
[QA Phase 0/5: Khởi động]

Tôi đã đọc `docs/auth-srs.md`. Phạm vi tôi hiểu: đăng nhập email + mật khẩu, khoá tài khoản sau nhiều lần sai, và phân quyền trang /admin. Chưa có yêu cầu về "quên mật khẩu" nên tôi sẽ để ngoài phạm vi trừ khi bạn bảo khác.

Hai câu hỏi nhanh:
1. Thư mục `qa-artifacts/` nên (a) thêm vào `.gitignore` hay (b) giữ lại trong repo? — Mặc định tôi chọn (b) nếu bạn cần chia sẻ báo cáo cho team.
2. Môi trường test sẽ chạy ở đâu (URL/build)? — [Cần bổ sung: môi trường test]

> **Cố vấn QA**
> - *Vì sao quan trọng:* đăng nhập là cửa vào của mọi tính năng; lỗi ở đây chặn toàn bộ người dùng.
> - *Góc khuất:* khoá tài khoản (đếm sai thế nào, mở khoá khi nào), user thường vào được /admin, bấm đúp nút đăng nhập.
> - *Mặc định:* tôi chọn giữ `qa-artifacts/` trong repo và tiếp tục Pha 1 ngay khi bạn trả lời.
```

## Lượt 2 — Kết thúc Pha 1 (Hard Stop)

```markdown
[QA Phase 1/5: Test Plan]

Đã lưu `qa-artifacts/01-test-plan.md` (Draft). Top phát hiện: REQ-03 chưa nói bộ đếm sai được reset khi nào; REQ-04 không nói hành vi khi bị từ chối (chuyển trang hay báo 403).

**⏸ HARD STOP — chờ duyệt**
Vui lòng trả lời 2 câu hỏi mở (hoặc chấp nhận mặc định đã nêu) rồi nhắn "duyệt" để sang Pha 2.
```

**Điểm cần học từ ví dụ:** nhãn pha ở dòng đầu; hỏi `.gitignore` đúng một lần; khối Cố vấn có mặc định; dừng hẳn, không tự sang Pha 2.
