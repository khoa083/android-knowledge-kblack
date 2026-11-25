# Lập trình hàm · K7 (p7): validate gom lỗi: applicative và monoid (Phần 2: lỗi, ngữ cảnh và state)
# Nguồn (chỉ ghi ở đây và docs/research/fp.md): Vermeulen, Bjarnason, Chiusano, FP in Kotlin 4.4 (Listing 4.8, Exercise 4.8: map2 chỉ báo một lỗi),
# 10.1 (monoid), 12.3 (applicative so với monad: cấu trúc cố định hay phụ thuộc kết quả trước), 12.4 (Validation giữ nhiều lỗi, form web);
# Carli, FP in Kotlin by Tutorials ch.12 (monoid, semigroup), ch.14 (fail fast hay gom lỗi, Semigroup gộp lỗi kiểm dữ liệu);
# Arrow typed errors: validation, working with typed errors (zipOrAccumulate, mapOrAccumulate, NonEmptyList; đọc 2026-11-25). Giọng văn dạy học.

SEC_ORDER = {'p7': ['hook', 'indep', 'kotlin', 'monoid', 'arrow', 'bugs', 'ex', 'recall']}


def add(a):
    def B(ch, sec, n, field, vi, en=None):
        a('%s.sec.%s.b.%02d.%s' % (ch, sec, n, field), vi, vi if en is None else en)

    a('preset.validate', '''Lập trình hàm · validate gom lỗi''', '''Functional programming · validation that collects errors''')
    m = lambda k, vi, en=None: a('m.validate.' + k, vi, en)
    m('title', '''Form bốn ô sai: báo từng lỗi hay báo đủ''', '''A form with four wrong fields: one error at a time, or all of them''')
    m('overview', '''Form đăng ký bệnh nhân của app Hẹn Khám có 4 ô: họ tên, số điện thoại, ngày sinh, mã thẻ bảo hiểm. Người dùng nhập sai cả 4. Ta so hai cách kiểm: nối các ô bằng flatMap (dừng ở lỗi đầu tiên), và kiểm mọi ô rồi gộp lỗi. Mỗi lần nộp, người dùng sửa đúng những lỗi được báo rồi nộp lại.''',
      '''The ClinicBook patient sign-up form has 4 fields: full name, phone number, date of birth, insurance card code. The user gets all 4 wrong. We compare two ways of checking: chaining the fields with flatMap (stop at the first error), and checking every field and then combining the errors. Each time, the user fixes exactly the errors shown and submits again.''')
    m('wrapup', '''Dừng sớm bắt người dùng nộp 5 lần cho 4 lỗi độc lập; gom lỗi báo đủ 4 lỗi ngay lần đầu, và lần nộp thứ hai là qua. Gom lỗi chỉ dành cho các bước độc lập; luật cần một giá trị đã hợp lệ (số đã đăng ký chưa) vẫn nối sau bằng flatMap.''',
      '''Stopping early makes the user submit 5 times for 4 independent errors; collecting errors reports all 4 on the first try, and the second submission passes. Collecting errors is only for independent steps; a rule that needs an already valid value (is the number already registered) is still chained afterwards with flatMap.''')
    m('simp.1', '''Người dùng trong mô phỏng sửa đúng và đủ những lỗi được báo; người thật có thể sửa sai hay gõ ra lỗi mới.''',
      '''The simulated user fixes exactly the errors shown, correctly; a real user may fix them wrongly or type new mistakes.''')
    m('simp.2', '''Các hàm kiểm tên, số điện thoại, ngày sinh (31/02 không có thật), mã thẻ và phép nối list chạy thật bằng JavaScript. API gom lỗi của Arrow theo các trang validation và working with typed errors (đọc ngày 2026-11-25). Outcome và errorOrNull là mã tự viết của site; site không chạy Kotlin trong trang.''',
      '''The checks for name, phone number, date of birth (31/02 does not exist), card code and the list concatenation really run in JavaScript. Arrow\'s error-collecting API follows its validation and working-with-typed-errors pages (read on 2026-11-25). Outcome and errorOrNull are code the site writes itself; the site does not run Kotlin in the page.''')
    m('ctl.hint', '''Chọn cách kiểm rồi đi qua bốn bước; đếm số lần nộp và số lỗi được báo mỗi lần.''', '''Pick a way of checking and walk the four steps; count the submissions and the errors shown each time.''')
    m('ctl.case', '''Cách kiểm form''', '''How the form is checked''')
    m('ctl.case.fast', '''dừng ở lỗi đầu tiên (flatMap)''', '''stop at the first error (flatMap)'''); m('ctl.case.acc', '''kiểm hết rồi gom lỗi''', '''check everything, then collect the errors''')
    m('diagramTitle', '''Form, các hàm kiểm, gộp lỗi, bước phụ thuộc, màn hình''', '''Form, field checks, combining errors, a dependent step, screen''')
    m('diagramDesc', '''Form đi qua các hàm kiểm từng ô; lỗi được gộp rồi tới màn hình; bước phụ thuộc chạy sau khi mọi ô hợp lệ''', '''The form goes through each field\'s check; the errors are combined and reach the screen; a dependent step runs once every field is valid''')
    for k, vi, en in [('form', 'Form đăng ký', 'Sign-up form'), ('checks', 'Hàm kiểm từng ô', 'Per-field checks'), ('screen', 'Lỗi trên màn hình', 'Errors on screen'),
                      ('merge', 'Gộp lỗi (monoid)', 'Combining errors (monoid)'), ('dep', 'Bước phụ thuộc (flatMap)', 'Dependent step (flatMap)')]:
        m('n.' + k, vi, en)
    m('met.submits', '''Lần nộp''', '''Submission'''); m('met.shown', '''Lỗi được báo lần này''', '''Errors shown this time''')
    m('met.checked', '''Số ô được kiểm''', '''Fields checked'''); m('met.unknown', '''Lỗi còn bị giấu''', '''Errors still hidden''')
    a('cap.validate', '''Form đi qua các hàm kiểm từng ô; lỗi tới màn hình, hoặc được gộp lại trước; bước phụ thuộc chạy sau cùng. Ô đỏ: người dùng chưa thấy đủ lỗi.''',
      '''The form goes through each field\'s check; errors reach the screen, or are combined first; the dependent step runs last. A red box: the user has not seen every error yet.''')
    S = [
        ('fast', 's1', 'Lần nộp 1: chỉ thấy lỗi đầu tiên', 'Submission 1: only the first error shows',
         'Form có 4 ô sai: tên trống, số điện thoại 9 chữ số, ngày sinh 31/02/1990 (không có ngày này), mã thẻ sai dạng. Chuỗi flatMap kiểm ô tên trước, gặp lỗi là dừng, nên ba ô sau không được kiểm. Người dùng chỉ đọc "Tên không được để trống".',
         'The form has 4 wrong fields: an empty name, a 9-digit phone number, a birth date of 31/02/1990 (no such day), a wrongly formatted card code. The flatMap chain checks the name first and stops at the error, so the other three fields are never checked. The user only reads "Name must not be empty".'),
        ('fast', 's2', 'Lần nộp 2: lỗi thứ hai mới lộ ra', 'Submission 2: the second error appears',
         'Người dùng sửa tên rồi nộp lại. Ô tên qua, chuỗi dừng ở số điện thoại. Lỗi này có từ đầu, nhưng lần trước chưa ai kiểm tới.',
         'The user fixes the name and submits again. The name passes, and the chain stops at the phone number. That error was there from the start, but nobody checked it last time.'),
        ('fast', 's3', 'Lần nộp 3: lại thêm một lỗi', 'Submission 3: yet another error',
         'Sửa số điện thoại, nộp lại, chuỗi dừng ở ngày sinh. Với người dùng, form như cứ đẻ thêm lỗi sau mỗi lần sửa.',
         'Fix the phone number, submit again, and the chain stops at the birth date. To the user, the form seems to grow a new error after every fix.'),
        ('fast', 's4', 'Lần nộp 4, rồi lần 5', 'Submission 4, then 5',
         'Lần 4 báo mã thẻ sai; phải tới lần nộp thứ 5 form mới qua. Bốn lỗi độc lập với nhau, nhưng bị báo lần lượt chỉ vì flatMap dừng ở lỗi đầu tiên.',
         'Submission 4 reports the wrong card code; only the 5th submission passes. The four errors are independent of each other, yet they are reported one by one, only because flatMap stops at the first error.'),
        ('acc', 's1', 'Kiểm mọi ô, báo đủ 4 lỗi', 'Check every field, report all 4 errors',
         'Bốn hàm kiểm chạy độc lập, mỗi hàm cho Ok hoặc Err. Không ô nào phải chờ ô khác, nên cả bốn đều được kiểm, và màn hình báo đủ 4 lỗi ngay lần nộp đầu.',
         'The four checks run independently, each giving Ok or Err. No field waits for another, so all four are checked, and the screen reports all 4 errors on the first submission.'),
        ('acc', 's2', 'Gộp lỗi bằng phép nối list', 'Combining errors by joining lists',
         'Bốn kết quả được gộp lại: list lỗi của từng ô nối thành một list, ô hợp lệ góp một list rỗng. Phép nối list có tính kết hợp và có phần tử đơn vị là [], nên gộp theo thứ tự nào cũng ra một kết quả: đó là một monoid.',
         'The four results are combined: each field\'s error list is joined into one list, and a valid field contributes an empty list. Joining lists is associative and has [] as its identity element, so any grouping gives the same result: that is a monoid.'),
        ('acc', 's3', 'Lần nộp 2 là qua', 'The second submission passes',
         'Người dùng sửa cả 4 ô một lượt rồi nộp lại. Mọi ô là Ok, nên tạo được Patient. Hai lần nộp thay vì năm.',
         'The user fixes all 4 fields in one go and submits again. Every field is Ok, so a Patient can be built. Two submissions instead of five.'),
        ('acc', 's4', 'Bước phụ thuộc: gom xong mới flatMap', 'A dependent step: collect first, then flatMap',
         'Nhóm thêm luật "số điện thoại chưa có ai đăng ký". Luật này cần một số đã hợp lệ, tức phụ thuộc vào kết quả của ô số điện thoại, nên không gom chung được: nó nối sau bằng flatMap. Số 0901234567 đã có người dùng, nên kết quả là lỗi "số này đã được đăng ký".',
         'The team adds the rule "the phone number is not registered yet". This rule needs an already valid number, so it depends on the phone field\'s result and cannot be collected with the others: it is chained afterwards with flatMap. The number 0901234567 is already in use, so the result is the error "this number is already registered".'),
    ]
    for case, k, tv, te, xv, xe in S:
        sid = case + '.' + k
        m('s.%s.title' % sid, tv, te); m('s.%s.explain' % sid, xv, xe); m('ev.' + sid, tv, te)
    for k, vi, en in [
        ('try', '''Mẹo đọc: mỗi hàng là một ô của form. Cột "Kiểm" cho biết hàm kiểm của ô đó có chạy ở lần nộp này không; ô mờ là chưa được kiểm. Đổi sang "kiểm hết rồi gom lỗi" để so.''',
         '''Reading tip: each row is a form field. The "Check" column says whether that field\'s check ran on this submission; a faded field was not checked. Switch to "check everything, then collect the errors" to compare.'''),
        ('fast.s2', '''Marco Vermeulen và cộng sự chỉ ra: gộp hai kết quả kiểu Either ("lỗi hoặc kết quả") bằng map2 chỉ báo được một lỗi, kể cả khi cả tên lẫn tuổi đều sai. [[src:book-fp-manning]]''',
         '''Marco Vermeulen and co-authors point out: combining two Either ("error or result") values with map2 can only report one error, even when both the name and the age are wrong. [[src:book-fp-manning]]'''),
        ('fast.s3', '''Massimo Carli: dừng sớm hợp khi không thể đi tiếp vì thiếu dữ liệu của bước trước; còn kiểm dữ liệu, như một địa chỉ có thể sai vì nhiều lý do, thì nên gom hết lỗi. [[src:book-fp-tut]]''',
         '''Massimo Carli: failing fast fits when you cannot go on without the previous step\'s data; validating data, such as an address that can be wrong for many reasons, should collect every error. [[src:book-fp-tut]]'''),
        ('fast.s4', '''Tài liệu Arrow đặt hai cách cạnh nhau: dừng ngay ở lỗi đầu tiên (short-circuit), và gom mọi lỗi mà không dừng. [[src:arrow-validation]]''',
         '''The Arrow docs set the two side by side: stop right at the first error (short-circuit), and collect every error without stopping. [[src:arrow-validation]]'''),
        ('acc.s1', '''Vermeulen và cộng sự: với applicative, cấu trúc tính toán cố định từ trước và các bước không phụ thuộc nhau; với monad, kết quả của bước trước quyết định bước sau chạy gì. [[src:book-fp-manning]]''',
         '''Vermeulen and co-authors: with an applicative, the structure of the computation is fixed in advance and the steps do not depend on each other; with a monad, the result of a previous step decides what runs next. [[src:book-fp-manning]]'''),
        ('acc.s2', '''Monoid là một kiểu cùng một phép gộp có tính kết hợp và một phần tử đơn vị: nối list với [], cộng số với 0, nối chuỗi với "". [[src:book-fp-manning]] [[src:book-fp-tut]]''',
         '''A monoid is a type with an associative combining operation and an identity element: joining lists with [], adding numbers with 0, joining strings with "". [[src:book-fp-manning]] [[src:book-fp-tut]]'''),
        ('acc.s3', '''Vermeulen và cộng sự dựng một kiểu Validation giống Either nhưng giữ được nhiều lỗi, cho đúng ví dụ một form có tên, ngày sinh và số điện thoại. [[src:book-fp-manning]]''',
         '''Vermeulen and co-authors build a Validation type like Either but able to hold several errors, for exactly this kind of form with a name, a birth date and a phone number. [[src:book-fp-manning]]'''),
        ('acc.s4', '''Gom lỗi chỉ dùng cho các bước độc lập. Bước cần kết quả của bước khác, như kiểm số đã đăng ký, vẫn nối bằng flatMap sau khi các ô đã qua. [[src:book-fp-manning]]''',
         '''Collecting errors is only for independent steps. A step that needs another step\'s result, such as checking whether the number is registered, is still chained with flatMap once the fields pass. [[src:book-fp-manning]]'''),
    ]:
        m('co.' + k, vi, en)

    z = lambda k, vi, en=None: a('vz.' + k, vi, en)
    z('tab.validate', '''Các ô của form và lỗi''', '''Form fields and errors''')
    for k, vi, en in [('name', 'Họ tên', 'Full name'), ('phone', 'Số điện thoại', 'Phone number'), ('dob', 'Ngày sinh', 'Date of birth'), ('card', 'Mã thẻ bảo hiểm', 'Insurance card code'), ('dep', 'Số đã đăng ký? (bước phụ thuộc)', 'Already registered? (dependent step)')]:
        z('validate.f.' + k, vi, en)
    for k, vi, en in [('ok', 'đã kiểm, hợp lệ', 'checked, valid'), ('err', 'đã kiểm, sai', 'checked, wrong'), ('unchecked', 'chưa kiểm', 'not checked')]:
        z('validate.st.' + k, vi, en)
    for k, vi, en in [('EmptyName', 'Tên không được để trống', 'Name must not be empty'), ('PhoneDigits', 'Số điện thoại phải có 10 chữ số', 'The phone number must have 10 digits'),
                      ('BadDate', 'Ngày sinh không có thật', 'That birth date does not exist'), ('CardFormat', 'Mã thẻ phải có dạng BHYT-1234', 'The card code must look like BHYT-1234'),
                      ('PhoneTaken', 'Số này đã được đăng ký', 'This number is already registered')]:
        z('validate.e.' + k, vi, en)
    for k, vi, en in [('field', 'Ô', 'Field'), ('value', 'Giá trị lần nộp này', 'Value this submission'), ('checked', 'Kiểm', 'Check'), ('error', 'Lỗi người dùng thấy', 'Error the user sees')]:
        z('validate.col.' + k, vi, en)
    z('validate.res.ok', '''Kết quả: tạo được Patient, đăng ký xong.''', '''Result: a Patient is built, sign-up done.''')
    z('validate.res.taken', '''Kết quả: các ô đều hợp lệ, nhưng bước phụ thuộc báo số đã được đăng ký.''', '''Result: every field is valid, but the dependent step reports the number is already registered.''')
    z('validate.res.err', '''Kết quả: báo {n} lỗi.''', '''Result: {n} errors reported.''')
    z('validate.cap.fast', '''Dừng ở lỗi đầu tiên · lần nộp thứ {n}''', '''Stop at the first error · submission {n}''')
    z('validate.cap.acc', '''Kiểm hết rồi gom lỗi · lần nộp thứ {n}''', '''Check everything, then collect · submission {n}''')
    z('validate.total.fast', '''Với cách này, người dùng phải nộp {n} lần mới qua form.''', '''With this approach, the user must submit {n} times to get through the form.''')
    z('validate.total.acc', '''Với cách này, người dùng nộp {n} lần là qua form.''', '''With this approach, the user gets through the form in {n} submissions.''')
    z('validate.legend', '''Đỏ: ô sai. Xanh: ô hợp lệ. Mờ: ô chưa được kiểm ở lần nộp này, nên lỗi của nó (nếu có) còn bị giấu.''',
      '''Red: a wrong field. Green: a valid field. Faded: a field not checked on this submission, so its error (if any) is still hidden.''')

    C = 'p7'
    a(C + '.title', '''Validate gom lỗi: applicative và monoid''', '''Validation that collects errors: applicatives and monoids''')
    a(C + '.essence', '''Nối các bước bằng flatMap thì dừng ở lỗi đầu tiên: đúng khi bước sau cần kết quả bước trước, nhưng với một form thì người dùng phải sửa từng lỗi một.\nCác bước độc lập (các ô của form) nên được kiểm hết rồi gộp mọi lỗi; kiểu biết gộp các kết quả độc lập như vậy gọi là applicative. Lỗi được gộp bằng một monoid: phép gộp có tính kết hợp cùng một phần tử đơn vị, như nối list với [].\nKotlin thuần làm được: gọi mọi hàm kiểm, gộp lỗi, chỉ tạo kết quả khi tất cả là Ok. Arrow có zipOrAccumulate. Bước phụ thuộc vẫn nối sau bằng flatMap.''',
      '''Chaining steps with flatMap stops at the first error: right when a later step needs an earlier result, but with a form the user has to fix one error at a time.\nIndependent steps (the fields of a form) should all be checked and every error combined; a type that knows how to combine independent results like this is called an applicative. Errors are combined with a monoid: an associative combining operation plus an identity element, such as joining lists with [].\nPlain Kotlin can do it: call every check, combine the errors, and build the result only when everything is Ok. Arrow has zipOrAccumulate. A dependent step is still chained afterwards with flatMap.''')
    a(C + '.goal.g1', '''Đã đếm số lần nộp form''', '''Counted the form submissions''')
    a(C + '.goal.g2', '''Đã thấy bước phụ thuộc nối sau bước gom lỗi''', '''Saw a dependent step chained after collecting errors''')
    a(C + '.sim.fp.validate', '''dừng ở lỗi đầu tiên hay gom mọi lỗi''', '''stop at the first error or collect them all''')

    S_ = 'hook'
    a(C + '.sec.%s.title' % S_, '''Đoán trước khi đọc''', '''Predict before reading''')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'predict', '''Form đăng ký có 4 ô, và người dùng nhập sai cả 4. Nếu hàm kiểm nối các ô bằng flatMap như ở chương trước, người dùng phải nộp form bao nhiêu lần mới qua?''',
      '''A sign-up form has 4 fields, and the user gets all 4 wrong. If the check chains the fields with flatMap as in the previous chapter, how many times must the user submit before the form passes?''')
    B(C, S_, 1, 'ans', '''5 lần. flatMap dừng ở lỗi đầu tiên, nên mỗi lần nộp chỉ báo một lỗi, và phải sửa xong cả 4 mới qua ở lần thứ 5. Bốn ô không phụ thuộc nhau, nên có thể kiểm hết một lượt rồi báo đủ 4 lỗi. Mô phỏng ngay dưới so hai cách.''',
      '''5 times. flatMap stops at the first error, so each submission reports just one error, and only after all 4 are fixed does the 5th pass. The four fields do not depend on each other, so they can all be checked at once and all 4 errors reported. The simulation just below compares the two ways.''')

    S_ = 'indep'
    a(C + '.sec.%s.title' % S_, '''Bước phụ thuộc và bước độc lập''', '''Dependent steps and independent steps''')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'p', '''Ở chương "Lỗi là giá trị", quy trình đặt lịch dừng ở lỗi đầu tiên (fail fast), và ở chương "map và flatMap: functor và monad qua ví dụ" ta nối nó bằng flatMap. Cách đó đúng cho đặt lịch, vì bước sau cần kết quả bước trước: chưa có số điện thoại hợp lệ thì không kiểm được lượt. Dừng sớm là chuyện tự nhiên của flatMap: hàm ở bước sau nhận giá trị của bước trước, và khi bước trước hỏng thì không có giá trị nào để đưa vào. [[src:book-fp-tut]]''',
      '''In the chapter "Errors as values", the booking flow stopped at the first error (fail fast), and in the chapter "map and flatMap: functors and monads by example" we chained it with flatMap. That is right for booking, because a later step needs an earlier result: without a valid phone number, the quota cannot be checked. Stopping early is natural for flatMap: the next step\'s function receives the previous step\'s value, and when the previous step fails there is no value to pass in. [[src:book-fp-tut]]''')
    B(C, S_, 2, 'p', '''Các ô của form thì khác: kiểm tên không cần biết ngày sinh, kiểm ngày sinh không cần biết số điện thoại. Các bước độc lập nên chạy hết rồi gộp lỗi lại. Marco Vermeulen và cộng sự mô tả đúng khác biệt này: với applicative (kiểu biết gộp các kết quả độc lập, như map2 gộp hai giá trị), cấu trúc tính toán cố định từ trước; với monad, kết quả bước trước quyết định bước sau. Mọi monad đều là applicative, nhưng flatMap của nó luôn dừng sớm, nên muốn gom lỗi phải dùng một cách gộp khác. [[src:book-fp-manning]]''',
      '''Form fields are different: checking the name does not need the birth date, checking the birth date does not need the phone number. Independent steps should all run, and then their errors are combined. Marco Vermeulen and co-authors describe exactly this difference: with an applicative (a type that knows how to combine independent results, as map2 combines two values), the structure of the computation is fixed in advance; with a monad, the previous result decides the next step. Every monad is an applicative, but its flatMap always stops early, so collecting errors needs a different way of combining. [[src:book-fp-manning]]''')
    B(C, S_, 3, 'note', '''Quy tắc dễ nhớ: bước sau cần giá trị của bước trước thì nối bằng flatMap và chấp nhận dừng sớm; các bước không cần nhau thì kiểm hết rồi gộp lỗi.''',
      '''An easy rule: if a step needs the previous step\'s value, chain it with flatMap and accept stopping early; if the steps do not need each other, check them all and combine the errors.''')
    B(C, S_, 3, 'kind', 'mechanism')

    S_ = 'kotlin'
    a(C + '.sec.%s.title' % S_, '''Gom lỗi bằng Kotlin thuần''', '''Collecting errors in plain Kotlin''')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'p', '''Không cần thư viện. Mỗi ô có một hàm kiểm trả Outcome<FormError, T>. Gọi cả bốn hàm, lấy lỗi của những ô hỏng ra một list, và chỉ tạo Patient khi cả bốn đều Ok. Hàm phụ errorOrNull lấy lỗi ra khỏi một Outcome:''',
      '''No library needed. Each field has a check returning Outcome<FormError, T>. Call all four, pull the errors of the failing fields into one list, and build the Patient only when all four are Ok. The helper errorOrNull takes the error out of an Outcome:''')
    B(C, S_, 2, 'kt', '''fun <E, A> Outcome<E, A>.errorOrNull(): E? = when (this) {
    is Err -> error
    is Ok -> null
}''')
    B(C, S_, 3, 'p', '''Hàm register trong đoạn mã của mô phỏng (cách "kiểm hết rồi gom lỗi") làm đúng như vậy; kiểu trả về là Outcome<List<FormError>, Patient>, tức phía lỗi là cả một list. Nhờ smart cast (tự coi là kiểu hẹp hơn) sau `name is Ok && …`, dòng tạo Patient đọc được name.value mà không cần `!!`. Luật phụ thuộc (số đã đăng ký) nối sau bằng flatMap, ở dòng cuối của đoạn mã đó.''',
      '''The register function in the simulation\'s code (the "check everything, then collect" way) does exactly this; its return type is Outcome<List<FormError>, Patient>, so the error side is a whole list. Thanks to the smart cast (treating a value as the narrower type) after `name is Ok && …`, the line that builds the Patient can read name.value without `!!`. The dependent rule (is the number registered) is chained afterwards with flatMap, on the last line of that code.''')

    S_ = 'monoid'
    a(C + '.sec.%s.title' % S_, '''Gộp lỗi: monoid''', '''Combining errors: monoids''')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'p', '''Để gộp lỗi của bốn ô, ta cần một phép gộp hai thứ cùng kiểu thành một thứ cùng kiểu: ở đây là nối hai list lỗi. Phép này có hai tính chất. Kết hợp: (a + b) + c bằng a + (b + c), nên gộp theo thứ tự nào cũng ra một kết quả. Có phần tử đơn vị: [] nối với a vẫn là a, nên ô hợp lệ góp một list rỗng mà không làm sai gì. Một kiểu cùng phép gộp như vậy gọi là monoid. [[src:book-fp-manning]] [[src:book-fp-tut]]''',
      '''To combine the errors of four fields we need an operation that merges two things of a type into one thing of the same type: here, joining two error lists. It has two properties. Associative: (a + b) + c equals a + (b + c), so any grouping gives the same result. An identity element: [] joined with a is still a, so a valid field contributes an empty list without breaking anything. A type with such an operation is called a monoid. [[src:book-fp-manning]] [[src:book-fp-tut]]''')
    B(C, S_, 2, 'p', '''Bạn đã dùng monoid nhiều lần mà không gọi tên: cộng số với 0, nối chuỗi với "", nối list với emptyList(). Bỏ phần tử đơn vị, chỉ giữ phép gộp có tính kết hợp, thì gọi là semigroup. Massimo Carli gộp lỗi kiểm dữ liệu bằng đúng một semigroup như vậy. [[src:book-fp-tut]]''',
      '''You have used monoids many times without naming them: adding numbers with 0, joining strings with "", joining lists with emptyList(). Drop the identity element and keep only the associative operation, and it is called a semigroup. Massimo Carli combines validation errors with exactly such a semigroup. [[src:book-fp-tut]]''')
    B(C, S_, 3, 'kt', '''val a = listOf("EmptyName"); val b = listOf("PhoneDigits"); val c = listOf("BadDate")
(a + b) + c == a + (b + c)                                       // true: kết hợp
emptyList<String>() + a == a                                     // true: [] là phần tử đơn vị
listOf(a, b, c).fold(emptyList<String>()) { acc, x -> acc + x }   // gộp nhiều list''', '''val a = listOf("EmptyName"); val b = listOf("PhoneDigits"); val c = listOf("BadDate")
(a + b) + c == a + (b + c)                                       // true: associative
emptyList<String>() + a == a                                     // true: [] is the identity
listOf(a, b, c).fold(emptyList<String>()) { acc, x -> acc + x }   // combine many lists''')

    S_ = 'arrow'
    a(C + '.sec.%s.title' % S_, '''Arrow: gom lỗi bằng zipOrAccumulate''', '''Arrow: collecting errors with zipOrAccumulate''')
    a(C + '.sec.%s.badge' % S_, 'version')
    B(C, S_, 1, 'p', '''Arrow (thư viện bên ngoài; trang cài đặt ghi bản 2.3.0, tài liệu đọc ngày 2026-11-25) có sẵn cách gom lỗi. `zipOrAccumulate` nhận vài khối kiểm độc lập và một hàm tạo kết quả; nếu có khối hỏng, nó trả mọi lỗi trong một `NonEmptyList` (list luôn có ít nhất một phần tử, nên chỉ là semigroup). Arrow còn có `mapOrAccumulate` để kiểm từng phần tử của một list và gom lỗi của tất cả. [[src:arrow-validation]]''',
      '''Arrow (an external library; its setup page lists version 2.3.0, docs read on 2026-11-25) ships a way to collect errors. `zipOrAccumulate` takes several independent check blocks and a function that builds the result; if any block fails, it returns every error in a `NonEmptyList` (a list that always has at least one element, so only a semigroup). Arrow also has `mapOrAccumulate` to check each element of a list and collect all their errors. [[src:arrow-validation]]''')
    B(C, S_, 2, 'kt', '''fun register(f: Form): Either<NonEmptyList<FormError>, Patient> = either {
    zipOrAccumulate(
        { validName(f.name).bind() },
        { validPhone(f.phone).bind() },
        { validDob(f.dob).bind() },
        { validCard(f.card).bind() }
    ) { name, phone, dob, card -> Patient(name, phone, dob, card) }
}''')
    B(C, S_, 3, 'p', '''Ở đây các hàm validX trả Either<FormError, T>. Tài liệu Arrow đặt hai cách cạnh nhau: dừng ngay ở lỗi đầu tiên, hay gom mọi lỗi mà không dừng. Bản Kotlin thuần ở mục trước làm cùng việc, chỉ dài hơn vài dòng. [[src:arrow-validation]]''',
      '''Here the validX functions return Either<FormError, T>. The Arrow docs set the two ways side by side: stop right at the first error, or collect every error without stopping. The plain Kotlin version above does the same job, just a few lines longer. [[src:arrow-validation]]''')

    S_ = 'bugs'
    a(C + '.sec.%s.title' % S_, '''Hai lỗi hay gặp''', '''Two common bugs''')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'bug', '''Người dùng phàn nàn form đăng ký "báo lỗi từng cái một", phải bấm Gửi 5 lần.''', '''Users complain the sign-up form "reports errors one at a time" and they had to press Send 5 times.''')
    B(C, S_, 1, 'cause', '''Hàm kiểm nối các ô bằng flatMap (hoặc một chuỗi return sớm), nên dừng ở ô sai đầu tiên.''', '''The check chains the fields with flatMap (or a series of early returns), so it stops at the first wrong field.''')
    B(C, S_, 1, 'fix', '''Kiểm mọi ô độc lập rồi gộp lỗi; chỉ nối bằng flatMap những bước thật sự cần kết quả của bước trước.''', '''Check every field independently and combine the errors; chain with flatMap only the steps that really need an earlier result.''')
    B(C, S_, 2, 'bug', '''Mỗi lần người dùng gõ sai số điện thoại, app vẫn gọi máy chủ hỏi "số này đã đăng ký chưa", và nhật ký máy chủ đầy lỗi 400 (yêu cầu sai dạng).''',
      '''Every time a user mistypes the phone number, the app still asks the server "is this number registered", and the server log fills with 400 errors (malformed requests).''')
    B(C, S_, 2, 'cause', '''Kiểm "số đã đăng ký" được gom chung với các kiểm từng ô, nên chạy cả khi số còn sai dạng.''', '''The "already registered" check was collected together with the per-field checks, so it runs even when the number is still malformed.''')
    B(C, S_, 2, 'fix', '''Bước phụ thuộc chạy sau, nối bằng flatMap, chỉ khi ô số điện thoại đã hợp lệ.''', '''Run the dependent step afterwards, chained with flatMap, only once the phone field is valid.''')

    S_ = 'ex'
    a(C + '.sec.%s.title' % S_, '''Bài tập''', '''Exercise''')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'ex', '''Form "Đổi thông tin" có 3 ô: email (phải có @), chiều cao tính bằng cm (số nguyên từ 50 tới 250), và nhóm máu (A, B, AB hoặc O). Viết hàm kiểm từng ô trả Outcome<String, T>, rồi viết `update(email, height, blood)` trả Outcome<List<String>, Profile> báo đủ mọi lỗi. Thử với email "lan.gmail.com", chiều cao "1m60", nhóm máu "C": phải ra đủ 3 lỗi.''',
      '''The "Edit profile" form has 3 fields: email (must contain @), height in cm (a whole number from 50 to 250), and blood type (A, B, AB or O). Write a check for each field returning Outcome<String, T>, then write `update(email, height, blood)` returning Outcome<List<String>, Profile> that reports every error. Try email "lan.gmail.com", height "1m60", blood type "C": you must get all 3 errors.''')
    B(C, S_, 1, 'hint', '''Viết giống register: gọi cả ba hàm, gộp lỗi bằng mapNotNull { it.errorOrNull() }, chỉ tạo Profile khi cả ba là Ok.''', '''Write it like register: call all three checks, combine the errors with mapNotNull { it.errorOrNull() }, and build the Profile only when all three are Ok.''')
    B(C, S_, 1, 'sol', '''Ba ô độc lập nên gom được; với đầu vào trong đề, list lỗi có đủ 3 phần tử theo thứ tự các ô.''', '''The three fields are independent, so their errors can be collected; with the given input, the error list has all 3 entries in field order.''')
    B(C, S_, 1, 'solkt', '''enum class Blood { A, B, AB, O }
data class Profile(val email: String, val heightCm: Int, val blood: Blood)

fun validEmail(s: String): Outcome<String, String> = if ("@" in s) Ok(s) else Err("Email thiếu @")
fun validHeight(s: String): Outcome<String, Int> =
    s.toIntOrNull()?.takeIf { it in 50..250 }?.let { Ok(it) } ?: Err("Chiều cao phải là số cm từ 50 tới 250")
fun validBlood(s: String): Outcome<String, Blood> =
    Blood.entries.firstOrNull { it.name == s }?.let { Ok(it) } ?: Err("Nhóm máu phải là A, B, AB hoặc O")

fun update(email: String, height: String, blood: String): Outcome<List<String>, Profile> {
    val e = validEmail(email); val h = validHeight(height); val b = validBlood(blood)
    val errors = listOf(e, h, b).mapNotNull { it.errorOrNull() }
    return if (e is Ok && h is Ok && b is Ok) Ok(Profile(e.value, h.value, b.value)) else Err(errors)
}''', '''enum class Blood { A, B, AB, O }
data class Profile(val email: String, val heightCm: Int, val blood: Blood)

fun validEmail(s: String): Outcome<String, String> = if ("@" in s) Ok(s) else Err("Email is missing @")
fun validHeight(s: String): Outcome<String, Int> =
    s.toIntOrNull()?.takeIf { it in 50..250 }?.let { Ok(it) } ?: Err("Height must be a number of cm from 50 to 250")
fun validBlood(s: String): Outcome<String, Blood> =
    Blood.entries.firstOrNull { it.name == s }?.let { Ok(it) } ?: Err("Blood type must be A, B, AB or O")

fun update(email: String, height: String, blood: String): Outcome<List<String>, Profile> {
    val e = validEmail(email); val h = validHeight(height); val b = validBlood(blood)
    val errors = listOf(e, h, b).mapNotNull { it.errorOrNull() }
    return if (e is Ok && h is Ok && b is Ok) Ok(Profile(e.value, h.value, b.value)) else Err(errors)
}''')

    S_ = 'recall'
    a(C + '.sec.%s.title' % S_, '''Tự trả lời''', '''Answer it yourself''')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'ask', '''Khi nào gom lỗi, khi nào dừng ở lỗi đầu tiên?''', '''When do you collect errors, and when do you stop at the first one?''')
    B(C, S_, 1, 'ans', '''Các bước độc lập (như các ô của form) thì kiểm hết rồi gom lỗi. Bước cần kết quả của bước trước thì nối bằng flatMap và dừng ở lỗi đầu tiên.''',
      '''Independent steps (like form fields): check them all and collect the errors. A step that needs the previous result: chain it with flatMap and stop at the first error.''')
    B(C, S_, 2, 'ask', '''Monoid gồm những gì?''', '''What makes a monoid?''')
    B(C, S_, 2, 'ans', '''Một kiểu, một phép gộp hai giá trị có tính kết hợp, và một phần tử đơn vị (gộp với nó không đổi gì), ví dụ nối list với [].''',
      '''A type, an associative operation combining two values, and an identity element (combining with it changes nothing), for example joining lists with [].''')

    for q, qv, qe, av, ae, wv, we in [
        ('q1', 'flatMap có gom được lỗi của hai bước không?', 'Can flatMap collect the errors of two steps?', 'Không.', 'No.',
         'Bước sau chỉ chạy khi bước trước thành công, nên có tối đa một lỗi.', 'The later step only runs when the earlier one succeeds, so there is at most one error.'),
        ('q2', 'Phần tử đơn vị của phép nối chuỗi là gì?', 'What is the identity element of string concatenation?', 'Chuỗi rỗng "".', 'The empty string "".',
         '"" + s và s + "" đều bằng s.', '"" + s and s + "" both equal s.'),
        ('q3', 'NonEmptyList với phép nối là monoid hay chỉ là semigroup?', 'Is NonEmptyList with concatenation a monoid or only a semigroup?', 'Chỉ là semigroup.', 'Only a semigroup.',
         'Không có NonEmptyList rỗng để làm phần tử đơn vị.', 'There is no empty NonEmptyList to serve as the identity element.'),
        ('q4', 'Kiểm "số điện thoại đã đăng ký chưa" có nên gom chung với kiểm định dạng số không?', 'Should "is the phone number already registered" be collected together with the format check?', 'Không, nó nối sau bằng flatMap.', 'No, it is chained afterwards with flatMap.',
         'Nó cần một số đã hợp lệ, tức phụ thuộc vào bước kiểm định dạng.', 'It needs an already valid number, so it depends on the format check.')]:
        a(C + '.quiz.%s.q' % q, qv, qe); a(C + '.quiz.%s.a' % q, av, ae); a(C + '.quiz.%s.why' % q, wv, we)
