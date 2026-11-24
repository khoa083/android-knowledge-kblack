# Kiến trúc · G11: thêm tính năng mới và di trú dự án cũ (Phần 2)
# Nguồn: Boudjnah, Clean Architecture for Android ch.7 (Implementing a New Feature) và ch.8 (Migrating An Existing Project),
# đọc từ epub trong kho ngày 2026-11-24. Gom các chương G1–G10.
# Trần: 8 mục, mục cơ chế ≤ 4 khối.

SEC_ORDER = {'g11': ['hook', 'migrate', 'newfeature', 'order', 'bugs', 'ex', 'recall', 'honest']}


def add(a):
    def B(ch, sec, n, field, vi, en=None):
        a('%s.sec.%s.b.%02d.%s' % (ch, sec, n, field), vi, vi if en is None else en)

    m = lambda k, vi, en=None: a('m.feature.' + k, vi, en)
    m('title', 'Đổi kiến trúc mà không dừng phát hành', 'Changing the architecture without stopping releases')
    m('overview', 'App Hẹn Khám có năm màn viết theo kiểu cũ: Chọn giờ, Lịch của tôi, Lịch sử, Hồ sơ, Thanh toán. Ba tình huống: (1) mở nhánh viết lại cả app; (2) di trú dần từng màn, mỗi màn một bản phát hành; (3) thêm tính năng mới Hủy lịch theo từng tầng.',
      'ClinicBook has five screens written the old way: Choose a time, My appointments, History, Profile, Payment. Three cases: (1) open a branch to rewrite the whole app; (2) migrate screen by screen, one release per screen; (3) add a new Cancel appointment feature layer by layer.')
    m('wrapup', 'Viết lại cả app trên một nhánh riêng tạo ra hai codebase cùng thay đổi, và nhánh mới không phát hành được cho tới khi xong hết, nên dễ bị bỏ dở. Di trú dần thì mỗi bước đều có bản phát hành: trước hết viết test cho điều người dùng thấy và làm được, rồi đặt repository sau interface, rút logic ra use case, và để test cũ chứng minh hành vi không đổi. Tính năng mới đi theo thứ tự domain, presentation, UI, rồi data, với repository stub trong lúc chờ.',
      'Rewriting the whole app on a separate branch creates two codebases changing at once, and the new branch cannot ship until everything is done, so it is easily abandoned. Gradual migration has a release at every step: first write tests for what the user sees and can do, then put the repository behind an interface, move logic into use cases, and let the old tests prove behaviour is unchanged. A new feature goes domain, presentation, UI, then data, with a stub repository meanwhile.')
    m('simp.1', 'Năm màn và các bước được rút gọn; một dự án thật có thể cần nhiều bước trung gian hơn cho mỗi màn.', 'The five screens and steps are simplified; a real project may need more intermediate steps per screen.')
    m('ctl.hint', 'Đổi cách làm rồi đi lại bốn bước; xem tab "Tiến độ".', 'Switch the approach and walk the four steps again; watch the "Progress" tab.')
    m('ctl.case', 'Cách làm', 'Approach')
    for k, vi, en in [('rewrite', 'viết lại cả app trên nhánh riêng', 'rewrite the whole app on a branch'), ('gradual', 'di trú dần từng màn', 'migrate screen by screen'), ('newfeature', 'thêm tính năng Hủy lịch theo tầng', 'add Cancel appointment layer by layer')]:
        m('ctl.case.' + k, vi, en)
    m('diagramTitle', 'Màn hình, ViewModel, use case, repository', 'Screen, ViewModel, use case, repository')
    m('diagramDesc', 'Các tầng mà một màn hay một tính năng đi qua', 'The layers a screen or feature passes through')
    for k, vi, en in [('ui', 'Màn hình', 'Screen'), ('vm', 'ViewModel', 'ViewModel'), ('uc', 'Use case', 'Use case'), ('repo', 'Repository', 'Repository')]:
        m('n.' + k, vi, en)
    m('met.ship', 'Có bản phát hành được', 'A shippable build'); m('met.done', 'Phần đã xong', 'Done so far'); m('met.tests', 'Có test bảo vệ', 'Guarded by tests')
    for k, vi, en in [('yes', 'có, ở mọi bước', 'yes, at every step'), ('mainOnly', 'chỉ nhánh cũ', 'only the old branch')]:
        m('ship.' + k, vi, en)
    for k, vi, en in [('yes', 'có', 'yes'), ('no', 'không', 'no')]:
        m('yn.' + k, vi, en)
    a('cap.feature', 'Từ trái sang phải: màn hình, ViewModel, use case, repository. Khối mờ là tầng chưa có; khối viền đỏ là chỗ cách làm đang gây rủi ro. Tab "Tiến độ" theo dõi từng màn hay từng tầng.',
      'Left to right: screen, ViewModel, use case, repository. A faded box is a layer that does not exist yet; a red-outlined box is where the approach is creating risk. The "Progress" tab tracks each screen or layer.')
    S = [
        ('rewrite', 's1', 'Mở nhánh viết lại, đóng băng tính năng', 'Open a rewrite branch, freeze features',
         'Nhóm quyết định viết lại cả app theo kiến trúc mới trên một nhánh riêng. Nhánh chính tạm không nhận tính năng mới.',
         'The team decides to rewrite the whole app on the new architecture on a separate branch. Main temporarily takes no new features.'),
        ('rewrite', 's2', 'Nhánh chính vẫn phải sửa lỗi: hai nơi cùng đổi', 'Main still needs fixes: two places change',
         'Người dùng báo lỗi ở Chọn giờ và Lịch sử; nhánh chính phải sửa ngay. Nhánh viết lại có hai màn mới, nhưng phải tự áp lại các bản sửa đó.',
         'Users report bugs in Choose a time and History; main must fix them now. The rewrite branch has two new screens, but must re-apply those fixes itself.'),
        ('rewrite', 's3', 'Kinh doanh cần Thanh toán ngay: hai nhánh lệch nhau', 'Business needs Payment now: the branches diverge',
         'Thanh toán được làm trên nhánh chính vì không thể chờ. Nhánh viết lại có ba màn, thiếu Hồ sơ và Thanh toán, và chưa phát hành được.',
         'Payment is built on main because it cannot wait. The rewrite branch has three screens, lacks Profile and Payment, and still cannot ship.'),
        ('rewrite', 's4', 'Sau nhiều tháng: nhánh viết lại bị bỏ dở', 'Months later: the rewrite branch is abandoned',
         'Khoảng cách giữa hai nhánh lớn tới mức hợp nhất quá tốn. Nhánh viết lại bị bỏ; app vẫn ở kiến trúc cũ, cộng thêm thời gian đã mất.',
         'The gap between the branches grows too costly to merge. The rewrite branch is dropped; the app stays on the old architecture, plus the lost time.'),
        ('gradual', 's1', 'Bắt đầu bằng test cho màn Lịch sử', 'Start with tests for the History screen',
         'Trước khi đổi gì, viết test cho điều người dùng thấy (danh sách lượt khám) và làm được (hủy một lượt). Các test này phải qua với mã cũ.',
         'Before changing anything, write tests for what the user sees (the visit list) and can do (cancel a visit). These tests must pass against the old code.'),
        ('gradual', 's2', 'Đặt repository sau interface, rút logic ra use case', 'Put the repository behind an interface, move logic into use cases',
         'ViewModel cũ gọi thẳng repository. Thêm interface VisitHistoryRepository và GetVisitHistoryUseCase; HistoryViewModel chuyển sang dùng use case. Test cũ vẫn qua, nên hành vi không đổi. Phát hành.',
         'The old ViewModel called the repository directly. Add a VisitHistoryRepository interface and GetVisitHistoryUseCase; HistoryViewModel switches to the use case. The old tests still pass, so behaviour is unchanged. Ship.'),
        ('gradual', 's3', 'Màn tiếp theo, bản phát hành tiếp theo', 'The next screen, the next release',
         'Lặp lại cho Lịch của tôi. Mỗi bước nhỏ, có test, và app luôn ở trạng thái phát hành được.',
         'Repeat for My appointments. Each step is small and tested, and the app is always shippable.'),
        ('gradual', 's4', 'Sau vài bản phát hành: cả năm màn đã chuyển', 'After a few releases: all five screens migrated',
         'Không có ngày "chuyển đổi lớn" nào. Tính năng mới vẫn được làm song song, viết thẳng theo kiến trúc mới.',
         'There was no big switch-over day. New features kept being built alongside, written directly on the new architecture.'),
        ('newfeature', 's1', 'Domain trước: use case và interface repository', 'Domain first: the use case and repository interface',
         'Tính năng Hủy lịch bắt đầu từ CancelAppointmentUseCase và interface CancelAppointmentRepository. Đây là phần mô tả yêu cầu nghiệp vụ, test được ngay.',
         'Cancel appointment starts with CancelAppointmentUseCase and the CancelAppointmentRepository interface. This part describes the business requirement and is testable right away.'),
        ('newfeature', 's2', 'Presentation với repository stub', 'Presentation with a stub repository',
         'ViewModel và UiState dùng use case; một StubCancelRepository luôn trả "đã hủy" để chạy được ngay, trong khi tầng data làm song song.',
         'The ViewModel and UiState use the use case; a StubCancelRepository always returns "cancelled" so it runs right away, while the data layer is built in parallel.'),
        ('newfeature', 's3', 'Giao diện: thử được tính năng trước khi có máy chủ', 'UI: the feature can be tried before the server exists',
         'Nút Hủy và hộp xác nhận nối vào ViewModel. Người làm sản phẩm thử được luồng dù API hủy lịch chưa xong.',
         'The Cancel button and confirmation dialog connect to the ViewModel. Product people can try the flow before the cancel API is ready.'),
        ('newfeature', 's4', 'Data thật thay stub, nối điều hướng', 'The real data layer replaces the stub; wire navigation',
         'OfflineFirstCancelRepository (Room và API) thay stub qua DI; nối điều hướng từ Lịch của tôi. Mỗi bước là commit nhỏ, không phá phần đang chạy.',
         'OfflineFirstCancelRepository (Room and API) replaces the stub through DI; navigation is wired from My appointments. Each step is a small commit that does not break what already runs.'),
    ]
    for case, k, tv, te, xv, xe in S:
        sid = case + '.' + k
        m('s.%s.title' % sid, tv, te); m('s.%s.explain' % sid, xv, xe); m('ev.' + sid, tv, te)
    for k, vi, en in [
        ('try', 'Đi bốn bước của từng cách; theo dõi cột "Có bản phát hành được".', 'Walk the four steps of each approach; watch "A shippable build".'),
        ('rewrite.s2', 'Boudjnah: di trú một kiến trúc có sẵn không có nghĩa là viết lại toàn bộ mã; nó chia được thành các bước nhỏ. [[src:book-boudjnah]]', 'Boudjnah: migrating an existing architecture does not have to mean a full rewrite of the code base; it can be broken into smaller steps. [[src:book-boudjnah]]'),
        ('rewrite.s3', 'Hai nhánh cùng thay đổi một app là hai nguồn sự thật cho chính mã nguồn: cùng kiểu lỗi của G2, ở mức dự án.', 'Two branches changing one app are two sources of truth for the code itself: G2\'s kind of bug, at project level.'),
        ('rewrite.s4', 'Nhận định "nhánh viết lại thường bị bỏ dở" là kinh nghiệm, không phải số liệu; chương dùng nó làm ví dụ, không đo.', '"Rewrite branches often get abandoned" is experience, not data; the chapter uses it as an example, not a measurement.'),
        ('gradual.s2', 'Boudjnah: trước khi đổi, bảo đảm có test; tìm các test của màn bằng hai câu hỏi: người dùng thấy gì và làm được gì trên màn này. [[src:book-boudjnah]]', 'Boudjnah: make sure you have good test coverage before changing anything; find a screen\'s tests by asking what the user can see and what they can do. [[src:book-boudjnah]]'),
        ('gradual.s3', 'Với MVVM, di trú là "thổi phồng" Model thành use case và repository interface; View và ViewModel giữ gần như nguyên. [[src:book-boudjnah]]', 'For MVVM, migration means inflating the Model into use cases and repository interfaces; the View and ViewModel stay mostly as they are. [[src:book-boudjnah]]'),
        ('gradual.s4', 'Boudjnah nhắc vì sao phải di trú: MVP và MVVM lớn lên thành god presenter hay god ViewModel, và ViewModel giữ repository thì presentation quá gần data. [[src:book-boudjnah]]', 'Boudjnah notes why migrate at all: MVP and MVVM grow into god presenters or god ViewModels, and a ViewModel holding repositories brings presentation too close to data. [[src:book-boudjnah]]'),
        ('newfeature.s2', 'Boudjnah: có thể cài một repository stub để cắm use case vào ViewModel ngay. Khi domain đã có, presentation và data làm song song được. [[src:book-boudjnah]]', 'Boudjnah: a stub repository lets you plug the use case into a ViewModel straight away. Once the domain exists, presentation and data can progress in parallel. [[src:book-boudjnah]]'),
        ('newfeature.s3', 'Chia tính năng theo tầng giúp tách thay đổi thành commit nhỏ không ảnh hưởng mã cho tới khi xong, và giữ độ phủ test cao. [[src:book-boudjnah]]', 'Splitting a feature by layer breaks the change into small commits that do not affect the code base until done, while keeping test coverage high. [[src:book-boudjnah]]'),
        ('newfeature.s4', 'Thứ tự Boudjnah đề xuất: domain, rồi presentation và data, cuối cùng UI và data source; "đừng đi tắt". Đây là thứ tự của tác giả theo Clean Architecture, không phải quy định của Google. [[src:book-boudjnah]]', 'Boudjnah\'s suggested order: domain, then presentation and data, finally UI and data sources; "don\'t take shortcuts". This is the author\'s Clean Architecture order, not a Google rule. [[src:book-boudjnah]]')]:
        m('co.' + k, vi, en)
    a('preset.feature', 'Kiến trúc · viết lại cả app so với di trú dần', 'Architecture · a full rewrite versus gradual migration')

    z = lambda k, vi, en=None: a('vz.' + k, vi, en)
    z('tab.ft', 'Tiến độ', 'Progress')
    z('ft.cap.screens', 'Mỗi ô là một màn của app, ghi trạng thái ở bước này. Ô có viền cam là ô vừa đổi.', 'Each chip is one of the app\'s screens with its state at this step. An orange-outlined chip just changed.')
    z('ft.cap.layers', 'Mỗi ô là một tầng của tính năng Hủy lịch, ghi trạng thái ở bước này. Ô có viền cam là ô vừa đổi.', 'Each chip is one layer of the Cancel appointment feature with its state at this step. An orange-outlined chip just changed.')
    z('ft.legend', 'Gạch chân xanh: đã theo kiến trúc mới hay đã xong. Viền đứt: chưa có. Đỏ: thiếu hay bị bỏ.', 'Green underline: on the new architecture or done. Dashed: not there yet. Red: missing or abandoned.')
    for k, vi, en in [('main', 'Nhánh chính (đang phát hành)', 'Main branch (shipping)'), ('rw', 'Nhánh viết lại', 'Rewrite branch'), ('layers', 'Tính năng Hủy lịch', 'Cancel appointment feature')]:
        z('ft.row.' + k, vi, en)
    for k, vi, en in [('choose', 'Chọn giờ', 'Choose a time'), ('mine', 'Lịch của tôi', 'My appointments'), ('history', 'Lịch sử', 'History'), ('profile', 'Hồ sơ', 'Profile'), ('pay', 'Thanh toán', 'Payment'),
                      ('domain', 'domain', 'domain'), ('present', 'presentation', 'presentation'), ('ui', 'giao diện', 'UI'), ('data', 'data', 'data')]:
        z('ft.item.' + k, vi, en)
    for k, vi, en in [('old', 'kiểu cũ', 'old style'), ('fixed', 'vừa sửa lỗi', 'just fixed'), ('new', 'kiến trúc mới', 'new architecture'), ('tested', 'đã có test', 'tests added'),
                      ('none', 'chưa có', 'not yet'), ('missing', 'thiếu', 'missing'), ('dead', 'bỏ dở', 'abandoned'), ('stub', 'stub', 'stubbed'), ('todo', 'chưa làm', 'to do'), ('done', 'xong', 'done')]:
        z('ft.st.' + k, vi, en)

    C = 'g11'
    a(C + '.title', 'Thêm tính năng mới và di trú dự án cũ', 'Adding a feature and migrating an old project')
    a(C + '.essence', 'Đổi kiến trúc không cần viết lại cả app. Di trú dần từng màn: viết test cho điều người dùng thấy và làm được, đặt repository sau interface, rút logic ra use case, để test cũ chứng minh hành vi không đổi, và phát hành sau mỗi màn.\nViết lại trên nhánh riêng tạo hai codebase cùng thay đổi và không phát hành được cho tới khi xong hết.\nTính năng mới đi theo tầng: domain trước, presentation chạy với repository stub, rồi giao diện, cuối cùng data thật thay stub. Mỗi bước là một commit nhỏ, có test.',
      'Changing the architecture does not require rewriting the whole app. Migrate screen by screen: write tests for what the user sees and can do, put the repository behind an interface, move logic into use cases, let the old tests prove behaviour is unchanged, and ship after each screen.\nRewriting on a separate branch creates two codebases changing at once that cannot ship until everything is done.\nA new feature goes layer by layer: domain first, presentation running against a stub repository, then the UI, finally the real data layer replacing the stub. Each step is a small, tested commit.')
    a(C + '.goal.g1', 'Đã thấy hai nhánh lệch nhau', 'Saw the two branches diverge')
    a(C + '.goal.g2', 'Đã đi hết bốn bước', 'Walked all four steps')
    a(C + '.sim.arch.feature', 'đổi kiến trúc mà không dừng phát hành', 'changing the architecture without stopping releases')

    S_ = 'hook'
    a(C + '.sec.%s.title' % S_, 'Đoán trước khi đọc', 'Predict before reading')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'predict', 'Nhóm muốn chuyển app Hẹn Khám từ "Activity làm mọi thứ" sang kiến trúc của track này. Ý kiến A: mở nhánh viết lại cả app, xong thì thay một lần. Ý kiến B: chuyển từng màn, mỗi màn một bản phát hành. Trong lúc đó người dùng vẫn báo lỗi và kinh doanh vẫn cần tính năng mới. Cách nào dễ đi tới đích hơn?',
      'The team wants to move ClinicBook from "an Activity doing everything" to this track\'s architecture. Option A: open a branch to rewrite the whole app and swap it in once done. Option B: move one screen at a time, one release per screen. Meanwhile users still report bugs and the business still needs new features. Which is more likely to reach the goal?')
    B(C, S_, 1, 'ans', 'B. Với A, nhánh chính vẫn phải sửa lỗi và thêm tính năng, nên hai codebase lệch nhau và nhánh mới không phát hành được cho tới khi đuổi kịp. Với B, mỗi bước đều có bản phát hành và có test bảo vệ. Mô phỏng bên dưới đi qua cả hai, cộng với cách thêm một tính năng mới. [[src:book-boudjnah]]',
      'B. With A, main still has to get fixes and features, so the two codebases diverge and the new branch cannot ship until it catches up. With B, every step has a release and is guarded by tests. The simulation below walks through both, plus how to add a new feature. [[src:book-boudjnah]]')

    S_ = 'migrate'
    a(C + '.sec.%s.title' % S_, 'Di trú dần một màn hình', 'Migrating one screen gradually')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'p', 'Boudjnah nói rõ: di trú một kiến trúc có sẵn không có nghĩa là viết lại toàn bộ; nó chia được thành các bước nhỏ. Lý do phải di trú: MVP và MVVM thường lớn lên thành god presenter hay god ViewModel, và ViewModel giữ thẳng repository làm presentation quá gần data. [[src:book-boudjnah]]',
      'Boudjnah is explicit: migrating an existing architecture does not have to mean a full rewrite; it can be broken into smaller steps. The reason to migrate: MVP and MVVM tend to grow into god presenters or god ViewModels, and a ViewModel holding repositories directly brings presentation too close to data. [[src:book-boudjnah]]')
    B(C, S_, 2, 'p', 'Các bước cho một màn MVVM: (1) trước khi đổi gì, bảo đảm có test; tìm chúng bằng hai câu hỏi "người dùng thấy gì" và "người dùng làm được gì" trên màn này. (2) Với mỗi điều đó, tạo một use case và interface repository tương ứng; phần Model cũ được "thổi phồng" thành các lớp đó, còn View và ViewModel giữ gần như nguyên. (3) ViewModel chuyển sang dùng use case; test cũ phải vẫn qua. (4) Phát hành, rồi sang màn tiếp theo. [[src:book-boudjnah]]',
      'Steps for one MVVM screen: (1) before changing anything, make sure there are tests; find them by asking "what can the user see" and "what can the user do" on this screen. (2) For each of those, create a use case and its repository interface; the old Model is inflated into those classes while the View and ViewModel stay mostly as they are. (3) The ViewModel switches to the use cases; the old tests must still pass. (4) Ship, then move to the next screen. [[src:book-boudjnah]]')

    S_ = 'newfeature'
    a(C + '.sec.%s.title' % S_, 'Thêm một tính năng mới theo tầng', 'Adding a new feature layer by layer')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'p', 'Boudjnah nêu ba lợi ích của việc chia tính năng theo tầng: dễ bắt đầu từ yêu cầu rồi xây hành vi quanh nó; chia được thành commit nhỏ không ảnh hưởng mã cho tới khi tính năng xong, mà vẫn giữ độ phủ test; và khi đã có domain, presentation và data làm song song được. Một repository stub cho phép cắm use case vào ViewModel ngay, trước khi tầng data xong. [[src:book-boudjnah]]',
      'Boudjnah gives three benefits of splitting a feature by layer: it is easy to start from the requirement and build behaviour around it; the change splits into small commits that do not affect the code base until the feature is done, while test coverage stays high; and once the domain exists, presentation and data can proceed in parallel. A stub repository lets you plug the use case into a ViewModel right away, before the data layer is done. [[src:book-boudjnah]]')
    B(C, S_, 2, 'kt', '// 1. domain\ninterface CancelAppointmentRepository { suspend fun cancel(id: Long): CancelResult }\nclass CancelAppointmentUseCase(private val repo: CancelAppointmentRepository) {\n    suspend operator fun invoke(id: Long) = repo.cancel(id)\n}\n// 2. presentation chạy được ngay với stub\nclass StubCancelRepository : CancelAppointmentRepository {\n    override suspend fun cancel(id: Long) = CancelResult.Cancelled\n}\n// 3. giao diện; 4. data thật thay stub qua DI (G6)',
      '// 1. domain\ninterface CancelAppointmentRepository { suspend fun cancel(id: Long): CancelResult }\nclass CancelAppointmentUseCase(private val repo: CancelAppointmentRepository) {\n    suspend operator fun invoke(id: Long) = repo.cancel(id)\n}\n// 2. presentation runs right away with a stub\nclass StubCancelRepository : CancelAppointmentRepository {\n    override suspend fun cancel(id: Long) = CancelResult.Cancelled\n}\n// 3. the UI; 4. the real data layer replaces the stub through DI (G6)')

    S_ = 'order'
    a(C + '.sec.%s.title' % S_, 'Ghép mọi chương lại', 'Putting the chapters together')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'p', 'Một tính năng hoàn chỉnh dùng mọi chương của track: tầng và hướng phụ thuộc (G2), UI state và sự kiện một lần như thông báo "Đã hủy" (G3), database làm nguồn sự thật và ghi lười khi mất mạng (G4), use case khi quy tắc được dùng lại (G5), nối bằng Hilt (G6), một state duy nhất cho màn (G7), failure có tên như "Không thể hủy trong vòng 2 giờ trước giờ khám" (G8), đặt trong feature module đúng chỗ (G9), và test ở từng tầng (G10).',
      'A complete feature uses every chapter of the track: layers and dependency direction (G2), UI state and one-off events such as the "Cancelled" message (G3), the database as source of truth and lazy writes when offline (G4), a use case when a rule is reused (G5), wiring with Hilt (G6), one single state for the screen (G7), named failures such as "Cannot cancel within 2 hours of the visit" (G8), placed in the right feature module (G9), and tests at each layer (G10).')
    B(C, S_, 2, 'note', 'Thứ tự domain trước là cách của sách Clean Architecture. Theo hướng dẫn của Google, domain là tùy chọn (G5); một nhóm theo hướng dẫn đó có thể bắt đầu từ repository và ViewModel. Điều chung của cả hai: chia nhỏ, có test ở mỗi bước, và luôn giữ app phát hành được.', 'Domain-first is the Clean Architecture books\' order. Under Google\'s guide the domain is optional (G5); a team following it may start from the repository and ViewModel. What both share: small steps, tests at each step, and an app that is always shippable.')

    S_ = 'bugs'
    a(C + '.sec.%s.title' % S_, 'Hai lỗi hay gặp', 'Two common bugs')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'bug', 'Sau khi "dọn kiến trúc" màn Lịch sử, nút Hủy không còn xóa lượt khám khỏi danh sách; không ai phát hiện cho tới khi người dùng báo.', 'After "cleaning up" the History screen, the Cancel button no longer removes the visit from the list; nobody notices until users report it.')
    B(C, S_, 1, 'cause', 'Đổi cấu trúc trước khi có test cho điều người dùng làm được trên màn, nên không gì báo hành vi đã đổi.', 'The structure was changed before there were tests for what the user can do on the screen, so nothing flagged the behaviour change.')
    B(C, S_, 1, 'fix', 'Viết test "hủy một lượt thì nó biến khỏi danh sách" với mã cũ trước, rồi mới di trú; test phải qua cả trước lẫn sau.', 'Write the test "cancelling a visit removes it from the list" against the old code first, then migrate; it must pass before and after.')
    B(C, S_, 2, 'bug', 'Tính năng Hủy lịch nằm trên nhánh riêng ba tuần, hợp nhất thì xung đột khắp nơi.', 'The Cancel feature lived on its own branch for three weeks and the merge conflicts everywhere.')
    B(C, S_, 2, 'cause', 'Tính năng được làm một lần cho mọi tầng rồi mới hợp nhất, thay vì từng tầng nhỏ.', 'The feature was built across all layers at once and merged at the end, instead of layer by layer.')
    B(C, S_, 2, 'fix', 'Hợp nhất từng tầng: domain và stub trước, rồi ViewModel, rồi giao diện (có thể ẩn sau cờ tính năng), cuối cùng data thật.', 'Merge layer by layer: domain and the stub first, then the ViewModel, then the UI (possibly behind a feature flag), finally the real data layer.')

    S_ = 'ex'
    a(C + '.sec.%s.title' % S_, 'Bài tập', 'Exercise')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'ex', 'Màn Hồ sơ cũ là một ProfileViewModel gọi thẳng UserRepository, đọc SharedPreferences và tự định dạng ngày sinh. Lập kế hoạch di trú bốn bước theo chương này: liệt kê test cần có trước, các use case và interface sẽ tạo, và điều phải đúng sau mỗi bước. (Bài tập của site, theo quy trình của Boudjnah .) [[src:book-boudjnah]]',
      'The old Profile screen is a ProfileViewModel calling UserRepository directly, reading SharedPreferences and formatting the birth date itself. Plan a four-step migration following this chapter: the tests needed first, the use cases and interfaces to create, and what must hold after each step. (The site\'s own exercise, after Boudjnah \'s process.) [[src:book-boudjnah]]')
    B(C, S_, 1, 'hint', 'Hỏi: người dùng thấy gì (tên, ngày sinh đã định dạng), làm được gì (sửa tên)?', 'Ask: what does the user see (name, formatted birth date), and what can they do (edit the name)?')
    B(C, S_, 1, 'sol', '(1) Test: hiện tên và ngày sinh dạng "12/03/1990"; sửa tên thì lưu và hiện tên mới. (2) Tạo GetProfileUseCase, UpdateNameUseCase, interface ProfileRepository; chuyển định dạng ngày vào FormatBirthDateUseCase nếu màn khác cũng dùng (G5). (3) ProfileViewModel dùng use case; SharedPreferences nằm sau repository (sau này đổi sang DataStore ở track Lưu dữ liệu). Test bước 1 vẫn qua. (4) Phát hành; màn tiếp theo.',
      '(1) Tests: show the name and the birth date as "12/03/1990"; editing the name saves and shows it. (2) Create GetProfileUseCase, UpdateNameUseCase, a ProfileRepository interface; move date formatting into FormatBirthDateUseCase if other screens use it (G5). (3) ProfileViewModel uses the use cases; SharedPreferences sits behind the repository (later moved to DataStore in the Saving Data track). Step 1\'s tests still pass. (4) Ship; next screen.')

    S_ = 'recall'
    a(C + '.sec.%s.title' % S_, 'Tự trả lời', 'Answer it yourself')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'ask', 'Việc đầu tiên trước khi di trú một màn là gì?', 'What comes first before migrating a screen?')
    B(C, S_, 1, 'ans', 'Viết test cho điều người dùng thấy và làm được, và cho chúng qua với mã cũ.', 'Write tests for what the user sees and can do, passing against the old code.')
    B(C, S_, 2, 'ask', 'Repository stub giúp gì khi thêm tính năng mới?', 'How does a stub repository help when adding a feature?')
    B(C, S_, 2, 'ans', 'ViewModel và giao diện chạy được ngay, trong khi tầng data làm song song.', 'The ViewModel and UI run right away while the data layer is built in parallel.')

    S_ = 'honest'
    a(C + '.sec.%s.title' % S_, 'Chương này giản lược những gì', 'What this chapter simplifies')
    a(C + '.sec.%s.badge' % S_, 'simplified')
    B(C, S_, 1, 'p', 'Quy trình theo Boudjnah (đọc từ epub trong kho). Việc nhánh viết lại bị bỏ dở là tình huống minh họa, không phải số liệu. Thứ tự domain trước là cách của tác giả; hướng dẫn của Google coi domain là tùy chọn. Chương chưa nói về di trú từ MVP (sách có), di trú sang Compose, và cờ tính năng chi tiết (track Thiết kế hệ thống, i12).',
      'The process follows Boudjnah (read from the epub in the library). The abandoned rewrite branch is an illustrative scenario, not data. Domain-first is the author\'s order; Google\'s guide treats the domain as optional. The chapter does not cover migrating from MVP (the book does), migrating to Compose, or feature flags in detail (System Design track, i12).')

    for q, qv, qe, av, ae, wv, we in [
        ('q1', 'Di trú kiến trúc có bắt buộc viết lại cả app không?', 'Does migrating the architecture require rewriting the whole app?', 'Không; chia thành bước nhỏ, từng màn.', 'No; split it into small steps, screen by screen.', 'Theo Boudjnah.', 'Per Boudjnah.'),
        ('q2', 'Tìm test cần có cho một màn bằng hai câu hỏi nào?', 'Which two questions find the tests a screen needs?', 'Người dùng thấy gì, và làm được gì trên màn này.', 'What the user can see, and what they can do on it.', 'Viết chúng trước khi đổi mã.', 'Write them before changing the code.'),
        ('q3', 'Thứ tự Boudjnah đề xuất khi thêm tính năng?', 'Boudjnah\'s suggested order for a new feature?', 'Domain, rồi presentation và data, cuối cùng UI và data source.', 'Domain, then presentation and data, finally UI and data sources.', 'Repository stub cho phép làm song song.', 'A stub repository enables parallel work.'),
        ('q4', 'Vì sao nhánh viết lại dễ bị bỏ dở?', 'Why do rewrite branches tend to be abandoned?', 'Nhánh chính vẫn đổi, hai nhánh lệch nhau, nhánh mới không phát hành được.', 'Main keeps changing, the branches diverge, and the new one cannot ship.', 'Di trú dần giữ app luôn phát hành được.', 'Gradual migration keeps the app shippable.')]:
        a(C + '.quiz.%s.q' % q, qv, qe); a(C + '.quiz.%s.a' % q, av, ae); a(C + '.quiz.%s.why' % q, wv, we)
