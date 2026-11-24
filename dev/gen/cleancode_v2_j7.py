# Mã sạch · J7: gỡ lỗi có phương pháp (Phần 2: test và thay đổi an toàn)
# Nguồn: Seemann, Code That Fits in Your Head 12.1 (hiểu trước; phương pháp khoa học; đơn giản hóa; rubber duck, giới hạn thời gian),
# 12.2 (lỗi: sửa ngay, đừng để dồn), 12.2.1 (tái hiện lỗi thành test; test đỏ là giả thuyết đúng và thành test hồi quy), 12.2.3 (lỗi không
# tất định), 12.3 (chia đôi: bỏ một nửa mã cho tới khi hiểu), 12.3.1 (git bisect, câu chuyện khoảng 130 commit), A.4, A.19;
# git-scm.com git-bisect (tìm kiếm nhị phân; bisect run: mã thoát 0 là good, 1–127 trừ 125 là bad, 125 là bỏ qua). Đọc 2026-11-24, diễn đạt lại.

SEC_ORDER = {'j7': ['hook', 'understand', 'reproduce', 'bisect', 'zero', 'bugs', 'ex', 'honest']}


def add(a):
    def B(ch, sec, n, field, vi, en=None):
        a('%s.sec.%s.b.%02d.%s' % (ch, sec, n, field), vi, vi if en is None else en)

    a('preset.bisect', 'Mã sạch · tìm commit gây lỗi bằng chia đôi', 'Clean code · finding the guilty commit by bisection')
    m = lambda k, vi, en=None: a('m.bisect.' + k, vi, en)
    m('title', 'Lùi từng commit, hay chia đôi khoảng nghi ngờ', 'Step back one commit at a time, or halve the suspect range')
    m('overview', 'Tester báo: tin nhắc lịch hiện sai giờ, nhưng chỉ trên máy của họ. Bản 1.4 (commit 0) chưa có lỗi; HEAD (commit 200) có lỗi. Trước hết tái hiện lỗi thành một test chạy được ở mọi máy. Sau đó tìm commit gây lỗi theo hai cách: lùi từng commit từ HEAD, hoặc chia đôi khoảng nghi ngờ bằng git bisect run.',
      'A tester reports: reminder messages show the wrong time, but only on their phone. Release 1.4 (commit 0) was fine; HEAD (commit 200) is broken. First, reproduce the bug as a test that runs on any machine. Then find the guilty commit two ways: step back one commit at a time from HEAD, or halve the suspect range with git bisect run.')
    m('wrapup', 'Test cố định múi giờ của phòng khám biến lỗi "chỉ trên máy tester" thành lỗi đỏ ở mọi máy. Lùi từng commit cần 64 lần build và chạy test (khoảng 3 giờ 12 phút) để tới commit 136, commit tốt đầu tiên. Chia đôi chỉ cần 8 lần (khoảng 24 phút), vì mỗi lần thử loại một nửa khoảng nghi ngờ: log2(200) ≈ 7,64, làm tròn lên 8. Cả hai cùng chỉ ra commit 137, một commit "tách hàm định dạng giờ" tưởng là refactor vô hại.',
      'A test that fixes the clinic\'s time zone turns a "only on the tester\'s phone" bug into a failure on every machine. Stepping back one commit at a time takes 64 builds and test runs (about 3 hours 12 minutes) to reach commit 136, the first good one. Bisection takes 8 (about 24 minutes), since each probe removes half the suspect range: log2(200) ≈ 7.64, rounded up to 8. Both point at commit 137, an "extract the time formatting function" commit that looked like a harmless refactoring.')
    m('simp.1', 'Số commit, vị trí commit lỗi và 3 phút mỗi lần build là minh họa. git bisect chọn commit giữa theo đồ thị commit; với lịch sử thẳng, mô phỏng chọn đúng điểm giữa của khoảng.', 'The number of commits, the position of the bad commit and 3 minutes per build are illustrative. git bisect picks the middle commit from the commit graph; with linear history the simulation picks the exact midpoint of the range.')
    m('simp.2', 'Seemann dùng git bisect ở chế độ tương tác cho câu chuyện khoảng 130 commit; chế độ git bisect run cần một lệnh tự trả lời tốt hay xấu, ở đây là test vừa viết để tái hiện lỗi.', 'Seemann used interactive git bisect in his story of about 130 commits; git bisect run needs a command that answers good or bad by itself, here the test just written to reproduce the bug.')
    m('ctl.hint', 'Đổi cách tìm rồi đi lại; đếm số lần thử và xem khoảng nghi ngờ (ô chưa gạch) thu hẹp nhanh tới đâu.', 'Switch the search and walk again; count the probes and watch how fast the suspect range (unstruck cells) shrinks.')
    m('ctl.case', 'Cách tìm', 'Search')
    for k, vi, en in [('linear', 'lùi từng commit', 'step back one commit at a time'), ('bisect', 'chia đôi (git bisect run)', 'bisect (git bisect run)')]:
        m('ctl.case.' + k, vi, en)
    m('diagramTitle', 'Báo lỗi, test tái hiện, chọn commit, kết luận', 'Report, reproducing test, picking a commit, verdict')
    m('diagramDesc', 'Báo lỗi thành test; test chạy trên commit được chọn; kết quả thu hẹp khoảng nghi ngờ', 'The report becomes a test; the test runs on the picked commit; the result narrows the suspect range')
    for k, vi, en in [('report', 'Báo lỗi của tester', 'Tester\'s report'), ('test', 'Test tái hiện', 'Reproducing test'), ('pick', 'Chọn commit để thử', 'Pick a commit to try'), ('verdict', 'Tốt hay xấu', 'Good or bad')]:
        m('n.' + k, vi, en)
    m('met.probes', 'Lần build và chạy test', 'Builds and test runs'); m('met.left', 'Commit còn bị nghi', 'Commits still suspect'); m('met.minutes', 'Phút đã tốn', 'Minutes spent')
    a('cap.bisect', 'Báo lỗi thành test; mỗi lần thử chạy test trên một commit và thu hẹp khoảng nghi ngờ. Nút đỏ: lỗi chưa tái hiện được, hay còn quá nhiều commit bị nghi.', 'The report becomes a test; each probe runs the test on one commit and narrows the suspect range. Red node: the bug is not reproducible yet, or too many commits are still suspect.')
    S = [
        ('linear', 's1', 'Tái hiện lỗi thành test', 'Reproduce the bug as a test',
         'Giả thuyết: máy tester ở múi giờ UTC+7, máy dev ở UTC. Test cố định múi giờ Asia/Ho_Chi_Minh: đỏ ở HEAD, xanh ở bản 1.4. Lỗi giờ tái hiện được ở mọi máy.', 'Hypothesis: the tester\'s phone is at UTC+7, the dev machine at UTC. A test fixing the Asia/Ho_Chi_Minh zone fails at HEAD and passes at release 1.4. The bug is now reproducible anywhere.'),
        ('linear', 's2', 'Lùi từ HEAD: 199, 198, … 190', 'Step back from HEAD: 199, 198, … 190',
         'Mười lần build và chạy test, cả mười đều xấu. Mỗi lần chỉ loại đúng một commit; còn 190 commit bị nghi.', 'Ten builds and test runs, all ten bad. Each removes exactly one commit; 190 commits are still suspect.'),
        ('linear', 's3', 'Lùi tiếp tới 170', 'Keep stepping back to 170',
         'Đã 30 lần, khoảng một tiếng rưỡi. Vẫn còn 170 commit bị nghi.', '30 probes so far, about an hour and a half. 170 commits are still suspect.'),
        ('linear', 's4', 'Commit 136 tốt: commit 137 là thủ phạm', 'Commit 136 is good: commit 137 is the culprit',
         'Lần thứ 64 mới gặp commit tốt đầu tiên. Commit 137 "tách hàm định dạng giờ" là commit xấu đầu tiên. Tổng cộng khoảng 192 phút.', 'The 64th probe finally hits the first good commit. Commit 137, "extract the time formatting function", is the first bad commit. About 192 minutes in total.'),
        ('bisect', 's1', 'Tái hiện lỗi thành test', 'Reproduce the bug as a test',
         'Cùng giả thuyết và cùng test: đỏ ở HEAD, xanh ở bản 1.4. Test này cũng chính là lệnh để git bisect run tự phân xử tốt hay xấu.', 'The same hypothesis and test: red at HEAD, green at release 1.4. This test is also the command git bisect run uses to judge good or bad by itself.'),
        ('bisect', 's2', 'Thử commit 100, rồi 150', 'Probe commit 100, then 150',
         '100 tốt: loại nửa dưới. 150 xấu: loại phần trên. Sau hai lần còn 50 commit bị nghi (101 tới 150).', '100 is good: drop the lower half. 150 is bad: drop the top. After two probes, 50 commits remain suspect (101 to 150).'),
        ('bisect', 's3', 'Thử 125, 137, 131', 'Probe 125, 137, 131',
         '125 tốt, 137 xấu, 131 tốt. Sau năm lần còn 6 commit bị nghi (132 tới 137).', '125 good, 137 bad, 131 good. After five probes, 6 commits remain suspect (132 to 137).'),
        ('bisect', 's4', 'Thử 134, 135, 136: thủ phạm là 137', 'Probe 134, 135, 136: the culprit is 137',
         'Ba lần nữa đều tốt. Sau 8 lần, khoảng chỉ còn commit 137: "tách hàm định dạng giờ". Tổng cộng khoảng 24 phút, và máy làm hộ.', 'Three more probes, all good. After 8 probes only commit 137 remains: "extract the time formatting function". About 24 minutes in total, and the machine did the work.'),
    ]
    for case, k, tv, te, xv, xe in S:
        sid = case + '.' + k
        m('s.%s.title' % sid, tv, te); m('s.%s.explain' % sid, xv, xe); m('ev.' + sid, tv, te)
    for k, vi, en in [
        ('try', 'Theo dãy 200 ô: ô xanh hay ô gạch xám là commit đã bị loại; ô trống là khoảng còn bị nghi.', 'Follow the strip of 200 cells: green or grey-struck cells are ruled out; plain cells are the range still suspect.'),
        ('linear.s2', 'Mỗi lần thử chỉ trả lời câu hỏi về một commit, nên số lần thử tăng theo khoảng cách tới commit lỗi.', 'Each probe answers a question about one commit only, so the number of probes grows with the distance to the bad commit.'),
        ('linear.s3', 'Seemann: đặt giới hạn thời gian cho việc gỡ lỗi, ví dụ 25 phút; hết giờ mà không tiến triển thì nghỉ, hoặc đổi cách làm. [[src:book-seemann]]', 'Seemann: time-box debugging, say 25 minutes; when time is up with no progress, take a break or change approach. [[src:book-seemann]]'),
        ('linear.s4', 'Seemann kể lần ông mất nhiều giờ theo hướng sai trước khi nhận ra: tính năng từng chạy, giờ không chạy, vậy có một commit ở giữa gây ra. Ông có khoảng 130 commit ở giữa và dùng git bisect. [[src:book-seemann]]', 'Seemann recounts losing hours on wrong leads before realising: the feature used to work and now did not, so some commit in between caused it. He had some 130 commits in between and used git bisect. [[src:book-seemann]]'),
        ('bisect.s1', 'Seemann: khi nghĩ đã hiểu lỗi, viết test với giả thuyết là nó sẽ đỏ. Nó đỏ thì giả thuyết đúng, và test ở lại làm test hồi quy; nó xanh thì sửa giả thuyết. [[src:book-seemann]]', 'Seemann: once you think you understand the defect, write a test whose hypothesis is that it fails. If it fails, the hypothesis holds and the test stays as a regression test; if it passes, revise the hypothesis. [[src:book-seemann]]'),
        ('bisect.s2', 'Tài liệu git-bisect: lệnh dùng tìm kiếm nhị phân; bạn chỉ ra một commit xấu và một commit tốt, git chọn commit ở giữa và hỏi tốt hay xấu, thu hẹp dần tới commit gây lỗi. [[src:git-bisect]]', 'The git-bisect docs: the command uses binary search; you name a bad commit and a good one, git picks a commit in between and asks good or bad, narrowing down to the commit that introduced the bug. [[src:git-bisect]]'),
        ('bisect.s3', 'git bisect run: lệnh trả mã thoát 0 nghĩa là tốt, từ 1 tới 127 (trừ 125) nghĩa là xấu, 125 nghĩa là commit này không thử được và bỏ qua. [[src:git-bisect]]', 'git bisect run: the command exits 0 for good, 1 to 127 (except 125) for bad, and 125 for "this commit cannot be tested, skip it". [[src:git-bisect]]'),
        ('bisect.s4', 'Mỗi lần thử loại một nửa: với n commit cần khoảng log2(n) lần. 200 commit: 8 lần; 1.000 commit: 10 lần. Lùi từng commit thì số lần tăng tuyến tính.', 'Each probe removes half: n commits need about log2(n) probes. 200 commits: 8 probes; 1,000 commits: 10. Stepping back one at a time grows linearly.')]:
        m('co.' + k, vi, en)

    z = lambda k, vi, en=None: a('vz.' + k, vi, en)
    z('tab.bisect', 'Dãy 200 commit', 'Strip of 200 commits')
    z('bs.cap', 'Mỗi ô là một commit, từ 1 (sau bản 1.4) tới 200 (HEAD), mỗi hàng 20 commit. Ô xanh hay ô gạch xám: đã loại; ô trống: còn bị nghi. Ô có viền: commit vừa thử ở bước này. Ô đỏ đậm: thủ phạm khi đã tìm ra.', 'Each cell is a commit, from 1 (after release 1.4) to 200 (HEAD), 20 per row. Green or grey-struck: ruled out; plain: still suspect. Outlined: probed in this step. Bold red: the culprit once found.')
    z('bs.aria', 'Còn {n} commit bị nghi sau {p} lần thử', '{n} commits still suspect after {p} probes')
    z('bs.math', 'log2(200) ≈ 7,64 → 8 lần thử nếu chia đôi; lùi từng commit tới commit 137 cần 64 lần.', 'log2(200) ≈ 7.64 → 8 probes by bisection; stepping back to commit 137 takes 64.')
    z('bs.tcap', 'Các lần thử ở bước này.', 'This step\'s probes.')
    for k, vi, en in [('n', 'Lần', 'Probe'), ('commit', 'Commit', 'Commit'), ('res', 'Kết quả', 'Result'), ('range', 'Còn nghi', 'Still suspect')]:
        z('bs.col.' + k, vi, en)
    z('bs.good', 'tốt', 'good'); z('bs.bad', 'xấu', 'bad'); z('bs.range', '{a}–{b} ({n} commit)', '{a}–{b} ({n} commits)'); z('bs.found', 'commit {c}', 'commit {c}')
    z('bs.repro', 'HEAD (200): test đỏ. Bản 1.4 (0): test xanh. Lỗi tái hiện được; khoảng nghi ngờ là 1–200.', 'HEAD (200): the test fails. Release 1.4 (0): the test passes. The bug reproduces; the suspect range is 1–200.')
    z('bs.more', '… và {n} lần trước đó, đều xấu', '… and {n} earlier probes, all bad')
    z('bs.legend', 'Ô xanh: loại vì tốt. Ô xám gạch: loại vì xấu (lỗi có từ trước đó). Ô đỏ đậm: commit xấu đầu tiên.', 'Green: ruled out as good. Grey struck: ruled out as bad (the bug started earlier). Bold red: the first bad commit.')

    C = 'j7'
    a(C + '.title', 'Gỡ lỗi có phương pháp: tái hiện và chia đôi', 'Methodical debugging: reproduce and bisect')
    a(C + '.essence', 'Trước khi sửa, hãy hiểu: đặt giả thuyết, làm thí nghiệm, so kết quả với dự đoán. Thí nghiệm tốt nhất là một test tái hiện lỗi: nó đỏ thì giả thuyết đúng, và nó ở lại làm test hồi quy.\nLỗi "chỉ xảy ra trên máy tester" thường do môi trường: múi giờ, ngôn ngữ, phiên bản. Cố định yếu tố đó trong test để lỗi đỏ ở mọi máy.\nKhi biết một điểm tốt và một điểm xấu, chia đôi khoảng ở giữa: mỗi lần thử loại một nửa, n commit cần khoảng log2(n) lần. git bisect run làm việc đó với test tái hiện lỗi.',
      'Before fixing, understand: form a hypothesis, run an experiment, compare the outcome with the prediction. The best experiment is a test reproducing the bug: if it fails, the hypothesis holds, and it stays as a regression test.\nBugs that "only happen on the tester\'s phone" are usually environmental: time zone, language, version. Pin that factor in the test so the bug fails on every machine.\nWith one known good point and one known bad point, halve the range between: each probe removes half, so n commits need about log2(n) probes. git bisect run does this with the reproducing test.')
    a(C + '.goal.g1', 'Đã thấy khoảng nghi ngờ thu hẹp', 'Saw the suspect range shrink')
    a(C + '.goal.g2', 'Đã tìm ra commit gây lỗi', 'Found the guilty commit')
    a(C + '.sim.cleancode.bisect', 'lùi từng commit hay chia đôi', 'step back or bisect')

    S_ = 'hook'
    a(C + '.sec.%s.title' % S_, 'Đoán trước khi đọc', 'Predict before reading')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'predict', 'Bản 1.4 chạy đúng; 200 commit sau thì tin nhắc lịch hiện sai giờ, nhưng chỉ trên máy tester. Mỗi lần build và chạy test mất 3 phút. Tìm commit gây lỗi bằng cách lùi từng commit tốn tối đa bao lâu? Có cách nào nhanh hơn?',
      'Release 1.4 worked; 200 commits later reminder messages show the wrong time, but only on the tester\'s phone. Each build and test run takes 3 minutes. How long could finding the guilty commit take by stepping back one at a time? Is there a faster way?')
    B(C, S_, 1, 'ans', 'Lùi từng commit có thể tốn tới 200 lần, tức 10 tiếng. Chia đôi chỉ cần khoảng log2(200) ≈ 8 lần, chừng 24 phút. Nhưng trước hết phải biến lỗi "chỉ trên máy tester" thành một test đỏ ở mọi máy, nếu không thì chẳng có gì để chia đôi. Mô phỏng ngay dưới làm cả hai bước.',
      'Stepping back could take up to 200 probes, 10 hours. Bisection needs about log2(200) ≈ 8 probes, around 24 minutes. But first the "only on the tester\'s phone" bug must become a test that fails on every machine, or there is nothing to bisect with. The simulation just below does both.')

    S_ = 'understand'
    a(C + '.sec.%s.title' % S_, 'Hiểu trước khi sửa', 'Understand before fixing')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'p', 'Seemann cảnh báo "lập trình theo may rủi": thử hết câu thần chú này tới câu khác (khởi động lại, xóa cache, thêm một dòng) cho tới khi lỗi tạm biến mất. Thay vào đó dùng một biến thể của phương pháp khoa học: đặt giả thuyết có thể bác bỏ, làm thí nghiệm, so kết quả với dự đoán, lặp lại cho tới khi hiểu. Mục tiêu của các bước này là hiểu lỗi, chưa phải sửa nó. [[src:book-seemann]]',
      'Seemann warns against "programming by coincidence": trying one incantation after another (restart, clear the cache, add a line) until the bug goes away for now. Instead use a variant of the scientific method: form a falsifiable hypothesis, run the experiment, compare the outcome with the prediction, repeat until you understand. The goal of these steps is understanding, not yet fixing. [[src:book-seemann]]')
    B(C, S_, 2, 'p', 'Hai lời khuyên đi kèm. Đơn giản hóa: thử xem bỏ bớt mã có làm lỗi biến mất không, vì phản xạ thêm mã cho trường hợp đặc biệt thường che một lỗi gốc. Giới hạn thời gian: đặt ví dụ 25 phút; hết giờ mà không tiến triển thì rời máy một lúc, hoặc nhờ người khác, kể cả kiểu "giải thích cho con vịt cao su". [[src:book-seemann]]',
      'Two companion tips. Simplify: try whether removing code makes the bug go away, since the reflex of adding code for a special case often hides a root defect. Time-box: say 25 minutes; when time is up with no progress, step away from the computer, or ask someone, even in the "explain it to a rubber duck" way. [[src:book-seemann]]')

    S_ = 'reproduce'
    a(C + '.sec.%s.title' % S_, 'Tái hiện lỗi thành test', 'Reproduce the defect as a test')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'p', 'Seemann: khi nghĩ đã hiểu lỗi, thí nghiệm là một test tự động với giả thuyết "nó sẽ đỏ". Nó đỏ: giả thuyết đúng, và bạn có sẵn test hồi quy. Nó xanh: giả thuyết sai, sửa giả thuyết và thử lại. Theo ông, phần khó của sửa lỗi là hiểu và tái hiện nó; có test đỏ rồi thì làm cho xanh thường không khó. [[src:book-seemann]]',
      'Seemann: once you think you understand the defect, the experiment is an automated test hypothesised to fail. It fails: the hypothesis holds, and you have a regression test for free. It passes: the hypothesis was wrong; revise and try again. In his view the hard part of fixing a defect is understanding and reproducing it; once a test fails, making it pass is usually not hard. [[src:book-seemann]]')
    B(C, S_, 2, 'kt', '@Test fun `giờ nhắc theo múi giờ phòng khám`() {\n    val zone = ZoneId.of("Asia/Ho_Chi_Minh")             // cố định thứ khác nhau giữa các máy\n    val clock = Clock.fixed(Instant.parse("2026-11-29T12:00:00Z"), zone)\n    val text = reminderText(LocalDateTime.parse("2026-11-30T09:00"), clock)\n    assertEquals("Nhắc lịch khám 09:00 ngày 30/11", text)\n}',
      '@Test fun `reminder time uses the clinic time zone`() {\n    val zone = ZoneId.of("Asia/Ho_Chi_Minh")             // pin what differs between machines\n    val clock = Clock.fixed(Instant.parse("2026-11-29T12:00:00Z"), zone)\n    val text = reminderText(LocalDateTime.parse("2026-11-30T09:00"), clock)\n    assertEquals("Reminder: visit at 09:00 on 30 Nov", text)\n}')
    B(C, S_, 3, 'p', 'Lỗi "chỉ trên máy tester" là lỗi phụ thuộc môi trường: múi giờ, ngôn ngữ, định dạng số, phiên bản Android, dữ liệu sẵn có. Biến những thứ đó thành tham số (như Clock và ZoneId ở trên) để test chọn giá trị, thay vì để máy chạy test tự quyết. Seemann cũng bàn lỗi không tất định như race condition: chấp nhận một test thỉnh thoảng mới đỏ còn hơn không có test nào. [[src:book-seemann]]',
      'A bug "only on the tester\'s phone" is environment-dependent: time zone, language, number format, Android version, existing data. Turn those into parameters (like Clock and ZoneId above) so the test chooses the values instead of the machine running it. Seemann also discusses non-deterministic defects such as race conditions: a test that only fails sometimes beats having no test. [[src:book-seemann]]')

    S_ = 'bisect'
    a(C + '.sec.%s.title' % S_, 'Chia đôi: mã và lịch sử commit', 'Bisection: code and commit history')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'p', 'Seemann mô tả chia đôi ở dạng tổng quát: có cách phát hiện lỗi; bỏ một nửa mã; lỗi còn thì lặp lại, lỗi mất thì trả lại nửa đó và bỏ nửa kia; tiếp tục tới khi phần mã còn lại đủ nhỏ để hiểu. Ông thường dùng nó khi soạn một ví dụ tối giản để hỏi người khác, và hay tự gỡ được trước khi kịp hỏi. [[src:book-seemann]]',
      'Seemann describes bisection in general: have a way to detect the problem; remove half the code; if the problem persists, repeat, if it vanishes, restore that half and remove the other; continue until what remains is small enough to understand. He often uses it while building a minimal example to ask others, and often gets unstuck before posting. [[src:book-seemann]]')
    B(C, S_, 2, 'p', 'Với lịch sử commit, git bisect làm đúng việc đó: tài liệu chính thức mô tả nó dùng tìm kiếm nhị phân; bạn chỉ ra một commit xấu, một commit tốt, git chọn commit ở giữa và hỏi tốt hay xấu. Có lệnh tự phân xử thì dùng git bisect run: mã thoát 0 là tốt, 1 tới 127 trừ 125 là xấu, 125 là bỏ qua commit không thử được (ví dụ không build được). Seemann nhận xét lỗi cần bisect thường là lỗi bộ test đã không bắt được, nên hay phải viết test tái hiện trước. [[src:git-bisect]] [[src:book-seemann]]',
      'For commit history, git bisect does exactly that: the official docs describe it as binary search; you name a bad commit and a good commit, git picks one in between and asks good or bad. With a command that judges by itself, use git bisect run: exit code 0 is good, 1 to 127 except 125 is bad, 125 skips a commit that cannot be tested (for example one that does not build). Seemann notes the bugs you bisect for are usually ones the test suite missed, so you often have to write the reproducing test first. [[src:git-bisect]] [[src:book-seemann]]')
    B(C, S_, 3, 'kt', 'git bisect start\ngit bisect bad HEAD                     # commit 200: có lỗi\ngit bisect good v1.4                    # commit 0: chưa có lỗi\ngit bisect run ./gradlew testDebugUnitTest --tests "*ReminderTimeTest"\n# … commit 137 is the first bad commit\ngit bisect reset',
      'git bisect start\ngit bisect bad HEAD                     # commit 200: broken\ngit bisect good v1.4                    # commit 0: fine\ngit bisect run ./gradlew testDebugUnitTest --tests "*ReminderTimeTest"\n# … commit 137 is the first bad commit\ngit bisect reset')
    B(C, S_, 3, 'lang', 'bash')
    B(C, S_, 4, 'p', 'Phép tính: mỗi lần thử chia đôi khoảng, nên sau k lần còn khoảng n / 2^k commit. Cần 2^k ≥ n, tức k = ⌈log2(n)⌉. Với n = 200: 2^7 = 128 < 200 ≤ 256 = 2^8, nên cần 8 lần. Commit nhỏ và mỗi commit đều build được (chương J6) làm chia đôi hiệu quả hơn: commit tìm ra chỉ chứa ít thay đổi để đọc.',
      'The arithmetic: each probe halves the range, so after k probes about n / 2^k commits remain. You need 2^k ≥ n, so k = ⌈log2(n)⌉. For n = 200: 2^7 = 128 < 200 ≤ 256 = 2^8, so 8 probes. Small commits that each build (chapter J6) make bisection more useful: the commit it finds holds few changes to read.')

    S_ = 'zero'
    a(C + '.sec.%s.title' % S_, 'Số lỗi lý tưởng là không', 'The ideal number of defects is zero')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'p', 'Seemann cho rằng không thể loại hết lỗi nhưng đừng để chúng dồn lại: khi một lỗi xuất hiện, dừng việc đang làm và sửa nó, vì "để sau" thì không bao giờ tới. Ông gọi theo cách của lean là "xây chất lượng vào trong". Với git, cất tạm việc đang làm bằng stash rồi quay lại sau là chuyện vài giây. [[src:book-seemann]]',
      'Seemann holds that you cannot eliminate defects but must not let them accumulate: when one appears, stop what you are doing and fix it, because "later" never comes. He uses the lean phrase "building quality in". With git, stashing current work and coming back later takes seconds. [[src:book-seemann]]')

    S_ = 'bugs'
    a(C + '.sec.%s.title' % S_, 'Hai lỗi hay gặp', 'Two common bugs')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'bug', 'Lỗi "chỉ xảy ra trên máy tester", dev không tái hiện được nên đóng báo lỗi.', 'A bug that "only happens on the tester\'s phone"; developers cannot reproduce it and close the report.')
    B(C, S_, 1, 'cause', 'Mã dùng ZoneId.systemDefault(); máy dev và trình giả lập ở UTC, máy tester ở UTC+7. Test cũng dùng múi giờ của máy chạy nó.', 'The code uses ZoneId.systemDefault(); dev machines and emulators are at UTC, the tester\'s phone at UTC+7. The tests also use the zone of the machine running them.')
    B(C, S_, 1, 'fix', 'Đưa Clock và múi giờ thành tham số; test cố định Asia/Ho_Chi_Minh để đỏ ở mọi máy; mã dùng múi giờ của phòng khám thay vì của máy.', 'Make Clock and the zone parameters; the test pins Asia/Ho_Chi_Minh so it fails on every machine; the code uses the clinic\'s zone rather than the device\'s.')
    B(C, S_, 2, 'bug', 'git bisect chỉ ra một commit khổng lồ "WIP" gộp 40 file, vẫn không biết dòng nào gây lỗi.', 'git bisect points at a huge "WIP" commit touching 40 files, and nobody can tell which line caused it.')
    B(C, S_, 2, 'cause', 'Commit to và nhiều commit giữa chừng không build được, nên chia đôi chỉ thu hẹp tới mức một khối lớn.', 'Large commits, many intermediate ones not building, so bisection only narrows things down to one big lump.')
    B(C, S_, 2, 'fix', 'Commit nhỏ, mỗi commit build được và xanh (chương J6, J10). Commit không thử được thì cho lệnh trả mã 125 để git bisect bỏ qua.', 'Small commits, each building and green (chapters J6, J10). For untestable commits, have the command exit 125 so git bisect skips them.')

    S_ = 'ex'
    a(C + '.sec.%s.title' % S_, 'Bài tập', 'Exercise')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'ex', 'Màn danh sách bác sĩ sắp xếp sai thứ tự tên có dấu ("Đặng" đứng sau "Zung"), chỉ trên một số máy. Bản 2.0 đúng, bản 2.3 sai, ở giữa có 1.000 commit. Viết giả thuyết, test tái hiện, và tính số lần thử tối đa nếu dùng git bisect.', 'The doctor list sorts names with diacritics wrongly ("Đặng" after "Zung"), only on some phones. Release 2.0 was right, 2.3 is wrong, with 1,000 commits in between. Write a hypothesis, a reproducing test, and compute the maximum number of probes with git bisect.')
    B(C, S_, 1, 'hint', 'Khác nhau giữa các máy ở đây là gì? So sánh chuỗi theo mã ký tự hay theo ngôn ngữ? 2^10 bằng bao nhiêu?', 'What differs between phones here? Are strings compared by character code or by language? What is 2^10?')
    B(C, S_, 1, 'sol', 'Giả thuyết: một commit đổi từ so sánh theo Collator của locale sang compareTo theo mã ký tự, hoặc dùng locale mặc định của máy; máy đặt tiếng Việt thì đúng, máy tiếng Anh thì sai. Test: cố định Locale("vi") và một danh sách tên, khẳng định thứ tự mong đợi; test đỏ ở 2.3 và xanh ở 2.0. Số lần thử: 2^9 = 512 < 1.000 ≤ 1.024 = 2^10, nên tối đa 10 lần.',
      'Hypothesis: a commit switched from a locale Collator to compareTo by character code, or started using the device\'s default locale; phones set to Vietnamese are right, English ones wrong. Test: pin Locale("vi") and a list of names, asserting the expected order; it fails at 2.3 and passes at 2.0. Probes: 2^9 = 512 < 1,000 ≤ 1,024 = 2^10, so at most 10.')

    S_ = 'honest'
    a(C + '.sec.%s.title' % S_, 'Chương này giản lược những gì', 'What this chapter simplifies')
    a(C + '.sec.%s.badge' % S_, 'simplified')
    B(C, S_, 1, 'p', 'Hiểu trước khi sửa, phương pháp khoa học, đơn giản hóa, giới hạn thời gian, tái hiện lỗi thành test, lỗi không tất định, chia đôi và câu chuyện khoảng 130 commit theo Mark Seemann, Code That Fits in Your Head; git bisect và quy ước mã thoát của bisect run theo tài liệu git-scm.com. Đọc ngày 2026-11-24, diễn đạt lại. 200 commit, commit 137, 3 phút mỗi lần build và lỗi múi giờ là minh họa của site. git bisect thật chọn commit theo đồ thị commit (có nhánh, có merge), không đúng điểm giữa như mô phỏng.',
      'Understanding before fixing, the scientific method, simplifying, time-boxing, reproducing defects as tests, non-deterministic defects, bisection and the story of some 130 commits follow Mark Seemann, Code That Fits in Your Head; git bisect and the bisect run exit codes follow the git-scm.com docs. Read on 2026-11-24 and paraphrased. 200 commits, commit 137, 3 minutes per build and the time zone bug are the site\'s illustration. Real git bisect picks commits from the commit graph (with branches and merges), not the exact midpoint as in the simulation.')

    for q, qv, qe, av, ae, wv, we in [
        ('q1', 'Có 500 commit giữa bản tốt và bản xấu. Chia đôi cần tối đa bao nhiêu lần thử?', 'There are 500 commits between a good and a bad release. At most how many bisection probes?', '9.', '9.', '2^8 = 256 < 500 ≤ 512 = 2^9, nên cần 9 lần.', '2^8 = 256 < 500 ≤ 512 = 2^9, so 9 probes.'),
        ('q2', 'Theo Seemann, test tái hiện lỗi mà chạy lại xanh nghĩa là gì?', 'According to Seemann, what does it mean if the reproducing test passes?', 'Giả thuyết sai; cần sửa giả thuyết và thử lại.', 'The hypothesis was wrong; revise it and try again.', 'Test đỏ mới xác nhận đã hiểu lỗi.', 'Only a failing test confirms you understand the defect.'),
        ('q3', 'Trong git bisect run, lệnh trả mã thoát 125 nghĩa là gì?', 'In git bisect run, what does exit code 125 mean?', 'Commit này không thử được, bỏ qua nó.', 'This commit cannot be tested; skip it.', '0 là tốt; 1 tới 127 trừ 125 là xấu.', '0 is good; 1 to 127 except 125 is bad.'),
        ('q4', 'Làm sao biến lỗi "chỉ trên máy tester" thành lỗi tái hiện ở mọi máy?', 'How do you turn a bug "only on the tester\'s phone" into one that reproduces everywhere?', 'Tìm yếu tố môi trường khác nhau và cố định nó trong test.', 'Find the differing environment factor and pin it in the test.', 'Ví dụ truyền Clock và ZoneId thay vì dùng giá trị mặc định của máy.', 'For example, pass a Clock and ZoneId instead of using the device default.')]:
        a(C + '.quiz.%s.q' % q, qv, qe); a(C + '.quiz.%s.a' % q, av, ae); a(C + '.quiz.%s.why' % q, wv, we)
