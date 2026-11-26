# Animation v2 · C3 updateTransition (viết lại; giữ mục v1 't' và sim animation.transition)
# Nguồn: Transition.kt @296313a4 (KDoc updateTransition, rememberTransition(MutableTransitionState), Transition, currentState, animateFloat);
# Kunneth Ch.8 (MultipleValuesAnimationDemo: borderWidth, degrees; isRunning, segment, currentState); Tutorials Ch.12 (JoinButton: bốn thuộc tính);
# "Value-based animations" (updateTransition).

SEC_ORDER = {'c3': ['hook', 'why', 't', 'state', 'spec', 'mutable', 'bugs', 'exercises', 'recall']}

def add(a):
    def B(ch, sec, n, field, vi, en=None):
        a('%s.sec.%s.b.%02d.%s' % (ch, sec, n, field), vi, vi if en is None else en)

    # ---------------- sim animation.segment ----------------
    m = lambda k, vi, en=None: a('m.segment.' + k, vi, en)
    m('title', 'Một Transition, ba con, và khi nào currentState đổi', 'One Transition, three children, and when currentState changes')
    m('overview', 'Thẻ `Collapsed ↔ Expanded` theo ví dụ của trang Value-based. Một `Transition` dẫn ba con: alpha (tween 150 ms), color (tween 300 ms), height (spring, khoảng 400 ms trong mô hình). Ba tình huống: mở rộng bình thường; đổi ý về Collapsed giữa chừng; và `MutableTransitionState` bắt đầu khác target.',
      'The `Collapsed ↔ Expanded` card from the Value-based page. One `Transition` drives three children: alpha (a 150 ms tween), color (a 300 ms tween), height (a spring, about 400 ms in the model). Three situations: a normal expansion; changing back to Collapsed mid-way; and a `MutableTransitionState` that starts different from its target.')
    m('wrapup', '`updateTransition` gom nhiều giá trị dưới một state. Khi target đổi, mọi con bắt đầu cùng lúc, mỗi con theo spec riêng.\n`currentState` vẫn là state cũ cho tới khi MỌI con xong, rồi mới thành target; `isRunning` cho biết còn con nào đang chạy. Đổi target giữa chừng thì mọi con cùng đổi hướng. Muốn chạy ngay khi vào composition, dùng `MutableTransitionState` với state đầu khác target.\nQuy tắc dễ nhớ: một state, nhiều giá trị, cùng xuất phát: đó là `updateTransition`.',
      '`updateTransition` groups several values under one state. When the target changes, every child starts at the same time, each with its own spec.\n`currentState` stays the old state until EVERY child is done, and only then becomes the target; `isRunning` tells you whether any child is still running. Changing the target mid-way turns every child around together. To run as soon as it enters composition, use a `MutableTransitionState` with an initial state different from the target.\nRule of thumb: one state, many values, starting together: that is `updateTransition`.')
    m('simp.1', 'Thời lượng của spring (khoảng 400 ms) và các mốc 150/300/450 ms là minh họa; mô hình không vẽ đường cong của từng con.', 'The spring\'s duration (about 400 ms) and the 150/300/450 ms marks are illustrative; the model does not draw each child\'s curve.')
    m('simp.2', 'Khi đổi hướng giữa chừng, mô hình không nói `segment` trở thành gì; tài liệu chỉ bảo đảm các con điều chỉnh về target mới và `currentState` đổi khi xong.', 'When turning around mid-way, the model does not say what `segment` becomes; the docs only guarantee that children adjust towards the new target and `currentState` changes when done.')
    m('ctl.hint', 'Chạy "mở rộng", để ý currentState; rồi thử đổi ý giữa chừng.', 'Run "expand" and watch currentState; then try changing back mid-way.')
    m('ctl.which', 'Tình huống', 'Situation')
    for k, vi, en in [('expand', 'Mở rộng Collapsed → Expanded', 'Expand Collapsed → Expanded'), ('reverse', 'Đổi ý về Collapsed ở 150 ms', 'Change back to Collapsed at 150 ms'), ('mutable', 'MutableTransitionState khác target', 'MutableTransitionState unlike its target')]:
        m('ctl.which.' + k, vi, en)
    m('diagramTitle', 'State, Transition và ba con', 'State, Transition and three children')
    m('diagramDesc', 'State đưa target cho Transition; Transition dẫn ba con alpha, color, height', 'The state gives the Transition its target; the Transition drives three children: alpha, color, height')
    for k, vi, en in [('state', 'State thẻ (cardState)', 'Card state (cardState)'), ('transition', 'Transition (một đối tượng)', 'Transition (one object)'), ('alpha', 'Con alpha (tween 150)', 'alpha child (150 ms tween)'), ('color', 'Con color (tween 300)', 'color child (300 ms tween)'), ('height', 'Con height (spring)', 'height child (spring)')]:
        m('n.' + k, vi, en)
    for k, vi, en in [('running', 'Con đang chạy', 'Children running'), ('ms', 'Thời gian (ms)', 'Time (ms)')]:
        m('met.' + k, vi, en)
    for k, vi, en in [('target', 'Giá trị targetState', 'targetState value'), ('current', 'Giá trị currentState', 'currentState value'), ('running', 'Giá trị isRunning', 'isRunning value')]:
        m('st.' + k, vi, en)
    S = [
        ('intro.expand', 'Thẻ đang Collapsed', 'The card is Collapsed', '`updateTransition(targetState = cardState)` đã ở yên: current = target = Collapsed.', '`updateTransition(targetState = cardState)` is at rest: current = target = Collapsed.'),
        ('intro.reverse', 'Thẻ đang Collapsed, sắp mở', 'The card is Collapsed, about to open', 'Như trên, nhưng người dùng sẽ bấm lại sau 150 ms.', 'As above, but the user will tap again after 150 ms.'),
        ('intro.mutable', 'Thẻ mới vào màn hình', 'The card just entered the screen', 'Dùng `MutableTransitionState(Collapsed)` rồi đặt `targetState = Expanded` ngay khi tạo.', 'It uses `MutableTransitionState(Collapsed)` and sets `targetState = Expanded` right away.'),
        ('target', 'Target đổi thành Expanded: ba con bắt đầu cùng lúc', 'The target becomes Expanded: three children start together', 'Mỗi lần composable chạy, `updateTransition` gọi `transition.animateTo(target)`. Target mới làm mọi con bắt đầu chạy về giá trị của Expanded, mỗi con theo `transitionSpec` của nó.', 'Every time the composable runs, `updateTransition` calls `transition.animateTo(target)`. The new target makes every child start towards Expanded\'s values, each following its own `transitionSpec`.'),
        ('enter', 'Vào composition là chạy ngay', 'It runs as soon as it enters composition', 'Current = Collapsed, target = Expanded ngay từ đầu, nên Transition chạy mà không cần đổi state nào.', 'Current = Collapsed and target = Expanded from the start, so the Transition runs without any state change.'),
        ('alphaDone', '150 ms: alpha xong, currentState vẫn Collapsed', '150 ms: alpha is done, currentState is still Collapsed', 'Một con xong chưa đủ: `currentState` chỉ đổi khi mọi con xong.', 'One child finishing is not enough: `currentState` only changes when every child is done.'),
        ('colorDone', '300 ms: color xong', '300 ms: color is done', 'Còn height (spring) đang chạy.', 'The height (spring) is still running.'),
        ('allDone', 'Height xong: currentState = Expanded', 'Height is done: currentState = Expanded', 'Con cuối cùng xong; Transition đặt `currentState` thành target và `isRunning` thành false.', 'The last child is done; the Transition sets `currentState` to the target and `isRunning` to false.'),
        ('reverse', '150 ms: target đổi về Collapsed', '150 ms: the target changes back to Collapsed', 'Mọi con đang chạy đổi hướng về giá trị của Collapsed, từ giá trị hiện tại của chúng.', 'Every running child turns towards Collapsed\'s values, from its current value.'),
        ('rev.mostDone', '300 ms: chỉ còn height', '300 ms: only the height is left', 'Alpha và color đã về; height (spring) còn đang quay lại.', 'Alpha and color are back; the height (spring) is still returning.'),
        ('rev.done', 'Xong: isRunning = false', 'Done: isRunning = false', 'Target là Collapsed và mọi con đã tới, nên current = target = Collapsed. `currentState` chưa từng là Expanded.', 'The target is Collapsed and every child has arrived, so current = target = Collapsed. `currentState` was never Expanded.'),
        ('end.expand', 'Kết thúc: current = Expanded sau 400 ms', 'The end: current = Expanded after 400 ms', 'Lâu bằng con chậm nhất.', 'As long as the slowest child.'),
        ('end.reverse', 'Kết thúc: quay về Collapsed', 'The end: back to Collapsed', 'Đổi ý giữa chừng không làm nhảy giá trị.', 'Changing your mind mid-way does not make values jump.'),
        ('end.mutable', 'Kết thúc: current = Expanded', 'The end: current = Expanded', '`MutableTransitionState` còn có `isIdle` để biết đã xong.', '`MutableTransitionState` also has `isIdle` to tell when it is done.'),
    ]
    for sid, tv, te, xv, xe in S:
        m('s.%s.title' % sid, tv, te); m('s.%s.explain' % sid, xv, xe); m('ev.' + sid, tv, te)
    for k, vi, en in [
        ('mutable', 'KDoc: biến thể `MutableTransitionState` cho phép state đầu khác target, nên Transition chạy ngay khi vào composition; và có thể tạo lại để cố ý chạy lại. [[src:an-transition-src]]', 'The KDoc: the `MutableTransitionState` variant allows an initial state different from the target, so the Transition starts as soon as it enters composition; and it can be recreated to restart on purpose. [[src:an-transition-src]]'),
        ('adjust', 'KDoc: khi target đổi, Transition tự bắt đầu hoặc "adjust course" cho mọi con về giá trị mới. [[src:an-transition-src]]', 'The KDoc: when the target changes, the Transition automatically starts or adjusts course for all its children towards the new values. [[src:an-transition-src]]'),
        ('current', 'KDoc: `currentState` luôn là initialState cho tới khi transition xong; xong thì được đặt bằng targetState. [[src:an-transition-src]]', 'The KDoc: `currentState` is always the initialState until the transition is finished; then it is set to targetState. [[src:an-transition-src]]'),
        ('end.expand', 'Transition còn có `isRunning`, `segment` (state đầu và đích của lượt đang chạy) và `currentState`. [[src:book-kunneth]]', 'A Transition also has `isRunning`, `segment` (the initial and target state of the ongoing run) and `currentState`. [[src:book-kunneth]]'),
        ('end.mutable', 'Đây là cách đúng để một phần tử "mờ dần khi vừa xuất hiện" (C1 bug 1). [[src:an-transition-src]]', 'This is the right way for an element to "fade in on appearing" (C1 bug 1). [[src:an-transition-src]]')]:
        m('co.' + k, vi, en)
    a('cap.segment', 'State bên trái đưa target cho Transition ở giữa; ba con bên phải chạy cùng lúc, mỗi con theo spec riêng. Chỉ số đếm số con còn chạy và thời gian.', 'The state on the left gives the Transition in the middle its target; the three children on the right run together, each with its own spec. The metrics count running children and time.')

    # ---------------- chương C3 ----------------
    C = 'c3'
    a(C + '.sim.animation.segment', 'currentState và các con', 'currentState and the children')
    a(C + '.sim.animation.transition', 'Bật/tắt từng con', 'Turning children on/off')

    S = 'hook'
    a(C + '.sec.%s.title' % S, 'Đoán trước khi đọc', 'Predict before reading')
    a(C + '.sec.%s.badge' % S, 'stable')
    B(C, S, 1, 'predict', 'Một Transition có ba con: alpha xong sau 150 ms, color sau 300 ms, height sau 400 ms. Ở 200 ms, `transition.currentState` là state cũ hay state mới?', 'A Transition has three children: alpha finishes after 150 ms, color after 300 ms, height after 400 ms. At 200 ms, is `transition.currentState` the old state or the new one?')
    B(C, S, 1, 'ans', 'State cũ. Theo KDoc ở commit ghim, `currentState` luôn là state ban đầu cho tới khi transition XONG, tức khi mọi con đã tới; chỉ khi đó nó mới bằng `targetState`. Ở 200 ms color và height còn chạy. [[src:an-transition-src]]', 'The old state. Per the KDoc at the pinned commit, `currentState` is always the initial state until the transition is FINISHED, that is, until every child has arrived; only then does it equal `targetState`. At 200 ms, color and height are still running. [[src:an-transition-src]]')

    S = 'why'
    a(C + '.sec.%s.title' % S, 'Vì sao cần Transition', 'Why a Transition is needed')
    a(C + '.sec.%s.badge' % S, 'stable')
    B(C, S, 1, 'p', 'Giả sử một nút "Tham gia" cần đổi bốn thứ cùng lúc khi state đổi: màu nền, màu icon, chữ hiện hay ẩn, và chiều rộng. Viết bốn `animate*AsState` riêng thì vẫn chạy. Nhưng chúng không biết gì về nhau: không có chỗ nào hỏi "đã xong hết chưa?", và mỗi cái là một đối tượng riêng trong công cụ [[src:book-compose-tut]] [[src:book-kunneth]].\n`updateTransition` gom chúng lại: một state, nhiều con, cùng bắt đầu. Cây quyết định cũng đi đúng câu hỏi đó: nhiều thuộc tính cần bắt đầu cùng lúc thì dùng `updateTransition` [[src:an-choose]].\nGiống một dàn nhạc: một cái vung tay của nhạc trưởng, mọi nhạc cụ cùng vào, mỗi cái theo bản nhạc riêng.',
      'Suppose a "Join" button must change four things at once when its state changes: background colour, icon colour, text shown or hidden, and width. Four separate `animate*AsState` calls still work. But they know nothing about each other: there is nowhere to ask "is everything done?", and each is a separate object in tooling [[src:book-compose-tut]] [[src:book-kunneth]].\n`updateTransition` groups them: one state, many children, starting together. The decision tree follows the same question: several properties that must start together call for `updateTransition` [[src:an-choose]].\nLike an orchestra: one wave of the conductor\'s hand, every instrument comes in, each following its own part.')
    B(C, S, 2, 'kt', '// rút gọn\nval transition = updateTransition(targetState = buttonState, label = "JoinButtonTransition")\nval duration = 600\nval buttonBackgroundColor: Color by transition.animateColor(\n    transitionSpec = { tween(duration) },\n    label = "Button Background Color"\n) { state ->\n    when (state) {\n        JoinButtonState.IDLE -> Color.Blue\n        JoinButtonState.PRESSED -> Color.White\n    }\n}\n// tương tự: animateDp cho chiều rộng, animateColor cho icon, animateFloat cho alpha của chữ', '// Tutorials, condensed\nval transition = updateTransition(targetState = buttonState, label = "JoinButtonTransition")\nval duration = 600\nval buttonBackgroundColor: Color by transition.animateColor(\n    transitionSpec = { tween(duration) },\n    label = "Button Background Color"\n) { state ->\n    when (state) {\n        JoinButtonState.IDLE -> Color.Blue\n        JoinButtonState.PRESSED -> Color.White\n    }\n}\n// likewise: animateDp for the width, animateColor for the icon, animateFloat for the text alpha')

    S = 'state'
    a(C + '.sec.%s.title' % S, 'Dưới mui xe: animateTo, currentState, isRunning', 'Under the hood: animateTo, currentState, isRunning')
    a(C + '.sec.%s.badge' % S, 'impl')
    B(C, S, 1, 'p', 'Ở commit ghim, `updateTransition(targetState, label)` chỉ làm ba việc: `remember` một Transition; gọi `transition.animateTo(targetState)` mỗi lần composable chạy; và dùng một `DisposableEffect` để dọn dẹp khi rời composition.\nMỗi con (`animateFloat`, `animateDp`, `animateColor`…) là một animation được thêm vào Transition, mặc định dùng spring. KDoc của Transition: khi target đổi, nó tự bắt đầu hoặc chỉnh hướng cho mọi con; đã tới target rồi mà giá trị đích của một con đổi (ví dụ theo theme), Transition chạy lại. `currentState` là state ban đầu cho tới khi xong, rồi bằng `targetState`.\nMô phỏng ngay dưới đi qua ba tình huống [[src:an-transition-src]].',
      "At the pinned commit, `updateTransition(targetState, label)` does just three things: `remember` a Transition; call `transition.animateTo(targetState)` every time the composable runs; and use a `DisposableEffect` to clean up on leaving composition.\nEach child (`animateFloat`, `animateDp`, `animateColor`…) is an animation added to the Transition, using a spring by default. The Transition KDoc: when the target changes, it starts or re-steers every child by itself; once it has reached the target, if a child's target value changes (say, with the theme), the Transition runs again. `currentState` is the initial state until done, then equals `targetState`.\nThe simulation just below walks through three situations [[src:an-transition-src]].")

    S = 'spec'
    a(C + '.sec.%s.title' % S, 'transitionSpec theo hướng', 'transitionSpec by direction')
    a(C + '.sec.%s.badge' % S, 'stable')
    B(C, S, 1, 'p', '`transitionSpec` là một lambda trên `Transition.Segment`, nên có thể chọn spec khác nhau cho từng cặp state đầu và đích. `Collapsed isTransitioningTo Expanded` đúng khi lượt đang chạy đi từ Collapsed tới Expanded. Ví dụ: mở bằng spring mềm, đóng bằng tween nhanh.\nKDoc của `animateFloat`: spec có thể là mọi `FiniteAnimationSpec` (tween, spring, keyframes, repeatable), nhưng KHÔNG được là `infiniteRepeatable`, vì Transition phải biết lúc nào xong [[src:an-transition-src]].\nQuy tắc dễ nhớ: mở và đóng không nhất thiết phải cùng một kiểu chuyển động.',
      '`transitionSpec` is a lambda on `Transition.Segment`, so you can pick a different spec for each pair of initial and target states. `Collapsed isTransitioningTo Expanded` is true when the current run goes from Collapsed to Expanded. For example: open with a soft spring, close with a quick tween.\nThe `animateFloat` KDoc: the spec can be any `FiniteAnimationSpec` (tween, spring, keyframes, repeatable), but NOT `infiniteRepeatable`, because the Transition must know when it is done [[src:an-transition-src]].\nRule of thumb: opening and closing need not use the same kind of motion.')

    S = 'mutable'
    a(C + '.sec.%s.title' % S, 'MutableTransitionState: chạy khi vừa vào', 'MutableTransitionState: running on entry')
    a(C + '.sec.%s.badge' % S, 'stable')
    B(C, S, 1, 'p', '`updateTransition` lấy target đầu tiên làm state ban đầu, nên lần composition đầu không có gì để chạy (giống C1).\nKDoc gợi ý biến thể `rememberTransition(transitionState)` với một `MutableTransitionState`. Nó cho phép state đầu khác target, để chạy ngay khi vào composition, và có thể tạo lại để cố ý chạy lại từ đầu. `MutableTransitionState` phải được `remember`. C4 dùng đúng cách này với `AnimatedVisibility` [[src:an-transition-src]].\nQuy tắc dễ nhớ: muốn animation chạy ngay lúc màn hình hiện ra thì cho state đầu khác state đích.',
      '`updateTransition` takes the first target as its initial state, so the first composition has nothing to run (as in C1).\nThe KDoc points to the `rememberTransition(transitionState)` variant with a `MutableTransitionState`. It allows an initial state different from the target, to run as soon as it enters composition, and it can be recreated to restart on purpose. The `MutableTransitionState` must be `remember`ed. C4 uses exactly this with `AnimatedVisibility` [[src:an-transition-src]].\nRule of thumb: to have an animation run the moment the screen appears, give it an initial state different from its target.')
    B(C, S, 2, 'kt', 'val cardState = remember {\n    MutableTransitionState(CardState.Collapsed).apply { targetState = CardState.Expanded }\n}\nval transition = rememberTransition(cardState, label = "card")\n// cardState.isIdle: true khi đã tới target và không còn chạy', 'val cardState = remember {\n    MutableTransitionState(CardState.Collapsed).apply { targetState = CardState.Expanded }\n}\nval transition = rememberTransition(cardState, label = "card")\n// cardState.isIdle: true once the target is reached and nothing is running')

    S = 'bugs'
    a(C + '.sec.%s.title' % S, 'Bug thường gặp', 'Common bugs')
    a(C + '.sec.%s.badge' % S, 'stable')
    B(C, S, 1, 'bug', 'Nút "Lưu" bật khi `transition.currentState == Expanded`, nhưng người dùng thấy thẻ đã mở mà nút vẫn mờ một lúc.', 'A "Save" button is enabled when `transition.currentState == Expanded`, but users see the card open while the button stays disabled for a moment.')
    B(C, S, 1, 'cause', '`currentState` chỉ đổi khi con CHẬM NHẤT xong (ví dụ một spring chiều cao còn đang lắng). Thẻ trông đã mở trước đó.', '`currentState` only changes when the SLOWEST child finishes (say, a height spring still settling). The card looks open before that.')
    B(C, S, 1, 'fix', 'Điều kiện logic dựa trên `targetState` (ý định) hoặc state của bạn, không dựa vào `currentState`; chỉ dùng `currentState`/`isRunning` khi thật cần biết animation đã xong. [[src:an-transition-src]]', 'Base logic on `targetState` (the intent) or your own state, not `currentState`; use `currentState`/`isRunning` only when you really need to know the animation is done. [[src:an-transition-src]]')
    B(C, S, 2, 'bug', 'Biên dịch lỗi khi truyền `infiniteRepeatable(tween(500))` vào `transitionSpec` của `animateFloat`.', 'A compile error when passing `infiniteRepeatable(tween(500))` to `animateFloat`\'s `transitionSpec`.')
    B(C, S, 2, 'cause', '`transitionSpec` đòi `FiniteAnimationSpec`; `infiniteRepeatable` không phải (theo KDoc), vì Transition phải kết thúc được.', '`transitionSpec` requires a `FiniteAnimationSpec`; `infiniteRepeatable` is not one (per the KDoc), because a Transition must be able to finish.')
    B(C, S, 2, 'fix', 'Dùng `rememberInfiniteTransition` cho chuyển động lặp mãi (chương "if"), hoặc `repeatable(n, …)` nếu số lần lặp có hạn. [[src:an-transition-src]] [[src:an-value]]', 'Use `rememberInfiniteTransition` for endlessly repeating motion (chapter "if"), or `repeatable(n, …)` for a finite number of repeats. [[src:an-transition-src]] [[src:an-value]]')

    S = 'exercises'
    a(C + '.sec.%s.title' % S, 'Bài tập', 'Exercises')
    a(C + '.sec.%s.badge' % S, 'stable')
    B(C, S, 1, 'ex', 'Viết `transitionSpec` cho chiều cao: mở (Collapsed → Expanded) bằng `spring(dampingRatio = Spring.DampingRatioLowBouncy)`, đóng bằng `tween(200)`.', 'Write a `transitionSpec` for the height: open (Collapsed → Expanded) with `spring(dampingRatio = Spring.DampingRatioLowBouncy)`, close with `tween(200)`.')
    B(C, S, 1, 'solkt', 'val height by transition.animateDp(\n    transitionSpec = {\n        when {\n            CardState.Collapsed isTransitioningTo CardState.Expanded ->\n                spring(dampingRatio = Spring.DampingRatioLowBouncy)\n            else -> tween(durationMillis = 200)\n        }\n    },\n    label = "height"\n) { if (it == CardState.Expanded) 200.dp else 64.dp }')
    B(C, S, 1, 'sol', '`isTransitioningTo` là infix trên `Segment`, kiểm cặp state đầu–đích của lượt đang chạy.', '`isTransitioningTo` is an infix on `Segment`, checking the initial–target pair of the current run.')
    B(C, S, 2, 'ex', 'Trong mô phỏng "đổi ý về Collapsed ở 150 ms", `currentState` có lúc nào là Expanded không? Vì sao?', 'In the "change back to Collapsed at 150 ms" simulation, is `currentState` ever Expanded? Why?')
    B(C, S, 2, 'sol', 'Không. Transition chưa bao giờ xong ở Expanded; `currentState` chỉ đổi khi transition xong, và khi xong thì target đã là Collapsed.', 'No. The Transition never finished at Expanded; `currentState` only changes when the transition finishes, and by then the target was Collapsed.')

    S = 'recall'
    a(C + '.sec.%s.title' % S, 'Tự trả lời', 'Answer it yourself')
    a(C + '.sec.%s.badge' % S, 'stable')
    B(C, S, 1, 'ask', 'updateTransition làm gì mỗi lần composable chạy?', 'What does updateTransition do each time the composable runs?')
    B(C, S, 1, 'ans', 'Gọi transition.animateTo(targetState) trên Transition đã remember.', 'Calls transition.animateTo(targetState) on the remembered Transition.')
    B(C, S, 2, 'ask', 'Khi nào currentState bằng targetState?', 'When does currentState equal targetState?')
    B(C, S, 2, 'ans', 'Khi mọi con đã xong.', 'When every child is done.')
    for q, qv, qe, av, ae, wv, we in [
        ('q3', 'Spec mặc định của một con trong Transition?', 'The default spec of a Transition child?',
         'spring.', 'A spring.', 'KDoc của animateFloat: mặc định spring cho mọi đích.', 'The animateFloat KDoc: a spring for every destination by default.'),
        ('q4', 'Muốn Transition chạy ngay khi vào composition thì dùng gì?', 'What makes a Transition run as soon as it enters composition?',
         'MutableTransitionState với state đầu khác target.', 'A MutableTransitionState whose initial state differs from its target.', 'Truyền vào rememberTransition.', 'Pass it to rememberTransition.')]:
        a(C + '.quiz.%s.q' % q, qv, qe); a(C + '.quiz.%s.a' % q, av, ae); a(C + '.quiz.%s.why' % q, wv, we)

