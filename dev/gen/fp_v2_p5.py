# Lập trình hàm · K5 (p5): lỗi là giá trị (Phần 2: lỗi, ngữ cảnh và state)
# Nguồn (chỉ ghi ở đây và docs/research/fp.md): Vermeulen, Bjarnason, Chiusano, FP in Kotlin ch.4 (4.1 ngoại lệ phá RT, không an toàn kiểu;
# 4.2 sentinel value); Carli, FP in Kotlin by Tutorials ch.14 (đưa side effect vào kiểu trả về, fail fast và gom lỗi, Result<T>, ViewModel dùng fold);
# Barbini, From Objects to Functions ch.7 (null khi lý do hiển nhiên, Pair lỗi kèm kết quả, giữ ngoại lệ cho việc không cứu được, Outcome sealed);
# API kotlin.Result và runCatching (đọc 2026-11-25, bản 2.4); Arrow typed errors và setup (2.3.0, đọc 2026-11-25). Giọng văn dạy học.

SEC_ORDER = {'p5': ['hook', 'why', 'ladder', 'chain', 'arrow', 'bugs', 'ex', 'recall']}


def add(a):
    def B(ch, sec, n, field, vi, en=None):
        a('%s.sec.%s.b.%02d.%s' % (ch, sec, n, field), vi, vi if en is None else en)

    a('preset.errors', '''Lập trình hàm · lỗi là giá trị''', '''Functional programming · errors as values''')
    m = lambda k, vi, en=None: a('m.errors.' + k, vi, en)
    m('title', '''Một quy trình đặt lịch, bốn cách báo lỗi''', '''One booking flow, four ways to report errors''')
    m('overview', '''Quy trình đặt lịch của app Hẹn Khám có bốn bước: đọc số điện thoại, tìm giờ trống, kiểm số lượt còn lại trong tuần, lưu lịch. Ta viết cùng quy trình này theo bốn cách (ngoại lệ, trả null, Result, kiểu lỗi riêng) rồi chạy bốn tình huống: mọi thứ suôn sẻ, giờ đã có người đặt, một bug trong hàm kiểm lượt, và một loại lỗi mới (phòng khám nghỉ đột xuất).''',
      '''The ClinicBook booking flow has four steps: read the phone number, find a free slot, check how many bookings are left this week, save the booking. We write this same flow four ways (exceptions, returning null, Result, a custom error type) and run four situations: everything goes well, the slot is already taken, a bug in the quota check, and a new kind of error (the clinic closes unexpectedly).''')
    m('wrapup', '''Ngoại lệ bắt chung báo "thất bại" cho mọi thứ và giấu luôn bug. null dừng đúng chỗ nhưng mất lý do. Result giữ được lý do nếu bạn đoán đúng lớp ngoại lệ, nhưng runCatching cũng gói luôn bug. Kiểu lỗi riêng liệt kê đủ lỗi nghiệp vụ ngay trong chữ ký, để bug đi lên như một bug, và khi có lỗi mới thì trình biên dịch chỉ ra chỗ cần sửa.''',
      '''A catch-all exception handler says "failed" for everything and hides bugs too. null stops at the right place but loses the reason. Result keeps the reason if you guess the right exception class, but runCatching wraps bugs as well. A custom error type lists every business error right in the signature, lets a bug travel up as a bug, and when a new error appears the compiler points at the place to fix.''')
    m('simp.1', '''Trong mô phỏng, mỗi bước chỉ hỏng theo một cách; hàm thật có thể hỏng ở nhiều chỗ, kể cả lỗi mạng ở bước lưu.''',
      '''In the simulation each step fails in only one way; real functions can fail in several places, including a network error at the save step.''')
    m('simp.2', '''Hành vi của Result và runCatching theo trang API của thư viện chuẩn Kotlin (bản 2.4, đọc ngày 2026-11-25); Arrow theo tài liệu typed errors và trang cài đặt (bản 2.3.0, đọc ngày 2026-11-25). Outcome là kiểu tự viết của site, không có trong thư viện chuẩn. Site không chạy Kotlin trong trang.''',
      '''The behaviour of Result and runCatching follows the Kotlin standard library API pages (version 2.4, read on 2026-11-25); Arrow follows its typed errors docs and setup page (version 2.3.0, read on 2026-11-25). Outcome is a type the site writes itself; it is not in the standard library. The site does not run Kotlin in the page.''')
    m('ctl.hint', '''Chọn một cách báo lỗi rồi đi qua bốn tình huống; so cột "đường lỗi" và dòng "màn hình hiện" ở bước 2 và bước 3.''',
      '''Pick a way of reporting errors and walk through the four situations; compare the "error track" column and the "the screen shows" line at steps 2 and 3.''')
    m('ctl.case', '''Cách báo lỗi''', '''How errors are reported''')
    for k, vi, en in [('throw', 'ngoại lệ, màn hình bắt mọi Exception', 'exceptions, the screen catches every Exception'), ('nullable', 'trả null', 'returning null'),
                      ('result', 'Result và runCatching', 'Result and runCatching'), ('typed', 'kiểu lỗi riêng (sealed interface)', 'a custom error type (sealed interface)')]:
        m('ctl.case.' + k, vi, en)
    m('diagramTitle', '''Đầu vào, chuỗi bước, đường lỗi, màn hình''', '''Input, the chain of steps, the error track, the screen''')
    m('diagramDesc', '''Đầu vào đi qua bốn bước; lỗi rẽ sang đường lỗi rồi tới màn hình, hoặc không ai bắt và app crash''', '''The input goes through four steps; an error turns onto the error track and reaches the screen, or nobody catches it and the app crashes''')
    for k, vi, en in [('input', 'Đầu vào (số điện thoại, mã giờ)', 'Input (phone number, slot id)'), ('chain', 'Bốn bước đặt lịch', 'The four booking steps'),
                      ('screen', 'Màn hình', 'The screen'), ('rail', 'Đường lỗi', 'The error track')]:
        m('n.' + k, vi, en)
    m('met.ran', '''Số bước đã chạy''', '''Steps that ran'''); m('met.reason', '''Màn hình biết lý do''', '''The screen knows the reason''')
    m('met.hidden', '''Bug bị giấu''', '''Bug hidden'''); m('met.flagged', '''Chỗ trình biên dịch chỉ ra''', '''Places the compiler points to''')
    a('cap.errors', '''Đầu vào đi qua bốn bước đặt lịch. Gặp lỗi, kết quả rẽ sang đường lỗi rồi tới màn hình; lỗi không ai bắt thì làm cả chuỗi dừng (crash). Ô đỏ: màn hình nói sai hoặc không đủ, hay app crash.''',
      '''The input goes through the four booking steps. On an error, the result turns onto the error track and reaches the screen; an error nobody catches stops the whole chain (a crash). A red box: the screen says something wrong or too vague, or the app crashes.''')
    S = [
        ('throw', 's1', 'Đường thành công: bốn bước chạy hết', 'The success path: all four steps run',
         'Số 0901234567 hợp lệ, giờ S12 còn trống, còn 2 lượt trong tuần: bốn hàm chạy lần lượt và book trả Booking(41). Chữ ký book(...): Booking chỉ kể đường thành công. Muốn biết hàm có thể hỏng ra sao, bạn phải đọc thân của nó và của mọi hàm nó gọi.',
         'The number 0901234567 is valid, slot S12 is free, 2 bookings are left this week: the four functions run in turn and book returns Booking(41). The signature book(...): Booking only tells the success story. To learn how the function can fail, you must read its body and the body of every function it calls.'),
        ('throw', 's2', 'Giờ đã có người đặt: catch chung chỉ nói "thất bại"', 'The slot is taken: the catch-all only says "failed"',
         'findFreeSlot ném SlotTakenException; hai bước sau không chạy. Ngoại lệ bay lên tới catch (e: Exception) ở màn hình, nơi chỉ biết là "có gì đó hỏng". Người dùng đọc "Đặt lịch thất bại" mà không biết chỉ cần chọn giờ khác.',
         'findFreeSlot throws SlotTakenException; the next two steps do not run. The exception flies up to the catch (e: Exception) on the screen, which only knows that "something broke". The user reads "Booking failed" without learning that picking another slot would do.'),
        ('throw', 's3', 'Bug bị nuốt', 'The bug is swallowed',
         'Số mới 0987654321 chưa có trong bảng lượt, và checkQuota viết quotas[phone]!!, nên ném NullPointerException. Đây là bug cần sửa, nhưng catch (e: Exception) bắt luôn nó và cũng hiện "Đặt lịch thất bại". Không crash, không báo cáo lỗi nào: bug nằm im trên máy người dùng.',
         'The new number 0987654321 is not in the quota table yet, and checkQuota writes quotas[phone]!!, so it throws NullPointerException. This is a bug that must be fixed, but catch (e: Exception) catches it too and also shows "Booking failed". No crash, no error report: the bug sits quietly on users\' phones.'),
        ('throw', 's4', 'Thêm lỗi mới: không chỗ nào bị buộc xử lý', 'A new error: nothing is forced to handle it',
         'Phòng khám nghỉ đột xuất thứ Bảy 28/11, nên findFreeSlot giờ có thể ném ClinicClosedException. Trình biên dịch không biết hàm có thể ném gì, nên không chỗ gọi nào được nhắc. Màn hình vẫn hiện câu chung chung.',
         'The clinic closes unexpectedly on Saturday 28/11, so findFreeSlot can now throw ClinicClosedException. The compiler does not know what a function may throw, so no caller is reminded. The screen still shows the vague message.'),
        ('nullable', 's1', 'Mỗi bước trả null khi hỏng', 'Each step returns null on failure',
         'Ở cách này, các hàm phụ trả null thay vì ném, và ?: return null dừng book ngay ở bước hỏng. Đường thành công vẫn chạy đủ bốn bước. Chữ ký Booking? thật thà hơn: nó nói rõ "có thể không có kết quả".',
         'Here the helper functions return null instead of throwing, and ?: return null stops book right at the failing step. The success path still runs all four steps. The Booking? signature is more honest: it clearly says "there may be no result".'),
        ('nullable', 's2', 'Có null, nhưng mất lý do', 'A null, but the reason is lost',
         'findFreeSlot trả null, nên book trả null. Màn hình chỉ biết "không có Booking", không biết vì số sai, vì giờ đã có người đặt hay vì hết lượt: ba lý do khác nhau dồn vào cùng một giá trị null.',
         'findFreeSlot returns null, so book returns null. The screen only knows "there is no Booking", not whether the number was wrong, the slot was taken or the quota ran out: three different reasons squeezed into the same null.'),
        ('nullable', 's3', 'Bug lộ ra khi test', 'The bug shows up in testing',
         'quotas[phone]!! vẫn ném NullPointerException, và không ai bắt nó. App crash khi test, kèm stack trace (danh sách các hàm đang chạy) chỉ đúng dòng sai, nên bug được sửa trước khi tới người dùng. null chỉ thay cho những lỗi bạn chủ động kiểm, không che bug.',
         'quotas[phone]!! still throws NullPointerException, and nobody catches it. The app crashes in testing with a stack trace (the list of functions that were running) pointing at the exact line, so the bug gets fixed before it reaches users. null only stands in for the errors you check on purpose; it does not hide bugs.'),
        ('nullable', 's4', 'Lỗi mới cũng chỉ là null', 'The new error is just another null',
         'Ngày nghỉ cũng trả null. Không có gì để trình biên dịch kiểm, và màn hình vẫn nói "thất bại".',
         'A closed day also returns null. There is nothing for the compiler to check, and the screen still says "failed".'),
        ('result', 's1', 'runCatching gói kết quả', 'runCatching wraps the result',
         'runCatching chạy cả khối; không có ngoại lệ thì trả Result.success(Booking). Chữ ký Result<Booking> nói rõ "có thể thất bại", nhưng không nói thất bại kiểu gì: phía lỗi luôn là một Throwable.',
         'runCatching runs the whole block; with no exception it returns Result.success(Booking). The signature Result<Booking> clearly says "this may fail", but not how: the failure side is always a Throwable.'),
        ('result', 's2', 'Biết lý do, nếu đoán đúng lớp', 'The reason is known, if you guess the class',
         'SlotTakenException được gói thành Result.failure. Màn hình kiểm e is SlotTakenException nên hiện đúng "Giờ này đã có người đặt". Nhưng danh sách lớp cần kiểm nằm trong đầu người viết, không nằm trong kiểu.',
         'SlotTakenException is wrapped into Result.failure. The screen checks e is SlotTakenException, so it shows the right "This slot is already taken". But the list of classes to check lives in the writer\'s head, not in the type.'),
        ('result', 's3', 'runCatching gói luôn cả bug', 'runCatching wraps the bug too',
         'runCatching bắt MỌI Throwable, nên NullPointerException cũng thành Result.failure, rơi vào nhánh else và hiện "Đặt lịch thất bại". Bug bị giấu y như với catch chung.',
         'runCatching catches EVERY Throwable, so the NullPointerException also becomes Result.failure, falls into the else branch and shows "Booking failed". The bug is hidden just as with the catch-all.'),
        ('result', 's4', 'Lỗi mới rơi vào nhánh else', 'The new error falls into else',
         'ClinicClosedException không khớp e is SlotTakenException, nên đi vào else. Không có gì nhắc bạn thêm một câu báo mới.',
         'ClinicClosedException does not match e is SlotTakenException, so it goes to else. Nothing reminds you to add a new message.'),
        ('typed', 's1', 'Lỗi nghiệp vụ là một kiểu có tên', 'Business errors are a named type',
         'BookingError liệt kê đủ ba lỗi nghiệp vụ. book trả Outcome<BookingError, Booking>: hoặc Ok(Booking), hoặc Err(một BookingError). Chữ ký giờ kể cả đường thành công lẫn mọi cách hỏng có thể xảy ra.',
         'BookingError lists all three business errors. book returns Outcome<BookingError, Booking>: either Ok(Booking) or Err(a BookingError). The signature now tells both the success path and every way it can fail.'),
        ('typed', 's2', 'Màn hình biết đúng lý do', 'The screen knows the exact reason',
         'findFreeSlot trả null nên book trả Err(SlotTaken("S07")) và dừng. when trên r.error chọn đúng nhánh SlotTaken: "Giờ này đã có người đặt". Không phải đoán lớp nào cả.',
         'findFreeSlot returns null, so book returns Err(SlotTaken("S07")) and stops. The when on r.error picks the SlotTaken branch: "This slot is already taken". No class guessing needed.'),
        ('typed', 's3', 'Bug không bị gói nhầm', 'The bug is not wrapped by mistake',
         'Không có catch chung: chỉ những lỗi đã khai báo mới thành Err. NullPointerException đi lên như một bug bình thường, app crash khi test và bug được sửa trước khi tới người dùng.',
         'There is no catch-all: only declared errors become Err. The NullPointerException travels up like any bug, the app crashes in testing, and the bug is fixed before it reaches users.'),
        ('typed', 's4', 'Thêm ClinicClosed: trình biên dịch chỉ ra chỗ cần sửa', 'Adding ClinicClosed: the compiler points at the place to fix',
         'Thêm data object ClinicClosed : BookingError, và một dòng kiểm ngay sau findFreeSlot: if (isClosed(slot)) return Err(BookingError.ClinicClosed). Câu when không có else nên không còn đủ nhánh và không biên dịch được, cho tới khi bạn viết câu báo cho ngày nghỉ. Lỗi mới không thể lặng lẽ đi qua.',
         'Add data object ClinicClosed : BookingError, plus one check right after findFreeSlot: if (isClosed(slot)) return Err(BookingError.ClinicClosed). The when has no else, so it is no longer complete and stops compiling until you write the message for a closed day. A new error cannot slip through silently.'),
    ]
    for case, k, tv, te, xv, xe in S:
        sid = case + '.' + k
        m('s.%s.title' % sid, tv, te); m('s.%s.explain' % sid, xv, xe); m('ev.' + sid, tv, te)
    for k, vi, en in [
        ('try', '''Mẹo đọc: mỗi hàng là một bước. Giá trị đi ở cột "đường thành công" cho tới khi gặp lỗi thì rẽ sang cột "đường lỗi", và các bước sau bị bỏ qua. Đổi cách báo lỗi rồi đi lại bốn bước.''',
         '''Reading tip: each row is a step. The value travels in the "success track" column until an error turns it onto the "error track" column, and the later steps are skipped. Change how errors are reported and walk the four steps again.'''),
        ('throw.s2', '''Marco Vermeulen và cộng sự chỉ ra: kiểu của một hàm ném ngoại lệ, như (Int) -> Int, không nói gì về lỗi, và trình biên dịch không buộc nơi gọi quyết định xử lý thế nào. [[src:book-fp-manning]]''',
         '''Marco Vermeulen and co-authors point out: the type of a throwing function, such as (Int) -> Int, says nothing about failure, and the compiler never forces callers to decide how to handle it. [[src:book-fp-manning]]'''),
        ('throw.s3', '''catch (e: Exception) không phân biệt lỗi bạn dự tính (giờ đã có người đặt) với lỗi bạn không ngờ (bug). Tài liệu Kotlin nói: catch đầu tiên có kiểu khớp sẽ thắng, và Exception là lớp cha của gần như mọi lỗi. [[src:kt-exceptions-lang]]''',
         '''catch (e: Exception) cannot tell an error you expected (the slot is taken) from one you did not (a bug). The Kotlin docs say: the first catch with a matching type wins, and Exception is the parent of almost every error. [[src:kt-exceptions-lang]]'''),
        ('throw.s4', '''Kotlin không có checked exception (ngoại lệ phải khai báo trong chữ ký), nên thêm một loại ngoại lệ mới không làm chỗ gọi nào báo lỗi biên dịch. [[src:kt-exceptions-lang]]''',
         '''Kotlin has no checked exceptions (exceptions that must be declared in the signature), so adding a new kind of exception makes no caller fail to compile. [[src:kt-exceptions-lang]]'''),
        ('nullable.s1', '''Uberto Barbini nhận xét: trả null khi có lỗi là đủ dùng nếu lý do hiển nhiên, ví dụ "không tìm thấy tệp". [[src:book-barbini]]''',
         '''Uberto Barbini notes: returning null on error works well enough when the reason is obvious, such as "the file was not found". [[src:book-barbini]]'''),
        ('nullable.s2', '''Khi có nhiều lý do hỏng, null gộp chúng làm một. Barbini chỉ ra rằng cách vá "trả thêm một chuỗi mô tả lỗi" (dùng Pair) vẫn buộc nơi gọi kiểm null và tự nhớ quy ước. [[src:book-barbini]]''',
         '''With several reasons to fail, null merges them into one. Barbini shows that the patch of "also returning an error string" (with a Pair) still makes callers check for null and remember the convention. [[src:book-barbini]]'''),
        ('nullable.s3', '''?: return null chỉ đổi những lỗi bạn chủ động kiểm thành null. Ngoại lệ do bug vẫn bay lên như thường, và đó là điều tốt: bug cần được thấy để được sửa.''',
         '''?: return null only turns the errors you check on purpose into null. An exception from a bug still flies up as usual, and that is good: a bug must be seen to be fixed.'''),
        ('nullable.s4', '''Vermeulen và cộng sự gọi đây là giá trị đặc biệt (sentinel value): lỗi lặng lẽ đi tiếp, và nơi gọi có thể quên kiểm. Với kiểu nullable, Kotlin ít ra buộc bạn kiểm null trước khi dùng giá trị. [[src:book-fp-manning]]''',
         '''Vermeulen and co-authors call this a sentinel value: the error silently travels on, and callers may forget to check. With nullable types, Kotlin at least makes you check for null before using the value. [[src:book-fp-manning]]'''),
        ('result.s1', '''Tài liệu Kotlin: Result gói hoặc một giá trị thành công kiểu T, hoặc một Throwable khi thất bại. [[src:kt-result]]''',
         '''The Kotlin docs: Result wraps either a successful value of type T or a Throwable on failure. [[src:kt-result]]'''),
        ('result.s2', '''Massimo Carli dùng Result cho đúng việc này: gói ngoại lệ thành giá trị trả về, rồi dùng fold để chọn trạng thái màn hình theo thành công hay thất bại. [[src:book-fp-tut]] [[src:kt-result]]''',
         '''Massimo Carli uses Result for exactly this: wrap the exception as a return value, then use fold to pick the screen state for success or failure. [[src:book-fp-tut]] [[src:kt-result]]'''),
        ('result.s3', '''Tài liệu nói runCatching bắt mọi Throwable ném ra trong khối và gói nó thành thất bại. Hệ quả: cả bug lẫn CancellationException (ngoại lệ dùng để hủy coroutine, tức đoạn mã chạy bất đồng bộ có thể tạm dừng) cũng bị gói. [[src:kt-runcatching]]''',
         '''The docs say runCatching catches any Throwable thrown from the block and wraps it as a failure. As a consequence, bugs and CancellationException (the exception used to cancel a coroutine, a piece of asynchronous code that can pause) are wrapped too. [[src:kt-runcatching]]'''),
        ('result.s4', '''Phía lỗi của Result luôn là Throwable, nên kiểu không thể liệt kê những lỗi nghiệp vụ nào có thể xảy ra. [[src:kt-result]]''',
         '''The failure side of Result is always a Throwable, so the type cannot list which business errors may happen. [[src:kt-result]]'''),
        ('typed.s1', '''Carli gọi cách này là đưa side effect vào kiểu trả về: hàm không ném nữa mà trả một giá trị mô tả cả hai khả năng, nên trở lại thành hàm thuần. [[src:book-fp-tut]]''',
         '''Carli calls this making the side effect part of the return type: the function no longer throws but returns a value describing both outcomes, so it becomes pure again. [[src:book-fp-tut]]'''),
        ('typed.s2', '''Dừng ngay ở lỗi đầu tiên (fail fast) hợp khi bước sau cần dữ liệu của bước trước: không có giờ trống thì không có gì để lưu. [[src:book-fp-tut]]''',
         '''Stopping at the first error (fail fast) fits when a later step needs the data of an earlier one: with no free slot there is nothing to save. [[src:book-fp-tut]]'''),
        ('typed.s3', '''Barbini giữ ngoại lệ cho những tình huống không thể phục hồi; lỗi nghiệp vụ dự tính trước thì thành giá trị. [[src:book-barbini]]''',
         '''Barbini keeps exceptions for situations that cannot be recovered from; expected business errors become values. [[src:book-barbini]]'''),
        ('typed.s4', '''Tài liệu Kotlin nói: when trên một sealed type mà phủ đủ mọi kiểu con thì không cần else; thêm kiểu con mới làm when đó không còn đủ nhánh. [[src:kt-sealed]]''',
         '''The Kotlin docs say: a when on a sealed type that covers every subtype needs no else; adding a new subtype makes that when incomplete. [[src:kt-sealed]]'''),
    ]:
        m('co.' + k, vi, en)

    z = lambda k, vi, en=None: a('vz.' + k, vi, en)
    z('tab.errors', '''Đường ray thành công và lỗi''', '''The success and error tracks''')
    for k, vi, en in [('ok', 'Đường thành công', 'Success track'), ('err', 'Đường lỗi', 'Error track')]:
        z('errors.col.' + k, vi, en)
    z('errors.skip', '''bỏ qua''', '''skipped''')
    z('errors.crash', '''{v}: không ai bắt, app crash''', '''{v}: nobody catches it, the app crashes''')
    z('errors.in.ok', '''Tình huống 1: số 0901234567, giờ S12 (thứ Bảy 28/11, 09:00) còn trống, còn 2 lượt trong tuần.''', '''Situation 1: number 0901234567, slot S12 (Saturday 28/11, 09:00) is free, 2 bookings left this week.''')
    z('errors.in.taken', '''Tình huống 2: giờ S07 đã có người đặt.''', '''Situation 2: slot S07 is already taken.''')
    z('errors.in.bug', '''Tình huống 3: số mới 0987654321 chưa có trong bảng lượt, và hàm kiểm lượt viết quotas[phone]!! (một bug).''', '''Situation 3: the new number 0987654321 is not in the quota table yet, and the quota check writes quotas[phone]!! (a bug).''')
    z('errors.in.closed', '''Tình huống 4: phòng khám nghỉ đột xuất thứ Bảy 28/11; nhóm thêm một lỗi mới, ClinicClosed.''', '''Situation 4: the clinic closes unexpectedly on Saturday 28/11; the team adds a new error, ClinicClosed.''')
    z('errors.screen', '''Màn hình hiện: {s}''', '''The screen shows: {s}''')
    for k, vi, en in [('booked', '"Đã đặt lịch"', '"Booked"'), ('failed', '"Đặt lịch thất bại", không rõ vì sao', '"Booking failed", with no reason'),
                      ('taken', '"Giờ này đã có người đặt"', '"This slot is already taken"'), ('crash', 'app crash khi test; stack trace chỉ đúng dòng bug', 'the app crashes in testing; the stack trace points at the buggy line'),
                      ('compile', 'chưa biên dịch được: when trên BookingError thiếu nhánh ClinicClosed (1 chỗ); viết xong nhánh đó thì màn hình hiện "Phòng khám nghỉ ngày này"', 'does not compile yet: the when on BookingError is missing the ClinicClosed branch (1 place); once that branch is written the screen shows "The clinic is closed that day"')]:
        z('errors.out.' + k, vi, en)
    z('errors.scr', '''Màn hình''', '''Screen''')
    z('errors.aria', '''Sơ đồ đường ray: {n} bước đã chạy; màn hình hiện {s}''', '''Railway diagram: {n} steps ran; the screen shows {s}''')
    z('errors.legend', '''Mỗi ga là một bước. Vệt màu là đường giá trị đã đi: xanh khi mọi bước suôn sẻ; vàng khi rẽ xuống đường lỗi ở ga hỏng rồi chạy thẳng tới màn hình, bỏ qua các ga sau (vòng nét đứt); đỏ và dừng ở một ga khi lỗi không ai bắt (app crash). Khung màn hình đỏ: màn hình nói sai hoặc không đủ.''',
      '''Each station is a step. The coloured trail is the path the value took: green when every step succeeds; yellow when it switches down to the error track at the failing station and runs straight to the screen, skipping the later stations (dashed circles); red, stopping at a station, when nobody catches the error (the app crashes). A red screen box: the screen says something wrong or too vague.''')

    C = 'p5'
    a(C + '.title', '''Lỗi là giá trị''', '''Errors as values''')
    a(C + '.essence', '''Ngoại lệ giấu lỗi khỏi chữ ký hàm và phá việc thay một lời gọi bằng giá trị của nó. Lập trình hàm đưa lỗi vào kiểu trả về: hàm trả "thành công hoặc lỗi", và lỗi là một giá trị bình thường.\nCó bốn mức: null (một lý do hiển nhiên); Result (lỗi là Throwable, lớp gốc của mọi lỗi; runCatching gói mọi thứ kể cả bug); kiểu lỗi riêng bằng sealed interface (liệt kê đủ lỗi nghiệp vụ, when không else buộc bạn xử lý lỗi mới); và Either (kiểu "lỗi hoặc kết quả") của thư viện Arrow.\nLỗi nghiệp vụ thành giá trị; bug và lỗi không cứu được vẫn là ngoại lệ, để chúng lộ ra và được sửa.''',
      '''Exceptions hide errors from the function signature and break replacing a call with its value. Functional programming puts the error into the return type: the function returns "success or error", and the error is an ordinary value.\nThere are four levels: null (one obvious reason); Result (the error is a Throwable, the root class of every error, and runCatching wraps everything, bugs included); a custom error type as a sealed interface (it lists every business error, and a when without else makes you handle a new one); and Either (an "error or result" type) from the Arrow library.\nBusiness errors become values; bugs and unrecoverable errors stay exceptions, so they show up and get fixed.''')
    a(C + '.goal.g1', '''Đã thấy lỗi rẽ sang đường lỗi''', '''Saw an error turn onto the error track''')
    a(C + '.goal.g2', '''Đã thấy lỗi mới được xử lý thế nào''', '''Saw how a new error is handled''')
    a(C + '.sim.fp.errors', '''ngoại lệ, null, Result hay kiểu lỗi riêng''', '''exceptions, null, Result or a custom error type''')

    S_ = 'hook'
    a(C + '.sec.%s.title' % S_, '''Đoán trước khi đọc''', '''Predict before reading''')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'predict', '''Hàm `fun book(raw: String, slotId: String): Booking` có thể hỏng theo những cách nào? Chỉ nhìn chữ ký, bạn trả lời được không? Còn nếu chữ ký là `Outcome<BookingError, Booking>` thì sao?''',
      '''In what ways can `fun book(raw: String, slotId: String): Booking` fail? Can you tell from the signature alone? And what if the signature were `Outcome<BookingError, Booking>`?''')
    B(C, S_, 1, 'ans', '''Với chữ ký trả Booking thì không biết: phải đọc thân hàm và mọi hàm nó gọi. Với Outcome<BookingError, Booking>, mở BookingError ra là thấy đủ: số điện thoại sai, giờ đã có người đặt, hết lượt. Mô phỏng ngay dưới chạy cùng một quy trình đặt lịch viết theo bốn cách.''',
      '''With a signature returning Booking you cannot tell: you must read the body and every function it calls. With Outcome<BookingError, Booking>, opening BookingError shows the full list: a bad phone number, a taken slot, no bookings left. The simulation just below runs one booking flow written four ways.''')

    S_ = 'why'
    a(C + '.sec.%s.title' % S_, '''Ngoại lệ có gì không ổn''', '''What is wrong with exceptions''')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'p', '''Ở chương "Hàm thuần và referential transparency", ta thay một lời gọi bằng giá trị của nó mà chương trình không đổi nghĩa. Ngoại lệ phá điều này: `throw` không có giá trị nào để thay vào, và ý nghĩa của nó tùy vào khối try nào bao quanh. Marco Vermeulen và cộng sự minh họa bằng một dòng ném: đặt trong một try có catch trả 43 thì hàm trả 43; đặt ngoài try thì chương trình dừng. Cùng một dòng, hai nghĩa khác nhau. [[src:book-fp-manning]]''',
      '''In the chapter "Pure functions and referential transparency", we replaced a call with its value without changing what the program means. Exceptions break this: `throw` has no value to put in its place, and what it means depends on which try surrounds it. Marco Vermeulen and co-authors show this with one throwing line: inside a try whose catch returns 43, the function returns 43; outside any try, the program stops. The same line, two meanings. [[src:book-fp-manning]]''')
    B(C, S_, 2, 'p', '''Vấn đề thứ hai: ngoại lệ không hiện trong kiểu. Kotlin không có checked exception (loại ngoại lệ Java buộc khai báo trong chữ ký), nên `book(...): Booking` trông y như một hàm không bao giờ hỏng. Nơi gọi chỉ biết khi đọc mã, hoặc khi app crash. Cách chữa chung của lập trình hàm: đưa lỗi vào kiểu trả về, biến nó thành một giá trị bình thường mà nơi gọi phải xử lý. [[src:book-fp-manning]] [[src:book-fp-tut]] [[src:kt-exceptions-lang]]''',
      '''The second problem: exceptions do not show up in the type. Kotlin has no checked exceptions (the kind Java makes you declare in the signature), so `book(...): Booking` looks exactly like a function that never fails. Callers only find out by reading the code, or when the app crashes. The general functional cure: put the error into the return type, turning it into an ordinary value that callers must handle. [[src:book-fp-manning]] [[src:book-fp-tut]] [[src:kt-exceptions-lang]]''')
    B(C, S_, 3, 'note', '''Không phải lỗi nào cũng nên thành giá trị. Hãy chia làm hai loại. Lỗi nghiệp vụ là những gì bạn dự tính được và người dùng có thể làm gì đó: giờ đã có người đặt, số điện thoại sai. Chúng nên là giá trị. Bug (NullPointerException, chỉ số vượt mảng) và lỗi không cứu được (hết RAM) vẫn để là ngoại lệ: chúng cần lộ ra để được sửa. Uberto Barbini cũng chỉ dùng ngoại lệ cho những tình huống không thể phục hồi. [[src:book-barbini]]''',
      '''Not every error should become a value. Split them in two. Business errors are the ones you can foresee and the user can act on: the slot is taken, the phone number is wrong. They should be values. Bugs (NullPointerException, an index out of bounds) and unrecoverable errors (running out of memory) stay exceptions: they must show up to be fixed. Uberto Barbini also keeps exceptions only for situations that cannot be recovered from. [[src:book-barbini]]''')
    B(C, S_, 3, 'kind', 'mechanism')

    S_ = 'ladder'
    a(C + '.sec.%s.title' % S_, '''Bốn cách nói "hàm này có thể hỏng"''', '''Four ways to say "this function can fail"''')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'p', '''Kiểu nullable (T?) là cách nhẹ nhất: trả null khi hỏng. Nó hợp khi chỉ có một lý do và lý do đó hiển nhiên, như "không tìm thấy". Khi có nhiều lý do, null gộp chúng làm một, và màn hình không biết phải nói gì với người dùng. [[src:book-barbini]]''',
      '''A nullable type (T?) is the lightest option: return null on failure. It fits when there is a single, obvious reason, such as "not found". With several reasons, null merges them into one, and the screen does not know what to tell the user. [[src:book-barbini]]''')
    B(C, S_, 2, 'p', '''`Result<T>` của thư viện chuẩn gói hoặc một giá trị thành công, hoặc một Throwable. `runCatching { }` chạy khối và gói mọi Throwable thành thất bại; đọc kết quả bằng `fold` (truyền một hàm cho thành công và một hàm cho thất bại), `getOrElse` hay `getOrNull`. Nó có hai giới hạn. Một: phía lỗi luôn là Throwable, nên kiểu không liệt kê được các lỗi nghiệp vụ. Hai: runCatching gói cả bug lẫn CancellationException. Result hợp nhất ở ranh giới với mã ném ngoại lệ, như khi gọi một thư viện mạng. [[src:kt-result]] [[src:kt-runcatching]]''',
      '''The standard library\'s `Result<T>` wraps either a successful value or a Throwable. `runCatching { }` runs a block and wraps any Throwable as a failure; you read the result with `fold` (pass one function for success and one for failure), `getOrElse` or `getOrNull`. It has two limits. One: the failure side is always a Throwable, so the type cannot list the business errors. Two: runCatching wraps bugs and CancellationException too. Result fits best at the boundary with code that throws, such as calling a network library. [[src:kt-result]] [[src:kt-runcatching]]''')
    B(C, S_, 3, 'p', '''Kiểu lỗi riêng: khai báo các lỗi nghiệp vụ thành một sealed interface (như ở chương "Kiểu dữ liệu đại số" của track này), rồi trả về một kiểu "thành công hoặc lỗi" (cũng là một sum type: Ok hoặc Err). Khi đó chữ ký `Outcome<BookingError, Booking>` kể đủ câu chuyện, và một `when` trên BookingError không có else sẽ báo lỗi biên dịch khi ai đó thêm lỗi mới. Thư viện chuẩn chưa có kiểu này (Arrow có sẵn Either, ở mục sau), nhưng tự viết chỉ mất ba dòng: [[src:kt-sealed]]''',
      '''A custom error type: declare the business errors as a sealed interface (as in this track\'s chapter "Algebraic data types"), then return a "success or error" type (also a sum type: Ok or Err). The signature `Outcome<BookingError, Booking>` then tells the whole story, and a `when` on BookingError without else fails to compile when someone adds a new error. The standard library has no such type yet (Arrow ships Either, in the next section), but writing one takes three lines: [[src:kt-sealed]]''')
    B(C, S_, 4, 'kt', '''sealed interface Outcome<out E, out T>
data class Ok<out T>(val value: T) : Outcome<Nothing, T>
data class Err<out E>(val error: E) : Outcome<E, Nothing>''')

    S_ = 'chain'
    a(C + '.sec.%s.title' % S_, '''Nối các bước: dừng ở lỗi đầu tiên''', '''Chaining steps: stop at the first error''')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'p', '''Quy trình đặt lịch có bốn bước, bước nào cũng có thể hỏng. Cách viết đơn giản nhất trong Kotlin thuần là trả về sớm: `val phone = parsePhone(raw) ?: return Err(BookingError.InvalidPhone)`. Bước hỏng thì hàm dừng ngay với lỗi; không hỏng thì đi tiếp với giá trị vừa có. Hình dung hai đường ray: giá trị chạy trên đường thành công, gặp lỗi thì rẽ sang đường lỗi và chạy thẳng tới cuối, bỏ qua các bước còn lại.''',
      '''The booking flow has four steps, and any of them can fail. The simplest way to write it in plain Kotlin is an early return: `val phone = parsePhone(raw) ?: return Err(BookingError.InvalidPhone)`. If the step fails, the function stops at once with the error; if not, it carries on with the value it just got. Picture two railway tracks: the value runs on the success track, and on an error it switches to the error track and runs straight to the end, skipping the remaining steps.''')
    B(C, S_, 2, 'p', '''Massimo Carli gọi chiến lược này là fail fast (dừng sớm). Nó hợp khi bước sau cần kết quả của bước trước. Khi các bước độc lập với nhau, như kiểm từng ô của một form, bạn lại muốn gom MỌI lỗi để báo một lần; đó là chủ đề của chương "Validate gom lỗi: applicative và monoid" trong track này. Còn cách nối các bước mà không phải viết return ở mỗi dòng là chủ đề của chương kế tiếp, "map và flatMap: functor và monad qua ví dụ". [[src:book-fp-tut]]''',
      '''Massimo Carli calls this strategy fail fast. It fits when a later step needs the result of an earlier one. When the steps are independent, like checking each field of a form, you want to collect EVERY error and report them at once instead; that is the topic of this track\'s chapter "Validation that collects errors: applicatives and monoids". Chaining steps without writing return on every line is the topic of the next chapter, "map and flatMap: functors and monads by example". [[src:book-fp-tut]]''')
    B(C, S_, 3, 'p', '''Ở tầng giao diện, chỉ cần đổi kết quả thành trạng thái màn hình ở một chỗ: thành công thì Success, lỗi thì một trạng thái lỗi kèm câu báo đúng cho từng BookingError. Carli làm đúng vậy với Result trong một ViewModel: dùng fold để chọn trạng thái theo thành công hay thất bại. [[src:book-fp-tut]]''',
      '''In the UI layer you only need to turn the result into a screen state in one place: Success on success, an error state with the right message for each BookingError on failure. Carli does exactly this with Result in a ViewModel: fold picks the state for success or failure. [[src:book-fp-tut]]''')

    S_ = 'arrow'
    a(C + '.sec.%s.title' % S_, '''Arrow: Either và khối either { }''', '''Arrow: Either and the either { } block''')
    a(C + '.sec.%s.badge' % S_, 'version')
    B(C, S_, 1, 'p', '''Arrow là một thư viện bên ngoài, không thuộc Kotlin; site đọc tài liệu của bản 2.3.0. Kiểu `Either<E, A>` của nó giống Outcome ở trên: Left chứa lỗi, Right chứa kết quả. Arrow còn có khối `either { }`: bên trong, `ensure(điều kiện) { lỗi }` và `ensureNotNull(giá trị) { lỗi }` dừng khối với lỗi đó khi điều kiện sai, `.bind()` lấy giá trị từ một Either khác hoặc dừng với lỗi của nó, và `raise(lỗi)` dừng ngay. Cùng quy trình đặt lịch viết lại: [[src:arrow-typed-errors]]''',
      '''Arrow is an external library, not part of Kotlin; the site read the docs for version 2.3.0. Its `Either<E, A>` type is like Outcome above: Left holds the error, Right holds the result. Arrow also has the `either { }` block: inside it, `ensure(condition) { error }` and `ensureNotNull(value) { error }` stop the block with that error when the condition fails, `.bind()` takes the value out of another Either or stops with its error, and `raise(error)` stops at once. The same booking flow rewritten: [[src:arrow-typed-errors]]''')
    B(C, S_, 2, 'kt', '''fun book(raw: String, slotId: String): Either<BookingError, Booking> = either {
    val phone = ensureNotNull(parsePhone(raw)) { BookingError.InvalidPhone }
    val slot = ensureNotNull(findFreeSlot(slotId)) { BookingError.SlotTaken(slotId) }
    ensure(quotaLeft(phone)) { BookingError.QuotaExceeded }
    save(phone, slot)
}''')
    B(C, S_, 3, 'p', '''Đọc kết quả bằng `fold`, `getOrElse`, hoặc `when` với hai nhánh Left và Right. Khi phải gọi mã ném ngoại lệ, tài liệu Arrow hướng dẫn dùng `catch` để đổi đúng loại ngoại lệ bạn mong đợi thành lỗi có kiểu; theo tài liệu, `catch` tự bỏ qua các lỗi nghiêm trọng như OutOfMemoryError và CancellationException. Ý tưởng không cần Arrow: bản Kotlin thuần ở mục trước làm đúng việc đó, chỉ dài hơn vài dòng. [[src:arrow-typed-errors]]''',
      '''Read the result with `fold`, `getOrElse`, or a `when` with Left and Right branches. When you must call code that throws, the Arrow docs show using `catch` to turn exactly the exception type you expect into a typed error; according to the docs, `catch` skips fatal errors such as OutOfMemoryError and CancellationException on its own. The idea does not need Arrow: the plain Kotlin version in the previous section does the same job, just a few lines longer. [[src:arrow-typed-errors]]''')

    S_ = 'bugs'
    a(C + '.sec.%s.title' % S_, '''Hai lỗi hay gặp''', '''Two common bugs''')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'bug', '''Mọi người dùng mới đều thấy "Đặt lịch thất bại", nhưng không có báo cáo crash nào.''', '''Every new user sees "Booking failed", yet there is not a single crash report.''')
    B(C, S_, 1, 'cause', '''Hàm kiểm lượt viết quotas[phone]!!, nên ném NullPointerException với số chưa có trong bảng. Màn hình bọc lời gọi bằng catch (e: Exception) hoặc runCatching, nên bug bị gói thành "thất bại" như một lỗi nghiệp vụ.''',
      '''The quota check writes quotas[phone]!!, so it throws NullPointerException for a number not yet in the table. The screen wraps the call in catch (e: Exception) or runCatching, so the bug is wrapped as "failed" like a business error.''')
    B(C, S_, 1, 'fix', '''Đổi lỗi nghiệp vụ thành giá trị có kiểu (BookingError) và bỏ catch chung, để bug lộ ra khi test. Sửa bug: số mới mặc định còn đủ lượt, ví dụ quotas[phone] ?: WEEKLY_LIMIT.''',
      '''Turn business errors into typed values (BookingError) and drop the catch-all, so the bug shows up in testing. Fix the bug: a new number starts with the full quota, for example quotas[phone] ?: WEEKLY_LIMIT.''')
    B(C, S_, 2, 'bug', '''Phòng khám thêm quy định "tối đa 2 lịch mỗi tuần", nhưng người vượt giới hạn chỉ thấy "Đặt lịch thất bại" chung chung.''', '''The clinic adds a "at most 2 bookings a week" rule, but users over the limit only see a vague "Booking failed".''')
    B(C, S_, 2, 'cause', '''Lỗi mới được thêm thành một ngoại lệ (hoặc thêm một chỗ trả null). Không gì buộc màn hình xử lý nó, nên nó rơi vào nhánh chung.''',
      '''The new error was added as an exception (or one more place returning null). Nothing forces the screen to handle it, so it falls into the generic branch.''')
    B(C, S_, 2, 'fix', '''Thêm QuotaExceeded vào BookingError. when không có else sẽ chỉ ra đúng chỗ cần viết câu báo mới.''',
      '''Add QuotaExceeded to BookingError. A when without else points at exactly the place that needs the new message.''')

    S_ = 'ex'
    a(C + '.sec.%s.title' % S_, '''Bài tập''', '''Exercise''')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'ex', '''Hàm hủy lịch dưới đây ném ngoại lệ ở ba chỗ. Viết lại để nó trả về `Outcome<CancelError, Unit>` (hoặc Either nếu bạn dùng Arrow), với CancelError là một sealed interface gồm ba lỗi. Rồi viết hàm đổi CancelError thành câu báo cho màn hình, bằng một when không có else.''',
      '''The cancel function below throws in three places. Rewrite it to return `Outcome<CancelError, Unit>` (or Either if you use Arrow), with CancelError a sealed interface of three errors. Then write the function that turns a CancelError into the screen message, using a when without else.''')
    B(C, S_, 1, 'exkt', '''fun cancel(bookingId: Long, now: LocalDateTime) {
    val b = repo.find(bookingId) ?: throw NoSuchElementException("Không có lịch $bookingId")
    if (b.cancelled) throw IllegalStateException("Lịch đã hủy")
    if (Duration.between(now, b.time).toHours() < 2) throw IllegalStateException("Quá sát giờ khám")
    repo.markCancelled(bookingId)
}''', '''fun cancel(bookingId: Long, now: LocalDateTime) {
    val b = repo.find(bookingId) ?: throw NoSuchElementException("No booking $bookingId")
    if (b.cancelled) throw IllegalStateException("Already cancelled")
    if (Duration.between(now, b.time).toHours() < 2) throw IllegalStateException("Too close to the visit")
    repo.markCancelled(bookingId)
}''')
    B(C, S_, 1, 'hint', '''Mỗi throw là một lỗi nghiệp vụ: đặt tên cho nó (NotFound, AlreadyCancelled, TooLate). Thay throw bằng return Err(...); dòng cuối trả Ok(Unit).''',
      '''Each throw is a business error: give it a name (NotFound, AlreadyCancelled, TooLate). Replace throw with return Err(...); the last line returns Ok(Unit).''')
    B(C, S_, 1, 'sol', '''Ba lỗi giờ nằm trong kiểu, nên màn hình biết đủ ba câu cần nói, và thêm lỗi thứ tư thì when báo thiếu nhánh. Nếu repo.find hay repo.markCancelled ném IOException (mất kết nối), đó là lỗi hạ tầng chứ không phải lỗi nghiệp vụ của hủy lịch: để nó đi lên, hoặc đổi riêng nó thành một lỗi có tên ở tầng dữ liệu.''',
      '''The three errors are now in the type, so the screen knows all three messages, and adding a fourth error makes the when report a missing branch. If repo.find or repo.markCancelled throws IOException (a lost connection), that is an infrastructure error, not a business error of cancelling: let it travel up, or turn just that one into a named error in the data layer.''')
    B(C, S_, 1, 'solkt', '''sealed interface CancelError {
    data class NotFound(val id: Long) : CancelError
    data object AlreadyCancelled : CancelError
    data object TooLate : CancelError
}

fun cancel(bookingId: Long, now: LocalDateTime): Outcome<CancelError, Unit> {
    val b = repo.find(bookingId) ?: return Err(CancelError.NotFound(bookingId))
    if (b.cancelled) return Err(CancelError.AlreadyCancelled)
    if (Duration.between(now, b.time).toHours() < 2) return Err(CancelError.TooLate)
    repo.markCancelled(bookingId)
    return Ok(Unit)
}

fun message(e: CancelError): String = when (e) {
    is CancelError.NotFound -> "Không tìm thấy lịch ${e.id}"
    CancelError.AlreadyCancelled -> "Lịch này đã hủy rồi"
    CancelError.TooLate -> "Chỉ hủy được trước giờ khám 2 tiếng"
}''', '''sealed interface CancelError {
    data class NotFound(val id: Long) : CancelError
    data object AlreadyCancelled : CancelError
    data object TooLate : CancelError
}

fun cancel(bookingId: Long, now: LocalDateTime): Outcome<CancelError, Unit> {
    val b = repo.find(bookingId) ?: return Err(CancelError.NotFound(bookingId))
    if (b.cancelled) return Err(CancelError.AlreadyCancelled)
    if (Duration.between(now, b.time).toHours() < 2) return Err(CancelError.TooLate)
    repo.markCancelled(bookingId)
    return Ok(Unit)
}

fun message(e: CancelError): String = when (e) {
    is CancelError.NotFound -> "Booking ${e.id} not found"
    CancelError.AlreadyCancelled -> "This booking is already cancelled"
    CancelError.TooLate -> "You can only cancel 2 hours before the visit"
}''')

    S_ = 'recall'
    a(C + '.sec.%s.title' % S_, '''Tự trả lời''', '''Answer it yourself''')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'ask', '''Lỗi nào nên thành giá trị, lỗi nào nên để là ngoại lệ?''', '''Which errors should become values, and which should stay exceptions?''')
    B(C, S_, 1, 'ans', '''Lỗi nghiệp vụ dự tính trước (giờ đã có người đặt, hết lượt) thành giá trị có kiểu, để nơi gọi buộc phải xử lý. Bug và lỗi không cứu được để là ngoại lệ, để chúng lộ ra và được sửa.''',
      '''Expected business errors (the slot is taken, no bookings left) become typed values, so callers must handle them. Bugs and unrecoverable errors stay exceptions, so they show up and get fixed.''')
    B(C, S_, 2, 'ask', '''Vì sao runCatching không thay được một kiểu lỗi riêng?''', '''Why can runCatching not replace a custom error type?''')
    B(C, S_, 2, 'ans', '''Phía lỗi của Result là Throwable, nên kiểu không liệt kê được các lỗi nghiệp vụ; và runCatching bắt mọi Throwable, gói cả bug lẫn CancellationException.''',
      '''The failure side of Result is a Throwable, so the type cannot list the business errors; and runCatching catches every Throwable, wrapping bugs and CancellationException too.''')

    for q, qv, qe, av, ae, wv, we in [
        ('q1', 'Kotlin có buộc khai báo ngoại lệ trong chữ ký hàm không?', 'Does Kotlin make you declare exceptions in a function signature?', 'Không.', 'No.',
         'Kotlin không có checked exception, nên chữ ký không cho biết hàm có thể ném gì.', 'Kotlin has no checked exceptions, so the signature does not say what a function may throw.'),
        ('q2', '`runCatching { error("x") }` trả về gì?', 'What does `runCatching { error("x") }` return?', 'Một Result thất bại chứa IllegalStateException.', 'A failed Result holding an IllegalStateException.',
         'error() ném IllegalStateException, và runCatching gói mọi Throwable ném ra trong khối thành thất bại.', 'error() throws IllegalStateException, and runCatching wraps any Throwable thrown in the block as a failure.'),
        ('q3', 'kotlin.Result có hàm flatMap không?', 'Does kotlin.Result have a flatMap function?', 'Không.', 'No.',
         'Result có map, mapCatching, recover, fold, getOrElse…, nhưng không có flatMap.', 'Result has map, mapCatching, recover, fold, getOrElse… but no flatMap.'),
        ('q4', 'Thêm một kiểu con vào sealed BookingError thì chỗ nào báo lỗi biên dịch?', 'Adding a subtype to the sealed BookingError makes which places fail to compile?', 'Mọi when dạng biểu thức trên BookingError không có else.', 'Every when expression on BookingError without else.',
         'when dạng biểu thức trên sealed type phải phủ đủ mọi kiểu con.', 'A when expression on a sealed type must cover every subtype.')]:
        a(C + '.quiz.%s.q' % q, qv, qe); a(C + '.quiz.%s.a' % q, av, ae); a(C + '.quiz.%s.why' % q, wv, we)
