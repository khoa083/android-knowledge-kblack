# Sinh tracks/runtime/content.vi.js và content.en.js từ MỘT nguồn (cùng cây khoá ở hai ngôn ngữ).
# Chạy: python dev/gen/runtime_content.py   (chỉ là công cụ phát triển, site không cần file này)
import json, os, unicodedata

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
P = 'track.runtime.'
E = []
def a(k, vi, en): E.append((P + k, vi, en))
def m(model, k, vi, en): a('m.' + model + '.' + k, vi, en)

# ---------------- chung ----------------
a('title', 'Compose Runtime Explorer', 'Compose Runtime Explorer')
a('summary', 'Theo dấu một cú bấm `+1`: từ `MutableState`, Snapshot, Recomposer, Composer, Applier đến các phase và semantics.',
  'Follow a single `+1` tap: from `MutableState` through Snapshot, Recomposer, Composer, and Applier to phases and semantics.')
a('preset.counter', 'Runtime · luồng +1 đầy đủ', 'Runtime · the full +1 flow')
a('preset.keys', 'Runtime · danh sách có và không có key()', 'Runtime · a list with and without key()')
a('preset.phases', 'Runtime · state được đọc ở phase nào', 'Runtime · which phase reads the state')
a('col.subject', 'Thành phần', 'Component')
for k, vi, en in [('host', 'ComposeView ‹android-impl›', 'ComposeView ‹android-impl›'), ('composition', 'Composition', 'Composition'), ('recomposer', 'Recomposer', 'Recomposer'),
                  ('compiler', 'Mã đã biến đổi', 'Transformed code'), ('composer', 'Composer', 'Composer'), ('slots', 'SlotTable', 'SlotTable'),
                  ('snapshot', 'Snapshot / state', 'Snapshot / state'), ('applier', 'Applier', 'Applier'), ('uitree', 'LayoutNode ‹android-impl›', 'LayoutNode ‹android-impl›'),
                  ('phases', 'Layout và Drawing', 'Layout and Drawing'), ('semantics', 'Semantics tree', 'Semantics tree')]:
    a('n.' + k, vi, en)
for k, vi, en in [('focus', 'đang xem', 'in focus'), ('androidImpl', 'android-impl', 'android-impl'), ('runtime', 'runtime', 'runtime'),
                  ('hasContent', 'đã nhận nội dung', 'content set'), ('none', 'chưa có', 'not yet'), ('attached', 'đã gắn window', 'attached'),
                  ('created', 'đã tạo', 'created'), ('composing', 'đang compose', 'composing'), ('recording', 'đang ghi nhận', 'recording'),
                  ('filled', 'có group', 'has groups'), ('applying', 'đang áp dụng', 'applying'), ('built', 'đã dựng', 'built'), ('ran', 'đã chạy', 'ran'),
                  ('kept', 'giữ nguyên', 'kept'), ('moved', 'di chuyển, giữ state', 'moved, state kept'), ('recomposed', 'recompose', 'recomposed'),
                  ('rerun', 'chạy lại', 'runs again'), ('skipped', 'bỏ qua', 'skipped'), ('idle', 'chờ', 'waiting'),
                  ('skippedNode', 'được skip', 'skipped'), ('recomposedNode', 'recompose', 'recomposed'), ('merged', 'merged', 'merged'), ('unmerged', 'unmerged', 'unmerged')]:
    a('st.' + k, vi, en)

# ---------------- B0: bản đồ ----------------
M = 'map'
m(M, 'title', 'Bản đồ runtime: chọn một thành phần', 'Runtime map: pick a component')
m(M, 'overview', 'Sơ đồ này dùng lại trong cả track. Chọn một thành phần ở ô "Thành phần" để xem nó là gì, nhận gì và chuyển gì cho thành phần kế tiếp.',
  'This diagram is reused across the whole track. Pick a component in the "Component" box to see what it is, what it receives and what it hands on.')
m(M, 'wrapup', 'Composition, Recomposer, Composer và Applier là bốn vai trò khác nhau, không phải một "engine". Các chương B1–B10 đi sâu từng vai trò.',
  'Composition, Recomposer, Composer and Applier are four different roles, not one "engine". Chapters B1–B10 look at each role in depth.')
m(M, 'simp.1', 'Sơ đồ chỉ giữ các thành phần chính; mũi tên là quan hệ khái niệm, không phải lời gọi hàm thật.',
  'The diagram keeps only the main components; arrows are conceptual relations, not real function calls.')
m(M, 'ctl.hint', 'Chọn thành phần; ba bước bên dưới đổi theo lựa chọn.', 'Pick a component; the three steps below change with it.')
m(M, 'ctl.focus', 'Thành phần', 'Component')
m(M, 'diagramTitle', 'Sơ đồ Compose Runtime', 'Compose Runtime diagram')
m(M, 'diagramDesc', 'Mười một thành phần từ host tới semantics tree, nối bằng mũi tên theo hướng dữ liệu đi.', 'Eleven components from the host to the semantics tree, joined by arrows in the direction data flows.')
m(M, 's.what.title', 'Thành phần này là gì?', 'What is this component?')
m(M, 's.input.title', 'Nó nhận gì?', 'What does it receive?')
m(M, 's.output.title', 'Nó chuyển gì đi, đọc thêm ở đâu?', 'What does it hand on, and where to read more?')
m(M, 'ev.what', 'vai trò', 'role')
m(M, 'st.chapter', 'Chương chi tiết', 'Detailed chapter')
m(M, 'ev.in', 'đầu vào', 'input')
m(M, 'ev.out', 'đầu ra', 'output')
m(M, 'co.try', 'Đổi "Thành phần" để đi hết sơ đồ; mỗi lựa chọn dẫn tới chương chi tiết.', 'Change "Component" to walk the diagram; each choice points to a detailed chapter.')
m(M, 'co.android', 'Thành phần này thuộc phần Android của Compose UI, không phải runtime chung. [[badge:android-impl]]', 'This component belongs to the Android part of Compose UI, not the shared runtime. [[badge:android-impl]]')
MAPC = {
 'host': ('`ComposeView` (hoặc `setContent` của Activity) là View chứa nội dung Compose và nối nó với vòng đời View/window.',
          '`ComposeView` (or an Activity\'s `setContent`) is a View that hosts Compose content and ties it to the View/window lifecycle.',
          'Nội dung composable qua `setContent`, và việc được gắn vào window.', 'Composable content through `setContent`, and being attached to a window.',
          'Tạo Composition ban đầu. Chi tiết ở chương B1.', 'It creates the initial Composition. Details in chapter B1.', '[[src:rt-composeview]]'),
 'composition': ('Composition giữ kết quả của việc chạy các composable cho một cây UI.', 'A Composition holds the result of running composables for one UI tree.',
          'Nội dung từ host và yêu cầu recompose từ Recomposer.', 'Content from the host and recompose requests from the Recomposer.',
          'Gọi mã composable đã biến đổi, qua Composer. Chi tiết ở B1.', 'It runs the transformed composable code through the Composer. Details in B1.', '[[src:rt-how]]'),
 'recomposer': ('Recomposer là bộ lập lịch cho recomposition và việc áp dụng thay đổi của một hoặc nhiều Composition.', 'The Recomposer schedules recomposition and the applying of changes for one or more Compositions.',
          'Thông báo rằng có scope bị invalidate (từ Snapshot) và nhịp frame.', 'Notice that scopes were invalidated (from Snapshot) and the frame timing.',
          'Yêu cầu Composition recompose phần bị invalidate rồi apply. Chi tiết ở B5.', 'It asks the Composition to recompose what was invalidated, then apply. Details in B5.', '[[src:rt-recomposer]]'),
 'compiler': ('Compose Compiler là Kotlin compiler plugin; nó biến đổi hàm `@Composable` để làm việc với Composer.', 'The Compose Compiler is a Kotlin compiler plugin; it transforms `@Composable` functions to work with the Composer.',
          'Mã Kotlin bạn viết (lúc build, không phải lúc chạy).', 'The Kotlin code you write (at build time, not at run time).',
          'Mã có group và điểm kiểm tra skip; lúc chạy, mã này gọi Composer. Chi tiết ở B2.', 'Code with groups and skip checks; at run time it calls the Composer. Details in B2.', '[[src:rt-how]]'),
 'composer': ('Composer là giao diện mà mã sinh ra gọi tới: nhớ theo vị trí, phát hiện thay đổi, chạy lại tăng dần.', 'The Composer is the interface the generated code calls: positional memoization, change detection, incremental re-run.',
          'Lời gọi từ mã đã biến đổi (group, tham số, `remember`).', 'Calls from the transformed code (groups, parameters, `remember`).',
          'Ghi vào SlotTable và tạo danh sách thay đổi cho Applier. Chi tiết ở B6.', 'It writes to the SlotTable and produces a list of changes for the Applier. Details in B6.', '[[src:rt-how]]'),
 'slots': ('SlotTable là dữ liệu có cấu trúc theo group và vị trí, dùng để nhớ giá trị và nhận diện từng phần của composition. Nó không phải cây UI.', 'The SlotTable is data organised by groups and positions, used to remember values and identify parts of the composition. It is not the UI tree.',
          'Group và giá trị do Composer ghi.', 'Groups and values written by the Composer.',
          'Giá trị đã nhớ cho lần chạy sau. Chi tiết ở B3.', 'Remembered values for the next run. Details in B3.', '[[src:rt-how]] [[badge:impl]]'),
 'snapshot': ('Snapshot là hệ thống state của Compose: state object như `mutableStateOf` được đọc và ghi qua snapshot.', 'Snapshot is the state system of Compose: state objects such as `mutableStateOf` are read and written through snapshots.',
          'Lần đọc (để ghi nhận ai phụ thuộc) và lần ghi (ví dụ `count++`).', 'Reads (to record who depends on what) and writes (such as `count++`).',
          'Báo cho Recomposer các scope đã đọc state vừa đổi. Chi tiết ở B4.', 'It tells the Recomposer which scopes read the state that changed. Details in B4.', '[[src:rt-snapshot]]'),
 'applier': ('Applier áp dụng các thao tác trên cây (chèn, xóa, di chuyển, cập nhật) mà composition phát ra.', 'The Applier applies the tree operations (insert, remove, move, update) emitted by the composition.',
          'Danh sách thay đổi từ Composer.', 'The list of changes from the Composer.',
          'Cây node được cập nhật. Applier là điểm mở rộng cho nhiều loại cây. Chi tiết ở B6.', 'An updated node tree. The Applier is an extension point for many kinds of trees. Details in B6.', '[[src:rt-applier]]'),
 'uitree': ('Trên Android, Compose UI dựng cây `LayoutNode`; đây là cây được đo, đặt và vẽ.', 'On Android, Compose UI builds a tree of `LayoutNode`s; this is the tree that is measured, placed and drawn.',
          'Thao tác từ Applier.', 'Operations from the Applier.',
          'Đầu vào cho Layout, Drawing và semantics. Chi tiết ở B6, B9.', 'The input for Layout, Drawing and semantics. Details in B6, B9.', '[[src:rt-applier]] [[badge:android-impl]]'),
 'phases': ('Sau Composition, Compose UI chạy Layout (đo và đặt) và Drawing (vẽ) khi cần.', 'After Composition, Compose UI runs Layout (measure and place) and Drawing when needed.',
          'Cây UI và các lần đọc state trong layout hoặc draw.', 'The UI tree and state reads made during layout or drawing.',
          'Điểm ảnh trên màn hình. Chi tiết ở B7.', 'Pixels on the screen. Details in B7.', '[[src:cp-phases]]'),
 'semantics': ('Semantics tree là cây song song mô tả ý nghĩa của phần tử UI.', 'The semantics tree is a parallel tree that describes what UI elements mean.',
          'Thuộc tính semantics từ composable và modifier.', 'Semantic properties from composables and modifiers.',
          'Dịch vụ trợ năng và framework kiểm thử dùng cây này. Chi tiết ở B9.', 'Accessibility services and the testing framework use this tree. Details in B9.', '[[src:cp-semantics]]'),
}
for f, (wv, we, iv, ie, ov, oe, src) in MAPC.items():
    m(M, 'c.' + f + '.what', wv, we); m(M, 'c.' + f + '.in', iv, ie); m(M, 'c.' + f + '.out', ov, oe)
    m(M, 'c.' + f + '.src', 'Nguồn: ' + src, 'Source: ' + src)

# ---------------- B1: setContent ----------------
M = 'setcontent'
m(M, 'title', 'Từ setContent tới khung hình đầu tiên', 'From setContent to the first frame')
m(M, 'overview', 'Một `ComposeView` nhận nội dung qua `setContent`. Chọn điều gì kích hoạt composition ban đầu và xem các thành phần lần lượt làm việc.',
  'A `ComposeView` receives content through `setContent`. Pick what triggers the initial composition and watch the components work in turn.')
m(M, 'wrapup', 'Composition ban đầu xảy ra khi view được gắn vào window hoặc khi gọi `createComposition()`, cái nào đến trước; nếu tắt việc tạo khi gắn, nó vẫn xảy ra ở lần measure đầu.',
  'The initial composition happens when the view is attached to a window or when `createComposition()` is called, whichever comes first; if creation on attach is turned off, it still happens at the first measure.')
