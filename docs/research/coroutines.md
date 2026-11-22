# Nghiên cứu track A: Kotlin Coroutines (P2)

> Ngày đối chiếu 2026-11-20. Đọc trực tiếp các trang bên dưới (tải về dạng văn bản và đối chiếu từng khẳng định). Phiên bản: Kotlin 2.4.21, kotlinx.coroutines 1.11.0, AndroidX Lifecycle 2.11.1 (xem `global.md`).

## Thay đổi so với spec (tài liệu đã được tổ chức lại)

| Spec ghi | Thực tế (đã đọc) | Xử lý |
|---|---|---|
| `kotlinlang.org/docs/flow.html` | stub chuyển hướng | dùng `coroutines-flow.html` ("Flows") |
| `…/cancellation-and-timeouts.html` | stub chuyển hướng | dùng `coroutines-cancellation.html` |
| Trang Flow chứa `conflate`, `collectLatest`, `flatMap*` | Trang "Flows" chỉ còn cold/hot, `flowOn`, `buffer`, `catch`, StateFlow/SharedFlow; `buffer`, `conflate`, `collectLatest` nằm ở **`coroutines-flow-operators.html`** ("Flow operators", 200) | thêm nguồn này; **không** khẳng định `flatMapConcat/Merge/Latest` vì chưa tìm thấy trong hai trang (xem "Điểm chưa xác minh") |
| `repeatOnLifecycle` thuộc trang lifecycle | Trang `topic/libraries/architecture/coroutines` chỉ nói ViewModelScope và scope gắn Composition; `repeatOnLifecycle` có trong ví dụ của `developer.android.com/kotlin/flow/stateflow-and-sharedflow` (200) | thêm nguồn này |
| `collectAsStateWithLifecycle` | Có ở `developer.android.com/develop/ui/compose/state` ("State and Jetpack Compose", 200) và trong reference `androidx.lifecycle.compose` | thêm nguồn này |

## Khẳng định theo chương (kèm nguồn và nhãn dự kiến)

**A0 Bản đồ.** Flow là chuỗi giá trị tuần tự sinh bất đồng bộ, không phải một thread riêng (`coroutines-flow`: "A flow represents a sequential stream of values that can be produced asynchronously"). ViewModel sở hữu coroutine, view không kích hoạt logic nghiệp vụ (`coroutines-best-practices`, nhãn `guideline`). `viewModelScope`: coroutine bị hủy khi ViewModel bị clear (`architecture/coroutines`, `stable`).

**A1 suspend và continuation.** Coroutine là computation có thể suspend/resume; bản thân `suspend` không tạo thread (`coroutines-basics`). Đối chiếu bộ nhớ coroutine so với thread (50 000 thread cần mỗi thread một stack riêng) là ví dụ của trang basics, **không** dùng số liệu. Continuation/state machine là chi tiết compiler → `impl`, mã giả gắn "minh họa"; sách KCDD chỉ để lấy ý.

**A2 Scope, Job.** Coroutine mới nhận context từ scope cha, Job của nó là con của Job cha; "When the parent coroutine is cancelled, all its children are recursively cancelled" (`coroutine-context-and-dispatchers`). Có hai cách ghi đè quan hệ cha–con (scope khác, hoặc truyền `Job` mới). `supervisorScope`: lan truyền hủy một chiều, chỉ hủy con khi chính nó fail, vẫn đợi mọi con (`exception-handling`).

**A3 Builders.** Mặc định tuần tự; `async` cho thực thi đồng thời, `await` lấy kết quả. Với structured concurrency, nếu `concurrentSum` ném exception thì mọi coroutine trong scope của nó bị hủy (`composing-suspending-functions`). `withContext` chạy khối trong context khác và trả kết quả (`coroutine-context-and-dispatchers`); không phải coroutine detached.

**A4 Context và Dispatcher.** Context ghép bằng toán tử `+`; `CoroutineName` giống tên thread, dùng khi debug; `Dispatchers.Default`, `Dispatchers.Unconfined`, dispatcher riêng (`coroutine-context-and-dispatchers`). Main-safety: suspend function nên an toàn khi gọi từ Main, lớp làm việc chặn dài phải tự chuyển bằng `withContext`; inject dispatcher, tránh hard-code (`coroutines-best-practices`, `guideline`).

