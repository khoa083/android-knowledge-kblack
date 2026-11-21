/* Model định lượng track E (thuần, không DOM, không câu chữ). Nguồn và ngày đối chiếu: docs/research/ui.md (2026-11-21). */
(function () {
  'use strict';
  var Q = ADE.uiQuant = {};

  /* ---------- WCAG 2.2: relative luminance và contrast ratio ---------- */
  Q.hex = function (h) { h = String(h).replace('#', ''); if (h.length === 3) h = h.replace(/(.)/g, '$1$1'); var n = parseInt(h, 16); return [(n >> 16) & 255, (n >> 8) & 255, n & 255]; };
  Q.toHex = function (rgb) { return '#' + rgb.map(function (v) { var s = Math.max(0, Math.min(255, Math.round(v))).toString(16); return s.length < 2 ? '0' + s : s; }).join(''); };
  Q.lum = function (hex) {
    var c = Q.hex(hex).map(function (v) { v = v / 255; return v <= 0.04045 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); });   // WCAG 2.2: ngưỡng 0.04045
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2];
  };
  Q.contrast = function (a, b) { var l1 = Q.lum(a), l2 = Q.lum(b); return (Math.max(l1, l2) + 0.05) / (Math.min(l1, l2) + 0.05); };
  /* Ngưỡng: 1.4.3 AA (4.5; chữ lớn 3), 1.4.6 AAA (7; chữ lớn 4.5), 1.4.11 AA thành phần không phải chữ (3) */
  Q.verdict = function (r) { return { aaText: r >= 4.5, aaLarge: r >= 3, aaaText: r >= 7, aaaLarge: r >= 4.5, nonText: r >= 3 }; };

  /* ---------- HSL (cho mô hình color role GIẢN LƯỢC — không phải HCT/dynamic color của Material) ---------- */
  Q.toHsl = function (hex) {
    var c = Q.hex(hex).map(function (v) { return v / 255; }), mx = Math.max.apply(null, c), mn = Math.min.apply(null, c), l = (mx + mn) / 2, s = 0, h = 0, d = mx - mn;
    if (d) { s = d / (1 - Math.abs(2 * l - 1)); h = mx === c[0] ? ((c[1] - c[2]) / d) % 6 : mx === c[1] ? (c[2] - c[0]) / d + 2 : (c[0] - c[1]) / d + 4; h *= 60; if (h < 0) h += 360; }
    return [h, s, l];
  };
  Q.fromHsl = function (h, s, l) {
    var c = (1 - Math.abs(2 * l - 1)) * s, x = c * (1 - Math.abs((h / 60) % 2 - 1)), m = l - c / 2, r = 0, g = 0, b = 0;
    if (h < 60) { r = c; g = x; } else if (h < 120) { r = x; g = c; } else if (h < 180) { g = c; b = x; } else if (h < 240) { g = x; b = c; } else if (h < 300) { r = x; b = c; } else { r = c; b = x; }
    return Q.toHex([(r + m) * 255, (g + m) * 255, (b + m) * 255]);
  };
  /* Ánh xạ giản lược: giữ hue của màu nguồn, đặt độ sáng cố định cho từng vai trò ở light/dark. */
  var LIGHT = { primary: 0.36, onPrimary: 1, primaryContainer: 0.9, onPrimaryContainer: 0.12, surface: 0.98, onSurface: 0.1, surfaceVariant: 0.9, onSurfaceVariant: 0.32, outline: 0.5, error: 0.4, onError: 1 };
  var DARK = { primary: 0.78, onPrimary: 0.18, primaryContainer: 0.3, onPrimaryContainer: 0.9, surface: 0.07, onSurface: 0.9, surfaceVariant: 0.3, onSurfaceVariant: 0.8, outline: 0.6, error: 0.8, onError: 0.2 };
  Q.PAIRS = [['onPrimary', 'primary'], ['onPrimaryContainer', 'primaryContainer'], ['onSurface', 'surface'], ['onSurfaceVariant', 'surfaceVariant'], ['onError', 'error']];
  Q.roles = function (src, dark, lightShift) {
    var hsl = Q.toHsl(src), T = dark ? DARK : LIGHT, out = {}, sh = lightShift || 0;
    Object.keys(T).forEach(function (k) {
      var neutral = /surface|outline|onSurface/i.test(k), hue = /error/i.test(k) ? 4 : hsl[0], sat = /error/i.test(k) ? 0.7 : neutral ? Math.min(0.12, hsl[1]) : Math.max(0.35, hsl[1]);
      var l = T[k]; if (k === 'primary') l = Math.max(0.05, Math.min(0.95, l + sh));
      out[k] = Q.fromHsl(hue, sat, Math.max(0, Math.min(1, l)));
    });
    return out;
  };
  Q.rolePairs = function (r) { return Q.PAIRS.map(function (p) { var c = Q.contrast(r[p[0]], r[p[1]]); return { fg: p[0], bg: p[1], ratio: c, ok: c >= 4.5 }; }); };

  /* ---------- mù màu (bộ lọc GIẢN LƯỢC): ma trận tuyến tính trên sRGB, chỉ để minh họa ---------- */
  Q.CVD = {
    protan: [[0.567, 0.433, 0], [0.558, 0.442, 0], [0, 0.242, 0.758]],
    deutan: [[0.625, 0.375, 0], [0.7, 0.3, 0], [0, 0.3, 0.7]],
    gray: [[0.299, 0.587, 0.114], [0.299, 0.587, 0.114], [0.299, 0.587, 0.114]]
  };
  Q.simulate = function (hex, kind) { var m = Q.CVD[kind]; if (!m) return hex; var c = Q.hex(hex); return Q.toHex(m.map(function (r) { return r[0] * c[0] + r[1] * c[1] + r[2] * c[2]; })); };

  /* ---------- Fitts (biến thể Shannon, MacKenzie): MT = a + b·log2(D/W + 1). a, b: hệ số minh họa ---------- */
  Q.fitts = function (D, W, a, b) { return a + b * Math.log(D / W + 1) / Math.LN2; };

  /* ---------- window size class (Android, use-window-size-classes) ---------- */
  Q.widthClass = function (dp) { return dp < 600 ? 'compact' : dp < 840 ? 'medium' : dp < 1200 ? 'expanded' : dp < 1600 ? 'large' : 'xlarge'; };

  /* ---------- token đã đối chiếu (m3.material.io, 2026-11-21) ---------- */
  Q.TYPE = { displayLarge: [57, 64], displayMedium: [45, 52], displaySmall: [36, 44], headlineLarge: [32, 40], headlineMedium: [28, 36], headlineSmall: [24, 32],
    titleLarge: [22, 28], titleMedium: [16, 24], titleSmall: [14, 20], bodyLarge: [16, 24], bodyMedium: [14, 20], bodySmall: [12, 16], labelLarge: [14, 20], labelMedium: [12, 16], labelSmall: [11, 16] };
  Q.EASING = { standard: [0.2, 0, 0, 1], standardDecelerate: [0, 0, 0, 1], standardAccelerate: [0.3, 0, 1, 1], emphasizedDecelerate: [0.05, 0.7, 0.1, 1], emphasizedAccelerate: [0.3, 0, 0.8, 0.15] };
  Q.DURATION = { short2: 100, short4: 200, medium2: 300, medium4: 400, long2: 500, extraLong2: 800 };
  Q.STATE_LAYER = { hover: 0.08, focus: 0.10, pressed: 0.10, dragged: 0.16 };

  /* ---------- ví dụ kiểm chứng ---------- */
  ADE.registerCheck('ui · WCAG: đen/trắng = 21:1; cùng màu = 1:1', function () {
    var a = Q.contrast('#000000', '#ffffff'), b = Q.contrast('#3a7bd5', '#3a7bd5'); return { pass: Math.abs(a - 21) < 1e-9 && Math.abs(b - 1) < 1e-9, detail: a.toFixed(3) + ' / ' + b.toFixed(3) };
  });
  ADE.registerCheck('ui · WCAG: #767676 trên trắng ≈ 4.54:1 (đạt 1.4.3 AA cho chữ thường)', function () {
    var r = Q.contrast('#767676', '#ffffff'); return { pass: r > 4.5 && r < 4.6 && Q.verdict(r).aaText, detail: r.toFixed(3) };
  });
  ADE.registerCheck('ui · size class: 599 → compact, 600 → medium, 840 → expanded, 1200 → large', function () {
    return { pass: Q.widthClass(599) === 'compact' && Q.widthClass(600) === 'medium' && Q.widthClass(840) === 'expanded' && Q.widthClass(1200) === 'large' && Q.widthClass(1600) === 'xlarge', detail: 'ok' };
  });
  ADE.registerCheck('ui · Fitts: D = 0 → MT = a; tăng D thì MT tăng', function () { return { pass: Q.fitts(0, 48, 100, 150) === 100 && Q.fitts(400, 48, 100, 150) > Q.fitts(100, 48, 100, 150), detail: 'ok' }; });
  ADE.registerCheck('ui · color role giản lược: light và dark là hai bảng khác nhau (không phải đảo màu)', function () {
    var l = Q.roles('#3a7bd5', false), d = Q.roles('#3a7bd5', true), inv = Q.toHex(Q.hex(l.surface).map(function (v) { return 255 - v; }));
    return { pass: l.surface !== d.surface && d.surface !== inv, detail: l.surface + ' / ' + d.surface + ' / đảo=' + inv };
  });
})();
