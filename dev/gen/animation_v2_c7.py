# Animation v2 · C7 Frame clock và phase (viết lại; giữ mục v1 'defer' và sim animation.phaseread)
# Nguồn: Recomposer.kt @296313a4 (frame: gửi frame cho awaiter trước, rồi sendApplyNotifications, recompose, apply; đã ghi ở Runtime B5);
# AndroidUiFrameClock.android.kt (Choreographer.postFrameCallback); WindowRecomposer.android.kt (MotionDurationScaleImpl đọc
# Settings.Global.ANIMATOR_DURATION_SCALE); SuspendAnimation.kt @296313a4 (durationScale 0 → playTime = durationNanos); quick-guide; phases docs.

SEC_ORDER = {'c7': ['hook', 'frame', 'defer', 'scale', 'bugs', 'exercises', 'recall']}

def add(a):
    def B(ch, sec, n, field, vi, en=None):
        a('%s.sec.%s.b.%02d.%s' % (ch, sec, n, field), vi, vi if en is None else en)

    m = lambda k, vi, en=None: a('m.frameorder.' + k, vi, en)
    m('title', 'Bên trong MỘT frame: animation tính trước, rồi mới tới recompose, layout, draw', 'Inside ONE frame: animations compute first, then recompose, layout, draw')
    m('overview', 'Một `animateFloatAsState` đang chạy. Ba trường hợp trong cùng một frame: giá trị được đọc trong thân composable; được đọc trong `graphicsLayer { }`; và tỉ lệ thời lượng animator của máy là 0. Theo dõi thứ tự các bước và bước nào bị bỏ qua.', 'An `animateFloatAsState` is running. Three cases within one frame: the value is read in the composable body; it is read in `graphicsLayer { }`; and the device\'s animator duration scale is 0. Watch the order of the steps and which ones are skipped.')
    m('wrapup', 'Mỗi frame, Recomposer đánh thức các coroutine đang chờ frame (animation) TRƯỚC, để chúng ghi giá trị mới vào state; rồi gửi thông báo thay đổi, recompose những scope bị ảnh hưởng và áp thay đổi; sau đó cây UI đo, đặt và vẽ. Nơi đọc giá trị quyết định bước nào phải chạy. Tỉ lệ thời lượng của máy (cài đặt animator duration scale) kéo dài hoặc rút ngắn animation; bằng 0 thì animation hữu hạn nhảy tới cuối ngay frame đầu.', 'Each frame, the Recomposer wakes the coroutines waiting for a frame (animations) FIRST, so they write their new values into state; then it sends change notifications, recomposes the affected scopes and applies changes; after that the UI tree measures, places and draws. Where the value is read decides which steps must run. The device\'s duration scale (the animator duration scale setting) stretches or shortens animations; at 0, a finite animation jumps to its end on the first frame.')
    m('simp.1', 'Mô hình gộp các bước của Recomposer và của hệ View vào một danh sách; nó đặt đo/đặt/vẽ ngay sau trong cùng frame như một giản lược.', 'The model folds the Recomposer\'s and the View system\'s steps into one list; placing measure/place/draw right after in the same frame is a simplification.')
    m('simp.2', 'Giá trị 0,4 → 0,5 là minh họa cho một frame giữa chừng.', 'The 0.4 → 0.5 values are illustrative of a mid-way frame.')
    m('ctl.hint', 'So "đọc trong thân" với "đọc trong graphicsLayer", rồi thử tỉ lệ 0.', 'Compare "read in body" with "read in graphicsLayer", then try scale 0.')
    m('ctl.which', 'Trường hợp', 'Case')
    for k, vi, en in [('body', 'Đọc trong thân composable', 'Read in the composable body'), ('layer', 'Đọc trong graphicsLayer { }', 'Read in graphicsLayer { }'), ('scale0', 'Tỉ lệ thời lượng = 0', 'Duration scale = 0')]:
        m('ctl.which.' + k, vi, en)
    m('diagramTitle', 'Choreographer, Recomposer, animation, cây UI', 'Choreographer, Recomposer, animation, the UI tree')
    m('diagramDesc', 'Choreographer báo frame; Recomposer gửi frame cho animation trước, rồi recompose; lớp vẽ cập nhật', 'Choreographer signals the frame; the Recomposer sends it to animations first, then recomposes; the layer updates')
    for k, vi, en in [('anim', 'Animation đang chờ frame', 'Animation awaiting a frame'), ('ui', 'Cây UI: lớp vẽ', 'UI tree: the layer')]:
        m('n.' + k, vi, en)
    m('n.vsync', 'Choreographer (nhịp vsync)', 'Choreographer (vsync)')
    m('n.recomposer', 'Bộ Recomposer', 'Recomposer')
    for k, vi, en in [('recomp', 'Lượt recompose', 'Recompositions'), ('draw', 'Lượt vẽ', 'Draws'), ('val', 'Giá trị ×100', 'Value ×100')]:
        m('met.' + k, vi, en)
    for k, vi, en in [('val', 'Giá trị animation', 'Animation value'), ('running', 'Animation còn chạy', 'Animation still running'), ('read', 'Đọc ở', 'Read in')]:
        m('st.' + k, vi, en)
    S = [
        ('intro.body', 'Giá trị đọc trong thân composable', 'The value is read in the composable body', '`val a by animateFloatAsState(target)` rồi `Box(Modifier.alpha(a))`: `a` được đọc khi composable chạy.', '`val a by animateFloatAsState(target)` then `Box(Modifier.alpha(a))`: `a` is read when the composable runs.'),
        ('intro.layer', 'Giá trị đọc trong graphicsLayer', 'The value is read in graphicsLayer', '`Box(Modifier.graphicsLayer { alpha = a })`: `a` chỉ được đọc khi lớp vẽ được cập nhật.', '`Box(Modifier.graphicsLayer { alpha = a })`: `a` is only read when the layer is updated.'),
        ('intro.scale0', 'Tỉ lệ thời lượng của máy = 0', 'The device duration scale = 0', 'Cài đặt animator duration scale bằng 0. Compose đọc nó thành `MotionDurationScale` trong coroutine context của Recomposer.', 'The animator duration scale setting is 0. Compose reads it as a `MotionDurationScale` in the Recomposer\'s coroutine context.'),
        ('vsync', 'Vsync: Choreographer gọi frame callback', 'Vsync: Choreographer calls the frame callback', 'Đồng hồ frame của Android (`AndroidUiFrameClock`) xin frame bằng `Choreographer.postFrameCallback`; Recomposer đang treo trong `withFrameNanos` được đánh thức.', 'Android\'s frame clock (`AndroidUiFrameClock`) requests frames with `Choreographer.postFrameCallback`; the Recomposer suspended in `withFrameNanos` is woken.'),
        ('awaiters', 'Bước 1: gửi frame cho animation, giá trị {v}', 'Step 1: send the frame to animations, value {v}', 'Recomposer gửi thời điểm frame cho các coroutine đang chờ (`withFrameNanos` bên trong animation) TRƯỚC khi recompose. Animation tính giá trị mới từ thời gian chơi và ghi vào state.', 'The Recomposer sends the frame time to the waiting coroutines (`withFrameNanos` inside the animation) BEFORE recomposing. The animation computes its new value from the play time and writes it to state.'),
        ('awaiters0', 'Bước 1: tỉ lệ 0, nhảy tới cuối = {v}', 'Step 1: scale 0, jump to the end = {v}', 'Mã ở commit ghim: khi `durationScale == 0f`, thời gian chơi = toàn bộ thời lượng, nên frame đầu tiên đã là frame cuối; animation kết thúc ngay.', 'Code at the pinned commit: when `durationScale == 0f`, play time = the whole duration, so the first frame is already the last; the animation ends at once.'),
        ('notify', 'Bước 2: gửi thông báo thay đổi', 'Step 2: send change notifications', 'Ghi state được báo đi (`sendApplyNotifications`): ai đã đọc state đó được đánh dấu cần chạy lại.', 'The state write is announced (`sendApplyNotifications`): whoever read that state is marked to run again.'),
        ('recompose', 'Bước 3: recompose scope đọc giá trị', 'Step 3: recompose the scope that read the value', 'Composable đã đọc `a` trong thân chạy lại, dựng lại modifier với alpha mới; thay đổi được ghi nhận rồi áp. Đổi alpha không đổi kích thước nên không cần đo lại.', 'The composable that read `a` in its body runs again, rebuilding the modifier with the new alpha; changes are recorded and then applied. Changing alpha does not change size, so no re-measure is needed.'),
        ('norecompose', 'Bước 3: không có scope nào cần recompose', 'Step 3: no scope needs recomposing', 'Không composable nào đọc `a` trong thân, nên không có recomposition; chỉ lớp vẽ đọc nó bị đánh dấu.', 'No composable read `a` in its body, so there is no recomposition; only the layer that reads it is marked.'),
        ('draw', 'Vẽ', 'Draw', 'Lớp vẽ đọc giá trị mới và vẽ lại.', 'The layer reads the new value and redraws.'),
        ('done.body', 'Frame xong: 1 recompose, 1 lượt vẽ', 'Frame done: 1 recomposition, 1 draw', 'Lặp lại mỗi frame tới khi animation xong.', 'This repeats every frame until the animation ends.'),
        ('done.layer', 'Frame xong: 0 recompose, chỉ vẽ', 'Frame done: 0 recompositions, draw only', 'Cùng animation, ít việc hơn mỗi frame.', 'The same animation, less work per frame.'),
        ('done.scale0', 'Xong trong một frame', 'Done in one frame', 'Người dùng đã tắt animation thì thấy trạng thái cuối ngay. Animation vô hạn có cách xử lý riêng (chương IF).', 'Users who turned animations off see the end state at once. Infinite animations have their own handling (chapter IF).'),
    ]
    for sid, tv, te, xv, xe in S:
        m('s.%s.title' % sid, tv, te); m('s.%s.explain' % sid, xv, xe); m('ev.' + sid, tv, te)
    for k, vi, en in [
        ('order', 'Mã Recomposer ở commit ghim (đã đọc ở chương B5 của Runtime): trong frame, gửi frame cho awaiter trước, rồi sendApplyNotifications, rồi recompose và apply. [[src:rt-recomposer-src]]', 'Recomposer code at the pinned commit (read in Runtime chapter B5): within a frame, send the frame to awaiters first, then sendApplyNotifications, then recompose and apply. [[src:rt-recomposer-src]]'),
        ('choreo', 'AndroidUiFrameClock dùng Choreographer.postFrameCallback. [[src:ui-frameclock]]', 'AndroidUiFrameClock uses Choreographer.postFrameCallback. [[src:ui-frameclock]]'),
        ('defer', 'Cầu nối X1: đọc trong graphicsLayer { } thì không recompose (chương B7, mục "Hoãn việc đọc" bên dưới). [[src:cp-phases]]', 'Bridge X1: reading in graphicsLayer { } does not recompose (chapter B7, the "Deferring the read" section below). [[src:cp-phases]]'),
        ('scale', 'MotionDurationScaleImpl đọc Settings.Global.ANIMATOR_DURATION_SCALE và theo dõi thay đổi; durationScale 0 → playTime = durationNanos. [[src:ui-windowrecomposer]] [[src:an-suspend-src]]', 'MotionDurationScaleImpl reads Settings.Global.ANIMATOR_DURATION_SCALE and observes changes; durationScale 0 → playTime = durationNanos. [[src:ui-windowrecomposer]] [[src:an-suspend-src]]')]:
        m('co.' + k, vi, en)
    a('cap.frameorder', 'Từ trái sang phải: Choreographer báo vsync, Recomposer gửi frame cho animation đang chờ, rồi lớp vẽ của cây UI cập nhật.', 'Left to right: Choreographer signals vsync, the Recomposer sends the frame to the waiting animation, then the UI tree\'s layer updates.')

    C = 'c7'
    a(C + '.sim.animation.frameorder', 'Thứ tự trong một frame', 'Order within a frame')
    a(C + '.sim.animation.phaseread', 'Ba nơi đọc', 'Three read sites')

    S = 'hook'
    a(C + '.sec.%s.title' % S, 'Đoán trước khi đọc', 'Predict before reading')
    a(C + '.sec.%s.badge' % S, 'stable')
    B(C, S, 1, 'predict', 'Trong một frame, cái nào chạy trước: animation tính giá trị mới, hay recompose những composable đọc giá trị đó? Nếu ngược lại thì sao?', 'Within one frame, which runs first: the animation computing its new value, or recomposing the composables that read it? What if it were the other way round?')
    B(C, S, 1, 'ans', 'Animation trước. Recomposer gửi frame cho các coroutine đang chờ frame trước, rồi mới gửi thông báo thay đổi và recompose. Nếu ngược lại, recomposition sẽ dùng giá trị của frame TRƯỚC và màn hình luôn trễ một frame. [[src:rt-recomposer-src]]', 'The animation. The Recomposer sends the frame to the coroutines waiting for it first, and only then sends change notifications and recomposes. Otherwise, recomposition would use the PREVIOUS frame\'s value and the screen would always lag one frame. [[src:rt-recomposer-src]]')

    S = 'frame'
    a(C + '.sec.%s.title' % S, 'Một frame từ Choreographer tới màn hình', 'One frame from Choreographer to the screen')
    a(C + '.sec.%s.badge' % S, 'impl')
    B(C, S, 1, 'p', 'Mọi animation của Compose cuối cùng đều chờ frame bằng `withFrameNanos` (hoặc biến thể vô hạn, chương IF) trên `MonotonicFrameClock` trong coroutine context. Trên Android, đồng hồ đó là `AndroidUiFrameClock`, xin frame bằng `Choreographer.postFrameCallback` (chương B5 của Runtime). Animation chạy trong coroutine của composition (`LaunchedEffect` bên trong `animate*AsState`, chương C1), nên frame đến từ Recomposer. [[src:ui-frameclock]] [[src:rt-recomposer-src]]', 'Every Compose animation ultimately waits for frames with `withFrameNanos` (or the infinite variant, chapter IF) on the `MonotonicFrameClock` in its coroutine context. On Android, that clock is `AndroidUiFrameClock`, which requests frames with `Choreographer.postFrameCallback` (Runtime chapter B5). Animations run in the composition\'s coroutines (the `LaunchedEffect` inside `animate*AsState`, chapter C1), so their frames come from the Recomposer. [[src:ui-frameclock]] [[src:rt-recomposer-src]]')
    B(C, S, 2, 'p', 'Thứ tự trong một frame, theo mã Recomposer ở commit ghim: (1) gửi thời điểm frame cho các awaiter, tức animation tính giá trị mới và ghi vào state; (2) `sendApplyNotifications`, báo ai đã đọc state đó; (3) recompose các scope bị vô hiệu; (4) áp thay đổi lên cây. Sau đó cây UI đo, đặt và vẽ phần bị ảnh hưởng. Vì animation đi TRƯỚC, recomposition trong cùng frame đã thấy giá trị mới. Mô phỏng ngay dưới chạy thứ tự đó với ba trường hợp. [[src:rt-recomposer-src]]', 'The order within a frame, per the Recomposer code at the pinned commit: (1) send the frame time to the awaiters, i.e. animations compute new values and write them to state; (2) `sendApplyNotifications`, announcing who read that state; (3) recompose the invalidated scopes; (4) apply changes to the tree. Then the UI tree measures, places and draws the affected part. Because animations go FIRST, recomposition in the same frame already sees the new value. The simulation just below runs that order in three cases. [[src:rt-recomposer-src]]')
    B(C, S, 3, 'note', 'Đây cũng là lý do tài liệu nói `withFrameNanos` là API mức thấp: bạn hiếm khi gọi nó trực tiếp; API mức cao (animate*AsState, Transition, Animatable) đã lo việc chờ frame và tính giá trị. Ghi chú này giữ cầu nối X3 với chương B5 của Runtime. [[src:an-quick]]', 'This is also why the docs call `withFrameNanos` a low-level API: you rarely call it directly; the high-level APIs (animate*AsState, Transition, Animatable) already handle waiting for frames and computing values. This note keeps bridge X3 to Runtime chapter B5. [[src:an-quick]]')
    B(C, S, 3, 'kind', 'mechanism')

    S = 'scale'
    a(C + '.sec.%s.title' % S, 'Tỉ lệ thời lượng của máy', 'The device duration scale')
    a(C + '.sec.%s.badge' % S, 'impl')
    B(C, S, 1, 'p', 'Ở commit ghim, khi tạo Recomposer cho cửa sổ, `WindowRecomposer` thêm một `MotionDurationScale` vào coroutine context (trừ khi đã có); bản Android đọc `Settings.Global.ANIMATOR_DURATION_SCALE` và theo dõi thay đổi qua ContentObserver. Mọi animation hữu hạn chia thời gian đã trôi cho tỉ lệ này: tỉ lệ 2 làm animation chậm gấp đôi; tỉ lệ 0 làm thời gian chơi bằng ngay toàn bộ thời lượng, nên animation tới cuối ở frame đầu tiên. Animation vô hạn có nhánh riêng (nhảy tới đích rồi chờ, chương IF). [[src:ui-windowrecomposer]] [[src:an-suspend-src]] [[src:an-inftrans-src]]', 'At the pinned commit, when creating a window\'s Recomposer, `WindowRecomposer` adds a `MotionDurationScale` to the coroutine context (unless one is already there); the Android version reads `Settings.Global.ANIMATOR_DURATION_SCALE` and observes changes through a ContentObserver. Every finite animation divides elapsed time by this scale: a scale of 2 makes animations twice as slow; a scale of 0 makes play time equal the whole duration at once, so the animation reaches its end on the first frame. Infinite animations have their own branch (snap to the target and wait, chapter IF). [[src:ui-windowrecomposer]] [[src:an-suspend-src]] [[src:an-inftrans-src]]')
    B(C, S, 2, 'p', 'Hệ quả thiết kế: đừng dùng việc animation "kết thúc" để mang thông tin quan trọng mà người dùng chỉ thấy được nếu animation chạy đủ lâu; với tỉ lệ 0, mọi trạng thái trung gian biến mất. Chương C8 bàn tiếp về giảm chuyển động và kiểm thử. [[src:an-suspend-src]]', 'A design consequence: do not rely on an animation\'s "ending" to carry important information that users only see if the animation runs long enough; at scale 0, every intermediate state disappears. Chapter C8 continues with reduced motion and testing. [[src:an-suspend-src]]')

    S = 'bugs'
    a(C + '.sec.%s.title' % S, 'Bug thường gặp', 'Common bugs')
    a(C + '.sec.%s.badge' % S, 'stable')
    B(C, S, 1, 'bug', 'Một hướng dẫn "vuốt để xem" dựa vào animation chạy 2 giây; trên máy của người kiểm thử, hướng dẫn hiện xong ngay và không ai thấy cử chỉ mẫu.', 'A "swipe to see more" hint relies on a 2-second animation; on the tester\'s device, the hint finishes instantly and nobody sees the example gesture.')
    B(C, S, 1, 'cause', 'Tỉ lệ thời lượng animator của máy là 0: animation hữu hạn tới cuối ở frame đầu.', 'The device\'s animator duration scale is 0: finite animations reach their end on the first frame.')
    B(C, S, 1, 'fix', 'Truyền thông tin bằng nội dung tĩnh (chữ, icon) và coi animation là phần bổ sung. [[src:an-suspend-src]] [[src:ui-windowrecomposer]]', 'Convey the information with static content (text, icons) and treat the animation as an extra. [[src:an-suspend-src]] [[src:ui-windowrecomposer]]')
    B(C, S, 2, 'bug', 'Tự viết `LaunchedEffect { while (true) { withFrameNanos { t -> x = f(t) } } }` cho một animation đơn giản; nó không dừng khi xong và bỏ qua tỉ lệ thời lượng.', 'Hand-writing `LaunchedEffect { while (true) { withFrameNanos { t -> x = f(t) } } }` for a simple animation; it does not stop when done and ignores the duration scale.')
    B(C, S, 2, 'cause', 'withFrameNanos chỉ cho thời điểm frame; việc kết thúc, ngắt, vận tốc, tỉ lệ thời lượng là việc của API mức cao.', 'withFrameNanos only gives the frame time; finishing, interruption, velocity and duration scale are the high-level APIs\' job.')
    B(C, S, 2, 'fix', 'Dùng animate*AsState, Animatable hoặc Transition. [[src:an-quick]]', 'Use animate*AsState, Animatable or Transition. [[src:an-quick]]')

    S = 'exercises'
    a(C + '.sec.%s.title' % S, 'Bài tập', 'Exercises')
    a(C + '.sec.%s.badge' % S, 'stable')
    B(C, S, 1, 'ex', 'Một màn hình có 50 ô, mỗi ô nhấp nháy alpha bằng `animateFloatAsState` đọc trong `Modifier.alpha(a)`. Sửa để mỗi frame không recompose 50 ô.', 'A screen has 50 cells, each blinking its alpha with `animateFloatAsState` read in `Modifier.alpha(a)`. Fix it so each frame does not recompose 50 cells.')
    B(C, S, 1, 'hint', 'Giữ animation, đổi nơi đọc.', 'Keep the animation, change where it is read.')
    B(C, S, 1, 'sol', 'Dùng `Modifier.graphicsLayer { alpha = a }`: giá trị chỉ được đọc ở bước cập nhật lớp vẽ, nên mỗi frame không ô nào recompose; vẫn nên đo để xác nhận (chương PF của Runtime).', 'Use `Modifier.graphicsLayer { alpha = a }`: the value is only read when the layer updates, so no cell recomposes per frame; still measure to confirm (Runtime chapter PF).')

    S = 'recall'
    a(C + '.sec.%s.title' % S, 'Tự trả lời', 'Answer it yourself')
    a(C + '.sec.%s.badge' % S, 'stable')
    B(C, S, 1, 'ask', 'Trong một frame, Recomposer làm gì trước khi recompose?', 'Within a frame, what does the Recomposer do before recomposing?')
    B(C, S, 1, 'ans', 'Gửi frame cho các coroutine đang chờ (animation), rồi sendApplyNotifications.', 'Sends the frame to the waiting coroutines (animations), then sendApplyNotifications.')
    B(C, S, 2, 'ask', 'Tỉ lệ thời lượng 0 làm gì với animation hữu hạn?', 'What does a duration scale of 0 do to a finite animation?')
    B(C, S, 2, 'ans', 'Thời gian chơi bằng toàn bộ thời lượng ngay frame đầu: nhảy tới cuối.', 'Play time equals the whole duration on the first frame: it jumps to the end.')
    for q, qv, qe, av, ae, wv, we in [
        ('q3', 'Tỉ lệ thời lượng của Compose đến từ đâu trên Android?', 'Where does Compose\'s duration scale come from on Android?', 'Cài đặt ANIMATOR_DURATION_SCALE.', 'The ANIMATOR_DURATION_SCALE setting.', 'WindowRecomposer gắn MotionDurationScale đọc cài đặt đó và theo dõi thay đổi.', 'WindowRecomposer attaches a MotionDurationScale that reads that setting and observes changes.'),
        ('q4', 'Animation chạy trước hay sau recomposition trong cùng frame?', 'Does the animation run before or after recomposition in the same frame?', 'Trước.', 'Before.', 'Recomposer gửi frame cho awaiter trước.', 'The Recomposer sends the frame to awaiters first.')]:
        a(C + '.quiz.%s.q' % q, qv, qe); a(C + '.quiz.%s.a' % q, av, ae); a(C + '.quiz.%s.why' % q, wv, we)

def override(o):
    C = 'c7'
    o(C + '.goal.g1', 'Đã thấy vsync tới', 'Saw the vsync arrive')
    o(C + '.goal.g2', 'Đã chạy một trường hợp tới cuối', 'Ran one case to the end')
