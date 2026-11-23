# Severity vs Priority Matrix

**Severity** = mức nghiêm trọng về **kỹ thuật/tác động lên hệ thống** (lỗi tệ đến đâu).
**Priority** = độ **gấp về nghiệp vụ** (khi nào cần sửa). Hai trục độc lập: lỗi Severity cao có thể Priority thấp và ngược lại.

## Severity (kỹ thuật)

| Mức | Định nghĩa | Ví dụ thực tế (minh hoạ) |
|---|---|---|
| **Blocker** | Chặn hoàn toàn: không test/dùng tiếp được; hệ thống sập; không có cách vòng | App không khởi động; không ai đăng nhập được; build crash khi mở |
| **Critical** | Chức năng cốt lõi hỏng, mất/sai dữ liệu, lỗ hổng bảo mật, sai tiền; không có workaround | User A xem được dữ liệu user B; thanh toán trừ tiền hai lần; xoá nhầm dữ liệu người khác |
| **Major** | Chức năng chính sai hoặc thiếu nhưng có workaround, hoặc ảnh hưởng nhóm người dùng đáng kể | Lọc theo ngày trả sai kết quả (vẫn xem được bằng cách tìm tay); không xuất được báo cáo PDF nhưng xuất được CSV |
| **Minor** | Chức năng phụ sai, ảnh hưởng nhỏ, có workaround dễ | Sắp xếp cột sai ở trang phụ; thông báo lỗi sai ngữ cảnh nhưng vẫn chặn đúng |
| **Trivial** | Thẩm mỹ/chính tả, không ảnh hưởng chức năng | Lỗi chính tả nhãn; lệch lề vài pixel; icon sai độ đậm |

### Câu hỏi giúp chấm Severity (hỏi theo thứ tự, dừng ở câu đầu tiên trả lời "có")
1. Hệ thống/luồng chính có dùng được không? Không → **Blocker**.
2. Có mất/hỏng dữ liệu, sai tiền, lộ dữ liệu, hoặc vượt quyền không? Có → **Critical**.
3. Chức năng chính có sai/thiếu không? Có → **Major** (nếu có workaround vẫn Major, ghi workaround).
4. Chức năng phụ sai? → **Minor**.
5. Chỉ là hình thức? → **Trivial**.

## Priority (nghiệp vụ)

| Mức | Ý nghĩa | Hành động | Ví dụ |
|---|---|---|---|
| **P0** | Khẩn cấp: phải sửa ngay, chặn release/vận hành | Dừng việc khác; hotfix | Lỗi thanh toán trên production; lộ dữ liệu khách hàng |
| **P1** | Cao: sửa trong bản phát hành hiện tại | Đưa vào sprint/bản hiện tại | Lỗi chức năng chính chưa có workaround rõ |
| **P2** | Trung bình: lên lịch | Bản kế tiếp | Lỗi chức năng phụ, có workaround |
| **P3** | Thấp: làm khi rảnh | Backlog | Lỗi thẩm mỹ, trường hợp rất hiếm |

> P0–P3 của **defect** cùng thang tên với Priority của **test case**, nhưng nghĩa khác: Priority của test case = mức quan trọng khi chạy test; Priority của defect = độ gấp phải sửa. Không nhầm lẫn khi báo cáo.

## Bảng đối chiếu (cách hai trục thường kết hợp)

| Severity \ Priority | P0 | P1 | P2 | P3 |
|---|---|---|---|---|
| Blocker | Thường gặp | Có thể (chặn môi trường test nhưng không phải production) | Hiếm | Hiếm |
| Critical | Thường gặp | Thường gặp | Hiếm | Hiếm |
| Major | Có thể (khi trên luồng doanh thu/ngày cao điểm) | Thường gặp | Thường gặp | Hiếm |
| Minor | Hiếm | Có thể (hiển thị cho khách VIP/demo) | Thường gặp | Thường gặp |
| Trivial | Rất hiếm | Có thể (logo/tên thương hiệu sai) | Có thể | Thường gặp |

### Ví dụ lệch trục (để giải thích cho người dùng)
- **Severity thấp, Priority cao:** sai chính tả tên công ty trên trang chủ trước buổi ra mắt → Trivial / P1.
- **Severity cao, Priority thấp:** crash ở tính năng cũ gần như không ai dùng, chỉ xảy ra với cấu hình đặc biệt → Critical / P2 (cần người dùng/PO xác nhận mức độ dùng thật).

## Yếu tố điều chỉnh Priority (hỏi nếu chưa biết)

- Số người dùng bị ảnh hưởng và tần suất gặp.
- Có workaround dễ dàng không.
- Có nằm trên luồng doanh thu/pháp lý/bảo mật không.
- Sắp tới có mốc release/demo không.
- Lỗi xuất hiện trên production hay chỉ môi trường test.

Priority cuối cùng thuộc về Product Owner/người dùng. QA **đề xuất** kèm lý do.

## Mẫu ghi lý do (một dòng)

```text
Severity: Critical — user thường xem được hoá đơn của user khác (lộ dữ liệu), không có workaround.
Priority: P0 (đề xuất) — ảnh hưởng toàn bộ khách hàng, cần chặn release.
```

## Quy tắc Reproducibility

| Tỉ lệ tái hiện | Ghi |
|---|---|
| Luôn (n/n) | `Always (n/n)` |
| Thỉnh thoảng | `Intermittent (x/y)` + điều kiện nghi ngờ nếu có |
| Chưa tái hiện được | `Cannot Reproduce` — giữ log/mô tả, hỏi thêm thông tin |

Chỉ ghi tỉ lệ khi đã thực sự thử; chưa thử → `[Cần bổ sung: số lần thử]`.
