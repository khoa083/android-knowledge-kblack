# Gỡ lỗi và hiệu năng · l9: CPU, trace và khung hình giật (Phần 2: nhìn vào bên trong app)
# Nguồn (chỉ ghi ở đây và docs/research/debugging.md), đọc 2026-11-25: developer.android.com/topic/performance/vitals/render (16 ms ở 60 fps, 11 ms ở 90, 8 ms ở 120;
# quá hạn thì Choreographer bỏ cả khung; khung chậm 16–700 ms, khung đứng 700 ms–5 s; Record View#draw trên luồng UI, DrawFrame trên RenderThread; nguyên nhân;
# mỗi trace marker tốn khoảng 10 µs, đừng gắn cho hàm ngắn hơn khoảng 200 µs; method trace cho giật giả vì chi phí lớn và không thấy luồng chạy hay bị chặn),
# topic/performance/tracing (system trace gom dữ liệu kernel: lập lịch CPU, đĩa, luồng của app; Perfetto từ Android 10), tracing/custom-events (androidx.tracing trace { };
# app phải profileable), studio/profile/record-traces (khung trên main thread và RenderThread), perfetto.dev/docs (công cụ mã nguồn mở, UI chạy trong trình duyệt, SQL).
# Số ms của từng khung và 12 khung một lần cuộn là của site.

SEC_ORDER = {'l9': ['hook', 'budget', 'trace', 'sections', 'method', 'bugs', 'ex', 'recall']}


