# Nghiên cứu Track B: Compose Runtime (P3, 2026-11-21)

Mọi URL dưới đây đã đọc trực tiếp ngày 2026-11-21, đều trả HTTP 200, không chuyển hướng.

## Phiên bản chốt (từ `global.md` mục 2)
- Compose BOM 2026.11.01 → `compose.runtime` 1.13.0, `compose.ui` 1.13.0.
- Compose Compiler = plugin `org.jetbrains.kotlin.plugin.compose` đi cùng Kotlin 2.4.21.
- Strong skipping bật mặc định từ Kotlin 2.0.20 (nhãn `version`).

## Chi tiết nội bộ: nguồn và giới hạn
- `how-compose-works.md`: nhánh **androidx-main**, đường dẫn `compose/runtime/design/how-compose-works.md`, đọc 2026-11-21. **Cập nhật 2026-11-23:** đã ghim commit `296313a488a01c84ddcb0801d4efee640a14070c` (xem mục "Runtime v2"); nguồn `rt-how` trỏ tới commit đó. Chương v1 chưa viết lại (B0, B5, B6…) còn ghi "androidx-main, đọc 2026-11-21" và sẽ được sửa khi viết lại. Bản thân tài liệu cảnh báo SlotTable đang phát triển và có thể mô tả bản cũ.
- Lấy từ đó (mức khái niệm, nhãn `impl`): Composer làm positional memoization, phát hiện thay đổi, đánh giá lại tăng dần; SlotTable gồm nhóm (group) và slot lưu trong mảng phẳng dạng gap buffer; compiler thêm tham số `$composer`, gọi start/end group, restart group trả về update scope khi có lần đọc quan sát được; thao tác node liền kề được gộp trước khi gọi Applier.
- `$changed`: tài liệu nói nằm ngoài phạm vi → **chỉ nhắc tên, không giải thích bit**. Không mô tả layout bộ nhớ chi tiết.
- Recomposer chạy trong coroutine: reference `Recomposer` có `runRecomposeAndApplyChanges()` là suspend function, chờ composer bị invalidate, recompose, apply; có pause/resume frame clock. Không có nguồn nói dispatcher cụ thể → không nêu.

## Khẳng định theo chương
| Ch. | Khẳng định | Nguồn | Nhãn |
|---|---|---|---|
| B0 | Composition, Recomposer, Composer, Applier là vai trò khác nhau | how-compose-works, Recomposer ref, Applier ref | stable / impl |
| B1 | ComposeView: composition ban đầu khi view gắn vào window hoặc khi gọi `createComposition()`, cái nào trước; cần LifecycleOwner, SavedStateRegistryOwner | ComposeView ref | android-impl |
| B2 | Compiler thêm `$composer`, group, kiểm tra skipping; mã giả chỉ minh họa | how-compose-works | impl simplified |
| B3 | Identity theo call site + thứ tự thực thi; thêm cuối danh sách: tái dùng; thêm đầu/giữa, xóa, đổi chỗ: các item đổi vị trí bị recompose và effect đang chạy bị hủy, chạy lại; `key()` giữ identity | lifecycle | stable |
| B4 | Snapshot: giá trị cách ly, `apply` nguyên tử, có xung đột; read/write observer dùng để composition đăng ký đọc | Snapshot ref | stable |
| B5 | Recomposer là "scheduler" cho recomposition và apply; `withFrameNanos` suspend tới frame mới, thời gian tăng nghiêm ngặt | Recomposer ref, MonotonicFrameClock ref | stable |
| B6 | Applier áp dụng thao tác cây phát ra khi composition; generic theo kiểu node; onBeginChanges/onEndChanges bao mỗi đợt | Applier ref | stable; UiApplier/LayoutNode `android-impl` |
| B7 | Đọc trong composition → recompose rồi layout/draw có thể bỏ qua; đọc trong `Modifier.offset {}` (placement) → layout (+draw nếu đổi vị trí); đọc trong `drawBehind` → chỉ draw | phases | stable |
| B7 | Ghi state từ `onSizeChanged` rồi dùng trong layout → thêm một frame (vòng lặp phase) | phases | stable |
| B8 | Stable: so bằng `equals`; unstable khi strong skipping bật: so `===`; tắt strong skipping: composable có tham số unstable recompose mỗi lần cha recompose; List/Set/Map coi là unstable; lambda luôn coi là stable; không gắn @Stable đại trà | stability, strongskipping, lifecycle | stable / version |
| B8 | Recomposition lạc quan, có thể bị hủy; composable nên nhanh, idempotent, không side effect | mental-model, side-effects | guideline |
| B9 | Semantics tree song song, dùng cho accessibility và testing; accessibility dùng cây unmerged, test mặc định dùng merged | semantics | stable |
| B10 | Chuỗi `+1`: write → (apply) → invalidate scope đã đọc → Recomposer lên lịch → Composer chạy lại, skip con có tham số không đổi → Applier chỉ khi cấu trúc đổi → layout/draw khi cần | tổng hợp các nguồn trên | simplified |

