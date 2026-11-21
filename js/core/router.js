/* router.js — hash routing có tiền tố ngôn ngữ.
   #/<lang>/                                   trang chủ
   #/<lang>/<trackId>                          tổng quan track
   #/<lang>/<trackId>/<chapterId>[/<step>]     chương (step: 0 = tổng quan, 1..N = bước, N+1 = tổng kết)
   #/<lang>/live?preset=<id>&step=<n>          Live Explorer
   #/<lang>/misconceptions[/<id>] · glossary[/<id>] · sources[/<id>] · about · search?q=
   Thiếu <lang> → chuyển sang ngôn ngữ đã lưu (mặc định vi). Bước đổi bằng replaceState (không chất đầy lịch sử);
   điều hướng giữa các trang dùng hashchange nên Back/Forward hoạt động. */
(function () {
  'use strict';
  var ADE = window.ADE = window.ADE || {};
  var PAGES = ['live', 'misconceptions', 'glossary', 'sources', 'about', 'search'];
  var listeners = [];

  function parse(hash) {
    var raw = (hash || location.hash || '').replace(/^#\/?/, '');
    var qi = raw.indexOf('?'), qs = qi >= 0 ? raw.slice(qi + 1) : '', path = qi >= 0 ? raw.slice(0, qi) : raw;
    var q = {};
    qs.split('&').forEach(function (kv) { if (!kv) return; var p = kv.split('='); q[decodeURIComponent(p[0])] = decodeURIComponent((p[1] || '').replace(/\+/g, ' ')); });
    var parts = path.split('/').filter(function (x) { return x !== ''; }).map(decodeURIComponent);
    var r = { lang: null, page: 'home', query: q, raw: raw };
    if (parts.length && ADE.langs.indexOf(parts[0]) >= 0) r.lang = parts.shift();
    if (!parts.length) return r;
    if (PAGES.indexOf(parts[0]) >= 0) { r.page = parts[0]; r.id = parts[1] || null; return r; }
    r.page = 'track'; r.track = parts[0]; r.chapter = parts[1] || null;
    r.step = parts[2] !== undefined && /^\d+$/.test(parts[2]) ? parseInt(parts[2], 10) : null;
    return r;
  }
  function build(r) {
    var p = '#/' + (r.lang || ADE.lang) + '/';
    if (r.page === 'track') p += encodeURIComponent(r.track) + (r.chapter ? '/' + encodeURIComponent(r.chapter) + (r.step != null ? '/' + r.step : '') : '');
    else if (r.page !== 'home') p += r.page + (r.id ? '/' + encodeURIComponent(r.id) : '');
    var qs = Object.keys(r.query || {}).filter(function (k) { return r.query[k] !== '' && r.query[k] != null; }).map(function (k) { return encodeURIComponent(k) + '=' + encodeURIComponent(r.query[k]); }).join('&');
    return p + (qs ? '?' + qs : '');
  }
  function replace(hash) {
    try { history.replaceState(null, '', hash); }
    catch (e) { /* một số môi trường chặn replaceState trên file:// → bỏ qua, URL không đổi nhưng ứng dụng vẫn chạy */ }
  }
  function onChange(fn) { listeners.push(fn); }
  function fire() { var r = parse(); listeners.forEach(function (f) { f(r); }); }
  function start() {
    window.addEventListener('hashchange', function () {
      var r = parse();
      if (!r.lang) { r.lang = ADE.initLang(null); replace(build(r)); r = parse(); }
      fire();
    });
    var r = parse();
    if (!r.lang) { r.lang = ADE.initLang(null); replace(build(r)); }
    fire();
  }
  // Đổi ngôn ngữ: giữ nguyên mọi phần còn lại của route; không tải lại.
  function withLang(lang) { var r = parse(); r.lang = lang; return build(r); }
  function go(r) { location.hash = build(r); }

  ADE.router = { parse: parse, build: build, replace: replace, onChange: onChange, start: start, withLang: withLang, go: go, PAGES: PAGES };
})();
