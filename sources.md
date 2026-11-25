# Nguồn / Sources

Sinh tự động từ registry của site (dev/tools/sources-md.js). Generated from the site registry. Ngày đối chiếu / checked: 2026-11-20 … 2026-11-25.

## Phiên bản và ngày đối chiếu / Versions and check dates

- Kotlin: 2.4.21
- kotlinx.coroutines: 1.11.0
- Compose BOM: 2026.11.01 (runtime 1.13.0, ui 1.13.0, animation 1.13.0, material3 1.5.0)
- Compose Compiler: org.jetbrains.kotlin.plugin.compose 2.4.21 — Đi kèm Kotlin; strong skipping bật mặc định từ Kotlin 2.0.20. / Ships with Kotlin; strong skipping is on by default since Kotlin 2.0.20.
- AndroidX Lifecycle: 2.11.1
- WCAG: 2.2 (W3C Recommendation 2024-12-12)
- Material 3: 2026-11-20 — Ngày đối chiếu. Giá trị token cụ thể được ghi ở track dùng đến. / Cross-check date. Specific token values are recorded in the track that uses them.
- Android design guidance: 2026-11-20 — Ngày đối chiếu. Giá trị cụ thể được ghi ở track dùng đến. / Cross-check date. Specific values are recorded in the track that uses them.

## Nguồn chính thức, chuẩn và thứ cấp / Official, normative and secondary sources

Nguồn chính thức hoặc chuẩn luôn thắng khi mâu thuẫn với nguồn thứ cấp (ví dụ lawsofux.com chỉ là nguồn thứ cấp). Official or normative sources win over secondary ones (for example lawsofux.com is secondary only). Mục "đọc thêm" chưa được dùng làm nguồn cho khẳng định cụ thể / "Further reading" items are not yet the source of a specific claim.

### Track A

- **Processes and threads overview** — Android Developers · `stable`
  https://developer.android.com/guide/components/processes-and-threads
  - vi: Luồng Main xử lý sự kiện và vẽ UI; bộ công cụ UI không thread-safe nên chỉ sửa view từ luồng UI (U1).
  - en: The Main thread handles events and draws the UI; the UI toolkit is not thread-safe, so views are changed only from the UI thread (U1).
- **NetworkOnMainThreadException** — Android Developers · `stable`
  https://developer.android.com/reference/android/os/NetworkOnMainThreadException
  - vi: Ném ra khi ứng dụng gọi mạng trên luồng chính (U1).
  - en: Thrown when an app performs a networking operation on its main thread (U1).
- **ANRs** — Android Developers · `stable`
  https://developer.android.com/topic/performance/issues/anr
  - vi: ANR khi luồng chính không phản hồi sự kiện nhập trong khoảng 5 giây (U1).
  - en: An ANR occurs when the main thread does not respond to an input event within about 5 seconds (U1).
- **Sequences** — JetBrains (kotlinlang.org) · `stable`
  https://kotlinlang.org/docs/sequences.html
  - vi: Sequence tính lười, `sequence { }` và `yield`, so với collection (U2).
  - en: Lazy sequences, `sequence { }` and `yield`, compared with collections (U2).
- **RestrictsSuspension** — JetBrains (kotlinlang.org) · `stable`
  https://kotlinlang.org/api/core/kotlin-stdlib/kotlin.coroutines/-restricts-suspension/
  - vi: Khối có receiver đánh dấu `@RestrictsSuspension` chỉ được gọi hàm suspend của chính receiver đó (U2).
  - en: A block whose receiver is annotated `@RestrictsSuspension` may only call that receiver’s own suspending functions (U2).
- **suspendCoroutine** — JetBrains (kotlinlang.org) · `stable`
  https://kotlinlang.org/api/core/kotlin-stdlib/kotlin.coroutines/suspend-coroutine.html
  - vi: Lấy continuation hiện tại trong lambda rồi suspend coroutine (U3).
  - en: Obtains the current continuation inside a lambda and suspends the coroutine (U3).
- **Continuation** — JetBrains (kotlinlang.org) · `stable`
  https://kotlinlang.org/api/core/kotlin-stdlib/kotlin.coroutines/-continuation/
  - vi: Interface `Continuation`: `context` và `resumeWith(Result)`; `resume`/`resumeWithException` là extension (U3).
  - en: The `Continuation` interface: `context` and `resumeWith(Result)`; `resume`/`resumeWithException` are extensions (U3).
- **delay** — JetBrains (kotlinx.coroutines API) · `stable`
  https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/delay.html
  - vi: `delay` suspend mà không chặn luồng; có thể hủy (U3).
  - en: `delay` suspends without blocking a thread and is cancellable (U3).
- **suspendCancellableCoroutine** — JetBrains (kotlinx.coroutines API) · `stable`
  https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/suspend-cancellable-coroutine.html
  - vi: Gói callback thành hàm suspend có hỗ trợ hủy, `invokeOnCancellation` (U3).
  - en: Wraps a callback into a cancellable suspending function, with `invokeOnCancellation` (U3).
- **KEEP: Kotlin Coroutines (design document)** — JetBrains (Kotlin KEEP) · `impl`
  https://github.com/Kotlin/KEEP/blob/master/proposals/coroutines.md
  - vi: Tài liệu thiết kế: continuation-passing style, state machine, COROUTINE_SUSPENDED, phần ngôn ngữ và phần thư viện (U4).
  - en: The design document: continuation-passing style, state machines, COROUTINE_SUSPENDED, language part vs library part (U4).
- **Debugging coroutines (kotlinx.coroutines)** — JetBrains (kotlinx.coroutines) · `stable`
  https://kotlinlang.org/docs/coroutines-debugging.html
  - vi: Chế độ debug, tên coroutine, khôi phục stack trace, kotlinx-coroutines-debug (U4).
  - en: Debug mode, coroutine names, stack-trace recovery, kotlinx-coroutines-debug (U4).
- **Debug coroutines using IntelliJ IDEA** — JetBrains (kotlinlang.org) · `stable`
  https://kotlinlang.org/docs/debug-coroutines-with-idea.html
  - vi: Biến "was optimized out" sau điểm suspend; tuỳ chọn `-Xdebug` và cảnh báo không dùng cho production vì có thể rò bộ nhớ (U4).
  - en: Variables that "were optimized out" after a suspension point; the `-Xdebug` option and the warning never to use it in production because it can leak memory (U4).
- **launch** — JetBrains (kotlinx.coroutines API) · `stable`
  https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/launch.html
  - vi: `launch` khởi động coroutine không chặn luồng, trả về `Job` (A3).
  - en: `launch` starts a coroutine without blocking the thread and returns a `Job` (A3).
- **async** — JetBrains (kotlinx.coroutines API) · `stable`
  https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/async.html
  - vi: `async` trả về `Deferred`; kết quả và exception lấy qua `await` (A3).
  - en: `async` returns a `Deferred`; the result and any exception come through `await` (A3).
- **runBlocking** — JetBrains (kotlinx.coroutines API) · `stable`
  https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/run-blocking.html
  - vi: `runBlocking` chạy coroutine mới và chặn luồng hiện tại tới khi xong; không dùng bên trong coroutine (A3).
  - en: `runBlocking` runs a new coroutine and blocks the current thread until it completes; not to be used from inside a coroutine (A3).
- **coroutineScope** — JetBrains (kotlinx.coroutines API) · `stable`
  https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/coroutine-scope.html
  - vi: `coroutineScope` tạo scope trong hàm suspend, chờ mọi con, lỗi ở con hủy các con khác (A3).
  - en: `coroutineScope` creates a scope inside a suspending function, waits for every child, and a failing child cancels the others (A3).
- **asContextElement** — JetBrains (kotlinx.coroutines API) · `stable`
  https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/as-context-element.html
  - vi: Bọc `ThreadLocal` thành phần tử context: đặt và khôi phục giá trị mỗi khi coroutine chạy trên một luồng (A4).
  - en: Wraps a `ThreadLocal` as a context element: sets and restores the value whenever the coroutine runs on a thread (A4).
- **Job** — JetBrains (kotlinx.coroutines API) · `stable`
  https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/-job/
  - vi: Vòng đời Job, bảng cờ isActive/isCompleted/isCancelled, quan hệ cha–con (A2).
  - en: The Job lifecycle, the isActive/isCompleted/isCancelled flag table, parent–child relations (A2).
- **Job() (factory function)** — JetBrains (kotlinx.coroutines API) · `stable`
  https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/-job.html
  - vi: Tạo `CompletableJob` ở trạng thái Active; tham số parent (A2).
  - en: Creates a `CompletableJob` in the Active state; the parent parameter (A2).
- **NonCancellable** — JetBrains (kotlinx.coroutines API) · `stable`
  https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/-non-cancellable/
  - vi: Job không thể hủy, chỉ dùng với `withContext` cho khối cần chạy dù đã bị hủy (A5).
  - en: A Job that cannot be cancelled, meant only for `withContext` blocks that must run despite cancellation (A5).
- **SupervisorJob()** — JetBrains (kotlinx.coroutines API) · `stable`
  https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/-supervisor-job.html
  - vi: Lỗi của một con không hủy supervisor và các con khác (A6).
  - en: A child failure does not cancel the supervisor or the other children (A6).
- **supervisorScope** — JetBrains (kotlinx.coroutines API) · `stable`
  https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/supervisor-scope.html
  - vi: Scope kiểu supervisor trong hàm suspend; lỗi của con trực tiếp không lan lên (A6).
  - en: A supervisor-style scope inside a suspending function; direct children failures do not propagate (A6).
- **CoroutineExceptionHandler** — JetBrains (kotlinx.coroutines API) · `stable`
  https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/-coroutine-exception-handler/
  - vi: Xử lý exception chưa bắt ở coroutine gốc; không chặn lan truyền (A6).
  - en: Handles uncaught exceptions at the root coroutine; does not stop propagation (A6).
- **GlobalScope** — JetBrains (kotlinx.coroutines API) · `stable`
  https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/-global-scope/
  - vi: Scope toàn cục không gắn Job; coroutine trên nó không có cha, dễ rò (SF).
  - en: A global scope with no Job; coroutines on it have no parent and leak easily (SF).
- **withTimeout** — JetBrains (kotlinx.coroutines API) · `stable`
  https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/with-timeout.html
  - vi: Giới hạn thời gian cho khối; ném TimeoutCancellationException (SF).
  - en: A time limit for a block; throws TimeoutCancellationException (SF).
- **Dispatchers** — JetBrains (kotlinx.coroutines API) · `stable`
  https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/-dispatchers/
  - vi: Default, Main, IO (64 luồng hoặc số nhân), Unconfined; IO.limitedParallelism tạo giới hạn độc lập (A4).
  - en: Default, Main, IO (64 threads or the number of cores), Unconfined; IO.limitedParallelism creates an independent limit (A4).
- **ContinuationInterceptor** — JetBrains (kotlinlang.org) · `stable`
  https://kotlinlang.org/api/core/kotlin-stdlib/kotlin.coroutines/-continuation-interceptor/
  - vi: Phần tử context chặn continuation; nền tảng của dispatcher (A4).
  - en: The context element that intercepts continuations; the basis of dispatchers (A4).
- **AndroidX lifecycle: CloseableCoroutineScope.kt (androidx-main, đọc 2026-11-22)** — Google (AndroidX source) · `impl`
  https://github.com/androidx/androidx/blob/androidx-main/lifecycle/lifecycle-viewmodel/src/commonMain/kotlin/androidx/lifecycle/viewmodel/internal/CloseableCoroutineScope.kt
  - vi: viewModelScope được tạo với Dispatchers.Main.immediate (A4, U1).
  - en: viewModelScope is created with Dispatchers.Main.immediate (A4, U1).
- **CoroutineScope() (factory function)** — JetBrains (kotlinx.coroutines API) · `stable`
  https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/-coroutine-scope.html
  - vi: Tạo scope từ context, thêm Job() nếu context chưa có Job (A8).
  - en: Creates a scope from a context, adding a Job() if the context has none (A8).
- **Mutex** — JetBrains (kotlinx.coroutines API) · `stable`
  https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.sync/-mutex/
  - vi: Khoá loại trừ không reentrant; chờ bằng suspend; withLock (A9).
  - en: A non-reentrant mutual-exclusion lock; waiting suspends; withLock (A9).
- **Semaphore** — JetBrains (kotlinx.coroutines API) · `stable`
  https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.sync/-semaphore/
  - vi: Giới hạn số coroutine vào vùng găng cùng lúc; withPermit (A9).
  - en: Limits how many coroutines enter a critical section at once; withPermit (A9).
- **kotlinx-coroutines-test** — JetBrains (kotlinx.coroutines API) · `stable`
  https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-test/
  - vi: runTest, TestScope, StandardTestDispatcher, UnconfinedTestDispatcher, TestCoroutineScheduler, setMain, backgroundScope (A9).
  - en: runTest, TestScope, StandardTestDispatcher, UnconfinedTestDispatcher, TestCoroutineScheduler, setMain, backgroundScope (A9).
- **Channel** — JetBrains (kotlinx.coroutines API) · `stable`
  https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.channels/-channel/
  - vi: Sức chứa RENDEZVOUS/BUFFERED/UNLIMITED/CONFLATED, onBufferOverflow, onUndeliveredElement (CH).
  - en: RENDEZVOUS/BUFFERED/UNLIMITED/CONFLATED capacities, onBufferOverflow, onUndeliveredElement (CH).
- **produce** — JetBrains (kotlinx.coroutines API) · `stable`
  https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.channels/produce.html
  - vi: Builder trả về ReceiveChannel, đóng channel khi coroutine kết thúc (CH).
  - en: A builder returning a ReceiveChannel, closing it when the coroutine ends (CH).
- **select** — JetBrains (kotlinx.coroutines API) · `stable`
  https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.selects/select.html
  - vi: Chờ mệnh đề đầu tiên sẵn sàng: onAwait, onReceive, onSend (CH).
  - en: Waits for the first ready clause: onAwait, onReceive, onSend (CH).
- **channelFlow** — JetBrains (kotlinx.coroutines API) · `stable`
  https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.flow/channel-flow.html
  - vi: Flow lạnh có ProducerScope: sản xuất song song, launch bên trong, send (FB).
  - en: A cold flow with a ProducerScope: concurrent production, launch inside, send (FB).
- **callbackFlow** — JetBrains (kotlinx.coroutines API) · `stable`
  https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.flow/callback-flow.html
  - vi: Bọc API callback; ném IllegalStateException nếu khối kết thúc mà channel chưa đóng, nên phải awaitClose (FB).
  - en: Wraps callback APIs; throws IllegalStateException if the block returns while the channel is still open, hence awaitClose (FB).
- **flowOn** — JetBrains (kotlinx.coroutines API) · `stable`
  https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.flow/flow-on.html
  - vi: Đổi context cho phía trên (upstream) của flow (FB).
  - en: Changes the context of the flow upstream (FB).
- **StateFlow** — JetBrains (kotlinx.coroutines API) · `stable`
  https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.flow/-state-flow/index.html
  - vi: Giá trị được gộp bằng Any.equals giống distinctUntilChanged; áp distinctUntilChanged lên StateFlow không có tác dụng (FP).
  - en: Values are conflated with Any.equals like distinctUntilChanged; applying distinctUntilChanged to a StateFlow has no effect (FP).
- **flatMapMerge** — JetBrains (kotlinx.coroutines API) · `stable`
  https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.flow/flat-map-merge.html
  - vi: Gộp các flow con song song, tham số concurrency (mặc định DEFAULT_CONCURRENCY = 16) (FP).
  - en: Merges child flows concurrently, with a concurrency parameter (default DEFAULT_CONCURRENCY = 16) (FP).
- **flatMapLatest** — JetBrains (kotlinx.coroutines API) · `stable`
  https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.flow/flat-map-latest.html
  - vi: Phần tử mới hủy flow con trước (FP).
  - en: A new element cancels the previous child flow (FP).
- **zip** — JetBrains (kotlinx.coroutines API) · `stable`
  https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.flow/zip.html
  - vi: Ghép cặp hai flow; xong khi một flow xong (FP).
  - en: Pairs two flows; completes when one of them completes (FP).
- **combine** — JetBrains (kotlinx.coroutines API) · `stable`
  https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.flow/combine.html
  - vi: Ghép giá trị mới nhất của các flow (FP).
  - en: Combines the most recent values of the flows (FP).
- **retryWhen** — JetBrains (kotlinx.coroutines API) · `stable`
  https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.flow/retry-when.html
  - vi: Collect lại flow phía trên khi predicate trả true (FP).
  - en: Re-collects the upstream when the predicate returns true (FP).
- **kotlinx.coroutines: Combine.kt (zipImpl)** — JetBrains (mã nguồn kotlinx.coroutines) · `stable`
  https://github.com/Kotlin/kotlinx.coroutines/blob/master/kotlinx-coroutines-core/common/src/flow/internal/Combine.kt
  - vi: Mã nguồn zip: flow thứ nhất collect trong coroutine của zip, flow thứ hai trong produce rendezvous (FP).
  - en: zip source: the first flow is collected in zip’s coroutine, the second in a rendezvous produce (FP).
- **shareIn** — JetBrains (kotlinx.coroutines API) · `stable`
  https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.flow/share-in.html
  - vi: Biến Flow lạnh thành SharedFlow trong một scope; tham số started và replay (A7).
  - en: Turns a cold Flow into a SharedFlow in a scope; the started and replay parameters (A7).
- **stateIn** — JetBrains (kotlinx.coroutines API) · `stable`
  https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.flow/state-in.html
  - vi: Dạng suspend (chờ giá trị đầu) và dạng có initialValue + started (A7).
  - en: The suspending form (waits for the first value) and the form with initialValue + started (A7).
- **SharingStarted.WhileSubscribed** — JetBrains (kotlinx.coroutines API) · `stable`
  https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.flow/-sharing-started/-companion/-while-subscribed.html
  - vi: stopTimeoutMillis mặc định 0, replayExpirationMillis mặc định Long.MAX_VALUE (A7).
  - en: stopTimeoutMillis defaults to 0, replayExpirationMillis to Long.MAX_VALUE (A7).
- **MutableSharedFlow** — JetBrains (kotlinx.coroutines API) · `stable`
  https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.flow/-mutable-shared-flow/index.html
  - vi: replay, extraBufferCapacity, onBufferOverflow; tryEmit chỉ trả false khi SUSPEND và có người collect (A7).
  - en: replay, extraBufferCapacity, onBufferOverflow; tryEmit returns false only with SUSPEND and active collectors (A7).
- **UI layer: State production** — Android Developers · `stable`
  https://developer.android.com/topic/architecture/ui-layer/state-production
  - vi: Ví dụ stateIn(viewModelScope, SharingStarted.WhileSubscribed(5_000), …) (A7).
  - en: The stateIn(viewModelScope, SharingStarted.WhileSubscribed(5_000), …) example (A7).
- **suspendCancellableCoroutine** — JetBrains (kotlinx.coroutines API) · `stable`
  https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/suspend-cancellable-coroutine.html
  - vi: Bọc callback thành hàm suspend có hủy; invokeOnCancellation (PR).
  - en: Wraps a callback into a cancellable suspending function; invokeOnCancellation (PR).
- **CoroutineDispatcher.limitedParallelism** — JetBrains (kotlinx.coroutines API) · `stable`
  https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/-coroutine-dispatcher/limited-parallelism.html
  - vi: Dispatcher có giới hạn song song riêng (PR).
  - en: A dispatcher with its own parallelism limit (PR).
- **future (kotlinx.coroutines.future)** — JetBrains (kotlinx.coroutines API) · `stable`
  https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.future/future.html
  - vi: Builder trả về CompletableFuture cho người dùng Java (PR).
  - en: A builder returning a CompletableFuture for Java users (PR).
- **awaitAll** — JetBrains (kotlinx.coroutines API) · `stable`
  https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/await-all.html
  - vi: Chờ nhiều Deferred, thất bại ngay khi một cái thất bại (PR).
  - en: Awaits several Deferreds, failing as soon as one fails (PR).
- **Threading in CoroutineWorker** — Android Developers · `stable`
  https://developer.android.com/develop/background-work/background-tasks/persistent/threading/coroutineworker
  - vi: doWork() là hàm suspend; WorkManager chạy và hủy nó (PR).
  - en: doWork() is a suspending function; WorkManager runs and cancels it (PR).
- **kotlin-coroutines-recipes (Marcin Moskała)** — Tác giả sách (GitHub) · `stable`
  https://github.com/MarcinMoskala/kotlin-coroutines-recipes
  - vi: Mã và test của các công thức mapAsync, suspendLazy, ConnectionPool, raceOf, retry (PR).
  - en: Code and tests for the mapAsync, suspendLazy, ConnectionPool, raceOf, retry recipes (PR).
- **Crashes (Android vitals)** — Android Developers · `stable`
  https://developer.android.com/topic/performance/vitals/crash
  - vi: App Java/Kotlin crash khi có exception không được xử lý (PR).
  - en: A Java/Kotlin app crashes on an unhandled exception (PR).
- **Kotlin Coroutines: Deep Dive (Marcin Moskała)** — Kt. Academy (sách) · `guideline`
  https://leanpub.com/coroutines
  - vi: Sách nguồn giảng chính của Coroutines v2: bố cục chương và ví dụ màn hình tin tức (U1 theo chương "Why Kotlin Coroutines?").
  - en: The main teaching source for Coroutines v2: chapter structure and the news-screen example (U1 follows the chapter "Why Kotlin Coroutines?").
- **Coroutines guide** — JetBrains (kotlinlang.org) · `stable`
  https://kotlinlang.org/docs/coroutines-guide.html
  - vi: Mục lục khái niệm của coroutine: nền cho bản đồ ở chương A0.
  - en: The conceptual index of coroutines: the basis for the overview map in chapter A0.
- **Coroutines basics** — JetBrains (kotlinlang.org) · `stable`
  https://kotlinlang.org/docs/coroutines-basics.html
  - vi: Coroutine, suspending function, scope và structured concurrency ở mức cơ bản (A1, A2).
  - en: Coroutines, suspending functions, scopes and structured concurrency at the basic level (A1, A2).
- **Composing suspending functions** — JetBrains (kotlinlang.org) · `stable`
  https://kotlinlang.org/docs/composing-suspending-functions.html
  - vi: Mặc định tuần tự, `async` cho đồng thời, và structured concurrency với `async`: lỗi trong scope hủy mọi con (A3).
  - en: Sequential by default, `async` for concurrency, and structured concurrency with `async`: a failure inside the scope cancels every child (A3).
- **Cancellation and timeouts** — JetBrains (kotlinlang.org) · `stable`
  https://kotlinlang.org/docs/coroutines-cancellation.html
  - vi: Hủy hợp tác, `isActive`, `ensureActive()`, `NonCancellable`, `withTimeoutOrNull` (A5). Thay cho URL cũ `cancellation-and-timeouts.html` chỉ là trang chuyển hướng.
  - en: Cooperative cancellation, `isActive`, `ensureActive()`, `NonCancellable`, `withTimeoutOrNull` (A5). Replaces the old `cancellation-and-timeouts.html` URL, which is only a redirect page.
- **Coroutine context and dispatchers** — JetBrains (kotlinlang.org) · `stable`
  https://kotlinlang.org/docs/coroutine-context-and-dispatchers.html
  - vi: Context, toán tử `+`, dispatcher, `withContext`, `CoroutineName`, quan hệ cha–con của Job (A2, A4).
  - en: Context, the `+` operator, dispatchers, `withContext`, `CoroutineName`, and the parent–child relation of Jobs (A2, A4).
- **Coroutine exceptions handling** — JetBrains (kotlinlang.org) · `stable`
  https://kotlinlang.org/docs/exception-handling.html
  - vi: `launch` và `async`, `CoroutineExceptionHandler`, `SupervisorJob`, `supervisorScope` (A6).
  - en: `launch` and `async`, `CoroutineExceptionHandler`, `SupervisorJob`, `supervisorScope` (A6).
- **Flows** — JetBrains (kotlinlang.org) · `stable`
  https://kotlinlang.org/docs/coroutines-flow.html
  - vi: Cold và hot flow, `flowOn`, `buffer`, xử lý exception, StateFlow và SharedFlow (A7). Thay cho URL cũ `flow.html` chỉ là trang chuyển hướng.
  - en: Cold and hot flows, `flowOn`, `buffer`, exception handling, StateFlow and SharedFlow (A7). Replaces the old `flow.html` URL, which is only a redirect page.
- **Flow operators** — JetBrains (kotlinlang.org) · `stable`
  https://kotlinlang.org/docs/coroutines-flow-operators.html
  - vi: `buffer`, `conflate`, `collectLatest` và cách chúng chạy upstream (A7). Trang này tách riêng khỏi trang Flows trong tài liệu hiện hành.
  - en: `buffer`, `conflate`, `collectLatest` and how they run the upstream (A7). This page is separate from the Flows page in the current documentation.
- **Channels** — JetBrains (kotlinlang.org) · `stable`
  https://kotlinlang.org/docs/channels.html
  - vi: Channel gần với BlockingQueue nhưng `send`/`receive` là suspend; fan-out; send và receive phục vụ theo thứ tự FIFO (A7).
  - en: A Channel is close to a BlockingQueue but `send`/`receive` suspend; fan-out; send and receive are served in first-in first-out order (A7).
- **Shared mutable state and concurrency** — JetBrains (kotlinlang.org) · `stable`
  https://kotlinlang.org/docs/shared-mutable-state-and-concurrency.html
  - vi: Volatile không đủ, thread confinement, Mutex, cấu trúc dữ liệu thread-safe (A9).
  - en: Volatile is not enough, thread confinement, Mutex, thread-safe data structures (A9).
- **Best practices for coroutines in Android** — Android Developers · `guideline`
  https://developer.android.com/kotlin/coroutines/coroutines-best-practices
  - vi: Inject dispatcher, main-safety, tránh `GlobalScope`, ViewModel tạo coroutine, không nuốt `CancellationException` (A0, A4, A5, A8).
  - en: Inject dispatchers, main-safety, avoid `GlobalScope`, let the ViewModel create coroutines, do not swallow `CancellationException` (A0, A4, A5, A8).
- **Use Kotlin coroutines with lifecycle-aware components** — Android Developers · `stable`
  https://developer.android.com/topic/libraries/architecture/coroutines
  - vi: `viewModelScope` và coroutine gắn với Composition bị hủy khi composable rời màn hình (A0, A8).
  - en: `viewModelScope` and Composition-bound coroutines are cancelled when the composable leaves the screen (A0, A8).
- **StateFlow and SharedFlow** — Android Developers · `stable`
  https://developer.android.com/kotlin/flow/stateflow-and-sharedflow
  - vi: StateFlow là state holder có giá trị hiện tại; SharedFlow có replay; `repeatOnLifecycle(STARTED)` (A7, A8).
  - en: StateFlow is a state holder with a current value; SharedFlow has replay; `repeatOnLifecycle(STARTED)` (A7, A8).
- **Testing Kotlin coroutines on Android** — Android Developers · `stable`
  https://developer.android.com/kotlin/coroutines/test
  - vi: `runTest`, `TestDispatcher`, `TestCoroutineScheduler`, virtual time; `withContext` làm delay không còn bị bỏ qua (A9).
  - en: `runTest`, `TestDispatcher`, `TestCoroutineScheduler`, virtual time; `withContext` stops delays from being skipped (A9).
- **Side-effects in Compose** — Android Developers · `stable`
  https://developer.android.com/develop/ui/compose/side-effects
  - vi: `LaunchedEffect` và `rememberCoroutineScope`: vòng đời coroutine theo Composition, key đổi thì chạy lại (A8, cầu nối X2).
  - en: `LaunchedEffect` and `rememberCoroutineScope`: coroutine lifetime follows the Composition, and a key change restarts it (A8, bridge X2).
- **State and Jetpack Compose** — Android Developers · `stable`
  https://developer.android.com/develop/ui/compose/state
  - vi: `collectAsStateWithLifecycle()` thu giá trị Flow theo lifecycle (A8).
  - en: `collectAsStateWithLifecycle()` collects Flow values in a lifecycle-aware way (A8).

### Track B

- **How Compose works (runtime design document)** — AndroidX (android.googlesource.com) · `impl`
  https://android.googlesource.com/platform/frameworks/support/+/296313a488a01c84ddcb0801d4efee640a14070c/compose/runtime/design/how-compose-works.md
  - vi: Composer, SlotTable (group, slot, gap buffer), skip, restart group, phát hiện thay đổi cấu trúc. Ghim androidx-main commit 296313a4 (2026-11-21); tài liệu tự cảnh báo vài chi tiết SlotTable có thể đã cũ (B0, B2, B3, B6).
  - en: Composer, SlotTable (groups, slots, gap buffer), skipping, restart groups, detecting structural changes. Pinned to androidx-main commit 296313a4 (2026-11-21); the document itself warns some SlotTable details may be outdated (B0, B2, B3, B6).
- **Composer.kt (androidx-main @296313a4)** — AndroidX (android.googlesource.com) · `impl`
  https://android.googlesource.com/platform/frameworks/support/+/296313a488a01c84ddcb0801d4efee640a14070c/compose/runtime/runtime/src/commonMain/kotlin/androidx/compose/runtime/Composer.kt
  - vi: Giao diện Composer mà mã compiler sinh gọi: startRestartGroup/endRestartGroup, skipToGroupEnd, startReplaceGroup, startMovableGroup, changed, skipping, ScopeUpdateScope.updateScope((Composer, Int) -> Unit) (B2).
  - en: The Composer interface that generated code calls: startRestartGroup/endRestartGroup, skipToGroupEnd, startReplaceGroup, startMovableGroup, changed, skipping, ScopeUpdateScope.updateScope((Composer, Int) -> Unit) (B2).
- **GapComposer.kt (androidx-main @296313a4)** — AndroidX (android.googlesource.com) · `impl`
  https://android.googlesource.com/platform/frameworks/support/+/296313a488a01c84ddcb0801d4efee640a14070c/compose/runtime/runtime/src/commonMain/kotlin/androidx/compose/runtime/GapComposer.kt
  - vi: Cài đặt Composer mặc định ở commit ghim: getter skipping, changed (so bằng !=) và changedInstance (!==), addRecomposeScope (requiresRecompose), skipToGroupEnd gọi recomposeToGroupEnd khi còn invalidation, endRestartGroup (B2).
  - en: The default Composer implementation at the pinned commit: the skipping getter, changed (compares with !=) and changedInstance (!==), addRecomposeScope (requiresRecompose), skipToGroupEnd calling recomposeToGroupEnd when invalidations remain, endRestartGroup (B2).
- **SnapshotMutationPolicy** — Android Developers · `stable`
  https://developer.android.com/reference/kotlin/androidx/compose/runtime/SnapshotMutationPolicy
  - vi: equivalent quyết định giá trị mới có là thay đổi không; merge gộp thay đổi xung đột giữa các snapshot; ví dụ counterPolicy (B4).
  - en: equivalent decides whether a new value counts as a change; merge combines conflicting changes between snapshots; the counterPolicy example (B4).
- **SnapshotState.kt (androidx-main @296313a4)** — AndroidX (android.googlesource.com) · `impl`
  https://android.googlesource.com/platform/frameworks/support/+/296313a488a01c84ddcb0801d4efee640a14070c/compose/runtime/runtime/src/commonMain/kotlin/androidx/compose/runtime/SnapshotState.kt
  - vi: mutableStateOf mặc định structuralEqualityPolicy; setter bỏ qua giá trị tương đương; mergeRecords giữ current nếu tương đương, không thì gọi policy.merge (B4).
  - en: mutableStateOf defaults to structuralEqualityPolicy; the setter ignores equivalent values; mergeRecords keeps current if equivalent, otherwise calls policy.merge (B4).
- **Snapshot.kt (androidx-main @296313a4)** — AndroidX (android.googlesource.com) · `impl`
  https://android.googlesource.com/platform/frameworks/support/+/296313a488a01c84ddcb0801d4efee640a14070c/compose/runtime/runtime/src/commonMain/kotlin/androidx/compose/runtime/snapshots/Snapshot.kt
  - vi: Bản ghi đọc được là bản ghi hợp lệ có snapshotId lớn nhất (id ≤ snapshot, không thuộc tập invalid) (B4).
  - en: The readable record is the valid record with the highest snapshotId (id ≤ the snapshot, not in the invalid set) (B4).
- **DerivedState.kt (androidx-main @296313a4)** — AndroidX (android.googlesource.com) · `impl`
  https://android.googlesource.com/platform/frameworks/support/+/296313a488a01c84ddcb0801d4efee640a14070c/compose/runtime/runtime/src/commonMain/kotlin/androidx/compose/runtime/DerivedState.kt
  - vi: derivedStateOf lưu cache kết quả; isInvalidFor so bằng policy hoặc structuralEqualityPolicy để scope chỉ chạy lại khi kết quả đổi (B4).
  - en: derivedStateOf caches its result; isInvalidFor compares with the policy or structuralEqualityPolicy so a scope re-runs only when the result changes (B4).
- **GlobalSnapshotManager.android.kt (androidx-main @296313a4)** — AndroidX (android.googlesource.com) · `android-impl`
  https://android.googlesource.com/platform/frameworks/support/+/296313a488a01c84ddcb0801d4efee640a14070c/compose/ui/ui/src/androidMain/kotlin/androidx/compose/ui/platform/GlobalSnapshotManager.android.kt
  - vi: Trên Android: global write observer gửi tín hiệu qua Channel(1), và sendApplyNotifications chạy trên AndroidUiDispatcher.Main (B4).
  - en: On Android: a global write observer signals through a Channel(1), and sendApplyNotifications runs on AndroidUiDispatcher.Main (B4).
- **Where to hoist state** — Android Developers · `stable`
  https://developer.android.com/develop/ui/compose/state-hoisting
  - vi: Screen UI state và UI element state; business logic và UI logic; composable, plain state holder, ViewModel làm chủ state; tổ tiên chung thấp nhất; property drilling; lưu ý MonotonicFrameClock (SH).
  - en: Screen UI state and UI element state; business and UI logic; composables, plain state holders and ViewModels as state owners; the lowest common ancestor; property drilling; the MonotonicFrameClock caveat (SH).
- **Save UI state in Compose** — Android Developers · `stable`
  https://developer.android.com/develop/ui/compose/state-saving
  - vi: Đổi cấu hình và process bị hệ thống dừng; rememberSaveable và Saver; giới hạn kích thước Bundle; ViewModel và SavedStateHandle; StateRestorationTester (SH).
  - en: Configuration changes and system-initiated process death; rememberSaveable and Savers; the Bundle size limit; ViewModel and SavedStateHandle; StateRestorationTester (SH).
- **Recomposer.kt (androidx-main @296313a4)** — AndroidX (android.googlesource.com) · `impl`
  https://android.googlesource.com/platform/frameworks/support/+/296313a488a01c84ddcb0801d4efee640a14070c/compose/runtime/runtime/src/commonMain/kotlin/androidx/compose/runtime/Recomposer.kt
  - vi: Vòng runRecomposeAndApplyChanges: awaitWorkAvailable, recordComposerModifications, withFrameNanos; trong frame: sendFrame cho awaiter trước, rồi recompose (cả invalidation sinh trong frame), rồi applyChanges; pause/resumeCompositionFrameClock (B5).
  - en: The runRecomposeAndApplyChanges loop: awaitWorkAvailable, recordComposerModifications, withFrameNanos; within a frame: sendFrame to awaiters first, then recompose (including invalidations produced in the frame), then applyChanges; pause/resumeCompositionFrameClock (B5).
