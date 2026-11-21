# Nguồn / Sources

Sinh tự động từ registry của site (dev/tools/sources-md.js). Generated from the site registry. Ngày đối chiếu / checked: 2026-11-20 … 2026-11-21.

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
  https://android.googlesource.com/platform/frameworks/support/+/refs/heads/androidx-main/compose/runtime/design/how-compose-works.md
  - vi: Composer, SlotTable (group, slot, gap buffer), restart group, gộp thao tác Applier. Nhánh androidx-main, đọc 2026-11-21; tài liệu tự cảnh báo vài chi tiết có thể đã cũ (B0, B2, B3, B6).
  - en: Composer, SlotTable (groups, slots, gap buffer), restart groups, merged Applier operations. androidx-main branch, read 2026-11-21; the document itself warns some details may be outdated (B0, B2, B3, B6).
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
- **Compose Runtime releases** — Android Developers · `version`
  https://developer.android.com/jetpack/androidx/releases/compose-runtime
  - vi: Chỉ dùng để xác định phiên bản (1.13.0 trong BOM 2026.11.01).
  - en: Used only to pin the version (1.13.0 in BOM 2026.11.01).

### Track C

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
- **Easing.kt (androidx-main)** — AndroidX (android.googlesource.com) · `impl`
  https://android.googlesource.com/platform/frameworks/support/+/refs/heads/androidx-main/compose/animation/animation-core/src/commonMain/kotlin/androidx/compose/animation/core/Easing.kt
  - vi: Điểm điều khiển cubic-bezier của các easing chuẩn; đọc 2026-11-21 (C2).
  - en: Cubic-bezier control points of the standard easings; read 2026-11-21 (C2).
- **FloatDecayAnimationSpec.kt (androidx-main)** — AndroidX (android.googlesource.com) · `impl`
  https://android.googlesource.com/platform/frameworks/support/+/refs/heads/androidx-main/compose/animation/animation-core/src/commonMain/kotlin/androidx/compose/animation/core/FloatDecayAnimationSpec.kt
  - vi: Công thức exponential decay, friction −4.2; đọc 2026-11-21 (C2, C6).
  - en: The exponential decay formula, friction −4.2; read 2026-11-21 (C2, C6).

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

## Sách (nguồn phụ, không chép) / Books (secondary, not copied)

Chỉ lấy ý tưởng và framework có ghi tên tác giả; không chép văn bản, mã, hình hay bài tập. Ideas and named frameworks only; no text, code, figures or exercises copied.

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

## Cảm hứng UX / UX inspiration

Hai trang mẫu chỉ là cảm hứng UX (bố cục, cách xem theo bước); site không sao chép mã, CSS, SVG, câu chữ hay ví dụ của chúng. The two sample sites are UX inspiration only; no code, CSS, SVG, wording or examples are copied. Xem trang Nguồn của site / see the site's Sources page.
