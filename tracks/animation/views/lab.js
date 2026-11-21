/* Lab dùng chung của track C: preview, đồ thị value-over-time, bảng current/target/velocity, điều khiển
   Play/Pause/Step Frame/Restart/Đổi target/Reset, khoảng frame minh họa, nhật ký sự kiện; C6 có thêm kéo và fling.
   Gắn qua view.mount của model kind 'compute' (lõi gọi mount cho loại này). Trạng thái lưu trong ADE.animLab.store
   nên đổi ngôn ngữ (dựng lại trang) giữ nguyên thời điểm, target và spec. Mọi chữ là message key. */
(function () {
  'use strict';
  var Ph = ADE.animPhys, K = 'track.animation.lab.';
  var L = ADE.animLab = { store: {}, keys: [] };
  var T = function (k, p) { L.keys.indexOf(K + k) < 0 && L.keys.push(K + k); return ADE.t(K + k, p); };
  var R1 = function (v, d) { var f = Math.pow(10, d == null ? 1 : d); return Math.round(v * f) / f; };   // số thô cho tham số nhật ký (định dạng lúc hiển thị)
  var N = function (v, d) { return v == null || isNaN(v) ? '—' : ADE.num(+v.toFixed(d == null ? 1 : d)); };

  var STYLE = '.alab{display:grid;gap:12px;min-width:0}.alab>*{min-width:0}.alab .code-wrap,.alab pre{max-width:100%;overflow-x:auto;position:relative}.alab .row{display:flex;flex-wrap:wrap;gap:8px;align-items:flex-end}' +
    '.alab-top{display:grid;grid-template-columns:minmax(0,1.4fr) minmax(0,1fr);gap:12px}@media(max-width:760px){.alab-top{grid-template-columns:minmax(0,1fr)}}' +
    '.alab-prev{position:relative;height:72px;border:1px solid var(--line-strong);border-radius:var(--radius);background:var(--paper);overflow:hidden;touch-action:none}' +
    '.alab-rail{position:absolute;left:24px;right:24px;top:50%;border-top:1px dashed var(--line-strong)}' +
    '.alab-tgt{position:absolute;top:14px;bottom:14px;width:0;border-left:2px solid var(--tok-state)}' +
    '.alab-puck{position:absolute;top:50%;width:28px;height:28px;margin:-14px 0 0 -14px;border-radius:50%;border:2px solid var(--ink);background:var(--tok-anim);cursor:grab}' +
    '.alab-puck:focus-visible{outline:2px solid var(--focus);outline-offset:2px}.alab-tbl{width:100%;border-collapse:collapse;font:12px var(--mono)}' +
    '.alab-tbl th{text-align:left;color:var(--ink-2);font-weight:600;padding:3px 6px}.alab-tbl td{text-align:right;padding:3px 6px}.alab-tbl tr{border-bottom:1px solid var(--line)}' +
    '.alab-g{width:100%;height:auto;display:block;border:1px solid var(--line);border-radius:var(--radius);background:var(--paper)}' +
    '.alab-g .ax{stroke:var(--line-strong);stroke-width:1}.alab-g .hist{fill:none;stroke:var(--tok-anim);stroke-width:2.5}.alab-g .pred{fill:none;stroke:var(--ink-2);stroke-width:1.5;stroke-dasharray:5 4}' +
    '.alab-g .tg{stroke:var(--tok-state);stroke-width:1.5;stroke-dasharray:2 3}.alab-g text{font:11px var(--mono);fill:var(--ink-2)}.alab-g .now{stroke:var(--ink);stroke-width:1}' +
    '.alab-log{list-style:none;margin:0;padding:0;font:12px var(--mono);max-height:180px;overflow:auto}.alab-log li{padding:3px 0;border-bottom:1px solid var(--line);display:flex;gap:8px}' +
    '.alab-log b{min-width:110px}.alab-clock{display:flex;gap:12px;flex-wrap:wrap}.alab-clock div{border:1px solid var(--line-strong);border-radius:var(--radius);padding:6px 10px;font:12px var(--mono)}' +
    '.alab-clock strong{display:block;font-size:16px}';
  function injectStyle() { if (document.getElementById('alab-style')) return; var s = document.createElement('style'); s.id = 'alab-style'; s.textContent = STYLE; document.head.appendChild(s); }

  /* ---------- trạng thái ---------- */
  var SPEC_DEFAULT = { type: 'spring', damping: 'NoBouncy', stiffness: 'Medium', duration: 300, easing: 'FastOutSlowIn', mode: 'Reverse', iterations: 2, delay: 150, multiplier: 1, v0: 600 };
  function specOf(c) {
    if (c.type === 'spring') return { type: 'spring', damping: Ph.DAMPING[c.damping], stiffness: Ph.STIFFNESS[c.stiffness] };
    if (c.type === 'tween') return { type: 'tween', duration: c.duration, easing: c.easing };
    if (c.type === 'keyframes') return { type: 'keyframes', duration: c.duration, frames: [{ at: c.duration * 0.25, f: 0.6 }, { at: c.duration * 0.6, f: 0.4 }] };
    if (c.type === 'repeat') return { type: 'repeat', duration: c.duration, iterations: c.iterations, mode: c.mode, easing: c.easing };
    if (c.type === 'infinite') return { type: 'repeat', duration: c.duration, iterations: Infinity, mode: c.mode, easing: c.easing };
    if (c.type === 'snap') return { type: 'snap', delay: c.delay };
    return { type: 'decay', multiplier: c.multiplier };
  }
  function fresh(kind) {
    var st = { kind: kind, T: 0, t: 0, frameMs: 16, playing: false, spec: JSON.parse(JSON.stringify(SPEC_DEFAULT)), start: 0, target: 100, slider: 60, hist: [], log: [], pointer: null, dismissed: false };
    if (kind === 'gesture') { st.target = 0; st.start = 0; st.spec.type = 'spring'; st.spec.damping = 'LowBouncy'; st.spec.stiffness = 'MediumLow'; }
    st.seg = { from: st.start, to: st.target, v0: st.spec.type === 'decay' ? st.spec.v0 : 0, spec: specOf(st.spec) };
    if (kind === 'gesture') st.seg = null;
    st.hist.push({ T: 0, v: st.start });
    return st;
  }
  L.cur = function (st) { return st.seg ? Ph.sample(st.seg, st.t) : { value: st.hist.length ? st.hist[st.hist.length - 1].v : st.start, velocity: 0, done: true }; };
  L.log = function (st, kind, key, params) { st.log.push({ T: st.T, kind: kind, key: key, params: params || {} }); if (st.log.length > 40) st.log.shift(); };
  L.retarget = function (st, to) {
    var c = L.cur(st), keepV = st.seg && st.seg.spec.type === 'spring';
    st.seg = { from: c.value, to: to, v0: keepV ? (c.velocity || 0) : 0, spec: specOf(st.spec) }; st.t = 0; st.target = to;
    L.log(st, 'target-change', keepV ? 'ev.retargetSpring' : 'ev.retargetOther', { from: R1(c.value), to: R1(to), v: R1(keepV ? c.velocity : 0) });
  };
  L.step = function (st) {
    if (!st.seg) return;
    var before = L.cur(st); if (before.done && st.t > 0) { st.playing = false; return; }
    st.t += st.frameMs; st.T += st.frameMs;
    var c = L.cur(st); st.hist.push({ T: st.T, v: c.value }); if (st.hist.length > 600) st.hist.shift();
    if (c.done) {
      st.playing = false;
      if (st.kind === 'gesture' && st.seg.spec.type === 'decay') { L.log(st, 'settle', 'ev.dismissed', { v: R1(c.value) }); st.dismissed = true; st.seg = null; return; }
      L.log(st, 'settle', 'ev.settle', { v: R1(c.value), t: R1(st.T, 0) });
    }
  };
  L.restart = function (st) {
    st.T = 0; st.t = 0; st.hist = [{ T: 0, v: st.start }]; st.log = []; st.playing = false; st.dismissed = false;
    st.seg = st.kind === 'gesture' ? null : { from: st.start, to: st.target, v0: st.spec.type === 'decay' ? st.spec.v0 : 0, spec: specOf(st.spec) };
    if (st.seg) L.log(st, 'target-change', 'ev.start', { from: R1(st.start), to: R1(st.target) });
  };
  /* gesture (theo ví dụ "advanced"): chạm → stop(); kéo → snapTo; thả → dự đoán đích bằng decay; trong biên → animateTo(0, initialVelocity), ngoài biên → animateDecay rồi bị loại */
  L.BOUND = 120;
  L.touch = function (st) {
    var c = L.cur(st);
    if (st.seg && !c.done) { L.log(st, 'interrupt', 'ev.stop', { v: R1(c.value) }); }
    st.seg = null; st.playing = false; st.hist.push({ T: st.T, v: c.value }); st.pointer = c.value; st.dismissed = false;
  };
  L.drag = function (st, dx) {
    if (st.pointer == null) L.touch(st);
    st.pointer = Math.max(-L.BOUND * 1.4, Math.min(L.BOUND * 1.4, st.pointer + dx)); st.T += st.frameMs; st.hist.push({ T: st.T, v: st.pointer });
    L.log(st, 'frame', 'ev.snap', { v: R1(st.pointer) });
  };
  L.release = function (st, v) {
    var from = st.pointer == null ? L.cur(st).value : st.pointer, pred = Ph.decayTarget(from, v, 1);
    st.pointer = null; st.t = 0;
    if (Math.abs(pred) <= L.BOUND) { st.seg = { from: from, to: 0, v0: v, spec: specOf(st.spec) }; st.target = 0; L.log(st, 'target-change', 'ev.back', { v: R1(v, 0), p: R1(pred) }); }
    else { st.seg = { from: from, to: pred, v0: v, spec: { type: 'decay', multiplier: 1 } }; st.target = pred; L.log(st, 'target-change', 'ev.fling', { v: R1(v, 0), p: R1(pred) }); }
  };

  /* ---------- dựng DOM (một lần) và cập nhật (render) để không mất focus ---------- */
  L.mount = function (container, kind, modelId) {
    injectStyle();
    var h = ADE.ui.h, key = modelId, st = L.store[key] || (L.store[key] = fresh(kind));
    var root = h('div', { class: 'alab panel pad' }); container.appendChild(root);
    var raf = 0, acc = 0, last = 0, onKey = null;
    var reduced = function () { return ADE.motionReduced(); };
    // tiêu đề + badge
    root.appendChild(h('header', { class: 'panel-h' }, h('h2', { class: 'caps', text: T('title.' + kind) }), h('span', { class: 'badge badge-simplified conceptual', text: ADE.t('app.conceptual') })));
    var top = h('div', { class: 'alab-top' }); root.appendChild(top);
    var prev = h('div', { class: 'alab-prev', role: 'img', 'aria-label': T('preview') }), rail = h('div', { class: 'alab-rail' }), tgt = h('div', { class: 'alab-tgt' });
    var puck = h('div', { class: 'alab-puck', tabindex: kind === 'gesture' ? '0' : null, 'data-fk': 'lab-puck', role: kind === 'gesture' ? 'slider' : null, 'aria-label': T('puck') });
    prev.appendChild(rail); prev.appendChild(tgt); prev.appendChild(puck);
    var left = h('div', null, h('h3', { class: 'caps sub', text: T('preview') }), prev); top.appendChild(left);
    var tbl = h('table', { class: 'alab-tbl' }), cells = {};
    ['time', 'current', 'target', 'velocity', 'frame'].concat(kind === 'gesture' ? ['pointer'] : []).forEach(function (r) { var td = h('td'); cells[r] = td; tbl.appendChild(h('tr', null, h('th', { text: T('row.' + r) }), td)); });
    top.appendChild(h('div', null, h('h3', { class: 'caps sub', text: T('values') }), tbl));
    var clocks = null;
    if (kind === 'gesture') { clocks = h('div', { class: 'alab-clock', 'aria-live': 'polite' }); left.appendChild(clocks); }
    var gWrap = h('div', null, h('h3', { class: 'caps sub', text: T('graph') })); root.appendChild(gWrap);
    var NS = 'http://www.w3.org/2000/svg', svg = document.createElementNS(NS, 'svg'); svg.setAttribute('class', 'alab-g'); svg.setAttribute('viewBox', '0 0 600 200'); svg.setAttribute('role', 'img'); gWrap.appendChild(svg);
    // điều khiển chung
    var row = h('div', { class: 'row' }); root.appendChild(row);
    var bPlay = h('button', { type: 'button', class: 'btn primary', 'data-fk': 'lab-play' });
    var bStep = h('button', { type: 'button', class: 'btn', 'data-fk': 'lab-step', text: T('ctl.step') });
    var bRestart = h('button', { type: 'button', class: 'btn', 'data-fk': 'lab-restart', text: T('ctl.restart') });
    var bTarget = h('button', { type: 'button', class: 'btn', 'data-fk': 'lab-target', text: T(kind === 'retarget' ? 'ctl.retarget' : 'ctl.reverse') });
    var bReset = h('button', { type: 'button', class: 'btn', 'data-fk': 'lab-reset', text: T('ctl.reset') });
    var selFrame = select('lab-frame', 'ctl.frame', [8, 16, 33].map(function (v) { return [v, T('ctl.frameN', { n: v })]; }), function (v) { st.frameMs = +v; });
    [bPlay, bStep, bRestart].forEach(function (b) { row.appendChild(b); });
    if (kind !== 'gesture') row.appendChild(bTarget);
    row.appendChild(bReset); row.appendChild(selFrame.wrap);
    // điều khiển spec
    var specRow = h('div', { class: 'row' }); root.appendChild(specRow);
    var sp = {};
    function select(fk, labelK, opts, on) {
      var id = 'alab-' + fk, sel = h('select', { id: id, class: 'sel', 'data-fk': fk });
      opts.forEach(function (o) { sel.appendChild(h('option', { value: String(o[0]), text: o[1] })); });
      sel.addEventListener('change', function () { on(sel.value); applySpec(); });
      var wrap = h('label', { class: 'field', for: id }, h('span', { text: T(labelK) }), sel);
      return { wrap: wrap, sel: sel };
    }
    function applySpec() { if (kind === 'gesture') { render(); return; } L.restart(st); render(); }
    var types = kind === 'retarget' ? ['spring', 'tween'] : ['spring', 'tween', 'keyframes', 'repeat', 'infinite', 'snap', 'decay'];
    if (kind !== 'gesture') sp.type = select('lab-type', 'spec.type', types.map(function (v) { return [v, T('spec.type.' + v)]; }), function (v) { st.spec.type = v; });
    sp.damping = select('lab-damping', 'spec.damping', Object.keys(Ph.DAMPING).map(function (k) { return [k, T('spec.damping.n', { name: k, v: Ph.DAMPING[k] })]; }), function (v) { st.spec.damping = v; });
    sp.stiffness = select('lab-stiffness', 'spec.stiffness', Object.keys(Ph.STIFFNESS).map(function (k) { return [k, T('spec.stiffness.n', { name: k, v: Ph.STIFFNESS[k] })]; }), function (v) { st.spec.stiffness = v; });
    if (kind !== 'gesture') {
      sp.duration = select('lab-duration', 'spec.duration', [150, 300, 600].map(function (v) { return [v, T(v === 300 ? 'spec.durationDefault' : 'spec.durationN', { n: v })]; }), function (v) { st.spec.duration = +v; });
      sp.easing = select('lab-easing', 'spec.easing', Object.keys(Ph.EASING).map(function (k) { return [k, k + 'Easing']; }), function (v) { st.spec.easing = v; });
      sp.mode = select('lab-mode', 'spec.mode', ['Restart', 'Reverse'].map(function (v) { return [v, 'RepeatMode.' + v]; }), function (v) { st.spec.mode = v; });
      sp.iterations = select('lab-iter', 'spec.iterations', [2, 3].map(function (v) { return [v, String(v)]; }), function (v) { st.spec.iterations = +v; });
      sp.delay = select('lab-delay', 'spec.delay', [0, 150, 300].map(function (v) { return [v, T('ctl.frameN', { n: v })]; }), function (v) { st.spec.delay = +v; });
      sp.multiplier = select('lab-mult', 'spec.multiplier', [0.5, 1, 2].map(function (v) { return [v, String(v)]; }), function (v) { st.spec.multiplier = +v; });
      sp.v0 = select('lab-v0', 'spec.v0', [300, 600, 1200].map(function (v) { return [v, T('spec.v0N', { n: v })]; }), function (v) { st.spec.v0 = +v; });
    }
    Object.keys(sp).forEach(function (k) { specRow.appendChild(sp[k].wrap); });
    // retarget: slider
    var slider = null;
    if (kind === 'retarget') {
      slider = h('input', { type: 'range', min: '0', max: '100', step: '5', id: 'alab-slider', 'data-fk': 'lab-slider', class: 'sel' });
      slider.addEventListener('input', function () { st.slider = +slider.value; render(); });
      specRow.appendChild(h('label', { class: 'field', for: 'alab-slider' }, h('span', { text: T('ctl.slider') }), slider));
    }
    // gesture: nút thay cho kéo bằng chuột/cảm ứng
    var gRow = null, selV = null;
    if (kind === 'gesture') {
      gRow = h('div', { class: 'row' }); root.appendChild(gRow);
      var bDrag = h('button', { type: 'button', class: 'btn', 'data-fk': 'lab-drag', text: T('ctl.drag') });
      var bTouch = h('button', { type: 'button', class: 'btn', 'data-fk': 'lab-touch', text: T('ctl.touch') });
      var bRel = h('button', { type: 'button', class: 'btn', 'data-fk': 'lab-release', text: T('ctl.release') });
      selV = select('lab-fling', 'ctl.flingV', [-1200, -400, 0, 400, 1200].map(function (v) { return [v, T('spec.v0N', { n: v })]; }), function () { });
      selV.sel.value = '400';
      bDrag.addEventListener('click', function () { ADE.ui.withFocus(function () { L.drag(st, 30); render(); }); });
      bTouch.addEventListener('click', function () { ADE.ui.withFocus(function () { L.touch(st); render(); }); });
      bRel.addEventListener('click', function () { ADE.ui.withFocus(function () { L.release(st, +selV.sel.value); go(); }); });
      [bTouch, bDrag, bRel, selV.wrap].forEach(function (b) { gRow.appendChild(b); });
      gRow.appendChild(h('p', { class: 'hint', text: T('hint.gesture') }));
      // kéo bằng con trỏ
      var dragging = false, lastX = 0, samples = [];
      puck.addEventListener('pointerdown', function (e) { dragging = true; lastX = e.clientX; samples = [{ x: 0, t: e.timeStamp }]; try { puck.setPointerCapture(e.pointerId); } catch (x) { } L.touch(st); render(); e.preventDefault(); });
      puck.addEventListener('pointermove', function (e) {
        if (!dragging) return; var w = prev.clientWidth - 48 || 1, dx = (e.clientX - lastX) / w * (L.BOUND * 2.8); lastX = e.clientX;
        st.pointer = Math.max(-L.BOUND * 1.4, Math.min(L.BOUND * 1.4, st.pointer + dx)); samples.push({ x: st.pointer, t: e.timeStamp }); if (samples.length > 6) samples.shift(); render();
      });
      var up = function (e) {
        if (!dragging) return; dragging = false;
        var a = samples[0], b = samples[samples.length - 1], v = b && a && b.t > a.t ? (b.x - a.x) / ((b.t - a.t) / 1000) : 0;   // VelocityTracker giản lược: độ dốc của vài mẫu cuối
        v = Math.max(-3000, Math.min(3000, v)); L.log(st, 'frame', 'ev.snap', { v: R1(st.pointer) }); L.release(st, v); go();
      };
      puck.addEventListener('pointerup', up); puck.addEventListener('pointercancel', up);
      onKey = function (e) { if (e.key === 'ArrowRight' || e.key === 'ArrowLeft') { L.drag(st, e.key === 'ArrowRight' ? 15 : -15); render(); e.preventDefault(); } else if (e.key === 'Enter' || e.key === ' ') { L.release(st, +selV.sel.value); go(); e.preventDefault(); } };
      puck.addEventListener('keydown', onKey);
    }
    // panel mã Kotlin tương ứng (lõi dựng khối mã); dòng được highlight theo spec đang chọn
    var codeBox = h('div', null, h('h3', { class: 'caps sub', text: T('code') })); root.appendChild(codeBox);
    var codeSlot = h('div'); codeBox.appendChild(codeSlot);
    var SPEC_LINE = { spring: 1, tween: 2, keyframes: 3, repeat: 4, infinite: 4, snap: 5, decay: 6 };
    var lastCode = '';
    function drawCode() {
      var sn = ADE.getCode('animation', kind), hl = kind === 'spec' ? [SPEC_LINE[st.spec.type]] : kind === 'retarget' ? [2] : st.pointer != null ? [4, 5] : st.seg ? [6, 7] : [1];
      var sig = kind + hl.join(',') + ADE.lang; if (sig === lastCode || !sn) return; lastCode = sig;
      codeSlot.innerHTML = ''; codeSlot.appendChild(ADE.ui.codeBlock(sn, hl));
    }
    // nhật ký + giản lược
    var logList = h('ol', { class: 'alab-log', 'aria-live': 'polite' });
    root.appendChild(h('div', null, h('h3', { class: 'caps sub', text: T('log') }), logList));
    var simp = h('details', { class: 'acc' }, h('summary', { text: T('simp.title') }));
    ['simp.1', 'simp.2', 'simp.3'].forEach(function (k) { simp.appendChild(h('p', { class: 'prose', html: ADE.markup(T(k)) })); });
    root.appendChild(simp);

    /* ---------- vòng chạy ---------- */
    function stop() { cancelAnimationFrame(raf); raf = 0; }
    function go() {
      if (!st.seg) { render(); return; }
      if (reduced()) { var g = 0; while (st.seg && !L.cur(st).done && g++ < 3000) L.step(st); if (st.seg) L.step(st); st.playing = false; render(); return; }   // giảm chuyển động: chuyển tức thời
      st.playing = true; last = 0; acc = 0; stop(); raf = requestAnimationFrame(tick); render();
    }
    function tick(now) {
      if (!st.playing) { stop(); render(); return; }
      if (last) acc += Math.min(100, now - last); last = now;
      while (acc >= st.frameMs && st.playing) { acc -= st.frameMs; L.step(st); }
      render(); if (st.playing) raf = requestAnimationFrame(tick);
    }
    bPlay.addEventListener('click', function () { ADE.ui.withFocus(function () { if (st.playing) { st.playing = false; stop(); render(); } else { if (st.seg && L.cur(st).done) L.restart(st); go(); } }); });
    bStep.addEventListener('click', function () { ADE.ui.withFocus(function () { st.playing = false; stop(); L.step(st); render(); }); });
    bRestart.addEventListener('click', function () { ADE.ui.withFocus(function () { stop(); L.restart(st); render(); }); });
    bTarget.addEventListener('click', function () { ADE.ui.withFocus(function () { var to = kind === 'retarget' ? st.slider : (st.target === 100 ? 0 : 100); L.retarget(st, to); if (st.playing || kind === 'retarget') go(); else render(); }); });
    bReset.addEventListener('click', function () { ADE.ui.withFocus(function () { stop(); st = L.store[key] = fresh(kind); syncInputs(); render(); }); });

    function syncInputs() {
      if (sp.type) sp.type.sel.value = st.spec.type;
      ['damping', 'stiffness', 'duration', 'easing', 'mode', 'iterations', 'delay', 'multiplier', 'v0'].forEach(function (k) { var m = { iterations: 'iterations' }; if (sp[k]) sp[k].sel.value = String(st.spec[m[k] || k]); });
      selFrame.sel.value = String(st.frameMs); if (slider) slider.value = String(st.slider);
    }
    var X = function (v) { var lo = kind === 'gesture' ? -L.BOUND * 1.4 : -20, hi = kind === 'gesture' ? L.BOUND * 1.4 : 160; return 24 + (Math.max(lo, Math.min(hi, v)) - lo) / (hi - lo) * Math.max(1, prev.clientWidth - 48); };
    function render() {
      var c = L.cur(st), t = st.spec.type, vel = st.seg ? P_has(st.seg.spec) : true;
      // hiện/ẩn điều khiển spec theo loại
      var show = { damping: t === 'spring' || kind === 'gesture', stiffness: t === 'spring' || kind === 'gesture', duration: /tween|keyframes|repeat|infinite/.test(t), easing: /tween|repeat|infinite/.test(t), mode: /repeat|infinite/.test(t), iterations: t === 'repeat', delay: t === 'snap', multiplier: t === 'decay', v0: t === 'decay' };
      Object.keys(sp).forEach(function (k) { if (k !== 'type') sp[k].wrap.hidden = !show[k]; });
      bPlay.textContent = st.playing ? T('ctl.pause') : T('ctl.play');
      bTarget.disabled = !st.seg && kind !== 'retarget';
      var val = st.pointer != null ? st.pointer : c.value;
      cells.time.textContent = T('unit.ms', { n: N(st.T, 0) });
      cells.current.textContent = N(val);
      cells.target.textContent = st.seg ? N(st.seg.to) : (st.dismissed ? T('val.dismissed') : '—');
      cells.velocity.textContent = st.pointer != null ? T('val.dragging') : (vel ? T('unit.perS', { n: N(c.velocity || 0, 0) }) : T('val.noVelocity'));
      cells.frame.textContent = T('ctl.frameN', { n: st.frameMs });
      if (cells.pointer) cells.pointer.textContent = st.pointer != null ? N(st.pointer) : '—';
      if (clocks) { clocks.innerHTML = ''; clocks.appendChild(h('div', null, h('span', { text: T('clock.pointer') }), h('strong', { text: st.pointer != null ? N(st.pointer) : '—' }))); clocks.appendChild(h('div', null, h('span', { text: T('clock.anim') }), h('strong', { text: st.pointer != null ? T('val.paused') : N(c.value) }))); }
      puck.style.left = X(val) + 'px'; tgt.style.left = X(st.seg ? st.seg.to : st.target) + 'px';
      if (kind === 'gesture') puck.setAttribute('aria-valuenow', String(Math.round(val)));
      drawGraph(c); drawCode();
      logList.innerHTML = '';
      st.log.slice(-8).forEach(function (e) { logList.appendChild(h('li', null, h('span', { text: T('unit.ms', { n: N(e.T, 0) }) }), h('b', { text: ADE.kindLabel('animation', e.kind) }), h('span', { text: T(e.key, e.params) }))); });
      if (!st.log.length) logList.appendChild(h('li', null, h('span', { text: T('log.empty') })));
    }
    function P_has(spec) { return Ph.hasVelocity(spec); }
    function drawGraph(c) {
      var pts = st.hist.slice(), pred = [];
      if (st.seg && !c.done) { for (var k = 0, tt = st.t; k < 200; k++, tt += 16) { var s = Ph.sample(st.seg, tt); pred.push({ T: st.T + (tt - st.t), v: s.value }); if (s.done) break; } }
      var all = pts.concat(pred), T0 = all.length ? all[0].T : 0, T1 = Math.max(T0 + 200, all.length ? all[all.length - 1].T : 1);
      var lo = Infinity, hi = -Infinity; all.concat([{ v: st.target }, { v: st.start }]).forEach(function (p) { lo = Math.min(lo, p.v); hi = Math.max(hi, p.v); }); if (hi - lo < 1) { hi += 1; lo -= 1; }
      var pad = (hi - lo) * 0.1; lo -= pad; hi += pad;
      var W = Math.max(300, Math.round(svg.getBoundingClientRect().width) || 600); svg.setAttribute('viewBox', '0 0 ' + W + ' 200');
      var x = function (t) { return 40 + (t - T0) / (T1 - T0) * (W - 52); }, y = function (v) { return 186 - (v - lo) / (hi - lo) * 172; };
      var line = function (arr) { return arr.map(function (p, i) { return (i ? 'L' : 'M') + x(p.T).toFixed(1) + ' ' + y(p.v).toFixed(1); }).join(''); };
      var tg = st.seg ? st.seg.to : st.target;
      svg.innerHTML = '<title>' + ADE.esc(T('graph')) + '</title><desc>' + ADE.esc(T('graphDesc')) + '</desc>' +
        '<line class="ax" x1="40" y1="186" x2="' + (W - 10) + '" y2="186"/><line class="ax" x1="40" y1="10" x2="40" y2="186"/>' +
        '<line class="tg" x1="40" x2="' + (W - 10) + '" y1="' + y(tg).toFixed(1) + '" y2="' + y(tg).toFixed(1) + '"/>' +
        '<text x="44" y="' + (y(tg) - 4).toFixed(1) + '">' + ADE.esc(T('row.target')) + '</text>' +
        '<text x="4" y="14">' + ADE.esc(N(hi, 0)) + '</text><text x="4" y="186">' + ADE.esc(N(lo, 0)) + '</text>' +
        '<text x="' + (W - 70) + '" y="198">' + ADE.esc(T('unit.ms', { n: N(T1, 0) })) + '</text>' +
        (pred.length ? '<path class="pred" d="' + line([pts[pts.length - 1]].concat(pred)) + '"/>' : '') +
        '<path class="hist" d="' + line(pts) + '"/>' +
        '<line class="now" x1="' + x(st.T).toFixed(1) + '" x2="' + x(st.T).toFixed(1) + '" y1="10" y2="186"/>';
    }
    syncInputs(); render();
    return { destroy: function () { stop(); st.playing = false; if (root.parentNode) root.parentNode.removeChild(root); } };
  };
})();
