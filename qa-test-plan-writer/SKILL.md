---
name: qa-test-plan-writer
description: Audits requirements for ambiguity, missing error flows, missing permission rules and business contradictions, then drafts a Test Plan with scope, risk analysis, test strategy split (Manual / Auto browser / Auto API), test environment and data needs, and entry/exit criteria. Use when the user says 'write a test plan', 'review these requirements for testability', 'find gaps in the spec', 'test strategy', 'what should we test', 'viết test plan', 'lập kế hoạch kiểm thử', 'soi yêu cầu', 'phân tích đặc tả trước khi test', 'rà soát SRS', 'chiến lược test'. Do NOT use for writing individual test cases or RTM (use qa-test-matrix-writer), writing Playwright or manual test scripts (use qa-e2e-writer), logging bugs (use qa-defect-writer), final reports (use qa-summary-reporter), development implementation plans (use feature-plan-writer), or developer unit tests.
---

# QA Test Plan Writer — Bước 1: Soi yêu cầu & Chiến lược

Biến đặc tả thô thành Test Plan có thể duyệt, **và** chỉ ra những chỗ đặc tả chưa đủ để test. Khi chạy trong `qa-lifecycle`, đây là Pha 1/5 và kết thúc bằng Hard Stop (nhãn `[QA Phase 1/5: Test Plan]` ở dòng đầu).

## Quy tắc

- Chỉ dựa trên đầu vào thật (SRS, Use Case, ticket, codebase). Không bịa yêu cầu, endpoint, vai trò, môi trường. Thiếu → `[Cần bổ sung: ...]` hoặc đưa vào câu hỏi mở kèm mặc định đề xuất.
- Suy luận từ code/UI mà không có đặc tả → gắn `[Suy luận từ code — cần xác nhận]`.
- Giải thích bằng ngôn ngữ developer; mỗi phát hiện kèm lý do "vì sao dễ sinh bug".
- Chỉ viết kế hoạch, không viết test case chi tiết (việc của `qa-test-matrix-writer`).

## Quy trình

### Bước 1 — Thu thập đầu vào
1. Xác định nguồn yêu cầu; đọc hết. Nếu là codebase: xem routes/controllers/models/UI chính, file cấu hình phân quyền, validate rules, README/docs, test hiện có (để biết framework test đã dùng).
2. Gán **ID cho từng yêu cầu** nếu đặc tả chưa có (`REQ-01`, `REQ-02`... hoặc giữ ID gốc `UC-xx`/ticket). ID này sẽ dùng cho RTM ở Pha 2, nên phải ổn định.
3. Hỏi tối đa 3 câu nếu thiếu: mục tiêu release, đối tượng người dùng/vai trò, môi trường test sẽ dùng.

### Bước 2 — Requirement Audit (làm TRƯỚC khi lập plan)
Duyệt từng yêu cầu theo checklist:

| Nhóm | Câu hỏi soi |
|---|---|
| Mơ hồ | Có từ không đo được ("nhanh", "thân thiện", "phù hợp", "một số")? Có số/ngưỡng cụ thể chưa? |
| Thiếu luồng lỗi | Input sai/rỗng/quá dài thì sao? Server lỗi, timeout, mất mạng thì sao? Gửi trùng/bấm đúp? |
| Thiếu phân quyền | Vai trò nào được làm gì? User A truy cập tài nguyên user B? Chưa đăng nhập/hết phiên? |
| Mâu thuẫn | Hai yêu cầu nói trái nhau? Yêu cầu trái với hành vi code hiện tại? |
| Thiếu trạng thái | Vòng đời đối tượng (nháp/đã gửi/huỷ)? Chuyển trạng thái nào hợp lệ? |
| Dữ liệu | Định dạng, độ dài, ký tự đặc biệt/Unicode, múi giờ, làm tròn tiền? |
| Phi chức năng | Hiệu năng, bảo mật, tương thích trình duyệt/thiết bị, i18n có được nêu không? |
| Phụ thuộc | Dịch vụ ngoài (email, thanh toán, SMS)? Có môi trường giả lập không? |

Mỗi phát hiện ghi dòng: ID yêu cầu · vấn đề · loại · câu hỏi làm rõ · **mặc định đề xuất** (để người dùng trả lời "ok"). Xếp hạng theo mức ảnh hưởng tới khả năng test. Nếu có phát hiện loại "chặn" (không thể viết test nếu không làm rõ) → nêu đầu danh sách.