def add(a):
    def B(ch, sec, n, field, vi, en=None):
        a('%s.sec.%s.b.%02d.%s' % (ch, sec, n, field), vi, vi if en is None else en)

    a('preset.jank', '''Gỡ lỗi · khung hình giật khi cuộn''', '''Debugging · janky frames while scrolling''')
    m = lambda k, vi, en=None: a('m.jank.' + k, vi, en)
    m('title', '''Cuộn danh sách lịch hẹn bị giật''', '''Scrolling the booking list stutters''')
    m('overview', '''Danh sách lịch hẹn giật mỗi khi cuộn tới trang mới. System trace của một lần cuộn có 12 khung hình. Cách 1 parse JSON của trang mới ngay trên luồng main trong lúc bind. Cách 2 parse trước trên một luồng nền và chỉ bind trên main. Ta xem khung nào quá hạn, quá bao nhiêu, ở 60 Hz rồi ở 120 Hz. Thời lượng từng khung và số vsync bị lỡ được tính thật.''',
      '''The booking list stutters whenever scrolling reaches a new page. A system trace of one scroll has 12 frames. Way 1 parses the new page\'s JSON right on the main thread while binding. Way 2 parses it beforehand on a background thread and only binds on main. We see which frames miss the deadline, and by how much, at 60 Hz and then 120 Hz. Each frame\'s duration and the missed vsyncs are really computed.''')
    m('wrapup', '''Hai khung có việc parse 28 ms trên main dài 34,5 ms, quá hạn 16 ms, nên mỗi khung làm lỡ 2 vsync ở 60 Hz và 4 vsync ở 120 Hz. Trace chỉ đúng chỗ: luồng main bận, RenderThread rảnh, và đoạn trace tên parseJson chiếm gần hết khung. Dời việc parse sang luồng nền thì mọi khung dưới 8 ms, không khung nào trễ kể cả ở 120 Hz.''',
      '''The two frames with 28 ms of parsing on main take 34.5 ms, over the 16 ms deadline, so each misses 2 vsyncs at 60 Hz and 4 at 120 Hz. The trace points to the exact spot: the main thread busy, RenderThread idle, and a trace section named parseJson taking most of the frame. Moving the parsing to a background thread keeps every frame under 8 ms, with no late frame even at 120 Hz.''')
    m('simp.1', '''Mỗi khung chỉ chia làm phần việc trên luồng main và trên RenderThread nối tiếp nhau; khung thật còn chồng lấn giữa hai luồng và có thêm input, animation.''',
      '''Each frame is split only into main-thread work and RenderThread work in sequence; real frames also overlap between the two threads and include input and animation.''')
    m('simp.2', '''Thời lượng khung, khung trễ và số vsync bị lỡ (ceil(thời lượng ÷ hạn) − 1) được tính thật bằng JavaScript từ số ms của từng phần việc; các số ms là của site.''',
      '''Frame durations, late frames and missed vsyncs (ceil(duration ÷ deadline) − 1) are really computed in JavaScript from each piece of work\'s milliseconds; the millisecond figures are the site\'s.''')
    m('ctl.hint', '''Chọn chỗ parse rồi đi qua bốn bước; xem khung nào chuyển đỏ và vạch vsync.''', '''Pick where parsing happens and walk the four steps; watch which frames turn red and the vsync marks.''')
    m('ctl.case', '''Parse JSON ở đâu''', '''Where JSON is parsed''')
    m('ctl.case.main', '''trên luồng main, lúc bind''', '''on the main thread, while binding'''); m('ctl.case.bg', '''trên luồng nền, trước khi hiện''', '''on a background thread, before showing''')
    m('diagramTitle', '''Một khung hình đi qua đâu''', '''Where a frame goes''')
    m('diagramDesc', '''vsync kích khung; luồng main ghi lệnh vẽ; RenderThread vẽ; quá hạn thì khung bị bỏ''', '''vsync starts a frame; the main thread records drawing; RenderThread draws; past the deadline the frame is dropped''')
    for k, vi, en in [('vsync', 'vsync: hạn khung hình', 'vsync: the frame deadline'), ('main', 'Luồng main: bind, layout, ghi lệnh vẽ', 'Main thread: bind, layout, record drawing'),
                      ('render', 'RenderThread: vẽ', 'RenderThread: draw'), ('worker', 'Luồng nền: parse JSON', 'Background thread: parse JSON'), ('screen', 'Màn hình', 'Screen')]:
        m('n.' + k, vi, en)
    m('met.hz', '''Tần số làm tươi''', '''Refresh rate'''); m('met.budget', '''Hạn mỗi khung (ms)''', '''Deadline per frame (ms)''')
    m('met.late', '''Khung trễ (trên 12)''', '''Late frames (of 12)'''); m('met.missed', '''Vsync bị lỡ''', '''Missed vsyncs''')
    a('cap.jank', '''Mỗi vsync mở một khung; luồng main và RenderThread phải xong trước vsync kế tiếp. Ô đỏ: chỗ làm khung quá hạn.''', '''Each vsync opens a frame; the main thread and RenderThread must finish before the next vsync. A red box: what makes the frame late.''')
    S = [
        ('main', 's1', 'System trace một lần cuộn: 2 trong 12 khung đỏ', 'A system trace of one scroll: 2 of 12 frames red',
         'Ghi system trace trong lúc cuộn. Mười khung bình thường mất 6,5 ms; hai khung, đúng lúc nạp trang mới, mất 34,5 ms. Hạn ở 60 Hz là 16 ms.',
         'Record a system trace while scrolling. Ten normal frames take 6.5 ms; two frames, exactly when a new page loads, take 34.5 ms. The deadline at 60 Hz is 16 ms.'),
        ('main', 's2', 'Phóng to khung đỏ: luồng main bận parseJson 28 ms', 'Zoom into a red frame: the main thread is busy in parseJson for 28 ms',
         'Trên làn luồng main, khung đỏ có đoạn bindPage 32 ms, bên trong là đoạn trace tự đặt tên parseJson 28 ms. RenderThread chỉ mất 2,5 ms. Vấn đề nằm hẳn ở luồng main.',
         'On the main thread lane, the red frame has a bindPage slice of 32 ms, containing a custom trace section named parseJson of 28 ms. RenderThread takes only 2.5 ms. The problem is entirely on the main thread.'),
        ('main', 's3', 'Quá hạn thì cả khung bị bỏ: lỡ 2 vsync', 'Past the deadline the whole frame is dropped: 2 vsyncs missed',
         'Khung quá hạn không hiện trễ một chút mà bị bỏ hẳn; màn hình giữ hình cũ tới vsync sau. 34,5 ms ở hạn 16 ms chiếm 3 khoảng vsync, tức lỡ 2 vsync mỗi khung, 4 vsync cả lần cuộn. Người dùng thấy như bị khựng.',
         'A late frame is not shown a little late; it is dropped entirely, and the screen keeps the old image until a later vsync. 34.5 ms against a 16 ms deadline spans 3 vsync intervals, so each such frame misses 2 vsyncs, 4 for the whole scroll. The user sees a hitch.'),
        ('main', 's4', 'Ở màn 120 Hz: hạn còn 8 ms, lỡ 4 vsync mỗi khung', 'On a 120 Hz screen: an 8 ms deadline, 4 missed vsyncs per frame',
         'Cùng mã trên máy 120 Hz: khung bình thường 6,5 ms vẫn kịp, nhưng mỗi khung parse lỡ 4 vsync, tổng 8. Màn càng mượt thì việc nặng trên main càng lộ.',
         'The same code on a 120 Hz phone: normal 6.5 ms frames still make it, but each parsing frame misses 4 vsyncs, 8 in total. The smoother the screen, the more heavy main-thread work shows.'),
        ('bg', 's1', 'Parse trên luồng nền: làn mới có đoạn parseJson 28 ms', 'Parsing on a background thread: a new lane holds parseJson for 28 ms',
         'Trang mới được parse trong withContext(Dispatchers.Default) trước khi gửi cho adapter. Trace có thêm một làn luồng nền với đoạn parseJson 28 ms, chạy song song, không chặn khung nào.',
         'The new page is parsed inside withContext(Dispatchers.Default) before it reaches the adapter. The trace gains a background-thread lane with a 28 ms parseJson slice, running in parallel and blocking no frame.'),
        ('bg', 's2', 'Luồng main chỉ bind: khung nạp trang còn 7,5 ms', 'The main thread only binds: the page-load frame is down to 7.5 ms',
         'Khi dữ liệu đã parse xong, khung nạp trang chỉ còn bind 5 ms cộng RenderThread 2,5 ms. Cả 12 khung đều dưới 16 ms; không vsync nào bị lỡ.',
         'With the data already parsed, the page-load frame only binds for 5 ms plus 2.5 ms on RenderThread. All 12 frames are under 16 ms; no vsync is missed.'),
        ('bg', 's3', 'Trace section vẫn ở đó để xác nhận', 'The trace section is still there to confirm',
         'Đoạn trace parseJson giờ nằm trên làn luồng nền, nên trace cho thấy rõ việc đã dời đi đâu. Giữ trace section trong mã giúp lần sau so trước và sau ngay trên cùng một trace.',
         'The parseJson trace section now sits on the background lane, so the trace shows clearly where the work moved. Keeping trace sections in the code makes before-and-after comparisons easy in the same kind of trace.'),
        ('bg', 's4', 'Ở 120 Hz: mọi khung dưới 8 ms', 'At 120 Hz: every frame under 8 ms',
         'Khung bình thường 6,5 ms, khung nạp trang 7,5 ms, đều dưới hạn 8 ms. Không khung nào trễ, kể cả trên màn 120 Hz.',
         'Normal frames 6.5 ms, the page-load frame 7.5 ms, all under the 8 ms deadline. No late frame, even on a 120 Hz screen.'),
    ]
    for case, k, tv, te, xv, xe in S:
        sid = case + '.' + k
        m('s.%s.title' % sid, tv, te); m('s.%s.explain' % sid, xv, xe); m('ev.' + sid, tv, te)
    for k, vi, en in [
        ('try', '''Mẹo đọc: vạch dọc là các vsync; mỗi khối trên làn main là một khung, rộng theo số ms. Khối đỏ là khung quá hạn; làn dưới là RenderThread và luồng nền.''',
         '''Reading tip: vertical marks are vsyncs; each block on the main lane is a frame, as wide as its milliseconds. A red block is a late frame; the lower lanes are RenderThread and the background thread.'''),
        ('main.s2', '''Hãy xem Record View#draw hay Layout có dài bất thường không; việc dài nên chạy bất đồng bộ, ngoài luồng UI. [[src:ad-slow-rendering]]''',
         '''Check whether Record View#draw or Layout is taking abnormally long; long-running work should run asynchronously, off the UI thread. [[src:ad-slow-rendering]]'''),
        ('main.s3', '''Một khung quá hạn dù chỉ 1 ms không được hiện trễ 1 ms: Choreographer bỏ cả khung, và người dùng thấy giật. [[src:ad-slow-rendering]]''',
         '''A frame that overruns by even 1 ms is not shown 1 ms late: Choreographer drops the whole frame, and the user sees jank. [[src:ad-slow-rendering]]'''),
        ('main.s4', '''Để đạt 60 khung mỗi giây, mỗi khung phải xong dưới 16 ms; ở 90 khung là 11 ms, ở 120 khung là 8 ms. [[src:ad-slow-rendering]]''',
         '''To reach 60 frames per second, each frame must finish in under 16 ms; at 90 it is 11 ms, at 120 it is 8 ms. [[src:ad-slow-rendering]]'''),
        ('bg.s1', '''System trace gom dữ liệu từ kernel: lập lịch CPU, hoạt động đĩa, các luồng của app; nên thấy được việc chạy song song trên nhiều luồng. [[src:ad-tracing]]''',
         '''A system trace combines kernel data: CPU scheduling, disk activity, the app\'s threads; so it shows work running in parallel across threads. [[src:ad-tracing]]'''),
        ('bg.s2', '''Mỗi khung có hai pha: ghi lệnh vẽ trên luồng UI, và DrawFrame trên RenderThread dựa trên những lệnh đó. [[src:ad-slow-rendering]]''',
         '''Each frame has two phases: recording drawing on the UI thread, and DrawFrame on RenderThread based on what was recorded. [[src:ad-slow-rendering]]'''),
        ('bg.s3', '''Hàm trace của Jetpack tự kết thúc đoạn trace khi lambda xong, nên không thể quên đóng; app phải ở chế độ profileable thì đoạn trace tự đặt mới hiện. [[src:ad-trace-events]]''',
         '''Jetpack\'s trace function ends the section automatically when the lambda completes, so it cannot be left open; the app must be profileable for custom sections to appear. [[src:ad-trace-events]]'''),
        ('bg.s4', '''Đo lại sau khi sửa, trên cùng loại trace và cùng thao tác, như chương "Đo hiệu năng cho đúng" sẽ nói kỹ.''',
         '''Measure again after the fix, with the same kind of trace and the same action, as the chapter "Measuring performance properly" covers in detail.'''),
    ]:
        m('co.' + k, vi, en)

    z = lambda k, vi, en=None: a('vz.' + k, vi, en)
    z('tab.jank', '''Làn thời gian các luồng''', '''Thread timeline''')
    z('jk.aria', '''Dòng thời gian {n} khung ở {hz} Hz; {l} khung trễ, lỡ {m} vsync''', '''A timeline of {n} frames at {hz} Hz; {l} late frames, {m} missed vsyncs''')
    z('jk.lane.main', '''luồng main''', '''main thread'''); z('jk.lane.render', '''RenderThread (vẽ)''', '''RenderThread (draw)'''); z('jk.lane.worker', '''luồng nền''', '''background''')
    z('jk.sub', '''{hz} Hz, hạn {b} ms: {l} khung trễ, lỡ {m} vsync.''', '''{hz} Hz, deadline {b} ms: {l} late frames, {m} missed vsyncs.''')
    z('jk.focus', '''Khung dài nhất: {t} ms (main {mm} ms, RenderThread {r} ms).''', '''Longest frame: {t} ms (main {mm} ms, RenderThread {r} ms).''')
    z('jk.legend', '''Vạch dọc: vsync. Khối trên làn main: một khung (rộng theo ms); đỏ là quá hạn. Khối vàng nhạt: đoạn trace parseJson.''',
      '''Vertical marks: vsyncs. A block on the main lane: one frame (width by ms); red means late. A pale amber block: the parseJson trace section.''')

    C = 'l9'
    a(C + '.title', '''CPU, trace và khung hình giật''', '''CPU, traces and janky frames''')
    a(C + '.essence', '''Mỗi khung hình có một hạn: 16 ms ở 60 Hz, 11 ms ở 90 Hz, 8 ms ở 120 Hz. Khung quá hạn dù 1 ms cũng bị bỏ cả khung, và người dùng thấy giật (jank). Khung dài hơn 700 ms là khung đứng.\nSystem trace (xem bằng Perfetto hay Android Studio) ghi lại các luồng trên một dòng thời gian: khung nào trễ, luồng main đang làm gì, RenderThread có bận không, luồng đang chạy hay đang chờ. Đặt tên cho đoạn mã nghi ngờ bằng trace("tên") { } để nó hiện trong trace.\nCách đọc: tìm khung đỏ, phóng to, xem đoạn nào trên luồng main chiếm thời gian; việc nặng như parse, đọc đĩa, gọi mạng thì dời khỏi luồng main.''',
      '''Every frame has a deadline: 16 ms at 60 Hz, 11 ms at 90 Hz, 8 ms at 120 Hz. A frame that overruns by even 1 ms is dropped entirely, and the user sees jank. A frame longer than 700 ms is a frozen frame.\nA system trace (viewed in Perfetto or Android Studio) records threads on a timeline: which frames are late, what the main thread is doing, whether RenderThread is busy, whether a thread is running or waiting. Name suspicious code with trace("name") { } so it shows up in the trace.\nHow to read it: find a red frame, zoom in, see which slice on the main thread takes the time; move heavy work such as parsing, disk reads or network calls off the main thread.''')
    a(C + '.goal.g1', '''Đã thấy đoạn nào làm khung quá hạn''', '''Saw which slice makes the frame late''')
    a(C + '.goal.g2', '''Đã thấy hạn khung đổi theo tần số màn''', '''Saw the frame deadline change with the refresh rate''')
    a(C + '.sim.debugging.jank', '''parse trên main, hay trên luồng nền''', '''parsing on main, or on a background thread''')

    S_ = 'hook'
    a(C + '.sec.%s.title' % S_, '''Đoán trước khi đọc''', '''Predict before reading''')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'predict', '''Một khung hình mất 17 ms trên màn 60 Hz, hạn 16 ms. Nó được hiện trễ 1 ms, hay chuyện gì khác xảy ra?''',
      '''A frame takes 17 ms on a 60 Hz screen with a 16 ms deadline. Is it shown 1 ms late, or does something else happen?''')
    B(C, S_, 1, 'ans', '''Nó bị bỏ hẳn: màn hình giữ hình cũ tới vsync sau, nên người dùng thấy khựng một nhịp. Vì vậy chỉ vài khung quá hạn là đủ thấy giật. Mô phỏng ngay dưới tìm khung quá hạn trong một system trace và dời việc nặng ra khỏi luồng main.''',
      '''It is dropped entirely: the screen keeps the old image until a later vsync, so the user sees a hitch. That is why a few late frames are enough to feel jank. The simulation just below finds the late frames in a system trace and moves the heavy work off the main thread.''')

    S_ = 'budget'
    a(C + '.sec.%s.title' % S_, '''Hạn của một khung hình''', '''A frame\'s deadline''')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'p', '''Màn hình làm tươi theo nhịp vsync. Để đạt 60 khung mỗi giây, mỗi khung phải xong dưới 16 ms; màn 90 Hz cho 11 ms, màn 120 Hz chỉ 8 ms. Mỗi khung có hai pha: luồng UI (main) xử lý input, animation, layout và ghi lại lệnh vẽ; RenderThread dựa vào đó để vẽ. Khung quá hạn không được hiện trễ mà bị bỏ hẳn. [[src:ad-slow-rendering]]''',
      '''The screen refreshes on a vsync rhythm. To reach 60 frames per second, each frame must finish in under 16 ms; a 90 Hz screen gives 11 ms, a 120 Hz screen only 8 ms. Each frame has two phases: the UI (main) thread handles input, animation, layout and records the drawing commands; RenderThread draws from them. A late frame is not shown late; it is dropped entirely. [[src:ad-slow-rendering]]''')
    B(C, S_, 2, 'p', '''Android vitals chia ba mức: khung chậm từ 16 tới 700 ms, khung đứng từ 700 ms tới 5 giây, và quá 5 giây là ANR (chương "ANR và StrictMode"). Nguyên nhân hay gặp trên luồng main: parse dữ liệu, đọc đĩa, gọi qua binder, chờ khóa, GC dày (chương "Bộ nhớ: churn, rò rỉ, heap dump"), tải ảnh lên GPU. Với Compose, recompose quá nhiều cũng tốn thời gian của khung; xem chương "Hiệu năng và debug: đo trước, sửa sau" của track Compose Runtime. [[src:ad-slow-rendering]]''',
      '''Android vitals uses three levels: slow frames from 16 to 700 ms, frozen frames from 700 ms to 5 seconds, and over 5 seconds an ANR (the chapter "ANRs and StrictMode"). Common causes on the main thread: parsing data, disk reads, binder calls, lock waits, frequent GC (the chapter "Memory: churn, leaks, heap dumps"), uploading bitmaps to the GPU. With Compose, recomposing too much also eats frame time; see "Performance and debugging: measure first, then fix" in the Compose Runtime track. [[src:ad-slow-rendering]]''')

    S_ = 'trace'
    a(C + '.sec.%s.title' % S_, '''System trace và Perfetto''', '''System traces and Perfetto''')
    a(C + '.sec.%s.badge' % S_, 'version')
    B(C, S_, 1, 'p', '''System trace ghi hoạt động của thiết bị trong một khoảng ngắn, gom dữ liệu từ kernel: lập lịch CPU, hoạt động đĩa, các luồng của app, các khung hình. Từ Android 10, công cụ ghi trace của cả hệ thống là Perfetto, một dự án mã nguồn mở; trace mở được ngay trong trình duyệt tại ui.perfetto.dev, không cần cài đặt, và truy vấn được bằng SQL. Android Studio cũng ghi và hiện system trace, với khung của luồng main và RenderThread. [[src:ad-tracing]] [[src:perfetto-docs]] [[src:ad-record-traces]]''',
      '''A system trace records device activity over a short period, combining kernel data: CPU scheduling, disk activity, the app\'s threads, frames. From Android 10 the platform-wide tracing tool is Perfetto, an open-source project; traces open straight in the browser at ui.perfetto.dev, with no installation, and can be queried with SQL. Android Studio also records and shows system traces, with frames on the main thread and RenderThread. [[src:ad-tracing]] [[src:perfetto-docs]] [[src:ad-record-traces]]''')
    B(C, S_, 2, 'p', '''Câu hỏi khi đọc một trace: khung nào trễ; trong khung đó luồng main đang làm gì (đoạn nào dài nhất); luồng đang chạy hay đang chờ (chờ khóa, chờ đĩa thì cách sửa khác hẳn); RenderThread có phải nút thắt không. System trace không cho thấy chi tiết từng hàm trong app; để thấy, đặt tên cho đoạn mã nghi ngờ (mục kế tiếp). [[src:ad-tracing]]''',
      '''Questions when reading a trace: which frames are late; what the main thread is doing in them (which slice is longest); whether the thread is running or waiting (waiting on a lock or on disk calls for a completely different fix); whether RenderThread is the bottleneck. A system trace does not show the details of each function in your app; to see them, name the suspicious code (next section). [[src:ad-tracing]]''')

    S_ = 'sections'
    a(C + '.sec.%s.title' % S_, '''Đặt tên cho đoạn mã trong trace''', '''Naming code in the trace''')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'kt', '''import androidx.tracing.trace

val items = withContext(Dispatchers.Default) {
    trace("parseJson") { rawRows.map { json.decodeFromString<BookingDto>(it) } }
}
adapter.submitList(items)                 // luồng main chỉ còn bind dữ liệu đã parse''', '''import androidx.tracing.trace

val items = withContext(Dispatchers.Default) {
    trace("parseJson") { rawRows.map { json.decodeFromString<BookingDto>(it) } }
}
adapter.submitList(items)                 // the main thread only binds already-parsed data''')
    B(C, S_, 2, 'p', '''Hàm trace của Jetpack mở một đoạn có tên và tự đóng khi lambda xong, nên không thể quên đóng; các đoạn lồng nhau thành cây. App phải được cấu hình profileable thì đoạn tự đặt mới hiện trong trace. Mỗi đoạn tốn khoảng 10 µs, nên đừng bọc hàm ngắn hơn khoảng 200 µs. [[src:ad-trace-events]] [[src:ad-slow-rendering]]''',
      '''Jetpack\'s trace function opens a named section and closes it when the lambda completes, so it cannot be left open; nested sections form a tree. The app must be configured as profileable for custom sections to appear in the trace. Each section costs roughly 10 µs, so do not wrap functions shorter than about 200 µs. [[src:ad-trace-events]] [[src:ad-slow-rendering]]''')

    S_ = 'method'
    a(C + '.sec.%s.title' % S_, '''Vì sao không bắt đầu bằng method trace''', '''Why not start with a method trace''')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'p', '''Method trace ghi từng lời gọi hàm, nghe chi tiết hơn, nhưng chi phí lớn làm mọi thứ chậm đi: nó cho giật giả, và không phân biệt được luồng đang chạy hay đang bị chặn. Bắt đầu bằng system trace để tìm khung trễ và luồng bận, đặt trace section để thu hẹp, chỉ dùng method trace khi cần biết hàm nào bên trong một đoạn đã khoanh vùng. Đừng tin số đo thời gian lấy khi debugger đang gắn hay method trace đang bật. [[src:ad-slow-rendering]]''',
      '''A method trace records every function call, which sounds more detailed, but its heavy overhead slows everything: it shows false jank, and it cannot tell whether a thread is running or blocked. Start with a system trace to find late frames and busy threads, add trace sections to narrow down, and use a method trace only when you need to know which function inside an already-fenced slice. Do not trust timings taken with the debugger attached or a method trace running. [[src:ad-slow-rendering]]''')

    S_ = 'bugs'
    a(C + '.sec.%s.title' % S_, '''Hai lỗi hay gặp''', '''Two common bugs''')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'bug', '''Màn chi tiết mở chậm nửa giây lần đầu; trace cho thấy luồng main ở trạng thái chờ chứ không chạy.''', '''The details screen takes half a second to open the first time; the trace shows the main thread waiting, not running.''')
    B(C, S_, 1, 'cause', '''Luồng main đọc SharedPreferences lần đầu và phải chờ tệp được nạp từ đĩa.''', '''The main thread reads SharedPreferences for the first time and has to wait for the file to load from disk.''')
    B(C, S_, 1, 'fix', '''Đọc trên luồng nền (hay dùng DataStore với coroutine); trạng thái "chờ" trong trace là manh mối cho I/O hay khóa, không phải tính toán.''', '''Read on a background thread (or use DataStore with coroutines); a "waiting" state in the trace points to I/O or a lock, not computation.''')
    B(C, S_, 2, 'bug', '''Đã "tối ưu" xong vì method trace cho thấy một hàm giảm từ 40 xuống 20 ms, nhưng người dùng vẫn thấy giật.''', '''"Optimised" because a method trace showed one function dropping from 40 to 20 ms, yet users still see jank.''')
    B(C, S_, 2, 'cause', '''Con số lấy khi method trace đang bật nên bị phóng đại; khung thật trễ vì một việc khác trên luồng main.''', '''The numbers were taken with method tracing on, so they were inflated; real frames are late because of other work on the main thread.''')
    B(C, S_, 2, 'fix', '''Đo bằng system trace (hay benchmark) trên bản release, xem khung nào thật sự quá hạn.''', '''Measure with a system trace (or a benchmark) on a release build, and see which frames really miss the deadline.''')

    S_ = 'ex'
    a(C + '.sec.%s.title' % S_, '''Bài tập''', '''Exercise''')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'ex', '''Trên màn 90 Hz, một khung có luồng main 9 ms và RenderThread 4 ms, coi như nối tiếp. Khung có trễ không, lỡ mấy vsync? Nếu dời 6 ms việc trên main sang luồng nền thì sao?''',
      '''On a 90 Hz screen, a frame has 9 ms on the main thread and 4 ms on RenderThread, taken as sequential. Is it late, and how many vsyncs are missed? What if 6 ms of main-thread work moves to a background thread?''')
    B(C, S_, 1, 'hint', '''Hạn ở 90 Hz là 11 ms; số vsync lỡ là ceil(thời lượng ÷ hạn) − 1.''', '''The deadline at 90 Hz is 11 ms; missed vsyncs are ceil(duration ÷ deadline) − 1.''')
    B(C, S_, 1, 'sol', '''9 + 4 = 13 ms > 11 ms: trễ, ceil(13 ÷ 11) − 1 = 1 vsync bị lỡ. Dời 6 ms đi: 3 + 4 = 7 ms < 11 ms, kịp hạn.''', '''9 + 4 = 13 ms > 11 ms: late, ceil(13 ÷ 11) − 1 = 1 missed vsync. Moving 6 ms away: 3 + 4 = 7 ms < 11 ms, on time.''')

    S_ = 'recall'
    a(C + '.sec.%s.title' % S_, '''Tự trả lời''', '''Answer it yourself''')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'ask', '''Hạn mỗi khung ở 60, 90 và 120 Hz là bao nhiêu?''', '''What is the per-frame deadline at 60, 90 and 120 Hz?''')
    B(C, S_, 1, 'ans', '''16 ms, 11 ms và 8 ms.''', '''16 ms, 11 ms and 8 ms.''')
    B(C, S_, 2, 'ask', '''Trong trace, luồng main "đang chờ" thay vì "đang chạy" gợi ý điều gì?''', '''In a trace, what does the main thread "waiting" rather than "running" suggest?''')
    B(C, S_, 2, 'ans', '''Nó chờ I/O, khóa hay binder, không phải tính toán; cách sửa là dời việc chờ đó khỏi luồng main.''', '''It is waiting on I/O, a lock or binder, not computing; the fix is to move that wait off the main thread.''')

    for q, qv, qe, av, ae, wv, we in [
        ('q1', 'Khung quá hạn 1 ms thì sao?', 'What happens to a frame 1 ms past the deadline?', 'Bị bỏ cả khung.', 'The whole frame is dropped.',
         'Màn hình giữ hình cũ tới vsync sau.', 'The screen keeps the old image until a later vsync.'),
        ('q2', 'Khung đứng là khung dài hơn bao nhiêu?', 'A frozen frame is longer than what?', '700 ms.', '700 milliseconds.',
         'Khung chậm từ 16 tới 700 ms; quá 5 giây là ANR.', 'Slow frames are 16 to 700 ms; over 5 seconds is an ANR.'),
        ('q3', 'Vì sao nên bắt đầu bằng system trace thay vì method trace?', 'Why start with a system trace rather than a method trace?', 'Method trace tốn chi phí lớn nên cho giật giả và không phân biệt chạy với chờ.', 'A method trace\'s heavy overhead shows false jank and cannot tell running from waiting.',
         'Dùng method trace sau, khi đã khoanh vùng.', 'Use a method trace later, once narrowed down.')]:
        a(C + '.quiz.%s.q' % q, qv, qe); a(C + '.quiz.%s.a' % q, av, ae); a(C + '.quiz.%s.why' % q, wv, we)
