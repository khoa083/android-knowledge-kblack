# Gỡ lỗi và hiệu năng · l0: bản đồ track (viết cuối, đặt đầu track; cùng khuôn với fp_v2_p0.py)
# Tổng hợp từ l1–l12; mỗi triệu chứng là đúng tình huống mô phỏng của chương được trỏ tới, cùng con số (nguồn ở chương đó).

SEC_ORDER = {'l0': ['hook', 'order', 'index', 'links', 'recall']}

TITLES = [
    ('l1', 'Quy trình gỡ lỗi, adb và bug report', 'The debugging process, adb and bug reports'),
    ('l2', 'Debugger: breakpoint, watch, evaluate', 'The debugger: breakpoints, watches, evaluate'),
    ('l3', 'Logcat', 'Logcat'),
    ('l4', 'Đọc stack trace', 'Reading stack traces'),
    ('l5', 'R8 và stack trace bị làm rối', 'R8 and obfuscated stack traces'),
    ('l6', 'Layout Inspector: xem cây giao diện', 'Layout Inspector: looking at the UI tree'),
    ('l7', 'Dữ liệu và việc nền: Database Inspector, Background Task Inspector', 'Data and background work: Database Inspector, Background Task Inspector'),
    ('l8', 'Bộ nhớ: churn, rò rỉ, heap dump', 'Memory: churn, leaks, heap dumps'),
    ('l9', 'CPU, trace và khung hình giật', 'CPU, traces and janky frames'),
    ('l10', 'ANR và StrictMode', 'ANRs and StrictMode'),
    ('l11', 'Mạng và pin', 'Network and battery'),
    ('l12', 'Đo hiệu năng cho đúng', 'Measuring performance properly'),
]

