# Animation v2 · C0 Bản đồ và chọn API (viết lại CUỐI CÙNG; giữ mục v1 'pairs' và sim animation.choose)
# Nguồn: "Choose an animation API" (an-choose: cây quyết định, cấu trúc lồng nhau đọc từ HTML 2026-11-23); các chương C1–C8, IF, SE, CV, VM.

SEC_ORDER = {'c0': ['hook', 'map', 'tree', 'pairs', 'symptoms', 'recall']}

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
    m('wrapup', 'Cây quyết định là lối tắt, không phải luật: các API chồng lấn nhau. Hai câu hỏi đầu tiên đúng nhất thường là "đây có phải layout không?" và "có cần lặp mãi không?". Có API rồi thì chương tương ứng giải thích nó chạy thế nào ở bên trong.\nQuy tắc dễ nhớ: chọn API theo NHU CẦU (đổi gì, bao lâu, ai điều khiển), không theo tên quen tay.',
      'The decision tree is a shortcut, not a rule: the APIs overlap. The two best first questions are often "is this a layout?" and "does it repeat forever?". Once you have the API, the matching chapter explains how it works inside.\nRule of thumb: choose an API by the NEED (what changes, for how long, who controls it), not by the name you are used to.')
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
    B(C, S, 1, 'p', 'Track này có 13 chương. Nếu bạn từng làm animation trong hệ View, đọc VM trước để có bảng đối chiếu.\n• Lõi là bốn chương liền nhau: C1 (animate*AsState: từ đích tới giá trị), C2 (AnimationSpec: spring, tween, easing, keyframes, AnimationVector), C3 (updateTransition: nhiều giá trị theo một state), C4 (AnimatedVisibility, AnimatedContent, và lúc nào nội dung rời composition).\n• Tiếp theo là các nhu cầu cụ thể: C5 (kích thước, layout, mục trong danh sách), IF (lặp và vô hạn), C6 (Animatable và cử chỉ), SE (shared element), CV (Canvas và vector động).\n• Hai chương cuối nhìn vào bên trong và kiểm chứng: C7 (frame clock, thứ tự trong một frame, tỉ lệ thời lượng), C8 (đồng hồ test, công cụ, giảm chuyển động).\nQuy tắc dễ nhớ: đọc lõi C1–C4 trước, các chương còn lại đọc theo nhu cầu.',
      'This track has 13 chapters. If you have done animation in the View system, read VM first for the mapping table.\n• The core is four chapters in a row: C1 (animate*AsState: from target to value), C2 (AnimationSpec: spring, tween, easing, keyframes, AnimationVector), C3 (updateTransition: several values from one state), C4 (AnimatedVisibility, AnimatedContent, and when content leaves composition).\n• Then come specific needs: C5 (size, layout, list items), IF (repeating and infinite), C6 (Animatable and gestures), SE (shared elements), CV (Canvas and animated vectors).\n• The last two look inside and verify: C7 (the frame clock, the order within a frame, the duration scale), C8 (the test clock, tools, reduced motion).\nRule of thumb: read the core C1–C4 first; read the rest as you need them.')
    B(C, S, 2, 'p', 'Track này dựa trên track Compose Runtime: phase và nơi đọc state (B7, cầu nối X1), Recomposer và frame clock (B5, X3), effect và coroutine (EF, A8 của Coroutines), Modifier.Node (MD), lazy list và key (LZ).\nMọi chi tiết bên trong được ghim vào commit androidx-main 296313a4. Mỗi mô phỏng là mô hình giảng dạy: con số (pixel, mili giây, góc) chỉ để minh hoạ, và được ghi trong ô "giản lược". Chỗ nào nhạy với phiên bản (Animation Preview, runWithoutImplicitWait, InterruptionAwareAnimationSpec, opt-in của shared element) đều có nhãn.',
      'This track builds on the Compose Runtime track: phases and where state is read (B7, bridge X1), the Recomposer and frame clock (B5, X3), effects and coroutines (EF, Coroutines A8), Modifier.Node (MD), lazy lists and keys (LZ).\nEvery internal detail is pinned to androidx-main commit 296313a4. Each simulation is a teaching model: its numbers (pixels, milliseconds, angles) are only illustrative, and are listed in the "simplified" box. Version-sensitive spots (Animation Preview, runWithoutImplicitWait, InterruptionAwareAnimationSpec, the shared element opt-in) carry labels.')

    S = 'tree'
    a(C + '.sec.%s.title' % S, 'Cây quyết định chọn API', 'The API decision tree')
    a(C + '.sec.%s.badge' % S, 'guideline')
    B(C, S, 1, 'p', 'Trang "Choose an animation API" có một cây quyết định. Đi từ trên xuống:\n• Dựa trên hình vẽ? SVG đơn giản thì AnimatedVectorDrawable; phức tạp thì thư viện bên ngoài như Lottie.\n• Không, mà lặp vô hạn? Dùng `rememberInfiniteTransition`.\n• Không, mà animate một layout? Đổi giữa các nội dung khác nhau: với Navigation-Compose thì `composable()` cùng `enterTransition`/`exitTransition`, còn lại thì `AnimatedContent`, `Crossfade` hoặc `Pager`. Xuất hiện, biến mất: `AnimatedVisibility`, `CapturedAnimatedVisibility`, hoặc `animateFloatAsState` + `Modifier.alpha()`. Kích thước: `Modifier.animateContentSize`. Thuộc tính layout khác như offset, padding: xem nhánh nhiều thuộc tính. Mục trong danh sách: `animateItem()`.\n• Không phải layout, mà nhiều thuộc tính? Độc lập nhau thì `animate*AsState` (với Text: `TextMotion.Animated`); phụ thuộc nhau và bắt đầu cùng lúc thì `updateTransition`; khác thời điểm thì `Animatable` với các lời gọi suspend.\n• Một thuộc tính: có đích định trước thì `animate*AsState`; do cử chỉ điều khiển thì `Animatable` (`animateTo`/`snapTo`); chạy một lần, không cần quản lý state thì `AnimationState` hoặc `animate` [[src:an-choose]].',
      'The "Choose an animation API" page has a decision tree. From the top:\n• Art-based? A simple SVG uses AnimatedVectorDrawable; a complex one uses an outside library such as Lottie.\n• No, but repeating forever? Use `rememberInfiniteTransition`.\n• No, but animating a layout? Switching between different content: with Navigation-Compose use `composable()` with `enterTransition`/`exitTransition`, otherwise `AnimatedContent`, `Crossfade` or `Pager`. Appearing, disappearing: `AnimatedVisibility`, `CapturedAnimatedVisibility`, or `animateFloatAsState` + `Modifier.alpha()`. Size: `Modifier.animateContentSize`. Other layout properties such as offset or padding: see the several-properties branch. List items: `animateItem()`.\n• Not a layout, but several properties? Independent ones use `animate*AsState` (for Text: `TextMotion.Animated`); dependent ones that start together use `updateTransition`; ones that start at different times use `Animatable` with suspend calls.\n• One property: with a predefined target, `animate*AsState`; driven by a gesture, `Animatable` (`animateTo`/`snapTo`); a one-off without managed state, `AnimationState` or `animate` [[src:an-choose]].')
    B(C, S, 2, 'note', 'Cây có hai mục mới hơn: `CapturedAnimatedVisibility` (khi nội dung đang rời đi không cần "sống", chỉ cần ảnh chụp trạng thái lúc ra) và `TextMotion.Animated` cho Text. Site chưa giảng chi tiết hai mục này; hãy đọc trang tham chiếu của chúng trước khi dùng [[src:an-choose]].',
      'The tree has two newer items: `CapturedAnimatedVisibility` (when exiting content need not stay "alive", only a snapshot of its state at exit) and `TextMotion.Animated` for Text. The site does not teach these two in detail yet; read their reference pages before using them [[src:an-choose]].')
    B(C, S, 2, 'kind', 'source')
    B(C, S, 3, 'p', 'Mô phỏng ngay dưới đi theo cây với sáu nhu cầu hay gặp, và dẫn tới chương giảng API tương ứng.\nQuy tắc dễ nhớ: "có phải layout không?" là câu hỏi tách đôi cây hiệu quả nhất.',
      'The simulation just below walks the tree with six common needs, and leads to the chapter teaching each API.\nRule of thumb: "is this a layout?" is the question that splits the tree most usefully.')

    S = 'symptoms'
    a(C + '.sec.%s.title' % S, 'Chỉ mục triệu chứng', 'Symptom index')
    a(C + '.sec.%s.badge' % S, 'stable')
    B(C, S, 1, 'p', 'Gặp triệu chứng thì mở chương nào:\n• Box nhảy kích thước dù có `animateContentSize`: C5 (thứ tự modifier).\n• Hiệu ứng ẩn bị "cụt": C4 (animation nằm ngoài Transition).\n• Lệnh sau `animateTo` không chạy: C6 (CancellationException).\n• Nhấp nháy giật ở lượt cuối: IF (số lượt chẵn với Reverse).\n• Ảnh không bay giữa hai màn hình: SE (key, scope). Góc bo mất khi bay: SE (clip trước `sharedElement`).\n• AVD chạy ngược khi bấm lần hai: CV (Transition hai trạng thái).\n• Cả màn hình recompose mỗi frame: C7 và B7 (đọc ở phase draw).\n• Test luôn thấy frame đầu hoặc giá trị cuối: C8 (frame khởi động, `autoAdvance`).\n• Nút đã dời chỗ mà không bấm được (mã View cũ): VM (view animation).',
      'Which chapter to open for which symptom:\n• A Box jumps in size despite `animateContentSize`: C5 (modifier order).\n• A hide effect is "cut short": C4 (an animation outside the Transition).\n• Code after `animateTo` does not run: C6 (CancellationException).\n• A blink jerks on the last iteration: IF (an even count with Reverse).\n• An image does not fly between two screens: SE (keys, scope). Rounded corners vanish in flight: SE (clip before `sharedElement`).\n• An AVD plays backwards on the second tap: CV (a two-state Transition).\n• The whole screen recomposes every frame: C7 and B7 (read in the draw phase).\n• A test always sees the first frame or the final value: C8 (start-up frames, `autoAdvance`).\n• A moved button cannot be tapped (old View code): VM (view animation).')

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
