# Lập trình hàm · K2 (p2): bất biến, dữ liệu dùng chung, đệ quy và tailrec (Phần 1: nền tảng)
# Nguồn: Massimo Carli, FP in Kotlin by Tutorials ch.6 (bất biến khác hằng, data class toàn val chưa đủ, lợi ích của bất biến, đệ quy,
# tailrec thành vòng while, Challenge 6.1), ch.7 (immutable, functional, persistent); Vermeulen, Bjarnason, Chiusano, FP in Kotlin ch.2
# (tail call, tailrec, cảnh báo khi không có lời gọi đuôi), ch.3 (3.3 data sharing, persistent, pessimistic copying, append, init, Exercise 3.9);
# tài liệu Kotlin Functions (Tail recursive functions). Đọc 2026-11-24, diễn đạt lại; ví dụ viết lại theo app Hẹn Khám.

SEC_ORDER = {'p2': ['hook', 'immut', 'share', 'recursion', 'tailrec', 'bugs', 'ex', 'honest']}


def add(a):
    def B(ch, sec, n, field, vi, en=None):
        a('%s.sec.%s.b.%02d.%s' % (ch, sec, n, field), vi, vi if en is None else en)

    a('preset.persist', 'Lập trình hàm · dữ liệu dùng chung và tailrec', 'Functional programming · data sharing and tailrec')
    m = lambda k, vi, en=None: a('m.persist.' + k, vi, en)
    m('title', 'Sửa tại chỗ hay dùng chung đuôi; đệ quy thường hay tailrec', 'Mutate in place or share the tail; plain recursion or tailrec')
    m('overview', 'Hai câu hỏi độc lập trên app Hẹn Khám. Bước 1–2: màn "Chọn lịch để hủy" tạo danh sách đã chọn từ danh sách lịch đã đặt, thêm một lịch rồi bỏ lịch đầu; giữ bằng một MutableList mang hai tên, hay bằng list persistent dùng chung đuôi. Bước 3–4: báo cáo cả năm cộng phí 50.000 lịch hẹn bằng đệ quy thường, hay bằng tham số tích lũy và tailrec.',
      'Two independent questions on the ClinicBook app. Steps 1–2: the "Pick bookings to cancel" screen builds a selected list from the booked list, adds one booking, then drops the first; kept as one MutableList with two names, or as a persistent list sharing its tail. Steps 3–4: the yearly report sums the fees of 50,000 bookings with plain recursion, or with an accumulator and tailrec.')
    m('wrapup', 'MutableList mang hai tên: không tạo nút nào, nhưng thêm và bỏ qua selected đều lọt sang booked. List persistent: thêm vào đầu tạo 1 nút, 3 nút đuôi dùng chung; bỏ phần tử đầu tạo 0 nút và trả về chính booked; booked không đổi. Đệ quy thường giữ một khung cho mỗi phần tử và tràn ở phần tử thứ 10.000 (giới hạn minh họa); tailrec giữ 1 khung và cộng đủ 10.000.000.000 đ.',
      'One MutableList with two names: no node is created, yet both the add and the drop through selected leak into booked. The persistent list: adding at the front creates 1 node and shares the 3 tail nodes; dropping the first creates 0 nodes and returns booked itself; booked never changes. Plain recursion holds one frame per element and overflows at element 10,000 (an illustrative limit); tailrec holds 1 frame and sums all 10,000,000,000 VND.')
    m('simp.1', 'Giới hạn 10.000 khung là con số minh họa; độ sâu thật tùy kích thước stack của luồng và của mỗi khung. FList tự viết để thấy nút dùng chung; 50.000 lịch và phí 200.000 đ là của site.',
      'The 10,000-frame limit is illustrative; the real depth depends on the thread\'s stack size and the size of each frame. FList is hand-written to make shared nodes visible; the 50,000 bookings and the 200,000 VND fee are the site\'s.')
    m('simp.2', 'Hai nửa của chương độc lập: cách giữ danh sách không ảnh hưởng tới độ sâu stack. Chúng đi cùng nhau vì một lý do: không sửa tại chỗ thì lặp bằng đệ quy, và đệ quy trên dữ liệu lớn cần tailrec.',
      'The two halves of the chapter are independent: how the list is kept does not affect stack depth. They belong together for one reason: without in-place mutation you loop by recursion, and recursion over large data needs tailrec.')
    m('ctl.hint', 'Hai điều khiển độc lập: "Cách giữ danh sách" đổi bước 1–2, "Cách đệ quy" đổi bước 3–4.', 'Two independent controls: "List kept as" changes steps 1–2, "Recursion" changes steps 3–4.')
    m('ctl.list', 'Cách giữ danh sách', 'List kept as')
    m('ctl.list.mutable', 'MutableList mang hai tên', 'one MutableList, two names'); m('ctl.list.persistent', 'list persistent dùng chung đuôi', 'a persistent list sharing its tail')
    m('ctl.rec', 'Cách đệ quy', 'Recursion')
    m('ctl.rec.plain', 'đệ quy thường', 'plain recursion'); m('ctl.rec.tailrec', 'tích lũy + tailrec', 'accumulator + tailrec')
    m('diagramTitle', 'Hai danh sách dùng chung dữ liệu; hàm đệ quy và stack', 'Two lists sharing data; a recursive function and the stack')
    m('diagramDesc', 'Dùng chung an toàn khi dữ liệu bất biến; đệ quy an toàn khi lời gọi ở vị trí đuôi', 'Sharing is safe when data is immutable; recursion is safe when the call is in tail position')
    for k, vi, en in [('selected', 'Danh sách đã chọn', 'Selected list'), ('booked', 'Lịch đã đặt', 'Booked list'), ('fold', 'Hàm cộng phí', 'Fee sum'), ('stack', 'Stack của luồng', 'Thread stack')]:
        m('n.' + k, vi, en)
    m('met.touched', 'Lần danh sách gốc bị đổi', 'Times the original changed'); m('met.nodes', 'Nút mới tạo', 'New nodes created'); m('met.depth', 'Độ sâu stack lớn nhất', 'Deepest stack')
    a('cap.persist', 'Trên: danh sách đã chọn trỏ tới danh sách gốc. Dưới: hàm cộng phí dùng stack của luồng. Nút đỏ: danh sách gốc bị đổi ngoài ý muốn, hay stack sâu tới mức tràn.',
      'Top: the selected list points into the original. Bottom: the fee sum uses the thread stack. A red node: the original changed by accident, or the stack deep enough to overflow.')
    S = [
        ('mutable', 's1', 'Chọn thêm b4 qua selected = booked', 'Add b4 through selected = booked',
         'Màn chọn lịch viết val selected = booked rồi selected.add(b4). val chỉ cố định tên, không làm object bất biến: hai tên trỏ cùng một MutableList, nên booked cũng có b4. Không nút mới nào được tạo, và đó chính là vấn đề.',
         'The picker screen writes val selected = booked, then selected.add(b4). val only fixes the name; it does not make the object immutable: both names point to the same MutableList, so booked gets b4 too. No new node is created, and that is exactly the problem.'),
        ('mutable', 's2', 'Bỏ lịch đầu của selected', 'Drop the first booking of selected',
         'selected.removeAt(0) bỏ b1. Vì là cùng một object, danh sách lịch đã đặt cũng mất b1: cả hai lần sửa qua selected đều lọt sang booked.',
         'selected.removeAt(0) drops b1. Since it is one object, the booked list loses b1 as well: both changes made through selected leak into booked.'),
        ('persistent', 's1', 'Thêm b4 vào đầu: Cons(b4, booked)', 'Add b4 at the front: Cons(b4, booked)',
         'Tạo đúng 1 nút mới; tail của nó chính là booked (so bằng ===), nên 3 nút cũ được dùng chung chứ không bị chép. booked vẫn là b1, b2, b3.',
         'Exactly 1 new node is created; its tail is booked itself (checked with ===), so the 3 old nodes are shared, not copied. booked is still b1, b2, b3.'),
        ('persistent', 's2', 'Bỏ phần tử đầu: selected.tail', 'Drop the first element: selected.tail',
         'Bỏ phần tử đầu là trả về tail: 0 nút mới, và kết quả chính là booked. Không có gì bị xóa; mọi phiên bản cũ vẫn dùng được, nên cấu trúc này gọi là persistent.',
         'Dropping the first element returns the tail: 0 new nodes, and the result is booked itself. Nothing is deleted; every old version stays usable, which is why the structure is called persistent.'),
        ('plain', 's3', 'Cộng phí 50.000 lịch: đi xuống từng khung', 'Summing 50,000 fees: descending frame by frame',
         'total(xs) = xs.head.fee + total(xs.tail): phép cộng chỉ làm được sau khi lời gọi bên trong trả về, nên mỗi phần tử giữ một khung trên stack. Đi qua 5.000 phần tử: 5.001 khung đang chờ.',
         'total(xs) = xs.head.fee + total(xs.tail): the addition can only happen after the inner call returns, so each element holds a frame on the stack. After 5,000 elements: 5,001 frames waiting.'),
        ('plain', 's4', 'Phần tử thứ 10.000: StackOverflowError', 'Element 10,000: StackOverflowError',
         'Độ sâu vượt giới hạn minh họa 10.000 khung: app crash trước khi làm được phép cộng nào. Báo cáo một tháng chỉ vài trăm lịch nên chạy được; lỗi chỉ lộ với dữ liệu cả năm.',
         'The depth passes the illustrative limit of 10,000 frames: the app crashes before a single addition is done. A monthly report has only a few hundred bookings and runs fine; the bug only shows with a whole year of data.'),
        ('tailrec', 's3', 'Tham số tích lũy và tailrec: một khung', 'An accumulator and tailrec: one frame',
         'total(xs.tail, acc + xs.head.fee): lời gọi là việc cuối cùng, không còn gì phải làm khi nó trả về. Có tailrec, trình biên dịch đổi đệ quy thành vòng lặp: độ sâu luôn là 1.',
         'total(xs.tail, acc + xs.head.fee): the call is the last thing done; nothing is left once it returns. With tailrec the compiler turns the recursion into a loop: the depth is always 1.'),
        ('tailrec', 's4', 'Đi hết 50.000 phần tử: 10.000.000.000 đ', 'All 50,000 elements: 10,000,000,000 VND',
         'Độ sâu vẫn là 1 ở mọi mốc; tổng phí 50.000 × 200.000 đ = 10.000.000.000 đ. Trên List thường của Kotlin, xs.sumOf { it.fee } cho cùng kết quả và vốn chạy bằng vòng lặp.',
         'The depth stays 1 at every mark; the total is 50,000 × 200,000 VND = 10,000,000,000 VND. On an ordinary Kotlin List, xs.sumOf { it.fee } gives the same result and already runs as a loop.'),
    ]
    for case, k, tv, te, xv, xe in S:
        sid = case + '.' + k
        m('s.%s.title' % sid, tv, te); m('s.%s.explain' % sid, xv, xe); m('ev.' + sid, tv, te)
    for k, vi, en in [
        ('try', 'Hai điều khiển độc lập: bước 1–2 xem bảng các danh sách, bước 3–4 xem bảng độ sâu stack.', 'Two independent controls: steps 1–2 watch the list table, steps 3–4 the stack depth table.'),
        ('mutable.s2', 'Carli: bất biến khác hằng. Một tên khai báo bằng val không gán lại được, nhưng object nó trỏ tới vẫn sửa được nếu kiểu cho phép. List chỉ đọc của Kotlin cũng chưa phải bất biến (track Kotlin, chương K7). [[src:book-fp-tut]]',
         'Carli: immutable is not constant. A name declared with val cannot be reassigned, yet the object it points to can still change if its type allows. Kotlin\'s read-only List is not immutable either (Kotlin track, chapter K7). [[src:book-fp-tut]]'),
        ('persistent.s1', 'Vermeulen và cộng sự: thêm phần tử vào đầu list xs là trả về Cons(x, xs); vì list bất biến, không cần chép xs mà dùng lại luôn. Đó là data sharing. [[src:book-fp-manning]]',
         'Vermeulen and co-authors: adding an element to the front of xs returns Cons(x, xs); since the list is immutable, xs need not be copied but is simply reused. That is data sharing. [[src:book-fp-manning]]'),
        ('persistent.s2', 'Vermeulen và cộng sự: bỏ phần tử đầu là trả về tail; list gốc vẫn còn nguyên. Carli phân biệt ba từ: bất biến (không đổi sau khi tạo), hàm (chỉ thao tác bằng hàm thuần), persistent (luôn giữ phiên bản trước). [[src:book-fp-manning]] [[src:book-fp-tut]]',
         'Vermeulen and co-authors: dropping the first element returns the tail; the original list stays intact. Carli separates three words: immutable (unchanged after creation), functional (handled only with pure functions), persistent (always keeps the previous version). [[src:book-fp-manning]] [[src:book-fp-tut]]'),
        ('plain.s3', 'Vermeulen và cộng sự: một lời gọi ở vị trí đuôi khi nơi gọi không làm gì khác ngoài trả kết quả của nó. 1 + go(...) không ở vị trí đuôi, vì còn phép cộng. [[src:book-fp-manning]]',
         'Vermeulen and co-authors: a call is in tail position when the caller does nothing but return its result. 1 + go(...) is not, because the addition remains. [[src:book-fp-manning]]'),
        ('plain.s4', 'Vermeulen và cộng sự: foldRight viết bằng đệ quy thường không stack-safe và gây StackOverflowError với list lớn; foldLeft viết tailrec thì không. [[src:book-fp-manning]]',
         'Vermeulen and co-authors: foldRight written with plain recursion is not stack-safe and throws StackOverflowError on large lists; foldLeft written with tailrec is. [[src:book-fp-manning]]'),
        ('tailrec.s3', 'Tài liệu Kotlin: chỉ gắn tailrec khi hàm gọi chính nó như thao tác cuối cùng; không dùng được khi còn mã sau lời gọi, trong try/catch/finally, hay với hàm open. Khi đủ điều kiện, trình biên dịch bỏ đệ quy và để lại một vòng lặp. [[src:kt-functions]]',
         'Kotlin docs: tailrec applies only when the function calls itself as its final operation; not when code follows the call, inside try/catch/finally, or for open functions. When the conditions hold, the compiler removes the recursion and leaves a loop. [[src:kt-functions]]'),
        ('tailrec.s4', 'Carli: mã dịch ngược của hàm tailrec là một vòng while(true), không còn lời gọi đệ quy. Không gắn tailrec thì trình biên dịch không tự làm việc đó, dù lời gọi đã ở vị trí đuôi (Vermeulen và cộng sự). [[src:book-fp-tut]] [[src:book-fp-manning]]',
         'Carli: the decompiled tailrec function is a while(true) loop with no recursive call left. Without tailrec the compiler does not do this on its own, even when the call is in tail position (Vermeulen and co-authors). [[src:book-fp-tut]] [[src:book-fp-manning]]'),
    ]:
        m('co.' + k, vi, en)

    z = lambda k, vi, en=None: a('vz.' + k, vi, en)
    z('tab.persist', 'Nút danh sách và độ sâu stack', 'List nodes and stack depth')
    z('persist.cap', 'Mỗi ô là một nút của danh sách. Viền: nút vừa tạo hay vừa thêm. Đậm: nút dùng chung với booked. Gạch đỏ: booked bị đổi ngoài ý muốn.', 'Each cell is a list node. Outlined: a node just created or added. Bold: a node shared with booked. Red hatched: booked changed by accident.')
    z('persist.scap', 'Độ sâu stack theo số phần tử đã đi qua trong {n} lịch hẹn. Giới hạn minh họa: {lim} khung.', 'Stack depth by elements visited among {n} bookings. Illustrative limit: {lim} frames.')
    z('persist.legend', 'Ô "?": chưa tới bước đó. Đỏ: sâu quá nửa giới hạn, hay tràn stack. Đậm: 1 khung (đã thành vòng lặp).', '"?": that step has not come yet. Red: deeper than half the limit, or an overflow. Bold: 1 frame (now a loop).')
    for k, vi, en in [('name', 'Tên', 'Name'), ('ref', 'Là gì', 'What it is'), ('nodes', 'Các nút', 'Nodes'), ('seen', 'Đã đi qua', 'Elements visited')]:
        z('persist.col.' + k, vi, en)
    for k, vi, en in [('leak', 'lọt sang', 'leaked in'), ('new', 'mới', 'new'), ('shared', 'dùng chung', 'shared'), ('lost', 'mất', 'lost')]:
        z('persist.chip.' + k, vi, en)
    for k, vi, en in [('booked', 'danh sách lịch đã đặt', 'the booked list'), ('selected', 'Cons(b4, booked): một nút mới và đuôi cũ', 'Cons(b4, booked): one new node and the old tail'),
                      ('alias', 'cùng một object với booked', 'the same object as booked'), ('tail', 'selected.tail: chính là booked', 'selected.tail: booked itself')]:
        z('persist.ref.' + k, vi, en)
    z('persist.rec.plain', 'đệ quy thường', 'plain recursion'); z('persist.rec.tailrec', 'tích lũy + tailrec', 'accumulator + tailrec')
    z('persist.crash', 'tràn', 'overflow'); z('persist.skip', 'không tới', 'not reached')
    z('persist.result.crash', 'StackOverflowError ở phần tử thứ {n}: chưa làm được phép cộng nào.', 'StackOverflowError at element {n}: not a single addition done.')
    z('persist.result.ok', 'Tổng phí: {t} đ; độ sâu luôn là 1.', 'Total fees: {t} VND; the depth is always 1.')
    z('persist.result.none', 'Hàm cộng phí chưa chạy (bước 3–4).', 'The fee sum has not run yet (steps 3–4).')

    C = 'p2'
    a(C + '.title', 'Bất biến, dữ liệu dùng chung và đệ quy', 'Immutability, data sharing and recursion')
    a(C + '.essence', 'Bất biến nói về object, hằng nói về tên: val chỉ cấm gán lại, không cấm sửa object. Hai tên trỏ cùng một MutableList thì sửa qua tên này là sửa cả tên kia.\nCấu trúc persistent không sửa tại chỗ: thêm vào đầu tạo một nút mới và dùng chung phần đuôi; bỏ phần tử đầu là trả về đuôi. Bản cũ còn nguyên, nên không cần chép phòng xa.\nĐệ quy thường giữ một khung stack cho mỗi lời gọi còn chờ và tràn với dữ liệu lớn. Viết lại với tham số tích lũy để lời gọi là việc cuối cùng, rồi gắn tailrec: trình biên dịch đổi nó thành vòng lặp.',
      'Immutability is about objects, constancy about names: val only forbids reassignment, not changing the object. Two names for one MutableList mean a change through one is a change through the other.\nA persistent structure never changes in place: adding at the front creates one new node and shares the tail; dropping the first element returns the tail. Old versions stay intact, so there is no need to copy just in case.\nPlain recursion holds a stack frame for every pending call and overflows on large data. Rewrite it with an accumulator so the call is the last thing done, then mark it tailrec: the compiler turns it into a loop.')
    a(C + '.goal.g1', 'Đã thấy danh sách gốc đổi hay không đổi', 'Saw whether the original list changed')
    a(C + '.goal.g2', 'Đã thấy stack tràn hay giữ một khung', 'Saw the stack overflow or stay at one frame')
    a(C + '.sim.fp.persist', 'dữ liệu dùng chung và độ sâu stack', 'data sharing and stack depth')

    S_ = 'hook'
    a(C + '.sec.%s.title' % S_, 'Đoán trước khi đọc', 'Predict before reading')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'predict', 'Màn "Chọn lịch để hủy" có dòng val selected = booked, với booked là MutableList. Người dùng bỏ chọn một lịch, rồi quay lại tab "Lịch đã đặt". Họ thấy gì?',
      'The "Pick bookings to cancel" screen has val selected = booked, where booked is a MutableList. The user unselects a booking, then goes back to the "Booked" tab. What do they see?')
    B(C, S_, 1, 'ans', 'Lịch vừa bỏ chọn cũng biến khỏi danh sách lịch đã đặt: hai tên, một object. val không làm object bất biến; nó chỉ cấm gán tên đó cho object khác.',
      'The booking just unselected has vanished from the booked list too: two names, one object. val does not make the object immutable; it only forbids pointing that name at another object.')

    S_ = 'immut'
    a(C + '.sec.%s.title' % S_, 'Bất biến khác hằng', 'Immutable is not constant')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'p', 'Carli: object bất biến là object không đổi trạng thái sau khi được tạo; lớp bất biến không có hàm sửa. Ông tách hai khái niệm hay bị nhầm: bất biến nói về object, hằng nói về tham chiếu. val user = MutableUser(…) là hằng, không gán lại được, nhưng object vẫn sửa được qua user.username = … [[src:book-fp-tut]]',
      'Carli: an immutable object cannot change state after it is created; an immutable class has no mutators. He separates two ideas that are often confused: immutability is about objects, constancy about references. val user = MutableUser(…) is a constant that cannot be reassigned, yet the object can still be changed through user.username = … [[src:book-fp-tut]]')
    B(C, S_, 2, 'p', 'Với data class, mọi thuộc tính là val vẫn chưa đủ: nếu một thuộc tính có kiểu sửa được (ví dụ java.util.Date), object vẫn đổi được qua nó; Carli cho ví dụ đổi dob.time của một user "toàn val". List của Kotlin là read-only chứ không phải bất biến; track Kotlin chương K7 có mô phỏng riêng. [[src:book-fp-tut]]',
      'For a data class, all-val properties are not enough: if one property has a mutable type (say java.util.Date), the object can still change through it; Carli changes dob.time on an "all val" user. Kotlin\'s List is read-only, not immutable; the Kotlin track\'s chapter K7 has its own simulation. [[src:book-fp-tut]]')
    B(C, S_, 3, 'p', 'Lợi ích Carli nêu: đơn giản, nhất quán (object bất biến làm khóa Map an toàn, còn khóa bị sửa làm Map hỏng, như track Kotlin K4), tránh tạo trùng, và an toàn khi nhiều luồng cùng dùng. [[src:book-fp-tut]]',
      'The benefits Carli lists: simplicity, consistency (immutable objects are safe Map keys, while a mutated key breaks the Map, as in Kotlin track K4), avoiding duplicates, and safety when several threads share the object. [[src:book-fp-tut]]')

    S_ = 'share'
    a(C + '.sec.%s.title' % S_, 'Dữ liệu dùng chung và cấu trúc persistent', 'Data sharing and persistent structures')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'p', 'Không sửa tại chỗ thì thêm hay bớt phần tử thế nào? Vermeulen và cộng sự: thêm x vào đầu xs là tạo Cons(x, xs), không chép xs vì nó không thể đổi; bỏ phần tử đầu là trả về tail. Cách này gọi là data sharing, và cấu trúc giữ nguyên mọi phiên bản cũ gọi là persistent. [[src:book-fp-manning]]',
      'Without changing in place, how do you add or remove elements? Vermeulen and co-authors: adding x at the front of xs creates Cons(x, xs), without copying xs since it cannot change; dropping the first element returns the tail. This is called data sharing, and a structure that keeps every old version intact is called persistent. [[src:book-fp-manning]]')
    B(C, S_, 2, 'p', 'Họ nhấn mạnh cái lợi khi chương trình lớn: dữ liệu sửa được đi qua nhiều thành phần thì mỗi nơi phải tự chép một bản phòng nơi khác sửa (pessimistic copying); dữ liệu bất biến chia sẻ an toàn, không cần chép. [[src:book-fp-manning]]',
      'They stress the gain in large programs: mutable data passed through many components forces each one to copy it in case another changes it (pessimistic copying); immutable data is safe to share and needs no copies. [[src:book-fp-manning]]')
    B(C, S_, 3, 'note', 'Không phải phép nào cũng rẻ. append(a1, a2) chỉ chép các nút của a1, còn a2 dùng chung; nhưng init (bỏ phần tử cuối) phải chép mọi nút đứng trước, vì muốn đổi tail của nút cuối thì phải tạo lại cả chuỗi (Vermeulen và cộng sự). List thường của Kotlin là mảng: list + x tạo một list mới và chép mọi phần tử. [[src:book-fp-manning]]',
      'Not every operation is cheap. append(a1, a2) copies only the nodes of a1 and shares a2; but init (dropping the last element) must copy every preceding node, because changing the last node\'s tail means rebuilding the chain (Vermeulen and co-authors). An ordinary Kotlin List is array-based: list + x builds a new list and copies every element. [[src:book-fp-manning]]')
    B(C, S_, 3, 'kind', 'source')

    S_ = 'recursion'
    a(C + '.sec.%s.title' % S_, 'Đệ quy thay vòng lặp, và cái giá của nó', 'Recursion instead of loops, and its cost')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'p', 'Đệ quy lặp mà không cần biến sửa được: thay vì đổi giá trị một biến trong vòng for, gọi lại hàm với giá trị mới làm tham số (Carli). Nhưng đệ quy thường tốn một khung stack cho mỗi lời gọi còn chờ. Carli khai triển recursiveFactorial(5) thành 5 * recursiveFactorial(4), rồi 5 * 4 * recursiveFactorial(3)…: mọi phép nhân phải đợi tới đáy rồi mới tính ngược lên. [[src:book-fp-tut]]',
      'Recursion loops without mutable variables: instead of changing a variable in a for loop, call the function again with the new value as a parameter (Carli). But plain recursion costs a stack frame for every pending call. Carli expands recursiveFactorial(5) into 5 * recursiveFactorial(4), then 5 * 4 * recursiveFactorial(3)…: every multiplication waits for the bottom before working back up. [[src:book-fp-tut]]')
    B(C, S_, 2, 'kt', '// đệ quy thường: các phép cộng chờ ở mỗi tầng\ntotal([b1, b2, b3])\n= 200_000 + total([b2, b3])\n= 200_000 + (200_000 + total([b3]))\n= 200_000 + (200_000 + (200_000 + total(Nil)))   // 4 khung đang chờ\n= 600_000\n\n// tích lũy: không gì phải chờ\ntotal([b1, b2, b3], 0)\n= total([b2, b3], 200_000)\n= total([b3], 400_000)\n= total(Nil, 600_000) = 600_000',
      '// plain recursion: the additions wait at every level\ntotal([b1, b2, b3])\n= 200_000 + total([b2, b3])\n= 200_000 + (200_000 + total([b3]))\n= 200_000 + (200_000 + (200_000 + total(Nil)))   // 4 frames waiting\n= 600_000\n\n// accumulator: nothing waits\ntotal([b1, b2, b3], 0)\n= total([b2, b3], 200_000)\n= total([b3], 400_000)\n= total(Nil, 600_000) = 600_000')

    S_ = 'tailrec'
    a(C + '.sec.%s.title' % S_, 'Vị trí đuôi và tailrec', 'Tail position and tailrec')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'p', 'Vị trí đuôi: nơi gọi không làm gì khác ngoài trả kết quả của lời gọi (Vermeulen và cộng sự). Kotlin không tự nhận ra; phải gắn tailrec. Tài liệu Kotlin: chỉ gắn khi hàm gọi chính nó như thao tác cuối cùng; không dùng được khi còn mã sau lời gọi, trong try/catch/finally, hay với hàm open. Khi đủ điều kiện, trình biên dịch bỏ đệ quy và để lại một vòng lặp. [[src:kt-functions]] [[src:book-fp-manning]]',
      'Tail position: the caller does nothing but return the call\'s result (Vermeulen and co-authors). Kotlin does not detect it on its own; you add tailrec. The Kotlin docs: apply it only when the function calls itself as its final operation; not when code follows the call, inside try/catch/finally, or for open functions. When the conditions hold, the compiler removes the recursion and leaves a loop. [[src:kt-functions]] [[src:book-fp-manning]]')
    B(C, S_, 2, 'p', 'Cách đổi hay gặp: thêm một tham số tích lũy (acc) mang kết quả từng phần, như go(n - 1, n * acc) của Vermeulen và cộng sự hay tailRecFactorial(n - 1, n * fact) của Carli. [[src:book-fp-manning]] [[src:book-fp-tut]]',
      'The usual rewrite: add an accumulator (acc) carrying the partial result, like go(n - 1, n * acc) in Vermeulen and co-authors or tailRecFactorial(n - 1, n * fact) in Carli. [[src:book-fp-manning]] [[src:book-fp-tut]]')
    B(C, S_, 3, 'note', 'Theo Vermeulen và cộng sự, gắn tailrec cho một hàm không có lời gọi đuôi nào chỉ làm trình biên dịch cảnh báo, không báo lỗi. Đừng coi chữ tailrec là bảo đảm; đọc từng lời gọi. Trong mã app, cách đơn giản nhất thường là hàm của thư viện chuẩn (sumOf, fold) trên List, vốn chạy bằng vòng lặp. [[src:book-fp-manning]]',
      'Per Vermeulen and co-authors, marking a function tailrec when it has no tail call at all only gives a compiler warning, not an error. Do not treat the word tailrec as a guarantee; read each call. In app code the simplest route is usually a standard library function (sumOf, fold) on List, which already runs as a loop. [[src:book-fp-manning]]')
    B(C, S_, 3, 'kind', 'pitfall')

    S_ = 'bugs'
    a(C + '.sec.%s.title' % S_, 'Hai lỗi hay gặp', 'Two common bugs')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'bug', 'Ở màn "Chọn lịch để hủy", bỏ chọn một lịch làm lịch đó biến khỏi danh sách lịch đã đặt.', 'On the "Pick bookings to cancel" screen, unselecting a booking makes it vanish from the booked list.')
    B(C, S_, 1, 'cause', 'val selected = booked với booked là MutableList: hai tên cùng trỏ một object, nên removeAt qua selected sửa cả booked.', 'val selected = booked where booked is a MutableList: both names point to one object, so removeAt through selected changes booked too.')
    B(C, S_, 1, 'fix', 'Giữ danh sách bằng List (hay cấu trúc persistent) và tạo danh sách mới khi đổi (filter, minus, Cons); không đưa một MutableList dùng chung qua nhiều màn hình.', 'Keep lists as List (or a persistent structure) and build a new list on change (filter, minus, Cons); do not pass one shared MutableList across screens.')
    B(C, S_, 2, 'bug', 'Xuất báo cáo cả năm (50.000 lịch hẹn) làm app crash với StackOverflowError; báo cáo một tháng thì chạy.', 'Exporting the yearly report (50,000 bookings) crashes with StackOverflowError; the monthly report works.')
    B(C, S_, 2, 'cause', 'Hàm cộng phí đệ quy còn phép cộng sau lời gọi, nên mỗi phần tử giữ một khung stack. Vài trăm phần tử vừa stack; vài chục nghìn thì không.', 'The recursive fee sum still adds after the call, so each element holds a stack frame. A few hundred elements fit the stack; tens of thousands do not.')
    B(C, S_, 2, 'fix', 'Viết lại với tham số tích lũy và gắn tailrec, hoặc dùng hàm của thư viện chuẩn như sumOf. Thêm test với một danh sách đủ lớn để bắt lỗi trước khi phát hành.', 'Rewrite with an accumulator and tailrec, or use a standard library function such as sumOf. Add a test with a large enough list to catch it before release.')

    S_ = 'ex'
    a(C + '.sec.%s.title' % S_, 'Bài tập', 'Exercise')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'ex', 'Hàm dưới đây đã gắn tailrec. Trình biên dịch có biến cả hàm thành vòng lặp không? Viết lại cho đúng. (Ý bài tập theo của Carli và của Vermeulen và cộng sự, viết lại cho app Hẹn Khám.)',
      'The function below is marked tailrec. Does the compiler turn the whole function into a loop? Rewrite it properly. (The idea follows Carli\'s and of Vermeulen and co-authors, rewritten for the ClinicBook app.)')
    B(C, S_, 1, 'exkt', 'tailrec fun countPaid(xs: FList<Booking>): Int = when (xs) {\n    Nil -> 0\n    is Cons -> if (xs.head.paid) 1 + countPaid(xs.tail) else countPaid(xs.tail)\n}')
    B(C, S_, 1, 'hint', 'Với mỗi lời gọi đệ quy, hỏi: khi nó trả về, hàm còn phải làm gì nữa không?', 'For each recursive call, ask: once it returns, is there anything left for the function to do?')
    B(C, S_, 1, 'sol', 'Không. Ở nhánh paid còn phép cộng 1 sau lời gọi, nên lời gọi đó không ở vị trí đuôi; tài liệu Kotlin nói không dùng được tailrec khi còn mã sau lời gọi. Với một năm toàn lịch đã trả, stack vẫn sâu dần. Thêm tham số tích lũy để mọi nhánh kết thúc bằng chính lời gọi.',
      'No. In the paid branch an addition of 1 follows the call, so that call is not in tail position; the Kotlin docs say tailrec cannot be used when code follows the recursive call. Over a year of paid bookings the stack still grows. Add an accumulator so every branch ends with the call itself.')
    B(C, S_, 1, 'solkt', 'tailrec fun countPaid(xs: FList<Booking>, acc: Int = 0): Int = when (xs) {\n    Nil -> acc\n    is Cons -> countPaid(xs.tail, if (xs.head.paid) acc + 1 else acc)\n}')

    S_ = 'honest'
    a(C + '.sec.%s.title' % S_, 'Chương này giản lược những gì', 'What this chapter simplifies')
    a(C + '.sec.%s.badge' % S_, 'simplified')
    B(C, S_, 1, 'p', 'Data sharing, persistent, tail call và foldRight không stack-safe theo Vermeulen, Bjarnason, Chiusano; bất biến khác hằng, lợi ích của bất biến, tailrec thành vòng while theo Carli; điều kiện của tailrec theo tài liệu Kotlin (Functions, đọc 2026-11-24). FList tự viết để thấy nút dùng chung; trong app thường dùng List của Kotlin. Giới hạn 10.000 khung là con số minh họa: độ sâu thật tùy kích thước stack của luồng và kích thước mỗi khung, nên đừng dựa vào một con số cụ thể. 50.000 lịch và phí 200.000 đ là của site.',
      'Data sharing, persistence, tail calls and the non-stack-safe foldRight follow Vermeulen, Bjarnason, Chiusano; immutable versus constant, the benefits of immutability and tailrec becoming a while loop follow Carli; the tailrec conditions follow the Kotlin docs (Functions, read 2026-11-24). FList is hand-written to make shared nodes visible; apps normally use Kotlin\'s List. The 10,000-frame limit is illustrative: the real depth depends on the thread\'s stack size and each frame\'s size, so do not rely on any specific number. The 50,000 bookings and the 200,000 VND fee are the site\'s.')

    for q, qv, qe, av, ae, wv, we in [
        ('q1', 'booked là MutableList; val selected = booked; selected.add(b4). booked có đổi không?', 'booked is a MutableList; val selected = booked; selected.add(b4). Does booked change?', 'Có.', 'Yes.', 'Hai tên trỏ cùng một object; val chỉ cấm gán lại tên, không cấm sửa object.', 'Both names point to one object; val only forbids reassigning the name, not changing the object.'),
        ('q2', 'Thêm b4 vào đầu một list persistent 3 phần tử tạo bao nhiêu nút mới?', 'How many new nodes does adding b4 to the front of a 3-element persistent list create?', 'Một.', 'One.', 'Nút mới trỏ tới list cũ làm đuôi; 3 nút cũ được dùng chung.', 'The new node points to the old list as its tail; the 3 old nodes are shared.'),
        ('q3', 'Lời gọi trong xs.head.fee + total(xs.tail) có ở vị trí đuôi không?', 'Is the call in xs.head.fee + total(xs.tail) in tail position?', 'Không.', 'No.', 'Khi nó trả về, hàm còn phải cộng xs.head.fee.', 'Once it returns, the function still has to add xs.head.fee.'),
        ('q4', 'Hàm có try/catch bao quanh lời gọi đệ quy có dùng tailrec được không?', 'Can a function with try/catch around its recursive call use tailrec?', 'Không.', 'No.', 'Tài liệu Kotlin liệt kê try/catch/finally là chỗ không dùng được tail recursion.', 'The Kotlin docs list try/catch/finally among the places tail recursion cannot be used.')]:
        a(C + '.quiz.%s.q' % q, qv, qe); a(C + '.quiz.%s.a' % q, av, ae); a(C + '.quiz.%s.why' % q, wv, we)
