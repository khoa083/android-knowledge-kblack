/* registry.js — đăng ký track, model, view, mã, nguồn, glossary, hiểu lầm, cầu nối, lộ trình.
   Lõi KHÔNG chứa id track nào: mọi thứ đi qua registerTrack().
   Kiểm tra hai giai đoạn: registerTrack() kiểm cấu trúc; ADE.validateAll() kiểm tham chiếu chéo sau khi mọi script đã nạp. */
(function () {
  'use strict';
  var ADE = window.ADE = window.ADE || {};

  // Id bị cấm: tiền tố khoá chung (master 6.3) + tên trang của router.
  var RESERVED_PREFIX = ['app', 'track', 'job', 'phase', 'step', 'badge', 'a11y', 'domain', 'shared'];
  var RESERVED_ROUTES = ['live', 'misconceptions', 'glossary', 'sources', 'about', 'search', 'dev'];
  ADE.reservedIds = RESERVED_PREFIX.concat(RESERVED_ROUTES);

  var LEVELS = ['beginner', 'intermediate', 'advanced'];
  var STATUSES = ['stable', 'draft'];

  ADE.tracks = [];
  ADE.trackMap = {};
  ADE.models = {};
  ADE.views = {};
  ADE.code = {};
  ADE.sources = {};
  ADE.sourceList = [];
  ADE.versions = null;
  ADE.bridgeList = [];
  ADE.bridgeMap = {};
  ADE.pathList = [];
  ADE.glossaryOwner = {};
  ADE.glossaryMeta = {};
  ADE.glossaryIds = [];
  ADE.misOwner = {};
  ADE.misMeta = {};
  ADE.misIds = [];

  /* ---------- loại sự kiện (kind): màu = token ngữ nghĩa, icon tự vẽ ---------- */
  ADE.kinds = {};
  ADE.defineKind = function (kind, def) { ADE.kinds[kind] = def; };
  [
    ['launch', 'coroutine', 'play'], ['suspend', 'thread', 'pause'], ['resume', 'coroutine', 'resume'],
    ['cancel', 'cancel', 'forbidden'], ['complete', 'job', 'check'], ['exception', 'error', 'cross'],
    ['emit', 'flow', 'diamond'], ['collect', 'flow', 'diamondo'], ['write', 'state', 'square'],
    ['invalidate', 'signal', 'bolt'], ['schedule', 'runtime', 'clock'], ['recompose', 'runtime', 'refresh'],
    ['skip', 'thread', 'skip'], ['apply', 'ui', 'check'], ['layout', 'ui', 'grid'], ['draw', 'ui', 'halfcircle'],
    ['target-change', 'state', 'target'], ['frame', 'anim', 'frame'], ['interrupt', 'cancel', 'bolt'],
    ['settle', 'job', 'dot'], ['observe', 'ui', 'eye'], ['act', 'state', 'triangle'], ['error', 'error', 'cross'],
    ['feedback', 'signal', 'spark'], ['decide', 'runtime', 'diamond'], ['measure', 'anim', 'clock'],
    ['recover', 'job', 'refresh']
  ].forEach(function (k) { ADE.defineKind(k[0], { tok: k[1], icon: k[2] }); });

  ADE.kindLabel = function (trackId, kind) {
    var k = 'track.' + trackId + '.kind.' + kind;
    if (trackId && ADE.hasKey(k)) return ADE.t(k);
    return ADE.t('app.kind.' + kind);
  };

  /* ---------- track ---------- */
  function fail(m, msg) { ADE.err('error', 'registry', 'Track "' + (m && m.id) + '": ' + msg); return false; }

  ADE.registerTrack = function (m) {
    if (!m || typeof m !== 'object') return fail(m, 'manifest không hợp lệ');
    var req = ['id', 'code', 'order', 'domain', 'accent', 'icon', 'titleKey', 'summaryKey', 'level', 'estMinutes', 'status', 'chapters', 'logKinds', 'labels', 'languages'];
    for (var i = 0; i < req.length; i++) if (m[req[i]] === undefined || m[req[i]] === null) return fail(m, 'thiếu trường bắt buộc "' + req[i] + '"');
    if (!/^[a-z][a-z0-9-]*$/.test(m.id)) return fail(m, 'id không hợp lệ (chỉ a-z, 0-9, gạch nối)');
    if (ADE.reservedIds.indexOf(m.id) >= 0) return fail(m, 'id nằm trong danh sách cấm');
    if (ADE.trackMap[m.id]) return fail(m, 'id trùng');
    if (typeof m.domain !== 'string' || !m.domain) return fail(m, 'domain phải là chuỗi');
    if (!/^#[0-9a-fA-F]{6}$/.test(m.accent)) return fail(m, 'accent phải là mã hex #RRGGBB');
    if (typeof m.order !== 'number') return fail(m, 'order phải là số');
    if (LEVELS.indexOf(m.level) < 0) return fail(m, 'level phải thuộc ' + LEVELS.join('|'));
    if (STATUSES.indexOf(m.status) < 0) return fail(m, 'status phải thuộc ' + STATUSES.join('|'));
    if (!Array.isArray(m.chapters) || !m.chapters.length) return fail(m, 'chapters rỗng');
    if (!Array.isArray(m.languages) || m.languages.some(function (l) { return ADE.langs.indexOf(l) < 0; })) return fail(m, 'languages chứa ngôn ngữ chưa được hỗ trợ');
    var seen = {};
    for (var c = 0; c < m.chapters.length; c++) {
      var ch = m.chapters[c];
      if (!ch.id || !ch.titleKey) return fail(m, 'chương thứ ' + (c + 1) + ' thiếu id hoặc titleKey');
      if (!/^[a-z][a-z0-9]*$/.test(ch.id)) return fail(m, 'id chương không hợp lệ: ' + ch.id);
      if (seen[ch.id]) return fail(m, 'id chương trùng: ' + ch.id);
      seen[ch.id] = 1;
      ch.sims = ch.sims || [];
      ch.bridges = ch.bridges || [];
      ch.goals = ch.goals || [];
    }
    m.presets = m.presets || [];
    m.prerequisites = m.prerequisites || [];
    var pseen = {};
    for (var p = 0; p < m.presets.length; p++) {
      var ps = m.presets[p];
      if (!ps.id || !ps.model || !ps.titleKey) return fail(m, 'preset thứ ' + (p + 1) + ' thiếu id/model/titleKey');
      if (pseen[ps.id]) return fail(m, 'preset trùng: ' + ps.id);
      pseen[ps.id] = 1;
    }
    ADE.tracks.push(m);
    ADE.tracks.sort(function (a, b) { return a.order - b.order; });
    ADE.trackMap[m.id] = m;
    return true;
  };

  ADE.getTrack = function (id) { return ADE.trackMap[id] || null; };
  ADE.getChapter = function (trackId, chapterId) {
    var t = ADE.trackMap[trackId];
    if (!t) return null;
    for (var i = 0; i < t.chapters.length; i++) if (t.chapters[i].id === chapterId) return { track: t, chapter: t.chapters[i], index: i };
    return null;
  };
  // 'trackId' hoặc 'trackId/chapterId' → {track, chapter|null}
  ADE.resolveRef = function (ref) {
    var parts = String(ref).split('/');
    var t = ADE.trackMap[parts[0]];
    if (!t) return null;
    if (!parts[1]) return { track: t, chapter: null };
    var c = ADE.getChapter(parts[0], parts[1]);
    return c ? { track: t, chapter: c.chapter } : null;
  };
  ADE.domains = function () {
    var map = {}, out = [];
    ADE.tracks.forEach(function (t) {
      if (!map[t.domain]) { map[t.domain] = { id: t.domain, tracks: [] }; out.push(map[t.domain]); }
      map[t.domain].tracks.push(t);
    });
    return out;
  };
  ADE.domainLabel = function (id) { return ADE.hasKey('domain.' + id) ? ADE.t('domain.' + id) : id; };
  ADE.allPresets = function () {
    var out = [];
    ADE.tracks.forEach(function (t) { t.presets.forEach(function (p) { out.push({ track: t, preset: p }); }); });
    return out;
  };
  ADE.chapterKey = function (trackId, chapterId, sub) { return 'track.' + trackId + '.' + chapterId + (sub ? '.' + sub : ''); };

  /* ---------- model, view, mã ---------- */
  ADE.registerModel = function (id, def) {
    if (ADE.models[id]) { ADE.err('error', 'registry', 'Model trùng id: ' + id); return false; }
    var kind = def && def.kind;
    var need = { discrete: ['init', 'steps', 'act'], continuous: ['init', 'advance', 'sample', 'act'], compute: ['compute'] }[kind];
    if (!need) { ADE.err('error', 'registry', 'Model "' + id + '": kind phải là discrete|continuous|compute'); return false; }
    for (var i = 0; i < need.length; i++) if (typeof def[need[i]] !== 'function') { ADE.err('error', 'registry', 'Model "' + id + '" thiếu hàm ' + need[i]); return false; }
    def.id = id;
    ADE.models[id] = def;
    return true;
  };
  ADE.registerView = function (modelId, cfg) { ADE.views[modelId] = cfg; };
  ADE.addCode = function (trackId, id, snippet) { ADE.code[trackId + '.' + id] = snippet; };
  ADE.getCode = function (trackId, id) { return ADE.code[trackId + '.' + id] || null; };

  /* ---------- nguồn (master 6.1: shared/sources.js + sources.js của track) ---------- */
  // {id, title, url, org, tracks:[], label?, lang:'en'|'vi', pageOnly?, supports:{vi,en}}
  ADE.addSources = function (list) {
    list.forEach(function (s) {
      if (!s.id || !s.url || !s.title) { ADE.err('error', 'sources', 'Nguồn thiếu id/url/title: ' + JSON.stringify(s).slice(0, 80)); return; }
      if (ADE.sources[s.id]) { ADE.err('error', 'sources', 'Nguồn trùng id: ' + s.id); return; }
      ADE.sources[s.id] = s;
      ADE.sourceList.push(s);
    });
  };
  ADE.setVersions = function (v) { ADE.versions = v; };

  /* ---------- glossary và hiểu lầm: khoá phẳng dưới track.<ns>.* hoặc shared.* ---------- */
  function nsPrefix(ns, part) { return (ns === 'shared' ? 'shared.' : 'track.' + ns + '.') + part + '.'; }
  function addNs(lang, ns, part, entries, fields, owner, meta, ids) {
    var strings = {};
    var prefix = nsPrefix(ns, part);
    Object.keys(entries).forEach(function (id) {
      var e = entries[id];
      if (owner[id] && owner[id] !== ns) { ADE.err('error', 'i18n', part + ' "' + id + '" trùng giữa ' + owner[id] + ' và ' + ns); return; }
      if (!owner[id]) { owner[id] = ns; ids.push(id); }
      fields.forEach(function (f) { if (e[f] !== undefined) strings[prefix + id + '.' + f] = e[f]; });
      meta[lang] = meta[lang] || {};
      meta[lang][id] = { chapter: e.chapter || null };
    });
    var scope = ns === 'shared' ? ['shared.'] : ['track.' + ns + '.'];
    ADE.addStrings(lang, strings, scope, part + ':' + ns);
  }
  ADE.addGlossary = function (lang, ns, entries) { addNs(lang, ns, 'glossary', entries, ['term', 'def'], ADE.glossaryOwner, ADE.glossaryMeta, ADE.glossaryIds); };
  ADE.addMisconceptions = function (lang, ns, entries) { addNs(lang, ns, 'mis', entries, ['wrong', 'right', 'example'], ADE.misOwner, ADE.misMeta, ADE.misIds); };
  ADE.glossaryKey = function (id, part) { var ns = ADE.glossaryOwner[id]; return ns ? nsPrefix(ns, 'glossary') + id + '.' + part : null; };
  ADE.misKey = function (id, part) { var ns = ADE.misOwner[id]; return ns ? nsPrefix(ns, 'mis') + id + '.' + part : null; };
  ADE.glossaryTerm = function (id) {
    var k = ADE.glossaryKey(id, 'term');
    return k && ADE.hasKey(k) ? ADE.t(k) : null;
  };

  /* ---------- cầu nối và lộ trình (cấu trúc không phụ thuộc ngôn ngữ) ---------- */
  // {id:'X1', owner:'trackId/chapterId', links:['trackId/chapterId', ...]}; văn bản ở shared.bridge.<id>.*
  ADE.addBridges = function (list) {
    list.forEach(function (b) {
      if (ADE.bridgeMap[b.id]) { ADE.err('error', 'registry', 'Cầu nối trùng: ' + b.id); return; }
      ADE.bridgeMap[b.id] = b; ADE.bridgeList.push(b);
    });
  };
  // {id, steps:['trackId' | 'trackId/chapterId', ...]}; văn bản ở shared.path.<id>.*
  ADE.addPaths = function (list) {
    list.forEach(function (p) {
      if (ADE.pathList.some(function (x) { return x.id === p.id; })) { ADE.err('error', 'registry', 'Lộ trình trùng: ' + p.id); return; }
      ADE.pathList.push(p);
    });
  };

  /* ---------- giai đoạn 2: kiểm tra tham chiếu chéo ---------- */
  ADE.validateAll = function () {
    var pend = function (area, msg, ref) { // track chưa đăng ký → cảnh báo; track có mà chương thiếu → lỗi
      var parts = String(ref).split('/');
      if (!ADE.trackMap[parts[0]]) ADE.err('warn', area, msg + ' (track "' + parts[0] + '" chưa đăng ký)');
      else ADE.err('error', area, msg + ' (không có chương "' + ref + '")');
    };
    ADE.tracks.forEach(function (t) {
      ['titleKey', 'summaryKey'].forEach(function (f) {
        ADE.langs.forEach(function (l) { if (!ADE.hasKey(t[f], l)) ADE.err('error', 'registry', 'Track ' + t.id + ': thiếu chuỗi ' + t[f] + ' ở ' + l); });
      });
      t.prerequisites.forEach(function (p) { if (!ADE.trackMap[p]) ADE.err('warn', 'registry', 'Track ' + t.id + ': tiên quyết "' + p + '" chưa đăng ký'); });
      t.logKinds.forEach(function (k) { if (!ADE.kinds[k]) ADE.err('error', 'registry', 'Track ' + t.id + ': logKind chưa định nghĩa: ' + k); });
      t.chapters.forEach(function (ch) {
        ADE.langs.forEach(function (l) {
          if (!ADE.hasKey(ch.titleKey, l)) ADE.err('error', 'registry', t.id + '/' + ch.id + ': thiếu tiêu đề ' + ch.titleKey + ' ở ' + l);
          var ek = ADE.chapterKey(t.id, ch.id, 'essence');
          if (!ADE.hasKey(ek, l)) ADE.err('error', 'registry', t.id + '/' + ch.id + ': thiếu "bản chất" ' + ek + ' ở ' + l);
        });
        ch.sims.forEach(function (s) { if (!ADE.models[s]) ADE.err('error', 'registry', t.id + '/' + ch.id + ': sim trỏ tới model không tồn tại: ' + s); });
        ch.bridges.forEach(function (b) { if (!ADE.bridgeMap[b]) ADE.err('error', 'registry', t.id + '/' + ch.id + ': cầu nối không tồn tại: ' + b); });
        ch.goals.forEach(function (g) {
          ADE.langs.forEach(function (l) { var gk = ADE.chapterKey(t.id, ch.id, 'goal.' + g.id); if (!ADE.hasKey(gk, l)) ADE.err('error', 'registry', 'Thiếu mục tiêu ' + gk + ' ở ' + l); });
        });
      });
      t.presets.forEach(function (p) {
        if (!ADE.models[p.model]) ADE.err('error', 'registry', t.id + ': preset "' + p.id + '" trỏ tới model không tồn tại: ' + p.model);
        ADE.langs.forEach(function (l) { if (!ADE.hasKey(p.titleKey, l)) ADE.err('error', 'registry', t.id + ': thiếu tiêu đề preset ' + p.titleKey + ' ở ' + l); });
      });
    });
    ADE.bridgeList.forEach(function (b) {
      [b.owner].concat(b.links || []).forEach(function (ref) {
        if (!ADE.resolveRef(ref)) pend('registry', 'Cầu nối ' + b.id + ' trỏ tới ' + ref, ref);
      });
    });
    ADE.pathList.forEach(function (p) {
      p.steps.forEach(function (ref) { if (!ADE.resolveRef(ref)) pend('registry', 'Lộ trình ' + p.id + ' trỏ tới ' + ref, ref); });
    });
    Object.keys(ADE.glossaryMeta).forEach(function (l) {
      Object.keys(ADE.glossaryMeta[l]).forEach(function (id) {
        var ch = ADE.glossaryMeta[l][id].chapter;
        if (ch && !ADE.resolveRef(ch)) pend('registry', 'Glossary "' + id + '" trỏ tới ' + ch, ch);
      });
    });
    Object.keys(ADE.misMeta).forEach(function (l) {
      Object.keys(ADE.misMeta[l]).forEach(function (id) {
        var ch = ADE.misMeta[l][id].chapter;
        if (ch && !ADE.resolveRef(ch)) pend('registry', 'Hiểu lầm "' + id + '" trỏ tới ' + ch, ch);
      });
    });
    return ADE.errors;
  };
})();