**A5 Hủy và timeout.** "coroutine cancellation is cooperative": chỉ phản ứng khi suspend hoặc kiểm tra hủy; `isActive` trả `false`, `ensureActive()` ném `CancellationException`; khi bị hủy, coroutine ném `CancellationException` ở lần kiểm tra kế tiếp; `NonCancellable` chỉ truyền cho `withContext`, tránh dùng với `launch/async` vì phá structured concurrency; `withTimeoutOrNull` dùng cho trường hợp muốn fallback (`coroutines-cancellation`). Best practice: không nuốt `CancellationException` (không catch, hoặc luôn ném lại nếu catch) (`coroutines-best-practices`).

**A6 Exception.** `launch` coi exception là uncaught; `async` dựa vào người dùng gọi `await`; `CoroutineExceptionHandler` trên root coroutine là "generic catch block" cho root đó và các con, nhưng **không thể phục hồi**: handler gọi khi coroutine đã hoàn tất với exception; `async` bắt mọi exception vào `Deferred` nên handler của nó cũng vô tác dụng; coroutine trong supervision scope không lan exception lên cha và được loại khỏi quy tắc đó (`exception-handling`). `SupervisorJob`: fail hoặc cancel của một con không lan lên supervisor hay con khác.

**A7 Flow.** Cold flow bắt đầu sản xuất khi được collect, mỗi collector chạy một lần riêng; hot flow phát độc lập với collector (`coroutines-flow`). Mặc định cold flow chạy trong cùng coroutine context của collector; `flowOn` đổi context của upstream. `buffer` cho producer chạy trước tối đa N giá trị; `conflate` là rút gọn của `buffer(1, DROP_OLDEST)`; `collectLatest` hủy xử lý đã bắt đầu (`coroutines-flow-operators`). Channel về khái niệm giống `BlockingQueue` nhưng `send`/`receive` là suspend; nhiều coroutine nhận cùng channel là fan-out (`channels`). StateFlow là state holder có giá trị hiện tại; ví dụ SharedFlow `replay = 1` phát lại giá trị cuối cho collector mới (`kotlin/flow/stateflow-and-sharedflow`).

**A8 Lifecycle và Compose.** `viewModelScope` hủy khi ViewModel clear; coroutine gắn Composition tự hủy khi composable rời màn hình (`architecture/coroutines`). `repeatOnLifecycle(STARTED)` chạy khối trong coroutine mới mỗi lần lifecycle ở STARTED trở lên và hủy khi STOPPED (ví dụ trong `stateflow-and-sharedflow`). `LaunchedEffect`: chạy coroutine khi vào Composition, hủy khi rời, và nếu key đổi thì hủy coroutine cũ rồi chạy mới (`side-effects`). `collectAsStateWithLifecycle` thu giá trị Flow theo lifecycle để tiết kiệm tài nguyên (`develop/ui/compose/state`).

**A9 Shared state và test.** Volatile không giải quyết vấn đề đồng thời: bảo đảm đọc/ghi từng biến nhưng không bảo đảm tính nguyên tử của thao tác lớn như tăng; Mutex có `lock` suspend, không chặn thread; thread confinement; cấu trúc dữ liệu thread-safe (`shared-mutable-state-and-concurrency`). `runTest`, `TestDispatcher` dùng chung một `TestCoroutineScheduler` điều khiển virtual time; nếu code chuyển sang dispatcher khác (ví dụ `withContext`), delay không còn được bỏ qua (`kotlin/coroutines/test`).

## Điểm chưa xác minh / cách xử lý

- `flatMapConcat/flatMapMerge/flatMapLatest`: không có trong hai trang đã đọc ("Flows", "Flow operators"). Site **không** mô phỏng hay khẳng định ngữ nghĩa của chúng; chỉ nhắc tên ở mức "xem tài liệu API", không dựa trên trí nhớ.
- Số thread của `Dispatchers.IO`/`Default`: không ghi (spec cấm hard-code). Tên thread trong sơ đồ chỉ là ví dụ.
- Thứ tự thực thi giữa các coroutine cùng dispatcher không được tài liệu bảo đảm: mô hình chỉ dùng FIFO để minh họa, gắn nhãn `simplified`.
- Hành vi chính xác khi `CancellationException` bị bắt rồi tiếp tục chạy: mô hình giản lược; chỉ khẳng định điều trang `coroutines-best-practices` nêu.
- `lifecycleScope`: không được tìm thấy trong trang `architecture/coroutines` bản hiện tại; site dùng `repeatOnLifecycle` và `viewModelScope` (có nguồn) và không dựa vào `lifecycleScope` như khẳng định riêng.

