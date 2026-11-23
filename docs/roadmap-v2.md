# Lộ trình v2: học sâu, đầy đủ, dễ hiểu hơn đọc sách (ghi 2026-11-21)

## Vì sao có v2 (lời người dùng, tóm ý)

- Site hiện tại **quá rút gọn**. Với người mới, đọc sách (nhất là *Kotlin Coroutines: Deep Dive*) còn dễ hiểu hơn.
- Mục tiêu là hiểu **bản chất và cơ chế** để tự sửa được những bug mà AI không nhìn ra.
- Không ngại dài. Phải chi tiết, đầy đủ và dễ hiểu hết mức có thể.
- **Quyết định của người dùng:** site chỉ dùng nội bộ, cá nhân, để tự học. Vì vậy được **tận dụng tối đa** sách trong `E:\AndroidBooks`:
  - sách thành nguồn giảng dạy chính, cùng với tài liệu chính thức;
  - tìm thêm cách giảng dễ hiểu trên mạng.
  - Điều này thay quy tắc "sách chỉ là nguồn phụ, không chép" trước đây. CLAUDE.md đã sửa theo.
  - Vẫn giữ: không ghi đường dẫn file cục bộ lên site; chi tiết nội bộ có phiên bản; mô hình giản lược phải gắn nhãn.

## Cách làm mỗi chương (thay kiểu "1 đoạn bản chất + 1 sim")

Mỗi chương gồm các phần sau, theo thứ tự:

1. **Vấn đề trước khi có khái niệm:** viết theo cách cũ thì đau ở đâu, có ví dụ mã.
2. **Giảng từng bước:** nhiều đoạn, đi theo mạch của sách, ví dụ chạy được và có output dự đoán.
3. **Dưới mui xe:** cơ chế thật, gồm mã sau khi compiler biến đổi, cấu trúc dữ liệu và trích mã nguồn thư viện có ghi phiên bản.
4. **Sim / hình**, giữ phần đã làm.
5. **Bug thường gặp:**
   - triệu chứng → nguyên nhân cơ chế → cách sửa;
   - bài "đoán output" và "tìm bug".
6. **Bài tập** (lấy ý từ *Kotlin Exercises* và từ bài tập trong sách) cùng lời giải.
7. **Tóm tắt và câu hỏi tự kiểm.**

Kỹ thuật: thêm loại mục `sec.*.deep`, `sec.*.bug`, `sec.*.exercise` cho thân chương dài. Nếu cần, thêm chế độ "đọc dài" có mục lục nổi. Viết nội dung qua generator `dev/gen/*_content.py`.

## Thứ tự ưu tiên

| # | Việc | Sách chính (trong `E:\AndroidBooks`) |
|---|---|---|
| 1 | **Coroutines viết lại theo Deep Dive** (track A mở rộng) | `deep_dive_kotlin/kotlin/Kotlin Coroutines  Deep Dive.pdf`; `Kotlin Coroutines by Tutorials.pdf`; `Programming Android with Kotlin…` |
| 2 | Compose Runtime / Animation sâu hơn | `Jetpack Compose by Tutorials`, `Jetpack Compose 1.3 Essentials`, `Android UI Development with Jetpack Compose`, `Android Animations by Tutorials.pdf` |
| 3 | UX / UI sâu hơn | thư mục `UX/` (Norman, Krug, Podmajersky, Metts & Welfle, Greever, Albert & Tullis); `UI/` (Tidwell *Designing Interfaces*, Neil, MacDonald, Williams, Wendel, Design Sprint, Design Thinking Playbook); `design/` |
| 4 | **Track mới: Kotlin (trừ coroutines)** | `deep_dive_kotlin/kotlin/`: Kotlin Essentials, Advanced Kotlin, Effective Kotlin, Functional Kotlin, Kotlin Exercises |
| 5 | **Track mới: Clean Android Architecture** | `Clean Android Architecture/` (Dumbravan; Boudjnah); `Advanced Android App Architecture….pdf`; `Fundamentals of Software Architecture`; `Dagger by Tutorials` (DI) |
| 6 | **Track mới: Saving Data on Android** | `Saving Data on Android….pdf` (SharedPreferences/DataStore, file, SQLite, Room, đồng bộ) |
| 7 | **Track mới: Mobile System Design** | `deep_dive_kotlin/system-design/`: Mobile System Design (Tjeerd), DDIA (bản 1 và 2), Alex Xu tập 1 và 2, Acing the SDI, OS Concepts (chỉ phần áp dụng được cho mobile: tiến trình/luồng, bộ nhớ, đồng bộ hoá) |
| 8 | **Track mới: Clean Code** (tuyển tập, người dùng bổ sung nguồn) | `deep_dive_kotlin/ggplaybook/`: *The Clean Coder*, *Clean Craftsmanship* (TDD, refactoring, simple design, kỷ luật), *Clean Architecture* (SOLID, nguyên lý thành phần, Dependency Rule; dùng chung với track 5), *Clean Agile*, *Code That Fits in Your Head* (Seemann: heuristic, checklist, đo độ phức tạp), *The Software Craftsman*; cùng với *Effective Kotlin* để có ví dụ Kotlin. Có thể dùng thêm *API Design Patterns* và *Fundamentals of Software Architecture* (cùng thư mục) cho phần thiết kế API và kiến trúc |
| 9 | **Track mới: Functional Programming in Kotlin** ("Build Your Software Faster and Safer…") | `From Objects to Functions….pdf`, `Functional Programming in K_….pdf`, `Functional Programming in Kotlin by Tutorials.pdf`, Functional Kotlin |

