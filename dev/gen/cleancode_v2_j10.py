# Mã sạch · J10: làm việc nhóm với mã (Phần 4: làm nghề)
# Nguồn: Seemann, Code That Fits in Your Head 9.1.1 (commit message, quy tắc 50/72, câu mệnh lệnh, viết đúng ngữ pháp), 9.1.3 (commit nhỏ),
# 9.2.3 (review là một trong số ít thực hành có tác dụng được ghi nhận; độ trễ review), 9.2.4 (từ chối PR lớn; review quá một giờ kém hiệu quả;
# chi phí chìm), 9.2.5 (câu hỏi gốc "mình có bảo trì nổi không"; người review tự đọc; checklist của Cory House), 9.2.6 (quy tắc cho pull request),
# A.1, A.20; Martin, Clean Craftsmanship ch.1, ch.7 (lập trình cộng tác: cặp, nhóm, review). Đọc 2026-11-24, diễn đạt lại.

SEC_ORDER = {'j10': ['hook', 'small', 'review', 'messages', 'together', 'bugs', 'ex', 'honest']}


def add(a):
    def B(ch, sec, n, field, vi, en=None):
        a('%s.sec.%s.b.%02d.%s' % (ch, sec, n, field), vi, vi if en is None else en)

    a('preset.review', 'Mã sạch · PR nhỏ, review thật, commit message rõ', 'Clean code · small PRs, real reviews, clear commit messages')
    m = lambda k, vi, en=None: a('m.review.' + k, vi, en)
    m('title', 'Một PR 3.000 dòng, hay sáu PR nhỏ', 'One 3,000-line PR, or six small ones')
    m('overview', 'Hai tuần công việc trên app Hẹn Khám: kiểu PhoneNumber, parse ở ranh giới, giờ nhắc theo múi giờ phòng khám, tách FeePolicy, thanh toán MoMo. Cách thứ nhất: một nhánh, một PR 3.000 dòng ở 48 file, commit message "fix". Cách thứ hai: sáu PR, mỗi PR một việc, khoảng 500 dòng, commit message theo quy tắc 50/72. Xem review diễn ra thế nào, rồi hai tuần sau tìm một lỗi.',
      'Two weeks of work on ClinicBook: a PhoneNumber type, parsing at the boundary, reminder times in the clinic time zone, splitting out FeePolicy, MoMo payments. First approach: one branch, one 3,000-line PR across 48 files, commit message "fix". Second: six PRs, one thing each, about 500 lines, commit messages following the 50/72 rule. Watch how review goes, then hunt a bug two weeks later.')
    m('wrapup', 'PR 3.000 dòng được "duyệt" sau 2 phút: không ai đọc nổi nên review thành con dấu. Ba lỗi lọt qua, và hai tuần sau, chia đôi lịch sử chỉ dẫn tới một commit "fix" khổng lồ. Sáu PR nhỏ được review trong ngày, mỗi PR dưới một giờ, theo một checklist; ba lỗi bị bắt trước khi gộp. Commit message có tiêu đề mệnh lệnh dưới 50 ký tự, nên git log --oneline đọc như mục lục, và lỗi hai tuần sau được khoanh vào một commit 530 dòng có giải thích vì sao.',
      'The 3,000-line PR is "approved" after 2 minutes: nobody can read it, so the review becomes a rubber stamp. Three defects slip through, and two weeks later bisecting the history leads to one giant "fix" commit. The six small PRs are reviewed the same day, each in under an hour, against a checklist; three defects are caught before merging. Commit messages have imperative summaries under 50 characters, so git log --oneline reads like a table of contents, and the bug two weeks later is pinned to one 530-line commit that explains why.')
    m('simp.1', 'Số dòng, thời gian review và ba lỗi bị bắt là minh họa. Seemann trích nghiên cứu rằng review quá một giờ kém hiệu quả; site không tự đo điều đó.', 'Line counts, review times and the three caught defects are illustrative. Seemann cites research that reviews longer than an hour are ineffective; the site did not measure that itself.')
    m('simp.2', 'Checklist sáu câu hỏi là gợi ý của Cory House mà Seemann trích, cộng câu hỏi gốc của Seemann; nó không đầy đủ, chỉ cho biết nên nhìn vào đâu.', 'The six-question checklist is Cory House\'s, quoted by Seemann, plus Seemann\'s own core question; it is not exhaustive, only a hint where to look.')
    m('ctl.hint', 'Đổi cách làm rồi đi lại; so cột thời gian review, bảng checklist và độ dài tiêu đề commit.', 'Switch the approach and walk again; compare review times, the checklist and commit summary lengths.')
    m('ctl.case', 'Cách làm', 'Approach')
    for k, vi, en in [('big', 'một PR lớn', 'one big PR'), ('small', 'sáu PR nhỏ', 'six small PRs')]:
        m('ctl.case.' + k, vi, en)
    m('diagramTitle', 'Thay đổi, pull request, review, lịch sử', 'Change, pull request, review, history')
    m('diagramDesc', 'Thay đổi thành PR, PR được review, rồi thành lịch sử git mà người sau đọc lại', 'Changes become PRs, PRs are reviewed, then become the git history later readers come back to')
    for k, vi, en in [('work', 'Hai tuần công việc', 'Two weeks of work'), ('pr', 'Pull request', 'Pull request'), ('review', 'Review', 'Review'), ('log', 'Lịch sử git', 'Git history')]:
        m('n.' + k, vi, en)
    m('met.biggest', 'Dòng trong PR lớn nhất', 'Lines in the largest PR'); m('met.caught', 'Lỗi bắt được khi review', 'Defects caught in review'); m('met.read', 'Dòng phải đọc khi tìm lỗi', 'Lines to read when hunting a bug')
    a('cap.review', 'Công việc thành PR, PR qua review, rồi thành lịch sử git. Nút đỏ là chỗ thông tin bị mất: review không đọc được, hay lịch sử không nói gì.', 'Work becomes PRs, PRs go through review, then become git history. A red node is where information is lost: an unreadable review, or a history that says nothing.')
    S = [
        ('big', 's1', 'Mở một PR: 3.000 dòng, 48 file', 'Open one PR: 3,000 lines, 48 files',
         'Hai tuần làm trên một nhánh; năm việc khác nhau trộn trong một PR, cả định dạng lại mã lẫn thay đổi logic.', 'Two weeks on one branch; five different things mixed in one PR, reformatting and logic changes together.'),
        ('big', 's2', 'Review: "LGTM" sau 2 phút', 'Review: "LGTM" after 2 minutes',
         'Không ai đọc nổi 3.000 dòng. Từ chối thì thấy tiếc hai tuần công, nên người review bấm duyệt. Không câu nào trong checklist được trả lời.', 'Nobody can read 3,000 lines. Rejecting feels like wasting two weeks of work, so the reviewer approves. No checklist question is answered.'),
        ('big', 's3', 'Lịch sử: fix, fix 2, wip', 'History: fix, fix 2, wip',
         'git log --oneline chỉ cho thấy "fix", "fix 2", "wip" và một tiêu đề 55 ký tự kể mọi thứ. Không dòng nào nói vì sao.', 'git log --oneline shows only "fix", "fix 2", "wip" and a 55-character summary listing everything. No line says why.'),
        ('big', 's4', 'Hai tuần sau: lỗi làm tròn phí', 'Two weeks later: a fee rounding bug',
         'Chia đôi lịch sử (chương J7) dẫn tới commit "fix" 3.000 dòng. Phải đọc lại hết để tìm một dòng làm tròn.', 'Bisecting the history (chapter J7) leads to the 3,000-line "fix" commit. All of it must be reread to find one rounding line.'),
        ('small', 's1', 'Mở sáu PR, mỗi PR một việc', 'Open six PRs, one thing each',
         'Từ 420 tới 590 dòng mỗi PR; mỗi PR build được và mọi test xanh; PR định dạng lại mã đứng riêng.', 'From 420 to 590 lines each; each builds and passes every test; the reformatting PR stands alone.'),
        ('small', 's2', 'Review trong ngày, theo checklist', 'Same-day review, against a checklist',
         'Mỗi PR được đọc trong 20 tới 40 phút. Ba lỗi bị bắt trước khi gộp: một nhánh else -> 0L, một ZoneId.systemDefault(), một test thiếu ngày lễ.', 'Each PR is read in 20 to 40 minutes. Three defects are caught before merging: an else -> 0L branch, a ZoneId.systemDefault(), a test missing the holiday.'),
        ('small', 's3', 'Lịch sử đọc như mục lục', 'The history reads like a table of contents',
         'Mỗi tiêu đề là câu mệnh lệnh dưới 50 ký tự; phần thân, nếu có, giải thích vì sao và xuống dòng ở 72 ký tự.', 'Each summary is an imperative sentence under 50 characters; the body, when present, explains why and wraps at 72 characters.'),
        ('small', 's4', 'Hai tuần sau: lỗi khoanh vào một commit 530 dòng', 'Two weeks later: the bug is pinned to one 530-line commit',
         'Chia đôi dẫn tới "Split FeePolicy out of AppointmentManager". Thân commit ghi đã đổi cách làm tròn; lỗi nằm ở đó.', 'Bisection leads to "Split FeePolicy out of AppointmentManager". The commit body says rounding changed; the bug is right there.'),
    ]
    for case, k, tv, te, xv, xe in S:
        sid = case + '.' + k
        m('s.%s.title' % sid, tv, te); m('s.%s.explain' % sid, xv, xe); m('ev.' + sid, tv, te)
    for k, vi, en in [
        ('try', 'Nhìn ba phần: danh sách PR, checklist review, rồi git log. Mỗi bước mở thêm một phần.', 'Look at three parts: the PR list, the review checklist, then git log. Each step opens another part.'),
        ('big.s2', 'Seemann (9.2.4): review chỉ có giá trị khi từ chối là một lựa chọn thật. Ông từng từ chối ngay một PR hàng nghìn dòng ở năm mươi file mà không đọc, rồi chỉ cả nhóm cách làm thay đổi nhỏ. Tiếc công đã bỏ ra là ngụy biện chi phí chìm. [[src:book-seemann]]', 'Seemann (9.2.4): a review is worth something only if rejection is a real option. He once rejected a PR of thousands of lines across fifty files without reading it, then showed the team how to make small changes. Regretting the effort already spent is the sunk cost fallacy. [[src:book-seemann]]'),
        ('big.s3', 'Seemann (9.1.1): commit message là thông điệp gửi tương lai. Diff đã cho biết đổi gì; tiêu đề là mục lục của lịch sử, thân giải thích vì sao. [[src:book-seemann]]', 'Seemann (9.1.1): a commit message is a message to the future. The diff already shows what changed; the summary is the history\'s table of contents and the body explains why. [[src:book-seemann]]'),
        ('big.s4', 'Commit nhỏ làm chia đôi có ích (chương J7): commit tìm ra chỉ chứa ít thay đổi. Commit khổng lồ thì chia đôi xong vẫn phải đọc lại tất cả.', 'Small commits make bisection useful (chapter J7): the commit it finds holds few changes. With a giant commit you still reread everything after bisecting.'),
        ('small.s1', 'Seemann (9.2.6) gom quy tắc cho PR: nhỏ nhất có thể, nhỏ hơn bạn nghĩ; mỗi PR một việc; tránh định dạng lại mã trừ khi PR chỉ làm việc đó; build được; mọi test xanh; có test cho hành vi mới. [[src:book-seemann]]', 'Seemann (9.2.6) lists rules for PRs: as small as possible, smaller than you think; one thing per PR; avoid reformatting unless that is all the PR does; it builds; all tests pass; new behaviour has tests. [[src:book-seemann]]'),
        ('small.s2', 'Seemann (9.2.5): câu hỏi gốc của review là "mình có bảo trì nổi đoạn này không?". Người review tự đọc theo nhịp của mình; tác giả dẫn đi thì dễ thuyết phục người đọc bỏ qua chỗ có vấn đề. [[src:book-seemann]]', 'Seemann (9.2.5): the core review question is "will I be okay maintaining this?". The reviewer reads at their own pace; an author guiding the tour can talk the reader past problems. [[src:book-seemann]]'),
        ('small.s3', 'Quy tắc 50/72 (Seemann, A.1): tiêu đề dạng mệnh lệnh, không quá 50 ký tự; muốn viết thêm thì để trống dòng thứ hai; phần thân xuống dòng ở 72 ký tự. Đây là chuẩn thực tế, không phải chuẩn chính thức. [[src:book-seemann]]', 'The 50/72 rule (Seemann, A.1): an imperative summary of at most 50 characters; for more text leave the second line blank; wrap the body at 72 characters. It is a de facto convention, not an official standard. [[src:book-seemann]]'),
        ('small.s4', 'Seemann (9.2.3): review là một trong số ít thực hành có tác dụng được ghi nhận; bắt lỗi trước khi gọi là xong tránh được việc ngoài kế hoạch về sau. [[src:book-seemann]]', 'Seemann (9.2.3): code review is one of the few practices with documented effects; catching defects before calling work done avoids unplanned work later. [[src:book-seemann]]')]:
        m('co.' + k, vi, en)

    z = lambda k, vi, en=None: a('vz.' + k, vi, en)
    z('tab.review', 'PR, checklist, git log', 'PRs, checklist, git log')
    z('rv.pcap', 'Danh sách pull request.', 'The pull requests.')
    for k, vi, en in [('pr', 'PR', 'PR'), ('lines', 'Dòng', 'Lines'), ('files', 'File', 'Files'), ('min', 'Phút review', 'Review minutes'), ('found', 'Lỗi bắt được', 'Defects caught')]:
        z('rv.col.' + k, vi, en)
    z('rv.ccap', 'Checklist review (câu hỏi gốc của Seemann và sáu câu của Cory House mà ông trích).', 'Review checklist (Seemann\'s core question and the six by Cory House he quotes).')
    for k, vi, en in [('maintain', 'Mình có bảo trì nổi đoạn này không?', 'Will I be okay maintaining this?'), ('works', 'Mã có chạy đúng ý định không?', 'Does the code work as intended?'), ('intent', 'Ý định có rõ không?', 'Is the intent clear?'),
                      ('dup', 'Có trùng lặp không cần thiết không?', 'Is there needless duplication?'), ('exist', 'Có mã sẵn có giải quyết được không?', 'Could existing code have solved this?'), ('simpler', 'Có thể đơn giản hơn không?', 'Could this be simpler?'), ('tests', 'Test có đủ và rõ không?', 'Are the tests comprehensive and clear?')]:
        z('rv.q.' + k, vi, en)
    z('rv.col.q', 'Câu hỏi', 'Question'); z('rv.col.ans', 'Trả lời', 'Answer')
    for k, vi, en in [('skip', 'không ai kiểm', 'nobody checked'), ('yes', 'đã kiểm, ổn', 'checked, fine'),
                      ('works', 'đã kiểm: bắt được else -> 0L tính phí MoMo bằng 0', 'checked: caught an else -> 0L charging MoMo 0'),
                      ('simpler', 'đã kiểm: bỏ ZoneId.systemDefault(), dùng múi giờ phòng khám', 'checked: drop ZoneId.systemDefault(), use the clinic zone'),
                      ('tests', 'đã kiểm: thiếu test ngày lễ, đã thêm', 'checked: a holiday test was missing, now added')]:
        z('rv.a.' + k, vi, en)
    z('rv.lcap', 'git log --oneline (tiêu đề commit; số là độ dài, quy tắc 50/72 cho phép tối đa 50).', 'git log --oneline (commit summaries; the number is the length, the 50/72 rule allows at most 50).')
    z('rv.bug', 'Chia đôi dẫn tới commit {c}: phải đọc {n} dòng.', 'Bisection leads to commit {c}: {n} lines to read.')
    z('rv.legend', 'Ô gạch đỏ: PR quá lớn để review, câu hỏi không ai kiểm, hay tiêu đề vô nghĩa hoặc quá 50 ký tự. Ô đậm: đạt.', 'Red hatched: a PR too big to review, an unchecked question, or a meaningless summary or one over 50 characters. Bold: fine.')

    C = 'j10'
    a(C + '.title', 'Làm việc nhóm với mã', 'Working on code as a team')
    a(C + '.essence', 'PR nhỏ, mỗi PR một việc, build được và mọi test xanh. PR lớn biến review thành con dấu: không ai đọc nổi, và tiếc công nên không ai từ chối.\nReview thật: người review tự đọc, hỏi "mình có bảo trì nổi đoạn này không?", dùng checklist, và từ chối phải là một lựa chọn thật. Review trong ngày, mỗi lần dưới một giờ.\nCommit message theo quy tắc 50/72: tiêu đề mệnh lệnh không quá 50 ký tự, thân giải thích vì sao, xuống dòng ở 72. Lịch sử git là tài liệu người sau đọc lại khi tìm lỗi.',
      'Small PRs, one thing each, building and passing every test. Big PRs turn review into a rubber stamp: nobody can read them, and regret for the effort means nobody rejects them.\nReal review: the reviewer reads alone, asks "will I be okay maintaining this?", uses a checklist, and rejection is a real option. Review the same day, under an hour each time.\nCommit messages follow 50/72: an imperative summary of at most 50 characters, a body explaining why, wrapped at 72. Git history is the documentation the next person reads when hunting a bug.')
    a(C + '.goal.g1', 'Đã thấy git log của hai cách', 'Saw both git logs')
    a(C + '.goal.g2', 'Đã thấy lỗi hai tuần sau', 'Saw the bug two weeks later')
    a(C + '.sim.cleancode.review', 'một PR lớn hay sáu PR nhỏ', 'one big PR or six small ones')

    S_ = 'hook'
    a(C + '.sec.%s.title' % S_, 'Đoán trước khi đọc', 'Predict before reading')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'predict', 'Một PR 3.000 dòng được duyệt sau 2 phút; một PR 30 dòng nhận mười bình luận. Vì sao thường như vậy, và nó nói gì về cách chia công việc?',
      'A 3,000-line PR is approved in 2 minutes; a 30-line PR gets ten comments. Why does this usually happen, and what does it say about how work is split?')
    B(C, S_, 1, 'ans', 'PR nhỏ thì đọc được, nên người review thật sự góp ý. PR lớn thì không đọc nổi, và từ chối hai tuần công thì ngại, nên review thành con dấu. Muốn review có tác dụng thì phải chia việc thành PR đủ nhỏ để đọc trong chưa tới một giờ. Mô phỏng ngay dưới so hai cách cho cùng hai tuần công việc.',
      'A small PR is readable, so reviewers genuinely engage. A big one is unreadable, and rejecting two weeks of work feels awkward, so review becomes a rubber stamp. For review to work, split work into PRs small enough to read in under an hour. The simulation just below compares both for the same two weeks of work.')

    S_ = 'small'
    a(C + '.sec.%s.title' % S_, 'Commit nhỏ, PR nhỏ', 'Small commits, small PRs')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'p', 'Seemann (9.1.3): lập trình có nhiều bất định, có buổi viết được nhiều, có buổi phải bỏ mã đã viết. Commit nhiều và nhỏ thì sai lầm rẻ: bỏ commit gần nhất chỉ bỏ đúng thứ muốn bỏ. Với PR (9.2.6), ông gom quy tắc: nhỏ nhất có thể, nhỏ hơn bạn nghĩ; mỗi PR một việc; tránh định dạng lại mã trừ khi PR chỉ làm việc đó; build được; mọi test xanh; có test cho hành vi mới. [[src:book-seemann]]',
      'Seemann (9.1.3): programming is full of variance; some sessions produce a lot, others end with code thrown away. Many small commits make mistakes cheap: dropping the last commit drops only what you want gone. For PRs (9.2.6) he lists rules: as small as possible, smaller than you think; one thing per PR; avoid reformatting unless that is all it does; it builds; all tests pass; new behaviour has tests. [[src:book-seemann]]')
    B(C, S_, 2, 'p', 'Ông kể lần nhận một PR hàng nghìn dòng ở năm mươi file từ một người đã im lặng hai tuần, và từ chối ngay vì quá lớn, rồi chỉ cả nhóm cách làm thay đổi nhỏ. Từ chối vài giờ công thì dễ chấp nhận hơn từ chối vài tuần, thêm một lý do để mỗi thay đổi chỉ khoảng nửa ngày công. Ông cũng trích nghiên cứu rằng review quá một giờ thì kém hiệu quả. [[src:book-seemann]]',
      'He recounts receiving a PR of thousands of lines across fifty files from someone silent for two weeks, rejecting it at once as too big, then showing the team how to make small changes. Rejecting hours of work is easier to accept than rejecting weeks, one more reason to keep each change to about half a day. He also cites research that reviews longer than an hour are ineffective. [[src:book-seemann]]')

    S_ = 'review'
    a(C + '.sec.%s.title' % S_, 'Review thật, không phải con dấu', 'Real review, not a rubber stamp')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'p', 'Seemann (9.2.3) gọi review là một trong số ít thực hành có tác dụng được ghi nhận, nhưng nhiều nơi bỏ qua vì sợ chậm. Ông cho rằng không review thì lỗi lộ ra muộn thành việc ngoài kế hoạch, kéo theo làm đêm, trễ hạn và vòng lặp chữa cháy. Lời giải không phải bỏ review mà giảm độ trễ: đưa review vào nhịp làm việc hằng ngày. [[src:book-seemann]]',
      'Seemann (9.2.3) calls code review one of the few practices with documented effects, yet many organisations skip it fearing slowness. In his view skipping it turns late-found defects into unplanned work, then overtime, missed deadlines and a firefighting loop. The answer is not dropping review but cutting its latency: make review part of the daily rhythm. [[src:book-seemann]]')
    B(C, S_, 2, 'p', 'Câu hỏi gốc (9.2.5): "Mình có bảo trì nổi đoạn này không?". Tiêu chí quan trọng nhất là mã có đọc được, có vừa trong đầu không (chương J1). Người review tự đọc theo nhịp của mình, vì tác giả vừa viết nên không đánh giá được độ dễ đọc, và nếu tác giả dẫn đi thì dễ thuyết phục người đọc bỏ qua chỗ có vấn đề. Đừng bắt bẻ định dạng hay tên biến nhỏ nhặt, trừ lỗi chính tả trong API công khai vì sửa về sau là thay đổi phá vỡ. Mục tiêu không phải hạ tác giả mà là thống nhất cách đi tiếp. [[src:book-seemann]]',
      'The core question (9.2.5): "Will I be okay maintaining this?". The most important criterion is readability, whether it fits in your head (chapter J1). The reviewer reads alone at their own pace, because the author just wrote it and cannot judge readability, and an author guiding the tour can talk the reader past problems. Do not nitpick formatting or minor variable names, except typos in public APIs, since fixing those later is a breaking change. The goal is not to hurt the author but to agree on how to move forward. [[src:book-seemann]]')
    B(C, S_, 3, 'note', 'Clean Code ch.17 (danh mục mùi và heuristic) dùng được như bảng tra khi review: tham số cờ, trùng lặp, hàm làm nhiều việc, test thiếu. Nó là gợi ý nhìn vào đâu, không phải luật để chấm điểm.',
      'Clean Code ch.17 (the smells and heuristics catalogue) works as a lookup table while reviewing: flag arguments, duplication, functions doing many things, insufficient tests. It suggests where to look; it is not a scoring rulebook.')
    B(C, S_, 3, 'kind', 'source')

    S_ = 'messages'
    a(C + '.sec.%s.title' % S_, 'Commit message: quy tắc 50/72', 'Commit messages: the 50/72 rule')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'p', 'Seemann (9.1.1, A.1) giới thiệu quy tắc 50/72, một chuẩn thực tế chứ không chính thức: tiêu đề dạng mệnh lệnh, không quá 50 ký tự; muốn viết thêm thì để trống dòng thứ hai; phần thân xuống dòng ở 72 ký tự. Lý do là cách các công cụ git hiển thị, như git log --oneline chỉ hiện tiêu đề. Diff đã cho biết đổi gì, nên thân commit nên nói vì sao. Ông cũng khuyên viết đúng chính tả, ngữ pháp, vì lỗi chính tả làm việc tìm kiếm trong lịch sử thất bại. [[src:book-seemann]]',
      'Seemann (9.1.1, A.1) presents the 50/72 rule, a de facto convention rather than an official standard: an imperative summary of at most 50 characters; for more text leave the second line blank; wrap the body at 72 characters. The reason is how git tools display history, such as git log --oneline showing only summaries. The diff already shows what changed, so the body should say why. He also asks for proper spelling and grammar, since typos make searching the history fail. [[src:book-seemann]]')
    B(C, S_, 2, 'kt', 'Split FeePolicy out of AppointmentManager\n\nAccounting changes fee rules monthly; the front desk changes\nscheduling. Keeping both in one class caused merge conflicts\nand one regression in reminders (see #412).\n\nFee rounding now uses roundToLong() instead of Long division,\nmatching the invoice service.',
      'Split FeePolicy out of AppointmentManager\n\nAccounting changes fee rules monthly; the front desk changes\nscheduling. Keeping both in one class caused merge conflicts\nand one regression in reminders (see #412).\n\nFee rounding now uses roundToLong() instead of Long division,\nmatching the invoice service.')
    B(C, S_, 2, 'lang', 'text')

    S_ = 'together'
    a(C + '.sec.%s.title' % S_, 'Lập trình cùng nhau và sở hữu mã chung', 'Programming together and collective ownership')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'p', 'Martin (Clean Craftsmanship ch.1) xếp lập trình cộng tác vào năm kỷ luật của nghề: lập trình cặp, lập trình nhóm, review, cùng bàn ý tưởng. Ông gọi nó là kỷ luật ít kỹ thuật và ít quy định nhất, nhưng có thể là quan trọng nhất, vì xây được một nhóm làm việc hiệu quả là điều hiếm. Seemann (9.2) nói theo hướng tương tự: khi tác giả và người review đều sẵn lòng bảo trì một đoạn mã, nhóm đang đi tới chỗ mã là của chung, không phải của riêng ai. [[src:book-craft]] [[src:book-seemann]]',
      'Martin (Clean Craftsmanship ch.1) lists collaborative programming among the five disciplines of the craft: pair programming, mob programming, code review, brainstorming. He calls it the least technical and least prescriptive discipline, yet perhaps the most important, since building an effective team is rare. Seemann (9.2) points the same way: when both author and reviewer are willing to maintain a piece of code, the team is moving toward collective ownership rather than individual turf. [[src:book-craft]] [[src:book-seemann]]')

    S_ = 'bugs'
    a(C + '.sec.%s.title' % S_, 'Hai lỗi hay gặp', 'Two common bugs')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'bug', 'PR 3.000 dòng được duyệt nhanh, ba lỗi lọt ra bản phát hành.', 'A 3,000-line PR is approved quickly and three defects reach the release.')
    B(C, S_, 1, 'cause', 'Không ai đọc nổi PR đó trong một lần, và ngại từ chối hai tuần công; review thành con dấu.', 'Nobody can read that PR in one sitting, and rejecting two weeks of work feels awkward; review becomes a rubber stamp.')
    B(C, S_, 1, 'fix', 'Từ chối PR quá lớn và chia lại: mỗi PR một việc, khoảng nửa ngày công, build được, test xanh; review trong ngày theo checklist.', 'Reject the oversized PR and split it: one thing per PR, about half a day of work, building and green; same-day review against a checklist.')
    B(C, S_, 2, 'bug', 'Tìm nguyên nhân một lỗi, git log toàn "fix", "update", "wip".', 'Hunting a bug, git log shows nothing but "fix", "update", "wip".')
    B(C, S_, 2, 'cause', 'Commit message chỉ để vượt qua việc git không nhận message rỗng; không ai viết vì sao.', 'Commit messages were written only to get past git refusing empty ones; nobody wrote why.')
    B(C, S_, 2, 'fix', 'Theo quy tắc 50/72: tiêu đề mệnh lệnh nói việc gì, thân nói vì sao; nếu cần, gộp và viết lại commit trên nhánh của mình trước khi mở PR.', 'Follow 50/72: an imperative summary saying what, a body saying why; if needed, squash and rewrite commits on your own branch before opening the PR.')

    S_ = 'ex'
    a(C + '.sec.%s.title' % S_, 'Bài tập', 'Exercise')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'ex', 'Viết lại bốn commit message dưới đây theo quy tắc 50/72. Commit thứ tư cần thêm thân giải thích vì sao.', 'Rewrite the four commit messages below to follow 50/72. The fourth needs a body explaining why.')
    B(C, S_, 1, 'exkt', 'fixed bug\nupdate\nAdded the new MoMo payment method and also changed fee rounding and some formatting\nchange timezone')
    B(C, S_, 1, 'hint', 'Một commit có đang làm nhiều việc không? Tiêu đề mệnh lệnh bắt đầu bằng động từ: Add, Fix, Use, Split.', 'Is one commit doing several things? Imperative summaries start with a verb: Add, Fix, Use, Split.')
    B(C, S_, 1, 'sol', 'Hai commit đầu cần biết nội dung thật để đặt tên, ví dụ "Fix double booking on retry" và "Bump Room to 2.6.1". Commit thứ ba làm ba việc: tách thành "Add MoMo payment method", "Round fees with roundToLong()" và một commit định dạng riêng. Commit thứ tư: "Schedule reminders in the clinic time zone", thân giải thích lời nhắc từng lệch 7 tiếng trên máy UTC+7 vì dùng ZoneId.systemDefault().',
      'The first two need their real content to be named, for example "Fix double booking on retry" and "Bump Room to 2.6.1". The third does three things: split into "Add MoMo payment method", "Round fees with roundToLong()" and a separate formatting commit. The fourth: "Schedule reminders in the clinic time zone", with a body explaining reminders were 7 hours off on UTC+7 phones because of ZoneId.systemDefault().')

    S_ = 'honest'
    a(C + '.sec.%s.title' % S_, 'Chương này giản lược những gì', 'What this chapter simplifies')
    a(C + '.sec.%s.badge' % S_, 'simplified')
    B(C, S_, 1, 'p', 'Commit nhỏ, quy tắc 50/72, review và độ trễ review, từ chối PR lớn, câu hỏi gốc của review, checklist của Cory House và quy tắc cho PR theo Mark Seemann, Code That Fits in Your Head ch.9, A.1, A.20; lập trình cộng tác theo Robert C. Martin, Clean Craftsmanship ch.1. Đọc ngày 2026-11-24, diễn đạt lại. Các nghiên cứu về hiệu quả review là Seemann trích, site không tự đọc hay đo. Số dòng, số phút, ba lỗi bị bắt, các commit message là minh họa. Quy trình Agile (planning, standup, story point) nằm ngoài phạm vi theo dàn ý.',
      'Small commits, the 50/72 rule, review and its latency, rejecting big PRs, the core review question, Cory House\'s checklist and the PR rules follow Mark Seemann, Code That Fits in Your Head ch.9, A.1, A.20; collaborative programming follows Robert C. Martin, Clean Craftsmanship ch.1. Read on 2026-11-24 and paraphrased. The research on review effectiveness is cited by Seemann; the site did not read or measure it. Line counts, minutes, the three caught defects and the commit messages are illustrative. Agile process (planning, stand-ups, story points) is out of scope per the outline.')

    for q, qv, qe, av, ae, wv, we in [
        ('q1', 'Theo quy tắc 50/72, tiêu đề commit dài tối đa bao nhiêu ký tự?', 'Under the 50/72 rule, how long may a commit summary be?', '50 ký tự.', '50 characters.', 'Thân commit xuống dòng ở 72 ký tự; dòng thứ hai để trống.', 'The body wraps at 72; the second line stays blank.'),
        ('q2', 'Câu hỏi gốc của review theo Seemann là gì?', 'What is Seemann\'s core review question?', '"Mình có bảo trì nổi đoạn này không?"', '"Will I be okay maintaining this?"', 'Tiêu chí quan trọng nhất là mã đọc được, vừa trong đầu.', 'The most important criterion is readability: does it fit in your head.'),
        ('q3', 'Vì sao PR lớn hay được duyệt nhanh?', 'Why do big PRs often get approved quickly?', 'Không đọc nổi, và ngại từ chối nhiều công sức (chi phí chìm).', 'They cannot be read, and rejecting so much effort feels bad (sunk cost).', 'Review chỉ có giá trị khi từ chối là lựa chọn thật.', 'Review is only worth something when rejection is a real option.'),
        ('q4', 'Thân commit nên tập trung nói gì?', 'What should a commit body focus on?', 'Vì sao thay đổi.', 'Why the change was made.', 'Diff đã cho biết đổi gì.', 'The diff already shows what changed.')]:
        a(C + '.quiz.%s.q' % q, qv, qe); a(C + '.quiz.%s.a' % q, av, ae); a(C + '.quiz.%s.why' % q, wv, we)
