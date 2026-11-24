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

  /* J5: test "phí cuối tuần" viết hai cách: mock từng lời gọi (MockK, minh họa) và kiểm kết quả với fake theo AAA */
  add('j5.mock', [
    c('@Test fun `phí cuối tuần`() {', '@Test fun `weekend fee`() {'),
    '    val fees = mockk<FeeCalculator>()',
    c('    every { fees.feeFor(SATURDAY) } returns 300_000         // mã tính phí thật không chạy', '    every { fees.feeFor(SATURDAY) } returns 300_000         // the real fee code never runs'),
    '    val repo = mockk<Repo>(relaxed = true)',
    '    BookingService(validator, fees, repo, reminders).book(request(on = SATURDAY))',
    c('    verify { fees.feeFor(SATURDAY) }                          // kiểm cách làm', '    verify { fees.feeFor(SATURDAY) }                          // checks how, not what'),
    '    verify { repo.save(match { it.fee == 300_000 }) }',
    '}'
  ]);
  add('j5.behavior', [
    c('@Test fun `phí cuối tuần`() {', '@Test fun `weekend fee`() {'),
    c('    val repo = FakeRepo()                                     // arrange', '    val repo = FakeRepo()                                     // arrange'),
    '    val service = bookingService(repo = repo, holidays = emptySet())',
    '',
    c('    service.book(request(on = SATURDAY))                      // act', '    service.book(request(on = SATURDAY))                      // act'),
    '',
    c('    assertEquals(300_000, repo.saved.single().fee)            // assert: kết quả', '    assertEquals(300_000, repo.saved.single().fee)            // assert: the outcome'),
    '}'
  ]);

  /* J6: đổi tại chỗ (j6.big, nhật ký theo giờ) và song song kiểu strangler (j6.small) */
  add('j6.big', [
    'data class Appointment(',
    c('    val time: LocalDateTime,                  // đổi tại chỗ: mọi nơi đọc chuỗi đều vỡ', '    val time: LocalDateTime,                  // changed in place: every string reader breaks'),
    ')',
    c('// 13:00  17 lỗi biên dịch ở 6 file', '// 13:00  17 compile errors in 6 files'),
    c('// 15:00  40 lỗi biên dịch ở 12 file', '// 15:00  40 compile errors in 12 files'),
    c('// 17:30  biên dịch được; 3 test đỏ: do thay đổi nào trong 8?', '// 17:30  it compiles; 3 tests fail: which of the 8 changes?'),
    '// 18:00  git reset --hard before-refactor'
  ]);
  add('j6.small', [
    'data class Appointment(',
    c('    @Deprecated("dùng startsAt") val time: String,', '    @Deprecated("use startsAt") val time: String,'),
    c('    val startsAt: LocalDateTime? = null,      // bước 1: đặt cạnh cái cũ', '    val startsAt: LocalDateTime? = null,      // step 1: placed beside the old'),
    ')',
    c('// bước 2: kho dữ liệu ghi cả hai trường', '// step 2: storage writes both fields'),
    c('val sorted = items.sortedBy { it.startsAt }                          // bước 3, 6', 'val sorted = items.sortedBy { it.startsAt }                          // steps 3, 6'),
    c('reminders.schedule(a.startsAt!!.toInstant(ZoneOffset.UTC))           // bước 4: đỏ, lệch 7 tiếng', 'reminders.schedule(a.startsAt!!.toInstant(ZoneOffset.UTC))           // step 4: red, 7 hours off'),
    c('reminders.schedule(a.startsAt!!.atZone(clinicZone).toInstant())      // bước 4′: xanh', 'reminders.schedule(a.startsAt!!.atZone(clinicZone).toInstant())      // step 4′: green'),
    c('// bước 8: xóa time khi không còn ai đọc', '// step 8: delete time when nothing reads it')
  ]);

  /* J7: lùi từng commit (j7.linear) và chia đôi tự động (j7.bisect); test tái hiện ở dòng 4 của mỗi đoạn */
  add('j7.linear', [
    c('# test tái hiện: ReminderTimeTest (cố định múi giờ Asia/Ho_Chi_Minh)', '# reproducing test: ReminderTimeTest (pins the Asia/Ho_Chi_Minh zone)'),
    c('git checkout HEAD~1                     # lùi một commit', 'git checkout HEAD~1                     # step back one commit'),
    './gradlew testDebugUnitTest --tests "*ReminderTimeTest"',
    c('# lặp lại hai dòng trên: 64 lần, khoảng 3 phút mỗi lần', '# repeat the two lines above: 64 times, about 3 minutes each')
  ]);
  add('j7.bisect', [
    'git bisect start',
    c('git bisect bad HEAD                     # commit 200: có lỗi', 'git bisect bad HEAD                     # commit 200: broken'),
    c('git bisect good v1.4                    # commit 0: chưa có lỗi', 'git bisect good v1.4                    # commit 0: fine'),
    'git bisect run ./gradlew testDebugUnitTest --tests "*ReminderTimeTest"',
    c('# mã thoát 0 = tốt; 1–127 trừ 125 = xấu; 125 = bỏ qua commit không build được', '# exit 0 = good; 1–127 except 125 = bad; 125 = skip a commit that does not build'),
    '# ... 137 is the first bad commit',
    'git bisect reset'
  ]);

  /* J8: thiết kế when theo chuỗi (j8.switch) và thiết kế theo SOLID (j8.solid) */
  add('j8.switch', [
    c('class AppointmentManager {                 // lịch + phí + thông báo: 3 nhóm người cùng sửa (SRP)', 'class AppointmentManager {                 // schedule + fees + notifications: 3 groups edit it (SRP)'),
    '    fun fee(method: String, amount: Long) = when (method) {',
    '        "cash" -> 0L',
    '        "card" -> amount * 2 / 100',
    c('        else -> 0L                            // MoMo rơi vào đây: phí 0', '        else -> 0L                            // MoMo lands here: a 0 fee'),
    '    }',
    c('    // cùng kiểu when (method) ở pay(), receipt(), refund(), analytics(): 5 nơi (OCP)', '    // the same when (method) in pay(), receipt(), refund(), analytics(): 5 places (OCP)'),
    '}',
    'class InsurancePayment : CardPayment() {',
    '    override fun refund(id: String) = throw UnsupportedOperationException()   // LSP',
    '}',
    c('class BookingService(private val vnpay: VnPaySdkClient)     // nghiệp vụ → SDK (DIP)', 'class BookingService(private val vnpay: VnPaySdkClient)     // policy → SDK (DIP)')
  ]);
  add('j8.solid', [
    c('class BookingScheduler      // lễ tân', 'class BookingScheduler      // front desk'),
    c('class FeePolicy             // kế toán', 'class FeePolicy             // accounting'),
    c('class ReminderComposer      // marketing', 'class ReminderComposer      // marketing'),
    'sealed interface PaymentMethod { fun fee(amount: Long): Long }',
    c('class MoMo(val phone: PhoneNumber) : PaymentMethod, Refundable { /* ... */ }   // thêm: 1 file', 'class MoMo(val phone: PhoneNumber) : PaymentMethod, Refundable { /* ... */ }   // added: 1 file'),
    'interface Refundable { suspend fun refund(id: PaymentId) }',
    c('class Insurance(val policy: PolicyNo) : PaymentMethod { /* không hứa hoàn tiền */ }', 'class Insurance(val policy: PolicyNo) : PaymentMethod { /* promises no refund */ }'),
    c('interface PaymentGateway { suspend fun charge(m: PaymentMethod, amount: Long) }   // nghiệp vụ sở hữu', 'interface PaymentGateway { suspend fun charge(m: PaymentMethod, amount: Long) }   // owned by the policy'),
    'class BookingService(private val gateway: PaymentGateway)',
    c('class VnPayGateway(private val sdk: VnPaySdkClient) : PaymentGateway { /* ... */ }   // nơi duy nhất import SDK', 'class VnPayGateway(private val sdk: VnPaySdkClient) : PaymentGateway { /* ... */ }   // the only SDK import')
  ]);

  /* J9: khai báo phụ thuộc Gradle của hai cách chia module */
  add('j9.common', [
    c('// :core:common: model, định dạng, tên sự kiện analytics… "ai cũng cần"', '// :core:common: models, formatting, analytics event names… "everyone needs it"'),
    'dependencies {',
    c('    implementation(project(":core:analytics"))   // module ổn định phụ thuộc module kém ổn định (SDP)', '    implementation(project(":core:analytics"))   // a stable module depending on a less stable one (SDP)'),
    '}',
    c('// :feature:booking, :feature:profile, :feature:reminder, :core:data, :app đều có:', '// :feature:booking, :feature:profile, :feature:reminder, :core:data and :app all have:'),
    '//     implementation(project(":core:common"))'
  ]);
  add('j9.split', [
    c('// :core:model: chỉ data class và giao diện (AnalyticsTracker); không phụ thuộc gì', '// :core:model: only data classes and interfaces (AnalyticsTracker); depends on nothing'),
    'dependencies { }',
    c('// :feature:booking: tên sự kiện và định dạng của chính nó nằm ở đây (CCP)', '// :feature:booking: its own event names and formatting live here (CCP)'),
    'dependencies {',
    '    implementation(project(":core:model"))',
    '    implementation(project(":core:data"))',
    '}',
    c('// :core:analytics cài AnalyticsTracker: implementation(project(":core:model"))   (DIP)', '// :core:analytics implements AnalyticsTracker: implementation(project(":core:model"))   (DIP)')
  ]);

  /* J10: git log --oneline của hai cách làm (dòng 1–4: PR lớn; j10.small: sáu PR) */
  add('j10.big', [
    'a91c0e2 update booking + phone + reminder + fee + momo + format',
    'f03d7b1 wip',
    '7c2e9a4 fix 2',
    '5b18d63 fix'
  ]);
  add('j10.small', [
    '3e7f0a1 Charge MoMo payments through PaymentGateway',
    '9d2c4b8 Split FeePolicy out of AppointmentManager',
    '61a8e03 Schedule reminders in the clinic time zone',
    'c4f19d2 Parse phone numbers at the booking boundary',
    '0b7e5a6 Add PhoneNumber value class',
    '8a3d2f9 Reformat booking module (no behaviour change)'
  ]);
})();
