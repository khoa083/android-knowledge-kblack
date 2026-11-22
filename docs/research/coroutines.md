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

### A5 v2 · Hủy (viết 2026-11-22)

**Đã đọc:** *Kotlin Coroutines: Deep Dive*, chương "Cancellation", trang PDF 107–121. Đọc toàn văn.

| Claim | Nguồn | Loại |
|---|---|---|
| Ba hiệu ứng của `cancel()`; nguyên nhân phải là `CancellationException` | Deep Dive tr. 107–108; `kt-cancellation` | API ổn định |
| Race khi không `join`; `cancelAndJoin`; hủy nhóm bằng `Job()`/`cancelChildren` | Deep Dive tr. 108–111 | API ổn định |
| Hủy = ném `CancellationException` ở điểm suspend; `finally` chạy | Deep Dive tr. 111–112; `kt-cancellation` | API ổn định |
| Ở Cancelling: launch bị bỏ qua, suspend ném ngay; `withContext(NonCancellable)` | Deep Dive tr. 112–114; `kx-noncancellable` (URL 200) | API ổn định |
| `invokeOnCompletion` (cause null/CE/exception; `onCancelling`, `invokeImmediately`; gọi đồng bộ) | Deep Dive tr. 114–116 | API ổn định |
| `yield` / `isActive` / `ensureActive` | Deep Dive tr. 116–119 | API ổn định |
| `suspendCancellableCoroutine` + Retrofit | Deep Dive tr. 119–121; `kx-scc` | API ổn định |
| `runCatching` cũng nuốt `CancellationException` | Suy từ ngữ nghĩa `runCatching` (bắt mọi `Throwable`) | **Suy luận, chưa trích nguồn chính thức** |
| Bài đoán output (work 0, work 1, caught, after try, done) | Tự suy từ ngữ nghĩa trên | **Chưa chạy thử** |

### A6 v2 · Exception (viết 2026-11-22)

**Đã đọc:** *Kotlin Coroutines: Deep Dive*, chương "Exception handling", trang PDF 122–132. Đọc toàn văn; hình minh hoạ lan truyền chưa xem dạng ảnh.

| Claim | Nguồn | Loại |
|---|---|---|
| Lan truyền hai chiều; `runBlocking` ném lại lỗi | Deep Dive tr. 122–123; `kt-exceptions` | API ổn định |
| `try/catch` quanh `launch` vô dụng | Deep Dive tr. 123–124 | API ổn định |
| `SupervisorJob`: chỉ bảo vệ con trực tiếp; lỗi khi truyền vào một `launch` | Deep Dive tr. 124–127; `kx-supervisorjob` (URL 200) | API ổn định |
| `supervisorScope`; `withContext(SupervisorJob())` sai | Deep Dive tr. 127–129; `kx-supervisorscope` | API ổn định |
| `await` ném lại exception của `async` | Deep Dive tr. 130 | API ổn định |
| `CancellationException` không lan lên cha | Deep Dive tr. 131 | API ổn định |
| CEH không chặn lan truyền; chỉ dùng ở gốc hoặc con trực tiếp của supervisor; không dùng cho `async` | Deep Dive tr. 131–132 (phần đầu); `kx-ceh`, `kt-exceptions` (phần "chỉ ở gốc") | API ổn định |
| Bài đoán output supervisorScope (lỗi, Will be printed, Done) | Output in sẵn trong sách tr. 128 | Ví dụ của sách |

### SF · Coroutine scope functions (chương mới, viết 2026-11-22)

**Đã đọc:** *Kotlin Coroutines: Deep Dive*, chương "Coroutine scope functions", trang PDF 133–152. Đọc toàn văn.