- **AndroidUiFrameClock.android.kt (androidx-main @296313a4)** — AndroidX (android.googlesource.com) · `android-impl`
  https://android.googlesource.com/platform/frameworks/support/+/296313a488a01c84ddcb0801d4efee640a14070c/compose/ui/ui/src/androidMain/kotlin/androidx/compose/ui/platform/AndroidUiFrameClock.android.kt
  - vi: withFrameNanos đăng ký Choreographer.FrameCallback và resume với thời điểm frame (B5).
  - en: withFrameNanos registers a Choreographer.FrameCallback and resumes with the frame time (B5).
- **WindowRecomposer.android.kt (androidx-main @296313a4)** — AndroidX (android.googlesource.com) · `android-impl`
  https://android.googlesource.com/platform/frameworks/support/+/296313a488a01c84ddcb0801d4efee640a14070c/compose/ui/ui/src/androidMain/kotlin/androidx/compose/ui/platform/WindowRecomposer.android.kt
  - vi: Recomposer theo window; ON_START resume, ON_STOP pauseCompositionFrameClock, ON_DESTROY cancel (B5).
  - en: A Recomposer per window; ON_START resumes, ON_STOP pauseCompositionFrameClock, ON_DESTROY cancels (B5).
- **Effects.kt (androidx-main @296313a4)** — AndroidX (android.googlesource.com) · `impl`
  https://android.googlesource.com/platform/frameworks/support/+/296313a488a01c84ddcb0801d4efee640a14070c/compose/runtime/runtime/src/commonMain/kotlin/androidx/compose/runtime/Effects.kt
  - vi: LaunchedEffect(key) = remember(key) { LaunchedEffectImpl }: launch ở onRemembered, cancel ở onForgotten/onAbandoned; gọi không có key là lỗi; SideEffect = recordSideEffect (EF).
  - en: LaunchedEffect(key) = remember(key) { LaunchedEffectImpl }: launches in onRemembered, cancels in onForgotten/onAbandoned; calling it without a key is an error; SideEffect = recordSideEffect (EF).
- **RememberObserver.kt (androidx-main @296313a4)** — AndroidX (android.googlesource.com) · `impl`
  https://android.googlesource.com/platform/frameworks/support/+/296313a488a01c84ddcb0801d4efee640a14070c/compose/runtime/runtime/src/commonMain/kotlin/androidx/compose/runtime/RememberObserver.kt
  - vi: onRemembered/onForgotten trên apply thread; onAbandoned khi không được remember thành công; thứ tự forgotten ngược thứ tự remembered (EF).
  - en: onRemembered/onForgotten on the apply thread; onAbandoned when not successfully remembered; forgotten in reverse order of remembered (EF).
- **Locally scoped data with CompositionLocal** — Android Developers · `stable`
  https://developer.android.com/develop/ui/compose/compositionlocal
  - vi: Truyền dữ liệu ngầm theo cây; MaterialTheme; nhà cung cấp gần nhất; compositionLocalOf và staticCompositionLocalOf; khi nào dùng; không đặt ViewModel; thay thế bằng tham số, đảo điều khiển, content lambda (CL).
  - en: Passing data implicitly down the tree; MaterialTheme; the nearest provider; compositionLocalOf vs staticCompositionLocalOf; when to use it; not for ViewModels; alternatives: parameters, inversion of control, content lambdas (CL).
- **CompositionLocal.kt (androidx-main @296313a4)** — AndroidX (android.googlesource.com) · `impl`
  https://android.googlesource.com/platform/frameworks/support/+/296313a488a01c84ddcb0801d4efee640a14070c/compose/runtime/runtime/src/commonMain/kotlin/androidx/compose/runtime/CompositionLocal.kt
  - vi: KDoc: static không theo dõi lần đọc nên đổi giá trị recompose toàn bộ content; nên dùng cho context, font loader; màu và giá trị theme có thể đổi hoặc animate nên dùng compositionLocalOf (CL).
  - en: KDoc: static reads are untracked, so a change recomposes the whole content; use it for context, font loaders; colours and theme values may change or animate, so use compositionLocalOf (CL).
- **Applier.kt (androidx-main @296313a4)** — AndroidX (android.googlesource.com) · `impl`
  https://android.googlesource.com/platform/frameworks/support/+/296313a488a01c84ddcb0801d4efee640a14070c/compose/runtime/runtime/src/commonMain/kotlin/androidx/compose/runtime/Applier.kt
  - vi: KDoc insertTopDown/insertBottomUp với ví dụ cây R, B, A, C và số thông báo; down/up, remove, move, clear, apply, onBeginChanges/onEndChanges (B6).
  - en: The insertTopDown/insertBottomUp KDoc with the R, B, A, C tree example and notification counts; down/up, remove, move, clear, apply, onBeginChanges/onEndChanges (B6).
- **Composables.kt (androidx-main @296313a4)** — AndroidX (android.googlesource.com) · `impl`
  https://android.googlesource.com/platform/frameworks/support/+/296313a488a01c84ddcb0801d4efee640a14070c/compose/runtime/runtime/src/commonMain/kotlin/androidx/compose/runtime/Composables.kt
  - vi: ComposeNode/ReusableComposeNode: startNode, createNode khi đang chèn hoặc useNode, Updater, endNode; factory không bảo đảm được gọi tại chỗ (B6).
  - en: ComposeNode/ReusableComposeNode: startNode, createNode while inserting or useNode, Updater, endNode; the factory is not guaranteed to be called in place (B6).
- **UiApplier.android.kt (androidx-main @296313a4)** — AndroidX (android.googlesource.com) · `android-impl`
  https://android.googlesource.com/platform/frameworks/support/+/296313a488a01c84ddcb0801d4efee640a14070c/compose/ui/ui/src/androidMain/kotlin/androidx/compose/ui/node/UiApplier.android.kt
  - vi: Applier cho LayoutNode: insertTopDown bị bỏ qua, chèn trong insertBottomUp; onEndChanges gọi owner.onEndApplyChanges (B6).
  - en: The Applier for LayoutNode: insertTopDown is ignored, inserts happen in insertBottomUp; onEndChanges calls owner.onEndApplyChanges (B6).
- **Layout.kt và BasicText.kt (androidx-main @296313a4)** — AndroidX (android.googlesource.com) · `impl`
  https://android.googlesource.com/platform/frameworks/support/+/296313a488a01c84ddcb0801d4efee640a14070c/compose/ui/ui/src/commonMain/kotlin/androidx/compose/ui/layout/Layout.kt
  - vi: Layout() phát node bằng ReusableComposeNode; BasicText với chuỗi đơn giản gọi Layout với modifier TextStringSimpleElement (B6).
  - en: Layout() emits its node with ReusableComposeNode; BasicText with a simple string calls Layout with a TextStringSimpleElement modifier (B6).
- **Boolean.or (Kotlin standard library)** — JetBrains (kotlinlang.org) · `stable`
  https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-boolean/or.html
  - vi: Hàm or của Boolean không short-circuit: cả hai vế đều được tính, khác toán tử || (B2).
  - en: Boolean.or does not short-circuit: both sides are evaluated, unlike the || operator (B2).
- **androidx.compose.runtime (package summary)** — Android Developers · `stable`
  https://developer.android.com/reference/kotlin/androidx/compose/runtime/package-summary.html
  - vi: Danh mục API của runtime, gồm CompositionLocal (B0).
  - en: The runtime API index, including CompositionLocal (B0).
- **Snapshot** — Android Developers · `stable`
  https://developer.android.com/reference/kotlin/androidx/compose/runtime/snapshots/Snapshot
  - vi: Cách ly, apply nguyên tử, xung đột, read/write observer (B4, B10).
  - en: Isolation, atomic apply, conflicts, read/write observers (B4, B10).
- **Applier** — Android Developers · `stable`
  https://developer.android.com/reference/kotlin/androidx/compose/runtime/Applier
  - vi: Applier<N> generic, các thao tác cây, onBeginChanges/onEndChanges (B6).
  - en: Generic Applier<N>, tree operations, onBeginChanges/onEndChanges (B6).
- **ComposeView** — Android Developers · `android-impl`
  https://developer.android.com/reference/kotlin/androidx/compose/ui/platform/ComposeView
  - vi: Thời điểm composition ban đầu: gắn window hoặc createComposition(); measure đầu (B1).
  - en: When the initial composition happens: attach or createComposition(); first measure (B1).
- **MonotonicFrameClock** — Android Developers · `stable`
  https://developer.android.com/reference/kotlin/androidx/compose/runtime/MonotonicFrameClock
  - vi: withFrameNanos, thời điểm frame tăng nghiêm ngặt (B5, cầu nối X3).
  - en: withFrameNanos, strictly increasing frame times (B5, bridge X3).
- **Recomposer** — Android Developers · `stable`
  https://developer.android.com/reference/kotlin/androidx/compose/runtime/Recomposer
  - vi: Bộ lập lịch recomposition; runRecomposeAndApplyChanges là suspend; pause/resume frame clock (B5).
  - en: The recomposition scheduler; runRecomposeAndApplyChanges is suspend; pause/resume of the frame clock (B5).
- **Lifecycle of composables** — Android Developers · `stable`
  https://developer.android.com/develop/ui/compose/lifecycle
  - vi: Identity theo call site, danh sách có/không key, điều kiện skip, kiểu stable (B3, B8).
  - en: Identity by call site, lists with/without keys, skip conditions, stable types (B3, B8).
- **Thinking in Compose** — Android Developers · `stable`
  https://developer.android.com/develop/ui/compose/mental-model
  - vi: Recomposition skip tối đa, lạc quan, có thể bị hủy; composable không side effect (B8).
  - en: Recomposition skips as much as possible, is optimistic and can be cancelled; side-effect-free composables (B8).
- **Jetpack Compose phases** — Android Developers · `stable`
  https://developer.android.com/develop/ui/compose/phases
  - vi: Ba phase, đọc state theo phase, vòng lặp phase (B7, cầu nối X1).
  - en: The three phases, state reads per phase, phase loops (B7, bridge X1).
- **Stability in Compose** — Android Developers · `stable`
  https://developer.android.com/develop/ui/compose/performance/stability
  - vi: Stable/unstable, so sánh tham số, cảnh báo về chú thích (B8).
  - en: Stable/unstable, parameter comparison, cautions about annotations (B8).
- **Strong skipping mode** — Android Developers · `version`
  https://developer.android.com/develop/ui/compose/performance/stability/strongskipping
  - vi: Bật mặc định từ Kotlin 2.0.20; unstable so bằng ===; memoize lambda (B8, B10).
  - en: On by default since Kotlin 2.0.20; unstable compared with ===; lambda memoization (B8, B10).
- **Semantics in Compose** — Android Developers · `stable`
  https://developer.android.com/develop/ui/compose/accessibility/semantics
  - vi: Semantics tree song song; merged và unmerged; ai dùng cây nào (B9).
  - en: The parallel semantics tree; merged and unmerged; who uses which tree (B9).
- **Custom layouts** — Android Developers · `stable`
  https://developer.android.com/develop/ui/compose/layouts/custom
  - vi: Ba bước của mỗi node (đo con, quyết kích thước, đặt con); không cho đo nhiều lượt; Modifier.layout (firstBaselineToTop); Layout (MyBasicColumn); place và placeRelative theo hướng bố cục (LO).
  - en: Each node’s three steps (measure children, decide size, place children); no multi-pass measurement; Modifier.layout (firstBaselineToTop); Layout (MyBasicColumn); place vs placeRelative and layout direction (LO).
- **Compose layout basics** — Android Developers · `stable`
  https://developer.android.com/develop/ui/compose/layouts/basics
  - vi: Cây UI được layout trong một lượt; cha đo trước con nhưng có kích thước và được đặt sau con; ví dụ SearchResult; lồng sâu không tốn thêm; BoxWithConstraints (LO).
  - en: The UI tree is laid out in a single pass; parents measure before their children but are sized and placed after them; the SearchResult example; deep nesting costs nothing extra; BoxWithConstraints (LO).
- **Intrinsic measurements in Compose layouts** — Android Developers · `stable`
  https://developer.android.com/develop/ui/compose/layouts/intrinsic-measurements
  - vi: Đo hai lần ném exception lúc chạy; intrinsic hỏi con trước khi đo, không đo hai lần; ví dụ TwoTexts với IntrinsicSize.Min; override intrinsic trong MeasurePolicy phải khớp measure (LO).
  - en: Measuring twice throws a runtime exception; intrinsics query children before measuring and do not measure twice; the TwoTexts example with IntrinsicSize.Min; intrinsic overrides in MeasurePolicy must match measure (LO).
- **Constraints and modifier order** — Android Developers · `stable`
  https://developer.android.com/develop/ui/compose/layouts/constraints-modifiers
  - vi: Loại constraints (bounded, unbounded, exact, kết hợp); size và requiredSize; ví dụ fillMaxSize().size(50.dp) (LO, MD).
  - en: Kinds of constraints (bounded, unbounded, exact, combined); size vs requiredSize; the fillMaxSize().size(50.dp) example (LO, MD).
- **MeasurePolicy.kt và Measurable.kt (androidx-main @296313a4)** — AndroidX (android.googlesource.com) · `impl`
  https://android.googlesource.com/platform/frameworks/support/+/296313a488a01c84ddcb0801d4efee640a14070c/compose/ui/ui/src/commonMain/kotlin/androidx/compose/ui/layout/MeasurePolicy.kt
  - vi: KDoc: không có thương lượng kích thước giữa cha và con; con chọn kích thước ngoài constraints thì bị ép và căn giữa; định nghĩa bốn hàm intrinsic và cài đặt mặc định dựa trên measure; Measurable chỉ được đo một lần trong một lượt layout (LO).
  - en: KDoc: no measurement negotiation between parent and child; a child sized outside its constraints is coerced and centred; the four intrinsic functions and their default implementation via measure; a Measurable can only be measured once per layout pass (LO).
- **LayoutNodeLayoutDelegate.kt và MeasurePassDelegate.kt (androidx-main @296313a4)** — AndroidX (android.googlesource.com) · `impl`
  https://android.googlesource.com/platform/frameworks/support/+/296313a488a01c84ddcb0801d4efee640a14070c/compose/ui/ui/src/commonMain/kotlin/androidx/compose/ui/node/LayoutNodeLayoutDelegate.kt
  - vi: MeasuredTwiceErrorMessage và kiểm tra trackMeasurementByParent: đo cùng một Measurable lần hai trong cùng lượt ném IllegalStateException; chỉ được đo trong khối measure hoặc layout của cha (LO).
  - en: MeasuredTwiceErrorMessage and the trackMeasurementByParent check: measuring the same Measurable twice in one pass throws IllegalStateException; measuring is only allowed in the parent’s measure or layout block (LO).
- **SubcomposeLayout.kt (androidx-main @296313a4)** — AndroidX (android.googlesource.com) · `impl`
  https://android.googlesource.com/platform/frameworks/support/+/296313a488a01c84ddcb0801d4efee640a14070c/compose/ui/ui/src/commonMain/kotlin/androidx/compose/ui/layout/SubcomposeLayout.kt
  - vi: KDoc: compose nội dung trong lúc đo; ba trường hợp dùng (biết constraints khi compose như BoxWithConstraints, dùng kích thước con này khi compose con kia, compose lười theo kích thước); subcompose(slotId, content) (LO, LZ).
  - en: KDoc: composing content during measurement; three use cases (constraints during composition as in BoxWithConstraints, one child’s size while composing another, lazy composition by available size); subcompose(slotId, content) (LO, LZ).
- **Constraints.kt (androidx-main @296313a4)** — AndroidX (android.googlesource.com) · `impl`
  https://android.googlesource.com/platform/frameworks/support/+/296313a488a01c84ddcb0801d4efee640a14070c/compose/ui/ui-unit/src/commonMain/kotlin/androidx/compose/ui/unit/Constraints.kt
  - vi: Bốn giá trị minWidth, maxWidth, minHeight, maxHeight; Constraints.Infinity = Int.MAX_VALUE; hasBoundedWidth/Height; fixed, fixedWidth, fixedHeight (LO).
  - en: The four values minWidth, maxWidth, minHeight, maxHeight; Constraints.Infinity = Int.MAX_VALUE; hasBoundedWidth/Height; fixed, fixedWidth, fixedHeight (LO).
- **Compose modifiers** — Android Developers · `stable`
  https://developer.android.com/develop/ui/compose/modifiers
  - vi: Modifier dùng để làm gì; thứ tự quan trọng (clickable trước/sau padding; không có margin); size, requiredSize, offset, matchParentSize, weight và scope an toàn; chuỗi là danh sách Modifier.Element có thứ tự, bất biến; trích và dùng lại modifier, then (MD).
  - en: What modifiers are for; order matters (clickable before/after padding; no margin modifier); size, requiredSize, offset, matchParentSize, weight and scope safety; a chain is an ordered, immutable list of Modifier.Elements; extracting and reusing modifiers, then (MD).
- **Create custom modifiers** — Android Developers · `stable`
  https://developer.android.com/develop/ui/compose/custom-modifiers
  - vi: Ba cách tạo modifier (nối modifier có sẵn, factory @Composable, Modifier.Node); caveat của factory @Composable; ModifierNodeElement create/update/equals; ví dụ circle; các loại node; shouldAutoInvalidate; coroutineScope; currentValueOf; delegate; composed {} không còn được khuyên dùng (MD).
  - en: Three ways to make a modifier (chaining existing ones, a @Composable factory, Modifier.Node); caveats of @Composable factories; ModifierNodeElement create/update/equals; the circle example; node kinds; shouldAutoInvalidate; coroutineScope; currentValueOf; delegate; composed {} no longer recommended (MD).
- **Migrate from Modifier.composed to Modifier.Node** — Android Developers · `stable`
  https://developer.android.com/develop/ui/compose/custom-modifiers-node
  - vi: Vấn đề của Modifier.composed (state trong composition, không skip được, lambda so theo tham chiếu); Modifier.Node sống lâu, tạo một lần cho mỗi element trên LayoutNode; các bước chuyển đổi (MD).
  - en: Problems with Modifier.composed (state in composition, not skippable, lambdas compared by reference); Modifier.Node is long-lived, created once per element on a LayoutNode; migration steps (MD).
- **Modifier.kt (androidx-main @296313a4)** — AndroidX (android.googlesource.com) · `impl`
  https://android.googlesource.com/platform/frameworks/support/+/296313a488a01c84ddcb0801d4efee640a14070c/compose/ui/ui/src/commonMain/kotlin/androidx/compose/ui/Modifier.kt
  - vi: Modifier là tập Element có thứ tự, bất biến; then trả về CombinedModifier(outer, inner), hoặc chính nó nếu other là Modifier rỗng; foldIn/foldOut; quy ước tham số modifier (MD).
  - en: A Modifier is an ordered, immutable collection of Elements; then returns CombinedModifier(outer, inner), or itself when other is the empty Modifier; foldIn/foldOut; the modifier parameter convention (MD).
- **NodeChain.kt (androidx-main @296313a4)** — AndroidX (android.googlesource.com) · `impl`
  https://android.googlesource.com/platform/frameworks/support/+/296313a488a01c84ddcb0801d4efee640a14070c/compose/ui/ui/src/commonMain/kotlin/androidx/compose/ui/node/NodeChain.kt
  - vi: updateFrom: cùng độ dài thì so tuyến tính từng vị trí; actionForModifiers: equals → dùng lại, cùng lớp → update, khác → diff cấu trúc (MyersDiff) với insert/remove/same; node bị bỏ chạy detach, node mới chạy attach (MD).
  - en: updateFrom: equal lengths get a linear position-by-position comparison; actionForModifiers: equals → reuse, same class → update, otherwise → structural diff (MyersDiff) with insert/remove/same; removed nodes run detach, new nodes run attach (MD).
- **ModifierNodeElement.kt và Background.kt (androidx-main @296313a4)** — AndroidX (android.googlesource.com) · `impl`
  https://android.googlesource.com/platform/frameworks/support/+/296313a488a01c84ddcb0801d4efee640a14070c/compose/ui/ui/src/commonMain/kotlin/androidx/compose/ui/node/ModifierNodeElement.kt
  - vi: ModifierNodeElement nhẹ, chỉ giữ dữ liệu để tạo và cập nhật node; create, update, equals và hashCode bắt buộc; BackgroundElement so color, brush, alpha, shape (MD).
  - en: A ModifierNodeElement is lightweight and only holds the data to create and update its node; create, update, and required equals and hashCode; BackgroundElement compares color, brush, alpha and shape (MD).
- **Lists and grids** — Android Developers · `stable`
  https://developer.android.com/develop/ui/compose/lists
  - vi: Column compose mọi mục, lazy chỉ compose mục trong viewport; DSL item/items/itemsIndexed/stickyHeader; contentPadding, spacedBy; key giữ state khi mục đổi vị trí, kiểu key phải lưu được trong Bundle; contentType; derivedStateOf với firstVisibleItemIndex; animateItem cần key; mẹo: tránh mục 0 px, tránh lồng cuộn cùng chiều, không gộp nhiều phần tử vào một item, đo ở release (LZ).
  - en: Column composes every item, lazy composes only items in the viewport; the item/items/itemsIndexed/stickyHeader DSL; contentPadding, spacedBy; keys keep state when items move, key types must be Bundle-saveable; contentType; derivedStateOf with firstVisibleItemIndex; animateItem needs keys; tips: avoid 0-px items, avoid same-direction nested scrolling, do not group several elements in one item, measure in release (LZ).
- **LazyLayout.kt (androidx-main @296313a4)** — AndroidX (android.googlesource.com) · `impl`
  https://android.googlesource.com/platform/frameworks/support/+/296313a488a01c84ddcb0801d4efee640a14070c/compose/foundation/foundation/src/commonMain/kotlin/androidx/compose/foundation/lazy/layout/LazyLayout.kt
  - vi: LazyLayout chỉ compose và đặt mục đang cần; compose trong bước đo là tín hiệu "đang cần"; dựng trên SubcomposeLayout với LazyLayoutItemReusePolicy: giữ tối đa 7 slot mỗi contentType (5 + 2 như RecyclerView), chỉ dùng lại khi contentType bằng nhau (LZ).
  - en: LazyLayout only composes and lays out currently needed items; composing during measurement signals "needed"; built on SubcomposeLayout with LazyLayoutItemReusePolicy: keeps up to 7 slots per contentType (5 + 2 like RecyclerView), reusing only when contentTypes are equal (LZ).
- **LazyLayoutItemContentFactory.kt và LazySaveableStateHolder.kt (androidx-main @296313a4)** — AndroidX (android.googlesource.com) · `impl`
  https://android.googlesource.com/platform/frameworks/support/+/296313a488a01c84ddcb0801d4efee640a14070c/compose/foundation/foundation/src/commonMain/kotlin/androidx/compose/foundation/lazy/layout/LazyLayoutItemContentFactory.kt
  - vi: Cache lambda nội dung theo key để skip được cả mục; ánh xạ key ↔ index; bọc mỗi mục trong SaveableStateProvider theo key; khi lưu chỉ lưu mục đang hiện để tránh TransactionTooLargeException (LZ).
  - en: Caches content lambdas by key so a whole item can be skipped; maps keys ↔ indices; wraps each item in a SaveableStateProvider by key; on save, only visible items are saved to avoid TransactionTooLargeException (LZ).
- **CheckScrollableContainerConstraints.kt (androidx-main @296313a4)** — AndroidX (android.googlesource.com) · `impl`
  https://android.googlesource.com/platform/frameworks/support/+/296313a488a01c84ddcb0801d4efee640a14070c/compose/foundation/foundation/src/commonMain/kotlin/androidx/compose/foundation/CheckScrollableContainerConstraints.kt
  - vi: Thứ cuộn dọc bị đo với chiều cao tối đa vô hạn thì ném IllegalStateException ("Vertically scrollable component was measured with an infinity maximum height constraints…") (LZ).
  - en: A vertically scrollable component measured with an infinite maximum height throws IllegalStateException ("Vertically scrollable component was measured with an infinity maximum height constraints…") (LZ).
- **Diagnose stability issues** — Android Developers · `stable`
  https://developer.android.com/develop/ui/compose/performance/stability/diagnose
  - vi: Layout Inspector đếm recompose/skip nhưng đừng chỉ dựa vào nó; bật compiler report bằng composeCompiler { reportsDestination, metricsDestination }; ba file classes.txt, composables.txt, composables.csv; ví dụ dòng report; lớp unstable dưới strong skipping chưa chắc là vấn đề (B8).
  - en: The Layout Inspector counts recompositions/skips but do not rely on it alone; enable compiler reports with composeCompiler { reportsDestination, metricsDestination }; the classes.txt, composables.txt and composables.csv files; example report lines; under strong skipping an unstable class is not necessarily a problem (B8).
- **Fix stability issues** — Android Developers · `stable`
  https://developer.android.com/develop/ui/compose/performance/stability/fix
  - vi: Thứ tự sửa: strong skipping, giữ tham chiếu, lớp bất biến, collection bất biến (và cái giá equals từng phần tử), @Stable/@Immutable cho lớp nhỏ equals rẻ, file cấu hình stability (từ Compose Compiler 1.5.5), nhiều module; không phải composable nào cũng nên skip được (B8).
  - en: The order of fixes: strong skipping, stable references, immutable classes, immutable collections (and the cost of element-by-element equals), @Stable/@Immutable for small classes with cheap equals, the stability configuration file (since Compose Compiler 1.5.5), multiple modules; not every composable should be skippable (B8).
- **Annotation của compose/runtime (androidx-main @296313a4)** — AndroidX (android.googlesource.com) · `impl`
  https://android.googlesource.com/platform/frameworks/support/+/296313a488a01c84ddcb0801d4efee640a14070c/compose/runtime/runtime/src/commonMain/kotlin/androidx/compose/runtime/
  - vi: Thư mục runtime ở commit ghim: Composable.kt, NonRestartableComposable.kt, NonSkippableComposable.kt, ReadOnlyComposable.kt, DontMemoize.kt, ExplicitGroupsComposable.kt, DisallowComposableCalls.kt, ComposableTarget.kt, ComposableOpenTarget.kt, ComposableTargetMarker.kt, ComposableInferredTarget.kt, ComposeCompilerApi.kt, NoLiveLiterals.kt và KDoc của từng cái (B8).
  - en: The runtime directory at the pinned commit: Composable.kt, NonRestartableComposable.kt, NonSkippableComposable.kt, ReadOnlyComposable.kt, DontMemoize.kt, ExplicitGroupsComposable.kt, DisallowComposableCalls.kt, ComposableTarget.kt, ComposableOpenTarget.kt, ComposableTargetMarker.kt, ComposableInferredTarget.kt, ComposeCompilerApi.kt, NoLiveLiterals.kt and each one’s KDoc (B8).
- **compose/runtime/runtime-annotation (androidx-main @296313a4)** — AndroidX (android.googlesource.com) · `impl`
  https://android.googlesource.com/platform/frameworks/support/+/296313a488a01c84ddcb0801d4efee640a14070c/compose/runtime/runtime-annotation/src/commonMain/kotlin/androidx/compose/runtime/
  - vi: Stable.kt, Immutable.kt, StableMarker.kt (ba điều kiện của kiểu stable, lời hứa không được kiểm chứng, hành vi không xác định nếu vi phạm) và annotation/FrequentlyChangingValue.kt, RememberInComposition.kt, DoNotRetain.kt cho lint (B8).
  - en: Stable.kt, Immutable.kt, StableMarker.kt (the three conditions of a stable type, an unverified promise, undefined behaviour if violated) and annotation/FrequentlyChangingValue.kt, RememberInComposition.kt, DoNotRetain.kt for lint (B8).
- **ComposableFunctionBodyTransformer.kt (Kotlin v2.4.21)** — JetBrains/kotlin (GitHub) · `impl`
  https://github.com/JetBrains/kotlin/blob/v2.4.21/plugins/compose/compiler-hosted/src/main/java/androidx/compose/compiler/plugins/kotlin/lower/ComposableFunctionBodyTransformer.kt
  - vi: Compose compiler đã chuyển vào repo Kotlin. Hàm non-restartable không gọi changed() cho tham số; group bao thân bị bỏ với ReadOnly/ExplicitGroups hoặc khi OptimizeNonSkippingGroups bật; canSkip bắt đầu bằng !hasNonSkippableAnnotation; nơi gọi hàm ReadOnly không có group; strong skipping so tham số unstable bằng instance (B8).
  - en: The Compose compiler moved into the Kotlin repository. Non-restartable functions never call changed() on parameters; the body group is dropped for ReadOnly/ExplicitGroups or when OptimizeNonSkippingGroups is on; canSkip starts as !hasNonSkippableAnnotation; calls to ReadOnly functions get no group; strong skipping compares unstable parameters by instance (B8).
- **AbstractComposeLowering.kt (Kotlin v2.4.21)** — JetBrains/kotlin (GitHub) · `impl`
  https://github.com/JetBrains/kotlin/blob/v2.4.21/plugins/compose/compiler-hosted/src/main/java/androidx/compose/compiler/plugins/kotlin/lower/AbstractComposeLowering.kt
  - vi: shouldBeRestartable(): không restartable nếu không có thân, local, inline, @NonRestartableComposable, @ExplicitGroupsComposable, trả về khác Unit, accessor delegate, hàm ảo có tham số mặc định, hàm open trong lớp không final (B8).
  - en: shouldBeRestartable(): not restartable if it has no body, is local, inline, @NonRestartableComposable, @ExplicitGroupsComposable, returns non-Unit, is a delegated accessor, a virtual function with default parameters, or open in a non-final class (B8).
- **ComposerLambdaMemoization.kt (Kotlin v2.4.21)** — JetBrains/kotlin (GitHub) · `impl`
  https://github.com/JetBrains/kotlin/blob/v2.4.21/plugins/compose/compiler-hosted/src/main/java/androidx/compose/compiler/plugins/kotlin/lower/ComposerLambdaMemoization.kt
  - vi: Lambda không được memoize nếu có @DontMemoize (trên lambda hoặc hàm chứa), capture var, property delegate, lambda inline, hoặc giá trị unstable khi strong skipping tắt (B8).
  - en: A lambda is not memoized if it has @DontMemoize (on the lambda or the enclosing function), or captures a var, a property delegate, an inline lambda, or an unstable value when strong skipping is off (B8).
- **ComposePlugin.kt (Kotlin v2.4.21)** — JetBrains/kotlin (GitHub) · `impl`
  https://github.com/JetBrains/kotlin/blob/v2.4.21/plugins/compose/compiler-hosted/src/main/java/androidx/compose/compiler/plugins/kotlin/ComposePlugin.kt
  - vi: enum FeatureFlag: StrongSkipping, IntrinsicRemember, OptimizeNonSkippingGroups, PausableComposition đều mặc định true ở Kotlin 2.4.21 (B8).
  - en: enum FeatureFlag: StrongSkipping, IntrinsicRemember, OptimizeNonSkippingGroups, PausableComposition all default to true in Kotlin 2.4.21 (B8).
- **Merging and clearing** — Android Developers · `stable`
  https://developer.android.com/develop/ui/compose/accessibility/merging-clearing
  - vi: Luật gộp theo từng thuộc tính; cha không gộp được con đang tự gộp (nút, clickable); clearAndSetSemantics (rỗng hoặc có nội dung, ảnh hưởng mọi bên dùng, thứ tự modifier); hideFromAccessibility; custom actions (B9).
  - en: Per-property merge policies; a parent cannot merge children that merge themselves (buttons, clickables); clearAndSetSemantics (empty or with content, affects every consumer, modifier order); hideFromAccessibility; custom actions (B9).
- **Test your Compose layout** — Android Developers · `stable`
  https://developer.android.com/develop/ui/compose/testing
  - vi: Phụ thuộc ui-test-junit4 và ui-test-manifest; createComposeRule và createAndroidComposeRule; ví dụ test cơ bản (B9).
  - en: The ui-test-junit4 and ui-test-manifest dependencies; createComposeRule and createAndroidComposeRule; a basic test example (B9).
- **Testing APIs** — Android Developers · `stable`
  https://developer.android.com/develop/ui/compose/testing/apis
  - vi: Finder, assertion, action, matcher phân cấp; useUnmergedTree; printToLog cho cây merged và unmerged (B9).
  - en: Finders, assertions, actions, hierarchical matchers; useUnmergedTree; printToLog for the merged and unmerged trees (B9).
- **Synchronize your tests** — Android Developers · `stable`
  https://developer.android.com/develop/ui/compose/testing/synchronization
  - vi: Đồng bộ trước mỗi action/assertion; đồng hồ ảo; MainTestClock, autoAdvance, advanceTimeBy, advanceTimeByFrame, waitForIdle, waitUntil; idling resource; cảnh báo CountDownLatch (B9).
  - en: Synchronisation before every action/assertion; the virtual clock; MainTestClock, autoAdvance, advanceTimeBy, advanceTimeByFrame, waitForIdle, waitUntil; idling resources; the CountDownLatch warning (B9).
- **Compose performance** — Android Developers · `stable`
  https://developer.android.com/develop/ui/compose/performance
  - vi: Chế độ debug có chi phí hiệu năng; chạy release với R8; Baseline Profile (Compose có sẵn một profile, app nên có riêng); bảng jank: từ Compose 1.9.0 bằng View; danh sách thực hành (PF).
  - en: Debug mode has a performance cost; run release with R8; Baseline Profiles (Compose ships one, apps should add their own); the jank table: Compose matches Views since 1.9.0; the list of practices (PF).
- **Follow best practices** — Android Developers · `stable`
  https://developer.android.com/develop/ui/compose/performance/bestpractices
  - vi: remember phép tính đắt (và phản ví dụ); key và contentType (Bundle, không dùng chỉ số/hashCode, itemsIndexed, cacheWindow); derivedStateOf và computedStateOf (Compose 1.13); hoãn lần đọc (Jetsnack, offset lambda, drawBehind); không ghi ngược (BadComposable) (PF).
  - en: remember expensive work (and the counter-example); keys and contentType (Bundle, no indices/hashCode, itemsIndexed, cacheWindow); derivedStateOf and computedStateOf (Compose 1.13); deferring reads (Jetsnack, offset lambda, drawBehind); no backwards writes (BadComposable) (PF).
- **Composition tracing** — Android Developers · `stable`
  https://developer.android.com/develop/ui/compose/tooling/tracing
  - vi: Tên composable trong system trace; runtime-tracing; phiên bản tối thiểu; Profiler và Perfetto; profileable, không debuggable; recomposition tracing (1.13.0+, tốn hơn, để debug) (PF).
  - en: Composable names in system traces; runtime-tracing; minimum versions; Profiler and Perfetto; profileable, not debuggable; recomposition tracing (1.13.0+, more overhead, for debugging) (PF).
- **Baseline Profiles (Compose)** — Android Developers · `stable`
  https://developer.android.com/develop/ui/compose/performance/baseline-profiles
  - vi: Khoảng 30% nhanh hơn từ lần mở đầu cho đường đi có trong profile; ART biên dịch AOT khi cài; profile của Compose chỉ cho mã thư viện; tạo bằng Macrobenchmark (PF).
  - en: About 30% faster from the first launch for included paths; ART compiles AOT at install; Compose’s profile only covers library code; create one with Macrobenchmark (PF).
