# Lập trình hàm · K3 (p3): ghép hàm: composition, currying, partial application (Phần 1: nền tảng)
# Nguồn: Massimo Carli, FP in Kotlin by Tutorials ch.8 (compose, after, curry, pipe, partial application, Designing for partial application,
# side effects break composition: map(f).map(g) và map(f compose g)); Vermeulen, Bjarnason, Chiusano, FP in Kotlin ch.2 (partial1, curry,
# compose, Exercise 2.3–2.5). Đọc 2026-11-24, diễn đạt lại; ví dụ viết lại theo app Hẹn Khám.

SEC_ORDER = {'p3': ['hook', 'compose', 'curry', 'partial', 'kotlin', 'bugs', 'ex', 'honest']}


def add(a):
    def B(ch, sec, n, field, vi, en=None):
        a('%s.sec.%s.b.%02d.%s' % (ch, sec, n, field), vi, vi if en is None else en)

    a('preset.compose', 'Lập trình hàm · ghép hàm và partial application', 'Functional programming · composition and partial application')
    m = lambda k, vi, en=None: a('m.compose.' + k, vi, en)
    m('title', 'Gọi lồng nhau với 6 tham số, hay ghép hàm và cố định trước', 'Nested calls with 6 arguments, or composing and fixing up front')
    m('overview', 'App Hẹn Khám hiện một lịch hẹn ở bốn màn hình: danh sách, chi tiết, tin nhắc, biên lai. Dữ liệu đi qua bốn hàm: parse (chuỗi thô thành yêu cầu), assign (gán bác sĩ và giờ), price (tính phí), format (thành chuỗi hiển thị, cần ngôn ngữ, tiền tệ, múi giờ). Cách thứ nhất: gọi lồng nhau và truyền đủ 6 tham số ở mỗi chỗ. Cách thứ hai: ghép bằng compose và cố định ba tham số chung bằng partial application.',
      'The ClinicBook app shows a booking on four screens: list, detail, reminder, receipt. The data passes through four functions: parse (raw string to request), assign (doctor and time), price (the fee), format (display text, needing locale, currency, time zone). First version: nested calls passing all 6 arguments at every site. Second: compose the functions and fix the three shared arguments with partial application.')
    m('wrapup', 'Lời gọi lồng nhau đọc ngược thứ tự chạy; bốn chỗ gọi mang 24 đối số, 12 là cấu hình lặp lại; một chỗ chép nhầm UTC nên tin nhắc hiện 02:00 thay vì 09:00; thêm một tham số cấu hình phải sửa 4 chỗ. Ghép bằng compose đọc đúng thứ tự chạy; cố định cấu hình một lần thì còn 8 đối số, không lặp, không màn nào sai giờ, và thêm tham số chỉ sửa 1 chỗ. Ở mọi màn truyền đúng múi giờ, hai cách cho cùng một chuỗi.',
      'Nested calls read against the run order; the four call sites carry 24 arguments, 12 of them repeated settings; one site copied UTC by mistake, so the reminder shows 02:00 instead of 09:00; a new settings parameter means editing 4 places. Composing reads in run order; fixing the settings once leaves 8 arguments, none repeated, no screen with the wrong time, and a new parameter touches 1 place. Wherever the right zone is passed, both versions produce the same text.')
    m('simp.1', 'Chỉ có hai múi giờ (giờ phòng khám UTC+7 và UTC) và định dạng ngày rút gọn; lịch hẹn, bác sĩ, phí là của site. compose trong mô phỏng viết bằng JS, cùng ý với compose của Carli.',
      'There are only two time zones (clinic time UTC+7 and UTC) and a short date format; the booking, doctor and fee are the site\'s. The simulation\'s compose is written in JS, with the same meaning as Carli\'s compose.')
    m('simp.2', 'formatFor là một cách của site; một class giữ cấu hình trong constructor cũng đạt cùng mục đích. Carli nhận xét partial application và dependency injection rất gần nhau.',
      'formatFor is one way of the site\'s; a class holding the settings in its constructor reaches the same goal. Carli notes that partial application and dependency injection are very close.')
    m('ctl.hint', 'Đổi cách viết rồi đi lại; xem cột thứ tự đọc, số đối số, và chuỗi hiện ở tin nhắc.', 'Switch the version and walk again; watch the reading-order column, the argument count and the text in the reminder.')
    m('ctl.case', 'Cách viết', 'Version')
    m('ctl.case.nested', 'gọi lồng nhau, 6 tham số mỗi chỗ', 'nested calls, 6 arguments each'); m('ctl.case.composed', 'compose và partial application', 'compose and partial application')
    m('diagramTitle', 'Đầu vào, chuỗi hàm, cấu hình, bốn màn hình', 'Input, function chain, settings, four screens')
    m('diagramDesc', 'Dữ liệu đi qua chuỗi hàm; cấu hình đi tới từng màn hình', 'Data flows through the chain; settings flow to each screen')
    for k, vi, en in [('raw', 'Chuỗi thô', 'Raw string'), ('pipe', 'Chuỗi hàm parse, assign, price', 'The parse, assign, price chain'), ('screens', 'Bốn màn hình', 'Four screens'), ('config', 'Cấu hình phòng khám', 'Clinic settings')]:
        m('n.' + k, vi, en)
    m('met.args', 'Đối số ở 4 chỗ gọi', 'Arguments at the 4 call sites'); m('met.repeated', 'Đối số cấu hình lặp lại', 'Repeated settings arguments')
    m('met.wrong', 'Màn hiện sai giờ', 'Screens showing the wrong time'); m('met.edits', 'Chỗ phải sửa khi thêm tham số', 'Places to edit for a new parameter')
    a('cap.compose', 'Chuỗi thô đi qua các hàm ghép tới bốn màn hình; cấu hình phòng khám cũng đi tới từng màn. Nút đỏ: nơi cấu hình bị lặp hay bị truyền sai.',
      'The raw string flows through the composed functions to four screens; the clinic settings flow to each screen too. A red node: where settings are repeated or passed wrong.')
    S = [
        ('nested', 's1', 'Đọc từ trong ra ngoài', 'Reading from the inside out',
         'b = assign(parse(raw)), rồi price(b) nằm trong lời gọi formatAppointment. Máy chạy parse, assign, price, format; mắt đọc từ trái sang thì gặp format trước, parse sau cùng. Cột "thứ tự đọc" lệch hẳn với thứ tự chạy.',
         'b = assign(parse(raw)), then price(b) sits inside the formatAppointment call. The machine runs parse, assign, price, format; the eye reading left to right meets format first and parse last. The reading-order column is the exact reverse of the run order.'),
        ('nested', 's2', 'Bốn chỗ gọi, sáu đối số mỗi chỗ', 'Four call sites, six arguments each',
         'Danh sách, chi tiết, tin nhắc, biên lai đều gọi formatAppointment: 24 đối số, trong đó 12 là ba tham số cấu hình (ngôn ngữ, tiền tệ, múi giờ) lặp lại y nguyên.',
         'List, detail, reminder and receipt all call formatAppointment: 24 arguments, 12 of which are the three settings (locale, currency, time zone) repeated verbatim.'),
        ('nested', 's3', 'Tin nhắc hiện 02:00', 'The reminder shows 02:00',
         'Chỗ gọi của tin nhắc được chép từ một test dùng ZoneOffset.UTC. Ba màn kia hiện 09:00, tin nhắc hiện 02:00. Khi review không ai thấy, vì dòng đó trông giống hệt ba dòng kia.',
         'The reminder\'s call was copied from a test that used ZoneOffset.UTC. The other three screens show 09:00, the reminder 02:00. Nobody noticed in review, because the line looks just like the other three.'),
        ('nested', 's4', 'Thêm tham số "đồng hồ 24 giờ": sửa 4 chỗ', 'Adding a "24-hour clock" parameter: 4 places to edit',
         'Một tham số cấu hình mới phải thêm vào chữ ký và vào cả bốn chỗ gọi; mỗi chỗ là một cơ hội truyền nhầm như múi giờ.',
         'A new settings parameter goes into the signature and into all four call sites; each site is another chance to pass it wrong, like the time zone.'),
        ('composed', 's1', 'Ghép theo thứ tự chạy', 'Composing in run order',
         '::parse compose ::assign compose ::price đọc từ trái sang đúng như máy chạy. Kiểu nối tiếp nhau: String → Request → Booking → Priced; ghép chỉ biên dịch được khi đầu ra của hàm trước khớp đầu vào của hàm sau.',
         '::parse compose ::assign compose ::price reads left to right exactly as it runs. The types chain: String → Request → Booking → Priced; composing only compiles when each output matches the next input.'),
        ('composed', 's2', 'Cố định ba tham số chung một lần', 'Fixing the three shared arguments once',
         'formatFor(VI, VND, CLINIC_ZONE) trả về một hàm show chỉ cần hai đối số. Đó là partial application: ba giá trị nằm trong closure của hàm trả về. Bốn chỗ gọi còn 8 đối số, không cái nào lặp.',
         'formatFor(VI, VND, CLINIC_ZONE) returns a show function needing only two arguments. That is partial application: the three values live in the returned function\'s closure. The four call sites are down to 8 arguments, none repeated.'),
        ('composed', 's3', 'Bốn màn hình, một múi giờ', 'Four screens, one time zone',
         'Múi giờ chỉ được viết một lần, khi dựng show. Cả bốn màn hiện 09:00; không còn chỗ nào để chép nhầm UTC.',
         'The time zone is written once, when show is built. All four screens show 09:00; there is no place left to copy UTC by mistake.'),
        ('composed', 's4', 'Thêm "đồng hồ 24 giờ": sửa 1 chỗ', 'Adding a "24-hour clock": 1 place to edit',
         'Tham số mới thêm vào formatFor và vào dòng dựng show. Bốn chỗ gọi không đổi.',
         'The new parameter goes into formatFor and the line that builds show. The four call sites stay as they are.'),
    ]
    for case, k, tv, te, xv, xe in S:
        sid = case + '.' + k
        m('s.%s.title' % sid, tv, te); m('s.%s.explain' % sid, xv, xe); m('ev.' + sid, tv, te)
    for k, vi, en in [
        ('try', 'Theo dõi hai bảng: cột "thứ tự đọc" ở bảng trên; đối số và chuỗi hiện ra ở bảng dưới.', 'Watch the two tables: the reading-order column above; the arguments and the shown text below.'),
        ('nested.s2', 'Carli (ch.8): hàm có quá nhiều tham số nói chung là thói quen xấu; khi thiết kế, đặt tham số ít đổi lên trước, hay đổi ra sau, để dễ cố định từng phần. [[src:book-fp-tut]]',
         'Carli (ch.8): functions with too many parameters are generally bad practice; when designing, put the parameters less likely to change first and the more likely last, so they are easy to fix piece by piece. [[src:book-fp-tut]]'),
        ('nested.s3', 'Khi cùng một bộ giá trị phải chép ở nhiều chỗ gọi, mỗi chỗ là một cơ hội sai, và dòng sai trông giống hệt dòng đúng. Gom chúng về một chỗ (bước 2 của cách ghép).',
         'When the same set of values must be copied to many call sites, each site is a chance to get it wrong, and the wrong line looks just like the right ones. Gather them in one place (step 2 of the composed version).'),
        ('nested.s4', 'Seemann đếm tham số như một phần những thứ phải giữ trong đầu (track Mã sạch, chương J1); sáu tham số cộng thêm biến cục bộ dễ vượt ngưỡng 7. [[src:book-seemann]]',
         'Seemann counts parameters among the things you must hold in your head (Clean Code track, chapter J1); six parameters plus local variables easily pass the threshold of 7. [[src:book-seemann]]'),
        ('composed.s1', 'Carli (ch.8): compose(f, g) trả về hàm a → g(f(a)); after là cùng ý, viết theo chiều ngược lại. Thư viện chuẩn của Kotlin không có hai hàm này; sách tự viết chúng bằng infix fun. [[src:book-fp-tut]]',
         'Carli (ch.8): compose(f, g) returns a → g(f(a)); after is the same idea written the other way round. Kotlin\'s standard library has neither; the book writes them as infix functions. [[src:book-fp-tut]]'),
        ('composed.s2', 'Vermeulen và cộng sự (ch.2): partial1(a, f) trả về { b -> f(a, b) }; hàm bên trong giữ a trong closure. Chỉ có một cách viết thân hàm cho đúng kiểu: chữ ký dẫn đường. [[src:book-fp-manning]]',
         'Vermeulen and co-authors (ch.2): partial1(a, f) returns { b -> f(a, b) }; the inner function keeps a in its closure. There is only one body that fits the types: the signature leads the way. [[src:book-fp-manning]]'),
        ('composed.s3', 'Carli (ch.8) nhận xét partial application gần với dependency injection: cố định trước phụ thuộc chung (database), chỉ truyền phần khác nhau (logger). [[src:book-fp-tut]]',
         'Carli (ch.8) notes that partial application is close to dependency injection: fix the shared dependency up front (the database), pass only what differs (the logger). [[src:book-fp-tut]]'),
        ('composed.s4', 'Carli (ch.8): curry biến hàm (A, B) -> C thành (A) -> (B) -> C, nên mọi hàm nhiều tham số viết được thành chuỗi hàm một tham số; nhưng với nhiều tham số, curry và flip làm mã khó đọc. Một hàm dựng như formatFor thường rõ hơn. [[src:book-fp-tut]]',
         'Carli (ch.8): curry turns (A, B) -> C into (A) -> (B) -> C, so any multi-parameter function can become a chain of one-parameter functions; but with many parameters, curry and flip make code hard to read. A builder like formatFor is usually clearer. [[src:book-fp-tut]]'),
    ]:
        m('co.' + k, vi, en)

    z = lambda k, vi, en=None: a('vz.' + k, vi, en)
    z('tab.compose', 'Luồng hàm và chỗ gọi', 'Function flow and call sites')
    z('compose.cap.nested', 'Luồng dữ liệu khi viết lồng nhau: máy chạy theo cột "Chạy", mắt đọc theo cột "Đọc". Ô đỏ: hai thứ tự lệch nhau.', 'The data flow when calls are nested: the machine follows the "Run" column, the eye the "Read" column. Red: the two orders disagree.')
    z('compose.cap.composed', 'Luồng dữ liệu khi ghép bằng compose: thứ tự đọc trùng thứ tự chạy.', 'The data flow when composed: the reading order matches the run order.')
    z('compose.scap', 'Bốn chỗ gọi: {a} đối số, {r} là cấu hình lặp lại.', 'Four call sites: {a} arguments, {r} of them repeated settings.')
    z('compose.legend', 'Ô mờ: đối số cấu hình lặp lại. Đỏ: múi giờ chép nhầm, hay chuỗi khác các màn khác. Viền ở bước 4: chỗ phải sửa khi thêm tham số. "?": chưa tới bước đó.', 'Faded: a repeated settings argument. Red: a wrongly copied time zone, or text that differs from the other screens. Outlined in step 4: what to edit for a new parameter. "?": that step has not come yet.')
    for k, vi, en in [('run', 'Chạy', 'Run'), ('read', 'Đọc', 'Read'), ('fn', 'Hàm', 'Function'), ('type', 'Kiểu vào → ra', 'Type in → out'), ('value', 'Giá trị sau bước', 'Value after the step'),
                      ('site', 'Màn hình', 'Screen'), ('args', 'Đối số', 'Arguments'), ('out', 'Chuỗi hiện ra', 'Shown text')]:
        z('compose.col.' + k, vi, en)
    for k, vi, en in [('list', 'danh sách', 'list'), ('detail', 'chi tiết', 'detail'), ('reminder', 'tin nhắc', 'reminder'), ('receipt', 'biên lai', 'receipt')]:
        z('compose.site.' + k, vi, en)
    z('compose.site.build', 'dựng show (một lần)', 'building show (once)')
    z('compose.build.out', 'một hàm (Priced, Boolean) -> String', 'a (Priced, Boolean) -> String function')
    z('compose.edits.none', 'Bước 4 thêm một tham số cấu hình mới.', 'Step 4 adds a new settings parameter.')
    z('compose.edits.nested', 'Thêm tham số "đồng hồ 24 giờ": sửa chữ ký và {n} chỗ gọi.', 'Adding a "24-hour clock" parameter: edit the signature and {n} call sites.')
    z('compose.edits.composed', 'Thêm tham số "đồng hồ 24 giờ": sửa formatFor và {n} dòng dựng show; các chỗ gọi không đổi.', 'Adding a "24-hour clock" parameter: edit formatFor and {n} line building show; the call sites stay the same.')

    C = 'p3'
    a(C + '.title', 'Ghép hàm: composition, currying, partial application', 'Composing functions: composition, currying, partial application')
    a(C + '.essence', 'Ghép hàm: compose(f, g) là hàm a → g(f(a)). Viết chuỗi bằng compose thì đọc đúng thứ tự chạy; lời gọi lồng nhau phải đọc từ trong ra.\nCurry biến hàm nhiều tham số thành chuỗi hàm một tham số; partial application cố định trước một số tham số và trả về hàm cần phần còn lại.\nKhi cùng bộ cấu hình phải truyền ở nhiều chỗ gọi, cố định nó một lần: chỗ gọi ngắn lại, và không còn chỗ nào truyền nhầm.',
      'Composition: compose(f, g) is the function a → g(f(a)). A chain written with compose reads in run order; nested calls must be read from the inside out.\nCurrying turns a multi-parameter function into a chain of one-parameter functions; partial application fixes some parameters up front and returns a function needing the rest.\nWhen the same settings must be passed at many call sites, fix them once: the calls get shorter, and no site can pass them wrong.')
    a(C + '.goal.g1', 'Đã đếm đối số ở bốn chỗ gọi', 'Counted the arguments at the four call sites')
    a(C + '.goal.g2', 'Đã thấy thêm tham số phải sửa mấy chỗ', 'Saw how many places a new parameter touches')
    a(C + '.sim.fp.compose', 'gọi lồng nhau hay ghép hàm', 'nested calls or composed functions')

    S_ = 'hook'
    a(C + '.sec.%s.title' % S_, 'Đoán trước khi đọc', 'Predict before reading')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'predict', 'Hàm formatAppointment có 6 tham số và được gọi ở 4 màn hình; ba tham số đầu (ngôn ngữ, tiền tệ, múi giờ) giống nhau ở mọi chỗ. Một ngày, tin nhắc lịch hiện giờ lệch 7 tiếng so với màn chi tiết. Bạn tìm ở đâu trước?',
      'formatAppointment has 6 parameters and is called on 4 screens; the first three (locale, currency, time zone) are the same everywhere. One day the reminder shows a time 7 hours off from the detail screen. Where do you look first?')
    B(C, S_, 1, 'ans', 'Ở các chỗ gọi: một trong bốn chỗ truyền múi giờ khác (ở đây là UTC chép từ test). Khi cùng một bộ giá trị phải chép ở nhiều nơi, lỗi nằm ở chỗ chép. Cách chặn: cố định bộ giá trị đó một lần.',
      'At the call sites: one of the four passes another time zone (here UTC, copied from a test). When the same values must be copied to many places, the bug lives in the copying. The cure: fix those values once.')

    S_ = 'compose'
    a(C + '.sec.%s.title' % S_, 'Ghép hàm', 'Function composition')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'p', 'Carli (ch.8) viết hai hàm ghép: f compose g là hàm a → g(f(a)), chạy f trước; g after f cùng nghĩa, viết theo chiều toán học. Ví dụ của sách ghép double, square và stringify: hai cách viết cho cùng kết quả vì ghép hàm có tính kết hợp; không cần biết nhóm nào ghép trước. [[src:book-fp-tut]]',
      'Carli (ch.8) writes two composition functions: f compose g is a → g(f(a)), running f first; g after f means the same, written the mathematical way. The book composes double, square and stringify: both forms give the same result because composition is associative; it does not matter which pair is grouped first. [[src:book-fp-tut]]')
    B(C, S_, 2, 'p', 'Ghép chỉ hợp lệ khi đầu ra của hàm trước khớp đầu vào của hàm sau, và trình biên dịch kiểm điều đó. Với hàm thuần, chuỗi ghép là một hàm thuần mới: thay được bằng kết quả, test được từng mắt xích lẫn cả chuỗi (chương K1). [[src:book-fp-tut]]',
      'Composition is only valid when each output matches the next input, and the compiler checks it. With pure functions, the chain is a new pure function: substitutable by its result, testable link by link and as a whole (chapter K1). [[src:book-fp-tut]]')
    B(C, S_, 3, 'kt', 'infix fun <A, B, C> ((A) -> B).compose(g: (B) -> C): (A) -> C = { a -> g(this(a)) }\n\nval toPriced: (String) -> Priced = ::parse compose ::assign compose ::price\n// cùng nghĩa với: { raw -> price(assign(parse(raw))) }',
      'infix fun <A, B, C> ((A) -> B).compose(g: (B) -> C): (A) -> C = { a -> g(this(a)) }\n\nval toPriced: (String) -> Priced = ::parse compose ::assign compose ::price\n// means the same as: { raw -> price(assign(parse(raw))) }')

    S_ = 'curry'
    a(C + '.sec.%s.title' % S_, 'Currying: mọi hàm thành hàm một tham số', 'Currying: every function as one-parameter functions')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'p', 'compose chỉ nối hàm một tham số. Hàm hai tham số thì sao? Carli (ch.8): mọi hàm nhiều tham số viết được thành hàm bậc cao một tham số. sum(a, b) thành sum(a) trả về hàm { b -> a + b }; sum(3) là hàm "cộng 3", gọi với 4 cho 7. Hàm curry làm việc đó cho mọi hàm (A, B) -> C, cho ra (A) -> (B) -> C. Tên gọi theo nhà toán học Haskell Curry. [[src:book-fp-tut]]',
      'compose only chains one-parameter functions. What about two parameters? Carli (ch.8): every multi-parameter function can be written as a one-parameter higher-order function. sum(a, b) becomes sum(a) returning { b -> a + b }; sum(3) is "add 3", and calling it with 4 gives 7. The curry function does this for any (A, B) -> C, producing (A) -> (B) -> C. The name comes from the mathematician Haskell Curry. [[src:book-fp-tut]]')
    B(C, S_, 2, 'p', 'Vermeulen và cộng sự (ch.2) cho viết curry, uncurry và compose như những câu đố kiểu: với chữ ký fun <A, B, C> curry(f: (A, B) -> C): (A) -> (B) -> C, chỉ có một thân hàm biên dịch được. Lập trình hàm trong thực tế có nhiều việc là ghép các khối theo cách duy nhất hợp kiểu. [[src:book-fp-manning]]',
      'Vermeulen and co-authors (ch.2) have you write curry, uncurry and compose as type puzzles: for the signature fun <A, B, C> curry(f: (A, B) -> C): (A) -> (B) -> C, only one body compiles. Much of practical functional programming is fitting blocks together in the only way the types allow. [[src:book-fp-manning]]')

    S_ = 'partial'
    a(C + '.sec.%s.title' % S_, 'Partial application và thứ tự tham số', 'Partial application and parameter order')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'p', 'Partial application: cố định trước một số tham số, nhận về hàm cần phần còn lại. partial1(a, f) của Vermeulen và cộng sự trả về { b -> f(a, b) }: hàm bên trong "đóng" lấy a trong môi trường của nó (closure). [[src:book-fp-manning]]',
      'Partial application: fix some parameters up front and get back a function needing the rest. partial1(a, f) in Vermeulen and co-authors returns { b -> f(a, b) }: the inner function closes over a in its environment (a closure). [[src:book-fp-manning]]')
    B(C, S_, 2, 'p', 'Carli (ch.8) dùng curry để cố định database chung cho nhiều Calculator, chỉ truyền logger khác nhau, và nhận xét đây là dependency injection theo kiểu hàm. Ông khuyên khi thiết kế: tham số ít đổi đặt trước, hay đổi đặt sau; và hàm quá nhiều tham số nói chung là thói quen xấu. [[src:book-fp-tut]]',
      'Carli (ch.8) curries a factory to fix a shared database for several Calculators, passing only the different logger, and notes this is dependency injection done functionally. His design advice: parameters less likely to change go first, more likely ones last; and functions with too many parameters are generally bad practice. [[src:book-fp-tut]]')
    B(C, S_, 3, 'kt', 'fun formatFor(locale: Locale, currency: Currency, zone: ZoneId): (Priced, Boolean) -> String =\n    { p, compact -> formatAppointment(locale, currency, zone, p.booking, p.fee, compact) }\n\nval show = formatFor(VI, VND, CLINIC_ZONE)   // ba tham số ít đổi: một lần\nshow(toPriced(raw), false)                  // chỉ phần khác nhau',
      'fun formatFor(locale: Locale, currency: Currency, zone: ZoneId): (Priced, Boolean) -> String =\n    { p, compact -> formatAppointment(locale, currency, zone, p.booking, p.fee, compact) }\n\nval show = formatFor(VI, VND, CLINIC_ZONE)   // the three rarely-changing ones: once\nshow(toPriced(raw), false)                  // only what differs')

    S_ = 'kotlin'
    a(C + '.sec.%s.title' % S_, 'Trong mã Kotlin hằng ngày', 'In everyday Kotlin code')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'p', 'Kotlin có sẵn những gì cần để ghép: kiểu hàm, lambda, tham chiếu hàm ::parse, hàm infix (track Kotlin, chương K8). Thư viện chuẩn không có compose hay curry; tự viết như trên chỉ mất một dòng. Carli cũng viết pipe (a pipe f là f(a)) để đọc từ trái sang; trong thư viện chuẩn, let đóng vai tương tự: raw.let(::parse).let(::assign).let(::price). [[src:book-fp-tut]]',
      'Kotlin has what composition needs: function types, lambdas, function references like ::parse, infix functions (Kotlin track, chapter K8). The standard library has no compose or curry; writing them as above takes one line. Carli also writes pipe (a pipe f is f(a)) to read left to right; in the standard library, let plays a similar role: raw.let(::parse).let(::assign).let(::price). [[src:book-fp-tut]]')
    B(C, S_, 2, 'note', 'Đừng ghép cho bằng được: một chuỗi dài compose với tham số được curry rồi flip có thể khó đọc hơn lời gọi bình thường, như chính Carli nhận xét. Mục tiêu là mã dễ đọc và khó truyền sai, không phải không còn dấu ngoặc nào.',
      'Do not compose at all costs: a long compose chain with curried and flipped parameters can read worse than an ordinary call, as Carli himself notes. The goal is code that is easy to read and hard to call wrong, not code without parentheses.')
    B(C, S_, 2, 'kind', 'pitfall')

    S_ = 'bugs'
    a(C + '.sec.%s.title' % S_, 'Hai lỗi hay gặp', 'Two common bugs')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'bug', 'Tin nhắc lịch hiện giờ lệch 7 tiếng so với màn chi tiết.', 'The reminder shows a time 7 hours off from the detail screen.')
    B(C, S_, 1, 'cause', 'Một trong bốn chỗ gọi hàm định dạng 6 tham số truyền ZoneOffset.UTC chép từ test; ba tham số cấu hình lặp lại ở mọi chỗ gọi.', 'One of the four calls to the 6-parameter formatter passes ZoneOffset.UTC copied from a test; the three settings are repeated at every call site.')
    B(C, S_, 1, 'fix', 'Cố định cấu hình một lần (partial application, hay một hàm dựng như formatFor) để chỗ gọi chỉ truyền phần khác nhau.', 'Fix the settings once (partial application, or a builder such as formatFor) so call sites pass only what differs.')
    B(C, S_, 2, 'bug', 'Sau khi gộp list.map(f).map(g) thành list.map(f compose g), một test kiểm thứ tự dòng log bị đỏ.', 'After merging list.map(f).map(g) into list.map(f compose g), a test checking the order of log lines turns red.')
    B(C, S_, 2, 'cause', 'Với hàm thuần, hai cách cho cùng kết quả (Carli ch.8). Nhưng f ghi log: cách đầu chạy f cho mọi phần tử rồi mới tới g, cách sau chạy f rồi g cho từng phần tử, nên thứ tự các dòng log đổi.', 'With pure functions both forms give the same result (Carli ch.8). But f logs: the first form runs f on every element before g, the second runs f then g per element, so the log lines change order.')
    B(C, S_, 2, 'fix', 'Giữ các bước được ghép thuần và ghi log ở ngoài chuỗi, như chương K1. Khi đó gộp hay tách map là refactor an toàn.', 'Keep the composed steps pure and log outside the chain, as in chapter K1. Then merging or splitting maps is a safe refactoring.')

    S_ = 'ex'
    a(C + '.sec.%s.title' % S_, 'Bài tập', 'Exercise')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'ex', 'Viết hàm curry cho hàm hai tham số, rồi dùng nó để tạo hàm tính phí cả tuần cho một bác sĩ từ fee(doctor, day). Vì sao nên đặt doctor trước day? (Ý bài tập theo Exercise 2.3 của Vermeulen và cộng sự và mục "Designing for partial application" của Carli.)',
      'Write curry for a two-parameter function, then use it to build a whole-week fee function for one doctor from fee(doctor, day). Why should doctor come before day? (The idea follows Exercise 2.3 of Vermeulen and co-authors and Carli\'s "Designing for partial application".)')
    B(C, S_, 1, 'exkt', 'fun fee(doctor: Doctor, day: DayOfWeek): Long = TODO()\n\nfun <A, B, C> ((A, B) -> C).curry(): (A) -> (B) -> C = TODO()')
    B(C, S_, 1, 'hint', 'Kiểu trả về là một hàm nhận A và trả về một hàm nhận B. Chỉ có một cách lấy được giá trị kiểu C.', 'The return type is a function taking A and returning a function taking B. There is only one way to get a C.')
    B(C, S_, 1, 'sol', 'Chỉ một thân hàm hợp kiểu: { a -> { b -> this(a, b) } }. ::fee.curry()(an) cho một hàm (DayOfWeek) -> Long dùng được cho cả tuần. doctor đứng trước vì ít đổi hơn day; Carli khuyên đặt tham số ít đổi lên trước để cố định được bằng curry hay partial application.',
      'Only one body fits the types: { a -> { b -> this(a, b) } }. ::fee.curry()(an) gives a (DayOfWeek) -> Long usable for the whole week. doctor comes first because it changes less often than day; Carli advises putting rarely-changing parameters first so curry or partial application can fix them.')
    B(C, S_, 1, 'solkt', 'fun <A, B, C> ((A, B) -> C).curry(): (A) -> (B) -> C = { a -> { b -> this(a, b) } }\n\nval feeForAn: (DayOfWeek) -> Long = ::fee.curry()(an)\nval week: List<Long> = DayOfWeek.values().map(feeForAn)')

    S_ = 'honest'
    a(C + '.sec.%s.title' % S_, 'Chương này giản lược những gì', 'What this chapter simplifies')
    a(C + '.sec.%s.badge' % S_, 'simplified')
    B(C, S_, 1, 'p', 'compose, after, curry, pipe, partial application, lời khuyên về thứ tự tham số và việc side effect phá ghép hàm theo Massimo Carli, Functional Programming in Kotlin by Tutorials ch.8; partial1, curry, compose như câu đố kiểu theo Vermeulen, Bjarnason, Chiusano ch.2. Bốn hàm parse, assign, price, format, hàm 6 tham số và lỗi UTC là của site; mô phỏng chỉ có hai múi giờ. formatFor là một cách; một class nhận cấu hình qua constructor cũng làm được cùng việc.',
      'compose, after, curry, pipe, partial application, the advice on parameter order and side effects breaking composition follow Massimo Carli, Functional Programming in Kotlin by Tutorials ch.8; partial1, curry and compose as type puzzles follow Vermeulen, Bjarnason, Chiusano ch.2. The four functions parse, assign, price, format, the 6-parameter function and the UTC bug are the site\'s; the simulation has only two time zones. formatFor is one way; a class taking the settings through its constructor does the same job.')

    for q, qv, qe, av, ae, wv, we in [
        ('q1', 'f compose g, gọi với x, cho ra gì?', 'What does f compose g give when called with x?', 'Bằng g(f(x)).', 'It gives g(f(x)).', 'f chạy trước; g nhận kết quả của f.', 'f runs first; g receives f\'s result.'),
        ('q2', 'curry biến hàm (A, B) -> C thành kiểu gì?', 'What type does curry turn (A, B) -> C into?', '(A) -> (B) -> C, một chuỗi hàm một tham số.', '(A) -> (B) -> C, a chain of one-parameter functions.', 'Một hàm nhận A, trả về hàm nhận B (Carli ch.8).', 'A function taking A that returns a function taking B (Carli ch.8).'),
        ('q3', 'Thiết kế hàm để dễ cố định từng phần: tham số nào nên đặt trước?', 'Designing a function to be fixed piece by piece: which parameters go first?', 'Những tham số ít đổi nhất.', 'The ones least likely to change.', 'Cố định được chúng bằng curry hay partial application mà không cần flip (Carli ch.8).', 'They can then be fixed with curry or partial application without flipping (Carli ch.8).'),
        ('q4', 'assign: (Request) -> Booking và price: (Booking) -> Priced. ::price compose ::assign có biên dịch không?', 'assign: (Request) -> Booking and price: (Booking) -> Priced. Does ::price compose ::assign compile?', 'Không.', 'No.', 'Nó cần đầu ra của price (Priced) khớp đầu vào của assign (Request); thứ tự đúng là ::assign compose ::price.', 'It needs price\'s output (Priced) to match assign\'s input (Request); the right order is ::assign compose ::price.')]:
        a(C + '.quiz.%s.q' % q, qv, qe); a(C + '.quiz.%s.a' % q, av, ae); a(C + '.quiz.%s.why' % q, wv, we)
