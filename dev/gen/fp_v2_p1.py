# Lập trình hàm · K1 (p1): hàm thuần và referential transparency (Phần 1: nền tảng)
# Nguồn: Massimo Carli, Functional Programming in Kotlin by Tutorials ch.3 (Pure functions, Referential transparency and the substitution model,
# Exercise 3.1, 3.2); Vermeulen, Bjarnason, Chiusano, Functional Programming in Kotlin ch.1 (1.1 quán cà phê, 1.2, 1.3);
# Mark Seemann, Code That Fits in Your Head 13.1.3, 8.2.2. Đọc 2026-11-24, diễn đạt lại; ví dụ viết lại theo app Hẹn Khám.

SEC_ORDER = {'p1': ['hook', 'pure', 'rt', 'effects', 'edge', 'bugs', 'ex', 'honest']}


def add(a):
    def B(ch, sec, n, field, vi, en=None):
        a('%s.sec.%s.b.%02d.%s' % (ch, sec, n, field), vi, vi if en is None else en)

    a('preset.pure', 'Lập trình hàm · hàm thuần và mô hình thay thế', 'Functional programming · pure functions and the substitution model')
    m = lambda k, vi, en=None: a('m.pure.' + k, vi, en)
    m('title', 'fee() đọc ngày hiện tại, hay fee(date) nhận ngày', 'fee() reading today\'s date, or fee(date) taking the date')
    m('overview', 'Hàm tính phí khám của app Hẹn Khám: ngày thường 200.000 đ, thứ Bảy và Chủ nhật 300.000 đ. Cách thứ nhất: fee() tự đọc ngày hiện tại và đếm lượt gọi. Cách thứ hai: fee(date) nhận ngày làm tham số. Với mỗi cách, thay từng biểu thức bằng giá trị của nó (mô hình thay thế), rồi chạy cùng một test vào các ngày trong tuần 23–29/11/2026.',
      'The ClinicBook visit fee: 200,000 VND on weekdays, 300,000 VND on Saturday and Sunday. First version: fee() reads today\'s date itself and counts its calls. Second version: fee(date) takes the date as a parameter. For each, replace every expression with its value (the substitution model), then run the same test on each day of the week of 23–29 November 2026.')
    m('wrapup', 'fee() đọc ngày hiện tại và tăng một biến đếm. Bảng thế dừng ngay từ đầu: cùng một biểu thức có hai giá trị, và tách biến làm biến đếm đổi. Test xanh thứ Hai, đỏ thứ Bảy và Chủ nhật dù không ai sửa mã. fee(date) nhận ngày làm tham số: mọi hàng thay được, rút gọn tới 600_000; test truyền ngày cố định nên xanh mọi ngày. Đồng hồ và biến đếm vẫn còn, nhưng nằm ở lớp gọi, nơi ai cũng thấy chúng.',
      'fee() reads today\'s date and bumps a counter. The substitution table stops at once: the same expression has two values, and extracting a variable changes the counter. The test is green on Monday and red on Saturday and Sunday though nobody touched the code. fee(date) takes the date as a parameter: every row substitutes, reducing to 600_000; the tests pass fixed dates, so they are green every day. The clock and the counter are still there, but in the calling layer, where everyone can see them.')
    m('simp.1', 'Phí chỉ có hai mức và không có ngày lễ; tuần 23–29/11/2026 là lịch thật, số tiền là của site. Bảng thế chỉ ghi những lần thay liên quan; các bước rút gọn hằng như SATURDAY == SATURDAY được gộp lại.',
      'The fee has only two levels and no public holidays; the week of 23–29 November 2026 is the real calendar, the amounts are the site\'s. The substitution table records only the relevant substitutions; constant reductions such as SATURDAY == SATURDAY are merged.')
    m('simp.2', 'Có hai cách phát biểu hàm thuần: theo hai điều kiện (cùng đầu vào cùng đầu ra; không tác động ra ngoài), hay theo referential transparency (thay được bằng kết quả). Hai cách nói cùng một ý; cũng là một hàm đọc dữ liệu tất định và không side effect.',
      'There are two ways to state purity: by two conditions (same input, same output; no effect outside), or by referential transparency (replaceable by its result). Both say the same thing; it is also a data-reading function that is deterministic and free of side effects.')
    m('ctl.hint', 'Đổi cách viết rồi đi lại; so bảng thế (hàng đỏ là chỗ không thay được) và hàng test theo ngày.', 'Switch the version and walk again; compare the substitution table (red rows cannot be substituted) and the test row by day.')
    m('ctl.case', 'Cách viết', 'Version')
    for k, vi, en in [('impure', 'fee() đọc ngày hiện tại', 'fee() reads today\'s date'), ('pure', 'fee(date) nhận ngày', 'fee(date) takes the date')]:
        m('ctl.case.' + k, vi, en)
    m('diagramTitle', 'Thế giới bên ngoài, lời gọi, giá trị, test', 'The outside world, the call, the value, the test')
    m('diagramDesc', 'Kết quả của lời gọi phụ thuộc vào đâu, và test thấy gì', 'What the call\'s result depends on, and what the test sees')
    for k, vi, en in [('world', 'Đồng hồ và biến đếm', 'Clock and counter'), ('call', 'Lời gọi fee', 'The fee call'), ('value', 'Giá trị', 'Value'), ('test', 'Bộ test', 'Tests')]:
        m('n.' + k, vi, en)
    m('met.subst', 'Hàng thay được', 'Substitutable rows'); m('met.opaque', 'Hàng không thay được', 'Rows that cannot be substituted'); m('met.red', 'Ngày test đỏ', 'Days with a red test')
    a('cap.pure', 'Đồng hồ và biến đếm đi vào lời gọi; lời gọi cho ra giá trị; test kiểm giá trị. Nút đỏ: nơi kết quả phụ thuộc vào thứ không phải đầu vào.',
      'The clock and the counter feed the call; the call yields a value; the test checks the value. A red node is where the result depends on something other than the input.')
    S = [
        ('impure', 's1', 'Thay fee() bằng giá trị của nó', 'Replace fee() with its value',
         'Chương trình: total = fee() + fee(). Thử thay fee() bằng kết quả: chạy thứ Hai 23/11 thì được 200_000, chạy thứ Bảy 28/11 thì được 300_000. Một biểu thức, hai giá trị: không có giá trị nào để thay. fee() không referentially transparent.',
         'The program: total = fee() + fee(). Try replacing fee() with its result: run on Monday 23 November it gives 200_000, run on Saturday 28 November it gives 300_000. One expression, two values: there is no value to substitute. fee() is not referentially transparent.'),
        ('impure', 's2', 'Tách biến: val a = fee(); total = a + a', 'Extract a variable: val a = fee(); total = a + a',
         'Với hàm thuần, hai cách viết là một. Ở đây fee() còn tăng calls: viết fee() + fee() thì calls tăng 2, tách biến thì tăng 1. Số lượt tính phí trong thống kê đổi chỉ vì một refactor nhỏ.',
         'For a pure function the two forms are the same. Here fee() also bumps calls: fee() + fee() adds 2, the extracted variable adds 1. The fee lookup count in the analytics changes because of a tiny refactoring.'),
        ('impure', 's3', 'Chạy test thứ Hai: xanh', 'Run the test on Monday: green',
         'weekdayFee kiểm fee() == 200_000. Chạy trên máy dev hôm thứ Hai 23/11: xanh. Test không nói nó đang kiểm ngày nào; ngày nằm trong đồng hồ của máy chạy test.',
         'weekdayFee checks fee() == 200_000. Run on the dev machine on Monday 23 November: green. The test does not say which day it checks; the day lives in the clock of the machine running it.'),
        ('impure', 's4', 'CI chạy thứ Bảy 28/11: đỏ', 'CI runs on Saturday 28 November: red',
         'Bản build đêm thứ Bảy chạy lại cùng test, không ai sửa dòng mã nào: fee() trả 300_000, test đỏ. Chạy cả tuần thì đỏ đúng hai ngày, thứ Bảy và Chủ nhật. Test lúc xanh lúc đỏ theo lịch.',
         'Saturday\'s nightly build reruns the same test with no line changed: fee() returns 300_000 and the test is red. Run all week, it is red on exactly two days, Saturday and Sunday. The test flips with the calendar.'),
        ('pure', 's1', 'Thay d bằng giá trị của nó', 'Replace d with its value',
         'fee nhận ngày làm tham số. d là LocalDate.of(2026, 11, 28), một thứ Bảy; thay d vào: total = fee(2026-11-28) + fee(2026-11-28). Ngoài tham số, không có gì quyết định kết quả.',
         'fee takes the date as a parameter. d is LocalDate.of(2026, 11, 28), a Saturday; substitute d: total = fee(2026-11-28) + fee(2026-11-28). Nothing but the parameter decides the result.'),
        ('pure', 's2', 'Thay thân hàm, rút gọn tới một giá trị', 'Substitute the body, reduce to one value',
         'Thay mỗi lời gọi bằng thân hàm: 28/11 là thứ Bảy nên điều kiện là true, mỗi lời gọi thành 300_000, total thành 600_000. Tách biến val a = fee(d); a + a cũng ra 600_000: hai cách viết là một chương trình.',
         'Replace each call with the function body: 28 November is a Saturday, so the condition is true, each call becomes 300_000 and total becomes 600_000. Extracting val a = fee(d); a + a also gives 600_000: the two forms are one program.'),
        ('pure', 's3', 'Test với ngày cố định: xanh', 'Tests with fixed dates: green',
         'Hai test truyền ngày vào: thứ Hai 23/11 cho 200_000, thứ Bảy 28/11 cho 300_000. Chạy thứ Hai: xanh. Giờ có test cho cả ngày cuối tuần, điều test cũ không làm được.',
         'Two tests pass the date in: Monday 23 November gives 200_000, Saturday 28 November gives 300_000. Run on Monday: green. There is now a test for the weekend too, which the old test could not have.'),
        ('pure', 's4', 'Vỏ đọc đồng hồ; test xanh mọi ngày', 'The shell reads the clock; tests are green every day',
         'Đọc LocalDate.now(clock) và đếm lượt cho analytics chuyển ra lớp gọi fee, ở rìa của app. Chạy test cả tuần: không ngày nào đỏ, vì test không còn đọc đồng hồ. Side effect không biến mất; nó chỉ dời ra ngoài (chương K9).',
         'Reading LocalDate.now(clock) and counting for analytics move to the layer that calls fee, at the edge of the app. Run the tests all week: no red day, because the tests no longer read the clock. The side effects do not vanish; they just move outwards (chapter K9).'),
    ]
    for case, k, tv, te, xv, xe in S:
        sid = case + '.' + k
        m('s.%s.title' % sid, tv, te); m('s.%s.explain' % sid, xv, xe); m('ev.' + sid, tv, te)
    for k, vi, en in [
        ('try', 'Theo dõi bảng thế: hàng đỏ là chỗ thay biểu thức bằng giá trị làm đổi chương trình.', 'Watch the substitution table: a red row is where replacing an expression with its value changes the program.'),
        ('impure.s2', 'Một hàm trả đúng giá trị mong muốn nhưng còn làm thêm việc khác (in log, tăng biến đếm) thì không thuần: thay lời gọi bằng kết quả là mất việc làm thêm đó, nên chương trình đổi. [[src:book-fp-tut]]',
         'A function that returns the right value but also does something else (logs, bumps a counter) is not pure: replacing the call with its result loses that extra work, so the program changes. [[src:book-fp-tut]]'),
        ('impure.s3', 'Một hàm chỉ đọc dữ liệu mà muốn thuần thì còn phải tất định: không dựa vào số ngẫu nhiên, ID sinh ngẫu nhiên, giờ trong ngày hay ngày trong tháng. [[src:book-seemann]]',
         'A function that only reads data must also be deterministic to be pure: no random numbers, randomly generated IDs, time of day or day of the month. [[src:book-seemann]]'),
        ('impure.s4', 'Test phụ thuộc ngày chạy là test không tất định: cùng mã, kết quả khác. Cách sửa không phải chạy lại cho tới khi xanh, mà là đưa đồng hồ ra khỏi hàm cần kiểm.',
         'A test that depends on the day it runs is not deterministic: the same code, different results. The fix is not rerunning until green but moving the clock out of the function under test.'),
        ('pure.s1', 'Định nghĩa: một biểu thức referentially transparent nếu ở mọi chương trình, thay nó bằng kết quả của nó không đổi nghĩa chương trình. Hàm thuần khi mọi lời gọi của nó đều như vậy. [[src:book-fp-manning]]',
         'Definition: an expression is referentially transparent if, in every program, replacing it with its result leaves the meaning unchanged. A function is pure when every call to it is like that. [[src:book-fp-manning]]'),
        ('pure.s2', 'Khi mọi biểu thức đều thay được, ta suy luận về mã như giải phương trình: thay bằng thứ tương đương cho tới khi còn một giá trị. Cách suy luận này gọi là mô hình thay thế. [[src:book-fp-manning]]',
         'When every expression is substitutable, we reason about code like solving an equation: replace equals with equals until one value remains. This way of reasoning is called the substitution model. [[src:book-fp-manning]]'),
        ('pure.s3', 'Lời gọi hàm thuần thay được bằng kết quả; khi nó đã trả về, chỉ kết quả là thứ cần giữ trong đầu, cách nó tính ra thì không. [[src:book-seemann]]',
         'A pure function call can be replaced by its result; once it returns, only the result needs to stay in your head, not how it was computed. [[src:book-seemann]]'),
        ('pure.s4', 'Cách tổ chức này hay được gọi là lõi thuần, vỏ mỏng: phần quyết định nhận mọi thứ qua tham số, còn lớp ngoài cùng mới đọc đồng hồ, ghi log, gọi mạng. [[src:book-seemann]] [[src:book-fp-manning]]',
         'This layout is often called a pure core with a thin shell: the decisions receive everything through parameters, and only the outermost layer reads the clock, logs or calls the network. [[src:book-seemann]] [[src:book-fp-manning]]'),
    ]:
        m('co.' + k, vi, en)

    z = lambda k, vi, en=None: a('vz.' + k, vi, en)
    z('tab.pure', 'Bảng thế từng bước', 'Substitution table')
    z('pure.cap', 'Mỗi hàng là chương trình sau một lần thay biểu thức bằng giá trị của nó. Hàng đỏ: phép thay làm đổi chương trình. Viền: hàng mới ở bước này.', 'Each row is the program after one expression is replaced with its value. A red row: the substitution changes the program. Outlined: rows new in this step.')
    z('pure.tcap', 'Chạy cùng bộ test vào từng ngày của tuần 23–29/11/2026. "?": chưa chạy ngày đó.', 'Running the same tests on each day of the week of 23–29 November 2026. "?": not run on that day yet.')
    z('pure.legend', 'Ô gạch đỏ: không thay được, hay test đỏ. Chữ đậm: thay được, hay test xanh. Ô "?" mở theo bước.', 'Red hatched: cannot be substituted, or a red test. Bold: substitutable, or a green test. "?" cells open step by step.')
    for k, vi, en in [('n', 'Lần thay', 'Rewrite'), ('expr', 'Chương trình sau khi thay', 'Program after substitution'), ('st', 'Thay được?', 'Substitutable?'), ('why', 'Vì sao', 'Why'), ('run', 'Bộ test', 'Test suite')]:
        z('pure.col.' + k, vi, en)
    for k, vi, en in [('start', 'ban đầu', 'start'), ('ok', 'thay được', 'yes'), ('bad', 'không thay được', 'no')]:
        z('pure.st.' + k, vi, en)
    for k, vi, en in [
        ('start', 'chương trình gốc', 'the original program'),
        ('runMon', 'nếu chạy thứ Hai 23/11; chạy ngày khác có thể ra số khác', 'if run on Monday 23 November; another day may give another number'),
        ('runSat', 'nếu chạy thứ Bảy 28/11: cùng biểu thức, giá trị khác, nên không có giá trị nào để thay', 'if run on Saturday 28 November: the same expression, another value, so there is no value to substitute'),
        ('calls', 'calls tăng 1 thay vì 2: tách biến đã đổi chương trình', 'calls goes up by 1 instead of 2: extracting the variable changed the program'),
        ('valD', 'thay d bằng giá trị của nó', 'replace d with its value'),
        ('body', 'thay lời gọi bằng thân hàm; 28/11 là thứ Bảy nên điều kiện là true', 'replace each call with the body; 28 November is a Saturday, so the condition is true'),
        ('eval', 'rút gọn if', 'reduce the if'),
        ('sum', 'cộng hai số', 'add the two numbers'),
        ('same', 'tách biến cũng ra 600_000: cùng một chương trình', 'extracting the variable also gives 600_000: the same program')]:
        z('pure.why.' + k, vi, en)
    for k, vi, en in [('mon', 'T2 {d}', 'Mon {d}'), ('tue', 'T3 {d}', 'Tue {d}'), ('wed', 'T4 {d}', 'Wed {d}'), ('thu', 'T5 {d}', 'Thu {d}'), ('fri', 'T6 {d}', 'Fri {d}'), ('sat', 'T7 {d}', 'Sat {d}'), ('sun', 'CN {d}', 'Sun {d}')]:
        z('pure.day.' + k, vi, en)
    z('pure.test.impure', 'weekdayFee với fee()', 'weekdayFee with fee()')
    z('pure.test.pure', 'weekdayFee, weekendFee với ngày cố định', 'weekdayFee, weekendFee with fixed dates')
    z('pure.pass', 'xanh', 'green'); z('pure.fail', 'đỏ', 'red')

    C = 'p1'
    a(C + '.title', 'Hàm thuần và referential transparency', 'Pure functions and referential transparency')
    a(C + '.essence', 'Hàm thuần: cùng đầu vào luôn cho cùng đầu ra, và lời gọi không làm gì khác mà người ngoài thấy được.\nReferential transparency: thay lời gọi bằng kết quả mà chương trình không đổi. Khi đó tách biến, gộp biến hay bỏ một lời gọi thừa đều an toàn.\nHàm đọc đồng hồ, số ngẫu nhiên hay biến toàn cục thì không thuần, và test của nó phụ thuộc lúc chạy. Cách sửa: biến thứ hàm đọc ngầm thành tham số, và đọc nó ở rìa.',
      'A pure function: the same input always gives the same output, and a call does nothing else an outsider can see.\nReferential transparency: replacing a call with its result leaves the program unchanged. Then extracting a variable, inlining one or dropping a redundant call are all safe.\nA function that reads the clock, random numbers or a global variable is not pure, and its tests depend on when they run. The fix: turn what the function reads silently into a parameter, and read it at the edge.')
    a(C + '.goal.g1', 'Đã thấy biểu thức không thay được', 'Saw an expression that cannot be substituted')
    a(C + '.goal.g2', 'Đã thấy test theo ngày chạy', 'Saw the tests by the day they run')
    a(C + '.sim.fp.pure', 'hàm đọc ngày hiện tại hay hàm nhận ngày', 'a function reading today\'s date or one taking the date')

    S_ = 'hook'
    a(C + '.sec.%s.title' % S_, 'Đoán trước khi đọc', 'Predict before reading')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'predict', 'Test weekdayFee kiểm fee() == 200_000 và xanh suốt tuần trên máy bạn. Đêm thứ Bảy, CI chạy lại đúng commit đó và báo đỏ. Không ai sửa mã. Bạn nghi điều gì?',
      'The weekdayFee test checks fee() == 200_000 and is green all week on your machine. On Saturday night, CI reruns the very same commit and reports red. Nobody changed the code. What do you suspect?')
    B(C, S_, 1, 'ans', 'fee() tự đọc LocalDate.now(). Kết quả của nó không chỉ phụ thuộc đầu vào mà còn phụ thuộc lúc chạy, nên cùng một mã cho test xanh ngày thường và đỏ cuối tuần. Hàm không thuần, và test của nó cũng mất tính tất định theo.',
      'fee() reads LocalDate.now() itself. Its result depends not only on its input but on when it runs, so the same code makes the test green on weekdays and red at the weekend. The function is not pure, and its test loses determinism with it.')

    S_ = 'pure'
    a(C + '.sec.%s.title' % S_, 'Hàm thuần: hai điều kiện', 'Pure functions: two conditions')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'p', 'Hàm f thuần khi thỏa hai điều kiện: (1) cùng đầu vào luôn cho cùng đầu ra; (2) ngoài việc trả kết quả, f không làm gì mà bên ngoài thấy được. fun double(x: Int) = x * 2 thuần. Một bản in thêm một dòng log rồi trả x * 2 thì không: kết quả đúng, nhưng thế giới đã có thêm dòng log. fun plusRandom(a: Int) = a + Random.nextInt() vi phạm cả hai: kết quả khác mỗi lần, và bộ sinh số ngẫu nhiên đổi trạng thái sau mỗi lần gọi. [[src:book-fp-tut]]',
      'A function f is pure when it meets two conditions: (1) the same input always gives the same output; (2) besides returning its result, f does nothing visible from outside. fun double(x: Int) = x * 2 is pure. A version that logs a line and then returns x * 2 is not: the result is right, but the world now has an extra log line. fun plusRandom(a: Int) = a + Random.nextInt() breaks both: a different result each time, and the random generator changes state with every call. [[src:book-fp-tut]]')
    B(C, S_, 2, 'p', 'Nhìn từ phía khác: command query separation (chương J2) nói hàm đọc dữ liệu (query) không được có side effect. Seemann thêm một luật: query còn phải tất định, không dựa vào số ngẫu nhiên, ID sinh ngẫu nhiên, giờ trong ngày, ngày trong tháng, hay nội dung tệp và database. Hàm tất định và không side effect chính là hàm thuần. [[src:book-seemann]]',
      'From another side: command query separation (chapter J2) says a function that reads data (a query) must have no side effects. Seemann adds one rule: a query must also be deterministic, relying on no random numbers, randomly generated IDs, time of day, day of the month, or the contents of files and databases. A deterministic function without side effects is exactly a pure function. [[src:book-seemann]]')
    B(C, S_, 3, 'note', 'Sửa một biến cục bộ trong thân hàm vẫn được, miễn không ai bên ngoài nhìn thấy biến đó. Thuần là chuyện người gọi quan sát được gì, không phải trong thân hàm có var hay không. [[src:book-fp-manning]]',
      'Changing a local variable inside the function body is fine, as long as nothing outside can see it. Purity is about what the caller can observe, not whether the body has a var. [[src:book-fp-manning]]')
    B(C, S_, 3, 'kind', 'source')

    S_ = 'rt'
    a(C + '.sec.%s.title' % S_, 'Referential transparency và mô hình thay thế', 'Referential transparency and the substitution model')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'p', 'Một biểu thức referentially transparent nếu ở mọi chương trình, thay nó bằng kết quả của nó không đổi nghĩa chương trình: 2 + 3 thay được bằng 5. Hàm f thuần khi lời gọi f(x) có tính chất này, với mọi đối số x cũng có tính chất này. [[src:book-fp-manning]]',
      'An expression is referentially transparent if, in every program, replacing it with its result leaves the program\'s meaning unchanged: 2 + 3 can be replaced by 5. A function f is pure when the call f(x) has this property, for every argument x that has it too. [[src:book-fp-manning]]')
    B(C, S_, 2, 'p', 'Cách kiểm: viết chương trình hai lần, một lần gọi biểu thức ở từng chỗ dùng, một lần tính một lần rồi dùng lại, rồi so. Với { 3 * 10 } hai cách như nhau. Với một hàm chỉ in một dòng chào, cả hai cách đều trả Unit, nhưng cách thứ nhất in hai dòng, cách thứ hai in một (đoạn mã dưới đây). So giá trị trả về thôi là chưa đủ; phải so cả chương trình. [[src:book-fp-tut]]',
      'How to check: write the program twice, once calling the expression at each use, once evaluating it once and reusing the value, then compare. With { 3 * 10 } both ways agree. With a function that only prints a greeting, both ways return Unit, but the first prints two lines and the second one (code below). Comparing return values is not enough; you compare the whole program. [[src:book-fp-tut]]')
    B(C, S_, 3, 'kt', 'fun greet() = println("Xin chào")\n\nval (c1, c2) = greet() to greet()   // in hai dòng\nval g = greet()\nval (d1, d2) = g to g               // in một dòng\n// c1 == d1 và c2 == d2 (đều là Unit), nhưng hai chương trình khác nhau',
      'fun greet() = println("Hello")\n\nval (c1, c2) = greet() to greet()   // prints two lines\nval g = greet()\nval (d1, d2) = g to g               // prints one line\n// c1 == d1 and c2 == d2 (both Unit), yet the two programs differ')
    B(C, S_, 4, 'p', 'Khi mọi biểu thức thay được, suy luận về mã giống giải phương trình: thay bằng thứ tương đương cho tới khi còn một giá trị. Cách này gọi là mô hình thay thế (substitution model). Bảng thế trong mô phỏng làm đúng việc ấy; hàng đỏ là chỗ phép thay làm đổi chương trình. [[src:book-fp-manning]]',
      'When every expression is substitutable, reasoning about code is like solving an equation: replace equals with equals until one value remains. This is called the substitution model. The simulation\'s substitution table does exactly that; a red row is where substituting changes the program. [[src:book-fp-manning]]')

    S_ = 'effects'
    a(C + '.sec.%s.title' % S_, 'Side effect trông thế nào trong mã Android', 'What side effects look like in Android code')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'p', 'Đọc từ thế giới bên ngoài: LocalDate.now(), System.currentTimeMillis(), Random, UUID.randomUUID(), SharedPreferences, database, mạng. Ghi ra thế giới: Log.d, println, sửa biến toàn cục hay field của một object dùng chung, ghi database, gửi request, phát sự kiện analytics. Ném ngoại lệ cũng tính là side effect, vì chữ ký hàm không nói gì về nó (chương K5). [[src:book-fp-tut]]',
      'Reading from the outside world: LocalDate.now(), System.currentTimeMillis(), Random, UUID.randomUUID(), SharedPreferences, a database, the network. Writing to the world: Log.d, println, changing a global variable or a field of a shared object, writing to a database, sending a request, emitting an analytics event. Throwing counts as a side effect too, because the function signature says nothing about it (chapter K5). [[src:book-fp-tut]]')
    B(C, S_, 2, 'p', 'Không phải mã nào cũng phải thuần: app tồn tại để có side effect, như hiện màn hình, lưu lịch hẹn, gửi nhắc. Tới lúc nào đó chương trình phải thật sự tác động lên thế giới. Mục tiêu là biết rõ chỗ nào có side effect, và gom chúng lại để phần quyết định nghiệp vụ còn lại thuần. [[src:book-fp-manning]]',
      'Not all code must be pure: an app exists to have side effects, such as drawing screens, saving bookings, sending reminders. At some point a program must actually affect the world. The goal is to know where the side effects are, and gather them so the business decisions left over are pure. [[src:book-fp-manning]]')

    S_ = 'edge'
    a(C + '.sec.%s.title' % S_, 'Cách sửa: đưa thứ đọc ngầm thành tham số', 'The fix: turn hidden reads into parameters')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'p', 'Cách sửa đơn giản nhất cho fee(): biến thứ nó đọc ngầm thành tham số. fee(date) không còn biết hôm nay là ngày nào; nơi gọi quyết định. Hàm nhận "bây giờ" làm tham số, còn lớp gọi (ViewModel) mới đọc đồng hồ thật. [[src:book-seemann]]',
      'The simplest fix for fee(): turn what it reads silently into a parameter. fee(date) no longer knows what day it is; the caller decides. The function takes "now" as a parameter, and only the calling layer (the ViewModel) reads the real clock. [[src:book-seemann]]')
    B(C, S_, 2, 'kt', 'class BookingViewModel(private val clock: Clock) : ViewModel() {\n    fun onOpen() {\n        val today = LocalDate.now(clock)          // side effect ở rìa\n        _state.value = FeeUi(fee(today))          // quyết định thuần\n    }\n}\n// test phần quyết định: gọi thẳng fee(LocalDate.of(2026, 11, 28))',
      'class BookingViewModel(private val clock: Clock) : ViewModel() {\n    fun onOpen() {\n        val today = LocalDate.now(clock)          // the side effect, at the edge\n        _state.value = FeeUi(fee(today))          // the pure decision\n    }\n}\n// test the decision directly: fee(LocalDate.of(2026, 11, 28))')
    B(C, S_, 3, 'p', 'Cùng cách đó dùng được cho việc ghi: thay vì để hàm đặt lịch tự gọi cổng thanh toán, cho nó trả về một giá trị "khoản cần thu" (số tiền, thẻ), rồi lớp ngoài mới gửi đi. Test chỉ cần so giá trị trả về, không cần giả lập cổng thanh toán. Lõi thuần, vỏ mỏng xử lý hiệu ứng: chương K9 đi sâu vào ý này. [[src:book-fp-manning]]',
      'The same move works for writes: instead of letting the booking function call the payment gateway itself, have it return a "charge" value (amount, card), and let the outer layer send it. Tests only compare the returned value, with no fake payment gateway. A pure core with a thin shell handling effects: chapter K9 goes deeper. [[src:book-fp-manning]]')

    S_ = 'bugs'
    a(C + '.sec.%s.title' % S_, 'Hai lỗi hay gặp', 'Two common bugs')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'bug', 'Test phí lúc xanh lúc đỏ, và đỏ đúng vào cuối tuần.', 'A fee test is sometimes green, sometimes red, and red exactly at the weekend.')
    B(C, S_, 1, 'cause', 'Hàm cần kiểm tự đọc LocalDate.now(); kết quả phụ thuộc ngày chạy test, không chỉ đầu vào.', 'The function under test reads LocalDate.now() itself; its result depends on the day the test runs, not only on its input.')
    B(C, S_, 1, 'fix', 'Truyền ngày vào làm tham số và đọc đồng hồ ở lớp gọi. Viết một test cho mỗi loại ngày bằng ngày cố định.', 'Pass the date in as a parameter and read the clock in the calling layer. Write one test per kind of day, with fixed dates.')
    B(C, S_, 2, 'bug', 'Đặt lịch khi mạng chập chờn tạo ra hai lịch hẹn, ngay sau một refactor "chỉ gộp biến cho gọn".', 'Booking on a flaky network creates two appointments, right after a refactoring that "only inlined a variable".')
    B(C, S_, 2, 'cause', 'Trước đó, val key = UUID.randomUUID().toString() nằm ngoài vòng thử lại. Người refactor gộp biến vào chỗ dùng, nên lời gọi UUID.randomUUID() vào trong vòng lặp: mỗi lần thử có một khóa mới, server không nhận ra là cùng một yêu cầu. UUID.randomUUID() không referentially transparent, nên gộp biến đã đổi chương trình.',
      'Before, val key = UUID.randomUUID().toString() sat outside the retry loop. The refactoring inlined the variable, moving the UUID.randomUUID() call into the loop: each attempt gets a new key, and the server cannot tell it is the same request. UUID.randomUUID() is not referentially transparent, so inlining changed the program.')
    B(C, S_, 2, 'fix', 'Chỉ gộp hay tách biến với biểu thức thuần. Tạo khóa một lần, đặt tên, truyền vào; thêm test "thử lại dùng cùng khóa". Khóa chống trùng được giải thích ở track Thiết kế hệ thống phía mobile, chương I5.',
      'Only inline or extract pure expressions. Create the key once, name it, pass it in; add a "retries reuse the same key" test. Idempotency keys are explained in the Mobile System Design track, chapter I5.')

    S_ = 'ex'
    a(C + '.sec.%s.title' % S_, 'Bài tập', 'Exercise')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'ex', 'Trong bốn hàm dưới đây, hàm nào thuần? Viết lại các hàm còn lại để phần quyết định thành thuần.',
      'Which of the four functions below are pure? Rewrite the others so the decision part becomes pure.')
    B(C, S_, 1, 'exkt', 'var lastTicket = 0\nfun ticket(): Int = ++lastTicket\nfun discount(fee: Long, member: Boolean): Long = if (member) fee * 9 / 10 else fee\nfun isPast(slot: LocalDateTime): Boolean = slot.isBefore(LocalDateTime.now())\nfun feeAndLog(fee: Long): Long { Log.d("fee", "$fee"); return fee }')
    B(C, S_, 1, 'hint', 'Với mỗi hàm, hỏi hai câu của định nghĩa: cùng đầu vào có luôn cho cùng đầu ra không? Gọi thêm một lần có làm gì người khác thấy được không?', 'For each function, ask the definition\'s two questions: does the same input always give the same output? Does one extra call do anything someone else can see?')
    B(C, S_, 1, 'sol', 'Chỉ discount thuần. ticket sửa biến bên ngoài và trả số khác mỗi lần. isPast đọc đồng hồ: đưa now thành tham số. feeAndLog trả đúng fee nhưng ghi log: chuyển việc ghi log ra nơi gọi. Muốn phần đánh số thuần thì hàm nhận số hiện tại và trả số kế tiếp; lưu số kế tiếp là việc của nơi gọi.',
      'Only discount is pure. ticket changes an outside variable and returns a different number each time. isPast reads the clock: make now a parameter. feeAndLog returns fee unchanged but logs: move the logging to the caller. To make numbering pure, take the current number and return the next one; storing it is the caller\'s job.')
    B(C, S_, 1, 'solkt', 'fun nextTicket(current: Int): Int = current + 1\nfun discount(fee: Long, member: Boolean): Long = if (member) fee * 9 / 10 else fee\nfun isPast(slot: LocalDateTime, now: LocalDateTime): Boolean = slot.isBefore(now)\n// nơi gọi: val f = fee(today); Log.d("fee", "$f")',
      'fun nextTicket(current: Int): Int = current + 1\nfun discount(fee: Long, member: Boolean): Long = if (member) fee * 9 / 10 else fee\nfun isPast(slot: LocalDateTime, now: LocalDateTime): Boolean = slot.isBefore(now)\n// the caller: val f = fee(today); Log.d("fee", "$f")')

    S_ = 'honest'
    a(C + '.sec.%s.title' % S_, 'Chương này giản lược những gì', 'What this chapter simplifies')
    a(C + '.sec.%s.badge' % S_, 'simplified')
    B(C, S_, 1, 'p', 'Định nghĩa hàm thuần, các ví dụ hàm thuần và không thuần, cách so hai chương trình theo Massimo Carli, Functional Programming in Kotlin by Tutorials ch.3; định nghĩa referential transparency, mô hình thay thế và ý trả về khoản cần thu thay vì gọi cổng thanh toán theo Vermeulen, Bjarnason, Chiusano, Functional Programming in Kotlin ch.1; luật query tất định và việc truyền "bây giờ" làm tham số theo Seemann 13.1.3 và 8.2.2; ý bài tập theo Exercise 3.1, 3.2 của Carli. Hàm phí chỉ có hai mức, không có ngày lễ (chương J4 có ngày lễ). Biến calls là một side effect nhỏ để thấy được; trong app thật, đọc đồng hồ, ghi log và gửi analytics là những side effect hay gặp nhất.',
      'The definition of a pure function, the pure and impure examples and the way of comparing two programs follow Massimo Carli, Functional Programming in Kotlin by Tutorials ch.3; the definition of referential transparency, the substitution model and returning a charge instead of calling the payment gateway follow Vermeulen, Bjarnason, Chiusano, Functional Programming in Kotlin ch.1; the deterministic-query rule and passing "now" as a parameter follow Seemann 13.1.3 and 8.2.2; the exercise idea follows Carli\'s Exercises 3.1, 3.2. The fee has only two levels and no holidays (chapter J4 has holidays). The calls counter is a small side effect made visible; in real apps, reading the clock, logging and sending analytics are the most common side effects.')

    for q, qv, qe, av, ae, wv, we in [
        ('q1', 'Một biểu thức referentially transparent khi nào?', 'When is an expression referentially transparent?', 'Khi thay nó bằng giá trị của nó ở mọi chỗ dùng mà chương trình không đổi nghĩa.', 'When replacing it with its value wherever it is used leaves the program\'s meaning unchanged.', 'So cả chương trình, không chỉ giá trị trả về.', 'Compare the whole program, not only return values.'),
        ('q2', 'fun fee(): Long đọc LocalDate.now() và không sửa biến nào. Nó có thuần không?', 'fun fee(): Long reads LocalDate.now() and changes no variable. Is it pure?', 'Không.', 'No.', 'Nó không tất định: cùng đầu vào (không có gì) mà kết quả đổi theo ngày chạy.', 'It is not deterministic: the same input (none) gives a result that changes with the day it runs.'),
        ('q3', 'Hàm chỉ ghi một dòng log rồi trả đúng x * 2. Nó có thuần không?', 'A function only writes a log line and returns x * 2. Is it pure?', 'Không.', 'No.', 'Thay lời gọi bằng kết quả làm mất dòng log, nên chương trình đổi.', 'Replacing the call with its result loses the log line, so the program changes.'),
        ('q4', 'Sửa một biến var cục bộ trong thân hàm có làm hàm mất thuần không?', 'Does changing a local var inside a function body make it impure?', 'Không, nếu không ai bên ngoài quan sát được biến đó.', 'No, as long as nothing outside can observe that variable.', 'Thuần là chuyện người gọi thấy gì, không phải trong thân hàm có var hay không.', 'Purity is about what the caller sees, not whether the body has a var.')]:
        a(C + '.quiz.%s.q' % q, qv, qe); a(C + '.quiz.%s.a' % q, av, ae); a(C + '.quiz.%s.why' % q, wv, we)
