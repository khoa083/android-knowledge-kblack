# Gỡ lỗi và hiệu năng · l4: đọc stack trace (Phần 1: tìm ra lỗi)
# Nguồn (chỉ ghi ở đây và docs/research/debugging.md), đọc 2026-11-25: Java SE 21 API Throwable (printStackTrace: dòng đầu là toString,
# "Caused by", "... n more" là các frame trùng với đáy stack của ngoại lệ bọc ngoài, "Suppressed" từ try-with-resources, getCause, initCause),
# developer.android.com/topic/performance/vitals/crash (FATAL EXCEPTION: main, Process, PID; loại ngoại lệ và chỗ ném là hai mảnh quan trọng;
# đi lên stack tìm chỗ truyền giá trị sai; NPE là nguyên nhân crash lớn nhất trên Google Play), studio/debug/stacktraces (dán stack trace từ
# bên ngoài; mã nguồn phải cùng phiên bản với bản tạo ra stack trace), kotlinlang.org/docs/coroutines-debugging.html (khôi phục stack trace).
# Crash ba tầng với ngày 2026-11-31 từ máy chủ là ví dụ của site; số dòng trong mã của Android là minh họa.

SEC_ORDER = {'l4': ['hook', 'anatomy', 'chain', 'appframe', 'coroutines', 'bugs', 'ex', 'recall']}