## Trạng thái các track (cập nhật 2026-11-24)

| Mã | Track (id) | Trạng thái | Dàn ý / spec |
|---|---|---|---|
| A | Coroutines (`coroutines`) | **Xong v2**, stable | mục "Coroutines v2" bên dưới |
| B | Compose Runtime (`runtime`) | **Xong v2**, stable; đã đổi hình B3, B4, MD, LZ | mục "Compose Runtime v2" bên dưới |
| C | Compose Animation (`animation`) | **Xong v2**, stable; đã đổi hình C0 | mục "Compose Animation v2" bên dưới |
| D | UX (`ux`) | **Tạm dừng** ("Sắp ra mắt"); dàn v2 đã đối chiếu sách | mục "UX v2" bên dưới |
| E | UI (`ui`) | **Tạm dừng** ("Sắp ra mắt"); dàn v2 đã đối chiếu sách | mục "UI v2" bên dưới |
| F | Kotlin (`kotlin`) | **Xong**, stable, 14 chương; đã đổi hình K4, K9, K10, K12, K0 | `docs/tracks/F-kotlin.md` |
| G | Kiến trúc app Android (`arch`) | **Đã duyệt**, đang viết (G1 xong), draft | `docs/tracks/G-clean-architecture.md` |
| H | Lưu dữ liệu (`storage`) | **Đã duyệt** 2026-11-24, chưa xây (sau G) | `docs/tracks/H-saving-data.md` |
| I | Thiết kế hệ thống phía mobile (`sysdesign`) | **Đã duyệt** 2026-11-24, chưa xây (sau H) | `docs/tracks/I-mobile-system-design.md` |
| J | Mã sạch và kỷ luật làm nghề (`cleancode`) | **Đã duyệt** 2026-11-24, chưa xây (sau I) | `docs/tracks/J-clean-code.md` |
| K | Lập trình hàm với Kotlin (`fp`) | **Đã duyệt** 2026-11-24, chưa xây (sau J) | `docs/tracks/K-functional-kotlin.md` |

Mỗi dàn ý ghi cột **Hình chính** cho từng chương. Kiểu hình chọn theo nội dung, xem `docs/chapter-template-v2.md`, mục "Chọn kiểu hình theo nội dung". Một track chỉ được xây sau khi người dùng duyệt IN/OUT và dàn chương của nó.

Thêm track mới theo `E:\AndroidDeepDiveExplorer-Prompts\P-NEW-TRACK.md` và `TRACK-TEMPLATE.md`. Lõi không phải sửa.

## Coroutines v2: dàn chương (đã đối chiếu mục lục thật của *Kotlin Coroutines: Deep Dive*, 2026-11-22; số trang là trang PDF)

Mục lục sách: Phần 1 (tr. 13–64): Why Kotlin Coroutines? · Sequence builder · How does suspension work? · Coroutines under the hood · Built-in support vs library. Phần 2 (tr. 65–233): Coroutine builders · Coroutine context · Jobs and awaiting children · Cancellation · Exception handling · Coroutine scope functions · Dispatchers · Constructing a coroutine scope · The problem with shared state · Testing. Phần 3 (tr. 234–375): Channel · Select · Hot and cold data sources · Flow introduction · Understanding Flow · Flow building · Flow lifecycle functions · Flow processing · SharedFlow and StateFlow · Testing flow. Phần 4 (tr. 376–449): Common use cases · Recipes · Using coroutines from other languages · Launching coroutines vs. suspending functions · Best practices.

Chương mới của Phần 1 dùng id mới, chèn trước `a1` trong manifest; giữ nguyên id `a0…a9` (cầu nối, lộ trình, tiến độ đã lưu trỏ tới chúng).

**Phần 1: Hiểu coroutine**
- Vì sao cần coroutine: callback, RxJava, thread.
- Sequence builder (`sequence`/`yield`) là bước đệm để hiểu suspension.
- Suspension hoạt động thế nào: `suspendCoroutine`, `Continuation`, resume với giá trị hoặc exception.
- Coroutine dưới mui xe:
  - CPS;
  - state machine với `label`;
  - continuation lồng nhau như call stack;
  - giá cả hiệu năng.
- Hỗ trợ của ngôn ngữ so với thư viện kotlinx.

**Phần 2: Thư viện**
- Builder: `launch`, `async`, `runBlocking`.
- `CoroutineContext`: là một map, dùng phép `+`, có các phần tử như `Job`, dispatcher, tên, handler.
- Job và chờ con.
- Hủy:
  - hủy là hợp tác;
  - `CancellationException`;
  - `NonCancellable`;
  - `ensureActive`.
- Xử lý exception: `SupervisorJob`, `supervisorScope`, `CoroutineExceptionHandler`.
- Scope functions: `coroutineScope`, `withContext`, `withTimeout`.
- Dispatchers: Default, IO, Main, `limitedParallelism`.
- Tự dựng scope.
- Shared state: `Mutex`, atomic, giới hạn luồng.
- Test: `runTest`, thời gian ảo.

**Phần 3: Channel và Flow**
- Channel và `select`.
- Nguồn nóng và lạnh.
- Flow:
  - Flow tự dựng từ đầu (để hiểu bản chất);
  - tạo flow, vòng đời (`onStart`, `onCompletion`, `catch`);
  - xử lý (`map`, `flatMapConcat`/`Merge`/`Latest`, `combine`, `zip`);
  - `SharedFlow`/`StateFlow`, `stateIn`/`shareIn`;
  - test flow.

