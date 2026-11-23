# Kotlin · K5: enum, sealed và when (Phần 1)
# Nguồn: kotlinlang.org Sealed classes and interfaces, Enum classes, Conditions and loops đọc 2026-11-23;
# Kotlin Essentials (Enum classes, Sealed classes and interfaces); Effective Kotlin Items 39–41.
# Bài tập dựa trên "Days of the week enum" (Kotlin Exercises), diễn đạt lại. Trần: 8 mục, mục cơ chế ≤ 5 khối.

SEC_ORDER = {'k5': ['hook', 'enum', 'sealed', 'when', 'bugs', 'ex', 'recall', 'honest']}


def add(a):
    def B(ch, sec, n, field, vi, en=None):
        a('%s.sec.%s.b.%02d.%s' % (ch, sec, n, field), vi, vi if en is None else en)

    m = lambda k, vi, en=None: a('m.sealed.' + k, vi, en)
    m('title', 'sealed và when: khi thêm một trạng thái mới', 'sealed and when: when a new state is added')
    m('overview', 'Màn Chọn giờ có UiState là một sealed interface với Loading, Success, Error. Sau này nhóm thêm Empty. Hai cách viết when (không else và có else) phản ứng rất khác. Tình huống thứ ba: đổi chuỗi từ máy chủ sang enum bằng valueOf.',
      'The Choose a time screen has a UiState sealed interface with Loading, Success, Error. Later the team adds Empty. Two ways of writing when (no else and with else) react very differently. A third situation: turning a server string into an enum with valueOf.')
    m('wrapup', 'Với sealed, trình biên dịch biết hết các kiểu con, nên when dạng biểu thức không cần else và sẽ báo lỗi ở mọi chỗ thiếu nhánh khi bạn thêm kiểu con mới. Viết else là tự tắt lời nhắc đó. Với enum đến từ dữ liệu ngoài, valueOf cần tên khớp chính xác; dùng entries và tìm có kiểm.',
      'With sealed, the compiler knows every subtype, so a when expression needs no else and reports every missing branch when you add a new subtype. Writing else switches that reminder off. For enums coming from outside data, valueOf needs an exact name match; use entries with a checked lookup.')
    m('simp.1', 'Sơ đồ gom việc kiểm exhaustive vào khối "trình biên dịch"; số nhánh đã phủ là đếm theo đoạn mã mẫu.', 'The diagram folds the exhaustiveness check into the "compiler" box; the covered branch count is counted from the sample code.')
    m('simp.2', 'Kết quả (lỗi biên dịch khi thiếu nhánh, IllegalArgumentException của valueOf) theo tài liệu Kotlin; site không chạy Kotlin trong trang.', 'The outcomes (a compile error for a missing branch, valueOf\'s IllegalArgumentException) follow the Kotlin docs; the site does not run Kotlin in the page.')
    m('ctl.hint', 'So "when không else" với "when có else" ở bước thêm Empty.', 'Compare "when without else" with "when with else" at the step that adds Empty.')
    m('ctl.case', 'Tình huống', 'Situation')
    for k, vi, en in [('exhaustive', 'when không else', 'when without else'), ('withElse', 'when có else', 'when with else'), ('valueOf', 'enum từ chuỗi bằng valueOf', 'enum from a string with valueOf')]:
        m('ctl.case.' + k, vi, en)
    m('diagramTitle', 'Khai báo kiểu, when, trình biên dịch, kết quả lúc chạy', 'Type declaration, when, compiler, runtime result')
    m('diagramDesc', 'Kiểu sealed hoặc enum được dùng trong một when hay một phép đổi; trình biên dịch kiểm đủ nhánh; lúc chạy màn hình hiện kết quả', 'A sealed or enum type is used in a when or a conversion; the compiler checks the branches; at runtime the screen shows the result')
    for k, vi, en in [('def', 'Khai báo sealed / enum', 'sealed / enum declaration'), ('when', 'when / chuyển đổi', 'when / conversion'), ('compiler', 'Trình biên dịch kiểm', 'Compiler check'), ('screen', 'Kết quả lúc chạy', 'Runtime result')]:
        m('n.' + k, vi, en)
    m('met.covered', 'Nhánh xử lý đúng', 'Branches handled right'); m('met.total', 'Số kiểu con', 'Number of subtypes')
    a('cap.sealed', 'Từ trái sang phải: khai báo kiểu, when hoặc phép đổi, kiểm tra của trình biên dịch, kết quả trên màn hình. Khối viền đỏ là chỗ trình biên dịch báo lỗi, hoặc chỗ lúc chạy cho kết quả sai hay ném ngoại lệ.', 'Left to right: the type declaration, the when or conversion, the compiler\'s check, the result on screen. A red-outlined box is where the compiler reports an error, or where the runtime gives a wrong result or throws.')
    S = [
        ('exhaustive', 'start', 'sealed interface UiState: 3 kiểu con', 'sealed interface UiState: 3 subtypes', 'Loading, Success(slots), Error(message). Hàm title() đổi state thành tiêu đề bằng when, KHÔNG có else.', 'Loading, Success(slots), Error(message). title() turns a state into a heading with when, WITHOUT else.'),
        ('exhaustive', 'first', 'Trình biên dịch: đủ 3/3 nhánh', 'Compiler: all 3/3 branches', 'Vì UiState là sealed, trình biên dịch biết đúng ba kiểu con và thấy when đã phủ hết, nên không đòi else. Trong nhánh is Success, s được smart cast sang Success.', 'Because UiState is sealed, the compiler knows exactly three subtypes and sees the when covers them all, so it does not ask for else. Inside the is Success branch, s is smart cast to Success.'),
        ('exhaustive', 'next', 'Thêm Empty: lỗi biên dịch ở title()', 'Add Empty: compile error in title()', 'Bây giờ có 4 kiểu con mà when chỉ phủ 3. Trình biên dịch báo lỗi ở ĐÚNG chỗ này và mọi when khác trên UiState: đây là điều ta muốn.', 'There are now 4 subtypes and the when covers only 3. The compiler reports an error right here and at every other when over UiState: this is what we want.'),
        ('exhaustive', 'end', 'Thêm nhánh Empty: đủ 4/4', 'Add the Empty branch: 4/4', 'Người viết buộc phải quyết định màn hình hiện gì khi Empty, ví dụ "Chưa có giờ trống".', 'The author is forced to decide what the screen shows for Empty, for example "No free slots yet".'),
        ('withElse', 'start', 'Cùng UiState, when có else', 'The same UiState, a when with else', 'Lần này title() xử lý Loading và Success, còn lại gom vào else "Có lỗi xảy ra".', 'This time title() handles Loading and Success and sends everything else to else, "Something went wrong".'),
        ('withElse', 'first', 'Biên dịch được', 'It compiles', 'Có else thì when luôn phủ hết, trình biên dịch không có gì để kiểm thêm.', 'With else the when always covers everything, so the compiler has nothing more to check.'),
        ('withElse', 'next', 'Thêm Empty: vẫn biên dịch, màn hình báo lỗi sai', 'Add Empty: still compiles, the screen shows a wrong error', 'Empty lặng lẽ rơi vào else. Người dùng chưa có lịch nào lại thấy "Có lỗi xảy ra". Không có cảnh báo nào ở đâu cả.', 'Empty silently lands in else. A user who simply has no bookings sees "Something went wrong". No warning anywhere.'),
        ('withElse', 'end', 'Sửa: bỏ else, để trình biên dịch tìm chỗ thiếu', 'Fix: drop else and let the compiler find the gaps', 'Viết đủ từng nhánh (kể cả Error) thay vì else; lần thêm kiểu con sau, trình biên dịch sẽ chỉ ra mọi chỗ cần sửa.', 'Write every branch (Error included) instead of else; next time a subtype is added, the compiler points to every place that needs a change.'),
        ('valueOf', 'start', 'enum Status; máy chủ gửi "booked"', 'enum Status; the server sends "booked"', 'Hằng enum tên BOOKED (chữ hoa), còn chuỗi từ máy chủ là "booked" (chữ thường).', 'The enum constant is named BOOKED (uppercase), while the server string is "booked" (lowercase).'),
        ('valueOf', 'first', 'Status.valueOf("booked")', 'Status.valueOf("booked")', 'valueOf tìm hằng có tên khớp CHÍNH XÁC với chuỗi.', 'valueOf looks for a constant whose name matches the string EXACTLY.'),
        ('valueOf', 'next', 'Không khớp: IllegalArgumentException', 'No match: IllegalArgumentException', 'Không có hằng nào tên "booked", nên valueOf ném IllegalArgumentException. Một giá trị mới từ máy chủ (ví dụ "no_show") cũng làm crash y như vậy.', 'No constant is named "booked", so valueOf throws IllegalArgumentException. A new value from the server ("no_show", say) crashes in exactly the same way.'),
        ('valueOf', 'end', 'Sửa: tìm trong entries, có giá trị dự phòng', 'Fix: search entries, with a fallback', 'Status.entries.firstOrNull { it.name.equals(raw, ignoreCase = true) } trả null thay vì crash; quyết định rõ làm gì với giá trị lạ.', 'Status.entries.firstOrNull { it.name.equals(raw, ignoreCase = true) } returns null instead of crashing; decide explicitly what to do with unknown values.'),
    ]
    for case, k, tv, te, xv, xe in S:
        sid = case + '.' + k
        m('s.%s.title' % sid, tv, te); m('s.%s.explain' % sid, xv, xe); m('ev.' + sid, tv, te)
    for k, vi, en in [
        ('try', 'Đổi tình huống rồi đi lại; để ý số nhánh xử lý đúng so với số kiểu con.', 'Change the situation and walk again; compare branches handled right with the number of subtypes.'),
        ('exhaustive.next', 'Tài liệu Sealed classes: dùng với when, trình biên dịch kiểm được đã phủ hết mọi trường hợp, nên không cần else. [[src:kt-sealed]]', 'Sealed classes docs: used with when, the compiler can check exhaustively that all cases are covered, so no else is needed. [[src:kt-sealed]]'),
        ('exhaustive.end', 'Tài liệu Conditions and loops: when dạng biểu thức phải phủ đủ; với subject là Boolean, enum hay sealed thì có thể phủ đủ mà không cần else. [[src:kt-control-flow]]', 'Conditions and loops docs: a when expression must be exhaustive; with a Boolean, enum or sealed subject it can be exhaustive without else. [[src:kt-control-flow]]'),
        ('withElse.next', 'else khớp mọi thứ chưa được liệt kê, nên kiểu con mới không làm lỗi biên dịch. Đó là lý do nên tránh else khi subject là sealed hay enum mà bạn tự quản lý.', 'else matches everything not listed, so a new subtype causes no compile error. That is why to avoid else when the subject is a sealed or enum type you control.'),
        ('withElse.end', 'Ngoại lệ hợp lý: dự án multiplatform, nơi tài liệu nói when trên sealed trong mã chung vẫn cần else. [[src:kt-sealed]]', 'A reasonable exception: multiplatform projects, where the docs say a when over a sealed type in common code still needs else. [[src:kt-sealed]]'),
        ('valueOf.next', 'Tài liệu Enum classes: tên truyền cho valueOf phải khớp chính xác; không có hằng nào thì ném IllegalArgumentException. [[src:kt-enum]]', 'Enum classes docs: the name passed to valueOf must match exactly; if no constant matches, it throws IllegalArgumentException. [[src:kt-enum]]'),
        ('valueOf.end', 'Tài liệu cũng gợi ý entries.getOrNull(index) khi có vị trí số thay vì ép kiểu Int sang enum. [[src:kt-enum]]', 'The docs also suggest entries.getOrNull(index) when you have a numeric position instead of casting an Int to an enum. [[src:kt-enum]]')]:
        m('co.' + k, vi, en)

    C = 'k5'
    a(C + '.title', 'Enum, sealed và when', 'Enums, sealed types and when')
    a(C + '.essence', 'enum class là một tập giá trị cố định, mỗi hằng có name và ordinal, có thể mang thuộc tính và hàm; entries liệt kê tất cả.\nsealed class/interface là một tập KIỂU cố định: mọi kiểu con trực tiếp được biết lúc biên dịch, mỗi kiểu con có thể mang dữ liệu riêng. Hợp để mô hình trạng thái màn hình.\nwhen dạng biểu thức trên sealed hay enum không cần else; bỏ else để trình biên dịch nhắc mọi chỗ thiếu khi thêm kiểu con mới.',
      'An enum class is a fixed set of values; each constant has a name and an ordinal, can carry properties and functions, and entries lists them all.\nA sealed class/interface is a fixed set of TYPES: every direct subtype is known at compile time, and each can carry its own data. A good fit for screen state.\nA when expression over a sealed or enum type needs no else; drop the else so the compiler flags every gap when a new subtype is added.')
    a(C + '.goal.g1', 'Đã xem trình biên dịch kiểm when', 'Saw the compiler check the when')
    a(C + '.goal.g2', 'Đã đi tới cách sửa', 'Reached the fix')
    a(C + '.sim.kotlin.sealed', 'sealed và when', 'sealed and when')

    S_ = 'hook'
    a(C + '.sec.%s.title' % S_, 'Đoán trước khi đọc', 'Predict before reading')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'predict', 'UiState là sealed interface có Loading, Success, Error. Hai màn hình dùng `when (state)`: màn A liệt kê đủ ba nhánh, màn B có Loading, Success và `else`. Nhóm thêm `data object Empty : UiState`. Màn nào lỗi biên dịch, màn nào chạy sai mà không ai biết?',
      'UiState is a sealed interface with Loading, Success, Error. Two screens use `when (state)`: screen A lists all three branches, screen B has Loading, Success and `else`. The team adds `data object Empty : UiState`. Which screen fails to compile, and which silently runs wrong?')
    B(C, S_, 1, 'ans', 'Màn A lỗi biên dịch (thiếu nhánh Empty): đó là tin tốt, trình biên dịch chỉ đúng chỗ cần sửa. Màn B vẫn biên dịch, và Empty rơi vào else, hiện thông báo lỗi cho người dùng chỉ đơn giản là chưa có lịch. Mô phỏng ngay dưới đi qua cả hai. [[src:kt-sealed]]',
      'Screen A fails to compile (the Empty branch is missing): good news, the compiler points at exactly what to fix. Screen B still compiles, and Empty lands in else, showing an error to a user who simply has no bookings yet. The simulation just below walks through both. [[src:kt-sealed]]')

    S_ = 'enum'
    a(C + '.sec.%s.title' % S_, 'enum class', 'enum classes')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'p', '`enum class Status { BOOKED, CANCELLED, DONE }` khai báo một tập giá trị cố định. Mỗi hằng có sẵn `name` (tên như đã viết) và `ordinal` (vị trí, bắt đầu từ 0). Hằng enum có thể mang thuộc tính qua constructor và có hàm riêng. `Status.entries` là danh sách mọi hằng theo thứ tự khai báo; `Status.valueOf("BOOKED")` tìm theo tên và ném `IllegalArgumentException` nếu không khớp chính xác. [[src:kt-enum]]',
      '`enum class Status { BOOKED, CANCELLED, DONE }` declares a fixed set of values. Each constant has a built-in `name` (as written) and `ordinal` (its position, starting at 0). Enum constants can carry properties through a constructor and have their own functions. `Status.entries` is the list of all constants in declaration order; `Status.valueOf("BOOKED")` looks up by name and throws `IllegalArgumentException` if there is no exact match. [[src:kt-enum]]')
    B(C, S_, 2, 'kt', 'enum class Status(val label: String, val canReschedule: Boolean) {\n    BOOKED("Đã đặt", true),\n    CANCELLED("Đã hủy", false),\n    DONE("Đã khám", false);\n\n    fun isActive() = this == BOOKED\n}\nStatus.entries.filter { it.canReschedule }   // [BOOKED]',
      'enum class Status(val label: String, val canReschedule: Boolean) {\n    BOOKED("Booked", true),\n    CANCELLED("Cancelled", false),\n    DONE("Seen", false);\n\n    fun isActive() = this == BOOKED\n}\nStatus.entries.filter { it.canReschedule }   // [BOOKED]')

    S_ = 'sealed'
    a(C + '.sec.%s.title' % S_, 'sealed class và sealed interface', 'Sealed classes and sealed interfaces')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'p', 'enum giới hạn GIÁ TRỊ; sealed giới hạn KIỂU. Mọi kiểu con trực tiếp của một sealed class hay sealed interface được biết lúc biên dịch: chúng phải nằm cùng package và module, và sau khi module được biên dịch thì không ai thêm kiểu con mới được. Khác enum, mỗi kiểu con có thể là data class mang dữ liệu riêng, hay data object khi không có dữ liệu. [[src:kt-sealed]]',
      'An enum restricts VALUES; sealed restricts TYPES. Every direct subtype of a sealed class or sealed interface is known at compile time: they must live in the same package and module, and once the module is compiled nobody can add new subtypes. Unlike an enum, each subtype can be a data class carrying its own data, or a data object when there is none. [[src:kt-sealed]]')
    B(C, S_, 2, 'p', 'Đó là lý do sealed hợp với trạng thái màn hình trên Android: Loading không có dữ liệu, Success mang danh sách giờ trống, Error mang thông báo. Một biến kiểu UiState luôn đúng một trong các trạng thái đó, không có tổ hợp vô nghĩa như "đang tải mà cũng có lỗi" kiểu hay gặp khi dùng nhiều cờ Boolean.',
      'That is why sealed fits screen state on Android: Loading has no data, Success carries the free slots, Error carries a message. A UiState variable is always exactly one of them, with none of the meaningless combinations such as "loading and also an error" that you get with several Boolean flags.')

    S_ = 'when'
    a(C + '.sec.%s.title' % S_, 'when phủ đủ và vì sao tránh else', 'Exhaustive when and why to avoid else')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'p', 'Khi `when` được dùng như biểu thức, nó phải phủ mọi trường hợp. Với subject là Boolean, enum hay sealed, trình biên dịch biết đủ các trường hợp nên when có thể phủ hết mà không cần `else`. Trong nhánh `is Success`, subject được smart cast sang Success, nên đọc được `s.slots` (chương K2). [[src:kt-control-flow]] [[src:kt-sealed]]',
      'When `when` is used as an expression, it must cover every case. With a Boolean, enum or sealed subject, the compiler knows all the cases, so the when can be exhaustive without `else`. Inside an `is Success` branch the subject is smart cast to Success, so `s.slots` is readable (chapter K2). [[src:kt-control-flow]] [[src:kt-sealed]]')
    B(C, S_, 2, 'note', 'Viết `else` trên một sealed hay enum mà bạn tự quản lý là tự tắt lời nhắc quý nhất của trình biên dịch: lần thêm kiểu con sau, mọi when có else vẫn biên dịch và lặng lẽ xử lý sai. Liệt kê đủ từng nhánh. Ngoại lệ: mã chung trong dự án multiplatform, nơi tài liệu nói vẫn cần else. [[src:kt-sealed]]',
      'Writing `else` over a sealed or enum type you control switches off the compiler\'s most valuable reminder: next time a subtype is added, every when with else still compiles and silently does the wrong thing. List every branch. The exception: common code in multiplatform projects, where the docs say else is still needed. [[src:kt-sealed]]')
    B(C, S_, 2, 'kind', 'pitfall')

    S_ = 'bugs'
    a(C + '.sec.%s.title' % S_, 'Hai lỗi hay gặp', 'Two common bugs')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'bug', 'Sau khi thêm trạng thái `Empty`, người dùng mới (chưa có lịch nào) thấy "Có lỗi xảy ra" ở màn Lịch của tôi.', 'After the `Empty` state is added, new users (with no bookings yet) see "Something went wrong" on My appointments.')
    B(C, S_, 1, 'cause', '`when (state)` trên UiState có nhánh `else -> ErrorView()`; Empty rơi vào đó, trình biên dịch không báo gì.', '`when (state)` over UiState has an `else -> ErrorView()` branch; Empty lands there and the compiler says nothing.')
    B(C, S_, 1, 'fix', 'Bỏ `else`, liệt kê đủ nhánh (kể cả Error); trình biên dịch sẽ đòi nhánh Empty và mọi chỗ tương tự.', 'Drop `else` and list every branch (Error included); the compiler then demands an Empty branch here and everywhere similar.')
    B(C, S_, 2, 'bug', 'App crash khi máy chủ bắt đầu trả trạng thái mới "no_show" cho lịch hẹn.', 'The app crashes when the server starts returning a new "no_show" appointment status.')
    B(C, S_, 2, 'cause', '`Status.valueOf(json.status.uppercase())` ném `IllegalArgumentException` vì enum chưa có `NO_SHOW`.', '`Status.valueOf(json.status.uppercase())` throws `IllegalArgumentException` because the enum has no `NO_SHOW` yet.')
    B(C, S_, 2, 'fix', 'Đổi dữ liệu ngoài sang enum bằng `entries.firstOrNull { … }` với giá trị dự phòng (ví dụ `UNKNOWN`) và ghi log, thay vì valueOf.', 'Convert outside data with `entries.firstOrNull { … }` and a fallback (such as `UNKNOWN`) plus a log entry, instead of valueOf.')

    S_ = 'ex'
    a(C + '.sec.%s.title' % S_, 'Bài tập', 'Exercise')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'ex', 'Phòng khám làm việc cả tuần. Viết `enum class ClinicDay` với bảy ngày từ MONDAY tới SUNDAY theo đúng thứ tự, mỗi hằng có `isWeekend: Boolean` và `label: String` (ví dụ "Thứ Hai"). Thêm `fun next(): ClinicDay` trả ngày kế tiếp, với SUNDAY.next() là MONDAY. (Dựa trên bài "Days of the week enum" của Kotlin Exercises, diễn đạt lại.) [[src:book-kt-exercises]]',
      'The clinic works all week. Write an `enum class ClinicDay` with the seven days MONDAY to SUNDAY in order, each with `isWeekend: Boolean` and `label: String` ("Monday", say). Add `fun next(): ClinicDay` returning the following day, with SUNDAY.next() being MONDAY. (Based on the "Days of the week enum" exercise in Kotlin Exercises, restated.) [[src:book-kt-exercises]]')
    B(C, S_, 1, 'hint', 'Dùng `ordinal` và `entries`: ngày kế tiếp là phần tử ở vị trí `(ordinal + 1) % entries.size`.', 'Use `ordinal` and `entries`: the next day is the element at `(ordinal + 1) % entries.size`.')
    B(C, S_, 1, 'sol', 'Lời giải dựa vào thứ tự khai báo, nên đừng đổi thứ tự các hằng.', 'The solution relies on declaration order, so do not reorder the constants.')
    B(C, S_, 1, 'solkt', 'enum class ClinicDay(val isWeekend: Boolean, val label: String) {\n    MONDAY(false, "Monday"), TUESDAY(false, "Tuesday"), WEDNESDAY(false, "Wednesday"),\n    THURSDAY(false, "Thursday"), FRIDAY(false, "Friday"),\n    SATURDAY(true, "Saturday"), SUNDAY(true, "Sunday");\n\n    fun next(): ClinicDay = entries[(ordinal + 1) % entries.size]\n}')

    S_ = 'recall'
    a(C + '.sec.%s.title' % S_, 'Tự trả lời', 'Answer it yourself')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'ask', 'Khi nào chọn sealed thay vì enum?', 'When do you choose sealed over enum?')
    B(C, S_, 1, 'ans', 'Khi các trường hợp cần mang dữ liệu khác nhau (Success có danh sách, Error có thông báo); enum hợp khi mọi giá trị cùng một dạng.', 'When the cases need to carry different data (Success has a list, Error has a message); enum fits when every value has the same shape.')
    B(C, S_, 2, 'ask', 'Vì sao when có else trên một sealed type nguy hiểm khi thêm kiểu con mới?', 'Why is a when with else over a sealed type dangerous when a subtype is added?')
    B(C, S_, 2, 'ans', 'else khớp kiểu con mới, nên mã vẫn biên dịch và xử lý sai mà không có cảnh báo nào.', 'else matches the new subtype, so the code still compiles and handles it wrongly with no warning.')

    S_ = 'honest'
    a(C + '.sec.%s.title' % S_, 'Chương này giản lược những gì', 'What this chapter simplifies')
    a(C + '.sec.%s.badge' % S_, 'simplified')
    B(C, S_, 1, 'p', 'Quy tắc về sealed, when và valueOf theo tài liệu Kotlin đọc ngày 2026-11-23. Chương chỉ khẳng định quy tắc phủ đủ cho when dạng BIỂU THỨC, vì đó là điều tài liệu nêu; site chưa tự kiểm hành vi của when dạng câu lệnh trên sealed ở các phiên bản trình biên dịch. Chương bỏ qua sealed class lồng nhiều tầng, enum implement interface và context-sensitive resolution (tài liệu ghi đang preview).',
      'The rules on sealed, when and valueOf follow the Kotlin docs as read on 2026-11-23. The chapter only states the exhaustiveness rule for when used as an EXPRESSION, because that is what the docs say; the site has not checked how when statements over sealed types behave across compiler versions. It skips multi-level sealed hierarchies, enums implementing interfaces and context-sensitive resolution (which the docs mark as preview).')

    for q, qv, qe, av, ae, wv, we in [
        ('q1', '`Status.valueOf("booked")` với hằng BOOKED trả gì?', 'What does `Status.valueOf("booked")` return for a constant BOOKED?', 'Ném IllegalArgumentException.', 'It throws IllegalArgumentException.', 'Tên phải khớp chính xác, kể cả chữ hoa.', 'The name must match exactly, case included.'),
        ('q2', 'Kiểu con của một sealed interface có được khai báo ở module khác không?', 'Can a subtype of a sealed interface be declared in another module?', 'Không.', 'No.', 'Kiểu con trực tiếp phải cùng package và module.', 'Direct subtypes must be in the same package and module.'),
        ('q3', 'when dạng biểu thức trên enum có bắt buộc else không?', 'Does a when expression over an enum require else?', 'Không, nếu đã liệt kê đủ mọi hằng.', 'No, if every constant is listed.', 'Trình biên dịch biết đủ các hằng.', 'The compiler knows every constant.'),
        ('q4', '`ordinal` của hằng đầu tiên là bao nhiêu?', 'What is the `ordinal` of the first constant?', '0.', '0.', 'Vị trí bắt đầu từ 0.', 'Positions start at 0.')]:
        a(C + '.quiz.%s.q' % q, qv, qe); a(C + '.quiz.%s.a' % q, av, ae); a(C + '.quiz.%s.why' % q, wv, we)