def add(a):
    def B(ch, sec, n, field, vi, en=None):
        a('%s.sec.%s.b.%02d.%s' % (ch, sec, n, field), vi, vi if en is None else en)

    a('preset.trace', '''Gỡ lỗi · đọc stack trace ba tầng tới nguyên nhân gốc''', '''Debugging · reading a three-layer stack trace down to the root cause''')
    m = lambda k, vi, en=None: a('m.trace.' + k, vi, en)
    m('title', '''Crash khi mở chi tiết lịch hẹn: sửa ở dòng đầu hay ở nguyên nhân gốc''', '''A crash when opening booking details: fix at the first line or at the root cause''')
    m('overview', '''Mở chi tiết một lịch hẹn thì app crash. Stack trace có ba ngoại lệ lồng nhau: RuntimeException của Android bọc IllegalStateException của ViewModel, và cái đó bọc DateTimeParseException từ chỗ đọc ngày. Cách 1 sửa theo dòng đầu tiên. Cách 2 đọc chuỗi "Caused by" tới cuối, tìm frame đầu tiên thuộc mã của app trong nguyên nhân gốc. Các dòng "... N more" được tính thật từ phần đáy chung giữa các stack.''',
      '''Opening a booking\'s details crashes the app. The stack trace has three nested exceptions: Android\'s RuntimeException wraps the ViewModel\'s IllegalStateException, which wraps a DateTimeParseException from where the date is read. Way 1 fixes according to the first line. Way 2 reads the "Caused by" chain to the end and finds the first frame of the app\'s own code in the root cause. The "... N more" lines are really computed from the shared bottom of the stacks.''')
    m('wrapup', '''Dòng đầu của stack trace là ngoại lệ ngoài cùng, ở đây là lời bọc của Android, không chứa một dòng mã nào của app. Nguyên nhân gốc nằm ở "Caused by" cuối cùng: ngày 2026-11-31 không tồn tại, và frame đầu tiên của app trong đó là BookingMapper.kt dòng 22. Sửa ở đó, chỗ dữ liệu đi vào, thì cả ba tầng biến mất; sửa ở tầng trên chỉ đổi crash thành một màn lỗi khó hiểu.''',
      '''The first line of a stack trace is the outermost exception, here Android\'s wrapper, with not a single line of the app\'s code in it. The root cause is in the last "Caused by": the date 2026-11-31 does not exist, and the first app frame in it is BookingMapper.kt line 22. Fix it there, where the data comes in, and all three layers go away; fixing a higher layer only turns the crash into a confusing error screen.''')
    m('simp.1', '''Stack trace được rút gọn; số dòng trong mã của Android là minh họa và đổi theo phiên bản. Tên lớp và hàm của app Hẹn Khám là của site.''',
      '''The stack trace is shortened; line numbers in Android\'s code are illustrative and change between versions. ClinicBook\'s class and function names are the site\'s.''')
    m('simp.2', '''Mỗi ngoại lệ có stack đầy đủ của nó; số frame được in và số trong dòng "... N more" được tính thật bằng JavaScript: đếm các frame cuối giống hệt nhau giữa stack của nó và stack của ngoại lệ bọc ngoài.''',
      '''Each exception has its full stack; the frames printed and the number in "... N more" are really computed in JavaScript: count the trailing frames identical between its stack and the enclosing exception\'s stack.''')
    m('ctl.hint', '''Chọn cách đọc rồi đi qua bốn bước; xem hàng nào được tô và dòng "... N more" mở ra thành gì.''', '''Pick a way of reading and walk the four steps; watch which rows are highlighted and what the "... N more" line expands into.''')
    m('ctl.case', '''Cách đọc''', '''How it is read''')
    m('ctl.case.top', '''sửa theo dòng đầu''', '''fix by the first line'''); m('ctl.case.root', '''đọc tới nguyên nhân gốc''', '''read down to the root cause''')
    m('diagramTitle', '''Ba tầng ngoại lệ''', '''Three layers of exceptions''')
    m('diagramDesc', '''Ngoại lệ gốc bị bắt và bọc lại hai lần trước khi tới hệ thống''', '''The root exception is caught and wrapped twice before it reaches the system''')
    for k, vi, en in [('root', 'Tầng gốc: DateTimeParseException, ngày không tồn tại', 'Root layer: DateTimeParseException, a date that does not exist'), ('mid', 'Tầng giữa: IllegalStateException của ViewModel', 'Middle layer: the ViewModel\'s IllegalStateException'),
                      ('outer', 'Tầng ngoài: RuntimeException của Android', 'Outer layer: Android\'s RuntimeException'), ('crash', 'Crash trên luồng main', 'Crash on the main thread')]:
        m('n.' + k, vi, en)
    m('met.layers', '''Tầng ngoại lệ đã đọc (trên 3)''', '''Exception layers read (of 3)'''); m('met.frame', '''Frame của app được chọn để sửa''', '''App frame chosen for the fix''')
    m('met.fixed', '''Nguyên nhân gốc đã sửa''', '''Root cause fixed'''); m('frame.none', '''chưa có''', '''none yet''')
    m('frame.start', '''lời gọi startActivity (không nằm trong stack)''', '''the startActivity call (not in the stack)''')
    m('frame.vm', '''DetailViewModel.kt dòng 58''', '''DetailViewModel.kt line 58'''); m('frame.mapper', '''BookingMapper.kt dòng 22''', '''BookingMapper.kt line 22''')
    m('fixed.no', '''chưa''', '''no'''); m('fixed.yes', '''đã sửa''', '''yes''')
    a('cap.trace', '''Ngoại lệ gốc ở bên trái, bị bọc dần sang phải tới khi hệ thống in crash. Ô đỏ: tầng đang bị sửa nhầm chỗ.''',
      '''The root exception on the left, wrapped step by step to the right until the system prints the crash. A red box: the layer being fixed in the wrong place.''')
    S = [
        ('top', 's1', 'Dòng đầu: RuntimeException của Android', 'The first line: Android\'s RuntimeException',
         'Dòng đầu nói "Unable to start activity", và 5 frame ngay dưới đều là mã của Android (ActivityThread, Handler, Looper). Không frame nào là của app, nên không có dòng nào của mình để sửa.',
         'The first line says "Unable to start activity", and the 5 frames under it are all Android\'s code (ActivityThread, Handler, Looper). None is the app\'s, so there is no line of yours to fix.'),
        ('top', 's2', 'Sửa theo đoán: bọc startActivity trong try/catch', 'A guessed fix: wrap startActivity in try/catch',
         'Không thấy mã của app, người sửa bọc lời mở màn chi tiết trong try/catch. Nhưng ngoại lệ được ném trong lúc Android tạo Activity, không phải ở lời gọi startActivity, nên catch đó không bao giờ chạy. App vẫn crash.',
         'With no app code in sight, the editor wraps the call that opens the details screen in try/catch. But the exception is thrown while Android creates the Activity, not inside startActivity, so that catch never runs. The app still crashes.'),
        ('top', 's3', 'Đọc thêm một tầng: sửa ở DetailViewModel.kt:58', 'Reading one layer more: fixing DetailViewModel.kt:58',
         'Caused by đầu tiên có frame của app: requireBooking ném "Booking not loaded". Người sửa trả về một Booking rỗng thay vì ném lỗi. Hết crash, nhưng màn chi tiết hiện một lịch hẹn trống.',
         'The first Caused by has app frames: requireBooking throws "Booking not loaded". The editor returns an empty Booking instead of throwing. No more crash, but the details screen shows an empty booking.'),
        ('top', 's4', 'Ngày 2026-11-31 vẫn ở đó', 'The date 2026-11-31 is still there',
         'Tầng cuối chưa ai đọc: máy chủ gửi ngày 31 tháng 11, một ngày không tồn tại. Dữ liệu hỏng vẫn đi vào app và giờ hiện thành một màn trống không lời giải thích.',
         'The last layer was never read: the server sends 31 November, a date that does not exist. The broken data still enters the app and now shows up as an empty screen with no explanation.'),
        ('root', 's1', 'Đầu crash: luồng main, tiến trình, PID', 'The crash header: the main thread, the process, the PID',
         'Logcat in "FATAL EXCEPTION: main" (crash trên luồng giao diện), rồi tên tiến trình và PID. Bên dưới là ba ngoại lệ: dòng đầu và hai dòng "Caused by". Đếm trước có mấy tầng rồi mới đọc chi tiết.',
         'Logcat prints "FATAL EXCEPTION: main" (a crash on the UI thread), then the process name and PID. Below are three exceptions: the first line and two "Caused by" lines. Count the layers before reading the details.'),
        ('root', 's2', 'Đi tới Caused by cuối cùng: ngày không tồn tại', 'Go to the last Caused by: a date that does not exist',
         'Ngoại lệ cuối cùng trong chuỗi là nguyên nhân gốc: DateTimeParseException, "Text \'2026-11-31\' could not be parsed: Invalid date \'NOVEMBER 31\'". Hai tầng trên chỉ là lời bọc thêm ngữ cảnh.',
         'The last exception in the chain is the root cause: DateTimeParseException, "Text \'2026-11-31\' could not be parsed: Invalid date \'NOVEMBER 31\'". The two layers above only wrap it with more context.'),
        ('root', 's3', 'Frame đầu tiên của app trong nguyên nhân gốc', 'The first app frame in the root cause',
         'Hai frame trên cùng thuộc thư viện java.time; frame đầu tiên của app là BookingMapper.toBooking, dòng 22. Dòng "... 8 more" nghĩa là 8 frame cuối giống hệt stack của tầng bọc ngoài, nên không in lại; mở ra thì thấy đó là DetailActivity.onCreate và mã của Android.',
         'The top two frames belong to the java.time library; the first app frame is BookingMapper.toBooking, line 22. The "... 8 more" line means the last 8 frames are identical to the enclosing layer\'s stack, so they are not printed again; expanded, they are DetailActivity.onCreate and Android\'s code.'),
        ('root', 's4', 'Sửa ở chỗ dữ liệu đi vào', 'Fix where the data comes in',
         'BookingMapper kiểm ngày ngay khi đọc từ máy chủ: ngày không hợp lệ thì trả một lỗi có tên (dữ liệu lịch hẹn hỏng) thay vì để ngoại lệ đi lên. Cả ba tầng biến mất; màn chi tiết báo rõ lịch này có lỗi dữ liệu, và máy chủ được báo để sửa.',
         'BookingMapper checks the date as soon as it is read from the server: an invalid date returns a named error (broken booking data) instead of letting the exception climb. All three layers go away; the details screen says clearly that this booking has bad data, and the server team is told to fix it.'),
    ]
    for case, k, tv, te, xv, xe in S:
        sid = case + '.' + k
        m('s.%s.title' % sid, tv, te); m('s.%s.explain' % sid, xv, xe); m('ev.' + sid, tv, te)
    for k, vi, en in [
        ('try', '''Mẹo đọc: mỗi hàng là một dòng của stack trace; hàng chữ rõ là frame thuộc mã của app (vn.henkham), hàng chữ mờ là của Android và thư viện. Hàng tô viền là chỗ đang đọc; hàng đỏ là chỗ bị sửa.''',
         '''Reading tip: each row is one line of the stack trace; full-strength rows are frames from the app\'s own code (vn.henkham), faded rows are Android and library code. The outlined rows are where you are reading; red rows are where the fix goes.'''),
        ('top.s1', '''Dòng đầu tiên là kết quả toString() của ngoại lệ ngoài cùng: tên lớp, dấu hai chấm, rồi thông điệp. Nó là tầng bọc cuối, không phải chỗ lỗi bắt đầu. [[src:java-throwable]]''',
         '''The first line is the toString() of the outermost exception: the class name, a colon, then the message. It is the last wrapper, not where the bug started. [[src:java-throwable]]'''),
        ('top.s2', '''Loại ngoại lệ và chỗ nó bị ném là hai mảnh quan trọng nhất của một stack trace. Ở đây chỗ ném nằm trong mã của Android, nên phải đọc tiếp xuống. [[src:ad-crashes]]''',
         '''The exception type and where it was thrown are the two most important pieces of a stack trace. Here the throw is inside Android\'s code, so keep reading down. [[src:ad-crashes]]'''),
        ('top.s3', '''Sửa ở tầng giữa giống phép kiểm isInitialized ở chương "Quy trình gỡ lỗi, adb và bug report": crash biến thành một màn trống, nguyên nhân vẫn còn.''',
         '''Fixing the middle layer is like the isInitialized check in "The debugging process, adb and bug reports": the crash becomes an empty screen, and the cause remains.'''),
        ('top.s4', '''Đi lên stack và xem mã, bạn có thể thấy chỗ đã truyền một giá trị sai. Ở đây giá trị sai đến từ máy chủ, và nó đi qua mọi tầng. [[src:ad-crashes]]''',
         '''Walking up the stack and reading the code, you may find the place that passed a wrong value. Here the wrong value comes from the server and passes through every layer. [[src:ad-crashes]]'''),
        ('root.s1', '''Crash trên Android trong Logcat bắt đầu bằng "--- beginning of crash", rồi "FATAL EXCEPTION: <tên luồng>" và "Process: <package>, PID: <số>". [[src:ad-crashes]]''',
         '''An Android crash in Logcat starts with "--- beginning of crash", then "FATAL EXCEPTION: <thread name>" and "Process: <package>, PID: <number>". [[src:ad-crashes]]'''),
        ('root.s2', '''Khi một ngoại lệ có cause, stack trace của nó in thêm phần "Caused by" cho cause, và cứ thế xuống tới ngoại lệ không có cause nào nữa. [[src:java-throwable]]''',
         '''When an exception has a cause, its stack trace also prints a "Caused by" section for that cause, and so on down to an exception with no cause. [[src:java-throwable]]'''),
        ('root.s3', '''"... n more" nghĩa là phần còn lại của stack trace này trùng với n frame cuối của stack trace của ngoại lệ bọc ngoài. [[src:java-throwable]]''',
         '''"... n more" means the rest of this stack trace matches the last n frames of the enclosing exception\'s stack trace. [[src:java-throwable]]'''),
        ('root.s4', '''Đây là cách "parse một lần ở ranh giới": dữ liệu từ ngoài được kiểm và đổi thành kiểu rõ ràng ngay khi vào app, như chương "Đóng gói, bất biến, parse một lần" của track Mã sạch và kỷ luật làm nghề.''',
         '''This is "parse once at the boundary": data from outside is checked and turned into a clear type as soon as it enters the app, as in "Encapsulation, immutability, parse once" in the Clean Code and Craft track.'''),
    ]:
        m('co.' + k, vi, en)

    z = lambda k, vi, en=None: a('vz.' + k, vi, en)
    z('tab.trace', '''Stack trace từng dòng''', '''Stack trace line by line''')
    z('tr.more', '''... {n} more   (frame trùng tầng bọc ngoài)''', '''... {n} more   (frames shared with the enclosing layer)''')
    z('tr.expanded', '''(frame trùng với tầng bọc ngoài, mở ra)''', '''(frames shared with the enclosing layer, expanded)''')
    z('tr.focus.top.0', '''Đang đọc: dòng đầu và các frame của nó; 0 frame của app.''', '''Reading: the first line and its frames; 0 app frames.''')
    z('tr.focus.top.1', '''Sửa ở lời gọi startActivity: không nằm trên đường đi của ngoại lệ, vẫn crash.''', '''Fixing at the startActivity call: not on the exception\'s path, still crashing.''')
    z('tr.focus.top.2', '''Sửa ở DetailViewModel.kt:58: hết crash, ra lịch hẹn trống.''', '''Fixing at DetailViewModel.kt:58: no crash, an empty booking.''')
    z('tr.focus.top.3', '''Tầng cuối chưa ai đọc: ngày 2026-11-31 vẫn đi vào app.''', '''The last layer was never read: the date 2026-11-31 still enters the app.''')
    z('tr.focus.root.0', '''Đếm tầng: 1 dòng đầu, {n} dòng "Caused by".''', '''Counting layers: 1 first line, {n} "Caused by" lines.''')
    z('tr.focus.root.1', '''Caused by cuối cùng là nguyên nhân gốc.''', '''The last Caused by is the root cause.''')
    z('tr.focus.root.2', '''Frame đầu của app trong nguyên nhân gốc: {f}.''', '''The first app frame in the root cause: {f}.''')
    z('tr.focus.root.3', '''Sửa ở {f}: kiểm ngày ngay khi đọc từ máy chủ.''', '''Fix at {f}: check the date as soon as it is read from the server.''')
    z('tr.legend', '''Mỗi hàng là một dòng của stack trace, thụt lề theo tầng. Chữ rõ: frame của app; chữ mờ: frame của Android và thư viện. Viền: chỗ đang đọc. Đỏ: chỗ đặt bản sửa.''',
      '''Each row is one line of the stack trace, indented by layer. Full-strength text: an app frame; faded text: Android and library frames. Outline: where you are reading. Red: where the fix goes.''')

    C = 'l4'
    a(C + '.title', '''Đọc stack trace''', '''Reading stack traces''')
    a(C + '.essence', '''Stack trace là ảnh chụp chuỗi lời gọi hàm tại lúc ngoại lệ được ném: dòng đầu là loại ngoại lệ và thông điệp, mỗi dòng "at" là một frame (một hàm đang chạy dở), frame trên cùng là chỗ ném.\nKhi một ngoại lệ được bắt rồi bọc vào ngoại lệ khác, stack trace in thêm phần "Caused by". Nguyên nhân gốc thường nằm ở "Caused by" cuối cùng, không phải ở dòng đầu. Dòng "... N more" chỉ là N frame cuối trùng với tầng bọc ngoài, được bỏ bớt cho gọn.\nCách đọc: đếm số tầng, đi tới tầng cuối, tìm frame đầu tiên thuộc mã của app trong tầng đó, rồi đi lên stack để xem giá trị sai đến từ đâu.''',
      '''A stack trace is a snapshot of the chain of function calls at the moment an exception was thrown: the first line is the exception type and message, each "at" line is a frame (a function still running), and the top frame is where it was thrown.\nWhen an exception is caught and wrapped in another, the stack trace prints an extra "Caused by" section. The root cause is usually in the last "Caused by", not in the first line. A "... N more" line is just N trailing frames shared with the enclosing layer, left out for brevity.\nHow to read one: count the layers, go to the last one, find the first frame from the app\'s own code in it, then walk up the stack to see where the wrong value came from.''')
    a(C + '.goal.g1', '''Đã tới Caused by cuối cùng''', '''Reached the last Caused by''')
    a(C + '.goal.g2', '''Đã sửa ở frame đầu của app trong nguyên nhân gốc''', '''Fixed at the first app frame in the root cause''')
    a(C + '.sim.debugging.trace', '''sửa theo dòng đầu, hay đọc tới nguyên nhân gốc''', '''fixing by the first line, or reading down to the root cause''')

    S_ = 'hook'
    a(C + '.sec.%s.title' % S_, '''Đoán trước khi đọc''', '''Predict before reading''')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'predict', '''Một crash in ra: dòng đầu "RuntimeException: Unable to start activity", rồi hai dòng "Caused by", cái cuối là "DateTimeParseException: Text \'2026-11-31\' could not be parsed". Lỗi bắt đầu ở tầng nào, và có bao nhiêu dòng trong tầng đầu là mã của app?''',
      '''A crash prints: a first line "RuntimeException: Unable to start activity", then two "Caused by" lines, the last being "DateTimeParseException: Text \'2026-11-31\' could not be parsed". Which layer did the bug start in, and how many lines of the first layer are the app\'s code?''')
    B(C, S_, 1, 'ans', '''Ở tầng cuối: ngày 31 tháng 11 không tồn tại. Tầng đầu là lời bọc của Android, 0 dòng là mã của app. Mô phỏng ngay dưới so việc sửa theo dòng đầu với việc đọc tới nguyên nhân gốc.''',
      '''In the last layer: 31 November does not exist. The first layer is Android\'s wrapper, with 0 lines of the app\'s code. The simulation just below compares fixing by the first line with reading down to the root cause.''')

    S_ = 'anatomy'
    a(C + '.sec.%s.title' % S_, '''Cấu tạo một stack trace''', '''Anatomy of a stack trace''')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'p', '''App viết bằng Java hay Kotlin crash khi một ngoại lệ (một Throwable) bị ném mà không ai bắt. Stack trace là ảnh chụp chuỗi hàm lồng nhau đang chạy dở tại lúc đó. Dòng đầu là toString() của ngoại lệ: tên lớp, dấu hai chấm, thông điệp. Mỗi dòng "at" là một frame: lớp, hàm, tên file và số dòng. Frame trên cùng là chỗ ngoại lệ được tạo và ném; đi xuống là các hàm đã gọi tới đó. [[src:ad-crashes]] [[src:java-throwable]]''',
      '''An app written in Java or Kotlin crashes when an exception (a Throwable) is thrown and nobody catches it. A stack trace is a snapshot of the nested functions still running at that moment. The first line is the exception\'s toString(): the class name, a colon, the message. Each "at" line is a frame: class, function, file name and line number. The top frame is where the exception was created and thrown; going down are the functions that called their way there. [[src:ad-crashes]] [[src:java-throwable]]''')
    B(C, S_, 2, 'kt', '''--- beginning of crash
AndroidRuntime: FATAL EXCEPTION: main
Process: vn.henkham, PID: 4120
java.lang.RuntimeException: Unable to start activity ComponentInfo{vn.henkham/vn.henkham.DetailActivity}: java.lang.IllegalStateException: Booking not loaded
    at android.app.ActivityThread.performLaunchActivity(ActivityThread.java:4206)
    ...''')
    B(C, S_, 3, 'p', '''Loại ngoại lệ thường là gợi ý mạnh nhất về chuyện gì đã sai: NullPointerException là đọc một giá trị null (nguyên nhân crash lớn nhất trên Google Play), IllegalStateException là gọi hàm khi đối tượng chưa ở trạng thái đúng, DateTimeParseException là chuỗi ngày không đọc được. Dòng ngay sau tên ngoại lệ cho biết nó được ném ở đâu. [[src:ad-crashes]]''',
      '''The exception type is usually the strongest hint about what went wrong: NullPointerException means reading a null value (the largest cause of crashes on Google Play), IllegalStateException means calling something when the object is not in the right state, DateTimeParseException means a date string that cannot be read. The line right after the exception\'s name says where it was thrown. [[src:ad-crashes]]''')

    S_ = 'chain'
    a(C + '.sec.%s.title' % S_, '''Caused by, "... N more" và Suppressed''', '''Caused by, "... N more" and Suppressed''')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'p', '''Mã thường bắt một ngoại lệ cấp thấp rồi ném một ngoại lệ có ý nghĩa hơn, gắn cái cũ làm cause: throw IllegalStateException("Booking not loaded", e). Khi in, ngoại lệ có cause in thêm phần "Caused by" cho cause, cứ thế tới tầng không còn cause. Tầng cuối là nơi chuyện bắt đầu; các tầng trên thêm ngữ cảnh. [[src:java-throwable]]''',
      '''Code often catches a low-level exception and throws a more meaningful one, attaching the old one as its cause: throw IllegalStateException("Booking not loaded", e). When printed, an exception with a cause prints an extra "Caused by" section for it, and so on until a layer with no cause. The last layer is where things started; the layers above add context. [[src:java-throwable]]''')
    B(C, S_, 2, 'p', '''Mỗi tầng có stack riêng, và phần đáy của chúng thường giống nhau (cùng đi qua onCreate, cùng vòng lặp của luồng main). Để khỏi in lại, Java thay phần trùng bằng "... n more": n frame cuối của tầng này giống hệt n frame cuối của tầng bọc ngoài. Đó không phải frame bị mất; muốn xem thì đọc ở tầng trên. [[src:java-throwable]]''',
      '''Each layer has its own stack, and their bottoms are often identical (all through onCreate, all in the main thread\'s loop). To avoid printing them again, Java replaces the shared part with "... n more": the last n frames of this layer are identical to the last n frames of the enclosing layer. They are not lost frames; to see them, read the layer above. [[src:java-throwable]]''')
    B(C, S_, 3, 'p', '''Phần "Suppressed:" xuất hiện khi một ngoại lệ phụ bị gác lại để ngoại lệ chính đi tiếp, thường do try-with-resources (trong Kotlin là use): khối chính ném lỗi, rồi lúc đóng tài nguyên lại ném thêm lỗi nữa; lỗi đóng được gắn làm suppressed, in thụt vào dưới ngoại lệ chính. [[src:java-throwable]]''',
      '''A "Suppressed:" section appears when a secondary exception is set aside so the main one can propagate, usually through try-with-resources (use in Kotlin): the main block throws, then closing the resource throws too; the closing error is attached as suppressed and printed indented under the main exception. [[src:java-throwable]]''')

    S_ = 'appframe'
    a(C + '.sec.%s.title' % S_, '''Tìm frame của app và đi lên stack''', '''Finding the app\'s frames and walking up the stack''')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'p', '''Trong mỗi tầng, bỏ qua các frame của Android, Kotlin và thư viện ở trên cùng; frame đầu tiên có package của app là chỗ mã của bạn chạm vào lỗi. Nếu không tầng nào có mã của app, có thể một giá trị sai đã được đưa cho một việc bất đồng bộ (chạy sau, trên luồng khác), nên stack lúc crash không còn chứa chỗ đã gọi. [[src:ad-crashes]]''',
      '''In each layer, skip the Android, Kotlin and library frames at the top; the first frame with the app\'s package is where your code touched the error. If no layer contains app code, a wrong value may have been handed to asynchronous work (running later, on another thread), so the stack at the crash no longer contains the caller. [[src:ad-crashes]]''')
    B(C, S_, 2, 'p', '''Stack trace từ Play Console hay từ bug report có thể dán vào Android Studio để mỗi frame thành liên kết tới mã. Điều kiện: mã nguồn bạn đang xem phải cùng phiên bản với bản app đã tạo ra stack trace, nếu không thì tên file, số dòng và thứ tự gọi sẽ không khớp. Bản release còn có thể bị R8 đổi tên lớp; chương "R8 và stack trace bị làm rối" nói cách dịch ngược. [[src:ad-stacktraces]]''',
      '''A stack trace from Play Console or a bug report can be pasted into Android Studio so each frame becomes a link to the code. The condition: the source you are looking at must be the same version as the app that produced the stack trace, otherwise file names, line numbers and call order will not match. Release builds may also have class names renamed by R8; the chapter "R8 and obfuscated stack traces" explains how to translate them back. [[src:ad-stacktraces]]''')
    B(C, S_, 3, 'kt', '''// BookingMapper.kt: kiểm ngày ngay khi dữ liệu đi vào app
fun toBooking(dto: BookingDto): Outcome<BookingError, Booking> {
    val date = runCatching { LocalDate.parse(dto.date) }.getOrNull()
        ?: return Outcome.Err(BookingError.BadData("date=${dto.date}"))
    return Outcome.Ok(Booking(dto.id, date, dto.patientName))
}''', '''// BookingMapper.kt: check the date as soon as the data enters the app
fun toBooking(dto: BookingDto): Outcome<BookingError, Booking> {
    val date = runCatching { LocalDate.parse(dto.date) }.getOrNull()
        ?: return Outcome.Err(BookingError.BadData("date=${dto.date}"))
    return Outcome.Ok(Booking(dto.id, date, dto.patientName))
}''')
    B(C, S_, 4, 'note', '''Ở đây runCatching chỉ bọc đúng lời parse ngày, nên không nuốt bug nào khác. Cách trả lỗi như một giá trị có kiểu được nói ở chương "Lỗi là giá trị" của track Lập trình hàm với Kotlin.''',
      '''Here runCatching wraps only the date parse, so it swallows no other bug. Returning errors as typed values is covered in "Errors as values" in the Functional Programming in Kotlin track.''')
    B(C, S_, 4, 'kind', 'mechanism')

    S_ = 'coroutines'
    a(C + '.sec.%s.title' % S_, '''Stack trace của coroutine''', '''Coroutine stack traces''')
    a(C + '.sec.%s.badge' % S_, 'version')
    B(C, S_, 1, 'p', '''Khi một coroutine suspend rồi chạy tiếp trên luồng khác, stack lúc ngoại lệ được ném không còn chứa chỗ đã gọi hàm suspend. Ở chế độ debug, kotlinx-coroutines khôi phục stack trace: khi ngoại lệ đi qua một lời gọi suspend như await(), thư viện tạo một bản sao của ngoại lệ có thêm các frame phía bên đang chờ, và gắn ngoại lệ gốc làm cause. [[src:kx-coroutines-debug]]''',
      '''When a coroutine suspends and resumes on another thread, the stack at the time the exception is thrown no longer contains the place that called the suspend function. In debug mode, kotlinx-coroutines recovers the stack trace: when the exception passes through a suspending call such as await(), the library creates a copy of the exception with extra frames from the waiting side, and attaches the original exception as its cause. [[src:kx-coroutines-debug]]''')
    B(C, S_, 2, 'p', '''Vì vậy với coroutine, bạn thường thấy cùng một ngoại lệ hai lần: bản sao ở trên với các frame của nơi đang chờ, và bản gốc trong "Caused by" với chỗ thật sự ném. Giữa các frame có một dòng ranh giới _COROUTINE._BOUNDARY. Đọc như mọi chuỗi cause: bản gốc ở cuối là chỗ lỗi xảy ra, phần trên cho biết ai đang chờ kết quả. Cách bật chế độ debug được nói ở chương "Debugger: breakpoint, watch, evaluate". [[src:kx-coroutines-debug]]''',
      '''So with coroutines you often see the same exception twice: the copy on top with frames from the waiting side, and the original in "Caused by" with where it was really thrown. Among the frames there is a boundary line, _COROUTINE._BOUNDARY. Read it like any cause chain: the original at the bottom is where the error happened, the part above tells you who was waiting for the result. Turning on debug mode is covered in "The debugger: breakpoints, watches, evaluate". [[src:kx-coroutines-debug]]''')

    S_ = 'bugs'
    a(C + '.sec.%s.title' % S_, '''Hai lỗi hay gặp''', '''Two common bugs''')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'bug', '''Báo cáo crash nào cũng chỉ còn một dòng "IllegalStateException: something went wrong", không có Caused by.''', '''Every crash report now shows only "IllegalStateException: something went wrong", with no Caused by.''')
    B(C, S_, 1, 'cause', '''Mã bọc lỗi viết throw IllegalStateException("something went wrong") mà không truyền e làm cause; nguyên nhân gốc bị vứt đi.''', '''The wrapping code writes throw IllegalStateException("something went wrong") without passing e as the cause; the root cause is thrown away.''')
    B(C, S_, 1, 'fix', '''Luôn truyền ngoại lệ cũ làm cause khi bọc: IllegalStateException("Booking $id not loaded", e).''', '''Always pass the old exception as the cause when wrapping: IllegalStateException("Booking $id not loaded", e).''')
    B(C, S_, 2, 'bug', '''Số dòng trong stack trace từ Play Console chỉ vào một dòng trống trong file.''', '''A line number in a Play Console stack trace points at an empty line in the file.''')
    B(C, S_, 2, 'cause', '''Đang xem mã của nhánh main, còn crash đến từ bản 1.4.0 đã phát hành tháng trước.''', '''You are looking at the main branch, while the crash comes from release 1.4.0 shipped last month.''')
    B(C, S_, 2, 'fix', '''Checkout đúng tag git (nhãn đánh dấu commit của một bản phát hành) của phiên bản trong báo cáo crash rồi mới đọc mã.''', '''Check out the git tag (the label marking a release's commit) of the version in the crash report before reading the code.''')

    S_ = 'ex'
    a(C + '.sec.%s.title' % S_, '''Bài tập''', '''Exercise''')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'ex', '''Đọc stack trace dưới và trả lời: có mấy tầng; nguyên nhân gốc là gì; frame đầu tiên của app trong nguyên nhân gốc là dòng nào; dòng "... 6 more" ứng với những frame nào?''',
      '''Read the stack trace below and answer: how many layers are there; what is the root cause; which line is the first app frame in the root cause; which frames does the "... 6 more" line stand for?''')
    B(C, S_, 1, 'exkt', '''java.lang.RuntimeException: Payment failed
    at vn.henkham.pay.PayViewModel.pay(PayViewModel.kt:40)
    at vn.henkham.pay.PayFragment.onPayClicked(PayFragment.kt:72)
    at android.view.View.performClick(View.java:7659)
    ... (4 frame của Android)
Caused by: java.lang.NumberFormatException: For input string: "150.000"
    at java.lang.Long.parseLong(Long.java:711)
    at vn.henkham.pay.PriceParser.parse(PriceParser.kt:12)
    at vn.henkham.pay.PayViewModel.pay(PayViewModel.kt:37)
    ... 6 more''', '''java.lang.RuntimeException: Payment failed
    at vn.henkham.pay.PayViewModel.pay(PayViewModel.kt:40)
    at vn.henkham.pay.PayFragment.onPayClicked(PayFragment.kt:72)
    at android.view.View.performClick(View.java:7659)
    ... (4 Android frames)
Caused by: java.lang.NumberFormatException: For input string: "150.000"
    at java.lang.Long.parseLong(Long.java:711)
    at vn.henkham.pay.PriceParser.parse(PriceParser.kt:12)
    at vn.henkham.pay.PayViewModel.pay(PayViewModel.kt:37)
    ... 6 more''')
    B(C, S_, 1, 'hint', '''Tầng có cause in thêm Caused by; "... n more" là n frame cuối trùng với tầng bọc ngoài. Frame của app có package vn.henkham.''', '''A layer with a cause prints a Caused by; "... n more" is n trailing frames shared with the enclosing layer. App frames have the package vn.henkham.''')
    B(C, S_, 1, 'sol', '''Hai tầng. Nguyên nhân gốc: chuỗi giá "150.000" có dấu chấm ngăn cách hàng nghìn, Long.parseLong không đọc được. Frame đầu của app trong đó: PriceParser.kt dòng 12. "... 6 more" là PayFragment.onPayClicked, View.performClick và 4 frame của Android, giống hệt đáy của tầng trên (dòng 37 và 40 của PayViewModel khác nhau nên không tính).''',
      '''Two layers. The root cause: the price string "150.000" has a dot as the thousands separator, which Long.parseLong cannot read. The first app frame in it: PriceParser.kt line 12. "... 6 more" is PayFragment.onPayClicked, View.performClick and 4 Android frames, identical to the bottom of the layer above (lines 37 and 40 of PayViewModel differ, so they are not counted).''')

    S_ = 'recall'
    a(C + '.sec.%s.title' % S_, '''Tự trả lời''', '''Answer it yourself''')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'ask', '''Nguyên nhân gốc của một crash thường nằm ở đâu trong stack trace?''', '''Where in a stack trace is the root cause of a crash usually found?''')
    B(C, S_, 1, 'ans', '''Ở "Caused by" cuối cùng; dòng đầu là tầng bọc ngoài cùng.''', '''In the last "Caused by"; the first line is the outermost wrapper.''')
    B(C, S_, 2, 'ask', '''"... 8 more" có phải 8 frame bị mất không?''', '''Does "... 8 more" mean 8 frames were lost?''')
    B(C, S_, 2, 'ans', '''Không. Đó là 8 frame cuối trùng với tầng bọc ngoài, đã in ở tầng đó.''', '''No. They are the last 8 frames shared with the enclosing layer, already printed there.''')

    for q, qv, qe, av, ae, wv, we in [
        ('q1', 'Dòng đầu tiên của stack trace là gì?', 'What is the first line of a stack trace?', 'toString() của ngoại lệ ngoài cùng: tên lớp và thông điệp.', 'The outermost exception\'s toString(): its class name and message.',
         'Các tầng sâu hơn nằm trong các phần Caused by.', 'Deeper layers are in the Caused by sections.'),
        ('q2', 'Frame trên cùng của một tầng cho biết gì?', 'What does the top frame of a layer tell you?', 'Chỗ ngoại lệ của tầng đó được tạo và ném.', 'Where that layer\'s exception was created and thrown.',
         'Đi xuống là các hàm đã gọi tới đó.', 'Going down are the functions that called their way there.'),
        ('q3', 'Bọc ngoại lệ mà quên truyền cause thì sao?', 'What happens if you wrap an exception without passing the cause?', 'Mất phần Caused by và cả nguyên nhân gốc.', 'The Caused by section, and with it the root cause, is lost.',
         'Luôn truyền ngoại lệ cũ vào constructor của ngoại lệ mới.', 'Always pass the old exception to the new exception\'s constructor.'),
        ('q4', 'Vì sao stack trace của coroutine hay có cùng ngoại lệ hai lần?', 'Why do coroutine stack traces often show the same exception twice?', 'Khôi phục stack trace tạo một bản sao có frame phía bên đang chờ, gắn bản gốc làm cause.', 'Stack trace recovery creates a copy with frames from the waiting side and attaches the original as the cause.',
         'Bản gốc ở Caused by là chỗ lỗi thật sự xảy ra.', 'The original in Caused by is where the error really happened.')]:
        a(C + '.quiz.%s.q' % q, qv, qe); a(C + '.quiz.%s.a' % q, av, ae); a(C + '.quiz.%s.why' % q, wv, we)