## Điểm chưa xác minh / cách xử lý
- ~~Không có commit hash cho how-compose-works~~ → đã ghim `296313a4` (2026-11-23).
- mental-model nói composable "có thể" chạy song song nhưng ghi chú hiện chưa chạy song song → nội dung dùng "tài liệu yêu cầu viết như thể có thể chạy song song".
- Số frame, thời lượng frame: không ghi.
- Grokking Android (nguồn phụ): không dùng cho khẳng định nào.

## Sách
Không có sách riêng về Compose Runtime; chỉ dẫn chiếu Kotlin (delegation, equals) ở mức "đọc thêm", không chép.

## Checklist mục 5 (Track B) — tick 2026-11-21

| Mục | Ở đâu |
|---|---|
| Không gộp 4 vai trò | B0 `sec.roles`, model `runtime.map` (mỗi vai trò một node, ba bước riêng) |
| Runtime chung ≠ Android host | B0 `sec.roles.p.2`, node host/uitree mang trạng thái `android-impl`, callout `co.android` |
| Không khẳng định mọi `setContent` tạo Composition mới | B1 `essence` dòng 3 |
| Runtime gọi mã đã biến đổi | B1 bước `run` + `co.transformed`; B2 |
| Không "chỉ khi Snapshot đổi", không "mỗi frame một lần" | B5 essence, quiz, misconceptions `recomposer-snapshot`, `one-per-frame` |
| Không hard-code thời lượng frame | `m.recomposer.simp.2`, B5 `sec.x3.p.2` (không có số ms nào trong track) |
| Mã giả có nhãn minh họa | `code.js` (illustrative), `m.compiler.co.illustrative`, badge `impl simplified` |
| Không khuyến khích `currentComposer`/API nội bộ | B2 `sec.transform.p.2`, `m.compiler.simp.2`, misconception `manual-composer` |
| Gap buffer, `$changed` không như API ổn định; có nhánh/ngày | B3 `sec.slots.p.2`, B2 `sec.transform` (androidx-main, đọc 2026-11-21; không có commit hash, xem "Điểm chưa xác minh") |
| SlotTable ≠ "mảng Any?"; khác cây UI; cảnh báo của tài liệu | B3 `sec.slots`, quiz q2, misconception `slot-ui` |
| Applier: tính ≠ áp dụng; không chỉ Android | B6 essence, `sec.applier`, model `runtime.applier` |
| StateObject/StateRecord khái niệm; nhiều record | B4 `sec.snapshot.p.2`, `m.snapshot.simp.1` |
| Không chạy lại toàn bộ cây; recomposition ≠ redraw | B4 essence, B7 essence, misconceptions `whole-tree`, `redraw` |
| Không "thiếu key luôn tạo lại" | B3, model `runtime.keys` (4 thao tác × 2 chế độ, selfCheck thêm cuối giữ nguyên) |
| Không phải Virtual DOM nhưng có theo dõi cấu trúc | B3 essence dòng 3 |
| `AndroidComposeView`, `Owner`, `UiApplier`, `LayoutNode` gắn `android-impl` | B0, B6 `sec.applier.p.2`, B9 `sec.sem.p.2` |
| Accessibility không chỉ qua Owner; semantics song song | B9 `sec.sem`, model `runtime.semantics` |
| Stability không thành mẹo; không `@Stable` đại trà; strong skipping `version` | B8 `sec.stability`, `m.skip.co.correct`, `m.skip.co.version` |
| Composable an toàn khi chạy lại | B8 `sec.correct` |
| Chỉ kết luận phase sau khi chỉ ra nơi đọc | model `runtime.phases`: bước 1 luôn là "State được đọc ở đâu?" |
| Luồng `+1` đủ 8 bước | model `runtime.counter` (selfCheck "luôn đủ 8 bước") |
| Hiểu lầm ≥ 8, có nguồn | 9 mục |
| Release notes không là nguồn duy nhất; Grokking chỉ bổ trợ | `rt-releases` chỉ dùng cho phiên bản (B0); Grokking không dùng |

