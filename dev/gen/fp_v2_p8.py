# Lập trình hàm · K8 (p8): state thuần: reducer và event (Phần 2: lỗi, ngữ cảnh và state)
# Nguồn (chỉ ghi ở đây và docs/research/fp.md): Barbini, From Objects to Functions ch.5 (Event Sourcing: lưu thay đổi kèm lý do, bốn lợi ích và cái giá;
# Folding Events; máy trạng thái bằng sealed class), ch.6 (command-oriented interface, command mang id tạo sẵn; Understanding Commands and Events Better:
# nhiều event, ít command; Mutable and Immutable State); Carli ch.15 (state là giá trị đổi được; kiểu State, chỉ nhắc). Giọng văn dạy học.

SEC_ORDER = {'p8': ['hook', 'why', 'reduce', 'log', 'android', 'bugs', 'ex', 'recall']}


def add(a):
    def B(ch, sec, n, field, vi, en=None):
        a('%s.sec.%s.b.%02d.%s' % (ch, sec, n, field), vi, vi if en is None else en)

    a('preset.reducer', '''Lập trình hàm · reducer và nhật ký event''', '''Functional programming · reducers and an event log''')
    m = lambda k, vi, en=None: a('m.reducer.' + k, vi, en)
    m('title', '''Số lượt khám còn lại: một biến hay một nhật ký event''', '''Visits left: one variable or an event log''')
    m('overview', '''Gói khám 5 lượt của app Hẹn Khám. Bốn việc xảy ra: mua gói, đặt lịch #41, đặt lịch #42, hủy lịch #41; đúng ra còn 4 lượt. Cách 1 giữ một biến remaining mà màn đặt lịch và bước đồng bộ cùng sửa. Cách 2 ghi mỗi việc thành một event và tính state bằng một hàm reduce thuần.''',
      '''A ClinicBook package of 5 visits. Four things happen: the package is bought, booking #41, booking #42, booking #41 is cancelled; 4 visits should be left. Way 1 keeps a remaining variable that both the booking screen and the sync step modify. Way 2 records each thing as an event and computes the state with a pure reduce function.''')
    m('wrapup', '''Biến bị hai chỗ cùng trừ cho 2 thay vì 4, và không có lịch sử để tìm ra vì sao. Nhật ký event cùng reduce thuần cho đúng 4, cho state sau từng event, và dựng lại được state ở quá khứ. Phát lại chỉ đúng khi reduce thuần: id phải nằm sẵn trong event chứ không được sinh ra trong reduce.''',
      '''The variable subtracted in two places gives 2 instead of 4, with no history to find out why. An event log with a pure reduce gives the correct 4, the state after each event, and can rebuild past states. Replaying is only correct when reduce is pure: the id must already be in the event, not created inside reduce.''')
    m('simp.1', '''Nhật ký chỉ có bốn event và một loại state; ứng dụng thật còn phải lưu nhật ký, xử lý event trùng và nâng cấp định dạng event.''',
      '''The log has just four events and one kind of state; a real app must also store the log, handle duplicate events and migrate the event format.''')
    m('simp.2', '''fold, runningFold và cả hai cách đều chạy thật bằng JavaScript trên cùng bốn việc; reducer không thuần ở bước 4 sinh id mới ở mỗi lần chạy. Đoạn Kotlin chỉ để minh họa; site không chạy Kotlin trong trang.''',
      '''fold, runningFold and both ways really run in JavaScript on the same four events; the impure reducer at step 4 creates a new id on each run. The Kotlin code is illustrative; the site does not run Kotlin in the page.''')
    m('ctl.hint', '''Chọn cách giữ state rồi đi qua bốn bước; so cột "đúng phải là" với cột của cách đang chọn.''', '''Pick a way of keeping state and walk the four steps; compare the "should be" column with the column of the chosen way.''')
    m('ctl.case', '''Cách giữ state''', '''How state is kept''')
    m('ctl.case.mutable', '''một biến, nhiều chỗ sửa''', '''one variable, many writers'''); m('ctl.case.events', '''nhật ký event và reduce''', '''an event log and reduce''')
    m('diagramTitle', '''Màn đặt lịch, bước đồng bộ, nhật ký event, reduce, state''', '''Booking screen, sync step, event log, reduce, state''')
    m('diagramDesc', '''Hai chỗ cùng sửa state, hay chỉ thêm event vào nhật ký để reduce tính state''', '''Two places modify the state, or they only add events to the log so reduce computes the state''')
    for k, vi, en in [('ui', 'Màn đặt lịch', 'Booking screen'), ('sync', 'Bước đồng bộ', 'Sync step'), ('state', 'State (số lượt)', 'State (visits left)'), ('log', 'Nhật ký event', 'Event log'), ('reduce', 'reduce (hàm thuần)', 'reduce (pure function)')]:
        m('n.' + k, vi, en)
    m('met.app', '''App đang giữ''', '''The app holds'''); m('met.want', '''Đúng phải là''', '''Should be''')
    m('met.writers', '''Số chỗ sửa state''', '''Places that modify state'''); m('met.count', '''Event trong nhật ký''', '''Events in the log''')
    a('cap.reducer', '''Màn hình và bước đồng bộ cùng sửa state, hoặc chỉ ghi event vào nhật ký để reduce tính state. Ô đỏ: số app giữ khác số đúng.''',
      '''The screen and the sync step both modify the state, or they only write events to the log for reduce to compute the state. A red box: the number the app holds differs from the correct one.''')
    S = [
        ('mutable', 's1', 'Đặt lịch #41: số lượt tụt 2', 'Booking #41: visits drop by 2',
         'Gói khám 5 lượt. Đặt lịch #41: màn đặt lịch trừ remaining một lần, rồi khi máy chủ xác nhận, bước đồng bộ trừ thêm một lần. Đúng phải còn 4, app giữ 3. Hai chỗ cùng sửa một biến, chỗ nào cũng tưởng mình là chỗ duy nhất.',
         'A 5-visit package. Booking #41: the booking screen subtracts one from remaining, then when the server confirms, the sync step subtracts one more. It should be 4, the app holds 3. Two places modify one variable, each believing it is the only one.'),
        ('mutable', 's2', 'Đặt #42, hủy #41: lệch ngày càng xa', 'Book #42, cancel #41: the gap grows',
         'Đặt #42 lại bị trừ hai lần; hủy #41 cộng một lần. Đúng phải còn 4, app giữ 2. Mỗi lần đặt lịch thêm một lần lệch, và không chỗ nào ghi lại vì sao.',
         'Booking #42 is again subtracted twice; cancelling #41 adds one. It should be 4, the app holds 2. Every booking adds another error, and nothing records why.'),
        ('mutable', 's3', 'Không có lịch sử để kiểm lại', 'No history to check against',
         'Người dùng hỏi: "Sau khi đặt #41 tôi còn mấy lượt?" App chỉ có con số hiện tại là 2; các giá trị trước đã bị ghi đè. Muốn biết sai từ đâu, phải đọc mọi chỗ có remaining-- hay remaining++.',
         'The user asks: "How many visits did I have after booking #41?" The app only has the current number, 2; earlier values were overwritten. To find where it went wrong, you must read every place with remaining-- or remaining++.'),
        ('mutable', 's4', 'Mở lại app: chỉ còn con số sai', 'Reopening the app: only the wrong number is left',
         'App lưu remaining = 2 rồi bị đóng. Mở lại, số đó được nạp lên như thể đúng. Không có gì để tính lại từ đầu, nên lỗi ở lại mãi.',
         'The app saves remaining = 2 and is closed. On reopening, that number is loaded as if it were right. There is nothing to recompute from, so the error stays forever.'),
        ('events', 's1', 'Chỉ reduce đổi state', 'Only reduce changes the state',
         'Mỗi việc xảy ra được ghi thành một event: PackageBought(5), rồi VisitBooked(41). State là kết quả của fold(Quota(), ::reduce) trên nhật ký. Màn hình và bước đồng bộ không sửa state; chúng chỉ thêm event. Còn 4 lượt, đúng.',
         'Each thing that happens is recorded as an event: PackageBought(5), then VisitBooked(41). The state is the result of fold(Quota(), ::reduce) over the log. The screen and the sync step do not modify the state; they only add events. 4 visits left, correct.'),
        ('events', 's2', 'Mỗi event qua đúng một lần reduce', 'Each event goes through reduce exactly once',
         'Thêm VisitBooked(42) và VisitCancelled(41). reduce là chỗ duy nhất biết "đặt lịch thì trừ 1, hủy thì cộng 1", nên không thể bị trừ hai lần. runningFold cho state sau từng event: 5, 4, 3, 4.',
         'Add VisitBooked(42) and VisitCancelled(41). reduce is the only place that knows "a booking subtracts 1, a cancellation adds 1", so nothing gets subtracted twice. runningFold gives the state after each event: 5, 4, 3, 4.'),
        ('events', 's3', 'Dựng lại state ở thời điểm bất kỳ', 'Rebuilding the state at any point',
         'Muốn biết sau khi đặt #41 còn mấy lượt: fold hai event đầu, được 4. Vì reduce thuần, phát lại bao nhiêu lần cũng ra cùng kết quả, và ta còn biết vì sao mỗi con số đổi.',
         'To know how many visits were left after booking #41: fold the first two events and get 4. Because reduce is pure, replaying any number of times gives the same result, and we also know why each number changed.'),
        ('events', 's4', 'Phát lại bằng một reducer không thuần', 'Replaying with an impure reducer',
         'Một phiên bản reduce tự sinh id cho lịch (như gọi UUID.randomUUID() để lấy một mã ngẫu nhiên) thay vì lấy id từ event. Lần chạy đầu khớp, nhưng khi phát lại, lịch #41 nhận id mới, nên VisitCancelled(41) không tìm thấy lịch nào và không cộng lại lượt: ra 3 thay vì 4. Cách sửa: id được tạo một lần khi nhận lệnh, rồi nằm sẵn trong event.',
         'A version of reduce creates the booking id itself (like calling UUID.randomUUID() for a random code) instead of taking it from the event. The first run matches, but on replay booking #41 gets a new id, so VisitCancelled(41) finds no booking and does not give the visit back: 3 instead of 4. The fix: the id is created once when the request comes in, and is already in the event.'),
    ]
    for case, k, tv, te, xv, xe in S:
        sid = case + '.' + k
        m('s.%s.title' % sid, tv, te); m('s.%s.explain' % sid, xv, xe); m('ev.' + sid, tv, te)
    for k, vi, en in [
        ('try', '''Mẹo đọc: mỗi hàng là một việc đã xảy ra với gói khám. So cột "đúng phải là" với cột của cách đang chọn; ô đỏ là chỗ app giữ sai.''',
         '''Reading tip: each row is something that happened to the package. Compare the "should be" column with the chosen way\'s column; a red cell is where the app holds a wrong number.'''),
        ('mutable.s2', '''Uberto Barbini chỉ ra cái giá của việc chỉ lưu state mới nhất: không còn biết thay đổi xảy ra khi nào và vì sao. [[src:book-barbini]]''',
         '''Uberto Barbini points out the cost of storing only the latest state: you no longer know when or why a change happened. [[src:book-barbini]]'''),
        ('mutable.s3', '''Barbini: lập trình hàm đẩy mọi thay đổi state ra rìa để logic chính khỏi phải lo; hướng đối tượng giấu thay đổi bên trong object, và ta không bao giờ chắc hết hệ quả của một lần sửa. [[src:book-barbini]]''',
         '''Barbini: functional programming keeps all state changes at the edges so the core logic can ignore them; object orientation hides changes inside objects, and we are never quite sure of a change\'s consequences. [[src:book-barbini]]'''),
        ('mutable.s4', '''Xóa một dòng remaining-- chỉ chữa triệu chứng; chỗ thứ ba cùng sửa biến sẽ đem lỗi quay lại. Chương "Bất biến, dữ liệu dùng chung và đệ quy" của track này nói vì sao dữ liệu dùng chung mà sửa được thì khó lần ra lỗi.''',
         '''Deleting one remaining-- line only treats the symptom; a third place modifying the variable will bring the bug back. This track\'s chapter "Immutability, data sharing and recursion" explains why shared mutable data makes bugs hard to trace.'''),
        ('events.s1', '''Event sourcing (lưu các event thay cho state): thay vì lưu state mới sau mỗi lần đổi, chỉ lưu sự thay đổi kèm lý do nghiệp vụ. Barbini kể bốn lợi ích: giữ lý do, có dữ liệu kiểm toán, dựng lại state ở quá khứ, và dễ tạo nhiều cách nhìn trên cùng dữ liệu. [[src:book-barbini]]''',
         '''Event sourcing (storing events instead of state): rather than saving the new state after each change, save only the change with its business reason. Barbini lists four benefits: keeping the reason, audit data, rebuilding past states, and easily creating several views of the same data. [[src:book-barbini]]'''),
        ('events.s2', '''runningFold của thư viện chuẩn trả mọi giá trị trung gian của fold, bắt đầu từ giá trị ban đầu; đó đúng là cột "state sau từng event".''',
         '''The standard library\'s runningFold returns every intermediate value of a fold, starting with the initial value; that is exactly the "state after each event" column.'''),
        ('events.s3', '''Barbini: để biết state ở một thời điểm trong quá khứ, chỉ cần xử lý mọi event tới thời điểm đó. [[src:book-barbini]]''',
         '''Barbini: to know the state at a point in the past, just process all the events up to that point. [[src:book-barbini]]'''),
        ('events.s4', '''Barbini tạo id ngẫu nhiên ngay trong command, trước khi có event, nên hàm gộp event vẫn thuần. Đọc đồng hồ hay sinh số ngẫu nhiên trong reduce lặp lại đúng lỗi ở chương "Hàm thuần và referential transparency". [[src:book-barbini]]''',
         '''Barbini mints the random id inside the command, before any event exists, so the function folding events stays pure. Reading the clock or making random numbers inside reduce repeats exactly the bug from the chapter "Pure functions and referential transparency". [[src:book-barbini]]'''),
    ]:
        m('co.' + k, vi, en)

    z = lambda k, vi, en=None: a('vz.' + k, vi, en)
    z('tab.reducer', '''Nhật ký event''', '''Event log''')
    for k, vi, en in [('n', '#', '#'), ('event', 'Việc đã xảy ra (event)', 'What happened (event)'), ('want', 'Đúng phải là', 'Should be'), ('var', 'Biến remaining', 'The remaining variable'),
                      ('state', 'State từ reduce', 'State from reduce'), ('replay', 'Phát lại (reducer tự sinh id)', 'Replay (reducer creates ids)')]:
        z('reducer.col.' + k, vi, en)
    z('reducer.cap.mutable', '''Cách 1: biến remaining, màn đặt lịch và bước đồng bộ cùng sửa.''', '''Way 1: a remaining variable that the booking screen and the sync step both modify.''')
    z('reducer.cap.events', '''Cách 2: nhật ký event; state = events.fold(Quota(), ::reduce).''', '''Way 2: an event log; state = events.fold(Quota(), ::reduce).''')
    z('reducer.now', '''App đang giữ {a} lượt; đúng phải là {w}.''', '''The app holds {a} visits; it should be {w}.''')
    z('reducer.note.mutable.0', '''Mỗi lần đặt lịch, biến bị trừ ở hai chỗ.''', '''Every booking subtracts from the variable in two places.''')
    z('reducer.note.mutable.1', '''Lệch tăng dần sau mỗi lần đặt.''', '''The gap grows with every booking.''')
    z('reducer.note.mutable.2', '''Chỉ còn con số hiện tại; các giá trị trước đã bị ghi đè.''', '''Only the current number is left; earlier values were overwritten.''')
    z('reducer.note.events', '''Màn hình và bước đồng bộ chỉ thêm event; reduce là chỗ duy nhất đổi state.''', '''The screen and the sync step only add events; reduce is the only place that changes the state.''')
    z('reducer.note.replay', '''Dựng lại state sau event 2 (đặt lịch #41): fold hai event đầu được 4 lượt.''', '''Rebuilding the state after event 2 (booking #41): folding the first two events gives 4 visits.''')
    z('reducer.note.impure', '''Cột cuối: phát lại cùng nhật ký bằng một reducer tự sinh id. Hủy #41 không khớp lịch nào nên không cộng lại lượt.''', '''Last column: replaying the same log with a reducer that creates ids. Cancelling #41 matches no booking, so the visit is not given back.''')
    z('reducer.legend', '''Đỏ: số khác với "đúng phải là". Viền: event được dựng lại tới đó. Mỗi hàng là một việc đã xảy ra, theo đúng thứ tự.''',
      '''Red: a number different from "should be". Outlined: the event the state was rebuilt up to. Each row is something that happened, in order.''')

    C = 'p8'
    a(C + '.title', '''State thuần: reducer và event''', '''Pure state: reducers and events''')
    a(C + '.essence', '''Một biến bị nhiều chỗ sửa thì dễ sai mà không ai biết: hai chỗ cùng trừ một lượt, và không còn dấu vết vì sao.\nCách làm theo lập trình hàm: mỗi việc xảy ra là một event; một hàm thuần reduce(state, event) là chỗ duy nhất đổi state; state hiện tại là events.fold(initial, ::reduce), và runningFold cho state sau từng event.\nLưu nhật ký event (event sourcing) cho phép dựng lại state ở bất kỳ thời điểm nào, miễn là reduce thuần: id, giờ, số ngẫu nhiên phải nằm sẵn trong event.''',
      '''A variable modified in many places goes wrong without anyone noticing: two places subtract the same visit, and nothing records why.\nThe functional way: each thing that happens is an event; a pure function reduce(state, event) is the only place that changes the state; the current state is events.fold(initial, ::reduce), and runningFold gives the state after each event.\nStoring the event log (event sourcing) lets you rebuild the state at any point, as long as reduce is pure: ids, times and random numbers must already be in the event.''')
    a(C + '.goal.g1', '''Đã thấy state lệch hoặc đúng sau từng việc''', '''Saw the state go wrong or stay right after each event''')
    a(C + '.goal.g2', '''Đã thấy phát lại nhật ký''', '''Saw the log replayed''')
    a(C + '.sim.fp.reducer', '''một biến nhiều chỗ sửa hay nhật ký event''', '''one variable with many writers or an event log''')

    S_ = 'hook'
    a(C + '.sec.%s.title' % S_, '''Đoán trước khi đọc''', '''Predict before reading''')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'predict', '''Gói khám 5 lượt. Màn đặt lịch gọi remaining-- khi người dùng bấm "Đặt", và bước đồng bộ cũng gọi remaining-- khi máy chủ xác nhận. Đặt 2 lịch rồi hủy 1, app hiện còn mấy lượt? Đúng ra phải còn mấy?''',
      '''A 5-visit package. The booking screen calls remaining-- when the user taps "Book", and the sync step also calls remaining-- when the server confirms. After booking 2 and cancelling 1, how many visits does the app show? How many should be left?''')
    B(C, S_, 1, 'ans', '''App hiện 2, đúng ra là 4. Mỗi lần đặt bị trừ hai lần vì có hai chỗ cùng sửa một biến. Mô phỏng ngay dưới so cách đó với cách ghi lại các việc đã xảy ra rồi tính state bằng một hàm thuần.''',
      '''The app shows 2; it should be 4. Each booking is subtracted twice because two places modify one variable. The simulation just below compares that with recording what happened and computing the state with a pure function.''')

    S_ = 'why'
    a(C + '.sec.%s.title' % S_, '''Khi nhiều chỗ cùng sửa một biến''', '''When many places modify one variable''')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'p', '''State là những giá trị đổi theo thời gian: số lượt còn lại, danh sách lịch đã đặt. Cách quen thuộc là một biến và nhiều hàm sửa nó. Khi chỉ có một chỗ sửa thì ổn. Khi màn hình, bước đồng bộ và thông báo đẩy đều sửa cùng một biến, mỗi chỗ chỉ biết phần việc của mình, và hai chỗ có thể cùng làm một việc. Kết quả sai mà không có lỗi nào được báo.''',
      '''State is the values that change over time: visits left, the list of bookings. The familiar way is one variable and many functions modifying it. With a single writer, that is fine. When the screen, the sync step and push notifications all modify the same variable, each knows only its own part, and two of them may do the same job. The result is wrong, and no error is reported.''')
    B(C, S_, 2, 'p', '''Uberto Barbini chỉ ra một vấn đề sâu hơn: khi chỉ lưu state mới nhất, ta mất luôn thông tin thay đổi xảy ra khi nào và vì sao. Con số 2 không kể được nó đến từ đâu. Lập trình hàm làm ngược lại: giữ logic đổi state trong một hàm thuần, và đẩy việc lưu, việc hiển thị ra rìa. [[src:book-barbini]]''',
      '''Uberto Barbini points to a deeper problem: when only the latest state is stored, we also lose when and why each change happened. The number 2 cannot tell where it came from. Functional programming does the opposite: keep the state-changing logic in a pure function, and push storing and displaying to the edges. [[src:book-barbini]]''')

    S_ = 'reduce'
    a(C + '.sec.%s.title' % S_, '''Một hàm thuần: reduce(state, event)''', '''One pure function: reduce(state, event)''')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'p', '''Thay vì sửa biến, mỗi việc xảy ra được mô tả thành một event: một data class đặt tên ở thì quá khứ, như VisitBooked(41). Rồi viết một hàm thuần duy nhất reduce(state, event) trả state mới. Chỉ hàm này biết "đặt lịch thì trừ 1, hủy thì cộng 1"; màn hình và bước đồng bộ chỉ tạo event. Event là một sealed interface, nên when trong reduce phải xử lý đủ mọi loại event (chương "Kiểu dữ liệu đại số" của track này).''',
      '''Instead of modifying a variable, each thing that happens is described as an event: a data class named in the past tense, such as VisitBooked(41). Then write one pure function reduce(state, event) returning the new state. Only this function knows "a booking subtracts 1, a cancellation adds 1"; the screen and the sync step only create events. Event is a sealed interface, so the when inside reduce must handle every kind of event (this track\'s chapter "Algebraic data types").''')
    B(C, S_, 2, 'kt', '''fun reduce(s: Quota, e: Event): Quota = when (e) {
    is Event.PackageBought -> s.copy(remaining = e.visits)
    is Event.VisitBooked -> s.copy(remaining = s.remaining - 1, active = s.active + e.bookingId)
    is Event.VisitCancelled ->
        if (e.bookingId in s.active) s.copy(remaining = s.remaining + 1, active = s.active - e.bookingId) else s
}
val current = events.fold(Quota(), ::reduce)            // remaining = 4
val history = events.runningFold(Quota(), ::reduce)     // remaining: 0, 5, 4, 3, 4''')
    B(C, S_, 3, 'p', '''fold đi qua nhật ký từ trái sang phải, mỗi lần đưa state hiện tại và một event vào reduce. runningFold làm như fold nhưng giữ lại mọi state trung gian, bắt đầu từ state ban đầu: đúng là bảng "state sau từng event". Barbini gọi đây là gộp event (folding events), và dùng sealed class để mô tả các trạng thái của một máy trạng thái (thứ chỉ chuyển trạng thái khi nhận event hợp lệ). [[src:book-barbini]]''',
      '''fold walks the log from left to right, each time passing the current state and one event to reduce. runningFold works like fold but keeps every intermediate state, starting with the initial one: exactly the "state after each event" table. Barbini calls this folding events, and uses sealed classes to describe the states of a state machine (something that only changes state on a valid event). [[src:book-barbini]]''')

    S_ = 'log'
    a(C + '.sec.%s.title' % S_, '''Nhật ký event: dựng lại, phát lại, command và event''', '''The event log: rebuilding, replaying, commands and events''')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'p', '''Lưu các event thay cho state gọi là event sourcing. Lợi ích, theo Barbini: giữ được lý do của mỗi thay đổi, có dữ liệu kiểm toán, dựng lại state ở bất kỳ thời điểm nào trong quá khứ (chỉ cần fold các event tới thời điểm đó), và tạo nhiều cách nhìn khác nhau trên cùng dữ liệu. Cái giá: phức tạp hơn, đội phải học cách làm mới, và không đáng làm khi miền nghiệp vụ ít logic. [[src:book-barbini]]''',
      '''Storing events instead of state is called event sourcing. The benefits, according to Barbini: keeping the reason for each change, audit data, rebuilding the state at any point in the past (just fold the events up to that point), and creating different views of the same data. The cost: more complexity, new techniques for the team to learn, and it is not worth it when the domain has little business logic. [[src:book-barbini]]''')
    B(C, S_, 2, 'p', '''Phát lại chỉ cho cùng kết quả khi reduce thuần. Nếu reduce đọc đồng hồ, sinh số ngẫu nhiên hay UUID, mỗi lần phát lại ra một state khác: đúng lỗi ở chương "Hàm thuần và referential transparency". Những giá trị như thế được tạo một lần, ở ngoài, rồi ghi vào event. [[src:book-barbini]]''',
      '''Replaying only gives the same result when reduce is pure. If reduce reads the clock or creates random numbers or UUIDs, every replay gives a different state: exactly the bug from the chapter "Pure functions and referential transparency". Such values are created once, outside, and written into the event. [[src:book-barbini]]''')
    B(C, S_, 3, 'p', '''Command khác event. Command là một yêu cầu (đặt lịch #43), có thể bị từ chối, ví dụ khi đã hết lượt; event là việc đã xảy ra (đã đặt lịch #43), nên chỉ việc áp vào state. Barbini khuyên có nhiều event, mỗi thay đổi một event, nhưng ít command, vì command là API công khai của hệ thống còn event nằm bên trong domain. [[src:book-barbini]]''',
      '''A command differs from an event. A command is a request (book #43) that may be rejected, for example when no visits are left; an event is something that already happened (#43 was booked), so it is simply applied to the state. Barbini recommends many events, one per change, but few commands, because commands are the system\'s public API while events stay inside the domain. [[src:book-barbini]]''')

    S_ = 'android'
    a(C + '.sec.%s.title' % S_, '''Trên Android: reducer trong ViewModel và Flow''', '''On Android: a reducer in a ViewModel and in a Flow''')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'p', '''Trên Android, một ViewModel có thể giữ state trong một StateFlow và cập nhật nó bằng reducer. Màn hình chỉ gửi event; không chỗ nào khác sửa state. Cách nối reducer vào ViewModel và màn hình, tức mô hình MVI, là chủ đề của chương G7, "MVVM và MVI", của track Kiến trúc app Android; chương này chỉ lo phần hàm thuần.''',
      '''On Android, a ViewModel can hold the state in a StateFlow and update it with a reducer. The screen only sends events; nothing else modifies the state. Wiring the reducer into the ViewModel and the screen, the MVI pattern, is the topic of chapter G7, "MVVM and MVI", of the Android App Architecture track; this chapter only covers the pure-function part.''')
    B(C, S_, 2, 'kt', '''private val _state = MutableStateFlow(Quota())
val state: StateFlow<Quota> = _state

fun onEvent(e: Event) { _state.update { reduce(it, e) } }      // chỗ duy nhất đổi state
// hoặc khi các event đến dưới dạng một Flow:
val quota: Flow<Quota> = events.scan(Quota(), ::reduce)''', '''private val _state = MutableStateFlow(Quota())
val state: StateFlow<Quota> = _state

fun onEvent(e: Event) { _state.update { reduce(it, e) } }      // the only place that changes state
// or when the events arrive as a Flow:
val quota: Flow<Quota> = events.scan(Quota(), ::reduce)''')
    B(C, S_, 3, 'p', '''Với Flow (dòng giá trị bất đồng bộ của coroutine), toán tử scan là runningFold theo thời gian: mỗi event mới cho ra một state mới (chương "Xử lý flow: map, filter, scan, merge/zip/combine, flatMap, retry, distinct" của track Kotlin Coroutines Explorer). Massimo Carli còn mô tả một kiểu State riêng cho việc chuyển trạng thái; site không đi sâu vào kiểu đó. [[src:book-fp-tut]]''',
      '''With a Flow (an asynchronous stream of values from coroutines), the scan operator is runningFold over time: every new event produces a new state (the chapter "Flow processing: map, filter, scan, merge/zip/combine, flatMap, retry, distinct" of the Kotlin Coroutines Explorer track). Massimo Carli also describes a dedicated State type for state transitions; the site does not go into that type. [[src:book-fp-tut]]''')

    S_ = 'bugs'
    a(C + '.sec.%s.title' % S_, '''Hai lỗi hay gặp''', '''Two common bugs''')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'bug', '''Đặt 2 lịch, app báo chỉ còn 1 lượt dù gói có 5.''', '''After booking 2 visits, the app says only 1 is left in a 5-visit package.''')
    B(C, S_, 1, 'cause', '''Màn đặt lịch và bước đồng bộ cùng trừ remaining, nên mỗi lịch bị trừ hai lần.''', '''The booking screen and the sync step both subtract from remaining, so each booking is subtracted twice.''')
    B(C, S_, 1, 'fix', '''Chỉ reduce biến việc "đã đặt lịch" thành thay đổi state. Bước đồng bộ chỉ xác nhận event đã có, không tạo thêm thay đổi.''', '''Only reduce turns "a booking happened" into a state change. The sync step only confirms the existing event and adds no change of its own.''')
    B(C, S_, 2, 'bug', '''Sau khi dựng lại state từ nhật ký, lịch đã hủy vẫn bị tính là đang giữ một lượt.''', '''After rebuilding the state from the log, a cancelled booking still counts as holding a visit.''')
    B(C, S_, 2, 'cause', '''reduce tự sinh id cho lịch bằng UUID.randomUUID(); mỗi lần phát lại id khác đi, nên event hủy không khớp lịch nào.''', '''reduce creates the booking id itself with UUID.randomUUID(); each replay gives a different id, so the cancel event matches no booking.''')
    B(C, S_, 2, 'fix', '''Tạo id một lần khi nhận lệnh đặt lịch rồi ghi vào event; reduce chỉ đọc id từ event.''', '''Create the id once, when the booking request arrives, and write it into the event; reduce only reads the id from the event.''')

    S_ = 'ex'
    a(C + '.sec.%s.title' % S_, '''Bài tập''', '''Exercise''')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'ex', '''Thêm event PackageExtended(visits: Int) cộng thêm lượt, và VisitCompleted(bookingId) đánh dấu đã khám xong (không đổi số lượt, nhưng lịch đó không còn hủy được). Viết lại reduce. Rồi với nhật ký [PackageBought(5), VisitBooked(41), VisitCompleted(41), VisitCancelled(41), PackageExtended(3)], dùng runningFold: số lượt sau từng event là bao nhiêu?''',
      '''Add the event PackageExtended(visits: Int), which adds visits, and VisitCompleted(bookingId), which marks a visit as done (no change to visits left, but that booking can no longer be cancelled). Rewrite reduce. Then for the log [PackageBought(5), VisitBooked(41), VisitCompleted(41), VisitCancelled(41), PackageExtended(3)], use runningFold: how many visits are left after each event?''')
    B(C, S_, 1, 'hint', '''Thêm một tập done cho lịch đã khám; VisitCancelled chỉ cộng lại lượt khi lịch còn nằm trong active.''', '''Add a done set for completed visits; VisitCancelled only gives a visit back while the booking is still in active.''')
    B(C, S_, 1, 'sol', '''Số lượt: 0 (ban đầu), 5, 4, 4, 4 (lần hủy bị bỏ qua vì lịch đã khám xong), 7. Vì Event là sealed interface, thêm hai loại event làm when trong reduce báo thiếu nhánh cho tới khi bạn xử lý chúng.''',
      '''Visits left: 0 (initial), 5, 4, 4, 4 (the cancellation is ignored because the visit is done), 7. Because Event is a sealed interface, adding two kinds of event makes the when in reduce report missing branches until you handle them.''')
    B(C, S_, 1, 'solkt', '''data class Quota(val remaining: Int = 0, val active: Set<Long> = emptySet(), val done: Set<Long> = emptySet())

fun reduce(s: Quota, e: Event): Quota = when (e) {
    is Event.PackageBought -> s.copy(remaining = e.visits)
    is Event.PackageExtended -> s.copy(remaining = s.remaining + e.visits)
    is Event.VisitBooked -> s.copy(remaining = s.remaining - 1, active = s.active + e.bookingId)
    is Event.VisitCompleted -> s.copy(active = s.active - e.bookingId, done = s.done + e.bookingId)
    is Event.VisitCancelled ->
        if (e.bookingId in s.active) s.copy(remaining = s.remaining + 1, active = s.active - e.bookingId) else s
}
// runningFold → remaining: 0, 5, 4, 4, 4, 7''')

    S_ = 'recall'
    a(C + '.sec.%s.title' % S_, '''Tự trả lời''', '''Answer it yourself''')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'ask', '''Vì sao reduce phải là hàm thuần?''', '''Why must reduce be a pure function?''')
    B(C, S_, 1, 'ans', '''Để phát lại nhật ký bao nhiêu lần cũng ra cùng state. Đồng hồ, số ngẫu nhiên hay UUID phải được tạo ở ngoài rồi ghi vào event.''',
      '''So that replaying the log any number of times gives the same state. Clock readings, random numbers and UUIDs must be created outside and written into the event.''')
    B(C, S_, 2, 'ask', '''Command và event khác nhau thế nào?''', '''How does a command differ from an event?''')
    B(C, S_, 2, 'ans', '''Command là yêu cầu, có thể bị từ chối; event là việc đã xảy ra, đặt tên ở thì quá khứ, chỉ việc áp vào state.''',
      '''A command is a request that may be rejected; an event is something that already happened, named in the past tense, and is simply applied to the state.''')

    for q, qv, qe, av, ae, wv, we in [
        ('q1', '`listOf(1, 2, 3).runningFold(0) { a, x -> a + x }` cho gì?', 'What does `listOf(1, 2, 3).runningFold(0) { a, x -> a + x }` give?', 'Danh sách [0, 1, 3, 6].', 'The list [0, 1, 3, 6].',
         'runningFold giữ mọi giá trị trung gian, bắt đầu từ giá trị ban đầu.', 'runningFold keeps every intermediate value, starting with the initial value.'),
        ('q2', 'Muốn biết state sau 3 event đầu tiên thì làm gì?', 'How do you get the state after the first 3 events?', 'Fold 3 event đầu từ state ban đầu.', 'Fold the first 3 events from the initial state.',
         'Với event sourcing, state ở thời điểm nào cũng dựng lại được.', 'With event sourcing, the state at any point can be rebuilt.'),
        ('q3', 'Trong cách dùng reducer, màn hình có được sửa state trực tiếp không?', 'With a reducer, may the screen modify the state directly?', 'Không, nó chỉ gửi event.', 'No, it only sends events.',
         'reduce là chỗ duy nhất đổi state.', 'reduce is the only place that changes the state.'),
        ('q4', 'Id của một lịch mới nên được tạo ở đâu?', 'Where should a new booking\'s id be created?', 'Ở ngoài reduce, khi nhận lệnh, rồi ghi vào event.', 'Outside reduce, when the request comes in, then written into the event.',
         'Sinh id trong reduce làm mỗi lần phát lại ra kết quả khác.', 'Creating the id in reduce makes each replay give a different result.')]:
        a(C + '.quiz.%s.q' % q, qv, qe); a(C + '.quiz.%s.a' % q, av, ae); a(C + '.quiz.%s.why' % q, wv, we)
