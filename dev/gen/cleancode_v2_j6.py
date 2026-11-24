# Mã sạch · J6: refactor từng bước nhỏ (Phần 2: test và thay đổi an toàn)
# Nguồn: Martin, Clean Craftsmanship ch.5 (định nghĩa: chuỗi thay đổi nhỏ giữ hành vi, chứng minh bằng test sau MỖI thay đổi; nhỏ tới mức không
# phải gỡ lỗi; Rule 15 tránh dùng debugger; bộ công cụ Rename, Extract Method/Variable/Field; kỷ luật: test, test nhanh, refactor liên tục,
# không để test đỏ quá vài phút, đổi cấu trúc dữ liệu lớn bằng cách dựng cấu trúc mới song song rồi chuyển dần; chừa đường lui bằng tag và
# git reset); Seemann, Code That Fits in Your Head 10.2 (Strangler: thay đổi lớn làm song song, không tại chỗ; câu của Kent Beck; câu chuyện một
# tuần không biên dịch được), A.24 (dưới nửa ngày thì không cần gì đặc biệt), 11.1.3, A.22; Martin, Clean Code ch.17 (danh mục mùi: F3, G5,
# G30…). Đọc 2026-11-24, diễn đạt lại.

SEC_ORDER = {'j6': ['hook', 'what', 'toolkit', 'disciplines', 'strangler', 'bugs', 'ex', 'honest']}