m(M, 'simp.1', 'Mô hình bỏ qua `ViewCompositionStrategy`, LifecycleOwner và SavedStateRegistryOwner mà ComposeView cần.', 'The model leaves out the `ViewCompositionStrategy`, LifecycleOwner and SavedStateRegistryOwner that ComposeView needs.')
m(M, 'ctl.hint', 'Đổi cách kích hoạt hoặc tắt "tạo khi gắn window"; danh sách bước tính lại.', 'Change the trigger or turn off "create on attach"; the step list is recomputed.')
m(M, 'ctl.trigger', 'Điều gì xảy ra trước', 'What happens first')
m(M, 'ctl.trigger.attach', 'view được gắn vào window', 'the view is attached to a window')
m(M, 'ctl.trigger.create', 'gọi createComposition()', 'createComposition() is called')
m(M, 'ctl.eager', 'Tạo composition khi gắn window', 'Create composition on attach')
m(M, 'diagramTitle', 'Sơ đồ runtime: composition ban đầu', 'Runtime diagram: initial composition')
m(M, 'diagramDesc', 'Host, Composition, mã đã biến đổi, Composer, Applier và các phase lần lượt được kích hoạt.', 'The host, Composition, transformed code, Composer, Applier and phases are activated in turn.')
m(M, 's.set.title', 'setContent lưu nội dung', 'setContent stores the content')
m(M, 's.set.explain', 'Gọi `setContent` đưa lambda composable cho host. Lúc này chưa có Composition nào chạy.', 'Calling `setContent` hands the composable lambda to the host. No Composition has run yet.')
m(M, 'ev.set', 'setContent { CounterScreen() }', 'setContent { CounterScreen() }')
m(M, 's.attachLazy.title', 'Gắn vào window nhưng chưa compose', 'Attached, but not composed yet')
m(M, 's.attachLazy.explain', 'Vì đã tắt "tạo khi gắn window", việc gắn không kích hoạt composition ban đầu.', 'Because "create on attach" is off, attaching does not trigger the initial composition.')
m(M, 'ev.attachLazy', 'gắn window, chưa tạo composition', 'attached, no composition yet')
m(M, 'sk.initial', 'Composition ban đầu lúc gắn', 'Initial composition on attach')
m(M, 'sk.lazy', 'shouldCreateCompositionOnAttachedToWindow = false', 'shouldCreateCompositionOnAttachedToWindow = false')
m(M, 's.trigger.attach.title', 'Gắn vào window: tạo Composition', 'Attached to a window: Composition created')
m(M, 's.trigger.attach.explain', 'View được gắn vào window nên host tạo Composition ban đầu.', 'The view is attached to a window, so the host creates the initial Composition.')
m(M, 's.trigger.create.title', 'createComposition(): tạo Composition sớm', 'createComposition(): Composition created early')
m(M, 's.trigger.create.explain', '`createComposition()` được gọi trước khi gắn, nên composition ban đầu xảy ra ngay lúc đó.', '`createComposition()` is called before attaching, so the initial composition happens right then.')
m(M, 's.trigger.measure.title', 'Lần measure đầu: tạo Composition', 'First measure: Composition created')
m(M, 's.trigger.measure.explain', 'Không tạo khi gắn, nhưng composition ban đầu vẫn xảy ra ở lần measure đầu tiên.', 'It was not created on attach, but the initial composition still happens at the first measure.')
m(M, 'ev.trigger.attach', 'onAttachedToWindow → composition ban đầu', 'onAttachedToWindow → initial composition')
m(M, 'ev.trigger.create', 'createComposition() → composition ban đầu', 'createComposition() → initial composition')
m(M, 'ev.trigger.measure', 'measure lần đầu → composition ban đầu', 'first measure → initial composition')
m(M, 's.run.title', 'Runtime gọi mã đã biến đổi', 'The runtime calls the transformed code')
m(M, 's.run.explain', 'Composition chạy lambda `CounterScreen()`; đây là mã mà compiler đã thêm tham số và group.', 'The Composition runs the `CounterScreen()` lambda; this is code the compiler has given extra parameters and groups.')
m(M, 'ev.run', 'chạy CounterScreen()', 'run CounterScreen()')
m(M, 'co.transformed', 'Compose Compiler là Kotlin compiler plugin, nên hàm `@Composable` lúc chạy không còn y như mã bạn viết. Xem B2.', 'The Compose Compiler is a Kotlin compiler plugin, so a `@Composable` function at run time is not exactly the code you wrote. See B2.')
m(M, 's.record.title', 'Composer xây dựng trạng thái composition', 'The Composer builds the composition state')
m(M, 's.record.explain', 'Lần đầu, Composer ghi group và giá trị (`remember`) vào SlotTable và ghi lại các node cần tạo.', 'The first time, the Composer writes groups and values (`remember`) to the SlotTable and records the nodes to create.')
m(M, 'ev.record', 'ghi group và slot', 'write groups and slots')
m(M, 'ch.groups', 'SlotTable có group cho CounterScreen, Column, Text, Button', 'The SlotTable has groups for CounterScreen, Column, Text, Button')
m(M, 's.apply.title', 'Applier dựng cây UI', 'The Applier builds the UI tree')
m(M, 's.apply.explain', 'Các thay đổi đã ghi nhận được áp dụng qua Applier: node được chèn vào cây UI.', 'The recorded changes are applied through the Applier: nodes are inserted into the UI tree.')
m(M, 'ev.apply', 'chèn các node', 'insert nodes')
m(M, 'ch.nodes', 'Cây UI có node cho Column, Text, Button', 'The UI tree has nodes for Column, Text, Button')
m(M, 's.phases.title', 'Đo, đặt và vẽ', 'Measure, place and draw')
m(M, 's.phases.explain', 'Compose UI chạy Layout rồi Drawing cho cây mới để có khung hình đầu tiên.', 'Compose UI runs Layout then Drawing for the new tree to produce the first frame.')
m(M, 'ev.phases', 'layout và draw', 'layout and draw')
m(M, 'st.content', 'Nội dung', 'Content')
m(M, 'st.comp', 'Composition', 'Composition')
m(M, 'val.stored', 'đã lưu', 'stored')
m(M, 'val.none', 'chưa có', 'none')
m(M, 'val.created', 'đã tạo', 'created')
m(M, 'co.eagerIgnored', '`createComposition()` được gọi trước khi gắn, nên việc tắt "tạo khi gắn window" không ảnh hưởng thời điểm composition ban đầu.', '`createComposition()` is called before attaching, so turning off "create on attach" does not change when the initial composition happens.')
m(M, 'co.host', '`ComposeView` là View của Android; phần host này gắn nhãn [[badge:android-impl]]. [[src:rt-composeview]]', '`ComposeView` is an Android View; this host part is labelled [[badge:android-impl]]. [[src:rt-composeview]]')

# ---------------- B2: compiler ----------------
M = 'compiler'
m(M, 'title', 'Restart group và điều kiện skip (mã giả)', 'Restart groups and the skip check (pseudo-code)')
m(M, 'overview', 'Hàm `Greeting(name)` sau khi compiler biến đổi, viết ở dạng mã giả. Bật/tắt "tham số đổi" và "hàm có đọc state" để thấy hai nhánh.',
  'The `Greeting(name)` function after the compiler transform, written as pseudo-code. Toggle "parameter changed" and "reads state" to see both branches.')
m(M, 'wrapup', 'Mã sinh ra bọc thân hàm trong group, hỏi Composer có thể skip không, và đăng ký cách chạy lại khi hàm có đọc state. Đây là hình dung khái niệm, không phải mã compiler bảo đảm.',
  'The generated code wraps the body in a group, asks the Composer whether it can skip, and registers how to run again when the function reads state. This is a conceptual picture, not guaranteed compiler output.')
m(M, 'simp.1', 'Mã giả bỏ qua bit của `$changed`, key thật của group và nhiều nhánh khác của compiler.', 'The pseudo-code leaves out the bits of `$changed`, real group keys and many other compiler branches.')
m(M, 'simp.2', 'Không gọi `currentComposer`, `changed()` hay API nội bộ trong ứng dụng: chúng phụ thuộc vị trí Composer đang duyệt.', 'Do not call `currentComposer`, `changed()` or internal APIs in an app: they depend on where the Composer currently is.')
m(M, 'ctl.hint', 'Hai công tắc chọn nhánh của mã giả.', 'Two switches pick the branch of the pseudo-code.')
m(M, 'ctl.changed', 'Tham số name đổi', 'Parameter name changed')
m(M, 'ctl.reads', 'Hàm có đọc state', 'The function reads state')
m(M, 'diagramTitle', 'Sơ đồ runtime: mã đã biến đổi và Composer', 'Runtime diagram: transformed code and the Composer')
m(M, 'diagramDesc', 'Mã đã biến đổi gọi Composer; Composer đọc giá trị cũ trong SlotTable.', 'The transformed code calls the Composer; the Composer reads the old value in the SlotTable.')
m(M, 's.start.title', 'Mở restart group', 'Open a restart group')
m(M, 's.start.explain', 'Compiler thêm tham số `$composer` và mở một group có thể khởi động lại quanh thân hàm.', 'The compiler adds a `$composer` parameter and opens a restartable group around the body.')
m(M, 'ev.start', 'startRestartGroup', 'startRestartGroup')
m(M, 'co.illustrative', 'Mã giả minh họa, không phải mã compiler bảo đảm sinh ra. [[badge:simplified]]', 'Illustrative pseudo-code, not guaranteed compiler output. [[badge:simplified]]')
m(M, 's.compare.title', 'So tham số với lần trước', 'Compare the parameter with last time')
m(M, 's.compare.changed', 'Giá trị `name` khác giá trị đã nhớ trong slot, nên thân hàm phải chạy.', 'The value of `name` differs from the one remembered in the slot, so the body must run.')
m(M, 's.compare.same', 'Giá trị `name` bằng giá trị đã nhớ và Composer cho phép skip.', 'The value of `name` equals the remembered one and the Composer allows skipping.')
m(M, 'ev.changed', 'name đổi', 'name changed')
m(M, 'ev.same', 'name không đổi', 'name unchanged')
m(M, 'st.old', 'name đã nhớ', 'remembered name')
m(M, 'st.new', 'name mới', 'new name')
m(M, 's.body.title', 'Chạy thân hàm', 'Run the body')
m(M, 's.body.explain', '`Text("Hi $name")` được gọi lại với giá trị mới.', '`Text("Hi $name")` is called again with the new value.')
m(M, 'ev.body', 'gọi Text', 'call Text')
m(M, 'ch.text', 'Text nhận chuỗi mới', 'Text receives the new string')
m(M, 's.skip.title', 'Nhảy tới cuối group', 'Skip to the end of the group')
m(M, 's.skip.explain', '`skipToGroupEnd()` bỏ qua thân hàm; nội dung cũ trong composition được giữ.', '`skipToGroupEnd()` skips the body; the old content in the composition is kept.')
m(M, 'ev.skip', 'skipToGroupEnd', 'skipToGroupEnd')
m(M, 'sk.body', 'Thân hàm Greeting', 'The body of Greeting')
m(M, 'sk.same', 'tham số không đổi', 'the parameter did not change')
m(M, 's.end.title', 'Đóng group: có cần cách chạy lại không?', 'Close the group: is a way to re-run needed?')
m(M, 's.end.scope', 'Thân hàm đã đọc state, nên `endRestartGroup()` trả về một scope; runtime giữ lambda để chạy lại riêng hàm này khi state đổi.', 'The body read state, so `endRestartGroup()` returns a scope; the runtime keeps a lambda to re-run just this function when the state changes.')
m(M, 's.end.null', 'Không có lần đọc state quan sát được, nên `endRestartGroup()` trả `null`: không cần cách chạy lại riêng.', 'There was no observable state read, so `endRestartGroup()` returns `null`: no separate way to re-run is needed.')
m(M, 'ev.scope', 'trả về update scope', 'returns an update scope')
m(M, 'ev.null', 'trả về null', 'returns null')
m(M, 'st.scope', 'endRestartGroup()', 'endRestartGroup()')
m(M, 'val.scope', 'update scope', 'update scope')
m(M, 'val.null', 'null', 'null')
m(M, 'co.impl', 'Restart group và update scope được mô tả trong tài liệu thiết kế của runtime (nhánh androidx-main, đọc 2026-11-21). [[badge:impl]] [[src:rt-how]]', 'Restart groups and update scopes are described in the runtime design document (androidx-main branch, read 2026-11-21). [[badge:impl]] [[src:rt-how]]')

# ---------------- B3: key ----------------
M = 'keys'
m(M, 'title', 'Danh sách có và không có key()', 'A list with and without key()')
m(M, 'overview', 'Danh sách A, B, C; mỗi item có một `remember` và một `LaunchedEffect(movie.id)`. Chọn thao tác, bật/tắt `key()` và xem từng vị trí.',
  'A list A, B, C; each item has a `remember` and a `LaunchedEffect(movie.id)`. Pick an operation, toggle `key()` and look at each position.')
m(M, 'wrapup', 'Không có key, instance được nhận diện theo vị trí: tùy thao tác, có item giữ nguyên, có item recompose với state của vị trí cũ. Có key, instance đi theo key. Kết quả khác nhau theo từng kịch bản.',
  'Without a key, instances are identified by position: depending on the operation, some items are kept and some recompose with the state of the old position. With a key, instances follow the key. The outcome differs per scenario.')
m(M, 'simp.1', 'Mô hình coi `remember {}` không key là giữ theo vị trí và bỏ qua animation di chuyển, lazy list và cách runtime thật tìm node.', 'The model treats a key-less `remember {}` as kept by position and leaves out move animations, lazy lists and how the real runtime finds nodes.')
m(M, 'ctl.hint', 'Thử cả bốn thao tác ở hai chế độ; đừng khái quát từ một kịch bản.', 'Try all four operations in both modes; do not generalise from one scenario.')
m(M, 'ctl.op', 'Thao tác', 'Operation')
m(M, 'ctl.op.insertTop', 'chèn N vào đầu', 'insert N at the top')
m(M, 'ctl.op.insertEnd', 'thêm N vào cuối', 'add N at the end')
m(M, 'ctl.op.removeMiddle', 'xóa B ở giữa', 'remove B in the middle')
m(M, 'ctl.op.swap', 'đổi chỗ A và B', 'swap A and B')
m(M, 'ctl.key', 'Dùng key(movie.id)', 'Use key(movie.id)')
m(M, 'diagramTitle', 'Danh sách và các vị trí trong composition', 'The list and its positions in the composition')
m(M, 'diagramDesc', 'Nguồn dữ liệu bên trái, bốn vị trí item bên phải; trạng thái mỗi vị trí hiện dưới nhãn.', 'The data source on the left, four item positions on the right; each position shows its state under the label.')
m(M, 'n.list', 'movies', 'movies')
for i in range(4): m(M, 'n.p%d' % i, 'Vị trí %d' % (i + 1), 'Position %d' % (i + 1))
for k, vi, en in [('kept', 'Giữ hoặc di chuyển', 'Kept or moved'), ('recomposed', 'Recompose', 'Recomposed'), ('created', 'Tạo mới', 'Created'), ('removed', 'Rời Composition', 'Left composition')]:
    m(M, 'met.' + k, vi, en)
m(M, 's.op.insertTop.title', 'Chèn N vào đầu danh sách', 'Insert N at the top of the list')
m(M, 's.op.insertEnd.title', 'Thêm N vào cuối danh sách', 'Add N at the end of the list')
m(M, 's.op.removeMiddle.title', 'Xóa B ở giữa danh sách', 'Remove B from the middle of the list')
m(M, 's.op.swap.title', 'Đổi chỗ A và B', 'Swap A and B')
m(M, 's.op.positional', 'Danh sách đổi từ {before} thành {after}. Không có key: mỗi instance được nhận diện theo call site và thứ tự thực thi, tức là theo vị trí.', 'The list changes from {before} to {after}. Without a key, each instance is identified by its call site and execution order, that is, by position.')
m(M, 's.op.keyed', 'Danh sách đổi từ {before} thành {after}. Có `key(movie.id)`: mỗi instance được nhận diện theo id của item.', 'The list changes from {before} to {after}. With `key(movie.id)`, each instance is identified by the item id.')
m(M, 'ev.op', '{before} → {after}', '{before} → {after}')
m(M, 'co.try', 'Đổi "Thao tác" hoặc bật "Dùng key" rồi đi lại từ đầu.', 'Change "Operation" or turn on "Use key", then walk through again.')
m(M, 'st.list', 'Danh sách', 'List')
m(M, 'st.remember', 'remember thuộc về', 'remember belongs to')
m(M, 'st.effect', 'LaunchedEffect', 'LaunchedEffect')
m(M, 'val.restarted', 'bị hủy và chạy lại', 'cancelled and restarted')
m(M, 'val.started', 'bắt đầu', 'started')
m(M, 'val.kept', 'giữ nguyên', 'kept running')
m(M, 's.kept.title', 'Vị trí {pos}: {item} giữ nguyên', 'Position {pos}: {item} is kept')
m(M, 's.kept.positional', 'Ở vị trí {pos}, đầu vào vẫn là {item} như trước, nên instance được tái dùng và có thể skip.', 'At position {pos} the input is still {item}, so the instance is reused and can be skipped.')
m(M, 's.kept.keyed', 'Instance của {item} vẫn ở vị trí {pos}; đầu vào không đổi nên có thể skip.', 'The instance for {item} is still at position {pos}; its input is unchanged so it can be skipped.')
m(M, 's.moved.title', 'Vị trí {pos}: {item} di chuyển tới', 'Position {pos}: {item} moves here')
m(M, 's.moved.keyed', 'Nhờ key, instance của {item} được di chuyển cùng state `remember` và effect của nó; không cần recompose chỉ vì đổi vị trí.', 'Thanks to the key, the instance for {item} moves along with its `remember` state and effect; it does not need to recompose just because it moved.')
m(M, 's.recomposed.title', 'Vị trí {pos}: recompose với {item}', 'Position {pos}: recomposes with {item}')
m(M, 's.recomposed.positional', 'Vị trí {pos} trước đây là {from}, giờ nhận {item}: đầu vào đổi nên recompose. `remember` không key vẫn là state của vị trí cũ ({from}); `LaunchedEffect(movie.id)` bị hủy và chạy lại.', 'Position {pos} used to hold {from} and now gets {item}: the input changed, so it recomposes. A key-less `remember` still holds the old position state ({from}); `LaunchedEffect(movie.id)` is cancelled and restarted.')
m(M, 'co.stateWrong', 'State `remember` của {from} giờ hiện cạnh dữ liệu {item}: đây là lý do dùng `key()` khi item có state hoặc effect.', 'The `remember` state of {from} now sits next to the data of {item}: this is why you use `key()` when items have state or effects.')
m(M, 's.created.title', 'Vị trí {pos}: tạo mới {item}', 'Position {pos}: {item} is created')
m(M, 's.created.positional', 'Vị trí {pos} chưa từng có, nên instance mới được tạo cho {item}.', 'Position {pos} did not exist before, so a new instance is created for {item}.')
m(M, 's.created.keyed', '{item} là id mới, nên một instance mới được tạo, dù nó nằm ở vị trí {pos}.', '{item} is a new id, so a new instance is created, even though it sits at position {pos}.')
m(M, 's.removed.title', '{item} rời Composition', '{item} leaves the Composition')
m(M, 's.removed.positional', 'Danh sách ngắn hơn, nên instance ở vị trí cuối (đang giữ state của {item}) rời Composition và effect của nó bị hủy.', 'The list is shorter, so the instance at the last position (holding the state of {item}) leaves the Composition and its effect is cancelled.')
m(M, 's.removed.keyed', 'Id {item} không còn trong danh sách, nên đúng instance của {item} rời Composition.', 'Id {item} is no longer in the list, so exactly the instance for {item} leaves the Composition.')
m(M, 'ch.leave', 'Instance {item} bị gỡ', 'The {item} instance is removed')
m(M, 'ev.kept', '{item} giữ, có thể skip', '{item} kept, can skip')
m(M, 'ev.moved', '{item} di chuyển tới vị trí {pos}', '{item} moved to position {pos}')
m(M, 'ev.recomposed', 'vị trí {pos}: {from} → {item}', 'position {pos}: {from} → {item}')
m(M, 'ev.created', 'tạo {item}', 'create {item}')
m(M, 'ev.removed', 'gỡ {item}', 'remove {item}')
m(M, 'sk.item', 'Recompose item', 'Recomposing the item')
m(M, 'sk.same', 'đầu vào ở vị trí này không đổi', 'the input at this position did not change')
m(M, 'co.source', 'Quy tắc lấy từ trang "Lifecycle of composables": thêm ở cuối thì tái dùng; chèn đầu, xóa, đổi chỗ thì các item đổi đầu vào bị recompose. [[src:cp-lifecycle]]', 'The rule comes from the "Lifecycle of composables" page: adding at the end reuses instances; inserting at the top, removing or reordering recomposes the items whose input changed. [[src:cp-lifecycle]]')

