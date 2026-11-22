/* ui.js — DOM helper, tab, badge, callout, dialog, mock-frame và "stage" mô phỏng (ba vùng).
   Bố cục ba vùng: canvas (tab Sơ đồ/Timeline) · panel ngữ cảnh (Tổng quan → Bước n/N → Tổng kết, tab Giải thích/Mã) · bảng nhật ký sự kiện.
   Lõi không biết track nào: mọi thứ lấy từ view config của model (ADE.views[modelId]). */
(function () {
  'use strict';
  var ADE = window.ADE = window.ADE || {};
  var ui = ADE.ui = {};

  /* ---------- DOM ---------- */
  function h(tag, attrs) {
    var el = document.createElement(tag);
    if (attrs) Object.keys(attrs).forEach(function (k) {
      var v = attrs[k];
      if (v === false || v === null || v === undefined) return;
      if (k === 'class') el.className = v;
      else if (k === 'text') el.textContent = v;
      else if (k === 'html') el.innerHTML = v;
      else if (k.slice(0, 2) === 'on' && typeof v === 'function') el.addEventListener(k.slice(2), v);
      else if (v === true) el.setAttribute(k, '');
      else el.setAttribute(k, v);
    });
    for (var i = 2; i < arguments.length; i++) append(el, arguments[i]);
    return el;
  }
  function append(el, c) {
    if (c === null || c === undefined || c === false) return;
    if (Array.isArray(c)) { c.forEach(function (x) { append(el, x); }); return; }
    if (typeof c === 'string' || typeof c === 'number') { el.appendChild(document.createTextNode(String(c))); return; }
    el.appendChild(c);
  }
  ui.h = h;
  ui.icon = function (name, o) { var s = document.createElement('span'); s.className = 'ic-wrap'; s.innerHTML = ADE.diagram.icon(name, o); return s; };
  ui.html = function (tag, cls, html) { return h(tag, { class: cls, html: html }); };
  // Chữ HOA chỉ cho tiêu đề ngắn (≤ 40 ký tự): STYLE-REFERENCE 4.3.
  ui.caps = function (s) { return s.length <= 40 ? 'caps' : ''; };
  ui.clear = function (el) { while (el.firstChild) el.removeChild(el.firstChild); return el; };
  // Giữ focus khi dựng lại DOM: phần tử đang focus có data-fk thì sau khi dựng lại, focus phần tử cùng data-fk;
  // nếu nó biến mất, đưa focus về vùng mô phỏng (hoặc nội dung chính) thay vì để rơi về <body>.
  ui.withFocus = function (fn) {
    var ae = document.activeElement, key = ae && ae.getAttribute ? ae.getAttribute('data-fk') : null, had = ae && ae !== document.body;
    fn();
    if (key) {
      var n = document.querySelector('[data-fk="' + key.replace(/"/g, '') + '"]');
      if (n && !n.disabled) { n.focus({ preventScroll: true }); return; }
    }
    if (had && (!document.activeElement || document.activeElement === document.body)) {
      var f = document.querySelector('.stage') || document.getElementById('main');
      if (f) f.focus({ preventScroll: true });
    }
  };

  /* ---------- aria-live ---------- */
  ui.announce = function (text) {
    var r = document.getElementById('ade-live');
    if (!r) return;
    r.textContent = '';
    setTimeout(function () { r.textContent = text; }, 30);
  };

  /* ---------- tab (WAI-ARIA APG: tablist) ---------- */
  ui.tabs = function (items, active, onChange, label) {
    var list = h('div', { class: 'tabs', role: 'tablist', 'aria-label': label || '' });
    items.forEach(function (it) {
      var b = h('button', { type: 'button', role: 'tab', class: 'tab' + (it.id === active ? ' on' : ''), 'aria-selected': it.id === active ? 'true' : 'false', tabindex: it.id === active ? '0' : '-1', 'data-id': it.id, 'data-fk': 'tab:' + (label || '') + ':' + it.id },
        it.icon ? ui.icon(it.icon, { size: 14 }) : null, h('span', { text: it.label }));
      b.addEventListener('click', function () { ui.withFocus(function () { onChange(it.id); }); });
      list.appendChild(b);
    });
    list.addEventListener('keydown', function (e) {
      if (e.key !== 'ArrowRight' && e.key !== 'ArrowLeft') return;
      var tabs = [].slice.call(list.querySelectorAll('[role=tab]')), i = tabs.indexOf(document.activeElement);
      if (i < 0) return;
      i = (i + (e.key === 'ArrowRight' ? 1 : -1) + tabs.length) % tabs.length;
      e.preventDefault(); tabs[i].focus(); tabs[i].click();
    });
    return list;
  };

  /* ---------- badge, callout ---------- */
  ui.badge = function (key) { return h('span', { class: 'badge badge-' + key, text: ADE.t('badge.' + key) }); };
  ui.stepBadge = function (type) { return h('span', { class: 'steptype st-' + type, text: ADE.t('step.' + type) }); };
  ui.callout = function (kind, html) {
    return h('aside', { class: 'callout co-' + kind }, h('div', { class: 'co-h' }, ui.icon(kind, { size: 16 }), h('span', { text: ADE.t('app.callout.' + kind) })), h('div', { class: 'co-b prose', html: html }));
  };
  ui.kindChip = function (trackId, kind) {
    var kd = ADE.kinds[kind] || { tok: 'thread', icon: 'dot' };
    return h('span', { class: 'kchip', style: '--n:var(--tok-' + kd.tok + ')' }, ui.icon(kd.icon, { size: 12, sw: 2 }), h('span', { text: ADE.kindLabel(trackId, kind) }));
  };
  ui.panel = function (titleText, body, cls, right) {
    return h('section', { class: 'panel ' + (cls || '') }, h('header', { class: 'panel-h' }, h('h2', { class: 'caps', text: titleText }), right || null), body);
  };

  /* ---------- khối mã: translate="no", dòng được highlight; snippet = {lang, illustrative?, lines:[string | {vi,en}]} ---------- */
  ui.codeBlock = function (sn, hlLines) {
    hlLines = hlLines || [];
    var wrap = h('div', { class: 'code-wrap' });
    var head = h('div', { class: 'code-h' }, h('span', { class: 'code-lang', text: sn.lang || 'kotlin' }));
    if (sn.illustrative) head.appendChild(ui.badge('simplified'));
    if (sn.illustrative) head.lastChild.textContent = ADE.t('app.illustrative');
    wrap.appendChild(head);
    var pre = h('pre', { class: 'code', translate: 'no', tabindex: '0', 'aria-label': ADE.t('app.codeBlock') });
    sn.lines.forEach(function (ln, i) {
      var on = hlLines.indexOf(i + 1) >= 0;
      pre.appendChild(h('span', { class: 'cl' + (on ? ' hl' : '') }, h('span', { class: 'ln', 'aria-hidden': 'true', text: String(i + 1) }), h('span', { class: 'lt', text: typeof ln === 'string' ? ln : (ln[ADE.lang] || ln.vi) }), on ? h('span', { class: 'sr-only', text: ' ◀' }) : null));
    });
    wrap.appendChild(pre);
    return wrap;
  };

  /* ---------- hộp thoại (dùng <dialog> gốc: bẫy focus + Esc) ---------- */
  ui.dialog = function (title, body, opts) {
    opts = opts || {};
    var d = h('dialog', { class: 'dlg ' + (opts.cls || ''), 'aria-label': title });
    var closeBtn = h('button', { type: 'button', class: 'btn icon', 'aria-label': ADE.t('app.close') }, ui.icon('close', { size: 16 }));
    d.appendChild(h('header', { class: 'dlg-h' }, h('h2', { class: 'caps', text: title }), closeBtn));
    d.appendChild(h('div', { class: 'dlg-b' }, body));
    var prevFocus = document.activeElement;
    var close = function () { if (d.open) d.close(); };
    closeBtn.addEventListener('click', close);
    d.addEventListener('click', function (e) { if (e.target === d) close(); });
    ADE.markMissing(d);
    d.addEventListener('close', function () { if (d.parentNode) d.parentNode.removeChild(d); if (prevFocus && prevFocus.focus) prevFocus.focus(); if (opts.onClose) opts.onClose(); });
    document.body.appendChild(d);
    if (d.showModal) d.showModal(); else d.setAttribute('open', '');
    return { el: d, close: close };
  };

  /* ---------- khung điện thoại mẫu (mock device frame), dùng chung ---------- */
  // Nội dung bên trong là minh hoạ: token ngữ nghĩa không áp dụng; khung có viền và nhãn "Giao diện mẫu".
  ui.mockFrame = function (screen, o) {
    o = o || {};
    var clsSize = o.size ? ' mf-' + o.size : '';
    return h('figure', { class: 'mock-frame' + clsSize },
      h('div', { class: 'mf-device', role: 'group', 'aria-label': ADE.t('app.sampleUi') },
        h('div', { class: 'mf-status' }, h('span', { text: '9:41' }), h('span', { class: 'mf-icons', 'aria-hidden': 'true' }, '▮▮▮')),
        h('div', { class: 'mf-screen' }, screen),
        h('div', { class: 'mf-nav', 'aria-hidden': 'true' }, h('span', { class: 'mf-pill' }))),
      h('figcaption', { class: 'mf-label' }, ui.icon('info', { size: 13 }), h('span', { text: ADE.t('app.sampleUi') })));
  };

  /* ---------- stage mô phỏng ---------- */
  // opts: {session, trackId, modelId, mode:'guided'|'live', viewState, goals:fn, onPos:fn(pos,fromUser), onQuiz:fn}
  ui.mountSim = function (container, opts) {
    var S = opts.session, def = S.def, vw = ADE.views[opts.modelId] || { nodes: [], edges: [] };
    var vs = opts.viewState = opts.viewState || { canvasTab: 'diagram', sideTab: 'explain', mtab: 'diagram' };
    var track = ADE.getTrack(opts.trackId);
    var disc = S.kind === 'discrete';
    var offs = [];
    var root = h('section', { class: 'stage', tabindex: '0', 'data-mtab': vs.mtab, 'aria-label': ADE.t('app.simArea') });
    container.appendChild(root);

    /* -- khối sandbox (điều khiển của model) -- */
    var sandbox = def.controls && def.controls.length ? h('div', { class: 'sandbox panel' }) : null;
    /* -- canvas -- */
    var canvasTabs = h('div', { class: 'tabs-slot' });
    var metrics = h('div', { class: 'metrics', role: 'group', 'aria-label': ADE.t('app.metrics') });
    var diagramBox = h('div', { class: 'view-diagram', tabindex: '0', role: 'region', 'aria-label': ADE.t('app.diagram') });
    var timelineBox = h('div', { class: 'view-timeline', tabindex: '0', role: 'region', 'aria-label': ADE.t('app.timeline') });
    var conceptual = h('span', { class: 'badge badge-simplified conceptual', text: ADE.t('app.conceptual') });
    var diagOnly = h('button', { type: 'button', class: 'btn small toggle', 'aria-pressed': ADE.diagramOnly() ? 'true' : 'false', title: ADE.t('app.diagramOnlyHint'), onclick: function () {
      var on = !ADE.diagramOnly(); document.documentElement.classList.toggle('diagram-only', on); ADE.store.set('diagramOnly', on);
      diagOnly.setAttribute('aria-pressed', on ? 'true' : 'false'); if (scene) refreshCanvas(false);
    } }, ui.icon('eye', { size: 14 }), h('span', { text: ADE.t('app.diagramOnly') }));
    var canvasHead = h('header', { class: 'panel-h' }, h('h2', { class: 'caps', text: ADE.t('app.canvas') }), canvasTabs, conceptual, diagOnly);
    var canvas = h('section', { class: 'panel canvas' }, canvasHead, metrics, h('div', { class: 'canvas-body' }, diagramBox, timelineBox));
    // "Bạn đang xem gì": câu ngắn mô tả hình (captionKey, nếu không có thì descKey), rồi hình, rồi chú giải hình dạng
    var hasDiagram = disc && (vw.nodes.length || vw.layout === 'lanes');
    var caption = hasDiagram ? h('p', { class: 'diagram-caption' }, h('b', { class: 'caps', text: ADE.t('app.whatYouSee') }), ' ', h('span', { html: ADE.tm(vw.captionKey || vw.descKey) })) : null;
    if (caption) diagramBox.appendChild(caption);
    var scene = hasDiagram ? ADE.diagram.scene(diagramBox, vw) : null;
    if (scene && vw.nodeAction) scene.onNode = function (id) { S.act(vw.nodeAction, id); };
    var shapeLegend = hasDiagram ? h('div', { class: 'shape-legend', role: 'list', 'aria-label': ADE.t('app.shapeLegend') }) : null;
    if (shapeLegend) diagramBox.appendChild(shapeLegend);
    if (!disc) diagramBox.appendChild(h('div', { class: 'pad muted', text: ADE.t('app.noDiagram') }));

    /* -- panel phải -- */
    var sideTabs = h('div', { class: 'tabs-slot' });
    var sideBody = h('div', { class: 'side-body' });
    var side = h('aside', { class: 'panel side' }, h('header', { class: 'panel-h' }, h('h2', { class: 'caps', text: ADE.t('app.currentStep') }), sideTabs), sideBody);

    /* -- nhật ký -- */
    var legend = h('div', { class: 'legend', role: 'list', 'aria-label': ADE.t('app.legend') });
    (track ? track.logKinds : []).forEach(function (k) { var li = h('span', { role: 'listitem' }, ui.kindChip(opts.trackId, k)); legend.appendChild(li); });
    var ctlSlot = h('div', { class: 'ctl-slot' });
    var logWrap = h('div', { class: 'log-scroll' });
    var logHead = h('header', { class: 'panel-h log-h' }, h('h2', { class: 'caps', text: ADE.t('app.eventLog') }), legend, ctlSlot);
    var log = h('section', { class: 'panel log' }, logHead, logWrap);

    var bar = ADE.controls.bar(S, opts);
    var mtabs = h('div', { class: 'mtabs' });

    root.appendChild(h('div', { class: 'stage-top' }, sandbox, mtabs));
    root.appendChild(h('div', { class: 'stage-main' }, canvas, side));
    root.appendChild(log);
    // điều khiển: trong header bảng (desktop), dính đáy (mobile)
    var mq = window.matchMedia('(max-width: 767px)');
    var place = function () { if (mq.matches) root.appendChild(bar.el); else ctlSlot.appendChild(bar.el); };
    place(); var mqh = function () { place(); }; if (mq.addEventListener) mq.addEventListener('change', mqh); else mq.addListener(mqh);

    /* -- render từng phần -- */
    function renderMobileTabs() {
      ui.clear(mtabs);
      mtabs.appendChild(ui.tabs([{ id: 'diagram', label: ADE.t('app.canvas') }, { id: 'side', label: ADE.t('app.currentStep') }, { id: 'log', label: ADE.t('app.eventLog') }], vs.mtab, function (id) { vs.mtab = id; root.setAttribute('data-mtab', id); renderMobileTabs(); }, ADE.t('app.panels')));
    }
    function renderSandbox() {
      if (!sandbox) return;
      ui.clear(sandbox);
      sandbox.appendChild(h('header', { class: 'panel-h' }, h('h2', { class: 'caps', text: ADE.t('app.experiment') })));
      var row = h('div', { class: 'sandbox-row' });
      def.controls.forEach(function (c) {
        var id = 'ctl-' + c.id;
        if (c.type === 'toggle') {
          var on = !!c.get(S.state);
          row.appendChild(h('button', { type: 'button', 'data-fk': 'sb-' + c.id, class: 'btn toggle', 'aria-pressed': on ? 'true' : 'false', onclick: function () { S.act(c.action, !on); } },
            ui.icon(on ? 'check' : 'square', { size: 14, sw: 2 }), h('span', { text: ADE.t(c.labelKey) })));
        } else if (c.type === 'select') {
          var sel = h('select', { id: id, 'data-fk': 'sb-' + c.id, class: 'sel', onchange: function () { var raw = sel.value, num = parseFloat(raw); S.act(c.action, String(num) === raw ? num : raw); } });
          c.options.forEach(function (o) { sel.appendChild(h('option', { value: String(o.value), selected: String(c.get(S.state)) === String(o.value) ? true : null, text: ADE.t(o.labelKey, o.params) })); });
          row.appendChild(h('label', { class: 'field', for: id }, h('span', { text: ADE.t(c.labelKey) }), sel));
        } else if (c.type === 'button') {
          row.appendChild(h('button', { type: 'button', 'data-fk': 'sb-' + c.id, class: 'btn', onclick: function () { S.act(c.action, c.payload); } }, ui.icon(c.icon || 'set', { size: 14 }), h('span', { text: ADE.t(c.labelKey) })));
        }
      });
      sandbox.appendChild(row);
      if (def.controlsHintKey) sandbox.appendChild(h('p', { class: 'hint', text: ADE.t(def.controlsHintKey) }));
    }
    function renderCanvasTabs() {
      ui.clear(canvasTabs);
      if (!disc) return;
      canvasTabs.appendChild(ui.tabs([{ id: 'diagram', label: ADE.t('app.diagram'), icon: 'layers' }, { id: 'timeline', label: ADE.t('app.timeline'), icon: 'list' }], vs.canvasTab, function (id) { vs.canvasTab = id; renderCanvasTabs(); applyCanvasTab(); refreshCanvas(); }, ADE.t('app.views')));
    }
    function applyCanvasTab() { diagramBox.hidden = vs.canvasTab !== 'diagram'; timelineBox.hidden = vs.canvasTab !== 'timeline'; }
    var prevVals = null;   // giá trị chỉ số lần vẽ trước: chỉ số nào đổi thì nháy một lần (chuyển cảnh, tắt khi reduced-motion)
    function renderMetrics() {
      ui.clear(metrics);
      var list = vw.metrics || [];
      metrics.hidden = !list.length;
      var vals = disc ? S.metricsAt() : {};
      list.forEach(function (m) {
        var v = vals[m.id], known = v !== undefined && v !== null, changed = prevVals && known && prevVals[m.id] !== v;
        metrics.appendChild(h('div', { class: 'metric' + (known ? '' : ' unknown') + (changed ? ' changed' : '') }, h('span', { class: 'metric-l', text: ADE.t(m.labelKey) }),
          h('b', { class: 'metric-v', 'aria-label': known ? null : ADE.t('app.unknownValue') }, known ? (typeof v === 'number' ? ADE.num(v) : ADE.t(String(v))) : '?')));
      });
      prevVals = vals;
    }
    function refreshCanvas(animate) {
      if (!disc) return;
      var step = S.step();
      var evs = S.eventsUpTo();
      if (scene) scene.render(step, { speed: S.speed, instant: animate === false, prev: S.pos >= 2 ? S.steps[S.pos - 2] : null, events: evs, pos: S.pos, steps: S.steps });
      renderShapeLegend();
      ADE.diagram.timeline(timelineBox, vw, opts.trackId, evs, { speed: S.speed });
    }
    function renderShapeLegend() {
      if (!shapeLegend) return;
      ui.clear(shapeLegend);
      var items = [];
      if (vw.layout === 'lanes') {
        var seen = {}, bars = (scene.lastLanes && scene.lastLanes.allKinds) || [];
        (scene.lastLanes && scene.lastLanes.bars || []).forEach(function (b) { seen[b.kind] = 1; });
        bars.forEach(function (k) { seen[k] = 1; });
        ['run', 'block', 'wait', 'ready'].forEach(function (k) { if (seen[k]) items.push([ADE.diagram.barSvg(k), ADE.t((vw.barKeys && vw.barKeys[k]) || 'app.bar.' + k)]); });
        if (scene.lastLanes && scene.lastLanes.marks && scene.lastLanes.marks.length) items.push(['<svg viewBox="0 0 14 14" width="14" height="14" aria-hidden="true"><path d="M7 1l5 6-5 6-5-6z" class="lane-mark-g"/></svg>', ADE.t((vw.barKeys && vw.barKeys.mark) || 'app.bar.mark')]);
      } else {
        ADE.diagram.familiesIn(S.steps, vw).forEach(function (f) { items.push([ADE.diagram.glyphSvg(f), ADE.t((vw.famKeys && vw.famKeys[f]) || 'app.fam.' + f)]); });
      }
      shapeLegend.hidden = !items.length;
      items.forEach(function (it) { shapeLegend.appendChild(h('span', { role: 'listitem', class: 'shape-li' }, h('span', { class: 'shape-g', html: it[0] }), h('span', { text: it[1] }))); });
    }
    function titleOf(step) { return ADE.t(step.titleKey, step.params); }
    function snippetFor(step) {
      var hl = step && step.codeHighlight, id = hl ? hl.snippet : def.codeId;
      return id ? { sn: ADE.getCode(opts.trackId, id), lines: hl ? hl.lines || [] : [] } : null;
    }
    function codeView(step) {
      var info = snippetFor(step);
      if (!info || !info.sn) return h('p', { class: 'muted pad', text: ADE.t('app.noCode') });
      return ui.codeBlock(info.sn, info.lines);
    }
    function nameOfPos(p) { return p === 0 ? ADE.t('app.overview') : (p > S.N ? ADE.t('app.wrapup') : titleOf(S.steps[p - 1])); }
    function renderSide() {
      ui.clear(sideBody); ui.clear(sideTabs);
      if (!disc) { sideBody.appendChild(h('p', { class: 'muted pad', text: ADE.t('app.noDiagram') })); return; }
      var step = S.step();
      sideTabs.appendChild(ui.tabs([{ id: 'explain', label: ADE.t('app.explain') }, { id: 'code', label: ADE.t('app.code') }], vs.sideTab, function (id) { vs.sideTab = id; renderSide(); }, ADE.t('app.sideTabs')));
      if (vs.sideTab === 'code') { sideBody.appendChild(codeView(step)); sideBody.appendChild(simplifies(step)); return; }
      if (S.pos === 0) sideBody.appendChild(overview());
      else if (S.pos > S.N) sideBody.appendChild(wrapup());
      else sideBody.appendChild(stepView(step));
      sideBody.appendChild(simplifies(step));
    }
    function goalsBlock() {
      var gs = opts.goals ? opts.goals() : [];
      if (!gs.length) return null;
      var ul = h('ul', { class: 'goals' });
      gs.forEach(function (g) { ul.appendChild(h('li', { class: g.done ? 'done' : '' }, ui.icon(g.done ? 'check' : 'square', { size: 14, sw: 2 }), h('span', { class: 'sr-only', text: g.done ? ADE.t('app.done') + ': ' : ADE.t('app.notYet') + ': ' }), h('span', { html: ADE.markup(g.text) }))); });
      return h('div', { class: 'goals-box' }, h('h3', { class: 'caps', text: ADE.t('app.goals') }), ul);
    }
    function overview() {
      var d = h('div', { class: 'ctx ctx-overview' });
      d.appendChild(h('h3', { class: 'step-title', text: ADE.t(def.titleKey) }));
      if (def.overviewKey) d.appendChild(h('p', { class: 'prose', html: ADE.tm(def.overviewKey) }));
      var ol = h('ol', { class: 'steplist' });
      S.steps.forEach(function (st, i) { ol.appendChild(h('li', null, h('button', { type: 'button', 'data-fk': 'step-' + i, class: 'steplink', onclick: function () { S.goto(i + 1); } }, h('span', { class: 'n', text: String(i + 1) }), h('span', { text: titleOf(st) })))); });
      d.appendChild(h('h3', { class: 'caps sub', text: ADE.t('app.stepList') })); d.appendChild(ol);
      var g = goalsBlock(); if (g) d.appendChild(g);
      d.appendChild(h('button', { type: 'button', 'data-fk': 'start', class: 'btn primary', onclick: function () { S.next(); } }, ui.icon('play', { size: 14 }), h('span', { text: ADE.t('app.start') })));
      return d;
    }
    function listOf(cls, titleKey, items, mk) {
      if (!items || !items.length) return null;
      var ul = h('ul', { class: cls });
      items.forEach(function (it) { ul.appendChild(mk(it)); });
      return h('div', { class: 'ctx-block' }, h('h3', { class: 'caps sub', text: ADE.t(titleKey) }), ul);
    }
    function stateList(arr) {
      return h('ul', { class: 'kv' }, (arr || []).map(function (s) { return h('li', null, h('span', { class: 'k', text: ADE.t(s.labelKey) }), h('span', { class: 'v', text: s.valueKey ? ADE.t(s.valueKey) : (typeof s.value === 'number' ? ADE.num(s.value) : String(s.value)) })); }));
    }
    var OPG = { add: 'add', set: 'set', remove: 'remove', skip: 'skip' };
    function stepView(step) {
      var d = h('div', { class: 'ctx ctx-step' });
      d.appendChild(h('div', { class: 'step-meta' }, h('span', { class: 'step-n', text: ADE.t('app.stepNofM', { n: S.pos, total: S.N }) }), ui.stepBadge(step.type || 'mechanism')));
      d.appendChild(h('h3', { class: 'step-title', text: titleOf(step) }));
      d.appendChild(h('p', { class: 'prose', html: ADE.tm(step.explainKey, step.params) }));
      (step.callouts || []).forEach(function (c) { d.appendChild(ui.callout(c.kind, ADE.tm(c.textKey, c.params))); });
      if ((step.stateBefore && step.stateBefore.length) || (step.stateAfter && step.stateAfter.length)) {
        d.appendChild(h('div', { class: 'ctx-block ba' }, h('h3', { class: 'caps sub', text: ADE.t('app.state') }),
          h('div', { class: 'ba-cols' }, h('div', null, h('h4', { text: ADE.t('app.before') }), stateList(step.stateBefore)), h('div', null, h('h4', { text: ADE.t('app.after') }), stateList(step.stateAfter)))));
      }
      var ch = listOf('changes', 'app.changed', step.changes, function (c) {
        return h('li', { class: 'op-' + c.op }, h('span', { class: 'op', title: ADE.t('app.op.' + c.op) }, ui.icon(OPG[c.op] || 'set', { size: 14, sw: 2.2 }), h('span', { class: 'sr-only', text: ADE.t('app.op.' + c.op) + ': ' })), h('span', { html: ADE.tm(c.textKey, c.params) }));
      });
      if (ch) d.appendChild(ch);
      var sk = listOf('skipped', 'app.skipped', step.skipped, function (s) { return h('li', null, h('span', { class: 'op' }, ui.icon('skip', { size: 14, sw: 2 })), h('span', null, h('b', { text: ADE.t(s.whatKey) }), ' — ', h('span', { text: ADE.t(s.whyKey) }))); });
      if (sk) d.appendChild(sk);
      if (step.affected && step.affected.length) {
        var chips = h('div', { class: 'chips' });
        step.affected.forEach(function (id) { var nd = vw.nodes.filter(function (n) { return n.id === id; })[0]; chips.appendChild(h('span', { class: 'chip', text: nd ? ADE.t(nd.labelKey) : id })); });
        d.appendChild(h('div', { class: 'ctx-block' }, h('h3', { class: 'caps sub', text: ADE.t('app.affected') }), chips));
      }
      var nav = h('div', { class: 'step-nav' },
        h('button', { type: 'button', 'data-fk': 'nav-prev', class: 'btn', onclick: function () { S.prev(); } }, ui.icon('prev', { size: 14 }), h('span', null, h('small', { text: ADE.t('app.prev') }), h('span', { class: 'nav-t', text: nameOfPos(S.pos - 1) }))),
        h('button', { type: 'button', 'data-fk': 'nav-next', class: 'btn primary', onclick: function () { S.next(); } }, h('span', null, h('small', { text: ADE.t('app.nextLabel') }), h('span', { class: 'nav-t', text: nameOfPos(S.pos + 1) })), ui.icon('next', { size: 14 })));
      d.appendChild(nav);
      return d;
    }
    function wrapup() {
      var d = h('div', { class: 'ctx ctx-wrapup' });
      d.appendChild(h('div', { class: 'step-meta' }, ui.stepBadge('wrapup'), h('span', { class: 'done-mark' }, ui.icon('check', { size: 14, sw: 2.4 }), h('span', { text: ADE.t('app.completed') }))));
      d.appendChild(h('h3', { class: 'step-title', text: ADE.t('app.wrapup') }));
      if (def.wrapupKey) d.appendChild(h('p', { class: 'prose', html: ADE.tm(def.wrapupKey) }));
      var counts = {}, total = 0;
      S.eventsUpTo(S.N).forEach(function (x) { counts[x.e.kind] = (counts[x.e.kind] || 0) + 1; total++; });
      var ul = h('ul', { class: 'kv' });
      Object.keys(counts).forEach(function (k) { ul.appendChild(h('li', null, h('span', { class: 'k' }, ui.kindChip(opts.trackId, k)), h('span', { class: 'v', text: ADE.num(counts[k]) }))); });
      d.appendChild(h('div', { class: 'ctx-block' }, h('h3', { class: 'caps sub', text: ADE.t('app.totals', { n: total }) }), ul));
      var g = goalsBlock(); if (g) d.appendChild(g);
      var acts = h('div', { class: 'row-actions' }, h('button', { type: 'button', 'data-fk': 'replay', class: 'btn', onclick: function () { S.goto(0); S.play(); } }, ui.icon('replay', { size: 14 }), h('span', { text: ADE.t('app.replay') })));
      if (opts.onQuiz) acts.appendChild(h('button', { type: 'button', 'data-fk': 'quiz', class: 'btn primary', onclick: opts.onQuiz }, ui.icon('check', { size: 14 }), h('span', { text: ADE.t('app.selfCheck') })));
      d.appendChild(acts);
      return d;
    }
    function simplifies(step) {
      var keys = (def.simplificationKeys || []).concat((step && step.simplificationKeys) || []);
      var seen = {}; keys = keys.filter(function (k) { if (seen[k]) return false; seen[k] = 1; return true; });
      var ul = h('ul', { class: 'simp' }); keys.forEach(function (k) { ul.appendChild(h('li', { html: ADE.tm(k) })); });
      var det = h('details', { class: 'simplifies' }, h('summary', { 'data-fk': 'simp' }, ui.icon('info', { size: 14 }), h('span', { class: 'caps', text: ADE.t('app.simplifies') })), ul.children.length ? ul : h('p', { class: 'muted', text: ADE.t('app.noSimplifies') }));
      if (vs.simpOpen) det.setAttribute('open', '');
      det.addEventListener('toggle', function () { vs.simpOpen = det.open; });
      return det;
    }
    function renderLog() {
      ui.clear(logWrap);
      if (!disc) return;
      var evs = S.eventsUpTo();
      var table = h('table', { class: 'evt' });
      var cols = [['#', 'app.col.n'], ['t', 'app.col.t'], ['subject', vw.subjectKey || 'app.col.subject']];
      if (vw.scopeKey) cols.push(['scope', vw.scopeKey]);
      cols.push(['kind', 'app.col.kind'], ['detail', 'app.col.detail']);
      table.appendChild(h('caption', { class: 'sr-only', text: ADE.t('app.eventLog') }));
      table.appendChild(h('thead', null, h('tr', null, cols.map(function (c) { return h('th', { scope: 'col', class: 'c-' + c[0], text: ADE.t(c[1]) }); }))));
      var tb = h('tbody');
      if (!evs.length) tb.appendChild(h('tr', { class: 'empty' }, h('td', { colspan: String(cols.length), text: ADE.t('app.logEmpty') })));
      var activeRow = null;
      evs.forEach(function (x, i) {
        var e = x.e, nd = vw.nodes.filter(function (n) { return n.id === e.subject; })[0];
        var cur = x.step === S.pos;
        var tr = h('tr', { class: 'ev' + (cur ? ' current' : '') + (cur && freshRows ? ' fresh' : ''), 'aria-current': cur ? 'step' : null, onclick: function () { S.goto(x.step); } });
        var tds = {
          '#': h('td', { class: 'c-#', 'data-label': ADE.t('app.col.n') }, h('button', { type: 'button', 'data-fk': 'row-' + i, class: 'rowbtn', 'aria-label': ADE.t('app.gotoStep', { n: x.step }), onclick: function (ev) { ev.stopPropagation(); S.goto(x.step); } }, (cur ? '▶ ' : '') + ADE.num(i + 1))),
          t: h('td', { class: 'c-t', 'data-label': ADE.t('app.col.t'), text: e.t === undefined ? '—' : ADE.num(e.t) }),
          subject: h('td', { class: 'c-subject', 'data-label': ADE.t(vw.subjectKey || 'app.col.subject'), text: nd ? ADE.t(nd.labelKey) : e.subject }),
          scope: h('td', { class: 'c-scope', 'data-label': vw.scopeKey ? ADE.t(vw.scopeKey) : '', text: e.scope ? (ADE.hasKey(e.scope) ? ADE.t(e.scope) : e.scope) : '—' }),
          kind: h('td', { class: 'c-kind', 'data-label': ADE.t('app.col.kind') }, ui.kindChip(opts.trackId, e.kind)),
          detail: h('td', { class: 'c-detail', 'data-label': ADE.t('app.col.detail'), text: ADE.t(e.detailKey, e.params) })
        };
        cols.forEach(function (c) { tr.appendChild(tds[c[0]]); });
        tb.appendChild(tr);
        if (cur) activeRow = tr;
      });
      table.appendChild(tb); logWrap.appendChild(table);
      if (activeRow && logWrap.scrollHeight > logWrap.clientHeight) logWrap.scrollTop = Math.max(0, activeRow.offsetTop - logWrap.clientHeight + activeRow.offsetHeight + 8);
    }
    function all(animate) {
      ui.withFocus(function () {
        renderMobileTabs(); renderSandbox(); renderCanvasTabs(); applyCanvasTab(); renderMetrics(); refreshCanvas(animate); renderSide(); renderLog(); bar.update();
        ADE.markMissing(root);
      });
    }
    all(false);

    var lastPos = S.pos, freshRows = false;
    offs.push(S.on(function (e) {
      if (e.type === 'play' || e.type === 'pause' || e.type === 'speed') { bar.update(); return; }
      if (e.type === 'replay') { refreshCanvas(true); return; }
      if (e.type === 'frame') { bar.update(); return; }
      // chuyển cảnh theo hướng: tới → panel trượt từ phải, lùi → từ trái (CSS; reduced-motion tắt hết)
      var dir = disc && S.pos !== lastPos ? (S.pos > lastPos ? 'fwd' : 'back') : '';
      sideBody.setAttribute('data-dir', dir); freshRows = !!dir;
      ui.withFocus(function () {
        renderMetrics(); renderSide(); renderLog(); refreshCanvas(); bar.update();
        if (e.type === 'act' || e.type === 'reset') renderSandbox();
        ADE.markMissing(root);
      });
      if (disc && S.pos !== lastPos) {
        lastPos = S.pos;
        var step = S.step();
        ADE.ui.announce(step ? ADE.t('a11y.stepOf', { n: S.pos, total: S.N, title: titleOf(step) }) : (S.pos === 0 ? ADE.t('app.overview') : ADE.t('app.wrapup')));
        if (opts.onPos) opts.onPos(S.pos);
      }
    }));
    ADE.controls.keys(root, S);

    return {
      root: root,
      refresh: function () { all(false); },
      destroy: function () { offs.forEach(function (f) { f(); }); if (scene) scene.destroy(); if (mq.removeEventListener) mq.removeEventListener('change', mqh); else mq.removeListener(mqh); if (root.parentNode) root.parentNode.removeChild(root); }
    };
  };

  /* ---------- chuyển động cho lab tự vẽ (model kind 'compute') ----------
     Lab vẽ lại DOM của chính nó (thường bằng innerHTML) khi người dùng thao tác. Lõi không biết lab vẽ gì, nên so CẤU TRÚC:
     chụp cây trước (đường dẫn tag+thứ tự), lab vẽ lại, MutationObserver báo (trước khi trình duyệt vẽ), rồi so:
       · chữ là số đổi → số chạy dần từ cũ tới mới; chữ khác đổi → nháy một lần;
       · thuộc tính hình học SVG đổi (x, y, width, height, cx, cy, r, x1…y2, points, d cùng cấu trúc) → nội suy;
       · phần tử mới → hiện dần; những gì vừa đổi giữ lớp .mo-live (chuyển động liên tục) tới lần đổi sau.
     Lab tự chạy theo khung hình (đổi DOM liên tục < 150 ms) thì bỏ qua: chính nó đã là chuyển động.
     Tắt hết khi giảm chuyển động hoặc "Chỉ sơ đồ". Không đổi nội dung: trạng thái cuối luôn là DOM lab đã vẽ. */
  var GEO = ['x', 'y', 'width', 'height', 'cx', 'cy', 'r', 'rx', 'ry', 'x1', 'y1', 'x2', 'y2', 'points', 'd'];
  var SKIP = { OPTION: 1, SCRIPT: 1, STYLE: 1, TEXTAREA: 1, INPUT: 1, SELECT: 1 };
  var NUM_RE = /-?\d[\d.,\u00a0\u202f]*\d|-?\d/g;
  function seps() {
    var s = ADE.num ? ADE.num(12345.6, { minimumFractionDigits: 1, maximumFractionDigits: 1 }) : '12,345.6';
    return { dec: s.charAt(s.length - 2), grp: s.replace(/\d/g, '').charAt(0) === s.charAt(s.length - 2) ? '' : s.replace(/\d/g, '').charAt(0) };
  }
  function parseTok(t, sp) {
    var dec = 0, s = t.replace(/[\u00a0\u202f\s]/g, '');
    var i = sp.dec ? s.lastIndexOf(sp.dec) : -1;
    if (i >= 0 && sp.grp !== sp.dec) { dec = s.length - i - 1; s = s.slice(0, i).split(sp.grp).join('') + '.' + s.slice(i + 1); }
    else if (sp.grp) s = s.split(sp.grp).join('');
    var v = parseFloat(s);
    return isNaN(v) ? null : { v: v, dec: dec, grp: sp.grp && t.indexOf(sp.grp) >= 0 };
  }
  function fmtTok(v, ref) {
    return ADE.num ? ADE.num(v, { minimumFractionDigits: ref.dec, maximumFractionDigits: ref.dec, useGrouping: !!ref.grp }) : v.toFixed(ref.dec);
  }
  function geoNums(s) { return String(s).match(/-?\d*\.?\d+(e-?\d+)?/gi) || []; }
  function geoSkel(s) { return String(s).replace(/-?\d*\.?\d+(e-?\d+)?/gi, '#'); }

  ui.labMotion = function (root) {
    if (!root || typeof MutationObserver === 'undefined') return { destroy: function () { } };
    var off = function () { return ADE.motionReduced() || ADE.diagramOnly(); };
    var last = null, lastMut = 0, settle = null, mo = null, dead = false, gen = 0;
    function take() {
      var m = {};
      (function walk(el, key) {
        var seen = {}, kids = el.children;
        for (var i = 0; i < kids.length; i++) {
          var c = kids[i], t = c.tagName; seen[t] = (seen[t] || 0) + 1;
          var k = key + '/' + t + seen[t], info = { el: c, tag: t };
          if (!c.children.length && !SKIP[t]) info.txt = c.textContent;
          if (c instanceof SVGElement) { info.g = {}; GEO.forEach(function (a) { var v = c.getAttribute(a); if (v != null) info.g[a] = v; }); }
          m[k] = info;
          if (!SKIP[t]) walk(c, k);
        }
      })(root, '');
      return m;
    }
    function tween(ms, step, done) {
      var t0 = performance.now(), g = gen;
      (function fr(now) {
        if (dead || g !== gen) return;
        var p = Math.min(1, (now - t0) / ms), e = 1 - Math.pow(1 - p, 3);
        step(e); if (mo) mo.takeRecords();
        if (p < 1) requestAnimationFrame(fr); else if (done) done();
      })(t0);
    }
    function morph(old) {
      var now = take(), sp = seps(), live = [], flash = [], fresh = [];
      root.querySelectorAll('.mo-live').forEach(function (x) { x.classList.remove('mo-live'); });
      Object.keys(now).forEach(function (k) {
        var n = now[k], o = old[k];
        if (!o || o.tag !== n.tag) {
          var pk = k.slice(0, k.lastIndexOf('/'));
          if (!pk || (old[pk] && old[pk].tag === (now[pk] || {}).tag)) fresh.push(n.el);
          return;
        }
        if (n.txt != null && o.txt != null && n.txt !== o.txt) {
          var a = o.txt.match(NUM_RE) || [], b = n.txt.match(NUM_RE) || [];
          if (b.length && a.length === b.length && o.txt.replace(NUM_RE, '#') === n.txt.replace(NUM_RE, '#')) {
            var from = a.map(function (t) { return parseTok(t, sp); }), to = b.map(function (t) { return parseTok(t, sp); });
            var norm = function (x) { return x.replace(/[  \s]/g, ' '); };
            var exact = function (arr, toks) { return arr.every(function (t, i) { return t && norm(fmtTok(t.v, t)) === norm(toks[i]); }); };
            if (exact(from, a) && exact(to, b)) {
              var parts = n.txt.split(NUM_RE), el = n.el, fin = n.txt;
              tween(520, function (e) {
                var s = parts[0];
                for (var i = 0; i < to.length; i++) s += fmtTok(from[i].v + (to[i].v - from[i].v) * e, to[i]) + parts[i + 1];
                el.textContent = e >= 1 ? fin : s;
              });
            }
          }
          flash.push(n.el); live.push(n.el);
        }
        if (n.g && o.g) {
          var ch = GEO.filter(function (a) { return n.g[a] != null && o.g[a] != null && n.g[a] !== o.g[a] && geoSkel(n.g[a]) === geoSkel(o.g[a]); });
          if (ch.length) {
            var el2 = n.el, fromG = {}, toG = {};
            ch.forEach(function (a) { fromG[a] = geoNums(o.g[a]).map(Number); toG[a] = geoNums(n.g[a]).map(Number); });
            tween(460, function (e) {
              ch.forEach(function (a) {
                if (e >= 1) { el2.setAttribute(a, n.g[a]); return; }
                var i = 0, f = fromG[a], t = toG[a];
                el2.setAttribute(a, geoSkel(n.g[a]).replace(/#/g, function () { var v = f[i] + (t[i] - f[i]) * e; i++; return String(Math.round(v * 100) / 100); }));
              });
            });
            live.push(n.el);
          }
        }
      });
      fresh.slice(0, 60).forEach(function (el) {
        if (el instanceof SVGElement) el.animate([{ opacity: 0 }, { opacity: 1 }], { duration: 320, easing: 'ease-out' });
        else el.animate([{ opacity: 0, transform: 'translateY(6px)' }, { opacity: 1, transform: 'none' }], { duration: 280, easing: 'cubic-bezier(.2,.7,.2,1)' });
      });
      flash.slice(0, 40).forEach(function (el) { if (!(el instanceof SVGElement)) { el.classList.remove('mo-chg'); void el.offsetWidth; el.classList.add('mo-chg'); } });
      live.slice(0, 14).forEach(function (el) { el.classList.add('mo-live'); });
      return now;
    }
    function onMut() {
      if (dead) return;
      var t = performance.now(), streaming = t - lastMut < 150;
      lastMut = t;
      clearTimeout(settle);
      if (streaming) gen++;
      if (!last || streaming || off()) { settle = setTimeout(function () { if (!dead) last = take(); }, 160); return; }
      last = morph(last);
      if (mo) mo.takeRecords();
    }
    mo = new MutationObserver(onMut);
    mo.observe(root, { childList: true, subtree: true, characterData: true });
    setTimeout(function () { if (!dead) last = take(); }, 0);
    return { destroy: function () { dead = true; clearTimeout(settle); if (mo) mo.disconnect(); mo = null; } };
  };
})();
