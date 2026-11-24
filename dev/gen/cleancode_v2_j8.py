# Mã sạch · J8: simple design và SOLID (Phần 3: thiết kế)
# Nguồn: Martin, Clean Architecture ch.7–11 (tóm tắt SOLID: Feathers gợi tên; SRP là "chịu trách nhiệm với đúng một actor", không phải "làm một
# việc"; OCP mở để mở rộng, đóng để sửa; LSP định nghĩa của Barbara Liskov, ví dụ hình vuông/chữ nhật; ISP đừng phụ thuộc thứ không dùng; DIP chính
# sách không phụ thuộc chi tiết, phụ thuộc vào trừu tượng ổn định, bỏ qua nền tảng ổn định như String); Martin, Clean Code ch.12 (bốn luật simple
# design của Kent Beck), ch.6 (đối xứng giữa object và cấu trúc dữ liệu); Clean Craftsmanship ch.6 (simple design dựa vào phán đoán);
# Moskała, Effective Kotlin Item 36 (ưu tiên composition hơn kế thừa). Đọc 2026-11-24, diễn đạt lại.

SEC_ORDER = {'j8': ['hook', 'simple', 'srpocp', 'lspisp', 'dip', 'bugs', 'ex', 'honest']}


def add(a):
    def B(ch, sec, n, field, vi, en=None):
        a('%s.sec.%s.b.%02d.%s' % (ch, sec, n, field), vi, vi if en is None else en)

    a('preset.solid', 'Mã sạch · SOLID qua một yêu cầu thanh toán', 'Clean code · SOLID through a payment request')
    m = lambda k, vi, en=None: a('m.solid.' + k, vi, en)
    m('title', 'when theo chuỗi khắp nơi, hay thiết kế theo SOLID', 'String when everywhere, or a SOLID design')
    m('overview', 'Phần thanh toán của app Hẹn Khám có tiền mặt, thẻ và bảo hiểm. Yêu cầu mới: thêm ví MoMo. Đi qua bốn bước, mỗi bước một hay hai nguyên lý SOLID, và so hai thiết kế: một lớp AppointmentManager với when theo chuỗi ở mọi nơi, và một thiết kế tách theo SRP, OCP, LSP, ISP, DIP.',
      'ClinicBook\'s payments support cash, card and insurance. A new request: add the MoMo e-wallet. Walk four steps, each about one or two SOLID principles, comparing two designs: an AppointmentManager class with string-based when everywhere, and a design split along SRP, OCP, LSP, ISP and DIP.')
    m('wrapup', 'Bản when theo chuỗi: ba nhóm người sửa cùng một lớp, thêm MoMo phải sửa 5 file và một nhánh else âm thầm tính phí 0, lớp bảo hiểm kế thừa thẻ nhưng ném lỗi khi hoàn tiền, và nghiệp vụ phụ thuộc thẳng vào SDK của cổng thanh toán. Bản SOLID: mỗi lớp chỉ một nhóm người sửa, thêm MoMo là thêm 1 file, bảo hiểm không hứa hoàn tiền nên trình biên dịch chặn lời gọi sai, và mũi tên phụ thuộc đổi chiều: SDK phụ thuộc vào giao diện do nghiệp vụ định nghĩa.',
      'The string-when version: three groups of people edit one class, adding MoMo touches 5 files and a silent else branch charges a 0 fee, the insurance class inherits from card yet throws on refund, and the business logic depends directly on the payment SDK. The SOLID version: each class is edited by one group, adding MoMo adds 1 file, insurance does not promise refunds so the compiler blocks the wrong call, and the dependency arrow flips: the SDK depends on an interface the business logic defines.')
    m('simp.1', 'Ba nhóm người (lễ tân, kế toán, marketing), năm chỗ when và mức phí là minh họa. Mỗi bước gom một hay hai nguyên lý cho gọn; trong mã thật chúng đan vào nhau.', 'The three groups (front desk, accounting, marketing), the five when sites and the fees are illustrative. Each step groups one or two principles for brevity; in real code they intertwine.')
    m('simp.2', 'Định nghĩa SOLID theo Martin, Clean Architecture; ông nói các chương đó chỉ tóm tắt hệ quả kiến trúc, không thay cho tài liệu chi tiết. Với Kotlin, sealed và when không có else là lựa chọn thứ ba ở bước OCP, xem mục SRP và OCP.', 'The SOLID definitions follow Martin, Clean Architecture; he says those chapters only summarise the architectural implications and do not replace detailed treatments. In Kotlin, sealed types with a when that has no else are a third option at the OCP step; see the SRP and OCP section.')
    m('ctl.hint', 'Đổi thiết kế rồi đi lại; mỗi bước mở thêm một hàng của ma trận nguyên lý.', 'Switch the design and walk again; each step opens another row of the principle matrix.')
    m('ctl.case', 'Thiết kế', 'Design')
    for k, vi, en in [('switch', 'when theo chuỗi khắp nơi', 'string when everywhere'), ('solid', 'tách theo SOLID', 'split along SOLID')]:
        m('ctl.case.' + k, vi, en)
    m('diagramTitle', 'Nghiệp vụ, giao diện, cổng thanh toán, SDK', 'Business logic, interface, gateway, SDK')
    m('diagramDesc', 'Nghiệp vụ đặt lịch gọi thanh toán; mũi tên phụ thuộc đi thẳng tới SDK, hay qua một giao diện do nghiệp vụ sở hữu', 'Booking logic calls payments; the dependency arrow goes straight to the SDK, or through an interface the business logic owns')
    for k, vi, en in [('booking', 'BookingService (nghiệp vụ)', 'BookingService (policy)'), ('port', 'PaymentGateway (giao diện)', 'PaymentGateway (interface)'), ('adapter', 'VnPayGateway (chi tiết)', 'VnPayGateway (detail)'), ('sdk', 'SDK cổng thanh toán', 'Payment SDK')]:
        m('n.' + k, vi, en)
    m('met.files', 'File phải sửa để thêm MoMo', 'Files edited to add MoMo'); m('met.crash', 'Chỗ có thể crash khi hoàn tiền', 'Places that can crash on refund'); m('met.detail', 'Nghiệp vụ phụ thuộc chi tiết', 'Policy depending on a detail')
    a('cap.solid', 'Nghiệp vụ ở trái, SDK ở phải. Mũi tên là phụ thuộc mã nguồn: ai import ai. Nút đỏ là chỗ nghiệp vụ dính vào chi tiết hay dễ vỡ.', 'Business logic on the left, the SDK on the right. Arrows are source dependencies: who imports whom. A red node is where policy is tied to a detail or fragile.')
    S = [
        ('switch', 's1', 'SRP: ba nhóm người cùng sửa một lớp', 'SRP: three groups edit one class',
         'AppointmentManager giữ lịch (lễ tân muốn), phí (kế toán muốn) và nội dung thông báo (marketing muốn). Kế toán đổi cách làm tròn phí, sửa nhầm hàm dùng chung, và giờ trong thông báo lệch.', 'AppointmentManager holds scheduling (front desk), fees (accounting) and notification wording (marketing). Accounting changes fee rounding, edits a shared helper by mistake, and notification times go off.'),
        ('switch', 's2', 'OCP: thêm MoMo phải sửa 5 file', 'OCP: adding MoMo edits 5 files',
         'when (method) ở phí, thanh toán, biên lai, hoàn tiền, thống kê. Sửa bốn chỗ, quên chỗ thứ năm: nhánh else -> 0L tính phí MoMo bằng 0 mà không ai thấy.', 'when (method) in fees, paying, receipts, refunds, analytics. Four are updated, the fifth forgotten: the else -> 0L branch charges MoMo a 0 fee and nobody notices.'),
        ('switch', 's3', 'LSP, ISP: bảo hiểm kế thừa thẻ, ném lỗi khi hoàn', 'LSP, ISP: insurance inherits card, throws on refund',
         'InsurancePayment : CardPayment để dùng lại phần thanh toán, nhưng bảo hiểm không hoàn tiền nên refund() ném UnsupportedOperationException. Màn hủy lịch gọi refund() cho mọi cách thanh toán: crash.', 'InsurancePayment : CardPayment to reuse paying, but insurance cannot refund, so refund() throws UnsupportedOperationException. The cancel screen calls refund() for every method: crash.'),
        ('switch', 's4', 'DIP: nghiệp vụ phụ thuộc thẳng vào SDK', 'DIP: policy depends straight on the SDK',
         'BookingService nhận VnPaySdkClient. Muốn test phải có SDK; SDK đổi phiên bản thì nghiệp vụ biên dịch lại và có thể vỡ. Mũi tên đi từ chính sách xuống chi tiết.', 'BookingService takes a VnPaySdkClient. Testing needs the SDK; an SDK update recompiles and may break the business logic. The arrow runs from policy down to detail.'),
        ('solid', 's1', 'SRP: mỗi lớp một nhóm người', 'SRP: one group per class',
         'BookingScheduler cho lễ tân, FeePolicy cho kế toán, ReminderComposer cho marketing. Kế toán đổi cách làm tròn chỉ sửa FeePolicy; thông báo không bị ảnh hưởng.', 'BookingScheduler for the front desk, FeePolicy for accounting, ReminderComposer for marketing. Accounting changes rounding in FeePolicy only; notifications are untouched.'),
        ('solid', 's2', 'OCP: thêm MoMo là thêm 1 file', 'OCP: adding MoMo adds 1 file',
         'PaymentMethod là giao diện; tiền mặt, thẻ, bảo hiểm là các lớp. MoMo là lớp mới tự khai báo phí và cách thanh toán. Không file cũ nào phải sửa, ngoài danh sách đăng ký.', 'PaymentMethod is an interface; cash, card and insurance are classes. MoMo is a new class declaring its own fee and payment. No existing file changes apart from the registration list.'),
        ('solid', 's3', 'LSP, ISP: hoàn tiền là giao diện riêng', 'LSP, ISP: refunds are a separate interface',
         'Refundable tách khỏi PaymentMethod. Thẻ và MoMo cài nó; bảo hiểm thì không. Màn hủy lịch chỉ gọi refund() trên Refundable, nên lời gọi sai không biên dịch được.', 'Refundable is split from PaymentMethod. Card and MoMo implement it; insurance does not. The cancel screen calls refund() only on a Refundable, so the wrong call does not compile.'),
        ('solid', 's4', 'DIP: mũi tên đổi chiều', 'DIP: the arrow flips',
         'BookingService phụ thuộc PaymentGateway, giao diện do tầng nghiệp vụ sở hữu. VnPayGateway cài giao diện đó và là nơi duy nhất import SDK. Test dùng gateway giả; đổi cổng thanh toán chỉ đổi một lớp.', 'BookingService depends on PaymentGateway, an interface the business layer owns. VnPayGateway implements it and is the only place importing the SDK. Tests use a fake gateway; switching providers changes one class.'),
    ]
    for case, k, tv, te, xv, xe in S:
        sid = case + '.' + k
        m('s.%s.title' % sid, tv, te); m('s.%s.explain' % sid, xv, xe); m('ev.' + sid, tv, te)
    for k, vi, en in [
        ('try', 'Mỗi bước mở một hàng của ma trận. Đổi qua lại hai thiết kế ở cùng bước để so.', 'Each step opens one matrix row. Switch between the two designs at the same step to compare.'),
        ('switch.s2', 'Martin (Clean Architecture): nếu một mở rộng đơn giản của yêu cầu buộc phải sửa phần mềm hàng loạt, kiến trúc đó đã thất bại. [[src:book-carch]]', 'Martin (Clean Architecture): if simple extensions to the requirements force massive changes to the software, the architecture has failed. [[src:book-carch]]'),
        ('switch.s3', 'Martin dùng ví dụ kinh điển hình vuông kế thừa hình chữ nhật: kiểu con không thay được kiểu cha thì người gọi phải biết đang cầm loại nào. Moskała (Effective Kotlin) khuyên dùng composition khi chỉ cần dùng lại mã, vì kế thừa kéo theo cả những hành vi không hợp. [[src:book-carch]] [[src:book-effective-kotlin]]', 'Martin uses the classic square-inherits-rectangle example: when a subtype cannot stand in for its parent, callers must know which one they hold. Moskała (Effective Kotlin) advises composition when all you need is reuse, since inheritance drags along behaviours that do not fit. [[src:book-carch]] [[src:book-effective-kotlin]]'),
        ('switch.s4', 'Martin: mã cài đặt chính sách cấp cao không nên phụ thuộc mã cài đặt chi tiết cấp thấp; thứ cần tránh phụ thuộc là những thứ cụ thể hay thay đổi. [[src:book-carch]]', 'Martin: code implementing high-level policy should not depend on code implementing low-level details; what to avoid depending on is volatile concrete things. [[src:book-carch]]'),
        ('solid.s1', 'Martin: SRP không phải "mỗi module làm một việc" (đó là quy tắc cho hàm). SRP là: một module chịu trách nhiệm với đúng một actor, tức một nhóm người cần thay đổi nó. [[src:book-carch]]', 'Martin: SRP is not "every module does one thing" (that rule is for functions). SRP is: a module should be responsible to one, and only one, actor, a group of people who need it changed. [[src:book-carch]]'),
        ('solid.s2', 'Martin: hành vi của một thành phần nên mở rộng được mà không phải sửa chính nó. Ý này do Bertrand Meyer phổ biến từ thập niên 1980. [[src:book-carch]]', 'Martin: a component\'s behaviour should be extendible without modifying it. Bertrand Meyer made the idea famous in the 1980s. [[src:book-carch]]'),
        ('solid.s3', 'Martin: đừng phụ thuộc vào những thứ mình không dùng. Màn hủy lịch chỉ cần khả năng hoàn tiền, nên nó phụ thuộc Refundable, không phụ thuộc cả PaymentMethod. [[src:book-carch]]', 'Martin: avoid depending on things you do not use. The cancel screen only needs refunding, so it depends on Refundable, not the whole PaymentMethod. [[src:book-carch]]'),
        ('solid.s4', 'Martin: giao diện ít biến động hơn cài đặt; kiến trúc ổn định tránh phụ thuộc vào thứ cụ thể hay đổi và dựa vào giao diện trừu tượng ổn định. Nền tảng ổn định như String thì không cần tránh. [[src:book-carch]]', 'Martin: interfaces are less volatile than implementations; stable architectures avoid depending on volatile concretions and rely on stable abstract interfaces. Stable platform facilities such as String need not be avoided. [[src:book-carch]]')]:
        m('co.' + k, vi, en)

    z = lambda k, vi, en=None: a('vz.' + k, vi, en)
    z('tab.solid', 'Ma trận SOLID', 'SOLID matrix')
    z('sd.cap', 'Mỗi hàng là một nguyên lý: phát biểu của Martin, triệu chứng khi vi phạm, và tình trạng ở thiết kế đang chọn. Hàng mở dần theo bước.', 'Each row is a principle: Martin\'s statement, the symptom of violating it, and its state in the chosen design. Rows open step by step.')
    for k, vi, en in [('p', 'Nguyên lý', 'Principle'), ('says', 'Phát biểu', 'Statement'), ('sym', 'Triệu chứng khi vi phạm', 'Symptom when violated'), ('here', 'Ở thiết kế này', 'In this design')]:
        z('sd.col.' + k, vi, en)
    for p, sv, se, yv, ye in [
        ('srp', 'một module chịu trách nhiệm với đúng một actor', 'a module is responsible to one, and only one, actor', 'sửa cho nhóm này làm hỏng việc của nhóm kia', 'a change for one group breaks another group\'s feature'),
        ('ocp', 'mở để mở rộng, đóng để sửa', 'open for extension, closed for modification', 'thêm một loại mới phải sửa nhiều file cũ', 'adding a new kind edits many old files'),
        ('lsp', 'kiểu con thay được kiểu cha mà không đổi hành vi', 'a subtype can stand in for its parent without changing behaviour', 'người gọi phải kiểm loại, hoặc crash', 'callers must check the type, or crash'),
        ('isp', 'đừng phụ thuộc thứ mình không dùng', 'do not depend on things you do not use', 'buộc phải cài hàm mình không làm được', 'forced to implement functions you cannot support'),
        ('dip', 'chính sách không phụ thuộc chi tiết; cả hai dựa vào trừu tượng', 'policy does not depend on details; both rely on abstractions', 'đổi SDK làm vỡ nghiệp vụ; khó test', 'an SDK change breaks the business logic; hard to test')]:
        z('sd.says.' + p, sv, se); z('sd.sym.' + p, yv, ye)
    for k, vi, en in [
        ('switch.srp', 'vi phạm: 3 nhóm sửa AppointmentManager', 'violated: 3 groups edit AppointmentManager'),
        ('switch.ocp', 'vi phạm: 5 file sửa, else tính phí 0', 'violated: 5 files edited, else charges 0'),
        ('switch.lsp', 'vi phạm: Insurance.refund() ném lỗi', 'violated: Insurance.refund() throws'),
        ('switch.isp', 'vi phạm: bảo hiểm phải có refund()', 'violated: insurance must have refund()'),
        ('switch.dip', 'vi phạm: BookingService → VnPaySdkClient', 'violated: BookingService → VnPaySdkClient'),
        ('solid.srp', 'giữ: 3 lớp, mỗi lớp một nhóm', 'kept: 3 classes, one group each'),
        ('solid.ocp', 'giữ: thêm MoMo là 1 file mới', 'kept: MoMo is 1 new file'),
        ('solid.lsp', 'giữ: bảo hiểm không hứa hoàn tiền', 'kept: insurance promises no refund'),
        ('solid.isp', 'giữ: Refundable là giao diện riêng', 'kept: Refundable is its own interface'),
        ('solid.dip', 'giữ: BookingService → PaymentGateway ← VnPayGateway', 'kept: BookingService → PaymentGateway ← VnPayGateway')]:
        z('sd.here.' + k, vi, en)
    z('sd.gcap', 'Đồ thị phụ thuộc mã nguồn (ai import ai). Bước 4 làm mũi tên giữa nghiệp vụ và chi tiết đổi chiều.', 'Source dependency graph (who imports whom). Step 4 flips the arrow between policy and detail.')
    z('sd.aria', 'Đồ thị phụ thuộc: {d}', 'Dependency graph: {d}')
    z('sd.g.policy', 'nghiệp vụ', 'policy'); z('sd.g.detail', 'chi tiết', 'detail')
    z('sd.legend', 'Ô gạch đỏ: nguyên lý bị vi phạm. Ô đậm: nguyên lý được giữ. "?": chưa tới bước đó. Mũi tên đỏ: nghiệp vụ phụ thuộc thẳng vào chi tiết.', 'Red hatched: the principle is violated. Bold: the principle holds. "?": that step has not come yet. Red arrow: policy depending straight on a detail.')

    C = 'j8'
    a(C + '.title', 'Simple design và SOLID', 'Simple design and SOLID')
    a(C + '.essence', 'Bốn luật simple design của Kent Beck, theo thứ tự ưu tiên ghi trong Clean Code: chạy qua mọi test, không trùng lặp, diễn đạt rõ ý định, ít lớp và hàm nhất có thể.\nSOLID (Martin): SRP một module chịu trách nhiệm với một nhóm người; OCP thêm loại mới bằng mã mới chứ không sửa mã cũ; LSP kiểu con thay được kiểu cha; ISP không phụ thuộc thứ mình không dùng; DIP chính sách không phụ thuộc chi tiết.\nĐây là nguyên lý thiết kế, không phải luật: áp lúc thấy triệu chứng (sửa một chỗ hỏng chỗ khác, thêm một loại phải sửa nhiều nơi), không áp trước cho mọi lớp.',
      'Kent Beck\'s four rules of simple design, in the priority order Clean Code gives: passes all the tests, has no duplication, expresses intent, has as few classes and functions as possible.\nSOLID (Martin): SRP a module is responsible to one group of people; OCP add a new kind with new code instead of editing old code; LSP subtypes stand in for their parents; ISP do not depend on what you do not use; DIP policy does not depend on details.\nThese are design principles, not laws: apply them when you see the symptoms (one change breaks another, a new kind edits many places), not upfront to every class.')
    a(C + '.goal.g1', 'Đã thấy LSP và ISP', 'Saw LSP and ISP')
    a(C + '.goal.g2', 'Đã thấy mũi tên DIP đổi chiều', 'Saw the DIP arrow flip')
    a(C + '.sim.cleancode.solid', 'when theo chuỗi hay SOLID', 'string when or SOLID')

    S_ = 'hook'
    a(C + '.sec.%s.title' % S_, 'Đoán trước khi đọc', 'Predict before reading')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'predict', 'Thêm ví MoMo vào app, bạn tìm thấy when (method) ở năm file và sửa bốn. Mọi test xanh, app chạy. Tháng sau kế toán phát hiện mọi giao dịch MoMo có phí bằng 0. Thiết kế nào để thêm một cách thanh toán mà không thể quên chỗ nào?',
      'Adding MoMo to the app, you find when (method) in five files and update four. All tests pass, the app runs. A month later accounting finds every MoMo transaction has a 0 fee. What design lets you add a payment method without any place to forget?')
    B(C, S_, 1, 'ans', 'Có hai cách đúng. Một: mỗi cách thanh toán là một lớp tự mang phí và cách thanh toán của nó (OCP), nên thêm MoMo là thêm một lớp, không có when nào để quên. Hai, riêng ở Kotlin: sealed interface và when không có else, để trình biên dịch chỉ ra mọi chỗ còn thiếu. Nhánh else -> 0L là thứ đã che lỗi. Mô phỏng ngay dưới đi qua cả năm nguyên lý SOLID trên cùng phần thanh toán.',
      'Two right answers. One: each payment method is a class carrying its own fee and payment logic (OCP), so adding MoMo adds a class, with no when to forget. Two, Kotlin-specific: a sealed interface and a when without else, so the compiler points at every place still missing. The else -> 0L branch is what hid the bug. The simulation just below walks all five SOLID principles on the same payment code.')

    S_ = 'simple'
    a(C + '.sec.%s.title' % S_, 'Bốn luật simple design', 'The four rules of simple design')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'p', 'Clean Code thuật lại bốn luật simple design của Kent Beck: chạy qua mọi test; không trùng lặp; diễn đạt ý định của người viết; giảm tối đa số lớp và hàm; và ghi rằng đó là thứ tự ưu tiên. Ở Clean Craftsmanship, Martin gọi chúng là phủ bởi test, tối đa sự diễn đạt, tối thiểu trùng lặp, tối thiểu kích thước (đặt diễn đạt trước trùng lặp), và nói simple design không chính xác như TDD hay refactor: nó dựa vào phán đoán và kinh nghiệm. [[src:book-cleancode]] [[src:book-craft]]',
      'Clean Code recounts Kent Beck\'s four rules of simple design: runs all the tests; contains no duplication; expresses the intent of the programmer; minimises the number of classes and methods; and states they are given in order of importance. In Clean Craftsmanship Martin names them covered by tests, maximise expression, minimise duplication, minimise size (putting expression before duplication), and says simple design is less precise than TDD or refactoring: it relies on judgement and experience. [[src:book-cleancode]] [[src:book-craft]]')
    B(C, S_, 2, 'note', 'Martin kể Beck từng nói làm theo bốn luật này thật chăm thì mọi nguyên lý thiết kế khác sẽ tự được thỏa; ông nói mình không biết điều đó có đúng không, nhưng chắc rằng học các nguyên lý như SOLID giúp chia hệ thống tốt hơn. [[src:book-craft]]',
      'Martin recalls Beck saying that following these four rules diligently would satisfy all other design principles; he says he does not know whether that is true, but is sure that studying principles such as SOLID makes partitioning a system much easier. [[src:book-craft]]')
    B(C, S_, 2, 'kind', 'source')
    B(C, S_, 3, 'p', 'Luật cuối là cái hãm cho các nguyên lý còn lại: đừng tạo giao diện, lớp trừu tượng hay factory khi chưa có triệu chứng đòi chúng. Một app chỉ có tiền mặt không cần PaymentMethod; thêm cách thanh toán thứ hai, thứ ba mới là lúc tách.',
      'The last rule brakes the other principles: do not create interfaces, abstract classes or factories before a symptom asks for them. An app with cash only needs no PaymentMethod; the second and third payment methods are when to split.')

    S_ = 'srpocp'
    a(C + '.sec.%s.title' % S_, 'SRP và OCP', 'SRP and OCP')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'p', 'Martin (Clean Architecture) nói SRP là nguyên lý bị hiểu sai nhiều nhất vì cái tên: nó không phải "mỗi module làm một việc" (đó là quy tắc cho hàm, chương J1). Phát biểu cuối của ông: một module chịu trách nhiệm với đúng một actor, tức một nhóm người cần thay đổi nó. Triệu chứng vi phạm: thay đổi cho nhóm này vô tình làm hỏng việc của nhóm kia, hay hai nhóm sửa cùng một file rồi xung đột khi gộp. [[src:book-carch]]',
      'Martin (Clean Architecture) calls SRP the most misunderstood principle because of its name: it is not "every module does one thing" (that rule is for functions, chapter J1). His final statement: a module should be responsible to one, and only one, actor, a group of people who need it changed. Symptoms: a change for one group accidentally breaks another\'s, or two groups edit the same file and conflict on merge. [[src:book-carch]]')
    B(C, S_, 2, 'p', 'OCP: phần mềm nên mở để mở rộng nhưng đóng để sửa; theo Martin, nếu mở rộng đơn giản buộc phải sửa hàng loạt thì kiến trúc đã thất bại. Ở Kotlin có một lựa chọn thứ ba đáng biết: sealed interface với when không có else. Thêm loại mới vẫn phải sửa mọi when, nhưng trình biên dịch chỉ ra đủ chỗ. Clean Code gọi đây là đối xứng giữa object và cấu trúc dữ liệu: object dễ thêm loại mới, cấu trúc dữ liệu cùng hàm xử lý dễ thêm thao tác mới. Chọn theo cái hay đổi hơn. [[src:book-carch]] [[src:book-cleancode]]',
      'OCP: software should be open for extension but closed for modification; for Martin, if simple extensions force massive changes, the architecture has failed. Kotlin has a third option worth knowing: a sealed interface with a when that has no else. Adding a kind still edits every when, but the compiler finds them all. Clean Code calls this the data/object anti-symmetry: objects make new kinds easy, data structures with functions make new operations easy. Choose by what changes more often. [[src:book-carch]] [[src:book-cleancode]]')
    B(C, S_, 3, 'kt', 'sealed interface PaymentMethod { fun fee(amount: Long): Long }\nobject Cash : PaymentMethod { override fun fee(amount: Long) = 0L }\nclass Card(val token: String) : PaymentMethod { override fun fee(amount: Long) = amount * 2 / 100 }\nclass MoMo(val phone: PhoneNumber) : PaymentMethod { override fun fee(amount: Long) = amount / 100 }   // thêm: 1 file',
      'sealed interface PaymentMethod { fun fee(amount: Long): Long }\nobject Cash : PaymentMethod { override fun fee(amount: Long) = 0L }\nclass Card(val token: String) : PaymentMethod { override fun fee(amount: Long) = amount * 2 / 100 }\nclass MoMo(val phone: PhoneNumber) : PaymentMethod { override fun fee(amount: Long) = amount / 100 }   // added: 1 file')

    S_ = 'lspisp'
    a(C + '.sec.%s.title' % S_, 'LSP và ISP', 'LSP and ISP')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'p', 'LSP là định nghĩa kiểu con của Barbara Liskov (1988): kiểu S là kiểu con của T nếu thay một object T bằng một object S thì mọi chương trình viết theo T vẫn hành xử y như cũ. Ví dụ kinh điển của Martin là hình vuông kế thừa hình chữ nhật: đặt chiều rộng thì chiều cao cũng đổi, nên người gọi phải biết đang cầm loại nào. Ở app: bảo hiểm kế thừa thẻ nhưng refund() ném lỗi là cùng một bệnh. [[src:book-carch]]',
      'LSP is Barbara Liskov\'s 1988 definition of subtypes: S is a subtype of T if substituting an S object for a T object leaves every program written against T behaving the same. Martin\'s classic example is a square inheriting from a rectangle: setting the width also changes the height, so callers must know which one they hold. In the app, insurance inheriting from card with a refund() that throws is the same disease. [[src:book-carch]]')
    B(C, S_, 2, 'p', 'ISP: đừng phụ thuộc vào những thứ mình không dùng. Tách khả năng hoàn tiền thành giao diện Refundable chữa cả hai: bảo hiểm không phải giả vờ có refund(), và màn hủy lịch chỉ phụ thuộc đúng thứ nó cần. Moskała (Effective Kotlin) bổ sung: khi chỉ muốn dùng lại mã, ưu tiên composition hơn kế thừa, vì kế thừa mang theo cả hành vi không hợp. [[src:book-carch]] [[src:book-effective-kotlin]]',
      'ISP: do not depend on things you do not use. Splitting refunds into a Refundable interface cures both: insurance need not pretend to have refund(), and the cancel screen depends on exactly what it needs. Moskała (Effective Kotlin) adds: when you only want reuse, prefer composition over inheritance, since inheritance carries behaviours that do not fit. [[src:book-carch]] [[src:book-effective-kotlin]]')
    B(C, S_, 3, 'kt', 'interface Refundable { suspend fun refund(id: PaymentId) }\nclass Card(...) : PaymentMethod, Refundable { /* ... */ }\nclass Insurance(...) : PaymentMethod { /* không hứa hoàn tiền */ }\n\nsuspend fun cancel(p: Payment) {\n    (p.method as? Refundable)?.refund(p.id)        // bảo hiểm: không có gì để gọi, không crash\n}',
      'interface Refundable { suspend fun refund(id: PaymentId) }\nclass Card(...) : PaymentMethod, Refundable { /* ... */ }\nclass Insurance(...) : PaymentMethod { /* promises no refund */ }\n\nsuspend fun cancel(p: Payment) {\n    (p.method as? Refundable)?.refund(p.id)        // insurance: nothing to call, no crash\n}')

    S_ = 'dip'
    a(C + '.sec.%s.title' % S_, 'DIP: chính sách không phụ thuộc chi tiết', 'DIP: policy does not depend on details')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'p', 'DIP: hệ thống linh hoạt nhất là hệ thống mà phụ thuộc mã nguồn chỉ trỏ vào trừu tượng. Martin nói rõ coi đây là luật tuyệt đối thì không thực tế: String là lớp cụ thể và phụ thuộc vào nó là bình thường, vì nó ổn định. Thứ cần tránh là phụ thuộc vào những thứ cụ thể hay thay đổi, những module đang được phát triển. Giao diện ít biến động hơn cài đặt, nên kiến trúc ổn định dựa vào giao diện. [[src:book-carch]]',
      'DIP: the most flexible systems are those whose source dependencies refer only to abstractions. Martin says plainly that treating this as an absolute rule is unrealistic: String is concrete and depending on it is fine, because it is stable. What to avoid is depending on volatile concrete things, the modules under active development. Interfaces are less volatile than implementations, so stable architectures rely on interfaces. [[src:book-carch]]')
    B(C, S_, 2, 'p', 'Ở app Android: SDK của cổng thanh toán là chi tiết hay đổi (phiên bản mới, đổi nhà cung cấp). Tầng nghiệp vụ định nghĩa PaymentGateway theo nhu cầu của mình; lớp VnPayGateway ở tầng dữ liệu cài giao diện đó và là nơi duy nhất import SDK. Mũi tên mã nguồn giờ đi từ chi tiết vào chính sách, ngược với chiều gọi lúc chạy: đó là chữ "đảo" trong tên nguyên lý. Hướng phụ thuộc giữa các tầng của cả app được dạy ở track Kiến trúc (G2). [[src:book-carch]]',
      'In an Android app: the payment SDK is a volatile detail (new versions, switching providers). The business layer defines PaymentGateway for its own needs; VnPayGateway in the data layer implements it and is the only place importing the SDK. The source arrow now runs from detail into policy, against the runtime call direction: that is the "inversion" in the name. Dependency direction across the whole app\'s layers is taught in the Architecture track (G2). [[src:book-carch]]')

    S_ = 'bugs'
    a(C + '.sec.%s.title' % S_, 'Hai lỗi hay gặp', 'Two common bugs')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'bug', 'Thêm ví MoMo, mọi giao dịch MoMo có phí bằng 0.', 'After adding MoMo, every MoMo transaction has a 0 fee.')
    B(C, S_, 1, 'cause', 'Cách thanh toán là chuỗi, xử lý bằng when ở năm file; một file bị quên và nhánh else -> 0L âm thầm nhận MoMo.', 'Payment methods are strings handled by when in five files; one file was forgotten and its else -> 0L branch silently took MoMo.')
    B(C, S_, 1, 'fix', 'Mỗi cách thanh toán là một lớp cài PaymentMethod và tự tính phí; hoặc sealed interface với when không có else để trình biên dịch bắt chỗ thiếu.', 'Each payment method becomes a class implementing PaymentMethod and computing its own fee; or a sealed interface with when and no else, so the compiler catches what is missing.')
    B(C, S_, 2, 'bug', 'Hủy lịch hẹn trả bằng bảo hiểm làm app crash.', 'Cancelling an insurance-paid booking crashes the app.')
    B(C, S_, 2, 'cause', 'InsurancePayment kế thừa CardPayment để dùng lại mã, rồi ghi đè refund() bằng throw UnsupportedOperationException(); màn hủy lịch tin mọi cách thanh toán đều hoàn được.', 'InsurancePayment inherits CardPayment for reuse, then overrides refund() with throw UnsupportedOperationException(); the cancel screen trusts every method to refund.')
    B(C, S_, 2, 'fix', 'Tách Refundable; bảo hiểm không cài nó; dùng composition để dùng lại phần thanh toán chung thay vì kế thừa.', 'Split out Refundable; insurance does not implement it; reuse common payment code through composition instead of inheritance.')

    S_ = 'ex'
    a(C + '.sec.%s.title' % S_, 'Bài tập', 'Exercise')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'ex', 'NotificationSender dưới đây gửi nhắc lịch. Chỉ ra nguyên lý SOLID nào bị vi phạm ở từng dòng đánh dấu, và viết lại.', 'The NotificationSender below sends reminders. Name the SOLID principle violated at each marked line, and rewrite it.')
    B(C, S_, 1, 'exkt', 'class NotificationSender(private val fcm: FirebaseMessaging) {   // (1)\n    fun send(r: Reminder, channel: String) = when (channel) {      // (2)\n        "push" -> fcm.send(r.toMessage())\n        "sms" -> SmsGatewayClient().send(r.phone, r.text)           // (3)\n        else -> Unit\n    }\n    fun reminderText(r: Reminder) = "Nhắc: ${r.time}"           // (4) marketing hay đổi câu chữ\n}')
    B(C, S_, 1, 'hint', 'Ai muốn đổi câu chữ, ai muốn thêm kênh Zalo? Lớp nghiệp vụ đang import những gì?', 'Who wants the wording changed, who wants a Zalo channel added? What does the business class import?')
    B(C, S_, 1, 'sol', '(1) và (3) vi phạm DIP: nghiệp vụ phụ thuộc thẳng FirebaseMessaging và SmsGatewayClient; định nghĩa giao diện NotificationChannel ở tầng nghiệp vụ, mỗi kênh một lớp cài nó ở tầng dữ liệu. (2) vi phạm OCP: thêm Zalo phải sửa when, và else -> Unit nuốt mất kênh lạ; danh sách kênh truyền vào, thêm kênh là thêm lớp. (4) vi phạm SRP: câu chữ thuộc về marketing, việc gửi thuộc về kỹ thuật; tách ReminderComposer.',
      '(1) and (3) violate DIP: the business class depends directly on FirebaseMessaging and SmsGatewayClient; define a NotificationChannel interface in the business layer, one implementing class per channel in the data layer. (2) violates OCP: adding Zalo edits the when, and else -> Unit swallows unknown channels; pass in a list of channels, and adding one adds a class. (4) violates SRP: wording belongs to marketing, sending belongs to engineering; split out ReminderComposer.')
    B(C, S_, 1, 'solkt', 'interface NotificationChannel { suspend fun send(r: Reminder, text: String) }\n\nclass ReminderComposer { fun text(r: Reminder) = "..." }      // marketing\n\nclass NotificationSender(\n    private val channels: List<NotificationChannel>,\n    private val composer: ReminderComposer,\n) {\n    suspend fun send(r: Reminder) = channels.forEach { it.send(r, composer.text(r)) }\n}\n// tầng dữ liệu: class FcmChannel(...) : NotificationChannel, class SmsChannel(...) : NotificationChannel')

    S_ = 'honest'
    a(C + '.sec.%s.title' % S_, 'Chương này giản lược những gì', 'What this chapter simplifies')
    a(C + '.sec.%s.badge' % S_, 'simplified')
    B(C, S_, 1, 'p', 'Định nghĩa SRP, OCP, LSP, ISP, DIP và các ví dụ hình vuông, String theo Robert C. Martin, Clean Architecture (chính tác giả nói các chương đó chỉ tóm tắt hệ quả kiến trúc); bốn luật simple design của Kent Beck theo Clean Code và Clean Craftsmanship; đối xứng object và cấu trúc dữ liệu theo Clean Code; composition hơn kế thừa theo Effective Kotlin. Đọc ngày 2026-11-24, diễn đạt lại; ví dụ viết bằng Kotlin trên app Hẹn Khám. SOLID là nguyên lý thiết kế của một tác giả, được dùng rộng nhưng cũng có người phê bình; chương trình bày nó như công cụ chữa triệu chứng, không như luật. Ba nhóm người, năm chỗ when, mức phí là minh họa.',
      'The SRP, OCP, LSP, ISP and DIP definitions and the square and String examples follow Robert C. Martin, Clean Architecture (the author says those chapters only summarise architectural implications); Kent Beck\'s four rules of simple design follow Clean Code and Clean Craftsmanship; the object and data structure anti-symmetry follows Clean Code; composition over inheritance follows Effective Kotlin. Read on 2026-11-24 and paraphrased; examples written in Kotlin on the ClinicBook app. SOLID is one author\'s set of design principles, widely used and also criticised; the chapter presents it as tools for treating symptoms, not as laws. The three groups, five when sites and fees are illustrative.')

    for q, qv, qe, av, ae, wv, we in [
        ('q1', 'Theo Martin, SRP có nghĩa là "mỗi lớp làm một việc" không?', 'According to Martin, does SRP mean "every class does one thing"?', 'Không; nghĩa là một module chịu trách nhiệm với đúng một nhóm người cần thay đổi nó.', 'No; it means a module is responsible to one group of people who need it changed.', '"Làm một việc" là quy tắc cho hàm.', '"Do one thing" is a rule for functions.'),
        ('q2', 'Vì sao nhánh else -> 0L nguy hiểm khi thêm cách thanh toán mới?', 'Why is an else -> 0L branch dangerous when adding a payment method?', 'Nó âm thầm nhận loại mới với hành vi sai, không ai được báo.', 'It silently takes the new kind with the wrong behaviour, and nobody is told.', 'Đa hình (OCP) hay sealed và when không else để trình biên dịch bắt.', 'Polymorphism (OCP), or sealed with a when that has no else, so the compiler catches it.'),
        ('q3', 'Lớp con ghi đè một hàm của lớp cha bằng throw UnsupportedOperationException vi phạm nguyên lý nào?', 'A subclass overriding a parent function with throw UnsupportedOperationException violates which principle?', 'LSP (và thường cả ISP).', 'LSP (and usually ISP too).', 'Kiểu con không còn thay được kiểu cha; tách giao diện cho khả năng đó.', 'The subtype no longer stands in for the parent; split that capability into its own interface.'),
        ('q4', 'Theo DIP, có cần tránh phụ thuộc vào String không?', 'Under DIP, should you avoid depending on String?', 'Không; String ổn định. Tránh phụ thuộc thứ cụ thể hay thay đổi.', 'No; String is stable. Avoid depending on volatile concrete things.', 'Martin nói coi DIP là luật tuyệt đối thì không thực tế.', 'Martin says treating DIP as an absolute rule is unrealistic.')]:
        a(C + '.quiz.%s.q' % q, qv, qe); a(C + '.quiz.%s.a' % q, av, ae); a(C + '.quiz.%s.why' % q, wv, we)
