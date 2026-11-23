# Kotlin · K0: bản đồ track (viết CUỐI, đặt đầu track). Chỉ tổng hợp K1–K13; mọi khẳng định có nguồn ở chương tương ứng.

SEC_ORDER = {'k0': ['hook', 'order', 'index', 'bridges', 'honest']}

CH = [
    ('k1', 'val, kiểu, hàm và biểu thức', 'val, types, functions and expressions'),
    ('k2', 'Null safety, smart cast và platform type', 'Null safety, smart casts and platform types'),
    ('k3', 'Class, interface, object và thứ tự khởi tạo', 'Classes, interfaces, objects and initialization order'),
    ('k4', 'Data class và bằng nhau', 'Data classes and equality'),
    ('k5', 'Enum, sealed và when', 'Enums, sealed types and when'),
    ('k6', 'Ngoại lệ, require/check và use', 'Exceptions, require/check and use'),
    ('k7', 'Collection: read-only, mutable và xử lý', 'Collections: read-only, mutable and processing'),
    ('k8', 'Lambda, closure và inline', 'Lambdas, closures and inline'),
    ('k9', 'Sequence và hiệu năng', 'Sequences and performance'),
    ('k10', 'Generics và variance', 'Generics and variance'),
    ('k11', 'Ủy quyền: by lazy, by remember, by viewModels', 'Delegation: by lazy, by remember, by viewModels'),
    ('k12', 'Scope function và DSL', 'Scope functions and DSLs'),
    ('k13', 'Java interop và dưới mui xe', 'Java interop and under the hood'),
]

