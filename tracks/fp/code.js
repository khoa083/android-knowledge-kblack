/* Đoạn mã track K (minh họa, rút gọn; không chạy trong trang). Số dòng được tham chiếu bởi codeHighlight trong models/models.js. */
(function () {
  var add = function (id, lines) { ADE.addCode('fp', id, { lang: 'kotlin', illustrative: true, lines: lines }); };
  var c = function (vi, en) { return { vi: vi, en: en }; };

  /* K1: hàm tự đọc ngày hiện tại và tăng một biến đếm; dòng 4 đọc đồng hồ, dòng 3 là side effect */
  add('p1.impure', [
    c('var calls = 0                                  // thống kê: đếm lượt tính phí', 'var calls = 0                                  // analytics: count fee lookups'),
    'fun fee(): Long {',
    '    calls++',
    '    val day = LocalDate.now().dayOfWeek',
    '    return if (day == SATURDAY || day == SUNDAY) 300_000 else 200_000',
    '}',
    c('val total = fee() + fee()                      // hai lượt khám cùng ngày', 'val total = fee() + fee()                      // two visits on the same day'),
    '@Test fun weekdayFee() = assertEquals(200_000, fee())'
  ]);
  /* K1: ngày là tham số; đọc đồng hồ và đếm lượt ở vỏ (dòng 9) */
  add('p1.pure', [
    'fun fee(date: LocalDate): Long {',
    '    val day = date.dayOfWeek',
    '    return if (day == SATURDAY || day == SUNDAY) 300_000 else 200_000',
    '}',
    c('val d = LocalDate.of(2026, 11, 28)             // thứ Bảy', 'val d = LocalDate.of(2026, 11, 28)             // a Saturday'),
    'val total = fee(d) + fee(d)',
    '@Test fun weekdayFee() = assertEquals(200_000, fee(LocalDate.of(2026, 11, 23)))',
    '@Test fun weekendFee() = assertEquals(300_000, fee(LocalDate.of(2026, 11, 28)))',
    c('// vỏ: fee(LocalDate.now(clock)); analytics.count("fee")', '// shell: fee(LocalDate.now(clock)); analytics.count("fee")')
  ]);

  /* K2: hai tên, một MutableList: sửa qua tên này là sửa cả tên kia */
  add('p2.mutable', [
    'val booked: MutableList<Booking> = mutableListOf(b1, b2, b3)',
    c('val selected = booked                         // cùng một object', 'val selected = booked                         // the very same object'),
    c('selected.add(b4)                              // booked cũng có b4', 'selected.add(b4)                              // booked gets b4 too'),
    c('selected.removeAt(0)                          // booked mất b1', 'selected.removeAt(0)                          // booked loses b1')
  ]);
  /* K2: list persistent tự viết (như FList của Carli, List của Vermeulen và cộng sự): thêm vào đầu tạo 1 nút, đuôi dùng chung */
  add('p2.persistent', [
    'sealed interface FList<out A>',
    'object Nil : FList<Nothing>',
    'data class Cons<A>(val head: A, val tail: FList<A>) : FList<A>',
    'val booked = Cons(b1, Cons(b2, Cons(b3, Nil)))',
    c('val selected = Cons(b4, booked)               // 1 nút mới, đuôi dùng chung', 'val selected = Cons(b4, booked)               // 1 new node, shared tail'),
    c('val rest = selected.tail                      // 0 nút mới; rest === booked', 'val rest = selected.tail                      // 0 new nodes; rest === booked')
  ]);
  /* K2: đệ quy thường: còn phép cộng sau lời gọi, mỗi phần tử giữ một khung stack */
  add('p2.plain', [
    'fun total(xs: FList<Booking>): Long = when (xs) {',
    '    Nil -> 0L',
    c('    is Cons -> xs.head.fee + total(xs.tail)       // còn phép cộng sau lời gọi', '    is Cons -> xs.head.fee + total(xs.tail)       // an addition remains after the call'),
    '}'
  ]);
  /* K2: tham số tích lũy + tailrec: lời gọi là việc cuối cùng, trình biên dịch đổi thành vòng lặp */
  add('p2.tailrec', [
    'tailrec fun total(xs: FList<Booking>, acc: Long = 0L): Long = when (xs) {',
    '    Nil -> acc',
    c('    is Cons -> total(xs.tail, acc + xs.head.fee)  // lời gọi là việc cuối cùng', '    is Cons -> total(xs.tail, acc + xs.head.fee)  // the call is the last thing done'),
    '}'
  ]);

  /* K3: hàm 6 tham số gọi ở 4 chỗ; ba tham số cấu hình lặp lại; dòng 7 chép múi giờ UTC từ test */
  add('p3.nested', [
    'fun formatAppointment(locale: Locale, currency: Currency, zone: ZoneId,',
    '                      b: Booking, fee: Long, compact: Boolean): String = TODO()',
    '',
    c('val b = assign(parse(raw))                                     // đọc từ trong ra', 'val b = assign(parse(raw))                                     // read inside out'),
    c('formatAppointment(VI, VND, CLINIC_ZONE, b, price(b), true)     // danh sách', 'formatAppointment(VI, VND, CLINIC_ZONE, b, price(b), true)     // list'),
    c('formatAppointment(VI, VND, CLINIC_ZONE, b, price(b), false)    // chi tiết', 'formatAppointment(VI, VND, CLINIC_ZONE, b, price(b), false)    // detail'),
    c('formatAppointment(VI, VND, ZoneOffset.UTC, b, price(b), false) // nhắc lịch: chép từ test', 'formatAppointment(VI, VND, ZoneOffset.UTC, b, price(b), false) // reminder: copied from a test'),
    c('formatAppointment(VI, VND, CLINIC_ZONE, b, price(b), false)    // biên lai', 'formatAppointment(VI, VND, CLINIC_ZONE, b, price(b), false)    // receipt')
  ]);
  /* K3: ghép theo thứ tự chạy; cố định ba tham số chung một lần (partial application) */
  add('p3.composed', [
    c('infix fun <A, B, C> ((A) -> B).compose(g: (B) -> C): (A) -> C = { a -> g(this(a)) }   // như compose của Carli', 'infix fun <A, B, C> ((A) -> B).compose(g: (B) -> C): (A) -> C = { a -> g(this(a)) }   // like Carli\'s compose'),
    c('val toPriced: (String) -> Priced = ::parse compose ::assign compose ::price   // đọc theo thứ tự chạy', 'val toPriced: (String) -> Priced = ::parse compose ::assign compose ::price   // reads in run order'),
    'fun formatFor(locale: Locale, currency: Currency, zone: ZoneId): (Priced, Boolean) -> String =',
    '    { p, compact -> formatAppointment(locale, currency, zone, p.booking, p.fee, compact) }',
    c('val show = formatFor(VI, VND, CLINIC_ZONE)                    // ba tham số chung: một lần', 'val show = formatFor(VI, VND, CLINIC_ZONE)                    // the three shared ones: once'),
    c('show(toPriced(raw), true)                                     // danh sách', 'show(toPriced(raw), true)                                     // list'),
    c('show(toPriced(raw), false)                                    // chi tiết', 'show(toPriced(raw), false)                                    // detail'),
    c('show(toPriced(raw), false)                                    // nhắc lịch', 'show(toPriced(raw), false)                                    // reminder'),
    c('show(toPriced(raw), false)                                    // biên lai', 'show(toPriced(raw), false)                                    // receipt')
  ]);

  /* K4: product type: ba trường độc lập, 2 × 2 × 2 = 8 dạng; dòng 6 quên tắt isLoading; dòng 7 là chuỗi if của màn hình */
  add('p4.product', [
    'data class SlotsUiState(',
    '    val isLoading: Boolean = false,',
    '    val error: String? = null,',
    '    val slots: List<Slot>? = null',
    c(')                                                   // 2 × 2 × 2 = 8 dạng', ')                                                   // 2 × 2 × 2 = 8 shapes'),
    c('catch (e: IOException) { _state.update { it.copy(error = e.message) } }   // quên isLoading = false', 'catch (e: IOException) { _state.update { it.copy(error = e.message) } }   // forgets isLoading = false'),
    'if (s.isLoading) Spinner() else if (s.error != null) ErrorText(s.error) else SlotList(s.slots!!)'
  ]);
  /* K4: sum type: mỗi trạng thái một kiểu con; when phủ đủ, không else; Refreshing thêm ở bước 4 */
  add('p4.sum', [
    'sealed interface SlotsUiState {',
    '    data object Loading : SlotsUiState',
    '    data class Error(val message: String) : SlotsUiState',
    '    data class Success(val slots: List<Slot>) : SlotsUiState',
    c('    data class Refreshing(val slots: List<Slot>) : SlotsUiState   // thêm ở bước 4', '    data class Refreshing(val slots: List<Slot>) : SlotsUiState   // added in step 4'),
    c('}                                                   // 1 + 1 + 1 (+ 1) dạng', '}                                                   // 1 + 1 + 1 (+ 1) shapes'),
    'catch (e: IOException) { _state.value = SlotsUiState.Error(e.message ?: "") }',
    'when (s) { Loading -> Spinner(); is Error -> ErrorText(s.message); is Success -> SlotList(s.slots); is Refreshing -> SlotList(s.slots, refreshing = true) }'
  ]);

  /* K5: ngoại lệ: chữ ký không nói gì về lỗi; màn hình bắt mọi Exception (dòng 9), kể cả lỗi lập trình */
  add('p5.throw', [
    c('class SlotTakenException(id: String) : Exception("Giờ $id đã có người đặt")', 'class SlotTakenException(id: String) : Exception("Slot $id is already taken")'),
    c('fun book(raw: String, slotId: String): Booking {      // chữ ký không nhắc tới lỗi', 'fun book(raw: String, slotId: String): Booking {      // the signature never mentions errors'),
    c('    val phone = parsePhone(raw)                        // có thể ném IllegalArgumentException', '    val phone = parsePhone(raw)                        // may throw IllegalArgumentException'),
    c('    val slot = findFreeSlot(slotId)                    // có thể ném SlotTakenException', '    val slot = findFreeSlot(slotId)                    // may throw SlotTakenException'),
    c('    checkQuota(phone)                                  // có thể ném QuotaExceededException', '    checkQuota(phone)                                  // may throw QuotaExceededException'),
    '    return save(phone, slot)',
    '}',
    c('val message = try { book(raw, id); "Đã đặt lịch" }', 'val message = try { book(raw, id); "Booked" }'),
    c('    catch (e: Exception) { "Đặt lịch thất bại" }       // bắt cả lỗi lập trình', '    catch (e: Exception) { "Booking failed" }          // also catches programming bugs')
  ]);
  /* K5: nullable: mỗi bước hỏng trả null; màn hình chỉ biết "có hay không" */
  add('p5.nullable', [
    'fun book(raw: String, slotId: String): Booking? {',
    '    val phone = parsePhone(raw) ?: return null',
    '    val slot = findFreeSlot(slotId) ?: return null',
    '    if (!quotaLeft(phone)) return null',
    '    return save(phone, slot)',
    '}',
    c('val message = if (book(raw, id) != null) "Đã đặt lịch"', 'val message = if (book(raw, id) != null) "Booked"'),
    c('    else "Đặt lịch thất bại"                            // không biết vì sao', '    else "Booking failed"                               // no idea why')
  ]);
  /* K5: Result: runCatching gói mọi Throwable (dòng 1); màn hình phải đoán lớp ngoại lệ (dòng 9) */
  add('p5.result', [
    'fun book(raw: String, slotId: String): Result<Booking> = runCatching {',
    '    val phone = parsePhone(raw)',
    '    val slot = findFreeSlot(slotId)',
    '    checkQuota(phone)',
    '    save(phone, slot)',
    '}',
    'val message = book(raw, id).fold(',
    c('    onSuccess = { "Đã đặt lịch" },', '    onSuccess = { "Booked" },'),
    c('    onFailure = { e -> if (e is SlotTakenException) "Giờ này đã có người đặt" else "Đặt lịch thất bại" })', '    onFailure = { e -> if (e is SlotTakenException) "This slot is already taken" else "Booking failed" })')
  ]);
  /* K5: kiểu lỗi riêng: lỗi nghiệp vụ là một sealed interface; when không có else (dòng 14) */
  add('p5.typed', [
    'sealed interface BookingError {',
    '    data object InvalidPhone : BookingError',
    '    data class SlotTaken(val slotId: String) : BookingError',
    '    data object QuotaExceeded : BookingError',
    '}',
    'fun book(raw: String, slotId: String): Outcome<BookingError, Booking> {',
    '    val phone = parsePhone(raw) ?: return Err(BookingError.InvalidPhone)',
    '    val slot = findFreeSlot(slotId) ?: return Err(BookingError.SlotTaken(slotId))',
    '    if (!quotaLeft(phone)) return Err(BookingError.QuotaExceeded)',
    '    return Ok(save(phone, slot))',
    '}',
    'val message = when (val r = book(raw, id)) {',
    c('    is Ok -> "Đã đặt lịch"', '    is Ok -> "Booked"'),
    c('    is Err -> when (r.error) {                          // không có else', '    is Err -> when (r.error) {                          // no else'),
    c('        BookingError.InvalidPhone -> "Số điện thoại không hợp lệ"', '        BookingError.InvalidPhone -> "Invalid phone number"'),
    c('        is BookingError.SlotTaken -> "Giờ này đã có người đặt"', '        is BookingError.SlotTaken -> "This slot is already taken"'),
    c('        BookingError.QuotaExceeded -> "Bạn đã hết lượt đặt trong tuần"', '        BookingError.QuotaExceeded -> "You have no bookings left this week"'),
    '    }',
    '}'
  ]);

  /* K6: cùng map và flatMap trên List, kiểu nullable (qua ?.let) và Outcome */
  add('p6.list', [
    'val doctors = listOf("an", "binh")',
    c('val names = doctors.map { displayName(it) }              // [BS An, BS Bình]', 'val names = doctors.map { displayName(it) }              // [Dr An, Dr Binh]'),
    'val nested = doctors.map { slotsToday(it) }             // [[S12, S13], [S20]]',
    'val all = doctors.flatMap { slotsToday(it) }            // [S12, S13, S20]',
    c('val same = doctors.map { slotsToday(it) }.flatten()    // flatMap = map rồi flatten', 'val same = doctors.map { slotsToday(it) }.flatten()    // flatMap = map, then flatten'),
    c('// chuỗi: mọi bác sĩ, cả thứ Bảy và Chủ nhật', '// a chain: every doctor, both Saturday and Sunday'),
    'val weekend = doctors.flatMap { d -> listOf(SAT, SUN).flatMap { day -> slotsOn(d, day) } }'
  ]);
  add('p6.nullable', [
    'val lan: Patient? = findPatient("0901234567")',
    'val name = lan?.let { it.name }                          // "Lan"',
    c('val card = lan?.let { it.insuranceCard }                // String?: không có kiểu String?? riêng', 'val card = lan?.let { it.insuranceCard }                // String?: there is no separate String?? type'),
    c('val noCard = findPatient("0912000111")?.let { it.insuranceCard }   // null: Minh không có thẻ', 'val noCard = findPatient("0912000111")?.let { it.insuranceCard }   // null: Minh has no card'),
    c('// chuỗi: bệnh nhân → thẻ → mức chi trả', '// a chain: patient → card → coverage'),
    'val cover = findPatient(phone)?.let { p -> p.insuranceCard?.let { coverageOf(it) } }   // 80'
  ]);
  add('p6.outcome', [
    'val phone = parsePhone("0901234567")                     // Outcome<BookingError, Phone>',
    'val masked = phone.map { it.masked() }                   // Ok("090•••4567")',
    c('val nested = phone.map { ensureQuota(it) }               // Ok(Ok(Unit)): hộp trong hộp', 'val nested = phone.map { ensureQuota(it) }               // Ok(Ok(Unit)): a box in a box'),
    c('val quota = phone.flatMap { ensureQuota(it) }           // Ok(Unit): một tầng', 'val quota = phone.flatMap { ensureQuota(it) }           // Ok(Unit): one level'),
    'fun book(raw: String, slotId: String) = parsePhone(raw).flatMap { p ->',
    '    findFreeSlot(slotId).flatMap { s ->',
    '        ensureQuota(p).map { save(p, s) }',
    '    }',
    '}'
  ]);

  /* K7: dừng sớm: nối bằng flatMap, mỗi lần nộp chỉ thấy lỗi đầu tiên */
  add('p7.fast', [
    'fun register(f: Form): Outcome<FormError, Patient> =',
    '    validName(f.name).flatMap { name ->',
    '    validPhone(f.phone).flatMap { phone ->',
    '    validDob(f.dob).flatMap { dob ->',
    '    validCard(f.card).map { card -> Patient(name, phone, dob, card) } } } }',
    c('// lỗi đầu tiên dừng cả chuỗi: các ô sau không được kiểm', '// the first error stops the chain: later fields are never checked')
  ]);
  /* K7: gom lỗi bằng Kotlin thuần: kiểm mọi ô độc lập, gộp lỗi, chỉ tạo Patient khi mọi ô đều Ok; bước phụ thuộc nối sau bằng flatMap */
  add('p7.acc', [
    'fun register(f: Form): Outcome<List<FormError>, Patient> {',
    c('    val name = validName(f.name)                    // mỗi ô kiểm độc lập', '    val name = validName(f.name)                    // each field is checked on its own'),
    '    val phone = validPhone(f.phone)',
    '    val dob = validDob(f.dob)',
    '    val card = validCard(f.card)',
    c('    val errors = listOf(name, phone, dob, card).mapNotNull { it.errorOrNull() }   // gộp mọi lỗi', '    val errors = listOf(name, phone, dob, card).mapNotNull { it.errorOrNull() }   // collect every error'),
    '    return if (name is Ok && phone is Ok && dob is Ok && card is Ok)',
    '        Ok(Patient(name.value, phone.value, dob.value, card.value))',
    '    else Err(errors)',
    '}',
    c('fun registerNew(f: Form) = register(f).flatMap { p -> ensurePhoneFree(p.phone).map { p } }   // bước phụ thuộc', 'fun registerNew(f: Form) = register(f).flatMap { p -> ensurePhoneFree(p.phone).map { p } }   // a dependent step')
  ]);

  /* K8: một biến, nhiều chỗ sửa: màn đặt lịch và bước đồng bộ cùng trừ */
  add('p8.mutable', [
    c('var remaining = 0                                       // một biến, nhiều chỗ sửa', 'var remaining = 0                                       // one variable, many writers'),
    'fun onPackageBought(visits: Int) { remaining = visits }',
    c('fun onBookTapped(id: Long) { remaining--; api.book(id) }   // màn đặt lịch trừ', 'fun onBookTapped(id: Long) { remaining--; api.book(id) }   // the booking screen subtracts'),
    c('fun onBookingSynced(id: Long) { remaining-- }              // bước đồng bộ cũng trừ', 'fun onBookingSynced(id: Long) { remaining-- }              // the sync step subtracts too'),
    'fun onCancelled(id: Long) { remaining++ }'
  ]);
  /* K8: nhật ký event và một hàm reduce thuần; id lịch nằm trong event */
  add('p8.events', [
    'sealed interface Event { data class PackageBought(val visits: Int) : Event',
    '    data class VisitBooked(val bookingId: Long) : Event; data class VisitCancelled(val bookingId: Long) : Event }',
    'data class Quota(val remaining: Int = 0, val active: Set<Long> = emptySet())',
    'fun reduce(s: Quota, e: Event): Quota = when (e) {',
    '    is Event.PackageBought -> s.copy(remaining = e.visits)',
    '    is Event.VisitBooked -> s.copy(remaining = s.remaining - 1, active = s.active + e.bookingId)',
    '    is Event.VisitCancelled -> if (e.bookingId in s.active) s.copy(remaining = s.remaining + 1, active = s.active - e.bookingId) else s',
    '}',
    c('val history = events.runningFold(Quota(), ::reduce)     // state sau từng event', 'val history = events.runningFold(Quota(), ::reduce)     // the state after each event'),
    c('val current = events.fold(Quota(), ::reduce)            // state hiện tại', 'val current = events.fold(Quota(), ::reduce)            // the current state')
  ]);

  /* K9: một hàm trộn đọc, quyết định và ghi xen kẽ */
  add('p9.mixed', [
    'suspend fun book(req: BookRequest): String {',
    '    val now = clock.now()',
    '    val slots = repo.slots(req.day)',
    c('    if (req.time < now) return "Giờ đã qua"', '    if (req.time < now) return "That time has passed"'),
    c('    analytics.track("booked")                      // gửi trước khi biết có đặt được không', '    analytics.track("booked")                      // sent before we know whether it can be booked'),
    '    val quota = api.quota(req.phone)',
    c('    if (req.slotId !in slots || quota == 0) return "Không đặt được"', '    if (req.slotId !in slots || quota == 0) return "Cannot book"'),
    '    val fee = if (req.day.isWeekend()) 300_000 else 200_000',
    '    repo.save(Booking(req, fee)); log.info("booked ${req.slotId}")',
    c('    return "Đã đặt, phí $fee"', '    return "Booked, fee $fee"'),
    '}'
  ]);
  /* K9: lõi thuần decide() và vỏ mỏng book(): đọc hết, gọi lõi, rồi mới ghi */
  add('p9.core', [
    'sealed interface Decision { data class Accept(val booking: Booking) : Decision; data class Reject(val reason: BookingError) : Decision }',
    c('fun decide(req: BookRequest, now: LocalDateTime, slots: Set<String>, quota: Int): Decision = when {   // lõi: thuần', 'fun decide(req: BookRequest, now: LocalDateTime, slots: Set<String>, quota: Int): Decision = when {   // core: pure'),
    '    req.time < now -> Decision.Reject(BookingError.SlotPassed)',
    '    req.slotId !in slots -> Decision.Reject(BookingError.SlotTaken(req.slotId))',
    '    quota == 0 -> Decision.Reject(BookingError.QuotaExceeded)',
    '    else -> Decision.Accept(Booking(req, fee = if (req.day.isWeekend()) 300_000 else 200_000))',
    '}',
    c('suspend fun book(req: BookRequest): Decision {                                   // vỏ: mỏng', 'suspend fun book(req: BookRequest): Decision {                                   // shell: thin'),
    '    val d = decide(req, clock.now(), repo.slots(req.day), api.quota(req.phone))',
    '    if (d is Decision.Accept) { repo.save(d.booking); analytics.track("booked"); log.info("booked ${req.slotId}") }',
    '    return d',
    '}'
  ]);

  /* K10: dựng lại object bên trong (mất trường) và sửa MutableList tại chỗ (StateFlow không phát) */
  add('p10.careless', [
    'val p = state.patient',
    c('state = state.copy(patient = Patient(name = p.name, address = Address(p.address.street, "Đà Nẵng")))   // phone, card về mặc định', 'state = state.copy(patient = Patient(name = p.name, address = Address(p.address.street, "Da Nang")))   // phone, card fall back to defaults'),
    c('val old = state                                         // giữ để hoàn tác', 'val old = state                                         // kept for undo'),
    c('state.bookings.add(42)                                  // bookings là MutableList: sửa tại chỗ', 'state.bookings.add(42)                                  // bookings is a MutableList: changed in place'),
    c('_state.value = state                                    // cùng object: StateFlow không phát', '_state.value = state                                    // the same object: StateFlow does not emit')
  ]);
  /* K10: copy lồng, list mới; Arrow optics cho cùng kết quả */
  add('p10.careful', [
    c('state = state.copy(patient = state.patient.copy(address = state.patient.address.copy(city = "Đà Nẵng")))', 'state = state.copy(patient = state.patient.copy(address = state.patient.address.copy(city = "Da Nang")))'),
    'val old = state',
    c('state = state.copy(bookings = state.bookings + 42)      // List chỉ đọc: tạo list mới', 'state = state.copy(bookings = state.bookings + 42)      // a read-only List: a new list is built'),
    c('_state.value = state                                    // object mới: StateFlow phát', '_state.value = state                                    // a new object: StateFlow emits'),
    c('// Arrow optics (thư viện bên ngoài): cùng kết quả với dòng 1', '// Arrow optics (an external library): the same result as line 1'),
    c('state = ProfileState.patient.address.city.set(state, "Đà Nẵng")', 'state = ProfileState.patient.address.city.set(state, "Da Nang")')
  ]);
})();