# ---------------- B4: snapshot ----------------
M = 'snapshot'
m(M, 'title', 'Ghi state, apply và invalidate', 'Writing state, applying and invalidating')
m(M, 'overview', 'Biến `count` là `mutableStateOf(0)`. Chọn ghi trong một mutable snapshot hay ghi thẳng, và có scope nào đọc `count` hay không.',
  '`count` is a `mutableStateOf(0)`. Choose whether to write inside a mutable snapshot or directly, and whether any scope reads `count`.')
m(M, 'wrapup', 'Đọc state ghi nhận ai phụ thuộc; ghi state tạo thay đổi; khi thay đổi được apply, chỉ những scope đã đọc state đó bị invalidate. Không ai đọc thì không có gì để recompose.',
  'Reading state records who depends on it; writing it creates a change; when the change is applied, only the scopes that read that state are invalidated. If nobody reads it, there is nothing to recompose.')
m(M, 'simp.1', 'Mô hình không vẽ StateRecord. Một state object có thể có nhiều record cho nhiều snapshot; đó là khái niệm, không phải cấu trúc bộ nhớ được mô tả ở đây.', 'The model does not draw StateRecords. A state object can have several records for several snapshots; that is a concept, not a memory layout described here.')
m(M, 'simp.2', 'Xung đột khi apply chỉ được nhắc tới, không mô phỏng.', 'Apply conflicts are only mentioned, not simulated.')
m(M, 'ctl.hint', 'Hai công tắc: nơi ghi và việc có ai đọc state.', 'Two switches: where the write happens and whether anyone reads the state.')
m(M, 'ctl.isolated', 'Ghi trong mutable snapshot', 'Write inside a mutable snapshot')
m(M, 'ctl.read', 'Text đọc count', 'Text reads count')
m(M, 'diagramTitle', 'Sơ đồ runtime: Snapshot và Recomposer', 'Runtime diagram: Snapshot and Recomposer')
m(M, 'diagramDesc', 'Snapshot báo cho Recomposer, Recomposer yêu cầu Composition chạy lại.', 'Snapshot notifies the Recomposer, which asks the Composition to run again.')
m(M, 's.read.title', 'Lần đọc được ghi nhận', 'The read is recorded')
m(M, 's.read.explain', 'Trong composition, `Text` đọc `count`. Composition dùng read observer của snapshot để ghi nhận scope này phụ thuộc `count`.', 'During composition, `Text` reads `count`. Composition uses the snapshot read observer to record that this scope depends on `count`.')
m(M, 's.read.none', 'Không composable nào đọc `count`, nên không có scope nào được ghi nhận là phụ thuộc.', 'No composable reads `count`, so no scope is recorded as depending on it.')
m(M, 'ev.read', 'đăng ký đọc count', 'register read of count')
m(M, 'st.readers', 'Phụ thuộc count', 'Depends on count')
m(M, 'val.scopeText', 'scope của Counter', 'the Counter scope')
m(M, 'val.noReader', 'không có', 'nobody')
m(M, 's.write.title', 'Ghi count = 1', 'Write count = 1')
m(M, 's.write.isolated', 'Ghi bên trong mutable snapshot: giá trị mới chỉ thấy bên trong snapshot đó; global vẫn thấy 0.', 'The write happens inside a mutable snapshot: the new value is visible only inside it; global still sees 0.')
m(M, 's.write.global', 'Ghi thẳng: đi vào global snapshot. Thay đổi được gom lại và apply sau.', 'A direct write goes to the global snapshot. Changes are collected and applied afterwards.')
m(M, 'ev.write', 'count = 1', 'count = 1')
m(M, 'st.global', 'Global thấy', 'Global sees')
m(M, 'st.inside', 'Trong snapshot', 'Inside the snapshot')
m(M, 's.apply.title', 'apply(): thay đổi được áp dụng nguyên tử', 'apply(): changes are applied atomically')
m(M, 's.apply.explain', '`apply()` đưa mọi thay đổi của snapshot vào global cùng lúc, rồi apply observer được gọi.', '`apply()` moves all of the snapshot\'s changes into global at once, then apply observers are called.')
m(M, 'ev.apply', 'apply', 'apply')
m(M, 'co.conflict', 'Apply có thể xung đột nếu state bị đổi ở nơi khác; `withMutableSnapshot` khi đó ném `SnapshotApplyConflictException`. [[src:rt-snapshot]]', 'Applying can conflict if the state was changed elsewhere; `withMutableSnapshot` then throws `SnapshotApplyConflictException`. [[src:rt-snapshot]]')
m(M, 's.invalidate.title', 'Scope đã đọc count bị invalidate', 'The scope that read count is invalidated')
m(M, 's.invalidate.explain', 'Thay đổi được apply và được quan sát; runtime đánh dấu scope của `Counter` cần chạy lại và báo cho Recomposer.', 'The change is applied and observed; the runtime marks the `Counter` scope as needing to run again and tells the Recomposer.')
m(M, 'ev.invalidate', 'invalidate scope Counter', 'invalidate the Counter scope')
m(M, 's.recompose.title', 'Recomposer lên lịch recompose', 'The Recomposer schedules a recompose')
m(M, 's.recompose.explain', 'Chỉ scope bị invalidate chạy lại, không phải toàn bộ cây. Chi tiết ở B5 và B10.', 'Only the invalidated scope runs again, not the whole tree. Details in B5 and B10.')
m(M, 'ev.recompose', 'recompose Counter', 'recompose Counter')
m(M, 's.nothing.title', 'Không có gì để recompose', 'Nothing to recompose')
m(M, 's.nothing.explain', 'Giá trị đổi nhưng không scope nào đọc nó, nên không có invalidation và không có recomposition.', 'The value changed but no scope read it, so there is no invalidation and no recomposition.')
m(M, 'ev.nothing', 'không có scope phụ thuộc', 'no dependent scope')
m(M, 'sk.recompose', 'Recomposition', 'Recomposition')
m(M, 'sk.noReader', 'không scope nào đọc count', 'no scope read count')

# ---------------- B5: recomposer ----------------
M = 'recomposer'
m(M, 'title', 'Recomposer gom việc và chờ frame', 'The Recomposer batches work and waits for a frame')
m(M, 'overview', 'Một hoặc nhiều lần ghi state làm invalidate scope. Chọn số lần ghi và thử tạm dừng frame clock.', 'One or more state writes invalidate a scope. Pick the number of writes and try pausing the frame clock.')
m(M, 'wrapup', 'Recomposer chờ composer bị invalidate, recompose rồi apply; công việc cần thời điểm frame dùng `withFrameNanos`. Không có quy tắc "mỗi frame đúng một lần recomposition".',
  'The Recomposer waits for invalidated composers, recomposes, then applies; work that needs the frame time uses `withFrameNanos`. There is no rule of "exactly one recomposition per frame".')
m(M, 'simp.1', 'Mô hình gom các lần ghi trước khi xử lý vào một lượt; thời điểm thật phụ thuộc host, frame clock và effect.', 'The model groups writes made before processing into one pass; real timing depends on the host, the frame clock and effects.')
m(M, 'simp.2', 'Không có thời lượng frame cố định ở đây; thời gian trong nhật ký chỉ để sắp thứ tự.', 'There is no fixed frame duration here; times in the log only order the events.')
m(M, 'ctl.hint', 'Đổi số lần ghi hoặc tạm dừng frame clock.', 'Change the number of writes or pause the frame clock.')
m(M, 'ctl.writes', 'Số lần ghi trước khi xử lý', 'Writes before processing')
m(M, 'ctl.writes.n', '{n} lần ghi', '{n} writes')
m(M, 'ctl.paused', 'Frame clock tạm dừng (UI không ở foreground)', 'Frame clock paused (UI not in the foreground)')
m(M, 'diagramTitle', 'Sơ đồ runtime: Recomposer', 'Runtime diagram: Recomposer')
m(M, 'diagramDesc', 'Snapshot báo invalidation cho Recomposer; Recomposer điều phối Composition và Applier.', 'Snapshot reports invalidations to the Recomposer; the Recomposer coordinates the Composition and the Applier.')
m(M, 'met.writes', 'Lần ghi', 'Writes')
m(M, 'ch.applied', 'Cây UI nhận thay đổi của lượt recompose', 'The UI tree receives the changes of the recompose pass')
m(M, 'met.passes', 'Lượt recompose', 'Recompose passes')
m(M, 's.write.title', 'Lần ghi {n}', 'Write {n}')
m(M, 's.write.explain', 'Ghi state lần {n}; scope đã đọc state đó bị invalidate.', 'State write number {n}; the scope that read that state is invalidated.')
m(M, 'ev.write', 'invalidate (lần ghi {n})', 'invalidate (write {n})')
m(M, 's.pending.title', 'Recomposer có việc chờ', 'The Recomposer has pending work')
m(M, 's.pending.explain', 'Recomposer ghi nhận có composer bị invalidate. {n} lần ghi được gom thành việc chờ cho cùng một lượt trong mô hình này.', 'The Recomposer notes that a composer was invalidated. In this model, {n} writes are grouped as pending work for one pass.')
m(M, 'ev.pending', '{n} invalidation chờ xử lý', '{n} invalidations pending')
m(M, 'st.pending', 'Việc chờ', 'Pending')
m(M, 's.paused.title', 'Frame clock đang tạm dừng', 'The frame clock is paused')
m(M, 's.paused.explain', 'Khi UI không ở foreground, host có thể tạm dừng frame clock mà `withFrameNanos` dùng; việc chờ frame phải đợi.', 'When the UI is not in the foreground, the host can pause the frame clock used by `withFrameNanos`; work waiting for a frame has to wait.')
m(M, 'ev.paused', 'chờ frame clock', 'waiting for the frame clock')
m(M, 'sk.frame', 'Frame kế tiếp', 'The next frame')
m(M, 'sk.paused', 'frame clock đang tạm dừng', 'the frame clock is paused')
m(M, 'co.pause', '`Recomposer` có `pauseCompositionFrameClock()` và `resumeCompositionFrameClock()`. [[src:rt-recomposer]]', '`Recomposer` has `pauseCompositionFrameClock()` and `resumeCompositionFrameClock()`. [[src:rt-recomposer]]')
m(M, 's.resume.title', 'Frame clock chạy lại', 'The frame clock resumes')
m(M, 's.resume.explain', 'UI trở lại foreground; frame clock tiếp tục.', 'The UI is back in the foreground; the frame clock continues.')
m(M, 'ev.resume', 'resumeCompositionFrameClock', 'resumeCompositionFrameClock')
m(M, 's.frame.title', 'Frame mới', 'A new frame')
m(M, 's.frame.explain', '`withFrameNanos` suspend tới khi có frame mới rồi gọi khối với thời điểm frame (nano giây).', '`withFrameNanos` suspends until a new frame, then calls the block with the frame time in nanoseconds.')
m(M, 'ev.frame', 'frame', 'frame')
m(M, 'co.frame', '`MonotonicFrameClock` là phần tử của `CoroutineContext`; thời điểm frame tăng nghiêm ngặt giữa các lần gọi. [[src:rt-frameclock]]', '`MonotonicFrameClock` is a `CoroutineContext` element; frame times strictly increase between calls. [[src:rt-frameclock]]')
m(M, 's.recompose.title', 'Recompose phần bị invalidate', 'Recompose what was invalidated')
m(M, 's.recompose.explain', 'Recomposer yêu cầu Composition chạy lại các scope bị invalidate; {n} lần ghi được xử lý trong một lượt.', 'The Recomposer asks the Composition to re-run the invalidated scopes; {n} writes are handled in one pass.')
m(M, 'ev.recompose', 'recompose ({n} invalidation)', 'recompose ({n} invalidations)')
m(M, 's.apply.title', 'Apply thay đổi', 'Apply the changes')
m(M, 's.apply.explain', 'Thay đổi đã tính được áp dụng qua Applier. `runRecomposeAndApplyChanges()` là suspend function lặp lại chu trình này.', 'The computed changes are applied through the Applier. `runRecomposeAndApplyChanges()` is a suspend function that repeats this cycle.')
m(M, 'ev.apply', 'apply', 'apply')

# ---------------- B6: applier ----------------
M = 'applier'
m(M, 'title', 'Tính thay đổi rồi áp dụng thay đổi', 'Compute changes, then apply them')
m(M, 'overview', 'Chọn loại thay đổi trên cây UI và xem Composer ghi nhận gì, Applier được gọi thế nào.', 'Pick a kind of UI tree change and see what the Composer records and how the Applier is called.')
m(M, 'wrapup', 'Composer tính thay đổi; Applier áp dụng chúng giữa `onBeginChanges()` và `onEndChanges()`. Hai bước liên quan nhưng không phải một.', 'The Composer computes changes; the Applier applies them between `onBeginChanges()` and `onEndChanges()`. The two steps are related but not the same.')
m(M, 'simp.1', 'Mô hình đếm lời gọi ở mức khái niệm; số lời gọi thật phụ thuộc phiên bản runtime và cách gộp.', 'The model counts calls at a conceptual level; the real number of calls depends on the runtime version and batching.')
m(M, 'ctl.hint', 'Chọn loại thay đổi.', 'Pick a kind of change.')
m(M, 'ctl.change', 'Thay đổi', 'Change')
m(M, 'ctl.change.text', 'chỉ đổi chữ của Text', 'only the Text string changes')
m(M, 'ctl.change.insert', 'chèn một node', 'insert one node')
m(M, 'ctl.change.insert2', 'chèn hai node liền kề', 'insert two adjacent nodes')
m(M, 'ctl.change.remove', 'xóa một node', 'remove one node')
m(M, 'ctl.change.move', 'di chuyển một node', 'move one node')
m(M, 'diagramTitle', 'Sơ đồ runtime: Composer và Applier', 'Runtime diagram: Composer and Applier')
m(M, 'diagramDesc', 'Composer tính thay đổi trong SlotTable; Applier áp dụng lên cây UI.', 'The Composer computes changes in the SlotTable; the Applier applies them to the UI tree.')
m(M, 'met.calls', 'Lời gọi thao tác cây', 'Tree operation calls')
m(M, 'st.nodes', 'Node con của Column', 'Children of Column')
m(M, 's.compute.title', 'Composer tính thay đổi', 'The Composer computes changes')
for k, vi, en in [('text', 'Cấu trúc không đổi; chỉ một giá trị của node Text đổi.', 'The structure is unchanged; only a value on the Text node changes.'),
                  ('insert', 'Một group mới xuất hiện, kèm một node cần chèn.', 'A new group appears, with one node to insert.'),
                  ('insert2', 'Hai group mới liền kề, kèm hai node cần chèn.', 'Two new adjacent groups appear, with two nodes to insert.'),
                  ('remove', 'Một group biến mất; node của nó cần gỡ.', 'A group disappears; its node must be removed.'),
                  ('move', 'Một group đổi chỗ; node của nó cần di chuyển.', 'A group moves; its node must be moved.')]:
    m(M, 's.compute.' + k, vi, en)
