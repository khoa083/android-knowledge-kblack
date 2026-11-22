# Coroutines v2 · Phần 2 · A2 Job và chờ con (Deep Dive, "Jobs and awaiting children", tr. PDF 94–106) + sim coroutines.jobstate.
# Viết sâu thêm vào A2 (giữ id a2, sim coroutines.jobtree và mục v1 "tree"); thêm sim vòng đời Job.

SEC_ORDER = {'a2': ['recap', 'intro', 'states', 'builders', 'join', 'factory', 'tree', 'bugs', 'exercises', 'recall']}


def override(o):
    o('a2.title', 'Job, vòng đời và chờ con', 'Jobs, their lifecycle, and awaiting children')
    o('a2.essence',
      'Ba trong bốn hệ quả của structured concurrency (cha chờ con, hủy cha thì hủy con, con lỗi thì phá cha) đều dựa trên `Job`. Về khái niệm, Job là "một việc có vòng đời và hủy được"; vòng đời đó là một máy trạng thái: New → Active → Completing → Completed, hoặc rẽ sang Cancelling → Cancelled.\n'
      'Mỗi coroutine có Job RIÊNG: builder tạo Job mới và lấy Job của cha (hoặc Job bạn truyền vào) làm cha của nó. `Job` là phần tử context duy nhất không được thừa hưởng nguyên vẹn. Cha giữ tham chiếu tới các con, con giữ tham chiếu tới cha; nhờ đó hủy và lỗi mới lan được.\n'
      '`join()` suspend tới khi một Job ở trạng thái cuối. `Job()` tạo một Job không gắn với coroutine nào; nó không tự hoàn tất khi các con xong, nên `join()` trên nó sẽ chờ mãi nếu không gọi `complete()`.',
      'Three of the four effects of structured concurrency (the parent waits, cancelling the parent cancels the children, a failing child destroys the parent) all rest on `Job`. Conceptually, a Job is "a cancellable thing with a lifecycle"; that lifecycle is a state machine: New → Active → Completing → Completed, or a turn into Cancelling → Cancelled.\n'
      'Every coroutine has its OWN Job: the builder creates a new Job and makes the parent\'s Job (or the Job you pass in) its parent. `Job` is the one context element that is not inherited as-is. The parent keeps references to its children and each child to its parent; that is what lets cancellation and errors propagate.\n'
      '`join()` suspends until a Job reaches a final state. `Job()` creates a Job not tied to any coroutine; it does not complete by itself when its children finish, so `join()` on it waits forever unless you call `complete()`.')
    o('a2.goal.g1', 'Đã đi qua vòng đời Job tới một trạng thái cuối', 'Followed a Job\'s lifecycle to a final state')
    o('a2.goal.g2', 'Đã thử hủy ở hai thời điểm khác nhau', 'Tried cancelling at two different moments')


