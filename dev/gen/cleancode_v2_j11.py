# Mã sạch · J11: tính chuyên nghiệp (Phần 4: làm nghề)
# Nguồn: Martin, The Clean Coder ch.2 (nói không; "cố" là cam kết; không có chuyện "cố"), ch.3 (nói có: cam kết thật), ch.10 (ước lượng khác cam kết;
# PERT: ước lượng ba điểm O, N, P; μ = (O + 4N + P)/6, σ = (P − O)/6; chuỗi việc: μ cộng thẳng, σ là căn của tổng bình phương; hy vọng là thứ giết dự án),
# ch.11 (áp lực: tránh bằng cách quản lý cam kết; khi đã có: đừng hoảng, trao đổi, dựa vào kỷ luật, nhờ người làm cặp); Clean Agile ch.5 (chỉ nhắc).
# Đọc 2026-11-24, diễn đạt lại. Ví dụ ba việc của app Hẹn Khám và mọi con số là của site; phép tính kiểm bằng code.

SEC_ORDER = {'j11': ['hook', 'estimate', 'pert', 'no', 'pressure', 'bugs', 'ex']}


def add(a):
    def B(ch, sec, n, field, vi, en=None):
        a('%s.sec.%s.b.%02d.%s' % (ch, sec, n, field), vi, vi if en is None else en)

    a('preset.estimate', 'Mã sạch · ước lượng ba điểm', 'Clean code · three-point estimates')
    m = lambda k, vi, en=None: a('m.estimate.' + k, vi, en)
    m('title', 'Hứa "em cố" một con số, hay ước lượng ba điểm', 'Promising "I\'ll try" one number, or a three-point estimate')
    m('overview', 'Quản lý hỏi: ba việc (thanh toán MoMo, hủy lịch có hoàn tiền, nhắc lịch theo múi giờ) có xong trong 6 ngày, kịp hội chợ y tế không? Cách thứ nhất: đáp "em cố", tức một con số đầy hy vọng. Cách thứ hai: cho mỗi việc ba con số theo PERT, cộng lại thành khoảng có xác suất, và nói không với 6 ngày.',
      'The manager asks: can three tasks (MoMo payments, cancelling with refunds, time-zone reminders) be done in 6 days, in time for the health fair? First approach: answer "I\'ll try", one hopeful number. Second: give each task three numbers per PERT, combine them into a range with probabilities, and say no to 6 days.')
    m('wrapup', '"Em cố" là một cam kết ngầm: tới ngày thứ 4 đã trễ, nên bỏ viết test và làm đêm; xong sau 10,5 ngày thay vì 6, kèm 2 lỗi lọt ra. Ước lượng ba điểm cho μ ≈ 10,2 ngày và σ ≈ 2,2: rất có thể xong trong khoảng 10 ngày, có thể tới 12,4 (μ + σ), hiếm khi quá 14,6 (μ + 2σ). Quản lý biết từ đầu 6 ngày là không thể, nên chọn dời hội chợ sang bản sau và lên kế hoạch 12 ngày; nhóm xong sau 10,5 ngày, giữ nguyên kỷ luật, không lỗi nào lọt.',
      '"I\'ll try" is an implied commitment: by day 4 the work is late, so tests are skipped and nights are long; it ends after 10.5 days instead of 6, with 2 defects shipped. The three-point estimate gives μ ≈ 10.2 days and σ ≈ 2.2: very likely about 10 days, possibly 12.4 (μ + σ), rarely beyond 14.6 (μ + 2σ). The manager knows from the start that 6 days is impossible, moves the fair demo to a later release and plans 12 days; the team finishes in 10.5, disciplines intact, no defects shipped.')
    m('simp.1', 'Ba việc, các ước lượng, 10,5 ngày thực tế và 2 lỗi là minh họa. Phép tính PERT chỉ hợp lý khi O và P thật sự hiếm (dưới 1% khả năng xảy ra).', 'The three tasks, their estimates, the actual 10.5 days and the 2 defects are illustrative. The PERT arithmetic only works when O and P are truly unlikely (well under a 1% chance).')
    m('simp.2', 'Các ý về nói không, "cố", ước lượng và áp lực là quan điểm của Robert C. Martin về hành xử nghề nghiệp, không phải quy định. Nơi làm việc thật có quyền lực và ràng buộc mà một chương không giải quyết được.', 'The points on saying no, "trying", estimates and pressure are Robert C. Martin\'s view of professional conduct, not regulations. Real workplaces have power dynamics and constraints one chapter cannot solve.')
    m('ctl.hint', 'Đổi cách trả lời rồi đi lại; so dòng thước ngày: ngày hứa, ngày thật, và khoảng μ, μ + σ, μ + 2σ.', 'Switch the answer and walk again; compare the day ruler: the promised day, the actual day, and μ, μ + σ, μ + 2σ.')
    m('ctl.case', 'Cách trả lời', 'Answer')
    for k, vi, en in [('promise', '"em cố" 6 ngày', '"I\'ll try" for 6 days'), ('pert', 'ước lượng ba điểm', 'three-point estimate')]:
        m('ctl.case.' + k, vi, en)
    m('diagramTitle', 'Yêu cầu, ước lượng, cam kết, kết quả', 'Request, estimate, commitment, outcome')
    m('diagramDesc', 'Yêu cầu có hạn; ước lượng thành cam kết (hay không); kết quả so với cam kết', 'A request with a deadline; the estimate becomes a commitment (or not); the outcome against the commitment')
    for k, vi, en in [('ask', 'Yêu cầu: 6 ngày?', 'Request: 6 days?'), ('est', 'Ước lượng', 'Estimate'), ('commit', 'Cam kết', 'Commitment'), ('done', 'Kết quả', 'Outcome')]:
        m('n.' + k, vi, en)
    m('met.promised', 'Ngày đã hứa hay đã lên kế hoạch', 'Days promised or planned'); m('met.actual', 'Ngày làm thật', 'Actual days'); m('met.bugs', 'Lỗi lọt ra vì bỏ test', 'Defects shipped from skipped tests')
    a('cap.estimate', 'Yêu cầu đi qua ước lượng thành cam kết rồi tới kết quả. Nút đỏ: nơi cam kết không dựa trên ước lượng, hay kết quả trễ cam kết.', 'The request goes through an estimate into a commitment, then an outcome. Red node: where a commitment is not based on an estimate, or the outcome misses it.')
    S = [
        ('promise', 's1', 'Quản lý hỏi: ba việc trong 6 ngày?', 'The manager asks: three tasks in 6 days?',
         'Hội chợ y tế còn 6 ngày; quản lý muốn có MoMo, hủy lịch hoàn tiền và nhắc lịch theo múi giờ để trình diễn.', 'The health fair is in 6 days; the manager wants MoMo, refunding cancellations and time-zone reminders to demo.'),
        ('promise', 's2', '"Em cố"', '"I\'ll try"',
         'Không muốn làm ai thất vọng, lập trình viên đáp sẽ cố. Quản lý ghi vào kế hoạch: 6 ngày. Một câu "cố" đã thành cam kết.', 'Not wanting to disappoint, the developer says they will try. The manager writes 6 days into the plan. "Try" has become a commitment.'),
        ('promise', 's3', 'Ngày 4: trễ, bỏ test, làm đêm', 'Day 4: late, tests skipped, long nights',
         'MoMo mới xong một nửa. Để kịp, test bị bỏ qua và nhóm làm cả cuối tuần. Không ai báo trước là sẽ trễ.', 'MoMo is only half done. To catch up, tests are skipped and the team works the weekend. Nobody warns that it will be late.'),
        ('promise', 's4', 'Xong sau 10,5 ngày, 2 lỗi lọt ra', 'Done after 10.5 days, 2 defects shipped',
         'Trễ 4,5 ngày so với lời hứa, hội chợ đã qua, và hai lỗi từ phần không có test tới tay bệnh nhân.', '4.5 days past the promise, the fair is over, and two defects from the untested code reach patients.'),
        ('pert', 's1', 'Quản lý hỏi: ba việc trong 6 ngày?', 'The manager asks: three tasks in 6 days?',
         'Cùng yêu cầu. Lần này lập trình viên xin vài phút để ước lượng từng việc bằng ba con số.', 'The same request. This time the developer asks for a few minutes to estimate each task with three numbers.'),
        ('pert', 's2', 'Ba con số cho mỗi việc', 'Three numbers per task',
         'MoMo: 1, 3, 12 ngày. Hủy lịch: 2, 3, 8. Nhắc lịch: 1, 2, 5. Tính μ và σ cho từng việc, rồi gộp lại (μ cộng thẳng, σ lấy căn tổng bình phương): μ ≈ 10,2 ngày, σ ≈ 2,2.', 'MoMo: 1, 3, 12 days. Cancelling: 2, 3, 8. Reminders: 1, 2, 5. Compute μ and σ per task, then combine (μ adds up, σ is the square root of the sum of squares): μ ≈ 10.2 days, σ ≈ 2.2.'),
        ('pert', 's3', 'Nói không với 6 ngày, đưa ra lựa chọn', 'Say no to 6 days, offer options',
         '"Sáu ngày là gần như không thể. Có thể trình diễn hủy lịch và nhắc lịch (khoảng 6 ngày), hoặc cả ba trong khoảng 12 ngày." Quản lý chọn dời hội chợ sang bản sau, kế hoạch 12 ngày.', '"Six days is close to impossible. We can demo cancelling and reminders (about 6 days), or all three in about 12." The manager moves the fair demo to a later release and plans 12 days.'),
        ('pert', 's4', 'Xong sau 10,5 ngày, trong kế hoạch', 'Done after 10.5 days, within plan',
         'Cùng khối lượng việc, cùng 10,5 ngày thật. Khác biệt: không ai bị bất ngờ, test vẫn viết đủ, không lỗi nào lọt.', 'The same work, the same actual 10.5 days. The difference: nobody is surprised, tests are still written, no defects ship.'),
    ]
    for case, k, tv, te, xv, xe in S:
        sid = case + '.' + k
        m('s.%s.title' % sid, tv, te); m('s.%s.explain' % sid, xv, xe); m('ev.' + sid, tv, te)
    for k, vi, en in [
        ('try', 'Theo thước ngày ở dưới bảng: vạch hứa, vạch thật, và khoảng ước lượng.', 'Follow the day ruler under the table: the promise mark, the actual mark, and the estimated range.'),
        ('promise.s2', 'Theo Martin, đồng ý "cố" là đồng ý thành công. Cố nghĩa là gì: làm thêm giờ, cuối tuần? Không có kế hoạch nào khác thì "cố" chỉ là cam kết ngầm. [[src:book-coder]]', 'According to Martin, agreeing to try is agreeing to succeed. What does trying mean: overtime, weekends? Without any different plan, "trying" is just an implied commitment. [[src:book-coder]]'),
        ('promise.s3', 'Martin khuyên: khi áp lực tới, đừng bỏ kỷ luật; đó chính là lúc cần chúng nhất. Theo TDD thì viết test nhiều hơn, không ít đi. Và báo sớm: bất ngờ nhân áp lực lên gấp bội. [[src:book-coder]]', 'Martin advises: under pressure, do not abandon your disciplines; that is exactly when you need them most. If you follow TDD, write more tests, not fewer. And warn early: surprises multiply pressure. [[src:book-coder]]'),
        ('promise.s4', 'Martin gọi hy vọng là thứ giết dự án: nó phá lịch và hủy uy tín. Nếu ước lượng thường gặp là 12 ngày mà hạn là 10, bạn sẽ không kịp; đừng để ai giữ hy vọng sai. [[src:book-coder]]', 'Martin calls hope the project killer: it destroys schedules and ruins reputations. If your nominal estimate is 12 days and the deadline is 10, you will not make it; do not let anyone keep false hope. [[src:book-coder]]'),
        ('pert.s1', 'Theo Martin, người chuyên nghiệp phân biệt rõ ước lượng với cam kết; họ chỉ cam kết khi biết chắc sẽ làm được, và tránh mọi cam kết ngầm. [[src:book-coder]]', 'According to Martin, professionals distinguish clearly between estimates and commitments; they commit only when they know they will succeed, and avoid implied commitments. [[src:book-coder]]'),
        ('pert.s2', 'PERT (ra đời năm 1957 cho dự án tàu ngầm Polaris): O lạc quan, N thường gặp nhất, P bi quan. μ = (O + 4N + P) / 6, σ = (P − O) / 6. Chuỗi việc: μ cộng thẳng, σ là căn của tổng bình phương. [[src:book-coder]]', 'PERT (created in 1957 for the Polaris submarine project): O optimistic, N nominal (most likely), P pessimistic. μ = (O + 4N + P) / 6, σ = (P − O) / 6. For a sequence: μ adds up, σ is the square root of the sum of squares. [[src:book-coder]]'),
        ('pert.s3', 'Theo Martin, người chuyên nghiệp nói không khi câu trả lời thật là không, và cùng quản lý tìm phương án tốt nhất; nói có một điều biết là không thể thì không giúp ai. [[src:book-coder]]', 'According to Martin, professionals say no when the real answer is no, and work with managers on the best alternative; saying yes to something known to be impossible helps nobody. [[src:book-coder]]'),
        ('pert.s4', 'Khối lượng việc không đổi giữa hai cách; cái đổi là thông tin quản lý có để lên kế hoạch, và việc kỷ luật được giữ.', 'The amount of work is the same in both; what changes is the information the manager has to plan with, and whether discipline holds.')]:
        m('co.' + k, vi, en)

    z = lambda k, vi, en=None: a('vz.' + k, vi, en)
    z('tab.estimate', 'Bảng PERT và thước ngày', 'PERT table and day ruler')
    z('es.cap', 'Bảng tính kiểm chứng: μ = (O + 4N + P) / 6, σ = (P − O) / 6; hàng tổng cộng μ thẳng và lấy căn tổng bình phương của σ.', 'The worked table: μ = (O + 4N + P) / 6, σ = (P − O) / 6; the total row adds μ and takes the square root of the sum of σ squared.')
    for k, vi, en in [('task', 'Việc', 'Task'), ('o', 'O', 'O'), ('n', 'N', 'N'), ('p', 'P', 'P'), ('mu', 'μ (ngày)', 'μ (days)'), ('sd', 'σ (ngày)', 'σ (days)')]:
        z('es.col.' + k, vi, en)
    for k, vi, en in [('momo', 'thanh toán MoMo', 'MoMo payments'), ('cancel', 'hủy lịch có hoàn tiền', 'cancel with refund'), ('remind', 'nhắc lịch theo múi giờ', 'time-zone reminders'), ('total', 'cả ba, nối tiếp', 'all three, in sequence')]:
        z('es.t.' + k, vi, en)
    z('es.nocalc', '"em cố": không có con số nào', '"I\'ll try": no numbers at all')
    z('es.rcap', 'Thước ngày (0 tới 16). Mỗi ô là một ngày.', 'Day ruler (0 to 16). Each cell is one day.')
    for k, vi, en in [('ask', 'hạn hỏi', 'asked'), ('plan', 'kế hoạch', 'plan'), ('mu', 'μ', 'μ'), ('s1', 'μ+σ', 'μ+σ'), ('s2', 'μ+2σ', 'μ+2σ'), ('done', 'xong thật', 'actually done'), ('crunch', 'trễ, bỏ test', 'late, tests skipped')]:
        z('es.mk.' + k, vi, en)
    z('es.days', '{n} ngày', '{n} days')
    z('es.legend', 'Ô xanh: khoảng ước lượng từ μ tới μ + 2σ. Ô gạch đỏ: lời hứa không dựa trên ước lượng, hay ngày bỏ test. Viền đậm: ngày xong thật. "?": chưa tới bước đó.', 'Green: the estimated range from μ to μ + 2σ. Red hatched: a promise not based on an estimate, or the day tests were skipped. Bold outline: the actual finish. "?": that step has not come yet.')

    C = 'j11'
    a(C + '.title', 'Tính chuyên nghiệp: ước lượng, nói không, giữ kỷ luật', 'Professionalism: estimates, saying no, keeping discipline')
    a(C + '.essence', 'Ước lượng không phải cam kết. Ước lượng là một phỏng đoán có xác suất (một phân bố xác suất: khả năng xong sớm, đúng hạn hay trễ); cam kết là lời hứa chỉ đưa ra khi biết chắc làm được. "Em cố" là một cam kết ngầm (lời hứa không nói ra nhưng người nghe hiểu là hứa).\nPERT là cách ước lượng ba điểm: mỗi việc ba con số, O lạc quan, N thường gặp nhất, P bi quan. μ (đọc "muy", thời gian kỳ vọng) = (O + 4N + P) / 6; σ (đọc "xích-ma", độ bất định) = (P − O) / 6. Với chuỗi việc nối tiếp, μ cộng thẳng, còn σ lấy căn của tổng bình phương (ví dụ σ là 3 và 4 thì cả chuỗi là √(9 + 16) = 5). Nói cho quản lý cả khoảng (μ, μ + σ, μ + 2σ) để họ lên kế hoạch.\nKhi câu trả lời thật là không, nói không và cùng tìm phương án. Khi áp lực tới, đừng bỏ test (TDD: viết test trước) hay refactor (sắp xếp lại mã): đó là lúc kỷ luật cần nhất; báo sớm và nhờ người làm cặp (hai người cùng làm một việc).',
      'An estimate is not a commitment. An estimate is a guess with probabilities (a probability distribution: the chance of finishing early, on time or late); a commitment is a promise made only when you know you will succeed. "I\'ll try" is an implied commitment (a promise nobody says aloud but the listener hears as a promise).\nPERT is a three-point estimate: three numbers per task, O optimistic, N nominal (most likely), P pessimistic. μ (pronounced "mu", the expected duration) = (O + 4N + P) / 6; σ ("sigma", the uncertainty) = (P − O) / 6. For tasks in sequence, μ adds up and σ is the square root of the sum of squares (for example σ of 3 and 4 gives √(9 + 16) = 5 for the sequence). Give the manager the whole range (μ, μ + σ, μ + 2σ) to plan with.\nWhen the real answer is no, say no and look for alternatives together. Under pressure, do not drop tests (TDD: writing the test first) or refactoring (rearranging code): that is when discipline matters most; warn early and pair up (two people working on one task).')
    a(C + '.goal.g1', 'Đã thấy bảng PERT hay lời "em cố"', 'Saw the PERT table or the "I\'ll try"')
    a(C + '.goal.g2', 'Đã thấy kết quả trên thước ngày', 'Saw the outcome on the day ruler')
    a(C + '.sim.cleancode.estimate', 'hứa "em cố" hay ước lượng ba điểm', '"I\'ll try" or a three-point estimate')

    S_ = 'hook'
    a(C + '.sec.%s.title' % S_, 'Đoán trước khi đọc', 'Predict before reading')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'predict', 'Quản lý hỏi: "Mai xong được không?". Bạn nghĩ nếu mọi thứ suôn sẻ thì được, và đáp "em cố". Tối mai còn dở dang, bạn bỏ viết test để kịp. Điều gì đã sai trước cả khi bạn bắt đầu viết mã?',
      'The manager asks: "Can it be done by tomorrow?". You think it can if everything goes smoothly, and answer "I\'ll try". Tomorrow evening it is half done and you skip the tests to make it. What went wrong before you even started coding?')
    B(C, S_, 1, 'ans', 'Con số "mai" là ước lượng lạc quan nhất, nhưng đã được nói ra như một cam kết. Quản lý nghe "cố" là "được". Lẽ ra phải đưa ra khoảng: thường thì bao lâu, xấu thì bao lâu, và nói rõ đó là ước lượng. Mô phỏng ngay dưới so hai cách trả lời cho cùng ba việc.',
      'The number "tomorrow" was the most optimistic estimate, yet it was voiced as a commitment. The manager heard "try" as "yes". It should have been a range: how long usually, how long if things go badly, stated clearly as an estimate. The simulation just below compares both answers for the same three tasks.')

    S_ = 'estimate'
    a(C + '.sec.%s.title' % S_, 'Ước lượng không phải cam kết', 'An estimate is not a commitment')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'p', 'Theo Martin, người chuyên nghiệp phân biệt rõ ước lượng với cam kết. Cam kết là lời hứa phải giữ; chỉ đưa ra khi biết chắc sẽ làm được. Ước lượng là một phỏng đoán, một phân bố xác suất, không hứa gì. Vấn đề hay gặp là ước lượng bị nghe thành cam kết, hoặc cam kết được đưa ra ngầm, như khi đồng ý "cố". Cách nhớ: ước lượng là dự báo thời tiết, cam kết là lịch chiếu phim. [[src:book-coder]]',
      'According to Martin, professionals draw a clear line between estimates and commitments. A commitment is a promise you must keep, made only when you know you will succeed. An estimate is a guess, a probability distribution, promising nothing. The usual trouble is an estimate heard as a commitment, or a commitment made implicitly, as when agreeing to "try". To remember it: an estimate is a weather forecast, a commitment is a cinema showtime. [[src:book-coder]]')
    B(C, S_, 2, 'p', 'Martin giải thích vì sao "cố" là cam kết: nếu không có kế hoạch nào khác ngoài cố hơn, thì cố nghĩa là làm thêm giờ, làm cuối tuần, bỏ nghỉ. Đồng ý cố tức là đồng ý thành công. Martin mượn câu của Yoda, nhân vật trong phim Star Wars: làm, hoặc không làm, không có chuyện cố. [[src:book-coder]]',
      'Martin explains why "try" is a commitment: if there is no plan other than trying harder, trying means overtime, weekends, skipped holidays. Agreeing to try is agreeing to succeed. Martin borrows the line of Yoda, a character in the Star Wars films: do, or do not, there is no try. [[src:book-coder]]')

    S_ = 'pert'
    a(C + '.sec.%s.title' % S_, 'Ước lượng ba điểm (PERT)', 'Three-point estimates (PERT)')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'p', 'PERT (Program Evaluation and Review Technique, kỹ thuật đánh giá và xem xét chương trình) là cách ước lượng có từ năm 1957 cho dự án tàu ngầm Polaris. Mỗi việc ba con số: O lạc quan (chỉ đạt khi mọi thứ đều suôn sẻ, khả năng dưới 1%), N thường gặp nhất, P bi quan (mọi thứ trừ thảm họa, cũng dưới 1%). Từ đó μ = (O + 4N + P) / 6 là thời gian kỳ vọng, σ = (P − O) / 6 đo độ bất định. Với một chuỗi việc làm nối tiếp, μ cộng thẳng, còn σ là căn bậc hai của tổng bình phương các σ. Cách nhớ: thời gian thì cộng thẳng, bất định thì lấy căn tổng bình phương. [[src:book-coder]]',
      'PERT (Program Evaluation and Review Technique) is an estimation scheme created in 1957 for the Polaris submarine project. Three numbers per task: O optimistic (only if everything goes right, well under 1% likely), N nominal (most likely), P pessimistic (everything short of catastrophe, also well under 1%). Then μ = (O + 4N + P) / 6 is the expected duration and σ = (P − O) / 6 measures uncertainty. For tasks in sequence, μ adds up and σ is the square root of the sum of the squared σ. To remember it: durations add straight, uncertainties add by square root of the sum of squares. [[src:book-coder]]')
    B(C, S_, 2, 'p', 'Tính tay cho mô phỏng. MoMo (1, 3, 12): μ = (1 + 12 + 12) / 6 ≈ 4,17; σ = 11/6 ≈ 1,83. Hủy lịch (2, 3, 8): μ = 22/6 ≈ 3,67; σ = 1. Nhắc lịch (1, 2, 5): μ = 14/6 ≈ 2,33; σ = 4/6 ≈ 0,67. Cả ba: μ ≈ 4,17 + 3,67 + 2,33 = 10,17; σ = √(1,83² + 1² + 0,67²) ≈ √4,81 ≈ 2,19. Vậy có khả năng xong trong khoảng 10 ngày, có thể tới 12,4 (μ + σ), hiếm khi quá 14,6 (μ + 2σ). 6 ngày thấp hơn μ gần hai σ (10,17 − 6 ≈ 4,2 ≈ 1,9σ).',
      'By hand for the simulation. MoMo (1, 3, 12): μ = (1 + 12 + 12) / 6 ≈ 4.17; σ = 11/6 ≈ 1.83. Cancelling (2, 3, 8): μ = 22/6 ≈ 3.67; σ = 1. Reminders (1, 2, 5): μ = 14/6 ≈ 2.33; σ = 4/6 ≈ 0.67. All three: μ ≈ 4.17 + 3.67 + 2.33 = 10.17; σ = √(1.83² + 1² + 0.67²) ≈ √4.81 ≈ 2.19. So likely about 10 days, possibly 12.4 (μ + σ), rarely beyond 14.6 (μ + 2σ). 6 days is almost two σ below μ (10.17 − 6 ≈ 4.2 ≈ 1.9σ).')
    B(C, S_, 3, 'note', 'Martin cũng khuyên ước lượng cùng cả nhóm (Wideband Delphi: mỗi người ước lượng riêng rồi cùng bàn tới khi gần nhau) và chia việc lớn thành nhiều việc nhỏ, vì nhiều sai số nhỏ có xu hướng bù trừ nhau (luật số lớn). Chương chỉ dùng PERT vì nó có phép tính kiểm chứng được.',
      'Martin also recommends estimating as a team (Wideband Delphi: each person estimates alone, then everyone discusses until the numbers come close) and splitting big tasks into many small ones, since many small errors tend to cancel out (the law of large numbers). The chapter uses only PERT because it comes with checkable arithmetic.')
    B(C, S_, 3, 'kind', 'source')

    S_ = 'no'
    a(C + '.sec.%s.title' % S_, 'Nói không và nói có', 'Saying no and saying yes')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'p', 'Theo Martin, người chuyên nghiệp nói không khi câu trả lời thật là không, kể cả với cấp trên, vì quản lý cần thông tin đúng để quyết định; nói có với một điều biết là không thể là làm hại họ. Nói không không có nghĩa là dừng ở đó: hai bên cùng tìm phương án tốt nhất, như cắt bớt phạm vi hay dời hạn. Martin cũng mô tả một lời nói có thật: nói rõ sẽ làm gì, trước khi nào, và nếu gặp trở ngại thì báo ngay. Cách nhớ: nói không thì kèm phương án, nói có thì kèm hạn. [[src:book-coder]]',
      'According to Martin, professionals say no when the real answer is no, even to their managers, because managers need accurate information to decide; saying yes to something known to be impossible harms them. Saying no does not end there: both sides look for the best alternative, such as cutting scope or moving the date. Martin also describes a real yes: say clearly what you will do and by when, and if something blocks you, say so at once. To remember it: a no comes with an alternative, a yes comes with a date. [[src:book-coder]]')

    S_ = 'pressure'
    a(C + '.sec.%s.title' % S_, 'Làm việc dưới áp lực', 'Working under pressure')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'p', 'Theo Martin, cách tốt nhất là tránh áp lực bằng cách quản lý cam kết và giữ mã sạch. Khi áp lực vẫn tới: đừng hoảng, đừng vội, vì vội chỉ đào hố sâu hơn; nghĩ kỹ và đi với nhịp đều. Trao đổi: báo cho nhóm và cấp trên biết đang gặp khó, kèm kế hoạch tốt nhất, vì bất ngờ nhân áp lực lên nhiều lần. Dựa vào kỷ luật: theo TDD thì viết test nhiều hơn, theo refactor thì refactor nhiều hơn. Và nhờ người làm cặp. Cách nhớ: áp lực là lúc bám kỷ luật, không phải lúc bỏ. [[src:book-coder]]',
      'According to Martin, the best way is to avoid pressure by managing commitments and keeping code clean. When it comes anyway: do not panic, do not rush, since rushing digs the hole deeper; think it through and move at a steady pace. Communicate: tell your team and managers you are in trouble, with your best plan, because surprises multiply pressure. Rely on your disciplines: if you follow TDD, write more tests; if you refactor, refactor more. And get someone to pair with. To remember it: pressure is the time to hold on to discipline, not to drop it. [[src:book-coder]]')

    S_ = 'bugs'
    a(C + '.sec.%s.title' % S_, 'Hai lỗi hay gặp', 'Two common bugs')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'bug', 'Tính năng xong trễ 4,5 ngày so với lời hứa, và hai lỗi lọt ra bản phát hành.', 'A feature ships 4.5 days later than promised, with two defects in the release.')
    B(C, S_, 1, 'cause', 'Lời "em cố" đưa ra từ ước lượng lạc quan nhất đã thành cam kết; khi trễ, test bị bỏ để đuổi kịp.', 'An "I\'ll try" based on the most optimistic estimate became a commitment; once late, tests were skipped to catch up.')
    B(C, S_, 1, 'fix', 'Đưa ước lượng ba điểm và khoảng μ, μ + σ; chỉ cam kết điều biết chắc làm được; giữ TDD khi bị dồn.', 'Give a three-point estimate and the μ, μ + σ range; commit only to what you know you can do; keep TDD under pressure.')
    B(C, S_, 2, 'bug', 'Quản lý bất ngờ biết dự án trễ đúng vào ngày phát hành.', 'The manager learns the project is late on release day itself.')
    B(C, S_, 2, 'cause', 'Nhóm biết mình trễ từ ngày thứ tư nhưng hy vọng đuổi kịp và không nói.', 'The team knew they were late on day four but hoped to catch up and said nothing.')
    B(C, S_, 2, 'fix', 'Báo ngay khi ước lượng đổi, kèm phương án; với Martin, để người khác giữ hy vọng sai là không chuyên nghiệp.', 'Report as soon as the estimate changes, with options; for Martin, letting others keep false hope is unprofessional.')

    S_ = 'ex'
    a(C + '.sec.%s.title' % S_, 'Bài tập', 'Exercise')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'ex', 'Hai việc nối tiếp: đăng nhập bằng mã OTP, tức mã dùng một lần gửi qua SMS (O = 2, N = 4, P = 12 ngày) và đổi giao diện màn hồ sơ (O = 1, N = 2, P = 3). Tính μ và σ cho từng việc và cho cả hai. Hạn quản lý đưa ra là 8 ngày: bạn trả lời thế nào?', 'Two tasks in sequence: OTP sign-in, with a one-time code sent by SMS (O = 2, N = 4, P = 12 days) and a profile screen redesign (O = 1, N = 2, P = 3). Compute μ and σ for each and for both. The manager\'s deadline is 8 days: what do you answer?')
    B(C, S_, 1, 'hint', 'μ = (O + 4N + P) / 6; σ = (P − O) / 6; tổng σ là căn của tổng bình phương. So 8 với μ và μ + σ.', 'μ = (O + 4N + P) / 6; σ = (P − O) / 6; the combined σ is the square root of the sum of squares. Compare 8 with μ and μ + σ.')
    B(C, S_, 1, 'sol', 'OTP: μ = (2 + 16 + 12) / 6 = 5; σ = 10/6 ≈ 1,67. Hồ sơ: μ = (1 + 8 + 3) / 6 = 2; σ = 2/6 ≈ 0,33. Cả hai: μ = 7; σ = √(1,67² + 0,33²) ≈ √2,89 ≈ 1,70. 8 ngày nằm giữa μ (7) và μ + σ (8,7): có thể kịp, nhưng không chắc. Trả lời: "Thường là 7 ngày, nhưng có thể tới 9; nếu 8 là hạn cứng, ta làm OTP trước và màn hồ sơ sau, hoặc lùi hạn thêm 1 ngày." Đó là ước lượng, không phải cam kết.',
      'OTP: μ = (2 + 16 + 12) / 6 = 5; σ = 10/6 ≈ 1.67. Profile: μ = (1 + 8 + 3) / 6 = 2; σ = 2/6 ≈ 0.33. Both: μ = 7; σ = √(1.67² + 0.33²) ≈ √2.89 ≈ 1.70. 8 days lies between μ (7) and μ + σ (8.7): it may be met, but not surely. Answer: "Usually 7 days, but possibly 9; if 8 is a hard deadline, we do OTP first and the profile after, or move the deadline by a day." That is an estimate, not a commitment.')

    for q, qv, qe, av, ae, wv, we in [
        ('q1', 'O = 2, N = 5, P = 14. μ và σ là bao nhiêu?', 'O = 2, N = 5, P = 14. What are μ and σ?', 'μ = 6 ngày, σ = 2 ngày.', 'μ = 6 days, σ = 2 days.', 'Thay vào: μ = (2 + 20 + 14) / 6 = 6; σ = (14 − 2) / 6 = 2.', 'Plug in: μ = (2 + 20 + 14) / 6 = 6; σ = (14 − 2) / 6 = 2.'),
        ('q2', 'Hai việc nối tiếp có σ là 3 và 4. σ của cả chuỗi là bao nhiêu?', 'Two tasks in sequence have σ of 3 and 4. What is σ of the sequence?', '5.', '5.', 'Căn của tổng bình phương: √(9 + 16) = 5, không phải 7.', 'The square root of the sum of squares: √(9 + 16) = 5, not 7.'),
        ('q3', 'Theo Martin, đáp "em sẽ cố" nghĩa là gì?', 'According to Martin, what does answering "I\'ll try" mean?', 'Một cam kết ngầm sẽ thành công.', 'An implied commitment to succeed.', 'Không có kế hoạch khác thì "cố" chỉ là làm thêm giờ.', 'Without a different plan, "trying" only means overtime.'),
        ('q4', 'Khi bị dồn tiến độ, Martin khuyên làm gì với TDD?', 'Under schedule pressure, what does Martin advise about TDD?', 'Giữ, thậm chí viết test nhiều hơn.', 'Keep it, even write more tests.', 'Áp lực là lúc kỷ luật cần nhất, không phải lúc bỏ chúng.', 'Pressure is when disciplines matter most, not when to drop them.')]:
        a(C + '.quiz.%s.q' % q, qv, qe); a(C + '.quiz.%s.a' % q, av, ae); a(C + '.quiz.%s.why' % q, wv, we)
