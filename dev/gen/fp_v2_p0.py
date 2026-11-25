# Lập trình hàm với Kotlin · P0: bản đồ track (viết cuối, đặt đầu track; cùng khuôn với cleancode_v2_j0.py)
# Tổng hợp từ P1–P10; mọi triệu chứng là đúng tình huống mô phỏng của chương được trỏ tới, cùng con số (nguồn ở chương đó).

SEC_ORDER = {'p0': ['hook', 'order', 'index', 'links', 'recall']}

TITLES = [
    ('p1', 'Hàm thuần và referential transparency', 'Pure functions and referential transparency'),
    ('p2', 'Bất biến, dữ liệu dùng chung và đệ quy', 'Immutability, data sharing and recursion'),
    ('p3', 'Ghép hàm: composition, currying, partial application', 'Composing functions: composition, currying, partial application'),
    ('p4', 'Kiểu dữ liệu đại số', 'Algebraic data types'),
    ('p5', 'Lỗi là giá trị', 'Errors as values'),
    ('p6', 'map và flatMap: functor và monad qua ví dụ', 'map and flatMap: functors and monads by example'),
    ('p7', 'Validate gom lỗi: applicative và monoid', 'Validation that collects errors: applicatives and monoids'),
    ('p8', 'State thuần: reducer và event', 'Pure state: reducers and events'),
    ('p9', 'Functional core, imperative shell: lõi thuần, vỏ mỏng', 'Functional core, imperative shell: a pure core, a thin shell'),
    ('p10', 'FP trên Android: state bất biến và cập nhật lồng sâu', 'FP on Android: immutable state and deep updates'),
]

