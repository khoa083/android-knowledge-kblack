/* Mô hình số của track C (thuần, không DOM, không câu chữ). MÔ HÌNH GIẢNG DẠY: không khớp từng frame với Compose.
   Hằng số và nguồn: docs/research/animation.md (animation-core 1.13.0; Easing.kt và FloatDecayAnimationSpec.kt ở androidx-main, đọc 2026-11-21).
   Đơn vị: giá trị là số thực (ví dụ px minh họa), thời gian ms, vận tốc đơn-vị/giây. */
(function () {
  'use strict';
  var P = ADE.animPhys = {};

  /* ---------- hằng số có nguồn ---------- */
  P.DAMPING = { HighBouncy: 0.2, MediumBouncy: 0.5, LowBouncy: 0.75, NoBouncy: 1.0 };          // reference Spring
  P.STIFFNESS = { Medium: 1500, MediumLow: 400, Low: 200, VeryLow: 50 };                     // reference Spring (StiffnessHigh không xác minh → không dùng)
  P.DEFAULT_DURATION = 300;                                                                  // AnimationConstants.DefaultDurationMillis
  P.EASING = {                                                                              // Easing.kt (androidx-main)
    FastOutSlowIn: [0.4, 0.0, 0.2, 1.0], LinearOutSlowIn: [0.0, 0.0, 0.2, 1.0], FastOutLinearIn: [0.4, 0.0, 1.0, 1.0], Linear: null
  };
  P.DECAY_FRICTION = -4.2;                                                                  // ExponentialDecayFriction (FloatDecayAnimationSpec.kt)
  P.DECAY_THRESHOLD = 0.1;                                                                  // exponentialDecay(absVelocityThreshold = 0.1f)

  /* ---------- cubic-bezier: x(s), y(s) với P0=(0,0), P3=(1,1); giải s theo x bằng Newton + chia đôi ---------- */
  P.bezier = function (pts) {
    if (!pts) return function (x) { return x; };
    var x1 = pts[0], y1 = pts[1], x2 = pts[2], y2 = pts[3];
    var B = function (a, b, s) { var u = 1 - s; return 3 * u * u * s * a + 3 * u * s * s * b + s * s * s; };
    var dB = function (a, b, s) { var u = 1 - s; return 3 * u * u * a + 6 * u * s * (b - a) + 3 * s * s * (1 - b); };
    return function (x) {
      if (x <= 0) return 0; if (x >= 1) return 1;
      var s = x, i;
      for (i = 0; i < 8; i++) { var e = B(x1, x2, s) - x, d = dB(x1, x2, s); if (Math.abs(e) < 1e-6) break; if (Math.abs(d) < 1e-6) break; s -= e / d; }
      if (s < 0 || s > 1 || Math.abs(B(x1, x2, s) - x) > 1e-4) { var lo = 0, hi = 1; for (i = 0; i < 40; i++) { s = (lo + hi) / 2; if (B(x1, x2, s) < x) lo = s; else hi = s; } }
      return B(y1, y2, s);
    };
  };

  /* ---------- spring: dao động điều hòa tắt dần, khối lượng 1. x là độ lệch so với target ----------
     ω0 = √k, ζ = dampingRatio.
     ζ < 1 : x(t) = e^(−ζω0t)·(x0·cos ωd t + (v0 + ζω0x0)/ωd · sin ωd t), ωd = ω0√(1−ζ²)
     ζ = 1 : x(t) = e^(−ω0t)·(x0 + (v0 + ω0x0)·t)
     ζ > 1 : x(t) = c1·e^(r1 t) + c2·e^(r2 t), r1,2 = −ω0(ζ ∓ √(ζ²−1)), c1 = (v0 − r2x0)/(r1 − r2), c2 = x0 − c1 */
  P.springX = function (x0, v0, k, z, t) {
    var w0 = Math.sqrt(k);
    if (Math.abs(z - 1) < 1e-6) return Math.exp(-w0 * t) * (x0 + (v0 + w0 * x0) * t);
    if (z < 1) { var wd = w0 * Math.sqrt(1 - z * z); return Math.exp(-z * w0 * t) * (x0 * Math.cos(wd * t) + (v0 + z * w0 * x0) / wd * Math.sin(wd * t)); }
    var q = Math.sqrt(z * z - 1), r1 = -w0 * (z - q), r2 = -w0 * (z + q), c1 = (v0 - r2 * x0) / (r1 - r2), c2 = x0 - c1;
    return c1 * Math.exp(r1 * t) + c2 * Math.exp(r2 * t);
  };

  /* ---------- đoạn animation: {type, from, to, v0, spec} → sample(tMs) = {value, velocity|null, done} ---------- */
  P.sample = function (seg, tMs) {
    var s = seg.spec, from = seg.from, to = seg.to, t = Math.max(0, tMs);
    if (s.type === 'spring') {
      var ts = t / 1000, x0 = from - to, x = P.springX(x0, seg.v0 || 0, s.stiffness, s.damping, ts);
      var h = 1e-4, v = (P.springX(x0, seg.v0 || 0, s.stiffness, s.damping, ts + h) - P.springX(x0, seg.v0 || 0, s.stiffness, s.damping, Math.max(0, ts - h))) / (ts > h ? 2 * h : h);
      var thr = s.threshold || 0.01 * Math.max(1, Math.abs(x0));
      var done = Math.abs(x) < thr && Math.abs(v) < thr * 10;
      return { value: done ? to : to + x, velocity: done ? 0 : v, done: done };
    }
    if (s.type === 'tween') {
      var d = s.duration, dl = s.delay || 0, f = d <= 0 ? 1 : Math.min(1, Math.max(0, (t - dl) / d));
      return { value: from + (to - from) * P.bezier(P.EASING[s.easing])(f), velocity: null, done: t >= dl + d };
    }
    if (s.type === 'keyframes') {
      // mốc {at: ms, f: tỉ lệ 0..1 trên đoạn from→to}; nội suy tuyến tính giữa các mốc (giản lược)
      var ks = [{ at: 0, f: 0 }].concat(s.frames).concat([{ at: s.duration, f: 1 }]), k = 0;
      if (t >= s.duration) return { value: to, velocity: null, done: true };
      while (k < ks.length - 2 && t > ks[k + 1].at) k++;
      var a = ks[k], b = ks[k + 1], u = b.at === a.at ? 1 : (t - a.at) / (b.at - a.at);
      return { value: from + (to - from) * (a.f + (b.f - a.f) * u), velocity: null, done: false };
    }
    if (s.type === 'repeat') {
      // repeatable / infiniteRepeatable quanh một tween; RepeatMode.Restart hoặc Reverse
      var D = s.duration, i = Math.floor(t / D), loc = t - i * D, n = s.iterations;   // n = Infinity cho infiniteRepeatable
      if (i >= n) { var endFwd = s.mode === 'Restart' || n % 2 === 1; return { value: endFwd ? to : from, velocity: null, done: true }; }
      if (s.mode === 'Reverse' && i % 2 === 1) loc = D - loc;
      return { value: from + (to - from) * P.bezier(P.EASING[s.easing])(loc / D), velocity: null, done: false };
    }
    if (s.type === 'snap') return { value: t >= (s.delay || 0) ? to : from, velocity: null, done: t >= (s.delay || 0) };
    if (s.type === 'decay') {
      // FloatExponentialDecaySpec: friction = −4.2·multiplier; v(t) = v0·e^(friction·t); x(t) = x0 − v0/friction + v0/friction·e^(friction·t)
      var fr = P.DECAY_FRICTION * Math.max(0.0001, s.multiplier || 1), tt = t / 1000, v0 = seg.v0 || 0;
      var dur = v0 === 0 ? 0 : Math.max(0, Math.log(P.DECAY_THRESHOLD / Math.abs(v0)) / fr);
      var te = Math.min(tt, dur);
      return { value: from - v0 / fr + v0 / fr * Math.exp(fr * te), velocity: tt >= dur ? 0 : v0 * Math.exp(fr * te), done: tt >= dur };
    }
    return { value: to, velocity: null, done: true };
  };
  P.decayTarget = function (from, v0, multiplier) { var fr = P.DECAY_FRICTION * Math.max(0.0001, multiplier || 1); return from - v0 / fr; };
  P.hasVelocity = function (spec) { return spec.type === 'spring' || spec.type === 'decay'; };

  /* ---------- ví dụ kiểm chứng ---------- */
  var sp = function (z, k) { return { type: 'spring', damping: z, stiffness: k }; };
  ADE.registerCheck('animation · spring hội tụ về target (ba chế độ tắt dần)', function () {
    var ok = [0.2, 1.0, 2.0].every(function (z) { var r = P.sample({ from: 0, to: 100, v0: 0, spec: sp(z, 1500) }, 3000); return Math.abs(r.value - 100) < 0.5; });
    return { pass: ok, detail: 'z=0.2,1,2 @3s' };
  });
  ADE.registerCheck('animation · spring underdamped vượt target, critically damped thì không', function () {
    var maxOf = function (z) { var m = -1e9; for (var t = 0; t <= 1500; t += 4) m = Math.max(m, P.sample({ from: 0, to: 100, v0: 0, spec: sp(z, 400) }, t).value); return m; };
    var a = maxOf(0.2), b = maxOf(1.0);
    return { pass: a > 100.5 && b <= 100.0001, detail: 'max(0.2)=' + a.toFixed(2) + ' max(1)=' + b.toFixed(4) };
  });
  ADE.registerCheck('animation · tween: t=0 bằng start, t=duration bằng target', function () {
    var seg = { from: 10, to: 90, spec: { type: 'tween', duration: 300, easing: 'FastOutSlowIn' } }, a = P.sample(seg, 0).value, b = P.sample(seg, 300).value;
    return { pass: Math.abs(a - 10) < 1e-9 && Math.abs(b - 90) < 1e-9, detail: 'v(0)=' + a + ' v(300)=' + b };
  });
  ADE.registerCheck('animation · cubic-bezier FastOutSlowIn: đơn điệu, f(0.5) > 0.5', function () {
    var f = P.bezier(P.EASING.FastOutSlowIn), prev = -1, mono = true;
    for (var x = 0; x <= 1.0001; x += 0.01) { var y = f(x); if (y < prev - 1e-9) mono = false; prev = y; }
    return { pass: mono && f(0.5) > 0.5 && Math.abs(f(1) - 1) < 1e-9, detail: 'f(0.5)=' + f(0.5).toFixed(3) };
  });
  ADE.registerCheck('animation · decay: vận tốc giảm dần, dừng tại x0 − v0/friction', function () {
    var seg = { from: 0, to: 0, v0: 1000, spec: { type: 'decay', multiplier: 1 } }, dec = true, prev = Infinity;
    for (var t = 0; t <= 3000; t += 50) { var v = P.sample(seg, t).velocity; if (v > prev + 1e-9) dec = false; prev = v; }
    var end = P.sample(seg, 10000).value, exp = P.decayTarget(0, 1000, 1);
    return { pass: dec && Math.abs(end - exp) < 0.1, detail: 'end=' + end.toFixed(2) + ' expected≈' + exp.toFixed(2) };
  });
  ADE.registerCheck('animation · repeatable Reverse 2 lần kết thúc ở start; Restart kết thúc ở target', function () {
    var base = { from: 0, to: 100, spec: { type: 'repeat', duration: 200, iterations: 2, easing: 'Linear' } };
    base.spec.mode = 'Reverse'; var a = P.sample(base, 500).value; base.spec.mode = 'Restart'; var b = P.sample(base, 500).value;
    return { pass: a === 0 && b === 100, detail: 'Reverse=' + a + ' Restart=' + b };
  });
})();