m(M, 'ev.compute', 'ghi nhận thay đổi', 'record changes')
for k, vi, en in [('update', 'cập nhật giá trị node', 'update a node value'), ('insert', 'chèn node', 'insert a node'), ('remove', 'gỡ node', 'remove a node'), ('move', 'di chuyển node', 'move a node')]:
    m(M, 'ch.' + k, vi, en)
m(M, 's.begin.title', 'onBeginChanges()', 'onBeginChanges()')
m(M, 's.begin.explain', 'Applier được báo trước khi một đợt thay đổi bắt đầu.', 'The Applier is told before a batch of changes begins.')
m(M, 'ev.begin', 'onBeginChanges', 'onBeginChanges')
m(M, 's.ops.title', 'Thao tác trên cây', 'Tree operations')
for k, vi, en in [('text', 'Không có chèn, xóa hay di chuyển: giá trị mới được đặt lên node đang có ({calls} lời gọi cập nhật).', 'No insert, remove or move: the new value is set on the existing node ({calls} update call).'),
                  ('insert', 'Applier chèn node (`insertTopDown` hoặc `insertBottomUp`, một trong hai): {calls} lời gọi.', 'The Applier inserts the node (`insertTopDown` or `insertBottomUp`, one of the two): {calls} call.'),
                  ('insert2', 'Hai node liền kề được chèn; thao tác liền kề có thể được gộp thành {calls} lời gọi.', 'Two adjacent nodes are inserted; adjacent operations can be merged into {calls} call.'),
                  ('remove', '`remove(index, count)` gỡ node: {calls} lời gọi.', '`remove(index, count)` removes the node: {calls} call.'),
                  ('move', '`move(from, to, count)` di chuyển node: {calls} lời gọi.', '`move(from, to, count)` moves the node: {calls} call.')]:
    m(M, 's.ops.' + k, vi, en)
    m(M, 'ev.ops.' + k, {'text': 'apply/update', 'insert': 'insert', 'insert2': 'insert (gộp)', 'remove': 'remove', 'move': 'move'}[k] + ' ×{calls}',
      {'text': 'apply/update', 'insert': 'insert', 'insert2': 'insert (merged)', 'remove': 'remove', 'move': 'move'}[k] + ' ×{calls}')
m(M, 'co.coalesce', 'Tài liệu thiết kế runtime mô tả việc gộp thao tác node liền kề thành một lời gọi Applier (androidx-main, đọc 2026-11-21). [[badge:impl]] [[src:rt-how]]', 'The runtime design document describes merging adjacent node operations into one Applier call (androidx-main, read 2026-11-21). [[badge:impl]] [[src:rt-how]]')
m(M, 'co.noStructure', 'Cấu trúc không đổi nên không có chèn hay xóa node; đổi chữ không đồng nghĩa với dựng lại cây.', 'The structure is unchanged, so no node is inserted or removed; changing text does not mean rebuilding the tree.')
m(M, 's.end.title', 'onEndChanges()', 'onEndChanges()')
m(M, 's.end.explain', 'Đợt thay đổi kết thúc; `onBeginChanges` luôn đi trước `onEndChanges`.', 'The batch ends; `onBeginChanges` comes before `onEndChanges`.')
m(M, 'ev.end', 'onEndChanges', 'onEndChanges')
m(M, 'co.android', '`Applier<N>` là generic: nó không gắn với Android. Trên Android, Compose UI dùng applier cho cây `LayoutNode` [[badge:android-impl]]. [[src:rt-applier]]', '`Applier<N>` is generic: it is not tied to Android. On Android, Compose UI uses an applier for the `LayoutNode` tree [[badge:android-impl]]. [[src:rt-applier]]')

# ---------------- B7: phases ----------------
M = 'phases'
m(M, 'title', 'Đọc state ở đâu thì phase đó chạy lại', 'Where state is read decides which phase runs again')
m(M, 'overview', 'Cùng một state `value`, đọc ở ba chỗ khác nhau. Trước hết xác định state được đọc ở đâu, rồi mới xem phase nào chạy lại.',
  'The same `value` state, read in three different places. First find where the state is read, then see which phase runs again.')
m(M, 'wrapup', 'Đọc trong composition: recompose, rồi layout và draw nếu kết quả đổi. Đọc trong khối placement của `Modifier.offset {}`: layout, và draw nếu vị trí đổi. Đọc trong `drawBehind {}`: chỉ draw.',
  'Read in composition: recompose, then layout and drawing if the result changed. Read in the placement block of `Modifier.offset {}`: layout, and drawing if the position changed. Read in `drawBehind {}`: drawing only.')
m(M, 'simp.1', 'Mô hình giả định kết quả mỗi phase đều đổi khi phase đó chạy, nên phase sau cũng chạy; thực tế phase sau có thể được bỏ qua nếu kích thước, vị trí không đổi.', 'The model assumes each phase that runs changes its result, so the next phase runs too; in reality a later phase can be skipped if size and position did not change.')
m(M, 'ctl.hint', 'Đổi nơi đọc state; bật vòng lặp phase để thấy frame thừa.', 'Change where the state is read; turn on the phase loop to see the extra frame.')
m(M, 'ctl.where', 'State được đọc ở', 'State is read in')
m(M, 'ctl.where.composition', 'composition: Text("Value: $value")', 'composition: Text("Value: $value")')
m(M, 'ctl.where.layout', 'layout: Modifier.offset { }', 'layout: Modifier.offset { }')
m(M, 'ctl.where.draw', 'draw: Modifier.drawBehind { }', 'drawing: Modifier.drawBehind { }')
m(M, 'ctl.backwards', 'Ghi state từ onSizeChanged (vòng lặp phase)', 'Write state from onSizeChanged (phase loop)')
m(M, 'diagramTitle', 'Ba phase và nơi state được đọc', 'Three phases and where the state is read')
m(M, 'diagramDesc', 'State bên trái; Composition, Layout, Drawing bên phải, mỗi phase có đèn chạy lại hoặc bỏ qua.', 'The state on the left; Composition, Layout and Drawing on the right, each with a runs-again or skipped light.')
for k, vi, en in [('state', 'value (state)', 'value (state)'), ('comp', 'Composition', 'Composition'), ('layout', 'Layout', 'Layout'), ('draw', 'Drawing', 'Drawing')]:
    m(M, 'n.' + k, vi, en)
for k, vi, en in [('comp', 'Composition', 'Composition'), ('layout', 'Layout', 'Layout'), ('draw', 'Drawing', 'Drawing'), ('frames', 'Số frame', 'Frames')]:
    m(M, 'met.' + k, vi, en)
m(M, 'val.run', 'chạy lại', 'runs again')
m(M, 'val.skip', 'bỏ qua', 'skipped')
m(M, 's.where.title', 'State được đọc ở đâu?', 'Where is the state read?')
m(M, 's.where.composition', '`value` được đọc trong thân composable (`Text("Value: $value")`), tức là trong phase Composition.', '`value` is read in the composable body (`Text("Value: $value")`), that is, in the Composition phase.')
m(M, 's.where.layout', '`value` được đọc trong lambda của `Modifier.offset { }`; lambda này chạy ở bước đặt vị trí của phase Layout.', '`value` is read in the `Modifier.offset { }` lambda; this lambda runs in the placement step of the Layout phase.')
m(M, 's.where.draw', '`value` được đọc trong `Modifier.drawBehind { }`, tức là trong phase Drawing.', '`value` is read in `Modifier.drawBehind { }`, that is, in the Drawing phase.')
for k in ['composition', 'layout', 'draw']:
    m(M, 'ev.read.' + k, {'composition': 'đọc trong composition', 'layout': 'đọc trong layout (placement)', 'draw': 'đọc trong draw'}[k],
      {'composition': 'read in composition', 'layout': 'read in layout (placement)', 'draw': 'read in drawing'}[k])
m(M, 'co.try', 'Chọn lần lượt ba nơi đọc ở "State được đọc ở" và so đèn của ba phase.', 'Pick each of the three places in "State is read in" and compare the lights of the three phases.')
m(M, 's.write.title', 'value đổi từ 0 thành 1', 'value changes from 0 to 1')
m(M, 's.write.explain', 'State được ghi. Phase nào chạy lại tùy vào nơi nó đã được đọc ở bước trước.', 'The state is written. Which phase runs again depends on where it was read in the previous step.')
m(M, 'ev.write', 'value = 1', 'value = 1')
m(M, 'st.value', 'value', 'value')
m(M, 's.comp.title', 'Phase Composition', 'The Composition phase')
m(M, 's.layout.title', 'Phase Layout', 'The Layout phase')
m(M, 's.draw.title', 'Phase Drawing', 'The Drawing phase')
m(M, 's.comp.run.composition', 'State được đọc trong composition, nên scope đó recompose.', 'The state was read during composition, so that scope recomposes.')
m(M, 's.comp.skip.layout', 'Không composable nào đọc `value`, nên không có recomposition.', 'No composable reads `value`, so there is no recomposition.')
m(M, 's.comp.skip.draw', 'Không composable nào đọc `value`, nên không có recomposition.', 'No composable reads `value`, so there is no recomposition.')
m(M, 's.layout.run.composition', 'Chữ của Text đổi nên kích thước có thể đổi; Layout chạy (mô hình giả định có đổi).', 'The Text string changed so its size may change; Layout runs (the model assumes it did).')
m(M, 's.layout.run.layout', 'State được đọc ở bước đặt vị trí, nên Layout chạy lại; bước đo không bị gọi lại vì đo và đặt có restart scope riêng.', 'The state was read in the placement step, so Layout runs again; measuring is not re-invoked because measure and placement have separate restart scopes.')
m(M, 's.layout.skip.draw', 'Layout không đọc `value`, nên được bỏ qua.', 'Layout does not read `value`, so it is skipped.')
m(M, 's.draw.run.composition', 'Nội dung đã đổi nên Drawing chạy.', 'The content changed, so Drawing runs.')
m(M, 's.draw.run.layout', 'Vị trí đổi nên Drawing chạy.', 'The position changed, so Drawing runs.')
m(M, 's.draw.run.draw', 'State được đọc trong draw: chỉ phase Drawing chạy lại.', 'The state was read in drawing: only the Drawing phase runs again.')
m(M, 'ev.run', 'chạy lại', 'runs again')
m(M, 'ev.skip', 'bỏ qua', 'skipped')
m(M, 'sk.comp', 'Composition', 'Composition')
m(M, 'sk.layout', 'Layout', 'Layout')
m(M, 'sk.draw', 'Drawing', 'Drawing')
m(M, 'sk.notRead', 'phase này không đọc state đã đổi', 'this phase does not read the changed state')
m(M, 's.loop.title', 'Vòng lặp phase: thêm một frame', 'Phase loop: one extra frame')
m(M, 's.loop.explain', 'Kích thước đo được ghi vào state trong `onSizeChanged`, rồi state đó được dùng trong `padding`. Frame đầu vẽ với giá trị cũ; layout ghi state nên cần frame thứ hai.', 'The measured size is written to state in `onSizeChanged`, then used in `padding`. The first frame draws with the old value; layout writes the state, so a second frame is needed.')
m(M, 'co.loop', 'Trang Compose phases gọi đây là phụ thuộc phase vòng tròn: tốn thêm frame và có thể làm UI nhảy. Dùng layout primitive hoặc custom layout thay vì cách này. [[src:cp-phases]] [[badge:guideline]]', 'The Compose phases page calls this a cyclic phase dependency: it costs an extra frame and can make the UI jump. Use layout primitives or a custom layout instead. [[src:cp-phases]] [[badge:guideline]]')
m(M, 'ev.loop', 'onSizeChanged ghi state', 'onSizeChanged writes state')
m(M, 'ev.extraFrame', 'cần frame thứ hai', 'second frame needed')

# ---------------- B8: skip ----------------
M = 'skip'
m(M, 'title', 'Khi nào composable con được skip?', 'When is a child composable skipped?')
m(M, 'overview', '`Parent` recompose vì `tick` đổi; `Child(data)` nhận một tham số. Chọn loại tham số và bật/tắt strong skipping.', '`Parent` recomposes because `tick` changed; `Child(data)` takes one parameter. Pick the parameter kind and toggle strong skipping.')
m(M, 'wrapup', 'Tham số stable được so bằng `equals`; tham số unstable được so bằng `===` khi strong skipping bật (mặc định từ Kotlin 2.0.20); khi tắt, composable có tham số unstable recompose mỗi lần cha recompose.',
  'Stable parameters are compared with `equals`; unstable parameters are compared with `===` when strong skipping is on (the default since Kotlin 2.0.20); when it is off, a composable with unstable parameters recomposes every time its parent does.')
