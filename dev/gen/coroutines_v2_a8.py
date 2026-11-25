# Coroutines v2 · Phần 2 · A8 (phần 1) Tự dựng coroutine scope (Deep Dive, "Constructing a coroutine scope", tr. PDF 173–182).
# Viết thêm vào A8 (giữ id a8, các sim lifecycle/effects và mục v1 scopes, effects, bridge).

SEC_ORDER = {'a8': ['recap', 'iface', 'factory', 'android', 'vmscope', 'extra', 'scopes', 'effects', 'bridge', 'bugs', 'exercises', 'recall']}


def add(a):
    def B(ch, sec, n, field, vi, en=None):
        a('%s.sec.%s.b.%02d.%s' % (ch, sec, n, field), vi, vi if en is None else en)
    C = 'a8'

    S = 'recap'
    a(C + '.sec.%s.title' % S, 'Ôn nhanh: những gì cần để dựng một scope', 'Quick review: what you need to build a scope')
    B(C, S, 1, 'ask', 'Một scope cho màn hình Android cần những phần tử context nào, và mỗi phần tử để làm gì? (Gợi ý: luồng, quan hệ giữa các con, lỗi chưa bắt.)', 'Which context elements does a scope for an Android screen need, and what is each for? (Hint: the thread, the relationship between children, uncaught errors.)')
    B(C, S, 1, 'ans', '`Dispatchers.Main` (hoặc `Main.immediate`): mặc định chạy trên luồng UI. `SupervisorJob()`: các coroutine độc lập, một cái lỗi không kéo cái khác, và có Job để hủy. `CoroutineExceptionHandler` (tuỳ chọn): xử lý chung lỗi chưa bắt. Chương này ghép chúng lại.', '`Dispatchers.Main` (or `Main.immediate`): run on the UI thread by default. `SupervisorJob()`: independent coroutines, so one failing does not drag the others, plus a Job to cancel. `CoroutineExceptionHandler` (optional): common handling of uncaught errors. This chapter puts them together.')

    S = 'iface'
    a(C + '.sec.%s.title' % S, 'Đừng cho lớp hiện thực CoroutineScope; hãy giữ scope trong một thuộc tính', 'Do not make a class implement CoroutineScope; keep a scope in a property')
    a(C + '.sec.%s.badge' % S, 'stable')
    B(C, S, 1, 'p', '`CoroutineScope` chỉ là interface có một thuộc tính `coroutineContext`, nên một lớp có thể hiện thực nó và gọi builder trực tiếp. Tiện, nhưng có vấn đề: trong lớp đó, mọi hàm của `CoroutineScope` như `cancel()`, `ensureActive()`, `isActive` đều gọi được trực tiếp. Lỡ tay `cancel()` là cả scope bị hủy và không coroutine nào khởi động được nữa. Thường người ta giữ scope trong một thuộc tính rồi gọi `scope.launch { }`.', '`CoroutineScope` is just an interface with one `coroutineContext` property, so a class can implement it and call builders directly. Convenient, but problematic: inside that class, every `CoroutineScope` member such as `cancel()`, `ensureActive()`, `isActive` can be called directly. One accidental `cancel()` cancels the whole scope, and no coroutine can start any more. The usual approach is to keep a scope in a property and call `scope.launch { }`.')
    B(C, S, 2, 'kt', '// không phổ biến\nclass SomeClass : CoroutineScope {\n    override val coroutineContext: CoroutineContext = Job()\n    fun onStart() { launch { /* ... */ } }\n}\n\n// nên dùng\nclass SomeClass {\n    val scope: CoroutineScope = CoroutineScope(SupervisorJob() + Dispatchers.Main)\n    fun onStart() { scope.launch { /* ... */ } }\n}', '// uncommon\nclass SomeClass : CoroutineScope {\n    override val coroutineContext: CoroutineContext = Job()\n    fun onStart() { launch { /* ... */ } }\n}\n\n// preferred\nclass SomeClass {\n    val scope: CoroutineScope = CoroutineScope(SupervisorJob() + Dispatchers.Main)\n    fun onStart() { scope.launch { /* ... */ } }\n}')

    S = 'factory'
    a(C + '.sec.%s.title' % S, 'Hàm CoroutineScope(context): tự thêm Job nếu thiếu', 'The CoroutineScope(context) function: adds a Job if missing')
    a(C + '.sec.%s.badge' % S, 'stable')
    B(C, S, 1, 'p', 'Cách dễ nhất tạo scope là hàm factory `CoroutineScope(context)` (một "constructor giả" như `Job()`). Nó tạo scope với context bạn đưa, và thêm một `Job()` nếu context chưa có Job, để structured concurrency hoạt động (có gì để hủy, để làm cha) ([[src:kx-scopefn]]):', 'The easiest way to create a scope is the factory function `CoroutineScope(context)` (a "fake constructor" like `Job()`). It creates a scope with the context you give, adding a `Job()` if the context has none, so structured concurrency works (there is something to cancel and to act as parent) ([[src:kx-scopefn]]):')
    B(C, S, 2, 'kt', 'public fun CoroutineScope(context: CoroutineContext): CoroutineScope =\n    ContextScope(if (context[Job] != null) context else context + Job())')

    S = 'android'
    a(C + '.sec.%s.title' % S, 'Dựng scope cho ViewModel, từng bước', 'Building a ViewModel scope, step by step')
    a(C + '.sec.%s.badge' % S, 'stable')
    B(C, S, 1, 'p', 'Trong MVVM/MVP, coroutine thường được khởi động ở ViewModel/Presenter; các tầng khác (use case, repository) chỉ có hàm suspend. Dựng scope một lần trong `BaseViewModel`, bốn bước:', 'In MVVM/MVP, coroutines are usually started in ViewModels/Presenters; other layers (use cases, repositories) only have suspending functions. Build the scope once in a `BaseViewModel`, in four steps:')
    B(C, S, 2, 'p',
      '1. Dispatcher: nhiều hàm Android phải gọi trên Main, nên `Dispatchers.Main` là mặc định tốt nhất.\n'
      '2. Hủy được: cần một Job, rồi hủy trong `onCleared()`. Tốt hơn nữa là chỉ hủy CON (`cancelChildren()`) thay vì cả scope, để scope vẫn dùng được nếu cần.\n'
      '3. Độc lập: dùng `SupervisorJob` thay `Job`, để lỗi tải user không chặn việc hiện tin tức.\n'
      '4. Lỗi chưa bắt: thêm `CoroutineExceptionHandler` gọi một hàm xử lý chung (ví dụ 401 thì mở màn đăng nhập, 503 thì báo lỗi máy chủ), hoặc đẩy lỗi vào một `LiveData`/`StateFlow` cho UI quan sát.',
      '1. Dispatcher: many Android functions must be called on Main, so `Dispatchers.Main` is the best default.\n'
      '2. Cancellable: you need a Job, then cancel it in `onCleared()`. Even better, cancel only the CHILDREN (`cancelChildren()`) instead of the whole scope, so the scope stays usable if needed.\n'
      '3. Independent: use `SupervisorJob` instead of `Job`, so a failure loading the user does not stop the news from showing.\n'
      '4. Uncaught errors: add a `CoroutineExceptionHandler` that calls a common handler (for example, 401 opens the login screen, 503 shows a server error), or pushes the error into a `LiveData`/`StateFlow` for the UI to observe.')
    B(C, S, 3, 'kt', 'abstract class BaseViewModel(private val onError: (Throwable) -> Unit) : ViewModel() {\n    private val exceptionHandler = CoroutineExceptionHandler { _, throwable -> onError(throwable) }\n    private val context = Dispatchers.Main + SupervisorJob() + exceptionHandler\n    protected val scope = CoroutineScope(context)\n\n    override fun onCleared() {\n        context.cancelChildren()\n    }\n}')

    S = 'vmscope'
    a(C + '.sec.%s.title' % S, 'viewModelScope và lifecycleScope làm sẵn đúng việc đó', 'viewModelScope and lifecycleScope do exactly that for you')
    a(C + '.sec.%s.badge' % S, 'stable impl')
    B(C, S, 1, 'p', 'Ứng dụng Android hiện đại thường không tự dựng mà dùng `viewModelScope` (từ `lifecycle-viewmodel-ktx` 2.2.0) hoặc `lifecycleScope` (`lifecycle-runtime-ktx` 2.2.0). Chúng gần như y hệt thứ ta vừa dựng: `SupervisorJob` + `Dispatchers.Main.immediate`, và hủy khi ViewModel bị xoá hoặc lifecycle owner bị huỷ. Bản Marcin Moskała trình bày (lifecycle 2.4.0) lưu scope làm "tag" của ViewModel và đóng nó khi `onCleared`. Bản mới (androidx-main) chuyển sang `CloseableCoroutineScope` trong `lifecycle-viewmodel` (commonMain), vẫn dùng `Dispatchers.Main.immediate` ([[src:ax-vmscope]]).', 'Modern Android apps usually do not build their own, but use `viewModelScope` (from `lifecycle-viewmodel-ktx` 2.2.0) or `lifecycleScope` (`lifecycle-runtime-ktx` 2.2.0). They are almost identical to what we just built: `SupervisorJob` + `Dispatchers.Main.immediate`, cancelled when the ViewModel is cleared or the lifecycle owner is destroyed. The version Marcin Moskała shows (lifecycle 2.4.0) stores the scope as a ViewModel "tag" and closes it in `onCleared`. The newer version (androidx-main) moved to `CloseableCoroutineScope` in `lifecycle-viewmodel` (commonMain), still using `Dispatchers.Main.immediate` ([[src:ax-vmscope]]).')
    B(C, S, 2, 'kt', '// bản lifecycle-viewmodel-ktx 2.4.0, rút gọn\npublic val ViewModel.viewModelScope: CoroutineScope\n    get() = getTag(JOB_KEY) ?: setTagIfAbsent(\n        JOB_KEY,\n        CloseableCoroutineScope(SupervisorJob() + Dispatchers.Main.immediate)\n    )\n\ninternal class CloseableCoroutineScope(context: CoroutineContext) : Closeable, CoroutineScope {\n    override val coroutineContext: CoroutineContext = context\n    override fun close() { coroutineContext.cancel() }\n}', '// the lifecycle-viewmodel-ktx 2.4.0 version, condensed\npublic val ViewModel.viewModelScope: CoroutineScope\n    get() = getTag(JOB_KEY) ?: setTagIfAbsent(\n        JOB_KEY,\n        CloseableCoroutineScope(SupervisorJob() + Dispatchers.Main.immediate)\n    )\n\ninternal class CloseableCoroutineScope(context: CoroutineContext) : Closeable, CoroutineScope {\n    override val coroutineContext: CoroutineContext = context\n    override fun close() { coroutineContext.cancel() }\n}')
    B(C, S, 3, 'p', 'Dùng `viewModelScope`/`lifecycleScope` là tiện và được khuyến nghị khi không cần context đặc biệt (như `CoroutineExceptionHandler`). Khi đó, lỗi thường được xử lý bằng `try/catch` trong từng coroutine và đưa vào state cho UI.', 'Using `viewModelScope`/`lifecycleScope` is convenient and recommended when you need no special context (such as a `CoroutineExceptionHandler`). Errors are then usually handled with `try/catch` inside each coroutine and turned into UI state.')

    S = 'extra'
    a(C + '.sec.%s.title' % S, 'Scope cho việc phụ và scope phía backend', 'Scopes for side work, and on the backend')
    a(C + '.sec.%s.badge' % S, 'stable')
    B(C, S, 1, 'p', 'Việc phụ (analytics, log) nên chạy trên một scope riêng được inject (chương SF). Đủ là `CoroutineScope(SupervisorJob())`; thêm `CoroutineExceptionHandler` nếu muốn gửi lỗi lên hệ thống theo dõi, và `Dispatchers.IO` nếu có lời gọi chặn. Phía backend (Spring cũ, tác vụ nền), scope thường gồm dispatcher có giới hạn (ví dụ `Dispatchers.IO.limitedParallelism(5)`), `SupervisorJob`, và handler. Scope được định nghĩa một lần, inject qua constructor để dùng chung và để thay bằng scope test.', 'Side work (analytics, logging) should run on a separate, injected scope (SF chapter). `CoroutineScope(SupervisorJob())` is enough; add a `CoroutineExceptionHandler` to send errors to monitoring, and `Dispatchers.IO` if there are blocking calls. On the backend (older Spring, background tasks), a scope usually combines a limited dispatcher (for example `Dispatchers.IO.limitedParallelism(5)`), a `SupervisorJob` and a handler. The scope is defined once and injected through the constructor, so it is shared and can be swapped for a test scope.')

    S = 'bugs'
    a(C + '.sec.%s.title' % S, 'Bug thường gặp khi dựng scope', 'Common bugs when building scopes')
    a(C + '.sec.%s.badge' % S, 'stable')
    B(C, S, 1, 'bug', 'Một "manager" dùng chung giữa nhiều màn hình có `fun stop() { scope.cancel() }`. Sau khi một màn hình gọi `stop()`, mọi `scope.launch { }` về sau không làm gì cả: không lỗi, không log.', 'A "manager" shared across screens has `fun stop() { scope.cancel() }`. After one screen calls `stop()`, every later `scope.launch { }` does nothing: no error, no log.')
    B(C, S, 1, 'cause', 'Một scope (Job) đã bị hủy không làm cha cho coroutine mới được nữa: `launch` trên nó tạo ra coroutine bị hủy ngay lập tức.', 'A cancelled scope (Job) can no longer be the parent of new coroutines: `launch` on it creates a coroutine that is cancelled immediately.')
    B(C, S, 1, 'fix', 'Dùng `scope.coroutineContext.cancelChildren()` để dừng việc đang chạy mà giữ scope dùng tiếp. Chỉ `cancel()` cả scope khi đối tượng sở hữu nó kết thúc vòng đời.', 'Use `scope.coroutineContext.cancelChildren()` to stop running work while keeping the scope usable. Only `cancel()` the whole scope when its owning object reaches the end of its life.')
    B(C, S, 2, 'bug', '`BaseViewModel` dùng `CoroutineScope(Dispatchers.Main + Job())`. Khi một request lỗi, mọi coroutine khác của ViewModel ngừng, và các nút bấm sau đó không còn phản hồi.', '`BaseViewModel` uses `CoroutineScope(Dispatchers.Main + Job())`. When one request fails, every other coroutine of the ViewModel stops, and later button taps no longer respond.')
    B(C, S, 2, 'cause', 'Job thường: con lỗi thì hủy cha (scope), và scope bị hủy thì không khởi động được con mới. Một lỗi làm "chết" cả ViewModel.', 'An ordinary Job: a failing child cancels the parent (the scope), and a cancelled scope cannot start new children. One failure "kills" the whole ViewModel.')
    B(C, S, 2, 'fix', 'Dùng `SupervisorJob()`, hoặc đơn giản là `viewModelScope`.', 'Use `SupervisorJob()`, or simply `viewModelScope`.')
    B(C, S, 3, 'bug', 'Test của repository thỉnh thoảng thất bại ngẫu nhiên vì coroutine của test trước vẫn đang chạy và ghi vào fake DB.', 'Repository tests fail randomly now and then because a previous test\'s coroutines are still running and writing into the fake DB.')
    B(C, S, 3, 'cause', 'Repository tự tạo `CoroutineScope(SupervisorJob())` bên trong (hoặc dùng `GlobalScope`). Test không kiểm soát và không hủy được scope đó, nên việc nền sống sang test sau.', 'The repository creates its own `CoroutineScope(SupervisorJob())` internally (or uses `GlobalScope`). The test cannot control or cancel that scope, so background work survives into the next test.')
    B(C, S, 3, 'fix', 'Inject scope qua constructor; trong test truyền scope của `runTest` (`backgroundScope` hoặc một `TestScope`) để mọi việc bị dọn khi test kết thúc.', 'Inject the scope through the constructor; in tests pass a scope from `runTest` (`backgroundScope` or a `TestScope`), so everything is cleaned up when the test ends.')

    S = 'exercises'
    a(C + '.sec.%s.title' % S, 'Bài tập', 'Exercises')
    a(C + '.sec.%s.badge' % S, 'stable')
    B(C, S, 1, 'ex', 'Đoán output:', 'Predict the output:')
    B(C, S, 1, 'exkt', 'suspend fun main() {\n    val scope = CoroutineScope(SupervisorJob())\n    scope.cancel()\n    val job = scope.launch { println("A") }\n    job.join()\n    println("cancelled=${job.isCancelled}")\n}')
    B(C, S, 1, 'sol', 'Chỉ "cancelled=true": "A" không in. Scope đã hủy nên coroutine mới bị hủy ngay khi được tạo, trước khi thân kịp chạy.', 'Only "cancelled=true": "A" never prints. The scope is cancelled, so the new coroutine is cancelled as soon as it is created, before its body gets to run.')
    B(C, S, 2, 'ex', 'Bài khuyết bước: viết `AppScope` dùng cho việc nền toàn ứng dụng (đồng bộ, analytics): không phụ thuộc màn hình, lỗi không làm chết scope, gửi lỗi lên Crashlytics, có thể có lời gọi chặn, và thay được trong test.', 'A partly-solved exercise: write an `AppScope` for app-wide background work (sync, analytics): independent of screens, errors must not kill the scope, errors go to Crashlytics, blocking calls may happen, and it must be replaceable in tests.')
    B(C, S, 2, 'hint', 'Ba phần tử context + inject qua DI (ví dụ một `@Provides` trong Hilt).', 'Three context elements + injection through DI (for example a Hilt `@Provides`).')
    B(C, S, 2, 'sol', '`SupervisorJob()` để lỗi không lan; `Dispatchers.IO` vì có lời gọi chặn; `CoroutineExceptionHandler` gửi Crashlytics. Cung cấp qua DI để test truyền scope khác.', '`SupervisorJob()` so errors do not spread; `Dispatchers.IO` for blocking calls; a `CoroutineExceptionHandler` that reports to Crashlytics. Provide it through DI so tests can pass a different scope.')
    B(C, S, 2, 'solkt', '@Provides @Singleton\nfun provideAppScope(): CoroutineScope = CoroutineScope(\n    SupervisorJob() +\n    Dispatchers.IO +\n    CoroutineExceptionHandler { _, e -> FirebaseCrashlytics.getInstance().recordException(e) }\n)')

    S = 'recall'
    a(C + '.sec.%s.title' % S, 'Tự trả lời', 'Answer it yourself')
    a(C + '.sec.%s.badge' % S, 'stable')
    B(C, S, 1, 'ask', 'Vì sao `onCleared()` nên `cancelChildren()` thay vì `cancel()`? Vì sao `SupervisorJob` chứ không phải `Job`?', 'Why should `onCleared()` call `cancelChildren()` rather than `cancel()`? Why `SupervisorJob` rather than `Job`?')
    B(C, S, 1, 'ans', '`cancelChildren()` dừng mọi việc đang chạy nhưng scope vẫn khởi động được coroutine mới; `cancel()` làm scope "chết" vĩnh viễn. `SupervisorJob` để các coroutine độc lập: một cái lỗi không hủy cái khác hay hủy scope.', '`cancelChildren()` stops all running work but the scope can still start new coroutines; `cancel()` makes the scope "dead" for good. `SupervisorJob` keeps coroutines independent: one failing does not cancel the others or the scope.')
