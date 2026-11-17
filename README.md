# GMaps Media Viewer

Lấy **ảnh gốc** (`=s0`), **video gốc** (`=dv`, mp4) và **bình luận kèm ảnh** của một địa điểm Google Maps.
Ảnh ở cột trái (nhóm theo bình luận), video ở cột phải (kèm ngày đăng). Click để xem, tick nhiều mục để copy
các link cách nhau dấu phẩy.

**Dùng ngay:** https://huynguyenkhac17.github.io/gmaps-media-viewer/

Yêu cầu: Chrome hoặc Edge trên máy tính. Không cần cài extension hay phần mềm.

## Cách dùng

1. Mở trang trên, kéo nút đỏ **📍 Lấy ảnh Maps** lên thanh dấu trang (Ctrl+Shift+B để hiện thanh).
   Không kéo được thì bấm **Copy code bookmark**, tạo bookmark mới và dán vào ô URL.
2. Mở một địa điểm trên Google Maps (đang ở trang thông tin của địa điểm), rồi bấm bookmark đó.
3. Chờ khung nhỏ ở góc phải chạy xong 3 bước:
   - **Bài đánh giá**: cuộn hết, mở "Thêm", lấy tên, số sao, nội dung và ảnh của từng bình luận có ảnh
     (bỏ phản hồi của chủ quán);
   - **Thư viện → tab Tất cả**: lấy mọi ảnh, kể cả ảnh không kèm bình luận; ô gắn nhãn "Video" là video;
   - **Thư viện → tab Video**: bổ sung video và mở từng video để đọc ngày đăng.
4. Trang kết quả tự mở. Nếu trình duyệt chặn cửa sổ bật lên, bấm **Mở kết quả** trên khung nhỏ.

Ba nút trên khung nhỏ:

| Nút | Tác dụng |
| --- | --- |
| **Bỏ qua bước** | Kết thúc bước đang chạy, làm tiếp bước sau (ví dụ địa điểm quá nhiều bình luận) |
| **Gửi ngay** | Dừng tất cả, gửi những gì đã lấy được. Các bước chưa chạy sẽ **không có dữ liệu** |
| **Huỷ** | Dừng và không gửi gì |

Mỗi lần bấm bookmark **thay** danh sách cũ, nên các địa điểm không chồng lên nhau.
Cũng có thể dán thẳng vào ô nhập: link Maps của một ảnh/video, link lh3, hoặc cả danh sách URL.

## Khi kết quả thiếu hoặc sai

Dòng trạng thái ở góc phải trên cùng ghi lại bookmark đã thấy gì, ví dụ:

`61 mục · Bình luận: duyệt 60, có ảnh 20 · Tất cả: 58 ảnh, 3 video · Video: 3 · Ảnh bình luận có trong thư viện: 51/51`

Bấm vào dòng đó để copy rồi gửi cho người phụ trách. Cách đọc:

- `Đã bấm Gửi ngay/Bỏ qua ở bước …`: thiếu dữ liệu là do dừng sớm.
- `Tất cả: 0 ảnh` hoặc `Không mở được thư viện ảnh`: Maps không mở/nạp kịp thư viện; chạy lại.
- `N ô chưa nạp`: còn N ô ảnh Maps chưa tải xong thumbnail.
- `Ảnh bình luận có trong thư viện: 0/N`: ảnh trong bình luận và trong thư viện dùng hai kiểu link khác nhau
  (trang xem đã gộp theo mã ảnh; nếu vẫn thấy ảnh trùng thì báo lại).

Trang báo **bookmark là bản cũ**: xoá bookmark đó và kéo lại nút mới. Code nằm ngay trong bookmark nên bản cũ không tự cập nhật.

## Mạng chậm

Bookmark không dùng thời gian chờ cố định: khi danh sách chưa hiện gì nó chờ tối đa 20 giây; ở cuối danh sách
nó chờ ít nhất 8 giây, hoặc gấp 3 lần thời gian đợt trước cần để nạp (tối đa 30 giây). Ô ảnh chưa kịp có
thumbnail được quay lại lần nữa. Đổi lại, mỗi bước mất thêm khoảng 8 giây ở cuối.