| Claim | Nguồn | Loại |
|---|---|---|
| Vấn đề của `GlobalScope.async` và của việc truyền scope; ví dụ Twitter | Deep Dive tr. 133–137; `kx-globalscope` (URL 200) | API ổn định / ví dụ của sách |
| `coroutineScope` chạy tại chỗ, thừa hưởng context, ghi đè Job, chờ con, ném lại lỗi | Deep Dive tr. 137–141; `kx-coroutinescope` | API ổn định |
| Bảng so sánh builder và scope function; `runBlocking` ở đỉnh | Deep Dive tr. 141–143 | Tóm tắt |
| `withContext(EmptyCoroutineContext)` = `coroutineScope`; `async{}.await()` gần tương đương | Deep Dive tr. 143–144 | API ổn định |
| `supervisorScope` + `try/catch` ở `await`; `withContext(SupervisorJob())` sai | Deep Dive tr. 144–147 | API ổn định |
| `withTimeout`/`withTimeoutOrNull`; `TimeoutCancellationException` là `CancellationException`, không lan lên cha | Deep Dive tr. 147–150; `kx-withtimeout` (URL 200) | API ổn định |
| Việc phụ chạy trên scope riêng được inject | Deep Dive tr. 150–152 | Khuyến nghị của tác giả |
| Bug "withTimeout im lặng trong launch" | Suy ra từ ngữ nghĩa `CancellationException` (tr. 149) | Suy luận, khớp ví dụ của sách |

Chương mới id `sf`, đặt giữa A6 và A7, dùng lại sim `coroutines.builders` (đặt sau mục "cs"). Đã sửa câu dẫn sim ở SF và A3 cho khớp nhãn điều khiển thật.

### A4 v2 (phần 2) · Dispatchers (viết 2026-11-22)

**Đã đọc:** *Kotlin Coroutines: Deep Dive*, chương "Dispatchers", trang PDF 153–172. Đọc toàn văn. Mục Project Loom (JVM 19+, không áp dụng cho Android) chỉ nhắc qua, không viết thành mục.

| Claim | Nguồn | Loại |
|---|---|---|
| Default = số nhân (tối thiểu 2); `runBlocking` tự đặt dispatcher | Deep Dive tr. 153–154; `kx-dispatchers` | API ổn định |
| IO giới hạn 64 hoặc số nhân (lấy số lớn hơn); dùng chung pool với Default; `IO.limitedParallelism` có giới hạn độc lập, không bị chặn ở 64 | Deep Dive tr. 156–160; **đã đối chiếu nguyên văn tài liệu API `Dispatchers.IO`** ("64 threads or the number of cores (whichever is larger)"; ví dụ 64 + 100 + 60) | API ổn định |
| `limitedParallelism` có từ 1.6; executor dispatcher phải `close()` | Deep Dive tr. 154, 161–162 | API ổn định |
| Unconfined; `Main.immediate` | Deep Dive tr. 166–168 | API ổn định |
| `viewModelScope` dùng `Dispatchers.Main.immediate` | **mã nguồn AndroidX** `lifecycle-viewmodel/.../internal/CloseableCoroutineScope.kt` (androidx-main, đọc 2026-11-22; dòng 61) → nguồn `ax-vmscope`. **Đóng mục còn mở của U1** | impl, có nguồn |
| `ContinuationInterceptor`, `DispatchedContinuation` | Deep Dive tr. 168–170; `kt-interceptor` | Interface ổn định; `DispatchedContinuation` là impl |
| Bảng đo hiệu năng | Deep Dive tr. 170–172 | Số đo của tác giả; chỉ dùng các nhận xét, không chép bảng |
| Lỗi "Module with the Main dispatcher is missing" | Thông báo của kotlinx khi thiếu Main | **Ghi theo trí nhớ, chưa đối chiếu nguyên văn** |

**Sửa lõi CSS:** tiêu đề của khối hỏi–đáp có mã dài làm tràn 3px ở 360px; đã cho `overflow-wrap: anywhere` trong `summary > span`.

### A8 v2 (phần 1) · Tự dựng coroutine scope (viết 2026-11-22)

**Đã đọc:** *Kotlin Coroutines: Deep Dive*, chương "Constructing a coroutine scope", trang PDF 173–182. Đọc toàn văn.

| Claim | Nguồn | Loại |
|---|---|---|
| `CoroutineScope` là interface một thuộc tính; không nên cho lớp hiện thực nó | Deep Dive tr. 173–174 | Khuyến nghị của tác giả |
| `CoroutineScope(context)` thêm `Job()` nếu thiếu | Deep Dive tr. 174; `kx-scopefn` (URL 200) | API ổn định |
| BaseViewModel: Main + SupervisorJob + handler; `cancelChildren` | Deep Dive tr. 175–178 | Mẫu thiết kế |
| `viewModelScope` = SupervisorJob + Main.immediate; bản 2.4.0 dùng tag | Deep Dive tr. 178–179 (lifecycle 2.4.0); mã nguồn androidx-main `CloseableCoroutineScope.kt` (`ax-vmscope`) | impl, có phiên bản |
| Scope backend/analytics | Deep Dive tr. 180–182 | Mẫu thiết kế |
| Scope đã hủy: `launch` tạo coroutine bị hủy ngay, thân không chạy | Suy từ ngữ nghĩa Job (Job đã hủy không làm cha) và `CoroutineStart.DEFAULT` | **Suy luận; chưa chạy thử** |
| `backgroundScope` của `runTest` | kotlinx-coroutines-test | Sẽ đối chiếu ở chương Testing |

