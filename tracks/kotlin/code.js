/* Đoạn mã track F. Giá trị in ra theo tài liệu kotlinlang.org (Numbers, Conditions and loops), không chạy thật trong trang.
   Số dòng được tham chiếu bởi codeHighlight trong models/models.js. */
(function () {
  var add = function (id, lines) { ADE.addCode('kotlin', id, { lang: 'kotlin', lines: lines }); };
  var c = function (vi, en) { return { vi: vi, en: en }; };
  add('eval.intdiv', [
    'val total = 7 + 8',
    'val avg = total / 2',
    'println(avg)   // 7'
  ]);
  add('eval.double', [
    'val total = 7 + 8',
    'val avg = total / 2.0',
    'println(avg)   // 7.5'
  ]);
  add('eval.overflow', [
    'val max = Int.MAX_VALUE        // 2147483647',
    'val next = max + 1',
    'println(next)  // -2147483648',
    c('val safe = max.toLong() + 1  // 2147483648 (Long)', 'val safe = max.toLong() + 1  // 2147483648 (Long)')
  ]);
  /* K2: smart cast — năm loại biến (điều kiện theo trang Type checks and casts; platform type theo Calling Java from Kotlin) */
  add('smart.localVal', [
    'fun nameLength(user: User): Int {',
    '    val name = user.name              // String?',
    '    if (name != null) {',
    '        return name.length            // smart cast: String',
    '    }',
    '    return 0',
    '}',
    c('// gọn hơn: return user.name?.length ?: 0', '// shorter: return user.name?.length ?: 0')
  ]);
  add('smart.varProp', [
    'class User(var name: String?)',
    'fun nameLength(user: User): Int {',
    '    if (user.name != null) {',
    c('        return user.name.length       // LỖI biên dịch: không smart cast được', '        return user.name.length       // COMPILE ERROR: no smart cast'),
    '    }',
    '    return 0',
    '}',
    c('// sửa: val name = user.name rồi kiểm name, hoặc user.name?.length ?: 0', '// fix: val name = user.name then check name, or user.name?.length ?: 0')
  ]);
  add('smart.openProp', [
    'open class Patient { open val name: String? = null }',
    'fun greet(p: Patient): String {',
    '    if (p.name != null) {',
    c('        return p.name.uppercase()     // LỖI biên dịch: property open', '        return p.name.uppercase()     // COMPILE ERROR: open property'),
    '    }',
    '    return ""',
    '}',
    c('// sửa: val name = p.name; if (name != null) return name.uppercase()', '// fix: val name = p.name; if (name != null) return name.uppercase()')
  ]);
  add('smart.lambdaVar', [
    'var note: String? = load()',
    c('val reset = { note = null }           // lambda SỬA note', 'val reset = { note = null }           // the lambda MODIFIES note'),
    'if (note != null) {',
    c('    println(note.length)              // LỖI biên dịch: note bị lambda sửa', '    println(note.length)              // COMPILE ERROR: modified by a lambda'),
    '}',
    c('// sửa: val current = note; if (current != null) println(current.length)', '// fix: val current = note; if (current != null) println(current.length)')
  ]);
  add('smart.platform', [
    c('// Java, không có chú thích nullability: public String getTitle()', '// Java, no nullability annotation: public String getTitle()'),
    c('val title = legacy.title               // kiểu String! (platform type)', 'val title = legacy.title               // type String! (platform type)'),
    c('println(title.length)                  // biên dịch được; NPE nếu title là null', 'println(title.length)                  // compiles; NPE if title is null'),
    c('// sửa: val title: String? = legacy.title rồi xử lý null', '// fix: val title: String? = legacy.title, then handle null'),
    c('// hoặc thêm @Nullable/@NonNull ở phía Java', '// or add @Nullable/@NonNull on the Java side')
  ]);
  /* K3: thứ tự khởi tạo (Inheritance: Derived class initialization order; Classes: Initializer blocks; Object declarations; Properties: lateinit) */
  add('init.order', [
    'open class Entity(val id: String) {',
    '    init { println("1. Entity.init") }',
    '    open val tag: String = "E-$id".also { println("2. Entity.tag") }',
    '}',
    'class Appointment(id: String, val doctor: String) : Entity(id.uppercase()) {',
    '    init { println("3. Appointment.init") }',
    '    override val tag: String = (super.tag + doctor).also { println("4. Appointment.tag") }',
    '}',
    c('Appointment("a1", "Minh")   // in ra: 1, 2, 3, 4', 'Appointment("a1", "Minh")   // prints: 1, 2, 3, 4')
  ]);
  add('init.openCall', [
    'open class Screen {',
    c('    init { render() }                     // gọi hàm open khi đang khởi tạo', '    init { render() }                     // calls an open function during init'),
    '    open fun render() {}',
    '}',
    'class DetailScreen : Screen() {',
    c('    private val title: String = "Chi tiết"', '    private val title: String = "Details"'),
    c('    override fun render() { println(title.length) }  // title chưa được gán', '    override fun render() { println(title.length) }  // title not assigned yet'),
    '}',
    c('DetailScreen()   // NullPointerException trong render()', 'DetailScreen()   // NullPointerException inside render()')
  ]);
  add('init.object', [
    'object ClinicConfig {',
    c('    init { println("ClinicConfig khởi tạo") }', '    init { println("ClinicConfig initialised") }'),
    '    val baseUrl = "https://api.example.test"',
    '}',
    'fun main() {',
    c('    println("App chạy")              // ClinicConfig chưa khởi tạo', '    println("App runs")              // ClinicConfig not initialised yet'),
    c('    println(ClinicConfig.baseUrl)    // lần truy cập đầu: chạy init', '    println(ClinicConfig.baseUrl)    // first access: init runs'),
    c('    println(ClinicConfig.baseUrl)    // không chạy lại', '    println(ClinicConfig.baseUrl)    // does not run again'),
    '}'
  ]);
  add('init.lateinit', [
    'class BookingScreen {',
    '    lateinit var adapter: SlotAdapter',
    '    fun onCreate() { adapter = SlotAdapter() }',
    '    fun refresh() { adapter.notifyChanged() }',
    '}',
    c('BookingScreen().refresh()     // UninitializedPropertyAccessException', 'BookingScreen().refresh()     // UninitializedPropertyAccessException'),
    c('// kiểm trước: if (::adapter.isInitialized) adapter.notifyChanged()', '// check first: if (::adapter.isInitialized) adapter.notifyChanged()')
  ]);
  /* K4: phần tử trong HashSet (ví dụ theo Effective Kotlin Item 43; data class theo trang Data classes) */
  add('hash.mutate', [
    'data class Patient(var name: String, var surname: String)',
    'val lan = Patient("Lan", "Nguyen")',
    'val waiting = mutableSetOf<Patient>()',
    'waiting.add(lan)',
    c('lan.surname = "Tran"                 // sửa SAU khi đã thêm vào set', 'lan.surname = "Tran"                 // modified AFTER being added'),
    'println(lan in waiting)              // false',
    'println(waiting.first() == lan)      // true'
  ]);
  add('hash.copy', [
    'data class Patient(val name: String, val surname: String)',
    'val lan = Patient("Lan", "Nguyen")',
    'val waiting = mutableSetOf(lan)',
    c('val renamed = lan.copy(surname = "Tran")   // object MỚI, lan không đổi', 'val renamed = lan.copy(surname = "Tran")   // a NEW object, lan unchanged'),
    'waiting.remove(lan); waiting.add(renamed)',
    'println(renamed in waiting)          // true'
  ]);
  add('hash.bodyProp', [
    'data class Patient(val id: String) {',
    c('    var note: String = ""            // khai báo trong thân: KHÔNG thuộc equals', '    var note: String = ""            // declared in the body: NOT part of equals'),
    '}',
    'val a = Patient("P01").apply { note = "dị ứng" }',
    'val b = Patient("P01")',
    'println(a == b)                      // true',
    'println(setOf(a, b).size)            // 1'
  ]);
  add('hash.plain', [
    c('class Patient(val id: String)        // class thường, không có data', 'class Patient(val id: String)        // a plain class, no data'),
    'val a = Patient("P01")',
    'val b = Patient("P01")',
    c('println(a == b)                      // false: equals mặc định so tham chiếu', 'println(a == b)                      // false: default equals compares references'),
    'println(setOf(a, b).size)            // 2'
  ]);
  /* K5: sealed + when (Sealed classes and interfaces; Conditions and loops), enum valueOf (Enum classes) */
  add('sealed.exhaustive', [
    'sealed interface UiState',
    'data object Loading : UiState',
    'data class Success(val slots: List<String>) : UiState',
    'data class Error(val message: String) : UiState',
    c('data object Empty : UiState          // THÊM SAU', 'data object Empty : UiState          // ADDED LATER'),
    'fun title(s: UiState): String = when (s) {',
    c('    Loading -> "Đang tải"', '    Loading -> "Loading"'),
    c('    is Success -> "${s.slots.size} giờ trống"   // smart cast sang Success', '    is Success -> "${s.slots.size} free slots"   // smart cast to Success'),
    '    is Error -> s.message',
    c('    // không có else: thiếu Empty là lỗi biên dịch', '    // no else: a missing Empty is a compile error'),
    '}'
  ]);
  add('sealed.withElse', [
    'sealed interface UiState',
    'data object Loading : UiState',
    'data class Success(val slots: List<String>) : UiState',
    'data class Error(val message: String) : UiState',
    c('data object Empty : UiState          // THÊM SAU', 'data object Empty : UiState          // ADDED LATER'),
    'fun title(s: UiState): String = when (s) {',
    c('    Loading -> "Đang tải"', '    Loading -> "Loading"'),
    c('    is Success -> "${s.slots.size} giờ trống"', '    is Success -> "${s.slots.size} free slots"'),
    c('    else -> "Có lỗi xảy ra"            // Empty lặng lẽ rơi vào đây', '    else -> "Something went wrong"     // Empty silently lands here'),
    '}'
  ]);
  add('sealed.valueOf', [
    'enum class Status { BOOKED, CANCELLED, DONE }',
    c('val raw = "booked"                     // chuỗi từ máy chủ, chữ thường', 'val raw = "booked"                     // a string from the server, lowercase'),
    'val status = Status.valueOf(raw)',
    '// IllegalArgumentException: No enum constant Status.booked',
    c('// an toàn hơn:', '// safer:'),
    'val safe = Status.entries.firstOrNull { it.name.equals(raw, ignoreCase = true) }'
  ]);
  add('exc.uncaught', [
    'fun parseSlot(raw: String): Int = raw.substringBefore(":").toInt()',
    'fun loadSlots(raws: List<String>): List<Int> = raws.map { parseSlot(it) }',
    'fun onShowSlots(raws: List<String>) {',
    '    val slots = loadSlots(raws)          // raws = ["09:00", "9h30"]',
    c('    render(slots)                        // không bao giờ chạy', '    render(slots)                        // never runs'),
    '}',
    c('// sửa: bắt ở tầng quyết định màn hình hiện gì', '// fix: catch where the screen state is decided'),
    'val state = try { UiState.Success(loadSlots(raws)) }',
    '    catch (e: NumberFormatException) { UiState.Error(e.message) }'
  ]);
  add('exc.swallow', [
    'fun loadSlots(raws: List<String>): List<Int> =',
    '    try {',
    '        raws.map { parseSlot(it) }',
    '    } catch (e: Exception) {',
    c('        emptyList()                      // nuốt mọi lỗi', '        emptyList()                      // swallows every error'),
    '    }',
    c('// màn hình: slots.isEmpty() -> "Chưa có giờ trống"', '// screen: slots.isEmpty() -> "No free slots yet"'),
    c('// sửa: bắt đúng loại, ghi log, trả trạng thái lỗi', '// fix: catch the right type, log it, return an error state'),
    '    } catch (e: NumberFormatException) {',
    '        Log.w(TAG, "Bad slot from server", e)',
    '        UiState.Error(e.message)',
    '    }'
  ]);
  add('exc.resource', [
    'fun readCache(file: File): String {',
    '    val reader = file.bufferedReader()',
    c('    val text = reader.readText()         // có thể ném IOException', '    val text = reader.readText()         // may throw IOException'),
    c('    reader.close()                       // bị bỏ qua nếu dòng 3 ném', '    reader.close()                       // skipped if line 3 throws'),
    '    return text',
    '}',
    c('// sửa: use đóng reader dù có ngoại lệ hay không', '// fix: use closes the reader whether or not an exception occurs'),
    'fun readCache(file: File): String = file.bufferedReader().use { it.readText() }'
  ]);
  add('coll.view', [
    'class SlotsViewModel {',
    '    private val _booked = mutableListOf("09:00", "09:30")',
    '    val booked: List<String> get() = _booked',
    '    fun book(slot: String) { _booked.add(slot) }',
    '}',
    'val before = vm.booked',
    'vm.book("10:00")',
    c('println(before.size)              // 3: cùng một object', 'println(before.size)              // 3: the same object'),
    c('println(before == vm.booked)      // true: "không có gì đổi"', 'println(before == vm.booked)      // true: "nothing changed"'),
    c('// sửa: lộ ra bản chụp, không lộ chính list đang sửa', '// fix: expose a snapshot, not the list being modified'),
    'val booked: List<String> get() = _booked.toList()'
  ]);
  add('coll.downcast', [
    'val slots: List<String> = listOf("09:00", "09:30")',
    c('// ĐỪNG: ép kiểu để sửa', '// DON\'T: cast to modify it'),
    '(slots as MutableList<String>).add("10:00")',
    '// JVM: UnsupportedOperationException',
    c('// sửa: sửa trên một bản sao', '// fix: modify a copy'),
    'val more = slots.toMutableList().apply { add("10:00") }'
  ]);
  add('coll.mapOnMap', [
    'val prices = mapOf("checkup" to 200, "bloodTest" to 150)',
    'val discounted = prices.map { it.value * 9 / 10 }',
    c('// discounted: List<Int> = [180, 135], mất key', '// discounted: List<Int> = [180, 135], the keys are gone'),
    c('val p = discounted["checkup"]     // lỗi biên dịch', 'val p = discounted["checkup"]     // compile error'),
    c('// sửa: mapValues giữ key, chỉ đổi value', '// fix: mapValues keeps the keys, changes only the values'),
    'val discounted = prices.mapValues { it.value * 9 / 10 }   // {checkup=180, bloodTest=135}'
  ]);
  add('inl.inlined', [
    'fun hasFreeSlot(slots: List<String>, taken: Set<String>): Boolean {',
    '    slots.forEach {',
    c('        if (it !in taken) return true    // thoát hasFreeSlot', '        if (it !in taken) return true    // exits hasFreeSlot'),
    '    }',
    '    return false',
    '}',
    c('// forEach là inline: trình biên dịch chép thân thành vòng lặp, gần như:', '// forEach is inline: the compiler copies the body into a loop, roughly:'),
    'for (it in slots) { if (it !in taken) return true }'
  ]);
  add('inl.returnBug', [
    'fun confirmAll(slots: List<String>) {',
    '    slots.forEach {',
    c('        if (it in cancelled) return      // định "bỏ qua giờ này"', '        if (it in cancelled) return      // meant as "skip this slot"'),
    '        confirm(it)',
    '    }',
    c('    saveAndNotify()                      // không chạy nếu gặp giờ đã hủy', '    saveAndNotify()                      // never runs once a cancelled slot is met'),
    '}',
    c('// sửa: return@forEach chỉ thoát lambda, giống continue', '// fix: return@forEach exits only the lambda, like continue'),
    '        if (it in cancelled) return@forEach'
  ]);
  add('inl.stored', [
    'object ClinicRepository {',
    c('    var onUpdate: (() -> Unit)? = null   // giữ lambda lâu dài', '    var onUpdate: (() -> Unit)? = null   // holds the lambda for a long time'),
    '}',
    'class SlotsActivity : AppCompatActivity() {',
    '    override fun onCreate(savedInstanceState: Bundle?) {',
    '        super.onCreate(savedInstanceState)',
    c('        ClinicRepository.onUpdate = { render() }   // bắt this (Activity)', '        ClinicRepository.onUpdate = { render() }   // captures this (the Activity)'),
    '    }',
    c('    // sửa: gỡ lambda khi Activity bị hủy', '    // fix: remove the lambda when the Activity is destroyed'),
    '    override fun onDestroy() { ClinicRepository.onUpdate = null; super.onDestroy() }',
    '}'
  ]);
  add('eval.when', [
    'val score = 7',
    'val label = when (score) {',
    c('    in 9..10 -> "Giỏi"', '    in 9..10 -> "Excellent"'),
    c('    in 5..8 -> "Đạt"', '    in 5..8 -> "Pass"'),
    c('    else -> "Chưa đạt"', '    else -> "Not yet"'),
    '}'
  ]);
})();
