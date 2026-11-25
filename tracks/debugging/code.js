/* Đoạn mã track L (minh họa, rút gọn; không chạy trong trang). Số dòng được tham chiếu bởi codeHighlight trong models/models.js. */
(function () {
  var add = function (id, lines) { ADE.addCode('debugging', id, { lang: 'kotlin', illustrative: true, lines: lines }); };
  var c = function (vi, en) { return { vi: vi, en: en }; };

  /* l1: hai bản sửa theo đoán: cố định màn hình dọc (dòng 1–2) và phép kiểm isInitialized (dòng 7) */
  add('l1.guess', [
    c('// AndroidManifest.xml, bản 1.4.1', '// AndroidManifest.xml, release 1.4.1'),
    '<activity android:name=".MainActivity" android:screenOrientation="portrait" />',
    'class BookingDetailFragment : Fragment() {',
    '    private lateinit var booking: Booking',
    '    fun show(b: Booking) { booking = b }',
    '    override fun onViewCreated(view: View, saved: Bundle?) {',
    c('        if (!::booking.isInitialized) return        // bản 1.4.2: hết crash, ra màn trống', '        if (!::booking.isInitialized) return        // release 1.4.2: no crash, a blank screen'),
    '        binding.patient.text = booking.patientName',
    '    }',
    '}'
  ]);
  /* l1: nguyên nhân: dữ liệu chỉ vào qua setter (dòng 3), đọc ở dòng 5 */
  add('l1.bug', [
    'class BookingDetailFragment : Fragment() {',
    '    private lateinit var booking: Booking',
    c('    fun show(b: Booking) { booking = b }          // chỉ màn danh sách gọi', '    fun show(b: Booking) { booking = b }          // only the list screen calls it'),
    '    override fun onViewCreated(view: View, saved: Bundle?) {',
    c('        binding.patient.text = booking.patientName   // tạo lại: UninitializedPropertyAccessException', '        binding.patient.text = booking.patientName   // after recreation: UninitializedPropertyAccessException'),
    '    }',
    '}'
  ]);
  /* l1: sửa: id đi qua arguments (dòng 2, 9), hệ thống lưu và trả lại khi tạo lại Fragment */
  add('l1.fix', [
    'class BookingDetailFragment : Fragment() {',
    '    private val bookingId get() = requireArguments().getLong("bookingId")',
    '    private val vm: DetailViewModel by viewModels()',
    '    override fun onViewCreated(view: View, saved: Bundle?) {',
    '        vm.load(bookingId)',
    '        vm.booking.observe(viewLifecycleOwner) { binding.patient.text = it.patientName }',
    '    }',
    '}',
    c('BookingDetailFragment().apply { arguments = bundleOf("bookingId" to booking.id) }   // màn danh sách', 'BookingDetailFragment().apply { arguments = bundleOf("bookingId" to booking.id) }   // the list screen'),
    c('// thêm test: launchFragmentInContainer(...).recreate(), kiểm tên bệnh nhân vẫn hiện', '// add a test: launchFragmentInContainer(...).recreate(), check the patient name still shows')
  ]);

  /* l2: vòng lặp tính tổng phí trên luồng nền; breakpoint đặt ở dòng 5 */
  add('l2.loop', [
    'suspend fun monthlyTotal(bookings: List<Booking>): Long = withContext(Dispatchers.Default) {',
    '    var total = 0L',
    '    for ((i, b) in bookings.withIndex()) {',
    c('        val fee = b.base * (100 - b.discountPercent) / 100     // điều kiện: fee < 0', '        val fee = b.base * (100 - b.discountPercent) / 100     // condition: fee < 0'),
    c('        total += fee                                           // breakpoint ở đây', '        total += fee                                           // breakpoint here'),
    '    }',
    '    total',
    '}'
  ]);

  /* l3: log trong BookingRepo và Sync; dòng 3, 8 lộ số điện thoại; dòng 9 là bản sửa */
  add('l3.log', [
    'private const val TAG = "BookingRepo"',
    'suspend fun save(b: Booking) {',
    c('    Log.d(TAG, "saving booking for phone=${b.phone}")     // lộ số điện thoại', '    Log.d(TAG, "saving booking for phone=${b.phone}")     // leaks the phone number'),
    '    try { dao.insert(b) }',
    '    catch (e: SQLiteConstraintException) { Log.e(TAG, "save failed", e) }',
    '}',
    c('// SyncWorker', '// SyncWorker'),
    c('Log.w("Sync", "retry $n for phone=${b.phone}")              // mức W: R8 không xóa', 'Log.w("Sync", "retry $n for phone=${b.phone}")              // level W: R8 does not remove it'),
    c('Log.w("Sync", "retry $n for booking id=${b.id}")             // sửa: chỉ log id', 'Log.w("Sync", "retry $n for booking id=${b.id}")             // fix: log only the id')
  ]);

  /* l4: chỗ bọc ngoại lệ trong ViewModel (dòng 4–5) và chỗ đọc ngày (dòng 2) */
  add('l4.code', [
    c('fun requireBooking(dto: BookingDto): Booking = try {      // DetailViewModel.kt, dòng 55', 'fun requireBooking(dto: BookingDto): Booking = try {      // DetailViewModel.kt, line 55'),
    c('    mapper.toBooking(dto)                                   // BookingMapper.kt:22 gọi LocalDate.parse(dto.date)', '    mapper.toBooking(dto)                                   // BookingMapper.kt:22 calls LocalDate.parse(dto.date)'),
    '} catch (e: DateTimeParseException) {',
    c('    throw IllegalStateException("Booking not loaded", e)    // dòng 58: bọc lại, giữ e làm cause', '    throw IllegalStateException("Booking not loaded", e)    // line 58: wraps it, keeping e as the cause'),
    c('}                                                          // DetailActivity.onCreate gọi hàm này', '}                                                          // DetailActivity.onCreate calls this'),
    c('// dto.date = "2026-11-31" từ máy chủ', '// dto.date = "2026-11-31" from the server')
  ]);

  /* l5: tạo lớp thanh toán bằng tên (dòng 3), keep rule (dòng 8), hay bỏ reflection (dòng 9) */
  add('l5.code', [
    'object PaymentFactory {',
    '    fun create(name: String): PaymentMethod {',
    c('        val cls = Class.forName("vn.henkham.pay.$name")      // tìm lớp bằng tên: R8 không thấy', '        val cls = Class.forName("vn.henkham.pay.$name")      // finds a class by name: invisible to R8'),
    '        return cls.getDeclaredConstructor().newInstance() as PaymentMethod',
    '    }',
    '}',
    '// proguard-rules.pro',
    '-keep class vn.henkham.pay.** implements vn.henkham.pay.PaymentMethod { <init>(); }',
    c('// hoặc bỏ reflection: val makers = mapOf("MomoPayment" to ::MomoPayment, "CardPayment" to ::CardPayment)', '// or drop reflection: val makers = mapOf("MomoPayment" to ::MomoPayment, "CardPayment" to ::CardPayment)')
  ]);

  /* l6: màn đặt lịch; dòng 5 là nút, dòng 7 lớp phủ luôn có trong cây (alpha 0 vẫn nhận chạm), dòng 8 là bản sửa */
  add('l6.screen', [
    '@Composable fun BookScreen(state: BookState, onBook: () -> Unit) {',
    c('    Box(Modifier.fillMaxSize()) {                       // con khai báo sau được vẽ sau, nằm trên', '    Box(Modifier.fillMaxSize()) {                       // a child declared later is drawn later, on top'),
    '        Column(Modifier.padding(16.dp)) {',
    '            Text(stringResource(R.string.pick_time)); SlotGrid(state.slots)',
    '            Button(onClick = onBook) { Text(stringResource(R.string.book)) }',
    '        }',
    c('        LoadingOverlay(Modifier.alpha(if (state.loading) 1f else 0f))   // luôn trong cây, có clickable', '        LoadingOverlay(Modifier.alpha(if (state.loading) 1f else 0f))   // always in the tree, clickable'),
    c('        // sửa: if (state.loading) LoadingOverlay()        // chỉ có trong cây khi đang tải', '        // fix: if (state.loading) LoadingOverlay()        // in the tree only while loading')
  ]);

  /* l7: lưu lịch với status PENDING (dòng 1–2), truy vấn danh sách (dòng 4); chuỗi worker sai (dòng 6) và đã sửa (dòng 8–9) */
  add('l7.code', [
    c('suspend fun book(b: Booking) = dao.insert(b.copy(status = Status.PENDING))   // chờ máy chủ xác nhận', 'suspend fun book(b: Booking) = dao.insert(b.copy(status = Status.PENDING))   // waiting for server confirmation'),
    c('// danh sách sắp tới:', '// upcoming list:'),
    '@Query("SELECT * FROM booking WHERE status = \'CONFIRMED\' ORDER BY day")',
    c('fun confirmed(): Flow<List<Booking>>                    // sửa: status IN (\'PENDING\', \'CONFIRMED\')', 'fun confirmed(): Flow<List<Booking>>                    // fix: status IN (\'PENDING\', \'CONFIRMED\')'),
    c('// đồng bộ nền:', '// background sync:'),
    'workManager.beginWith(uploadPhotos).then(syncBookings).then(notifyUser).enqueue()   // uploadPhotos: UNMETERED',
    c('// sửa: hai chuỗi độc lập', '// fix: two independent chains'),
    'workManager.beginWith(syncBookings).then(notifyUser).enqueue()                       // CONNECTED',
    'workManager.enqueue(uploadPhotos)                                                    // UNMETERED'
  ]);

  /* l8: object toàn cục giữ listener (dòng 1–2), lambda giữ Activity (dòng 7), đăng ký (dòng 8), hủy trong onDestroy (dòng 9) */
  add('l8.code', [
    c('object BookingEventBus {                                   // object: sống suốt tiến trình', 'object BookingEventBus {                                   // object: lives as long as the process'),
    '    private val listeners = mutableListOf<(BookingEvent) -> Unit>()',
    '    fun register(l: (BookingEvent) -> Unit) { listeners += l }',
    '    fun unregister(l: (BookingEvent) -> Unit) { listeners -= l }',
    '}',
    'class DetailActivity : AppCompatActivity() {',
    c('    private val onEvent: (BookingEvent) -> Unit = { render(it) }  // lambda giữ this', '    private val onEvent: (BookingEvent) -> Unit = { render(it) }  // the lambda holds this'),
    '    override fun onCreate(s: Bundle?) { super.onCreate(s); BookingEventBus.register(onEvent) }',
    c('    override fun onDestroy() { BookingEventBus.unregister(onEvent); super.onDestroy() }  // sửa', '    override fun onDestroy() { BookingEventBus.unregister(onEvent); super.onDestroy() }  // fix'),
    '}'
  ]);

  /* l9: parse trên main lúc bind (dòng 3) và bản sửa parse trên luồng nền (dòng 8–9) */
  add('l9.code', [
    'override fun onBindViewHolder(h: BookingVH, pos: Int) {',
    c('    // gọi khi cuộn tới trang mới', '    // called when scrolling reaches a new page'),
    c('    val dto = trace("parseJson") { json.decodeFromString<PageDto>(rawPage) }   // trên luồng main: 28 ms', '    val dto = trace("parseJson") { json.decodeFromString<PageDto>(rawPage) }   // on the main thread: 28 ms'),
    '    h.bind(dto.items[pos % PAGE_SIZE])',
    '}',
    c('// sửa: parse trước, trên luồng nền', '// fix: parse beforehand, on a background thread'),
    'suspend fun loadPage(raw: String) {',
    '    val items = withContext(Dispatchers.Default) { trace("parseJson") { json.decodeFromString<PageDto>(raw).items } }',
    c('    adapter.submitList(adapter.currentList + items)           // main chỉ bind: 5 ms', '    adapter.submitList(adapter.currentList + items)           // main only binds: 5 ms')
  ]);

  /* l10: save và sync cùng khóa (dòng 3–5); bản sửa (dòng 9–10); StrictMode trong bản debug (dòng 12) */
  add('l10.code', [
    'object BookingRepo {',
    '    private val lock = Any()',
    c('    fun save(b: Booking) = synchronized(lock) { cache[b.id] = b; db.insert(b) }   // nút Lưu gọi trên main', '    fun save(b: Booking) = synchronized(lock) { cache[b.id] = b; db.insert(b) }   // Save calls it on main'),
    '    fun sync() = synchronized(lock) {',
    c('        val fresh = api.fetchAll()                    // mạng chậm: giữ khóa 9 giây', '        val fresh = api.fetchAll()                    // slow network: holds the lock for 9 s'),
    '        cache.putAll(fresh)',
    '    }',
    '}',
    c('// sửa: save chạy trong withContext(Dispatchers.IO); sync gọi mạng ngoài khóa', '// fix: save runs in withContext(Dispatchers.IO); sync calls the network outside the lock'),
    'fun sync() { val fresh = api.fetchAll(); synchronized(lock) { cache.putAll(fresh) } }',
    c('// Application.onCreate, chỉ bản debug:', '// Application.onCreate, debug builds only:'),
    'if (BuildConfig.DEBUG) StrictMode.setThreadPolicy(StrictMode.ThreadPolicy.Builder().detectAll().penaltyLog().build())'
  ]);
})();
