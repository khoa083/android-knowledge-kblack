/* Đoạn mã track G (minh họa, rút gọn; không chạy trong trang). Số dòng được tham chiếu bởi codeHighlight trong models/models.js. */
(function () {
  var add = function (id, lines) { ADE.addCode('arch', id, { lang: 'kotlin', illustrative: true, lines: lines }); };
  var c = function (vi, en) { return { vi: vi, en: en }; };
  add('g1.god', [
    'class ChooseTimeActivity : ComponentActivity() {',
    c('    private var slots: List<Slot> = emptyList()      // dữ liệu nằm trong Activity', '    private var slots: List<Slot> = emptyList()      // data lives in the Activity'),
    '    fun onBookClick(day: LocalDate) = lifecycleScope.launch {',
    c('        val json = http.get("/slots?day=$day")        // gọi mạng', '        val json = http.get("/slots?day=$day")        // network call'),
    c('        slots = parseSlots(json)                      // tự parse JSON', '        slots = parseSlots(json)                      // parses JSON itself'),
    c('        prefs.edit { putString("cache", json) }       // tự lưu cache', '        prefs.edit { putString("cache", json) }       // caches it itself'),
    c('        render(slots)                                 // cập nhật UI', '        render(slots)                                 // updates the UI'),
    '    }',
    '}'
  ]);
  add('g1.layered', [
    'class ChooseTimeActivity : ComponentActivity() {',
    '    private val vm: ChooseTimeViewModel by viewModels()',
    c('    // UI chỉ gửi sự kiện và vẽ state', '    // the UI only sends events and draws state'),
    '}',
    'class ChooseTimeViewModel(private val repo: SlotRepository) : ViewModel() {',
    '    val state = MutableStateFlow<UiState>(UiState.Loading)',
    '}',
    'class SlotRepository(private val remote: SlotApi, private val local: SlotDao) { … }',
    c('class SlotApi { fun slots(day: LocalDate): List<SlotDto> = … }   // chỉ nơi này biết JSON', 'class SlotApi { fun slots(day: LocalDate): List<SlotDto> = … }   // the only place that knows the JSON'),
    c('// kiểm thử trên máy, không cần thiết bị:', '// tested on your machine, no device needed:'),
    'val vm = ChooseTimeViewModel(FakeSlotRepository(listOf(slot9h)))',
    'vm.load(today); assertEquals(UiState.Success(listOf(slot9h)), vm.state.value)'
  ]);
  add('g2.google', [
    c('// :feature:slots', '// :feature:slots'),
    c('class ChooseTimeScreen(vm: ChooseTimeViewModel)                          // UI biết ViewModel', 'class ChooseTimeScreen(vm: ChooseTimeViewModel)                          // the UI knows the ViewModel'),
    c('class ChooseTimeViewModel(getSlots: GetFreeSlotsUseCase) : ViewModel()   // ViewModel biết use case', 'class ChooseTimeViewModel(getSlots: GetFreeSlotsUseCase) : ViewModel()   // the ViewModel knows the use case'),
    c('// :core:domain (tùy chọn)', '// :core:domain (optional)'),
    c('class GetFreeSlotsUseCase(private val repo: SlotRepository)            // domain biết data', 'class GetFreeSlotsUseCase(private val repo: SlotRepository)            // domain knows data'),
    '// :core:data',
    'class SlotRepository(private val api: SlotApi, private val dao: SlotDao) {',
    c('    fun slots(day: LocalDate): Flow<List<Slot>> = dao.observe(day)     // dữ liệu đi ngược lên', '    fun slots(day: LocalDate): Flow<List<Slot>> = dao.observe(day)     // data flows back up'),
    '}',
    c('// test chạy trên máy (JVM): repository chỉ cần hai bản giả', '// tested on your machine (JVM): the repository needs only two fakes'),
    'val repo = SlotRepository(FakeSlotApi(), FakeSlotDao())'
  ]);
  add('g2.wrong', [
    c('// tất cả trong một module :app', '// everything in one module, :app'),
    c('import com.henkham.ui.slots.SlotChipUi                 // lớp của màn hình', 'import com.henkham.ui.slots.SlotChipUi                 // a screen class'),
    'class SlotRepository(private val api: SlotApi, private val context: Context) {',
    '    fun chips(day: LocalDate): List<SlotChipUi> =',
    '        api.slots(day).map { SlotChipUi(context.getString(R.string.slot_at, it.start)) }',
    '}',
    c('// build: vẫn qua. Trong một module, lớp public nào cũng import được', '// build: still passes. Within one module, any public class can be imported'),
    c('// test repository giờ cần Context và tài nguyên Android', '// testing the repository now needs a Context and Android resources')
  ]);
  add('g2.modules', [
    c('// core/data/build.gradle.kts: data không phụ thuộc feature', '// core/data/build.gradle.kts: data does not depend on feature'),
    'dependencies { implementation(libs.room.runtime) }',
    c('import com.henkham.feature.slots.SlotChipUi        // lỗi: Unresolved reference', 'import com.henkham.feature.slots.SlotChipUi        // error: Unresolved reference'),
    'class SlotRepository(…) { fun chips(day: LocalDate): List<SlotChipUi> = … }',
    c('// "sửa" sai: thêm phụ thuộc vào core/data/build.gradle.kts', '// the wrong "fix": add a dependency in core/data/build.gradle.kts'),
    c('implementation(project(":feature:slots"))   // mà :feature:slots → :core:domain → :core:data', 'implementation(project(":feature:slots"))   // but :feature:slots → :core:domain → :core:data'),
    c('// Gradle báo phụ thuộc vòng và không build', '// Gradle reports a circular dependency and does not build'),
    c('// sửa đúng: repository trả Slot; ViewModel đổi Slot thành SlotChipUi', '// the right fix: the repository returns Slot; the ViewModel turns Slot into SlotChipUi'),
    'val chips = repo.slots(day).map { list -> list.map { it.toChip(resources) } }'
  ]);
  add('g2.inverted', [
    c('// :core:domain: Kotlin thuần, không phụ thuộc module nào', '// :core:domain: plain Kotlin, depends on no module'),
    'interface SlotRepository { fun slots(day: LocalDate): Flow<List<Slot>> }',
    c('class GetFreeSlotsUseCase(private val repo: SlotRepository)   // chỉ biết interface', 'class GetFreeSlotsUseCase(private val repo: SlotRepository)   // knows only the interface'),
    c('// :core:data phụ thuộc :core:domain (mũi tên đổi chiều)', '// :core:data depends on :core:domain (the arrow flips)'),
    'class OfflineFirstSlotRepository(api: SlotApi, dao: SlotDao) : SlotRepository { … }',
    c('// module app nối hai bên (chương G6)', '// the app module wires the two together (chapter G6)'),
    '@Binds abstract fun bind(impl: OfflineFirstSlotRepository): SlotRepository'
  ]);
  add('g2.twowriters', [
    c('class BookingRepository { val bookings = mutableListOf<Booking>() }   // ai cũng sửa được', 'class BookingRepository { val bookings = mutableListOf<Booking>() }   // anyone can change it'),
    'class ChooseTimeViewModel(private val repo: BookingRepository) : ViewModel() {',
    '    private val mine = mutableListOf<Booking>(); fun book(s: Slot) { mine += Booking(s); repo.bookings += Booking(s) } }',
    c('class MyBookingsViewModel(private val repo: BookingRepository) : ViewModel() { val list = repo.bookings.toList()   // bản chụp lúc mở', 'class MyBookingsViewModel(private val repo: BookingRepository) : ViewModel() { val list = repo.bookings.toList()   // a snapshot taken on open'),
    c('    fun cancel(b: Booking) { repo.bookings -= b } }                      // màn Chọn giờ không biết', '    fun cancel(b: Booking) { repo.bookings -= b } }                      // Choose a time never hears of it')
  ]);
  add('g2.ssot', [
    'class BookingRepository(private val dao: BookingDao) {',
    c('    val bookings: Flow<List<Booking>> = dao.observeAll()        // chỉ đọc, bất biến', '    val bookings: Flow<List<Booking>> = dao.observeAll()        // read-only, immutable'),
    c('    suspend fun book(slot: Slot) = dao.insert(Booking(slot))      // chỉ sửa qua đây', '    suspend fun book(slot: Slot) = dao.insert(Booking(slot))      // changes go through here only'),
    '    suspend fun cancel(id: Long) = dao.delete(id)',
    '}',
    'class ChooseTimeViewModel(private val repo: BookingRepository) : ViewModel() { fun onBook(s: Slot) = viewModelScope.launch { repo.book(s) } }',
    'class MyBookingsViewModel(private val repo: BookingRepository) : ViewModel() { val state = repo.bookings.stateIn(viewModelScope, WhileSubscribed(5_000), emptyList()) }',
    c('// hai màn hình đọc cùng một nguồn: sự kiện đi lên, state đi xuống', '// both screens read the same source: events go up, state comes down')
  ]);
  add('g3.sticky', [
    'class BookingViewModel(private val repo: BookingRepository) : ViewModel() {',
    '    val state = MutableStateFlow(BookingState())',
    '    fun book(slot: Slot) = viewModelScope.launch { repo.book(slot); state.update { it.copy(showSuccess = true) } }',
    '}',
    c('// Activity (trong repeatOnLifecycle(STARTED)): mỗi lần nhận showSuccess = true thì hiện Toast', '// Activity (inside repeatOnLifecycle(STARTED)): show a Toast whenever showSuccess = true arrives'),
    'vm.state.collect { if (it.showSuccess) Toast.makeText(this, R.string.booked, Toast.LENGTH_SHORT).show() }'
  ]);
  add('g3.shared', [
    'class BookingViewModel(private val repo: BookingRepository) : ViewModel() {',
    c('    val events = MutableSharedFlow<String>()           // không replay, không buffer', '    val events = MutableSharedFlow<String>()           // no replay, no buffer'),
    '    fun book(slot: Slot) = viewModelScope.launch {',
    c('        repo.book(slot); events.emit("booked")         // không ai thu thập: trả về ngay, giá trị bị bỏ', '        repo.book(slot); events.emit("booked")         // nobody collecting: returns at once, the value is dropped'),
    '    }',
    '}',
    c('// Activity mới bắt đầu thu thập sau khi emit đã xảy ra: không nhận được gì', '// the new Activity starts collecting after the emit happened: it receives nothing')
  ]);
  add('g3.state', [
    'data class BookingState(val slots: List<Slot> = emptyList(), val userMessage: String? = null)',
    'class BookingViewModel(private val repo: BookingRepository) : ViewModel() {',
    '    val state = MutableStateFlow(BookingState())',
    c('    fun messageShown() = state.update { it.copy(userMessage = null) }   // UI báo: đã hiện xong', '    fun messageShown() = state.update { it.copy(userMessage = null) }   // the UI reports: shown'),
    '    fun book(slot: Slot) = viewModelScope.launch { repo.book(slot); state.update { it.copy(userMessage = "booked") } } }',
    '// UI (Compose)',
    'state.userMessage?.let { msg -> LaunchedEffect(msg) { snackbarHostState.showSnackbar(msg)',
    '    vm.messageShown() } }'
  ]);
  add('g4.mixed', [
    'class SlotRepository(private val api: SlotApi, private val dao: SlotDao) {',
    c('    fun slots(day: LocalDate): Flow<List<Slot>> = dao.observe(day)      // mở màn: đọc DB', '    fun slots(day: LocalDate): Flow<List<Slot>> = dao.observe(day)      // screen opens: read the DB'),
    c('    suspend fun refresh(day: LocalDate): List<Slot> = api.slots(day)    // trả thẳng kết quả mạng', '    suspend fun refresh(day: LocalDate): List<Slot> = api.slots(day)    // hands back the network result'),
    '}',
    c('// ViewModel: hiện kết quả refresh, nhưng DB vẫn giữ bản cũ', '// ViewModel: shows the refresh result, but the DB still holds the old copy'),
    'fun onRefresh() = viewModelScope.launch { state.update { it.copy(slots = repo.refresh(day)) } }',
    c('// mở lại màn, hay màn khác đọc dao.observe(day): thấy bản cũ', '// reopen the screen, or another screen reading dao.observe(day): sees the old copy')
  ]);
  add('g4.ssot', [
    'class OfflineFirstSlotRepository(private val api: SlotApi, private val dao: SlotDao) {',
    c('    fun slots(day: LocalDate): Flow<List<Slot>> = dao.observe(day)      // chỉ đọc từ DB', '    fun slots(day: LocalDate): Flow<List<Slot>> = dao.observe(day)      // reads only from the DB'),
    '    suspend fun refresh(day: LocalDate) {',
    c('        val fresh = api.slots(day)                                      // có thể ném lỗi khi mất mạng', '        val fresh = api.slots(day)                                      // may throw when offline'),
    c('        dao.replace(day, fresh)                                         // ghi vào DB; DB báo cho mọi người đọc', '        dao.replace(day, fresh)                                         // write to the DB; the DB notifies every reader'),
    '    }',
    '}',
    'val slots = repo.slots(day).stateIn(viewModelScope, SharingStarted.WhileSubscribed(5_000), emptyList())'
  ]);
  add('g4.lazy', [
    'suspend fun cancel(id: Long) {',
    c('    dao.markCancelled(id, pending = true)                 // ghi DB trước: UI thấy ngay', '    dao.markCancelled(id, pending = true)                 // write the DB first: the UI sees it at once'),
    c('    WorkManager.getInstance(context).enqueueUniqueWork(   // xếp việc đồng bộ, chạy khi có mạng', '    WorkManager.getInstance(context).enqueueUniqueWork(   // queue the sync, runs when online'),
    '        "sync-cancel-$id", ExistingWorkPolicy.KEEP,',
    '        OneTimeWorkRequestBuilder<SyncCancelWorker>().setConstraints(onlineOnly).build())',
    '}',
    c('// SyncCancelWorker: gọi api.cancel(id); xong thì dao.clearPending(id), lỗi thì Result.retry()', '// SyncCancelWorker: calls api.cancel(id); on success dao.clearPending(id), on failure Result.retry()')
  ]);
  add('g5.duplicated', [
    'class ChooseTimeViewModel(private val repo: SlotRepository) : ViewModel() {',
    '    fun bookable(s: Slot, now: LocalDateTime) = s.start > now && s.start.hour in 7..17 && ChronoUnit.MINUTES.between(now, s.start) >= 120',
    '}',
    'class RescheduleViewModel(private val repo: SlotRepository) : ViewModel() {',
    c('    fun bookable(s: Slot, now: LocalDateTime) = s.start > now && s.start.hour in 7..17 && ChronoUnit.MINUTES.between(now, s.start) >= 60  // bản chép cũ', '    fun bookable(s: Slot, now: LocalDateTime) = s.start > now && s.start.hour in 7..17 && ChronoUnit.MINUTES.between(now, s.start) >= 60  // the old copy'),
    '}',
    c('// 8:00 xem giờ 9:30: màn Chọn giờ nói không, màn Đổi lịch nói có', '// at 8:00 looking at 9:30: Choose a time says no, Reschedule says yes')
  ]);
  add('g5.shared', [
    'class IsSlotBookableUseCase(private val clock: Clock) {',
    '    operator fun invoke(s: Slot): Boolean { val now = LocalDateTime.now(clock)',
    '        return s.start > now && s.start.hour in 7..17 && ChronoUnit.MINUTES.between(now, s.start) >= 120 }',
    '}',
    'class ChooseTimeViewModel(private val isBookable: IsSlotBookableUseCase) : ViewModel()',
    'class RescheduleViewModel(private val isBookable: IsSlotBookableUseCase) : ViewModel()',
    c('// test một lần, với đồng hồ cố định lúc 8:00', '// test once, with a clock fixed at 8:00'),
    'val uc = IsSlotBookableUseCase(Clock.fixed(at8am, zone)); assertFalse(uc(slot930))'
  ]);
  add('g5.passthrough', [
    'class GetSlotsUseCase(private val repo: SlotRepository) {',
    c('    operator fun invoke(day: LocalDate) = repo.slots(day)   // chỉ chuyển tiếp', '    operator fun invoke(day: LocalDate) = repo.slots(day)   // only forwards'),
    '}',
    'class ChooseTimeViewModel(private val getSlots: GetSlotsUseCase) : ViewModel()',
    c('// không thêm quy tắc nào: bỏ use case, ViewModel nhận thẳng repository', '// adds no rule: drop the use case, the ViewModel takes the repository directly'),
    'class ChooseTimeViewModel(private val repo: SlotRepository) : ViewModel()'
  ]);
})();
