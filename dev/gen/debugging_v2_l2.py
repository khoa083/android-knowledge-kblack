# Gỡ lỗi và hiệu năng · l2: debugger: breakpoint, watch, evaluate (Phần 1: tìm ra lỗi)
# Nguồn (chỉ ghi ở đây và docs/research/debugging.md): JetBrains IntelliJ IDEA 2026.3 Help "Breakpoints" và "Examine suspended program"
# (trang ghi ngày 17/11/2026; trình gỡ lỗi của Android Studio dựa trên IntelliJ IDEA); kotlinlang.org/docs/coroutines-debugging.html (ngày 07/09/2026,
# kotlinx-coroutines 1.11.0); kotlinx-coroutines-debug README. Đọc 2026-11-25. Dạy khái niệm, không dạy vị trí nút.
# Vòng lặp tính phí 500 lịch, đơn i = 347 giảm giá 120 %, luồng đồng bộ gửi nhịp mỗi giây và hết phiên sau 10 giây là ví dụ của site.

SEC_ORDER = {'l2': ['hook', 'kinds', 'suspend', 'inspect', 'coroutines', 'bugs', 'ex', 'recall']}


def add(a):
    def B(ch, sec, n, field, vi, en=None):
        a('%s.sec.%s.b.%02d.%s' % (ch, sec, n, field), vi, vi if en is None else en)

    a('preset.bp', '''Gỡ lỗi · breakpoint thường, có điều kiện, chỉ ghi log''', '''Debugging · plain, conditional and logging breakpoints''')
    m = lambda k, vi, en=None: a('m.bp.' + k, vi, en)
    m('title', '''Tổng phí tháng sai vì một đơn trong 500''', '''The monthly fee total is wrong because of one booking in 500''')
    m('overview', '''Báo cáo tháng của app Hẹn Khám cộng phí 500 lịch hẹn trên một luồng nền, và tổng bị sai. Lỗi nằm ở một đơn duy nhất: đơn số 347 (đếm từ 0) có mức giảm giá 120 %, nên phí âm. Cùng lúc, một luồng đồng bộ gửi nhịp cho máy chủ mỗi giây; mất nhịp quá 10 giây thì máy chủ ngắt phiên. Ta thử bốn cách đặt breakpoint và đếm số lần app dừng, số lần bấm chạy tiếp, số dòng log, và phiên đồng bộ còn sống không.''',
      '''The ClinicBook monthly report adds up the fees of 500 bookings on a background thread, and the total is wrong. The bug is in a single booking: number 347 (counting from 0) has a 120% discount, so its fee is negative. Meanwhile a sync thread sends the server a heartbeat every second; after 10 seconds without one, the server ends the session. We try four ways of setting a breakpoint and count how often the app stops, how many times you press resume, how many log lines appear, and whether the sync session survives.''')
    m('wrapup', '''Breakpoint thường dừng 348 lần trước khi tới đơn lỗi. Đặt điều kiện theo triệu chứng (fee < 0) thì dừng đúng một lần, ở đúng đơn đó. Dừng mọi luồng (Suspend All) thì luồng đồng bộ cũng đứng, và xem biến 30 giây là đủ để máy chủ ngắt phiên; chỉ dừng luồng chạm breakpoint (Suspend Thread) thì luồng đồng bộ vẫn gửi nhịp. Breakpoint không dừng mà chỉ ghi log cho 500 dòng mà không phải build lại.''',
      '''A plain breakpoint stops 348 times before reaching the bad booking. A condition on the symptom (fee < 0) stops exactly once, at exactly that booking. Suspending every thread (Suspend All) freezes the sync thread too, and 30 seconds of looking at variables is enough for the server to end the session; suspending only the thread that hit the breakpoint (Suspend Thread) lets the sync thread keep sending heartbeats. A breakpoint that does not stop but only logs gives 500 lines without a rebuild.''')
    m('simp.1', '''Hai luồng, 500 lịch, nhịp mỗi giây và hạn 10 giây là của site; app thật có nhiều luồng hơn, và thời gian bạn nhìn vào biến là ước lượng.''',
      '''Two threads, 500 bookings, a heartbeat every second and a 10-second timeout are the site\'s; a real app has more threads, and the time you spend looking at variables is an estimate.''')
    m('simp.2', '''Phí từng đơn, số lần dừng, số dòng log, số nhịp bị lỡ được tính thật bằng JavaScript từ danh sách 500 lịch; mỗi lần dừng ở bước "xem biến" được tính là 30 giây. Mã Kotlin chỉ để minh họa.''',
      '''Each booking\'s fee, the number of stops, log lines and missed heartbeats are really computed in JavaScript from the list of 500 bookings; each stop at the "look at variables" step counts as 30 seconds. The Kotlin code is illustrative.''')
    m('ctl.hint', '''Chọn kiểu breakpoint rồi đi qua ba bước; xem làn luồng đồng bộ có bị đứt không.''', '''Pick a kind of breakpoint and walk the three steps; watch whether the sync thread\'s lane breaks.''')
    m('ctl.case', '''Kiểu breakpoint''', '''Kind of breakpoint''')
    for k, vi, en in [('plain', 'thường, dừng mọi luồng', 'plain, suspends all threads'), ('cond', 'điều kiện fee < 0, dừng mọi luồng', 'condition fee < 0, suspends all threads'),
                      ('thread', 'điều kiện fee < 0, chỉ dừng luồng đó', 'condition fee < 0, suspends that thread only'), ('logbp', 'không dừng, ghi log biểu thức', 'non-suspending, logs an expression')]:
        m('ctl.case.' + k, vi, en)
    m('diagramTitle', '''Luồng báo cáo, breakpoint, luồng đồng bộ''', '''Report thread, breakpoint, sync thread''')
    m('diagramDesc', '''Breakpoint dừng luồng báo cáo; tùy chính sách, luồng đồng bộ dừng theo hay chạy tiếp''', '''The breakpoint stops the report thread; depending on the policy, the sync thread stops too or keeps running''')
    for k, vi, en in [('report', 'Luồng báo cáo: vòng lặp 500 lịch', 'Report thread: the 500-booking loop'), ('bp', 'Breakpoint', 'Breakpoint'), ('vars', 'Bảng biến khi dừng', 'Variables at the stop'),
                      ('sync', 'Luồng đồng bộ: nhịp mỗi giây', 'Sync thread: a heartbeat per second'), ('server', 'Máy chủ: hết phiên sau 10 giây', 'Server: session ends after 10 seconds')]:
        m('n.' + k, vi, en)
    m('met.stops', '''Lần app dừng''', '''Times the app stops'''); m('met.resumes', '''Lần bấm chạy tiếp''', '''Resumes pressed''')
    m('met.logs', '''Dòng log''', '''Log lines'''); m('met.sync', '''Phiên đồng bộ''', '''Sync session''')
    m('sync.alive', '''còn sống''', '''alive'''); m('sync.expired', '''bị ngắt''', '''ended'''); m('sync.na', '''chưa xét''', '''not yet''')
    a('cap.bp', '''Breakpoint dừng luồng báo cáo; ô đỏ là chỗ có vấn đề: dừng quá nhiều lần, hay luồng đồng bộ bị dừng theo và mất phiên.''',
      '''The breakpoint stops the report thread; a red box marks a problem: too many stops, or the sync thread frozen too and the session lost.''')
    S = [
        ('plain', 's1', 'Breakpoint thường trong vòng lặp: dừng ở đơn 0', 'A plain breakpoint in the loop: it stops at booking 0',
         'Breakpoint đặt ở dòng cộng phí. Nó dừng ngay lần lặp đầu tiên, i = 0, phí 200.000 đ, chẳng có gì sai. Breakpoint thường dừng mỗi lần chạy qua dòng đó.',
         'The breakpoint sits on the line that adds the fee. It stops on the very first iteration, i = 0, fee 200,000 VND, nothing wrong. A plain breakpoint stops every time execution passes that line.'),
        ('plain', 's2', 'Bấm chạy tiếp 347 lần mới tới đơn lỗi', 'Resume 347 times to reach the bad booking',
         'Đơn lỗi là i = 347, nên phải dừng 348 lần và bấm chạy tiếp 347 lần. Đây chính là lý do người ta bỏ debugger, quay về thêm Log rồi build lại.',
         'The bad booking is i = 347, so the app stops 348 times and you press resume 347 times. This is exactly why people give up on the debugger and go back to adding a Log and rebuilding.'),
        ('plain', 's3', 'Xem biến 30 giây: luồng đồng bộ đứng theo, máy chủ ngắt phiên', 'Thirty seconds on the variables: the sync thread freezes too, the server ends the session',
         'Mặc định breakpoint dừng mọi luồng (Suspend All). Trong 30 giây bạn đọc bảng biến, luồng đồng bộ không gửi được nhịp nào; quá 10 giây, máy chủ ngắt phiên. Khi chạy tiếp, app gặp một lỗi thứ hai do chính việc gỡ lỗi gây ra.',
         'By default a breakpoint suspends every thread (Suspend All). During the 30 seconds you read the variables, the sync thread sends no heartbeat; after 10 seconds the server ends the session. On resuming, the app meets a second error caused by the debugging itself.'),
        ('cond', 's1', 'Điều kiện fee < 0: chạy thẳng qua các đơn bình thường', 'Condition fee < 0: run straight past the normal bookings',
         'Breakpoint có điều kiện chỉ dừng khi biểu thức là true. Không cần biết trước đơn nào lỗi: đặt điều kiện theo triệu chứng, phí âm. 347 đơn đầu chạy qua mà không dừng.',
         'A conditional breakpoint stops only when its expression is true. You do not need to know which booking is bad: put the condition on the symptom, a negative fee. The first 347 bookings run through without a stop.'),
        ('cond', 's2', 'Dừng đúng một lần, ở đơn 347: giảm giá 120 %', 'One stop, at booking 347: a 120% discount',
         'App dừng một lần duy nhất. Bảng biến cho thấy base = 200.000, discountPercent = 120, nên fee = −40.000. Nguyên nhân hiện ra ngay: mức giảm giá không được kiểm ở chỗ nhập.',
         'The app stops exactly once. The variables show base = 200,000 and discountPercent = 120, so fee = −40,000. The cause is plain: the discount was never checked where it was entered.'),
        ('cond', 's3', 'Vẫn dừng mọi luồng: xem 30 giây, phiên bị ngắt', 'Still suspending all threads: 30 seconds of looking, the session ends',
         'Chỉ dừng một lần, nhưng chính sách vẫn là Suspend All. Trong lúc bạn đọc biến, luồng đồng bộ đứng 30 giây và máy chủ ngắt phiên. Ít lần dừng chưa đủ; còn phải chọn dừng luồng nào.',
         'Only one stop, but the policy is still Suspend All. While you read the variables, the sync thread is frozen for 30 seconds and the server ends the session. Fewer stops is not enough; you also choose which threads stop.'),
        ('thread', 's1', 'Cùng điều kiện, nhưng chỉ dừng luồng chạm breakpoint', 'The same condition, but suspend only the thread that hits it',
         'Chính sách Suspend Thread: khi luồng báo cáo chạm breakpoint, chỉ luồng đó dừng. Các luồng khác chạy tiếp như không có gì xảy ra.',
         'Suspend Thread policy: when the report thread hits the breakpoint, only that thread stops. The other threads keep running as if nothing happened.'),
        ('thread', 's2', 'Dừng một lần ở đơn 347; luồng đồng bộ vẫn chạy', 'One stop at booking 347; the sync thread keeps running',
         'Bảng biến giống hệt cách trước: discountPercent = 120. Khác ở làn dưới: luồng đồng bộ vẫn gửi nhịp đều mỗi giây.',
         'The variables are exactly as before: discountPercent = 120. The difference is the lower lane: the sync thread still sends a heartbeat every second.'),
        ('thread', 's3', 'Xem 30 giây, phiên đồng bộ vẫn sống', 'Thirty seconds of looking, the sync session is still alive',
         'Không nhịp nào bị lỡ, máy chủ không ngắt phiên. Đổi lại, các luồng khác vẫn có thể đổi dữ liệu trong lúc bạn đang nhìn, nên một giá trị dùng chung có thể khác đi giữa hai lần xem.',
         'No heartbeat is missed and the server keeps the session. The trade-off: other threads can still change data while you look, so a shared value may differ between two looks.'),
        ('logbp', 's1', 'Breakpoint không dừng: ghi log "i, fee" mỗi lần chạy qua', 'A non-suspending breakpoint: log "i, fee" on every pass',
         'Bỏ chọn Suspend và bật "Evaluate and log" với biểu thức "i=$i fee=$fee". App không dừng lần nào; mỗi lần chạy qua dòng đó, debugger ghi một dòng. Không phải thêm Log vào mã.',
         'Untick Suspend and turn on "Evaluate and log" with the expression "i=$i fee=$fee". The app never stops; each pass over the line writes one line. No Log call is added to the code.'),
        ('logbp', 's2', '500 dòng log; lọc phí âm còn một dòng: i = 347', '500 log lines; filtering for a negative fee leaves one: i = 347',
         'Lọc các dòng có fee âm thì chỉ còn đúng một dòng, i = 347, fee = −40.000. Luồng đồng bộ không bị dừng lần nào.',
         'Filtering for a negative fee leaves exactly one line, i = 347, fee = −40,000. The sync thread is never stopped.'),
        ('logbp', 's3', 'Muốn xem thêm biến: sửa biểu thức, không build lại', 'Want another variable: edit the expression, no rebuild',
         'Muốn in thêm discountPercent, chỉ cần sửa biểu thức của breakpoint rồi chạy lại vòng lặp. Thêm Log.d vào mã thì mỗi lần đổi là một lần build và cài lại app, và dễ quên xóa trước khi phát hành.',
         'To print discountPercent too, just edit the breakpoint\'s expression and run the loop again. Adding Log.d to the code means a rebuild and reinstall for every change, and it is easy to forget to remove before release.'),
    ]
    for case, k, tv, te, xv, xe in S:
        sid = case + '.' + k
        m('s.%s.title' % sid, tv, te); m('s.%s.explain' % sid, xv, xe); m('ev.' + sid, tv, te)
    for k, vi, en in [
        ('try', '''Mẹo đọc: làn trên là luồng báo cáo đi qua 500 lịch, vạch đỏ là chỗ app dừng; làn dưới là luồng đồng bộ, mỗi chấm là một nhịp gửi máy chủ. Đoạn đứt đỏ ở làn dưới là lúc luồng đồng bộ bị dừng theo.''',
         '''Reading tip: the upper lane is the report thread going through 500 bookings, a red mark is where the app stops; the lower lane is the sync thread, each dot a heartbeat to the server. A red break in the lower lane is when the sync thread was frozen too.'''),
        ('plain.s2', '''Một breakpoint dừng ở mọi lần chạy qua dòng của nó. Trong vòng lặp, đó là mọi lần lặp. [[src:jb-breakpoints]]''',
         '''A breakpoint stops every time execution reaches its line. Inside a loop, that is every iteration. [[src:jb-breakpoints]]'''),
        ('plain.s3', '''Chính sách All dừng mọi luồng khi một luồng chạm breakpoint; Thread chỉ dừng luồng đó. [[src:jb-breakpoints]]''',
         '''The All policy suspends every thread when any thread hits the breakpoint; Thread suspends only that thread. [[src:jb-breakpoints]]'''),
        ('cond.s1', '''Điều kiện được tính ở mỗi lần chạm; không true thì breakpoint bị bỏ qua. Biểu thức phải hợp lệ tại dòng đặt breakpoint. [[src:jb-breakpoints]]''',
         '''The condition is evaluated on every hit; if it is not true, the breakpoint is ignored. The expression must be valid at the breakpoint\'s line. [[src:jb-breakpoints]]'''),
        ('cond.s2', '''Đặt điều kiện theo triệu chứng (phí âm) thay vì theo chỉ số: bạn chưa cần biết đơn nào lỗi, debugger tìm giúp.''',
         '''Put the condition on the symptom (a negative fee) rather than on an index: you do not need to know which booking is bad, the debugger finds it.'''),
        ('cond.s3', '''Đây là hiệu ứng phụ của chính việc gỡ lỗi: dừng mọi luồng làm hỏng những gì phụ thuộc vào thời gian, như nhịp gửi máy chủ hay hạn chờ mạng.''',
         '''This is a side effect of debugging itself: suspending every thread breaks anything that depends on time, such as heartbeats or network timeouts.'''),
        ('thread.s1', '''Chọn chính sách theo câu hỏi: cần ảnh chụp đứng yên của cả app thì All; cần app chạy tiếp quanh luồng đang xem thì Thread. [[src:jb-breakpoints]]''',
         '''Choose the policy by your question: for a frozen snapshot of the whole app, All; to keep the app running around the thread you are looking at, Thread. [[src:jb-breakpoints]]'''),
        ('thread.s2', '''Bảng biến là ảnh chụp của luồng đang dừng: biến cục bộ, tham số, trường của object, ở đúng frame (hàm) đang dừng. [[src:jb-examine]]''',
         '''The variables view is a snapshot of the stopped thread: local variables, parameters and object fields, in the frame (function) where it stopped. [[src:jb-examine]]'''),
        ('thread.s3', '''Khi các luồng khác vẫn chạy, giá trị dùng chung có thể đổi dưới tay bạn. Lỗi do nhiều luồng đôi khi biến mất khi dừng mọi luồng, và lộ ra khi chỉ dừng một.''',
         '''With other threads still running, shared values can change under you. A multithreading bug sometimes vanishes when every thread is stopped and shows up when only one is.'''),
        ('logbp.s1', '''Breakpoint không dừng dùng để ghi log, hay làm cò kích hoạt cho breakpoint khác. "Evaluate and log" ghi kết quả của một biểu thức tùy ý, tính trong ngữ cảnh của dòng đó. [[src:jb-breakpoints]]''',
         '''A non-suspending breakpoint is for logging, or as a trigger for another breakpoint. "Evaluate and log" writes the result of any expression, evaluated in the context of that line. [[src:jb-breakpoints]]'''),
        ('logbp.s2', '''Đây là cách thay cho Log.d tạm thời: dòng log nằm trong debugger, không nằm trong mã, nên không thể lọt vào bản phát hành.''',
         '''This replaces a temporary Log.d: the log line lives in the debugger, not in the code, so it cannot slip into a release.'''),
        ('logbp.s3', '''Ghi log cho mỗi lần lặp vẫn làm vòng lặp chậm đi nhiều so với lúc không gỡ lỗi; đừng dùng số đo thời gian lấy khi debugger đang gắn.''',
         '''Logging on every iteration still slows the loop a lot compared with running undebugged; do not trust timings taken while the debugger is attached.'''),
    ]:
        m('co.' + k, vi, en)

    z = lambda k, vi, en=None: a('vz.' + k, vi, en)
    z('tab.bp', '''Làn luồng và bảng biến''', '''Thread lanes and variables''')
    z('bp.aria', '''Hai làn luồng; app dừng {s} lần, luồng đồng bộ lỡ {m} nhịp''', '''Two thread lanes; the app stops {s} times, the sync thread misses {m} heartbeats''')
    z('bp.lane.report', '''luồng báo cáo''', '''report thread'''); z('bp.lane.sync', '''luồng đồng bộ''', '''sync thread''')
    z('bp.axis', '''đơn 0 → 499''', '''booking 0 → 499'''); z('bp.hit', '''đơn 347''', '''booking 347''')
    z('bp.sub.stops', '''Dừng {s} lần, bấm chạy tiếp {r} lần.''', '''{s} stops, {r} resumes.''')
    z('bp.sub.sync', '''Luồng đồng bộ lỡ {m} nhịp (hạn 10): phiên {st}.''', '''The sync thread missed {m} heartbeats (limit 10): session {st}.''')
    z('bp.sub.logs', '''{n} dòng log; lọc phí âm còn {k} dòng.''', '''{n} log lines; filtering for a negative fee leaves {k}.''')
    z('bp.st.alive', '''còn sống''', '''alive'''); z('bp.st.expired', '''bị ngắt''', '''ended''')
    z('bp.vars.title', '''Bảng biến tại chỗ dừng''', '''Variables at the stop'''); z('bp.log.title', '''Log của breakpoint (quanh đơn 347)''', '''Breakpoint log (around booking 347)''')
    z('bp.col.name', '''Biến''', '''Variable'''); z('bp.col.val', '''Giá trị''', '''Value''')
    z('bp.legend', '''Vạch đỏ ở làn trên: một lần dừng. Chấm ở làn dưới: một nhịp gửi máy chủ; đoạn đỏ: lúc luồng đồng bộ bị dừng theo. Ô đỏ trong bảng: giá trị gây lỗi.''',
      '''A red mark on the upper lane: one stop. A dot on the lower lane: one heartbeat; a red stretch: when the sync thread was frozen too. A red cell in the table: the value causing the bug.''')

    C = 'l2'
    a(C + '.title', '''Debugger: breakpoint, watch, evaluate''', '''The debugger: breakpoints, watches, evaluate''')
    a(C + '.essence', '''Debugger (trình gỡ lỗi) dừng app ở một dòng để bạn xem biến của đúng lúc đó, thay vì đoán rồi thêm Log và build lại.\nBreakpoint thường dừng mỗi lần chạy qua dòng của nó. Đặt điều kiện (như fee < 0) thì chỉ dừng khi triệu chứng xuất hiện; bỏ dừng và cho ghi log một biểu thức thì có log mà không sửa mã.\nMặc định breakpoint dừng mọi luồng (thread, một dòng chạy mã song song trong app); điều đó làm hỏng những gì phụ thuộc thời gian, như nhịp gửi máy chủ. Có thể chỉ dừng luồng chạm breakpoint. Khi đã dừng, watch theo dõi một biểu thức qua từng bước, còn evaluate tính một biểu thức bất kỳ; cẩn thận, gọi hàm có side effect là đổi trạng thái của app.''',
      '''A debugger pauses the app at a line so you can see the variables at exactly that moment, instead of guessing, adding a Log and rebuilding.\nA plain breakpoint stops every time execution reaches its line. Add a condition (such as fee < 0) and it stops only when the symptom appears; turn off suspending and log an expression instead, and you get logs without touching the code.\nBy default a breakpoint suspends every thread, which breaks anything that depends on time, such as heartbeats to a server. You can suspend only the thread that hit it. Once stopped, a watch follows an expression from step to step, and evaluate computes any expression; careful, calling a function with side effects changes the app\'s state.''')
    a(C + '.goal.g1', '''Đã thấy breakpoint có điều kiện dừng đúng một lần''', '''Saw a conditional breakpoint stop exactly once''')
    a(C + '.goal.g2', '''Đã thấy chính sách dừng ảnh hưởng luồng khác''', '''Saw the suspend policy affect other threads''')
    a(C + '.sim.debugging.bp', '''bốn kiểu breakpoint trên cùng một lỗi''', '''four kinds of breakpoint on the same bug''')

    S_ = 'hook'
    a(C + '.sec.%s.title' % S_, '''Đoán trước khi đọc''', '''Predict before reading''')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'predict', '''Tổng phí tháng của 500 lịch hẹn bị sai, và chỉ một đơn có lỗi: đơn số 347 (đếm từ 0). Đặt một breakpoint thường trong vòng lặp, bạn phải bấm chạy tiếp bao nhiêu lần mới thấy đơn đó?''',
      '''The monthly fee total of 500 bookings is wrong, and only one booking is bad: number 347 (counting from 0). With a plain breakpoint in the loop, how many times must you press resume before you see that booking?''')
    B(C, S_, 1, 'ans', '''347 lần, với 348 lần dừng. Một điều kiện theo triệu chứng, fee < 0, đưa con số đó về một lần dừng, và không cần biết trước đơn nào lỗi. Mô phỏng ngay dưới so bốn kiểu breakpoint.''',
      '''347 times, with 348 stops. A condition on the symptom, fee < 0, brings that down to one stop, without knowing in advance which booking is bad. The simulation just below compares four kinds of breakpoint.''')

    S_ = 'kinds'
    a(C + '.sec.%s.title' % S_, '''Các loại breakpoint và điều kiện''', '''Kinds of breakpoint and conditions''')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'p', '''Trình gỡ lỗi của Android Studio dựa trên IntelliJ IDEA, và có bốn loại breakpoint. Breakpoint dòng dừng khi chạy tới một dòng. Breakpoint hàm dừng khi vào hay ra khỏi một hàm. Watchpoint trên trường dừng khi một trường được đọc hay ghi (không bắt được thay đổi qua reflection). Breakpoint ngoại lệ dừng khi một Throwable được ném ra, dù sau đó nó có bị bắt hay không. [[src:jb-breakpoints]]''',
      '''Android Studio\'s debugger is based on IntelliJ IDEA, and it has four kinds of breakpoint. A line breakpoint stops when execution reaches a line. A method breakpoint stops on entering or leaving a function. A field watchpoint stops when a field is read or written (changes made through reflection are not caught). An exception breakpoint stops when a Throwable is thrown, whether or not it is caught later. [[src:jb-breakpoints]]''')
    B(C, S_, 2, 'p', '''Mỗi breakpoint có thêm vài tùy chọn đáng nhớ. Điều kiện: một biểu thức Boolean, chỉ dừng khi nó true. Pass count: chỉ có hiệu lực sau một số lần chạm nhất định. Remove once hit: tự xóa sau lần chạm đầu. Breakpoint phụ thuộc: chỉ bật sau khi một breakpoint khác đã chạm, ví dụ chỉ dừng trong saveBooking() khi đã đi qua màn thanh toán. [[src:jb-breakpoints]]''',
      '''Each breakpoint has a few more options worth remembering. Condition: a Boolean expression; it stops only when that is true. Pass count: it takes effect only after a set number of hits. Remove once hit: it deletes itself after the first hit. A dependent breakpoint: it switches on only after another breakpoint has been hit, for example stopping in saveBooking() only after the payment screen has been passed. [[src:jb-breakpoints]]''')
    B(C, S_, 3, 'note', '''Breakpoint hàm thật chạy chậm, nên IntelliJ mặc định "mô phỏng" nó bằng breakpoint dòng ở câu lệnh đầu và cuối của hàm. Điều kiện cũng có thể có side effect: một điều kiện gọi hàm đổi trạng thái sẽ đổi luôn hành vi của app. [[src:jb-breakpoints]]''',
      '''True method breakpoints are slow, so IntelliJ by default "emulates" them with line breakpoints on the function\'s first and last statements. Conditions can have side effects too: a condition that calls a state-changing function changes the app\'s behaviour. [[src:jb-breakpoints]]''')
    B(C, S_, 3, 'kind', 'pitfall')

    S_ = 'suspend'
    a(C + '.sec.%s.title' % S_, '''Dừng luồng nào: All hay Thread''', '''Which threads stop: All or Thread''')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'p', '''Khi một luồng chạm breakpoint, chính sách dừng quyết định ai đứng lại. All: mọi luồng của app dừng, bạn có một ảnh chụp đứng yên. Thread: chỉ luồng chạm breakpoint dừng, các luồng khác chạy tiếp. Bỏ hẳn Suspend thì breakpoint không dừng gì, chỉ ghi log hay làm cò cho breakpoint khác. [[src:jb-breakpoints]]''',
      '''When a thread hits a breakpoint, the suspend policy decides who stops. All: every thread in the app stops, giving you a frozen snapshot. Thread: only the thread that hit the breakpoint stops; the others carry on. Turn Suspend off entirely and the breakpoint stops nothing; it only logs, or triggers another breakpoint. [[src:jb-breakpoints]]''')
    B(C, S_, 2, 'p', '''Dừng mọi luồng tiện cho việc đọc, nhưng thời gian vẫn trôi bên ngoài app: máy chủ vẫn đếm hạn phiên, kết nối mạng vẫn hết hạn chờ. Khi gỡ lỗi mã có nhịp, hạn chờ hay nhiều luồng phối hợp, chỉ dừng luồng bạn cần xem. Ngược lại, khi cần chắc không luồng nào đổi dữ liệu trong lúc bạn nhìn, hãy dừng tất cả.''',
      '''Stopping every thread makes reading easy, but time still passes outside the app: the server still counts down the session, network connections still time out. When debugging code with heartbeats, timeouts or several cooperating threads, suspend only the thread you need to see. Conversely, when you must be sure no thread changes data while you look, suspend them all.''')

    S_ = 'inspect'
    a(C + '.sec.%s.title' % S_, '''Khi đã dừng: biến, watch, evaluate''', '''Once stopped: variables, watches, evaluate''')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'p', '''Khi app dừng ở một breakpoint, bạn thấy biến cục bộ, tham số và trường của object ở frame đang dừng, và có thể chọn frame khác trong chuỗi gọi để xem biến của hàm gọi nó. Watch giữ một biến hay một biểu thức phức tạp hơn trong tầm mắt, và được tính lại ở mỗi bước. Watch và evaluate chỉ chạy khi app đang dừng ở breakpoint, không chạy khi bạn chỉ tạm dừng app bằng tay. [[src:jb-examine]]''',
      '''When the app stops at a breakpoint, you see the local variables, parameters and object fields of the frame where it stopped, and you can pick another frame in the call chain to see its caller\'s variables. A watch keeps a variable or a more complex expression in view, recomputed at every step. Watches and evaluate only work while the app is stopped at a breakpoint, not when you merely pause it by hand. [[src:jb-examine]]''')
    B(C, S_, 2, 'p', '''Evaluate tính một biểu thức bất kỳ trong ngữ cảnh của frame đang dừng, kể cả khai báo biến và gọi hàm. Đây cũng là chỗ dễ tự gây lỗi: gọi một hàm có side effect là chạy thật hàm đó trên app thật. Breakpoint nằm trong hàm được gọi lúc evaluate sẽ bị bỏ qua. [[src:jb-examine]]''',
      '''Evaluate computes any expression in the context of the stopped frame, including variable declarations and function calls. It is also an easy place to cause a bug yourself: calling a function with side effects really runs it in the real app. Breakpoints inside functions called during evaluation are ignored. [[src:jb-examine]]''')
    B(C, S_, 3, 'kt', '''// đang dừng ở đơn 347, evaluate:
b.base * (100 - b.discountPercent) / 100   // an toàn: chỉ tính, ra -40000
repo.markChecked(b)                        // KHÔNG an toàn: ghi vào database thật
counter.next()                             // KHÔNG an toàn: bộ đếm tăng thêm 1, lần chạy sau lệch đi''',
      '''// stopped at booking 347, evaluate:
b.base * (100 - b.discountPercent) / 100   // safe: computes only, gives -40000
repo.markChecked(b)                        // NOT safe: writes to the real database
counter.next()                             // NOT safe: the counter goes up by 1, the next run is off''')
    B(C, S_, 4, 'note', '''Watch có thể tốn nhiều tính toán vì được tính lại ở mỗi bước; một watch nặng làm việc đi từng bước chậm hẳn. Có thể tạm dừng watch đó và chỉ tính khi cần. [[src:jb-examine]]''',
      '''A watch can be expensive because it is recomputed at every step; a heavy watch makes stepping noticeably slow. You can pause that watch and compute it only on demand. [[src:jb-examine]]''')

    S_ = 'coroutines'
    a(C + '.sec.%s.title' % S_, '''Gỡ lỗi coroutine''', '''Debugging coroutines''')
    a(C + '.sec.%s.badge' % S_, 'version')
    B(C, S_, 1, 'p', '''Một coroutine có thể bắt đầu trên luồng này rồi chạy tiếp trên luồng khác sau mỗi lần suspend, nên tên luồng không nói nhiều. kotlinx-coroutines (thư viện coroutine của Kotlin, bản 1.11.0) có chế độ debug: mỗi coroutine được đặt một tên duy nhất, hiện trong debugger, trong chuỗi mô tả coroutine, và trong tên luồng khi luồng đó đang chạy nó. Bật bằng thuộc tính hệ thống kotlinx.coroutines.debug; chạy với assertion (lệnh assert tự kiểm điều kiện trong mã) bật (-ea, mặc định khi chạy unit test trên JVM) cũng bật nó. Tài liệu nói chi phí lúc chạy của chế độ này không đáng kể. [[src:kx-coroutines-debug]]''',
      '''A coroutine can start on one thread and continue on another after each suspension, so thread names tell you little. kotlinx-coroutines (Kotlin\'s coroutine library, version 1.11.0) has a debug mode: every coroutine gets a unique name, shown in the debugger, in the coroutine\'s string form, and in the thread name while that thread is running it. Turn it on with the kotlinx.coroutines.debug system property; running with assertions (assert statements that check a condition in the code) enabled (-ea, the default for unit tests on the JVM) turns it on too. The documentation says its runtime overhead is negligible. [[src:kx-coroutines-debug]]''')
    B(C, S_, 2, 'p', '''Chế độ debug còn bật khôi phục stack trace: khi một ngoại lệ đi qua một lời gọi suspend như await(), thư viện tạo một bản sao của ngoại lệ có thêm các frame của nơi đang chờ, và gắn ngoại lệ gốc làm cause. Trong stack trace bạn sẽ thấy một frame đánh dấu ranh giới coroutine (_COROUTINE._BOUNDARY). Chương "Đọc stack trace" nói cách đọc chuỗi cause này. [[src:kx-coroutines-debug]]''',
      '''Debug mode also turns on stack trace recovery: when an exception passes through a suspending call such as await(), the library creates a copy of the exception with extra frames from the waiting side, and attaches the original as its cause. In the stack trace you will see a frame marking the coroutine boundary (_COROUTINE._BOUNDARY). The chapter "Reading stack traces" explains how to read this cause chain. [[src:kx-coroutines-debug]]''')
    B(C, S_, 3, 'note', '''Module kotlinx-coroutines-debug có debug agent (DebugProbes) để in danh sách mọi coroutine đang sống cùng trạng thái và chỗ đang treo, rất có ích khi một test chờ mãi. Tài liệu nói rõ debug agent không chạy trên Android; dùng nó trong unit test chạy trên JVM. [[src:kx-coroutines-debug]]''',
      '''The kotlinx-coroutines-debug module has a debug agent (DebugProbes) that prints every live coroutine with its state and where it is suspended, very useful when a test waits forever. The documentation states clearly that the debug agent is not supported on Android; use it in unit tests running on the JVM. [[src:kx-coroutines-debug]]''')
    B(C, S_, 3, 'kind', 'pitfall')

    S_ = 'bugs'
    a(C + '.sec.%s.title' % S_, '''Hai lỗi hay gặp''', '''Two common bugs''')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'bug', '''Lỗi biến mất khi gỡ lỗi: dừng ở breakpoint thì mọi thứ đúng, chạy bình thường thì sai.''', '''The bug vanishes under the debugger: stopped at a breakpoint everything is right, running normally it is wrong.''')
    B(C, S_, 1, 'cause', '''Lỗi phụ thuộc thứ tự giữa các luồng; dừng mọi luồng đã thay đổi chính thứ tự đó.''', '''The bug depends on the order between threads; suspending every thread changed that very order.''')
    B(C, S_, 1, 'fix', '''Dùng breakpoint chỉ ghi log hay chính sách Suspend Thread để quan sát mà ít làm đổi thời gian; rồi tái hiện bằng test.''', '''Use logging breakpoints or the Suspend Thread policy to observe with less disturbance to timing; then reproduce it with a test.''')
    B(C, S_, 2, 'bug', '''Sau một buổi gỡ lỗi, database có thêm vài dòng "đã kiểm" không ai tạo.''', '''After a debugging session, the database has a few "checked" rows nobody created.''')
    B(C, S_, 2, 'cause', '''Ai đó đã evaluate repo.markChecked(b) hay đặt nó trong một điều kiện breakpoint: hàm có side effect chạy thật.''', '''Someone evaluated repo.markChecked(b), or put it in a breakpoint condition: a function with side effects really ran.''')
    B(C, S_, 2, 'fix', '''Khi evaluate hay viết điều kiện, chỉ dùng biểu thức đọc: phép tính, getter không side effect.''', '''When evaluating or writing conditions, use only reading expressions: arithmetic, getters without side effects.''')

    S_ = 'ex'
    a(C + '.sec.%s.title' % S_, '''Bài tập''', '''Exercise''')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'ex', '''Màn danh sách thỉnh thoảng hiện một lịch hẹn với tên bệnh nhân trống. Danh sách có khoảng 2.000 lịch, được nạp lại mỗi lần mở màn. Hãy chọn kiểu breakpoint, vị trí, điều kiện hay biểu thức log, và chính sách dừng, để tìm lịch nào gây lỗi mà không phải bấm chạy tiếp hàng nghìn lần.''',
      '''The list screen occasionally shows a booking with an empty patient name. The list has about 2,000 bookings and reloads every time the screen opens. Choose a kind of breakpoint, a location, a condition or a log expression, and a suspend policy, to find which booking causes it without pressing resume thousands of times.''')
    B(C, S_, 1, 'hint', '''Đặt điều kiện theo triệu chứng, không theo chỉ số. Đặt ở chỗ dữ liệu được tạo ra (ánh xạ từ dữ liệu mạng sang Booking) thì thấy nguyên nhân sớm hơn chỗ hiển thị.''',
      '''Put the condition on the symptom, not on an index. Placing it where the data is created (mapping network data to Booking) shows the cause earlier than where it is displayed.''')
    B(C, S_, 1, 'sol', '''Breakpoint dòng trong hàm ánh xạ, điều kiện patientName.isBlank(); chính sách Thread để luồng giao diện còn vẽ được. Hoặc không dừng mà ghi log "id=$id raw=$raw" khi điều kiện đúng. Lần chạm đầu cho bạn đúng bản ghi lỗi và dữ liệu gốc của nó.''',
      '''A line breakpoint in the mapping function with the condition patientName.isBlank(); the Thread policy so the UI thread can still draw. Or do not stop at all and log "id=$id raw=$raw" when the condition holds. The first hit gives you exactly the bad record and its raw data.''')

    S_ = 'recall'
    a(C + '.sec.%s.title' % S_, '''Tự trả lời''', '''Answer it yourself''')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'ask', '''Khác nhau giữa chính sách All và Thread là gì, và khi nào chọn Thread?''', '''What is the difference between the All and Thread policies, and when do you choose Thread?''')
    B(C, S_, 1, 'ans', '''All dừng mọi luồng; Thread chỉ dừng luồng chạm breakpoint. Chọn Thread khi mã phụ thuộc thời gian hay nhiều luồng phối hợp, như nhịp gửi máy chủ hay hạn chờ mạng.''', '''All suspends every thread; Thread suspends only the one that hit the breakpoint. Choose Thread when the code depends on time or on cooperating threads, such as heartbeats or network timeouts.''')
    B(C, S_, 2, 'ask', '''Vì sao evaluate repo.markChecked(b) là nguy hiểm?''', '''Why is evaluating repo.markChecked(b) dangerous?''')
    B(C, S_, 2, 'ans', '''Evaluate chạy thật hàm đó trên app đang chạy; nó ghi vào database thật.''', '''Evaluate really runs that function in the running app; it writes to the real database.''')

    for q, qv, qe, av, ae, wv, we in [
        ('q1', 'Một breakpoint thường trong vòng lặp 500 lần dừng bao nhiêu lần?', 'How many times does a plain breakpoint in a 500-iteration loop stop?', '500 lần, mỗi lần lặp một lần.', '500 times, once per iteration.',
         'Breakpoint dừng mỗi lần chạy qua dòng của nó.', 'A breakpoint stops every time execution reaches its line.'),
        ('q2', 'Muốn có log mà không sửa mã và không build lại, dùng gì?', 'To get logs without changing the code or rebuilding, what do you use?', 'Breakpoint không dừng với "Evaluate and log".', 'A non-suspending breakpoint with "Evaluate and log".',
         'Dòng log nằm trong debugger, không thể lọt vào bản phát hành.', 'The log line lives in the debugger and cannot slip into a release.'),
        ('q3', 'Watch và evaluate có chạy khi bạn chỉ tạm dừng app bằng tay không?', 'Do watches and evaluate work when you merely pause the app by hand?', 'Không; chỉ khi app dừng ở một breakpoint.', 'No; only when the app is stopped at a breakpoint.',
         'Chúng cần một frame đang dừng để tính trong ngữ cảnh của nó.', 'They need a stopped frame to evaluate in its context.'),
        ('q4', 'Debug agent của kotlinx-coroutines có chạy trên Android không?', 'Does the kotlinx-coroutines debug agent run on Android?', 'Không; dùng nó trong unit test trên JVM.', 'No; use it in unit tests on the JVM.',
         'Tài liệu ghi rõ debug agent không được hỗ trợ trên Android.', 'The documentation says the debug agent is not supported on Android.')]:
        a(C + '.quiz.%s.q' % q, qv, qe); a(C + '.quiz.%s.a' % q, av, ae); a(C + '.quiz.%s.why' % q, wv, we)