## Sách (chỉ để lấy ý, không chép)

*Kotlin Coroutines: Deep Dive* (Moskała, bản 2023-06-26): A1 (suspension, under the hood), A2 (Job), A5 (Cancellation), A6 (Exception handling), A7 (Flow). Ý tưởng câu tự kiểm tra lấy chủ đề từ *Kotlin Exercises* (không chép). Sách ra trước Kotlin 2.4 nên mọi API đã được đối chiếu lại với tài liệu hiện hành ở trên.

## Checklist mục 6 (Track A) — đã tick 2026-11-21

| Mục | Ở đâu |
|---|---|
| 9 cặp khái niệm | A0 mục `pairs` (`track.coroutines.a0.sec.pairs.*`), mỗi cặp dẫn tới chương chi tiết |
| Không nói các hiểu lầm cấm (suspend = background, 1 coroutine = 1 thread, hủy = dừng ngay, CEH = try/catch, Flow luôn cold, IO bắt buộc, GlobalScope, async thay launch) | `misconceptions.{vi,en}.js` (11 mục, có nguồn); rà câu tuyệt đối vi/en 2026-11-21 |
| `withContext` không tạo coroutine detached | `m.full.co.withctx`, misconceptions |
| Không gộp các kiểu lan truyền lỗi; builder và supervisor boundary | model `coroutines.exception` (builder, CEH, ai ném), A6 `sec.rules`, A2 nhánh coroutineScope/supervisorScope |
| Dispatcher không gắn thread cố định; không hard-code số thread | `simp.sched`, select số luồng ở A1 (tham số minh họa), A4 |
| Rethrow `CancellationException`; ví dụ nuốt sai; giới hạn `finally`/`NonCancellable` | model `coroutines.cancel` (điều khiển `fin`, nhánh nuốt exception), `m.cancel.wrapup` |
| `withTimeout` ≠ `withTimeoutOrNull`; non-cooperative không dừng ngay | model `coroutines.cancel` (mode timeout/timeoutNull, coop) |
| cancelling / cancelled / completed tách biệt | model `coroutines.jobtree` (`simp.1` nêu điều kiện hiện `cancelling`) |
| `flowOn`, `catch` chỉ upstream; Flow không mô phỏng scheduler | A7 `sec.ops.p.3`, `m.flowpipe.simp.1` |
| Mã giả continuation có nhãn giản lược | A1 `sec.impl.badge = "impl simplified"` |
| Thời gian minh họa; race/thứ tự gắn nhãn minh họa | `simp.time`, `simp.sched`, `m.race.*` (interleaving minh họa) |
| Không có chiến lược concurrency luôn tốt nhất | `m.race.co.atomic` |
| Best practice gắn `guideline` + nguồn chính thức | A8 `sec.scopes.p.2`, `sec.bridge.p.3` (and-co-best, and-effects) |
| Phiên bản Kotlin, kotlinx.coroutines, Lifecycle | `shared/sources.js` (mục phiên bản), A8 `sec.bridge.p.2` |
| Badge "mô phỏng khái niệm" ở khu timeline | lõi hiển thị trên panel sơ đồ/timeline (đã chụp ảnh kiểm) |
| Hiểu lầm ≥ 8, có nguồn | 11 mục |

Cầu nối X2: nội dung đầy đủ ở A8 `sec.bridge` (vi/en); `shared/bridges.*.js` giữ tóm tắt 1–2 dòng cho nơi dẫn (B4, B8, C6).

## v2 · Bảng theo dõi nguồn theo chương

### U1 · Vì sao cần coroutine? (viết 2026-11-22)

**Đã đọc**
- *Kotlin Coroutines: Deep Dive*, chương "Why Kotlin Coroutines?", trang PDF 14–26. Trích text bằng `pdftotext`.
  - Các dòng gạch đầu dòng bị mất khi trích; nội dung của chúng được dựng lại từ ngữ cảnh của sách.
  - Hình updateNews/updateProfile (khoảng tr. 28) chưa xem dạng ảnh; chỉ dùng phần chú thích hình.
