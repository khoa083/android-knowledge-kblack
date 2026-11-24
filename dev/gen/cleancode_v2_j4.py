# Mã sạch · J4: TDD (Phần 2: test và thay đổi an toàn)
# Nguồn: Martin, Clean Craftsmanship ch.2 (bản chất của TDD, ba luật "hoàn toàn tùy ý", luật thứ tư: refactor; red → green → refactor);
# Martin, Clean Code ch.9 (ba luật TDD, F.I.R.S.T.); Seemann, Code That Fits in Your Head 5.2.2 (Red Green Refactor, như phương pháp khoa học),
# 6.2.2 (Devil's Advocate, trích Martin "test càng cụ thể, mã càng tổng quát"), 6.2.5 (đủ test chưa là đánh giá rủi ro), 11.2 (đừng tin test
# chưa từng thấy đỏ), A.10, A.17. Đọc 2026-11-24, diễn đạt lại. Ngày trong ví dụ đã kiểm thứ: 23/11/2026 thứ hai, 28/11 thứ bảy, 29/11 chủ nhật,
# 2/9/2026 (Quốc khánh) thứ tư.

SEC_ORDER = {'j4': ['hook', 'laws', 'cycle', 'triangulate', 'first', 'bugs', 'ex', 'honest']}


def add(a):
    def B(ch, sec, n, field, vi, en=None):
        a('%s.sec.%s.b.%02d.%s' % (ch, sec, n, field), vi, vi if en is None else en)

    a('preset.tdd', 'Mã sạch · TDD cho phí khám', 'Clean code · TDD for the visit fee')
    m = lambda k, vi, en=None: a('m.tdd.' + k, vi, en)
    m('title', 'Viết mã rồi mới test, hay test trước từng ví dụ', 'Code first and test later, or test first, one example at a time')
    m('overview', 'Hàm fee(date) tính phí khám: ngày thường 200.000 đ, cuối tuần 300.000 đ, ngày lễ 400.000 đ. Cách thứ nhất: viết cả hàm theo trí nhớ, rồi viết vài test cho chắc. Cách thứ hai: TDD, mỗi vòng thêm một ví dụ vào danh sách test, thấy nó đỏ, viết vừa đủ mã cho xanh, rồi dọn mã.',
      'The fee(date) function computes the visit fee: 200,000 VND on weekdays, 300,000 on weekends, 400,000 on public holidays. First approach: write the whole function from memory, then add a few tests to be sure. Second approach: TDD, each cycle adds one example to the test list, sees it fail, writes just enough code to pass, then cleans up.')
    m('wrapup', 'Viết mã trước, test chỉ kiểm lại những gì người viết đã nghĩ tới: hai test xanh ngay lần đầu, không ai thấy chúng đỏ, và ngày lễ chưa bao giờ có trong đầu ai cho tới khi bệnh nhân bị tính sai vào ngày 2/9. Với TDD, danh sách ví dụ là nơi nghĩ về trường hợp biên trước khi viết mã; mỗi test được thấy đỏ trước khi xanh, nên ta biết nó kiểm thật; và mã chỉ trở nên tổng quát khi một ví dụ mới buộc nó phải như vậy.',
      'Writing code first, the tests only re-check what the author already thought of: two tests pass the first time, nobody sees them fail, and public holidays were never on anyone\'s mind until a patient was charged wrongly on 2 September. With TDD, the example list is where edge cases are thought about before code exists; every test is seen failing before it passes, so we know it really checks something; and the code becomes general only when a new example forces it to.')
    m('simp.1', 'Mức phí, danh sách ngày lễ và các ngày ví dụ là minh họa; danh sách ngày lễ giả định do server cấp. Một vòng TDD thật chỉ dài vài chục giây và có nhiều bước nhỏ hơn bốn bước ở đây.', 'The fees, the holiday list and the example dates are illustrative; the holiday list is assumed to come from the server. A real TDD cycle lasts tens of seconds and has many more, smaller steps than the four shown here.')
    m('simp.2', 'Ba luật và luật thứ tư là của Robert C. Martin; chính ông gọi ba luật là tùy ý, vì có cách khác đạt cùng mục tiêu. Red Green Refactor và Devil\'s Advocate theo Seemann.', 'The three laws and the fourth are Robert C. Martin\'s; he himself calls the three laws arbitrary, since other disciplines reach the same goals. Red Green Refactor and Devil\'s Advocate follow Seemann.')
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
        ('after.s2', 'Seemann (11.2): đừng tin một test chưa từng thấy nó đỏ. Assertion luôn đúng (tautological) dễ viết hơn ta tưởng; nếu chưa thấy test đỏ thì chưa biết nó có kiểm gì không. [[src:book-seemann]]', 'Seemann (11.2): do not trust a test you have not seen fail. Tautological assertions are surprisingly easy to write; until you have seen a test fail, you do not know whether it checks anything. [[src:book-seemann]]'),
        ('after.s3', 'Test viết sau mã thường đi theo đúng đường mã đã có. Danh sách ví dụ viết trước mã là chỗ để nghĩ tới trường hợp biên.', 'Tests written after the code tend to follow the paths the code already has. An example list written before the code is where edge cases get thought of.'),
        ('after.s4', 'Seemann (6.2.5): lỗi đã lọt ra môi trường thật chứng tỏ lỗi đó có thể xảy ra; hãy viết một test tái hiện nó trước khi sửa. [[src:book-seemann]]', 'Seemann (6.2.5): a defect that reached production proves that error can happen; write a test that reproduces it before fixing. [[src:book-seemann]]'),
        ('tdd.s1', 'Seemann (6.2.2) gọi đây là Devil\'s Advocate: cố tình viết cài đặt sai rõ ràng mà vẫn qua mọi test. Làm được thì danh sách test chưa đủ. [[src:book-seemann]]', 'Seemann (6.2.2) calls this the Devil\'s Advocate: deliberately write an obviously wrong implementation that still passes every test. If you can, the test list is not enough. [[src:book-seemann]]'),
        ('tdd.s2', 'Martin (Clean Craftsmanship ch.2): luật thứ ba, không viết nhiều mã hơn mức đủ cho test đang đỏ được xanh. [[src:book-craft]]', 'Martin (Clean Craftsmanship ch.2): the third law, write no more production code than resolves the currently failing test. [[src:book-craft]]'),
        ('tdd.s3', 'Martin (ch.2): luật thứ tư là refactor. Không thể vừa làm cho mã chạy vừa làm cho mã đẹp cùng lúc; theo lời khuyên của Kent Beck: trước làm cho chạy, rồi làm cho đúng. [[src:book-craft]]', 'Martin (ch.2): the fourth law is refactoring. You cannot make code work and make it well-structured at the same moment; following Kent Beck\'s advice: first make it work, then make it right. [[src:book-craft]]'),
        ('tdd.s4', 'Seemann (5.2.2) so Red Green Refactor với phương pháp khoa học: test đỏ là giả thuyết có thể bác bỏ, chạy test là thí nghiệm, so kết quả với dự đoán. [[src:book-seemann]]', 'Seemann (5.2.2) compares Red Green Refactor to the scientific method: the failing test is a falsifiable prediction, running it is the experiment, then compare the outcome with the prediction. [[src:book-seemann]]')]:
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
    z('td.tcap', 'Danh sách ví dụ thành test. Cột cuối: test đã từng đỏ chưa (Seemann: đừng tin test chưa từng thấy đỏ).', 'The example list as tests. Last column: has the test ever failed (Seemann: do not trust a test you have not seen fail).')
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
    a(C + '.essence', 'Ba luật TDD của Martin: không viết mã khi chưa có test đỏ; không viết test nhiều hơn mức đủ để đỏ; không viết mã nhiều hơn mức đủ để xanh. Luật thứ tư: refactor khi mọi test xanh.\nViết danh sách ví dụ trước mã: đó là lúc nghĩ tới trường hợp biên như ngày lễ. Mỗi test phải được thấy đỏ trước khi xanh, nếu không thì chưa biết nó có kiểm gì.\nTriangulation: nếu một cài đặt sai rõ ràng vẫn qua mọi test (Devil\'s Advocate), hãy thêm ví dụ. Test càng cụ thể, mã càng tổng quát.',
      'Martin\'s three laws of TDD: write no production code without a failing test; write no more test than is enough to fail; write no more code than is enough to pass. The fourth law: refactor while all tests are green.\nWrite the example list before the code: that is when edge cases like public holidays get thought of. Each test must be seen failing before it passes, or you do not know whether it checks anything.\nTriangulation: if an obviously wrong implementation still passes every test (Devil\'s Advocate), add an example. As the tests get more specific, the code gets more generic.')
    a(C + '.goal.g1', 'Đã thấy tam giác hóa ở ví dụ chủ nhật', 'Saw triangulation with the Sunday example')
    a(C + '.goal.g2', 'Đã thấy ngày 2/9', 'Saw 2 September')
    a(C + '.sim.cleancode.tdd', 'viết mã trước hay TDD', 'code first or TDD')

    S_ = 'hook'
    a(C + '.sec.%s.title' % S_, 'Đoán trước khi đọc', 'Predict before reading')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'predict', 'Hàm tính phí có hai test, cả hai xanh, độ phủ dòng gần 100%. Vậy mà ngày Quốc khánh bệnh nhân bị tính phí ngày thường. Vì sao test xanh và độ phủ cao vẫn không bắt được lỗi này?',
      'The fee function has two tests, both green, with nearly 100% line coverage. Yet on National Day patients are charged the weekday fee. Why did green tests and high coverage miss it?')
    B(C, S_, 1, 'ans', 'Vì lỗi không nằm ở dòng mã nào: nó là một nhánh chưa bao giờ được viết. Độ phủ chỉ đo những dòng đã có. Test viết sau mã thường kiểm lại đúng những gì người viết đã nghĩ, nên không thể tìm ra điều họ chưa nghĩ tới. Mô phỏng ngay dưới so cách đó với TDD, nơi danh sách ví dụ có trước mã.',
      'Because the bug is not on any line of code: it is a branch that was never written. Coverage measures only the lines that exist. Tests written after the code tend to re-check what the author already thought, so they cannot find what the author never thought of. The simulation just below compares that with TDD, where the example list comes before the code.')

    S_ = 'laws'
    a(C + '.sec.%s.title' % S_, 'Ba luật và luật thứ tư', 'The three laws and the fourth')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'p', 'Martin (Clean Craftsmanship ch.2, cũng có ở Clean Code ch.9) phát biểu ba luật. Một: không viết mã sản phẩm khi chưa có một test đỏ vì thiếu chính mã đó. Hai: không viết test nhiều hơn mức đủ để đỏ, và không biên dịch được cũng tính là đỏ. Ba: không viết mã sản phẩm nhiều hơn mức đủ cho test đang đỏ được xanh. Ba luật khóa người viết vào một vòng chỉ dài vài giây, chuyển qua lại giữa test và mã. [[src:book-craft]] [[src:book-cleancode]]',
      'Martin (Clean Craftsmanship ch.2, also in Clean Code ch.9) states three laws. One: write no production code until you have a test that fails for lack of that code. Two: write no more of a test than is enough to fail, and failing to compile counts as failing. Three: write no more production code than resolves the currently failing test. The three laws lock you into a cycle a few seconds long, switching between test and code. [[src:book-craft]] [[src:book-cleancode]]')
    B(C, S_, 2, 'p', 'Ông thêm luật thứ tư: refactor. Tập trung viết test cho đỏ thì test khó đẹp; tập trung cho xanh thì mã khó đẹp; nên sau mỗi lần xanh, dọn mã ngay, khi mọi test vẫn xanh. Refactor là việc liên tục, không lên lịch, không xin phép. Ông cũng nói thẳng ba luật là tùy ý: điều cốt lõi là bộ test đủ tin để test qua nghĩa là triển khai được, mã đủ tách để test được, và một vòng phản hồi rất ngắn; cách làm khác của Kent Beck (test && commit || revert) cũng đạt được những điều đó. [[src:book-craft]]',
      'He adds a fourth law: refactor. Focused on making a test fail, the test is rarely well written; focused on making it pass, the code is rarely well written; so after each pass, clean up at once, while all tests stay green. Refactoring is continuous, never scheduled, never asked permission for. He also says plainly the three laws are arbitrary: the essence is a test suite trusted enough that passing means deployable, code decoupled enough to test, and a very short feedback loop; Kent Beck\'s different discipline (test && commit || revert) reaches the same goals. [[src:book-craft]]')

    S_ = 'cycle'
    a(C + '.sec.%s.title' % S_, 'Đỏ, xanh, refactor', 'Red, green, refactor')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'p', 'Seemann (5.2.2, A.17) mô tả vòng Red Green Refactor như một checklist: viết một test đỏ; thay đổi tối thiểu để mọi test xanh; cải thiện mã mà không đổi hành vi; rồi bắt đầu lại. Ông so nó với phương pháp khoa học: test đỏ là một dự đoán có thể sai, chạy test là thí nghiệm. Test chưa từng đỏ là thí nghiệm không thể thất bại, nên không chứng minh được gì (11.2). [[src:book-seemann]]',
      'Seemann (5.2.2, A.17) describes Red Green Refactor as a checklist: write a failing test; make the minimal change so all tests pass; improve the code without changing behaviour; start over. He compares it to the scientific method: a failing test is a prediction that can be wrong, running it is the experiment. A test that has never failed is an experiment that cannot fail, so it proves nothing (11.2). [[src:book-seemann]]')
    B(C, S_, 2, 'kt', '@Test fun `ngày lễ tính 400 nghìn`() {\n    val holidays = setOf(LocalDate.of(2026, 9, 2))\n    assertEquals(400_000, fee(LocalDate.of(2026, 9, 2), holidays))   // đỏ trước, rồi mới xanh\n}',
      '@Test fun `holiday costs 400 thousand`() {\n    val holidays = setOf(LocalDate.of(2026, 9, 2))\n    assertEquals(400_000, fee(LocalDate.of(2026, 9, 2), holidays))   // red first, then green\n}')
    B(C, S_, 3, 'note', 'Tên test có khoảng trắng trong dấu backtick là quy ước Kotlin chỉ dành cho test; theo tài liệu quy ước, Android runtime chỉ hỗ trợ tên như vậy từ API 30, nên dùng cho test chạy trên JVM. [[src:kt-conventions]]',
      'Test names with spaces in backticks are a Kotlin convention for tests only; per the conventions page, the Android runtime supports such names only from API 30, so use them for tests that run on the JVM. [[src:kt-conventions]]')
    B(C, S_, 3, 'kind', 'android')

    S_ = 'triangulate'
    a(C + '.sec.%s.title' % S_, 'Tam giác hóa và Devil\'s Advocate', 'Triangulation and the Devil\'s Advocate')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'p', 'Làm sao biết đã đủ ví dụ? Seemann (6.2.2) đề xuất Devil\'s Advocate: cố tình viết một cài đặt sai rõ ràng mà vẫn qua mọi test, như trả về hằng 200.000 hay chỉ kiểm thứ bảy. Nếu làm được, danh sách test còn thiếu; thêm một ví dụ buộc mã phải tổng quát hơn. Ông trích Martin: test càng cụ thể, mã càng tổng quát. Đó là tam giác hóa: hai, ba điểm ví dụ chốt được một quy tắc. [[src:book-seemann]]',
      'How do you know you have enough examples? Seemann (6.2.2) proposes the Devil\'s Advocate: deliberately write an obviously wrong implementation that still passes every test, such as returning the constant 200,000 or checking only Saturday. If you can, the test list is short; add one example that forces more general code. He quotes Martin: as the tests get more specific, the code gets more generic. That is triangulation: two or three example points pin down a rule. [[src:book-seemann]]')
    B(C, S_, 2, 'p', 'Seemann (6.2.5) thừa nhận không có câu trả lời định lượng cho "đủ test chưa": đó là đánh giá rủi ro, cân xác suất một lỗi xảy ra với hậu quả của nó. Một lỗi đã lọt ra môi trường thật chứng tỏ nó có thể xảy ra, nên luôn viết một test tái hiện nó. [[src:book-seemann]]',
      'Seemann (6.2.5) admits there is no quantitative answer to "do I have enough tests": it is risk assessment, weighing the probability of a defect against its impact. A defect that reached production proves it can happen, so always write a test that reproduces it. [[src:book-seemann]]')

    S_ = 'first'
    a(C + '.sec.%s.title' % S_, 'Test sạch: F.I.R.S.T.', 'Clean tests: F.I.R.S.T.')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'p', 'Martin (Clean Code ch.9) tóm tắt năm tính chất của unit test sạch. Fast: chạy nhanh, nếu chậm người ta sẽ ngại chạy. Independent: test không phụ thuộc nhau, chạy theo thứ tự nào cũng được. Repeatable: chạy được ở mọi môi trường, kể cả không có mạng. Self-validating: kết quả là đạt hay không đạt, không phải đọc log để đoán. Timely: viết ngay trước mã sản phẩm. Hàm fee nhận danh sách ngày lễ làm tham số thay vì tự gọi server, nên test của nó vừa nhanh vừa lặp lại được. [[src:book-cleancode]]',
      'Martin (Clean Code ch.9) sums up five qualities of clean unit tests. Fast: they run quickly, or people avoid running them. Independent: tests do not depend on one another and run in any order. Repeatable: they run in any environment, even without a network. Self-validating: the outcome is pass or fail, not a log to interpret. Timely: written just before the production code. The fee function takes the holiday list as a parameter instead of calling the server itself, so its tests are fast and repeatable. [[src:book-cleancode]]')
    B(C, S_, 2, 'note', 'Test chạy trên JVM, có thiết bị và test giao diện ở Android được dạy theo tầng ở track Kiến trúc (G10); runTest cho coroutine ở track Coroutines (A9). Chương này chỉ bàn nhịp viết test.',
      'JVM, instrumented and UI tests on Android are taught by layer in the Architecture track (G10); runTest for coroutines in the Coroutines track (A9). This chapter only covers the rhythm of writing tests.')
    B(C, S_, 2, 'kind', 'android')

    S_ = 'bugs'
    a(C + '.sec.%s.title' % S_, 'Hai lỗi hay gặp', 'Two common bugs')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'bug', 'Ngày Quốc khánh, bệnh nhân bị tính phí ngày thường, dù mọi test đều xanh.', 'On National Day patients are charged the weekday fee, though every test is green.')
    B(C, S_, 1, 'cause', 'Mã viết trước, test viết sau chỉ kiểm hai trường hợp người viết đã nghĩ tới; ngày lễ chưa bao giờ có trong danh sách nào.', 'The code came first, and the tests written afterwards check only the two cases the author had in mind; holidays were never on any list.')
    B(C, S_, 1, 'fix', 'Viết test tái hiện lỗi (2/9 → 400.000), thấy nó đỏ, rồi mới sửa. Lần sau, viết danh sách ví dụ trước khi viết mã.', 'Write a test reproducing the defect (2 Sep → 400,000), see it fail, then fix. Next time, write the example list before the code.')
    B(C, S_, 2, 'bug', 'Một test luôn xanh, kể cả khi mã fee bị sửa sai.', 'A test that is always green, even when fee is broken.')
    B(C, S_, 2, 'cause', 'Assertion so sánh kết quả với chính nó (assertEquals(fee(d), fee(d))), hoặc tính giá trị mong đợi bằng cùng công thức với mã. Test chưa bao giờ được thấy đỏ nên không ai phát hiện.', 'The assertion compares the result with itself (assertEquals(fee(d), fee(d))), or computes the expected value with the same formula as the code. The test was never seen failing, so nobody noticed.')
    B(C, S_, 2, 'fix', 'Viết giá trị mong đợi là hằng cụ thể (400_000). Khi sửa test, tạm phá mã sản phẩm để thấy test đỏ, rồi bỏ phần phá đi (Seemann 11.2).', 'Write the expected value as a concrete constant (400_000). When editing a test, temporarily sabotage the production code to see it fail, then discard the sabotage (Seemann 11.2).')

    S_ = 'ex'
    a(C + '.sec.%s.title' % S_, 'Bài tập', 'Exercise')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'ex', 'Phòng khám thêm quy định: trẻ dưới 6 tuổi được giảm 50% phí (áp sau quy tắc ngày). Viết danh sách ví dụ trước, rồi đi từng vòng đỏ, xanh, refactor. Ở mỗi vòng, viết ra một cài đặt "Devil\'s Advocate" vẫn qua mọi test hiện có.', 'The clinic adds a rule: children under 6 get 50% off (applied after the day rule). Write the example list first, then walk each red, green, refactor cycle. In each cycle, write down a "Devil\'s Advocate" implementation that still passes the current tests.')
    B(C, S_, 1, 'hint', 'Ví dụ nên chạm cả ranh giới tuổi (5 và 6 tuổi) và tổ hợp với cuối tuần, ngày lễ. Tuổi tính tại ngày khám, không phải hôm nay.', 'Examples should touch the age boundary (5 and 6) and combine with weekends and holidays. Age is computed on the visit date, not today.')
    B(C, S_, 1, 'sol', 'Danh sách: 5 tuổi thứ hai → 100.000; 6 tuổi thứ hai → 200.000; 5 tuổi thứ bảy → 150.000; 5 tuổi ngày lễ → 200.000; bé tròn 6 tuổi đúng ngày khám → 200.000. Vòng 1: test 5 tuổi đỏ; Devil\'s Advocate: if (age == 5) trả nửa giá. Vòng 2: test 6 tuổi chốt ranh giới, mã thành age < 6. Vòng 3–4: tổ hợp với cuối tuần, ngày lễ buộc giảm giá áp lên kết quả của quy tắc ngày, không áp lên BASE. Vòng 5: sinh nhật đúng ngày khám buộc tính tuổi theo ngày khám. Refactor: tách ageOn(visitDate).',
      'The list: age 5 on Monday → 100,000; age 6 on Monday → 200,000; age 5 on Saturday → 150,000; age 5 on a holiday → 200,000; turning 6 on the visit day → 200,000. Cycle 1: the age-5 test fails; Devil\'s Advocate: if (age == 5) charge half. Cycle 2: the age-6 test pins the boundary, the code becomes age < 6. Cycles 3–4: weekend and holiday combinations force the discount onto the day-rule result, not onto BASE. Cycle 5: a birthday on the visit day forces age to be computed on the visit date. Refactor: extract ageOn(visitDate).')
    B(C, S_, 1, 'solkt', 'fun fee(date: LocalDate, holidays: Set<LocalDate>, birth: LocalDate): Int {\n    val byDay = dayFee(date, holidays)\n    return if (ageOn(date, birth) < 6) byDay / 2 else byDay\n}\n\nprivate fun ageOn(date: LocalDate, birth: LocalDate) = Period.between(birth, date).years')

    S_ = 'honest'
    a(C + '.sec.%s.title' % S_, 'Chương này giản lược những gì', 'What this chapter simplifies')
    a(C + '.sec.%s.badge' % S_, 'simplified')
    B(C, S_, 1, 'p', 'Ba luật, luật thứ tư và bản chất của TDD theo Robert C. Martin, Clean Craftsmanship ch.2; ba luật và F.I.R.S.T. cũng theo Clean Code ch.9; Red Green Refactor, Devil\'s Advocate, đủ test chưa, đừng tin test chưa thấy đỏ theo Mark Seemann, Code That Fits in Your Head 5.2.2, 6.2.2, 6.2.5, 11.2. Đọc ngày 2026-11-24, diễn đạt lại; ví dụ viết lại bằng Kotlin. TDD là một kỷ luật do các tác giả đề xuất, có người dùng và có người không; chính Martin gọi ba luật là tùy ý. Chương không đưa số liệu nghiên cứu về hiệu quả của TDD vì site chưa đọc nghiên cứu nào. Mức phí, ngày lễ và mọi con số là minh họa của site.',
      'The three laws, the fourth law and the essence of TDD follow Robert C. Martin, Clean Craftsmanship ch.2; the three laws and F.I.R.S.T. also follow Clean Code ch.9; Red Green Refactor, the Devil\'s Advocate, having enough tests and not trusting a test never seen failing follow Mark Seemann, Code That Fits in Your Head 5.2.2, 6.2.2, 6.2.5, 11.2. Read on 2026-11-24 and paraphrased; examples rewritten in Kotlin. TDD is a discipline its authors advocate, practised by some and not by others; Martin himself calls the three laws arbitrary. The chapter cites no research on TDD\'s effectiveness because the site has not read any. Fees, holidays and every number are the site\'s illustration.')

    for q, qv, qe, av, ae, wv, we in [
        ('q1', 'Theo luật thứ ba của Martin, khi test đang đỏ bạn được viết bao nhiêu mã?', 'Under Martin\'s third law, how much code may you write while a test fails?', 'Vừa đủ để test đó xanh.', 'Just enough to make that test pass.', 'Muốn mã tổng quát hơn thì phải có thêm test đỏ.', 'More general code needs another failing test.'),
        ('q2', 'Vì sao nên thấy test đỏ trước khi thấy nó xanh?', 'Why should you see a test fail before you see it pass?', 'Để biết test kiểm thật; test chưa từng đỏ có thể luôn đúng.', 'To know it really checks something; a test never seen failing may always pass.', 'Seemann 11.2: đừng tin test chưa từng thấy đỏ.', 'Seemann 11.2: do not trust a test you have not seen fail.'),
        ('q3', 'Mã trả hằng 200.000 qua test "thứ hai → 200.000". Nghĩa là gì?', 'Code returning the constant 200,000 passes the test "Monday → 200,000". What does that mean?', 'Danh sách test chưa đủ; cần thêm ví dụ (tam giác hóa).', 'The test list is not enough; add examples (triangulation).', 'Đó là Devil\'s Advocate của Seemann.', 'That is Seemann\'s Devil\'s Advocate.'),
        ('q4', 'Độ phủ dòng 100% có bảo đảm không thiếu trường hợp?', 'Does 100% line coverage guarantee no missing cases?', 'Không; nó chỉ đo những dòng đã có.', 'No; it only measures lines that exist.', 'Nhánh ngày lễ chưa được viết thì không có dòng nào để thiếu độ phủ.', 'If the holiday branch was never written, there is no line to be uncovered.')]:
        a(C + '.quiz.%s.q' % q, qv, qe); a(C + '.quiz.%s.a' % q, av, ae); a(C + '.quiz.%s.why' % q, wv, we)
