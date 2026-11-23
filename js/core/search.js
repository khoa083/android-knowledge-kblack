/* search.js — tìm kiếm phía client theo ngôn ngữ hiện tại: track, chương, glossary, hiểu lầm, preset.
   So khớp không phân biệt hoa thường và không phân biệt dấu (để gõ "ung dung" vẫn ra "ứng dụng"). */
(function () {
  'use strict';
  var ADE = window.ADE = window.ADE || {};

  function norm(s) {
    return String(s).normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/đ/g, 'd').replace(/Đ/g, 'D').toLowerCase();
  }
  var cache = null, cacheLang = '';
  function strip(s) { return String(s).replace(/\[\[(term|src|badge):[^\]]*\]\]/g, '').replace(/`/g, ''); }

  function build() {
    var L = ADE.lang, out = [], href = function (p) { return '#/' + L + '/' + p; };
    ADE.tracks.forEach(function (t) {
      var tt = ADE.t(t.titleKey);
      out.push({ type: 'track', title: tt, text: tt + ' ' + ADE.t(t.summaryKey), href: href(t.id), meta: ADE.domainLabel(t.domain) });
      if (!ADE.trackOpen(t)) return;   // track tạm đóng: chỉ tìm được trang track
      t.chapters.forEach(function (c) {
        var ct = ADE.t(c.titleKey), es = ADE.t(ADE.chapterKey(t.id, c.id, 'essence'));
        out.push({ type: 'chapter', title: ct, text: ct + ' ' + strip(es), snippet: strip(es), href: href(t.id + '/' + c.id), meta: tt });
      });
      t.presets.forEach(function (p) { var pt = ADE.t(p.titleKey); out.push({ type: 'preset', title: pt, text: pt, href: href('live?preset=' + p.id), meta: tt }); });
    });
    ADE.glossaryIds.forEach(function (id) {
      var term = ADE.glossaryTerm(id), def = ADE.t(ADE.glossaryKey(id, 'def'));
      out.push({ type: 'term', title: term, text: term + ' ' + strip(def), snippet: strip(def), href: href('glossary/' + id), meta: '' });
    });
    ADE.misIds.forEach(function (id) {
      var w = ADE.t(ADE.misKey(id, 'wrong')), r = ADE.t(ADE.misKey(id, 'right'));
      out.push({ type: 'mis', title: w, text: w + ' ' + strip(r), snippet: strip(r), href: href('misconceptions/' + id), meta: '' });
    });
    out.forEach(function (o) { o.n = norm(o.text); o.nt = norm(o.title); });
    return out;
  }

  function query(q) {
    if (!cache || cacheLang !== ADE.lang) { cache = build(); cacheLang = ADE.lang; }
    var words = norm(q).split(/\s+/).filter(Boolean);
    if (!words.length) return [];
    var res = [];
    cache.forEach(function (o) {
      var score = 0;
      for (var i = 0; i < words.length; i++) {
        var w = words[i], inT = o.nt.indexOf(w), inB = o.n.indexOf(w);
        if (inB < 0) return;
        score += (inT === 0 ? 6 : inT > 0 ? 4 : 1) + (o.type === 'chapter' || o.type === 'track' ? 1 : 0);
      }
      res.push({ o: o, score: score });
    });
    res.sort(function (a, b) { return b.score - a.score || a.o.title.length - b.o.title.length; });
    return res.map(function (r) { return r.o; });
  }
  function invalidate() { cache = null; }

  function openDialog(initial) {
    var h = ADE.ui.h, results = [], active = 0;
    var input = h('input', { type: 'search', class: 'search-input', placeholder: ADE.t('app.searchPlaceholder'), 'aria-label': ADE.t('app.search'), autocomplete: 'off', value: initial || '' });
    var list = h('ul', { class: 'results', role: 'listbox', 'aria-label': ADE.t('app.results') });
    var status = h('p', { class: 'hint', role: 'status' });
    var body = h('div', { class: 'search-box' }, input, status, list);
    var dlg = ADE.ui.dialog(ADE.t('app.search'), body, { cls: 'dlg-search' });
    function go(o) { dlg.close(); location.hash = o.href; }
    function draw() {
      ADE.ui.clear(list);
      results = input.value.trim() ? query(input.value).slice(0, 30) : [];
      active = 0;
      status.textContent = input.value.trim() ? ADE.t('app.resultCount', { n: results.length }) : ADE.t('app.searchHint');
      results.forEach(function (o, i) {
        var li = h('li', { role: 'option', id: 'sr-' + i, 'aria-selected': i === 0 ? 'true' : 'false', class: 'res' + (i === 0 ? ' on' : '') },
          h('a', { href: o.href, onclick: function (e) { e.preventDefault(); go(o); } }, h('span', { class: 'rt', text: ADE.t('app.type.' + o.type) }), h('b', { text: o.title }), o.meta ? h('span', { class: 'rm', text: o.meta }) : null, o.snippet ? h('span', { class: 'rs', text: o.snippet.slice(0, 110) }) : null));
        list.appendChild(li);
      });
    }
    function mark(i) {
      var items = list.children; if (!items.length) return;
      active = (i + items.length) % items.length;
      [].forEach.call(items, function (li, j) { li.classList.toggle('on', j === active); li.setAttribute('aria-selected', j === active ? 'true' : 'false'); });
      input.setAttribute('aria-activedescendant', 'sr-' + active);
      items[active].scrollIntoView({ block: 'nearest' });
    }
    input.addEventListener('input', draw);
    input.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowDown') { e.preventDefault(); mark(active + 1); }
      else if (e.key === 'ArrowUp') { e.preventDefault(); mark(active - 1); }
      else if (e.key === 'Enter' && results[active]) { e.preventDefault(); go(results[active]); }
    });
    draw(); input.focus();
    return dlg;
  }

  ADE.search = { query: query, openDialog: openDialog, invalidate: invalidate, norm: norm };
})();