def add(a):
    def B(ch, sec, n, field, vi, en=None):
        a('%s.sec.%s.b.%02d.%s' % (ch, sec, n, field), vi, vi if en is None else en)

    a('preset.refactor', 'Mã sạch · refactor từng bước nhỏ', 'Clean code · refactoring in small steps')
    m = lambda k, vi, en=None: a('m.refactor.' + k, vi, en)
    m('title', 'Một lần sửa lớn, hay một chuỗi bước nhỏ luôn xanh', 'One big rewrite, or a chain of small always-green steps')
    m('overview', 'Appointment.time đang là chuỗi "2026-11-30 09:00"; cần đổi thành LocalDateTime ở mọi nơi dùng nó: kho dữ liệu, danh sách, chi tiết, sắp xếp và lịch nhắc. Cách thứ nhất: đổi tại chỗ một lần, sửa hết lỗi biên dịch, cuối ngày mới chạy test. Cách thứ hai: thêm trường mới bên cạnh trường cũ, chuyển từng nơi một, mỗi bước chạy test và commit.',
      'Appointment.time is a string "2026-11-30 09:00"; it must become a LocalDateTime everywhere it is used: storage, the list, the detail screen, sorting and reminders. First approach: change it in place in one go, fix all compile errors, run the tests at the end of the day. Second approach: add the new field beside the old one, move each user over one at a time, running the tests and committing after every step.')
    m('wrapup', 'Đổi tại chỗ để lại 40 lỗi biên dịch, cả buổi chiều không chạy được test nào, và khi chạy thì 3 test đỏ mà 8 thay đổi đều bị nghi. Không biết bước nào sai nên phải hoàn tác cả 5 giờ. Đổi song song (strangler) giữ mọi test xanh sau mỗi bước; bước 4 đỏ vì lịch nhắc dùng giờ UTC, nhưng chỉ một thay đổi bị nghi, hoàn tác mất 15 phút, làm lại bước nhỏ hơn rồi đi tiếp. Cả quá trình app luôn ở trạng thái phát hành được.',
      'Changing in place leaves 40 compile errors, no test can run all afternoon, and when they finally run, 3 fail with all 8 changes under suspicion. Nobody knows which step was wrong, so the whole 5 hours are reverted. Changing side by side (strangler) keeps every test green after each step; step 4 fails because reminders use UTC, but only one change is suspect, the revert costs 15 minutes, and a smaller redo moves on. Throughout, the app stays releasable.')
    m('simp.1', 'Tám thay đổi, thời gian (15 phút mỗi bước nhỏ, 5 giờ cho cả lần sửa lớn) và số lỗi biên dịch là minh họa. Lỗi múi giờ được chọn vì nó hay gặp khi chuyển chuỗi giờ sang kiểu ngày giờ.', 'Eight changes, the timings (15 minutes per small step, 5 hours for the big rewrite) and the compile error count are illustrative. The time zone bug is chosen because it is common when moving time strings to date-time types.')
    m('simp.2', 'Định nghĩa refactor và các kỷ luật theo Robert C. Martin; strangler theo Seemann (tên mẫu do Martin Fowler đặt). Mô phỏng không bàn công cụ refactor tự động của IDE, vốn an toàn sẵn.', 'The definition of refactoring and the disciplines follow Robert C. Martin; the strangler follows Seemann (the pattern was named by Martin Fowler). The simulation does not cover the IDE\'s automated refactorings, which are already safe.')
    m('ctl.hint', 'Đổi cách làm rồi đi lại; nhìn dãy ô commit và số thay đổi bị nghi khi test đỏ.', 'Switch the approach and walk again; watch the commit strip and how many changes are suspect when a test fails.')
    m('ctl.case', 'Cách làm', 'Approach')
    for k, vi, en in [('big', 'đổi tại chỗ một lần', 'change in place in one go'), ('small', 'song song, từng bước nhỏ', 'side by side, small steps')]:
        m('ctl.case.' + k, vi, en)
    m('diagramTitle', 'Thay đổi, biên dịch, test, commit', 'Change, compile, test, commit')
    m('diagramDesc', 'Mỗi thay đổi đi qua biên dịch và test trước khi thành commit', 'Each change goes through compiling and testing before it becomes a commit')
    for k, vi, en in [('edit', 'Thay đổi', 'Change'), ('build', 'Biên dịch', 'Compile'), ('test', 'Test', 'Tests'), ('commit', 'Commit', 'Commit')]:
        m('n.' + k, vi, en)
    m('met.suspects', 'Thay đổi bị nghi khi test đỏ', 'Changes suspected when a test fails'); m('met.lost', 'Phút công phải bỏ', 'Minutes of work thrown away'); m('met.release', 'Phát hành được ngay', 'Releasable right now')
    a('cap.refactor', 'Thay đổi đi qua biên dịch, test, rồi mới thành commit. Nút đỏ: nơi dòng chảy bị chặn.', 'A change goes through compiling and testing before it becomes a commit. Red node: where the flow is blocked.')
    S = [
        ('big', 's1', 'Đổi kiểu tại chỗ, sửa nửa số chỗ dùng', 'Change the type in place, fix half the users',
         'Appointment.time thành LocalDateTime. Kho dữ liệu, danh sách và lịch nhắc được sửa; còn 17 lỗi biên dịch. Chưa thể chạy test.', 'Appointment.time becomes a LocalDateTime. Storage, the list and reminders are fixed; 17 compile errors remain. No test can run yet.'),
        ('big', 's2', 'Sửa nốt, lỗi biên dịch lan ra', 'Fix the rest, compile errors spread',
         'Màn chi tiết, sắp xếp và các hàm định dạng kéo theo thêm lỗi ở file khác: 40 lỗi ở 12 file. Ba giờ trôi qua mà app không chạy.', 'The detail screen, sorting and formatting helpers drag in errors in other files: 40 errors across 12 files. Three hours pass with the app not running.'),
        ('big', 's3', 'Biên dịch được; chạy test: 3 đỏ', 'It compiles; run the tests: 3 fail',
         'Cuối buổi chiều mới biên dịch được. Ba test đỏ, và cả 8 thay đổi đều có thể là nguyên nhân. Bật debugger.', 'Late in the afternoon it finally compiles. Three tests fail, and any of the 8 changes could be the cause. Out comes the debugger.'),
        ('big', 's4', 'Hoàn tác cả ngày', 'Revert the whole day',
         'Không tìm ra nhanh lỗi nằm ở đâu, sắp tới giờ phát hành: git reset về sáng nay. 5 giờ công bỏ đi.', 'The fault cannot be found quickly and the release is near: git reset to this morning. 5 hours of work thrown away.'),
        ('small', 's1', 'Thêm startsAt cạnh time; kho ghi cả hai', 'Add startsAt beside time; storage writes both',
         'Hai bước nhỏ, mỗi bước chạy test (xanh) và commit. Chưa ai đọc trường mới, nên không gì vỡ.', 'Two small steps, each running the tests (green) and committing. Nobody reads the new field yet, so nothing breaks.'),
        ('small', 's2', 'Chuyển danh sách; chuyển lịch nhắc: đỏ', 'Move the list; move reminders: red',
         'Danh sách đọc startsAt: xanh, commit. Lịch nhắc đọc startsAt nhưng hiểu là giờ UTC, nhắc lệch 7 tiếng: test đỏ. Chỉ một thay đổi bị nghi; hoàn tác bước đó, mất 15 phút.', 'The list reads startsAt: green, commit. Reminders read startsAt but treat it as UTC, 7 hours off: a test fails. Only one change is suspect; revert that step, 15 minutes lost.'),
        ('small', 's3', 'Làm lại lịch nhắc với múi giờ; chuyển chi tiết, sắp xếp', 'Redo reminders with the time zone; move detail and sorting',
         'Bước 4′ dùng múi giờ của phòng khám: xanh. Màn chi tiết và sắp xếp chuyển sang startsAt: xanh, mỗi bước một commit.', 'Step 4′ uses the clinic\'s time zone: green. The detail screen and sorting move to startsAt: green, one commit each.'),
        ('small', 's4', 'Bỏ đọc time, rồi xóa trường cũ', 'Stop reading time, then delete the old field',
         'Khi không còn nơi nào đọc time, xóa nó. Mọi commit đều xanh; app phát hành được ở bất kỳ commit nào.', 'When nothing reads time any more, delete it. Every commit is green; the app is releasable at any commit.'),
    ]
    for case, k, tv, te, xv, xe in S:
        sid = case + '.' + k
        m('s.%s.title' % sid, tv, te); m('s.%s.explain' % sid, xv, xe); m('ev.' + sid, tv, te)
    for k, vi, en in [
        ('try', 'Theo dãy ô từ trái sang phải; mỗi ô là một thay đổi, màu là kết quả test sau thay đổi đó.', 'Follow the strip left to right; each cell is one change, coloured by the test result after it.'),
        ('big.s2', 'Seemann (10.2) kể chính lần ông đổi một lớp nền tảng tại chỗ: một tuần sau mã vẫn chưa biên dịch được. Ông rút ra quy tắc: thay đổi lớn thì đừng làm tại chỗ, hãy làm song song. [[src:book-seemann]]', 'Seemann (10.2) tells of changing a fundamental class in place himself: a week later the code still did not compile. His rule from it: for any significant change, do not make it in place; make it side by side. [[src:book-seemann]]'),
        ('big.s3', 'Martin (Clean Craftsmanship ch.5): mỗi bước refactor phải đủ nhỏ để không phải gỡ lỗi; Rule 15: tránh dùng debugger. Cần debugger nghĩa là bước đã quá lớn. [[src:book-craft]]', 'Martin (Clean Craftsmanship ch.5): each refactoring step must be small enough that you will not have to debug; Rule 15: avoid using debuggers. Needing the debugger means the step was too big. [[src:book-craft]]'),
        ('big.s4', 'Seemann (A.24): đi từ một trạng thái nhất quán tới trạng thái nhất quán tiếp theo trong chưa tới nửa ngày thì không cần gì đặc biệt; dài hơn thì cần strangler. [[src:book-seemann]]', 'Seemann (A.24): if you can go from one consistent state to the next in under half a day, nothing special is needed; longer, and you need a strangler. [[src:book-seemann]]'),
        ('small.s1', 'Martin (ch.5): để đổi một cấu trúc dữ liệu nền tảng, dựng cấu trúc mới song song với cấu trúc cũ, rồi chuyển dần từng phần mã sang, giữ test xanh suốt quá trình. [[src:book-craft]]', 'Martin (ch.5): to change a fundamental data structure, build the new one alongside the old, then move each part of the code over gradually, keeping the tests passing throughout. [[src:book-craft]]'),
        ('small.s2', 'Test đỏ ngay sau một bước nhỏ chỉ ra đúng chỗ sai. Martin: chừa đường lui; đặt tag trước một chuỗi refactor để có thể quay lại. [[src:book-craft]]', 'A test failing right after a small step points at exactly what went wrong. Martin: leave yourself an out; tag before a chain of refactorings so you can go back. [[src:book-craft]]'),
        ('small.s3', 'Kent Beck, theo trích dẫn của Seemann: với mỗi thay đổi, trước hết làm cho nó dễ (việc này có thể khó), rồi làm thay đổi dễ đó. [[src:book-seemann]]', 'Kent Beck, as quoted by Seemann: for each desired change, make the change easy (this may be hard), then make the easy change. [[src:book-seemann]]'),
        ('small.s4', 'Strangler lấy tên từ cây đa bóp cổ (strangler fig): cây mới mọc quanh cây chủ cho tới khi cây cũ không còn cần. Martin Fowler đặt tên cho mẫu này; Seemann thấy nó dùng được ở gần như mọi quy mô. [[src:book-seemann]]', 'The strangler is named after the strangler fig: the new vine grows around the host until the old tree is no longer needed. Martin Fowler named the pattern; Seemann finds it useful at almost any scale. [[src:book-seemann]]')]:
        m('co.' + k, vi, en)

    z = lambda k, vi, en=None: a('vz.' + k, vi, en)
    z('tab.refactor', 'Dãy ô commit', 'Commit strip')
    z('rf.cap', 'Mỗi cột là một thay đổi theo thứ tự thời gian. Hàng trên: test sau thay đổi đó; hàng dưới: đã commit chưa.', 'Each column is one change, in time order. Top row: the tests after that change; bottom row: whether it was committed.')
    z('rf.row.test', 'Test', 'Tests'); z('rf.row.commit', 'Commit', 'Commit')
    for k, vi, en in [('c1', 'thêm startsAt', 'add startsAt'), ('c2', 'kho ghi cả hai', 'storage writes both'), ('c3', 'danh sách', 'list'), ('c4', 'lịch nhắc', 'reminders'), ('c4b', 'lịch nhắc + múi giờ', 'reminders + zone'),
                      ('c5', 'màn chi tiết', 'detail screen'), ('c6', 'sắp xếp', 'sorting'), ('c7', 'bỏ đọc time', 'stop reading time'), ('c8', 'xóa time', 'delete time')]:
        z('rf.c.' + k, vi, en)
    for k, vi, en in [('green', 'xanh', 'green'), ('red', 'đỏ', 'red'), ('nobuild', 'không biên dịch', 'no build'), ('sus', 'nghi', 'suspect'), ('none', '·', '·'), ('yes', '✓', '✓'), ('no', '—', '—'), ('undo', 'hoàn tác', 'reverted'), ('gone', 'bỏ', 'discarded')]:
        z('rf.st.' + k, vi, en)
    z('rf.status', 'Biên dịch: {b}. Test đỏ: {r}. Thay đổi bị nghi: {s}.', 'Build: {b}. Failing tests: {r}. Suspect changes: {s}.')
    z('rf.build.ok', 'được', 'ok'); z('rf.build.err', '{n} lỗi', '{n} errors')
    z('rf.legend', 'Ô gạch đỏ: test đỏ, không biên dịch được, hay thay đổi bị nghi. Ô đậm: test xanh. Viền đậm: thay đổi của bước này.', 'Red hatched: failing tests, no build, or a suspect change. Bold: green tests. Bold outline: this step\'s changes.')

    C = 'j6'
    a(C + '.title', 'Refactor từng bước nhỏ', 'Refactoring in small steps')
    a(C + '.essence', 'Refactor là chuỗi thay đổi nhỏ cải thiện cấu trúc mà không đổi hành vi, và bộ test phải xanh sau MỖI thay đổi. Mỗi bước nhỏ tới mức không cần gỡ lỗi.\nThay đổi lớn thì không làm tại chỗ mà làm song song (strangler): thêm cái mới cạnh cái cũ, chuyển dần từng nơi, xóa cái cũ khi không còn ai dùng.\nTest đỏ sau một bước nhỏ chỉ đúng một nghi phạm; hoàn tác bước đó rẻ. Test đỏ sau cả ngày sửa thì mọi thay đổi đều bị nghi.',
      'Refactoring is a sequence of small changes that improve structure without changing behaviour, with the tests green after EVERY change. Each step is small enough that no debugging is needed.\nBig changes are not made in place but side by side (strangler): add the new beside the old, move users over one at a time, delete the old when nobody uses it.\nA test failing after a small step has exactly one suspect; reverting that step is cheap. A test failing after a day of edits makes every change a suspect.')
    a(C + '.goal.g1', 'Đã thấy test đỏ sau một bước nhỏ', 'Saw a test fail after a small step')
    a(C + '.goal.g2', 'Đã thấy kết quả cuối', 'Saw the final outcome')
    a(C + '.sim.cleancode.refactor', 'sửa lớn một lần hay từng bước nhỏ', 'one big rewrite or small steps')

    S_ = 'hook'
    a(C + '.sec.%s.title' % S_, 'Đoán trước khi đọc', 'Predict before reading')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'predict', 'Bạn dành cả ngày refactor màn Lịch hẹn: đổi kiểu dữ liệu, tách lớp, đổi tên. Cuối ngày chạy test: 3 đỏ. Bạn có biết thay đổi nào gây ra không? Bạn sẽ làm gì tiếp?',
      'You spend a whole day refactoring the Appointments screen: changing a data type, splitting classes, renaming. At the end of the day you run the tests: 3 fail. Do you know which change caused it? What do you do next?')
    B(C, S_, 1, 'ans', 'Thường là không biết: mọi thay đổi trong ngày đều là nghi phạm, nên phải bật debugger hoặc hoàn tác cả ngày. Nếu chạy test sau mỗi bước nhỏ và commit khi xanh, lần đỏ đầu tiên chỉ có một nghi phạm và hoàn tác chỉ mất vài phút. Mô phỏng ngay dưới so hai cách cho cùng một thay đổi kiểu dữ liệu.',
      'Usually not: every change of the day is a suspect, so out comes the debugger or the whole day gets reverted. Running the tests after each small step and committing when green means the first failure has a single suspect and a revert costs minutes. The simulation just below compares both ways for the same data type change.')

    S_ = 'what'
    a(C + '.sec.%s.title' % S_, 'Refactor là gì, nhỏ cỡ nào', 'What refactoring is, and how small')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'p', 'Martin (Clean Craftsmanship ch.5) định nghĩa refactor là một chuỗi thay đổi nhỏ cải thiện cấu trúc mà không đổi hành vi, và điều đó được chứng minh bằng việc bộ test đầy đủ xanh sau mỗi thay đổi trong chuỗi. Hai điểm then chốt: hành vi giữ nguyên, và từng bước nhỏ. Nhỏ cỡ nào? Thước đo của ông: nhỏ tới mức không phải gỡ lỗi; ông đặt hẳn thành Rule 15: tránh dùng debugger. [[src:book-craft]]',
      'Martin (Clean Craftsmanship ch.5) defines refactoring as a sequence of small changes that improve the structure of the software without changing its behaviour, as proven by a comprehensive test suite passing after each change in the sequence. Two key points: behaviour is preserved, and each step is small. How small? His rubric: small enough that you will not have to debug; he even makes it Rule 15: avoid using debuggers. [[src:book-craft]]')
    B(C, S_, 2, 'p', 'Refactor không phải một hạng mục lên lịch riêng. Theo Martin nó là một phần của mỗi vòng đỏ, xanh, refactor; ngay cả thay đổi thiết kế lớn cũng được làm dần, xen với việc thêm tính năng và sửa lỗi, không dừng cả nhóm lại để "refactor". [[src:book-craft]]',
      'Refactoring is not a separately scheduled item. For Martin it is part of every red, green, refactor cycle; even large design changes are made gradually, interleaved with features and bug fixes, without stopping the team to "refactor". [[src:book-craft]]')

    S_ = 'toolkit'
    a(C + '.sec.%s.title' % S_, 'Bộ công cụ cơ bản và mùi mã', 'The basic toolkit and code smells')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'p', 'Martin nêu bộ công cụ cơ bản: Rename, Extract Method, Extract Variable, Extract Field; IDE làm sẵn nhiều thao tác như vậy và chúng an toàn với cả mã lẫn test (Seemann 11.1.3). Những thay đổi khác, như thêm tham số, rủi ro hơn và cần test bảo vệ. Khi nào nên refactor? Clean Code ch.17 có danh mục mùi để nhận ra, ví dụ F3 tham số cờ, G5 trùng lặp, G9 mã chết, G30 hàm làm nhiều việc. Danh mục là gợi ý để xem lại, không phải luật. [[src:book-craft]] [[src:book-seemann]] [[src:book-cleancode]]',
      'Martin lists a basic toolkit: Rename, Extract Method, Extract Variable, Extract Field; the IDE does many such operations and they are safe for code and tests alike (Seemann 11.1.3). Other changes, such as adding a parameter, are riskier and need tests to protect them. When to refactor? Clean Code ch.17 has a catalogue of smells to spot it, such as F3 flag arguments, G5 duplication, G9 dead code, G30 functions doing more than one thing. The catalogue suggests where to look; it is not a law. [[src:book-craft]] [[src:book-seemann]] [[src:book-cleancode]]')
    B(C, S_, 2, 'note', 'Android Studio có sẵn các thao tác này trong menu Refactor (đổi tên, tách hàm, tách biến, đổi chữ ký). Dùng chúng thay vì sửa tay khi có thể; sau mỗi thao tác vẫn chạy test.',
      'Android Studio provides these operations in its Refactor menu (rename, extract function, extract variable, change signature). Use them instead of hand edits when possible; still run the tests after each one.')
    B(C, S_, 2, 'kind', 'android')

    S_ = 'disciplines'
    a(C + '.sec.%s.title' % S_, 'Kỷ luật khi refactor', 'The disciplines of refactoring')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'p', 'Martin (ch.5) nêu các kỷ luật. Có test, và test phải nhanh: chạy được tập con liên quan trong vài giây, cả bộ thì thỉnh thoảng. Refactor liên tục như rửa bát trong lúc nấu, đừng để dồn. Mạnh dạn sửa. Nhưng giữ test xanh: đừng bao giờ để test đỏ quá vài phút. Thay đổi kéo dài nhiều giờ hay nhiều ngày thì chia nhỏ, giữ mọi thứ xanh trong lúc vẫn làm việc khác. Và chừa đường lui: đặt tag trước một chuỗi refactor để git reset được khi đi vào ngõ cụt. [[src:book-craft]]',
      'Martin (ch.5) lists the disciplines. Have tests, and keep them quick: run the relevant subset in seconds, the whole suite now and then. Refactor continuously, like washing dishes while cooking, before the mess piles up. Be bold. But keep the tests passing: never leave them broken for more than a few minutes. Changes taking hours or days are split into chunks, keeping everything green while other work continues. And leave yourself an out: tag before a chain of refactorings so you can git reset when it hits a dead end. [[src:book-craft]]')

    S_ = 'strangler'
    a(C + '.sec.%s.title' % S_, 'Strangler: làm song song, không làm tại chỗ', 'Strangler: side by side, not in place')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'p', 'Seemann (10.2) kể lần ông đổi một lớp nền tảng tại chỗ, mong trình biên dịch chỉ ra mọi chỗ cần sửa; một tuần sau mã vẫn chưa biên dịch được. Quy tắc ông rút ra: thay đổi đáng kể thì đừng làm tại chỗ, hãy làm song song. Đó là mẫu Strangler, Martin Fowler đặt tên theo cây đa bóp cổ, ban đầu cho việc thay cả hệ thống cũ; Seemann thấy nó dùng được ở mọi quy mô, kể cả một trường dữ liệu. Ngưỡng của ông (A.24): đi được từ trạng thái nhất quán này sang trạng thái nhất quán kế tiếp trong chưa tới nửa ngày thì không cần gì đặc biệt. [[src:book-seemann]]',
      'Seemann (10.2) recounts changing a fundamental class in place, hoping the compiler would point at every call site; a week later the code still did not compile. His rule from it: for any significant change, do not make it in place; make it side by side. That is the Strangler pattern, named by Martin Fowler after the strangler fig and originally meant for replacing whole legacy systems; Seemann finds it useful at any scale, down to a single field. His threshold (A.24): if you can get from one consistent state to the next in under half a day, nothing special is needed. [[src:book-seemann]]')
    B(C, S_, 2, 'kt', 'data class Appointment(\n    @Deprecated("dùng startsAt") val time: String,     // cũ: còn đọc được trong lúc chuyển\n    val startsAt: LocalDateTime? = null,                // mới, đặt cạnh cái cũ\n)\n// chuyển từng nơi đọc sang startsAt, mỗi nơi một commit xanh;\n// khi không còn ai đọc time: xóa time, bỏ dấu ? của startsAt',
      'data class Appointment(\n    @Deprecated("use startsAt") val time: String,       // old: still readable during the move\n    val startsAt: LocalDateTime? = null,                // new, placed beside the old\n)\n// move each reader to startsAt, one green commit each;\n// when nothing reads time any more: delete time, drop the ? on startsAt')

    S_ = 'bugs'
    a(C + '.sec.%s.title' % S_, 'Hai lỗi hay gặp', 'Two common bugs')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'bug', 'Refactor cả màn hình trong một nhánh, app hỏng, không biết bước nào gây ra.', 'A whole screen refactored in one branch, the app breaks, and nobody knows which step caused it.')
    B(C, S_, 1, 'cause', 'Nhiều thay đổi dồn vào một lần, test chỉ chạy ở cuối; mọi thay đổi đều là nghi phạm.', 'Many changes piled into one go, tests run only at the end; every change is a suspect.')
    B(C, S_, 1, 'fix', 'Hoàn tác về tag trước khi bắt đầu, làm lại theo từng bước nhỏ, chạy test và commit sau mỗi bước. Nếu đã có lịch sử commit, dùng chia đôi (chương J7) để tìm commit gây lỗi.', 'Reset to the tag from before you started, redo it in small steps, running the tests and committing after each. If a commit history exists, use bisection (chapter J7) to find the guilty commit.')
    B(C, S_, 2, 'bug', 'Sau khi đổi giờ hẹn sang LocalDateTime, lời nhắc tới lệch 7 tiếng.', 'After moving appointment times to LocalDateTime, reminders arrive 7 hours off.')
    B(C, S_, 2, 'cause', 'Chuỗi giờ cũ ngầm là giờ địa phương của phòng khám; mã mới đổi LocalDateTime sang Instant theo UTC.', 'The old time string was implicitly the clinic\'s local time; the new code converts the LocalDateTime to an Instant as UTC.')
    B(C, S_, 2, 'fix', 'Chuyển đổi bằng múi giờ của phòng khám (atZone(clinicZone)); thêm test lịch nhắc với một giờ cụ thể để lỗi này đỏ ngay ở bước chuyển lịch nhắc.', 'Convert with the clinic\'s time zone (atZone(clinicZone)); add a reminder test with a concrete time so this fails right at the reminder step.')

    S_ = 'ex'
    a(C + '.sec.%s.title' % S_, 'Bài tập', 'Exercise')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'ex', 'Phòng khám muốn đổi Doctor.name: String thành hai trường firstName và lastName để sắp xếp theo họ. Tên đang được đọc ở 6 nơi: danh sách bác sĩ, màn đặt lịch, thông báo, PDF hóa đơn, tìm kiếm và đồng bộ với server. Viết chuỗi bước nhỏ theo kiểu strangler, mỗi bước giữ test xanh.', 'The clinic wants to change Doctor.name: String into firstName and lastName to sort by surname. The name is read in 6 places: the doctor list, the booking screen, notifications, the invoice PDF, search and server sync. Write a chain of small strangler steps, each keeping the tests green.')
    B(C, S_, 1, 'hint', 'Thêm trường mới trước, ghi cả hai, chuyển từng nơi đọc, rồi mới xóa. Server sync là ranh giới với bên ngoài: nó có đổi cùng lúc không?', 'Add the new fields first, write both, move each reader, then delete. Server sync is a boundary with the outside: does it change at the same time?')
    B(C, S_, 1, 'sol', 'Bước 1: thêm firstName, lastName có giá trị mặc định, tính từ name khi đọc dữ liệu cũ. Bước 2: mọi nơi ghi Doctor ghi cả ba trường. Bước 3–7: chuyển lần lượt danh sách (sắp xếp theo lastName), màn đặt lịch, thông báo, PDF, tìm kiếm; mỗi bước một commit xanh. Bước 8: đồng bộ server vẫn gửi name ghép từ hai trường cho tới khi API mới sẵn sàng (giữ tương thích như chương I12). Bước 9: đánh dấu name là @Deprecated, xóa khi không còn ai đọc. Mỗi bước dưới nửa giờ; nếu một bước đỏ, hoàn tác đúng bước đó.',
      'Step 1: add firstName and lastName with defaults, derived from name when reading old data. Step 2: every place writing a Doctor writes all three fields. Steps 3–7: move the list (sorted by lastName), the booking screen, notifications, the PDF and search, one green commit each. Step 8: server sync keeps sending name built from the two fields until the new API is ready (staying compatible, as in chapter I12). Step 9: mark name @Deprecated and delete it when nothing reads it. Each step under half an hour; if one fails, revert exactly that step.')

    S_ = 'honest'
    a(C + '.sec.%s.title' % S_, 'Chương này giản lược những gì', 'What this chapter simplifies')
    a(C + '.sec.%s.badge' % S_, 'simplified')
    B(C, S_, 1, 'p', 'Định nghĩa refactor, thước đo "nhỏ tới mức không phải gỡ lỗi", bộ công cụ và các kỷ luật theo Robert C. Martin, Clean Craftsmanship ch.5; strangler, câu chuyện một tuần không biên dịch được, câu của Kent Beck và ngưỡng nửa ngày theo Mark Seemann, Code That Fits in Your Head 10.2, A.24, 11.1.3; danh mục mùi theo Clean Code ch.17. Đọc ngày 2026-11-24, diễn đạt lại. Tám thay đổi, thời gian, số lỗi biên dịch và lỗi múi giờ là minh họa của site. Chương không đi qua catalogue refactoring của Martin Fowler; Clean Code ch.14–16 (ba bài refactor dài bằng Java) nằm ngoài phạm vi theo dàn ý.',
      'The definition of refactoring, the "small enough not to debug" rubric, the toolkit and the disciplines follow Robert C. Martin, Clean Craftsmanship ch.5; the strangler, the week-without-compiling story, Kent Beck\'s quote and the half-day threshold follow Mark Seemann, Code That Fits in Your Head 10.2, A.24, 11.1.3; the smell catalogue follows Clean Code ch.17. Read on 2026-11-24 and paraphrased. The eight changes, timings, compile error count and the time zone bug are the site\'s illustration. The chapter does not walk through Martin Fowler\'s refactoring catalogue; Clean Code ch.14–16 (three long Java refactorings) are out of scope per the outline.')

    for q, qv, qe, av, ae, wv, we in [
        ('q1', 'Theo Martin, một bước refactor nên nhỏ cỡ nào?', 'According to Martin, how small should a refactoring step be?', 'Nhỏ tới mức không phải gỡ lỗi.', 'Small enough that you will not have to debug.', 'Rule 15: tránh dùng debugger; cần debugger nghĩa là bước quá lớn.', 'Rule 15: avoid using debuggers; needing one means the step was too big.'),
        ('q2', 'Strangler nghĩa là gì?', 'What does strangler mean?', 'Làm thay đổi lớn song song: thêm cái mới cạnh cái cũ, chuyển dần, rồi xóa cái cũ.', 'Making a big change side by side: add the new beside the old, move over gradually, then delete the old.', 'Seemann: thay đổi đáng kể thì đừng làm tại chỗ.', 'Seemann: for any significant change, do not make it in place.'),
        ('q3', 'Vì sao test đỏ sau một bước nhỏ dễ xử lý hơn test đỏ cuối ngày?', 'Why is a failure after a small step easier to handle than one at the end of the day?', 'Vì chỉ có một thay đổi bị nghi, và hoàn tác nó rẻ.', 'Because only one change is suspect, and reverting it is cheap.', 'Cuối ngày thì mọi thay đổi đều là nghi phạm.', 'At the end of the day every change is a suspect.'),
        ('q4', 'Theo Martin, test được phép đỏ bao lâu trong lúc refactor?', 'According to Martin, how long may the tests stay red during refactoring?', 'Không quá vài phút.', 'No more than a few minutes.', 'Thay đổi dài thì chia nhỏ, giữ mọi thứ xanh trong lúc vẫn làm việc khác.', 'Long changes are split into chunks, keeping everything green while other work continues.')]:
        a(C + '.quiz.%s.q' % q, qv, qe); a(C + '.quiz.%s.a' % q, av, ae); a(C + '.quiz.%s.why' % q, wv, we)
