/* Đoạn mã track J (minh họa, rút gọn; không chạy trong trang). Số dòng được tham chiếu bởi codeHighlight trong models/models.js. */
(function () {
  var add = function (id, lines) { ADE.addCode('cleancode', id, { lang: 'kotlin', illustrative: true, lines: lines }); };
  var c = function (vi, en) { return { vi: vi, en: en }; };

  /* J1: một hàm dài 19 dòng; 8 lệnh if/for ở dòng 2, 4, 6, 8, 9, 10, 12, 16 */
  var LONG_HEAD = [
    'fun bookAppointment(req: BookingRequest): Result {',
    '    if (req.phone.isBlank()) return Result.Invalid("phone")',
    '    val doctor = doctors.find(req.doctorId)',
    '    if (doctor == null) return Result.Invalid("doctor")',
    '    val slot = req.slot',
    '    if (slot.isBefore(clock.now())) return Result.Invalid("past")',
    '    var fee = doctor.baseFee',
    '    if (slot.isWeekend()) fee += doctor.baseFee / 2',
    '    if (req.insured) fee = fee * 70 / 100',
    '    for (code in req.voucherCodes) {',
    '        val v = vouchers.find(code)',
    '        if (v != null) fee -= v.amount',
    '    }'
  ];
  var LONG_TAIL = [
    '    val booking = Booking(req.patientId, doctor.id, slot, fee)',
    '    repo.save(booking)',
    '    val hours = if (req.prefersEarly) 24 else 2',
    c('    reminders.schedule(booking.id, slot.minusHours(hours))   // hẹn nhắc', '    reminders.schedule(booking.id, slot.minusHours(hours))   // the reminder'),
    '    return Result.Ok(booking)',
    '}'
  ];
  add('j1.long', LONG_HEAD.concat(LONG_TAIL));
  /* yêu cầu mới chèn sau vòng for (dòng 14–17): return sớm bỏ qua dòng 21 */
  add('j1.longFree', LONG_HEAD.concat([
    c('    if (fee <= 0) {                                 // mới: phí 0 đ', '    if (fee <= 0) {                                 // new: a 0 fee'),
    '        val free = Booking(req.patientId, doctor.id, slot, 0)',
    c('        repo.save(free); return Result.Ok(free)    // trả về luôn', '        repo.save(free); return Result.Ok(free)    // returns at once'),
    '    }'
  ], LONG_TAIL));

  /* J1: tách thành ba hàm đọc từ trên xuống (stepdown) */
  var SPLIT = function (feeLine) {
    return [
      'fun bookAppointment(req: BookingRequest): Result {',
      '    val doctor = validate(req)',
      '    if (doctor == null) return Result.Invalid("input")',
      '    val fee = feeFor(doctor, req)',
      '    val booking = Booking(req.patientId, doctor.id, req.slot, fee)',
      '    repo.save(booking)',
      c('    reminders.scheduleFor(booking, req.prefersEarly)   // hẹn nhắc', '    reminders.scheduleFor(booking, req.prefersEarly)   // the reminder'),
      '    return Result.Ok(booking)',
      '}',
      '',
      'private fun validate(req: BookingRequest): Doctor? {',
      '    if (req.phone.isBlank()) return null',
      '    if (req.slot.isBefore(clock.now())) return null',
      '    return doctors.find(req.doctorId)',
      '}',
      '',
      'private fun feeFor(doctor: Doctor, req: BookingRequest): Int {',
      '    var fee = doctor.baseFee',
      '    if (req.slot.isWeekend()) fee += doctor.baseFee / 2',
      '    if (req.insured) fee = fee * 70 / 100',
      feeLine,
      '}'
    ];
  };
  add('j1.split', SPLIT(c('    return fee - vouchers.totalFor(req.voucherCodes)   // vòng lặp voucher ở đây', '    return fee - vouchers.totalFor(req.voucherCodes)   // the voucher loop lives here')));
  add('j1.splitFree', SPLIT(c('    return (fee - vouchers.totalFor(req.voucherCodes)).coerceAtLeast(0)   // mới: không âm', '    return (fee - vouchers.totalFor(req.voucherCodes)).coerceAtLeast(0)   // new: never negative')));

  /* J2: bản trộn đọc và ghi (thành viên ở dòng 2, 7, 9, 12) và bản tách command, query (dòng 2–7) */
  add('j2.mixed', [
    'class AppointmentRepo(private val api: Api, private val cache: Cache) {',
    '    fun getAppointments(): List<Appointment> {',
    '        val tmp = cache.all()',
    c('        cache.clear()                                  // để lần sau tải bản mới', '        cache.clear()                                  // so the next call loads fresh data'),
    '        return tmp.ifEmpty { api.fetchAllOrEmpty() }',
    '    }',
    '    fun save(a: Appointment): Boolean =',
    c('        cache.put(a.id, a) != null                     // true: đã có từ trước', '        cache.put(a.id, a) != null                     // true: it already existed'),
    '    fun process(data2: String, flag: Boolean) {',
    '        if (flag) api.cancel(data2) else api.reschedule(data2, nextFree)',
    '    }',
    '    val nextFree: Slot',
    c('        get() = api.findNextFreeSlotBlocking()         // gọi mạng trong getter', '        get() = api.findNextFreeSlotBlocking()         // a network call in the getter'),
    '}'
  ]);
  add('j2.cqs', [
    'class AppointmentRepo(private val api: Api, private val cache: Cache) {',
    c('    fun appointments(): List<Appointment> = cache.all()            // query: chỉ đọc', '    fun appointments(): List<Appointment> = cache.all()            // query: read only'),
    c('    fun clearExpiredCache() { cache.removeBefore(today()) }        // command, có tên riêng', '    fun clearExpiredCache() { cache.removeBefore(today()) }        // a named command'),
    '    fun add(a: Appointment) { cache.put(a.id, a) }',
    '    fun cancel(id: AppointmentId) { api.cancel(id) }',
    '    fun reschedule(id: AppointmentId, to: Slot) { api.reschedule(id, to) }',
    '    suspend fun findNextFreeSlot(doctor: DoctorId): Slot? = api.nextFreeSlot(doctor)',
    '}'
  ]);

  /* J3: kiểm rải rác (ba luật ở dòng 2–4, luật thứ tư ở dòng 12) và parse một lần (dòng 7–10), bên trong chỉ nhận PhoneNumber */
  add('j3.validate', [
    c('// ba màn hình, ba luật; giá trị qua kiểm vẫn là String', '// three screens, three rules; a checked value is still a String'),
    'fun bookingPhoneOk(s: String) = s.replace(" ", "").length == 10',
    'fun profilePhoneOk(s: String) = s.startsWith("+84") || s.startsWith("0")',
    'fun reminderPhoneOk(s: String) = s.length >= 9',
    '',
    'class PatientRepo {',
    c('    fun savePhone(id: PatientId, phone: String) { /* lưu nguyên chuỗi */ }', '    fun savePhone(id: PatientId, phone: String) { /* stored as typed */ }'),
    '}',
    'class SmsSender {',
    '    fun send(phone: String, text: String) {',
    '        val d = phone.replace(" ", "")',
    c('        if (!Regex("0\\\\d{9}").matches(d)) error("bad phone: $phone")   // luật thứ tư', '        if (!Regex("0\\\\d{9}").matches(d)) error("bad phone: $phone")   // a fourth rule'),
    '        gateway.send(d, text)',
    '    }',
    '}'
  ]);
  add('j3.parse', [
    '@JvmInline',
    'value class PhoneNumber(val digits: String) {',
    c('    init { require(VN_MOBILE.matches(digits)) }     // không tạo được giá trị sai', '    init { require(VN_MOBILE.matches(digits)) }     // an invalid value cannot be built'),
    '}',
    'private val VN_MOBILE = Regex("0[35789]\\\\d{8}")',
    '',
    c('fun parsePhone(raw: String): PhoneNumber? {        // ranh giới: thô → kiểu đã chắc đúng', 'fun parsePhone(raw: String): PhoneNumber? {        // the boundary: raw → a type known to be valid'),
    '    val d = raw.filter(Char::isDigit)',
    '    val local = if (d.startsWith("84")) "0" + d.drop(2) else d',
    '    return if (VN_MOBILE.matches(local)) PhoneNumber(local) else null',
    '}',
    '',
    'class PatientRepo { fun savePhone(id: PatientId, phone: PhoneNumber) { /* ... */ } }',
    'class SmsSender { fun send(phone: PhoneNumber, text: String) = gateway.send(phone.digits, text) }'
  ]);

  /* J4: viết mã trước (j4.after) và bốn phiên bản mã qua bốn vòng TDD (j4.t1–t4) */
  add('j4.after', [
    'fun fee(date: LocalDate): Int =',
    '    if (date.dayOfWeek == SATURDAY || date.dayOfWeek == SUNDAY) 300_000',
    c('    else 200_000                                 // ngày lễ rơi vào đây', '    else 200_000                                 // holidays land here'),
    c('// test viết sau: thứ hai 23/11 → 200_000; thứ bảy 28/11 → 300_000 (xanh ngay lần đầu)', '// tests written after: Monday 23 Nov → 200_000; Saturday 28 Nov → 300_000 (green on first run)')
  ]);
  add('j4.t1', [
    'fun fee(date: LocalDate): Int =',
    c('    200_000                                       // đơn giản nhất để test 1 xanh', '    200_000                                       // the simplest code that passes test 1')
  ]);
  add('j4.t2', [
    'fun fee(date: LocalDate): Int =',
    c('    if (date.dayOfWeek == SATURDAY) 300_000      // chủ nhật chưa có ví dụ', '    if (date.dayOfWeek == SATURDAY) 300_000      // no Sunday example yet'),
    '    else 200_000'
  ]);
  add('j4.t3', [
    'fun fee(date: LocalDate): Int =',
    '    if (date.isWeekend()) 300_000 else 200_000',
    '',
    c('private fun LocalDate.isWeekend() =               // refactor khi mọi test xanh', 'private fun LocalDate.isWeekend() =               // refactored while every test is green'),
    '    dayOfWeek == SATURDAY || dayOfWeek == SUNDAY'
  ]);
  add('j4.t4', [
    'private const val BASE = 200_000',
    '',
    'fun fee(date: LocalDate, holidays: Set<LocalDate>): Int = when {',
    '    date in holidays -> BASE * 2',
    '    date.isWeekend() -> BASE * 3 / 2',
    '    else -> BASE',
    '}',
    '',
    'private fun LocalDate.isWeekend() =',
    '    dayOfWeek == SATURDAY || dayOfWeek == SUNDAY'
  ]);
})();
