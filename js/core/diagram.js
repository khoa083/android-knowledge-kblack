/* diagram.js — bộ icon tự vẽ, helper isometric, sơ đồ (scene, nhiều dạng bố cục), timeline, logo.
   Mọi hình ở đây TỰ VẼ từ đầu (chủ thể: Android). Không trace, không chép SVG của trang mẫu.
   Nét mực đơn sắc (currentColor / var(--ink)); màu token chỉ ở icon/viền, không là cách phân biệt duy nhất. */
(function () {
  'use strict';
  var ADE = window.ADE = window.ADE || {};
  var NS = 'http://www.w3.org/2000/svg';

  /* ---------- icon 24×24, nét tròn đầu ---------- */
  var C = function (cx, cy, r, extra) { return '<circle cx="' + cx + '" cy="' + cy + '" r="' + r + '"' + (extra || '') + '/>'; };
  var P = function (d, extra) { return '<path d="' + d + '"' + (extra || '') + '/>'; };
  var R = function (x, y, w, h, rx, extra) { return '<rect x="' + x + '" y="' + y + '" width="' + w + '" height="' + h + '"' + (rx ? ' rx="' + rx + '"' : '') + (extra || '') + '/>'; };
  var FILL = ' fill="currentColor"';
  var ICONS = {
    add: P('M12 5v14M5 12h14'),
    set: P('M5 12h14M13 6l6 6-6 6'),
    remove: P('M6 6l12 12M18 6L6 18'),
    cross: P('M6 6l12 12M18 6L6 18'),
    skip: P('M5 6l9 6-9 6z', FILL) + P('M18 6v12'),
    check: P('M5 12.5l4.5 4.5L19 7'),
    play: P('M7 5l12 7-12 7z', FILL),
    pause: P('M8 5v14M16 5v14'),
    resume: P('M4 5l7 7-7 7M12 5l7 7-7 7'),
    next: P('M9 5l7 7-7 7'),
    prev: P('M15 5l-7 7 7 7'),
    reset: P('M4 12a8 8 0 1 0 3-6.2M4 4v5h5'),
    replay: P('M20 12a8 8 0 1 1-3-6.2M20 4v5h-5'),
    refresh: P('M20 12a8 8 0 1 1-3-6.2M20 4v5h-5'),
    forbidden: C(12, 12, 8) + P('M6.5 6.5l11 11'),
    bolt: P('M13 3L5 14h6l-1 7 8-11h-6z'),
    clock: C(12, 12, 8) + P('M12 7v5l3 2'),
    square: R(6, 6, 12, 12, 1, FILL),
    triangle: P('M12 5l8 14H4z'),
    diamond: P('M12 4l8 8-8 8-8-8z', FILL),
    diamondo: P('M12 4l8 8-8 8-8-8z'),
    dot: C(12, 12, 5, FILL),
    grid: R(4, 4, 16, 16, 1) + P('M12 4v16M4 12h16'),
    halfcircle: C(12, 12, 8) + P('M12 4a8 8 0 0 1 0 16z', FILL),
    target: C(12, 12, 8) + C(12, 12, 3),
    frame: R(4, 6, 16, 12, 1) + P('M8 6v12M16 6v12'),
    eye: P('M2 12s4-7 10-7 10 7 10 7-4 7-10 7S2 12 2 12z') + C(12, 12, 3),
    spark: P('M12 3v6M12 15v6M3 12h6M15 12h6'),
    source: P('M16 8l-7 7a2.5 2.5 0 0 0 3.5 3.5l8-8a4.5 4.5 0 0 0-6.4-6.4L6 12.5'),
    mechanism: C(12, 12, 4) + P('M12 3v3M12 18v3M3 12h3M18 12h3M5.6 5.6l2.1 2.1M16.3 16.3l2.1 2.1M18.4 5.6l-2.1 2.1M7.7 16.3l-2.1 2.1'),
    pitfall: P('M12 4l9 16H3z') + P('M12 10v4M12 17v.4'),
    android: P('M5 16a7 7 0 0 1 14 0z') + P('M8 8l-2-3M16 8l2-3') + C(9.5, 13, 0.9, FILL) + C(14.5, 13, 0.9, FILL),
    try: C(12, 12, 9) + P('M10 8.5l5 3.5-5 3.5z', FILL),
    menu: P('M4 7h16M4 12h16M4 17h16'),
    search: C(11, 11, 6) + P('M16 16l4 4'),
    sun: C(12, 12, 4) + P('M12 2v3M12 19v3M2 12h3M19 12h3M4.9 4.9l2.1 2.1M17 17l2.1 2.1M19.1 4.9L17 7M7 17l-2.1 2.1'),
    moon: P('M20 14.5A8 8 0 1 1 9.5 4a6.5 6.5 0 0 0 10.5 10.5z'),
    motion: P('M3 12c3-6 6 6 9 0s6 6 9 0'),
    keyboard: R(3, 6, 18, 12, 2) + P('M7 10h.01M11 10h.01M15 10h.01M7 14h10'),
    info: C(12, 12, 9) + P('M12 11v5M12 8v.4'),
    chevd: P('M6 9l6 6 6-6'),
    chevr: P('M9 6l6 6-6 6'),
    close: P('M6 6l12 12M18 6L6 18'),
    rail: R(3, 4, 18, 16, 1.5) + P('M9 4v16'),
    lang: C(12, 12, 9) + P('M3 12h18M12 3c3 3 3 15 0 18M12 3c-3 3-3 15 0 18'),
    sans: P('M5 18l5-12 5 12M7 14h6M17 8h3M17 12h3'),
    list: P('M9 7h11M9 12h11M9 17h11M4.5 7h.01M4.5 12h.01M4.5 17h.01'),
    /* biểu tượng khối cho node sơ đồ */
    phone: R(7, 2.5, 10, 19, 2.2) + P('M10.5 5h3M10.5 19h3'),
    chip: R(7, 7, 10, 10, 1.5) + P('M10 7V4M14 7V4M10 20v-3M14 20v-3M7 10H4M7 14H4M20 10h-3M20 14h-3') + R(10, 10, 4, 4, 0.5),
    layers: P('M12 4l8 4-8 4-8-4z') + P('M4 12l8 4 8-4M4 16l8 4 8-4'),
    queue: R(2.5, 8, 5, 8, 1) + R(9.5, 8, 5, 8, 1) + R(16.5, 8, 5, 8, 1) + P('M5 5.5h14M16.5 3.5l2.5 2-2.5 2'),
    screen: R(3, 4, 18, 14, 1.5) + P('M3 8h18M9 21h6M12 18v3'),
    job: C(12, 6, 2.6) + C(6, 18, 2.6) + C(18, 18, 2.6) + P('M10.8 8.2L7.2 15.6M13.2 8.2l3.6 7.4'),
    store: '<ellipse cx="12" cy="6" rx="7" ry="2.8"/>' + P('M5 6v12c0 1.6 3.1 2.8 7 2.8s7-1.2 7-2.8V6') + P('M5 12c0 1.6 3.1 2.8 7 2.8s7-1.2 7-2.8'),
    thread: P('M3 7h18M3 12h18M3 17h18M8 5v4M14 10v4M10 15v4')
  };
  function icon(name, o) {
    o = o || {};
    var s = o.size || 16;
    var body = ICONS[name];
    if (!body) { body = ICONS.info; }
    return '<svg class="ic ic-' + name + (o.cls ? ' ' + o.cls : '') + '" viewBox="0 0 24 24" width="' + s + '" height="' + s +
      '" fill="none" stroke="currentColor" stroke-width="' + (o.sw || 1.7) + '" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">' + body + '</svg>';
  }

  /* ---------- logo: điện thoại isometric, mũi tên đi xuống xuyên các lớp ---------- */
  function logo(size) {
    var s = size || 34;
    return '<svg class="logo" viewBox="0 0 32 32" width="' + s + '" height="' + s + '" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round" stroke-linecap="round" aria-hidden="true" focusable="false">' +
      '<path d="M16 2.5l11 5.5-11 5.5L5 8z" class="logo-fill"/>' +
      '<path d="M16 6.2l5.2 2.6-5.2 2.6-5.2-2.6z" opacity=".75"/>' +
      '<path d="M5 13.5l11 5.5 11-5.5" opacity=".8"/>' +
      '<path d="M5 19l11 5.5L27 19" opacity=".6"/>' +
      '<path d="M16 8.2v21M12.2 25.8L16 29.6l3.8-3.8" stroke-width="1.9"/>' +
      '</svg>';
  }

  /* ---------- isometric ---------- */
  var U = 36;
  function iso(x, y, z) { return [(x - y) * 0.866 * U, (x + y) * 0.5 * U - (z || 0) * U]; }
  function pts(arr) { return arr.map(function (p) { return p[0].toFixed(1) + ',' + p[1].toFixed(1); }).join(' '); }
  function box(x, y, w, d, h, cls) {
    var t = [iso(x, y, h), iso(x + w, y, h), iso(x + w, y + d, h), iso(x, y + d, h)];
    var l = [iso(x, y + d, h), iso(x + w, y + d, h), iso(x + w, y + d, 0), iso(x, y + d, 0)];
    var r = [iso(x + w, y, h), iso(x + w, y + d, h), iso(x + w, y + d, 0), iso(x + w, y, 0)];
    return '<g class="' + (cls || 'iso-box') + '"><polygon class="iso-left" points="' + pts(l) + '"/><polygon class="iso-right" points="' + pts(r) + '"/><polygon class="iso-top" points="' + pts(t) + '"/></g>';
  }
  function easeInOut(t) { return t < 0.5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2; }

  /* ---------- họ trạng thái: mỗi trạng thái node có HÌNH + NHÃN riêng (không chỉ màu) ---------- */
  // Khoá trạng thái (message key) → họ, theo đoạn cuối của khoá. View có thể ghi đè bằng `stateFamilies: {đoạn: họ}`.
  var FAM_WORDS = {
    run: 'running active busy composing applying animating recording entering exiting collecting rerun emitting started resumed',
    wait: 'suspended suspending waiting ready held paused stopped hidden queued pending',
    block: 'blocking blocked',
    cancel: 'cancelled cancelledS cancelling',
    fail: 'failed uncaught broken error crashed',
    done: 'done completed settled finished ok kept caught handled ran built filled delivered',
    idle: 'idle idleS free unused none skipped skippedNode'
  };
  var FAM = {};
  Object.keys(FAM_WORDS).forEach(function (f) { FAM_WORDS[f].split(' ').forEach(function (w) { FAM[w] = f; }); });
  var FAM_ORDER = ['run', 'wait', 'block', 'cancel', 'fail', 'done', 'idle'];
  function famOf(key, view) {
    if (!key) return null;
    var seg = String(key).split('.').pop();
    if (view && view.stateFamilies && view.stateFamilies[seg]) return view.stateFamilies[seg];
    return FAM[seg] || 'info';
  }
  // glyph 12×12 tại (x,y): hình khác nhau cho từng họ
  function glyph(fam, x, y) {
    var b;
    switch (fam) {
      case 'run': b = '<path d="M2 1l9 5-9 5z" class="g-fill"/>'; break;
      case 'wait': b = '<path d="M3.5 1.5v9M8.5 1.5v9"/>'; break;
      case 'block': b = '<rect x="1.5" y="1.5" width="9" height="9" class="g-fill"/>'; break;
      case 'cancel': b = '<circle cx="6" cy="6" r="4.8"/><path d="M2.6 2.6l6.8 6.8"/>'; break;
      case 'fail': b = '<path d="M7 0.5L2.5 7h3.5l-1 4.5L10 5H6.5z" class="g-fill"/>'; break;
      case 'done': b = '<path d="M1.5 6.5l3 3 6-7"/>'; break;
      case 'idle': b = '<circle cx="6" cy="6" r="4.2"/>'; break;
      default: b = '<path d="M6 1.5l4.5 4.5L6 10.5 1.5 6z"/>';
    }
    return '<g class="sg sg-' + fam + '" transform="translate(' + x.toFixed(1) + ',' + y.toFixed(1) + ')">' + b + '</g>';
  }
  function glyphSvg(fam) { return '<svg class="sg-svg" viewBox="-1 -1 14 14" width="14" height="14" aria-hidden="true" focusable="false">' + glyph(fam, 0, 0) + '</svg>'; }
  function barSvg(kind) { return '<svg class="bar-svg" viewBox="0 0 26 14" width="26" height="14" aria-hidden="true" focusable="false"><defs>' + hatchDef('lg-h-' + kind) + '</defs><rect x="1" y="2" width="24" height="10" rx="2" class="bar bar-' + kind + '"' + (kind === 'block' ? ' style="fill:url(#lg-h-' + kind + ')"' : '') + '/></svg>'; }
  function hatchDef(id) { return '<pattern id="' + id + '" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><rect width="6" height="6" class="hatch-bg"/><path d="M0 0v6" class="hatch-ln"/></pattern>'; }

  /* ---------- tiện ích hình học ---------- */
  var sid = 0;
  function wrap(text, max) {
    var words = [], lines = [''], i;
    String(text).split(' ').forEach(function (w) { while (w.length > max) { words.push(w.slice(0, max - 1) + '-'); w = w.slice(max - 1); } words.push(w); });
    for (i = 0; i < words.length; i++) {
      var cur = lines[lines.length - 1], next = cur ? cur + ' ' + words[i] : words[i];
      if (next.length > max && cur) lines.push(words[i]); else lines[lines.length - 1] = next;
    }
    if (lines.length > 2) { lines = lines.slice(0, 2); lines[1] = lines[1].slice(0, max - 1) + '…'; }
    return lines.map(function (l) { return l.length > max ? l.slice(0, max - 1) + '…' : l; });
  }
  function polyLen(p) { var L = 0; for (var i = 1; i < p.length; i++) L += Math.hypot(p[i][0] - p[i - 1][0], p[i][1] - p[i - 1][1]); return L; }
  function polyAt(p, k) {
    var total = polyLen(p) * k;
    for (var i = 1; i < p.length; i++) {
      var seg = Math.hypot(p[i][0] - p[i - 1][0], p[i][1] - p[i - 1][1]);
      if (total <= seg || i === p.length - 1) { var r = seg ? Math.min(1, total / seg) : 1; return [p[i - 1][0] + (p[i][0] - p[i - 1][0]) * r, p[i - 1][1] + (p[i][1] - p[i - 1][1]) * r]; }
      total -= seg;
    }
    return p[p.length - 1];
  }
  function pathD(p) { return p.map(function (q, i) { return (i ? 'L' : 'M') + q[0].toFixed(1) + ' ' + q[1].toFixed(1); }).join(''); }
  function inBox(q, b, pad) { return q[0] > b.x0 - pad && q[0] < b.x1 + pad && q[1] > b.y0 - pad && q[1] < b.y1 + pad; }

  /* ---------- scene ---------- */
  // view: {titleKey, descKey, captionKey?, layout?:'iso'|'tree'|'pipeline'|'cycle'|'lanes', nodes, edges, ...}
  function Scene(container, view) {
    this.view = view; this.container = container; this.uid = 's' + (++sid);
    this.layout = view.layout || 'iso';
    this.svg = document.createElementNS(NS, 'svg');
    this.svg.setAttribute('class', 'scene layout-' + this.layout);
    this.svg.setAttribute('role', 'img');
    this.svg.setAttribute('preserveAspectRatio', 'xMidYMid meet');
    container.appendChild(this.svg);
    this.nodeBox = {}; this.edgeGeo = {};
    if (this.layout !== 'lanes') this._layout();
    else this.full = [0, 0, 760, 200];
    this.vb = this.full.slice();
    this.svg.setAttribute('viewBox', this.vb.join(' '));
    this._fit();
    this._raf = 0; this._tokRaf = []; this._typeTimer = 0;
  }
  // sơ đồ ít thành phần không phóng to quá cỡ thật (1 đơn vị viewBox ≈ 1.15 px)
  Scene.prototype._fit = function () { if (this.layout !== 'iso') this.svg.style.maxWidth = Math.round(this.full[2] * 1.15) + 'px'; };
  Scene.prototype.byId = function (id) { return this.view.nodes.filter(function (n) { return n.id === id; })[0]; };
  Scene.prototype._layout = function () {
    if (this.layout === 'iso') return this._layoutIso();
    this._layoutFlat();
  };
  Scene.prototype._layoutIso = function () {
    var v = this.view, minX = 1e9, minY = 1e9, maxX = -1e9, maxY = -1e9;
    v.nodes.forEach(function (n) {
      n.w = n.w || 1.6; n.d = n.d || 1.6; n.h = n.h == null ? 0.35 : n.h;
      var c = [iso(n.x, n.y, n.h), iso(n.x + n.w, n.y, n.h), iso(n.x + n.w, n.y + n.d, 0), iso(n.x, n.y + n.d, 0), iso(n.x, n.y, 0)];
      var ctop = iso(n.x + n.w / 2, n.y + n.d / 2, n.h), lb = iso(n.x + n.w, n.y + n.d, 0);
      c.forEach(function (p) { minX = Math.min(minX, p[0]); maxX = Math.max(maxX, p[0]); minY = Math.min(minY, p[1]); maxY = Math.max(maxY, p[1]); });
      minY = Math.min(minY, ctop[1] - 62); maxY = Math.max(maxY, lb[1] + 54);
      minX = Math.min(minX, ctop[0] - 90); maxX = Math.max(maxX, ctop[0] + 90);
      // hộp bao gồm cả icon phía trên và hai dòng chữ phía dưới (tránh cắt nhãn khi zoom)
      this.nodeBox[n.id] = { cx: ctop[0], cy: ctop[1], base: iso(n.x + n.w / 2, n.y + n.d / 2, 0), x0: ctop[0] - 92, x1: ctop[0] + 92, y0: ctop[1] - 70, y1: lb[1] + 46 };
    }, this);
    var pad = 22;
    this.full = [minX - pad, minY - pad - 40, (maxX - minX) + pad * 2, (maxY - minY) + pad * 2 + 40];
  };
  /* bố cục phẳng: tree (trên → dưới), pipeline (trái → phải), cycle (vòng) */
  var CW = 176, CH = 62, DEPTH = 6;
  Scene.prototype._layoutFlat = function () {
    var v = this.view, self = this, L = this.layout, nodes = v.nodes, pos = {};
    var ids = nodes.map(function (n) { return n.id; });
    if (L === 'tree') {
      var hasParent = nodes.some(function (n) { return n.parent !== undefined; });
      var par = {};
      nodes.forEach(function (n) { par[n.id] = hasParent ? (n.parent || null) : null; });
      if (!hasParent) v.edges.forEach(function (e) { if (par[e.to] == null && e.from !== e.to && ids.indexOf(e.from) >= 0) par[e.to] = e.from; });
      var kids = {}; ids.forEach(function (id) { kids[id] = []; });
      ids.forEach(function (id) { if (par[id] && kids[par[id]]) kids[par[id]].push(id); });
      var width = function (id) { return kids[id].length ? kids[id].reduce(function (s, k) { return s + width(k); }, 0) : 1; };
      var place = function (id, left, depth) {
        var w = width(id), x = left;
        kids[id].forEach(function (k) { place(k, x, depth + 1); x += width(k); });
        pos[id] = { x: (left + w / 2) * (CW + 34), y: depth * (CH + 70) };
      };
      var left = 0;
      ids.filter(function (id) { return !par[id]; }).forEach(function (r) { place(r, left, 0); left += width(r) + 0.25; });
    } else if (L === 'pipeline') {
      // hạng = đường dài nhất từ nguồn, bỏ qua cạnh quay lui (phát hiện bằng DFS theo thứ tự khai báo)
      var out = {}; ids.forEach(function (id) { out[id] = []; });
      var back = {}, state = {};
      var dfs = function (id) {
        state[id] = 1;
        v.edges.forEach(function (e) { if (e.from !== id || ids.indexOf(e.to) < 0) return; if (state[e.to] === 1) back[e.id] = 1; else if (!state[e.to]) dfs(e.to); });
        state[id] = 2;
      };
      ids.forEach(function (id) { if (!state[id]) dfs(id); });
      this.backEdges = back;
      var rank = {}; ids.forEach(function (id) { rank[id] = 0; });
      for (var it = 0; it < ids.length; it++) v.edges.forEach(function (e) { if (!back[e.id] && rank[e.to] !== undefined && rank[e.from] !== undefined) rank[e.to] = Math.max(rank[e.to], rank[e.from] + 1); });
      nodes.forEach(function (n) { if (n.col !== undefined) rank[n.id] = n.col; });
      var cols = {}; ids.forEach(function (id) { (cols[rank[id]] = cols[rank[id]] || []).push(id); });
      var maxRows = Math.max.apply(null, Object.keys(cols).map(function (k) { return cols[k].length; }));
      Object.keys(cols).forEach(function (k) {
        var list = cols[k], off = (maxRows - list.length) / 2;
        list.forEach(function (id, i) { var n = self.byId(id); pos[id] = { x: +k * (CW + 62), y: (n.row !== undefined ? n.row : off + i) * (CH + 46) }; });
      });
    } else {  // cycle
      var N = nodes.length, rx = Math.max(200, N * 52), ry = Math.max(120, rx * 0.5);
      nodes.forEach(function (n, i) { var a = -Math.PI / 2 + i * 2 * Math.PI / N; pos[n.id] = { x: rx + rx * Math.cos(a), y: ry + ry * Math.sin(a) }; });
      this.ring = { cx: rx, cy: ry };
    }
    var minX = 1e9, minY = 1e9, maxX = -1e9, maxY = -1e9;
    nodes.forEach(function (n) {
      var p = pos[n.id], x0 = p.x - CW / 2, y0 = p.y;
      var b = { x0: x0, y0: y0, x1: x0 + CW, y1: y0 + CH, cx: p.x, cy: y0 + CH / 2 };
      b.base = [b.cx, b.y1];
      self.nodeBox[n.id] = b;
      minX = Math.min(minX, b.x0); minY = Math.min(minY, b.y0); maxX = Math.max(maxX, b.x1 + DEPTH); maxY = Math.max(maxY, b.y1 + DEPTH);
    });
    // hình học cạnh (polyline) — dùng cho nét vẽ, nhãn và token
    v.edges.forEach(function (e) {
      var a = self.nodeBox[e.from], b = self.nodeBox[e.to]; if (!a || !b) return;
      var p;
      if (L === 'tree') {
        if (b.cy > a.cy + 4) { var my = (a.y1 + b.y0) / 2; p = [[a.cx, a.y1], [a.cx, my], [b.cx, my], [b.cx, b.y0]]; }
        else if (b.cy < a.cy - 4) { var my2 = (b.y1 + a.y0) / 2; p = [[a.cx, a.y0], [a.cx, my2], [b.cx, my2], [b.cx, b.y1]]; }
        else p = b.cx > a.cx ? [[a.x1, a.cy], [b.x0, b.cy]] : [[a.x0, a.cy], [b.x1, b.cy]];
      } else if (L === 'pipeline') {
        if (!self.backEdges[e.id] && b.x0 > a.x1) { var mx = (a.x1 + b.x0) / 2; p = [[a.x1, a.cy], [mx, a.cy], [mx, b.cy], [b.x0, b.cy]]; }
        else if (!self.backEdges[e.id] && Math.abs(b.cx - a.cx) < 5) p = b.cy > a.cy ? [[a.cx, a.y1 + DEPTH], [b.cx, b.y0]] : [[a.cx, a.y0], [b.cx, b.y1 + DEPTH]];
        else if (!self.backEdges[e.id] && b.x1 < a.x0) { var mx2 = (a.x0 + b.x1 + DEPTH) / 2; p = [[a.x0, a.cy], [mx2, a.cy], [mx2, b.cy], [b.x1 + DEPTH, b.cy]]; }
        else { var low = maxY + 26; p = [[a.cx, a.y1 + DEPTH], [a.cx, low], [b.cx, low], [b.cx, b.y1 + DEPTH]]; maxY = Math.max(maxY, low + 8); }
      } else {
        // cung cong ra ngoài vòng, cắt hai đầu ở mép thẻ
        var R = self.ring, mxp = (a.cx + b.cx) / 2, myp = (a.cy + b.cy) / 2, dx = mxp - R.cx, dy = myp - R.cy, dl = Math.hypot(dx, dy) || 1;
        var ctl = [mxp + dx / dl * 46, myp + dy / dl * 46], raw = [];
        for (var k = 0; k <= 24; k++) { var t = k / 24, u = 1 - t; raw.push([u * u * a.cx + 2 * u * t * ctl[0] + t * t * b.cx, u * u * a.cy + 2 * u * t * ctl[1] + t * t * b.cy]); }
        p = raw.filter(function (q) { return !inBox(q, a, 4) && !inBox(q, b, 4); });
        if (p.length < 2) p = [[a.cx, a.cy], [b.cx, b.cy]];
      }
      self.edgeGeo[e.id] = p;
      p.forEach(function (q) { minX = Math.min(minX, q[0]); maxX = Math.max(maxX, q[0]); minY = Math.min(minY, q[1]); maxY = Math.max(maxY, q[1]); });
    });
    var pad = 26;
    this.full = [minX - pad, minY - pad - 64, (maxX - minX) + pad * 2, (maxY - minY) + pad * 2 + 64];   // chừa chỗ cho chú thích phía trên
  };
  Scene.prototype.setVB = function (vb) { this.vb = vb; this.svg.setAttribute('viewBox', vb.map(function (n) { return n.toFixed(1); }).join(' ')); };
  Scene.prototype._camera = function (target, instant) {
    var self = this;
    cancelAnimationFrame(this._raf);
    if (instant || ADE.motionReduced() || ADE.diagramOnly()) { this.setVB(target); return; }
    var from = this.vb.slice(), t0 = performance.now(), dur = 420;
    var tick = function (now) {
      var k = Math.min(1, (now - t0) / dur), e = easeInOut(k);
      self.setVB(from.map(function (f, i) { return f + (target[i] - f) * e; }));
      if (k < 1) self._raf = requestAnimationFrame(tick);
    };
    this._raf = requestAnimationFrame(tick);
  };
  // zoom vào thành phần đang xử lý (chỉ khi sơ đồ đủ lớn để zoom có ích)
  Scene.prototype._zoomTarget = function (ids) {
    if (ADE.motionReduced() || ADE.diagramOnly() || !ids || !ids.length) return this.full.slice();
    if (this.layout !== 'iso') return this._zoomFlat(ids);
    var self = this, x0 = 1e9, y0 = 1e9, x1 = -1e9, y1 = -1e9;
    ids.forEach(function (id) { var b = self.nodeBox[id]; if (!b) return; x0 = Math.min(x0, b.x0); x1 = Math.max(x1, b.x1); y0 = Math.min(y0, b.y0 - 60); y1 = Math.max(y1, b.y1 + 14); });
    if (x0 > x1) return this.full.slice();
    var F = this.full, ar = F[2] / F[3];
    var w = Math.max(x1 - x0 + 60, 420), h = Math.max(y1 - y0 + 40, 420 / ar);
    if (w / h < ar) w = h * ar; else h = w / ar;
    if (w > F[2] * 0.72) return this.full.slice();       // gần như toàn cảnh thì khỏi zoom
    var cx = (x0 + x1) / 2, cy = (y0 + y1) / 2;
    var x = Math.max(F[0], Math.min(F[0] + F[2] - w, cx - w / 2)), y = Math.max(F[1], Math.min(F[1] + F[3] - h, cy - h / 2));
    return [x, y, w, h];
  };
  // dạng phẳng: đẩy camera vào nhẹ, không cắt — hộp = thẻ đích + hàng xóm nối trực tiếp + chỗ chú thích phía trên
  Scene.prototype._zoomFlat = function (ids) {
    if (this.view.zoom === false) return this.full.slice();
    var self = this, F = this.full, set = {};
    ids.forEach(function (id) { set[id] = 1; });
    this.view.edges.forEach(function (e) { if (set[e.from] === 1) set[e.to] = set[e.to] || 2; if (set[e.to] === 1) set[e.from] = set[e.from] || 2; });
    var x0 = 1e9, y0 = 1e9, x1 = -1e9, y1 = -1e9;
    Object.keys(set).forEach(function (id) { var b = self.nodeBox[id]; if (!b) return; x0 = Math.min(x0, b.x0 - 12); x1 = Math.max(x1, b.x1 + DEPTH + 12); y0 = Math.min(y0, b.y0 - (set[id] === 1 ? 80 : 12)); y1 = Math.max(y1, b.y1 + DEPTH + 12); });
    if (x0 > x1) return F.slice();
    var ar = F[2] / F[3], w = Math.max(x1 - x0 + 80, F[2] * 0.68), h = Math.max(y1 - y0 + 80, F[3] * 0.68);
    if (w / h < ar) w = h * ar; else h = w / ar;
    if (w >= F[2] * 0.9 || h >= F[3] * 0.9) return F.slice();
    var cx = (x0 + x1) / 2, cy = (y0 + y1) / 2;
    return [Math.max(F[0], Math.min(F[0] + F[2] - w, cx - w / 2)), Math.max(F[1], Math.min(F[1] + F[3] - h, cy - h / 2)), w, h];
  };
  function edgeEnds(sc, e, trim) {
    var a = sc.nodeBox[e.from], b = sc.nodeBox[e.to];
    if (!a || !b) return null;
    var dx = b.base[0] - a.base[0], dy = b.base[1] - a.base[1], len = Math.sqrt(dx * dx + dy * dy) || 1;
    var ux = dx / len, uy = dy / len;
    return { x1: a.base[0] + ux * trim, y1: a.base[1] + uy * trim, x2: b.base[0] - ux * trim, y2: b.base[1] - uy * trim, ux: ux, uy: uy };
  }
  // node đổi trạng thái so với bước trước → đó là "điều vừa thay đổi" của bước này
  function changedNodes(step, prev) {
    if (!step || !step.nodeStates) return [];
    var a = step.nodeStates, b = (prev && prev.nodeStates) || {};
    return Object.keys(a).filter(function (id) { return a[id] !== b[id]; });
  }
  Scene.prototype._defs = function () {
    return '<defs><marker id="' + this.uid + '-arw" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M1 1.5L8.5 5 1 8.5z" class="arw-head"/></marker>' + hatchDef(this.uid + '-hatch') + '</defs>';
  };
  // chú thích trên hình: tiêu đề bước + (nếu có) "nhãn: trước → sau" của thành phần vừa đổi
  Scene.prototype._callout = function (step, prev, focusId, bounds) {
    if (!step) return '';
    var title = ADE.t(step.titleKey, step.params), lines = wrap(title, 42), sub = '';
    var ch = changedNodes(step, prev).filter(function (id) { return this.nodeBox[id]; }, this);
    var fid = ch[0] || focusId;
    if (ch.length) {
      var n = this.byId(ch[0]), before = prev && prev.nodeStates && prev.nodeStates[ch[0]];
      sub = (n ? ADE.t(n.labelKey) : ch[0]) + ': ' + (before ? ADE.t(before) : '—') + ' → ' + ADE.t(step.nodeStates[ch[0]]);
      if (sub.length > 46) sub = sub.slice(0, 45) + '…';
    }
    var b = fid && this.nodeBox[fid];
    var maxLen = Math.max.apply(null, lines.concat(sub ? [sub] : []).map(function (l) { return l.length; }));
    var w = Math.min(360, maxLen * 7.3 + 24), h = lines.length * 16 + (sub ? 18 : 0) + 12;
    var F = bounds || this.full, x, y, ax, ay;
    if (b) {
      x = b.cx - w / 2; y = b.y0 - h - 16; ax = b.cx; ay = b.y0 - 4;
      if (y < F[1] + 4) { y = b.y1 + 16; ay = b.y1 + 4; }
    } else { x = F[0] + 10; y = F[1] + 8; }
    x = Math.max(F[0] + 4, Math.min(F[0] + F[2] - w - 4, x)); y = Math.max(F[1] + 4, y);
    var o = '<g class="dg-callout">';
    if (b) o += '<path class="dg-callout-ptr" d="M' + Math.max(x + 10, Math.min(x + w - 10, ax)).toFixed(1) + ' ' + (ay < y ? y : y + h).toFixed(1) + 'L' + ax.toFixed(1) + ' ' + ay.toFixed(1) + '"/>';
    o += '<rect x="' + x.toFixed(1) + '" y="' + y.toFixed(1) + '" width="' + w.toFixed(1) + '" height="' + h + '" rx="3"/>';
    lines.forEach(function (l, i) { o += '<text class="dg-callout-t" x="' + (x + 12).toFixed(1) + '" y="' + (y + 19 + i * 16).toFixed(1) + '">' + ADE.esc(l) + '</text>'; });
    if (sub) o += '<text class="dg-callout-s" x="' + (x + 12).toFixed(1) + '" y="' + (y + 19 + lines.length * 16 + 2).toFixed(1) + '">' + ADE.esc(sub) + '</text>';
    return o + '</g>';
  };
  // step: bước hiện tại hoặc null (tổng quan/tổng kết). opts: {speed, instant, prev, events, pos}
  Scene.prototype.render = function (step, opts) {
    opts = opts || {};
    this._stop();
    if (this.layout === 'lanes') return this._renderLanes(step, opts);
    var self = this, v = this.view, active = (step && step.activeNodes) || [], sig = (step && step.movingSignals) || [];
    var changed = changedNodes(step, opts.prev);
    // Chuyển động bắt buộc cho MỌI sơ đồ (design-principles §5.1): nếu model không khai báo movingSignals,
    // lõi tự cho token chạy từ node đang xử lý ở bước trước sang node của bước này (dọc cạnh nối nếu có, ngược chiều nếu cạnh ngược, không có cạnh thì bay thẳng).
    var fly = null;
    if (!sig.length && step && opts.prev) {
      var pa = (opts.prev.activeNodes || []).filter(function (x) { return active.indexOf(x) < 0; });
      var tokOf = function (id) { var n = v.nodes.filter(function (x) { return x.id === id; })[0]; return n && n.tok; };
      var auto = [];
      v.edges.forEach(function (e) { if (pa.indexOf(e.from) >= 0 && active.indexOf(e.to) >= 0) auto.push({ edge: e.id, tok: tokOf(e.from), auto: true }); });
      if (!auto.length) v.edges.forEach(function (e) { if (pa.indexOf(e.to) >= 0 && active.indexOf(e.from) >= 0) auto.push({ edge: e.id, tok: tokOf(e.to), auto: true, reverse: true }); });
      if (auto.length) sig = auto;
      else if (pa.length && active.length) fly = { from: pa[0], to: active[0], tok: tokOf(pa[0]) };
    }
    var activeEdges = {};
    sig.forEach(function (s) { activeEdges[s.edge] = s; });
    var anyActive = active.length > 0;
    var html = this._defs();
    var flat = this.layout !== 'iso';
    // nền: lưới isometric mờ (giữ "giấy bản vẽ" ở mọi bố cục)
    var grid = '';
    if (!flat) {
      for (var gx = -14; gx <= 14; gx++) {
        var a = iso(gx, -14, 0), b = iso(gx, 14, 0), c = iso(-14, gx, 0), d = iso(14, gx, 0);
        grid += 'M' + a[0].toFixed(0) + ' ' + a[1].toFixed(0) + 'L' + b[0].toFixed(0) + ' ' + b[1].toFixed(0) + 'M' + c[0].toFixed(0) + ' ' + c[1].toFixed(0) + 'L' + d[0].toFixed(0) + ' ' + d[1].toFixed(0);
      }
    } else {
      var F = this.full, g0x = Math.floor(F[0] / 24) * 24, g0y = Math.floor(F[1] / 24) * 24;
      for (var gxx = g0x; gxx <= F[0] + F[2]; gxx += 24) grid += 'M' + gxx + ' ' + g0y + 'V' + (F[1] + F[3]).toFixed(0);
      for (var gyy = g0y; gyy <= F[1] + F[3]; gyy += 24) grid += 'M' + g0x + ' ' + gyy + 'H' + (F[0] + F[2]).toFixed(0);
    }
    html += '<path class="iso-grid" d="' + grid + '"/>';
    if (this.layout === 'cycle' && this.ring) html += '<ellipse class="ring-guide" cx="' + this.ring.cx + '" cy="' + (this.ring.cy + CH / 2) + '" rx="' + (this.ring.cx - 20) + '" ry="' + Math.max(40, this.ring.cy - 10) + '"/>';
    // cạnh
    var arw = 'url(#' + this.uid + '-arw)';
    v.edges.forEach(function (e) {
      var on = !!activeEdges[e.id], mid, near = !on && (active.indexOf(e.from) >= 0 || active.indexOf(e.to) >= 0);
      html += '<g class="edge' + (on ? ' active' : '') + (near ? ' near' : '') + (on && activeEdges[e.id].tok ? ' tok-' + activeEdges[e.id].tok : '') + '" data-edge="' + e.id + '"' + (on && activeEdges[e.id].tok ? ' style="--n:var(--tok-' + activeEdges[e.id].tok + ')"' : '') + '>';
      if (flat) {
        var p = self.edgeGeo[e.id]; if (!p) { html += '</g>'; return; }
        html += '<path class="edge-path" d="' + pathD(p) + '" marker-end="' + arw + '"/>';
        mid = polyAt(p, 0.5);
      } else {
        var en = edgeEnds(self, e, 44); if (!en) { html += '</g>'; return; }
        html += '<line x1="' + en.x1.toFixed(1) + '" y1="' + en.y1.toFixed(1) + '" x2="' + en.x2.toFixed(1) + '" y2="' + en.y2.toFixed(1) + '" marker-end="' + arw + '"/>';
        mid = [(en.x1 + en.x2) / 2, (en.y1 + en.y2) / 2];
      }
      if (e.labelKey) html += '<text class="edge-label" x="' + mid[0].toFixed(1) + '" y="' + (mid[1] - 7).toFixed(1) + '" text-anchor="middle">' + ADE.esc(ADE.t(e.labelKey)) + '</text>';
      html += '</g>';
    });
    // node
    var nodes = flat ? v.nodes.slice() : v.nodes.slice().sort(function (a, b) { return (a.x + a.y) - (b.x + b.y); });
    nodes.forEach(function (n) {
      var on = active.indexOf(n.id) >= 0, ch = changed.indexOf(n.id) >= 0, bx = self.nodeBox[n.id];
      var tok = n.tok ? 'var(--tok-' + n.tok + ')' : 'var(--ink)';
      var nsKey = step && step.nodeStates && step.nodeStates[n.id];          // trạng thái của node tại bước này (message key)
      var fam = famOf(nsKey, v);
      var nsCls = nsKey ? ' st-' + String(nsKey).split('.').pop().replace(/[^a-z0-9\-]/gi, '') + ' fam-' + fam : '';
      var cls = 'node' + (flat ? ' flat' : '') + (on ? ' active' : (anyActive ? ' dim' : '')) + (ch ? ' changed' : '') + nsCls;
      var act = v.nodeAction ? ' role="button" tabindex="0" data-fk="node-' + n.id + '" aria-pressed="' + (on ? 'true' : 'false') + '" aria-label="' + ADE.esc(ADE.t('app.nodeAction', { name: ADE.t(n.labelKey) })) + '"' : '';
      html += '<g class="' + cls + (v.nodeAction ? ' clickable' : '') + '" data-node="' + n.id + '"' + act + (nsKey ? ' data-state="' + ADE.esc(nsKey) + '"' : '') + ' style="--n:' + tok + '">';
      if (on && bx) html += flat ? '<rect class="halo" x="' + (bx.x0 - 7).toFixed(1) + '" y="' + (bx.y0 - 7).toFixed(1) + '" width="' + (bx.x1 - bx.x0 + DEPTH + 14).toFixed(1) + '" height="' + (bx.y1 - bx.y0 + DEPTH + 14).toFixed(1) + '" rx="9"/>' : '<ellipse class="halo" cx="' + bx.cx.toFixed(1) + '" cy="' + (bx.cy + 6).toFixed(1) + '" rx="62" ry="34"/>';
      html += flat ? self._card(n, bx, nsKey, fam, on) : self._isoNode(n, bx, nsKey, fam, on);
      html += '</g>';
    });
    html += '<g class="tokens"></g><g class="typing"></g>';
    html += this._callout(step, opts.prev, changed[0] || active[0], this._zoomTarget(changed.length ? changed : active));
    this.svg.innerHTML = '<title>' + ADE.esc(ADE.t(v.titleKey)) + '</title><desc>' + ADE.esc(ADE.t(v.descKey) + (step ? ' — ' + ADE.t(step.titleKey, step.params) : '')) + '</desc>' + html;
    if (v.nodeAction) this._wireNodes();
    // chuyển động: chỉ khi không giảm chuyển động và không ở chế độ "chỉ sơ đồ"
    this._camera(this._zoomTarget(changed.length ? changed : active), opts.instant || !step);
    var anim = !ADE.motionReduced() && !ADE.diagramOnly() && !opts.instant;
    if (!anim) this.svg.classList.add('still'); else this.svg.classList.remove('still');
    sig.forEach(function (s) { self._token(s, anim, opts.speed || 1); });
    if (fly && anim) { var b0 = this.nodeBox[fly.from], b1 = this.nodeBox[fly.to]; var cy = function (b) { return b.cy != null ? b.cy : (b.y0 + b.y1) / 2; }; if (b0 && b1) this._flyPts([[b0.cx, cy(b0)], [b1.cx, cy(b1)]], fly.tok, opts.speed || 1, true); }
    if (step && step.typing) this._typing(step.typing, anim);
  };
  // node bấm được (view.nodeAction): chuột, Enter, Space → scene.onNode(id)
  Scene.prototype._wireNodes = function () {
    var self = this;
    [].forEach.call(this.svg.querySelectorAll('.node.clickable'), function (g) {
      var id = g.getAttribute('data-node');
      g.addEventListener('click', function () { if (self.onNode) self.onNode(id); });
      g.addEventListener('keydown', function (e) { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); e.stopPropagation(); if (self.onNode) self.onNode(id); } });
    });
  };
  Scene.prototype._isoNode = function (n, bx, nsKey, fam, on) {
    var html = box(n.x, n.y, n.w, n.d, n.h, 'iso-box');
    var tag = iso(n.x + 0.28, n.y + n.d - 0.28, n.h);
    html += '<path class="node-tag" d="M' + tag[0].toFixed(1) + ' ' + (tag[1] - 5).toFixed(1) + 'l5 5-5 5-5-5z"/>';
    html += '<g transform="translate(' + (bx.cx - 19).toFixed(1) + ',' + (bx.cy - 40).toFixed(1) + ')" class="node-icon">' + icon(n.icon || 'chip', { size: 38, sw: 1.5 }).replace('<svg ', '<svg x="0" y="0" ') + '</g>';
    if (on) html += '<g transform="translate(' + (bx.cx - 7).toFixed(1) + ',' + (bx.cy - 62).toFixed(1) + ')" class="node-ptr">' + icon('chevd', { size: 14, sw: 2.4 }).replace('<svg ', '<svg x="0" y="0" ') + '</g>';
    var lb = iso(n.x + n.w, n.y + n.d, 0);
    html += '<text class="node-label" x="' + (bx.cx).toFixed(1) + '" y="' + (lb[1] + 20).toFixed(1) + '" text-anchor="middle">' + ADE.esc(ADE.t(n.labelKey)) + '</text>';
    if (nsKey) {
      var st = ADE.t(nsKey), tw = st.length * 6.7 + 18;
      html += glyph(fam, bx.cx - tw / 2, lb[1] + 27) + '<text class="node-state" x="' + (bx.cx - tw / 2 + 17).toFixed(1) + '" y="' + (lb[1] + 37).toFixed(1) + '">' + ADE.esc(st) + '</text>';
    }
    return html;
  };
  // thẻ phẳng có độ dày (gợi khối isometric), icon, nhãn 1–2 dòng, dòng trạng thái có glyph
  Scene.prototype._card = function (n, b, nsKey, fam, on) {
    var x0 = b.x0, y0 = b.y0, x1 = b.x1, y1 = b.y1, D = DEPTH;
    var h = '<polygon class="iso-right" points="' + [x1, y0 + 3, x1 + D, y0 + 3 + D, x1 + D, y1 + D, x1, y1].join(',') + '"/>' +
      '<polygon class="iso-left" points="' + [x0 + 3, y1, x1, y1, x1 + D, y1 + D, x0 + 3 + D, y1 + D].join(',') + '"/>' +
      '<rect class="card-face" x="' + x0 + '" y="' + y0 + '" width="' + CW + '" height="' + CH + '" rx="3"/>' +
      '<rect class="card-accent" x="' + x0 + '" y="' + y0 + '" width="5" height="' + CH + '"/>';
    if (fam === 'cancel') h += '<path class="card-strike" d="M' + (x0 + 8) + ' ' + (y1 - 6) + 'L' + (x1 - 8) + ' ' + (y0 + 6) + '"/>';
    h += '<g transform="translate(' + (x0 + 12) + ',' + (y0 + 10) + ')" class="node-icon">' + icon(n.icon || 'chip', { size: 24, sw: 1.7 }).replace('<svg ', '<svg x="0" y="0" ') + '</g>';
    var lines = wrap(ADE.t(n.labelKey), 17);
    lines.forEach(function (l, i) { h += '<text class="node-label" x="' + (x0 + 44) + '" y="' + (y0 + 20 + i * 15) + '">' + ADE.esc(l) + '</text>'; });
    if (nsKey) {
      var st = ADE.t(nsKey); if (st.length > 19) st = st.slice(0, 18) + '…';
      h += glyph(fam, x0 + 44, y1 - 18) + '<text class="node-state" x="' + (x0 + 61) + '" y="' + (y1 - 8) + '">' + ADE.esc(st) + '</text>';
    }
    if (on) h += '<rect class="card-ring" x="' + (x0 - 5) + '" y="' + (y0 - 5) + '" width="' + (CW + 10 + D) + '" height="' + (CH + 10 + D) + '" rx="6"/>';
    return h;
  };
  Scene.prototype._stop = function () {
    cancelAnimationFrame(this._raf);
    (this._tokRaf || []).forEach(function (r) { cancelAnimationFrame(r); });
    this._tokRaf = [];
    clearTimeout(this._typeTimer);
  };
  Scene.prototype._token = function (s, anim, speed) {
    var self = this, p;
    if (this.layout === 'iso') {
      var e = null;
      this.view.edges.forEach(function (x) { if (x.id === s.edge) e = x; });
      if (!e) return;
      var en = edgeEnds(this, e, 44); if (!en) return;
      p = [[en.x1, en.y1], [en.x2, en.y2]];
    } else p = this.edgeGeo[s.edge];
    if (!p) return;
    if (s.reverse) p = p.slice().reverse();
    var g = this.svg.querySelector('.tokens');
    var tok = s.tok ? 'var(--tok-' + s.tok + ')' : 'var(--tok-signal)';
    var c = document.createElementNS(NS, 'g');
    c.setAttribute('class', 'token'); c.setAttribute('style', '--n:' + tok);
    c.innerHTML = '<circle r="7"/><circle r="2.6" class="token-core"/>' + (s.label != null ? '<text class="token-label" y="-11" text-anchor="middle">' + ADE.esc(String(s.label)) + '</text>' : '');
    g.appendChild(c);
    var place = function (k) { var q = polyAt(p, k); c.setAttribute('transform', 'translate(' + q[0].toFixed(1) + ',' + q[1].toFixed(1) + ')'); };
    if (!anim) { place(1); return; }
    var t0 = performance.now(), dur = (this.layout === 'iso' ? 900 : 1100) / speed, idx = this._tokRaf.length;
    var tick = function (now) {
      var k = Math.min(1, (now - t0) / dur); place(easeInOut(k));
      if (k < 1) self._tokRaf[idx] = requestAnimationFrame(tick);
    };
    place(0); this._tokRaf[idx] = requestAnimationFrame(tick);
  };
  // token bay giữa hai điểm (dùng khi không có cạnh nối, và giữa các hàng của lanes); xong thì mờ dần
  Scene.prototype._flyPts = function (p, tokName, speed, fade) {
    var self = this, g = this.svg.querySelector('.tokens');
    if (!g) { g = document.createElementNS(NS, 'g'); g.setAttribute('class', 'tokens'); this.svg.appendChild(g); }
    var c = document.createElementNS(NS, 'g');
    c.setAttribute('class', 'token fly'); c.setAttribute('style', '--n:' + (tokName ? 'var(--tok-' + tokName + ')' : 'var(--tok-signal)'));
    c.innerHTML = '<circle r="7"/><circle r="2.6" class="token-core"/>';
    g.appendChild(c);
    var mid = [(p[0][0] + p[1][0]) / 2, Math.min(p[0][1], p[1][1]) - 30];       // vòng cung nhẹ phía trên
    var place = function (k) {
      var a = 1 - k, x = a * a * p[0][0] + 2 * a * k * mid[0] + k * k * p[1][0], y = a * a * p[0][1] + 2 * a * k * mid[1] + k * k * p[1][1];
      c.setAttribute('transform', 'translate(' + x.toFixed(1) + ',' + y.toFixed(1) + ')');
    };
    var t0 = performance.now(), dur = 900 / speed, idx = this._tokRaf.length;
    var tick = function (now) {
      var k = Math.min(1, (now - t0) / dur); place(easeInOut(k));
      if (k < 1) self._tokRaf[idx] = requestAnimationFrame(tick);
      else if (fade && c.animate) c.animate([{ opacity: 1 }, { opacity: 0 }], { duration: 400, fill: 'forwards' });
    };
    place(0); this._tokRaf[idx] = requestAnimationFrame(tick);
  };
  Scene.prototype._typing = function (ty, anim) {
    var b = this.nodeBox[ty.node]; if (!b) return;
    var g = this.svg.querySelector('.typing');
    var tx = document.createElementNS(NS, 'text');
    tx.setAttribute('class', 'type-text'); tx.setAttribute('x', b.cx.toFixed(1)); tx.setAttribute('y', (this.layout === 'iso' ? b.cy - 72 : b.y0 - 10).toFixed(1)); tx.setAttribute('text-anchor', 'middle');
    tx.setAttribute('translate', 'no');
    g.appendChild(tx);
    var code = String(ty.code), i = 0, self = this;
    if (!anim) { tx.textContent = code; return; }
    var tick = function () { i++; tx.textContent = code.slice(0, i) + (i < code.length ? '▍' : ''); if (i < code.length) self._typeTimer = setTimeout(tick, 45); };
    tick();
  };

  /* ---------- lanes: chuyển động liên tục giữa hai bước (kiểu FLIP) ----------
     Mỗi lần vẽ lại, nhớ vị trí/độ dài từng thanh (data-k), từng mốc và vạch "bây giờ". Lần vẽ sau, phần tử nào đã có thì chạy
     từ hình cũ sang hình mới (thanh dài ra, vạch "bây giờ" trượt tới); phần tử mới thì mọc ra từ mép trái / bật lên.
     Dùng Web Animations trên transform/opacity; tắt khi reduced-motion, "Chỉ sơ đồ" hoặc vẽ tức thời (anim = false). */
  Scene.prototype._laneTween = function (anim, nowX, opts) {
    var svg = this.svg, geo = { bars: {}, marks: {}, now: nowX }, prev = this._laneGeo;
    [].forEach.call(svg.querySelectorAll('.bar-g[data-k]'), function (g) { geo.bars[g.getAttribute('data-k')] = { x: +g.getAttribute('data-x'), w: +g.getAttribute('data-w') }; });
    [].forEach.call(svg.querySelectorAll('.lane-mark[data-k]'), function (g) { geo.marks[g.getAttribute('data-k')] = +g.getAttribute('data-x'); });
    this._laneGeo = geo;
    if (!anim || !prev || !svg.animate) return;
    var dur = 560 / ((opts && opts.speed) || 1), ease = 'cubic-bezier(.2,.7,.2,1)', T = { duration: dur, easing: ease };
    [].forEach.call(svg.querySelectorAll('.bar-g[data-k]'), function (g) {
      var k = g.getAttribute('data-k'), n = geo.bars[k], p = prev.bars[k], rect = g.querySelector('.bar'), txt = g.querySelector('.bar-t');
      g.classList.remove('grow');
      if (!rect) return;
      if (p) {
        if (Math.abs(p.x - n.x) < 0.5 && Math.abs(p.w - n.w) < 0.5) return;
        rect.animate([{ transform: 'translateX(' + (p.x - n.x).toFixed(1) + 'px) scaleX(' + (p.w / n.w).toFixed(3) + ')' }, { transform: 'none' }], T);
        if (txt) txt.animate([{ transform: 'translateX(' + (p.x - n.x).toFixed(1) + 'px)' }, { transform: 'none' }], T);
      } else {
        rect.animate([{ transform: 'scaleX(0.02)', opacity: 0.2 }, { transform: 'none', opacity: 1 }], T);
        if (txt) txt.animate([{ opacity: 0 }, { opacity: 0 }, { opacity: 1 }], T);
      }
    });
    [].forEach.call(svg.querySelectorAll('.lane-mark[data-k]'), function (g) {
      var k = g.getAttribute('data-k'), p = prev.marks[k];
      if (p == null) g.animate([{ transform: 'scale(0)', opacity: 0 }, { transform: 'scale(1.25)', opacity: 1, offset: 0.7 }, { transform: 'none', opacity: 1 }], { duration: dur, easing: ease, delay: dur * 0.35, fill: 'backwards' });
      else if (Math.abs(p - geo.marks[k]) > 0.5) g.animate([{ transform: 'translateX(' + (p - geo.marks[k]).toFixed(1) + 'px)' }, { transform: 'none' }], T);
    });
    if (prev.now != null && nowX != null && Math.abs(prev.now - nowX) > 0.5) {
      [].forEach.call(svg.querySelectorAll('.lane-now, .lane-now-t'), function (el) { el.animate([{ transform: 'translateX(' + (prev.now - nowX).toFixed(1) + 'px)' }, { transform: 'none' }], T); });
    }
    var co = svg.querySelector('.dg-callout');
    if (co) co.animate([{ opacity: 0, transform: 'translateY(8px)' }, { opacity: 1, transform: 'none' }], { duration: dur * 0.8, easing: ease, delay: dur * 0.3, fill: 'backwards' });
  };

  /* ---------- bố cục "lanes": hàng = tài nguyên/coroutine, trục ngang = thời gian ---------- */
  // view.lanes(events, step, opts) → {rows:[{id, labelKey|label, group?}], bars:[{row, from, to, kind:'run'|'block'|'wait'|'ready', label?, cur?}],
  //   marks:[{row, t, label?, cur?}], tMax, now, axisKey?}. Track tự suy ra thanh từ nhật ký; lõi chỉ vẽ.
  Scene.prototype._renderLanes = function (step, opts) {
    var v = this.view, d = v.lanes(opts.events || [], step, opts) || { rows: [], bars: [] };
    var LBL = 150, W = 600, top = 52, rowH = 42, gH = 20, RIGHT = LBL + W + 10;
    var tMax = Math.max(10, d.tMax || 10), sx = function (t) { return LBL + 10 + (t / tMax) * W; };
    var html = this._defs(), y = top, rowY = {}, lastGroup = null, rowsHtml = '';
    (d.rows || []).forEach(function (r) {
      if (r.group && r.group !== lastGroup) { rowsHtml += '<text class="lane-group" x="6" y="' + (y + 14) + '">' + ADE.esc(ADE.t(r.group)) + '</text><path class="lane-sep" d="M6 ' + (y + 18) + 'H' + (LBL + W + 20) + '"/>'; y += gH; lastGroup = r.group; }
      rowY[r.id] = y;
      var lab = r.labelKey ? ADE.t(r.labelKey) : r.label;
      rowsHtml += '<text class="lane-label" x="10" y="' + (y + 28) + '">' + ADE.esc(lab.length > 18 ? lab.slice(0, 17) + '…' : lab) + '</text><path class="lane-line" d="M' + (LBL + 10) + ' ' + (y + rowH - 2) + 'H' + (LBL + W + 10) + '"/>';
      y += rowH;
    });
    var H = y + 34;
    // trục thời gian
    var stepT = [1, 2, 5, 10, 20, 25, 50, 100, 200, 250, 500, 1000].filter(function (s) { return tMax / s <= 8; })[0] || 1000, axis = '';
    for (var t = 0; t <= tMax + 1e-9; t += stepT) axis += '<path class="lane-tick" d="M' + sx(t).toFixed(1) + ' ' + (top - 8) + 'V' + (H - 30) + '"/><text class="lane-tick-t" x="' + sx(t).toFixed(1) + '" y="' + (top - 14) + '" text-anchor="middle">' + ADE.num(t) + '</text>';
    axis += '<text class="lane-axis" x="' + (LBL + 10) + '" y="' + (top - 32) + '">' + ADE.esc(ADE.t(d.axisKey || 'app.lanes.axis')) + '</text>';
    html += axis + rowsHtml;
    var anim = !ADE.motionReduced() && !ADE.diagramOnly() && !opts.instant, cur = null, self = this, liveRun = null;
    (d.bars || []).forEach(function (b) {
      var ry = rowY[b.row]; if (ry === undefined) return;
      var x0 = sx(b.from) + 1, x1 = sx(b.to == null ? d.now : b.to) - 1, w = Math.max(3, x1 - x0);
      var live = !b.ghost && b.from <= d.now && (b.to == null || b.to >= d.now - 0.01);
      if (live && b.kind === 'run' && (!liveRun || ry < liveRun.y)) liveRun = { x: x0 + w, y: ry + 13, row: b.row };
      html += '<g class="bar-g' + (b.ghost ? ' ghost' : '') + (live ? ' live' : '') + (b.cur ? ' cur' + (anim ? ' grow' : '') : '') + '" data-k="' + ADE.esc(b.row + '|' + b.from + '|' + b.kind + (b.ghost ? '|g' : '')) + '" data-x="' + x0.toFixed(1) + '" data-w="' + w.toFixed(1) + '">' +
        '<rect class="bar bar-' + b.kind + '" x="' + x0.toFixed(1) + '" y="' + (ry + 13) + '" width="' + w.toFixed(1) + '" height="22" rx="2"' + (b.kind === 'block' ? ' style="fill:url(#' + self.uid + '-hatch)"' : '') + '/>';
      if (b.label && w > b.label.length * 7 + 8) html += '<text class="bar-t" x="' + (x0 + 6).toFixed(1) + '" y="' + (ry + 28) + '">' + ADE.esc(b.label) + '</text>';
      html += '</g>';
      if (b.cur) cur = { x: x0 + w / 2, y: ry + 13, row: b.row };
    });
    (d.marks || []).forEach(function (m) {
      var ry = rowY[m.row]; if (ry === undefined) return;
      var x = sx(m.t);
      var flip = m.label && x + 4 + m.label.length * 6.5 > RIGHT + 30;
      html += '<g class="lane-mark' + (m.cur ? ' cur' : '') + '" data-k="' + ADE.esc(m.row + '|' + m.t + '|' + (m.label || '')) + '" data-x="' + x.toFixed(1) + '"><path d="M' + x.toFixed(1) + ' ' + (ry + 15) + 'l6 9-6 9-6-9z"/>' + (m.label ? '<text class="mark-t" x="' + (flip ? x - 4 : x + 4).toFixed(1) + '" y="' + (ry + 10) + '"' + (flip ? ' text-anchor="end"' : '') + '>' + ADE.esc(m.label) + '</text>' : '') + '</g>';
      if (m.cur && !cur) cur = { x: x, y: ry + 13, row: m.row };
    });
    if (d.now != null) html += '<path class="lane-now" d="M' + sx(d.now).toFixed(1) + ' ' + (top - 6) + 'V' + (H - 28) + '"/><text class="lane-now-t" x="' + sx(d.now).toFixed(1) + '" y="' + (H - 12) + '" text-anchor="' + (sx(d.now) > RIGHT - 30 ? 'end' : 'middle') + '">' + ADE.esc(ADE.t('app.lanes.now', { t: ADE.num(d.now) })) + '</text>';
    // chú thích trên hình gắn vào thanh vừa đổi
    var full = [0, -70, RIGHT + 50, H + 70];
    if (step) {
      var lines = wrap(ADE.t(step.titleKey, step.params), 44), w2 = Math.min(380, Math.max.apply(null, lines.map(function (l) { return l.length; })) * 7.3 + 24), h2 = lines.length * 16 + 12;
      var cx = cur ? cur.x : LBL + W / 2, x2 = Math.max(4, Math.min(full[2] - w2 - 4, cx - w2 / 2)), y2 = -62;
      html += '<g class="dg-callout">' + (cur ? '<path class="dg-callout-ptr" d="M' + Math.max(x2 + 10, Math.min(x2 + w2 - 10, cx)).toFixed(1) + ' ' + (y2 + h2) + 'L' + cx.toFixed(1) + ' ' + (cur.y - 2) + '"/>' : '') +
        '<rect x="' + x2.toFixed(1) + '" y="' + y2 + '" width="' + w2.toFixed(1) + '" height="' + h2 + '" rx="3"/>';
      lines.forEach(function (l, i) { html += '<text class="dg-callout-t" x="' + (x2 + 12).toFixed(1) + '" y="' + (y2 + 19 + i * 16) + '">' + ADE.esc(l) + '</text>'; });
      html += '</g>';
    }
    this.full = full; this.setVB(full); this._fit();
    this.svg.innerHTML = '<title>' + ADE.esc(ADE.t(v.titleKey)) + '</title><desc>' + ADE.esc(ADE.t(v.descKey) + (step ? ' — ' + ADE.t(step.titleKey, step.params) : '')) + '</desc>' + html;
    if (!anim) this.svg.classList.add('still'); else this.svg.classList.remove('still');
    this._laneTween(anim, d.now != null ? sx(d.now) : null, opts);
    var pc = this._laneCur, here = liveRun || cur;
    if (anim && pc && here && pc.row !== here.row) this._flyPts([[pc.x, pc.y + 11], [here.x, here.y + 11]], null, opts.speed || 1, true);
    this._laneCur = here ? { x: here.x, y: here.y, row: here.row } : pc;
    this.lastLanes = d;
  };
  Scene.prototype.destroy = function () { this._stop(); };

  // các họ trạng thái xuất hiện trong danh sách bước (để dựng chú giải ổn định cho cả mô phỏng)
  function familiesIn(steps, view) {
    var seen = {};
    (steps || []).forEach(function (s) { var ns = s.nodeStates || {}; Object.keys(ns).forEach(function (id) { var f = famOf(ns[id], view); if (f && f !== 'info') seen[f] = 1; }); });
    return FAM_ORDER.filter(function (f) { return seen[f]; });
  }

  /* ---------- timeline (sơ đồ tuần tự) ---------- */
  // events: [{e:{t,kind,subject,to?,detailKey,params}, step}]
  function timeline(container, view, trackId, events, opts) {
    opts = opts || {};
    var lanes = [], labels = {};
    view.nodes.forEach(function (n) { labels[n.id] = n.labelKey; });
    var addLane = function (id) { if (id && lanes.indexOf(id) < 0) lanes.push(id); };
    view.nodes.forEach(function (n) { if (events.some(function (x) { return x.e.subject === n.id || x.e.to === n.id; })) addLane(n.id); });
    events.forEach(function (x) { addLane(x.e.subject); addLane(x.e.to); });
    if (!lanes.length) view.nodes.slice(0, 3).forEach(function (n) { addLane(n.id); });
    var LW = 150, W = Math.max(520, lanes.length * LW + 40), top = 52, rowH = 34;
    var H = top + Math.max(events.length, 1) * rowH + 24;
    var X = function (id) { return 20 + LW / 2 + lanes.indexOf(id) * LW; };
    var h = '<title>' + ADE.esc(ADE.t('app.timeline')) + '</title><desc>' + ADE.esc(ADE.t('app.timelineDesc', { n: events.length })) + '</desc>';
    lanes.forEach(function (id) {
      var lb = labels[id] ? ADE.t(labels[id]) : id;
      h += '<g class="lane"><text class="lane-title" x="' + X(id) + '" y="24" text-anchor="middle">' + ADE.esc(lb.length > 20 ? lb.slice(0, 19) + '…' : lb) + '</text><line class="lifeline" x1="' + X(id) + '" y1="34" x2="' + X(id) + '" y2="' + (H - 8) + '"/></g>';
    });
    events.forEach(function (x, i) {
      var ev = x.e, y = top + i * rowH + 12, kd = ADE.kinds[ev.kind] || { tok: 'thread', icon: 'dot' };
      var last = i === events.length - 1, cls = 'tl-ev' + (last ? ' current' : '');
      var txt = ADE.t(ev.detailKey, ev.params), shown = txt.length > 36 ? txt.slice(0, 35) + '…' : txt;
      var sx = X(ev.subject), kl = ADE.kindLabel(trackId, ev.kind);
      h += '<g class="' + cls + '" style="--n:var(--tok-' + kd.tok + ')" data-step="' + x.step + '"><title>' + ADE.esc(kl + ': ' + txt) + '</title>';
      if (ev.to && ev.to !== ev.subject) {
        var tx = X(ev.to), dir = tx > sx ? 1 : -1;
        h += '<line class="tl-arrow' + (last && !ADE.motionReduced() && !ADE.diagramOnly() ? ' draw-in' : '') + '" x1="' + sx + '" y1="' + y + '" x2="' + (tx - dir * 4) + '" y2="' + y + '" marker-end="url(#arw)"/>' +
          '<text class="tl-text" x="' + ((sx + tx) / 2) + '" y="' + (y - 6) + '" text-anchor="middle">' + ADE.esc(shown) + '</text>';
      } else {
        var lastLane = lanes.indexOf(ev.subject) === lanes.length - 1 && lanes.length > 1;
        h += '<text class="tl-text" x="' + (lastLane ? sx - 16 : sx + 16) + '" y="' + (y + 4) + '"' + (lastLane ? ' text-anchor="end"' : '') + '>' + ADE.esc(shown) + '</text>';
      }
      h += '<g transform="translate(' + (sx - 8) + ',' + (y - 8) + ')" class="tl-dot"><circle cx="8" cy="8" r="9"/>' + icon(kd.icon, { size: 11, sw: 2 }).replace('<svg ', '<svg x="2.5" y="2.5" ') + '</g></g>';
    });
    var defs = '<defs><marker id="arw" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M1 1.5L8.5 5 1 8.5z" class="arw-head"/></marker></defs>';
    var svg = container.querySelector('svg.timeline');
    if (!svg) {
      svg = document.createElementNS(NS, 'svg'); svg.setAttribute('class', 'timeline'); svg.setAttribute('role', 'img');
      container.appendChild(svg);
    }
    svg.setAttribute('viewBox', '0 0 ' + W + ' ' + H);
    svg.setAttribute('width', W);
    svg.setAttribute('height', H);
    svg.innerHTML = defs + h;
    container.scrollTop = container.scrollHeight;
  }

  ADE.diagram = { icon: icon, logo: logo, iso: iso, box: box, Scene: Scene, scene: function (c, v) { return new Scene(c, v); }, timeline: timeline, ICONS: ICONS,
    famOf: famOf, familiesIn: familiesIn, glyphSvg: glyphSvg, barSvg: barSvg, FAM_ORDER: FAM_ORDER };
})();