m(M, 'simp.1', 'Mô hình chỉ có một tham số và giả định composable restartable; bỏ qua `@NonSkippableComposable`, kiểu trả về khác Unit và memoize lambda.', 'The model has one parameter and assumes a restartable composable; it leaves out `@NonSkippableComposable`, non-Unit return types and lambda memoization.')
m(M, 'simp.2', 'Skip là tối ưu: tính đúng đắn không được dựa vào việc một composable có chạy hay không.', 'Skipping is an optimisation: correctness must not depend on whether a composable runs or not.')
m(M, 'ctl.hint', 'Bốn loại tham số × strong skipping bật/tắt.', 'Four parameter kinds × strong skipping on/off.')
m(M, 'ctl.param', 'Tham số data', 'The data parameter')
m(M, 'ctl.param.stableSame', 'Tag stable, cùng instance', 'stable Tag, same instance')
m(M, 'ctl.param.stableEqual', 'Tag stable, instance mới nhưng equals', 'stable Tag, new instance but equal')
m(M, 'ctl.param.unstableSame', 'Tags unstable, cùng instance', 'unstable Tags, same instance')
m(M, 'ctl.param.unstableEqual', 'Tags unstable, instance mới cùng nội dung', 'unstable Tags, new instance with the same content')
m(M, 'ctl.strong', 'Strong skipping', 'Strong skipping')
m(M, 'diagramTitle', 'Cha và con trong recomposition', 'Parent and child during recomposition')
m(M, 'diagramDesc', 'Parent truyền tham số cho Child; Child được skip hoặc recompose.', 'Parent passes a parameter to Child; Child is skipped or recomposed.')
m(M, 'n.parent', 'Parent', 'Parent')
m(M, 'n.child', 'Child(data)', 'Child(data)')
m(M, 'met.child', 'Child', 'Child')
m(M, 'val.skipped', 'skip', 'skipped')
m(M, 'val.recomposed', 'recompose', 'recomposed')
m(M, 's.parent.title', 'Parent recompose', 'Parent recomposes')
m(M, 's.parent.explain', '`tick` đổi nên scope của `Parent` chạy lại và gọi `Child(data)`.', '`tick` changed, so the `Parent` scope runs again and calls `Child(data)`.')
m(M, 'ev.parent', 'recompose Parent', 'recompose Parent')
m(M, 's.param.title', 'Tham số có stable không?', 'Is the parameter stable?')
m(M, 's.param.stableSame', '`Tag` là data class chỉ có `val` kiểu stable nên được suy ra là stable; lần này truyền đúng instance cũ.', '`Tag` is a data class with only `val`s of stable types, so it is inferred stable; this time the same instance is passed.')
m(M, 's.param.stableEqual', '`Tag` stable; lần này là instance mới nhưng `equals` với giá trị cũ.', '`Tag` is stable; this time it is a new instance but `equals` the old value.')
m(M, 's.param.unstableSame', '`Tags` có `var` nên unstable: Compose không biết khi nào nó đổi. Lần này truyền đúng instance cũ.', '`Tags` has a `var`, so it is unstable: Compose cannot know when it changes. This time the same instance is passed.')
m(M, 's.param.unstableEqual', '`Tags` unstable; lần này là instance mới với cùng nội dung.', '`Tags` is unstable; this time it is a new instance with the same content.')
m(M, 'ev.param', 'kiểm tra stability', 'check stability')
m(M, 'st.stability', 'Stability', 'Stability')
m(M, 'st.strong', 'Strong skipping', 'Strong skipping')
m(M, 'val.stable', 'stable', 'stable')
m(M, 'val.unstable', 'unstable', 'unstable')
m(M, 'val.on', 'bật', 'on')
m(M, 'val.off', 'tắt', 'off')
m(M, 's.compare.title', 'So tham số', 'Compare the parameter')
m(M, 's.compare.equals', 'Tham số stable được so bằng `equals`.', 'A stable parameter is compared with `equals`.')
m(M, 's.compare.identity', 'Strong skipping bật: tham số unstable được so bằng `===` (cùng instance hay không).', 'Strong skipping is on: an unstable parameter is compared with `===` (same instance or not).')
m(M, 's.compare.never', 'Strong skipping tắt: composable có tham số unstable không skip được, nên không cần so.', 'Strong skipping is off: a composable with an unstable parameter cannot be skipped, so there is nothing to compare.')
m(M, 'ev.compare.equals', 'so bằng equals', 'compare with equals')
m(M, 'ev.compare.identity', 'so bằng ===', 'compare with ===')
m(M, 'ev.compare.never', 'không so (không skip được)', 'no comparison (not skippable)')
m(M, 'co.version', 'Strong skipping bật mặc định từ Kotlin 2.0.20; site đối chiếu với Kotlin 2.4.21. [[badge:version]] [[src:cp-strong]]', 'Strong skipping is on by default since Kotlin 2.0.20; the site was checked against Kotlin 2.4.21. [[badge:version]] [[src:cp-strong]]')
m(M, 's.skipped.title', 'Child được skip', 'Child is skipped')
m(M, 's.skipped.explain', 'Phép so cho kết quả "không đổi", nên Child không chạy lại; nội dung cũ được giữ.', 'The comparison says "unchanged", so Child does not run again; its old content is kept.')
m(M, 'ev.skipped', 'skip Child', 'skip Child')
m(M, 's.recomposed.title', 'Child recompose', 'Child recomposes')
m(M, 's.recomposed.explain', 'Phép so cho kết quả "có thể đã đổi" (hoặc không skip được), nên Child chạy lại.', 'The comparison says "may have changed" (or skipping is not possible), so Child runs again.')
m(M, 'ev.recomposed', 'recompose Child', 'recompose Child')
m(M, 'sk.child', 'Child(data)', 'Child(data)')
m(M, 'sk.equals', 'stable và equals với giá trị cũ', 'stable and equal to the old value')
m(M, 'sk.identity', 'unstable nhưng cùng instance (===)', 'unstable but the same instance (===)')
m(M, 'co.correct', 'Recompose thừa không sai về kết quả, chỉ tốn công. Không nên gắn `@Stable`/`@Immutable` đại trà để ép skip: chỉ đúng khi kiểu thật sự giữ hợp đồng stability và `equals` rẻ. [[src:cp-stability]] [[badge:guideline]]', 'An extra recompose does not give a wrong result, it only costs work. Do not add `@Stable`/`@Immutable` everywhere to force skipping: it is correct only when the type really keeps the stability contract and `equals` is cheap. [[src:cp-stability]] [[badge:guideline]]')

# ---------------- B9: semantics ----------------
M = 'semantics'
m(M, 'title', 'Semantics tree: ai đọc cây nào', 'The semantics tree: who reads which tree')
m(M, 'overview', 'Một `Button` có Icon và Text. Bật/tắt việc gộp con cháu và chọn ai đọc cây: dịch vụ trợ năng hay framework kiểm thử.', 'A `Button` with an Icon and a Text. Toggle merging of descendants and choose who reads the tree: an accessibility service or the testing framework.')
m(M, 'wrapup', 'Semantics tree là cây song song với UI. Dịch vụ trợ năng nhận cây unmerged và tự gộp; framework kiểm thử mặc định dùng cây merged (có `useUnmergedTree` để đổi).',
  'The semantics tree runs parallel to the UI. Accessibility services receive the unmerged tree and merge it themselves; the testing framework uses the merged tree by default (`useUnmergedTree` switches it).')
m(M, 'simp.1', 'Số node là minh họa cho ví dụ ba phần tử; mô hình không vẽ thuộc tính semantics cụ thể.', 'Node counts are illustrative for the three-element example; the model does not draw specific semantic properties.')
m(M, 'ctl.hint', 'Bật/tắt gộp và đổi người đọc cây.', 'Toggle merging and change who reads the tree.')
m(M, 'ctl.merge', 'Gộp con cháu (như Button)', 'Merge descendants (like Button)')
m(M, 'ctl.consumer', 'Ai đọc cây', 'Who reads the tree')
m(M, 'ctl.consumer.a11y', 'dịch vụ trợ năng', 'an accessibility service')
m(M, 'ctl.consumer.test', 'framework kiểm thử', 'the testing framework')
m(M, 'diagramTitle', 'Cây UI, semantics tree và người dùng cây', 'The UI tree, the semantics tree and its consumers')
m(M, 'diagramDesc', 'Cây UI sinh semantics tree; dịch vụ trợ năng và framework kiểm thử đọc cây đó.', 'The UI tree produces the semantics tree; accessibility services and the testing framework read it.')
for k, vi, en in [('ui', 'Cây UI', 'UI tree'), ('sem', 'Semantics tree', 'Semantics tree'), ('a11y', 'Dịch vụ trợ năng', 'Accessibility service'), ('test', 'Framework kiểm thử', 'Testing framework')]:
    m(M, 'n.' + k, vi, en)
m(M, 'met.nodes', 'Node người đọc thấy', 'Nodes the consumer sees')
m(M, 'st.merged', 'Node trong cây merged', 'Nodes in the merged tree')
m(M, 's.compose.title', 'Button có Icon và Text', 'A Button with an Icon and a Text')
m(M, 's.compose.explain', 'Composition dựng ba phần tử trong cây UI: nút, icon, chữ.', 'Composition builds three elements in the UI tree: the button, the icon, the text.')
m(M, 'ev.compose', 'dựng Button, Icon, Text', 'build Button, Icon, Text')
m(M, 's.tree.title', 'Semantics tree song song', 'A parallel semantics tree')
m(M, 's.tree.explain', 'Thuộc tính semantics từ component và modifier tạo ra một cây mô tả ý nghĩa, không mô tả cách vẽ.', 'Semantic properties from components and modifiers form a tree that describes meaning, not how to draw.')
m(M, 'ev.tree', 'dựng semantics tree', 'build the semantics tree')
m(M, 'co.parallel', 'Semantics tree không đi qua một "đường duy nhất": nó được dựng song song với composition và dùng cho cả trợ năng lẫn kiểm thử. [[src:cp-semantics]]', 'The semantics tree is not a single "pipe": it is built in parallel with composition and serves both accessibility and testing. [[src:cp-semantics]]')
m(M, 's.merge.title', 'Gộp hay không gộp', 'Merge or not')
m(M, 's.merge.on', '`Button` đặt `mergeDescendants = true`: Icon và Text được gộp vào node của nút trong cây merged.', '`Button` sets `mergeDescendants = true`: the Icon and Text are merged into the button node in the merged tree.')
m(M, 's.merge.off', 'Không gộp: mỗi phần tử là một node riêng trong cả hai cây.', 'Not merged: each element is its own node in both trees.')
m(M, 'ev.merge', 'tính cây merged', 'compute the merged tree')
m(M, 's.consume.title', 'Người đọc cây', 'The tree consumer')
m(M, 's.consume.test.merged', 'Framework kiểm thử mặc định dùng cây merged: thấy {n} node cho cả nút.', 'The testing framework uses the merged tree by default: it sees {n} node for the whole button.')
m(M, 's.consume.test.plain', 'Không có gộp nên cây merged giống cây unmerged: thấy {n} node.', 'Nothing is merged, so the merged tree equals the unmerged one: it sees {n} nodes.')
m(M, 's.consume.a11y.merged', 'Dịch vụ trợ năng nhận cây unmerged ({n} node) và tự áp dụng việc gộp.', 'The accessibility service receives the unmerged tree ({n} nodes) and applies merging itself.')
m(M, 's.consume.a11y.plain', 'Dịch vụ trợ năng nhận cây unmerged: {n} node.', 'The accessibility service receives the unmerged tree: {n} nodes.')
m(M, 'ev.consume', 'thấy {n} node', 'sees {n} nodes')
m(M, 'st.nodes', 'Số node thấy được', 'Visible nodes')
m(M, 'co.x6', 'WCAG và thiết kế bao hàm nằm ở cầu nối X6 (chương E10). [[src:cp-semantics]]', 'WCAG and inclusive design live in bridge X6 (chapter E10). [[src:cp-semantics]]')

# ---------------- B10: +1 ----------------
M = 'counter'
m(M, 'title', 'Luồng +1: tám bước', 'The +1 flow: eight steps')
m(M, 'overview', 'Màn hình đếm số. Bấm `+1` và theo dõi toàn bộ đường đi từ handler tới các phase. Đổi giá trị bắt đầu và loại tham số của `Header` để thấy bước 6 và 7 thay đổi.',
  'A counter screen. Tap `+1` and follow the whole path from the handler to the phases. Change the start value and the `Header` parameter kind to see steps 6 and 7 change.')
m(M, 'wrapup', 'Ghi state → snapshot → invalidate scope đã đọc → Recomposer → Composer chạy lại phần cần thiết và skip phần không đổi → Applier chỉ đổi cấu trúc khi cần → layout và draw.',
  'Write state → snapshot → invalidate the scope that read it → Recomposer → the Composer re-runs what is needed and skips what is unchanged → the Applier changes structure only when needed → layout and drawing.')
m(M, 'simp.1', 'Tám bước là cách chia để giảng giải; runtime thật gộp, sắp xếp và tối ưu các bước này khác đi.', 'The eight steps are a teaching split; the real runtime batches, orders and optimises them differently.')
m(M, 'simp.2', 'Đếm số composable recompose/skip là minh họa cho ví dụ này.', 'Counts of recomposed/skipped composables are illustrative for this example.')
m(M, 'ctl.hint', 'Đổi giá trị bắt đầu hoặc tham số của Header.', 'Change the start value or the Header parameter.')
m(M, 'ctl.start', 'count bắt đầu ở', 'count starts at')
m(M, 'ctl.start.n', '{n}', '{n}')
m(M, 'ctl.child', 'Tham số của Header', 'Header parameter')
m(M, 'ctl.child.stable', 'title = "Counter" (stable)', 'title = "Counter" (stable)')
m(M, 'ctl.child.unstable', 'tags = listOf("a") (unstable, instance mới)', 'tags = listOf("a") (unstable, new instance)')
m(M, 'diagramTitle', 'Sơ đồ runtime: luồng +1', 'Runtime diagram: the +1 flow')
m(M, 'diagramDesc', 'Từ cây UI (nút bấm) tới Snapshot, Recomposer, Composer, Applier và các phase.', 'From the UI tree (the button) through Snapshot, Recomposer, Composer, Applier and the phases.')
for k, vi, en in [('count', 'count', 'count'), ('recomposed', 'Composable recompose', 'Recomposed composables'), ('skipped', 'Composable skip', 'Skipped composables')]:
    m(M, 'met.' + k, vi, en)
m(M, 'st.count', 'count', 'count')
steps = [
 ('s1', 'Handler chạy count++', 'Handler runs count++', '`onClick` chạy `count++`: ghi giá trị {c1} vào `MutableState`.', '`onClick` runs `count++`: it writes {c1} into the `MutableState`.', 'ghi count = {c1}', 'write count = {c1}'),
 ('s2', 'Snapshot ghi nhận thay đổi', 'Snapshot records the change', 'Lần ghi đi vào global snapshot; khi thay đổi được apply, apply observer được báo.', 'The write goes to the global snapshot; when the change is applied, apply observers are notified.', 'apply thay đổi', 'apply the change'),
 ('s3', 'Scope đã đọc count bị invalidate', 'The scope that read count is invalidated', '`Text("Count: $count")` đọc `count` trong scope của `CounterScreen`, nên chính scope đó bị đánh dấu cần chạy lại, không phải toàn bộ cây.', '`Text("Count: $count")` reads `count` in the `CounterScreen` scope, so that scope is marked to run again, not the whole tree.', 'invalidate scope CounterScreen', 'invalidate the CounterScreen scope'),
 ('s4', 'Recomposer nhận công việc', 'The Recomposer takes the work', 'Recomposer thấy có scope bị invalidate và lên lịch recompose cho Composition.', 'The Recomposer sees an invalidated scope and schedules a recompose for the Composition.', 'lên lịch recompose', 'schedule a recompose'),
 ('s5', 'Composer chạy lại phần cần thiết', 'The Composer re-runs what is needed', 'Composer chạy lại scope của `CounterScreen` và so sánh: chuỗi của `Text` đổi thành "Count: {c1}".', 'The Composer re-runs the `CounterScreen` scope and compares: the `Text` string becomes "Count: {c1}".', 'recompose CounterScreen', 'recompose CounterScreen'),
 ('s6', 'Composable con được skip?', 'Are child composables skipped?', None, None, None, None),
 ('s7', 'Applier cập nhật cây UI', 'The Applier updates the UI tree', None, None, None, None),
 ('s8', 'Các phase cần thiết chạy', 'The needed phases run', None, None, 'layout và draw', 'layout and drawing'),
]
for sid, tv, te, xv, xe, ev, ee in steps:
    m(M, 's.' + sid + '.title', tv, te)
    if xv: m(M, 's.' + sid + '.explain', xv, xe)
    if ev: m(M, 'ev.' + sid, ev, ee)
