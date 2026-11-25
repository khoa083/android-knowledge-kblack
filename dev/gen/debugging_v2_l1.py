# Gỡ lỗi và hiệu năng · l1: quy trình gỡ lỗi, adb và bug report (Phần 1: tìm ra lỗi)
# Nguồn (chỉ ghi ở đây và docs/research/debugging.md): developer.android.com/tools/adb (adb gồm client, server cổng 5037, daemon adbd;
# adb devices, install, shell, pull, push; am start, am kill), studio/debug/bug-report (bug report chứa dumpsys, dumpstate, logcat; adb bugreport
# lưu file ZIP; Play Console và Crashlytics cho crash từ người dùng), studio/debug (bản build debuggable), đọc 2026-11-25.
# Fragment nhận dữ liệu qua setter và mất nó khi bị tạo lại là ví dụ của site. Giọng văn dạy học; không dạy nút bấm của Android Studio.

SEC_ORDER = {'l1': ['hook', 'loop', 'repro', 'narrow', 'lock', 'bugs', 'ex', 'recall']}


def add(a):
    def B(ch, sec, n, field, vi, en=None):
        a('%s.sec.%s.b.%02d.%s' % (ch, sec, n, field), vi, vi if en is None else en)

    a('preset.loop', '''Gỡ lỗi · đoán và sửa, hay tái hiện rồi thu hẹp''', '''Debugging · guess and patch, or reproduce and narrow down''')
    m = lambda k, vi, en=None: a('m.loop.' + k, vi, en)
    m('title', '''Crash "thỉnh thoảng" ở màn chi tiết lịch hẹn''', '''A crash that happens "sometimes" on the booking details screen''')
    m('overview', '''Màn chi tiết lịch hẹn của app Hẹn Khám thỉnh thoảng crash. Cách 1 đoán nguyên nhân rồi sửa ngay, ba lần. Cách 2 đi theo vòng gỡ lỗi: tái hiện, thu hẹp, đặt giả thuyết và kiểm nó, sửa rồi khóa bằng test. Cả hai cách được thử trên cùng 8 kịch bản thao tác; mỗi kịch bản cho kết quả bình thường, crash, hoặc màn trống.''',
      '''The ClinicBook booking details screen crashes now and then. Way 1 guesses the cause and patches it straight away, three times. Way 2 follows the debugging loop: reproduce, narrow down, form a hypothesis and test it, fix and lock it with a test. Both are tried on the same 8 usage scenarios; each scenario ends normally, in a crash, or on a blank screen.''')
    m('wrapup', '''Đoán và sửa làm số crash giảm, nhưng lỗi vẫn còn: một lần sửa chỉ né một đường dẫn tới lỗi, lần sau giấu lỗi thành màn trống. Đi theo vòng gỡ lỗi, ta thấy cả 4 kịch bản crash đều có một điểm chung là màn hình bị tạo lại, nên sửa đúng một chỗ và có test giữ cho lỗi không quay lại.''',
      '''Guessing and patching lowers the crash count, but the bug stays: one patch only avoids one path to it, the next hides it as a blank screen. Following the debugging loop shows that all 4 crashing scenarios share one thing, the screen being recreated, so one fix in one place is enough, and a test keeps the bug from coming back.''')
    m('simp.1', '''8 kịch bản thao tác là của site; một lỗi thật có thể cần nhiều kịch bản hơn và vài lần chạy mới tái hiện được.''',
      '''The 8 usage scenarios are the site\'s; a real bug may need more scenarios and several runs before it reproduces.''')
    m('simp.2', '''Kết quả của từng kịch bản (bình thường, crash, màn trống) được tính thật bằng JavaScript từ hai điều: kịch bản có làm màn hình bị tạo lại không, và bản sửa nào đang áp dụng. Mã Kotlin chỉ để minh họa.''',
      '''Each scenario\'s result (normal, crash, blank) is really computed in JavaScript from two things: whether the scenario recreates the screen, and which patch is applied. The Kotlin code is illustrative.''')
    m('ctl.hint', '''Chọn cách gỡ lỗi rồi đi qua bốn bước; xem bảng kịch bản đổi theo từng bản sửa.''', '''Pick a way of debugging and walk the four steps; watch the scenario table change with each patch.''')
    m('ctl.case', '''Cách gỡ lỗi''', '''How the bug is handled''')
    m('ctl.case.guess', '''đoán rồi sửa ngay''', '''guess and patch at once'''); m('ctl.case.method', '''tái hiện, thu hẹp, giả thuyết, kiểm''', '''reproduce, narrow down, hypothesise, test''')
    m('diagramTitle', '''Vòng gỡ lỗi''', '''The debugging loop''')
    m('diagramDesc', '''Tái hiện, thu hẹp, giả thuyết, kiểm; sai thì quay lại; đúng thì sửa và khóa bằng test''', '''Reproduce, narrow down, hypothesise, test; back round if wrong; fix and lock with a test if right''')
    for k, vi, en in [('repro', 'Tái hiện', 'Reproduce'), ('narrow', 'Thu hẹp', 'Narrow down'), ('hypo', 'Giả thuyết', 'Hypothesis'), ('check', 'Kiểm', 'Test it'), ('lock', 'Sửa và khóa bằng test', 'Fix and lock with a test')]:
        m('n.' + k, vi, en)
    m('met.crash', '''Kịch bản crash (trên 8)''', '''Scenarios that crash (of 8)'''); m('met.blank', '''Kịch bản ra màn trống''', '''Scenarios ending blank''')
    m('met.releases', '''Bản phát hành để sửa''', '''Releases spent on fixes'''); m('met.known', '''Biết nguyên nhân''', '''Cause known''')
    m('known.no', '''chưa''', '''no'''); m('known.yes', '''đã biết''', '''yes''')
    a('cap.loop', '''Bốn trạm của vòng gỡ lỗi; giả thuyết sai thì quay lại tái hiện hay thu hẹp, đúng thì đi ra trạm cuối: sửa và khóa bằng test.''',
      '''The four stations of the debugging loop; a wrong hypothesis goes back to reproducing or narrowing down, a right one exits to the last station: fix and lock with a test.''')
    S = [
        ('guess', 's1', 'Đoán 1: lỗi do xoay màn hình, cố định màn hình dọc', 'Guess 1: rotation causes it, so lock the screen to portrait',
         'Ai đó từng thấy crash sau khi xoay máy, nên bản 1.4.1 cố định màn hình dọc. Crash giảm từ 4 xuống 3 trong 8 kịch bản: đổi giao diện tối, đổi ngôn ngữ, và quay lại app sau khi hệ thống đã đóng tiến trình vẫn crash.',
         'Someone once saw a crash after rotating the phone, so release 1.4.1 locks the screen to portrait. Crashes drop from 4 to 3 of the 8 scenarios: switching to dark theme, changing the language, and returning after the system has killed the process still crash.'),
        ('guess', 's2', 'Đoán 2: thêm một phép kiểm cho khỏi crash', 'Guess 2: add a check so it stops crashing',
         'Stack trace báo booking chưa được khởi tạo, nên bản 1.4.2 thêm if (!::booking.isInitialized) return. Không còn crash nào, nhưng 3 kịch bản kia giờ ra một màn trống: lỗi vẫn còn, chỉ không còn ồn ào.',
         'The stack trace says booking was never initialised, so release 1.4.2 adds if (!::booking.isInitialized) return. No crash is left, but those 3 scenarios now end on a blank screen: the bug is still there, it is just quiet.'),
        ('guess', 's3', 'Người dùng báo: màn chi tiết trống trơn', 'Users report: the details screen is empty',
         'Đánh giá một sao kêu "bấm vào lịch hẹn không thấy gì". Không có crash nào trong báo cáo, nên cũng không có stack trace để lần theo. Lỗi bị giấu khó tìm hơn lỗi crash.',
         'One-star reviews say "tapping a booking shows nothing". There is no crash in the reports, so there is no stack trace to follow either. A hidden bug is harder to find than a crashing one.'),
        ('guess', 's4', 'Ba bản phát hành, nguyên nhân vẫn chưa biết', 'Three releases, and the cause is still unknown',
         'Bản 1.4.3 lại đoán thêm một lần. Sau ba bản, đội vẫn không trả lời được "khi nào thì lỗi xảy ra", nên không biết lần sửa nào là đủ. Mỗi lần đoán là một lần đặt cược lên người dùng thật.',
         'Release 1.4.3 guesses once more. After three releases the team still cannot answer "when does the bug happen", so it cannot tell which fix is enough. Every guess is a bet placed on real users.'),
        ('method', 's1', 'Tái hiện: chạy cả 8 kịch bản trên máy dev', 'Reproduce: run all 8 scenarios on a dev device',
         'Thay vì đoán, thử lần lượt 8 kịch bản thao tác trên bản debug. Crash đúng 4 lần, ở các kịch bản 2, 4, 6, 7, và lần nào cũng crash. Lỗi tái hiện được đều đặn thì mới kiểm được bản sửa.',
         'Instead of guessing, try the 8 usage scenarios one by one on a debug build. It crashes exactly 4 times, in scenarios 2, 4, 6 and 7, and every time. A bug that reproduces reliably is one whose fix can be checked.'),
        ('method', 's2', 'Thu hẹp: bốn kịch bản crash có gì chung', 'Narrow down: what the four crashing scenarios share',
         'Xoay máy, đổi giao diện tối, đổi ngôn ngữ, và quay lại sau khi tiến trình bị đóng đều làm Activity và Fragment bị tạo lại. Bốn kịch bản không crash thì không. Stack trace chỉ vào cùng một dòng: đọc booking trong onViewCreated.',
         'Rotating, switching to dark theme, changing the language, and returning after the process was killed all recreate the Activity and the Fragment. The four scenarios that do not crash do not. The stack trace points at the same line every time: reading booking in onViewCreated.'),
        ('method', 's3', 'Giả thuyết và phép thử: dữ liệu chỉ được gán qua setter', 'Hypothesis and test: the data is only set through a setter',
         'Giả thuyết: màn danh sách gán booking cho Fragment qua một hàm setter; khi hệ thống tự tạo lại Fragment, không ai gọi setter nữa. Dự đoán: crash khi và chỉ khi màn hình bị tạo lại. Kết quả khớp cả 8 kịch bản, kể cả 4 kịch bản không crash.',
         'Hypothesis: the list screen hands booking to the Fragment through a setter; when the system recreates the Fragment on its own, nobody calls the setter again. Prediction: it crashes if and only if the screen is recreated. The result matches all 8 scenarios, including the 4 that do not crash.'),
        ('method', 's4', 'Sửa một chỗ, khóa bằng test', 'Fix one place, lock it with a test',
         'Truyền id lịch hẹn qua arguments của Fragment (được hệ thống lưu và trả lại khi tạo lại) và nạp booking từ id đó. Cả 8 kịch bản bình thường, không màn trống. Một test tạo lại màn hình rồi kiểm tên bệnh nhân vẫn hiện giữ cho lỗi không quay lại.',
         'Pass the booking id in the Fragment\'s arguments (saved and handed back by the system on recreation) and load booking from that id. All 8 scenarios end normally, with no blank screen. A test that recreates the screen and checks that the patient name still shows keeps the bug from coming back.'),
    ]
    for case, k, tv, te, xv, xe in S:
        sid = case + '.' + k
        m('s.%s.title' % sid, tv, te); m('s.%s.explain' % sid, xv, xe); m('ev.' + sid, tv, te)
    for k, vi, en in [
        ('try', '''Mẹo đọc: mỗi hàng của bảng là một kịch bản thao tác; cột cuối là kết quả với bản sửa đang áp dụng. Đếm số ô đỏ (crash) và ô vàng (màn trống) sau mỗi bước.''',
         '''Reading tip: each table row is a usage scenario; the last column is the result with the current patch. Count the red cells (crash) and the amber cells (blank screen) after each step.'''),
        ('guess.s2', '''Một bản sửa làm biến mất triệu chứng chưa chắc đã sửa nguyên nhân. Ở đây phép kiểm chỉ đổi crash thành màn trống.''',
         '''A patch that removes the symptom has not necessarily fixed the cause. Here the check only turns a crash into a blank screen.'''),
        ('guess.s3', '''Crash có stack trace và được Play Console hay Crashlytics thu lại; màn trống thì không. Giấu lỗi làm mất chính dấu vết cần để tìm nó. [[src:ad-bug-report]]''',
         '''A crash has a stack trace and is collected by Play Console or Crashlytics; a blank screen is not. Hiding the bug removes the very trail needed to find it. [[src:ad-bug-report]]'''),
        ('guess.s4', '''Câu hỏi cần trả lời trước khi sửa: "khi nào thì lỗi xảy ra, khi nào thì không". Chưa trả lời được thì chưa biết bản sửa có đủ không.''',
         '''The question to answer before fixing: "when does the bug happen, and when does it not". Until that is answered, nobody knows whether a fix is enough.'''),
        ('method.s1', '''Kịch bản 6 dùng adb để giả việc hệ thống đóng tiến trình: đưa app xuống nền, chạy adb shell am kill với tên gói, rồi mở lại app. am kill chỉ đóng tiến trình đang ở trạng thái đóng được an toàn, như app đang ở nền. [[src:ad-adb]]''',
         '''Scenario 6 uses adb to imitate the system killing the process: send the app to the background, run adb shell am kill with the package name, then reopen the app. am kill only kills a process that is safe to kill, such as an app in the background. [[src:ad-adb]]'''),
        ('method.s2', '''So kịch bản crash với kịch bản không crash quan trọng không kém: điểm chung chỉ có ý nghĩa khi nó vắng mặt ở nhóm còn lại.''',
         '''Comparing the crashing scenarios with the ones that do not crash matters just as much: a shared trait only means something if it is absent from the other group.'''),
        ('method.s3', '''Một giả thuyết tốt đưa ra dự đoán kiểm được, kể cả dự đoán "ở đây sẽ không crash". Nếu một kịch bản không khớp, giả thuyết sai, và ta quay lại vòng.''',
         '''A good hypothesis makes a testable prediction, including "this one will not crash". If one scenario does not match, the hypothesis is wrong and we go round the loop again.'''),
        ('method.s4', '''Test trước khi sửa phải đỏ và sau khi sửa phải xanh; như vậy mới chắc nó kiểm đúng lỗi này. Cách tái hiện lỗi bằng test và chia đôi lịch sử commit được nói kỹ ở chương "Gỡ lỗi có phương pháp: tái hiện và chia đôi" của track Mã sạch và kỷ luật làm nghề.''',
         '''The test must be red before the fix and green after it; only then is it sure to check this bug. Reproducing bugs as tests and bisecting the commit history are covered in "Methodical debugging: reproduce and bisect" in the Clean Code and Craft track.'''),
    ]:
        m('co.' + k, vi, en)

    z = lambda k, vi, en=None: a('vz.' + k, vi, en)
    z('tab.loop', '''Vòng gỡ lỗi và bảng kịch bản''', '''Debugging loop and scenario table''')
    z('loop.aria', '''Vòng gỡ lỗi bốn trạm; {c} trên 8 kịch bản crash, {b} ra màn trống''', '''A four-station debugging loop; {c} of 8 scenarios crash, {b} end blank''')
    z('loop.cap.guess', '''Cách 1: đoán, sửa, phát hành; đường tắt bỏ qua cả vòng.''', '''Way 1: guess, patch, release; a shortcut that skips the loop.''')
    z('loop.cap.method', '''Cách 2: đi đủ vòng tái hiện, thu hẹp, giả thuyết, kiểm.''', '''Way 2: go round the loop: reproduce, narrow down, hypothesise, test.''')
    z('loop.guess', '''Đoán rồi sửa''', '''Guess and patch''')
    z('loop.patch', '''Bản sửa đang áp dụng: {p}''', '''Patch applied: {p}''')
    for k, vi, en in [('none', 'chưa có', 'none'), ('portrait', 'cố định màn hình dọc', 'portrait lock'), ('check', 'cố định dọc và phép kiểm isInitialized', 'portrait lock and an isInitialized check'),
                      ('args', 'truyền id qua arguments', 'id passed in arguments')]:
        z('loop.p.' + k, vi, en)
    z('loop.col.n', '''#''', '''#'''); z('loop.col.sc', '''Kịch bản thao tác''', '''Usage scenario'''); z('loop.col.re', '''Tạo lại màn hình?''', '''Screen recreated?'''); z('loop.col.out', '''Kết quả''', '''Result''')
    for k, vi, en in [('openBack', 'mở chi tiết, bấm quay lại', 'open details, press back'), ('rotate', 'mở chi tiết, xoay máy', 'open details, rotate the phone'),
                      ('scroll', 'mở chi tiết, cuộn xuống', 'open details, scroll down'), ('dark', 'mở chi tiết, bật giao diện tối', 'open details, switch to dark theme'),
                      ('home', 'mở chi tiết, về màn chính, mở lại app', 'open details, go home, reopen the app'), ('kill', 'như trên, nhưng chạy adb shell am kill trước khi mở lại', 'as above, but run adb shell am kill before reopening'),
                      ('lang', 'mở chi tiết, đổi ngôn ngữ máy', 'open details, change the device language'), ('wait', 'mở chi tiết, để yên 10 phút', 'open details, leave it for 10 minutes')]:
        z('loop.sc.' + k, vi, en)
    for k, vi, en in [('guess.0', 'Bản 1.4.1 đã phát hành; chưa ai biết khi nào lỗi xảy ra.', 'Release 1.4.1 is out; nobody knows yet when the bug happens.'),
                      ('guess.1', 'Bản 1.4.2 đã phát hành: hết crash trong báo cáo.', 'Release 1.4.2 is out: no crashes in the reports.'),
                      ('guess.2', 'Người dùng báo màn trống ở các hàng vàng; không có stack trace nào.', 'Users report a blank screen in the amber rows; there is no stack trace.'),
                      ('guess.3', 'Bản 1.4.3: lần đoán thứ ba, nguyên nhân vẫn chưa biết.', 'Release 1.4.3: the third guess, the cause still unknown.'),
                      ('method.0', 'Chưa sửa gì: chỉ chạy đủ 8 kịch bản trên bản debug.', 'Nothing fixed yet: just run all 8 scenarios on a debug build.'),
                      ('method.1', 'So hàng đỏ với hàng không đỏ: cột "tạo lại màn hình" khớp từng hàng.', 'Compare the red rows with the rest: the "recreated" column matches row by row.'),
                      ('method.2', 'Giả thuyết dự đoán đúng cả 8 hàng, kể cả 4 hàng không crash.', 'The hypothesis predicts all 8 rows correctly, including the 4 that do not crash.'),
                      ('method.3', 'Một bản phát hành, có test tạo lại màn hình giữ cho lỗi không quay lại.', 'One release, with a recreation test keeping the bug from coming back.')]:
        z('loop.rel.' + k, vi, en)
    z('loop.re.yes', '''có''', '''yes'''); z('loop.re.no', '''không''', '''no'''); z('loop.re.hidden', '''không (đã cố định dọc)''', '''no (portrait locked)''')
    z('loop.out.ok', '''bình thường''', '''normal'''); z('loop.out.crash', '''crash''', '''crash'''); z('loop.out.blank', '''màn trống''', '''blank screen''')
    z('loop.legend', '''Đỏ: crash. Vàng: màn trống, lỗi bị giấu. Trạm đang đứng có viền; ở cách 1, đường tắt "đoán rồi sửa" không đi qua trạm nào.''',
      '''Red: crash. Amber: blank screen, the bug hidden. The current station is outlined; in way 1 the "guess and patch" shortcut passes no station.''')

    C = 'l1'
    a(C + '.title', '''Quy trình gỡ lỗi, adb và bug report''', '''The debugging process, adb and bug reports''')
    a(C + '.essence', '''Sửa theo đoán thường chỉ né một đường dẫn tới lỗi hoặc giấu nó đi, nên lỗi quay lại.\nGỡ lỗi có phương pháp là một vòng: tái hiện lỗi đều đặn; thu hẹp bằng cách so lúc lỗi xảy ra với lúc không; đặt một giả thuyết có dự đoán kiểm được; kiểm nó. Sai thì quay lại vòng; đúng thì sửa, rồi khóa bằng một test đỏ trước khi sửa và xanh sau khi sửa.\nadb (Android Debug Bridge, công cụ dòng lệnh) cho bạn điều khiển thiết bị từ máy tính để tái hiện (cài app, chạy lệnh, giả việc hệ thống đóng tiến trình); bug report gom log, stack trace và trạng thái hệ thống khi lỗi xảy ra trên máy khác.''',
      '''Fixing by guesswork usually only avoids one path to the bug or hides it, so the bug comes back.\nMethodical debugging is a loop: reproduce the bug reliably; narrow it down by comparing when it happens with when it does not; form a hypothesis with a testable prediction; test it. If it is wrong, go round again; if it is right, fix it, then lock it with a test that is red before the fix and green after.\nadb (Android Debug Bridge, a command-line tool) lets you drive a device from your computer to reproduce the bug (install the app, run commands, imitate the system killing the process); a bug report gathers the logs, stack traces and system state when the bug happens on someone else\'s device.''')
    a(C + '.goal.g1', '''Đã thấy kịch bản crash có điểm chung''', '''Saw what the crashing scenarios share''')
    a(C + '.goal.g2', '''Đã thấy bản sửa được khóa bằng test''', '''Saw the fix locked with a test''')
    a(C + '.sim.debugging.loop', '''đoán và sửa, hay đi đủ vòng gỡ lỗi''', '''guess and patch, or the full debugging loop''')

    S_ = 'hook'
    a(C + '.sec.%s.title' % S_, '''Đoán trước khi đọc''', '''Predict before reading''')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'predict', '''Màn chi tiết crash "thỉnh thoảng". Đội cố định màn hình dọc vì có người thấy crash sau khi xoay máy. Trong 8 kịch bản thao tác ở mô phỏng dưới, bạn đoán còn bao nhiêu kịch bản crash sau bản sửa đó?''',
      '''The details screen crashes "sometimes". The team locks the screen to portrait because someone saw a crash after rotating. Of the 8 usage scenarios in the simulation below, how many do you guess still crash after that fix?''')
    B(C, S_, 1, 'ans', '''Ba, giảm từ bốn. Xoay máy chỉ là một trong bốn cách làm màn hình bị tạo lại; đổi giao diện tối, đổi ngôn ngữ và quay lại sau khi tiến trình bị đóng vẫn crash. Bản sửa né một đường dẫn tới lỗi, không sửa nguyên nhân.''',
      '''Three, down from four. Rotating is only one of four ways the screen gets recreated; switching to dark theme, changing the language and returning after the process was killed still crash. The fix avoids one path to the bug without fixing the cause.''')

    S_ = 'loop'
    a(C + '.sec.%s.title' % S_, '''Vòng gỡ lỗi''', '''The debugging loop''')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'p', '''Gỡ lỗi là trả lời câu hỏi "khi nào thì lỗi xảy ra, khi nào thì không" rồi mới sửa. Vòng gồm bốn trạm. Tái hiện: tìm các bước làm lỗi xảy ra mỗi lần. Thu hẹp: so lúc lỗi xảy ra với lúc không để khoanh vùng nguyên nhân. Giả thuyết: nói rõ bạn nghĩ nguyên nhân là gì, và vì thế lỗi sẽ xảy ra ở đâu, không xảy ra ở đâu. Kiểm: chạy thử đúng các dự đoán đó.''',
      '''Debugging means answering "when does the bug happen, and when does it not" before fixing anything. The loop has four stations. Reproduce: find steps that make the bug happen every time. Narrow down: compare when it happens with when it does not, to fence in the cause. Hypothesis: say clearly what you think the cause is, and therefore where the bug will and will not happen. Test it: run exactly those predictions.''')
    B(C, S_, 2, 'p', '''Giả thuyết sai thì quay lại tái hiện hay thu hẹp, với hiểu biết mới. Giả thuyết đúng thì mới sửa, và sửa đúng một chỗ mà giả thuyết chỉ ra. Bước cuối là khóa: một test tái hiện lỗi, đỏ trước khi sửa và xanh sau khi sửa, để lỗi không lặng lẽ quay lại ở bản sau.''',
      '''A wrong hypothesis sends you back to reproducing or narrowing down, with what you have learned. Only a right hypothesis leads to a fix, made in the one place it points to. The last step is locking: a test that reproduces the bug, red before the fix and green after, so the bug does not quietly return in a later release.''')
    B(C, S_, 3, 'note', '''Đoán không bị cấm: một giả thuyết cũng là một lời đoán. Khác biệt là giả thuyết được kiểm trước khi sửa, còn bản sửa theo đoán được "kiểm" bằng người dùng thật sau khi phát hành.''',
      '''Guessing is not forbidden: a hypothesis is a guess too. The difference is that a hypothesis is tested before the fix, while a guessed fix is "tested" on real users after release.''')
    B(C, S_, 3, 'kind', 'mechanism')

    S_ = 'repro'
    a(C + '.sec.%s.title' % S_, '''Tái hiện: adb và bug report''', '''Reproducing: adb and bug reports''')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'p', '''adb (Android Debug Bridge) là công cụ dòng lệnh để điều khiển thiết bị từ máy tính. Nó gồm ba phần: client chạy trên máy tính khi bạn gõ lệnh, một server trên máy tính (lắng nghe ở cổng TCP 5037), và daemon adbd chạy trên thiết bị. Thiết bị thật cần bật USB debugging trong tùy chọn nhà phát triển; từ Android 11 có thể kết nối không dây. [[src:ad-adb]]''',
      '''adb (Android Debug Bridge) is a command-line tool for driving a device from your computer. It has three parts: the client that runs on your computer when you type a command, a server on your computer (listening on TCP port 5037), and the adbd daemon running on the device. A real device needs USB debugging enabled in the developer options; from Android 11 it can also connect wirelessly. [[src:ad-adb]]''')
    B(C, S_, 2, 'kt', '''adb devices                         # thiết bị nào đang kết nối, trạng thái device / offline
adb install app-debug.apk           # cài bản debug
adb shell am start -n vn.henkham/.MainActivity   # mở một Activity
adb shell am kill vn.henkham        # đóng tiến trình đang ở nền, như hệ thống làm khi thiếu bộ nhớ
adb pull /sdcard/log.txt .          # chép file từ thiết bị về máy tính
adb bugreport                       # gom một bug report thành file ZIP''',
      '''adb devices                         # which devices are connected, state device / offline
adb install app-debug.apk           # install the debug build
adb shell am start -n vn.henkham/.MainActivity   # open an Activity
adb shell am kill vn.henkham        # kill the process while it is in the background, as the system does when memory is short
adb pull /sdcard/log.txt .          # copy a file from the device to the computer
adb bugreport                       # gather a bug report into a ZIP file''')
    B(C, S_, 3, 'p', '''Lỗi xảy ra trên máy người khác thì cần dấu vết từ máy đó. Bug report là một file ZIP chứa log hệ thống (logcat), log lỗi (dumpstate) và trạng thái các dịch vụ hệ thống (dumpsys), kèm stack trace. Có thể lấy nó bằng adb bugreport, hay ngay trên máy bằng mục "Take bug report" trong tùy chọn nhà phát triển. Với crash và ANR (app không phản hồi đủ lâu, hệ thống hỏi người dùng có đóng app không) của người dùng thật, Play Console và Firebase Crashlytics thu stack trace cho bạn. [[src:ad-bug-report]]''',
      '''A bug on someone else\'s device needs evidence from that device. A bug report is a ZIP file holding the system log (logcat), error logs (dumpstate) and the state of system services (dumpsys), along with stack traces. You can get one with adb bugreport, or on the device itself with "Take bug report" in the developer options. For crashes and ANRs (the app stays unresponsive long enough that the system offers to close it) from real users, Play Console and Firebase Crashlytics collect the stack traces for you. [[src:ad-bug-report]]''')
    B(C, S_, 4, 'note', '''Ghi lại các bước tái hiện thành một danh sách cố định, như 8 kịch bản ở mô phỏng. Danh sách đó vừa giúp thu hẹp, vừa là cách kiểm bản sửa về sau. Tái hiện trên bản debug (biến thể build có debuggable bật) để còn gắn debugger (trình gỡ lỗi, dừng app ở một dòng để xem bên trong), xem biến và tính biểu thức lúc chạy. [[src:ad-debug]]''',
      '''Write the reproduction steps down as a fixed list, like the 8 scenarios in the simulation. That list helps you narrow down, and later it is how you check the fix. Reproduce on a debug build (a build variant with debuggable on) so you can still attach the debugger (which pauses the app at a line so you can look inside), examine variables and evaluate expressions at runtime. [[src:ad-debug]]''')
    B(C, S_, 4, 'kind', 'mechanism')

    S_ = 'narrow'
    a(C + '.sec.%s.title' % S_, '''Thu hẹp và đặt giả thuyết''', '''Narrowing down and forming a hypothesis''')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'p', '''Thu hẹp là chia các trường hợp thành hai nhóm, có lỗi và không lỗi, rồi tìm thứ chỉ nhóm có lỗi mới có. Ở mô phỏng, bốn kịch bản crash đều làm màn hình bị tạo lại; bốn kịch bản kia thì không. Stack trace (chương "Đọc stack trace" giải thích cách đọc) cho thêm một manh mối: dòng nào, hàm nào.''',
      '''Narrowing down means splitting the cases into two groups, failing and passing, then looking for what only the failing group has. In the simulation, the four crashing scenarios all recreate the screen; the other four do not. The stack trace (the chapter "Reading stack traces" explains how to read one) adds another clue: which line, which function.''')
    B(C, S_, 2, 'p', '''Giả thuyết tốt thì cụ thể và có dự đoán kiểm được. "Có gì đó sai với vòng đời" chưa dùng được. "booking chỉ được gán qua setter, nên mọi lần tạo lại Fragment đều mất nó" dùng được, vì nó dự đoán đúng kịch bản nào crash và kịch bản nào không, kể cả những kịch bản chưa thử.''',
      '''A good hypothesis is specific and makes testable predictions. "Something is wrong with the lifecycle" is not usable yet. "booking is only set through a setter, so every recreation of the Fragment loses it" is usable, because it predicts exactly which scenarios crash and which do not, including ones not tried yet.''')
    B(C, S_, 3, 'kt', '''class BookingDetailFragment : Fragment() {
    private lateinit var booking: Booking
    fun show(b: Booking) { booking = b }          // chỉ màn danh sách gọi; hệ thống tạo lại Fragment thì không ai gọi
    override fun onViewCreated(view: View, saved: Bundle?) {
        binding.patient.text = booking.patientName   // tạo lại: UninitializedPropertyAccessException
    }
}''', '''class BookingDetailFragment : Fragment() {
    private lateinit var booking: Booking
    fun show(b: Booking) { booking = b }          // only the list screen calls this; nobody calls it when the system recreates the Fragment
    override fun onViewCreated(view: View, saved: Bundle?) {
        binding.patient.text = booking.patientName   // after recreation: UninitializedPropertyAccessException
    }
}''')

    S_ = 'lock'
    a(C + '.sec.%s.title' % S_, '''Sửa đúng chỗ và khóa bằng test''', '''Fixing the right place and locking it with a test''')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'p', '''Giả thuyết chỉ ra chỗ sửa: dữ liệu Fragment cần phải đi qua arguments, nơi hệ thống lưu lại và trả về khi tạo lại màn hình, chứ không qua setter. Fragment chỉ giữ id và tự nạp booking từ id đó.''',
      '''The hypothesis points to the fix: data the Fragment needs must go through its arguments, which the system saves and hands back when it recreates the screen, not through a setter. The Fragment keeps only the id and loads booking from it.''')
    B(C, S_, 2, 'kt', '''@Test fun detailsSurviveRecreation() {
    val scenario = launchFragmentInContainer<BookingDetailFragment>(bundleOf("bookingId" to 42L))
    scenario.recreate()                             // giống xoay máy hay đổi giao diện tối
    onView(withId(R.id.patient)).check(matches(withText("Nguyễn Văn An")))
}''', '''@Test fun detailsSurviveRecreation() {
    val scenario = launchFragmentInContainer<BookingDetailFragment>(bundleOf("bookingId" to 42L))
    scenario.recreate()                             // like rotating or switching to dark theme
    onView(withId(R.id.patient)).check(matches(withText("Nguyen Van An")))
}''')
    B(C, S_, 3, 'p', '''Chạy test này trên mã cũ trước: nó phải đỏ. Nếu nó xanh ngay, test không tái hiện được lỗi và chưa bảo vệ gì cả. Sau khi sửa, nó chuyển xanh, và chạy lại cả 8 kịch bản để chắc bản sửa không làm hỏng chỗ khác. Lỗi chỉ xuất hiện trong một khoảng commit thì chia đôi lịch sử để tìm commit gây ra nó, như chương "Gỡ lỗi có phương pháp: tái hiện và chia đôi" của track Mã sạch và kỷ luật làm nghề.''',
      '''Run this test on the old code first: it must be red. If it is green straight away, the test does not reproduce the bug and protects nothing. After the fix it turns green; then rerun all 8 scenarios to make sure the fix broke nothing else. When a bug appeared somewhere in a range of commits, bisect the history to find the commit that caused it, as in "Methodical debugging: reproduce and bisect" in the Clean Code and Craft track.''')

    S_ = 'bugs'
    a(C + '.sec.%s.title' % S_, '''Hai lỗi hay gặp''', '''Two common bugs''')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'bug', '''Đã "sửa" crash bằng try/catch quanh cả hàm; một tháng sau người dùng báo đặt lịch không lưu.''', '''A crash was "fixed" with a try/catch around the whole function; a month later users report that bookings are not saved.''')
    B(C, S_, 1, 'cause', '''Khối catch nuốt cả lỗi lưu dữ liệu; triệu chứng mất, nguyên nhân vẫn còn và giờ không để lại stack trace nào.''', '''The catch block also swallows the save error; the symptom is gone, the cause remains and now leaves no stack trace.''')
    B(C, S_, 1, 'fix', '''Tái hiện và tìm nguyên nhân trước; chỉ bắt đúng loại lỗi dự đoán được, và vẫn ghi lại nó.''', '''Reproduce and find the cause first; catch only the specific, expected error, and still record it.''')
    B(C, S_, 2, 'bug', '''Lỗi "không tái hiện được" trên máy dev, nên được đóng lại.''', '''The bug "cannot be reproduced" on the dev device, so it is closed.''')
    B(C, S_, 2, 'cause', '''Máy dev không bao giờ bị hệ thống đóng tiến trình, không đổi ngôn ngữ, không bật giao diện tối; các bước của người dùng chưa được thử.''', '''The dev device never has its process killed, never changes language, never switches to dark theme; the user\'s steps were never tried.''')
    B(C, S_, 2, 'fix', '''Lấy bug report hay stack trace từ Play Console để biết điều kiện; giả các điều kiện đó, như adb shell am kill để đóng tiến trình ở nền.''', '''Get a bug report or a Play Console stack trace to learn the conditions; recreate them, such as adb shell am kill to kill the process in the background.''')

    S_ = 'ex'
    a(C + '.sec.%s.title' % S_, '''Bài tập''', '''Exercise''')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'ex', '''Nút "Đặt lịch" đôi khi đặt trùng hai lịch. Kết quả thử 6 kịch bản: bấm một lần (1 lịch); bấm hai lần thật nhanh (2 lịch); bấm hai lần cách 3 giây (1 lịch, lần sau báo "đã đặt"); bấm một lần khi mạng chậm 5 giây (1 lịch); bấm hai lần thật nhanh khi mạng chậm (2 lịch); bấm một lần rồi xoay máy khi đang chờ (1 lịch). Nhóm có lỗi có điểm chung gì? Viết một giả thuyết, kèm một dự đoán cho kịch bản chưa thử: bấm ba lần thật nhanh.''',
      '''The "Book" button sometimes books twice. Results from 6 scenarios: tap once (1 booking); double-tap quickly (2); tap twice 3 seconds apart (1, the second says "already booked"); tap once on a 5-second slow network (1); double-tap quickly on a slow network (2); tap once, then rotate while waiting (1). What do the failing cases share? Write a hypothesis, with a prediction for a scenario not yet tried: tapping three times quickly.''')
    B(C, S_, 1, 'hint', '''Nhóm có lỗi là hai kịch bản bấm lần hai trước khi yêu cầu đầu tiên trả lời. Bấm cách 3 giây thì không lỗi, vì yêu cầu đầu đã xong.''',
      '''The failing group is the two scenarios where the second tap comes before the first request has answered. Tapping 3 seconds apart does not fail, because the first request has finished.''')
    B(C, S_, 1, 'sol', '''Giả thuyết: nút vẫn bấm được trong lúc yêu cầu đầu chưa trả lời, và mỗi lần bấm gửi một yêu cầu mới. Dự đoán: bấm ba lần thật nhanh ra 3 lịch. Nếu thử ra đúng 3 thì giả thuyết đứng vững; sửa bằng cách tắt nút khi đang gửi (và cho máy chủ một key chống trùng (idempotency key)), rồi viết test bấm hai lần.''',
      '''Hypothesis: the button stays enabled while the first request is pending, and every tap sends a new request. Prediction: three quick taps make 3 bookings. If trying it gives exactly 3, the hypothesis stands; fix it by disabling the button while sending (and giving the server a deduplication key), then write a double-tap test.''')

    S_ = 'recall'
    a(C + '.sec.%s.title' % S_, '''Tự trả lời''', '''Answer it yourself''')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'ask', '''Bốn trạm của vòng gỡ lỗi là gì, và khi nào thì được sửa?''', '''What are the four stations of the debugging loop, and when do you get to fix?''')
    B(C, S_, 1, 'ans', '''Tái hiện, thu hẹp, giả thuyết, kiểm. Chỉ sửa khi giả thuyết đã khớp dự đoán, cả chỗ có lỗi lẫn chỗ không; rồi khóa bằng test.''', '''Reproduce, narrow down, hypothesise, test. Fix only once the hypothesis matches its predictions, both where the bug happens and where it does not; then lock it with a test.''')
    B(C, S_, 2, 'ask', '''Vì sao bản sửa làm hết crash vẫn có thể là bản sửa sai?''', '''Why can a fix that removes every crash still be the wrong fix?''')
    B(C, S_, 2, 'ans', '''Nó có thể chỉ giấu lỗi, như phép kiểm biến crash thành màn trống; lỗi vẫn còn nhưng mất dấu vết.''', '''It may only hide the bug, like the check that turns a crash into a blank screen; the bug remains but its trail is gone.''')

    for q, qv, qe, av, ae, wv, we in [
        ('q1', 'Một test viết để khóa lỗi chạy xanh ngay trên mã chưa sửa. Điều đó nói gì?', 'A test written to lock a bug is green straight away on the unfixed code. What does that tell you?',
         'Test không tái hiện được lỗi.', 'The test does not reproduce the bug.', 'Test khóa lỗi phải đỏ trước khi sửa, xanh sau khi sửa.', 'A locking test must be red before the fix and green after it.'),
        ('q2', 'adb gồm những phần nào?', 'What parts make up adb?', 'Client, server trên máy tính, và daemon adbd trên thiết bị.', 'A client and a server on the computer, and the adbd daemon on the device.',
         'Server lắng nghe ở cổng TCP 5037 và nối client với adbd.', 'The server listens on TCP port 5037 and connects clients to adbd.'),
        ('q3', 'Bug report chứa gì?', 'What does a bug report contain?', 'Log hệ thống, log lỗi, trạng thái dịch vụ hệ thống và stack trace, trong một file ZIP.', 'System logs, error logs, the state of system services and stack traces, in a ZIP file.',
         'Lấy bằng adb bugreport hay mục "Take bug report" trên máy.', 'Get one with adb bugreport or "Take bug report" on the device.'),
        ('q4', 'Bốn kịch bản crash đều làm màn hình bị tạo lại. Còn cần kiểm gì trước khi tin giả thuyết?', 'All four crashing scenarios recreate the screen. What else must be checked before trusting the hypothesis?',
         'Rằng các kịch bản không crash đều không làm màn hình bị tạo lại.', 'That none of the non-crashing scenarios recreate the screen.', 'Điểm chung chỉ có nghĩa khi nhóm không lỗi không có nó.', 'A shared trait only means something if the passing group lacks it.')]:
        a(C + '.quiz.%s.q' % q, qv, qe); a(C + '.quiz.%s.a' % q, av, ae); a(C + '.quiz.%s.why' % q, wv, we)
