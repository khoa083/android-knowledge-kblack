# Animation v2 · C0 Bản đồ và chọn API (viết lại CUỐI CÙNG; giữ mục v1 'pairs' và sim animation.choose)
# Nguồn: "Choose an animation API" (an-choose: cây quyết định, cấu trúc lồng nhau đọc từ HTML 2026-11-23); các chương C1–C8, IF, SE, CV, VM.

SEC_ORDER = {'c0': ['hook', 'map', 'tree', 'pairs', 'symptoms', 'honesty', 'recall']}

QS = [
    ('art', 'Animation có dựa trên hình (SVG, ảnh) không?', 'Is the animation art-based (SVGs, images)?'),
    ('svg', 'Có phải SVG đơn giản (icon với micro-animation)?', 'Is it a simple SVG (an icon with micro-animations)?'),
    ('infinite', 'Có cần lặp vô hạn không?', 'Does it need to repeat infinitely?'),
    ('layout', 'Có đang animate một layout không?', 'Are you animating a layout?'),
    ('switch', 'Có đổi giữa các composable có nội dung khác nhau?', 'Are you switching between composables with different content?'),
    ('nav', 'Có dùng Navigation-Compose không?', 'Are you using Navigation-Compose?'),
    ('appear', 'Có animate việc nội dung xuất hiện/biến mất?', 'Are you animating content appearing/disappearing?'),
    ('size', 'Có animate thay đổi kích thước?', 'Are you animating a size change?'),
    ('multi', 'Có animate nhiều thuộc tính?', 'Are you animating multiple properties?'),
    ('indep', 'Các thuộc tính hoàn toàn độc lập với nhau?', 'Are the properties completely independent?'),
    ('together', 'Chúng cần bắt đầu cùng lúc?', 'Do they need to start at the same time?'),
    ('target', 'Animation có giá trị đích định trước?', 'Does the animation have predefined target values?'),
    ('gesture', 'Animation do cử chỉ điều khiển và là nguồn sự thật duy nhất?', 'Is it gesture-driven and the single source of truth?'),
]
SCEN = [
    ('icon', 'Icon "yêu thích" có micro-animation từ file SVG của designer', 'A "favourite" icon with a micro-animation from the designer\'s SVG',
     'AnimatedVectorDrawable', 'AnimatedVectorDrawable (chương CV)', 'AnimatedVectorDrawable (chapter CV)'),
    ('spinner', 'Vòng xoay chờ tải, quay tới khi có dữ liệu', 'A loading spinner turning until data arrives',
     'rememberInfiniteTransition', 'rememberInfiniteTransition (chương IF)', 'rememberInfiniteTransition (chapter IF)'),
    ('screen', 'Chuyển từ màn danh sách sang màn chi tiết bằng Navigation-Compose', 'Going from a list screen to a detail screen with Navigation-Compose',
     'composable() + enterTransition/exitTransition', 'composable() với enterTransition/exitTransition (chương C4; thêm shared element ở chương SE)', 'composable() with enterTransition/exitTransition (chapter C4; add shared elements in chapter SE)'),
    ('expand', 'Thẻ "Đọc thêm" mở rộng chiều cao', 'A "Read more" card growing taller',
     'Modifier.animateContentSize', 'Modifier.animateContentSize (chương C5)', 'Modifier.animateContentSize (chapter C5)'),
    ('together', 'Nút đổi màu nền, viền và kích thước cùng lúc khi chọn', 'A button changing background, border and size together when selected',
     'updateTransition', 'updateTransition (chương C3)', 'updateTransition (chapter C3)'),
    ('swipe', 'Thẻ kéo để xóa, thả thì bật về hoặc bay đi', 'A swipe-to-dismiss card that springs back or flies away on release',
     'Animatable (animateTo / snapTo)', 'Animatable với animateTo / snapTo (chương C6)', 'Animatable with animateTo / snapTo (chapter C6)'),
]