**Đã xử lý 2026-11-21:** mỗi khối của sơ đồ B0 bấm được (chuột, Enter, Space; `role=button`, `aria-pressed`, nhãn "Chọn {tên}") qua `view.nodeAction: 'focus'` trong lõi; ô chọn "Thành phần" vẫn giữ làm cách thứ hai. (Trước đó là lệch spec có chủ ý vì lời nhắc tác vụ tự động cấm sửa `js/core`.)

## Runtime v2 (từ 2026-11-22)

**Ghim phiên bản cho chi tiết nội bộ:**
- AndroidX `androidx-main` tại commit **`296313a488a01c84ddcb0801d4efee640a14070c`** (21/11/2026), lấy từ `+log/androidx-main?format=JSON`.
- `how-compose-works.md` đọc toàn văn tại đúng commit đó.
- Phiên bản thư viện vẫn là Compose 1.13.0 (BOM 2026.11.01), Kotlin 2.4.21.

### DC · Tư duy khai báo và luật của thân composable

**Đã đọc:**
- Kunneth Ch.2 (trang PDF 42–61) và Ch.3 (trang PDF 62–86, phần composable functions và composing/recomposing);
- "Thinking in Compose" (`cp-mental`), toàn văn, 2026-11-22.

| Claim | Nguồn | Loại |
|---|---|---|
| Hệ View: inflate thành cây đối tượng, setter, view binding; ví dụ Hello View; hạn chế kế thừa (Button/ImageButton, padding/margin) | Kunneth Ch.2 | Ví dụ của sách |
| Hai rủi ro của cập nhật thủ công (quên một nơi; cập nhật node vừa bị gỡ) | `cp-mental` | stable |
| Khai báo: tạo lại khái niệm cả màn hình, chỉ áp thay đổi cần thiết; Compose chọn phần cần chạy | `cp-mental` | stable |
| Composable trả `Unit` (ví dụ `println`); chuỗi Text → BasicText → CoreText → Layout → ReusableComposeNode; node có MeasurePolicy, LayoutDirection, Density, Modifier | Kunneth Ch.3 | Theo phiên bản Compose của sách; **ghi rõ trong nội dung, sẽ đối chiếu lại ở B6** |
| `currentComposer` là nội bộ, không gọi | `rt-pkg` | stable |
| Năm điều: skip, lạc quan/hủy, chạy thường xuyên, song song, thứ tự bất kỳ; ví dụ SharedPrefsToggle, ListWithBug, ButtonRow | `cp-mental` | stable |
| HIỆN TẠI composable không chạy song song; Compose chạy trên luồng main | `cp-mental` (hai ghi chú "Note") | stable. **Sách (Kunneth) viết "có thể xảy ra song song": site sửa theo tài liệu** |
| Sim `runtime.runs`: 11/5/4 lần | Kịch bản của site (2 frame animation, một lần hủy, là giả định) | selfCheck; nhãn giản lược |

### B2 · Compiler transform: $composer, group, changed(), skip, restart (viết lại 2026-11-23)

