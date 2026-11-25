# Kiến trúc · G10: kiểm thử theo tầng (Phần 2)
# Nguồn: developer.android.com Fundamentals of testing, Testing strategies, Use test doubles (đọc 2026-11-24).
# Nối Coroutines A9 (runTest, thời gian ảo), Runtime B9 (kiểm thử UI Compose), track Mã sạch (TDD, thiết kế test).
# Trần: 8 mục, mục cơ chế ≤ 4 khối.

SEC_ORDER = {'g10': ['hook', 'pyramid', 'doubles', 'layers', 'bugs', 'ex', 'recall']}


def add(a):
    def B(ch, sec, n, field, vi, en=None):
        a('%s.sec.%s.b.%02d.%s' % (ch, sec, n, field), vi, vi if en is None else en)

    m = lambda k, vi, en=None: a('m.testing.' + k, vi, en)
    m('title', 'Test từng tầng của màn Đặt lịch', 'Testing each layer of the Booking screen')
    m('overview', 'Bốn chỗ cần test: ViewModel, repository, DAO của Room, và giao diện. Hai cách: (1) mọi test dùng phụ thuộc thật, kể cả mạng và máy chủ; (2) mỗi tầng thay phụ thuộc của nó bằng fake, chỉ một số ít test chạy trên thiết bị. Mỗi bước xem một tầng.',
      'Four things to test: the ViewModel, the repository, the Room DAO, and the UI. Two approaches: (1) every test uses real dependencies, network and server included; (2) each layer replaces its dependencies with fakes, and only a few tests run on a device. Each step looks at one layer.')
    m('wrapup', 'Test dùng mạng thật thì chậm và chập chờn: mất mạng, máy chủ chậm hay dữ liệu đổi đều làm test trượt dù mã đúng. Nhờ các tầng nhận phụ thuộc qua constructor (G1, G6), mỗi tầng test được với fake trên JVM, nhanh và luôn cùng kết quả. Theo tháp kiểm thử: nhiều test nhỏ như vậy, ít test lớn trên thiết bị cho những gì chỉ thiết bị kiểm được.',
      'Tests that use the real network are slow and flaky: being offline, a slow server or changed data all make a test fail although the code is right. Because layers receive dependencies through constructors (G1, G6), each layer can be tested with fakes on the JVM, fast and with the same result every time. Following the testing pyramid: many such small tests, few big device tests for what only a device can check.')
    m('simp.1', 'Thời gian chạy ghi theo cấp (mili giây, giây, phút), không phải số đo; thời gian thật tùy máy và dự án. Nguyên tắc theo tài liệu chính thức của Android về kiểm thử (đọc ngày 2026-11-24). Chương chưa nói về screenshot test (so ảnh chụp màn hình), test hiệu năng, cấu hình CI (máy chạy test tự động), và cách test coroutine và giao diện chi tiết: xem chương A9, "Trạng thái chung và kiểm thử coroutine", và B9, "Semantics, accessibility và kiểm thử UI".',
      'Run times are given as orders of magnitude (milliseconds, seconds, minutes), not measurements; real times depend on the machine and project. The principles follow the official Android testing docs (read on 2026-11-24). The chapter does not cover screenshot tests (comparing screen captures), performance tests, CI setup (machines that run tests automatically), or testing coroutines and UI in detail: see chapters A9, "Shared state and testing coroutines", and B9, "Semantics, accessibility and UI testing".')
    m('ctl.hint', 'Đổi cách test rồi đi lại bốn bước; xem tab "Ma trận kiểm thử".', 'Switch the testing approach and walk the four steps again; watch the "Test matrix" tab.')
    m('ctl.case', 'Cách test', 'Testing approach')
    m('ctl.case.real', 'phụ thuộc thật, cả mạng', 'real dependencies, network included'); m('ctl.case.fakes', 'fake cho từng tầng', 'fakes for each layer')
    m('diagramTitle', 'Test, ViewModel, repository, mạng, database', 'Test, ViewModel, repository, network, database')
    m('diagramDesc', 'Test gọi vào một tầng; tầng đó gọi tiếp các phụ thuộc thật hay giả', 'The test calls into one layer; that layer calls its real or fake dependencies')
    for k, vi, en in [('test', 'Test', 'Test'), ('vm', 'BookingViewModel', 'BookingViewModel'), ('repo', 'SlotRepository', 'SlotRepository'), ('api', 'Nguồn mạng', 'Network source'), ('dao', 'Room DAO', 'Room DAO')]:
        m('n.' + k, vi, en)
    m('met.where', 'Test chạy ở', 'The test runs on'); m('met.time', 'Thời gian', 'Time'); m('met.stable', 'Kết quả', 'Result')
    for k, vi, en in [('jvm', 'JVM (máy phát triển)', 'the JVM (your machine)'), ('jvmNet', 'JVM, nhưng cần mạng', 'the JVM, but needs the network'), ('device', 'thiết bị hay máy ảo', 'a device or emulator'), ('deviceOrRobo', 'thiết bị, hay Robolectric', 'a device, or Robolectric')]:
        m('where.' + k, vi, en)
    for k, vi, en in [('millis', 'mili giây', 'milliseconds'), ('seconds', 'vài giây', 'seconds'), ('minutes', 'vài phút', 'minutes')]:
        m('time.' + k, vi, en)
    for k, vi, en in [('stable', 'luôn như nhau', 'always the same'), ('flaky', 'lúc qua lúc trượt', 'passes or fails at random')]:
        m('stable.' + k, vi, en)
    a('cap.testing', 'Từ trái sang phải: test, ViewModel, repository, rồi mạng và database. Khối viền đỏ là phụ thuộc làm test chập chờn; khối mờ là phần không tham gia test của bước này.',
      'Left to right: the test, the ViewModel, the repository, then network and database. A red-outlined box is a dependency that makes the test flaky; a faded box takes no part in this step\'s test.')
    S = [
        ('real', 's1', 'Test ViewModel với repository và mạng thật', 'Testing the ViewModel with the real repository and network',
         'BookingViewModel nhận SlotRepository thật, gọi máy chủ thật. Test kiểm hôm nay có 2 giờ trống. Nó chạy trên JVM nhưng phải có mạng và mất vài giây.',
         'BookingViewModel gets the real SlotRepository, calling the real server. The test checks there are 2 free slots today. It runs on the JVM but needs the network and takes seconds.'),
        ('real', 's2', 'Test repository: lúc qua lúc trượt', 'Testing the repository: passes or fails at random',
         'Mất mạng, máy chủ chậm quá thời gian chờ, hay ai đó vừa đặt một giờ: test trượt dù mã không đổi. Người chạy test học cách bấm chạy lại, và test mất giá trị.',
         'Offline, the server timing out, or someone just booking a slot: the test fails though the code did not change. People learn to hit re-run, and the test loses its value.'),
        ('real', 's3', 'Test DAO với Room thật: hợp lý', 'Testing the DAO with real Room: reasonable',
         'Test truy vấn của DAO cần Room thật, chạy trên thiết bị với một database tạm. Chậm hơn JVM nhưng ổn định, vì không phụ thuộc mạng.',
         'Testing DAO queries needs real Room, run on a device with a temporary database. Slower than the JVM but stable, since it does not touch the network.'),
        ('real', 's4', 'Test giao diện toàn app với mạng thật: phút, chập chờn', 'Testing the UI across the whole app with the real network: minutes, flaky',
         'Test giao diện dựng cả app trên thiết bị và gọi máy chủ thật. Chạy mất vài phút và trượt mỗi khi mạng không ổn. Nếu hầu hết test đều kiểu này, lỗi chỉ bị bắt sau nhiều giờ.',
         'The UI test builds the whole app on a device and calls the real server. It takes minutes and fails whenever the network wobbles. If most tests look like this, bugs are only caught hours later.'),
        ('fakes', 's1', 'ViewModel với FakeSlotRepository', 'The ViewModel with FakeSlotRepository',
         'FakeSlotRepository cài đặt cùng interface, giữ danh sách trong bộ nhớ, nằm trong source set test. Test chạy trên JVM trong vài mili giây và luôn cùng kết quả.',
         'FakeSlotRepository implements the same interface, keeps the list in memory and lives in the test source set. The test runs on the JVM in milliseconds with the same result every time.'),
        ('fakes', 's2', 'Repository với nguồn mạng giả và DAO giả', 'The repository with a fake network source and a fake DAO',
         'Test repository thay SlotApi bằng FakeSlotApi (trả dữ liệu hay ném IOException theo ý test) và DAO bằng bản trong bộ nhớ. Kiểm được cả nhánh mất mạng của G8 mà không cần tắt mạng.',
         'The repository test swaps SlotApi for FakeSlotApi (returning data or throwing IOException as the test wants) and the DAO for an in-memory version. It can even check G8\'s offline branch without turning off the network.'),
        ('fakes', 's3', 'DAO với Room trong bộ nhớ', 'The DAO with in-memory Room',
         'Truy vấn SQL chỉ kiểm thật được với Room. Dùng database trong bộ nhớ, trên thiết bị hay Robolectric: chậm hơn JVM thuần nhưng ổn định.',
         'SQL queries can only really be checked with Room. Use an in-memory database, on a device or Robolectric: slower than plain JVM but stable.'),
        ('fakes', 's4', 'Vài test giao diện, ViewModel dùng repository giả', 'A few UI tests, with the ViewModel on a fake repository',
         'Test Compose dựng màn Đặt lịch với ViewModel nhận repository giả. Ít test, chạy trên thiết bị, chỉ cho những gì cần giao diện thật: bấm nút, đọc chữ trên màn hình.',
         'A Compose test builds the Booking screen with a ViewModel on a fake repository. Few tests, on a device, only for what needs the real UI: tapping buttons, reading on-screen text.'),
    ]
    for case, k, tv, te, xv, xe in S:
        sid = case + '.' + k
        m('s.%s.title' % sid, tv, te); m('s.%s.explain' % sid, xv, xe); m('ev.' + sid, tv, te)
    for k, vi, en in [
        ('try', 'Đi bốn bước của mỗi cách; xem cột "Kết quả" trong ma trận.', 'Walk the four steps of each approach; watch the "Result" column in the matrix.'),
        ('real.s2', 'Tài liệu Android nói: test nhỏ tập trung vào một phần mã nên nhanh và tin cậy; test lớn có phạm vi rộng, cần dựng phức tạp và khó giữ. [[src:ax-test-strategies]]', 'The Android docs say: small tests focus on a small portion of code, so they are fast and reliable; big tests have a broad scope and need complex setups that are hard to maintain. [[src:ax-test-strategies]]'),
        ('real.s3', 'Test instrumented chạy trên thiết bị thật hay giả lập; dùng khi cần API của Android như Room thật. [[src:ax-test-fundamentals]]', 'Instrumented tests run on a physical or emulated device; use them when Android APIs such as real Room are needed. [[src:ax-test-fundamentals]]'),
        ('real.s4', 'Tài liệu tả một chiến lược kém hiệu quả: quá nhiều test end-to-end, quá ít test nhỏ, nên lỗi chỉ bị bắt khi test đêm hay tuần chạy. [[src:ax-test-strategies]]', 'The docs describe an inefficient strategy: too many end-to-end tests, too few small ones, so bugs are only caught when nightly or weekly tests run. [[src:ax-test-strategies]]'),
        ('fakes.s2', 'Tài liệu Android nói: fake (bản giả) có cài đặt chạy được nhưng chỉ hợp cho test, không cần thư viện mock và nhẹ; được ưu tiên. [[src:ax-test-doubles]]', 'The Android docs say: a fake has a working implementation fit only for tests, needs no mocking framework and is lightweight; it is preferred. [[src:ax-test-doubles]]'),
        ('fakes.s3', 'Kiểm một phần tử khi tách riêng: ViewModel không cần máy ảo hay giao diện vì nó không (hay không nên) phụ thuộc framework Android. [[src:ax-test-doubles]]', 'Test an element in isolation: a ViewModel needs no emulator or UI because it does not (or should not) depend on the Android framework. [[src:ax-test-doubles]]'),
        ('fakes.s4', 'Phần lớn app nên có nhiều test nhỏ và tương đối ít test lớn, thành hình tháp. Lỗi bắt bằng unit test thường sửa trong vài phút. [[src:ax-test-strategies]]', 'Most apps should have many small tests and relatively few big ones, forming a pyramid. A bug caught by a unit test is usually fixed in minutes. [[src:ax-test-strategies]]')]:
        m('co.' + k, vi, en)
    a('preset.testing', 'Kiến trúc · test theo tầng: mạng thật so với fake', 'Architecture · testing by layer: real network versus fakes')

    z = lambda k, vi, en=None: a('vz.' + k, vi, en)
    z('tab.ts', 'Ma trận kiểm thử', 'Test matrix')
    z('ts.cap', 'Mỗi hàng là test của một tầng; các cột cho biết test chạy ở đâu, phụ thuộc được thay bằng gì, mất bao lâu và có ổn định không. Hàng hiện dần theo bước.', 'Each row is the test of one layer; the columns show where it runs, what replaces its dependencies, how long it takes and whether it is stable. Rows appear step by step.')
    z('ts.legend', 'Ô đỏ: test phụ thuộc mạng hay chập chờn. Thời gian ghi theo cấp, không phải số đo.', 'Red cell: the test depends on the network or is flaky. Times are orders of magnitude, not measurements.')
    for k, vi, en in [('layer', 'Tầng được test', 'Layer under test'), ('where', 'Chạy ở', 'Runs on'), ('double', 'Phụ thuộc thay bằng', 'Dependencies replaced by'), ('time', 'Thời gian', 'Time'), ('stable', 'Kết quả', 'Result')]:
        z('ts.col.' + k, vi, en)
    for k, vi, en in [('vm', 'ViewModel', 'ViewModel'), ('repo', 'Repository', 'Repository'), ('dao', 'DAO (Room)', 'DAO (Room)'), ('ui', 'Giao diện (Compose)', 'UI (Compose)')]:
        z('ts.row.' + k, vi, en)
    for k, vi, en in [('jvm', 'JVM', 'the JVM'), ('jvmNet', 'JVM + mạng thật', 'JVM + the real network'), ('device', 'thiết bị', 'a device'), ('deviceOrRobo', 'thiết bị hay Robolectric', 'a device or Robolectric')]:
        z('ts.where.' + k, vi, en)
    for k, vi, en in [('realRepo', 'không thay: repository và máy chủ thật', 'nothing: the real repository and server'), ('realApi', 'không thay: API thật', 'nothing: the real API'), ('roomTemp', 'Room thật, database tạm', 'real Room, a temporary database'),
                      ('wholeApp', 'không thay: cả app và máy chủ', 'nothing: the whole app and server'), ('fakeRepo', 'FakeSlotRepository', 'FakeSlotRepository'), ('fakeApiDao', 'FakeSlotApi + DAO trong bộ nhớ', 'FakeSlotApi + an in-memory DAO'),
                      ('roomMemory', 'Room trong bộ nhớ', 'in-memory Room'), ('fakeVmRepo', 'ViewModel với repository giả', 'a ViewModel with a fake repository')]:
        z('ts.double.' + k, vi, en)
    for k, vi, en in [('millis', 'mili giây', 'milliseconds'), ('seconds', 'vài giây', 'seconds'), ('minutes', 'vài phút', 'minutes')]:
        z('ts.time.' + k, vi, en)
    for k, vi, en in [('stable', 'luôn như nhau', 'always the same'), ('flaky', 'chập chờn', 'flaky')]:
        z('ts.stable.' + k, vi, en)

    C = 'g10'
    a(C + '.title', 'Kiểm thử theo tầng', 'Testing by layer')
    a(C + '.essence', 'Lý do lớn nhất để tách tầng là test được từng phần riêng. Mỗi tầng nhận phụ thuộc qua constructor, nên test thay chúng bằng test double, thường là fake: một cài đặt đơn giản trong bộ nhớ.\nTest dùng fake chạy trên JVM, nhanh và luôn cùng kết quả. Test dùng mạng thật thì chậm và chập chờn: trượt vì mạng chứ không vì mã.\nTháp kiểm thử: rất nhiều test nhỏ (ViewModel, use case, repository), ít test vừa (DAO với Room, giao diện một màn), rất ít test lớn đầu tới cuối trên thiết bị.',
      'The biggest reason to split layers is testing each part on its own. Each layer receives its dependencies through its constructor, so tests replace them with test doubles, usually fakes: simple in-memory implementations.\nTests with fakes run on the JVM, fast and with the same result every time. Tests on the real network are slow and flaky: they fail because of the network, not the code.\nThe testing pyramid: very many small tests (ViewModel, use case, repository), fewer medium ones (DAO with Room, one screen\'s UI), very few big end-to-end tests on a device.')
    a(C + '.goal.g1', 'Đã thấy test chập chờn vì mạng', 'Saw a test go flaky because of the network')
    a(C + '.goal.g2', 'Đã đi hết bốn bước', 'Walked all four steps')
    a(C + '.sim.arch.testing', 'test từng tầng của màn Đặt lịch', 'testing each layer of the Booking screen')

    S_ = 'hook'
    a(C + '.sec.%s.title' % S_, 'Đoán trước khi đọc', 'Predict before reading')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'predict', 'Test BookingViewModel dùng repository thật gọi máy chủ thử nghiệm, kiểm hôm nay có đúng 2 giờ trống. Hôm qua test qua. Sáng nay nó trượt dù không ai sửa mã. Vì sao có thể như vậy?',
      'A BookingViewModel test uses the real repository calling a staging server, and checks there are exactly 2 free slots today. Yesterday it passed. This morning it fails though nobody changed the code. How can that be?')
    B(C, S_, 1, 'ans', 'Test phụ thuộc thứ nằm ngoài mã: mạng, tốc độ máy chủ, dữ liệu trên máy chủ (ai đó vừa đặt một giờ). Test trượt vì môi trường chứ không vì lỗi. Mô phỏng bên dưới so cách này với dùng fake cho từng tầng. [[src:ax-test-strategies]]',
      'The test depends on things outside the code: the network, server speed, the data on the server (someone just booked a slot). It fails because of the environment, not a bug. The simulation below compares this with fakes for each layer. [[src:ax-test-strategies]]')

    S_ = 'pyramid'
    a(C + '.sec.%s.title' % S_, 'Tháp kiểm thử', 'The testing pyramid')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'p', 'Tài liệu chia test theo kích cỡ. Test nhỏ tập trung vào một phần mã nên nhanh và tin cậy. Test lớn có phạm vi rộng, cần dựng phức tạp, khó giữ, nhưng có độ trung thực cao (môi trường gần với thật) nên tìm được nhiều lỗi một lần. Phần lớn app nên có nhiều test nhỏ và tương đối ít test lớn: hình tháp. [[src:ax-test-strategies]]',
      'The docs sort tests by size. Small tests focus on a small portion of code, so they are fast and reliable. Big tests have a broad scope and need complex, hard-to-maintain setups, but have higher fidelity (an environment closer to production) and find many issues at once. Most apps should have many small tests and relatively few big ones: a pyramid. [[src:ax-test-strategies]]')
    B(C, S_, 2, 'p', 'Lý do là giá của một lỗi. Lỗi bắt bằng unit test thường sửa trong vài phút; cùng lỗi đó nếu chỉ test end-to-end bắt được thì có thể mất nhiều ngày và kéo nhiều người vào; lọt ra người dùng thì bản sửa mất hàng tuần mới tới máy họ. Nên thêm test càng sớm càng tốt, bắt đầu từ test nhỏ, dù không thể test mọi thứ bằng unit test. Test local chạy trên máy phát triển; test instrumented chạy trên thiết bị hay máy ảo. [[src:ax-test-strategies]] [[src:ax-test-fundamentals]]',
      'The reason is the cost of a bug. A bug caught by a unit test is usually fixed in minutes; the same bug caught only by an end-to-end test can take days and pull in several people; if it reaches users, the fix takes weeks to land on their devices. Add tests as early as possible, starting small, even though not everything can be unit tested. Local tests run on the development machine; instrumented tests run on a device or emulator. [[src:ax-test-strategies]] [[src:ax-test-fundamentals]]')

    S_ = 'doubles'
    a(C + '.sec.%s.title' % S_, 'Test double: fake, mock và các loại khác', 'Test doubles: fakes, mocks and others')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'p', 'Khi test một phần tử, ta tách nó ra: ViewModel không cần máy ảo vì nó không nên phụ thuộc framework Android. Phụ thuộc của nó được thay bằng test double. Fake có cài đặt chạy được nhưng chỉ hợp cho test (ví dụ database trong bộ nhớ); không cần thư viện mock, nhẹ, và được ưu tiên. Mock được lập trình hành vi và có kỳ vọng về tương tác (ví dụ một hàm được gọi đúng một lần). Stub được lập trình mà không kiểm tương tác; dummy chỉ để điền tham số; spy bọc object thật để ghi lại lời gọi. [[src:ax-test-doubles]]',
      'To test an element, isolate it: a ViewModel needs no emulator because it should not depend on the Android framework. Its dependencies are replaced with test doubles. A fake has a working implementation fit only for tests (for example an in-memory database); it needs no mocking framework, is lightweight, and is preferred. A mock is preprogrammed and has expectations about interactions (for example a method called exactly once). A stub is preprogrammed without checking interactions; a dummy only fills a parameter; a spy wraps a real object to record calls. [[src:ax-test-doubles]]')
    B(C, S_, 2, 'kt', 'class FakeSlotRepository : SlotRepository {           // nằm trong src/test\n    val slots = MutableStateFlow(listOf(slot9h, slot930))\n    var failNext: IOException? = null                 // để test nhánh lỗi (G8)\n    override fun slots(day: LocalDate): Flow<List<Slot>> = slots\n    override suspend fun book(s: Slot): BookResult =\n        failNext?.let { BookResult.Failed(BookingFailure.Offline) } ?: BookResult.Booked\n}',
      'class FakeSlotRepository : SlotRepository {           // lives in src/test\n    val slots = MutableStateFlow(listOf(slot9h, slot930))\n    var failNext: IOException? = null                 // to test the error branch (G8)\n    override fun slots(day: LocalDate): Flow<List<Slot>> = slots\n    override suspend fun book(s: Slot): BookResult =\n        failNext?.let { BookResult.Failed(BookingFailure.Offline) } ?: BookResult.Booked\n}')
    B(C, S_, 3, 'note', 'Định nghĩa các loại test double khác nhau giữa các nguồn; tài liệu Android dẫn bài "Mocks Aren\'t Stubs" của Martin Fowler làm nguồn đầy đủ. Test kiểm từng lời gọi của mock dễ vỡ khi refactor dù hành vi không đổi; track Mã sạch (thiết kế test) nói kỹ hơn. [[src:ax-test-doubles]]', 'Definitions of test doubles conflict between sources; the Android docs point to Martin Fowler\'s "Mocks Aren\'t Stubs" as a comprehensive one. Tests that check every mock call break easily on refactoring even when behaviour is unchanged; the clean code track (test design) goes deeper. [[src:ax-test-doubles]]')

    S_ = 'layers'
    a(C + '.sec.%s.title' % S_, 'Mỗi tầng test thế nào', 'How each layer is tested')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'p', 'ViewModel và use case: test local trên JVM, repository giả, coroutine chạy bằng runTest với thời gian ảo (track Coroutines A9). Repository: test local, nguồn mạng giả và DAO giả, kiểm cả nhánh lỗi. DAO: cần Room thật nên dùng database trong bộ nhớ, trên thiết bị hay Robolectric. Giao diện một màn: test Compose với ViewModel nhận repository giả (track Runtime B9). Đầu tới cuối: vài test cho luồng quan trọng nhất, chạy trên thiết bị. [[src:ax-test-doubles]] [[src:ax-test-fundamentals]]',
      'ViewModels and use cases: local tests on the JVM, a fake repository, coroutines run with runTest on virtual time (Coroutines track A9). Repositories: local tests with a fake network source and fake DAO, error branches included. DAOs: need real Room, so an in-memory database on a device or Robolectric. A single screen\'s UI: a Compose test with the ViewModel on a fake repository (Runtime track B9). End to end: a few tests for the most important flows, on a device. [[src:ax-test-doubles]] [[src:ax-test-fundamentals]]')
    B(C, S_, 2, 'p', 'Tất cả chỉ làm được khi kiến trúc cho phép: phụ thuộc vào qua constructor (G1, G6), repository là interface hay có thể thay (G2, G9), thời gian nhận qua Clock (G5). Một Activity làm mọi thứ (G1) chỉ test được bằng test lớn trên thiết bị.', 'All of this only works if the architecture allows it: dependencies come in through constructors (G1, G6), the repository is an interface or otherwise replaceable (G2, G9), and time comes from a Clock (G5). An Activity that does everything (G1) can only be tested with big device tests.')

    S_ = 'bugs'
    a(C + '.sec.%s.title' % S_, 'Hai lỗi hay gặp', 'Two common bugs')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'bug', 'Bộ test trên CI trượt vài lần mỗi tuần, chạy lại thì qua; không ai còn tin kết quả test.', 'The CI test suite fails a few times a week and passes on re-run; nobody trusts the results any more.')
    B(C, S_, 1, 'cause', 'Test ViewModel và repository gọi máy chủ thật, nên phụ thuộc mạng, tốc độ máy chủ và dữ liệu trên đó.', 'The ViewModel and repository tests call the real server, so they depend on the network, server speed and server data.')
    B(C, S_, 1, 'fix', 'Thay nguồn mạng bằng fake ở test repository, và repository bằng fake ở test ViewModel; để mạng thật cho vài test đầu tới cuối.', 'Replace the network source with a fake in repository tests and the repository with a fake in ViewModel tests; keep the real network for a few end-to-end tests.')
    B(C, S_, 2, 'bug', 'Bộ test mất 40 phút, nên chỉ chạy ban đêm; lỗi phát hiện trễ một ngày.', 'The test suite takes 40 minutes, so it only runs at night; bugs are found a day late.')
    B(C, S_, 2, 'cause', 'Hầu hết test là test giao diện toàn app trên máy ảo, rất ít unit test: tháp lộn ngược.', 'Most tests are whole-app UI tests on emulators, with very few unit tests: an upside-down pyramid.')
    B(C, S_, 2, 'fix', 'Chuyển phần logic xuống test local trên JVM với fake; chỉ giữ test giao diện cho những gì cần giao diện thật.', 'Move logic checks down to local JVM tests with fakes; keep UI tests only for what needs the real UI.')

    S_ = 'ex'
    a(C + '.sec.%s.title' % S_, 'Bài tập', 'Exercise')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'ex', 'Viết FakeSlotApi cho test SlotRepository, sao cho test chọn được: trả danh sách, ném IOException, hay trả HTTP 409. Rồi liệt kê ba test cho hàm book() của repository (theo các failure của G8). Test nào chạy trên JVM, test nào cần thiết bị? (Bài tập của site, theo trang Use test doubles.) [[src:ax-test-doubles]]',
      'Write a FakeSlotApi for SlotRepository tests, letting the test choose: return a list, throw IOException, or return HTTP 409. Then list three tests for the repository\'s book() (following G8\'s failures). Which run on the JVM, which need a device? (The site\'s own exercise, after the Use test doubles page.) [[src:ax-test-doubles]]')
    B(C, S_, 1, 'hint', 'Fake có một trường "kết quả lần tới" mà test đặt trước khi gọi.', 'Give the fake a "next result" field the test sets before calling.')
    B(C, S_, 1, 'sol', 'FakeSlotApi có var next: Next (Ok(slots), Offline, Conflict). Ba test: book trả Booked khi Ok; trả Failed(Offline) khi Offline; trả Failed(SlotTaken) khi Conflict. Cả ba chạy trên JVM với runTest, vì repository không cần Android khi DAO cũng là fake.',
      'FakeSlotApi has var next: Next (Ok(slots), Offline, Conflict). Three tests: book returns Booked on Ok; Failed(Offline) on Offline; Failed(SlotTaken) on Conflict. All three run on the JVM with runTest, since the repository needs no Android when the DAO is a fake too.')

    S_ = 'recall'
    a(C + '.sec.%s.title' % S_, 'Tự trả lời', 'Answer it yourself')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'ask', 'Vì sao test gọi máy chủ thật lại chập chờn?', 'Why are tests that call a real server flaky?')
    B(C, S_, 1, 'ans', 'Kết quả phụ thuộc mạng, tốc độ và dữ liệu máy chủ, không chỉ phụ thuộc mã.', 'The result depends on the network, server speed and server data, not just the code.')
    B(C, S_, 2, 'ask', 'Loại test double nào được tài liệu ưu tiên, và vì sao?', 'Which test double do the docs prefer, and why?')
    B(C, S_, 2, 'ans', 'Fake: cài đặt chạy được, nhẹ, không cần thư viện mock.', 'Fakes: working implementations, lightweight, no mocking framework.')

    for q, qv, qe, av, ae, wv, we in [
        ('q1', 'Tháp kiểm thử khuyên số lượng test nhỏ và test lớn thế nào?', 'What does the testing pyramid advise about small and big tests?', 'Nhiều test nhỏ, tương đối ít test lớn.', 'Many small tests, relatively few big ones.', 'Test nhỏ nhanh và tin cậy; lỗi bắt sớm rẻ hơn.', 'Small tests are fast and reliable; bugs caught early are cheaper.'),
        ('q2', 'Fake khác mock ở đâu?', 'How does a fake differ from a mock?', 'Fake có cài đặt chạy được; mock có kỳ vọng về tương tác.', 'A fake has a working implementation; a mock has expectations about interactions.', 'Tài liệu ưu tiên fake.', 'The docs prefer fakes.'),
        ('q3', 'Test ViewModel có cần máy ảo không?', 'Does a ViewModel test need an emulator?', 'Không; nó chạy trên JVM với repository giả.', 'No; it runs on the JVM with a fake repository.', 'ViewModel không nên phụ thuộc framework Android.', 'A ViewModel should not depend on the Android framework.'),
        ('q4', 'Test truy vấn của DAO chạy ở đâu?', 'Where do DAO query tests run?', 'Trên thiết bị hay Robolectric, với Room trong bộ nhớ.', 'On a device or Robolectric, with in-memory Room.', 'Truy vấn SQL cần Room thật.', 'SQL queries need real Room.')]:
        a(C + '.quiz.%s.q' % q, qv, qe); a(C + '.quiz.%s.a' % q, av, ae); a(C + '.quiz.%s.why' % q, wv, we)