- Chưa đọc *Kotlin Coroutines by Tutorials* cho chương này.

| Claim | Nguồn | Loại |
|---|---|---|
| Chỉ luồng tạo cây view mới được sửa view; UI toolkit không thread-safe | `and-threads` (developer.android.com, Processes and threads) | API ổn định |
| Gọi mạng trên luồng Main ném `NetworkOnMainThreadException` | `and-nomain` (API reference) | API ổn định (với ứng dụng target từ Honeycomb trở lên) |
| ANR khi luồng Main không phản hồi sự kiện nhập trong khoảng 5 giây | `and-anr` | Hành vi hệ thống. Ngưỡng là số được tài liệu công bố, có thể đổi |
| `CalledFromWrongThreadException` khi sửa view từ luồng khác | kiến thức chung về Android, cùng nhóm với `and-threads` | **Chưa trích nguồn riêng** |
| Bốn cách giải (thread, callback, RxJava, coroutine), ví dụ tin tức, ba endpoint, progress bar, 100 000 luồng so với coroutine | Deep Dive tr. 15–25 | Ví dụ giảng dạy, đã viết lại |
| `async`/`await`; mặc định tuần tự | `kt-composing` | API ổn định |
| Stack luồng JVM mặc định thường 1 MB trên 64-bit, đặt bằng `-Xss` | Deep Dive tr. 25; tài liệu `java` launcher của Oracle (`-Xss`) | Phụ thuộc nền tảng; **URL Oracle chưa thêm vào sources.js** |
| `viewModelScope` dùng `Dispatchers.Main.immediate` | tài liệu AndroidX lifecycle-viewmodel-ktx | Chi tiết thư viện. **Chưa thêm nguồn/phiên bản**; cần thêm khi viết chương A8 v2 |
| Coroutine đang suspend lưu trạng thái trong continuation trên heap | Deep Dive (chương under the hood, sẽ đọc ở U4) | impl, đã gắn nhãn |

**Chưa xác minh**
- URL `https://leanpub.com/coroutines` của sách: viết theo trí nhớ, chưa mở lại.
- URL `and-threads`, `and-nomain`, `and-anr`: chưa mở lại trong phiên này. Đây là các trang chính thức quen thuộc nhưng cần đối chiếu URL đích.
- Chưa tìm cách giảng khác trên mạng cho chương này.

### U2 · Sequence builder (viết 2026-11-22)

**Đã đọc:** *Kotlin Coroutines: Deep Dive*, chương "Sequence builder", trang PDF 27–32. Trích bằng `pdftotext -enc UTF-8`, đọc toàn văn.

| Claim | Nguồn | Loại |
|---|---|---|
| Sequence tính lười, có thể vô hạn; `sequence { }` + `yield` | `kt-seq`; Deep Dive tr. 27–31 | API ổn định |
| Thứ tự in xen kẽ; iterator thủ công; Fibonacci; random | Deep Dive tr. 28–31; output đã tự suy ra từ ngữ nghĩa | Ví dụ, đã viết lại |
| `SequenceScope` có `@RestrictsSuspension`; chỉ được gọi `yield`/`yieldAll` | `kt-restricts`; Deep Dive tr. 32 (chú thích 8) | API ổn định. **Nội dung thông báo lỗi biên dịch ghi theo trí nhớ, chưa chạy thử** |
| Iterator của `sequence { }` đồng thời là continuation (`SequenceBuilderIterator`) | mã nguồn kotlin-stdlib `SequenceBuilder.kt` (theo hiểu biết, **chưa mở lại file ở phiên này**) | impl, đã gắn nhãn `impl` |
| Mỗi lần duyệt chạy lại khối; sequence không cache | ngữ nghĩa `Sequence` (`kt-seq`: sequence có thể duyệt nhiều lần, trừ khi bị ràng buộc một lần) | API ổn định |

**Sim `coroutines.seq` (mới):** lanes gồm main, khối sequence và một luồng; trục là thứ tự bước. Có hai bật/tắt: "gọi tới hết" và "Dùng List" (`buildList`). Có selfCheck.

**Chưa xác minh:** URL `kt-restricts` (dạng URL API mới của kotlinlang.org) chưa mở lại.

