# Gỡ lỗi và hiệu năng · l8: bộ nhớ: churn, rò rỉ, heap dump (Phần 2: nhìn vào bên trong app)
# Nguồn (chỉ ghi ở đây và docs/research/debugging.md), đọc 2026-11-25: developer.android.com/studio/profile/memory-profiler (heap dump: Shallow Size,
# Retained Size theo dominator tree, Depth là số bước ngắn nhất từ GC root, References, bộ lọc rò rỉ Activity/Fragment), topic/performance/memory-overview
# (heap phân thế hệ; GC có thể đẩy khung hình quá 16 ms; cấp phát trong vòng lặp; giới hạn heap, OutOfMemoryError; getMemoryClass),
# topic/performance/memory/manage-app-memory (rò rỉ thường do giữ tham chiếu trong biến static; churn gây nhiều GC; onTrimMemory), studio/profile/
# record-java-kotlin-allocations (ghi cấp phát kèm stack trace, Sampled để giảm chi phí), square.github.io/leakcanary (thư viện bên ngoài, bản 2.14: bốn bước,
# chờ 5 giây và chạy GC, ngưỡng 5 đối tượng khi app hiện; leak trace; nguyên nhân hay gặp). Số MB, giới hạn 64 MB và BookingEventBus là của site.

SEC_ORDER = {'l8': ['hook', 'heap', 'leak', 'dump', 'leakcanary', 'bugs', 'ex', 'recall']}