**Đã đọc:**
- `how-compose-works.md` @296313a4, toàn văn: Purpose of the Composer, Positional Memoization, Slot Table, Compiler Plugin, Skipping, Restarting, `$changed`.
- `Composer.kt`, `GapComposer.kt`, `RecomposeScopeImpl.kt`, `ComposeRuntimeFlags.kt` @296313a4: phần skipping, changed/changedInstance, startRestartGroup/addRecomposeScope, endRestartGroup, skipToGroupEnd/recomposeToGroupEnd.
- Ba sách Compose trong kho không có chương về nội bộ compiler.

| Claim | Nguồn | Loại |
|---|---|---|
| Composer có ba việc: ghi vị trí (remember, tham số), phát hiện thay đổi, tính lại từng phần | `rt-how` | impl |
| Composer là tham số ẩn của mọi hàm `@Composable`; lời gọi do plugin chèn | `rt-how` | impl |
| Nhớ theo vị trí; ví dụ A/B: 2 Data lần đầu, 0 lần gọi lambda khi recompose | `rt-how` | impl |
| Luật slot: số slot của group cố định khi cập nhật; slot có điều kiện cần group có điều kiện; group con đã chèn thì cha không thêm slot | `rt-how` | impl |
| `key` của group do compiler tính từ vị trí trong mã nguồn | `rt-composer-src` (KDoc `startReplaceableGroup`, `startRestartGroup`) | impl |
| `startReplaceGroup` thay `startReplaceableGroup` (cũ, chỉ để tương thích); `startMovableGroup` cho `key()` | `rt-composer-src` | impl |
| `skipping` = !inserting && !reusing && !providersInvalid && requiresRecompose == false && !forciblyRecompose; KDoc nêu ví dụ `staticCompositionLocalOf` | `rt-gapcomposer`, `rt-composer-src` | impl |
| `changed(v)`: `nextSlot() != v` → ghi và trả true; `changedInstance` dùng `!==` | `rt-gapcomposer` | impl |
| Mẫu `||` không short-circuit: `changed()` gọi vào `val` trước `if` | `rt-how` | impl |
| `Boolean.or` không short-circuit | `kt-boolean-or` | stable |
| `startRestartGroup` → `addRecomposeScope`: scope lưu vào một slot của group; `requiresRecompose = invalidation != null \|\| forcedRecompose` | `rt-gapcomposer` | impl |
| `endRestartGroup()` trả null khi không có lần đọc quan sát được (impl: `scope.used \|\| forceRecomposeScopes`, và scope không bị skip) | `rt-how`, `rt-gapcomposer` | impl |
| Mã của B không được giả định gì về `Person` ngoài khai báo kiểu (module khác có thể đổi) | `rt-how` | impl |
| `skipToEndGroup` restart con bị invalidate trước khi trả về; impl `skipToGroupEnd` → `recomposeToGroupEnd` khi còn invalidation | `rt-how`, `rt-gapcomposer` | impl |
| Tên thật: `skipToGroupEnd`; lambda `updateScope` nhận `(Composer, Int)` | `rt-composer-src` | impl |
| Hai cài đặt Composer: GapComposer (mặc định), LinkComposer sau cờ `isLinkBufferComposerEnabled` (mặc định false) | `ComposeRuntimeFlags.kt` @296313a4 | impl, version |
| `$changed`: chỉ nêu tên và mục đích; tài liệu nói nằm ngoài phạm vi | `rt-how` | impl |
| Strong skipping so tham số không ổn định theo địa chỉ, mặc định từ Kotlin 2.0.20 | Đã ghi ở B8 (v1); chương B8 v2 sẽ đối chiếu lại | stable / version |
| Xem mã thật: Tools → Kotlin → Show Kotlin Bytecode → Decompile | Hướng dẫn của site; kết quả tùy phiên bản | version |
| Sim `runtime.groups`: 3 group / 5 slot (mô hình tài liệu), 4 kịch bản, biến thể giả định | Kịch bản của site, theo mã giả của tài liệu | selfCheck; nhãn giản lược (số slot thật lớn hơn) |

