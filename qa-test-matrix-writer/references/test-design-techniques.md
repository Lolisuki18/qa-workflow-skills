# Test Design Techniques

Sáu kỹ thuật dùng để sinh test case có hệ thống. Các ví dụ dùng số liệu **minh hoạ** — khi áp dụng thật, lấy ngưỡng/quy tắc từ đặc tả hoặc code, thiếu thì ghi `[Cần bổ sung: ...]`.

## Chọn nhanh kỹ thuật

| Tình huống trong yêu cầu | Kỹ thuật chính | Kết hợp |
|---|---|---|
| Field nhập liệu, có khoảng/định dạng/độ dài | Equivalence Partitioning | Boundary Value Analysis |
| Số lượng, giá tiền, độ dài, ngày, phân trang, giới hạn | Boundary Value Analysis | Equivalence Partitioning |
| Nhiều điều kiện kết hợp ra kết quả khác nhau (giảm giá, duyệt đơn) | Decision Table | Boundary Value Analysis |
| Đối tượng có vòng đời/trạng thái (đơn hàng, ticket, tài khoản) | State Transition | Error Guessing |
| Nhiều vai trò, quyền khác nhau | Role-Based Access Control | State Transition |
| Mọi tính năng, bước cuối | Error Guessing | — |

---

## 1. Equivalence Partitioning (EP) — Phân vùng tương đương

**Ý tưởng:** chia miền đầu vào thành các vùng mà hệ thống xử lý "như nhau"; mỗi vùng test một đại diện. Phải có cả vùng **hợp lệ** và **không hợp lệ**.

**Cách làm**
1. Liệt kê input và quy tắc của nó.
2. Chia: hợp lệ (có thể nhiều vùng nếu xử lý khác nhau) và không hợp lệ (dưới, trên, sai kiểu, rỗng, null, sai định dạng).
3. Mỗi vùng ≥ 1 test case. Không gộp hai vùng không hợp lệ vào một case (khó biết lỗi do đâu).

**Ví dụ minh hoạ:** trường "Tuổi" yêu cầu số nguyên 18–60.

| Vùng | Loại | Đại diện |
|---|---|---|
| < 18 | Không hợp lệ | 10 |
| 18–60 | Hợp lệ | 30 |
| > 60 | Không hợp lệ | 75 |
| Không phải số | Không hợp lệ | `abc` |
| Số thập phân | Không hợp lệ | `25.5` |
| Rỗng | Không hợp lệ | (để trống) |
| Số âm | Không hợp lệ | `-5` |

**Lỗi hay gặp:** quên vùng rỗng/khoảng trắng, quên kiểu dữ liệu sai, quên ký tự đặc biệt/Unicode (dấu tiếng Việt, emoji) với field văn bản.

---

## 2. Boundary Value Analysis (BVA) — Phân tích giá trị biên

**Ý tưởng:** lỗi tập trung ở ranh giới (`<` vs `<=`, lệch 1). Test tại biên và sát hai bên biên.

**Cách làm (2-value hoặc 3-value)**
- Với khoảng [min, max]: test `min-1`, `min`, `min+1`, `max-1`, `max`, `max+1`.
- Biên của số lượng, độ dài chuỗi, kích thước file, ngày/giờ, trang cuối cùng, số lượng phần tử trong danh sách (0, 1, nhiều, tối đa).

**Ví dụ minh hoạ:** mật khẩu 8–20 ký tự.

| Giá trị | Độ dài | Kỳ vọng |
|---|---|---|
| min-1 | 7 | Từ chối |
| min | 8 | Chấp nhận |
| min+1 | 9 | Chấp nhận |
| max-1 | 19 | Chấp nhận |
| max | 20 | Chấp nhận |
| max+1 | 21 | Từ chối |

**Biên đáng nhớ:** 0 và 1 phần tử; trang đầu/trang cuối/trang vượt quá; ngày cuối tháng, năm nhuận, chuyển múi giờ/DST; tiền làm tròn (0.01, 0.005); file đúng bằng giới hạn dung lượng; chuỗi chứa ký tự đa byte (đếm ký tự hay byte?).

---

