# Lập trình hàm · K9 (p9): functional core, imperative shell (Phần 3: ứng dụng)
# Nguồn (chỉ ghi ở đây và docs/research/fp.md): Seemann, Code That Fits in Your Head A.12 và 13.1.3 (ưu tiên hàm thuần; Post đọc hết rồi gọi WillAccept thuần,
# chỉ ghi khi true; đẩy query không tất định và side effect ra rìa; càng nhiều hàm thuần càng ít cần log); Barbini ch.6 (thay đổi state ở rìa);
# Carli ch.16 (side effect là thay đổi thế giới; kiểu IO, chỉ nhắc). Giọng văn dạy học.

SEC_ORDER = {'p9': ['hook', 'why', 'split', 'test', 'android', 'bugs', 'ex', 'recall']}


def add(a):
    def B(ch, sec, n, field, vi, en=None):
        a('%s.sec.%s.b.%02d.%s' % (ch, sec, n, field), vi, vi if en is None else en)

    a('preset.core', '''Lập trình hàm · lõi thuần, vỏ mỏng''', '''Functional programming · a pure core, a thin shell''')
    m = lambda k, vi, en=None: a('m.core.' + k, vi, en)
    m('title', '''Hàm đặt lịch: trộn I/O với luật, hay tách lõi và vỏ''', '''The booking function: I/O mixed with rules, or a core and a shell''')
    m('overview', '''Hàm book() của app Hẹn Khám kiểm giờ đã qua chưa, còn trống không, còn lượt không, và tính phí cuối tuần. Cách 1 viết tất cả trong một hàm vừa đọc vừa ghi. Cách 2 tách các luật ra một hàm thuần decide() và để book() thành một lớp vỏ mỏng. Ta đếm số lần hàm qua lại giữa việc đụng ra ngoài và luật thuần, số đồ giả cần để test luật phí, và các lần ghi ra ngoài sai chỗ.''',
      '''The ClinicBook book() function checks whether the time has passed, whether the slot is free, whether visits are left, and computes the weekend fee. Way 1 writes everything in one function that both reads and writes. Way 2 moves the rules into a pure decide() function and makes book() a thin shell. We count how often the function crosses between outside work and pure rules, how many fakes a fee test needs, and misplaced writes.''')
    m('wrapup', '''Hàm trộn qua lại ranh giới 4 lần, cần 5 đồ giả để test một luật phí, và gửi thống kê trước khi biết có đặt được không. Lõi thuần cùng vỏ mỏng chỉ qua ranh giới 2 lần, test luật bằng giá trị với 0 đồ giả, và chỉ ghi khi lõi đã trả Accept.''',
      '''The mixed function crosses the boundary 4 times, needs 5 fakes to test one fee rule, and sends analytics before knowing whether the booking succeeds. The pure core with a thin shell crosses only twice, tests rules with plain values and 0 fakes, and writes only after the core returns Accept.''')
    m('simp.1', '''Mỗi việc đụng ra ngoài là một ô; hàm thật có thể đọc ghi nhiều hơn, và đồng hồ hay máy chủ thường được truyền vào thay vì gọi trực tiếp.''',
      '''Each piece of outside work is one box; a real function may read and write more, and the clock or the server is often passed in rather than called directly.''')
    m('simp.2', '''Thứ tự thao tác, số lần qua ranh giới, số đồ giả và luật phí được đếm, tính thật bằng JavaScript từ danh sách thao tác của hai đoạn mã. Đoạn Kotlin chỉ để minh họa; site không chạy Kotlin trong trang.''',
      '''The order of operations, boundary crossings, fakes and the fee rule are really counted and computed in JavaScript from the operation lists of the two code samples. The Kotlin code is illustrative; the site does not run Kotlin in the page.''')
    m('ctl.hint', '''Chọn cách viết rồi đi qua bốn bước; đếm số lần vệt vượt đường nét đứt và xem ô nào chuyển đỏ.''', '''Pick a way of writing it and walk the four steps; count how often the trail crosses the dashed line and watch which boxes turn red.''')
    m('ctl.case', '''Cách viết book()''', '''How book() is written''')
    m('ctl.case.mixed', '''một hàm trộn đọc, luật và ghi''', '''one function mixing reads, rules and writes'''); m('ctl.case.core', '''lõi thuần decide() và vỏ mỏng''', '''a pure decide() core and a thin shell''')
    m('diagramTitle', '''Vỏ, lõi, bài test''', '''Shell, core, test''')
    m('diagramDesc', '''Vỏ gọi lõi rồi làm theo kết quả; bài test gọi lõi trực tiếp''', '''The shell calls the core and acts on its result; a test calls the core directly''')
    for k, vi, en in [('shell', 'Vỏ: đọc và ghi bên ngoài', 'Shell: outside reads and writes'), ('core', 'Lõi: luật thuần', 'Core: pure rules'), ('test', 'Bài test luật', 'Rule tests')]:
        m('n.' + k, vi, en)
    m('met.cross', '''Lần qua lại ranh giới''', '''Boundary crossings'''); m('met.fakes', '''Đồ giả cần để test luật phí''', '''Fakes needed to test the fee rule''')
    m('met.early', '''Lần ghi trước khi quyết định xong''', '''Writes before the decision is made'''); m('met.branches', '''Nhánh luật trong hàm có I/O''', '''Rule branches inside the I/O function''')
    a('cap.core', '''Vỏ đọc dữ liệu cho lõi và ghi theo kết quả của lõi; bài test gọi thẳng lõi. Ô đỏ: test cần nhiều đồ giả, hoặc ghi ra ngoài sai chỗ.''',
      '''The shell reads data for the core and writes according to the core\'s result; a test calls the core directly. A red box: a test needing many fakes, or a misplaced write.''')
    S = [
        ('mixed', 's1', 'Một hàm vừa đọc, vừa quyết định, vừa ghi', 'One function that reads, decides and writes',
         'book() đọc đồng hồ, đọc giờ trống từ database, kiểm giờ đã qua, gửi thống kê, hỏi máy chủ số lượt, kiểm còn trống và còn lượt, tính phí, lưu lịch, ghi log. Luật (cột phải) và các việc đụng ra ngoài (cột trái) xen kẽ nhau: vệt qua lại ranh giới 4 lần.',
         'book() reads the clock, reads the free slots from the database, checks whether the time has passed, sends analytics, asks the server for the quota, checks the slot and quota, computes the fee, saves the booking, writes a log. Rules (right column) and outside work (left column) interleave: the trail crosses the boundary 4 times.'),
        ('mixed', 's2', 'Test luật phí cần 5 đồ giả', 'Testing the fee rule needs 5 fakes',
         'Muốn kiểm "thứ Bảy tính 300.000 đ", bài test phải gọi cả book(), nên phải giả đồng hồ, database, máy chủ, thống kê và log: 5 đồ giả chỉ để kiểm một phép so sánh ngày.',
         'To check "Saturday costs 300,000 VND", the test must call the whole book(), so it must fake the clock, the database, the server, analytics and logging: 5 fakes just to check one date comparison.'),
        ('mixed', 's3', 'Thống kê đếm cả lịch không đặt được', 'Analytics counts bookings that failed',
         'analytics.track("booked") chạy trước khi kiểm còn trống và còn lượt. Khi giờ đã có người đặt, hàm trả "Không đặt được" nhưng thống kê đã ghi một lần đặt. Ghi ra ngoài xen giữa các phép kiểm làm thứ tự rất dễ sai.',
         'analytics.track("booked") runs before the slot and quota checks. When the slot is taken, the function returns "Cannot book", but analytics has already recorded a booking. Writes interleaved with checks make the order easy to get wrong.'),
        ('mixed', 's4', 'Luật nằm giữa các lệnh I/O', 'Rules sit between I/O calls',
         'Hai phép kiểm và một phép tính phí nằm giữa các lệnh đọc, ghi. Muốn đổi một luật, bạn phải đọc cả hàm và cẩn thận không làm đổi thứ tự các lệnh I/O xung quanh.',
         'Two checks and a fee computation sit between reads and writes. To change one rule, you must read the whole function and take care not to reorder the I/O calls around it.'),
        ('core', 's1', 'Vỏ đọc hết, lõi quyết định, vỏ ghi', 'The shell reads, the core decides, the shell writes',
         'Vỏ book() đọc đồng hồ, giờ trống và số lượt; gọi decide() một lần với các giá trị đó; rồi mới ghi. decide() là hàm thuần: nhận giá trị, trả một Decision (Accept kèm lịch, hoặc Reject kèm lý do). Vệt chỉ qua ranh giới 2 lần: vào lõi, rồi ra.',
         'The shell book() reads the clock, the free slots and the quota; calls decide() once with those values; and only then writes. decide() is a pure function: it takes values and returns a Decision (Accept with the booking, or Reject with a reason). The trail crosses the boundary only twice: into the core and back out.'),
        ('core', 's2', 'Test luật phí không cần đồ giả', 'Testing the fee rule needs no fakes',
         'Bài test gọi thẳng decide() với các giá trị tự chọn: ngày thứ Bảy, now là thứ Hai, giờ S12 còn trống, còn 2 lượt. Kết quả là Accept với phí 300.000 đ. Không đồng hồ, không database, không máy chủ: 0 đồ giả.',
         'The test calls decide() directly with values it chooses: a Saturday, now on a Monday, slot S12 free, 2 visits left. The result is Accept with a 300,000 VND fee. No clock, no database, no server: 0 fakes.'),
        ('core', 's3', 'Chỉ ghi khi đã quyết định xong', 'Write only after deciding',
         'Vỏ chỉ lưu lịch, gửi thống kê và ghi log khi decide() trả Accept. Lịch không đặt được thì không có lần ghi nào, nên thống kê không thể đếm sai.',
         'The shell saves the booking, sends analytics and writes the log only when decide() returns Accept. A booking that fails causes no write at all, so analytics cannot miscount.'),
        ('core', 's4', 'Vỏ chỉ còn một nhánh', 'The shell has just one branch',
         'Mọi luật nằm trong decide(); vỏ chỉ còn một if: Accept thì ghi, Reject thì trả lý do. Vỏ mỏng tới mức một bài test tích hợp là đủ, còn luật được kiểm kỹ bằng nhiều bài test giá trị.',
         'Every rule lives in decide(); the shell keeps a single if: on Accept write, on Reject return the reason. The shell is thin enough that one integration test is enough, while the rules get thorough value-based tests.'),
    ]
    for case, k, tv, te, xv, xe in S:
        sid = case + '.' + k
        m('s.%s.title' % sid, tv, te); m('s.%s.explain' % sid, xv, xe); m('ev.' + sid, tv, te)
    for k, vi, en in [
        ('try', '''Mẹo đọc: cột trái là các việc đụng ra ngoài (đọc đồng hồ, database, máy chủ; lưu, gửi thống kê, ghi log), cột phải là luật thuần. Vệt nối các việc theo thứ tự chạy; đếm số lần nó vượt đường nét đứt.''',
         '''Reading tip: the left column is outside work (reading the clock, the database, the server; saving, analytics, logging), the right column is pure rules. The trail joins the operations in running order; count how often it crosses the dashed line.'''),
        ('mixed.s2', '''Mark Seemann: hàm thuần dễ ghép và dễ unit test; còn query không tất định (đồng hồ, database) và side effect nên được đẩy ra rìa hệ thống. [[src:book-seemann]]''',
         '''Mark Seemann: pure functions compose well and are easy to unit test; nondeterministic queries (the clock, the database) and side effects should be pushed to the edge of the system. [[src:book-seemann]]'''),
        ('mixed.s3', '''Seemann mô tả một hàm Post đọc hết dữ liệu trước, gọi một hàm thuần, và chỉ ghi khi hàm đó cho phép. Hàm trộn ở đây làm ngược lại: ghi trước khi biết kết quả. [[src:book-seemann]]''',
         '''Seemann describes a Post method that first reads all the data, calls a pure function, and writes only when that function allows it. The mixed function here does the opposite: it writes before knowing the outcome. [[src:book-seemann]]'''),
        ('mixed.s4', '''Uberto Barbini: lập trình hàm giữ mọi thay đổi state ở rìa để logic chính khỏi phải lo tới chúng. [[src:book-barbini]]''',
         '''Uberto Barbini: functional programming keeps all state changes at the edges so the core logic can ignore them. [[src:book-barbini]]'''),
        ('core.s1', '''Seemann dùng kiểu kiến trúc mà Gary Bernhardt đặt tên là functional core, imperative shell (lõi thuần, vỏ mệnh lệnh): logic phức tạp viết thành hàm thuần, còn việc không tất định và side effect nằm sát rìa. [[src:book-seemann]]''',
         '''Seemann uses the architecture Gary Bernhardt named functional core, imperative shell: complex logic written as pure functions, with nondeterminism and side effects kept close to the edge. [[src:book-seemann]]'''),
        ('core.s2', '''Đây là cùng ý ở chương "Hàm thuần và referential transparency": ngày là tham số thì bài test không phụ thuộc hôm nay là thứ mấy. [[src:book-seemann]]''',
         '''This is the same idea as in the chapter "Pure functions and referential transparency": when the date is a parameter, the test does not depend on what day it is today. [[src:book-seemann]]'''),
        ('core.s3', '''Trong ví dụ của Seemann, chỉ khi hàm thuần WillAccept trả true thì Post mới cho side effect xảy ra. [[src:book-seemann]]''',
         '''In Seemann\'s example, Post only lets the side effect happen when the pure WillAccept function returns true. [[src:book-seemann]]'''),
        ('core.s4', '''Seemann còn nhận xét: càng nhiều hàm thuần thì càng ít cần log, vì biết đầu vào là tính lại được đầu ra. [[src:book-seemann]]''',
         '''Seemann also notes: the more of your code is pure functions, the less you need to log, because knowing the inputs lets you recompute the output. [[src:book-seemann]]'''),
    ]:
        m('co.' + k, vi, en)

    z = lambda k, vi, en=None: a('vz.' + k, vi, en)
    z('tab.core', '''Vỏ và lõi''', '''Shell and core''')
    z('core.aria', '''Hai cột vỏ và lõi; các thao tác qua lại ranh giới {n} lần''', '''Two columns, shell and core; the operations cross the boundary {n} times''')
    z('core.col.shell', '''Vỏ: đọc, ghi bên ngoài''', '''Shell: outside reads and writes''')
    z('core.col.core', '''Lõi: luật thuần''', '''Core: pure rules''')
    z('core.cap.mixed', '''Cách 1: một hàm book() trộn đọc, luật và ghi; các ô xếp theo thứ tự chạy.''', '''Way 1: one book() function mixing reads, rules and writes; boxes in running order.''')
    z('core.cap.core', '''Cách 2: vỏ book() đọc hết, gọi decide() một lần, rồi mới ghi.''', '''Way 2: the shell book() reads everything, calls decide() once, and only then writes.''')
    z('core.focus.0', '''Vệt qua lại ranh giới {n} lần.''', '''The trail crosses the boundary {n} times.''')
    z('core.focus.1', '''Test luật phí cần {n} đồ giả (ô đỏ là thứ phải giả).''', '''Testing the fee rule needs {n} fakes (red boxes are what must be faked).''')
    z('core.focus.2', '''Số lần ghi ra ngoài trước khi quyết định xong: {n}.''', '''Writes before the decision is made: {n}.''')
    z('core.focus.3', '''Số nhánh luật nằm trong hàm có I/O: {n}.''', '''Rule branches inside the function doing I/O: {n}.''')
    z('core.legend', '''Cột phải là luật thuần, cột trái là việc đụng ra ngoài; đường xanh nối các ô theo thứ tự chạy. Đỏ: chỗ có vấn đề ở bước này. Viền xanh: chỗ đã ổn.''',
      '''The right column is pure rules, the left column is outside work; the green line joins the boxes in running order. Red: a problem at this step. Green outline: already fine.''')

    C = 'p9'
    a(C + '.title', '''Functional core, imperative shell: lõi thuần, vỏ mỏng''', '''Functional core, imperative shell: a pure core, a thin shell''')
    a(C + '.essence', '''Một hàm vừa đọc đồng hồ, database, máy chủ, vừa quyết định, vừa ghi ra ngoài thì khó test (cần nhiều đồ giả) và dễ ghi sai thứ tự.\nFunctional core, imperative shell (lõi thuần, vỏ mệnh lệnh): mọi luật nằm trong lõi gồm hàm thuần, nhận giá trị và trả một mô tả quyết định; vỏ mỏng đọc hết những gì lõi cần, gọi lõi một lần, rồi mới ghi theo kết quả.\nLõi test bằng giá trị, không cần đồ giả; vỏ chỉ còn một nhánh nên một bài test tích hợp là đủ.''',
      '''A function that reads the clock, the database and the server, decides, and writes to the outside is hard to test (it needs many fakes) and easy to write in the wrong order.\nFunctional core, imperative shell: every rule lives in a core of pure functions that take values and return a description of the decision; a thin shell reads everything the core needs, calls the core once, and only then writes according to the result.\nThe core is tested with values and needs no fakes; the shell keeps one branch, so one integration test is enough.''')
    a(C + '.goal.g1', '''Đã thấy test cần bao nhiêu đồ giả''', '''Saw how many fakes a test needs''')
    a(C + '.goal.g2', '''Đã thấy vỏ chỉ còn một nhánh''', '''Saw the shell reduced to one branch''')
    a(C + '.sim.fp.core', '''hàm trộn hay lõi thuần và vỏ mỏng''', '''a mixed function or a pure core with a thin shell''')

    S_ = 'hook'
    a(C + '.sec.%s.title' % S_, '''Đoán trước khi đọc''', '''Predict before reading''')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'predict', '''Muốn test luật "đặt lịch thứ Bảy tính 300.000 đ" trong một hàm book() vừa đọc đồng hồ, database, máy chủ, vừa ghi thống kê và log, bài test cần giả bao nhiêu thứ?''',
      '''To test the rule "a Saturday booking costs 300,000 VND" inside a book() function that reads the clock, the database and the server and also writes analytics and logs, how many things must the test fake?''')
    B(C, S_, 1, 'ans', '''Năm: đồng hồ, database, máy chủ, thống kê, log. Luật chỉ là một phép so sánh ngày, nhưng nó bị trộn với mọi việc đụng ra ngoài. Mô phỏng ngay dưới tách hàm đó thành một lõi thuần và một vỏ mỏng.''',
      '''Five: the clock, the database, the server, analytics and logging. The rule is just a date comparison, but it is mixed with all the outside work. The simulation just below splits that function into a pure core and a thin shell.''')

    S_ = 'why'
    a(C + '.sec.%s.title' % S_, '''Vì sao test cần nhiều đồ giả''', '''Why the test needs so many fakes''')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'p', '''Một hàm đặt lịch điển hình làm ba loại việc xen kẽ: đọc từ bên ngoài (đồng hồ, database, máy chủ), quyết định (giờ đã qua chưa, còn trống không, phí bao nhiêu), và ghi ra ngoài (lưu lịch, gửi thống kê, ghi log). Phần quyết định mới là thứ đáng test kỹ, nhưng không gọi riêng được nó: muốn chạy nó phải chạy cả hàm, và mỗi thứ bên ngoài hàm chạm tới cần một đồ giả (mock hay fake, tức vật thay thế dùng trong test).''',
      '''A typical booking function interleaves three kinds of work: reading from outside (the clock, the database, the server), deciding (has the time passed, is the slot free, what is the fee), and writing to outside (saving, analytics, logging). The deciding part is what deserves thorough tests, but it cannot be called on its own: to run it you must run the whole function, and everything outside that the function touches needs a fake (a mock or a fake, a stand-in used in tests).''')
    B(C, S_, 2, 'p', '''Mark Seemann khuyên ưu tiên hàm thuần: chúng dễ ghép, dễ unit test, và lời gọi của chúng thay được bằng kết quả. Còn những query không tất định (đọc đồng hồ, database) và các việc có side effect thì đẩy ra sát rìa hệ thống. [[src:book-seemann]]''',
      '''Mark Seemann recommends favouring pure functions: they compose well, are easy to unit test, and their calls can be replaced by their results. Nondeterministic queries (reading the clock, the database) and work with side effects are pushed to the edge of the system. [[src:book-seemann]]''')

    S_ = 'split'
    a(C + '.sec.%s.title' % S_, '''Lõi thuần, vỏ mỏng''', '''A pure core, a thin shell''')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'p', '''Cách tổ chức này có tên functional core, imperative shell, do Gary Bernhardt đặt; Seemann dùng nó, kể cả cho toàn bộ mã mẫu trong sách của ông. Lõi là các hàm thuần chứa mọi luật: nhận giá trị, trả giá trị. Vỏ là lớp mỏng bên ngoài: đọc mọi thứ lõi cần, gọi lõi, rồi làm theo kết quả (ghi, gửi, hiển thị). Ví dụ của ông là một hàm Post đọc hết dữ liệu, gọi hàm thuần WillAccept, và chỉ ghi khi hàm đó trả true. [[src:book-seemann]]''',
      '''This way of organising code is called functional core, imperative shell, a name coined by Gary Bernhardt; Seemann uses it, including for all the sample code in his book. The core is pure functions holding every rule: values in, values out. The shell is a thin outer layer: it reads everything the core needs, calls the core, and then acts on the result (writes, sends, displays). His example is a Post method that reads all the data, calls the pure WillAccept function, and writes only when it returns true. [[src:book-seemann]]''')
    B(C, S_, 2, 'kt', '''fun decide(req: BookRequest, now: LocalDateTime, slots: Set<String>, quota: Int): Decision = when {
    req.time < now -> Decision.Reject(BookingError.SlotPassed)
    req.slotId !in slots -> Decision.Reject(BookingError.SlotTaken(req.slotId))
    quota == 0 -> Decision.Reject(BookingError.QuotaExceeded)
    else -> Decision.Accept(Booking(req, fee = if (req.day.isWeekend()) 300_000 else 200_000))
}

suspend fun book(req: BookRequest): Decision {
    val d = decide(req, clock.now(), repo.slots(req.day), api.quota(req.phone))   // đọc hết, gọi lõi một lần
    if (d is Decision.Accept) { repo.save(d.booking); analytics.track("booked") }  // rồi mới ghi
    return d
}''', '''fun decide(req: BookRequest, now: LocalDateTime, slots: Set<String>, quota: Int): Decision = when {
    req.time < now -> Decision.Reject(BookingError.SlotPassed)
    req.slotId !in slots -> Decision.Reject(BookingError.SlotTaken(req.slotId))
    quota == 0 -> Decision.Reject(BookingError.QuotaExceeded)
    else -> Decision.Accept(Booking(req, fee = if (req.day.isWeekend()) 300_000 else 200_000))
}

suspend fun book(req: BookRequest): Decision {
    val d = decide(req, clock.now(), repo.slots(req.day), api.quota(req.phone))   // read everything, call the core once
    if (d is Decision.Accept) { repo.save(d.booking); analytics.track("booked") }  // and only then write
    return d
}''')
    B(C, S_, 3, 'p', '''Lõi trả về một mô tả quyết định chứ không tự làm: đúng ý ở chương "Hàm thuần và referential transparency" (trả về "cần thu bao nhiêu" thay vì tự gọi cổng thanh toán). Decision ở đây là một sum type như ở chương "Kiểu dữ liệu đại số"; lõi cũng có thể trả Outcome<BookingError, Booking> như chương "Lỗi là giá trị", hay một danh sách event để reducer ở chương "State thuần: reducer và event" áp vào.''',
      '''The core returns a description of the decision rather than acting on it: the same idea as in the chapter "Pure functions and referential transparency" (return "how much to charge" instead of calling the payment gateway). Decision here is a sum type as in the chapter "Algebraic data types"; the core could also return Outcome<BookingError, Booking> as in "Errors as values", or a list of events for the reducer from "Pure state: reducers and events" to apply.''')

    S_ = 'test'
    a(C + '.sec.%s.title' % S_, '''Test lõi bằng giá trị, test vỏ một lần''', '''Test the core with values, the shell once''')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'kt', '''@Test fun weekendFee() {
    val d = decide(req(slot = "S12", day = SAT_2026_11_28), now = MON_2026_11_23_0800, slots = setOf("S12"), quota = 2)
    assertEquals(300_000, (d as Decision.Accept).booking.fee)
}
@Test fun noQuotaLeft() {
    val d = decide(req(slot = "S12", day = SAT_2026_11_28), now = MON_2026_11_23_0800, slots = setOf("S12"), quota = 0)
    assertEquals(Decision.Reject(BookingError.QuotaExceeded), d)
}''')
    B(C, S_, 2, 'p', '''Mỗi luật có bài test riêng, chỉ dùng giá trị, chạy nhanh và không lúc qua lúc trượt. Vỏ chỉ còn một nhánh (Accept thì ghi, Reject thì thôi), nên một bài test tích hợp cho vỏ là đủ. Cách test theo từng tầng trên Android được nói kỹ ở chương G10, "Kiểm thử theo tầng", của track Kiến trúc app Android.''',
      '''Each rule gets its own test using only values; it runs fast and never flickers between pass and fail. The shell keeps one branch (on Accept write, on Reject do nothing), so one integration test for the shell is enough. Testing Android code layer by layer is covered in chapter G10, "Testing by layer", of the Android App Architecture track.''')
    B(C, S_, 3, 'note', '''Seemann nhận xét thêm: càng nhiều hàm thuần thì càng ít cần log, vì biết đầu vào là tính lại được đầu ra; chỉ cần log các việc không thuần. [[src:book-seemann]]''',
      '''Seemann adds: the more of your code is pure functions, the less you need to log, because knowing the inputs lets you recompute the output; only the impure actions need logging. [[src:book-seemann]]''')
    B(C, S_, 3, 'kind', 'mechanism')

    S_ = 'android'
    a(C + '.sec.%s.title' % S_, '''Trên Android: vỏ nằm ở đâu''', '''On Android: where the shell lives''')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'p', '''Trên Android, vỏ thường là ViewModel hay một use case: nơi gọi repository, đọc đồng hồ, gửi thống kê. Lõi là các hàm thuần mà chúng gọi, có thể đặt trong tầng domain (chương G5, "Domain layer (tùy chọn) và use case", của track Kiến trúc app Android). Dữ liệu từ ngoài nên được kiểm và đổi thành kiểu rõ ràng một lần ở ranh giới trước khi vào lõi (chương J3, "Đóng gói, bất biến, parse một lần", của track Mã sạch và kỷ luật làm nghề).''',
      '''On Android, the shell is usually a ViewModel or a use case: the place that calls the repository, reads the clock, sends analytics. The core is the pure functions they call, which can live in the domain layer (chapter G5, "The domain layer (optional) and use cases", of the Android App Architecture track). Outside data should be checked and turned into a clear type once at the boundary before entering the core (chapter J3, "Encapsulation, immutability, parse once", of the Clean Code and Craft track).''')
    B(C, S_, 2, 'p', '''Lõi thuần không có nghĩa là app không đọc ghi gì; nó chỉ có nghĩa là việc đọc ghi nằm ở một chỗ, ở rìa, theo thứ tự rõ ràng. Massimo Carli còn đi xa hơn với một kiểu IO mô tả cả việc đọc ghi như một giá trị; trong Kotlin, suspend và Flow thường đóng vai đó, nên site không đi sâu vào kiểu IO. [[src:book-fp-tut]]''',
      '''A pure core does not mean the app never reads or writes; it means reading and writing happen in one place, at the edge, in a clear order. Massimo Carli goes further with an IO type that describes reading and writing as a value; in Kotlin, suspend and Flow usually play that role, so the site does not go into the IO type. [[src:book-fp-tut]]''')

    S_ = 'bugs'
    a(C + '.sec.%s.title' % S_, '''Hai lỗi hay gặp''', '''Two common bugs''')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'bug', '''Báo cáo thống kê ghi số lượt đặt lịch cao hơn số lịch thật trong database.''', '''The analytics report shows more bookings than the database actually has.''')
    B(C, S_, 1, 'cause', '''analytics.track("booked") chạy trước các phép kiểm, nên cả lịch bị từ chối cũng được đếm.''', '''analytics.track("booked") runs before the checks, so rejected bookings are counted too.''')
    B(C, S_, 1, 'fix', '''Tách decide() thuần; vỏ chỉ gửi thống kê khi decide() trả Accept.''', '''Extract a pure decide(); the shell sends analytics only when decide() returns Accept.''')
    B(C, S_, 2, 'bug', '''Bài test luật phí cuối tuần chạy mất 4 giây và thỉnh thoảng trượt.''', '''The weekend fee test takes 4 seconds and sometimes fails.''')
    B(C, S_, 2, 'cause', '''Nó gọi cả book(), nên phải dựng 5 đồ giả, và vẫn còn đọc đồng hồ thật ở một chỗ quên giả.''', '''It calls the whole book(), so it builds 5 fakes, and still reads the real clock in one place someone forgot to fake.''')
    B(C, S_, 2, 'fix', '''Test decide() bằng giá trị: ngày, now, giờ trống và số lượt đều do bài test chọn.''', '''Test decide() with values: the day, now, the free slots and the quota are all chosen by the test.''')

    S_ = 'ex'
    a(C + '.sec.%s.title' % S_, '''Bài tập''', '''Exercise''')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'ex', '''Hàm dưới trộn I/O với luật hủy lịch. Tách thành một hàm thuần decideCancel(booking, now) trả CancelDecision, và một vỏ cancel(id) mỏng. Luật: không hủy lịch đã hủy; không hủy khi còn dưới 2 giờ tới giờ khám; hủy trước từ 24 giờ trở lên thì hoàn đủ phí, còn lại hoàn một nửa.''',
      '''The function below mixes I/O with the cancellation rules. Split it into a pure decideCancel(booking, now) returning a CancelDecision, and a thin cancel(id) shell. Rules: an already cancelled booking cannot be cancelled; no cancelling less than 2 hours before the visit; cancelling 24 hours or more before refunds the full fee, otherwise half.''')
    B(C, S_, 1, 'exkt', '''suspend fun cancel(id: Long) {
    val b = repo.find(id) ?: return
    if (b.cancelled) { toast("Lịch đã hủy"); return }
    val hours = Duration.between(LocalDateTime.now(), b.time).toHours()
    if (hours < 2) { toast("Quá sát giờ khám"); return }
    val refund = if (hours >= 24) b.fee else b.fee / 2
    payments.refund(b.id, refund); repo.markCancelled(id); analytics.track("cancelled")
}''', '''suspend fun cancel(id: Long) {
    val b = repo.find(id) ?: return
    if (b.cancelled) { toast("Already cancelled"); return }
    val hours = Duration.between(LocalDateTime.now(), b.time).toHours()
    if (hours < 2) { toast("Too close to the visit"); return }
    val refund = if (hours >= 24) b.fee else b.fee / 2
    payments.refund(b.id, refund); repo.markCancelled(id); analytics.track("cancelled")
}''')
    B(C, S_, 1, 'hint', '''decideCancel nhận booking và now, trả một sealed interface: Refuse(lý do) hoặc Cancel(refund). Vỏ đọc booking và đồng hồ, gọi lõi, rồi hoàn tiền, đánh dấu hủy và gửi thống kê khi kết quả là Cancel.''',
      '''decideCancel takes the booking and now and returns a sealed interface: Refuse(reason) or Cancel(refund). The shell reads the booking and the clock, calls the core, then refunds, marks as cancelled and sends analytics when the result is Cancel.''')
    B(C, S_, 1, 'sol', '''Mọi con số (2 giờ, 24 giờ, hoàn đủ hay một nửa) giờ test được bằng giá trị: now cách giờ khám 30 giờ thì hoàn đủ phí, 10 giờ thì hoàn nửa phí, 1 giờ thì Refuse(TooLate).''',
      '''Every number (2 hours, 24 hours, full or half refund) can now be tested with values: 30 hours before the visit refunds the full fee, 10 hours refunds half, 1 hour gives Refuse(TooLate).''')
    B(C, S_, 1, 'solkt', '''sealed interface CancelDecision {
    data class Refuse(val reason: CancelError) : CancelDecision
    data class Cancel(val refund: Long) : CancelDecision
}

fun decideCancel(b: Booking, now: LocalDateTime): CancelDecision {
    if (b.cancelled) return CancelDecision.Refuse(CancelError.AlreadyCancelled)
    val hours = Duration.between(now, b.time).toHours()
    if (hours < 2) return CancelDecision.Refuse(CancelError.TooLate)
    return CancelDecision.Cancel(refund = if (hours >= 24) b.fee else b.fee / 2)
}

suspend fun cancel(id: Long): CancelDecision? {
    val b = repo.find(id) ?: return null
    val d = decideCancel(b, clock.now())
    if (d is CancelDecision.Cancel) { payments.refund(b.id, d.refund); repo.markCancelled(id); analytics.track("cancelled") }
    return d
}''')

    S_ = 'recall'
    a(C + '.sec.%s.title' % S_, '''Tự trả lời''', '''Answer it yourself''')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'ask', '''Lõi và vỏ, mỗi bên chứa gì?''', '''What goes in the core, and what in the shell?''')
    B(C, S_, 1, 'ans', '''Lõi: các hàm thuần chứa luật, nhận và trả giá trị. Vỏ: đọc đồng hồ, database, máy chủ; gọi lõi; rồi ghi, gửi, hiển thị theo kết quả.''',
      '''The core: pure functions holding the rules, values in and out. The shell: reads the clock, the database, the server; calls the core; then writes, sends and displays according to the result.''')
    B(C, S_, 2, 'ask', '''Vì sao vỏ nên ghi sau khi lõi đã quyết định xong?''', '''Why should the shell write only after the core has decided?''')
    B(C, S_, 2, 'ans', '''Để không có lần ghi nào cho một yêu cầu rồi bị từ chối, và thứ tự đọc, quyết định, ghi luôn rõ ràng.''', '''So that nothing is written for a request that is then rejected, and the order of reading, deciding and writing is always clear.''')

    for q, qv, qe, av, ae, wv, we in [
        ('q1', 'Hàm đọc clock.now() bên trong có thuần không?', 'Is a function that reads clock.now() inside pure?', 'Không.', 'No.',
         'Cùng đầu vào có thể cho kết quả khác tùy lúc gọi.', 'The same input can give different results depending on when it is called.'),
        ('q2', 'Test một hàm decide() thuần cần bao nhiêu đồ giả?', 'How many fakes does testing a pure decide() need?', 'Không cần cái nào.', 'None.',
         'Mọi thứ nó cần là tham số, do bài test chọn.', 'Everything it needs is a parameter chosen by the test.'),
        ('q3', 'Theo Seemann, việc không tất định và side effect nên nằm ở đâu?', 'According to Seemann, where should nondeterminism and side effects go?', 'Sát rìa hệ thống: Main, controller, ViewModel…', 'At the edge of the system: Main, controllers, ViewModels…',
         'Phần còn lại viết thành hàm thuần.', 'The rest is written as pure functions.'),
        ('q4', 'Vỏ mỏng còn những nhánh nào?', 'What branches does a thin shell keep?', 'Chỉ nhánh làm theo kết quả của lõi, như Accept thì ghi, Reject thì báo lý do.', 'Only the branch acting on the core\'s result, such as write on Accept, report on Reject.',
         'Mọi luật đã nằm trong lõi.', 'Every rule already lives in the core.')]:
        a(C + '.quiz.%s.q' % q, qv, qe); a(C + '.quiz.%s.a' % q, av, ae); a(C + '.quiz.%s.why' % q, wv, we)
