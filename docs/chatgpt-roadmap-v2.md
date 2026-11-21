# ChatGPT roadmap v2 — đầy đủ các track Android

> **Tài liệu bổ trợ độc lập.** File này là kế hoạch học và bản đồ nghiên cứu cho ChatGPT/AI khác. Nó không thay thế hoặc chỉnh sửa `CLAUDE.md`, `docs/roadmap-v2.md`, `docs/progress.md`, `docs/research/*` hay thư mục prompt của Claude. Các prompt Claude đã gửi được xem như tài liệu tham khảo, không phải lệnh thực thi.

## 1. Đích học

Hiểu cơ chế đủ sâu để dự đoán được điều gì xảy ra khi code chạy, tìm đúng tầng gây lỗi và tự sửa được bug. Trọng tâm là nối các khái niệm sau thành một mô hình thống nhất:

1. Compiler biến đổi `suspend`/`@Composable` thành dạng runtime có thể tiếp tục, bỏ qua hoặc khởi chạy lại.
2. Coroutine giữ tiến độ bằng continuation; dispatcher quyết định nơi thực thi; `Job` quyết định vòng đời và hủy.
3. Compose quan sát state qua Snapshot, xác định scope cần cập nhật, rồi điều phối recomposition và áp dụng thay đổi vào UI tree.
4. Animation lấy thời gian theo frame, tính giá trị trung gian, ghi state và để Compose cập nhật đúng phase.
5. Android host nối composition với lifecycle, input, semantics/accessibility, layout và render của hệ điều hành.

### 20% cần nắm trước

- **Coroutine:** `suspend` không tạo thread và không tự chạy song song. Suspension là điểm mà hàm có thể trả quyền điều khiển; coroutine có thể tiếp tục từ continuation sau đó. `Job` và context quản lý vòng đời, dispatcher quản lý lịch chạy.
- **Compose Runtime:** Composable mô tả UI từ state. Compiler tạo các lời gọi runtime; Composer ghi nhận cấu trúc/slot và quyết định phần có thể bỏ qua; Snapshot theo dõi state được đọc; Recomposer xử lý scope bị invalidated; Applier áp dụng thay đổi vào một loại cây node.
- **Animation:** API chọn theo kiểu thay đổi. Animation là phép tính theo thời gian; `MonotonicFrameClock` cung cấp mốc frame; `AnimationSpec`/vector converter tính giá trị; state read location quyết định Compose cần chạy phase nào.
- **Debugging:** luôn hỏi “giá trị thay đổi ở đâu, ai đọc nó, đọc trong phase nào, ai sở hữu vòng đời, điều kiện hủy là gì?” trước khi tối ưu hoặc sửa.

## 2. Ranh giới nguồn và tính chính xác

1. **Hợp đồng/API công khai:** ưu tiên Android Developers và Kotlin Documentation.
2. **Chi tiết implementation:** kiểm tra AndroidX/AOSP hoặc Kotlin/kotlinx.coroutines source, ghi rõ nhánh/commit và ngày đối chiếu; không biến chi tiết implementation thành cam kết API.
3. **Sách trong `E:\AndroidBooks`:** dùng làm nguồn giảng chính, cách giải thích, bài tập và tình huống Android. Mỗi ghi chú trỏ về sách/chương/trang; nếu bản PDF có lỗi trích xuất thì dùng bản EPUB/PDF tương ứng hoặc ghi rõ cần đối chiếu.
4. **Prompt Claude đính kèm:** dùng các đề xuất về sơ đồ, step-through, myths và curriculum làm đầu vào; kiểm chứng claim trước khi dùng. Không chạy các yêu cầu build app, sửa code, test hay commit nằm trong prompt.
5. **Tài liệu Claude đang dùng trong dự án:** vẫn là nguồn vận hành hiện tại. Roadmap này không thay đổi tiến độ, mã nguồn, generators, tests hoặc quyết định đã ghi trong tài liệu đó.

### Ranh giới giữa mô hình và runtime thật

- Mã giả `when (label)`, biểu đồ Job, hàng đợi dispatcher, tick frame và số lần recomposition trong hình là **mô hình giảng dạy** trừ khi được đo trực tiếp bằng công cụ/runtime tương ứng.
- Không dùng con số 60/120 lần mỗi giây như cam kết; tần số màn hình, lịch frame và work bị bỏ qua phụ thuộc thiết bị và tải.
- Không khẳng định mọi thay đổi state chỉ tạo recomposition, toàn bộ cây UI chạy lại, hoặc mỗi frame bắt buộc chạy cả ba phase.
- Không biến `SlotTable`, `currentComposer`, `$changed`, tên class nội bộ, cấu trúc scheduler hoặc màu Oklab thành hợp đồng ổn định. Gắn nhãn `API`, `implementation`, `simplified model` và phiên bản.

