# Lập trình hàm · K2 (p2): bất biến, dữ liệu dùng chung, đệ quy và tailrec (Phần 1: nền tảng)
# Nguồn (chỉ ghi ở đây và docs/research/fp.md): Carli, FP in Kotlin by Tutorials ch.6–7 (Challenge 6.1); Vermeulen, Bjarnason, Chiusano,
# FP in Kotlin ch.2–3 (3.3, 3.3.1, Exercise 3.9); tài liệu Kotlin Functions (Tail recursive functions). Giọng văn dạy học (2026-11-24).

SEC_ORDER = {'p2': ['hook', 'immut', 'share', 'recursion', 'tailrec', 'bugs', 'ex']}


def add(a):
    def B(ch, sec, n, field, vi, en=None):
        a('%s.sec.%s.b.%02d.%s' % (ch, sec, n, field), vi, vi if en is None else en)

    a('preset.persist', 'Lập trình hàm · dữ liệu dùng chung và tailrec', 'Functional programming · data sharing and tailrec')
    m = lambda k, vi, en=None: a('m.persist.' + k, vi, en)
    m('title', 'Sửa tại chỗ hay dùng chung đuôi; đệ quy thường hay tailrec', 'Mutate in place or share the tail; plain recursion or tailrec')
    m('overview', 'Mô phỏng này trả lời hai câu hỏi riêng. Bước 1–2: màn "Chọn lịch để hủy" lấy danh sách lịch đã đặt làm gốc, thêm một lịch rồi bỏ một lịch. Liệu danh sách gốc có bị đổi theo? Bước 3–4: báo cáo cuối năm cộng phí của 50.000 lịch hẹn bằng đệ quy. Liệu app có chạy hết, hay crash giữa chừng?',
      'This simulation answers two separate questions. Steps 1–2: the "Pick bookings to cancel" screen starts from the booked list, adds one booking, then drops one. Does the original list change too? Steps 3–4: the year-end report adds up the fees of 50,000 bookings with recursion. Does the app finish, or crash halfway?')
    m('wrapup', 'Khi hai cái tên cùng trỏ vào một MutableList, sửa qua tên này là tên kia đổi theo. List persistent thì khác: thêm vào đầu chỉ tạo đúng một ô mới, phần còn lại dùng chung, và danh sách gốc không bao giờ bị đụng tới. Ở nửa sau, đệ quy thường để lại một "việc chờ" cho mỗi phần tử nên tràn stack; viết lại với biến tích lũy và tailrec thì chỉ cần một chỗ trên stack, cộng hết cả 50.000 lịch.',
      'When two names point at one MutableList, changing it through one changes the other. A persistent list is different: adding at the front creates exactly one new cell, the rest is shared, and the original is never touched. In the second half, plain recursion leaves one "pending job" per element and overflows the stack; rewritten with an accumulator and tailrec, it needs a single spot on the stack and adds up all 50,000 bookings.')
    m('simp.1', 'Giới hạn 10.000 tầng stack chỉ là con số ví dụ; trên máy thật nó tùy kích thước stack và từng hàm.',
      'The 10,000-level stack limit is just an example figure; on a real device it depends on the stack size and on each function.')
    m('simp.2', 'Danh sách FList được viết tay để thấy rõ ô nào dùng chung; app thật thường dùng List có sẵn của Kotlin.',
      'FList is hand-written so you can see which cells are shared; real apps usually use Kotlin\'s built-in List.')
    m('ctl.hint', 'Có hai nút chọn độc lập: "Cách giữ danh sách" đổi bước 1–2, "Cách đệ quy" đổi bước 3–4.', 'There are two independent choices: "List kept as" changes steps 1–2, "Recursion" changes steps 3–4.')
    m('ctl.list', 'Cách giữ danh sách', 'List kept as')
    m('ctl.list.mutable', 'một MutableList, hai cái tên', 'one MutableList, two names'); m('ctl.list.persistent', 'list persistent dùng chung đuôi', 'a persistent list sharing its tail')
    m('ctl.rec', 'Cách đệ quy', 'Recursion')
    m('ctl.rec.plain', 'đệ quy thường', 'plain recursion'); m('ctl.rec.tailrec', 'biến tích lũy + tailrec', 'accumulator + tailrec')
    m('diagramTitle', 'Hai danh sách dùng chung dữ liệu; hàm đệ quy và stack', 'Two lists sharing data; a recursive function and the stack')
    m('diagramDesc', 'Dùng chung an toàn khi không ai sửa được; đệ quy an toàn khi lời gọi là việc cuối cùng', 'Sharing is safe when nobody can change the data; recursion is safe when the call is the last thing done')
    for k, vi, en in [('selected', 'Danh sách đã chọn', 'Selected list'), ('booked', 'Lịch đã đặt', 'Booked list'), ('fold', 'Hàm cộng phí', 'Fee sum'), ('stack', 'Stack của luồng', 'Thread stack')]:
        m('n.' + k, vi, en)
    m('met.touched', 'Lần danh sách gốc bị đổi', 'Times the original changed'); m('met.nodes', 'Ô mới tạo', 'New cells created'); m('met.depth', 'Stack sâu nhất', 'Deepest stack')
    a('cap.persist', 'Hàng trên: danh sách đã chọn trỏ vào danh sách gốc. Hàng dưới: hàm cộng phí dùng stack. Ô đỏ: danh sách gốc bị đổi ngoài ý muốn, hoặc stack sâu tới mức tràn.',
      'Top row: the selected list points into the original. Bottom row: the fee sum uses the stack. A red box: the original changed by accident, or the stack is deep enough to overflow.')
    S = [
        ('mutable', 's1', 'Thêm b4 qua selected = booked', 'Add b4 through selected = booked',
         'Màn chọn lịch viết val selected = booked, rồi selected.add(b4). Trông như ta có hai danh sách, nhưng thật ra chỉ có một, với hai cái tên. Giống hai người cùng giữ chìa khóa một cái tủ: ai bỏ đồ vào thì người kia mở ra cũng thấy. Vì vậy booked cũng có b4.',
         'The picker screen writes val selected = booked, then selected.add(b4). It looks like two lists, but there is really one, with two names. Like two people holding keys to the same cupboard: whatever one puts in, the other sees too. So booked gets b4 as well.'),
        ('mutable', 's2', 'Bỏ lịch đầu của selected', 'Drop the first booking of selected',
         'selected.removeAt(0) bỏ b1 khỏi danh sách đã chọn. Vì chỉ có một danh sách, lịch đã đặt cũng mất b1. Cả hai lần sửa qua selected đều "lọt" sang booked.',
         'selected.removeAt(0) drops b1 from the selected list. Since there is only one list, the booked list loses b1 too. Both changes made through selected "leak" into booked.'),
        ('persistent', 's1', 'Thêm b4 vào đầu: Cons(b4, booked)', 'Add b4 at the front: Cons(b4, booked)',
         'Với list persistent, thêm vào đầu là tạo đúng một ô mới chứa b4, và cho ô đó trỏ vào booked. Ba ô cũ không bị chép, chỉ được dùng chung. booked vẫn là b1, b2, b3 như trước.',
         'With a persistent list, adding at the front creates exactly one new cell holding b4 and points it at booked. The three old cells are not copied, just shared. booked is still b1, b2, b3.'),
        ('persistent', 's2', 'Bỏ phần tử đầu: selected.tail', 'Drop the first element: selected.tail',
         'Bỏ phần tử đầu chỉ là lấy phần đuôi: không tạo ô mới nào, và phần đuôi chính là booked. Không có gì bị xóa thật; bản cũ vẫn nguyên vẹn và dùng được. Vì giữ được mọi bản cũ nên cấu trúc này được gọi là persistent.',
         'Dropping the first element just takes the tail: no new cell, and the tail is booked itself. Nothing is really deleted; the old version stays intact and usable. Because every old version survives, the structure is called persistent.'),
        ('plain', 's3', 'Cộng phí 50.000 lịch: việc chờ chồng chất', 'Summing 50,000 fees: pending jobs pile up',
         'total(xs) = phí đầu + total(phần còn lại). Phép cộng chỉ làm được khi lời gọi bên trong đã trả về, nên mỗi phần tử để lại một "việc chờ" trên stack, như xếp chồng đĩa chưa rửa. Đi qua 5.000 phần tử là 5.001 việc đang chờ.',
         'total(xs) = first fee + total(the rest). The addition can only happen once the inner call returns, so each element leaves a "pending job" on the stack, like a pile of unwashed plates. After 5,000 elements there are 5,001 jobs waiting.'),
        ('plain', 's4', 'Tới phần tử thứ 10.000: StackOverflowError', 'At element 10,000: StackOverflowError',
         'Chồng việc chờ cao quá giới hạn 10.000 (con số ví dụ) và app crash trước khi kịp cộng phép nào. Báo cáo một tháng chỉ vài trăm lịch nên vẫn chạy; lỗi chỉ lộ ra khi gặp dữ liệu cả năm.',
         'The pile of pending jobs passes the limit of 10,000 (an example figure) and the app crashes before a single addition. A monthly report has only a few hundred bookings and works; the bug only shows with a whole year of data.'),
        ('tailrec', 's3', 'Mang tổng theo và dùng tailrec: một tầng stack', 'Carry the total along with tailrec: one stack level',
         'Viết lại: total(phần còn lại, tổng đến giờ + phí đầu). Giờ lời gọi là việc cuối cùng; khi nó trả về thì không còn gì phải làm. Gắn tailrec, trình biên dịch đổi đệ quy thành vòng lặp, nên stack luôn chỉ sâu 1.',
         'Rewritten: total(the rest, total so far + first fee). Now the call is the last thing done; once it returns there is nothing left to do. With tailrec, the compiler turns the recursion into a loop, so the stack stays 1 level deep.'),
        ('tailrec', 's4', 'Đi hết 50.000 lịch: 10.000.000.000 đ', 'All 50,000 bookings: 10,000,000,000 VND',
         'Ở mọi mốc, stack vẫn chỉ sâu 1. Tổng phí là 50.000 × 200.000 đ = 10.000.000.000 đ. Với List thường của Kotlin, xs.sumOf { it.fee } cho cùng kết quả và vốn đã chạy bằng vòng lặp.',
         'At every mark the stack is still 1 level deep. The total is 50,000 × 200,000 VND = 10,000,000,000 VND. With Kotlin\'s ordinary List, xs.sumOf { it.fee } gives the same result and already runs as a loop.'),
    ]
    for case, k, tv, te, xv, xe in S:
        sid = case + '.' + k
        m('s.%s.title' % sid, tv, te); m('s.%s.explain' % sid, xv, xe); m('ev.' + sid, tv, te)
    for k, vi, en in [
        ('try', 'Mẹo đọc: bước 1–2 nhìn bảng danh sách phía trên, bước 3–4 nhìn hàng độ sâu stack phía dưới.', 'Reading tip: for steps 1–2 watch the list table above, for steps 3–4 the stack depth row below.'),
        ('mutable.s2', 'Nhớ câu này: val cố định cái tên, không cố định đồ vật. val không cho gán tên sang object khác, nhưng object vẫn sửa được nếu kiểu của nó cho sửa. [[src:book-fp-tut]]',
         'Remember: val fixes the name, not the thing. val stops you pointing the name at another object, but the object can still change if its type allows it. [[src:book-fp-tut]]'),
        ('persistent.s1', 'Vì không ai sửa được list, dùng chung phần đuôi là hoàn toàn an toàn. Kỹ thuật này gọi là dùng chung dữ liệu (data sharing). [[src:book-fp-manning]]',
         'Because nobody can change the list, sharing the tail is perfectly safe. This technique is called data sharing. [[src:book-fp-manning]]'),
        ('persistent.s2', 'Ba chữ hay đi cùng nhau: bất biến (tạo xong là không đổi), persistent (giữ được mọi bản cũ), và hàm (chỉ thao tác bằng hàm thuần, xem chương "Hàm thuần và referential transparency"). [[src:book-fp-tut]] [[src:book-fp-manning]]',
         'Three words often go together: immutable (unchanged once created), persistent (keeps every old version), and functional (handled only with pure functions, see the chapter "Pure functions and referential transparency"). [[src:book-fp-tut]] [[src:book-fp-manning]]'),
        ('plain.s3', 'Một lời gọi ở "vị trí đuôi" khi sau nó hàm không còn làm gì nữa, chỉ trả kết quả. phí + total(...) không phải vị trí đuôi, vì còn phép cộng chờ sau. [[src:book-fp-manning]]',
         'A call is in "tail position" when the function does nothing after it except return the result. fee + total(...) is not, because an addition is still waiting. [[src:book-fp-manning]]'),
        ('plain.s4', 'Kiểu đệ quy "cộng sau khi gọi" luôn có nguy cơ tràn stack với dữ liệu lớn. Ví dụ quen thuộc: hàm gộp từ phải (foldRight) viết bằng đệ quy thường thì tràn với danh sách dài, còn hàm gộp từ trái (foldLeft) viết theo tailrec thì không. [[src:book-fp-manning]]',
         'Recursion that "adds after calling" always risks overflowing the stack on large data. A familiar example: folding from the right (foldRight) written with plain recursion overflows on long lists, while folding from the left (foldLeft) written with tailrec does not. [[src:book-fp-manning]]'),
        ('tailrec.s3', 'Theo tài liệu Kotlin, chỉ gắn tailrec được khi hàm gọi lại chính nó như việc cuối cùng; không dùng được khi còn mã sau lời gọi, khi lời gọi nằm trong try/catch/finally, hay khi hàm là open. [[src:kt-functions]]',
         'Per the Kotlin docs, tailrec only applies when the function calls itself as the very last thing; not when code follows the call, when the call sits inside try/catch/finally, or when the function is open. [[src:kt-functions]]'),
        ('tailrec.s4', 'Bên dưới, hàm tailrec được dịch thành một vòng while, không còn lời gọi đệ quy nào. Nhưng Kotlin chỉ làm vậy khi bạn ghi rõ chữ tailrec; thiếu chữ đó, dù lời gọi đã ở vị trí đuôi, stack vẫn chồng lên. [[src:book-fp-tut]] [[src:book-fp-manning]]',
         'Under the hood, a tailrec function compiles to a while loop with no recursive call left. But Kotlin only does this when you write tailrec; without it, even a call in tail position still piles up on the stack. [[src:book-fp-tut]] [[src:book-fp-manning]]'),
    ]:
        m('co.' + k, vi, en)

    z = lambda k, vi, en=None: a('vz.' + k, vi, en)
    z('tab.persist', 'Ô danh sách và độ sâu stack', 'List cells and stack depth')
    z('persist.cap', 'Mỗi ô là một phần tử của danh sách. Viền: ô vừa tạo hay vừa thêm. Đậm: ô dùng chung với booked. Gạch đỏ: booked bị đổi ngoài ý muốn.', 'Each cell is one element of a list. Outlined: a cell just created or added. Bold: a cell shared with booked. Red hatched: booked changed by accident.')
    z('persist.scap', 'Stack sâu bao nhiêu sau khi đi qua từng ấy phần tử trong {n} lịch hẹn. Giới hạn ví dụ: {lim} tầng.', 'How deep the stack is after visiting that many of the {n} bookings. Example limit: {lim} levels.')
    z('persist.legend', 'Ô "?": chưa tới bước đó. Đỏ: sâu quá nửa giới hạn, hay tràn stack. Đậm: chỉ 1 tầng (đã thành vòng lặp).', '"?": that step has not come yet. Red: deeper than half the limit, or an overflow. Bold: just 1 level (now a loop).')
    for k, vi, en in [('name', 'Tên', 'Name'), ('ref', 'Là gì', 'What it is'), ('nodes', 'Các ô', 'Cells'), ('seen', 'Đã đi qua', 'Elements visited')]:
        z('persist.col.' + k, vi, en)
    for k, vi, en in [('leak', 'lọt sang', 'leaked in'), ('new', 'mới', 'new'), ('shared', 'dùng chung', 'shared'), ('lost', 'mất', 'lost')]:
        z('persist.chip.' + k, vi, en)
    for k, vi, en in [('booked', 'danh sách lịch đã đặt', 'the booked list'), ('selected', 'Cons(b4, booked): một ô mới và phần đuôi cũ', 'Cons(b4, booked): one new cell and the old tail'),
                      ('alias', 'cùng một danh sách với booked', 'the same list as booked'), ('tail', 'selected.tail: chính là booked', 'selected.tail: booked itself')]:
        z('persist.ref.' + k, vi, en)
    z('persist.rec.plain', 'đệ quy thường', 'plain recursion'); z('persist.rec.tailrec', 'biến tích lũy + tailrec', 'accumulator + tailrec')
    z('persist.crash', 'tràn', 'overflow'); z('persist.skip', 'không tới', 'not reached')
    z('persist.result.crash', 'StackOverflowError ở phần tử thứ {n}: chưa cộng được phép nào.', 'StackOverflowError at element {n}: not a single addition done.')
    z('persist.result.ok', 'Tổng phí: {t} đ; stack luôn chỉ sâu 1.', 'Total fees: {t} VND; the stack is always 1 level deep.')
    z('persist.result.none', 'Hàm cộng phí chưa chạy (bước 3–4).', 'The fee sum has not run yet (steps 3–4).')

    C = 'p2'
    a(C + '.title', 'Bất biến, dữ liệu dùng chung và đệ quy', 'Immutability, data sharing and recursion')
    a(C + '.essence', 'val cố định cái tên, không cố định đồ vật. Hai cái tên cùng trỏ vào một MutableList thì sửa qua tên này, tên kia đổi theo.\nDanh sách persistent không bao giờ sửa tại chỗ: thêm vào đầu chỉ tạo một ô mới và dùng chung phần còn lại; bỏ phần tử đầu chỉ là lấy phần đuôi. Bản cũ còn nguyên, nên không cần chép phòng xa.\nĐệ quy thường để lại một việc chờ cho mỗi lời gọi và tràn stack với dữ liệu lớn. Mang kết quả theo qua tham số để lời gọi là việc cuối cùng, rồi gắn tailrec: Kotlin đổi nó thành vòng lặp.',
      'val fixes the name, not the thing. When two names point at one MutableList, a change through one shows up in the other.\nA persistent list never changes in place: adding at the front creates one new cell and shares the rest; dropping the first element just takes the tail. The old version stays intact, so there is no need to copy just in case.\nPlain recursion leaves a pending job for every call and overflows the stack on large data. Carry the result along in a parameter so the call is the last thing done, then mark it tailrec: Kotlin turns it into a loop.')
    a(C + '.goal.g1', 'Đã thấy danh sách gốc có bị đổi theo không', 'Saw whether the original list changed')
    a(C + '.goal.g2', 'Đã thấy stack tràn hay chỉ một tầng', 'Saw the stack overflow or stay at one level')
    a(C + '.sim.fp.persist', 'dữ liệu dùng chung và độ sâu stack', 'data sharing and stack depth')

    S_ = 'hook'
    a(C + '.sec.%s.title' % S_, 'Đoán trước khi đọc', 'Predict before reading')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'predict', 'Màn "Chọn lịch để hủy" có dòng val selected = booked, trong đó booked là MutableList. Người dùng bỏ chọn một lịch, rồi quay lại tab "Lịch đã đặt". Họ sẽ thấy gì?',
      'The "Pick bookings to cancel" screen has val selected = booked, where booked is a MutableList. The user unselects a booking, then goes back to the "Booked" tab. What will they see?')
    B(C, S_, 1, 'ans', 'Lịch vừa bỏ chọn cũng biến mất khỏi "Lịch đã đặt". Lý do: chỉ có một danh sách, mang hai cái tên. val không làm danh sách trở nên bất biến; nó chỉ cấm gán tên đó sang danh sách khác.',
      'The booking just unselected has vanished from "Booked" too. The reason: there is only one list, with two names. val does not make the list immutable; it only forbids pointing that name at another list.')

    S_ = 'immut'
    a(C + '.sec.%s.title' % S_, 'Bất biến khác hằng', 'Immutable is not constant')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'p', 'Hai từ này hay bị dùng lẫn, nhưng nói về hai thứ khác nhau. "Hằng" nói về cái tên: tên đã gắn vào một object thì không gắn lại được. "Bất biến" nói về object: tạo xong là nội dung không bao giờ đổi. Trong Kotlin, val cho bạn hằng. Còn bất biến thì phụ thuộc vào kiểu của object. [[src:book-fp-tut]]',
      'These two words are often mixed up, but they are about different things. "Constant" is about the name: once a name is attached to an object it cannot be re-attached. "Immutable" is about the object: once created, its contents never change. In Kotlin, val gives you a constant. Immutability depends on the object\'s type. [[src:book-fp-tut]]')
    B(C, S_, 2, 'kt', 'val user = MutableUser("An")\n// user = MutableUser("Bình")   // không được: val không cho gán lại\nuser.name = "Bình"               // được: object vẫn sửa được\n\ndata class Patient(val name: String, val birth: java.util.Date)\n// mọi thuộc tính đều là val, nhưng birth.time = 0 vẫn đổi được ngày sinh',
      'val user = MutableUser("An")\n// user = MutableUser("Binh")   // not allowed: val forbids reassigning\nuser.name = "Binh"               // allowed: the object can still change\n\ndata class Patient(val name: String, val birth: java.util.Date)\n// every property is val, yet birth.time = 0 still changes the birth date')
    B(C, S_, 3, 'p', 'Ví dụ thứ hai hay bị bỏ sót: data class toàn val vẫn có thể bị đổi nếu một thuộc tính có kiểu sửa được, như java.util.Date. List của Kotlin cũng vậy: nó chỉ "chỉ đọc" qua giao diện, chưa phải bất biến thật (chương K7, "Collection: read-only, mutable và xử lý", của track Kotlin có mô phỏng riêng). [[src:book-fp-tut]]',
      'The second example is easy to miss: an all-val data class can still change if one property has a mutable type, like java.util.Date. Kotlin\'s List is similar: it is only "read-only" through its interface, not truly immutable (chapter K7, "Collections: read-only, mutable and processing", of the Kotlin track has its own simulation). [[src:book-fp-tut]]')
    B(C, S_, 4, 'p', 'Vì sao nên chuộng bất biến? Object không đổi thì dễ hiểu hơn, dùng làm khóa (key) của Map an toàn (key bị sửa làm Map hỏng, như ở chương K4, "Data class và bằng nhau", của track Kotlin), và nhiều luồng cùng đọc mà không cần khóa đồng bộ (lock). Quy tắc ngón tay cái: mặc định cho bất biến, chỉ cho sửa khi có lý do rõ ràng. [[src:book-fp-tut]]',
      'Why prefer immutability? An object that never changes is easier to understand, safe as a Map key (a changed key breaks the Map, as in chapter K4, "Data classes and equality", of the Kotlin track), and readable by many threads without locks. Rule of thumb: make things immutable by default, and mutable only for a clear reason. [[src:book-fp-tut]]')

    S_ = 'share'
    a(C + '.sec.%s.title' % S_, 'Dùng chung dữ liệu và danh sách persistent', 'Data sharing and persistent lists')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'p', 'Nếu không được sửa tại chỗ, làm sao thêm hay bớt phần tử? Hãy nghĩ tới một đoàn tàu. Muốn có đoàn tàu dài hơn một toa, ta không đóng lại cả đoàn; ta chỉ móc thêm một toa mới vào đầu. Danh sách persistent làm đúng vậy: Cons(x, xs) tạo một ô mới chứa x và trỏ vào xs. Đoàn tàu cũ vẫn nguyên, và cả hai cùng dùng chung các toa phía sau. [[src:book-fp-manning]]',
      'If you may not change things in place, how do you add or remove elements? Think of a train. To get a train one carriage longer, you do not rebuild the whole train; you hook a new carriage on the front. A persistent list does exactly that: Cons(x, xs) creates one new cell holding x and points it at xs. The old train is untouched, and both share the carriages behind. [[src:book-fp-manning]]')
    B(C, S_, 2, 'p', 'Bỏ toa đầu cũng không cần phá gì: chỉ cần nhìn từ toa thứ hai trở đi, tức là lấy phần đuôi (tail). Vì không ai sửa được dữ liệu, dùng chung là an toàn tuyệt đối. Ngược lại, với dữ liệu sửa được, mỗi nơi nhận nó thường phải tự chép một bản "phòng khi ai đó sửa", và chương trình càng lớn càng tốn. [[src:book-fp-manning]]',
      'Dropping the front carriage does not break anything either: you just look from the second carriage on, taking the tail. Since nobody can change the data, sharing is completely safe. With mutable data, by contrast, every place that receives it often makes its own copy "in case someone changes it", and the bigger the program, the more that costs. [[src:book-fp-manning]]')
    B(C, S_, 3, 'note', 'Không phải phép nào cũng rẻ. Nối hai danh sách chỉ chép các ô của danh sách thứ nhất; nhưng bỏ phần tử cuối thì phải chép mọi ô đứng trước, vì muốn đổi toa cuối phải đóng lại cả đoàn phía trước nó. List thường của Kotlin lại là mảng: list + x tạo một list mới và chép hết mọi phần tử. [[src:book-fp-manning]]',
      'Not every operation is cheap. Joining two lists copies only the cells of the first one; but dropping the last element means copying every cell before it, because changing the last carriage means rebuilding everything in front. Kotlin\'s ordinary List is an array instead: list + x builds a new list and copies every element. [[src:book-fp-manning]]')
    B(C, S_, 3, 'kind', 'mechanism')

    S_ = 'recursion'
    a(C + '.sec.%s.title' % S_, 'Đệ quy thay vòng lặp, và cái giá của nó', 'Recursion instead of loops, and its cost')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'p', 'Khi không muốn dùng biến sửa được, ta lặp bằng đệ quy: thay vì tăng một biến trong vòng for, hàm gọi lại chính nó với giá trị mới làm tham số. Cách này gọn, nhưng có một cái giá. Mỗi lời gọi còn đang chờ kết quả chiếm một tầng trên stack, giống như chồng đĩa: đĩa dưới chỉ được rửa khi mọi đĩa trên đã xong. [[src:book-fp-tut]]',
      'When you do not want mutable variables, you loop with recursion: instead of bumping a variable in a for loop, the function calls itself with the new value as a parameter. It is neat, but there is a cost. Each call still waiting for a result takes one level of the stack, like a pile of plates: the bottom plate gets washed only after every plate above it is done. [[src:book-fp-tut]]')
    B(C, S_, 2, 'p', 'Đoạn dưới đây tính tay cho danh sách 3 lịch. Với đệ quy thường, các phép cộng phải chờ tới đáy rồi mới tính ngược lên. Với biến tích lũy, tổng được mang theo ngay, nên không có gì phải chờ.',
      'The code below works it out by hand for a list of 3 bookings. With plain recursion, the additions wait until the bottom and then work back up. With an accumulator, the total is carried along at once, so nothing waits.')
    B(C, S_, 3, 'kt', '// đệ quy thường: các phép cộng chờ ở mỗi tầng\ntotal([b1, b2, b3])\n= 200_000 + total([b2, b3])\n= 200_000 + (200_000 + total([b3]))\n= 200_000 + (200_000 + (200_000 + total(Nil)))   // 4 tầng đang chờ\n= 600_000\n\n// biến tích lũy: không gì phải chờ\ntotal([b1, b2, b3], 0)\n= total([b2, b3], 200_000)\n= total([b3], 400_000)\n= total(Nil, 600_000) = 600_000',
      '// plain recursion: the additions wait at every level\ntotal([b1, b2, b3])\n= 200_000 + total([b2, b3])\n= 200_000 + (200_000 + total([b3]))\n= 200_000 + (200_000 + (200_000 + total(Nil)))   // 4 levels waiting\n= 600_000\n\n// accumulator: nothing waits\ntotal([b1, b2, b3], 0)\n= total([b2, b3], 200_000)\n= total([b3], 400_000)\n= total(Nil, 600_000) = 600_000')

    S_ = 'tailrec'
    a(C + '.sec.%s.title' % S_, 'Vị trí đuôi và tailrec', 'Tail position and tailrec')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'p', 'Một lời gọi ở "vị trí đuôi" khi nó là việc cuối cùng của hàm: gọi xong là trả kết quả, không cộng, không nhân gì thêm. Khi mọi lời gọi đệ quy đều ở vị trí đuôi, không còn việc nào phải chờ, nên không cần giữ tầng stack cũ. [[src:book-fp-manning]]',
      'A call is in "tail position" when it is the very last thing the function does: once it returns, the result goes straight out, with no adding or multiplying afterwards. When every recursive call is in tail position, no job is waiting, so the old stack level is not needed. [[src:book-fp-manning]]')
    B(C, S_, 2, 'p', 'Kotlin không tự nhận ra điều đó; bạn phải ghi chữ tailrec trước hàm. Khi đủ điều kiện, trình biên dịch đổi đệ quy thành vòng lặp. Tài liệu Kotlin nêu ba trường hợp không dùng được: còn mã chạy sau lời gọi, lời gọi nằm trong try/catch/finally, và hàm là open. [[src:kt-functions]]',
      'Kotlin does not notice this on its own; you must write tailrec before the function. When the conditions hold, the compiler turns the recursion into a loop. The Kotlin docs list three cases where it cannot be used: code runs after the call, the call sits inside try/catch/finally, and the function is open. [[src:kt-functions]]')
    B(C, S_, 3, 'p', 'Cách viết lại hay gặp nhất: thêm một tham số tích lũy (thường đặt tên acc) mang kết quả từng phần đi theo. Quy tắc ngón tay cái: nếu thấy "x + f(...)" hay "x * f(...)", hãy chuyển x vào tham số để f(...) đứng một mình ở cuối. [[src:book-fp-manning]] [[src:book-fp-tut]]',
      'The most common rewrite: add an accumulator parameter (often named acc) that carries the partial result along. Rule of thumb: when you see "x + f(...)" or "x * f(...)", move x into a parameter so f(...) stands alone at the end. [[src:book-fp-manning]] [[src:book-fp-tut]]')
    B(C, S_, 4, 'note', 'Chữ tailrec không phải là bảo đảm. Nếu hàm không có lời gọi đuôi nào, trình biên dịch chỉ cảnh báo chứ không báo lỗi. Hãy đọc từng lời gọi. Trong mã app hằng ngày, cách đơn giản nhất thường là dùng sẵn sumOf hay fold của List, vốn đã chạy bằng vòng lặp. [[src:book-fp-manning]]',
      'The word tailrec is not a guarantee. If the function has no tail call at all, the compiler only warns instead of failing. Read each call. In everyday app code, the simplest route is usually the List\'s own sumOf or fold, which already run as loops. [[src:book-fp-manning]]')
    B(C, S_, 4, 'kind', 'pitfall')

    S_ = 'bugs'
    a(C + '.sec.%s.title' % S_, 'Hai lỗi hay gặp', 'Two common bugs')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'bug', 'Ở màn "Chọn lịch để hủy", bỏ chọn một lịch làm lịch đó biến khỏi danh sách lịch đã đặt.', 'On the "Pick bookings to cancel" screen, unselecting a booking makes it vanish from the booked list.')
    B(C, S_, 1, 'cause', 'val selected = booked với booked là MutableList: chỉ có một danh sách mang hai tên, nên removeAt qua selected cũng sửa booked.', 'val selected = booked where booked is a MutableList: there is one list with two names, so removeAt through selected changes booked too.')
    B(C, S_, 1, 'fix', 'Giữ danh sách bằng List (hoặc cấu trúc persistent) và tạo danh sách mới mỗi khi đổi (filter, minus, Cons). Đừng chuyền một MutableList dùng chung qua nhiều màn hình.', 'Keep lists as List (or a persistent structure) and build a new list on every change (filter, minus, Cons). Do not pass one shared MutableList across screens.')
    B(C, S_, 2, 'bug', 'Xuất báo cáo cả năm (50.000 lịch hẹn) làm app crash với StackOverflowError, trong khi báo cáo một tháng vẫn chạy.', 'Exporting the yearly report (50,000 bookings) crashes with StackOverflowError, while the monthly report works.')
    B(C, S_, 2, 'cause', 'Hàm cộng phí đệ quy còn phép cộng sau lời gọi, nên mỗi phần tử để lại một tầng trên stack. Vài trăm tầng thì vừa; vài chục nghìn thì tràn.', 'The recursive fee sum still adds after the call, so each element leaves a level on the stack. A few hundred levels fit; tens of thousands overflow.')
    B(C, S_, 2, 'fix', 'Viết lại với biến tích lũy và gắn tailrec, hoặc dùng sumOf có sẵn. Thêm một bài test với danh sách đủ lớn để bắt lỗi trước khi phát hành.', 'Rewrite with an accumulator and tailrec, or use the built-in sumOf. Add a test with a large enough list to catch it before release.')

    S_ = 'ex'
    a(C + '.sec.%s.title' % S_, 'Bài tập', 'Exercise')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'ex', 'Hàm dưới đây đã gắn tailrec. Trình biên dịch có biến cả hàm thành vòng lặp không? Hãy viết lại cho đúng.',
      'The function below is marked tailrec. Does the compiler turn the whole function into a loop? Rewrite it properly.')
    B(C, S_, 1, 'exkt', 'tailrec fun countPaid(xs: FList<Booking>): Int = when (xs) {\n    Nil -> 0\n    is Cons -> if (xs.head.paid) 1 + countPaid(xs.tail) else countPaid(xs.tail)\n}')
    B(C, S_, 1, 'hint', 'Với từng lời gọi đệ quy, hỏi: khi nó trả về, hàm còn phải làm gì nữa không?', 'For each recursive call, ask: once it returns, is there anything left for the function to do?')
    B(C, S_, 1, 'sol', 'Không. Ở nhánh paid, phép "1 +" còn chờ sau lời gọi, nên lời gọi đó không ở vị trí đuôi. Với một năm toàn lịch đã trả, stack vẫn chồng lên. Thêm biến tích lũy để nhánh nào cũng kết thúc bằng chính lời gọi.',
      'No. In the paid branch, the "1 +" is still waiting after the call, so that call is not in tail position. Over a year of paid bookings the stack still piles up. Add an accumulator so every branch ends with the call itself.')
    B(C, S_, 1, 'solkt', 'tailrec fun countPaid(xs: FList<Booking>, acc: Int = 0): Int = when (xs) {\n    Nil -> acc\n    is Cons -> countPaid(xs.tail, if (xs.head.paid) acc + 1 else acc)\n}')

    for q, qv, qe, av, ae, wv, we in [
        ('q1', 'booked là MutableList; val selected = booked; selected.add(b4). booked có đổi không?', 'booked is a MutableList; val selected = booked; selected.add(b4). Does booked change?', 'Có.', 'Yes.', 'Chỉ có một danh sách mang hai tên; val cố định cái tên, không cố định đồ vật.', 'There is one list with two names; val fixes the name, not the thing.'),
        ('q2', 'Thêm b4 vào đầu một danh sách persistent 3 phần tử tạo ra bao nhiêu ô mới?', 'How many new cells does adding b4 to the front of a 3-element persistent list create?', 'Một.', 'One.', 'Ô mới trỏ vào danh sách cũ; 3 ô cũ được dùng chung.', 'The new cell points at the old list; the 3 old cells are shared.'),
        ('q3', 'Lời gọi trong xs.head.fee + total(xs.tail) có ở vị trí đuôi không?', 'Is the call in xs.head.fee + total(xs.tail) in tail position?', 'Không.', 'No.', 'Khi nó trả về, hàm còn phải cộng thêm xs.head.fee.', 'Once it returns, the function still has to add xs.head.fee.'),
        ('q4', 'Hàm có try/catch bao quanh lời gọi đệ quy có dùng tailrec được không?', 'Can a function with try/catch around its recursive call use tailrec?', 'Không.', 'No.', 'Tài liệu Kotlin ghi rõ try/catch/finally là một trong những chỗ không dùng được.', 'The Kotlin docs state that try/catch/finally is one of the places it cannot be used.')]:
        a(C + '.quiz.%s.q' % q, qv, qe); a(C + '.quiz.%s.a' % q, av, ae); a(C + '.quiz.%s.why' % q, wv, we)
