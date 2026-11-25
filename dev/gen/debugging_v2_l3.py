# Gỡ lỗi và hiệu năng · l3: Logcat (Phần 1: tìm ra lỗi)
# Nguồn (chỉ ghi ở đây và docs/research/debugging.md), đọc 2026-11-25, các trang không ghi ngày: developer.android.com/studio/debug/logcat
# (định dạng dòng, cú pháp truy vấn key:value, cùng key thì OR, khác key thì AND, level: là mức đó trở lên, package:mine, is:crash, age:),
# reference/android/util/Log (mức, hằng số, wtf, isLoggable mặc định INFO, setprop log.tag, giới hạn tag 23 ký tự tới API 25, tạo chuỗi tốn cấp phát),
# tools/logcat (adb logcat tag:priority *:S, -v threadtime mặc định, -b buffer, logd, bốn tầng lọc), privacy-and-security/risks/log-info-disclosure
# (READ_LOGS từ API 16, không log dữ liệu nhạy cảm, R8 -assumenosideeffects xóa v/d/i). 16 dòng log và hai dòng lộ số điện thoại là của site.

SEC_ORDER = {'l3': ['hook', 'levels', 'filter', 'cmdline', 'release', 'bugs', 'ex', 'recall']}


def add(a):
    def B(ch, sec, n, field, vi, en=None):
        a('%s.sec.%s.b.%02d.%s' % (ch, sec, n, field), vi, vi if en is None else en)

    a('preset.logcat', '''Gỡ lỗi · lọc Logcat và log trong bản release''', '''Debugging · filtering Logcat and logs in release builds''')
    m = lambda k, vi, en=None: a('m.logcat.' + k, vi, en)
    m('title', '''Tìm dòng "lưu thất bại" giữa log của cả máy''', '''Finding the "save failed" line among the whole device\'s logs''')
    m('overview', '''Logcat nhận log của mọi tiến trình trên máy: hệ thống, các app khác, và app Hẹn Khám. 16 dòng dưới đây là một lát cắt rất nhỏ. Cách 1 lọc dần để tìm dòng lỗi lưu lịch hẹn: theo app, theo mức, theo tag. Cách 2 xem log nào của app còn lại trong bản release khi R8 xóa các lời gọi Log.v, Log.d, Log.i, và dòng nào vẫn lộ số điện thoại.''',
      '''Logcat receives logs from every process on the device: the system, other apps, and ClinicBook. The 16 lines below are a tiny slice. Way 1 filters step by step to find the line where saving a booking failed: by app, by level, by tag. Way 2 looks at which of the app\'s logs remain in a release build when R8 removes the Log.v, Log.d and Log.i calls, and which line still leaks a phone number.''')
    m('wrapup', '''Lọc theo app bỏ được nửa số dòng; thêm mức WARN trở lên còn 2 dòng, trong đó có dòng lỗi. Cùng key thì các điều kiện được OR, khác key thì AND, nên "tag:BookingRepo tag:Sync" lấy dòng của cả hai tag. Trong bản release, R8 xóa log mức thấp, nhưng dòng mức WARN vẫn in số điện thoại: chỉ log id hay hằng số, đừng log dữ liệu người dùng.''',
      '''Filtering by app drops half the lines; adding level WARN and above leaves 2, including the error line. Terms with the same key are OR\'d and different keys are AND\'d, so "tag:BookingRepo tag:Sync" keeps lines from both tags. In the release build, R8 removes the low-level logs, but a WARN line still prints the phone number: log ids or constants, never user data.''')
    m('simp.1', '''16 dòng là của site; máy thật in hàng trăm hay hàng nghìn dòng mỗi giây. Cột thời gian và thread ID được bỏ cho gọn.''',
      '''The 16 lines are the site\'s; a real device prints hundreds or thousands of lines a second. The time and thread ID columns are left out for brevity.''')
    m('simp.2', '''Bộ lọc được áp thật bằng JavaScript lên 16 dòng theo luật của truy vấn Logcat: cùng key thì OR, khác key thì AND, level: là mức đó trở lên. Dòng còn trong bản release được tính bằng cách bỏ mọi dòng mức VERBOSE, DEBUG, INFO.''',
      '''The filters are really applied in JavaScript to the 16 lines by the rules of Logcat queries: the same key is OR\'d, different keys AND\'d, and level: means that level or higher. The lines left in the release build are computed by dropping every VERBOSE, DEBUG and INFO line.''')
    m('ctl.hint', '''Chọn việc cần làm rồi đi qua bốn bước; xem truy vấn ở trên bảng và các hàng mờ đi.''', '''Pick a task and walk the four steps; watch the query above the table and the rows that fade out.''')
    m('ctl.case', '''Việc cần làm''', '''Task''')
    m('ctl.case.find', '''tìm dòng lỗi''', '''find the error line'''); m('ctl.case.release', '''log trong bản release''', '''logs in the release build''')
    m('diagramTitle', '''Từ Log.d tới màn Logcat''', '''From Log.d to the Logcat window''')
    m('diagramDesc', '''Lời gọi Log ghi vào buffer của logd; Logcat đọc và lọc; R8 có thể xóa lời gọi từ lúc build''', '''Log calls write to logd\'s buffers; Logcat reads and filters; R8 can remove the calls at build time''')
    for k, vi, en in [('app', 'Lời gọi Log trong app', 'Log calls in the app'), ('r8', 'R8 lúc build release', 'R8 at release build time'), ('logd', 'logd: buffer vòng', 'logd: ring buffers'),
                      ('others', 'Hệ thống và app khác', 'The system and other apps'), ('view', 'Logcat: truy vấn lọc', 'Logcat: filter query')]:
        m('n.' + k, vi, en)
    m('met.shown', '''Dòng còn hiện (trên 16)''', '''Lines shown (of 16)'''); m('met.app', '''Dòng của app''', '''App lines''')
    m('met.pii', '''Dòng lộ số điện thoại''', '''Lines leaking a phone number'''); m('met.found', '''Thấy dòng lỗi''', '''Error line visible''')
    m('found.yes', '''có''', '''yes'''); m('found.no', '''lẫn trong đám đông''', '''lost in the crowd''')
    a('cap.logcat', '''Log của app và của cả hệ thống cùng vào buffer của logd; Logcat lọc chúng bằng truy vấn. Ô đỏ: dòng lỗi khó thấy, hay dòng lộ dữ liệu người dùng.''',
      '''Logs from the app and from the whole system go into logd\'s buffers; Logcat filters them with a query. A red box: an error line hard to see, or a line leaking user data.''')
    S = [
        ('find', 's1', 'Không lọc: 16 dòng của mọi tiến trình', 'No filter: 16 lines from every process',
         'Logcat hiện log của hệ thống, của dịch vụ Google Play, của thanh trạng thái và của app, xen kẽ nhau theo thời gian. Dòng "save failed" nằm đâu đó ở giữa. Trên máy thật con số là hàng nghìn dòng mỗi giây.',
         'Logcat shows logs from the system, Google Play services, the status bar and the app, interleaved in time. The "save failed" line is somewhere in the middle. On a real device it is thousands of lines a second.'),
        ('find', 's2', 'package:mine: chỉ còn log của app', 'package:mine: only the app\'s logs remain',
         'package:mine giữ các dòng thuộc package của project đang mở. Còn 8 trên 16 dòng, nhưng vẫn lẫn log DEBUG, VERBOSE, INFO.',
         'package:mine keeps lines belonging to the packages of the open project. 8 of 16 lines remain, still mixed with DEBUG, VERBOSE and INFO logs.'),
        ('find', 's3', 'Thêm level:WARN: còn 2 dòng, có dòng lỗi', 'Add level:WARN: 2 lines left, including the error',
         'level:WARN nghĩa là WARN trở lên: WARN, ERROR, ASSERT. Hai key khác nhau được AND với nhau, nên còn 2 dòng: một cảnh báo thử lại của Sync và dòng ERROR "save failed: SQLiteConstraintException".',
         'level:WARN means WARN and above: WARN, ERROR, ASSERT. Two different keys are AND\'d together, so 2 lines remain: a Sync retry warning and the ERROR line "save failed: SQLiteConstraintException".'),
        ('find', 's4', 'Xem ngữ cảnh: tag:BookingRepo tag:Sync', 'See the context: tag:BookingRepo tag:Sync',
         'Muốn biết chuyện gì xảy ra trước dòng lỗi, bỏ điều kiện mức và lọc theo hai tag. Cùng key tag thì được OR, nên còn 7 dòng của cả hai tag ở mọi mức: thấy Sync nhận mã 409 từ máy chủ (xung đột: lịch đã có) rồi BookingRepo lưu trùng.',
         'To see what happened before the error, drop the level and filter by two tags. The same tag key is OR\'d, so 7 lines from both tags at every level remain: Sync gets a 409 from the server (a conflict: the booking already exists), then BookingRepo saves a duplicate.'),
        ('release', 's1', 'Bản debug: 8 dòng của app, 2 dòng in số điện thoại', 'Debug build: 8 app lines, 2 print a phone number',
         'Lọc package:mine trên bản debug. Hai dòng in nguyên số điện thoại của bệnh nhân: một Log.d của BookingRepo và một Log.w của Sync. Ở bản debug trên máy dev điều đó vô hại; ở bản phát hành thì không.',
         'Filter package:mine on the debug build. Two lines print the patient\'s full phone number: a Log.d in BookingRepo and a Log.w in Sync. On a debug build on a dev device that is harmless; in a release it is not.'),
        ('release', 's2', 'Bản release với R8 xóa Log.v, Log.d, Log.i: còn 2 dòng', 'Release build with R8 removing Log.v, Log.d, Log.i: 2 lines left',
         'Quy tắc -assumenosideeffects cho android.util.Log báo R8 rằng các lời gọi v, d, i không có tác dụng gì, nên R8 xóa chúng. Chỉ còn dòng WARN và ERROR của app.',
         'An -assumenosideeffects rule for android.util.Log tells R8 that the v, d and i calls have no effect, so R8 removes them. Only the app\'s WARN and ERROR lines remain.'),
        ('release', 's3', 'Dòng WARN vẫn in số điện thoại', 'The WARN line still prints the phone number',
         'R8 chỉ xóa đúng các mức được liệt kê. Log.w trong Sync vẫn còn, và nó vẫn in số điện thoại. Log cũng nằm trong bug report và có thể bị đọc qua adb; xóa log theo mức không thay được việc đừng log dữ liệu nhạy cảm.',
         'R8 removes only the levels listed. Log.w in Sync is still there, and it still prints the phone number. Logs also go into bug reports and can be read over adb; removing logs by level does not replace not logging sensitive data.'),
        ('release', 's4', 'Sửa: chỉ log id', 'Fix: log only the id',
         'Đổi thông điệp thành "retry 1 for booking id=42". Đủ để lần theo lỗi (id tra được trong database), không chứa dữ liệu cá nhân. Còn 0 dòng lộ số điện thoại.',
         'Change the message to "retry 1 for booking id=42". It is enough to trace the bug (the id can be looked up in the database) and holds no personal data. 0 lines leak a phone number.'),
    ]
    for case, k, tv, te, xv, xe in S:
        sid = case + '.' + k
        m('s.%s.title' % sid, tv, te); m('s.%s.explain' % sid, xv, xe); m('ev.' + sid, tv, te)
    for k, vi, en in [
        ('try', '''Mẹo đọc: dòng truy vấn ở trên bảng là thứ gõ vào ô lọc của Logcat. Hàng mờ là dòng bị lọc đi; hàng đỏ là dòng lỗi cần tìm, hay dòng lộ dữ liệu.''',
         '''Reading tip: the query above the table is what goes in Logcat\'s filter box. Faded rows are filtered out; red rows are the error line you are looking for, or a line leaking data.'''),
        ('find.s2', '''Mỗi dòng Logcat có ngày, giờ, process ID và thread ID, tag, package, mức và nội dung. package:mine khớp mọi package có trong project đang mở. [[src:ad-logcat]]''',
         '''Each Logcat line has a date, time, process and thread ID, tag, package, priority and message. package:mine matches any package in the open project. [[src:ad-logcat]]'''),
        ('find.s3', '''level: lấy mức đó và các mức cao hơn. Các điều kiện có key khác nhau được AND với nhau. [[src:ad-logcat]]''',
         '''level: takes that level and every higher one. Terms with different keys are AND\'d together. [[src:ad-logcat]]'''),
        ('find.s4', '''Cùng key thì OR, khác key thì AND: "tag:foo tag:bar package:myapp" nghĩa là (tag:foo hoặc tag:bar) và package:myapp. Cũng có thể viết rõ bằng &, | và ngoặc. [[src:ad-logcat]]''',
         '''Same key is OR, different keys are AND: "tag:foo tag:bar package:myapp" means (tag:foo or tag:bar) and package:myapp. You can also write it out with &, | and parentheses. [[src:ad-logcat]]'''),
        ('release.s1', '''Đọc nội dung log như người lạ đọc nó: số điện thoại, email, token, mã thẻ đều là dữ liệu cá nhân. Ở đây hai dòng in nguyên số điện thoại của bệnh nhân.''',
         '''Read the log content as a stranger would: phone numbers, emails, tokens and card numbers are all personal data. Here two lines print the patient\'s full phone number.'''),
        ('release.s2', '''Trang hướng dẫn bảo mật của Android gợi ý dùng R8 để xóa mọi mức log trừ warning và error trong bản không phải debug. [[src:ad-log-disclosure]]''',
         '''Android\'s security guidance suggests using R8 to remove every log level except warning and error in non-debug builds. [[src:ad-log-disclosure]]'''),
        ('release.s3', '''Đừng log dữ liệu nhạy cảm như thông tin đăng nhập hay thông tin định danh cá nhân; khi có thể, chỉ log hằng số biết lúc biên dịch. [[src:ad-log-disclosure]]''',
         '''Do not log sensitive data such as credentials or personally identifiable information; where possible, log only compile-time constants. [[src:ad-log-disclosure]]'''),
        ('release.s4', '''Từ Android 4.1 (API 16), app khác chỉ đọc được logcat nếu có quyền READ_LOGS, nhưng log vẫn đi vào bug report và vẫn đọc được qua adb trên máy đã bật gỡ lỗi. [[src:ad-log-disclosure]]''',
         '''Since Android 4.1 (API 16), other apps can read logcat only with the READ_LOGS permission, but logs still go into bug reports and can still be read over adb on a device with debugging enabled. [[src:ad-log-disclosure]]'''),
    ]:
        m('co.' + k, vi, en)

    z = lambda k, vi, en=None: a('vz.' + k, vi, en)
    z('tab.logcat', '''Bảng log và truy vấn''', '''Log table and query''')
    z('lc.query', '''Truy vấn: {q}''', '''Query: {q}'''); z('lc.none', '''(không lọc)''', '''(no filter)''')
    z('lc.build.debug', '''Bản build: debug''', '''Build: debug'''); z('lc.build.release', '''Bản build: release, R8 xóa Log.v, Log.d, Log.i''', '''Build: release, R8 removes Log.v, Log.d, Log.i''')
    z('lc.count', '''Còn {n} trên 16 dòng; {p} dòng lộ số điện thoại.''', '''{n} of 16 lines shown; {p} leak a phone number.''')
    for k, vi, en in [('pid', 'PID', 'PID'), ('lvl', 'Mức', 'Level'), ('tag', 'Tag', 'Tag'), ('msg', 'Nội dung', 'Message')]:
        z('lc.col.' + k, vi, en)
    z('lc.removed', '''(R8 đã xóa lời gọi này)''', '''(R8 removed this call)''')
    z('lc.legend', '''Hàng mờ: bị lọc đi, hay đã bị R8 xóa. Hàng đỏ: dòng lỗi cần tìm, hay dòng lộ dữ liệu người dùng. PID 4120 là app Hẹn Khám.''',
      '''Faded rows: filtered out, or removed by R8. Red rows: the error line to find, or a line leaking user data. PID 4120 is ClinicBook.''')

    C = 'l3'
    a(C + '.title', '''Logcat''', '''Logcat''')
    a(C + '.essence', '''Logcat là nơi xem log của cả thiết bị: hệ thống, các app khác và app của bạn, hàng nghìn dòng mỗi giây. Muốn thấy dòng cần tìm thì phải lọc.\nMỗi dòng có mức (VERBOSE, DEBUG, INFO, WARN, ERROR, ASSERT), tag, package và tiến trình. Truy vấn Logcat lọc theo các key đó: cùng key thì OR, khác key thì AND, level: là mức đó trở lên.\nLog còn là chỗ dữ liệu người dùng hay bị lộ. Trong bản release, R8 (công cụ thu gọn và tối ưu mã lúc build) có thể xóa các lời gọi Log mức thấp, nhưng cách chắc nhất là đừng bao giờ log số điện thoại, mật khẩu hay token (chuỗi chứng minh người dùng đã đăng nhập); chỉ log id và hằng số.''',
      '''Logcat is where you see the logs of the whole device: the system, other apps and your app, thousands of lines a second. To see the line you need, you have to filter.\nEach line has a level (VERBOSE, DEBUG, INFO, WARN, ERROR, ASSERT), a tag, a package and a process. A Logcat query filters on those keys: the same key is OR\'d, different keys are AND\'d, and level: means that level or higher.\nLogs are also where user data often leaks. In a release build, R8 (the tool that shrinks and optimises code at build time) can remove low-level Log calls, but the surest way is never to log phone numbers, passwords or tokens (strings proving the user is signed in); log ids and constants only.''')
    a(C + '.goal.g1', '''Đã lọc còn dòng lỗi''', '''Filtered down to the error line''')
    a(C + '.goal.g2', '''Đã thấy log nào còn trong bản release''', '''Saw which logs remain in the release build''')
    a(C + '.sim.debugging.logcat', '''lọc log, và log còn lại trong bản release''', '''filtering logs, and the logs left in a release build''')

    S_ = 'hook'
    a(C + '.sec.%s.title' % S_, '''Đoán trước khi đọc''', '''Predict before reading''')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'predict', '''Bản release bật quy tắc R8 xóa mọi lời gọi Log.v, Log.d, Log.i. App có một Log.d và một Log.w cùng in số điện thoại của bệnh nhân. Sau khi build release, còn bao nhiêu dòng log lộ số điện thoại?''',
      '''The release build has an R8 rule removing every Log.v, Log.d and Log.i call. The app has one Log.d and one Log.w, both printing the patient\'s phone number. After the release build, how many log lines still leak the phone number?''')
    B(C, S_, 1, 'ans', '''Một: dòng Log.w vẫn còn, vì R8 chỉ xóa đúng các mức được liệt kê. Xóa log theo mức là lưới an toàn, không thay được việc đừng log dữ liệu người dùng. Mô phỏng ngay dưới cho thấy cả hai việc: lọc để tìm lỗi, và log nào còn trong bản release.''',
      '''One: the Log.w line is still there, because R8 removes only the levels listed. Removing logs by level is a safety net, not a substitute for not logging user data. The simulation just below shows both jobs: filtering to find a bug, and which logs remain in a release build.''')

    S_ = 'levels'
    a(C + '.sec.%s.title' % S_, '''Mức log và lớp Log''', '''Log levels and the Log class''')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'p', '''Lớp android.util.Log có các hàm v, d, i, w, e theo mức từ thấp tới cao: VERBOSE, DEBUG, INFO, WARN, ERROR; trên cùng là ASSERT. Mỗi hàm nhận một tag (chuỗi ngắn cho biết log đến từ đâu, thường là tên lớp) và nội dung, có bản nhận thêm Throwable để in stack trace kèm theo. Log.wtf ("what a terrible failure") dành cho điều không bao giờ được xảy ra: nó luôn ghi ở mức ASSERT kèm stack trace, và có thể làm tiến trình dừng. [[src:ad-log]]''',
      '''The android.util.Log class has the functions v, d, i, w and e, by level from low to high: VERBOSE, DEBUG, INFO, WARN, ERROR; ASSERT is at the top. Each takes a tag (a short string saying where the log comes from, usually the class name) and a message, with overloads taking a Throwable to print its stack trace too. Log.wtf ("what a terrible failure") is for things that must never happen: it always logs at ASSERT level with the call stack, and may end the process. [[src:ad-log]]''')
    B(C, S_, 2, 'p', '''Log.isLoggable(tag, level) cho biết một mức có được in cho tag đó không; mặc định mọi tag ở mức INFO, và có thể đổi bằng setprop log.tag.<TAG> <LEVEL> qua adb shell. Tạo chuỗi log tốn cấp phát bộ nhớ ngay cả khi dòng đó bị lọc đi, nên bọc log tốn kém trong if (Log.isLoggable(...)). Từ API 26 không còn giới hạn độ dài tag đáng lo; trước đó, tag dài quá 23 ký tự làm isLoggable ném lỗi. [[src:ad-log]]''',
      '''Log.isLoggable(tag, level) tells you whether a level is printed for that tag; by default every tag is at INFO, which you can change with setprop log.tag.<TAG> <LEVEL> through adb shell. Building a log string costs allocations even when the line is filtered out, so wrap expensive logs in if (Log.isLoggable(...)). From API 26 there is no tag length limit to worry about; before that, a tag over 23 characters made isLoggable throw. [[src:ad-log]]''')
    B(C, S_, 3, 'note', '''Chọn mức theo người đọc: ERROR cho thứ cần sửa, WARN cho thứ lạ nhưng app tự xử được, INFO cho mốc quan trọng, DEBUG và VERBOSE cho chi tiết chỉ cần khi đang gỡ lỗi. Log quá nhiều ở mức cao làm chính bộ lọc theo mức mất tác dụng.''',
      '''Choose the level for the reader: ERROR for something to fix, WARN for something odd the app handled, INFO for important milestones, DEBUG and VERBOSE for detail needed only while debugging. Logging too much at high levels makes filtering by level useless.''')

    S_ = 'filter'
    a(C + '.sec.%s.title' % S_, '''Truy vấn lọc của Logcat''', '''Logcat filter queries''')
    a(C + '.sec.%s.badge' % S_, 'version')
    B(C, S_, 1, 'p', '''Cửa sổ Logcat của Android Studio lọc bằng truy vấn dạng key:value. Các key chính: tag, package, process, message, level, age. package:mine là mọi package trong project đang mở; level:WARN là WARN trở lên; age:5m là log trong 5 phút gần nhất (tính theo đồng hồ máy tính, không phải của thiết bị); is:crash lấy các crash, is:stacktrace lấy các dòng trông như stack trace. [[src:ad-logcat]]''',
      '''Android Studio\'s Logcat window filters with key:value queries. The main keys: tag, package, process, message, level, age. package:mine is every package in the open project; level:WARN is WARN and above; age:5m is the last 5 minutes of logs (by the computer\'s clock, not the device\'s); is:crash takes crashes, is:stacktrace takes lines that look like stack traces. [[src:ad-logcat]]''')
    B(C, S_, 2, 'p', '''Dấu trừ phía trước để loại: -tag:Choreographer bỏ một tag ồn ào. Dấu ~ sau key để dùng biểu thức chính quy: tag~:Booking.* lấy mọi tag bắt đầu bằng Booking. Nhiều điều kiện cùng key được OR, khác key được AND; muốn rõ ràng thì viết &, | và ngoặc, với & ưu tiên hơn |. [[src:ad-logcat]]''',
      '''A leading minus excludes: -tag:Choreographer drops a noisy tag. A ~ after the key uses a regular expression: tag~:Booking.* takes every tag starting with Booking. Several terms with the same key are OR\'d, different keys AND\'d; to be explicit, write &, | and parentheses, with & binding tighter than |. [[src:ad-logcat]]''')
    B(C, S_, 3, 'kt', '''package:mine level:WARN                       // lỗi và cảnh báo của app
package:mine tag:BookingRepo tag:Sync         // (BookingRepo hoặc Sync) và của app
package:mine -tag:Choreographer               // bỏ một tag ồn ào
package:mine is:crash age:10m                 // crash trong 10 phút gần nhất''',
      '''package:mine level:WARN                       // the app\'s errors and warnings
package:mine tag:BookingRepo tag:Sync         // (BookingRepo or Sync) and from the app
package:mine -tag:Choreographer               // drop a noisy tag
package:mine is:crash age:10m                 // crashes in the last 10 minutes''')
    B(C, S_, 4, 'note', '''Khi app khởi động lại, Logcat ghi dòng PROCESS ENDED rồi PROCESS STARTED, và tiến trình mới có PID khác; lọc theo package thay vì theo PID thì không mất dấu qua lần khởi động lại. [[src:ad-logcat]]''',
      '''When the app restarts, Logcat writes PROCESS ENDED then PROCESS STARTED, and the new process has a different PID; filter by package rather than by PID to keep track across restarts. [[src:ad-logcat]]''')
    B(C, S_, 4, 'kind', 'mechanism')

    S_ = 'cmdline'
    a(C + '.sec.%s.title' % S_, '''adb logcat trên dòng lệnh''', '''adb logcat on the command line''')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'p', '''Log được giữ trong các buffer vòng của tiến trình hệ thống logd: đầy thì dòng cũ bị ghi đè. adb logcat đọc chúng từ máy tính, không cần Android Studio, hữu ích trên máy CI hay khi chỉ có dòng lệnh. Bộ lọc dạng tag:mức, với mức là một chữ cái V, D, I, W, E, F, S (S là im lặng); *:S làm mọi tag khác im lặng. [[src:ad-logcat-cli]]''',
      '''Logs are kept in ring buffers of the logd system process: when full, old lines are overwritten. adb logcat reads them from your computer, no Android Studio needed, useful on CI machines or when you only have a command line. Filters take the form tag:level, with the level a letter V, D, I, W, E, F, S (S is silent); *:S silences every other tag. [[src:ad-logcat-cli]]''')
    B(C, S_, 2, 'kt', '''adb logcat BookingRepo:D Sync:W *:S     # BookingRepo từ DEBUG, Sync từ WARN, còn lại im
adb logcat *:W                            # mọi tag, từ WARN trở lên
adb logcat -v threadtime                  # định dạng mặc định: ngày, giờ, PID, TID, mức, tag
adb logcat -b crash                       # chỉ buffer crash''',
      '''adb logcat BookingRepo:D Sync:W *:S     # BookingRepo from DEBUG, Sync from WARN, the rest silent
adb logcat *:W                            # every tag, WARN and above
adb logcat -v threadtime                  # the default format: date, time, PID, TID, level, tag
adb logcat -b crash                       # only the crash buffer''')
    B(C, S_, 3, 'p', '''Một dòng log có thể bị chặn ở bốn tầng: lúc biên dịch (R8 xóa lời gọi), theo thuộc tính hệ thống của tag, theo mức mặc định của app (INFO), và lúc hiển thị (bộ lọc của adb logcat hay Logcat). Khi một dòng "không hiện", hãy hỏi nó bị chặn ở tầng nào. [[src:ad-logcat-cli]]''',
      '''A log line can be stopped at four stages: at compile time (R8 removes the call), by the tag\'s system property, by the app\'s default level (INFO), and at display time (the adb logcat or Logcat filter). When a line "does not show", ask which stage stopped it. [[src:ad-logcat-cli]]''')

    S_ = 'release'
    a(C + '.sec.%s.title' % S_, '''Log trong bản release và dữ liệu nhạy cảm''', '''Logs in release builds and sensitive data''')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'p', '''In thông tin đăng nhập hay thông tin định danh cá nhân (số điện thoại, email, mã thẻ) ra log là một lỗ hổng có tên: lộ thông tin qua log. Từ API 16, app khác cần quyền READ_LOGS mới đọc được log, nhưng log vẫn vào bug report, vẫn đọc được qua adb, và vẫn có thể bị gửi đi cùng báo cáo lỗi. [[src:ad-log-disclosure]]''',
      '''Printing credentials or personally identifiable information (phone numbers, emails, card numbers) to the log is a named weakness: log information disclosure. Since API 16, other apps need the READ_LOGS permission to read logs, but logs still go into bug reports, can still be read over adb, and can still be sent along with error reports. [[src:ad-log-disclosure]]''')
    B(C, S_, 2, 'kt', '''# proguard-rules.pro: R8 coi các lời gọi này là không có tác dụng và xóa chúng khỏi bản release
-assumenosideeffects class android.util.Log {
    public static boolean isLoggable(java.lang.String, int);
    public static int v(...);
    public static int d(...);
    public static int i(...);
}''', '''# proguard-rules.pro: R8 treats these calls as having no effect and removes them from the release build
-assumenosideeffects class android.util.Log {
    public static boolean isLoggable(java.lang.String, int);
    public static int v(...);
    public static int d(...);
    public static int i(...);
}''')
    B(C, S_, 3, 'p', '''Quy tắc trên giữ lại w và e, đúng như hướng dẫn: xóa mọi mức trừ warning và error. Nhưng nó chỉ là lưới an toàn. Quy tắc chính: đừng log dữ liệu nhạy cảm; khi có thể, chỉ log hằng số biết lúc biên dịch, và thay dữ liệu người dùng bằng id hay bằng bản đã che. Cách R8 hoạt động được nói ở chương "R8 và stack trace bị làm rối". [[src:ad-log-disclosure]]''',
      '''The rule above keeps w and e, just as the guidance says: remove every level except warning and error. But it is only a safety net. The main rule: do not log sensitive data; where possible, log only compile-time constants, and replace user data with ids or masked values. How R8 works is covered in the chapter "R8 and obfuscated stack traces". [[src:ad-log-disclosure]]''')

    S_ = 'bugs'
    a(C + '.sec.%s.title' % S_, '''Hai lỗi hay gặp''', '''Two common bugs''')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'bug', '''Lọc theo PID của app, khởi động lại app, rồi Logcat trống trơn đúng lúc crash xảy ra.''', '''Filtering by the app\'s PID, restarting the app, then Logcat is empty exactly when the crash happens.''')
    B(C, S_, 1, 'cause', '''Mỗi lần khởi động, tiến trình có PID mới; bộ lọc vẫn trỏ vào PID cũ.''', '''Each start gives the process a new PID; the filter still points at the old one.''')
    B(C, S_, 1, 'fix', '''Lọc theo package (package:mine) thay vì PID.''', '''Filter by package (package:mine) instead of PID.''')
    B(C, S_, 2, 'bug', '''Báo cáo lỗi gửi về máy chủ có kèm token đăng nhập của người dùng.''', '''Error reports sent to the server contain users\' login tokens.''')
    B(C, S_, 2, 'cause', '''Một Log.w("Auth", "refresh failed token=$token") trong bản release; báo cáo lỗi gom log gần nhất.''', '''A Log.w("Auth", "refresh failed token=$token") in the release build; the error report gathers recent logs.''')
    B(C, S_, 2, 'fix', '''Không log token; log mã lỗi và id phiên đã che. Rà mọi lời gọi Log mức w, e vì R8 không xóa chúng.''', '''Never log the token; log the error code and a masked session id. Review every Log call at w and e levels, because R8 does not remove them.''')

    S_ = 'ex'
    a(C + '.sec.%s.title' % S_, '''Bài tập''', '''Exercise''')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'ex', '''Viết truy vấn Logcat cho từng câu hỏi: (a) mọi lỗi và cảnh báo của app trong 10 phút gần nhất; (b) log của tag Sync hoặc tag Payment, ở mọi mức, chỉ của app; (c) như (a) nhưng bỏ tag Choreographer. Rồi cho biết: dòng Log.i("Sync", "phone=$phone") có còn trong bản release dùng quy tắc R8 ở trên không?''',
      '''Write a Logcat query for each question: (a) every error and warning from the app in the last 10 minutes; (b) logs from the Sync tag or the Payment tag, at every level, from the app only; (c) like (a) but without the Choreographer tag. Then say: is the line Log.i("Sync", "phone=$phone") still in a release build using the R8 rule above?''')
    B(C, S_, 1, 'hint', '''Cùng key thì OR, khác key thì AND; level: là mức đó trở lên; dấu trừ để loại.''', '''Same key is OR, different keys AND; level: means that level or higher; a minus excludes.''')
    B(C, S_, 1, 'sol', '''(a) package:mine level:WARN age:10m. (b) package:mine tag:Sync tag:Payment. (c) package:mine level:WARN age:10m -tag:Choreographer. Dòng Log.i bị R8 xóa vì i nằm trong quy tắc; nhưng vẫn nên sửa nó, vì bản debug và mọi bản build không bật quy tắc đó vẫn in số điện thoại.''',
      '''(a) package:mine level:WARN age:10m. (b) package:mine tag:Sync tag:Payment. (c) package:mine level:WARN age:10m -tag:Choreographer. The Log.i line is removed by R8 because i is in the rule; still fix it, because the debug build and any build without that rule still print the phone number.''')

    S_ = 'recall'
    a(C + '.sec.%s.title' % S_, '''Tự trả lời''', '''Answer it yourself''')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'ask', '''"tag:A tag:B level:ERROR" lấy những dòng nào?''', '''Which lines does "tag:A tag:B level:ERROR" keep?''')
    B(C, S_, 1, 'ans', '''Dòng có tag A hoặc B, và mức ERROR trở lên.''', '''Lines with tag A or B, and level ERROR or above.''')
    B(C, S_, 2, 'ask', '''Vì sao xóa log mức thấp bằng R8 chưa đủ để bảo vệ dữ liệu người dùng?''', '''Why is removing low-level logs with R8 not enough to protect user data?''')
    B(C, S_, 2, 'ans', '''R8 chỉ xóa đúng các mức được liệt kê; Log.w, Log.e vẫn còn và vẫn in mọi thứ bạn đưa vào. Phải không log dữ liệu nhạy cảm ngay từ đầu.''', '''R8 removes only the levels listed; Log.w and Log.e remain and still print whatever you give them. Sensitive data must not be logged in the first place.''')

    for q, qv, qe, av, ae, wv, we in [
        ('q1', 'level:INFO lấy những mức nào?', 'Which levels does level:INFO keep?', 'Bốn mức: INFO, WARN, ERROR, ASSERT.', 'Four levels: INFO, WARN, ERROR, ASSERT.', 'level: là mức đó trở lên.', 'level: means that level or higher.'),
        ('q2', 'Mức mặc định của một tag theo Log.isLoggable là gì?', 'What is a tag\'s default level according to Log.isLoggable?', 'INFO.', 'INFO.', 'Có thể đổi bằng setprop log.tag.<TAG> <LEVEL>.', 'It can be changed with setprop log.tag.<TAG> <LEVEL>.'),
        ('q3', 'Trong adb logcat, *:S nghĩa là gì?', 'In adb logcat, what does *:S mean?', 'Mọi tag không được nêu tên đều im lặng.', 'Every tag not named is silent.', 'Dùng cùng các tag:mức khác để chỉ xem đúng những tag mình cần.', 'Use it with other tag:level terms to see only the tags you need.'),
        ('q4', 'Lọc theo PID hay theo package thì không mất dấu khi app khởi động lại?', 'Filtering by PID or by package: which keeps track across an app restart?', 'Theo package.', 'By package.', 'Tiến trình mới có PID mới.', 'The new process gets a new PID.')]:
        a(C + '.quiz.%s.q' % q, qv, qe); a(C + '.quiz.%s.a' % q, av, ae); a(C + '.quiz.%s.why' % q, wv, we)