# [id, tiêu đề vi, en, chi tiết vi, en, nguyên nhân vi, en, giải thích nguyên nhân vi, en, cách chữa vi, en, chương, lúc lộ ra]
SY = [
    ('ciRed', 'Test phí xanh cả tuần, đêm thứ Bảy máy CI báo đỏ', 'The fee test is green all week, then red on CI on Saturday night',
     'Không ai sửa gì. Cùng bản mã, cùng bài test fee() == 200.000; chỉ có ngày chạy khác.', 'Nobody changed anything. The same code, the same fee() == 200,000 test; only the day it runs is different.',
     'Hàm tự xem đồng hồ: kết quả phụ thuộc lúc chạy', 'The function reads the clock itself: the result depends on when it runs',
     'fee() không nhận ngày qua tham số mà tự hỏi hôm nay là thứ mấy. Thứ Bảy nó trả 300.000, nên lời gọi không thay được bằng một giá trị cố định.', 'fee() does not take the date as a parameter; it asks what day it is. On Saturday it returns 300,000, so the call cannot be replaced by a fixed value.',
     'Đưa ngày vào qua tham số: fee(date) là hàm thuần, test truyền đúng ngày mình muốn kiểm.', 'Pass the date in as a parameter: fee(date) is pure, and the test passes exactly the day it wants to check.', 'p1', 'test'),
    ('unselectGone', 'Bỏ chọn một lịch ở màn "Chọn lịch để hủy", lịch đó biến luôn khỏi "Lịch đã đặt"', 'Unselecting a booking on "Pick bookings to cancel" also removes it from "Booked"',
     'Thêm một lịch vào danh sách đã chọn thì danh sách đã đặt cũng có thêm lịch đó.', 'Adding a booking to the selected list also adds it to the booked list.',
     'Hai cái tên, một MutableList', 'Two names, one MutableList',
     'val selected = booked không tạo bản sao. val chỉ cấm gán tên đó sang danh sách khác; sửa qua tên này thì tên kia đổi theo.', 'val selected = booked does not make a copy. val only stops that name being pointed at another list; a change through one name shows through the other.',
     'Dùng danh sách bất biến: mỗi thay đổi tạo bản mới, dùng chung phần không đổi, bản cũ còn nguyên.', 'Use an immutable list: each change builds a new version that shares the unchanged part, and the old version stays intact.', 'p2', 'run'),
    ('stackOverflow', 'Báo cáo phí chạy tốt cả tháng, với dữ liệu cả năm thì crash StackOverflowError', 'The fee report runs fine for a month, then crashes with StackOverflowError on a full year of data',
     'Một tháng chỉ vài trăm lịch; cả năm là 50.000 lịch, và app crash khi tới phần tử thứ 10.000 (giới hạn ví dụ của mô phỏng).', 'A month has only a few hundred bookings; a year has 50,000, and the app crashes at the 10,000th element (the simulation\'s example limit).',
     'Đệ quy để lại một việc chờ cho mỗi lời gọi', 'Recursion leaves one pending step per call',
     'Mỗi lời gọi còn phải cộng sau khi lời gọi con trả về, nên stack cao thêm một tầng cho mỗi phần tử.', 'Each call still has an addition to do after the inner call returns, so the stack grows by one frame per element.',
     'Mang tổng theo qua tham số để lời gọi là việc cuối cùng, rồi gắn tailrec: Kotlin đổi nó thành vòng lặp.', 'Carry the total in a parameter so the call is the last thing done, then add tailrec: Kotlin turns it into a loop.', 'p2', 'run'),
    ('reminder2am', 'Tin nhắc lịch hiện 02:00, ba màn khác hiện 09:00', 'The reminder shows 02:00 while three other screens show 09:00',
     'Cùng một lịch hẹn, lệch 7 tiếng. Lúc review không ai thấy, vì dòng sai trông giống hệt ba dòng đúng.', 'The same appointment, 7 hours apart. Nobody saw it in review, because the wrong line looks exactly like the three right ones.',
     'Sáu tham số chép tay ở bốn chỗ gọi', 'Six arguments copied by hand at four call sites',
     'Ba tham số đầu (ngôn ngữ, tiền tệ, múi giờ) giống nhau ở mọi màn mà vẫn phải truyền lại; chỗ gọi ở màn tin nhắc chép múi giờ UTC từ một bài test.', 'The first three arguments (language, currency, time zone) are the same on every screen yet passed again each time; the reminder\'s call site copied UTC from a test.',
     'Chốt các tham số chung một lần bằng partial application, rồi nối các bước bằng compose.', 'Fix the shared arguments once with partial application, then chain the steps with compose.', 'p3', 'run'),
    ('add24h', 'Thêm tùy chọn "đồng hồ 24 giờ" phải sửa 4 chỗ gọi', 'Adding a "24-hour clock" option means editing 4 call sites',
     'Tham số mới phải thêm vào chữ ký hàm và vào cả bốn chỗ gọi; mỗi chỗ lại là một cơ hội truyền nhầm.', 'The new parameter goes into the function signature and into all four call sites; each one is another chance to pass the wrong value.',
     'Cấu hình chung không có chỗ ở riêng', 'Shared configuration has no home of its own',
     'Cùng nguyên nhân với tin nhắc lệch giờ: bộ giá trị chung bị chép ra mọi nơi gọi.', 'The same cause as the reminder\'s wrong time: the shared values are copied to every call site.',
     'Khi tham số chung đã được chốt ở một chỗ, thêm tùy chọn mới chỉ sửa đúng chỗ đó.', 'Once the shared arguments are fixed in one place, a new option changes only that place.', 'p3', 'change'),
    ('spinForever', 'Mất mạng lúc đang tải, màn chỉ quay mãi, không hiện lỗi', 'The network drops while loading, and the screen spins forever without showing the error',
     'Khối catch đã gán error, nhưng người dùng không bao giờ thấy nó.', 'The catch block did set error, but the user never sees it.',
     'Kiểu cho phép trạng thái vô nghĩa', 'The type allows meaningless states',
     'UiState ba trường độc lập cho 8 trạng thái, màn chỉ cần 3. Khối catch quên đặt isLoading = false, tạo ra "đang tải mà có lỗi"; màn xét isLoading trước nên chỉ quay.', 'A three-field UiState allows 8 states where the screen needs 3. The catch block forgets isLoading = false and produces "loading with an error"; the screen checks isLoading first, so it only spins.',
     'Dùng sealed interface với đúng 3 trạng thái: khối catch chỉ có thể tạo Error, không thể "vừa tải vừa lỗi".', 'Use a sealed interface with exactly 3 states: the catch block can only produce Error, never "loading and failed".', 'p4', 'run'),
    ('silentRefresh', 'Thêm trạng thái "tải lại, giữ dữ liệu cũ", trình biên dịch không chỉ ra chỗ nào cần sửa', 'Adding a "refresh but keep the old data" state, and the compiler points to nothing to fix',
     'Cả 3 màn vẫn xét isLoading trước và giấu danh sách sau vòng quay. Lỗi chỉ lộ khi có người nhìn màn hình.', 'All 3 screens still check isLoading first and hide the list behind the spinner. It shows only when someone looks at the screen.',
     'Trạng thái mới là một tổ hợp đã có sẵn', 'The new state is a combination that already existed',
     '"Đang tải và có danh sách" vốn là một trong 8 tổ hợp, nên không dòng nào hết biên dịch được.', '"Loading with a list" was already one of the 8 combinations, so no line stops compiling.',
     'Với sealed interface, thêm kiểu con Refreshing thì mọi when không có else báo lỗi: trình biên dịch chỉ ra 3 chỗ.', 'With a sealed interface, adding a Refreshing subtype breaks every when without else: the compiler points to the 3 places.', 'p4', 'change'),
    ('slotTaken', 'Giờ đã có người đặt, màn chỉ báo "Đặt lịch thất bại"', 'The slot is already taken, and the screen just says "Booking failed"',
     'Người dùng không biết chỉ cần chọn giờ khác. Một bug NullPointerException ở bước kiểm lượt cũng hiện đúng câu đó, không crash, không báo cáo lỗi.', 'The user does not learn that picking another time would do. A NullPointerException bug in the quota check shows the very same message, with no crash and no error report.',
     'Lỗi đi bằng ngoại lệ, màn bắt mọi Exception', 'Errors travel as exceptions, and the screen catches every Exception',
     'Chữ ký book() trả Booking không nói nó hỏng ra sao; catch (e: Exception) ở màn hình gộp lỗi nghiệp vụ với bug làm một.', 'book()\'s signature returns Booking and says nothing about how it fails; catch (e: Exception) on the screen lumps business errors and bugs together.',
     'Trả lỗi nghiệp vụ như một giá trị có kiểu (sealed interface BookingError); bug vẫn là ngoại lệ để lộ ra và được sửa.', 'Return business errors as a typed value (a sealed interface BookingError); bugs stay exceptions so they surface and get fixed.', 'p5', 'run'),
    ('nestedBox', 'map trả về Outcome<BookingError, Outcome<BookingError, Unit>>', 'map returns Outcome<BookingError, Outcome<BookingError, Unit>>',
     'Muốn nối bước kiểm lượt sau bước kiểm số điện thoại, kiểu kết quả thành hộp trong hộp; doctors.map { slotsToday(it) } cũng ra List<List<Slot>>.', 'Chaining the quota check after the phone check gives a box inside a box; doctors.map { slotsToday(it) } likewise gives List<List<Slot>>.',
     'Dùng map với hàm đã trả một hộp', 'Using map with a function that already returns a box',
     'map đặt kết quả của hàm vào lại cái hộp cũ; khi kết quả cũng là một hộp thì có hai tầng.', 'map puts the function\'s result back into the original box; when that result is itself a box, there are two layers.',
     'Dùng flatMap (map rồi flatten) để gộp còn một tầng; bước hỏng dừng cả chuỗi mà không cần return.', 'Use flatMap (map, then flatten) to merge it back to one layer; a failing step stops the chain with no return needed.', 'p6', 'change'),
    ('fiveSubmits', 'Form đăng ký sai cả 4 ô, phải nộp 5 lần mới qua', 'A sign-up form with all 4 fields wrong takes 5 submissions to pass',
     'Mỗi lần nộp chỉ báo một lỗi; sửa xong lỗi này mới thấy lỗi kế tiếp.', 'Each submission reports only one error; the next one appears only after this one is fixed.',
     'Các ô độc lập bị nối bằng flatMap', 'Independent fields chained with flatMap',
     'flatMap dừng ở lỗi đầu tiên, đúng khi bước sau cần kết quả bước trước; bốn ô của form thì không cần nhau.', 'flatMap stops at the first error, which is right when a step needs the previous result; the four form fields do not need each other.',
     'Kiểm mọi ô rồi gộp lỗi (applicative, gộp bằng phép nối list); lần nộp 2 là qua.', 'Check every field, then combine the errors (an applicative, combined by list concatenation); the second submission passes.', 'p7', 'run'),
    ('quotaTwo', 'Gói 5 lượt, đặt 2 lịch rồi hủy 1, app hiện còn 2 lượt thay vì 4', 'A 5-visit package, 2 bookings then 1 cancellation, and the app shows 2 visits left instead of 4',
     'Mở lại app chỉ còn con số sai, không có gì để kiểm lại vì sao.', 'After reopening the app only the wrong number is left, with nothing to check why.',
     'Một biến, nhiều chỗ sửa', 'One variable, many writers',
     'Màn đặt lịch và bước đồng bộ cùng gọi remaining--, nên mỗi lần đặt bị trừ hai lần.', 'The booking screen and the sync step both call remaining--, so each booking is subtracted twice.',
     'Ghi mỗi việc xảy ra thành một event; một hàm thuần reduce(state, event) là chỗ duy nhất đổi state.', 'Record each thing that happens as an event; a pure function reduce(state, event) is the only place that changes state.', 'p8', 'run'),
    ('fiveFakes', 'Test luật "thứ Bảy tính 300.000 đ" phải giả 5 thứ', 'Testing the "Saturday costs 300,000 VND" rule needs 5 fakes',
     'Đồng hồ, database, máy chủ, thống kê, log: luật chỉ là một phép so sánh ngày.', 'The clock, the database, the server, analytics, the log: the rule is just one date comparison.',
     'Luật trộn với mọi việc đụng ra ngoài', 'The rule is mixed with everything that touches the outside',
     'book() vừa đọc, vừa quyết định, vừa ghi; vệt chạy qua lại ranh giới 4 lần.', 'book() reads, decides and writes all at once; its path crosses the boundary 4 times.',
     'Tách lõi thuần decide() nhận giá trị và trả Decision; vỏ mỏng đọc hết, gọi lõi một lần, rồi mới ghi. Lõi test bằng giá trị, không cần đồ giả.', 'Split out a pure core, decide(), that takes values and returns a Decision; a thin shell reads everything, calls the core once, then writes. The core is tested with values, no fakes.', 'p9', 'test'),
    ('lostPhone', 'Đổi thành phố trong hồ sơ, số điện thoại và mã thẻ bảo hiểm biến mất', 'Changing the city in the profile wipes the phone number and the insurance card',
     'Mã vẫn biên dịch; hồ sơ lặng lẽ mất hai trường.', 'The code still compiles; the profile silently loses two fields.',
     'Dựng lại object bên trong từ đầu', 'Rebuilding an inner object from scratch',
     'Patient(name = p.name, address = …) chỉ điền những trường người viết nhớ tới; phone và card nhận giá trị mặc định.', 'Patient(name = p.name, address = …) fills only the fields the writer remembered; phone and card take their defaults.',
     'Copy lồng từ bản cũ ở từng tầng (hoặc một hàm cập nhật có tên, hoặc optics của Arrow).', 'Copy from the old value at each level (or use a named update function, or Arrow optics).', 'p10', 'run'),
    ('frozenList', 'Thêm lịch hẹn mà màn hình vẫn hiện danh sách cũ', 'A booking is added, yet the screen still shows the old list',
     'Nút "hoàn tác" cũng không đưa được về trạng thái trước.', 'The undo button cannot go back to the previous state either.',
     'Sửa MutableList tại chỗ rồi gán lại cùng object', 'Changing a MutableList in place, then assigning the same object',
     'StateFlow chỉ phát khi giá trị đổi; state vẫn là object cũ nên nó không phát. Bản giữ để hoàn tác là cùng object, nên cũng bị đổi.', 'StateFlow emits only when the value changes; state is still the old object, so nothing is emitted. The copy kept for undo is the same object, so it changes too.',
     'Dùng List chỉ đọc và thay cả state bằng copy: object mới thì StateFlow phát, bản cũ còn nguyên.', 'Use a read-only List and replace the whole state with copy: a new object makes StateFlow emit, and the old version stays intact.', 'p10', 'run'),
]


