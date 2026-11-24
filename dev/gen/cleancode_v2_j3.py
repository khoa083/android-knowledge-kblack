# Mã sạch · J3: đóng gói, bất biến, parse don't validate (Phần 1: mã đọc được)
# Nguồn: Seemann, Code That Fits in Your Head 5.2.3–5.2.4 (hợp đồng, luật Postel), 5.3, 5.3.1 (luôn hợp lệ; bất biến → kiểm một chỗ),
# 7.2.5 (parse, don't validate; trích ý Alexis King), A.15, A.16; Martin, Clean Code ch.6 (object và cấu trúc dữ liệu), ch.7 (đừng trả,
# đừng truyền null), ch.8 (ranh giới với mã bên thứ ba); Moskała, Effective Kotlin Item 1 (hạn chế mutable, lợi ích của object bất biến);
# Kotlin docs: inline value classes (init + require, khác typealias). Đọc 2026-11-24, diễn đạt lại.
# Hình: dòng chảy phẳng thô → ranh giới → bên trong → gửi SMS (không dùng hộp lồng như dàn ý cũ, theo quy tắc design-principles §5.2).

SEC_ORDER = {'j3': ['hook', 'encap', 'parse', 'postel', 'boundary', 'bugs', 'ex', 'honest']}


def add(a):
    def B(ch, sec, n, field, vi, en=None):
        a('%s.sec.%s.b.%02d.%s' % (ch, sec, n, field), vi, vi if en is None else en)

    a('preset.parse', 'Mã sạch · parse một lần ở ranh giới', 'Clean code · parse once at the boundary')
    m = lambda k, vi, en=None: a('m.parse.' + k, vi, en)
    m('title', 'Kiểm rải rác, hay parse một lần ở ranh giới', 'Scattered checks, or parse once at the boundary')
    m('overview', 'Ba màn hình của app Hẹn Khám nhận số điện thoại: form đặt lịch, hồ sơ, cài đặt nhắc lịch. Ba giá trị thô đi từ màn hình vào kho dữ liệu rồi tới lúc gửi SMS nhắc lịch, hai ngày sau. Cách thứ nhất: mỗi nơi tự kiểm một chuỗi String theo luật của mình. Cách thứ hai: parse một lần ở ranh giới thành kiểu PhoneNumber, bên trong chỉ nhận kiểu đó.',
      'Three ClinicBook screens take a phone number: the booking form, the profile, the reminder settings. Three raw values travel from the screens into storage and on to the SMS reminder, two days later. First approach: each place checks a String by its own rule. Second approach: parse once at the boundary into a PhoneNumber type, and the inside accepts only that type.')
    m('wrapup', 'Kiểm rải rác cho ra bốn luật khác nhau ở bốn chỗ, và giá trị đã qua kiểm vẫn là String: không ai bên trong biết nó đã được kiểm theo luật nào. Hai SMS hỏng hai ngày sau, khi người dùng không còn ở màn hình để sửa: một số thật sự thiếu chữ số đã lọt qua, và một số đúng nhưng viết dạng +84 bị luật thứ tư từ chối. Parse một lần: một luật, chuẩn hóa +84 thành 0, số thiếu chữ số bị từ chối ngay tại form. Từ ranh giới vào trong, kiểu PhoneNumber bảo đảm giá trị đúng, nên kho dữ liệu và SmsSender không cần kiểm lại.',
      'Scattered checks produce four different rules in four places, and a checked value is still a String: nobody inside knows which rule it passed. Two SMS fail two days later, when the user is no longer on the screen to fix them: one number really missing a digit slipped through, and one valid number written as +84 is rejected by the fourth rule. Parsing once: one rule, +84 normalised to 0, the number missing a digit rejected right at the form. From the boundary inwards the PhoneNumber type guarantees a valid value, so storage and SmsSender need not check again.')
    m('simp.1', 'Luật số di động Việt Nam ở đây (10 chữ số, bắt đầu 03, 05, 07, 08, 09) là quy tắc minh họa của site, không phải đặc tả của nhà mạng. Ba luật kiểm rải rác cố ý khác nhau để thấy chuyện gì xảy ra khi mỗi người viết một bản.', 'The Vietnamese mobile number rule here (10 digits starting 03, 05, 07, 08 or 09) is the site\'s illustrative rule, not a carrier specification. The three scattered rules are deliberately different to show what happens when everyone writes their own.')
    m('simp.2', 'Parse don\'t validate là cách gọi của Alexis King mà Seemann trích; value class với init và require theo tài liệu Kotlin. Trả về null khi parse thất bại là một lựa chọn; có thể trả về kiểu lỗi chi tiết hơn để form báo đúng lý do.', 'Parse, don\'t validate is Alexis King\'s phrase, quoted by Seemann; the value class with init and require follows the Kotlin docs. Returning null on failure is one choice; a richer error type lets the form say exactly why.')
    m('ctl.hint', 'Đổi cách làm rồi đi lại; nhìn cột cuối "Gửi SMS" và hàng số thiếu chữ số.', 'Switch the approach and walk again; watch the last column "Send SMS" and the row with the missing digit.')
    m('ctl.case', 'Cách làm', 'Approach')
    for k, vi, en in [('validate', 'mỗi nơi tự kiểm String', 'each place checks a String'), ('parse', 'parse một lần thành PhoneNumber', 'parse once into PhoneNumber')]:
        m('ctl.case.' + k, vi, en)
    m('diagramTitle', 'Màn hình, ranh giới, kho dữ liệu, gửi SMS', 'Screens, boundary, storage, SMS')
    m('diagramDesc', 'Giá trị thô đi từ màn hình qua ranh giới vào kho dữ liệu, hai ngày sau tới bộ gửi SMS', 'Raw values go from the screens through the boundary into storage, and two days later to the SMS sender')
    for k, vi, en in [('screen', 'Ba màn hình nhập', 'Three input screens'), ('boundary', 'Ranh giới', 'Boundary'), ('repo', 'Kho dữ liệu', 'Storage'), ('sms', 'Gửi SMS (2 ngày sau)', 'SMS (2 days later)')]:
        m('n.' + k, vi, en)
    m('met.checks', 'Chỗ kiểm số điện thoại', 'Places checking the number'); m('met.form', 'Bị từ chối ngay tại form', 'Rejected at the form'); m('met.late', 'SMS hỏng lúc gửi', 'SMS failing at send time')
    a('cap.parse', 'Giá trị đi từ trái sang phải: màn hình, ranh giới, kho dữ liệu, gửi SMS. Nút đỏ là nơi một số sai bị phát hiện quá muộn.', 'Values flow left to right: screens, boundary, storage, SMS. A red node is where a bad number is caught too late.')
    S = [
        ('validate', 's1', 'Ba màn hình nhận ba chuỗi thô', 'Three screens receive three raw strings',
         '"0912 345 678" ở form đặt lịch, "+84 912 345 678" ở hồ sơ, "091234567" (thiếu một chữ số) ở cài đặt nhắc lịch.', '"0912 345 678" on the booking form, "+84 912 345 678" on the profile, "091234567" (one digit short) on the reminder settings.'),
        ('validate', 's2', 'Mỗi màn hình kiểm theo luật của mình', 'Each screen checks by its own rule',
         'Form đặt lịch đếm 10 chữ số sau khi bỏ khoảng trắng; hồ sơ chỉ xem đầu số +84 hay 0; cài đặt nhắc chỉ cần dài ít nhất 9 ký tự. Cả ba đều qua, và được lưu nguyên chuỗi gốc.', 'The booking form counts 10 digits after removing spaces; the profile only checks for a +84 or 0 prefix; the reminder settings only need 9 characters. All three pass and are stored exactly as typed.'),
        ('validate', 's3', 'Bên trong: vẫn là String', 'Inside: still a String',
         'PatientRepo nhận String. Người đọc kho dữ liệu không biết chuỗi đã được kiểm chưa, theo luật nào, nên phải tin mù hoặc kiểm lại.', 'PatientRepo takes a String. A reader of the storage code cannot tell whether the string was checked or by which rule, so they must trust blindly or check again.'),
        ('validate', 's4', 'Hai ngày sau: hai SMS hỏng', 'Two days later: two SMS fail',
         'SmsSender kiểm lần thứ tư với luật thứ tư: số thiếu chữ số bị từ chối, và số đúng viết dạng +84 cũng bị từ chối vì luật này chỉ nhận đầu 0. Người dùng không nhận được nhắc lịch và không còn ở màn hình nào để sửa.', 'SmsSender checks a fourth time with a fourth rule: the short number is rejected, and so is the valid +84 number, because this rule only accepts a leading 0. The users get no reminder and are on no screen where they could fix it.'),
        ('parse', 's1', 'Ba màn hình nhận ba chuỗi thô', 'Three screens receive three raw strings',
         'Cùng ba giá trị. Lần này cả ba màn hình gọi cùng một hàm parsePhone.', 'The same three values. This time all three screens call the same parsePhone function.'),
        ('parse', 's2', 'Ranh giới: parse một lần', 'The boundary: parse once',
         'parsePhone bỏ ký tự không phải số, đổi 84 ở đầu thành 0, rồi kiểm một luật. Hai số đầu thành PhoneNumber("0912345678"); số thiếu chữ số trả về null, form báo lỗi ngay khi người dùng còn đang nhập.', 'parsePhone drops non-digits, turns a leading 84 into 0, then checks one rule. The first two become PhoneNumber("0912345678"); the short number returns null and the form shows the error while the user is still typing.'),
        ('parse', 's3', 'Bên trong: chỉ nhận PhoneNumber', 'Inside: only PhoneNumber',
         'PatientRepo nhận PhoneNumber, không nhận String. Kiểu nói thay cho mọi lần kiểm: đã có PhoneNumber thì nó đúng.', 'PatientRepo takes a PhoneNumber, not a String. The type replaces every check: if you hold a PhoneNumber, it is valid.'),
        ('parse', 's4', 'Hai ngày sau: hai SMS đi, không cần kiểm lại', 'Two days later: two SMS sent, no re-check',
         'SmsSender.send(phone: PhoneNumber, …) không có nhánh kiểm nào. Số sai đã dừng ở ranh giới từ hai ngày trước.', 'SmsSender.send(phone: PhoneNumber, …) has no checking branch. The bad number stopped at the boundary two days ago.'),
    ]
    for case, k, tv, te, xv, xe in S:
        sid = case + '.' + k
        m('s.%s.title' % sid, tv, te); m('s.%s.explain' % sid, xv, xe); m('ev.' + sid, tv, te)
    for k, vi, en in [
        ('try', 'Theo từng hàng từ trái sang phải; để ý giá trị ở mỗi cột là String hay PhoneNumber.', 'Follow each row left to right; notice whether each column holds a String or a PhoneNumber.'),
        ('validate.s2', 'Ba luật khác nhau không phải do ai ẩu: mỗi người viết một hàm kiểm vào ngày khác nhau, và không có kiểu nào buộc họ dùng chung.', 'Three different rules are nobody\'s carelessness: each person wrote a check on a different day, and no type forced them to share one.'),
        ('validate.s3', 'Seemann (5.3): phương thức kiểm điều kiện trước rồi gọi kho dữ liệu, nhưng hiểu biết đó mất ngay khi gọi. Người bảo trì mở kho dữ liệu sẽ phải làm thám tử để biết giá trị có hợp lệ không. [[src:book-seemann]]', 'Seemann (5.3): a method checks the preconditions and calls the repository, but that knowledge is lost the moment it calls. A maintainer opening the repository has to play detective to know whether the value is valid. [[src:book-seemann]]'),
        ('validate.s4', 'Lỗi càng lộ xa chỗ nhập thì càng khó sửa: lúc gửi SMS không còn người dùng nào để hỏi lại số đúng.', 'The further from the input an error surfaces, the harder it is to fix: at SMS time there is no user left to ask for the right number.'),
        ('parse.s2', 'Seemann (7.2.5): thay vì một hàm IsValid trả Boolean, chuyển dữ liệu thô thành object của miền khi điều kiện đúng. Theo Alexis King, parser nhận đầu vào ít cấu trúc và trả đầu ra nhiều cấu trúc hơn, và vì có đầu vào không tương ứng với đầu ra nào nên parser luôn có khả năng thất bại. [[src:book-seemann]]', 'Seemann (7.2.5): instead of an IsValid method returning a Boolean, translate raw data into a domain object when the preconditions hold. As Alexis King puts it, a parser takes less-structured input and produces more-structured output, and since some inputs map to no output, every parser can fail. [[src:book-seemann]]'),
        ('parse.s3', 'Seemann (5.3.1): đóng gói phải bảo đảm object không bao giờ ở trạng thái sai. Với object bất biến, chỉ cần kiểm ở một chỗ: constructor. [[src:book-seemann]]', 'Seemann (5.3.1): encapsulation should guarantee an object is never in an invalid state. With an immutable object you only check in one place: the constructor. [[src:book-seemann]]'),
        ('parse.s4', 'Kiểu riêng khác typealias: tài liệu Kotlin nói typealias gán lẫn được với kiểu gốc, còn value class là một kiểu mới thật sự. Truyền nhầm một String thô vào SmsSender sẽ không biên dịch. [[src:kt-inline-classes]]', 'A dedicated type is not a typealias: the Kotlin docs say a typealias is assignment-compatible with its underlying type, while a value class is a truly new type. Passing a raw String to SmsSender will not compile. [[src:kt-inline-classes]]')]:
        m('co.' + k, vi, en)

    z = lambda k, vi, en=None: a('vz.' + k, vi, en)
    z('tab.parse', 'Dòng chảy dữ liệu', 'Data flow')
    z('ps.cap', 'Mỗi hàng là một số điện thoại, đi từ trái sang phải. Cột mở dần theo bước. Ô ghi kiểu của giá trị ở chặng đó.', 'Each row is one phone number travelling left to right. Columns open step by step. Each cell shows the value\'s type at that stage.')
    for k, vi, en in [('raw', 'Thô (màn hình)', 'Raw (screen)'), ('edge', 'Ranh giới', 'Boundary'), ('inside', 'Bên trong (kho)', 'Inside (storage)'), ('sms', 'Gửi SMS, 2 ngày sau', 'SMS, 2 days later')]:
        z('ps.col.' + k, vi, en)
    for k, vi, en in [('booking', 'form đặt lịch', 'booking form'), ('profile', 'hồ sơ', 'profile'), ('reminder', 'cài đặt nhắc', 'reminder settings')]:
        z('ps.from.' + k, vi, en)
    for k, vi, en in [
        ('pass.booking', 'qua: đủ 10 chữ số', 'passes: 10 digits'),
        ('pass.profile', 'qua: đầu số +84', 'passes: +84 prefix'),
        ('pass.reminder', 'qua: dài ít nhất 9', 'passes: at least 9 long'),
        ('parsed', 'PhoneNumber', 'PhoneNumber'),
        ('rejected', 'null: form báo thiếu chữ số', 'null: the form says a digit is missing'),
        ('string', 'String chưa rõ đã kiểm chưa', 'String, checked or not, unknown'),
        ('typed', 'PhoneNumber', 'PhoneNumber'),
        ('stopped', 'không vào', 'never enters'),
        ('sent', 'đã gửi', 'sent'),
        ('failed', 'hỏng: luật thứ tư từ chối', 'failed: a fourth rule rejects it'),
        ('none', 'không có gì để gửi', 'nothing to send')]:
        z('ps.v.' + k, vi, en)
    z('ps.rules', 'Luật kiểm đang có: {n}', 'Checking rules in play: {n}')
    z('ps.legend', 'Viền đậm: cột vừa mở. Ô gạch đỏ: số sai đi tiếp mà không ai chặn, hay hỏng lúc gửi. Ô đậm: giá trị có kiểu bảo đảm đúng.', 'Bold outline: the column just opened. Red hatched: a bad number moving on unchecked, or failing at send time. Bold: a value whose type guarantees it is valid.')

    C = 'j3'
    a(C + '.title', 'Đóng gói, bất biến, parse một lần', 'Encapsulation, immutability, parse once')
    a(C + '.essence', 'Kiểm hợp lệ rồi trả Boolean làm mất hiểu biết ngay sau lệnh if: giá trị vẫn là String, nơi khác không biết nó đã được kiểm, nên kiểm lại theo luật riêng.\nParse một lần ở ranh giới: chuyển dữ liệu thô thành kiểu của miền (PhoneNumber), hoặc từ chối ngay khi người dùng còn ở đó. Bên trong chỉ nhận kiểu đó.\nObject bất biến chỉ cần kiểm ở constructor; từ đó trở đi nó luôn hợp lệ. Dễ dãi với đầu vào (bỏ khoảng trắng, đổi +84) nhưng chặt với những gì đưa vào trong.',
      'Checking validity and returning a Boolean loses the knowledge right after the if: the value is still a String, other places do not know it was checked, so they check again by their own rule.\nParse once at the boundary: turn raw data into a domain type (PhoneNumber), or reject it while the user is still there. The inside accepts only that type.\nAn immutable object needs checking only in its constructor; from then on it is always valid. Be liberal with input (drop spaces, convert +84) but strict about what goes inside.')
    a(C + '.goal.g1', 'Đã thấy bên trong nhận gì', 'Saw what the inside receives')
    a(C + '.goal.g2', 'Đã thấy kết quả gửi SMS', 'Saw the SMS outcome')
    a(C + '.sim.cleancode.parse', 'kiểm rải rác hay parse một lần', 'scattered checks or parse once')

    S_ = 'hook'
    a(C + '.sec.%s.title' % S_, 'Đoán trước khi đọc', 'Predict before reading')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'predict', 'App có ba màn hình nhập số điện thoại, mỗi màn hình đều "đã kiểm hợp lệ". Vậy mà mỗi tuần vẫn có vài SMS nhắc lịch gửi hỏng. Vì sao kiểm ở ba chỗ vẫn không đủ?',
      'The app has three screens that take a phone number, each one "already validated". Yet every week a few reminder SMS fail. Why are three checks not enough?')
    B(C, S_, 1, 'ans', 'Vì ba chỗ kiểm theo ba luật khác nhau, và sau khi kiểm, số vẫn là một String như mọi String khác. Bộ gửi SMS không biết số đến từ màn hình nào, nên kiểm lần thứ tư theo luật thứ tư, hai ngày sau, khi không còn ai để sửa. Mô phỏng ngay dưới cho ba số đi qua cả hai cách làm.',
      'Because the three checks follow three different rules, and after checking, the number is still a String like any other. The SMS sender does not know which screen it came from, so it checks a fourth time by a fourth rule, two days later, when there is nobody left to fix it. The simulation just below sends three numbers through both approaches.')

    S_ = 'encap'
    a(C + '.sec.%s.title' % S_, 'Đóng gói là hợp đồng, không phải getter và setter', 'Encapsulation is a contract, not getters and setters')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'p', 'Seemann (ch.5) cho rằng đóng gói hay bị hiểu nhầm là "giấu field sau getter, setter". Theo ông, đóng gói là hợp đồng: object nhận đầu vào nào, bảo đảm gì về đầu ra, và quan trọng nhất là không bao giờ ở trạng thái sai. Hợp đồng đơn giản hơn phần cài đặt nên vừa trong đầu hơn; nó nối thẳng với chương J1. [[src:book-seemann]]',
      'Seemann (ch.5) argues encapsulation is often misread as "hide fields behind getters and setters". In his view encapsulation is a contract: which input the object accepts, what it guarantees about output, and above all that it is never in an invalid state. A contract is simpler than the implementation, so it fits in your head better; this ties straight back to chapter J1. [[src:book-seemann]]')
    B(C, S_, 2, 'p', 'Bất biến làm hợp đồng dễ giữ. Với object bất biến, chỉ có một chỗ cần kiểm là constructor; khởi tạo thành công thì object hợp lệ mãi (Seemann 5.3.1). Moskała (Effective Kotlin, Item 1) liệt kê thêm lợi ích: dễ suy luận vì trạng thái không đổi, an toàn khi chạy song song, cache được tham chiếu, không cần sao chép phòng thủ, dùng làm khóa của Map hay phần tử của Set mà không sợ "lạc chỗ". [[src:book-seemann]] [[src:book-effective-kotlin]]',
      'Immutability makes the contract easy to keep. An immutable object has one place to check, the constructor; if construction succeeds, the object stays valid (Seemann 5.3.1). Moskała (Effective Kotlin, Item 1) adds more benefits: easier reasoning since state never changes, safety when running in parallel, references can be cached, no defensive copies, and safe use as Map keys or Set elements without getting "lost". [[src:book-seemann]] [[src:book-effective-kotlin]]')
    B(C, S_, 3, 'note', 'Track Kotlin (K4) cho thấy object bị sửa sau khi đã nằm trong HashSet thì không tìm lại được; K6 dạy require và check. Chương này dùng cả hai để bảo vệ bất biến của PhoneNumber.',
      'The Kotlin track (K4) shows an object mutated after being put in a HashSet can no longer be found; K6 teaches require and check. This chapter uses both to protect PhoneNumber\'s invariant.')
    B(C, S_, 3, 'kind', 'android')

    S_ = 'parse'
    a(C + '.sec.%s.title' % S_, 'Parse một lần thay vì kiểm rồi trả Boolean', 'Parse, don\'t validate')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'p', 'Seemann (7.2.5) đề xuất: thay vì hàm isValid trả Boolean, viết hàm chuyển dữ liệu thô thành object của miền khi mọi điều kiện đúng, và trả "không có gì" khi sai. Kiểu trả về nói hết: kết quả có thể không có, và trình biên dịch buộc người gọi xử lý trường hợp đó. Ông mượn cách gọi parse, don\'t validate của Alexis King: parser biến đầu vào ít cấu trúc thành đầu ra nhiều cấu trúc hơn, và luôn có khả năng thất bại. [[src:book-seemann]]',
      'Seemann (7.2.5) proposes: instead of an isValid function returning a Boolean, write a function that turns raw data into a domain object when every precondition holds, and returns "nothing" when not. The return type says it all: the result may be absent, and the compiler forces callers to handle that. He borrows Alexis King\'s phrase parse, don\'t validate: a parser turns less-structured input into more-structured output, and can always fail. [[src:book-seemann]]')
    B(C, S_, 2, 'kt', '@JvmInline\nvalue class PhoneNumber(val digits: String) {\n    init { require(VN_MOBILE.matches(digits)) }   // không tạo được giá trị sai\n}\nprivate val VN_MOBILE = Regex("0[35789]\\\\d{8}")\n\nfun parsePhone(raw: String): PhoneNumber? {      // ranh giới\n    val d = raw.filter(Char::isDigit)\n    val local = if (d.startsWith("84")) "0" + d.drop(2) else d\n    return if (VN_MOBILE.matches(local)) PhoneNumber(local) else null\n}',
      '@JvmInline\nvalue class PhoneNumber(val digits: String) {\n    init { require(VN_MOBILE.matches(digits)) }   // an invalid value cannot be built\n}\nprivate val VN_MOBILE = Regex("0[35789]\\\\d{8}")\n\nfun parsePhone(raw: String): PhoneNumber? {      // the boundary\n    val d = raw.filter(Char::isDigit)\n    val local = if (d.startsWith("84")) "0" + d.drop(2) else d\n    return if (VN_MOBILE.matches(local)) PhoneNumber(local) else null\n}')
    B(C, S_, 3, 'p', 'Tài liệu Kotlin: value class phải có đúng một property khởi tạo trong constructor chính, được phép có khối init (như require ở trên), và khác typealias ở chỗ nó là kiểu mới thật sự, không gán lẫn được với String. Lúc chạy, giá trị thường được biểu diễn bằng chính String bên trong, nên kiểu riêng gần như không tốn thêm bộ nhớ. [[src:kt-inline-classes]]',
      'The Kotlin docs: a value class must have exactly one property initialised in the primary constructor, may have an init block (like the require above), and unlike a typealias it is a truly new type, not assignment-compatible with String. At runtime the value is usually represented by the underlying String itself, so the dedicated type costs almost no extra memory. [[src:kt-inline-classes]]')

    S_ = 'postel'
    a(C + '.sec.%s.title' % S_, 'Dễ dãi với đầu vào, chặt với bên trong', 'Liberal with input, strict inside')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'p', 'Seemann (5.2.4) diễn giải luật Postel cho thiết kế API: thận trọng với những gì gửi đi, dễ dãi với những gì nhận vào. Ông hiểu là chấp nhận đầu vào chừng nào còn làm việc được với nó; đầu vào không dùng được thì từ chối ngay (fail fast). Ở đây: khoảng trắng, dấu gạch, đầu số +84 đều chấp nhận và chuẩn hóa; số thiếu chữ số thì từ chối ngay tại form. [[src:book-seemann]]',
      'Seemann (5.2.4) paraphrases Postel\'s law for API design: be conservative in what you send, liberal in what you accept. He reads it as accepting input as long as you can meaningfully work with it; input you cannot use is rejected at once (fail fast). Here: spaces, dashes and a +84 prefix are accepted and normalised; a number missing a digit is rejected right at the form. [[src:book-seemann]]')
    B(C, S_, 2, 'p', 'Ông cũng nhắc đừng kiểm quá mức thứ không kiểm được: địa chỉ email rất khó kiểm theo đặc tả, và cách duy nhất biết email đúng là gửi thư tới đó. Với số điện thoại cũng vậy: parse chỉ bảo đảm đúng định dạng, không bảo đảm số đó có thật hay của đúng người; muốn chắc thì gửi mã xác nhận.',
      'He also warns against over-checking what cannot be checked: email addresses are notoriously hard to validate against the spec, and the only way to know one works is to send mail to it. Phone numbers are the same: parsing only guarantees the format, not that the number exists or belongs to the right person; for that, send a confirmation code.')

    S_ = 'boundary'
    a(C + '.sec.%s.title' % S_, 'Ranh giới, null và mã bên thứ ba', 'Boundaries, null and third-party code')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'p', 'Martin (Clean Code ch.7) khuyên đừng trả null và đừng truyền null, vì mã đầy những lệnh kiểm null là mã mà chỉ cần quên một lần là hỏng. Kotlin giải quyết phần lớn chuyện này bằng kiểu: PhoneNumber? buộc người gọi xử lý trường hợp không có, còn PhoneNumber thì không bao giờ null. Ý của Martin chuyển thành: chỉ để kiểu có dấu ? ở ranh giới, bên trong dùng kiểu không null. [[src:book-cleancode]]',
      'Martin (Clean Code ch.7) advises against returning null and passing null, because code full of null checks breaks the one time someone forgets. Kotlin handles most of this with types: PhoneNumber? forces callers to handle absence, while PhoneNumber is never null. Martin\'s point becomes: keep the ? types at the boundary, and use non-null types inside. [[src:book-cleancode]]')
    B(C, S_, 2, 'p', 'Ch.8 bàn về ranh giới với mã bên thứ ba: thư viện được viết để dùng được ở mọi nơi nên giao diện rộng, còn app chỉ cần một phần hẹp. Martin đề xuất bọc nó trong một lớp của mình ở ranh giới; ch.6 phân biệt cấu trúc dữ liệu (lộ dữ liệu, không có hành vi, như DTO từ JSON) với object (giấu dữ liệu, lộ hành vi). Áp vào app: DTO từ server là dữ liệu thô ở ranh giới, parse thành object của miền trước khi vào trong; SDK gửi SMS được bọc sau SmsSender chỉ nhận PhoneNumber. [[src:book-cleancode]]',
      'Ch.8 discusses boundaries with third-party code: libraries are written to work everywhere, so their interfaces are broad, while the app needs a narrow slice. Martin suggests wrapping them in your own class at the boundary; ch.6 distinguishes data structures (expose data, no behaviour, like a DTO from JSON) from objects (hide data, expose behaviour). Applied to an app: a DTO from the server is raw data at the boundary, parsed into a domain object before going inside; the SMS SDK is wrapped behind a SmsSender that only accepts PhoneNumber. [[src:book-cleancode]]')

    S_ = 'bugs'
    a(C + '.sec.%s.title' % S_, 'Hai lỗi hay gặp', 'Two common bugs')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'bug', 'SMS nhắc lịch gửi hỏng với một số người dùng, dù mọi màn hình nhập đều có kiểm hợp lệ.', 'Reminder SMS fail for some users, even though every input screen validates.')
    B(C, S_, 1, 'cause', 'Mỗi màn hình có một hàm kiểm riêng với luật riêng; giá trị qua kiểm vẫn là String và được lưu nguyên chuỗi gốc. Bộ gửi SMS áp luật thứ tư.', 'Each screen has its own check with its own rule; a checked value is still a String and is stored as typed. The SMS sender applies a fourth rule.')
    B(C, S_, 1, 'fix', 'Một hàm parsePhone duy nhất ở ranh giới trả PhoneNumber?; mọi lớp bên trong (kho dữ liệu, SmsSender) chỉ nhận PhoneNumber. Số đã lưu từ trước chạy qua parsePhone một lần khi đọc từ database cũ và đánh dấu số không parse được để hỏi lại người dùng.', 'A single parsePhone at the boundary returns PhoneNumber?; every inner class (storage, SmsSender) takes only PhoneNumber. Numbers already stored go through parsePhone once when read from the old database, and unparseable ones are flagged so the user is asked again.')
    B(C, S_, 2, 'bug', 'Một lịch hẹn trong danh sách đổi giờ khi không ai sửa nó.', 'A booking in the list changes time though nobody edited it.')
    B(C, S_, 2, 'cause', 'Appointment có var time; một màn hình sửa time của object đang nằm chung trong danh sách và trong Set dùng để lọc, nên cả hai chỗ thấy đổi, và Set không còn tìm thấy object ở vị trí cũ.', 'Appointment has var time; one screen mutated time on an object shared by the list and a Set used for filtering, so both see the change, and the Set no longer finds the object in its old position.')
    B(C, S_, 2, 'fix', 'Dùng val và tạo bản mới bằng copy(time = …) khi cần đổi (Effective Kotlin Item 1); bất biến được kiểm một lần ở constructor.', 'Use val and create a new copy with copy(time = …) when a change is needed (Effective Kotlin Item 1); the invariant is checked once in the constructor.')

    S_ = 'ex'
    a(C + '.sec.%s.title' % S_, 'Bài tập', 'Exercise')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'ex', 'Hàm dưới đây nhận số người đi khám cùng (tối đa 3 người đi kèm) từ một ô nhập chữ. Viết lại theo kiểu parse: một kiểu Companions có bất biến, một hàm parse ở ranh giới, và hàm book chỉ nhận kiểu đó.', 'The function below takes the number of companions (at most 3) from a text field. Rewrite it parse-style: a Companions type with an invariant, a parse function at the boundary, and a book function that only takes that type.')
    B(C, S_, 1, 'exkt', 'fun isValidCompanions(s: String): Boolean {\n    val n = s.trim().toIntOrNull() ?: return false\n    return n in 0..3\n}\n\nfun book(slot: Slot, companions: String) {\n    if (!isValidCompanions(companions)) return\n    val n = companions.trim().toInt()       // parse lại lần nữa\n    api.book(slot, n)\n}')
    B(C, S_, 1, 'hint', 'Kiểu nào có thể biểu diễn "từ 0 tới 3"? Hàm parse trả về gì khi sai? book còn cần nhánh kiểm nào không?', 'Which type can represent "0 to 3"? What does parse return on failure? Does book still need any checking branch?')
    B(C, S_, 1, 'sol', 'Tạo value class Companions với init { require(count in 0..3) }; hàm parseCompanions(raw) trả Companions? (bỏ khoảng trắng, toIntOrNull, kiểm khoảng). Form gọi parse và báo lỗi tại chỗ khi null; book(slot, companions: Companions) không còn nhánh kiểm, cũng không parse lại chuỗi. isValid và hai lần toInt biến mất.',
      'Create a value class Companions with init { require(count in 0..3) }; parseCompanions(raw) returns Companions? (trim, toIntOrNull, range check). The form calls parse and shows an inline error on null; book(slot, companions: Companions) has no checking branch and no second parse of the string. The isValid plus double toInt disappears.')
    B(C, S_, 1, 'solkt', '@JvmInline\nvalue class Companions(val count: Int) {\n    init { require(count in 0..3) }\n}\n\nfun parseCompanions(raw: String): Companions? =\n    raw.trim().toIntOrNull()?.takeIf { it in 0..3 }?.let(::Companions)\n\nfun book(slot: Slot, companions: Companions) = api.book(slot, companions.count)')

    S_ = 'honest'
    a(C + '.sec.%s.title' % S_, 'Chương này giản lược những gì', 'What this chapter simplifies')
    a(C + '.sec.%s.badge' % S_, 'simplified')
    B(C, S_, 1, 'p', 'Đóng gói như hợp đồng, object luôn hợp lệ, luật Postel và parse don\'t validate theo Mark Seemann, Code That Fits in Your Head 5.2–5.3 và 7.2.5 (Seemann trích ý Alexis King); null, cấu trúc dữ liệu và object, ranh giới với mã bên thứ ba theo Robert C. Martin, Clean Code ch.6–8; lợi ích của object bất biến theo Marcin Moskała, Effective Kotlin Item 1; value class theo tài liệu Kotlin. Đọc ngày 2026-11-24, diễn đạt lại; ví dụ C# và Java của sách viết lại bằng Kotlin. Luật số di động Việt Nam, ba luật kiểm rải rác và mọi con số là minh họa của site. Chương không bàn Law of Demeter chi tiết, cũng không bàn kiểu lỗi chi tiết thay cho null; track Kiến trúc G8 và Kotlin K6 dạy cách báo lỗi.',
      'Encapsulation as a contract, always-valid objects, Postel\'s law and parse, don\'t validate follow Mark Seemann, Code That Fits in Your Head 5.2–5.3 and 7.2.5 (Seemann quoting Alexis King); null, data structures versus objects and third-party boundaries follow Robert C. Martin, Clean Code ch.6–8; the benefits of immutable objects follow Marcin Moskała, Effective Kotlin Item 1; value classes follow the Kotlin docs. Read on 2026-11-24 and paraphrased; the books\' C# and Java examples are rewritten in Kotlin. The Vietnamese mobile rule, the three scattered rules and every number are the site\'s illustration. The chapter does not cover the Law of Demeter in detail, nor rich error types in place of null; the Architecture track G8 and Kotlin K6 teach error reporting.')

    for q, qv, qe, av, ae, wv, we in [
        ('q1', 'Vì sao fun isValid(s: String): Boolean để lại vấn đề cho những chỗ khác?', 'Why does fun isValid(s: String): Boolean leave a problem for other places?', 'Vì sau lệnh if, giá trị vẫn là String; nơi khác không biết nó đã được kiểm.', 'Because after the if the value is still a String; other places cannot tell it was checked.', 'Parse trả về kiểu riêng mang theo bảo đảm đó.', 'Parsing returns a dedicated type that carries the guarantee.'),
        ('q2', 'Object bất biến cần kiểm hợp lệ ở mấy chỗ?', 'How many places must an immutable object be validated in?', 'Một: constructor.', 'One: the constructor.', 'Khởi tạo thành công thì không có thao tác nào làm nó sai được nữa (Seemann 5.3.1).', 'Once constructed, no operation can make it invalid (Seemann 5.3.1).'),
        ('q3', 'value class PhoneNumber khác typealias PhoneNumber = String ở đâu?', 'How does value class PhoneNumber differ from typealias PhoneNumber = String?', 'value class là kiểu mới, không gán lẫn với String; typealias chỉ là tên khác.', 'A value class is a new type, not assignment-compatible with String; a typealias is just another name.', 'Với typealias, truyền nhầm String thô vẫn biên dịch được.', 'With a typealias, passing a raw String by mistake still compiles.'),
        ('q4', 'parsePhone có bảo đảm số điện thoại có thật không?', 'Does parsePhone guarantee the phone number exists?', 'Không; chỉ bảo đảm đúng định dạng.', 'No; it only guarantees the format.', 'Muốn chắc số có thật và của đúng người thì gửi mã xác nhận.', 'To be sure it exists and belongs to the right person, send a confirmation code.')]:
        a(C + '.quiz.%s.q' % q, qv, qe); a(C + '.quiz.%s.a' % q, av, ae); a(C + '.quiz.%s.why' % q, wv, we)