## 3. Decision Table — Bảng quyết định

**Ý tưởng:** khi kết quả phụ thuộc **tổ hợp** điều kiện, liệt kê mọi tổ hợp (hoặc rút gọn hợp lý) và kết quả tương ứng; mỗi cột luật = một test case.

**Cách làm**
1. Liệt kê điều kiện (Y/N hoặc giá trị) và hành động/kết quả.
2. Với n điều kiện Y/N có 2ⁿ tổ hợp; rút gọn các tổ hợp không thể xảy ra hoặc kết quả giống nhau — ghi rõ lý do rút gọn.
3. Mỗi luật → 1 test case với dữ liệu cụ thể.

**Ví dụ minh hoạ:** giảm giá khi thanh toán.

| Điều kiện | R1 | R2 | R3 | R4 |
|---|---|---|---|---|
| Là thành viên | Y | Y | N | N |
| Có mã giảm giá hợp lệ | Y | N | Y | N |
| **Hành động** | | | | |
| Áp dụng giảm giá thành viên | ✔ | ✔ | — | — |
| Áp dụng mã giảm giá | ✔* | — | ✔ | — |
| Giá gốc | — | — | — | ✔ |

(*) Có cộng dồn hay không là điểm **chưa rõ** → đưa vào câu hỏi làm rõ, không tự giả định.

**Lỗi hay gặp:** bỏ sót tổ hợp "tất cả sai"; không hỏi thứ tự ưu tiên/cộng dồn của các luật.

---

## 4. State Transition — Chuyển trạng thái

**Ý tưởng:** đối tượng có các trạng thái và sự kiện làm chuyển trạng thái. Test cả chuyển **hợp lệ** và cố tình chuyển **không hợp lệ**.

**Cách làm**
1. Vẽ/liệt kê trạng thái, sự kiện, điều kiện (guard), hành động.
2. Dựng bảng trạng thái × sự kiện. Ô hợp lệ → test chuyển đúng. Ô không hợp lệ → test bị từ chối và trạng thái không đổi.
3. Phủ ít nhất: mọi chuyển hợp lệ (0-switch); các chuỗi chuyển quan trọng (1-switch, ví dụ Huỷ rồi Khôi phục); trạng thái cuối cùng (không thoát ra được).

**Ví dụ minh hoạ:** đơn hàng.

| Trạng thái \ Sự kiện | Thanh toán | Giao hàng | Huỷ | Hoàn tiền |
|---|---|---|---|---|
| Mới | Đã thanh toán | ✗ | Đã huỷ | ✗ |
| Đã thanh toán | ✗ | Đang giao | Đã huỷ* | ✗ |
| Đang giao | ✗ | Đã giao | ✗ | ✗ |
| Đã giao | ✗ | ✗ | ✗ | Đã hoàn tiền |

(✗ = không hợp lệ, phải bị từ chối. *Huỷ sau thanh toán có hoàn tiền tự động không → cần làm rõ.)

**Góc khuất:** thao tác trùng (bấm "Thanh toán" hai lần), hai người cùng đổi trạng thái (race condition), gọi API chuyển trạng thái trực tiếp bỏ qua UI, quay lại bằng nút Back sau khi chuyển trạng thái.

---

## 5. Role-Based Access Control (RBAC) — Kiểm thử phân quyền

**Ý tưởng:** mỗi cặp (vai trò × hành động × tài nguyên) có kết quả cho phép/từ chối. Lỗi phân quyền thường là lỗi bảo mật nghiêm trọng → thường P0/P1.

**Cách làm**
1. Liệt kê vai trò (bao gồm **khách chưa đăng nhập** và **phiên hết hạn**), hành động, loại tài nguyên.
2. Dựng ma trận quyền kỳ vọng từ đặc tả (thiếu → hỏi; không tự suy).
3. Test:
   - Mỗi ô **được phép** → thực hiện thành công.
   - Mỗi ô **bị cấm** → bị từ chối đúng cách (ẩn nút **và** chặn ở tầng server/API: truy cập thẳng URL/endpoint).
   - **Horizontal:** user A truy cập tài nguyên của user B (đổi ID trên URL/request).
   - **Vertical:** user thường gọi chức năng admin.
   - Đổi vai trò/thu hồi quyền khi đang đăng nhập → hiệu lực thế nào?

