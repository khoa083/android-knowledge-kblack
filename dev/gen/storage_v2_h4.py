# Lưu dữ liệu · H4: Room cơ bản (Phần 1)
# Nguồn: developer.android.com Room, Async queries, Accessing data (đọc 2026-11-24; hướng dẫn dùng Room 3.0, gói androidx.room3).
# Trần: 8 mục, mục cơ chế ≤ 4 khối.

SEC_ORDER = {'h4': ['hook', 'parts', 'threads', 'observe', 'bugs', 'ex', 'recall']}


def add(a):
    def B(ch, sec, n, field, vi, en=None):
        a('%s.sec.%s.b.%02d.%s' % (ch, sec, n, field), vi, vi if en is None else en)

    a('preset.room', 'Lưu dữ liệu · Room: truy vấn một lần so với Flow', 'Saving data · Room: one-shot query versus Flow')
    m = lambda k, vi, en=None: a('m.room.' + k, vi, en)
    m('title', 'Màn hình có tự cập nhật khi database đổi không?', 'Does the screen update itself when the database changes?')
    m('overview', 'Màn Lịch của bác sĩ A đọc danh sách lịch hẹn từ Room (thư viện database của Android). Có hai cách đọc. Cách một: một hàm suspend trả về danh sách, đọc đúng một lần. Cách hai: một hàm trả về Flow, tức một luồng dữ liệu cứ có thay đổi là phát giá trị mới. Sau đó có ba lần ghi: thêm một lịch cho bác sĩ A, sửa một lịch của bác sĩ B, và thêm một ghi chú vào một bảng khác.',
      "Doctor A's schedule screen reads appointments from Room (Android's database library). There are two ways to read. One: a suspend function returning a list, read exactly once. Two: a function returning a Flow, a stream that emits a new value whenever something changes. Then come three writes: a new appointment for doctor A, an edit to one of doctor B's, and a new note in a different table.")
    m('wrapup', 'Truy vấn một lần trả về một ảnh chụp tại lúc gọi. Database đổi sau đó thì màn hình không hề biết. Truy vấn trả về Flow thì Room tự chạy lại mỗi khi một bảng nó đọc bị ghi, nên màn hình tự cập nhật.\nRoom theo dõi theo bảng, không theo từng dòng. Sửa một dòng không nằm trong kết quả vẫn làm truy vấn chạy lại; thêm distinctUntilChanged nếu chỉ muốn nghe thay đổi thật.\nHình dung: truy vấn một lần là chụp ảnh bảng tin; Flow là đứng cạnh bảng tin, ai dán gì mới là bạn thấy ngay.',
      'A one-shot query returns a snapshot taken at the moment of the call. Later changes to the database never reach the screen. A query returning a Flow is rerun by Room whenever a table it reads is written, so the screen updates itself.\nRoom tracks tables, not individual rows. Editing a row outside the result still reruns the query; add distinctUntilChanged if you only want real changes.\nPicture it: a one-shot query is a photo of the notice board; a Flow is standing next to the board and seeing every new notice as it goes up.')
    m('simp.1', 'Bốn tầng (DAO, mã sinh, SQLite, kết quả) là hình rút gọn; mã Room sinh còn lo chuyển đổi kiểu, giao dịch và theo dõi bảng. Số lịch là của ví dụ.', 'The four stages (DAO, generated code, SQLite, result) are simplified; Room\'s generated code also handles type conversion, transactions and table tracking. The appointment counts belong to the example.')
    m('simp.2', 'Hành vi chạy lại theo bảng theo tài liệu Android (đọc ngày 2026-11-24, khi hướng dẫn dùng Room 3.0); site không chạy SQLite thật. Chi tiết của Room 2.x là hành vi bản cũ. Chương chưa bàn TypeConverter, index, Paging, RxJava hay LiveData; quan hệ và giao dịch ở chương H5, migration ở chương H6.',
      'Table-based reruns follow the Android docs (read on 2026-11-24, when the guide used Room 3.0); the site does not run a real SQLite. Room 2.x details describe the older version. The chapter does not cover TypeConverters, indices, Paging, RxJava or LiveData; relations and transactions are chapter H5, migrations chapter H6.')
    m('ctl.hint', 'Đổi cách đọc rồi đi lại; so cột "Màn hình nhận" ở hai cách.', 'Switch the read and walk again; compare the "Screen gets" column for both.')
    m('ctl.case', 'Cách đọc', 'Read')
    for k, vi, en in [('flow', 'Flow (quan sát)', 'Flow (observable)'), ('oneshot', 'suspend (một lần)', 'suspend (one-shot)')]:
        m('ctl.case.' + k, vi, en)
    m('diagramTitle', 'DAO, mã Room sinh, SQLite, kết quả', 'DAO, Room-generated code, SQLite, result')
    m('diagramDesc', 'Lời gọi đi từ interface DAO qua mã Room sinh lúc build xuống SQLite; kết quả đi ngược về màn hình', 'A call goes from the DAO interface through code Room generated at build time down to SQLite; the result comes back to the screen')
    for k, vi, en in [('dao', 'DAO (interface bạn viết)', 'DAO (the interface you write)'), ('impl', 'Mã Room sinh lúc build', 'Code Room generates at build time'), ('sqlite', 'SQLite (bảng appointment)', 'SQLite (appointment table)'), ('out', 'Màn hình', 'Screen')]:
        m('n.' + k, vi, en)
    m('met.shown', 'Số lịch trên màn hình', 'Appointments on screen'); m('met.runs', 'Số lần truy vấn đã chạy', 'Times the query has run')
    a('cap.room', 'Từ trái sang phải: DAO, mã Room sinh, SQLite, màn hình. Khi chỉ SQLite sáng, có ghi xuống database nhưng màn hình không được báo.', 'Left to right: DAO, Room-generated code, SQLite, screen. When only SQLite is lit, the database was written but the screen was not told.')
    S = [
        ('flow', 's1', 'Mở màn hình: thu Flow, truy vấn chạy lần đầu', 'Open the screen: collect the Flow, the query runs once',
         'Màn hình thu dao.byDoctor(A). Room chạy câu SELECT, phát danh sách 3 lịch, và ghi nhớ rằng truy vấn này đọc bảng appointment.', 'The screen collects dao.byDoctor(A). Room runs the SELECT, emits a list of 3, and remembers that this query reads the appointment table.'),
        ('flow', 's2', 'Thêm lịch cho bác sĩ A: Flow phát 4 lịch', 'Add an appointment for doctor A: the Flow emits 4',
         'Lần insert ghi vào bảng appointment. Room thấy bảng này đổi, chạy lại truy vấn và phát danh sách mới. Màn hình không phải làm gì.', 'The insert writes to the appointment table. Room sees the table change, reruns the query and emits the new list. The screen does nothing.'),
        ('flow', 's3', 'Sửa lịch của bác sĩ B: chạy lại, kết quả y nguyên', 'Edit doctor B\'s appointment: rerun, same result',
         'Dòng bị sửa không thuộc bác sĩ A, nhưng vẫn ở bảng appointment. Room theo dõi theo bảng, nên vẫn chạy lại và phát một danh sách giống hệt lần trước.', 'The edited row is not doctor A\'s, but it is in the appointment table. Room tracks tables, so it reruns anyway and emits a list identical to the last one.'),
        ('flow', 's4', 'Thêm ghi chú vào bảng note: không chạy lại', 'Add a row to the note table: no rerun',
         'Truy vấn không đọc bảng note, nên ghi vào đó không đánh thức nó. Truy vấn đã chạy 3 lần cho 3 lần ghi: một lần đầu, hai lần cho bảng appointment.', 'The query does not read the note table, so writing there does not wake it. It has run 3 times for 3 writes: once at the start, twice for the appointment table.'),
        ('oneshot', 's1', 'Mở màn hình: gọi hàm suspend, nhận 3 lịch', 'Open the screen: call the suspend function, get 3',
         'byDoctorOnce chạy câu SELECT một lần trên luồng nền và trả về một List. Đó là ảnh chụp tại lúc gọi.', 'byDoctorOnce runs the SELECT once on a background thread and returns a List. It is a snapshot taken at call time.'),
        ('oneshot', 's2', 'Thêm lịch cho bác sĩ A: màn hình vẫn 3', 'Add an appointment for doctor A: the screen still shows 3',
         'Database đã có 4 lịch, nhưng không ai đọc lại. Người dùng vừa đặt lịch xong và không thấy nó trong danh sách.', 'The database now has 4, but nobody reads again. The user has just booked and does not see the booking in the list.'),
        ('oneshot', 's3', 'Sửa lịch của bác sĩ B: không có gì xảy ra', 'Edit doctor B\'s appointment: nothing happens',
         'Không có truy vấn nào đang quan sát, nên cũng không có lần chạy lại thừa nào. Nhưng cũng không có cập nhật nào.', 'No query is observing, so there is no wasted rerun. There is no update either.'),
        ('oneshot', 's4', 'Thêm ghi chú: màn hình vẫn cũ tới khi tự tải lại', 'Add a note: the screen stays stale until you reload by hand',
         'Muốn màn hình đúng, mã phải tự gọi lại byDoctorOnce sau mỗi lần ghi, ở mọi nơi có ghi. Dễ sót một chỗ; Flow làm việc đó thay bạn.', 'To keep the screen right, the code must call byDoctorOnce again after every write, wherever writes happen. Easy to miss one; the Flow does it for you.'),
    ]
    for case, k, tv, te, xv, xe in S:
        sid = case + '.' + k
        m('s.%s.title' % sid, tv, te); m('s.%s.explain' % sid, xv, xe); m('ev.' + sid, tv, te)
    for k, vi, en in [
        ('try', 'Đi hết bốn bước của mỗi cách; để ý số lần truy vấn đã chạy.', 'Walk all four steps of each read; watch how many times the query has run.'),
        ('flow.s2', 'Tài liệu Android nói: truy vấn quan sát đọc lại mỗi khi bảng bên dưới đổi và phát giá trị mới. [[src:ax-room-async]]', 'The Android docs say: an observable query re-reads whenever the underlying tables change and emits the new value. [[src:ax-room-async]]'),
        ('flow.s3', 'Tài liệu đó cũng nói: truy vấn chạy lại khi bất kỳ dòng nào của bảng được cập nhật, dù dòng đó có nằm trong kết quả hay không; dùng distinctUntilChanged để UI chỉ được báo khi kết quả thật sự đổi. [[src:ax-room-async]]', 'The same docs say: the query reruns whenever any row in the table is updated, whether or not that row is in the result; use distinctUntilChanged so the UI is only notified when the results actually change. [[src:ax-room-async]]'),
        ('flow.s4', 'Tài liệu Android nói: Room theo dõi những bảng mà câu truy vấn tham chiếu; bảng khác đổi thì truy vấn không chạy lại. [[src:ax-room-async]]', 'The Android docs say: Room tracks the tables a query references; changes to other tables do not rerun it. [[src:ax-room-async]]'),
        ('oneshot.s2', 'Tài liệu Android nói: truy vấn đọc một lần trả dữ liệu tại thời điểm gọi, không theo dõi thay đổi sau đó. [[src:ax-room-async]]', 'The Android docs say: a one-shot read returns the data as of the call, without tracking later changes. [[src:ax-room-async]]'),
        ('oneshot.s3', 'Đọc một lần hợp với dữ liệu chỉ cần lúc đó, như kiểm một lịch có trùng giờ không trước khi lưu.', 'A one-shot read suits data you need only at that moment, such as checking whether a slot clashes before saving.'),
        ('oneshot.s4', 'Gọi lại thủ công sau mỗi lần ghi là cách dễ sót. Màn hình hiển thị danh sách nên quan sát bằng Flow.', 'Calling again by hand after every write is easy to forget. A screen showing a list should observe it with a Flow.')]:
        m('co.' + k, vi, en)

    z = lambda k, vi, en=None: a('vz.' + k, vi, en)
    z('tab.rm', 'Bảng chạy lại', 'Rerun table')
    z('rm.cap', 'Dãy trên: tầng nào làm việc ở bước này. Bảng dưới: mỗi lần ghi vào bảng nào, truy vấn của màn hình có chạy lại không, và màn hình nhận được gì.', 'Top row: which stage works at this step. Table below: which table each write touched, whether the screen\'s query reran, and what the screen received.')
    z('rm.legend', 'Room theo dõi theo bảng: ghi vào bảng mà truy vấn đọc thì truy vấn chạy lại, dù kết quả có đổi hay không. Ô gạch đỏ: màn hình cũ, hay nhận một bản giống hệt.', 'Room tracks by table: writing to a table a query reads reruns the query, whether or not the result changes. Red hatched: a stale screen, or an identical copy delivered.')
    for k, vi, en in [('impl', 'mã sinh (_Impl)', 'generated (_Impl)'), ('sqlite', 'SQLite', 'SQLite'), ('out.flow', 'Flow → màn hình', 'Flow → screen'), ('out.oneshot', 'List → màn hình', 'List → screen')]:
        z('rm.stage.' + k, vi, en)
    z('rm.stage.dao', 'DAO (bạn viết)', 'DAO (yours)')
    for k, vi, en in [('write', 'Lần ghi', 'Write'), ('table', 'Bảng', 'Table'), ('rerun', 'Chạy lại?', 'Rerun?'), ('changed', 'Kết quả đổi?', 'Result changed?'), ('screen', 'Màn hình nhận', 'Screen gets')]:
        z('rm.col.' + k, vi, en)
    for k, vi, en in [('ins', 'thêm lịch bác sĩ A', 'add doctor A appointment'), ('updB', 'sửa lịch bác sĩ B', 'edit doctor B appointment'), ('note', 'thêm ghi chú', 'add a note')]:
        z('rm.w.' + k, vi, en)
    for k, vi, en in [('yes', 'có', 'yes'), ('no', 'không', 'no')]:
        z('rm.yn.' + k, vi, en)
    for k, vi, en in [('emit', '4 lịch mới', 'the new 4'), ('emitSame', 'bản giống hệt (thừa)', 'an identical copy (wasted)'), ('none', 'không gì', 'nothing'), ('stale', 'vẫn 3: cũ', 'still 3: stale')]:
        z('rm.scr.' + k, vi, en)

    C = 'h4'
    a(C + '.title', 'Room cơ bản', 'Room basics')
    a(C + '.essence', 'Room có ba phần. Entity là một bảng. DAO (Data Access Object) chứa các hàm đọc ghi. Lớp database gom chúng lại. Room sinh mã lúc build và kiểm câu SQL ngay lúc biên dịch.\nRoom không cho truy cập database trên main thread. Truy vấn một lần là hàm suspend; truy vấn quan sát trả về Flow.\nFlow chạy lại mỗi khi một bảng nó đọc bị ghi, kể cả khi kết quả không đổi. Thêm distinctUntilChanged để chỉ nghe thay đổi thật.',
      'Room has three parts. An entity is a table. A DAO (Data Access Object) holds the read and write functions. The database class ties them together. Room generates code at build time and checks SQL right at compile time.\nRoom does not allow database access on the main thread. One-shot queries are suspend functions; observable queries return a Flow.\nA Flow reruns whenever a table it reads is written, even if the result is unchanged. Add distinctUntilChanged to hear only real changes.')
    a(C + '.goal.g1', 'Đã thấy lần ghi đầu tiên', 'Saw the first write')
    a(C + '.goal.g2', 'Đã đi hết ba lần ghi', 'Walked through all three writes')
    a(C + '.sim.storage.room', 'truy vấn một lần và Flow qua ba lần ghi', 'one-shot query and Flow across three writes')

    S_ = 'hook'
    a(C + '.sec.%s.title' % S_, 'Đoán trước khi đọc', 'Predict before reading')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'predict', 'Màn Lịch của bác sĩ A thu một Flow từ Room: SELECT … WHERE doctorId = A. Một màn khác đổi trạng thái một lịch của bác sĩ B. Flow của bác sĩ A có phát lại không?',
      'Doctor A\'s schedule screen collects a Flow from Room: SELECT … WHERE doctorId = A. Another screen changes the status of one of doctor B\'s appointments. Does doctor A\'s Flow emit again?')
    B(C, S_, 1, 'ans', 'Có. Room theo dõi theo bảng, không theo từng dòng. Mọi lần ghi vào bảng appointment đều làm truy vấn chạy lại, và Flow phát một danh sách giống hệt lần trước. Mô phỏng ngay dưới đếm từng lần chạy. [[src:ax-room-async]]',
      'Yes. Room tracks tables, not individual rows. Any write to the appointment table reruns the query, and the Flow emits a list identical to the last one. The simulation just below counts every run. [[src:ax-room-async]]')

    S_ = 'parts'
    a(C + '.sec.%s.title' % S_, 'Ba phần của Room', 'Room\'s three parts')
    a(C + '.sec.%s.badge' % S_, 'version')
    B(C, S_, 1, 'p', 'Room là thư viện Jetpack đặt bên trên SQLite (database có sẵn trong Android). Nó có ba phần.\nEntity: một lớp gắn @Entity; mỗi lớp là một bảng, mỗi object là một dòng.\nDAO: một interface gắn @Dao, khai báo các hàm truy vấn, chèn, sửa, xóa.\nDatabase: một abstract class kế thừa RoomDatabase, gắn @Database kèm danh sách entity, và có một hàm trả về mỗi DAO.\nBạn chỉ viết khai báo; Room sinh phần cài đặt lúc build.\nHình dung: entity là mẫu phiếu, DAO là người thủ thư biết tìm phiếu, database là cả thư viện. [[src:ax-room]] [[src:ax-room-dao]]',
      'Room is a Jetpack library sitting on top of SQLite (the database built into Android). It has three parts.\nEntity: a class annotated @Entity; each class is a table, each object a row.\nDAO: an interface annotated @Dao that declares query, insert, update and delete functions.\nDatabase: an abstract class extending RoomDatabase, annotated @Database with its list of entities, with one function returning each DAO.\nYou write only the declarations; Room generates the implementation at build time.\nPicture it: an entity is a form template, a DAO is the librarian who knows how to find forms, and the database is the whole library. [[src:ax-room]] [[src:ax-room-dao]]')
    B(C, S_, 2, 'kt', '@Entity\ndata class Appointment(\n    @PrimaryKey(autoGenerate = true) val id: Long = 0,\n    val doctorId: Long,\n    val time: Long,          // epoch millis; kiểu khác cần TypeConverter\n    val status: String,\n)\n\n@Dao interface AppointmentDao {\n    @Insert suspend fun insert(a: Appointment): Long          // trả về rowId mới\n    @Query("SELECT * FROM appointment WHERE doctorId = :doctorId ORDER BY time")\n    fun byDoctor(doctorId: Long): Flow<List<Appointment>>\n}\n\n@Database(entities = [Appointment::class], version = 1)\nabstract class AppDatabase : RoomDatabase() { abstract fun appointments(): AppointmentDao }',
      '@Entity\ndata class Appointment(\n    @PrimaryKey(autoGenerate = true) val id: Long = 0,\n    val doctorId: Long,\n    val time: Long,          // epoch millis; other types need a TypeConverter\n    val status: String,\n)\n\n@Dao interface AppointmentDao {\n    @Insert suspend fun insert(a: Appointment): Long          // returns the new rowId\n    @Query("SELECT * FROM appointment WHERE doctorId = :doctorId ORDER BY time")\n    fun byDoctor(doctorId: Long): Flow<List<Appointment>>\n}\n\n@Database(entities = [Appointment::class], version = 1)\nabstract class AppDatabase : RoomDatabase() { abstract fun appointments(): AppointmentDao }')
    B(C, S_, 3, 'p', 'Lợi ích lớn nhất so với dùng SQLite trực tiếp: câu SQL trong @Query được kiểm ngay lúc biên dịch. Gõ sai tên cột hay tên bảng là lỗi build, không phải crash lúc người dùng mở màn hình.\n@Insert trả về rowId (mã của dòng mới). @Update và @Delete tìm dòng theo khóa chính và có thể trả số dòng bị ảnh hưởng. @Upsert chèn nếu chưa có, cập nhật nếu đã có.\nQuy tắc dễ nhớ: lỗi SQL nên hiện ra trên máy của bạn, không phải trên máy của người dùng. [[src:ax-room-dao]]',
      "The biggest gain over using SQLite directly: the SQL in @Query is checked right at compile time. A misspelled column or table name is a build error, not a crash when the user opens the screen.\n@Insert returns the rowId (the new row's id). @Update and @Delete find rows by primary key and can return the number of rows affected. @Upsert inserts when missing and updates when present.\nRule of thumb: SQL mistakes should show up on your machine, not on the user's phone. [[src:ax-room-dao]]")
    B(C, S_, 4, 'note', 'Về phiên bản: hướng dẫn chính thức đọc ngày 2026-11-24 dùng Room 3.0, gói androidx.room3. Bản này cần KSP (công cụ sinh mã lúc build) và đặt driver bằng setDriver(AndroidSQLiteDriver()). App đang có thường còn dùng Room 2.x (gói androidx.room). Các annotation trong chương (@Entity, @Dao, @Query, @Insert) dùng giống nhau ở cả hai bản.\nMỗi tiến trình chỉ nên giữ một instance AppDatabase, vì tạo nó tốn kém. [[src:ax-room]]',
      'On versions: the official guide as read on 2026-11-24 uses Room 3.0, package androidx.room3. It needs KSP (a build-time code generation tool) and sets the driver with setDriver(AndroidSQLiteDriver()). Existing apps often still use Room 2.x (package androidx.room). The annotations in this chapter (@Entity, @Dao, @Query, @Insert) work the same way in both.\nKeep a single AppDatabase instance per process, because creating one is expensive. [[src:ax-room]]')
    B(C, S_, 4, 'kind', 'android')

    S_ = 'threads'
    a(C + '.sec.%s.title' % S_, 'Không truy vấn trên main thread', 'No queries on the main thread')
    a(C + '.sec.%s.badge' % S_, 'version')
    B(C, S_, 1, 'p', 'Đọc database có thể mất thời gian. Nếu làm trên main thread, giao diện sẽ đứng. Vì vậy Room không cho truy cập database trên main thread.\nTài liệu Android chia truy vấn thành ba loại. Ghi một lần: chèn, sửa, xóa. Đọc một lần: lấy dữ liệu đúng lúc gọi. Đọc quan sát: đọc lại mỗi khi bảng bên dưới đổi. Với Kotlin, loại "một lần" dùng hàm suspend, loại "quan sát" dùng Flow. Room đã có sẵn hỗ trợ coroutine và Flow, không cần thêm thư viện. [[src:ax-room-async]]',
      'Reading a database can take time. Done on the main thread, the UI freezes. So Room does not allow database access on the main thread.\nThe Android docs sort queries into three kinds. One-shot writes: insert, update, delete. One-shot reads: get the data as of the call. Observable reads: read again whenever the underlying tables change. In Kotlin, "one-shot" uses suspend functions and "observable" uses Flow. Room already supports coroutines and Flow; no extra library needed. [[src:ax-room-async]]')
    B(C, S_, 2, 'p', 'Room 3.0 bắt buộc từ khóa suspend cho truy vấn một lần, nên không còn cách nào viết ra lỗi gọi trên main thread. Ở Room 2.x thì khác: một hàm DAO thường (không suspend, không Flow) gọi trên main thread sẽ ném IllegalStateException lúc chạy. Ngoại lệ duy nhất là khi bật allowMainThreadQueries(), một tùy chọn chỉ nên dùng trong test.\nQuy tắc dễ nhớ: hàm DAO nào cũng phải là suspend hoặc trả về Flow. [[src:ax-room-async]]',
      'Room 3.0 requires the suspend keyword for one-shot queries, so the main-thread mistake can no longer be written at all. Room 2.x is different: a plain DAO function (not suspend, not Flow) called on the main thread throws IllegalStateException at runtime. The only exception is when allowMainThreadQueries() is enabled, an option meant only for tests.\nRule of thumb: every DAO function is either suspend or returns a Flow. [[src:ax-room-async]]')
    B(C, S_, 3, 'note', 'Hàm suspend của Room tự chuyển sang luồng nền của Room, nên không cần bọc trong withContext(Dispatchers.IO). Vì sao hàm suspend không chặn luồng, và cách chọn dispatcher (nơi coroutine chạy), có ở track Kotlin Coroutines Explorer.',
      "Room's suspend functions move to Room's own background threads, so there is no need to wrap them in withContext(Dispatchers.IO). Why suspend functions do not block a thread, and how to choose a dispatcher (where a coroutine runs), are covered in the Kotlin Coroutines Explorer track.")
    B(C, S_, 3, 'kind', 'mechanism')

    S_ = 'observe'
    a(C + '.sec.%s.title' % S_, 'Flow chạy lại theo bảng, không theo dòng', 'Flows rerun by table, not by row')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'p', 'Khi một hàm DAO trả về Flow, Room ghi nhớ câu truy vấn đó đọc những bảng nào. Mỗi lần có ghi vào một trong các bảng đó, Room chạy lại câu truy vấn và phát kết quả mới.\nĐiều dễ bất ngờ: tài liệu Android nói truy vấn chạy lại khi bất kỳ dòng nào của bảng được cập nhật, dù dòng đó có nằm trong kết quả hay không. Room không biết dòng nào thuộc kết quả của bạn; nó chỉ biết bảng nào vừa đổi. [[src:ax-room-async]]',
      'When a DAO function returns a Flow, Room remembers which tables that query reads. Whenever one of those tables is written, Room reruns the query and emits the new result.\nThe surprising part: the Android docs say the query reruns whenever any row in the table is updated, whether or not that row is in the result. Room does not know which rows belong to your result; it only knows which table just changed. [[src:ax-room-async]]')
    B(C, S_, 2, 'kt', 'val schedule: StateFlow<List<Appointment>> = dao.byDoctor(doctorId)\n    .distinctUntilChanged()                    // bỏ các bản giống hệt\n    .stateIn(viewModelScope, SharingStarted.WhileSubscribed(5_000), emptyList())',
      'val schedule: StateFlow<List<Appointment>> = dao.byDoctor(doctorId)\n    .distinctUntilChanged()                    // drops identical copies\n    .stateIn(viewModelScope, SharingStarted.WhileSubscribed(5_000), emptyList())')
    B(C, S_, 3, 'p', 'distinctUntilChanged so mỗi danh sách mới với danh sách trước bằng equals. Vì entity là data class, hai danh sách cùng nội dung được coi là bằng nhau, và bản thừa bị bỏ. Lưu ý: câu truy vấn vẫn chạy lại trong SQLite; distinctUntilChanged chỉ giúp giao diện khỏi vẽ lại vô ích. Muốn tự theo dõi một bảng mà không cần truy vấn, có invalidationTracker.createFlow(…).\nQuy tắc dễ nhớ: Flow của Room báo "bảng vừa đổi", không báo "kết quả của bạn vừa đổi". [[src:ax-room-async]]',
      'distinctUntilChanged compares each new list with the previous one using equals. Because entities are data classes, two lists with the same content count as equal, and the duplicate is dropped. Note: the query still reruns inside SQLite; distinctUntilChanged only spares the UI a useless redraw. To watch a table yourself without a query, there is invalidationTracker.createFlow(…).\nRule of thumb: a Room Flow says "the table changed", not "your result changed". [[src:ax-room-async]]')

    S_ = 'bugs'
    a(C + '.sec.%s.title' % S_, 'Hai lỗi hay gặp', 'Two common bugs')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'bug', 'Người dùng đặt lịch xong, quay về danh sách và không thấy lịch vừa đặt; phải kéo để làm mới.', 'A user books, goes back to the list and does not see the new booking; they have to pull to refresh.')
    B(C, S_, 1, 'cause', 'ViewModel đọc danh sách bằng hàm suspend một lần trong init. Lần insert ở màn đặt lịch không đánh thức ai.', 'The ViewModel reads the list once with a suspend function in init. The insert on the booking screen wakes nobody.')
    B(C, S_, 1, 'fix', 'Đổi hàm DAO sang trả về Flow và để ViewModel lộ nó ra bằng stateIn; mọi lần ghi ở bất kỳ màn nào đều tự đến danh sách.', 'Make the DAO function return a Flow and expose it from the ViewModel with stateIn; every write from any screen reaches the list on its own.')
    B(C, S_, 2, 'bug', 'Danh sách lịch nhấp nháy và cuộn về đầu mỗi khi đồng bộ nền cập nhật trạng thái của các lịch không liên quan.', 'The appointment list flickers and scrolls back to the top whenever background sync updates the status of unrelated appointments.')
    B(C, S_, 2, 'cause', 'Mỗi lần ghi vào bảng appointment làm Flow phát lại, kể cả khi kết quả của màn này không đổi; UI vẽ lại cả danh sách.', 'Every write to the appointment table makes the Flow emit again, even when this screen\'s result has not changed; the UI redraws the whole list.')
    B(C, S_, 2, 'fix', 'Thêm distinctUntilChanged trước stateIn; trong Compose, đặt key cho các phần tử của LazyColumn để giữ vị trí cuộn.', 'Add distinctUntilChanged before stateIn; in Compose, give LazyColumn items keys so the scroll position is kept.')

    S_ = 'ex'
    a(C + '.sec.%s.title' % S_, 'Bài tập', 'Exercise')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'ex', 'Viết DAO cho bảng appointment với: (1) Flow các lịch sắp tới của một bác sĩ (time ≥ now), sắp theo giờ; (2) hàm một lần trả về true nếu bác sĩ đã có lịch đúng giờ đó; (3) đổi trạng thái một lịch theo id, trả về số dòng đã đổi. Sau đó nói hàm nào màn Lịch nên dùng và hàm nào màn Đặt lịch nên dùng.',
      'Write a DAO for the appointment table with: (1) a Flow of a doctor\'s upcoming appointments (time ≥ now), sorted by time; (2) a one-shot function returning true if the doctor already has an appointment at that exact time; (3) changing an appointment\'s status by id, returning the number of rows changed. Then say which function the Schedule screen should use and which the Booking screen should use.')
    B(C, S_, 1, 'hint', 'Danh sách cần tự cập nhật thì Flow; câu hỏi chỉ cần trả lời một lần lúc bấm lưu thì suspend. now là tham số, không phải hằng trong SQL.', 'A list that must stay current is a Flow; a question answered once when the user taps save is suspend. now is a parameter, not a constant in the SQL.')
    B(C, S_, 1, 'sol', 'Màn Lịch dùng (1) vì danh sách phải tự đổi khi có lịch mới. Màn Đặt lịch dùng (2) lúc bấm lưu, rồi insert; và (3) cho nút hủy. Hàm (3) trả về Int: 0 nghĩa là id không tồn tại.',
      'The Schedule screen uses (1), since the list must update itself. The Booking screen uses (2) when the user taps save, then inserts; and (3) for the cancel button. Function (3) returns Int: 0 means the id does not exist.')
    B(C, S_, 1, 'solkt', '@Dao interface AppointmentDao {\n    @Query("SELECT * FROM appointment WHERE doctorId = :doctorId AND time >= :now ORDER BY time")\n    fun upcoming(doctorId: Long, now: Long): Flow<List<Appointment>>\n\n    @Query("SELECT EXISTS(SELECT 1 FROM appointment WHERE doctorId = :doctorId AND time = :time)")\n    suspend fun isTaken(doctorId: Long, time: Long): Boolean\n\n    @Query("UPDATE appointment SET status = :status WHERE id = :id")\n    suspend fun setStatus(id: Long, status: String): Int\n}')

    S_ = 'recall'
    a(C + '.sec.%s.title' % S_, 'Tự trả lời', 'Answer it yourself')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'ask', 'Một truy vấn Flow đọc bảng appointment. Ghi vào bảng note có làm nó chạy lại không?', 'A Flow query reads the appointment table. Does a write to the note table rerun it?')
    B(C, S_, 1, 'ans', 'Không. Room chỉ chạy lại truy vấn khi một bảng nó tham chiếu bị ghi.', 'No. Room reruns a query only when a table it references is written.')
    B(C, S_, 2, 'ask', 'Room bắt lỗi sai tên cột trong @Query lúc nào?', 'When does Room catch a misspelled column in @Query?')
    B(C, S_, 2, 'ans', 'Lúc biên dịch: câu SQL được kiểm khi build, nên lỗi là lỗi build.', 'At compile time: SQL is checked during the build, so the mistake is a build error.')

    for q, qv, qe, av, ae, wv, we in [
        ('q1', 'Ba phần của Room là gì?', 'What are Room\'s three parts?', 'Entity, DAO, lớp database.', 'Entities, DAOs, the database class.', 'Room sinh phần cài đặt lúc build.', 'Room generates the implementation at build time.'),
        ('q2', 'Truy vấn một lần trong Kotlin khai báo thế nào?', 'How is a one-shot query declared in Kotlin?', 'Hàm suspend trả về dữ liệu.', 'A suspend function returning the data.', 'Room 3.0 bắt buộc suspend cho truy vấn một lần.', 'Room 3.0 requires suspend for one-shot queries.'),
        ('q3', 'Sửa một dòng không thuộc kết quả có làm Flow phát lại không?', 'Does editing a row outside the result make the Flow emit again?', 'Có, nếu dòng đó ở bảng mà truy vấn đọc.', 'Yes, if the row is in a table the query reads.', 'Room theo dõi theo bảng; dùng distinctUntilChanged để bỏ bản giống hệt.', 'Room tracks tables; use distinctUntilChanged to drop identical copies.'),
        ('q4', '@Insert với một entity trả về gì?', 'What does @Insert with one entity return?', 'rowId mới (Long).', 'The new rowId (Long).', 'Với danh sách thì trả danh sách rowId.', 'With a collection it returns a collection of rowIds.')]:
        a(C + '.quiz.%s.q' % q, qv, qe); a(C + '.quiz.%s.a' % q, av, ae); a(C + '.quiz.%s.why' % q, wv, we)