m(M, 's6.skip', '`Header(title = "Counter")`: tham số stable, `equals` với lần trước, nên được skip. `Button` cũng được skip vì lambda `{ count++ }` được nhớ và tham số không đổi.', '`Header(title = "Counter")`: a stable parameter equal to last time, so it is skipped. `Button` is skipped too because the `{ count++ }` lambda is remembered and its parameters are unchanged.')
m(M, 's6.recompose', '`Header(tags = listOf("a"))`: `List` được coi là unstable và mỗi lần là instance mới, nên phép so `===` thất bại và `Header` recompose. `Button` vẫn được skip.', '`Header(tags = listOf("a"))`: `List` is treated as unstable and is a new instance each time, so the `===` check fails and `Header` recomposes. `Button` is still skipped.')
m(M, 'ev.s6.skip', 'skip Header, Button', 'skip Header, Button')
m(M, 'ev.s6.recompose', 'recompose Header; skip Button', 'recompose Header; skip Button')
m(M, 'sk.header', 'Header', 'Header')
m(M, 'sk.headerStable', 'tham số stable, bằng lần trước', 'stable parameter, equal to last time')
m(M, 'sk.button', 'Button', 'Button')
m(M, 'sk.buttonSame', 'tham số không đổi (lambda được nhớ)', 'parameters unchanged (the lambda is remembered)')
m(M, 'co.unstable', 'Recompose này không làm sai kết quả, chỉ thêm việc. Xem B8 trước khi nghĩ tới `@Stable`.', 'This recompose does not make the result wrong, it only adds work. See B8 before reaching for `@Stable`.')
m(M, 's7.insert', 'Đi từ 0 lên 1 làm điều kiện `count > 0` thành đúng: có một node `Text("Started!")` mới cần chèn, và chữ của Text đếm số được cập nhật.', 'Going from 0 to 1 makes `count > 0` true: a new `Text("Started!")` node must be inserted, and the counter Text string is updated.')
m(M, 's7.update', 'Từ {c0} lên {c1}, cấu trúc không đổi: Applier chỉ cập nhật chữ của node Text, không chèn hay xóa node.', 'From {c0} to {c1} the structure is unchanged: the Applier only updates the Text node string, with no insert or removal.')
m(M, 'ev.s7.insert', 'chèn Text("Started!"), cập nhật Text', 'insert Text("Started!"), update Text')
m(M, 'ev.s7.update', 'cập nhật Text', 'update Text')
m(M, 's8.structural', 'Cây có node mới nên Layout đo và đặt lại, rồi Drawing vẽ. Phase nào chạy tùy nơi state được đọc (B7).', 'The tree has a new node, so Layout measures and places again, then Drawing draws. Which phase runs depends on where the state was read (B7).')
m(M, 's8.text', 'Chữ đổi có thể đổi kích thước, nên Layout và Drawing chạy cho phần bị ảnh hưởng. Phase nào chạy tùy nơi state được đọc (B7).', 'Changed text can change size, so Layout and Drawing run for the affected part. Which phase runs depends on where the state was read (B7).')
m(M, 'ch.write', 'count: {c0} → {c1}', 'count: {c0} → {c1}')
m(M, 'ch.text', 'Text: "Count: {c1}"', 'Text: "Count: {c1}"')
m(M, 'ch.badge', 'Nhánh if (count > 0) mở ra một group mới', 'The if (count > 0) branch opens a new group')
m(M, 'ch.insertNode', 'Chèn node Text("Started!")', 'Insert the Text("Started!") node')
m(M, 'ch.updateNode', 'Cập nhật node Text thành "Count: {c1}"', 'Update the Text node to "Count: {c1}"')
m(M, 'co.snapshot', 'Đọc và ghi `MutableState` đi qua hệ thống Snapshot; xem B4. [[src:rt-snapshot]]', 'Reading and writing a `MutableState` goes through the Snapshot system; see B4. [[src:rt-snapshot]]')
m(M, 'co.x1', 'Cầu nối X1: phase nào chạy lại tùy nơi state được đọc; chương B7 giải thích đầy đủ. [[src:cp-phases]]', 'Bridge X1: which phase runs again depends on where the state is read; chapter B7 explains it fully. [[src:cp-phases]]')

# ---------------- chương ----------------
def ch(c, title, essence, g1, g2, secs, quiz):
    a(c + '.title', *title); a(c + '.essence', *essence); a(c + '.goal.g1', *g1); a(c + '.goal.g2', *g2)
    for sid, stitle, badge, paras in secs:
        a(c + '.sec.' + sid + '.title', *stitle); a(c + '.sec.' + sid + '.badge', badge, badge)
        for i, p in enumerate(paras): a(c + '.sec.' + sid + '.p.' + str(i + 1), *p)
    for i, (q, ans, why) in enumerate(quiz):
        a(c + '.quiz.q%d.q' % (i + 1), *q); a(c + '.quiz.q%d.a' % (i + 1), *ans); a(c + '.quiz.q%d.why' % (i + 1), *why)

ch('b0', ('Bản đồ toàn cảnh', 'The big map'),
   ('Compose Runtime gồm nhiều vai trò: host, Composition, Recomposer, mã đã được compiler biến đổi, Composer, SlotTable, Snapshot, Applier, cây UI, các phase và semantics tree.\nMỗi vai trò làm một việc; gộp chúng thành một "engine" làm khó hiểu vì sao một thay đổi nhỏ chỉ làm chạy lại một phần nhỏ.\nTrình duyệt không chạy Compose Runtime thật: site là mô hình giảng dạy.',
    'Compose Runtime has many roles: the host, Composition, Recomposer, compiler-transformed code, Composer, SlotTable, Snapshot, Applier, the UI tree, the phases and the semantics tree.\nEach role does one job; lumping them into one "engine" makes it hard to see why a small change re-runs only a small part.\nThe browser does not run the real Compose Runtime: the site is a teaching model.'),
   ('Đã xem vai trò của ít nhất một thành phần', 'Looked at the role of at least one component'), ('Đã đi hết ba bước của một thành phần', 'Walked all three steps for one component'),
   [('roles', ('Bốn vai trò hay bị gộp', 'Four roles that get lumped together'), 'stable', [
      ('[[term:composition]] giữ kết quả của các composable; [[term:recomposer]] lên lịch recomposition và apply; [[term:composer]] là giao diện mà mã sinh ra gọi tới; [[term:applier]] áp dụng thao tác lên cây. [[src:rt-how]] [[src:rt-recomposer]] [[src:rt-applier]]',
       '[[term:composition]] holds the result of composables; the [[term:recomposer]] schedules recomposition and applying; the [[term:composer]] is the interface generated code calls; the [[term:applier]] applies operations to a tree. [[src:rt-how]] [[src:rt-recomposer]] [[src:rt-applier]]'),
      ('Phần chung của runtime khác phần Android host: `ComposeView`, `AndroidComposeView`, `Owner`, `LayoutNode` là chi tiết của Compose UI trên Android. [[badge:android-impl]]',
       'The shared runtime differs from the Android host: `ComposeView`, `AndroidComposeView`, `Owner` and `LayoutNode` are details of Compose UI on Android. [[badge:android-impl]]'),
      ('Site đối chiếu với `compose.runtime` và `compose.ui` 1.13.0 (Compose BOM 2026.11.01), Compose Compiler đi cùng Kotlin 2.4.21. Release notes chỉ dùng để xác định phiên bản, không phải nguồn về kiến trúc. [[badge:version]] [[src:rt-releases]]',
       'The site was checked against `compose.runtime` and `compose.ui` 1.13.0 (Compose BOM 2026.11.01), with the Compose Compiler that ships with Kotlin 2.4.21. Release notes are used only to pin versions, not as a source on architecture. [[badge:version]] [[src:rt-releases]]')]),
    ('theme', ('MaterialTheme cũng là dữ liệu trong Composition', 'MaterialTheme is data in the Composition too'), 'stable', [
      ('`MaterialTheme` cung cấp màu, typography và shape qua `CompositionLocal`, tức là dữ liệu đi xuống theo cây composition. Cầu nối X5 (chương E8) nói đầy đủ về theming. [[src:rt-pkg]]',
       '`MaterialTheme` provides colors, typography and shapes through a `CompositionLocal`, that is, data passed down the composition tree. Bridge X5 (chapter E8) covers theming in full. [[src:rt-pkg]]')])],
   [(('Recomposer và Composer có phải là một?', 'Are the Recomposer and the Composer the same thing?'), ('Không.', 'No.'),
     ('Recomposer lên lịch và điều phối; Composer là giao diện mà mã composable gọi khi chạy để nhớ và so sánh.', 'The Recomposer schedules and coordinates; the Composer is the interface composable code calls while running to remember and compare.')),
    (('SlotTable có phải là cây UI?', 'Is the SlotTable the UI tree?'), ('Không.', 'No.'),
     ('SlotTable nhớ dữ liệu theo group và vị trí; cây UI (trên Android là `LayoutNode`) là thứ được đo và vẽ.', 'The SlotTable remembers data by group and position; the UI tree (`LayoutNode` on Android) is what gets measured and drawn.'))])

ch('b1', ('Chuyện gì xảy ra khi gọi setContent', 'What happens when you call setContent'),
   ('`setContent` đưa nội dung cho host; composition ban đầu chạy khi điều kiện của host phù hợp, ví dụ view được gắn vào window.\nRuntime gọi mã đã được compiler biến đổi; Composer xây trạng thái composition; Applier dựng cây; Compose UI đo, đặt và vẽ.\nKhông phải mọi lần gọi `setContent` đều tạo một Composition hoàn toàn mới: điều đó tùy host và vòng đời.',
    '`setContent` hands content to the host; the initial composition runs when the host is ready, for example when the view is attached to a window.\nThe runtime calls compiler-transformed code; the Composer builds the composition state; the Applier builds the tree; Compose UI measures, places and draws.\nNot every `setContent` call creates a brand-new Composition: that depends on the host and its lifecycle.'),
   ('Đã thấy điều gì kích hoạt composition ban đầu', 'Saw what triggers the initial composition'), ('Đã thử tắt "tạo khi gắn window"', 'Tried turning off "create on attach"'),
   [('host', ('ComposeView và thời điểm composition ban đầu', 'ComposeView and when the initial composition happens'), 'android-impl', [
      ('Theo reference của `ComposeView`, composition ban đầu xảy ra khi view được gắn vào window hoặc khi gọi `createComposition()`, cái nào đến trước. `shouldCreateCompositionOnAttachedToWindow` mặc định là true; nếu đặt false, composition ban đầu vẫn xảy ra ở lần measure đầu. [[src:rt-composeview]]',
       'According to the `ComposeView` reference, the initial composition happens when the view is attached to a window or when `createComposition()` is called, whichever comes first. `shouldCreateCompositionOnAttachedToWindow` defaults to true; if set to false, the initial composition still happens at the first measure. [[src:rt-composeview]]'),
      ('`ComposeView` cần LifecycleOwner và SavedStateRegistryOwner trong cây View; mặc định composition được giải phóng theo `ViewCompositionStrategy.Default`. [[badge:android-impl]]',
       '`ComposeView` needs a LifecycleOwner and a SavedStateRegistryOwner in the View tree; by default the composition is disposed according to `ViewCompositionStrategy.Default`. [[badge:android-impl]]')])],
   [(('Gọi `setContent` có lập tức chạy composable không?', 'Does calling `setContent` run the composable immediately?'), ('Không nhất thiết.', 'Not necessarily.'),
     ('Với `ComposeView`, composition ban đầu chờ tới khi gắn window, gọi `createComposition()` hoặc measure lần đầu.', 'With `ComposeView`, the initial composition waits for attaching, a `createComposition()` call or the first measure.')),
    (('Runtime gọi đúng hàm bạn viết?', 'Does the runtime call exactly the function you wrote?'), ('Không hẳn.', 'Not quite.'),
     ('Nó gọi phiên bản đã được Compose Compiler biến đổi (thêm `$composer`, group, kiểm tra skip). Xem B2.', 'It calls the version transformed by the Compose Compiler (with `$composer`, groups and skip checks). See B2.'))])

ch('b2', ('Compiler transform: composable, Composer và điều kiện skip', 'Compiler transform: composables, the Composer and the skip check'),
   ('Compose Compiler là Kotlin compiler plugin; nó biến đổi hàm `@Composable` để làm việc với Composer.\nComposer điều phối group, vị trí, so sánh tham số, nhớ giá trị và hỗ trợ skip, restart.\nMã giả trong chương này là minh họa, không phải mã compiler bảo đảm sinh ra.',
    'The Compose Compiler is a Kotlin compiler plugin; it transforms `@Composable` functions to work with the Composer.\nThe Composer coordinates groups, positions, parameter comparison, remembered values, skipping and restarting.\nThe pseudo-code in this chapter is illustrative, not guaranteed compiler output.'),
   ('Đã so hai nhánh: tham số đổi và không đổi', 'Compared both branches: parameter changed and unchanged'), ('Đã thấy khi nào có update scope', 'Saw when there is an update scope'),
   [('transform', ('Mã sau transform, ở mức khái niệm', 'Code after the transform, at a conceptual level'), 'impl simplified', [
      ('Tài liệu thiết kế của runtime (nhánh androidx-main, `compose/runtime/design/how-compose-works.md`, đọc 2026-11-21) mô tả: hàm nhận thêm `$composer`, thân hàm được bọc trong group; hàm restartable dùng restart group; nếu Composer cho phép và tham số không đổi thì nhảy tới cuối group. [[src:rt-how]] [[badge:impl]]',
       'The runtime design document (androidx-main branch, `compose/runtime/design/how-compose-works.md`, read 2026-11-21) describes it: the function gets an extra `$composer`, its body is wrapped in a group; restartable functions use a restart group; if the Composer allows it and parameters are unchanged, it skips to the end of the group. [[src:rt-how]] [[badge:impl]]'),
      ('`changed()` chỉ có nghĩa trong ngữ cảnh vị trí và group mà Composer đang duyệt; site không hướng dẫn gọi nó thủ công, cũng không khuyến khích dùng `currentComposer` hay API nội bộ. Tham số `$changed` chỉ được nhắc tên. [[badge:impl]]',
       '`changed()` only makes sense in the position and group the Composer is currently visiting; the site does not teach calling it by hand, nor using `currentComposer` or internal APIs. The `$changed` parameter is only mentioned by name. [[badge:impl]]'),
      ('Bối cảnh Kotlin: compiler plugin là cơ chế chung của Kotlin; đọc thêm về compiler plugin trong tài liệu Kotlin nếu cần.',
       'Kotlin background: compiler plugins are a general Kotlin mechanism; read more about compiler plugins in the Kotlin documentation if needed.')])],
   [(('Có nên gọi `currentComposer.changed()` để tự tối ưu?', 'Should you call `currentComposer.changed()` to optimise by hand?'), ('Không.', 'No.'),
     ('Đó là API dành cho mã do compiler sinh, phụ thuộc vị trí Composer đang duyệt.', 'It is an API for compiler-generated code and depends on where the Composer currently is.')),
    (('Khi nào `endRestartGroup()` trả `null` trong mã giả?', 'When does `endRestartGroup()` return `null` in the pseudo-code?'), ('Khi thân hàm không có lần đọc state quan sát được.', 'When the body made no observable state read.'),
     ('Không có gì để theo dõi nên không cần cách chạy lại riêng hàm đó.', 'There is nothing to observe, so no separate way to re-run that function is needed.'))])

ch('b3', ('Composition identity và SlotTable', 'Composition identity and the SlotTable'),
   ('Identity của một instance composable dựa trên call site, nhánh điều kiện, vòng lặp và `key()`.\nKhông có key, item trong vòng lặp được nhận diện theo thứ tự; có key, theo giá trị key.\nCompose không diff toàn cây kiểu Virtual DOM, nhưng runtime vẫn theo dõi cấu trúc và áp dụng thay đổi tăng dần.',
    'The identity of a composable instance is based on the call site, conditional branches, loops and `key()`.\nWithout a key, items in a loop are identified by order; with a key, by the key value.\nCompose does not diff the whole tree like a Virtual DOM, but the runtime still tracks structure and applies changes incrementally.'),
   ('Đã thử một thao tác trên danh sách', 'Tried one list operation'), ('Đã so cùng thao tác có và không có key', 'Compared the same operation with and without a key'),
   [('identity', ('Call site, thứ tự và key()', 'Call site, order and key()'), 'stable', [
      ('Mỗi lời gọi composable được nhận diện theo call site; gọi nhiều lần từ cùng call site thì thêm thứ tự thực thi. Thêm item vào cuối: instance cũ được tái dùng. Chèn đầu, xóa giữa hay đổi chỗ: các item đổi đầu vào bị recompose và effect của chúng bị hủy rồi chạy lại. [[src:cp-lifecycle]]',
       'Each composable call is identified by its call site; calls from the same call site add execution order. Adding an item at the end reuses the old instances. Inserting at the top, removing in the middle or reordering recomposes the items whose input changed, and their effects are cancelled and restarted. [[src:cp-lifecycle]]'),
      ('`key(movie.id) { … }` cho runtime giữ instance theo id, kể cả khi item di chuyển. Nên dùng khi nhiều composable từ cùng call site có state hoặc effect. Không đúng khi nói thiếu `key()` thì mọi item luôn bị tạo lại: kết quả tùy thao tác. [[src:cp-lifecycle]]',
       '`key(movie.id) { … }` lets the runtime keep instances by id, even when items move. Use it when several composables from one call site have state or effects. It is wrong to say that without `key()` every item is always recreated: the outcome depends on the operation. [[src:cp-lifecycle]]')]),
    ('slots', ('SlotTable ở mức khái niệm', 'The SlotTable at a conceptual level'), 'impl', [
      ('SlotTable là dữ liệu có cấu trúc theo group và vị trí, dùng để nhớ giá trị (`remember`), nhận diện phần composition và cập nhật tăng dần. Nó khác cây node UI. [[src:rt-how]]',
       'The SlotTable is data organised by groups and positions, used to remember values (`remember`), identify parts of the composition and update incrementally. It differs from the UI node tree. [[src:rt-how]]'),
      ('Tài liệu thiết kế (androidx-main, đọc 2026-11-21) mô tả hai mảng phẳng cho group và slot, quản lý theo kiểu gap buffer, và tự cảnh báo rằng SlotTable đang được phát triển nên vài chi tiết có thể đã cũ. Site không mô tả bố cục bộ nhớ cụ thể. [[badge:impl]] [[src:rt-how]]',
       'The design document (androidx-main, read 2026-11-21) describes two flat arrays for groups and slots, managed as a gap buffer, and itself warns that the SlotTable is under development so some details may be out of date. The site does not describe a specific memory layout. [[badge:impl]] [[src:rt-how]]')])],
   [(('Không có `key()` thì mọi item luôn bị tạo lại?', 'Without `key()`, is every item always recreated?'), ('Không.', 'No.'),
     ('Thêm vào cuối thì các item cũ được tái dùng; chèn đầu thì các vị trí đổi đầu vào bị recompose, còn `remember` không key ở lại theo vị trí.', 'Adding at the end reuses the old items; inserting at the top recomposes the positions whose input changed, while a key-less `remember` stays with the position.')),
    (('SlotTable là mảng `Any?` chứa LayoutNode và mọi tham số?', 'Is the SlotTable an `Any?` array holding LayoutNodes and all parameters?'), ('Không nên mô tả như vậy.', 'It should not be described that way.'),
     ('Nó là dữ liệu theo group để nhớ và nhận diện; cây node UI là một cấu trúc khác.', 'It is group-based data for remembering and identification; the UI node tree is a different structure.'))])