**Phần 4: Thực hành** (Common use cases, Recipes, Launching vs suspending, Best practices; bỏ "from other languages" trừ phần liên quan Java interop)
- `viewModelScope`, `lifecycleScope`, `repeatOnLifecycle`.
- Các bug thường gặp: rò scope, nuốt `CancellationException`, `GlobalScope`, block luồng Main.

## Việc kỹ thuật đã làm trong phiên này

- `git init` và commit đầu tiên (snapshot P0–P8 cùng đợt đổi hình minh hoạ).
- `core.autocrlf=false` để generator vẫn tái tạo đúng từng byte.

## Dàn chương nháp cho các track còn lại (2026-11-21)

> **Chưa đối chiếu mục lục sách.** Viết từ hiểu biết chung về các sách này vì usage tuần gần hết. Trước khi viết một track, phải đọc mục lục thật (`tools/epub_toc.py` cho epub, các trang đầu cho pdf) rồi sửa dàn chương cho khớp.

### Compose Runtime v2: dàn chương ĐÃ đối chiếu mục lục sách (2026-11-22)

**Nguồn trong kho**, đều là sách thực hành, không có sách về nội bộ Compose:
- *Android UI Development with Jetpack Compose* (Kunneth):
  - Ch.2 Declarative paradigm;
  - Ch.3 Key principles (composable functions, composing/recomposing, modifiers);
  - Ch.4 Laying out (single measure pass, custom layouts);
  - Ch.5 State (stateful/stateless, hoisting, config changes);
  - Ch.7 Tips (persisting state, responsive, side effects);
  - Ch.9 Interop;
  - Ch.10 Testing, semantics, debugging.
- *Jetpack Compose by Tutorials* 2nd: Ch.4 Lists; Ch.6 Modifiers; Ch.7 State; Ch.11 Lifecycle and effects; Ch.13 View compat; Ch.14 UI tests; Ch.15 Accessibility.
- *Jetpack Compose 1.3 Essentials*:
  - Ch.18–20 overview, composables, state and recomposition;
  - Ch.21 CompositionLocal; Ch.22–23 Slot APIs; Ch.24 Modifiers;
  - Ch.28–29 custom layout modifiers and layouts; Ch.32 IntrinsicSize;
  - Ch.33 Coroutines and LaunchedEffect; Ch.34–37 Lists, lazy lists, sticky headers.

**Nguồn cơ chế** (thay cho sách nội bộ):
- tài liệu chính thức developer.android.com: mental model, lifecycle, state, side effects, phases, stability, performance;
- tài liệu thiết kế AndroidX `compose/runtime/design/how-compose-works.md`;
- mã nguồn AndroidX: runtime, compiler, ui. Ghi rõ nhánh hoặc phiên bản cho mọi chi tiết nội bộ.

**Dàn chương.** Giữ id v1 để route không đổi, đào sâu tại chỗ. Thêm chương mới:

| Thứ tự | Id | Chương | Nguồn chính |
|---|---|---|---|
| 1 | b0 | Bản đồ (cập nhật cuối cùng, sau khi các chương xong) | tổng hợp |
| 2 | **dc** (mới) | Tư duy khai báo: từ View tới composable; tính chất của composable function (idempotent, không side effect, chạy bất kỳ thứ tự/lần nào) | Kunneth Ch.2–3, Tutorials Ch.1–2, Essentials Ch.18–19, "Thinking in Compose" |
| 3 | b1 | setContent và host | Kunneth Ch.9 (một phần), mã AndroidX |
| 4 | b2 | Compiler biến đổi gì: `$composer`, `$changed`, group, restart/skip | how-compose-works.md, mã compiler |
| 5 | b3 | Identity, SlotTable, `remember`, `key` | how-compose-works.md, lifecycle docs, Essentials Ch.34–36 (key trong list) |
| 6 | b4 | State và Snapshot: `MutableState`, policy, snapshot isolation, `derivedStateOf`, `snapshotFlow`, state collection | Kunneth Ch.5, Tutorials Ch.7, Essentials Ch.20, Snapshot API, mã runtime |
| 7 | **sh** (mới) | Quản lý state: stateful/stateless, hoisting, `rememberSaveable`, ViewModel, nguồn sự thật | Kunneth Ch.5, Ch.7; Tutorials Ch.7; Essentials Ch.42 |
| 8 | b5 | Recomposer và frame clock | how-compose-works.md, mã Recomposer |
| 9 | **ef** (mới) | Side effects và vòng đời: LaunchedEffect, DisposableEffect, SideEffect, rememberUpdatedState, produceState, rememberCoroutineScope | Kunneth Ch.7, Tutorials Ch.11, Essentials Ch.33, side-effects docs. Nối với A8 của Coroutines |
| 10 | **cl** (mới) | CompositionLocal và slot API | Essentials Ch.21–23 |
| 11 | b6 | Composer ghi nhận, Applier áp dụng, LayoutNode | mã runtime/ui |
| 12 | b7 | Ba phase và hoãn đọc state | phases docs, performance-by-phase |
| 13 | **lo** (mới) | Layout: Constraints, single measure pass, custom Layout, intrinsics, SubcomposeLayout | Kunneth Ch.4, Essentials Ch.28–29, Ch.32, layout docs |
| 14 | **md** (mới) | Modifier: chuỗi, thứ tự, `Modifier.Node` | Tutorials Ch.6, Essentials Ch.24 và Ch.28, modifier docs |
| 15 | **lz** (mới) | Lazy list bên trong: compose theo nhu cầu, key, contentType, tái sử dụng | Tutorials Ch.4, Essentials Ch.34–37, lists docs |
| 16 | b8 | Skip, stability, strong skipping, compiler report; **các annotation của runtime** (yêu cầu người dùng 2026-11-23): `@Stable`, `@Immutable`, `@StableMarker`, `@NonSkippableComposable`, `@NonRestartableComposable`, `@ReadOnlyComposable`, `@DontMemoize`, `@ExplicitGroupsComposable`, `@DisallowComposableCalls`, `@ComposableTarget`… (chỉ dạy annotation có thật trong `compose/runtime` ở commit ghim; mỗi cái: compiler sinh mã gì khác, khi nào dùng, khi nào không) | stability docs, mã compiler, mã runtime |
| 17 | b9 | Host, semantics, test và accessibility | Kunneth Ch.10, Tutorials Ch.14–15 |
| 18 | **pf** (mới) | Hiệu năng và debug: đếm recomposition, Layout Inspector, baseline profile | Kunneth Ch.10, performance docs |
| 19 | b10 | Live: luồng +1 (giữ, cập nhật tham chiếu) | tổng hợp |

