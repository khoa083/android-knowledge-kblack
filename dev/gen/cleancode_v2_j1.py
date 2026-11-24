# Mã sạch · J1: mã phải vừa trong đầu (Phần 1: mã đọc được)
# Nguồn: Mark Seemann, Code That Fits in Your Head ch.3 (3.2.1), ch.7 (7.1.1–7.1.3, 7.2.1, 7.2.7), phụ lục A.2, A.7, A.8;
# Robert C. Martin, Clean Code ch.3 (Small!, Do One Thing, One Level of Abstraction, Stepdown Rule). Đọc 2026-11-24, diễn đạt lại.
# Mọi ngưỡng (7, 80/24, 20 dòng) là heuristic của tác giả. Cách đếm cho Kotlin là quy ước của site theo cách của Seemann.

SEC_ORDER = {'j1': ['hook', 'seven', 'count', 'decompose', 'limits', 'bugs', 'ex']}


def add(a):
    def B(ch, sec, n, field, vi, en=None):
        a('%s.sec.%s.b.%02d.%s' % (ch, sec, n, field), vi, vi if en is None else en)

    a('preset.fits', 'Mã sạch · mã vừa trong đầu', 'Clean code · code that fits in your head')
    m = lambda k, vi, en=None: a('m.fits.' + k, vi, en)
    m('title', 'Một hàm dài, hay vài hàm nhỏ đọc từ trên xuống', 'One long function, or a few small ones read top-down')
    m('overview', 'Hàm bookAppointment của app Hẹn Khám kiểm tra đầu vào, tính phí, lưu lịch hẹn và hẹn giờ gửi nhắc. Ta đọc nó từng đoạn và đếm hai thứ: có bao nhiêu đường đi qua mã, và có bao nhiêu biến phải nhớ. Ở bước cuối, một yêu cầu mới về phí được thêm vào: xem nó làm hỏng gì ở mỗi cách viết.',
      'ClinicBook\'s bookAppointment function checks the input, computes the fee, saves the booking and schedules the reminder. We read it part by part and count two things: how many paths run through the code, and how many variables you must remember. In the last step a new fee requirement is added: see what it breaks in each version.')
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
        ('long.s2', 'Quy tắc ngón tay cái của Seemann: đặt một ngưỡng và để mắt tới nó; vượt khoảng 7 thì tách hàm trước khi thêm nhánh mới. Con số chính xác không quan trọng bằng việc có ngưỡng. [[src:book-seemann]]', 'Seemann\'s rule of thumb: agree on a threshold and keep an eye on it; past about 7, split the function before adding a new branch. The exact number matters less than having one. [[src:book-seemann]]'),
        ('long.s3', 'Seemann cũng dùng ngưỡng số dòng (khoảng 24 dòng, cỡ một màn hình máy tính thời xưa), và tự nhận con số này là tùy ý. Hàm này lọt qua ngưỡng dòng nhưng không qua ngưỡng đường đi: một cách đếm là chưa đủ. [[src:book-seemann]]', 'Seemann also uses a line threshold (about 24 lines, the size of an old computer screen), and calls the number arbitrary himself. This function passes the line threshold but not the path threshold: one count is not enough. [[src:book-seemann]]'),
        ('long.s4', 'Một return sớm ở giữa hàm dài bỏ qua mọi thứ phía sau nó. Người sửa không sai vì ẩu: phần phía sau nằm ngoài những gì đầu họ giữ được lúc đó.', 'An early return in the middle of a long function skips everything after it. The editor was not careless: what came after was outside what their head could hold at that moment.'),
        ('split.s1', 'Mọi dòng trong một hàm nên ở cùng một mức chi tiết, và mã nên đọc từ trên xuống như mục lục: hàm tổng quát trước, hàm chi tiết hơn ngay bên dưới. [[src:book-cleancode]]', 'Every line in a function should sit at one level of detail, and code should read top-down like a table of contents: the general function first, the more detailed ones right below. [[src:book-cleancode]]'),
        ('split.s2', 'Khi đếm biến, tính cả biến cục bộ, tham số và field của lớp. validate dùng req, clock và doctors: ba thứ. [[src:book-seemann]]', 'When counting variables, include locals, parameters and class fields. validate uses req, clock and doctors: three things. [[src:book-seemann]]'),
        ('split.s3', 'Số đường đi cũng là số bài test tối thiểu để đi qua mọi lối của hàm. feeFor có 3 đường nên cần ít nhất 3 bài test. [[src:book-seemann]]', 'The path count is also the minimum number of tests needed to walk every way through a function. feeFor has 3 paths, so it needs at least 3 tests. [[src:book-seemann]]'),
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
    a(C + '.essence', 'Khi đọc mã, bạn chạy thử nó trong đầu. Nhưng trí nhớ ngắn hạn chỉ giữ được vài thứ cùng lúc, nên Seemann đề xuất một ngưỡng dễ nhớ: khoảng 7.\nĐể biết một hàm có vừa sức không, đếm hai thứ: số đường đi qua hàm (bắt đầu từ 1, mỗi if hay for cộng thêm 1) và số biến bạn phải theo dõi. Hàm ngắn chưa chắc đã dễ.\nVượt ngưỡng thì tách hàm: mỗi hàm làm một việc, đọc từ trên xuống như mục lục. Tổng độ phức tạp không giảm, nhưng mỗi lần bạn chỉ cần giữ một phần.',
      'When you read code, you run it in your head. But short-term memory holds only a few things at once, so Seemann proposes an easy-to-remember threshold: about 7.\nTo know whether a function is manageable, count two things: the paths through it (start at 1, each if or for adds 1) and the variables you must track. A short function is not necessarily an easy one.\nPast the threshold, split the function: each piece does one job and reads top-down like a table of contents. The total complexity does not shrink, but you only need to hold one part at a time.')
    a(C + '.goal.g1', 'Đã đếm hàm dài vượt ngưỡng', 'Counted the long function past the threshold')
    a(C + '.goal.g2', 'Đã thấy yêu cầu mới làm hỏng gì', 'Saw what the new requirement breaks')
    a(C + '.sim.cleancode.fits', 'một hàm dài hay vài hàm nhỏ', 'one long function or a few small ones')

    S_ = 'hook'
    a(C + '.sec.%s.title' % S_, 'Đoán trước khi đọc', 'Predict before reading')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'predict', 'Hàm bookAppointment dài 120 dòng: kiểm tra đầu vào, tính phí, lưu lịch hẹn, hẹn giờ gửi nhắc. Một đồng nghiệp sửa phần tính phí, test phần phí đều xanh. Tuần sau, phòng khám báo nhiều bệnh nhân không nhận được tin nhắc. Chuyện gì có thể đã xảy ra, và vì sao lúc review (người khác đọc và góp ý trước khi gộp mã) không ai thấy?',
      'The bookAppointment function is 120 lines: input checks, the fee, saving the booking, scheduling the reminder. A colleague edits the fee part and the fee tests are green. The next week the clinic reports that many patients got no reminder. What could have happened, and why did nobody see it in review (others reading and commenting before the code is merged)?')
    B(C, S_, 1, 'ans', 'Rất hay gặp: phần phí được thêm một nhánh rẽ "return sớm", và nhánh đó vô tình bỏ qua phần hẹn nhắc ở cuối hàm. Người sửa và người review chỉ giữ phần phí trong đầu; phần hẹn nhắc nằm ngoài tầm nhìn. Mô phỏng ngay dưới giúp bạn đếm xem hàm đó bắt người đọc nhớ bao nhiêu thứ cùng lúc.',
      'A very common story: the fee part gets an "early return" path, and that branch accidentally skips the reminder at the end. The editor and the reviewer held only the fee part in their heads; the reminder was out of view. The simulation just below lets you count how many things that function makes the reader hold at once.')

    S_ = 'seven'
    a(C + '.sec.%s.title' % S_, 'Trí nhớ ngắn hạn và con số 7', 'Short-term memory and the number 7')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'p', 'Hãy thử nhớ một số điện thoại vừa nghe: 10 chữ số đã khó, nếu không chia thành từng cụm. Đọc mã cũng vậy. Máy tính giữ hàng triệu thứ trong bộ nhớ, còn đầu người chỉ giữ khoảng bốn tới bảy mẩu thông tin cùng lúc. Mà mã được đọc nhiều hơn được viết, nên giới hạn này quan trọng hơn tốc độ gõ phím. [[src:book-seemann]]',
      'Try remembering a phone number you just heard: 10 digits is already hard unless you split it into chunks. Reading code is the same. A computer holds millions of things in memory, while a human head holds roughly four to seven pieces at once. And code is read far more often than it is written, so this limit matters more than typing speed. [[src:book-seemann]]')
    B(C, S_, 2, 'p', 'Seemann chọn 7 làm con số dễ nhớ, và nói rõ con số chính xác không quan trọng: đôi khi ta theo được chín thứ. Điều quan trọng là giới hạn đó rất nhỏ so với máy. Quy tắc ngón tay cái: một đoạn mã không nên bắt người đọc theo dõi quá khoảng bảy thứ cùng lúc. [[src:book-seemann]]',
      'Seemann picks 7 as an easy number to remember, and says plainly the exact figure does not matter: sometimes we can track nine things. What matters is that the limit is tiny compared with a machine. Rule of thumb: a piece of code should not make the reader track more than about seven things at once. [[src:book-seemann]]')
    B(C, S_, 3, 'note', 'Các nghiên cứu về trí nhớ ngắn hạn đo việc nhớ những mẩu thông tin rời, không đo việc đọc mã. Nối hai chuyện với nhau là lập luận của Seemann, không phải kết quả đo trên lập trình viên.',
      'Studies of short-term memory measure recalling separate pieces of information, not reading code. Linking the two is Seemann\'s argument, not a measurement on programmers.')
    B(C, S_, 3, 'kind', 'source')

    S_ = 'count'
    a(C + '.sec.%s.title' % S_, 'Ba cách đếm: đường đi, biến, dòng', 'Three counts: paths, variables, lines')
    a(C + '.sec.%s.badge' % S_, 'simplified')
    B(C, S_, 1, 'p', 'Đếm đường đi (tên chuyên môn là cyclomatic complexity) giống đếm số ngã rẽ trên một con đường. Đường thẳng một mạch thì có 1 lối đi; mỗi if hay for mở thêm một lối. Vậy: bắt đầu từ 1, mỗi lệnh rẽ nhánh hay lặp cộng thêm 1. Con số này cũng cho biết cần ít nhất bao nhiêu bài test để đi qua mọi lối. [[src:book-seemann]]',
      'Counting paths (the technical name is cyclomatic complexity) is like counting the forks on a road. A straight road has 1 way through; each if or for opens another. So: start at 1, add 1 for each branch or loop. The number also tells you the minimum number of tests needed to walk every way. [[src:book-seemann]]')
    B(C, S_, 2, 'p', 'Với Kotlin, chương này đếm if (kể cả if dùng như biểu thức), for, while, do-while và mỗi nhánh của when trừ else. Các toán tử ?:, && và || cũng rẽ nhánh, nhưng mỗi công cụ đếm chúng một kiểu, nên ví dụ ở đây chỉ dùng if và for. Hàm dài trong mô phỏng: 1 + 7 if + 1 for = 9 đường đi.',
      'For Kotlin, this chapter counts if (including if used as an expression), for, while, do-while and each when branch except else. The operators ?:, && and || also branch, but every tool counts them differently, so the examples here use only if and for. The long function in the simulation: 1 + 7 ifs + 1 for = 9 paths.')
    B(C, S_, 3, 'p', 'Đếm biến: đếm mọi thứ hàm bắt bạn theo dõi, gồm biến cục bộ, tham số và các field của lớp mà nó dùng. Cách đếm này có ích nhất khi bạn phân vân có nên thêm một tham số. Bốn tham số nghe thì ít, nhưng nếu chúng đi cùng năm biến cục bộ và ba field thì đã quá nhiều. Khi đó, hãy gom các tham số đi cùng nhau thành một object. [[src:book-seemann]]',
      'Counting variables: count everything the function makes you track, including local variables, parameters and the class fields it uses. This count helps most when you are unsure whether to add a parameter. Four parameters sounds few, but together with five locals and three fields it is already too much. Then group the parameters that travel together into one object. [[src:book-seemann]]')
    B(C, S_, 4, 'p', 'Đếm dòng: Seemann đặt ngưỡng một hàm vừa một khung 80 ký tự × 24 dòng, cỡ màn hình máy tính thời xưa, và nói thẳng con số này tùy ý; điều cần là có một ngưỡng. Martin còn chuộng hàm ngắn hơn nữa, hiếm khi tới 20 dòng, và thừa nhận đó là kinh nghiệm chứ không có nghiên cứu nào chứng minh. Mô phỏng cho thấy vì sao một cách đếm là không đủ: hàm 19 dòng vẫn có 9 đường đi và 13 biến. [[src:book-seemann]] [[src:book-cleancode]]',
      'Counting lines: Seemann sets the threshold of a function fitting in an 80-character × 24-line box, the size of an old computer screen, and says outright the number is arbitrary; what matters is having a threshold. Martin prefers even shorter functions, hardly ever reaching 20 lines, and admits it is experience rather than research. The simulation shows why one count is not enough: a 19-line function still has 9 paths and 13 variables. [[src:book-seemann]] [[src:book-cleancode]]')

    S_ = 'decompose'
    a(C + '.sec.%s.title' % S_, 'Tách hàm: một việc, một mức chi tiết', 'Splitting: one job, one level of detail')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'p', 'Hãy nghĩ tới một cuốn sách hay: mục lục cho bạn thấy các chương; mở chương ra mới thấy chi tiết. Một hàm tốt cũng thế. Nó làm một việc. Mọi dòng trong nó ở cùng một mức chi tiết: đừng để "tính phí" đứng cạnh "nhân 70 rồi chia 100". Và mã đọc từ trên xuống: hàm ở mức cao trước, các hàm chi tiết hơn ngay bên dưới. [[src:book-cleancode]]',
      'Think of a good book: the table of contents shows the chapters; you open a chapter to see the details. A good function is the same. It does one job. Every line in it sits at the same level of detail: do not put "compute the fee" next to "times 70 divided by 100". And the code reads top-down: the high-level function first, the more detailed ones right below. [[src:book-cleancode]]')
    B(C, S_, 2, 'kt', 'fun bookAppointment(req: BookingRequest): Result {   // mức cao: các bước\n    val doctor = validate(req)\n    if (doctor == null) return Result.Invalid("input")\n    val fee = feeFor(doctor, req)\n    val booking = Booking(req.patientId, doctor.id, req.slot, fee)\n    repo.save(booking)\n    reminders.scheduleFor(booking, req.prefersEarly)\n    return Result.Ok(booking)\n}\n// ngay dưới: validate, rồi feeFor (chi tiết hơn một bậc)',
      'fun bookAppointment(req: BookingRequest): Result {   // high level: the steps\n    val doctor = validate(req)\n    if (doctor == null) return Result.Invalid("input")\n    val fee = feeFor(doctor, req)\n    val booking = Booking(req.patientId, doctor.id, req.slot, fee)\n    repo.save(booking)\n    reminders.scheduleFor(booking, req.prefersEarly)\n    return Result.Ok(booking)\n}\n// just below: validate, then feeFor (one level more detailed)')
    B(C, S_, 3, 'p', 'Lưu ý: tách hàm không làm tổng độ phức tạp giảm đi. Vòng lặp voucher vẫn còn, chỉ là nằm trong vouchers.totalFor. Cái được là mỗi lần đọc, bạn chỉ cần giữ một hàm trong đầu. Seemann ví cách tổ chức này như một hình fractal: tầng nào cũng không quá khoảng bảy mẩu, và mở một mẩu ra lại thấy không quá bảy mẩu nhỏ hơn. [[src:book-seemann]]',
      'Note: splitting does not lower the total complexity. The voucher loop is still there, just inside vouchers.totalFor. The gain is that each time you read, you hold only one function in your head. Seemann likens this layout to a fractal: every level has no more than about seven pieces, and opening a piece shows no more than seven smaller ones. [[src:book-seemann]]')

    S_ = 'limits'
    a(C + '.sec.%s.title' % S_, 'Khi nào không nên làm theo', 'When not to follow it')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'p', 'Ngưỡng là đèn báo, không phải luật thép. Có lúc vượt ngưỡng là cách hợp lý nhất; khi đó hãy nhớ đưa đoạn mã về lại dưới ngưỡng sau, vì một khi đã vượt, sẽ không còn gì cảnh báo bạn nữa. Theo Seemann, ngưỡng có ích chủ yếu vì nó làm cả nhóm chú ý tới chất lượng. [[src:book-seemann]]',
      'A threshold is a warning light, not an iron law. Sometimes going past it is the most sensible choice; then remember to bring the code back under it later, because once you are past it nothing warns you any more. According to Seemann, a threshold helps mostly because it makes the whole team pay attention to quality. [[src:book-seemann]]')
    B(C, S_, 2, 'p', 'Tách quá vụn cũng có giá: đọc một luồng nghiệp vụ mà phải nhảy qua mười hàm một dòng thì thứ bạn phải nhớ lại là chuỗi các bước nhảy. Một when liệt kê nhiều trường hợp ngang hàng (ví dụ đổi mã lỗi sang câu thông báo) có nhiều đường đi nhưng vẫn dễ đọc, vì mỗi nhánh độc lập. Đếm là để gợi ý chỗ cần xem lại, không thay cho phán đoán của bạn.',
      'Splitting too finely has a cost too: following one business flow by jumping through ten one-line functions means the chain of jumps is what you must remember instead. A when listing many parallel cases (say, turning error codes into messages) has many paths yet stays easy to read, because each branch is independent. Counting points to places worth a second look; it does not replace your judgement.')

    S_ = 'bugs'
    a(C + '.sec.%s.title' % S_, 'Hai lỗi hay gặp', 'Two common bugs')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'bug', 'Sau một thay đổi nhỏ ở phần phí, lịch hẹn miễn phí không còn được nhắc.', 'After a small change to the fee part, free bookings no longer get reminders.')
    B(C, S_, 1, 'cause', 'Nhánh mới có "return sớm" nằm giữa một hàm 9 đường đi, 13 biến. Phần hẹn nhắc ở cuối hàm nằm ngoài những gì người sửa và người review giữ được trong đầu.', 'The new "early return" branch sits in the middle of a function with 9 paths and 13 variables. The reminder at the end was outside what the editor and reviewer could hold in their heads.')
    B(C, S_, 1, 'fix', 'Tách phần phí ra feeFor, để bookAppointment chỉ còn các bước ở mức cao. Yêu cầu về phí sửa trong feeFor và không thể chặn các bước sau. Thêm một bài test "lịch hẹn miễn phí vẫn được nhắc".', 'Move the fee into feeFor, leaving bookAppointment with only high-level steps. Fee requirements are edited inside feeFor and cannot block later steps. Add a test "a free booking still gets a reminder".')
    B(C, S_, 2, 'bug', 'Thêm một tham số cho hàm tạo lịch hẹn, và hai tham số cùng kiểu bị truyền đảo thứ tự.', 'A parameter is added to the booking function, and two same-typed arguments get passed in the wrong order.')
    B(C, S_, 2, 'cause', 'Hàm đã có bốn tham số, năm biến cục bộ và ba field. Thêm tham số thứ năm, người gọi phải nhớ quá nhiều vị trí; hai tham số String đứng cạnh nhau bị đảo mà trình biên dịch không báo.', 'The function already had four parameters, five locals and three fields. With a fifth parameter, callers must remember too many positions; two adjacent String parameters were swapped and the compiler said nothing.')
    B(C, S_, 2, 'fix', 'Gom các tham số đi cùng nhau thành một object (ở đây là BookingRequest). Trong Kotlin, gọi bằng tên tham số cũng giúp đọc dễ hơn và tránh đảo thứ tự.', 'Group the parameters that travel together into one object (here, BookingRequest). In Kotlin, calling with named arguments also makes reading easier and prevents swaps.')

    S_ = 'ex'
    a(C + '.sec.%s.title' % S_, 'Bài tập', 'Exercise')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'ex', 'Đếm đường đi và biến của hàm cancel dưới đây theo cách đếm của chương, rồi tách nó sao cho hàm nào cũng không quá 7 ở cả hai cách đếm.', 'Count the paths and variables of the cancel function below using this chapter\'s method, then split it so every function stays at or under 7 on both counts.')
    B(C, S_, 1, 'exkt', 'fun cancel(id: String, now: Instant): Result {\n    val b = repo.find(id)\n    if (b == null) return Result.NotFound\n    if (b.status == CANCELLED) return Result.Ok(b)\n    var refund = b.fee\n    if (Duration.between(now, b.slot).toHours() < 24) refund /= 2\n    if (b.paidByInsurance) refund = 0\n    for (r in reminders.forBooking(id)) {\n        if (!r.sent) reminders.cancel(r.id)\n    }\n    repo.save(b.copy(status = CANCELLED))\n    if (refund > 0) payments.refund(b.paymentId, refund)\n    return Result.Ok(b)\n}')
    B(C, S_, 1, 'hint', 'Đếm các if và for; đếm tham số (id, now), field (repo, reminders, payments) và biến cục bộ. Tìm những đoạn chi tiết hơn hẳn phần còn lại.', 'Count the ifs and the for; count parameters (id, now), fields (repo, reminders, payments) and locals. Look for parts that are much more detailed than the rest.')
    B(C, S_, 1, 'sol', 'Đường đi: 1 + 6 if + 1 for = 8. Biến: id, now, repo, reminders, payments, b, refund, r = 8. Cả hai đều vượt 7. Tách tiền hoàn ra refundFor (2 if: 3 đường, 2 biến) và việc hủy nhắc ra cancelReminders (1 for, 1 if: 3 đường, 3 biến). cancel còn 3 if: 4 đường, 6 biến, và đọc từ trên xuống như một danh sách bước: tìm, kiểm tra, hủy nhắc, lưu, hoàn tiền.',
      'Paths: 1 + 6 ifs + 1 for = 8. Variables: id, now, repo, reminders, payments, b, refund, r = 8. Both exceed 7. Move the refund into refundFor (2 ifs: 3 paths, 2 variables) and reminder cancelling into cancelReminders (1 for, 1 if: 3 paths, 3 variables). cancel keeps 3 ifs: 4 paths, 6 variables, and reads top-down like a list of steps: find, check, cancel reminders, save, refund.')
    B(C, S_, 1, 'solkt', 'fun cancel(id: String, now: Instant): Result {\n    val b = repo.find(id)\n    if (b == null) return Result.NotFound\n    if (b.status == CANCELLED) return Result.Ok(b)\n    cancelReminders(id)\n    repo.save(b.copy(status = CANCELLED))\n    val refund = refundFor(b, now)\n    if (refund > 0) payments.refund(b.paymentId, refund)\n    return Result.Ok(b)\n}\n\nprivate fun refundFor(b: Booking, now: Instant): Int {\n    if (b.paidByInsurance) return 0\n    if (Duration.between(now, b.slot).toHours() < 24) return b.fee / 2\n    return b.fee\n}\n\nprivate fun cancelReminders(id: String) {\n    for (r in reminders.forBooking(id)) {\n        if (!r.sent) reminders.cancel(r.id)\n    }\n}')

    for q, qv, qe, av, ae, wv, we in [
        ('q1', 'Một hàm có 3 lệnh if và 1 vòng for. Nó có bao nhiêu đường đi?', 'A function has 3 ifs and 1 for loop. How many paths does it have?', 'Năm.', 'Five.', 'Bắt đầu từ 1, mỗi if và for cộng 1: 1 + 3 + 1.', 'Start at 1, each if and for adds 1: 1 + 3 + 1.'),
        ('q2', 'Hàm 19 dòng, dưới ngưỡng 24 dòng. Vậy nó vừa trong đầu?', 'A 19-line function is under the 24-line threshold. Does it fit in your head?', 'Chưa chắc: còn phải đếm đường đi và biến.', 'Not necessarily: you still need to count paths and variables.', 'Hàm trong mô phỏng chỉ 19 dòng nhưng có 9 đường đi và 13 biến.', 'The function in the simulation is only 19 lines but has 9 paths and 13 variables.'),
        ('q3', 'Khi "đếm biến", ta đếm những gì?', 'When "counting variables", what do we count?', 'Biến cục bộ, tham số và các field của lớp mà hàm dùng.', 'Local variables, parameters and the class fields the function uses.', 'Mọi thứ hàm bắt bạn theo dõi, không chỉ biến khai báo trong hàm.', 'Everything the function makes you track, not just variables declared inside it.'),
        ('q4', 'Tách một hàm dài thành ba hàm nhỏ có làm tổng độ phức tạp giảm không?', 'Does splitting a long function into three small ones lower the total complexity?', 'Không; nó chia độ phức tạp ra để mỗi lần chỉ cần giữ một phần.', 'No; it spreads the complexity so you hold only one part at a time.', 'Vòng lặp voucher vẫn còn, chỉ là nằm trong vouchers.totalFor.', 'The voucher loop is still there, inside vouchers.totalFor.')]:
        a(C + '.quiz.%s.q' % q, qv, qe); a(C + '.quiz.%s.a' % q, av, ae); a(C + '.quiz.%s.why' % q, wv, we)