ch('b4', ('State và Snapshot', 'State and Snapshot'),
   ('`mutableStateOf` tạo state quan sát được qua hệ thống Snapshot.\nĐọc `State.value` tạo quan hệ theo dõi với scope hoặc phase đang đọc; ghi tạo ra thay đổi.\nKhi thay đổi được apply và quan sát, runtime có thể invalidate các phần phụ thuộc. Thay đổi state không chạy lại toàn bộ cây.',
    '`mutableStateOf` creates state observed through the Snapshot system.\nReading `State.value` creates a tracking relation with the scope or phase doing the read; writing creates a change.\nWhen the change is applied and observed, the runtime can invalidate the dependent parts. A state change does not re-run the whole tree.'),
   ('Đã ghi state trong và ngoài mutable snapshot', 'Wrote state inside and outside a mutable snapshot'), ('Đã thấy trường hợp không có gì để recompose', 'Saw the case where there is nothing to recompose'),
   [('snapshot', ('Snapshot: cách ly, apply, quan sát', 'Snapshot: isolation, apply, observation'), 'stable', [
      ('Snapshot cho một góc nhìn cách ly về giá trị của các state object. Thay đổi trong mutable snapshot chỉ thấy bên trong nó tới khi `apply()` áp dụng chúng nguyên tử; apply có thể xung đột. Composition dùng read observer và write observer để biết ai đọc và ai ghi. [[src:rt-snapshot]]',
       'A snapshot gives an isolated view of the values of state objects. Changes in a mutable snapshot are visible only inside it until `apply()` applies them atomically; applying can conflict. Composition uses read and write observers to learn who reads and who writes. [[src:rt-snapshot]]'),
      ('`StateObject` và `StateRecord` là mô hình khái niệm: một state có thể có nhiều record cho nhiều snapshot. Site không mô tả cấu trúc bộ nhớ của chúng. [[badge:impl]]',
       '`StateObject` and `StateRecord` are a conceptual model: one state can have several records for several snapshots. The site does not describe their memory layout. [[badge:impl]]'),
      ('Bối cảnh Kotlin: `var count by mutableStateOf(0)` dùng property delegation; getter đọc `value`, setter ghi `value`.',
       'Kotlin background: `var count by mutableStateOf(0)` uses property delegation; the getter reads `value` and the setter writes it.')]),
    ('flow', ('Snapshot state và StateFlow', 'Snapshot state and StateFlow'), 'stable', [
      ('`StateFlow` là Flow của kotlinx.coroutines; để dùng trong UI, `collectAsStateWithLifecycle()` thu nó thành Snapshot `State` theo Lifecycle. Cầu nối X2 (chương A8) nói đầy đủ. [[src:and-state]]',
       '`StateFlow` is a kotlinx.coroutines Flow; to use it in UI, `collectAsStateWithLifecycle()` collects it into a Snapshot `State` following the Lifecycle. Bridge X2 (chapter A8) covers it fully. [[src:and-state]]')])],
   [(('Ghi state có làm cả cây recompose?', 'Does writing state recompose the whole tree?'), ('Không.', 'No.'),
     ('Chỉ những scope đã đọc state đó bị invalidate.', 'Only the scopes that read that state are invalidated.')),
    (('Ghi trong mutable snapshot thì global thấy ngay?', 'Does global see a write inside a mutable snapshot right away?'), ('Không.', 'No.'),
     ('Chỉ sau khi snapshot được apply.', 'Only after the snapshot is applied.'))])

ch('b5', ('Recomposer và frame clock', 'The Recomposer and the frame clock'),
   ('Recomposer theo dõi và điều phối recomposition cho các Composition nó quản lý: invalidation, việc chờ, cập nhật.\n`MonotonicFrameClock` cung cấp thời điểm frame; `withFrameNanos` là API low-level để chờ frame.\nKhông có quy tắc "Recomposer chỉ chạy khi Snapshot đổi" hay "mỗi frame đúng một lần recomposition": composition ban đầu, invalidation, việc theo frame và effect đều tham gia.',
    'The Recomposer tracks and coordinates recomposition for the Compositions it manages: invalidations, pending work, updates.\n`MonotonicFrameClock` provides frame times; `withFrameNanos` is a low-level API to wait for a frame.\nThere is no rule that "the Recomposer runs only when Snapshot changes" or "exactly one recomposition per frame": initial composition, invalidation, frame work and effects all take part.'),
   ('Đã thấy nhiều lần ghi được xử lý trong một lượt', 'Saw several writes handled in one pass'), ('Đã thử tạm dừng frame clock', 'Tried pausing the frame clock'),
   [('rec', ('Recomposer chạy trong coroutine', 'The Recomposer runs in a coroutine'), 'stable', [
      ('`runRecomposeAndApplyChanges()` là suspend function: chờ composer bị invalidate, recompose, apply, và chỉ trả về khi Recomposer bị đóng. Recomposer được tạo với một `CoroutineContext` cho effect. [[src:rt-recomposer]]',
       '`runRecomposeAndApplyChanges()` is a suspend function: it awaits invalidated composers, recomposes, applies, and returns only when the Recomposer is closed. The Recomposer is created with a `CoroutineContext` for effects. [[src:rt-recomposer]]')]),
    ('x3', ('Cầu nối X3: frame clock', 'Bridge X3: the frame clock'), 'stable', [
      ('`MonotonicFrameClock` là một phần tử của `CoroutineContext`. `withFrameNanos { t -> … }` suspend tới khi có frame mới, gọi khối với thời điểm frame tính bằng nano giây, rồi resume với kết quả. Thời điểm tăng nghiêm ngặt giữa các lần gọi; nên dùng nó để tính độ chênh cho animation. [[src:rt-frameclock]]',
       '`MonotonicFrameClock` is a `CoroutineContext` element. `withFrameNanos { t -> … }` suspends until a new frame, calls the block with the frame time in nanoseconds, then resumes with the result. Times strictly increase between calls; use them to compute animation deltas. [[src:rt-frameclock]]'),
      ('Vì frame clock nằm trong context của coroutine, coroutine có một nhịp khác với dispatcher: nhịp theo frame. Recomposer có thể tạm dừng và chạy lại frame clock, ví dụ khi UI không ở foreground. Site không ghi thời lượng frame cố định. Chương A4 (dispatcher) và C7 (animation theo frame) chỉ nhắc lại phần này. [[src:rt-recomposer]]',
       'Because the frame clock lives in the coroutine context, a coroutine gets a different rhythm from the dispatcher: one tied to frames. The Recomposer can pause and resume the frame clock, for example when the UI is not in the foreground. The site does not state a fixed frame duration. Chapters A4 (dispatchers) and C7 (frame-based animation) only recap this part. [[src:rt-recomposer]]')])],
   [(('Recomposer chỉ chạy khi Snapshot đổi?', 'Does the Recomposer run only when Snapshot changes?'), ('Không.', 'No.'),
     ('Composition ban đầu, việc theo frame và effect cũng đi qua nó.', 'Initial composition, frame work and effects also go through it.')),
    (('Mỗi frame có đúng một lần recomposition?', 'Is there exactly one recomposition per frame?'), ('Không có quy tắc như vậy.', 'There is no such rule.'),
     ('Có frame không có recomposition nào; công việc được gom và lên lịch theo trạng thái invalidation.', 'Some frames have no recomposition; work is batched and scheduled by invalidation state.'))])

ch('b6', ('Composer ghi nhận, Applier áp dụng', 'The Composer records, the Applier applies'),
   ('Tính thay đổi và áp dụng thay đổi là hai bước liên quan nhưng không phải một.\nApplier áp dụng thao tác cây (chèn, xóa, di chuyển, cập nhật) mà composition phát ra.\n`Applier<N>` là điểm mở rộng cho nhiều loại cây, không chỉ trên Android.',
    'Computing changes and applying them are two related steps, not one.\nThe Applier applies the tree operations (insert, remove, move, update) emitted by the composition.\n`Applier<N>` is an extension point for many kinds of trees, not only on Android.'),
   ('Đã xem ít nhất một loại thay đổi', 'Looked at at least one kind of change'), ('Đã thấy đổi chữ không tạo thao tác cấu trúc', 'Saw that changing text creates no structural operation'),
   [('applier', ('Giao diện Applier', 'The Applier interface'), 'stable', [
      ('Mỗi Composer có một Applier. Thao tác gồm `insertTopDown` hoặc `insertBottomUp` (cài đặt một trong hai), `down`/`up` để duyệt, `move`, `remove`, `clear`; mỗi đợt được bao bởi `onBeginChanges()` và `onEndChanges()`. [[src:rt-applier]]',
       'Every Composer has an Applier. Operations include `insertTopDown` or `insertBottomUp` (implement one of the two), `down`/`up` for traversal, `move`, `remove` and `clear`; each batch is wrapped by `onBeginChanges()` and `onEndChanges()`. [[src:rt-applier]]'),
      ('Trên Android, Compose UI dùng một applier nội bộ (`UiApplier` ở bản đọc được) cho cây `LayoutNode`; đây là chi tiết cài đặt, không phải API ứng dụng. [[badge:android-impl]]',
       'On Android, Compose UI uses an internal applier (`UiApplier` in the version read) for the `LayoutNode` tree; it is an implementation detail, not an app API. [[badge:android-impl]]')])],
   [(('Applier chỉ có trên Android?', 'Does the Applier exist only on Android?'), ('Không.', 'No.'),
     ('`Applier<N>` là generic; cần một Applier riêng để dựng loại cây mới.', '`Applier<N>` is generic; a new kind of tree needs its own Applier.')),
    (('Đổi chữ của Text có chèn lại node?', 'Does changing a Text string re-insert the node?'), ('Không.', 'No.'),
     ('Cấu trúc không đổi; chỉ giá trị của node hiện có được cập nhật.', 'The structure is unchanged; only the value on the existing node is updated.'))])

ch('b7', ('Composition, Layout, Drawing', 'Composition, Layout, Drawing'),
   ('Ba phase: Composition quyết định hiển thị gì, Layout đo và đặt, Drawing vẽ.\nState được đọc ở phase nào thì phase đó cần chạy lại; phase không đọc state đó có thể được bỏ qua.\nRecomposition không đồng nghĩa với vẽ lại toàn màn hình.',
    'Three phases: Composition decides what to show, Layout measures and places, Drawing draws.\nThe phase that reads a state is the one that needs to run again; phases that do not read it can be skipped.\nRecomposition does not mean redrawing the whole screen.'),
   ('Đã xác định state được đọc ở đâu', 'Identified where the state is read'), ('Đã so đèn phase cho cả ba nơi đọc', 'Compared the phase lights for all three read sites'),
   [('x1', ('Cầu nối X1: state được đọc ở đâu', 'Bridge X1: where the state is read'), 'stable', [
      ('Đọc trong composable hay lambda `@Composable` ảnh hưởng Composition: scope đọc state bị recompose; Layout và Drawing chạy sau đó nhưng có thể được bỏ qua nếu nội dung, kích thước và vị trí không đổi. [[src:cp-phases]]',
       'A read inside a composable or `@Composable` lambda affects Composition: the reading scope recomposes; Layout and Drawing run afterwards but can be skipped if content, size and position did not change. [[src:cp-phases]]'),
      ('Đọc trong lambda đo hoặc trong bước đặt vị trí (ví dụ `Modifier.offset { }`) ảnh hưởng Layout, và Drawing chỉ khi kích thước hay vị trí đổi. Đo và đặt có restart scope riêng. Đọc trong `Canvas`, `drawBehind`, `drawWithContent` chỉ ảnh hưởng Drawing. [[src:cp-phases]]',
       'A read inside a measure lambda or in the placement step (for example `Modifier.offset { }`) affects Layout, and Drawing only if size or position changed. Measure and placement have separate restart scopes. A read in `Canvas`, `drawBehind` or `drawWithContent` affects only Drawing. [[src:cp-phases]]'),
      ('Ví dụ trong tài liệu: đổi `Modifier.offset(x.dp)` sang `Modifier.offset { … }` khi giá trị đổi theo cuộn, để mỗi lần cuộn chỉ chạy Layout và Drawing thay vì recompose. Ghi state từ `onSizeChanged` rồi dùng trong layout tạo vòng lặp phase và tốn thêm frame. Các chương C1, C5, C7, E9 chỉ nhắc lại phần này và dẫn về đây. [[src:cp-phases]] [[badge:guideline]]',
       'Example from the documentation: switch `Modifier.offset(x.dp)` to `Modifier.offset { … }` when the value follows scrolling, so each scroll runs only Layout and Drawing instead of recomposing. Writing state from `onSizeChanged` and using it in layout creates a phase loop and costs an extra frame. Chapters C1, C5, C7 and E9 only recap this part and link back here. [[src:cp-phases]] [[badge:guideline]]')])],
   [(('Recomposition có nghĩa là vẽ lại cả màn hình?', 'Does recomposition mean redrawing the whole screen?'), ('Không.', 'No.'),
     ('Recomposition là chạy lại composable; Layout và Drawing chạy riêng và có thể được bỏ qua.', 'Recomposition is re-running composables; Layout and Drawing run separately and can be skipped.')),
    (('Đọc state trong `drawBehind` thì phase nào chạy lại?', 'If state is read in `drawBehind`, which phase runs again?'), ('Chỉ Drawing.', 'Only Drawing.'),
     ('State chỉ được đọc trong phase Drawing.', 'The state is read only in the Drawing phase.'))])

