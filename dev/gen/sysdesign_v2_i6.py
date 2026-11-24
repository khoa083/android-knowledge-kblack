# Thiết kế hệ thống phía mobile · I6: cache (Phần 2)
# Nguồn: RFC 9111 (HTTP Caching: 4.2 freshness, 4.2.2 heuristic, 4.2.4 stale, 4.3 validation, 5.2.2 directive); RFC 9110 (8.8 validator, ETag,
# 13.1.2 If-None-Match, 15.4.5 304); Alex Xu tập 1 ch.1 (khi nào cache, hết hạn, nhất quán, LRU). Đọc 2026-11-24.

SEC_ORDER = {'i6': ['hook', 'layers', 'fresh', 'validate', 'directives', 'bugs', 'ex', 'honest']}


def add(a):
    def B(ch, sec, n, field, vi, en=None):
        a('%s.sec.%s.b.%02d.%s' % (ch, sec, n, field), vi, vi if en is None else en)

    a('preset.cache', 'Thiết kế hệ thống · cache bảng giá khám', 'System design · caching the fee list')
    m = lambda k, vi, en=None: a('m.cache.' + k, vi, en)
    m('title', 'Không cache, cache mãi, max-age, hay max-age kèm ETag', 'No cache, cache forever, max-age, or max-age with an ETag')
    m('overview', 'Màn "Bảng giá khám" tải một danh sách khoảng 200 KB. Người dùng mở màn này lúc 0:00, 0:02, 0:10 và 0:30; ở phút 20, phòng khám đổi giá khám từ 200.000 đ lên 250.000 đ. Giữa phút 2 và phút 10, app nằm ở nền và process bị giết, nên cache trong bộ nhớ mất. Bốn cách: không cache; tự lưu mãi trên đĩa; theo Cache-Control: max-age=300; max-age=300 kèm ETag để hỏi lại có điều kiện.',
      'The "Fees" screen loads a list of about 200 KB. The user opens it at 0:00, 0:02, 0:10 and 0:30; at minute 20 the clinic raises the fee from 200,000 to 250,000 VND. Between minutes 2 and 10 the app sits in the background and its process is killed, so the in-memory cache is lost. Four ways: no cache; keep it on disk forever; follow Cache-Control: max-age=300; max-age=300 plus an ETag for conditional requests.')
    m('wrapup', 'Không cache thì luôn đúng nhưng chậm và tốn dữ liệu. Cache mãi thì nhanh nhưng giá cũ ở lại vĩnh viễn. max-age cho phép dùng bản lưu mà không hỏi trong một khoảng thời gian, chấp nhận có thể cũ tối đa chừng đó. Khi bản lưu hết tươi, ETag biến lần tải lại thành một câu hỏi rẻ: "bản v7 còn đúng không?"; server trả 304 không kèm nội dung nếu còn, hoặc 200 với bản mới nếu đã đổi.',
      'No cache is always right but slow and costly in data. Caching forever is fast but the old price stays forever. max-age allows reusing the stored copy without asking for a while, accepting it may be up to that old. When the copy goes stale, an ETag turns the reload into a cheap question, "is v7 still current?"; the server answers 304 with no content if so, or 200 with the new version if it changed.')
    m('simp.1', 'Kích thước 200 KB, giá khám, các mốc phút và việc process bị giết giữa phút 2 và 10 là minh họa. 304 vẫn tốn vài trăm byte header; mô phỏng ghi tròn là 1 KB.', 'The 200 KB size, the fees, the minute marks and the process dying between minutes 2 and 10 are illustrative. A 304 still costs a few hundred bytes of headers; the simulation rounds it to 1 KB.')
    m('simp.2', 'Độ tươi, kiểm tra lại, directive Cache-Control theo RFC 9111; ETag, If-None-Match và 304 theo RFC 9110; cân nhắc khi dùng cache theo Alex Xu tập 1. Đọc ngày 2026-11-24.', 'Freshness, validation and Cache-Control directives follow RFC 9111; ETag, If-None-Match and 304 follow RFC 9110; cache considerations follow Alex Xu vol. 1. Read on 2026-11-24.')
    m('ctl.hint', 'Đổi cách cache rồi đi lại; so giá hiển thị ở bước 4 và tổng KB đã tải.', 'Switch the caching approach and walk again; compare the fee shown at step 4 and the total KB downloaded.')
    m('ctl.case', 'Cách cache', 'Caching approach')
    for k, vi, en in [('none', 'không cache', 'no cache'), ('forever', 'lưu mãi trên đĩa', 'keep on disk forever'), ('maxage', 'Cache-Control: max-age=300', 'Cache-Control: max-age=300 only'), ('etag', 'max-age=300 kèm ETag', 'max-age=300 plus ETag')]:
        m('ctl.case.' + k, vi, en)
    m('diagramTitle', 'Màn hình, bộ nhớ, đĩa, mạng', 'Screen, memory, disk, network')
    m('diagramDesc', 'Màn hình hỏi bộ nhớ trước, rồi đĩa, rồi mới tới mạng', 'The screen asks memory first, then disk, then the network')
    for k, vi, en in [('ui', 'Màn bảng giá', 'Fees screen'), ('mem', 'Cache trong bộ nhớ', 'In-memory cache'), ('disk', 'Cache HTTP trên đĩa', 'HTTP disk cache'), ('net', 'Server phòng khám', 'Server')]:
        m('n.' + k, vi, en)
    m('met.kb', 'KB đã tải (cộng dồn)', 'KB downloaded (running total)'); m('met.right', 'Giá hiển thị đúng', 'Fee shown is correct'); m('met.net', 'Lượt gọi mạng (cộng dồn)', 'Network calls (running total)')
    a('cap.cache', 'Màn hình bên trái hỏi lần lượt bộ nhớ, đĩa, rồi server bên phải; tầng nào trả lời thì sáng.', 'The screen on the left asks memory, then disk, then the server on the right; the tier that answers lights up.')
    S = [
        ('none', 's1', '0:00: mở màn hình, tải 200 KB', '0:00: open the screen, download 200 KB', 'Không lưu gì; mỗi lần mở là một lần tải đầy đủ.', 'Nothing is stored; every open is a full download.'),
        ('none', 's2', '0:02: mở lại, tải lại 200 KB', '0:02: open again, download 200 KB again', 'Dữ liệu chưa đổi, nhưng app không biết, nên tải lại hết.', 'The data has not changed, but the app cannot know, so it downloads everything.'),
        ('none', 's3', '0:10: mở lại, tải lại 200 KB', '0:10: open again, download 200 KB again', 'Mỗi lần mở đều chờ mạng; mất sóng thì màn hình trống.', 'Every open waits for the network; without signal the screen is empty.'),
        ('none', 's4', '0:30: giá đã đổi; tải 200 KB, hiện đúng 250.000 đ', '0:30: the fee has changed; download 200 KB, show the correct 250,000', 'Luôn đúng, nhưng đã tải 800 KB cho một danh sách gần như không đổi.', 'Always right, but 800 KB downloaded for a list that barely changes.'),
        ('forever', 's1', '0:00: tải 200 KB, lưu xuống đĩa và bộ nhớ', '0:00: download 200 KB, store it on disk and in memory', 'App tự lưu, không đọc header nào của server.', 'The app stores it itself, ignoring every server header.'),
        ('forever', 's2', '0:02: trúng cache bộ nhớ, hiện ngay', '0:02: memory cache hit, shown at once', 'Không gọi mạng. Nhanh.', 'No network call. Fast.'),
        ('forever', 's3', '0:10: process đã bị giết; trúng cache đĩa', '0:10: the process was killed; disk cache hit', 'Cache bộ nhớ mất cùng process (chương I2), cache đĩa thì còn.', 'The memory cache died with the process (chapter I2); the disk cache remains.'),
        ('forever', 's4', '0:30: trúng cache đĩa, hiện giá cũ 200.000 đ', '0:30: disk cache hit, shows the old 200,000', 'Không có hạn dùng nên app không bao giờ hỏi lại; giá cũ ở lại cho tới khi xóa dữ liệu app.', 'With no expiry, the app never asks again; the old fee stays until the app data is cleared.'),
        ('maxage', 's1', '0:00: tải 200 KB kèm Cache-Control: max-age=300', '0:00: download 200 KB with Cache-Control: max-age=300', 'Server nói: bản này tươi trong 300 giây.', 'The server says: this copy is fresh for 300 seconds.'),
        ('maxage', 's2', '0:02: bản lưu mới 2 phút, còn tươi: dùng luôn', '0:02: the copy is 2 minutes old, still fresh: reuse it', 'Không gọi mạng trong khoảng max-age.', 'No network call within max-age.'),
        ('maxage', 's3', '0:10: bản lưu 10 phút, đã cũ: tải lại 200 KB', '0:10: the copy is 10 minutes old, stale: download 200 KB again', 'Dữ liệu thật ra chưa đổi, nhưng không có ETag thì app không hỏi rẻ được.', 'The data has not actually changed, but without an ETag the app cannot ask cheaply.'),
        ('maxage', 's4', '0:30: đã cũ; tải 200 KB, hiện đúng 250.000 đ', '0:30: stale; download 200 KB, show the correct 250,000', 'Đúng giá. Đổi lại: trong 5 phút sau một lần tải, app có thể hiện giá cũ.', 'The fee is right. The price: for 5 minutes after a download, the app may show an old fee.'),
        ('etag', 's1', '0:00: tải 200 KB kèm max-age=300 và ETag "v7"', '0:00: download 200 KB with max-age=300 and ETag "v7"', 'ETag là nhãn phiên bản của nội dung, do server đặt.', 'The ETag is a version label for the content, chosen by the server.'),
        ('etag', 's2', '0:02: còn tươi: dùng luôn', '0:02: still fresh: reuse it', 'Giống max-age.', 'Same as max-age.'),
        ('etag', 's3', '0:10: đã cũ; hỏi If-None-Match "v7", server trả 304', '0:10: stale; ask If-None-Match "v7", the server answers 304', '304 Not Modified không có nội dung; app cập nhật header và dùng lại bản đã lưu. Chỉ tốn vài trăm byte.', '304 Not Modified has no content; the app updates the headers and reuses the stored copy. Just a few hundred bytes.'),
        ('etag', 's4', '0:30: hỏi If-None-Match "v7", server trả 200 với "v8"', '0:30: ask If-None-Match "v7", the server answers 200 with "v8"', 'Nội dung đã đổi nên tải bản mới 200 KB và hiện đúng 250.000 đ. Tổng 401 KB thay vì 800 KB.', 'The content changed, so download the new 200 KB and show the correct 250,000. 401 KB in total instead of 800 KB.'),
    ]
    for case, k, tv, te, xv, xe in S:
        sid = case + '.' + k
        m('s.%s.title' % sid, tv, te); m('s.%s.explain' % sid, xv, xe); m('ev.' + sid, tv, te)
    for k, vi, en in [
        ('try', 'Đi hết bốn bước của mỗi cách; nhìn tầng nào trả lời và giá hiển thị ở bước 4.', 'Walk all four steps of each approach; watch which tier answers and the fee shown at step 4.'),
        ('none.s2', 'Alex Xu (tập 1): nên cache khi dữ liệu được đọc thường xuyên mà ít khi sửa; bảng giá đúng là loại đó. [[src:book-xu1]]', 'Alex Xu: consider caching when data is read often but changed rarely; a fee list is exactly that. [[src:book-xu1]]'),
        ('none.s3', 'Không có bản lưu nào thì mất mạng là mất màn hình; offline-first ở track Lưu dữ liệu (H7) giải chuyện này bằng database.', 'With no stored copy, no network means no screen; offline-first in the Saving Data track (H7) solves it with a database.'),
        ('none.s4', 'Đúng nhưng tốn: 4 lần × 200 KB cho cùng một danh sách gần như không đổi.', 'Right but costly: 4 × 200 KB for nearly the same list.'),
        ('forever.s2', 'Cache bộ nhớ nhanh nhất, nhưng chỉ sống cùng process.', 'The memory cache is fastest, but lives only as long as the process.'),
        ('forever.s3', 'Process bị giết thì cache bộ nhớ mất; xem chương I2.', 'A killed process loses its memory cache; see chapter I2.'),
        ('forever.s4', 'Alex Xu (tập 1): nên có chính sách hết hạn; không có thì dữ liệu nằm trong cache mãi và có thể cũ. [[src:book-xu1]]', 'Alex Xu: have an expiration policy; without one, data stays in the cache forever and can go stale. [[src:book-xu1]]'),
        ('maxage.s2', 'RFC 9111: response còn tươi khi tuổi chưa vượt thời gian sống; max-age cho thời gian sống đó, tính bằng giây. [[src:rfc9111]]', 'RFC 9111: a response is fresh while its age has not exceeded its freshness lifetime; max-age gives that lifetime in seconds. [[src:rfc9111]]'),
        ('maxage.s3', 'RFC 9111: hết tươi thì cache phải lấy lại hay kiểm tra lại; không có validator (ETag, Last-Modified) thì chỉ còn cách tải lại đầy đủ. [[src:rfc9111]]', 'RFC 9111: once stale, the cache must fetch or validate again; with no validator (ETag, Last-Modified) only a full download remains. [[src:rfc9111]]'),
        ('maxage.s4', 'max-age là lời hứa "có thể cũ tối đa chừng này". Chọn giá trị theo mức chấp nhận được của dữ liệu: giá khám vài phút thì được, số dư tài khoản thì không.', 'max-age is a promise of "at most this stale". Choose it by what the data can tolerate: a few minutes for fees, not for an account balance.'),
        ('etag.s2', 'Trong khoảng max-age, ETag chưa được dùng tới.', 'Within max-age, the ETag is not used yet.'),
        ('etag.s3', 'RFC 9111: cache gửi lại ETag đã lưu trong If-None-Match; 304 nghĩa là bản đã lưu được cập nhật và dùng lại. RFC 9110: 304 không có nội dung. [[src:rfc9111]] [[src:rfc9110]]', 'RFC 9111: the cache sends the stored ETag in If-None-Match; a 304 means the stored response is updated and reused. RFC 9110: a 304 has no content. [[src:rfc9111]] [[src:rfc9110]]'),
        ('etag.s4', 'RFC 9111: nhận response đầy đủ thay cho 304 nghĩa là bản đã lưu không còn hợp, cache dùng bản mới. [[src:rfc9111]]', 'RFC 9111: a full response instead of a 304 means the stored copy is no longer suitable, and the cache uses the new one. [[src:rfc9111]]')]:
        m('co.' + k, vi, en)

    z = lambda k, vi, en=None: a('vz.' + k, vi, en)
    z('tab.ca', 'Các tầng cache và header', 'Cache tiers and headers')
    z('ca.cap', 'Màn hình hỏi từng tầng từ trên xuống; tầng có viền cam là tầng trả lời.', 'The screen asks each tier top to bottom; the orange-outlined tier is the one that answers.')
    for k, vi, en in [('tier', 'Tầng', 'Tier'), ('res', 'Kết quả', 'Result'), ('kb', 'KB tải', 'KB')]:
        z('ca.col.' + k, vi, en)
    for k, vi, en in [('mem', 'Bộ nhớ (mất khi process chết)', 'Memory (lost when the process dies)'), ('disk', 'Đĩa (cache HTTP)', 'Disk (HTTP cache)'), ('net', 'Mạng (server)', 'Network (server)')]:
        z('ca.t.' + k, vi, en)
    for k, vi, en in [('off', 'không dùng', 'not used'), ('miss', 'trượt', 'miss'), ('hit', 'trúng', 'hit'), ('fresh', 'trúng, còn tươi', 'hit, still fresh'), ('stale', 'có bản lưu nhưng đã cũ', 'stored, but stale'),
                      ('hitold', 'trúng, nhưng là giá cũ', 'hit, but the old fee'), ('skip', 'không hỏi', 'not asked'), ('full', '200: tải đầy đủ', '200: full download'),
                      ('n304', '304: không đổi, dùng lại bản lưu', '304: unchanged, reuse the stored copy'), ('n200new', '200: đã đổi, bản mới "v8"', '200: changed, new version "v8"'), ('full7', '200: tải đầy đủ, ETag "v7"', '200: full download, ETag "v7"')]:
        z('ca.r.' + k, vi, en)
    z('ca.shown', 'Giá hiển thị', 'Fee shown'); z('ca.server', 'Giá trên server', 'Fee on the server')
    z('ca.fee.old', '200.000 đ', '200,000 VND'); z('ca.fee.new', '250.000 đ', '250,000 VND')
    z('ca.hcap', 'Header nói gì với cache (RFC 9111, RFC 9110). Hàng tô là hàng cách này dùng.', 'What headers tell a cache (RFC 9111, RFC 9110). Highlighted rows are the ones this approach uses.')
    for k, h_, vi, en in [
        ('maxage', 'Cache-Control: max-age=N', 'tươi trong N giây; trong khoảng đó dùng lại không cần hỏi', 'fresh for N seconds; reuse without asking until then'),
        ('nocache', 'Cache-Control: no-cache', 'được lưu, nhưng phải kiểm tra lại với server trước mỗi lần dùng', 'may be stored, but must be validated with the server before each use'),
        ('nostore', 'Cache-Control: no-store', 'không được lưu bất kỳ phần nào', 'must not store any part of it'),
        ('mustrev', 'Cache-Control: must-revalidate', 'đã cũ thì phải kiểm tra lại; mất mạng thì báo lỗi chứ không dùng bản cũ', 'once stale, must validate; when offline, return an error rather than the stale copy'),
        ('private', 'Cache-Control: private', 'cache dùng chung (proxy) không được lưu; cache riêng của app thì được', 'shared caches (proxies) must not store it; the app\'s private cache may'),
        ('etag', 'ETag + If-None-Match', 'nhãn phiên bản; lần sau hỏi "còn là bản này không?"', 'a version label; next time ask "is it still this version?"'),
        ('n304', '304 Not Modified', 'không có nội dung; cập nhật header và dùng lại bản đã lưu', 'no content; update the headers and reuse the stored copy')]:
        z('ca.h.%s.what' % k, vi, en)
    z('ca.legend', 'Ô gạch đỏ: giá cũ đang hiện, hay tải lại không cần thiết.', 'Red hatched: an old fee on screen, or an unnecessary reload.')

    C = 'i6'
    a(C + '.title', 'Cache: bộ nhớ, đĩa và HTTP', 'Caching: memory, disk and HTTP')
    a(C + '.essence', 'Cache đổi độ tươi lấy tốc độ và dữ liệu. App thường có ba tầng: bộ nhớ (mất khi process chết), đĩa, và mạng.\nmax-age nói bản lưu tươi trong bao lâu; trong khoảng đó dùng lại không cần hỏi, và chấp nhận có thể cũ tới chừng ấy.\nHết tươi thì hỏi lại có điều kiện bằng ETag: 304 không có nội dung nếu chưa đổi, 200 kèm bản mới nếu đã đổi. no-cache là "lưu nhưng hỏi lại trước khi dùng"; no-store mới là "đừng lưu".',
      'A cache trades freshness for speed and data. An app usually has three tiers: memory (lost when the process dies), disk, and the network.\nmax-age says how long a stored copy is fresh; within it, reuse without asking, accepting it may be that old.\nOnce stale, ask conditionally with an ETag: a 304 with no content if unchanged, a 200 with the new version if changed. no-cache means "store but validate before use"; no-store is what means "do not store".')
    a(C + '.goal.g1', 'Đã thấy tầng cache trả lời', 'Saw a cache tier answer')
    a(C + '.goal.g2', 'Đã thấy giá hiển thị cuối cùng', 'Saw the final fee shown')
    a(C + '.sim.sysdesign.cache', 'không cache, cache mãi, max-age, max-age kèm ETag', 'no cache, forever, max-age, max-age plus ETag')

    S_ = 'hook'
    a(C + '.sec.%s.title' % S_, 'Đoán trước khi đọc', 'Predict before reading')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'predict', 'Để màn bảng giá mở nhanh, app lưu danh sách xuống đĩa lần đầu tải và lần sau đọc từ đĩa. Một tháng sau phòng khám tăng giá. Người dùng thấy gì, và bạn cần thêm đúng một thứ gì để sửa mà không mất cái nhanh?',
      'To make the fee screen open fast, the app stores the list on disk after the first download and reads it from disk afterwards. A month later the clinic raises its fees. What do users see, and what one thing do you need to fix it without losing the speed?')
    B(C, S_, 1, 'ans', 'Họ thấy giá cũ mãi, vì bản lưu không có hạn dùng. Cần một chính sách hết hạn (max-age), và tốt hơn là thêm validator (ETag) để khi hết hạn chỉ hỏi "còn là bản này không?" thay vì tải lại toàn bộ. [[src:book-xu1]] [[src:rfc9111]]',
      'They see the old fees forever, because the stored copy has no expiry. You need an expiration policy (max-age), and better, a validator (ETag) so that on expiry you only ask "is it still this version?" instead of downloading it all. [[src:book-xu1]] [[src:rfc9111]]')

    S_ = 'layers'
    a(C + '.sec.%s.title' % S_, 'Ba tầng và bốn câu hỏi', 'Three tiers and four questions')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'p', 'Alex Xu (tập 1) nêu các cân nhắc khi dùng cache. Khi nào nên cache: dữ liệu đọc nhiều, ít sửa. Chính sách hết hạn: quá ngắn thì tải lại liên tục, quá dài thì dữ liệu cũ. Nhất quán: nguồn dữ liệu và cache không đổi trong cùng một giao dịch nên có thể lệch nhau. Chính sách loại bỏ khi đầy: LRU phổ biến nhất, ngoài ra có LFU, FIFO. Sách nói về cache tầng server; trên app, cùng bốn câu hỏi đó áp vào từng tầng. [[src:book-xu1]]',
      'Alex Xu lists considerations for caching. When to cache: data read often, changed rarely. Expiration: too short means constant reloads, too long means stale data. Consistency: the data store and the cache are not updated in one transaction, so they can drift. Eviction when full: LRU is most common, with LFU and FIFO as alternatives. The book is about a server-side cache tier; in an app, the same four questions apply to each tier. [[src:book-xu1]]')
    B(C, S_, 2, 'p', 'Ba tầng của app: bộ nhớ (một LruCache, nhanh nhất, mất khi process bị giết), đĩa (cache HTTP của thư viện mạng, như Cache của OkHttp, theo đúng các header của RFC 9111), và mạng. Database Room thì khác: ở track Kiến trúc (G4), database là nguồn sự thật mà màn hình quan sát, không phải bản sao có hạn dùng. Cache HTTP hợp với dữ liệu chỉ đọc như bảng giá, ảnh, cấu hình. Đoạn này là diễn giải của site.',
      'An app\'s three tiers: memory (an LruCache, fastest, lost when the process is killed), disk (the network library\'s HTTP cache, such as OkHttp\'s Cache, following RFC 9111 headers), and the network. A Room database is different: in the Architecture track (G4), the database is the source of truth the screen observes, not a copy with an expiry. An HTTP cache suits read-only data such as fee lists, images and configuration. This paragraph is the site\'s interpretation.')

    S_ = 'fresh'
    a(C + '.sec.%s.title' % S_, 'Tươi và cũ', 'Fresh and stale')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'p', 'RFC 9111: một response tươi khi tuổi của nó chưa vượt thời gian sống, và cũ khi đã vượt. Thời gian sống lấy theo thứ tự: s-maxage (chỉ cache dùng chung), max-age, rồi Expires trừ Date. Không có gì cả thì cache được phép đoán (heuristic); nếu có Last-Modified, RFC khuyên đoán không quá một phần khoảng thời gian từ lần sửa cuối, thường là 10%. [[src:rfc9111]]',
      'RFC 9111: a response is fresh while its age has not exceeded its freshness lifetime, and stale after. The lifetime comes, in order, from s-maxage (shared caches only), max-age, then Expires minus Date. With none of these, a cache may guess (heuristic); with Last-Modified, the RFC suggests no more than a fraction of the time since the last change, typically 10%. [[src:rfc9111]]')
    B(C, S_, 2, 'p', 'Hệ quả cho app: server không gửi header cache thì thư viện có thể tự đoán thời gian sống, và màn hình hiện dữ liệu cũ mà không ai cố ý. Hãy thống nhất với backend (chương I1) header cho từng loại dữ liệu. Khi mất mạng, RFC cho phép dùng bản đã cũ, trừ khi response có must-revalidate hay no-cache. [[src:rfc9111]]',
      'For the app: if the server sends no cache headers, the library may guess a lifetime, and the screen shows stale data nobody intended. Agree headers per kind of data with the backend (chapter I1). When offline, the RFC allows serving a stale copy, unless the response carries must-revalidate or no-cache. [[src:rfc9111]]')

    S_ = 'validate'
    a(C + '.sec.%s.title' % S_, 'Hỏi lại có điều kiện: ETag và 304', 'Conditional requests: ETag and 304')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'p', 'ETag là một validator: một chuỗi do server đặt để phân biệt các phiên bản của cùng một tài nguyên (số phiên bản, mã băm nội dung…). ETag mạnh đổi mỗi khi dữ liệu đổi; ETag yếu, có tiền tố W/, có thể không đổi với thay đổi nhỏ. Khi bản lưu đã cũ, cache gửi lại ETag trong If-None-Match; If-None-Match được ưu tiên hơn If-Modified-Since. [[src:rfc9110]] [[src:rfc9111]]',
      'An ETag is a validator: a string the server chooses to tell versions of the same resource apart (a revision number, a content hash…). A strong ETag changes whenever the data changes; a weak one, prefixed W/, might not change for small edits. When the stored copy is stale, the cache sends the ETag back in If-None-Match; If-None-Match takes precedence over If-Modified-Since. [[src:rfc9110]] [[src:rfc9111]]')
    B(C, S_, 2, 'p', 'Nếu ETag còn khớp, server trả 304 Not Modified. 304 dừng ngay sau phần header, không có nội dung; cache cập nhật header của bản đã lưu và dùng lại nội dung cũ. Nếu đã đổi, server trả 200 với nội dung và ETag mới. Với danh sách 200 KB, một lần 304 chỉ tốn vài trăm byte. [[src:rfc9110]] [[src:rfc9111]]',
      'If the ETag still matches, the server answers 304 Not Modified. A 304 ends right after the headers, with no content; the cache updates the stored copy\'s headers and reuses the old content. If it changed, the server answers 200 with new content and a new ETag. For a 200 KB list, a 304 costs only a few hundred bytes. [[src:rfc9110]] [[src:rfc9111]]')
    B(C, S_, 3, 'kt', 'GET /fees\n← 200, ETag: "v7", Cache-Control: max-age=300      (200 KB)\n\n… 10 phút sau, bản lưu đã cũ …\nGET /fees\nIf-None-Match: "v7"\n← 304 Not Modified                                 (không có nội dung)',
      'GET /fees\n← 200, ETag: "v7", Cache-Control: max-age=300      (200 KB)\n\n… 10 minutes later, the stored copy is stale …\nGET /fees\nIf-None-Match: "v7"\n← 304 Not Modified                                 (no content)')

    S_ = 'directives'
    a(C + '.sec.%s.title' % S_, 'no-cache không có nghĩa là "đừng lưu"', 'no-cache does not mean "do not store"')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'p', 'Theo RFC 9111: no-cache cho phép lưu, nhưng không được dùng lại khi chưa kiểm tra lại với server. no-store mới là không được lưu bất kỳ phần nào; RFC cũng nói no-store không phải cơ chế bảo mật đáng tin. must-revalidate: đã cũ thì không được dùng nếu chưa kiểm tra lại, và khi mất mạng thì phải báo lỗi (nên là 504) chứ không trả bản cũ. private: cache dùng chung không được lưu, cache riêng của một người dùng thì được. [[src:rfc9111]]',
      'Per RFC 9111: no-cache allows storing, but the response must not be reused without validating with the server. no-store is what forbids storing any part; the RFC also says no-store is not a reliable privacy mechanism. must-revalidate: once stale, it must not be used until validated, and when offline the cache must return an error (504 recommended) rather than the stale copy. private: shared caches must not store it; a single user\'s private cache may. [[src:rfc9111]]')
    B(C, S_, 2, 'note', 'Chọn theo dữ liệu: bảng giá, danh sách bác sĩ: max-age vài phút kèm ETag. Ảnh có URL đổi theo phiên bản: max-age dài. Lịch hẹn của người dùng: no-cache kèm ETag, hoặc để database làm nguồn sự thật (G4, H7). Kết quả xét nghiệm, token: no-store. Đây là gợi ý của site.',
      'Choose by data: fee lists, the doctor list: a few minutes of max-age plus an ETag. Images whose URLs change per version: a long max-age. The user\'s own bookings: no-cache plus an ETag, or make the database the source of truth (G4, H7). Lab results, tokens: no-store. These are the site\'s suggestions.')
    B(C, S_, 2, 'kind', 'android')

    S_ = 'bugs'
    a(C + '.sec.%s.title' % S_, 'Hai lỗi hay gặp', 'Two common bugs')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'bug', 'Đã sửa giá trên server nhưng một số người vẫn thấy giá cũ cả ngày.', 'The fee was fixed on the server, but some users see the old fee all day.')
    B(C, S_, 1, 'cause', 'Server không gửi Cache-Control; thư viện tự đoán thời gian sống theo Last-Modified (danh sách đã lâu không sửa nên đoán ra vài ngày).', 'The server sent no Cache-Control; the library guessed a lifetime from Last-Modified (the list had not changed in a long time, so the guess was days).')
    B(C, S_, 1, 'fix', 'Thống nhất header rõ ràng cho từng endpoint, ví dụ max-age=300 kèm ETag; đừng để cache đoán.', 'Agree on explicit headers per endpoint, such as max-age=300 plus an ETag; do not let the cache guess.')
    B(C, S_, 2, 'bug', 'Đặt no-cache cho kết quả xét nghiệm "để không lưu trên máy", nhưng file vẫn nằm trong thư mục cache.', 'no-cache was set on lab results "so they are not stored on the device", yet the file sits in the cache folder.')
    B(C, S_, 2, 'cause', 'no-cache nghĩa là lưu nhưng kiểm tra lại trước khi dùng; muốn không lưu phải là no-store.', 'no-cache means store but validate before use; not storing requires no-store.')
    B(C, S_, 2, 'fix', 'Dùng no-store; và vì RFC nói no-store không phải cơ chế bảo mật đáng tin, dữ liệu nhạy cảm còn cần các biện pháp ở track Lưu dữ liệu (H9).', 'Use no-store; and since the RFC says no-store is not a reliable privacy mechanism, sensitive data still needs the measures in the Saving Data track (H9).')

    S_ = 'ex'
    a(C + '.sec.%s.title' % S_, 'Bài tập', 'Exercise')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'ex', 'Chọn header (và tầng cache phía app) cho: (a) ảnh đại diện bác sĩ, URL có số phiên bản; (b) danh sách chuyên khoa, đổi vài lần một năm; (c) số chỗ còn trống của ngày mai; (d) đơn thuốc của người dùng. Với (b), tính số KB tiết kiệm trong 30 lần mở mỗi tháng nếu danh sách 50 KB, max-age 1 giờ, và mỗi lần mở đều sau khi đã hết tươi.',
      'Choose headers (and the app\'s cache tier) for: (a) doctor avatars whose URLs carry a version; (b) the list of specialties, changing a few times a year; (c) tomorrow\'s free slots; (d) the user\'s prescriptions. For (b), compute the KB saved over 30 opens a month if the list is 50 KB, max-age is 1 hour, and every open happens after it went stale.')
    B(C, S_, 1, 'hint', 'Cũ một chút có sao không? Đổi thường xuyên không? Có nhạy cảm không?', 'Is a little staleness acceptable? Does it change often? Is it sensitive?')
    B(C, S_, 1, 'sol', '(a) max-age dài (URL đổi khi ảnh đổi), cache bộ nhớ và đĩa. (b) max-age vài giờ kèm ETag. (c) no-cache kèm ETag: luôn hỏi lại, nhưng 304 rẻ. (d) no-store, và nếu cần hiện khi mất mạng thì lưu có chủ đích theo H9, không qua cache HTTP. Phép tính (b): không ETag thì 30 × 50 = 1.500 KB; có ETag và danh sách không đổi trong tháng thì 1 lần 50 KB + 29 lần 304 (khoảng 1 KB) ≈ 79 KB, tiết kiệm khoảng 1.420 KB.',
      '(a) A long max-age (the URL changes when the image does), memory and disk caches. (b) A max-age of a few hours plus an ETag. (c) no-cache plus an ETag: always revalidate, but a 304 is cheap. (d) no-store, and if it must show offline, store it deliberately per H9, not through the HTTP cache. The arithmetic for (b): without an ETag, 30 × 50 = 1,500 KB; with an ETag and no change that month, one 50 KB download + 29 × 304s (about 1 KB) ≈ 79 KB, saving about 1,420 KB.')

    S_ = 'honest'
    a(C + '.sec.%s.title' % S_, 'Chương này giản lược những gì', 'What this chapter simplifies')
    a(C + '.sec.%s.badge' % S_, 'simplified')
    B(C, S_, 1, 'p', 'Độ tươi, heuristic 10%, dùng bản cũ khi mất mạng, kiểm tra lại và các directive theo RFC 9111 (6/2022); ETag mạnh và yếu, If-None-Match, 304 theo RFC 9110; cân nhắc khi cache theo Alex Xu tập 1; đọc ngày 2026-11-24, diễn đạt lại. Kích thước, giá, mốc phút, việc process bị giết giữa phút 2 và 10, 1 KB cho một 304 và gợi ý header theo loại dữ liệu là của site. Chương không bàn Vary, Age, s-maxage chi tiết, hay CDN; directive immutable không nằm trong RFC 9111 nên không nhắc.',
      'Freshness, the 10% heuristic, serving stale when offline, validation and the directives follow RFC 9111 (June 2022); strong and weak ETags, If-None-Match and 304 follow RFC 9110; cache considerations follow Alex Xu vol. 1; read on 2026-11-24, paraphrased. The sizes, fees, minute marks, the process dying between minutes 2 and 10, 1 KB per 304 and the per-data header suggestions are the site\'s. The chapter does not cover Vary, Age, s-maxage in depth, or CDNs; the immutable directive is not in RFC 9111, so it is not mentioned.')

    for q, qv, qe, av, ae, wv, we in [
        ('q1', 'Cache-Control: no-cache có nghĩa là không được lưu không?', 'Does Cache-Control: no-cache mean "do not store"?', 'Không. Được lưu, nhưng phải kiểm tra lại với server trước khi dùng. Không lưu là no-store.', 'No. It may be stored but must be validated before use. Not storing is no-store.', 'Hai directive hay bị nhầm nhất.', 'The two most commonly confused directives.'),
        ('q2', '304 Not Modified mang theo gì?', 'What does a 304 Not Modified carry?', 'Chỉ header, không có nội dung; app dùng lại bản đã lưu.', 'Only headers, no content; the app reuses its stored copy.', 'Vì vậy hỏi lại bằng ETag rẻ hơn tải lại nhiều.', 'That is why revalidating with an ETag is much cheaper than reloading.'),
        ('q3', 'Server không gửi header cache nào. Cache có thể làm gì?', 'The server sends no cache headers. What may a cache do?', 'Tự đoán thời gian sống (heuristic), ví dụ khoảng 10% thời gian từ Last-Modified.', 'Guess a lifetime (heuristic), for example about 10% of the time since Last-Modified.', 'Nên đặt header rõ ràng để không phải đoán.', 'Set explicit headers so nothing has to guess.'),
        ('q4', 'Vì sao cache trong bộ nhớ không đủ cho màn bảng giá?', 'Why is an in-memory cache not enough for the fee screen?', 'Vì nó mất khi process bị giết; lần mở sau phải dựa vào đĩa hay mạng.', 'Because it is lost when the process is killed; the next open relies on disk or the network.', 'Xem chương I2.', 'See chapter I2.')]:
        a(C + '.quiz.%s.q' % q, qv, qe); a(C + '.quiz.%s.a' % q, av, ae); a(C + '.quiz.%s.why' % q, wv, we)
