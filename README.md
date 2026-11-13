# GMaps Media Viewer

Xem và copy link **ảnh gốc** (`=s0`) và **video gốc** (`=dv`, mp4) của một địa điểm Google Maps.
Ảnh ở cột trái, video ở cột phải; click để xem, tick nhiều mục để copy các link cách nhau dấu phẩy.

**Dùng ngay:** https://huynguyenkhac17.github.io/gmaps-media-viewer/

## Cách dùng

1. Kéo nút **📍 Lấy ảnh Maps** trên trang lên thanh dấu trang (chỉ là bookmark, không cần cài extension).
   Không kéo được thì bấm **Copy code bookmark**, tạo bookmark mới và dán vào ô URL.
2. Mở địa điểm trên Google Maps, mở mục **Ảnh/Video**, cuộn hết danh sách để Maps nạp đủ.
3. Bấm bookmark: trang này mở ra với toàn bộ ảnh và video.

Cũng có thể dán thẳng vào ô nhập: link Maps của ảnh/video, link lh3, CSS `background-image`, hoặc danh sách URL.

## Vì sao cần bookmark

Trang chạy trên GitHub Pages (web tĩnh). Trình duyệt chặn trang khác đọc dữ liệu Google Maps (CORS),
nên một link địa điểm chỉ cho được ảnh nằm sẵn trong link. Bookmark chạy ngay trên tab Maps của bạn
(IP và phiên của chính bạn) để gom link lh3 trong DOM, rồi chuyển sang trang này qua `#p=…`. Không có server, không lưu gì ngoài `localStorage` của trình duyệt bạn.

## Phân biệt ảnh / video

Ảnh và video Maps dùng chung kiểu id lh3. Trang gọi `<id>=dv` với `redirect: 'manual'`:
video trả 302 sang mp4 gốc (`opaqueredirect`), ảnh trả lỗi → xếp vào cột ảnh.
