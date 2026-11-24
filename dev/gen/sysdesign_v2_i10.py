# Thiết kế hệ thống phía mobile · I10: ảnh và tệp lớn (Phần 2)
# Nguồn: Android Loading large bitmaps (inJustDecodeBounds, inSampleSize, ví dụ 2048×1536 → 0,75 MB thay vì 12 MB, khuyên thư viện ảnh);
# Bitmap.Config (ARGB_8888 4 byte, RGB_565 2 byte, HARDWARE); UIDT (Android 14); Alex Xu tập 1 ch.14 (chia khúc video), ch.15 (upload
# tiếp tục được, delta sync); IETF draft-ietf-httpbis-resumable-upload-16 (POST/Location, HEAD/Upload-Offset, PATCH). Đọc 2026-11-24.

SEC_ORDER = {'i10': ['hook', 'memory', 'sample', 'resumable', 'background', 'bugs', 'ex']}


def add(a):
    def B(ch, sec, n, field, vi, en=None):
        a('%s.sec.%s.b.%02d.%s' % (ch, sec, n, field), vi, vi if en is None else en)

    # ---------- mô phỏng 1: bitmap ----------
    a('preset.bitmap', 'Thiết kế hệ thống · RAM của lưới ảnh', 'System design · memory of a photo grid')
    m = lambda k, vi, en=None: a('m.bitmap.' + k, vi, en)
    m('title', 'Giải mã ảnh gốc, hay giải mã theo kích thước hiển thị', 'Decode the original, or decode for the display size')
    m('overview', 'Màn "Ảnh tổn thương da" hiện lưới 12 ảnh, mỗi ô 90 dp (đơn vị độc lập với mật độ màn hình), tức 270 px trên máy mật độ 3x (1 dp = 3 px). Mỗi ảnh chụp từ camera là 4000 × 3000 điểm ảnh, tệp JPEG chỉ vài MB. Hai cách: giải mã thẳng ảnh gốc; hoặc đọc kích thước trước, chọn inSampleSize (hệ số thu nhỏ khi giải mã) rồi giải mã bản nhỏ. Giới hạn heap (vùng RAM cấp cho app) 256 MiB là minh họa (MiB = 1.048.576 byte; MB trong chương này là 1.000.000 byte); con số thật tùy máy.',
      'The "Skin lesion photos" screen shows a grid of 12 photos, each cell 90 dp (a density-independent unit), i.e. 270 px on a 3x density phone (1 dp = 3 px). Each camera photo is 4000 × 3000 pixels, its JPEG file only a few MB. Two ways: decode the original directly; or read the size first, pick inSampleSize (the shrink factor used when decoding) and decode a smaller copy. The 256 MiB heap limit (the slice of RAM an app is given) is illustrative (MiB = 1,048,576 bytes; MB in this chapter means 1,000,000 bytes); the real figure depends on the device.')
    m('wrapup', 'RAM của một ảnh đã giải mã là rộng × cao × số byte mỗi điểm ảnh, không phải kích thước tệp. Ảnh 4000 × 3000 ở ARGB_8888 (4 byte mỗi điểm ảnh: trong suốt, đỏ, lục, lam) tốn khoảng 45,8 MiB dù tệp JPEG chỉ vài MB; mười hai ảnh như vậy vượt heap. Đọc kích thước trước, giải mã với inSampleSize 8 cho ảnh 500 × 375, khoảng 0,72 MiB mỗi ảnh. Thực tế, thư viện ảnh làm việc này theo kích thước view (thành phần hiển thị ảnh) và có cache sẵn.',
      'A decoded image costs width × height × bytes per pixel, not the file size. A 4000 × 3000 photo in ARGB_8888 (4 bytes per pixel: alpha, red, green, blue) takes about 45.8 MiB though its JPEG is a few MB; twelve of them exceed the heap. Read the size first and decode with inSampleSize 8 for a 500 × 375 image, about 0.72 MiB each. In practice an image library does this for the view size (the component that shows the image) and caches for you.')
    m('simp.1', 'Kích thước ảnh, 12 ô, mật độ 3x, giới hạn heap 256 MiB là minh họa; app thật còn cache, ảnh ở bộ nhớ đồ họa (bộ nhớ của GPU, chip vẽ hình), và RAM của chính màn hình.', 'The photo size, 12 cells, 3x density and the 256 MiB heap limit are illustrative; real apps also have caches, images in graphics memory (the GPU\'s own memory), and the screen\'s own memory.')
    m('simp.2', 'Mô phỏng chỉ tính ảnh giải mã ở ARGB_8888, còn Android có cấu hình khác tốn ít byte hơn mỗi điểm ảnh, và thư viện ảnh lo cả cache lẫn việc hủy tải. Hàm calculateInSampleSize lấy từ tài liệu Android đọc ngày 2026-11-24. Chương không bàn cấu hình thư viện ảnh hay nén video.', 'The simulation counts only an image decoded in ARGB_8888, while Android has other configurations that take fewer bytes per pixel, and an image library also handles caching and cancelling loads. calculateInSampleSize comes from the Android docs read on 2026-11-24. The chapter does not cover image library configuration or video compression.')
    m('ctl.hint', 'Đổi cách giải mã rồi đi lại; so tổng RAM ở bước 4.', 'Switch the decoding approach and walk again; compare the total memory at step 4.')
    m('ctl.case', 'Cách giải mã', 'Decoding approach')
    for k, vi, en in [('full', 'giải mã thẳng ảnh gốc', 'decode the original'), ('sampled', 'đọc kích thước, inSampleSize', 'read the size, inSampleSize')]:
        m('ctl.case.' + k, vi, en)
    m('diagramTitle', 'Tệp ảnh, bộ giải mã, heap, màn hình', 'Image file, decoder, heap, screen')
    m('diagramDesc', 'Tệp nén trên đĩa được giải mã thành bitmap (ảnh đã giải mã, mỗi điểm ảnh một ô nhớ) trong heap rồi vẽ lên màn hình', 'The compressed file on disk is decoded into a bitmap (a decoded image, one memory cell per pixel) in the heap and drawn on screen')
    for k, vi, en in [('file', 'Tệp JPEG', 'JPEG file'), ('decoder', 'BitmapFactory', 'BitmapFactory decoder'), ('heap', 'Heap của app', 'App heap'), ('screen', 'Lưới 12 ô', 'Grid of 12 cells')]:
        m('n.' + k, vi, en)
    m('met.one', 'MiB một ảnh', 'MiB per photo'); m('met.total', 'MiB đang giữ', 'MiB held'); m('met.oom', 'Hết RAM', 'Out of memory')
    a('cap.bitmap', 'Tệp ảnh bên trái được giải mã vào heap rồi lên lưới ảnh bên phải.', 'The image file on the left is decoded into the heap, then onto the grid on the right.')
    S = [
        ('full', 's1', 'Mở tệp ảnh, không xem kích thước trước', 'Open the image file without checking its size', 'Tệp JPEG chỉ vài MB, nên trông có vẻ vô hại.', 'The JPEG is only a few MB, so it looks harmless.'),
        ('full', 's2', 'inSampleSize = 1: giải mã đủ 4000 × 3000', 'inSampleSize = 1: decode all 4000 × 3000', 'Mặc định giải mã mọi điểm ảnh, dù ô chỉ có 270 px.', 'By default every pixel is decoded, though the cell is only 270 px.'),
        ('full', 's3', 'Một ảnh: 4000 × 3000 × 4 byte ≈ 45,8 MiB', 'One photo: 4000 × 3000 × 4 bytes ≈ 45.8 MiB', 'RAM tính theo số điểm ảnh, không theo kích thước tệp nén.', 'Memory follows the pixel count, not the compressed file size.'),
        ('full', 's4', '12 ảnh: khoảng 549 MiB, vượt giới hạn heap: OutOfMemoryError', '12 photos: about 549 MiB, over the heap limit: OutOfMemoryError', 'Màn hình chỉ cần 270 px mỗi ô, nhưng app giữ cả ảnh gốc. OutOfMemoryError là lỗi app dùng hết RAM được cấp.', 'The screen needs only 270 px per cell, but the app holds the originals. OutOfMemoryError means the app used up the RAM it was given.'),
        ('sampled', 's1', 'inJustDecodeBounds = true: đọc được 4000 × 3000, chưa cấp phát gì', 'inJustDecodeBounds = true: reads 4000 × 3000, allocates nothing', 'inJustDecodeBounds = true bảo bộ giải mã chỉ đọc kích thước. Bước đọc kích thước không tạo bitmap.', 'inJustDecodeBounds = true tells the decoder to read only the size. Reading the size creates no bitmap.'),
        ('sampled', 's2', 'Chọn inSampleSize = 8 cho ô 270 px', 'Pick inSampleSize = 8 for a 270 px cell', 'Nhân đôi chừng nào nửa kích thước chia cho nó vẫn còn lớn hơn ô; xem bảng vòng lặp.', 'Keep doubling while half the size divided by it still covers the cell; see the loop table.'),
        ('sampled', 's3', 'Giải mã ra 500 × 375: khoảng 0,72 MiB', 'Decode to 500 × 375: about 0.72 MiB', 'Vẫn lớn hơn ô 270 px nên ảnh không bị mờ.', 'Still larger than the 270 px cell, so it does not look blurry.'),
        ('sampled', 's4', '12 ảnh: khoảng 8,6 MiB', '12 photos: about 8.6 MiB', 'Ít hơn khoảng 64 lần so với giữ ảnh gốc.', 'About 64 times less than holding the originals.'),
    ]
    for case, k, tv, te, xv, xe in S:
        sid = case + '.' + k
        m('s.%s.title' % sid, tv, te); m('s.%s.explain' % sid, xv, xe); m('ev.' + sid, tv, te)
    for k, vi, en in [
        ('try', 'Đi hết bốn bước của mỗi cách; ở bước 4 so tổng RAM với giới hạn heap.', 'Walk all four steps of each approach; at step 4 compare the total with the heap limit.'),
        ('full.s2', 'Tài liệu Android: ảnh thường lớn hơn nhiều so với chỗ hiện nó, và giải mã ảnh lớn hơn cần làm tốn RAM vô ích. [[src:ax-load-bitmap]]', 'Android docs: images are often far larger than where they are shown, and decoding more than needed wastes memory. [[src:ax-load-bitmap]]'),
        ('full.s3', 'Bitmap.Config: ARGB_8888 giữ mỗi điểm ảnh trong 4 byte. [[src:ax-bitmap-config]]', 'Bitmap.Config: ARGB_8888 stores each pixel in 4 bytes. [[src:ax-bitmap-config]]'),
        ('full.s4', 'Ví dụ của tài liệu: ảnh 2048 × 1536 tốn khoảng 12 MiB; giải mã với inSampleSize 4 chỉ còn khoảng 0,75 MiB. [[src:ax-load-bitmap]]', 'The docs\' example: a 2048 × 1536 image takes about 12 MiB; decoded with inSampleSize 4 it is about 0.75 MiB. [[src:ax-load-bitmap]]'),
        ('sampled.s2', 'Tài liệu: bộ giải mã làm tròn inSampleSize xuống lũy thừa của 2, nên hàm mẫu chỉ nhân đôi. [[src:ax-load-bitmap]]', 'Docs: the decoder rounds inSampleSize down to a power of two, so the sample function only doubles. [[src:ax-load-bitmap]]'),
        ('sampled.s3', 'Muốn đúng 270 px thì thu nhỏ thêm sau khi giải mã; thư viện ảnh làm sẵn bước này.', 'For exactly 270 px, scale further after decoding; image libraries do this step for you.'),
        ('sampled.s4', 'Tài liệu khuyên dùng thư viện ảnh (Glide; ngoài ra Coil, Picasso, Fresco) thay vì tự viết; chúng giải mã theo kích thước view và cache. [[src:ax-load-bitmap]]', 'The docs recommend an image library (Glide; also Coil, Picasso, Fresco) over writing this yourself; they decode for the view size and cache. [[src:ax-load-bitmap]]')]:
        m('co.' + k, vi, en)

    # ---------- mô phỏng 2: upload ----------
    a('preset.upload', 'Thiết kế hệ thống · upload video 200 MB', 'System design · uploading a 200 MB video')
    u = lambda k, vi, en=None: a('m.upload.' + k, vi, en)
    u('title', 'Một request 200 MB, hay upload tiếp tục được theo khúc', 'One 200 MB request, or a resumable upload in chunks')
    u('overview', 'Người bệnh gửi video 200 MB quay vết thương cho bác sĩ, trên mạng di động chập chờn. Kết nối đứt khi đã gửi 195 MB. Hai cách: một request duy nhất; hoặc upload tiếp tục được theo khúc 10 MB, kiểu dự thảo "Resumable Uploads for HTTP" của IETF (tổ chức soạn chuẩn Internet; dự thảo là bản chưa thành chuẩn): tạo tài nguyên upload (một địa chỉ trên server đại diện cho lần upload này), hỏi server đã nhận tới đâu, gửi tiếp từ đó.',
      'A patient sends a 200 MB video of a wound to the doctor over a flaky mobile network. The connection drops after 195 MB. Two ways: a single request; or a resumable upload in 10 MB chunks, in the style of the draft "Resumable Uploads for HTTP" from the IETF (the body that writes Internet standards; a draft is not yet a standard): create an upload resource (an address on the server standing for this upload), ask the server how far it got, continue from there.')
    u('wrapup', 'Một request lớn là tất cả hoặc không có gì: đứt ở 95% là mất 195 MB và phải gửi lại từ byte 0, tổng 395 MB. Upload tiếp tục được tách việc "server đã có gì" khỏi kết nối: app giữ địa chỉ tài nguyên upload, sau khi đứt hỏi Upload-Offset (số byte server đã có) rồi gửi tiếp, chỉ mất phần đang gửi dở. Việc này còn phải sống qua khi app ra nền, nên chạy trong WorkManager (công cụ chạy việc nền của Android) hay job UIDT (job truyền dữ liệu do người dùng khởi động, mô tả ở mục cuối).',
      'One big request is all or nothing: cut at 95% loses 195 MB and restarts from byte 0, 395 MB in total. A resumable upload separates "what the server has" from the connection: the app keeps the upload resource address, asks Upload-Offset (the bytes the server already has) after a drop and continues, losing only the part in flight. It also has to survive the app going to the background, so it runs in WorkManager (Android\'s tool for background work) or a UIDT job (a user-initiated data transfer job, described near the end).')
    u('simp.1', 'Kích thước 200 MB, khúc 10 MB và việc đứt ở 195 MB là minh họa. Server trong mô phỏng chỉ giữ các khúc trọn vẹn; theo dự thảo IETF, server có thể báo cả phần lẻ đã nhận.', 'The 200 MB size, 10 MB chunks and the drop at 195 MB are illustrative. The simulated server keeps only whole chunks; per the IETF draft, a server may report partial bytes received too.')
    u('simp.2', 'Giao thức trong mô phỏng theo dự thảo draft-ietf-httpbis-resumable-upload-16 (chưa là RFC nên có thể đổi); nhiều dịch vụ có giao thức riêng cùng ý tưởng. Chương không bàn xác thực hay nén video.', 'The protocol in the simulation follows draft-ietf-httpbis-resumable-upload-16 (not yet an RFC, so it may change); many services have their own protocol with the same idea. The chapter does not cover authentication or video compression.')
    u('ctl.hint', 'Đổi cách upload rồi đi lại; so MB đã gửi và MB phải gửi lại ở bước 4.', 'Switch the upload approach and walk again; compare MB sent and MB wasted at step 4.')
    u('ctl.case', 'Cách upload', 'Upload approach')
    for k, vi, en in [('whole', 'một request 200 MB', 'one 200 MB request'), ('resumable', 'tiếp tục được, khúc 10 MB', 'resumable, 10 MB chunks')]:
        u('ctl.case.' + k, vi, en)
    u('diagramTitle', 'App, mạng di động, server', 'App, mobile network, server')
    u('diagramDesc', 'App gửi tệp qua mạng di động tới server; mạng có thể đứt giữa chừng', 'The app sends the file over the mobile network to the server; the network can drop midway')
    for k, vi, en in [('net', 'Mạng di động', 'Mobile network'), ('server', 'Server nhận video', 'Upload server')]:
        u('n.' + k, vi, en)
    u('n.app', 'App, chạy trong WorkManager', 'App, running in WorkManager')
    u('met.sent', 'MB đã gửi (cộng dồn)', 'MB sent (running total)'); u('met.stored', 'MB server đã giữ', 'MB kept by the server'); u('met.waste', 'MB gửi phí', 'MB wasted')
    a('cap.upload', 'App bên trái gửi qua mạng di động ở giữa tới server bên phải.', 'The app on the left sends through the mobile network in the middle to the server on the right.')
    S = [
        ('whole', 's1', 'Bắt đầu POST cả 200 MB; đã gửi 100 MB', 'Start a POST of all 200 MB; 100 MB sent', 'Server chỉ giữ tệp khi nhận đủ request.', 'The server keeps the file only when the whole request arrives.'),
        ('whole', 's2', 'Đứt kết nối ở 195 MB', 'The connection drops at 195 MB', 'Request hỏng; server bỏ toàn bộ 195 MB đã nhận.', 'The request failed; the server discards all 195 MB received.'),
        ('whole', 's3', 'Thử lại từ byte 0; đã gửi lại 100 MB', 'Retry from byte 0; 100 MB resent', 'Mạng vẫn chập chờn; lần này cũng có thể đứt.', 'The network is still flaky; this attempt can drop too.'),
        ('whole', 's4', 'Lần hai xong: tổng đã gửi 395 MB cho tệp 200 MB', 'The second attempt completes: 395 MB sent for a 200 MB file', 'Gần gấp đôi dữ liệu di động, và thời gian chờ của người bệnh.', 'Nearly double the mobile data, and the patient\'s waiting time.'),
        ('resumable', 's1', 'POST tạo tài nguyên upload, nhận Location; gửi khúc 1 tới 10', 'POST creates an upload resource and returns Location; chunks 1 to 10 sent', 'Location là header trả về địa chỉ của tài nguyên upload. App lưu địa chỉ /uploads/abc xuống đĩa để dùng lại sau.', 'Location is the header that returns the upload resource\'s address. The app saves the address /uploads/abc to disk for later.'),
        ('resumable', 's2', 'Đứt kết nối giữa khúc 20, ở 195 MB', 'The connection drops in the middle of chunk 20, at 195 MB', 'Mười chín khúc đầu đã nằm trên server; chỉ khúc đang gửi dở bị mất.', 'The first nineteen chunks are on the server; only the chunk in flight is lost.'),
        ('resumable', 's3', 'Có mạng lại: HEAD /uploads/abc → Upload-Offset: 190 MB', 'Back online: HEAD /uploads/abc → Upload-Offset: 190 MB', 'HEAD là cách hỏi thông tin mà không tải nội dung. Server, không phải app, nói đã nhận tới đâu.', 'HEAD asks for information without transferring content. The server, not the app, says how far it got.'),
        ('resumable', 's4', 'PATCH từ 190 MB, khúc cuối: xong; tổng đã gửi 205 MB', 'PATCH from 190 MB, the last chunk: done; 205 MB sent in total', 'PATCH là phương thức HTTP gửi tiếp một phần vào tài nguyên đã có. Chỉ mất 5 MB gửi dở thay vì 195 MB.', 'PATCH is the HTTP method for sending one more part into an existing resource. Only the 5 MB in flight was wasted, instead of 195 MB.'),
    ]
    for case, k, tv, te, xv, xe in S:
        sid = case + '.' + k
        u('s.%s.title' % sid, tv, te); u('s.%s.explain' % sid, xv, xe); u('ev.' + sid, tv, te)
    for k, vi, en in [
        ('try', 'Đi hết bốn bước của mỗi cách; nhìn dãy ô các khúc và MB gửi phí.', 'Walk all four steps of each approach; watch the chunk strip and the MB wasted.'),
        ('whole.s2', 'Alex Xu nhận xét: upload thường chỉ hợp với tệp nhỏ; tệp lớn trên mạng dễ đứt cần upload tiếp tục được. [[src:book-xu1]]', 'Alex Xu notes: simple upload suits small files; large files on networks likely to drop need resumable upload. [[src:book-xu1]]'),
        ('whole.s3', 'Thử lại nguyên request không giúp: mỗi lần thử vẫn là tất cả hoặc không có gì.', 'Retrying the whole request does not help: each attempt is still all or nothing.'),
        ('whole.s4', 'Với người dùng trả tiền theo dung lượng, 195 MB gửi phí là tiền thật.', 'For users paying per megabyte, 195 MB wasted is real money.'),
        ('resumable.s2', 'Alex Xu cho biết: chia video thành khúc giúp upload nhanh và tiếp tục được khi lần trước lỗi. [[src:book-xu1]]', 'Alex Xu says: splitting a video into chunks makes uploads fast and resumable after a failure. [[src:book-xu1]]'),
        ('resumable.s3', 'Dự thảo IETF: sau khi đứt, client gửi HEAD tới tài nguyên upload và nhận Upload-Offset; offset không được giảm. [[src:ietf-resumable-upload]]', 'IETF draft: after an interruption, the client sends HEAD to the upload resource and gets Upload-Offset; the offset must not decrease. [[src:ietf-resumable-upload]]'),
        ('resumable.s4', 'Dự thảo IETF: gửi tiếp bằng PATCH kèm Upload-Offset, và Upload-Complete: ?1 ở phần cuối. Đây vẫn là Internet-Draft (dự thảo chưa thành chuẩn); nhiều dịch vụ có giao thức riêng cùng ý tưởng. [[src:ietf-resumable-upload]]', 'IETF draft: continue with PATCH carrying Upload-Offset, and Upload-Complete: ?1 on the last part. It is still an Internet-Draft (a draft that is not yet a standard); many services have their own protocol with the same idea. [[src:ietf-resumable-upload]]')]:
        u('co.' + k, vi, en)

    z = lambda k, vi, en=None: a('vz.' + k, vi, en)
    z('tab.bm', 'Bảng tính RAM ảnh', 'Image memory worksheet')
    z('bm.cap', 'Mỗi hàng hiện ra theo từng bước; hàng có viền là bước hiện tại.', 'Rows appear step by step; the outlined row is the current step.')
    z('bm.col.what', 'Đại lượng', 'Quantity'); z('bm.col.val', 'Giá trị', 'Value')
    for k, vi, en in [('src', 'Ảnh gốc', 'Original image'), ('need', 'Ô cần hiện (90 dp × mật độ 3)', 'Cell to fill (90 dp × density 3)'), ('s', 'inSampleSize', 'inSampleSize chosen'),
                      ('dec', 'Ảnh sau giải mã', 'Decoded image'), ('bpp', 'Byte mỗi điểm ảnh', 'Bytes per pixel'), ('one', 'RAM một ảnh', 'Memory per image'),
                      ('n', 'Số ảnh trên màn hình', 'Images on screen'), ('total', 'Tổng RAM', 'Total memory'), ('heap', 'Giới hạn heap (minh họa)', 'Heap limit (illustrative)')]:
        z('bm.r.' + k, vi, en)
    z('bm.bppv', '4 (ARGB_8888)', '4 bytes (ARGB_8888)')
    z('bm.mib', 'khoảng {n} MiB', 'about {n} MiB')
    z('bm.oom', 'vượt heap: OutOfMemoryError', 'over the heap: OutOfMemoryError')
    z('bm.lcap', 'Vòng lặp của calculateInSampleSize. Mỗi hàng hỏi: nếu nhân đôi s, ảnh (nửa rộng / s × nửa cao / s) còn từ 270 trở lên ở cả hai chiều không? Còn thì nhân đôi; không thì dừng và giữ s hiện tại.', 'The calculateInSampleSize loop. Each row asks: if s doubles, is the image (half width / s × half height / s) still 270 or more in both directions? If so, double; if not, stop and keep the current s.')
    for k, vi, en in [('s', 's', 'value of s'), ('half', 'ảnh nếu dùng 2s', 'image if 2s were used'), ('go', 'Kết quả', 'Result')]:
        z('bm.lcol.' + k, vi, en)
    z('bm.l.go', 'cả hai ≥ 270: nhân đôi s', 'both ≥ 270: double s'); z('bm.l.stop', 'có chiều < 270: dừng, giữ s này', 'one side < 270: stop, keep this s')
    z('bm.legend', 'Gạch đỏ: vượt giới hạn heap. Dấu ?: bước chưa tới.', 'Red hatched: over the heap limit. A ? means the step is not reached yet.')
    z('tab.up', 'Các khúc của tệp', 'File chunks')
    z('up.cap', 'Mỗi ô là một khúc 10 MB của video, đánh số 1 tới 20; mỗi lần gửi chiếm hai hàng.', 'Each cell is one 10 MB chunk of the video, numbered 1 to 20; each attempt takes two rows.')
    z('up.row.r1', 'Lần 1', 'Request 1'); z('up.row.r2', 'Lần 2', 'Request 2'); z('up.row.file', 'Bản upload abc', 'Upload abc')
    for k, vi, en in [('none', 'chưa gửi', 'not sent'), ('sent', 'đang gửi, server chưa giữ', 'sending, not kept yet'), ('ok', 'server đã giữ', 'kept by the server'), ('lost', 'đã gửi nhưng mất', 'sent but lost'), ('part', 'gửi dở thì đứt', 'cut while sending')]:
        z('up.st.' + k, vi, en)
    z('up.httph', 'HTTP của bước này', 'HTTP in this step')
    z('up.legend', 'Chữ đậm: server đã giữ. Viền cam: đang gửi, server chưa giữ. Gạch đỏ: đã gửi nhưng mất; ½ là khúc gửi dở thì đứt. Chữ mờ: chưa gửi.', 'Bold: kept by the server. Orange outline: sending, not kept yet. Red hatched: sent but lost; ½ marks the chunk cut mid-send. Faded: not sent.')

    C = 'i10'
    a(C + '.title', 'Ảnh và tệp lớn', 'Images and large files')
    a(C + '.essence', 'RAM của ảnh đã giải mã là rộng × cao × byte mỗi điểm ảnh, không phải kích thước tệp: ảnh camera 4000 × 3000 tốn khoảng 45,8 MiB. Hãy đọc kích thước trước và giải mã theo kích thước hiển thị (hệ số thu nhỏ inSampleSize), hoặc để thư viện ảnh làm.\nTệp lớn trên mạng di động nên upload tiếp tục được: tạo tài nguyên upload (địa chỉ trên server đại diện cho lần upload), gửi theo khúc, sau khi đứt hỏi server đã nhận tới đâu rồi gửi tiếp.\nViệc upload lâu phải sống qua khi app ra nền: WorkManager (công cụ chạy việc nền của Android) chạy foreground (có thông báo hiện), hay job truyền dữ liệu do người dùng khởi động (Android 14).',
      'A decoded image costs width × height × bytes per pixel, not the file size: a 4000 × 3000 camera photo takes about 45.8 MiB. Read the size first and decode for the display size (the inSampleSize shrink factor), or let an image library do it.\nLarge files on mobile networks should use resumable uploads: create an upload resource (an address on the server standing for the upload), send in chunks, and after a drop ask the server how far it got and continue.\nLong uploads must survive the app going to the background: WorkManager (Android\'s tool for background work) in the foreground (with a visible notification), or a user-initiated data transfer job (Android 14).')
    a(C + '.goal.g1', 'Đã thấy RAM của một ảnh', 'Saw the memory of one image')
    a(C + '.goal.g2', 'Đã thấy tổng RAM của lưới ảnh', 'Saw the total memory of the grid')
    a(C + '.sim.sysdesign.bitmap', 'RAM của ảnh', 'Image memory')
    a(C + '.sim.sysdesign.upload', 'Upload tệp lớn', 'Large uploads')

    S_ = 'hook'
    a(C + '.sec.%s.title' % S_, 'Đoán trước khi đọc', 'Predict before reading')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'predict', 'Tệp JPEG chụp từ camera nặng 3 MB, kích thước 4000 × 3000. App hiện 12 ảnh như vậy trong lưới, mỗi ô 270 px, bằng cách giải mã thẳng tệp gốc. Ước lượng RAM app cần là bao nhiêu?',
      'A camera JPEG weighs 3 MB at 4000 × 3000. The app shows 12 such photos in a grid of 270 px cells by decoding the original files directly. Estimate how much memory the app needs.')
    B(C, S_, 1, 'ans', 'Không phải 36 MB. Mỗi ảnh giải mã ở ARGB_8888 tốn 4000 × 3000 × 4 byte, khoảng 45,8 MiB; 12 ảnh là khoảng 549 MiB, vượt heap của hầu hết máy. Giải mã theo ô 270 px (inSampleSize 8) chỉ còn khoảng 8,6 MiB. [[src:ax-bitmap-config]] [[src:ax-load-bitmap]]',
      'Not 36 MB. Each decoded photo in ARGB_8888 takes 4000 × 3000 × 4 bytes, about 45.8 MiB; 12 photos are about 549 MiB, beyond most devices\' heaps. Decoding for the 270 px cell (inSampleSize 8) needs only about 8.6 MiB. [[src:ax-bitmap-config]] [[src:ax-load-bitmap]]')

    S_ = 'memory'
    a(C + '.sec.%s.title' % S_, 'RAM của ảnh tính theo điểm ảnh', 'Image memory counts pixels')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'p', 'JPEG hay PNG là dạng nén để lưu và truyền. Để vẽ, ảnh phải được giải mã thành bitmap, mỗi điểm ảnh một ô nhớ. Bitmap.Config cho số byte mỗi điểm ảnh: ARGB_8888 là 4 byte và được khuyên dùng; RGB_565 là 2 byte nhưng không có kênh trong suốt; RGBA_F16 là 8 byte cho ảnh dải màu rộng (nhiều màu hơn bình thường). Từ API 26 (Android 8.0), cấu hình HARDWARE chỉ giữ ảnh trong bộ nhớ đồ họa, hợp khi chỉ vẽ lên màn hình. [[src:ax-bitmap-config]]',
      'JPEG or PNG are compressed forms for storage and transfer. To draw, an image must be decoded into a bitmap, one memory cell per pixel. Bitmap.Config gives bytes per pixel: ARGB_8888 is 4 bytes and recommended; RGB_565 is 2 bytes but has no transparency; RGBA_F16 is 8 bytes for wide-gamut images (a wider range of colours than usual). From API 26 (Android 8.0), the HARDWARE config keeps the image only in graphics memory, best when it is only drawn to screen. [[src:ax-bitmap-config]]')
    B(C, S_, 2, 'kt', 'RAM = rộng × cao × byte mỗi điểm ảnh\n4000 × 3000 × 4 = 48.000.000 byte ≈ 45,8 MiB\n 500 ×  375 × 4 =    750.000 byte ≈  0,72 MiB',
      'memory = width × height × bytes per pixel\n4000 × 3000 × 4 = 48,000,000 bytes ≈ 45.8 MiB\n 500 ×  375 × 4 =    750,000 bytes ≈  0.72 MiB')
    B(C, S_, 3, 'note', 'Đây là lý do một màn ảnh trông đơn giản lại hay gây OutOfMemoryError, và vì sao chương I2, "Tiến trình, bộ nhớ và cái chết của process", nhắc app ở nền giữ nhiều RAM thì dễ bị giết trước.', 'This is why a simple-looking photo screen often causes OutOfMemoryError, and why chapter I2, "Processes, memory and process death", noted that a background app holding lots of memory is killed sooner.')
    B(C, S_, 3, 'kind', 'android')

    S_ = 'sample'
    a(C + '.sec.%s.title' % S_, 'Giải mã theo kích thước hiển thị', 'Decode for the display size')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'p', 'Tài liệu Android: đặt inJustDecodeBounds = true thì bộ giải mã không tạo bitmap nhưng vẫn trả outWidth, outHeight, nên biết được kích thước mà không tốn RAM. Rồi chọn inSampleSize: giải mã bỏ bớt điểm ảnh, 4 nghĩa là lấy một trong mỗi 4 × 4. Bộ giải mã làm tròn xuống lũy thừa của 2; hàm mẫu calculateInSampleSize nhân đôi s chừng nào nửa kích thước chia cho s vẫn không nhỏ hơn kích thước cần ở cả hai chiều. [[src:ax-load-bitmap]]',
      'Android docs: with inJustDecodeBounds = true the decoder creates no bitmap but still returns outWidth and outHeight, so you learn the size without spending memory. Then pick inSampleSize: decoding skips pixels, 4 meaning one of every 4 × 4. The decoder rounds down to a power of two; the sample calculateInSampleSize doubles s while half the size divided by s stays at or above the requested size in both directions. [[src:ax-load-bitmap]]')
    B(C, S_, 2, 'p', 'Tài liệu Android cũng khuyên dùng thư viện ảnh, nêu Glide và ngoài ra Coil, Picasso, Fresco: chúng giải mã theo kích thước view, cache trong RAM và trên đĩa, và hủy việc tải khi ô cuộn khỏi màn hình. Hiểu phép tính ở trên để biết thư viện đang làm gì và để đặt kích thước đích đúng; còn cấu hình từng thư viện thì đọc tài liệu của nó. [[src:ax-load-bitmap]]',
      'The Android docs also recommend an image library, naming Glide and also Coil, Picasso and Fresco: they decode for the view size, cache in memory and on disk, and cancel loads when a cell scrolls away. Understand the arithmetic above to know what the library does and to set the right target size; for each library\'s configuration, read its own docs. [[src:ax-load-bitmap]]')
    B(C, S_, 3, 'note', 'Phía server cũng giúp được: lưu sẵn nhiều cỡ ảnh (ảnh nhỏ cho lưới, ảnh lớn khi mở) để app không phải tải 3 MB chỉ để hiện một ô 270 px. Đây là gợi ý của site, khớp với bước ước lượng dữ liệu ở chương I1, "Từ đề bài tới kế hoạch".', 'The server can help too: store several sizes (thumbnails for the grid, large when opened) so the app need not download 3 MB to fill a 270 px cell. This is the site\'s suggestion, matching the data estimate in chapter I1, "From a brief to a plan".')
    B(C, S_, 3, 'kind', 'mechanism')

    S_ = 'resumable'
    a(C + '.sec.%s.title' % S_, 'Upload tiếp tục được', 'Resumable uploads')
    a(C + '.sec.%s.badge' % S_, 'version')
    B(C, S_, 1, 'p', 'Alex Xu chia upload làm hai loại: upload thường cho tệp nhỏ, và upload tiếp tục được cho tệp lớn khi mạng dễ đứt, theo ba bước: lấy URL để tiếp tục, gửi dữ liệu và theo dõi trạng thái, đứt thì tiếp. Alex Xu cũng chia video thành khúc để upload nhanh và làm lại được khi lỗi. [[src:book-xu1]]',
      'Alex Xu splits uploads into two kinds: simple uploads for small files, and resumable uploads for large files when the network may drop, in three steps: get a resumable URL, upload and monitor the state, resume when interrupted. Alex Xu also splits videos into chunks for fast uploads that can be redone after failure. [[src:book-xu1]]')
    B(C, S_, 2, 'p', 'IETF đang chuẩn hóa cách làm này trong dự thảo "Resumable Uploads for HTTP" (bản 16, 2026-11, chưa là RFC nên còn có thể đổi). Client tạo một tài nguyên upload và nhận địa chỉ qua Location; sau khi đứt, gửi HEAD để biết Upload-Offset, tức số byte server đã có; rồi gửi tiếp bằng PATCH kèm Upload-Offset, đánh dấu phần cuối bằng Upload-Complete (?1 là phần cuối, ?0 là còn tiếp). Offset không bao giờ giảm. Trong ví dụ dưới đây, 104 là phản hồi tạm báo địa chỉ upload, 204 là "thành công, không có nội dung", 201 là "đã tạo xong". [[src:ietf-resumable-upload]]',
      'The IETF is standardising this in the draft "Resumable Uploads for HTTP" (version 16, 2026-11, not yet an RFC, so it may still change). The client creates an upload resource and gets its address in Location; after a drop it sends HEAD to learn Upload-Offset, the bytes the server has; then continues with PATCH carrying Upload-Offset, marking the last part with Upload-Complete (?1 means last part, ?0 means more to come). The offset never decreases. In the example below, 104 is an interim response announcing the upload address, 204 means "success, no content", and 201 means "created". [[src:ietf-resumable-upload]]')
    B(C, S_, 3, 'kt', 'POST /uploads                      Upload-Complete: ?0\n← 104   Location: /uploads/abc\nPATCH /uploads/abc                 Upload-Offset: 0 …\n… đứt kết nối …\nHEAD /uploads/abc\n← 204   Upload-Offset: 190000000   (190 MB)\nPATCH /uploads/abc                 Upload-Offset: 190000000, Upload-Complete: ?1\n← 201 Created',
      'POST /uploads                      Upload-Complete: ?0\n← 104   Location: /uploads/abc\nPATCH /uploads/abc                 Upload-Offset: 0 …\n… connection drops …\nHEAD /uploads/abc\n← 204   Upload-Offset: 190000000   (190 MB)\nPATCH /uploads/abc                 Upload-Offset: 190000000, Upload-Complete: ?1\n← 201 Created')
    B(C, S_, 4, 'note', 'Ý chính, dù dùng giao thức nào: server mới là bên biết đã nhận tới đâu. App lưu địa chỉ tài nguyên upload xuống đĩa (process có thể chết giữa chừng, chương I2, "Tiến trình, bộ nhớ và cái chết của process") và hỏi lại server thay vì tự nhớ offset.', 'The key idea, whatever the protocol: the server is the one that knows how far it got. The app saves the upload resource address to disk (the process may die midway, chapter I2, "Processes, memory and process death") and asks the server again instead of remembering the offset itself.')
    B(C, S_, 4, 'kind', 'mechanism')

    S_ = 'background'
    a(C + '.sec.%s.title' % S_, 'Sống qua khi app ra nền', 'Surviving the background')
    a(C + '.sec.%s.badge' % S_, 'version')
    B(C, S_, 1, 'p', 'Upload 200 MB có thể mất nhiều phút; người dùng sẽ chuyển app khác. Từ Android 14 (API 34) có job truyền dữ liệu do người dùng khởi động (UIDT): dành cho việc truyền lâu mà người dùng tự bấm bắt đầu, cần quyền RUN_USER_INITIATED_JOBS, phải hiện thông báo, phải lên lịch khi app đang hiện, và được chạy lâu khi hệ thống cho phép. Trước Android 14, tài liệu khuyên dùng WorkManager chạy dạng foreground service (dịch vụ chạy nổi, luôn có thông báo). [[src:ax-uidt]]',
      'A 200 MB upload can take minutes; the user will switch apps. From Android 14 (API 34) there are user-initiated data transfer (UIDT) jobs: for long transfers the user starts, needing the RUN_USER_INITIATED_JOBS permission, a visible notification, scheduling while the app is visible, and allowed to run for a long time as conditions permit. Before Android 14 the docs recommend WorkManager running as a foreground service (a service that runs visibly, with a notification always shown). [[src:ax-uidt]]')
    B(C, S_, 2, 'p', 'Kết hợp với phần trên: mỗi lần job chạy lại (sau khi bị dừng vì mất mạng hay máy nóng), nó đọc địa chỉ upload đã lưu, HEAD để biết offset, rồi gửi tiếp. Thử lại theo backoff (giãn dần khoảng chờ giữa các lần thử) như chương I5, "Mạng không tin cậy: timeout, thử lại, idempotency". Đây là cách ghép của site.', 'Combined with the above: each time the job runs again (after being stopped for lost network or heat), it reads the saved upload address, HEADs for the offset, and continues. Retries follow backoff (growing waits between attempts) as in chapter I5, "Unreliable networks: timeouts, retries, idempotency". This is the site\'s way of putting it together.')

    S_ = 'bugs'
    a(C + '.sec.%s.title' % S_, 'Hai lỗi hay gặp', 'Two common bugs')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'bug', 'Màn ảnh chạy tốt trên máy thử, nhưng crash OutOfMemoryError trên máy người dùng có camera 200 MP (megapixel, 200 triệu điểm ảnh).', 'The photo screen runs fine on test phones but crashes with OutOfMemoryError on a user\'s phone with a 200 MP (megapixel) camera.')
    B(C, S_, 1, 'cause', 'App giải mã thẳng tệp gốc; ảnh lớn hơn nhiều lần nên bitmap lớn hơn nhiều lần, dù ô hiển thị không đổi.', 'The app decodes the original file; the much larger photo makes a much larger bitmap, though the cell did not change.')
    B(C, S_, 1, 'fix', 'Đọc kích thước trước và giải mã theo kích thước ô (inSampleSize), hoặc dùng thư viện ảnh với kích thước đích. [[src:ax-load-bitmap]]', 'Read the size first and decode for the cell (inSampleSize), or use an image library with a target size. [[src:ax-load-bitmap]]')
    B(C, S_, 2, 'bug', 'Upload tiếp tục được, nhưng sau khi app bị giết thì luôn bắt đầu lại từ 0.', 'The upload is resumable, but after the app is killed it always restarts from 0.')
    B(C, S_, 2, 'cause', 'Địa chỉ tài nguyên upload chỉ nằm trong RAM (trong một ViewModel, đối tượng giữ dữ liệu cho màn hình); process mới không biết upload cũ, nên tạo upload mới.', 'The upload resource address lived only in memory (a ViewModel, the object holding data for the screen); the new process knows nothing about the old upload, so it creates a new one.')
    B(C, S_, 2, 'fix', 'Lưu địa chỉ upload xuống đĩa cùng với id tệp, chạy upload trong WorkManager, và khi chạy lại thì HEAD trước. [[src:ietf-resumable-upload]]', 'Persist the upload address with the file id, run the upload in WorkManager, and HEAD first when it restarts. [[src:ietf-resumable-upload]]')

    S_ = 'ex'
    a(C + '.sec.%s.title' % S_, 'Bài tập', 'Exercise')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'ex', '(a) Ảnh 3000 × 2000, ô hiển thị 300 × 300 px: hàm calculateInSampleSize cho s bằng mấy, ảnh sau giải mã bao nhiêu điểm ảnh và tốn bao nhiêu MiB ở ARGB_8888? (b) Upload 120 MB, khúc 8 MB, mạng đứt khi đã gửi 100 MB và server giữ các khúc trọn vẹn: một request thì tổng gửi bao nhiêu MB, upload tiếp tục được thì bao nhiêu?',
      '(a) A 3000 × 2000 photo for a 300 × 300 px cell: what s does calculateInSampleSize give, how many pixels is the decoded image, and how many MiB in ARGB_8888? (b) A 120 MB upload in 8 MB chunks drops after 100 MB, with the server keeping whole chunks: how many MB are sent in total with one request, and with a resumable upload?')
    B(C, S_, 1, 'hint', '(a) Nửa kích thước là 1500 × 1000. (b) 100 MB là bao nhiêu khúc trọn vẹn?', '(a) Half the size is 1500 × 1000. (b) How many whole chunks is 100 MB?')
    B(C, S_, 1, 'sol', '(a) s = 1: 1500, 1000 đều ≥ 300 nên s = 2; 750, 500 ≥ 300 nên s = 4; 375, 250: 250 < 300 nên dừng, s = 4. Ảnh 750 × 500, tốn 750 × 500 × 4 = 1.500.000 byte ≈ 1,43 MiB (ảnh gốc ≈ 22,9 MiB). (b) Một request: 100 + 120 = 220 MB. Tiếp tục được: 12 khúc trọn vẹn = 96 MB được giữ; gửi lại từ 96 MB thêm 24 MB, tổng 100 + 24 = 124 MB.',
      '(a) s = 1: 1500 and 1000 are both ≥ 300, so s = 2; 750, 500 ≥ 300, so s = 4; 375, 250: 250 < 300, stop, s = 4. The image is 750 × 500, taking 750 × 500 × 4 = 1,500,000 bytes ≈ 1.43 MiB (the original ≈ 22.9 MiB). (b) One request: 100 + 120 = 220 MB. Resumable: 12 whole chunks = 96 MB kept; resending from 96 MB adds 24 MB, 100 + 24 = 124 MB in total.')

    for q, qv, qe, av, ae, wv, we in [
        ('q1', 'Ảnh 1000 × 1000 ở ARGB_8888 tốn bao nhiêu RAM khi đã giải mã?', 'How much memory does a decoded 1000 × 1000 image take in ARGB_8888?', 'Khoảng 4.000.000 byte, tức khoảng 3,8 MiB (1000 × 1000 × 4 byte), bất kể tệp JPEG nặng bao nhiêu.', 'About 4,000,000 bytes, roughly 3.8 MiB (1000 × 1000 × 4 bytes), whatever the JPEG file weighs.', 'RAM theo điểm ảnh, không theo tệp.', 'Memory follows pixels, not the file.'),
        ('q2', 'inJustDecodeBounds = true dùng để làm gì?', 'What is inJustDecodeBounds = true for?', 'Đọc kích thước ảnh mà không tạo bitmap, để chọn inSampleSize trước khi giải mã thật.', 'Reading the image size without creating a bitmap, to pick inSampleSize before the real decode.', 'Không tốn RAM cho bitmap.', 'No bitmap memory is spent.'),
        ('q3', 'Sau khi kết nối đứt, upload tiếp tục được biết gửi tiếp từ đâu bằng cách nào?', 'After a drop, how does a resumable upload know where to continue?', 'Hỏi server: HEAD tới tài nguyên upload, đọc Upload-Offset.', 'It asks the server: HEAD the upload resource and read Upload-Offset.', 'Server mới biết chắc đã nhận gì.', 'Only the server knows for sure what it received.'),
        ('q4', 'Vì sao địa chỉ tài nguyên upload phải lưu xuống đĩa?', 'Why must the upload resource address be saved to disk?', 'Vì process có thể bị giết giữa lúc upload; process mới cần địa chỉ đó để tiếp tục thay vì tạo upload mới.', 'Because the process may be killed mid-upload; the new process needs it to continue instead of starting a new upload.', 'Xem chương I2, "Tiến trình, bộ nhớ và cái chết của process".', 'See chapter I2, "Processes, memory and process death".')]:
        a(C + '.quiz.%s.q' % q, qv, qe); a(C + '.quiz.%s.a' % q, av, ae); a(C + '.quiz.%s.why' % q, wv, we)
