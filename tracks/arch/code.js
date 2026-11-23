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
  add('g6.manual', [
    'class ChooseTimeViewModel : ViewModel() {',
    c('    private val repo = SlotRepository(SlotApi(), Room.databaseBuilder(app, AppDatabase::class.java, "app.db").build())', '    private val repo = SlotRepository(SlotApi(), Room.databaseBuilder(app, AppDatabase::class.java, "app.db").build())'),
    c('class RescheduleViewModel : ViewModel() {   // chép cùng dòng tạo', 'class RescheduleViewModel : ViewModel() {   // copies the same construction'),
    '    private val repo = SlotRepository(SlotApi(), Room.databaseBuilder(app, AppDatabase::class.java, "app.db").build())',
    c('// repository #1 cache "9:30 đã đặt"; repository #2 vẫn cache cũ', '// repository #1 caches "9:30 booked"; repository #2 still has the old cache'),
    c('class AppContainer(app: Application) {      // container dùng chung, đặt trong Application', 'class AppContainer(app: Application) {      // shared container, held by the Application'),
    '    val slotRepository by lazy { SlotRepository(SlotApi(), AppDatabase.create(app)) } }',
    'class ClinicApp : Application() { val container by lazy { AppContainer(this) } }'
  ]);
  add('g6.hilt', [
    '@HiltAndroidApp class ClinicApp : Application()',
    '@Singleton',
    'class SlotRepository @Inject constructor(private val api: SlotApi, private val dao: SlotDao)',
    '@HiltViewModel',
    'class ChooseTimeViewModel @Inject constructor(private val repo: SlotRepository) : ViewModel()',
    c('class RescheduleViewModel @Inject constructor(private val repo: SlotRepository) : ViewModel()   // cùng instance', 'class RescheduleViewModel @Inject constructor(private val repo: SlotRepository) : ViewModel()   // the same instance'),
    '@AndroidEntryPoint class ChooseTimeActivity : ComponentActivity() {',
    '    private val vm: ChooseTimeViewModel by viewModels() }'
  ]);
  add('g6.leak', [
    c('object AppContainer {                        // object: sống suốt tiến trình', 'object AppContainer {                        // object: lives for the whole process'),
    '    lateinit var repo: SlotRepository }',
    c('// trong ChooseTimeActivity.onCreate: AppContainer.repo = SlotRepository(this)   // this = Activity', '// in ChooseTimeActivity.onCreate: AppContainer.repo = SlotRepository(this)   // this = the Activity'),
    c('// xoay màn hình: Activity #1 bị hủy, nhưng AppContainer.repo vẫn giữ nó', '// rotate: Activity #1 is destroyed, but AppContainer.repo still holds it'),
    '@Singleton class SlotRepository @Inject constructor(',
    c('    @ApplicationContext private val context: Context)   // context của Application, sống cùng singleton', '    @ApplicationContext private val context: Context)   // the Application context, lives as long as the singleton'),
    c('// thử: @Singleton class SlotRepository @Inject constructor(private val activity: Activity)', '// try: @Singleton class SlotRepository @Inject constructor(private val activity: Activity)'),
    c('// Hilt báo lỗi khi biên dịch: SingletonComponent không có binding Activity', '// Hilt fails at compile time: SingletonComponent has no Activity binding')
  ]);
  add('g7.streams', [
    'val isLoading = MutableStateFlow(false)',
    'val error = MutableStateFlow<String?>(null)',
    'val appointments = MutableStateFlow<List<Appt>>(emptyList())',
    'fun load() = viewModelScope.launch {',
    '    isLoading.value = true',
    '    try { appointments.value = repo.load(); isLoading.value = false }',
    c('    catch (e: IOException) { error.value = "Mất mạng" }   // quên isLoading = false; thành công thì quên xóa lỗi', '    catch (e: IOException) { error.value = "Offline" }    // forgets isLoading = false; on success forgets to clear the error'),
    '}'
  ]);
  add('g7.single', [
    'data class ApptUiState(val isLoading: Boolean = false, val error: String? = null, val items: List<Appt> = emptyList())',
    'val state = MutableStateFlow(ApptUiState())',
    'fun load() = viewModelScope.launch {',
    '    state.update { it.copy(isLoading = true, error = null) }',
    '    val items = try { repo.load() } catch (e: IOException) { null }',
    c('    state.update { if (items != null) it.copy(isLoading = false, items = items) else it.copy(isLoading = false, error = "Mất mạng") } }', '    state.update { if (items != null) it.copy(isLoading = false, items = items) else it.copy(isLoading = false, error = "Offline") } }'),
    c('// một luồng, mỗi thay đổi là một lần cập nhật; nhưng kiểu vẫn cho phép isLoading = true cùng error != null', '// one stream, one update per change; but the type still allows isLoading = true with error != null')
  ]);
  add('g7.mvi', [
    'sealed interface ApptState { data object Loading : ApptState; data class Content(val items: List<Appt>) : ApptState',
    '    data class Refreshing(val items: List<Appt>) : ApptState; data class Error(val message: String) : ApptState }',
    'sealed interface ApptIntent { data object Load : ApptIntent; data object Retry : ApptIntent }',
    'sealed interface ApptResult { data class Loaded(val items: List<Appt>) : ApptResult; data class Failed(val message: String) : ApptResult }',
    'fun reduce(s: ApptState, r: ApptResult): ApptState = when (r) {',
    '    is ApptResult.Loaded -> ApptState.Content(r.items)',
    '    is ApptResult.Failed -> ApptState.Error(r.message) }',
    'fun onIntent(i: ApptIntent) = viewModelScope.launch { state.value = ApptState.Loading',
    c('    val r = try { ApptResult.Loaded(repo.load()) } catch (e: IOException) { ApptResult.Failed("Mất mạng") }; state.value = reduce(state.value, r) }', '    val r = try { ApptResult.Loaded(repo.load()) } catch (e: IOException) { ApptResult.Failed("Offline") }; state.value = reduce(state.value, r) }')
  ]);
  add('g8.raw', [
    c('class SlotRepository(private val api: SlotApi) { suspend fun book(s: Slot) = api.book(s) }   // ném gì ném nấy', 'class SlotRepository(private val api: SlotApi) { suspend fun book(s: Slot) = api.book(s) }   // throws whatever it gets'),
    'fun onBook(s: Slot) = viewModelScope.launch {',
    c('    repo.book(s)                                       // IOException không ai bắt: app crash', '    repo.book(s)                                       // nobody catches the IOException: the app crashes'),
    '}',
    c('// "sửa" vội: bắt tất cả, hiện nguyên message', '// a hasty "fix": catch everything, show the raw message'),
    'fun onBook(s: Slot) = viewModelScope.launch { try { repo.book(s) } catch (e: Exception) { state.update { it.copy(userMessage = e.message) } } }',
    c('// người dùng thấy "HTTP 500 Internal Server Error"; lỗi lập trình (NPE) cũng bị nuốt', '// the user sees "HTTP 500 Internal Server Error"; programming errors (NPE) are swallowed too')
  ]);
  add('g8.mapped', [
    'sealed interface BookingFailure { data object Offline : BookingFailure; data object SlotTaken : BookingFailure; data object ServerProblem : BookingFailure }',
    'sealed interface BookResult { data object Booked : BookResult; data class Failed(val reason: BookingFailure) : BookResult }',
    'suspend fun book(s: Slot): BookResult = try { api.book(s); BookResult.Booked }',
    '    catch (e: IOException) { BookResult.Failed(BookingFailure.Offline) }',
    '    catch (e: HttpException) { BookResult.Failed(if (e.code() == 409) BookingFailure.SlotTaken else BookingFailure.ServerProblem) }',
    c('// ViewModel: đổi failure thành câu cho người dùng (chuỗi trong tài nguyên)', '// ViewModel: turn the failure into a sentence for the user (a string resource)'),
    'is BookResult.Failed -> state.update { it.copy(userMessage = messageFor(r.reason)) }',
    c('// NullPointerException không bị bắt ở đây: đó là lỗi lập trình, để crash report ghi lại', '// NullPointerException is not caught here: it is a programming error, let crash reporting record it')
  ]);
  add('g8.swallow', [
    'suspend fun slots(day: LocalDate): List<Slot> = try { api.slots(day) }',
    c('    catch (e: Exception) { emptyList() }               // mất mạng thành "không có giờ trống"', '    catch (e: Exception) { emptyList() }               // offline becomes "no free slots"'),
    'suspend fun book(s: Slot): Boolean = try { api.book(s); true } catch (e: Exception) { false }',
    c('// rời màn hình: viewModelScope bị hủy, CancellationException cũng bị bắt ở đây', '// leaving the screen: viewModelScope is cancelled, and CancellationException is caught here too'),
    c('// nên mã sau đó vẫn chạy như chưa bị hủy', '// so the code after it keeps running as if nothing was cancelled'),
    c('// NullPointerException trong api.slots bị nuốt: không có crash report nào', '// a NullPointerException in api.slots is swallowed: no crash report at all')
  ]);
  add('g9.features', [
    '// settings.gradle.kts: include(":app", ":feature:booking", ":feature:history", ":core:data")',
    c('// :app phụ thuộc hai feature; mỗi feature phụ thuộc :core:data', '// :app depends on both features; each feature depends on :core:data'),
    'dependencies { implementation(project(":core:data")) }',
    c('// feature/booking: muốn mở màn Lịch sử nên thêm implementation(project(":feature:history"))', '// feature/booking: wants to open History, so adds implementation(project(":feature:history"))'),
    c('// feature/history: muốn "đặt lại" nên thêm implementation(project(":feature:booking"))', '// feature/history: wants "book again", so adds implementation(project(":feature:booking"))'),
    c('// Gradle: hai project phụ thuộc vòng, không build được', '// Gradle: the two projects depend on each other in a cycle; no build'),
    c('// sửa: :app giữ navigation graph và làm trung gian; feature chỉ truyền id', '// fix: :app owns the navigation graph and mediates; features pass only ids'),
    'navController.navigate("history/$patientId")'
  ]);
  add('g9.visibility', [
    c('// :core:data — SlotRepository là giao diện công khai của module', '// :core:data — SlotRepository is the module\'s public interface'),
    'class SlotRepository(private val dao: SlotDao) { … }',
    c('@Dao interface SlotDao { … }                      // mặc định public: module khác dùng được', '@Dao interface SlotDao { … }                      // public by default: other modules can use it'),
    c('// :feature:booking dùng thẳng SlotDao, bỏ qua repository', '// :feature:booking uses SlotDao directly, bypassing the repository'),
    '@Dao internal interface SlotDao { … }',
    c('// :feature:booking: lỗi biên dịch, SlotDao là internal của :core:data', '// :feature:booking: compile error, SlotDao is internal to :core:data'),
    'class SlotRepository internal constructor(private val dao: SlotDao) { … }'
  ]);
  add('g9.abstraction', [
    c('// :core:data gồm cả interface và cài đặt (Room, Retrofit)', '// :core:data holds both the interface and the implementation (Room, Retrofit)'),
    c('// :feature:booking phụ thuộc :core:data, nên phụ thuộc cả chi tiết cài đặt', '// :feature:booking depends on :core:data, so on implementation details too'),
    c('// tách: :core:data-api (interface SlotRepository, mô hình) và :core:data-impl (Room, Retrofit)', '// split: :core:data-api (SlotRepository interface, models) and :core:data-impl (Room, Retrofit)'),
    c('// :core:data-impl phụ thuộc :core:data-api', '// :core:data-impl depends on :core:data-api'),
    c('// :feature:booking chỉ phụ thuộc :core:data-api', '// :feature:booking depends only on :core:data-api'),
    c('// :app phụ thuộc :core:data-impl và nối DI (@Binds, chương G6)', '// :app depends on :core:data-impl and wires DI (@Binds, chapter G6)'),
    c('// đổi mã Room trong data-impl: :feature:booking không phụ thuộc module đó', '// changing Room code in data-impl: :feature:booking does not depend on that module')
  ]);
  add('g10.real', [
    '@Test fun booking_showsSlots() = runTest {',
    c('    val vm = BookingViewModel(SlotRepository(RetrofitSlotApi(BASE_URL), realDao))   // mạng thật', '    val vm = BookingViewModel(SlotRepository(RetrofitSlotApi(BASE_URL), realDao))   // the real network'),
    '    vm.load(today)',
    c('    assertEquals(2, vm.state.value.slots.size)        // hôm nay 2 giờ trống; mai có thể khác', '    assertEquals(2, vm.state.value.slots.size)        // 2 free slots today; tomorrow may differ'),
    '}',
    c('// mất mạng, máy chủ chậm, dữ liệu đổi: test lúc qua lúc trượt', '// offline, a slow server, changed data: the test passes or fails at random')
  ]);
  add('g10.fakes', [
    c('class FakeSlotRepository : SlotRepository {          // trong source set test', 'class FakeSlotRepository : SlotRepository {          // in the test source set'),
    '    val slots = MutableStateFlow(listOf(slot9h, slot930))',
    '    override fun slots(day: LocalDate) = slots }',
    '@Test fun booking_showsSlots() = runTest {',
    '    val vm = BookingViewModel(FakeSlotRepository()); vm.load(today)',
    c('    assertEquals(2, vm.state.value.slots.size) }      // chạy trên JVM, rất nhanh, luôn cùng kết quả', '    assertEquals(2, vm.state.value.slots.size) }      // runs on the JVM, fast, same result every time'),
    c('// repository: FakeSlotApi + FakeSlotDao; DAO: Room.inMemoryDatabaseBuilder trên thiết bị hay Robolectric', '// repository: FakeSlotApi + FakeSlotDao; DAO: Room.inMemoryDatabaseBuilder on a device or Robolectric'),
    c('// UI: createComposeRule(), ViewModel nhận repository giả', '// UI: createComposeRule(), the ViewModel gets a fake repository')
  ]);
  add('g11.rewrite', [
    c('// nhánh "rewrite": viết lại cả app theo kiến trúc mới, đóng băng tính năng', '// a "rewrite" branch: rebuild the whole app on the new architecture, freeze features'),
    c('git switch -c rewrite', 'git switch -c rewrite'),
    c('// nhánh chính vẫn phải sửa lỗi gấp cho người dùng: hai nơi cùng đổi', '// main still needs urgent fixes for users: two places change at once'),
    c('// nhánh chính thêm Thanh toán theo yêu cầu kinh doanh; nhánh rewrite chưa có', '// main adds Payment for business reasons; the rewrite branch lacks it'),
    c('// sau nhiều tháng: nhánh rewrite chưa phát hành được, bị bỏ dở', '// months later: the rewrite branch still cannot ship and is abandoned')
  ]);
  add('g11.gradual', [
    c('// 1. test cho màn Lịch sử: người dùng thấy gì, làm được gì', '// 1. tests for the History screen: what the user sees, what they can do'),
    '@Test fun history_showsVisits() = runTest { … }; @Test fun history_cancelRemovesVisit() = runTest { … }',
    c('// 2. đặt repository sau interface, rút logic ra use case', '// 2. put the repository behind an interface, move logic into use cases'),
    'interface VisitHistoryRepository { fun visits(): Flow<List<Visit>> }',
    'class GetVisitHistoryUseCase(private val repo: VisitHistoryRepository) { operator fun invoke() = repo.visits() }',
    c('// 3. HistoryViewModel dùng use case; test cũ vẫn qua; phát hành', '// 3. HistoryViewModel uses the use case; the old tests still pass; ship'),
    c('// 4. lặp lại cho từng màn, mỗi lần một bản phát hành', '// 4. repeat for each screen, one release at a time')
  ]);
  add('g11.newfeature', [
    c('// domain: tính năng Hủy lịch bắt đầu từ use case và interface repository', '// domain: the Cancel appointment feature starts with the use case and repository interface'),
    'interface CancelAppointmentRepository { suspend fun cancel(id: Long): CancelResult }',
    'class CancelAppointmentUseCase(private val repo: CancelAppointmentRepository) { suspend operator fun invoke(id: Long) = repo.cancel(id) }',
    c('// presentation: ViewModel và UiState, chạy được ngay với repository stub', '// presentation: ViewModel and UiState, runnable right away with a stub repository'),
    'class StubCancelRepository : CancelAppointmentRepository { override suspend fun cancel(id: Long) = CancelResult.Cancelled }',
    c('// UI: nút Hủy và hộp xác nhận; thử được tính năng dù chưa có máy chủ', '// UI: the Cancel button and confirmation dialog; the feature can be tried before the server exists'),
    c('// data: cài đặt thật (Room + API), thay stub; nối điều hướng', '// data: the real implementation (Room + API) replaces the stub; wire navigation'),
    'class OfflineFirstCancelRepository(private val api: AppointmentApi, private val dao: AppointmentDao) : CancelAppointmentRepository { … }'
  ]);
})();
