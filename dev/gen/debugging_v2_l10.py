# Gỡ lỗi và hiệu năng · l10: ANR và StrictMode (Phần 3: lỗi trên máy người dùng)
# Nguồn (chỉ ghi ở đây và docs/research/debugging.md), đọc 2026-11-25, trang không ghi ngày: developer.android.com/topic/performance/vitals/anr
# (ANR khi luồng main không xử lý được input hay vẽ; 5 giây cho input; nguyên nhân: I/O, tính lâu, binder đồng bộ, chờ khóa của luồng khác, deadlock;
# trace ở /data/anr, bug report), topic/performance/anrs/diagnose-and-fix-anrs (hạn mặc định của AOSP và Pixel, có thể khác theo hãng: input 5 s,
# service 20 s tiền cảnh, 200 s nền, broadcast 10 s / 60 s tới Android 13, 10–20 s / 60–120 s từ Android 14; trạng thái Blocked, Waiting; "held by";
# deadlock; Mutex.withLock; nativePollOnce thường không hành động được), reference/android/os/StrictMode (công cụ cho nhà phát triển bắt việc vô tình như
# đọc ghi đĩa, mạng trên main; detectAll, penaltyLog; không phải cơ chế bảo mật, không bắt được mọi truy cập). Khóa, luồng sync và 9 giây là của site.

SEC_ORDER = {'l10': ['hook', 'what', 'causes', 'read', 'strict', 'bugs', 'ex', 'recall']}


