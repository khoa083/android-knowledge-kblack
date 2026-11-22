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

### B5 · Recomposer và frame clock (viết lại 2026-11-23)

**Đã đọc:**
- `Recomposer.kt` @296313a4: `runRecomposeAndApplyChanges`, `awaitWorkAvailable`, `recordComposerModifications`, `hasBroadcastFrameClockAwaiters`, `pause/resumeCompositionFrameClock`;
- `AndroidUiFrameClock.android.kt` và `WindowRecomposer.android.kt` @296313a4;
- Recomposer và MonotonicFrameClock reference. Ba sách Compose không có chương về Recomposer.

| Claim | Nguồn | Loại |
|---|---|---|
| Vòng lặp: awaitWorkAvailable → recordComposerModifications (không có việc theo frame thì không xin frame) → withFrameNanos | `rt-recomposer-src` | impl |
| Trong frame: sendFrame cho awaiter + sendApplyNotifications trước; recompose (lặp khi giá trị đọc bởi composition khác đổi); applyChanges | `rt-recomposer-src` | impl |
| Effect chạy trong context có broadcastFrameClock của Recomposer | `rt-recomposer-src` (recompositionRunner: withContext(broadcastFrameClock)) | impl |
| withFrameNanos semantics, thời điểm tăng nghiêm ngặt | `rt-frameclock` | stable |
| Android: Choreographer.postFrameCallback; đặt sau đợt dispatch của AndroidUiDispatcher | `ui-frameclock` | android-impl |
| Recomposer theo window; clock bắt đầu tạm dừng; ON_START resume; ON_STOP pauseCompositionFrameClock; ON_DESTROY cancel | `ui-windowrecomposer` | android-impl |
| viewModelScope không có frame clock (DrawerState.close) | `cp-hoisting` | stable |
| Sim `runtime.frame`: 3 kịch bản | Theo vòng lặp ở commit ghim; số frame animation là giả định | selfCheck; nhãn giản lược |

### EF · Side effect và vòng đời (chương mới, 2026-11-23)

**Đã đọc:**
- "Side-effects in Compose" (`and-effects`), toàn văn;
- `Effects.kt`, `RememberObserver.kt` @296313a4;
- Kunneth Ch.7 (mục Understanding side effects), Tutorials Ch.11 (rememberCoroutineScope, Effects in Compose, Migrate Effects).

| Claim | Nguồn | Loại |
|---|---|---|
| Định nghĩa side effect và effect; dùng trong môi trường biết vòng đời; đừng lạm dụng, giữ UDF | `and-effects` | stable |
| LaunchedEffect: launch khi vào, hủy khi rời, khởi động lại khi key đổi; LaunchedEffect(true) đáng ngờ như while(true) | `and-effects` | stable |
| LaunchedEffect(key) = remember(key) { LaunchedEffectImpl }; launch ở onRemembered, hủy ở onForgotten/onAbandoned; không key là lỗi | `rt-effects-src` | impl |
| onRemembered/onForgotten trên apply thread; onAbandoned khi không được remember thành công | `rt-remember-observer` | impl |
| KDoc: không dùng LaunchedEffect để launch việc theo callback qua MutableState làm key; dùng rememberCoroutineScope | `rt-effects-src` | impl |
| rememberCoroutineScope; quy tắc key; rememberUpdatedState (LandingScreen); DisposableEffect + lifecycle observer, onDispose bắt buộc; SideEffect sau mỗi lượt thành công; produceState conflate, awaitDispose, đặt tên chữ thường | `and-effects` | stable |
| SideEffect = recordSideEffect | `rt-effects-src` | impl |
| LaunchedEffectDemo (Start/Restart/Stop), log init/dispose của DisposableEffect | Kunneth Ch.7 | Ví dụ của sách; sim là biến thể (ghi trong simp.2) |
| Cẩm nang chuyển đổi onActive/onCommit → effect hiện tại | Tutorials Ch.11 | Lịch sử (API cũ) |
| Sim `runtime.effects`: bộ đếm, hẹn giờ có/không rememberUpdatedState | Theo `and-effects` và Effects.kt | selfCheck; nhãn giản lược |

### CL · CompositionLocal và slot API (chương mới, 2026-11-23)

**Đã đọc:**
- "Locally scoped data with CompositionLocal" (`cp-compositionlocal`), toàn văn, 2026-11-23;
- `CompositionLocal.kt` @296313a4 (KDoc của compositionLocalOf/staticCompositionLocalOf);
- Essentials Ch.21 (CompLocalDemo) và Ch.22 (slot API).

