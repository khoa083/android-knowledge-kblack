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
})();
