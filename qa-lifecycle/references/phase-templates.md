# Phase Templates — qa-lifecycle

Template cho 5 file trong `qa-artifacts/`. Mọi chỗ chưa có dữ liệu thật phải ghi `[Cần bổ sung: ...]`. Không bịa số liệu.

## Header chung (đặt đầu mỗi file)

```markdown
# <Tên tài liệu> — <Tên tính năng/release>
- **Pha:** X/5 — <Tên pha>
- **Ngày:** YYYY-MM-DD
- **Phiên bản:** v0.1
- **Trạng thái:** Draft | Approved (ngày duyệt: ...)
- **Nguồn yêu cầu:** <SRS / Use Case / ticket / đường dẫn code>
- **Người duyệt:** [Cần bổ sung: ...]
```

---

## 01-test-plan.md

```markdown
## 1. Requirement Audit
| # | Yêu cầu (ID) | Vấn đề | Loại (Mơ hồ/Thiếu luồng lỗi/Thiếu phân quyền/Mâu thuẫn) | Câu hỏi cần làm rõ | Mặc định đề xuất |
## 2. Scope
- In-scope: ...
- Out-of-scope: ... (kèm lý do)
## 3. Risk Analysis
| Rủi ro | Khả năng (H/M/L) | Tác động (H/M/L) | Mức ưu tiên test | Biện pháp |
## 4. Chiến lược kiểm thử
| Khu vực/Module | Manual | Auto (browser) | Auto (API) | Lý do |
## 5. Môi trường & dữ liệu test
- Môi trường: [Cần bổ sung: URL/phiên bản build]
- Browser/thiết bị: [Cần bổ sung: ...]
- Tài khoản/vai trò: ...
- Dữ liệu cần chuẩn bị: ...
## 6. Entry / Exit Criteria
## 7. Lịch & phân công (nếu có)
## 8. Câu hỏi mở / Giả định
```

## 02-test-matrix.md

```markdown
## 1. Tổng quan
Số TC: N | P0: a | P1: b | P2: c | P3: d | Manual: x | Auto (browser): y | Auto (API): z
## 2. Test Cases
| TC ID | Req/UC ID | Module | Title | Pre-condition | Test Steps | Test Data | Expected Result | Priority | Execution Type |
## 3. RTM (Requirement Traceability Matrix)
| Req/UC ID | Mô tả yêu cầu | TC ID (Happy) | TC ID (Negative) | TC ID (Permission) | Trạng thái phủ |
## 4. Yêu cầu chưa được phủ / Ghi chú
```

## 03-execution-notes.md

```markdown
## 1. Thông tin lần chạy
- Vòng chạy: 1 | Ngày: ... | Build/commit: [Cần bổ sung] | Môi trường: [Cần bổ sung] | Người chạy: ...
## 2. Kết quả theo test case
| TC ID | Execution Type | Kết quả (Pass/Fail/Blocked/Not Run) | Ngày chạy | Defect ID | Bằng chứng/Ghi chú |
## 3. Automation
- File test: ... | Lệnh chạy: ... | Kết quả thô (dán output thật): ...
## 4. Phát hiện từ Exploratory
## 5. Vấn đề chặn (Blocked) & nguyên nhân
```

## 04-defects.md

```markdown
## 1. Bảng tổng hợp
| Defect ID | Title | Severity | Priority | Status (New/Open/Fixed/Re-test/Closed/Reopened/Won't Fix) | TC liên quan |
## 2. Chi tiết từng defect
### DEF-001 — [Module] Hiện tượng + Điều kiện
- Environment / Severity / Priority / Pre-conditions
- Steps to Reproduce / Actual / Expected / Evidence
## 3. Lịch sử Re-test
| Defect ID | Vòng | Build | Kết quả | Regression đã kiểm |
```

## 05-summary-report.md

```markdown
## 1. Executive Verdict: Go | Conditional Go | No-Go
(lý do 3–5 dòng, dẫn chiếu ngưỡng đã chọn)
## 2. Execution Summary
| Total | Passed | Failed | Blocked | Not Run | Pass Rate |
## 3. Defect Statistics (Severity × Status)
## 4. Requirement Coverage (từ RTM)
## 5. Rủi ro tồn đọng
## 6. Hành động tiếp theo (owner, hạn)
## 7. Dữ liệu còn thiếu
```

---

## Mẫu khối Cố vấn QA (dán cuối mỗi pha)

```markdown
> **Cố vấn QA**
> - *Vì sao quan trọng:* ...
> - *Góc khuất cần để ý:* ...
> - *Mặc định tôi sẽ chọn nếu bạn không phản hồi:* ...
```

## Mẫu Hard Stop

```markdown
**⏸ HARD STOP — chờ duyệt**
Tôi đã lưu `qa-artifacts/0X-....md` (Draft). Vui lòng:
1. Trả lời các câu hỏi mở (hoặc chấp nhận mặc định đã nêu).
2. Nhắn "duyệt" để sang Pha tiếp theo, hoặc nêu chỗ cần sửa.
```
