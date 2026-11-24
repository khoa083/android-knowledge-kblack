# Kiến trúc · G8: lỗi qua các tầng (Phần 2)
# Nguồn: developer.android.com Data layer (Expose errors), UI layer (Show errors on the screen) (đọc 2026-11-24);
# Boudjnah, Clean Architecture for Android ch.6 Failures and Exceptions (đọc từ epub trong kho). Nối Kotlin K6, Coroutines A5.
# Trần: 8 mục, mục cơ chế ≤ 4 khối.

SEC_ORDER = {'g8': ['hook', 'classify', 'map', 'show', 'bugs', 'ex', 'recall', 'honest']}


def add(a):
    def B(ch, sec, n, field, vi, en=None):
        a('%s.sec.%s.b.%02d.%s' % (ch, sec, n, field), vi, vi if en is None else en)

    m = lambda k, vi, en=None: a('m.failure.' + k, vi, en)
    m('title', 'Khi đặt lịch thất bại: lỗi đi từ mạng tới màn hình', 'When booking fails: errors travel from the network to the screen')
    m('overview', 'Đặt lịch có thể hỏng theo nhiều cách: mất mạng (IOException), giờ vừa có người đặt (HTTP 409), máy chủ lỗi (HTTP 500), người dùng rời màn hình (CancellationException), hay lỗi lập trình (NullPointerException). Ba cách xử lý: (1) để nguyên ngoại lệ đi lên, rồi "sửa" bằng cách bắt tất cả và hiện message; (2) repository đổi lỗi dự đoán được thành failure có nghĩa; (3) repository bắt Exception rộng và trả giá trị rỗng.',
      'Booking can fail in many ways: offline (IOException), the slot was just taken (HTTP 409), a server error (HTTP 500), the user leaving the screen (CancellationException), or a programming error (NullPointerException). Three ways to handle it: (1) let exceptions travel up untouched, then "fix" it by catching everything and showing the message; (2) the repository turns expected errors into meaningful failures; (3) the repository catches Exception broadly and returns empty values.')
    m('wrapup', 'Lỗi dự đoán được (mất mạng, giờ đã kín, máy chủ bận) là failure: tầng data bắt đúng loại, đổi thành một giá trị có tên, và UI hiện một câu người dùng hiểu kèm cách xử lý. Lỗi bất ngờ (lỗi lập trình) là exception: không nuốt, để crash report ghi lại và sửa mã. Bắt rộng mọi Exception thì vừa giấu lỗi, vừa nuốt cả việc hủy coroutine.',
      'Expected errors (offline, slot taken, server busy) are failures: the data layer catches the specific types, turns them into named values, and the UI shows a sentence the user understands with a way forward. Unexpected errors (programming bugs) are exceptions: do not swallow them, let crash reporting record them and fix the code. Catching every Exception hides errors and swallows coroutine cancellation too.')
    m('simp.1', 'Năm loại lỗi đại diện; mã HTTP lấy từ HttpException của Retrofit như một ví dụ, thư viện mạng khác có cách báo khác.', 'Five representative errors; the HTTP code comes from Retrofit\'s HttpException as an example, other network libraries report it differently.')
    m('ctl.hint', 'Đổi cách xử lý rồi đi lại bốn bước; xem tab "Bảng ánh xạ lỗi".', 'Switch the handling approach and walk the four steps again; watch the "Error mapping" tab.')
    m('ctl.case', 'Cách xử lý lỗi', 'How errors are handled')
    for k, vi, en in [('raw', 'để nguyên, rồi bắt tất cả', 'untouched, then catch everything'), ('mapped', 'đổi thành failure ở repository', 'mapped to failures in the repository'), ('swallow', 'bắt Exception rộng, trả rỗng', 'catch Exception broadly, return empty')]:
        m('ctl.case.' + k, vi, en)
    m('diagramTitle', 'Màn hình, ViewModel, repository, nguồn mạng', 'Screen, ViewModel, repository, network source')
    m('diagramDesc', 'Ngoại lệ sinh ở nguồn mạng và đi ngược lên từng tầng', 'Exceptions start at the network source and travel back up layer by layer')
    for k, vi, en in [('ui', 'Màn Đặt lịch', 'Booking screen'), ('vm', 'BookingViewModel', 'BookingViewModel'), ('repo', 'SlotRepository', 'SlotRepository'), ('source', 'Nguồn mạng (API)', 'Network source (API)')]:
        m('n.' + k, vi, en)
    m('met.crash', 'App crash', 'App crashes'); m('met.text', 'Lộ chữ kỹ thuật', 'Technical text shown'); m('met.hidden', 'Lỗi bị giấu', 'Error hidden')
    for k, vi, en in [('yes', 'có', 'yes'), ('no', 'không', 'no'), ('report', 'không crash vì failure; lỗi lập trình vào crash report', 'no crash from failures; bugs go to crash reports')]:
        m('crash.' + k, vi, en)
    for k, vi, en in [('yes', 'có', 'yes'), ('no', 'không', 'no')]:
        m('yn.' + k, vi, en)
    a('cap.failure', 'Từ trái sang phải: màn hình, ViewModel, repository, nguồn mạng. Hạt đỏ chạy ngược là ngoại lệ đi lên; hạt vàng là giá trị (failure) đi lên. Khối viền đỏ là chỗ lỗi gây hại: crash, lộ chữ kỹ thuật hay bị giấu.',
      'Left to right: screen, ViewModel, repository, network source. Red dots moving back are exceptions going up; yellow dots are values (failures) going up. A red-outlined box is where the error does harm: a crash, technical text, or a hidden error.')
    S = [
        ('raw', 's1', 'Mất mạng: IOException không ai bắt, app crash', 'Offline: nobody catches the IOException, the app crashes',
         'api.book ném IOException. Repository ném tiếp, ViewModel gọi trong viewModelScope.launch mà không bắt. Ngoại lệ chưa xử lý trong coroutine làm app crash.',
         'api.book throws an IOException. The repository rethrows, the ViewModel calls it in viewModelScope.launch without catching. An unhandled exception in the coroutine crashes the app.'),
        ('raw', 's2', '"Sửa" vội: bắt tất cả, hiện e.message', 'A hasty "fix": catch everything, show e.message',
         'ViewModel bọc catch (e: Exception) và đưa e.message vào UI state. Máy chủ lỗi 500: người dùng thấy "HTTP 500 Internal Server Error".',
         'The ViewModel wraps catch (e: Exception) and puts e.message into UI state. The server returns 500: the user sees "HTTP 500 Internal Server Error".'),
        ('raw', 's3', 'Giờ đã kín: người dùng thấy "HTTP 409 Conflict"', 'Slot taken: the user sees "HTTP 409 Conflict"',
         'Máy chủ trả 409 vì giờ vừa có người đặt. Thông báo đúng về mặt kỹ thuật nhưng người dùng không biết phải làm gì: chọn giờ khác.',
         'The server returns 409 because the slot was just taken. The message is technically correct, but the user does not know what to do: pick another slot.'),
        ('raw', 's4', 'Lỗi lập trình cũng bị bắt và hiện "null"', 'A programming error is caught too and shows "null"',
         'Một NullPointerException do bug cũng rơi vào catch, hiện chữ "null". App không crash nên không có crash report: lỗi lập trình bị giấu.',
         'A NullPointerException from a bug also lands in the catch and shows "null". The app does not crash, so there is no crash report: the bug is hidden.'),
        ('mapped', 's1', 'Mất mạng: repository đổi thành Offline', 'Offline: the repository maps it to Offline',
         'Repository bắt đúng IOException và trả BookResult.Failed(BookingFailure.Offline). Lên tới ViewModel chỉ còn một giá trị có tên, không còn ngoại lệ.',
         'The repository catches exactly IOException and returns BookResult.Failed(BookingFailure.Offline). By the ViewModel there is only a named value, no exception.'),
        ('mapped', 's2', 'Giờ đã kín: SlotTaken, câu người dùng hiểu', 'Slot taken: SlotTaken, a sentence the user understands',
         'HTTP 409 thành SlotTaken. ViewModel đổi failure thành câu "Giờ này vừa có người đặt, chọn giờ khác nhé" từ tài nguyên chuỗi.',
         'HTTP 409 becomes SlotTaken. The ViewModel turns the failure into "This slot was just taken, please pick another" from a string resource.'),
        ('mapped', 's3', 'Máy chủ lỗi: ServerProblem, kèm Thử lại', 'Server error: ServerProblem, with Retry',
         'HTTP 500 thành ServerProblem; màn hình hiện "Phòng khám đang bận, thử lại sau" và nút Thử lại.',
         'HTTP 500 becomes ServerProblem; the screen shows "The clinic is busy, try again later" and a Retry button.'),
        ('mapped', 's4', 'Lỗi lập trình: không bắt, để crash report ghi lại', 'Programming error: not caught, crash reporting records it',
         'NullPointerException không thuộc loại repository biết xử lý, nên không bị bắt. App báo lỗi qua crash report để sửa mã, thay vì giả vờ chạy tiếp ở trạng thái không biết.',
         'A NullPointerException is not a type the repository knows how to handle, so it is not caught. It surfaces in crash reports so the code gets fixed, instead of pretending to continue in an unknown state.'),
        ('swallow', 's1', 'Mất mạng thành "Chưa có giờ trống"', 'Offline becomes "No free slots"',
         'slots() bắt mọi Exception và trả emptyList(). Màn hình hiện "Chưa có giờ trống" trong khi thật ra là mất mạng; người dùng bỏ đi.',
         'slots() catches every Exception and returns emptyList(). The screen says "No free slots" when the real problem is being offline; the user gives up.'),
        ('swallow', 's2', 'Mọi lỗi đặt lịch thành "Có lỗi xảy ra"', 'Every booking error becomes "Something went wrong"',
         'book() trả false cho mọi lỗi. Giờ đã kín, mất mạng, máy chủ bận đều thành một câu chung; người dùng không biết nên thử lại hay chọn giờ khác.',
         'book() returns false for every error. Slot taken, offline, server busy all become one generic sentence; the user cannot tell whether to retry or pick another slot.'),
        ('swallow', 's3', 'Rời màn hình: cả việc hủy coroutine cũng bị nuốt', 'Leaving the screen: even coroutine cancellation is swallowed',
         'Người dùng rời màn khi đang đặt; viewModelScope bị hủy và CancellationException được ném ở điểm suspend. catch (e: Exception) bắt luôn nó, nên mã sau đó chạy tiếp như chưa bị hủy.',
         'The user leaves mid-booking; viewModelScope is cancelled and CancellationException is thrown at the suspension point. catch (e: Exception) catches it too, so the code after it keeps running as if nothing was cancelled.'),
        ('swallow', 's4', 'Lỗi lập trình biến mất không dấu vết', 'A programming error vanishes without a trace',
         'NullPointerException trong api.slots bị nuốt thành danh sách rỗng. Không crash, không log, không crash report: bug sống mãi.',
         'A NullPointerException inside api.slots is swallowed into an empty list. No crash, no log, no crash report: the bug lives forever.'),
    ]
    for case, k, tv, te, xv, xe in S:
        sid = case + '.' + k
        m('s.%s.title' % sid, tv, te); m('s.%s.explain' % sid, xv, xe); m('ev.' + sid, tv, te)
    for k, vi, en in [
        ('try', 'Đi bốn bước của từng cách; so cột "Người dùng thấy" trong bảng ánh xạ.', 'Walk the four steps of each approach; compare the "User sees" column in the mapping table.'),
        ('raw.s2', 'UI layer: lỗi trên màn hình thường cần kèm thông điệp cho người dùng và một hành động như thử lại; e.message của thư viện mạng không phải thông điệp đó. [[src:ax-ui-layer]]', 'UI layer: errors on screen usually need a message for the user and an action such as retry; a network library\'s e.message is not that message. [[src:ax-ui-layer]]'),
        ('raw.s3', 'Data layer: tầng data hiểu các loại lỗi và có thể lộ chúng bằng ngoại lệ riêng hay một kiểu Result, để UI biết những lỗi đã biết trước. [[src:ax-data-layer]]', 'Data layer: the data layer understands the kinds of errors and can expose them with custom exceptions or a Result type, so the UI knows the expected errors. [[src:ax-data-layer]]'),
        ('raw.s4', 'Boudjnah: exception là cờ đỏ, có thể do bug; cần ghi log và theo dõi, mục tiêu là càng ít càng tốt. Giấu nó là ngược lại. [[src:book-boudjnah]]', 'Boudjnah: exceptions are red flags, possibly bugs; they should be logged and monitored, with the goal of having as few as possible. Hiding them does the opposite. [[src:book-boudjnah]]'),
        ('mapped.s2', 'Boudjnah: failure là chuyện dự đoán được và phục hồi được, xử lý như giá trị bình thường; sealed class tốt hơn Boolean vì đặt tên rõ và mở rộng được. [[src:book-boudjnah]]', 'Boudjnah: failures are expected and recoverable, handled as normal values; a sealed class beats a Boolean because it names each case and scales. [[src:book-boudjnah]]'),
        ('mapped.s3', 'Hiện lỗi kèm hành động thử lại là đúng ví dụ trong mục Show errors on the screen. [[src:ax-ui-layer]]', 'Showing the error with a retry action matches the example in Show errors on the screen. [[src:ax-ui-layer]]'),
        ('mapped.s4', 'Một khi ta biết một tình huống có thể xảy ra và biết cách xử lý, nó thôi là exception mà thành failure (Boudjnah). NPE ở đây chưa phải loại đó: nó là bug cần sửa. [[src:book-boudjnah]]', 'Once we know a scenario can happen and how to handle it, it stops being an exception and becomes a failure (Boudjnah). The NPE here is not that: it is a bug to fix. [[src:book-boudjnah]]'),
        ('swallow.s2', 'Boolean không nói được "thất bại vì sao": Boudjnah dùng đúng ví dụ này để chọn sealed class. [[src:book-boudjnah]]', 'A Boolean cannot say why something failed: Boudjnah uses exactly this example to choose a sealed class. [[src:book-boudjnah]]'),
        ('swallow.s3', 'CancellationException là một Exception, nên catch (e: Exception) bắt luôn nó. Track Coroutines (A5) và Kotlin (K6) giải thích vì sao phải để nó đi tiếp.', 'CancellationException is an Exception, so catch (e: Exception) catches it too. The Coroutines (A5) and Kotlin (K6) tracks explain why it must be let through.'),
        ('swallow.s4', 'Bắt đúng loại lỗi dự đoán được (IOException, HttpException) thay vì Exception; mọi thứ khác để đi lên.', 'Catch the specific expected types (IOException, HttpException) instead of Exception; let everything else go up.')]:
        m('co.' + k, vi, en)
    a('preset.failure', 'Kiến trúc · lỗi qua các tầng: crash, chữ kỹ thuật, lỗi bị giấu', 'Architecture · errors across layers: crashes, technical text, hidden errors')

    z = lambda k, vi, en=None: a('vz.' + k, vi, en)
    z('tab.fl', 'Bảng ánh xạ lỗi', 'Error mapping')
    z('fl.cap', 'Mỗi hàng là một loại lỗi sinh ở nguồn mạng; các cột cho biết mỗi tầng làm gì với nó và cuối cùng người dùng thấy gì. Hàng của bước đang xem được viền.', 'Each row is an error raised at the network source; the columns show what each layer does with it and what the user finally sees. The current step\'s row is outlined.')
    z('fl.legend', 'Ô đỏ: crash, chữ kỹ thuật, hay lỗi bị giấu. Ô mờ: chưa tới bước đó.', 'Red cell: a crash, technical text, or a hidden error. Faded cell: that step has not come yet.')
    for k, vi, en in [('src', 'Lỗi ở nguồn mạng', 'Error at the network source'), ('repo', 'Repository', 'Repository'), ('vm', 'ViewModel', 'ViewModel'), ('user', 'Người dùng thấy', 'User sees')]:
        z('fl.col.' + k, vi, en)
    for k, vi, en in [('io', 'IOException (mất mạng)', 'IOException (offline)'), ('conflict', 'HTTP 409 (giờ đã kín)', 'HTTP 409 (slot taken)'), ('server', 'HTTP 500 (máy chủ lỗi)', 'HTTP 500 (server error)'),
                      ('cancel', 'CancellationException (rời màn)', 'CancellationException (left the screen)'), ('bug', 'NullPointerException (bug)', 'NullPointerException (a bug)')]:
        z('fl.row.' + k, vi, en)
    for k, vi, en in [
        ('rethrow', 'ném tiếp', 'rethrows'), ('noCatch', 'không bắt', 'does not catch'), ('crash', 'app crash', 'the app crashes'),
        ('catchAllMsg', 'bắt Exception, lấy e.message', 'catches Exception, takes e.message'), ('http500', '"HTTP 500 Internal Server Error"', '"HTTP 500 Internal Server Error" text'),
        ('http409', '"HTTP 409 Conflict"', '"HTTP 409 Conflict" text'), ('nullText', '"null"', 'the text "null"'),
        ('toOffline', 'đổi thành Offline', 'maps to Offline'), ('toTaken', 'đổi thành SlotTaken', 'maps to SlotTaken'), ('toServer', 'đổi thành ServerProblem', 'maps to ServerProblem'),
        ('msgFor', 'chọn câu theo failure', 'picks a sentence for the failure'), ('notCaught', 'không bắt (không phải lỗi dự đoán được)', 'not caught (not an expected error)'),
        ('offlineMsg', '"Không có mạng. Thử lại?"', '"No connection. Retry?"'), ('takenMsg', '"Giờ này vừa có người đặt, chọn giờ khác"', '"This slot was just taken, pick another"'),
        ('serverMsg', '"Phòng khám đang bận, thử lại sau" + Thử lại', '"The clinic is busy, try later" + Retry'), ('crashReport', 'crash, có crash report để sửa', 'a crash, with a crash report to fix'),
        ('emptyList', 'bắt Exception, trả danh sách rỗng', 'catches Exception, returns an empty list'), ('showsList', 'hiện danh sách rỗng', 'shows the empty list'), ('noSlots', '"Chưa có giờ trống"', '"No free slots"'),
        ('returnFalse', 'bắt Exception, trả false', 'catches Exception, returns false'), ('genericFail', 'chỉ biết là thất bại', 'only knows it failed'), ('genericMsg', '"Có lỗi xảy ra"', '"Something went wrong"'),
        ('caughtCancel', 'bắt cả CancellationException', 'catches CancellationException too'), ('keepsRunning', 'chạy tiếp sau khi đã bị hủy', 'keeps running after cancellation'),
        ('afterLeave', 'việc vẫn chạy sau khi đã rời màn', 'work continues after leaving'), ('silent', 'không gì cả, bug không được báo', 'nothing; the bug is never reported')]:
        z('fl.v.' + k, vi, en)

    C = 'g8'
    a(C + '.title', 'Lỗi qua các tầng', 'Errors across layers')
    a(C + '.essence', 'Mỗi tầng làm một việc với lỗi. Nguồn dữ liệu ném ngoại lệ; repository bắt đúng các loại dự đoán được và đổi thành failure có tên (Offline, SlotTaken, ServerProblem); ViewModel đổi failure thành UI state có câu cho người dùng và cách xử lý.\nFailure là chuyện dự đoán được, xử lý như giá trị. Exception là chuyện bất ngờ, như lỗi lập trình: không nuốt, để crash report ghi lại.\nĐừng bắt Exception rộng: nó giấu bug, biến lỗi thành dữ liệu sai, và nuốt cả CancellationException của coroutine.',
      'Each layer does one thing with errors. Data sources throw exceptions; the repository catches the specific expected types and turns them into named failures (Offline, SlotTaken, ServerProblem); the ViewModel turns failures into UI state with a sentence for the user and a way forward.\nFailures are expected and handled as values. Exceptions are unexpected, such as programming bugs: do not swallow them, let crash reporting record them.\nDo not catch Exception broadly: it hides bugs, turns errors into wrong data, and swallows coroutine CancellationException too.')
    a(C + '.goal.g1', 'Đã thấy app crash vì mất mạng', 'Saw the app crash when offline')
    a(C + '.goal.g2', 'Đã đi hết bốn bước', 'Walked all four steps')
    a(C + '.sim.arch.failure', 'lỗi đi từ mạng tới màn hình', 'errors from the network to the screen')

    S_ = 'hook'
    a(C + '.sec.%s.title' % S_, 'Đoán trước khi đọc', 'Predict before reading')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'predict', 'Để app không crash khi mất mạng, ai đó bọc mọi hàm của repository trong catch (e: Exception) { emptyList() }. Mất mạng lúc mở màn Chọn giờ: người dùng thấy gì? Và nếu có một NullPointerException do bug thì sao?',
      'To stop the app crashing offline, someone wraps every repository function in catch (e: Exception) { emptyList() }. Offline when opening Choose a time: what does the user see? And what if a bug throws a NullPointerException?')
    B(C, S_, 1, 'ans', 'Người dùng thấy "Chưa có giờ trống", một câu sai. NullPointerException cũng bị nuốt thành danh sách rỗng, nên không có crash report và bug không ai thấy. Mô phỏng bên dưới so cách này với việc đổi lỗi thành failure có tên. [[src:book-boudjnah]]',
      'The user sees "No free slots", which is false. The NullPointerException is swallowed into an empty list too, so there is no crash report and nobody sees the bug. The simulation below compares this with mapping errors to named failures. [[src:book-boudjnah]]')

    S_ = 'classify'
    a(C + '.sec.%s.title' % S_, 'Failure và exception', 'Failures and exceptions')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'p', 'Boudjnah chia hai loại. Failure là kết quả không thành công nhưng dự đoán được và phục hồi được: sai mật khẩu, mất mạng, giờ đã kín. Exception là chuyện bất ngờ, không có cách phục hồi rõ: truy cập mảng ngoài chỉ số, một NullPointerException. Failure xử lý duyên dáng cho người dùng; exception là cờ đỏ, có thể do bug, cần ghi log và theo dõi. Khi đã biết một tình huống có thể xảy ra và biết cách xử lý, nó thôi là exception mà thành failure. [[src:book-boudjnah]]',
      'Boudjnah splits them in two. A failure is an unsuccessful but expected, recoverable outcome: a wrong password, being offline, a taken slot. An exception is unexpected with no clear recovery: an out-of-bounds array access, a NullPointerException. Failures are handled gracefully for the user; exceptions are red flags, possibly bugs, to be logged and monitored. Once we know a scenario can happen and how to handle it, it stops being an exception and becomes a failure. [[src:book-boudjnah]]')
    B(C, S_, 2, 'p', 'Failure nên là giá trị có tên, không phải Boolean: true/false không nói được thất bại vì sao, và không mở rộng được khi cần phân biệt sai mật khẩu, mất mạng hay máy chủ bận. Sealed class hay sealed interface đặt tên rõ từng trường hợp và thêm được trường hợp mới; when trên nó buộc xử lý đủ (Kotlin K5). [[src:book-boudjnah]]',
      'A failure should be a named value, not a Boolean: true/false cannot say why something failed, and cannot grow when you need to tell a wrong password from being offline or a busy server. A sealed class or interface names each case and can gain new ones; a when over it must handle them all (Kotlin K5). [[src:book-boudjnah]]')

    S_ = 'map'
    a(C + '.sec.%s.title' % S_, 'Đổi lỗi ở đâu', 'Where errors are mapped')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'p', 'Hướng dẫn chính thức: tương tác với repository và data source có thể thành công hay ném ngoại lệ; với coroutine dùng try/catch khi phù hợp, với Flow dùng toán tử catch. Tầng data hiểu các loại lỗi và có thể lộ chúng bằng ngoại lệ riêng (ví dụ UserNotAuthenticatedException), hay trả một kiểu Result để UI biết những lỗi đã biết trước. [[src:ax-data-layer]]',
      'Official guide: interactions with repositories and data sources can succeed or throw; with coroutines use try/catch when appropriate, with Flows use the catch operator. The data layer understands the kinds of errors and can expose them with custom exceptions (for example UserNotAuthenticatedException), or return a Result type so the UI knows the expected errors. [[src:ax-data-layer]]')
    B(C, S_, 2, 'kt', 'sealed interface BookingFailure {\n    data object Offline : BookingFailure\n    data object SlotTaken : BookingFailure\n    data object ServerProblem : BookingFailure\n}\nsuspend fun book(s: Slot): BookResult = try {\n    api.book(s); BookResult.Booked\n} catch (e: IOException) {\n    BookResult.Failed(BookingFailure.Offline)\n} catch (e: HttpException) {\n    BookResult.Failed(if (e.code() == 409) BookingFailure.SlotTaken else BookingFailure.ServerProblem)\n}   // không bắt Exception: lỗi lập trình và CancellationException đi tiếp',
      'sealed interface BookingFailure {\n    data object Offline : BookingFailure\n    data object SlotTaken : BookingFailure\n    data object ServerProblem : BookingFailure\n}\nsuspend fun book(s: Slot): BookResult = try {\n    api.book(s); BookResult.Booked\n} catch (e: IOException) {\n    BookResult.Failed(BookingFailure.Offline)\n} catch (e: HttpException) {\n    BookResult.Failed(if (e.code() == 409) BookingFailure.SlotTaken else BookingFailure.ServerProblem)\n}   // no catch of Exception: bugs and CancellationException go through')
    B(C, S_, 3, 'note', 'Repository là chỗ hợp để đổi lỗi: chỉ nó biết thư viện mạng ném gì (IOException, HttpException của Retrofit). Tầng trên chỉ thấy failure của app, nên đổi thư viện mạng không làm sửa ViewModel. Theo cách đảo phụ thuộc của sách (G2), failure là mô hình của domain.', 'The repository is the right place to map errors: only it knows what the network library throws (IOException, Retrofit\'s HttpException). Upper layers see only the app\'s failures, so changing the network library does not touch the ViewModel. With the books\' inversion (G2), failures are domain models.')

    S_ = 'show'
    a(C + '.sec.%s.title' % S_, 'Hiện lỗi trên màn hình', 'Showing errors on screen')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'p', 'Hiện lỗi giống hiện trạng thái đang tải ở chỗ đều là state, nhưng lỗi thường kèm thông điệp cho người dùng hay một hành động như thử lại, nên nên mô hình bằng data class mang đủ thông tin đó. ViewModel chọn câu theo failure (từ tài nguyên chuỗi, để dịch được) và quyết định có nút Thử lại không. Thông báo thoáng qua thì theo cách của chương G3: UI hiện rồi báo lại để xóa. [[src:ax-ui-layer]]',
      'Showing errors is like showing loading in that both are state, but errors often carry a message for the user or an action such as retry, so they are modelled with data classes holding that information. The ViewModel picks a sentence for the failure (from string resources, so it can be translated) and decides whether to offer Retry. Transient messages follow chapter G3: the UI shows them and reports back to clear them. [[src:ax-ui-layer]]')

    S_ = 'bugs'
    a(C + '.sec.%s.title' % S_, 'Hai lỗi hay gặp', 'Two common bugs')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'bug', 'App crash mỗi khi mở màn Chọn giờ lúc mất mạng.', 'The app crashes whenever Choose a time opens offline.')
    B(C, S_, 1, 'cause', 'IOException từ nguồn mạng đi thẳng lên viewModelScope.launch, không tầng nào bắt.', 'The IOException from the network source goes straight up into viewModelScope.launch; no layer catches it.')
    B(C, S_, 1, 'fix', 'Repository bắt IOException và trả failure Offline; ViewModel đổi thành UI state lỗi có nút Thử lại.', 'The repository catches IOException and returns an Offline failure; the ViewModel turns it into an error UI state with Retry.')
    B(C, S_, 2, 'bug', 'Người dùng chụp màn hình gửi hỗ trợ: "HTTP 409 Conflict".', 'A user sends support a screenshot: "HTTP 409 Conflict".')
    B(C, S_, 2, 'cause', 'ViewModel bắt Exception và đưa thẳng e.message của thư viện mạng lên màn hình.', 'The ViewModel catches Exception and puts the network library\'s e.message straight on screen.')
    B(C, S_, 2, 'fix', 'Đổi 409 thành SlotTaken ở repository; ViewModel hiện "Giờ này vừa có người đặt, chọn giờ khác" từ tài nguyên chuỗi.', 'Map 409 to SlotTaken in the repository; the ViewModel shows "This slot was just taken, pick another" from string resources.')

    S_ = 'ex'
    a(C + '.sec.%s.title' % S_, 'Bài tập', 'Exercise')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'ex', 'Phân loại failure hay exception, và nói tầng nào xử lý: (a) mã giảm giá đã hết hạn; (b) JSON từ máy chủ thiếu trường bắt buộc; (c) hết thời gian chờ kết nối; (d) người dùng chưa đăng nhập (401); (e) chia cho 0 trong hàm tính phí. (Bài tập của site, theo cách phân loại của Boudjnah .) [[src:book-boudjnah]]',
      'Classify as failure or exception, and say which layer handles it: (a) a discount code has expired; (b) the server\'s JSON lacks a required field; (c) a connection timeout; (d) the user is not signed in (401); (e) division by zero in the fee calculation. (The site\'s own exercise, after Boudjnah \'s classification.) [[src:book-boudjnah]]')
    B(C, S_, 1, 'hint', 'Hỏi: ta có dự đoán được nó và có cách cho người dùng đi tiếp không?', 'Ask: can we expect it, and is there a way for the user to carry on?')
    B(C, S_, 1, 'sol', '(a) Failure: repository đổi thành CouponExpired, UI gợi ý bỏ mã. (b) Exception (hợp đồng với máy chủ bị vỡ): ghi log, theo dõi; với người dùng có thể hiện lỗi chung, nhưng không giấu. (c) Failure: như mất mạng, Thử lại. (d) Failure: đưa về màn đăng nhập. (e) Exception: bug trong mã, sửa mã chứ không bắt.',
      '(a) Failure: the repository maps it to CouponExpired, the UI suggests removing the code. (b) Exception (the server contract is broken): log and monitor; the user may see a generic error, but do not hide it. (c) Failure: like offline, with Retry. (d) Failure: send the user to sign in. (e) Exception: a bug in the code; fix the code rather than catch it.')

    S_ = 'recall'
    a(C + '.sec.%s.title' % S_, 'Tự trả lời', 'Answer it yourself')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'ask', 'Failure khác exception ở điểm nào?', 'How does a failure differ from an exception?')
    B(C, S_, 1, 'ans', 'Failure dự đoán được và phục hồi được, xử lý như giá trị; exception là chuyện bất ngờ, ghi log và theo dõi.', 'A failure is expected and recoverable, handled as a value; an exception is unexpected, logged and monitored.')
    B(C, S_, 2, 'ask', 'Vì sao không nên bắt Exception trong hàm suspend?', 'Why not catch Exception in a suspend function?')
    B(C, S_, 2, 'ans', 'Nó bắt cả lỗi lập trình (giấu bug) và CancellationException (làm hỏng việc hủy coroutine).', 'It catches programming errors too (hiding bugs) and CancellationException (breaking coroutine cancellation).')

    S_ = 'honest'
    a(C + '.sec.%s.title' % S_, 'Chương này giản lược những gì', 'What this chapter simplifies')
    a(C + '.sec.%s.badge' % S_, 'simplified')
    B(C, S_, 1, 'p', 'Phân loại failure và exception theo Boudjnah (đọc từ epub trong kho), cách lộ lỗi ở tầng data và hiện lỗi trên màn hình theo trang Data layer và UI layer đọc ngày 2026-11-24. HttpException và mã 409/500 là ví dụ với Retrofit. Chương chưa nói về lỗi trong Flow (toán tử catch, retry) chi tiết, CoroutineExceptionHandler (track Coroutines A6) và cách thiết lập crash report.',
      'The failure/exception classification follows Boudjnah (read from the epub in the library); exposing errors in the data layer and showing them on screen follow the Data layer and UI layer pages as read on 2026-11-24. HttpException and codes 409/500 are examples with Retrofit. The chapter does not cover errors in Flows (the catch and retry operators) in detail, CoroutineExceptionHandler (Coroutines track A6), or setting up crash reporting.')

    for q, qv, qe, av, ae, wv, we in [
        ('q1', 'Mất mạng là failure hay exception?', 'Is being offline a failure or an exception?', 'Failure: dự đoán được, có cách xử lý.', 'A failure: expected, with a way to handle it.', 'Người dùng có thể thử lại.', 'The user can retry.'),
        ('q2', 'Tầng nào nên đổi IOException thành failure của app?', 'Which layer should turn an IOException into an app failure?', 'Tầng data (repository).', 'The data layer (repository).', 'Chỉ nó biết thư viện mạng ném gì.', 'Only it knows what the network library throws.'),
        ('q3', 'Vì sao dùng sealed class cho failure thay vì Boolean?', 'Why use a sealed class for failures rather than a Boolean?', 'Đặt tên được từng trường hợp và mở rộng được.', 'It names each case and can grow.', 'Boolean không nói được thất bại vì sao.', 'A Boolean cannot say why something failed.'),
        ('q4', 'Một NullPointerException do bug nên xử lý thế nào?', 'How should a NullPointerException from a bug be handled?', 'Không nuốt; để crash report ghi lại và sửa mã.', 'Do not swallow it; let crash reporting record it and fix the code.', 'Nó là exception, không phải failure.', 'It is an exception, not a failure.')]:
        a(C + '.quiz.%s.q' % q, qv, qe); a(C + '.quiz.%s.a' % q, av, ae); a(C + '.quiz.%s.why' % q, wv, we)
