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
})();