| Claim | Nguồn | Loại |
|---|---|---|
| Truyền ngầm theo cây; Composition khác cây UI; MaterialTheme dùng 3 CompositionLocal; nhà cung cấp gần nhất; LocalContext; tiền tố Local | `cp-compositionlocal` | stable |
| compositionLocalOf chỉ invalidate nơi đọc; static không theo dõi, recompose cả content | `cp-compositionlocal`, `rt-local-src` | stable |
| KDoc: static cho Context/font loader; màu/theme có thể đổi hoặc animate → compositionLocalOf | `rt-local-src` | impl. Essentials dùng static cho màu: ghi là lựa chọn của sách |
| Liên hệ getter skipping (`!providersInvalid`) | `rt-gapcomposer` | impl |
| Nhược điểm, hai điều kiện (mặc định tốt, gắn với cây); không đặt ViewModel; thay thế: tham số, đảo điều khiển, content lambda | `cp-compositionlocal` | stable |
| Cây Composable1–8, phạm vi theo nhánh, nhánh khác nhận giá trị mặc định | Essentials Ch.21 | Ví dụ của sách |
| Slot API (SlotDemo, cú pháp lambda cuối) | Essentials Ch.22 | Ví dụ của sách |
| Sim `runtime.locals`: dynamic recompose 2, static recompose 4 | Theo KDoc và tài liệu | selfCheck; nhãn giản lược |

### B6 · Composer ghi nhận, Applier áp dụng (viết lại 2026-11-23)

**Đã đọc:** `Applier.kt` (KDoc insertTopDown/insertBottomUp, AbstractApplier), `Composables.kt` (ComposeNode), `Composer.kt` (Updater.set), `UiApplier.android.kt`, `Layout.kt`, `BasicText.kt` @296313a4; Applier reference.

| Claim | Nguồn | Loại |
|---|---|---|
| Recompose trước, applyChanges sau trong cùng frame; lượt bị bỏ không đụng cây | `rt-recomposer-src`, `rt-how` | impl |
| ComposeNode: startNode, createNode (khi chèn) / useNode, Updater, endNode; factory không bảo đảm gọi tại chỗ | `rt-composenode-src` | impl |
| Updater.set chỉ apply khi đang chèn hoặc giá trị khác giá trị đã nhớ | `rt-composer-src` (Updater trong Composer.kt) | impl |
| Applier: current, down/up, insertTopDown/BottomUp (chỉ một), remove, move, clear, apply, onBegin/EndChanges; AbstractApplier dùng Stack | `rt-applier-src`, `rt-applier` | impl / stable |
| Ví dụ R → B → (A, C): báo tổ tiên TD 5 / BU 3; báo cây con TD 3 / BU 5 | `rt-applier-src` (KDoc) | impl. KDoc dùng từ "exponentially"; site ghi "tăng nhanh hơn nhiều so với số node" |
| UiApplier bỏ qua insertTopDown, chèn trong insertBottomUp; onEndChanges → owner.onEndApplyChanges | `ui-uiapplier` | android-impl |
| BasicText (chuỗi đơn giản) → Layout(modifier TextStringSimpleElement) → ReusableComposeNode; CoreText là bản của sách (Kunneth Ch.3) | `ui-layout-src`, Kunneth Ch.3 | impl; ghi chú lệch phiên bản |
| Sim `runtime.insert`: 4 tổ hợp | Theo KDoc Applier | selfCheck |

### B7 · Ba phase và đọc state theo phase (viết lại 2026-11-23)

**Đã đọc:** "Jetpack Compose phases" (`cp-phases`), toàn văn, 2026-11-23.

| Claim | Nguồn | Loại |
|---|---|---|
| Ba phase (what/where/how), so với View; thứ tự một chiều; ngoại lệ BoxWithConstraints, LazyColumn, LazyRow | `cp-phases` | stable |
| Bỏ qua việc lặp nhờ theo dõi đọc state theo phase | `cp-phases` | stable |
| Layout ba bước, ví dụ Row(Image, Column(Text, Text)), mỗi node thăm một lần (tuyến tính) | `cp-phases` | stable |
| Đọc theo phase: composition; layout (measurement, placement có restart scope riêng; draw nếu kích thước/vị trí đổi); draw | `cp-phases` | stable |
| Tối ưu parallax bằng Modifier.offset { }; lambda có chi phí nhưng đáng; derivedStateOf để lọc | `cp-phases` | stable |
| Vòng lặp onSizeChanged qua hai frame; mẫu onSizeChanged/onGloballyPositioned | `cp-phases` | stable |
| Sim `runtime.scroll`: 3/3/3, 0/3/3, 0/0/3, vòng lặp 2 frame | Theo `cp-phases` | selfCheck; nhãn giản lược |

