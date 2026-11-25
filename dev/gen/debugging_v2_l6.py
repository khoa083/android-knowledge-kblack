# Gỡ lỗi và hiệu năng · l6: Layout Inspector (Phần 2: nhìn vào bên trong app)
# Nguồn (chỉ ghi ở đây và docs/research/debugging.md), đọc 2026-11-25, các trang không ghi ngày: developer.android.com/studio/debug/layout-inspector
# (Component Tree theo thời gian thực, Attributes, có thể cần khởi động lại Activity để đọc thuộc tính, Deep Inspect: chuột phải một vùng để thấy mọi
# thành phần ở đó, Show Only Subtree/Parents, cập nhật trực tiếp, đếm recomposition và skip của Compose, xuất/nhập snapshot, chế độ nhúng),
# develop/ui/compose/touch-input/pointer-input/understand-gestures (hit test theo bounds; giữa các anh em chỉ cái z cao nhất, vẽ trên cùng, được "hit";
# clickable, Button tự consume), develop/ui/views/touch-and-input/gestures/viewgroup (onInterceptTouchEvent, cha thấy sự kiện trước con).
# Màn đặt lịch với lớp phủ đang tải đặt alpha 0 mà vẫn clickable là ví dụ của site.

SEC_ORDER = {'l6': ['hook', 'tree', 'hit', 'overlap', 'counts', 'bugs', 'ex', 'recall']}


