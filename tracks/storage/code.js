/* Đoạn mã track H (minh họa, rút gọn; không chạy trong trang). Số dòng được tham chiếu bởi codeHighlight trong models/models.js. */
(function () {
  var add = function (id, lines) { ADE.addCode('storage', id, { lang: 'kotlin', illustrative: true, lines: lines }); };
  var c = function (vi, en) { return { vi: vi, en: en }; };
  add('h7.online', [
    c('fun book(slot: Slot) = viewModelScope.launch {', 'fun book(slot: Slot) = viewModelScope.launch {'),
    c('    try { api.book(slot) }                         // mất mạng: ném IOException', '    try { api.book(slot) }                         // offline: throws IOException'),
    c('    catch (e: IOException) { _error.value = e }     // không có gì được lưu', '    catch (e: IOException) { _error.value = e }     // nothing is stored'),
    c('}                                                 // báo lỗi cho người dùng', '}                                                 // shows an error'),
    c('// người dùng tắt app: lịch chưa từng tồn tại ở đâu', '// the user closes the app: the booking never existed anywhere')
  ]);
  add('h7.coroutine', [
    c('fun book(slot: Slot) = viewModelScope.launch {', 'fun book(slot: Slot) = viewModelScope.launch {'),
    c('    val id = dao.insert(Appointment(slot, sync = PENDING))   // lưu máy trước', '    val id = dao.insert(Appointment(slot, sync = PENDING))   // local first'),
    c('    // UI đọc Flow từ dao nên hiện lịch ngay', '    // the UI reads a Flow from the dao, so it shows at once'),
    c('    while (true) { try { api.book(slot); dao.markSynced(id); break }', '    while (true) { try { api.book(slot); dao.markSynced(id); break }'),
    c('                   catch (e: IOException) { delay(30_000) } }   // thử lại trong coroutine', '                   catch (e: IOException) { delay(30_000) } }   // retries inside the coroutine'),
    c('}   // app đóng: coroutine dừng, #9 kẹt PENDING', '}   // app closes: the coroutine stops, #9 is stuck PENDING')
  ]);
  add('h7.lazy', [
    c('suspend fun book(slot: Slot) {', 'suspend fun book(slot: Slot) {'),
    c('    dao.insert(Appointment(slot, sync = PENDING))            // 1. lưu máy trước', '    dao.insert(Appointment(slot, sync = PENDING))            // 1. local first'),
    '    workManager.enqueueUniqueWork("sync", ExistingWorkPolicy.KEEP,',
    c('        OneTimeWorkRequestBuilder<SyncWorker>().setConstraints(onlyWhenOnline).build())   // 2. giao cho WorkManager', '        OneTimeWorkRequestBuilder<SyncWorker>().setConstraints(onlyWhenOnline).build())   // 2. hand it to WorkManager'),
    c('}   // app có thể bị tắt ngay sau dòng này', '}   // the app may be killed right after this line'),
    'class SyncWorker(ctx: Context, p: WorkerParameters) : CoroutineWorker(ctx, p) {',
    '    override suspend fun doWork(): Result {',
    c('        for (a in dao.pending()) {                           // đọc hàng chờ trong Room', '        for (a in dao.pending()) {                           // reads the queue in Room'),
    c('            try { api.book(a.slot) } catch (e: IOException) { return Result.retry() }', '            try { api.book(a.slot) } catch (e: IOException) { return Result.retry() }'),
    c('            dao.markSynced(a.id) }                           // 3. đánh dấu đã đồng bộ', '            dao.markSynced(a.id) }                           // 3. mark it synced'),
    '        return Result.success()',
    '    }',
    '}'
  ]);
  add('h6.missing', [
    c('@Database(entities = [Appointment::class], version = 3)   // app mới khai báo v3', '@Database(entities = [Appointment::class], version = 3)   // the new app declares v3'),
    c('Room.databaseBuilder<AppDatabase>(ctx, "clinic.db")', 'Room.databaseBuilder<AppDatabase>(ctx, "clinic.db")'),
    c('    .addMigrations(MIGRATION_2_3)                       // không có đường 1 → 2', '    .addMigrations(MIGRATION_2_3)                       // no path from 1 to 2'),
    '    .build()'
  ]);
  add('h6.destructive', [
    '@Database(entities = [Appointment::class], version = 3)',
    'Room.databaseBuilder<AppDatabase>(ctx, "clinic.db")',
    '    .addMigrations(MIGRATION_2_3)',
    c('    .fallbackToDestructiveMigration()                   // thiếu đường: xóa sạch bảng, tạo lại', '    .fallbackToDestructiveMigration()                   // missing path: drop every table, recreate'),
    '    .build()'
  ]);
  add('h6.complete', [
    c('@Database(entities = [Appointment::class], version = 3,', '@Database(entities = [Appointment::class], version = 3,'),
    c('    autoMigrations = [AutoMigration(from = 1, to = 2)])   // thêm cột note: Room tự sinh', '    autoMigrations = [AutoMigration(from = 1, to = 2)])   // adds the note column: Room generates it'),
    c('abstract class AppDatabase : RoomDatabase()', 'abstract class AppDatabase : RoomDatabase()'),
    '',
    c('val MIGRATION_2_3 = object : Migration(2, 3) {           // đổi dữ liệu: phải viết tay', 'val MIGRATION_2_3 = object : Migration(2, 3) {           // transforms data: written by hand'),
    '    override suspend fun migrate(connection: SQLiteConnection) {',
    '        connection.execSQL("ALTER TABLE appointment ADD COLUMN statusCode INTEGER NOT NULL DEFAULT 0")',
    '        connection.execSQL("UPDATE appointment SET statusCode = 2 WHERE status = \'done\'")',
    c('    }                                                     // xong: Room kiểm schema khớp v3', '    }                                                     // then Room checks the schema matches v3'),
    '}'
  ]);
  add('h5.loop', [
    c('val doctors = dao.doctors()                         // truy vấn 1', 'val doctors = dao.doctors()                         // query 1'),
    c('val result = doctors.associateWith { d ->', 'val result = doctors.associateWith { d ->'),
    c('    dao.appointmentsOf(d.id)                         // thêm 1 truy vấn cho mỗi bác sĩ', '    dao.appointmentsOf(d.id)                         // one more query per doctor'),
    c('}                                                   // tổng: 1 + N, không có giao dịch', '}                                                   // total: 1 + N, no transaction')
  ]);
  add('h5.relation', [
    'data class DoctorWithAppointments(',
    '    @Embedded val doctor: Doctor,',
    '    @Relation(parentColumns = ["id"], entityColumns = ["doctorId"])',
    '    val appointments: List<Appointment>,',
    ')',
    '@Transaction',
    c('@Query("SELECT * FROM doctor")                      // Room chạy thêm một câu cho bảng appointment', '@Query("SELECT * FROM doctor")                      // Room runs one more query for appointment'),
    c('suspend fun doctorsWithAppointments(): List<DoctorWithAppointments>   // 2 truy vấn, một giao dịch', 'suspend fun doctorsWithAppointments(): List<DoctorWithAppointments>   // 2 queries, one transaction')
  ]);
  add('h5.multimap', [
    '@Query("SELECT * FROM doctor JOIN appointment ON appointment.doctorId = doctor.id")',
    c('suspend fun doctorsWithAppointments(): Map<Doctor, List<Appointment>>   // 1 câu JOIN', 'suspend fun doctorsWithAppointments(): Map<Doctor, List<Appointment>>   // 1 JOIN query'),
    c('// Room gom các dòng (bác sĩ, lịch) thành Map theo bác sĩ', '// Room groups the (doctor, appointment) rows into a Map by doctor')
  ]);
  add('h4.flow', [
    '@Dao interface AppointmentDao {',
    '    @Query("SELECT * FROM appointment WHERE doctorId = :doctorId ORDER BY time")',
    c('    fun byDoctor(doctorId: Long): Flow<List<Appointment>>   // quan sát', '    fun byDoctor(doctorId: Long): Flow<List<Appointment>>   // observable'),
    '}',
    c('dao.byDoctor(A).collect { show(it) }                      // chạy lần đầu: 3 lịch', 'dao.byDoctor(A).collect { show(it) }                      // first run: 3 appointments'),
    c('dao.insert(Appointment(doctorId = A, …))                  // bảng appointment đổi', 'dao.insert(Appointment(doctorId = A, …))                  // the appointment table changes'),
    c('//   → Room chạy lại truy vấn, Flow phát 4 lịch', '//   → Room reruns the query, the Flow emits 4'),
    c('dao.update(apptOfDoctorB.copy(status = "done"))          // vẫn bảng appointment: chạy lại, kết quả như cũ', 'dao.update(apptOfDoctorB.copy(status = "done"))          // same table: rerun, same result'),
    c('noteDao.insert(Note(…))                                   // bảng note: truy vấn này không chạy lại', 'noteDao.insert(Note(…))                                   // note table: this query does not rerun')
  ]);
  add('h4.oneshot', [
    '@Dao interface AppointmentDao {',
    '    @Query("SELECT * FROM appointment WHERE doctorId = :doctorId ORDER BY time")',
    c('    suspend fun byDoctorOnce(doctorId: Long): List<Appointment>   // một lần', '    suspend fun byDoctorOnce(doctorId: Long): List<Appointment>   // one-shot'),
    c('}                                                                 // show(dao.byDoctorOnce(A)): 3 lịch', '}                                                                 // show(dao.byDoctorOnce(A)): 3 appointments'),
    '',
    c('dao.insert(Appointment(doctorId = A, …))       // database có 4 lịch', 'dao.insert(Appointment(doctorId = A, …))       // the database has 4'),
    c('//   → màn hình vẫn 3: không ai đọc lại', '//   → the screen still shows 3: nobody reads again'),
    c('dao.update(apptOfDoctorB.copy(status = "done"))', 'dao.update(apptOfDoctorB.copy(status = "done"))'),
    c('noteDao.insert(Note(…))                        // màn hình vẫn 3 tới khi tự tải lại', 'noteDao.insert(Note(…))                        // still 3 until you reload by hand')
  ]);
  add('h3.commit', [
    c('// màn Cài đặt, trong onClick (main thread)', '// Settings screen, inside onClick (main thread)'),
    c('val ok = prefs.edit().putBoolean("dark_theme", true).commit()   // chờ ghi xong cả file', 'val ok = prefs.edit().putBoolean("dark_theme", true).commit()   // waits for the whole file to be written'),
    c('if (ok) recreate()                                                // chỉ chạy khi commit trả về', 'if (ok) recreate()                                                // runs only once commit returns')
  ]);
  add('h3.apply', [
    c('// màn Cài đặt, trong onClick (main thread)', '// Settings screen, inside onClick (main thread)'),
    c('prefs.edit().putBoolean("dark_theme", true).apply()   // đổi bộ nhớ ngay, xếp hàng ghi đĩa', 'prefs.edit().putBoolean("dark_theme", true).apply()   // memory now, disk write queued'),
    c('recreate()', 'recreate()'),
    c('// onStop(): framework chờ các lần apply() đang ghi xong rồi mới chuyển trạng thái', '// onStop(): the framework waits for in-flight apply() writes before switching state'),
    c('// ghi lỗi: không ai được báo', '// a failed write: nobody is told')
  ]);
  add('h3.datastore', [
    'val Context.dataStore by preferencesDataStore(name = "settings")',
    'val DARK = booleanPreferencesKey("dark_theme")',
    c('val dark: Flow<Boolean> = context.dataStore.data', 'val dark: Flow<Boolean> = context.dataStore.data'),
    c('    .map { it[DARK] ?: false }                       // UI thu Flow này', '    .map { it[DARK] ?: false }                       // the UI collects this Flow'),
    c('// màn Cài đặt: onClick → ViewModel', '// Settings screen: onClick → ViewModel'),
    c('fun onDarkChanged(v: Boolean) = viewModelScope.launch {', 'fun onDarkChanged(v: Boolean) = viewModelScope.launch {'),
    c('    context.dataStore.edit { it[DARK] = v }          // suspend: main không bị chặn', '    context.dataStore.edit { it[DARK] = v }          // suspend: main is not blocked'),
    '}'
  ]);
  add('h2.direct', [
    'fun saveDraft(text: String) {',
    c('    FileOutputStream(File(filesDir, "draft.txt")).use { out ->   // mở: file bị cắt về 0 byte', '    FileOutputStream(File(filesDir, "draft.txt")).use { out ->   // open: the file is truncated to 0 bytes'),
    c('        out.write(text.toByteArray())                          // tiến trình chết ở đây: file dở dang', '        out.write(text.toByteArray())                          // process dies here: a half-written file'),
    '    }',
    '}',
    c('fun loadDraft(): String =', 'fun loadDraft(): String ='),
    c('    File(filesDir, "draft.txt").readText()                     // đọc được nửa bản nháp', '    File(filesDir, "draft.txt").readText()                     // reads half a draft')
  ]);
  add('h2.atomic', [
    'fun saveDraft(text: String) {',
    '    val file = AtomicFile(File(filesDir, "draft.txt"))',
    c('    val out = file.startWrite()                                // ghi vào draft.txt.new', '    val out = file.startWrite()                                // writes to draft.txt.new'),
    c('    try { out.write(text.toByteArray()); file.finishWrite(out) } // sync rồi đổi tên đè lên', '    try { out.write(text.toByteArray()); file.finishWrite(out) } // sync, then rename over'),
    c('    catch (e: IOException) { file.failWrite(out); throw e }     // xóa file .new', '    catch (e: IOException) { file.failWrite(out); throw e }     // deletes the .new file'),
    '}',
    'fun loadDraft(): String =',
    '    AtomicFile(File(filesDir, "draft.txt"))',
    c('        .readFully().decodeToString()                          // luôn là bản trọn vẹn gần nhất', '        .readFully().decodeToString()                          // always the last complete version')
  ]);
  add('h2.cache', [
    'suspend fun resultPdf(id: Long): File {',
    c('    val f = File(cacheDir, "result-$id.pdf")', '    val f = File(cacheDir, "result-$id.pdf")'),
    c('    // lần đầu: tải về và ghi vào cache', '    // first time: download and write to the cache'),
    c('    // … vài ngày sau, máy thiếu chỗ: hệ thống có thể xóa f', '    // … days later, space runs low: the system may delete f'),
    c('    return f                    // sai: mở thẳng, f có thể đã không còn', '    return f                    // wrong: opened as is, f may be gone'),
    '}',
    c('suspend fun resultPdfSafe(id: Long): File {', 'suspend fun resultPdfSafe(id: Long): File {'),
    '    val f = File(cacheDir, "result-$id.pdf")',
    c('    if (!f.exists()) api.download(id, f)   // kiểm trước khi đọc, thiếu thì tải lại', '    if (!f.exists()) api.download(id, f)   // check before reading, download again if missing'),
    '    return f',
    '}'
  ]);
})();
