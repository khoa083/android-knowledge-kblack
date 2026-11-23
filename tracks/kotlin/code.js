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
  add('eval.when', [
    'val score = 7',
    'val label = when (score) {',
    c('    in 9..10 -> "Giỏi"', '    in 9..10 -> "Excellent"'),
    c('    in 5..8 -> "Đạt"', '    in 5..8 -> "Pass"'),
    c('    else -> "Chưa đạt"', '    else -> "Not yet"'),
    '}'
  ]);
})();