Thứ tự viết: dc → b2 → b3 → b4 → sh → b5 → ef → … (cuối cùng là b0).

**Dàn nháp cũ (2026-11-21), giữ để đối chiếu:**
- Compose là gì ở tầng dưới: compiler plugin, `Composer`, slot table, gap buffer.
- `@Composable` bị biến đổi thế nào:
  - tham số `$composer` và `$changed`;
  - group;
  - `remember` lưu vào slot.
- Positional memoization và `key`. Bug thường gặp: state "nhảy" sang item khác trong list.
- Snapshot system:
  - `MutableState`;
  - đọc và ghi trong snapshot;
  - snapshot toàn cục;
  - `derivedStateOf`;
  - `snapshotFlow`.
- Recomposition:
  - invalidation, scope recompose;
  - skippable/restartable;
  - stability (`@Stable`, `@Immutable`, strong skipping);
  - compiler report.
- Side effects: `LaunchedEffect`, `DisposableEffect`, `SideEffect`, `rememberUpdatedState`, `produceState`. Bug thường gặp: effect chạy lại hoặc capture giá trị cũ.
- Ba phase: composition → layout → draw. Defer read bằng lambda modifier.
- Layout: measure policy, constraints, intrinsic, `SubcomposeLayout`, `LazyColumn` bên trong.
- Modifier chain: `Modifier.Node`, thứ tự áp dụng.
- `CompositionLocal`; Applier và cây `LayoutNode`; semantics tree.
- Hiệu năng: layout inspector, đếm số lần recompose, baseline profile.

### Compose Animation v2: dàn chương ĐÃ đối chiếu mục lục sách (2026-11-23)

**Mục lục thật đã đọc:**
- *Android Animations by Tutorials* (PDF, đọc trang mục lục bằng pdftotext): Phần I View & Property (Ch.1 Value & Object Animators, Ch.2 Animating Custom Views, Ch.3 XML Animations); Phần II Screen Transitions (Ch.4 Activity & Fragment transitions bằng XML, Ch.5 Transition Framework, Ch.6 Element Transitions/shared element); Phần III List & Gesture (Ch.7 Basic List Animations, Ch.8 ItemTouchHelper, Ch.9 Animate Scroll Gestures); Phần IV Ch.10 Jetpack Compose Animations (visibility, content size, state changes). Sách chủ yếu về hệ View; chỉ Ch.10 là Compose.
- Kunneth Ch.8 Working with Animations: animating single value / multiple value changes, AnimatedVisibility, animating size changes, Crossfade, animation specifications.
- Jetpack Compose by Tutorials Ch.12 Animating Properties: JoinButton (nền animate), Transition (định nghĩa, nối vào composable), animating composable content (JoinedToast).
- Jetpack Compose 1.3 Essentials: Ch.39 Visibility Animation (enter/exit, spec và easing, repeat, animateEnterExit cho con, auto-start, crossfade); Ch.40 State-Driven Animation (animate*AsState: rotation, color, Dp; spring; keyframes; kết hợp nhiều animation; Animation Inspector); Ch.41 Canvas; Ch.50 Gestures.
- Tài liệu developer.android.com (danh mục 2026-11-23): introduction, choose-api (cây quyết định), quick-guide, composables-modifiers, value-based, vectors, advanced, customize, shared-elements (+ customize, common-use-cases, navigation), testing, tooling.
- Mã ở commit ghim 296313a4: `compose/animation/animation-core` (Animatable, AnimateAsState, AnimationSpec, SpringSimulation, Easing, DecayAnimationSpec, Transition, InfiniteTransition, SuspendAnimation, VectorConverters…) và `compose/animation/animation` (AnimatedVisibility, AnimatedContent, Crossfade, EnterExitTransition, AnimationModifier, SharedTransitionScope, SharedElement…).

**Dàn chương.** Giữ id v1 (c0–c8) để route không đổi; thêm 4 chương mới. Mỗi chương theo khuôn v2 (đoán trước, giảng từng bước, dưới mui xe với mã ghim, sim mới, bug, bài tập, tự trả lời, quiz).

