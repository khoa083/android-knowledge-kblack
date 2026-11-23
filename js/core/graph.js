/* Đồ thị tương tác kiểu "graph view" (mô phỏng lực, kéo node, kéo nền để di chuyển, phóng to/thu nhỏ, rê chuột để làm nổi node lân cận).
   Lõi chung, KHÔNG biết id track nào: trang (app.js) dựng danh sách node và cạnh từ registry rồi gọi ADE.graph.create.
   Node: { id, kind: 'hub' | 'leaf', label, title, href, color, short }
   Cạnh: { a, b, kind: 'member' | 'bridge' | 'path' | 'term', label }
   Không thư viện ngoài. Vị trí ban đầu tất định (không random) để ảnh chụp kiểm thử ổn định.
   Giảm chuyển động: tính xong bố cục ngay (không chạy hoạt ảnh); kéo node vẫn được. Dừng mô phỏng khi tab bị ẩn. */
(function () {
  'use strict';
  var NS = 'http://www.w3.org/2000/svg';
  var LEN = { member: 58, bridge: 150, path: 110, term: 40 };
  var STR = { member: 0.09, bridge: 0.035, path: 0.03, term: 0.12 };

  function el(name, attrs) { var e = document.createElementNS(NS, name); for (var k in attrs) if (attrs[k] != null) e.setAttribute(k, attrs[k]); return e; }

  function create(opts) {
    var h = ADE.ui.h, T = function (k, p) { return ADE.t(k, p); };
    var height = opts.height || 420;
    var wrap = h('div', { class: 'gv' + (opts.labels === 'all' ? ' gv-labels-all' : ''), role: 'group', 'aria-label': opts.label || T('app.graph.name') });
    var bar = h('div', { class: 'gv-bar' });
    var svg = el('svg', { class: 'gv-svg', role: 'img', 'aria-label': opts.label || T('app.graph.name') });
    var title = el('title', {}); title.textContent = opts.label || T('app.graph.name'); svg.appendChild(title);
    var world = el('g', { class: 'gv-world' });
    var gEdges = el('g', { class: 'gv-edges' }), gNodes = el('g', { class: 'gv-nodes' });
    world.appendChild(gEdges); world.appendChild(gNodes); svg.appendChild(world);
    var info = h('p', { class: 'gv-info', 'aria-live': 'polite', text: T('app.graph.hint') });
    var stage = h('div', { class: 'gv-stage', style: 'height:' + height + 'px' }, svg);
    wrap.appendChild(bar); wrap.appendChild(stage); wrap.appendChild(info);
    if (opts.legend !== false) {
      var lg = h('div', { class: 'gv-legend' });
      [['hub', 'app.graph.lgHub'], ['leaf', 'app.graph.lgLeaf'], ['bridge', 'app.graph.lgBridge'], ['member', 'app.graph.lgMember'], ['path', 'app.graph.lgPath'], ['term', 'app.graph.lgTerm']].forEach(function (x) {
        if ((opts.legendKinds || ['hub', 'leaf', 'bridge', 'member', 'path']).indexOf(x[0]) < 0) return;
        lg.appendChild(h('span', { class: 'gv-lg gv-lg-' + x[0] }, h('i', { 'aria-hidden': 'true' }), h('span', { text: T(x[1]) })));
      });
      wrap.appendChild(lg);
    }

    var nodes = [], edges = [], byId = {}, adj = {};
    var GX = 0.0025, GY = 0.004, W = 640, H = height, view = { x: 0, y: 0, k: 1 }, alpha = 0, raf = 0, dead = false, hoverId = null, focusId = null;
    var prevPos = {};

    function build(data) {
      nodes.forEach(function (n) { prevPos[n.id] = { x: n.x, y: n.y }; });
      nodes = data.nodes.map(function (n) { var o = {}; for (var k in n) o[k] = n[k]; return o; });
      byId = {}; nodes.forEach(function (n) { byId[n.id] = n; });
      edges = data.edges.filter(function (e) { return byId[e.a] && byId[e.b] && e.a !== e.b; });
      adj = {}; nodes.forEach(function (n) { adj[n.id] = {}; });
      edges.forEach(function (e) { adj[e.a][e.b] = 1; adj[e.b][e.a] = 1; });
      // vị trí ban đầu tất định: hub trên một vòng, leaf quanh hub của nó (hoặc quanh tâm nếu không có hub)
      var hubs = nodes.filter(function (n) { return n.kind === 'hub'; });
      hubs.forEach(function (n, i) { var a = -Math.PI / 2 + i * 2 * Math.PI / Math.max(1, hubs.length); n._a = a; n.x = Math.cos(a) * 260; n.y = Math.sin(a) * 170; });
      var count = {};
      nodes.forEach(function (n, i) {
        if (prevPos[n.id]) { n.x = prevPos[n.id].x; n.y = prevPos[n.id].y; }
        else if (n.kind !== 'hub') {
          var hub = null; for (var j in adj[n.id]) if (byId[j].kind === 'hub') { hub = byId[j]; break; }
          var c = hub ? (count[hub.id] = (count[hub.id] || 0) + 1) : i + 1, base = hub ? hub._a : 0, r = hub ? 40 + (c % 3) * 14 : 60 + (i % 5) * 20;
          var a = base + c * 2.399;
          n.x = (hub ? hub.x : 0) + Math.cos(a) * r; n.y = (hub ? hub.y : 0) + Math.sin(a) * r;
        }
        n.vx = 0; n.vy = 0; n.fx = null; n.fy = null;
        n.deg = Object.keys(adj[n.id]).length;
        n.r = n.kind === 'hub' ? 15 : Math.min(9, 4 + Math.sqrt(n.deg) * 1.3);
      });
      draw();
    }

    function tick() {
      var i, j, a, b, dx, dy, d2, d, f, n = nodes.length;
      for (i = 0; i < n; i++) {
        a = nodes[i];
        for (j = i + 1; j < n; j++) {
          b = nodes[j]; dx = b.x - a.x; dy = b.y - a.y; d2 = dx * dx + dy * dy || 0.01;
          if (d2 > 250000) continue;
          d = Math.sqrt(d2); f = (a.kind === 'hub' && b.kind === 'hub' ? 12000 : a.kind === 'hub' || b.kind === 'hub' ? 1600 : 700) / d2;
          dx /= d; dy /= d; a.vx -= dx * f; a.vy -= dy * f; b.vx += dx * f; b.vy += dy * f;
        }
      }
      edges.forEach(function (e) {
        a = byId[e.a]; b = byId[e.b]; dx = b.x - a.x; dy = b.y - a.y; d = Math.sqrt(dx * dx + dy * dy) || 0.01;
        f = (d - (LEN[e.kind] || 60)) * (STR[e.kind] || 0.05); dx /= d; dy /= d;
        a.vx += dx * f; a.vy += dy * f; b.vx -= dx * f; b.vy -= dy * f;
      });
      nodes.forEach(function (p) {
        p.vx -= p.x * GX; p.vy -= p.y * GY;
        if (p.fx != null) { p.x = p.fx; p.y = p.fy; p.vx = p.vy = 0; return; }
        p.vx *= 0.82; p.vy *= 0.82;
        var sp = Math.sqrt(p.vx * p.vx + p.vy * p.vy), lim = 12 * Math.max(alpha, 0.2);
        if (sp > lim) { p.vx *= lim / sp; p.vy *= lim / sp; }
        p.x += p.vx * alpha * 2; p.y += p.vy * alpha * 2;
      });
      alpha *= 0.985;
    }

    function settle(nTicks) { alpha = 1; for (var i = 0; i < nTicks; i++) tick(); }
    function loop() {
      raf = 0; if (dead) return;
      tick(); positions();
      if (alpha > 0.02 && !document.hidden) raf = requestAnimationFrame(loop);
    }
    function heat(a) {
      alpha = Math.max(alpha, a);
      if (ADE.motionReduced()) { var guard = 0; while (alpha > 0.02 && guard++ < 400) tick(); positions(); return; }
      if (!raf && !dead) raf = requestAnimationFrame(loop);
    }

    var lineEls = [], nodeEls = [];
    function draw() {
      while (gEdges.firstChild) gEdges.removeChild(gEdges.firstChild);
      while (gNodes.firstChild) gNodes.removeChild(gNodes.firstChild);
      lineEls = edges.map(function (e) {
        var ln = el('line', { class: 'gv-e gv-e-' + e.kind });
        if (e.label) { var t = el('title', {}); t.textContent = e.label; ln.appendChild(t); }
        gEdges.appendChild(ln); return ln;
      });
      nodeEls = nodes.map(function (n) {
        var g = el(n.href ? 'a' : 'g', { class: 'gv-n gv-n-' + n.kind, 'data-id': n.id });
        if (n.href) { g.setAttribute('href', n.href); g.setAttribute('tabindex', n.kind === 'hub' ? '0' : '-1'); g.setAttribute('aria-label', n.title || n.label); }
        var t = el('title', {}); t.textContent = n.title || n.label; g.appendChild(t);
        var c = el('circle', { r: n.r, style: n.color ? 'fill:' + n.color : null }); g.appendChild(c);
        if (n.kind === 'hub' && n.short) { var s = el('text', { class: 'gv-code', 'text-anchor': 'middle', dy: '0.35em' }); s.textContent = n.short; g.appendChild(s); }
        var lb = el('text', { class: 'gv-label', 'text-anchor': 'middle', dy: (n.r + 12) }); lb.textContent = n.label; g.appendChild(lb);
        g.addEventListener('pointerdown', function (ev) { startDrag(ev, n); });
        g.addEventListener('click', function (ev) { if (n._moved) { ev.preventDefault(); n._moved = false; } });
        g.addEventListener('pointerenter', function () { hoverId = n.id; highlight(); });
        g.addEventListener('pointerleave', function () { if (hoverId === n.id) { hoverId = null; highlight(); } });
        g.addEventListener('focus', function () { focusId = n.id; highlight(); });
        g.addEventListener('blur', function () { if (focusId === n.id) { focusId = null; highlight(); } });
        gNodes.appendChild(g); return g;
      });
      positions(); highlight();
    }
    function positions() {
      edges.forEach(function (e, i) {
        var a = byId[e.a], b = byId[e.b], ln = lineEls[i];
        ln.setAttribute('x1', a.x.toFixed(1)); ln.setAttribute('y1', a.y.toFixed(1)); ln.setAttribute('x2', b.x.toFixed(1)); ln.setAttribute('y2', b.y.toFixed(1));
      });
      nodes.forEach(function (n, i) { nodeEls[i].setAttribute('transform', 'translate(' + n.x.toFixed(1) + ',' + n.y.toFixed(1) + ')'); });
    }
    function highlight() {
      var id = hoverId || focusId;
      wrap.classList.toggle('gv-focus', !!id);
      wrap.classList.toggle('gv-zoomed', view.k >= 1.8);
      nodes.forEach(function (n, i) { var on = id && (n.id === id || adj[id][n.id]); nodeEls[i].classList.toggle('on', !!on); nodeEls[i].classList.toggle('me', n.id === id); });
      edges.forEach(function (e, i) { lineEls[i].classList.toggle('on', !!(id && (e.a === id || e.b === id))); });
      if (id) {
        var n = byId[id], names = Object.keys(adj[id]).map(function (j) { return byId[j].label; });
        info.textContent = (n.title || n.label) + ' · ' + T('app.graph.links', { n: names.length }) + (names.length ? ': ' + names.slice(0, 8).join(', ') + (names.length > 8 ? '…' : '') : '');
      } else info.textContent = T('app.graph.hint');
    }

    /* ---- kéo node, kéo nền, phóng to ---- */
    function toWorld(ev) { var r = svg.getBoundingClientRect(); return { x: (ev.clientX - r.left - W / 2 - view.x) / view.k, y: (ev.clientY - r.top - H / 2 - view.y) / view.k }; }
    var drag = null;
    function startDrag(ev, n) {
      if (ev.button !== 0 && ev.pointerType === 'mouse') return;
      ev.stopPropagation();
      var p = toWorld(ev); drag = { n: n, x0: ev.clientX, y0: ev.clientY, dx: n.x - p.x, dy: n.y - p.y, id: ev.pointerId };
      n._moved = false;
      try { svg.setPointerCapture(ev.pointerId); } catch (e) { /* noop */ }
    }
    var pan = null;
    svg.addEventListener('pointerdown', function (ev) {
      if (drag || (ev.button !== 0 && ev.pointerType === 'mouse')) return;
      pan = { x0: ev.clientX, y0: ev.clientY, vx: view.x, vy: view.y };
      try { svg.setPointerCapture(ev.pointerId); } catch (e) { /* noop */ }
    });
    svg.addEventListener('pointermove', function (ev) {
      if (drag) {
        if (Math.abs(ev.clientX - drag.x0) + Math.abs(ev.clientY - drag.y0) > 4) drag.n._moved = true;
        if (!drag.n._moved) return;
        var p = toWorld(ev); drag.n.fx = p.x + drag.dx; drag.n.fy = p.y + drag.dy; drag.n.x = drag.n.fx; drag.n.y = drag.n.fy;
        heat(0.25); positions();
      } else if (pan) { view.x = pan.vx + ev.clientX - pan.x0; view.y = pan.vy + ev.clientY - pan.y0; applyView(); }
    });
    function endPointer() {
      if (drag) { drag.n.fx = null; drag.n.fy = null; if (drag.n._moved) heat(0.2); drag = null; }
      pan = null;
    }
    svg.addEventListener('pointerup', endPointer); svg.addEventListener('pointercancel', endPointer);
    // chỉ phóng to bằng bánh xe khi giữ Ctrl/⌘, để cuộn trang không bị đồ thị giữ lại
    svg.addEventListener('wheel', function (ev) {
      if (!ev.ctrlKey && !ev.metaKey) return;
      ev.preventDefault();
      var r = svg.getBoundingClientRect(), cx = ev.clientX - r.left - W / 2, cy = ev.clientY - r.top - H / 2;
      zoomAt(ev.deltaY < 0 ? 1.15 : 1 / 1.15, cx, cy);
    }, { passive: false });
    function zoomAt(f, cx, cy) {
      var k = Math.max(0.4, Math.min(3, view.k * f)); f = k / view.k;
      view.x = cx - (cx - view.x) * f; view.y = cy - (cy - view.y) * f; view.k = k; applyView(); highlight();
    }
    function applyView() { world.setAttribute('transform', 'translate(' + (W / 2 + view.x).toFixed(1) + ',' + (H / 2 + view.y).toFixed(1) + ') scale(' + view.k.toFixed(3) + ')'); }
    function fit() {
      if (!nodes.length) return;
      var x0 = Infinity, x1 = -Infinity, y0 = Infinity, y1 = -Infinity;
      nodes.forEach(function (n) { x0 = Math.min(x0, n.x); x1 = Math.max(x1, n.x); y0 = Math.min(y0, n.y); y1 = Math.max(y1, n.y); });
      var k = Math.min((W - 80) / Math.max(1, x1 - x0), (H - 80) / Math.max(1, y1 - y0), 1.2);
      view.k = Math.max(0.4, k); view.x = -(x0 + x1) / 2 * view.k; view.y = -(y0 + y1) / 2 * view.k; applyView(); highlight();
    }
    function measure() {
      W = Math.max(280, stage.clientWidth || 640); H = height; svg.setAttribute('viewBox', '0 0 ' + W + ' ' + H); applyView();
      // khung hẹp (điện thoại): kéo các node về giữa theo chiều ngang mạnh hơn để đồ thị dựng đứng, đỡ phải thu nhỏ
      GX = 0.0025 * Math.max(1, 640 / W); GY = 0.004 * Math.max(0.6, 440 / H);
    }

    var btn = function (key, icon, fn) { return h('button', { type: 'button', class: 'btn icon small', 'aria-label': T(key), title: T(key), onclick: fn }, ADE.ui.icon(icon, { size: 14 })); };
    var tools = h('span', { class: 'gv-tools' },
      btn('app.graph.zoomOut', 'minus', function () { zoomAt(1 / 1.25, 0, 0); }),
      btn('app.graph.zoomIn', 'add', function () { zoomAt(1.25, 0, 0); }),
      btn('app.graph.reset', 'reset', function () { build(opts.data()); settle(200); fit(); heat(0.3); }));
    (opts.toggles || []).forEach(function (tg) {
      var id = 'gv-' + tg.id + '-' + Math.random().toString(36).slice(2, 7);
      var cb = h('input', { type: 'checkbox', id: id, checked: tg.get() ? true : null, onchange: function () { tg.set(cb.checked); build(opts.data()); heat(0.6); } });
      bar.appendChild(h('label', { class: 'gv-toggle', for: id }, cb, h('span', { text: T(tg.labelKey) })));
    });
    bar.appendChild(tools);

    function onVis() { if (!document.hidden && alpha > 0.02) heat(alpha); }
    document.addEventListener('visibilitychange', onVis);
    var ro = typeof ResizeObserver === 'function' ? new ResizeObserver(function () { measure(); }) : null;

    build(opts.data());
    settle(ADE.motionReduced() ? 500 : 260);
    // đo kích thước sau khi phần tử được gắn vào trang
    requestAnimationFrame(function () { if (dead) return; measure(); if (W < 560) settle(260); fit(); positions(); heat(ADE.motionReduced() ? 0 : 0.25); if (ro) ro.observe(stage); });
    measure(); fit(); positions();

    return {
      el: wrap,
      destroy: function () { dead = true; if (raf) cancelAnimationFrame(raf); document.removeEventListener('visibilitychange', onVis); if (ro) ro.disconnect(); }
    };
  }

  ADE.graph = { create: create };
})();