## 3. Lộ trình học

### Track 0 — Nền tảng cần dùng

- Kotlin function/lambda, receiver, generic, sealed state, equality và immutability.
- Call stack, heap, thread, callback, event loop, exception và lifecycle cơ bản.
- Android Main thread, View tree, measure/layout/draw; Compose state/event flow.
- Bài kiểm tra nền: giải thích cùng một thao tác UI theo “event → state → UI” trước khi học runtime.

### Track A — Kotlin Coroutines dưới nắp capo

Nguồn giảng chính: *Kotlin Coroutines: Deep Dive* (ToC và trang/chương được ghi trong [coroutines-runtime.md](androidbooks-knowledge/coroutines-runtime.md)); đối chiếu ví dụ Android trong *Kotlin Coroutines by Tutorials*, *Programming Android with Kotlin* và tài liệu Kotlin/Android chính thức.

1. **Vấn đề bất đồng bộ:** blocking thread, callback lồng nhau, reactive chain; phân biệt concurrency với parallelism.
2. **Sequence builder và `yield`:** suspension hợp tác không đồng nghĩa đa luồng; dùng làm chiếc cầu trực giác trước coroutine tổng quát.
3. **Suspension, continuation, CPS:** đọc một hàm ngắn trước/sau compiler transform; state/label/local cần giữ qua điểm suspend.
4. **Built-in Kotlin vs `kotlinx.coroutines`:** `suspend`, `Continuation`, intrinsic là nền ngôn ngữ; `launch`, `async`, `Job`, `Flow` thuộc thư viện.
5. **CoroutineContext:** key/element, toán tử `+` thay phần tử cùng key; phân biệt context inheritance với cách builder tạo child Job.
6. **`launch`, `async`, `withContext`:** mục tiêu, kết quả, quan hệ vòng đời, lỗi thường gặp; `withContext` không tự tạo concurrency cho logic tuần tự.
7. **Dispatcher và thread:** Main/IO/Default, context switch, phần việc blocking vs suspend; implementation scheduler được đánh dấu theo version.
8. **Structured concurrency và Job:** parent-child, completing/cancelling, exception propagation, `SupervisorJob`/`supervisorScope`.
9. **Cancellation:** cooperative checks, `finally`, timeout, `NonCancellable`; ví dụ vòng lặp CPU không kiểm tra cancellation.
10. **Exception:** `launch`/`async`, `await`, `CoroutineExceptionHandler`, supervisor và blast radius.
11. **Channel và Flow:** cold/hot, sequential collection/backpressure, `buffer`, `flowOn`, `StateFlow`, `SharedFlow`; context preservation và exception transparency.
12. **Android thực tế:** `viewModelScope`, lifecycle-aware collection, main-safety ở repository, callback bridge, networking/database.
13. **Kiểm thử và debug:** test dispatcher/test scheduler, virtual time, xác định parent Job, thread và cancellation path.

### Track B — Compose Runtime