## Giới hạn đã biết

- Thời gian chạy tỉ lệ với số bình luận: khoảng 5 bình luận mỗi giây, tức vài phút cho địa điểm có trên 1.000 bình luận.
- Bình luận có nhiều ảnh hơn số Maps hiển thị (ô `+N`): các ảnh ẩn chỉ lấy được từ thư viện, không gắn được vào bình luận đó.
- Ngày đăng chỉ có độ chính xác tháng/năm (Maps không hiện ngày), ghi thành `15/mm/yyyy`; với "3 tuần trước"
  thì tính lùi từ lúc quét. Rê chuột lên dòng ngày để xem chữ gốc.
- Bookmark dựa vào cấu trúc trang Google Maps (`data-review-id`, `data-photo-index`, nhãn tab tiếng Việt/Anh).
  Google đổi giao diện thì phải sửa bookmark.
- Điện thoại không dùng được bookmark; trang xem thì vẫn mở được.

## Dữ liệu đi đâu

Không có server. Bookmark chạy trong tab Maps của chính bạn, nén kết quả vào phần `#z=…` của địa chỉ
(phần này trình duyệt không gửi lên máy chủ nào) rồi mở trang xem. Trang xem chỉ lưu trong `localStorage`
của trình duyệt bạn. Trang xem coi dữ liệu trong link là không tin cậy: chỉ nhận mã ảnh đúng định dạng và
hiển thị mọi chữ dưới dạng văn bản thuần.

Ảnh, video và bình luận thuộc về người đăng và chịu điều khoản của Google Maps; công cụ chỉ thu gom thứ
Maps đang hiển thị cho bạn. Việc dùng lại nội dung đó là trách nhiệm của người dùng.

## Cách hoạt động (cho người bảo trì)

- **Một file** `index.html`: trang xem + hàm `grab()` được nhúng nguyên văn vào bookmark.
  Sửa `grab()` thì tăng `BM_VER` để bookmark cũ nhận cảnh báo cập nhật. Trong `grab()` không dùng
  `innerHTML`/`eval` (Maps bật Trusted Types) và chỉ dùng chú thích `/* */`.
- **Vì sao cần bookmark**: trình duyệt chặn trang khác đọc dữ liệu Google Maps (CORS), còn bookmark chạy
  ngay trong tab Maps nên đọc được DOM.
- **Chỉ đọc đúng danh sách đang mở**: Maps là SPA, DOM và `performance` còn giữ ảnh của địa điểm đã xem trước
  đó; bookmark chỉ đọc các ô `[data-photo-index]` của thư viện và các khối `[data-review-id]` đang hiển thị,
  bỏ qua hàng tab (tab có ảnh đại diện riêng).
- **Ảnh hay video**: ô thư viện có `aria-label="Video"`. Trang xem kiểm tra lại từng video bằng hai cách độc lập
  (`fetch <id>=dv` có chuyển hướng sang mp4 không; thẻ `<video>` có đọc được metadata không) và chỉ chuyển
  một mục sang cột Ảnh khi cả hai đều nói không phải video. Mạng treo thì giữ nguyên nhãn của bookmark.
- **Kiểm thử** (cần Node, Python, Playwright và Chrome):

  ```
  node tests/core.mjs && node tests/dates.mjs
  python3 tests/viewer.py                      # trang xem: dữ liệu giả mạo, cảnh báo bản cũ, bố cục
  python3 tests/flow.py                        # toàn bộ luồng trên trang Maps giả lập
  NET=slow python3 tests/flow.py               # mạng chậm
  CLS=none PREFIX=1 DIRECT=1 python3 tests/flow.py
  PRESS=skip python3 tests/flow.py ; PRESS=send python3 tests/flow.py
  ```

  Trang Maps giả lập trong `tests/flow.py` dựng theo cấu trúc Maps thật đã quan sát được; nó không thay
  được việc chạy thử trên Maps thật sau mỗi lần sửa.
