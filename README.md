# GMaps Media Viewer

Xem và copy link **ảnh gốc** (`=s0`) và **video gốc** (`=dv`, mp4) của một địa điểm Google Maps.
Ảnh ở cột trái, video ở cột phải; click để xem, tick nhiều mục để copy các link cách nhau dấu phẩy.

**Dùng ngay:** https://huynguyenkhac17.github.io/gmaps-media-viewer/

## Cách dùng

1. Kéo nút **📍 Lấy ảnh Maps** trên trang lên thanh dấu trang (chỉ là bookmark, không cần cài extension).
   Không kéo được thì bấm **Copy code bookmark**, tạo bookmark mới và dán vào ô URL.
2. Mở địa điểm trên Google Maps rồi bấm bookmark. Bookmark tự:
   - mở tab **Bài đánh giá**, cuộn hết, bấm "Thêm" để lấy đủ nội dung bình luận kèm ảnh
     (tên, số sao, nội dung, các ảnh của bình luận đó; bỏ phản hồi của chủ quán);
   - quay về **Tổng quan**, mở thư viện ảnh → tab **Tất cả**: lấy mọi ảnh, kể cả ảnh không kèm bình luận
     (ô có `aria-label="Video"` được tính là video);
   - tab **Video**: bổ sung video và đọc ngày đăng.
   Khung nhỏ góc phải có **Gửi ngay** (không chờ cuộn hết) và **Huỷ**.
3. Cột Ảnh nhóm theo bình luận; cột Video có ngày đăng (và bình luận nếu video nằm trong một bình luận).
   Mỗi lần bấm bookmark **thay** danh sách cũ, nên các địa điểm không chồng lên nhau.

Ảnh không kèm bình luận nằm trong nhóm riêng. Ảnh đại diện của các tab thư viện (Mới nhất, Thực đơn…) được bỏ qua.
Bình luận có nhiều ảnh hơn số Maps hiển thị (ô `+N`) được đánh dấu trên trang.
Dữ liệu được nén (deflate) trong `#z=…` của URL; dòng trạng thái góc phải ghi bookmark đã thấy gì để dễ báo lỗi.

Cập nhật bookmark: xoá bookmark cũ, kéo lại nút mới trên trang.

Cũng có thể dán thẳng vào ô nhập: link Maps của ảnh/video, link lh3, CSS `background-image`, hoặc danh sách URL.

## Vì sao cần bookmark

Trang chạy trên GitHub Pages (web tĩnh). Trình duyệt chặn trang khác đọc dữ liệu Google Maps (CORS),
nên một link địa điểm chỉ cho được ảnh nằm sẵn trong link. Bookmark chạy ngay trên tab Maps của bạn
(IP và phiên của chính bạn) để gom link lh3 trong DOM, rồi chuyển sang trang này qua `#p=…`. Không có server, không lưu gì ngoài `localStorage` của trình duyệt bạn.

## Phân biệt ảnh / video

Bookmark quét riêng tab **Video** của thư viện ảnh, nên biết ngay id nào là video, không cần request nào thêm.
Với link dán tay (hoặc khi bấm *Gửi ngay* trước khi quét tab Video), trang gọi `<id>=dv` với
`redirect: 'manual'`: video trả 302 sang mp4 gốc (`opaqueredirect`), ảnh trả lỗi → cột ảnh.

## Ngày đăng video

Maps chỉ hiện ngày đăng khi một video đang được mở, và chỉ ở dạng tháng/năm (`Tháng 5 2024`, `May 2024`)
hoặc tương đối (`3 tuần trước`). Bookmark lần lượt mở từng video trong tab Video, đọc dòng ngày vừa xuất hiện,
rồi trang xem quy đổi thành **`15/mm/yyyy`** (ngày cố định là 15; thời gian tương đối tính lùi từ lúc quét).
Rê chuột lên dòng ngày để xem chữ gốc Maps ghi. Video dán tay thì không có ngày.

## Chỉ quét ô của thư viện ảnh

Google Maps là SPA: chuyển địa điểm không tải lại trang, nên DOM và `performance` vẫn giữ ảnh của các
địa điểm đã xem trước đó. Bookmark chỉ đọc các ô `[data-photo-index]` của thư viện đang mở để không lẫn.
