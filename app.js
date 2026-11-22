/* app.js — khởi động, giao diện chung (header, toolbar, drawer, rail), các trang và tiến độ.
   KHÔNG chứa id track nào: catalog, nav, tìm kiếm, Live Explorer, glossary, hiểu lầm, nguồn, lộ trình đều sinh từ registry. */
(function () {
  'use strict';
  var ADE = window.ADE;
  var ui = ADE.ui, h = ui.h, icon = ui.icon;
  var app = ADE.app = {};
  var main, rail, railBtn, header, toolbar, drawer, backdrop, drawerBtn, shell;
  var cur = { pageKey: '', lang: '', sessions: {}, viewStates: {}, mounts: [] };
  var drawerDomain = 'all', filters = { domain: 'all', level: 'all', status: 'all' };
  var progress = ADE.store.get('progress', {});

  /* ================= tuỳ chọn giao diện ================= */
  var root = document.documentElement;
  function applyTheme(t) { root.setAttribute('data-theme', t); }
  function currentTheme() { return root.getAttribute('data-theme') === 'dark' ? 'dark' : 'light'; }
  function initPrefs() {
    var th = ADE.store.get('theme', null);
    if (th !== 'light' && th !== 'dark') th = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
    applyTheme(th);
    applyMotion();
    root.classList.toggle('dev', !!ADE.dev);
    root.classList.toggle('sans-prose', ADE.store.get('sans', true) !== false);
    root.classList.toggle('diagram-only', !!ADE.store.get('diagramOnly', false));
    root.classList.toggle('rail-collapsed', !!ADE.store.get('rail', false));
    if (window.matchMedia) {
      var mq = window.matchMedia('(prefers-reduced-motion: reduce)');
      var f = function () { if (!ADE.store.get('motion', null)) { applyMotion(); rerender(); } };
      if (mq.addEventListener) mq.addEventListener('change', f);
    }
  }
  function applyMotion() {
    var pref = ADE.store.get('motion', null);
    var os = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    var reduced = pref === 'reduce' || (pref !== 'full' && os);
    root.classList.toggle('reduced-motion', reduced);
    root.classList.toggle('motion-full', pref === 'full');
  }

  /* ================= tiến độ ================= */
  function pkey(t, c) { return t + '/' + c; }
  function getProg(t, c) { return progress[pkey(t, c)] || { max: 0, done: false, quiz: {} }; }
  function saveProg(t, c, pos, N) {
    var p = progress[pkey(t, c)] = getProg(t, c);
    if (pos > p.max) p.max = pos;
    if (N != null && pos > N) p.done = true;
    ADE.store.set('progress', progress);
  }
  function trackProgress(t) {
    var done = 0; t.chapters.forEach(function (c) { if (getProg(t.id, c.id).done) done++; });
    return { done: done, total: t.chapters.length };
  }

  /* ================= tiện ích ================= */
  function href(p) { return '#/' + ADE.lang + '/' + (p || ''); }
  function setTitle(s) { document.title = ADE.stripSentinel((s ? s + ' · ' : '') + ADE.t('app.name')); }
  function para(str, cls) { return h('p', { class: cls || 'prose', html: ADE.markup(str) }); }
  /* chuyển cảnh: mục nội dung hiện dần (trượt lên + rõ dần) khi cuộn tới. Chỉ bật khi không giảm chuyển động;
     không có IntersectionObserver hoặc reduced-motion thì mọi thứ hiện ngay. */
  function reveal(scope) {
    if (ADE.motionReduced() || !window.IntersectionObserver) return;
    var items = [].slice.call(scope.querySelectorAll('.panel.sec, .panel.quiz, .bridges, .ch-nav'));
    if (!items.length) return;
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); } });
    }, { rootMargin: '0px 0px -8% 0px' });
    items.forEach(function (el) { el.classList.add('rv'); io.observe(el); });
    window.addEventListener('beforeprint', function () { items.forEach(function (el) { el.classList.add('in'); }); }, { once: true });
  }
  function lines(key, cls) { return ADE.t(key).split('\n').map(function (l) { return para(l, cls); }); }
  /* khối nội dung v2 trong một mục: key `<mục>.b.<n>.<trường>`; trường quyết định loại khối (docs/core-api.md §2.1) */
  function block(k) {
    var has = function (f) { return ADE.hasKey(k + '.' + f); }, tx = function (f) { return ADE.t(k + '.' + f); };
    var paras = function (f) { return tx(f).split('\n').map(function (l) { return para(l); }); };
    var codeEl = function (f, lang) { return ui.codeBlock({ lang: lang, lines: tx(f).split('\n') }, []); };
    var reveal = function (cls, label, q, inner, open) {
      return h('details', { class: 'blk ' + cls }, h('summary', null, h('span', { class: 'blk-l caps', text: ADE.t(label) }), q ? h('span', { html: ADE.markup(q) }) : null), h('div', { class: 'blk-a' }, inner));
    };
    if (has('h')) return h('h3', { class: 'blk-h', text: tx('h') });
    if (has('kt')) return codeEl('kt', has('lang') ? tx('lang') : 'kotlin');
    if (has('out')) return h('div', { class: 'blk-out' }, codeEl('out', ADE.t('app.blk.output')));
    if (has('note')) return ui.callout(has('kind') ? tx('kind') : 'mechanism', ADE.markup(tx('note')).split('\n').join('<br>'));
    if (has('predict')) return reveal('predict', 'app.blk.predict', tx('predict'), paras('ans'));
    if (has('ask')) return reveal('recall', 'app.blk.recall', tx('ask'), paras('ans'));
    if (has('bug')) {
      return h('div', { class: 'blk bug' }, h('p', { class: 'prose' }, h('span', { class: 'blk-l caps', text: ADE.t('app.blk.bug') }), h('span', { html: ADE.markup(tx('bug')) })),
        reveal('bug-why', 'app.blk.cause', null, [h('p', { class: 'prose', html: ADE.markup(tx('cause')) }), h('p', { class: 'prose' }, h('b', { text: ADE.t('app.blk.fix') + ': ' }), h('span', { html: ADE.markup(tx('fix')) }))].concat(has('fixkt') ? [codeEl('fixkt', 'kotlin')] : [])));
    }
    if (has('ex')) {
      var box = h('div', { class: 'blk ex' }, h('p', { class: 'prose' }, h('span', { class: 'blk-l caps', text: ADE.t('app.blk.exercise') }), h('span', { html: ADE.markup(tx('ex')) })));
      if (has('exkt')) box.appendChild(codeEl('exkt', 'kotlin'));
      if (has('hint')) box.appendChild(reveal('hint', 'app.blk.hint', null, paras('hint')));
      box.appendChild(reveal('sol', 'app.blk.solution', null, paras('sol').concat(has('solkt') ? [codeEl('solkt', 'kotlin')] : [])));
      return box;
    }
    if (has('p')) return h('div', null, paras('p'));
    return null;
  }
  function levelChip(t) { return h('span', { class: 'chip' }, icon('chevr', { size: 12 }), h('span', { text: ADE.t('app.level.' + t.level) })); }
  function trackIcon(t) { return ADE.diagram.ICONS[t.icon] ? t.icon : 'chip'; }
  function metaChips(t) {
    return h('div', { class: 'chips' }, levelChip(t), h('span', { class: 'chip' }, icon('clock', { size: 12 }), h('span', { text: ADE.t('app.minutes', { n: t.estMinutes }) })),
      h('span', { class: 'chip status-' + t.status, text: ADE.t('app.status.' + t.status) }), h('span', { class: 'chip', text: ADE.t('app.chapterCount', { n: t.chapters.length }) }));
  }
  function empty(msgKey) { return h('div', { class: 'panel pad empty-state' }, h('p', { class: 'prose', text: ADE.t(msgKey) })); }
  function stdPage(titleText, children) {
    return h('article', { class: 'page' }, h('header', { class: 'page-h' }, h('h1', { class: ui.caps(titleText), text: titleText })), children);
  }
  function scrollToId(id) {
    if (!id) return;
    setTimeout(function () {
      var el = document.getElementById(id);
      if (el) { el.scrollIntoView({ block: 'start' }); el.classList.add('flash'); setTimeout(function () { el.classList.remove('flash'); }, 2600); }
    }, 30);
  }

  /* ================= chrome ================= */
  function buildChrome() {
    var app0 = document.getElementById('app');
    ui.clear(app0);
    app0.appendChild(h('a', { class: 'skip', href: '#main', onclick: function (e) { e.preventDefault(); main.focus(); }, text: ADE.t('app.skip') }));
    header = h('header', { class: 'topbar' });
    toolbar = h('div', { class: 'toolbar' });
    rail = h('nav', { class: 'rail', 'aria-label': ADE.t('app.chapters') });
    main = h('main', { id: 'main', class: 'main', tabindex: '-1' });
    shell = h('div', { class: 'shell' }, rail, main);
    var footer = h('footer', { class: 'foot' });
    backdrop = h('div', { class: 'backdrop', hidden: true, onclick: function () { toggleDrawer(false); } });
    drawer = h('aside', { class: 'drawer', id: 'drawer', hidden: true, 'aria-label': ADE.t('app.catalog') });
    app0.appendChild(header); app0.appendChild(toolbar); app0.appendChild(shell); app0.appendChild(footer);
    app0.appendChild(backdrop); app0.appendChild(drawer);
    app0.appendChild(h('div', { id: 'ade-live', class: 'sr-only', 'aria-live': 'polite', role: 'status' }));
    renderChrome();
  }
  function renderChrome() { ui.withFocus(renderChromeInner); }
  function renderChromeInner() {
    var r = ADE.router.parse(), trk = r.page === 'track' ? ADE.getTrack(r.track) : null;
    ui.clear(header);
    drawerBtn = h('button', { type: 'button', 'data-fk': 'drawer-btn', class: 'btn icon', 'aria-label': ADE.t('app.catalog'), 'aria-expanded': 'false', 'aria-controls': 'drawer', onclick: function () { toggleDrawer(drawer.hidden); } }, icon('menu', { size: 20 }));
    var brand = h('a', { class: 'brand', href: href(''), 'aria-label': ADE.t('app.name') + ' — ' + ADE.t('app.home') }, h('span', { class: 'logo-wrap', html: ADE.diagram.logo(36) }), h('span', { class: 'brand-t' }, h('span', { class: 'wordmark', text: ADE.t('app.name') }), h('span', { class: 'tagline', text: ADE.t('app.tagline') })));
    var ctx = h('div', { class: 'ctx-now', 'aria-live': 'off' });
    if (trk) {
      var tp = trackProgress(trk);
      ctx.appendChild(h('span', { class: 'ctx-track' }, h('i', { class: 'accent-dot', style: 'background:' + trk.accent, 'aria-hidden': 'true' }), h('span', { text: ADE.t(trk.titleKey) })));
      ctx.appendChild(h('span', { class: 'ctx-prog', title: ADE.t('app.progress') }, h('progress', { max: String(tp.total), value: String(tp.done), 'aria-label': ADE.t('app.progress') }), h('span', { text: tp.done + '/' + tp.total })));
    }
    var langSeg = h('div', { class: 'seg', role: 'group', 'aria-label': ADE.t('app.language') });
    ADE.langs.forEach(function (l) {
      langSeg.appendChild(h('button', { type: 'button', 'data-fk': 'lang-' + l, class: 'seg-b' + (l === ADE.lang ? ' on' : ''), 'aria-pressed': l === ADE.lang ? 'true' : 'false', lang: l, title: ADE.t('app.langName.' + l), 'aria-label': ADE.t('app.langName.' + l), onclick: function () { switchLang(l); }, text: l.toUpperCase() }));
    });
    var th = currentTheme();
    var bTheme = h('button', { type: 'button', 'data-fk': 'theme', class: 'btn icon', 'aria-label': ADE.t('app.theme'), title: ADE.t(th === 'dark' ? 'app.themeToLight' : 'app.themeToDark'), onclick: function () {
      var n = currentTheme() === 'dark' ? 'light' : 'dark'; applyTheme(n); ADE.store.set('theme', n); renderChrome();
    } }, icon(th === 'dark' ? 'sun' : 'moon', { size: 18 }));
    var reduced = ADE.motionReduced();
    var bMotion = h('button', { type: 'button', 'data-fk': 'motion', class: 'btn toggle', 'aria-pressed': reduced ? 'true' : 'false', title: ADE.t('app.reducedMotionHint'), onclick: function () {
      ADE.store.set('motion', ADE.motionReduced() ? 'full' : 'reduce'); applyMotion(); renderChrome(); rerender();
    } }, icon('motion', { size: 16 }), h('span', { class: 'lbl', text: ADE.t('app.reducedMotion') }));
    var live = r.page === 'live';
    var modeSeg = h('div', { class: 'seg mode', role: 'group', 'aria-label': ADE.t('app.mode') },
      h('a', { 'data-fk': 'mode-guided', class: 'seg-b' + (!live ? ' on' : ''), href: lastGuidedHref(), 'aria-current': !live ? 'page' : null, text: ADE.t('app.guided') }),
      h('a', { 'data-fk': 'mode-live', class: 'seg-b' + (live ? ' on' : ''), href: href('live'), 'aria-current': live ? 'page' : null, text: ADE.t('app.live') }));
    header.appendChild(h('div', { class: 'topbar-in' }, drawerBtn, brand, ctx, h('div', { class: 'top-right' }, modeSeg, bMotion, bTheme, langSeg)));

    // toolbar: ô tìm kiếm + chip ngữ cảnh + liên kết trang chung
    ui.clear(toolbar);
    var search = h('button', { type: 'button', 'data-fk': 'search', class: 'searchbox', 'aria-label': ADE.t('app.search'), onclick: function () { ADE.search.openDialog(); } }, icon('search', { size: 16 }), h('span', { class: 'ph', text: ADE.t('app.searchPlaceholder') }), h('kbd', { text: 'Ctrl K' }));
    var chips = h('div', { class: 'ctx-chips', role: 'navigation', 'aria-label': ADE.t('app.tracks') });
    ADE.tracks.forEach(function (t) {
      chips.appendChild(h('a', { class: 'ctx-chip' + (trk && trk.id === t.id ? ' on' : ''), href: href(t.id), 'aria-current': trk && trk.id === t.id ? 'page' : null }, h('i', { class: 'accent-dot', style: 'background:' + t.accent, 'aria-hidden': 'true' }), h('span', { text: t.code + ' · ' + ADE.t(t.titleKey) })));
    });
    var links = h('nav', { class: 'toplinks', 'aria-label': ADE.t('app.pages') });
    [['misconceptions', 'app.nav.misconceptions'], ['glossary', 'app.nav.glossary'], ['sources', 'app.nav.sources'], ['about', 'app.nav.about']].forEach(function (p) {
      links.appendChild(h('a', { href: href(p[0]), class: r.page === p[0] ? 'on' : '', 'aria-current': r.page === p[0] ? 'page' : null, text: ADE.t(p[1]) }));
    });
    var help = h('button', { type: 'button', 'data-fk': 'help', class: 'btn icon', 'aria-label': ADE.t('app.shortcuts'), title: ADE.t('app.shortcuts') + ' (?)', onclick: openHelp }, icon('keyboard', { size: 18 }));
    var sansOn = root.classList.contains('sans-prose');
    var bSans = h('button', { type: 'button', 'data-fk': 'sans', class: 'btn toggle small', 'aria-pressed': sansOn ? 'true' : 'false', title: ADE.t('app.sansHint'), onclick: function () {
      var on = !root.classList.contains('sans-prose'); root.classList.toggle('sans-prose', on); ADE.store.set('sans', on); renderChrome();
    } }, icon('sans', { size: 14 }), h('span', { text: ADE.t('app.sans') }));
    toolbar.appendChild(h('div', { class: 'toolbar-in' }, search, chips, links, bSans, help));
    renderFooter();
    renderRail(r);
    renderDrawer();
    ADE.markMissing(document.getElementById('app'));
  }
  function renderFooter() {
    var f = document.querySelector('.foot'); if (!f) return;
    ui.clear(f);
    f.appendChild(h('p', null, h('span', { text: ADE.t('app.footer') }), ' ', h('a', { href: href('about'), text: ADE.t('app.nav.about') }), ' · ', h('span', { class: 'ver', text: 'v' + ADE.version })));
  }
  function lastGuidedHref() {
    var last = ADE.store.get('last', null);
    if (last && ADE.getChapter(last.track, last.chapter)) return href(last.track + '/' + last.chapter);
    return href('');
  }
  function openHelp() { ui.dialog(ADE.t('app.shortcuts'), ADE.controls.helpBody(), { cls: 'dlg-help' }); }

  function renderRail(r) {
    ui.clear(rail);
    var trk = r.page === 'track' ? ADE.getTrack(r.track) : null;
    shell.classList.toggle('has-rail', !!trk);
    if (!trk) return;
    var collapsed = root.classList.contains('rail-collapsed');
    railBtn = h('button', { type: 'button', 'data-fk': 'rail-toggle', class: 'btn icon rail-toggle', 'aria-expanded': collapsed ? 'false' : 'true', 'aria-label': ADE.t('app.railToggle'), title: ADE.t('app.railToggle'), onclick: function () {
      var c = !root.classList.contains('rail-collapsed'); root.classList.toggle('rail-collapsed', c); ADE.store.set('rail', c); railBtn.setAttribute('aria-expanded', c ? 'false' : 'true');
    } }, icon('rail', { size: 18 }));
    rail.appendChild(railBtn);
    var box = h('div', { class: 'rail-body' });
    box.appendChild(h('h2', { class: 'caps', text: ADE.t('app.chapters') }));
    var ol = h('ol', { class: 'rail-list' });
    trk.chapters.forEach(function (c, i) {
      var on = r.chapter === c.id, pg = getProg(trk.id, c.id);
      ol.appendChild(h('li', null, h('a', { href: href(trk.id + '/' + c.id), class: on ? 'on' : '', 'aria-current': on ? 'page' : null },
        h('span', { class: 'rn' }, pg.done ? icon('check', { size: 13, sw: 2.4 }) : String(i)), h('span', { class: 'rt', text: ADE.t(c.titleKey) }), pg.done ? h('span', { class: 'sr-only', text: ' (' + ADE.t('app.done') + ')' }) : null)));
    });
    box.appendChild(ol); rail.appendChild(box);
  }

  /* ---------- drawer catalog: chip domain (có đếm) · accordion track → chương → bước ---------- */
  function toggleDrawer(open) {
    drawer.hidden = !open; backdrop.hidden = !open;
    drawerBtn.setAttribute('aria-expanded', open ? 'true' : 'false');
    document.body.classList.toggle('no-scroll', open);
    if (open) { var f = drawer.querySelector('button,a'); if (f) f.focus(); } else drawerBtn.focus();
  }
  function stepTitles(chapter) {
    var id = chapter.sims[0], d = id && ADE.models[id];
    if (!d || d.kind !== 'discrete') return [];
    try { return d.steps(d.init({})).map(function (s) { return ADE.t(s.titleKey, s.params); }); } catch (e) { return []; }
  }
  function renderDrawer() {
    ui.clear(drawer);
    var doms = ADE.domains();
    drawer.appendChild(h('header', { class: 'drawer-h' }, h('h2', { class: 'caps', text: ADE.t('app.catalog') }), h('button', { type: 'button', class: 'btn icon', 'aria-label': ADE.t('app.close'), onclick: function () { toggleDrawer(false); } }, icon('close', { size: 16 }))));
    var dl = h('nav', { class: 'drawer-links', 'aria-label': ADE.t('app.pages') });
    [['', 'app.home'], ['misconceptions', 'app.nav.misconceptions'], ['glossary', 'app.nav.glossary'], ['sources', 'app.nav.sources'], ['about', 'app.nav.about']].forEach(function (p) {
      dl.appendChild(h('a', { href: href(p[0]), onclick: function () { toggleDrawer(false); }, text: ADE.t(p[1]) }));
    });
    drawer.appendChild(dl);
    var chips = h('div', { class: 'chips filter', role: 'group', 'aria-label': ADE.t('app.filterDomain') });
    var total = ADE.tracks.length;
    chips.appendChild(h('button', { type: 'button', 'data-fk': 'dchip-all', class: 'chip btn' + (drawerDomain === 'all' ? ' on' : ''), 'aria-pressed': drawerDomain === 'all' ? 'true' : 'false', onclick: function () { drawerDomain = 'all'; renderDrawer(); } }, h('span', { text: ADE.t('app.all') }), h('b', { text: String(total) })));
    doms.forEach(function (d) { chips.appendChild(h('button', { type: 'button', 'data-fk': 'dchip-' + d.id, class: 'chip btn' + (drawerDomain === d.id ? ' on' : ''), 'aria-pressed': drawerDomain === d.id ? 'true' : 'false', onclick: function () { drawerDomain = d.id; renderDrawer(); } }, h('span', { text: ADE.domainLabel(d.id) }), h('b', { text: String(d.tracks.length) }))); });
    drawer.appendChild(chips);
    var body = h('div', { class: 'drawer-b' });
    if (!ADE.tracks.length) body.appendChild(h('p', { class: 'muted pad', text: ADE.t('app.noTracks') }));
    ADE.tracks.forEach(function (t) {
      if (drawerDomain !== 'all' && t.domain !== drawerDomain) return;
      var det = h('details', { class: 'acc' }, h('summary', null, h('i', { class: 'accent-dot', style: 'background:' + t.accent, 'aria-hidden': 'true' }), h('span', { text: t.code + ' · ' + ADE.t(t.titleKey) })));
      det.appendChild(h('a', { class: 'acc-link', href: href(t.id), onclick: function () { toggleDrawer(false); }, text: ADE.t('app.overview') }));
      t.chapters.forEach(function (c) {
        var steps = stepTitles(c);
        var ch = h('details', { class: 'acc sub' }, h('summary', null, h('span', { text: ADE.t(c.titleKey) })));
        ch.appendChild(h('a', { class: 'acc-link', href: href(t.id + '/' + c.id), onclick: function () { toggleDrawer(false); }, text: ADE.t('app.openChapter') }));
        if (steps.length) {
          var ol = h('ol', { class: 'acc-steps' });
          steps.forEach(function (s, i) { ol.appendChild(h('li', null, h('a', { href: href(t.id + '/' + c.id + '/' + (i + 1)), onclick: function () { toggleDrawer(false); } }, h('span', { class: 'n', text: String(i + 1) }), h('span', { text: s })))); });
          ch.appendChild(ol);
        }
        det.appendChild(ch);
      });
      body.appendChild(det);
    });
    drawer.appendChild(body);
  }

  /* ================= đổi ngôn ngữ (giữ route và trạng thái mô phỏng) ================= */
  function switchLang(l) {
    if (l === ADE.lang) return;
    ADE.setLang(l, true);
    ADE.search.invalidate();
    ADE.router.replace(ADE.router.withLang(l));
    renderChrome();
    rerender();
    ui.announce(ADE.t('app.langChanged'));
  }

  /* ================= điều hướng và render ================= */
  function pageKeyOf(r) { return r.page + '|' + (r.track || '') + '|' + (r.chapter || '') + '|' + (r.query && r.query.preset || '') + '|' + (r.id || ''); }
  function unmount() { cur.mounts.forEach(function (m) { try { m.destroy(); } catch (e) { /* bỏ qua */ } }); cur.mounts = []; }
  function destroySessions() { Object.keys(cur.sessions).forEach(function (k) { cur.sessions[k].destroy(); }); cur.sessions = {}; cur.viewStates = {}; }
  var lastRoute = null;

  function handleRoute(r) {
    if (r.lang && r.lang !== ADE.lang) { ADE.setLang(r.lang, true); ADE.search.invalidate(); }
    var key = pageKeyOf(r);
    var samePage = key === cur.pageKey;
    var langChanged = cur.lang !== ADE.lang;
    cur.lang = ADE.lang;
    if (samePage && langChanged && lastRoute) { lastRoute = r; rerender(); return; }   // đổi ngôn ngữ qua URL: giữ session
    if (samePage && lastRoute && r.page === 'track' && r.chapter) {
      // chỉ đổi bước (hoặc ngôn ngữ): không dựng lại trang
      var s = cur.sessions[cur.simKey];
      if (s && s.kind === 'discrete' && r.step != null && r.step !== s.pos) s.goto(r.step);
      lastRoute = r; renderChrome(); return;
    }
    if (samePage && r.page === 'live') {
      var ls = cur.sessions[cur.simKey];
      if (ls && ls.kind === 'discrete') { var st = r.query.step != null ? parseInt(r.query.step, 10) : null; if (st != null && !isNaN(st) && st !== ls.pos) ls.goto(st); }
      lastRoute = r; renderChrome(); return;
    }
    if (!samePage) destroySessions();
    cur.pageKey = key; lastRoute = r;
    renderMain(r);
    renderChrome();
    if (!samePage) { window.scrollTo(0, 0); if (r.page !== 'home' || true) { try { main.focus({ preventScroll: true }); } catch (e) { /* noop */ } } }
    toggleDrawerSafe();
  }
  function toggleDrawerSafe() { if (!drawer.hidden) { drawer.hidden = true; backdrop.hidden = true; document.body.classList.remove('no-scroll'); drawerBtn.setAttribute('aria-expanded', 'false'); } }
  function rerender() {
    var y = window.scrollY, r = ADE.router.parse();
    ui.withFocus(function () { renderMain(r); renderChrome(); });
    window.scrollTo(0, y);
  }
  app.rerender = rerender;

  function renderMain(r) {
    unmount();
    ui.clear(main);
    var node;
    try {
      switch (r.page) {
        case 'home': node = pageHome(); break;
        case 'track': node = r.chapter ? pageChapter(r) : pageTrack(r); break;
        case 'live': node = pageLive(r); break;
        case 'misconceptions': node = pageMisconceptions(r); break;
        case 'glossary': node = pageGlossary(r); break;
        case 'sources': node = pageSources(r); break;
        case 'about': node = pageAbout(); break;
        case 'search': node = pageSearch(r); break;
        default: node = pageNotFound();
      }
    } catch (e) {
      console.error(e);
      node = h('div', { class: 'panel pad' }, h('h1', { text: ADE.t('app.error') }), h('pre', { class: 'code', translate: 'no', text: String(e && e.stack || e) }));
    }
    main.appendChild(node);
    ADE.markMissing(main);
    if (r.id && { glossary: 'glo', sources: 'src', misconceptions: 'mis' }[r.page]) scrollToId({ glossary: 'glo', sources: 'src', misconceptions: 'mis' }[r.page] + '-' + r.id);
  }

  /* ================= trang chủ / catalog ================= */
  function pageHome() {
    setTitle('');
    var wrap = h('article', { class: 'page home' });
    var hero = h('section', { class: 'hero panel' },
      h('div', { class: 'hero-art', 'aria-hidden': 'true', html: ADE.diagram.logo(84) }),
      h('div', { class: 'hero-t' }, h('h1', { class: 'caps', text: ADE.t('app.heroTitle') }), para(ADE.t('app.heroLead')),
        h('div', { class: 'row-actions' }, h('a', { class: 'btn primary', href: '#catalog', onclick: function (e) { e.preventDefault(); var c = document.getElementById('catalog'); if (c) c.scrollIntoView(); } }, icon('layers', { size: 16 }), h('span', { text: ADE.t('app.browseCatalog') })),
          h('a', { class: 'btn', href: href('live') }, icon('play', { size: 16 }), h('span', { text: ADE.t('app.openLive') })))));
    wrap.appendChild(hero);

    var last = ADE.store.get('last', null), lc = last && ADE.getChapter(last.track, last.chapter);
    if (lc) {
      var pg = getProg(last.track, last.chapter);
      wrap.appendChild(h('section', { class: 'panel continue' }, h('h2', { class: 'caps', text: ADE.t('app.continue') }),
        h('p', null, h('b', { text: ADE.t(lc.track.titleKey) }), ' › ', ADE.t(lc.chapter.titleKey), pg.done ? ' (' + ADE.t('app.done') + ')' : ''),
        h('a', { class: 'btn primary', href: href(last.track + '/' + last.chapter) }, h('span', { text: ADE.t('app.continueBtn') }), icon('next', { size: 14 }))));
    }

    // hai chế độ + phím tắt
    wrap.appendChild(h('section', { class: 'modes' },
      h('div', { class: 'panel pad' }, h('h2', { class: 'caps', text: ADE.t('app.guided') }), para(ADE.t('app.guidedDesc'))),
      h('div', { class: 'panel pad' }, h('h2', { class: 'caps', text: ADE.t('app.live') }), para(ADE.t('app.liveDesc'))),
      h('div', { class: 'panel pad' }, h('h2', { class: 'caps', text: ADE.t('app.shortcuts') }), para(ADE.t('app.shortcutsDesc')), h('button', { type: 'button', class: 'btn', onclick: openHelp }, icon('keyboard', { size: 16 }), h('span', { text: ADE.t('app.showShortcuts') })))));

    // catalog
    var cat = h('section', { class: 'catalog', id: 'catalog' });
    cat.appendChild(h('h2', { class: 'caps sec-h', text: ADE.t('app.catalog') }));
    var doms = ADE.domains();
    var fb = h('div', { class: 'filters' });
    var dchips = h('div', { class: 'chips filter', role: 'group', 'aria-label': ADE.t('app.filterDomain') });
    var mkChip = function (id, label, n) { return h('button', { type: 'button', 'data-fk': 'fchip-' + id, class: 'chip btn' + (filters.domain === id ? ' on' : ''), 'aria-pressed': filters.domain === id ? 'true' : 'false', onclick: function () { filters.domain = id; rerender(); } }, h('span', { text: label }), h('b', { text: String(n) })); };
    dchips.appendChild(mkChip('all', ADE.t('app.all'), ADE.tracks.length));
    doms.forEach(function (d) { dchips.appendChild(mkChip(d.id, ADE.domainLabel(d.id), d.tracks.length)); });
    fb.appendChild(dchips);
    var sel = function (id, labelKey, opts) {
      var s = h('select', { id: id, 'data-fk': id, class: 'sel', onchange: function () { filters[id.slice(2)] = s.value; rerender(); } });
      opts.forEach(function (o) { s.appendChild(h('option', { value: o[0], selected: filters[id.slice(2)] === o[0] ? true : null, text: o[1] })); });
      return h('label', { class: 'field inline', for: id }, h('span', { text: ADE.t(labelKey) }), s);
    };
    fb.appendChild(sel('f-level', 'app.filterLevel', [['all', ADE.t('app.all')], ['beginner', ADE.t('app.level.beginner')], ['intermediate', ADE.t('app.level.intermediate')], ['advanced', ADE.t('app.level.advanced')]]));
    fb.appendChild(sel('f-status', 'app.filterStatus', [['all', ADE.t('app.all')], ['stable', ADE.t('app.status.stable')], ['draft', ADE.t('app.status.draft')]]));
    cat.appendChild(fb);
    var shown = 0;
    doms.forEach(function (d) {
      if (filters.domain !== 'all' && filters.domain !== d.id) return;
      var list = d.tracks.filter(function (t) { return (filters.level === 'all' || t.level === filters.level) && (filters.status === 'all' || t.status === filters.status); });
      if (!list.length) return;
      cat.appendChild(h('h3', { class: 'caps dom-h', text: ADE.domainLabel(d.id) }));
      var grid = h('div', { class: 'cards' });
      list.forEach(function (t) { grid.appendChild(trackCard(t)); shown++; });
      cat.appendChild(grid);
    });
    if (!shown) cat.appendChild(empty(ADE.tracks.length ? 'app.noMatch' : 'app.noTracks'));
    wrap.appendChild(cat);

    // lộ trình học
    var paths = ADE.pathList.map(function (p) { return { p: p, steps: p.steps.map(function (ref) { return { ref: ref, r: ADE.resolveRef(ref) }; }) }; }).filter(function (x) { return x.steps.some(function (s) { return s.r; }); });
    if (paths.length) {
      var ps = h('section', { class: 'paths' }, h('h2', { class: 'caps sec-h', text: ADE.t('app.paths') }));
      var grid2 = h('div', { class: 'cards' });
      paths.forEach(function (x) {
        var ol = h('ol', { class: 'path-steps' });
        x.steps.forEach(function (s) {
          if (!s.r) return;
          var label = s.r.track.code + (s.r.chapter ? ' · ' + ADE.t(s.r.chapter.titleKey) : ' · ' + ADE.t(s.r.track.titleKey));
          ol.appendChild(h('li', null, h('a', { href: href(s.r.track.id + (s.r.chapter ? '/' + s.r.chapter.id : '')), text: label })));
        });
        grid2.appendChild(h('div', { class: 'panel pad path' }, h('h3', { text: ADE.t('shared.path.' + x.p.id + '.title') }), para(ADE.t('shared.path.' + x.p.id + '.desc')), ol));
      });
      ps.appendChild(grid2); wrap.appendChild(ps);
    }

    // bản đồ cầu nối
    var bridges = ADE.bridgeList.filter(function (b) { return ADE.resolveRef(b.owner); });
    if (bridges.length) {
      var bs = h('section', { class: 'bridges' }, h('h2', { class: 'caps sec-h', text: ADE.t('app.bridgeMap') }));
      bs.appendChild(bridgeSvg(bridges));
      var ul = h('ul', { class: 'bridge-list' });
      bridges.forEach(function (b) {
        var o = ADE.resolveRef(b.owner), links = h('span', { class: 'chips' });
        (b.links || []).forEach(function (ref) { var r = ADE.resolveRef(ref); if (r && r.chapter) links.appendChild(h('a', { class: 'chip', href: href(r.track.id + '/' + r.chapter.id), text: r.track.code + ' · ' + ADE.t(r.chapter.titleKey) })); });
        ul.appendChild(h('li', { class: 'panel pad' }, h('b', { text: b.id + ' · ' + ADE.t('shared.bridge.' + b.id + '.title') }), para(ADE.t('shared.bridge.' + b.id + '.summary')),
          h('p', { class: 'hint' }, ADE.t('app.owner') + ': ', o.chapter ? h('a', { href: href(o.track.id + '/' + o.chapter.id), text: ADE.t(o.chapter.titleKey) }) : ADE.t(o.track.titleKey)), links));
      });
      bs.appendChild(ul); wrap.appendChild(bs);
    }
    return wrap;
  }
  /* Bản đồ cầu nối dạng SVG line-art (P7): mỗi track là một khối isometric (sinh từ registry, không biết id nào),
     mỗi cầu nối là đường từ track chủ sở hữu tới track dẫn link, nhãn là mã cầu nối. Khối là link tới trang track. */
  function bridgeSvg(bridges) {
    var NS = 'http://www.w3.org/2000/svg', tracks = ADE.tracks.slice(), n = tracks.length, pos = {}, W = 640, H = 300;
    tracks.forEach(function (t, i) { var ang = -Math.PI / 2 + i * 2 * Math.PI / n; pos[t.id] = [W / 2 + Math.cos(ang) * 230, H / 2 + Math.sin(ang) * 105]; });
    var svg = document.createElementNS(NS, 'svg'); svg.setAttribute('viewBox', '0 0 ' + W + ' ' + H); svg.setAttribute('class', 'bridge-map'); svg.setAttribute('role', 'group'); svg.setAttribute('aria-label', ADE.t('app.bridgeMap'));
    var html = '<title>' + ADE.esc(ADE.t('app.bridgeMap')) + '</title>', pairs = {};
    bridges.forEach(function (b) {
      var o = ADE.resolveRef(b.owner); if (!o) return;
      (b.links || []).forEach(function (ref) {
        var r = ADE.resolveRef(ref); if (!r || r.track.id === o.track.id) return;
        var key = [o.track.id, r.track.id].sort().join('|'); pairs[key] = pairs[key] || {}; pairs[key][b.id] = 1;
      });
    });
    Object.keys(pairs).forEach(function (key) {
      var ids = key.split('|'), p = pos[ids[0]], q = pos[ids[1]], mx = (p[0] + q[0]) / 2, my = (p[1] + q[1]) / 2 - 4;
      html += '<line class="bm-edge" x1="' + p[0].toFixed(1) + '" y1="' + p[1].toFixed(1) + '" x2="' + q[0].toFixed(1) + '" y2="' + q[1].toFixed(1) + '"/>' +
        '<text class="bm-label" x="' + mx.toFixed(1) + '" y="' + my.toFixed(1) + '" text-anchor="middle">' + ADE.esc(Object.keys(pairs[key]).sort().join(' ')) + '</text>';
    });
    tracks.forEach(function (t) {
      var p = pos[t.id], x = p[0], y = p[1];
      html += '<a href="' + ADE.esc(href(t.id)) + '" class="bm-node"><title>' + ADE.esc(ADE.t(t.titleKey)) + '</title>' +
        '<path class="bm-box" d="M' + (x - 34) + ' ' + y + 'l34 -17 34 17 -34 17z M' + (x - 34) + ' ' + y + 'v10l34 17 34 -17v-10 M' + x + ' ' + (y + 17) + 'v10"/>' +
        '<text class="bm-code" x="' + x + '" y="' + (y + 4) + '" text-anchor="middle">' + ADE.esc(t.code) + '</text></a>';
    });
    svg.innerHTML = html;
    return h('div', { class: 'bridge-map-wrap' }, svg);
  }
  function trackCard(t) {
    var tp = trackProgress(t);
    return h('a', { class: 'card', href: href(t.id), style: '--accent:' + t.accent },
      h('span', { class: 'card-stripe', 'aria-hidden': 'true' }),
      h('span', { class: 'card-h' }, icon(trackIcon(t), { size: 28, sw: 1.5 }), h('span', { class: 'card-code', text: t.code })),
      h('span', { class: 'card-t', text: ADE.t(t.titleKey) }),
      h('span', { class: 'card-s', text: ADE.t(t.summaryKey) }),
      metaChips(t),
      h('span', { class: 'card-p' }, h('progress', { max: String(tp.total), value: String(tp.done), 'aria-label': ADE.t('app.progress') }), h('span', { text: ADE.t('app.chaptersDone', { n: tp.done, total: tp.total }) })));
  }

  /* ================= track ================= */
  function pageTrack(r) {
    var t = ADE.getTrack(r.track);
    if (!t) return pageNotFound();
    setTitle(ADE.t(t.titleKey));
    var wrap = h('article', { class: 'page track', style: '--accent:' + t.accent });
    wrap.appendChild(crumbs([[ADE.t('app.home'), href('')], [ADE.t(t.titleKey)]]));
    wrap.appendChild(h('header', { class: 'page-h track-h' }, h('span', { class: 'accent-bar', 'aria-hidden': 'true' }), h('h1', { class: ui.caps(ADE.t(t.titleKey)), text: ADE.t(t.titleKey) }), para(ADE.t(t.summaryKey)), metaChips(t)));
    if (t.prerequisites.length) {
      var pl = h('p', { class: 'hint' }, ADE.t('app.prereq') + ': ');
      t.prerequisites.forEach(function (p, i) { var pt = ADE.getTrack(p); if (pt) { if (i) pl.appendChild(document.createTextNode(', ')); pl.appendChild(h('a', { href: href(p), text: ADE.t(pt.titleKey) })); } });
      wrap.appendChild(pl);
    }
    var list = h('ol', { class: 'chapter-list' });
    t.chapters.forEach(function (c, i) {
      var pg = getProg(t.id, c.id);
      list.appendChild(h('li', null, h('a', { class: 'panel ch-card', href: href(t.id + '/' + c.id) },
        h('span', { class: 'rn big' }, pg.done ? icon('check', { size: 18, sw: 2.4 }) : String(i)),
        h('span', { class: 'ch-card-t' }, h('b', { text: ADE.t(c.titleKey) }), h('small', { text: pg.done ? ADE.t('app.done') : pg.max > 0 ? ADE.t('app.inProgress') : ADE.t('app.notStarted') })))));
    });
    wrap.appendChild(h('h2', { class: 'caps sec-h', text: ADE.t('app.chapters') }));
    wrap.appendChild(list);
    if (t.presets.length) {
      var pr = h('div', { class: 'chips' });
      t.presets.forEach(function (p) { pr.appendChild(h('a', { class: 'chip btn', href: href('live?preset=' + p.id) }, icon('play', { size: 12 }), h('span', { text: ADE.t(p.titleKey) }))); });
      wrap.appendChild(h('h2', { class: 'caps sec-h', text: ADE.t('app.presets') })); wrap.appendChild(pr);
    }
    return wrap;
  }
  function crumbs(items) {
    var ol = h('ol', { class: 'crumbs' });
    items.forEach(function (it, i) { ol.appendChild(h('li', null, it[1] ? h('a', { href: it[1], text: it[0] }) : h('span', { 'aria-current': 'page', text: it[0] }))); });
    return h('nav', { 'aria-label': ADE.t('app.breadcrumb') }, ol);
  }

  /* ================= chương (Guided) ================= */
  function sessionFor(key, modelId, params) {
    if (!cur.sessions[key]) cur.sessions[key] = ADE.engine.create(modelId, params);
    return cur.sessions[key];
  }
  function mountStage(slot, trackId, chapter, modelId, mode, startPos) {
    var def = ADE.models[modelId];
    if (!def) { slot.appendChild(empty('app.noModel')); return; }
    if (def.kind === 'compute') {
      var vw = ADE.views[modelId];
      if (vw && vw.mount) { var m = vw.mount(slot, { trackId: trackId, modelId: modelId, def: def }); if (m) cur.mounts.push(m); }
      return;
    }
    var key = (mode === 'live' ? 'live:' : 'ch:' + trackId + '/' + chapter.id + ':') + modelId;
    cur.simKey = key;
    var S = sessionFor(key, modelId);
    var vsKey = 'vs:' + key; cur.viewStates[vsKey] = cur.viewStates[vsKey] || { canvasTab: 'diagram', sideTab: 'explain', mtab: 'diagram' };
    if (startPos != null) S.goto(startPos);
    var onQuiz = function () { var q = document.getElementById('quiz'); if (q) q.scrollIntoView({ behavior: ADE.motionReduced() ? 'auto' : 'smooth' }); };
    var m = ui.mountSim(slot, {
      session: S, trackId: trackId, modelId: modelId, mode: mode, viewState: cur.viewStates[vsKey],
      goals: chapter ? function () {
        var pg = getProg(trackId, chapter.id), mx = Math.max(pg.max, S.maxPos), N = S.N || 0;
        return chapter.goals.map(function (g) { return { id: g.id, text: ADE.t(ADE.chapterKey(trackId, chapter.id, 'goal.' + g.id)), done: g.step === 'end' ? (pg.done || mx > N) : mx >= g.step }; });
      } : null,
      onQuiz: chapter ? onQuiz : null,
      onPos: function (pos) {
        if (chapter) saveProg(trackId, chapter.id, pos, S.N);
        var rr = ADE.router.parse();
        if (mode === 'live') { rr.query = rr.query || {}; rr.query.step = pos || ''; ADE.router.replace(ADE.router.build(rr)); }
        else { rr.step = pos; ADE.router.replace(ADE.router.build(rr)); }
        if (chapter) { renderRailOnly(); }
      }
    });
    cur.mounts.push(m);
  }
  function renderRailOnly() { var r = ADE.router.parse(); var tb = rail.scrollTop; renderRail(r); rail.scrollTop = tb; }

  function pageChapter(r) {
    var info = ADE.getChapter(r.track, r.chapter);
    if (!info) return pageNotFound();
    var t = info.track, c = info.chapter, i = info.index, base = ADE.chapterKey(t.id, c.id);
    var title = ADE.t(c.titleKey);
    setTitle(title + ' · ' + ADE.t(t.titleKey));
    ADE.store.set('last', { track: t.id, chapter: c.id });
    var wrap = h('article', { class: 'page chapter', style: '--accent:' + t.accent });
    wrap.appendChild(crumbs([[ADE.t('app.home'), href('')], [ADE.t(t.titleKey), href(t.id)], [title]]));
    wrap.appendChild(h('header', { class: 'page-h' }, h('p', { class: 'eyebrow' }, h('span', { class: 'accent-bar inline', 'aria-hidden': 'true' }), t.code + ' · ' + ADE.t('app.chapterNofM', { n: i + 1, total: t.chapters.length })),
      h('h1', { class: ui.caps(title), text: title }), metaChips(t)));
    // 1. bản chất
    wrap.appendChild(h('section', { class: 'panel essence' }, h('header', { class: 'panel-h' }, h('h2', { class: 'caps', text: ADE.t('app.essence') })), h('div', { class: 'pad' }, lines(base + '.essence'))));
    // 2. mô phỏng (mặc định ngay sau "bản chất"; chapter.simAfter = id mục → đặt sau mục đó, để câu "đoán trước" đứng trước sim)
    function addSim() {
      if (!c.sims.length) return;
      var simSel = cur.viewStates['sim:' + t.id + '/' + c.id] || (cur.viewStates['sim:' + t.id + '/' + c.id] = { idx: 0 });
      var slot = h('div', { class: 'stage-slot' });
      if (c.sims.length > 1) {
        wrap.appendChild(ui.tabs(c.sims.map(function (s, k) { return { id: String(k), label: ADE.hasKey(ADE.chapterKey(t.id, c.id, 'sim.' + s)) ? ADE.t(ADE.chapterKey(t.id, c.id, 'sim.' + s)) : s }; }), String(simSel.idx), function (id) { simSel.idx = parseInt(id, 10); rerender(); }, ADE.t('app.sims')));
      }
      wrap.appendChild(slot);
      mountStage(slot, t.id, c, c.sims[Math.min(simSel.idx, c.sims.length - 1)], 'guided', r.step != null ? r.step : null);
    }
    var secIds = ADE.keysUnder(base + '.sec');
    if (!c.simAfter || secIds.indexOf(c.simAfter) < 0) addSim();
    // 3. các mục nội dung (khối v2: docs/core-api.md §2.1)
    secIds.forEach(function (s) {
      var pre = base + '.sec.' + s, st = ADE.t(pre + '.title');
      var sec = h('section', { class: 'panel sec', id: 'sec-' + s }, h('header', { class: 'panel-h' }, h('h2', { class: ui.caps(st), text: st }),
        ADE.hasKey(pre + '.badge') ? h('span', { class: 'badges' }, ADE.t(pre + '.badge').split(/\s+/).filter(Boolean).map(function (b) { return ui.badge(b); })) : null));
      var body = h('div', { class: 'pad' });
      ADE.keysUnder(pre).forEach(function (part) {
        if (part === 'p') ADE.keysUnder(pre + '.p').forEach(function (n) { body.appendChild(para(ADE.t(pre + '.p.' + n))); });
        else if (part === 'code') { var sn = ADE.getCode(t.id, ADE.t(pre + '.code')); if (sn) body.appendChild(ui.codeBlock(sn, [])); }
        else if (part === 'b') ADE.keysUnder(pre + '.b').forEach(function (n) { var el = block(pre + '.b.' + n); if (el) body.appendChild(el); });
      });
      sec.appendChild(body); wrap.appendChild(sec);
      if (c.simAfter === s) addSim();
    });
    // 4. tự kiểm tra
    var qs = ADE.keysUnder(base + '.quiz');
    if (qs.length) {
      var qbox = h('section', { class: 'panel quiz', id: 'quiz' }, h('header', { class: 'panel-h' }, h('h2', { class: 'caps', text: ADE.t('app.selfCheck') })));
      var qb = h('div', { class: 'pad' });
      qs.forEach(function (q, n) {
        var qp = base + '.quiz.' + q;
        var det = h('details', { class: 'qa' }, h('summary', null, h('span', { class: 'n', text: String(n + 1) }), h('span', { html: ADE.markup(ADE.t(qp + '.q')) })), h('div', { class: 'qa-a' }, h('p', { class: 'prose' }, h('b', { text: ADE.t('app.answer') + ': ' }), h('span', { html: ADE.markup(ADE.t(qp + '.a')) })), h('p', { class: 'prose', html: ADE.markup(ADE.t(qp + '.why')) })));
        det.addEventListener('toggle', function () { if (det.open) { var p = progress[pkey(t.id, c.id)] = getProg(t.id, c.id); p.quiz[q] = true; ADE.store.set('progress', progress); } });
        qb.appendChild(det);
      });
      qbox.appendChild(qb); wrap.appendChild(qbox);
    }
    // 5. cầu nối
    if (c.bridges.length) {
      var bl = h('ul', { class: 'bridge-list' });
      c.bridges.forEach(function (bid) {
        var b = ADE.bridgeMap[bid]; if (!b) return;
        var item = h('li', { class: 'pad panel' }, h('b', { text: bid + ' · ' + ADE.t('shared.bridge.' + bid + '.title') }), para(ADE.t('shared.bridge.' + bid + '.summary')));
        var rs = h('span', { class: 'chips' });
        [b.owner].concat(b.links || []).forEach(function (ref) { var rr = ADE.resolveRef(ref); if (rr && rr.chapter && !(rr.track.id === t.id && rr.chapter.id === c.id)) rs.appendChild(h('a', { class: 'chip', href: href(rr.track.id + '/' + rr.chapter.id), text: rr.track.code + ' · ' + ADE.t(rr.chapter.titleKey) })); });
        item.appendChild(rs); bl.appendChild(item);
      });
      wrap.appendChild(h('section', { class: 'bridges' }, h('h2', { class: 'caps sec-h', text: ADE.t('app.bridges') }), bl));
    }
    reveal(wrap);
    // 6. chương trước / sau
    var prev = t.chapters[i - 1], next = t.chapters[i + 1];
    wrap.appendChild(h('nav', { class: 'ch-nav', 'aria-label': ADE.t('app.chapterNav') },
      prev ? h('a', { class: 'btn', href: href(t.id + '/' + prev.id) }, icon('prev', { size: 14 }), h('span', null, h('small', { text: ADE.t('app.prevChapter') }), h('span', { class: 'nav-t', text: ADE.t(prev.titleKey) }))) : h('span'),
      next ? h('a', { class: 'btn primary', href: href(t.id + '/' + next.id) }, h('span', null, h('small', { text: ADE.t('app.nextChapter') }), h('span', { class: 'nav-t', text: ADE.t(next.titleKey) })), icon('next', { size: 14 })) : h('a', { class: 'btn', href: href(t.id) }, h('span', { text: ADE.t('app.backToTrack') }))));
    return wrap;
  }

  /* ================= Live Explorer ================= */
  function pageLive(r) {
    setTitle(ADE.t('app.live'));
    var all = ADE.allPresets();
    var wrap = h('article', { class: 'page live' });
    wrap.appendChild(h('header', { class: 'page-h' }, h('h1', { class: 'caps', text: ADE.t('app.live') }), para(ADE.t('app.liveDesc'))));
    if (!all.length) { wrap.appendChild(empty('app.noPresets')); return wrap; }
    var pid = r.query.preset, cur0 = all.filter(function (x) { return x.preset.id === pid; })[0] || all[0];
    var sel = h('select', { id: 'preset', 'data-fk': 'preset', class: 'sel wide', onchange: function () { ADE.router.go({ page: 'live', query: { preset: sel.value } }); } });
    ADE.tracks.forEach(function (t) {
      if (!t.presets.length) return;
      var og = h('optgroup', { label: t.code + ' · ' + ADE.t(t.titleKey) });
      t.presets.forEach(function (p) { og.appendChild(h('option', { value: p.id, selected: p.id === cur0.preset.id ? true : null, text: ADE.t(p.titleKey) })); });
      sel.appendChild(og);
    });
    wrap.appendChild(h('div', { class: 'panel pad preset-bar' }, h('label', { class: 'field', for: 'preset' }, h('span', { text: ADE.t('app.preset') }), sel),
      h('a', { class: 'chip', href: href(cur0.track.id) }, h('span', { text: ADE.t(cur0.track.titleKey) }))));
    var slot = h('div', { class: 'stage-slot live-slot' }); wrap.appendChild(slot);
    var startStep = r.query.step != null && !isNaN(parseInt(r.query.step, 10)) ? parseInt(r.query.step, 10) : null;
    mountStage(slot, cur0.track.id, null, cur0.preset.model, 'live', startStep);
    return wrap;
  }

  /* ================= hiểu lầm, glossary, nguồn, về, tìm ================= */
  function nsLabel(ns) { return ns === 'shared' ? ADE.t('app.shared') : ADE.t(ADE.getTrack(ns) ? ADE.getTrack(ns).titleKey : 'app.shared'); }
  var misFilter = 'all';
  function pageMisconceptions(r) {
    setTitle(ADE.t('app.nav.misconceptions'));
    var wrap = stdPage(ADE.t('app.nav.misconceptions'), []);
    wrap.appendChild(para(ADE.t('app.misIntro')));
    var nss = []; ADE.misIds.forEach(function (id) { if (nss.indexOf(ADE.misOwner[id]) < 0) nss.push(ADE.misOwner[id]); });
    if (!nss.length) { wrap.appendChild(empty('app.noMis')); return wrap; }
    var chips = h('div', { class: 'chips filter', role: 'group', 'aria-label': ADE.t('app.filterTrack') });
    var mk = function (id, label) { return h('button', { type: 'button', 'data-fk': 'mis-' + id, class: 'chip btn' + (misFilter === id ? ' on' : ''), 'aria-pressed': misFilter === id ? 'true' : 'false', onclick: function () { misFilter = id; rerender(); }, text: label }); };
    chips.appendChild(mk('all', ADE.t('app.all')));
    nss.forEach(function (ns) { chips.appendChild(mk(ns, nsLabel(ns))); });
    wrap.appendChild(chips);
    var list = h('div', { class: 'mis-list' });
    ADE.misIds.forEach(function (id) {
      var ns = ADE.misOwner[id]; if (misFilter !== 'all' && misFilter !== ns) return;
      var meta = (ADE.misMeta[ADE.lang] || {})[id] || {}, ref = meta.chapter && ADE.resolveRef(meta.chapter);
      list.appendChild(h('article', { class: 'panel mis', id: 'mis-' + id },
        h('header', { class: 'panel-h' }, h('h2', { html: ADE.markup(ADE.t(ADE.misKey(id, 'wrong'))) }), h('span', { class: 'chip', text: nsLabel(ns) })),
        h('div', { class: 'pad' },
          h('p', { class: 'mis-row wrong' }, h('span', { class: 'mis-l' }, icon('cross', { size: 14, sw: 2.2 }), ADE.t('app.mis.wrong')), h('span', { class: 'prose', html: ADE.markup(ADE.t(ADE.misKey(id, 'wrong'))) })),
          h('p', { class: 'mis-row right' }, h('span', { class: 'mis-l' }, icon('check', { size: 14, sw: 2.2 }), ADE.t('app.mis.right')), h('span', { class: 'prose', html: ADE.markup(ADE.t(ADE.misKey(id, 'right'))) })),
          ADE.hasKey(ADE.misKey(id, 'example')) ? h('p', { class: 'mis-row' }, h('span', { class: 'mis-l' }, icon('info', { size: 14 }), ADE.t('app.mis.example')), h('span', { class: 'prose', html: ADE.markup(ADE.t(ADE.misKey(id, 'example'))) })) : null,
          ref && ref.chapter ? h('p', null, h('a', { class: 'btn small', href: href(ref.track.id + '/' + ref.chapter.id) }, h('span', { text: ADE.t('app.toChapter') + ': ' + ADE.t(ref.chapter.titleKey) }), icon('next', { size: 12 }))) : null)));
    });
    wrap.appendChild(list);
    return wrap;
  }
  function pageGlossary(r) {
    setTitle(ADE.t('app.nav.glossary'));
    var wrap = stdPage(ADE.t('app.nav.glossary'), []);
    wrap.appendChild(para(ADE.t('app.glossIntro')));
    if (!ADE.glossaryIds.length) { wrap.appendChild(empty('app.noGloss')); return wrap; }
    var ids = ADE.glossaryIds.slice().sort(function (a, b) { return ADE.glossaryTerm(a).localeCompare(ADE.glossaryTerm(b), 'en', { sensitivity: 'base' }); });
    var letters = {}; ids.forEach(function (id) { letters[ADE.glossaryTerm(id).charAt(0).toUpperCase()] = 1; });
    wrap.appendChild(h('nav', { class: 'abc', 'aria-label': ADE.t('app.letters') }, Object.keys(letters).map(function (L) { return h('a', { class: 'chip btn', href: '#', onclick: function (e) { e.preventDefault(); var el = document.getElementById('gl-' + L); if (el) el.scrollIntoView(); }, text: L }); })));
    var dl = h('dl', { class: 'gloss' }), lastL = '';
    ids.forEach(function (id) {
      var term = ADE.glossaryTerm(id), L = term.charAt(0).toUpperCase();
      if (L !== lastL) { lastL = L; dl.appendChild(h('div', { class: 'gl-letter', id: 'gl-' + L }, h('h2', { text: L }))); }
      var meta = (ADE.glossaryMeta[ADE.lang] || {})[id] || {}, ref = meta.chapter && ADE.resolveRef(meta.chapter);
      dl.appendChild(h('div', { class: 'gl-item', id: 'glo-' + id }, h('dt', { lang: 'en', translate: 'no', text: term }), h('dd', null, h('span', { class: 'prose', html: ADE.markup(ADE.t(ADE.glossaryKey(id, 'def'))) }),
        ref && ref.chapter ? h('a', { class: 'chip', href: href(ref.track.id + '/' + ref.chapter.id), text: ADE.t('app.intro') + ': ' + ADE.t(ref.chapter.titleKey) }) : null)));
    });
    wrap.appendChild(dl);
    return wrap;
  }
  function srcItem(s) {
    var viOnlyEn = ADE.lang === 'vi' && (s.lang || 'en') === 'en';
    return h('li', { class: 'src-item panel', id: 'src-' + s.id },
      h('div', { class: 'pad' },
        h('h3', null, h('a', { href: s.url, target: '_blank', rel: 'noopener noreferrer', text: s.title }), viOnlyEn ? h('small', { class: 'muted', text: ' ' + ADE.t('app.englishOnly') }) : null),
        h('p', { class: 'hint' }, s.org + ' · ', h('span', { class: 'url', translate: 'no', text: s.url })),
        s.label ? ui.badge(s.label) : null,
        s.supports ? h('p', { class: 'prose', text: s.supports[ADE.lang] || s.supports.vi }) : null));
  }
  function pageSources(r) {
    setTitle(ADE.t('app.nav.sources'));
    var wrap = stdPage(ADE.t('app.nav.sources'), []);
    wrap.appendChild(para(ADE.t('app.srcIntro')));
    var v = ADE.versions;
    if (v) {
      var dl = h('dl', { class: 'ver-list' });
      v.items.forEach(function (it) { dl.appendChild(h('div', null, h('dt', { text: it.name }), h('dd', { translate: 'no', text: it.value }), it.note ? h('dd', { class: 'hint', text: it.note[ADE.lang] || it.note.vi }) : null)); });
      wrap.appendChild(h('section', { class: 'panel versions' }, h('header', { class: 'panel-h' }, h('h2', { class: 'caps', text: ADE.t('app.versions') }), h('span', { class: 'chip', translate: 'no', text: v.date })), h('div', { class: 'pad' }, dl)));
    }
    var groups = [], map = {};
    ADE.sourceList.forEach(function (s) {
      var gk = s.pageOnly ? '~inspiration' : (s.tracks && s.tracks.length === 1 ? s.tracks[0] : (s.tracks && s.tracks.length ? '~multi' : '~shared'));
      if (!map[gk]) { map[gk] = []; groups.push(gk); }
      map[gk].push(s);
    });
    var gOrder = function (g) { var t = ADE.getTrack(g); return t ? t.order : { '~multi': 1000, '~shared': 1100, '~inspiration': 1200 }[g] || 1150; };
    groups.sort(function (a, b) { return gOrder(a) - gOrder(b); });
    groups.forEach(function (gk) {
      var t = ADE.getTrack(gk);
      var title = t ? ADE.t(t.titleKey) : ADE.t('app.srcGroup.' + gk.slice(1));
      var ul = h('ul', { class: 'src-list' }); map[gk].forEach(function (s) { ul.appendChild(srcItem(s)); });
      // chữ hoa chỉ cho tiêu đề ngắn (≤ 40 ký tự, STYLE-REFERENCE 4.3); tên track dài giữ chữ thường
      wrap.appendChild(h('section', null, h('h2', { class: (title.length <= 40 ? 'caps ' : '') + 'sec-h', text: title }), ul));
    });
    return wrap;
  }
  function pageAbout() {
    setTitle(ADE.t('app.nav.about'));
    var wrap = stdPage(ADE.t('app.nav.about'), []);
    ADE.keysUnder('shared.about.sec').forEach(function (s) {
      var pre = 'shared.about.sec.' + s, tt = ADE.t(pre + '.title');
      var body = h('div', { class: 'pad' });
      ADE.keysUnder(pre + '.p').forEach(function (n) { body.appendChild(para(ADE.t(pre + '.p.' + n))); });
      if (s === 'labels') {
        var ul = h('ul', { class: 'labels-list' });
        ['stable', 'impl', 'android-impl', 'version', 'experimental', 'guideline', 'simplified', 'normative', 'research', 'ds-guideline', 'author-framework', 'quant-model'].forEach(function (b) {
          ul.appendChild(h('li', null, ui.badge(b), h('span', { class: 'prose', text: ADE.t('shared.about.label.' + b) })));
        });
        body.appendChild(ul);
      }
      if (s === 'diagrams') {
        body.appendChild(ui.callout('mechanism', ADE.tm('shared.about.co.mechanism')));
        body.appendChild(ui.callout('pitfall', ADE.tm('shared.about.co.pitfall')));
        body.appendChild(ui.callout('android', ADE.tm('shared.about.co.android')));
        body.appendChild(ui.callout('source', ADE.tm('shared.about.co.source')));
        body.appendChild(ui.callout('try', ADE.tm('shared.about.co.try')));
      }
      wrap.appendChild(h('section', { class: 'panel sec' }, h('header', { class: 'panel-h' }, h('h2', { class: ui.caps(tt), text: tt })), body));
    });
    return wrap;
  }
  function pageSearch(r) {
    var q = r.query.q || '';
    setTitle(ADE.t('app.search'));
    var wrap = stdPage(ADE.t('app.search'), []);
    var input = h('input', { type: 'search', class: 'search-input', value: q, 'aria-label': ADE.t('app.search'), placeholder: ADE.t('app.searchPlaceholder') });
    input.addEventListener('keydown', function (e) { if (e.key === 'Enter') ADE.router.go({ page: 'search', query: { q: input.value } }); });
    wrap.appendChild(input);
    var res = q ? ADE.search.query(q) : [];
    wrap.appendChild(h('p', { class: 'hint', role: 'status', text: q ? ADE.t('app.resultCount', { n: res.length }) : ADE.t('app.searchHint') }));
    var ul = h('ul', { class: 'results page-results' });
    res.forEach(function (o) { ul.appendChild(h('li', { class: 'res' }, h('a', { href: o.href }, h('span', { class: 'rt', text: ADE.t('app.type.' + o.type) }), h('b', { text: o.title }), o.meta ? h('span', { class: 'rm', text: o.meta }) : null, o.snippet ? h('span', { class: 'rs', text: o.snippet.slice(0, 160) }) : null))); });
    wrap.appendChild(ul);
    return wrap;
  }
  function pageNotFound() {
    setTitle(ADE.t('app.notFound'));
    return stdPage(ADE.t('app.notFound'), [para(ADE.t('app.notFoundDesc')), h('a', { class: 'btn primary', href: href('') }, h('span', { text: ADE.t('app.home') }))]);
  }

  /* ================= khởi động ================= */
  function boot() {
    initPrefs();
    ADE.validateAll();
    ADE.setLang(ADE.initLang(ADE.router.parse().lang), true);
    buildChrome();
    ADE.controls.global({ openSearch: function () { ADE.search.openDialog(); }, openHelp: openHelp, closeDrawer: function () { if (!drawer.hidden) toggleDrawer(false); } });
    ADE.router.onChange(handleRoute);
    ADE.router.start();
    if (ADE.dev) {
      var bad = ADE.errors.filter(function (e) { return e.level === 'error'; });
      if (bad.length) console.warn('[ADE] ' + bad.length + ' lỗi đăng ký, xem dev/report.html');
    }
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot); else boot();
})();
