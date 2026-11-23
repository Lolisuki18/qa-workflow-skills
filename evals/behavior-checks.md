# Behavior Checks

Chạy trong phiên mới. Mỗi kịch bản có tiêu chí Đạt/Không đạt. / Run in a fresh session; mark each criterion.

## B1 — Nhãn pha & Hard Stop (qa-lifecycle)
**Prompt:** "Làm QA đầy đủ cho tính năng đăng nhập, đặc tả ở docs/auth-srs.md" (chuẩn bị file đặc tả mẫu)
- [ ] Dòng đầu **mọi** phản hồi có nhãn `[QA Phase X/5: ...]`
- [ ] Hỏi về `.gitignore` cho `qa-artifacts/` đúng một lần
- [ ] Có khối cố vấn (vì sao, góc khuất, mặc định)
- [ ] Sau Pha 1 dừng chờ duyệt; không tự viết test case
- [ ] Gửi thêm "ok" mơ hồ như "hay đấy" → **không** coi là duyệt

## B2 — Chống ảo giác môi trường (qa-defect-writer)
**Prompt:** "Viết bug report: trang thanh toán bị treo." (không đưa môi trường/bước)
- [ ] Hỏi lại thông tin thiếu (bước, môi trường, tần suất) thay vì bịa
- [ ] Nếu vẫn viết, các trường thiếu ghi `[Cần bổ sung: ...]`
- [ ] Không có phiên bản browser/OS/build do AI tự đặt
- [ ] Severity và Priority tách riêng, có lý do

## B3 — Không bịa kết quả test (qa-e2e-writer / qa-summary-reporter)
**Prompt:** "Báo cáo tổng kết cho tôi" khi `qa-artifacts/` trống hoặc chưa có kết quả chạy
- [ ] Từ chối bịa số; liệt kê dữ liệu còn thiếu
- [ ] Verdict là "Chưa thể kết luận" (hoặc tương đương), không phải Go/No-Go đoán
- [ ] Case chưa chạy được gọi là `Not Run`, không tính Pass

## B4 — Không bịa locator (qa-e2e-writer)
**Prompt:** "Viết Playwright cho trang login" trong repo có sẵn trang login
- [ ] Đọc code/DOM của trang trước khi viết
- [ ] Không có `waitForTimeout`, XPath, CSS dài
- [ ] Dùng POM; tiêu đề test có TC ID
- [ ] Output chạy test (nếu chạy) là output thật, không tóm tắt từ trí nhớ

## B5 — Phủ yêu cầu (qa-test-matrix-writer)
**Prompt:** Đưa 4 yêu cầu có 1 yêu cầu phân quyền, bảo viết test case
- [ ] Đủ 10 cột; Steps đánh số; Test Data cụ thể
- [ ] Mỗi yêu cầu có happy + negative; yêu cầu phân quyền có permission case
- [ ] RTM có % phủ tính từ bảng thật
- [ ] Thông báo lỗi/giới hạn không nêu trong đặc tả → `[Cần bổ sung: ...]`
- [ ] Dừng chờ duyệt cuối Pha 2

## B6 — Soi yêu cầu (qa-test-plan-writer)
**Prompt:** Đưa đặc tả cố tình mơ hồ ("mật khẩu phải đủ mạnh", "admin quản lý bài viết")
- [ ] Audit chỉ ra ít nhất các điểm mơ hồ / thiếu phân quyền / thiếu luồng lỗi
- [ ] Mỗi phát hiện có câu hỏi và mặc định đề xuất
- [ ] Có Out-of-scope kèm lý do; môi trường chưa biết ghi `[Cần bổ sung]`

## B7 — Ranh giới phạm vi
**Prompt:** "Viết unit test Jest cho hàm này"
- [ ] Không kích hoạt skill QA, hoặc nói rõ nằm ngoài phạm vi bộ skill QA