### LO · Layout: constraints, một lượt đo, Layout tùy chỉnh, intrinsic (chương mới 2026-11-23)

**Đã đọc:** "Custom layouts", "Compose layout basics", "Intrinsic measurements in Compose layouts", "Constraints and modifier order" (developer.android.com, toàn văn, 2026-11-23); `MeasurePolicy.kt`, `Measurable.kt`, `Layout.kt`, `SubcomposeLayout.kt`, `MeasurePassDelegate.kt` (`trackMeasurementByParent`), `LayoutNodeLayoutDelegate.kt` (`MeasuredTwiceErrorMessage`), `ui-unit/Constraints.kt` @296313a4; Kunneth Ch.4; Essentials Ch.28, 29, 32.

| Claim | Nguồn | Loại |
|---|---|---|
| Ba bước mỗi node; không đo nhiều lượt; Modifier.layout (firstBaselineToTop); Layout (MyBasicColumn); place vs placeRelative, LocalLayoutDirection | `cp-layout-custom` | stable |
| Một lượt; cha đo trước con nhưng có kích thước/đặt sau; ví dụ Row(Image, Column(Text, Text)); lồng sâu không ảnh hưởng hiệu năng; đo và đặt là hai bước con; BoxWithConstraints | `cp-layout-basics` | stable |
| Hệ View có thể đo lại nhiều lần; Compose đo một lần, đo lại ném exception; source Column → Layout + MeasurePolicy; SimpleFlexBox; mô tả DefaultIntrinsicMeasurable | Kunneth Ch.4 | Ví dụ của sách (khớp mã ghim) |
| "2^10 lần" là phép tính minh họa cho giả định mỗi tầng đo hai lần, tài liệu chỉ nói "a lot of work" | `cp-layout-basics` | site tự diễn giải, ghi là giả định |
| Constraints: 4 giá trị, Infinity = Int.MAX_VALUE, hasBounded*, fixed* | `ui-constraints-src` | impl |
| 4 loại constraints; fillMaxSize().size(50.dp) → 300×200; wrapContentSize; requiredSize tràn và căn giữa | `cp-constraints-mod` | stable |
| KDoc MeasurePolicy: không thương lượng; con ngoài constraints bị ép, căn giữa, measuredWidth/Height; định nghĩa 4 intrinsic; mặc định chạy measure với DefaultIntrinsicMeasurable, "best effort" | `ui-measurepolicy-src` | impl |
| Đo lần hai ném IllegalStateException (thông điệp MeasuredTwiceErrorMessage); đo được trong khối measure hoặc layout | `ui-measure-once` | impl |
| exampleLayout: tọa độ là độ lệch so với vị trí mặc định; CascadeLayout đo trong khối layout | Essentials Ch.28–29 | Ví dụ của sách |
| IntrinsicSize Min/Max với Text (từ dài nhất / cả dòng); width(IntrinsicSize.Max) cho Column | Essentials Ch.32 | Ví dụ của sách |
| Intrinsic hỏi trước khi đo, không đo hai lần; TwoTexts + VerticalDivider; minIntrinsicHeight Row = max con, divider 0; override phải khớp measure | `cp-intrinsics` | stable |
| SubcomposeLayout: 3 trường hợp dùng; subcompose(slotId) và slotId phải equals giữa các lần đo | `ui-subcompose-src` | impl |
| Sim `runtime.measure`: cột 3 lần đo; đo hai lần → pitfall; Row không intrinsic → divider 640; IntrinsicSize.Min → 3 hỏi, 3 đo, cao 72 | Theo tài liệu và mã ghim | selfCheck; số px minh họa; thứ tự đo weight trong Row giản lược (simp.2) |

### MD · Modifier: chuỗi, thứ tự, kích thước, Modifier.Node (chương mới 2026-11-23)

**Đã đọc:** "Compose modifiers", "Create custom modifiers", "Migrate from Modifier.composed to Modifier.Node" (bản tóm tắt), "Constraints and modifier order" (developer.android.com, 2026-11-23); `Modifier.kt`, `ModifierNodeElement.kt`, `NodeChain.kt` (`updateFrom`, `actionForModifiers`, `Differ`), foundation `Background.kt`, foundation-layout `Padding.kt` @296313a4; Tutorials Ch.6; Essentials Ch.24.