def add(a):
    def B(ch, sec, n, field, vi, en=None):
        a('%s.sec.%s.b.%02d.%s' % (ch, sec, n, field), vi, vi if en is None else en)

    a('preset.anr', '''Gỡ lỗi · ANR khi bấm Lưu và StrictMode''', '''Debugging · an ANR on Save, and StrictMode''')
    m = lambda k, vi, en=None: a('m.anr.' + k, vi, en)
    m('title', '''Bấm "Lưu" thì app đứng, Android hỏi có đóng app không''', '''Tapping "Save" freezes the app, and Android offers to close it''')
    m('overview', '''Android vitals báo ANR ở nút "Lưu" của app Hẹn Khám, nhưng trên máy dev không tái hiện được. Cách 1 đọc trace các luồng lúc ANR: luồng main đang chờ gì, ai đang giữ thứ đó. Cách 2 bật StrictMode trong bản debug để bắt việc đọc ghi đĩa và mạng trên luồng main ngay khi phát triển. Thời gian chờ của luồng main và các vi phạm được tính thật từ mô hình của các luồng.''',
      '''Android vitals reports an ANR on ClinicBook\'s "Save" button, but it does not reproduce on the dev device. Way 1 reads the threads\' traces at the ANR: what the main thread is waiting for, and who holds it. Way 2 turns on StrictMode in the debug build to catch disk and network access on the main thread during development. The main thread\'s waiting time and the violations are really computed from a model of the threads.''')
    m('wrapup', '''Luồng main không chậm vì tự làm việc nặng: nó chờ khóa (lock) mà luồng đồng bộ giữ trong lúc gọi mạng. Trên Wi-Fi nhanh, khóa được nhả sau 0,3 giây nên không ai thấy; trên 4G chậm, luồng main chờ 8 giây, quá hạn 5 giây cho input, và hệ thống báo ANR. Gọi mạng ngoài khóa, chỉ khóa phần ghi bộ nhớ, thì thời gian chờ gần như bằng 0. StrictMode bắt sớm loại việc này ngay trên máy dev.''',
      '''The main thread is not slow because it does heavy work itself: it waits for a lock the sync thread holds during a network call. On fast Wi-Fi the lock is released after 0.3 seconds, so nobody notices; on slow 4G the main thread waits 8 seconds, past the 5-second input deadline, and the system reports an ANR. Calling the network outside the lock and locking only the in-memory update brings the wait close to 0. StrictMode catches this kind of thing early, on the dev device.''')
    m('simp.1', '''Chỉ có bốn luồng và một khóa; trace ANR thật có hàng chục luồng. Thời gian mạng 0,3 và 9 giây là của site.''', '''Only four threads and one lock; a real ANR trace has dozens of threads. The 0.3 and 9 second network times are the site\'s.''')
    m('simp.2', '''Thời gian luồng main phải chờ khóa được tính thật: luồng sync lấy khóa 1 giây trước khi bấm Lưu và giữ nó suốt lời gọi mạng; ANR khi thời gian chờ vượt 5 giây. Danh sách vi phạm StrictMode được lọc thật từ các thao tác chạy trên luồng main.''',
      '''The main thread\'s wait for the lock is really computed: the sync thread takes the lock 1 second before Save is tapped and holds it for the whole network call; an ANR occurs when the wait exceeds 5 seconds. The StrictMode violation list is really filtered from the operations running on the main thread.''')
    m('ctl.hint', '''Chọn cách tìm rồi đi qua bốn bước; xem hàng luồng nào được tô và thanh chờ của luồng main.''', '''Pick an approach and walk the four steps; watch which thread rows are highlighted and the main thread\'s wait bar.''')
    m('ctl.case', '''Cách tìm''', '''Approach''')
    m('ctl.case.trace', '''đọc trace các luồng lúc ANR''', '''read the threads\' traces at the ANR'''); m('ctl.case.strict', '''bật StrictMode khi phát triển''', '''turn on StrictMode during development''')
    m('diagramTitle', '''Luồng main chờ khóa''', '''The main thread waits for a lock''')
    m('diagramDesc', '''Nút Lưu chạy trên main; main chờ khóa; luồng sync giữ khóa trong lúc gọi mạng''', '''Save runs on main; main waits for the lock; the sync thread holds it during a network call''')
    for k, vi, en in [('tap', 'Bấm Lưu (input)', 'Tap Save (input)'), ('main', 'Luồng main', 'Main thread'), ('lock', 'Khóa của BookingRepo', 'BookingRepo\'s lock'),
                      ('sync', 'Luồng sync: gọi mạng', 'Sync thread: network call'), ('strict', 'StrictMode (bản debug)', 'StrictMode (debug build)')]:
        m('n.' + k, vi, en)
    m('met.net', '''Thời gian gọi mạng (giây)''', '''Network call time (s)'''); m('met.wait', '''Luồng main chờ (giây)''', '''Main thread waits (s)''')
    m('met.anr', '''ANR (hạn input 5 giây)''', '''ANR (5 s input deadline)'''); m('met.viol', '''Vi phạm StrictMode''', '''StrictMode violations''')
    m('anr.no', '''không''', '''no'''); m('anr.yes', '''có''', '''yes''')
    a('cap.anr', '''Input vào luồng main; luồng main cần khóa mà luồng sync đang giữ trong lúc gọi mạng. Ô đỏ: chỗ làm luồng main đứng.''', '''Input reaches the main thread; the main thread needs the lock the sync thread holds during a network call. A red box: what freezes the main thread.''')
    S = [
        ('trace', 's1', 'Vitals báo ANR ở nút Lưu; máy dev không tái hiện được', 'Vitals reports an ANR on Save; the dev device cannot reproduce it',
         'Trên máy dev với Wi-Fi nhanh, bấm Lưu luôn tức thì. Luồng sync lấy khóa trước khi bấm 1 giây, gọi mạng 0,3 giây rồi nhả, nên luồng main không phải chờ. Lỗi chỉ hiện ở điều kiện của người dùng.',
         'On the dev device with fast Wi-Fi, Save is always instant. The sync thread takes the lock 1 second before the tap, calls the network for 0.3 seconds and releases it, so the main thread never waits. The bug appears only under the user\'s conditions.'),
        ('trace', 's2', 'Trace lúc ANR: main Blocked, chờ khóa do luồng 24 giữ', 'The trace at the ANR: main Blocked, waiting for a lock held by thread 24',
         'Mở trace của ANR từ Play Console hay bug report. Luồng main (tid 1) ở trạng thái Blocked trong BookingRepo.save, dòng "waiting to lock <0x0a1b> held by tid=24". Luồng main không làm gì nặng; nó đang chờ.',
         'Open the ANR trace from Play Console or a bug report. The main thread (tid 1) is Blocked in BookingRepo.save, with the line "waiting to lock <0x0a1b> held by tid=24". The main thread is doing nothing heavy; it is waiting.'),
        ('trace', 's3', 'Luồng 24 giữ khóa trong lúc đọc socket: 4G chậm, 9 giây', 'Thread 24 holds the lock while reading a socket: slow 4G, 9 seconds',
         'Đi tới tid 24, luồng SyncWorker: nó đang đọc socket bên trong BookingRepo.sync, trong khối synchronized cùng khóa 0x0a1b. Trên 4G chậm lời gọi mạng mất 9 giây; bấm Lưu 1 giây sau khi sync bắt đầu, luồng main phải chờ 8 giây, quá hạn 5 giây cho input.',
         'Go to tid 24, the SyncWorker thread: it is reading a socket inside BookingRepo.sync, within a synchronized block on the same lock 0x0a1b. On slow 4G the network call takes 9 seconds; tapping Save 1 second after sync starts, the main thread must wait 8 seconds, past the 5-second input deadline.'),
        ('trace', 's4', 'Sửa: gọi mạng ngoài khóa, chỉ khóa phần ghi bộ nhớ', 'Fix: call the network outside the lock, lock only the in-memory update',
         'sync() gọi mạng trước, rồi mới lấy khóa để ghi kết quả vào cache, mất vài mili giây. save() chạy trên Dispatchers.IO thay vì main. Trên 4G chậm, luồng main giờ chờ gần 0 giây: không ANR.',
         'sync() calls the network first and only then takes the lock to write the result into the cache, a few milliseconds. save() runs on Dispatchers.IO instead of main. On slow 4G the main thread now waits close to 0 seconds: no ANR.'),
        ('strict', 's1', 'Bật StrictMode trong bản debug', 'Turn on StrictMode in the debug build',
         'Trong Application.onCreate của bản debug, đặt ThreadPolicy với detectAll và penaltyLog. Từ giờ mỗi lần luồng main đọc ghi đĩa hay gọi mạng, Logcat in một vi phạm kèm stack trace.',
         'In the debug build\'s Application.onCreate, set a ThreadPolicy with detectAll and penaltyLog. From now on, every disk or network access on the main thread prints a violation with a stack trace to Logcat.'),
        ('strict', 's2', 'Bấm Lưu: hai vi phạm trên luồng main', 'Tap Save: two violations on the main thread',
         'Logcat in DiskReadViolation và DiskWriteViolation từ BookingRepo.save: lời ghi database chạy thẳng trên main. Trên máy dev nó chỉ mất 40 ms nên không ai thấy chậm, nhưng StrictMode vẫn báo.',
         'Logcat prints DiskReadViolation and DiskWriteViolation from BookingRepo.save: the database write runs straight on main. On the dev device it takes only 40 ms, so nobody notices, but StrictMode still reports it.'),
        ('strict', 's3', 'Vi phạm chỉ ra đúng chỗ sẽ thành ANR', 'The violation points at exactly what would become an ANR',
         'save() chạy trên main và lấy khóa của BookingRepo; chính lời gọi đó là chỗ luồng main bị kẹt trong ANR ở cách đọc trace. StrictMode không biết về khóa, nhưng nó chỉ ra việc không nên nằm trên main ngay từ máy dev.',
         'save() runs on main and takes BookingRepo\'s lock; that very call is where the main thread got stuck in the ANR of the trace approach. StrictMode knows nothing about the lock, but it flags work that should not be on main right on the dev device.'),
        ('strict', 's4', 'Dời save() sang Dispatchers.IO: không còn vi phạm', 'Move save() to Dispatchers.IO: no more violations',
         'Bấm Lưu giờ chạy save() trong withContext(Dispatchers.IO). Logcat không còn vi phạm nào từ luồng main, và luồng main không bao giờ phải chờ khóa của BookingRepo nữa.',
         'Tapping Save now runs save() inside withContext(Dispatchers.IO). Logcat shows no more violations from the main thread, and the main thread never waits for BookingRepo\'s lock again.'),
    ]
    for case, k, tv, te, xv, xe in S:
        sid = case + '.' + k
        m('s.%s.title' % sid, tv, te); m('s.%s.explain' % sid, xv, xe); m('ev.' + sid, tv, te)
    for k, vi, en in [
        ('try', '''Mẹo đọc: bảng là các luồng trong trace ANR (tên, trạng thái, đang chờ gì, đang giữ gì); dòng nối là "chờ" với "giữ". Thanh dưới là thời gian luồng main chờ, vạch đỏ là hạn 5 giây.''',
         '''Reading tip: the table is the threads in the ANR trace (name, state, waiting for, holding); the connecting line links "waiting" to "holding". The bar below is the main thread\'s wait, the red mark the 5-second deadline.'''),
        ('trace.s2', '''Một nguyên nhân ANR hay gặp: luồng main bị chặn trong khối synchronized vì một luồng khác đang giữ khóa đó. Khi luồng main chờ khóa, luồng giữ khóa cũng liên quan. [[src:ad-anr]] [[src:ad-anr-diagnose]]''',
         '''A common ANR cause: the main thread is blocked in a synchronized block because another thread holds that lock. When the main thread waits for a lock, the holder thread is involved too. [[src:ad-anr]] [[src:ad-anr-diagnose]]'''),
        ('trace.s3', '''Nếu app không phản hồi một input (bấm phím, chạm màn hình) trong 5 giây, hệ thống báo ANR; nếu app đang ở tiền cảnh, người dùng thấy hộp thoại. [[src:ad-anr]]''',
         '''If the app has not responded to an input event (a key press, a touch) within 5 seconds, the system reports an ANR; if the app is in the foreground, the user sees a dialog. [[src:ad-anr]]'''),
        ('trace.s4', '''Tài liệu gợi ý thay khóa nguyên thủy bằng Mutex.withLock của coroutine; ý chung là đừng giữ khóa trong lúc làm việc chậm, và đừng để luồng main chờ khóa. [[src:ad-anr-diagnose]]''',
         '''The documentation suggests replacing primitive locks with coroutine Mutex.withLock; the general idea is never to hold a lock during slow work, and never to make the main thread wait for one. [[src:ad-anr-diagnose]]'''),
        ('strict.s1', '''StrictMode là công cụ cho nhà phát triển, bắt những việc bạn có thể làm vô tình; hay dùng nhất để bắt truy cập đĩa hay mạng trên luồng main. [[src:ad-strictmode]]''',
         '''StrictMode is a developer tool that detects things you might be doing by accident; it is most commonly used to catch disk or network access on the main thread. [[src:ad-strictmode]]'''),
        ('strict.s2', '''Với penaltyLog, vi phạm được ghi vào log để xem bằng adb logcat; bạn không buộc phải sửa mọi thứ StrictMode báo, nhưng gọi mạng trên luồng UI gần như luôn là vấn đề. [[src:ad-strictmode]]''',
         '''With penaltyLog, violations are logged for adb logcat; you need not fix everything StrictMode finds, but network requests on the UI thread are almost always a problem. [[src:ad-strictmode]]'''),
        ('strict.s3', '''StrictMode không phải cơ chế bảo mật và không bảo đảm bắt được mọi truy cập đĩa hay mạng, ví dụ qua JNI. [[src:ad-strictmode]]''',
         '''StrictMode is not a security mechanism and is not guaranteed to find every disk or network access, for example through JNI. [[src:ad-strictmode]]'''),
        ('strict.s4', '''Bắt được trên máy dev thì không phải đợi vitals báo từ máy người dùng: đó là cách đẩy việc phát hiện lỗi lên sớm hơn.''',
         '''Catching it on the dev device means not waiting for vitals to report it from users\' phones: it moves detection earlier.'''),
    ]:
        m('co.' + k, vi, en)

    z = lambda k, vi, en=None: a('vz.' + k, vi, en)
    z('tab.anr', '''Trace các luồng và thời gian chờ''', '''Thread traces and waiting time''')
    for k, vi, en in [('name', 'Luồng', 'Thread'), ('state', 'Trạng thái', 'State'), ('wait', 'Đang chờ', 'Waiting for'), ('hold', 'Đang giữ', 'Holding'), ('at', 'Đang ở', 'At')]:
        z('an.col.' + k, vi, en)
    z('an.net', '''Mạng: {n}''', '''Network: {n}'''); z('an.net.wifi', '''Wi-Fi nhanh (gọi mạng 0,3 giây)''', '''fast Wi-Fi (0.3 s network call)'''); z('an.net.slow', '''4G chậm (gọi mạng 9 giây)''', '''slow 4G (9 s network call)''')
    z('an.bar', '''Luồng main chờ {w} giây; hạn input 5 giây.''', '''The main thread waits {w} s; the input deadline is 5 s.''')
    z('an.viol.title', '''Logcat: vi phạm StrictMode''', '''Logcat: StrictMode violations'''); z('an.viol.none', '''(chưa bật StrictMode)''', '''(StrictMode not enabled)''')
    z('an.outside', '''(ngoài khóa)''', '''(outside the lock)''')
    z('an.viol.zero', '''không có vi phạm nào trên luồng main''', '''no violations on the main thread''')
    z('an.legend', '''Hàng tô viền: luồng đang xét. Ô đỏ: trạng thái chờ hay khóa gây ANR. Thanh: thời gian luồng main chờ; vạch đỏ ở 5 giây.''',
      '''Outlined row: the thread being examined. Red cell: the waiting state or lock causing the ANR. Bar: the main thread\'s waiting time; the red mark at 5 s.''')

    C = 'l10'
    a(C + '.title', '''ANR và StrictMode''', '''ANRs and StrictMode''')
    a(C + '.essence', '''ANR (Application Not Responding) xảy ra khi luồng main không xử lý được input hay vẽ trong một thời hạn, như 5 giây cho một cú chạm; nếu app đang hiện, hệ thống hỏi người dùng có đóng app không.\nLuồng main thường không tự làm việc nặng mà đang chờ: chờ I/O, chờ một lời gọi binder, hay chờ khóa (lock) mà luồng khác giữ trong lúc làm việc chậm. Trace ANR cho thấy trạng thái từng luồng; tìm dòng "waiting to lock … held by" rồi đi tới luồng giữ khóa.\nStrictMode (bật trong bản debug) báo mỗi lần luồng main đọc ghi đĩa hay gọi mạng, để bắt loại lỗi này trên máy dev, trước khi nó thành ANR trên máy người dùng.''',
      '''An ANR (Application Not Responding) happens when the main thread cannot handle input or draw within a deadline, such as 5 seconds for a touch; if the app is visible, the system asks the user whether to close it.\nThe main thread is usually not doing heavy work itself but waiting: on I/O, on a binder call, or on a lock that another thread holds during slow work. An ANR trace shows each thread\'s state; find the "waiting to lock … held by" line, then go to the thread holding the lock.\nStrictMode (enabled in debug builds) reports every disk or network access on the main thread, so you catch this kind of bug on the dev device before it becomes an ANR on users\' phones.''')
    a(C + '.goal.g1', '''Đã thấy luồng main chờ khóa của luồng khác''', '''Saw the main thread waiting for another thread\'s lock''')
    a(C + '.goal.g2', '''Đã thấy thời gian chờ về gần 0''', '''Saw the wait drop close to zero''')
    a(C + '.sim.debugging.anr', '''đọc trace ANR, và bắt sớm bằng StrictMode''', '''reading an ANR trace, and catching it early with StrictMode''')

    S_ = 'hook'
    a(C + '.sec.%s.title' % S_, '''Đoán trước khi đọc''', '''Predict before reading''')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'predict', '''Trace của một ANR cho thấy luồng main ở trạng thái Blocked, CPU của luồng main gần như không dùng. Luồng main đang làm việc nặng, hay đang làm gì?''',
      '''An ANR trace shows the main thread Blocked, using almost no CPU. Is the main thread doing heavy work, or what is it doing?''')
    B(C, S_, 1, 'ans', '''Nó đang chờ: Blocked nghĩa là chờ một khóa mà luồng khác giữ. Phải đi tới luồng giữ khóa mới thấy nguyên nhân. Mô phỏng ngay dưới đọc một trace như vậy, và cho thấy StrictMode bắt nó từ sớm ra sao.''',
      '''It is waiting: Blocked means waiting for a lock another thread holds. You have to go to the holder thread to see the cause. The simulation just below reads such a trace, and shows how StrictMode catches it early.''')

    S_ = 'what'
    a(C + '.sec.%s.title' % S_, '''ANR là gì, và các hạn''', '''What an ANR is, and the deadlines''')
    a(C + '.sec.%s.badge' % S_, 'version')
    B(C, S_, 1, 'p', '''ANR xảy ra khi luồng main của app không xử lý được input hay vẽ. Hạn tùy loại việc; đây là mặc định của AOSP và máy Pixel, các hãng có thể đổi: input (chạm, phím) 5 giây; Service 20 giây khi ở tiền cảnh, 200 giây khi ở nền; BroadcastReceiver tới Android 13 là 10 giây (tiền cảnh) và 60 giây (nền), từ Android 14 là 10–20 giây và 60–120 giây tùy tiến trình có bị thiếu CPU không. Gọi startForegroundService thì phải gọi startForeground trong 5 giây. [[src:ad-anr]] [[src:ad-anr-diagnose]]''',
      '''An ANR happens when the app\'s main thread cannot handle input or draw. The deadline depends on the kind of work; these are AOSP and Pixel defaults that manufacturers may change: input (touch, key) 5 seconds; a Service 20 seconds in the foreground, 200 in the background; a BroadcastReceiver up to Android 13 10 seconds (foreground) and 60 (background), from Android 14 10–20 and 60–120 seconds depending on whether the process is CPU-starved. After startForegroundService, startForeground must be called within 5 seconds. [[src:ad-anr]] [[src:ad-anr-diagnose]]''')

    S_ = 'causes'
    a(C + '.sec.%s.title' % S_, '''Vì sao luồng main không phản hồi''', '''Why the main thread does not respond''')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'p', '''Các nguyên nhân hay gặp: I/O (đĩa, mạng) trên luồng main; tính toán dài trên luồng main; gọi binder đồng bộ sang một tiến trình chậm; luồng main bị chặn trong khối synchronized vì luồng khác giữ khóa (lock) đó; và deadlock, khi hai luồng mỗi bên giữ thứ bên kia cần và cùng chờ nhau mãi. Hai cái sau đặc biệt khó vì luồng main không bận: nó chỉ chờ. [[src:ad-anr]]''',
      '''Common causes: I/O (disk, network) on the main thread; long computation on the main thread; a synchronous binder call to a slow process; the main thread blocked in a synchronized block because another thread holds that lock; and deadlock, where two threads each hold what the other needs and wait for each other forever. The last two are especially tricky because the main thread is not busy: it is only waiting. [[src:ad-anr]]''')
    B(C, S_, 2, 'p', '''Vì sao máy dev không tái hiện được: thời gian giữ khóa phụ thuộc vào việc bên trong khối, ở đây là một lời gọi mạng. Mạng nhanh thì khóa nhả kịp; mạng chậm của người dùng mới đẩy thời gian chờ quá 5 giây. Cơ chế khóa, deadlock và vì sao không nên giữ khóa khi làm việc chậm được nói kỹ ở chương "Luồng, khóa, ANR và deadlock" của track Thiết kế hệ thống phía mobile.''',
      '''Why the dev device cannot reproduce it: how long the lock is held depends on the work inside the block, here a network call. On a fast network the lock is released in time; only the user\'s slow network pushes the wait past 5 seconds. Locks, deadlock and why not to hold a lock during slow work are covered in "Threads, locks, ANRs and deadlock" in the Mobile System Design track.''')

    S_ = 'read'
    a(C + '.sec.%s.title' % S_, '''Đọc trace của ANR''', '''Reading an ANR trace''')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'kt', '''"main" prio=5 tid=1 Blocked
  at vn.henkham.data.BookingRepo.save(BookingRepo.kt:21)
  - waiting to lock <0x0a1b> (a java.lang.Object) held by thread 24
  at vn.henkham.ui.EditViewModel.onSave(EditViewModel.kt:40)
  ...
"SyncWorker" prio=5 tid=24 Native
  at java.net.SocketInputStream.socketRead0(Native method)
  ...
  at vn.henkham.data.BookingRepo.sync(BookingRepo.kt:30)
  - locked <0x0a1b> (a java.lang.Object)''')
    B(C, S_, 2, 'p', '''Đọc từ luồng main: trạng thái (Blocked là chờ khóa, Waiting là chờ một điều kiện, Native hay Runnable là đang chạy), rồi dòng "waiting to lock <địa chỉ> held by …". Tìm luồng có dòng "locked <cùng địa chỉ>": đó là luồng giữ khóa, và stack của nó cho biết nó đang làm gì trong lúc giữ. Trace lấy từ Play Console (Android vitals), từ Firebase Crashlytics, hay từ bug report và thư mục /data/anr trên máy thử. [[src:ad-anr]] [[src:ad-anr-diagnose]]''',
      '''Read from the main thread: its state (Blocked means waiting for a lock, Waiting means waiting for a condition, Native or Runnable means running), then the line "waiting to lock <address> held by …". Find the thread with "locked <same address>": that is the holder, and its stack tells you what it is doing while holding. Traces come from Play Console (Android vitals), Firebase Crashlytics, or a bug report and the /data/anr directory on a test device. [[src:ad-anr]] [[src:ad-anr-diagnose]]''')
    B(C, S_, 3, 'note', '''Có những cụm ANR mà luồng main đang ở nativePollOnce, tức đang rảnh: với ANR do input, tài liệu nói chúng thường không hành động được, vì trace được chụp khi việc gây chậm đã xong. Ưu tiên các cụm có stack chỉ vào mã của app. [[src:ad-anr-diagnose]]''',
      '''Some ANR clusters show the main thread in nativePollOnce, that is, idle: for input ANRs the documentation says these are generally not actionable, because the trace was taken after the slow work had finished. Prioritise clusters whose stacks point into the app\'s code. [[src:ad-anr-diagnose]]''')
    B(C, S_, 3, 'kind', 'pitfall')

    S_ = 'strict'
    a(C + '.sec.%s.title' % S_, '''StrictMode: bắt sớm trên máy dev''', '''StrictMode: catching it early on the dev device''')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'kt', '''class HenKhamApp : Application() {
    override fun onCreate() {
        super.onCreate()
        if (BuildConfig.DEBUG) {
            StrictMode.setThreadPolicy(StrictMode.ThreadPolicy.Builder().detectAll().penaltyLog().build())
            StrictMode.setVmPolicy(StrictMode.VmPolicy.Builder().detectAll().penaltyLog().build())
        }
    }
}''')
    B(C, S_, 2, 'p', '''ThreadPolicy bắt những việc trên luồng hiện tại, chủ yếu đọc ghi đĩa và gọi mạng trên luồng main; VmPolicy bắt vấn đề cả tiến trình, như tài nguyên mở mà không đóng. penaltyLog ghi vi phạm kèm stack trace vào Logcat. StrictMode không bắt được mọi truy cập và không phải cơ chế bảo mật; nó là lưới báo sớm. Không phải vi phạm nào cũng phải sửa, nhưng gọi mạng trên luồng main thì gần như luôn là vấn đề. [[src:ad-strictmode]]''',
      '''ThreadPolicy catches things on the current thread, mainly disk and network access on the main thread; VmPolicy catches process-wide problems, such as resources opened and never closed. penaltyLog writes each violation with a stack trace to Logcat. StrictMode does not catch every access and is not a security mechanism; it is an early-warning net. Not every violation must be fixed, but network calls on the main thread are almost always a problem. [[src:ad-strictmode]]''')

    S_ = 'bugs'
    a(C + '.sec.%s.title' % S_, '''Hai lỗi hay gặp''', '''Two common bugs''')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'bug', '''ANR lúc mở app trên máy cũ; trace cho thấy main Blocked trong một hàm khởi tạo của thư viện DI.''', '''An ANR at app start on old phones; the trace shows main Blocked inside a DI library initialiser.''')
    B(C, S_, 1, 'cause', '''Một luồng nền đang khởi tạo cùng singleton và giữ khóa của nó trong lúc đọc tệp cấu hình lớn từ đĩa.''', '''A background thread is initialising the same singleton and holds its lock while reading a large config file from disk.''')
    B(C, S_, 1, 'fix', '''Đọc tệp trước, ngoài phần khởi tạo có khóa; hoặc khởi tạo lười trên luồng nền, và đừng để luồng main lấy singleton đó lúc khởi động.''', '''Read the file first, outside the locked initialisation; or initialise lazily on a background thread, and keep the main thread from touching that singleton at start-up.''')
    B(C, S_, 2, 'bug', '''Bật StrictMode với penaltyDeath trong mọi bản build; bản phát hành crash trên vài máy.''', '''StrictMode with penaltyDeath turned on in every build; the release crashes on some phones.''')
    B(C, S_, 2, 'cause', '''StrictMode là công cụ khi phát triển; một vi phạm vô hại (ví dụ một lần đọc nhỏ của thư viện) làm bản phát hành chết.''', '''StrictMode is a development tool; a harmless violation (say a small read inside a library) kills the release build.''')
    B(C, S_, 2, 'fix', '''Chỉ bật trong bản debug (if (BuildConfig.DEBUG)), dùng penaltyLog; xem vi phạm và quyết định sửa cái nào.''', '''Enable it only in debug builds (if (BuildConfig.DEBUG)), with penaltyLog; review the violations and decide which to fix.''')

    S_ = 'ex'
    a(C + '.sec.%s.title' % S_, '''Bài tập''', '''Exercise''')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'ex', '''Trace ANR: "main" tid=1 Blocked, waiting to lock <0x11> held by thread 31. "Uploader" tid=31 Blocked, waiting to lock <0x22> held by thread 1; trước đó luồng main đã "locked <0x22>". Đây là gì, và sửa theo hướng nào?''',
      '''An ANR trace: "main" tid=1 Blocked, waiting to lock <0x11> held by thread 31. "Uploader" tid=31 Blocked, waiting to lock <0x22> held by thread 1; earlier, main had "locked <0x22>". What is this, and which direction does the fix take?''')
    B(C, S_, 1, 'hint', '''Luồng nào giữ gì, và chờ gì?''', '''Which thread holds what, and waits for what?''')
    B(C, S_, 1, 'sol', '''Deadlock: main giữ 0x22 và chờ 0x11; Uploader giữ 0x11 và chờ 0x22; không bên nào nhả. Sửa: luôn lấy các khóa theo cùng một thứ tự ở mọi nơi, hoặc gộp thành một khóa, và tốt nhất là không để luồng main lấy khóa nào có thể bị giữ lâu.''',
      '''Deadlock: main holds 0x22 and waits for 0x11; Uploader holds 0x11 and waits for 0x22; neither lets go. Fix: always take the locks in the same order everywhere, or merge them into one, and ideally never let the main thread take a lock that can be held for long.''')

    S_ = 'recall'
    a(C + '.sec.%s.title' % S_, '''Tự trả lời''', '''Answer it yourself''')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'ask', '''Luồng main Blocked trong trace ANR. Bước tiếp theo là gì?''', '''The main thread is Blocked in an ANR trace. What is the next step?''')
    B(C, S_, 1, 'ans', '''Đọc dòng "waiting to lock … held by", tìm luồng giữ khóa đó và xem nó đang làm gì trong lúc giữ.''', '''Read the "waiting to lock … held by" line, find the thread holding that lock and see what it does while holding it.''')
    B(C, S_, 2, 'ask', '''StrictMode nên bật ở bản build nào, và để làm gì?''', '''Which builds should enable StrictMode, and why?''')
    B(C, S_, 2, 'ans', '''Bản debug, để bắt đọc ghi đĩa và gọi mạng trên luồng main ngay khi phát triển.''', '''Debug builds, to catch disk and network access on the main thread during development.''')

    for q, qv, qe, av, ae, wv, we in [
        ('q1', 'Hạn mặc định cho input trước khi ANR là bao nhiêu?', 'What is the default input deadline before an ANR?', '5 giây.', '5 seconds.',
         'Hạn của Service và BroadcastReceiver dài hơn và tùy phiên bản, tùy hãng.', 'Service and BroadcastReceiver deadlines are longer and vary by version and manufacturer.'),
        ('q2', 'Vì sao ANR do chờ khóa hay không tái hiện được trên máy dev?', 'Why does a lock-wait ANR often not reproduce on the dev device?', 'Thời gian giữ khóa phụ thuộc việc bên trong, như mạng; máy dev có mạng nhanh.', 'The holding time depends on the work inside, such as the network; the dev device has a fast network.',
         'Giả điều kiện của người dùng (mạng chậm) mới thấy.', 'Recreate the user\'s conditions (a slow network) to see it.'),
        ('q3', 'StrictMode có bắt được mọi truy cập đĩa và mạng không?', 'Does StrictMode catch every disk and network access?', 'Không; ví dụ truy cập qua JNI có thể lọt.', 'No; access through JNI, for example, can slip through.',
         'Nó là lưới báo sớm, không phải cơ chế bảo mật.', 'It is an early-warning net, not a security mechanism.')]:
        a(C + '.quiz.%s.q' % q, qv, qe); a(C + '.quiz.%s.a' % q, av, ae); a(C + '.quiz.%s.why' % q, wv, we)