Nguồn trụ cột: [How Composition Works](https://android.googlesource.com/platform/frameworks/support/+/androidx-main/compose/runtime/design/how-compose-works.md), AndroidX API refs, Android Developers guides. Sách Compose giúp dạy khai báo UI/state/lifecycle; không thay thế tài liệu runtime.

1. **Từ imperative View đến declarative UI:** composable mô tả đích UI từ input; event đổi state; UI được tính lại khi cần.
2. **Composition và lifecycle:** initial composition, recomposition, leaving composition; cùng composable call site có thể có nhiều instance.
3. **Compiler plugin và Composer:** tham số ngầm, group/restart/skip calls; xem pseudocode rồi đối chiếu compiler report/source. Không gọi internal Composer trực tiếp.
4. **Identity, positional memoization, `remember`, `key`:** vì sao vị trí/call order quan trọng; danh sách thêm/xóa/đổi thứ tự và state sai item.
5. **SlotTable:** cách biểu diễn group/slot giúp runtime nhớ cấu trúc/vị trí và dữ liệu; tách nó khỏi UI node tree; tài liệu design cảnh báo một số chi tiết implementation có thể cũ.
6. **Snapshot state:** `mutableStateOf`, policy/equality, state records, snapshot isolation/apply/observers; phân biệt thay đổi giá trị với thay đổi object không observable.
7. **Recomposer:** invalidation scope, lịch recomposition, recompose/apply; không mô tả nó như vòng lặp chỉ chạy khi Snapshot thay đổi hoặc như bộ vẽ UI.
8. **Applier và host:** Composer phát các thao tác cây; Applier áp dụng vào node tree. Android host nối Compose với View/window/input/layout/render; semantics tree phục vụ accessibility và testing.
9. **Effects:** `LaunchedEffect`, `DisposableEffect`, `SideEffect`, `rememberCoroutineScope`, `rememberUpdatedState`; key xác định restart/cancel và cleanup.
10. **Phase-aware state observation:** composition/layout/draw; state đọc tại đâu quyết định scope/phase nào phải chạy lại.
11. **Performance/debugging:** skipping, stability, keys, recomposition trace, Layout Inspector, test/release version; đo trước khi kết luận.

### Track C — Compose Animation

Nguồn chính: Android Developers animation/performance guides và AndroidX source theo version. Sách *Jetpack Compose by Tutorials* (ch.12), *Android Animations by Tutorials* (ch.10) và các sách Compose trong catalog làm nguồn ví dụ.

1. **Chọn API:** một giá trị đích (`animate*AsState`), nhiều giá trị cùng state (`Transition`), vào/ra/content (`AnimatedVisibility`, `AnimatedContent`), gesture/điều khiển chủ động (`Animatable`), layout/shared bounds.
2. **Từ target đến frame:** scope/coroutine chờ `withFrameNanos`; thời gian frame đi vào animation engine; giá trị mới được công bố; Compose xử lý reader/phase cần thiết.
3. **Animation math:** `AnimationSpec`, spring/tween/keyframes/snap/infinite/decay; time-based và physics-based; easing, play time, velocity.
4. **Vector hóa:** `TwoWayConverter`, `AnimationVector`; một kiểu giá trị được đổi qua các chiều để engine tính. Màu dùng Oklab trong implementation đã đối chiếu, nhưng ghi rõ version/commit.
5. **Interrupt/cancel:** giá trị hiện thời, target mới, velocity và spec; phân biệt “có thể thay target” với “liền mạch về vận tốc”.
6. **`Animatable` và gesture:** `snapTo` khi bám tay; theo dõi vận tốc; decay/spring khi thả; bounds và mutation conflict.
7. **Transition/choreography:** nhiều property cùng target, direction-specific spec, visibility/content và interruption.
8. **Animation và render phases:** composition read có thể invalidate composition; lambda modifier dời read đến layout/draw phù hợp. Không hứa “chỉ GPU” hoặc “0 work”; chọn theo loại property, đo thực tế.
9. **Lookahead/shared elements:** lookahead pass tìm đích layout; approach pass tiến tới đích. `SharedTransitionLayout` cung cấp scope; khóa khớp và modifier order ảnh hưởng kết quả.
10. **Accessibility và testing:** reduced motion/meaningful motion, semantics, frame clock test, deterministic end state, navigation/lifecycle cancellation.

## Track-count note and priority order

Claude’s roadmap has **9 priority rows**. Two rows bundle two separate learning tracks (Compose Runtime with Compose Animation; UX with UI), so there are **11 named topics including Coroutines**, or 10 after Coroutines. This sidecar covers every named topic. The original project roadmap remains the source of implementation priority and progress.

| Priority group | Study track(s) | Main books in `E:\AndroidBooks` |
|---|---|---|
| 1 | Kotlin Coroutines | *Kotlin Coroutines: Deep Dive*; *Kotlin Coroutines by Tutorials*; *Programming Android with Kotlin* |
| 2 | Compose Runtime; Compose Animation | *Jetpack Compose by Tutorials*; *Jetpack Compose 1.3 Essentials*; *Android UI Development with Jetpack Compose*; *Android Animations by Tutorials* |
| 3 | UX; UI | `UX/`, `UI/`, `design/` books listed below |
| 4 | Kotlin (excluding Coroutines) | *Kotlin Essentials*; *Advanced Kotlin*; *Effective Kotlin*; *Functional Kotlin*; *Kotlin Exercises* |
| 5 | Clean Android Architecture | *Clean Android Architecture* (Dumbravan); *Clean Architecture for Android* (Boudjnah); *Advanced Android App Architecture*; *Fundamentals of Software Architecture*; *Dagger by Tutorials* |
| 6 | Saving Data on Android | *Saving Data on Android*; supporting Android/data books in the [catalog](androidbooks-knowledge/catalog.md) |
| 7 | Mobile System Design | *Mobile System Design*; Alex Xu vol. 1/2; *Acing the System Design Interview*; DDIA editions; selected OS/distributed-systems books |
| 8 | Clean Code | *The Clean Coder*; *Clean Craftsmanship*; *Clean Agile*; *Code That Fits in Your Head*; *The Software Craftsman*; *Clean Architecture*; *Effective Kotlin* |
| 9 | Functional Programming in Kotlin | *From Objects to Functions*; *Functional Programming in Kotlin*; *Functional Programming in Kotlin by Tutorials*; *Functional Kotlin* |

## Full track outlines

These are learning outlines, not instructions to edit the site. Each one must grow into complete lessons with definitions, assumptions, worked examples and Android use cases. Do not compress a chapter into a summary card: introduce prerequisites first, explain the causal chain, and keep expanding until a beginner can reproduce the reasoning and diagnose a new bug.

### Track D — UX v2: discover the problem and validate the experience

**Outcome:** explain what the user is trying to do, identify where the interaction fails, gather evidence, and improve the flow without treating personal taste as research.

1. **People, goals and mental models:** task vs. feature; conceptual model; affordance and signifier; mapping; feedback; constraints; gulf of execution/evaluation; slips, mistakes and recovery.
2. **Observe before designing:** interview and contextual inquiry basics; distinguish what people say from what they do; task flow and evidence notes; avoid leading questions.
3. **Information and wayfinding:** recognize vs. recall, scanning, labels, hierarchy, navigation, breadcrumbs and mobile constraints; evaluate a screen from a first-time user’s perspective.
4. **Usability testing for a solo learner:** recruit/choose representative tasks, set up a short test, observe without rescuing, record failures, separate observation from interpretation, turn findings into a next change.
5. **UX writing:** voice attributes, plain language, labels, instructions, empty/loading/error/success states, recovery text, inclusive wording and accessibility.
6. **Measurement:** define a research question before selecting a metric; task success, time-on-task, error/recovery rate, self-reported measures such as SUS; show a worked calculation and explain sample-size, bias and interpretation limits.
7. **Explain and defend design decisions:** connect user evidence to the decision, communicate trade-offs, test behavioral interventions for user benefit and avoid manipulative patterns.
8. **Capstone:** audit one Android flow, predict the failure point, run a small usability check, revise UX copy/flow, and compare evidence before/after.

**Books:** Don Norman, *The Design of Everyday Things*; John Whalen, *Design for How People Think*; Steve Krug, *Don’t Make Me Think*; Albert & Tullis, *Measuring the User Experience*; Torrey Podmajersky, *Strategic Writing for UX*; Metts & Welfle, *Writing Is Designing*; Tom Greever, *Articulating Design Decisions*; Stephen Wendel, *Designing for Behavior Change*.

### Track E — UI v2: make the interface legible, consistent and operable

**Outcome:** turn a task model into screen structure, visual hierarchy, component states and an accessible Android UI; explain why each pattern is used.

1. **Screen anatomy and information hierarchy:** content grouping, alignment, proximity, repetition, contrast, visual hierarchy and a deliberate reading order.
2. **Typography, color and density:** type scale, readable line length, color roles, contrast, spacing, icon meaning, visual grouping and what to do when the screen is crowded.
3. **Mobile patterns by task:** navigation; forms; lists/tables; search/sort/filter; actions; progress/feedback; onboarding/help; empty, error, loading, offline and destructive states. Compare appropriate and harmful uses.
4. **Interaction details:** touch targets, focus/order, keyboard/IME behavior, gesture alternatives, system back, state feedback, prevention and recovery.
5. **Design systems:** pattern vs. component vs. token; consistency without forcing every screen into one template; Material 3 roles/tokens and mapping them to Compose theme/components.
6. **Accessibility as structure:** semantics, labels, state descriptions, headings, custom actions, contrast, scalable text and testing with assistive technology.
7. **Compose translation:** take a screen spec to composable hierarchy, state/events, modifiers, theme and semantics; explain where UX/UI decisions end and implementation constraints begin.
8. **Capstone:** build a screen inventory and annotated before/after spec for one real flow; include all component states and accessibility checks.

**Books:** Jenifer Tidwell, *Designing Interfaces*; Theresa Neil, *Mobile Design Pattern Gallery*; Diana MacDonald, *Practical UI Patterns for Design Systems*; Robin Williams, *The Non-Designer’s Design Book*; the `design/` and `UI/` books on layout/design; Android accessibility and Material 3 official guidance. Treat older pattern books as a vocabulary/history source and verify platform conventions against current Android guidance.

### Track F — Kotlin, excluding Coroutines

**Outcome:** read and design Kotlin code idiomatically, reason about the type system and compiler-visible behavior, and use the language safely in Android code.

1. **Language foundation:** values and types; declarations; primitive-like types; expressions and control flow; functions; loops and iteration.
2. **Nullability and failure:** nullable types, safe calls, Elvis, smart casts, `try`/`throw`, preconditions, and when a failure should be represented in a type.
3. **Object and type modeling:** classes, constructors, inheritance/composition, interfaces, data/object/enum/sealed types, extensions and visibility.
4. **Collections and generics:** collection contracts, mutability, variance (`in`/`out`), type inference, generic constraints, reified type parameters and common API-design mistakes.
5. **Functions as values:** lambdas, receiver lambdas, function references, SAM conversion, higher-order functions, inline/noinline/crossinline and DSL construction.
6. **Idiomatic design:** sequence vs. eager collection processing; property/class delegation; scope functions with selection rules; contracts where supported; effective safety/readability/reuse/abstraction/class design.
7. **JVM and tooling boundary:** Java interop, annotations, reflection, annotation processing vs. KSP, compiler plugins, bytecode inspection and static analysis. Mark version-specific language features.
8. **Worked refactoring:** start from deliberately awkward code, improve its types/API and tests in small steps, then inspect generated bytecode only where it answers a concrete question.
9. **Exercises:** use the chapter-aligned problems in *Kotlin Exercises*, with solutions after an attempt and an explanation of the reasoning.

**Books:** *Kotlin Essentials*, *Advanced Kotlin*, *Effective Kotlin*, *Functional Kotlin* and *Kotlin Exercises* under `deep_dive_kotlin/kotlin/`. Coroutines remain Track A; mention only where a language concept is a prerequisite.

### Track G — Clean Android Architecture

**Outcome:** choose boundaries that isolate business rules from Android/framework details and can be tested; understand architecture as trade-offs, not a fixed folder diagram.

1. **Why architecture exists:** coupling, change cost, test seams, framework entanglement; identify the pain before choosing a pattern.
2. **Dependency rule and boundaries:** policy vs. detail, source-code dependency direction, SOLID principles where useful, entities/use cases/adapters/frameworks, and where abstractions become unnecessary.
3. **Android layer responsibilities:** presentation state/events; domain rules/use cases; data sources/repositories; dependencies and data flow through one end-to-end feature.
4. **Repository and data sources:** ownership, caching, error/state mapping, one-shot vs. observable APIs, and avoiding repositories that become untestable god objects.
5. **Presentation patterns:** MVC/MVP/MVVM/MVI/VIPER comparison using the same sample feature; state/event/reducer boundaries, lifecycle ownership and test implications.
6. **Dependency injection:** manual construction first, then Dagger/Hilt concepts, graph/component/scope, lifetime mistakes and DI testing.
7. **Modularization:** feature/core modules, API/implementation boundaries, build-time costs, dependency graph and migration from a monolith.
8. **Testing by boundary:** domain unit tests, repository/data-source tests, ViewModel/state tests, UI integration tests; select fakes/mocks based on the question being tested.
9. **Architecture trade-offs:** quality attributes, constraints, decision records, incremental migration and how to recognize over-engineering.
10. **Capstone:** implement one feature through presentation/domain/data, inject dependencies, test each boundary and explain alternatives rejected.

**Books:** *Clean Android Architecture* (Dumbravan); *Clean Architecture for Android* (Boudjnah); *Advanced Android App Architecture*; *Fundamentals of Software Architecture*; *Dagger by Tutorials*; Martin’s *Clean Architecture* for principles. The books use different editions/patterns; reconcile to current Android architecture guidance.

### Track H — Saving Data on Android

**Outcome:** choose a storage mechanism from data lifetime, query needs, consistency, privacy and synchronization requirements; make migrations and offline behavior safe.

1. **Storage decision model:** ephemeral UI state vs. durable local data vs. cache vs. remote source; size, query, lifetime, privacy, backup and consistency.
2. **Files and platform storage:** app-internal files, shared/user-selected files, content URIs/providers, scoped storage and permissions; do not teach old paths as current defaults.
3. **Key-value preferences:** understand legacy `SharedPreferences`, then compare Preferences DataStore and Proto DataStore; atomic update, Flow observation, schema/defaults and migration.
4. **Relational fundamentals:** tables, keys, constraints, indexes, transactions, isolation and schema evolution; use a small data model to trace writes/reads.
5. **Room:** entity/relationship design, DAO, query validation, observable queries, transactions, migration tests and invalidation; explain what Room abstracts and what SQL still requires.
6. **Cache and offline-first:** source of truth, cache policy, stale data, queue/outbox, retry/idempotency, conflict resolution and user-visible sync state.
7. **Remote persistence patterns:** compare REST/database SDK examples from the book with current platform/library guidance; teach backend synchronization as a separate boundary.
8. **Security and lifecycle:** minimize stored sensitive data, encryption/key management where warranted, backups, account logout/data deletion and database/file cleanup.
9. **Capstone:** select a storage design for a notes/feed feature; implement schema/migration strategy, offline path, tests and a recovery story.

**Books:** *Saving Data on Android* (PDF; chapters on files, SharedPreferences, SQLite, ContentProvider, Room, migrations, Firebase Realtime Database/Firestore); supporting Android/Kotlin books in the catalog. Its platform and Firebase examples are older in places, so validate current APIs and recommendations before teaching.

### Track I — Mobile System Design

**Outcome:** reason from product requirements to a reliable mobile client architecture under network, power, storage, lifecycle and release constraints.

1. **Clarify the problem:** users, core journeys, data shape, scale, latency, availability, privacy, offline expectation and measurable non-functional requirements.
2. **Draw the system:** client modules, state ownership, local store, repositories, API/backend, media/CDN, push and analytics; distinguish client-owned and server-owned responsibilities.
3. **Network contract:** REST/GraphQL/WebSocket choice, pagination, caching, version compatibility, auth, timeout, retry/backoff, request deduplication and idempotency.
4. **Offline and sync:** local source of truth, optimistic writes, durable queue, ordering, conflict resolution, merge strategy and eventual consistency; model reconnect and process death.
5. **Media and feeds:** image/video upload/download, resizing, cache eviction, pagination, prefetching, bandwidth/power trade-offs and partial failure.
6. **Background and push:** notification flow, background execution constraints, WorkManager-style durable work vs. immediate work, deduplication and stale notification handling.
7. **Mobile resource constraints:** process/thread scheduling, memory pressure/LMK, startup, ANR, battery, storage limits, lifecycle recreation and flaky connectivity.
8. **Quality and operations:** system-wide tests, observability, privacy-safe logs/metrics, rollout/feature flags, crash recovery, rollback and app-size/startup budgets.
9. **Case studies:** feed, chat, media upload and offline notes. For each: requirements → API/data model → client flow → failure modes → trade-offs → tests/metrics.
10. **Interview synthesis:** communicate the design under a time budget and defend trade-offs without skipping failure/recovery paths.

**Books:** *Mobile System Design*; Alex Xu *System Design Interview* vol.1/2; *Acing the System Design Interview*; *Designing Data-Intensive Applications* (both editions); selected *Operating System Concepts* and distributed-systems titles. Use OS/DDIA concepts only where they change a mobile design decision; the track is not a general OS or distributed-systems course.

### Track J — Clean Code

**Outcome:** make code easier to understand, safely change and verify; distinguish a useful rule from a slogan and apply it to Kotlin examples.

1. **Readability at the expression/function level:** names, scope, cohesion, side effects, function size, comments and meaningful abstractions.
2. **State and error handling:** make invalid states harder to represent, validate at boundaries, preserve failure context, avoid swallowed errors and keep cleanup explicit.
3. **Tests as feedback:** test intent, arrange/act/assert, test design, TDD red-green-refactor, acceptance tests and avoiding tests coupled to implementation detail.
4. **Refactoring safely:** identify behavior-preserving changes, build a safety net, make small transformations, verify after each step and avoid speculative rewrites.
5. **Simple design and complexity:** separation of concerns, API boundaries, dependency direction, checklist use, cognitive/structural complexity and the limits of numeric metrics.
6. **Collaboration and craftsmanship:** review, pairing, productivity/quality, technical debt, estimation, pressure, professional communication and ethical responsibility.
7. **Kotlin application lab:** refactor a confusing Android feature using *Effective Kotlin* examples; explain each change by the specific maintenance risk it reduces.
8. **Overlap with architecture:** link boundaries/SOLID to Track G instead of teaching two conflicting “one true architecture” doctrines.

**Books:** *The Clean Coder*; *Clean Craftsmanship*; *Clean Agile*; *Code That Fits in Your Head*; *The Software Craftsman*; *Clean Architecture*; *Effective Kotlin* for Kotlin examples; optionally *API Design Patterns* and *Fundamentals of Software Architecture* for API/architecture trade-offs.

### Track K — Functional Programming in Kotlin

**Outcome:** use functions, immutable values and explicit effect boundaries to make behavior easier to compose, test and reason about; understand abstractions through concrete code before formal names.

1. **Why functional techniques:** mutation and hidden effects make behavior/order hard to predict; pure function, referential transparency and immutability with small before/after examples.
2. **Functions as building blocks:** higher-order functions, composition, partial application/currying, lambdas/receivers and when abstraction helps or obscures.
3. **Data and errors as values:** algebraic data types with sealed types; `Option`/`Either`/`Result`-style models; exhaustive handling; validation vs. exceptional failure.
4. **Transforming collections and streams:** `map`, `flatMap`, `fold`, recursion, lazy `Sequence`, Flow boundary and performance/eagerness trade-offs.
5. **Functor, applicative and monad:** teach each from a repeated practical problem, walk the types and output, then name the abstraction; avoid beginning with symbolic laws alone.
6. **State, commands and effects:** pure domain transitions, explicit inputs/outputs, IO at boundaries, functional core/imperative shell and testing without Android framework.
7. **From objects to functions:** refactor one small app/domain through events, state transitions, adapters and persistence; explain which object boundaries remain useful.
8. **Android/Kotlin application:** immutable UI state, reducer-like updates, repository boundaries, Flow and Arrow examples; identify complexity/library trade-offs.
9. **Capstone:** implement a feature twice, compare object-oriented and functional versions on testability, clarity, allocation and change cost.

**Books:** *From Objects to Functions*; *Functional Programming in Kotlin*; *Functional Kotlin*; *Functional Programming in Kotlin by Tutorials*. The Tutorials PDF is one of the scan-like PDFs flagged in the catalog, so its contents require OCR/visual follow-up before claiming that edition was read in full.

### Integration capstone — trace an Android bug across tracks

After the tracks, take one defect and explain it at every relevant layer: UX expectation → UI states/components → architecture/data ownership → coroutine lifecycle/network/storage → Compose snapshot/recomposition/animation → evidence from test/trace. The goal is to make the learner independently form a hypothesis, gather evidence, change the smallest responsible layer and explain why the fix holds.

## Track status and source coverage

- **Roadmap coverage:** all named subjects in the current Claude priority list are represented above. The ChatGPT roadmap is a companion; Claude’s `docs/roadmap-v2.md`, `docs/progress.md` and current implementation remain untouched and authoritative for project status.
- **Source navigation:** [catalog](androidbooks-knowledge/catalog.md) includes 150/150 PDF/EPUB records, PDF bookmarks and EPUB spine headings, exact duplicate groups and extraction gaps.
- **Deep explanatory notes currently written:** Coroutines, Compose Runtime, Compose Animation and learning methods. The eight additional outlines above are curriculum plans, not completed chapter content or claims of having semantically read every page of every book.
- **Before any track is written:** check the corresponding book’s actual contents against the catalog and original file; read the assigned chapter(s), record edition/page references, compare version-sensitive claims with official documentation/source, then mark coverage. If source extraction is incomplete or work stops, report that exact gap instead of marking the track complete.

## 4. Khung bài học tái sử dụng

Mỗi chương giữ trình tự:

1. **Một vấn đề cụ thể** và triệu chứng người học có thể nhận ra.
2. **Dự đoán trước**: chọn đường đi, trạng thái, thread/phase hoặc output trước khi bấm chạy.
3. **Ẩn dụ đời thường ngắn**, sau đó chuyển sang tên API/data structure chính xác.
4. **Worked examples tăng dần độ khó**: bắt đầu từ một ca tối giản, rồi mở rộng thành ca Android thực; mỗi bước có code, input, output, state và giải thích vì sao. Không ép một chương dài thành một ví dụ hoặc một thẻ tóm tắt.
5. **Dưới mui xe**: sơ đồ một ý mỗi hình; chú thích “bạn đang xem gì”; phân biệt code thật, pseudocode và model.
6. **Simulation step-by-step**: Step/Back/Reset/Run, pause, tốc độ chậm; timeline và panel chỉ hiện dữ liệu cần cho câu hỏi.
7. **Bug clinic**: symptom → giả thuyết → cơ chế → fix → cách xác minh; dùng nhiều bug đại diện cho các nhánh quan trọng và giải thích cả vì sao cách sửa chỉ xử lý đúng tầng đó.
8. **Bài tập có lời giải mẫu**, rồi bài tương tự bỏ dần gợi ý.
9. **Retrieval check**: giải thích “vì sao”, không chỉ nhận diện tên API.
10. **Ôn liên kết**: đầu chương kế tiếp có 2–3 câu về chương trước; thẻ lặp lại ngắt quãng có thể thêm sau nếu cơ chế localStorage và UX rõ ràng.

## 5. Minh họa và style

- Dùng hai link người dùng đưa làm **tham khảo hình thức**: [Designed to Scale](https://designed-to-scale.vercel.app/) cho cách kể chuyện có nhịp, [Protocol Explorer](https://protocol-explorer-alpha.vercel.app/) cho bảng trạng thái/timeline tương tác. Chúng không phải nguồn kỹ thuật.
- Cấu trúc có thể gồm guided deep-dive và explorer riêng; mục lục sticky, node map, timeline, step-through, panel code/state/threads/phases.
- Mỗi hình chỉ mang một mối quan hệ. Nêu trạng thái ban đầu, bước kế, kết quả; giảm tốc/tua frame có chủ đích. Một diagram phải khớp đúng với code ví dụ bên cạnh.
- Dùng màu theo nhóm thành phần và giữ nghĩa màu nhất quán; không truyền tải trạng thái chỉ bằng màu. Có nhãn/icon/text.
- Nội dung Việt tự nhiên, giữ tên API/class tiếng Anh; responsive, keyboard accessible, contrast đủ và hỗ trợ reduced motion.
- Mô phỏng web không thể khẳng định nó chạy đúng Android runtime chỉ vì cho output giống nhau. Hiển thị nhãn `Mô hình khái niệm` và nút mở nguồn code/API.

## 6. Cách tận dụng thư viện sách

- [Catalog toàn bộ PDF/EPUB](androidbooks-knowledge/catalog.md) ghi 150 tệp, SHA-256, bản trùng chính xác, số trang/chương và tình trạng trích xuất.
- [Knowledge base index](androidbooks-knowledge/README.md) chỉ AI cách sử dụng ghi chú và tìm nguồn trong kho.
- Ghi chú theo chủ đề giữ phần giải thích nguyên bản và đường dẫn đến chương/trang, không lưu bản chép toàn văn.
- Với sách có ấn bản cũ (ví dụ Compose 1.3), dùng để dạy fundamentals và lịch sử; xác minh API hiện tại bằng docs/source trước khi dạy.
- Khi hai sách khác cách diễn đạt: đối chiếu với ngôn ngữ Kotlin, Android Developers, API contract và source code đang dùng; lưu khác biệt thành ghi chú phiên bản thay vì gộp thành một quy tắc.

## 7. Nguồn chính để bắt đầu

### Kotlin Coroutines

- [Kotlin Coroutines Guide](https://kotlinlang.org/docs/coroutines-guide.html) — lộ trình chủ đề Kotlin.
- [Coroutines basics](https://kotlinlang.org/docs/coroutines-basics.html) — suspension, scope, structured concurrency, builder và dispatcher.
- [Coroutine context and dispatchers](https://kotlinlang.org/docs/coroutine-context-and-dispatchers.html).
- [Cancellation and timeouts](https://kotlinlang.org/docs/coroutines-cancellation.html).
- [Flows](https://kotlinlang.org/docs/coroutines-flow.html).
- [Coroutines on Android](https://developer.android.com/kotlin/coroutines) và [coroutine best practices](https://developer.android.com/kotlin/coroutines/coroutines-best-practices).
- [Kotlin KEEP: Coroutines proposal](https://github.com/Kotlin/KEEP/blob/master/proposals/coroutines.md) cho CPS/Continuation ở mức language design.

### Compose Runtime

- [Thinking in Compose](https://developer.android.com/develop/ui/compose/mental-model).
- [Composable lifecycle](https://developer.android.com/develop/ui/compose/lifecycle).
- [State and Jetpack Compose](https://developer.android.com/develop/ui/compose/state).
- [How Composition Works](https://android.googlesource.com/platform/frameworks/support/+/androidx-main/compose/runtime/design/how-compose-works.md) — đọc kèm cảnh báo về chi tiết SlotTable có thể thay đổi.
- [Composer API](https://developer.android.com/reference/kotlin/androidx/compose/runtime/Composer), [Applier API](https://developer.android.com/reference/kotlin/androidx/compose/runtime/Applier), [Snapshot API](https://developer.android.com/reference/kotlin/androidx/compose/runtime/snapshots/Snapshot), [Compose Runtime release notes](https://developer.android.com/jetpack/androidx/releases/compose-runtime).
- [Compose side-effects](https://developer.android.com/develop/ui/compose/side-effects), [phases](https://developer.android.com/develop/ui/compose/phases), [performance](https://developer.android.com/develop/ui/compose/performance/phases).

### Compose Animation

- [Quick guide to animations in Compose](https://developer.android.com/develop/ui/compose/animation/quick-guide).
- [Value-based animations](https://developer.android.com/develop/ui/compose/animation/value-based).
- [Shared element transitions](https://developer.android.com/develop/ui/compose/animation/shared-elements) và [LookaheadScope API](https://developer.android.com/reference/kotlin/androidx/compose/ui/layout/LookaheadScope).
- AndroidX source theo version: `compose/animation/animation-core` (`Animatable`, `SuspendAnimation`, specs, vector converters) và `compose/animation/animation` (high-level APIs).

## 8. Trạng thái tài liệu

Roadmap này hiện bao quát toàn bộ các track được nêu trong lộ trình Claude, nhưng không tuyên bố rằng nội dung bài học của tất cả track đã được viết. Ghi chú chuyên sâu hiện có cho Coroutines, Compose Runtime và Compose Animation; các track còn lại có outline chi tiết và nguồn sách để tiếp tục. Đây không phải chỉ thị triển khai website hay thay thế tiến độ Claude. Version hiện tại phải được lấy từ tài liệu project có ngày kiểm chứng trước khi viết từng chương. Chi tiết đọc kho sách và giới hạn trích xuất xem [knowledge base README](androidbooks-knowledge/README.md).
