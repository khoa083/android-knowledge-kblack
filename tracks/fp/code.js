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
})();