### A9 v2 (phần 1) · Trạng thái chung (viết 2026-11-22)

**Đã đọc:** *Kotlin Coroutines: Deep Dive*, chương "The problem with shared state", trang PDF 183–197. Đọc toàn văn.

| Claim | Nguồn | Loại |
|---|---|---|
| `UserDownloader` mất phần tử, có thể ném `ArrayIndexOutOfBoundsException`; `counter++` mất cập nhật | Deep Dive tr. 183–185 (số đo của tác giả, mỗi lần chạy khác nhau) | Ví dụ |
| `synchronized` đúng nhưng chặn luồng, không gọi được hàm suspend bên trong | Deep Dive tr. 185–186 | Nguyên tắc |
| Atomic: chỉ từng thao tác; `getAndUpdate` | Deep Dive tr. 186–188 | API Java ổn định |
| Dispatcher 1 luồng, thô và mịn | Deep Dive tr. 188–190 | Khuyến nghị của tác giả |
| `Mutex`: `withLock`; không reentrant (deadlock khi khoá lồng); không nhả khi suspend | Deep Dive tr. 190–195; `kx-mutex` (URL 200) | API ổn định |
| `Semaphore` để giới hạn đồng thời | Deep Dive tr. 195–197; `kx-semaphore` (URL 200) | API ổn định |
| `@Volatile` không làm `++` nguyên tử; `MutableStateFlow.update` so sánh-và-đặt | Kiến thức JVM/kotlinx | **Chưa trích nguồn riêng** (sẽ đối chiếu ở chương StateFlow) |
| `withContext` lồng với cùng dispatcher 1 luồng không deadlock | Suy từ ngữ nghĩa `withContext` (cùng dispatcher thì không dispatch lại) | **Suy luận; chưa chạy thử** |

### A9 v2 (phần 2) · Kiểm thử coroutine (viết 2026-11-22)

**Đã đọc:** *Kotlin Coroutines: Deep Dive*, chương "Testing Kotlin Coroutines", trang PDF 198–233. Đọc toàn văn.

| Claim | Nguồn | Loại |
|---|---|---|
| Fake/mock; `runBlocking` đủ khi không kiểm thời gian | Deep Dive tr. 198–200 | Khuyến nghị |
| `TestCoroutineScheduler`, `StandardTestDispatcher` (không tự đẩy thời gian), `advanceUntilIdle`, `advanceTimeBy` + `runCurrent`, `TestScope` | Deep Dive tr. 201–207; `kx-test` (URL 200) | API (từ 1.6; sách ghi lúc đó còn experimental) |
| `delay` dùng `Delay.scheduleResumeAfterDelay` của dispatcher test | Deep Dive tr. 205 | impl |
| `runTest`, `currentTime`; `backgroundScope` | Deep Dive tr. 208–213 | API |
| `currentCoroutineContext()` thay `coroutineContext` trong lambda lồng | Deep Dive tr. 214 | API |
| `UnconfinedTestDispatcher`; gần `runBlockingTest` cũ | Deep Dive tr. 216–217 | API |
| Inject dispatcher; `coroutineContext[ContinuationInterceptor]`; `EmptyCoroutineContext` | Deep Dive tr. 218–221 | Mẫu |
| Kiểm trạng thái giữa chừng; inject `TestScope`; 700 ms ảo | Deep Dive tr. 221–225 | Ví dụ |
| `setMain`/`resetMain`; "Module with the Main dispatcher is missing"; `MainCoroutineRule`/Extension | Deep Dive tr. 225–232. **Đóng mục còn mở ở A4: nguyên văn thông báo lỗi có trong sách** | API |
| Trạng thái "experimental" ở phiên bản hiện tại | **Chưa đối chiếu**; nội dung đã ghi "kiểm ở đúng phiên bản bạn dùng" | |