# (id, triệu chứng vi/en, chi tiết vi/en, cơ chế vi/en, cơ chế chi tiết vi/en, cách sửa vi/en)
SYM = [
    ('intDiv', 'Điểm trung bình ra 7 thay vì 7.5', 'The average comes out as 7 instead of 7.5',
     'Không lỗi, không cảnh báo; con số chỉ sai.', 'No error, no warning; the number is just wrong.',
     'Int chia Int là chia nguyên', 'Int divided by Int is integer division',
     'Kiểu của biểu thức được quyết định lúc biên dịch: hai toán hạng Int cho kết quả Int, phần lẻ bị bỏ.', 'The expression\'s type is decided at compile time: two Int operands give an Int, and the fraction is dropped.',
     'Đổi một toán hạng sang Double (total / 2.0 hay total.toDouble() / n).', 'Make one operand a Double (total / 2.0 or total.toDouble() / n).'),
    ('smartCast', '"Smart cast to String is impossible"', 'The "Smart cast to String is impossible" error',
     'Đã kiểm != null ngay dòng trên mà trình biên dịch vẫn không cho dùng.', 'You checked != null on the line above, yet the compiler still refuses.',
     'Biến có thể đổi giữa lúc kiểm và lúc dùng', 'The variable could change between check and use',
     'Smart cast chỉ chạy khi trình biên dịch chứng minh được biến không đổi: var property, property open hay có getter tự viết, var bị lambda sửa thì không.', 'A smart cast only works when the compiler can prove the variable does not change: not for a var property, an open property or one with a custom getter, or a var modified by a lambda.',
     'Chép vào một val cục bộ rồi kiểm, hoặc dùng ?.let.', 'Copy into a local val and check that, or use ?.let.'),
    ('initNpe', 'NPE trong constructor dù property khai báo non-null', 'An NPE in a constructor although the property is non-null',
     'Crash khi tạo object, ở lớp cha, trỏ tới một property của lớp con.', 'A crash while creating the object, in the parent class, pointing at a child property.',
     'Lớp cha gọi hàm open trong init', 'The parent calls an open function in init',
     'Lớp cha khởi tạo trước lớp con; hàm open bị override chạy khi property của lớp con chưa được gán.', 'The parent initialises before the child; the overridden open function runs before the child\'s properties are assigned.',
     'Không gọi thành viên open trong khởi tạo của lớp cha; chuyển việc đó ra sau khi tạo xong.', 'Do not call open members during parent initialisation; move that work to after construction.'),
    ('hashLost', 'Phần tử "biến mất" khỏi HashSet sau khi sửa', 'An element "disappears" from a HashSet after being modified',
     'contains trả false dù object vẫn nằm trong set.', 'contains returns false though the object is still in the set.',
     'hashCode đổi theo property var', 'hashCode changes with a var property',
     'Data class tính hashCode từ property trong constructor chính; sửa một var làm đổi hashCode, nên tra cứu tìm sai bucket.', 'A data class computes hashCode from its primary constructor properties; changing a var changes the hashCode, so lookups go to the wrong bucket.',
     'Dùng val cho property tham gia equals/hashCode; muốn đổi thì xóa, copy rồi thêm lại.', 'Use val for properties taking part in equals/hashCode; to change one, remove, copy and add back.'),
    ('elseBranch', 'Trạng thái mới hiện thông báo lỗi chung', 'A new state shows the generic error message',
     'Thêm một kiểu con mới, không có lỗi biên dịch nào, nhưng màn hình xử lý sai.', 'A new subtype was added with no compile error, but the screen handles it wrongly.',
     'else nuốt kiểu con mới', 'else swallows the new subtype',
     'when trên sealed hay enum có else thì luôn phủ đủ, nên trình biên dịch không nhắc chỗ cần thêm nhánh.', 'A when over a sealed or enum type with else is always exhaustive, so the compiler never points at the branches to add.',
     'Bỏ else, liệt kê đủ nhánh để trình biên dịch báo mọi chỗ thiếu.', 'Drop else and list every branch so the compiler flags every gap.'),
    ('swallowed', 'Màn hình trống, không crash, không log', 'An empty screen, no crash, no log',
     'Dữ liệu có vấn đề nhưng app im lặng hiện "không có gì".', 'The data is wrong but the app silently shows "nothing".',
     'catch quá rộng nuốt lỗi', 'An overly broad catch swallows the error',
     'catch (e: Exception) hay runCatching bắt cả lỗi bạn cần thấy và biến nó thành kết quả rỗng.', 'catch (e: Exception) or runCatching also catches the errors you need to see and turns them into an empty result.',
     'Chỉ bắt loại ngoại lệ xử lý được, ghi log, và trả trạng thái lỗi rõ ràng.', 'Catch only the types you can handle, log them, and return an explicit error state.'),
    ('listChanged', 'Màn hình không cập nhật sau khi thêm dữ liệu', 'The screen does not refresh after data is added',
     'Một List "read-only" lại đổi theo, và so sánh trước/sau luôn bằng nhau.', 'A "read-only" List changes along with it, and before/after comparisons are always equal.',
     'Hai tham chiếu tới cùng một MutableList', 'Two references to the same MutableList',
     'List chỉ cấm sửa qua tham chiếu đó; object bên dưới vẫn là MutableList mà nơi khác đang sửa.', 'List only forbids changes through that reference; the object underneath is still a MutableList being changed elsewhere.',
     'Lộ ra bản chụp (toList) hoặc thay cả list thay vì sửa tại chỗ.', 'Expose a snapshot (toList) or replace the whole list instead of modifying it in place.'),
    ('forEachReturn', 'Code sau forEach không chạy', 'The code after forEach never runs',
     'Vòng lặp dừng ở phần tử đầu tiên khớp điều kiện, và phần sau của hàm bị bỏ.', 'The loop stops at the first matching element, and the rest of the function is skipped.',
     'return trong lambda inline thoát cả hàm', 'A return inside an inline lambda exits the whole function',
     'forEach là inline nên return trần là non-local return, thoát hàm bao ngoài chứ không chỉ bỏ qua phần tử.', 'forEach is inline, so a bare return is a non-local return that exits the enclosing function, not just the element.',
     'Dùng return@forEach (giống continue) hoặc vòng for.', 'Use return@forEach (like continue) or a for loop.'),
    ('seqNothing', 'Chuỗi asSequence() không làm gì cả', 'An asSequence() chain does nothing at all',
     'Hàm chạy không lỗi nhưng tác dụng phụ (gửi tin, ghi log) không xảy ra.', 'The function runs without errors but its side effects (sending, logging) never happen.',
     'Sequence thiếu thao tác cuối', 'The Sequence has no terminal operation',
     'Thao tác trung gian của Sequence chỉ dựng chuỗi; chỉ thao tác cuối (toList, forEach…) mới làm nó chạy.', 'Intermediate Sequence operations only build the chain; only a terminal operation (toList, forEach…) makes it run.',
     'Kết thúc bằng forEach hay toList; đặt tác dụng phụ trong forEach.', 'End with forEach or toList; put side effects in forEach.'),
    ('castLater', 'ClassCastException ở một dòng chỉ đọc list', 'A ClassCastException on a line that only reads a list',
     'Lỗi nổ ra xa chỗ dữ liệu sai được tạo.', 'The error explodes far from where the bad data was created.',
     'Ép kiểu generic không được kiểm, hay lách variance', 'An unchecked generic cast, or working around variance',
     'Kiểu tham số bị xóa lúc chạy, nên as List<Doctor> không kiểm phần tử; ép MutableList để lách bất biến cho phép ghi sai kiểu.', 'Type arguments are erased at runtime, so as List<Doctor> does not check elements; casting a MutableList to dodge invariance lets wrong types in.',
     'Kiểm từng phần tử (filterIsInstance), khai báo List<out> hay MutableList<in> đúng chỗ.', 'Check elements (filterIsInstance), and declare List<out> or MutableList<in> where they belong.'),
    ('lazyTwice', 'Hai object được tạo dù dùng by lazy', 'Two objects get created despite by lazy',
     'Thỉnh thoảng có hai kết nối cơ sở dữ liệu, khó tái hiện.', 'Now and then there are two database connections, hard to reproduce.',
     'lazy(NONE) được đọc từ nhiều luồng', 'lazy(NONE) read from several threads',
     'NONE không đồng bộ; khi hai luồng đọc lần đầu cùng lúc, cả hai có thể chạy initializer.', 'NONE does not synchronize; when two threads read it first at the same time, both may run the initializer.',
     'Dùng lazy mặc định (SYNCHRONIZED) cho thứ có thể đọc từ nhiều luồng.', 'Use the default lazy (SYNCHRONIZED) for anything read from several threads.'),
    ('applyNested', 'Thuộc tính của object bên ngoài bị đổi trong apply', 'An outer object\'s property changes inside apply',
     'Tiêu đề lịch hẹn thành "Bà" sau khi tạo bệnh nhân.', 'The booking title becomes "Mrs" after creating the patient.',
     'Tên được hiểu theo receiver bên ngoài', 'A name resolves against the outer receiver',
     'Trong apply lồng nhau, tên không có ở receiver gần nhất được tìm ra receiver bên ngoài, mà không có lỗi.', 'In nested apply calls, a name missing on the nearest receiver is looked up on outer receivers, with no error.',
     'Tránh lồng; dùng also { p -> } hay ghi rõ this@nhãn; với DSL dùng @DslMarker.', 'Avoid nesting; use also { p -> } or an explicit this@label; for DSLs use @DslMarker.'),
    ('javaCall', 'Mã Java không gọi được hàm Kotlin như mong đợi', 'Java code cannot call a Kotlin function as expected',
     'SlotFormatter.format(9) hay book(9) không biên dịch trong Java.', 'SlotFormatter.format(9) or book(9) does not compile in Java.',
     'Java chỉ thấy những gì trình biên dịch sinh ra', 'Java sees only what the compiler generates',
     'Companion thành object Companion, tham số mặc định chỉ còn chữ ký đầy đủ, tham số non-null có kiểm tra lúc chạy.', 'A companion becomes a Companion object, default parameters leave only the full signature, and non-null parameters get runtime checks.',
     'Thêm @JvmStatic, @JvmOverloads, @JvmField, @file:JvmName hay khai báo kiểu nullable khi null hợp lệ.', 'Add @JvmStatic, @JvmOverloads, @JvmField, @file:JvmName, or declare a nullable type when null is valid.'),
]