def override(o):
    C = 'c3'
    o(C + '.essence',
      '`animate*AsState` hợp với từng thuộc tính độc lập. Khi nhiều thuộc tính phải đổi cùng nhau theo một state (ví dụ màu nền, màu icon, chữ, chiều rộng của một nút), `updateTransition` gom chúng: một state, nhiều con, bắt đầu cùng lúc, mỗi con một spec (`transitionSpec`, có thể khác theo hướng).\n'
      'Ở commit ghim, `updateTransition` chỉ remember một Transition và gọi `animateTo(target)` mỗi lần chạy. `currentState` giữ state cũ cho tới khi MỌI con xong; `isRunning` cho biết còn con nào chạy; đổi target giữa chừng thì mọi con đổi hướng.\n'
      'Muốn chạy ngay khi vào composition, dùng `rememberTransition` với một `MutableTransitionState` có state đầu khác target.',
      '`animate*AsState` suits independent properties. When several properties must change together following one state (for example a button\'s background colour, icon colour, text and width), `updateTransition` groups them: one state, many children, starting together, each with its own spec (`transitionSpec`, which can depend on direction).\n'
      'At the pinned commit, `updateTransition` just remembers a Transition and calls `animateTo(target)` on every run. `currentState` keeps the old state until EVERY child is done; `isRunning` says whether any child is still running; changing the target mid-way turns every child around.\n'
      'To run as soon as it enters composition, use `rememberTransition` with a `MutableTransitionState` whose initial state differs from its target.')
    o(C + '.goal.g1', 'Đã thấy target đổi và các con bắt đầu', 'Saw the target change and the children start')
    o(C + '.goal.g2', 'Đã chạy một tình huống tới cuối', 'Ran one situation to the end')