def add(a):
    def B(ch, sec, n, field, vi, en=None):
        a('%s.sec.%s.b.%02d.%s' % (ch, sec, n, field), vi, vi if en is None else en)

    m = lambda k, vi, en=None: a('m.tree.' + k, vi, en)
    m('title', 'Đi theo cây quyết định của tài liệu', 'Walking the docs\' decision tree')
    m('overview', 'Chọn một nhu cầu thật, rồi đi từng câu hỏi của cây "Choose an animation API" tới API mà tài liệu gợi ý và chương của track giảng nó.', 'Pick a real need, then walk each question of the "Choose an animation API" tree to the API the docs suggest and the track chapter that teaches it.')
    m('wrapup', 'Cây quyết định là lối tắt, không phải luật: các API chồng lấp nhau, và câu hỏi đầu tiên đúng thường là "đây có phải layout không?" và "có cần lặp mãi không?". Khi đã có API, chương tương ứng giải thích nó chạy thế nào ở bên trong.', 'The decision tree is a shortcut, not a rule: the APIs overlap, and the right first questions are often "is this a layout?" and "does it repeat forever?". Once you have the API, the matching chapter explains how it works inside.')
    m('simp.1', 'Mô hình chỉ đi theo các nhánh của 6 nhu cầu mẫu; cây đầy đủ có thêm nhánh (Lottie, AnimatedContent/Crossfade/Pager, CapturedAnimatedVisibility, animateItem, AnimationState/animate).', 'The model only follows the branches of 6 sample needs; the full tree has more branches (Lottie, AnimatedContent/Crossfade/Pager, CapturedAnimatedVisibility, animateItem, AnimationState/animate).')
    m('ctl.hint', 'Thử "Nút đổi nhiều thuộc tính" và "Thẻ kéo để xóa": cả hai đi qua nhánh "không phải layout".', 'Try "A button changing several properties" and "A swipe-to-dismiss card": both go through the "not a layout" branch.')
    m('ctl.which', 'Nhu cầu', 'Need')
    m('diagramTitle', 'Nhu cầu, câu hỏi, API, chương', 'Need, question, API, chapter')
    m('diagramDesc', 'Nhu cầu đi qua từng câu hỏi của cây tới một API, rồi tới chương giảng API đó', 'The need goes through each question of the tree to an API, then to the chapter teaching it')
    for k, vi, en in [('need', 'Nhu cầu', 'Need'), ('question', 'Câu hỏi của cây', 'Tree question'), ('api', 'API gợi ý', 'Suggested API'), ('chapter', 'Chương giảng nó', 'Chapter teaching it')]:
        m('n.' + k, vi, en)
    for k, vi, en in [('depth', 'Số câu hỏi đã qua', 'Questions answered')]:
        m('met.' + k, vi, en)
    for k, vi, en in [('answer', 'Trả lời', 'Answer'), ('api', 'API', 'API')]:
        m('st.' + k, vi, en)
    for qid, vi, en in QS:
        m('s.q.%s.title' % qid, vi, en); m('ev.q.' + qid, vi, en)
    m('s.ans.yes', 'Với nhu cầu này: CÓ, đi nhánh "Có".', 'For this need: YES, take the "Yes" branch.')
    m('s.ans.no', 'Với nhu cầu này: KHÔNG, đi nhánh "Không".', 'For this need: NO, take the "No" branch.')
    for sid, nv, ne, api, av, ae in SCEN:
        m('ctl.which.' + sid, nv, ne)
        m('s.intro.%s.title' % sid, nv, ne); m('ev.intro.' + sid, nv, ne)
        m('s.intro.%s.explain' % sid, 'Bắt đầu từ câu hỏi đầu tiên của cây.', 'Start from the tree\'s first question.')
        m('s.api.%s.title' % sid, av, ae); m('ev.api.' + sid, av, ae)
        m('s.api.%s.explain' % sid, 'Đây là API cây gợi ý cho nhu cầu này. Chương tương ứng giải thích nó chạy thế nào bên trong và các bẫy thường gặp.', 'This is the API the tree suggests for this need. The matching chapter explains how it works inside and its common traps.')
    m('co.tree', 'Cây quyết định của trang "Choose an animation API" (cấu trúc đọc từ trang ngày 2026-11-23). [[src:an-choose]]', 'The decision tree from the "Choose an animation API" page (structure read from the page on 2026-11-23). [[src:an-choose]]')
    m('co.overlap', 'Các API chồng lấp: ví dụ mờ dần có thể dùng AnimatedVisibility hoặc animateFloatAsState với Modifier.alpha; tài liệu liệt kê cả hai. [[src:an-choose]]', 'The APIs overlap: a fade, for example, can use AnimatedVisibility or animateFloatAsState with Modifier.alpha; the docs list both. [[src:an-choose]]')
    a('cap.tree', 'Nhu cầu bên trái đi qua câu hỏi của cây tới API gợi ý, rồi tới chương giảng API đó bên phải.', 'The need on the left goes through the tree\'s questions to the suggested API, then to the chapter teaching it on the right.')

    C = 'c0'
    a(C + '.sim.animation.tree', 'Đi theo cây chọn API', 'Walking the API decision tree')
    a(C + '.sim.animation.choose', 'API theo nhu cầu', 'API by need')

    S = 'hook'
    a(C + '.sec.%s.title' % S, 'Đoán trước khi đọc', 'Predict before reading')
    a(C + '.sec.%s.badge' % S, 'stable')
    B(C, S, 1, 'predict', 'Một nút đổi màu nền, màu viền và kích thước khi được chọn, ba thay đổi phải bắt đầu cùng lúc. Dùng ba `animate*AsState` hay một `updateTransition`?', 'A button changes its background, border colour and size when selected, and the three changes must start together. Three `animate*AsState` or one `updateTransition`?')
    B(C, S, 1, 'ans', 'Cây của tài liệu: không phải layout → nhiều thuộc tính → KHÔNG độc lập → cần bắt đầu cùng lúc → `updateTransition`. Ba `animate*AsState` chỉ hợp khi các thuộc tính hoàn toàn độc lập. Chương C3 giải thích vì sao một Transition giữ chúng đồng bộ. [[src:an-choose]]', 'The docs\' tree: not a layout → multiple properties → NOT independent → need to start together → `updateTransition`. Three `animate*AsState` only fit when the properties are completely independent. Chapter C3 explains why one Transition keeps them in sync. [[src:an-choose]]')

    S = 'map'
    a(C + '.sec.%s.title' % S, 'Bản đồ track và thứ tự đọc', 'Track map and reading order')
    a(C + '.sec.%s.badge' % S, 'stable')
    B(C, S, 1, 'p', 'Track này có 13 chương. Nếu từng làm animation trong hệ View, đọc VM trước để có bảng đối chiếu. Lõi là bốn chương liền nhau: C1 (animate*AsState: từ đích tới giá trị), C2 (AnimationSpec: spring, tween, easing, keyframes, AnimationVector), C3 (updateTransition: nhiều giá trị theo một state) và C4 (AnimatedVisibility, AnimatedContent, khi nào nội dung rời composition). Tiếp theo là các nhu cầu cụ thể: C5 (kích thước, layout, item trong list), IF (lặp và vô hạn), C6 (Animatable và cử chỉ), SE (shared element), CV (Canvas và vector động). Hai chương cuối nhìn vào bên trong và kiểm chứng: C7 (frame clock, thứ tự trong một frame, tỉ lệ thời lượng) và C8 (đồng hồ test, công cụ, giảm chuyển động).', 'This track has 13 chapters. If you have done animation in the View system, read VM first for the mapping table. The core is four consecutive chapters: C1 (animate*AsState: from target to value), C2 (AnimationSpec: spring, tween, easing, keyframes, AnimationVector), C3 (updateTransition: several values from one state) and C4 (AnimatedVisibility, AnimatedContent, when content leaves composition). Then specific needs: C5 (size, layout, list items), IF (repeating and infinite), C6 (Animatable and gestures), SE (shared elements), CV (Canvas and animated vectors). The last two look inside and verify: C7 (the frame clock, the order within a frame, the duration scale) and C8 (the test clock, tools, reduced motion).')
    B(C, S, 2, 'p', 'Track này dựa trên track Compose Runtime: phase và nơi đọc state (B7, cầu nối X1), Recomposer và frame clock (B5, X3), effect và coroutine (EF, A8 của Coroutines), Modifier.Node (MD), lazy list và key (LZ). Mọi chi tiết bên trong được ghim vào commit androidx-main 296313a4; sách (Kunneth, Jetpack Compose by Tutorials, Jetpack Compose 1.3 Essentials, Android Animations by Tutorials) là nguồn giảng chính, và chỗ nào sách cũ hơn mã hiện tại đều được ghi rõ.', 'This track builds on the Compose Runtime track: phases and where state is read (B7, bridge X1), the Recomposer and frame clock (B5, X3), effects and coroutines (EF, Coroutines A8), Modifier.Node (MD), lazy lists and keys (LZ). Every internal detail is pinned to androidx-main commit 296313a4; the books (Kunneth, Jetpack Compose by Tutorials, Jetpack Compose 1.3 Essentials, Android Animations by Tutorials) are the main teaching sources, and wherever a book is older than the current code, it is noted.')

    S = 'tree'
    a(C + '.sec.%s.title' % S, 'Cây quyết định chọn API', 'The API decision tree')
    a(C + '.sec.%s.badge' % S, 'guideline')
    B(C, S, 1, 'p', 'Trang "Choose an animation API" có một cây quyết định. Nhánh trên cùng: dựa trên hình? (SVG đơn giản → AnimatedVectorDrawable; phức tạp → thư viện bên thứ ba như Lottie). Không → lặp vô hạn? (→ `rememberInfiniteTransition`). Không → animate một layout? Nếu CÓ: đổi giữa nội dung khác nhau (Navigation-Compose → `composable()` với `enterTransition`/`exitTransition`; không → `AnimatedContent`, `Crossfade` hoặc `Pager`); xuất hiện/biến mất (`AnimatedVisibility`, `CapturedAnimatedVisibility`, hoặc `animateFloatAsState` + `Modifier.alpha()`); kích thước (`Modifier.animateContentSize`); thuộc tính layout khác như offset hay padding (xem nhánh nhiều thuộc tính); item trong list (`animateItem()`). Nếu KHÔNG phải layout: nhiều thuộc tính? độc lập → `animate*AsState` (với Text: `TextMotion.Animated`); phụ thuộc và bắt đầu cùng lúc → `updateTransition`; khác thời điểm → `Animatable` với các lời gọi suspend. Một thuộc tính: có đích định trước → `animate*AsState`; do cử chỉ điều khiển → `Animatable` (`animateTo`/`snapTo`); một lần không cần quản lý state → `AnimationState` hoặc `animate`. [[src:an-choose]]', 'The "Choose an animation API" page has a decision tree. The top branch: art-based? (simple SVG → AnimatedVectorDrawable; complex → a third-party library such as Lottie). No → repeat infinitely? (→ `rememberInfiniteTransition`). No → animating a layout? If YES: switching between different content (Navigation-Compose → `composable()` with `enterTransition`/`exitTransition`; otherwise → `AnimatedContent`, `Crossfade` or `Pager`); appearing/disappearing (`AnimatedVisibility`, `CapturedAnimatedVisibility`, or `animateFloatAsState` + `Modifier.alpha()`); size (`Modifier.animateContentSize`); another layout property such as offset or padding (see the multiple-properties branch); list items (`animateItem()`). If NOT a layout: multiple properties? independent → `animate*AsState` (for Text: `TextMotion.Animated`); dependent and starting together → `updateTransition`; different timings → `Animatable` with suspend calls. One property: predefined targets → `animate*AsState`; gesture-driven → `Animatable` (`animateTo`/`snapTo`); one-shot without state management → `AnimationState` or `animate`. [[src:an-choose]]')
    B(C, S, 2, 'note', 'Cây có hai mục mới so với các sách: `CapturedAnimatedVisibility` (khi nội dung đang rời đi không cần "sống", chỉ là ảnh chụp trạng thái lúc ra) và `TextMotion.Animated` cho Text. Site chưa giảng chi tiết hai mục này; đọc trang tham chiếu tương ứng trước khi dùng. [[src:an-choose]]', 'The tree has two items newer than the books: `CapturedAnimatedVisibility` (when exiting content need not stay live, just a snapshot of its state at exit) and `TextMotion.Animated` for Text. The site does not teach these two in detail yet; read their reference pages before using them. [[src:an-choose]]')
    B(C, S, 2, 'kind', 'source')
    B(C, S, 3, 'p', 'Mô phỏng ngay dưới đi theo cây với sáu nhu cầu thường gặp và dẫn tới chương giảng API đó.', 'The simulation just below walks the tree with six common needs and leads to the chapter teaching each API.')

    S = 'symptoms'
    a(C + '.sec.%s.title' % S, 'Chỉ mục triệu chứng', 'Symptom index')
    a(C + '.sec.%s.badge' % S, 'stable')
    B(C, S, 1, 'p', 'Box nhảy kích thước dù có animateContentSize → C5 (thứ tự modifier). Hiệu ứng ẩn bị "cụt" → C4 (animation ngoài Transition). Lệnh sau animateTo không chạy → C6 (CancellationException). Nhấp nháy giật ở lượt cuối → IF (số lượt chẵn với Reverse). Ảnh không bay giữa hai màn → SE (key, scope). Góc bo mất khi bay → SE (clip trước sharedElement). AVD chạy ngược khi bấm lần hai → CV (Transition hai trạng thái). Cả màn hình recompose mỗi frame → C7 và B7 (đọc ở phase draw). Test luôn thấy frame đầu hoặc giá trị cuối → C8 (frame khởi động, autoAdvance). Nút dời rồi không bấm được (code View cũ) → VM (view animation).', 'A Box jumps in size despite animateContentSize → C5 (modifier order). A hide effect is "cut short" → C4 (animation outside the Transition). Code after animateTo does not run → C6 (CancellationException). A blink jerks on the last iteration → IF (an even count with Reverse). An image does not fly between screens → SE (keys, scope). Rounded corners vanish in flight → SE (clip before sharedElement). An AVD plays backwards on the second tap → CV (a two-state Transition). The whole screen recomposes every frame → C7 and B7 (read in the draw phase). A test always sees the first frame or the final value → C8 (start-up frames, autoAdvance). A moved button cannot be tapped (old View code) → VM (view animation).')

    S = 'honesty'
    a(C + '.sec.%s.title' % S, 'Site trung thực với bạn thế nào', 'How the site stays honest with you')
    a(C + '.sec.%s.badge' % S, 'simplified')
    B(C, S, 1, 'p', 'Mỗi mô phỏng là mô hình giảng dạy: số liệu (pixel, mili giây, góc) là minh họa và được ghi trong mục "Mô phỏng đang giản lược điều gì". Chi tiết bên trong luôn ghi nguồn là mã AndroidX ở commit 296313a4; API có thể đổi ở phiên bản khác, nên những chỗ nhạy với phiên bản (Animation Preview, runWithoutImplicitWait, InterruptionAwareAnimationSpec, opt-in của shared element) đều có nhãn. Bảng đối chiếu View → Compose ở chương VM là ánh xạ ý niệm do site tự lập.', 'Each simulation is a teaching model: its numbers (pixels, milliseconds, angles) are illustrative and listed under "What the simulation simplifies". Internal details always cite AndroidX code at commit 296313a4; APIs may change in other versions, so version-sensitive spots (Animation Preview, runWithoutImplicitWait, InterruptionAwareAnimationSpec, the shared element opt-in) carry labels. The View → Compose mapping table in chapter VM is a conceptual mapping the site made.')

    S = 'recall'
    a(C + '.sec.%s.title' % S, 'Tự trả lời', 'Answer it yourself')
    a(C + '.sec.%s.badge' % S, 'stable')
    B(C, S, 1, 'ask', 'Hai câu hỏi đầu của cây (sau câu "dựa trên hình?") là gì?', 'What are the tree\'s first two questions (after "art-based?")?')
    B(C, S, 1, 'ans', 'Có lặp vô hạn không? Rồi: có đang animate một layout không?', 'Does it repeat infinitely? Then: are you animating a layout?')
    B(C, S, 2, 'ask', 'Nhiều thuộc tính cần bắt đầu cùng lúc thì dùng gì, nếu khác thời điểm thì dùng gì?', 'Several properties starting together use what, and with different timings?')
    B(C, S, 2, 'ans', 'Cùng lúc: updateTransition. Khác thời điểm: Animatable với các lời gọi suspend.', 'Together: updateTransition. Different timings: Animatable with suspend calls.')
    for q, qv, qe, av, ae, wv, we in [
        ('q3', 'Chuyển màn bằng Navigation-Compose thì cây gợi ý gì?', 'What does the tree suggest for screen changes with Navigation-Compose?', 'composable() với enterTransition/exitTransition.', 'composable() with enterTransition/exitTransition.', 'Nhánh layout → đổi nội dung → Navigation-Compose.', 'Branch layout → switching content → Navigation-Compose.'),
        ('q4', 'Icon micro-animation từ SVG đơn giản dùng gì?', 'What fits a micro-animated icon from a simple SVG?', 'AnimatedVectorDrawable.', 'AnimatedVectorDrawable.', 'Nhánh đầu tiên: dựa trên hình → SVG đơn giản.', 'The first branch: art-based → simple SVG.')]:
        a(C + '.quiz.%s.q' % q, qv, qe); a(C + '.quiz.%s.a' % q, av, ae); a(C + '.quiz.%s.why' % q, wv, we)

def override(o):
    C = 'c0'
    o(C + '.title', 'Bản đồ track và chọn API', 'Track map and choosing an API')
    o(C + '.goal.g1', 'Đã trả lời câu hỏi đầu tiên của cây', 'Answered the tree\'s first question')
    o(C + '.goal.g2', 'Đã đi tới API của một nhu cầu', 'Reached the API for one need')
