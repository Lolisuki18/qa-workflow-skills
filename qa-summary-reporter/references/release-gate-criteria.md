# Release Gate Criteria

Ngưỡng định lượng để chọn **Go / Conditional Go / No-Go**. Đây là **ngưỡng mặc định đề xuất**. Nếu Test Plan (`01-test-plan.md` mục Exit Criteria) hoặc người dùng đã chốt ngưỡng khác, dùng ngưỡng đó và ghi rõ nguồn. Khi áp mặc định, nói thẳng "ngưỡng mặc định, chưa được xác nhận".

## Định nghĩa số liệu

| Chỉ số | Công thức |
|---|---|
| Pass Rate | Passed / Total |
| Executed Rate | (Passed + Failed) / Total |
| P0 Pass Rate | P0 Passed / P0 Total |
| RTM Coverage | Số yêu cầu in-scope có đủ case / tổng yêu cầu in-scope |
| Open Defect | Status ∈ {New, Open, Fixed (chưa re-test), Re-test, Reopened} |

`Not Run` và `Blocked` **không** tính là Passed.

## Ngưỡng mặc định

| Tiêu chí | Go | Conditional Go | No-Go |
|---|---|---|---|
| P0 Pass Rate | 100% | 100% (bắt buộc) | < 100% |
| P1 Pass Rate | ≥ 95% | ≥ 90% | < 90% |
| Pass Rate tổng | ≥ 95% | ≥ 90% | < 90% |
| Executed Rate | 100% | ≥ 95% (phần còn lại có lý do và kế hoạch) | < 95% |
| Case Blocked | 0 | ≤ 5%, không thuộc P0 | > 5% hoặc có P0 Blocked |
| Blocker mở | 0 | 0 | ≥ 1 |
| Critical mở | 0 | 0 (hoặc có biện pháp giảm thiểu được người dùng/PO chấp nhận bằng văn bản) | ≥ 1 không biện pháp |
| Major mở | 0 | ≤ 3, đều có workaround đã ghi nhận và kế hoạch sửa | > 3 hoặc có Major không workaround |
| Minor/Trivial mở | Bất kỳ, đã ghi backlog | Bất kỳ, đã ghi backlog | — |
| RTM Coverage | 100% | ≥ 95%, yêu cầu thiếu đều P2/P3 | < 95% hoặc thiếu yêu cầu P0/P1 |
| Defect đã Fixed nhưng chưa Re-test | 0 | Có, chỉ ở Minor/Trivial | Có ở Major trở lên |
| Phân quyền/bảo mật | Mọi case đã chạy và Pass | Như Go | Có case fail hoặc chưa chạy |

> Điều kiện **bất kỳ cột No-Go nào đúng → No-Go**. Nếu không có cột No-Go nào đúng nhưng không đạt đủ cột Go → **Conditional Go**. Chỉ khi đạt **tất cả** cột Go → **Go**.

## Cách chọn verdict (thuật toán)

1. Có dữ liệu để tính mọi tiêu chí bắt buộc không? Không → `Chưa thể kết luận`, liệt kê dữ liệu cần bổ sung. (Không đoán.)
2. Duyệt tiêu chí cột No-Go. Có bất kỳ cái nào đúng → **No-Go**; liệt kê tất cả.
3. Ngược lại, đạt hết cột Go → **Go**.
4. Ngược lại → **Conditional Go**, kèm điều kiện cụ thể.

## Điều kiện cho Conditional Go

Mỗi điều kiện phải:
- Cụ thể, kiểm chứng được (ví dụ "Re-test DEF-007 và regression nhóm Thanh toán đều Pass trên build kế tiếp").
- Có owner và hạn (nếu không biết → `[Cần bổ sung]`).
- Nêu hậu quả nếu không thực hiện (chuyển thành No-Go).

Các loại điều kiện thường gặp: sửa và re-test defect Major cụ thể; chạy nốt nhóm case Not Run; xác nhận bằng văn bản chấp nhận rủi ro tồn đọng; theo dõi chỉ số sau phát hành; chuẩn bị kế hoạch rollback.

## Điều chỉnh theo bối cảnh (chỉ khi người dùng đồng ý)

| Bối cảnh | Điều chỉnh gợi ý |
|---|---|
| Hệ thống tiền/y tế/bảo mật cao | Siết: Major mở = 0 cho Go và Conditional Go; Pass Rate ≥ 98% |
| MVP/demo nội bộ/đồ án | Nới: chấp nhận Major mở có workaround, Pass Rate ≥ 85%; vẫn giữ P0 = 100% và Blocker/Critical = 0 |
| Hotfix | Tập trung: re-test lỗi sửa + regression vùng ảnh hưởng đạt 100%; phần còn lại theo plan đã chốt |
| Có tính năng tắt được bằng feature flag | Có thể nới điều kiện cho tính năng đó, ghi rõ cách tắt |

Mọi điều chỉnh phải ghi vào báo cáo mục "Ngưỡng áp dụng" (mặc định hay chỉnh, ai chốt).

## Mẫu đoạn kết luận

```markdown
**Executive Verdict: Conditional Go** (ngưỡng mặc định — chưa được xác nhận)
- Đạt: P0 Pass Rate 100% (a/a), Blocker mở 0, Critical mở 0.
- Không đạt cột Go: Pass Rate tổng x% (< 95%), Major mở n (> 0).
- Điều kiện: (1) ... owner/hạn ..., (2) ...
- Nếu không đạt điều kiện trước ngày ...: chuyển No-Go.
Đây là khuyến nghị của QA; quyết định phát hành thuộc về người dùng/PO.
```

(Ví dụ chỉ minh hoạ định dạng — các số a, x, n phải lấy từ dữ liệu thật.)

## Dữ liệu tối thiểu để báo cáo được

- [ ] Bảng kết quả theo từng TC (có Priority)
- [ ] Danh sách defect với Severity, Status
- [ ] RTM hoặc danh sách yêu cầu in-scope
- [ ] Build/phiên bản và môi trường đã test (thiếu → ghi `[Cần bổ sung]`, vẫn báo cáo được nhưng nêu giới hạn)
- [ ] Ngưỡng Exit đã chốt (thiếu → dùng mặc định và nói rõ)