### U3 · Suspension hoạt động thế nào (viết 2026-11-22)

**Đã đọc:** *Kotlin Coroutines: Deep Dive*, chương "How does suspension work?", trang PDF 33–44. Đọc toàn văn.

| Claim | Nguồn | Loại |
|---|---|---|
| `suspendCoroutine` gọi lambda với continuation ngay trước khi suspend | `kt-suspendco`; Deep Dive tr. 34–35 | API ổn định |
| Resume ngay trong lambda thì không suspend thật (tối ưu) | Deep Dive tr. 35, chú thích 10 | impl, ghi là tối ưu |
| `Continuation` có `context` + `resumeWith(Result)`; `resume`/`resumeWithException` là extension (từ Kotlin 1.3) | `kt-continuation`; Deep Dive tr. 35–36 | API ổn định |
| Resume từ luồng khác trong `suspend fun main`: phần sau chạy trên luồng gọi resume; thứ tự Before, Suspended, After, Resumed | Deep Dive tr. 36 (output in sẵn); `suspend fun main` không có dispatcher | Hành vi; mô hình giữ đúng output của sách |
| `delay` tự viết bằng `ScheduledExecutorService`; `delay` thật từng được viết như vậy | Deep Dive tr. 37–39; `kx-delay` | Lịch sử và impl theo lời tác giả. Không khẳng định chi tiết bản hiện tại ngoài "dispatcher xử lý (interface `Delay`)" |
| `suspendCancellableCoroutine` + `invokeOnCancellation` | `kx-scc`; Deep Dive tr. 41 | API ổn định |
| Resume hai lần ném `IllegalStateException` ("Already resumed") | kiến thức về `SafeContinuation` (stdlib) | **Chưa đối chiếu nguyên văn thông báo lỗi ở phiên này** |
| Dispatcher (Main) chặn resume và chuyển continuation về luồng của nó | ContinuationInterceptor (kotlin.coroutines); sẽ trích nguồn ở chương Dispatchers | Cần thêm nguồn ở chương Dispatchers |

**Sim `coroutines.cont` (mới):** lanes gồm coroutine, luồng main, luồng phụ/scheduler. Có 5 chế độ resume. selfCheck kiểm: thứ tự After trước Resumed, After chạy trên luồng phụ; chế độ never không có After; chế độ now không suspend.

**URL đã kiểm (curl, 2026-11-22):** 10 URL nguồn mới của U1–U3 đều trả về 200. Trang ANR chuyển hướng sang `/topic/performance/issues/anr`, đã cập nhật.

### U4 · Coroutine dưới mui xe + hỗ trợ của ngôn ngữ so với thư viện (viết 2026-11-22)

**Đã đọc:** *Kotlin Coroutines: Deep Dive*, "Coroutines under the hood" và "Coroutines: built-in support vs library", trang PDF 45–64. Đọc toàn văn; hình minh hoạ bytecode chưa xem dạng ảnh.

| Claim | Nguồn | Loại |
|---|---|---|
| CPS: continuation là tham số cuối; kiểu trả về `Any?` vì có thể trả `COROUTINE_SUSPENDED` | `kt-design` (KEEP); Deep Dive tr. 45–46 | impl, ổn định về mặt thiết kế |
| State machine với `label`; đặt label trước lời gọi; cất và nạp biến cục bộ; `result` kiểu `Result` | Deep Dive tr. 46–56 (mã giản lược); `kt-design` | impl, giản lược, đã gắn nhãn |
| Chuỗi continuation thay call stack; ví dụ a/b/c, đáp án 13 Tick | Deep Dive tr. 56–58 (đáp án ở chú thích 16) | impl, giản lược |
| `BaseContinuationImpl.resumeWith` dùng vòng lặp thay đệ quy | Deep Dive tr. 59–60, trích Kotlin 1.5.30 | impl, có phiên bản |
| Chi phí suspend thấp | Deep Dive tr. 60–61 | Nhận định của tác giả |
| Ngôn ngữ (`kotlin.coroutines`) và thư viện (`kotlinx.coroutines`) | Deep Dive tr. 63–64; `kt-design` | API ổn định |
| Biến không dùng sau điểm suspend không được cất → "optimized out"; `-Xdebug` | kiến thức về compiler Kotlin | **Chưa đối chiếu tài liệu phiên bản**; nội dung đã ghi "kiểm tra đúng phiên bản" |
| Chế độ debug / `-ea` / khôi phục stack trace | `kx-debug` | API ổn định; **chưa trích nguyên văn điều kiện bật** |