def add(a):
    def B(ch, sec, n, field, vi, en=None):
        a('%s.sec.%s.b.%02d.%s' % (ch, sec, n, field), vi, vi if en is None else en)

    a('preset.leak', '''Gỡ lỗi · Activity bị giữ lại sau khi đóng''', '''Debugging · Activities kept alive after closing''')
    m = lambda k, vi, en=None: a('m.leak.' + k, vi, en)
    m('title', '''App chậm dần rồi OutOfMemoryError ở lần mở thứ 20''', '''The app slows down, then an OutOfMemoryError on the 20th open''')
    m('overview', '''Mỗi lần mở màn chi tiết lịch hẹn, DetailActivity đăng ký một listener vào BookingEventBus, một object sống suốt tiến trình. Cách 1 không bao giờ hủy đăng ký. Cách 2 hủy trong onDestroy. Ta mở rồi đóng màn đó nhiều lần, xem bộ nhớ sau mỗi lần GC, đếm số DetailActivity còn trong heap, và lần theo đường tham chiếu từ GC root. Bộ nhớ và số đối tượng được tính thật từ đồ thị tham chiếu.''',
      '''Each time the booking details screen opens, DetailActivity registers a listener with BookingEventBus, an object that lives as long as the process. Way 1 never unregisters. Way 2 unregisters in onDestroy. We open and close the screen many times, look at memory after each GC, count the DetailActivity instances left in the heap, and follow the reference path from a GC root. Memory and object counts are really computed from the reference graph.''')
    m('wrapup', '''Một listener không hủy đăng ký giữ lambda, lambda giữ Activity, Activity giữ cả cây view và ảnh đầu trang. GC không thu được những gì còn đường tham chiếu từ GC root, nên mỗi lần mở để lại 2,4 MB; lần thứ 20 vượt giới hạn 64 MB và app crash. Hủy đăng ký trong onDestroy cắt đường đó: chỉ màn đang mở còn trong heap, bộ nhớ đứng yên.''',
      '''An unregistered listener holds the lambda, the lambda holds the Activity, the Activity holds its whole view tree and header image. GC cannot collect anything still reachable from a GC root, so each open leaves 2.4 MB behind; the 20th open crosses the 64 MB limit and the app crashes. Unregistering in onDestroy cuts that path: only the screen currently open stays in the heap, and memory stays flat.''')
    m('simp.1', '''Bộ nhớ nền 18 MB, mỗi DetailActivity giữ 2,4 MB và giới hạn heap 64 MB là số của site; giới hạn thật tùy máy (đọc bằng getMemoryClass).''',
      '''The 18 MB baseline, 2.4 MB per DetailActivity and the 64 MB heap limit are the site\'s numbers; the real limit depends on the device (read it with getMemoryClass).''')
    m('simp.2', '''Mỗi lần mở thêm một DetailActivity vào đồ thị tham chiếu; sau GC, chỉ những gì còn đường từ GC root được giữ lại. Bộ nhớ, số instance và đường tham chiếu được tính thật bằng JavaScript từ đồ thị đó.''',
      '''Each open adds a DetailActivity to the reference graph; after GC, only what is still reachable from a GC root is kept. Memory, instance counts and the reference path are really computed in JavaScript from that graph.''')
    m('ctl.hint', '''Chọn cách viết rồi đi qua bốn bước; xem cột bộ nhớ và đường đỏ từ GC root.''', '''Pick a way of writing it and walk the four steps; watch the memory bars and the red path from the GC root.''')
    m('ctl.case', '''Cách viết DetailActivity''', '''How DetailActivity is written''')
    m('ctl.case.leak', '''đăng ký listener, không hủy''', '''registers a listener, never unregisters'''); m('ctl.case.fixed', '''hủy đăng ký trong onDestroy''', '''unregisters in onDestroy''')
    m('diagramTitle', '''Đường tham chiếu từ GC root''', '''The reference path from a GC root''')
    m('diagramDesc', '''GC root giữ object, object giữ danh sách listener, listener giữ Activity đã đóng''', '''A GC root holds the object, the object holds the listener list, a listener holds a closed Activity''')
    for k, vi, en in [('root', 'GC root: trường static', 'GC root: a static field'), ('bus', 'BookingEventBus (object toàn cục)', 'BookingEventBus (a global object)'), ('list', 'Danh sách listeners', 'The listeners list'),
                      ('lambda', 'Lambda listener', 'Listener lambda'), ('act', 'DetailActivity đã đóng', 'A closed DetailActivity')]:
        m('n.' + k, vi, en)
    m('met.opens', '''Số lần mở rồi đóng''', '''Times opened and closed'''); m('met.mem', '''Bộ nhớ sau GC (MB)''', '''Memory after GC (MB)''')
    m('met.inst', '''DetailActivity trong heap''', '''DetailActivity instances in the heap'''); m('met.oom', '''Kết quả''', '''Outcome''')
    m('oom.ok', '''chạy được''', '''running'''); m('oom.slow', '''chậm dần, GC chạy dày''', '''slowing down, frequent GC'''); m('oom.crash', '''crash OutOfMemoryError''', '''OutOfMemoryError crash''')
    a('cap.leak', '''GC chỉ thu những gì không còn đường từ GC root. Ô đỏ: mắt xích giữ Activity đã đóng ở lại trong bộ nhớ.''', '''GC only collects what is no longer reachable from a GC root. A red box: the link keeping a closed Activity in memory.''')
    S = [
        ('leak', 's1', 'Mở rồi đóng 5 lần: bộ nhớ không về lại', 'Open and close 5 times: memory does not come back',
         'Sau mỗi lần đóng màn và GC chạy, bộ nhớ lẽ ra quay về khoảng 20 MB. Nó tăng đều: 20,4; 22,8; 25,2; 27,6; 30 MB. Mỗi lần mở để lại 2,4 MB không thu hồi được.',
         'After each close and a GC, memory should return to about 20 MB. It climbs steadily: 20.4, 22.8, 25.2, 27.6, 30 MB. Each open leaves 2.4 MB that cannot be reclaimed.'),
        ('leak', 's2', 'Heap dump: 5 DetailActivity, 4 cái đã bị hủy', 'Heap dump: 5 DetailActivity, 4 of them destroyed',
         'Chụp heap dump rồi lọc các Activity bị rò rỉ: có 5 instance của DetailActivity, chỉ một cái đang hiện; 4 cái kia đã qua onDestroy mà vẫn nằm trong heap. Retained size của mỗi cái khoảng 2,4 MB: cả cây view và ảnh đầu trang.',
         'Take a heap dump and filter for leaked Activities: there are 5 DetailActivity instances, only one on screen; the other 4 went through onDestroy yet remain in the heap. Each one\'s retained size is about 2.4 MB: the whole view tree and the header image.'),
        ('leak', 's3', 'Đường tham chiếu: GC root → BookingEventBus → listeners → lambda → Activity', 'The reference path: GC root → BookingEventBus → listeners → lambda → Activity',
         'Xem các tham chiếu tới một Activity đã hủy: nó được lambda onEvent giữ (lambda dùng render nên giữ this), lambda nằm trong danh sách listeners, danh sách thuộc BookingEventBus, và object đó được giữ bởi một trường static, tức một GC root. Độ sâu 4.',
         'Look at the references to a destroyed Activity: the onEvent lambda holds it (the lambda calls render, so it holds this), the lambda sits in the listeners list, the list belongs to BookingEventBus, and that object is held by a static field, a GC root. Depth 4.'),
        ('leak', 's4', 'Lần mở thứ 20: OutOfMemoryError', 'The 20th open: OutOfMemoryError',
         'Mỗi lần thêm 2,4 MB: 18 + 20 × 2,4 = 66 MB, vượt giới hạn 64 MB. Trước đó, GC chạy ngày càng dày khi heap gần đầy, nên app giật dần. Stack trace của OOM chỉ vào chỗ cấp phát cuối cùng, không phải chỗ rò rỉ.',
         'Each open adds 2.4 MB: 18 + 20 × 2.4 = 66 MB, over the 64 MB limit. Before that, GC runs more and more often as the heap fills, so the app gets janky. The OOM stack trace points at the last allocation, not at the leak.'),
        ('fixed', 's1', 'Mở rồi đóng 5 lần: bộ nhớ đứng ở 20,4 MB', 'Open and close 5 times: memory stays at 20.4 MB',
         'onDestroy gọi unregister(onEvent), nên khi màn đóng, danh sách listeners không còn giữ lambda. Sau GC, bộ nhớ trở về 20,4 MB lần nào cũng vậy: nền 18 MB cộng màn đang mở.',
         'onDestroy calls unregister(onEvent), so when the screen closes the listeners list no longer holds the lambda. After GC memory returns to 20.4 MB every time: the 18 MB baseline plus the open screen.'),
        ('fixed', 's2', 'Heap dump: đúng 1 DetailActivity', 'Heap dump: exactly 1 DetailActivity',
         'Bộ lọc rò rỉ không thấy Activity nào; heap chỉ có instance đang hiện. Bốn instance cũ không còn đường từ GC root nên đã bị GC thu.',
         'The leak filter finds no Activity; the heap holds only the instance on screen. The four old instances are no longer reachable from a GC root, so GC collected them.'),
        ('fixed', 's3', 'Không còn đường từ GC root tới Activity đã đóng', 'No path from a GC root to a closed Activity',
         'BookingEventBus vẫn là object sống suốt tiến trình, nhưng danh sách listeners chỉ chứa listener của màn đang mở. Mắt xích giữa object và Activity cũ đã bị cắt.',
         'BookingEventBus is still a process-wide object, but its listeners list holds only the open screen\'s listener. The link between the object and old Activities is cut.'),
        ('fixed', 's4', 'Mở 20 lần: vẫn 20,4 MB', 'Opened 20 times: still 20.4 MB',
         'Bộ nhớ sau GC phẳng ở 20,4 MB, không gần giới hạn 64 MB. Không OOM, không giật vì GC.',
         'Memory after GC stays flat at 20.4 MB, nowhere near the 64 MB limit. No OOM, no GC jank.'),
    ]
    for case, k, tv, te, xv, xe in S:
        sid = case + '.' + k
        m('s.%s.title' % sid, tv, te); m('s.%s.explain' % sid, xv, xe); m('ev.' + sid, tv, te)
    for k, vi, en in [
        ('try', '''Mẹo đọc: hàng ô trên là đường tham chiếu từ GC root; ô đỏ là mắt xích giữ Activity đã đóng. Các cột dưới là bộ nhớ sau GC của từng lần mở, vạch ngang là giới hạn heap.''',
         '''Reading tip: the top row of boxes is the reference path from a GC root; red boxes are links keeping a closed Activity. The bars below are memory after GC for each open, the horizontal line is the heap limit.'''),
        ('leak.s2', '''Heap dump có bộ lọc riêng để hiện các Activity và Fragment bị rò rỉ. Retained size là lượng bộ nhớ mà instance đó chi phối, tức sẽ được giải phóng nếu nó bị thu. [[src:ad-memory-profiler]]''',
         '''A heap dump has a filter to show leaked Activities and Fragments. Retained size is the memory that instance dominates, which would be freed if it were collected. [[src:ad-memory-profiler]]'''),
        ('leak.s3', '''Depth là số bước ngắn nhất từ một GC root tới instance đang chọn; phần References liệt kê mọi tham chiếu tới nó. [[src:ad-memory-profiler]]''',
         '''Depth is the shortest number of hops from any GC root to the selected instance; the References view lists every reference to it. [[src:ad-memory-profiler]]'''),
        ('leak.s4', '''Heap có giới hạn cứng; chạm giới hạn thì app có thể nhận OutOfMemoryError. GC chạy dày khi heap gần đầy có thể đẩy khung hình quá 16 ms. [[src:ad-memory-overview]]''',
         '''The heap has a hard limit; reaching it, the app can receive an OutOfMemoryError. GC running often as the heap fills can push frames past 16 ms. [[src:ad-memory-overview]]'''),
        ('fixed.s1', '''Đăng ký listener, receiver hay subscription mà không hủy là một trong các nguyên nhân rò rỉ hay gặp nhất. [[src:leakcanary-fundamentals]]''',
         '''Registering a listener, receiver or subscription without unregistering is one of the most common causes of leaks. [[src:leakcanary-fundamentals]]'''),
        ('fixed.s2', '''Rò rỉ bộ nhớ là lỗi lập trình làm app giữ tham chiếu tới một đối tượng không còn cần nữa. [[src:leakcanary-fundamentals]]''',
         '''A memory leak is a programming error that makes an app keep a reference to an object it no longer needs. [[src:leakcanary-fundamentals]]'''),
        ('fixed.s3', '''Rò rỉ thường do giữ tham chiếu trong biến static; object của Kotlin cũng là một trường static sống suốt tiến trình. [[src:ad-manage-memory]]''',
         '''Leaks are usually caused by holding references in static fields; a Kotlin object is also a static field living as long as the process. [[src:ad-manage-memory]]'''),
        ('fixed.s4', '''Cách an toàn hơn là để vòng đời tự lo: thu Flow bằng repeatOnLifecycle trong lifecycleScope thì việc thu tự dừng khi màn hình dừng, không cần nhớ hủy đăng ký.''',
         '''Safer still is to let the lifecycle handle it: collecting a Flow with repeatOnLifecycle in lifecycleScope stops collecting automatically when the screen stops, with nothing to remember to unregister.'''),
    ]:
        m('co.' + k, vi, en)

    z = lambda k, vi, en=None: a('vz.' + k, vi, en)
    z('tab.leak', '''Đường tham chiếu và bộ nhớ''', '''Reference path and memory''')
    z('lk.aria', '''Đường tham chiếu từ GC root; sau {n} lần mở, bộ nhớ {m} MB, giới hạn 64 MB''', '''The reference path from a GC root; after {n} opens, memory is {m} MB, limit 64 MB''')
    z('lk.limit', '''giới hạn 64 MB''', '''limit 64 MB'''); z('lk.open', '''lần mở''', '''open #''')
    z('lk.sub', '''Sau {n} lần mở: {m} MB; {k} DetailActivity trong heap.''', '''After {n} opens: {m} MB; {k} DetailActivity instances in the heap.''')
    z('lk.cut', '''(đã cắt: listener được hủy trong onDestroy)''', '''(cut: the listener is unregistered in onDestroy)''')
    z('lk.legend', '''Ô đỏ: mắt xích giữ Activity đã đóng. Cột: bộ nhớ sau GC của từng lần mở; cột đỏ là vượt giới hạn (OutOfMemoryError).''',
      '''Red boxes: links keeping a closed Activity. Bars: memory after GC for each open; a red bar crosses the limit (OutOfMemoryError).''')

    C = 'l8'
    a(C + '.title', '''Bộ nhớ: churn, rò rỉ, heap dump''', '''Memory: churn, leaks, heap dumps''')
    a(C + '.essence', '''Bộ nhớ trên Android do GC (bộ thu gom rác) quản lý: đối tượng nào không còn đường tham chiếu từ một GC root (như trường static, luồng đang chạy) thì được thu. Rò rỉ bộ nhớ là khi mã vô tình giữ một đường như vậy tới thứ không còn cần, điển hình là Activity đã đóng.\nRò rỉ làm bộ nhớ sau mỗi lần GC tăng dần; GC chạy dày hơn, app giật, rồi tới OutOfMemoryError. Stack trace của OOM chỉ vào lần cấp phát cuối, không vào chỗ rò rỉ.\nHeap dump trả lời: có bao nhiêu instance, mỗi cái giữ bao nhiêu bộ nhớ (retained size), và đường tham chiếu nào từ GC root đang giữ nó. LeakCanary (thư viện bên ngoài) tự làm các bước đó khi Activity hay Fragment bị hủy mà vẫn còn trong bộ nhớ.''',
      '''Memory on Android is managed by the GC (garbage collector): any object no longer reachable from a GC root (such as a static field or a running thread) is collected. A memory leak is when code accidentally keeps such a path to something no longer needed, typically a closed Activity.\nLeaks make memory after each GC creep up; GC runs more often, the app gets janky, then comes an OutOfMemoryError. The OOM stack trace points at the last allocation, not at the leak.\nA heap dump answers: how many instances there are, how much memory each holds (retained size), and which reference path from a GC root is keeping it. LeakCanary (an external library) does those steps automatically when an Activity or Fragment is destroyed yet still in memory.''')
    a(C + '.goal.g1', '''Đã thấy Activity đã hủy còn trong heap''', '''Saw destroyed Activities still in the heap''')
    a(C + '.goal.g2', '''Đã thấy đường tham chiếu bị cắt''', '''Saw the reference path cut''')
    a(C + '.sim.debugging.leak', '''listener không hủy, hay hủy trong onDestroy''', '''a listener never unregistered, or unregistered in onDestroy''')

    S_ = 'hook'
    a(C + '.sec.%s.title' % S_, '''Đoán trước khi đọc''', '''Predict before reading''')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'predict', '''Mỗi lần mở màn chi tiết, Activity đăng ký một listener vào một object toàn cục mà không bao giờ hủy. Mở rồi đóng màn đó 5 lần, heap còn bao nhiêu DetailActivity?''',
      '''Each time the details screen opens, the Activity registers a listener with a global object and never unregisters. After opening and closing it 5 times, how many DetailActivity instances are in the heap?''')
    B(C, S_, 1, 'ans', '''5: một cái đang hiện và 4 cái đã đóng mà GC không thu được, vì object toàn cục vẫn giữ listener, listener giữ Activity. Mô phỏng ngay dưới lần theo đường đó và cho thấy nó dẫn tới OutOfMemoryError.''',
      '''5: one on screen and 4 closed ones GC cannot collect, because the global object still holds the listener and the listener holds the Activity. The simulation just below follows that path and shows where it leads: an OutOfMemoryError.''')

    S_ = 'heap'
    a(C + '.sec.%s.title' % S_, '''GC, GC root và churn''', '''GC, GC roots and churn''')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'p', '''Heap của Android chia theo thế hệ: đối tượng mới vào vùng trẻ, sống lâu thì được chuyển sang vùng già hơn. Khi một vùng đầy, GC chạy và thu những đối tượng không còn với tới được từ GC root. Heap có giới hạn cứng cho mỗi app (đọc bằng getMemoryClass của ActivityManager); chạm giới hạn thì app nhận OutOfMemoryError. [[src:ad-memory-overview]]''',
      '''Android\'s heap is generational: new objects go into a young area, long-lived ones are moved to older ones. When an area fills up, GC runs and collects the objects no longer reachable from a GC root. Each app\'s heap has a hard limit (read with ActivityManager\'s getMemoryClass); reaching it, the app gets an OutOfMemoryError. [[src:ad-memory-overview]]''')
    B(C, S_, 2, 'p', '''Churn (cấp phát dồn dập) là vấn đề khác với rò rỉ: không giữ gì lâu, nhưng tạo rất nhiều đối tượng tạm, ví dụ trong vòng lặp trong cùng, trong lúc vẽ hay trong mỗi lần recompose. Mỗi đợt GC tốn thời gian, và nhiều đợt có thể đẩy một khung hình quá hạn 16 ms. Ghi lại các lần cấp phát (kèm stack trace) cho thấy chỗ tạo đối tượng; chế độ lấy mẫu giảm chi phí ghi. [[src:ad-manage-memory]] [[src:ad-alloc-tracking]]''',
      '''Churn (allocating in bursts) is a different problem from a leak: nothing is kept long, but many temporary objects are created, for example in an innermost loop, while drawing or on every recomposition. Each GC takes time, and many of them can push a frame past the 16 ms deadline. Recording allocations (with stack traces) shows where objects are created; sampled mode lowers the recording cost. [[src:ad-manage-memory]] [[src:ad-alloc-tracking]]''')

    S_ = 'leak'
    a(C + '.sec.%s.title' % S_, '''Rò rỉ là gì, và vì sao Activity hay bị rò''', '''What a leak is, and why Activities leak so often''')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'p', '''Rò rỉ bộ nhớ là lỗi lập trình làm app giữ tham chiếu tới một đối tượng không còn cần. Activity là thứ hay bị rò nhất vì nó lớn (giữ cả cây view, ảnh, Context) và có vòng đời ngắn hơn nhiều thứ quanh nó. Nguyên nhân hay gặp: lưu Activity hay Context vào trường static, singleton hay object sống lâu; đăng ký listener, receiver, subscription mà không hủy; Fragment trên back stack giữ view sau onDestroyView. [[src:leakcanary-fundamentals]] [[src:ad-manage-memory]]''',
      '''A memory leak is a programming error that makes an app keep a reference to an object it no longer needs. Activities leak most often because they are big (holding the whole view tree, images, a Context) and live shorter than many things around them. Common causes: storing an Activity or Context in a static field, singleton or long-lived object; registering listeners, receivers or subscriptions without unregistering; a Fragment on the back stack holding its views after onDestroyView. [[src:leakcanary-fundamentals]] [[src:ad-manage-memory]]''')
    B(C, S_, 2, 'p', '''Lambda trong Kotlin giữ những gì nó dùng; lambda gọi một hàm của Activity thì giữ chính Activity (this). Vì vậy một lambda nhỏ nằm trong danh sách listener của một object toàn cục đủ để giữ cả màn hình. Cách lambda giữ biến được nói ở chương "Lambda, closure và inline" của track Kotlin: cơ chế ngôn ngữ; singleton và phạm vi của dependency ở chương "Dependency injection: thủ công và Hilt" của track Kiến trúc app Android.''',
      '''A Kotlin lambda holds what it uses; a lambda calling an Activity function holds the Activity itself (this). So one small lambda sitting in a global object\'s listener list is enough to hold the whole screen. How lambdas capture variables is covered in "Lambdas, closures and inline" in the Kotlin: How the Language Works track; singletons and dependency scopes in "Dependency injection: manual and Hilt" in the Android App Architecture track.''')

    S_ = 'dump'
    a(C + '.sec.%s.title' % S_, '''Đọc heap dump''', '''Reading a heap dump''')
    a(C + '.sec.%s.badge' % S_, 'version')
    B(C, S_, 1, 'p', '''Heap dump là ảnh chụp mọi đối tượng trong heap tại một lúc. Với mỗi lớp: số instance, shallow size (bộ nhớ của chính các instance) và retained size (bộ nhớ sẽ được giải phóng nếu chúng bị thu, gồm mọi thứ chỉ chúng giữ). Với mỗi instance: depth là số bước ngắn nhất từ một GC root, và danh sách tham chiếu tới nó. Có bộ lọc riêng để hiện Activity, Fragment bị rò. [[src:ad-memory-profiler]]''',
      '''A heap dump is a snapshot of every object in the heap at one moment. For each class: the instance count, the shallow size (memory of the instances themselves) and the retained size (memory freed if they were collected, including everything only they hold). For each instance: depth, the shortest number of hops from a GC root, and the list of references to it. There is a filter to show leaked Activities and Fragments. [[src:ad-memory-profiler]]''')
    B(C, S_, 2, 'p', '''Cách đọc: mở rồi đóng màn nghi rò vài lần, cho GC chạy, chụp heap dump. Nếu số instance của Activity lớn hơn số màn đang mở, chọn một instance đã hủy và đi ngược theo tham chiếu tới GC root. Mắt xích cần cắt thường là chỗ một đối tượng sống lâu (object, singleton, luồng) trỏ vào thứ sống ngắn.''',
      '''How to read it: open and close the suspected screen a few times, let GC run, take a heap dump. If the Activity\'s instance count exceeds the screens currently open, pick a destroyed instance and walk the references back to a GC root. The link to cut is usually where a long-lived object (an object, a singleton, a thread) points at something short-lived.''')
    B(C, S_, 3, 'kt', '''object BookingEventBus {                                   // object: sống suốt tiến trình
    private val listeners = mutableListOf<(BookingEvent) -> Unit>()
    fun register(l: (BookingEvent) -> Unit) { listeners += l }
    fun unregister(l: (BookingEvent) -> Unit) { listeners -= l }
}
class DetailActivity : AppCompatActivity() {
    private val onEvent: (BookingEvent) -> Unit = { render(it) }  // lambda giữ this
    override fun onCreate(s: Bundle?) { super.onCreate(s); BookingEventBus.register(onEvent) }
    override fun onDestroy() { BookingEventBus.unregister(onEvent); super.onDestroy() }  // sửa
}''', '''object BookingEventBus {                                   // object: lives as long as the process
    private val listeners = mutableListOf<(BookingEvent) -> Unit>()
    fun register(l: (BookingEvent) -> Unit) { listeners += l }
    fun unregister(l: (BookingEvent) -> Unit) { listeners -= l }
}
class DetailActivity : AppCompatActivity() {
    private val onEvent: (BookingEvent) -> Unit = { render(it) }  // the lambda holds this
    override fun onCreate(s: Bundle?) { super.onCreate(s); BookingEventBus.register(onEvent) }
    override fun onDestroy() { BookingEventBus.unregister(onEvent); super.onDestroy() }  // fix
}''')

    S_ = 'leakcanary'
    a(C + '.sec.%s.title' % S_, '''LeakCanary làm những bước đó tự động''', '''LeakCanary does those steps automatically''')
    a(C + '.sec.%s.badge' % S_, 'version')
    B(C, S_, 1, 'p', '''LeakCanary là thư viện bên ngoài (bản 2.14) thêm vào bản debug. Nó theo dõi Activity, Fragment, view của Fragment và ViewModel sau khi bị hủy bằng tham chiếu yếu; chờ 5 giây và chạy GC; đối tượng còn sống thì bị coi là bị giữ lại. Khi số đối tượng bị giữ đạt ngưỡng (mặc định 5 khi app đang hiện), nó chụp heap dump, phân tích và in leak trace: đường tham chiếu từ GC root giữ đối tượng đó lại, với các mắt xích đáng ngờ được đánh dấu. [[src:leakcanary-how]]''',
      '''LeakCanary is an external library (version 2.14) added to debug builds. It watches Activities, Fragments, Fragment views and ViewModels after they are destroyed, using weak references; it waits 5 seconds and runs GC; an object still alive is considered retained. When the retained count reaches a threshold (5 by default while the app is visible), it takes a heap dump, analyses it and prints a leak trace: the reference path from a GC root keeping that object alive, with the suspect links marked. [[src:leakcanary-how]]''')
    B(C, S_, 2, 'p', '''Cơ chế đáng nhớ hơn tên thư viện: tham chiếu yếu để biết đối tượng có bị thu không, heap dump để thấy mọi thứ, và đường ngắn nhất từ GC root để biết mắt xích nào cần cắt. Cùng cơ chế đó, bạn làm được bằng tay với heap dump như mục trên.''',
      '''The mechanism matters more than the library\'s name: a weak reference to learn whether an object was collected, a heap dump to see everything, and the shortest path from a GC root to learn which link to cut. With that same mechanism you can do it by hand with a heap dump, as in the section above.''')

    S_ = 'bugs'
    a(C + '.sec.%s.title' % S_, '''Hai lỗi hay gặp''', '''Two common bugs''')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'bug', '''Một singleton ImageCache nhận Context trong constructor; sau vài lần xoay máy, heap có nhiều MainActivity.''', '''An ImageCache singleton takes a Context in its constructor; after a few rotations the heap has several MainActivity instances.''')
    B(C, S_, 1, 'cause', '''Lần tạo đầu nhận Activity làm Context, và singleton giữ nó suốt tiến trình; mỗi lần xoay, Activity mới thay chỗ nhưng cái cũ vẫn bị giữ.''', '''The first creation received the Activity as its Context, and the singleton keeps it for the life of the process; each rotation creates a new Activity, but the old one stays held.''')
    B(C, S_, 1, 'fix', '''Đối tượng sống lâu chỉ giữ applicationContext, không giữ Activity.''', '''Long-lived objects keep only the applicationContext, never an Activity.''')
    B(C, S_, 2, 'bug', '''Cuộn danh sách lịch hẹn bị giật; Memory profiler cho thấy GC chạy liên tục mà bộ nhớ không tăng.''', '''Scrolling the booking list stutters; the memory profiler shows GC running constantly while memory does not grow.''')
    B(C, S_, 2, 'cause', '''Churn, không phải rò rỉ: mỗi lần vẽ một hàng tạo một SimpleDateFormat và vài chuỗi mới.''', '''Churn, not a leak: drawing each row creates a SimpleDateFormat and several new strings.''')
    B(C, S_, 2, 'fix', '''Tạo bộ định dạng một lần rồi dùng lại; tính chuỗi hiển thị trước, không trong lúc vẽ.''', '''Create the formatter once and reuse it; compute display strings beforehand, not while drawing.''')

    S_ = 'ex'
    a(C + '.sec.%s.title' % S_, '''Bài tập''', '''Exercise''')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'ex', '''Leak trace của LeakCanary: GC root (luồng "sync-timer") → SyncTimer.callback → PaymentFragment$1 (anonymous) → PaymentFragment.binding → ConstraintLayout (đã tách khỏi cửa sổ). Đối tượng nào bị giữ, mắt xích nào nên cắt, và sửa thế nào?''',
      '''A LeakCanary leak trace: GC root (thread "sync-timer") → SyncTimer.callback → PaymentFragment$1 (anonymous) → PaymentFragment.binding → ConstraintLayout (detached from the window). What is being held, which link should be cut, and how do you fix it?''')
    B(C, S_, 1, 'hint', '''Tìm chỗ một đối tượng sống lâu (luồng, timer) trỏ vào thứ sống ngắn (Fragment, view).''', '''Find where a long-lived object (a thread, a timer) points at something short-lived (a Fragment, a view).''')
    B(C, S_, 1, 'sol', '''Bị giữ là cây view của PaymentFragment (qua binding). Mắt xích cần cắt là SyncTimer.callback → lớp ẩn danh của Fragment: hủy callback khi view bị hủy (onDestroyView), và đặt binding = null ở đó. Tốt hơn: dùng coroutine trong viewLifecycleOwner.lifecycleScope thay cho timer, để việc tự dừng theo vòng đời của view.''',
      '''What is held is PaymentFragment\'s view tree (through binding). The link to cut is SyncTimer.callback → the Fragment\'s anonymous class: remove the callback when the view is destroyed (onDestroyView), and set binding = null there. Better: use a coroutine in viewLifecycleOwner.lifecycleScope instead of the timer, so the work stops with the view\'s lifecycle.''')

    S_ = 'recall'
    a(C + '.sec.%s.title' % S_, '''Tự trả lời''', '''Answer it yourself''')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'ask', '''Vì sao GC không thu được một Activity đã đóng?''', '''Why can GC not collect a closed Activity?''')
    B(C, S_, 1, 'ans', '''Vì vẫn còn một đường tham chiếu mạnh từ GC root tới nó, ví dụ object toàn cục → listener → lambda → Activity.''', '''Because a strong reference path from a GC root still reaches it, for example global object → listener → lambda → Activity.''')
    B(C, S_, 2, 'ask', '''Churn và rò rỉ khác nhau thế nào trên biểu đồ bộ nhớ?''', '''How do churn and a leak differ on the memory graph?''')
    B(C, S_, 2, 'ans', '''Rò rỉ: bộ nhớ sau GC tăng dần. Churn: răng cưa dày, GC chạy liên tục, nhưng bộ nhớ sau GC không tăng.''', '''A leak: memory after GC creeps up. Churn: a dense sawtooth, GC running constantly, but memory after GC not growing.''')

    for q, qv, qe, av, ae, wv, we in [
        ('q1', 'Retained size của một instance là gì?', 'What is an instance\'s retained size?', 'Bộ nhớ sẽ được giải phóng nếu instance đó bị thu, gồm mọi thứ chỉ nó giữ.', 'The memory freed if that instance were collected, including everything only it holds.',
         'Shallow size chỉ là bộ nhớ của chính nó.', 'Shallow size is only its own memory.'),
        ('q2', 'Stack trace của OutOfMemoryError có chỉ vào chỗ rò rỉ không?', 'Does an OutOfMemoryError stack trace point at the leak?', 'Không; nó chỉ vào lần cấp phát cuối cùng.', 'No; it points at the last allocation.',
         'Phải dùng heap dump để tìm thứ đang chiếm bộ nhớ.', 'Use a heap dump to find what is taking the memory.'),
        ('q3', 'Đối tượng sống suốt tiến trình nên giữ Context nào?', 'Which Context should a process-wide object hold?', 'applicationContext.', 'The applicationContext.',
         'Giữ Activity thì cả màn hình bị giữ theo.', 'Holding an Activity keeps the whole screen alive.')]:
        a(C + '.quiz.%s.q' % q, qv, qe); a(C + '.quiz.%s.a' % q, av, ae); a(C + '.quiz.%s.why' % q, wv, we)
