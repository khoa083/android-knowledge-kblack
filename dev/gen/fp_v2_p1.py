# Lập trình hàm · K1 (p1): hàm thuần và referential transparency (Phần 1: nền tảng)
# Nguồn (chỉ ghi ở đây, sources.js và docs/research/fp.md; văn bản cho người đọc tự giải thích, không dẫn chương sách):
# Carli, FP in Kotlin by Tutorials ch.3 (Exercise 3.1, 3.2); Vermeulen, Bjarnason, Chiusano, FP in Kotlin ch.1; Seemann 13.1.3, 8.2.2.
# Giọng văn: người dạy giảng cho người mới, câu ngắn, mỗi đoạn một ý, thuật ngữ giải thích bằng lời thường trước (quyết định 2026-11-24).

SEC_ORDER = {'p1': ['hook', 'pure', 'rt', 'effects', 'edge', 'bugs', 'ex']}


def add(a):
    def B(ch, sec, n, field, vi, en=None):
        a('%s.sec.%s.b.%02d.%s' % (ch, sec, n, field), vi, vi if en is None else en)

    a('preset.pure', 'Lập trình hàm · hàm thuần và mô hình thay thế', 'Functional programming · pure functions and the substitution model')
    m = lambda k, vi, en=None: a('m.pure.' + k, vi, en)
    m('title', 'fee() đọc ngày hiện tại, hay fee(date) nhận ngày', 'fee() reading today\'s date, or fee(date) taking the date')
    m('overview', 'Phòng khám tính phí 200.000 đ ngày thường và 300.000 đ thứ Bảy, Chủ nhật. Ta viết hàm tính phí theo hai cách. Cách 1: fee() tự xem hôm nay là ngày nào. Cách 2: fee(date) được người gọi cho biết ngày. Với mỗi cách, ta làm hai việc: thử thay lời gọi hàm bằng kết quả của nó, và chạy cùng một bài test vào từng ngày trong tuần 23–29/11/2026.',
      'The clinic charges 200,000 VND on weekdays and 300,000 VND on Saturday and Sunday. We write the fee function two ways. Way 1: fee() looks up today\'s date by itself. Way 2: fee(date) is told the date by its caller. For each, we do two things: try replacing the call with its result, and run the same test on each day of the week of 23–29 November 2026.')
    m('wrapup', 'Cách 1 có vấn đề ngay từ đầu: cùng một lời gọi fee() lúc ra 200.000, lúc ra 300.000, nên không thể thay nó bằng một con số. Bài test cũng vậy: xanh từ thứ Hai tới thứ Sáu, đỏ thứ Bảy và Chủ nhật, dù không ai sửa mã. Cách 2 thì mọi bước thay đều được, và bài test truyền ngày cố định nên xanh mọi ngày. Đồng hồ không biến mất; nó chỉ chuyển ra chỗ gọi hàm, nơi ai cũng nhìn thấy.',
      'Way 1 is in trouble from the start: the same call fee() gives 200,000 one day and 300,000 another, so it cannot be replaced by a number. The test behaves the same: green Monday to Friday, red on Saturday and Sunday, though nobody changed the code. In way 2 every replacement works, and the test passes fixed dates, so it is green every day. The clock does not disappear; it just moves to where the function is called, in plain sight.')
    m('simp.1', 'Phí chỉ có hai mức, không tính ngày lễ. Số tiền là ví dụ; tuần 23–29/11/2026 là lịch thật.',
      'The fee has only two levels, with no public holidays. The amounts are an example; the week of 23–29 November 2026 is the real calendar.')
    m('simp.2', 'Bảng chỉ ghi những lần thay quan trọng; vài bước rút gọn hiển nhiên được gộp lại cho gọn.',
      'The table records only the important replacements; a few obvious simplifications are merged to keep it short.')
    m('ctl.hint', 'Chọn một cách viết rồi bấm qua từng bước. Hàng đỏ trong bảng là chỗ không thay được; hàng dưới cùng cho biết bài test xanh hay đỏ vào từng ngày.', 'Pick a version and step through. A red row in the table cannot be replaced; the bottom row shows whether the test is green or red on each day.')
    m('ctl.case', 'Cách viết', 'Version')
    for k, vi, en in [('impure', 'fee() tự xem ngày', 'fee() looks up the date'), ('pure', 'fee(date) được cho ngày', 'fee(date) is given the date')]:
        m('ctl.case.' + k, vi, en)
    m('diagramTitle', 'Kết quả của hàm phụ thuộc vào đâu', 'What the function\'s result depends on')
    m('diagramDesc', 'Đồng hồ, lời gọi hàm, giá trị nhận được và bài test', 'The clock, the call, the value it returns and the test')
    for k, vi, en in [('world', 'Đồng hồ và biến đếm', 'Clock and counter'), ('call', 'Lời gọi fee', 'The fee call'), ('value', 'Giá trị trả về', 'Returned value'), ('test', 'Bài test', 'Tests')]:
        m('n.' + k, vi, en)
    m('met.subst', 'Hàng thay được', 'Replaceable rows'); m('met.opaque', 'Hàng không thay được', 'Rows that cannot be replaced'); m('met.red', 'Ngày test đỏ', 'Days with a red test')
    a('cap.pure', 'Mũi tên chỉ đường đi của thông tin: đồng hồ đi vào lời gọi hàm, lời gọi cho ra giá trị, bài test kiểm giá trị đó. Ô đỏ là chỗ kết quả phụ thuộc vào thứ không nằm trong tham số.',
      'Arrows show how information flows: the clock feeds the call, the call yields a value, the test checks that value. A red box is where the result depends on something outside the parameters.')
    S = [
        ('impure', 's1', 'Thử thay fee() bằng kết quả của nó', 'Try replacing fee() with its result',
         'Ta có total = fee() + fee(). Muốn tính tay, ta thay fee() bằng con số nó trả về. Nhưng con số đó là bao nhiêu? Chạy thứ Hai thì 200.000, chạy thứ Bảy thì 300.000. Một lời gọi mà có hai đáp án, nên không thay được. Đây là dấu hiệu đầu tiên của một hàm không thuần.',
         'We have total = fee() + fee(). To work it out by hand, we replace fee() with the number it returns. But which number? On Monday it is 200,000, on Saturday 300,000. One call, two answers, so it cannot be replaced. This is the first sign of an impure function.'),
        ('impure', 's2', 'Viết gọn: val a = fee(); total = a + a', 'Tidy up: val a = fee(); total = a + a',
         'Đây là kiểu sửa mã ai cũng làm: gọi một lần, dùng hai lần. Với một hàm bình thường thì kết quả y hệt. Nhưng fee() còn lén tăng biến đếm calls. Viết fee() + fee() thì calls tăng 2; viết gọn thì chỉ tăng 1. Thống kê đã sai chỉ vì một lần dọn mã.',
         'This is a tidy-up everyone does: call once, use twice. For a normal function the result is identical. But fee() also secretly bumps the counter calls. Writing fee() + fee() adds 2; the tidy version adds only 1. The statistics are now wrong because of a clean-up.'),
        ('impure', 's3', 'Chạy test vào thứ Hai: xanh', 'Run the test on Monday: green',
         'Bài test kiểm fee() == 200.000. Bạn chạy trên máy mình vào thứ Hai 23/11: xanh. Nhìn bài test, không ai biết nó đang kiểm ngày nào, vì ngày nằm trong đồng hồ của máy chứ không nằm trong mã.',
         'The test checks fee() == 200,000. You run it on your machine on Monday 23 November: green. Reading the test, nobody can tell which day it checks, because the day lives in the machine\'s clock, not in the code.'),
        ('impure', 's4', 'Máy CI chạy lại vào thứ Bảy 28/11: đỏ', 'The CI server reruns it on Saturday 28 November: red',
         'Đêm thứ Bảy, máy CI chạy lại đúng bài test đó, không ai sửa dòng nào. Lần này fee() trả 300.000 và bài test đỏ. Chạy cả tuần thì đỏ đúng hai ngày: thứ Bảy và Chủ nhật. Một bài test xanh hay đỏ tùy ngày là bài test không đáng tin.',
         'On Saturday night the CI server reruns the very same test, with no line changed. This time fee() returns 300,000 and the test is red. Run all week, it is red on exactly two days: Saturday and Sunday. A test that is green or red depending on the day cannot be trusted.'),
        ('pure', 's1', 'Thay d bằng giá trị của nó', 'Replace d with its value',
         'Bây giờ hàm nhận ngày qua tham số. Ta cho d là thứ Bảy 28/11 rồi thay vào: total = fee(28/11) + fee(28/11). Kết quả chỉ còn phụ thuộc vào thứ ta truyền vào, không phụ thuộc hôm nay là ngày nào.',
         'Now the function takes the date as a parameter. We set d to Saturday 28 November and substitute: total = fee(28 Nov) + fee(28 Nov). The result depends only on what we pass in, not on what day it is today.'),
        ('pure', 's2', 'Tính tay tới khi còn một con số', 'Work it out by hand down to one number',
         'Thay mỗi lời gọi bằng phần thân hàm: 28/11 là thứ Bảy nên điều kiện cuối tuần đúng, mỗi lời gọi thành 300.000, tổng là 600.000. Viết gọn val a = fee(d); a + a cũng ra 600.000. Hai cách viết giờ đúng là một.',
         'Replace each call with the function body: 28 November is a Saturday, so the weekend condition holds, each call becomes 300,000 and the total is 600,000. The tidy version val a = fee(d); a + a also gives 600,000. The two forms are now truly the same.'),
        ('pure', 's3', 'Test với ngày cố định: xanh', 'Tests with fixed dates: green',
         'Giờ bài test tự chọn ngày: thứ Hai 23/11 phải ra 200.000, thứ Bảy 28/11 phải ra 300.000. Chạy vào thứ Hai: cả hai đều xanh. Lợi thêm một điều: ta kiểm được cả giá cuối tuần mà không phải đợi tới cuối tuần.',
         'Now the test picks its own dates: Monday 23 November must give 200,000, Saturday 28 November 300,000. Run on Monday: both green. A bonus: we can check the weekend price without waiting for the weekend.'),
        ('pure', 's4', 'Đồng hồ chuyển ra ngoài; test xanh mọi ngày', 'The clock moves outside; tests are green every day',
         'Việc đọc đồng hồ thật và đếm lượt gọi chuyển ra lớp gọi hàm, tức ViewModel. Chạy bài test cả tuần: không ngày nào đỏ, vì bài test không còn dính tới đồng hồ. Việc đọc đồng hồ vẫn phải có, nhưng giờ nó nằm ở một chỗ rõ ràng (chương "Functional core, imperative shell: lõi thuần, vỏ mỏng" của track này nói kỹ hơn).',
         'Reading the real clock and counting calls move to the layer that calls the function, the ViewModel. Run the test all week: no red day, because the test no longer touches the clock. Reading the clock still has to happen, but now in one obvious place (this track\'s chapter "Functional core, imperative shell: a pure core, a thin shell" goes further).'),
    ]
    for case, k, tv, te, xv, xe in S:
        sid = case + '.' + k
        m('s.%s.title' % sid, tv, te); m('s.%s.explain' % sid, xv, xe); m('ev.' + sid, tv, te)
    for k, vi, en in [
        ('try', 'Mẹo đọc: mỗi bước, nhìn bảng trên để biết có thay được không, rồi nhìn hàng ngày ở dưới để biết bài test xanh hay đỏ.', 'Reading tip: at each step, check the table above to see if the replacement works, then the day row below to see if the test is green or red.'),
        ('impure.s2', 'Một hàm trả đúng con số nhưng còn làm thêm việc khác (ghi log, tăng biến đếm) thì không thuần. Thay lời gọi bằng con số là mất luôn việc làm thêm đó. [[src:book-fp-tut]]',
         'A function that returns the right number but also does something else (logs, bumps a counter) is not pure. Replacing the call with the number loses that extra work. [[src:book-fp-tut]]'),
        ('impure.s3', 'Một hàm chỉ đọc dữ liệu muốn thuần thì phải luôn trả cùng kết quả cho cùng đầu vào. Vậy nó không được tự xem giờ, ngày, số ngẫu nhiên hay ID sinh ngẫu nhiên. [[src:book-seemann]]',
         'A function that only reads data must always return the same result for the same input to be pure. So it may not look up the time, the date, random numbers or randomly generated IDs on its own. [[src:book-seemann]]'),
        ('impure.s4', 'Gặp bài test lúc xanh lúc đỏ, đừng bấm chạy lại cho tới khi xanh. Hãy tìm thứ mà hàm đang tự đọc từ bên ngoài, và chuyển nó thành tham số.',
         'When a test flips between green and red, do not rerun it until it turns green. Find what the function reads from outside on its own, and turn it into a parameter.'),
        ('pure.s1', 'Nói gọn: một biểu thức "thay được bằng kết quả" nếu ở bất cứ đâu, đổi nó thành kết quả mà chương trình vẫn chạy y như cũ. Hàm thuần là hàm mà mọi lời gọi đều như vậy. [[src:book-fp-manning]]',
         'In short: an expression is "replaceable by its result" if, anywhere it appears, swapping it for the result leaves the program running exactly as before. A pure function is one where every call is like that. [[src:book-fp-manning]]'),
        ('pure.s2', 'Cách tính tay này giống giải phương trình ở trường: thay từng phần bằng thứ bằng nó, cho tới khi còn một con số. Người ta gọi nó là mô hình thay thế. [[src:book-fp-manning]]',
         'This hand calculation is like solving an equation at school: replace each part with something equal to it until one number is left. It is called the substitution model. [[src:book-fp-manning]]'),
        ('pure.s3', 'Lợi ích lớn nhất của hàm thuần là bạn đọc mã nhẹ đầu hơn: khi hàm đã trả về, chỉ cần nhớ kết quả, không cần nhớ nó tính ra bằng cách nào. [[src:book-seemann]]',
         'The biggest gain of a pure function is easier reading: once it returns, you only need to remember the result, not how it was computed. [[src:book-seemann]]'),
        ('pure.s4', 'Cách sắp xếp này có tên là "lõi thuần, vỏ mỏng": phần quyết định nhận mọi thứ qua tham số; chỉ lớp ngoài cùng mới xem đồng hồ, ghi log, gọi mạng. [[src:book-seemann]] [[src:book-fp-manning]]',
         'This arrangement is called "a pure core with a thin shell": the decisions receive everything through parameters; only the outermost layer looks at the clock, logs or calls the network. [[src:book-seemann]] [[src:book-fp-manning]]'),
    ]:
        m('co.' + k, vi, en)

    z = lambda k, vi, en=None: a('vz.' + k, vi, en)
    z('tab.pure', 'Bảng thay từng bước', 'Step-by-step replacement table')
    z('pure.cap', 'Mỗi hàng là chương trình sau một lần thay một phần bằng giá trị của nó. Hàng đỏ: thay vào thì chương trình không còn như cũ. Hàng có viền: vừa thêm ở bước này.', 'Each row is the program after replacing one part with its value. A red row: after the replacement the program is no longer the same. Outlined: added in this step.')
    z('pure.tcap', 'Chạy cùng bài test vào từng ngày trong tuần 23–29/11/2026. Ô "?": chưa chạy ngày đó.', 'Running the same test on each day of the week of 23–29 November 2026. "?": not run on that day yet.')
    z('pure.legend', 'Ô gạch đỏ: không thay được, hoặc test đỏ. Chữ đậm: thay được, hoặc test xanh. Ô "?" sẽ mở dần theo từng bước.', 'Red hatched: cannot be replaced, or a red test. Bold: replaceable, or a green test. "?" cells open step by step.')
    for k, vi, en in [('n', 'Lần thay', 'Rewrite'), ('expr', 'Chương trình sau khi thay', 'Program after the replacement'), ('st', 'Thay được?', 'Replaceable?'), ('why', 'Vì sao', 'Why'), ('run', 'Bài test', 'Test')]:
        z('pure.col.' + k, vi, en)
    for k, vi, en in [('start', 'ban đầu', 'start'), ('ok', 'được', 'yes'), ('bad', 'không được', 'no')]:
        z('pure.st.' + k, vi, en)
    for k, vi, en in [
        ('start', 'chương trình gốc', 'the original program'),
        ('runMon', 'nếu chạy thứ Hai 23/11; ngày khác có thể ra số khác', 'if run on Monday 23 November; another day may give another number'),
        ('runSat', 'nếu chạy thứ Bảy 28/11: cùng lời gọi mà ra số khác, nên không có con số nào để thay', 'if run on Saturday 28 November: the same call gives another number, so there is no number to put in'),
        ('calls', 'calls chỉ tăng 1 thay vì 2: viết gọn đã làm chương trình khác đi', 'calls goes up by 1 instead of 2: tidying up changed the program'),
        ('valD', 'thay d bằng ngày cụ thể', 'replace d with the actual date'),
        ('body', 'thay lời gọi bằng thân hàm; 28/11 là thứ Bảy nên điều kiện đúng', 'replace each call with the body; 28 November is a Saturday, so the condition holds'),
        ('eval', 'tính phép if', 'evaluate the if'),
        ('sum', 'cộng hai số', 'add the two numbers'),
        ('same', 'viết gọn cũng ra 600_000: đúng là một chương trình', 'the tidy version also gives 600_000: truly the same program')]:
        z('pure.why.' + k, vi, en)
    for k, vi, en in [('mon', 'T2 {d}', 'Mon {d}'), ('tue', 'T3 {d}', 'Tue {d}'), ('wed', 'T4 {d}', 'Wed {d}'), ('thu', 'T5 {d}', 'Thu {d}'), ('fri', 'T6 {d}', 'Fri {d}'), ('sat', 'T7 {d}', 'Sat {d}'), ('sun', 'CN {d}', 'Sun {d}')]:
        z('pure.day.' + k, vi, en)
    z('pure.test.impure', 'kiểm fee() == 200.000', 'checks fee() == 200,000')
    z('pure.test.pure', 'kiểm với ngày cố định', 'checks with fixed dates')
    z('pure.pass', 'xanh', 'green'); z('pure.fail', 'đỏ', 'red')

    C = 'p1'
    a(C + '.title', 'Hàm thuần và referential transparency', 'Pure functions and referential transparency')
    a(C + '.essence', 'Hàm thuần là hàm "nói gì làm nấy": cùng đầu vào thì luôn cho cùng kết quả, và ngoài việc trả kết quả, nó không làm gì khác.\nVới hàm thuần, bạn có thể thay lời gọi hàm bằng kết quả của nó mà chương trình không đổi. Tính chất này có tên là referential transparency. Nhờ nó, bạn dọn mã, đổi thứ tự hay tính tay đều an toàn.\nHàm tự xem đồng hồ, lấy số ngẫu nhiên hay đọc biến toàn cục thì không thuần, và bài test của nó có thể xanh hôm nay, đỏ ngày mai. Cách chữa: đưa những thứ đó vào qua tham số.',
      'A pure function "does exactly what it says": the same input always gives the same result, and besides returning that result it does nothing else.\nWith a pure function, you can replace a call with its result and the program does not change. This property is called referential transparency. Thanks to it, tidying up code, reordering it or working it out by hand are all safe.\nA function that looks at the clock, takes random numbers or reads global variables is not pure, and its test may be green today and red tomorrow. The cure: pass those things in as parameters.')
    a(C + '.goal.g1', 'Đã thấy một lời gọi không thay được', 'Saw a call that cannot be replaced')
    a(C + '.goal.g2', 'Đã thấy bài test xanh hay đỏ theo ngày', 'Saw the test go green or red by day')
    a(C + '.sim.fp.pure', 'hàm tự xem ngày hay được cho ngày', 'a function that looks up the date or is given it')

    S_ = 'hook'
    a(C + '.sec.%s.title' % S_, 'Đoán trước khi đọc', 'Predict before reading')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'predict', 'Bài test kiểm fee() == 200.000 xanh suốt tuần trên máy bạn. Đêm thứ Bảy, máy CI chạy lại đúng bản mã đó và báo đỏ. Không ai sửa gì. Bạn đoán chuyện gì đã xảy ra?',
      'A test checking fee() == 200,000 is green all week on your machine. On Saturday night, the CI server reruns the very same code and reports red. Nobody changed anything. What do you think happened?')
    B(C, S_, 1, 'ans', 'fee() tự xem hôm nay là ngày nào. Thứ Bảy thì nó trả giá cuối tuần, 300.000, nên bài test đỏ. Kết quả của hàm phụ thuộc vào lúc chạy chứ không chỉ vào đầu vào; chương này gọi đó là hàm không thuần.',
      'fee() looks up today\'s date by itself. On Saturday it returns the weekend price, 300,000, so the test turns red. The function\'s result depends on when it runs, not only on its input; this chapter calls that an impure function.')

    S_ = 'pure'
    a(C + '.sec.%s.title' % S_, 'Hàm thuần là gì', 'What a pure function is')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'p', 'Hãy hình dung một chiếc máy tính bỏ túi. Bấm 2 × 3 thì luôn ra 6, hôm nay hay năm sau cũng vậy, và bấm xong thì không có gì khác thay đổi. Một hàm thuần giống hệt thế. Nó phải đạt hai điều: cùng đầu vào thì luôn cho cùng kết quả; và ngoài việc trả kết quả, nó không làm gì mà bên ngoài nhìn thấy được. [[src:book-fp-tut]]',
      'Picture a pocket calculator. Press 2 × 3 and you always get 6, today or next year, and nothing else changes when you press it. A pure function is just like that. It must do two things: the same input always gives the same result; and besides returning the result, it does nothing visible from outside. [[src:book-fp-tut]]')
    B(C, S_, 2, 'kt', 'fun double(x: Int) = x * 2                  // thuần\n\nfun doubleAndLog(x: Int): Int {               // không thuần: còn ghi log\n    Log.d("calc", "x = $x")\n    return x * 2\n}\n\nfun plusRandom(x: Int) = x + Random.nextInt()  // không thuần: mỗi lần một kết quả',
      'fun double(x: Int) = x * 2                  // pure\n\nfun doubleAndLog(x: Int): Int {               // not pure: it also logs\n    Log.d("calc", "x = $x")\n    return x * 2\n}\n\nfun plusRandom(x: Int) = x + Random.nextInt()  // not pure: a different result each time')
    B(C, S_, 3, 'p', 'doubleAndLog trả đúng con số, nhưng mỗi lần gọi lại để lại một dòng log. plusRandom còn tệ hơn: mỗi lần gọi một kết quả khác. Chỉ có double là thuần. [[src:book-fp-tut]]',
      'doubleAndLog returns the right number, but every call leaves a log line behind. plusRandom is worse: a different result every call. Only double is pure. [[src:book-fp-tut]]')
    B(C, S_, 4, 'p', 'Một mẹo nhận ra hàm không thuần: xem nó có tự lấy thông tin từ bên ngoài không. Seemann nêu cụ thể: một hàm chỉ đọc dữ liệu thì không nên tự xem giờ, ngày, số ngẫu nhiên, ID sinh ngẫu nhiên, nội dung tệp hay database. Hàm nào cần những thứ đó thì nên nhận chúng qua tham số. [[src:book-seemann]]',
      'A tip for spotting impure functions: check whether they fetch information from outside on their own. Seemann is specific: a function that only reads data should not look up the time, the date, random numbers, randomly generated IDs, file contents or the database. A function that needs those should receive them as parameters. [[src:book-seemann]]')
    B(C, S_, 5, 'note', 'Bên trong hàm, bạn vẫn được dùng biến var và sửa nó thoải mái. Miễn là bên ngoài không ai thấy biến đó, hàm vẫn thuần. Thuần hay không là chuyện người gọi nhìn thấy gì. [[src:book-fp-manning]]',
      'Inside the function you may still use a var and change it freely. As long as nobody outside can see that variable, the function stays pure. Purity is about what the caller can see. [[src:book-fp-manning]]')
    B(C, S_, 5, 'kind', 'mechanism')

    S_ = 'rt'
    a(C + '.sec.%s.title' % S_, 'Thay lời gọi bằng kết quả', 'Replacing a call with its result')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'p', 'Ở trường, khi giải toán, bạn thay 2 + 3 bằng 5 mà không cần nghĩ. Ta làm được vậy vì 2 + 3 lúc nào cũng bằng 5. Trong mã cũng thế: nếu đổi một lời gọi hàm thành kết quả của nó mà chương trình vẫn chạy y như cũ, ta nói lời gọi đó có referential transparency, tạm dịch là "thay được bằng kết quả". Hàm thuần là hàm mà mọi lời gọi đều thay được như vậy. [[src:book-fp-manning]]',
      'At school you replace 2 + 3 with 5 without a second thought. You can, because 2 + 3 always equals 5. Code works the same way: if swapping a function call for its result leaves the program running exactly as before, the call has referential transparency, "replaceable by its result". A pure function is one whose every call can be replaced like this. [[src:book-fp-manning]]')
    B(C, S_, 2, 'p', 'Muốn kiểm tra, hãy viết chương trình theo hai cách rồi so. Cách 1: gọi hàm ở mỗi chỗ cần dùng. Cách 2: gọi một lần, lưu vào biến, rồi dùng biến. Nếu hai cách cho cùng mọi thứ, kể cả những gì in ra màn hình hay ghi vào log, thì lời gọi thay được. Đoạn mã dưới đây cho thấy chỉ so giá trị trả về là chưa đủ. [[src:book-fp-tut]]',
      'To check, write the program two ways and compare. Way 1: call the function wherever it is needed. Way 2: call it once, store it in a variable, and use the variable. If both give the same everything, including what is printed or logged, the call is replaceable. The code below shows why comparing return values alone is not enough. [[src:book-fp-tut]]')
    B(C, S_, 3, 'kt', 'fun greet() = println("Xin chào")\n\nval (c1, c2) = greet() to greet()   // in hai dòng\nval g = greet()\nval (d1, d2) = g to g               // in một dòng\n// c1 == d1 và c2 == d2 (đều là Unit), nhưng hai chương trình khác nhau',
      'fun greet() = println("Hello")\n\nval (c1, c2) = greet() to greet()   // prints two lines\nval g = greet()\nval (d1, d2) = g to g               // prints one line\n// c1 == d1 and c2 == d2 (both Unit), yet the two programs differ')
    B(C, S_, 4, 'p', 'Khi mọi lời gọi đều thay được, bạn có thể đọc mã như giải phương trình: thay từng phần bằng thứ bằng nó, cho tới khi còn một con số. Cách đọc này gọi là mô hình thay thế. Bảng trong phần thử nghiệm ở trên làm đúng việc đó; hàng đỏ là chỗ phép thay hỏng. [[src:book-fp-manning]]',
      'When every call is replaceable, you can read code like solving an equation: replace each part with something equal until one number is left. This way of reading is called the substitution model. The table in the experiment above does exactly that; a red row is where the replacement breaks. [[src:book-fp-manning]]')

    S_ = 'effects'
    a(C + '.sec.%s.title' % S_, 'Side effect là gì, và trông thế nào trong app Android', 'What a side effect is, and how it looks in an Android app')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'p', 'Side effect là mọi việc hàm làm ngoài việc trả kết quả, hoặc mọi thông tin nó tự lấy từ bên ngoài. Trong app Android, chúng thường là: đọc đồng hồ (LocalDate.now()), lấy số ngẫu nhiên hay UUID, đọc SharedPreferences, database, mạng; ghi log, sửa biến toàn cục, ghi database, gửi request, gửi sự kiện thống kê. Ném ngoại lệ cũng tính, vì nhìn chữ ký hàm, người gọi không biết nó có thể ném (chương "Lỗi là giá trị" của track này nói tiếp). [[src:book-fp-tut]]',
      'A side effect is anything a function does besides returning its result, or any information it fetches from outside on its own. In an Android app they are usually: reading the clock (LocalDate.now()), taking random numbers or UUIDs, reading SharedPreferences, the database or the network; logging, changing global variables, writing to the database, sending requests, sending analytics events. Throwing an exception counts too, because the function signature does not tell the caller it may throw (this track\'s chapter "Errors as values" picks this up). [[src:book-fp-tut]]')
    B(C, S_, 2, 'p', 'Đừng hiểu nhầm: không ai bắt mọi dòng mã phải thuần. App sinh ra là để hiện màn hình, lưu lịch hẹn, gửi tin nhắc, mà đó đều là side effect. Mục tiêu là biết rõ side effect nằm ở đâu, gom chúng lại một chỗ, để phần tính toán và quyết định còn lại được thuần. [[src:book-fp-manning]]',
      'Do not get it wrong: nobody demands that every line be pure. An app exists to draw screens, save bookings and send reminders, and those are all side effects. The goal is to know where the side effects are and gather them in one place, so the calculations and decisions left over can be pure. [[src:book-fp-manning]]')

    S_ = 'edge'
    a(C + '.sec.%s.title' % S_, 'Cách chữa: đưa thứ hàm tự lấy vào thành tham số', 'The cure: turn what the function fetches into a parameter')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'p', 'Chữa fee() rất đơn giản: thay vì để hàm tự xem đồng hồ, ta đưa ngày vào qua tham số. fee(date) không còn cần biết hôm nay là ngày nào; ai gọi thì người đó quyết định. Trong app, việc xem đồng hồ thật chuyển sang ViewModel. [[src:book-seemann]]',
      'Fixing fee() is simple: instead of letting the function look at the clock, we pass the date in as a parameter. fee(date) no longer needs to know what day it is; whoever calls it decides. In the app, reading the real clock moves to the ViewModel. [[src:book-seemann]]')
    B(C, S_, 2, 'kt', 'class BookingViewModel(private val clock: Clock) : ViewModel() {\n    fun onOpen() {\n        val today = LocalDate.now(clock)          // xem đồng hồ ở đây, ngoài rìa\n        _state.value = FeeUi(fee(today))          // phần tính toán thuần\n    }\n}\n// test phần tính toán: gọi thẳng fee(LocalDate.of(2026, 11, 28))',
      'class BookingViewModel(private val clock: Clock) : ViewModel() {\n    fun onOpen() {\n        val today = LocalDate.now(clock)          // read the clock here, at the edge\n        _state.value = FeeUi(fee(today))          // the pure calculation\n    }\n}\n// test the calculation directly: fee(LocalDate.of(2026, 11, 28))')
    B(C, S_, 3, 'p', 'Cách này dùng được cả khi hàm cần ghi ra ngoài. Ví dụ, hàm đặt lịch không nên tự gọi cổng thanh toán. Hãy cho nó trả về một giá trị mô tả "cần thu bao nhiêu, từ thẻ nào", rồi để lớp ngoài gửi đi. Khi test, bạn chỉ cần so giá trị đó, không phải giả lập cổng thanh toán. Ý "lõi thuần, vỏ mỏng" này được bàn kỹ ở chương "Functional core, imperative shell: lõi thuần, vỏ mỏng" của track này. [[src:book-fp-manning]]',
      'This also works when a function needs to write to the outside. For example, the booking function should not call the payment gateway itself. Have it return a value describing "how much to charge, from which card", and let the outer layer send it. To test, you only compare that value, with no fake payment gateway. This "pure core, thin shell" idea is covered in depth in this track\'s chapter "Functional core, imperative shell: a pure core, a thin shell". [[src:book-fp-manning]]')

    S_ = 'bugs'
    a(C + '.sec.%s.title' % S_, 'Hai lỗi hay gặp', 'Two common bugs')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'bug', 'Bài test phí lúc xanh lúc đỏ, và đỏ đúng vào cuối tuần.', 'A fee test is sometimes green, sometimes red, and red exactly at the weekend.')
    B(C, S_, 1, 'cause', 'Hàm được test tự xem LocalDate.now(), nên kết quả phụ thuộc vào ngày chạy test chứ không chỉ vào đầu vào.', 'The function under test calls LocalDate.now() itself, so its result depends on the day the test runs, not only on its input.')
    B(C, S_, 1, 'fix', 'Đưa ngày vào qua tham số và để lớp gọi xem đồng hồ. Viết một bài test cho mỗi loại ngày, mỗi bài dùng một ngày cố định.', 'Pass the date in as a parameter and let the calling layer read the clock. Write one test per kind of day, each with a fixed date.')
    B(C, S_, 2, 'bug', 'Đặt lịch khi mạng chập chờn tạo ra hai lịch hẹn, ngay sau một lần sửa mã "chỉ gộp biến cho gọn".', 'Booking on a flaky network creates two appointments, right after a change that "only inlined a variable".')
    B(C, S_, 2, 'cause', 'Trước đó, mã tạo một mã chống trùng (key = UUID.randomUUID()) một lần, bên ngoài vòng thử lại. Người sửa gộp biến vào chỗ dùng, nên lệnh tạo UUID chạy lại ở mỗi lần thử. Mỗi lần thử có một mã mới, server tưởng là yêu cầu mới và tạo lịch thứ hai. Lời gọi UUID.randomUUID() không thay được bằng kết quả, nên gộp biến đã làm chương trình khác đi.',
      'Before, the code created a duplicate-prevention key (key = UUID.randomUUID()) once, outside the retry loop. The change inlined the variable, so the UUID was created again on every attempt. Each attempt got a new key, the server took it for a new request and created a second booking. The call UUID.randomUUID() is not replaceable by its result, so inlining changed the program.')
    B(C, S_, 2, 'fix', 'Chỉ gộp hay tách biến với những biểu thức thuần. Tạo mã chống trùng một lần, đặt tên rõ ràng, rồi truyền vào; thêm một bài test "thử lại phải dùng cùng mã". Mã chống trùng được giải thích ở chương I5, "Mạng không tin cậy: timeout, thử lại, idempotency", của track Thiết kế hệ thống phía mobile.',
      'Only inline or extract pure expressions. Create the duplicate-prevention key once, give it a clear name and pass it in; add a "retries must reuse the same key" test. Such keys are explained in chapter I5, "Unreliable networks: timeouts, retries, idempotency", of the Mobile System Design track.')

    S_ = 'ex'
    a(C + '.sec.%s.title' % S_, 'Bài tập', 'Exercise')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'ex', 'Trong bốn hàm dưới đây, hàm nào thuần? Viết lại các hàm còn lại sao cho phần tính toán trở nên thuần.',
      'Which of the four functions below are pure? Rewrite the others so that the calculation part becomes pure.')
    B(C, S_, 1, 'exkt', 'var lastTicket = 0\nfun ticket(): Int = ++lastTicket\nfun discount(fee: Long, member: Boolean): Long = if (member) fee * 9 / 10 else fee\nfun isPast(slot: LocalDateTime): Boolean = slot.isBefore(LocalDateTime.now())\nfun feeAndLog(fee: Long): Long { Log.d("fee", "$fee"); return fee }')
    B(C, S_, 1, 'hint', 'Với mỗi hàm, hỏi hai câu: cùng đầu vào có luôn ra cùng kết quả không? Gọi thêm một lần có làm thay đổi gì bên ngoài không?', 'For each function, ask two questions: does the same input always give the same result? Does one extra call change anything outside?')
    B(C, S_, 1, 'sol', 'Chỉ discount là thuần. ticket sửa biến bên ngoài và mỗi lần trả một số khác. isPast tự xem đồng hồ, nên hãy đưa "bây giờ" vào qua tham số. feeAndLog trả đúng phí nhưng còn ghi log, nên hãy để chỗ gọi tự ghi log. Muốn phần đánh số thuần, cho hàm nhận số hiện tại và trả số kế tiếp; việc lưu số mới là của chỗ gọi.',
      'Only discount is pure. ticket changes an outside variable and returns a different number each time. isPast looks at the clock itself, so pass "now" in as a parameter. feeAndLog returns the right fee but also logs, so let the caller do the logging. To make numbering pure, take the current number and return the next one; storing the new number is the caller\'s job.')
    B(C, S_, 1, 'solkt', 'fun nextTicket(current: Int): Int = current + 1\nfun discount(fee: Long, member: Boolean): Long = if (member) fee * 9 / 10 else fee\nfun isPast(slot: LocalDateTime, now: LocalDateTime): Boolean = slot.isBefore(now)\n// chỗ gọi: val f = fee(today); Log.d("fee", "$f")',
      'fun nextTicket(current: Int): Int = current + 1\nfun discount(fee: Long, member: Boolean): Long = if (member) fee * 9 / 10 else fee\nfun isPast(slot: LocalDateTime, now: LocalDateTime): Boolean = slot.isBefore(now)\n// the caller: val f = fee(today); Log.d("fee", "$f")')

    for q, qv, qe, av, ae, wv, we in [
        ('q1', 'Khi nào một lời gọi hàm "thay được bằng kết quả"?', 'When is a function call "replaceable by its result"?', 'Khi đổi nó thành kết quả ở mọi chỗ mà chương trình vẫn chạy y như cũ.', 'When swapping it for its result everywhere leaves the program running exactly as before.', 'Phải so cả chương trình, kể cả log và những gì in ra, không chỉ so giá trị trả về.', 'Compare the whole program, including logs and printed output, not only return values.'),
        ('q2', 'fun fee(): Long tự xem LocalDate.now() và không sửa biến nào. Nó có thuần không?', 'fun fee(): Long calls LocalDate.now() and changes no variable. Is it pure?', 'Không.', 'No.', 'Cùng một lời gọi mà kết quả đổi theo ngày chạy.', 'The same call gives a result that changes with the day it runs.'),
        ('q3', 'Hàm ghi một dòng log rồi trả đúng x * 2. Nó có thuần không?', 'A function writes a log line and returns x * 2. Is it pure?', 'Không.', 'No.', 'Thay lời gọi bằng kết quả thì mất dòng log, nên chương trình đã khác.', 'Replacing the call with its result loses the log line, so the program is different.'),
        ('q4', 'Dùng và sửa một biến var bên trong thân hàm có làm hàm mất thuần không?', 'Does using and changing a var inside the function body make it impure?', 'Không, nếu bên ngoài không ai thấy biến đó.', 'No, as long as nobody outside can see that variable.', 'Thuần hay không là chuyện người gọi nhìn thấy gì.', 'Purity is about what the caller can see.')]:
        a(C + '.quiz.%s.q' % q, qv, qe); a(C + '.quiz.%s.a' % q, av, ae); a(C + '.quiz.%s.why' % q, wv, we)