| Thứ tự | Id | Chương | Nguồn chính |
|---|---|---|---|
| 1 | c0 | Chọn API (viết lại CUỐI CÙNG, theo cây quyết định choose-api) | choose-api, Kunneth Ch.8 mở đầu |
| 2 | **vm** (mới) | Trước Compose: ValueAnimator, ObjectAnimator, interpolator, Transition framework, shared element trong View; đối chiếu từng khái niệm với Compose | AAT Ch.1–6 |
| 3 | c1 | Từ target đến giá trị: animate*AsState, đổi target giữa chừng, label | Kunneth Ch.8, Essentials Ch.40, Tutorials Ch.12, value-based, `AnimateAsState.kt` |
| 4 | c2 | AnimationSpec: spring, tween/easing, keyframes, repeat, snap, decay, AnimationVector/TwoWayConverter | Essentials 39.4, 40.7–40.8, customize, `AnimationSpec.kt`, `SpringSimulation.kt`, `Easing.kt`; AAT Ch.1 (interpolator) |
| 5 | c3 | updateTransition: nhiều giá trị theo một state, transitionSpec theo hướng, MutableTransitionState | Kunneth Ch.8, Tutorials Ch.12, value-based, `Transition.kt` |
| 6 | c4 | AnimatedVisibility, animateEnterExit, AnimatedContent, Crossfade, thời điểm rời composition | Kunneth Ch.8, Essentials Ch.39, AAT Ch.10, composables-modifiers, `AnimatedVisibility.kt`, `AnimatedContent.kt` |
| 7 | c5 | Kích thước, layout và item: animateContentSize, animateItem, layout vs graphicsLayer | Kunneth Ch.8, AAT Ch.10 và Ch.7 (đối chiếu ItemAnimator), lists docs, `AnimationModifier.kt` |
| 8 | **if** (mới) | Lặp và vô hạn: repeatable, infiniteRepeatable, rememberInfiniteTransition, InfiniteAnimationPolicy | Essentials 39.5, value-based, `InfiniteTransition.kt`, `InfiniteAnimationPolicy.kt` |
| 9 | c6 | Animatable và gesture: animateTo/snapTo/animateDecay/stop, mutex, VelocityTracker, fling | advanced, Essentials Ch.50, AAT Ch.9, `Animatable.kt`, `DecayAnimationSpec.kt` |
| 10 | **se** (mới) | Shared element và chuyển màn hình: SharedTransitionLayout, sharedElement/sharedBounds, navigation | shared-elements docs, AAT Ch.4–6 (đối chiếu View), `SharedTransitionScope.kt` |
| 11 | **cv** (mới) | Vẽ và vector động: Canvas + animation, AnimatedVectorDrawable | Essentials Ch.41, vectors docs, AAT Ch.2 |
| 12 | c7 | Frame clock và phase (giữ X1, X3) | Runtime B5, B7, quick-guide (hiệu năng) |
| 13 | c8 | Kiểm thử, công cụ, giảm chuyển động | testing, tooling, Essentials 40.10, Runtime B9 (đồng hồ ảo) |

Thứ tự viết: c1 → c2 → c3 → c4 → c5 → if → c6 → se → cv → vm → c7 → c8 → c0.

**Việc kỹ thuật trước chương đầu:** `dev/gen/animation_content.py` chưa có cơ chế module v2; thêm vòng `for mod in (...)` với `add/override/SEC_ORDER` giống `runtime_content.py`.

### UX v2: dàn chương ĐÃ đối chiếu mục lục sách (2026-11-23)

> **Tạm dừng (2026-11-23, người dùng):** UX và UI hiển thị "Sắp ra mắt" (`status: 'soon'`). Đã xong: D1 v2 và cơ chế màn hình mẫu. SM dở dang nằm trong `git stash`. Khi làm lại: chọn kiến thức cần và đủ, không bám từng chương sách.

