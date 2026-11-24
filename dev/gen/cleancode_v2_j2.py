# Mã sạch · J2: đặt tên, mức trừu tượng, command và query (Phần 1: mã đọc được)
# Nguồn: Seemann, Code That Fits in Your Head 8.1.3–8.1.7 (viết cho người đọc, tên tốt hơn comment, X out names, CQS, thứ bậc giao tiếp), A.6;
# Martin, Clean Code ch.2 (tên lộ ý định, tránh thông tin sai, mỗi khái niệm một từ, tên theo miền), ch.3 (không side effect ẩn,
# tham số cờ, CQS), ch.4 (comment bù cho việc chưa diễn đạt được bằng mã); Moskała, Effective Kotlin Item 15, 17;
# Kotlin coding conventions (Choose good names). Đọc 2026-11-24, diễn đạt lại.

SEC_ORDER = {'j2': ['hook', 'names', 'xout', 'cqs', 'props', 'bugs', 'ex', 'honest']}


def add(a):
    def B(ch, sec, n, field, vi, en=None):
        a('%s.sec.%s.b.%02d.%s' % (ch, sec, n, field), vi, vi if en is None else en)

    a('preset.names', 'Mã sạch · che tên, đoán việc', 'Clean code · x out the names')
    m = lambda k, vi, en=None: a('m.names.' + k, vi, en)
    m('title', 'Che tên đi: chữ ký còn nói được gì', 'X out the names: what the signatures still say')
    m('overview', 'Lớp AppointmentRepo của app Hẹn Khám có hai phiên bản. Theo cách của Seemann, che tên hàm đi rồi đoán mỗi hàm đọc hay ghi chỉ từ kiểu; sau đó mở tên; cuối cùng đọc phần cài đặt xem đoán có đúng không. Bước cuối là lỗi thật: màn hình gọi cùng một hàm hai lần khi mất mạng.',
      'ClinicBook\'s AppointmentRepo class comes in two versions. Following Seemann, x out the function names and guess from the types alone whether each one reads or writes; then reveal the names; finally read the implementation to check the guesses. The last step is the real bug: the screen calls the same function twice while offline.')
    m('wrapup', 'Ở bản trộn, kiểu và tên nói một đằng, mã làm một nẻo: getAppointments trả dữ liệu mà vẫn xóa cache, save trả Boolean mà người đọc không biết nghĩa là gì, process nhận một cờ để làm hai việc, nextFree trông như trạng thái nhưng gọi mạng. Chỉ đoán đúng 1 trên 4. Bản tách command và query: hàm trả dữ liệu thì không đổi gì, hàm đổi trạng thái thì không trả gì, nên chữ ký đủ để đoán đúng cả 6, và gọi một query hai lần luôn an toàn.',
      'In the mixed version, types and names say one thing and the code does another: getAppointments returns data yet clears the cache, save returns a Boolean the reader cannot interpret, process takes a flag to do two things, nextFree looks like state but calls the network. Only 1 of 4 guesses is right. With commands and queries separated, a function that returns data changes nothing and one that changes state returns nothing, so the signature is enough to guess all 6 correctly, and calling a query twice is always safe.')
    m('simp.1', 'Lớp rút gọn còn vài hàm; Api và Cache là giao diện giả định. "Đoán" ở đây là đoán đọc hay ghi, theo cách lập luận của Seemann ở mục 8.1.5–8.1.6.', 'The class is cut down to a few functions; Api and Cache are assumed interfaces. "Guessing" here means guessing read or write, following Seemann\'s reasoning in 8.1.5–8.1.6.')
    m('simp.2', 'CQS là nguyên tắc của Bertrand Meyer mà Seemann và Martin đều dùng; trình biên dịch Kotlin không ép nó. Có những trường hợp khó tách (ví dụ thêm một hàng và cần id vừa tạo); chương không đi sâu vào đó.', 'CQS is Bertrand Meyer\'s principle, used by both Seemann and Martin; the Kotlin compiler does not enforce it. Some cases are hard to separate (say, inserting a row and needing the new id); the chapter does not go into them.')
    m('ctl.hint', 'Đổi phiên bản rồi đi lại; so cột "Đoán từ kiểu" với cột "Thật sự làm".', 'Switch versions and walk again; compare the "Guess from types" column with "What it really does".')
    m('ctl.case', 'Phiên bản', 'Version')
    for k, vi, en in [('mixed', 'trộn đọc và ghi', 'reads and writes mixed'), ('cqs', 'tách command và query', 'commands and queries separated')]:
        m('ctl.case.' + k, vi, en)
    m('diagramTitle', 'Chữ ký, tên, cài đặt, màn hình gọi', 'Signature, name, implementation, the calling screen')
    m('diagramDesc', 'Người đọc đoán từ chữ ký, rồi tên, rồi cài đặt; màn hình gọi hàm theo những gì nó tin', 'The reader guesses from the signature, then the name, then the implementation; the screen calls functions based on what it believes')
    for k, vi, en in [('sig', 'Chữ ký (tên bị che)', 'Signature (name hidden)'), ('name', 'Tên hàm', 'Function name'), ('impl', 'Cài đặt', 'Implementation'), ('screen', 'Màn hình gọi', 'Calling screen')]:
        m('n.' + k, vi, en)
    m('met.right', 'Đoán đúng đọc hay ghi', 'Read or write guessed right'); m('met.both', 'Hàm vừa đọc vừa ghi', 'Functions that read and write'); m('met.second', 'Lần gọi thứ hai trả về', 'Second call returns')
    a('cap.names', 'Người đọc đi từ chữ ký sang tên rồi tới cài đặt; màn hình gọi hàm dựa trên những gì người viết màn hình tin. Nút đỏ: chỗ chữ ký hay tên đã nói sai.', 'The reader goes from the signature to the name to the implementation; the screen calls functions based on what its author believes. Red node: where the signature or name told a lie.')
    S = [
        ('mixed', 's1', 'Che tên, đoán từ kiểu', 'Hide the names, guess from the types',
         'Hàm trả List thì đoán là chỉ đọc; hàm nhận Appointment trả Boolean thì đoán là hỏi một điều về lịch hẹn; hàm nhận String và Boolean không trả gì thì chỉ biết là có ghi; val Slot thì đoán là trạng thái có sẵn.', 'A function returning a List looks read-only; one taking an Appointment and returning a Boolean looks like a question about it; one taking a String and a Boolean and returning nothing must write something; a val Slot looks like ready state.'),
        ('mixed', 's2', 'Mở tên', 'Reveal the names',
         'getAppointments, save, process(data2, flag), nextFree. Tên "get" củng cố đoán là chỉ đọc. data2 và flag không nói gì; người đọc phải mở cài đặt.', 'getAppointments, save, process(data2, flag), nextFree. The "get" name reinforces the read-only guess. data2 and flag say nothing; the reader must open the implementation.'),
        ('mixed', 's3', 'Đọc cài đặt: ba trên bốn lần đoán sai', 'Read the implementation: three of four guesses wrong',
         'getAppointments đọc rồi xóa cache. save ghi và trả true nếu lịch đã có từ trước. process làm hai việc theo cờ. nextFree gọi mạng trong getter và có thể ném lỗi.', 'getAppointments reads, then clears the cache. save writes and returns true if the booking already existed. process does two things depending on the flag. nextFree calls the network in its getter and may throw.'),
        ('mixed', 's4', 'Lỗi thật: gọi hai lần khi mất mạng', 'The real bug: two calls while offline',
         'Màn hình gọi getAppointments() để vẽ danh sách, rồi gọi lần nữa để đếm số trên huy hiệu. Lần đầu trả 3 lịch và xóa cache; lần hai không có mạng, trả danh sách rỗng: huy hiệu báo 0.', 'The screen calls getAppointments() to draw the list, then again to count the badge. The first call returns 3 bookings and clears the cache; the second has no network and returns an empty list: the badge says 0.'),
        ('cqs', 's1', 'Che tên, đoán từ kiểu', 'Hide the names, guess from the types',
         'Hai hàm trả dữ liệu: đoán là query, chỉ đọc. Bốn hàm không trả gì: đoán là command, có ghi. Hàm suspend trả Slot? thì đoán là tìm kiếm, có thể không thấy.', 'Two functions return data: guess queries, read-only. Four return nothing: guess commands that write. The suspend function returning Slot? looks like a lookup that may find nothing.'),
        ('cqs', 's2', 'Mở tên', 'Reveal the names',
         'appointments, clearExpiredCache, add, cancel, reschedule, findNextFreeSlot. Mỗi tên là một động từ hay danh từ nói đúng một việc; tên không cần nhắc lại những gì kiểu đã nói.', 'appointments, clearExpiredCache, add, cancel, reschedule, findNextFreeSlot. Each name is a verb or noun stating one thing; names need not repeat what the types already say.'),
        ('cqs', 's3', 'Đọc cài đặt: đoán đúng cả sáu', 'Read the implementation: all six guessed right',
         'Query không đổi trạng thái; command không trả dữ liệu. Việc xóa cache hết hạn có tên riêng, ai muốn xóa thì gọi nó.', 'Queries change no state; commands return no data. Clearing the expired cache has its own name; whoever wants it calls it.'),
        ('cqs', 's4', 'Cùng màn hình, gọi hai lần khi mất mạng', 'The same screen, two calls while offline',
         'appointments() gọi hai lần trả cùng 3 lịch hẹn: query gọi bao nhiêu lần cũng được. Huy hiệu báo 3.', 'appointments() called twice returns the same 3 bookings: a query can be called any number of times. The badge says 3.'),
    ]
    for case, k, tv, te, xv, xe in S:
        sid = case + '.' + k
        m('s.%s.title' % sid, tv, te); m('s.%s.explain' % sid, xv, xe); m('ev.' + sid, tv, te)
    for k, vi, en in [
        ('try', 'Đoán trước khi mở cột tiếp theo: mỗi hàng là đọc hay ghi?', 'Guess before the next column opens: does each row read or write?'),
        ('mixed.s2', 'Martin (Clean Code): tên phải lộ ý định; nếu tên cần comment giải thích thì tên chưa lộ ý định. data2 và flag là kiểu phân biệt vô nghĩa mà ông cảnh báo. [[src:book-cleancode]]', 'Martin (Clean Code): a name should reveal intent; if it needs a comment, it does not. data2 and flag are the meaningless distinctions he warns about. [[src:book-cleancode]]'),
        ('mixed.s3', 'Martin: side effect là lời nói dối; hàm hứa làm một việc nhưng làm thêm việc ẩn. Ví dụ set trả Boolean của ông giống save ở đây: đọc lệnh if (save(a)) người ta không biết nó hỏi hay làm. [[src:book-cleancode]]', 'Martin: side effects are lies; the function promises one thing and does hidden others. His example of a set returning a Boolean matches save here: reading if (save(a)), nobody knows whether it asks or acts. [[src:book-cleancode]]'),
        ('mixed.s4', 'Một query có side effect làm thứ tự và số lần gọi trở nên quan trọng. Người viết màn hình tin cái tên "get" nên gọi hai lần; lỗi chỉ hiện khi mất mạng.', 'A query with a side effect makes the order and number of calls matter. The screen\'s author trusted the "get" name and called it twice; the bug shows only offline.'),
        ('cqs.s2', 'Seemann: đừng nói bằng comment điều nói được bằng tên hàm; đừng nói bằng tên điều nói được bằng kiểu. Slot? đã nói "có thể không có", tên không cần thêm OrNull. [[src:book-seemann]]', 'Seemann: do not say with a comment what a method name can say; do not say with a name what a type can say. Slot? already says "may be absent"; the name needs no OrNull. [[src:book-seemann]]'),
        ('cqs.s3', 'Seemann: hàm có side effect không trả dữ liệu (command); hàm trả dữ liệu không có side effect (query). Khi đó chữ ký đủ để biết loại, không cần đọc cài đặt. [[src:book-seemann]]', 'Seemann: methods with side effects return no data (commands); methods that return data have no side effects (queries). Then the signature tells you which, without reading the implementation. [[src:book-seemann]]'),
        ('cqs.s4', 'Query gọi hai lần cho cùng kết quả nếu dữ liệu không đổi ở giữa. Xóa cache hết hạn là một command có tên, gọi ở chỗ có chủ đích.', 'A query called twice gives the same result if nothing changed in between. Clearing the expired cache is a named command, called deliberately.')]:
        m('co.' + k, vi, en)

    z = lambda k, vi, en=None: a('vz.' + k, vi, en)
    z('tab.names', 'Bảng đối chiếu', 'Comparison table')
    z('nm.cap', 'Mỗi hàng là một thành viên của AppointmentRepo. Cột mở dần theo bước: chữ ký với tên bị che, đoán từ kiểu, tên thật, rồi việc nó thật sự làm.', 'Each row is one member of AppointmentRepo. Columns open step by step: the signature with the name hidden, the guess from types, the real name, then what it really does.')
    for k, vi, en in [('sig', 'Chữ ký (tên che)', 'Signature (name hidden)'), ('guess', 'Đoán từ kiểu', 'Guess from types'), ('name', 'Tên', 'Name'), ('does', 'Thật sự làm', 'What it really does'), ('kind', 'Đọc hay ghi', 'Read or write')]:
        z('nm.col.' + k, vi, en)
    for k, vi, en in [('query', 'chỉ đọc (query)', 'read only (query)'), ('command', 'có ghi (command)', 'writes (command)'), ('ask', 'hỏi một điều về lịch hẹn', 'asks something about the booking'),
                      ('state', 'trạng thái có sẵn, rẻ', 'ready state, cheap'), ('lookup', 'tìm, có thể không thấy', 'lookup, may find nothing'), ('unknown', 'có ghi, không rõ ghi gì', 'writes, unclear what')]:
        z('nm.g.' + k, vi, en)
    for k, vi, en in [
        ('getAll', 'đọc cache, rồi xóa sạch cache', 'reads the cache, then wipes it'),
        ('save', 'ghi; true nếu lịch đã có từ trước', 'writes; true if the booking already existed'),
        ('process', 'cờ true: hủy lịch; false: dời lịch', 'flag true: cancel; false: reschedule'),
        ('nextFree', 'gọi mạng trong getter, có thể ném lỗi', 'calls the network in the getter, may throw'),
        ('appointments', 'đọc cache', 'reads the cache'),
        ('clear', 'xóa lịch hết hạn khỏi cache', 'removes expired bookings from the cache'),
        ('add', 'ghi lịch hẹn vào cache', 'writes the booking to the cache'),
        ('cancel', 'hủy lịch trên server', 'cancels the booking on the server'),
        ('reschedule', 'dời lịch trên server', 'reschedules on the server'),
        ('find', 'hỏi server giờ trống gần nhất', 'asks the server for the next free slot')]:
        z('nm.d.' + k, vi, en)
    for k, vi, en in [('r', 'đọc', 'read'), ('w', 'ghi', 'write'), ('rw', 'đọc và ghi', 'read and write'), ('slow', 'đọc, chậm, ném lỗi', 'read, slow, throws')]:
        z('nm.k.' + k, vi, en)
    z('nm.tcap', 'Màn hình gọi hai lần liên tiếp khi mất mạng (bước 4): lần đầu vẽ danh sách, lần hai đếm cho huy hiệu.', 'The screen calls twice in a row while offline (step 4): first to draw the list, then to count the badge.')
    for k, vi, en in [('call', 'Lần gọi', 'Call'), ('ret', 'Trả về', 'Returns'), ('cache', 'Cache sau lần gọi', 'Cache afterwards')]:
        z('nm.tcol.' + k, vi, en)
    z('nm.call.1', '1 · danh sách', '1 · the list'); z('nm.call.2', '2 · huy hiệu', '2 · the badge')
    z('nm.ret', '{n} lịch hẹn', '{n} bookings'); z('nm.cacheN', '{n} lịch hẹn', '{n} bookings')
    z('nm.legend', 'Ô gạch đỏ: điều chữ ký hay tên khiến người đọc tin sai. Viền đậm: cột vừa mở ở bước này. "?": chưa mở.', 'Red hatched: what the signature or name led the reader to believe wrongly. Bold outline: the column opened in this step. "?": not open yet.')

    C = 'j2'
    a(C + '.title', 'Đặt tên, command và query', 'Names, commands and queries')
    a(C + '.essence', 'Người đọc đoán hàm làm gì từ kiểu, rồi từ tên, và chỉ đọc cài đặt khi buộc phải. Tên phải nói đúng ý định; một khái niệm một từ; không nói bằng tên điều kiểu đã nói.\nTách command và query: hàm đổi trạng thái thì không trả dữ liệu, hàm trả dữ liệu thì không đổi trạng thái. Khi đó chữ ký đủ để biết hàm đọc hay ghi, và gọi query bao nhiêu lần cũng an toàn.\nTrong Kotlin, property dành cho trạng thái rẻ, không ném lỗi; việc tốn kém hay có logic nghiệp vụ là hàm. Tham số cờ báo hiệu hàm làm hai việc; tham số khó hiểu thì gọi bằng tên.',
      'Readers guess what a function does from its types, then its name, and read the implementation only when forced to. Names must state the intent; one word per concept; do not say with a name what the type says.\nSeparate commands and queries: a function that changes state returns no data, and one that returns data changes no state. Then the signature tells you whether it reads or writes, and a query is safe to call any number of times.\nIn Kotlin, properties are for cheap state that does not throw; expensive work or business logic is a function. A flag parameter signals a function doing two things; call unclear parameters by name.')
    a(C + '.goal.g1', 'Đã so đoán với cài đặt', 'Compared the guesses with the implementation')
    a(C + '.goal.g2', 'Đã thấy lỗi gọi hai lần', 'Saw the double-call bug')
    a(C + '.sim.cleancode.names', 'che tên rồi đoán đọc hay ghi', 'x out the names and guess read or write')

    S_ = 'hook'
    a(C + '.sec.%s.title' % S_, 'Đoán trước khi đọc', 'Predict before reading')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'predict', 'Màn hình Lịch hẹn gọi repo.getAppointments() để vẽ danh sách, rồi gọi lần nữa để đếm số trên huy hiệu. Có mạng thì mọi thứ đúng. Mất mạng thì danh sách có 3 lịch nhưng huy hiệu báo 0. Hàm tên "get" có thể đã làm gì?',
      'The Appointments screen calls repo.getAppointments() to draw the list, then again to count the badge. Online, all is well. Offline, the list shows 3 bookings but the badge says 0. What might a function named "get" have done?')
    B(C, S_, 1, 'ans', 'Nó không chỉ đọc: nó đọc cache rồi xóa cache "để lần sau tải bản mới". Lần gọi thứ hai không còn cache, không có mạng, nên trả danh sách rỗng. Cái tên "get" và kiểu trả về List khiến người viết màn hình tin rằng gọi hai lần là vô hại. Mô phỏng ngay dưới cho bạn che tên đi và đoán từng hàm.',
      'It does not just read: it reads the cache, then clears it "so the next call loads fresh data". The second call has no cache and no network, so it returns an empty list. The "get" name and the List return type made the screen\'s author believe two calls were harmless. The simulation just below lets you hide the names and guess each function.')

    S_ = 'names'
    a(C + '.sec.%s.title' % S_, 'Tên nói đúng ý định', 'Names that state the intent')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'p', 'Martin (Clean Code) đưa ra một loạt chỉ dẫn; vài chỉ dẫn hay gặp nhất trong app Android: tên phải lộ ý định (cần comment giải thích thì tên chưa đạt); tránh thông tin sai (đừng gọi là list thứ không phải List); phân biệt có nghĩa (data và data2, info và details không nói khác nhau ở đâu); mỗi khái niệm một từ (đừng để fetch, retrieve, get cùng nghĩa ở ba lớp); dùng tên của miền bài toán (Appointment, Slot, Doctor) khi không có thuật ngữ kỹ thuật hợp hơn. [[src:book-cleancode]]',
      'Martin (Clean Code) gives a series of guidelines; the ones that come up most in Android apps: names should reveal intent (if one needs a comment, it does not); avoid disinformation (do not call something a list unless it is a List); make meaningful distinctions (data and data2, info and details, do not say how they differ); pick one word per concept (do not have fetch, retrieve and get meaning the same thing in three classes); use problem-domain names (Appointment, Slot, Doctor) when no technical term fits better. [[src:book-cleancode]]')
    B(C, S_, 2, 'p', 'Quy ước của Kotlin: tên lớp thường là danh từ (List, PersonReader), tên hàm thường là động từ (close, readPersons); tên hàm nên cho biết nó sửa object hay trả bản mới, như sort sắp xếp tại chỗ còn sorted trả bản sao; tránh những từ vô nghĩa như Manager, Wrapper. [[src:kt-conventions]]',
      'Kotlin\'s conventions: class names are usually nouns (List, PersonReader), function names usually verbs (close, readPersons); a function name should say whether it mutates the object or returns a new one, as sort sorts in place while sorted returns a copy; avoid meaningless words such as Manager and Wrapper. [[src:kt-conventions]]')
    B(C, S_, 3, 'kt', '// trước\nval data2 = repo.load(true)\nfun handle(tmp: String) { /* ... */ }\n\n// sau: tên theo miền, động từ cho hàm, không cờ\nval upcoming = repo.upcomingAppointments()\nfun cancel(appointmentId: AppointmentId) { /* ... */ }',
      '// before\nval data2 = repo.load(true)\nfun handle(tmp: String) { /* ... */ }\n\n// after: domain names, verbs for functions, no flag\nval upcoming = repo.upcomingAppointments()\nfun cancel(appointmentId: AppointmentId) { /* ... */ }')

    S_ = 'xout'
    a(C + '.sec.%s.title' % S_, 'Che tên đi và thứ bậc giao tiếp', 'X out names, and the hierarchy of communication')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'p', 'Tên cũng có thể cũ đi như comment: ai đó đổi cài đặt mà quên đổi tên. Seemann đề xuất một bài tập: thay mọi tên hàm bằng xxx rồi xem chữ ký còn nói được gì. Hàm nhận một ngày và trả danh sách lịch hẹn thì gần như chắc là truy vấn theo ngày; hàm nhận một id và trả lịch hẹn có thể null thì là tìm theo id. Hàm không trả gì thì chỉ biết là có side effect; khi đó tên là kênh duy nhất. Bài tập hiệu quả khi lớp có ít thành viên và mỗi thành viên có kiểu khác nhau; API toàn String và Int thì kiểu không giúp được gì. [[src:book-seemann]]',
      'Names can go stale like comments: someone changes the implementation and forgets the name. Seemann proposes an exercise: replace every method name with xxx and see what the signatures still say. A function taking a date and returning bookings is almost certainly a date query; one taking an id and returning a nullable booking is a lookup by id. A function that returns nothing only tells you it has a side effect; then the name is the only channel. The exercise works when a class has few members with distinct types; an API made of String and Int gets no help from types. [[src:book-seemann]]')
    B(C, S_, 2, 'p', 'Từ đó Seemann rút ra thứ bậc giao tiếp với người đọc, từ mạnh tới yếu: kiểu riêng biệt, tên hàm tốt, comment tốt, ví dụ dưới dạng test tự động, commit message, tài liệu. Kiểu đứng đầu vì sai kiểu thì không biên dịch được; mọi kênh khác đều có thể cũ đi. Martin nói theo hướng tương tự: comment là để bù cho lúc ta chưa diễn đạt được bằng mã, nên trước khi viết comment hãy thử đặt một tên hàm. Comment vẫn có chỗ: giải thích vì sao chọn cách làm này, cảnh báo hậu quả. [[src:book-seemann]] [[src:book-cleancode]]',
      'From this Seemann draws a hierarchy of communicating with readers, strongest first: distinct types, good method names, good comments, examples as automated tests, commit messages, documentation. Types come first because wrong types do not compile; every other channel can go stale. Martin points the same way: comments compensate for failing to express ourselves in code, so before writing one, try naming a function. Comments still have a place: explaining why this approach was chosen, warning of consequences. [[src:book-seemann]] [[src:book-cleancode]]')

    S_ = 'cqs'
    a(C + '.sec.%s.title' % S_, 'Command và query', 'Commands and queries')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'p', 'Command Query Separation (của Bertrand Meyer, Seemann và Martin đều dùng): hàm có side effect thì không trả dữ liệu, đó là command; hàm trả dữ liệu thì không có side effect, đó là query. Biến cục bộ được sửa bên trong hàm không tính là side effect, vì người gọi không quan sát được. Trình biên dịch Kotlin không ép quy tắc này; đó là kỷ luật của người viết. Seemann khuyên ưu tiên query, vì query dễ suy luận hơn. [[src:book-seemann]] [[src:book-cleancode]]',
      'Command Query Separation (Bertrand Meyer\'s, used by Seemann in and Martin in): a function with a side effect returns no data, a command; a function that returns data has no side effect, a query. Mutating a local variable inside the function is not a side effect, because callers cannot observe it. The Kotlin compiler does not enforce this; it is the author\'s discipline. Seemann advises favouring queries, as they are easier to reason about. [[src:book-seemann]] [[src:book-cleancode]]')
    B(C, S_, 2, 'p', 'Martin cho hai ví dụ cùng kiểu với bản trộn trong mô phỏng. Hàm set trả Boolean: đọc if (set(...)) thì không biết là hỏi "đã đặt chưa" hay "đặt có thành công không"; cách sửa là tách thành một query kiểm tra và một command đặt. Tham số cờ: truyền một Boolean vào hàm là tuyên bố hàm làm hai việc, cách sửa là tách thành hai hàm có tên. Đừng nhầm CQS với CQRS: CQRS là một kiểu kiến trúc mượn tên của CQS. [[src:book-cleancode]] [[src:book-seemann]]',
      'Martin gives two examples of the same kind as the mixed version in the simulation. A set function returning a Boolean: reading if (set(...)), you cannot tell whether it asks "was it set" or "did setting succeed"; the fix is a query that checks and a command that sets. Flag arguments: passing a Boolean declares that the function does two things; the fix is two named functions. Do not confuse CQS with CQRS: CQRS is an architectural style that borrows CQS\'s name. [[src:book-cleancode]] [[src:book-seemann]]')
    B(C, S_, 3, 'kt', '// trước: vừa ghi vừa trả lời\nif (repo.save(a)) showToast(R.string.replaced)\n\n// sau: một query, một command\nval existed = repo.exists(a.id)\nrepo.add(a)\nif (existed) showToast(R.string.replaced)',
      '// before: writes and answers at once\nif (repo.save(a)) showToast(R.string.replaced)\n\n// after: one query, one command\nval existed = repo.exists(a.id)\nrepo.add(a)\nif (existed) showToast(R.string.replaced)')

    S_ = 'props'
    a(C + '.sec.%s.title' % S_, 'Property hay hàm, và gọi tham số bằng tên', 'Property or function, and named arguments')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'p', 'Moskała (Effective Kotlin): property trong Kotlin là accessor, không phải field, nên dùng được cho trạng thái suy ra; nhưng property nên biểu diễn trạng thái, không phải hành vi. Dùng hàm thay property khi việc đó tốn kém (phức tạp hơn O(1)), có thể ném lỗi, chứa logic nghiệp vụ, không tất định, là phép chuyển đổi, hay làm getter đổi trạng thái. Một phép thử của ông: nếu viết thành hàm, bạn có đặt tên bắt đầu bằng get hay set không? Nếu không thì có lẽ nó không nên là property. nextFree gọi mạng nên phải là hàm suspend. [[src:book-effective-kotlin]]',
      'Moskała (Effective Kotlin): a Kotlin property is an accessor, not a field, so it can hold derived state; but properties should represent state, not behaviour. Use a function instead when the work is expensive (worse than O(1)), may throw, contains business logic, is not deterministic, is a conversion, or would make a getter change state. His test: if you wrote it as a function, would you prefix it with get or set? If not, it probably should not be a property. nextFree calls the network, so it must be a suspend function. [[src:book-effective-kotlin]]')
    B(C, S_, 2, 'p', 'Moskała: khi giá trị truyền vào không tự nói nghĩa của nó, gọi bằng tên tham số. sleep(100) là 100 gì? Tên tham số an toàn hơn đặt tên biến, vì biến có tên đẹp vẫn có thể bị đặt sai vị trí; kiểu riêng (như Duration) còn mạnh hơn. Ông gợi ý dùng tham số có tên nhất là với tham số Boolean và tham số mặc định. [[src:book-effective-kotlin]]',
      'Moskała: when a value does not explain itself, pass it by parameter name. sleep(100) is 100 what? A named argument is safer than a well-named variable, since a variable can still be put in the wrong position; a dedicated type (such as Duration) is stronger still. He suggests named arguments especially for Boolean and default parameters. [[src:book-effective-kotlin]]')
    B(C, S_, 3, 'kt', 'process(id, true)                         // true là gì?\nprocess(id, cancel = true)                // đọc được, nhưng hàm vẫn làm hai việc\ncancel(id)                                // tốt nhất: hai hàm có tên\nreschedule(id, to = slot)',
      'process(id, true)                         // true means what?\nprocess(id, cancel = true)                // readable, but the function still does two things\ncancel(id)                                // best: two named functions\nreschedule(id, to = slot)')

    S_ = 'bugs'
    a(C + '.sec.%s.title' % S_, 'Hai lỗi hay gặp', 'Two common bugs')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'bug', 'Mất mạng, danh sách có 3 lịch hẹn nhưng huy hiệu báo 0.', 'Offline, the list has 3 bookings but the badge says 0.')
    B(C, S_, 1, 'cause', 'getAppointments() đọc rồi xóa cache; màn hình gọi nó hai lần vì tin tên "get" và kiểu trả về List.', 'getAppointments() reads and then clears the cache; the screen calls it twice, trusting the "get" name and the List return type.')
    B(C, S_, 1, 'fix', 'Tách thành query appointments() chỉ đọc và command clearExpiredCache() gọi ở nơi có chủ đích. Thêm test: gọi appointments() hai lần khi mất mạng trả cùng kết quả.', 'Split into a read-only query appointments() and a command clearExpiredCache() called deliberately. Add a test: calling appointments() twice offline gives the same result.')
    B(C, S_, 2, 'bug', 'Màn hình đặt lịch đơ một giây mỗi lần mở.', 'The booking screen freezes for a second every time it opens.')
    B(C, S_, 2, 'cause', 'val nextFree có getter gọi mạng đồng bộ; Compose đọc nó trong lúc vẽ, trên luồng chính, mà người đọc mã không ngờ một property lại tốn kém như vậy.', 'val nextFree has a getter making a blocking network call; Compose reads it while drawing, on the main thread, and readers never expect a property to be that expensive.')
    B(C, S_, 2, 'fix', 'Đổi thành suspend fun findNextFreeSlot(doctor): Slot?, gọi từ ViewModel trong coroutine và đưa kết quả vào state.', 'Make it suspend fun findNextFreeSlot(doctor): Slot?, called from the ViewModel in a coroutine, with the result put into state.')

    S_ = 'ex'
    a(C + '.sec.%s.title' % S_, 'Bài tập', 'Exercise')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'ex', 'Che tên các hàm dưới đây, đoán từng hàm đọc hay ghi, rồi viết lại để mọi hàm tuân theo CQS và có tên nói đúng việc.', 'X out the names below, guess whether each reads or writes, then rewrite so every function follows CQS and has a name stating what it does.')
    B(C, S_, 1, 'exkt', 'class ReminderStore(private val prefs: Prefs) {\n    fun check(id: String): Boolean {\n        val seen = prefs.has(id)\n        prefs.put(id)              // đánh dấu đã nhắc\n        return seen\n    }\n    fun list(flag: Boolean): List<Reminder> =\n        if (flag) prefs.all().filter { it.sent } else prefs.all()\n    val count: Int get() = prefs.all().size\n}',
      'class ReminderStore(private val prefs: Prefs) {\n    fun check(id: String): Boolean {\n        val seen = prefs.has(id)\n        prefs.put(id)              // marks as reminded\n        return seen\n    }\n    fun list(flag: Boolean): List<Reminder> =\n        if (flag) prefs.all().filter { it.sent } else prefs.all()\n    val count: Int get() = prefs.all().size\n}')
    B(C, S_, 1, 'hint', 'check trả Boolean nhưng có ghi. list nhận cờ. count đọc toàn bộ danh sách mỗi lần gọi.', 'check returns a Boolean yet writes. list takes a flag. count reads the whole list on every call.')
    B(C, S_, 1, 'sol', 'check vi phạm CQS: tách thành query wasReminded(id) và command markReminded(id). list(flag) làm hai việc: tách thành allReminders() và sentReminders(). count đọc toàn bộ danh sách mỗi lần: nếu danh sách lớn, đổi thành hàm reminderCount() để người đọc biết nó có chi phí; nếu luôn nhỏ thì property vẫn chấp nhận được. Người gọi kiểm rồi đánh dấu rõ ràng: if (!store.wasReminded(id)) { notify(); store.markReminded(id) }.',
      'check breaks CQS: split it into a query wasReminded(id) and a command markReminded(id). list(flag) does two things: split it into allReminders() and sentReminders(). count reads the whole list each time: if the list can be large, make it a function reminderCount() so readers see it has a cost; if it is always tiny, a property is still acceptable. The caller checks and then marks explicitly: if (!store.wasReminded(id)) { notify(); store.markReminded(id) }.')
    B(C, S_, 1, 'solkt', 'class ReminderStore(private val prefs: Prefs) {\n    fun wasReminded(id: ReminderId): Boolean = prefs.has(id)\n    fun markReminded(id: ReminderId) { prefs.put(id) }\n    fun allReminders(): List<Reminder> = prefs.all()\n    fun sentReminders(): List<Reminder> = prefs.all().filter { it.sent }\n    fun reminderCount(): Int = prefs.all().size\n}')

    S_ = 'honest'
    a(C + '.sec.%s.title' % S_, 'Chương này giản lược những gì', 'What this chapter simplifies')
    a(C + '.sec.%s.badge' % S_, 'simplified')
    B(C, S_, 1, 'p', 'X out names, CQS và thứ bậc giao tiếp theo Mark Seemann, Code That Fits in Your Head 8.1.3–8.1.7; chỉ dẫn đặt tên, side effect, tham số cờ và ví dụ set trả Boolean theo Robert C. Martin, Clean Code; property và tham số có tên theo Marcin Moskała, Effective Kotlin, 17; quy ước đặt tên theo Kotlin coding conventions. Đọc ngày 2026-11-24, diễn đạt lại; ví dụ của sách viết lại bằng Kotlin. Đây là chỉ dẫn của tác giả, không phải luật của ngôn ngữ. Lớp AppointmentRepo, hai lỗi và mọi con số là của site. Chương không bàn định dạng mã (Clean Code); dùng trình định dạng của IDE theo quy ước Kotlin là đủ cho track này.',
      'X out names, CQS and the hierarchy of communication follow Mark Seemann, Code That Fits in Your Head 8.1.3–8.1.7; naming guidelines, side effects, flag arguments and the Boolean-returning set example follow Robert C. Martin, Clean Code; properties and named arguments follow Marcin Moskała, Effective Kotlin and 17; naming conventions follow the Kotlin coding conventions. Read on 2026-11-24 and paraphrased; the books\' examples are rewritten in Kotlin. These are the authors\' guidelines, not language rules. The AppointmentRepo class, both bugs and every number are the site\'s. The chapter does not cover code formatting (Clean Code); the IDE formatter following Kotlin\'s conventions is enough for this track.')

    for q, qv, qe, av, ae, wv, we in [
        ('q1', 'Theo CQS, hàm fun xxx(id: AppointmentId): Appointment? có được đổi trạng thái không?', 'Under CQS, may fun xxx(id: AppointmentId): Appointment? change state?', 'Không: nó trả dữ liệu nên là query.', 'No: it returns data, so it is a query.', 'Hàm trả dữ liệu không có side effect; hàm có side effect không trả dữ liệu.', 'Functions that return data have no side effects; functions with side effects return no data.'),
        ('q2', 'Vì sao save(a): Boolean khó đọc trong if (save(a))?', 'Why is save(a): Boolean hard to read in if (save(a))?', 'Không rõ nó hỏi hay làm, và true nghĩa là gì.', 'It is unclear whether it asks or acts, and what true means.', 'Martin: tách thành một query kiểm tra và một command ghi.', 'Martin: split it into a query that checks and a command that writes.'),
        ('q3', 'Khi nào nên dùng hàm thay property trong Kotlin?', 'When should you use a function instead of a property in Kotlin?', 'Khi việc đó tốn kém, có thể ném lỗi, có logic nghiệp vụ hay không tất định.', 'When the work is expensive, may throw, holds business logic or is not deterministic.', 'Effective Kotlin: property biểu diễn trạng thái, không phải hành vi.', 'Effective Kotlin: properties represent state, not behaviour.'),
        ('q4', 'Theo thứ bậc giao tiếp của Seemann, kênh nào mạnh nhất?', 'In Seemann\'s hierarchy of communication, which channel is strongest?', 'Kiểu.', 'Types.', 'Sai kiểu thì không biên dịch được; tên, comment, tài liệu đều có thể cũ đi.', 'Wrong types do not compile; names, comments and docs can all go stale.')]:
        a(C + '.quiz.%s.q' % q, qv, qe); a(C + '.quiz.%s.a' % q, av, ae); a(C + '.quiz.%s.why' % q, wv, we)