### Bước 3 — Soạn Test Plan
Dùng template ở `qa-lifecycle/references/phase-templates.md` mục `01-test-plan.md`. Nếu chạy độc lập, dùng cấu trúc dưới.

1. **Scope**
   - In-scope: liệt kê module/luồng/vai trò/nền tảng, gắn ID yêu cầu.
   - Out-of-scope: nêu rõ + lý do (ví dụ "hạ tầng thanh toán bên thứ 3 — chỉ test tích hợp ở mức mock").
2. **Risk Analysis** — chấm Khả năng × Tác động (H/M/L) cho từng khu vực. Ưu tiên cao: tiền/thanh toán, phân quyền, dữ liệu cá nhân, luồng chính doanh thu, tính năng mới/đang thay đổi nhiều, tích hợp bên ngoài. Kết quả quyết định độ sâu test và Priority P0–P3 ở Pha 2.
3. **Phân bổ chiến lược** — bảng khu vực × `Manual` / `Auto (browser)` / `Auto (API)`:
   - `Auto (browser)`: luồng quan trọng, ổn định, lặp lại nhiều lần (đăng nhập, checkout, CRUD chính) — dùng cho regression.
   - `Auto (API)`: logic nghiệp vụ, validate, phân quyền ở tầng API, tổ hợp dữ liệu lớn.
   - `Manual`: UX/trực quan, tính năng mới chưa ổn định, test thăm dò, case khó/đắt để tự động hoá, kịch bản "phá app".
   - Nêu lý do mỗi lựa chọn; mặc định đề xuất nếu repo đã có công cụ (ví dụ phát hiện sẵn Playwright → dùng).
4. **Môi trường & dữ liệu test** — URL/build, DB seed, tài khoản theo vai trò, dữ liệu biên cần tạo, dịch vụ giả lập, browser/thiết bị. Mục nào chưa biết → `[Cần bổ sung: ...]`; **không** tự điền "Chrome 120" hay tương tự.
5. **Entry / Exit Criteria**
   - Entry: build triển khai được lên môi trường test, smoke pass, dữ liệu sẵn sàng, yêu cầu blocker đã làm rõ.
   - Exit: nêu ngưỡng đề xuất (ví dụ 100% P0 pass, không còn Blocker/Critical mở, RTM phủ 100% yêu cầu in-scope). Ngưỡng cuối cùng chốt cùng `qa-summary-reporter`; ghi `Đề xuất — cần người dùng xác nhận`.
6. **Câu hỏi mở & giả định** — danh sách đánh số, mỗi câu kèm mặc định.

### Bước 4 — Lưu & trình bày
- Ghi `qa-artifacts/01-test-plan.md` (tạo thư mục nếu chưa có; vấn đề `.gitignore` do `qa-lifecycle` hỏi — nếu chạy độc lập, hỏi một lần).
- Trong chat: tóm tắt ≤ 15 dòng — top 5 phát hiện từ Audit, rủi ro cao nhất, chiến lược tổng, câu hỏi mở.
- Thêm khối **Cố vấn QA**: vì sao cần các điểm này, 2–3 góc khuất đặc thù tính năng (phân quyền, rớt mạng, bấm đúp, dữ liệu biên), mặc định sẽ chọn.
- **HARD STOP:** chờ người dùng duyệt hoặc trả lời câu hỏi mở. Không sang test case khi chưa duyệt.

## Ví dụ phát hiện Audit (minh hoạ cách viết)

| Yêu cầu | Vấn đề | Loại | Câu hỏi | Mặc định |
|---|---|---|---|---|
| REQ-03 "Mật khẩu phải đủ mạnh" | Không có tiêu chí đo được | Mơ hồ | Quy tắc độ dài/ký tự cụ thể? | ≥ 8 ký tự, có chữ và số |
| REQ-07 "Admin xoá được bài viết" | Không nói tác giả có xoá bài mình không; xoá mềm hay cứng? | Thiếu phân quyền/trạng thái | Ma trận quyền xoá? | Tác giả + Admin; xoá mềm |

(Đây là ví dụ định dạng, không phải dữ liệu của dự án thật.)

## Checklist hoàn thành

- [ ] Mọi yêu cầu có ID; Audit đã duyệt đủ 8 nhóm
- [ ] Mỗi phát hiện có câu hỏi + mặc định đề xuất
- [ ] Scope có cả Out-of-scope kèm lý do
- [ ] Mỗi khu vực có Execution Type và lý do
- [ ] Không có thông tin môi trường/số liệu bịa
- [ ] Đã lưu file và dừng chờ duyệt
