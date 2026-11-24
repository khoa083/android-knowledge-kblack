/* Đoạn mã track I (minh họa, rút gọn; không chạy trong trang). Số dòng được tham chiếu bởi codeHighlight trong models/models.js. */
(function () {
  var add = function (id, lines) { ADE.addCode('sysdesign', id, { lang: 'kotlin', illustrative: true, lines: lines }); };
  var c = function (vi, en) { return { vi: vi, en: en }; };
  add('i11.heavy', [
    'class ClinicApp : Application() {',
    '    override fun onCreate() {',
    '        super.onCreate()',
    '        Crash.init(this)                 // 80 ms',
    '        Analytics.init(this)             // 300 ms',
    '        Ads.init(this)                   // 900 ms',
    '        Chat.init(this)                  // 600 ms',
    '        ImageLoader.init(this)           // 150 ms',
    c('        db = openAndMigrate(this)        // 700 ms: mở và migrate database trên luồng chính', '        db = openAndMigrate(this)        // 700 ms: open and migrate the database on the main thread'),
    '    }',
    '}'
  ]);
  add('i11.lazy', [
    'class ClinicApp : Application() {',
    c('    override fun onCreate() { super.onCreate(); Crash.init(this) }   // chỉ thứ cần ngay: bắt crash từ sớm', '    override fun onCreate() { super.onCreate(); Crash.init(this) }   // only what is needed now: catch crashes early'),
    '}',
    c('class AnalyticsInitializer : Initializer<Analytics> {     // App Startup; bỏ meta-data để khởi tạo lười', 'class AnalyticsInitializer : Initializer<Analytics> {     // App Startup; remove the meta-data to init lazily'),
    '    override fun create(context: Context) = Analytics.init(context)',
    '    override fun dependencies() = emptyList<Class<out Initializer<*>>>()',
    '}',
    c('// Ads, Chat: khởi tạo khi mở màn cần chúng; database mở trên Dispatchers.IO', '// Ads, Chat: initialised when their screen opens; the database opens on Dispatchers.IO'),
    c('setContent { HomeScreen(state); ReportDrawnWhen { state.isLoaded } }   // báo TTFD khi nội dung thật đã hiện', 'setContent { HomeScreen(state); ReportDrawnWhen { state.isLoaded } }   // report TTFD once real content shows')
  ]);
  add('i10.full', [
    c('val bmp = BitmapFactory.decodeFile(path)                     // 4000 × 3000 × 4 byte ≈ 45,8 MiB', 'val bmp = BitmapFactory.decodeFile(path)                     // 4000 × 3000 × 4 bytes ≈ 45.8 MiB'),
    c('Image(bmp.asImageBitmap(), null, Modifier.size(90.dp))       // hiện ở 270×270 px, vẫn giữ cả ảnh gốc', 'Image(bmp.asImageBitmap(), null, Modifier.size(90.dp))       // shown at 270×270 px, still holding the original')
  ]);
  add('i10.sampled', [
    'val opts = BitmapFactory.Options().apply { inJustDecodeBounds = true }',
    c('BitmapFactory.decodeFile(path, opts)                          // chỉ đọc kích thước 4000×3000, chưa tốn bộ nhớ', 'BitmapFactory.decodeFile(path, opts)                          // reads only the size, 4000×3000, no memory yet'),
    'opts.inSampleSize = calculateInSampleSize(opts, 270, 270)     // 8 → 500×375',
    'opts.inJustDecodeBounds = false',
    c('val bmp = BitmapFactory.decodeFile(path, opts)                // 500 × 375 × 4 byte ≈ 0,72 MiB', 'val bmp = BitmapFactory.decodeFile(path, opts)                // 500 × 375 × 4 bytes ≈ 0.72 MiB'),
    c('// thực tế: thư viện ảnh (Glide, Coil) làm việc này theo kích thước view và có cache', '// in practice an image library (Glide, Coil) does this for the view size, with caching')
  ]);
  add('i10.whole', [
    'val body = file.asRequestBody("video/mp4".toMediaType())',
    c('api.upload(body)                   // một request 200 MB: đứt ở 95% thì gửi lại cả 200 MB', 'api.upload(body)                   // one 200 MB request: cut at 95%, resend all 200 MB')
  ]);
  add('i10.resumable', [
    c('val url = store.uploadUrl ?: api.createUpload(file.length()).also { store.uploadUrl = it }  // POST → Location, lưu lại', 'val url = store.uploadUrl ?: api.createUpload(file.length()).also { store.uploadUrl = it }  // POST → Location, kept'),
    c('var offset = api.uploadOffset(url)                       // HEAD → Upload-Offset: server đã có bao nhiêu', 'var offset = api.uploadOffset(url)                       // HEAD → Upload-Offset: how much the server has'),
    'while (offset < file.length()) {',
    '    val n = minOf(CHUNK, file.length() - offset)',
    c('    offset = api.append(url, file.slice(offset, n), offset)   // PATCH, Upload-Offset: offset', '    offset = api.append(url, file.slice(offset, n), offset)   // PATCH, Upload-Offset: offset'),
    '}',
    c('// chạy trong WorkManager (foreground) hay job UIDT (Android 14+), để sống qua khi app ra nền', '// run in WorkManager (foreground) or a UIDT job (Android 14+), so it survives the app going to the background')
  ]);
  add('i9.payload', [
    c('// server: gửi cả nội dung trong push', '// server: the whole content goes in the push'),
    c('push.send(device, mapOf("text" to "Lịch khám đổi sang 10:00"))', 'push.send(device, mapOf("text" to "Your visit moved to 10:00"))'),
    c('// app: hiện đúng chữ nhận được, theo thứ tự tới', '// app: show exactly the text received, in arrival order'),
    'notifier.show(msg.data["text"])'
  ]);
  add('i9.tickle', [
    c('// server: push chỉ báo "lịch b42 vừa đổi"; cùng khóa gộp thì cái mới thay cái cũ chưa giao', '// server: the push only says "booking b42 changed"; with one collapse key the newer replaces an undelivered older one'),
    'push.send(device, mapOf("type" to "booking", "id" to "b42"), collapseKey = "booking-b42")',
    c('// app: callback chỉ có vài giây, nên giao việc tải cho WorkManager', '// app: the callback only gets a few seconds, so hand the fetch to WorkManager'),
    'WorkManager.getInstance(ctx).enqueue(syncBooking(msg.data["id"]!!))',
    c('// SyncWorker: val b = api.booking(id); db.save(b); notifier.show(b)   // luôn là bản mới nhất', '// SyncWorker: val b = api.booking(id); db.save(b); notifier.show(b)   // always the latest version'),
    c('// mở app cũng đồng bộ: push mất thì màn hình vẫn đúng', '// opening the app also syncs: if a push is lost, the screen is still right')
  ]);
  add('i9.dedupe', [
    'val eventId = msg.data["eventId"] ?: return',
    c('if (!db.markSeen(eventId)) return          // đã thấy id này: bỏ (lưu trong database, sống qua process chết)', 'if (!db.markSeen(eventId)) return          // id seen before: drop (kept in the database, survives process death)'),
    'notifier.show(eventId)'
  ]);
  add('i8.lww', [
    'data class Note(val id: String, val symptom: String, val allergy: String, val memo: String, val editedAt: Long)',
    c('suspend fun save(note: Note) = api.put(note.id, note)                  // cả bản ghi, kể cả trường không sửa', 'suspend fun save(note: Note) = api.put(note.id, note)                  // the whole record, untouched fields too'),
    c('// server: if (incoming.editedAt > stored.editedAt) stored = incoming   // so giờ do máy client đặt', '// server: if (incoming.editedAt > stored.editedAt) stored = incoming   // compares times set by client clocks')
  ]);
  add('i8.ifmatch', [
    'suspend fun save(id: String, edit: (Note) -> Note): Boolean {',
    c('    var cur = api.get(id)                                         // nội dung + ETag "v1"', '    var cur = api.get(id)                                         // body + ETag "v1"'),
    '    repeat(3) {',
    '        val res = api.put(id, edit(cur.body), ifMatch = cur.etag)',
    c('        if (res.code != 412) return res.isSuccessful               // 2xx: đã lưu', '        if (res.code != 412) return res.isSuccessful               // 2xx: saved'),
    c('        cur = api.get(id)                                         // 412: có người sửa trước; tải bản mới, làm lại thay đổi', '        cur = api.get(id)                                         // 412: someone edited first; fetch the new one, redo the change'),
    '    }',
    c('    return false                                                  // vẫn xung đột: hỏi người dùng', '    return false                                                  // still conflicting: ask the user'),
    '}'
  ]);
  add('i8.field', [
    c('data class NotePatch(val baseVersion: Int, val changes: Map<String, String>)   // chỉ các trường đã sửa', 'data class NotePatch(val baseVersion: Int, val changes: Map<String, String>)   // only the edited fields'),
    'suspend fun save(id: String, base: Note, mine: Note): SaveResult =',
    c('    api.patch(id, NotePatch(base.version, diff(base, mine)))     // {"symptom": "ho, sốt"}', '    api.patch(id, NotePatch(base.version, diff(base, mine)))     // {"symptom": "cough, fever"}'),
    c('// server, từng trường: chỉ một bên sửa → lấy bên đó; hai bên sửa khác nhau → xung đột', '// server, per field: edited on one side only → take it; edited differently on both → conflict'),
    'sealed interface SaveResult { data class Saved(val note: Note) : SaveResult; data class Conflict(val field: String, val theirs: String, val mine: String) : SaveResult }'
  ]);
  add('i7.offset', [
    'class NewsSource(private val api: NewsApi) : PagingSource<Int, Post>() {',
    '    override suspend fun load(params: LoadParams<Int>): LoadResult<Int, Post> {',
    c('        val offset = params.key ?: 0                                     // khóa là vị trí trong danh sách', '        val offset = params.key ?: 0                                     // the key is a position in the list'),
    c('        val posts = api.news(offset = offset, limit = params.loadSize)   // GET /news?offset=4&limit=4', '        val posts = api.news(offset = offset, limit = params.loadSize)   // GET /news?offset=4&limit=4'),
    '        return LoadResult.Page(posts, prevKey = null,',
    c('            nextKey = if (posts.isEmpty()) null else offset + posts.size)  // vị trí lệch khi danh sách đổi', '            nextKey = if (posts.isEmpty()) null else offset + posts.size)  // positions shift when the list changes'),
    '    }',
    c('    override fun getRefreshKey(state: PagingState<Int, Post>): Int? = null   // làm mới: tải lại từ đầu', '    override fun getRefreshKey(state: PagingState<Int, Post>): Int? = null   // refresh: reload from the top'),
    '}',
    c('// LazyColumn { items(posts.itemCount, key = posts.itemKey { it.id }) { … } }  // id trùng → crash', '// LazyColumn { items(posts.itemCount, key = posts.itemKey { it.id }) { … } }  // duplicate id → crash')
  ]);
  add('i7.cursor', [
    'class NewsSource(private val api: NewsApi) : PagingSource<String, Post>() {',
    '    override suspend fun load(params: LoadParams<String>): LoadResult<String, Post> {',
    c('        val res = api.news(pageToken = params.key, limit = params.loadSize)  // GET /news?limit=4&page_token=tk1', '        val res = api.news(pageToken = params.key, limit = params.loadSize)  // GET /news?limit=4&page_token=tk1'),
    '        return LoadResult.Page(res.posts, prevKey = null,',
    c('            nextKey = res.nextPageToken.ifEmpty { null })                  // rỗng: hết danh sách', '            nextKey = res.nextPageToken.ifEmpty { null })                  // empty: end of the list'),
    '    }',
    c('    override fun getRefreshKey(state: PagingState<String, Post>): String? = null  // làm mới: tải lại từ đầu', '    override fun getRefreshKey(state: PagingState<String, Post>): String? = null  // refresh: reload from the top'),
    '}',
    c('// server giải tk1 thành (giờ đăng, id) của bài 17: WHERE (published_at, id) < (t17, 17) ORDER BY published_at DESC, id DESC', '// the server decodes tk1 as (published time, id) of post 17: WHERE (published_at, id) < (t17, 17) ORDER BY published_at DESC, id DESC')
  ]);
  add('i6.none', [
    c('suspend fun fees(): List<Fee> = api.fees()         // mỗi lần mở: tải 200 KB', 'suspend fun fees(): List<Fee> = api.fees()         // every open: download 200 KB')
  ]);
  add('i6.forever', [
    'suspend fun fees(): List<Fee> {',
    c('    memory["fees"]?.let { return it }                                 // mất khi process chết', '    memory["fees"]?.let { return it }                                 // lost when the process dies'),
    c('    disk.read("fees")?.let { memory["fees"] = it; return it }         // không có hạn dùng', '    disk.read("fees")?.let { memory["fees"] = it; return it }         // no expiry at all'),
    '    return api.fees().also { disk.write("fees", it); memory["fees"] = it }',
    '}'
  ]);
  add('i6.http', [
    'val client = OkHttpClient.Builder()',
    c('    .cache(Cache(File(cacheDir, "http"), 10L * 1024 * 1024))     // cache HTTP trên đĩa, 10 MB', '    .cache(Cache(File(cacheDir, "http"), 10L * 1024 * 1024))     // HTTP disk cache, 10 MB'),
    '    .build()',
    c('// server gửi: Cache-Control: max-age=300 (và ETag: "v7")', '// the server sends: Cache-Control: max-age=300 (and ETag: "v7")'),
    c('// còn tươi: trả từ cache, không gọi mạng', '// still fresh: served from the cache, no network call'),
    c('// đã cũ, có ETag: tự gửi If-None-Match; 304 → dùng lại bản đã lưu', '// stale, with an ETag: sends If-None-Match itself; 304 → reuse the stored copy')
  ]);
  add('i5.nokey', [
    'suspend fun book(slot: Slot): Appointment {',
    '    repeat(3) {',
    '        try { return api.book(slot) }                         // POST /appointments',
    c('        catch (e: SocketTimeoutException) { delay(1_000) }   // không biết server đã làm chưa', '        catch (e: SocketTimeoutException) { delay(1_000) }   // did the server do it? unknown'),
    '    }',
    c('    error("hết lượt thử")', '    error("out of attempts")'),
    '}'
  ]);
  add('i5.key', [
    c('val key = draft.idempotencyKey                 // sinh một lần khi bấm "Đặt lịch", lưu trong Room', 'val key = draft.idempotencyKey                 // generated once on "Book", stored in Room'),
    'repeat(3) { attempt ->',
    c('    try { return api.book(slot, idempotencyKey = key) }   // header Idempotency-Key', '    try { return api.book(slot, idempotencyKey = key) }   // the Idempotency-Key header'),
    '    catch (e: SocketTimeoutException) { delay(backoffMillis(attempt)) }',
    '}',
    c('// server: key đã thấy → trả lại kết quả cũ, không tạo lịch mới', '// server: key already seen → return the earlier result, create nothing')
  ]);
  add('i5.storm', [
    c('// sai: mọi máy chờ cùng một khoảng cố định', '// wrong: every phone waits the same fixed time'),
    'delay(2_000)',
    c('// tốt hơn: exponential backoff', '// better: exponential backoff'),
    c('val cap = 1_000L shl attempt                  // 1, 2, 4, 8 giây', 'val cap = 1_000L shl attempt                  // 1, 2, 4, 8 seconds'),
    c('delay(Random.nextLong(0, cap))                // jitter: ngẫu nhiên trong [0, cap)', 'delay(Random.nextLong(0, cap))                // jitter: random in [0, cap)')
  ]);
  add('i4.poll', [
    c('while (isActive) {                          // kể cả khi app ở nền', 'while (isActive) {                          // even with the app in background'),
    c('    val news = api.messagesSince(lastId)    // phần lớn trả về rỗng', '    val news = api.messagesSince(lastId)    // mostly returns empty'),
    '    if (news.isNotEmpty()) show(news)',
    c('    delay(5_000)                            // mỗi lần hỏi giữ radio thức ~18 giây', '    delay(5_000)                            // each request keeps the radio up ~18 s'),
    '}'
  ]);
  add('i4.long', [
    'while (isActive) {',
    c('    val news = api.waitForMessages(lastId)  // server giữ tới khi có tin hay hết hạn', '    val news = api.waitForMessages(lastId)  // the server holds it until news or a timeout'),
    c('    if (news.isNotEmpty()) show(news)       // rồi hỏi lại ngay', '    if (news.isNotEmpty()) show(news)       // then ask again at once'),
    '}'
  ]);
  add('i4.ws', [
    c('val ws = client.newWebSocket(request, object : WebSocketListener() {   // HTTP rồi nâng cấp', 'val ws = client.newWebSocket(request, object : WebSocketListener() {   // HTTP, then upgraded'),
    c('    override fun onMessage(ws: WebSocket, text: String) = show(parse(text))   // server đẩy xuống', '    override fun onMessage(ws: WebSocket, text: String) = show(parse(text))   // server pushes down'),
    c('    override fun onFailure(ws: WebSocket, t: Throwable, r: Response?) = reconnectLater()   // Doze, mất mạng', '    override fun onFailure(ws: WebSocket, t: Throwable, r: Response?) = reconnectLater()   // Doze, offline'),
    '})',
    c('ws.send(outgoing.toJson())                  // gửi trên cùng kết nối', 'ws.send(outgoing.toJson())                  // send on the same connection'),
    c('// rời màn chat: ws.close(1000, null), để FCM lo phần còn lại', '// leaving the chat screen: ws.close(1000, null) and let FCM take over')
  ]);
  add('i4.push', [
    c('override fun onNewToken(token: String) = tokenRepo.upload(token)       // server cần token', 'override fun onNewToken(token: String) = tokenRepo.upload(token)       // the server needs the token'),
    c('// app không giữ kết nối nào; hệ thống giữ một kết nối chung tới FCM', '// the app keeps no connection; the system keeps one shared FCM connection'),
    'override fun onMessageReceived(msg: RemoteMessage) {',
    c('    val convId = msg.data["conversationId"] ?: return   // chỉ id, không có nội dung', '    val convId = msg.data["conversationId"] ?: return   // only an id, no content'),
    c('    notifier.showNewMessage(convId); SyncWork.enqueue(this, convId)   // tải theo thứ tự', '    notifier.showNewMessage(convId); SyncWork.enqueue(this, convId)   // fetch in order'),
    '}'
  ]);
  add('i3.hold', [
    c('// luồng đồng bộ (nền)', '// sync thread (background)'),
    'synchronized(cacheLock) {',
    c('    db.insertAll(appointments)        // khoảng 6 giây I/O trong lúc giữ khóa', '    db.insertAll(appointments)        // about 6 seconds of I/O while holding the lock'),
    '}',
    c('// main thread, khi người dùng chạm', '// main thread, on a tap'),
    c('synchronized(cacheLock) {             // bị chặn: chờ luồng nền nhả khóa', 'synchronized(cacheLock) {             // blocks: waits for the background thread'),
    '    adapter.submitList(cache.toList())',
    '}'
  ]);
  add('i3.cycle', [
    c('// luồng đồng bộ: dbLock rồi cacheLock', '// sync thread: dbLock, then cacheLock'),
    'synchronized(dbLock) {',
    '    synchronized(cacheLock) { cache.replaceAll(readDb()) }',
    '}',
    c('// main thread: cacheLock rồi dbLock (ngược thứ tự)', '// main thread: cacheLock, then dbLock (the opposite order)'),
    'synchronized(cacheLock) {',
    '    synchronized(dbLock) { db.markSeen(id) }',
    '}'
  ]);
  add('i3.order', [
    c('// mọi nơi: cacheLock (1) trước, dbLock (2) sau', '// everywhere: cacheLock (1) first, dbLock (2) second'),
    c('val rows = synchronized(cacheLock) { synchronized(dbLock) { cache.toList() } }  // sao chép rồi nhả', 'val rows = synchronized(cacheLock) { synchronized(dbLock) { cache.toList() } }  // copy, then release'),
    c('withContext(Dispatchers.IO) { db.insertAll(rows) }                            // I/O ngoài khóa', 'withContext(Dispatchers.IO) { db.insertAll(rows) }                            // I/O outside the lock'),
    c('// main thread', '// main thread'),
    c('val list = synchronized(cacheLock) { cache.toList() }    // chờ vài trăm mili giây là cùng', 'val list = synchronized(cacheLock) { cache.toList() }    // waits a few hundred ms at most'),
    'adapter.submitList(list)',
    c('// trong coroutine: mutex.withLock { … } treo coroutine, không chặn luồng', '// in a coroutine: mutex.withLock { … } suspends the coroutine, never blocks the thread')
  ]);
  add('i2.vm', [
    'class BookingViewModel : ViewModel() {',
    c('    var doctorId by mutableStateOf<Long?>(null)     // chỉ trong bộ nhớ của process', '    var doctorId by mutableStateOf<Long?>(null)     // only in the process\'s memory'),
    '    var note by mutableStateOf("")',
    c('    var photoUri: Uri? = null                      // Uri của tệp ảnh sắp chụp', '    var photoUri: Uri? = null                      // Uri of the photo file about to be taken'),
    '}',
    c('// Activity: mở Camera, app bị che hẳn → onStop, process vào nhóm cached', '// Activity: open the Camera, the app is fully covered → onStop, the process goes cached'),
    'takePhoto.launch(vm.photoUri)',
    c('// lmkd giết process: ViewModel mất; onDestroy() có thể không chạy', '// lmkd kills the process: the ViewModel is gone; onDestroy() may not run'),
    c('// process mới: ViewModel mới, doctorId = null, note = "", photoUri = null', '// new process: a new ViewModel, doctorId = null, note = "", photoUri = null')
  ]);
  add('i2.saved', [
    'class BookingViewModel(private val state: SavedStateHandle) : ViewModel() {',
    c('    val doctorId = state.getStateFlow<Long?>("doctorId", null)   // chỉ một id', '    val doctorId = state.getStateFlow<Long?>("doctorId", null)   // just an id'),
    '    val note = state.getStateFlow("note", "")',
    c('    fun photoTarget(uri: Uri) { state["photoUri"] = uri }       // Uri, không phải ảnh', '    fun photoTarget(uri: Uri) { state["photoUri"] = uri }       // the Uri, not the image'),
    '}',
    c('// onStop: hệ thống sao saved state ra ngoài process', '// onStop: the system copies saved state outside the process'),
    c('// lmkd giết process: ViewModel mất, bản sao saved state còn', '// lmkd kills the process: the ViewModel is gone, the saved-state copy remains'),
    c('val takePhoto = registerForActivityResult(TakePicture()) { ok ->   // đăng ký mỗi lần tạo Activity', 'val takePhoto = registerForActivityResult(TakePicture()) { ok ->   // registered on every creation'),
    c('    if (ok) vm.attachPhoto()                    // đọc photoUri từ SavedStateHandle đã khôi phục', '    if (ok) vm.attachPhoto()                    // reads photoUri from the restored SavedStateHandle'),
    '}'
  ]);
})();
