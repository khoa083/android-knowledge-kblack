# Mã sạch · J4: TDD (Phần 2: test và thay đổi an toàn)
# Nguồn: Martin, Clean Craftsmanship ch.2 (bản chất của TDD, ba luật "hoàn toàn tùy ý", luật thứ tư: refactor; red → green → refactor);
# Martin, Clean Code ch.9 (ba luật TDD, F.I.R.S.T.); Seemann, Code That Fits in Your Head 5.2.2 (Red Green Refactor, như phương pháp khoa học),
# 6.2.2 (Devil's Advocate, trích Martin "test càng cụ thể, mã càng tổng quát"), 6.2.5 (đủ test chưa là đánh giá rủi ro), 11.2 (đừng tin test
# chưa từng thấy đỏ), A.10, A.17. Đọc 2026-11-24, diễn đạt lại. Ngày trong ví dụ đã kiểm thứ: 23/11/2026 thứ hai, 28/11 thứ bảy, 29/11 chủ nhật,
# 2/9/2026 (Quốc khánh) thứ tư.

SEC_ORDER = {'j4': ['hook', 'laws', 'cycle', 'triangulate', 'first', 'bugs', 'ex']}


def add(a):
    def B(ch, sec, n, field, vi, en=None):
        a('%s.sec.%s.b.%02d.%s' % (ch, sec, n, field), vi, vi if en is None else en)

    a('preset.tdd', 'Mã sạch · TDD cho phí khám', 'Clean code · TDD for the visit fee')
    m = lambda k, vi, en=None: a('m.tdd.' + k, vi, en)
    m('title', 'Viết mã rồi mới test, hay test trước từng ví dụ', 'Code first and test later, or test first, one example at a time')
    m('overview', 'Hàm fee(date) tính phí khám: ngày thường 200.000 đ, cuối tuần 300.000 đ, ngày lễ 400.000 đ. Cách thứ nhất: viết cả hàm theo trí nhớ, rồi viết vài test cho chắc. Cách thứ hai: TDD (test-driven development, viết test trước rồi mới viết mã), mỗi vòng thêm một ví dụ vào danh sách test, thấy test đỏ (không qua), viết vừa đủ mã cho nó xanh (qua), rồi dọn mã.',
      'The fee(date) function computes the visit fee: 200,000 VND on weekdays, 300,000 on weekends, 400,000 on public holidays. First approach: write the whole function from memory, then add a few tests to be sure. Second approach: TDD (test-driven development: write the test first, then the code), each cycle adds one example to the test list, sees the test fail (red), writes just enough code to make it pass (green), then cleans up.')
    m('wrapup', 'Viết mã trước, test chỉ kiểm lại những gì người viết đã nghĩ tới: hai test xanh ngay lần đầu, không ai thấy chúng đỏ, và ngày lễ chưa bao giờ có trong đầu ai cho tới khi bệnh nhân bị tính sai vào ngày 2/9. Với TDD, danh sách ví dụ là nơi nghĩ về trường hợp biên trước khi viết mã; mỗi test được thấy đỏ trước khi xanh, nên ta biết nó kiểm thật; và mã chỉ trở nên tổng quát khi một ví dụ mới buộc nó phải như vậy.',
      'Writing code first, the tests only re-check what the author already thought of: two tests pass the first time, nobody sees them fail, and public holidays were never on anyone\'s mind until a patient was charged wrongly on 2 September. With TDD, the example list is where edge cases are thought about before code exists; every test is seen failing before it passes, so we know it really checks something; and the code becomes general only when a new example forces it to.')
    m('simp.1', 'Mức phí, danh sách ngày lễ và các ngày ví dụ là minh họa; danh sách ngày lễ giả định do server cấp. Một vòng TDD thật chỉ dài vài chục giây và có nhiều bước nhỏ hơn bốn bước ở đây.', 'The fees, the holiday list and the example dates are illustrative; the holiday list is assumed to come from the server. A real TDD cycle lasts tens of seconds and has many more, smaller steps than the four shown here.')
    m('simp.2', 'Ba luật TDD và luật thứ tư là của Robert C. Martin; chính Martin gọi ba luật là tùy ý, vì có cách khác đạt cùng mục tiêu. Devil\'s Advocate (người cố tình cãi ngược) là cách gọi của Mark Seemann.', 'The three TDD laws and the fourth are Robert C. Martin\'s; Martin himself calls the three laws arbitrary, since other disciplines reach the same goals. The Devil\'s Advocate (someone who argues against on purpose) is Mark Seemann\'s name for a check.')
    m('ctl.hint', 'Đổi cách làm rồi đi lại; nhìn vòng ba pha và cột "Đã thấy đỏ" trong bảng test.', 'Switch the approach and walk again; watch the three-phase ring and the "Seen red" column of the test table.')
    m('ctl.case', 'Cách làm', 'Approach')
    for k, vi, en in [('after', 'viết mã trước, test sau', 'code first, tests after'), ('tdd', 'TDD: test trước từng ví dụ', 'TDD: test first, one example at a time')]:
        m('ctl.case.' + k, vi, en)
    m('diagramTitle', 'Danh sách ví dụ, test, mã, bệnh nhân', 'Example list, tests, code, patients')
    m('diagramDesc', 'Ví dụ thành test; test đỏ dẫn mã; mã tính phí cho bệnh nhân', 'Examples become tests; red tests drive the code; the code charges patients')
    for k, vi, en in [('list', 'Danh sách ví dụ', 'Example list'), ('test', 'Test', 'Tests'), ('code', 'Mã fee()', 'fee() code'), ('patient', 'Bệnh nhân', 'Patients')]:
        m('n.' + k, vi, en)
    m('met.tests', 'Test đã viết', 'Tests written'); m('met.red', 'Test đã thấy đỏ', 'Tests seen failing'); m('met.wrong', 'Ngày tính sai phí', 'Days charged wrongly')
    a('cap.tdd', 'Danh sách ví dụ sinh ra test, test đỏ dẫn đường cho mã, mã tính phí cho bệnh nhân. Nút đỏ: nơi một trường hợp bị bỏ sót lộ ra.', 'The example list produces tests, red tests guide the code, the code charges patients. Red node: where a missed case surfaces.')
    S = [
        ('after', 's1', 'Viết cả hàm theo trí nhớ', 'Write the whole function from memory',
         'Người viết nhớ quy tắc cuối tuần và viết luôn: thứ bảy, chủ nhật 300.000 đ, còn lại 200.000 đ. Chưa có test nào; ngày lễ không ai nhắc tới.', 'The author remembers the weekend rule and writes it straight away: Saturday and Sunday 300,000, otherwise 200,000. No tests yet; nobody mentions holidays.'),
        ('after', 's2', 'Thêm hai test cho chắc', 'Add two tests to be sure',
         'Test thứ hai 23/11 → 200.000 và thứ bảy 28/11 → 300.000. Cả hai xanh ngay lần chạy đầu. Không ai thấy chúng đỏ bao giờ.', 'Tests for Monday 23 Nov → 200,000 and Saturday 28 Nov → 300,000. Both pass on the first run. Nobody ever sees them fail.'),
        ('after', 's3', 'Mọi test xanh, phát hành', 'All tests green, ship it',
         'Hai test, hai màu xanh. Các test chỉ kiểm lại đúng những gì người viết đã nghĩ khi viết mã, nên không thể tìm ra điều họ chưa nghĩ tới.', 'Two tests, two greens. The tests only re-check exactly what the author thought while writing the code, so they cannot find what the author never thought of.'),
        ('after', 's4', 'Ngày 2/9: tính sai phí', '2 September: the wrong fee',
         'Quốc khánh 2/9/2026 là thứ tư. Hàm trả 200.000 đ thay vì 400.000 đ. Không có test nào cho ngày lễ, vì ngày lễ chưa từng có trong danh sách nào.', 'National Day, 2 Sep 2026, is a Wednesday. The function returns 200,000 instead of 400,000. There is no holiday test, because holidays were never on any list.'),
        ('tdd', 's1', 'Ví dụ 1: thứ hai → 200.000', 'Example 1: Monday → 200,000',
         'Danh sách ví dụ được viết trước, có cả ngày lễ. Test đầu đỏ (hàm chưa có), rồi xanh với mã đơn giản nhất: trả về hằng 200.000. Mã rõ ràng còn thiếu: danh sách test chưa đủ.', 'The example list comes first, holidays included. The first test fails (no function yet), then passes with the simplest code: return the constant 200,000. The code is obviously incomplete: the test list is not done.'),
        ('tdd', 's2', 'Ví dụ 2: thứ bảy → 300.000', 'Example 2: Saturday → 300,000',
         'Test đỏ: hằng 200.000 không còn đủ. Mã vừa đủ cho xanh: nếu là thứ bảy thì 300.000. Vẫn có thể "lừa" test: chủ nhật chưa được kiểm.', 'The test fails: the 200,000 constant is no longer enough. Just enough code to pass: Saturday gives 300,000. The tests can still be "fooled": Sunday is unchecked.'),
        ('tdd', 's3', 'Ví dụ 3: chủ nhật → 300.000, rồi dọn mã', 'Example 3: Sunday → 300,000, then clean up',
         'Test đỏ, thêm chủ nhật cho xanh, rồi refactor: tách isWeekend() khi mọi test đang xanh. Test càng cụ thể, mã càng tổng quát.', 'The test fails, adding Sunday makes it pass, then refactor: extract isWeekend() while every test is green. As the tests get more specific, the code gets more generic.'),
        ('tdd', 's4', 'Ví dụ 4: 2/9 → 400.000, rồi dọn mã', 'Example 4: 2 Sep → 400,000, then clean up',
         'Test đỏ, thêm nhánh ngày lễ cho xanh, rồi refactor thành when với hằng BASE. Bốn test, cả bốn đã từng đỏ rồi xanh. Ngày 2/9 tính đúng 400.000.', 'The test fails, a holiday branch makes it pass, then refactor into a when with a BASE constant. Four tests, all four seen failing then passing. 2 September is charged 400,000 correctly.'),
    ]
    for case, k, tv, te, xv, xe in S:
        sid = case + '.' + k
        m('s.%s.title' % sid, tv, te); m('s.%s.explain' % sid, xv, xe); m('ev.' + sid, tv, te)
    for k, vi, en in [
        ('try', 'Theo vòng ba pha và bảng test; để ý test nào đã từng đỏ.', 'Follow the three-phase ring and the test table; watch which tests have ever failed.'),
        ('after.s2', 'Quy tắc ngón tay cái: đừng tin một test chưa từng thấy nó đỏ. Assertion (dòng khẳng định kết quả phải bằng gì) luôn đúng bất kể mã, gọi là tautological, dễ viết hơn ta tưởng; nếu chưa thấy test đỏ thì chưa biết nó có kiểm gì không. [[src:book-seemann]]', 'Rule of thumb: do not trust a test you have not seen fail. A tautological assertion (an assertion that is always true, whatever the code does) is surprisingly easy to write; an assertion is the line that states what the result must equal. Until you have seen a test fail, you do not know whether it checks anything. [[src:book-seemann]]'),
        ('after.s3', 'Test viết sau mã thường đi theo đúng đường mã đã có. Danh sách ví dụ viết trước mã là chỗ để nghĩ tới trường hợp biên.', 'Tests written after the code tend to follow the paths the code already has. An example list written before the code is where edge cases get thought of.'),
        ('after.s4', 'Lỗi đã lọt ra môi trường thật chứng tỏ lỗi đó có thể xảy ra; hãy viết một test tái hiện nó trước khi sửa. [[src:book-seemann]]', 'A defect that reached production proves that error can happen; write a test that reproduces it before fixing. [[src:book-seemann]]'),
        ('tdd.s1', 'Devil\'s Advocate (người cố tình cãi ngược, cách gọi của Seemann): cố tình viết cài đặt sai rõ ràng mà vẫn qua mọi test. Làm được thì danh sách test chưa đủ. [[src:book-seemann]]', 'The Devil\'s Advocate (someone who argues against on purpose; Seemann\'s name for it): deliberately write an obviously wrong implementation that still passes every test. If you can, the test list is not enough. [[src:book-seemann]]'),
        ('tdd.s2', 'Một trong ba luật TDD của Robert C. Martin: không viết nhiều mã hơn mức đủ để test đang đỏ chuyển xanh (mã ở đây là mã sản phẩm, tức mã chạy trong app, khác với mã test). [[src:book-craft]]', 'One of Robert C. Martin\'s three TDD laws: write no more production code than resolves the currently failing test (production code is the code that ships in the app, as opposed to test code). [[src:book-craft]]'),
        ('tdd.s3', 'Luật thứ tư của Martin: refactor, tức là sắp xếp lại mã cho gọn mà không đổi hành vi, và chỉ làm khi mọi test đang xanh. Không thể vừa làm cho mã chạy vừa làm cho mã đẹp cùng lúc; theo lời khuyên của Kent Beck: trước làm cho chạy, rồi làm cho đúng. [[src:book-craft]]', 'Martin\'s fourth law: refactor, meaning rearrange the code to be cleaner without changing behaviour, and only while every test is green. You cannot make code work and make it well-structured at the same moment; Kent Beck\'s advice: first make it work, then make it right. [[src:book-craft]]'),
        ('tdd.s4', 'Vòng đỏ, xanh, refactor giống phương pháp khoa học: test đỏ là một dự đoán có thể sai (có thể bác bỏ), chạy test là thí nghiệm, rồi so kết quả với dự đoán. [[src:book-seemann]]', 'The red, green, refactor cycle resembles the scientific method: a failing test is a prediction that could turn out wrong, running it is the experiment, then you compare the outcome with the prediction. [[src:book-seemann]]')]:
        m('co.' + k, vi, en)

    z = lambda k, vi, en=None: a('vz.' + k, vi, en)
    z('tab.tdd', 'Vòng TDD và danh sách test', 'TDD cycle and test list')
    z('td.cap', 'Vòng ba pha: pha sáng là pha cuối của bước này; dòng dưới vòng là các pha đã đi qua trong bước.', 'The three-phase ring: the lit phase is where this step ends; the line below lists the phases walked in this step.')
    for k, vi, en in [('red', 'Đỏ', 'Red'), ('green', 'Xanh', 'Green'), ('refactor', 'Refactor', 'Refactor')]:
        z('td.ph.' + k, vi, en)
    z('td.walk', 'Bước này: {path}', 'This step: {path}')
    z('td.walk.none', 'chưa có test nào chạy', 'no test has run')
    z('td.walk.code', 'viết mã, chưa có test', 'writing code, no test yet')
    z('td.walk.prod', 'không có test: lỗi lộ ra ở bệnh nhân', 'no test: the bug shows up at the patient')
    z('td.aria', 'Vòng TDD, pha hiện tại: {ph}', 'TDD cycle, current phase: {ph}')
    z('td.tcap', 'Danh sách ví dụ thành test. Cột cuối: test đã từng đỏ chưa (đừng tin test chưa từng thấy đỏ).', 'The example list as tests. Last column: has the test ever failed (do not trust a test you have not seen fail).')
    for k, vi, en in [('ex', 'Ví dụ', 'Example'), ('want', 'Mong đợi', 'Expected'), ('now', 'Lúc này', 'Now'), ('seen', 'Đã thấy đỏ', 'Seen red')]:
        z('td.col.' + k, vi, en)
    for k, vi, en in [('mon', 'thứ hai 23/11', 'Monday 23 Nov'), ('sat', 'thứ bảy 28/11', 'Saturday 28 Nov'), ('sun', 'chủ nhật 29/11', 'Sunday 29 Nov'), ('hol', 'lễ 2/9 (thứ tư)', 'holiday 2 Sep (Wednesday)')]:
        z('td.ex.' + k, vi, en)
    for k, vi, en in [('pass', 'xanh', 'pass'), ('fail', 'đỏ', 'fail'), ('none', 'chưa viết', 'not written'), ('prod', 'chưa viết; thực tế {v}', 'not written; in production {v}')]:
        z('td.st.' + k, vi, en)
    z('td.yes', 'có', 'yes'); z('td.no', 'chưa', 'never')
    z('td.money', '{v} đ', '{v} VND')
    z('td.legend', 'Viền đậm: hàng vừa đổi ở bước này. Ô gạch đỏ: test đang đỏ hay ngày bị tính sai phí. "chưa": test chưa từng đỏ, chưa biết nó kiểm thật hay không.', 'Bold outline: rows changed in this step. Red hatched: a failing test or a day charged wrongly. "never": the test has never failed, so we do not know whether it really checks anything.')

    C = 'j4'
    a(C + '.title', 'TDD: test trước, từng ví dụ một', 'TDD: test first, one example at a time')
    a(C + '.essence', 'Ba luật TDD (viết test trước rồi mới viết mã) của Robert C. Martin: không viết mã sản phẩm, tức mã chạy trong app, khi chưa có test đỏ (test không qua); không viết test nhiều hơn mức đủ để đỏ; không viết mã nhiều hơn mức đủ để test xanh (qua). Luật thứ tư: refactor, sắp xếp lại mã cho gọn mà không đổi hành vi, khi mọi test xanh.\nViết danh sách ví dụ trước mã: đó là lúc nghĩ tới trường hợp biên như ngày lễ. Mỗi test phải được thấy đỏ trước khi xanh, nếu không thì chưa biết nó có kiểm gì.\nTam giác hóa (triangulation): nếu một cài đặt sai rõ ràng vẫn qua mọi test (cách thử này gọi là Devil\'s Advocate, người cố tình cãi ngược), hãy thêm ví dụ. Test càng cụ thể, mã càng tổng quát.',
      'Robert C. Martin\'s three laws of TDD (write the test first, then the code): write no production code, meaning code that ships in the app, without a failing (red) test; write no more test than is enough to fail; write no more code than is enough to pass (green). The fourth law: refactor, meaning rearrange the code to be cleaner without changing behaviour, while all tests are green.\nWrite the example list before the code: that is when edge cases like public holidays get thought of. Each test must be seen failing before it passes, or you do not know whether it checks anything.\nTriangulation: if an obviously wrong implementation still passes every test (this check is called the Devil\'s Advocate, someone arguing against on purpose), add an example. As the tests get more specific, the code gets more generic.')
    a(C + '.goal.g1', 'Đã thấy tam giác hóa ở ví dụ chủ nhật', 'Saw triangulation with the Sunday example')
    a(C + '.goal.g2', 'Đã thấy ngày 2/9', 'Saw 2 September')
    a(C + '.sim.cleancode.tdd', 'viết mã trước hay TDD', 'code first or TDD')

    S_ = 'hook'
    a(C + '.sec.%s.title' % S_, 'Đoán trước khi đọc', 'Predict before reading')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'predict', 'Hàm tính phí có hai test, cả hai xanh, độ phủ dòng (tỉ lệ dòng mã mà test chạy qua) gần 100%. Vậy mà ngày Quốc khánh bệnh nhân bị tính phí ngày thường. Vì sao test xanh và độ phủ cao vẫn không bắt được lỗi này?',
      'The fee function has two tests, both green, with nearly 100% line coverage (the share of code lines the tests run through). Yet on National Day patients are charged the weekday fee. Why did green tests and high coverage miss it?')
    B(C, S_, 1, 'ans', 'Vì lỗi không nằm ở dòng mã nào: nó là một nhánh chưa bao giờ được viết. Độ phủ chỉ đo những dòng đã có. Test viết sau mã thường kiểm lại đúng những gì người viết đã nghĩ, nên không thể tìm ra điều họ chưa nghĩ tới. Mô phỏng ngay dưới so cách đó với TDD, nơi danh sách ví dụ có trước mã.',
      'Because the bug is not on any line of code: it is a branch that was never written. Coverage measures only the lines that exist. Tests written after the code tend to re-check what the author already thought, so they cannot find what the author never thought of. The simulation just below compares that with TDD, where the example list comes before the code.')

    S_ = 'laws'
    a(C + '.sec.%s.title' % S_, 'Ba luật và luật thứ tư', 'The three laws and the fourth')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'p', 'Robert C. Martin phát biểu ba luật TDD. Một: không viết mã sản phẩm (mã chạy trong app, khác mã test) khi chưa có một test đỏ vì thiếu chính mã đó. Hai: không viết test nhiều hơn mức đủ để đỏ, và không biên dịch được cũng tính là đỏ. Ba: không viết mã sản phẩm nhiều hơn mức đủ cho test đang đỏ được xanh. Ba luật khóa người viết vào một vòng chỉ dài vài giây, chuyển qua lại giữa test và mã. Cách nhớ: một test đỏ, một bước mã, rồi lại một test đỏ. [[src:book-craft]] [[src:book-cleancode]]',
      'Robert C. Martin states three TDD laws. One: write no production code (the code that runs in the app, as opposed to test code) until you have a test that fails for lack of that code. Two: write no more of a test than is enough to fail, and failing to compile counts as failing. Three: write no more production code than resolves the currently failing test. The three laws lock you into a cycle a few seconds long, switching between test and code. To remember it: one red test, one step of code, then the next red test. [[src:book-craft]] [[src:book-cleancode]]')
    B(C, S_, 2, 'p', 'Martin thêm luật thứ tư: refactor (sắp xếp lại mã cho gọn mà không đổi hành vi). Tập trung viết test cho đỏ thì test khó đẹp; tập trung cho xanh thì mã khó đẹp; nên sau mỗi lần xanh, dọn mã ngay, khi mọi test vẫn xanh. Refactor là việc liên tục, không lên lịch, không xin phép. Martin cũng nói thẳng ba luật là tùy ý: điều cốt lõi là bộ test đủ tin để test qua nghĩa là triển khai được, mã đủ tách rời để test được, và một vòng phản hồi rất ngắn; cách làm khác của Kent Beck, TCR (test && commit || revert: chạy test, qua thì commit, hỏng thì bỏ thay đổi vừa làm), cũng đạt được những điều đó. Cách nhớ: vừa xanh là dọn. [[src:book-craft]]',
      'Martin adds a fourth law: refactor (rearrange the code to be cleaner without changing behaviour). Focused on making a test fail, the test is rarely well written; focused on making it pass, the code is rarely well written; so after each pass, clean up at once, while all tests stay green. Refactoring is continuous, never scheduled, never asked permission for. Martin also says plainly the three laws are arbitrary: the essence is a test suite trusted enough that passing means deployable, code decoupled enough to test, and a very short feedback loop; Kent Beck\'s different discipline, TCR (test && commit || revert: run the tests, commit if they pass, throw the change away if they fail), reaches the same goals. To remember it: green, then tidy. [[src:book-craft]]')

    S_ = 'cycle'
    a(C + '.sec.%s.title' % S_, 'Đỏ, xanh, refactor', 'Red, green, refactor')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'p', 'Vòng đỏ, xanh, refactor (Red Green Refactor) là một checklist: viết một test đỏ; thay đổi tối thiểu để mọi test xanh; cải thiện mã mà không đổi hành vi; rồi bắt đầu lại. Có thể so nó với phương pháp khoa học: test đỏ là một dự đoán có thể sai, chạy test là thí nghiệm. Test chưa từng đỏ là thí nghiệm không thể thất bại, nên không chứng minh được gì. Cách nhớ: chưa thấy đỏ thì chưa tin xanh. [[src:book-seemann]]',
      'The Red Green Refactor cycle is a checklist: write a failing test; make the minimal change so all tests pass; improve the code without changing behaviour; start over. It can be compared to the scientific method: a failing test is a prediction that can be wrong, running it is the experiment. A test that has never failed is an experiment that cannot fail, so it proves nothing. To remember it: no red seen, no green trusted. [[src:book-seemann]]')
    B(C, S_, 2, 'kt', '@Test fun `ngày lễ tính 400 nghìn`() {\n    val holidays = setOf(LocalDate.of(2026, 9, 2))\n    assertEquals(400_000, fee(LocalDate.of(2026, 9, 2), holidays))   // đỏ trước, rồi mới xanh\n}',
      '@Test fun `holiday costs 400 thousand`() {\n    val holidays = setOf(LocalDate.of(2026, 9, 2))\n    assertEquals(400_000, fee(LocalDate.of(2026, 9, 2), holidays))   // red first, then green\n}')
    B(C, S_, 3, 'note', 'Tên test có khoảng trắng trong dấu backtick là quy ước Kotlin chỉ dành cho test; theo tài liệu quy ước, Android runtime chỉ hỗ trợ tên như vậy từ API 30 (Android 11), nên dùng cho test chạy trên JVM (chạy ngay trên máy tính, không cần điện thoại). [[src:kt-conventions]]',
      'Test names with spaces in backticks are a Kotlin convention for tests only; per the conventions page, the Android runtime supports such names only from API 30 (Android 11), so use them for tests that run on the JVM (right on your computer, no phone needed). [[src:kt-conventions]]')
    B(C, S_, 3, 'kind', 'android')

    S_ = 'triangulate'
    a(C + '.sec.%s.title' % S_, 'Tam giác hóa và Devil\'s Advocate', 'Triangulation and the Devil\'s Advocate')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'p', 'Làm sao biết đã đủ ví dụ? Hãy làm người cố tình cãi ngược (Devil\'s Advocate, cách gọi của Seemann): cố tình viết một cài đặt sai rõ ràng mà vẫn qua mọi test, như trả về hằng 200.000 hay chỉ kiểm thứ bảy. Nếu làm được, danh sách test còn thiếu; thêm một ví dụ buộc mã phải tổng quát hơn. Martin có một câu để nhớ: test càng cụ thể, mã càng tổng quát. Đó là tam giác hóa (triangulation): hai, ba điểm ví dụ chốt được một quy tắc, như hai, ba mốc trên bản đồ chốt được một vị trí. [[src:book-seemann]]',
      'How do you know you have enough examples? Play the devil\'s advocate (Seemann\'s name for it): deliberately write an obviously wrong implementation that still passes every test, such as returning the constant 200,000 or checking only Saturday. If you can, the test list is short; add one example that forces more general code. Martin has a line worth remembering: as the tests get more specific, the code gets more generic. That is triangulation: two or three example points pin down a rule, the way two or three landmarks on a map pin down a position. [[src:book-seemann]]')
    B(C, S_, 2, 'p', 'Không có câu trả lời bằng con số cho câu hỏi "đủ test chưa": đó là đánh giá rủi ro, cân xác suất một lỗi xảy ra với hậu quả của nó. Một lỗi đã lọt ra môi trường thật chứng tỏ nó có thể xảy ra, nên luôn viết một test tái hiện nó. [[src:book-seemann]]',
      'There is no quantitative answer to "do I have enough tests": it is risk assessment, weighing the probability of a defect against its impact. A defect that reached production proves it can happen, so always write a test that reproduces it. [[src:book-seemann]]')

    S_ = 'first'
    a(C + '.sec.%s.title' % S_, 'Test sạch: F.I.R.S.T.', 'Clean tests: F.I.R.S.T.')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'p', 'Một unit test sạch có năm tính chất, gọi tắt bằng chữ cái đầu là F.I.R.S.T. (unit test là test kiểm một đơn vị nhỏ của mã, như một hàm). Fast: chạy nhanh, nếu chậm người ta sẽ ngại chạy. Independent: test không phụ thuộc nhau, chạy theo thứ tự nào cũng được. Repeatable: chạy được ở mọi môi trường, kể cả không có mạng. Self-validating: kết quả là đạt hay không đạt, không phải đọc log để đoán. Timely: viết ngay trước mã sản phẩm. Hàm fee nhận danh sách ngày lễ làm tham số thay vì tự gọi server, nên test của nó vừa nhanh vừa lặp lại được. Cách nhớ: test tốt là test bạn muốn chạy mỗi vài giây. [[src:book-cleancode]]',
      'A clean unit test has five qualities, named by their initials as F.I.R.S.T. (a unit test checks one small piece of code, such as a function). Fast: they run quickly, or people avoid running them. Independent: tests do not depend on one another and run in any order. Repeatable: they run in any environment, even without a network. Self-validating: the outcome is pass or fail, not a log to interpret. Timely: written just before the production code. The fee function takes the holiday list as a parameter instead of calling the server itself, so its tests are fast and repeatable. To remember it: a good test is one you are happy to run every few seconds. [[src:book-cleancode]]')
    B(C, S_, 2, 'note', 'Test chạy trên JVM (trên máy tính), test trên thiết bị (chạy trên điện thoại hay máy ảo) và test giao diện ở Android được dạy theo tầng ở chương "Kiểm thử theo tầng" (G10) của track Kiến trúc; runTest cho coroutine ở chương "Trạng thái chung và kiểm thử coroutine" (A9) của track Coroutines. Chương này chỉ bàn nhịp viết test.',
      'JVM tests (on your computer), instrumented tests (on a phone or emulator) and UI tests on Android are taught by layer in the chapter "Testing by layer" (G10) of the Architecture track; runTest for coroutines in the chapter "Shared state and testing coroutines" (A9) of the Coroutines track. This chapter only covers the rhythm of writing tests.')
    B(C, S_, 2, 'kind', 'android')

    S_ = 'bugs'
    a(C + '.sec.%s.title' % S_, 'Hai lỗi hay gặp', 'Two common bugs')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'bug', 'Ngày Quốc khánh, bệnh nhân bị tính phí ngày thường, dù mọi test đều xanh.', 'On National Day patients are charged the weekday fee, though every test is green.')
    B(C, S_, 1, 'cause', 'Mã viết trước, test viết sau chỉ kiểm hai trường hợp người viết đã nghĩ tới; ngày lễ chưa bao giờ có trong danh sách nào.', 'The code came first, and the tests written afterwards check only the two cases the author had in mind; holidays were never on any list.')
    B(C, S_, 1, 'fix', 'Viết test tái hiện lỗi (2/9 → 400.000), thấy nó đỏ, rồi mới sửa. Lần sau, viết danh sách ví dụ trước khi viết mã.', 'Write a test reproducing the defect (2 Sep → 400,000), see it fail, then fix. Next time, write the example list before the code.')
    B(C, S_, 2, 'bug', 'Một test luôn xanh, kể cả khi mã fee bị sửa sai.', 'A test that is always green, even when fee is broken.')
    B(C, S_, 2, 'cause', 'Assertion so sánh kết quả với chính nó (assertEquals(fee(d), fee(d))), hoặc tính giá trị mong đợi bằng cùng công thức với mã. Test chưa bao giờ được thấy đỏ nên không ai phát hiện.', 'The assertion compares the result with itself (assertEquals(fee(d), fee(d))), or computes the expected value with the same formula as the code. The test was never seen failing, so nobody noticed.')
    B(C, S_, 2, 'fix', 'Viết giá trị mong đợi là hằng cụ thể (400_000). Khi sửa test, tạm phá mã sản phẩm để thấy test đỏ, rồi bỏ phần phá đi.', 'Write the expected value as a concrete constant (400_000). When editing a test, temporarily sabotage the production code to see it fail, then discard the sabotage.')

    S_ = 'ex'
    a(C + '.sec.%s.title' % S_, 'Bài tập', 'Exercise')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'ex', 'Phòng khám thêm quy định: trẻ dưới 6 tuổi được giảm 50% phí (áp sau quy tắc ngày). Viết danh sách ví dụ trước, rồi đi từng vòng đỏ, xanh, refactor. Ở mỗi vòng, viết ra một cài đặt "Devil\'s Advocate" vẫn qua mọi test hiện có.', 'The clinic adds a rule: children under 6 get 50% off (applied after the day rule). Write the example list first, then walk each red, green, refactor cycle. In each cycle, write down a "Devil\'s Advocate" implementation that still passes the current tests.')
    B(C, S_, 1, 'hint', 'Ví dụ nên chạm cả ranh giới tuổi (5 và 6 tuổi) và tổ hợp với cuối tuần, ngày lễ. Tuổi tính tại ngày khám, không phải hôm nay.', 'Examples should touch the age boundary (5 and 6) and combine with weekends and holidays. Age is computed on the visit date, not today.')
    B(C, S_, 1, 'sol', 'Danh sách: 5 tuổi thứ hai → 100.000; 6 tuổi thứ hai → 200.000; 5 tuổi thứ bảy → 150.000; 5 tuổi ngày lễ → 200.000; bé tròn 6 tuổi đúng ngày khám → 200.000. Vòng 1: test 5 tuổi đỏ; Devil\'s Advocate: if (age == 5) trả nửa giá. Vòng 2: test 6 tuổi chốt ranh giới, mã thành age < 6. Vòng 3–4: tổ hợp với cuối tuần, ngày lễ buộc giảm giá áp lên kết quả của quy tắc ngày, không áp lên BASE. Vòng 5: sinh nhật đúng ngày khám buộc tính tuổi theo ngày khám. Refactor: tách ageOn(visitDate).',
      'The list: age 5 on Monday → 100,000; age 6 on Monday → 200,000; age 5 on Saturday → 150,000; age 5 on a holiday → 200,000; turning 6 on the visit day → 200,000. Cycle 1: the age-5 test fails; Devil\'s Advocate: if (age == 5) charge half. Cycle 2: the age-6 test pins the boundary, the code becomes age < 6. Cycles 3–4: weekend and holiday combinations force the discount onto the day-rule result, not onto BASE. Cycle 5: a birthday on the visit day forces age to be computed on the visit date. Refactor: extract ageOn(visitDate).')
    B(C, S_, 1, 'solkt', 'fun fee(date: LocalDate, holidays: Set<LocalDate>, birth: LocalDate): Int {\n    val byDay = dayFee(date, holidays)\n    return if (ageOn(date, birth) < 6) byDay / 2 else byDay\n}\n\nprivate fun ageOn(date: LocalDate, birth: LocalDate) = Period.between(birth, date).years')

    for q, qv, qe, av, ae, wv, we in [
        ('q1', 'Theo luật thứ ba của Martin, khi test đang đỏ bạn được viết bao nhiêu mã?', 'Under Martin\'s third law, how much code may you write while a test fails?', 'Vừa đủ để test đó xanh.', 'Just enough to make that test pass.', 'Muốn mã tổng quát hơn thì phải có thêm test đỏ.', 'More general code needs another failing test.'),
        ('q2', 'Vì sao nên thấy test đỏ trước khi thấy nó xanh?', 'Why should you see a test fail before you see it pass?', 'Để biết test kiểm thật; test chưa từng đỏ có thể luôn đúng.', 'To know it really checks something; a test never seen failing may always pass.', 'Đừng tin test chưa từng thấy đỏ.', 'Do not trust a test you have not seen fail.'),
        ('q3', 'Mã trả hằng 200.000 qua test "thứ hai → 200.000". Nghĩa là gì?', 'Code returning the constant 200,000 passes the test "Monday → 200,000". What does that mean?', 'Danh sách test chưa đủ; cần thêm ví dụ (tam giác hóa).', 'The test list is not enough; add examples (triangulation).', 'Đó là Devil\'s Advocate của Seemann.', 'That is Seemann\'s Devil\'s Advocate.'),
        ('q4', 'Độ phủ dòng 100% có bảo đảm không thiếu trường hợp?', 'Does 100% line coverage guarantee no missing cases?', 'Không; nó chỉ đo những dòng đã có.', 'No; it only measures lines that exist.', 'Nhánh ngày lễ chưa được viết thì không có dòng nào để thiếu độ phủ.', 'If the holiday branch was never written, there is no line to be uncovered.')]:
        a(C + '.quiz.%s.q' % q, qv, qe); a(C + '.quiz.%s.a' % q, av, ae); a(C + '.quiz.%s.why' % q, wv, we)
