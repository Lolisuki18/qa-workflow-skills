# Evals — tự kiểm skill / Self-check for the skills

Hai bộ kiểm tra thủ công (chạy được trên mọi agent) / Two manual check sets that work on any agent:

| File | Mục đích / Purpose |
|---|---|
| [trigger-prompts.md](trigger-prompts.md) | Prompt **nên** và **không nên** kích hoạt từng skill (VI + EN) / prompts that should and should not trigger each skill |
| [behavior-checks.md](behavior-checks.md) | Kịch bản kiểm hành vi: nhãn pha, Hard Stop, chống ảo giác / behavior scenarios: phase label, hard stops, anti-hallucination |

## Cách chạy / How to run

1. Cài bộ skill (bản `qa-*` ở root cho tiếng Việt, hoặc `en/qa-*` cho tiếng Anh; chỉ cài **một** bộ để tránh trùng tên).
   Install one set only (Vietnamese `qa-*` at root, or `en/qa-*`) to avoid duplicate names.
2. Mở phiên mới (không có ngữ cảnh cũ), dán từng prompt. / Start a fresh session and paste each prompt.
3. Ghi lại: skill nào được kích hoạt, có đúng không. Tính tỉ lệ đúng cho nhóm "nên" và nhóm "không nên". / Record which skill fired.
4. Với behavior-checks, đối chiếu từng tiêu chí Đạt/Không đạt. / For behavior checks, mark each criterion pass/fail.

**Mục tiêu gợi ý / Suggested targets:** ≥ 90% prompt "nên" kích hoạt đúng skill; 0 prompt "không nên" kích hoạt nhầm skill QA; mọi tiêu chí chống ảo giác Đạt.

Kết quả phụ thuộc agent và mô hình; ghi lại agent/mô hình đã dùng khi báo cáo. / Results vary by agent and model; record which you used.
