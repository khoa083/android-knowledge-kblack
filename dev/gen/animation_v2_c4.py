# Animation v2 · C4 AnimatedVisibility, AnimatedContent, Crossfade (viết lại; giữ mục v1 'vis' và sim animation.visibility)
# Nguồn: AnimatedVisibility.kt @296313a4 (KDoc); "Animation modifiers and composables" (an-composables); Kunneth Ch.8 (AnimatedVisibility, Crossfade);
# Essentials Ch.39 (enter/exit, animateEnterExit cho con, auto-start bằng MutableTransitionState, crossfade).

SEC_ORDER = {'c4': ['hook', 'vis', 'life', 'content', 'bugs', 'exercises', 'recall']}

def add(a):
    def B(ch, sec, n, field, vi, en=None):
        a('%s.sec.%s.b.%02d.%s' % (ch, sec, n, field), vi, vi if en is None else en)

    m = lambda k, vi, en=None: a('m.exitlife.' + k, vi, en)
    m('title', 'Khi nào nội dung rời composition?', 'When does content leave composition?')
    m('overview', 'Một banner trong `AnimatedVisibility` bị ẩn (`visible` thành false). Ba cách viết: chỉ hiệu ứng có sẵn; thêm một animation tùy biến trên `transition` của scope; và một `animateFloatAsState` đặt trong nội dung. Theo dõi nội dung còn trong composition tới lúc nào.', 'A banner inside `AnimatedVisibility` is hidden (`visible` becomes false). Three versions: built-in effects only; an extra custom animation on the scope\'s `transition`; and an `animateFloatAsState` placed in the content. Watch how long the content stays in composition.')
    m('wrapup', 'Ẩn không có nghĩa là gỡ ngay. Nội dung vẫn còn trong composition suốt hiệu ứng exit, và chỉ bị gỡ, dispose khi MỌI animation enter/exit thuộc Transition của nó xong, kể cả animation tuỳ biến tạo trên `transition` của scope.\nAnimation nằm ngoài Transition đó (như một `animate*AsState` trong nội dung) thì không ai chờ, nên có thể bị cắt ngang giữa chừng.\nQuy tắc dễ nhớ: muốn AnimatedVisibility chờ animation của bạn, hãy tạo nó trên `transition` của scope.',
      "Hiding does not mean removing at once. The content stays in composition throughout the exit effect, and is only removed and disposed when ALL enter/exit animations of its Transition are done, including custom ones created on the scope's `transition`.\nAnimations outside that Transition (such as an `animate*AsState` in the content) are not waited for, so they can be cut off mid-way.\nRule of thumb: to make AnimatedVisibility wait for your animation, create it on the scope's `transition`.")
    m('simp.1', 'Mốc 150/300/500 ms là minh họa; thời lượng thật của fadeOut/shrinkOut phụ thuộc spec (mặc định là spring).', 'The 150/300/500 ms marks are illustrative; the real duration of fadeOut/shrinkOut depends on the spec (a spring by default).')
    m('ctl.hint', 'Chạy cả ba và so thời điểm nội dung bị gỡ.', 'Run all three and compare when the content is removed.')
    m('ctl.which', 'Cách viết', 'Version')
    for k, vi, en in [('builtin', 'Chỉ hiệu ứng có sẵn', 'Built-in effects only'), ('custom', 'Thêm animation trên transition', 'Plus an animation on the transition'), ('outside', 'animateFloatAsState trong nội dung', 'animateFloatAsState in the content')]:
        m('ctl.which.' + k, vi, en)
    m('diagramTitle', 'Cờ visible, AnimatedVisibility, nội dung', 'The visible flag, AnimatedVisibility, the content')
    m('diagramDesc', 'Cờ visible điều khiển AnimatedVisibility; nó giữ nội dung trong composition và cuối cùng gỡ nội dung', 'The visible flag drives AnimatedVisibility; it keeps the content in composition and finally removes it')
    for k, vi, en in [('flag', 'Cờ visible', 'The visible flag'), ('av', 'AnimatedVisibility (Transition)', 'AnimatedVisibility (a Transition)'), ('content', 'Nội dung (banner)', 'Content (banner)'), ('gone', 'Đã gỡ và dispose', 'Removed and disposed')]:
        m('n.' + k, vi, en)
    for k, vi, en in [('ms', 'Thời gian (ms)', 'Time (ms)'), ('inComp', 'Còn trong composition (1/0)', 'Still in composition (1/0)')]:
        m('met.' + k, vi, en)
    for k, vi, en in [('visible', 'Giá trị visible', 'visible value'), ('inComp', 'Còn trong composition', 'Still in composition'), ('running', 'Đang chạy', 'Running')]:
        m('st.' + k, vi, en)
    S = [
        ('intro.builtin', 'Banner đang hiện', 'The banner is showing', 'Exit = fadeOut + shrinkOut (đúng mặc định).', 'Exit = fadeOut + shrinkOut (exactly the default).'),
        ('intro.custom', 'Banner có thêm màu nền animate', 'The banner also animates its background', 'Trong nội dung, `transition.animateColor(...)` dùng `transition` của `AnimatedVisibilityScope`, kéo dài 500 ms.', 'In the content, `transition.animateColor(...)` uses the `AnimatedVisibilityScope`\'s `transition` and lasts 500 ms.'),
        ('intro.outside', 'Banner có một animateFloatAsState', 'The banner has an animateFloatAsState', 'Trong nội dung, `animateFloatAsState(if (visible) 1f else 0.5f, tween(500))`: một animation riêng, không thuộc Transition của AnimatedVisibility.', 'In the content, `animateFloatAsState(if (visible) 1f else 0.5f, tween(500))`: a separate animation, not part of AnimatedVisibility\'s Transition.'),
        ('hide', 'visible = false: exit bắt đầu, nội dung VẪN ở đó', 'visible = false: exit starts, the content is STILL there', 'Nội dung không bị gỡ khi cờ đổi; nó còn được compose để hiệu ứng exit có cái mà làm mờ và thu nhỏ.', 'The content is not removed when the flag changes; it is still composed so the exit effect has something to fade and shrink.'),
        ('mid', '150 ms: đang mờ và thu nhỏ', '150 ms: fading and shrinking', 'Vẫn trong composition; các phần tử bên cạnh có thể dịch theo vì kích thước đang co.', 'Still in composition; neighbours may move because the size is shrinking.'),
        ('waitCustom', '300 ms: hiệu ứng có sẵn xong, vẫn chờ', '300 ms: built-in effects done, still waiting', 'Animation màu nền thuộc cùng Transition nên AnimatedVisibility chờ nó.', 'The background animation belongs to the same Transition, so AnimatedVisibility waits for it.'),
        ('removed', 'Mọi animation xong: nội dung bị gỡ', 'All animations done: the content is removed', 'Nội dung rời composition và bị dispose; `remember` bên trong mất.', 'The content leaves composition and is disposed; `remember` inside is lost.'),
        ('cut', '300 ms: nội dung bị gỡ, animateFloatAsState bị cắt', '300 ms: the content is removed, animateFloatAsState is cut off', 'Transition của AnimatedVisibility không biết animation riêng đó, nên khi exit có sẵn xong thì nội dung bị gỡ dù scale mới đi được nửa đường.', 'AnimatedVisibility\'s Transition does not know about that separate animation, so when the built-in exit finishes, the content is removed while the scale is only half-way.'),
        ('end.builtin', 'Kết thúc: gỡ ở 300 ms', 'The end: removed at 300 ms', 'Lâu bằng hiệu ứng exit.', 'As long as the exit effect.'),
        ('end.custom', 'Kết thúc: gỡ ở 500 ms', 'The end: removed at 500 ms', 'Lâu bằng animation dài nhất của Transition.', 'As long as the Transition\'s longest animation.'),
        ('end.outside', 'Kết thúc: animation bị cắt', 'The end: an animation cut off', 'Đưa animation đó vào `transition` của scope, hoặc dùng `Modifier.animateEnterExit`.', 'Move that animation onto the scope\'s `transition`, or use `Modifier.animateEnterExit`.'),
    ]
    for sid, tv, te, xv, xe in S:
        m('s.%s.title' % sid, tv, te); m('s.%s.explain' % sid, xv, xe); m('ev.' + sid, tv, te)
    for k, vi, en in [
        ('stillThere', 'KDoc: nội dung chỉ bị gỡ sau khi mọi animation exit (có sẵn và tùy biến) xong. [[src:an-av-src]]', 'The KDoc: content is only removed after all exit animations (built-in and custom) have finished. [[src:an-av-src]]'),
        ('waitAll', 'KDoc: AnimatedVisibility chờ MỌI animation enter/exit xong mới coi là idle. [[src:an-av-src]]', 'The KDoc: AnimatedVisibility waits until ALL enter/exit animations finish before it considers itself idle. [[src:an-av-src]]'),
        ('outside', 'Tài liệu: animation ngoài Transition (như animate*AsState) không được theo dõi, nên nội dung có thể bị gỡ trước khi chúng xong. [[src:an-composables]]', 'The docs: animations outside the Transition (such as animate*AsState) are not tracked, so content may be removed before they finish. [[src:an-composables]]'),
        ('end.builtin', 'Mặc định: fadeIn + expandIn khi vào, fadeOut + shrinkOut khi ra; trong Row/Column có mặc định riêng. [[src:an-av-src]]', 'Defaults: fadeIn + expandIn on enter, fadeOut + shrinkOut on exit; inside Row/Column there are tailored defaults. [[src:an-av-src]]'),
        ('end.custom', 'Animation tùy biến tạo trên `AnimatedVisibilityScope.transition` chạy cùng hiệu ứng có sẵn và được chờ. [[src:an-av-src]]', 'Custom animations created on `AnimatedVisibilityScope.transition` run alongside the built-in ones and are waited for. [[src:an-av-src]]'),
        ('end.outside', 'Muốn làm việc sau khi exit xong (xóa dữ liệu, animation tuần tự), KDoc gợi ý biến thể nhận `MutableTransitionState`. [[src:an-av-src]]', 'To act after the exit finishes (remove data, sequential animations), the KDoc suggests the variant taking a `MutableTransitionState`. [[src:an-av-src]]')]:
        m('co.' + k, vi, en)
    a('cap.exitlife', 'Cờ visible bên trái điều khiển AnimatedVisibility; bên phải trên là nội dung còn trong composition, bên phải dưới là lúc nội dung đã bị gỡ.', 'The visible flag on the left drives AnimatedVisibility; top right is the content still in composition, bottom right is when it has been removed.')

    C = 'c4'
    a(C + '.sim.animation.exitlife', 'Vòng đời nội dung khi ẩn', 'Content lifetime when hiding')
    a(C + '.sim.animation.visibility', 'Hiệu ứng enter/exit', 'Enter/exit effects')
    S = 'hook'
    a(C + '.sec.%s.title' % S, 'Đoán trước khi đọc', 'Predict before reading')
    a(C + '.sec.%s.badge' % S, 'stable')
    B(C, S, 1, 'predict', 'Banner trong `AnimatedVisibility` có một `LaunchedEffect` đếm giây. Khi `visible` thành false, bộ đếm dừng NGAY hay chạy tiếp tới khi hiệu ứng mờ dần xong?', 'A banner inside `AnimatedVisibility` has a `LaunchedEffect` counting seconds. When `visible` becomes false, does the counter stop AT ONCE, or keep running until the fade-out is done?')
    B(C, S, 1, 'ans', 'Chạy tiếp tới khi exit xong. Nội dung còn trong composition suốt hiệu ứng exit; chỉ khi mọi animation exit xong nó mới bị gỡ và dispose, lúc đó `LaunchedEffect` bị hủy (chương EF của Runtime). [[src:an-av-src]]', 'It keeps running until the exit finishes. The content stays in composition throughout the exit effect; only when every exit animation is done is it removed and disposed, and only then is the `LaunchedEffect` cancelled (Runtime chapter EF). [[src:an-av-src]]')

    S = 'life'
    a(C + '.sec.%s.title' % S, 'Ẩn không phải là gỡ ngay', 'Hiding is not removing at once')
    a(C + '.sec.%s.badge' % S, 'impl')
    B(C, S, 1, 'p', '`AnimatedVisibility(visible, enter, exit)` có ba loại hiệu ứng: fade, slide, expand/shrink (cộng scale), kết hợp bằng dấu `+` [[src:book-kunneth]] [[src:book-compose-ess]].\nKDoc ở commit ghim thêm những điều quan trọng:\n• Các hiệu ứng kết hợp chạy CÙNG LÚC, nên thứ tự quanh dấu `+` không quan trọng.\n• AnimatedVisibility chờ MỌI animation enter/exit, kể cả animation tuỳ biến tạo trên `transition` của `AnimatedVisibilityScope`.\n• Nội dung chỉ bị gỡ và dispose sau khi exit xong.\n• Nó dựng một `Layout` riêng, lấy kích thước lớn nhất trong các con.\nMô phỏng ngay dưới cho thấy hệ quả với một animation đặt NGOÀI Transition [[src:an-av-src]].',
      "`AnimatedVisibility(visible, enter, exit)` has three kinds of effect: fade, slide, expand/shrink (plus scale), combined with `+` [[src:book-kunneth]] [[src:book-compose-ess]].\nThe KDoc at the pinned commit adds the important parts:\n• Combined effects run AT THE SAME TIME, so the order around `+` does not matter.\n• AnimatedVisibility waits for ALL enter/exit animations, including custom ones created on the `AnimatedVisibilityScope`'s `transition`.\n• The content is only removed and disposed after the exit finishes.\n• It builds its own `Layout`, taking the largest size among its children.\nThe simulation just below shows the consequence for an animation placed OUTSIDE the Transition [[src:an-av-src]].")
    B(C, S, 2, 'p', 'Thêm hai kỹ thuật hữu ích:\n• `Modifier.animateEnterExit(enter, exit)` cho từng con một hiệu ứng riêng bên trong cùng một AnimatedVisibility.\n• "Tự chạy": truyền `MutableTransitionState(false).apply { targetState = true }`, để hiệu ứng enter chạy ngay khi nội dung xuất hiện (cùng ý với C3) [[src:book-compose-ess]] [[src:an-av-src]].\nQuy tắc dễ nhớ: hiệu ứng chung cho cả khối thì đặt ở AnimatedVisibility; hiệu ứng riêng cho từng con thì `animateEnterExit`.',
      'Two more useful techniques:\n• `Modifier.animateEnterExit(enter, exit)` gives each child its own effect inside the same AnimatedVisibility.\n• "Auto-start": pass `MutableTransitionState(false).apply { targetState = true }`, so the enter effect runs as soon as the content appears (the same idea as C3) [[src:book-compose-ess]] [[src:an-av-src]].\nRule of thumb: an effect for the whole block goes on AnimatedVisibility; an effect for one child uses `animateEnterExit`.')

    S = 'content'
    a(C + '.sec.%s.title' % S, 'AnimatedContent và Crossfade', 'AnimatedContent and Crossfade')
    a(C + '.sec.%s.badge' % S, 'stable')
    B(C, S, 1, 'p', 'Khi đổi giữa hai nội dung (chứ không phải hiện hay ẩn một nội dung), dùng `AnimatedContent(targetState) { state -> … }` hoặc `Crossfade`, ví dụ để đổi giữa hai bố cục [[src:book-kunneth]].\nTrong lúc chuyển, cả nội dung cũ lẫn nội dung mới cùng được compose. Vì vậy bên trong lambda phải dùng THAM SỐ của lambda (state của nội dung đó), đừng dùng biến state bên ngoài. Đọc biến bên ngoài thì nội dung đang rời đi cũng hiện ra giá trị mới [[src:an-composables]].\nQuy tắc dễ nhớ: trong `AnimatedContent`, luôn dùng tham số `state ->`, không dùng biến của bên ngoài.',
      "When switching between two contents (rather than showing or hiding one), use `AnimatedContent(targetState) { state -> … }` or `Crossfade`, for example to switch between two layouts [[src:book-kunneth]].\nDuring the switch, both the old and the new content are composed. So inside the lambda you must use the lambda's PARAMETER (that content's own state), not the outer state variable. If you read the outer variable, the leaving content shows the new value too [[src:an-composables]].\nRule of thumb: inside `AnimatedContent`, always use the `state ->` parameter, never the outer variable.")
    B(C, S, 2, 'kt', 'AnimatedContent(targetState = count, label = "count") { target ->\n    Text("Count: $target")          // ✓ tham số của lambda\n    // Text("Count: $count")        // ✗ nội dung đang rời đi cũng nhảy sang số mới\n}', 'AnimatedContent(targetState = count, label = "count") { target ->\n    Text("Count: $target")          // ✓ the lambda parameter\n    // Text("Count: $count")        // ✗ the leaving content would jump to the new number too\n}')

    S = 'bugs'
    a(C + '.sec.%s.title' % S, 'Bug thường gặp', 'Common bugs')
    a(C + '.sec.%s.badge' % S, 'stable')
    B(C, S, 1, 'bug', 'Hiệu ứng thu nhỏ của banner bị "cụt": banner biến mất khi mới thu được nửa.', 'A banner\'s shrink effect is "cut short": the banner disappears when only half-shrunk.')
    B(C, S, 1, 'cause', 'Hiệu ứng thu nhỏ viết bằng `animateFloatAsState` trong nội dung, ngoài Transition của AnimatedVisibility, nên không ai chờ nó.', 'The shrink is written with `animateFloatAsState` in the content, outside AnimatedVisibility\'s Transition, so nobody waits for it.')
    B(C, S, 1, 'fix', 'Dùng `scaleOut()` trong `exit`, hoặc `Modifier.animateEnterExit`, hoặc `transition.animateFloat` trên scope. [[src:an-composables]] [[src:an-av-src]]', 'Use `scaleOut()` in `exit`, or `Modifier.animateEnterExit`, or `transition.animateFloat` on the scope. [[src:an-composables]] [[src:an-av-src]]')
    B(C, S, 2, 'bug', 'Trong `AnimatedContent`, số cũ đang trượt ra cũng hiện số mới.', 'In `AnimatedContent`, the old number sliding out also shows the new number.')
    B(C, S, 2, 'cause', 'Lambda đọc biến `count` bên ngoài thay vì tham số `target`.', 'The lambda reads the outer `count` variable instead of the `target` parameter.')
    B(C, S, 2, 'fix', 'Dùng tham số của lambda. [[src:an-composables]]', 'Use the lambda parameter. [[src:an-composables]]')

    S = 'exercises'
    a(C + '.sec.%s.title' % S, 'Bài tập', 'Exercises')
    a(C + '.sec.%s.badge' % S, 'stable')
    B(C, S, 1, 'ex', 'Xóa một mục khỏi dữ liệu CHỈ sau khi hiệu ứng exit của nó xong.', 'Remove an item from the data ONLY after its exit effect is done.')
    B(C, S, 1, 'hint', 'KDoc gợi ý biến thể nhận MutableTransitionState; kiểm `isIdle` và `currentState`.', 'The KDoc suggests the MutableTransitionState variant; check `isIdle` and `currentState`.')
    B(C, S, 1, 'solkt', 'val state = remember { MutableTransitionState(true) }\nAnimatedVisibility(visibleState = state) { ItemRow(item) }\nButton(onClick = { state.targetState = false }) { Text("Delete") }\nif (state.isIdle && !state.currentState) {\n    LaunchedEffect(item.id) { onRemove(item) }    // exit đã xong\n}', 'val state = remember { MutableTransitionState(true) }\nAnimatedVisibility(visibleState = state) { ItemRow(item) }\nButton(onClick = { state.targetState = false }) { Text("Delete") }\nif (state.isIdle && !state.currentState) {\n    LaunchedEffect(item.id) { onRemove(item) }    // the exit has finished\n}')
    B(C, S, 1, 'sol', '`isIdle` đúng khi không còn chạy; `currentState == false` nghĩa là đã ẩn xong (không phải chỉ mới có ý định ẩn).', '`isIdle` is true when nothing is running; `currentState == false` means hiding has finished (not just been requested).')

    S = 'recall'
    a(C + '.sec.%s.title' % S, 'Tự trả lời', 'Answer it yourself')
    a(C + '.sec.%s.badge' % S, 'stable')
    B(C, S, 1, 'ask', 'Khi visible thành false, nội dung bị gỡ lúc nào?', 'When visible becomes false, when is the content removed?')
    B(C, S, 1, 'ans', 'Sau khi mọi animation enter/exit của Transition (có sẵn và tùy biến) xong.', 'After all of the Transition\'s enter/exit animations (built-in and custom) finish.')
    for q, qv, qe, av, ae, wv, we in [
        ('q3', 'fadeIn() + slideInVertically() chạy lần lượt hay cùng lúc?', 'Do fadeIn() + slideInVertically() run one after another or together?',
         'Cùng lúc.', 'Together.', 'KDoc: thứ tự kết hợp không quan trọng, chúng bắt đầu đồng thời.', 'The KDoc: the order does not matter; they start simultaneously.')]:
        a(C + '.quiz.%s.q' % q, qv, qe); a(C + '.quiz.%s.a' % q, av, ae); a(C + '.quiz.%s.why' % q, wv, we)

def override(o):
    C = 'c4'
    o(C + '.goal.g1', 'Đã thấy visible đổi và nội dung vẫn còn', 'Saw visible change while the content stayed')
    o(C + '.goal.g2', 'Đã chạy một cách viết tới cuối', 'Ran one version to the end')
