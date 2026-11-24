/* Đoạn mã track I (minh họa, rút gọn; không chạy trong trang). Số dòng được tham chiếu bởi codeHighlight trong models/models.js. */
(function () {
  var add = function (id, lines) { ADE.addCode('sysdesign', id, { lang: 'kotlin', illustrative: true, lines: lines }); };
  var c = function (vi, en) { return { vi: vi, en: en }; };
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