**Mục lục thật đã đọc** (epub bằng `tools/epub_toc.py`, PDF bằng pdftotext; chỉ đọc tiêu đề):
- Norman, *The Design of Everyday Things* (bản sửa đổi): Ch.1 Psychopathology of Everyday Things (HCD, nguyên lý tương tác, system image, nghịch lý công nghệ); Ch.2 Psychology of Everyday Actions (gulf of execution/evaluation, seven stages, ba mức xử lý, tự đổ lỗi, 7 nguyên lý từ seven stages); Ch.3 Knowledge in the Head and in the World (cấu trúc trí nhớ, đánh đổi đầu/thế giới, natural mapping và văn hóa); Ch.4 Constraints, Discoverability, Feedback (4 loại ràng buộc, forcing function, quy ước, âm thanh làm signifier); Ch.5 Human Error? No, Bad Design (slip/mistake và phân loại, vi phạm cố ý, phát hiện lỗi, designing for error, resilience engineering, nghịch lý tự động hóa); Ch.6 Design Thinking (giải đúng vấn đề, Double Diamond, HCD process, chuẩn hóa); Ch.7 Design in the World of Business (đổi mới tiệm tiến/đột phá, trách nhiệm đạo đức).
- Krug, *Don't Make Me Think, Revisited* (3rd ed.): Ch.1 Don't make me think; Ch.2 How we really use the Web (quét, satisficing, muddle through); Ch.3 Billboard Design 101 (quy ước, phân cấp thị giác, vùng bấm được); Ch.4 Animal, Vegetable, or Mineral? (lựa chọn không cần nghĩ); Ch.5 Omit needless words; Ch.6 Street signs and Breadcrumbs (điều hướng); Ch.7 The Big Bang Theory of Web Design (trang chủ); Ch.8 The Farmer and the Cowman (tranh luận trong nhóm, "người dùng trung bình" là huyền thoại); Ch.9 Usability testing on 10 cents a day; Ch.10 Mobile; Ch.11 Usability as common courtesy (reservoir of goodwill); Ch.12 Accessibility; Ch.13 Guide for the perplexed.
- Whalen, *Design for How People Think*: Part I Ch.1 The Six Minds of Experience; Ch.2 Vision/Attention/Automaticity; Ch.3 Wayfinding; Ch.4 Memory/Semantics; Ch.5 Language; Ch.6 Decision Making and Problem Solving; Ch.7 Emotion; Part II Ch.8 Contextual Interviews; Ch.9–14 khai thác từng "mind" trong nghiên cứu; Part III Ch.15 Sense-Making; Ch.16 Appeal, Enhance, Awaken; Ch.17 Succeed Fast; Ch.19 How to Make a Better Human.
- Albert & Tullis, *Measuring the User Experience*: Ch.1 Introduction (10 myths); Ch.2 Background (biến, kiểu dữ liệu, thống kê mô tả, so sánh trung bình, phi tham số, trình bày); Ch.3 Planning; Ch.4 Performance Metrics (task success, time-on-task, errors, efficiency, learnability); Ch.5 Self-Reported Metrics (rating scales, post-task, SUS); Ch.6 Issues-Based Metrics (severity, nhất quán, thiên lệch, số người tham gia); Ch.7 Eye Tracking; Ch.8 Measuring Emotion; Ch.9 Combined and Comparative Metrics.
- Podmajersky, *Strategic Writing for UX*: Ch.1 Why (mục tiêu người dùng và tổ chức); Ch.2 Voice (voice chart); Ch.3 Conversation for content-first design; Ch.4 UX text patterns (title, button, description, empty state, label, control, input, transitional, confirmation, notification, error); Ch.5 Edit in four phases (purposeful, concise, conversational, clear); Ch.6 Measuring UX content; Ch.7 Tools; Ch.8 30/60/90-day plan; Ch.9 What to do first.
- Metts & Welfle, *Writing Is Designing*: Ch.1 How words shape experiences; Ch.2 Strategy and research; Ch.3 Clarity (recognition vs recall, cognitive load, plain language); Ch.4 Errors and stress cases; Ch.5 Inclusivity and accessibility; Ch.6 Voice; Ch.7 Tone; Ch.8 Collaboration and consistency.
- Greever, *Articulating Design Decisions*: Ch.1 Great designers are great communicators; Ch.2 Stakeholders are people too; Ch.3 Design the meeting; Ch.4 Listen to understand; Ch.5 Right mindset; Ch.6 Form a response; Ch.7 Choose a message (business, design, research, limitations); Ch.8 Lock in agreement (IDEA → IDEAL); Ch.9 Follow up; Ch.10 Dealing with changes; Ch.11 How executives can help.
- Wendel, *Designing for Behavior Change*: Part I Ch.1–4 (deciding and acting, creating action, stopping negative actions, ethics); Part II Ch.5–13 (process, defining the problem, context, cue–reaction–evaluation, ability–timing–experience, implementation, A/B tests).
- Banfield, Lombardo, Wax, *Design Sprint*: Ch.1–4 (what, when, approach, plan); Ch.5–9 năm pha Understand, Diverge, Converge, Prototype, Test; Ch.10 after the sprint. Lewrick, Link, Leifer, *The Design Thinking Playbook*: 3 phần (understand, transform organizations, design the future).

**Dàn chương.** Giữ id v1 (d0–d10) để route không đổi; thêm 4 chương mới. Ví dụ xuyên suốt vẫn là app "Hẹn Khám" (spec track D). Framework của tác giả luôn ghi tên tác giả; "định luật" là heuristic có giới hạn; công thức (SUS, 1 − (1 − p)^n) có ví dụ kiểm chứng.

| Thứ tự | Id | Chương | Nguồn chính |
|---|---|---|---|
| 1 | d0 | Bản đồ UX (viết CUỐI CÙNG) | Norman Ch.1, Ch.6 (HCD, Double Diamond); Krug Ch.1 |
| 2 | d1 | Bộ óc người dùng: thị giác, chú ý, trí nhớ, mô hình tư duy | Whalen Ch.1–2, Ch.4; Norman Ch.3; Krug Ch.2 |
| 3 | **sm** (mới) | Sáu "bộ óc" của Whalen: wayfinding, ngôn ngữ, ra quyết định, cảm xúc, và cách quan sát chúng | Whalen Ch.3, Ch.5–7, Part II Ch.9–14, Ch.15–16 (framework của Whalen) |
| 4 | d2 | Nguyên lý tương tác: affordance, signifier, mapping, constraint, feedback, conceptual model, hai vịnh, seven stages | Norman Ch.1, Ch.2, Ch.4 |
| 5 | d3 | Lỗi người dùng: slip, mistake, thiết kế để phát hiện và phục hồi | Norman Ch.5; Metts & Welfle Ch.4 (thông báo lỗi) |
| 6 | **kr** (mới) | Thiết kế cho người quét trang: billboard design, quy ước, bỏ chữ thừa, điều hướng, mobile, thiện chí | Krug Ch.2–8, Ch.10–12 (framework của Krug) |
| 7 | d4 | Heuristic evaluation và mức độ nghiêm trọng | spec D4 (Nielsen); Albert & Tullis Ch.6 (severity, nhất quán, thiên lệch) |
| 8 | d5 | Quyết định, hành vi và đạo đức | Wendel Part I–II (cue–reaction–evaluation, ability–timing–experience; framework của Wendel), Ch.4 ethics; Whalen Ch.6–7; Norman Ch.7 |
| 9 | d6 | Nghiên cứu người dùng: phỏng vấn, contextual inquiry, chọn phương pháp | Whalen Ch.8; Metts & Welfle Ch.2; Albert & Tullis Ch.3 |
| 10 | d7 | Usability testing và "5 người dùng" | Krug Ch.9; Albert & Tullis Ch.6.7 (số người tham gia) |
| 11 | d8 | Đo lường UX: task success, thời gian, lỗi, SUS, kết hợp chỉ số | Albert & Tullis Ch.2, Ch.4, Ch.5, Ch.9 (Ch.7–8 chỉ giới thiệu) |
| 12 | d9 | UX writing: mục tiêu, voice chart, mẫu chữ, biên tập bốn pha | Podmajersky Ch.1–5; Metts & Welfle Ch.1, Ch.3, Ch.6–7 |
| 13 | **wx** (mới) | Viết cho lúc khó và cho mọi người: lỗi, stress case, hòa nhập, đo nội dung, làm nghề viết | Metts & Welfle Ch.4–5, Ch.8; Podmajersky Ch.6–9 |
| 14 | d10 | Quy trình: design thinking, design sprint năm pha | Banfield và cộng sự (Design Sprint) Ch.1–10; Lewrick và cộng sự (Design Thinking Playbook); Norman Ch.6 |
| 15 | **ad** (mới) | Trình bày và bảo vệ quyết định thiết kế với stakeholder | Greever Ch.1–11 (IDEAL; framework của Greever) |

