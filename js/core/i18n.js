/* i18n.js — namespace window.ADE, kho chuỗi song ngữ, t(), markup, store, tuỳ chọn chuyển động.
   Quy tắc (docs/research/global.md mục 4):
   - Chuỗi lưu PHẲNG theo khoá chấm; addStrings từ chối khoá trùng và khoá ngoài vùng cho phép.
   - Mọi chuỗi ở dạng Unicode NFC (report kiểm tra).
   - Lõi không biết id track nào. */
(function () {
  'use strict';
  var ADE = window.ADE = window.ADE || {};
  ADE.version = '0.1.0';
  ADE.langs = ['vi', 'en'];            // thêm ngôn ngữ mới: thêm mã vào đây (xem README)
  ADE.defaultLang = 'vi';
  ADE.lang = ADE.defaultLang;
  ADE.errors = [];                     // {level:'error'|'warn', area, msg}
  ADE.err = function (level, area, msg) { ADE.errors.push({ level: level, area: area, msg: msg }); };
  ADE.dev = /[?&]dev=1/.test(location.search);

  /* ---------- store: localStorage có tiền tố 'ade.', bọc try/catch ---------- */
  var mem = {};
  ADE.store = {
    get: function (k, d) {
      try {
        var v = window.localStorage.getItem('ade.' + k);
        if (v === null) return k in mem ? mem[k] : d;
        return JSON.parse(v);
      } catch (e) { return k in mem ? mem[k] : d; }
    },
    set: function (k, v) {
      mem[k] = v;
      try { window.localStorage.setItem('ade.' + k, JSON.stringify(v)); } catch (e) { /* storage không dùng được: giữ trong bộ nhớ */ }
    },
    remove: function (k) {
      delete mem[k];
      try { window.localStorage.removeItem('ade.' + k); } catch (e) { /* bỏ qua */ }
    }
  };

  /* ---------- chuyển động ---------- */
  // ade.motion: 'reduce' | 'full' | null (theo hệ điều hành)
  ADE.motionReduced = function () { return document.documentElement.classList.contains('reduced-motion'); };
  ADE.diagramOnly = function () { return document.documentElement.classList.contains('diagram-only'); };

  /* ---------- kho chuỗi ---------- */
  ADE.strings = {};
  ADE.langs.forEach(function (l) { ADE.strings[l] = {}; });
  var keyCache = {};
  var UI_SCOPES = ['app.', 'job.', 'phase.', 'step.', 'badge.', 'a11y.', 'domain.'];

  ADE.addStrings = function (lang, obj, scopes, origin) {
    if (!ADE.strings[lang]) { ADE.err('error', 'i18n', 'Ngôn ngữ không hỗ trợ: ' + lang); return; }
    var dst = ADE.strings[lang];
    Object.keys(obj).forEach(function (k) {
      var ok = scopes.some(function (p) { return k.indexOf(p) === 0; });
      if (!ok) { ADE.err('error', 'i18n', '[' + (origin || '?') + '/' + lang + '] khoá ngoài vùng cho phép: ' + k); return; }
      if (Object.prototype.hasOwnProperty.call(dst, k)) { ADE.err('error', 'i18n', '[' + lang + '] khoá trùng: ' + k); return; }
      dst[k] = obj[k];
    });
    keyCache = {};
  };
  ADE.addUiStrings = function (lang, obj) { ADE.addStrings(lang, obj, UI_SCOPES, 'ui'); };
  ADE.addSharedStrings = function (lang, obj) { ADE.addStrings(lang, obj, ['shared.'], 'shared'); };
  ADE.addTrackStrings = function (trackId, lang, obj) { ADE.addStrings(lang, obj, ['track.' + trackId + '.'], 'track:' + trackId); };

  ADE.hasKey = function (key, lang) { return Object.prototype.hasOwnProperty.call(ADE.strings[lang || ADE.lang] || {}, key); };

  // Các khoá con trực tiếp dưới một tiền tố, theo thứ tự khai báo (lấy từ bản vi làm chuẩn, bổ sung từ ngôn ngữ hiện tại).
  ADE.keysUnder = function (prefix) {
    var ck = prefix;
    if (keyCache[ck]) return keyCache[ck];
    var seen = {}, out = [], p = prefix + '.';
    [ADE.defaultLang, ADE.lang].forEach(function (l) {
      Object.keys(ADE.strings[l] || {}).forEach(function (k) {
        if (k.indexOf(p) !== 0) return;
        var seg = k.slice(p.length).split('.')[0];
        if (!seen[seg]) { seen[seg] = 1; out.push(seg); }
      });
    });
    keyCache[ck] = out;
    return out;
  };

  /* ---------- số, plural ---------- */
  var nfCache = {}, prCache = {};
  ADE.num = function (n, opts) {
    var id = ADE.lang + JSON.stringify(opts || {});
    if (!nfCache[id]) { try { nfCache[id] = new Intl.NumberFormat(ADE.lang, opts); } catch (e) { nfCache[id] = { format: String }; } }
    return nfCache[id].format(n);
  };
  ADE.pluralCat = function (n) {
    if (!prCache[ADE.lang]) { try { prCache[ADE.lang] = new Intl.PluralRules(ADE.lang); } catch (e) { prCache[ADE.lang] = { select: function () { return 'other'; } }; } }
    return prCache[ADE.lang].select(n);
  };

  /* ---------- t() ---------- */
  var warned = {};
  var SENT_A = '\u2063', SENT_B = '\u2064';
  ADE.stripSentinel = function (s) { return String(s).replace(/[\u2063\u2064]/g, ''); };
  ADE.markMissing = function (root) {
    if (!root) return;
    var w = document.createTreeWalker(root, NodeFilter.SHOW_TEXT, null), hit = [], n;
    while ((n = w.nextNode())) if (n.nodeValue.indexOf(SENT_A) >= 0) hit.push(n);
    hit.forEach(function (t) {
      var frag = document.createDocumentFragment(), re = /\u2063([^\u2064]*)\u2064/g, last = 0, m, v = t.nodeValue;
      while ((m = re.exec(v))) {
        if (m.index > last) frag.appendChild(document.createTextNode(v.slice(last, m.index)));
        var sp = document.createElement('span'); sp.className = 'i18n-missing'; sp.textContent = m[1]; frag.appendChild(sp);
        last = re.lastIndex;
      }
      if (last < v.length) frag.appendChild(document.createTextNode(v.slice(last)));
      t.parentNode.replaceChild(frag, t);
    });
    [].forEach.call(root.querySelectorAll('[aria-label],[title],[placeholder],[alt]'), function (el) {
      ['aria-label', 'title', 'placeholder', 'alt'].forEach(function (a) {
        var v = el.getAttribute(a);
        if (v && /[\u2063\u2064]/.test(v)) { el.setAttribute(a, ADE.stripSentinel(v)); el.classList.add('i18n-missing'); }
      });
    });
  };
  function lookup(key, params) {
    var tryKeys = [key];
    if (params && typeof params.n === 'number') tryKeys = [key + '.' + ADE.pluralCat(params.n), key + '.other', key];
    var langs = [ADE.lang];
    if (ADE.lang !== ADE.defaultLang) langs.push(ADE.defaultLang);
    for (var li = 0; li < langs.length; li++) {
      for (var i = 0; i < tryKeys.length; i++) {
        var s = ADE.strings[langs[li]][tryKeys[i]];
        if (typeof s === 'string') return { text: s, missing: li > 0 };
      }
    }
    return null;
  }
  ADE.tx = function (key, params) {
    var r = lookup(key, params);
    if (!r) {
      if (ADE.dev && !warned[key]) { warned[key] = 1; console.warn('[ADE] thiếu khoá:', key); }
      return { text: key, missing: true };
    }
    if (r.missing && ADE.dev && !warned[ADE.lang + key]) { warned[ADE.lang + key] = 1; console.warn('[ADE] thiếu khoá ở ' + ADE.lang + ':', key); }
    r.text = r.text.replace(/\{(\w+)\}/g, function (m, name) {
      if (!params || !(name in params)) return m;
      var v = params[name];
      return typeof v === 'number' ? ADE.num(v) : String(v);
    });
    // chuỗi rơi về bản vi: đánh dấu bằng ký tự vô hình; ADE.markMissing() bọc thành span.i18n-missing sau khi render
    if (r.missing) r.text = SENT_A + r.text + SENT_B;
    return r;
  };
  ADE.t = function (key, params) { return ADE.tx(key, params).text; };

  /* ---------- markup: [[term:id]] [[src:id]] [[badge:key]] `code` ---------- */
  ADE.esc = function (s) {
    return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  };
  ADE.markup = function (str) {
    var codes = [];
    var s = ADE.esc(str).replace(/`([^`]+)`/g, function (m, c) { codes.push(c); return '\u0000' + (codes.length - 1) + '\u0000'; });
    s = s.replace(/\[\[(term|src|badge):([A-Za-z0-9_.\-]+)\]\]/g, function (m, kind, id) {
      if (kind === 'term') {
        var termText = ADE.glossaryTerm ? ADE.glossaryTerm(id) : null;
        if (termText === null) return '<span class="term term-missing" lang="en">' + ADE.esc(id) + '</span>';
        return '<a class="term" href="#/' + ADE.lang + '/glossary/' + encodeURIComponent(id) + '"' + (ADE.lang !== 'en' ? ' lang="en"' : '') + '>' + ADE.esc(termText) + '</a>';
      }
      if (kind === 'src') {
        var src = ADE.sources && ADE.sources[id];
        var title = src ? src.title : id;
        var cls = src ? 'src' : 'src src-missing';
        return '<a class="' + cls + '" href="#/' + ADE.lang + '/sources/' + encodeURIComponent(id) + '" title="' + ADE.esc(title) + '" aria-label="' + ADE.esc(ADE.t('app.sourceOf', { title: title })) + '">' +
          (ADE.diagram && ADE.diagram.icon ? ADE.diagram.icon('source', { size: 13 }) : '[src]') + '</a>';
      }
      var bl = ADE.t('badge.' + id);
      return '<span class="badge badge-' + id.replace(/[^a-z\-]/g, '') + '">' + ADE.esc(bl) + '</span>';
    });
    s = s.replace(/\u0000(\d+)\u0000/g, function (m, i) { return '<code translate="no">' + codes[+i] + '</code>'; });
    return s;
  };
  // Trả về chuỗi đã bản địa hoá và render markup (HTML an toàn).
  ADE.tm = function (key, params) { return ADE.markup(ADE.t(key, params)); };

  /* ---------- đổi ngôn ngữ ---------- */
  var langListeners = [];
  ADE.onLang = function (fn) { langListeners.push(fn); };
  ADE.setLang = function (lang, silent) {
    if (ADE.langs.indexOf(lang) < 0) lang = ADE.defaultLang;
    ADE.lang = lang;
    document.documentElement.lang = lang;     // WCAG 3.1.1
    ADE.store.set('lang', lang);
    if (!silent) langListeners.forEach(function (f) { f(lang); });
  };
  ADE.initLang = function (hashLang) {
    var l = hashLang;
    if (ADE.langs.indexOf(l) < 0) l = ADE.store.get('lang', ADE.defaultLang);
    if (ADE.langs.indexOf(l) < 0) l = ADE.defaultLang;
    ADE.lang = l;
    document.documentElement.lang = l;
    return l;
  };
})();