**Phần 2 của Coroutines v2 hoàn tất** (Builders → A3, Context + Dispatchers → A4, Job → A2, Hủy → A5, Exception → A6, Scope functions → SF, Tự dựng scope → A8, Shared state + Testing → A9).

### CH · Channel và select (viết 2026-11-22)

**Đã đọc:** Deep Dive tr. 235–262, toàn văn. Đã kiểm 3 URL API (`kx-channel`, `kx-produce`, `kx-select`: 200). Output của sim `coroutines.chan` khớp output in trong sách cho cả 5 chế độ (selfCheck). Sách sai một chỗ ở tr. 258: bản "dùng coroutineScope" in lại mã dùng `scope.async`; nội dung site trình bày đúng phiên bản `coroutineScope` + `cancelChildren`.

### FL · Flow từ gốc (viết 2026-11-22)

**Đã đọc:** Deep Dive "Hot and cold data sources" (tr. 263–270), "Flow introduction" (tr. 271–282), "Understanding Flow" (tr. 283–294), toàn văn.

| Claim | Nguồn | Loại |
|---|---|---|
| Nóng/lạnh; output list và sequence (m1…f16) | Deep Dive tr. 263–266 | Ví dụ của sách |
| Channel và Flow; "Flow started" mỗi lần collect | Deep Dive tr. 267–269 | Ví dụ của sách |
| Sequence chặn luồng, Flow thì không (ví dụ "Processing") | Deep Dive tr. 272–275 | Ví dụ của sách |
| Dựng Flow từ lambda; `map`/`filter`/`onEach`/`onStart` | Deep Dive tr. 283–291; `kt-flow` | impl giản lược; bản thật có `SafeCollector` (**chưa trích mã nguồn ở phiên này**) |
| Flow đồng bộ; trạng thái chung trong và ngoài bước flow | Deep Dive tr. 291–294 | Nguyên tắc |

### FB · Tạo flow và vòng đời (viết 2026-11-22)

**Đã đọc:** Deep Dive "Flow building" (tr. 295–306) và "Flow lifecycle functions" (tr. 307–317), toàn văn. Đã kiểm 3 URL API (`kx-channelflow`, `kx-callbackflow`, `kx-flowon`: 200).

| Claim | Nguồn | Loại |
|---|---|---|
| `flowOf`, `emptyFlow`, `asFlow` (collection, sequence, hàm suspend), Reactive Streams | Deep Dive tr. 295–298 | API |
| Phân trang: `flow` xong sau 6 s với 2 trang, `channelFlow` xong sau 5 s với 5 trang | Deep Dive tr. 300–303 (output in trong sách) | Ví dụ của sách; selfCheck của sim `coroutines.paging` khớp |
| `channelFlow` chạy trên `ProducerScope`, `launch` bên trong, `send` | Deep Dive tr. 302–304; `kx-channelflow` | API |
| `callbackFlow` ném IllegalStateException nếu khối kết thúc mà channel chưa đóng, nên phải `awaitClose` | `kx-callbackflow` (đã đọc nguyên văn tài liệu) ; Deep Dive tr. 304–306 | API |
| `onEach`/`onStart`/`onCompletion` (cả khi hủy)/`onEmpty` | Deep Dive tr. 307–310 | API + ví dụ của sách |
| `catch` chỉ bắt lỗi phía trên; lỗi trong `collect` không bị bắt; dời vào `onEach` | Deep Dive tr. 310–313 | Nguyên tắc |
| `flowOn` chỉ đổi context phía trên (ví dụ Name1/Name2/Name3); `launchIn`; mẫu Android | Deep Dive tr. 313–317; `kx-flowon` | API |
| "Flow invariant is violated" do `SafeCollector` kiểm context | Mã nguồn kotlinx.coroutines, `flow/internal/SafeCollector.common.kt` (nhánh master, đã kiểm 2026-11-22) | impl |

### FP · Xử lý flow (viết 2026-11-22)

**Đã đọc:** Deep Dive "Flow processing" (trang PDF 318–344), toàn văn. Đã kiểm 6 URL API (`kx-stateflow`, `kx-flatmapmerge`, `kx-flatmaplatest`, `kx-zip`, `kx-combine`, `kx-retrywhen`: 200) và mã nguồn `Combine.kt` (200).