- **Debug your Compose UI** — Android Developers · `stable`
  https://developer.android.com/develop/ui/compose/tooling/debug
  - vi: Layout Inspector: cột composition và skip, Show Recomposition Counts, API 29+, Compose 1.2.0+, Reset, gradient; giữ file META-INF version; số đếm không thay được benchmark (trang Tools) (PF).
  - en: Layout Inspector: composition and skip columns, Show Recomposition Counts, API 29+, Compose 1.2.0+, Reset, gradient; keep the META-INF version files; counts are no substitute for benchmarks (Tools page) (PF).
- **Android UI Development with Jetpack Compose (Thomas Kunneth, Packt), mã mẫu** — Packt (sách) · `guideline`
  https://github.com/PacktPublishing/Android-UI-Development-with-Jetpack-Compose
  - vi: Sách giảng chính của Runtime v2: tư duy khai báo, composable, recomposition (DC);, 7, 9, 10 cho các chương sau. Viết theo phiên bản Compose cũ hơn: chi tiết nội bộ được đối chiếu lại với tài liệu hiện tại.
  - en: Main teaching book for Runtime v2: declarative thinking, composables, recomposition (DC);, 7, 9, 10 for later chapters. Written against an older Compose version: internals are re-checked against current docs.
- **Jetpack Compose by Tutorials, 2nd edition (Kodeco)** — Kodeco (sách) · `guideline`
  https://www.kodeco.com/books/jetpack-compose-by-tutorials
  - vi: Lists, modifiers, state, lifecycle/effects, interop, UI test, accessibility.
  - en: Lists, modifiers, state, lifecycle/effects, interop, UI tests, accessibility.
- **Jetpack Compose 1.3 Essentials (Neil Smyth, Payload Media)** — Payload Media (sách) · `guideline`
  https://www.ebookfrenzy.com/
  - vi: Theo Compose 1.3 (lịch sử): CompositionLocal, slot API, custom layout, IntrinsicSize, lazy list. Không bê hành vi phiên bản cũ sang hiện tại.
  - en: Targets Compose 1.3 (historical): CompositionLocal, slot APIs, custom layouts, IntrinsicSize, lazy lists. Old-version behaviour is not carried over to today.
- **Compose Runtime releases** — Android Developers · `version`
  https://developer.android.com/jetpack/androidx/releases/compose-runtime
  - vi: Chỉ dùng để xác định phiên bản (1.13.0 trong BOM 2026.11.01).
  - en: Used only to pin the version (1.13.0 in BOM 2026.11.01).

### Track C

- **AnimatedVisibility.kt (androidx-main @296313a4)** — AndroidX (android.googlesource.com) · `impl`
  https://android.googlesource.com/platform/frameworks/support/+/296313a488a01c84ddcb0801d4efee640a14070c/compose/animation/animation/src/commonMain/kotlin/androidx/compose/animation/AnimatedVisibility.kt
  - vi: KDoc: mặc định fadeIn + expandIn, fadeOut + shrinkOut; enter/exit kết hợp bằng +, chạy cùng lúc; chờ MỌI animation enter/exit (kể cả tùy biến trên transition của scope) rồi mới gỡ content; content bị gỡ và dispose sau exit; Layout riêng lấy kích thước lớn nhất của con; Row/Column có mặc định riêng (C4).
  - en: KDoc: defaults fadeIn + expandIn, fadeOut + shrinkOut; enter/exit combine with +, starting together; waits for ALL enter/exit animations (including custom ones on the scope’s transition) before removing content; content is removed and disposed after exit; its own Layout takes the children’s largest size; Row/Column have their own defaults (C4).
- **Transition.kt (androidx-main @296313a4)** — AndroidX (android.googlesource.com) · `impl`
  https://android.googlesource.com/platform/frameworks/support/+/296313a488a01c84ddcb0801d4efee640a14070c/compose/animation/animation-core/src/commonMain/kotlin/androidx/compose/animation/core/Transition.kt
  - vi: updateTransition: remember Transition, animateTo(targetState) mỗi lần chạy, DisposableEffect dọn dẹp; rememberTransition(MutableTransitionState) cho state đầu khác target; currentState là initialState tới khi xong; con mặc định spring, chỉ nhận FiniteAnimationSpec; isTransitioningTo (C3).
  - en: updateTransition: remember a Transition, animateTo(targetState) on every run, a DisposableEffect cleanup; rememberTransition(MutableTransitionState) for an initial state unlike the target; currentState is the initialState until done; children default to spring and only accept FiniteAnimationSpec; isTransitioningTo (C3).
- **AnimationSpec.kt (androidx-main @296313a4)** — AndroidX (android.googlesource.com) · `impl`
  https://android.googlesource.com/platform/frameworks/support/+/296313a488a01c84ddcb0801d4efee640a14070c/compose/animation/animation-core/src/commonMain/kotlin/androidx/compose/animation/core/AnimationSpec.kt
  - vi: AnimationSpec chỉ có vectorize(converter) → VectorizedAnimationSpec; FiniteAnimationSpec; tween mặc định 300 ms, delay 0, FastOutSlowInEasing; spring mặc định NoBouncy/StiffnessMedium; keyframes (LinearEasing mặc định, ArcMode); snap(delay) (C2).
  - en: AnimationSpec only has vectorize(converter) → VectorizedAnimationSpec; FiniteAnimationSpec; tween defaults 300 ms, delay 0, FastOutSlowInEasing; spring defaults NoBouncy/StiffnessMedium; keyframes (LinearEasing by default, ArcMode); snap(delay) (C2).
- **VectorConverters.kt (androidx-main @296313a4)** — AndroidX (android.googlesource.com) · `impl`
  https://android.googlesource.com/platform/frameworks/support/+/296313a488a01c84ddcb0801d4efee640a14070c/compose/animation/animation-core/src/commonMain/kotlin/androidx/compose/animation/core/VectorConverters.kt
  - vi: TwoWayConverter; converter có sẵn: Float, Int, Dp (1D), DpOffset, Size, Offset (2D), Rect (4D)… (C2).
  - en: TwoWayConverter; built-in converters: Float, Int, Dp (1D), DpOffset, Size, Offset (2D), Rect (4D)… (C2).
- **ColorVectorConverter.kt (androidx-main @296313a4)** — AndroidX (android.googlesource.com) · `impl`
  https://android.googlesource.com/platform/frameworks/support/+/296313a488a01c84ddcb0801d4efee640a14070c/compose/animation/animation/src/commonMain/kotlin/androidx/compose/animation/ColorVectorConverter.kt
  - vi: Màu đổi sang Oklab và đóng gói AnimationVector4D(alpha, L, a, b); khi đổi ngược thì kẹp giá trị và chuyển về color space đích (C2).
  - en: Colours are converted to Oklab and packed as AnimationVector4D(alpha, L, a, b); converting back clamps values and returns to the target colour space (C2).
- **AnimateAsState.kt (androidx-main @296313a4)** — AndroidX (android.googlesource.com) · `impl`
  https://android.googlesource.com/platform/frameworks/support/+/296313a488a01c84ddcb0801d4efee640a14070c/compose/animation/animation-core/src/commonMain/kotlin/androidx/compose/animation/core/AnimateAsState.kt
  - vi: animateValueAsState: rememberCoroutineScope, remember AnimateAsState(Animatable), SideEffect gọi update() trừ lần đầu; update so target với animatable.targetValue; restartAnimation hủy job cũ và launch animateTo (UNDISPATCHED); KDoc: không hủy được nếu không gỡ khỏi cây, dùng Animatable (C1).
  - en: animateValueAsState: rememberCoroutineScope, a remembered AnimateAsState(Animatable), a SideEffect calling update() except the first time; update compares the target with animatable.targetValue; restartAnimation cancels the old job and launches animateTo (UNDISPATCHED); KDoc: cannot be cancelled without leaving the tree, use Animatable (C1).
- **Animations in Compose** — Android Developers · `stable`
  https://developer.android.com/develop/ui/compose/animation/introduction
  - vi: Tổng quan các nhóm API animation (C0).
  - en: Overview of the animation API groups (C0).
- **Choose an animation API** — Android Developers · `stable`
  https://developer.android.com/develop/ui/compose/animation/choose-api
  - vi: Cây quyết định chọn API (C0).
  - en: The decision tree for choosing an API (C0).
- **Value-based animations** — Android Developers · `stable`
  https://developer.android.com/develop/ui/compose/animation/value-based
  - vi: animate*AsState đổi target giữa chừng, Animatable, updateTransition, infinite transition (C1, C3, C6).
  - en: animate*AsState retargeting, Animatable, updateTransition, infinite transitions (C1, C3, C6).
- **Animation modifiers and composables** — Android Developers · `stable`
  https://developer.android.com/develop/ui/compose/animation/composables-modifiers
  - vi: AnimatedVisibility, AnimatedContent, Crossfade, animateContentSize (C4, C5).
  - en: AnimatedVisibility, AnimatedContent, Crossfade, animateContentSize (C4, C5).
- **Customize animations** — Android Developers · `stable`
  https://developer.android.com/develop/ui/compose/animation/customize
  - vi: spring, tween, keyframes, keyframesWithSpline, repeatable, snap, easing, AnimationVector (C2).
  - en: spring, tween, keyframes, keyframesWithSpline, repeatable, snap, easing, AnimationVector (C2).
- **Advanced animation example: Gestures** — Android Developers · `stable`
  https://developer.android.com/develop/ui/compose/animation/advanced
  - vi: Kéo, stop(), VelocityTracker, decay, animateTo với initialVelocity (C6).
  - en: Dragging, stop(), VelocityTracker, decay, animateTo with initialVelocity (C6).
- **Test animations** — Android Developers · `stable`
  https://developer.android.com/develop/ui/compose/animation/testing
  - vi: mainClock, autoAdvance, advanceTimeBy làm tròn lên theo frame (C8).
  - en: mainClock, autoAdvance, advanceTimeBy rounding up to frames (C8).
- **Quick guide to Animations in Compose** — Android Developers · `guideline`
  https://developer.android.com/develop/ui/compose/animation/quick-guide
  - vi: Tối ưu hiệu năng: dạng lambda của modifier, graphicsLayer, thứ tự animateContentSize (C5, C7).
  - en: Performance: lambda modifiers, graphicsLayer, animateContentSize order (C5, C7).
- **Animatable** — Android Developers · `stable`
  https://developer.android.com/reference/kotlin/androidx/compose/animation/core/Animatable
  - vi: Hủy animation đang chạy bằng CancellationException, stop(), initialVelocity mặc định = velocity (C6).
  - en: Cancelling a running animation with CancellationException, stop(), initialVelocity defaulting to velocity (C6).
- **Spring** — Android Developers · `stable`
  https://developer.android.com/reference/kotlin/androidx/compose/animation/core/Spring
  - vi: Hằng số damping ratio và stiffness (C2).
  - en: Damping ratio and stiffness constants (C2).
- **AnimationConstants** — Android Developers · `stable`
  https://developer.android.com/reference/kotlin/androidx/compose/animation/core/AnimationConstants
  - vi: DefaultDurationMillis = 300 (C2).
  - en: DefaultDurationMillis = 300 (C2).
- **FloatExponentialDecaySpec** — Android Developers · `stable`
  https://developer.android.com/reference/kotlin/androidx/compose/animation/core/FloatExponentialDecaySpec
  - vi: Tham số mặc định của exponential decay (C2, C6).
  - en: Default parameters of exponential decay (C2, C6).
- **androidx.compose.animation.core (package summary)** — Android Developers · `version`
  https://developer.android.com/reference/kotlin/androidx/compose/animation/core/package-summary
  - vi: Mặc định của spring() và tween(); keyframesWithSpline thêm ở 1.6.0 (C2).
  - en: Defaults of spring() and tween(); keyframesWithSpline added in 1.6.0 (C2).
- **Easing.kt (androidx-main @296313a4)** — AndroidX (android.googlesource.com) · `impl`
  https://android.googlesource.com/platform/frameworks/support/+/296313a488a01c84ddcb0801d4efee640a14070c/compose/animation/animation-core/src/commonMain/kotlin/androidx/compose/animation/core/Easing.kt
  - vi: Điểm điều khiển cubic-bezier của các easing chuẩn; ghim commit 296313a4, đọc lại 2026-11-23 (C2).
  - en: Cubic-bezier control points of the standard easings; pinned commit 296313a4, re-read 2026-11-23 (C2).
- **FloatDecayAnimationSpec.kt (androidx-main @296313a4)** — AndroidX (android.googlesource.com) · `impl`
  https://android.googlesource.com/platform/frameworks/support/+/296313a488a01c84ddcb0801d4efee640a14070c/compose/animation/animation-core/src/commonMain/kotlin/androidx/compose/animation/core/FloatDecayAnimationSpec.kt
  - vi: Công thức exponential decay, friction −4.2; ghim commit 296313a4, đọc lại 2026-11-23 (C2, C6).
  - en: The exponential decay formula, friction −4.2; pinned commit 296313a4, re-read 2026-11-23 (C2, C6).
- **InfiniteTransition.kt (androidx-main @296313a4)** — AndroidX (android.googlesource.com) · `impl`
  https://android.googlesource.com/platform/frameworks/support/+/296313a488a01c84ddcb0801d4efee640a14070c/compose/animation/animation-core/src/commonMain/kotlin/androidx/compose/animation/core/InfiniteTransition.kt
  - vi: rememberInfiniteTransition = remember + run(): LaunchedEffect lặp withInfiniteAnimationFrameNanos; play time chia durationScale; durationScale = 0 → skipToEnd và treo tới khi > 0; đổi tỉ lệ → chạy lại từ 0; con là TransitionAnimationState (mutableStateOf), DisposableEffect thêm/gỡ, SideEffect tạo lại khi initial/target đổi (không giữ liên tục) (IF).
  - en: rememberInfiniteTransition = remember + run(): a LaunchedEffect looping withInfiniteAnimationFrameNanos; play time divided by durationScale; durationScale = 0 → skipToEnd and suspend until > 0; scale change → restart from 0; children are TransitionAnimationStates (mutableStateOf), DisposableEffect adds/removes, SideEffect recreates when initial/target change (continuity not kept) (IF).
- **SuspendAnimation.kt (androidx-main @296313a4)** — AndroidX (android.googlesource.com) · `impl`
  https://android.googlesource.com/platform/frameworks/support/+/296313a488a01c84ddcb0801d4efee640a14070c/compose/animation/animation-core/src/commonMain/kotlin/androidx/compose/animation/core/SuspendAnimation.kt
  - vi: callWithFrameNanos: Animation.isInfinite → withInfiniteAnimationFrameNanos, ngược lại withFrameNanos (IF).
  - en: callWithFrameNanos: Animation.isInfinite → withInfiniteAnimationFrameNanos, otherwise withFrameNanos (IF).
- **InfiniteAnimationPolicy.kt (androidx-main @296313a4)** — AndroidX (android.googlesource.com) · `impl`
  https://android.googlesource.com/platform/frameworks/support/+/296313a488a01c84ddcb0801d4efee640a14070c/compose/ui/ui/src/commonMain/kotlin/androidx/compose/ui/platform/InfiniteAnimationPolicy.kt
  - vi: KDoc: chính sách áp cho animation lấy frame qua withInfiniteAnimationFrameNanos/Millis, có thể biến chúng thành hữu hạn; mặc định không cài, trừ test instrumented dùng ComposeTestRule (IF).
  - en: KDoc: the policy applies to animations taking frames through withInfiniteAnimationFrameNanos/Millis and can make them finite; none installed by default, except instrumented tests using ComposeTestRule (IF).
- **Animatable.kt (androidx-main @296313a4)** — AndroidX (android.googlesource.com) · `impl`
  https://android.googlesource.com/platform/frameworks/support/+/296313a488a01c84ddcb0801d4efee640a14070c/compose/animation/animation-core/src/commonMain/kotlin/androidx/compose/animation/core/Animatable.kt
  - vi: KDoc và mã: loại trừ nhau qua MutatorMutex, lời gọi mới hủy cũ bằng CancellationException; animateTo đi từ giá trị/vận tốc hiện tại; initialVelocity chỉ nên đặt sau fling; endAnimation đặt vận tốc 0; AnimationResult Finished/BoundReached; bounds theo từng chiều, snapTo kẹp; stop dừng tại chỗ; @RememberInComposition; InterruptionAwareAnimationSpec (C6).
  - en: KDoc and code: mutual exclusion via MutatorMutex, a new call cancels the old with CancellationException; animateTo starts from the current value/velocity; set initialVelocity only after a fling; endAnimation resets velocity to 0; AnimationResult Finished/BoundReached; per-dimension bounds, snapTo clamps; stop halts in place; @RememberInComposition; InterruptionAwareAnimationSpec (C6).
- **InternalMutatorMutex.kt (androidx-main @296313a4)** — AndroidX (android.googlesource.com) · `impl`
  https://android.googlesource.com/platform/frameworks/support/+/296313a488a01c84ddcb0801d4efee640a14070c/compose/animation/animation-core/src/commonMain/kotlin/androidx/compose/animation/core/InternalMutatorMutex.kt
  - vi: MutatorMutex nội bộ: mutate mới hủy job của mutator cũ bằng MutationInterruptedException (C6).
  - en: Internal MutatorMutex: a new mutate cancels the old mutator's job with MutationInterruptedException (C6).
- **Shared element transitions in Compose** — Android Developers · `stable`
  https://developer.android.com/develop/ui/compose/animation/shared-elements
  - vi: SharedTransitionLayout/SharedTransitionScope, sharedElement vs sharedBounds (hero vs container transform, Text), key data class, isMatchFound, thứ tự modifier, requiredSize, quản lý visibility thủ công, giới hạn (không interop View, không animate hình clip) (SE).
  - en: SharedTransitionLayout/SharedTransitionScope, sharedElement vs sharedBounds (hero vs container transform, Text), data class keys, isMatchFound, modifier order, requiredSize, manual visibility, limits (no View interop, no clip-shape animation) (SE).
- **Customize shared element transition** — Android Developers · `stable`
  https://developer.android.com/develop/ui/compose/animation/shared-elements/customize
  - vi: boundsTransform (keyframes, ArcMode), resizeMode scaleToBounds vs RemeasureToBounds, SharedContentConfig.isEnabled (SE).
  - en: boundsTransform (keyframes, ArcMode), resizeMode scaleToBounds vs RemeasureToBounds, SharedContentConfig.isEnabled (SE).
- **Shared elements with Navigation** — Android Developers · `version`
  https://developer.android.com/develop/ui/compose/animation/shared-elements/navigation
  - vi: Navigation 3: NavDisplay trong SharedTransitionLayout, LocalNavAnimatedContentScope; Navigation 2: NavHost, this@composable; predictive back theo phiên bản Android (SE).
  - en: Navigation 3: NavDisplay in SharedTransitionLayout, LocalNavAnimatedContentScope; Navigation 2: NavHost, this@composable; predictive back by Android version (SE).
- **SharedTransitionScope.kt (androidx-main @296313a4)** — AndroidX (android.googlesource.com) · `impl`
  https://android.googlesource.com/platform/frameworks/support/+/296313a488a01c84ddcb0801d4efee640a14070c/compose/animation/animation/src/commonMain/kotlin/androidx/compose/animation/SharedTransitionScope.kt
  - vi: SharedTransitionLayout = SharedTransitionScope + Box; SharedTransitionScope bắt đầu bằng LookaheadScope; KDoc: không gian tọa độ, overlay, khớp key (không qua scope khác), isTransitionActive, isMatchFound chỉ true sau khi phần tử mới được compose; clip/fade phải đặt sau; DefaultSpring StiffnessMediumLow; không còn @ExperimentalSharedTransitionApi trong file (SE).
  - en: SharedTransitionLayout = SharedTransitionScope + Box; SharedTransitionScope starts with LookaheadScope; KDoc: coordinate space, overlay, key matching (not across scopes), isTransitionActive, isMatchFound only true after the new element is composed; clipping/fading must come after; DefaultSpring StiffnessMediumLow; no @ExperimentalSharedTransitionApi in the file (SE).
- **Animating vectors in Compose** — Android Developers · `stable`
  https://developer.android.com/develop/ui/compose/animation/vectors
  - vi: Ba cách: AnimatedVectorDrawable, ImageVector + API animation, thư viện bên thứ ba (Lottie); animatedVectorResource + rememberAnimatedVectorPainter(image, atEnd) (CV).
  - en: Three ways: AnimatedVectorDrawable, ImageVector + animation APIs, third-party libraries (Lottie); animatedVectorResource + rememberAnimatedVectorPainter(image, atEnd) (CV).
- **AnimatedVectorPainterResources.android.kt (androidx-main @296313a4)** — AndroidX (android.googlesource.com) · `impl`
  https://android.googlesource.com/platform/frameworks/support/+/296313a488a01c84ddcb0801d4efee640a14070c/compose/animation/animation-graphics/src/androidMain/kotlin/androidx/compose/animation/graphics/res/AnimatedVectorPainterResources.android.kt
  - vi: rememberAnimatedVectorPainter = rememberVectorPainter { updateTransition(atEnd); mỗi target createVectorConfig(transition, totalDuration) }; KDoc: thay đổi atEnd được animate (CV).
  - en: rememberAnimatedVectorPainter = rememberVectorPainter { updateTransition(atEnd); each target createVectorConfig(transition, totalDuration) }; KDoc: changes to atEnd are animated (CV).
- **Animator.kt (animation-graphics, androidx-main @296313a4)** — AndroidX (android.googlesource.com) · `impl`
  https://android.googlesource.com/platform/frameworks/support/+/296313a488a01c84ddcb0801d4efee640a14070c/compose/animation/animation-graphics/src/commonMain/kotlin/androidx/compose/animation/graphics/vector/Animator.kt
  - vi: ObjectAnimator/AnimatorSet/PropertyValuesHolder → keyframes + transition.animateFloat; đích false thì spec.reversed(overallDuration) (CV).
  - en: ObjectAnimator/AnimatorSet/PropertyValuesHolder → keyframes + transition.animateFloat; a false target uses spec.reversed(overallDuration) (CV).
- **AnimatedImageVector.kt (androidx-main @296313a4)** — AndroidX (android.googlesource.com) · `impl`
  https://android.googlesource.com/platform/frameworks/support/+/296313a488a01c84ddcb0801d4efee640a14070c/compose/animation/animation-graphics/src/commonMain/kotlin/androidx/compose/animation/graphics/vector/AnimatedImageVector.kt
  - vi: AnimatedImageVector: imageVector + danh sách target (tên + Animator); totalDuration = animator dài nhất kể cả delay và repeat (CV).
  - en: AnimatedImageVector: imageVector + a list of targets (name + Animator); totalDuration = the longest animator including delays and repeats (CV).
- **VectorPainter.kt (androidx-main @296313a4)** — AndroidX (android.googlesource.com) · `impl`
  https://android.googlesource.com/platform/frameworks/support/+/296313a488a01c84ddcb0801d4efee640a14070c/compose/ui/ui/src/commonMain/kotlin/androidx/compose/ui/graphics/vector/VectorPainter.kt
  - vi: rememberVectorPainter dựng nội dung bằng Composition(VectorApplier(root), compositionContext); RenderVectorGroup (CV).
  - en: rememberVectorPainter builds its content with Composition(VectorApplier(root), compositionContext); RenderVectorGroup (CV).
- **Property Animation overview (View system)** — Android Developers · `stable`
  https://developer.android.com/develop/ui/views/animations/prop-animation
  - vi: Mỗi frame: phân số thời gian → TimeInterpolator → TypeEvaluator; View thì invalidate() khi thuộc tính đổi; mặc định 300 ms; view animation chỉ đổi chỗ vẽ, không đổi View (VM).
  - en: Each frame: elapsed fraction → TimeInterpolator → TypeEvaluator; for a View, invalidate() when the property changes; default 300 ms; view animation only changes where the View is drawn, not the View (VM).
- **MainTestClock.kt (ui-test, androidx-main @296313a4)** — AndroidX (android.googlesource.com) · `impl`
  https://android.googlesource.com/platform/frameworks/support/+/296313a488a01c84ddcb0801d4efee640a14070c/compose/ui/ui-test/src/commonMain/kotlin/androidx/compose/ui/test/MainTestClock.kt
  - vi: KDoc: đồng hồ điều khiển recomposition, withFrameNanos, LaunchedEffect; trên Android vẽ do Choreographer; frame gửi cho animation trước recompose nên cần 2 frame để có play time 0; advanceTimeBy làm tròn lên bội số frame (16 ms trên JVM), ignoreFrameDuration; autoAdvance mặc định true; advanceTimeUntil (C8).
  - en: KDoc: the clock drives recomposition, withFrameNanos, LaunchedEffect; on Android draw is Choreographer-driven; the frame goes to animations before recomposition, so play time 0 needs 2 frames; advanceTimeBy rounds up to a frame multiple (16 ms on the JVM), ignoreFrameDuration; autoAdvance true by default; advanceTimeUntil (C8).
- **Animation tooling (Android Studio)** — Android Developers · `version`
  https://developer.android.com/develop/ui/compose/animation/tooling
  - vi: Animation Preview hỗ trợ animate*AsState, Crossfade, rememberInfiniteTransition, AnimatedContent, updateTransition, AnimatedVisibility; xem từng frame, xem giá trị, đặt label (C8).
  - en: Animation Preview supports animate*AsState, Crossfade, rememberInfiniteTransition, AnimatedContent, updateTransition, AnimatedVisibility; frame-by-frame preview, value inspection, labels (C8).
- **AnimationModifier.kt (androidx-main @296313a4)** — AndroidX (android.googlesource.com) · `impl`
  https://android.googlesource.com/platform/frameworks/support/+/296313a488a01c84ddcb0801d4efee640a14070c/compose/animation/animation/src/commonMain/kotlin/androidx/compose/animation/AnimationModifier.kt
  - vi: animateContentSize = clipToBounds() then SizeAnimationModifierNode; spec mặc định spring(StiffnessMediumLow); đo con, animateTo(kích thước con) trả giá trị hiện tại, ép vào constraints đầu vào; lần đo đầu không animate; listener chỉ khi Finished, giá trị đầu là điểm ngắt; onReset xóa dữ liệu; dùng kích thước lookahead (C5).
  - en: animateContentSize = clipToBounds() then SizeAnimationModifierNode; default spec spring(StiffnessMediumLow); measures the child, animateTo(child size) returns the current value, constrained to incoming constraints; no animation on first measure; listener only on Finished, initial value is the interruption point; onReset clears data; uses the lookahead size (C5).
- **LazyItemScope.kt (androidx-main @296313a4)** — AndroidX (android.googlesource.com) · `impl`
  https://android.googlesource.com/platform/frameworks/support/+/296313a488a01c84ddcb0801d4efee640a14070c/compose/foundation/foundation/src/commonMain/kotlin/androidx/compose/foundation/lazy/LazyItemScope.kt
  - vi: KDoc của Modifier.animateItem: fade in, fade out, placement (kể cả đổi arrangement/alignment); cần key; null tắt từng phần; mặc định spring(StiffnessMediumLow); animateItemWithTransitions còn internal (C5).
  - en: KDoc of Modifier.animateItem: fade in, fade out, placement (including arrangement/alignment changes); needs keys; null turns each part off; defaults spring(StiffnessMediumLow); animateItemWithTransitions is still internal (C5).
- **LazyLayoutItemAnimation.kt (androidx-main @296313a4)** — AndroidX (android.googlesource.com) · `impl`
  https://android.googlesource.com/platform/frameworks/support/+/296313a488a01c84ddcb0801d4efee640a14070c/compose/foundation/foundation/src/commonMain/kotlin/androidx/compose/foundation/lazy/layout/LazyLayoutItemAnimation.kt
  - vi: placementDelta animate về 0, item đặt ở targetOffset + placementDelta bằng placeWithLayer (LazyListMeasuredItem.kt); alpha của GraphicsLayer cho fade; độ lệch do cuộn không animate (C5).
  - en: placementDelta animates to 0, the item is placed at targetOffset + placementDelta with placeWithLayer (LazyListMeasuredItem.kt); the GraphicsLayer alpha does the fade; scroll offsets are not animated (C5).
- **Android Animations by Tutorials (Kodeco)** — Kodeco (sách) · `guideline`
  https://www.kodeco.com/books/android-animations-by-tutorials
  - vi: Sách chủ yếu về hệ View: animator, chuyển màn hình, list (notifyItem*, ItemAnimator), cử chỉ; Compose (animateContentSize, visibility). Viết theo phiên bản cũ; API Compose được đối chiếu lại với tài liệu hiện tại.
  - en: Mostly about the View system: animators, screen transitions, lists (notifyItem*, ItemAnimator), gestures; Compose (animateContentSize, visibility). Written for older versions; Compose APIs are re-checked against current docs.

### Track D

- **The Definition of User Experience (UX)** — Nielsen Norman Group (Norman, Nielsen) · `research`
  https://www.nngroup.com/articles/definition-user-experience/
  - vi: UX bao trùm mọi tương tác; phân biệt UX, UI và usability (D0).
  - en: UX covers every interaction; UX vs UI vs usability (D0).
- **Usability 101: Introduction to Usability** — Nielsen Norman Group · `research`
  https://www.nngroup.com/articles/usability-101-introduction-to-usability/
  - vi: Năm thành phần của usability (D0).
  - en: The five components of usability (D0).
- **10 Usability Heuristics for User Interface Design** — Nielsen Norman Group (Nielsen) · `research`
  https://www.nngroup.com/articles/ten-usability-heuristics/
  - vi: Mười heuristic — quy tắc kinh nghiệm rộng, không phải hướng dẫn cụ thể (D2, D4).
  - en: The ten heuristics — broad rules of thumb, not specific guidelines (D2, D4).
- **How to Conduct a Heuristic Evaluation** — Nielsen Norman Group · `research`
  https://www.nngroup.com/articles/how-to-conduct-a-heuristic-evaluation/
  - vi: 3–5 người đánh giá độc lập rồi gộp; không thay nghiên cứu người dùng (D4).
  - en: 3–5 evaluators work independently, then consolidate; not a replacement for user research (D4).
- **Severity Ratings for Usability Problems** — Nielsen Norman Group (Nielsen) · `research`
  https://www.nngroup.com/articles/how-to-rate-the-severity-of-usability-problems/
  - vi: Thang severity 0–4; tần suất, tác động, dai dẳng; trung bình nhiều người chấm (D4).
  - en: The 0–4 severity scale; frequency, impact, persistence; average several raters (D4).
- **Memory Recognition and Recall in User Interfaces** — Nielsen Norman Group · `research`
  https://www.nngroup.com/articles/recognition-and-recall/
  - vi: Nhận ra dễ hơn nhớ lại (D1).
  - en: Recognition is easier than recall (D1).
- **Short-Term Memory and Web Usability** — Nielsen Norman Group (Nielsen) · `research`
  https://www.nngroup.com/articles/short-term-memory-and-web-usability/
  - vi: Trí nhớ ngắn hạn ~7 chunk, phai ~20 s; giới hạn menu 7 mục là hiểu lầm (D1).
  - en: Short-term memory ~7 chunks, fading in ~20 s; a 7-item menu limit is a misconception (D1).
- **Preventing User Errors: Avoiding Unconscious Slips** — Nielsen Norman Group · `research`
  https://www.nngroup.com/articles/slips/
  - vi: Định nghĩa slip và cách phòng (D3).
  - en: Slips and how to prevent them (D3).
- **Preventing User Errors: Avoiding Conscious Mistakes** — Nielsen Norman Group · `research`
  https://www.nngroup.com/articles/user-mistakes/
  - vi: Định nghĩa mistake, mô hình tư duy, xác nhận, undo (D3).
  - en: Mistakes, mental models, confirmations, undo (D3).
- **Error-Message Guidelines** — Nielsen Norman Group · `research`
  https://www.nngroup.com/articles/error-message-guidelines/
  - vi: Thông báo lỗi: hiển thị rõ, dễ hiểu, chính xác, gợi ý sửa, không đổ lỗi (D3, D9).
  - en: Error messages: visible, human-readable, precise, constructive, no blame (D3, D9).
- **Deceptive Patterns in UX: How to Recognize and Avoid Them** — Nielsen Norman Group · `research`
  https://www.nngroup.com/articles/deceptive-patterns/
  - vi: Định nghĩa và các loại deceptive pattern; chỉ để nhận diện và tránh (D5).
  - en: Definition and types of deceptive patterns; for recognizing and avoiding only (D5).
- **Simplicity Wins over Abundance of Choice** — Nielsen Norman Group · `research`
  https://www.nngroup.com/articles/simplicity-vs-choice/
  - vi: Nhiều lựa chọn tốn công hơn (D5).
  - en: More choices mean more effort (D5).
- **Progressive Disclosure** — Nielsen Norman Group (Nielsen) · `research`
  https://www.nngroup.com/articles/progressive-disclosure/
  - vi: Hiện cái quan trọng trước; hơn 2 tầng thường kém (D5).
  - en: Show the important things first; more than 2 levels tends to be poor (D5).
- **Hick's Law** — Laws of UX (Jon Yablonski) · `research`
  https://lawsofux.com/hicks-law/
  - vi: NGUỒN THỨ CẤP: thời gian quyết định tăng theo số và độ phức tạp lựa chọn; không có công thức trên trang (D5).
  - en: SECONDARY SOURCE: decision time grows with the number and complexity of choices; no formula on the page (D5).
- **When to Use Which User-Experience Research Methods** — Nielsen Norman Group · `research`
  https://www.nngroup.com/articles/which-ux-research-methods/
  - vi: Ba trục: thái độ/hành vi, định tính/định lượng, bối cảnh dùng (D6).
  - en: Three axes: attitudinal/behavioral, qualitative/quantitative, context of use (D6).
- **Why You Only Need to Test with 5 Users** — Nielsen Norman Group (Nielsen, 2000) · `quant-model`
  https://www.nngroup.com/articles/why-you-only-need-to-test-with-5-users/
  - vi: Công thức N(1 − (1 − L)^n), L điển hình 31%, các giả định (D7).
  - en: The N(1 − (1 − L)^n) formula, typical L = 31%, the assumptions (D7).
- **How Many Test Users in a Usability Study?** — Nielsen Norman Group (Nielsen) · `research`
  https://www.nngroup.com/articles/how-many-test-users/
  - vi: 5 người cho nghiên cứu định tính; định lượng ≥ 20; nhiều nhóm người dùng (D7).
  - en: 5 users for qualitative studies; quantitative ≥ 20; several user groups (D7).
- **Success Rate: The Simplest Usability Metric** — Nielsen Norman Group · `research`
  https://www.nngroup.com/articles/success-rate-the-simplest-usability-metric/
  - vi: Mọi tỉ lệ cần khoảng tin cậy; ví dụ adjusted Wald 20% → 13–29% (D8).
  - en: Every percentage needs a confidence interval; adjusted Wald example 20% → 13–29% (D8).
- **Beyond the NPS: Measure Perceived Usability with the SUS, NASA-TLX, and the Single Ease Question** — Nielsen Norman Group · `research`
  https://www.nngroup.com/articles/measuring-perceived-usability/
  - vi: SUS 0–100, không phải phần trăm; trung bình 68 (D8).
  - en: SUS is 0–100, not a percentage; average 68 (D8).
- **Measuring Usability with the System Usability Scale (SUS)** — MeasuringU (Jeff Sauro) · `quant-model`
  https://measuringu.com/sus/
  - vi: Cách chấm SUS và "SUS không phải phần trăm" (D8).
  - en: How to score SUS and "SUS scores are not percentages" (D8).
- **Confidence Interval Calculator for a Completion Rate** — MeasuringU (Jeff Sauro) · `quant-model`
  https://measuringu.com/wald/
  - vi: Tỉ lệ hiệu chỉnh của adjusted Wald (D8).
  - en: The adjusted Wald proportion (D8).