def add(a):
    def B(ch, sec, n, field, vi, en=None):
        a('%s.sec.%s.b.%02d.%s' % (ch, sec, n, field), vi, vi if en is None else en)

    a('preset.layout', '''Gỡ lỗi · nút bấm không ăn vì bị che''', '''Debugging · a button that ignores taps because it is covered''')
    m = lambda k, vi, en=None: a('m.layout.' + k, vi, en)
    m('title', '''Nút "Đặt lịch" bấm không ăn''', '''The "Book" button ignores taps''')
    m('overview', '''Trên màn đặt lịch của app Hẹn Khám, bấm nút "Đặt lịch" không có gì xảy ra, dù nút hiện rõ. Cách 1 đoán lỗi nằm ở nút và sửa nút. Cách 2 dùng Layout Inspector để hỏi: tại đúng điểm chạm có những thành phần nào, cái nào được vẽ trên cùng, thuộc tính của nó là gì. Thành phần nhận cú chạm được tính thật bằng hit test trên cây giao diện của màn.''',
      '''On ClinicBook\'s booking screen, tapping "Book" does nothing, although the button is clearly visible. Way 1 guesses the bug is in the button and changes the button. Way 2 uses Layout Inspector to ask: which components are at exactly the tap point, which one is drawn on top, what are its attributes. The component that receives the tap is really computed by hit testing the screen\'s UI tree.''')
    m('wrapup', '''Nút không hỏng: một lớp phủ "đang tải" phủ kín màn hình, alpha bằng 0 nên không thấy, nhưng vẫn clickable và được vẽ sau nên nằm trên. Mọi cú chạm rơi vào nó. Sửa nút bao nhiêu cũng vô ích; chỉ đặt lớp phủ vào cây khi thật sự đang tải thì cú chạm về đúng nút.''',
      '''The button is not broken: a "loading" overlay covers the whole screen, with alpha 0 so it is invisible, but still clickable and drawn later, so it sits on top. Every tap lands on it. No amount of changing the button helps; putting the overlay in the tree only while actually loading sends the tap back to the button.''')
    m('simp.1', '''Cây giao diện rút gọn còn 7 thành phần; kích thước tính bằng dp trên màn 360 × 800.''', '''The UI tree is trimmed to 7 components; sizes are in dp on a 360 × 800 screen.''')
    m('simp.2', '''Thành phần nhận cú chạm được tính thật bằng JavaScript: trong các thành phần có bounds chứa điểm chạm, lấy cái vẽ sau cùng (z cao nhất) có xử lý chạm. Đoạn Compose chỉ để minh họa.''',
      '''The component receiving the tap is really computed in JavaScript: among the components whose bounds contain the tap point, take the last drawn (highest z) that handles touch. The Compose code is illustrative.''')
    m('ctl.hint', '''Chọn cách tìm lỗi rồi đi qua bốn bước; xem hình chữ nhật nào sáng lên tại điểm chạm.''', '''Pick a way of hunting the bug and walk the four steps; watch which rectangle lights up at the tap point.''')
    m('ctl.case', '''Cách tìm lỗi''', '''How the bug is hunted''')
    m('ctl.case.guess', '''đoán lỗi ở nút''', '''guess the button is at fault'''); m('ctl.case.inspect', '''xem cây giao diện bằng Layout Inspector''', '''look at the UI tree with Layout Inspector''')
    m('diagramTitle', '''Cú chạm đi tới đâu''', '''Where a tap goes''')
    m('diagramDesc', '''Hit test tìm thành phần vẽ trên cùng tại điểm chạm; nó nhận và tiêu thụ cú chạm''', '''Hit testing finds the top-most component at the tap point; it receives and consumes the tap''')
    for k, vi, en in [('tap', 'Cú chạm tại (180, 624)', 'A tap at (180, 624)'), ('hit', 'Hit test: vẽ trên cùng thắng', 'Hit test: top-most wins'), ('overlay', 'Lớp phủ đang tải (alpha 0)', 'Loading overlay (alpha 0)'),
                      ('button', 'Nút "Đặt lịch"', 'The "Book" button'), ('inspector', 'Layout Inspector: xem cây', 'Layout Inspector: the tree')]:
        m('n.' + k, vi, en)
    m('met.under', '''Thành phần xử lý chạm dưới điểm chạm''', '''Touch-handling components under the tap'''); m('met.hit', '''Nhận cú chạm''', '''Receives the tap''')
    m('met.booked', '''Lịch được đặt''', '''Bookings made'''); m('met.cause', '''Nguyên nhân''', '''Cause''')
    for k, vi, en in [('overlay', 'lớp phủ đang tải', 'the loading overlay'), ('button', 'nút "Đặt lịch"', 'the "Book" button')]:
        m('hit.' + k, vi, en)
    for k, vi, en in [('none', 'chưa biết', 'unknown'), ('button', 'đoán: lỗi ở nút', 'guess: the button'), ('overlay', 'lớp phủ trong suốt vẫn nhận chạm', 'an invisible overlay still takes taps'), ('fixed', 'đã sửa', 'fixed')]:
        m('cause.' + k, vi, en)
    a('cap.layout', '''Cú chạm đi qua hit test; thành phần vẽ trên cùng tại điểm đó nhận nó. Ô đỏ: thứ đang lấy mất cú chạm.''', '''A tap goes through hit testing; the top-most component at that point receives it. A red box: what is stealing the tap.''')
    S = [
        ('guess', 's1', 'Bấm "Đặt lịch": không có gì xảy ra', 'Tap "Book": nothing happens',
         'Nút hiện rõ, đúng màu, đúng chữ. Bấm vào giữa nút, không đặt được lịch, không có lỗi trong Logcat. Ai cũng nghĩ ngay tới onClick của nút.',
         'The button is clearly visible, right colour, right text. Tap its centre: no booking, no error in Logcat. Everyone thinks of the button\'s onClick straight away.'),
        ('guess', 's2', 'Thêm log vào onClick: không dòng nào được in', 'Add a log to onClick: not a single line printed',
         'Log.d trong onClick không bao giờ chạy. Điều này đã là manh mối: cú chạm không hề tới nút. Nhưng người sửa kết luận onClick bị "mất" và gắn lại nó.',
         'The Log.d in onClick never runs. That is already a clue: the tap never reaches the button. But the editor concludes onClick was "lost" and wires it up again.'),
        ('guess', 's3', 'Phóng to nút: vẫn không ăn', 'Make the button bigger: still nothing',
         'Nghĩ vùng chạm quá nhỏ, người sửa tăng chiều cao nút từ 48 lên 64 dp. Bấm ở đâu trên nút cũng vậy, vì toàn bộ nút vẫn nằm dưới một thứ khác.',
         'Thinking the touch area is too small, the editor raises the button from 48 to 64 dp. Tapping anywhere on it gives the same result, because the whole button is still under something else.'),
        ('guess', 's4', 'Ba giờ sửa nút, nút chưa từng hỏng', 'Three hours on the button, which was never broken',
         'Mọi thay đổi đều nhắm vào nút, mà nút chưa từng nhận được cú chạm nào. Câu hỏi đúng là "cú chạm đang đi tới đâu", và nút không trả lời được câu đó.',
         'Every change targeted the button, which never received a single tap. The right question is "where is the tap going", and the button cannot answer it.'),
        ('inspect', 's1', 'Chọn vùng tại điểm chạm: có hai thành phần', 'Select the region at the tap point: there are two components',
         'Trong Layout Inspector, xem mọi thành phần chồng lên nhau tại điểm (180, 624). Ngoài nút "Đặt lịch" còn một Box phủ kín màn hình: LoadingOverlay.',
         'In Layout Inspector, list every component overlapping at the point (180, 624). Besides the "Book" button there is a Box covering the whole screen: LoadingOverlay.'),
        ('inspect', 's2', 'Thuộc tính của lớp phủ: alpha 0, 360 × 800, clickable', 'The overlay\'s attributes: alpha 0, 360 × 800, clickable',
         'Bảng thuộc tính cho thấy lớp phủ đang có alpha 0 (trong suốt hoàn toàn) nhưng vẫn ở trong cây, vẫn chiếm cả màn, và có clickable để chặn chạm lúc đang tải.',
         'The attributes show the overlay with alpha 0 (fully transparent) but still in the tree, still covering the whole screen, and carrying clickable to block taps while loading.'),
        ('inspect', 's3', 'Nó được vẽ sau nên nằm trên và nhận cú chạm', 'It is drawn later, so it sits on top and takes the tap',
         'Trong Box, con khai báo sau được vẽ sau, nằm trên con trước. Hit test chọn thành phần vẽ trên cùng tại điểm chạm, tức lớp phủ; nó tiêu thụ cú chạm, nút bên dưới không nhận được gì. Alpha không ảnh hưởng tới hit test.',
         'In a Box, a child declared later is drawn later, on top of earlier ones. Hit testing picks the top-most component at the tap point, the overlay; it consumes the tap, and the button below gets nothing. Alpha does not affect hit testing.'),
        ('inspect', 's4', 'Sửa: chỉ đặt lớp phủ vào cây khi đang tải', 'Fix: put the overlay in the tree only while loading',
         'Thay vì đổi alpha, viết if (state.loading) LoadingOverlay(). Không tải thì lớp phủ không có trong cây, dưới điểm chạm chỉ còn nút, và bấm là đặt được lịch.',
         'Instead of changing alpha, write if (state.loading) LoadingOverlay(). When not loading the overlay is not in the tree, only the button is under the tap, and tapping books.'),
    ]
    for case, k, tv, te, xv, xe in S:
        sid = case + '.' + k
        m('s.%s.title' % sid, tv, te); m('s.%s.explain' % sid, xv, xe); m('ev.' + sid, tv, te)
    for k, vi, en in [
        ('try', '''Mẹo đọc: khung bên trái là màn hình với bounds của từng thành phần, chấm đỏ là điểm chạm; bảng bên dưới là cây thành phần theo thứ tự vẽ. Thành phần sáng lên là cái nhận cú chạm.''',
         '''Reading tip: the frame on the left is the screen with each component\'s bounds, the red dot is the tap point; the table below is the component tree in drawing order. The lit component is the one receiving the tap.'''),
        ('guess.s2', '''Log không in ra là một kết quả đo, không phải một trở ngại. Nó loại được giả thuyết "onClick chạy nhưng làm sai", như vòng gỡ lỗi ở chương "Quy trình gỡ lỗi, adb và bug report".''',
         '''A log that never prints is a measurement, not an obstacle. It rules out "onClick runs but does the wrong thing", as in the debugging loop of "The debugging process, adb and bug reports".'''),
        ('guess.s3', '''Trong Compose, hit test đi từ gốc xuống; giữa các thành phần anh em chồng nhau, chỉ cái có z cao nhất, tức vẽ trên cùng, được hit. [[src:ad-compose-gestures]]''',
         '''In Compose, hit testing goes from the root down; among overlapping siblings, only the one with the highest z, drawn on top, is hit. [[src:ad-compose-gestures]]'''),
        ('guess.s4', '''Khi triệu chứng là "không có gì xảy ra", hỏi xem sự kiện có tới nơi không trước khi hỏi nó được xử lý thế nào.''',
         '''When the symptom is "nothing happens", ask whether the event arrives before asking how it is handled.'''),
        ('inspect.s1', '''Layout Inspector hiện cây giao diện theo thời gian thực; ở chế độ Deep Inspect, chọn một vùng để xem mọi thành phần ở đó, kể cả thành phần nằm sau thành phần khác. [[src:ad-layout-inspector]]''',
         '''Layout Inspector shows the UI hierarchy in real time; in Deep Inspect mode, select a region to see every component there, including ones behind others. [[src:ad-layout-inspector]]'''),
        ('inspect.s2', '''Chọn một thành phần trong cây hay trên hình thì bảng thuộc tính hiện thuộc tính bố cục của nó. Có khi phải khởi động lại Activity mới đọc được thuộc tính. [[src:ad-layout-inspector]]''',
         '''Selecting a component in the tree or the rendering shows its layout attributes. Sometimes the Activity must restart before attributes can be read. [[src:ad-layout-inspector]]'''),
        ('inspect.s3', '''Thành phần gesture có sẵn như clickable và Button tự tiêu thụ sự kiện; ví dụ ở hai Button chồng nhau trong một Box, chỉ cái vẽ trên cùng nhận sự kiện chạm. [[src:ad-compose-gestures]]''',
         '''Built-in gesture components such as clickable and Button consume events themselves; in the example of two overlapping Buttons in a Box, only the one drawn on top receives pointer events. [[src:ad-compose-gestures]]'''),
        ('inspect.s4', '''Không có trong cây thì không thể nhận chạm. Ẩn bằng alpha chỉ đổi cách vẽ, không đổi việc ai đứng ở đó.''',
         '''What is not in the tree cannot take taps. Hiding with alpha only changes drawing, not who is standing there.'''),
    ]:
        m('co.' + k, vi, en)

    z = lambda k, vi, en=None: a('vz.' + k, vi, en)
    z('tab.layout', '''Màn hình và cây thành phần''', '''Screen and component tree''')
    z('ly.aria', '''Màn hình 360 × 800 với bounds của từng thành phần; điểm chạm (180, 624) rơi vào {h}''', '''A 360 × 800 screen with each component\'s bounds; the tap at (180, 624) lands on {h}''')
    z('ly.col.name', '''Thành phần (theo thứ tự vẽ)''', '''Component (in drawing order)'''); z('ly.col.bounds', '''Bounds (dp)''', '''Bounds (dp)''')
    z('ly.col.alpha', '''alpha''', '''alpha'''); z('ly.col.click', '''Xử lý chạm''', '''Handles taps''')
    for k, vi, en in [('guess.0', 'Bấm vào giữa nút: không có gì.', 'Tap the centre of the button: nothing.'),
                      ('guess.1', 'Thêm Log.d vào onClick: không dòng nào in ra.', 'Add Log.d to onClick: nothing prints.'),
                      ('guess.2', 'Nút cao lên 64 dp (bảng bên dưới), cú chạm vẫn rơi vào lớp phủ.', 'The button grows to 64 dp (table below); the tap still lands on the overlay.'),
                      ('guess.3', 'Chưa ai nhìn cây giao diện; lớp phủ vẫn ở đó.', 'Nobody has looked at the UI tree; the overlay is still there.'),
                      ('inspect.0', 'Chọn vùng tại điểm chạm: các hàng có viền là thành phần dưới điểm đó.', 'Select the region at the tap point: the outlined rows are under it.'),
                      ('inspect.1', 'Thuộc tính của lớp phủ: alpha 0, phủ kín màn, có xử lý chạm.', 'The overlay\'s attributes: alpha 0, full screen, handles taps.'),
                      ('inspect.2', 'Lớp phủ đứng sau Column trong cây nên được vẽ trên và nhận cú chạm.', 'The overlay comes after the Column in the tree, so it is drawn on top and takes the tap.'),
                      ('inspect.3', 'Lớp phủ không còn trong cây; cú chạm về nút.', 'The overlay is no longer in the tree; the tap reaches the button.')]:
        z('ly.note.' + k, vi, en)
    z('ly.yes', '''có''', '''yes'''); z('ly.no', '''không''', '''no''')
    z('ly.gone', '''(không có trong cây)''', '''(not in the tree)''')
    z('ly.sub', '''Dưới điểm chạm có {n} thành phần xử lý chạm; nhận cú chạm: {h}.''', '''Under the tap: {n} touch-handling components; the tap goes to: {h}.''')
    z('ly.legend', '''Chấm đỏ: điểm chạm. Khung nét đứt: thành phần trong suốt. Đỏ: thành phần đang nhận cú chạm thay cho nút. Xanh: nút nhận được cú chạm.''',
      '''Red dot: the tap point. Dashed frame: a transparent component. Red: the component taking the tap instead of the button. Green: the button gets the tap.''')

    C = 'l6'
    a(C + '.title', '''Layout Inspector: xem cây giao diện''', '''Layout Inspector: looking at the UI tree''')
    a(C + '.essence', '''Layout Inspector cho bạn xem cây giao diện của app đang chạy: mọi thành phần, bounds (vị trí và kích thước), thuộc tính, và với Compose là số lần recompose và skip. Nó trả lời những câu mà nhìn màn hình không trả lời được: cái gì đang che cái gì, thành phần nào thật sự ở điểm này, thuộc tính đang là bao nhiêu.\nCú chạm đi tới thành phần được vẽ trên cùng tại điểm chạm mà có xử lý chạm. Một lớp trong suốt (alpha 0) vẫn đứng đó và vẫn nhận chạm; alpha chỉ đổi cách vẽ.\nKhi triệu chứng là "bấm không có gì xảy ra", hỏi trước: cú chạm có tới đúng thành phần không. Layout Inspector cho thấy mọi thành phần chồng lên nhau ở một điểm.''',
      '''Layout Inspector lets you see the UI tree of the running app: every component, its bounds (position and size), its attributes, and for Compose the recomposition and skip counts. It answers questions the screen alone cannot: what is covering what, which component is really at this point, what an attribute currently is.\nA tap goes to the top-most component at the tap point that handles touch. A transparent layer (alpha 0) is still there and still takes taps; alpha only changes drawing.\nWhen the symptom is "tapping does nothing", first ask whether the tap reaches the right component. Layout Inspector shows every component overlapping at a point.''')
    a(C + '.goal.g1', '''Đã thấy hai thành phần chồng tại điểm chạm''', '''Saw two components overlapping at the tap point''')
    a(C + '.goal.g2', '''Đã thấy cú chạm về đúng nút''', '''Saw the tap reach the button''')
    a(C + '.sim.debugging.layout', '''đoán lỗi ở nút, hay xem cây giao diện''', '''guess the button, or look at the UI tree''')

    S_ = 'hook'
    a(C + '.sec.%s.title' % S_, '''Đoán trước khi đọc''', '''Predict before reading''')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'predict', '''Nút "Đặt lịch" hiện rõ, nhưng bấm không có gì xảy ra, và Log.d đặt trong onClick không bao giờ in. Bạn sẽ sửa nút, hay đi tìm thứ gì khác trước?''',
      '''The "Book" button is clearly visible, but tapping it does nothing, and a Log.d inside onClick never prints. Would you fix the button, or look for something else first?''')
    B(C, S_, 1, 'ans', '''Tìm thứ khác: onClick không chạy nghĩa là cú chạm không tới nút. Ở đây một lớp phủ trong suốt nằm trên và nhận mọi cú chạm. Mô phỏng ngay dưới so việc sửa nút với việc xem cây giao diện tại điểm chạm.''',
      '''Look for something else: onClick not running means the tap never reaches the button. Here a transparent overlay sits on top and takes every tap. The simulation just below compares fixing the button with looking at the UI tree at the tap point.''')

    S_ = 'tree'
    a(C + '.sec.%s.title' % S_, '''Layout Inspector cho thấy gì''', '''What Layout Inspector shows''')
    a(C + '.sec.%s.badge' % S_, 'version')
    B(C, S_, 1, 'p', '''Layout Inspector gắn vào app đang chạy (bản debug) và hiện ba thứ. Cây thành phần: cấu trúc giao diện theo thời gian thực, cả View lẫn Compose. Bảng thuộc tính: thuộc tính bố cục của thành phần đang chọn, như kích thước, padding, alpha, modifier. Hình vẽ của màn với bounds của từng thành phần; chọn trên hình hay trên cây đều được. Nó cũng xuất được snapshot (hình, cây và thuộc tính) để gửi cho người khác xem. [[src:ad-layout-inspector]]''',
      '''Layout Inspector attaches to the running app (a debug build) and shows three things. The component tree: the UI structure in real time, Views and Compose alike. The attributes panel: layout attributes of the selected component, such as size, padding, alpha and modifiers. A rendering of the screen with each component\'s bounds; you can select either on the rendering or in the tree. It can also export a snapshot (rendering, tree and attributes) to share with someone else. [[src:ad-layout-inspector]]''')
    B(C, S_, 2, 'p', '''Giao diện của công cụ đổi theo từng bản Android Studio (vị trí nút, chế độ nhúng hay cửa sổ riêng), nên hãy nhớ câu hỏi nó trả lời thay vì nhớ nút: có gì ở đây, nó to bao nhiêu, thuộc tính đang là gì, cái nào nằm trên. Những câu hỏi đó giữ nguyên qua mọi phiên bản.''',
      '''The tool\'s UI changes with each Android Studio version (button positions, embedded or standalone window), so remember the questions it answers rather than the buttons: what is here, how big is it, what are its attributes, which one is on top. Those questions stay the same across versions.''')

    S_ = 'hit'
    a(C + '.sec.%s.title' % S_, '''Cú chạm đi tới đâu''', '''Where a tap goes''')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'p', '''Trong Compose, hit test đi từ gốc cây xuống; một thành phần được "hit" khi điểm chạm nằm trong bounds của nó. Giữa các thành phần anh em chồng nhau, chỉ cái có z cao nhất, tức cái được vẽ trên cùng, được hit. Trong Box, con khai báo sau được vẽ sau. Sau khi đã hit, mọi sự kiện của cùng ngón tay đó đi tới cùng chuỗi thành phần cho tới hết cử chỉ. [[src:ad-compose-gestures]]''',
      '''In Compose, hit testing goes from the root of the tree down; a component is "hit" when the tap point lies within its bounds. Among overlapping siblings, only the one with the highest z, the one drawn on top, is hit. In a Box, a child declared later is drawn later. Once hit, every event of that same pointer goes to the same chain of components until the gesture ends. [[src:ad-compose-gestures]]''')
    B(C, S_, 2, 'p', '''clickable và Button tự tiêu thụ sự kiện, nên một lớp phủ có clickable sẽ nuốt cú chạm dù nó trong suốt. Với View, đường đi tương tự: ViewGroup thấy sự kiện trước con qua onInterceptTouchEvent, có thể chặn lại; con nào xử lý và trả true trong onTouchEvent thì giữ sự kiện. [[src:ad-compose-gestures]] [[src:ad-viewgroup-touch]]''',
      '''clickable and Button consume events themselves, so an overlay with clickable swallows taps even when transparent. With Views the path is similar: a ViewGroup sees events before its children through onInterceptTouchEvent and can intercept them; a child that handles the event and returns true from onTouchEvent keeps it. [[src:ad-compose-gestures]] [[src:ad-viewgroup-touch]]''')
    B(C, S_, 3, 'kt', '''Box(Modifier.fillMaxSize()) {
    Column { /* … */ Button(onClick = onBook) { Text("Đặt lịch") } }
    // SAI: luôn ở trong cây, alpha 0 vẫn nhận chạm
    LoadingOverlay(Modifier.alpha(if (state.loading) 1f else 0f))
    // ĐÚNG: chỉ có trong cây khi đang tải
    if (state.loading) LoadingOverlay()
}''', '''Box(Modifier.fillMaxSize()) {
    Column { /* … */ Button(onClick = onBook) { Text("Book") } }
    // WRONG: always in the tree, alpha 0 still takes taps
    LoadingOverlay(Modifier.alpha(if (state.loading) 1f else 0f))
    // RIGHT: in the tree only while loading
    if (state.loading) LoadingOverlay()
}''')

    S_ = 'overlap'
    a(C + '.sec.%s.title' % S_, '''Tìm thứ đang che''', '''Finding what is covering it''')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'p', '''Thứ che một nút thường không nhìn thấy được: lớp phủ trong suốt, một view có nền trong suốt đặt nhầm kích thước match_parent, một màn trước chưa bị gỡ khỏi cây. Trên hình vẽ chỉ thấy cái nhìn thấy được; cây thành phần thì liệt kê mọi thứ. Ở chế độ Deep Inspect, chọn một vùng để xem mọi thành phần tại đó, rồi chọn thành phần nằm sau qua cây. Show Only Subtree giữ lại một nhánh để nhìn cho gọn. [[src:ad-layout-inspector]]''',
      '''What covers a button is usually invisible: a transparent overlay, a view with a transparent background mistakenly sized match_parent, a previous screen never removed from the tree. The rendering shows only what is visible; the component tree lists everything. In Deep Inspect mode, select a region to see every component there, then pick the one behind through the tree. Show Only Subtree keeps one branch to reduce clutter. [[src:ad-layout-inspector]]''')
    B(C, S_, 2, 'p', '''Cùng kiểu câu hỏi giải được nhiều lỗi giao diện khác: chữ bị cắt (bounds của Text nhỏ hơn nội dung), nút lệch chỗ (padding hay offset không như nghĩ), thành phần không hiện (kích thước 0, hay nằm ngoài màn). Đọc bounds và thuộc tính thật thay vì đoán từ mã.''',
      '''The same kind of question solves many other UI bugs: clipped text (the Text\'s bounds are smaller than its content), a misplaced button (padding or offset not as you thought), a missing component (zero size, or off-screen). Read the real bounds and attributes instead of guessing from the code.''')

    S_ = 'counts'
    a(C + '.sec.%s.title' % S_, '''Đếm recomposition trong Compose''', '''Counting recompositions in Compose''')
    a(C + '.sec.%s.badge' % S_, 'version')
    B(C, S_, 1, 'p', '''Với Compose, Layout Inspector còn đếm số lần mỗi composable được recompose (chạy lại) và được skip (bỏ qua vì đầu vào không đổi). Một composable recompose liên tục trong lúc không có gì thay đổi trên màn là dấu hiệu nó đọc state ở chỗ quá cao hay nhận tham số không ổn định. Vì sao một composable bị recompose hay được skip được giải thích ở chương "Hiệu năng và debug: đo trước, sửa sau" của track Compose Runtime. [[src:ad-layout-inspector]]''',
      '''With Compose, Layout Inspector also counts how many times each composable is recomposed (run again) and skipped (left out because its inputs did not change). A composable that keeps recomposing while nothing changes on screen is a sign that it reads state too high up or receives unstable parameters. Why a composable recomposes or is skipped is explained in "Performance and debugging: measure first, then fix" in the Compose Runtime track. [[src:ad-layout-inspector]]''')

    S_ = 'bugs'
    a(C + '.sec.%s.title' % S_, '''Hai lỗi hay gặp''', '''Two common bugs''')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'bug', '''Sau khi đóng hộp thoại xác nhận, cả màn hình không bấm được gì.''', '''After closing a confirmation dialog, nothing on the screen can be tapped.''')
    B(C, S_, 1, 'cause', '''Hộp thoại tự vẽ chỉ được đặt alpha 0 khi đóng; lớp nền mờ của nó vẫn phủ kín màn và có clickable.''', '''The hand-drawn dialog is only set to alpha 0 when closed; its dimmed backdrop still covers the screen and is clickable.''')
    B(C, S_, 1, 'fix', '''Gỡ hộp thoại khỏi cây khi đóng (if (showDialog) …), không chỉ làm trong suốt.''', '''Remove the dialog from the tree when closed (if (showDialog) …), not just make it transparent.''')
    B(C, S_, 2, 'bug', '''Chữ "Nguyễn Văn An" trên thẻ lịch hẹn bị cắt mất chữ cuối ở máy có cỡ chữ lớn.''', '''The name "Nguyen Van An" on a booking card loses its last letters on phones with a large font size.''')
    B(C, S_, 2, 'cause', '''Text nằm trong một Box có chiều cao cố định 20 dp; bounds của Text nhỏ hơn nội dung khi cỡ chữ tăng.''', '''The Text sits in a Box with a fixed 20 dp height; its bounds are smaller than its content when the font grows.''')
    B(C, S_, 2, 'fix', '''Xem bounds trong Layout Inspector để thấy chỗ cắt; bỏ chiều cao cố định, dùng heightIn(min = 20.dp).''', '''Check the bounds in Layout Inspector to see where it is clipped; drop the fixed height and use heightIn(min = 20.dp).''')

    S_ = 'ex'
    a(C + '.sec.%s.title' % S_, '''Bài tập''', '''Exercise''')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'ex', '''Một Box chứa theo thứ tự: Image nền (fillMaxSize), Button "Gọi phòng khám" ở giữa, và Text "Đang mở cửa" (fillMaxWidth, cao 120 dp, có Modifier.clickable { showHours() }) đặt ở giữa màn. Bấm vào giữa nút thì mở giờ làm việc thay vì gọi. Vì sao, và sửa thế nào?''',
      '''A Box contains, in order: a background Image (fillMaxSize), a "Call the clinic" Button in the centre, and a Text "Open now" (fillMaxWidth, 120 dp tall, with Modifier.clickable { showHours() }) placed in the middle of the screen. Tapping the centre of the button shows opening hours instead of calling. Why, and how do you fix it?''')
    B(C, S_, 1, 'hint', '''Thành phần nào được vẽ sau cùng, bounds của nó có chứa điểm chạm không, và nó có xử lý chạm không?''', '''Which component is drawn last, do its bounds contain the tap point, and does it handle taps?''')
    B(C, S_, 1, 'sol', '''Text khai báo sau nên vẽ trên nút; bounds của nó rộng cả màn và cao 120 dp nên phủ lên nút; nó có clickable nên nhận cú chạm. Sửa: thu Text về đúng kích thước nội dung (bỏ fillMaxWidth, bỏ chiều cao cố định) hoặc đặt nó ở chỗ không chồng lên nút.''',
      '''The Text is declared later, so it is drawn over the button; its bounds span the screen width and 120 dp of height, so it covers the button; it is clickable, so it takes the tap. Fix: shrink the Text to its content (drop fillMaxWidth and the fixed height) or place it where it does not overlap the button.''')

    S_ = 'recall'
    a(C + '.sec.%s.title' % S_, '''Tự trả lời''', '''Answer it yourself''')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'ask', '''Một thành phần alpha 0 có nhận cú chạm không?''', '''Does a component with alpha 0 receive taps?''')
    B(C, S_, 1, 'ans', '''Có, nếu nó còn trong cây, bounds chứa điểm chạm, nằm trên cùng và có xử lý chạm. Alpha chỉ đổi cách vẽ.''', '''Yes, if it is still in the tree, its bounds contain the point, it is on top and it handles touch. Alpha only changes drawing.''')
    B(C, S_, 2, 'ask', '''Log trong onClick không in. Câu hỏi tiếp theo nên là gì?''', '''A log inside onClick never prints. What should the next question be?''')
    B(C, S_, 2, 'ans', '''Cú chạm đang đi tới đâu: xem mọi thành phần chồng lên nhau tại điểm chạm.''', '''Where is the tap going: look at every component overlapping at the tap point.''')

    for q, qv, qe, av, ae, wv, we in [
        ('q1', 'Trong Box, hai con chồng lên nhau, con nào nhận cú chạm?', 'In a Box with two overlapping children, which one gets the tap?', 'Con được vẽ trên cùng, tức con khai báo sau, nếu nó xử lý chạm.', 'The one drawn on top, the one declared later, if it handles taps.',
         'Giữa các anh em, chỉ cái có z cao nhất được hit.', 'Among siblings, only the highest z is hit.'),
        ('q2', 'Layout Inspector trả lời những câu hỏi gì?', 'What questions does Layout Inspector answer?', 'Có gì ở đây, nó to bao nhiêu, thuộc tính là gì, cái nào nằm trên; với Compose, recompose bao nhiêu lần.', 'What is here, how big it is, what its attributes are, which is on top; for Compose, how often it recomposes.',
         'Giao diện công cụ đổi theo phiên bản, câu hỏi thì không.', 'The tool\'s UI changes between versions; the questions do not.'),
        ('q3', 'Muốn ẩn một lớp phủ để nó không chặn chạm, làm gì?', 'To hide an overlay so it stops blocking taps, what do you do?', 'Gỡ nó khỏi cây: chỉ gọi nó khi cần.', 'Remove it from the tree: only call it when needed.',
         'Không có trong cây thì không thể nhận chạm.', 'What is not in the tree cannot take taps.')]:
        a(C + '.quiz.%s.q' % q, qv, qe); a(C + '.quiz.%s.a' % q, av, ae); a(C + '.quiz.%s.why' % q, wv, we)
