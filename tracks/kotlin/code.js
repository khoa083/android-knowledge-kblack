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
  add('eval.when', [
    'val score = 7',
    'val label = when (score) {',
    c('    in 9..10 -> "Giỏi"', '    in 9..10 -> "Excellent"'),
    c('    in 5..8 -> "Đạt"', '    in 5..8 -> "Pass"'),
    c('    else -> "Chưa đạt"', '    else -> "Not yet"'),
    '}'
  ]);
})();