Thứ tự viết: d1 → sm → d2 → d3 → kr → d4 → d5 → d6 → d7 → d8 → d9 → wx → d10 → ad → d0.

**Việc kỹ thuật trước chương đầu:** kiểm `dev/gen/ux_content.py` (hoặc file sinh nội dung UX tương ứng) có cơ chế module v2 (`for mod in (...)`, add/override/SEC_ORDER) chưa; nếu chưa thì thêm như Runtime/Animation. Chương mới thêm vào manifest theo đúng thứ tự trên; goal `step` tính theo sim từng bước đầu tiên của chương.

### UI v2: dàn chương ĐÃ đối chiếu mục lục sách (2026-11-23)

**Mục lục thật đã đọc:**
- Tidwell và cộng sự, *Designing Interfaces* (3rd ed.): Ch.1 Designing for People; Ch.2 Organizing the Content (IA, cấu trúc ứng dụng); Ch.3 Getting Around (điều hướng, signpost, wayfinding); Ch.4 Layout of Screen Elements; Ch.5 Visual Style and Aesthetics; Ch.6 Mobile Interfaces; Ch.7 Lists of Things; Ch.8 Doing Things (actions, commands); Ch.9 Showing Complex Data; Ch.10 Getting Input (forms, controls); Ch.11 UI Systems and Atomic Design; Ch.12 Beyond and Behind the Screen.
- Neil, *Mobile Design Pattern Gallery*: Ch.1 Navigation; Ch.2 Forms; Ch.3 Tables; Ch.4 Search, Sort, Filter; Ch.5 Tools; Ch.6 Charts; Ch.7 Tutorials and Invitations; Ch.8 Social; Ch.9 Feedback and Affordance; Ch.10 Help; Ch.11 Anti-Patterns.
- MacDonald, *Practical UI Patterns for Design Systems*: Ch.1 Introducing UI patterns; Ch.2 Tap into patterns; Ch.3 Deciding which pattern to use and when; Ch.4 Patterns in design systems; Ch.5 Anti-patterns and dark patterns; Ch.6 Mixing and matching patterns.
- Williams, *The Non-Designer's Design Book*: Ch.1–6 bốn nguyên tắc (proximity, alignment, repetition, contrast) và ôn tập; Ch.7 Color; Ch.8 Extra tips; Ch.9–12 typography (essentials, type & life, categories, type contrasts); Ch.13 Does it make sense?
- *App Design Apprentice* (Kodeco, 2nd ed., PDF): Ch.3 App teardowns; Ch.4 Wireframing & screen layout; Ch.5 Reusable elements & data; Ch.6 Typography; Ch.7 Colors; Ch.8 Design systems; Ch.9 Transitions & animations; Ch.10 Feedback & testing (Ch.1–2 là tổng quan và Figma).
- Chưa đọc được mục lục: Lupton, *Thinking with Type* (PDF, pdftotext không trích được tiêu đề ở các trang 5–12); phải đọc trước khi dùng cho E2.

**Dàn chương.** Giữ id v1 (e0–e10); thêm 3 chương mới. Nguồn chính thức cho Android: Material 3 và tài liệu Compose (theme, color roles, type scale, window size classes, accessibility); sách là nguồn giảng chính cho nguyên lý và pattern. Framework của tác giả (CRAP của Williams, atomic design trong Tidwell Ch.11) ghi tên tác giả; "định luật" (Fitts) là heuristic có giới hạn và có ví dụ tính.