- **Binomial proportion confidence interval (Agresti–Coull)** — Wikipedia · `quant-model`
  https://en.wikipedia.org/wiki/Binomial_proportion_confidence_interval
  - vi: Dạng đầy đủ của khoảng Agresti–Coull dùng cho adjusted Wald (D8).
  - en: The full form of the Agresti–Coull interval used for adjusted Wald (D8).
- **The Four Dimensions of Tone of Voice** — Nielsen Norman Group · `research`
  https://www.nngroup.com/articles/tone-of-voice-dimensions/
  - vi: Bốn chiều của tone (D9).
  - en: The four dimensions of tone (D9).
- **Per-app language preferences** — Android Developers · `stable`
  https://developer.android.com/guide/topics/resources/app-languages
  - vi: Ngôn ngữ theo app từ Android 13 (API 33); AppCompatDelegate cho bản cũ (D9, X8).
  - en: Per-app languages since Android 13 (API 33); AppCompatDelegate for older versions (D9, X8).
- **Localize your app** — Android Developers · `stable`
  https://developer.android.com/guide/topics/resources/localization
  - vi: Tài nguyên chuỗi theo ngôn ngữ; đọc thêm cho X8 (D9).
  - en: Language-specific string resources; further reading for X8 (D9).
- **The Double Diamond** — Design Council · `author-framework`
  https://www.designcouncil.org.uk/resources/the-double-diamond/
  - vi: Bốn pha Discover, Define, Develop, Deliver; quy trình là "lời mời", hay quay lại đầu (D0).
  - en: Four phases Discover, Define, Develop, Deliver; a process is "an invitation", often returning to the start (D0).
- **The Design Sprint** — GV · `author-framework`
  https://www.gv.com/sprint/
  - vi: Năm ngày: map, sketch, decide, prototype, test (D10).
  - en: Five days: map, sketch, decide, prototype, test (D10).