### B3 · SlotTable, thay đổi cấu trúc, identity (viết lại 2026-11-23)

**Đã đọc:**
- `how-compose-works.md` @296313a4, các mục The Slot Table, Detecting Structural Changes (Deletes, Inserts, Moves), Content Identity, Duplicate keys;
- "Lifecycle of composables" (`cp-lifecycle`), toàn văn, 2026-11-23.

| Claim | Nguồn | Loại |
|---|---|---|
| SlotTable: cây group trải thành 2 mảng (group, slot), tránh boxing; 6 trường trong 5 số nguyên; không có con trỏ con; Parent/Size thừa nhau nhưng giữ cả hai; số slot = hiệu chỉ số slot | `rt-how` | impl |
| Bảng ví dụ của tài liệu đảo key 1234/4567 so với ví dụ mã; site đổi lại cho khớp và ghi chú | `rt-how` | Ghi chú của site |
| SlotReader/SlotWriter: một writer khi không có reader; nhiều reader khi không có writer; gap buffer, index/address, anchor | `rt-how` | impl |
| Ký hiệu chuỗi group; so tuần tự với bảng cũ khi phát group | `rt-how` | impl |
| Xóa: Pending (bảng băm theo key) ở chỗ lệch; dời Email về #5; `/G` xóa phần còn lại; index node theo tổng node; gộp thao tác liền kề | `rt-how` | impl |
| Chèn: insert table riêng vì bảng chính chỉ đọc trong composition; chèn ở #5, node index 1 | `rt-how` | impl |
| Di chuyển: hiện chỉ `key` sinh ra; runtime tổng quát; ví dụ đảo thứ tự; gộp di chuyển liền kề | `rt-how` | impl |
| Danh tính = call site; ví dụ Counters/showMiddle; flow-control group quanh `if` | `rt-how` | impl |
| Ở commit ghim, group của `if`/`when` dùng `startReplaceGroup` | `rt-composer-src` | impl |
| Key trùng trả theo thứ tự bảng cũ (ví dụ repeat + Text có điều kiện) | `rt-how` | impl |
| Call site, thứ tự thực thi; thêm cuối dùng lại; chèn đầu/giữa, xóa, đổi chỗ làm recompose và effect chạy lại; `key()` chỉ cần duy nhất trong call site; `LazyColumn items(key)`; ví dụ LoginScreen | `cp-lifecycle` | stable |
| Sim `runtime.structure`: 5 kịch bản (xóa, chèn, di chuyển, Counters không/có group `if`) | Theo lời mô tả của tài liệu; kịch bản không group là giả định | selfCheck; nhãn giản lược |

### B4 · State và Snapshot (viết lại 2026-11-23)

**Đã đọc:**
- Snapshot reference và SnapshotMutationPolicy reference, toàn văn;
- "State and Jetpack Compose" (`and-state`) và mục derivedStateOf/snapshotFlow của "Side-effects in Compose" (`and-effects`), 2026-11-23;
- `SnapshotState.kt`, `snapshots/Snapshot.kt` (readable/valid), `DerivedState.kt`, `RecomposeScopeImpl.kt` (isInvalidFor), `Composition.kt` và `GlobalSnapshotManager.android.kt` @296313a4;
- Kunneth Ch.5 (đọc toàn văn; phần stateless/hoisting/rememberSaveable/ViewModel dành cho chương SH).

