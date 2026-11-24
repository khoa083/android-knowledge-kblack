# Thiết kế hệ thống phía mobile · I0: bản đồ track (viết cuối, đặt đầu track)
# Tổng hợp từ I1–I13; mọi khẳng định có nguồn ở chương được trỏ tới. Trần: 6 mục.

SEC_ORDER = {'i0': ['hook', 'order', 'index', 'links', 'recall']}


def add(a):
    def B(ch, sec, n, field, vi, en=None):
        a('%s.sec.%s.b.%02d.%s' % (ch, sec, n, field), vi, vi if en is None else en)

    m = lambda k, vi, en=None: a('m.map.' + k, vi, en)
    m('title', 'Gặp triệu chứng này thì đọc chương nào', 'Seen this symptom? Read this chapter')
    m('overview', 'Chọn một lỗi hay gặp khi thiết kế app. Bốn bước: triệu chứng, lúc nó lộ ra (ngoài đời thật, khi đông người hay lâu ngày, khi có nhiều máy, hay sau một lần phát hành), nguyên nhân, và chương giải thích.',
      'Pick a common app design bug. Four steps: the symptom, when it shows up (in the real world, at scale or over time, across devices, or after a release), the cause, and the chapter that explains it.')
    m('wrapup', 'Lỗi thiết kế hệ thống hiếm khi lộ ra trên máy của đội phát triển: mạng ở văn phòng tốt, app không bị giết, chỉ có một máy, và dữ liệu không đổi giữa chừng. Biết lỗi lộ ra lúc nào giúp bạn thử đúng điều kiện trước khi phát hành: mạng yếu, máy ngủ, nhiều máy, bản cũ còn chạy.',
      'System design bugs rarely show up on a developer\'s device: the office network is good, the app is never killed, there is one device, and data does not change midway. Knowing when a bug shows up tells you which conditions to test before shipping: weak networks, sleeping devices, several devices, old versions still running.')
    m('simp.1', 'Mỗi triệu chứng chỉ trỏ tới một chương chính; lỗi thật có thể có nhiều nguyên nhân cùng lúc. App phòng khám, con số và mốc thời gian trong các mô phỏng là của site. Phần lớn sách system design viết cho backend; track chỉ lấy phần áp được vào app. Dịch vụ bên thứ ba như FCM (dịch vụ đẩy của Google) chỉ được nhắc làm ví dụ, vì API của chúng đổi liên tục.', 'Each symptom points to one main chapter; real bugs can have several causes at once. The clinic app, the numbers and the timings in the simulations are the site\'s. Most system design books are written for the backend; the track takes only what applies to apps. Third-party services such as FCM (Google\'s push service) appear only as examples because their APIs change constantly.')
    m('ctl.hint', 'Chọn triệu chứng rồi đi bốn bước; tab "Bảng tra" liệt kê tất cả.', 'Pick a symptom and walk the four steps; the "Lookup table" tab lists them all.')
    m('ctl.symptom', 'Triệu chứng', 'Symptom')
    m('diagramTitle', 'Triệu chứng, lúc lộ ra, nguyên nhân, chương', 'Symptom, when it shows, cause, chapter')
    m('diagramDesc', 'Từ điều bạn thấy tới chương cần đọc', 'From what you see to the chapter to read')
    for k, vi, en in [('symptom', 'Triệu chứng', 'Symptom'), ('phase', 'Lộ ra lúc', 'Shows up'), ('cause', 'Nguyên nhân', 'Cause'), ('chapter', 'Chương', 'Chapter')]:
        m('n.' + k, vi, en)
    m('met.phase', 'Lộ ra lúc', 'Shows up'); m('met.chapter', 'Chương', 'Chapter')
    m('phase.none', 'chưa xét', 'not yet'); m('ch.none', 'chưa xét', 'not yet')
    for k, vi, en, xv, xe in [
        ('field', 'ngoài đời thật', 'in the real world', 'Chỉ lộ khi mạng yếu hay mất, máy ngủ, hay hệ thống giết process: những điều văn phòng hiếm có.', 'Only shows on weak or lost networks, sleeping devices, or when the system kills the process: rare in an office.'),
        ('scale', 'khi đông người hay lâu ngày', 'at scale or over time', 'Chỉ lộ khi nhiều người cùng dùng, dữ liệu đổi liên tục, hay sau một thời gian.', 'Only shows with many users, constantly changing data, or after some time.'),
        ('device', 'khi có nhiều máy hay máy khác', 'across devices', 'Chỉ lộ khi một người dùng nhiều máy, hay trên máy có cấu hình khác máy thử.', 'Only shows when one user has several devices, or on devices unlike the test ones.'),
        ('update', 'sau một lần phát hành', 'after a release', 'Chỉ lộ sau khi bản mới, cấu hình mới hay API mới ra ngoài, khi bản cũ vẫn còn chạy.', 'Only shows after a new version, config or API ships, while old versions still run.')]:
        m('phase.' + k, vi, en); m('phase.%s.explain' % k, xv, xe)
    SY = [
        ('blankOffline', 'Mất mạng là màn hình trống trơn', 'No network means a blank screen', 'Bản thiết kế chỉ có trạng thái đẹp; ngoài đời màn hình trắng khi mất sóng.', 'The design only had the happy state; in the real world the screen goes blank without signal.',
         'Không hỏi trạng thái lỗi, rỗng, mất mạng trước khi làm', 'Error, empty and offline states never asked about', 'Yêu cầu phụ không hiện trên bản thiết kế.', 'Secondary requirements are not on the mockup.', 'Hỏi designer và backend trước khi viết mã (chương I1).', 'Ask the designer and backend before coding (chapter I1).', 'i1', 'field'),
        ('formLost', 'Quay lại từ Camera, form trống trơn', 'Back from the Camera, the form is empty', 'Người dùng chụp ảnh giấy tờ rồi quay lại: mọi thứ vừa nhập biến mất.', 'The user photographs a document and returns: everything entered is gone.',
         'Dữ liệu chỉ nằm trong ViewModel (đối tượng giữ dữ liệu cho màn hình)', 'Data lived only in the ViewModel (the object holding data for the screen)', 'Hệ thống giết process lúc app ở nền.', 'The system killed the process in the background.', 'Saved state (chỗ hệ thống giữ lại dữ liệu nhỏ qua lúc process bị giết) cho phần vừa nhập (chương I2).', 'Saved state (a place where the system keeps small data across process death) for what was just entered (chapter I2).', 'i2', 'field'),
        ('anr', 'App đứng rồi ANR (app không phản hồi) khi đồng bộ', 'The app freezes, then an ANR (app not responding) while syncing', 'Chỉ khi đồng bộ chạy cùng lúc người dùng mở màn hình.', 'Only when sync runs while the user opens the screen.',
         'Luồng chính chờ lock (khóa) do luồng nền giữ', 'The main thread waits for a lock held by a background thread', 'Có khi các lock chờ nhau thành vòng tròn: deadlock.', 'Sometimes the locks form a cycle: deadlock.', 'Không giữ lock lâu, lấy lock theo một thứ tự cố định (chương I3).', 'Hold locks briefly, in one order (chapter I3).', 'i3', 'field'),
        ('battery', 'Pin tụt nhanh khi app chỉ nằm ở nền', 'Battery drains while the app just sits in the background', 'Người dùng gỡ app vì hao pin.', 'Users uninstall the app over battery drain.',
         'Polling (hỏi server liên tục) vài giây một lần', 'Polling (asking the server over and over) every few seconds', 'Mỗi lần gọi giữ radio (bộ thu phát sóng của máy) thức thêm một lúc.', 'Each call keeps the radio (the phone\'s transmitter and receiver) awake for a while.', 'Dùng push hay kết nối hợp với việc (chương I4).', 'Use push or a channel fit for the job (chapter I4).', 'i4', 'field'),
        ('doubleBooking', 'Một lần bấm, hai lịch hẹn', 'One tap, two appointments', 'Mạng chập chờn, app báo lỗi rồi tự thử lại.', 'On a flaky network the app reports an error and retries.',
         'Thử lại không có khóa chống trùng (idempotency key: mã giúp server nhận ra lần thử lại)', 'Retrying without a duplicate key (an idempotency key: a code that lets the server recognise a retry)', 'Response mất chứ không phải request mất.', 'The response was lost, not the request.', 'Idempotency key và backoff có jitter (khoảng chờ giãn dần, cộng thêm phần ngẫu nhiên) (chương I5).', 'An idempotency key and backoff with jitter (growing waits plus some randomness) (chapter I5).', 'i5', 'field'),
        ('oldPrice', 'Giá đã đổi mà app vẫn hiện giá cũ', 'The fee changed but the app shows the old one', 'Chỉ một số người dùng, kéo dài nhiều ngày.', 'Only some users, lasting for days.',
         'Cache không có hạn dùng', 'A cache with no expiry', 'Server không gửi Cache-Control (header cho biết được lưu bao lâu), app lưu mãi.', 'The server sent no Cache-Control (the header saying how long to cache); the app stores forever.', 'max-age (thời gian bản lưu còn tươi) kèm ETag (nhãn phiên bản) (chương I6).', 'max-age (how long the stored copy stays fresh) plus an ETag (a version label) (chapter I6).', 'i6', 'update'),
        ('dupPost', 'Cuộn danh sách thấy một bài hai lần', 'Scrolling shows one post twice', 'Chỉ vào giờ đăng bài nhiều.', 'Only at busy publishing hours.',
         'Phân trang bằng offset (bỏ qua bấy nhiêu mục đầu)', 'Offset paging (skip that many items from the start)', 'Bài mới chèn lên đầu làm vị trí trôi.', 'New posts at the top shift the positions.', 'Cursor (đánh dấu chỗ dừng bằng nội dung, qua page_token) (chương I7).', 'A cursor (marks where you stopped by content, through a page_token) (chapter I7).', 'i7', 'scale'),
        ('overwritten', 'Sửa trên máy tính bảng bị điện thoại ghi đè', 'Edits on the tablet are overwritten by the phone', 'Không có lỗi nào, thông tin dị ứng biến mất.', 'No error at all; the allergy information vanishes.',
         'Ghi sau thắng, gửi cả bản ghi', 'Last write wins, sending the whole record', 'Bản cũ trên máy kia đè bản mới.', 'The old copy on the other device clobbers the new one.', 'If-Match (chỉ ghi nếu server vẫn ở đúng bản này) hay gộp theo trường (chương I8).', 'If-Match (write only if the server is still at this exact version) or per-field merging (chapter I8).', 'i8', 'device'),
        ('wrongTime', 'Thông báo hiện giờ khám cũ', 'The notification shows the old visit time', 'Đổi giờ hai lần liên tiếp, máy đang ngủ.', 'The time changed twice while the phone slept.',
         'Đặt dữ liệu vào push', 'Data inside the push', 'Push không bảo đảm thứ tự hay đúng một lần.', 'Push guarantees neither order nor exactly-once.', 'Push chỉ là tín hiệu, giờ lấy từ server (chương I9).', 'Push as a signal, the time from the server (chapter I9).', 'i9', 'field'),
        ('oom', 'Màn ảnh crash OutOfMemoryError (hết RAM)', 'The photo screen crashes with OutOfMemoryError (out of RAM)', 'Chỉ trên máy có camera độ phân giải cao.', 'Only on phones with high-resolution cameras.',
         'Giải mã thẳng ảnh gốc', 'Decoding the original image', 'RAM của ảnh tính theo số điểm ảnh, không theo kích thước tệp.', 'Memory follows the pixel count, not the file size.', 'Giải mã theo kích thước hiển thị (chương I10).', 'Decode for the display size (chapter I10).', 'i10', 'device'),
        ('uploadRestart', 'Upload 200 MB đứt khi đã gửi 195 MB, phải làm lại từ đầu', 'A 200 MB upload drops after 195 MB and restarts', 'Trên mạng di động chập chờn.', 'On flaky mobile networks.',
         'Một request duy nhất cho cả tệp', 'One request for the whole file', 'Đứt là mất hết phần đã gửi.', 'A drop loses everything sent.', 'Upload tiếp tục được theo khúc (chương I10).', 'A resumable upload in chunks (chapter I10).', 'i10', 'field'),
        ('slowStart', 'Mở app mất 4 giây', 'The app takes 4 seconds to open', 'Tăng dần qua từng bản phát hành khi thêm SDK (thư viện của bên khác).', 'Growing release by release as SDKs (third-party libraries) are added.',
         'Khởi tạo mọi thứ trong Application.onCreate (hàm app chạy đầu tiên)', 'Initialising everything in Application.onCreate (the first function the app runs)', 'Mọi việc đó nằm trên đường tới khung hình đầu.', 'All of it sits on the path to the first frame.', 'Chỉ thứ cần ngay; còn lại để lười hay chạy nền (chương I11).', 'Only what is needed now; the rest lazy or in the background (chapter I11).', 'i11', 'update'),
        ('oldAppCrash', 'Bản app cũ crash ngay sau khi server đổi API', 'Old app versions crash right after an API change', 'Người dùng chưa cập nhật mở màn lịch hẹn thì lỗi.', 'Users who have not updated see the bookings screen fail.',
         'Đổi tên hay bỏ trường tại chỗ', 'Renaming or removing a field in place', 'App cũ không đổi được nữa.', 'Old apps can no longer change.', 'Chỉ thêm vào, hay mở phiên bản API mới (chương I12).', 'Only add, or open a new API version (chapter I12).', 'i12', 'update'),
        ('chatLost', 'Tin nhắn gửi lúc mất mạng không bao giờ tới', 'A message sent while offline never arrives', 'Người dùng tắt app sau khi bấm gửi trong thang máy.', 'The user closed the app after tapping send in a lift.',
         'Gửi trong coroutine (việc chạy nền trong Kotlin) của màn hình, không có outbox (hộp tin chờ gửi)', 'Sending in a screen coroutine (Kotlin background work), no outbox (a box of unsent messages)', 'App đóng là không còn ai gửi.', 'Once the app closes nobody sends it.', 'Outbox trên đĩa, WorkManager (công cụ chạy việc nền của Android), khóa chống trùng (chương I13).', 'An on-disk outbox, WorkManager (Android\'s tool for background work), a duplicate key (chapter I13).', 'i13', 'field'),
    ]
    for sid, tv, te, dv, de, cv, ce, cdv, cde, fv, fe, ch, ph in SY:
        m('s.%s.title' % sid, tv, te); m('s.%s.detail' % sid, dv, de); m('s.%s.cause' % sid, cv, ce); m('s.%s.causeDetail' % sid, cdv, cde); m('s.%s.fix' % sid, fv, fe)
        m('ctl.symptom.' + sid, tv, te)
    for h, vi, en in [('i1', 'I1 · Từ đề bài tới kế hoạch', 'I1 · From a brief to a plan'), ('i2', 'I2 · Process và cái chết của process', 'I2 · Processes and process death'), ('i3', 'I3 · Luồng, khóa, ANR, deadlock', 'I3 · Threads, locks, ANRs, deadlock'),
                      ('i4', 'I4 · Chọn kênh giao tiếp', 'I4 · Choosing a channel'), ('i5', 'I5 · Mạng không tin cậy', 'I5 · Unreliable networks'), ('i6', 'I6 · Cache', 'I6 · Caching'),
                      ('i7', 'I7 · Phân trang', 'I7 · Paging'), ('i8', 'I8 · Nhiều thiết bị và xung đột', 'I8 · Multiple devices and conflicts'), ('i9', 'I9 · Thông báo đẩy', 'I9 · Push notifications'),
                      ('i10', 'I10 · Ảnh và tệp lớn', 'I10 · Images and large files'), ('i11', 'I11 · Khởi động, pin, kích thước', 'I11 · Startup, battery, size'), ('i12', 'I12 · Phát hành an toàn', 'I12 · Safe releases'),
                      ('i13', 'I13 · Bài mẫu nhắn tin', 'I13 · Worked messaging example')]:
        m('ch.' + h, vi, en); m('go.' + h, 'Đọc ' + vi, 'Read ' + en)
    m('co.try', 'Chọn một triệu chứng bạn từng gặp; đi bốn bước rồi mở chương được chỉ tới.', 'Pick a symptom you have met; walk the four steps, then open the chapter pointed to.')
    m('co.cause', 'Nguyên nhân thường là một quyết định thiết kế, không phải một dòng sai lẻ.', 'The cause is usually a design decision, not a single wrong line.')
    m('co.chapter', 'Chương được chỉ tới có mô phỏng đúng tình huống này, cách sửa và nguồn.', 'The chapter pointed to simulates exactly this case, with the fix and sources.')
    a('cap.map', 'Từ trái sang phải: triệu chứng, lúc nó lộ ra, nguyên nhân, chương giải thích. Tab "Bảng tra" liệt kê mọi triệu chứng.', 'Left to right: the symptom, when it shows up, the cause, the chapter that explains it. The "Lookup table" tab lists every symptom.')
    a('preset.map', 'Thiết kế hệ thống · bản đồ triệu chứng và chương', 'System design · symptom map to chapters')

    z = lambda k, vi, en=None: a('vz.' + k, vi, en)
    z('tab.map', 'Bảng tra', 'Lookup table')
    z('map.cap', 'Mọi triệu chứng của track, lúc chúng lộ ra và chương giải thích. Hàng đang chọn được viền; ô "?" mở dần theo bước.', 'Every symptom in the track, when it shows up and the chapter that explains it. The chosen row is outlined; "?" cells open step by step.')
    z('map.legend', 'Tám trong mười bốn triệu chứng chỉ lộ ra ngoài đời thật (mạng yếu, máy ngủ, process bị giết): thử ở điều kiện đó trước khi phát hành.', 'Eight of the fourteen symptoms only show up in the real world (weak networks, sleeping devices, killed processes): test under those conditions before shipping.')
    for k, vi, en in [('sym', 'Triệu chứng', 'Symptom'), ('phase', 'Lộ ra lúc', 'Shows up'), ('ch', 'Chương', 'Chapter')]:
        z('map.col.' + k, vi, en)

    C = 'i0'
    a(C + '.title', 'Bản đồ track: triệu chứng và chương', 'Track map: symptoms and chapters')
    a(C + '.essence', 'Track này dạy thiết kế hệ thống nhìn từ phía app Android: những gì máy của đội phát triển không cho thấy, như process bị giết, mạng không tin cậy, nhiều máy, bản cũ còn chạy, theo tài liệu chính thức và sách system design.\nPhần 1 (I1–I5) là nền: lập kế hoạch, process và bộ nhớ, luồng và khóa, chọn kênh, mạng không tin cậy. Phần 2 (I6–I12) là các chủ đề: cache, phân trang, xung đột, thông báo đẩy, tệp lớn, khởi động, phát hành an toàn. I13 ghép tất cả vào một app nhắn tin.\nNếu bạn đang gặp một lỗi cụ thể, bắt đầu từ bảng tra triệu chứng bên dưới.',
      'This track teaches system design seen from the Android app: what a developer\'s device does not show, such as process death, unreliable networks, multiple devices and old versions still running, following official docs and system design books.\nPart 1 (I1–I5) is the foundation: planning, processes and memory, threads and locks, choosing a channel, unreliable networks. Part 2 (I6–I12) covers the topics: caching, paging, conflicts, push, large files, startup, safe releases. I13 puts it all together in a messaging app.\nIf you are facing a specific bug, start from the symptom lookup table below.')
    a(C + '.goal.g1', 'Đã thấy lúc triệu chứng lộ ra', 'Saw when the symptom shows up')
    a(C + '.goal.g2', 'Đã tới chương cần đọc', 'Reached the chapter to read')
    a(C + '.sim.sysdesign.map', 'triệu chứng và chương', 'symptoms and chapters')

    S_ = 'hook'
    a(C + '.sec.%s.title' % S_, 'Đoán trước khi đọc', 'Predict before reading')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'predict', 'Trong 14 triệu chứng của bảng tra, bạn đoán bao nhiêu cái máy của đội phát triển (Wi-Fi văn phòng, không bị giết, một máy, luôn bản mới nhất) sẽ không bao giờ gặp?',
      'Of the 14 symptoms in the lookup table, how many do you guess a developer\'s device (office Wi-Fi, never killed, one device, always the latest version) would never hit?')
    B(C, S_, 1, 'ans', 'Gần như tất cả. Tám cái chỉ lộ ngoài đời thật, hai cái cần nhiều máy hay máy khác, ba cái chỉ lộ sau một lần phát hành, và một cái cần đông người. Đây là đếm trên bảng của site, không phải thống kê.',
      'Almost all of them. Eight only show in the real world, two need several or different devices, three only after a release, and one needs scale. This counts the site\'s table, not a statistic.')

    S_ = 'order'
    a(C + '.sec.%s.title' % S_, 'Thứ tự đọc', 'Reading order')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'p', 'Đọc I1 trước: nó đặt cách hỏi trước khi thiết kế. I2 và I3 là nền về process và luồng. I4 → I5 nối tiếp (chọn kênh, rồi xử lý khi kênh hỏng). I6 tới I12 đọc riêng được, nhưng I8 dùng ETag (nhãn phiên bản) của I6, I9 dùng I4 và I5, I10 dùng I2 và I5. I13 nên đọc cuối. Nên biết trước ba chương A1–A3 của track Kotlin Coroutines Explorer và chương G4, "Data layer: repository, data source và offline-first", của track Kiến trúc app Android.',
      'Read I1 first: it sets the habit of asking before designing. I2 and I3 are the foundation on processes and threads. I4 → I5 build on each other (choosing a channel, then handling its failures). I6 to I12 stand alone, though I8 uses I6\'s ETags (version labels), I9 uses I4 and I5, I10 uses I2 and I5. Read I13 last. Knowing chapters A1–A3 of the Kotlin Coroutines Explorer track and chapter G4, "The data layer: repositories, data sources and offline-first", of the Android App Architecture track first helps.')

    S_ = 'index'
    a(C + '.sec.%s.title' % S_, 'Chỉ mục: mỗi chương dùng hình gì', 'Index: the visual of each chapter')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'p', 'I1: bảng câu hỏi và bảng ước lượng. I2: thang bậc process và thanh RAM. I3: làn thời gian hai luồng và đồ thị chờ. I4: sơ đồ tuần tự từng kênh. I5: sơ đồ tuần tự và làn thử lại. I6: bảng ba tầng cache và bảng header. I7: hai dãy ô server và app. I8: làn ba bên và bảng gộp theo trường. I9: sơ đồ tuần tự và bảng bảo đảm. I10: bảng tính RAM của ảnh và dãy khúc upload. I11: làn thời gian khởi động. I12: dãy ô theo ngày và ma trận phiên bản. I13: đồ thị thành phần và sơ đồ tuần tự.',
      'I1: a question table and an estimate table. I2: a process ladder and a RAM bar. I3: two-thread lanes and a wait-for graph. I4: a sequence diagram per channel. I5: a sequence diagram and retry lanes. I6: a three-tier cache table and a header table. I7: two strips, server and app. I8: three-party lanes and a per-field merge table. I9: a sequence diagram and a guarantees table. I10: an image memory worksheet and an upload chunk strip. I11: a startup timeline. I12: a day-by-day strip and a version matrix. I13: a component graph and a sequence diagram.')

    S_ = 'links'
    a(C + '.sec.%s.title' % S_, 'Cầu nối sang track khác', 'Bridges to other tracks')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'p', 'I2 nối với chương "Quản lý state: stateless, hoisting, ai giữ state và sống qua tái tạo" của track Compose Runtime Explorer; I3 nối với chương "Trạng thái chung và kiểm thử coroutine" của track Kotlin Coroutines Explorer; I6 nối với chương G4 của track Kiến trúc app Android, nơi database là nguồn sự thật. Outbox (hộp tin chờ gửi) và WorkManager ở I5, I10, I13 dùng cơ chế của chương "Offline-first và đồng bộ nền" (H7) của track Lưu dữ liệu trên Android.',
      'I2 links to the chapter "Managing state: stateless composables, hoisting, who owns state, and surviving recreation" of the Compose Runtime Explorer track; I3 to the chapter "Shared state and testing coroutines" of the Kotlin Coroutines Explorer track; I6 to chapter G4 of the Android App Architecture track, where the database is the source of truth. The outbox (a box of unsent messages) and WorkManager in I5, I10 and I13 use the mechanics of the chapter "Offline-first and background sync" (H7) of the Saving Data on Android track.')

    S_ = 'recall'
    a(C + '.sec.%s.title' % S_, 'Tự trả lời', 'Answer it yourself')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'ask', 'Bốn điều kiện nào máy của đội phát triển hay thiếu khi thử một thiết kế?', 'Which four conditions does a developer\'s device usually lack when testing a design?')
    B(C, S_, 1, 'ans', 'Mạng yếu hay mất và máy ngủ; process bị giết; nhiều máy cho một người; bản app cũ vẫn chạy khi server đổi.', 'Weak or lost networks and a sleeping device; process death; several devices per user; old app versions still running when the server changes.')

    for q, qv, qe, av, ae, wv, we in [
        ('q1', 'Một lần bấm "Đặt lịch" tạo hai lịch: đọc chương nào?', 'One "Book" tap creates two appointments: which chapter?', 'I5 · Mạng không tin cậy.', 'I5 · Unreliable networks.', 'Thử lại sau khi hết thời gian chờ cần idempotency key (mã giúp server nhận ra lần thử lại).', 'Retrying after a timeout needs an idempotency key (a code that lets the server recognise a retry).'),
        ('q2', 'Cuộn danh sách thấy bài lặp: đọc chương nào?', 'Scrolling shows a duplicate post: which chapter?', 'I7 · Phân trang.', 'I7 · Paging.', 'Offset trôi khi có bài chèn lên đầu.', 'Offsets drift when posts are inserted at the top.'),
        ('q3', 'App cũ crash ngay sau khi backend đổi API: đọc chương nào?', 'Old apps crash right after a backend API change: which chapter?', 'I12 · Phát hành an toàn.', 'I12 · Safe releases.', 'Đổi API phải giữ tương thích với bản cũ.', 'API changes must stay compatible with old versions.')]:
        a(C + '.quiz.%s.q' % q, qv, qe); a(C + '.quiz.%s.a' % q, av, ae); a(C + '.quiz.%s.why' % q, wv, we)