- **Design for How People Think (John Whalen, O'Reilly, 2019)** — O'Reilly (sách) · `research`
  https://www.oreilly.com/library/view/design-for-how/9781491985441/
  - vi: Sáu "bộ óc" (framework của tác giả); thị giác, chú ý, popout, vùng nhìn nét, "chỗ không ai nhìn"; trí nhớ trừu tượng, khuôn mẫu, mô hình tư duy (D1).
  - en: The six "minds" (the author's framework); vision, attention, popout, the sharp visual zone, "where nobody looks"; abstract memory, stereotypes, mental models (D1).
- **The Design of Everyday Things, Revised and Expanded Edition (Don Norman, Basic Books, 2013)** — Basic Books (sách) · `research`
  https://www.hachettebookgroup.com/titles/don-norman/the-design-of-everyday-things/9780465050659/
  - vi: Mô hình khái niệm và system image; kiến thức trong đầu và trong thế giới, trí nhớ ngắn hạn 5–7 (thực hành 3–5), Bảng 3.1 (D1).
  - en: Conceptual models and the system image; knowledge in the head and in the world, short-term memory 5–7 (3–5 in practice), Table 3.1 (D1).
- **Don't Make Me Think, Revisited, 3rd edition (Steve Krug, New Riders, 2014)** — New Riders (sách) · `author-framework`
  https://sensible.com/dont-make-me-think/
  - vi: Ba "sự thật": quét, satisficing, xoay xở cho qua (D1).
  - en: Three "facts of life": scanning, satisficing, muddling through (D1).
- **SnackbarHost.kt (androidx-main @296313a4, Material 3)** — AndroidX (android.googlesource.com) · `impl`
  https://android.googlesource.com/platform/frameworks/support/+/296313a488a01c84ddcb0801d4efee640a14070c/compose/material3/material3/src/commonMain/kotlin/androidx/compose/material3/SnackbarHost.kt
  - vi: showSnackbar: không action → Short, có action → Indefinite; toMillis: Short 4000L, Long 10000L dưới TODO; qua calculateRecommendedTimeoutMillis (D1).
  - en: showSnackbar: no action → Short, with an action → Indefinite; toMillis: Short 4000L, Long 10000L under a TODO; through calculateRecommendedTimeoutMillis (D1).
- **AndroidAccessibilityManager.android.kt (androidx-main @296313a4, compose/ui)** — AndroidX (android.googlesource.com) · `impl`
  https://android.googlesource.com/platform/frameworks/support/+/296313a488a01c84ddcb0801d4efee640a14070c/compose/ui/ui/src/androidMain/kotlin/androidx/compose/ui/platform/AndroidAccessibilityManager.android.kt
  - vi: API 29+: gọi getRecommendedTimeoutMillis của nền tảng; dưới 29: vô hạn chỉ khi có control và touch exploration bật (D1).
  - en: API 29+: calls the platform's getRecommendedTimeoutMillis; below 29: infinite only with controls and touch exploration on (D1).
- **AccessibilityManager.getRecommendedTimeoutMillis (API 29)** — Android Developers · `stable`
  https://developer.android.com/reference/android/view/accessibility/AccessibilityManager#getRecommendedTimeoutMillis(int,%20int)
  - vi: Thời gian khuyến nghị cho thay đổi UI theo nhu cầu của người dùng hiện tại; cờ FLAG_CONTENT_ICONS/TEXT/CONTROLS (D1).
  - en: The recommended timeout for UI changes needed by the current user; flags FLAG_CONTENT_ICONS/TEXT/CONTROLS (D1).
- **Journey Mapping 101** — Nielsen Norman Group · `research` · đọc thêm / further reading
  https://www.nngroup.com/articles/journey-mapping-101/
  - vi: Đọc thêm (chưa dùng làm nguồn cho khẳng định cụ thể).
  - en: Further reading (not yet used as the source of a specific claim).
- **Personas** — Nielsen Norman Group · `research` · đọc thêm / further reading
  https://www.nngroup.com/articles/persona/
  - vi: Đọc thêm (chưa dùng làm nguồn cho khẳng định cụ thể).
  - en: Further reading (not yet used as the source of a specific claim).
- **User Interviews** — Nielsen Norman Group · `research` · đọc thêm / further reading
  https://www.nngroup.com/articles/user-interviews/
  - vi: Đọc thêm (chưa dùng làm nguồn cho khẳng định cụ thể).
  - en: Further reading (not yet used as the source of a specific claim).
- **Thinking Aloud: The #1 Usability Tool** — Nielsen Norman Group · `research` · đọc thêm / further reading
  https://www.nngroup.com/articles/thinking-aloud-the-1-usability-tool/
  - vi: Đọc thêm (chưa dùng làm nguồn cho khẳng định cụ thể).
  - en: Further reading (not yet used as the source of a specific claim).
- **UX Writing: Study Guide** — Nielsen Norman Group · `research` · đọc thêm / further reading
  https://www.nngroup.com/articles/ux-writing-study-guide/
  - vi: Đọc thêm (chưa dùng làm nguồn cho khẳng định cụ thể).
  - en: Further reading (not yet used as the source of a specific claim).
- **Design Thinking 101** — Nielsen Norman Group · `research` · đọc thêm / further reading
  https://www.nngroup.com/articles/design-thinking/
  - vi: Đọc thêm (chưa dùng làm nguồn cho khẳng định cụ thể).
  - en: Further reading (not yet used as the source of a specific claim).

### Track E

- **Web Content Accessibility Guidelines (WCAG) 2.2** — W3C · `normative`
  https://www.w3.org/TR/WCAG22/
  - vi: Relative luminance (ngưỡng 0.04045), contrast ratio, chữ lớn, các tiêu chí 1.4.1, 1.4.3, 1.4.4, 1.4.6, 1.4.11, 2.2.2, 2.3.3, 2.4.7, 2.5.5, 2.5.8 (E3, E5, E9, E10).
  - en: Relative luminance (0.04045 threshold), contrast ratio, large text, criteria 1.4.1, 1.4.3, 1.4.4, 1.4.6, 1.4.11, 2.2.2, 2.3.3, 2.4.7, 2.5.5, 2.5.8 (E3, E5, E9, E10).
- **Accessibility Principles** — W3C WAI · `normative`
  https://www.w3.org/WAI/fundamentals/accessibility-principles/
  - vi: Bốn nguyên tắc: perceivable, operable, understandable, robust (E10).
  - en: Four principles: perceivable, operable, understandable, robust (E10).
- **Use window size classes** — Android Developers · `stable`
  https://developer.android.com/develop/ui/compose/layouts/adaptive/use-window-size-classes
  - vi: Breakpoint: compact < 600dp, medium < 840, expanded < 1200, large < 1600, extra-large (E4).
  - en: Breakpoints: compact < 600dp, medium < 840, expanded < 1200, large < 1600, extra-large (E4).
- **Canonical layouts** — Android Developers · `stable`
  https://developer.android.com/develop/ui/compose/layouts/adaptive/canonical-layouts
  - vi: List-detail, supporting pane, feed; ListDetailPaneScaffold (E4).
  - en: List-detail, supporting pane, feed; ListDetailPaneScaffold (E4).
- **Accessibility (Android design foundations)** — Android Developers · `ds-guideline`
  https://developer.android.com/design/ui/mobile/guides/foundations/accessibility
  - vi: Target ít nhất 48 dp; tương phản chữ 4.5:1, thành phần 3:1 (E5, E10).
  - en: Targets at least 48 dp; text contrast 4.5:1, components 3:1 (E5, E10).
- **Accessibility API defaults** — Android Developers · `stable`
  https://developer.android.com/develop/ui/compose/accessibility/api-defaults
  - vi: minimumInteractiveComponentSize giữ ≥ 48 dp (E5).
  - en: minimumInteractiveComponentSize reserves ≥ 48 dp (E5).
- **Material Design 3 in Compose** — Android Developers · `stable`
  https://developer.android.com/develop/ui/compose/designsystems/material3
  - vi: MaterialTheme(colorScheme, typography, shapes); dynamic color từ Android 12; NavigationBar/Rail/Drawer theo kích thước (E3, E4, E8).
  - en: MaterialTheme(colorScheme, typography, shapes); dynamic color from Android 12; NavigationBar/Rail/Drawer by size (E3, E4, E8).
- **Typography – type scale tokens** — Material Design 3 (Google) · `ds-guideline`
  https://m3.material.io/styles/typography/type-scale-tokens
  - vi: Cỡ, line height, tracking của 15 vai trò chữ; đọc 2026-11-21 (E2).
  - en: Size, line height and tracking of the 15 type roles; read 2026-11-21 (E2).
- **Easing and duration – tokens & specs** — Material Design 3 (Google) · `ds-guideline`
  https://m3.material.io/styles/motion/easing-and-duration/tokens-specs
  - vi: Token easing (cubic-bezier) và duration 50–1000 ms; đọc 2026-11-21 (E9).
  - en: Easing (cubic-bezier) and duration tokens 50–1000 ms; read 2026-11-21 (E9).
- **States – state layers** — Material Design 3 (Google) · `ds-guideline`
  https://m3.material.io/foundations/interaction/states/state-layers
  - vi: State layer: hover 8%, focus 10%, press 10%, drag 16%; đọc 2026-11-21 (E6).
  - en: State layers: hover 8%, focus 10%, press 10%, drag 16%; read 2026-11-21 (E6).
- **Color theming (Material Components for Android)** — Material Components for Android · `ds-guideline`
  https://github.com/material-components/material-components-android/blob/master/docs/theming/Color.md
  - vi: Danh sách color role và cặp on-; site chỉ dùng tên vai trò (E3, E8).
  - en: The list of color roles and their on- pairs; the site uses role names only (E3, E8).
- **Fitts's Law and Its Applications in UX** — Nielsen Norman Group (Budiu) · `quant-model`
  https://www.nngroup.com/articles/fitts-law/
  - vi: Thời gian di chuyển phụ thuộc kích thước và khoảng cách; T = a + b·log2(2D/W) (E5).
  - en: Movement time depends on target size and distance; T = a + b·log2(2D/W) (E5).
- **Response Times: The 3 Important Limits** — Nielsen Norman Group (Nielsen) · `research`
  https://www.nngroup.com/articles/response-times-3-important-limits/
  - vi: Mốc 0,1 s, 1 s, 10 s (E7).
  - en: The 0.1 s, 1 s and 10 s limits (E7).
- **Proximity Principle in Visual Design** — Nielsen Norman Group · `research` · đọc thêm / further reading
  https://www.nngroup.com/articles/gestalt-proximity/
  - vi: Đọc thêm (chưa dùng làm nguồn cho khẳng định cụ thể).
  - en: Further reading (not yet used as the source of a specific claim).
- **The Aesthetic-Usability Effect** — Nielsen Norman Group · `research` · đọc thêm / further reading
  https://www.nngroup.com/articles/aesthetic-usability-effect/
  - vi: Đọc thêm (chưa dùng làm nguồn cho khẳng định cụ thể).
  - en: Further reading (not yet used as the source of a specific claim).
- **Dark Mode vs. Light Mode** — Nielsen Norman Group · `research` · đọc thêm / further reading
  https://www.nngroup.com/articles/dark-mode/
  - vi: Đọc thêm (chưa dùng làm nguồn cho khẳng định cụ thể).
  - en: Further reading (not yet used as the source of a specific claim).
- **Placeholders in Form Fields Are Harmful** — Nielsen Norman Group · `research` · đọc thêm / further reading
  https://www.nngroup.com/articles/form-design-placeholders/
  - vi: Đọc thêm (chưa dùng làm nguồn cho khẳng định cụ thể).
  - en: Further reading (not yet used as the source of a specific claim).
- **Hamburger Menus and Hidden Navigation** — Nielsen Norman Group · `research` · đọc thêm / further reading
  https://www.nngroup.com/articles/hamburger-menus/
  - vi: Đọc thêm (chưa dùng làm nguồn cho khẳng định cụ thể).
  - en: Further reading (not yet used as the source of a specific claim).
- **Design Systems 101** — Nielsen Norman Group · `research` · đọc thêm / further reading
  https://www.nngroup.com/articles/design-systems-101/
  - vi: Đọc thêm (chưa dùng làm nguồn cho khẳng định cụ thể).
  - en: Further reading (not yet used as the source of a specific claim).
- **The Role of Animation and Motion in UX** — Nielsen Norman Group · `research` · đọc thêm / further reading
  https://www.nngroup.com/articles/animation-purpose-ux/
  - vi: Đọc thêm (chưa dùng làm nguồn cho khẳng định cụ thể).
  - en: Further reading (not yet used as the source of a specific claim).
- **Understanding SC 1.4.3: Contrast (Minimum)** — W3C WAI · `normative` · đọc thêm / further reading
  https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html
  - vi: Đọc thêm (chưa dùng làm nguồn cho khẳng định cụ thể).
  - en: Further reading (not yet used as the source of a specific claim).
- **Understanding SC 2.5.8: Target Size (Minimum)** — W3C WAI · `normative` · đọc thêm / further reading
  https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html
  - vi: Đọc thêm (chưa dùng làm nguồn cho khẳng định cụ thể).
  - en: Further reading (not yet used as the source of a specific claim).
- **Understanding SC 2.3.3: Animation from Interactions** — W3C WAI · `normative` · đọc thêm / further reading
  https://www.w3.org/WAI/WCAG22/Understanding/animation-from-interactions.html
  - vi: Đọc thêm (chưa dùng làm nguồn cho khẳng định cụ thể).
  - en: Further reading (not yet used as the source of a specific claim).

### Track F

- **Basic syntax** — Kotlin docs (JetBrains) · `stable`
  https://kotlinlang.org/docs/basic-syntax.html
  - vi: val gán một lần, var gán lại được (K1).
  - en: val is assigned once, var can be reassigned (K1).
- **Numbers** — Kotlin docs (JetBrains) · `stable`
  https://kotlinlang.org/docs/numbers.html
  - vi: Chia nguyên bỏ phần lẻ; chuyển kiểu phải tường minh; tràn số không báo lỗi; boxing và cache -128..127 trên JVM (K1).
  - en: Integer division drops the fraction; conversions are explicit; overflow is silent; boxing and the -128..127 cache on the JVM (K1).
- **Conditions and loops** — Kotlin docs (JetBrains) · `stable`
  https://kotlinlang.org/docs/control-flow.html
  - vi: if và when là biểu thức; nhánh khớp đầu tiên; when dạng biểu thức phải đủ trường hợp (K1).
  - en: if and when are expressions; the first matching branch wins; a when expression must be exhaustive (K1).
- **Null safety** — Kotlin docs (JetBrains) · `stable`
  https://kotlinlang.org/docs/null-safety.html
  - vi: Kiểu nullable, ?., ?:, !!, let, as?; danh sách nguyên nhân có thể gây NPE trong Kotlin (K2).
  - en: Nullable types, ?., ?:, !!, let, as?; the list of possible NPE causes in Kotlin (K2).
- **Type checks and casts** — Kotlin docs (JetBrains) · `stable`
  https://kotlinlang.org/docs/typecasts.html
  - vi: Smart cast và bảng điều kiện: val cục bộ, val property, var cục bộ, var property (K2).
  - en: Smart casts and their conditions: local val, val property, local var, var property (K2).
- **Calling Java from Kotlin** — Kotlin docs (JetBrains) · `stable`
  https://kotlinlang.org/docs/java-interop.html
  - vi: Platform type T!, kiểm tra null được nới lỏng, chèn kiểm tra khi gán vào kiểu non-null; các họ chú thích nullability, có Android và JSpecify (K2).
  - en: Platform types T!, relaxed null checks, a check inserted on assignment to a non-null type; nullability annotation families including Android and JSpecify (K2).
- **Classes** — Kotlin docs (JetBrains) · `stable`
  https://kotlinlang.org/docs/classes.html
  - vi: Constructor chính, khối init chạy theo thứ tự xuất hiện, xen với giá trị khởi tạo property (K3).
  - en: Primary constructor; init blocks run in order of appearance, interleaved with property initialisers (K3).
- **Inheritance** — Kotlin docs (JetBrains) · `stable`
  https://kotlinlang.org/docs/inheritance.html
  - vi: Class final mặc định, open/override; lớp cha khởi tạo trước lớp con; tránh thành viên open trong khởi tạo của lớp cha (K3).
  - en: Classes are final by default, open/override; the superclass initialises before the subclass; avoid open members in base-class initialisation (K3).
- **Interfaces** — Kotlin docs (JetBrains) · `stable`
  https://kotlinlang.org/docs/interfaces.html
  - vi: Interface có hàm có thân nhưng không giữ trạng thái (K3).
  - en: Interfaces can have function bodies but hold no state (K3).
- **Object declarations and expressions** — Kotlin docs (JetBrains) · `stable`
  https://kotlinlang.org/docs/object-declarations.html
  - vi: object declaration khởi tạo lười ở lần truy cập đầu, an toàn luồng; companion khi lớp được nạp; object expression ngay tại chỗ (K3).
  - en: Object declarations initialise lazily on first access, thread-safely; companions when the class loads; object expressions immediately (K3).
- **Properties** — Kotlin docs (JetBrains) · `stable`
  https://kotlinlang.org/docs/properties.html
  - vi: Getter/setter tự viết, setter không chạy lúc khởi tạo, field; lateinit: điều kiện, ngoại lệ, isInitialized (K3).
  - en: Custom getters/setters, the setter does not run during initialisation, field; lateinit: requirements, exception, isInitialized (K3).
- **Data classes** — Kotlin docs (JetBrains) · `stable`
  https://kotlinlang.org/docs/data-classes.html
  - vi: equals/hashCode, toString, componentN, copy sinh từ property của constructor chính; property trong thân bị loại; copy là bản sao nông (K4).
  - en: equals/hashCode, toString, componentN, copy generated from primary constructor properties; body properties excluded; copy is shallow (K4).
- **Equality** — Kotlin docs (JetBrains) · `stable`
  https://kotlinlang.org/docs/equality.html
  - vi: == là bằng nhau cấu trúc (a?.equals(b) ?: (b === null)), === là bằng nhau tham chiếu (K4).
  - en: == is structural equality (a?.equals(b) ?: (b === null)), === is referential equality (K4).
- **Enum classes** — Kotlin docs (JetBrains) · `stable`
  https://kotlinlang.org/docs/enum-classes.html
  - vi: name, ordinal, entries; valueOf cần tên khớp chính xác, nếu không ném IllegalArgumentException; entries.getOrNull(index) (K5).
  - en: name, ordinal, entries; valueOf needs an exact name or throws IllegalArgumentException; entries.getOrNull(index) (K5).
- **use (kotlin.io)** — Kotlin API reference (JetBrains) · `stable`
  https://kotlinlang.org/api/core/kotlin-stdlib/kotlin.io/use.html
  - vi: use chạy khối trên tài nguyên Closeable rồi đóng nó đúng cách, dù có ngoại lệ hay không (K6).
  - en: use runs the block on a Closeable resource and then closes it correctly whether or not an exception is thrown (K6).
- **Closeable.kt (stdlib, tag v2.1.0)** — JetBrains/kotlin (mã nguồn) · `version`
  https://github.com/JetBrains/kotlin/blob/v2.1.0/libraries/stdlib/jvm/src/kotlin/io/Closeable.kt
  - vi: Cài đặt use: bắt Throwable để nhớ, ném lại, trong finally gọi closeFinally; nếu close() cũng ném thì lỗi đó được addSuppressed vào lỗi chính (K6).
  - en: The use implementation: catches Throwable to remember it, rethrows, and calls closeFinally in finally; if close() also throws, that error is addSuppressed onto the main one (K6).
- **Collections overview** — Kotlin docs (JetBrains) · `stable`
  https://kotlinlang.org/docs/collections-overview.html
  - vi: Mỗi loại có interface read-only và Mutable; ưu tiên read-only khi nơi gọi không cần sửa; read-only khác bất biến (kotlinx-collections-immutable); Map không kế thừa Collection (K7).
  - en: Each type has a read-only and a Mutable interface; prefer read-only when callers need not modify; read-only is not immutable (kotlinx-collections-immutable); Map does not extend Collection (K7).
- **Collection types** — Kotlin docs (JetBrains) · `stable`
  https://kotlinlang.org/docs/collection-types.html
  - vi: List, Set, Map và cách so bằng; cài đặt mặc định ArrayList, LinkedHashSet, LinkedHashMap giữ thứ tự thêm vào; HashSet/HashMap không bảo đảm thứ tự (K7).
  - en: List, Set, Map and how they compare; default implementations ArrayList, LinkedHashSet, LinkedHashMap keep insertion order; HashSet/HashMap do not guarantee order (K7).
- **Create collections** — Kotlin docs (JetBrains) · `stable`
  https://kotlinlang.org/docs/constructing-collections.html
  - vi: Gán là tạo tham chiếu mới tới cùng object; tham chiếu List tới MutableList thấy trạng thái hiện tại; toList/toMutableList là bản chụp nông; buildList (K7).
  - en: Assignment creates a new reference to the same object; a List reference to a MutableList shows the current state; toList/toMutableList are shallow snapshots; buildList (K7).
- **Collection transformations** — Kotlin docs (JetBrains) · `stable`
  https://kotlinlang.org/docs/collection-transformations.html
  - vi: map trả về list các kết quả; mapKeys/mapValues biến đổi key hoặc value của map (K7).
  - en: map returns a list of the results; mapKeys/mapValues transform a map's keys or values (K7).
- **Map-specific operations** — Kotlin docs (JetBrains) · `stable`
  https://kotlinlang.org/docs/map-operations.html
  - vi: get trả null khi thiếu key, getValue ném ngoại lệ, getOrDefault/getOrElse; filterKeys/filterValues trả map mới (K7).
  - en: get returns null for a missing key, getValue throws, getOrDefault/getOrElse; filterKeys/filterValues return a new map (K7).
- **_Maps.kt (stdlib, tag v2.1.0)** — JetBrains/kotlin (mã nguồn) · `version`
  https://github.com/JetBrains/kotlin/blob/v2.1.0/libraries/stdlib/common/src/generated/_Maps.kt
  - vi: Chữ ký Map<out K, V>.map(transform): List<R>, tức map trên Map trả về List (K7).
  - en: The signature Map<out K, V>.map(transform): List<R>, so map over a Map returns a List (K7).
- **Higher-order functions and lambdas** — Kotlin docs (JetBrains) · `stable`
  https://kotlinlang.org/docs/lambdas.html
  - vi: Kiểu hàm, lambda, it, trailing lambda, tham chiếu hàm; closure: lambda đọc và sửa được biến ở phạm vi ngoài (K8).
  - en: Function types, lambdas, it, trailing lambdas, function references; closures: a lambda can read and modify variables of the outer scope (K8).
- **Inline functions** — Kotlin docs (JetBrains) · `stable`
  https://kotlinlang.org/docs/inline-functions.html
  - vi: Hàm bậc cao: mỗi hàm là một object và bắt closure; inline chép hàm và lambda vào chỗ gọi; noinline, crossinline, non-local return, reified; cảnh báo khi không có gì để inline (K8).
  - en: Higher-order functions: each function is an object capturing a closure; inline copies the function and its lambdas to the call site; noinline, crossinline, non-local return, reified; a warning when there is nothing to inline (K8).
- **Returns and jumps** — Kotlin docs (JetBrains) · `stable`
  https://kotlinlang.org/docs/returns.html
  - vi: return trần chỉ thoát hàm có tên hoặc hàm ẩn danh; return@label thoát lambda (giống continue); giả lập break bằng run (K8).
  - en: A bare return exits only a named or anonymous function; return@label exits the lambda (like continue); break simulated with run (K8).
- **What's new in Kotlin 2.0.0** — Kotlin docs (JetBrains) · `version`
  https://kotlinlang.org/docs/whatsnew20.html
  - vi: Từ Kotlin 2.0.0, lambda (không inline) mặc định sinh bằng invokedynamic thay cho lớp ẩn danh; -Xlambdas=class giữ cách cũ (K8).
  - en: From Kotlin 2.0.0, (non-inline) lambdas are generated with invokedynamic by default instead of anonymous classes; -Xlambdas=class keeps the old way (K8).
- **Functional Kotlin (Marcin Moskała)** — Kt. Academy (sách) · `guideline`
  https://leanpub.com/kotlin_functional
  - vi: Hàm inline: thân thay vào chỗ gọi, lambda tham số cũng được inline, ít object hơn; map/filter của stdlib là inline; crossinline và noinline (K8).
  - en: Inline functions: the body replaces the call, lambda parameters are inlined too, fewer objects; stdlib map/filter are inline; crossinline and noinline (K8).
- **Sequences** — Kotlin docs (JetBrains) · `stable`
  https://kotlinlang.org/docs/sequences.html
  - vi: Iterable xử lý háo hức, mỗi bước tạo collection trung gian; Sequence xử lý lười, từng phần tử qua cả chuỗi, chỉ chạy khi có thao tác cuối; overhead đáng kể với collection nhỏ; generateSequence, sequence { yield } (K9).
  - en: Iterable processing is eager, each step producing an intermediate collection; Sequence is lazy, element by element through the chain, running only on a terminal operation; noticeable overhead for small collections; generateSequence, sequence { yield } (K9).
- **Generics: in, out, where** — Kotlin docs (JetBrains) · `stable`
  https://kotlinlang.org/docs/generics.html
  - vi: Generic Java bất biến; declaration-site variance: out (chỉ ở vị trí trả ra, C<Base> là cha của C<Derived>), in (ngược lại); type projection, star-projection; upper bound; type erasure, ép kiểu generic không kiểm được lúc chạy (K10).
  - en: Java generics are invariant; declaration-site variance: out (only in out-positions, C<Base> is a supertype of C<Derived>), in (the reverse); type projections, star-projections; upper bounds; type erasure, generic casts unchecked at runtime (K10).
- **Collections.kt (builtins, tag v2.1.0)** — JetBrains/kotlin (mã nguồn) · `version`
  https://github.com/JetBrains/kotlin/blob/v2.1.0/libraries/stdlib/jvm/builtins/Collections.kt
  - vi: Khai báo Collection<out E>, List<out E>, MutableList<E>, Map<K, out V> (K10).
  - en: The declarations Collection<out E>, List<out E>, MutableList<E>, Map<K, out V> (K10).
- **Flow.kt (kotlinx.coroutines 1.9.0)** — Kotlin/kotlinx.coroutines (mã nguồn) · `version`
  https://github.com/Kotlin/kotlinx.coroutines/blob/1.9.0/kotlinx-coroutines-core/common/src/flow/Flow.kt
  - vi: Khai báo public interface Flow<out T> (K10).
  - en: The declaration public interface Flow<out T> (K10).
- **Advanced Kotlin (Marcin Moskała)** — Kt. Academy (sách) · `guideline`
  https://leanpub.com/advanced_kotlin
  - vi: Variance: Nothing là kiểu con của mọi kiểu nên List<Nothing> hợp với mọi list; mẫu Response<out R, out E> với Success/Failure kế thừa Response<R, Nothing> (K10).
  - en: Variance: Nothing is a subtype of every type, so List<Nothing> fits every list; the Response<out R, out E> pattern with Success/Failure extending Response<R, Nothing> (K10).
- **Delegated properties** — Kotlin docs (JetBrains) · `stable`
  https://kotlinlang.org/docs/delegated-properties.html
  - vi: by gọi getValue/setValue của delegate; trình biên dịch sinh prop$delegate; lazy mặc định synchronized, PUBLICATION, NONE; observable, vetoable, map, ủy quyền cho property khác (K11).
  - en: by calls the delegate's getValue/setValue; the compiler generates prop$delegate; lazy is synchronized by default, PUBLICATION, NONE; observable, vetoable, map, delegating to another property (K11).
- **Delegation** — Kotlin docs (JetBrains) · `stable`
  https://kotlinlang.org/docs/delegation.html
  - vi: class Derived(b: Base) : Base by b: trình biên dịch sinh các hàm của Base chuyển tiếp sang b; override thắng, nhưng b không gọi được override đó (K11).
  - en: class Derived(b: Base) : Base by b: the compiler generates Base's members forwarding to b; overrides win, but b cannot call those overrides (K11).
- **Lazy.kt và LazyJVM.kt (stdlib, tag v2.1.0)** — JetBrains/kotlin (mã nguồn) · `version`
  https://github.com/JetBrains/kotlin/blob/v2.1.0/libraries/stdlib/jvm/src/kotlin/util/LazyJVM.kt
  - vi: lazy {} là SynchronizedLazyImpl (khóa); PUBLICATION là SafePublicationLazyImpl (compareAndSet, initializer có thể chạy nhiều lần); NONE là UnsafeLazyImpl, Lazy.kt ghi hành vi với nhiều luồng là không xác định (K11).
  - en: lazy {} is SynchronizedLazyImpl (locks); PUBLICATION is SafePublicationLazyImpl (compareAndSet, the initializer may run several times); NONE is UnsafeLazyImpl, and Lazy.kt says its multi-thread behaviour is unspecified (K11).
- **ActivityViewModelLazy.kt (androidx-main @296313a4)** — AndroidX (mã nguồn) · `version`
  https://android.googlesource.com/platform/frameworks/support/+/296313a488a01c84ddcb0801d4efee640a14070c/activity/activity/src/main/java/androidx/activity/ActivityViewModelLazy.kt
  - vi: ComponentActivity.viewModels() là hàm inline reified trả về Lazy<VM>, cụ thể là ViewModelLazy (K11).
  - en: ComponentActivity.viewModels() is an inline reified function returning Lazy<VM>, namely a ViewModelLazy (K11).
- **ViewModelLazy.kt (androidx-main @296313a4)** — AndroidX (mã nguồn) · `version`
  https://android.googlesource.com/platform/frameworks/support/+/296313a488a01c84ddcb0801d4efee640a14070c/lifecycle/lifecycle-viewmodel/src/commonMain/kotlin/androidx/lifecycle/ViewModelLazy.kt
  - vi: ViewModelLazy giữ ViewModel trong biến cached; lần đọc đầu lấy từ ViewModelProvider rồi nhớ lại (K11).
  - en: ViewModelLazy keeps the ViewModel in a cached variable; the first read gets it from ViewModelProvider and remembers it (K11).
- **Scope functions** — Kotlin docs (JetBrains) · `stable`
  https://kotlinlang.org/docs/scope-functions.html
  - vi: Bảng let/run/with/apply/also: tham chiếu this hay it, trả kết quả lambda hay object; gợi ý chọn; tránh lồng scope function vì dễ lẫn this và it; takeIf/takeUnless (K12).
  - en: The let/run/with/apply/also table: this or it, lambda result or the object; how to choose; avoid nesting scope functions because this and it get confusing; takeIf/takeUnless (K12).
- **Type-safe builders** — Kotlin docs (JetBrains) · `stable`
  https://kotlinlang.org/docs/type-safe-builders.html
  - vi: Builder dùng lambda có receiver; không có marker thì gọi được thành viên của mọi receiver ngầm; @DslMarker chỉ cho receiver gần nhất, receiver ngoài phải ghi this@… (K12).
  - en: Builders use lambdas with receivers; without a marker, members of every implicit receiver are callable; @DslMarker allows only the nearest receiver, outer ones need an explicit this@… (K12).
- **Calling Kotlin from Java** — Kotlin docs (JetBrains) · `stable`
  https://kotlinlang.org/docs/java-to-kotlin-interop.html
  - vi: Property thành getter/setter (quy tắc is); hàm cấp file thành static của lớp TênFileKt, @file:JvmName; @JvmField, const, lateinit thành field; companion và @JvmStatic; @JvmName; tham số mặc định và @JvmOverloads; @Throws; kiểm null lúc chạy cho tham số non-null (K13).
  - en: Properties become getters/setters (the is rule); file-level functions become statics of a FileNameKt class, @file:JvmName; @JvmField, const, lateinit become fields; companions and @JvmStatic; @JvmName; default parameters and @JvmOverloads; @Throws; runtime null checks for non-null parameters (K13).
- **NumberFormatException (Java SE 17 API)** — Oracle · `stable`
  https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/lang/NumberFormatException.html
  - vi: NumberFormatException là lớp con của IllegalArgumentException, nên thứ tự catch quan trọng (K6).
  - en: NumberFormatException is a subclass of IllegalArgumentException, so catch order matters (K6).
- **Kotlin Essentials (Marcin Moskała)** — Kt. Academy (sách) · `guideline`
  https://leanpub.com/kotlin_developers
  - vi: Biến, kiểu cơ bản, câu điều kiện, hàm; giá trị nào cũng là object, trình biên dịch tối ưu thành kiểu nguyên thủy (K1).
  - en: Variables, basic types, conditions, functions; every value is an object, optimised to primitives by the compiler (K1).
- **Kotlin Exercises (Marcin Moskała)** — Kt. Academy (sách) · `guideline`
  https://leanpub.com/kotlin_exercises
  - vi: Nguồn bài tập của track, diễn đạt lại theo ứng dụng Hẹn Khám (K1: Pretty time display; K2: Person details display; K3: Implementing the Product class; K4: Data class practice; K5: Days of the week enum; K6: Catching exceptions, Specify expectations; K7: Inventory management; K8: Implement map, Inline functions; K9: Understanding sequences; K10: Generic Response; K11: Mutable lazy delegate; K12: Using scope functions, HTML table DSL; K13: Adjust Kotlin for Java usage).
  - en: The track's exercise source, restated for the ClinicBook app (K1: Pretty time display; K2: Person details display; K3: Implementing the Product class; K4: Data class practice; K5: Days of the week enum; K6: Catching exceptions, Specify expectations; K7: Inventory management; K8: Implement map, Inline functions; K9: Understanding sequences; K10: Generic Response; K11: Mutable lazy delegate; K12: Using scope functions, HTML table DSL; K13: Adjust Kotlin for Java usage).

### Track F, J

- **Effective Kotlin: Best Practices (Marcin Moskała)** — Kt. Academy (sách) · `guideline`
  https://leanpub.com/effectivekotlin
  - vi: val không có nghĩa là bất biến (K1); loại bỏ platform type càng sớm càng tốt (K2); hợp đồng hashCode, bảng băm, phần tử bị sửa sau khi thêm vào set (K4);, 6, 8: require/check sớm, ưu tiên lỗi chuẩn, đóng tài nguyên bằng use (K6); collection read-only không phải bất biến, không ép kiểu xuống Mutable (K7);, 57: ưu tiên Sequence cho collection lớn xử lý nhiều bước, giảm số thao tác (K9). Track Mã sạch và kỷ luật làm nghề: property biểu diễn trạng thái, không phải hành vi; dùng hàm khi tốn kém, ném lỗi, có logic nghiệp vụ, không tất định, là chuyển đổi; gọi tham số bằng tên, nhất là Boolean (J2).
  - en: val does not mean immutable (K1); eliminate platform types as soon as possible (K2); the hashCode contract, hash tables, an element modified after being added to a set (K4);, 6, 8: require/check early, prefer standard errors, close resources with use (K6); read-only collections are not immutable, never down-cast to Mutable (K7);, 57: prefer Sequence for big collections with several processing steps, limit the number of operations (K9). Clean Code and Craft track: properties represent state, not behaviour; use a function when it is expensive, throws, holds business logic, is not deterministic or is a conversion; named arguments, especially for Booleans (J2).

### Track F, K

- **Functions** — Kotlin docs (JetBrains) · `stable`
  https://kotlinlang.org/docs/functions.html
  - vi: Tham số mặc định, đối số có tên, hàm một biểu thức; hàm override dùng giá trị mặc định của hàm gốc (K1). Track Lập trình hàm với Kotlin, mục Tail recursive functions (đọc 2026-11-24): với một số thuật toán vốn dùng vòng lặp, có thể dùng hàm đệ quy mà không sợ tràn stack; hàm có tailrec và đủ điều kiện thì trình biên dịch bỏ đệ quy, để lại một vòng lặp; chỉ gắn khi hàm gọi chính nó như thao tác cuối cùng; không dùng được khi còn mã sau lời gọi, trong try/catch/finally, hay khi hàm là open (chương "Bất biến, dữ liệu dùng chung và đệ quy").
  - en: Default parameters, named arguments, single-expression functions; overrides use the base defaults (K1). Functional Programming in Kotlin track, section Tail recursive functions (read 2026-11-24): for some algorithms that would normally use loops, a recursive function can be used without the risk of stack overflow; with tailrec and the formal conditions met, the compiler removes the recursion and leaves a loop; tailrec applies only when the function calls itself as its final operation; not when there is more code after the call, within try/catch/finally, or when the function is open (chapter "Immutability, data sharing and recursion").
- **Sealed classes and interfaces** — Kotlin docs (JetBrains) · `stable`
  https://kotlinlang.org/docs/sealed-classes.html
  - vi: Kiểu con trực tiếp biết lúc biên dịch, cùng package và module; when kiểm phủ đủ, không cần else; ngoại lệ multiplatform (K5). Track Lập trình hàm với Kotlin: sealed là sum type, when phủ đủ báo mọi chỗ chưa xử lý kiểu con mới (chương "Kiểu dữ liệu đại số").
  - en: Direct subtypes known at compile time, same package and module; when is checked exhaustively with no else; the multiplatform exception (K5). Functional Programming in Kotlin track: sealed as a sum type, an exhaustive when flags every place missing a new subtype (chapter "Algebraic data types").
- **Exceptions** — Kotlin docs (JetBrains) · `stable`
  https://kotlinlang.org/docs/exceptions.html
  - vi: Mọi ngoại lệ là unchecked; require/check/error và loại ngoại lệ; try-catch là biểu thức, catch khớp đầu tiên theo kiểu; finally luôn chạy, không đổi kết quả; use; kiểu Nothing; đừng tạo ngoại lệ bằng object (K6). Track Lập trình hàm với Kotlin: ngoại lệ là cách thứ nhất trong bốn cách báo lỗi (chương "Lỗi là giá trị").
  - en: All exceptions are unchecked; require/check/error and the exception types; try-catch is an expression, the first catch matching by type wins; finally always runs and does not change the result; use; the Nothing type; do not create exceptions with object (K6). Functional Programming in Kotlin track: exceptions are the first of four ways to report errors (chapter "Errors as values").
- **runCatching** — Kotlin API reference (JetBrains) · `stable`
  https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/run-catching.html
  - vi: runCatching bắt MỌI Throwable ném ra từ khối và gói thành Result thất bại (K6). Track Lập trình hàm với Kotlin: vì vậy runCatching gói luôn cả bug (chương "Lỗi là giá trị").
  - en: runCatching catches ANY Throwable thrown from the block and wraps it as a failed Result (K6). Functional Programming in Kotlin track: which is why runCatching wraps bugs too (chapter "Errors as values").

### Track G

- **Guide to app architecture** — Android Developers · `stable`
  https://developer.android.com/topic/architecture
  - vi: Component có thể bị hủy bất cứ lúc nào nên không giữ dữ liệu trong đó; tách mối quan tâm; UI dẫn từ model dữ liệu; SSOT; tối thiểu hai tầng UI và data, domain là tùy chọn (G1).
  - en: Components can be destroyed at any time, so do not keep data in them; separation of concerns; drive UI from data models; SSOT; at least a UI and a data layer, the domain layer is optional (G1).
- **Handle configuration changes** — Android Developers · `stable`
  https://developer.android.com/guide/topics/resources/runtime-changes
  - vi: Khi đổi cấu hình, hệ thống gọi onDestroy, hủy Activity và tạo instance mới bằng onCreate (G1).
  - en: On a configuration change, the system calls onDestroy, destroys the Activity and creates a new instance with onCreate (G1).
- **ViewModel overview** — Android Developers · `stable`
  https://developer.android.com/topic/libraries/architecture/viewmodel
  - vi: ViewModel giữ state và thao tác qua thay đổi cấu hình như xoay màn hình; sống tới khi ViewModelStoreOwner mất (Activity finish) (G1).
  - en: ViewModel keeps state and operations across configuration changes such as rotation; it lives until its ViewModelStoreOwner goes away (the Activity finishes) (G1).
- **Fundamentals of testing Android apps** — Android Developers · `stable`
  https://developer.android.com/training/testing/fundamentals
  - vi: Test local chạy trên máy phát triển, nhỏ và nhanh; test instrumented chạy trên thiết bị thật hay giả lập (G1).
  - en: Local tests run on the development machine, small and fast; instrumented tests run on a physical or emulated device (G1).
- **UI events** — Android Developers · `stable`
  https://developer.android.com/topic/architecture/ui-layer/events
  - vi: Sự kiện từ ViewModel luôn phải thành cập nhật UI state; UI báo lại khi đã xử lý thông báo; Channel và stream khác không bảo đảm giao khi ViewModel sống lâu hơn UI (G3).
  - en: ViewModel events must always result in a UI state update; the UI reports back once a message is consumed; Channels and other streams do not guarantee delivery when the ViewModel outlives the UI (G3).
- **State holders and UI state** — Android Developers · `stable`
  https://developer.android.com/topic/architecture/ui-layer/stateholders
  - vi: ViewModel giữ state và thao tác qua việc Activity bị tạo lại; khi process bị giết, SavedStateHandle giữ dữ liệu tối thiểu (G3).
  - en: A ViewModel keeps state and operations across Activity recreation; on process death, SavedStateHandle keeps the minimum data (G3).
- **StateFlow (kotlinx.coroutines 1.11.0 API)** — JetBrains · `stable`
  https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.flow/-state-flow/
  - vi: StateFlow luôn có giá trị, phát lại một giá trị mới nhất cho subscriber mới (G3).
  - en: A StateFlow always has a value and replays the most recent one to new subscribers (G3).
- **SharedFlow (kotlinx.coroutines 1.11.0 API)** — JetBrains · `stable`
  https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.flow/-shared-flow/
  - vi: Khi vắng subscriber chỉ giá trị replay được giữ; MutableSharedFlow() không replay, không buffer, emit trả về ngay nếu không có subscriber (G3).
  - en: With no subscribers only replay values are kept; MutableSharedFlow() has no replay or buffer, and emit returns immediately if there are no subscribers (G3).
- **Build an offline-first app** — Android Developers · `stable`
  https://developer.android.com/topic/architecture/data-layer/offline-first
  - vi: Nguồn cục bộ là nguồn sự thật chuẩn và là nơi duy nhất tầng trên đọc; ghi cập nhật vào nguồn cục bộ trước; đọc qua Flow, ghi qua suspend; ba chiến lược ghi: chỉ online, hàng đợi, ghi lười với WorkManager (G4).
  - en: The local data source is the canonical source of truth and the only one higher layers read; write updates to it first; reads via Flow, writes via suspend; three write strategies: online-only, queued, lazy with WorkManager (G4).
- **Dependency injection in Android** — Android Developers · `stable`
  https://developer.android.com/training/dependency-injection
  - vi: DI giúp dùng lại mã, dễ refactor, dễ test; Hilt cho phụ thuộc kiểm lúc biên dịch (G6).
  - en: DI helps code reuse, refactoring and testing; Hilt gives compile-time checked dependencies (G6).
- **Manual dependency injection** — Android Developers · `stable`
  https://developer.android.com/training/dependency-injection/manual
  - vi: Container dùng chung (AppContainer) đặt trong lớp Application, không phải singleton kiểu object; singleton làm test khó vì mọi test dùng chung instance (G6).
  - en: A shared container (AppContainer) held by the Application class, not an object singleton; singletons make testing harder because all tests share the instance (G6).
- **Dependency injection with Hilt** — Android Developers · `stable`
  https://developer.android.com/training/dependency-injection/hilt-android
  - vi: Component theo lớp Android và vòng đời; binding mặc định không scope; binding có scope tạo một lần mỗi instance component; binding mặc định của từng component; @ApplicationContext và @ActivityContext (G6).
  - en: Components per Android class and their lifetimes; bindings are unscoped by default; a scoped binding is created once per component instance; default bindings per component; @ApplicationContext and @ActivityContext (G6).
- **Testing strategies** — Android Developers · `stable`
  https://developer.android.com/training/testing/fundamentals/strategies
  - vi: Tháp kiểm thử: nhiều test nhỏ nhanh và tin cậy, ít test lớn có độ trung thực cao; lỗi bắt sớm bằng unit test rẻ hơn nhiều (G10).
  - en: The testing pyramid: many small fast reliable tests, few big high-fidelity tests; bugs caught early by unit tests are far cheaper (G10).
- **Use test doubles in Android** — Android Developers · `stable`
  https://developer.android.com/training/testing/fundamentals/test-doubles
  - vi: Fake (cài đặt chạy được, chỉ hợp cho test) được ưu tiên; mock có kỳ vọng về tương tác; stub, dummy, spy, shadow (G10).
  - en: Fakes (working implementations fit only for tests) are preferred; mocks carry expectations about interactions; stubs, dummies, spies, shadows (G10).
- **Clean Android Architecture (Alexandru Dumbravan)** — Packt (sách) · `guideline`
  https://www.oreilly.com/library/view/clean-android-architecture/9781803234588/
  - vi: Ch1: app cũ dồn mạng, parse JSON và UI vào Activity với AsyncTask, rò rỉ context, khó test và khó bảo trì khi app lớn (G1). Ch8: MVVM, View phụ thuộc ViewModel, ViewModel phụ thuộc Model, quan sát được. Ch9: MVI, dữ liệu bất biến gộp thành một state, intent đổi state qua luồng dữ liệu phản ứng, xây trên ViewModel (G7).
  - en: Ch1: old apps packed networking, JSON parsing and UI into Activities with AsyncTask, leaking context, hard to test and to maintain as the app grows (G1). Ch8: MVVM, the View depends on the ViewModel, the ViewModel on the Model, through observables. Ch9: MVI, immutable data combined into one state, intents change state through a reactive flow, built on top of ViewModels (G7).
- **UI layer** — Android Developers · `stable`
  https://developer.android.com/topic/architecture/ui-layer
  - vi: UDF: ViewModel giữ và lộ state cho UI; UI báo sự kiện cho ViewModel; ViewModel xử lý và cập nhật state; state mới quay về UI (G2).
  - en: UDF: the ViewModel holds and exposes state to the UI; the UI notifies the ViewModel of events; the ViewModel handles them and updates state; the new state flows back to the UI (G2).
- **Data layer** — Android Developers · `stable`
  https://developer.android.com/topic/architecture/data-layer
  - vi: Repository là lối vào duy nhất của data layer; mỗi repository định nghĩa một nguồn sự thật; dữ liệu lộ ra phải bất biến (G2).
  - en: Repositories are the only entry point to the data layer; each repository defines a single source of truth; exposed data must be immutable (G2).
- **Domain layer** — Android Developers · `stable`
  https://developer.android.com/topic/architecture/domain-layer
  - vi: Domain là tầng tùy chọn giữa UI và data; use case thường phụ thuộc repository (G2).
  - en: The domain layer is optional, between UI and data; use cases usually depend on repositories (G2).
- **Guide to Android app modularization** — Android Developers · `stable`
  https://developer.android.com/topic/modularization
  - vi: Module cho phép kiểm soát chặt phần lộ ra: đánh dấu internal hay private mọi thứ trừ giao diện công khai (G2, G9).
  - en: Modules give strict visibility control: mark everything but the public interface internal or private (G2).
- **Common modularization patterns** — Android Developers · `stable`
  https://developer.android.com/topic/modularization/patterns
  - vi: Hai module không thể gọi thẳng lẫn nhau vì phụ thuộc vòng; module cao và module cài đặt cùng phụ thuộc module trừu tượng (G2). Feature phụ thuộc data; app là điểm vào, giữ navigation graph và làm trung gian; truyền id chứ không truyền object; lộ ít nhất có thể, ưu tiên implementation hơn api (G9).
  - en: Two modules cannot talk to each other directly because of cyclic dependencies; high-level and implementation modules both depend on an abstraction module (G2). Features depend on data; the app module is the entry point, owns the navigation graph and mediates; pass ids, not objects; expose as little as possible, prefer implementation over api (G9).
- **Visibility modifiers** — Kotlin docs (JetBrains) · `stable`
  https://kotlinlang.org/docs/visibility-modifiers.html
  - vi: internal: thấy được trong cùng module; module là tập file Kotlin biên dịch cùng nhau, ví dụ một Gradle source set (G2).
  - en: internal: visible within the same module; a module is a set of Kotlin files compiled together, such as a Gradle source set (G2).
- **Clean Architecture for Android (Eran Boudjnah)** — BPB (sách) · `guideline`
  https://bpbonline.com/products/clean-architecture-for-android
  - vi: Ch1–2: nguyên lý Clean Architecture và các tầng domain, presentation, UI, data (G1); Dependency Rule: mũi tên hướng vào domain, đảo phụ thuộc bằng interface repository đặt cạnh use case (G2). Ch6: failure (dự đoán được, phục hồi được, xử lý như giá trị bằng sealed class) và exception (bất ngờ, ghi log và theo dõi) (G8). Ch7: thêm tính năng theo tầng, repository stub, commit nhỏ; Ch8: di trú dần MVP/MVVM, test trước khi đổi (G11).
  - en: Ch1–2: Clean Architecture principles and the domain, presentation, UI and data layers (G1); the Dependency Rule: arrows point inward to the domain, inverted with repository interfaces defined next to the use cases (G2). Ch6: failures (expected, recoverable, handled as values with sealed classes) versus exceptions (unexpected, logged and monitored) (G8). Ch7: building a feature layer by layer, stub repositories, small commits; Ch8: gradual migration from MVP/MVVM, tests before changes (G11).

### Track H

- **Data and file storage overview** — Android Developers · `stable`
  https://developer.android.com/training/data-storage
  - vi: Bốn lựa chọn: lưu riêng của app, lưu chung (media, tài liệu), preferences, database (Room). Bảng so sánh: cách truy cập, quyền, app khác có đọc được không, có bị xóa khi gỡ app không. Bốn câu hỏi khi chọn: dung lượng, độ tin cậy, loại dữ liệu, có riêng tư không. Không viết cứng đường dẫn (H1).
  - en: Four options: app-specific storage, shared storage (media, documents), preferences, databases (Room). A comparison table: access method, permissions, whether other apps can access it, whether it is removed on uninstall. Four questions when choosing: space, reliability, kind of data, privacy. Do not hardcode paths (H1).
- **Access app-specific files** — Android Developers · `stable`
  https://developer.android.com/training/data-storage/app-specific
  - vi: filesDir và cacheDir không cần quyền; từ Android 10 các thư mục nội bộ được mã hóa; file riêng của app bị xóa khi gỡ app. Khi máy thiếu dung lượng, hệ thống có thể xóa file cache; phải kiểm file còn trước khi đọc. Bộ nhớ ngoài của app không phải lúc nào cũng truy cập được (H1, H2).
  - en: filesDir and cacheDir need no permissions; from Android 10 the internal locations are encrypted; app-specific files are removed on uninstall. When the device is low on storage, the system may delete cache files; check a cache file exists before reading it. App-specific external storage is not always accessible (H1, H2).
- **DataStore** — Android Developers · `stable`
  https://developer.android.com/topic/libraries/architecture/datastore
  - vi: Lưu cặp khóa–giá trị hay đối tượng có kiểu, bất đồng bộ, nhất quán, theo giao dịch, bằng coroutine và Flow. Nên chuyển từ SharedPreferences sang DataStore. DataStore hợp với dữ liệu nhỏ, không hỗ trợ cập nhật từng phần hay ràng buộc tham chiếu; cần những thứ đó thì dùng Room. Không tạo hai instance cho cùng một file trong một tiến trình. Nhiều tiến trình từ bản 1.1.0. Bản trong hướng dẫn: 1.3.0 (H1, H3).
  - en: Stores key–value pairs or typed objects asynchronously, consistently and transactionally, using coroutines and Flow. Consider migrating from SharedPreferences to DataStore. DataStore suits small datasets and does not support partial updates or referential integrity; use Room when you need those. Never create two instances for the same file in one process. Multi-process since 1.1.0. Version in the guide: 1.3.0 (H1, H3).
- **SharedPreferences.Editor (reference)** — Android Developers · `stable`
  https://developer.android.com/reference/android/content/SharedPreferences.Editor
  - vi: commit() ghi đồng bộ và trả về true nếu ghi xuống bộ nhớ bền thành công. apply() đổi bản trong bộ nhớ ngay, ghi đĩa bất đồng bộ, không báo lỗi. Các lần apply() đang chờ có thể chặn main thread lúc chuyển trạng thái vòng đời, một nguồn ANR hay gặp (H3).
  - en: commit() writes synchronously and returns true if the values were written to persistent storage. apply() changes the in-memory copy at once, writes to disk asynchronously and reports no failure. Pending apply() calls can block the main thread during lifecycle transitions, a common source of ANRs (H3).
- **SharedPreferencesImpl.java (AOSP, nhánh main)** — Android Open Source Project · `impl`
  https://android.googlesource.com/platform/frameworks/base/+/refs/heads/main/core/java/android/app/SharedPreferencesImpl.java
  - vi: Nạp cả file XML vào một map trong bộ nhớ ở luồng nền (loadFromDisk); hàm get chờ tới khi nạp xong (awaitLoadedLocked). Mỗi lần ghi, writeToFile ghi lại toàn bộ map rồi sync; có file .bak để khôi phục khi ghi hỏng (H1, H3).
  - en: Loads the whole XML file into an in-memory map on a background thread (loadFromDisk); getters wait until loading finishes (awaitLoadedLocked). Each write, writeToFile writes the whole map then syncs; a .bak file allows recovery from a failed write (H1, H3).
- **ANRs** — Android Developers · `stable`
  https://developer.android.com/topic/performance/vitals/anr
  - vi: ANR xảy ra khi main thread bị chặn quá lâu; với sự kiện nhập (chạm, phím), ngưỡng là không phản hồi trong 5 giây. Thao tác đọc ghi đĩa trên main thread là một nguyên nhân hay gặp (H3).
  - en: An ANR happens when the main thread is blocked too long; for input events (touches, keys) the threshold is no response within 5 seconds. Disk I/O on the main thread is a common cause (H3).
- **SharedPreferencesMigration (reference)** — Android Developers · `stable`
  https://developer.android.com/reference/androidx/datastore/migrations/SharedPreferencesMigration
  - vi: Chuyển khóa từ SharedPreferences sang DataStore (boolean, float, int, long, string, string set). Khóa đã có trong DataStore thì không chuyển lại. SharedPreferences rỗng sau khi chuyển thì migration cố xóa nó. Không đọc DataStore bên trong migration, kẻo deadlock (H3).
  - en: Moves keys from SharedPreferences to DataStore (boolean, float, int, long, string, string set). A key already in DataStore is not migrated again. If the SharedPreferences is empty afterwards, the migration tries to delete it. Do not read DataStore inside a migration, or it deadlocks (H3).
- **AtomicFile (androidx.core.util)** — Android Developers · `stable`
  https://developer.android.com/reference/androidx/core/util/AtomicFile
  - vi: Ghi vào file "<tên>.new", sync xuống đĩa rồi đổi tên đè lên file gốc. startWrite trả stream (không tự đóng); finishWrite đóng, sync và chốt; failWrite đóng và xóa file mới. Không khóa file: phải tự loại trừ nhiều luồng hay tiến trình cùng ghi (H2).
  - en: Writes to a "<name>.new" file, syncs it to disk, then renames it over the original. startWrite returns a stream (do not close it yourself); finishWrite closes, syncs and commits; failWrite closes and deletes the new file. No file locking: you must keep several threads or processes from writing at once (H2).
- **rename(2), Linux manual page** — man7.org · `impl`
  https://man7.org/linux/man-pages/man2/rename.2.html
  - vi: Nếu tên đích đã có, nó được thay thế một cách nguyên tử: không có lúc nào tên đích không tồn tại (H2).
  - en: If the new path already exists, it is replaced atomically: there is no point at which the new path is missing (H2).
- **Save data in a local database using Room** — Android Developers · `stable`
  https://developer.android.com/training/data-storage/room
  - vi: Ba thành phần: lớp database, entity, DAO. Room kiểm câu SQL lúc biên dịch, giảm mã lặp, có đường migration. Nên dùng Room thay cho API SQLite trực tiếp (H1, H4).
  - en: Three components: the database class, entities, DAOs. Room verifies SQL at compile time, reduces boilerplate and provides migration paths. Use Room rather than the SQLite APIs directly (H1, H4).
- **Write asynchronous DAO queries** — Android Developers · `stable`
  https://developer.android.com/training/data-storage/room/async-queries
  - vi: Room không cho truy cập database trên main thread. Ba loại truy vấn: ghi một lần, đọc một lần (suspend), đọc quan sát (Flow) chạy lại khi bảng được tham chiếu đổi, kể cả khi dòng đổi không nằm trong kết quả; dùng distinctUntilChanged để UI chỉ nhận khi kết quả đổi. Room 3.0 bắt buộc suspend cho truy vấn một lần (H4).
  - en: Room does not allow database access on the main thread. Three kinds of query: one-shot write, one-shot read (suspend), observable read (Flow) that reruns when a referenced table changes, even if the changed row is not in the result; use distinctUntilChanged so the UI only hears about real changes. Room 3.0 requires suspend for one-shot queries (H4).
- **Accessing data using Room DAOs** — Android Developers · `stable`
  https://developer.android.com/training/data-storage/room/accessing-data
  - vi: DAO là interface hay abstract class gắn @Dao; Room sinh mã lúc biên dịch. @Insert trả rowId, @Update và @Delete khớp theo khóa chính, @Upsert chèn hoặc cập nhật. @Query được kiểm lúc biên dịch: câu sai là lỗi biên dịch (H4).
  - en: A DAO is an interface or abstract class annotated @Dao; Room generates the code at compile time. @Insert returns the rowId, @Update and @Delete match by primary key, @Upsert inserts or updates. @Query is checked at compile time: a wrong query is a compile error (H4).
- **Define relationships between objects (Room)** — Android Developers · `stable`
  https://developer.android.com/training/data-storage/room/relationships
  - vi: Room cấm tham chiếu đối tượng giữa các entity. Hai cách: lớp trung gian với @Embedded và @Relation, hoặc truy vấn trả về multimap (Map<A, List<B>>); nếu không có lý do cụ thể, nên dùng multimap. Multimap để SQL làm nhiều việc hơn; lớp trung gian để mã app làm nhiều việc hơn. @Relation cần Room chạy hai truy vấn, nên thêm @Transaction để cả thao tác là nguyên tử. Nhiều–nhiều dùng bảng nối và Junction (H5).
  - en: Room forbids object references between entities. Two approaches: an intermediate class with @Embedded and @Relation, or a query returning a multimap (Map<A, List<B>>); without a specific reason, the multimap is recommended. The multimap makes SQL do more work; the intermediate class makes app code do more. @Relation needs Room to run two queries, so add @Transaction to make the whole operation atomic. Many-to-many uses a junction table and Junction (H5).
- **Transaction (androidx.room reference)** — Android Developers · `stable`
  https://developer.android.com/reference/androidx/room/Transaction
  - vi: Đánh dấu một hàm DAO là giao dịch. Với SELECT: kết quả lớn có cái nhìn nhất quán; POJO có @Relation được truy vấn bằng các câu riêng nên cần giao dịch để nhất quán. Với hàm không trừu tượng gọi nhiều hàm DAO: chạy cả hàm trong một giao dịch. @Insert, @Update, @Delete vốn đã chạy trong giao dịch. Room chạy tối đa một giao dịch mỗi lúc, các giao dịch khác xếp hàng (H5).
  - en: Marks a DAO method as a transaction. For SELECT: a large result gets a consistent view; a POJO with @Relation is fetched in separate queries, so a transaction keeps it consistent. On a non-abstract method calling several DAO methods: the whole method runs in one transaction. @Insert, @Update and @Delete already run in a transaction. Room performs at most one transaction at a time; others queue (H5).
- **Migrate your Room database** — Android Developers · `stable`
  https://developer.android.com/training/data-storage/room/migrating-db-versions
  - vi: Migration tự động (AutoMigration) cho thay đổi đơn giản, cần schema đã xuất; đổi tên hay xóa bảng, cột thì cần spec (@RenameColumn, @DeleteColumn, @RenameTable, @DeleteTable). Migration tay: lớp Migration(start, end), đăng ký bằng addMigrations; có cả hai cho cùng phiên bản thì Room dùng bản tay. Thiếu đường thì IllegalStateException. fallbackToDestructiveMigration xóa vĩnh viễn mọi dữ liệu trong bảng. Kiểm thử bằng MigrationTestHelper với schema đã xuất (H6).
  - en: Automated migrations (AutoMigration) cover simple changes and need exported schemas; renaming or deleting tables or columns needs a spec (@RenameColumn, @DeleteColumn, @RenameTable, @DeleteTable). Manual migrations: a Migration(start, end) class registered with addMigrations; if both exist for the same versions, Room uses the manual one. A missing path throws IllegalStateException. fallbackToDestructiveMigration permanently deletes all data in the tables. Test with MigrationTestHelper and exported schemas (H6).
- **Build an offline-first app** — Android Developers · `stable`
  https://developer.android.com/topic/architecture/data-layer/offline-first
  - vi: Nguồn cục bộ là nguồn sự thật; UI quan sát nó. Ba chiến lược ghi: online-only (ghi mạng trước, lỗi thì ném ra; ví dụ chuyển tiền), queued (đưa vào hàng chờ, rút khi có mạng với backoff lũy thừa; cho dữ liệu không quan trọng), lazy (ghi máy trước rồi xếp lệnh ghi mạng; lựa chọn đúng khi dữ liệu quan trọng, có thể sinh xung đột). Hàng chờ có thể giữ trong Room và rút bằng WorkManager. Xung đột: "last write wins" là cách phổ biến (H7).
  - en: The local source is the source of truth; the UI observes it. Three write strategies: online-only (network first, throw on failure; e.g. a bank transfer), queued (put in a queue, drain when online with exponential backoff; for non-critical data), lazy (write locally first, then queue the network write; the right choice for critical data, may cause conflicts). The queue can live in Room and be drained by WorkManager. Conflicts: "last write wins" is a common approach (H7).
- **Persistent work (WorkManager)** — Android Developers · `stable`
  https://developer.android.com/develop/background-work/background-tasks/persistent
  - vi: WorkManager cho công việc phải chạy chắc chắn kể cả khi người dùng rời màn hình, app thoát hay máy khởi động lại; công việc được lưu trong một database SQLite nội bộ. Coroutine dừng ngay khi app đóng. Có ràng buộc (mạng, pin), công việc duy nhất có thể thay thế, và chính sách thử lại với backoff lũy thừa (H7).
  - en: WorkManager is for work that must run reliably even if the user leaves the screen, the app exits or the device restarts; scheduled work is stored in an internal SQLite database. Coroutines stop as soon as the app closes. It offers constraints (network, battery), unique replaceable work, and retry policies with exponential backoff (H7).
- **Access media files from shared storage** — Android Developers · `stable`
  https://developer.android.com/training/data-storage/shared/media
  - vi: Bộ sưu tập Images, Video, Audio, Downloads (Downloads từ Android 10). Từ Android 10 không cần quyền để thêm và sửa media của chính app; Android 9 trở xuống cần READ/WRITE_EXTERNAL_STORAGE. IS_PENDING ẩn mục đang ghi; RELATIVE_PATH gợi ý thư mục. Android 10 tạm thoát scoped storage bằng requestLegacyExternalStorage. Từ Android 11 dùng được File trên shared storage; đọc ghi ngẫu nhiên có thể chậm gấp đôi. READ_MEDIA_IMAGES/VIDEO bị chính sách Play giới hạn; nên dùng photo picker (H8).
  - en: Images, Video, Audio and Downloads collections (Downloads from Android 10). From Android 10 no permission is needed to add and modify the app's own media; Android 9 and lower need READ/WRITE_EXTERNAL_STORAGE. IS_PENDING hides an item being written; RELATIVE_PATH hints the folder. Android 10 can temporarily opt out of scoped storage with requestLegacyExternalStorage. From Android 11, File works on shared storage; random reads and writes can be up to twice as slow. READ_MEDIA_IMAGES/VIDEO are limited by Play policy; prefer the photo picker (H8).
- **Photo picker** — Android Developers · `stable`
  https://developer.android.com/training/data-storage/shared/photopicker
  - vi: PickVisualMedia và PickMultipleVisualMedia (androidx.activity 1.7.0+). Có sẵn từ Android 11 qua cập nhật hệ thống; backport qua Google Play services cho Android 4.4 tới 10; không có thì dùng ACTION_OPEN_DOCUMENT. takePersistableUriPermission để giữ quyền qua lần khởi động lại (H8).
  - en: PickVisualMedia and PickMultipleVisualMedia (androidx.activity 1.7.0+). Built in from Android 11 through system updates; backported through Google Play services for Android 4.4 to 10; otherwise falls back to ACTION_OPEN_DOCUMENT. takePersistableUriPermission keeps access across restarts (H8).
- **Back up user data with Auto Backup** — Android Developers · `stable`
  https://developer.android.com/identity/data/autobackup
  - vi: Từ Android 6.0. Tối đa 25 MB mỗi app, lưu trong thư mục riêng trên Google Drive, mã hóa đầu cuối từ Android 9. Mặc định sao lưu SharedPreferences, filesDir, getDatabasePath, getExternalFilesDir; luôn loại cacheDir, codeCacheDir, noBackupFilesDir. Chạy khi máy rảnh, có Wi-Fi, cách lần trước ít nhất 24 giờ; khôi phục sau khi cài APK và trước khi người dùng mở app. Android 12+ dùng dataExtractionRules với cloud-backup và device-transfer; exclude thắng include. File chứa định danh riêng của thiết bị như token FCM thường bị loại; token đăng nhập nên dùng Block Store (H9).
  - en: From Android 6.0. Up to 25 MB per app, stored in a private Google Drive folder, end-to-end encrypted from Android 9. By default backs up SharedPreferences, filesDir, getDatabasePath, getExternalFilesDir; always excludes cacheDir, codeCacheDir, noBackupFilesDir. Runs when the device is idle, on Wi-Fi, at least 24 hours since the last one; restores after the APK installs and before the user can open the app. Android 12+ uses dataExtractionRules with cloud-backup and device-transfer; exclude wins over include. Files with device-specific identifiers such as the FCM token are typically excluded; login tokens should use Block Store (H9).

### Track I

- **System Design Interview: An Insider's Guide, vol. 1 (Alex Xu)** — ByteByteGo (sách) · `guideline`
  https://bytebytego.com/
  - vi: ước lượng nhanh là quá trình, không cần chính xác; làm tròn số, viết rõ giả định và đơn vị. khung bốn bước của Alex Xu (hiểu đề và khoanh phạm vi, đề xuất thiết kế tổng quát, đi sâu, tổng kết); đừng trả lời ngay, hãy hỏi để làm rõ yêu cầu và ghi lại giả định; thiết kế quá mức là dấu hiệu xấu (I1). gửi tin qua HTTP là đủ; nhận tin cần polling (tốn vì phần lớn trả lời rỗng), long polling (giữ yêu cầu tới khi có tin hay hết hạn; ba nhược điểm phía server) hay WebSocket (bắt đầu là HTTP rồi nâng cấp, hai chiều, sống lâu) (I4). nên cache khi đọc nhiều ít sửa; chính sách hết hạn; nhất quán; loại bỏ LRU, LFU, FIFO (I6). xung đột đồng bộ: bản được xử lý trước thắng, bản sau nhận xung đột; hiện cả bản trên máy lẫn bản mới nhất từ server để người dùng gộp hay chọn (I8). thu thập device token khi cài hay đăng ký, lưu trong bảng thiết bị, một người nhiều thiết bị; thông báo được trễ, đảo thứ tự nhưng không được mất (lưu và thử lại phía server); không bảo đảm đúng một lần, khử trùng theo id sự kiện; tôn trọng opt-out (I9). bảng tin nhắn với message_id duy nhất và tăng theo thời gian, không dựa vào created_at; id cục bộ trong một cuộc trò chuyện là đủ; mỗi thiết bị giữ cur_max_message_id để đồng bộ tin mới; người nhận offline thì gửi thông báo đẩy; heartbeat cho trạng thái online (I13). chia video thành khúc để upload nhanh và tiếp tục được khi lỗi; pre-signed URL. upload thường cho tệp nhỏ, upload tiếp tục được cho tệp lớn và mạng hay đứt (lấy URL, gửi và theo dõi, đứt thì tiếp); chia khối, chỉ gửi khối đổi (delta sync), nén (I10).
  - en: back-of-the-envelope estimation is about the process, not precision; round numbers, write down assumptions and units. Alex Xu's four-step framework (understand the problem and scope, propose a high-level design, deep dive, wrap up); do not answer at once, ask to clarify requirements and write down assumptions; over-engineering is a red flag (I1). HTTP is fine for sending; receiving needs polling (costly, most answers empty), long polling (held until a message or timeout; three server-side drawbacks) or WebSocket (starts as HTTP, upgraded, two-way, long-lived) (I4). cache data read often and changed rarely; expiration; consistency; LRU, LFU, FIFO eviction (I6). sync conflicts: the version processed first wins, the later one gets a conflict; show both the local copy and the latest server version so the user merges or picks (I8). device tokens collected at install or sign-up, stored in a device table, one user with many devices; notifications may be delayed or reordered but never lost (persist and retry on the server); no exactly-once delivery, dedupe by event ID; respect opt-outs (I9). a message table keyed by a unique, time-sortable message_id rather than created_at; IDs local to one conversation are enough; each device keeps cur_max_message_id to sync new messages; offline recipients get a push notification; heartbeats for presence (I13). split videos into chunks for faster uploads that can resume after failure; pre-signed URLs. simple upload for small files, resumable upload for large files and flaky networks (get the URL, upload and monitor, resume when interrupted); splitting into blocks, sending only changed blocks (delta sync), compression (I10).
- **Mobile System Design (Tjeerd in 't Veen), bản early release** — Resourceful Engineering (sách) · `guideline`
  https://www.mobilesystemdesign.com/
  - vi: đừng mở IDE ngay, hãy tìm yêu cầu phụ trước; thiết kế thường chỉ có trường hợp đẹp, hãy xin bản với nội dung xấu nhất; bàn sớm về lỗi và ưu tiên lỗi không chặn màn hình; thống nhất với backend về phiên, token, timeout, mã lỗi (client tự dịch theo mã) và thông báo đẩy theo ngôn ngữ của máy (I1).
  - en: do not open the IDE yet, uncover secondary requirements first; designs usually show only the best case, ask for a worst-case content version; discuss errors early and prefer errors that do not block the screen; align with the backend on sessions, tokens, timeouts, error codes (the client localises by code) and push notifications in the device's language (I1).
- **Processes and app lifecycle** — Android Developers · `stable`
  https://developer.android.com/guide/components/activities/process-lifecycle
  - vi: Bốn bậc theo thứ tự quan trọng: foreground, visible, service, cached; hệ thống giết cached trước, foreground là phương án cuối. Service chạy khoảng 30 phút trở lên có thể bị hạ xuống cached. Process được bind hay dùng ContentProvider quan trọng ít nhất bằng process dùng nó. Lỗi BroadcastReceiver mở luồng rồi trả về. Từ Android 13, process cached có thể không được cấp thời gian chạy (I2).
  - en: Four levels in order of importance: foreground, visible, service, cached; the system kills cached first, foreground as a last resort. A Service running for about 30 minutes or more may be demoted to cached. A process that is bound or whose ContentProvider is used is at least as important as its client. The BroadcastReceiver-starts-a-thread bug. From Android 13 a cached process may get little or no execution time (I2).
- **The activity lifecycle** — Android Developers · `stable`
  https://developer.android.com/guide/components/activities/activity-lifecycle
  - vi: Hệ thống không bao giờ giết trực tiếp một Activity để lấy bộ nhớ; nó giết process. Bảng liên hệ trạng thái process với trạng thái Activity; khi người dùng quay lại, Activity được tạo lại từ dữ liệu đã lưu (I2).
  - en: The system never kills an activity directly to free memory; it kills the process. A table relating process state to activity state; when the user returns, the activity is recreated from saved data (I2).
- **Overview of memory management** — Android Developers · `stable`
  https://developer.android.com/topic/performance/memory-overview
  - vi: Vùng nhớ app đã sửa luôn nằm trong RAM, chỉ phần không sửa như mã mới bị bỏ ra; mỗi app có giới hạn heap (getMemoryClass); process cached có thể bị giết bất cứ lúc nào (I2).
  - en: Memory an app has modified stays in RAM, only unmodified parts such as code can be paged out; each app has a heap limit (getMemoryClass); cached processes can be killed at any time (I2).
- **Save UI states** — Android Developers · `stable`
  https://developer.android.com/topic/libraries/architecture/saving-states
  - vi: So sánh ViewModel, saved state và lưu trữ bền: cái nào sống qua đổi cấu hình, qua process bị hệ thống giết, qua việc người dùng đóng hẳn màn hình. Saved state chỉ cho dữ liệu nhỏ, lưu lúc Activity bị stop, bản sao giữ ngoài process (I2).
  - en: Compares ViewModel, saved state and durable storage: which survives configuration changes, system-initiated process death, and the user fully closing the screen. Saved state is for small data, saved when the activity stops, with a copy kept outside the process (I2).
- **Get a result from an activity** — Android Developers · `stable`
  https://developer.android.com/training/basics/intents/result
  - vi: Với tác vụ tốn bộ nhớ như camera, process và Activity gần như chắc chắn bị hủy; callback phải đăng ký vô điều kiện mỗi lần Activity được tạo; trạng thái cần để xử lý kết quả phải lưu riêng (I2).
  - en: With memory-hungry work such as the camera, the process and activity are almost certainly destroyed; the callback must be registered unconditionally every time the activity is created; state needed to handle the result must be saved separately (I2).
- **ComponentCallbacks2 (reference)** — Android Developers · `version`
  https://developer.android.com/reference/android/content/ComponentCallbacks2
  - vi: Từ API 34 app chỉ nhận TRIM_MEMORY_UI_HIDDEN và TRIM_MEMORY_BACKGROUND; các mức khác và onLowMemory() không còn được gọi, deprecated ở API 35; so sánh bằng >= (I2).
  - en: Since API 34 apps only receive TRIM_MEMORY_UI_HIDDEN and TRIM_MEMORY_BACKGROUND; other levels and onLowMemory() are no longer called and are deprecated in API 35; compare with >= (I2).
- **Low memory killer daemon** — Android Open Source Project · `version`
  https://source.android.com/docs/core/perf/lmkd
  - vi: lmkd theo dõi áp lực bộ nhớ và giết process ít cần thiết nhất; driver LMK trong kernel bị gỡ từ kernel 4.12, Android 9+ dùng lmkd ở userspace, Android 10+ dùng PSI; ở mức medium mặc định chỉ giết process có oom_adj từ 800 (I2).
  - en: lmkd monitors memory pressure and kills the least essential processes; the in-kernel LMK driver was removed as of kernel 4.12, Android 9+ uses userspace lmkd, Android 10+ uses PSI; at medium level the default only kills processes with oom_adj 800 or more (I2).
- **Android Debug Bridge (adb)** — Android Developers · `stable`
  https://developer.android.com/tools/adb
  - vi: Lệnh am kill <package> giết mọi process của gói mà an toàn để giết, không ảnh hưởng trải nghiệm người dùng (I2).
  - en: The am kill <package> command kills all processes of a package that are safe to kill without affecting the user experience (I2).
- **Operating System Concepts, 10th edition (Silberschatz, Galvin, Gagne)** — Wiley (sách) · `guideline`
  https://www.os-book.com/OS10/
  - vi: Mục 3.3.2.1: Android xếp process theo năm bậc (foreground, visible, service, background, empty) và giết theo thứ tự quan trọng tăng dần. Mục 9.5.3: hệ điều hành mobile thường không swap vì flash nhỏ, chịu ít lần ghi và chậm; Android giết process khi thiếu bộ nhớ (I2). race condition, critical section, mutex. ví dụ hai mutex lấy ngược thứ tự, bốn điều kiện cần của deadlock, đồ thị chờ, chống vòng chờ bằng thứ tự khóa toàn cục; phần lớn hệ điều hành để app tự phòng deadlock (I3).
  - en: Section 3.3.2.1: Android ranks processes in five levels (foreground, visible, service, background, empty) and kills in order of increasing importance. Section 9.5.3: mobile systems usually do not swap because flash is small, tolerates few writes and is slow; Android kills processes when memory runs low (I2). race conditions, critical sections, mutexes. two mutexes taken in opposite orders, the four necessary deadlock conditions, the wait-for graph, preventing circular wait with a global lock order; most operating systems leave deadlock prevention to applications (I3).
- **Optimize network access** — Android Developers · `version`
  https://developer.android.com/develop/connectivity/network-ops/network-access-optimization
  - vi: Máy trạng thái radio (ví dụ radio 3G): năng lượng cao, thấp (giảm khoảng 50%), chờ; sau mỗi lần truyền thêm 5 giây năng lượng cao và 12 giây năng lượng thấp; thức dậy từ chờ có thể hơn 2 giây; gom việc truyền, tải trước, kiểm kết nối, dùng lại kết nối (I4).
  - en: The radio state machine (a 3G example): full power, low power (around 50% less), standby; after each transfer 5 more seconds at full and 12 at low power; waking from standby can take over 2 seconds; bundle transfers, prefetch, check connectivity, reuse connections (I4).
- **Optimize for Doze and App Standby** — Android Developers · `stable`
  https://developer.android.com/training/monitoring-device-state/doze-standby
  - vi: Doze tạm dừng mạng, bỏ qua wake lock, hoãn alarm, JobScheduler và WorkManager tới cửa sổ bảo trì; App Standby hoãn mạng nền; khuyên dùng FCM thay vì tự giữ kết nối vì FCM dùng chung một kết nối; Google Play hạn chế xin miễn trừ (I4).
  - en: Doze suspends network access, ignores wake locks, defers alarms, JobScheduler and WorkManager to maintenance windows; App Standby defers background network; recommends FCM over your own connection since FCM shares one; Google Play restricts exemption requests (I4).
- **Firebase Cloud Messaging** — Firebase · `stable`
  https://firebase.google.com/docs/cloud-messaging
  - vi: Môi trường tin cậy (server, Cloud Functions) gửi message; app nhận qua dịch vụ vận chuyển của nền tảng; payload tối đa 4096 byte (I4).
  - en: A trusted environment (a server, Cloud Functions) sends messages; the app receives through the platform transport; payload up to 4096 bytes (I4).
- **Set Android message priority (FCM)** — Firebase · `version`
  https://firebase.google.com/docs/cloud-messaging/android/message-priority
  - vi: Ưu tiên thường có thể chờ tới khi máy ra khỏi Doze; ưu tiên cao cố giao ngay, đánh thức máy, nên dẫn tới thông báo; không dẫn tới thông báo thì có thể bị hạ ưu tiên; onMessageReceived chỉ có vài giây (I4).
  - en: Normal priority may wait until the device leaves Doze; high priority tries immediate delivery, wakes the device, and should lead to a notification, otherwise it may be deprioritized; onMessageReceived only gets a few seconds (I4).
- **Collapsible and non-collapsible messages (FCM)** — Firebase · `stable`
  https://firebase.google.com/docs/cloud-messaging/customize-messages/collapsible-message-types
  - vi: Không bảo đảm thứ tự; message gộp được thay cái cũ chưa giao, tối đa bốn khóa gộp mỗi máy; trên Android quá 100 message không gộp được đang chờ thì bỏ hết và app phải đồng bộ lại (I4).
  - en: No ordering guarantee; a collapsible message replaces an undelivered older one, at most four collapse keys per device; on Android past 100 pending non-collapsible messages all are discarded and the app must resync (I4).
- **Using server-sent events (MDN)** — MDN Web Docs · `stable`
  https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events
  - vi: Kết nối một chiều server → client, kiểu nội dung text/event-stream, tự nối lại khi đứt; trường retry đặt thời gian chờ nối lại (I4).
  - en: A one-way server → client connection, text/event-stream content type, reconnects automatically; the retry field sets the reconnection delay (I4).
- **The WebSocket API (MDN)** — MDN Web Docs · `stable`
  https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API
  - vi: Phiên giao tiếp hai chiều, gửi nhận không cần polling; API WebSocket không hỗ trợ backpressure (I4).
  - en: A two-way session, sending and receiving without polling; the WebSocket API does not support backpressure (I4).
- **Designing Data-Intensive Applications, 2nd edition (Kleppmann, Riccomini)** — O'Reilly (sách) · `guideline`
  https://dataintensive.net/
  - vi: cơn bão thử lại và lỗi metastable; tăng và ngẫu nhiên hóa khoảng thử lại (exponential backoff), circuit breaker. gửi request không có response thì không biết request mất, server chết hay response mất; timeout. thao tác idempotent, làm idempotent bằng siêu dữ liệu (I5). sync engine, mỗi thiết bị là một leader, ghi đồng thời gây xung đột; LWW bỏ âm thầm các ghi khác; gộp tay và anh em (siblings); gộp tự động, map khóa-giá trị gộp từng khóa độc lập; CRDT, OT. lost update, ghi có điều kiện (compare-and-set), khóa lạc quan theo số phiên bản. LWW theo giờ của client làm mất ghi khi đồng hồ lệch (I8). mã cũ và mới cùng tồn tại (app phía client phụ thuộc người dùng có cập nhật hay không); tương thích ngược (mã mới đọc dữ liệu cũ) và xuôi (mã cũ đọc dữ liệu mới, phải bỏ qua phần thêm); API REST: thêm tham số tùy chọn, thêm trường vào response thường giữ tương thích; phá vỡ thì giữ nhiều phiên bản API song song (I12).
  - en: retry storms and metastable failure; increase and randomise retry intervals (exponential backoff), circuit breakers. a request without a response cannot tell a lost request, a dead server or a lost response apart; timeouts. idempotent operations, made idempotent with metadata (I5). sync engines, every device a leader, concurrent writes conflict; LWW silently discards the others; manual resolution and siblings; automatic merging, key-value maps merged per key independently; CRDTs, OT. lost updates, conditional writes (compare-and-set), optimistic locking with a version number. LWW on client clocks drops writes when clocks are skewed (I8). old and new code coexist (client apps depend on users installing updates); backward compatibility (new code reads old data) and forward compatibility (old code reads new data, ignoring additions); REST APIs: adding optional parameters and response fields usually keeps compatibility; breaking changes mean maintaining several API versions side by side (I12).
- **RFC 9110: HTTP Semantics** — IETF · `stable`
  https://www.rfc-editor.org/rfc/rfc9110.html
  - vi: Mục 9.2.2: PUT, DELETE và các phương thức an toàn là idempotent; client không nên tự thử lại request không idempotent khi không biết kết quả (I5). 8.8: validator, ETag mạnh và yếu (W/); 13.1.2: If-None-Match; 15.4.5: 304 không có nội dung (I6). 13.1.1: If-Match chống ghi đè khi nhiều client cùng sửa (lost update), so sánh mạnh, điều kiện sai thì không thực hiện và trả 412; 13.1.2: If-None-Match: * khi tạo mới; 15.5.13: 412 Precondition Failed (I8).
  - en: Section 9.2.2: PUT, DELETE and the safe methods are idempotent; a client should not automatically retry a non-idempotent request when the outcome is unknown (I5). 8.8: validators, strong and weak (W/) ETags; 13.1.2: If-None-Match; 15.4.5: a 304 has no content (I6). 13.1.1: If-Match prevents overwrites when several clients edit in parallel (lost update), strong comparison, a false condition means the method is not performed and 412 is returned; 13.1.2: If-None-Match: * when creating; 15.5.13: 412 Precondition Failed (I8).
- **The Idempotency-Key HTTP Header Field (draft-ietf-httpapi-idempotency-key-header-09)** — IETF HTTPAPI (bản nháp) · `version`
  https://datatracker.ietf.org/doc/draft-ietf-httpapi-idempotency-key-header/
  - vi: Bản nháp 09 (21/11/2026): client gửi key duy nhất (nên dùng UUID) để POST, PATCH chịu được lỗi; không dùng lại key cho nội dung khác; key đã xong thì trả response nhất quán; đang xử lý thì 409; nội dung khác thì 422 (I5).
  - en: Draft 09 (21 Nov 2026): the client sends a unique key (UUID recommended) to make POST and PATCH fault-tolerant; never reuse a key for a different payload; completed key: a consistent response; still processing: 409; different payload: 422 (I5).
- **Define work requests (WorkManager)** — Android Developers · `stable`
  https://developer.android.com/develop/background-work/background-tasks/persistent/getting-started/define-work
  - vi: Result.retry() và chính sách backoff LINEAR hay EXPONENTIAL; mặc định EXPONENTIAL 30 giây, tối thiểu 10 giây (MIN_BACKOFF_MILLIS); ví dụ EXPONENTIAL khoảng 20, 40, 80 giây; thời điểm lệch vài giây (I5).
  - en: Result.retry() and the LINEAR or EXPONENTIAL backoff policy; the default is EXPONENTIAL with 30 seconds, at least 10 seconds (MIN_BACKOFF_MILLIS); an EXPONENTIAL example of about 20, 40, 80 seconds; times drift by a few seconds (I5).
- **RFC 9111: HTTP Caching** — IETF · `stable`
  https://www.rfc-editor.org/rfc/rfc9111.html
  - vi: 4.2: tươi khi tuổi chưa vượt thời gian sống (s-maxage, max-age, Expires); 4.2.2: heuristic, thường 10% thời gian từ Last-Modified; 4.2.4: dùng bản cũ khi mất mạng trừ khi có must-revalidate, no-cache; 4.3: kiểm tra lại bằng If-None-Match, 304 cập nhật và dùng lại bản lưu; 5.2.2: max-age, no-cache, no-store, must-revalidate, private (I6).
  - en: 4.2: fresh while age is below the freshness lifetime (s-maxage, max-age, Expires); 4.2.2: heuristics, typically 10% of the time since Last-Modified; 4.2.4: stale may be served when disconnected unless must-revalidate or no-cache; 4.3: validation with If-None-Match, a 304 updates and reuses the stored copy; 5.2.2: max-age, no-cache, no-store, must-revalidate, private (I6).
- **Acing the System Design Interview (Zhiyong Tan)** — Manning (sách) · `guideline`
  https://www.manning.com/books/acing-the-system-design-interview
  - vi: Design a text messaging app: người nhận gửi xác nhận đã nhận và đã xem về người gửi; tin được ghi ở message service trước, giao không được thì bỏ vì máy lấy lại sau; phía nhận kiểm tra trùng rồi mới hiện (I13). (Design Flickr), 12.7.1: trang theo số thứ tự bị lệch khi có ảnh mới thêm vào đầu (trang 2 trả 10–19 thay vì 11–20); cách đánh phiên bản phân trang (page_version) chỉ đúng khi thêm hay xóa ở đầu danh sách; cách tốt hơn là gửi mục đầu hay mục cuối hiện có (previous_last, previous_first) (I7).
  - en: Design a text messaging app: the recipient sends delivery confirmations and read receipts back to the sender; messages are recorded in the message service first, undeliverable sends are dropped because the device fetches later; the receiver checks for duplicates before showing (I13). (Design Flickr), 12.7.1: numbered pages shift when a new thumbnail is added at the front (page 2 returns 10–19 instead of 11–20); versioning the pagination (page_version) only works for additions or deletions at the start of the list; a better technique is to pass the current last or first item (previous_last, previous_first) (I7).
- **AIP-158: Pagination** — Google API Improvement Proposals · `stable`
  https://google.aip.dev/158
  - vi: page_size, page_token, next_page_token; token phải mờ (opaque), an toàn cho URL, người dùng không đọc ra được, vì đọc được thì người ta sẽ dựa vào và server không đổi được nữa; next_page_token rỗng là cách duy nhất báo hết danh sách; trang có thể ít hơn page_size, kể cả rỗng, mà chưa hết; đổi tham số khác giữa các trang thì nên báo INVALID_ARGUMENT; token có thể hết hạn, thường khoảng ba ngày; thêm phân trang sau là thay đổi không tương thích (I7).
  - en: page_size, page_token, next_page_token; tokens must be opaque, URL-safe and not user-parseable, because users who can parse them will rely on them and the server can no longer change them; an empty next_page_token is the only end-of-collection signal; a page may hold fewer than page_size results, even zero, before the end; changing other parameters between pages should return INVALID_ARGUMENT; tokens may expire, about three days as a rule of thumb; adding pagination later is a breaking change (I7).
- **Paging library overview; Load and display paged data** — Android Developers · `stable`
  https://developer.android.com/topic/libraries/architecture/paging/v3-overview
  - vi: Paging 3.5.3: cache dữ liệu đã tải trong bộ nhớ, gộp request trùng, làm mới và thử lại; PagingSource (tầng repository), Pager và PagingData (ViewModel), collectAsLazyPagingItems (UI). LoadResult.Page(data, prevKey, nextKey), null là hết theo chiều đó; LoadResult.Error; getRefreshKey cho lần làm mới; nguồn dữ liệu phải bất biến, dữ liệu đổi thì invalidate() và Pager tạo PagingSource mới (I7).
  - en: Paging 3.5.3: in-memory caching of loaded data, request deduplication, refresh and retry; PagingSource (repository layer), Pager and PagingData (ViewModel), collectAsLazyPagingItems (UI). LoadResult.Page(data, prevKey, nextKey), null meaning no more in that direction; LoadResult.Error; getRefreshKey for refreshes; the data source is expected to be immutable, so on changes call invalidate() and the Pager creates a new PagingSource (I7).
- **Page from network and database** — Android Developers · `stable`
  https://developer.android.com/topic/libraries/architecture/paging/v3-network-db
  - vi: RemoteMediator tải từ mạng khi hết dữ liệu đã cache và ghi vào database; database là nguồn sự thật, UI chỉ hiện dữ liệu đã nằm trong database; LoadType REFRESH, APPEND, PREPEND; bảng remote_keys giữ nextKey khi khóa của server không gắn với từng mục; initialize() chọn SKIP_INITIAL_REFRESH hay LAUNCH_INITIAL_REFRESH (I7).
  - en: RemoteMediator loads from the network when cached data runs out and writes it to the database; the database is the source of truth and the UI shows only data already in it; LoadType REFRESH, APPEND, PREPEND; a remote_keys table keeps nextKey when server keys are not tied to items; initialize() picks SKIP_INITIAL_REFRESH or LAUNCH_INITIAL_REFRESH (I7).
- **SubcomposeLayout.kt (androidx, commit 3fa4054, 2026-10-15)** — AOSP / androidx · `impl`
  https://github.com/androidx/androidx/blob/3fa4054361e62c157e2f140c655a409600f45db9/compose/ui/ui/src/commonMain/kotlin/androidx/compose/ui/layout/SubcomposeLayout.kt
  - vi: Trong subcompose(slotId, content): cùng một slot id được dùng hai lần thì requirePrecondition ném lỗi với thông điệp Key "…" was already used, nhắc LazyColumn/Row phải có key duy nhất cho mỗi mục (I7).
  - en: In subcompose(slotId, content): using the same slot id twice fails a requirePrecondition with the message Key "…" was already used, reminding LazyColumn/Row users to give each item a unique key (I7).
- **RFC 6585: Additional HTTP Status Codes** — IETF · `stable`
  https://www.rfc-editor.org/rfc/rfc6585.html
  - vi: 3: 428 Precondition Required, server đòi request phải có điều kiện, thường để tránh lost update (GET, sửa, PUT trong khi bên thứ ba đã sửa); 7.1: 428 là tùy chọn, client không dựa vào nó để chống lost update được (I8).
  - en: 3: 428 Precondition Required, the server requires the request to be conditional, typically to avoid the lost update problem (GET, modify, PUT while a third party changed it); 7.1: 428 is optional, so clients cannot rely on it to prevent lost updates (I8).
- **Best practices for FCM registration management** — Firebase · `stable`
  https://firebase.google.com/docs/cloud-messaging/manage-tokens
  - vi: Lưu ID đăng ký của từng thiết bị trên server kèm thời điểm, cập nhật mỗi lần app gửi lên; mặc định coi là cũ khi app không kết nối một tháng và message tới đó khó bao giờ tới; trên Android không hoạt động 270 ngày thì hết hạn; lỗi UNREGISTERED nghĩa là xóa ID (I9, chỉ nhắc).
  - en: Store each device registration ID on the server with a timestamp, updated on every upload; by default it is stale after a month without connecting and messages to it are unlikely to arrive; on Android it expires after 270 days inactive; an UNREGISTERED error means delete the ID (I9, mention only).
- **Notification runtime permission** — Android Developers · `stable`
  https://developer.android.com/develop/ui/views/notifications/notification-permission
  - vi: Từ Android 13 (API 33), thông báo không miễn trừ cần quyền chạy POST_NOTIFICATIONS; app mới cài thì thông báo tắt mặc định; hỏi vào lúc người dùng tự chọn (bấm chuông, đặt hàng) và giải thích lý do trước (I9).
  - en: From Android 13 (API 33), non-exempt notifications need the POST_NOTIFICATIONS runtime permission; for newly installed apps notifications are off by default; ask at a user-driven moment (tapping a bell, placing an order) and explain why first (I9).
- **Loading large bitmaps efficiently** — Android Developers · `stable`
  https://developer.android.com/topic/performance/graphics/load-bitmap
  - vi: inJustDecodeBounds = true chỉ đọc outWidth, outHeight, không cấp phát; inSampleSize làm tròn xuống lũy thừa của 2; ví dụ 2048×1536 với inSampleSize 4 thành 512×384, khoảng 0,75 MB thay vì 12 MB; calculateInSampleSize nhân đôi tới khi nửa kích thước chia cho nó còn lớn hơn kích thước cần; khuyên dùng thư viện ảnh (Glide; Coil, Picasso, Fresco) (I10).
  - en: inJustDecodeBounds = true only reads outWidth and outHeight without allocating; inSampleSize rounds down to a power of two; the example of 2048×1536 with inSampleSize 4 gives 512×384, about 0.75 MB instead of 12 MB; calculateInSampleSize doubles while half the size divided by it stays at or above the requested size; recommends an image library (Glide; Coil, Picasso, Fresco) (I10).
- **Bitmap.Config** — Android Developers · `stable`
  https://developer.android.com/reference/android/graphics/Bitmap.Config
  - vi: ARGB_8888: 4 byte mỗi điểm ảnh, nên dùng khi có thể; RGB_565: 2 byte, không có kênh alpha; RGBA_F16: 8 byte; HARDWARE (API 26): chỉ nằm trong bộ nhớ đồ họa, bất biến, hợp khi chỉ vẽ lên màn hình (I10).
  - en: ARGB_8888: 4 bytes per pixel, recommended whenever possible; RGB_565: 2 bytes, no alpha; RGBA_F16: 8 bytes; HARDWARE (API 26): stored only in graphics memory, immutable, best when only drawn to screen (I10).
- **User-initiated data transfer jobs** — Android Developers · `version`
  https://developer.android.com/develop/background-work/background-tasks/uidt
  - vi: Android 14 (API 34): job truyền dữ liệu lâu do người dùng khởi động, như tải tệp; quyền RUN_USER_INITIATED_JOBS; phải có thông báo; chạy được lâu khi điều kiện hệ thống cho phép; phải lên lịch khi app đang hiện; trước Android 14 dùng WorkManager với foreground service (I10).
  - en: Android 14 (API 34): long data transfers started by the user, such as downloading a file; the RUN_USER_INITIATED_JOBS permission; a notification is required; may run for an extended time as conditions allow; must be scheduled while the app is visible; before Android 14 use WorkManager with a foreground service (I10).
- **Resumable Uploads for HTTP (draft-ietf-httpbis-resumable-upload-16)** — IETF (Internet-Draft) · `version`
  https://datatracker.ietf.org/doc/draft-ietf-httpbis-resumable-upload/
  - vi: Bản nháp 16 (2026-11), chưa là RFC. Tạo tài nguyên upload (POST, server trả Location); sau khi đứt, HEAD lấy Upload-Offset; gửi tiếp bằng PATCH với Upload-Offset và Upload-Complete; offset không được giảm (I10).
  - en: Draft 16 (2026-11), not yet an RFC. Create an upload resource (POST, the server returns Location); after an interruption, HEAD gets Upload-Offset; continue with PATCH carrying Upload-Offset and Upload-Complete; the offset must not decrease (I10).
- **App startup time** — Android Developers · `stable`
  https://developer.android.com/topic/performance/vitals/launch-time
  - vi: Cold start tạo process, Application.onCreate, Activity, khung hình đầu; warm start dựng lại Activity, có thể dùng lại process; hot start rẻ nhất; luôn tối ưu theo giả định cold start. TTID: tới khung hình đầu, hệ thống tự đo (dòng Displayed trong Logcat); TTFD: tới khi dùng được, app tự báo bằng reportFullyDrawn hay ReportDrawnWhen trong Compose. Vấn đề hay gặp: khởi tạo nặng trong Application và Activity; cách sửa: khởi tạo lười, App Startup (I11).
  - en: A cold start creates the process, runs Application.onCreate, creates the Activity and draws the first frame; a warm start recreates the Activity and may reuse the process; a hot start is cheapest; always optimise assuming a cold start. TTID: to the first frame, measured by the system (the Displayed line in Logcat); TTFD: to fully usable, reported by the app with reportFullyDrawn or ReportDrawnWhen in Compose. Common problems: heavy initialisation in Application and Activity; fixes: lazy initialisation, App Startup (I11).
- **App startup analysis and optimization** — Android Developers · `stable`
  https://developer.android.com/topic/performance/appstartup/analysis-optimization
  - vi: Đo bằng Macrobenchmark (StartupTimingMetric) và trace trong Perfetto; xem mọi việc dài hơn 20 ms lúc khởi động; hỏi việc nào cần ngay, việc nào đợi sau khung hình đầu được; việc nền vẫn tranh CPU; StrictMode bắt I/O trên luồng chính; Baseline Profiles; App Startup (I11).
  - en: Measure with Macrobenchmark (StartupTimingMetric) and Perfetto traces; look at every operation longer than 20 ms during startup; ask which work is needed now and which can wait until after the first frame; background work still competes for CPU; StrictMode catches main-thread I/O; Baseline Profiles; App Startup (I11).
- **App Startup (Jetpack)** — Android Developers · `version`
  https://developer.android.com/topic/libraries/app-startup
  - vi: startup-runtime 1.2.0: các Initializer dùng chung một ContentProvider thay vì mỗi thư viện một cái (ContentProvider tốn khi khởi tạo, thứ tự không xác định); dependencies() định thứ tự; bỏ meta-data để khởi tạo lười bằng AppInitializer (I11).
  - en: startup-runtime 1.2.0: Initializers share one ContentProvider instead of one per library (providers are expensive and run in an undetermined order); dependencies() sets the order; remove the meta-data to initialise lazily with AppInitializer (I11).
- **Reduce your app size** — Android Developers · `stable`
  https://developer.android.com/topic/performance/reduce-apk-size
  - vi: Người dùng tránh tải app lớn, nhất là mạng chậm hay gói dữ liệu ít; kích thước còn ảnh hưởng thời gian tải, bộ nhớ, pin. App Bundle để Play tạo APK theo máy; minifyEnabled và shrinkResources (R8 bỏ mã thừa rồi bỏ tài nguyên thừa); giới hạn ngôn ngữ, mật độ; vector cho ảnh nhỏ; WebP (I11).
  - en: Users avoid large downloads, especially on slow networks or small data plans; size also affects load time, memory and power. App Bundles let Play build per-device APKs; minifyEnabled and shrinkResources (R8 removes unused code, then unused resources); limit locales and densities; vectors for small images; WebP (I11).
- **Release app updates with staged rollouts (Google Play)** — Google Play Console Help · `stable`
  https://support.google.com/googleplay/android-developer/answer/6346149
  - vi: Bản mới chỉ tới một phần trăm người dùng chọn ngẫu nhiên, tăng dần bằng tay; tạm dừng thì không thêm người nhận, nhưng người đã nhận vẫn giữ bản đó; có lỗi thì phát hành bản mới đã sửa (I12, chỉ nhắc).
  - en: A release reaches only a chosen percentage of randomly selected users, raised by hand; halting stops new users from getting it, but those who already got it keep it; on problems, roll out a new fixed release (I12, mention only).
- **Android vitals** — Android Developers · `stable`
  https://developer.android.com/topic/performance/vitals
  - vi: Chỉ số cốt lõi: tỉ lệ người dùng gặp crash, tỉ lệ người dùng gặp ANR; ngưỡng hành vi xấu chung 1,09% (crash) và 0,47% (ANR), theo từng mẫu điện thoại 8%; vượt ngưỡng thì Play có thể giảm hiển thị và cảnh báo trên trang app; tính trên 28 ngày (I12).
  - en: Core metrics: user-perceived crash rate and user-perceived ANR rate; overall bad-behaviour thresholds 1.09% (crash) and 0.47% (ANR), 8% per phone model; exceeding them may reduce Play visibility and add a store listing warning; computed over 28 days (I12).
- **In-app updates** — Android Developers · `stable`
  https://developer.android.com/guide/playcore/in-app-updates
  - vi: Flexible: tải và cài ở nền, người dùng vẫn dùng app; immediate: màn hình toàn phần bắt cập nhật và khởi động lại, hợp khi bản cập nhật quan trọng với chức năng chính (I12, chỉ nhắc).
  - en: Flexible: download and install in the background while the user keeps using the app; immediate: a full-screen flow requiring update and restart, for updates critical to core functionality (I12, mention only).
- **Customize the Json instance (kotlinx.serialization)** — Kotlin docs · `stable`
  https://kotlinlang.org/docs/serialization-json-configuration.html
  - vi: Mặc định, khóa lạ trong JSON gây lỗi khi giải mã (SerializationException); ignoreUnknownKeys = true thì bỏ qua; coerceInputValues, explicitNulls (I12).
  - en: By default, unknown keys in the JSON input cause an error during decoding (SerializationException); ignoreUnknownKeys = true ignores them; coerceInputValues, explicitNulls (I12).

### Track I, J, K

- **Code That Fits in Your Head (Mark Seemann)** — Addison-Wesley (sách) · `guideline`
  https://blog.ploeh.dk/code-that-fits-in-your-head/
  - vi: 10.1: tách tính năng khỏi mã hiện thực nó; triển khai mã chưa xong được nếu hành vi bị ẩn sau feature flag; tích hợp thường xuyên. 10.3: Semantic Versioning major.minor.patch, chỉ tăng major khi phá tương thích; báo trước, đánh dấu deprecated; cố tránh thay đổi phá vỡ (I12). Track Mã sạch và kỷ luật làm nghề: 3.2.1 trí nhớ ngắn hạn giữ khoảng bốn tới bảy mẩu thông tin, tác giả dùng 7 làm con số tượng trưng; 7.1 đặt ngưỡng để chặn mã mục dần; 7.1.2 cyclomatic complexity: bắt đầu từ 1, mỗi lệnh rẽ nhánh hay lặp cộng 1, cũng là số test tối thiểu; 7.1.3 luật 80/24, tác giả nói là tùy ý; 7.2.1 không quá bảy thứ trong một đoạn mã; 7.2.7 đếm biến cục bộ, tham số và field (J1); 8.1.4 tên hàm tốt hơn comment; 8.1.5 che tên (X out names) để xem kiểu còn nói gì; 8.1.6 command query separation, ưu tiên query; 8.1.7 thứ bậc giao tiếp: kiểu, tên, comment, test, commit message, tài liệu (J2); 12.1 hiểu trước, phương pháp khoa học, đơn giản hóa, giới hạn thời gian; 12.2.1 tái hiện lỗi thành test; 12.3 chia đôi, 12.3.1 git bisect với khoảng 130 commit (J7); 9.1.1 quy tắc 50/72; 9.1.3 commit nhỏ; 9.2.3–9.2.6 review, từ chối PR lớn, câu hỏi gốc, checklist của Cory House, quy tắc PR (J10). Track Lập trình hàm với Kotlin: 13.1.3 query phải tất định, không dựa vào số ngẫu nhiên, GUID, giờ trong ngày, ngày trong tháng, tệp hay database; hàm tất định không side effect là referentially transparent, tức hàm thuần; thay được lời gọi bằng kết quả; 8.2.2 WillAccept nhận now làm tham số, bộ điều khiển truyền DateTime.Now vào (chương "Hàm thuần và referential transparency"). A.12 ưu tiên hàm thuần, hàm thuần dễ ghép và dễ unit test; 13.1.3 (Listing 13.6) Post đọc hết dữ liệu (GUID, database, ngày giờ), gọi WillAccept thuần, chỉ ghi khi nó trả true, đẩy query không tất định và side effect ra rìa, tên gọi functional core, imperative shell là của Gary Bernhardt; càng nhiều hàm thuần càng ít cần log, chỉ log việc không thuần (chương "Functional core, imperative shell: lõi thuần, vỏ mỏng").
  - en: 10.1: separate the feature from the code that implements it; incomplete code can be deployed if its behaviour is hidden behind a feature flag; integrate often. 10.3: Semantic Versioning major.minor.patch, increment major only for breaking changes; warn in advance, mark deprecated; try to avoid breaking changes (I12). Clean Code and Craft track: 3.2.1 short-term memory holds about four to seven pieces of information, the author uses 7 as a symbolic number; 7.1 thresholds to curb code rot; 7.1.2 cyclomatic complexity: start at 1, add 1 per branching or looping instruction, also the minimum number of tests; 7.1.3 the 80/24 rule, which the author calls arbitrary; 7.2.1 no more than seven things in a piece of code; 7.2.7 count locals, parameters and fields (J1); 8.1.4 well-named methods over comments; 8.1.5 x out names to see what the types still say; 8.1.6 command query separation, favour queries; 8.1.7 hierarchy of communication: types, names, comments, tests, commit messages, documentation (J2); 12.1 understand first, scientific method, simplify, time-box; 12.2.1 reproduce defects as tests; 12.3 bisection, 12.3.1 git bisect across some 130 commits (J7); 9.1.1 the 50/72 rule; 9.1.3 small commits; 9.2.3–9.2.6 review, rejecting big PRs, the core question, Cory House's checklist, PR rules (J10). Functional Programming in Kotlin track: 13.1.3 queries must be deterministic, relying on no random numbers, GUIDs, time of day, day of month, files or databases; a deterministic method without side effects is referentially transparent, a pure function; a call can be replaced by its result; 8.2.2 WillAccept takes now as a parameter, and the controller passes DateTime.Now in (chapter "Pure functions and referential transparency"). A.12 prefer pure functions, which compose easily and are easy to unit test; 13.1.3 (Listing 13.6) Post reads all data first (GUID, database, date and time), calls the pure WillAccept, writes only when it returns true, pushing non-deterministic queries and side effects to the edge; the name functional core, imperative shell is Gary Bernhardt's; the more pure functions, the less logging you need, so log only impure actions (chapter "Functional core, imperative shell: a pure core, a thin shell").

### Track J

- **Clean Code: A Handbook of Agile Software Craftsmanship (Robert C. Martin, 2008)** — Prentice Hall (sách) · `guideline`
  https://www.informit.com/store/clean-code-a-handbook-of-agile-software-craftsmanship-9780132350884
  - vi: hàm nên nhỏ, và nhỏ hơn nữa; hiếm khi tới 20 dòng (tác giả thừa nhận không có nghiên cứu chứng minh, chỉ có kinh nghiệm); khối trong if, else, while nên dài một dòng; làm một việc; mọi câu lệnh ở cùng một mức trừu tượng; đọc từ trên xuống theo stepdown rule (J1). tên lộ ý định, tránh thông tin sai, phân biệt có nghĩa, mỗi khái niệm một từ, tên theo miền; side effect là lời nói dối, tham số cờ báo hàm làm hai việc, command query separation (ví dụ set trả Boolean); comment bù cho việc chưa diễn đạt được bằng mã (J2). Ví dụ Java, site viết lại bằng Kotlin.
  - en: functions should be small, then smaller than that; hardly ever 20 lines (the author admits no research shows this, only experience); blocks inside if, else, while should be one line; do one thing; every statement at one level of abstraction; read top-down by the stepdown rule (J1). intention-revealing names, avoid disinformation, meaningful distinctions, one word per concept, domain names; side effects are lies, flag arguments signal a function doing two things, command query separation (the Boolean-returning set example); comments compensate for failing to express ourselves in code (J2). Java examples, rewritten by the site in Kotlin.
- **Clean Architecture: A Craftsman's Guide to Software Structure and Design (Robert C. Martin, 2017)** — Prentice Hall (sách) · `guideline`
  https://www.informit.com/store/clean-architecture-a-craftsmans-guide-to-software-structure-9780134494166
  - vi: SOLID: SRP một module chịu trách nhiệm với đúng một actor (không phải "làm một việc"); OCP mở để mở rộng, đóng để sửa; LSP định nghĩa kiểu con của Barbara Liskov, ví dụ hình vuông và hình chữ nhật; ISP đừng phụ thuộc thứ không dùng; DIP chính sách không phụ thuộc chi tiết, tránh phụ thuộc thứ cụ thể hay đổi, nền tảng ổn định như String thì không cần tránh (J8). REP, CCP (SRP cho thành phần), CRP. ADP; SDP; ổn định là khó dời đi, không phải ít đổi; Fan-in, Fan-out, I = Fan-out/(Fan-in + Fan-out), ví dụ Cc có I = 1/4; mũi tên chỉ lên là vi phạm, sửa bằng DIP; SAP (J9).
  - en: SOLID: SRP a module is responsible to one, and only one, actor (not "does one thing"); OCP open for extension, closed for modification; LSP Barbara Liskov's subtype definition, the square and rectangle example; ISP do not depend on what you do not use; DIP policy does not depend on details, avoid volatile concretions, stable platform facilities such as String need not be avoided (J8). REP, CCP (SRP for components), CRP. ADP; SDP; stability means hard to move, not rarely changed; Fan-in, Fan-out, I = Fan-out/(Fan-in + Fan-out), the Cc example with I = 1/4; an upward arrow is a violation, fixed with DIP; SAP (J9).
- **The Clean Coder: A Code of Conduct for Professional Programmers (Robert C. Martin, 2011)** — Prentice Hall (sách) · `guideline`
  https://www.informit.com/store/clean-coder-a-code-of-conduct-for-professional-programmers-9780137081073
  - vi: nói không khi câu trả lời thật là không; "cố" là cam kết; không có chuyện cố. nói có là cam kết rõ ràng. hy vọng là thứ giết dự án. ước lượng khác cam kết; PERT (1957, dự án Polaris): O, N, P; μ = (O + 4N + P)/6, σ = (P − O)/6; chuỗi việc cộng μ, σ là căn tổng bình phương; Wideband Delphi; luật số lớn. tránh áp lực bằng quản lý cam kết; khi bị áp lực đừng hoảng, trao đổi, dựa vào kỷ luật, làm cặp (J11).
  - en: say no when the real answer is no; "try" is a commitment; there is no trying. saying yes is a clear commitment. hope is the project killer. estimates differ from commitments; PERT (1957, the Polaris project): O, N, P; μ = (O + 4N + P)/6, σ = (P − O)/6; for a sequence μ adds and σ is the root of the sum of squares; Wideband Delphi; the law of large numbers. avoid pressure by managing commitments; under pressure do not panic, communicate, rely on disciplines, pair (J11).
- **Clean Craftsmanship: Disciplines, Standards, and Ethics (Robert C. Martin, 2021)** — Addison-Wesley (sách) · `guideline`
  https://www.informit.com/store/clean-craftsmanship-disciplines-standards-and-ethics-9780136915713
  - vi: bản chất của TDD (bộ test đủ tin để triển khai, mã tách được, vòng phản hồi ngắn); ba luật TDD mà tác giả gọi là tùy ý; luật thứ tư là refactor, vòng đỏ → xanh → refactor; refactor liên tục, không lên lịch (J4). năm loại test double theo Meszaros (dummy, stub, spy, mock, fake); mock là spy biết kỳ vọng; spy và mock buộc test vào thuật toán; London (chắc chắn, mock ở mọi ranh giới) và Chicago (linh hoạt, test giá trị và thuộc tính), tác giả nghiêng về Chicago. test dễ vỡ là vấn đề thiết kế; tương ứng một-một giữa lớp và lớp test; Rule 12 tách cấu trúc test khỏi cấu trúc mã (J5). refactor là chuỗi thay đổi nhỏ giữ hành vi, test xanh sau mỗi thay đổi; nhỏ tới mức không phải gỡ lỗi (Rule 15: tránh debugger); Rename, Extract Method/Variable/Field; test nhanh, refactor liên tục, không để test đỏ quá vài phút, cấu trúc mới song song rồi chuyển dần, đặt tag để còn đường lui (J6).
  - en: the essence of TDD (a test suite trusted enough to deploy, decoupled code, a short feedback loop); the three laws of TDD, which the author calls arbitrary; the fourth law is refactoring, the red → green → refactor cycle; refactoring is continuous, never scheduled (J4). Meszaros's five test doubles (dummy, stub, spy, mock, fake); a mock is a spy that knows expectations; spies and mocks tie tests to the algorithm; London (certainty, mocks at every boundary) and Chicago (flexibility, value and property tests), the author leans Chicago. fragile tests are a design problem; one-to-one correspondence between classes and test classes; Rule 12 decouple test structure from code structure (J5). refactoring is a sequence of small behaviour-preserving changes, tests green after each; small enough not to debug (Rule 15: avoid debuggers); Rename, Extract Method/Variable/Field; quick tests, refactor continuously, never leave tests red more than minutes, build the new structure alongside and migrate, tag to leave yourself an out (J6).
- **git-bisect: Use binary search to find the commit that introduced a bug** — Git documentation · `stable`
  https://git-scm.com/docs/git-bisect
  - vi: Lệnh dùng tìm kiếm nhị phân: chỉ ra một commit xấu và một commit tốt, git chọn commit ở giữa và hỏi tốt hay xấu cho tới khi tìm ra commit gây lỗi. git bisect run: lệnh trả 0 là tốt, 1 tới 127 trừ 125 là xấu, 125 là bỏ qua commit không thử được (J7).
  - en: The command uses binary search: name a bad commit and a good one, git picks a commit in between and asks good or bad until it finds the commit that introduced the bug. git bisect run: the command exits 0 for good, 1 to 127 except 125 for bad, 125 to skip a commit that cannot be tested (J7).
- **Inline value classes** — Kotlin docs (JetBrains) · `stable`
  https://kotlinlang.org/docs/inline-classes.html
  - vi: Value class có đúng một property khởi tạo trong constructor chính; được có khối init (ví dụ require) và constructor phụ; là kiểu mới thật sự, khác typealias vốn gán lẫn được với kiểu gốc; lúc chạy thường biểu diễn bằng giá trị bên trong (J3).
  - en: A value class has exactly one property initialised in the primary constructor; it may have an init block (for example require) and secondary constructors; it is a truly new type, unlike a typealias, which is assignment-compatible with its underlying type; at runtime it is usually represented by the underlying value (J3).
- **Coding conventions** — Kotlin docs (JetBrains) · `stable`
  https://kotlinlang.org/docs/coding-conventions.html
  - vi: Choose good names: tên lớp là danh từ, tên hàm là động từ; tên hàm cho biết sửa tại chỗ (sort) hay trả bản mới (sorted); tránh từ vô nghĩa như Manager, Wrapper (J2).
  - en: Choose good names: class names are nouns, function names verbs; a function name tells whether it mutates in place (sort) or returns a new copy (sorted); avoid meaningless words such as Manager and Wrapper (J2).

### Track K

- **Functional Programming in Kotlin by Tutorials (Massimo Carli, Kodeco, 2022)** — Kodeco (sách) · `guideline`
  https://www.kodeco.com/books/functional-programming-in-kotlin-by-tutorials
  - vi: hàm thuần có hai điều kiện: cùng đầu vào luôn cho cùng đầu ra, và không làm thế giới bên ngoài đổi sau mỗi lần gọi; ví dụ twice và twiceAndLog (println là side effect), randomInc (Random đổi trạng thái); referential transparency: thay biểu thức bằng kết quả ở mọi chỗ dùng mà chương trình không đổi; mô hình thay thế (substitution model); ngoại lệ cũng là side effect (chương "Hàm thuần và referential transparency"). bất biến khác hằng (val với MutableUser); data class toàn val chưa đủ nếu có thuộc tính kiểu sửa được (Date); List là read-only; lợi ích: đơn giản, nhất quán (khóa Map), tránh tạo trùng, an toàn luồng; đệ quy thay vòng lặp; recursiveFactorial khai triển; tailrec, mã dịch ngược thành while(true). immutable, functional, persistent (chương "Bất biến, dữ liệu dùng chung và đệ quy"). compose và after, tính kết hợp; curry, mọi hàm nhiều tham số thành hàm một tham số; pipe; partial application gần với dependency injection; đặt tham số ít đổi lên trước, quá nhiều tham số là thói quen xấu; side effect phá ghép hàm, map(f).map(g) và map(f compose g) (chương "Ghép hàm: composition, currying, partial application"). Pair là tích Descartes, số giá trị nhân; Either là tổng; Unit là 1, Nothing là 0; Struct = 2 × 3 × 256; callback (Data, Result?, Error?) không an toàn kiểu, viết lại thành Result × (Info + Error); Optional là A + 1 (chương "Kiểu dữ liệu đại số"). Ngoại lệ là side effect; đưa side effect vào kiểu trả về; dừng sớm (fail fast) hay gom lỗi; Result<T> của Kotlin, phía lỗi là Throwable, có map nhưng không có flatMap; ViewModel dùng fold để chọn trạng thái màn hình (chương "Lỗi là giá trị"). Functor giữ cấu trúc (luật đơn vị và luật ghép); hàm dạng (A) -> M<B>; flatten có kiểu M<M<A>> -> M<A>; flatMap dựng từ map và flatten (chương "map và flatMap: functor và monad qua ví dụ"). Monoid và semigroup; hai chiến lược dừng sớm hay gom lỗi; Semigroup gộp lỗi kiểm dữ liệu (chương "Validate gom lỗi: applicative và monoid"). State là giá trị đổi được; kiểu State mô tả việc chuyển trạng thái (chương "State thuần: reducer và event", chỉ nhắc). Side effect là thay đổi thế giới; kiểu IO (chương "Functional core, imperative shell: lõi thuần, vỏ mỏng", chỉ nhắc). Ví dụ của sách, site viết lại theo app Hẹn Khám.
  - en: a pure function meets two conditions: the same input always gives the same output, and the universe does not change after each call; the twice and twiceAndLog examples (println is a side effect), randomInc (Random changes state); referential transparency: replacing an expression with its result wherever it is used without changing the program; the substitution model; exceptions are side effects too (chapter "Pure functions and referential transparency"). immutable versus constant (val with MutableUser); an all-val data class is not enough with a mutable-typed property (Date); List is read-only; benefits: simplicity, consistency (Map keys), avoiding duplicates, thread safety; recursion instead of loops; the recursiveFactorial expansion; tailrec, decompiled into while(true). immutable, functional, persistent (chapter "Immutability, data sharing and recursion"). compose and after, associativity; curry, every multi-parameter function as one-parameter functions; pipe; partial application close to dependency injection; put rarely-changing parameters first, too many parameters is bad practice; side effects break composition, map(f).map(g) versus map(f compose g) (chapter "Composing functions: composition, currying, partial application"). Pair as the Cartesian product, counts multiply; Either as the sum; Unit is 1, Nothing is 0; Struct = 2 × 3 × 256; the callback (Data, Result?, Error?) is not type-safe, rewritten as Result × (Info + Error); Optional is A + 1 (chapter "Algebraic data types"). Exceptions are side effects; make the side effect part of the result type; fail fast versus collecting errors; Kotlin Result<T>, whose failure is a Throwable and which has map but no flatMap; a ViewModel uses fold to pick the UI state (chapter "Errors as values"). A functor preserves structure (identity and composition laws); functions of the form (A) -> M<B>; flatten has type M<M<A>> -> M<A>; flatMap built from map and flatten (chapter "map and flatMap: functors and monads by example"). Monoids and semigroups; failing fast versus collecting errors; a Semigroup combining validation errors (chapter "Validation that collects errors: applicatives and monoids"). State is a value that can change; the State type describes state transitions (chapter "Pure state: reducers and events", mentioned only). A side effect is a change to the world; the IO type (chapter "Functional core, imperative shell: a pure core, a thin shell", mentioned only). The book's examples are rewritten by the site for the ClinicBook app.
- **Functional Programming in Kotlin (Marco Vermeulen, Rúnar Bjarnason, Paul Chiusano, Manning, 2021)** — Manning (sách) · `guideline`
  https://www.manning.com/books/functional-programming-in-kotlin
  - vi: ví dụ quán cà phê: buyCoffee gọi cc.charge là side effect, khó test, không dùng lại được; trả về Charge như một giá trị thì test không cần mock; đẩy hiệu ứng ra lớp ngoài, lõi thuần; định nghĩa referential transparency và hàm thuần; mô hình thay thế, suy luận như giải phương trình; ví dụ String.reversed (thay được) và StringBuilder.append (không thay được); sửa dữ liệu cục bộ mà không ai bên ngoài thấy thì vẫn chấp nhận được (chương "Hàm thuần và referential transparency"). Ném ngoại lệ phá referential transparency (nghĩa phụ thuộc khối try bao quanh) và không an toàn kiểu (kiểu hàm không nói gì về lỗi); giá trị đặc biệt (sentinel) để lỗi lặng lẽ đi tiếp (chương "Lỗi là giá trị"). Functor tổng quát hóa map của Option, Gen, Parser; monad là flatMap cùng unit; luật kết hợp và luật đơn vị trái, phải (chương "map và flatMap: functor và monad qua ví dụ"). map2 trên Either chỉ báo một lỗi; monoid; applicative: cấu trúc cố định, bước độc lập, còn monad thì kết quả trước quyết định bước sau; kiểu Validation giữ nhiều lỗi cho form web (chương "Validate gom lỗi: applicative và monoid"). partial1, curry, uncurry, compose như câu đố kiểu, closure (chương "Ghép hàm: composition, currying, partial application"); vị trí đuôi, tailrec, không gắn thì không bỏ tail call, chỉ cảnh báo khi không có lời gọi đuôi. 3.3 data sharing, Cons(x, xs), tail, persistent, pessimistic copying; 3.3.1 append chép a1, init phải chép; foldRight không stack-safe, foldLeft tailrec (chương "Bất biến, dữ liệu dùng chung và đệ quy").
  - en: the coffee shop example: buyCoffee calling cc.charge is a side effect, hard to test, not reusable; returning a Charge as a value makes tests need no mocks; push effects to the outer layer, a pure core; the definitions of referential transparency and a pure function; the substitution model, reasoning like solving an equation; String.reversed (substitutable) versus StringBuilder.append (not); mutating local data nobody outside can observe is still acceptable (chapter "Pure functions and referential transparency"). partial1, curry, uncurry, compose as type puzzles, closures (chapter "Composing functions: composition, currying, partial application"); tail position, tailrec, no tail call elimination without it, only a warning when no tail call exists. 3.3 data sharing, Cons(x, xs), tail, persistence, pessimistic copying; 3.3.1 append copies a1, init must copy; foldRight is not stack-safe, foldLeft is tailrec (chapter "Immutability, data sharing and recursion"). Throwing an exception breaks referential transparency (the meaning depends on the enclosing try) and is not type-safe (the function type says nothing about failure); sentinel values let errors propagate silently (chapter "Errors as values"). The functor generalises the map of Option, Gen, Parser; a monad is flatMap together with unit; the associative law and the left and right identity laws (chapter "map and flatMap: functors and monads by example"). map2 on Either reports only one error; monoids; applicatives: a fixed structure of independent steps, while with a monad the previous result decides the next step; a Validation type holding several errors for a web form (chapter "Validation that collects errors: applicatives and monoids").
- **From Objects to Functions (Uberto Barbini, Pragmatic Bookshelf, 2023)** — Pragmatic Bookshelf (sách) · `guideline`
  https://pragprog.com/titles/uboop/from-objects-to-functions/
  - vi: trả null khi lỗi đủ dùng nếu lý do hiển nhiên; trả kèm chuỗi lỗi (Pair) vẫn buộc nơi gọi kiểm null; giữ ngoại lệ cho tình huống không thể phục hồi; kết quả là một kiểu sealed thành công hoặc thất bại (chương "Lỗi là giá trị"). Event sourcing: lưu thay đổi kèm lý do, bốn lợi ích và cái giá; gộp event; máy trạng thái bằng sealed class; command mang id tạo sẵn; nhiều event, ít command (chương "State thuần: reducer và event"). Ví dụ của sách là ứng dụng phía server; site chỉ lấy ý về lỗi và viết lại theo app Hẹn Khám.
  - en: returning null on error is enough when the reason is obvious; returning an error string alongside (a Pair) still makes callers check null; keep exceptions for unrecoverable situations; a result as a sealed success-or-failure type (chapter "Errors as values"). Event sourcing: storing changes with their reason, four benefits and the costs; folding events; state machines with sealed classes; commands carrying a pre-minted id; many events, few commands (chapter "Pure state: reducers and events"). The book builds a server-side application; the site takes only the ideas about errors and rewrites them for the ClinicBook app.
- **Result (kotlin)** — Kotlin API reference (JetBrains) · `stable`
  https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-result/
  - vi: Result gói một giá trị thành công kiểu T hoặc một Throwable khi thất bại; có map, mapCatching, recover, fold, getOrNull, getOrElse, getOrDefault, getOrThrow, exceptionOrNull, onSuccess, onFailure; không có flatMap (bản 2.4, đọc ngày 2026-11-25) (chương "Lỗi là giá trị").
  - en: Result wraps a successful value of type T or a Throwable on failure; it has map, mapCatching, recover, fold, getOrNull, getOrElse, getOrDefault, getOrThrow, exceptionOrNull, onSuccess, onFailure; there is no flatMap (version 2.4, read on 2026-11-25) (chapter "Errors as values").
- **Working with typed errors (Arrow 2.3.0)** — Arrow (thư viện bên ngoài) · `version`
  https://arrow-kt.io/learn/typed-errors/working-with-typed-errors/
  - vi: Hai cách: kiểu bọc Either<E, A> và ngữ cảnh Raise<E>; khối either { }, .bind(), raise, ensure, ensureNotNull, fold, getOrElse, recover; catch tự bỏ qua lỗi nghiêm trọng như OutOfMemoryError và CancellationException. Phiên bản 2.3.0 theo trang cài đặt (đọc ngày 2026-11-25) (chương "Lỗi là giá trị").
  - en: Two styles: the Either<E, A> wrapper type and the Raise<E> context; the either { } block, .bind(), raise, ensure, ensureNotNull, fold, getOrElse, recover; catch skips fatal errors such as OutOfMemoryError and CancellationException. Version 2.3.0 per the setup page (read on 2026-11-25) (chapter "Errors as values").
- **Validation and accumulating errors (Arrow)** — Arrow (thư viện bên ngoài) · `version`
  https://arrow-kt.io/learn/typed-errors/validation/
  - vi: Dừng ngay ở lỗi đầu tiên (short-circuit) so với gom mọi lỗi; zipOrAccumulate nhận các khối kiểm độc lập và một hàm tạo kết quả; mapOrAccumulate kiểm từng phần tử; lỗi gom trong NonEmptyList (đọc ngày 2026-11-25, trang không ghi số phiên bản) (chương "Validate gom lỗi: applicative và monoid").
  - en: Short-circuiting at the first error versus collecting every error; zipOrAccumulate takes independent check blocks and a function building the result; mapOrAccumulate checks each element; errors are collected in a NonEmptyList (read on 2026-11-25; the page states no version number) (chapter "Validation that collects errors: applicatives and monoids").
- **Immutable data and lenses (Arrow 2.3.0)** — Arrow (thư viện bên ngoài) · `version`
  https://arrow-kt.io/learn/immutable-data/lens/
  - vi: Kotlin không có sẵn công cụ tốt cho giá trị lồng sâu, phải lặp tên trường và chép nhiều tầng; @optics sinh optic cho mỗi trường; lens có get, set, modify; copy { set / transform } đổi nhiều trường; nên dùng plugin biên dịch, KSP cần companion object (bản 2.3.0, đọc ngày 2026-11-25) (chương "FP trên Android: state bất biến và cập nhật lồng sâu").
  - en: Kotlin lacks good built-in tooling for deeply nested values, so you repeat field names and copy several levels; @optics generates an optic per field; a lens has get, set, modify; copy { set / transform } changes several fields; the compiler plugin is recommended, KSP needs a companion object (version 2.3.0, read on 2026-11-25) (chapter "FP on Android: immutable state and deep updates").

### Track L

- **Android Debug Bridge (adb)** — Android Developers · `stable`
  https://developer.android.com/tools/adb
  - vi: adb gồm client, server (cổng TCP 5037) và daemon adbd trên thiết bị; USB debugging trong tùy chọn nhà phát triển, gỡ lỗi không dây từ Android 11; adb devices, install, shell, pull, push; am start, am kill (chỉ đóng tiến trình đóng được an toàn) (đọc 2026-11-25) (chương "Quy trình gỡ lỗi, adb và bug report").
  - en: adb has a client, a server (TCP port 5037) and the adbd daemon on the device; USB debugging in the developer options, wireless debugging from Android 11; adb devices, install, shell, pull, push; am start, am kill (kills only processes that are safe to kill) (read 2026-11-25) (chapter "The debugging process, adb and bug reports").
- **Capture and read bug reports** — Android Developers · `stable`
  https://developer.android.com/studio/debug/bug-report
  - vi: Bug report chứa log thiết bị, stack trace và thông tin chẩn đoán; lấy bằng mục Take bug report, menu emulator hay adb bugreport; file ZIP với bugreport-*.txt gồm dumpsys, dumpstate, logcat; Play Console và Firebase Crashlytics thu crash và ANR của người dùng (đọc 2026-11-25) (chương "Quy trình gỡ lỗi, adb và bug report").
  - en: A bug report holds device logs, stack traces and diagnostic information; capture it with Take bug report, the emulator menu or adb bugreport; a ZIP file whose bugreport-*.txt has dumpsys, dumpstate and logcat output; Play Console and Firebase Crashlytics collect crashes and ANRs from users (read 2026-11-25) (chapter "The debugging process, adb and bug reports").
- **Debug your app** — Android Developers · `stable`
  https://developer.android.com/studio/debug
  - vi: Đặt breakpoint trong mã Java, Kotlin, C/C++, xem biến và tính biểu thức lúc chạy; thiết bị thật cần bật gỡ lỗi trong tùy chọn nhà phát triển; biến thể build phải debuggable (đọc 2026-11-25) (chương "Quy trình gỡ lỗi, adb và bug report").
  - en: Set breakpoints in Java, Kotlin and C/C++ code, examine variables and evaluate expressions at runtime; a real device needs debugging enabled in the developer options; the build variant must be debuggable (read 2026-11-25) (chapter "The debugging process, adb and bug reports").
- **Breakpoints (IntelliJ IDEA 2026.3 Help)** — JetBrains · `version`
  https://www.jetbrains.com/help/idea/using-breakpoints.html
  - vi: Bốn loại: dòng, hàm (vào hay ra), watchpoint trên trường (không bắt thay đổi qua reflection), ngoại lệ; điều kiện tính ở mỗi lần chạm, có thể có side effect; Suspend tắt thì breakpoint chỉ ghi log hay làm cò; chính sách All dừng mọi luồng, Thread chỉ dừng luồng chạm; Evaluate and log; Remove once hit; breakpoint phụ thuộc; pass count; breakpoint hàm mặc định được mô phỏng vì bản thật chậm (trang ghi ngày 17/11/2026, đọc 2026-11-25) (chương "Debugger: breakpoint, watch, evaluate").
  - en: Four kinds: line, method (entry or exit), field watchpoint (misses changes via reflection), exception; the condition is evaluated on each hit and may have side effects; with Suspend off a breakpoint only logs or triggers; the All policy suspends every thread, Thread only the one that hit; Evaluate and log; Remove once hit; dependent breakpoints; pass count; method breakpoints are emulated by default because real ones are slow (page dated 17 Nov 2026, read 2026-11-25) (chapter "The debugger: breakpoints, watches, evaluate").
- **Examine suspended program (IntelliJ IDEA 2026.3 Help)** — JetBrains · `version`
  https://www.jetbrains.com/help/idea/examining-suspended-program.html
  - vi: Watch giữ một biến hay biểu thức, tính lại ở mỗi bước, có thể nặng; watch và evaluate chỉ chạy khi dừng ở breakpoint; evaluate tính biểu thức bất kỳ trong ngữ cảnh frame, kể cả gọi hàm; cảnh báo side effect khi gọi hàm; breakpoint trong hàm được gọi lúc evaluate bị bỏ qua (đọc 2026-11-25) (chương "Debugger: breakpoint, watch, evaluate").
  - en: A watch keeps a variable or expression in view, recomputed at each step, and can be heavy; watches and evaluate only work when stopped at a breakpoint; evaluate computes any expression in the frame's context, including calls; a warning about side effects of calls; breakpoints in functions called during evaluation are ignored (read 2026-11-25) (chapter "The debugger: breakpoints, watches, evaluate").
- **Debugging coroutines (Kotlin docs)** — Kotlin docs (JetBrains) · `version`
  https://kotlinlang.org/docs/coroutines-debugging.html
  - vi: Chế độ debug đặt tên duy nhất cho mỗi coroutine (hiện trong debugger, chuỗi mô tả, tên luồng); bật bằng -Dkotlinx.coroutines.debug hay -ea; chi phí không đáng kể; khôi phục stack trace tạo bản sao ngoại lệ có thêm frame, gắn bản gốc làm cause, frame _COROUTINE._BOUNDARY; debug agent DebugProbes (dumpCoroutines) không chạy trên Android (kotlinx-coroutines 1.11.0, trang ghi ngày 07/09/2026, đọc 2026-11-25) (chương "Debugger: breakpoint, watch, evaluate").
  - en: Debug mode gives each coroutine a unique name (shown in the debugger, its string form and the thread name); enabled with -Dkotlinx.coroutines.debug or -ea; negligible overhead; stack trace recovery copies the exception with extra frames and attaches the original as cause, with a _COROUTINE._BOUNDARY frame; the DebugProbes debug agent (dumpCoroutines) is not supported on Android (kotlinx-coroutines 1.11.0, page dated 7 Sep 2026, read 2026-11-25) (chapter "The debugger: breakpoints, watches, evaluate").
- **View logs with Logcat** — Android Developers · `stable`
  https://developer.android.com/studio/debug/logcat
  - vi: Mỗi dòng có ngày, giờ, process và thread ID, tag, package, mức, nội dung; truy vấn key:value (tag, package, process, message, level, age), is:crash, is:stacktrace; dấu - để loại, ~ cho biểu thức chính quy; cùng key OR, khác key AND, &, |, ngoặc; level: là mức đó trở lên; package:mine; age tính theo đồng hồ máy tính; PROCESS ENDED, PROCESS STARTED (đọc 2026-11-25) (chương "Logcat").
  - en: Each line has a date, time, process and thread ID, tag, package, priority and message; key:value queries (tag, package, process, message, level, age), is:crash, is:stacktrace; - to exclude, ~ for regular expressions; the same key OR, different keys AND, &, |, parentheses; level: means that level or higher; package:mine; age uses the computer's clock; PROCESS ENDED, PROCESS STARTED (read 2026-11-25) (chapter "Logcat").
- **Log (android.util)** — Android API reference · `stable`
  https://developer.android.com/reference/android/util/Log
  - vi: Hàm v, d, i, w, e, wtf; hằng số VERBOSE 2 tới ASSERT 7; wtf luôn ghi ở mức ASSERT kèm stack trace; isLoggable mặc định INFO, đổi bằng setprop log.tag.<TAG>; tag dài quá 23 ký tự làm isLoggable ném lỗi tới API 25; tạo chuỗi log tốn cấp phát dù dòng bị lọc (đọc 2026-11-25) (chương "Logcat").
  - en: Functions v, d, i, w, e, wtf; constants VERBOSE 2 to ASSERT 7; wtf always logs at ASSERT with the call stack; isLoggable defaults to INFO, changed with setprop log.tag.<TAG>; tags over 23 characters make isLoggable throw up to API 25; building a log string allocates even if the line is filtered (read 2026-11-25) (chapter "Logcat").
- **Logcat command-line tool** — Android Developers · `stable`
  https://developer.android.com/tools/logcat
  - vi: adb logcat với bộ lọc tag:mức (V, D, I, W, E, F, S), *:S; -v threadtime mặc định; -b main, system, crash, radio, events, all; buffer vòng của logd; bốn tầng lọc: lúc biên dịch, thuộc tính hệ thống, mặc định của app (INFO), lúc hiển thị (đọc 2026-11-25) (chương "Logcat").
  - en: adb logcat with tag:priority filters (V, D, I, W, E, F, S), *:S; -v threadtime by default; -b main, system, crash, radio, events, all; logd ring buffers; four filtering stages: compile time, system property, the app default (INFO), display (read 2026-11-25) (chapter "Logcat").
- **Log info disclosure** — Android Developers · `stable`
  https://developer.android.com/privacy-and-security/risks/log-info-disclosure
  - vi: In thông tin đăng nhập hay thông tin định danh cá nhân ra log là lỗ hổng; từ API 16 cần READ_LOGS để đọc log của app khác; làm sạch log trong bản không phải debug; R8 -assumenosideeffects xóa mọi mức trừ warning và error; chỉ log hằng số biết lúc biên dịch khi có thể (đọc 2026-11-25) (chương "Logcat").
  - en: Printing credentials or personally identifiable information to the log is a weakness; since API 16 READ_LOGS is needed to read other apps' logs; sanitise logging in non-debug builds; R8 -assumenosideeffects removes every level except warning and error; log only compile-time constants where possible (read 2026-11-25) (chapter "Logcat").
- **Throwable (Java SE 21 API)** — Oracle · `stable`
  https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/lang/Throwable.html
  - vi: printStackTrace: dòng đầu là toString() (tên lớp, ": ", thông điệp), sau đó là các frame; ngoại lệ có cause in thêm phần Caused by; "... n more" nghĩa là phần còn lại trùng n frame cuối của stack của ngoại lệ bọc ngoài; Suppressed từ try-with-resources; getCause, initCause (đọc 2026-11-25) (chương "Đọc stack trace").
  - en: printStackTrace: the first line is toString() (class name, ": ", message), then the frames; an exception with a cause prints a Caused by section; "... n more" means the rest matches the last n frames of the enclosing exception's stack; Suppressed from try-with-resources; getCause, initCause (read 2026-11-25) (chapter "Reading stack traces").
- **Crashes (Android vitals)** — Android Developers · `stable`
  https://developer.android.com/topic/performance/vitals/crash
  - vi: App Java hay Kotlin crash khi có ngoại lệ không được bắt; Logcat in "--- beginning of crash", "FATAL EXCEPTION: main", "Process: …, PID: …"; loại ngoại lệ và chỗ ném là hai mảnh quan trọng; đi lên stack tìm chỗ truyền giá trị sai; không có mã của app thì có thể do việc bất đồng bộ; NullPointerException là nguyên nhân crash lớn nhất trên Google Play (đọc 2026-11-25) (chương "Đọc stack trace").
  - en: A Java or Kotlin app crashes on an uncaught exception; Logcat prints "--- beginning of crash", "FATAL EXCEPTION: main", "Process: …, PID: …"; the exception type and where it was thrown are the two key pieces; walk up the stack to find where a wrong value was passed; no app code may point to asynchronous work; NullPointerException is the largest cause of crashes on Google Play (read 2026-11-25) (chapter "Reading stack traces").
- **Analyze a stack trace** — Android Developers · `stable`
  https://developer.android.com/studio/debug/stacktraces
  - vi: Stack trace từ bên ngoài (bug report, Play Console) dán vào Android Studio để mỗi frame thành liên kết; mã nguồn phải cùng phiên bản với bản app tạo ra stack trace, nếu không tên file, số dòng, thứ tự gọi không khớp (đọc 2026-11-25) (chương "Đọc stack trace").
  - en: A stack trace from outside (a bug report, Play Console) can be pasted into Android Studio so each frame becomes a link; the source must be the same version as the app that produced the trace, or file names, line numbers and call order will not match (read 2026-11-25) (chapter "Reading stack traces").
- **Shrink, obfuscate, and optimize your app** — Android Developers · `version`
  https://developer.android.com/build/shrink-code
  - vi: R8 thu gọn mã từ các điểm vào trong manifest, tối ưu (inline, gộp lớp), làm rối tên (com.example.MyActivity có thể thành a.b.a), thu gọn tài nguyên; isMinifyEnabled, isShrinkResources, proguard-android-optimize.txt; từ AGP 9.3 có cú pháp optimization { enable = true } và keep rule trong file .keep; khuyên luôn bật cho bản release (đọc 2026-11-25) (chương "R8 và stack trace bị làm rối").
  - en: R8 shrinks code from the manifest's entry points, optimises (inlining, class merging), obfuscates names (com.example.MyActivity could become a.b.a), shrinks resources; isMinifyEnabled, isShrinkResources, proguard-android-optimize.txt; from AGP 9.3 an optimization { enable = true } syntax with keep rules in .keep files; recommended for every release build (read 2026-11-25) (chapter "R8 and obfuscated stack traces").
- **retrace** — Android Developers · `stable`
  https://developer.android.com/studio/command-line/retrace
  - vi: retrace path-to-mapping-file [path-to-stack-trace-file] [options]; không có file thì đọc đầu vào chuẩn; --verbose, --info, --quiet, --regex; công cụ độc lập từ command-line tools 4.0 (đọc 2026-11-25) (chương "R8 và stack trace bị làm rối").
  - en: retrace path-to-mapping-file [path-to-stack-trace-file] [options]; reads standard input without a file; --verbose, --info, --quiet, --regex; a standalone tool since command-line tools 4.0 (read 2026-11-25) (chapter "R8 and obfuscated stack traces").
- **Troubleshoot the optimization** — Android Developers · `version`
  https://developer.android.com/topic/performance/app-optimization/troubleshoot-the-optimization
  - vi: Crash chỉ ở release thường do reflection hỏng: ClassNotFoundException, NoSuchMethodException, NoSuchFieldException…; sửa bằng keep rule hay chú thích Keep của Jetpack; configuration.txt gom mọi quy tắc; -whyareyoukeeping; mapping.txt bị ghi đè mỗi lần build, lưu bản cho mỗi lần phát hành, được gói vào AAB; Logcat của Android Studio Otter 3 Feature Drop với AGP 9.0 tự dịch ngược (đọc 2026-11-25) (chương "R8 và stack trace bị làm rối").
  - en: Release-only crashes are typically broken reflection: ClassNotFoundException, NoSuchMethodException, NoSuchFieldException…; fix with a keep rule or Jetpack Keep annotations; configuration.txt merges every rule; -whyareyoukeeping; mapping.txt is overwritten on every build, keep a copy per release, bundled into the AAB; Logcat in Android Studio Otter 3 Feature Drop with AGP 9.0 deobfuscates automatically (read 2026-11-25) (chapter "R8 and obfuscated stack traces").
- **Deobfuscate or symbolicate crash stack traces (Play Console Help)** — Google Play Console Help · `stable`
  https://support.google.com/googleplay/android-developer/answer/9848633
  - vi: Tải file mapping cho từng phiên bản; App Bundle với AGP 4.1 trở lên thì Play tự lấy file từ bundle; chỉ crash sau khi tải lên mới được dịch ngược; thiếu mapping thì crash vẫn bị làm rối (đọc 2026-11-25) (chương "R8 và stack trace bị làm rối").
  - en: Upload a mapping file per version; for App Bundles with AGP 4.1 or later Play takes it from the bundle; only crashes after the upload are deobfuscated; without a mapping, crashes stay obfuscated (read 2026-11-25) (chapter "R8 and obfuscated stack traces").
- **Debug your layout with Layout Inspector** — Android Developers · `version`
  https://developer.android.com/studio/debug/layout-inspector
  - vi: Component Tree theo thời gian thực, bảng Attributes; có thể cần khởi động lại Activity; Deep Inspect: chọn một vùng để thấy mọi thành phần ở đó; Show Only Subtree, Show Only Parents; cập nhật trực tiếp; đếm recomposition và skip của Compose; xuất và nhập snapshot; chế độ nhúng được khuyên dùng (đọc 2026-11-25) (chương "Layout Inspector: xem cây giao diện").
  - en: A real-time Component Tree and an Attributes panel; an Activity restart may be needed; Deep Inspect: select a region to see every component there; Show Only Subtree, Show Only Parents; live updates; Compose recomposition and skip counts; snapshot export and import; embedded mode recommended (read 2026-11-25) (chapter "Layout Inspector: looking at the UI tree").
- **Understand gestures (Compose)** — Android Developers · `stable`
  https://developer.android.com/develop/ui/compose/touch-input/pointer-input/understand-gestures
  - vi: Hit test đi từ gốc xuống, thành phần được hit khi điểm chạm nằm trong bounds; giữa anh em chỉ cái z cao nhất được hit, như hai Button chồng nhau trong Box; sau khi hit, mọi sự kiện của cùng ngón tay tới cùng chuỗi; clickable, Button tự tiêu thụ sự kiện (đọc 2026-11-25) (chương "Layout Inspector: xem cây giao diện").
  - en: Hit testing goes from the root down, a component is hit when the pointer is within its bounds; among siblings only the highest z is hit, as with two overlapping Buttons in a Box; once hit, the same pointer's events go to the same chain; clickable and Button consume events themselves (read 2026-11-25) (chapter "Layout Inspector: looking at the UI tree").
- **Manage touch events in a ViewGroup** — Android Developers · `stable`
  https://developer.android.com/develop/ui/views/touch-and-input/gestures/viewgroup
  - vi: onInterceptTouchEvent được gọi cho mọi sự kiện chạm trên ViewGroup, kể cả trên con; trả true thì chặn, con đang xử lý nhận ACTION_CANCEL; cha thấy sự kiện trước con; requestDisallowInterceptTouchEvent; TouchDelegate mở rộng vùng chạm (đọc 2026-11-25) (chương "Layout Inspector: xem cây giao diện").
  - en: onInterceptTouchEvent is called for every touch event on a ViewGroup, including on its children; returning true intercepts, and the handling child gets ACTION_CANCEL; the parent sees events before its children; requestDisallowInterceptTouchEvent; TouchDelegate extends a touch area (read 2026-11-25) (chapter "Layout Inspector: looking at the UI tree").
- **Debug your database with the Database Inspector** — Android Developers · `version`
  https://developer.android.com/studio/inspect/database
  - vi: Xem, truy vấn, sửa database khi app chạy, với SQLite có sẵn và Room; API 26+, không dùng với SQLite app tự mang theo; Live updates làm bảng chỉ đọc; sửa hiện ngay nếu UI quan sát bằng Flow hay LiveData; chạy @Query của DAO; tab truy vấn cho phép UPDATE, INSERT, DELETE; giữ kết nối mở; chế độ offline chỉ đọc (đọc 2026-11-25) (chương "Dữ liệu và việc nền: Database Inspector, Background Task Inspector").
  - en: Inspect, query and modify databases while the app runs, for built-in SQLite and Room; API 26+, not with SQLite bundled in the app; Live updates make the table read-only; edits show at once if the UI observes through Flow or LiveData; run DAO @Query functions; the query tab allows UPDATE, INSERT, DELETE; keep connections open; offline mode is read-only (read 2026-11-25) (chapter "Data and background work: Database Inspector, Background Task Inspector").
- **Debug WorkManager workers with Background Task Inspector** — Android Developers · `version`
  https://developer.android.com/studio/inspect/task
  - vi: Worker của WorkManager 2.5.0+, thiết bị API 26+; danh sách tên lớp, trạng thái, giờ bắt đầu, số lần thử lại; chi tiết: tag, id, ràng buộc, tần suất, trạng thái, vị trí trong chuỗi, đầu ra; Graph View; hủy worker; job, alarm, wakelock chuyển từ Energy profiler (đọc 2026-11-25) (chương "Dữ liệu và việc nền: Database Inspector, Background Task Inspector").
  - en: WorkManager 2.5.0+ workers on API 26+ devices; a list of class name, state, start time, retries; details: tag, id, constraints, frequency, state, chain position, output; Graph View; cancelling a worker; jobs, alarms, wakelocks migrated from the Energy profiler (read 2026-11-25) (chapter "Data and background work: Database Inspector, Background Task Inspector").
- **WorkInfo.State** — Android API reference · `stable`
  https://developer.android.com/reference/androidx/work/WorkInfo.State
  - vi: ENQUEUED chạy khi ràng buộc thỏa và có tài nguyên; RUNNING; SUCCEEDED (việc định kỳ quay về ENQUEUED); FAILED, việc phụ thuộc cũng FAILED; BLOCKED vì việc trước chưa xong thành công; CANCELLED, việc phụ thuộc cũng CANCELLED; isFinished cho SUCCEEDED, FAILED, CANCELLED (đọc 2026-11-25) (chương "Dữ liệu và việc nền: Database Inspector, Background Task Inspector").
  - en: ENQUEUED runs when constraints are met and resources are available; RUNNING; SUCCEEDED (periodic work goes back to ENQUEUED); FAILED, dependent work also FAILED; BLOCKED because prerequisites have not succeeded; CANCELLED, dependent work also CANCELLED; isFinished for SUCCEEDED, FAILED, CANCELLED (read 2026-11-25) (chapter "Data and background work: Database Inspector, Background Task Inspector").
- **Define work requests (WorkManager)** — Android Developers · `stable`
  https://developer.android.com/develop/background-work/background-tasks/persistent/getting-started/define-work
  - vi: Ràng buộc NetworkType (UNMETERED là Wi-Fi), BatteryNotLow, RequiresCharging, DeviceIdle, StorageNotLow; nhiều ràng buộc thì phải thỏa tất cả; ràng buộc mất giữa chừng thì worker bị dừng và chạy lại sau; Result.retry với backoff mặc định EXPONENTIAL 30 giây, tối thiểu 10 giây (đọc 2026-11-25) (chương "Dữ liệu và việc nền: Database Inspector, Background Task Inspector").
  - en: Constraints NetworkType (UNMETERED is Wi-Fi), BatteryNotLow, RequiresCharging, DeviceIdle, StorageNotLow; with several, all must be met; if one becomes unmet mid-run the worker is stopped and retried later; Result.retry with default EXPONENTIAL backoff of 30 seconds, minimum 10 seconds (read 2026-11-25) (chapter "Data and background work: Database Inspector, Background Task Inspector").
- **Inspect your app's memory usage with Memory Profiler** — Android Developers · `version`
  https://developer.android.com/studio/profile/memory-profiler
  - vi: Heap dump: số instance, Shallow Size, Retained Size (bộ nhớ instance chi phối theo cây dominator); Depth là số bước ngắn nhất từ GC root; References liệt kê mọi tham chiếu; bộ lọc hiện Activity/Fragment bị rò (đọc 2026-11-25) (chương "Bộ nhớ: churn, rò rỉ, heap dump").
  - en: Heap dumps: instance counts, Shallow Size, Retained Size (memory the instance dominates in the dominator tree); Depth is the shortest hops from a GC root; References lists every reference; a filter shows leaked Activities/Fragments (read 2026-11-25) (chapter "Memory: churn, leaks, heap dumps").
- **Overview of memory management** — Android Developers · `stable`
  https://developer.android.com/topic/performance/memory-overview
  - vi: Heap phân thế hệ; GC chạy khi một thế hệ đầy, có thể đẩy khung hình quá 16 ms; cấp phát trong vòng lặp trong cùng; heap có giới hạn cứng, chạm thì OutOfMemoryError; getMemoryClass (đọc 2026-11-25) (chương "Bộ nhớ: churn, rò rỉ, heap dump").
  - en: A generational heap; GC runs when a generation fills and can push frames past 16 ms; allocating in innermost loops; the heap has a hard limit, reaching it gives OutOfMemoryError; getMemoryClass (read 2026-11-25) (chapter "Memory: churn, leaks, heap dumps").
- **Manage your app's memory** — Android Developers · `stable`
  https://developer.android.com/topic/performance/memory/manage-app-memory
  - vi: Rò rỉ thường do giữ tham chiếu trong biến static; giữ logic trong Activity thay vì ViewModel để không rò Context; churn gây nhiều lần GC; đối tượng tạm trong vòng lặp, khi recompose hay khi vẽ; onTrimMemory (đọc 2026-11-25) (chương "Bộ nhớ: churn, rò rỉ, heap dump").
  - en: Leaks are usually caused by holding references in static fields; keeping such logic in the Activity rather than the ViewModel avoids leaking a Context; churn causes many GC events; temporary objects in loops, in recomposition or while drawing; onTrimMemory (read 2026-11-25) (chapter "Memory: churn, leaks, heap dumps").
- **Record Java/Kotlin allocations** — Android Developers · `version`
  https://developer.android.com/studio/profile/record-java-kotlin-allocations
  - vi: Ghi các lần cấp phát kèm stack trace và lúc giải phóng; chế độ Sampled giảm chi phí so với Full; mỗi lần GC hiện trên dòng thời gian (đọc 2026-11-25) (chương "Bộ nhớ: churn, rò rỉ, heap dump").
  - en: Records allocations with stack traces and deallocation times; Sampled mode costs less than Full; each GC event appears on the timeline (read 2026-11-25) (chapter "Memory: churn, leaks, heap dumps").
- **How LeakCanary works (LeakCanary 2.14)** — Square (thư viện bên ngoài) · `version`
  https://square.github.io/leakcanary/fundamentals-how-leakcanary-works/
  - vi: Bốn bước: phát hiện đối tượng bị giữ, chụp heap, phân tích, phân loại; theo dõi Activity, Fragment, view của Fragment, ViewModel đã hủy bằng tham chiếu yếu; chờ 5 giây và chạy GC; ngưỡng mặc định 5 khi app hiện, 1 khi ẩn; leak trace là đường tham chiếu giữ đối tượng (đọc 2026-11-25) (chương "Bộ nhớ: churn, rò rỉ, heap dump").
  - en: Four steps: detect retained objects, dump the heap, analyse, categorise; watches destroyed Activities, Fragments, Fragment views and ViewModels via weak references; waits 5 seconds and runs GC; default threshold 5 when visible, 1 when not; the leak trace is the reference path keeping the object (read 2026-11-25) (chapter "Memory: churn, leaks, heap dumps").
- **LeakCanary: introduction** — Square (thư viện bên ngoài) · `version`
  https://square.github.io/leakcanary/fundamentals/
  - vi: Rò rỉ bộ nhớ là lỗi lập trình giữ tham chiếu tới đối tượng không còn cần; nguyên nhân hay gặp: Activity trong trường static, giữ Activity làm Context trong đối tượng sống qua thay đổi cấu hình, đăng ký listener, receiver, subscription mà không hủy, Fragment trên back stack giữ view (đọc 2026-11-25) (chương "Bộ nhớ: churn, rò rỉ, heap dump").
  - en: A memory leak is a programming error keeping a reference to an object no longer needed; common causes: an Activity in a static field, keeping an Activity as a Context in an object surviving configuration changes, registering listeners, receivers or subscriptions without unregistering, a back-stack Fragment holding its views (read 2026-11-25) (chapter "Memory: churn, leaks, heap dumps").
- **Slow rendering (Android vitals)** — Android Developers · `stable`
  https://developer.android.com/topic/performance/vitals/render
  - vi: Mỗi khung dưới 16 ms để đạt 60 fps; 11 ms ở 90, 8 ms ở 120; quá hạn thì Choreographer bỏ cả khung; khung chậm 16–700 ms, khung đứng 700 ms–5 s, quá 5 s là ANR; Record View#draw trên luồng UI, DrawFrame trên RenderThread; nguyên nhân: việc dài trên luồng UI, binder, khóa, GC, tải bitmap; trace marker tốn khoảng 10 µs, đừng gắn cho hàm dưới khoảng 200 µs; method trace cho giật giả (đọc 2026-11-25) (chương "CPU, trace và khung hình giật").
  - en: Each frame under 16 ms for 60 fps; 11 ms at 90, 8 ms at 120; past the deadline Choreographer drops the whole frame; slow frames 16–700 ms, frozen 700 ms–5 s, over 5 s an ANR; Record View#draw on the UI thread, DrawFrame on RenderThread; causes: long work on the UI thread, binder, locks, GC, bitmap uploads; a trace marker costs about 10 µs, avoid it below about 200 µs; method traces show false jank (read 2026-11-25) (chapter "CPU, traces and janky frames").
- **Overview of system tracing** — Android Developers · `stable`
  https://developer.android.com/topic/performance/tracing
  - vi: System trace ghi hoạt động thiết bị trong thời gian ngắn, gom dữ liệu kernel: lập lịch CPU, đĩa, luồng của app; Perfetto từ Android 10, mã nguồn mở; không cho chi tiết thực thi bên trong app (đọc 2026-11-25) (chương "CPU, trace và khung hình giật").
  - en: A system trace records device activity briefly, combining kernel data: CPU scheduling, disk, app threads; Perfetto from Android 10, open source; it does not show detailed execution inside the app (read 2026-11-25) (chapter "CPU, traces and janky frames").
- **Define custom events** — Android Developers · `stable`
  https://developer.android.com/topic/performance/tracing/custom-events
  - vi: Hàm trace của Jetpack (androidx.tracing) mở đoạn có tên, tự kết thúc khi lambda xong, lồng được; app phải profileable để đoạn tự đặt hiện ra (đọc 2026-11-25) (chương "CPU, trace và khung hình giật").
  - en: Jetpack's trace function (androidx.tracing) opens a named section that ends automatically when the lambda completes, and can nest; the app must be profileable for custom sections to appear (read 2026-11-25) (chapter "CPU, traces and janky frames").
- **Record traces (Android Studio)** — Android Developers · `version`
  https://developer.android.com/studio/profile/record-traces
  - vi: System trace trong Android Studio hiện hoạt động toàn hệ thống: CPU, tương tác, màn hình, luồng, lõi CPU, bộ nhớ tiến trình; thời gian mỗi khung trên main thread và RenderThread (đọc 2026-11-25) (chương "CPU, trace và khung hình giật").
  - en: A system trace in Android Studio shows system-wide activity: CPU, interactions, display, threads, CPU cores, process memory; each frame's time on the main thread and RenderThread (read 2026-11-25) (chapter "CPU, traces and janky frames").
- **Perfetto documentation** — Perfetto (Google, mã nguồn mở) · `version`
  https://perfetto.dev/docs/
  - vi: Bộ SDK, daemon và công cụ mã nguồn mở dùng tracing; hệ thống tracing mặc định của Android; UI chạy hoàn toàn trong trình duyệt, không cần cài, chạy offline; phân tích bằng SQL (đọc 2026-11-25) (chương "CPU, trace và khung hình giật").
  - en: An open-source suite of SDKs, daemons and tools for tracing; the default tracing system on Android; a fully local browser UI with no installation that works offline; SQL-based analysis (read 2026-11-25) (chapter "CPU, traces and janky frames").
- **ANRs (Android vitals)** — Android Developers · `stable`
  https://developer.android.com/topic/performance/vitals/anr
  - vi: ANR khi luồng main không xử lý được input hay vẽ; ở tiền cảnh thì hiện hộp thoại; input không phản hồi trong 5 giây; startForeground trong 5 giây; nguyên nhân: I/O, tính toán dài, binder đồng bộ, chờ khóa của luồng khác, deadlock; trace ở /data/anr, bug report (đọc 2026-11-25) (chương "ANR và StrictMode").
  - en: An ANR when the main thread cannot handle input or draw; a dialog in the foreground; input unanswered within 5 seconds; startForeground within 5 seconds; causes: I/O, long computation, synchronous binder, waiting for another thread's lock, deadlock; traces in /data/anr, bug reports (read 2026-11-25) (chapter "ANRs and StrictMode").
- **Diagnose and fix ANRs** — Android Developers · `stable`
  https://developer.android.com/topic/performance/anrs/diagnose-and-fix-anrs
  - vi: Hạn mặc định của AOSP và Pixel, có thể khác theo hãng: input 5 s; service 20 s tiền cảnh, 200 s nền; broadcast 10 s / 60 s tới Android 13, 10–20 s / 60–120 s từ Android 14; tranh khóa, luồng giữ khóa cũng liên quan; Blocked, Waiting, "held by"; deadlock; Mutex.withLock; cụm nativePollOnce với ANR input thường không hành động được (đọc 2026-11-25) (chương "ANR và StrictMode").
  - en: AOSP and Pixel defaults that may vary by manufacturer: input 5 s; service 20 s foreground, 200 s background; broadcast 10 s / 60 s up to Android 13, 10–20 s / 60–120 s from Android 14; lock contention, the holder thread is involved too; Blocked, Waiting, "held by"; deadlock; Mutex.withLock; nativePollOnce clusters for input ANRs are generally not actionable (read 2026-11-25) (chapter "ANRs and StrictMode").
- **StrictMode (android.os)** — Android API reference · `stable`
  https://developer.android.com/reference/android/os/StrictMode
  - vi: Công cụ cho nhà phát triển bắt việc làm vô tình, hay dùng nhất để bắt truy cập đĩa, mạng trên luồng main; ThreadPolicy, VmPolicy, detectAll, penaltyLog; không phải cơ chế bảo mật, không bảo đảm bắt mọi truy cập (JNI); không buộc sửa mọi thứ, nhưng mạng trên luồng UI gần như luôn là vấn đề (đọc 2026-11-25) (chương "ANR và StrictMode").
  - en: A developer tool that detects things done by accident, most often disk or network access on the main thread; ThreadPolicy, VmPolicy, detectAll, penaltyLog; not a security mechanism, not guaranteed to find every access (JNI); no need to fix everything, but network on the UI thread is almost always a problem (read 2026-11-25) (chapter "ANRs and StrictMode").
- **Inspect network traffic with the Network Inspector** — Android Developers · `version`
  https://developer.android.com/studio/debug/network-profiler
  - vi: Hoạt động mạng thời gian thực trên dòng thời gian gửi và nhận; mỗi request có kích thước, loại, trạng thái, thời gian truyền; header, body, call stack; Thread View cho biết luồng gửi; chỉ hỗ trợ HttpsURLConnection và OkHttp (Retrofit dùng OkHttp); Rules sửa mã trạng thái, header, body của phản hồi (đọc 2026-11-25) (chương "Mạng và pin").
  - en: Real-time network activity on a sent/received timeline; each request's size, type, status, transfer time; headers, body, call stack; Thread View shows the sending thread; supports only HttpsURLConnection and OkHttp (Retrofit uses OkHttp); Rules change a response's status, headers, body (read 2026-11-25) (chapter "Network and battery").
- **Optimize network access (efficient downloads)** — Android Developers · `stable`
  https://developer.android.com/training/efficient-downloads/efficient-network-access
  - vi: Radio 3G điển hình: toàn công suất, công suất thấp tiết kiệm khoảng 50 %, chờ; mỗi kết nối mới đưa radio lên toàn công suất; 5 giây đuôi rồi 12 giây công suất thấp, mỗi phiên ít nhất khoảng 18 giây; gom request; tải trước mỗi 2–5 phút, 1–5 MB; WorkManager khi sạc và Wi-Fi; tìm sóng rất tốn pin; connection pooling mặc định (đọc 2026-11-25) (chương "Mạng và pin").
  - en: A typical 3G radio: full power, low power saving about 50%, standby; each new connection goes to full power; 5 seconds of tail then 12 at low power, at least about 18 seconds per session; bundle requests; prefetch every 2–5 minutes, 1–5 MB; WorkManager when charging and on Wi-Fi; searching for signal is power-hungry; connection pooling by default (read 2026-11-25) (chapter "Network and battery").
- **Manage network usage** — Android Developers · `stable`
  https://developer.android.com/develop/connectivity/network-ops/managing
  - vi: Chiến lược thường dùng là chỉ tải dữ liệu lớn khi có Wi-Fi; Wi-Fi thường nhanh hơn, mạng di động thường bị đo lưu lượng và tốn tiền (đọc 2026-11-25) (chương "Mạng và pin").
  - en: A common strategy is to fetch large data only on Wi-Fi; Wi-Fi is typically faster, and mobile data is often metered and can be expensive (read 2026-11-25) (chapter "Network and battery").
- **Excessive partial wake locks (Android vitals)** — Android Developers · `stable`
  https://developer.android.com/topic/performance/vitals/wakelock
  - vi: Wake lock cục bộ dùng quá mức làm hao pin vì máy không vào được trạng thái tiết kiệm; quá mức khi tổng từ 2 giờ trong 24 giờ, tính khi app ở nền hay chạy foreground service; miễn âm thanh, vị trí, job do người dùng khởi động; quá 5 % phiên trong 28 ngày có thể ảnh hưởng hiển thị trên Play (đọc 2026-11-25) (chương "Mạng và pin").
  - en: Excessive partial wake locks drain the battery by keeping the device out of low-power states; excessive when they total 2 hours or more in 24, counted in the background or with a foreground service; audio, location and user-initiated jobs exempt; over 5% of sessions in 28 days can affect visibility on Play (read 2026-11-25) (chapter "Network and battery").
- **Write a Macrobenchmark** — Android Developers · `version`
  https://developer.android.com/topic/performance/benchmarking/macrobenchmark-overview
  - vi: Đo khởi động, cuộn, animation; module com.android.test riêng; app được đo gần bản release, không debuggable, nên bật thu gọn, profileable; measureRepeated với packageName, metrics, iterations; startupMode COLD, WARM, HOT; compilationMode mặc định cài Baseline Profile nếu có; không khuyên chạy emulator; báo lỗi khi debuggable, emulator, pin yếu; kết quả JSON và trace mỗi lần lặp (đọc 2026-11-25) (chương "Đo hiệu năng cho đúng").
  - en: Measures startup, scrolling, animations; a separate com.android.test module; the measured app close to release, non-debuggable, preferably minified, profileable; measureRepeated with packageName, metrics, iterations; startupMode COLD, WARM, HOT; compilationMode installs a Baseline Profile by default if available; emulators discouraged; errors for debuggable apps, emulators, low battery; JSON results and a trace per iteration (read 2026-11-25) (chapter "Measuring performance properly").
- **Capture Macrobenchmark metrics** — Android Developers · `version`
  https://developer.android.com/topic/performance/benchmarking/macrobenchmark-metrics
  - vi: StartupTimingMetric: timeToInitialDisplayMs, timeToFullDisplayMs, nhỏ nhất, trung vị, lớn nhất, luôn tập trung vào trung vị; FrameTimingMetric: frameDurationCpuMs, frameOverrunMs (API 31+), phân vị P50, P90, P95, P99, nhìn khung tệ nhất ở P95, P99 (đọc 2026-11-25) (chương "Đo hiệu năng cho đúng").
  - en: StartupTimingMetric: timeToInitialDisplayMs, timeToFullDisplayMs, minimum, median, maximum, always focus on the median; FrameTimingMetric: frameDurationCpuMs, frameOverrunMs (API 31+), P50, P90, P95, P99 percentiles, look at the worst frames at P95, P99 (read 2026-11-25) (chapter "Measuring performance properly").
- **App startup time** — Android Developers · `stable`
  https://developer.android.com/topic/performance/vitals/launch-time
  - vi: TTID là thời gian tới khung đầu tiên; TTFD là tới khi dùng được, chỉ báo khi gọi reportFullyDrawn; cold, warm, hot start; khuyên tối ưu theo giả định cold start; dòng Displayed trong Logcat (đọc 2026-11-25) (chương "Đo hiệu năng cho đúng").
  - en: TTID is the time to the first frame; TTFD to being usable, reported only with reportFullyDrawn; cold, warm, hot starts; recommends optimising for a cold start; the Displayed line in Logcat (read 2026-11-25) (chapter "Measuring performance properly").

### Chung / Shared

- **Protocol Explorer** — Vercel (trang mẫu) · đọc thêm / further reading
  https://protocol-explorer-alpha.vercel.app/
  - vi: Cảm hứng UX: tinh thần explorer từng bước, chọn thành phần. Site chỉ học cách truyền đạt, không sao chép mã, hình hay chữ.
  - en: UX inspiration: the step-by-step explorer idea and picking a component. This site learns only the way of teaching and copies no code, image or text.
- **Designed to Scale** — Vercel (trang mẫu) · đọc thêm / further reading
  https://designed-to-scale.vercel.app/
  - vi: Cảm hứng UX: chia bài thành bước, sơ đồ có chuyển động. Chỉ học cách truyền đạt, không sao chép.
  - en: UX inspiration: splitting a lesson into steps and animated diagrams. Only the way of teaching is learned; nothing is copied.
- **Declaring language in HTML** — W3C Internationalization
  https://www.w3.org/International/questions/qa-html-language-declarations
  - vi: Khai báo ngôn ngữ trang bằng thuộc tính lang và đánh dấu ngôn ngữ cho từng đoạn văn bản.
  - en: Declaring the page language with the lang attribute and marking the language of text fragments.
- **W3C Internationalization** — W3C
  https://www.w3.org/International/
  - vi: Nguyên tắc quốc tế hóa chung cho web, làm nền cho cách tổ chức song ngữ của site.
  - en: General web internationalization principles behind how this site organizes two languages.
- **Understanding Success Criterion 3.1.1: Language of Page** — W3C WAI (WCAG 2.2) · `normative`
  https://www.w3.org/WAI/WCAG22/Understanding/language-of-page.html
  - vi: Tiêu chí 3.1.1: ngôn ngữ của trang phải xác định được bằng phần mềm, nên site cập nhật lang khi đổi ngôn ngữ.
  - en: Success criterion 3.1.1: the page language must be programmatically determinable, so the site updates lang when you switch language.
- **Understanding Success Criterion 3.1.2: Language of Parts** — W3C WAI (WCAG 2.2) · `normative`
  https://www.w3.org/WAI/WCAG22/Understanding/language-of-parts.html
  - vi: Tiêu chí 3.1.2: đoạn văn bản khác ngôn ngữ trang cần được đánh dấu, nên thuật ngữ tiếng Anh trong bản tiếng Việt được bọc lang="en".
  - en: Success criterion 3.1.2: passages in another language should be marked, so English terms inside the Vietnamese text are wrapped in lang="en".
- **lang HTML global attribute** — MDN Web Docs
  https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Global_attributes/lang
  - vi: Cú pháp và ý nghĩa của thuộc tính lang.
  - en: Syntax and meaning of the lang attribute.
- **prefers-reduced-motion CSS media feature** — MDN Web Docs
  https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/@media/prefers-reduced-motion
  - vi: Đọc tùy chọn giảm chuyển động của hệ điều hành; site dùng thêm nút tắt thủ công.
  - en: Reads the operating-system reduced-motion preference; the site adds a manual switch on top.
- **ARIA Authoring Practices Guide** — W3C WAI
  https://www.w3.org/WAI/ARIA/apg/
  - vi: Mẫu tab, hộp thoại và phím tắt mà các thành phần giao diện của site tham khảo.
  - en: Tab, dialog and keyboard patterns that the site interface components follow.

## Sách tham khảo / Reference books

Sách là nguồn giảng dạy cùng tài liệu chính thức; khi mâu thuẫn, tài liệu chính thức thắng. Bài giảng viết lại bằng lời của site và không dẫn số chương sách. Framework của tác giả ghi tên tác giả. Books are teaching sources alongside the official documentation; when they conflict, the official documentation wins. Lessons are written in the site's own words and do not cite book chapter numbers. Named frameworks credit their authors.

- *Kotlin Coroutines: Deep Dive* — Marcin Moskała (track A)
- *Advanced Kotlin; Effective Kotlin* — Marcin Moskała (track A, B)
- *Android Animations by Tutorials* — Filip Babić, Prateek Prasad, Alex Sullivan (track C)
- *The Design of Everyday Things (Revised & Expanded)* — Don Norman (track D)
- *Don't Make Me Think, Revisited* — Steve Krug (track D, E)
- *Design for How People Think* — John Whalen (track D)
- *Measuring the User Experience (3rd ed.)* — Bill Albert, Tom Tullis (track D)
- *Strategic Writing for UX* — Torrey Podmajersky (track D)
- *Writing Is Designing* — Michael Metts, Andy Welfle (track D, E)
- *Articulating Design Decisions* — Tom Greever (track D)
- *Designing for Behavior Change (2nd ed.)* — Stephen Wendel (track D)
- *Design Sprint* — Richard Banfield, C. Todd Lombardo, Trace Wax (track D)
- *The Design Thinking Playbook* — Michael Lewrick, Patrick Link, Larry Leifer (track D)
- *Designing Interfaces (3rd ed.)* — Jenifer Tidwell, Charles Brewer, Aynne Valencia (track E)
- *Mobile Design Pattern Gallery* — Theresa Neil (track E)
- *Practical UI Patterns for Design Systems* — Diana MacDonald (track E)
- *The Non-Designer's Design Book* — Robin Williams (track E)
- *Kotlin Coroutines by Tutorials* — Kodeco (track A)
- *Android UI Development with Jetpack Compose* — Thomas Künneth (track B)
- *Jetpack Compose by Tutorials* — Kodeco (track B)
- *Jetpack Compose 1.3 Essentials* — Neil Smyth (track B)
- *Kotlin Essentials; Effective Kotlin; Kotlin Exercises* — Marcin Moskała (track F)
- *Clean Android Architecture* — Alexandru Dumbravan (track G)
- *Clean Architecture for Android* — Eran Boudjnah (track G)
- *Saving Data on Android* — raywenderlich.com (Kodeco) (track H)
- *Mobile System Design* — Tjeerd in 't Veen (track I)
- *Designing Data-Intensive Applications* — Martin Kleppmann (track I)
- *System Design Interview (vol. 1, 2)* — Alex Xu (track I)
- *Acing the System Design Interview* — Zhiyong Tan (track I)
- *Operating System Concepts (10th ed.)* — Abraham Silberschatz, Peter B. Galvin, Greg Gagne (track I)
- *API Design Patterns* — JJ Geewax (track I)
- *Clean Code; The Clean Coder; Clean Architecture; Clean Craftsmanship; Clean Agile* — Robert C. Martin (track J)
- *The Software Craftsman* — Sandro Mancuso (track J)
- *Code That Fits in Your Head* — Mark Seemann (track J, K)
- *Android Test-Driven Development* — Kodeco (track J)
- *From Objects to Functions* — Uberto Barbini (track K)
- *Functional Programming in Kotlin* — Marco Vermeulen, Rúnar Bjarnason, Paul Chiusano (track K)
- *Functional Programming in Kotlin by Tutorials* — Kodeco (track K)
- *Functional Kotlin* — Marcin Moskała (track K)

## Cảm hứng UX / UX inspiration

Hai trang mẫu chỉ là cảm hứng UX (bố cục, cách xem theo bước); site không sao chép mã, CSS, SVG, câu chữ hay ví dụ của chúng. The two sample sites are UX inspiration only; no code, CSS, SVG, wording or examples are copied. Xem trang Nguồn của site / see the site's Sources page.
