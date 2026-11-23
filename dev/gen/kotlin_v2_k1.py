# Kotlin · K1: val/var, kiểu, hàm, biểu thức (Phần 1: nền tảng cho người mới)
# Nguồn: kotlinlang.org Basic syntax, Numbers, Conditions and loops, Functions (đọc 2026-11-23);
# Kotlin Essentials (Variables, Basic types, Conditional statements, Functions); Effective Kotlin Item 1;
# bài tập dựa trên "Pretty time display" (Kotlin Exercises), diễn đạt lại. Trần: 8 mục, mục cơ chế ≤ 5 khối.

SEC_ORDER = {'k1': ['hook', 'vars', 'numbers', 'expr', 'bugs', 'ex', 'recall', 'honest']}


def add(a):
    def B(ch, sec, n, field, vi, en=None):
        a('%s.sec.%s.b.%02d.%s' % (ch, sec, n, field), vi, vi if en is None else en)

    # ---------------- sim kotlin.eval ----------------
    m = lambda k, vi, en=None: a('m.eval.' + k, vi, en)
    m('title', 'Một biểu thức: kiểu lúc biên dịch, giá trị lúc chạy', 'One expression: type at compile time, value at runtime')
    m('overview', 'Bốn biểu thức ngắn. Với mỗi biểu thức, theo dõi hai việc tách biệt: trình biên dịch suy ra kiểu gì (trước khi chạy), rồi lúc chạy giá trị là bao nhiêu. Phần lớn bất ngờ của người mới nằm ở khoảng giữa hai việc đó.',
      'Four short expressions. For each one, follow two separate things: which type the compiler infers (before running), then what the value is at runtime. Most beginner surprises live between the two.')
    m('wrapup', 'Kiểu được chốt lúc biên dịch từ kiểu của các toán hạng; lúc chạy, phép tính làm đúng theo kiểu đó. Int chia Int vẫn là Int nên mất phần lẻ; Int cộng tràn vẫn là Int nên quay vòng. Muốn kết quả khác thì đổi kiểu của toán hạng TRƯỚC khi tính.',
      'The type is fixed at compile time from the operand types; at runtime the operation follows that type exactly. Int divided by Int stays Int, so the fraction is lost; an overflowing Int stays Int, so it wraps around. For a different result, change an operand\'s type BEFORE the operation.')
    m('simp.1', 'Sơ đồ tách "suy kiểu" và "tính giá trị" thành hai khối cho dễ nhìn; trình biên dịch thật làm nhiều việc hơn (phân tích cú pháp, kiểm tra, sinh bytecode).', 'The diagram splits "infer the type" and "compute the value" into two boxes for clarity; a real compiler does much more (parsing, checking, generating bytecode).')
    m('simp.2', 'Giá trị trong mô phỏng là kết quả tài liệu Kotlin nêu, không phải mã Kotlin chạy trong trang.', 'The values in the simulation are the results stated by the Kotlin docs, not Kotlin code running in the page.')
    m('ctl.hint', 'So "chia nguyên" với "chia cho 2.0" ở bước suy kiểu.', 'Compare "integer division" with "dividing by 2.0" at the type step.')
    m('ctl.case', 'Biểu thức', 'Expression')
    for k, vi, en in [('intdiv', 'Chia nguyên: total / 2', 'Integer division: total / 2'), ('double', 'Chia cho 2.0', 'Dividing by 2.0'),
                      ('overflow', 'Tràn Int: max + 1', 'Int overflow: max + 1'), ('when', 'when có subject và khoảng', 'when with a subject and ranges')]:
        m('ctl.case.' + k, vi, en)
    m('diagramTitle', 'Mã nguồn, suy kiểu, tính giá trị, biến', 'Source, type inference, evaluation, variable')
    m('diagramDesc', 'Mã nguồn đi qua bước suy kiểu lúc biên dịch, rồi bước tính giá trị lúc chạy, rồi giá trị được gán cho biến', 'The source goes through type inference at compile time, then evaluation at runtime, then the value is assigned to the variable')
    for k, vi, en in [('src', 'Mã nguồn', 'Source code'), ('types', 'Suy kiểu (biên dịch)', 'Type inference (compile time)'), ('eval', 'Tính giá trị (chạy)', 'Evaluation (runtime)'), ('out', 'Biến nhận kết quả', 'Variable gets the result')]:
        m('n.' + k, vi, en)
    m('met.type', 'Kiểu', 'Type'); m('met.value', 'Giá trị', 'Value')
    for k in ('Int', 'Double', 'String'):
        m('type.' + k, k, k)
    m('val.pass', '"Đạt"', '"Pass"')
    a('cap.eval', 'Từ trái sang phải: mã nguồn, trình biên dịch suy ra kiểu, lúc chạy tính ra giá trị, biến nhận giá trị. Khối viền đỏ là chỗ kết quả gây bất ngờ dù không có lỗi nào được báo.', 'Left to right: the source, the compiler infers the type, the runtime computes the value, the variable receives it. A red-outlined box is where the result surprises you even though no error is reported.')
    S = [
        ('intdiv', 'code', 'val avg = total / 2 với total = 7 + 8', 'val avg = total / 2 with total = 7 + 8', 'Điểm trung bình của hai lượt khám. Đoán trước: avg là 7.5 hay 7?', 'The average score of two visits. Guess first: is avg 7.5 or 7?'),
        ('intdiv', 'types', 'Int / Int cho kiểu Int', 'Int / Int gives type Int', 'total là Int (7 + 8, hai literal Int), 2 là Int. Phép chia giữa hai số nguyên có kiểu Int, nên avg được suy ra là Int. Việc này xong trước khi chương trình chạy.', 'total is Int (7 + 8, two Int literals), 2 is Int. Division between two integers has type Int, so avg is inferred as Int. This is settled before the program runs.'),
        ('intdiv', 'run', '15 / 2 ra 7', '15 / 2 comes out as 7', 'Lúc chạy, phép chia nguyên bỏ phần lẻ: 15 / 2 = 7.', 'At runtime, integer division drops the fraction: 15 / 2 = 7.'),
        ('intdiv', 'result', 'avg = 7, không có lỗi nào', 'avg = 7, no error at all', 'Trình biên dịch và lúc chạy đều không báo gì: mã đúng theo luật, chỉ khác ý bạn. Đây là loại lỗi khó thấy nhất.', 'Neither the compiler nor the runtime says anything: the code follows the rules, it just differs from your intent. This is the hardest kind of bug to see.'),
        ('double', 'code', 'val avg = total / 2.0', 'val avg = total / 2.0', 'Cùng phép chia, chỉ đổi 2 thành 2.0.', 'The same division, only 2 becomes 2.0.'),
        ('double', 'types', 'Int / Double cho kiểu Double', 'Int / Double gives type Double', 'Trong biểu thức số học trộn kiểu, kết quả lấy kiểu rộng hơn: Int chia Double cho Double. avg được suy ra là Double.', 'In mixed arithmetic the result takes the wider type: Int divided by Double gives Double. avg is inferred as Double.'),
        ('double', 'run', '15 / 2.0 ra 7.5', '15 / 2.0 comes out as 7.5', 'Phép chia số thực giữ phần lẻ.', 'Floating-point division keeps the fraction.'),
        ('double', 'result', 'avg = 7.5', 'avg = 7.5', 'Muốn có phần lẻ, chỉ cần MỘT toán hạng là Double (hoặc gọi toDouble()) trước khi chia.', 'To keep the fraction, ONE operand being a Double (or calling toDouble()) before dividing is enough.'),
        ('overflow', 'code', 'val next = Int.MAX_VALUE + 1', 'val next = Int.MAX_VALUE + 1', 'Int.MAX_VALUE là 2147483647. Cộng thêm 1 thì sao?', 'Int.MAX_VALUE is 2147483647. What happens when you add 1?'),
        ('overflow', 'types', 'Int + Int cho kiểu Int', 'Int + Int gives type Int', 'Cả hai toán hạng là Int nên kết quả là Int. Trình biên dịch không đổi sang Long dù giá trị không vừa.', 'Both operands are Int, so the result is Int. The compiler does not switch to Long even though the value will not fit.'),
        ('overflow', 'run', 'Tràn: quay vòng về số âm', 'Overflow: wraps to a negative number', 'Giá trị vượt khoảng của Int nên quay vòng: kết quả là -2147483648. Không có ngoại lệ nào.', 'The value exceeds the Int range, so it wraps around: the result is -2147483648. No exception is thrown.'),
        ('overflow', 'result', 'next = -2147483648; cách sửa: toLong() trước', 'next = -2147483648; the fix: toLong() first', 'Đổi kiểu TRƯỚC khi cộng: max.toLong() + 1 là phép cộng Long, cho 2147483648. Đổi sau khi cộng thì đã muộn.', 'Convert BEFORE adding: max.toLong() + 1 is a Long addition and gives 2147483648. Converting after the addition is too late.'),
        ('when', 'code', 'val label = when (score) { … }', 'val label = when (score) { … }', 'when có subject là score = 7, ba nhánh: 9..10, 5..8, else.', 'when with subject score = 7 and three branches: 9..10, 5..8, else.'),
        ('when', 'types', 'Mọi nhánh là String → String', 'Every branch is a String → String', 'when dùng như biểu thức nên mỗi nhánh phải cho một giá trị, và các nhánh phải phủ đủ mọi trường hợp (ở đây nhờ else). Mọi nhánh là String nên label là String.', 'when is used as an expression, so every branch must produce a value and the branches must cover every case (here thanks to else). Every branch is a String, so label is a String.'),
        ('when', 'run', 'Thử nhánh theo thứ tự: 9..10 không, 5..8 có', 'Branches in order: 9..10 no, 5..8 yes', 'when so subject với từng nhánh theo thứ tự và dừng ở nhánh khớp ĐẦU TIÊN; các nhánh sau không được xét.', 'when compares the subject with each branch in order and stops at the FIRST match; later branches are not checked.'),
        ('when', 'result', 'label = "Đạt"', 'label = "Pass"', 'Giá trị của nhánh khớp là giá trị của cả biểu thức when.', 'The matching branch\'s value is the value of the whole when expression.'),
    ]
    for case, k, tv, te, xv, xe in S:
        sid = case + '.' + k
        m('s.%s.title' % sid, tv, te); m('s.%s.explain' % sid, xv, xe); m('ev.' + sid, tv, te)
    for k, vi, en in [
        ('try', 'Đổi biểu thức rồi đi lại các bước; để ý bước suy kiểu.', 'Change the expression and walk the steps again; watch the type step.'),
        ('intdiv.types', 'Tài liệu Numbers: phép chia giữa hai số nguyên luôn trả về số nguyên, phần lẻ bị bỏ. [[src:kt-numbers]]', 'The Numbers docs: division between integers always returns an integer and discards the fraction. [[src:kt-numbers]]'),
        ('intdiv.result', 'Bẫy: kết quả sai mà không có lỗi. Sửa bằng total / 2.0 hoặc total.toDouble() / 2.', 'Trap: a wrong result with no error. Fix it with total / 2.0 or total.toDouble() / 2.'),
        ('double.types', 'Tài liệu Numbers: trong biểu thức trộn kiểu số, kiểu kết quả xác định từ kiểu các toán hạng. [[src:kt-numbers]]', 'The Numbers docs: in mixed numeric expressions, the result type is determined from the operand types. [[src:kt-numbers]]'),
        ('double.result', 'Double theo chuẩn số thực nhị phân IEEE 754, nên nhiều số thập phân như 0.1 không biểu diễn chính xác. Với tiền, dùng số nguyên theo đơn vị nhỏ nhất (đồng, xu) hoặc BigDecimal. [[src:kt-numbers]]', 'Double follows the IEEE 754 binary floating-point standard, so many decimals such as 0.1 cannot be represented exactly. For money, use integers in the smallest unit (cents) or BigDecimal. [[src:kt-numbers]]'),
        ('overflow.types', 'Tài liệu Numbers: các kiểu số không phải kiểu con của nhau, và Kotlin không chuyển kiểu ngầm khi gán. [[src:kt-numbers]]', 'The Numbers docs: numeric types are not subtypes of each other, and Kotlin does no implicit conversion on assignment. [[src:kt-numbers]]'),
        ('overflow.result', 'Tài liệu Numbers: trình biên dịch không tự báo lỗi khi tràn số nguyên. [[src:kt-numbers]]', 'The Numbers docs: the compiler does not automatically report integer overflow. [[src:kt-numbers]]'),
        ('when.types', 'Tài liệu Conditions and loops: when dùng như biểu thức phải phủ đủ mọi trường hợp, nếu không trình biên dịch báo lỗi. [[src:kt-control-flow]]', 'Conditions and loops docs: a when used as an expression must cover every case, or the compiler reports an error. [[src:kt-control-flow]]'),
        ('when.result', 'Nhánh khớp đầu tiên thắng: nếu viết in 5..10 trước in 9..10 thì điểm 9 rơi vào "Đạt". Đặt nhánh hẹp trước nhánh rộng.', 'The first matching branch wins: write in 5..10 before in 9..10 and a 9 lands in "Pass". Put narrow branches before wide ones.')]:
        m('co.' + k, vi, en)

    # ---------------- chương ----------------
    C = 'k1'
    a(C + '.title', 'val, kiểu, hàm và biểu thức', 'val, types, functions and expressions')
    a(C + '.essence', 'val gán một lần, var gán lại được; val không làm object bên trong bất biến.\nKiểu được chốt lúc biên dịch: Int chia Int vẫn là Int (mất phần lẻ), Int cộng tràn vẫn là Int (quay vòng), và Kotlin không tự đổi Int sang Long hay Double.\nif và when là biểu thức trả về giá trị; when chọn nhánh khớp đầu tiên. Hàm có tham số mặc định và đối số có tên thay cho nhiều overload.',
      'val is assigned once, var can be reassigned; val does not make the object behind it immutable.\nTypes are fixed at compile time: Int divided by Int stays Int (the fraction is lost), an overflowing Int stays Int (it wraps), and Kotlin never widens Int to Long or Double on its own.\nif and when are expressions that return values; when picks the first matching branch. Functions have default parameters and named arguments instead of many overloads.')
    a(C + '.goal.g1', 'Đã xem kiểu được suy ra', 'Saw the inferred type')
    a(C + '.goal.g2', 'Đã đi hết một biểu thức', 'Walked one expression to the end')
    a(C + '.sim.kotlin.eval', 'Kiểu và giá trị', 'Type and value')

    S_ = 'hook'
    a(C + '.sec.%s.title' % S_, 'Đoán trước khi đọc', 'Predict before reading')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'predict', 'Hẹn Khám tính phần trăm lịch đã hoàn thành: `val percent = done / total * 100` với done = 3, total = 4. Màn hình hiện bao nhiêu phần trăm?',
      'ClinicBook computes the share of completed appointments: `val percent = done / total * 100` with done = 3, total = 4. What percentage does the screen show?')
    B(C, S_, 1, 'ans', '0. done và total là Int, nên 3 / 4 là phép chia nguyên và cho 0; 0 * 100 vẫn là 0. Không có lỗi biên dịch hay lỗi lúc chạy. Sửa: nhân trước rồi chia (`done * 100 / total` = 75), hoặc đổi sang Double (`done * 100.0 / total` = 75.0). Mô phỏng ngay dưới cho thấy vì sao: kiểu được chốt TRƯỚC khi tính. [[src:kt-numbers]]',
      '0. done and total are Int, so 3 / 4 is integer division and gives 0; 0 * 100 is still 0. No compile error, no runtime error. Fix: multiply first, then divide (`done * 100 / total` = 75), or switch to Double (`done * 100.0 / total` = 75.0). The simulation just below shows why: the type is fixed BEFORE the computation. [[src:kt-numbers]]')

    S_ = 'vars'
    a(C + '.sec.%s.title' % S_, 'val, var và suy kiểu', 'val, var and type inference')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'p', 'Biến khai báo bằng `val` chỉ được gán một lần; `var` gán lại được. Thói quen tốt: dùng `val` mặc định, chỉ đổi sang `var` khi thật sự cần gán lại. Kiểu thường được suy ra từ giá trị khởi tạo (`val count = 3` là Int); khi khai báo trước rồi gán sau thì phải ghi kiểu (`val count: Int`). [[src:kt-basic-syntax]]',
      'A variable declared with `val` can be assigned only once; `var` can be reassigned. A good habit: use `val` by default and switch to `var` only when you really need to reassign. The type is usually inferred from the initial value (`val count = 3` is an Int); if you declare first and assign later, you must write the type (`val count: Int`). [[src:kt-basic-syntax]]')
    B(C, S_, 2, 'kt', 'val clinic = "Hẹn Khám"      // String, suy ra từ giá trị\nvar waiting = 3              // Int\nwaiting = 4                  // được: var gán lại\n// clinic = "Khác"           // lỗi biên dịch: val không gán lại được\nval visits = mutableListOf("08:00")\nvisits.add("09:30")          // được: val không cấm sửa list bên trong',
      'val clinic = "ClinicBook"    // String, inferred from the value\nvar waiting = 3              // Int\nwaiting = 4                  // fine: var can be reassigned\n// clinic = "Other"          // compile error: val cannot be reassigned\nval visits = mutableListOf("08:00")\nvisits.add("09:30")          // fine: val does not stop the list from changing')
    B(C, S_, 3, 'note', '`val` không có nghĩa là bất biến. Nó chỉ cấm gán lại tham chiếu; object mà tham chiếu trỏ tới vẫn có thể đổi (như MutableList ở trên). Muốn dữ liệu thật sự không đổi, dùng kiểu chỉ đọc (List) và kiểu có thuộc tính val (chương K4, K7). [[src:book-effective-kotlin]]',
      '`val` does not mean immutable. It only forbids reassigning the reference; the object it points to can still change (like the MutableList above). For data that really does not change, use read-only types (List) and types with val properties (chapters K4, K7). [[src:book-effective-kotlin]]')
    B(C, S_, 3, 'kind', 'pitfall')

    S_ = 'numbers'
    a(C + '.sec.%s.title' % S_, 'Số: chia nguyên, chuyển kiểu, tràn số', 'Numbers: integer division, conversion, overflow')
    a(C + '.sec.%s.badge' % S_, 'stable impl')
    B(C, S_, 1, 'p', 'Ba luật đủ để tránh phần lớn bất ngờ với số. Một: phép chia giữa hai số nguyên trả về số nguyên, phần lẻ bị bỏ (`5 / 2` là 2); muốn phần lẻ thì một toán hạng phải là Double hoặc Float (`5 / 2.0` là 2.5). Hai: các kiểu số không phải kiểu con của nhau, nên Kotlin không tự đổi kiểu khi gán hay truyền đối số; phải gọi `toLong()`, `toDouble()`, `toInt()`. Riêng trong biểu thức số học trộn kiểu (Int + Long), kết quả lấy kiểu rộng hơn. Ba: số nguyên tràn khoảng thì quay vòng, trình biên dịch không báo lỗi. [[src:kt-numbers]]',
      'Three rules prevent most surprises with numbers. One: division between integers returns an integer and drops the fraction (`5 / 2` is 2); to keep the fraction, one operand must be a Double or Float (`5 / 2.0` is 2.5). Two: numeric types are not subtypes of each other, so Kotlin does not convert on assignment or for arguments; call `toLong()`, `toDouble()`, `toInt()`. Only in mixed arithmetic (Int + Long) does the result take the wider type. Three: an integer that overflows its range wraps around, and the compiler reports no error. [[src:kt-numbers]]')
    B(C, S_, 2, 'kt', 'val i: Int = 1\nval l: Long = 1000\nval sum = i + l              // Long: biểu thức trộn kiểu lấy kiểu rộng hơn\n// val small: Int = i + l    // lỗi biên dịch: Long không gán vào Int\nval d: Double = i.toDouble() // phải đổi tường minh\nval cut = 9.99.toInt()       // 9: phần lẻ bị bỏ khi đổi số thực sang số nguyên',
      'val i: Int = 1\nval l: Long = 1000\nval sum = i + l              // Long: mixed arithmetic takes the wider type\n// val small: Int = i + l    // compile error: a Long does not fit an Int\nval d: Double = i.toDouble() // the conversion must be explicit\nval cut = 9.99.toInt()       // 9: the fraction is dropped when converting to an integer')
    B(C, S_, 3, 'p', 'Dưới mui xe trên JVM: Kotlin coi mọi giá trị là object, nhưng trình biên dịch lưu số không-null như Int, Long, Double bằng kiểu nguyên thủy của JVM (int, long, double). Khi số là nullable (`Int?`) hoặc nằm trong kiểu generic (`List<Int>`), nó được boxing thành object. [[src:book-kt-essentials]] [[src:kt-numbers]]',
      'Under the hood on the JVM: Kotlin treats every value as an object, but the compiler stores non-null numbers such as Int, Long and Double as JVM primitives (int, long, double). When a number is nullable (`Int?`) or sits inside a generic type (`List<Int>`), it is boxed into an object. [[src:book-kt-essentials]] [[src:kt-numbers]]')
    B(C, S_, 4, 'note', 'Hệ quả của boxing: so hai `Int?` bằng `===` (cùng object) chỉ "tình cờ" đúng với số nhỏ, vì JVM cache các Integer từ -128 tới 127; với 1000 thì `===` cho false dù giá trị bằng nhau. So giá trị số luôn dùng `==`. [[src:kt-numbers]]',
      'A consequence of boxing: comparing two `Int?` values with `===` (same object) is only "accidentally" true for small numbers, because the JVM caches Integer values from -128 to 127; with 1000, `===` gives false even though the values are equal. Always compare numbers with `==`. [[src:kt-numbers]]')
    B(C, S_, 4, 'kind', 'pitfall')

    S_ = 'expr'
    a(C + '.sec.%s.title' % S_, 'if, when là biểu thức; hàm với tham số mặc định', 'if and when as expressions; functions with defaults')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'p', 'Trong Kotlin, `if` và `when` là biểu thức: chúng trả về giá trị và gán thẳng vào biến được, thay cho toán tử ba ngôi `? :` của Java. Khi dùng như biểu thức, `if` bắt buộc có `else`, và `when` phải phủ đủ mọi trường hợp. `when` so subject với từng nhánh theo thứ tự và lấy nhánh khớp đầu tiên; nhánh có thể là giá trị, khoảng (`in 5..8`) hay kiểm kiểu (`is String`). [[src:kt-control-flow]]',
      'In Kotlin, `if` and `when` are expressions: they return values you can assign directly, instead of Java\'s `? :` operator. Used as an expression, `if` must have an `else`, and `when` must cover every case. `when` checks the subject against each branch in order and takes the first match; a branch can be a value, a range (`in 5..8`) or a type check (`is String`). [[src:kt-control-flow]]')
    B(C, S_, 2, 'kt', 'fun slotLabel(minutesLeft: Int): String = when {\n    minutesLeft < 0 -> "Đã qua"\n    minutesLeft < 60 -> "Còn $minutesLeft phút"\n    else -> "Còn ${minutesLeft / 60} giờ"\n}\n\nfun book(service: String, time: String = "08:00", remind: Boolean = true) { /* … */ }\nbook("Khám tổng quát")                       // dùng giá trị mặc định\nbook("Nha khoa", remind = false)             // đối số có tên, bỏ qua time',
      'fun slotLabel(minutesLeft: Int): String = when {\n    minutesLeft < 0 -> "Past"\n    minutesLeft < 60 -> "$minutesLeft min left"\n    else -> "${minutesLeft / 60} h left"\n}\n\nfun book(service: String, time: String = "08:00", remind: Boolean = true) { /* … */ }\nbook("General check-up")                     // uses the defaults\nbook("Dental", remind = false)               // named argument, skips time')
    B(C, S_, 3, 'p', 'Hàm khai báo bằng `fun`. Hàm chỉ có một biểu thức viết gọn bằng `=` (như `slotLabel`). Hàm không trả gì có kiểu `Unit`. Tham số có giá trị mặc định giúp không phải viết nhiều overload; đối số có tên cho phép bỏ qua tham số ở giữa và làm lời gọi dễ đọc hơn. Một chi tiết hay gây nhầm: hàm override luôn dùng giá trị mặc định của hàm gốc, và không được khai báo lại giá trị mặc định. [[src:kt-functions]]',
      'Functions are declared with `fun`. A function with a single expression can be written with `=` (like `slotLabel`). A function that returns nothing has type `Unit`. Default parameter values save you from writing many overloads; named arguments let you skip parameters in the middle and make calls easier to read. A detail that often confuses: an overriding function always uses the base function\'s default values and may not redeclare them. [[src:kt-functions]]')
    B(C, S_, 4, 'p', 'Chuỗi template: `"Còn $minutesLeft phút"` chèn giá trị biến, `"${minutesLeft / 60}"` chèn cả một biểu thức. Vòng lặp `for` đi trên khoảng: `1..5` (gồm 5), `0 until 5` (không gồm 5), `10 downTo 1`, `step 2`.',
      'String templates: `"$minutesLeft min left"` inserts a variable, `"${minutesLeft / 60}"` inserts a whole expression. `for` loops walk ranges: `1..5` (includes 5), `0 until 5` (excludes 5), `10 downTo 1`, `step 2`.')

    S_ = 'bugs'
    a(C + '.sec.%s.title' % S_, 'Hai lỗi hay gặp', 'Two common bugs')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'bug', 'Thanh tiến độ "đã khám 3/4" của Hẹn Khám luôn đứng ở 0% cho tới khi khám xong hết thì nhảy lên 100%.', 'ClinicBook\'s "3 of 4 visits done" progress bar sits at 0% until every visit is done, then jumps to 100%.')
    B(C, S_, 1, 'cause', '`done / total * 100` với hai Int: `done / total` là chia nguyên, cho 0 khi done < total và 1 khi bằng nhau.', '`done / total * 100` with two Ints: `done / total` is integer division, giving 0 while done < total and 1 when they are equal.')
    B(C, S_, 1, 'fix', 'Nhân trước rồi chia (`done * 100 / total`), hoặc tính bằng Double (`done.toDouble() / total`) rồi mới định dạng.', 'Multiply first, then divide (`done * 100 / total`), or compute in Double (`done.toDouble() / total`) and format afterwards.')
    B(C, S_, 2, 'bug', 'Kiểm tra "mã phòng khám đã chọn có trùng mã trong lịch không" bằng `selected === booked` (hai `Int?`) chạy đúng khi thử với mã 12, nhưng sai với mã 1024.', 'The check "is the selected clinic id the same as the booked one" uses `selected === booked` (two `Int?` values); it works when tested with id 12 but fails with id 1024.')
    B(C, S_, 2, 'cause', '`Int?` được boxing; `===` so sánh object chứ không so giá trị. JVM cache Integer từ -128 tới 127 nên số nhỏ "tình cờ" cùng object; 1024 thì không.', '`Int?` is boxed; `===` compares objects, not values. The JVM caches Integer values from -128 to 127, so small numbers are "accidentally" the same object; 1024 is not.')
    B(C, S_, 2, 'fix', 'Dùng `==` (so giá trị). Chỉ dùng `===` khi thật sự muốn hỏi "có phải cùng một object không".', 'Use `==` (compares values). Use `===` only when you really mean "is this the same object".')

    S_ = 'ex'
    a(C + '.sec.%s.title' % S_, 'Bài tập', 'Exercise')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'ex', 'Hẹn Khám cần hiện thời gian còn lại tới giờ hẹn. Viết `fun timeLeftLabel(seconds: Int): String` trả về dạng "X h Y min Z sec", bỏ những phần bằng 0; trả về "Now" khi seconds bằng 0 và "Invalid input" khi âm. Ví dụ: 45 → "45 sec", 150 → "2 min 30 sec", 3600 → "1 h", 3665 → "1 h 1 min 5 sec". (Dựa trên bài "Pretty time display" của Kotlin Exercises, diễn đạt lại.) [[src:book-kt-exercises]]',
      'ClinicBook needs to show the time left until an appointment. Write `fun timeLeftLabel(seconds: Int): String` that returns "X h Y min Z sec", leaving out the parts equal to 0; return "Now" when seconds is 0 and "Invalid input" when it is negative. Examples: 45 → "45 sec", 150 → "2 min 30 sec", 3600 → "1 h", 3665 → "1 h 1 min 5 sec". (Based on the "Pretty time display" exercise in Kotlin Exercises, restated.) [[src:book-kt-exercises]]')
    B(C, S_, 1, 'hint', 'Giờ là `seconds / 3600` (chia nguyên ở đây là đúng ý), phút là `seconds % 3600 / 60`, giây là `seconds % 60`. Dùng `when` cho hai trường hợp đặc biệt.', 'Hours are `seconds / 3600` (integer division is exactly what you want here), minutes `seconds % 3600 / 60`, seconds `seconds % 60`. Use `when` for the two special cases.')
    B(C, S_, 1, 'sol', 'Một lời giải: ghép các phần khác 0 vào một danh sách rồi nối bằng khoảng trắng. Để ý chia nguyên ở đây là chủ đích, khác với lỗi thanh tiến độ.', 'One solution: collect the non-zero parts in a list and join them with spaces. Note that integer division is intended here, unlike the progress-bar bug.')
    B(C, S_, 1, 'solkt', 'fun timeLeftLabel(seconds: Int): String = when {\n    seconds < 0 -> "Invalid input"\n    seconds == 0 -> "Now"\n    else -> {\n        val h = seconds / 3600\n        val m = seconds % 3600 / 60\n        val s = seconds % 60\n        listOf(h to "h", m to "min", s to "sec")\n            .filter { it.first > 0 }\n            .joinToString(" ") { "${it.first} ${it.second}" }\n    }\n}')

    S_ = 'recall'
    a(C + '.sec.%s.title' % S_, 'Tự trả lời', 'Answer it yourself')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'ask', '`val price = 10 / 4` có kiểu gì và giá trị bao nhiêu? Sửa thế nào để được 2.5?', 'What type and value does `val price = 10 / 4` have? How do you get 2.5?')
    B(C, S_, 1, 'ans', 'Int, giá trị 2 (chia nguyên). Viết `10 / 4.0` hoặc `10.toDouble() / 4`.', 'Int, value 2 (integer division). Write `10 / 4.0` or `10.toDouble() / 4`.')
    B(C, S_, 2, 'ask', 'Vì sao `val list = mutableListOf(1)` vẫn thêm phần tử được?', 'Why can `val list = mutableListOf(1)` still get new elements?')
    B(C, S_, 2, 'ans', 'val chỉ cấm gán lại biến list; object MutableList mà nó trỏ tới vẫn sửa được.', 'val only forbids reassigning the variable; the MutableList object it points to can still be changed.')

    S_ = 'honest'
    a(C + '.sec.%s.title' % S_, 'Chương này giản lược những gì', 'What this chapter simplifies')
    a(C + '.sec.%s.badge' % S_, 'simplified')
    B(C, S_, 1, 'p', 'Giá trị trong mô phỏng và trong các đoạn mã là kết quả tài liệu Kotlin nêu, không phải mã chạy trong trang. Phần "dưới mui xe" về kiểu nguyên thủy và boxing theo tài liệu Numbers và sách Kotlin Essentials; site chưa tự biên dịch và xem bytecode. Chương chỉ dạy phần cú pháp cần cho các chương sau, không thay một khóa học lập trình nhập môn.',
      'The values in the simulation and the code samples are the results stated by the Kotlin docs, not code running in the page. The "under the hood" part on primitives and boxing follows the Numbers docs and the Kotlin Essentials book; the site has not compiled code and inspected the bytecode itself. The chapter only teaches the syntax later chapters need; it does not replace an introductory programming course.')

    for q, qv, qe, av, ae, wv, we in [
        ('q1', '`5 / 2` trong Kotlin bằng bao nhiêu?', 'What is `5 / 2` in Kotlin?', '2.', '2.', 'Chia giữa hai số nguyên bỏ phần lẻ.', 'Division between integers drops the fraction.'),
        ('q2', 'Có gán được một Int vào biến kiểu Long mà không gọi hàm đổi kiểu không?', 'Can you assign an Int to a Long variable without a conversion call?', 'Không.', 'No.', 'Kotlin không chuyển kiểu số ngầm khi gán; gọi `toLong()`.', 'Kotlin does no implicit numeric conversion on assignment; call `toLong()`.'),
        ('q3', '`Int.MAX_VALUE + 1` có ném ngoại lệ không?', 'Does `Int.MAX_VALUE + 1` throw an exception?', 'Không, kết quả là -2147483648.', 'No, the result is -2147483648.', 'Số nguyên tràn thì quay vòng; trình biên dịch không báo.', 'An overflowing integer wraps around; the compiler reports nothing.'),
        ('q4', 'Hai nhánh của when cùng khớp thì nhánh nào được chọn?', 'If two when branches both match, which one is chosen?', 'Nhánh viết trước.', 'The one written first.', 'when dừng ở nhánh khớp đầu tiên.', 'when stops at the first matching branch.')]:
        a(C + '.quiz.%s.q' % q, qv, qe); a(C + '.quiz.%s.a' % q, av, ae); a(C + '.quiz.%s.why' % q, wv, we)
