# Kiến trúc · G5: domain layer (tùy chọn) và use case (Phần 1)
# Nguồn: developer.android.com Domain layer, Guide to app architecture (đọc 2026-11-24). Boudjnah ch2 (domain trong Clean Architecture) đã dẫn ở G2.
# Trần: 8 mục, mục cơ chế ≤ 4 khối.

SEC_ORDER = {'g5': ['hook', 'when', 'shape', 'restrict', 'bugs', 'ex', 'recall', 'honest']}


def add(a):
    def B(ch, sec, n, field, vi, en=None):
        a('%s.sec.%s.b.%02d.%s' % (ch, sec, n, field), vi, vi if en is None else en)

    m = lambda k, vi, en=None: a('m.usecase.' + k, vi, en)
    m('title', 'Quy tắc "giờ đặt được" sống ở đâu', 'Where the "bookable slot" rule lives')
    m('overview', 'Quy tắc: một giờ đặt được nếu chưa qua, nằm trong giờ mở cửa (7:00 tới 17:59) và cách hiện tại ít nhất một khoảng tối thiểu. Lúc 8:00, người dùng xem giờ 9:30. Ba cách: (1) quy tắc chép ở màn Chọn giờ và màn Đổi lịch; (2) hai màn dùng chung một use case; (3) một use case chỉ chuyển tiếp lời gọi repository.',
      'The rule: a slot is bookable if it has not passed, is within opening hours (7:00 to 17:59) and is at least a minimum lead time away. At 8:00 the user looks at the 9:30 slot. Three approaches: (1) the rule copied into Choose a time and Reschedule; (2) both screens sharing one use case; (3) a use case that only forwards a repository call.')
    m('wrapup', 'Logic nghiệp vụ dùng lại ở nhiều ViewModel nên sống ở một chỗ: một use case nhỏ, một việc, không giữ dữ liệu thay đổi. Đổi quy tắc thì đổi một nơi, test một lần. Nhưng domain là tùy chọn: use case không thêm quy tắc nào chỉ là một lớp và một chỗ nối DI thừa. Thêm use case khi nó giải quyết trùng lặp hay độ phức tạp.',
      'Business logic reused by several ViewModels should live in one place: a small use case, one job, no mutable data. Change the rule in one place, test it once. But the domain layer is optional: a use case that adds no rule is just an extra class and an extra DI binding. Add a use case when it removes duplication or complexity.')
    m('simp.1', 'Quy tắc được rút gọn còn ba điều kiện; giờ mở cửa cố định, không theo bác sĩ hay ngày lễ.', 'The rule is cut down to three conditions; opening hours are fixed, not per doctor or holiday.')
    m('ctl.hint', 'Đổi cách viết rồi đi lại bốn bước; xem tab "Quy tắc và nơi viết".', 'Switch the approach and walk the four steps again; watch the "Rule and where it lives" tab.')
    m('ctl.case', 'Cách viết quy tắc', 'Where the rule is written')
    for k, vi, en in [('duplicated', 'chép ở hai ViewModel', 'copied into two ViewModels'), ('shared', 'dùng chung một use case', 'one shared use case'), ('passthrough', 'use case chỉ chuyển tiếp', 'a pass-through use case')]:
        m('ctl.case.' + k, vi, en)
    m('diagramTitle', 'Hai ViewModel, use case, repository', 'Two ViewModels, a use case, the repository')
    m('diagramDesc', 'Hai ViewModel gọi repository trực tiếp hay qua use case', 'Two ViewModels call the repository directly or through a use case')
    for k, vi, en in [('choose', 'ChooseTimeViewModel', 'ChooseTimeViewModel'), ('resched', 'RescheduleViewModel', 'RescheduleViewModel'), ('uc', 'Use case', 'Use case'), ('repo', 'SlotRepository', 'SlotRepository')]:
        m('n.' + k, vi, en)
    m('met.copies', 'Số chỗ viết quy tắc', 'Places the rule is written'); m('met.agree', 'Hai màn cùng đáp án', 'Both screens agree'); m('met.extra', 'Lớp chỉ chuyển tiếp', 'Pass-through classes')
    for k, vi, en in [('na', 'chưa xét', 'not yet'), ('yes', 'có', 'yes'), ('no', 'không', 'no')]:
        m('agree.' + k, vi, en)
    a('cap.usecase', 'Bên trái hai ViewModel, giữa là use case, bên phải là repository. ViewModel gọi repository trực tiếp hay qua use case. Khối viền đỏ đang giữ một bản quy tắc cũ, hay là một lớp không thêm gì.',
      'Two ViewModels on the left, the use case in the middle, the repository on the right. ViewModels call the repository directly or through the use case. A red-outlined box holds an outdated copy of the rule, or is a class that adds nothing.')
    S = [
        ('duplicated', 's1', 'Màn Chọn giờ tự viết quy tắc', 'Choose a time writes the rule itself',
         'ChooseTimeViewModel có hàm bookable(): chưa qua, trong giờ mở cửa, cách hiện tại ít nhất 1 giờ. Lúc 8:00, giờ 9:30 đặt được.',
         'ChooseTimeViewModel has a bookable() function: not passed, within opening hours, at least 1 hour away. At 8:00, the 9:30 slot is bookable.'),
        ('duplicated', 's2', 'Màn Đổi lịch chép lại quy tắc', 'Reschedule copies the rule',
         'Màn Đổi lịch cũng cần biết giờ nào đặt được, nên ai đó chép nguyên hàm bookable() sang RescheduleViewModel. Hai bản giống nhau, hai màn cùng đáp án.',
         'Reschedule also needs to know which slots are bookable, so someone copies bookable() into RescheduleViewModel. Two identical copies, both screens agree.'),
        ('duplicated', 's3', 'Quy tắc đổi: đặt trước ít nhất 2 giờ', 'The rule changes: book at least 2 hours ahead',
         'Phòng khám đổi chính sách. Người sửa tìm thấy bản ở ChooseTimeViewModel và đổi thành 120 phút; bản ở RescheduleViewModel vẫn là 60.',
         'The clinic changes its policy. Whoever makes the change finds the copy in ChooseTimeViewModel and sets 120 minutes; the copy in RescheduleViewModel still says 60.'),
        ('duplicated', 's4', 'Hai màn trả lời khác nhau', 'The two screens disagree',
         'Lúc 8:00, màn Chọn giờ nói 9:30 không đặt được; màn Đổi lịch vẫn cho đổi sang 9:30. Máy chủ từ chối, người dùng thấy lỗi khó hiểu.',
         'At 8:00, Choose a time says 9:30 is not bookable; Reschedule still lets the user move to 9:30. The server refuses, and the user sees a confusing error.'),
        ('shared', 's1', 'Rút quy tắc thành IsSlotBookableUseCase', 'Extract the rule into IsSlotBookableUseCase',
         'Quy tắc nằm trong một lớp có một việc, nhận Clock qua constructor và không giữ dữ liệu thay đổi. ChooseTimeViewModel nhận use case này.',
         'The rule lives in a single-purpose class that takes a Clock through its constructor and holds no mutable data. ChooseTimeViewModel receives this use case.'),
        ('shared', 's2', 'Màn Đổi lịch dùng cùng use case', 'Reschedule uses the same use case',
         'RescheduleViewModel nhận cùng IsSlotBookableUseCase thay vì chép hàm. Một bản quy tắc, hai người dùng.',
         'RescheduleViewModel receives the same IsSlotBookableUseCase instead of copying the function. One copy of the rule, two users.'),
        ('shared', 's3', 'Quy tắc đổi: sửa một chỗ', 'The rule changes: edit one place',
         'Đổi 60 thành 120 phút trong use case. Cả hai màn tự nhận quy tắc mới.',
         'Change 60 to 120 minutes in the use case. Both screens pick up the new rule automatically.'),
        ('shared', 's4', 'Hai màn cùng đáp án, test một lần', 'Both screens agree, tested once',
         'Lúc 8:00, cả hai màn nói 9:30 không đặt được. Test use case với đồng hồ cố định lúc 8:00, không cần dựng ViewModel nào.',
         'At 8:00 both screens say 9:30 is not bookable. The use case is tested with a clock fixed at 8:00, without building any ViewModel.'),
        ('passthrough', 's1', 'GetSlotsUseCase chỉ gọi repo.slots()', 'GetSlotsUseCase only calls repo.slots()',
         'Theo thói quen "mọi thứ qua domain", có thêm GetSlotsUseCase mà thân chỉ là repo.slots(day). Nó không thêm quy tắc, không gộp nguồn nào.',
         'Out of a habit of "everything through the domain", a GetSlotsUseCase appears whose body is just repo.slots(day). It adds no rule and combines no sources.'),
        ('passthrough', 's2', 'ViewModel đi vòng qua use case', 'The ViewModel detours through the use case',
         'ChooseTimeViewModel nhận GetSlotsUseCase thay vì repository. Thêm một lớp, một chỗ nối DI và một lớp phải đọc khi lần theo lỗi, mà hành vi y hệt.',
         'ChooseTimeViewModel takes GetSlotsUseCase instead of the repository. One more class, one more DI binding and one more file to read when tracing a bug, with identical behaviour.'),
        ('passthrough', 's3', 'Khi nào việc chặn truy cập tầng data đáng giá', 'When restricting data-layer access pays off',
         'Tài liệu nêu lý do để buộc mọi truy cập qua domain: ví dụ mỗi lần truy cập dữ liệu đều phải ghi analytics. Cái giá là phải viết use case cả khi chỉ chuyển tiếp lời gọi.',
         'The docs give a reason to force all access through the domain: for example, logging analytics on every data access. The cost is writing use cases even when they only forward a call.'),
        ('passthrough', 's4', 'Bỏ use case thừa', 'Drop the redundant use case',
         'Không có lý do đó ở đây, nên ViewModel nhận thẳng repository. Cây quyết định bên tab hình đi theo nhánh "không dùng lại, không phức tạp".',
         'No such reason applies here, so the ViewModel takes the repository directly. The decision tree in the visual tab follows the "not reused, not complex" branch.'),
    ]
    for case, k, tv, te, xv, xe in S:
        sid = case + '.' + k
        m('s.%s.title' % sid, tv, te); m('s.%s.explain' % sid, xv, xe); m('ev.' + sid, tv, te)
    for k, vi, en in [
        ('try', 'Đi bốn bước của từng cách viết; so ô "đáp án lúc 8:00" của hai màn.', 'Walk the four steps of each approach; compare the "answer at 8:00" cells of the two screens.'),
        ('duplicated.s2', 'Domain layer: gói logic nghiệp vụ lặp lại ở tầng UI vào một use case giúp đổi một chỗ là áp dụng mọi nơi. [[src:ax-domain-layer]]', 'Domain layer: wrapping business logic repeated in the UI layer in a use case means a change in one place applies everywhere. [[src:ax-domain-layer]]'),
        ('duplicated.s3', 'Lợi ích đầu tiên tài liệu kể cho domain layer là tránh trùng lặp mã. [[src:ax-domain-layer]]', 'The first benefit the docs list for a domain layer is avoiding code duplication. [[src:ax-domain-layer]]'),
        ('duplicated.s4', 'Đây đúng là lỗi dẫn dắt của chương: cùng một quy tắc viết ở hai ViewModel và lệch nhau.', 'This is the chapter\'s lead bug: the same rule written in two ViewModels, drifting apart.'),
        ('shared.s2', 'Mỗi use case chỉ chịu trách nhiệm một việc và không chứa dữ liệu thay đổi; dữ liệu thay đổi để ở tầng UI hay data. [[src:ax-domain-layer]]', 'Each use case is responsible for a single functionality and holds no mutable data; mutable data belongs in the UI or data layer. [[src:ax-domain-layer]]'),
        ('shared.s3', 'Đặt tên theo quy ước của tài liệu: động từ thì hiện tại + danh từ + UseCase, ví dụ FormatDateUseCase. [[src:ax-domain-layer]]', 'Naming follows the docs\' convention: present-tense verb + noun + UseCase, for example FormatDateUseCase. [[src:ax-domain-layer]]'),
        ('shared.s4', 'Use case phải gọi an toàn từ main thread; việc nặng thì tự chuyển sang dispatcher khác, hay tốt hơn là để ở tầng data nếu kết quả cần cache. [[src:ax-domain-layer]]', 'Use cases must be main-safe; heavy work moves to another dispatcher, or better, into the data layer if the result should be cached. [[src:ax-domain-layer]]'),
        ('passthrough.s2', 'Domain là tầng tùy chọn: chỉ dùng khi cần, để xử lý độ phức tạp hay để dùng lại. [[src:ax-domain-layer]]', 'The domain layer is optional: use it only when needed, to handle complexity or favour reuse. [[src:ax-domain-layer]]'),
        ('passthrough.s3', 'Tài liệu: chặn tầng UI truy cập thẳng tầng data giúp UI không đi vòng qua logic domain, nhưng buộc phải thêm use case cả khi chỉ là lời gọi đơn giản, thêm phức tạp mà ít lợi. [[src:ax-domain-layer]]', 'Docs: blocking the UI from the data layer stops it bypassing domain logic, but forces use cases even for simple calls, adding complexity for little benefit. [[src:ax-domain-layer]]'),
        ('passthrough.s4', 'Cách tài liệu gợi ý: thêm use case khi cần; nếu gần như mọi truy cập đã đi qua use case thì mới cân nhắc bắt buộc. [[src:ax-domain-layer]]', 'The docs\' suggestion: add use cases only when required; consider making them mandatory only if the UI already accesses data almost exclusively through them. [[src:ax-domain-layer]]')]:
        m('co.' + k, vi, en)
    a('preset.usecase', 'Kiến trúc · quy tắc chép ở hai ViewModel so với use case', 'Architecture · a rule copied into two ViewModels versus a use case')

    z = lambda k, vi, en=None: a('vz.' + k, vi, en)
    z('tab.uc', 'Quy tắc và nơi viết', 'Rule and where it lives')
    z('uc.cap', 'Mỗi cột là một nơi có thể viết quy tắc; mỗi hàng là một điều kiện, hàng cuối là đáp án lúc 8:00 cho giờ 9:30.', 'Each column is a place the rule may be written; each row is a condition, and the last row is the answer at 8:00 for the 9:30 slot.')
    z('uc.treeCap', 'Cây quyết định: có cần use case cho logic này không? Nhánh của tình huống đang xem được viền.', 'Decision tree: does this logic need a use case? The branch for the current case is outlined.')
    z('uc.legend', 'Ô đỏ: ngưỡng cũ còn sót, hai màn trả lời khác nhau, hay lớp chỉ chuyển tiếp. Ô mờ: nơi đó không có quy tắc.', 'Red cell: an outdated threshold, the two screens disagreeing, or a pass-through class. Faded cell: no rule there.')
    z('uc.colRule', 'Điều kiện', 'Condition')
    for k, vi, en in [('choose', 'ChooseTimeViewModel', 'ChooseTimeViewModel'), ('resched', 'RescheduleViewModel', 'RescheduleViewModel'), ('uc', 'Use case', 'Use case')]:
        z('uc.col.' + k, vi, en)
    for k, vi, en in [('past', 'chưa qua', 'not passed'), ('hours', 'trong giờ mở cửa', 'within opening hours'), ('lead', 'đặt trước tối thiểu', 'minimum lead time'), ('ans', 'đáp án: 8:00 đặt 9:30?', 'answer: book 9:30 at 8:00?')]:
        z('uc.row.' + k, vi, en)
    for k, vi, en in [('y', 'có kiểm', 'checked'), ('1h', '60 phút', '60 minutes'), ('2h', '120 phút', '120 minutes'), ('use', 'gọi use case', 'calls the use case'),
                      ('-', 'không có', 'none'), ('fwd', 'chỉ gọi repo.slots()', 'only calls repo.slots()'), ('yes', 'đặt được', 'bookable'), ('no', 'không đặt được', 'not bookable')]:
        z('uc.v.' + k, vi, en)
    z('uc.q.reuse', 'Logic này có được nhiều ViewModel (hay service, Application) dùng lại không?', 'Is this logic reused by several ViewModels (or a service, the Application)?')
    z('uc.q.complex', 'Logic có phức tạp, hay gộp dữ liệu từ nhiều repository không?', 'Is the logic complex, or does it combine data from several repositories?')
    z('uc.yes', 'Có', 'Yes'); z('uc.no', 'Không', 'No')
    z('uc.leaf.useCase', '→ Use case dùng chung', '→ A shared use case')
    z('uc.leaf.useCaseOrRepo', '→ Use case (hay repository riêng nếu database tự gộp được, ví dụ truy vấn quan hệ của Room)', '→ A use case (or a dedicated repository if the database can join it, such as a Room relation query)')
    z('uc.leaf.none', '→ Không cần use case: ViewModel gọi repository', '→ No use case: the ViewModel calls the repository')

    C = 'g5'
    a(C + '.title', 'Domain layer (tùy chọn) và use case', 'The domain layer (optional) and use cases')
    a(C + '.essence', 'Domain layer là tầng tùy chọn giữa UI và data. Nó gói logic nghiệp vụ phức tạp, hay logic đơn giản mà nhiều ViewModel cùng dùng, vào các use case.\nMỗi use case làm một việc, không giữ dữ liệu thay đổi, gọi an toàn từ main thread, và được đặt tên theo hành động: IsSlotBookableUseCase.\nThêm use case khi nó xóa được trùng lặp hay độ phức tạp; use case chỉ chuyển tiếp lời gọi repository là một lớp thừa.',
      'The domain layer is an optional layer between UI and data. It wraps complex business logic, or simple logic reused by several ViewModels, in use cases.\nEach use case does one job, holds no mutable data, is safe to call from the main thread, and is named after its action: IsSlotBookableUseCase.\nAdd a use case when it removes duplication or complexity; a use case that only forwards a repository call is a redundant class.')
    a(C + '.goal.g1', 'Đã thấy hai màn trả lời khác nhau', 'Saw the two screens disagree')
    a(C + '.goal.g2', 'Đã đi hết bốn bước', 'Walked all four steps')
    a(C + '.sim.arch.usecase', 'quy tắc "giờ đặt được" sống ở đâu', 'where the "bookable slot" rule lives')

    S_ = 'hook'
    a(C + '.sec.%s.title' % S_, 'Đoán trước khi đọc', 'Predict before reading')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'predict', 'Quy tắc "đặt trước ít nhất 1 giờ" được chép ở màn Chọn giờ và màn Đổi lịch. Phòng khám đổi thành 2 giờ; người sửa chỉ tìm thấy bản ở màn Chọn giờ. Lúc 8:00, hai màn trả lời gì cho giờ 9:30?',
      'The rule "book at least 1 hour ahead" is copied into Choose a time and Reschedule. The clinic changes it to 2 hours; whoever makes the change only finds the copy in Choose a time. At 8:00, what do the two screens say about 9:30?')
    B(C, S_, 1, 'ans', 'Chọn giờ nói không đặt được, Đổi lịch nói đặt được. Mô phỏng bên dưới so cách chép quy tắc với một use case dùng chung, và với một use case không thêm gì. [[src:ax-domain-layer]]',
      'Choose a time says not bookable, Reschedule says bookable. The simulation below compares the copied rule with one shared use case, and with a use case that adds nothing. [[src:ax-domain-layer]]')

    S_ = 'when'
    a(C + '.sec.%s.title' % S_, 'Khi nào cần domain layer', 'When you need a domain layer')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'p', 'Theo hướng dẫn chính thức, domain layer gói logic nghiệp vụ phức tạp, hay logic đơn giản được nhiều ViewModel dùng lại. Nó tùy chọn vì không phải app nào cũng có nhu cầu đó: chỉ dùng khi cần xử lý độ phức tạp hay để dùng lại. Lợi ích được kể: tránh trùng lặp, lớp dùng nó dễ đọc hơn, dễ test hơn, và tách bớt các lớp lớn. [[src:ax-domain-layer]]',
      'Per the official guide, the domain layer wraps complex business logic, or simple logic reused by several ViewModels. It is optional because not every app needs that: use it only to handle complexity or favour reuse. The listed benefits: no duplication, more readable callers, better testability, and smaller classes. [[src:ax-domain-layer]]')
    B(C, S_, 2, 'p', 'Hai trường hợp điển hình trong tài liệu. Logic đơn giản lặp lại ở tầng UI (định dạng ngày, kiểm giờ đặt được): gói vào use case để đổi một chỗ là áp dụng mọi nơi. Logic gộp nhiều repository (tin tức kèm tác giả): use case kéo logic đó ra khỏi ViewModel. Nhưng nếu database là nguồn sự thật và tự gộp được bằng truy vấn quan hệ của Room, thì một repository riêng hợp hơn use case. [[src:ax-domain-layer]]',
      'Two typical cases in the docs. Simple logic repeated in the UI layer (date formatting, checking bookable slots): wrap it in a use case so a change in one place applies everywhere. Logic combining several repositories (news with authors): a use case pulls it out of the ViewModel. But if the database is the source of truth and can join the data with a Room relation query, a dedicated repository fits better than a use case. [[src:ax-domain-layer]]')
    B(C, S_, 3, 'note', 'Chữ "domain layer" trong hướng dẫn Android khác nghĩa với domain trong Clean Architecture: tài liệu nhắc đừng nhầm hai định nghĩa. Ở Android, domain nằm giữa và phụ thuộc vào data (chương G2); ở sách Clean Architecture, domain ở trung tâm và data phụ thuộc vào nó. [[src:ax-domain-layer]] [[src:book-boudjnah]]',
      'The term "domain layer" in the Android guide means something different from the domain in Clean Architecture: the docs warn not to confuse the two. In Android, the domain sits in the middle and depends on data (chapter G2); in the Clean Architecture books, the domain is at the centre and data depends on it. [[src:ax-domain-layer]] [[src:book-boudjnah]]')

    S_ = 'shape'
    a(C + '.sec.%s.title' % S_, 'Một use case trông thế nào', 'What a use case looks like')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'p', 'Mỗi use case chịu trách nhiệm một việc, không chứa dữ liệu thay đổi; tên theo quy ước động từ thì hiện tại + danh từ + UseCase. Trong Kotlin có thể khai báo operator fun invoke để gọi use case như một hàm. Use case không có vòng đời riêng: nó theo lớp đang dùng nó, nên có thể tạo mới mỗi khi truyền làm phụ thuộc. [[src:ax-domain-layer]]',
      'Each use case is responsible for one functionality and holds no mutable data; it is named present-tense verb + noun + UseCase. In Kotlin you can declare operator fun invoke to call the use case like a function. A use case has no lifecycle of its own: it follows the class using it, so a new instance can be created whenever it is passed as a dependency. [[src:ax-domain-layer]]')
    B(C, S_, 2, 'kt', 'class IsSlotBookableUseCase(private val clock: Clock) {\n    operator fun invoke(slot: Slot): Boolean {\n        val now = LocalDateTime.now(clock)\n        return slot.start > now && slot.start.hour in 7..17 &&\n            ChronoUnit.MINUTES.between(now, slot.start) >= 120\n    }\n}\n// gọi như một hàm\nval ok = isSlotBookable(slot)',
      'class IsSlotBookableUseCase(private val clock: Clock) {\n    operator fun invoke(slot: Slot): Boolean {\n        val now = LocalDateTime.now(clock)\n        return slot.start > now && slot.start.hour in 7..17 &&\n            ChronoUnit.MINUTES.between(now, slot.start) >= 120\n    }\n}\n// called like a function\nval ok = isSlotBookable(slot)')
    B(C, S_, 3, 'p', 'Use case phải main-safe: gọi từ main thread không làm treo UI. Nếu có việc nặng, use case tự chuyển sang dispatcher phù hợp; nhưng trước đó nên xem việc ấy có nên nằm ở tầng data không, nhất là khi kết quả cần cache cho nhiều màn. Nhận Clock qua constructor như trên giúp test với giờ cố định thay vì giờ thật. [[src:ax-domain-layer]]',
      'Use cases must be main-safe: calling them from the main thread must not freeze the UI. Heavy work moves to a suitable dispatcher inside the use case; but first check whether that work belongs in the data layer, especially when the result should be cached for several screens. Taking a Clock through the constructor, as above, lets tests use a fixed time instead of the real one. [[src:ax-domain-layer]]')

    S_ = 'restrict'
    a(C + '.sec.%s.title' % S_, 'Có nên buộc mọi truy cập đi qua domain?', 'Should all access go through the domain?')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'p', 'Tài liệu cân hai phía. Chặn tầng UI gọi thẳng tầng data giúp UI không đi vòng qua logic domain, ví dụ khi mỗi lần truy cập dữ liệu phải ghi analytics. Cái giá có thể lớn: phải thêm use case cả khi chỉ là một lời gọi đơn giản, thêm phức tạp mà ít lợi. Gợi ý: thêm use case khi cần; nếu UI đã gần như chỉ truy cập dữ liệu qua use case thì mới cân nhắc bắt buộc. [[src:ax-domain-layer]]',
      'The docs weigh both sides. Blocking the UI from calling the data layer directly stops it bypassing domain logic, for example when every data access must log analytics. The cost can be significant: use cases must be added even for simple calls, adding complexity for little benefit. Suggestion: add use cases when required; consider making them mandatory only if the UI already accesses data almost exclusively through them. [[src:ax-domain-layer]]')
    B(C, S_, 2, 'note', 'Tài liệu cũng khuyên đặt logic dùng lại vào use case thay vì hàm tĩnh trong lớp Util, vì lớp Util khó tìm và khó biết nó làm gì. [[src:ax-domain-layer]]', 'The docs also advise putting reusable logic in a use case rather than static methods in a Util class, because Util classes are hard to find and their functionality hard to discover. [[src:ax-domain-layer]]')

    S_ = 'bugs'
    a(C + '.sec.%s.title' % S_, 'Hai lỗi hay gặp', 'Two common bugs')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'bug', 'Màn Đổi lịch cho chọn 9:30 nhưng máy chủ từ chối; màn Chọn giờ thì đã khóa 9:30 từ trước.', 'Reschedule lets the user pick 9:30 but the server refuses; Choose a time had already greyed 9:30 out.')
    B(C, S_, 1, 'cause', 'Quy tắc đặt trước được chép ở hai ViewModel, và lần đổi chính sách chỉ sửa một bản.', 'The lead-time rule is copied into two ViewModels, and the policy change only updated one copy.')
    B(C, S_, 1, 'fix', 'Rút quy tắc vào IsSlotBookableUseCase và cho cả hai ViewModel dùng nó.', 'Extract the rule into IsSlotBookableUseCase and have both ViewModels use it.')
    B(C, S_, 2, 'bug', 'Test quy tắc giờ đặt được lúc qua lúc trượt, tùy giờ chạy test.', 'The bookable-slot test passes or fails depending on what time it runs.')
    B(C, S_, 2, 'cause', 'Use case gọi LocalDateTime.now() bên trong, nên kết quả phụ thuộc giờ thật.', 'The use case calls LocalDateTime.now() internally, so its result depends on the real time.')
    B(C, S_, 2, 'fix', 'Nhận Clock qua constructor; app dùng Clock.systemDefaultZone(), test dùng Clock.fixed(...).', 'Take a Clock through the constructor; the app passes Clock.systemDefaultZone(), tests pass Clock.fixed(...).')

    S_ = 'ex'
    a(C + '.sec.%s.title' % S_, 'Bài tập', 'Exercise')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'ex', 'Với mỗi đoạn logic sau, quyết định: use case, repository riêng, hay để trong ViewModel. (a) Định dạng "Thứ Hai, 9:30" dùng ở 4 màn. (b) Lấy danh sách lịch hẹn, chỉ một màn dùng. (c) Lịch hẹn kèm thông tin bác sĩ, cả hai cùng ở Room. (d) Tính phí khám theo bảo hiểm, dùng ở màn Đặt lịch và màn Hóa đơn. (Bài tập của site, theo các trường hợp trong trang Domain layer.) [[src:ax-domain-layer]]',
      'For each piece of logic, decide: a use case, a dedicated repository, or keep it in the ViewModel. (a) Formatting "Monday, 9:30", used on 4 screens. (b) Getting the appointment list, used by one screen. (c) Appointments with doctor info, both stored in Room. (d) Computing the visit fee by insurance, used by Booking and Invoice. (The site\'s own exercise, after the cases on the Domain layer page.) [[src:ax-domain-layer]]')
    B(C, S_, 1, 'hint', 'Đi theo cây quyết định của hình: có dùng lại không, có phức tạp hay gộp nhiều nguồn không, database có tự gộp được không.', 'Follow the visual\'s decision tree: is it reused, is it complex or combining sources, can the database join it itself?')
    B(C, S_, 1, 'sol', '(a) Use case (FormatAppointmentDateUseCase): logic đơn giản nhưng dùng lại. (b) ViewModel gọi repository: không dùng lại, không phức tạp. (c) Repository riêng với truy vấn quan hệ của Room: database tự gộp được. (d) Use case (CalculateVisitFeeUseCase): quy tắc nghiệp vụ dùng ở hai nơi.',
      '(a) A use case (FormatAppointmentDateUseCase): simple logic, but reused. (b) The ViewModel calls the repository: not reused, not complex. (c) A dedicated repository with a Room relation query: the database can join it. (d) A use case (CalculateVisitFeeUseCase): a business rule used in two places.')

    S_ = 'recall'
    a(C + '.sec.%s.title' % S_, 'Tự trả lời', 'Answer it yourself')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'ask', 'Hai lý do để thêm một use case là gì?', 'What are the two reasons to add a use case?')
    B(C, S_, 1, 'ans', 'Logic được nhiều nơi dùng lại, hay logic phức tạp (ví dụ gộp nhiều repository).', 'The logic is reused in several places, or it is complex (for example combining several repositories).')
    B(C, S_, 2, 'ask', 'Vì sao use case nên nhận Clock qua constructor?', 'Why should a use case take a Clock through its constructor?')
    B(C, S_, 2, 'ans', 'Để test đặt được giờ cố định, kết quả không phụ thuộc lúc chạy test.', 'So tests can fix the time, and results do not depend on when the test runs.')

    S_ = 'honest'
    a(C + '.sec.%s.title' % S_, 'Chương này giản lược những gì', 'What this chapter simplifies')
    a(C + '.sec.%s.badge' % S_, 'simplified')
    B(C, S_, 1, 'p', 'Nguyên tắc theo trang Domain layer và Guide to app architecture đọc ngày 2026-11-24. Quy tắc giờ đặt được là ví dụ của site, rút còn ba điều kiện. Cây quyết định là cách site tóm tắt các trường hợp trong tài liệu, không phải sơ đồ có trong tài liệu. Chương chưa nói về use case gọi use case khác, dùng lại domain cho TV hay Wear, và cách test domain bằng repository giả (chương G10).',
      'The principles follow the Domain layer and Guide to app architecture pages as read on 2026-11-24. The bookable-slot rule is the site\'s own example, cut to three conditions. The decision tree is the site\'s summary of the cases in the docs, not a diagram from them. The chapter does not cover use cases calling other use cases, reusing the domain for TV or Wear, or testing the domain with fake repositories (chapter G10).')

    for q, qv, qe, av, ae, wv, we in [
        ('q1', 'Theo hướng dẫn chính thức, domain layer có bắt buộc không?', 'Per the official guide, is the domain layer mandatory?', 'Không; nó tùy chọn.', 'No; it is optional.', 'Chỉ dùng khi cần xử lý độ phức tạp hay để dùng lại.', 'Use it only to handle complexity or favour reuse.'),
        ('q2', 'Một use case nên chịu trách nhiệm bao nhiêu việc?', 'How many functionalities should a use case own?', 'Một việc.', 'One.', 'Và không chứa dữ liệu thay đổi.', 'And it holds no mutable data.'),
        ('q3', 'Use case có nên gọi an toàn từ main thread không?', 'Should a use case be safe to call from the main thread?', 'Có; nó phải main-safe.', 'Yes; it must be main-safe.', 'Việc nặng tự chuyển dispatcher, hay để ở tầng data.', 'Heavy work moves to another dispatcher, or into the data layer.'),
        ('q4', 'Hai bảng đều ở Room, cần gộp: use case hay repository?', 'Two tables both in Room need joining: use case or repository?', 'Repository riêng với truy vấn quan hệ.', 'A dedicated repository with a relation query.', 'Database tự gộp được thì không cần use case.', 'If the database can join it, no use case is needed.')]:
        a(C + '.quiz.%s.q' % q, qv, qe); a(C + '.quiz.%s.a' % q, av, ae); a(C + '.quiz.%s.why' % q, wv, we)