| Thứ tự | Id | Chương | Nguồn chính |
|---|---|---|---|
| 1 | e0 | Bản đồ UI (viết CUỐI CÙNG) | Tidwell Ch.1; App Design Apprentice Ch.3 (teardown) |
| 2 | e1 | Nguyên lý thị giác: proximity, alignment, repetition, contrast; Gestalt; phân cấp | Williams Ch.1–6, Ch.13; Tidwell Ch.5 |
| 3 | e2 | Typography: type scale, độ dễ đọc, chữ tiếng Việt | Williams Ch.9–12; App Design Apprentice Ch.6; Lupton (sau khi đọc mục lục); M3 type scale |
| 4 | e3 | Màu: color roles, dynamic color, tương phản | Williams Ch.7; App Design Apprentice Ch.7; M3 color roles; WCAG |
| 5 | e4 | Bố cục, khoảng cách, giao diện thích ứng | Tidwell Ch.4, Ch.6; App Design Apprentice Ch.4; window size classes |
| 6 | **ia** (mới) | Kiến trúc thông tin và điều hướng | Tidwell Ch.2–3; Neil Ch.1; nối UX `kr` (Krug Ch.6) |
| 7 | e5 | Kích thước mục tiêu chạm và Fitts's law | spec E5; M3 touch target; Tidwell Ch.6 |
| 8 | e6 | Component và trạng thái tương tác | Tidwell Ch.8; Neil Ch.9; App Design Apprentice Ch.5 |
| 9 | e7 | Pattern: danh sách, form, tìm/sắp/lọc, onboarding, trợ giúp; chọn pattern | Tidwell Ch.7, Ch.10; Neil Ch.2–5, Ch.7, Ch.10; MacDonald Ch.1–3, Ch.6 |
| 10 | **dv** (mới) | Dữ liệu phức tạp và biểu đồ trên màn hình nhỏ | Tidwell Ch.9; Neil Ch.3, Ch.6 |
| 11 | **ap** (mới) | Anti-pattern và dark pattern | Neil Ch.11; MacDonald Ch.5; nối UX d5 (đạo đức) |
| 12 | e8 | Design system và token → `MaterialTheme` | Tidwell Ch.11; MacDonald Ch.4; App Design Apprentice Ch.8; M3 theming |
| 13 | e9 | Chuyển động có mục đích | App Design Apprentice Ch.9; nối track Animation (C0, C8) |
| 14 | e10 | Accessibility trong UI Compose | spec E10; tài liệu accessibility Compose; nối Runtime B9 |

Thứ tự viết: e1 → e2 → e3 → e4 → ia → e5 → e6 → e7 → dv → ap → e8 → e9 → e10 → e0.

### UX v2 / UI v2 (track D, E mở rộng) (dàn nháp cũ, giữ để đối chiếu)
- **UX:**
  - Norman: affordance, signifier, mapping, feedback, mô hình tư duy, hai vịnh (gulf of execution/evaluation), phân loại lỗi.
  - Krug: quét trang, tự giải thích, test khả dụng giá rẻ.
  - *Design for How People Think*.
  - Viết UX: Podmajersky (voice chart, các mẫu chữ), Metts & Welfle.
  - Bảo vệ quyết định thiết kế: Greever.
  - Đo lường: Albert & Tullis (task success, time, SUS, cỡ mẫu). Công thức phải có ví dụ kiểm chứng.
- **UI:**
  - Tidwell *Designing Interfaces*: pattern theo nhóm.
  - Neil, *Mobile Design Pattern Gallery*.
  - MacDonald, *Practical UI Patterns for Design Systems*.
  - Robin Williams: 4 nguyên tắc CRAP.
  - Wendel, *Designing for Behavior Change*.
  - *Design Sprint*, *Design Thinking Playbook*.
  - Material 3 trong Compose: token, theme.

### Kotlin (track mới, trừ coroutines)

> **Đã xong (2026-11-23):** cả 14 chương K0–K13, track `stable`. **Spec chốt (2026-11-23):** `docs/tracks/F-kotlin.md`, 14 chương, hai phần (nền tảng cho người mới; cơ chế sâu), chọn kiến thức cần và đủ, bài tập từ *Kotlin Exercises*. Dàn nháp dưới đây giữ để đối chiếu.
- **Essentials:** biến, kiểu, null-safety, hàm, class/object, data/sealed/enum, interface, generics cơ bản, collection, exception.
- **Advanced Kotlin:**
  - generics nâng cao: variance in/out, reified;
  - delegation (`by`, property delegate);
  - DSL và lambda with receiver;
  - annotation processing/KSP;
  - reflection;
  - Kotlin/JVM interop;
  - contract.
- **Functional Kotlin:** hàm bậc cao, inline/crossinline/noinline, `Sequence` so với collection, scope function, function reference.
- **Effective Kotlin:**
  - an toàn: hạn chế mutability, smart cast, require/check;
  - dễ đọc;
  - thiết kế lại mã;
  - hiệu năng: inline class, tránh tạo object, collection.
- **Dưới mui xe:** bytecode của lambda, inline, data class, `object`, `companion`, `lateinit`, `by lazy`.
- Bài tập lấy từ *Kotlin Exercises*.

### Các track mới G–K: đã có dàn ý riêng (2026-11-24)

Dàn nháp cũ (2026-11-21) của Clean Android Architecture, Saving Data, Mobile System Design, Clean Code và Functional Programming đã được thay bằng dàn ý có đối chiếu mục lục sách thật, IN/OUT có lý do, và kiểu hình cho từng chương:
- G: `docs/tracks/G-clean-architecture.md` (đã duyệt, đang viết)
- H: `docs/tracks/H-saving-data.md`
- I: `docs/tracks/I-mobile-system-design.md`
- J: `docs/tracks/J-clean-code.md`
- K: `docs/tracks/K-functional-kotlin.md`

Thay đổi so với dàn nháp cũ, đáng chú ý:
- Clean Code không dạy theo cuốn *Clean Code* (2008), vì cuốn đó không có trong kho.
- Mobile System Design nhìn từ phía client. Phần scale backend để OUT.
- FP bỏ các phần đã có ở track Kotlin (lambda, inline, collection, Sequence) và Coroutines (Flow).
