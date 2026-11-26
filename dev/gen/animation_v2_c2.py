# Animation v2 · C2 AnimationSpec (viết lại; giữ mục v1 'spring', 'more' và lab animation.spec)
# Nguồn: AnimationSpec.kt (vectorize, tween/spring/keyframes/snap/repeatable mặc định), Easing.kt (cubic-bezier), FloatDecayAnimationSpec.kt
# (friction −4.2), VectorConverters.kt, ColorVectorConverter.kt (Oklab, AnimationVector4D) @296313a4 (đọc lại 2026-11-23); "Customize animations";
# Essentials Ch.39.4 (spec và easing), 40.7 (spring), 40.8 (keyframes); Kunneth Ch.8 ("Understanding animation specifications").

SEC_ORDER = {'c2': ['hook', 'what', 'spring', 'easing', 'more', 'vectors', 'bugs', 'exercises', 'recall']}

def add(a):
    def B(ch, sec, n, field, vi, en=None):
        a('%s.sec.%s.b.%02d.%s' % (ch, sec, n, field), vi, vi if en is None else en)

    # ---------------- sim animation.vector ----------------
    m = lambda k, vi, en=None: a('m.vector.' + k, vi, en)
    m('title', 'Spec không biết kiểu: mọi thứ thành AnimationVector', 'A spec does not know types: everything becomes an AnimationVector')
    m('overview', 'Bốn giá trị được animate: một `Dp` với tween, một `Offset` với spring, một `Color` với tween và một `Float` với keyframes. Theo đường đi ở commit ghim: giá trị → `TwoWayConverter` → `AnimationVector` (1–4 chiều) → `VectorizedAnimationSpec` tính từng thành phần theo thời gian → đổi ngược về kiểu cũ.', 'Four animated values: a `Dp` with a tween, an `Offset` with a spring, a `Color` with a tween and a `Float` with keyframes. Follow the path at the pinned commit: value → `TwoWayConverter` → `AnimationVector` (1–4 dimensions) → a `VectorizedAnimationSpec` computes each component over time → converted back to the original type.')
    m('wrapup', '`AnimationSpec<T>` chỉ có một việc: `vectorize(converter)` thành một `VectorizedAnimationSpec<V>` làm việc trên vector số thực. Vì vậy cùng một `tween` dùng được cho Dp, Offset, Color hay kiểu của riêng bạn, miễn là có converter.\nMàu được animate trong không gian màu Oklab (bốn chiều: alpha, L, a, b), không phải RGB. Nhờ vậy đi từ đỏ sang trắng không phải đi qua những màu xỉn ở giữa.\nQuy tắc dễ nhớ: spec chỉ biết số; converter lo đổi kiểu của bạn thành số và ngược lại.',
      '`AnimationSpec<T>` has only one job: `vectorize(converter)` into a `VectorizedAnimationSpec<V>` that works on vectors of floats. That is why the same `tween` works for Dp, Offset, Color or your own type, as long as there is a converter.\nColours are animated in the Oklab colour space (four dimensions: alpha, L, a, b), not RGB. So red to white does not have to pass through muddy colours in between.\nRule of thumb: the spec only knows numbers; the converter turns your type into numbers and back.')
    m('simp.1', 'Giá trị giữa chừng: Dp và Color tính theo FastOutSlowIn tại 150/300 ms (fraction ≈ 0.776); Offset (spring) là số minh họa; keyframes nội suy tuyến tính (LinearEasing mặc định giữa các mốc).', 'Mid-way values: Dp and Color use FastOutSlowIn at 150/300 ms (fraction ≈ 0.776); Offset (spring) numbers are illustrative; keyframes interpolate linearly (LinearEasing is the default between marks).')
    m('simp.2', 'Toạ độ Oklab của đỏ và trắng tính theo công thức chuẩn của Oklab với sRGB; bộ chuyển đổi thật còn kẹp giá trị và đổi về color space đích.', 'The Oklab coordinates of red and white follow the standard Oklab formula from sRGB; the real converter also clamps values and converts back to the target colour space.')
    m('ctl.hint', 'Đổi kiểu giá trị và xem số chiều của vector.', 'Change the value type and watch the vector\'s dimension.')
    m('ctl.which', 'Giá trị được animate', 'Animated value')
    for k, vi, en in [('dp', 'Dp với tween', 'Dp with a tween'), ('offset', 'Offset với spring', 'Offset with a spring'), ('color', 'Color với tween (Oklab)', 'Color with a tween (Oklab)'), ('keyframes', 'Float với keyframes', 'Float with keyframes')]:
        m('ctl.which.' + k, vi, en)
    m('diagramTitle', 'Giá trị, converter, vector và spec', 'Value, converter, vector and spec')
    m('diagramDesc', 'Giá trị đi qua converter thành vector; spec tính vector theo thời gian; vector quay lại thành giá trị', 'The value goes through the converter into a vector; the spec computes the vector over time; the vector turns back into a value')
    for k, vi, en in [('value', 'Giá trị (kiểu T)', 'Value (type T)')]:
        m('n.' + k, vi, en)
    m('n.conv', 'TwoWayConverter (đổi hai chiều)', 'TwoWayConverter (both ways)')
    m('n.vec', 'AnimationVector (1–4 số)', 'AnimationVector (1–4 floats)')
    m('n.spec', 'Spec đã vector hóa', 'Vectorized spec')
    m('met.dim', 'Số chiều của vector', 'Vector dimensions')
    for k, vi, en in [('value', 'Giá trị', 'Value'), ('vector', 'Vector (đầu → cuối hoặc hiện tại)', 'Vector (start → end, or current)'), ('spec', 'Spec', 'Spec')]:
        m('st.' + k, vi, en)
    S = [
        ('intro.dp', 'Animate Dp từ 0 tới 100', 'Animating a Dp from 0 to 100', 'Tween 300 ms, easing FastOutSlowIn (mặc định của tween).', 'A 300 ms tween, FastOutSlowIn easing (the tween default).'),
        ('intro.offset', 'Animate Offset từ (0, 0) tới (100, 40)', 'Animating an Offset from (0, 0) to (100, 40)', 'Spring mặc định: damping 1 (không nảy), stiffness 1500.', 'A default spring: damping 1 (no bounce), stiffness 1500.'),
        ('intro.color', 'Animate Color từ đỏ sang trắng', 'Animating a Color from red to white', 'Tween 300 ms. Câu hỏi: màu giữa chừng tính trong không gian màu nào?', 'A 300 ms tween. The question: in which colour space is the mid-way colour computed?'),
        ('intro.keyframes', 'Animate Float bằng keyframes', 'Animating a Float with keyframes', 'Thời lượng 300 ms; 80 ở 100 ms, 60 ở 200 ms, kết thúc ở 100.', 'Duration 300 ms; 80 at 100 ms, 60 at 200 ms, ending at 100.'),
        ('convert.dp', 'Đổi Dp → AnimationVector1D', 'Converting Dp → AnimationVector1D', '`Dp.VectorConverter` biến 0.dp và 100.dp thành vector một chiều [0] và [100].', '`Dp.VectorConverter` turns 0.dp and 100.dp into one-dimensional vectors [0] and [100].'),
        ('convert.offset', 'Đổi Offset → AnimationVector2D', 'Converting Offset → AnimationVector2D', 'Hai chiều: x và y. Mỗi chiều có giá trị và vận tốc riêng.', 'Two dimensions: x and y. Each has its own value and velocity.'),
        ('convert.color', 'Color → AnimationVector4D trong Oklab', 'Color → AnimationVector4D in Oklab', 'Bộ chuyển đổi đổi màu sang Oklab và đóng gói (alpha, L, a, b): đỏ ≈ (1, .628, .225, .126), trắng = (1, 1, 0, 0).', 'The converter turns the colour into Oklab and packs (alpha, L, a, b): red ≈ (1, .628, .225, .126), white = (1, 1, 0, 0).'),
        ('convert.keyframes', 'Đổi Float → AnimationVector1D', 'Converting Float → AnimationVector1D', 'Một chiều; các mốc keyframes cũng được đổi sang vector.', 'One dimension; the keyframe marks are converted to vectors too.'),
        ('vectorize', 'spec.vectorize(converter)', 'spec.vectorize(converter)', 'AnimationSpec chỉ biết tạo ra một `VectorizedAnimationSpec` làm việc trên vector {n} chiều; nó không cần biết đó là Dp hay màu.', 'The AnimationSpec only knows how to produce a `VectorizedAnimationSpec` working on {n}-dimensional vectors; it does not need to know whether it is a Dp or a colour.'),
        ('frame.dp', 'Tại 150 ms: vector [77.6]', 'At 150 ms: vector [77.6]', 'Nửa thời gian nhưng đã đi 77.6%: FastOutSlowIn tăng tốc nhanh rồi chậm dần ở cuối.', 'Half the time but 77.6% of the way: FastOutSlowIn speeds up fast and slows down at the end.'),
        ('frame.offset', 'Giữa chừng: vector [60, 24]', 'Mid-way: vector [60, 24]', 'Mỗi thành phần chạy spring của riêng nó; với cùng tham số và cùng xuất phát từ đứng yên, hai thành phần đi cùng tỉ lệ.', 'Each component runs its own spring; with the same parameters and both starting at rest, the two components move in proportion.'),
        ('frame.color', 'Tại 150 ms: (1, .917, .050, .028)', 'At 150 ms: (1, .917, .050, .028)', 'Nội suy từng thành phần Oklab theo cùng fraction 0.776: độ sáng L tăng, a và b về 0.', 'Each Oklab component is interpolated at the same fraction 0.776: lightness L rises, a and b move towards 0.'),
        ('frame.keyframes', 'Tại 150 ms: vector [70]', 'At 150 ms: vector [70]', 'Giữa mốc 80 (100 ms) và 60 (200 ms), nội suy tuyến tính: 70.', 'Between the 80 (100 ms) and 60 (200 ms) marks, linear interpolation: 70.'),
        ('back.dp', 'Đổi ngược: vector → 77.6.dp', 'Back: vector → 77.6.dp', '`convertFromVector` cho lại Dp.', '`convertFromVector` gives back a Dp.'),
        ('back.offset', 'Đổi ngược: vector → Offset(60, 24)', 'Back: vector → Offset(60, 24)', 'Cho lại Offset.', 'Gives back an Offset.'),
        ('back.color', 'Vector → màu (Oklab → sRGB)', 'Vector → a colour (Oklab → sRGB)', 'Giá trị được kẹp vào khoảng hợp lệ rồi đổi từ Oklab về color space đích.', 'The values are clamped into range, then converted from Oklab back to the target colour space.'),
        ('back.keyframes', 'Vector → 70f', 'Vector → 70f', 'Cho lại Float.', 'Gives back a Float.'),
        ('end.dp', 'Kết thúc ở 100.dp', 'Ends at 100.dp', 'Một chiều, một đường cong.', 'One dimension, one curve.'),
        ('end.offset', 'Kết thúc ở Offset(100, 40)', 'Ends at Offset(100, 40)', 'Hai chiều chạy song song.', 'Two dimensions run side by side.'),
        ('end.color', 'Kết thúc ở trắng', 'Ends at white', 'Bốn chiều trong Oklab.', 'Four dimensions in Oklab.'),
        ('end.keyframes', 'Kết thúc ở 100f', 'Ends at 100f', 'Keyframes đi qua các mốc theo thời gian.', 'Keyframes pass through the marks over time.'),
    ]
    for sid, tv, te, xv, xe in S:
        m('s.%s.title' % sid, tv, te); m('s.%s.explain' % sid, xv, xe); m('ev.' + sid, tv, te)
    for k, vi, en in [
        ('oklab', '`ColorVectorConverter.kt` ở commit ghim: `color.convert(ColorSpaces.Oklab)` rồi `AnimationVector4D(alpha, l, a, b)`. [[src:an-colorconv-src]]', '`ColorVectorConverter.kt` at the pinned commit: `color.convert(ColorSpaces.Oklab)`, then `AnimationVector4D(alpha, l, a, b)`. [[src:an-colorconv-src]]'),
        ('vectorize', 'KDoc của `AnimationSpec`: hệ thống animation làm việc trên `AnimationVector`; spec mô tả cách vector đó chuyển động. [[src:an-spec-src]]', 'The `AnimationSpec` KDoc: the animation system operates on `AnimationVector`s; the spec describes how that vector should be animated. [[src:an-spec-src]]'),
        ('end.dp', '`tween()` mặc định: 300 ms, delay 0, `FastOutSlowInEasing` = cubic-bezier (0.4, 0, 0.2, 1) ở commit ghim. [[src:an-spec-src]] [[src:an-easing-src]]', '`tween()` defaults: 300 ms, delay 0, `FastOutSlowInEasing` = cubic-bezier (0.4, 0, 0.2, 1) at the pinned commit. [[src:an-spec-src]] [[src:an-easing-src]]'),
        ('end.offset', '`spring()` mặc định: `DampingRatioNoBouncy`, `StiffnessMedium`. [[src:an-spec-src]]', '`spring()` defaults: `DampingRatioNoBouncy`, `StiffnessMedium`. [[src:an-spec-src]]'),
        ('end.color', 'Nội suy trong Oklab là lựa chọn của bộ chuyển đổi màu, không phải của tween. [[src:an-colorconv-src]]', 'Interpolating in Oklab is the colour converter\'s choice, not the tween\'s. [[src:an-colorconv-src]]'),
        ('end.keyframes', 'Easing mặc định giữa các mốc keyframes là `LinearEasing`. [[src:an-spec-src]]', 'The default easing between keyframe marks is `LinearEasing`. [[src:an-spec-src]]')]:
        m('co.' + k, vi, en)
    a('cap.vector', 'Bốn khối: giá trị, converter, vector và spec đã vector hóa. Mũi tên từ spec vào vector là tính toán mỗi frame; mũi tên vòng về giá trị là đổi ngược kiểu.', 'Four blocks: the value, the converter, the vector and the vectorized spec. The arrow from the spec into the vector is the per-frame computation; the arrow looping back to the value is the conversion back.')

    # ---------------- chương C2 ----------------
    C = 'c2'
    a(C + '.sim.animation.vector', 'Kiểu, vector và spec', 'Types, vectors and specs')
    a(C + '.sim.animation.spec', 'Lab: so spec', 'Lab: comparing specs')

    S = 'hook'
    a(C + '.sec.%s.title' % S, 'Đoán trước khi đọc', 'Predict before reading')
    a(C + '.sec.%s.badge' % S, 'stable')
    B(C, S, 1, 'predict', '`tween(durationMillis = 300)` animate từ 0 tới 100. Ở 150 ms (nửa thời gian), giá trị là 50, nhỏ hơn 50, hay lớn hơn 50?', '`tween(durationMillis = 300)` animates from 0 to 100. At 150 ms (half the time), is the value 50, below 50, or above 50?')
    B(C, S, 1, 'ans', 'Lớn hơn 50, khoảng 77.6. Easing mặc định của tween là `FastOutSlowInEasing`, cubic-bezier (0.4, 0, 0.2, 1): tăng tốc nhanh, chậm dần ở cuối. Chỉ `LinearEasing` mới cho 50. Mô phỏng của chương tính đúng con số này. [[src:an-spec-src]] [[src:an-easing-src]]', 'Above 50, about 77.6. The tween\'s default easing is `FastOutSlowInEasing`, cubic-bezier (0.4, 0, 0.2, 1): it speeds up quickly and slows down at the end. Only `LinearEasing` would give 50. The chapter\'s simulation computes exactly this number. [[src:an-spec-src]] [[src:an-easing-src]]')

    S = 'what'
    a(C + '.sec.%s.title' % S, 'AnimationSpec là gì', 'What an AnimationSpec is')
    a(C + '.sec.%s.badge' % S, 'stable')
    B(C, S, 1, 'p', 'Cần tách hai chuyện. API animation (animate*AsState, Transition, AnimatedVisibility…) quyết định CÁI GÌ được animate, và khi nào. `AnimationSpec` quyết định giá trị đi THẾ NÀO theo thời gian. Mọi API cấp cao đều nhận một tham số spec. Ví dụ hay gặp: easing cho hiệu ứng hiện/ẩn, `spring` với damping và stiffness, `keyframes` để đi qua các mốc [[src:book-kunneth]] [[src:book-compose-ess]].\nCó hai họ spec. Spec theo thời lượng: tween, keyframes, snap, repeatable. Spec vật lý: spring, decay. Thêm `infiniteRepeatable`, không bao giờ kết thúc [[src:an-customize]].\nQuy tắc dễ nhớ: API là "cái gì, khi nào"; spec là "đi ra sao".',
      'Two things need separating. An animation API (animate*AsState, Transition, AnimatedVisibility…) decides WHAT is animated, and when. An `AnimationSpec` decides HOW the value travels over time. Every high-level API takes a spec parameter. Common examples: easing for show/hide effects, `spring` with damping and stiffness, `keyframes` to pass through marks [[src:book-kunneth]] [[src:book-compose-ess]].\nThere are two families of spec. Duration-based specs: tween, keyframes, snap, repeatable. Physics specs: spring, decay. Plus `infiniteRepeatable`, which never ends [[src:an-customize]].\nRule of thumb: the API is "what and when"; the spec is "how it travels".')

    S = 'easing'
    a(C + '.sec.%s.title' % S, 'Easing: thời gian tuyến tính, quãng đường không', 'Easing: linear time, non-linear distance')
    a(C + '.sec.%s.badge' % S, 'impl')
    B(C, S, 1, 'p', 'Một tween chia thời gian đều: phần thời gian đã trôi t đi từ 0 tới 1. Easing biến "phần thời gian" thành "phần quãng đường": ví dụ chạy nhanh lúc đầu rồi chậm dần khi gần tới đích.\nỞ commit ghim, ba easing chuẩn là đường cong cubic-bezier: `FastOutSlowInEasing` (0.4, 0, 0.2, 1), `LinearOutSlowInEasing` (0, 0, 0.2, 1), `FastOutLinearInEasing` (0.4, 0, 1, 1). `LinearEasing` thì giữ nguyên. Với một phần thời gian x, đường cubic-bezier tìm tham số u sao cho x(u) = x, rồi trả về y(u). Đó là cách mô phỏng tính ra 0.776 tại x = 0.5 [[src:an-easing-src]].\nQuy tắc dễ nhớ: easing không đổi THỜI LƯỢNG, chỉ đổi NHỊP đi trong khoảng thời lượng đó.',
      'A tween divides time evenly: the elapsed time fraction t goes from 0 to 1. Easing turns "fraction of time" into "fraction of distance": for example moving fast at first, then slowing as it nears the target.\nAt the pinned commit, the three standard easings are cubic-bezier curves: `FastOutSlowInEasing` (0.4, 0, 0.2, 1), `LinearOutSlowInEasing` (0, 0, 0.2, 1), `FastOutLinearInEasing` (0.4, 0, 1, 1). `LinearEasing` leaves it unchanged. For a time fraction x, a cubic-bezier curve finds the parameter u where x(u) = x, then returns y(u). That is how the simulation gets 0.776 at x = 0.5 [[src:an-easing-src]].\nRule of thumb: easing does not change the DURATION, only the RHYTHM within it.')

    S = 'vectors'
    a(C + '.sec.%s.title' % S, 'Dưới mui xe: AnimationVector và TwoWayConverter', 'Under the hood: AnimationVector and TwoWayConverter')
    a(C + '.sec.%s.badge' % S, 'impl')
    B(C, S, 1, 'p', 'Interface `AnimationSpec<T>` ở commit ghim chỉ có một hàm: `vectorize(converter: TwoWayConverter<T, V>): VectorizedAnimationSpec<V>`. KDoc giải thích: hệ thống animation làm việc trên `AnimationVector`; giá trị kiểu T được đổi sang vector để animate.\nCó sẵn converter cho Float, Int, Dp (1 chiều), Offset, Size, DpOffset (2 chiều), Rect (4 chiều)…; màu dùng `AnimationVector4D` trong không gian Oklab. Mô phỏng ngay dưới đi qua bốn kiểu [[src:an-spec-src]] [[src:an-vectorconv-src]] [[src:an-colorconv-src]].',
      'The `AnimationSpec<T>` interface at the pinned commit has just one function: `vectorize(converter: TwoWayConverter<T, V>): VectorizedAnimationSpec<V>`. The KDoc explains: the animation system works on `AnimationVector`s; a value of type T is converted into a vector to be animated.\nThere are built-in converters for Float, Int, Dp (1 dimension), Offset, Size, DpOffset (2 dimensions), Rect (4 dimensions)…; colours use an `AnimationVector4D` in the Oklab space. The simulation just below walks through four types [[src:an-spec-src]] [[src:an-vectorconv-src]] [[src:an-colorconv-src]].')
    B(C, S, 2, 'note', 'Mỗi thành phần có giá trị và vận tốc riêng. Vì vậy một spring hai chiều không phải "một chuyển động cong": x và y là hai lò xo độc lập.\nMuốn một đường cong có chủ đích (cung tròn), `keyframes` có `using(ArcMode)` cho Offset, theo KDoc của `keyframes` [[src:an-spec-src]].',
      'Each component has its own value and velocity. So a two-dimensional spring is not "one curved motion": x and y are two independent springs.\nFor an intentional curved path (an arc), `keyframes` offers `using(ArcMode)` for Offsets, per the `keyframes` KDoc [[src:an-spec-src]].')
    B(C, S, 2, 'kind', 'mechanism')

    S = 'bugs'
    a(C + '.sec.%s.title' % S, 'Bug thường gặp', 'Common bugs')
    a(C + '.sec.%s.badge' % S, 'stable')
    B(C, S, 1, 'bug', 'Animation đổi màu từ xanh sang đỏ trông "khác" so với bản thiết kế làm bằng công cụ nội suy RGB.', 'A blue-to-red colour animation looks "different" from a design made with a tool that interpolates in RGB.')
    B(C, S, 1, 'cause', 'Compose nội suy màu trong Oklab (bộ chuyển đổi màu), không phải RGB, nên màu giữa chừng khác.', 'Compose interpolates colours in Oklab (the colour converter), not RGB, so the mid-way colours differ.')
    B(C, S, 1, 'fix', 'Chấp nhận (Oklab thường cho màu giữa đẹp hơn), hoặc dùng `animateValueAsState` với một `TwoWayConverter` tự viết nội suy theo RGB nếu thiết kế bắt buộc. [[src:an-colorconv-src]]', 'Accept it (Oklab usually gives nicer mid-way colours), or use `animateValueAsState` with a custom `TwoWayConverter` interpolating in RGB if the design requires it. [[src:an-colorconv-src]]')
    B(C, S, 2, 'bug', 'Đổi `tween` sang `spring` thì animation "không còn 300 ms" và test chờ 300 ms thất bại.', 'Switching from `tween` to `spring` means the animation "is no longer 300 ms", and a test waiting 300 ms fails.')
    B(C, S, 2, 'cause', 'Spring không có thời lượng cố định: nó kết thúc khi giá trị đủ gần target (ngưỡng hiển thị) và vận tốc đủ nhỏ.', 'A spring has no fixed duration: it ends when the value is close enough to the target (the visibility threshold) and the velocity is small enough.')
    B(C, S, 2, 'fix', 'Trong test, để `mainClock` tự chạy tới khi idle, hoặc dùng tween khi thật cần thời lượng xác định (C8). [[src:an-testing]]', 'In tests, let `mainClock` advance until idle, or use a tween when a fixed duration is really needed (C8). [[src:an-testing]]')

    S = 'exercises'
    a(C + '.sec.%s.title' % S, 'Bài tập', 'Exercises')
    a(C + '.sec.%s.badge' % S, 'stable')
    B(C, S, 1, 'ex', 'Viết keyframes cho một Float đi 0 → 100 trong 600 ms, đứng yên ở 50 từ 200 ms tới 400 ms, và đoạn cuối dùng `FastOutSlowInEasing`.', 'Write keyframes for a Float going 0 → 100 in 600 ms, holding at 50 from 200 ms to 400 ms, with `FastOutSlowInEasing` for the last stretch.')
    B(C, S, 1, 'hint', 'Một mốc có thể gắn easing cho đoạn BẮT ĐẦU từ nó: `50f at 400 using FastOutSlowInEasing`.', 'A mark can carry the easing for the stretch STARTING at it: `50f at 400 using FastOutSlowInEasing`.')
    B(C, S, 1, 'solkt', 'animateFloatAsState(\n    targetValue = if (go) 100f else 0f,\n    animationSpec = keyframes {\n        durationMillis = 600\n        50f at 200\n        50f at 400 using FastOutSlowInEasing\n    },\n    label = "hold"\n)')
    B(C, S, 1, 'sol', 'Giữa 200 và 400 hai mốc bằng nhau nên giá trị đứng yên; đoạn 400 → 600 dùng easing gắn ở mốc 400; đoạn 0 → 200 dùng `LinearEasing` mặc định.', 'Between 200 and 400 the two marks are equal, so the value holds; the 400 → 600 stretch uses the easing attached at 400; the 0 → 200 stretch uses the default `LinearEasing`.')
    B(C, S, 2, 'ex', 'Một `Rect` được animate bằng spring. Vector có mấy chiều, và có mấy "lò xo" độc lập?', 'A `Rect` is animated with a spring. How many dimensions does the vector have, and how many independent "springs"?')
    B(C, S, 2, 'sol', '`Rect.VectorConverter` dùng `AnimationVector4D` (left, top, right, bottom): bốn thành phần, mỗi cái một lò xo với giá trị và vận tốc riêng.', '`Rect.VectorConverter` uses an `AnimationVector4D` (left, top, right, bottom): four components, each a spring with its own value and velocity.')

    S = 'recall'
    a(C + '.sec.%s.title' % S, 'Tự trả lời', 'Answer it yourself')
    a(C + '.sec.%s.badge' % S, 'stable')
    B(C, S, 1, 'ask', 'AnimationSpec<T> làm việc trên kiểu T thế nào?', 'How does an AnimationSpec<T> work on type T?')
    B(C, S, 1, 'ans', 'Không trực tiếp: vectorize(converter) tạo spec làm việc trên AnimationVector; converter đổi T qua lại.', 'Not directly: vectorize(converter) creates a spec working on AnimationVectors; the converter translates T both ways.')
    B(C, S, 2, 'ask', 'Màu được nội suy trong không gian nào?', 'In which space are colours interpolated?')
    B(C, S, 2, 'ans', 'Oklab, dưới dạng AnimationVector4D (alpha, L, a, b).', 'Oklab, as an AnimationVector4D (alpha, L, a, b).')
    for q, qv, qe, av, ae, wv, we in [
        ('q3', 'tween 300 ms với easing mặc định, ở 150 ms đi được bao nhiêu?', 'A 300 ms tween with the default easing: how far along is it at 150 ms?',
         'Khoảng 77.6%.', 'About 77.6%.', 'FastOutSlowInEasing (0.4, 0, 0.2, 1) tại x = 0.5.', 'FastOutSlowInEasing (0.4, 0, 0.2, 1) at x = 0.5.'),
        ('q4', 'Easing mặc định giữa các mốc keyframes?', 'The default easing between keyframe marks?',
         'LinearEasing.', 'LinearEasing (linear).', 'Theo KeyframesSpec ở commit ghim.', 'Per KeyframesSpec at the pinned commit.')]:
        a(C + '.quiz.%s.q' % q, qv, qe); a(C + '.quiz.%s.a' % q, av, ae); a(C + '.quiz.%s.why' % q, wv, we)

