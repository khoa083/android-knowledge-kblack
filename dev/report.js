/* dev/report.js — kiểm tra song ngữ, registry, nguồn, glossary, model (master 6.5). CHỈ cho dev, không liên kết từ giao diện chính. */
(function () {
  'use strict';
  var ADE = window.ADE, h = ADE.ui.h;
  var out = document.getElementById('report');
  var PLURAL = /\.(zero|one|two|few|many|other)$/;
  // URL đã bị thay (docs/research/global.md mục 3.1): không được xuất hiện trong nguồn của site
  var BANNED_URLS = [
    'https://developer.android.com/develop/ui/compose/animation',
    'https://kotlinlang.org/docs/flow.html',
    'https://kotlinlang.org/docs/cancellation-and-timeouts.html'
  ];
  // khoá mà hai ngôn ngữ được phép giống hệt nhau (id mã, tên riêng, ký hiệu)
  var SAME_OK = /(\.code|\.badge|\.col\.n|\.col\.t|^app\.name$|^app\.guided$|^app\.live$|^app\.kind\.|^app\.callout\.|^badge\.(experimental|guideline)$|^badge\.android-impl$|^domain\.(engineering|design)$|^app\.langName\.|\.term$)/;

  var sections = [];
  function section(title, items, note) { sections.push({ title: title, items: items, note: note }); }
  var allErrors = 0, allWarns = 0;
  function row(level, msg) { if (level === 'error') allErrors++; else if (level === 'warn') allWarns++; return { level: level, msg: msg }; }

  /* 1. Song ngữ */
  function bilingual() {
    var items = [], base = function (k) { return k.replace(PLURAL, ''); };
    var sets = {};
    ADE.langs.forEach(function (l) { sets[l] = {}; Object.keys(ADE.strings[l]).forEach(function (k) { sets[l][base(k)] = 1; }); });
    ADE.langs.forEach(function (a) {
      ADE.langs.forEach(function (b) {
        if (a === b) return;
        Object.keys(sets[a]).forEach(function (k) { if (!sets[b][k]) items.push(row('error', 'Khoá có ở ' + a + ' nhưng thiếu ở ' + b + ': ' + k)); });
      });
    });
    ADE.langs.forEach(function (l) {
      Object.keys(ADE.strings[l]).forEach(function (k) {
        var s = ADE.strings[l][k];
        if (typeof s !== 'string' || !s.trim()) items.push(row('error', '[' + l + '] chuỗi rỗng: ' + k));
        else if (s !== s.normalize('NFC')) items.push(row('error', '[' + l + '] không ở dạng NFC: ' + k));
      });
    });
    var a = ADE.strings.vi, b = ADE.strings.en;
    Object.keys(a).forEach(function (k) {
      if (b[k] === undefined || SAME_OK.test(k)) return;
      if (a[k] === b[k] && !/\.(kt|exkt|solkt|fixkt|out|kind|lang)$/.test(k) && /\s/.test(a[k]) && a[k].length > 12) items.push(row('warn', 'Nghi chưa dịch (vi = en): ' + k + ' → "' + a[k].slice(0, 50) + '"'));
    });
    // markup trong hai ngôn ngữ phải khớp: cùng tập [[src:]], [[term:]], [[badge:]]
    var refs = function (s) { var m = String(s).match(/\[\[(?:src|term|badge):[^\]]+\]\]/g) || []; return m.sort().join(' '); };
    Object.keys(a).forEach(function (k) {
      if (b[k] !== undefined && typeof a[k] === 'string' && refs(a[k]) !== refs(b[k])) items.push(row('error', 'Markup [[...]] khác nhau giữa vi và en: ' + k));
    });
    // meta của glossary/hiểu lầm phải khớp
    ['glossaryMeta', 'misMeta'].forEach(function (mk) {
      var m = ADE[mk], ids = Object.keys(m.vi || {});
      ids.forEach(function (id) { if (JSON.stringify(m.vi[id]) !== JSON.stringify((m.en || {})[id])) items.push(row('error', mk + ': ' + id + ' khác nhau giữa vi và en')); });
    });
    // nguồn: ghi chú 'supports' đủ hai ngôn ngữ
    if (!items.length) items.push(row('ok', 'Hai ngôn ngữ có cùng cây khoá (' + Object.keys(sets.vi).length + ' khoá), không rỗng, đều NFC, markup khớp.'));
    section('1. Song ngữ', items);
  }

  /* 2. Registry */
  function registry() {
    var items = [];
    var pending = {}, pendingN = 0;
    ADE.errors.forEach(function (e) {
      var m = /\(track "([^"]+)" chưa đăng ký\)/.exec(e.msg);
      if (e.level === 'warn' && m) { pending[m[1]] = (pending[m[1]] || 0) + 1; pendingN++; return; }
      items.push(row(e.level, '[' + e.area + '] ' + e.msg));
    });
    if (pendingN) items.push(row('warn', pendingN + ' tham chiếu (cầu nối, lộ trình, glossary) trỏ tới track chưa đăng ký — bình thường cho tới khi các phase track thêm chúng: ' + Object.keys(pending).map(function (k) { return k + ' ×' + pending[k]; }).join(', ')));
    items.push(row('ok', ADE.tracks.length + ' track đã đăng ký: ' + ADE.tracks.map(function (t) { return t.id; }).join(', ') + ' · ' + Object.keys(ADE.models).length + ' model · ' + ADE.allPresets().length + ' preset'));
    ADE.reservedIds.forEach(function (id) { var t = { id: id, code: 'X', order: 1, domain: 'd', accent: '#112233', icon: 'chip', titleKey: 'a', summaryKey: 'b', level: 'beginner', estMinutes: 1, status: 'draft', chapters: [{ id: 'c', titleKey: 'x' }], logKinds: [], labels: [], languages: ['vi'] }; var n = ADE.errors.length; ADE.registerTrack(t); var rejected = ADE.errors.length > n; ADE.errors.length = n; if (!rejected) items.push(row('error', 'registerTrack nhận id bị cấm: ' + id)); });
    section('2. Registry (cấu trúc và tham chiếu chéo)', items, 'Gồm ' + ADE.reservedIds.length + ' id bị cấm được thử và phải bị từ chối.');
  }

  /* 3. Nguồn */
  function sources() {
    var items = [], used = {}, missing = {};
    ADE.langs.forEach(function (l) {
      Object.keys(ADE.strings[l]).forEach(function (k) {
        var m, re = /\[\[src:([A-Za-z0-9_.\-]+)\]\]/g;
        while ((m = re.exec(ADE.strings[l][k]))) { used[m[1]] = 1; if (!ADE.sources[m[1]]) missing[l + ':' + k + ' → ' + m[1]] = 1; }
      });
    });
    Object.keys(missing).forEach(function (m) { items.push(row('error', '[[src]] không có trong registry nguồn: ' + m)); });
    ADE.sourceList.forEach(function (s) {
      if (!s.pageOnly && !used[s.id]) items.push(row('warn', 'Nguồn khai báo nhưng chưa được dùng: ' + s.id));
      ADE.langs.forEach(function (l) { if (!s.supports || !s.supports[l] || !String(s.supports[l]).trim()) items.push(row('error', 'Nguồn ' + s.id + ' thiếu ghi chú "hỗ trợ" ở ' + l)); });
      if (BANNED_URLS.indexOf(s.url) >= 0) items.push(row('error', 'Nguồn ' + s.id + ' dùng URL đã bị thay: ' + s.url));
      if (!/^https:\/\//.test(s.url)) items.push(row('error', 'Nguồn ' + s.id + ' có URL không phải https'));
    });
    if (!items.length) items.push(row('ok', ADE.sourceList.length + ' nguồn; mọi [[src]] đều hợp lệ; mọi nguồn có ghi chú ở cả hai ngôn ngữ.'));
    section('3. Nguồn', items);
  }

  /* 4. Glossary */
  function glossary() {
    var items = [];
    ADE.langs.forEach(function (l) {
      Object.keys(ADE.strings[l]).forEach(function (k) {
        var m, re = /\[\[term:([A-Za-z0-9_.\-]+)\]\]/g;
        while ((m = re.exec(ADE.strings[l][k]))) { if (!ADE.glossaryOwner[m[1]]) items.push(row('error', '[[term:' + m[1] + ']] không có mục glossary (' + l + ': ' + k + ')')); }
      });
    });
    ADE.glossaryIds.forEach(function (id) { ADE.langs.forEach(function (l) { ['term', 'def'].forEach(function (f) { if (!ADE.hasKey(ADE.glossaryKey(id, f), l)) items.push(row('error', 'Glossary ' + id + ' thiếu ' + f + ' ở ' + l)); }); }); });
    ADE.misIds.forEach(function (id) { ADE.langs.forEach(function (l) { ['wrong', 'right'].forEach(function (f) { if (!ADE.hasKey(ADE.misKey(id, f), l)) items.push(row('error', 'Hiểu lầm ' + id + ' thiếu ' + f + ' ở ' + l)); }); }); });
    if (!items.length) items.push(row('ok', ADE.glossaryIds.length + ' thuật ngữ, ' + ADE.misIds.length + ' hiểu lầm; mọi [[term]] đều có mục.'));
    section('4. Glossary và hiểu lầm', items);
  }

  /* 5. Model và ví dụ kiểm chứng */
  function models() {
    var items = [];
    Object.keys(ADE.models).forEach(function (id) {
      var def = ADE.models[id];
      if (def.kind !== 'discrete') return;
      // Cấu hình kiểm tra: tích Descartes của mọi select/toggle (tối đa 600 cấu hình), cộng sampleStates do model khai báo (cho model dùng nút thao tác)
      var states = [def.init({})], axes = (def.controls || []).filter(function (c) { return c.type === 'toggle' || c.type === 'select'; });
      var combos = [def.init({})];
      axes.forEach(function (c) {
        var opts = c.type === 'toggle' ? [true, false] : (c.options || []).map(function (o) { return o.value; });
        var next = [];
        combos.forEach(function (st) { opts.forEach(function (v) { next.push(def.act(st, c.action, v)); }); });
        if (next.length <= 600) combos = next;
      });
      states = states.concat(combos).concat(def.sampleStates ? def.sampleStates() : []);
      var seen = {}, n = 0;
      states.forEach(function (st) {
        var steps = def.steps(st);
        steps.forEach(function (sp) {
          ADE.engine.collectKeys(sp).forEach(function (k) {
            n++;
            if (!ADE.engine.looksLikeKey(k)) items.push(row('error', id + ': trường *Key chứa câu chữ thay vì khoá: "' + String(k).slice(0, 40) + '"'));
            ADE.langs.forEach(function (l) { var kk = l + k; if (!seen[kk] && !ADE.hasKey(k, l) && !ADE.hasKey(k + '.other', l)) { seen[kk] = 1; items.push(row('error', id + ': thiếu khoá ' + k + ' ở ' + l)); } });
          });
          (sp.logEvents || []).forEach(function (e) { if (!ADE.kinds[e.kind]) items.push(row('error', id + ': logEvent kind chưa định nghĩa: ' + e.kind)); });
        });
      });
      ['titleKey', 'overviewKey', 'wrapupKey'].concat((def.simplificationKeys || []).map(function () { return 'x'; })).forEach(function (f) {
        if (f === 'x') return; if (def[f]) ADE.langs.forEach(function (l) { if (!ADE.hasKey(def[f], l)) items.push(row('error', id + ': thiếu ' + def[f] + ' ở ' + l)); });
      });
      (def.simplificationKeys || []).forEach(function (k) { ADE.langs.forEach(function (l) { if (!ADE.hasKey(k, l)) items.push(row('error', id + ': thiếu ' + k + ' ở ' + l)); }); });
      var vw = ADE.views[id];
      if (!vw) items.push(row('warn', id + ': chưa có view (sơ đồ)'));
      else vw.nodes.forEach(function (nd) { ADE.langs.forEach(function (l) { if (!ADE.hasKey(nd.labelKey, l)) items.push(row('error', id + ': thiếu nhãn node ' + nd.labelKey + ' ở ' + l)); }); });
      items.push(row('ok', id + ': ' + states.length + ' cấu hình, ' + n + ' khoá được phát ra đều hợp lệ ở hai ngôn ngữ.'));
    });
    ADE.engine.runChecks().forEach(function (r) { items.push(row(r.pass ? 'ok' : 'error', (r.pass ? 'PASS' : 'FAIL') + ' · ' + r.id + (r.detail ? ' (' + r.detail + ')' : ''))); });
    section('5. Model và ví dụ kiểm chứng', items);
  }

  function render() {
    bilingual(); registry(); sources(); glossary(); models();
    out.appendChild(h('p', { class: 'summary ' + (allErrors ? 'bad' : 'good') }, allErrors ? '✗ ' + allErrors + ' lỗi, ' + allWarns + ' cảnh báo' : '✓ Không có lỗi. ' + allWarns + ' cảnh báo.'));
    sections.forEach(function (s) {
      var ul = h('ul', { class: 'rpt' });
      s.items.forEach(function (r) { ul.appendChild(h('li', { class: r.level }, h('b', { text: { ok: '✓', error: '✗', warn: '!' }[r.level] }), ' ', r.msg)); });
      out.appendChild(h('section', { class: 'panel' }, h('header', { class: 'panel-h' }, h('h2', { class: 'caps', text: s.title })), h('div', { class: 'pad' }, s.note ? h('p', { class: 'hint', text: s.note }) : null, ul)));
    });
    ui();
  }

  /* 6. Mẫu giao diện để kiểm tra bằng mắt (font tiếng Việt viết hoa, badge, callout, khung điện thoại) */
  function ui() {
    var U = ADE.ui, box = h('div', { class: 'pad' });
    var test = 'TIẾNG VIỆT · ỨNG DỤNG · ĐỒNG THỜI · HỦY BỎ · CẬP NHẬT · NHẬT KÝ SỰ KIỆN';
    box.appendChild(h('p', { class: 'hint', text: 'Chuỗi kiểm tra dấu tiếng Việt khi viết hoa (STYLE-REFERENCE 4.3), line-height ≥ 1.3, dùng font monospace hệ thống:' }));
    box.appendChild(h('p', { class: 'caps', id: 'vn-caps', style: 'font-size:14px', text: test }));
    box.appendChild(h('p', { class: 'caps', style: 'font-size:22px;font-weight:800', text: 'Ứng dụng đồng thời · Hủy bỏ' }));
    box.appendChild(h('p', { id: 'vn-lower', text: 'tiếng Việt: ứng dụng, đồng thời, hủy bỏ, cập nhật, nhật ký sự kiện' }));
    var kinds = h('div', { class: 'chips' }); Object.keys(ADE.kinds).forEach(function (k) { kinds.appendChild(U.kindChip('', k)); });
    box.appendChild(h('h3', { class: 'caps sub', text: 'Loại sự kiện' })); box.appendChild(kinds);
    var bd = h('div', { class: 'badges' }); ['stable', 'impl', 'android-impl', 'version', 'experimental', 'guideline', 'simplified', 'normative', 'research', 'ds-guideline', 'author-framework', 'quant-model'].forEach(function (b) { bd.appendChild(U.badge(b)); });
    box.appendChild(h('h3', { class: 'caps sub', text: 'Nhãn' })); box.appendChild(bd);
    var sb = h('div', { class: 'chips' }); ['scenario', 'mechanism', 'experiment', 'pitfall', 'android', 'wrapup'].forEach(function (s) { sb.appendChild(U.stepBadge(s)); });
    box.appendChild(h('h3', { class: 'caps sub', text: 'Loại bước' })); box.appendChild(sb);
    box.appendChild(h('h3', { class: 'caps sub', text: 'Callout' }));
    ['mechanism', 'pitfall', 'android', 'source', 'try'].forEach(function (k) { box.appendChild(U.callout(k, ADE.markup('Nội dung mẫu với `code` và [[term:event-log]].'))); });
    box.appendChild(h('h3', { class: 'caps sub', text: 'Khung điện thoại mẫu' }));
    box.appendChild(U.mockFrame(h('div', null, h('h4', { text: ADE.t('app.sample') }), h('p', { text: 'Nội dung minh họa trong khung.' }))));
    var ics = h('div', { class: 'chips' }); Object.keys(ADE.diagram.ICONS).forEach(function (n) { ics.appendChild(h('span', { class: 'chip', title: n }, U.icon(n, { size: 20 }), n)); });
    box.appendChild(h('h3', { class: 'caps sub', text: 'Bộ icon tự vẽ' })); box.appendChild(ics);
    out.appendChild(h('section', { class: 'panel' }, h('header', { class: 'panel-h' }, h('h2', { class: 'caps', text: '6. Mẫu giao diện (kiểm tra bằng mắt)' })), box));
  }

  // thanh công cụ của trang report
  var bar = document.getElementById('rbar');
  bar.appendChild(h('button', { class: 'btn', type: 'button', onclick: function () { var d = document.documentElement; d.setAttribute('data-theme', d.getAttribute('data-theme') === 'dark' ? 'light' : 'dark'); } }, 'Light / Dark'));
  ADE.langs.forEach(function (l) { bar.appendChild(h('button', { class: 'btn', type: 'button', onclick: function () { ADE.setLang(l, true); location.reload(); } }, 'Mẫu giao diện: ' + l)); });
  ADE.validateAll();
  ADE.setLang(ADE.store.get('lang', 'vi'), true);
  render();
})();