def add(a):
    def B(ch, sec, n, field, vi, en=None):
        a('%s.sec.%s.b.%02d.%s' % (ch, sec, n, field), vi, vi if en is None else en)

    m = lambda k, vi, en=None: a('m.map.' + k, vi, en)
    m('title', 'Gặp triệu chứng này thì đọc chương nào', 'Seen this symptom? Read this chapter')
    m('overview', 'Chọn một vấn đề hay gặp trên app Hẹn Khám. Bốn bước: triệu chứng, lúc nó lộ ra (khi chạy test, khi người dùng dùng app, hay khi viết và sửa mã), nguyên nhân, và chương giải thích.',
      'Pick a common problem on the ClinicBook app. Four steps: the symptom, when it shows up (when tests run, when people use the app, or when writing and changing code), the cause, and the chapter that explains it.')
    m('wrapup', 'Mọi triệu chứng trong bảng đều biên dịch được, và phần lớn chỉ lộ ra khi người dùng đang dùng app. Nhiều cách chữa của track đẩy việc phát hiện lên sớm hơn: kiểu sealed để trình biên dịch chỉ ra chỗ thiếu, lỗi nằm trong kiểu trả về để nơi gọi không quên được, hàm thuần để test bằng giá trị thay cho đồ giả.',
      'Every symptom in the table compiles, and most of them show up only while people are using the app. Many of the track\'s fixes move detection earlier: sealed types so the compiler points to what is missing, errors in the return type so callers cannot forget them, pure functions so tests use values instead of fakes.')
    m('simp.1', 'Mỗi triệu chứng chỉ trỏ tới một chương chính; vấn đề thật thường có nhiều nguyên nhân cùng lúc.', 'Each symptom points to one main chapter; real problems often have several causes at once.')
    m('ctl.hint', 'Chọn triệu chứng rồi đi bốn bước; tab "Bảng tra" liệt kê tất cả.', 'Pick a symptom and walk the four steps; the "Lookup table" tab lists them all.')
    m('ctl.symptom', 'Triệu chứng', 'Symptom')
    m('diagramTitle', 'Triệu chứng, lúc lộ ra, nguyên nhân, chương', 'Symptom, when it shows, cause, chapter')
    m('diagramDesc', 'Từ điều bạn thấy tới chương cần đọc', 'From what you see to the chapter to read')
    for k, vi, en in [('symptom', 'Triệu chứng', 'Symptom'), ('phase', 'Lộ ra lúc', 'Shows up'), ('cause', 'Nguyên nhân', 'Cause'), ('chapter', 'Chương', 'Chapter')]:
        m('n.' + k, vi, en)
    m('met.phase', 'Lộ ra lúc', 'Shows up'); m('met.chapter', 'Chương', 'Chapter')
    m('phase.none', 'chưa xét', 'not yet'); m('ch.none', 'chưa xét', 'not yet')
    for k, vi, en, xv, xe in [
        ('test', 'khi chạy test', 'when tests run', 'Lộ ra trong bài test: test đỏ mà không ai sửa gì, hay muốn kiểm một luật nhỏ mà phải dựng cả đống đồ giả. Đây là dấu hiệu hàm phụ thuộc vào thứ không nằm trong tham số.', 'Shows up in the tests: a test turns red although nobody changed anything, or checking one small rule needs a pile of fakes. It is a sign that a function depends on something that is not in its parameters.'),
        ('run', 'khi người dùng dùng app', 'when people use the app', 'Mã biên dịch, test có thể xanh, nhưng người dùng thấy sai: con số lệch, dữ liệu mất, màn hình đứng yên. Đây là chỗ đắt nhất để phát hiện lỗi.', 'The code compiles and the tests may be green, but users see something wrong: a number off, data lost, a screen that does not move. This is the most expensive place to find a bug.'),
        ('change', 'khi viết hay sửa mã', 'when writing or changing code', 'Lộ ra khi bạn thêm một tính năng: kiểu kết quả rối, phải sửa nhiều chỗ, hay trình biên dịch im lặng ở chỗ lẽ ra phải báo.', 'Shows up when you add a feature: a tangled result type, many places to edit, or a compiler that stays quiet where it should complain.')]:
        m('phase.' + k, vi, en); m('phase.%s.explain' % k, xv, xe)
    for sid, tv, te, dv, de, cv, ce, cdv, cde, fv, fe, ch, ph in SY:
        m('s.%s.title' % sid, tv, te); m('s.%s.detail' % sid, dv, de); m('s.%s.cause' % sid, cv, ce); m('s.%s.causeDetail' % sid, cdv, cde); m('s.%s.fix' % sid, fv, fe)
        m('ctl.symptom.' + sid, tv, te)
    for h, vi, en in TITLES:
        n = h[1:]
        m('ch.' + h, 'P%s · %s' % (n, vi), 'P%s · %s' % (n, en)); m('go.' + h, 'Đọc P%s · %s' % (n, vi), 'Read P%s · %s' % (n, en))
    m('co.try', 'Chọn một triệu chứng bạn từng gặp; đi bốn bước rồi mở chương được chỉ tới.', 'Pick a symptom you have met; walk the four steps, then open the chapter pointed to.')
    m('co.cause', 'Nguyên nhân thường là một cách viết, không phải một dòng sai lẻ: hàm đọc thứ không nằm trong tham số, dữ liệu sửa được dùng chung, kiểu cho phép điều vô nghĩa.', 'The cause is usually a way of writing, not a single wrong line: a function reading something outside its parameters, mutable data being shared, a type that allows nonsense.')
    m('co.chapter', 'Chương được chỉ tới có mô phỏng đúng tình huống này, cách chữa và nguồn.', 'The chapter pointed to simulates exactly this case, with the fix and sources.')
    a('cap.map', 'Từ trái sang phải: triệu chứng, lúc nó lộ ra, nguyên nhân, chương giải thích. Tab "Bảng tra" liệt kê mọi triệu chứng.', 'Left to right: the symptom, when it shows up, the cause, the chapter that explains it. The "Lookup table" tab lists every symptom.')
    a('preset.map', 'Lập trình hàm · bản đồ triệu chứng và chương', 'Functional programming · symptom map to chapters')

    z = lambda k, vi, en=None: a('vz.' + k, vi, en)
    z('tab.map', 'Bảng tra', 'Lookup table')
    z('map.cap', 'Mọi triệu chứng của track, lúc chúng lộ ra và chương giải thích. Hàng đang chọn được viền; ô "?" mở dần theo bước.', 'Every symptom in the track, when it shows up and the chapter that explains it. The chosen row is outlined; "?" cells open step by step.')
    z('map.legend', 'Chín trong mười bốn triệu chứng lộ ra khi người dùng đang dùng app, hai khi chạy test, ba khi viết hay sửa mã. Cả mười bốn đều biên dịch được.', 'Nine of the fourteen symptoms show up while people are using the app, two when tests run, three when writing or changing code. All fourteen compile.')
    for k, vi, en in [('sym', 'Triệu chứng', 'Symptom'), ('phase', 'Lộ ra lúc', 'Shows up'), ('ch', 'Chương', 'Chapter')]:
        z('map.col.' + k, vi, en)

    C = 'p0'
    a(C + '.title', 'Bản đồ track: triệu chứng và chương', 'Track map: symptoms and chapters')
    a(C + '.essence', 'Track này dạy dùng lập trình hàm để viết mã Android ít bất ngờ hơn: hàm cho cùng kết quả với cùng đầu vào, dữ liệu không bị sửa sau lưng, kiểu dữ liệu không cho phép trạng thái vô nghĩa, lỗi nằm ngay trong kiểu trả về. Ví dụ đều bằng Kotlin trên app Hẹn Khám.\nPhần 1 (P1–P4) là nền móng: hàm thuần, bất biến và đệ quy, ghép hàm, kiểu dữ liệu đại số. Phần 2 (P5–P7) là xử lý lỗi bằng giá trị: kiểu lỗi riêng, map và flatMap để nối các bước, gom lỗi khi các bước độc lập. Phần 3 (P8–P10) đưa các ý đó vào app: state thuần bằng reducer, lõi thuần với vỏ mỏng, cập nhật state lồng sâu.\nĐang gặp một vấn đề cụ thể? Hãy bắt đầu từ bảng tra bên dưới: tìm triệu chứng giống của bạn, rồi đọc chương được chỉ tới.',
      'This track teaches using functional programming to write Android code with fewer surprises: functions that give the same result for the same input, data that is not changed behind your back, types that cannot hold meaningless states, errors that sit right in the return type. All examples are Kotlin on the ClinicBook app.\nPart 1 (P1–P4) is the foundation: pure functions, immutability and recursion, composing functions, algebraic data types. Part 2 (P5–P7) is handling errors as values: your own error types, map and flatMap to chain steps, collecting errors when steps are independent. Part 3 (P8–P10) brings these ideas into the app: pure state with reducers, a pure core with a thin shell, updating deeply nested state.\nFacing a specific problem? Start from the lookup table below: find the symptom that looks like yours, then read the chapter it points to.')
    a(C + '.goal.g1', 'Đã thấy lúc triệu chứng lộ ra', 'Saw when the symptom shows up')
    a(C + '.goal.g2', 'Đã tới chương cần đọc', 'Reached the chapter to read')
    a(C + '.sim.fp.map', 'triệu chứng và chương', 'symptoms and chapters')

    S_ = 'hook'
    a(C + '.sec.%s.title' % S_, 'Đoán trước khi đọc', 'Predict before reading')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'predict', 'Cả 14 triệu chứng trong bảng tra đều biên dịch được. Bạn đoán bao nhiêu cái chỉ lộ ra khi người dùng đang dùng app?',
      'All 14 symptoms in the lookup table compile. How many do you guess show up only while people are using the app?')
    B(C, S_, 1, 'ans', 'Chín. Hai lộ ra khi chạy test, ba khi viết hay sửa mã. Nhiều cách chữa trong track đẩy việc phát hiện lên sớm hơn, tới bài test hay tới trình biên dịch. Đây là đếm trên bảng của site, không phải thống kê.',
      'Nine. Two show up when tests run, three when writing or changing code. Many fixes in the track move detection earlier, to the tests or to the compiler. This counts the site\'s table, not a statistic.')

    S_ = 'order'
    a(C + '.sec.%s.title' % S_, 'Thứ tự đọc', 'Reading order')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'p', 'Đọc P1 "Hàm thuần và referential transparency" trước: gần như mọi chương sau dựa vào ý thay một lời gọi bằng kết quả của nó. P2 và P3 đọc theo thứ tự nào cũng được. P4 "Kiểu dữ liệu đại số" cần cho P5 "Lỗi là giá trị", vì kiểu lỗi riêng là một sealed interface. P5, P6 "map và flatMap" và P7 "Validate gom lỗi" nên đọc liền nhau: P6 nối các bước của P5, P7 nói khi nào không nên nối. P8 "State thuần: reducer và event" và P9 "Functional core, imperative shell" dùng hàm thuần của P1; P10 "FP trên Android" dùng bất biến của P2.',
      'Read P1 "Pure functions and referential transparency" first: almost every later chapter relies on replacing a call with its result. P2 and P3 can be read in either order. P4 "Algebraic data types" is needed for P5 "Errors as values", because your own error type is a sealed interface. Read P5, P6 "map and flatMap" and P7 "Validation that collects errors" together: P6 chains P5\'s steps, and P7 says when not to chain them. P8 "Pure state: reducers and events" and P9 "Functional core, imperative shell" use P1\'s pure functions; P10 "FP on Android" uses P2\'s immutability.')
    B(C, S_, 2, 'p', 'Nên biết cú pháp Kotlin trước, nhất là các chương "Data class và bằng nhau", "Enum, sealed và when" và "Ngoại lệ, require/check và use" của track Kotlin: cơ chế ngôn ngữ.',
      'Knowing Kotlin syntax first helps, especially the chapters "Data classes and equality", "Enums, sealed types and when" and "Exceptions, require/check and use" of the Kotlin: How the Language Works track.')

    S_ = 'index'
    a(C + '.sec.%s.title' % S_, 'Chỉ mục: mỗi chương dùng hình gì', 'Index: the visual of each chapter')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'p', 'P1: bảng thay từng bước, mỗi hàng là chương trình sau một lần thay. P2: các ô của danh sách (ô mới, ô dùng chung) và độ sâu stack. P3: luồng hàm theo thứ tự chạy và bốn chỗ gọi. P4: bảng đếm trạng thái và ma trận mọi tổ hợp. P5: đường ray thành công và đường ray lỗi. P6: hộp và giá trị, với hộp trong hộp. P7: các ô của form và lỗi theo từng lần nộp. P8: nhật ký event với số lượt đúng và số app đang giữ. P9: hai cột vỏ và lõi, với vệt qua ranh giới. P10: cây object của state, ô mới và ô dùng chung.',
      'P1: a step-by-step substitution table, each row the program after one replacement. P2: list cells (new and shared) and the stack depth. P3: the function pipeline in running order and the four call sites. P4: a state-counting table and a matrix of every combination. P5: a success rail and an error rail. P6: boxes and values, including a box inside a box. P7: the form fields and their errors for each submission. P8: an event log with the correct visit count and the one the app holds. P9: two columns, shell and core, with the path across the boundary. P10: the state\'s object tree, new and shared nodes.')

    S_ = 'links'
    a(C + '.sec.%s.title' % S_, 'Cầu nối sang track khác', 'Bridges to other tracks')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'p', 'P4 "Kiểu dữ liệu đại số" nối với chương "Enum, sealed và when" của track Kotlin: cơ chế ngôn ngữ và chương "MVVM và MVI" của track Kiến trúc app Android. P5 "Lỗi là giá trị" nối với chương "Ngoại lệ, require/check và use" của track Kotlin và chương "Lỗi qua các tầng" của track Kiến trúc. P8 "State thuần: reducer và event" nối với chương "MVVM và MVI". P9 "Functional core, imperative shell" nối với chương "Đóng gói, bất biến, parse một lần" của track Mã sạch và kỷ luật làm nghề và chương "Kiểm thử theo tầng" của track Kiến trúc.',
      'P4 "Algebraic data types" links to "Enums, sealed types and when" in the Kotlin: How the Language Works track and "MVVM and MVI" in the Android App Architecture track. P5 "Errors as values" links to "Exceptions, require/check and use" in the Kotlin track and "Errors across layers" in the Architecture track. P8 "Pure state: reducers and events" links to "MVVM and MVI". P9 "Functional core, imperative shell" links to "Encapsulation, immutability, parse once" in the Clean Code and Craft track and "Testing by layer" in the Architecture track.')

    S_ = 'recall'
    a(C + '.sec.%s.title' % S_, 'Tự trả lời', 'Answer it yourself')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'ask', 'Ba lúc một vấn đề của track này lộ ra là gì? Cho mỗi lúc một ví dụ từ bảng tra.', 'What are the three moments when a problem in this track shows up? Give one example from the lookup table for each.')
    B(C, S_, 1, 'ans', 'Khi chạy test (test phí đỏ đêm thứ Bảy); khi người dùng dùng app (đổi thành phố làm mất số điện thoại); khi viết hay sửa mã (map trả về hộp trong hộp).', 'When tests run (the fee test red on Saturday night); when people use the app (changing the city wipes the phone number); when writing or changing code (map returning a box inside a box).')

    for q, qv, qe, av, ae, wv, we in [
        ('q1', 'Một bài test đỏ vào cuối tuần mà không ai sửa mã: đọc chương nào?', 'A test turns red at the weekend although nobody changed the code: which chapter?', 'P1 · Hàm thuần và referential transparency.', 'P1 · Pure functions and referential transparency.', 'Hàm tự đọc đồng hồ thay vì nhận ngày qua tham số.', 'The function reads the clock instead of taking the date as a parameter.'),
        ('q2', 'Form sai 4 ô mà mỗi lần nộp chỉ báo một lỗi: đọc chương nào?', 'A form with 4 wrong fields reports only one error per submission: which chapter?', 'P7 · Validate gom lỗi: applicative và monoid.', 'P7 · Validation that collects errors: applicatives and monoids.', 'Các ô độc lập bị nối bằng flatMap, vốn dừng ở lỗi đầu tiên.', 'Independent fields are chained with flatMap, which stops at the first error.'),
        ('q3', 'Thêm lịch mà màn hình không đổi: đọc chương nào?', 'A booking is added and the screen does not change: which chapter?', 'P10 · FP trên Android: state bất biến và cập nhật lồng sâu.', 'P10 · FP on Android: immutable state and deep updates.', 'MutableList bị sửa tại chỗ rồi gán lại cùng object, nên StateFlow không phát.', 'A MutableList is changed in place and the same object assigned again, so StateFlow does not emit.')]:
        a(C + '.quiz.%s.q' % q, qv, qe); a(C + '.quiz.%s.a' % q, av, ae); a(C + '.quiz.%s.why' % q, wv, we)