**Ví dụ minh hoạ**

| Hành động | Khách | User (chủ) | User (khác) | Admin |
|---|---|---|---|---|
| Xem bài | ✔ | ✔ | ✔ | ✔ |
| Sửa bài | ✗ | ✔ | ✗ | ✔ |
| Xoá bài | ✗ | ✔ | ✗ | ✔ |
| Xem trang quản trị | ✗ | ✗ | ✗ | ✔ |

**Lưu ý kết quả từ chối:** nêu rõ mong đợi (chuyển trang đăng nhập / thông báo / mã 401 vs 403 vs 404) — nếu đặc tả không nói, ghi `[Cần bổ sung: hành vi khi bị từ chối]`.

---

## 6. Error Guessing — Đoán lỗi

**Ý tưởng:** dùng kinh nghiệm để thêm case ngoài các kỹ thuật hệ thống. Chạy sau cùng, như "lưới an toàn". Đánh dấu nguồn để dễ truy vết (ví dụ tag `EG`).

**Danh sách gợi ý (chọn theo tính năng, không dùng máy móc)**

| Nhóm | Ý tưởng case |
|---|---|
| Thao tác lặp | Bấm đúp nút gửi/thanh toán; gửi form hai tab cùng lúc; F5 sau khi submit (gửi lại form) |
| Điều hướng | Back/Forward giữa luồng nhiều bước; mở link sâu khi chưa đăng nhập; đóng tab giữa chừng |
| Mạng | Mất mạng/timeout giữa lúc submit; mạng chậm; server trả 500; phản hồi trễ khiến người dùng bấm lại |
| Phiên | Phiên hết hạn khi đang điền form; đăng nhập hai thiết bị; đăng xuất ở tab khác |
| Dữ liệu văn bản | Chuỗi rỗng, chỉ khoảng trắng, rất dài; ký tự đặc biệt `' " < > & %`; tiếng Việt có dấu, emoji; chuỗi dạng `<script>`/SQL (kiểm tra được escape, không phải tấn công thật vào hệ thống không phải của bạn) |
| Số/ngày | 0, âm, số rất lớn, thập phân, định dạng dấu `,` `.`; ngày 29/02, múi giờ, ngày quá khứ/tương lai |
| File | File 0 byte, quá dung lượng, sai đuôi/MIME, tên file có ký tự đặc biệt/rất dài, upload lại cùng file |
| Môi trường | Trình duyệt khác, màn hình nhỏ, tắt JavaScript/cookie, zoom 200% |
| Dữ liệu tồn tại | Dữ liệu trùng (email đã đăng ký), bản ghi đã bị xoá nhưng link còn, danh sách rỗng, danh sách rất lớn |
| Đồng thời | Hai người sửa cùng bản ghi; xoá bản ghi trong lúc người khác đang xem |

**Cách ghi test case:** vẫn đủ cột chuẩn; Title nêu tình huống; Priority theo rủi ro thực (không mặc định P3); đa số là `Manual` hoặc `Auto (API)`.

---

## Quy trình tổng hợp cho một yêu cầu

1. Xác định loại yêu cầu → chọn kỹ thuật từ bảng "Chọn nhanh".
2. Sinh case theo kỹ thuật chính, rồi kỹ thuật kết hợp.
3. Thêm permission case nếu yêu cầu có liên quan đến vai trò.
4. Thêm 1–3 case Error Guessing đặc thù.
5. Loại case trùng (cùng vùng tương đương, cùng kết quả) để bảng gọn nhưng vẫn phủ.
6. Gắn Req/UC ID, Priority, Execution Type; đưa vào RTM.

## Phát hiện trùng lặp / thừa

- Hai case cùng Req, cùng vùng EP, cùng kết quả → giữ một.
- Case chỉ khác dữ liệu nhưng cùng luồng → cân nhắc gộp thành một case có nhiều dòng Test Data (data-driven), nhất là với `Auto`.
- Không cắt case P0/P1 chỉ vì bảng dài.
