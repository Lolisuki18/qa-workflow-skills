# Trigger Prompts

✅ should trigger, ❌ should not (the better skill is noted where one exists). Vietnamese prompts are kept on purpose: descriptions carry bilingual trigger keywords.

## qa-lifecycle
| | Prompt |
|---|---|
| ✅ | Chạy quy trình QA đầy đủ cho tính năng đăng nhập của tôi |
| ✅ | Run a full QA process for the checkout feature, from test plan to release verdict |
| ✅ | Tôi muốn kiểm thử bài bản từ đầu đến cuối trước khi release |
| ❌ | Viết unit test cho hàm `calculateTotal` (unit test của dev) |
| ❌ | Chỉ viết cho tôi cái test plan thôi → `qa-test-plan-writer` |

## qa-test-plan-writer
| | Prompt |
|---|---|
| ✅ | Soi giúp tôi đặc tả này có chỗ nào mơ hồ trước khi test |
| ✅ | Write a test plan with scope, risks and entry/exit criteria from this SRS |
| ✅ | Lập chiến lược test: phần nào manual, phần nào automation? |
| ❌ | Sinh bảng test case và RTM → `qa-test-matrix-writer` |
| ❌ | Lên kế hoạch triển khai code cho tính năng mới (kế hoạch phát triển, không phải kiểm thử) |

## qa-test-matrix-writer
| | Prompt |
|---|---|
| ✅ | Viết test case cho module giỏ hàng, kèm ma trận truy vết yêu cầu |
| ✅ | Generate test cases with boundary value analysis and export to CSV for TestRail |
| ✅ | Xuất bảng test case ra file CSV để import Excel |
| ❌ | Viết test Playwright cho trang đăng nhập → `qa-e2e-writer` |
| ❌ | Review lỗ hổng trong đặc tả → `qa-test-plan-writer` |

## qa-e2e-writer
| | Prompt |
|---|---|
| ✅ | Viết test Playwright cho các case Auto (browser) trong ma trận test |
| ✅ | Give me a manual exploratory script to try to break the signup form |
| ✅ | Chạy test và ghi kết quả vào execution notes |
| ❌ | Viết bug report cho lỗi này → `qa-defect-writer` |
| ❌ | Viết unit test Jest cho service này (unit test của dev) |

## qa-defect-writer
| | Prompt |
|---|---|
| ✅ | Biến mô tả lỗi này thành bug report chuẩn: "bấm thanh toán hai lần bị trừ tiền hai lần" |
| ✅ | Dev says DEF-003 is fixed — give me the re-test and regression checklist |
| ✅ | Lỗi này nên đánh Severity hay Priority nào? |
| ❌ | Tìm nguyên nhân gốc và sửa code lỗi này (debug, không phải QA) |
| ❌ | Tổng hợp báo cáo release → `qa-summary-reporter` |

## qa-summary-reporter
| | Prompt |
|---|---|
| ✅ | Tổng hợp báo cáo kiểm thử, cho tôi biết Go hay No-Go |
| ✅ | Is this ready to release? Write the test summary report from qa-artifacts |
| ✅ | Báo cáo nghiệm thu cuối kỳ cho dự án |
| ❌ | Viết bug report cho lỗi mới → `qa-defect-writer` |
| ❌ | Viết mô tả pull request |

## qa-api-tester
| | Prompt |
|---|---|
| ✅ | Viết test API cho các endpoint đăng nhập và đặt hàng, kiểm tra status code và schema |
| ✅ | Test these REST endpoints for auth, validation and permission, and give me a Postman collection |
| ✅ | Chạy các case Auto (API) trong ma trận test và ghi kết quả |
| ❌ | Viết test Playwright cho trang đăng nhập → `qa-e2e-writer` |
| ❌ | Viết unit test cho controller này (unit test của dev) |

## qa-nonfunctional-writer
| | Prompt |
|---|---|
| ✅ | Thiết kế test hiệu năng và test tải cho trang danh sách sản phẩm |
| ✅ | Check this signup flow for accessibility (WCAG) and cross-browser compatibility |
| ✅ | Lập bộ test phi chức năng cho tính năng thanh toán |
| ❌ | Viết bảng test case chức năng và RTM → `qa-test-matrix-writer` |
| ❌ | Review code tìm lỗ hổng bảo mật trong mã nguồn (đây là review code, không phải QA) |

## qa-regression-planner
| | Prompt |
|---|---|
| ✅ | Dev vừa sửa 5 lỗi, tôi cần test lại những case nào? |
| ✅ | Build a regression plan from the RTM and this diff: smoke, targeted and full |
| ✅ | Chọn danh sách smoke test cho bản build mới |
| ❌ | Viết checklist re-test cho đúng một lỗi vừa sửa → `qa-defect-writer` |
| ❌ | Viết test plan cho release mới → `qa-test-plan-writer` |

## Ambiguous prompts — expect a clarifying question
| Prompt | Expected |
|---|---|
| "Test giúp tôi cái này" ("Test this for me") | Asks which kind of testing is meant (QA plan/cases/execution vs developer unit tests) and the target |
| "Write tests" (repo has both Playwright and Jest) | Asks whether QA E2E tests or unit tests are wanted |
