---
name: qa-summary-reporter
description: Compiles a Test Summary Report from real execution results and defect lists (or qa-artifacts/), with executive verdict Go / Conditional Go / No-Go against quantitative release-gate thresholds, execution table with pass rate, defect statistics by severity and status, RTM coverage, residual risks and next actions. Use when the user says 'test summary report', 'is it ready to release', 'go or no-go', 'QA sign-off', 'release readiness', 'final test report', 'báo cáo tổng kết kiểm thử', 'nghiệm thu', 'có release được chưa', 'kết luận Go/No-Go', 'báo cáo QA cuối kỳ'. Do NOT use for writing test plans, test cases, automation scripts or bug reports (use the other qa-* skills), for code audits, or for PR descriptions.
---

# QA Summary Reporter — Bước 5: Báo cáo & Nghiệm thu

Tổng hợp kết quả thật thành báo cáo và đưa ra kết luận release. Khi chạy trong `qa-lifecycle`, đây là Pha 5/5 (nhãn `[QA Phase 5/5: Summary Report]` ở dòng đầu).

## Quy tắc

- **Đọc trước:** `references/release-gate-criteria.md` (ngưỡng Go / Conditional Go / No-Go).
- **Chỉ dùng dữ liệu thật:** nguồn hợp lệ là (1) `qa-artifacts/02-test-matrix.md`, `03-execution-notes.md`, `04-defects.md`, (2) số liệu người dùng cung cấp trực tiếp. Không ước lượng, không "làm tròn cho đẹp", không suy ra Pass từ việc chưa thấy Fail.
- **Thiếu số liệu:** ghi rõ mục nào chưa có dữ liệu (bảng "Dữ liệu còn thiếu"). Không điền số. Nếu thiếu làm không thể kết luận → verdict `Chưa thể kết luận` kèm danh sách việc cần làm, thay vì đoán.
- Tính toán đều từ bảng thật; ghi công thức và nguồn (file/dòng) để người đọc kiểm lại. Case `Not Run` và `Blocked` **không** tính là Pass.
- Chống mâu thuẫn: nếu số liệu hai nguồn lệch (ví dụ defect Closed nhưng TC liên quan vẫn Fail) → nêu rõ, hỏi người dùng, không tự chọn.
- Ngưỡng nào do người dùng/Test Plan đã chốt thì ưu tiên theo đó; mặc định trong file reference chỉ là đề xuất.

## Quy trình

1. **Nạp dữ liệu:** đọc các file trong `qa-artifacts/`; nếu không có, hỏi người dùng số liệu hoặc xin file/bảng kết quả. Xác định vòng chạy mới nhất (nếu có nhiều vòng re-test, dùng trạng thái mới nhất của từng case/defect và nêu rõ).
2. **Kiểm tra đủ dữ liệu:** có bảng kết quả theo TC? Có danh sách defect với Severity/Status? Có RTM? Liệt kê phần thiếu.
3. **Tính số liệu:**
   - Execution: `Total`, `Passed`, `Failed`, `Blocked`, `Not Run`. `Pass Rate = Passed / Total` (và, nếu hữu ích, `Passed / (Total − Not Run − Blocked)` ghi rõ là "trên các case đã chạy"). Tính thêm theo Priority (đặc biệt P0, P1).
   - Defect: đếm theo Severity × Status; số Blocker/Critical còn mở; số defect mở theo Priority.
   - RTM: yêu cầu đủ phủ / tổng; yêu cầu có case Fail/Not Run; yêu cầu chưa có case.
4. **Đối chiếu ngưỡng** trong reference → chọn verdict. Nêu **từng** tiêu chí: đạt/không đạt + số liệu.
5. **Rủi ro tồn đọng:** defect mở, case Blocked/Not Run, vùng ít test (đối chiếu Risk Analysis ở Test Plan), giới hạn môi trường, giả định chưa xác nhận.
6. **Hành động tiếp theo:** việc cụ thể, đề xuất owner/hạn nếu biết (không biết → `[Cần bổ sung]`).
7. **Ghi `qa-artifacts/05-summary-report.md`** và trình bày trong chat bản tóm tắt ≤ 20 dòng.

## Cấu trúc báo cáo

```markdown
# Test Summary Report — <Tên tính năng/release>
(header chung: ngày, phiên bản, build/commit [Cần bổ sung nếu thiếu], môi trường, nguồn dữ liệu)

## 1. Executive Verdict: Go | Conditional Go | No-Go
Lý do 3–5 dòng, dẫn từng tiêu chí đã đạt/không đạt.
Điều kiện (chỉ với Conditional Go): danh sách việc bắt buộc, owner, hạn, cách xác minh.

## 2. Execution Summary
| Total | Passed | Failed | Blocked | Not Run | Pass Rate |
Theo Priority: bảng P0/P1/P2/P3 cùng các cột trên.

## 3. Defect Statistics
Ma trận Severity (Blocker…Trivial) × Status (New/Open/Fixed/Re-test/Closed/Reopened/Won't Fix). Danh sách defect còn mở có Severity ≥ Major.

## 4. Requirement Coverage (RTM)
Tổng yêu cầu · Đủ phủ · Có case Fail · Có case Not Run · Chưa có case. Liệt kê yêu cầu rủi ro.

## 5. Rủi ro tồn đọng
## 6. Hành động tiếp theo
## 7. Dữ liệu còn thiếu / Giả định
```

Mọi bảng phải điền từ dữ liệu thật; ô không có dữ liệu ghi `N/A — chưa có dữ liệu` (không để 0 nếu thực ra chưa biết).

## Khối Cố vấn QA

Giải thích bằng ngôn ngữ developer: vì sao Go/No-Go dựa trên ngưỡng chứ không dựa cảm giác; vì sao `Not Run` là rủi ro chứ không phải "tạm ổn"; nhắc góc khuất chưa phủ (phân quyền, rớt mạng, bấm đúp, dữ liệu biên); phương án mặc định (ví dụ "Conditional Go với 2 điều kiện X, Y — hoặc hoãn một vòng nếu bạn muốn an toàn hơn").

## Lưu ý

- Verdict là **khuyến nghị của QA**; quyết định phát hành thuộc người dùng/PO. Nói rõ điều này.
- Không dùng ngôn từ cảm tính ("khá ổn", "gần như xong"); dùng số liệu.
- Báo cáo cho dự án nhỏ/cá nhân vẫn giữ đủ cấu trúc; có thể ngắn nhưng không bỏ mục.

## Ví dụ minh hoạ

Xem `references/worked-example.md` để biết định dạng đầu ra mẫu (dữ liệu hư cấu, chỉ đọc khi cần; không sao chép số liệu của ví dụ vào dự án thật).

## Checklist hoàn thành

- [ ] Đã đọc `release-gate-criteria.md` và nêu ngưỡng áp dụng (mặc định hay đã chốt)
- [ ] Mọi con số truy được nguồn trong `qa-artifacts/` hoặc từ người dùng
- [ ] Not Run/Blocked không bị tính là Pass
- [ ] Mỗi tiêu chí gate có kết quả đạt/không đạt kèm số liệu
- [ ] Có mục "Dữ liệu còn thiếu"; verdict không dựa trên dữ liệu bịa
- [ ] Đã lưu `05-summary-report.md`