**Sim `coroutines.sm` (mới):** dạng pipeline gồm người gọi, label 0/1/2 và continuation. Dải chỉ số hiện các trường. Có 3 tình huống. selfCheck đạt.

### Đối chiếu bổ sung U1–U4 (2026-11-22, sau khi viết)

Đã tải mã nguồn và tài liệu thật để đóng các mục "chưa xác minh" (raw.githubusercontent.com, nhánh master, ngày 2026-11-22):

| Mục | Kết quả |
|---|---|
| `SequenceBuilderIterator` (U2) | **Đúng**, có chỉnh câu chữ. `kotlin/libraries/stdlib/src/kotlin/collections/SequenceBuilder.kt`: lớp là `SequenceScope<T>(), Iterator<T>, Continuation<Unit>`; trường `nextStep`; `createCoroutineUnintercepted(receiver = iterator, completion = iterator)`; `SequenceScope` có `@RestrictsSuspension`. Đã sửa ghi chú U2 cho chính xác (iterator là completion của khối) |
| Vòng lặp `BaseContinuationImpl.resumeWith` (U4) | **Đúng.** `stdlib/jvm/src/kotlin/coroutines/jvm/internal/ContinuationImpl.kt`: `while (true)`, `probeCoroutineResumed`, `if (outcome === COROUTINE_SUSPENDED) return`, `releaseIntercepted()` |
| "Already resumed" (U3) | **Đúng.** `stdlib/jvm/src/kotlin/coroutines/SafeContinuationJvm.kt`: `throw IllegalStateException("Already resumed")` |
| Chế độ debug kotlinx (U4) | **Đúng**, đã sửa chi tiết. Tài liệu đã chuyển sang `kotlinlang.org/docs/coroutines-debugging.html`: chạy với assertion bật → tự bật debug mode (unit test mặc định bật); `-Dkotlinx.coroutines.debug`; debug mode bật stack trace recovery mặc định; tắt bằng `-Dkotlinx.coroutines.stacktrace.recovery=false`. Đã đổi URL `kx-debug` |
| "was optimized out" và `-Xdebug` (U4) | **Đúng**, có thêm cảnh báo. `kotlinlang.org/docs/debug-coroutines-with-idea.html` mục "Optimized-out variables": `-Xdebug` tắt tối ưu này; "Never use this flag in production: -Xdebug can cause memory leaks". Đã thêm nguồn `kt-debugidea` và cảnh báo vào U4 |
| Thông báo lỗi `@RestrictsSuspension` (U2) | **Chưa xác minh nguyên văn.** Đã bỏ phần trích nguyên văn, chỉ còn mô tả loại lỗi |
| `viewModelScope` dùng `Dispatchers.Main.immediate` (U1) | Còn mở. Sẽ trích nguồn AndroidX ở chương Dispatchers / A8 |
| `CalledFromWrongThreadException` (U1) | Còn mở. Chưa có trang chính thức riêng |


### A3 v2 · Coroutine builders (viết 2026-11-22)

**Đã đọc:** *Kotlin Coroutines: Deep Dive*, chương "Coroutine builders", trang PDF 66–81. Đọc toàn văn; hình sơ đồ tổng quan (tr. 80) chưa xem dạng ảnh.

