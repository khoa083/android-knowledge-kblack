# Gỡ lỗi và hiệu năng · l7: dữ liệu và việc nền: Database Inspector, Background Task Inspector (Phần 2: nhìn vào bên trong app)
# Nguồn (chỉ ghi ở đây và docs/research/debugging.md), đọc 2026-11-25: developer.android.com/studio/inspect/database (xem, truy vấn, sửa database khi app chạy;
# API 26+; Live updates làm bảng chỉ đọc; sửa thì UI quan sát bằng Flow/LiveData thấy ngay; chạy @Query của DAO; tab truy vấn tự do cho phép UPDATE, INSERT,
# DELETE; Keep database connections open; chế độ offline), studio/inspect/task (WorkManager 2.5.0+, API 26+; danh sách, chi tiết: ràng buộc, trạng thái,
# vị trí trong chuỗi; Graph View; job, alarm, wakelock chuyển từ Energy profiler sang), reference WorkInfo.State (ENQUEUED, RUNNING, SUCCEEDED, FAILED,
# BLOCKED, CANCELLED; FAILED và CANCELLED lan sang việc phụ thuộc; isFinished), background-tasks/persistent/getting-started/define-work (mọi ràng buộc
# phải thỏa; UNMETERED; Result.retry, backoff mặc định EXPONENTIAL 30 giây, tối thiểu 10 giây). Bảng booking và chuỗi ba worker là ví dụ của site.

SEC_ORDER = {'l7': ['hook', 'db', 'probe', 'work', 'task', 'bugs', 'ex', 'recall']}


