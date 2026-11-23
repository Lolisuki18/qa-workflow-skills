# Ví dụ chạy thật — qa-summary-reporter

> ⚠️ Số liệu **hư cấu**, lấy từ ví dụ của `qa-e2e-writer` và `qa-defect-writer` ("DemoShop"). Trong thực tế mọi con số phải đọc từ `qa-artifacts/`.

## Dữ liệu đầu vào (từ `03-execution-notes.md` và `04-defects.md`)

9 test case: 7 Pass, 1 Fail (TC-LOGIN-006), 1 Not Run (TC-LOGIN-008). 1 defect: DEF-001, Critical, Status Open.

## Số liệu tính được

| Total | Passed | Failed | Blocked | Not Run | Pass Rate |
|---|---|---|---|---|---|
| 9 | 7 | 1 | 0 | 1 | 77.8% (7/9) |

| Priority | Total | Passed | Pass Rate |
|---|---|---|---|
| P0 | 4 | 3 | 75.0% |
| P1 | 3 | 3 | 100% |
| P2 | 2 | 1 | 50.0% (1 Not Run) |

Defect: Critical × Open = 1; các ô khác = 0. RTM Coverage: 4/4 yêu cầu có case, nhưng REQ-04 có case Fail.

## Đối chiếu ngưỡng (mặc định, chưa được xác nhận)

| Tiêu chí | Giá trị | Kết quả |
|---|---|---|
| P0 Pass Rate = 100% | 75.0% | Không đạt → cột No-Go |
| Critical mở = 0 | 1 | Không đạt → cột No-Go |
| Pass Rate tổng ≥ 90% | 77.8% | Không đạt |
| Executed Rate ≥ 95% | 88.9% (8/9) | Không đạt |

## Executive Verdict: **No-Go** (ngưỡng mặc định — chưa được xác nhận)

- Không đạt: P0 chưa 100%, còn 1 Critical mở (DEF-001, vượt quyền vào /admin).
- Hành động: dev sửa DEF-001 → re-test + regression (TC-LOGIN-006, 009) → chạy nốt TC-LOGIN-008 → lập lại báo cáo.
- Dữ liệu còn thiếu: build/môi trường, trình duyệt đã test.
- Đây là khuyến nghị của QA; quyết định phát hành thuộc về người dùng/PO.

**Điểm cần học:** Not Run không tính là Pass; mỗi tiêu chí có số liệu và kết quả; ghi rõ dữ liệu còn thiếu và tính chất "ngưỡng mặc định".