# [id, triệu chứng vi, en, chi tiết vi, en, công cụ vi, en, công cụ trả lời gì vi, en, cách chữa vi, en, chương, lộ ra ở: dev | user]
SY = [
    ('crashAgain', 'Crash "thỉnh thoảng", sửa ba lần vẫn quay lại', 'A crash "now and then" that returns after three fixes',
     'Khóa màn hình dọc còn 3 trên 8 kịch bản crash; thêm phép kiểm thì thành màn trống.', 'Locking portrait leaves 3 of 8 scenarios crashing; adding a check turns them into blank screens.',
     'Danh sách kịch bản, adb, bug report', 'A scenario list, adb, bug reports', 'Khi nào lỗi xảy ra, khi nào không: cả 4 kịch bản crash đều làm màn hình bị tạo lại.', 'When the bug happens and when it does not: all 4 crashing scenarios recreate the screen.',
     'Tái hiện, thu hẹp, đặt giả thuyết, kiểm; sửa một chỗ và khóa bằng test.', 'Reproduce, narrow down, hypothesise, test; fix one place and lock it with a test.', 'l1', 'user'),
    ('loop347', 'Lỗi ở một đơn trong 500; thêm Log rồi build lại mãi', 'A bug in one booking of 500; adding Logs and rebuilding again and again',
     'Breakpoint thường dừng 348 lần trước khi tới đơn lỗi.', 'A plain breakpoint stops 348 times before reaching the bad booking.',
     'Breakpoint có điều kiện, breakpoint chỉ ghi log', 'Conditional and logging breakpoints', 'Dừng đúng một lần khi fee < 0, hay ghi log mà không sửa mã.', 'Stop exactly once when fee < 0, or log without touching the code.',
     'Đặt điều kiện theo triệu chứng; chọn chính sách dừng Thread khi có luồng phụ thuộc thời gian.', 'Put the condition on the symptom; choose the Thread suspend policy when other threads depend on time.', 'l2', 'dev'),
    ('logNoise', 'Không tìm thấy dòng lỗi giữa log của cả máy', 'The error line is lost among the whole device\'s logs',
     '16 dòng của mọi tiến trình; lọc theo app và mức còn 2 dòng.', '16 lines from every process; filtering by app and level leaves 2.',
     'Truy vấn Logcat', 'Logcat queries', 'Cùng key thì OR, khác key thì AND, level: là mức đó trở lên.', 'The same key ORs, different keys AND, level: means that level or higher.',
     'package:mine level:WARN, rồi tag: để xem ngữ cảnh.', 'package:mine level:WARN, then tag: for context.', 'l3', 'dev'),
    ('phoneInLog', 'Log của bản release in số điện thoại', 'Release-build logs print phone numbers',
     'R8 xóa Log.d, nhưng Log.w vẫn in số điện thoại.', 'R8 removes Log.d, but Log.w still prints the phone number.',
     'Quy tắc R8 cho Log, đọc lại nội dung log', 'An R8 rule for Log, reviewing log content', 'Dòng nào còn trong bản release, dòng nào lộ dữ liệu.', 'Which lines remain in release, which leak data.',
     'Không log dữ liệu cá nhân; chỉ log id và hằng số.', 'Do not log personal data; log ids and constants only.', 'l3', 'user'),
    ('firstLine', 'Sửa theo dòng đầu stack trace mà crash vẫn còn', 'Fixing by the stack trace\'s first line, and the crash remains',
     'Dòng đầu là RuntimeException của Android, 0 dòng của app.', 'The first line is Android\'s RuntimeException, with 0 lines of the app.',
     'Chuỗi Caused by, "... N more"', 'The Caused by chain, "... N more"', 'Nguyên nhân gốc ở Caused by cuối và frame đầu của app trong đó.', 'The root cause in the last Caused by and the first app frame in it.',
     'Sửa ở BookingMapper.kt:22, nơi ngày 2026-11-31 đi vào app.', 'Fix at BookingMapper.kt:22, where the date 2026-11-31 enters the app.', 'l4', 'dev'),
    ('abc', 'Play Console báo crash toàn tên a.b.c', 'Play Console reports a crash full of a.b.c names',
     'Tra bằng mapping của bản mới nhất cho 2 frame sai mà trông hợp lý.', 'Looking up with the latest build\'s mapping gives 2 wrong but plausible frames.',
     'File mapping đúng phiên bản, retrace', 'The exact version\'s mapping file, retrace', 'Tên lớp, hàm và số dòng thật của bản bị crash.', 'The real class, function and line numbers of the crashing build.',
     'Giữ mapping cho mỗi bản phát hành, hay phát hành bằng App Bundle.', 'Keep a mapping per release, or ship App Bundles.', 'l5', 'user'),
    ('releaseOnly', 'ClassNotFoundException chỉ có ở bản release', 'A ClassNotFoundException only in release',
     'Class.forName tìm một lớp mà R8 đã đổi tên.', 'Class.forName looks for a class R8 renamed.',
     'Keep rule, -whyareyoukeeping', 'Keep rules, -whyareyoukeeping', 'Thứ gì được tìm bằng tên qua reflection.', 'What is looked up by name through reflection.',
     'Keep rule hẹp, hay bỏ reflection.', 'A narrow keep rule, or drop reflection.', 'l5', 'user'),
    ('deadButton', 'Bấm nút không có gì xảy ra', 'Tapping a button does nothing',
     'Log trong onClick không bao giờ in.', 'The log in onClick never prints.',
     'Layout Inspector: cây giao diện', 'Layout Inspector: the UI tree', 'Những thành phần nào chồng nhau ở điểm chạm, cái nào nằm trên.', 'Which components overlap at the tap point, which is on top.',
     'Gỡ lớp phủ trong suốt khỏi cây khi không cần.', 'Remove the transparent overlay from the tree when not needed.', 'l6', 'dev'),
    ('savedEmpty', 'Lịch "đã lưu" mà danh sách trống', 'A booking "saved" but the list is empty',
     'Dòng 42 có trong bảng nhưng mang status PENDING.', 'Row 42 is in the table but has status PENDING.',
     'Database Inspector: bảng dữ liệu', 'Database Inspector: the tables', 'Dữ liệu thật trong bảng và kết quả đúng truy vấn của màn.', 'The real table data and the screen\'s exact query result.',
     'Sửa thử một dòng để kiểm giả thuyết, rồi sửa truy vấn.', 'Edit a row to test the hypothesis, then fix the query.', 'l7', 'dev'),
    ('syncStuck', '"Đang đồng bộ" hiện mãi', '"Syncing" never goes away',
     'Một worker ENQUEUED chờ Wi-Fi, hai worker sau BLOCKED.', 'One worker ENQUEUED waiting for Wi-Fi, two behind it BLOCKED.',
     'Background Task Inspector: các worker', 'Background Task Inspector: the workers', 'Trạng thái, ràng buộc và vị trí trong chuỗi của từng worker.', 'Each worker\'s state, constraints and chain position.',
     'Tách việc cần Wi-Fi khỏi chuỗi đồng bộ.', 'Take the Wi-Fi-only work out of the sync chain.', 'l7', 'user'),
    ('oom', 'App chậm dần rồi OutOfMemoryError', 'The app slows down, then an OutOfMemoryError',
     'Mỗi lần mở để lại 2,4 MB; lần thứ 20 vượt 64 MB.', 'Each open leaves 2.4 MB; the 20th crosses 64 MB.',
     'Heap dump, LeakCanary', 'Heap dumps, LeakCanary', 'Bao nhiêu instance, giữ bao nhiêu bộ nhớ, đường nào từ GC root đang giữ.', 'How many instances, how much they retain, which path from a GC root holds them.',
     'Cắt mắt xích: hủy đăng ký listener trong onDestroy.', 'Cut the link: unregister the listener in onDestroy.', 'l8', 'user'),
    ('jank', 'Cuộn danh sách bị giật', 'Scrolling the list stutters',
     'Hai khung 34,5 ms ở hạn 16 ms.', 'Two 34.5 ms frames against a 16 ms deadline.',
     'System trace, Perfetto', 'System traces, Perfetto', 'Khung nào trễ, luồng main đang làm gì trong khung đó.', 'Which frames are late, what the main thread is doing in them.',
     'Dời việc parse khỏi luồng main.', 'Move the parsing off the main thread.', 'l9', 'user'),
    ('anr', 'ANR khi bấm Lưu, máy dev không tái hiện được', 'An ANR on Save that the dev device cannot reproduce',
     'Luồng main chờ 8 giây cho một khóa.', 'The main thread waits 8 seconds for a lock.',
     'Trace ANR, StrictMode', 'ANR traces, StrictMode', 'Luồng main chờ gì và luồng nào đang giữ nó.', 'What the main thread waits for and which thread holds it.',
     'Gọi mạng ngoài khóa; bật StrictMode trong bản debug.', 'Call the network outside the lock; enable StrictMode in debug builds.', 'l10', 'user'),
    ('battery', 'Hao pin và tốn dữ liệu', 'Battery drain and heavy data use',
     'Ba request trùng mỗi lần mở màn, mỗi cái 1,2 MB.', 'Three duplicate requests per screen open, 1.2 MB each.',
     'Network Inspector: các request', 'Network Inspector: the requests', 'Request nào, khi nào, to bao nhiêu, ai gọi.', 'Which requests, when, how big, who calls them.',
     'Một nguồn dữ liệu chung, chỉ tải trang đầu.', 'One shared data source, first page only.', 'l11', 'user'),
    ('fake41', '"Nhanh hơn 41%" sau một lần đo', '"41% faster" after one measurement',
     'So lần chạy đầu sau khi cài với lần nhanh nhất.', 'Comparing the first run after install with the fastest run.',
     'Macrobenchmark', 'Macrobenchmark', 'Trung vị và độ dao động của nhiều lần đo cùng điều kiện.', 'The median and spread of many runs under the same conditions.',
     'Lặp 10 lần mỗi bên, so trung vị: khoảng 5 %.', '10 runs per side, compare medians: about 5%.', 'l12', 'dev'),
]


