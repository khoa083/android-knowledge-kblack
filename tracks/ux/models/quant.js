/* Model định lượng track D (quant-model). Thuần, không DOM, không câu chữ. Nguồn và ví dụ kiểm chứng: docs/research/ux.md. */
(function () {
  'use strict';
  var Q = ADE.uxQuant = {};

  /* SUS (Sauro, measuringu.com/sus): câu lẻ: điểm − 1; câu chẵn: 5 − điểm; tổng × 2.5 → 0–100. KHÔNG phải phần trăm. */
  Q.sus = function (answers) {
    if (!answers || answers.length !== 10) return null;
    var sum = 0;
    for (var i = 0; i < 10; i++) { var a = answers[i]; if (!(a >= 1 && a <= 5)) return null; sum += (i % 2 === 0) ? a - 1 : 5 - a; }
    return sum * 2.5;
  };
  Q.SUS_AVERAGE = 68;   // trung bình 500 nghiên cứu (Sauro; NN/g measuring-perceived-usability)

  /* Adjusted Wald (Agresti–Coull): p̃ = (x + z²/2)/(n + z²); khoảng p̃ ± z·√(p̃(1−p̃)/(n + z²)), cắt về [0, 1].
     Nguồn: measuringu.com/wald (p̃), Wikipedia "Binomial proportion confidence interval" (Agresti–Coull). z = 1.96 cho 95%. */
  Q.Z95 = 1.96;
  Q.adjWald = function (x, n, z) {
    z = z || Q.Z95; if (!(n > 0) || x < 0 || x > n) return null;
    var nt = n + z * z, pt = (x + z * z / 2) / nt, me = z * Math.sqrt(pt * (1 - pt) / nt);
    return { p: x / n, pAdj: pt, lo: Math.max(0, pt - me), hi: Math.min(1, pt + me) };
  };
  Q.overlap = function (a, b) { return a.lo <= b.hi && b.lo <= a.hi; };

  /* Đường cong phát hiện (Nielsen, why-you-only-need-to-test-with-5-users): found(n) = 1 − (1 − L)^n; L điển hình 0.31 (giả định). */
  Q.L_DEFAULT = 0.31;
  Q.found = function (n, L) { return 1 - Math.pow(1 - L, n); };

  /* Workbench heuristic: chấm bài đánh dấu của người đọc so với đáp án. marks: {spot: {issue:bool, h:int, sev:int}} */
  Q.grade = function (answer, marks) {
    var r = { hit: [], miss: [], falsePos: [], heurOk: 0, sevClose: 0 };
    Object.keys(answer).forEach(function (sp) {
      var a = answer[sp], m = marks[sp];
      var said = m && m.issue;
      if (a.issue && said) { r.hit.push(sp); if (a.h.indexOf(m.h) >= 0) r.heurOk++; if (Math.abs((m.sev || 0) - a.sev) <= 1) r.sevClose++; }
      else if (a.issue && !said) r.miss.push(sp);
      else if (!a.issue && said) r.falsePos.push(sp);
    });
    return r;
  };
  /* Ba người đánh giá (mô hình giản lược): mỗi người tìm một tập con cố định đã định sẵn; hợp lại nhiều hơn từng người. */
  Q.union = function (sets) { var u = {}; sets.forEach(function (s) { s.forEach(function (x) { u[x] = 1; }); }); return Object.keys(u); };

  /* ---------- ví dụ kiểm chứng ---------- */
  ADE.registerCheck('ux · SUS: mọi câu bằng 3 → 50; lẻ 5 / chẵn 1 → 100; lẻ 1 / chẵn 5 → 0', function () {
    var a = Q.sus([3, 3, 3, 3, 3, 3, 3, 3, 3, 3]), b = Q.sus([5, 1, 5, 1, 5, 1, 5, 1, 5, 1]), c = Q.sus([1, 5, 1, 5, 1, 5, 1, 5, 1, 5]);
    return { pass: a === 50 && b === 100 && c === 0, detail: a + ' / ' + b + ' / ' + c };
  });
  ADE.registerCheck('ux · adjusted Wald: 20/100 → 13–29% (ví dụ của NN/g success-rate); 9/10 → p̃ ≈ 11/14 (MeasuringU)', function () {
    var r = Q.adjWald(20, 100), s = Q.adjWald(9, 10);
    var ok = Math.round(r.lo * 100) === 13 && Math.round(r.hi * 100) === 29 && Math.abs(s.pAdj - 11 / 14) < 0.01;
    return { pass: ok, detail: (r.lo * 100).toFixed(1) + '–' + (r.hi * 100).toFixed(1) + '%; p̃(9/10)=' + s.pAdj.toFixed(4) };
  });
  ADE.registerCheck('ux · đường cong phát hiện: L = 0.31, n = 5 → ≈ 84–85%', function () {
    var f = Q.found(5, 0.31); return { pass: f > 0.84 && f < 0.85, detail: (f * 100).toFixed(1) + '%' };
  });
})();