def override(o):
    C = 'c2'
    o(C + '.essence',
      'API animation quyết định CÁI GÌ chuyển động; `AnimationSpec` quyết định chuyển động THẾ NÀO theo thời gian: spring (vật lý, giữ vận tốc, không có thời lượng cố định), tween (thời lượng và easing), keyframes (đi qua các mốc), repeatable/infiniteRepeatable, snap, decay.\n'
      'Dưới mui xe, ở commit ghim, mọi spec làm việc trên `AnimationVector`: giá trị kiểu nào cũng được một `TwoWayConverter` đổi sang vector 1–4 chiều, spec tính từng thành phần theo thời gian, rồi đổi ngược. Màu được nội suy trong Oklab.\n'
      'Hằng số (300 ms, FastOutSlowIn, damping/stiffness mặc định, friction của decay) lấy từ API reference và mã ở commit ghim, không từ trí nhớ.',
      'The animation API decides WHAT moves; the `AnimationSpec` decides HOW it moves over time: spring (physical, keeps velocity, no fixed duration), tween (duration and easing), keyframes (passing through marks), repeatable/infiniteRepeatable, snap, decay.\n'
      'Under the hood, at the pinned commit, every spec works on `AnimationVector`s: a value of any type is turned by a `TwoWayConverter` into a 1–4-dimensional vector, the spec computes each component over time, then converts back. Colours are interpolated in Oklab.\n'
      'Constants (300 ms, FastOutSlowIn, the default damping/stiffness, the decay friction) come from the API reference and the code at the pinned commit, not from memory.')
    o(C + '.goal.g1', 'Đã thấy giá trị được đổi sang AnimationVector', 'Saw the value converted to an AnimationVector')
    o(C + '.goal.g2', 'Đã chạy một kiểu giá trị tới cuối', 'Ran one value type to the end')
    o(C + '.sec.spring.p.2', '`tween()` mặc định: `DefaultDurationMillis` = 300 ms, không delay, `FastOutSlowInEasing`. [[src:an-constants]] [[src:an-pkg]] Theo mã nguồn (ghim androidx-main commit 296313a4, đọc lại 2026-11-23), `FastOutSlowInEasing` là cubic-bezier (0.4, 0, 0.2, 1), `LinearOutSlowInEasing` (0, 0, 0.2, 1), `FastOutLinearInEasing` (0.4, 0, 1, 1). [[badge:impl]] [[src:an-easing-src]]',
      '`tween()` defaults: `DefaultDurationMillis` = 300 ms, no delay, `FastOutSlowInEasing`. [[src:an-constants]] [[src:an-pkg]] According to the source (pinned androidx-main commit 296313a4, re-read 2026-11-23), `FastOutSlowInEasing` is cubic-bezier (0.4, 0, 0.2, 1), `LinearOutSlowInEasing` (0, 0, 0.2, 1), `FastOutLinearInEasing` (0.4, 0, 1, 1). [[badge:impl]] [[src:an-easing-src]]')
    o('lab.simp.2', 'Spring là dao động điều hòa tắt dần với khối lượng 1: ω0 = √stiffness, hệ số tắt 2·ζ·ω0, ba nghiệm cho ζ < 1, ζ = 1, ζ > 1. Tween dùng cubic-bezier; keyframes nội suy tuyến tính giữa các mốc. Decay theo công thức của `FloatExponentialDecaySpec` (ghim androidx-main commit 296313a4: friction = −4.2 × frictionMultiplier). [[badge:simplified]] [[src:an-decay-src]]',
      'Spring is a damped harmonic oscillator with mass 1: ω0 = √stiffness, damping coefficient 2·ζ·ω0, three solutions for ζ < 1, ζ = 1, ζ > 1. Tween uses cubic-bezier; keyframes interpolate linearly between marks. Decay follows the `FloatExponentialDecaySpec` formula (pinned androidx-main commit 296313a4: friction = −4.2 × frictionMultiplier). [[badge:simplified]] [[src:an-decay-src]]')
