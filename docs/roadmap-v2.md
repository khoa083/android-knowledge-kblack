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
| 16 | b8 | Skip, stability, strong skipping, compiler report | stability docs, mã compiler |
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

### Compose Animation v2 (track C mở rộng)
- Nền tảng: frame clock, `withFrameNanos`, `Animatable`, `AnimationSpec` (tween, spring, keyframes, repeatable), easing.
- API cao: `animate*AsState`, `updateTransition`, `AnimatedVisibility`, `AnimatedContent`, `Crossfade`, `animateContentSize`.
- Cử chỉ: `pointerInput`, `draggable`, fling/decay, ngắt và retarget.
- Shared element transition, navigation animation.
- Từ *Android Animations by Tutorials*:
  - View system (property animator, `MotionLayout`, vector drawable);
  - đối chiếu với Compose.
- Hiệu năng và a11y: đọc state trong phase draw, reduced motion.

### UX v2 / UI v2 (track D, E mở rộng)
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

### Clean Android Architecture (track mới)
- Vì sao cần kiến trúc: mã dính vào framework, khó test.
- Clean Architecture (Martin):
  - SOLID;
  - Dependency Rule;
  - entity/use case/interface adapter/framework;
  - boundary.
- Tầng trên Android (Dumbravan, Boudjnah):
  - domain (use case, model);
  - data (repository, data source);
  - presentation (MVVM/MVI, ViewModel, UI state).
- Module hoá: feature module, quy tắc phụ thuộc giữa các module.
- DI: thủ công → Dagger/Hilt (*Dagger by Tutorials*), scope, component.
- *Advanced Android App Architecture*: MVC → MVP → MVVM → MVI → VIPER, so sánh trên cùng một app.
- Test theo tầng.
- *Fundamentals of Software Architecture*: đặc tính kiến trúc, trade-off.

### Saving Data on Android (track mới)
- SharedPreferences → DataStore (Preferences/Proto): luồng ghi, đọc qua Flow, tính nhất quán.
- File: internal/external, scoped storage.
- SQLite thuần: transaction, index.
- Room:
  - entity, DAO, quan hệ;
  - migration;
  - Flow/LiveData;
  - test.
- Đồng bộ dữ liệu với server, cache, offline-first, xung đột.
- Bảo mật dữ liệu lưu trên máy.

### Mobile System Design (track mới)
- **Khung phỏng vấn:** làm rõ yêu cầu → API → luồng dữ liệu → kiến trúc client → các chủ đề sâu.
- **Bài mẫu** (*Mobile System Design*, Alex Xu tập 1 và 2, *Acing the SDI*, chỉ phần client):
  - feed, chat, ảnh/video;
  - thông báo đẩy;
  - đồng bộ offline;
  - phân trang.
- **Dữ liệu** (DDIA):
  - mô hình dữ liệu;
  - đồng bộ, nhất quán;
  - replication;
  - log, idempotency, retry.
- **Mạng:** REST/GraphQL/WebSocket, cache HTTP, backoff, giới hạn băng thông và pin.
- **Hệ điều hành** (OS Concepts, phần áp dụng cho mobile):
  - tiến trình/luồng, lập lịch;
  - bộ nhớ (từ đó suy ra LMK trên Android);
  - đồng bộ hoá, deadlock.
- **Phi chức năng:** hiệu năng, khởi động app, kích thước, quan sát (log/metric), feature flag, phát hành từng phần.

### Clean Code (track mới, tuyển tập)
- **Mã sạch ở mức dòng/hàm:**
  - đặt tên, hàm nhỏ;
  - comment;
  - xử lý lỗi;
  - mã Kotlin minh hoạ lấy từ *Effective Kotlin*.
- **Kỷ luật** (*Clean Craftsmanship*):
  - TDD (3 luật, chu trình red-green-refactor);
  - refactoring;
  - simple design;
  - lập trình theo cặp.
- *Code That Fits in Your Head*: giới hạn trí nhớ làm việc, checklist, đo độ phức tạp, quy tắc 80/24.
- **Tính chuyên nghiệp** (*The Clean Coder*, *The Software Craftsman*): nói "không", ước lượng, áp lực, luyện tập.
- *Clean Agile*: các thực hành kỹ thuật của XP.
- **Thiết kế** (*Clean Architecture*, phần SOLID): dùng chung với track Clean Android Architecture, có liên kết qua lại.

### Functional Programming in Kotlin (track mới)
- **Nền tảng:**
  - hàm thuần, bất biến;
  - referential transparency;
  - hàm bậc cao, composition, currying.
- **Kiểu dữ liệu:**
  - ADT với sealed class;
  - Option/Either/Result;
  - xử lý lỗi không dùng exception.
- **Trừu tượng:** functor, applicative, monad (giảng bằng ví dụ, không bắt đầu từ lý thuyết), fold/recursion, lazy evaluation.
- **Hiệu ứng:** tách hiệu ứng ra rìa (functional core, imperative shell).
- **Từ OOP sang FP** (*From Objects to Functions*): dựng một app thật theo kiểu hàm.
- **FP trên Android** (*FP in Kotlin by Tutorials*): Arrow, state bất biến cho UI.
