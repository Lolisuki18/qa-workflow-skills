# qa-workflow-skills

Bộ **Agent Skills** độc lập cho toàn bộ vòng đời kiểm thử phần mềm (STLC), theo đặc tả chuẩn mở Anthropic Agent Skills. Dùng được với Claude Code, Cursor, Gemini CLI, Codex và các AI coding agent khác đọc `SKILL.md`.

Thiết kế cho cả developer không chuyên QA: AI đóng vai **cố vấn QA chủ động** — giải thích vì sao cần test điểm này, cảnh báo góc khuất, đề xuất phương án mặc định để chọn nhanh.

## 5 pha, 6 skill

| Pha | Skill | Đầu ra (`qa-artifacts/`) |
|---|---|---|
| Điều phối | `qa-lifecycle` | Điều khiển 5 pha, hard stop duyệt |
| 1. Soi yêu cầu & chiến lược | `qa-test-plan-writer` | `01-test-plan.md` |
| 2. Thiết kế test case | `qa-test-matrix-writer` | `02-test-matrix.md` (+ RTM) |
| 3. Chạy test & automation | `qa-e2e-writer` | `03-execution-notes.md` + code Playwright |
| 4. Quản lý lỗi | `qa-defect-writer` | `04-defects.md` |
| 5. Báo cáo & nghiệm thu | `qa-summary-reporter` | `05-summary-report.md` |

> **Trạng thái:** cả 6 skill đã hoàn tất (Đợt 1 và Đợt 2).

## Cấu trúc

```text
qa-workflow-skills/
├── README.md
├── qa-lifecycle/            (SKILL.md, references/phase-templates.md)
├── qa-test-plan-writer/     (SKILL.md)
├── qa-test-matrix-writer/   (SKILL.md, references/test-design-techniques.md)
├── qa-e2e-writer/           (SKILL.md, references/playwright-standards.md, exploratory-charters.md)
├── qa-defect-writer/        (SKILL.md, references/severity-priority-matrix.md)
└── qa-summary-reporter/     (SKILL.md, references/release-gate-criteria.md)
```

## Cài đặt

Copy (hoặc symlink) các thư mục `qa-*` ở root repo vào nơi agent của bạn đọc skill:

| Agent | Thư mục skill (tham khảo, kiểm tra tài liệu agent của bạn) |
|---|---|
| Claude Code | `~/.claude/skills/` hoặc `<project>/.claude/skills/` |
| Cursor / Gemini CLI / Codex | theo cơ chế skill/rules của từng agent; có thể trỏ agent tới file `SKILL.md` |

## Cách dùng

Chỉ cần nói tự nhiên, ví dụ:

- "Lập quy trình QA đầy đủ cho tính năng đăng nhập" → `qa-lifecycle`
- "Viết test plan từ SRS này" → `qa-test-plan-writer`
- "Sinh test case và RTM cho module giỏ hàng" → `qa-test-matrix-writer`

Mỗi phản hồi của `qa-lifecycle` bắt đầu bằng nhãn `[QA Phase X/5: Tên pha]`. Pha 1 và 2 có **Hard Stop**: AI dừng chờ bạn duyệt rồi mới đi tiếp.

## Nguyên tắc chung

- **Chống ảo giác:** không bịa số liệu Pass/Fail, môi trường, browser hay bước tái hiện; thiếu thì ghi `[Cần bổ sung: ...]` hoặc hỏi lại.
- **Không lẫn unit test:** bộ skill này lo kiểm thử ở góc nhìn QA (chức năng, E2E, API, thăm dò), không viết unit test của dev.
- **Progressive disclosure:** `SKILL.md` gọn (<250 dòng), nội dung dài nằm ở `references/`.
