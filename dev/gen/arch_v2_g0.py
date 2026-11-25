# Kiến trúc · G0: bản đồ track (viết cuối, đặt đầu track). Tổng hợp G1–G11.

SEC_ORDER = {'g0': ['hook', 'order', 'index', 'links', 'recall', 'honest']}


def add(a):
    def B(ch, sec, n, field, vi, en=None):
        a('%s.sec.%s.b.%02d.%s' % (ch, sec, n, field), vi, vi if en is None else en)

    m = lambda k, vi, en=None: a('m.map.' + k, vi, en)
    m('title', 'Gặp triệu chứng này thì đọc chương nào', 'Seen this symptom? Read this chapter')
    m('overview', 'Chọn một triệu chứng hay gặp trong app Android. Bốn bước: triệu chứng, lúc nó lộ ra (khi build, khi test, lúc chạy, hay sai lặng lẽ), nguyên nhân kiến trúc, và chương giải thích.',
      'Pick a symptom common in Android apps. Four steps: the symptom, when it shows up (at build, in tests, at runtime, or silently wrong), the architectural cause, and the chapter that explains it.')
    m('wrapup', 'Phần lớn lỗi kiến trúc không làm app crash mà làm nó sai lặng lẽ: dữ liệu lệch, thông báo lặp, test chập chờn. Vì vậy chúng khó tìm bằng debugger và dễ tìm hơn khi biết hình dạng của chúng. Mỗi triệu chứng ở đây dẫn tới một chương có mô phỏng và cách sửa.',
      'Most architecture bugs do not crash the app; they make it silently wrong: drifting data, repeated messages, flaky tests. That makes them hard to find with a debugger and easier once you know their shape. Each symptom here leads to a chapter with a simulation and a fix.')
    m('simp.1', 'Mỗi triệu chứng chỉ trỏ tới một chương chính; nhiều lỗi thật có nhiều nguyên nhân cùng lúc.', 'Each symptom points to one main chapter; many real bugs have several causes at once.')
    m('ctl.hint', 'Chọn triệu chứng rồi đi bốn bước; tab "Bảng tra" liệt kê tất cả.', 'Pick a symptom and walk the four steps; the "Lookup table" tab lists them all.')
    m('ctl.symptom', 'Triệu chứng', 'Symptom')
    m('diagramTitle', 'Triệu chứng, lúc lộ ra, nguyên nhân, chương', 'Symptom, when it shows, cause, chapter')
    m('diagramDesc', 'Từ điều bạn thấy tới chương cần đọc', 'From what you see to the chapter to read')
    for k, vi, en in [('symptom', 'Triệu chứng', 'Symptom'), ('phase', 'Lộ ra lúc', 'Shows up'), ('cause', 'Nguyên nhân', 'Cause'), ('chapter', 'Chương', 'Chapter')]:
        m('n.' + k, vi, en)
    m('met.phase', 'Lộ ra lúc', 'Shows up'); m('met.chapter', 'Chương', 'Chapter')
    m('phase.none', 'chưa xét', 'not yet'); m('ch.none', 'chưa xét', 'not yet')
    for k, vi, en, xv, xe in [
        ('build', 'khi build', 'at build time', 'Công cụ chặn ngay: trình biên dịch hay Gradle từ chối.', 'Tools stop it at once: the compiler or Gradle refuses.'),
        ('test', 'khi chạy test', 'when tests run', 'Không lộ khi dùng app, nhưng làm test chậm hay chập chờn.', 'Invisible in the app, but makes tests slow or flaky.'),
        ('runtime', 'lúc chạy, thấy rõ', 'at runtime, visibly', 'App crash, mất dữ liệu hay tốn bộ nhớ dần; người dùng thấy.', 'The app crashes, loses data or keeps growing in memory; users notice.'),
        ('silent', 'sai lặng lẽ', 'silently wrong', 'Không crash, không lỗi build: app chạy nhưng hiện sai hay khó đổi.', 'No crash, no build error: the app runs but shows the wrong thing or resists change.')]:
        m('phase.' + k, vi, en); m('phase.%s.explain' % k, xv, xe)
    T = {
        'g1': ('Vì sao cần kiến trúc', 'Why architecture matters'), 'g2': ('Các tầng, hướng phụ thuộc, SSOT, UDF', 'Layers, dependency direction, SSOT, UDF'),
        'g3': ('UI layer: UiState, ViewModel, sự kiện', 'The UI layer: UiState, ViewModel, events'), 'g4': ('Data layer và offline-first', 'The data layer and offline-first'),
        'g5': ('Domain layer và use case', 'The domain layer and use cases'), 'g6': ('Dependency injection (DI)', 'Dependency injection'), 'g7': ('MVVM và MVI', 'MVVM and MVI'),
        'g8': ('Lỗi qua các tầng', 'Errors across layers'), 'g9': ('Module hóa', 'Modularization'), 'g10': ('Kiểm thử theo tầng', 'Testing by layer'),
        'g11': ('Thêm tính năng và di trú', 'Adding features and migrating')}
    for g, (vi, en) in T.items():
        m('ch.' + g, '%s · %s' % (g.upper(), vi), '%s · %s' % (g.upper(), en)); m('go.' + g, 'Đọc chương %s: %s' % (g.upper(), vi), 'Read chapter %s: %s' % (g.upper(), en))
    SY = [
        ('rotateLoses', 'Xoay màn hình thì danh sách mất và tải lại', 'Rotating loses the list and reloads it', 'Người dùng xoay điện thoại giữa lúc tải; màn hình trống rồi gọi mạng lại.', 'The user rotates mid-load; the screen goes blank and calls the network again.',
         'Dữ liệu nằm trong Activity', 'Data lives in the Activity', 'Activity bị hủy và tạo lại khi đổi cấu hình; biến của nó mất theo.', 'The Activity is destroyed and recreated on a configuration change; its fields go with it.',
         'Đưa state vào ViewModel; Activity chỉ quan sát.', 'Move state into a ViewModel; the Activity only observes.'),
        ('importUi', 'Test repository bỗng cần Context và tài nguyên Android', 'Repository tests suddenly need a Context and Android resources', 'Một thay đổi nhỏ ở giao diện ô giờ làm hỏng test của repository.', 'A small change to the time-chip UI breaks the repository tests.',
         'Phụ thuộc sai chiều: data biết UI', 'A wrong-way dependency: data knows the UI', 'Repository import lớp UI; trong một module không công cụ nào chặn.', 'The repository imports a UI class; within one module no tool stops it.',
         'Repository trả mô hình dữ liệu; ViewModel đổi sang mô hình UI; tách module để công cụ giữ quy tắc.', 'The repository returns data models; the ViewModel maps them to UI models; split modules so tools hold the rule.'),
        ('toastAgain', 'Thông báo "Đã đặt lịch" hiện lại sau khi xoay', 'The "Booked" message shows again after rotating', 'Mỗi lần xoay hay đổi sáng tối, Toast lại hiện.', 'Every rotation or light/dark switch shows the Toast again.',
         'Sự kiện bị giữ như trạng thái kéo dài', 'An event held as a lasting state', 'Cờ trong StateFlow không ai xóa; StateFlow phát lại giá trị mới nhất cho Activity mới.', 'A flag in a StateFlow nobody clears; StateFlow replays its latest value to the new Activity.',
         'Đưa thông báo vào UI state và cho UI báo lại khi đã hiện để xóa.', 'Put the message in UI state and have the UI report back once shown so it is cleared.'),
        ('staleAfterRefresh', 'Làm mới thấy bản mới, mở lại thấy bản cũ', 'Refresh shows the new copy, reopening shows the old one', 'Sau khi kéo làm mới, 9:30 đã kín; mở lại màn thì 9:30 lại trống.', 'After pulling to refresh, 9:30 is taken; reopening shows it free again.',
         'Hai nguồn dữ liệu cho UI', 'Two data sources for the UI', 'Kết quả mạng trả thẳng cho UI, không ghi vào database mà màn hình đọc khi mở.', 'The network result goes straight to the UI and never reaches the database the screen reads on opening.',
         'Database là nguồn sự thật: mạng chỉ ghi vào database, UI chỉ quan sát database.', 'Make the database the source of truth: the network only writes it, the UI only observes it.'),
        ('rulesDiffer', 'Hai màn trả lời khác nhau cho cùng một câu hỏi', 'Two screens answer the same question differently', 'Màn Chọn giờ khóa 9:30; màn Đổi lịch vẫn cho chọn.', 'Choose a time greys out 9:30; Reschedule still allows it.',
         'Quy tắc nghiệp vụ bị chép', 'A business rule was copied', 'Cùng quy tắc viết ở hai ViewModel; lần đổi chính sách chỉ sửa một bản.', 'The same rule lives in two ViewModels; the policy change updated only one.',
         'Rút quy tắc vào một use case dùng chung.', 'Extract the rule into one shared use case.'),
        ('memoryGrows', 'Bộ nhớ tăng sau mỗi lần xoay', 'Memory grows with every rotation', 'Mỗi lần xoay, app dùng thêm vài MB và không giảm.', 'Each rotation adds a few MB that never go away.',
         'Object sống lâu giữ Activity', 'A long-lived object holds an Activity', 'Một singleton được tạo với Activity làm Context, nên giữ Activity đã hủy.', 'A singleton was built with an Activity as its Context, so it holds the destroyed Activity.',
         'Dùng context của Application (@ApplicationContext); object cần Activity thì để ở scope Activity.', 'Use the Application context (@ApplicationContext); objects needing the Activity belong in the Activity scope.'),
        ('spinnerError', 'Màn hình vừa đang tải vừa báo lỗi', 'The screen is loading and showing an error at once', 'Vòng xoay và thông báo lỗi hiện cùng lúc.', 'A spinner and an error show together.',
         'Nhiều luồng state lệch nhau', 'Several state streams drift apart', 'isLoading và error là hai StateFlow riêng; một nhánh mã chỉ cập nhật một trong hai.', 'isLoading and error are separate StateFlows; one code path updates only one of them.',
         'Một UiState duy nhất; tốt hơn, một sealed state chỉ có trạng thái có nghĩa.', 'One single UiState; better, a sealed state with only meaningful states.'),
        ('crashOffline', 'Mất mạng là app crash, hay hiện "HTTP 500"', 'Offline crashes the app, or shows "HTTP 500"', 'Mở màn lúc mất mạng thì crash; lúc máy chủ lỗi thì người dùng thấy chữ kỹ thuật.', 'Opening offline crashes; when the server fails the user sees technical text.',
         'Lỗi không được đổi ở đúng tầng', 'Errors are not mapped in the right layer', 'Ngoại lệ đi thẳng lên ViewModel, hay bị bắt rộng và hiện nguyên message.', 'Exceptions go straight up to the ViewModel, or are caught broadly and shown raw.',
         'Repository đổi lỗi dự đoán được thành failure có tên; ViewModel chọn câu cho người dùng; không nuốt lỗi lập trình.', 'The repository maps expected errors to named failures; the ViewModel picks a user sentence; programming errors are not swallowed.'),
        ('cycleBuild', 'Build hỏng: hai module phụ thuộc vòng', 'The build fails: two modules depend on each other', 'Thêm nút "Đặt lại" ở màn Lịch sử thì Gradle báo vòng phụ thuộc.', 'Adding "Book again" to History makes Gradle report a cycle.',
         'Feature phụ thuộc feature', 'A feature depends on a feature', 'Hai feature module gọi thẳng màn của nhau.', 'Two feature modules call each other\'s screens directly.',
         'App module giữ điều hướng làm trung gian; feature chỉ truyền id.', 'The app module owns navigation and mediates; features pass only ids.'),
        ('flakyTests', 'Test lúc qua lúc trượt dù không ai sửa mã', 'Tests pass or fail though nobody changed the code', 'CI trượt vài lần mỗi tuần, chạy lại thì qua.', 'CI fails a few times a week and passes on re-run.',
         'Test dùng mạng thật', 'Tests use the real network', 'Test ViewModel và repository gọi máy chủ thật, nên phụ thuộc mạng và dữ liệu.', 'ViewModel and repository tests call the real server, so they depend on the network and its data.',
         'Thay phụ thuộc bằng fake ở từng tầng; giữ mạng thật cho vài test đầu tới cuối.', 'Replace dependencies with fakes per layer; keep the real network for a few end-to-end tests.'),
        ('rewriteStalls', 'Dự án đổi kiến trúc kéo dài mãi không xong', 'The architecture change drags on and never finishes', 'Nhánh viết lại sau nhiều tháng vẫn chưa phát hành được.', 'After months, the rewrite branch still cannot ship.',
         'Viết lại cả app một lần', 'Rewriting the whole app at once', 'Nhánh chính vẫn đổi; hai codebase lệch nhau; nhánh mới không phát hành được.', 'Main keeps changing; the codebases diverge; the new branch cannot ship.',
         'Di trú dần từng màn, có test trước, phát hành sau mỗi bước.', 'Migrate screen by screen, tests first, shipping after each step.'),
    ]
    for sid, tv, te, dv, de, cv, ce, cdv, cde, fv, fe in SY:
        m('s.%s.title' % sid, tv, te); m('s.%s.detail' % sid, dv, de); m('s.%s.cause' % sid, cv, ce); m('s.%s.causeDetail' % sid, cdv, cde); m('s.%s.fix' % sid, fv, fe)
        m('ctl.symptom.' + sid, tv, te)
    m('co.try', 'Chọn một triệu chứng bạn từng gặp; đi bốn bước rồi mở chương được chỉ tới.', 'Pick a symptom you have met; walk the four steps, then open the chapter it points to.')
    m('co.cause', 'Nguyên nhân là ở cách tổ chức mã, không phải một dòng sai; sửa một dòng thường chỉ làm lỗi đổi chỗ.', 'The cause is in how the code is organised, not one wrong line; fixing one line usually just moves the bug.')
    m('co.chapter', 'Chương được chỉ tới có mô phỏng của đúng tình huống này, cách sửa, và nguồn.', 'The chapter pointed to has a simulation of exactly this case, the fix, and its sources.')
    a('cap.map', 'Từ trái sang phải: triệu chứng, lúc nó lộ ra, nguyên nhân kiến trúc, chương giải thích. Tab "Bảng tra" liệt kê mọi triệu chứng.', 'Left to right: the symptom, when it shows up, the architectural cause, the chapter that explains it. The "Lookup table" tab lists every symptom.')
    a('preset.map', 'Kiến trúc · bản đồ triệu chứng và chương', 'Architecture · symptom map to chapters')

    z = lambda k, vi, en=None: a('vz.' + k, vi, en)
    z('tab.map', 'Bảng tra', 'Lookup table')
    z('map.cap', 'Mọi triệu chứng của track, lúc chúng lộ ra và chương giải thích. Hàng đang chọn được viền; ô "?" mở dần theo bước.', 'Every symptom in the track, when it shows up, and the chapter that explains it. The selected row is outlined; "?" cells open step by step.')
    z('map.legend', 'Phần lớn lỗi kiến trúc là "sai lặng lẽ": không crash, không lỗi build.', 'Most architecture bugs are "silently wrong": no crash, no build error.')
    for k, vi, en in [('sym', 'Triệu chứng', 'Symptom'), ('phase', 'Lộ ra lúc', 'Shows up'), ('ch', 'Chương', 'Chapter')]:
        z('map.col.' + k, vi, en)

    C = 'g0'
    a(C + '.title', 'Bản đồ track: triệu chứng và chương', 'Track map: symptoms and chapters')
    a(C + '.essence', 'Track này dạy cách tổ chức một app Android để thay đổi, xoay màn hình, mất mạng và kiểm thử bớt đau, theo hướng dẫn chính thức của Android và đối chiếu với sách Clean Architecture.\nPhần 1 (G1–G5) là nền: vì sao cần kiến trúc, các tầng và hướng phụ thuộc, tầng UI, tầng data, tầng domain tùy chọn. Phần 2 (G6–G11) là thực hành: DI, MVVM và MVI, lỗi qua các tầng, module hóa, kiểm thử, và đổi kiến trúc dần dần.\nNếu bạn đang gặp một lỗi cụ thể, bắt đầu từ bảng tra triệu chứng bên dưới.',
      'This track teaches how to organise an Android app so that change, rotation, losing the network and testing hurt less, following Android\'s official guide and comparing it with the Clean Architecture books.\nPart 1 (G1–G5) is the foundation: why architecture matters, layers and dependency direction, the UI layer, the data layer, the optional domain layer. Part 2 (G6–G11) is practice: DI, MVVM and MVI, errors across layers, modularization, testing, and changing architecture gradually.\nIf you are facing a specific bug, start from the symptom lookup below.')
    a(C + '.goal.g1', 'Đã thấy lúc triệu chứng lộ ra', 'Saw when the symptom shows up')
    a(C + '.goal.g2', 'Đã tới chương cần đọc', 'Reached the chapter to read')
    a(C + '.sim.arch.map', 'triệu chứng và chương', 'symptoms and chapters')

    S_ = 'hook'
    a(C + '.sec.%s.title' % S_, 'Đoán trước khi đọc', 'Predict before reading')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'predict', 'Trong 11 triệu chứng của bảng tra, bạn đoán bao nhiêu cái làm app crash hay hỏng build, và bao nhiêu cái chỉ làm app sai lặng lẽ?',
      'Of the 11 symptoms in the lookup table, how many do you guess crash the app or break the build, and how many only make it silently wrong?')
    B(C, S_, 1, 'ans', 'Trong bảng của track này: 3 cái lộ ra lúc chạy (mất dữ liệu khi xoay, bộ nhớ tăng, crash khi mất mạng), 1 cái khi build, 1 cái khi test, và 6 cái sai lặng lẽ. Đây là đếm trong bảng của site, không phải thống kê chung; nhưng nó cho thấy vì sao lỗi kiến trúc khó tìm bằng debugger.',
      'In this track\'s table: 3 show up at runtime (data lost on rotation, growing memory, offline crash), 1 at build, 1 in tests, and 6 are silently wrong. This is a count of the site\'s table, not a general statistic; but it shows why architecture bugs are hard to find with a debugger.')

    S_ = 'order'
    a(C + '.sec.%s.title' % S_, 'Thứ tự đọc', 'Reading order')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'p', 'Người mới đọc theo thứ tự G1 → G11; nên đọc trước Kotlin K1–K7 và Coroutines A1–A3. Phần 1 dựng mô hình: component có thể bị hủy (G1), mũi tên là phụ thuộc và dữ liệu có một nguồn sự thật (G2), UI state và sự kiện (G3), database là nguồn sự thật (G4), khi nào cần use case (G5). Phần 2 đi vào công cụ và quy trình: DI (G6), một state duy nhất (G7), failure (G8), module (G9), test (G10), đổi dần (G11).',
      'Newcomers read G1 → G11 in order; Kotlin K1–K7 and Coroutines A1–A3 first help. Part 1 builds the model: components can be destroyed (G1), arrows are dependencies and data has one source of truth (G2), UI state and events (G3), the database as source of truth (G4), when a use case is needed (G5). Part 2 covers tools and process: DI (G6), one single state (G7), failures (G8), modules (G9), tests (G10), gradual change (G11).')

    S_ = 'index'
    a(C + '.sec.%s.title' % S_, 'Chỉ mục: mỗi chương dùng hình gì', 'Index: the visual of each chapter')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'p', 'G1: luồng qua bốn tầng. G2: đồ thị phụ thuộc, và vòng UDF. G3: làn thời gian qua một lần xoay. G4: làn thời gian máy chủ, database, repository, màn hình. G5: bảng quy tắc và cây quyết định. G6: sơ đồ phạm vi theo thời gian sống. G7: ma trận tổ hợp state. G8: bảng ánh xạ lỗi. G9: đồ thị module. G10: ma trận kiểm thử. G11: dãy ô tiến độ.',
      'G1: a flow through four layers. G2: a dependency graph, and the UDF loop. G3: timeline lanes across a rotation. G4: timeline lanes for server, database, repository, screen. G5: a rule table and decision tree. G6: a scope map by lifetime. G7: a state-combination matrix. G8: an error mapping table. G9: a module graph. G10: a test matrix. G11: a progress strip.')

    S_ = 'links'
    a(C + '.sec.%s.title' % S_, 'Cầu nối sang track khác', 'Bridges to other tracks')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'p', 'G3 ↔ Coroutines A8 và Runtime SH (sự kiện một lần, thu thập theo vòng đời, state hoisting). G6 ↔ Kotlin K11 (by viewModels() là một delegate). G8 ↔ Kotlin K6 (ngoại lệ, catch quá rộng). G10 ↔ Coroutines A9 và Runtime B9 (runTest, kiểm thử giao diện). Track Lưu dữ liệu đi sâu Room, DataStore và WorkManager mà G4 chỉ dùng; track Mã sạch đi sâu SOLID và nguyên lý thành phần mà G2, G9 chỉ nhắc.',
      'G3 ↔ Coroutines A8 and Runtime SH (one-off events, lifecycle-aware collection, state hoisting). G6 ↔ Kotlin K11 (by viewModels() is a delegate). G8 ↔ Kotlin K6 (exceptions, over-broad catch). G10 ↔ Coroutines A9 and Runtime B9 (runTest, UI testing). The Saving Data track goes deep into Room, DataStore and WorkManager, which G4 only uses; the Clean Code and Craft track goes deep into SOLID and component principles, which G2 and G9 only mention.')

    S_ = 'recall'
    a(C + '.sec.%s.title' % S_, 'Tự trả lời', 'Answer it yourself')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'ask', 'Vì sao lỗi kiến trúc khó tìm bằng debugger?', 'Why are architecture bugs hard to find with a debugger?')
    B(C, S_, 1, 'ans', 'Phần lớn không crash mà sai lặng lẽ; nguyên nhân nằm ở cách tổ chức mã chứ không ở một dòng.', 'Most do not crash but are silently wrong; the cause is in how the code is organised, not one line.')

    S_ = 'honest'
    a(C + '.sec.%s.title' % S_, 'Track này giản lược những gì', 'What this track simplifies')
    a(C + '.sec.%s.badge' % S_, 'simplified')
    B(C, S_, 1, 'p', 'Track theo hướng dẫn kiến trúc chính thức của Android đọc ngày 2026-11-23 và 2026-11-24, đối chiếu với Dumbravan (Clean Android Architecture) và Boudjnah (Clean Architecture for Android); mỗi chương ghi nguồn trong mục trung thực và bảng nguồn. Ví dụ là app hư cấu Hẹn Khám; mô phỏng là mô hình giảng dạy, không chạy Android hay Gradle thật. Phần Room, DataStore chi tiết, Dagger thuần, MVP, điều hướng chi tiết và kiến trúc hệ thống lớn nằm ngoài track (xem dàn ý track).',
      'The track follows Android\'s official architecture guidance as read on 2026-11-23 and 2026-11-24, compared with Dumbravan (Clean Android Architecture) and Boudjnah (Clean Architecture for Android); each chapter lists its sources in its honesty section and source table. The example is the fictional ClinicBook app; simulations are teaching models that do not run real Android or Gradle. Room and DataStore in depth, plain Dagger, MVP, detailed navigation and large-system architecture are outside the track (see the track outline).')

    for q, qv, qe, av, ae, wv, we in [
        ('q1', 'Thông báo hiện lại sau khi xoay: đọc chương nào?', 'A message shows again after rotating: which chapter?', 'G3 (UI layer: UiState, ViewModel, sự kiện).', 'G3 (the UI layer: UiState, ViewModel, events).', 'Sự kiện một lần phải thành UI state.', 'One-off events must become UI state.'),
        ('q2', 'Hai màn trả lời khác nhau cho cùng quy tắc: đọc chương nào?', 'Two screens answer the same rule differently: which chapter?', 'G5 (domain layer và use case).', 'G5 (the domain layer and use cases).', 'Quy tắc dùng lại nên nằm ở một use case.', 'A reused rule belongs in one use case.'),
        ('q3', 'Test chập chờn dù không ai sửa mã: đọc chương nào?', 'Tests flake though nobody changed the code: which chapter?', 'G10 (kiểm thử theo tầng).', 'G10 (testing by layer).', 'Thay mạng thật bằng fake.', 'Replace the real network with fakes.')]:
        a(C + '.quiz.%s.q' % q, qv, qe); a(C + '.quiz.%s.a' % q, av, ae); a(C + '.quiz.%s.why' % q, wv, we)
