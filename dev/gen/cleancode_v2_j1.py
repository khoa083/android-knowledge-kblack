# Mã sạch · J1: mã phải vừa trong đầu (Phần 1: mã đọc được)
# Nguồn: Mark Seemann, Code That Fits in Your Head ch.3 (3.2.1), ch.7 (7.1.1–7.1.3, 7.2.1, 7.2.7), phụ lục A.2, A.7, A.8;
# Robert C. Martin, Clean Code ch.3 (Small!, Do One Thing, One Level of Abstraction, Stepdown Rule). Đọc 2026-11-24, diễn đạt lại.
# Mọi ngưỡng (7, 80/24, 20 dòng) là heuristic của tác giả. Cách đếm cho Kotlin là quy ước của site theo cách của Seemann.

SEC_ORDER = {'j1': ['hook', 'seven', 'count', 'decompose', 'limits', 'bugs', 'ex', 'honest']}


def add(a):
    def B(ch, sec, n, field, vi, en=None):
        a('%s.sec.%s.b.%02d.%s' % (ch, sec, n, field), vi, vi if en is None else en)

    a('preset.fits', 'Mã sạch · mã vừa trong đầu', 'Clean code · code that fits in your head')
    m = lambda k, vi, en=None: a('m.fits.' + k, vi, en)
    m('title', 'Một hàm dài, hay vài hàm nhỏ đọc từ trên xuống', 'One long function, or a few small ones read top-down')
    m('overview', 'Hàm bookAppointment của app Hẹn Khám kiểm tra đầu vào, tính phí, lưu lịch hẹn và hẹn giờ gửi nhắc. Đọc nó từng đoạn và đếm hai thứ theo cách của Seemann: số đường đi qua mã (cyclomatic complexity) và số biến phải theo dõi. Ở bước cuối, một yêu cầu mới về phí được thêm vào: xem nó làm hỏng gì ở mỗi cách viết.',
      'ClinicBook\'s bookAppointment function checks the input, computes the fee, saves the booking and schedules the reminder. Read it part by part and count two things the way Seemann does: the number of paths through the code (cyclomatic complexity) and the number of variables to keep track of. In the last step a new fee requirement is added: see what it breaks in each version.')
    m('wrapup', 'Hàm dài chỉ 19 dòng, dưới ngưỡng 24 dòng của Seemann, nhưng có 9 đường đi và 13 biến: quá nhiều thứ phải giữ trong đầu cùng lúc. Người sửa phần phí thêm một lệnh return sớm và không thấy nó bỏ qua việc hẹn nhắc ở cuối hàm. Khi tách thành vài hàm nhỏ, mỗi hàm có 2 hoặc 3 đường đi và tối đa 6 biến; yêu cầu mới chỉ chạm vào feeFor, còn việc hẹn nhắc nằm ở chỗ khác nên không thể bị bỏ qua.',
      'The long function is only 19 lines, under Seemann\'s 24-line threshold, yet it has 9 paths and 13 variables: too much to hold in your head at once. Whoever edits the fee part adds an early return and does not see that it skips the reminder at the end. Split into a few small functions, each has 2 or 3 paths and at most 6 variables; the new requirement touches only feeFor, and the reminder lives elsewhere, so it cannot be skipped.')
    m('simp.1', 'Hàm thật trong lỗi dẫn dắt dài 120 dòng; mô phỏng rút gọn còn 19 dòng để đọc được trên màn hình. Ngưỡng 7 là con số tượng trưng của Seemann, không phải giới hạn cứng của não.', 'The real function in the leading bug is 120 lines; the simulation shortens it to 19 so it fits on screen. The threshold of 7 is Seemann\'s symbolic number, not a hard limit of the brain.')
    m('simp.2', 'Cách đếm là quy ước của site theo cách của Seemann: bắt đầu từ 1, cộng 1 cho mỗi if và for. Đoạn mã chỉ dùng if và for để con số không phụ thuộc công cụ đo; ?:, && và || cũng rẽ nhánh nhưng các công cụ đếm chúng khác nhau.', 'The counting is the site\'s convention following Seemann\'s method: start at 1, add 1 for each if and for. The code uses only if and for so the number does not depend on the tool; ?:, && and || also branch, but tools count them differently.')
    m('ctl.hint', 'Đổi cách viết rồi đi lại; so hai hàng ô ở hình chính và bảng đếm đường đi.', 'Switch the version and walk again; compare the two rows of slots in the main view and the path-count table.')
    m('ctl.case', 'Cách viết', 'Version')
    for k, vi, en in [('long', 'một hàm dài 19 dòng', 'one 19-line function'), ('split', 'tách thành ba hàm nhỏ', 'split into three small functions')]:
        m('ctl.case.' + k, vi, en)
    m('diagramTitle', 'Mã, bộ nhớ làm việc, yêu cầu mới, việc hẹn nhắc', 'Code, working memory, new requirement, reminder')
    m('diagramDesc', 'Người đọc nạp mã vào bộ nhớ làm việc; yêu cầu mới sửa mã; mã đã sửa có còn hẹn nhắc không', 'The reader loads code into working memory; a new requirement edits the code; does the edited code still schedule the reminder')
    for k, vi, en in [('code', 'Mã đang đọc', 'Code being read'), ('head', 'Bộ nhớ làm việc', 'Working memory'), ('change', 'Yêu cầu mới', 'New requirement'), ('remind', 'Hẹn nhắc', 'Reminder')]:
        m('n.' + k, vi, en)
    m('met.paths', 'Đường đi của hàm đang đọc', 'Paths in the function being read'); m('met.vars', 'Biến phải theo dõi', 'Variables to track'); m('met.skipped', 'Nhánh bỏ qua hẹn nhắc', 'Branches that skip the reminder')
    a('cap.fits', 'Mã bên trái nạp vào bộ nhớ làm việc; yêu cầu mới ở dưới sửa mã; bên phải là việc hẹn nhắc. Khi bộ nhớ làm việc đỏ, người đọc đang phải giữ quá 7 thứ.', 'Code on the left loads into working memory; the new requirement below edits the code; the reminder is on the right. When working memory turns red, the reader is holding more than 7 things.')
    S = [
        ('long', 's1', 'Đọc dòng 1–6: kiểm tra đầu vào', 'Read lines 1–6: input checks',
         'Ba lệnh if, năm biến: req, doctors, doctor, slot, clock. Vẫn vừa trong đầu.', 'Three ifs, five variables: req, doctors, doctor, slot, clock. Still fits in your head.'),
        ('long', 's2', 'Đọc dòng 7–13: tính phí', 'Read lines 7–13: the fee',
         'Thêm ba if và một for: 8 đường đi. Thêm fee, vouchers, code, v: 9 biến. Cả hai đã quá 7 mà hàm mới đi được hai phần ba.', 'Three more ifs and a for: 8 paths. Add fee, vouchers, code, v: 9 variables. Both are past 7 and the function is only two-thirds done.'),
        ('long', 's3', 'Đọc dòng 14–18: lưu và hẹn nhắc', 'Read lines 14–18: save and remind',
         'Thêm một if: 9 đường đi; thêm booking, repo, hours, reminders: 13 biến. Hàm chỉ 19 dòng, dưới ngưỡng 24 dòng, nên đếm dòng không thấy vấn đề.', 'One more if: 9 paths; add booking, repo, hours, reminders: 13 variables. The function is only 19 lines, under the 24-line threshold, so counting lines misses the problem.'),
        ('long', 's4', 'Yêu cầu mới: phí 0 đ thì lưu luôn và trả về', 'New requirement: a 0 fee saves and returns at once',
         'Người sửa chỉ nhìn phần phí, chèn một if có return sớm sau vòng for. Mọi lịch hẹn miễn phí giờ bỏ qua dòng 21: không ai được nhắc.', 'The editor looks only at the fee part and inserts an if with an early return after the for loop. Every free booking now skips line 21: nobody gets a reminder.'),
        ('split', 's1', 'Đọc bookAppointment: sáu dòng, từ trên xuống', 'Read bookAppointment: six lines, top-down',
         'Một if, sáu biến. Mỗi dòng là một bước ở cùng mức trừu tượng: kiểm tra, tính phí, lưu, hẹn nhắc.', 'One if, six variables. Each line is a step at the same level of abstraction: check, compute the fee, save, remind.'),
        ('split', 's2', 'Đọc validate khi cần chi tiết', 'Read validate when you need the details',
         'Hai if, ba biến. Đọc hàm này không cần nhớ phần phí hay phần hẹn nhắc.', 'Two ifs, three variables. Reading it does not require remembering the fee or the reminder.'),
        ('split', 's3', 'Đọc feeFor', 'Read feeFor',
         'Hai if, bốn biến. Vòng lặp voucher nằm trong vouchers.totalFor: độ phức tạp không biến mất, nó được chia ra chỗ khác.', 'Two ifs, four variables. The voucher loop lives in vouchers.totalFor: the complexity does not vanish, it moves elsewhere.'),
        ('split', 's4', 'Cùng yêu cầu mới, sửa trong feeFor', 'The same requirement, edited in feeFor',
         'Phí không âm: coerceAtLeast(0) ở dòng 21. bookAppointment không đổi, dòng hẹn nhắc vẫn chạy cho mọi lịch hẹn.', 'The fee never goes below zero: coerceAtLeast(0) on line 21. bookAppointment is unchanged, and the reminder line still runs for every booking.'),
    ]
    for case, k, tv, te, xv, xe in S:
        sid = case + '.' + k
        m('s.%s.title' % sid, tv, te); m('s.%s.explain' % sid, xv, xe); m('ev.' + sid, tv, te)
    for k, vi, en in [
        ('try', 'Đi bốn bước; mỗi bước đọc thêm một đoạn mã. Để ý hai hàng ô: đường đi và biến.', 'Walk four steps; each reads one more part of the code. Watch the two rows of slots: paths and variables.'),
        ('long.s2', 'Seemann: đặt một ngưỡng và theo dõi nó; vượt 7 thì tách hàm trước khi thêm nhánh mới. Con số 7 là tượng trưng; điều có tác dụng là có ngưỡng. [[src:book-seemann]]', 'Seemann: agree on a threshold and watch it; past 7, decompose before adding a new branch. The 7 is symbolic; what works is having a threshold. [[src:book-seemann]]'),
        ('long.s3', 'Seemann: ông không thoải mái khi hàm C# dài gần 20 dòng và chọn 24 làm ngưỡng tùy ý (khung 80 × 24 của màn hình VT100). Số dòng chỉ là một góc nhìn; hàm này lọt qua ngưỡng dòng nhưng không qua ngưỡng đường đi. [[src:book-seemann]]', 'Seemann: he gets uncomfortable when a C# method nears 20 lines and picks 24 as an arbitrary threshold (the 80 × 24 VT100 screen). Line count is one view; this function passes the line threshold but not the path threshold. [[src:book-seemann]]'),
        ('long.s4', 'Một return sớm ở giữa hàm dài bỏ qua mọi thứ phía sau nó. Người sửa không sai vì ẩu: phần phía sau nằm ngoài những gì đầu họ giữ được lúc đó.', 'An early return in the middle of a long function skips everything after it. The editor was not careless: what came after was outside what their head could hold at that moment.'),
        ('split.s1', 'Martin (Clean Code): mọi câu lệnh trong một hàm nên ở cùng một mức trừu tượng, và mã nên đọc từ trên xuống như một câu chuyện, mỗi hàm theo sau bởi các hàm ở mức thấp hơn (stepdown rule). [[src:book-cleancode]]', 'Martin (Clean Code): every statement in a function should sit at one level of abstraction, and code should read top-down like a narrative, each function followed by those one level below (the stepdown rule). [[src:book-cleancode]]'),
        ('split.s2', 'Seemann: đếm cả biến cục bộ, tham số và field của lớp. validate dùng req, clock và doctors: ba thứ. [[src:book-seemann]]', 'Seemann: count local variables, parameters and class fields. validate uses req, clock and doctors: three things. [[src:book-seemann]]'),
        ('split.s3', 'Seemann: cyclomatic complexity cũng là số test tối thiểu để đi qua mọi đường của hàm. feeFor có 3 đường nên cần ít nhất 3 test. [[src:book-seemann]]', 'Seemann: cyclomatic complexity is also the minimum number of tests to cover every path of a function. feeFor has 3 paths, so it needs at least 3 tests. [[src:book-seemann]]'),
        ('split.s4', 'Thay đổi rơi vào đúng một hàm nhỏ. Những gì nằm ngoài hàm đó không cần giữ trong đầu, nên không thể vô tình bị bỏ qua.', 'The change lands in exactly one small function. Whatever lives outside it does not need to be held in your head, so it cannot be skipped by accident.')]:
        m('co.' + k, vi, en)

    z = lambda k, vi, en=None: a('vz.' + k, vi, en)
    z('tab.fits', 'Bộ nhớ làm việc', 'Working memory')
    z('fits.cap', 'Hàm đang đọc: {fn}. Mỗi ô là một thứ người đọc phải giữ trong đầu; hàng 7 ô là ngưỡng của Seemann, hàng ô đỏ bên dưới là phần vượt ngưỡng.', 'Function being read: {fn}. Each slot is one thing the reader must hold in their head; the row of 7 slots is Seemann\'s threshold, the red row below is what goes beyond it.')
    z('fits.row.paths', 'Đường đi: {n}', 'Paths: {n}')
    z('fits.row.vars', 'Biến: {n}', 'Variables: {n}')
    z('fits.limit', 'vượt ngưỡng 7', 'past the threshold of 7')
    z('fits.start', 'bắt đầu', 'start')
    z('fits.empty', 'trống', 'empty')
    z('fits.kind.param', 'tham số', 'param'); z('fits.kind.field', 'field', 'field'); z('fits.kind.local', 'cục bộ', 'local')
    z('fits.lines', 'Số dòng: {n} (ngưỡng 24 dòng của Seemann: {verdict})', 'Lines: {n} (Seemann\'s 24-line threshold: {verdict})')
    z('fits.lines.ok', 'chưa vượt', 'not exceeded'); z('fits.lines.over', 'vượt', 'exceeded')
    z('fits.tcap', 'Đếm đường đi theo cách của Seemann: bắt đầu từ 1, mỗi if hay for cộng 1. Hàng mới là phần vừa đọc ở bước này.', 'Counting paths Seemann\'s way: start at 1, each if or for adds 1. New rows are what this step just read.')
    for k, vi, en in [('fn', 'Hàm', 'Function'), ('line', 'Dòng', 'Line'), ('what', 'Cấu trúc', 'Construct'), ('sum', 'Tổng', 'Total')]:
        z('fits.col.' + k, vi, en)
    z('fits.what.start', 'bắt đầu: 1 đường', 'start: 1 path')
    z('fits.what.if', 'if', 'if'); z('fits.what.for', 'for', 'for')
    z('fits.skipped', 'Dòng {line} (hẹn nhắc) bị bỏ qua khi phí bằng 0', 'Line {line} (the reminder) is skipped when the fee is 0')
    z('fits.kept', 'Dòng {line} (hẹn nhắc) vẫn chạy cho mọi lịch hẹn', 'Line {line} (the reminder) still runs for every booking')
    z('fits.legend', 'Viền đậm: thứ vừa thêm ở bước này. Ô gạch đỏ: vượt ngưỡng 7. Ô nét đứt: còn trống. Ở bảng đếm, ô trống ở cột Hàm nghĩa là cùng hàm với hàng trên.', 'Bold outline: added in this step. Red hatched slot: beyond the threshold of 7. Dashed slot: still empty. In the count table, a blank Function cell means the same function as the row above.')

    C = 'j1'
    a(C + '.title', 'Mã phải vừa trong đầu', 'Code that fits in your head')
    a(C + '.essence', 'Khi đọc mã, người đọc chạy thử nó trong đầu, mà trí nhớ ngắn hạn chỉ giữ được vài thứ cùng lúc. Seemann dùng con số 7 làm ngưỡng tượng trưng.\nĐếm hai thứ: số đường đi qua hàm (cyclomatic complexity: bắt đầu từ 1, mỗi if hay for cộng 1) và số biến phải theo dõi (cục bộ, tham số, field). Số dòng ít không có nghĩa là đơn giản.\nKhi vượt ngưỡng, tách hàm sao cho mỗi hàm làm một việc ở một mức trừu tượng, đọc từ trên xuống. Độ phức tạp không biến mất, nhưng mỗi lần chỉ cần giữ một phần.',
      'When you read code you run it in your head, and short-term memory holds only a few things at once. Seemann uses 7 as a symbolic threshold.\nCount two things: the paths through a function (cyclomatic complexity: start at 1, each if or for adds 1) and the variables to track (locals, parameters, fields). Few lines does not mean simple.\nPast the threshold, split the function so each does one thing at one level of abstraction, read top-down. The complexity does not vanish, but you only need to hold one part at a time.')
    a(C + '.goal.g1', 'Đã đếm hàm dài vượt ngưỡng', 'Counted the long function past the threshold')
    a(C + '.goal.g2', 'Đã thấy yêu cầu mới làm hỏng gì', 'Saw what the new requirement breaks')
    a(C + '.sim.cleancode.fits', 'một hàm dài hay vài hàm nhỏ', 'one long function or a few small ones')

    S_ = 'hook'
    a(C + '.sec.%s.title' % S_, 'Đoán trước khi đọc', 'Predict before reading')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'predict', 'Hàm bookAppointment dài 120 dòng: kiểm tra đầu vào, tính phí, lưu lịch hẹn, hẹn giờ gửi nhắc. Một đồng nghiệp sửa phần tính phí, test phần phí đều xanh, nhưng tuần sau phòng khám báo nhiều bệnh nhân không nhận được tin nhắc. Chuyện gì có thể đã xảy ra, và vì sao review không thấy?',
      'The bookAppointment function is 120 lines: input checks, the fee, saving the booking, scheduling the reminder. A colleague edits the fee part, the fee tests are green, yet the next week the clinic reports many patients got no reminder. What could have happened, and why did review miss it?')
    B(C, S_, 1, 'ans', 'Một kiểu rất hay gặp: thêm một nhánh có return sớm ở phần phí, và nhánh đó bỏ qua phần hẹn nhắc ở cuối hàm. Người sửa và người review đều chỉ giữ trong đầu phần phí; phần hẹn nhắc nằm ngoài tầm nhìn đó. Mô phỏng ngay dưới cho bạn đếm xem hàm đó phải giữ bao nhiêu thứ cùng lúc.',
      'A very common pattern: adding a branch with an early return in the fee part, and that branch skips the reminder at the end of the function. The editor and the reviewer each held only the fee part in their heads; the reminder was outside that view. The simulation just below lets you count how many things that function makes you hold at once.')

    S_ = 'seven'
    a(C + '.sec.%s.title' % S_, 'Bộ nhớ làm việc và con số 7', 'Working memory and the number 7')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'p', 'Seemann lập luận: máy tính giữ hàng triệu thứ trong RAM, còn trí nhớ ngắn hạn của người chỉ giữ khoảng bốn tới bảy mẩu thông tin. Khi đọc mã, ta giả lập ngôn ngữ lập trình trong đầu; nếu có quá nhiều thứ diễn ra cùng lúc, ta không theo kịp. Vì mã được đọc nhiều hơn được viết, giới hạn này quan trọng hơn tốc độ gõ. [[src:book-seemann]]',
      'Seemann argues: a computer keeps millions of things in RAM, while human short-term memory holds roughly four to seven pieces of information. Reading code, we emulate the language in our heads; if too much is going on at once, we cannot keep up. Since code is read more than it is written, this limit matters more than typing speed. [[src:book-seemann]]')
    B(C, S_, 2, 'p', 'Ông chọn 7 làm con số tượng trưng và nói rõ con số chính xác không quan trọng: đôi khi ta theo được chín thứ, và "bảy cộng trừ hai" quen thuộc cũng chỉ là một cách nói. Điều quan trọng là giới hạn đó nhỏ hơn bộ nhớ máy tính nhiều bậc. Quy tắc ông đề xuất: không quá bảy thứ diễn ra trong một đoạn mã. [[src:book-seemann]]',
      'He picks 7 as a symbolic number and says plainly that the exact figure does not matter: sometimes we can track nine things, and the familiar "seven plus or minus two" is just a way of putting it. What matters is that the limit is orders of magnitude below a computer\'s memory. The rule he proposes: no more than seven things going on in a single piece of code. [[src:book-seemann]]')
    B(C, S_, 3, 'note', 'Nghiên cứu về trí nhớ ngắn hạn đo việc nhớ các mẩu thông tin rời, không đo việc đọc mã. Nối nó với mã là lập luận của Seemann, không phải kết quả đo trên lập trình viên.',
      'Research on short-term memory measures recalling separate pieces of information, not reading code. Linking it to code is Seemann\'s argument, not a measurement on programmers.')
    B(C, S_, 3, 'kind', 'source')

    S_ = 'count'
    a(C + '.sec.%s.title' % S_, 'Ba cách đếm: đường đi, biến, dòng', 'Three counts: paths, variables, lines')
    a(C + '.sec.%s.badge' % S_, 'simplified')
    B(C, S_, 1, 'p', 'Cyclomatic complexity đếm số đường đi qua một đoạn mã. Cách tính tay của Seemann: bắt đầu từ 1 (mã thẳng một mạch vẫn có một đường), rồi cộng 1 cho mỗi lệnh rẽ nhánh hay lặp. Từ khóa cần đếm tùy ngôn ngữ. Con số này cũng là số test tối thiểu để đi qua mọi đường của hàm. [[src:book-seemann]]',
      'Cyclomatic complexity counts the paths through a piece of code. Seemann\'s hand method: start at 1 (straight-line code still has one path), then add 1 for each branching or looping instruction. Which keywords to count depends on the language. The number is also the minimum number of tests to cover every path. [[src:book-seemann]]')
    B(C, S_, 2, 'p', 'Quy ước của site cho Kotlin: đếm if (kể cả if dùng như biểu thức), for, while, do-while và mỗi nhánh của when trừ else. Các toán tử ?:, &&, || cũng rẽ nhánh; công cụ đo khác nhau ở chỗ có đếm chúng hay không, nên ví dụ trong chương chỉ dùng if và for. Đếm hàm dài trong mô phỏng: 1 + 7 if + 1 for = 9.',
      'The site\'s convention for Kotlin: count if (including if used as an expression), for, while, do-while and each when branch except else. The operators ?:, && and || also branch; tools differ on whether they count them, so this chapter\'s examples use only if and for. Counting the long function in the simulation: 1 + 7 ifs + 1 for = 9.')
    B(C, S_, 3, 'p', 'Đếm biến (Seemann): đếm mọi thứ hàm phải theo dõi, gồm biến cục bộ, tham số và field của lớp. Ông dùng nó chủ yếu khi phân vân có nên thêm một tham số: bốn tham số nghe thì ít, nhưng nếu chúng tương tác với năm biến cục bộ và ba field thì đã quá nhiều. Cách gỡ khi đó là gom tham số thành một object. [[src:book-seemann]]',
      'Counting variables (Seemann): count everything the function has to track, including local variables, parameters and class fields. He uses it mainly when deciding whether to add a parameter: four parameters sounds few, but if they interact with five locals and three fields, that is too much. The way out is to group parameters into an object. [[src:book-seemann]]')
    B(C, S_, 4, 'p', 'Đếm dòng (luật 80/24 của Seemann): một hàm không nên vượt khung 80 ký tự × 24 dòng, kích thước màn hình VT100. Ông nói thẳng con số này tùy ý; điều cần là có một ngưỡng. Martin (Clean Code) nghiêng về nhỏ hơn nữa: hàm hiếm khi nên tới 20 dòng, và ông thừa nhận không có nghiên cứu nào chứng minh điều đó, chỉ có kinh nghiệm. Mô phỏng cho thấy vì sao cần nhiều cách đếm: hàm 19 dòng vẫn có 9 đường đi và 13 biến. [[src:book-seemann]] [[src:book-cleancode]]',
      'Counting lines (Seemann\'s 80/24 rule): a function should not exceed an 80-character × 24-line box, the size of a VT100 screen. He says outright the number is arbitrary; what matters is having a threshold. Martin (Clean Code) leans even smaller: functions should hardly ever reach 20 lines, and he admits no research shows this, only experience. The simulation shows why you need more than one count: a 19-line function still has 9 paths and 13 variables. [[src:book-seemann]] [[src:book-cleancode]]')

    S_ = 'decompose'
    a(C + '.sec.%s.title' % S_, 'Tách hàm: một việc, một mức trừu tượng', 'Splitting: one thing, one level of abstraction')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'p', 'Martin (Clean Code) đưa ra ba chỉ dẫn. Hàm nên làm một việc. Để biết hàm có làm một việc không, xem mọi câu lệnh có ở cùng một mức trừu tượng không: trộn "tính phí" với chi tiết như "chia 100 rồi nhân 70" làm người đọc không phân biệt được đâu là ý chính, đâu là chi tiết. Và mã nên đọc từ trên xuống, mỗi hàm theo sau bởi các hàm ở mức thấp hơn một bậc (stepdown rule). [[src:book-cleancode]]',
      'Martin (Clean Code) gives three guidelines. A function should do one thing. To tell whether it does, check that all its statements sit at the same level of abstraction: mixing "compute the fee" with details like "times 70 divided by 100" leaves readers unable to tell the essential idea from a detail. And code should read top-down, each function followed by those one level below (the stepdown rule). [[src:book-cleancode]]')
    B(C, S_, 2, 'kt', 'fun bookAppointment(req: BookingRequest): Result {   // mức cao: các bước\n    val doctor = validate(req)\n    if (doctor == null) return Result.Invalid("input")\n    val fee = feeFor(doctor, req)\n    val booking = Booking(req.patientId, doctor.id, req.slot, fee)\n    repo.save(booking)\n    reminders.scheduleFor(booking, req.prefersEarly)\n    return Result.Ok(booking)\n}\n// ngay dưới: validate, rồi feeFor (mức thấp hơn một bậc)',
      'fun bookAppointment(req: BookingRequest): Result {   // high level: the steps\n    val doctor = validate(req)\n    if (doctor == null) return Result.Invalid("input")\n    val fee = feeFor(doctor, req)\n    val booking = Booking(req.patientId, doctor.id, req.slot, fee)\n    repo.save(booking)\n    reminders.scheduleFor(booking, req.prefersEarly)\n    return Result.Ok(booking)\n}\n// just below: validate, then feeFor (one level down)')
    B(C, S_, 3, 'p', 'Tách hàm không làm tổng độ phức tạp giảm: vòng lặp voucher vẫn còn, chỉ là nằm trong vouchers.totalFor. Cái được là mỗi lần đọc chỉ cần giữ một hàm. Seemann gọi đây là kiến trúc dạng fractal: mỗi tầng có không quá bảy mẩu, và mỗi mẩu khi mở ra lại có không quá bảy mẩu. [[src:book-seemann]]',
      'Splitting does not lower the total complexity: the voucher loop is still there, just inside vouchers.totalFor. The gain is that each read only needs one function in your head. Seemann calls this a fractal architecture: each level has no more than seven chunks, and each chunk, when opened, again has no more than seven. [[src:book-seemann]]')

    S_ = 'limits'
    a(C + '.sec.%s.title' % S_, 'Khi nào không nên làm theo', 'When not to follow it')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'p', 'Seemann cảnh báo chính ngưỡng của mình. Có lúc vượt ngưỡng là cách xử lý tốt nhất; khi đó hãy đưa đoạn mã về lại dưới ngưỡng sau, vì một khi đã vượt, sẽ không còn cảnh báo nào nữa. Ông cũng nhắc tới luật hậu quả ngoài ý muốn và khuyên cẩn thận khi đặt luật cứng; theo ông, ngưỡng có ích vì làm cả nhóm chú ý tới chất lượng, và khi thói quen đã đổi thì chính luật trở nên thừa. [[src:book-seemann]]',
      'Seemann warns about his own threshold. Sometimes exceeding it is the best response; then bring the code back under it later, because once it is exceeded you get no further warnings. He also mentions the law of unintended consequences and advises care with hard rules; in his view a threshold helps because it makes the team pay attention to quality, and once the mindset has changed the rule itself becomes redundant. [[src:book-seemann]]')
    B(C, S_, 2, 'p', 'Tách quá vụn cũng có giá: đọc một luồng nghiệp vụ mà phải nhảy qua mười hàm một dòng thì thứ phải giữ trong đầu là chuỗi các bước nhảy. Một when liệt kê nhiều trường hợp ngang hàng (ví dụ ánh xạ mã lỗi sang chuỗi) có độ phức tạp cao nhưng vẫn dễ đọc, vì mỗi nhánh độc lập với nhau. Đếm là để gợi ý chỗ cần xem lại, không thay cho phán đoán.',
      'Splitting too finely has a cost too: following one business flow by jumping through ten one-line functions means the chain of jumps is what you hold in your head. A when listing many parallel cases (say, mapping error codes to strings) has high complexity yet stays easy to read, because each branch is independent. Counting suggests where to look again; it does not replace judgement.')

    S_ = 'bugs'
    a(C + '.sec.%s.title' % S_, 'Hai lỗi hay gặp', 'Two common bugs')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'bug', 'Sau một thay đổi nhỏ ở phần phí, lịch hẹn miễn phí không còn được nhắc.', 'After a small change to the fee part, free bookings no longer get reminders.')
    B(C, S_, 1, 'cause', 'Nhánh mới có return sớm nằm giữa một hàm 9 đường đi, 13 biến. Phần hẹn nhắc ở cuối hàm nằm ngoài những gì người sửa và người review giữ trong đầu.', 'The new branch with an early return sits in the middle of a function with 9 paths and 13 variables. The reminder at the end was outside what the editor and reviewer held in their heads.')
    B(C, S_, 1, 'fix', 'Tách phần phí ra feeFor, để bookAppointment chỉ còn các bước ở mức cao. Yêu cầu về phí sửa trong feeFor và không thể chặn các bước sau; thêm một test "lịch hẹn miễn phí vẫn được nhắc".', 'Move the fee into feeFor, leaving bookAppointment with only high-level steps. Fee requirements are edited inside feeFor and cannot block later steps; add a test "a free booking still gets a reminder".')
    B(C, S_, 2, 'bug', 'Thêm một tham số cho hàm tạo lịch hẹn, và lỗi truyền nhầm thứ tự giữa hai tham số cùng kiểu.', 'Adding a parameter to the booking function, and a bug from passing two same-typed arguments in the wrong order.')
    B(C, S_, 2, 'cause', 'Hàm đã có bốn tham số, năm biến cục bộ và ba field. Thêm tham số thứ năm, người gọi phải nhớ quá nhiều vị trí; hai tham số String cạnh nhau bị đảo mà trình biên dịch không báo.', 'The function already had four parameters, five locals and three fields. With a fifth parameter, callers must remember too many positions; two adjacent String parameters were swapped and the compiler said nothing.')
    B(C, S_, 2, 'fix', 'Gom các tham số đi cùng nhau thành một object (ở đây là BookingRequest), như Seemann gợi ý khi đếm biến thấy quá nhiều. Với Kotlin, gọi bằng tham số có tên cũng giúp đọc và tránh đảo thứ tự.', 'Group the parameters that travel together into an object (here, BookingRequest), as Seemann suggests when the variable count is too high. In Kotlin, calling with named arguments also helps reading and prevents swaps.')

    S_ = 'ex'
    a(C + '.sec.%s.title' % S_, 'Bài tập', 'Exercise')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'ex', 'Đếm đường đi và biến của hàm cancel dưới đây theo quy ước của chương, rồi tách nó sao cho mỗi hàm không quá 7 ở cả hai cách đếm.', 'Count the paths and variables of the cancel function below using this chapter\'s convention, then split it so every function stays at or under 7 on both counts.')
    B(C, S_, 1, 'exkt', 'fun cancel(id: String, now: Instant): Result {\n    val b = repo.find(id)\n    if (b == null) return Result.NotFound\n    if (b.status == CANCELLED) return Result.Ok(b)\n    var refund = b.fee\n    if (Duration.between(now, b.slot).toHours() < 24) refund /= 2\n    if (b.paidByInsurance) refund = 0\n    for (r in reminders.forBooking(id)) {\n        if (!r.sent) reminders.cancel(r.id)\n    }\n    repo.save(b.copy(status = CANCELLED))\n    if (refund > 0) payments.refund(b.paymentId, refund)\n    return Result.Ok(b)\n}')
    B(C, S_, 1, 'hint', 'Đếm if và for; đếm tham số (id, now), field (repo, reminders, payments) và biến cục bộ. Tìm những đoạn ở mức trừu tượng thấp hơn phần còn lại.', 'Count the ifs and the for; count parameters (id, now), fields (repo, reminders, payments) and locals. Look for parts at a lower level of abstraction than the rest.')
    B(C, S_, 1, 'sol', 'Đường đi: 1 + 6 if + 1 for = 8. Biến: id, now, repo, reminders, payments, b, refund, r = 8. Cả hai đều vượt 7. Tách tiền hoàn ra refundFor (2 if: 3 đường, 2 biến) và việc hủy nhắc ra cancelReminders (1 for, 1 if: 3 đường, 3 biến). cancel còn 3 if: 4 đường, 6 biến, và đọc từ trên xuống thành các bước: tìm, kiểm tra, hủy nhắc, lưu, hoàn tiền.',
      'Paths: 1 + 6 ifs + 1 for = 8. Variables: id, now, repo, reminders, payments, b, refund, r = 8. Both exceed 7. Move the refund into refundFor (2 ifs: 3 paths, 2 variables) and reminder cancelling into cancelReminders (1 for, 1 if: 3 paths, 3 variables). cancel keeps 3 ifs: 4 paths, 6 variables, and reads top-down as steps: find, check, cancel reminders, save, refund.')
    B(C, S_, 1, 'solkt', 'fun cancel(id: String, now: Instant): Result {\n    val b = repo.find(id)\n    if (b == null) return Result.NotFound\n    if (b.status == CANCELLED) return Result.Ok(b)\n    cancelReminders(id)\n    repo.save(b.copy(status = CANCELLED))\n    val refund = refundFor(b, now)\n    if (refund > 0) payments.refund(b.paymentId, refund)\n    return Result.Ok(b)\n}\n\nprivate fun refundFor(b: Booking, now: Instant): Int {\n    if (b.paidByInsurance) return 0\n    if (Duration.between(now, b.slot).toHours() < 24) return b.fee / 2\n    return b.fee\n}\n\nprivate fun cancelReminders(id: String) {\n    for (r in reminders.forBooking(id)) {\n        if (!r.sent) reminders.cancel(r.id)\n    }\n}')

    S_ = 'honest'
    a(C + '.sec.%s.title' % S_, 'Chương này giản lược những gì', 'What this chapter simplifies')
    a(C + '.sec.%s.badge' % S_, 'simplified')
    B(C, S_, 1, 'p', 'Lập luận về trí nhớ ngắn hạn, con số 7, cyclomatic complexity, đếm biến và luật 80/24 theo Mark Seemann, Code That Fits in Your Head và phụ lục A; hàm nhỏ, làm một việc, một mức trừu tượng và stepdown rule theo Robert C. Martin, Clean Code. Đọc ngày 2026-11-24, diễn đạt lại, ví dụ Java và C# của sách được viết lại bằng Kotlin trên app Hẹn Khám. Mọi ngưỡng là heuristic của tác giả. Quy ước đếm cho Kotlin, hàm 19 dòng và mọi con số trong mô phỏng là của site.',
      'The argument about short-term memory, the number 7, cyclomatic complexity, counting variables and the 80/24 rule follow Mark Seemann, Code That Fits in Your Head and appendix A; small functions, doing one thing, one level of abstraction and the stepdown rule follow Robert C. Martin, Clean Code. Read on 2026-11-24 and paraphrased; the books\' Java and C# examples are rewritten in Kotlin on the ClinicBook app. Every threshold is the author\'s heuristic. The Kotlin counting convention, the 19-line function and every number in the simulation are the site\'s.')

    for q, qv, qe, av, ae, wv, we in [
        ('q1', 'Một hàm có 3 lệnh if và 1 vòng for. Cyclomatic complexity theo cách đếm của Seemann là bao nhiêu?', 'A function has 3 ifs and 1 for loop. What is its cyclomatic complexity, counting Seemann\'s way?', '5.', '5.', 'Bắt đầu từ 1, cộng 1 cho mỗi if và for: 1 + 3 + 1.', 'Start at 1, add 1 for each if and for: 1 + 3 + 1.'),
        ('q2', 'Hàm 19 dòng, dưới ngưỡng 24 dòng. Vậy nó vừa trong đầu?', 'A 19-line function is under the 24-line threshold. Does it fit in your head?', 'Chưa chắc: còn phải đếm đường đi và biến.', 'Not necessarily: you still need to count paths and variables.', 'Hàm trong mô phỏng có 19 dòng nhưng 9 đường đi và 13 biến.', 'The function in the simulation has 19 lines but 9 paths and 13 variables.'),
        ('q3', 'Seemann đếm những gì khi "đếm biến"?', 'What does Seemann count when "counting variables"?', 'Biến cục bộ, tham số và field của lớp.', 'Local variables, parameters and class fields.', 'Mọi thứ hàm phải theo dõi, không chỉ biến khai báo trong hàm.', 'Everything the function has to track, not just variables declared inside it.'),
        ('q4', 'Tách hàm dài thành ba hàm nhỏ có làm tổng độ phức tạp giảm không?', 'Does splitting a long function into three small ones lower the total complexity?', 'Không; nó chia độ phức tạp ra để mỗi lần chỉ cần giữ một phần.', 'No; it spreads the complexity so you hold only one part at a time.', 'Vòng lặp voucher vẫn còn, chỉ là nằm trong vouchers.totalFor.', 'The voucher loop is still there, inside vouchers.totalFor.')]:
        a(C + '.quiz.%s.q' % q, qv, qe); a(C + '.quiz.%s.a' % q, av, ae); a(C + '.quiz.%s.why' % q, wv, we)