| Claim | Nguồn | Loại |
|---|---|---|
| `map`/`filter`/`take`/`drop` và hiện thực `flow { collect { emit } }`; lần theo chuỗi 1–8 | Deep Dive tr. PDF 318–324 | Ví dụ của sách |
| `merge` không chờ; `zip` ghép một-một, xong khi một flow xong; `combine` thay giá trị, chạy tới khi cả hai xong | Deep Dive tr. PDF 324–329; `kx-zip`, `kx-combine` | Ví dụ của sách; selfCheck của sim `coroutines.combine` khớp output |
| zip collect flow thứ nhất tuần tự trong coroutine của nó, flow thứ hai trong `produce` rendezvous → flow1 phát ở 400/1400/2400 | Mã nguồn `zipImpl`, kotlinx.coroutines `common/src/flow/internal/Combine.kt` (nhánh master, đã đọc 2026-11-22) | impl; **suy luận thời điểm từ mã, sách chỉ in output** |
| `fold` terminal, `scan` trung gian, hiện thực `scan` | Deep Dive tr. PDF 329–333 | Ví dụ của sách |
| flatMapConcat/Merge/Latest, `concurrency` mặc định 16 (`DEFAULT_CONCURRENCY`) | Deep Dive tr. PDF 333–339; `kx-flatmapmerge` | Ví dụ của sách; selfCheck của sim `coroutines.flatmap` khớp output cả 4 chế độ |
| `retryWhen` giản lược, `retry`, output `12E12E12E12` | Deep Dive tr. PDF 339–342; `kx-retrywhen` | API + ví dụ |
| `distinctUntilChanged` và biến thể; terminal (`first`, `count`, `reduce`, `fold`) | Deep Dive tr. PDF 342–344 | Ví dụ của sách |
| Áp `distinctUntilChanged` lên StateFlow không có tác dụng | `kx-stateflow` (đã đọc nguyên văn tài liệu) | API |
| `scan` là reducer kiểu MVI/UDF; tìm kiếm `debounce` + `flatMapLatest` | Hiểu biết chung về kiến trúc Android | Ghi chú Android, **chưa gắn nguồn chính thức** |

### A7 · SharedFlow, StateFlow, shareIn, stateIn (viết lại 2026-11-22, giữ id `a7`)

**Đã đọc:** Deep Dive "SharedFlow and StateFlow" (trang PDF 345–358), toàn văn. Đã kiểm 5 URL mới (`kx-sharein`, `kx-statein`, `kx-whilesubscribed`, `kx-mutablesharedflow`, `and-stateprod`: 200).

| Claim | Nguồn | Loại |
|---|---|---|
| MutableSharedFlow phát cho mọi người collect; không đóng được; `replay`, `replayCache`, `resetReplayCache`; tách SharedFlow/FlowCollector | Deep Dive tr. PDF 345–349 | Ví dụ của sách |
| `tryEmit` chỉ trả false khi SUSPEND và có người collect; không ai collect thì giá trị bị bỏ (nếu không có replay) | `kx-mutablesharedflow` (tài liệu `tryEmit`, đọc nguyên văn) | API |
| `shareIn` và Eagerly/Lazily/WhileSubscribed; ví dụ WhileSubscribed (Started/Finished) | Deep Dive tr. PDF 349–353; `kx-sharein`, `kx-whilesubscribed` | Ví dụ của sách; selfCheck của sim `coroutines.sharein` chạy lại ví dụ này và khớp output |
| `stopTimeoutMillis` mặc định 0, `replayExpirationMillis` mặc định `Long.MAX_VALUE` | `kx-whilesubscribed` (đọc nguyên văn) | API |
| StateFlow: `value`, giá trị khởi đầu, conflation (X, C, E), so bằng equals | Deep Dive tr. PDF 354–356; `kx-stateflow` | Ví dụ của sách + API |
| `stateIn` suspend và dạng có `initialValue` | Deep Dive tr. PDF 356–358; `kx-statein` | Ví dụ của sách |
| `stateIn(viewModelScope, WhileSubscribed(5_000), …)` | `and-stateprod` (tài liệu Android, đọc nguyên văn ví dụ) | Hướng dẫn chính thức. **Lý do "sống qua xoay màn hình" là suy luận của site từ hành vi các chế độ, không trích từ tài liệu** |
| Kịch bản màn hình (1,2 / 3,6 / 4,3 / 6,6 / 12,4 / 14,8 s) | Của site, giả định | Minh hoạ |

Sách dùng `Lazily` cho ví dụ ViewModel; site trình bày cả hai và nói rõ nguồn của mỗi bên.