| Claim | Nguồn | Loại |
|---|---|---|
| Builder là cầu nối; `suspend main` cũng được khởi động bằng builder | Deep Dive tr. 66, chú thích 18 | Diễn giải |
| `launch` trả `Job`; `async` trả `Deferred`, khởi động ngay; `runBlocking` chặn luồng tới khi xong | `kx-launch`, `kx-async`, `kx-runblocking` (URL đã kiểm, 200); Deep Dive tr. 67–74 | API ổn định |
| Chữ ký `launch`/`async`/`runBlocking` với `CoroutineScope` làm receiver | Deep Dive tr. 76; khớp tài liệu API (mặc định `EmptyCoroutineContext`, `CoroutineStart.DEFAULT`) | API ổn định |
| Bốn hệ quả của structured concurrency | Deep Dive tr. 77 | Tóm tắt, mỗi ý sẽ có chương riêng |
| `coroutineScope` tạo scope và chờ con | `kx-coroutinescope`; Deep Dive tr. 79 | API ổn định |
| Exception trong `async` lộ ra khi `await` | `kt-exceptions` (đã có từ v1) | API ổn định |
| `runBlocking` trên luồng Main gây đứng hoặc deadlock với `Dispatchers.Main` | Suy ra từ ngữ nghĩa `runBlocking` (chặn luồng) và dispatcher Main | **Suy luận, chưa có trang chính thức trích dẫn riêng** |
| Bài đoán output (start, L, A, end) | Tự suy từ ngữ nghĩa dispatch của `runBlocking` (một luồng, con chạy khi cha suspend) | **Chưa chạy thử thật** |

**Cách tích hợp:** viết sâu thêm vào A3, giữ id, sim `coroutines.builders` và mục v1 "when". `SEC_ORDER` trong generator sắp lại thứ tự mục; `override` thay tiêu đề, phần "bản chất" và goal g1.

### A4 v2 · Coroutine context (viết 2026-11-22)

**Đã đọc:** *Kotlin Coroutines: Deep Dive*, chương "Coroutine context", trang PDF 82–93. Đọc toàn văn.

| Claim | Nguồn | Loại |
|---|---|---|
| Context là tập có chỉ mục; mỗi Element cũng là context; key so sánh bằng tham chiếu; `get`, `+`, `minusKey`, `fold`, `EmptyCoroutineContext` | Deep Dive tr. 83–88; `kt-context` | API ổn định |
| Companion object `Key`; `Job` dùng chung key cho `Job`/`SupervisorJob` | Deep Dive tr. 85–86 | API ổn định |
| Mặc định chỉ thêm `Dispatchers.Default` (khi không có interceptor) và `CoroutineId` (debug) | Deep Dive tr. 90 | impl, ghi theo sách; **chưa đối chiếu `newCoroutineContext` ở phiên này** |
| Coroutine luôn tạo Job riêng; `Job` truyền vào làm cha → phá structured concurrency | Deep Dive tr. 90 (Job là ngoại lệ), sẽ đối chiếu ở chương Job | API ổn định |
| `ThreadLocal.asContextElement` | `kx-asctx` (URL đã kiểm, 200) | API ổn định |
| Đoán output `[c1]`, `[main]`, `Outer`/`Inner` | Deep Dive tr. 89–92 (output in sẵn trong sách) | Ví dụ của sách |

### A2 v2 · Job và chờ con (viết 2026-11-22)

**Đã đọc:** *Kotlin Coroutines: Deep Dive*, chương "Jobs and awaiting children", trang PDF 94–106. Đọc toàn văn; hình sơ đồ trạng thái (tr. 95) chưa xem dạng ảnh. Sơ đồ trạng thái dựng lại theo phần chữ của sách và tài liệu API `Job`.

| Claim | Nguồn | Loại |
|---|---|---|
| Sáu trạng thái và chuyển tiếp; bảng cờ isActive/isCompleted/isCancelled | Deep Dive tr. 95–97; `kx-job` (URL đã kiểm, 200) | API ổn định |
| Job không được thừa hưởng; Job truyền vào làm cha; `children`, `coroutineContext.job` | Deep Dive tr. 97–99 | API ổn định |
| `Job()` trả `CompletableJob`; `complete`, `completeExceptionally`, `Job(parent)`; `join` trên `Job()` chờ mãi | Deep Dive tr. 100–105; `kx-jobfn` | API ổn định |
| Lazy chưa start giữ cha ở Completing | Suy từ quy tắc "cha chờ mọi con" cộng trạng thái New | **Suy luận; chưa chạy thử** |
| Tên lớp `JobImpl`, `StandaloneCoroutine`, `LazyStandaloneCoroutine` trong `toString` | Deep Dive tr. 96 | impl, đã ghi "có thể khác giữa các phiên bản" |

**Sim mới `coroutines.jobstate`:** pipeline 6 trạng thái, token chạy dọc mũi tên chuyển tiếp. Có toggle lazy và chọn thời điểm hủy (none/active/completing). selfCheck đạt. A2 giờ có 2 tab sim; sim đặt sau mục "states".
