# Coroutines v2 · U3 Suspension hoạt động thế nào (Deep Dive, "How does suspension work?", tr. PDF 33–44) + chuỗi của sim coroutines.cont.
# Được dev/gen/coroutines_content.py nạp. Khung: docs/chapter-template-v2.md.

def add(a):
    def B(ch, sec, n, field, vi, en=None):
        a('%s.sec.%s.b.%02d.%s' % (ch, sec, n, field), vi, vi if en is None else en)
    m = lambda k, vi, en=None: a('m.cont.' + k, vi, en)

    # ---------------- sim coroutines.cont ----------------
    m('title', 'suspendCoroutine: ai giữ Continuation và ai gọi resume', 'suspendCoroutine: who holds the Continuation and who calls resume')
    m('overview', 'Chọn một cách resume ở ô "Cách resume", rồi bấm Step. Hàng trên là coroutine (đang chạy, hay đang suspend mà không giữ luồng nào); hai hàng dưới là luồng main và luồng phụ/scheduler. Câu hỏi chính: sau khi resume, phần còn lại của coroutine chạy trên luồng nào?',
      'Pick a way to resume in the "How to resume" box, then press Step. The top row is the coroutine (running, or suspended and holding no thread); the two rows below are the main thread and the helper/scheduler thread. The key question: after resume, which thread runs the rest of the coroutine?')
    m('wrapup', 'Suspend = coroutine trả luồng và để lại một Continuation. Không ai gọi `resume` thì coroutine dừng mãi. Gọi `resume` ở đâu thì (khi không có dispatcher) phần tiếp theo chạy ngay trên luồng đó. Hẹn giờ bằng một scheduler dùng chung thay vì một luồng ngủ cho mỗi lần chờ: đó là ý tưởng gốc của `delay`. Ở mã thật, dispatcher (như `Dispatchers.Main`) chặn lời resume và chuyển phần tiếp theo về đúng luồng của nó.',
      'Suspend = the coroutine gives up its thread and leaves a Continuation behind. If nobody calls `resume`, the coroutine stays stopped forever. Wherever `resume` is called (when there is no dispatcher), the rest runs right on that thread. Setting an alarm on a shared scheduler instead of one sleeping thread per wait is the original idea behind `delay`. In real code, a dispatcher (such as `Dispatchers.Main`) intercepts the resume and moves the continuation back to its own thread.')
    m('simp.1', '`suspend fun main` không có dispatcher; mô hình giữ đúng điều đó. Trong `viewModelScope`/`lifecycleScope`, `Dispatchers.Main` sẽ chuyển phần tiếp theo về luồng Main (học ở chương Dispatchers).', '`suspend fun main` has no dispatcher, and the model keeps that. In `viewModelScope`/`lifecycleScope`, `Dispatchers.Main` moves the continuation back to the Main thread (covered in the Dispatchers chapter).')
    m('simp.2', 'Ở chế độ "resume ngay", mô hình bỏ qua chi tiết: thư viện thấy kết quả đã có nên trả về luôn, không suspend.', 'In "resume immediately" mode the model skips the detail: the library sees the result is already there, so it returns at once without suspending.')
    m('ctl.hint', 'Mỗi lựa chọn là một đoạn mã trong chương. So sánh hàng luồng giữa "luồng mới + sleep" và "scheduler hẹn giờ".', 'Each option is a code snippet from the chapter. Compare the thread rows between "new thread + sleep" and "scheduler alarm".')
    m('ctl.how', 'Cách resume', 'How to resume')
    for k, vi, en in [('thread', 'Luồng mới ngủ 1 s rồi resume', 'A new thread sleeps 1 s, then resumes'), ('never', 'Không ai resume', 'Nobody resumes'),
                      ('now', 'Resume ngay trong lambda', 'Resume right inside the lambda'), ('sched', 'Scheduler hẹn giờ (delay tự viết)', 'Scheduler alarm (hand-made delay)'),
                      ('exc', 'resumeWithException', 'resumeWithException')]:
        m('ctl.how.' + k, vi, en)
    m('diagramTitle', 'Coroutine và các luồng theo thời gian', 'The coroutine and the threads over time')
    m('diagramDesc', 'Hàng coroutine, hàng luồng main, hàng luồng phụ hoặc scheduler', 'A coroutine row, a main-thread row, and a helper or scheduler thread row')
    m('n.co', 'Coroutine của main', 'The main coroutine')
    m('n.th0', 'Luồng main', 'Main thread')
    m('n.th1', 'Luồng phụ / scheduler', 'Helper / scheduler thread')
    m('axis', 'ms (minh hoạ; 1000 ms trong mã) →', 'ms (illustrative; 1000 ms in the code) →')
    m('scope.th0', 'luồng main', 'main thread')
    m('scope.th1', 'luồng phụ / scheduler', 'helper / scheduler thread')
    m('scope.none', 'không luồng nào', 'no thread')
    m('met.on', 'Coroutine đang chạy trên', 'Coroutine is running on')
    m('met.out', 'Dòng in gần nhất', 'Last printed line')
    m('bar.wait', 'suspend: không giữ luồng nào', 'suspended: holds no thread')
    m('bar.timer', 'đã hẹn giờ (luồng rảnh, không bị chặn)', 'alarm set (thread idle, not blocked)')
    m('lbl.co', 'coroutine', 'coroutine')
    m('lbl.wait', 'suspend', 'suspended')
    m('lbl.timer', 'hẹn giờ', 'alarm set')
    for k, vi, en in [('run', 'đang chạy', 'running'), ('wait', 'đang suspend', 'suspended'), ('done', 'đã xong', 'finished'), ('busy', 'đang chạy coroutine', 'running the coroutine'),
                      ('free', 'rảnh', 'free'), ('blocked', 'bị chặn (sleep)', 'blocked (sleep)'), ('timer', 'giữ hẹn giờ', 'holding an alarm')]:
        m('st.' + k, vi, en)
    for k, vi, en in [('none', '(chưa có)', '(nothing yet)'), ('before', 'Before', 'Before'), ('beforeToo', 'Before too', 'Before too'), ('after', 'After', 'After'),
                      ('suspended', 'Suspended', 'Suspended'), ('resumed', 'Resumed', 'Resumed'), ('caught', 'Caught!', 'Caught!')]:
        m('o.' + k, vi, en)
    for k, vi, en in [('th0', 'luồng main', 'main thread'), ('th1', 'luồng phụ / scheduler', 'helper / scheduler thread'), ('none', 'không luồng nào', 'no thread')]:
        m('thr.' + k, vi, en)
    S = [
        ('before', 'In "Before"', 'Print "Before"', 'Coroutine của `main` chạy trên luồng main và in "Before".', 'The `main` coroutine runs on the main thread and prints "Before".'),
        ('lambda', 'Lambda của suspendCoroutine nhận continuation', 'The suspendCoroutine lambda receives the continuation',
         '`suspendCoroutine` gọi lambda NGAY TRƯỚC khi suspend, đưa vào đối tượng `continuation`. Lambda in "Before too" nhưng không cất continuation ở đâu cả.', '`suspendCoroutine` calls the lambda RIGHT BEFORE suspending, passing in the `continuation` object. The lambda prints "Before too" but stores the continuation nowhere.'),
        ('suspended', 'Coroutine suspend: không giữ luồng nào', 'The coroutine suspends: it holds no thread',
         'Coroutine dừng lại. Luồng main được thả ra; hàng coroutine có viền đứt vì không luồng nào đang chạy nó.', 'The coroutine stops. The main thread is released; the coroutine row is dashed because no thread is running it.'),
        ('hang', 'Không ai resume: "After" không bao giờ in', 'Nobody resumes: "After" is never printed',
         'Không còn tham chiếu nào tới continuation, nên không ai có thể gọi `resume`. Coroutine dừng mãi; chương trình không kết thúc vì `main` chưa xong.', 'No reference to the continuation remains, so nobody can call `resume`. The coroutine stays stopped forever; the program does not end because `main` never finishes.'),
        ('lambdaNow', 'resume(Unit) ngay trong lambda', 'resume(Unit) right inside the lambda',
         'Lambda gọi `continuation.resume(Unit)` trước khi `suspendCoroutine` kịp suspend. Thư viện thấy kết quả đã có nên trả về luôn: không có suspension thật.', 'The lambda calls `continuation.resume(Unit)` before `suspendCoroutine` gets to suspend. The library sees the result is already there and returns at once: there is no real suspension.'),
        ('after', 'In "After"', 'Print "After"', 'Coroutine chạy tiếp sau `suspendCoroutine` và in "After".', 'The coroutine continues after `suspendCoroutine` and prints "After".'),
        ('done', 'Coroutine kết thúc', 'The coroutine finishes', '`main` chạy xong; chương trình kết thúc.', '`main` finishes; the program ends.'),
        ('lambdaThread', 'Lambda khởi động một luồng mới, giữ continuation', 'The lambda starts a new thread that holds the continuation',
         'Lambda tạo luồng mới. Lambda của luồng đó "bắt" (capture) biến `continuation`, nên continuation còn được giữ sau khi coroutine suspend.', 'The lambda creates a new thread. That thread\'s lambda captures the `continuation` variable, so the continuation is still held after the coroutine suspends.'),
        ('sleep', 'Luồng phụ ngủ 1 giây (bị chặn)', 'The helper thread sleeps 1 second (blocked)',
         'Coroutine không tốn luồng nào trong lúc chờ, nhưng luồng phụ bị chặn suốt 1 giây chỉ để đếm giờ. Mỗi lần chờ lại tốn một luồng như vậy.', 'The coroutine uses no thread while waiting, but the helper thread is blocked for a whole second just to count time. Every wait would cost another such thread.'),
        ('resumeThread', 'resume(Unit): "After" chạy TRÊN luồng phụ', 'resume(Unit): "After" runs ON the helper thread',
         'Luồng phụ gọi `continuation.resume(Unit)`. Không có dispatcher nào chuyển việc đi chỗ khác, nên phần còn lại của coroutine (in "After") chạy ngay bên trong lời gọi `resume`, trên chính luồng phụ.', 'The helper thread calls `continuation.resume(Unit)`. No dispatcher moves the work elsewhere, so the rest of the coroutine (printing "After") runs right inside the `resume` call, on the helper thread itself.'),
        ('resumed', '`resume` trả về; luồng phụ in "Resumed"', '`resume` returns; the helper thread prints "Resumed"',
         'Chỉ khi coroutine chạy xong (hoặc suspend lần nữa), lời gọi `resume` mới trả về. Vì vậy "After" in TRƯỚC "Resumed".', 'Only when the coroutine finishes (or suspends again) does the `resume` call return. That is why "After" prints BEFORE "Resumed".'),
        ('schedule', 'delay(1000): đặt hẹn giờ rồi suspend', 'delay(1000): set an alarm, then suspend',
         '`delay` tự viết gọi `suspendCoroutine`; lambda đặt một tác vụ hẹn giờ trên scheduler dùng chung: "sau 1000 ms, gọi `cont.resume(Unit)`".', 'The hand-made `delay` calls `suspendCoroutine`; the lambda schedules a task on a shared scheduler: "after 1000 ms, call `cont.resume(Unit)`".'),
        ('fire', 'Hết giờ: scheduler gọi resume', 'Time is up: the scheduler calls resume',
         'Luồng scheduler gọi `cont.resume(Unit)`, và coroutine in "After" trên luồng scheduler (vẫn không có dispatcher). Trong suốt lúc chờ, không luồng nào bị chặn.', 'The scheduler thread calls `cont.resume(Unit)`, and the coroutine prints "After" on the scheduler thread (still no dispatcher). During the whole wait, no thread was blocked.'),
        ('excLambda', 'Lambda nhận continuation', 'The lambda receives the continuation', 'Bên trong `try`, `suspendCoroutine` gọi lambda với continuation.', 'Inside `try`, `suspendCoroutine` calls the lambda with the continuation.'),
        ('excThrow', 'resumeWithException: ném ra tại điểm suspension', 'resumeWithException: thrown at the suspension point',
         '`cont.resumeWithException(MyException())` làm `suspendCoroutine` ném `MyException` ngay tại chỗ gọi nó, như một hàm bình thường ném lỗi.', '`cont.resumeWithException(MyException())` makes `suspendCoroutine` throw `MyException` right where it was called, just like an ordinary function throwing.'),
        ('excCatch', 'catch bắt được: in "Caught!"', 'catch handles it: print "Caught!"', '`try/catch` quanh điểm suspension bắt exception như với mã đồng bộ.', 'A `try/catch` around the suspension point catches the exception just like with synchronous code.'),
    ]
    for sid, tv, te, xv, xe in S:
        m('s.%s.title' % sid, tv, te); m('s.%s.explain' % sid, xv, xe)
        m('ev.' + sid, tv, te)
    for k, vi, en in [
        ('lambda', 'Lambda chạy trước khi suspend: đây là chỗ duy nhất để cất continuation hoặc hẹn ai đó resume nó.', 'The lambda runs before suspending: it is the only place to store the continuation or arrange for someone to resume it.'),
        ('free', 'Suspend: coroutine không còn chạy trên luồng nào. Chỉ đối tượng continuation còn lại.', 'Suspended: the coroutine no longer runs on any thread. Only the continuation object remains.'),
        ('hang', 'Mất continuation = mất cách duy nhất để chạy tiếp. Ở mã thật đây là coroutine treo vĩnh viễn (và có thể rò bộ nhớ).', 'Losing the continuation means losing the only way to continue. In real code this is a coroutine that hangs forever (and may leak memory).'),
        ('noSuspend', 'Kết quả đã có trước khi kịp suspend → không suspend. Tối ưu này làm hàm suspend "nhanh" khi dữ liệu có sẵn (ví dụ cache).', 'The result arrived before suspending → no suspension. This optimization makes a suspending function "fast" when the data is already there (for example, a cache).'),
        ('sleepCost', 'Hai luồng cho một lần chờ: cách này đúng nhưng phí. Cách scheduler hẹn giờ dùng một luồng cho mọi lần chờ.', 'Two threads for one wait: correct but wasteful. The scheduler-alarm approach uses one thread for every wait.'),
        ('onThread', 'Bẫy: không có dispatcher thì phần sau `resume` chạy trên luồng gọi `resume`. Trên Android, đây là lý do mã sau callback có thể chạy trên luồng nền nếu bạn tự viết continuation mà không có `Dispatchers.Main`.', 'Trap: without a dispatcher, the code after `resume` runs on the thread that calls `resume`. On Android, this is why code after a callback can end up on a background thread if you write continuations by hand without `Dispatchers.Main`.'),
        ('order', '"After" trước "Resumed": `resume` chạy coroutine tới điểm suspend kế tiếp (hoặc tới hết) rồi mới trả về.', '"After" before "Resumed": `resume` runs the coroutine up to its next suspension point (or to the end) before returning.'),
        ('schedule', 'Một luồng scheduler phục vụ mọi lần delay. Đây là ý tưởng gốc của `delay` trong kotlinx.coroutines; bản hiện tại phức tạp hơn (hỗ trợ test, dispatcher).', 'One scheduler thread serves every delay. This is the original idea behind `delay` in kotlinx.coroutines; the current version is more complex (test support, dispatchers).'),
        ('onSched', 'Phần sau `delay` tự viết chạy trên luồng scheduler. `delay` thật dùng dispatcher của coroutine để quay về đúng luồng.', 'The code after the hand-made `delay` runs on the scheduler thread. The real `delay` uses the coroutine\'s dispatcher to return to the right thread.'),
        ('exc', 'Exception đi ra từ điểm suspension như từ một lời gọi hàm, nên `try/catch` và `finally` hoạt động y như mã đồng bộ.', 'The exception comes out of the suspension point as if from a function call, so `try/catch` and `finally` work exactly as in synchronous code.')]:
        m('co.' + k, vi, en)
    a('cap.cont', 'Hàng trên: coroutine (thanh liền = đang chạy, ghi tên luồng; viền đứt = suspend, không giữ luồng). Hai hàng dưới: luồng main và luồng phụ/scheduler (gạch chéo = bị chặn bởi sleep). Theo dõi xem sau resume, coroutine chạy trên hàng luồng nào.',
      'Top row: the coroutine (solid = running, labelled with its thread; dashed = suspended, holding no thread). Bottom rows: the main thread and the helper/scheduler thread (hatched = blocked by sleep). Watch which thread row runs the coroutine after resume.')

    # ---------------- chương U3 ----------------
    C = 'u3'
    a(C + '.title', 'Suspension hoạt động thế nào: Continuation và resume', 'How suspension works: Continuation and resume')
    a(C + '.essence',
      'Suspend một coroutine là dừng nó giữa chừng và đổi lấy một đối tượng `Continuation`: "phiếu" để chạy tiếp từ đúng chỗ đó. Coroutine đang suspend không chạy trên luồng nào và gần như không tốn tài nguyên.\n'
      '`suspendCoroutine { continuation -> … }` cho bạn cầm continuation ngay trước khi suspend. Ai gọi `continuation.resume(value)` thì coroutine chạy tiếp và nhận `value`; `resumeWithException(e)` thì `e` bị ném ra tại điểm suspend. Không ai gọi thì coroutine dừng mãi.\n'
      'Toàn bộ thư viện (delay, Retrofit suspend, Room, withContext…) được xây trên cơ chế này. Hiểu nó thì đọc được mọi hàm suspend và biến được mọi API callback thành hàm suspend.',
      'Suspending a coroutine means stopping it midway in exchange for a `Continuation` object: a "ticket" to continue from that exact point. A suspended coroutine runs on no thread and costs almost nothing.\n'
      '`suspendCoroutine { continuation -> … }` hands you the continuation right before suspending. Whoever calls `continuation.resume(value)` makes the coroutine continue and receive `value`; with `resumeWithException(e)`, `e` is thrown at the suspension point. If nobody calls either, the coroutine stays stopped forever.\n'
      'The whole library (delay, Retrofit suspend functions, Room, withContext…) is built on this mechanism. Understand it and you can read any suspending function and turn any callback API into one.')
    a(C + '.goal.g1', 'Đã thấy điều xảy ra ngay sau khi lambda nhận continuation', 'Saw what happens right after the lambda receives the continuation')
    a(C + '.goal.g2', 'Đã xem hết một cách resume', 'Went through one way of resuming to the end')

    S = 'recap'
    a(C + '.sec.%s.title' % S, 'Ôn nhanh chương trước', 'Quick review of the previous chapter')
    B(C, S, 1, 'ask', 'Trong `sequence { }`, giữa hai lần `next()`, biến cục bộ của khối được giữ ở đâu? Khối có chiếm luồng không?', 'In `sequence { }`, between two `next()` calls, where are the block\'s local variables kept? Does the block occupy a thread?')
    B(C, S, 1, 'ans', 'Trong đối tượng continuation trên heap, cùng với vị trí đang dừng. Khối không chiếm luồng nào; nó chỉ chạy khi `next()` gọi `resume` trên continuation đó.', 'In the continuation object on the heap, together with the stopping point. The block occupies no thread; it runs only when `next()` calls `resume` on that continuation.')

    S = 'save'
    a(C + '.sec.%s.title' % S, 'Suspend giống lưu game', 'Suspending is like saving a game')
    a(C + '.sec.%s.badge' % S, 'stable')
    B(C, S, 1, 'note',
      'Suspend giống lưu game ở một checkpoint rồi tắt máy: bạn và máy tính đều rảnh làm việc khác. Lúc sau mở lại bản lưu và chơi tiếp đúng chỗ cũ. Khi suspend, coroutine trả về một `Continuation`: đó là "bản lưu".\n'
      'Chỗ khớp: bản lưu giữ đúng vị trí và trạng thái; trong lúc "tắt máy" không tốn tài nguyên chạy. Chỗ không khớp: (1) khi resume, bạn có thể đưa vào một giá trị (kết quả mạng) hoặc một exception, điều mà game thường không cho; (2) một bản lưu continuation chỉ được dùng đúng một lần.',
      'Suspending is like saving a game at a checkpoint and switching the computer off: both you and the computer are free to do other things. Later you load the save and continue from the same spot. When it suspends, a coroutine hands back a `Continuation`: that is the "save".\n'
      'Where it matches: the save keeps the exact position and state, and nothing is running while it is "switched off". Where it does not: (1) on resume you can pass in a value (a network result) or an exception, which games usually do not allow; (2) a continuation "save" can be used exactly once.')
    B(C, S, 1, 'kind', 'analogy')
    B(C, S, 2, 'p',
      'Đây là khác biệt lớn với luồng: luồng không lưu lại được, chỉ có thể bị chặn (đứng chờ, giữ stack và tài nguyên hệ điều hành). Coroutine đang suspend không tiêu tài nguyên chạy. Nó có thể được resume trên một luồng khác. Về lý thuyết, continuation còn có thể được tuần tự hoá rồi resume sau.',
      'This is a big difference from threads: a thread cannot be saved, only blocked (standing and waiting, holding its stack and operating-system resources). A suspended coroutine consumes no running resources. It can be resumed on a different thread. In theory, a continuation could even be serialized and resumed later.')

    S = 'suspend'
    a(C + '.sec.%s.title' % S, 'suspendCoroutine: dừng coroutine bằng tay', 'suspendCoroutine: stopping a coroutine by hand')
    a(C + '.sec.%s.badge' % S, 'stable')
    B(C, S, 1, 'p',
      'Hàm suspend là hàm có thể suspend một coroutine, nên phải được gọi từ một coroutine hoặc từ hàm suspend khác: cuối cùng phải có một coroutine để mà dừng. Cách đơn giản nhất để có coroutine là `suspend fun main()`: Kotlin tự chạy `main` trong một coroutine.\n'
      'Để dừng coroutine giữa hai lệnh in, dùng `suspendCoroutine` của thư viện chuẩn ([[src:kt-suspendco]]):',
      'A suspending function is a function that can suspend a coroutine, so it must be called from a coroutine or from another suspending function: in the end there has to be a coroutine to stop. The simplest way to get a coroutine is `suspend fun main()`: Kotlin runs `main` in a coroutine for you.\n'
      'To stop the coroutine between two prints, use the standard library\'s `suspendCoroutine` ([[src:kt-suspendco]]):')
    B(C, S, 2, 'kt', 'suspend fun main() {\n    println("Before")\n    suspendCoroutine<Unit> { }\n    println("After")\n}')
    B(C, S, 3, 'predict', 'Chương trình in gì, và có kết thúc không?', 'What does the program print, and does it end?')
    B(C, S, 3, 'ans', 'Chỉ in "Before", và chương trình không kết thúc. Coroutine đã suspend sau "Before" nhưng không ai resume nó: game đã lưu mà không bao giờ được mở lại.', 'It prints only "Before", and the program never ends. The coroutine suspended after "Before" but nobody resumes it: the game was saved and never loaded again.')
    B(C, S, 4, 'p', 'Vậy continuation ở đâu? Để ý `suspendCoroutine` nhận một lambda `{ }`. Lambda này được gọi NGAY TRƯỚC khi coroutine dừng, với continuation làm tham số. Giống `let` hay `apply`, hàm gọi lambda của bạn ngay tại chỗ.\nChờ tới sau `suspendCoroutine` thì đã muộn, vì coroutine đã dừng rồi. Nên lambda là chỗ duy nhất để cất continuation đi, hoặc sắp xếp ai sẽ resume nó.\nQuy tắc dễ nhớ: lambda của `suspendCoroutine` là khoảnh khắc "trao chìa khóa trước khi rời nhà".',
      'So where is the continuation? Notice that `suspendCoroutine` takes a lambda `{ }`. This lambda is called RIGHT BEFORE the coroutine stops, with the continuation as its parameter. Like `let` or `apply`, the function calls your lambda right there.\nWaiting until after `suspendCoroutine` would be too late, because the coroutine has already stopped. So the lambda is the only place to store the continuation, or to arrange who will resume it.\nRule of thumb: the `suspendCoroutine` lambda is the moment of "handing over the key before leaving the house".')
    B(C, S, 5, 'kt', 'suspend fun main() {\n    println("Before")\n    suspendCoroutine<Unit> { continuation ->\n        println("Before too")\n    }\n    println("After")\n}\n// Before\n// Before too')

    S = 'resume'
    a(C + '.sec.%s.title' % S, 'resume: ai gọi, chạy trên luồng nào', 'resume: who calls it, and on which thread')
    a(C + '.sec.%s.badge' % S, 'stable')
    B(C, S, 1, 'p', 'Gọi `resume` ngay trong lambda thì "After" được in:', 'Calling `resume` right inside the lambda makes "After" print:')
    B(C, S, 2, 'kt', 'suspend fun main() {\n    println("Before")\n    suspendCoroutine<Unit> { continuation ->\n        continuation.resume(Unit)\n    }\n    println("After")\n}\n// Before\n// After')
    B(C, S, 3, 'note',
      'Từ Kotlin 1.3, `Continuation` chỉ có một hàm `resumeWith(result: Result<T>)` cùng thuộc tính `context`. `resume(value)` và `resumeWithException(e)` là extension function của thư viện chuẩn, gọi `resumeWith(Result.success(value))` và `resumeWith(Result.failure(e))` ([[src:kt-continuation]]).\n'
      'Khi resume ngay trong lambda như trên, thực tế không có suspension nào: `suspendCoroutine` thấy kết quả đã có nên trả về luôn.',
      'Since Kotlin 1.3, `Continuation` has just one function, `resumeWith(result: Result<T>)`, plus a `context` property. `resume(value)` and `resumeWithException(e)` are standard-library extension functions that call `resumeWith(Result.success(value))` and `resumeWith(Result.failure(e))` ([[src:kt-continuation]]).\n'
      'When you resume right inside the lambda as above, there is actually no suspension: `suspendCoroutine` sees the result is already there and returns at once.')
    B(C, S, 4, 'kt',
      'public interface Continuation<in T> {\n    public val context: CoroutineContext\n    public fun resumeWith(result: Result<T>)\n}\n\ninline fun <T> Continuation<T>.resume(value: T): Unit =\n    resumeWith(Result.success(value))\n\ninline fun <T> Continuation<T>.resumeWithException(exception: Throwable): Unit =\n    resumeWith(Result.failure(exception))')
    B(C, S, 5, 'p', 'Thú vị hơn: để một luồng khác resume sau 1 giây. Lambda của `thread { }` "bắt" biến `continuation`, nên nó còn giữ continuation sau khi coroutine đã suspend:', 'More interesting: let another thread resume after 1 second. The `thread { }` lambda captures the `continuation` variable, so it still holds the continuation after the coroutine has suspended:')
    B(C, S, 6, 'kt', 'suspend fun main() {\n    println("Before")\n    suspendCoroutine<Unit> { continuation ->\n        thread {\n            println("Suspended")\n            Thread.sleep(1000)\n            continuation.resume(Unit)\n            println("Resumed")\n        }\n    }\n    println("After")\n}')
    B(C, S, 7, 'predict', 'Thứ tự in bốn dòng Before, Suspended, After, Resumed là gì? "After" được in trên luồng nào?', 'In what order are the four lines Before, Suspended, After, Resumed printed? On which thread is "After" printed?')
    B(C, S, 7, 'ans', 'Before → Suspended → (1 giây) → After → Resumed. "After" in trên luồng phụ (luồng gọi `resume`), vì `suspend fun main` không có dispatcher. `resume` chạy phần còn lại của coroutine ngay bên trong nó rồi mới trả về, nên "Resumed" đứng sau "After". Chọn "Luồng mới ngủ 1 s" trong mô phỏng ngay dưới để xem từng bước.', 'Before → Suspended → (1 second) → After → Resumed. "After" is printed on the helper thread (the one calling `resume`), because `suspend fun main` has no dispatcher. `resume` runs the rest of the coroutine inside itself before returning, so "Resumed" comes after "After". Pick "A new thread sleeps 1 s" in the simulation just below to see each step.')

    S = 'delay'
    a(C + '.sec.%s.title' % S, 'Tự viết delay: hẹn giờ thay vì ngủ', 'Writing delay yourself: an alarm instead of sleeping')
    a(C + '.sec.%s.badge' % S, 'stable impl')
    B(C, S, 1, 'p', 'Cách dùng luồng ở trên chạy đúng, nhưng nó tạo cả một luồng chỉ để ngủ 1 giây rồi bỏ đi. Luồng thì đắt, sao phải phí?\nTốt hơn là đặt một "đồng hồ báo thức". Trên JVM có `ScheduledExecutorService`: một luồng hẹn giờ dùng chung, nhận lời dặn "sau X ms thì gọi `resume`". Gói lại thành một hàm, ta có `delay`:',
      'The thread approach above works, but it creates a whole thread just to sleep for 1 second and then throws it away. Threads are expensive, so why waste one?\nBetter to set an "alarm clock". On the JVM there is `ScheduledExecutorService`: one shared timer thread that takes the instruction "after X ms, call `resume`". Wrap that in a function and you get `delay`:')
    B(C, S, 2, 'kt',
      'private val executor = Executors.newSingleThreadScheduledExecutor {\n    Thread(it, "scheduler").apply { isDaemon = true }\n}\n\nsuspend fun delay(timeMillis: Long): Unit =\n    suspendCoroutine { cont ->\n        executor.schedule({ cont.resume(Unit) }, timeMillis, TimeUnit.MILLISECONDS)\n    }\n\nsuspend fun main() {\n    println("Before")\n    delay(1000)\n    println("After")\n}\n// Before\n// (1 giây)\n// After',
      'private val executor = Executors.newSingleThreadScheduledExecutor {\n    Thread(it, "scheduler").apply { isDaemon = true }\n}\n\nsuspend fun delay(timeMillis: Long): Unit =\n    suspendCoroutine { cont ->\n        executor.schedule({ cont.resume(Unit) }, timeMillis, TimeUnit.MILLISECONDS)\n    }\n\nsuspend fun main() {\n    println("Before")\n    delay(1000)\n    println("After")\n}\n// Before\n// (1 second)\n// After')
    B(C, S, 3, 'p', 'Executor vẫn dùng một luồng, nhưng chỉ MỘT luồng cho mọi coroutine gọi `delay`. Tốt hơn nhiều so với chặn một luồng cho mỗi lần chờ.\nMarcin Moskała cho biết đây chính là cách `delay` của kotlinx.coroutines từng được viết. Bản hiện tại phức tạp hơn, chủ yếu để kiểm thử được với thời gian ảo, nhưng ý cốt lõi giữ nguyên. Trong bản thật, việc hẹn giờ do dispatcher (nơi coroutine chạy) đảm nhận qua interface `Delay`, và phần mã sau `delay` quay về đúng dispatcher đó ([[src:kx-delay]]).\nQuy tắc dễ nhớ: `delay` là đặt báo thức rồi đi làm việc khác; `Thread.sleep` là ngồi nhìn đồng hồ.',
      "The executor still uses a thread, but just ONE thread for every coroutine that calls `delay`. That is far better than blocking a thread for every wait.\nMarcin Moskała explains that this is exactly how kotlinx.coroutines' `delay` used to be written. The current version is more complex, mainly so it can be tested with virtual time, but the core idea is the same. In the real version, the dispatcher (where the coroutine runs) does the scheduling through the `Delay` interface, and the code after `delay` returns to that same dispatcher ([[src:kx-delay]]).\nRule of thumb: `delay` is setting an alarm and going off to do other things; `Thread.sleep` is sitting and staring at the clock.")

    S = 'value'
    a(C + '.sec.%s.title' % S, 'Resume với một giá trị: biến callback thành hàm suspend', 'Resuming with a value: turning a callback into a suspending function')
    a(C + '.sec.%s.badge' % S, 'stable')
    B(C, S, 1, 'p',
      '`Unit` trong `suspendCoroutine<Unit>` và trong `resume(Unit)` không trùng nhau ngẫu nhiên. Kiểu đó là kiểu giá trị `suspendCoroutine` trả về, đồng thời là tham số kiểu của `Continuation`. Giá trị bạn đưa vào `resume` chính là giá trị mà `suspendCoroutine` trả ra:',
      'The `Unit` in `suspendCoroutine<Unit>` and in `resume(Unit)` is no coincidence. That type is the type `suspendCoroutine` returns, and also the type parameter of the `Continuation`. The value you pass to `resume` is exactly the value `suspendCoroutine` returns:')
    B(C, S, 2, 'kt', 'suspend fun main() {\n    val i: Int = suspendCoroutine<Int> { cont -> cont.resume(42) }\n    println(i) // 42\n    val str: String = suspendCoroutine<String> { cont -> cont.resume("Some text") }\n    println(str) // Some text\n}')
    B(C, S, 3, 'p', 'Đây là trường hợp thực tế nhất. Coroutine chạy logic tới chỗ cần dữ liệu, ví dụ phản hồi từ API. Không có coroutine, luồng phải ngồi chờ; với luồng Main trên Android thì không được phép, vì màn hình sẽ đứng.\nCó coroutine thì khác. Nó suspend và đưa continuation cho thư viện mạng, kèm lời dặn: "có dữ liệu thì gửi vào `resume`". Luồng đi làm việc khác. Dữ liệu về, coroutine chạy tiếp đúng chỗ đã dừng, với dữ liệu trong tay.\nHình dung: để lại số điện thoại ở quầy sửa đồ thay vì đứng chờ; sửa xong người ta gọi, bạn quay lại đúng quầy đó. Đây là cách gói một API callback thành hàm suspend:',
      'This is the most practical case. A coroutine runs its logic up to the point where it needs data, say an API response. Without coroutines, the thread would have to sit and wait; on Android\'s Main thread that is not allowed, because the screen would freeze.\nWith coroutines it is different. The coroutine suspends and hands the continuation to the network library with the instruction: "when you have the data, send it to `resume`". The thread goes off to other work. When the data arrives, the coroutine continues exactly where it stopped, data in hand.\nPicture leaving your phone number at a repair counter instead of standing there; when it is fixed they call, and you come back to the same counter. This is how you wrap a callback API into a suspending function:')
    B(C, S, 4, 'kt',
      'suspend fun requestUser(): User =\n    suspendCancellableCoroutine { cont ->\n        requestUser { user ->          // API callback cũ\n            cont.resume(user)          // giá trị đi ra từ requestUser()\n        }\n    }\n\nsuspend fun main() {\n    println("Before")\n    val user = requestUser()           // suspend tới khi callback chạy\n    println(user)\n    println("After")\n}',
      'suspend fun requestUser(): User =\n    suspendCancellableCoroutine { cont ->\n        requestUser { user ->          // the old callback API\n            cont.resume(user)          // the value comes out of requestUser()\n        }\n    }\n\nsuspend fun main() {\n    println("Before")\n    val user = requestUser()           // suspends until the callback runs\n    println(user)\n    println("After")\n}')
    B(C, S, 5, 'note',
      'Ngày nay Retrofit, Room và nhiều thư viện đã có sẵn hàm suspend, nên hiếm khi phải tự gói. Khi cần, dùng `suspendCancellableCoroutine` (kotlinx.coroutines) thay vì `suspendCoroutine` ([[src:kx-scc]]). Nó hỗ trợ hủy: coroutine bị hủy thì lời chờ kết thúc ngay bằng `CancellationException`, và bạn đăng ký `cont.invokeOnCancellation { call.cancel() }` để huỷ luôn request bên dưới. Chương Hủy sẽ đi sâu.',
      'Today Retrofit, Room and many libraries already provide suspending functions, so you rarely need to wrap things yourself. When you do, use `suspendCancellableCoroutine` (kotlinx.coroutines) instead of `suspendCoroutine` ([[src:kx-scc]]). It supports cancellation: if the coroutine is cancelled, the wait ends immediately with a `CancellationException`, and you can register `cont.invokeOnCancellation { call.cancel() }` to cancel the underlying request too. The Cancellation chapter goes deeper.')
    B(C, S, 5, 'kind', 'android')

    S = 'exception'
    a(C + '.sec.%s.title' % S, 'Resume với exception', 'Resuming with an exception')
    a(C + '.sec.%s.badge' % S, 'stable')
    B(C, S, 1, 'p', 'Hàm nào cũng có thể trả về giá trị hoặc ném exception, và `suspendCoroutine` cũng vậy. Gọi `resume(x)` thì nó trả về `x`. Gọi `resumeWithException(e)` thì `e` được ném ra, về mặt khái niệm, từ đúng điểm coroutine đã dừng. Nhờ vậy lỗi mạng rơi vào `try/catch` hệt như mã đồng bộ.\nQuy tắc dễ nhớ: với hàm suspend, `resume` là "trả về", `resumeWithException` là "ném lỗi".',
      'Every function can return a value or throw an exception, and `suspendCoroutine` is no different. Call `resume(x)` and it returns `x`. Call `resumeWithException(e)` and `e` is, conceptually, thrown from the exact point where the coroutine stopped. That is how a network error lands in a `try/catch` just like synchronous code.\nRule of thumb: for a suspending function, `resume` means "return", `resumeWithException` means "throw".')
    B(C, S, 2, 'kt',
      'suspend fun requestNews(): News =\n    suspendCancellableCoroutine { cont ->\n        requestNews(\n            onSuccess = { news -> cont.resume(news) },\n            onError = { e -> cont.resumeWithException(e) }\n        )\n    }\n\n// gọi:\ntry {\n    val news = requestNews()\n    show(news)\n} catch (e: IOException) {\n    showError(e)\n}',
      'suspend fun requestNews(): News =\n    suspendCancellableCoroutine { cont ->\n        requestNews(\n            onSuccess = { news -> cont.resume(news) },\n            onError = { e -> cont.resumeWithException(e) }\n        )\n    }\n\n// calling it:\ntry {\n    val news = requestNews()\n    show(news)\n} catch (e: IOException) {\n    showError(e)\n}')

    S = 'notfunction'
    a(C + '.sec.%s.title' % S, 'Suspend một coroutine, không phải một hàm', 'You suspend a coroutine, not a function')
    a(C + '.sec.%s.badge' % S, 'stable')
    B(C, S, 1, 'p', 'Hàm suspend không phải coroutine. Nó chỉ là một hàm có thể làm coroutine đang gọi nó tạm dừng.\nĐoạn mã dưới đây cất continuation vào một biến toàn cục, rồi định resume ngay ở dòng kế tiếp sau lời gọi. Hãy đoán xem chuyện gì xảy ra:',
      'A suspending function is not a coroutine. It is just a function that can make the coroutine calling it pause.\nThe code below stores the continuation in a global variable, then plans to resume it on the very next line after the call. Guess what happens:')
    B(C, S, 2, 'kt',
      '// ĐỪNG làm thế này\nvar continuation: Continuation<Unit>? = null\n\nsuspend fun suspendAndSetContinuation() {\n    suspendCoroutine<Unit> { cont -> continuation = cont }\n}\n\nsuspend fun main() {\n    println("Before")\n    suspendAndSetContinuation()\n    continuation?.resume(Unit)   // không bao giờ tới được dòng này\n    println("After")\n}',
      '// DO NOT do this\nvar continuation: Continuation<Unit>? = null\n\nsuspend fun suspendAndSetContinuation() {\n    suspendCoroutine<Unit> { cont -> continuation = cont }\n}\n\nsuspend fun main() {\n    println("Before")\n    suspendAndSetContinuation()\n    continuation?.resume(Unit)   // this line is never reached\n    println("After")\n}')
    B(C, S, 3, 'ask', 'Vì sao dòng `continuation?.resume(Unit)` không bao giờ chạy?', 'Why does the line `continuation?.resume(Unit)` never run?')
    B(C, S, 3, 'ans', 'Vì chính coroutine chạy dòng đó đang bị suspend ở lời gọi phía trên. Giống như định "tiếp tục game" bằng một nút nằm bên trong game đã tắt. Muốn resume, phải là một luồng hoặc coroutine KHÁC gọi. Ngay cả khi có, cất continuation trong biến toàn cục vẫn dễ rò bộ nhớ và dễ resume nhầm hai lần.', 'Because the very coroutine that would run that line is suspended at the call above it. It is like planning to "continue the game" with a button inside the game you switched off. To resume, ANOTHER thread or coroutine has to call it. Even then, keeping a continuation in a global variable leaks memory easily and makes double resumes easy.')

    S = 'bugs'
    a(C + '.sec.%s.title' % S, 'Bug thường gặp khi tự gói callback', 'Common bugs when wrapping callbacks yourself')
    a(C + '.sec.%s.badge' % S, 'stable')
    B(C, S, 1, 'bug',
      'Ứng dụng crash với `IllegalStateException: Already resumed` khi mạng chập chờn.',
      'The app crashes with `IllegalStateException: Already resumed` when the network is flaky.')
    B(C, S, 1, 'cause', 'API callback gọi cả `onError` rồi sau đó `onSuccess` (hoặc gọi `onSuccess` hai lần, ví dụ khi retry hay cache rồi mạng). Mỗi continuation chỉ được resume đúng một lần; lần thứ hai ném `IllegalStateException`.', 'The callback API calls `onError` and later `onSuccess` (or calls `onSuccess` twice, for example on retry, or cache then network). A continuation may be resumed exactly once; the second time throws `IllegalStateException`.')
    B(C, S, 1, 'fix', 'Nếu API có thể gọi lại nhiều lần thì nó là một dòng giá trị, không phải một kết quả: dùng `callbackFlow` (Phần 3). Nếu chỉ cần kết quả đầu, kiểm `cont.isActive` trước khi resume và gỡ listener sau lần đầu.', 'If the API can call back several times, it is a stream of values, not one result: use `callbackFlow` (Part 3). If you only need the first result, check `cont.isActive` before resuming and remove the listener after the first call.')
    B(C, S, 2, 'bug',
      'Màn hình đóng rồi mà request vẫn chạy tới cùng; coroutine bị "kẹt" không kết thúc khi người dùng rời màn hình.',
      'The screen is closed yet the request runs to the end; the coroutine is "stuck" and does not finish when the user leaves the screen.')
    B(C, S, 2, 'cause', 'Dùng `suspendCoroutine` (không hỗ trợ hủy) hoặc không đăng ký `invokeOnCancellation`. Coroutine cha bị hủy nhưng lời chờ vẫn đợi callback, và request bên dưới vẫn chạy.', 'Using `suspendCoroutine` (no cancellation support), or not registering `invokeOnCancellation`. The parent coroutine is cancelled, but the wait still waits for the callback, and the underlying request keeps running.')
    B(C, S, 2, 'fix', 'Dùng `suspendCancellableCoroutine` và huỷ request khi coroutine bị hủy.', 'Use `suspendCancellableCoroutine` and cancel the request when the coroutine is cancelled.')
    B(C, S, 2, 'fixkt', 'suspend fun Call.await(): Response = suspendCancellableCoroutine { cont ->\n    enqueue(onResponse = { cont.resume(it) }, onFailure = { cont.resumeWithException(it) })\n    cont.invokeOnCancellation { cancel() }\n}')
    B(C, S, 3, 'bug',
      'Coroutine treo mãi ở một hàm tự gói; không lỗi, không log, "Loading" quay vô tận.',
      'A coroutine hangs forever in a hand-wrapped function; no error, no log, "Loading" spins forever.')
    B(C, S, 3, 'cause', 'Có một nhánh trong callback không gọi `resume` hay `resumeWithException`, ví dụ `if (resp.body == null) return`. Không ai resume thì coroutine dừng vĩnh viễn, giống chế độ "Không ai resume" trong mô phỏng.', 'Some branch in the callback calls neither `resume` nor `resumeWithException`, for example `if (resp.body == null) return`. If nobody resumes, the coroutine stops forever, just like the "Nobody resumes" mode in the simulation.')
    B(C, S, 3, 'fix', 'Mọi nhánh của callback phải kết thúc bằng đúng một lần resume. Viết `when` có đủ nhánh, và thêm `withTimeout` ở chỗ gọi để lộ ra treo thay vì chờ mãi.', 'Every branch of the callback must end with exactly one resume. Write an exhaustive `when`, and add `withTimeout` at the call site so a hang shows up instead of waiting forever.')
    B(C, S, 4, 'bug',
      'Bạn tự gói một SDK có callback chạy trên luồng nền, gọi hàm đó trong một coroutine tự dựng không có dispatcher, rồi cập nhật view sau lời gọi: `CalledFromWrongThreadException`.',
      'You wrap an SDK whose callback runs on a background thread, call it in a hand-built coroutine with no dispatcher, then update a view after the call: `CalledFromWrongThreadException`.')
    B(C, S, 4, 'cause', 'Không có dispatcher thì phần sau `resume` chạy trên luồng gọi `resume`, tức luồng nền của SDK (đúng như hàng luồng trong mô phỏng).', 'Without a dispatcher, the code after `resume` runs on the thread that calls `resume`, which is the SDK\'s background thread (exactly as the thread rows in the simulation show).')
    B(C, S, 4, 'fix', 'Chạy coroutine trong `viewModelScope`/`lifecycleScope` (dispatcher `Dispatchers.Main`). Khi đó lời resume được dispatcher chặn lại và chuyển phần tiếp theo về luồng Main, dù callback chạy ở đâu.', 'Run the coroutine in `viewModelScope`/`lifecycleScope` (dispatcher `Dispatchers.Main`). The resume is then intercepted by the dispatcher and the continuation is moved back to the Main thread, wherever the callback runs.')

    S = 'exercises'
    a(C + '.sec.%s.title' % S, 'Bài tập', 'Exercises')
    a(C + '.sec.%s.badge' % S, 'stable')
    B(C, S, 1, 'ex', 'Ví dụ có lời giải: gói API sau thành `suspend fun Geocoder.lookup(query: String): Address`, có hủy.', 'A worked example: wrap the API below into `suspend fun Geocoder.lookup(query: String): Address`, with cancellation.')
    B(C, S, 1, 'exkt', 'interface Geocoder {\n    fun find(query: String, onResult: (Address) -> Unit, onError: (Throwable) -> Unit): Cancellable\n}')
    B(C, S, 1, 'sol', 'Ba bước: (1) `suspendCancellableCoroutine`; (2) mỗi callback gọi đúng một lần `resume`/`resumeWithException`; (3) `invokeOnCancellation` huỷ request bên dưới.', 'Three steps: (1) `suspendCancellableCoroutine`; (2) each callback calls `resume`/`resumeWithException` exactly once; (3) `invokeOnCancellation` cancels the underlying request.')
    B(C, S, 1, 'solkt', 'suspend fun Geocoder.lookup(query: String): Address =\n    suspendCancellableCoroutine { cont ->\n        val handle = find(query,\n            onResult = { cont.resume(it) },\n            onError = { cont.resumeWithException(it) })\n        cont.invokeOnCancellation { handle.cancel() }\n    }')
    B(C, S, 2, 'ex', 'Bài khuyết bước: viết `delay` cho Android bằng `Handler(Looper.getMainLooper()).postDelayed`. Phần sau delay chạy trên luồng nào? Nếu coroutine bị hủy thì phải gỡ gì?', 'A partly-solved exercise: write `delay` for Android using `Handler(Looper.getMainLooper()).postDelayed`. On which thread does the code after this delay run? If the coroutine is cancelled, what must you remove?')
    B(C, S, 2, 'exkt', 'private val main = Handler(Looper.getMainLooper())\n\nsuspend fun mainDelay(ms: Long): Unit = suspendCancellableCoroutine { cont ->\n    val r = Runnable { /* ? */ }\n    main.postDelayed(r, ms)\n    /* ? */\n}')
    B(C, S, 2, 'hint', 'Runnable chạy trên luồng của Looper chính. Cái gì đã được "đăng" lên Handler thì phải gỡ khi hủy.', 'The Runnable runs on the main Looper\'s thread. Whatever was posted to the Handler must be removed on cancellation.')
    B(C, S, 2, 'sol', 'Runnable gọi `cont.resume(Unit)` trên luồng Main, nên (khi không có dispatcher khác chen vào) phần sau `mainDelay` chạy trên luồng Main. Khi hủy, gỡ Runnable khỏi Handler để không resume một continuation đã bị hủy và không giữ tham chiếu.', 'The Runnable calls `cont.resume(Unit)` on the Main thread, so (unless another dispatcher steps in) the code after `mainDelay` runs on the Main thread. On cancellation, remove the Runnable from the Handler so you neither resume a cancelled continuation nor keep a reference.')
    B(C, S, 2, 'solkt', 'suspend fun mainDelay(ms: Long): Unit = suspendCancellableCoroutine { cont ->\n    val r = Runnable { cont.resume(Unit) }\n    main.postDelayed(r, ms)\n    cont.invokeOnCancellation { main.removeCallbacks(r) }\n}')
    B(C, S, 3, 'ex', 'Đoán output:', 'Predict the output:')
    B(C, S, 3, 'exkt', 'suspend fun main() {\n    val x = suspendCoroutine<Int> { cont ->\n        thread {\n            cont.resume(7)\n            println("B")\n        }\n    }\n    println("A$x")\n}')
    B(C, S, 3, 'sol', '"A7" rồi "B". `resume(7)` chạy phần còn lại của coroutine (in "A7") ngay trên luồng mới, rồi mới trả về để in "B". Giống thứ tự After → Resumed trong mô phỏng.', '"A7", then "B". `resume(7)` runs the rest of the coroutine (printing "A7") right on the new thread before returning to print "B". Same as the After → Resumed order in the simulation.')

    S = 'recall'
    a(C + '.sec.%s.title' % S, 'Tự trả lời', 'Answer it yourself')
    a(C + '.sec.%s.badge' % S, 'stable')
    B(C, S, 1, 'ask', 'Lambda truyền cho `suspendCoroutine` chạy lúc nào, và vì sao phải là lúc đó?', 'When does the lambda passed to `suspendCoroutine` run, and why must it be then?')
    B(C, S, 1, 'ans', 'Ngay trước khi coroutine suspend. Sau khi suspend thì coroutine đã dừng, không còn mã nào chạy để cất continuation; trước đó thì continuation chưa có ý nghĩa. Lambda là cửa sổ duy nhất để giao continuation cho ai đó.', 'Right before the coroutine suspends. After suspending, the coroutine has stopped and no code runs to store the continuation; before that, the continuation means nothing yet. The lambda is the only window to hand the continuation to someone.')
    B(C, S, 2, 'ask', 'Trong `suspend fun main`, luồng phụ gọi `resume`. Phần sau điểm suspend chạy trên luồng nào? Trong `viewModelScope` thì sao?', 'In `suspend fun main`, a helper thread calls `resume`. Which thread runs the code after the suspension point? What about inside `viewModelScope`?')
    B(C, S, 2, 'ans', '`suspend fun main`: trên luồng phụ, vì không có dispatcher. `viewModelScope`: trên luồng Main, vì `Dispatchers.Main` chặn lời resume và gửi phần tiếp theo về luồng Main.', '`suspend fun main`: on the helper thread, because there is no dispatcher. `viewModelScope`: on the Main thread, because `Dispatchers.Main` intercepts the resume and sends the continuation to the Main thread.')
    B(C, S, 3, 'ask', 'Nêu ba lỗi khi tự gói callback và cách phòng từng lỗi.', 'Name three mistakes when wrapping callbacks yourself, and how to prevent each.')
    B(C, S, 3, 'ans', 'Resume hai lần → chỉ resume một lần, hoặc dùng `callbackFlow` cho nhiều giá trị. Có nhánh không resume → treo; mọi nhánh phải resume, thêm `withTimeout`. Không hỗ trợ hủy → dùng `suspendCancellableCoroutine` + `invokeOnCancellation`.', 'Resuming twice → resume exactly once, or use `callbackFlow` for many values. A branch that never resumes → a hang; every branch must resume, and add `withTimeout`. No cancellation support → use `suspendCancellableCoroutine` + `invokeOnCancellation`.')
    for q, qv, qe, av, ae, wv, we in [
        ('q1', 'Coroutine đang suspend chiếm bao nhiêu luồng?', 'How many threads does a suspended coroutine occupy?',
         'Không luồng nào.', 'None.', 'Chỉ còn đối tượng continuation trên heap; luồng đã được thả.', 'Only the continuation object on the heap remains; the thread has been released.'),
        ('q2', '`resumeWithException(e)` làm gì?', 'What does `resumeWithException(e)` do?',
         'Làm `e` bị ném ra tại điểm suspension của coroutine.', 'It makes `e` be thrown at the coroutine\'s suspension point.',
         'Nhờ vậy `try/catch`/`finally` quanh lời gọi suspend hoạt động như mã đồng bộ.', 'That is why `try/catch`/`finally` around a suspending call work like synchronous code.'),
        ('q3', 'Vì sao `delay` không cần một luồng ngủ cho mỗi coroutine?', 'Why does `delay` not need a sleeping thread for each coroutine?',
         'Vì nó chỉ hẹn giờ: cất continuation và để một bộ hẹn giờ dùng chung gọi `resume` khi tới lúc.', 'Because it only sets an alarm: it stores the continuation and lets a shared timer call `resume` when the time comes.',
         'Trong lúc chờ, coroutine suspend và không luồng nào bị chặn.', 'While waiting, the coroutine is suspended and no thread is blocked.')]:
        a(C + '.quiz.%s.q' % q, qv, qe); a(C + '.quiz.%s.a' % q, av, ae); a(C + '.quiz.%s.why' % q, wv, we)