def add(a):
    def B(ch, sec, n, field, vi, en=None):
        a('%s.sec.%s.b.%02d.%s' % (ch, sec, n, field), vi, vi if en is None else en)

    m = lambda k, vi, en=None: a('m.map.' + k, vi, en)
    m('title', 'Gặp triệu chứng này thì đọc chương nào', 'Which chapter to read for this symptom')
    m('overview', 'Chọn một triệu chứng hay gặp khi viết Kotlin trên Android. Mô phỏng đi qua bốn bước: lỗi lộ ra lúc nào (biên dịch, lúc chạy, hay sai mà không báo gì), cơ chế gây ra nó, và chương giải thích cơ chế đó.',
      'Pick a symptom you often meet writing Kotlin on Android. The simulation walks four steps: when the problem shows up (compile time, runtime, or silently wrong), the mechanism behind it, and the chapter that explains that mechanism.')
    m('wrapup', 'Phần lớn lỗi Kotlin khó thấy thuộc loại "sai mà không báo gì": chia nguyên, else nuốt kiểu con, catch quá rộng, return trong forEach, Sequence thiếu thao tác cuối, apply lồng. Biết cơ chế là cách nhanh nhất để nhận ra chúng. Mỗi chương có một mô phỏng, hai lỗi thật, một bài tập và quiz.',
      'Most hard-to-see Kotlin bugs are "silently wrong": integer division, else swallowing a subtype, an overly broad catch, return inside forEach, a Sequence missing its terminal operation, nested apply. Knowing the mechanism is the fastest way to spot them. Every chapter has a simulation, two real bugs, an exercise and a quiz.')
    m('simp.1', 'Mỗi triệu chứng chỉ trỏ tới một chương chính; một lỗi thật có thể liên quan nhiều chương.', 'Each symptom points to one main chapter; a real bug may involve several.')
    m('ctl.hint', 'Đổi triệu chứng; để ý "lúc xảy ra": nhiều lỗi khó nhất không có lỗi biên dịch hay crash nào.', 'Change the symptom; watch "when it shows up": many of the hardest bugs have no compile error and no crash.')
    m('ctl.symptom', 'Triệu chứng', 'Symptom')
    for row in SYM:
        m('ctl.symptom.' + row[0], row[1], row[2])
    m('diagramTitle', 'Triệu chứng, lúc xảy ra, cơ chế, chương', 'Symptom, when it shows, mechanism, chapter')
    m('diagramDesc', 'Từ một triệu chứng tới lúc nó lộ ra, cơ chế gây ra nó, và chương cần đọc', 'From a symptom to when it shows up, the mechanism behind it, and the chapter to read')
    for k, vi, en in [('symptom', 'Triệu chứng', 'Symptom'), ('phase', 'Lộ ra lúc nào', 'When it shows up'), ('cause', 'Cơ chế gây ra', 'Mechanism behind it'), ('chapter', 'Chương cần đọc', 'Chapter to read')]:
        m('n.' + k, vi, en)
    m('met.phase', 'Lộ ra lúc', 'Shows up'); m('met.chapter', 'Chương', 'Chapter')
    for k, vi, en, xv, xe in [
        ('none', 'chưa xét', 'not yet', '', ''),
        ('compile', 'Lỗi lúc biên dịch', 'A compile-time error', 'Trình biên dịch từ chối mã. Đây là loại dễ nhất: nó chỉ đúng chỗ, và đọc thông báo lỗi cùng cơ chế là biết sửa.', 'The compiler rejects the code. This is the easiest kind: it points at the exact spot, and the message plus the mechanism tell you the fix.'),
        ('runtime', 'Lỗi lúc chạy', 'A runtime error', 'Mã biên dịch được nhưng ném ngoại lệ khi chạy. Stack trace cho biết chỗ nổ, nhưng nguyên nhân có thể ở chỗ khác.', 'The code compiles but throws at runtime. The stack trace shows where it blew up, but the cause may be elsewhere.'),
        ('silent', 'Sai mà không báo gì', 'Silently wrong', 'Không lỗi biên dịch, không crash, chỉ có kết quả sai. Đây là loại khó nhất, và là lý do track này dạy cơ chế.', 'No compile error, no crash, just a wrong result. This is the hardest kind, and the reason this track teaches mechanisms.')]:
        m('phase.' + k, vi, en)
        if xv:
            m('phase.%s.explain' % k, xv, xe)
    m('ch.none', 'chưa xác định', 'not decided yet')
    for cid, tv, te in CH:
        m('ch.' + cid, '%s · %s' % (cid.upper(), tv), '%s · %s' % (cid.upper(), te))
        m('go.' + cid, 'Đọc chương %s: %s' % (cid.upper(), tv), 'Read chapter %s: %s' % (cid.upper(), te))
    for row in SYM:
        i, tv, te, dv, de, cv, ce, cdv, cde, fv, fe = row
        m('s.%s.title' % i, tv, te); m('s.%s.detail' % i, dv, de)
        m('s.%s.cause' % i, cv, ce); m('s.%s.causeDetail' % i, cdv, cde); m('s.%s.fix' % i, fv, fe)
    m('co.try', 'Đổi triệu chứng ở ô phía trên rồi đi lại bốn bước.', 'Change the symptom in the box above and walk the four steps again.')
    m('co.cause', 'Đây là cơ chế, không phải lỗi gõ: sửa đúng chỗ này thì cả nhóm lỗi tương tự cũng hết.', 'This is a mechanism, not a typo: fixing it at this level removes the whole family of similar bugs.')
    m('co.chapter', 'Mở chương này ở mục lục bên trái; mô phỏng của chương đi qua đúng tình huống trên.', 'Open this chapter in the left-hand contents; its simulation walks through exactly this situation.')
    a('cap.map', 'Từ trái sang phải: triệu chứng bạn thấy, lúc nó lộ ra (biên dịch, lúc chạy, hay sai lặng lẽ), cơ chế gây ra nó, và chương cần đọc. Khối viền đỏ là chỗ lỗi xuất hiện.', 'Left to right: the symptom you see, when it shows up (compile time, runtime, or silently wrong), the mechanism behind it, and the chapter to read. A red-outlined box is where the problem appears.')

    C = 'k0'
    a(C + '.title', 'Bản đồ track: triệu chứng và chương', 'Track map: symptoms and chapters')
    a(C + '.essence', 'Track gồm hai phần. Phần 1 (K1–K7) là nền tảng cho người mới: kiểu, null, class, data class, sealed, ngoại lệ, collection. Phần 2 (K8–K13) đi vào cơ chế: lambda và inline, sequence, variance, delegate, scope function, Java interop.\nMỗi chương bắt đầu từ một lỗi thật trên Android, có một mô phỏng, hai lỗi hay gặp, một bài tập, câu tự trả lời và quiz.\nNếu đang gặp một lỗi cụ thể, dùng mô phỏng bên dưới để tìm chương.',
      'The track has two parts. Part 1 (K1–K7) is the foundation for newcomers: types, null, classes, data classes, sealed types, exceptions, collections. Part 2 (K8–K13) goes into mechanisms: lambdas and inline, sequences, variance, delegates, scope functions, Java interop.\nEvery chapter starts from a real Android bug and has a simulation, two common bugs, an exercise, self-check questions and a quiz.\nIf you are facing a specific bug, use the simulation below to find the chapter.')
    a(C + '.goal.g1', 'Đã thấy lỗi lộ ra lúc nào', 'Saw when the problem shows up')
    a(C + '.goal.g2', 'Đã tới chương cần đọc', 'Reached the chapter to read')
    a(C + '.sim.kotlin.map', 'triệu chứng → chương', 'symptom → chapter')

    S_ = 'hook'
    a(C + '.sec.%s.title' % S_, 'Đoán trước khi đọc', 'Predict before reading')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'predict', 'Trong 13 triệu chứng của mô phỏng ngay dưới, bạn đoán bao nhiêu cái KHÔNG có lỗi biên dịch cũng không crash, chỉ cho kết quả sai?', 'Of the 13 symptoms in the simulation just below, how many do you think give NO compile error and NO crash, just a wrong result?')
    B(C, S_, 1, 'ans', 'Tám: chia nguyên, phần tử mất khỏi HashSet, else nuốt kiểu con, catch quá rộng, List đổi theo, return trong forEach, Sequence thiếu thao tác cuối, apply lồng. Đó là lý do track dạy cơ chế: những lỗi này không tự báo.', 'Eight: integer division, an element lost from a HashSet, else swallowing a subtype, an overly broad catch, a List changing underneath, return inside forEach, a Sequence missing its terminal operation, nested apply. That is why the track teaches mechanisms: these bugs do not announce themselves.')

    S_ = 'order'
    a(C + '.sec.%s.title' % S_, 'Thứ tự đọc', 'Reading order')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'p', 'Người mới đọc theo thứ tự K1 → K13. Phần 1 (K1–K7) đủ để đọc và viết mã Kotlin của một app Android thông thường. Phần 2 (K8–K13) cần cho ai làm việc với Coroutines, Compose hay mã Java cũ, vì các track đó dựa trên lambda inline, delegate và variance. Đã biết Kotlin thì có thể đi thẳng tới chương có triệu chứng mình đang gặp.',
      'Newcomers read in order, K1 → K13. Part 1 (K1–K7) is enough to read and write the Kotlin of an ordinary Android app. Part 2 (K8–K13) matters for anyone working with Coroutines, Compose or old Java code, because those tracks build on inline lambdas, delegates and variance. If you already know Kotlin, jump straight to the chapter for the symptom you are facing.')

    S_ = 'index'
    a(C + '.sec.%s.title' % S_, 'Chỉ mục: cơ chế theo chương', 'Index: mechanisms by chapter')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'p', '• K1: kiểu suy ra lúc biên dịch, chia nguyên, tràn số, if/when là biểu thức.\n• K2: smart cast và điều kiện của nó, platform type từ Java.\n• K3: thứ tự khởi tạo cha/con, object và companion khởi tạo khi nào, lateinit.\n• K4: equals/hashCode của data class, copy nông, HashSet.\n• K5: enum, sealed, when phủ đủ, valueOf.\n• K6: ngoại lệ lan qua chuỗi gọi, try là biểu thức, require/check, use.\n• K7: read-only không phải bất biến, bản chụp, map trên Map.',
      '• K1: types inferred at compile time, integer division, overflow, if/when as expressions.\n• K2: smart casts and their conditions, platform types from Java.\n• K3: parent/child initialization order, when objects and companions initialize, lateinit.\n• K4: data class equals/hashCode, shallow copy, HashSet.\n• K5: enums, sealed types, exhaustive when, valueOf.\n• K6: exceptions travelling up the call chain, try as an expression, require/check, use.\n• K7: read-only is not immutable, snapshots, map over a Map.')
    B(C, S_, 2, 'p', '• K8: lambda inline hay object hàm, non-local return, closure giữ object.\n• K9: List háo hức, Sequence lười, thao tác cuối.\n• K10: out, in, bất biến, type erasure.\n• K11: by và getValue, ba chế độ lazy, by remember, by viewModels.\n• K12: scope function, receiver lồng nhau, @DslMarker.\n• K13: Kotlin nhìn từ Java, @JvmStatic, @JvmOverloads, kiểm null lúc chạy.',
      '• K8: inline lambdas versus function objects, non-local return, closures holding objects.\n• K9: eager Lists, lazy Sequences, terminal operations.\n• K10: out, in, invariant, type erasure.\n• K11: by and getValue, the three lazy modes, by remember, by viewModels.\n• K12: scope functions, nested receivers, @DslMarker.\n• K13: Kotlin as seen from Java, @JvmStatic, @JvmOverloads, runtime null checks.')

    S_ = 'bridges'
    a(C + '.sec.%s.title' % S_, 'Cầu nối sang các track khác', 'Bridges to the other tracks')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'p', '• Coroutines: suspend lambda và coroutineScope dựa trên lambda (K8); Flow<out T> hiệp biến (K10); catch rộng nuốt cả CancellationException (K6); thu thập Flow theo vòng đời thay cho callback giữ Activity (K8).\n• Compose Runtime: by remember dùng State.getValue (K11); UiState sealed với when phủ đủ (K5); UiState<out T> với Loading : UiState<Nothing> (K10).\n• Mọi track: data class làm state phải bất biến (K4, K7).',
      '• Coroutines: suspend lambdas and coroutineScope build on lambdas (K8); Flow<out T> is covariant (K10); a broad catch also swallows CancellationException (K6); collecting a Flow with the lifecycle instead of a callback holding an Activity (K8).\n• Compose Runtime: by remember uses State.getValue (K11); a sealed UiState with an exhaustive when (K5); UiState<out T> with Loading : UiState<Nothing> (K10).\n• Every track: data classes used as state should be immutable (K4, K7).')

    S_ = 'honest'
    a(C + '.sec.%s.title' % S_, 'Track này nói thật tới đâu', 'How far this track\'s claims go')
    a(C + '.sec.%s.badge' % S_, 'simplified')
    B(C, S_, 1, 'p', 'Mọi mô phỏng là mô hình giảng dạy có nhãn giản lược; site không chạy hay biên dịch Kotlin trong trang. Quy tắc ngôn ngữ theo tài liệu kotlinlang.org đọc ngày 2026-11-23; chi tiết bên trong ghim mã stdlib tag v2.1.0, kotlinx.coroutines 1.9.0 và androidx-main commit 296313a4. Máy viết track không có kotlinc hay javap, nên mọi khẳng định về bytecode lấy từ tài liệu hay sách và được ghi là giản lược. Sách (Kotlin Essentials, Effective Kotlin, Functional Kotlin, Advanced Kotlin, Kotlin Exercises) là nguồn giảng dạy phụ; khi lệch với tài liệu chính thức, chương theo tài liệu và ghi rõ.',
      'Every simulation is a teaching model labelled as simplified; the site neither runs nor compiles Kotlin in the page. Language rules follow the kotlinlang.org docs as read on 2026-11-23; internal details are pinned to the stdlib at tag v2.1.0, kotlinx.coroutines 1.9.0 and androidx-main commit 296313a4. The machine that wrote this track had no kotlinc or javap, so every bytecode claim comes from the docs or books and is marked simplified. The books (Kotlin Essentials, Effective Kotlin, Functional Kotlin, Advanced Kotlin, Kotlin Exercises) are secondary teaching sources; where they differ from the official docs, the chapter follows the docs and says so.')

    for q, qv, qe, av, ae, wv, we in [
        ('q1', 'Code sau forEach không chạy: đọc chương nào?', 'The code after forEach never runs: which chapter?', 'K8.', 'K8.', 'return trong lambda inline là non-local return.', 'A return inside an inline lambda is a non-local return.'),
        ('q2', 'Phần tử biến mất khỏi HashSet sau khi sửa: đọc chương nào?', 'An element disappears from a HashSet after a change: which chapter?', 'K4.', 'K4.', 'hashCode đổi theo property var.', 'hashCode changes with a var property.'),
        ('q3', 'Hai kết nối được tạo dù dùng by lazy: đọc chương nào?', 'Two connections get created despite by lazy: which chapter?', 'K11.', 'K11.', 'Chế độ NONE với nhiều luồng.', 'NONE mode with several threads.')]:
        a(C + '.quiz.%s.q' % q, qv, qe); a(C + '.quiz.%s.a' % q, av, ae); a(C + '.quiz.%s.why' % q, wv, we)
