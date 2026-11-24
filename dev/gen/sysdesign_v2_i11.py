# Thiết kế hệ thống phía mobile · I11: khởi động, pin, kích thước (Phần 2)
# Nguồn: Android App startup time (cold, warm, hot; TTID, TTFD; reportFullyDrawn, ReportDrawnWhen; khởi tạo nặng), Startup analysis and
# optimization (Macrobenchmark, việc > 20 ms, đợi sau khung hình đầu, StrictMode, Baseline Profiles), App Startup 1.2.0, Reduce app size;
# pin dẫn lại I4 (ax-doze, ax-network-access) vì trang Power không tải được đúng nội dung. Đọc 2026-11-24.

SEC_ORDER = {'i11': ['hook', 'kinds', 'defer', 'measure', 'cost', 'bugs', 'ex', 'honest']}


def add(a):
    def B(ch, sec, n, field, vi, en=None):
        a('%s.sec.%s.b.%02d.%s' % (ch, sec, n, field), vi, vi if en is None else en)

    a('preset.startup', 'Thiết kế hệ thống · khởi động app phòng khám', 'System design · starting the clinic app')
    m = lambda k, vi, en=None: a('m.startup.' + k, vi, en)
    m('title', 'Khởi tạo mọi thứ lúc mở app, hay chỉ thứ cần ngay', 'Initialise everything at launch, or only what is needed now')
    m('overview', 'App phòng khám dùng năm SDK (báo crash, thống kê, quảng cáo, chat, thư viện ảnh) và một database cần migrate. Bản đầu khởi tạo tất cả trong Application.onCreate trên luồng chính. Bốn tình huống: cold start khởi tạo hết; cold start chỉ khởi tạo thứ cần ngay, còn lại để lười hay chạy nền; warm start; hot start. Mọi con số mili giây là minh họa.',
      'The clinic app uses five SDKs (crash reporting, analytics, ads, chat, an image library) and a database that needs migrating. The first version initialises everything in Application.onCreate on the main thread. Four situations: a cold start initialising everything; a cold start initialising only what is needed now, the rest lazily or in the background; a warm start; a hot start. All millisecond figures are illustrative.')
    m('wrapup', 'Người dùng chờ cho tới khung hình đầu (TTID), rồi tới khi nội dung thật hiện ra (TTFD). Ở cold start, mọi thứ trong Application.onCreate nằm trên đường đó: năm SDK và một lần migrate làm luồng chính bận 2,7 giây. Chỉ giữ thứ cần ngay (báo crash), dời việc khác ra sau khung hình đầu, sang luồng nền, hay tới lúc thật sự dùng; TTID giảm từ 3,5 giây còn 0,9 giây. Warm và hot start bỏ qua bước tạo process và Application, nhưng phải tối ưu theo cold start.',
      'Users wait until the first frame (TTID), then until real content shows (TTFD). On a cold start, everything in Application.onCreate sits on that path: five SDKs and a migration keep the main thread busy for 2.7 seconds. Keep only what is needed now (crash reporting) and move the rest after the first frame, to a background thread, or to first use; TTID drops from 3.5 to 0.9 seconds. Warm and hot starts skip process creation and Application, but you optimise for the cold start.')
    m('simp.1', 'Thời gian từng SDK, thời gian tạo process và dựng Activity là minh họa; trên máy thật, việc nền vẫn tranh CPU với luồng chính, nên nó không hoàn toàn miễn phí như trên hình.', 'The time for each SDK, process creation and Activity setup are illustrative; on real devices background work still competes with the main thread for CPU, so it is not fully free as drawn.')
    m('simp.2', 'Cold, warm, hot start, TTID, TTFD theo Android App startup time; việc dài hơn 20 ms và đợi sau khung hình đầu theo Startup analysis and optimization; Initializer theo App Startup 1.2.0. Đọc ngày 2026-11-24.', 'Cold, warm and hot starts, TTID and TTFD follow Android App startup time; operations over 20 ms and waiting until after the first frame follow Startup analysis and optimization; Initializer follows App Startup 1.2.0. Read on 2026-11-24.')
    m('ctl.hint', 'Đổi tình huống rồi đi lại; so vạch TTID và TTFD trên làn thời gian.', 'Switch the situation and walk again; compare the TTID and TTFD markers on the timeline.')
    m('ctl.case', 'Tình huống', 'Situation')
    for k, vi, en in [('heavy', 'cold start, khởi tạo hết', 'cold start, initialise everything'), ('lazy', 'cold start, chỉ thứ cần ngay', 'cold start, only what is needed now'), ('warm', 'warm start', 'warm start (process alive)'), ('hot', 'hot start', 'hot start (Activity alive)')]:
        m('ctl.case.' + k, vi, en)
    m('diagramTitle', 'Process, Application, Activity, khung hình đầu', 'Process, Application, Activity, first frame')
    m('diagramDesc', 'Các chặng của một lần mở app, từ tạo process tới khung hình đầu', 'The stages of a launch, from process creation to the first frame')
    for k, vi, en in [('proc', 'Tạo process', 'Process creation'), ('app', 'Application.onCreate', 'Application.onCreate()'), ('act', 'Activity, giao diện', 'Activity and UI'), ('frame', 'Khung hình đầu', 'First frame')]:
        m('n.' + k, vi, en)
    m('met.init', 'ms khởi tạo trên luồng chính', 'ms of init on the main thread'); m('met.ttid', 'TTID (ms)', 'TTID in ms'); m('met.ttfd', 'TTFD (ms)', 'TTFD in ms')
    a('cap.startup', 'Các chặng của một lần mở app, từ trái sang phải.', 'The stages of a launch, left to right.')
    S = [
        ('heavy', 's1', 'Cold start: hệ thống tạo process (300 ms)', 'Cold start: the system creates the process (300 ms)', 'Trong lúc đó người dùng thấy cửa sổ khởi động trống.', 'Meanwhile the user sees a blank starting window.'),
        ('heavy', 's2', 'Application.onCreate khởi tạo năm SDK và migrate database: 2730 ms', 'Application.onCreate initialises five SDKs and migrates the database: 2730 ms', 'Tất cả trên luồng chính, trước khi Activity được tạo.', 'All on the main thread, before the Activity is created.'),
        ('heavy', 's3', 'Activity dựng giao diện, khung hình đầu: TTID 3530 ms', 'The Activity builds its UI, first frame: TTID 3530 ms', 'Hơn 3,5 giây nhìn màn hình trống.', 'Over 3.5 seconds of a blank screen.'),
        ('heavy', 's4', 'Tải lịch hẹn, nội dung thật hiện: TTFD 3930 ms', 'Load bookings, real content shows: TTFD 3930 ms', 'Gần 4 giây; quảng cáo và chat chưa ai mở mà đã tốn 1,5 giây.', 'Nearly 4 seconds; ads and chat, which nobody opened yet, cost 1.5 seconds.'),
        ('lazy', 's1', 'Cold start: tạo process (300 ms)', 'Cold start: process creation (300 ms)', 'Phần này app không đổi được.', 'The app cannot change this part.'),
        ('lazy', 's2', 'Application.onCreate chỉ khởi tạo báo crash (80 ms); database mở ở luồng nền', 'Application.onCreate initialises only crash reporting (80 ms); the database opens in the background', 'Báo crash cần từ sớm để bắt được crash lúc khởi động. Những thứ khác chờ.', 'Crash reporting is needed early to catch startup crashes. Everything else waits.'),
        ('lazy', 's3', 'Activity dựng giao diện, khung hình đầu: TTID 880 ms', 'The Activity builds its UI, first frame: TTID 880 ms', 'Quảng cáo, chat chỉ khởi tạo khi người dùng mở màn cần chúng.', 'Ads and chat initialise only when the user opens a screen that needs them.'),
        ('lazy', 's4', 'Lịch hẹn hiện: TTFD 1280 ms, báo bằng ReportDrawnWhen', 'Bookings show: TTFD 1280 ms, reported with ReportDrawnWhen', 'Thống kê khởi tạo sau đó, ở nền. Nhanh hơn khoảng 3 lần mà không bỏ tính năng nào.', 'Analytics initialises after that, in the background. About 3 times faster without dropping any feature.'),
        ('warm', 's1', 'Warm start: process vẫn còn, không tạo lại', 'Warm start: the process is still alive, not recreated', 'Ví dụ người dùng bấm Back thoát app rồi mở lại ngay.', 'For example the user pressed Back to leave and reopened at once.'),
        ('warm', 's2', 'Application.onCreate không chạy lại', 'Application.onCreate does not run again', 'Mọi thứ đã khởi tạo vẫn còn trong bộ nhớ.', 'Everything initialised is still in memory.'),
        ('warm', 's3', 'Activity được tạo lại: TTID 500 ms', 'The Activity is recreated: TTID 500 ms', 'Chỉ trả giá phần dựng giao diện.', 'Only the UI building is paid for.'),
        ('warm', 's4', 'Lịch hẹn lấy từ database: TTFD 600 ms', 'Bookings come from the database: TTFD 600 ms', 'Nhanh, nhưng không phải lần mở nào cũng là warm.', 'Fast, but not every launch is warm.'),
        ('hot', 's1', 'Hot start: Activity vẫn còn trong bộ nhớ', 'Hot start: the Activity is still in memory', 'Ví dụ người dùng chuyển sang app khác vài giây rồi quay lại.', 'For example the user switched apps for a few seconds and came back.'),
        ('hot', 's2', 'Không tạo process, không chạy Application', 'No process creation, no Application run', 'Bỏ qua hai chặng đầu.', 'The first two stages are skipped.'),
        ('hot', 's3', 'Đưa Activity ra trước và vẽ: TTID 100 ms', 'Bring the Activity forward and draw: TTID 100 ms', 'Rẻ nhất trong ba kiểu.', 'The cheapest of the three.'),
        ('hot', 's4', 'Nội dung vẫn còn: TTFD 100 ms', 'Content is still there: TTFD 100 ms', 'Nếu hệ thống đã thu bộ nhớ (chương I2), lần sau có thể là warm hay cold.', 'If the system reclaimed memory (chapter I2), next time may be warm or cold.'),
    ]
    for case, k, tv, te, xv, xe in S:
        sid = case + '.' + k
        m('s.%s.title' % sid, tv, te); m('s.%s.explain' % sid, xv, xe); m('ev.' + sid, tv, te)
    for k, vi, en in [
        ('try', 'Đi hết bốn bước của mỗi tình huống; so vị trí vạch TTID và TTFD.', 'Walk all four steps of each situation; compare where the TTID and TTFD markers land.'),
        ('heavy.s2', 'Tài liệu Android nêu khởi tạo nặng trong lớp Application là vấn đề khởi động hay gặp nhất, ví dụ khởi tạo thư viện mà màn đầu không cần. [[src:ax-launch-time]]', 'The Android docs list heavy initialisation in the Application class as a common startup problem, such as initialising libraries the first screen does not need. [[src:ax-launch-time]]'),
        ('heavy.s3', 'TTID là thời gian tới khung hình đầu; hệ thống tự đo và ghi dòng Displayed trong Logcat. [[src:ax-launch-time]]', 'TTID is the time to the first frame; the system measures it and logs a Displayed line in Logcat. [[src:ax-launch-time]]'),
        ('heavy.s4', 'Tài liệu tối ưu khởi động khuyên xem mọi việc dài hơn 20 ms lúc khởi động và hỏi: có cần ngay không, có đợi sau khung hình đầu được không. [[src:ax-startup-analysis]]', 'The startup optimisation guide advises looking at every operation over 20 ms during startup and asking: is it needed now, can it wait until after the first frame? [[src:ax-startup-analysis]]'),
        ('lazy.s2', 'App Startup: các Initializer dùng chung một ContentProvider thay vì mỗi thư viện một cái, và bỏ meta-data đi thì khởi tạo lười bằng AppInitializer khi cần. [[src:ax-app-startup-lib]]', 'App Startup: Initializers share one ContentProvider instead of one per library, and removing the meta-data lets you initialise lazily with AppInitializer when needed. [[src:ax-app-startup-lib]]'),
        ('lazy.s3', 'Tài liệu cũng nhắc việc nền vẫn tranh CPU trong lúc khởi động; dời ra nền giúp luồng chính, nhưng không miễn phí. [[src:ax-startup-analysis]]', 'The guide also notes background work still competes for CPU during startup; moving it off the main thread helps, but is not free. [[src:ax-startup-analysis]]'),
        ('lazy.s4', 'TTFD hệ thống không tự biết; app báo bằng reportFullyDrawn(), hay ReportDrawnWhen trong Compose. [[src:ax-launch-time]]', 'The system cannot detect TTFD; the app reports it with reportFullyDrawn(), or ReportDrawnWhen in Compose. [[src:ax-launch-time]]'),
        ('warm.s2', 'Warm start dựng lại Activity nhưng có thể dùng lại process đã có. [[src:ax-launch-time]]', 'A warm start recreates the Activity but may reuse the existing process. [[src:ax-launch-time]]'),
        ('warm.s3', 'Tài liệu khuyên luôn tối ưu theo giả định cold start, vì cải thiện cold start cũng cải thiện warm và hot. [[src:ax-launch-time]]', 'The docs advise always optimising for a cold start, since that also improves warm and hot starts. [[src:ax-launch-time]]'),
        ('warm.s4', 'Dữ liệu đã có trong database (track Lưu dữ liệu) làm TTFD gần bằng TTID.', 'Data already in the database (Saving Data track) brings TTFD close to TTID.'),
        ('hot.s2', 'Hot start chỉ đưa Activity đang có ra trước; chi phí thấp nhất. [[src:ax-launch-time]]', 'A hot start only brings the existing Activity to the front; the lowest overhead. [[src:ax-launch-time]]'),
        ('hot.s3', 'Nếu bộ nhớ đã bị thu lại, hot start phải dựng lại một phần, gần với warm. [[src:ax-launch-time]]', 'If memory was trimmed, a hot start has to rebuild part of it, closer to warm. [[src:ax-launch-time]]'),
        ('hot.s4', 'Không thể chọn người dùng sẽ gặp kiểu nào; vì vậy cold start mới là con số cần giữ.', 'You cannot choose which kind users get; that is why the cold start is the number to protect.')]:
        m('co.' + k, vi, en)

    z = lambda k, vi, en=None: a('vz.' + k, vi, en)
    z('tab.st', 'Làn thời gian khởi động', 'Startup timeline')
    z('st.cap', 'Thanh trên là luồng chính, thanh dưới là luồng nền. Thanh viền cam nét đứt là việc của bước hiện tại; thanh tô đỏ là khởi tạo chặn luồng chính.', 'The upper lane is the main thread, the lower lane a background thread. Dashed orange bars belong to the current step; red-tinted bars are initialisation blocking the main thread.')
    z('st.lane.main', 'Luồng chính', 'Main thread'); z('st.lane.bg', 'Luồng nền', 'Background')
    z('st.m.ttid', 'TTID', 'TTID (first frame)'); z('st.m.ttfd', 'TTFD', 'TTFD (fully drawn)')
    for k, vi, en in [('proc', 'Tạo process', 'Create process'), ('crash', 'Báo crash', 'Crash reporting'), ('analytics', 'Thống kê', 'Analytics'), ('ads', 'Quảng cáo', 'Ads SDK'), ('chat', 'Chat', 'Chat SDK'),
                      ('img', 'Thư viện ảnh', 'Image library'), ('db', 'Mở, migrate DB', 'Open, migrate DB'), ('act', 'Activity, giao diện', 'Activity, UI'), ('load', 'Tải lịch hẹn', 'Load bookings'), ('resume', 'Đưa ra trước, vẽ', 'Resume, draw')]:
        z('st.k.' + k, vi, en)
    for k, vi, en in [('job', 'Việc', 'Work'), ('lane', 'Luồng', 'Thread'), ('ms', 'ms', 'Duration (ms)'), ('why', 'Vì sao ở đây', 'Why here')]:
        z('st.col.' + k, vi, en)
    W = [
        ('heavy', 'proc', 'hệ thống tạo process', 'the system creates the process'), ('heavy', 'crash', 'cần từ sớm', 'needed early'),
        ('heavy', 'analytics', 'ai đó thêm vào Application', 'someone added it to Application'), ('heavy', 'ads', 'thư viện hướng dẫn gọi ở đây', 'the library\'s guide said to call it here'),
        ('heavy', 'chat', 'cho tiện', 'for convenience'), ('heavy', 'img', 'cho tiện', 'convenient at the time'), ('heavy', 'db', 'migrate đồng bộ', 'synchronous migration'),
        ('heavy', 'act', 'màn đầu', 'the first screen'), ('heavy', 'load', 'sau khung hình đầu', 'after the first frame'),
        ('lazy', 'proc', 'hệ thống tạo process', 'the system creates the process'), ('lazy', 'crash', 'cần từ sớm', 'needed early'),
        ('lazy', 'db', 'luồng nền, song song với giao diện', 'background, in parallel with the UI'), ('lazy', 'act', 'màn đầu', 'the first screen'),
        ('lazy', 'analytics', 'sau khi nội dung đã hiện, ở nền', 'after content shows, in the background'), ('lazy', 'load', 'khi database sẵn sàng', 'once the database is ready'),
        ('warm', 'act', 'Activity được tạo lại', 'the Activity is recreated'), ('warm', 'load', 'đọc từ database', 'read from the database'),
        ('hot', 'resume', 'Activity vẫn còn', 'the Activity is still alive')]
    for c, k, vi, en in W:
        z('st.w.%s.%s' % (c, k), vi, en)
    z('st.legend', 'Tô đỏ trên làn, gạch đỏ trong bảng: khởi tạo chặn luồng chính. Vạch đỏ TTID: khung hình đầu; vạch TTFD: nội dung thật đã hiện. Trục ngang tính bằng giây.', 'Red tint on the lanes, red hatching in the table: initialisation blocking the main thread. TTID marker: the first frame; TTFD marker: real content shown. The horizontal axis is in seconds.')

    C = 'i11'
    a(C + '.title', 'Khởi động, pin và kích thước app', 'Startup, battery and app size')
    a(C + '.essence', 'Người dùng chờ tới khung hình đầu (TTID) rồi tới nội dung thật (TTFD). Cold start gồm tạo process, Application.onCreate, Activity; mọi thứ khởi tạo trong Application nằm trên đường chờ đó.\nChỉ giữ thứ cần ngay; dời việc khác ra sau khung hình đầu, sang luồng nền, hay tới lúc thật sự dùng (App Startup, khởi tạo lười). Đo bằng Macrobenchmark và trace, xem mọi việc dài hơn 20 ms.\nPin và kích thước là chi phí âm thầm: gom việc mạng, tôn trọng Doze (chương I4); thu nhỏ bằng R8, bỏ tài nguyên thừa, phát hành bằng App Bundle.',
      'Users wait until the first frame (TTID), then until real content (TTFD). A cold start includes process creation, Application.onCreate and the Activity; anything initialised in Application sits on that waiting path.\nKeep only what is needed now; move the rest after the first frame, to a background thread, or to first use (App Startup, lazy initialisation). Measure with Macrobenchmark and traces, looking at every operation over 20 ms.\nBattery and size are silent costs: batch network work and respect Doze (chapter I4); shrink with R8, strip unused resources, ship an App Bundle.')
    a(C + '.goal.g1', 'Đã thấy khung hình đầu (TTID)', 'Saw the first frame (TTID)')
    a(C + '.goal.g2', 'Đã thấy nội dung thật hiện ra (TTFD)', 'Saw real content appear (TTFD)')
    a(C + '.sim.sysdesign.startup', 'cold khởi tạo hết, cold khởi tạo lười, warm, hot', 'cold with everything, cold with lazy init, warm, hot')

    S_ = 'hook'
    a(C + '.sec.%s.title' % S_, 'Đoán trước khi đọc', 'Predict before reading')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'predict', 'App mất 4 giây mới hiện màn đầu khi mở lần đầu trong ngày, nhưng chỉ nửa giây khi mở lại sau vài phút. Bạn đoán thời gian bị tiêu ở đâu, và vì sao hai lần mở khác nhau đến vậy?',
      'The app takes 4 seconds to show its first screen on the first launch of the day, but half a second when reopened a few minutes later. Where do you think the time goes, and why do the two launches differ so much?')
    B(C, S_, 1, 'ans', 'Lần đầu trong ngày là cold start: phải tạo process và chạy Application.onCreate, nơi app khởi tạo mọi SDK trên luồng chính. Lần sau là warm hay hot start: process (thậm chí Activity) vẫn còn, nên bỏ qua đúng phần nặng đó. Sửa ở cold start: chỉ khởi tạo thứ cần ngay. [[src:ax-launch-time]]',
      'The first launch of the day is a cold start: the process is created and Application.onCreate runs, where the app initialises every SDK on the main thread. The later one is a warm or hot start: the process (even the Activity) is still alive, skipping exactly that heavy part. Fix the cold start: initialise only what is needed now. [[src:ax-launch-time]]')

    S_ = 'kinds'
    a(C + '.sec.%s.title' % S_, 'Cold, warm, hot; TTID và TTFD', 'Cold, warm, hot; TTID and TTFD')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'p', 'Tài liệu Android chia ba kiểu. Cold start: app bắt đầu từ đầu; hệ thống hiện cửa sổ khởi động trống, tạo process, rồi app tạo đối tượng Application, Activity, dựng giao diện và vẽ khung hình đầu. Warm start: process có thể còn, nhưng Activity phải tạo lại. Hot start: Activity còn trong bộ nhớ, chỉ cần đưa ra trước. Tài liệu khuyên luôn tối ưu theo giả định cold start. [[src:ax-launch-time]]',
      'The Android docs name three kinds. Cold start: the app starts from scratch; the system shows a blank starting window and creates the process, then the app creates the Application object and the Activity, builds the UI and draws the first frame. Warm start: the process may survive but the Activity must be recreated. Hot start: the Activity is in memory and just comes to the front. The docs advise always optimising assuming a cold start. [[src:ax-launch-time]]')
    B(C, S_, 2, 'p', 'Hai con số: TTID (time to initial display) là tới khung hình đầu, hệ thống tự đo và ghi dòng Displayed trong Logcat. TTFD (time to full display) là tới khi dùng được thật, kể cả nội dung tải sau khung hình đầu; hệ thống không tự biết, nên app gọi reportFullyDrawn(), hay dùng ReportDrawnWhen, ReportDrawnAfter trong Compose. Không báo thì không có TTFD. [[src:ax-launch-time]]',
      'Two numbers: TTID (time to initial display) is to the first frame, measured by the system and logged as a Displayed line in Logcat. TTFD (time to full display) is to truly usable, including content loaded after the first frame; the system cannot know it, so the app calls reportFullyDrawn(), or uses ReportDrawnWhen or ReportDrawnAfter in Compose. Without a report there is no TTFD. [[src:ax-launch-time]]')

    S_ = 'defer'
    a(C + '.sec.%s.title' % S_, 'Thứ gì thật sự cần lúc khởi động', 'What is really needed at startup')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'p', 'Với mỗi việc lúc khởi động, tài liệu gợi ý hỏi: có cần ngay không, hay đợi tới sau khung hình đầu được? Có chạy ở luồng nền được không? Thường thì báo crash cần từ sớm; thống kê đợi được tới sau khung hình đầu; quảng cáo, chat chỉ cần khi người dùng mở màn của chúng; database mở ở luồng nền. Việc nền vẫn tranh CPU, nên dời ra nền là giúp, chứ không miễn phí. [[src:ax-startup-analysis]]',
      'For each startup task, the guide suggests asking: is it needed now, or can it wait until after the first frame? Can it run on a background thread? Typically crash reporting is needed early; analytics can wait until after the first frame; ads and chat are needed only when their screens open; the database opens off the main thread. Background work still competes for CPU, so moving it helps but is not free. [[src:ax-startup-analysis]]')
    B(C, S_, 2, 'p', 'Nhiều thư viện tự khởi tạo qua một ContentProvider riêng, chạy trước cả Application.onCreate. Thư viện App Startup gom chúng về một ContentProvider chung, cho phép định thứ tự bằng dependencies(), và cho tắt khởi tạo tự động để gọi AppInitializer khi thật sự cần. Tài liệu gọi ContentProvider là thứ tốn khi khởi tạo, chạy theo thứ tự không xác định. [[src:ax-app-startup-lib]]',
      'Many libraries initialise through their own ContentProvider, which runs even before Application.onCreate. The App Startup library gathers them into one shared ContentProvider, lets you order them with dependencies(), and lets you disable automatic initialisation to call AppInitializer when really needed. The docs call ContentProviders expensive to instantiate, running in an undetermined order. [[src:ax-app-startup-lib]]')
    B(C, S_, 3, 'note', 'Cẩn thận với "khởi tạo lười" làm chậm lần dùng đầu: nếu màn chat mất 600 ms để mở lần đầu, có thể khởi tạo trước ở nền ngay sau khung hình đầu. Đây là đánh đổi của site, không phải quy tắc.', 'Beware lazy initialisation slowing the first use: if the chat screen takes 600 ms to open the first time, pre-initialise it in the background right after the first frame. This is the site\'s trade-off, not a rule.')
    B(C, S_, 3, 'kind', 'pitfall')

    S_ = 'measure'
    a(C + '.sec.%s.title' % S_, 'Đo trước khi sửa', 'Measure before fixing')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'p', 'Tài liệu tối ưu khởi động: đo bằng Macrobenchmark (StartupTimingMetric) và xem system trace trong Perfetto hay Android Studio; nhìn mọi việc dài hơn 20 ms trong lúc khởi động. Bật StrictMode.ThreadPolicy ở bản debug để bắt I/O trên luồng chính, như lần migrate database ở trên. Thêm startup profile (Baseline Profiles) để mã khởi động được biên dịch sẵn. [[src:ax-startup-analysis]] [[src:cp-baseline]]',
      'The startup guide: measure with Macrobenchmark (StartupTimingMetric) and read system traces in Perfetto or Android Studio; look at every operation over 20 ms during startup. Enable StrictMode.ThreadPolicy in debug builds to catch main-thread I/O, like the database migration above. Add a startup profile (Baseline Profiles) so startup code is compiled ahead of time. [[src:ax-startup-analysis]] [[src:cp-baseline]]')
    B(C, S_, 2, 'note', 'Đo trên bản release, máy thật, và cold start; bản debug chậm hơn nhiều và cho con số sai lệch. Đây là nhắc nhở của site, cùng tinh thần với chương đo hiệu năng ở track Compose Runtime.', 'Measure release builds on real devices, from a cold start; debug builds are much slower and mislead. This is the site\'s reminder, in the spirit of the performance chapter in the Compose Runtime track.')
    B(C, S_, 2, 'kind', 'android')

    S_ = 'cost'
    a(C + '.sec.%s.title' % S_, 'Pin và kích thước: chi phí âm thầm', 'Battery and size: silent costs')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'p', 'Pin: phần lớn đã gặp ở chương I4. Mỗi lần mạng thức giữ radio bật thêm một lúc, nên gom việc mạng lại thay vì gửi lắt nhắt; Doze hoãn mạng và việc nền của app, nên đừng giữ kết nối riêng mà dựa vào dịch vụ đẩy và WorkManager với điều kiện (sạc, Wi-Fi) cho việc không gấp. [[src:ax-network-access]] [[src:ax-doze]]',
      'Battery: most of it appeared in chapter I4. Every network wake-up keeps the radio on for a while, so batch network work instead of trickling it; Doze defers the app\'s network and background work, so do not hold your own connection but rely on push and on WorkManager with constraints (charging, Wi-Fi) for non-urgent work. [[src:ax-network-access]] [[src:ax-doze]]')
    B(C, S_, 2, 'p', 'Kích thước: tài liệu Android nói người dùng tránh tải app lớn, nhất là trên mạng chậm hay gói dữ liệu ít, và kích thước còn ảnh hưởng thời gian tải, bộ nhớ, pin. Cách chính: phát hành App Bundle để Google Play tạo APK theo từng máy; bật minifyEnabled và shrinkResources để R8 bỏ mã thừa rồi bỏ tài nguyên thừa; giới hạn ngôn ngữ và mật độ ảnh; dùng vector cho hình nhỏ, WebP cho ảnh. [[src:ax-reduce-size]]',
      'Size: the Android docs say users avoid large downloads, especially on slow networks or small data plans, and size also affects load time, memory and battery. The main levers: ship an App Bundle so Google Play builds per-device APKs; enable minifyEnabled and shrinkResources so R8 removes unused code and then unused resources; limit locales and image densities; use vectors for small graphics and WebP for photos. [[src:ax-reduce-size]]')

    S_ = 'bugs'
    a(C + '.sec.%s.title' % S_, 'Hai lỗi hay gặp', 'Two common bugs')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'bug', 'Sau khi thêm một SDK quảng cáo, thời gian mở app tăng gần một giây, dù màn đầu không có quảng cáo.', 'After adding an ads SDK, launch time grows by almost a second, though the first screen has no ads.')
    B(C, S_, 1, 'cause', 'Hướng dẫn của SDK bảo khởi tạo trong Application.onCreate; SDK còn tự đăng ký một ContentProvider chạy trước cả onCreate.', 'The SDK\'s guide said to initialise in Application.onCreate; the SDK also registered its own ContentProvider that runs before onCreate.')
    B(C, S_, 1, 'fix', 'Tắt khởi tạo tự động (bỏ provider hay meta-data trong manifest), khởi tạo qua App Startup khi màn có quảng cáo mở lần đầu, và đo lại bằng Macrobenchmark. [[src:ax-app-startup-lib]]', 'Disable automatic initialisation (remove the provider or meta-data in the manifest), initialise through App Startup when the first ad screen opens, and measure again with Macrobenchmark. [[src:ax-app-startup-lib]]')
    B(C, S_, 2, 'bug', 'Báo cáo khởi động trên Play Console đẹp, nhưng người dùng vẫn chờ lâu mới thấy lịch hẹn.', 'Startup reports look good, yet users still wait long before seeing their bookings.')
    B(C, S_, 2, 'cause', 'App chỉ được đo TTID: khung hình đầu là một màn khung xương hiện rất nhanh; nội dung thật tới sau mà không ai báo TTFD.', 'Only TTID was measured: the first frame is a skeleton that appears fast; the real content comes later and nobody reports TTFD.')
    B(C, S_, 2, 'fix', 'Báo TTFD bằng reportFullyDrawn hay ReportDrawnWhen { lịch hẹn đã tải }, rồi tối ưu cả con số đó. [[src:ax-launch-time]]', 'Report TTFD with reportFullyDrawn or ReportDrawnWhen { bookings loaded }, then optimise that number too. [[src:ax-launch-time]]')

    S_ = 'ex'
    a(C + '.sec.%s.title' % S_, 'Bài tập', 'Exercise')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'ex', 'Application.onCreate của app đang làm: (1) báo crash 60 ms; (2) đọc cấu hình từ xa 400 ms qua mạng; (3) khởi tạo bản đồ 500 ms (chỉ màn "Tìm phòng khám" dùng); (4) đọc token đăng nhập từ DataStore 30 ms (màn đầu cần biết đã đăng nhập chưa); (5) thống kê 250 ms. Xếp mỗi việc vào: ngay trong onCreate, ở nền ngay sau khung hình đầu, hay khi lần đầu cần. Tính phần còn lại trên luồng chính.',
      'The app\'s Application.onCreate does: (1) crash reporting 60 ms; (2) remote config 400 ms over the network; (3) map initialisation 500 ms (only the "Find a clinic" screen uses it); (4) reading the login token from DataStore 30 ms (the first screen must know whether the user is logged in); (5) analytics 250 ms. Place each in: right in onCreate, in the background right after the first frame, or on first use. Compute what stays on the main thread.')
    B(C, S_, 1, 'hint', 'Màn đầu cần gì để vẽ đúng? Việc nào chờ mạng?', 'What does the first screen need to draw correctly? Which task waits on the network?')
    B(C, S_, 1, 'sol', '(1) ngay trong onCreate, để bắt crash lúc khởi động. (4) cần cho màn đầu, nhưng đọc ở luồng nền và hiện khung xương trong lúc chờ; không chặn luồng chính. (2) ở nền sau khung hình đầu, dùng giá trị mặc định hay bản lưu lần trước; đừng bắt màn đầu chờ mạng. (5) ở nền sau khung hình đầu. (3) khi lần đầu mở "Tìm phòng khám", có thể khởi tạo trước ở nền nếu đo thấy lần mở đó chậm. Còn lại trên luồng chính: 60 ms thay vì 1.240 ms.',
      '(1) right in onCreate, to catch startup crashes. (4) needed by the first screen, but read off the main thread while a skeleton shows; do not block the main thread. (2) in the background after the first frame, using defaults or last saved values; never make the first screen wait on the network. (5) in the background after the first frame. (3) on first opening "Find a clinic", optionally pre-initialised in the background if that first open measures slow. Left on the main thread: 60 ms instead of 1,240 ms.')

    S_ = 'honest'
    a(C + '.sec.%s.title' % S_, 'Chương này giản lược những gì', 'What this chapter simplifies')
    a(C + '.sec.%s.badge' % S_, 'simplified')
    B(C, S_, 1, 'p', 'Cold, warm, hot start, TTID, TTFD, reportFullyDrawn và ReportDrawnWhen theo Android App startup time; ngưỡng 20 ms, Macrobenchmark, StrictMode, Baseline Profiles theo Startup analysis and optimization; Initializer, ContentProvider chung, khởi tạo lười theo App Startup 1.2.0; kích thước theo Reduce your app size; pin dẫn lại chương I4 vì trang tổng quan về pin không đọc được đúng nội dung; đọc ngày 2026-11-24, diễn đạt lại. Mọi con số mili giây, năm SDK và bài tập là của site. Chương không nêu ngưỡng Android vitals cho thời gian khởi động vì chưa đọc được nguồn của con số đó, và không bàn splash screen API.',
      'Cold, warm and hot starts, TTID, TTFD, reportFullyDrawn and ReportDrawnWhen follow Android App startup time; the 20 ms threshold, Macrobenchmark, StrictMode and Baseline Profiles follow Startup analysis and optimization; Initializer, the shared ContentProvider and lazy initialisation follow App Startup 1.2.0; size follows Reduce your app size; battery points back to chapter I4 because the battery overview page could not be read correctly; read on 2026-11-24, paraphrased. All millisecond figures, the five SDKs and the exercise are the site\'s. The chapter gives no Android vitals startup thresholds because their source was not read, and does not cover the splash screen API.')

    for q, qv, qe, av, ae, wv, we in [
        ('q1', 'Cold start khác warm start ở chỗ nào?', 'How does a cold start differ from a warm start?', 'Cold start tạo process và chạy Application.onCreate; warm start dùng lại process, chỉ tạo lại Activity.', 'A cold start creates the process and runs Application.onCreate; a warm start reuses the process and only recreates the Activity.', 'Vì vậy khởi tạo trong Application chỉ làm chậm cold start, mà đó là kiểu cần tối ưu.', 'So initialisation in Application slows only cold starts, which are the ones to optimise.'),
        ('q2', 'TTID và TTFD khác nhau thế nào? Ai đo TTFD?', 'How do TTID and TTFD differ? Who measures TTFD?', 'TTID là tới khung hình đầu, hệ thống tự đo; TTFD là tới khi nội dung thật hiện, app phải tự báo.', 'TTID is to the first frame, measured by the system; TTFD is to real content, which the app must report.', 'Dùng reportFullyDrawn hay ReportDrawnWhen.', 'Use reportFullyDrawn or ReportDrawnWhen.'),
        ('q3', 'Dời việc khởi tạo sang luồng nền có làm nó miễn phí không?', 'Does moving initialisation to a background thread make it free?', 'Không. Luồng chính được giải phóng, nhưng việc nền vẫn tranh CPU trong lúc khởi động.', 'No. The main thread is freed, but background work still competes for CPU during startup.', 'Tốt nhất là không làm việc chưa cần.', 'Best is not doing work that is not yet needed.'),
        ('q4', 'Hai cài đặt Gradle nào giúp thu nhỏ app?', 'Which two Gradle settings help shrink the app?', 'minifyEnabled (R8 bỏ mã thừa) và shrinkResources (bỏ tài nguyên thừa).', 'minifyEnabled (R8 removes unused code) and shrinkResources (removes unused resources).', 'Thêm App Bundle để Play tạo APK theo máy.', 'Plus an App Bundle so Play builds per-device APKs.')]:
        a(C + '.quiz.%s.q' % q, qv, qe); a(C + '.quiz.%s.a' % q, av, ae); a(C + '.quiz.%s.why' % q, wv, we)