| Claim | Nguồn | Loại |
|---|---|---|
| size→background→clip cho hình vuông; thêm background vàng sau clip; padding trước size; `modifier` vs `Modifier`; bỏ tham số padding khi đã có modifier | Tutorials Ch.6 | Ví dụ của sách |
| border/padding đổi thứ tự; tham số modifier là tham số tùy chọn đầu tiên; then; hơn 100 hàm | Essentials Ch.24 | Ví dụ của sách |
| Thứ tự quan trọng (KDoc); quy ước modifier/fooModifier, modifier mặc định nối sau | `ui-modifier-src` | impl |
| clickable/padding; không có margin; size/requiredSize/offset/matchParentSize/weight; scope an toàn, parent data modifier; trích và dùng lại, cấp phát mỗi frame với animation; reusableItemModifier | `cp-modifiers` | stable |
| clip(CircleShape).padding(10).size(100) không tròn; size(100).size(50) → 100 | `cp-constraints-mod` | stable |
| then trả về CombinedModifier, hoặc this nếu other là Modifier rỗng | `ui-modifier-src` | impl |
| ModifierNodeElement nhẹ; create/update; equals/hashCode bắt buộc; BackgroundElement so color/brush/alpha/shape | `ui-mne-src` | impl |
| updateFrom: đường nhanh khi cùng độ dài; equals → reuse, cùng lớp → update, khác → diff Myers (insert attach, remove invalidate+detach, same update nếu khác) | `ui-nodechain-src` | impl |
| Ba cách viết modifier; caveat factory @Composable; composed {} không còn khuyên dùng; circle; các loại node; shouldAutoInvalidate; coroutineScope; currentValueOf | `cp-custom-modifiers`, `cp-modifiers-node` | stable |
| Bug "blink" đổi lớp element làm animation chạy lại | Suy ra từ `ui-nodechain-src` (Replace → detach/attach) | site suy luận từ mã, ví dụ giả định |
| Sim `runtime.chain`: 4/0/0/0, 3/1/0/0, 3 giữ + 1 chèn, 3 giữ + 1 gỡ + 1 chèn | Theo NodeChain @296313a4 | selfCheck; thứ tự lệnh diff giản lược (simp.2) |

### LZ · Lazy list bên trong (chương mới 2026-11-23)

**Đã đọc:** "Lists and grids" (developer.android.com, 2026-11-23; phần Tips và Paging chỉ qua bản tóm tắt); foundation `LazyLayout.kt`, `LazyLayoutItemContentFactory.kt`, `LazySaveableStateHolder.kt`, `CheckScrollableContainerConstraints.kt`, ui `SubcomposeLayout.kt` (`disposeOrReuseStartingFromIndex`, `takeNodeFromReusables`) @296313a4; Tutorials Ch.4; Essentials Ch.34–37.

| Claim | Nguồn | Loại |
|---|---|---|
| Column tạo mọi mục; 1000 ảnh; cuộn Column theo pixel, Lazy theo chỉ số; 4 hàm suspend; stickyHeader + groupBy; firstVisibleItemIndex | Essentials Ch.34, 37 | Ví dụ của sách (bản 1.3: stickyHeader experimental) |
| Nội dung là LazyListScope.() -> Unit, không phải @Composable; "without needing to recycle" | Tutorials Ch.4 | Sách đơn giản hóa; mã ghim có pool dùng lại |
| Column compose mọi mục, lazy chỉ mục trong viewport; key theo vị trí mặc định, "stable + unique", kiểu hỗ trợ Bundle; animateItem cần key; contentPadding; derivedStateOf; snapshotFlow | `cp-lists` (nguyên văn) | stable |
| Tips (0 px, lồng cuộn, nhiều phần tử một item, contentType, đo release) | `cp-lists` (bản tóm tắt) | stable; ghi rõ trên site là bản tóm tắt |
| LazyLayout là SubcomposeLayout, compose trong bước đo là tín hiệu "đang cần"; LazyLayoutItemReusePolicy giữ 7 slot mỗi contentType (5 + 2 như RecyclerView), areCompatible so contentType | `fd-lazylayout-src` | impl |
| Slot thôi dùng vào pool ở cuối lượt đo (disposeOrReuseStartingFromIndex); mục mới lấy từ pool (takeNodeFromReusables) | `ui-subcompose-src` | impl |
| Cache lambda theo key để skip; SaveableStateProvider theo key; chỉ lưu mục đang hiện (TransactionTooLargeException) | `fd-lazycontent-src` | impl |
| Thông điệp "Vertically scrollable component was measured with an infinity maximum height constraints…" | `fd-scrollcheck-src` | impl |
| Sim `runtime.lazy`: cùng loại 5 mới/2 dùng lại; khác loại 7/0; Column 20 từ đầu | Theo mã ghim | selfCheck; bỏ qua prefetch (simp.1) |
