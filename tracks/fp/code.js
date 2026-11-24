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
})();