ch('b8', ('Skip, stability và tính đúng đắn', 'Skipping, stability and correctness'),
   ('Skip phụ thuộc mã do compiler sinh, vị trí, trạng thái invalidation và giá trị tham số.\nStable hay unstable quyết định cách so sánh tham số; strong skipping (mặc định từ Kotlin 2.0.20) đổi quy tắc cho tham số unstable.\nComposable phải an toàn khi chạy lại và tránh side effect tùy tiện, vì recomposition có thể bị hủy hoặc chạy lại.',
    'Skipping depends on compiler-generated code, position, invalidation state and parameter values.\nStable or unstable decides how parameters are compared; strong skipping (the default since Kotlin 2.0.20) changes the rule for unstable parameters.\nComposables must be safe to re-run and avoid arbitrary side effects, because recomposition can be cancelled or repeated.'),
   ('Đã xem quy tắc so sánh cho một loại tham số', 'Saw the comparison rule for one parameter kind'), ('Đã bật/tắt strong skipping', 'Toggled strong skipping'),
   [('stability', ('Stable, unstable và strong skipping', 'Stable, unstable and strong skipping'), 'stable version', [
      ('Kiểu stable là kiểu bất biến, hoặc Compose biết khi nào giá trị đổi. Kiểu nguyên thủy, `String`, kiểu hàm được coi là stable; data class chỉ có `val` kiểu stable được suy ra là bất biến; `List`, `Set`, `Map` bị coi là unstable vì cài đặt có thể thay đổi được. [[src:cp-stability]] [[src:cp-lifecycle]]',
       'A stable type is immutable, or Compose knows when its value changes. Primitive types, `String` and function types are treated as stable; a data class with only `val`s of stable types is inferred immutable; `List`, `Set` and `Map` are treated as unstable because the implementation may be mutable. [[src:cp-stability]] [[src:cp-lifecycle]]'),
      ('Tham số stable được so bằng `equals`. Khi strong skipping bật, tham số unstable được so bằng `===` và mọi composable restartable đều skip được; khi tắt, composable có tham số unstable recompose mỗi lần cha recompose. Bật mặc định từ Kotlin 2.0.20; site đối chiếu Kotlin 2.4.21. [[src:cp-strong]] [[badge:version]]',
       'Stable parameters are compared with `equals`. With strong skipping on, unstable parameters are compared with `===` and every restartable composable can be skipped; with it off, a composable with unstable parameters recomposes every time its parent does. It is on by default since Kotlin 2.0.20; the site was checked against Kotlin 2.4.21. [[src:cp-strong]] [[badge:version]]'),
      ('Không gắn `@Stable`/`@Immutable` đại trà: tài liệu cảnh báo về lớp chứa collection và nói chú thích chỉ hợp khi `equals` rẻ. So sánh dựa trên `equals`, nên hợp đồng `equals` của kiểu là quan trọng. [[src:cp-stability]] [[badge:guideline]]',
       'Do not add `@Stable`/`@Immutable` everywhere: the documentation warns about classes that hold collections and says the annotations fit only where `equals` is cheap. Comparison relies on `equals`, so the type\'s `equals` contract matters. [[src:cp-stability]] [[badge:guideline]]')]),
    ('correct', ('Tính đúng đắn khi chạy lại', 'Correctness under re-runs'), 'guideline', [
      ('Recomposition lạc quan và có thể bị hủy; composable có thể chạy thường xuyên, tới mức mỗi frame của animation, và tài liệu yêu cầu viết như thể chúng có thể chạy theo thứ tự bất kỳ hoặc song song. Vì vậy composable nên nhanh, idempotent và không có side effect; side effect đặt trong effect API. [[src:cp-mental]] [[src:and-effects]]',
       'Recomposition is optimistic and can be cancelled; a composable can run often, as often as every animation frame, and the documentation asks you to write them as if they could run in any order or in parallel. So composables should be fast, idempotent and free of side effects; side effects belong in effect APIs. [[src:cp-mental]] [[src:and-effects]]'),
      ('Cầu nối X2: `LaunchedEffect` và `rememberCoroutineScope` gắn coroutine với Composition; chương A8 nói đầy đủ.', 'Bridge X2: `LaunchedEffect` and `rememberCoroutineScope` tie coroutines to the Composition; chapter A8 covers it fully.')])],
   [(('Gắn `@Stable` có luôn làm app nhanh hơn?', 'Does adding `@Stable` always make an app faster?'), ('Không.', 'No.'),
     ('Nếu kiểu không giữ hợp đồng, kết quả có thể sai; nếu `equals` đắt, so sánh có thể tốn hơn recompose.', 'If the type does not keep the contract, results can be wrong; if `equals` is expensive, comparing can cost more than recomposing.')),
    (('Strong skipping bật: tham số unstable, instance mới cùng nội dung. Child có skip?', 'Strong skipping on: an unstable parameter, a new instance with the same content. Is Child skipped?'), ('Không.', 'No.'),
     ('Tham số unstable được so bằng `===`, và đây là instance khác.', 'Unstable parameters are compared with `===`, and this is a different instance.'))])

ch('b9', ('Android host, semantics và accessibility', 'The Android host, semantics and accessibility'),
   ('Host nối Compose với vòng đời View và window.\nSemantics tree là cây song song, phục vụ accessibility và testing.\n`Owner` và `AndroidComposeView` là chi tiết cài đặt trên Android, không phải API ứng dụng.',
    'The host connects Compose to the View and window lifecycle.\nThe semantics tree is a parallel tree that serves accessibility and testing.\n`Owner` and `AndroidComposeView` are Android implementation details, not app APIs.'),
   ('Đã xem cây semantics được gộp thế nào', 'Saw how the semantics tree is merged'), ('Đã so hai người đọc cây', 'Compared the two tree consumers'),
   [('sem', ('Merged và unmerged', 'Merged and unmerged'), 'stable', [
      ('Component của foundation và Material tự điền semantics; composable tự vẽ ở mức thấp cần tự khai báo. `Button`, `clickable`, `toggleable` gộp con cháu. Dịch vụ trợ năng dùng cây unmerged và tự gộp; framework kiểm thử mặc định dùng cây merged, có `useUnmergedTree` để đổi. [[src:cp-semantics]]',
       'Foundation and Material components fill in semantics automatically; low-level custom composables must declare their own. `Button`, `clickable` and `toggleable` merge their descendants. Accessibility services use the unmerged tree and merge it themselves; the testing framework uses the merged tree by default, with `useUnmergedTree` to switch. [[src:cp-semantics]]'),
      ('Accessibility không "chỉ đi qua Owner": trên Android, phần host nối semantics tree với hệ thống trợ năng, nhưng cây đó cũng được framework kiểm thử dùng. `Owner`, `AndroidComposeView` gắn nhãn [[badge:android-impl]].',
       'Accessibility does not "go only through the Owner": on Android, the host part connects the semantics tree to the accessibility system, but the same tree is used by the testing framework. `Owner` and `AndroidComposeView` are labelled [[badge:android-impl]].'),
      ('WCAG, thiết kế bao hàm và semantics trong Compose gặp nhau ở cầu nối X6 (chương E10).', 'WCAG, inclusive design and semantics in Compose meet in bridge X6 (chapter E10).')])],
   [(('Framework kiểm thử mặc định dùng cây nào?', 'Which tree does the testing framework use by default?'), ('Cây merged.', 'The merged tree.'),
     ('Có thể đổi sang cây unmerged bằng `useUnmergedTree = true`.', 'You can switch to the unmerged tree with `useUnmergedTree = true`.')),
    (('`AndroidComposeView` có phải API để ứng dụng gọi?', 'Is `AndroidComposeView` an API for apps to call?'), ('Không.', 'No.'),
     ('Đó là chi tiết cài đặt của Compose UI trên Android.', 'It is an implementation detail of Compose UI on Android.'))])

ch('b10', ('Live Runtime Explorer: luồng +1', 'Live Runtime Explorer: the +1 flow'),
   ('Bắt đầu với `count = 0`; bấm `+1` và đi qua tám bước từ handler tới các phase.\nMỗi bước cho thấy state trước và sau, thành phần đang xử lý, scope hoặc phase bị ảnh hưởng, thay đổi trên cây UI và phần bị skip.\nĐổi giá trị bắt đầu và tham số của `Header` để thấy bước 6 và 7 tính lại.',
    'Start with `count = 0`; tap `+1` and walk eight steps from the handler to the phases.\nEach step shows the state before and after, the component at work, the affected scope or phase, the UI tree change and what was skipped.\nChange the start value and the `Header` parameter to see steps 6 and 7 recomputed.'),
   ('Đã tới bước Recomposer', 'Reached the Recomposer step'), ('Đã đi hết tám bước', 'Walked all eight steps'),
   [('flow', ('Toàn bộ đường đi', 'The whole path'), 'simplified', [
      ('Sự kiện người dùng → ghi vào `MutableState` → Snapshot ghi nhận; các scope đã đọc state có thể bị invalidate → Recomposer điều phối → mã composable đã biến đổi chạy lại ở scope cần thiết → Composer đối chiếu, quyết định cập nhật hay skip → Applier áp dụng lên cây UI → Compose UI chạy các phase cần thiết → semantics tree phục vụ trợ năng và kiểm thử.',
       'User event → write to `MutableState` → Snapshot records it; scopes that read the state may be invalidated → the Recomposer coordinates → transformed composable code re-runs at the needed scope → the Composer compares and decides to update or skip → the Applier applies to the UI tree → Compose UI runs the needed phases → the semantics tree serves accessibility and testing.'),
      ('Tám bước là cách chia để giảng giải; runtime thật gộp và tối ưu khác đi. Điều khiển Reset, Trước, Tiếp, Phát, Tạm dừng và tốc độ ở dưới sơ đồ.', 'The eight steps are a teaching split; the real runtime batches and optimises differently. The Reset, Previous, Next, Play, Pause and speed controls are below the diagram.')])],
   [(('Ở bước 7, khi nào Applier chèn node mới?', 'In step 7, when does the Applier insert a new node?'), ('Khi cấu trúc đổi: count đi từ 0 lên 1 làm nhánh `if (count > 0)` xuất hiện.', 'When the structure changes: count going from 0 to 1 makes the `if (count > 0)` branch appear.'),
     ('Từ 5 lên 6 chỉ có cập nhật chữ.', 'From 5 to 6 there is only a text update.')),
    (('Vì sao `Header(title = "Counter")` được skip?', 'Why is `Header(title = "Counter")` skipped?'), ('Tham số stable và bằng lần trước.', 'Its parameter is stable and equal to last time.'),
     ('Xem quy tắc ở B8.', 'See the rule in B8.'))])

# ---------------- ghi file ----------------
def norm(s): return unicodedata.normalize('NFC', s)
# ---- caption sơ đồ ("Bạn đang xem") và nhãn chú giải, thêm 2026-11-21 ----
a('cap.map', 'Bản đồ 11 thành phần của Compose Runtime (khối isometric). Bấm một khối (hoặc chọn ở ô "Thành phần") để xem nó làm gì; khối được nhấn là thành phần đang nói tới.', 'A map of the 11 parts of the Compose Runtime (isometric blocks). Click a block (or pick it in the "Component" box) to see what it does; the highlighted block is the part being discussed.')
a('cap.setcontent', 'Từ trái sang phải: setContent tạo Composition, code đã qua compiler chạy trong Composer, kết quả ghi vào slot table và qua Applier thành cây UI, rồi tới các phase. Thẻ nhấn là bước đang chạy.', 'Left to right: setContent creates a Composition, compiled code runs in the Composer, the result is written to the slot table and through the Applier into the UI tree, then the phases run. The highlighted card is the step running now.')
a('cap.compiler', 'Hàm @Composable sau khi compiler biến đổi được Composer chạy và ghi vào slot table. Token cho biết dữ liệu vừa đi tới đâu.', 'The @Composable function, after the compiler transforms it, is run by the Composer and recorded in the slot table. The token shows where data just went.')
a('cap.snapshot', 'Một vòng đọc–ghi: Composer đọc state trong snapshot; khi state đổi, snapshot báo cho Recomposer, Recomposer lên lịch chạy lại phần Composition đã đọc state đó.', 'A read–write loop: the Composer reads state inside a snapshot; when the state changes, the snapshot notifies the Recomposer, which schedules the part of the Composition that read that state to run again.')
a('cap.recomposer', 'Từ trái sang phải: ghi state → Recomposer gom thay đổi tới frame kế tiếp → Composition chạy lại phần bị ảnh hưởng → Applier áp thay đổi lên cây UI.', 'Left to right: a state write → the Recomposer batches changes until the next frame → the Composition re-runs the affected part → the Applier applies the changes to the UI tree.')
a('cap.applier', 'Composer ghi kết quả vào slot table (trên) và gửi lệnh cho Applier (dưới); Applier chèn, gỡ, di chuyển hoặc cập nhật node trên cây UI.', 'The Composer records results in the slot table (top) and sends commands to the Applier (bottom); the Applier inserts, removes, moves or updates nodes in the UI tree.')
a('cap.counter', 'Một lần bấm nút đếm đi trọn một vòng: cây UI nhận click → ghi state trong snapshot → Recomposer → Composition → Composer → Applier → cây UI và các phase. Theo dõi thẻ được nhấn đi quanh vòng.', 'One tap on the counter goes round a full loop: the UI tree receives the click → state is written in a snapshot → Recomposer → Composition → Composer → Applier → UI tree and phases. Follow the highlighted card round the loop.')
a('cap.keys', 'Danh sách ở trên, các vị trí trong danh sách ở dưới. Trạng thái dưới mỗi thẻ cho biết phần tử được giữ, recompose, tạo mới hay rời Composition khi danh sách đổi.', 'The list on top, its positions below. The state on each card says whether the item is kept, recomposed, created or leaves the Composition when the list changes.')
a('cap.phases', 'Bên trái là state; bên phải là ba phase Composition, Layout, Drawing. Nơi state được ĐỌC quyết định phase nào phải chạy lại (thẻ nhấn).', 'State on the left; the three phases Composition, Layout and Drawing on the right. Where the state is READ decides which phase has to run again (highlighted card).')
a('cap.skip', 'Composable cha ở trên, con ở dưới. Trạng thái của con cho biết lần này nó được recompose hay được bỏ qua (skip).', 'The parent composable on top, the child below. The child state says whether it is recomposed or skipped this time.')
a('fam.idle', 'không chạy ở bước này', 'not running at this step')
a('fam.run', 'đang chạy / chạy lại', 'running / running again')
a('fam.done', 'xong / được giữ', 'done / kept')
a('cap.semantics', 'Cây UI sinh ra cây semantics; cây semantics phục vụ trình đọc màn hình và kiểm thử.', 'The UI tree produces the semantics tree; the semantics tree serves screen readers and tests.')

# ---------------- v2 (2026-11-22): module chương dài, cùng khuôn với dev/gen/coroutines_content.py ----------------
# Mỗi module: add(a) (a(k, vi, en=None)), tuỳ chọn override(o) (ghi đè chuỗi v1, giữ vị trí khoá) và SEC_ORDER = {chương: [mục…]}.
import sys
_here = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, _here)
def a2(k, vi, en=None): E.append((P + k, vi, vi if en is None else en))
def o2(k, vi, en=None):
    k = P + k
    for i, e in enumerate(E):
        if e[0] == k: E[i] = (k, vi, vi if en is None else en); return
    raise KeyError(k)
for mod in ('runtime_v2_dc', 'runtime_v2_b2', 'runtime_v2_b3', 'runtime_v2_b4', 'runtime_v2_sh', 'runtime_v2_b5', 'runtime_v2_ef', 'runtime_v2_cl', 'runtime_v2_b6', 'runtime_v2_b7'):   # thêm module mới vào đây
    if os.path.exists(os.path.join(_here, mod + '.py')):
        mm = __import__(mod)
        mm.add(a2)
        if hasattr(mm, 'override'): mm.override(o2)
        for chap, order in getattr(mm, 'SEC_ORDER', {}).items():
            pre = P + chap + '.sec.'
            idx = [i for i, e in enumerate(E) if e[0].startswith(pre)]
            items = [E[i] for i in idx]
            rank = lambda e: order.index(e[0][len(pre):].split('.')[0]) if e[0][len(pre):].split('.')[0] in order else len(order)
            items.sort(key=rank)
            first = idx[0]; sidx = set(idx)
            E[:] = [e for i, e in enumerate(E) if i not in sidx]
            E[first:first] = items

keys = [k for k, _, _ in E]
dup = [k for k in set(keys) if keys.count(k) > 1]
assert not dup, dup
for lang, idx in (('vi', 1), ('en', 2)):
    lines = ['/* Nội dung track Compose Runtime (%s). SINH TỰ ĐỘNG từ dev/gen/runtime_content.py: sửa ở đó rồi chạy lại. Cùng cây khoá với file ngôn ngữ còn lại. */' % ('tiếng Việt' if lang == 'vi' else 'tiếng Anh'),
             "ADE.addTrackStrings('runtime', '%s', {" % lang]
    body = ['  %s: %s' % (json.dumps(e[0]), json.dumps(norm(e[idx]), ensure_ascii=False)) for e in E]
    lines.append(',\n'.join(body)); lines.append('});\n')
    with open(os.path.join(ROOT, 'tracks', 'runtime', 'content.%s.js' % lang), 'w', encoding='utf-8', newline='\n') as f: f.write('\n'.join(lines))
print(len(E), 'keys')