def add(a):
    def B(ch, sec, n, field, vi, en=None):
        a('%s.sec.%s.b.%02d.%s' % (ch, sec, n, field), vi, vi if en is None else en)
    m = lambda k, vi, en=None: a('m.jobstate.' + k, vi, en)

    # ---------------- sim coroutines.jobstate ----------------
    m('title', 'Vòng đời của một Job', 'The lifecycle of a Job')
    m('overview', 'Một coroutine cha có một con. Bấm Step để thấy Job của cha đi qua các trạng thái, và theo dõi ba cờ `isActive`, `isCompleted`, `isCancelled`. Thử bật "lazy" và thử hủy ở hai thời điểm.', 'A parent coroutine with one child. Press Step to watch the parent\'s Job move through its states, and follow the three flags `isActive`, `isCompleted`, `isCancelled`. Try turning on "lazy" and cancelling at two different moments.')
    m('wrapup', 'Thân coroutine chạy ở Active. Thân xong thì sang Completing và chờ con. Con xong thì Completed. Hủy (hoặc lỗi) khi đang Active/Completing thì sang Cancelling: các con bị hủy, `finally` chạy dọn dẹp, rồi mới tới Cancelled. Để ý: Completing vẫn có `isActive = true`; cả Completed lẫn Cancelled đều có `isCompleted = true`.', 'The coroutine body runs in Active. When the body finishes it moves to Completing and waits for its children. When the children finish it is Completed. Cancelling (or failing) while Active/Completing moves it to Cancelling: the children are cancelled, `finally` blocks clean up, and only then comes Cancelled. Note: Completing still has `isActive = true`; both Completed and Cancelled have `isCompleted = true`.')
    m('simp.1', 'Mô hình có một con và không có lỗi (lỗi đi đường giống hủy: qua Cancelling). Chuyển trạng thái thật diễn ra bên trong `JobSupport` của kotlinx.coroutines.', 'The model has one child and no errors (a failure takes the same road as cancellation: through Cancelling). The real transitions happen inside kotlinx.coroutines\' `JobSupport`.')
    m('ctl.hint', 'Bật "lazy" để bắt đầu ở New; chọn thời điểm hủy.', 'Turn on "lazy" to start in New; choose when to cancel.')
    m('ctl.lazy', 'start = CoroutineStart.LAZY', 'start = CoroutineStart.LAZY')
    m('ctl.cancelAt', 'Gọi cancel()', 'Call cancel()')
    for k, vi, en in [('none', 'không hủy', 'do not cancel'), ('active', 'khi thân đang chạy (Active)', 'while the body runs (Active)'), ('completing', 'khi thân xong, đang chờ con (Completing)', 'after the body, while waiting for the child (Completing)')]:
        m('ctl.cancelAt.' + k, vi, en)
    m('diagramTitle', 'Máy trạng thái của Job', 'The Job state machine')
    m('diagramDesc', 'Sáu trạng thái của Job và các chuyển tiếp giữa chúng', 'The six Job states and the transitions between them')
    for k, vi, en in [('new', 'New', 'New'), ('active', 'Active', 'Active'), ('completing', 'Completing', 'Completing'), ('completed', 'Completed', 'Completed'), ('cancelling', 'Cancelling', 'Cancelling'), ('cancelled', 'Cancelled', 'Cancelled')]:
        m('n.' + k, vi, en)
        m('state.' + k, vi, en)
    for k, vi, en in [('start', 'start()', 'start()'), ('body', 'thân xong', 'body done'), ('kids', 'mọi con xong', 'all children done'), ('cancel', 'cancel() / lỗi', 'cancel() / failure'), ('clean', 'dọn xong', 'cleanup done')]:
        m('e.' + k, vi, en)
    for k, vi, en in [('isActive', 'isActive', 'isActive'), ('isCompleted', 'isCompleted', 'isCompleted'), ('isCancelled', 'isCancelled', 'isCancelled'), ('kids', 'Số con đang chạy', 'Children running')]:
        m('met.' + k, vi, en)
    m('col.state', 'Trạng thái của Job cha', 'Parent Job state')
    m('v.yes', 'true', 'true')
    m('v.no', 'false', 'false')
    for k, vi, en in [('running', 'đang ở đây', 'here now'), ('completed', 'đang ở đây (cuối)', 'here (final)'), ('cancelled', 'đang ở đây (cuối)', 'here (final)'), ('cancelling', 'đang ở đây', 'here now'), ('done', 'đã qua', 'passed'), ('idle', 'chưa tới', 'not reached')]:
        m('st.' + k, vi, en)
    S = [
        ('createdLazy', 'launch(start = LAZY): Job ở New', 'launch(start = LAZY): the Job is New', 'Coroutine lazy chưa chạy gì: thân chưa bắt đầu, cả ba cờ đều false.', 'A lazy coroutine has not run anything: the body has not started, and all three flags are false.'),
        ('start', 'start(): New → Active', 'start(): New → Active', 'Gọi `start()` (hoặc `join()`/`await()`) thì coroutine lazy mới bắt đầu.', 'Only `start()` (or `join()`/`await()`) makes a lazy coroutine begin.'),
        ('created', 'launch: Job bắt đầu ở Active', 'launch: the Job starts in Active', 'Mặc định coroutine ở Active ngay khi tạo; thân của nó chạy trong trạng thái này.', 'By default a coroutine is Active as soon as it is created; its body runs in this state.'),
        ('child', 'Cha launch một con', 'The parent launches a child', 'Chỉ ở Active mới khởi động được con. Job của con là con của Job cha.', 'Children can only be started in Active. The child\'s Job is a child of the parent\'s Job.'),
        ('bodyDone', 'Thân của cha chạy xong → Completing', 'The parent body finishes → Completing', 'Cha không xong ngay: nó chờ con. Lưu ý `isActive` vẫn là true ở Completing.', 'The parent is not done yet: it waits for its child. Note that `isActive` is still true in Completing.'),
        ('childDone', 'Con xong', 'The child finishes', 'Không còn con nào chạy.', 'No child is running any more.'),
        ('completed', 'Completed: trạng thái cuối', 'Completed: the final state', '`isCompleted = true`, `isCancelled = false`. `join()` trên Job này trả về.', '`isCompleted = true`, `isCancelled = false`. `join()` on this Job returns.'),
        ('cancelActive', 'cancel() khi đang Active → Cancelling', 'cancel() while Active → Cancelling', 'Hủy chuyển Job sang Cancelling: `isActive = false`, `isCancelled = true`, nhưng chưa xong: còn phải hủy con và dọn dẹp.', 'Cancellation moves the Job to Cancelling: `isActive = false`, `isCancelled = true`, but it is not finished: the children still have to be cancelled and cleaned up.'),
        ('cancelCompleting', 'cancel() khi đang Completing → Cancelling', 'cancel() while Completing → Cancelling', 'Thân đã xong nhưng con còn chạy: hủy lúc này vẫn hủy con.', 'The body is done but the child is still running: cancelling now still cancels the child.'),
        ('cleanup', 'Cancelling: con bị hủy, finally chạy', 'Cancelling: the child is cancelled, finally runs', 'Đây là "cơ hội cuối" để đóng kết nối, giải phóng tài nguyên. Chương Hủy sẽ đi sâu.', 'This is the "last chance" to close connections and free resources. The Cancellation chapter goes deeper.'),
        ('cancelled', 'Cancelled: trạng thái cuối', 'Cancelled: the final state', '`isCompleted = true` VÀ `isCancelled = true`. `join()` cũng trả về ở đây.', '`isCompleted = true` AND `isCancelled = true`. `join()` returns here too.'),
    ]
    for sid, tv, te, xv, xe in S:
        m('s.%s.title' % sid, tv, te); m('s.%s.explain' % sid, xv, xe); m('ev.' + sid, tv, te)
    for k, vi, en in [
        ('lazy', 'Lazy hữu ích khi muốn chuẩn bị trước và chỉ chạy khi cần; nhưng quên `start()`/`join()` thì nó không bao giờ chạy (và giữ cha ở Completing).', 'Lazy is useful to prepare work and run it only when needed; but forget `start()`/`join()` and it never runs (and keeps the parent in Completing).'),
        ('completing', 'Đây là "cha chờ con" của structured concurrency, nằm ngay trong máy trạng thái.', 'This is structured concurrency\'s "the parent waits for its children", built right into the state machine.'),
        ('cancelling', 'Hủy không tức thời: Job đi qua Cancelling để con kịp dừng và dọn dẹp.', 'Cancellation is not instant: the Job passes through Cancelling so children can stop and clean up.'),
        ('finally', 'Trên Android, đây là chỗ đóng cursor, huỷ đăng ký listener, xoá file tạm khi người dùng rời màn hình.', 'On Android, this is where you close cursors, unregister listeners and delete temp files when the user leaves the screen.'),
        ('join', '`isCompleted` true ở CẢ Completed lẫn Cancelled. Muốn biết thành công hay bị hủy, xem thêm `isCancelled`.', '`isCompleted` is true in BOTH Completed and Cancelled. To tell success from cancellation, also check `isCancelled`.')]:
        m('co.' + k, vi, en)
    a('cap.jobstate', 'Sáu thẻ là sáu trạng thái của Job cha; token chạy dọc mũi tên khi Job chuyển trạng thái. Hàng trên là đường bình thường, hàng dưới là đường hủy. Dải chỉ số là ba cờ của Job và số con đang chạy.', 'The six cards are the parent Job\'s six states; a token runs along an arrow when the Job changes state. The top row is the normal path, the bottom row the cancellation path. The metric strip shows the Job\'s three flags and the number of running children.')
    a('a2.sim.coroutines.jobstate', 'Vòng đời Job', 'Job lifecycle')
    a('a2.sim.coroutines.jobtree', 'Cây Job: hủy và lỗi', 'Job tree: cancellation and failure')

    # ---------------- chương A2 ----------------
    C = 'a2'
    S = 'recap'
    a(C + '.sec.%s.title' % S, 'Ôn nhanh chương trước', 'Quick review of the previous chapter')
    B(C, S, 1, 'ask', 'Truyền `Job()` vào `launch` thì chuyện gì xảy ra với quan hệ cha–con? Vì sao?', 'What happens to the parent–child relationship when you pass `Job()` to `launch`? Why?')
    B(C, S, 1, 'ans', 'Job truyền vào thay Job của cha (bên phải thắng), nên nó thành cha của coroutine mới. Coroutine bị tách khỏi cây: cha cũ không chờ nó, hủy cha cũ không hủy nó. Chương này giải thích cơ chế đằng sau.', 'The passed Job replaces the parent\'s Job (the right side wins), so it becomes the new coroutine\'s parent. The coroutine is detached from the tree: the old parent neither waits for it nor cancels it. This chapter explains the mechanism behind that.')

    S = 'intro'
    a(C + '.sec.%s.title' % S, 'Vì sao Job quan trọng', 'Why Job matters')
    a(C + '.sec.%s.badge' % S, 'stable')
    B(C, S, 1, 'p', 'Trong bốn hệ quả của structured concurrency, "con thừa hưởng context" chỉ là hành vi cơ bản của builder. Ba hệ quả còn lại (cha chờ con, hủy lan xuống con, lỗi ở con phá cha) hoàn toàn dựa vào phần tử context `Job`. Job còn dùng để hủy coroutine, theo dõi trạng thái và nhiều việc khác. Chương này và hai chương sau (Hủy, Exception) đều xoay quanh Job ([[src:kx-job]]).', 'Of the four effects of structured concurrency, "children inherit the context" is just basic builder behaviour. The other three (the parent waits, cancellation reaches the children, a child\'s failure destroys the parent) rely entirely on the `Job` context element. A Job is also used to cancel coroutines, track their state and more. This chapter and the next two (Cancellation, Exceptions) all revolve around Job ([[src:kx-job]]).')

    S = 'states'
    a(C + '.sec.%s.title' % S, 'Job là gì: một việc hủy được, có vòng đời', 'What a Job is: a cancellable thing with a lifecycle')
    a(C + '.sec.%s.badge' % S, 'stable')
    B(C, S, 1, 'p',
      'Về hình thức `Job` là interface, nhưng có hợp đồng và trạng thái cụ thể. Vòng đời của nó là một máy trạng thái:\n'
      '• Active: Job đang chạy. Job tạo bằng builder chạy thân coroutine ở đây, và chỉ ở đây mới khởi động được con. Hầu hết coroutine bắt đầu ở Active.\n'
      '• New: chỉ coroutine lazy (`start = CoroutineStart.LAZY`) bắt đầu ở đây; phải được start mới sang Active.\n'
      '• Completing: thân đã chạy xong, Job chờ các con.\n'
      '• Completed: mọi con đã xong; trạng thái cuối.\n'
      '• Cancelling: Job bị hủy hoặc lỗi khi đang Active/Completing. Đây là cơ hội cuối để dọn dẹp (đóng kết nối, giải phóng tài nguyên).\n'
      '• Cancelled: dọn xong; trạng thái cuối.',
      'Formally `Job` is an interface, but it has a concrete contract and state. Its lifecycle is a state machine:\n'
      '• Active: the Job is running. A Job created by a builder runs the coroutine body here, and only here can children be started. Most coroutines start in Active.\n'
      '• New: only lazy coroutines (`start = CoroutineStart.LAZY`) start here; they must be started to become Active.\n'
      '• Completing: the body has finished; the Job waits for its children.\n'
      '• Completed: all children are done; a final state.\n'
      '• Cancelling: the Job was cancelled or failed while Active/Completing. This is the last chance to clean up (close connections, free resources).\n'
      '• Cancelled: cleanup is done; a final state.')
    B(C, S, 2, 'p', 'Trong mã, kiểm trạng thái bằng ba cờ. Đừng phân tích chuỗi `toString()` (dạng `StandaloneCoroutine{Active}@…`): nó chỉ để debug và log.', 'In code, check the state with three flags. Do not parse the `toString()` text (shaped like `StandaloneCoroutine{Active}@…`): it is only for debugging and logging.')
    B(C, S, 3, 'kt', '// trạng thái      isActive  isCompleted  isCancelled\n// New               false     false        false\n// Active            true      false        false\n// Completing        true      false        false\n// Cancelling        false     false        true\n// Cancelled         false     true         true\n// Completed         false     true         false', '// state           isActive  isCompleted  isCancelled\n// New               false     false        false\n// Active            true      false        false\n// Completing        true      false        false\n// Cancelling        false     false        true\n// Cancelled         false     true         true\n// Completed         false     true         false')
    B(C, S, 4, 'predict', 'Trước khi chạy mô phỏng: (1) ở Completing, `isActive` là gì? (2) Một Job bị hủy rồi xong thì `isCompleted` là gì? (3) Hủy khi thân đã xong nhưng con còn chạy thì con ra sao?', 'Before running the simulation: (1) in Completing, what is `isActive`? (2) For a Job that was cancelled and finished, what is `isCompleted`? (3) If you cancel after the body has finished but while the child is still running, what happens to the child?')
    B(C, S, 4, 'ans', '(1) true: Job vẫn "sống" vì còn chờ con. (2) true: Cancelled cũng là trạng thái cuối, nên `isCompleted = true` và `isCancelled = true`. (3) Con vẫn bị hủy: Completing → Cancelling. Bấm Step ở tab "Vòng đời Job" để kiểm.', '(1) true: the Job is still "alive" because it is waiting for its children. (2) true: Cancelled is also a final state, so `isCompleted = true` and `isCancelled = true`. (3) The child is still cancelled: Completing → Cancelling. Step through the "Job lifecycle" tab to check.')

    S = 'builders'
    a(C + '.sec.%s.title' % S, 'Builder tạo Job riêng; Job không được thừa hưởng', 'Builders create their own Job; Job is not inherited')
    a(C + '.sec.%s.badge' % S, 'stable')
    B(C, S, 1, 'p', 'Mọi builder của thư viện tạo Job riêng, và hầu hết trả nó về: `launch` trả `Job`; `async` trả `Deferred<T>`, mà `Deferred` cũng hiện thực `Job`. Vì Job là phần tử context, đọc được bằng `coroutineContext[Job]`, hoặc gọn hơn bằng extension `coroutineContext.job`.', 'Every library builder creates its own Job, and most return it: `launch` returns a `Job`; `async` returns a `Deferred<T>`, and `Deferred` also implements `Job`. Since a Job is a context element, you can read it with `coroutineContext[Job]`, or more conveniently with the `coroutineContext.job` extension.')
    B(C, S, 2, 'kt', 'fun main(): Unit = runBlocking {\n    val name = CoroutineName("Some name")\n    val job = Job()\n    launch(name + job) {\n        val childName = coroutineContext[CoroutineName]\n        println(childName == name)                        // true\n        val childJob = coroutineContext[Job]\n        println(childJob == job)                          // ?\n        println(childJob == job.children.first())         // ?\n    }\n}')
    B(C, S, 3, 'predict', 'Hai dòng có dấu `?` in gì?', 'What do the two lines marked `?` print?')
    B(C, S, 3, 'ans', 'false rồi true. Quy tắc rất quan trọng: Job là phần tử context DUY NHẤT không được coroutine thừa hưởng. Mỗi coroutine tạo Job riêng, và Job từ tham số (hay từ cha) được dùng làm CHA của Job mới. Tên thì thừa hưởng nguyên vẹn.', 'false, then true. A very important rule: Job is the ONLY context element a coroutine does not inherit. Every coroutine creates its own Job, and the Job from the argument (or from the parent) becomes the PARENT of the new Job. The name, by contrast, is inherited as-is.')
    B(C, S, 4, 'p', 'Cha tham chiếu tới mọi con (`job.children`), con tham chiếu tới cha. Chính các tham chiếu này cho phép hủy và lỗi lan trong scope. Thay Job cha bằng một Job mới là cắt đứt chúng:', 'The parent references all its children (`job.children`), and each child references its parent. These references are what let cancellation and errors propagate within a scope. Replacing the parent\'s Job with a new one cuts them:')
    B(C, S, 5, 'kt', 'fun main(): Unit = runBlocking {\n    launch(Job()) {               // Job mới thay Job của cha\n        delay(1000)\n        println("Will not be printed")\n    }\n}\n// (không in gì, kết thúc ngay)', 'fun main(): Unit = runBlocking {\n    launch(Job()) {               // the new Job replaces the parent\'s\n        delay(1000)\n        println("Will not be printed")\n    }\n}\n// (prints nothing, finishes immediately)')

    S = 'join'
    a(C + '.sec.%s.title' % S, 'Chờ: join() và children', 'Waiting: join() and children')
    a(C + '.sec.%s.badge' % S, 'stable')
    B(C, S, 1, 'p', '`join()` là hàm suspend, suspend cho tới khi Job tới trạng thái cuối (Completed hoặc Cancelled). Thuộc tính `children` cho phép chờ mọi con:', '`join()` is a suspending function that suspends until the Job reaches a final state (Completed or Cancelled). The `children` property lets you wait for every child:')
    B(C, S, 2, 'kt', 'fun main(): Unit = runBlocking {\n    launch { delay(1000); println("Test1") }\n    launch { delay(2000); println("Test2") }\n    val children = coroutineContext[Job]?.children\n    println("Number of children: ${children?.count()}")\n    children?.forEach { it.join() }\n    println("All tests are done")\n}\n// Number of children: 2\n// (1 s) Test1\n// (1 s) Test2\n// All tests are done', 'fun main(): Unit = runBlocking {\n    launch { delay(1000); println("Test1") }\n    launch { delay(2000); println("Test2") }\n    val children = coroutineContext[Job]?.children\n    println("Number of children: ${children?.count()}")\n    children?.forEach { it.join() }\n    println("All tests are done")\n}\n// Number of children: 2\n// (1 s) Test1\n// (1 s) Test2\n// All tests are done')

    S = 'factory'
    a(C + '.sec.%s.title' % S, 'Job(): Job không gắn coroutine, complete() và completeExceptionally()', 'Job(): a Job without a coroutine, complete() and completeExceptionally()')
    a(C + '.sec.%s.badge' % S, 'stable')
    B(C, S, 1, 'p', '`Job()` tạo một Job không gắn với coroutine nào, dùng được làm context, tức làm cha cho nhiều coroutine. `Job` là interface nên `Job()` không phải constructor mà là factory function (một "constructor giả"), và kiểu trả về thật là `CompletableJob` ([[src:kx-jobfn]]).', '`Job()` creates a Job not tied to any coroutine, usable as a context, that is, as the parent of many coroutines. `Job` is an interface, so `Job()` is not a constructor but a factory function (a "fake constructor"), and its real return type is `CompletableJob` ([[src:kx-jobfn]]).')
    B(C, S, 2, 'kt', 'suspend fun main(): Unit = coroutineScope {\n    val job = Job()\n    launch(job) { delay(1000); println("Text 1") }\n    launch(job) { delay(2000); println("Text 2") }\n    job.join()\n    println("Will not be printed")\n}')
    B(C, S, 3, 'predict', 'Chương trình in gì và có kết thúc không?', 'What does the program print, and does it end?')
    B(C, S, 3, 'ans', 'Text 1, Text 2, rồi chờ mãi: "Will not be printed" không bao giờ in. Job tạo bằng `Job()` vẫn ở Active dù các con đã xong, vì nó còn sẵn sàng cho coroutine khác. Sửa bằng `job.children.forEach { it.join() }`, hoặc gọi `job.complete()` sau khi launch con cuối rồi mới `join()`.', 'Text 1, Text 2, then it waits forever: "Will not be printed" never prints. A Job created with `Job()` stays Active even after its children finish, because it is still available for other coroutines. Fix it with `job.children.forEach { it.join() }`, or call `job.complete()` after launching the last child and then `join()`.')
    B(C, S, 4, 'p',
      '`CompletableJob` thêm hai hàm:\n'
      '• `complete(): Boolean`: hoàn tất Job. Các con đang chạy tiếp tục tới xong, nhưng không khởi động được con mới trong Job này. Trả true nếu chính lời gọi này hoàn tất Job.\n'
      '• `completeExceptionally(exception): Boolean`: hoàn tất Job với exception. Mọi con bị hủy NGAY (bằng `CancellationException` bọc exception đó).\n'
      'Có thể truyền cha: `Job(parentJob)`; khi đó hủy cha thì Job này cũng bị hủy.',
      '`CompletableJob` adds two functions:\n'
      '• `complete(): Boolean`: completes the Job. Running children carry on until they finish, but no new child can be started in this Job. Returns true if this very call completed the Job.\n'
      '• `completeExceptionally(exception): Boolean`: completes the Job with an exception. All children are cancelled IMMEDIATELY (with a `CancellationException` wrapping that exception).\n'
      'You can pass a parent: `Job(parentJob)`; then cancelling the parent cancels this Job too.')
    B(C, S, 5, 'kt', 'fun main() = runBlocking {\n    val job = Job()\n    launch(job) {\n        repeat(5) { num -> delay(200); println("Rep$num") }\n    }\n    launch { delay(500); job.complete() }\n    job.join()\n    launch(job) { println("Will not be printed") }\n    println("Done")\n}\n// Rep0 Rep1 Rep2 Rep3 Rep4 Done\n// (với completeExceptionally(Error("Some error")) ở chỗ complete(): Rep0 Rep1 Done)', 'fun main() = runBlocking {\n    val job = Job()\n    launch(job) {\n        repeat(5) { num -> delay(200); println("Rep$num") }\n    }\n    launch { delay(500); job.complete() }\n    job.join()\n    launch(job) { println("Will not be printed") }\n    println("Done")\n}\n// Rep0 Rep1 Rep2 Rep3 Rep4 Done\n// (with completeExceptionally(Error("Some error")) instead of complete(): Rep0 Rep1 Done)')

    S = 'bugs'
    a(C + '.sec.%s.title' % S, 'Bug thường gặp với Job', 'Common bugs with Job')
    a(C + '.sec.%s.badge' % S, 'stable')
    B(C, S, 1, 'bug', 'Màn hình hiện "Tải xong!" dù người dùng đã bấm Hủy. Code: `job.join(); if (job.isCompleted) showDone()`.', 'The screen shows "Loaded!" even though the user pressed Cancel. Code: `job.join(); if (job.isCompleted) showDone()`.')
    B(C, S, 1, 'cause', '`isCompleted` là true ở CẢ Completed lẫn Cancelled (bảng cờ). Sau `join()`, Job luôn ở trạng thái cuối, nên điều kiện luôn đúng.', '`isCompleted` is true in BOTH Completed and Cancelled (see the flag table). After `join()` the Job is always in a final state, so the condition is always true.')
    B(C, S, 1, 'fix', 'Kiểm `!job.isCancelled`, hoặc tốt hơn: để chính coroutine cập nhật UI khi việc thật sự xong (dòng cuối của khối), thay vì suy từ cờ.', 'Check `!job.isCancelled`, or better: let the coroutine itself update the UI when the work really finishes (the last line of its block), instead of inferring it from flags.')
    B(C, S, 2, 'bug', 'Bạn gom các coroutine "tải nền" vào một `val downloads = Job()` rồi `downloads.join()` để chờ hết. Test treo vĩnh viễn.', 'You group "background download" coroutines under `val downloads = Job()` and then call `downloads.join()` to wait for all of them. The test hangs forever.')
    B(C, S, 2, 'cause', 'Job tạo bằng `Job()` không tự chuyển sang Completed khi các con xong; nó ở Active chờ thêm con. `join()` chờ trạng thái cuối mãi không tới.', 'A Job created with `Job()` does not move to Completed by itself when its children finish; it stays Active, waiting for more children. `join()` waits for a final state that never comes.')
    B(C, S, 2, 'fix', 'Gọi `downloads.complete()` sau khi khởi động con cuối rồi mới `join()`, hoặc `downloads.children.forEach { it.join() }`. Tốt hơn nữa: dùng `coroutineScope { … }`, vì nó tự chờ mọi con.', 'Call `downloads.complete()` after starting the last child and then `join()`, or use `downloads.children.forEach { it.join() }`. Better still: use `coroutineScope { … }`, which waits for all its children by itself.')
    B(C, S, 3, 'bug', 'Bạn tạo `val prefetch = scope.async(start = CoroutineStart.LAZY) { load() }` để "dùng nếu cần". Khi không cần thì không gọi `await()`. Màn hình đóng nhưng scope không kết thúc, test báo coroutine còn chạy.', 'You create `val prefetch = scope.async(start = CoroutineStart.LAZY) { load() }` to "use it if needed". When it is not needed you never call `await()`. The screen closes but the scope does not finish, and the test reports a coroutine still running.')
    B(C, S, 3, 'cause', 'Coroutine lazy nằm ở New tới khi được start. Nó vẫn là con của scope, nên cha (đang ở Completing) chờ nó mãi.', 'A lazy coroutine stays in New until started. It is still a child of the scope, so the parent (in Completing) waits for it forever.')
    B(C, S, 3, 'fix', 'Không cần nữa thì `prefetch.cancel()`; hoặc chỉ tạo coroutine khi chắc cần dùng.', 'If it is no longer needed, call `prefetch.cancel()`; or create the coroutine only when you are sure it will be used.')

    S = 'exercises'
    a(C + '.sec.%s.title' % S, 'Bài tập', 'Exercises')
    a(C + '.sec.%s.badge' % S, 'stable')
    B(C, S, 1, 'ex', 'Đoán trạng thái in ra ở mỗi dòng (bỏ phần `@…`):', 'Predict the state printed on each line (ignore the `@…` part):')
    B(C, S, 1, 'exkt', 'suspend fun main() = coroutineScope {\n    val job = Job()\n    println(job)\n    job.complete()\n    println(job)\n    val lazyJob = launch(start = CoroutineStart.LAZY) { delay(1000) }\n    println(lazyJob)\n    lazyJob.start()\n    println(lazyJob)\n    lazyJob.join()\n    println(lazyJob)\n}')
    B(C, S, 1, 'sol', 'JobImpl{Active} → JobImpl{Completed} → LazyStandaloneCoroutine{New} → LazyStandaloneCoroutine{Active} → (1 s) LazyStandaloneCoroutine{Completed}. (Tên lớp nội bộ có thể khác giữa các phiên bản; trạng thái thì không.)', 'JobImpl{Active} → JobImpl{Completed} → LazyStandaloneCoroutine{New} → LazyStandaloneCoroutine{Active} → (1 s) LazyStandaloneCoroutine{Completed}. (Internal class names may differ between versions; the states do not.)')
    B(C, S, 2, 'ex', 'Bài khuyết bước: hàm dưới khởi động N việc trên một Job riêng và phải trả về khi tất cả xong. Hoàn thành hai chỗ `TODO`.', 'A partly-solved exercise: the function below starts N jobs under a separate Job and must return once all of them are done. Fill in the two `TODO`s.')
    B(C, S, 2, 'exkt', 'suspend fun runAll(scope: CoroutineScope, tasks: List<suspend () -> Unit>) {\n    val group = Job(scope.coroutineContext.job)   // con của scope: hủy scope thì hủy group\n    tasks.forEach { t -> scope.launch(group) { t() } }\n    TODO()   // 1\n    TODO()   // 2\n}', 'suspend fun runAll(scope: CoroutineScope, tasks: List<suspend () -> Unit>) {\n    val group = Job(scope.coroutineContext.job)   // child of the scope: cancelling the scope cancels group\n    tasks.forEach { t -> scope.launch(group) { t() } }\n    TODO()   // 1\n    TODO()   // 2\n}')
    B(C, S, 2, 'hint', 'Job tạo bằng `Job()` không tự hoàn tất. Cần làm gì trước khi `join()`?', 'A Job created with `Job()` does not complete by itself. What must you do before `join()`?')
    B(C, S, 2, 'sol', '`group.complete()` (không nhận thêm con, chuyển sang Completing chờ các con), rồi `group.join()`. Trong mã thật, cách gọn và an toàn hơn là `coroutineScope { tasks.forEach { launch { it() } } }`.', '`group.complete()` (accept no more children, move to Completing and wait for them), then `group.join()`. In real code, the shorter and safer way is `coroutineScope { tasks.forEach { launch { it() } } }`.')
    B(C, S, 2, 'solkt', 'group.complete()\ngroup.join()')

    S = 'recall'
    a(C + '.sec.%s.title' % S, 'Tự trả lời', 'Answer it yourself')
    a(C + '.sec.%s.badge' % S, 'stable')
    B(C, S, 1, 'ask', 'Vẽ lại (trên giấy) máy trạng thái của Job với sáu trạng thái và các mũi tên. Trạng thái nào là cuối? Trạng thái nào thân coroutine đang chạy?', 'Redraw (on paper) the Job state machine with its six states and arrows. Which states are final? In which state does the coroutine body run?')
    B(C, S, 1, 'ans', 'New → Active → Completing → Completed; Active/Completing → Cancelling → Cancelled. Cuối: Completed, Cancelled. Thân chạy ở Active.', 'New → Active → Completing → Completed; Active/Completing → Cancelling → Cancelled. Final: Completed, Cancelled. The body runs in Active.')
    B(C, S, 2, 'ask', 'Vì sao `join()` trên `Job()` có thể chờ mãi, còn `join()` trên Job do `launch` trả về thì không?', 'Why can `join()` on a `Job()` wait forever, while `join()` on a Job returned by `launch` does not?')
    B(C, S, 2, 'ans', 'Job của `launch` gắn với một thân coroutine: thân xong và con xong thì tự sang Completed. `Job()` không có thân, nên không có gì đẩy nó ra khỏi Active, trừ khi bạn gọi `complete()`/`cancel()`.', 'A `launch` Job is tied to a coroutine body: once the body and the children finish, it moves to Completed by itself. A `Job()` has no body, so nothing pushes it out of Active unless you call `complete()`/`cancel()`.')
