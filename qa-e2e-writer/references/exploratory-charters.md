# Exploratory Charters & Manual Run Scripts

Dùng cho case `Manual` và để "phá app" có chủ đích. Mọi mục dưới là **gợi ý** — chọn theo tính năng thực tế, không áp dụng máy móc. Kết quả chỉ ghi khi người dùng (hoặc bạn, nếu thực sự chạy được) đã quan sát thật.

## 1. Kịch bản bấm test nhanh (Manual Run Script)

Gom case theo module/luồng để giảm đổi ngữ cảnh. Mẫu:

```markdown
### Nhóm: <Module / luồng> — chuẩn bị: <tài khoản, dữ liệu, URL: [Cần bổ sung nếu chưa biết]>

| # | TC ID | Bước | Dữ liệu | Kết quả mong đợi | Kết quả (Pass/Fail/Blocked) | Ghi chú/Bằng chứng |
|---|---|---|---|---|---|---|
| 1 | TC-LOGIN-001 | 1. Mở /login 2. Nhập ... 3. Bấm Đăng nhập | ... | ... | ☐ | |
```

Quy tắc: sắp xếp để case tạo dữ liệu chạy trước case dùng dữ liệu đó, nhưng vẫn ghi pre-condition để từng case chạy độc lập được; đặt P0 lên đầu; ô kết quả để trống cho người dùng điền.

## 2. Charter thăm dò (Session-Based)

Mẫu một charter (30–60 phút):

```markdown
**Charter:** Khám phá <khu vực> bằng <cách/dữ liệu> để tìm <loại rủi ro>
**Thời lượng:** 45 phút | **Vai trò dùng:** <role> | **Môi trường:** [Cần bổ sung]
**Ghi lại:** lỗi tìm thấy · câu hỏi · ý tưởng test mới · khu vực chưa kịp xem
```

Ví dụ charter (minh hoạ):
- Khám phá form đăng ký bằng dữ liệu biên và ký tự đặc biệt để tìm lỗi validate/lưu sai.
- Khám phá luồng thanh toán bằng thao tác lặp và gián đoạn để tìm trùng đơn/lệch trạng thái.
- Khám phá màn hình quản trị bằng tài khoản quyền thấp để tìm lỗ hổng phân quyền.

Kết thúc phiên: tóm tắt lỗi (→ `qa-defect-writer`), điều chưa xác định (→ hỏi), vùng còn rủi ro.

## 3. Danh mục "phá app"

### Thao tác lặp & thời điểm
- **Double-click / bấm liên tục** nút gửi, thanh toán, tạo mới → có tạo trùng bản ghi/trừ tiền hai lần không? Nút có bị vô hiệu khi đang xử lý không?
- Gửi form từ **hai tab** cùng lúc; mở cùng bản ghi ở hai tab rồi sửa/xoá.
- Bấm Enter nhiều lần trong ô nhập.

### Điều hướng
- **Back / Forward** sau khi submit, giữa luồng nhiều bước, sau khi đăng xuất (có xem lại được trang riêng tư từ cache không?).
- **Reload (F5)** giữa luồng: mất dữ liệu đang nhập? Gửi lại form có tạo trùng?
- Đóng tab/trình duyệt giữa chừng rồi mở lại; mở link sâu (deep link) khi chưa đăng nhập; sửa ID trên URL.

### Mạng & máy chủ
- **Mất mạng** giữa lúc submit (tắt Wi-Fi hoặc chế độ offline của DevTools): thông báo gì, dữ liệu có mất, có thử lại an toàn không?
- **Mạng chậm** (throttling "Slow 3G"): spinner, timeout, người dùng bấm lại.
- Phản hồi lỗi từ server (500/timeout) → thông báo có thân thiện, không lộ chi tiết kỹ thuật nhạy cảm?

### Phiên & phân quyền
- Phiên hết hạn khi đang điền form dài; đăng nhập hai thiết bị; đăng xuất ở tab khác rồi thao tác ở tab này.
- Truy cập trực tiếp URL/chức năng của vai trò cao bằng tài khoản thấp; đổi ID tài nguyên của người khác.

### File upload/download
- File **nặng** vượt giới hạn, đúng bằng giới hạn; file **0 byte**; **sai định dạng** (đổi đuôi `.exe` thành `.jpg`); tên file rất dài/có dấu/ký tự đặc biệt/trùng tên; upload nhiều file; huỷ upload giữa chừng; mất mạng khi đang upload.

### Dữ liệu nhập
- Rỗng, chỉ khoảng trắng, rất dài; `' " < > & % \`; tiếng Việt có dấu, emoji, ký tự RTL; dán văn bản có xuống dòng; số âm/0/rất lớn/thập phân; ngày 29/02, múi giờ, ngày quá khứ/tương lai.
- Chuỗi dạng script/HTML/SQL để kiểm tra hệ thống **của dự án** có escape đúng. Không thử vào hệ thống không thuộc quyền kiểm thử.

### Giao diện & môi trường
- Thu nhỏ cửa sổ/màn hình điện thoại, zoom 200%, xoay màn hình; trình duyệt khác; tắt cookie/JavaScript nếu hỗ trợ; chế độ tối; bàn phím (Tab/Enter/Esc) và screen reader cơ bản.

### Dữ liệu tồn tại
- Dữ liệu trùng (email đã đăng ký); bản ghi đã xoá nhưng link còn; danh sách rỗng/rất dài; xoá thứ đang được tham chiếu.

## 4. Cách ghi nhận khi phát hiện bất thường

1. Dừng tại thời điểm xảy ra; ghi lại bước chính xác dẫn tới lỗi.
2. Chụp màn hình/log/Network tab (HAR) nếu có; ghi giờ xảy ra.
3. Thử tái hiện ≥ 2 lần; ghi tỉ lệ (ví dụ "2/3 lần") — không nói "luôn luôn" khi chưa thử.
4. Ghi môi trường **thật** đang dùng (không nhớ thì hỏi/ghi `[Cần bổ sung]`).
5. Chuyển cho `qa-defect-writer`.

## 5. Mẫu hỏi người dùng sau khi chạy tay

> Bạn chạy xong nhóm "<Module>" chưa? Cho tôi biết với mỗi TC: Pass / Fail / Blocked, và với Fail thì hiện tượng + ảnh/log nếu có. Case nào chưa chạy tôi sẽ để `Not Run`.
