# Lập trình hàm · K3 (p3): ghép hàm: composition, currying, partial application (Phần 1: nền tảng)
# Nguồn (chỉ ghi ở đây và docs/research/fp.md): Carli, FP in Kotlin by Tutorials ch.8; Vermeulen, Bjarnason, Chiusano, FP in Kotlin ch.2
# (partial1, curry, compose, Exercise 2.3–2.5); Seemann 7.2.7. Giọng văn dạy học (2026-11-24).

SEC_ORDER = {'p3': ['hook', 'compose', 'curry', 'partial', 'kotlin', 'bugs', 'ex']}


def add(a):
    def B(ch, sec, n, field, vi, en=None):
        a('%s.sec.%s.b.%02d.%s' % (ch, sec, n, field), vi, vi if en is None else en)

    a('preset.compose', 'Lập trình hàm · ghép hàm và partial application', 'Functional programming · composition and partial application')
    m = lambda k, vi, en=None: a('m.compose.' + k, vi, en)
    m('title', 'Gọi lồng nhau với 6 tham số, hay ghép hàm và cố định trước', 'Nested calls with 6 arguments, or composing and fixing up front')
    m('overview', 'App Hẹn Khám hiện một lịch hẹn ở bốn màn hình: danh sách, chi tiết, tin nhắc, biên lai. Dữ liệu đi qua bốn bước: parse (đọc chuỗi thô), assign (gán bác sĩ và giờ), price (tính phí), format (thành chữ để hiện, cần biết ngôn ngữ, tiền tệ, múi giờ). Cách 1: gọi lồng các hàm vào nhau và truyền đủ 6 tham số ở từng màn. Cách 2: nối các hàm thành một chuỗi, và chốt sẵn ba tham số chung một lần.',
      'The ClinicBook app shows a booking on four screens: list, detail, reminder, receipt. The data goes through four steps: parse (read the raw string), assign (doctor and time), price (the fee), format (turn it into display text, needing locale, currency and time zone). Way 1: nest the calls and pass all 6 arguments on every screen. Way 2: chain the functions together, and lock in the three shared arguments once.')
    m('wrapup', 'Gọi lồng nhau buộc ta đọc ngược thứ tự chạy, và bốn màn mang tổng cộng 24 đối số, trong đó 12 là cấu hình lặp lại. Chỉ cần một màn chép nhầm múi giờ UTC là tin nhắc hiện 02:00 thay vì 09:00. Nối hàm thành chuỗi thì đọc đúng thứ tự chạy; chốt cấu hình một lần thì chỉ còn 8 đối số, không lặp, không màn nào sai giờ, và thêm tham số mới chỉ phải sửa một chỗ.',
      'Nesting the calls makes you read against the run order, and the four screens carry 24 arguments in total, 12 of them repeated settings. A single screen copying the UTC time zone by mistake makes the reminder show 02:00 instead of 09:00. Chaining reads in run order; locking in the settings once leaves 8 arguments, none repeated, no screen with the wrong time, and a new parameter means editing one place.')
    m('simp.1', 'Chỉ có hai múi giờ (giờ phòng khám UTC+7 và UTC) và định dạng ngày rút gọn. Lịch hẹn, bác sĩ và phí là ví dụ.',
      'There are only two time zones (clinic time UTC+7 and UTC) and a short date format. The booking, doctor and fee are examples.')
    m('simp.2', 'formatFor chỉ là một cách; một class nhận cấu hình qua constructor cũng làm được cùng việc.',
      'formatFor is just one way; a class taking the settings through its constructor does the same job.')
    m('ctl.hint', 'Chọn cách viết rồi bấm qua từng bước; để ý cột "Đọc", số đối số, và giờ hiện ở tin nhắc.', 'Pick a version and step through; watch the "Read" column, the argument count and the time shown in the reminder.')
    m('ctl.case', 'Cách viết', 'Version')
    m('ctl.case.nested', 'gọi lồng nhau, 6 tham số mỗi chỗ', 'nested calls, 6 arguments each'); m('ctl.case.composed', 'nối hàm và chốt tham số chung', 'chained, shared arguments locked in')
    m('diagramTitle', 'Đầu vào, chuỗi hàm, cấu hình, bốn màn hình', 'Input, function chain, settings, four screens')
    m('diagramDesc', 'Dữ liệu chạy qua chuỗi hàm; cấu hình đi tới từng màn hình', 'Data runs through the chain; settings flow to each screen')
    for k, vi, en in [('raw', 'Chuỗi thô', 'Raw string'), ('pipe', 'Chuỗi hàm parse, assign, price', 'The parse, assign, price chain'), ('screens', 'Bốn màn hình', 'Four screens'), ('config', 'Cấu hình phòng khám', 'Clinic settings')]:
        m('n.' + k, vi, en)
    m('met.args', 'Đối số ở 4 chỗ gọi', 'Arguments at the 4 call sites'); m('met.repeated', 'Đối số cấu hình lặp lại', 'Repeated settings arguments')
    m('met.wrong', 'Màn hiện sai giờ', 'Screens showing the wrong time'); m('met.edits', 'Chỗ phải sửa khi thêm tham số', 'Places to edit for a new parameter')
    a('cap.compose', 'Chuỗi thô chạy qua các hàm đã nối tới bốn màn hình; cấu hình phòng khám cũng đi tới từng màn. Ô đỏ: chỗ cấu hình bị lặp lại hoặc truyền sai.',
      'The raw string runs through the chained functions to four screens; the clinic settings also flow to each screen. A red box: where settings are repeated or passed wrong.')
    S = [
        ('nested', 's1', 'Đọc từ trong ra ngoài', 'Reading from the inside out',
         'Mã viết b = assign(parse(raw)), rồi đặt price(b) bên trong lời gọi formatAppointment. Máy chạy theo thứ tự parse, assign, price, format. Nhưng mắt ta đọc từ trái sang phải nên gặp format trước, parse sau cùng. Cột "Đọc" ngược hẳn cột "Chạy": muốn hiểu, ta phải đọc từ trong ra ngoài.',
         'The code writes b = assign(parse(raw)), then puts price(b) inside the formatAppointment call. The machine runs parse, assign, price, format. But we read left to right, so we meet format first and parse last. The "Read" column is the exact reverse of "Run": to understand it, you must read from the inside out.'),
        ('nested', 's2', 'Bốn màn, sáu đối số mỗi màn', 'Four screens, six arguments each',
         'Danh sách, chi tiết, tin nhắc và biên lai đều gọi formatAppointment với 6 đối số: tổng 24. Trong đó 12 là ba thông số cấu hình (ngôn ngữ, tiền tệ, múi giờ) lặp đi lặp lại y hệt ở mỗi màn.',
         'The list, detail, reminder and receipt all call formatAppointment with 6 arguments: 24 in total. Of these, 12 are the three settings (locale, currency, time zone) repeated exactly on every screen.'),
        ('nested', 's3', 'Tin nhắc hiện 02:00', 'The reminder shows 02:00',
         'Dòng gọi ở màn tin nhắc được chép từ một bài test dùng múi giờ UTC. Ba màn kia hiện 09:00, riêng tin nhắc hiện 02:00. Lúc review không ai phát hiện, vì dòng sai trông giống hệt ba dòng đúng.',
         'The reminder\'s call line was copied from a test that used the UTC time zone. The other three screens show 09:00, but the reminder shows 02:00. Nobody spotted it in review, because the wrong line looks exactly like the three right ones.'),
        ('nested', 's4', 'Thêm tham số "đồng hồ 24 giờ": sửa 4 chỗ', 'Adding a "24-hour clock" parameter: 4 places to edit',
         'Một tham số cấu hình mới phải thêm vào chữ ký hàm và vào cả bốn chỗ gọi. Mỗi chỗ lại là một cơ hội truyền nhầm, y như chuyện múi giờ.',
         'A new settings parameter must go into the function signature and into all four call sites. Each site is another chance to pass it wrong, just like the time zone.'),
        ('composed', 's1', 'Nối hàm theo đúng thứ tự chạy', 'Chaining in run order',
         '::parse compose ::assign compose ::price đọc từ trái sang phải đúng như máy chạy, giống một dây chuyền: món hàng đi qua từng trạm theo thứ tự. Mỗi trạm nhận đúng loại hàng trạm trước giao ra: String → Request → Booking → Priced. Nếu xếp sai thứ tự, trình biên dịch báo lỗi ngay.',
         '::parse compose ::assign compose ::price reads left to right exactly as it runs, like an assembly line: the item goes through each station in order. Each station takes exactly what the previous one hands over: String → Request → Booking → Priced. Put them in the wrong order and the compiler complains at once.'),
        ('composed', 's2', 'Chốt ba tham số chung một lần', 'Locking in the three shared arguments once',
         'formatFor(VI, VND, CLINIC_ZONE) trả về một hàm show chỉ còn cần hai đối số. Ba giá trị kia đã được "nhớ" sẵn bên trong show. Kỹ thuật này gọi là partial application. Bốn chỗ gọi giờ chỉ còn 8 đối số, không cái nào lặp.',
         'formatFor(VI, VND, CLINIC_ZONE) returns a show function that needs only two arguments. The other three values are already "remembered" inside show. This technique is called partial application. The four call sites are now down to 8 arguments, none repeated.'),
        ('composed', 's3', 'Bốn màn, một múi giờ', 'Four screens, one time zone',
         'Múi giờ chỉ được viết đúng một lần, ở dòng tạo show. Cả bốn màn đều hiện 09:00, và không còn chỗ nào để chép nhầm UTC.',
         'The time zone is written exactly once, on the line that builds show. All four screens show 09:00, and there is nowhere left to copy UTC by mistake.'),
        ('composed', 's4', 'Thêm "đồng hồ 24 giờ": sửa 1 chỗ', 'Adding a "24-hour clock": 1 place to edit',
         'Tham số mới chỉ cần thêm vào formatFor và vào dòng tạo show. Bốn chỗ gọi giữ nguyên.',
         'The new parameter only goes into formatFor and the line that builds show. The four call sites stay as they are.'),
    ]
    for case, k, tv, te, xv, xe in S:
        sid = case + '.' + k
        m('s.%s.title' % sid, tv, te); m('s.%s.explain' % sid, xv, xe); m('ev.' + sid, tv, te)
    for k, vi, en in [
        ('try', 'Mẹo đọc: bảng trên cho thấy thứ tự đọc so với thứ tự chạy; bảng dưới cho thấy đối số và giờ hiện ở từng màn.', 'Reading tip: the top table compares reading order with run order; the bottom table shows the arguments and the time on each screen.'),
        ('nested.s2', 'Hàm có quá nhiều tham số thường là dấu hiệu thiết kế chưa tốt. Khi thiết kế, hãy đặt tham số ít thay đổi lên trước và tham số hay thay đổi ra sau, để sau này dễ chốt sẵn phần đầu. [[src:book-fp-tut]]',
         'A function with too many parameters is usually a sign of weak design. When designing, put the rarely-changing parameters first and the often-changing ones last, so the first ones are easy to lock in later. [[src:book-fp-tut]]'),
        ('nested.s3', 'Khi cùng một bộ giá trị phải chép ở nhiều nơi, mỗi nơi là một cơ hội sai, và dòng sai trông y hệt dòng đúng. Cách chữa là gom chúng về đúng một chỗ.',
         'When the same set of values must be copied to many places, each place is a chance to get it wrong, and the wrong line looks just like the right ones. The cure is to gather them in exactly one place.'),
        ('nested.s4', 'Mỗi tham số là một thứ người đọc phải giữ trong đầu. Sáu tham số cộng thêm vài biến cục bộ là dễ vượt ngưỡng khoảng 7 thứ mà Seemann đề xuất (chương J1, "Mã phải vừa trong đầu", của track Mã sạch và kỷ luật làm nghề). [[src:book-seemann]]',
         'Every parameter is one more thing the reader must hold in mind. Six parameters plus a few local variables easily pass the threshold of about 7 things that Seemann proposes (chapter J1, "Code that fits in your head", of the Clean Code and Craft track). [[src:book-seemann]]'),
        ('composed.s1', 'f compose g là một hàm mới: chạy f trước, đưa kết quả cho g. Thư viện chuẩn của Kotlin chưa có sẵn hàm này, nhưng tự viết chỉ mất một dòng (xem đoạn mã trong bài). [[src:book-fp-tut]]',
         'f compose g is a new function: run f first, hand the result to g. Kotlin\'s standard library does not ship it, but writing it yourself takes one line (see the code in the lesson). [[src:book-fp-tut]]'),
        ('composed.s2', 'Hàm bên trong "nhớ" được các giá trị của hàm bên ngoài nhờ closure. Đây cũng là lý do partial application viết gọn được trong Kotlin: chỉ là một hàm trả về một lambda. [[src:book-fp-manning]]',
         'The inner function "remembers" the outer function\'s values thanks to a closure. That is why partial application is so short in Kotlin: it is just a function returning a lambda. [[src:book-fp-manning]]'),
        ('composed.s3', 'Partial application rất gần với dependency injection: chốt sẵn những phụ thuộc chung (như database hay cấu hình), chỉ truyền phần khác nhau ở mỗi lần dùng. [[src:book-fp-tut]]',
         'Partial application is very close to dependency injection: lock in the shared dependencies (like a database or settings) and pass only what differs each time. [[src:book-fp-tut]]'),
        ('composed.s4', 'Về lý thuyết, mọi hàm nhiều tham số đều có thể biến thành chuỗi hàm một tham số (currying). Nhưng khi có nhiều tham số, cách đó dễ làm mã khó đọc. Một hàm tạo như formatFor thường rõ ràng hơn. [[src:book-fp-tut]]',
         'In theory, every multi-parameter function can become a chain of one-parameter functions (currying). But with many parameters that easily makes code hard to read. A builder like formatFor is usually clearer. [[src:book-fp-tut]]'),
    ]:
        m('co.' + k, vi, en)

    z = lambda k, vi, en=None: a('vz.' + k, vi, en)
    z('tab.compose', 'Luồng hàm và chỗ gọi', 'Function flow and call sites')
    z('compose.cap.nested', 'Khi gọi lồng nhau: máy chạy theo cột "Chạy", còn mắt đọc theo cột "Đọc". Ô đỏ: hai thứ tự ngược nhau.', 'With nested calls: the machine follows the "Run" column, the eye follows the "Read" column. Red: the two orders disagree.')
    z('compose.cap.composed', 'Khi nối hàm thành chuỗi: thứ tự đọc trùng với thứ tự chạy.', 'When the functions are chained: reading order matches run order.')
    z('compose.scap', 'Bốn chỗ gọi: {a} đối số, {r} trong đó là cấu hình lặp lại.', 'Four call sites: {a} arguments, {r} of them repeated settings.')
    z('compose.legend', 'Ô mờ: đối số cấu hình bị lặp lại. Đỏ: múi giờ chép nhầm, hay giờ hiện khác các màn còn lại. Viền ở bước 4: chỗ phải sửa khi thêm tham số. "?": chưa tới bước đó.', 'Faded: a repeated settings argument. Red: a wrongly copied time zone, or a time that differs from the other screens. Outlined in step 4: what to edit for a new parameter. "?": that step has not come yet.')
    for k, vi, en in [('run', 'Chạy', 'Run'), ('read', 'Đọc', 'Read'), ('fn', 'Hàm', 'Function'), ('type', 'Nhận vào → trả ra', 'Takes → returns'), ('value', 'Giá trị sau bước', 'Value after the step'),
                      ('site', 'Màn hình', 'Screen'), ('args', 'Đối số', 'Arguments'), ('out', 'Chữ hiện ra', 'Shown text')]:
        z('compose.col.' + k, vi, en)
    for k, vi, en in [('list', 'danh sách', 'list'), ('detail', 'chi tiết', 'detail'), ('reminder', 'tin nhắc', 'reminder'), ('receipt', 'biên lai', 'receipt')]:
        z('compose.site.' + k, vi, en)
    z('compose.site.build', 'tạo show (một lần)', 'building show (once)')
    z('compose.build.out', 'một hàm (Priced, Boolean) -> String', 'a (Priced, Boolean) -> String function')
    z('compose.edits.none', 'Bước 4 sẽ thêm một tham số cấu hình mới.', 'Step 4 adds a new settings parameter.')
    z('compose.edits.nested', 'Thêm tham số "đồng hồ 24 giờ": sửa chữ ký hàm và {n} chỗ gọi.', 'Adding a "24-hour clock" parameter: edit the signature and {n} call sites.')
    z('compose.edits.composed', 'Thêm tham số "đồng hồ 24 giờ": sửa formatFor và {n} dòng tạo show; các chỗ gọi giữ nguyên.', 'Adding a "24-hour clock" parameter: edit formatFor and {n} line building show; the call sites stay the same.')

    C = 'p3'
    a(C + '.title', 'Ghép hàm: composition, currying, partial application', 'Composing functions: composition, currying, partial application')
    a(C + '.essence', 'Nối hàm (composition) giống một dây chuyền: f compose g là "chạy f, rồi đưa kết quả cho g". Chuỗi viết bằng compose đọc đúng thứ tự chạy, còn lời gọi lồng nhau phải đọc từ trong ra.\nPartial application là chốt sẵn một số tham số và nhận về một hàm chỉ cần phần còn lại. Currying là trường hợp đặc biệt: biến hàm nhiều tham số thành chuỗi hàm một tham số.\nQuy tắc dễ nhớ: thứ gì lặp lại ở nhiều chỗ gọi thì chốt nó một lần. Chỗ gọi ngắn lại, và không còn chỗ nào truyền nhầm.',
      'Composition is like an assembly line: f compose g means "run f, then hand the result to g". A chain written with compose reads in run order, while nested calls must be read from the inside out.\nPartial application locks in some parameters and gives back a function needing only the rest. Currying is a special case: turning a multi-parameter function into a chain of one-parameter functions.\nAn easy rule: whatever repeats at many call sites, lock it in once. The calls get shorter, and nowhere is left to pass it wrong.')
    a(C + '.goal.g1', 'Đã đếm đối số ở bốn chỗ gọi', 'Counted the arguments at the four call sites')
    a(C + '.goal.g2', 'Đã thấy thêm tham số phải sửa mấy chỗ', 'Saw how many places a new parameter touches')
    a(C + '.sim.fp.compose', 'gọi lồng nhau hay nối hàm', 'nested calls or chained functions')

    S_ = 'hook'
    a(C + '.sec.%s.title' % S_, 'Đoán trước khi đọc', 'Predict before reading')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'predict', 'Hàm formatAppointment có 6 tham số và được gọi ở 4 màn hình; ba tham số đầu (ngôn ngữ, tiền tệ, múi giờ) giống nhau ở mọi màn. Một hôm, tin nhắc lịch hiện giờ lệch 7 tiếng so với màn chi tiết. Bạn sẽ tìm lỗi ở đâu trước?',
      'formatAppointment has 6 parameters and is called on 4 screens; the first three (locale, currency, time zone) are the same everywhere. One day the reminder shows a time 7 hours off from the detail screen. Where would you look first?')
    B(C, S_, 1, 'ans', 'Ở các chỗ gọi hàm: một trong bốn chỗ đã truyền múi giờ khác (ở đây là UTC chép từ bài test). Khi một bộ giá trị phải chép đi nhiều nơi, lỗi thường nằm ở chính việc chép. Cách phòng: chốt bộ giá trị đó ở một chỗ duy nhất.',
      'At the call sites: one of the four passed a different time zone (here UTC, copied from a test). When the same values must be copied to many places, the bug usually lives in the copying itself. The prevention: lock those values in one single place.')

    S_ = 'compose'
    a(C + '.sec.%s.title' % S_, 'Nối hàm thành dây chuyền', 'Chaining functions like an assembly line')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'p', 'Hãy hình dung một dây chuyền đóng gói: món hàng đi qua trạm cân, trạm dán nhãn, rồi trạm đóng thùng. Mỗi trạm làm một việc và đưa kết quả cho trạm sau. Nối hàm cũng vậy: f compose g là một hàm mới, chạy f trước rồi đưa kết quả cho g. [[src:book-fp-tut]]',
      'Picture a packing line: an item goes through the weighing station, the labelling station, then the boxing station. Each station does one job and hands the result to the next. Chaining functions works the same way: f compose g is a new function that runs f first and hands its result to g. [[src:book-fp-tut]]')
    B(C, S_, 2, 'p', 'Dây chuyền chỉ chạy được khi đầu ra của trạm trước vừa với đầu vào của trạm sau, và trình biên dịch Kotlin kiểm điều đó giúp bạn. Nếu các hàm đều thuần (chương "Hàm thuần và referential transparency"), cả dây chuyền cũng là một hàm thuần: test được từng trạm, và test được cả dây. [[src:book-fp-tut]]',
      'The line only works when each station\'s output fits the next one\'s input, and the Kotlin compiler checks that for you. If every function is pure (the chapter "Pure functions and referential transparency"), the whole line is a pure function too: you can test each station, and the whole line. [[src:book-fp-tut]]')
    B(C, S_, 3, 'kt', 'infix fun <A, B, C> ((A) -> B).compose(g: (B) -> C): (A) -> C = { a -> g(this(a)) }\n\nval toPriced: (String) -> Priced = ::parse compose ::assign compose ::price\n// cùng nghĩa với: { raw -> price(assign(parse(raw))) }',
      'infix fun <A, B, C> ((A) -> B).compose(g: (B) -> C): (A) -> C = { a -> g(this(a)) }\n\nval toPriced: (String) -> Priced = ::parse compose ::assign compose ::price\n// means the same as: { raw -> price(assign(parse(raw))) }')
    B(C, S_, 4, 'p', 'So hai cách viết ở dòng cuối: bản dùng compose đọc từ trái sang phải đúng thứ tự chạy; bản lồng nhau phải đọc từ trong ra ngoài. Với ba, bốn bước, khác biệt này đã rõ rệt.',
      'Compare the two forms on the last line: the compose version reads left to right in run order; the nested version must be read from the inside out. With three or four steps, the difference is already obvious.')

    S_ = 'curry'
    a(C + '.sec.%s.title' % S_, 'Currying: hàm nhiều tham số thành chuỗi hàm một tham số', 'Currying: a multi-parameter function as a chain of one-parameter functions')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'p', 'compose chỉ nối được hàm một tham số. Vậy hàm hai tham số thì sao? Mẹo là: hàm nhận hai tham số có thể viết thành hàm nhận một tham số và trả về một hàm khác nhận tham số thứ hai. Ví dụ, cộng(a, b) thành cộng(a) trả về { b -> a + b }. Khi đó cộng(3) là một hàm "cộng thêm 3", gọi với 4 thì ra 7. Cách biến đổi này gọi là currying, theo tên nhà toán học Haskell Curry. [[src:book-fp-tut]]',
      'compose only chains one-parameter functions. What about two parameters? The trick: a function taking two parameters can be written as a function taking one parameter that returns another function taking the second. For example, add(a, b) becomes add(a) returning { b -> a + b }. Then add(3) is an "add 3" function, and calling it with 4 gives 7. This transformation is called currying, after the mathematician Haskell Curry. [[src:book-fp-tut]]')
    B(C, S_, 2, 'p', 'Có một điều thú vị: chỉ nhìn chữ ký curry(f: (A, B) -> C): (A) -> (B) -> C, bạn gần như chỉ có một cách viết thân hàm cho đúng kiểu. Nhiều khi lập trình hàm giống ghép hình: các mảnh chỉ khớp theo một cách. [[src:book-fp-manning]]',
      'An interesting point: looking only at the signature curry(f: (A, B) -> C): (A) -> (B) -> C, there is essentially one way to write the body that fits the types. Functional programming is often like a jigsaw: the pieces fit only one way. [[src:book-fp-manning]]')

    S_ = 'partial'
    a(C + '.sec.%s.title' % S_, 'Chốt sẵn tham số: partial application', 'Locking in parameters: partial application')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'p', 'Partial application là chốt sẵn một số tham số, nhận về một hàm chỉ cần phần còn lại. Giống mẫu đơn in sẵn tên phòng khám và địa chỉ: mỗi lần dùng, bạn chỉ điền tên bệnh nhân. Trong Kotlin, đó đơn giản là một hàm trả về lambda; lambda "nhớ" các giá trị đã chốt nhờ closure. [[src:book-fp-manning]]',
      'Partial application locks in some parameters and gives back a function needing only the rest. Like a form with the clinic\'s name and address pre-printed: each time, you only fill in the patient\'s name. In Kotlin it is simply a function returning a lambda; the lambda "remembers" the locked-in values thanks to a closure. [[src:book-fp-manning]]')
    B(C, S_, 2, 'kt', 'fun formatFor(locale: Locale, currency: Currency, zone: ZoneId): (Priced, Boolean) -> String =\n    { p, compact -> formatAppointment(locale, currency, zone, p.booking, p.fee, compact) }\n\nval show = formatFor(VI, VND, CLINIC_ZONE)   // ba thông số ít đổi: chốt một lần\nshow(toPriced(raw), false)                  // mỗi lần chỉ truyền phần khác nhau',
      'fun formatFor(locale: Locale, currency: Currency, zone: ZoneId): (Priced, Boolean) -> String =\n    { p, compact -> formatAppointment(locale, currency, zone, p.booking, p.fee, compact) }\n\nval show = formatFor(VI, VND, CLINIC_ZONE)   // the three rarely-changing ones: locked in once\nshow(toPriced(raw), false)                  // each time, pass only what differs')
    B(C, S_, 3, 'p', 'Nếu bạn đã dùng dependency injection, ý này sẽ quen: chốt sẵn phụ thuộc chung một lần, chỉ truyền phần khác nhau. Hai lời khuyên khi thiết kế: đặt tham số ít đổi lên trước, hay đổi ra sau; và nếu hàm cần quá nhiều tham số, đó thường là dấu hiệu nên tách nó ra. [[src:book-fp-tut]]',
      'If you have used dependency injection, this will feel familiar: lock in the shared dependencies once, pass only what differs. Two design tips: put rarely-changing parameters first and often-changing ones last; and if a function needs too many parameters, that is usually a sign it should be split. [[src:book-fp-tut]]')

    S_ = 'kotlin'
    a(C + '.sec.%s.title' % S_, 'Trong mã Kotlin hằng ngày', 'In everyday Kotlin code')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'p', 'Kotlin có đủ đồ nghề để nối hàm: kiểu hàm, lambda, tham chiếu hàm như ::parse, và hàm infix (chương K8, "Lambda, closure và inline", của track Kotlin). Thư viện chuẩn không có sẵn compose hay curry, nhưng tự viết chỉ mất một dòng. Một cách khác để đọc từ trái sang phải là dùng let: raw.let(::parse).let(::assign).let(::price). [[src:book-fp-tut]]',
      'Kotlin has all the tools for chaining: function types, lambdas, function references like ::parse, and infix functions (chapter K8, "Lambdas, closures and inline", of the Kotlin track). The standard library has no compose or curry, but writing them takes one line. Another way to read left to right is let: raw.let(::parse).let(::assign).let(::price). [[src:book-fp-tut]]')
    B(C, S_, 2, 'note', 'Đừng nối hàm cho bằng được. Một chuỗi dài compose với tham số bị đảo qua đảo lại có thể khó đọc hơn một lời gọi bình thường. Mục tiêu là mã dễ đọc và khó truyền sai, không phải mã không còn dấu ngoặc nào.',
      'Do not chain at all costs. A long compose chain with parameters flipped around can read worse than an ordinary call. The goal is code that is easy to read and hard to call wrong, not code without parentheses.')
    B(C, S_, 2, 'kind', 'pitfall')

    S_ = 'bugs'
    a(C + '.sec.%s.title' % S_, 'Hai lỗi hay gặp', 'Two common bugs')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'bug', 'Tin nhắc lịch hiện giờ lệch 7 tiếng so với màn chi tiết.', 'The reminder shows a time 7 hours off from the detail screen.')
    B(C, S_, 1, 'cause', 'Một trong bốn chỗ gọi hàm định dạng 6 tham số truyền múi giờ UTC chép từ bài test; ba thông số cấu hình bị lặp lại ở mọi chỗ gọi.', 'One of the four calls to the 6-parameter formatter passes the UTC time zone copied from a test; the three settings are repeated at every call site.')
    B(C, S_, 1, 'fix', 'Chốt cấu hình một lần (partial application, hoặc một hàm tạo như formatFor) để mỗi chỗ gọi chỉ truyền phần khác nhau.', 'Lock in the settings once (partial application, or a builder such as formatFor) so each call site passes only what differs.')
    B(C, S_, 2, 'bug', 'Sau khi gộp list.map(f).map(g) thành list.map(f compose g), một bài test kiểm thứ tự dòng log bị đỏ.', 'After merging list.map(f).map(g) into list.map(f compose g), a test checking the order of log lines turns red.')
    B(C, S_, 2, 'cause', 'Nếu f và g thuần, hai cách cho cùng kết quả. Nhưng f có ghi log: cách đầu chạy f cho mọi phần tử rồi mới tới g, cách sau chạy f rồi g cho từng phần tử, nên thứ tự các dòng log khác đi.', 'If f and g are pure, both forms give the same result. But f logs: the first form runs f on every element before g, the second runs f then g per element, so the log lines come out in a different order.')
    B(C, S_, 2, 'fix', 'Giữ các bước trong dây chuyền thuần, và ghi log ở bên ngoài như chương "Hàm thuần và referential transparency". Khi đó gộp hay tách map là thay đổi an toàn.', 'Keep the steps in the chain pure, and log outside, as in the chapter "Pure functions and referential transparency". Then merging or splitting maps is a safe change.')

    S_ = 'ex'
    a(C + '.sec.%s.title' % S_, 'Bài tập', 'Exercise')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'ex', 'Viết hàm curry cho hàm hai tham số, rồi dùng nó để tạo một hàm tính phí cả tuần cho một bác sĩ từ fee(doctor, day). Vì sao nên đặt doctor trước day?',
      'Write curry for a two-parameter function, then use it to build a whole-week fee function for one doctor from fee(doctor, day). Why should doctor come before day?')
    B(C, S_, 1, 'exkt', 'fun fee(doctor: Doctor, day: DayOfWeek): Long = TODO()\n\nfun <A, B, C> ((A, B) -> C).curry(): (A) -> (B) -> C = TODO()')
    B(C, S_, 1, 'hint', 'Kiểu trả về là một hàm nhận A và trả về một hàm nhận B. Chỉ có một cách lấy được giá trị kiểu C.', 'The return type is a function taking A that returns a function taking B. There is only one way to get a C.')
    B(C, S_, 1, 'sol', 'Chỉ có một thân hàm hợp kiểu: { a -> { b -> this(a, b) } }. ::fee.curry()(an) cho một hàm (DayOfWeek) -> Long dùng được cho cả tuần. doctor đứng trước vì ít thay đổi hơn day; tham số ít đổi đặt trước thì mới chốt sẵn được bằng curry hay partial application.',
      'Only one body fits the types: { a -> { b -> this(a, b) } }. ::fee.curry()(an) gives a (DayOfWeek) -> Long usable for the whole week. doctor comes first because it changes less often than day; rarely-changing parameters must come first to be locked in with curry or partial application.')
    B(C, S_, 1, 'solkt', 'fun <A, B, C> ((A, B) -> C).curry(): (A) -> (B) -> C = { a -> { b -> this(a, b) } }\n\nval feeForAn: (DayOfWeek) -> Long = ::fee.curry()(an)\nval week: List<Long> = DayOfWeek.values().map(feeForAn)')

    for q, qv, qe, av, ae, wv, we in [
        ('q1', 'f compose g, gọi với x, cho ra gì?', 'What does f compose g give when called with x?', 'Bằng g(f(x)).', 'It gives g(f(x)).', 'f chạy trước; g nhận kết quả của f.', 'f runs first; g receives f\'s result.'),
        ('q2', 'curry biến hàm (A, B) -> C thành kiểu gì?', 'What type does curry turn (A, B) -> C into?', '(A) -> (B) -> C, một chuỗi hàm một tham số.', '(A) -> (B) -> C, a chain of one-parameter functions.', 'Một hàm nhận A, trả về một hàm nhận B.', 'A function taking A that returns a function taking B.'),
        ('q3', 'Thiết kế hàm để dễ chốt sẵn từng phần: tham số nào nên đặt trước?', 'Designing a function to be locked in piece by piece: which parameters go first?', 'Những tham số ít thay đổi nhất.', 'The ones least likely to change.', 'Khi đó chốt chúng bằng curry hay partial application rất tự nhiên.', 'Then locking them in with curry or partial application comes naturally.'),
        ('q4', 'assign: (Request) -> Booking và price: (Booking) -> Priced. ::price compose ::assign có biên dịch không?', 'assign: (Request) -> Booking and price: (Booking) -> Priced. Does ::price compose ::assign compile?', 'Không.', 'No.', 'Đầu ra của price (Priced) không vừa với đầu vào của assign (Request); thứ tự đúng là ::assign compose ::price.', 'price\'s output (Priced) does not fit assign\'s input (Request); the right order is ::assign compose ::price.')]:
        a(C + '.quiz.%s.q' % q, qv, qe); a(C + '.quiz.%s.a' % q, av, ae); a(C + '.quiz.%s.why' % q, wv, we)