def add(a):
    def B(ch, sec, n, field, vi, en=None):
        a('%s.sec.%s.b.%02d.%s' % (ch, sec, n, field), vi, vi if en is None else en)

    a('preset.inspect', '''Gỡ lỗi · xem database và worker khi app đang chạy''', '''Debugging · inspecting the database and workers while the app runs''')
    m = lambda k, vi, en=None: a('m.inspect.' + k, vi, en)
    m('title', '''Lịch "đã lưu" mà không hiện; đồng bộ kẹt mãi''', '''A booking "saved" but not shown; a sync stuck forever''')
    m('overview', '''Hai lỗi của app Hẹn Khám không có crash, không có stack trace. Lỗi 1: đặt lịch báo thành công, nhưng danh sách lịch trống. Lỗi 2: dòng "đang đồng bộ" hiện mãi không tắt. Cả hai được tìm bằng cách nhìn trực tiếp vào trạng thái của app đang chạy: bảng trong database, và trạng thái các worker của WorkManager. Kết quả truy vấn và trạng thái worker được tính thật từ dữ liệu của mô phỏng.''',
      '''Two ClinicBook bugs with no crash and no stack trace. Bug 1: booking reports success, but the booking list is empty. Bug 2: the "syncing" line never goes away. Both are found by looking straight at the running app\'s state: the tables in the database, and the states of the WorkManager workers. Query results and worker states are really computed from the simulation\'s data.''')
    m('wrapup', '''Lịch đã nằm trong bảng, nhưng ở trạng thái PENDING, còn truy vấn của danh sách chỉ lấy CONFIRMED; sửa thử một dòng ngay trong Database Inspector là danh sách hiện lịch, xác nhận giả thuyết trước khi sửa mã. Đồng bộ kẹt vì worker tải ảnh cần mạng không đo lưu lượng (Wi-Fi) nên đứng ở ENQUEUED trên 4G, và hai worker phía sau đứng ở BLOCKED chờ nó; tách việc tải ảnh khỏi chuỗi đồng bộ thì lịch hẹn đồng bộ được ngay.''',
      '''The booking is in the table, but with status PENDING, while the list\'s query only takes CONFIRMED; editing one row right in Database Inspector makes the list show it, confirming the hypothesis before changing code. The sync is stuck because the photo upload worker needs an unmetered network (Wi-Fi), so it sits in ENQUEUED on 4G, and the two workers behind it sit in BLOCKED waiting for it; taking the photo upload out of the sync chain lets bookings sync right away.''')
    m('simp.1', '''Bảng chỉ có 4 dòng và chuỗi có 3 worker; database và WorkManager thật có nhiều bảng, nhiều việc hơn.''', '''The table has only 4 rows and the chain 3 workers; a real database and WorkManager hold many more tables and jobs.''')
    m('simp.2', '''Truy vấn được áp thật bằng JavaScript lên các dòng của bảng; trạng thái worker được tính thật theo luật của WorkInfo.State: việc chưa thỏa ràng buộc ở ENQUEUED, việc có việc trước chưa xong ở BLOCKED, FAILED và CANCELLED lan sang việc phụ thuộc.''',
      '''The query is really applied in JavaScript to the table\'s rows; worker states are really computed by WorkInfo.State\'s rules: work whose constraints are unmet stays ENQUEUED, work whose prerequisites have not finished is BLOCKED, FAILED and CANCELLED spread to dependent work.''')
    m('ctl.hint', '''Chọn lỗi rồi đi qua bốn bước; xem bảng hay chuỗi worker đổi theo từng bước.''', '''Pick a bug and walk the four steps; watch the table or the worker chain change at each step.''')
    m('ctl.case', '''Lỗi''', '''Bug''')
    m('ctl.case.db', '''lịch đã lưu mà danh sách trống''', '''a saved booking missing from the list'''); m('ctl.case.work', '''đồng bộ kẹt mãi''', '''a sync stuck forever''')
    m('diagramTitle', '''App, database, WorkManager và hai công cụ xem''', '''The app, the database, WorkManager and two inspectors''')
    m('diagramDesc', '''Database Inspector đọc và sửa bảng của app đang chạy; Background Task Inspector đọc trạng thái các worker''', '''Database Inspector reads and edits the running app\'s tables; Background Task Inspector reads the workers\' states''')
    for k, vi, en in [('app', 'App đang chạy', 'The running app'), ('db', 'Cơ sở dữ liệu (Room)', 'Database (Room)'), ('wm', 'WorkManager: chuỗi worker', 'WorkManager: the worker chain'),
                      ('dbi', 'Database Inspector (xem bảng)', 'Database Inspector (tables)'), ('bti', 'Background Task Inspector (xem worker)', 'Background Task Inspector (workers)')]:
        m('n.' + k, vi, en)
    m('met.stored', '''Dòng trong bảng booking''', '''Rows in the booking table'''); m('met.shown', '''Lịch danh sách nhận được''', '''Bookings the list receives''')
    m('met.stuck', '''Worker chưa xong''', '''Workers not finished'''); m('met.cause', '''Nguyên nhân''', '''Cause''')
    for k, vi, en in [('none', 'chưa biết', 'unknown'), ('status', 'lưu PENDING, truy vấn chỉ lấy CONFIRMED', 'saved as PENDING, the query only takes CONFIRMED'),
                      ('fixed', 'đã sửa', 'fixed'), ('wifi', 'worker đầu chuỗi cần Wi-Fi, máy đang dùng 4G', 'the first worker needs Wi-Fi, the phone is on 4G')]:
        m('cause.' + k, vi, en)
    a('cap.inspect', '''Hai công cụ đọc trạng thái của app đang chạy: bảng trong database, trạng thái worker. Ô đỏ: chỗ dữ liệu hay việc nền đang kẹt.''',
      '''Two tools read the running app\'s state: tables in the database, worker states. A red box: where the data or background work is stuck.''')
    S = [
        ('db', 's1', 'Đặt lịch báo thành công, danh sách trống', 'Booking reports success, the list is empty',
         'Người dùng đặt lịch số 42, thấy thông báo "Đã đặt lịch", rồi mở danh sách: không có gì. Không crash, không lỗi trong Logcat. Câu hỏi đầu tiên: lịch có thật sự được ghi vào database không?',
         'The user books appointment 42, sees "Booked", then opens the list: nothing. No crash, no error in Logcat. The first question: was the booking really written to the database?'),
        ('db', 's2', 'Mở bảng booking: dòng 42 có ở đó', 'Open the booking table: row 42 is there',
         'Database Inspector mở bảng booking của app đang chạy. Có 4 dòng, kể cả dòng 42 vừa đặt. Vậy việc lưu không hỏng; vấn đề nằm ở chỗ đọc ra.',
         'Database Inspector opens the running app\'s booking table. There are 4 rows, including row 42 just booked. So saving is not broken; the problem is in reading.'),
        ('db', 's3', 'Chạy đúng truy vấn của danh sách: 0 dòng', 'Run the list\'s own query: 0 rows',
         'Chạy @Query của DAO danh sách ngay trong công cụ: SELECT * FROM booking WHERE status = \'CONFIRMED\'. Kết quả: 0 dòng. Ba dòng cũ đã COMPLETED hay CANCELLED, còn dòng 42 mang status PENDING. Mã đặt lịch mới ghi PENDING (chờ máy chủ xác nhận), còn danh sách chỉ lấy CONFIRMED.',
         'Run the list DAO\'s @Query right in the tool: SELECT * FROM booking WHERE status = \'CONFIRMED\'. Result: 0 rows. The three old rows are COMPLETED or CANCELLED, and row 42 has status PENDING. The new booking code writes PENDING (waiting for the server to confirm), while the list only takes CONFIRMED.'),
        ('db', 's4', 'Kiểm giả thuyết bằng cách sửa một dòng, rồi sửa mã', 'Test the hypothesis by editing a row, then fix the code',
         'Sửa status của dòng 42 thành CONFIRMED ngay trong Database Inspector: danh sách hiện lịch 42 tức thì, vì nó quan sát database bằng Flow. Giả thuyết đúng. Bản sửa thật: danh sách lấy cả PENDING và hiện nhãn "chờ xác nhận".',
         'Change row 42\'s status to CONFIRMED right in Database Inspector: the list shows booking 42 at once, because it observes the database through a Flow. The hypothesis holds. The real fix: the list takes PENDING too and shows a "waiting for confirmation" label.'),
        ('work', 's1', 'Dòng "đang đồng bộ" hiện mãi', 'The "syncing" line never goes away',
         'Sau khi đặt lịch lúc đang dùng 4G, app hiện "đang đồng bộ" suốt nhiều giờ. Không crash, không log lỗi. Việc nền chạy ngoài tầm mắt, nên phải hỏi trực tiếp WorkManager: các worker đang ở trạng thái nào?',
         'After booking on 4G, the app shows "syncing" for hours. No crash, no error log. Background work runs out of sight, so ask WorkManager directly: what state are the workers in?'),
        ('work', 's2', 'Ba worker: một ENQUEUED, hai BLOCKED', 'Three workers: one ENQUEUED, two BLOCKED',
         'Background Task Inspector liệt kê chuỗi: UploadPhotos ở ENQUEUED, SyncBookings và NotifyUser ở BLOCKED. BLOCKED nghĩa là việc trước nó trong chuỗi chưa xong thành công; vấn đề nằm ở worker đầu chuỗi.',
         'Background Task Inspector lists the chain: UploadPhotos in ENQUEUED, SyncBookings and NotifyUser in BLOCKED. BLOCKED means the work before it in the chain has not finished successfully; the problem is the first worker.'),
        ('work', 's3', 'Chi tiết của UploadPhotos: cần mạng không đo lưu lượng', 'UploadPhotos\' details: it needs an unmetered network',
         'Phần ràng buộc của UploadPhotos ghi NetworkType UNMETERED (thường là Wi-Fi). Máy đang dùng 4G nên ràng buộc không bao giờ thỏa; worker đứng ở ENQUEUED, chờ mãi. Việc đồng bộ lịch hẹn, vốn chỉ cần có mạng, bị kẹt sau nó.',
         'UploadPhotos\' constraints say NetworkType UNMETERED (usually Wi-Fi). The phone is on 4G, so the constraint is never met; the worker stays ENQUEUED, waiting forever. Booking sync, which only needs any network, is stuck behind it.'),
        ('work', 's4', 'Tách tải ảnh khỏi chuỗi: lịch hẹn đồng bộ ngay', 'Take the photo upload out of the chain: bookings sync right away',
         'SyncBookings và NotifyUser thành một chuỗi riêng với ràng buộc CONNECTED; UploadPhotos chạy độc lập khi có Wi-Fi. Trên 4G, hai worker đồng bộ xong ở SUCCEEDED; chỉ còn việc tải ảnh chờ Wi-Fi, đúng như thiết kế.',
         'SyncBookings and NotifyUser become their own chain with a CONNECTED constraint; UploadPhotos runs on its own when Wi-Fi is available. On 4G, the two sync workers finish in SUCCEEDED; only the photo upload waits for Wi-Fi, as designed.'),
    ]
    for case, k, tv, te, xv, xe in S:
        sid = case + '.' + k
        m('s.%s.title' % sid, tv, te); m('s.%s.explain' % sid, xv, xe); m('ev.' + sid, tv, te)
    for k, vi, en in [
        ('try', '''Mẹo đọc: với lỗi database, bảng là nội dung thật của bảng booking và dòng truy vấn ở trên là thứ đang chạy; với lỗi việc nền, mỗi ô là một worker kèm trạng thái của nó.''',
         '''Reading tip: for the database bug, the table is the real content of the booking table and the query line above is what is running; for the background bug, each box is a worker with its state.'''),
        ('db.s2', '''Database Inspector xem, truy vấn và sửa database của app khi app đang chạy, với SQLite và các thư viện dựng trên nó như Room; cần thiết bị API 26 trở lên. [[src:ad-db-inspector]]''',
         '''Database Inspector inspects, queries and modifies the app\'s databases while the app runs, for SQLite and libraries built on it such as Room; it needs a device with API 26 or higher. [[src:ad-db-inspector]]'''),
        ('db.s3', '''Với Room, mỗi hàm @Query của DAO có thể chạy thẳng trong Database Inspector; tham số có tên sẽ được hỏi giá trị. [[src:ad-db-inspector]]''',
         '''With Room, each DAO @Query function can be run straight in Database Inspector; named parameters are prompted for values. [[src:ad-db-inspector]]'''),
        ('db.s4', '''Nếu giao diện quan sát database bằng Flow hay LiveData, chỉnh sửa trong Database Inspector hiện ngay trên app đang chạy; nếu không, phải chờ lần đọc sau. [[src:ad-db-inspector]]''',
         '''If the UI observes the database with Flow or LiveData, edits in Database Inspector show up immediately in the running app; otherwise only on the next read. [[src:ad-db-inspector]]'''),
        ('work.s1', '''Việc nền không có màn hình để nhìn và thường không ném lỗi; câu hỏi đầu tiên luôn là "worker đang ở trạng thái nào", không phải "mã của worker sai ở đâu".''',
         '''Background work has no screen to look at and usually throws nothing; the first question is always "what state is the worker in", not "where is the worker\\'s code wrong".'''),
        ('work.s2', '''BLOCKED nghĩa là việc đang bị chặn vì các việc đi trước chưa hoàn thành thành công. ENQUEUED nghĩa là đã vào hàng, sẽ chạy khi ràng buộc thỏa và có tài nguyên. [[src:ad-workinfo-state]]''',
         '''BLOCKED means the work is blocked because its prerequisites have not finished successfully. ENQUEUED means it is queued and will run when its constraints are met and resources are available. [[src:ad-workinfo-state]]'''),
        ('work.s3', '''Khi có nhiều ràng buộc, việc chỉ chạy khi mọi ràng buộc đều thỏa; UNMETERED là mạng không đo lưu lượng, như Wi-Fi. [[src:ad-define-work]]''',
         '''With several constraints, work runs only when all of them are met; UNMETERED is a network without data metering, such as Wi-Fi. [[src:ad-define-work]]'''),
        ('work.s4', '''Background Task Inspector hiện chi tiết mỗi worker: ràng buộc, trạng thái, vị trí trong chuỗi, số lần thử lại; Graph View vẽ cả chuỗi. [[src:ad-task-inspector]]''',
         '''Background Task Inspector shows each worker\'s details: constraints, state, position in the chain, retry count; Graph View draws the whole chain. [[src:ad-task-inspector]]'''),
    ]:
        m('co.' + k, vi, en)

    z = lambda k, vi, en=None: a('vz.' + k, vi, en)
    z('tab.inspect', '''Bảng dữ liệu và chuỗi worker''', '''Data table and worker chain''')
    z('in.query', '''Truy vấn đang chạy: {q}''', '''Running query: {q}'''); z('in.noquery', '''(chỉ mở bảng, chưa truy vấn)''', '''(table opened, no query yet)''')
    z('in.table', '''Bảng booking ({n} dòng)''', '''The booking table ({n} rows)'''); z('in.result', '''Danh sách nhận {n} lịch: {ids}''', '''The list receives {n} bookings: {ids}''')
    for k, vi, en in [('id', 'id lịch', 'booking id'), ('patient', 'Bệnh nhân', 'Patient'), ('day', 'Ngày', 'Day'), ('status', 'status (trạng thái)', 'status')]:
        z('in.col.' + k, vi, en)
    z('in.net', '''Mạng của máy: {n}''', '''The phone\'s network: {n}'''); z('in.net.metered', '''4G (đo lưu lượng)''', '''4G (metered)''')
    z('in.need', '''cần: {c}''', '''needs: {c}''')
    z('in.chains', '''{n} worker chưa xong''', '''{n} workers not finished''')
    z('in.legend', '''Lỗi database: hàng có viền là kết quả truy vấn, ô đỏ là giá trị làm dòng bị loại. Lỗi việc nền: ô đỏ là worker kẹt, ô xanh là worker đã xong, mũi tên là thứ tự trong chuỗi.''',
      '''Database bug: outlined rows are the query result, a red cell is the value excluding a row. Background bug: a red box is a stuck worker, a green box a finished one, arrows give the chain order.''')

    C = 'l7'
    a(C + '.title', '''Dữ liệu và việc nền: Database Inspector, Background Task Inspector''', '''Data and background work: Database Inspector, Background Task Inspector''')
    a(C + '.essence', '''Có những lỗi không crash và không để lại log: dữ liệu "đã lưu" mà không hiện, việc nền "đang chạy" mà không bao giờ xong. Với chúng, hãy nhìn thẳng vào trạng thái của app đang chạy thay vì đoán từ mã.\nDatabase Inspector mở bảng của app đang chạy, chạy được chính truy vấn @Query của DAO, và cho sửa một dòng để thử giả thuyết; nếu giao diện quan sát bằng Flow, thay đổi hiện ngay.\nBackground Task Inspector cho thấy từng worker của WorkManager đang ở trạng thái nào (ENQUEUED, RUNNING, BLOCKED, SUCCEEDED, FAILED, CANCELLED), ràng buộc của nó và vị trí trong chuỗi. ENQUEUED mãi là ràng buộc chưa thỏa; BLOCKED là đang chờ việc phía trước.''',
      '''Some bugs neither crash nor leave a log: data "saved" but not shown, background work "running" but never finishing. For these, look straight at the running app\'s state instead of guessing from the code.\nDatabase Inspector opens the running app\'s tables, runs the DAO\'s own @Query, and lets you edit a row to test a hypothesis; if the UI observes through a Flow, the change shows at once.\nBackground Task Inspector shows which state each WorkManager worker is in (ENQUEUED, RUNNING, BLOCKED, SUCCEEDED, FAILED, CANCELLED), its constraints and its place in the chain. Forever ENQUEUED means a constraint is unmet; BLOCKED means waiting for the work in front.''')
    a(C + '.goal.g1', '''Đã thấy dữ liệu thật nằm trong bảng hay trạng thái thật của worker''', '''Saw the real data in the table or the workers\' real states''')
    a(C + '.goal.g2', '''Đã thấy nguyên nhân và bản sửa''', '''Saw the cause and the fix''')
    a(C + '.sim.debugging.inspect', '''lịch đã lưu mà không hiện, và đồng bộ kẹt mãi''', '''a saved booking not shown, and a sync stuck forever''')

    S_ = 'hook'
    a(C + '.sec.%s.title' % S_, '''Đoán trước khi đọc''', '''Predict before reading''')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'predict', '''Chuỗi đồng bộ gồm ba worker: tải ảnh (cần Wi-Fi), rồi đồng bộ lịch hẹn, rồi gửi thông báo. Máy dùng 4G cả ngày. Hai worker sau ở trạng thái nào?''',
      '''The sync chain has three workers: upload photos (needs Wi-Fi), then sync bookings, then notify the user. The phone is on 4G all day. What state are the last two workers in?''')
    B(C, S_, 1, 'ans', '''BLOCKED, cả ngày. Worker đầu đứng ở ENQUEUED vì ràng buộc Wi-Fi không thỏa, và hai worker sau chờ nó xong. Không crash, không log; chỉ nhìn vào trạng thái worker mới thấy. Mô phỏng ngay dưới có lỗi này và một lỗi database cùng kiểu "im lặng".''',
      '''BLOCKED, all day. The first worker sits in ENQUEUED because the Wi-Fi constraint is unmet, and the two behind it wait for it to finish. No crash, no log; only the workers\' states show it. The simulation just below has this bug and a database bug of the same "silent" kind.''')

    S_ = 'db'
    a(C + '.sec.%s.title' % S_, '''Database Inspector: bảng của app đang chạy''', '''Database Inspector: the running app\'s tables''')
    a(C + '.sec.%s.badge' % S_, 'version')
    B(C, S_, 1, 'p', '''Database Inspector xem, truy vấn và sửa database của app ngay khi app đang chạy, với SQLite có sẵn trong Android và các thư viện dựng trên nó như Room; cần thiết bị API 26 trở lên, và không dùng được với bản SQLite app tự mang theo. Có ba việc chính: mở bảng để xem dữ liệu thật, chạy truy vấn (kể cả @Query của DAO, hay câu SQL tự viết), và sửa giá trị trong bảng. [[src:ad-db-inspector]]''',
      '''Database Inspector inspects, queries and modifies the app\'s databases while the app runs, for Android\'s built-in SQLite and libraries built on it such as Room; it needs a device with API 26 or higher and does not work with a SQLite library bundled in the app. It does three main things: open tables to see the real data, run queries (including DAO @Query functions or hand-written SQL), and edit values in a table. [[src:ad-db-inspector]]''')
    B(C, S_, 2, 'p', '''Vài điều cần biết khi dùng. Bật cập nhật trực tiếp thì bảng tự làm mới nhưng chỉ đọc; tắt đi thì sửa được và làm mới bằng tay. Công cụ chỉ sửa được khi app còn giữ kết nối tới database, nên có tùy chọn giữ kết nối mở. Khi app ngắt, database được tải về để vẫn xem và truy vấn được, nhưng không sửa được. [[src:ad-db-inspector]]''',
      '''A few things to know when using it. With live updates on, the table refreshes itself but is read-only; turn them off to edit and refresh by hand. The tool can only modify a database while the app holds a connection to it, hence the option to keep connections open. When the app disconnects, the database is downloaded so you can still view and query it, but not modify it. [[src:ad-db-inspector]]''')

    S_ = 'probe'
    a(C + '.sec.%s.title' % S_, '''Dùng database để kiểm giả thuyết''', '''Using the database to test a hypothesis''')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'p', '''Lỗi "đã lưu mà không hiện" chia thành hai nửa: dữ liệu có vào bảng không, và truy vấn của màn có lấy ra không. Mở bảng trả lời nửa đầu; chạy đúng @Query của màn trả lời nửa sau. So hai kết quả là thấy cột nào làm dòng bị loại.''',
      '''A "saved but not shown" bug splits in two halves: did the data reach the table, and does the screen\'s query take it out. Opening the table answers the first half; running the screen\'s exact @Query answers the second. Comparing the two shows which column excludes the row.''')
    B(C, S_, 2, 'p', '''Sửa thử một giá trị trong bảng là một phép thử rẻ cho giả thuyết, đúng như vòng gỡ lỗi ở chương "Quy trình gỡ lỗi, adb và bug report": dự đoán "đổi status thành CONFIRMED thì danh sách hiện lịch", rồi kiểm. Nếu màn quan sát database bằng Flow, kết quả hiện ngay, không cần build lại. Cách Room và Flow phát lại dữ liệu khi bảng đổi được nói ở chương "Room cơ bản" của track Lưu dữ liệu. [[src:ad-db-inspector]]''',
      '''Editing a value in the table is a cheap test of a hypothesis, just like the debugging loop in "The debugging process, adb and bug reports": predict "changing status to CONFIRMED makes the list show the booking", then check. If the screen observes the database through a Flow, the result appears at once, with no rebuild. How Room and Flow re-emit data when a table changes is covered in "Room basics" in the Saving Data track. [[src:ad-db-inspector]]''')
    B(C, S_, 3, 'kt', '''@Query("SELECT * FROM booking WHERE status = 'CONFIRMED' ORDER BY day")
fun confirmed(): Flow<List<Booking>>            // danh sách cũ: bỏ sót lịch PENDING

@Query("SELECT * FROM booking WHERE status IN ('PENDING', 'CONFIRMED') ORDER BY day")
fun upcoming(): Flow<List<Booking>>             // sửa: lấy cả lịch chờ xác nhận''', '''@Query("SELECT * FROM booking WHERE status = 'CONFIRMED' ORDER BY day")
fun confirmed(): Flow<List<Booking>>            // old list: misses PENDING bookings

@Query("SELECT * FROM booking WHERE status IN ('PENDING', 'CONFIRMED') ORDER BY day")
fun upcoming(): Flow<List<Booking>>             // fix: includes bookings awaiting confirmation''')

    S_ = 'work'
    a(C + '.sec.%s.title' % S_, '''Trạng thái của một worker''', '''A worker\'s states''')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'p', '''Mỗi việc của WorkManager có một trạng thái. ENQUEUED: đã vào hàng, sẽ chạy khi ràng buộc thỏa và có tài nguyên. RUNNING: đang chạy. SUCCEEDED: xong thành công (việc định kỳ không bao giờ ở đây, nó quay về ENQUEUED). FAILED: xong mà thất bại, và mọi việc phụ thuộc cũng thành FAILED, không bao giờ chạy. BLOCKED: bị chặn vì việc đi trước chưa xong thành công. CANCELLED: bị hủy, việc phụ thuộc cũng bị hủy. Chỉ SUCCEEDED, FAILED, CANCELLED được tính là đã xong. [[src:ad-workinfo-state]]''',
      '''Every WorkManager job has a state. ENQUEUED: queued, will run when constraints are met and resources are available. RUNNING: running. SUCCEEDED: finished successfully (periodic work never gets here; it goes back to ENQUEUED). FAILED: finished with a failure, and all dependent work also becomes FAILED and never runs. BLOCKED: blocked because work before it has not finished successfully. CANCELLED: cancelled, and dependent work is cancelled too. Only SUCCEEDED, FAILED and CANCELLED count as finished. [[src:ad-workinfo-state]]''')
    B(C, S_, 2, 'p', '''Đọc trạng thái như một manh mối. ENQUEUED rất lâu: một ràng buộc không thỏa (mạng, sạc, pin, bộ nhớ, máy rảnh); khi có nhiều ràng buộc, mọi ràng buộc đều phải thỏa. BLOCKED: nhìn lên việc phía trước trong chuỗi. FAILED lan xuống cả chuỗi: tìm worker thất bại đầu tiên. Worker trả Result.retry() thì được chạy lại sau một khoảng backoff, mặc định tăng theo cấp số nhân từ 30 giây. [[src:ad-define-work]]''',
      '''Read the state as a clue. ENQUEUED for a long time: a constraint is unmet (network, charging, battery, storage, idle); with several constraints, all must be met. BLOCKED: look up the chain at the work in front. FAILED spreading down a chain: find the first worker that failed. A worker returning Result.retry() runs again after a backoff delay, exponential from 30 seconds by default. [[src:ad-define-work]]''')
    B(C, S_, 3, 'kt', '''// SAI: đồng bộ lịch hẹn bị xếp sau việc cần Wi-Fi
workManager.beginWith(uploadPhotos /* UNMETERED */).then(syncBookings).then(notifyUser).enqueue()

// SỬA: hai chuỗi độc lập, mỗi chuỗi đúng ràng buộc của nó
workManager.beginWith(syncBookings /* CONNECTED */).then(notifyUser).enqueue()
workManager.enqueue(uploadPhotos /* UNMETERED */)''', '''// WRONG: booking sync queued behind work that needs Wi-Fi
workManager.beginWith(uploadPhotos /* UNMETERED */).then(syncBookings).then(notifyUser).enqueue()

// FIX: two independent chains, each with its own constraint
workManager.beginWith(syncBookings /* CONNECTED */).then(notifyUser).enqueue()
workManager.enqueue(uploadPhotos /* UNMETERED */)''')

    S_ = 'task'
    a(C + '.sec.%s.title' % S_, '''Background Task Inspector: xem các worker''', '''Background Task Inspector: looking at workers''')
    a(C + '.sec.%s.badge' % S_, 'version')
    B(C, S_, 1, 'p', '''Background Task Inspector hiện các worker của app (WorkManager 2.5.0 trở lên, thiết bị API 26 trở lên): tên lớp, trạng thái, giờ bắt đầu, số lần thử lại. Chọn một worker để xem chi tiết: tag và id, ràng buộc, tần suất, trạng thái, vị trí trong chuỗi, dữ liệu đầu ra. Chế độ đồ thị vẽ cả chuỗi worker; cũng có thể hủy một worker đang chờ hay đang chạy để thử. Job, alarm và wakelock cũng được liệt kê ở đây (phần này trước kia thuộc Energy Profiler). Cách thiết kế đồng bộ nền được nói ở chương "Offline-first và đồng bộ nền" của track Lưu dữ liệu. [[src:ad-task-inspector]]''',
      '''Background Task Inspector shows the app\'s workers (WorkManager 2.5.0 or higher, a device with API 26 or higher): class name, state, start time, retry count. Select a worker for details: tag and id, constraints, frequency, state, position in the chain, output data. A graph view draws the whole worker chain; you can also cancel a waiting or running worker to experiment. Jobs, alarms and wakelocks are listed here too (this part used to belong to the Energy Profiler). Designing background sync is covered in "Offline-first and background sync" in the Saving Data track. [[src:ad-task-inspector]]''')

    S_ = 'bugs'
    a(C + '.sec.%s.title' % S_, '''Hai lỗi hay gặp''', '''Two common bugs''')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'bug', '''Sửa giá trị trong Database Inspector mà màn hình không đổi.''', '''Editing a value in Database Inspector does not change the screen.''')
    B(C, S_, 1, 'cause', '''Màn đọc database một lần lúc mở, không quan sát bằng Flow hay LiveData, nên chỉ thấy thay đổi ở lần đọc sau.''', '''The screen reads the database once when it opens, without observing through Flow or LiveData, so it only sees the change on the next read.''')
    B(C, S_, 1, 'fix', '''Cho DAO trả Flow và để màn quan sát nó; khi đó mọi thay đổi trong bảng đều hiện ngay.''', '''Have the DAO return a Flow and let the screen observe it; then every change in the table shows at once.''')
    B(C, S_, 2, 'bug', '''Một worker thất bại một lần, rồi cả chuỗi phía sau không bao giờ chạy, kể cả khi mạng đã ổn.''', '''A worker fails once, and the whole chain behind it never runs, even after the network recovers.''')
    B(C, S_, 2, 'cause', '''Worker trả Result.failure() cho một lỗi mạng tạm thời; FAILED lan xuống mọi việc phụ thuộc.''', '''The worker returns Result.failure() for a temporary network error; FAILED spreads to all dependent work.''')
    B(C, S_, 2, 'fix', '''Lỗi tạm thời thì trả Result.retry() để được chạy lại theo backoff; chỉ trả failure cho lỗi không thể khắc phục.''', '''For temporary errors return Result.retry() to run again with backoff; return failure only for errors that cannot be recovered.''')

    S_ = 'ex'
    a(C + '.sec.%s.title' % S_, '''Bài tập''', '''Exercise''')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'ex', '''Background Task Inspector cho thấy chuỗi: CompressLogs ở FAILED, UploadLogs ở FAILED, CleanUp ở FAILED. Worker nào cần đọc trước, và vì sao hai worker sau cũng FAILED dù chưa từng chạy?''',
      '''Background Task Inspector shows a chain: CompressLogs FAILED, UploadLogs FAILED, CleanUp FAILED. Which worker should you read first, and why are the last two FAILED though they never ran?''')
    B(C, S_, 1, 'hint', '''FAILED lan sang mọi việc phụ thuộc.''', '''FAILED spreads to all dependent work.''')
    B(C, S_, 1, 'sol', '''Đọc CompressLogs trước: nó là worker đầu chuỗi và là cái thật sự thất bại. Khi một việc FAILED, mọi việc phụ thuộc cũng được đánh FAILED và không bao giờ chạy, nên UploadLogs và CleanUp chỉ là hệ quả. Xem dữ liệu đầu ra và số lần thử lại của CompressLogs, rồi xét nó nên trả retry hay failure.''',
      '''Read CompressLogs first: it is the head of the chain and the one that really failed. When work FAILS, all dependent work is marked FAILED too and never runs, so UploadLogs and CleanUp are only consequences. Check CompressLogs\' output data and retry count, then decide whether it should return retry or failure.''')

    S_ = 'recall'
    a(C + '.sec.%s.title' % S_, '''Tự trả lời''', '''Answer it yourself''')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'ask', '''Lỗi "đã lưu mà không hiện" chia thành hai câu hỏi nào?''', '''What two questions does a "saved but not shown" bug split into?''')
    B(C, S_, 1, 'ans', '''Dữ liệu có vào bảng không (mở bảng), và truy vấn của màn có lấy ra không (chạy đúng @Query của màn).''', '''Did the data reach the table (open the table), and does the screen\'s query take it out (run the screen\'s exact @Query).''')
    B(C, S_, 2, 'ask', '''Worker ở ENQUEUED và ở BLOCKED khác nhau thế nào?''', '''How do a worker in ENQUEUED and one in BLOCKED differ?''')
    B(C, S_, 2, 'ans', '''ENQUEUED chờ ràng buộc của chính nó thỏa; BLOCKED chờ việc phía trước trong chuỗi xong thành công.''', '''ENQUEUED waits for its own constraints to be met; BLOCKED waits for the work in front of it in the chain to succeed.''')

    for q, qv, qe, av, ae, wv, we in [
        ('q1', 'Database Inspector cần thiết bị API bao nhiêu?', 'What device API level does Database Inspector need?', 'API 26 trở lên.', 'API 26 or higher.',
         'Và chỉ với SQLite có sẵn trong Android, không phải bản app tự mang theo.', 'And only with Android\'s built-in SQLite, not one bundled in the app.'),
        ('q2', 'Trạng thái nào được tính là đã xong?', 'Which states count as finished?', 'Ba trạng thái: SUCCEEDED, FAILED, CANCELLED.', 'Three states: SUCCEEDED, FAILED, CANCELLED.',
         'ENQUEUED, RUNNING, BLOCKED đều chưa xong.', 'ENQUEUED, RUNNING and BLOCKED are not finished.'),
        ('q3', 'Một worker FAILED thì việc phụ thuộc ra sao?', 'What happens to dependent work when a worker FAILS?', 'Cũng thành FAILED và không bao giờ chạy.', 'It also becomes FAILED and never runs.',
         'Vì vậy lỗi tạm thời nên trả Result.retry().', 'That is why temporary errors should return Result.retry().')]:
        a(C + '.quiz.%s.q' % q, qv, qe); a(C + '.quiz.%s.a' % q, av, ae); a(C + '.quiz.%s.why' % q, wv, we)