def add(a):
    def B(ch, sec, n, field, vi, en=None):
        a('%s.sec.%s.b.%02d.%s' % (ch, sec, n, field), vi, vi if en is None else en)

    m = lambda k, vi, en=None: a('m.map.' + k, vi, en)
    m('title', '''Gặp triệu chứng này thì mở công cụ nào, đọc chương nào''', '''Seen this symptom? Which tool to open, which chapter to read''')
    m('overview', '''Chọn một triệu chứng hay gặp trên app Hẹn Khám. Bốn bước: triệu chứng, nó lộ ra ở đâu (khi phát triển hay trên máy người dùng), công cụ trả lời câu hỏi nào, và chương giải thích.''',
      '''Pick a common symptom on the ClinicBook app. Four steps: the symptom, where it shows up (during development or on users\' phones), which question the tool answers, and the chapter that explains it.''')
    m('wrapup', '''Mỗi công cụ trả lời một câu hỏi: lỗi xảy ra khi nào (adb, bug report), giá trị lúc đó là gì (debugger), chuyện gì đã xảy ra (Logcat, stack trace), cái gì đang che, đang lưu, đang chờ (các inspector), ai giữ bộ nhớ (heap dump), luồng nào bận (trace), có thật nhanh hơn không (đo lặp lại). Chọn công cụ theo câu hỏi, không theo thói quen.''',
      '''Each tool answers one question: when does the bug happen (adb, bug reports), what is the value at that moment (the debugger), what happened (Logcat, stack traces), what is covering, stored or waiting (the inspectors), who holds the memory (heap dumps), which thread is busy (traces), is it really faster (repeated measurement). Pick the tool by the question, not by habit.''')
    m('simp.1', '''Mỗi triệu chứng chỉ trỏ tới một chương chính; lỗi thật thường cần vài công cụ cùng lúc.''', '''Each symptom points to one main chapter; real bugs often need several tools at once.''')
    m('ctl.hint', '''Chọn triệu chứng rồi đi bốn bước; tab "Bảng tra" liệt kê tất cả.''', '''Pick a symptom and walk the four steps; the "Lookup table" tab lists them all.''')
    m('ctl.symptom', '''Triệu chứng''', '''Symptom''')
    m('diagramTitle', '''Triệu chứng, nơi lộ ra, công cụ, chương''', '''Symptom, where it shows, tool, chapter''')
    m('diagramDesc', '''Từ điều bạn thấy tới công cụ và chương cần đọc''', '''From what you see to the tool and the chapter to read''')
    for k, vi, en in [('symptom', 'Triệu chứng', 'Symptom'), ('phase', 'Lộ ra ở', 'Shows up'), ('cause', 'Công cụ', 'Tool'), ('chapter', 'Chương', 'Chapter')]:
        m('n.' + k, vi, en)
    m('met.phase', '''Lộ ra ở''', '''Shows up'''); m('met.chapter', '''Chương''', '''Chapter''')
    m('phase.none', '''chưa xét''', '''not yet'''); m('ch.none', '''chưa xét''', '''not yet''')
    for k, vi, en, xv, xe in [
        ('dev', 'khi phát triển', 'during development', 'Lộ ra trên máy dev: bạn tự thấy, và có thể gắn debugger, xem log, mở inspector ngay lúc đó.', 'Shows up on the dev device: you see it yourself and can attach the debugger, read logs or open an inspector right then.'),
        ('user', 'trên máy người dùng', 'on users\' phones', 'Lộ ra ở người dùng: bằng chứng là bug report, stack trace từ Play Console, Android vitals; phải tái hiện hay đo lại trên máy dev.', 'Shows up for users: the evidence is bug reports, Play Console stack traces, Android vitals; you must reproduce or measure it again on a dev device.')]:
        m('phase.' + k, vi, en); m('phase.%s.explain' % k, xv, xe)
    for sid, tv, te, dv, de, cv, ce, cdv, cde, fv, fe, ch, ph in SY:
        m('s.%s.title' % sid, tv, te); m('s.%s.detail' % sid, dv, de); m('s.%s.cause' % sid, cv, ce); m('s.%s.causeDetail' % sid, cdv, cde); m('s.%s.fix' % sid, fv, fe)
        m('ctl.symptom.' + sid, tv, te)
    for h, vi, en in TITLES:
        n = h[1:]
        m('ch.' + h, 'L%s · %s' % (n, vi), 'L%s · %s' % (n, en)); m('go.' + h, 'Đọc L%s · %s' % (n, vi), 'Read L%s · %s' % (n, en))
    m('co.try', '''Chọn một triệu chứng bạn từng gặp; đi bốn bước rồi mở chương được chỉ tới.''', '''Pick a symptom you have met; walk the four steps, then open the chapter pointed to.''')
    m('co.cause', '''Công cụ là cách trả lời một câu hỏi cụ thể; giao diện của nó đổi theo bản Android Studio, câu hỏi thì không.''', '''A tool is a way to answer one specific question; its UI changes with Android Studio versions, the question does not.''')
    m('co.chapter', '''Chương được chỉ tới có mô phỏng đúng tình huống này, cách chữa và nguồn.''', '''The chapter pointed to simulates exactly this case, with the fix and sources.''')
    a('cap.map', '''Từ trái sang phải: triệu chứng, nơi nó lộ ra, công cụ, chương giải thích. Tab "Bảng tra" liệt kê mọi triệu chứng.''', '''Left to right: the symptom, where it shows up, the tool, the chapter that explains it. The "Lookup table" tab lists every symptom.''')
    a('preset.map', '''Gỡ lỗi · bản đồ triệu chứng, công cụ và chương''', '''Debugging · symptom map to tools and chapters''')

    z = lambda k, vi, en=None: a('vz.' + k, vi, en)
    z('tab.map', '''Bảng tra''', '''Lookup table''')
    z('map.cap', '''Mọi triệu chứng của track, nơi chúng lộ ra và chương giải thích. Hàng đang chọn được viền; ô "?" mở dần theo bước.''', '''Every symptom in the track, where it shows up and the chapter that explains it. The chosen row is outlined; "?" cells open step by step.''')
    z('map.legend', '''Chín trong mười lăm triệu chứng lộ ra trên máy người dùng, sáu khi phát triển. Với nhóm đầu, việc đầu tiên luôn là lấy bằng chứng (bug report, stack trace, vitals) rồi tái hiện.''',
      '''Nine of the fifteen symptoms show up on users\' phones, six during development. For the first group, the first job is always to get evidence (bug reports, stack traces, vitals), then reproduce.''')
    for k, vi, en in [('sym', 'Triệu chứng', 'Symptom'), ('phase', 'Lộ ra ở', 'Shows up'), ('ch', 'Chương', 'Chapter')]:
        z('map.col.' + k, vi, en)

    C = 'l0'
    a(C + '.title', '''Bản đồ track: triệu chứng, công cụ và chương''', '''Track map: symptoms, tools and chapters''')
    a(C + '.essence', '''Track này dạy tìm ra nguyên nhân thay vì đoán, bằng công cụ của Android. Mỗi chương bắt đầu từ một triệu chứng thật trên app Hẹn Khám và dạy câu hỏi mà công cụ trả lời, không dạy vị trí nút bấm, vì giao diện đổi theo từng bản Android Studio.\nPhần 1 (L1–L5) là tìm ra lỗi: quy trình gỡ lỗi, debugger, Logcat, đọc stack trace, R8 và stack trace bị làm rối. Phần 2 (L6–L9) là nhìn vào bên trong app: giao diện, dữ liệu và việc nền, bộ nhớ, trace và khung hình. Phần 3 (L10–L12) là lỗi trên máy người dùng: ANR, mạng và pin, đo hiệu năng cho đúng.\nĐang gặp một vấn đề cụ thể? Bắt đầu từ bảng tra bên dưới: tìm triệu chứng giống của bạn, rồi đọc chương được chỉ tới.''',
      '''This track teaches finding the cause instead of guessing, with Android\'s tools. Each chapter starts from a real symptom on the ClinicBook app and teaches the question a tool answers, not where its buttons are, because the UI changes with every Android Studio version.\nPart 1 (L1–L5) is finding the bug: the debugging process, the debugger, Logcat, reading stack traces, R8 and obfuscated stack traces. Part 2 (L6–L9) is looking inside the app: the UI, data and background work, memory, traces and frames. Part 3 (L10–L12) is bugs on users\' phones: ANRs, network and battery, measuring performance properly.\nFacing a specific problem? Start from the lookup table below: find the symptom that looks like yours, then read the chapter it points to.''')
    a(C + '.goal.g1', '''Đã thấy triệu chứng lộ ra ở đâu''', '''Saw where the symptom shows up''')
    a(C + '.goal.g2', '''Đã tới chương cần đọc''', '''Reached the chapter to read''')
    a(C + '.sim.debugging.map', '''triệu chứng, công cụ và chương''', '''symptoms, tools and chapters''')

    S_ = 'hook'
    a(C + '.sec.%s.title' % S_, '''Đoán trước khi đọc''', '''Predict before reading''')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'predict', '''Trong 15 triệu chứng của bảng tra, bạn đoán bao nhiêu cái lộ ra trên máy người dùng chứ không phải trên máy dev?''',
      '''Of the 15 symptoms in the lookup table, how many do you guess show up on users\' phones rather than on the dev device?''')
    B(C, S_, 1, 'ans', '''Chín. Với chúng, bạn không có debugger gắn sẵn: phải lấy bằng chứng (bug report, stack trace từ Play Console, Android vitals) rồi tái hiện hay đo lại trên máy dev. Đây là đếm trên bảng của site, không phải thống kê.''',
      '''Nine. For those you have no debugger attached: you must get evidence (bug reports, Play Console stack traces, Android vitals) and then reproduce or measure again on a dev device. This counts the site\'s table, not a statistic.''')

    S_ = 'order'
    a(C + '.sec.%s.title' % S_, '''Thứ tự đọc''', '''Reading order''')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'p', '''Đọc L1 "Quy trình gỡ lỗi, adb và bug report" trước: mọi chương sau dùng vòng tái hiện, thu hẹp, giả thuyết, kiểm. L2, L3, L4 là ba nguồn bằng chứng cơ bản (debugger, log, stack trace) và nên đọc liền nhau; L5 cần L4. L6 tới L9 đọc theo vấn đề đang gặp. L10 dùng cách đọc trace luồng gần với L9; L12 nên đọc sau cùng vì nó dạy kiểm lại mọi bản sửa hiệu năng.''',
      '''Read L1 "The debugging process, adb and bug reports" first: every later chapter uses the reproduce, narrow down, hypothesise, test loop. L2, L3 and L4 are the three basic sources of evidence (debugger, logs, stack traces) and are best read together; L5 needs L4. Read L6 to L9 by the problem you have. L10 reads thread traces much like L9; read L12 last, since it teaches checking every performance fix.''')
    B(C, S_, 2, 'p', '''Nên biết trước chương "Ngoại lệ, require/check và use" của track Kotlin: cơ chế ngôn ngữ, và các chương đầu của track Kotlin Coroutines.''',
      '''It helps to know "Exceptions, require/check and use" in the Kotlin: How the Language Works track, and the first chapters of the Kotlin Coroutines track.''')

    S_ = 'index'
    a(C + '.sec.%s.title' % S_, '''Chỉ mục: mỗi chương dùng hình gì''', '''Index: the visual of each chapter''')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'p', '''L1: vòng gỡ lỗi và bảng 8 kịch bản. L2: hai làn luồng và bảng biến tại chỗ dừng. L3: bảng log và truy vấn. L4: stack trace từng dòng, thụt lề theo tầng. L5: bảng đối chiếu frame rối và frame thật. L6: màn hình thu nhỏ với bounds và cây thành phần. L7: bảng database và chuỗi worker. L8: đường tham chiếu từ GC root và các cột bộ nhớ. L9: dòng thời gian khung hình với vạch vsync. L10: bảng trạng thái các luồng và thanh chờ. L11: request theo thời gian và dải trạng thái radio. L12: biểu đồ chấm các lần đo và trung vị.''',
      '''L1: the debugging loop and an 8-scenario table. L2: two thread lanes and the variables at the stop. L3: a log table and the query. L4: a stack trace line by line, indented by layer. L5: a table of obfuscated versus real frames. L6: a scaled screen with bounds and the component tree. L7: a database table and a worker chain. L8: the reference path from a GC root and memory bars. L9: a frame timeline with vsync marks. L10: a thread state table and a wait bar. L11: requests over time and a radio state strip. L12: a dot plot of runs and medians.''')

    S_ = 'links'
    a(C + '.sec.%s.title' % S_, '''Cầu nối sang track khác''', '''Bridges to other tracks''')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'p', '''L1 nối với "Gỡ lỗi có phương pháp: tái hiện và chia đôi" của track Mã sạch và kỷ luật làm nghề. L4 nối với "Ngoại lệ, require/check và use" của track Kotlin. L6 và L12 nối với "Hiệu năng và debug: đo trước, sửa sau" của track Compose Runtime. L7 nối với "Room cơ bản" và "Offline-first và đồng bộ nền" của track Lưu dữ liệu. L8 nối với "Lambda, closure và inline" của track Kotlin và "Dependency injection: thủ công và Hilt" của track Kiến trúc app Android. L10, L11, L12 nối với các chương "Luồng, khóa, ANR và deadlock", "Chọn kênh giao tiếp", "Cache: RAM, đĩa và HTTP", "Khởi động, pin và kích thước app" của track Thiết kế hệ thống phía mobile.''',
      '''L1 links to "Methodical debugging: reproduce and bisect" in the Clean Code and Craft track. L4 links to "Exceptions, require/check and use" in the Kotlin track. L6 and L12 link to "Performance and debugging: measure first, then fix" in the Compose Runtime track. L7 links to "Room basics" and "Offline-first and background sync" in the Saving Data track. L8 links to "Lambdas, closures and inline" in the Kotlin track and "Dependency injection: manual and Hilt" in the Android App Architecture track. L10, L11 and L12 link to "Threads, locks, ANRs and deadlock", "Choosing a channel", "Caching: memory, disk and HTTP" and "Startup, battery and app size" in the Mobile System Design track.''')

    S_ = 'recall'
    a(C + '.sec.%s.title' % S_, '''Tự trả lời''', '''Answer it yourself''')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'ask', '''Một triệu chứng lộ ra trên máy người dùng. Việc đầu tiên là gì?''', '''A symptom shows up on users\' phones. What is the first job?''')
    B(C, S_, 1, 'ans', '''Lấy bằng chứng: bug report, stack trace từ Play Console, Android vitals; rồi tái hiện hay đo lại trên máy dev.''', '''Get evidence: bug reports, Play Console stack traces, Android vitals; then reproduce or measure again on a dev device.''')

    for q, qv, qe, av, ae, wv, we in [
        ('q1', 'Bấm nút không có gì xảy ra và log trong onClick không in: mở công cụ nào?', 'A button does nothing and the log in onClick never prints: which tool?', 'Layout Inspector, chương L6.', 'Layout Inspector, chapter L6.',
         'Cú chạm không tới nút; xem thành phần nào nằm trên tại điểm chạm.', 'The tap never reaches the button; see which component is on top at the tap point.'),
        ('q2', 'App chậm dần rồi OutOfMemoryError: đọc chương nào?', 'The app slows down, then an OutOfMemoryError: which chapter?', 'L8 · Bộ nhớ: churn, rò rỉ, heap dump.', 'L8 · Memory: churn, leaks, heap dumps.',
         'Heap dump cho thấy đường tham chiếu đang giữ Activity đã đóng.', 'A heap dump shows the reference path keeping a closed Activity alive.'),
        ('q3', 'Bản sửa "nhanh hơn 41%" sau một lần đo: tin được không?', '"41% faster" after one measurement: can you trust it?', 'Chưa; đo lặp và so trung vị (L12).', 'Not yet; repeat and compare medians (L12).',
         'Một lần đo có thể là lần bất thường.', 'One measurement may be an unusual one.')]:
        a(C + '.quiz.%s.q' % q, qv, qe); a(C + '.quiz.%s.a' % q, av, ae); a(C + '.quiz.%s.why' % q, wv, we)