| Claim | Nguồn | Loại |
|---|---|---|
| State/MutableState; scope đọc `value` được đăng ký; so với `Delegates.observable`; `remember(key)` (RememberWithKeyDemo) | Kunneth Ch.5, `and-state` | stable; ví dụ của sách |
| Ba cách khai báo MutableState; remember không giữ qua đổi cấu hình | `and-state` | stable |
| Read observer cho composition/layout/draw; write observer; registerGlobalWriteObserver; sendApplyNotifications hoãn thông báo ghi global; apply mutable snapshot ngầm gửi | `rt-snapshot` | stable |
| Android: GlobalSnapshotManager, Channel(1), AndroidUiDispatcher.Main | `ui-globalsnap` | android-impl |
| Snapshot cách ly, enter theo luồng, apply nguyên tử, dispose, xung đột; composition dùng mutable snapshot và lên lịch lại khi apply thất bại | `rt-snapshot` | stable |
| Record đọc được = record hợp lệ có id lớn nhất (id ≤ snapshot, không thuộc invalid set) | `rt-snapshot-src` | impl |
| mutableStateOf mặc định structuralEqualityPolicy; setter bỏ qua giá trị tương đương; mergeRecords giữ current khi tương đương, gọi merge khi không | `rt-state-src` | impl |
| Ba policy có sẵn; equivalent/merge; ví dụ counterPolicy | `rt-policy`, `SnapshotMutationPolicy.kt` | stable |
| derivedStateOf: dùng đúng/sai (firstVisibleItemIndex, fullName); đắt | `and-effects` | stable |
| Scope chỉ đọc derived state là "conditional"; `isInvalidFor` dùng policy hoặc structural equality | `rt-derived-src`, `RecomposeScopeImpl.kt` | impl. KDoc @296313a4 nói derived state không có policy "trigger updates on each dependency change"; với composition, so sánh `isInvalidFor` vẫn chặn recompose khi kết quả không đổi |
| ArrayList/mutableListOf/data class `var` không quan sát được; dùng State<List> + listOf hoặc mutableStateListOf | `and-state` | stable |
| collectAsStateWithLifecycle / collectAsState / observeAsState; snapshotFlow lạnh, phát khi khác lần trước | `and-state`, `and-effects` | stable |
| Sim `runtime.records`: 4 tổ hợp (structural/counter × +20/=10) | Theo reference (counterPolicy) và mã @296313a4 | selfCheck; id snapshot minh họa |

### SH · Quản lý state (chương mới, 2026-11-23)

**Đã đọc:**
- Sách: Kunneth Ch.5 (toàn văn), Jetpack Compose by Tutorials Ch.7 (phần lý thuyết: UI update loop, UDF, ViewModel), Jetpack Compose 1.3 Essentials Ch.20 (20.1–20.8).
- Tài liệu: "Where to hoist state" (`cp-hoisting`), "Save UI state in Compose" (`cp-saving`) và phần hoisting/rememberSaveable của "State and Jetpack Compose" (`and-state`), 2026-11-23.

| Claim | Nguồn | Loại |
|---|---|---|
| Vòng cập nhật UI (event, update state, display state); rắc rối của hệ View; lợi ích UDF | Tutorials Ch.7 | Ví dụ của sách |
| FunctionA/FunctionB (Switch); NameField/NameText hoist lên MainScreen; rememberSaveable qua xoay màn hình | Essentials Ch.20 | Ví dụ của sách |
| Stateful/stateless, idempotent; TextFieldDemo hai bản; TemperatureRadioButton/calc lambda; `MutableState` làm tham số; ViewModel + LiveData + observeAsState (lifecycle 2.4.0) | Kunneth Ch.5 | Ví dụ của sách; mẫu `MutableState` làm tham số và LiveData được ghi là cách của sách, kèm mẫu hiện tại |
| Ba luật hoist; underhoisting; `rememberSaveable` không giữ khi người dùng đóng hẳn activity | `and-state` | stable |
| Screen UI state / UI element state; business / UI logic; composable, plain state holder, ViewModel làm chủ; tổ tiên chung thấp nhất; không truyền ViewModel xuống; property drilling; caveat MonotonicFrameClock (DrawerState.close) | `cp-hoisting` | stable |
| Đổi cấu hình, process death do hệ thống, khác người dùng đóng hẳn; giữ tối thiểu input và state điều hướng; rememberSaveable + Saver; giới hạn Bundle, TransactionTooLarge; ViewModel không qua process death → SavedStateHandle; StateRestorationTester | `cp-saving` | stable |
| Sim `runtime.survive`: 5 nơi giữ × 4 sự kiện | Bảng suy từ `cp-saving` và `and-state` | selfCheck; nhãn giản lược |
