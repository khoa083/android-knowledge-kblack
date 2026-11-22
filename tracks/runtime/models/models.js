/* Model track B: Compose Runtime (thuần, không DOM, không câu chữ; chỉ message key).
   Mọi quy tắc là MÔ HÌNH GIẢNG DẠY (simplified). Nguồn và phiên bản: docs/research/runtime.md
   (Compose runtime/ui 1.13.0 trong BOM 2026.11.01; Kotlin 2.4.21; chi tiết nội bộ theo how-compose-works.md và mã AndroidX ghim ở androidx-main @296313a4, 2026-11-21; model v1 cũ có thể còn ghi "đọc 2026-11-21"). */
(function () {
  'use strict';
  var K = 'track.runtime.';
  var M = function (m, s) { return K + 'm.' + m + '.' + s; };
  var ST = function (s) { return K + 'st.' + s; };
  function S(m, id, o) {
    o.id = id; o.type = o.type || 'mechanism';
    o.titleKey = o.titleKey || M(m, 's.' + id + '.title');
    o.explainKey = o.explainKey || M(m, 's.' + id + '.explain');
    o.params = o.params || {}; o.activeNodes = o.activeNodes || []; o.movingSignals = o.movingSignals || [];
    (o.logEvents || []).forEach(function (e) { if (!e.detailKey) e.detailKey = M(m, 'ev.' + id); if (!e.params) e.params = o.params; });
    return o;
  }
  function reg(m, def) {
    def.kind = 'discrete';
    def.titleKey = M(m, 'title'); def.overviewKey = M(m, 'overview'); def.wrapupKey = M(m, 'wrapup');
    def.codeId = def.codeId || m; def.controlsHintKey = M(m, 'ctl.hint');
    def.simplificationKeys = [M(m, 'simp.1')].concat(def.simpExtra || []);
    ADE.registerModel('runtime.' + m, def);
  }
  var R = ADE.runtimeModel = { K: K, M: M };

  /* ================= B0: bản đồ runtime. Chọn một thành phần để xem nó nhận gì và chuyển gì ================= */
  /* Thứ tự và vai trò theo how-compose-works.md, reference Recomposer/Applier/Snapshot/ComposeView, trang phases và semantics. */
  var MAP = R.MAP = ['host', 'composition', 'recomposer', 'compiler', 'composer', 'slots', 'snapshot', 'applier', 'uitree', 'phases', 'semantics'];
  var ANDROID = { host: 1, uitree: 1 };     // gắn nhãn android-impl
  var CH = { host: 'b1', composition: 'b1', recomposer: 'b5', compiler: 'b2', composer: 'b6', slots: 'b3', snapshot: 'b4', applier: 'b6', uitree: 'b6', phases: 'b7', semantics: 'b9' };
  var IN = { host: 'e0', composition: 'e1', recomposer: 'e5', compiler: 'e2', composer: 'e3', slots: 'e4', snapshot: 'e5', applier: 'e6', uitree: 'e7', phases: 'e8', semantics: 'e10' };
  (function () {
    var m = 'map';
    function steps(s) {
      var f = s.focus, P = { ch: CH[f] }, base = M(m, 'c.' + f + '.');
      return [
        S(m, 'what', { type: 'scenario', explainKey: base + 'what', params: P, activeNodes: [f], affected: [f],
          nodeStates: nodeStatesFor(f), callouts: ANDROID[f] ? [{ kind: 'android', textKey: M(m, 'co.android') }] : [{ kind: 'try', textKey: M(m, 'co.try') }],
          logEvents: [{ t: 0, kind: 'observe', subject: f, detailKey: M(m, 'ev.what') }] }),
        S(m, 'input', { explainKey: base + 'in', params: P, activeNodes: [f], affected: [f], movingSignals: [{ edge: IN[f], tok: 'runtime' }],
          nodeStates: nodeStatesFor(f), logEvents: [{ t: 1, kind: 'observe', subject: f, detailKey: M(m, 'ev.in') }] }),
        S(m, 'output', { explainKey: base + 'out', params: P, activeNodes: [f], affected: [f], stateAfter: [{ labelKey: M(m, 'st.chapter'), value: CH[f].toUpperCase() }],
          nodeStates: nodeStatesFor(f), callouts: [{ kind: 'source', textKey: base + 'src' }],
          logEvents: [{ t: 2, kind: 'observe', subject: f, detailKey: M(m, 'ev.out') }] })
      ];
    }
    function nodeStatesFor(f) { var o = {}; MAP.forEach(function (id) { o[id] = id === f ? ST('focus') : (ANDROID[id] ? ST('androidImpl') : ST('runtime')); }); return o; }
    reg(m, {
      controls: [{ id: 'focus', type: 'select', labelKey: M(m, 'ctl.focus'), get: function (s) { return s.focus; }, action: 'focus',
        options: MAP.map(function (id) { return { value: id, labelKey: K + 'n.' + id }; }) }],
      init: function () { return { focus: 'composition' }; },
      act: function (s, a, v) { return { focus: MAP.indexOf(v) >= 0 ? v : s.focus }; },
      steps: steps,
      selfChecks: [{ name: 'mỗi thành phần có 3 bước và trỏ tới một chương', run: function () { return MAP.every(function (f) { return steps({ focus: f }).length === 3 && !!CH[f]; }); } }]
    });
  })();

  /* ================= B1: setContent và composition ban đầu (ComposeView reference) =================
     Composition ban đầu xảy ra khi view gắn vào window hoặc khi gọi createComposition(), cái nào trước;
     nếu tắt tạo khi gắn (shouldCreateCompositionOnAttachedToWindow = false) thì vẫn xảy ra ở lần measure đầu. */
  (function () {
    var m = 'setcontent';
    function steps(s) {
      var out = [], t = 0, trig = s.trigger;    // 'attach' | 'create' | 'measure'
      var P = { trig: trig };
      out.push(S(m, 'set', { type: 'scenario', activeNodes: ['host'], params: P, nodeStates: { host: ST('hasContent'), composition: ST('none') },
        stateAfter: [{ labelKey: M(m, 'st.content'), valueKey: M(m, 'val.stored') }, { labelKey: M(m, 'st.comp'), valueKey: M(m, 'val.none') }],
        callouts: [{ kind: 'android', textKey: M(m, 'co.host') }].concat(!s.eager && trig === 'create' ? [{ kind: 'mechanism', textKey: M(m, 'co.eagerIgnored') }] : []), codeHighlight: { snippet: 'setcontent', lines: [1, 2, 3, 4] },
        logEvents: [{ t: t, kind: 'act', subject: 'host' }] }));
      if (!s.eager && trig === 'attach') {
        out.push(S(m, 'attachLazy', { type: 'experiment', activeNodes: ['host'], params: P, nodeStates: { host: ST('attached'), composition: ST('none') },
          skipped: [{ whatKey: M(m, 'sk.initial'), whyKey: M(m, 'sk.lazy') }], logEvents: [{ t: t += 10, kind: 'skip', subject: 'host' }] }));
        trig = 'measure';
      }
      out.push(S(m, 'trigger', { titleKey: M(m, 's.trigger.' + trig + '.title'), explainKey: M(m, 's.trigger.' + trig + '.explain'), activeNodes: ['host', 'composition'], params: P,
        movingSignals: [{ edge: 'e0', tok: 'runtime' }], nodeStates: { host: ST('attached'), composition: ST('created') },
        stateBefore: [{ labelKey: M(m, 'st.comp'), valueKey: M(m, 'val.none') }], stateAfter: [{ labelKey: M(m, 'st.comp'), valueKey: M(m, 'val.created') }],
        codeHighlight: { snippet: 'setcontent', lines: trig === 'create' ? [6] : [5] },
        logEvents: [{ t: t += 10, kind: 'schedule', subject: 'composition', detailKey: M(m, 'ev.trigger.' + trig) }] }));
      out.push(S(m, 'run', { activeNodes: ['composition', 'compiler'], movingSignals: [{ edge: 'e2', tok: 'runtime' }], nodeStates: { composition: ST('composing') },
        callouts: [{ kind: 'mechanism', textKey: M(m, 'co.transformed') }], logEvents: [{ t: t += 10, kind: 'recompose', subject: 'composition' }] }));
      out.push(S(m, 'record', { activeNodes: ['composer', 'slots'], movingSignals: [{ edge: 'e4', tok: 'runtime' }], nodeStates: { composer: ST('recording'), slots: ST('filled') },
        changes: [{ op: 'add', textKey: M(m, 'ch.groups') }], logEvents: [{ t: t += 10, kind: 'recompose', subject: 'composer' }] }));
      out.push(S(m, 'apply', { activeNodes: ['applier', 'uitree'], movingSignals: [{ edge: 'e7', tok: 'ui' }], nodeStates: { applier: ST('applying'), uitree: ST('built') },
        changes: [{ op: 'add', textKey: M(m, 'ch.nodes') }], logEvents: [{ t: t += 10, kind: 'apply', subject: 'applier', to: 'uitree' }] }));
      out.push(S(m, 'phases', { activeNodes: ['phases'], movingSignals: [{ edge: 'e8', tok: 'ui' }], nodeStates: { phases: ST('ran') },
        logEvents: [{ t: t += 10, kind: 'layout', subject: 'phases' }, { t: t += 5, kind: 'draw', subject: 'phases' }] }));
      return out;
    }
    reg(m, {
      controls: [
        { id: 'trigger', type: 'select', labelKey: M(m, 'ctl.trigger'), get: function (s) { return s.trigger; }, action: 'trigger',
          options: ['attach', 'create'].map(function (v) { return { value: v, labelKey: M(m, 'ctl.trigger.' + v) }; }) },
        { id: 'eager', type: 'toggle', labelKey: M(m, 'ctl.eager'), get: function (s) { return s.eager; }, action: 'eager' }
      ],
      init: function () { return { trigger: 'attach', eager: true }; },
      act: function (s, a, v) { var n = { trigger: s.trigger, eager: s.eager }; if (a === 'trigger') n.trigger = v === 'create' ? 'create' : 'attach'; else n.eager = !!v; return n; },
      steps: steps,
      selfChecks: [{ name: 'tắt tạo khi gắn window → composition ban đầu ở lần measure đầu', run: function () {
        var st = steps({ trigger: 'attach', eager: false }); return st.some(function (x) { return x.titleKey === M(m, 's.trigger.measure.title'); }) && st.length === 7;
      } }]
    });
  })();

  /* ================= B2: compiler transform (mã giả minh họa; how-compose-works.md, androidx-main) =================
     Restart group: nếu tham số không đổi và Composer cho phép skip → skipToGroupEnd; endRestartGroup trả null khi
     không có lần đọc state quan sát được, ngược lại trả về update scope để chạy lại hàm. */
  (function () {
    var m = 'compiler';
    function steps(s) {
      var out = [], P = {};
      out.push(S(m, 'start', { type: 'scenario', activeNodes: ['compiler', 'composer'], movingSignals: [{ edge: 'e2', tok: 'runtime' }],
        codeHighlight: { snippet: 'compiler', lines: [3, 4] }, callouts: [{ kind: 'pitfall', textKey: M(m, 'co.illustrative') }],
        logEvents: [{ t: 0, kind: 'recompose', subject: 'composer' }] }));
      out.push(S(m, 'compare', { activeNodes: ['composer', 'slots'], movingSignals: [{ edge: 'e4', tok: 'runtime' }],
        stateBefore: [{ labelKey: M(m, 'st.old'), value: '"Ana"' }], stateAfter: [{ labelKey: M(m, 'st.new'), value: s.changed ? '"Bo"' : '"Ana"' }],
        explainKey: M(m, s.changed ? 's.compare.changed' : 's.compare.same'), codeHighlight: { snippet: 'compiler', lines: [5] },
        logEvents: [{ t: 10, kind: 'recompose', subject: 'composer', detailKey: M(m, s.changed ? 'ev.changed' : 'ev.same') }] }));
      if (s.changed) {
        out.push(S(m, 'body', { activeNodes: ['compiler'], codeHighlight: { snippet: 'compiler', lines: [6] }, changes: [{ op: 'set', textKey: M(m, 'ch.text') }],
          logEvents: [{ t: 20, kind: 'recompose', subject: 'compiler' }] }));
      } else {
        out.push(S(m, 'skip', { activeNodes: ['composer'], codeHighlight: { snippet: 'compiler', lines: [8] },
          skipped: [{ whatKey: M(m, 'sk.body'), whyKey: M(m, 'sk.same') }], logEvents: [{ t: 20, kind: 'skip', subject: 'composer' }] }));
      }
      out.push(S(m, 'end', { explainKey: M(m, s.reads ? 's.end.scope' : 's.end.null'), activeNodes: ['composer'], codeHighlight: { snippet: 'compiler', lines: [10] },
        stateAfter: [{ labelKey: M(m, 'st.scope'), valueKey: M(m, s.reads ? 'val.scope' : 'val.null') }],
        callouts: [{ kind: 'mechanism', textKey: M(m, 'co.impl') }], logEvents: [{ t: 30, kind: s.reads ? 'schedule' : 'skip', subject: 'composer', detailKey: M(m, s.reads ? 'ev.scope' : 'ev.null') }] }));
      return out;
    }
    reg(m, {
      simpExtra: [M(m, 'simp.2')],
      controls: [
        { id: 'changed', type: 'toggle', labelKey: M(m, 'ctl.changed'), get: function (s) { return s.changed; }, action: 'changed' },
        { id: 'reads', type: 'toggle', labelKey: M(m, 'ctl.reads'), get: function (s) { return s.reads; }, action: 'reads' }
      ],
      init: function () { return { changed: true, reads: true }; },
      act: function (s, a, v) { var n = { changed: s.changed, reads: s.reads }; n[a] = !!v; return n; },
      steps: steps,
      selfChecks: [{ name: 'tham số không đổi → skip thân hàm; không đọc state → không có update scope', run: function () {
        var a = steps({ changed: false, reads: false }); return a[2].id === 'skip' && a[3].logEvents[0].kind === 'skip';
      } }]
    });
  })();

  /* ================= B3: identity trong danh sách, có và không có key() (trang Lifecycle of composables) =================
     Không key: instance được nhận diện theo call site + thứ tự thực thi (vị trí). Item đổi đầu vào ở một vị trí → recompose;
     effect phụ thuộc đầu vào bị hủy và chạy lại; `remember {}` không key ở lại với vị trí. Thêm ở cuối → các instance cũ tái dùng.
     Có key: instance đi theo key; item bị xoá rời Composition, item mới được tạo, item di chuyển giữ state. */
  var R3 = R.keys = {};
  R3.apply = function (list, op) {
    var l = list.slice();
    if (op === 'insertTop') l.unshift('N');
    else if (op === 'insertEnd') l.push('N');
    else if (op === 'removeMiddle') l.splice(1, 1);
    else if (op === 'swap') { var x = l[0]; l[0] = l[1]; l[1] = x; }
    return l;
  };
  // trả về danh sách kết quả cho từng item mới: {item, slot, fate:'kept'|'recomposed'|'created', stateFrom}, và danh sách bị bỏ
  R3.diff = function (before, after, keyed) {
    var res = [], removed = [];
    if (keyed) {
      after.forEach(function (it, i) {
        var j = before.indexOf(it);
        if (j < 0) res.push({ item: it, pos: i, fate: 'created', stateFrom: null });
        else res.push({ item: it, pos: i, fate: j === i ? 'kept' : 'moved', stateFrom: it });
      });
      before.forEach(function (it) { if (after.indexOf(it) < 0) removed.push(it); });
    } else {
      after.forEach(function (it, i) {
        if (i >= before.length) res.push({ item: it, pos: i, fate: 'created', stateFrom: null });
        else res.push({ item: it, pos: i, fate: before[i] === it ? 'kept' : 'recomposed', stateFrom: before[i] });
      });
      for (var i = after.length; i < before.length; i++) removed.push(before[i]);
    }
    return { res: res, removed: removed };
  };
  (function () {
    var m = 'keys', BEFORE = ['A', 'B', 'C'];
    function steps(s) {
      var after = R3.apply(BEFORE, s.op), d = R3.diff(BEFORE, after, s.key), out = [];
      var cnt = { kept: 0, moved: 0, recomposed: 0, created: 0, removed: d.removed.length };
      out.push(S(m, 'op', { type: 'scenario', titleKey: M(m, 's.op.' + s.op + '.title'), explainKey: M(m, s.key ? 's.op.keyed' : 's.op.positional'),
        params: { before: BEFORE.join(', '), after: after.join(', ') }, activeNodes: ['list'],
        stateBefore: [{ labelKey: M(m, 'st.list'), value: BEFORE.join(', ') }], stateAfter: [{ labelKey: M(m, 'st.list'), value: after.join(', ') }],
        codeHighlight: { snippet: 'keys', lines: s.key ? [2, 3, 4] : [6, 7, 8] }, callouts: [{ kind: 'try', textKey: M(m, 'co.try') }],
        logEvents: [{ t: 0, kind: 'write', subject: 'list' }] }));
      d.res.forEach(function (r, i) {
        cnt[r.fate]++;
        var slot = 'p' + r.pos, P = { item: r.item, pos: r.pos + 1, from: r.stateFrom || '–' };
        var ns = {}; ns[slot] = ST(r.fate);
        var kind = r.fate === 'kept' ? 'skip' : r.fate === 'created' ? 'apply' : 'recompose';
        var o = S(m, 'item' + i, { titleKey: M(m, 's.' + r.fate + '.title'), explainKey: M(m, 's.' + r.fate + (s.key ? '.keyed' : '.positional')), params: P,
          activeNodes: [slot], nodeStates: ns, affected: [slot],
          stateAfter: [{ labelKey: M(m, 'st.remember'), value: r.stateFrom ? 'remember(' + r.stateFrom + ')' : '–' }, { labelKey: M(m, 'st.effect'), valueKey: M(m, r.fate === 'recomposed' ? 'val.restarted' : r.fate === 'created' ? 'val.started' : 'val.kept') }],
          logEvents: [{ t: 10 * (i + 1), kind: kind, subject: slot, detailKey: M(m, 'ev.' + r.fate), params: P }] });
        if (r.fate === 'kept') o.skipped = [{ whatKey: M(m, 'sk.item'), whyKey: M(m, 'sk.same') }];
        if (r.fate === 'recomposed' && !s.key) o.callouts = [{ kind: 'pitfall', textKey: M(m, 'co.stateWrong'), params: P }];
        o.metrics = { kept: cnt.kept + cnt.moved, recomposed: cnt.recomposed, created: cnt.created, removed: 0 };
        out.push(o);
      });
      d.removed.forEach(function (it, i) {
        out.push(S(m, 'removed' + i, { titleKey: M(m, 's.removed.title'), explainKey: M(m, s.key ? 's.removed.keyed' : 's.removed.positional'), params: { item: it },
          activeNodes: ['list'], changes: [{ op: 'remove', textKey: M(m, 'ch.leave'), params: { item: it } }],
          logEvents: [{ t: 100 + i, kind: 'apply', subject: 'list', detailKey: M(m, 'ev.removed'), params: { item: it } }] }));
      });
      var last = out[out.length - 1];
      last.metrics = { kept: cnt.kept + cnt.moved, recomposed: cnt.recomposed, created: cnt.created, removed: cnt.removed };
      last.callouts = (last.callouts || []).concat([{ kind: 'source', textKey: M(m, 'co.source') }]);
      return out;
    }
    reg(m, {
      controls: [
        { id: 'op', type: 'select', labelKey: M(m, 'ctl.op'), get: function (s) { return s.op; }, action: 'op',
          options: ['insertTop', 'insertEnd', 'removeMiddle', 'swap'].map(function (v) { return { value: v, labelKey: M(m, 'ctl.op.' + v) }; }) },
        { id: 'key', type: 'toggle', labelKey: M(m, 'ctl.key'), get: function (s) { return s.key; }, action: 'key' }
      ],
      init: function () { return { op: 'insertTop', key: false }; },
      act: function (s, a, v) { var n = { op: s.op, key: s.key }; if (a === 'op') n.op = v; else n.key = !!v; return n; },
      steps: steps,
      selfChecks: [
        { name: 'không key + chèn đầu: 3 item recompose, 1 tạo mới; có key: 0 recompose, 1 tạo mới', run: function () {
          var a = R3.diff(BEFORE, R3.apply(BEFORE, 'insertTop'), false).res, b = R3.diff(BEFORE, R3.apply(BEFORE, 'insertTop'), true).res;
          var c = function (r, f) { return r.filter(function (x) { return x.fate === f; }).length; };
          return c(a, 'recomposed') === 3 && c(a, 'created') === 1 && c(b, 'recomposed') === 0 && c(b, 'created') === 1;
        } },
        { name: 'không key + thêm cuối: các item cũ giữ nguyên (không khái quát "luôn tạo lại")', run: function () {
          var a = R3.diff(BEFORE, R3.apply(BEFORE, 'insertEnd'), false).res; return a.filter(function (x) { return x.fate === 'kept'; }).length === 3;
        } },
        { name: 'không key + xoá giữa: A giữ, vị trí 2 recompose, instance cuối rời Composition', run: function () {
          var d = R3.diff(BEFORE, R3.apply(BEFORE, 'removeMiddle'), false); return d.res[0].fate === 'kept' && d.res[1].fate === 'recomposed' && d.removed.join() === 'C';
        } }
      ]
    });
  })();

  /* ================= B4: Snapshot (reference Snapshot) =================
     Ghi trong mutable snapshot được cách ly tới khi apply; apply thông báo cho apply observer; composition đã
     đăng ký đọc state đó thì bị invalidate. Nếu không scope nào đọc state, không có gì bị invalidate. */
  (function () {
    var m = 'snapshot';
    function steps(s) {
      var out = [], t = 0;
      out.push(S(m, 'read', { type: 'scenario', explainKey: M(m, s.read ? 's.read.explain' : 's.read.none'), activeNodes: ['composer', 'snapshot'], movingSignals: [{ edge: 'e5', tok: 'state' }],
        stateAfter: [{ labelKey: M(m, 'st.readers'), valueKey: M(m, s.read ? 'val.scopeText' : 'val.noReader') }], codeHighlight: { snippet: 'snapshot', lines: s.read ? [2, 3] : [2] },
        logEvents: [{ t: t, kind: 'observe', subject: 'snapshot' }] }));
      out.push(S(m, 'write', { explainKey: M(m, s.isolated ? 's.write.isolated' : 's.write.global'), activeNodes: ['snapshot'],
        stateBefore: [{ labelKey: M(m, 'st.global'), value: '0' }], stateAfter: [{ labelKey: M(m, 'st.global'), value: s.isolated ? '0' : '1' }, { labelKey: M(m, 'st.inside'), value: s.isolated ? '1' : '–' }],
        codeHighlight: { snippet: 'snapshot', lines: s.isolated ? [5, 6] : [8] }, logEvents: [{ t: t += 10, kind: 'write', subject: 'snapshot' }] }));
      if (s.isolated) out.push(S(m, 'apply', { activeNodes: ['snapshot'], stateAfter: [{ labelKey: M(m, 'st.global'), value: '1' }], codeHighlight: { snippet: 'snapshot', lines: [7] },
        callouts: [{ kind: 'mechanism', textKey: M(m, 'co.conflict') }], logEvents: [{ t: t += 10, kind: 'apply', subject: 'snapshot' }] }));
      if (s.read) {
        out.push(S(m, 'invalidate', { activeNodes: ['snapshot', 'recomposer'], movingSignals: [{ edge: 'e5', tok: 'state' }], affected: ['composition'],
          logEvents: [{ t: t += 10, kind: 'invalidate', subject: 'composition' }] }));
        out.push(S(m, 'recompose', { activeNodes: ['recomposer', 'composition'], logEvents: [{ t: t += 10, kind: 'recompose', subject: 'composition' }] }));
      } else {
        out.push(S(m, 'nothing', { type: 'experiment', activeNodes: ['snapshot'], skipped: [{ whatKey: M(m, 'sk.recompose'), whyKey: M(m, 'sk.noReader') }],
          logEvents: [{ t: t += 10, kind: 'skip', subject: 'composition' }] }));
      }
      return out;
    }
    reg(m, {
      simpExtra: [M(m, 'simp.2')],
      controls: [
        { id: 'isolated', type: 'toggle', labelKey: M(m, 'ctl.isolated'), get: function (s) { return s.isolated; }, action: 'isolated' },
        { id: 'read', type: 'toggle', labelKey: M(m, 'ctl.read'), get: function (s) { return s.read; }, action: 'read' }
      ],
      init: function () { return { isolated: false, read: true }; },
      act: function (s, a, v) { var n = { isolated: s.isolated, read: s.read }; n[a] = !!v; return n; },
      steps: steps,
      selfChecks: [{ name: 'không ai đọc state → không invalidate', run: function () { return !steps({ isolated: false, read: false }).some(function (x) { return x.id === 'invalidate'; }); } }]
    });
  })();

  /* ================= B5: Recomposer và frame clock (reference Recomposer, MonotonicFrameClock) =================
     Recomposer chờ composer bị invalidate, recompose và apply; withFrameNanos suspend tới frame mới.
     Hai lần ghi trước khi Recomposer xử lý được gộp vào cùng một lượt (mô hình giản lược). Frame clock bị pause → việc chờ. */
  (function () {
    var m = 'recomposer';
    function steps(s) {
      var out = [], t = 0, n = s.writes;
      for (var i = 1; i <= n; i++) out.push(S(m, 'write' + i, { type: i === 1 ? 'scenario' : 'mechanism', titleKey: M(m, 's.write.title'), explainKey: M(m, 's.write.explain'), params: { n: i },
        activeNodes: ['snapshot'], movingSignals: [{ edge: 'e5', tok: 'state' }], logEvents: [{ t: t += 2, kind: 'invalidate', subject: 'recomposer', detailKey: M(m, 'ev.write'), params: { n: i } }] }));
      out.push(S(m, 'pending', { params: { n: n }, activeNodes: ['recomposer'], stateAfter: [{ labelKey: M(m, 'st.pending'), value: String(n) }],
        logEvents: [{ t: t += 2, kind: 'schedule', subject: 'recomposer', params: { n: n } }] }));
      if (s.paused) out.push(S(m, 'paused', { type: 'experiment', activeNodes: ['recomposer'], skipped: [{ whatKey: M(m, 'sk.frame'), whyKey: M(m, 'sk.paused') }],
        logEvents: [{ t: t += 2, kind: 'skip', subject: 'recomposer' }], callouts: [{ kind: 'source', textKey: M(m, 'co.pause') }] }));
      if (s.paused) out.push(S(m, 'resume', { activeNodes: ['recomposer'], logEvents: [{ t: t += 20, kind: 'resume', subject: 'recomposer' }] }));
      out.push(S(m, 'frame', { activeNodes: ['recomposer'], callouts: [{ kind: 'mechanism', textKey: M(m, 'co.frame') }], codeHighlight: { snippet: 'recomposer', lines: [1, 2, 3] },
        logEvents: [{ t: t += 2, kind: 'frame', subject: 'recomposer' }] }));
      out.push(S(m, 'recompose', { params: { n: n }, activeNodes: ['recomposer', 'composition', 'composer'], movingSignals: [{ edge: 'e1', tok: 'runtime' }],
        stateBefore: [{ labelKey: M(m, 'st.pending'), value: String(n) }], stateAfter: [{ labelKey: M(m, 'st.pending'), value: '0' }], affected: ['composition'], logEvents: [{ t: t += 2, kind: 'recompose', subject: 'composition', params: { n: n } }] }));
      out.push(S(m, 'apply', { activeNodes: ['applier'], affected: ['uitree'], changes: [{ op: 'set', textKey: M(m, 'ch.applied') }], logEvents: [{ t: t += 2, kind: 'apply', subject: 'applier' }] }));
      out[out.length - 1].metrics = { writes: n, passes: 1 };
      return out;
    }
    reg(m, {
      simpExtra: [M(m, 'simp.2')],
      controls: [
        { id: 'writes', type: 'select', labelKey: M(m, 'ctl.writes'), get: function (s) { return s.writes; }, action: 'writes', options: [1, 2, 3].map(function (v) { return { value: v, labelKey: M(m, 'ctl.writes.n'), params: { n: v } }; }) },
        { id: 'paused', type: 'toggle', labelKey: M(m, 'ctl.paused'), get: function (s) { return s.paused; }, action: 'paused' }
      ],
      init: function () { return { writes: 1, paused: false }; },
      act: function (s, a, v) { var n = { writes: s.writes, paused: s.paused }; if (a === 'writes') n.writes = Math.max(1, Math.min(3, v | 0)); else n.paused = !!v; return n; },
      steps: steps,
      selfChecks: [{ name: 'nhiều lần ghi trước frame → một lượt recompose (mô hình)', run: function () { return steps({ writes: 3, paused: false }).filter(function (x) { return x.id === 'recompose'; }).length === 1; } }]
    });
  })();

  /* ================= B6: Composer ghi nhận, Applier áp dụng (reference Applier; how-compose-works.md) ================= */
  (function () {
    var m = 'applier';
    var OPS = { text: ['update'], insert: ['insert'], remove: ['remove'], move: ['move'], insert2: ['insert', 'insert'] };
    function steps(s) {
      var out = [], t = 0, ops = OPS[s.change], calls = s.change === 'insert2' ? 1 : ops.length;
      out.push(S(m, 'compute', { type: 'scenario', titleKey: M(m, 's.compute.title'), explainKey: M(m, 's.compute.' + s.change), activeNodes: ['composer', 'slots'],
        changes: ops.map(function (o) { return { op: o === 'remove' ? 'remove' : o === 'update' ? 'set' : 'add', textKey: M(m, 'ch.' + o) }; }),
        logEvents: [{ t: t, kind: 'recompose', subject: 'composer' }] }));
      out.push(S(m, 'begin', { activeNodes: ['applier'], codeHighlight: { snippet: 'applier', lines: [2] }, logEvents: [{ t: t += 10, kind: 'apply', subject: 'applier' }] }));
      var NB = 3, NA = { text: 3, insert: 4, insert2: 5, remove: 2, move: 3 }[s.change];
      out.push(S(m, 'ops', { explainKey: M(m, 's.ops.' + s.change), params: { calls: calls }, activeNodes: ['applier', 'uitree'], affected: ['uitree'],
        stateBefore: [{ labelKey: M(m, 'st.nodes'), value: String(NB) }], stateAfter: [{ labelKey: M(m, 'st.nodes'), value: String(NA) }], movingSignals: [{ edge: 'e7', tok: 'ui' }],
        codeHighlight: { snippet: 'applier', lines: s.change === 'text' ? [7] : s.change === 'remove' ? [5] : s.change === 'move' ? [6] : [3, 4] },
        callouts: s.change === 'insert2' ? [{ kind: 'mechanism', textKey: M(m, 'co.coalesce') }] : s.change === 'text' ? [{ kind: 'mechanism', textKey: M(m, 'co.noStructure') }] : [],
        logEvents: [{ t: t += 10, kind: 'apply', subject: 'uitree', detailKey: M(m, 'ev.ops.' + s.change), params: { calls: calls } }] }));
      out.push(S(m, 'end', { activeNodes: ['applier'], codeHighlight: { snippet: 'applier', lines: [8] }, callouts: [{ kind: 'android', textKey: M(m, 'co.android') }],
        logEvents: [{ t: t += 10, kind: 'apply', subject: 'applier' }] }));
      out[out.length - 1].metrics = { calls: calls };
      return out;
    }
    reg(m, {
      controls: [{ id: 'change', type: 'select', labelKey: M(m, 'ctl.change'), get: function (s) { return s.change; }, action: 'change',
        options: ['text', 'insert', 'insert2', 'remove', 'move'].map(function (v) { return { value: v, labelKey: M(m, 'ctl.change.' + v) }; }) }],
      init: function () { return { change: 'text' }; },
      act: function (s, a, v) { return { change: OPS[v] ? v : s.change }; },
      steps: steps,
      selfChecks: [{ name: 'hai lần chèn liền kề gộp thành một lời gọi Applier (theo how-compose-works.md)', run: function () { return steps({ change: 'insert2' })[3].metrics.calls === 1; } }]
    });
  })();

  /* ================= B7: đọc state ở phase nào thì phase đó chạy lại (trang Compose phases) =================
     composition: recompose, rồi layout/draw nếu nội dung, kích thước, vị trí đổi (ở đây chữ đổi nên có);
     layout (Modifier.offset {}): layout (placement), draw nếu vị trí đổi; draw (drawBehind): chỉ draw. */
  var PH = R.phases = {};
  PH.rerun = function (where) {
    return { composition: where === 'composition', layout: where === 'composition' || where === 'layout', draw: true };
  };
  (function () {
    var m = 'phases';
    function lamp(on) { return on ? ST('rerun') : ST('skipped'); }
    function steps(s) {
      var r = PH.rerun(s.where), out = [], t = 0;
      var ns = { comp: ST('idle'), layout: ST('idle'), draw: ST('idle') };
      out.push(S(m, 'where', { type: 'scenario', explainKey: M(m, 's.where.' + s.where), activeNodes: [s.where === 'composition' ? 'comp' : s.where], nodeStates: ns,
        codeHighlight: { snippet: 'phases', lines: s.where === 'composition' ? [3] : s.where === 'layout' ? [5] : [7] },
        callouts: [{ kind: 'try', textKey: M(m, 'co.try') }], logEvents: [{ t: t, kind: 'observe', subject: s.where === 'composition' ? 'comp' : s.where, detailKey: M(m, 'ev.read.' + s.where) }] }));
      out.push(S(m, 'write', { activeNodes: ['state'], movingSignals: [{ edge: s.where === 'composition' ? 'e1' : s.where === 'layout' ? 'e2' : 'e3', tok: 'state' }], nodeStates: ns,
        stateBefore: [{ labelKey: M(m, 'st.value'), value: '0' }], stateAfter: [{ labelKey: M(m, 'st.value'), value: '1' }], logEvents: [{ t: t += 10, kind: 'write', subject: 'state' }] }));
      ['comp', 'layout', 'draw'].forEach(function (ph) {
        var on = ph === 'comp' ? r.composition : r[ph]; ns = JSON.parse(JSON.stringify(ns)); ns[ph] = lamp(on);
        var o = S(m, ph, { titleKey: M(m, 's.' + ph + '.title'), explainKey: M(m, 's.' + ph + '.' + (on ? 'run' : 'skip') + '.' + s.where), activeNodes: [ph], nodeStates: ns,
          logEvents: [{ t: t += 10, kind: on ? (ph === 'comp' ? 'recompose' : ph) : 'skip', subject: ph, detailKey: M(m, 'ev.' + (on ? 'run' : 'skip')), params: { ph: ph } }] });
        if (!on) o.skipped = [{ whatKey: M(m, 'sk.' + ph), whyKey: M(m, 'sk.notRead') }];
        o.metrics = {}; o.metrics[ph] = on ? M(m, 'val.run') : M(m, 'val.skip');
        out.push(o);
      });
      if (s.backwards) {
        out.push(S(m, 'loop', { type: 'pitfall', activeNodes: ['layout', 'state'], nodeStates: ns, callouts: [{ kind: 'pitfall', textKey: M(m, 'co.loop') }],
          codeHighlight: { snippet: 'phases', lines: [9, 10] }, logEvents: [{ t: t += 10, kind: 'write', subject: 'state', detailKey: M(m, 'ev.loop') }, { t: t += 10, kind: 'frame', subject: 'comp', detailKey: M(m, 'ev.extraFrame') }] }));
      }
      var last = out[out.length - 1];
      last.metrics = { comp: r.composition ? M(m, 'val.run') : M(m, 'val.skip'), layout: r.layout ? M(m, 'val.run') : M(m, 'val.skip'), draw: M(m, 'val.run'), frames: s.backwards ? 2 : 1 };
      return out;
    }
    reg(m, {
      controls: [
        { id: 'where', type: 'select', labelKey: M(m, 'ctl.where'), get: function (s) { return s.where; }, action: 'where',
          options: ['composition', 'layout', 'draw'].map(function (v) { return { value: v, labelKey: M(m, 'ctl.where.' + v) }; }) },
        { id: 'backwards', type: 'toggle', labelKey: M(m, 'ctl.backwards'), get: function (s) { return s.backwards; }, action: 'backwards' }
      ],
      init: function () { return { where: 'composition', backwards: false }; },
      act: function (s, a, v) { var n = { where: s.where, backwards: s.backwards }; if (a === 'where') n.where = v; else n.backwards = !!v; return n; },
      steps: steps,
      selfChecks: [{ name: 'đọc trong draw: chỉ draw chạy lại; đọc trong layout: layout + draw; đọc trong composition: cả ba', run: function () {
        var a = PH.rerun('draw'), b = PH.rerun('layout'), c = PH.rerun('composition');
        return !a.composition && !a.layout && a.draw && !b.composition && b.layout && c.composition && c.layout;
      } }]
    });
  })();

  /* ================= B8: skip và stability (trang Stability, Strong skipping; Kotlin ≥ 2.0.20 bật mặc định) =================
     stable → so bằng equals; unstable + strong skipping → so ===; unstable + tắt strong skipping → không skip được. */
  var SK = R.skip = {};
  SK.decide = function (param, strong) {
    // param: 'stableSame' | 'stableEqual' | 'unstableSame' | 'unstableEqual'
    var stable = param.indexOf('stable') === 0, sameInstance = /Same$/.test(param);
    if (stable) return { skip: true, how: 'equals' };            // giá trị bằng nhau theo equals trong cả hai trường hợp
    if (!strong) return { skip: false, how: 'never' };
    return { skip: sameInstance, how: 'identity' };
  };
  (function () {
    var m = 'skip';
    function steps(s) {
      var d = SK.decide(s.param, s.strong), out = [], P = { how: d.how };
      out.push(S(m, 'parent', { type: 'scenario', activeNodes: ['parent'], params: P, codeHighlight: { snippet: 'skip', lines: [1, 2, 3] }, logEvents: [{ t: 0, kind: 'recompose', subject: 'parent' }] }));
      out.push(S(m, 'param', { explainKey: M(m, 's.param.' + s.param), activeNodes: ['parent', 'child'], movingSignals: [{ edge: 'e1', tok: 'runtime' }], params: P,
        stateAfter: [{ labelKey: M(m, 'st.stability'), valueKey: M(m, s.param.indexOf('stable') === 0 ? 'val.stable' : 'val.unstable') }, { labelKey: M(m, 'st.strong'), valueKey: M(m, s.strong ? 'val.on' : 'val.off') }],
        codeHighlight: { snippet: 'skip', lines: s.param.indexOf('stable') === 0 ? [5] : [6] }, logEvents: [{ t: 10, kind: 'observe', subject: 'child' }] }));
      out.push(S(m, 'compare', { explainKey: M(m, 's.compare.' + d.how), activeNodes: ['child'], params: P, callouts: [{ kind: 'source', textKey: M(m, 'co.version') }],
        logEvents: [{ t: 20, kind: 'observe', subject: 'child', detailKey: M(m, 'ev.compare.' + d.how) }] }));
      var o = S(m, d.skip ? 'skipped' : 'recomposed', { activeNodes: ['child'], params: P, nodeStates: { child: ST(d.skip ? 'skippedNode' : 'recomposedNode') },
        logEvents: [{ t: 30, kind: d.skip ? 'skip' : 'recompose', subject: 'child' }] });
      if (d.skip) o.skipped = [{ whatKey: M(m, 'sk.child'), whyKey: M(m, 'sk.' + d.how) }]; else o.callouts = [{ kind: 'mechanism', textKey: M(m, 'co.correct') }];
      o.metrics = { child: d.skip ? M(m, 'val.skipped') : M(m, 'val.recomposed') };
      out.push(o);
      return out;
    }
    reg(m, {
      simpExtra: [M(m, 'simp.2')],
      controls: [
        { id: 'param', type: 'select', labelKey: M(m, 'ctl.param'), get: function (s) { return s.param; }, action: 'param',
          options: ['stableSame', 'stableEqual', 'unstableSame', 'unstableEqual'].map(function (v) { return { value: v, labelKey: M(m, 'ctl.param.' + v) }; }) },
        { id: 'strong', type: 'toggle', labelKey: M(m, 'ctl.strong'), get: function (s) { return s.strong; }, action: 'strong' }
      ],
      init: function () { return { param: 'unstableEqual', strong: true }; },
      act: function (s, a, v) { var n = { param: s.param, strong: s.strong }; if (a === 'param') n.param = v; else n.strong = !!v; return n; },
      steps: steps,
      selfChecks: [{ name: 'bảng quyết định skip theo tài liệu Stability/Strong skipping', run: function () {
        return SK.decide('stableEqual', false).skip && SK.decide('unstableSame', true).skip && !SK.decide('unstableEqual', true).skip && !SK.decide('unstableSame', false).skip;
      } }]
    });
  })();

  /* ================= B9: semantics tree (trang Semantics) =================
     Accessibility service dùng cây unmerged và tự gộp; testing framework mặc định dùng cây merged.
     Button/clickable gộp con cháu (mergeDescendants). */
  (function () {
    var m = 'semantics';
    function steps(s) {
      var out = [], P = {};
      var seen = s.consumer === 'test' ? (s.merge ? 1 : 3) : 3;
      out.push(S(m, 'compose', { type: 'scenario', activeNodes: ['ui'], codeHighlight: { snippet: 'semantics', lines: [1, 2, 3, 4] }, logEvents: [{ t: 0, kind: 'apply', subject: 'ui' }] }));
      out.push(S(m, 'tree', { activeNodes: ['sem'], movingSignals: [{ edge: 'e1', tok: 'ui' }], callouts: [{ kind: 'mechanism', textKey: M(m, 'co.parallel') }], logEvents: [{ t: 10, kind: 'apply', subject: 'sem' }] }));
      out.push(S(m, 'merge', { explainKey: M(m, s.merge ? 's.merge.on' : 's.merge.off'), activeNodes: ['sem'], affected: ['sem'],
        stateBefore: [{ labelKey: M(m, 'st.merged'), value: '3' }], stateAfter: [{ labelKey: M(m, 'st.merged'), value: s.merge ? '1' : '3' }], nodeStates: { sem: ST(s.merge ? 'merged' : 'unmerged') },
        codeHighlight: { snippet: 'semantics', lines: s.merge ? [1] : [6] }, logEvents: [{ t: 20, kind: 'observe', subject: 'sem' }] }));
      out.push(S(m, 'consume', { explainKey: M(m, 's.consume.' + s.consumer + (s.merge ? '.merged' : '.plain')), params: { n: seen },
        activeNodes: [s.consumer === 'test' ? 'test' : 'a11y'], movingSignals: [{ edge: s.consumer === 'test' ? 'e3' : 'e2', tok: 'ui' }],
        stateAfter: [{ labelKey: M(m, 'st.nodes'), value: String(seen) }], callouts: [{ kind: 'source', textKey: M(m, 'co.x6') }],
        logEvents: [{ t: 30, kind: 'observe', subject: s.consumer === 'test' ? 'test' : 'a11y', params: { n: seen } }] }));
      out[out.length - 1].metrics = { nodes: seen };
      return out;
    }
    reg(m, {
      controls: [
        { id: 'merge', type: 'toggle', labelKey: M(m, 'ctl.merge'), get: function (s) { return s.merge; }, action: 'merge' },
        { id: 'consumer', type: 'select', labelKey: M(m, 'ctl.consumer'), get: function (s) { return s.consumer; }, action: 'consumer',
          options: ['a11y', 'test'].map(function (v) { return { value: v, labelKey: M(m, 'ctl.consumer.' + v) }; }) }
      ],
      init: function () { return { merge: true, consumer: 'test' }; },
      act: function (s, a, v) { var n = { merge: s.merge, consumer: s.consumer }; if (a === 'merge') n.merge = !!v; else n.consumer = v === 'a11y' ? 'a11y' : 'test'; return n; },
      steps: steps,
      selfChecks: [{ name: 'test mặc định thấy cây merged (1 node cho Button); accessibility nhận cây unmerged', run: function () {
        return steps({ merge: true, consumer: 'test' })[3].metrics.nodes === 1 && steps({ merge: true, consumer: 'a11y' })[3].metrics.nodes === 3;
      } }]
    });
  })();

  /* ================= B10: luồng +1 đầy đủ (8 bước) ================= */
  (function () {
    var m = 'counter';
    function steps(s) {
      var c0 = s.start, c1 = s.start + 1, structural = c0 === 0, childSkip = SK.decide(s.child === 'stable' ? 'stableEqual' : 'unstableEqual', true).skip;
      var B = function (v) { return [{ labelKey: M(m, 'st.count'), value: String(v) }]; }, P = { c0: c0, c1: c1 }, out = [];
      out.push(S(m, 's1', { type: 'scenario', params: P, activeNodes: ['uitree', 'snapshot'], movingSignals: [{ edge: 'e9', tok: 'state' }], stateBefore: B(c0), stateAfter: B(c1),
        affected: ['snapshot'], codeHighlight: { snippet: 'counter', lines: [7] }, typing: { node: 'snapshot', code: 'count++' },
        changes: [{ op: 'set', textKey: M(m, 'ch.write'), params: P }], logEvents: [{ t: 0, kind: 'write', subject: 'snapshot' }] }));
      out.push(S(m, 's2', { params: P, activeNodes: ['snapshot'], stateBefore: B(c1), stateAfter: B(c1), callouts: [{ kind: 'mechanism', textKey: M(m, 'co.snapshot') }],
        logEvents: [{ t: 2, kind: 'apply', subject: 'snapshot' }] }));
      out.push(S(m, 's3', { params: P, activeNodes: ['snapshot', 'composition'], movingSignals: [{ edge: 'e5', tok: 'state' }], affected: ['composition'], stateBefore: B(c1), stateAfter: B(c1),
        codeHighlight: { snippet: 'counter', lines: [2, 4] }, logEvents: [{ t: 4, kind: 'invalidate', subject: 'composition' }] }));
      out.push(S(m, 's4', { params: P, activeNodes: ['recomposer'], stateBefore: B(c1), stateAfter: B(c1), logEvents: [{ t: 6, kind: 'schedule', subject: 'recomposer' }] }));
      out.push(S(m, 's5', { params: P, activeNodes: ['composer', 'slots'], movingSignals: [{ edge: 'e4', tok: 'runtime' }], affected: ['composer'], stateBefore: B(c1), stateAfter: B(c1),
        codeHighlight: { snippet: 'counter', lines: [4, 5] }, changes: [{ op: 'set', textKey: M(m, 'ch.text'), params: P }].concat(structural ? [{ op: 'add', textKey: M(m, 'ch.badge') }] : []),
        logEvents: [{ t: 16, kind: 'recompose', subject: 'composer' }] }));
      var s6 = S(m, 's6', { explainKey: M(m, childSkip ? 's6.skip' : 's6.recompose'), params: P, activeNodes: ['composer'], stateBefore: B(c1), stateAfter: B(c1), codeHighlight: { snippet: 'counter', lines: [6, 7] },
        logEvents: [{ t: 18, kind: childSkip ? 'skip' : 'recompose', subject: 'composer', detailKey: M(m, childSkip ? 'ev.s6.skip' : 'ev.s6.recompose') }] });
      s6.skipped = childSkip ? [{ whatKey: M(m, 'sk.header'), whyKey: M(m, 'sk.headerStable') }, { whatKey: M(m, 'sk.button'), whyKey: M(m, 'sk.buttonSame') }] : [{ whatKey: M(m, 'sk.button'), whyKey: M(m, 'sk.buttonSame') }];
      if (!childSkip) s6.callouts = [{ kind: 'pitfall', textKey: M(m, 'co.unstable') }];
      out.push(s6);
      out.push(S(m, 's7', { explainKey: M(m, structural ? 's7.insert' : 's7.update'), params: P, activeNodes: ['applier', 'uitree'], movingSignals: [{ edge: 'e7', tok: 'ui' }], affected: ['uitree'],
        stateBefore: B(c1), stateAfter: B(c1), changes: structural ? [{ op: 'add', textKey: M(m, 'ch.insertNode') }, { op: 'set', textKey: M(m, 'ch.updateNode'), params: P }] : [{ op: 'set', textKey: M(m, 'ch.updateNode'), params: P }],
        logEvents: [{ t: 20, kind: 'apply', subject: 'applier', detailKey: M(m, structural ? 'ev.s7.insert' : 'ev.s7.update') }] }));
      out.push(S(m, 's8', { explainKey: M(m, structural ? 's8.structural' : 's8.text'), params: P, activeNodes: ['phases'], movingSignals: [{ edge: 'e8', tok: 'ui' }], stateBefore: B(c1), stateAfter: B(c1),
        callouts: [{ kind: 'source', textKey: M(m, 'co.x1') }],
        logEvents: [{ t: 24, kind: 'layout', subject: 'phases' }, { t: 26, kind: 'draw', subject: 'phases' }] }));
      // dải chỉ số điền dần: count từ bước 1; số composable recompose/skip từ bước 5 và 6 (minh họa cho ví dụ này)
      out[0].metrics = { count: c1 };
      out[4].metrics = { recomposed: 2, skipped: 0 };
      out[5].metrics = { recomposed: childSkip ? 2 : 3, skipped: childSkip ? 2 : 1 };
      out.forEach(function (o) { o.simplificationKeys = [M(m, 'simp.1')]; });
      return out;
    }
    reg(m, {
      simpExtra: [M(m, 'simp.2')],
      controls: [
        { id: 'start', type: 'select', labelKey: M(m, 'ctl.start'), get: function (s) { return s.start; }, action: 'start', options: [0, 5].map(function (v) { return { value: v, labelKey: M(m, 'ctl.start.n'), params: { n: v } }; }) },
        { id: 'child', type: 'select', labelKey: M(m, 'ctl.child'), get: function (s) { return s.child; }, action: 'child', options: ['stable', 'unstable'].map(function (v) { return { value: v, labelKey: M(m, 'ctl.child.' + v) }; }) }
      ],
      init: function () { return { start: 0, child: 'stable' }; },
      act: function (s, a, v) { var n = { start: s.start, child: s.child }; if (a === 'start') n.start = v === 5 ? 5 : 0; else n.child = v === 'unstable' ? 'unstable' : 'stable'; return n; },
      steps: steps,
      selfChecks: [
        { name: 'luôn đủ 8 bước, mỗi bước có state trước/sau', run: function () { return [0, 5].every(function (c) { var st = steps({ start: c, child: 'stable' }); return st.length === 8 && st.every(function (x) { return x.stateBefore && x.stateAfter; }); }); } },
        { name: 'đếm từ 5: Applier chỉ cập nhật, không chèn node', run: function () { return steps({ start: 5, child: 'stable' })[6].changes.length === 1; } }
      ]
    });
  })();

  /* ================= DC (v2): thân composable chạy bao nhiêu lần? (Thinking in Compose: fast, idempotent, side-effect free) =================
     Kịch bản của site: Counter(count) có side effect `sentCount++` đặt TRONG THÂN hoặc TRONG CALLBACK onClick.
     Có animation (Modifier.scale đọc giá trị animate trong composition) thì mỗi lần bấm thân chạy thêm 2 frame (giả định).
     Lần bấm 3 và 4 sát nhau: recomposition cho count = 3 bị hủy và chạy lại với count = 4. Tài liệu nói Compose CÓ THỂ hủy
     recomposition ("optimistic"); site minh hoạ hệ quả, không khẳng định thời điểm cụ thể của runtime. */
  (function () {
    var m = 'runs';
    function steps(s) {
      var out = [], t = 0, st = { taps: 0, runs: 0, fx: 0, shown: 0 }, inBody = s.where === 'body';
      var snap = function () { return { taps: st.taps, runs: st.runs, effects: st.fx, shown: st.shown }; };
      var body = function (count, cancelled) { st.runs++; if (inBody) st.fx++; if (!cancelled) st.shown = count; };
      var P = function (id, o) { o.metrics = snap(); o.params = o.params || {}; o.params.count = o.params.count != null ? o.params.count : st.shown; o.params.runs = st.runs; o.params.fx = st.fx;
        o.titleKey = M(m, 's.' + id + '.title'); o.explainKey = M(m, 's.' + id + '.explain'); (o.logEvents || []).forEach(function (e) { e.detailKey = M(m, 'ev.' + id); e.params = e.params || o.params; });
        out.push(S(m, id + out.length, o)); };
      var L = function (kind, subject, extra) { var e = { t: t += 4, kind: kind, subject: subject }; for (var k in extra || {}) e[k] = extra[k]; return [e]; };
      var lines = function (a) { return { snippet: 'runs' + (inBody ? 'Body' : 'Cb') + (s.anim ? 'Anim' : ''), lines: a }; };
      body(0);
      P('first', { type: 'scenario', activeNodes: ['body'], affected: inBody ? ['effect'] : [], codeHighlight: lines(inBody ? [3, 4] : [3]),
        callouts: inBody ? [{ kind: 'pitfall', textKey: M(m, 'co.firstBody') }] : [], logEvents: L('recompose', 'body') });
      function tap(n, fast) {
        st.taps++; if (!inBody) st.fx++;
        P(fast ? 'tapFast' : 'tap', { params: { n: n }, activeNodes: ['tap'], affected: inBody ? [] : ['effect'], codeHighlight: lines([7]), logEvents: L('act', 'tap', { params: { n: n } }) });
        P('write', { params: { n: n }, activeNodes: ['state', 'recomposer'], codeHighlight: lines([7]), logEvents: L('invalidate', 'recomposer', { params: { n: n } }) });
      }
      function recompose(n) {
        body(n);
        P('recompose', { params: { count: n }, activeNodes: ['body'], affected: inBody ? ['effect', 'screen'] : ['screen'], codeHighlight: lines(inBody ? [3, 4, 9] : [3, 9]), logEvents: L('recompose', 'body', { params: { count: n } }) });
        if (s.anim) { body(n); body(n);
          P('anim', { params: { count: n }, activeNodes: ['body'], affected: inBody ? ['effect'] : [], codeHighlight: lines([5, 8]), callouts: n === 1 ? [{ kind: 'mechanism', textKey: M(m, 'co.anim') }] : [], logEvents: L('frame', 'body') }); }
      }
      tap(1); recompose(1);
      tap(2); recompose(2);
      tap(3, false);
      body(3, true);
      P('start3', { params: { count: 3 }, activeNodes: ['body'], affected: inBody ? ['effect'] : [], codeHighlight: lines(inBody ? [3, 4] : [3]), logEvents: L('recompose', 'body', { params: { count: 3 } }) });
      st.taps++; if (!inBody) st.fx++;
      P('cancel', { type: 'pitfall', params: { n: 4 }, activeNodes: ['tap', 'recomposer'], codeHighlight: lines([7]), callouts: [{ kind: inBody ? 'pitfall' : 'mechanism', textKey: M(m, inBody ? 'co.cancelBody' : 'co.cancelCb') }],
        logEvents: L('cancel', 'recomposer', { params: { n: 4 } }) });
      recompose(4);
      P('end', { activeNodes: ['screen'], callouts: [{ kind: inBody ? 'pitfall' : 'mechanism', textKey: M(m, 'co.end.' + s.where) }], logEvents: L('complete', 'screen') });
      return out;
    }
    reg(m, {
      codeId: 'runsBodyAnim',
      simpExtra: [M(m, 'simp.2')],
      controls: [
        { id: 'where', type: 'select', labelKey: M(m, 'ctl.where'), get: function (s) { return s.where; }, action: 'where', options: ['body', 'callback'].map(function (v) { return { value: v, labelKey: M(m, 'ctl.where.' + v) }; }) },
        { id: 'anim', type: 'toggle', labelKey: M(m, 'ctl.anim'), get: function (s) { return s.anim; }, action: 'anim' }
      ],
      init: function () { return { where: 'body', anim: true }; },
      act: function (s, a, v) { var n = { where: s.where, anim: s.anim }; if (a === 'where') n.where = v === 'callback' ? 'callback' : 'body'; else n.anim = !!v; return n; },
      steps: steps,
      selfChecks: [{ name: 'side effect trong thân đếm theo số lần thân chạy (11 với animation, 5 không), trong callback đếm theo số lần bấm (4)', run: function () {
        var last = function (w, a) { var x = steps({ where: w, anim: a }); return x[x.length - 1].metrics; };
        var b = last('body', true), b0 = last('body', false), c = last('callback', true);
        return b.taps === 4 && b.runs === 11 && b.effects === 11 && b0.runs === 5 && b0.effects === 5 && c.effects === 4 && c.runs === 11 && b.shown === 4;
      } }]
    });
  })();

  /* ================= B2 (v2): group, slot, changed(), skip và restart theo how-compose-works.md @296313a4 =================
     B(person) gọi A(person.givenName), A(person.familyName). Lượt 1 là composition đầu (chèn group, ghi slot); lượt 2 là
     recomposition sau một thay đổi do người dùng chọn. Tên hàm theo tài liệu (skipToEndGroup); bản thật ở commit ghim là
     skipToGroupEnd, startReplaceGroup… (ghi trong chương). `skipping` theo getter của GapComposer @296313a4:
     !inserting && !reusing && !providersInvalid && currentRecomposeScope?.requiresRecompose == false && !forciblyRecompose.
     hypo = mã GIẢ ĐỊNH (compiler không sinh): changed() nằm trong điều kiện short-circuit → số slot của group B thay đổi giữa các lượt. */
  (function () {
    var m = 'groups';
    var CHG = ['none', 'newPerson', 'stateField', 'plainVar'];
    function steps(s) {
      var out = [], t = 0, hypo = !!s.hypo, ch = s.change;
      var st = { groups: 0, slots: 0, runs: 0, skipped: 0, shown: '' }, slotB = [], slotA1 = [], slotA2 = [];
      var snip = hypo ? 'grpHypo' : 'grp';
      var slotsVal = function () {
        var f = function (a) { return '[' + a.join(', ') + ']'; };
        return 'B ' + f(slotB) + (slotA1.length ? ' · A₁ ' + f(slotA1) : '') + (slotA2.length ? ' · A₂ ' + f(slotA2) : '');
      };
      var P = function (id, o) {
        o.metrics = { groups: st.groups, slots: st.slots, runs: st.runs, skipped: st.skipped, shown: st.shown || '—' };
        o.params = o.params || {}; o.params.shown = st.shown || '—'; o.params.slots = st.slots; o.params.groups = st.groups;
        o.codeHighlight = { snippet: snip, lines: o.lines || [] }; delete o.lines;
        o.stateAfter = (o.stateAfter || []).concat([{ labelKey: M(m, 'st.slots'), value: slotsVal() }]);
        var key = o.key || id; delete o.key;
        o.titleKey = M(m, 's.' + key + '.title'); o.explainKey = M(m, 's.' + key + '.explain');
        (o.logEvents || []).forEach(function (e) { e.detailKey = M(m, 'ev.' + key); });
        out.push(S(m, id + out.length, o));
      };
      var L = function (kind, subject) { return [{ t: t += 4, kind: kind, subject: subject }]; };
      // ---- lượt 1: composition đầu (inserting = true → skipping = false) ----
      st.groups = 1;
      P('f.startB', { type: 'scenario', activeNodes: ['caller', 'code', 'composer', 'groups'], movingSignals: [{ edge: 'e1', tok: 'runtime' }, { edge: 'e2', tok: 'runtime' }], lines: [3],
        callouts: [{ kind: 'mechanism', textKey: M(m, 'co.names') }], logEvents: L('recompose', 'composer') });
      if (hypo) {
        P('f.changedB', { key: 'f.hypoB', type: 'pitfall', activeNodes: ['composer'], lines: [4, 5], callouts: [{ kind: 'pitfall', textKey: M(m, 'co.hypo') }], logEvents: L('observe', 'composer') });
      } else {
        slotB = ['Person(Ana, Le)']; st.slots = 1;
        P('f.changedB', { activeNodes: ['composer', 'slots'], movingSignals: [{ edge: 'e3', tok: 'state' }], lines: [4, 5], logEvents: L('write', 'slots') });
      }
      st.groups = 2; slotA1 = ['Data#1', '"Ana"']; st.slots += 2; st.shown = 'Ana';
      P('f.A1', { activeNodes: ['code', 'composer', 'groups', 'slots', 'screen'], movingSignals: [{ edge: 'e3', tok: 'state' }, { edge: 'e6', tok: 'ui' }], lines: [6, 14, 15, 16, 17, 19],
        changes: [{ op: 'add', textKey: M(m, 'ch.text1') }], logEvents: L('apply', 'screen') });
      st.groups = 3; slotA2 = ['Data#2', '"Le"']; st.slots += 2; st.shown = 'Ana Le';
      P('f.A2', { activeNodes: ['code', 'composer', 'groups', 'slots', 'screen'], movingSignals: [{ edge: 'e6', tok: 'ui' }], lines: [7, 14, 15, 16, 17, 19],
        changes: [{ op: 'add', textKey: M(m, 'ch.text2') }], logEvents: L('apply', 'screen') });
      var reads = ch === 'stateField';
      P('f.endB', { key: reads ? 'f.endScope' : 'f.endNull', activeNodes: ['composer', 'scope'], movingSignals: reads ? [{ edge: 'e4', tok: 'state' }] : [], lines: [11],
        stateAfter: [{ labelKey: M(m, 'st.scope'), valueKey: M(m, reads ? 'val.scope' : 'val.null') }], logEvents: L(reads ? 'observe' : 'skip', 'scope') });
      // ---- sự kiện giữa hai lượt ----
      P('ev', { key: 'ev.' + ch, type: ch === 'plainVar' ? 'pitfall' : 'mechanism', activeNodes: ch === 'stateField' ? ['scope', 'caller'] : ['caller'],
        movingSignals: ch === 'stateField' ? [{ edge: 'e5', tok: 'state' }] : [{ edge: 'e0', tok: 'runtime' }], lines: ch === 'stateField' ? [11] : [2],
        logEvents: L(ch === 'stateField' ? 'invalidate' : ch === 'plainVar' ? 'write' : 'schedule', ch === 'stateField' ? 'scope' : 'caller') });
      // ---- lượt 2: recomposition ----
      var changedB = ch === 'newPerson', forced = ch === 'stateField', skippingB = !forced;
      P('r.startB', { activeNodes: ['code', 'composer', 'groups'], movingSignals: [{ edge: 'e1', tok: 'runtime' }], lines: [3],
        params: { skipping: String(skippingB) }, logEvents: L('recompose', 'composer') });
      if (hypo && skippingB) {   // skipping = true → lần này changed() ĐƯỢC gọi, nhưng lượt 1 không ghi slot nào cho nó
        P('r.hypo', { type: 'pitfall', activeNodes: ['composer', 'slots'], lines: [5], callouts: [{ kind: 'pitfall', textKey: M(m, 'co.hypoEnd') }], logEvents: L('observe', 'slots') });
        P('end', { key: 'end.hypo', type: 'pitfall', activeNodes: ['slots'], lines: [4, 5], logEvents: L('observe', 'slots') });
        return out;
      }
      if (changedB && !hypo) slotB = ['Person(Bo, Le)'];
      P('r.changedB', { key: 'r.changedB.' + ch, activeNodes: ['composer', 'slots'], movingSignals: [{ edge: 'e3', tok: 'state' }], lines: [4, 5],
        stateAfter: [hypo ? { labelKey: M(m, 'st.changed'), valueKey: M(m, 'val.notCalled') } : { labelKey: M(m, 'st.changed'), value: String(changedB) }, { labelKey: M(m, 'st.skipping'), value: String(skippingB) }],
        callouts: hypo ? [{ kind: 'pitfall', textKey: M(m, 'co.hypoLucky') }] : forced ? [{ kind: 'mechanism', textKey: M(m, 'co.forced') }] : ch === 'plainVar' ? [{ kind: 'pitfall', textKey: M(m, 'co.plainVar') }] : [],
        logEvents: L(changedB || forced ? 'recompose' : 'skip', 'composer') });
      if (changedB || forced) {
        st.runs++;   // thân B chạy
        slotA1 = ['Data#1', '"Bo"']; st.runs++; st.shown = 'Bo Le';
        P('r.A1', { activeNodes: ['code', 'composer', 'slots', 'screen'], movingSignals: [{ edge: 'e3', tok: 'state' }, { edge: 'e6', tok: 'ui' }], lines: [6, 15, 16, 17],
          changes: [{ op: 'set', textKey: M(m, 'ch.text1b') }], callouts: [{ kind: 'mechanism', textKey: M(m, 'co.remember') }], logEvents: L('apply', 'screen') });
        st.skipped++;
        P('r.A2', { activeNodes: ['composer', 'groups'], lines: [7, 16, 18], skipped: [{ whatKey: M(m, 'sk.a2'), whyKey: M(m, 'sk.same') }], logEvents: L('skip', 'composer') });
      } else {
        st.skipped++;
        P('r.skipB', { activeNodes: ['composer', 'groups'], lines: [8, 9], skipped: [{ whatKey: M(m, 'sk.b'), whyKey: M(m, ch === 'plainVar' ? 'sk.sameRef' : 'sk.same') }],
          callouts: [{ kind: 'mechanism', textKey: M(m, 'co.children') }], logEvents: L('skip', 'composer') });
      }
      P('r.endB', { key: reads ? 'r.endScope' : 'r.endNull', activeNodes: ['composer', 'scope'], lines: [11],
        stateAfter: [{ labelKey: M(m, 'st.scope'), valueKey: M(m, reads ? 'val.scope' : 'val.null') }], logEvents: L(reads ? 'observe' : 'skip', 'scope') });
      P('end', { key: 'end.' + ch, type: ch === 'plainVar' ? 'pitfall' : 'mechanism', activeNodes: ['screen'],
        callouts: [{ kind: ch === 'plainVar' ? 'pitfall' : 'mechanism', textKey: M(m, 'co.end.' + ch) }], logEvents: L('apply', 'screen') });
      return out;
    }
    reg(m, {
      codeId: 'grp',
      simpExtra: [M(m, 'simp.2')],
      controls: [
        { id: 'change', type: 'select', labelKey: M(m, 'ctl.change'), get: function (s) { return s.change; }, action: 'change', options: CHG.map(function (v) { return { value: v, labelKey: M(m, 'ctl.change.' + v) }; }) },
        { id: 'hypo', type: 'toggle', labelKey: M(m, 'ctl.hypo'), get: function (s) { return s.hypo; }, action: 'hypo' }
      ],
      init: function () { return { change: 'stateField', hypo: false }; },
      act: function (s, a, v) { var n = { change: s.change, hypo: s.hypo }; if (a === 'change') n.change = CHG.indexOf(v) >= 0 ? v : 'none'; else n.hypo = !!v; return n; },
      steps: steps,
      selfChecks: [{ name: 'composition đầu: 3 group, 5 slot; lượt 2: newPerson/stateField chạy B + A₁ và skip A₂ (hiện "Bo Le"), none/plainVar skip B (plainVar vẫn hiện "Ana Le"); giả định: B không có slot', run: function () {
        var last = function (c, h) { var x = steps({ change: c, hypo: h }); return x[x.length - 1].metrics; };
        var first = steps({ change: 'none', hypo: false })[3].metrics;
        var n = last('none'), np = last('newPerson'), sf = last('stateField'), pv = last('plainVar'), hy = steps({ change: 'none', hypo: true });
        return first.groups === 3 && first.slots === 5 && n.runs === 0 && n.skipped === 1 && n.shown === 'Ana Le' &&
          np.runs === 2 && np.skipped === 1 && np.shown === 'Bo Le' && sf.runs === 2 && sf.shown === 'Bo Le' &&
          pv.runs === 0 && pv.shown === 'Ana Le' && hy[3].metrics.slots === 4 && hy[hy.length - 1].titleKey === M(m, 's.end.hypo.title');
      } }]
    });
  })();

  /* ================= B3 (v2): phát hiện thay đổi cấu trúc theo how-compose-works.md @296313a4 =================
     Recomposition phát lại chuỗi group và so với bảng cũ. Khớp thì đi tiếp; lệch lần đầu thì các group còn lại của group cha
     được đưa vào một bảng băm (Pending) theo key; group mới tìm thấy trong Pending → giữ (có thể lên lịch di chuyển);
     không thấy → chèn vào insert table; hết group (/G) mà Pending còn → xóa. Key trùng được trả theo thứ tự cũ.
     Kịch bản là các ví dụ ShowPerson và Counters của tài liệu; số thao tác Applier theo mô tả của tài liệu (giản lược). */
  (function () {
    var m = 'structure';
    var SC = ['delete', 'insert', 'move', 'nogroup', 'ifgroup'];
    // mỗi bước: [khoá thông điệp, node sáng, dòng mã, trạng thái {old, seq, pending, ops, nodes}, thay đổi chỉ số]
    var DATA = {
      'delete': { snip: 'structPerson', steps: [
        ['start', ['code', 'old'], [5], { old: 'Name · Company · Email', seq: 'Name · Email', pending: '—', ops: '—', nodes: 'Text(name) · Text(company) · Text(email)' }, {}],
        ['matchName', ['composer', 'old'], [4], { pending: '—' }, { matched: 1 }],
        ['mismatchDel', ['composer', 'old', 'pending'], [8], { pending: 'Company · Email' }, {}],
        ['foundEmail', ['composer', 'pending'], [8], { pending: 'Company', ops: 'Email ↷ #5' }, { matched: 1 }],
        ['closeDelete', ['composer', 'pending', 'changes'], [9], { pending: '—', ops: 'Email ↷ #5 · ✗ Company → remove(index = 1, count = 1)' }, { deleted: 1 }],
        ['apply', ['changes', 'nodes'], [9], { nodes: 'Text(name) · Text(email)' }, { applier: 1 }],
        ['end.delete', ['nodes'], [], {}, {}]] },
      'insert': { snip: 'structPerson', steps: [
        ['start', ['code', 'old'], [5], { old: 'Name · Email', seq: 'Name · Company · Email', pending: '—', ops: '—', nodes: 'Text(name) · Text(email)' }, {}],
        ['matchName', ['composer', 'old'], [4], {}, { matched: 1 }],
        ['mismatchIns', ['composer', 'old', 'pending'], [5, 6], { pending: 'Email' }, {}],
        ['insertCompany', ['composer', 'insert'], [6], { ops: '+ Company (insert table) @ #5 → insert(index = 1)' }, { inserted: 1 }],
        ['foundEmailFront', ['composer', 'pending'], [8], { pending: '—' }, { matched: 1 }],
        ['closeNone', ['composer'], [9], {}, {}],
        ['apply', ['changes', 'nodes'], [9], { nodes: 'Text(name) · Text(company) · Text(email)' }, { applier: 1 }],
        ['end.insert', ['nodes'], [], {}, {}]] },
      'move': { snip: 'structMove', steps: [
        ['start', ['code', 'old'], [4], { old: 'Name · Company · Email', seq: 'Email · Company · Name', pending: '—', ops: '—', nodes: 'Text(name) · Text(company) · Text(email)' }, {}],
        ['mismatchMove', ['composer', 'old', 'pending'], [4, 5], { pending: 'Name · Company · Email' }, {}],
        ['moveEmail', ['composer', 'pending', 'changes'], [5], { pending: 'Name · Company', ops: 'Email ↷ #3 → move(2 → 0)' }, { moved: 1 }],
        ['moveCompany', ['composer', 'pending', 'changes'], [5], { pending: 'Name', ops: 'Email ↷ #3 → move(2 → 0) · Company ↷ #5 → move(2 → 1)' }, { moved: 1 }],
        ['nameInPlace', ['composer', 'pending'], [5], { pending: '—' }, { matched: 1 }],
        ['apply', ['changes', 'nodes'], [6], { nodes: 'Text(email) · Text(company) · Text(name)' }, { applier: 2 }],
        ['end.move', ['nodes'], [], {}, {}]] },
      'nogroup': { snip: 'structCountersNo', steps: [
        ['startCounters', ['code', 'old'], [4], { old: 'Counter(1) · Counter(5) · Counter(9)', seq: 'Counter · Counter', pending: '—', ops: '—', nodes: 'count 1 · count 5 · count 9' }, {}],
        ['matchC1', ['composer', 'old'], [3], {}, { matched: 1 }],
        ['matchC2wrong', ['composer', 'old'], [7], {}, { matched: 1 }],
        ['closeDeleteLast', ['composer', 'changes'], [8], { ops: '✗ Counter(9) → remove(index = 2)' }, { deleted: 1 }],
        ['apply', ['changes', 'nodes'], [8], { nodes: 'count 1 · count 5' }, { applier: 1 }],
        ['end.nogroup', ['nodes'], [], {}, {}]] },
      'ifgroup': { snip: 'structCounters', steps: [
        ['startCounters', ['code', 'old'], [4], { old: 'Counter(1) · <if>{Counter(5)} · Counter(9)', seq: 'Counter · <if>{} · Counter', pending: '—', ops: '—', nodes: 'count 1 · count 5 · count 9' }, {}],
        ['matchC1', ['composer', 'old'], [3], {}, { matched: 1 }],
        ['matchIf', ['composer', 'old'], [4], {}, { matched: 1 }],
        ['ifEmpty', ['composer', 'changes'], [6], { ops: '✗ <if>{Counter(5)} → remove(index = 1)' }, { deleted: 1 }],
        ['matchC3', ['composer', 'old'], [7], {}, { matched: 1 }],
        ['apply', ['changes', 'nodes'], [8], { nodes: 'count 1 · count 9' }, { applier: 1 }],
        ['end.ifgroup', ['nodes'], [], {}, {}]] }
    };
    var TYPE = { start: 'scenario', startCounters: 'scenario', matchC2wrong: 'pitfall', closeDeleteLast: 'pitfall', 'end.nogroup': 'pitfall' };
    var KIND = { start: 'recompose', startCounters: 'recompose', apply: 'apply', insertCompany: 'apply', closeDelete: 'apply', closeDeleteLast: 'apply', ifEmpty: 'apply', moveEmail: 'schedule', moveCompany: 'schedule' };
    var EDGE = { old: 'e2', pending: 'e3', insert: 'e4', changes: 'e5', nodes: 'e6' };
    function steps(s) {
      var d = DATA[s.scenario] || DATA['delete'], out = [], t = 0, cur = {}, met = { matched: 0, moved: 0, inserted: 0, deleted: 0, applier: 0 };
      d.steps.forEach(function (row) {
        var key = row[0], st = row[3], inc = row[4];
        for (var k in st) cur[k] = st[k];
        for (var j in inc) met[j] += inc[j];
        var sig = [];
        row[1].forEach(function (n) { if (EDGE[n]) sig.push({ edge: EDGE[n], tok: n === 'nodes' ? 'ui' : n === 'pending' ? 'state' : 'runtime' }); });
        out.push({
          id: key.replace('.', '_') + out.length, type: TYPE[key] || (/^end/.test(key) ? 'mechanism' : 'mechanism'),
          titleKey: M(m, 's.' + key + '.title'), explainKey: M(m, 's.' + key + '.explain'),
          activeNodes: row[1], movingSignals: /^end/.test(key) ? [] : sig, params: {},
          codeHighlight: { snippet: d.snip, lines: row[2] },
          metrics: { matched: met.matched, moved: met.moved, inserted: met.inserted, deleted: met.deleted, applier: met.applier },
          stateAfter: ['old', 'seq', 'pending', 'ops', 'nodes'].map(function (k) { return { labelKey: M(m, 'st.' + k), value: cur[k] }; }),
          callouts: /^end/.test(key) ? [{ kind: TYPE[key] === 'pitfall' ? 'pitfall' : 'mechanism', textKey: M(m, 'co.' + key) }] : key === 'mismatchDel' || key === 'mismatchMove' || key === 'mismatchIns' ? [{ kind: 'mechanism', textKey: M(m, 'co.pending') }] : [],
          logEvents: [{ t: t += 4, kind: KIND[key] || (/^match|^found|^name/.test(key) ? 'skip' : 'observe'), subject: row[1][row[1].length - 1], detailKey: M(m, 'ev.' + key), params: {} }]
        });
      });
      return out;
    }
    reg(m, {
      codeId: 'structPerson',
      simpExtra: [M(m, 'simp.2')],
      controls: [
        { id: 'scenario', type: 'select', labelKey: M(m, 'ctl.scenario'), get: function (s) { return s.scenario; }, action: 'scenario', options: SC.map(function (v) { return { value: v, labelKey: M(m, 'ctl.scenario.' + v) }; }) }
      ],
      init: function () { return { scenario: 'delete' }; },
      act: function (s, a, v) { return { scenario: SC.indexOf(v) >= 0 ? v : 'delete' }; },
      steps: steps,
      selfChecks: [{ name: 'xóa: 1 remove; chèn: 1 insert; di chuyển: 2 move; không có group <if>: xóa NHẦM Counter cuối (còn 1 · 5); có group <if>: xóa đúng Counter giữa (còn 1 · 9)', run: function () {
        var last = function (sc) { var x = steps({ scenario: sc }); return x[x.length - 1]; };
        var nodes = function (sc) { return last(sc).stateAfter[4].value; };
        return last('delete').metrics.deleted === 1 && last('insert').metrics.inserted === 1 && last('move').metrics.moved === 2 &&
          nodes('nogroup') === 'count 1 · count 5' && nodes('ifgroup') === 'count 1 · count 9' && last('delete').metrics.applier === 1;
      } }]
    });
  })();

  /* ================= B4 (v2): state record, snapshot cách ly, apply, xung đột và merge =================
     Theo Snapshot/SnapshotMutationPolicy reference và mã @296313a4: mutableStateOf mặc định structuralEqualityPolicy;
     setter không ghi nếu policy.equivalent(cũ, mới); bản ghi đọc được = bản ghi hợp lệ có snapshotId lớn nhất
     (id ≤ id snapshot, không nằm trong tập invalid); khi apply mà giá trị đã bị snapshot khác đổi: equivalent(current, applied)
     → giữ current; không thì policy.merge(previous, current, applied), null → thất bại (SnapshotApplyResult.Failure).
     counterPolicy là ví dụ trong reference: merge = current + (applied − previous). */
  (function () {
    var m = 'records';
    function steps(s) {
      var counter = s.policy === 'counter', plus = s.bWrite === 'plus20';
      var bVal = plus ? 20 : 10, out = [], t = 0, glob = 0, applied = 0, conflicts = 0;
      var recs = ['#1 = 0'];
      var outcome;
      if (!plus) outcome = 'same';                     // equivalent(10, 10) với cả hai policy
      else outcome = counter ? 'merged' : 'failed';
      var snip = plus ? 'recPlus' : 'recSet';
      var P = function (key, o) {
        o.id = key.replace(/\./g, '_') + out.length; o.type = o.type || 'mechanism';
        o.titleKey = M(m, 's.' + key + '.title'); o.explainKey = M(m, 's.' + key + '.explain');
        o.params = o.params || {}; o.params.g = glob; o.params.b = bVal;
        o.metrics = { global: glob, applied: applied, conflicts: conflicts, records: recs.length };
        o.stateAfter = [{ labelKey: M(m, 'st.records'), value: recs.join(' · ') }, { labelKey: M(m, 'st.global'), value: String(glob) }].concat(o.extra || []); delete o.extra;
        o.codeHighlight = { snippet: snip, lines: o.lines || [] }; delete o.lines;
        o.movingSignals = o.movingSignals || []; o.activeNodes = o.activeNodes || [];
        o.logEvents = [{ t: t += 4, kind: o.kind || 'write', subject: o.activeNodes[o.activeNodes.length - 1] || 'records', detailKey: M(m, 'ev.' + key), params: o.params }]; delete o.kind;
        out.push(o);
      };
      P('init', { type: 'scenario', activeNodes: ['global', 'records'], lines: [1], kind: 'observe' });
      P('take', { activeNodes: ['global', 'snapA', 'snapB'], movingSignals: [{ edge: 'e1', tok: 'state' }, { edge: 'e2', tok: 'state' }], lines: [2, 3], kind: 'observe',
        extra: [{ labelKey: M(m, 'st.readA'), value: '0' }, { labelKey: M(m, 'st.readB'), value: '0' }] });
      recs.push('#2 = 10 (A)');
      P('writeA', { activeNodes: ['snapA', 'records'], movingSignals: [{ edge: 'e3', tok: 'state' }], lines: [4],
        extra: [{ labelKey: M(m, 'st.readA'), value: '10' }, { labelKey: M(m, 'st.readB'), value: '0' }], callouts: [{ kind: 'mechanism', textKey: M(m, 'co.readable') }] });
      recs.push('#3 = ' + bVal + ' (B)');
      P('writeB', { activeNodes: ['snapB', 'records'], movingSignals: [{ edge: 'e4', tok: 'state' }], lines: [5],
        extra: [{ labelKey: M(m, 'st.readA'), value: '10' }, { labelKey: M(m, 'st.readB'), value: String(bVal) }] });
      glob = 10; applied++;
      P('applyA', { activeNodes: ['snapA', 'global', 'observers'], movingSignals: [{ edge: 'e5', tok: 'state' }, { edge: 'e7', tok: 'signal' }], lines: [6], kind: 'apply',
        callouts: [{ kind: 'mechanism', textKey: M(m, 'co.notify') }] });
      if (outcome === 'failed') {
        conflicts++;
        P('applyB.failed', { type: 'pitfall', activeNodes: ['snapB', 'policy'], movingSignals: [{ edge: 'e6', tok: 'error' }], lines: [7], kind: 'observe',
          extra: [{ labelKey: M(m, 'st.merge'), value: 'previous 0 · current 10 · applied 20 → null' }], callouts: [{ kind: 'pitfall', textKey: M(m, 'co.failed') }] });
      } else if (outcome === 'merged') {
        conflicts++; glob = 30; applied++; recs.push('#4 = 30 (merge)');
        P('applyB.merged', { activeNodes: ['snapB', 'policy', 'global', 'observers'], movingSignals: [{ edge: 'e6', tok: 'state' }, { edge: 'e7', tok: 'signal' }], lines: [7], kind: 'apply',
          extra: [{ labelKey: M(m, 'st.merge'), value: 'previous 0 · current 10 · applied 20 → 10 + (20 − 0) = 30' }], callouts: [{ kind: 'mechanism', textKey: M(m, 'co.merged') }] });
      } else {
        applied++;
        P('applyB.same', { activeNodes: ['snapB', 'policy', 'global'], movingSignals: [{ edge: 'e6', tok: 'state' }], lines: [7], kind: 'apply',
          extra: [{ labelKey: M(m, 'st.merge'), value: 'equivalent(current 10, applied 10) = true → current' }] });
      }
      P('end.' + outcome, { type: outcome === 'failed' ? 'pitfall' : 'mechanism', activeNodes: ['global'], lines: [8], kind: 'observe',
        callouts: [{ kind: outcome === 'failed' ? 'pitfall' : 'mechanism', textKey: M(m, 'co.end.' + outcome) }] });
      return out;
    }
    reg(m, {
      codeId: 'recPlus',
      simpExtra: [M(m, 'simp.2')],
      controls: [
        { id: 'policy', type: 'select', labelKey: M(m, 'ctl.policy'), get: function (s) { return s.policy; }, action: 'policy', options: ['structural', 'counter'].map(function (v) { return { value: v, labelKey: M(m, 'ctl.policy.' + v) }; }) },
        { id: 'bWrite', type: 'select', labelKey: M(m, 'ctl.bWrite'), get: function (s) { return s.bWrite; }, action: 'bWrite', options: ['plus20', 'set10'].map(function (v) { return { value: v, labelKey: M(m, 'ctl.bWrite.' + v) }; }) }
      ],
      init: function () { return { policy: 'structural', bWrite: 'plus20' }; },
      act: function (s, a, v) { var n = { policy: s.policy, bWrite: s.bWrite }; if (a === 'policy') n.policy = v === 'counter' ? 'counter' : 'structural'; else n.bWrite = v === 'set10' ? 'set10' : 'plus20'; return n; },
      steps: steps,
      selfChecks: [{ name: 'structural +20: B thất bại, global 10; counter +20: merge thành 30; ghi 10 (bằng A): apply thành công, global 10 với cả hai policy', run: function () {
        var last = function (p, b) { var x = steps({ policy: p, bWrite: b }); return x[x.length - 1].metrics; };
        var f = last('structural', 'plus20'), mg = last('counter', 'plus20'), s1 = last('structural', 'set10'), s2 = last('counter', 'set10');
        return f.global === 10 && f.applied === 1 && f.conflicts === 1 && mg.global === 30 && mg.applied === 2 && s1.global === 10 && s1.applied === 2 && s1.conflicts === 0 && s2.global === 10;
      } }]
    });
  })();

  /* ================= SH (v2): state giữ ở đâu thì sống qua sự kiện nào =================
     Theo "Save UI state in Compose" và "State and Jetpack Compose" (developer.android.com, đọc 2026-11-23):
     remember sống theo Composition; rememberSaveable dùng saved instance state (Bundle): qua đổi cấu hình và process bị hệ thống
     dừng, KHÔNG qua lúc người dùng đóng hẳn activity; ViewModel sống qua đổi cấu hình, không qua process death;
     SavedStateHandle dùng saved state nên qua process death; lưu trữ bền (DataStore/Room) qua mọi thứ ở đây. */
  (function () {
    var m = 'survive';
    var HOLD = ['remember', 'saveable', 'vm', 'handle', 'disk'];
    var EV = ['recompose', 'rotate', 'processDeath', 'dismiss'];
    var KEEP = {   // sự kiện → giữ được hay không, theo từng nơi giữ
      recompose: { remember: 1, saveable: 1, vm: 1, handle: 1, disk: 1 },
      rotate: { remember: 0, saveable: 1, vm: 1, handle: 1, disk: 1 },
      processDeath: { remember: 0, saveable: 1, vm: 0, handle: 1, disk: 1 },
      dismiss: { remember: 0, saveable: 0, vm: 0, handle: 0, disk: 1 }
    };
    var NODE = { remember: 'composition', saveable: 'bundle', vm: 'vm', handle: 'bundle', disk: 'disk' };
    var EDGE = { remember: 'e1', saveable: 'e2', vm: 'e3', handle: 'e4', disk: 'e5' };
    var LINE = { remember: 2, saveable: 3, vm: 4, handle: 5, disk: 6 };
    function steps(s) {
      var ev = EV.indexOf(s.event) >= 0 ? s.event : 'rotate', out = [], t = 0, kept = 0, lost = 0, vals = {};
      HOLD.forEach(function (h) { vals[h] = '—'; });
      var table = function () { return HOLD.map(function (h) { return { labelKey: M(m, 'h.' + h), value: vals[h] }; }); };
      var P = function (key, o) {
        o.id = key.replace(/\./g, '_') + out.length; o.type = o.type || 'mechanism';
        o.titleKey = M(m, 's.' + key + '.title'); o.explainKey = M(m, 's.' + key + '.explain');
        o.params = o.params || {}; o.metrics = { kept: kept, lost: lost, checked: kept + lost };
        o.stateAfter = table(); o.movingSignals = o.movingSignals || []; o.activeNodes = o.activeNodes || [];
        o.codeHighlight = { snippet: 'surviveCode', lines: o.lines || [] }; delete o.lines;
        o.logEvents = [{ t: t += 4, kind: o.kind || 'observe', subject: o.activeNodes[o.activeNodes.length - 1] || 'ui', detailKey: M(m, 'ev.' + key), params: o.params }]; delete o.kind;
        out.push(o);
      };
      HOLD.forEach(function (h) { vals[h] = '"Ana"'; });
      P('type', { type: 'scenario', activeNodes: ['ui', 'composition', 'bundle', 'vm', 'disk'], movingSignals: HOLD.map(function (h) { return { edge: EDGE[h], tok: 'state' }; }), lines: [2, 3, 4, 5, 6], kind: 'write' });
      P('event.' + ev, { type: ev === 'dismiss' || ev === 'processDeath' ? 'pitfall' : 'mechanism', activeNodes: ev === 'recompose' ? ['composition'] : ev === 'rotate' ? ['ui', 'composition'] : ['process'], kind: ev === 'recompose' ? 'recompose' : 'act' });
      HOLD.forEach(function (h) {
        var ok = KEEP[ev][h];
        if (ok) kept++; else { lost++; vals[h] = '""'; }
        var key = 'h.' + h + '.' + (ev === 'recompose' ? 'recompose' : ev);
        P(key, { type: ok ? 'mechanism' : 'pitfall', activeNodes: [NODE[h]], movingSignals: ok ? [{ edge: EDGE[h], tok: 'state' }] : [], lines: [LINE[h]], kind: ok ? 'resume' : 'skip',
          callouts: h === 'saveable' && ev === 'dismiss' ? [{ kind: 'source', textKey: M(m, 'co.dismiss') }] : h === 'vm' && ev === 'processDeath' ? [{ kind: 'pitfall', textKey: M(m, 'co.vmDeath') }] : [] });
      });
      P('end.' + ev, { type: lost >= 3 ? 'pitfall' : 'mechanism', activeNodes: ['ui'], kind: 'observe', callouts: [{ kind: 'mechanism', textKey: M(m, 'co.end.' + ev) }] });
      return out;
    }
    reg(m, {
      codeId: 'surviveCode',
      simpExtra: [M(m, 'simp.2')],
      controls: [
        { id: 'event', type: 'select', labelKey: M(m, 'ctl.event'), get: function (s) { return s.event; }, action: 'event', options: EV.map(function (v) { return { value: v, labelKey: M(m, 'ctl.event.' + v) }; }) }
      ],
      init: function () { return { event: 'rotate' }; },
      act: function (s, a, v) { return { event: EV.indexOf(v) >= 0 ? v : 'rotate' }; },
      steps: steps,
      selfChecks: [{ name: 'recompose giữ 5/5; xoay màn hình mất remember (4/5); process bị hệ thống dừng mất remember và ViewModel (3/5); người dùng đóng hẳn chỉ còn lưu trữ bền (1/5)', run: function () {
        var last = function (e) { var x = steps({ event: e }); return x[x.length - 1].metrics.kept; };
        return last('recompose') === 5 && last('rotate') === 4 && last('processDeath') === 3 && last('dismiss') === 1;
      } }]
    });
  })();

  /* ================= B5 (v2): vòng lặp của Recomposer theo frame (Recomposer.kt @296313a4) =================
     while { awaitWorkAvailable(); if (!recordComposerModifications()) continue; parentFrameClock.withFrameNanos { t ->
       if (có awaiter của broadcastFrameClock) { sendFrame(t); Snapshot.sendApplyNotifications() }  // animation trước
       recompose các composition bị invalidate (kể cả invalidation vừa sinh trong frame này); applyChanges() } }
     Android: AndroidUiFrameClock.withFrameNanos = Choreographer.postFrameCallback; WindowRecomposer: ON_STOP → pauseCompositionFrameClock,
     ON_START → resumeCompositionFrameClock. Số frame của animation là giả định của site. */
  (function () {
    var m = 'frame';
    var SC = ['write', 'anim', 'stopped'];
    function steps(s) {
      var sc = SC.indexOf(s.scenario) >= 0 ? s.scenario : 'write', out = [], t = 0;
      var st = { frames: 0, recomps: 0, animFrames: 0 }, wait = 'awaitWorkAvailable', offset = 0;
      var P = function (key, o) {
        o.id = key.replace(/\./g, '_') + out.length; o.type = o.type || 'mechanism';
        o.titleKey = M(m, 's.' + key + '.title'); o.explainKey = M(m, 's.' + key + '.explain');
        o.params = o.params || {}; o.params.f = st.frames; o.params.o = offset;
        o.metrics = { frames: st.frames, recomps: st.recomps, animFrames: st.animFrames };
        o.stateAfter = [{ labelKey: M(m, 'st.wait'), value: wait }, { labelKey: M(m, 'st.offset'), value: String(offset) }];
        o.movingSignals = o.movingSignals || []; o.activeNodes = o.activeNodes || [];
        o.codeHighlight = { snippet: o.snip || 'frameLoop', lines: o.lines || [] }; delete o.lines; delete o.snip;
        o.logEvents = [{ t: t += 4, kind: o.kind || 'observe', subject: o.activeNodes[o.activeNodes.length - 1] || 'recomposer', detailKey: M(m, 'ev.' + key), params: o.params }]; delete o.kind;
        out.push(o);
      };
      P('idle', { type: 'scenario', activeNodes: ['recomposer'], lines: [2], kind: 'observe' });
      if (sc === 'write') {
        wait = '—';
        P('write', { activeNodes: ['lifecycle', 'recomposer'], movingSignals: [{ edge: 'e5', tok: 'state' }], lines: [2, 3], kind: 'write' });
        wait = 'withFrameNanos';
        P('request', { activeNodes: ['recomposer', 'clock', 'choreographer'], movingSignals: [{ edge: 'e1', tok: 'signal' }, { edge: 'e0', tok: 'signal' }], lines: [4], kind: 'schedule' });
        st.frames++; wait = '—';
        P('vsync', { activeNodes: ['choreographer', 'clock', 'recomposer'], movingSignals: [{ edge: 'e0r', tok: 'signal' }], lines: [4], kind: 'frame' });
        st.recomps++;
        P('recompose', { activeNodes: ['recomposer', 'composition'], movingSignals: [{ edge: 'e3', tok: 'runtime' }], lines: [9], kind: 'recompose' });
        P('apply', { activeNodes: ['composition', 'applier'], movingSignals: [{ edge: 'e4', tok: 'ui' }], lines: [10], kind: 'apply' });
        wait = 'awaitWorkAvailable';
        P('end.write', { activeNodes: ['recomposer'], lines: [2], kind: 'observe', callouts: [{ kind: 'mechanism', textKey: M(m, 'co.end.write') }] });
        return out;
      }
      // animation chạy bằng withFrameNanos trong một effect (ví dụ LaunchedEffect hoặc animate*AsState)
      wait = 'withFrameNanos';
      P('animStart', { activeNodes: ['awaiters', 'recomposer', 'clock'], movingSignals: [{ edge: 'e2r', tok: 'anim' }, { edge: 'e1', tok: 'signal' }], lines: [2], snip: 'frameAnim', kind: 'schedule' });
      var frame = function (n) {
        st.frames++; st.animFrames++; offset += 8;
        P(n === 1 ? 'animFrame1' : 'animFrame', { params: { n: n }, activeNodes: ['choreographer', 'recomposer', 'awaiters'], movingSignals: [{ edge: 'e0r', tok: 'signal' }, { edge: 'e2', tok: 'anim' }], lines: [4, 5], snip: 'frameAnim', kind: 'frame',
          callouts: n === 1 ? [{ kind: 'mechanism', textKey: M(m, 'co.order') }] : [] });
        st.recomps++;
        P(n === 1 ? 'sameFrame1' : 'sameFrame', { params: { n: n }, activeNodes: ['recomposer', 'composition', 'applier'], movingSignals: [{ edge: 'e3', tok: 'runtime' }, { edge: 'e4', tok: 'ui' }], lines: [7, 9, 10], kind: 'recompose' });
      };
      frame(1); frame(2);
      if (sc === 'stopped') {
        wait = 'awaitWorkAvailable';
        P('stop', { type: 'experiment', activeNodes: ['lifecycle', 'recomposer'], movingSignals: [{ edge: 'e6', tok: 'cancel' }], lines: [5], kind: 'act', callouts: [{ kind: 'android', textKey: M(m, 'co.stop') }] });
        P('stopped', { activeNodes: ['awaiters'], lines: [4], snip: 'frameAnim', kind: 'skip', skipped: [{ whatKey: M(m, 'sk.frames'), whyKey: M(m, 'sk.paused') }] });
        wait = 'withFrameNanos';
        P('start', { activeNodes: ['lifecycle', 'recomposer', 'clock'], movingSignals: [{ edge: 'e6', tok: 'signal' }, { edge: 'e1', tok: 'signal' }], lines: [5], kind: 'resume' });
        frame(3);
      }
      wait = 'awaitWorkAvailable';
      P('animEnd', { activeNodes: ['awaiters', 'recomposer'], lines: [6], snip: 'frameAnim', kind: 'observe' });
      P('end.' + sc, { activeNodes: ['recomposer'], lines: [2], kind: 'observe', callouts: [{ kind: 'mechanism', textKey: M(m, 'co.end.' + sc) }] });
      return out;
    }
    reg(m, {
      codeId: 'frameLoop',
      simpExtra: [M(m, 'simp.2')],
      controls: [
        { id: 'scenario', type: 'select', labelKey: M(m, 'ctl.scenario'), get: function (s) { return s.scenario; }, action: 'scenario', options: SC.map(function (v) { return { value: v, labelKey: M(m, 'ctl.scenario.' + v) }; }) }
      ],
      init: function () { return { scenario: 'write' }; },
      act: function (s, a, v) { return { scenario: SC.indexOf(v) >= 0 ? v : 'write' }; },
      steps: steps,
      selfChecks: [{ name: 'một lần ghi: 1 frame, 1 recompose; animation: mỗi frame gửi cho animation TRƯỚC rồi recompose trong cùng frame (2 frame, 2 recompose); dừng nền: không frame nào trong lúc ON_STOP, chạy tiếp sau ON_START (3 frame)', run: function () {
        var last = function (sc) { var x = steps({ scenario: sc }); return x[x.length - 1].metrics; };
        var w = last('write'), a = last('anim'), p = last('stopped');
        var order = steps({ scenario: 'anim' }).map(function (x) { return x.titleKey.split('.s.')[1].replace('.title', ''); });
        return w.frames === 1 && w.recomps === 1 && w.animFrames === 0 && a.frames === 2 && a.recomps === 2 && a.animFrames === 2 && p.frames === 3 &&
          order.indexOf('animFrame1') >= 0 && order.indexOf('animFrame1') < order.indexOf('sameFrame1');
      } }]
    });
  })();

  /* ================= EF (v2): vòng đời của effect (Effects.kt, RememberObserver.kt @296313a4; Kunneth Ch.7; side-effects docs) =================
     LaunchedEffect(key) = remember(key) { LaunchedEffectImpl }: onRemembered (sau khi composition được apply) → launch;
     key đổi → object cũ bị forgotten (cancel), object mới remembered (launch); rời composition → onForgotten → cancel.
     DisposableEffect: key đổi → onDispose cũ rồi chạy effect mới; rời composition → onDispose. SideEffect chạy sau mỗi lần recompose thành công.
     Kịch bản counter là biến thể của LaunchedEffectDemo (Kunneth Ch.7): DisposableEffect đặt cùng nhánh if với LaunchedEffect. */
  (function () {
    var m = 'effects';
    var SC = ['counter', 'timeoutStale', 'timeoutUpdated'];
    function steps(s) {
      var sc = SC.indexOf(s.scenario) >= 0 ? s.scenario : 'counter', out = [], t = 0;
      var st = { launched: 0, cancelled: 0, disposed: 0, side: 0 }, job = '—', counter = 0, log = [], clicks = 0, called = '—';
      var P = function (key, o) {
        o.id = key.replace(/\./g, '_') + out.length; o.type = o.type || 'mechanism';
        o.titleKey = M(m, 's.' + key + '.title'); o.explainKey = M(m, 's.' + key + '.explain');
        o.params = o.params || {}; o.params.c = counter; o.params.k = clicks;
        o.metrics = { launched: st.launched, cancelled: st.cancelled, disposed: st.disposed, side: st.side };
        o.stateAfter = sc === 'counter'
          ? [{ labelKey: M(m, 'st.clicks'), value: String(clicks) }, { labelKey: M(m, 'st.job'), value: job }, { labelKey: M(m, 'st.counter'), value: String(counter) }, { labelKey: M(m, 'st.log'), value: log.length ? log.slice(-3).join(' · ') : '—' }]
          : [{ labelKey: M(m, 'st.job'), value: job }, { labelKey: M(m, 'st.lambda'), value: o.lambda || 'goHomeA' }, { labelKey: M(m, 'st.called'), value: called }];
        delete o.lambda;
        o.movingSignals = o.movingSignals || []; o.activeNodes = o.activeNodes || [];
        o.codeHighlight = { snippet: sc === 'counter' ? 'effCounter' : sc === 'timeoutStale' ? 'effStale' : 'effUpdated', lines: o.lines || [] }; delete o.lines;
        o.logEvents = [{ t: t += 4, kind: o.kind || 'observe', subject: o.activeNodes[o.activeNodes.length - 1] || 'composition', detailKey: M(m, 'ev.' + key), params: o.params }]; delete o.kind;
        out.push(o);
      };
      if (sc === 'counter') {
        st.side++;
        P('cInit', { type: 'scenario', activeNodes: ['composition', 'side'], movingSignals: [{ edge: 'e4', tok: 'signal' }], lines: [2, 3, 18], kind: 'recompose' });
        clicks = 1; st.side++; st.launched++; job = '#1'; log.push('init 1');
        P('cStart', { activeNodes: ['tap', 'composition', 'remembered', 'job'], movingSignals: [{ edge: 'e1', tok: 'state' }, { edge: 'e2', tok: 'runtime' }, { edge: 'e3', tok: 'job' }], lines: [4, 6, 7, 8, 11], kind: 'act',
          callouts: [{ kind: 'mechanism', textKey: M(m, 'co.remembered') }] });
        counter = 1; st.side++;
        P('cTick', { activeNodes: ['job', 'composition', 'side'], movingSignals: [{ edge: 'e5', tok: 'state' }, { edge: 'e4', tok: 'signal' }], lines: [13, 14], kind: 'write' });
        counter = 2; st.side++;
        P('cTick2', { activeNodes: ['job', 'composition', 'side'], movingSignals: [{ edge: 'e5', tok: 'state' }], lines: [13, 14], kind: 'write' });
        clicks = 2; st.side++; st.cancelled++; st.disposed++; st.launched++; job = '#2'; counter = 0; log.push('dispose 1'); log.push('init 2');
        P('cRestart', { activeNodes: ['tap', 'remembered', 'job'], movingSignals: [{ edge: 'e3', tok: 'cancel' }, { edge: 'e3', tok: 'job' }], lines: [4, 7, 8, 9, 11], kind: 'act',
          callouts: [{ kind: 'mechanism', textKey: M(m, 'co.restart') }] });
        counter = 1; st.side++;
        P('cTick3', { activeNodes: ['job', 'composition'], movingSignals: [{ edge: 'e5', tok: 'state' }], lines: [13, 14], kind: 'write' });
        clicks = 0; st.side++; st.cancelled++; st.disposed++; job = '—'; log.push('dispose 2');
        P('cStop', { type: 'pitfall', activeNodes: ['tap', 'remembered', 'job'], movingSignals: [{ edge: 'e3', tok: 'cancel' }], lines: [5, 6, 9], kind: 'skip',
          callouts: [{ kind: 'mechanism', textKey: M(m, 'co.leave') }] });
        P('end.counter', { activeNodes: ['composition'], lines: [], kind: 'observe', callouts: [{ kind: 'mechanism', textKey: M(m, 'co.end.counter') }] });
        return out;
      }
      var upd = sc === 'timeoutUpdated';
      st.launched++; job = 'delay(3000)';
      P('tInit', { type: 'scenario', activeNodes: ['composition', 'remembered', 'job'], movingSignals: [{ edge: 'e2', tok: 'runtime' }, { edge: 'e3', tok: 'job' }], lines: upd ? [2, 3, 4] : [2, 3], kind: 'schedule' });
      P('tChange', { activeNodes: ['tap', 'composition'], movingSignals: [{ edge: 'e1', tok: 'state' }], lines: upd ? [2] : [2], kind: 'recompose', lambda: 'goHomeB',
        callouts: [{ kind: 'mechanism', textKey: M(m, 'co.noRestart') }] });
      called = upd ? 'goHomeB' : 'goHomeA'; job = '—';
      P(upd ? 'tFireOk' : 'tFireStale', { type: upd ? 'mechanism' : 'pitfall', activeNodes: ['job', 'tap'], movingSignals: [{ edge: 'e5', tok: upd ? 'state' : 'error' }], lines: upd ? [5, 6] : [4, 5], kind: 'act', lambda: 'goHomeB' });
      P('end.' + sc, { type: upd ? 'mechanism' : 'pitfall', activeNodes: ['composition'], lines: [], kind: 'observe', lambda: 'goHomeB', callouts: [{ kind: upd ? 'mechanism' : 'pitfall', textKey: M(m, 'co.end.' + sc) }] });
      return out;
    }
    reg(m, {
      codeId: 'effCounter',
      simpExtra: [M(m, 'simp.2')],
      controls: [
        { id: 'scenario', type: 'select', labelKey: M(m, 'ctl.scenario'), get: function (s) { return s.scenario; }, action: 'scenario', options: SC.map(function (v) { return { value: v, labelKey: M(m, 'ctl.scenario.' + v) }; }) }
      ],
      init: function () { return { scenario: 'counter' }; },
      act: function (s, a, v) { return { scenario: SC.indexOf(v) >= 0 ? v : 'counter' }; },
      steps: steps,
      selfChecks: [{ name: 'counter: 2 coroutine được launch, cả 2 bị cancel (đổi key, rời composition), onDispose 2 lần, SideEffect chạy sau mỗi lượt (7); timeout: không có rememberUpdatedState thì gọi lambda cũ goHomeA, có thì gọi goHomeB, effect không restart', run: function () {
        var last = function (sc) { var x = steps({ scenario: sc }); return x[x.length - 1]; };
        var c = last('counter').metrics, a = last('timeoutStale'), b = last('timeoutUpdated');
        return c.launched === 2 && c.cancelled === 2 && c.disposed === 2 && c.side === 7 && a.metrics.launched === 1 && a.metrics.cancelled === 0 &&
          a.stateAfter[2].value === 'goHomeA' && b.stateAfter[2].value === 'goHomeB';
      } }]
    });
  })();

  /* ================= CL (v2): CompositionLocal, đổi giá trị được cung cấp (CompositionLocal.kt @296313a4; compositionlocal docs) =================
     Cây theo ví dụ Essentials Ch.21: C1 → C2 → C4 → C6; C1 → Provider(LocalColor) → C3 → C5 → (C7, C8). C3 và C8 đọc LocalColor.current; C6 đọc nhưng ở nhánh khác.
     compositionLocalOf: đổi giá trị → chỉ nơi đọc .current bị invalidate. staticCompositionLocalOf: không theo dõi lần đọc → toàn bộ content của provider recompose. */
  (function () {
    var m = 'locals';
    var CONTENT = ['c3', 'c5', 'c7', 'c8'], READERS = ['c3', 'c8'];
    function steps(s) {
      var stat = s.kind === 'static', out = [], t = 0, rec = 0, col = 'Peach';
      var P = function (key, o) {
        o.id = key.replace(/\./g, '_') + out.length; o.type = o.type || 'mechanism';
        o.titleKey = M(m, 's.' + key + '.title'); o.explainKey = M(m, 's.' + key + '.explain');
        o.params = o.params || {}; o.metrics = { recomposed: rec, readers: READERS.length, provided: col };
        o.stateAfter = [{ labelKey: M(m, 'st.provided'), value: col }, { labelKey: M(m, 'st.c8'), value: col }, { labelKey: M(m, 'st.c6'), value: 'Peach' }];
        o.movingSignals = o.movingSignals || []; o.activeNodes = o.activeNodes || [];
        o.codeHighlight = { snippet: stat ? 'localsStatic' : 'localsDyn', lines: o.lines || [] }; delete o.lines;
        o.logEvents = [{ t: t += 4, kind: o.kind || 'observe', subject: o.activeNodes[o.activeNodes.length - 1] || 'c1', detailKey: M(m, 'ev.' + key), params: o.params }]; delete o.kind;
        out.push(o);
      };
      P('first', { type: 'scenario', activeNodes: ['c1', 'prov', 'c3', 'c8', 'c6'], movingSignals: [{ edge: 'e1', tok: 'state' }, { edge: 'e2', tok: 'state' }], lines: [1, 6, 7, 10, 11], kind: 'recompose' });
      col = 'Brown';
      P('toggle', { activeNodes: ['c1', 'prov'], movingSignals: [{ edge: 'e1', tok: 'state' }], lines: [3, 4, 6], kind: 'write' });
      if (stat) {
        rec = CONTENT.length;
        P('staticAll', { type: 'pitfall', activeNodes: ['prov'].concat(CONTENT), movingSignals: [{ edge: 'e2', tok: 'runtime' }, { edge: 'e3', tok: 'runtime' }, { edge: 'e4', tok: 'runtime' }, { edge: 'e5', tok: 'runtime' }], lines: [1, 6, 7], kind: 'recompose',
          callouts: [{ kind: 'mechanism', textKey: M(m, 'co.static') }] });
      } else {
        rec = READERS.length;
        P('dynReaders', { activeNodes: ['prov', 'c3', 'c8'], movingSignals: [{ edge: 'e2', tok: 'state' }, { edge: 'e5', tok: 'state' }], lines: [1, 10], kind: 'recompose',
          callouts: [{ kind: 'mechanism', textKey: M(m, 'co.dynamic') }] });
      }
      P('other', { activeNodes: ['c2', 'c4', 'c6'], lines: [5, 11], kind: 'skip', skipped: [{ whatKey: M(m, 'sk.branch'), whyKey: M(m, 'sk.notInside') }] });
      P('end.' + (stat ? 'static' : 'dynamic'), { activeNodes: stat ? CONTENT : READERS, lines: [], kind: 'observe', callouts: [{ kind: 'mechanism', textKey: M(m, 'co.end.' + (stat ? 'static' : 'dynamic')) }] });
      return out;
    }
    reg(m, {
      codeId: 'localsDyn',
      simpExtra: [M(m, 'simp.2')],
      controls: [
        { id: 'kind', type: 'select', labelKey: M(m, 'ctl.kind'), get: function (s) { return s.kind; }, action: 'kind', options: ['dynamic', 'static'].map(function (v) { return { value: v, labelKey: M(m, 'ctl.kind.' + v) }; }) }
      ],
      init: function () { return { kind: 'dynamic' }; },
      act: function (s, a, v) { return { kind: v === 'static' ? 'static' : 'dynamic' }; },
      steps: steps,
      selfChecks: [{ name: 'compositionLocalOf: đổi giá trị chỉ recompose 2 nơi đọc (C3, C8); staticCompositionLocalOf: recompose cả 4 composable trong content; C6 ở nhánh khác luôn thấy giá trị mặc định', run: function () {
        var last = function (k) { var x = steps({ kind: k }); return x[x.length - 1]; };
        var d = last('dynamic'), st = last('static');
        return d.metrics.recomposed === 2 && st.metrics.recomposed === 4 && d.stateAfter[2].value === 'Peach' && d.stateAfter[1].value === 'Brown';
      } }]
    });
  })();

  /* ================= B6 (v2): chèn cây top-down hay bottom-up (KDoc Applier.insertTopDown @296313a4) =================
     Chèn B (có con A, C) vào R. "ancestors": mỗi khi một con được thêm, mọi tổ tiên tới gốc được báo; "subtree": khi một node vào cây,
     nó và mọi node trong cây con của nó được báo. Số đếm theo đúng ví dụ trong KDoc: ancestors TD 5 / BU 3; subtree TD 3 / BU 5.
     UiApplier (Android) bỏ qua insertTopDown và chèn trong insertBottomUp. */
  (function () {
    var m = 'insert';
    function steps(s) {
      var td = s.order !== 'bottomUp', anc = s.notify !== 'subtree', out = [], t = 0, n = 0, ins = 0, log = [], tree = 'R';
      var P = function (key, o) {
        o.id = key.replace(/\./g, '_') + out.length; o.type = o.type || 'mechanism';
        o.titleKey = M(m, 's.' + key + '.title'); o.explainKey = M(m, 's.' + key + '.explain');
        o.params = o.params || {}; o.params.n = n;
        o.metrics = { notifications: n, inserts: ins };
        o.stateAfter = [{ labelKey: M(m, 'st.tree'), value: tree }, { labelKey: M(m, 'st.call'), value: o.call || '—' }, { labelKey: M(m, 'st.notified'), value: log.length ? log.join(' · ') : '—' }];
        delete o.call;
        o.movingSignals = o.movingSignals || []; o.activeNodes = o.activeNodes || [];
        o.codeHighlight = { snippet: 'insertOrder', lines: o.lines || [] }; delete o.lines;
        o.logEvents = [{ t: t += 4, kind: o.kind || 'apply', subject: o.activeNodes[0] || 'r', detailKey: M(m, 'ev.' + key), params: o.params }]; delete o.kind;
        out.push(o);
      };
      var note = function (arr) { arr.forEach(function (x) { log.push(x); n++; }); };
      P('start', { type: 'scenario', activeNodes: ['r', 'b', 'a', 'c'], lines: [], kind: 'observe' });
      if (td) {
        ins++; tree = 'R → B'; note(anc ? ['R⇐B'] : ['B']);
        P('td1', { activeNodes: ['r', 'b'], movingSignals: [{ edge: 'e1', tok: 'ui' }], lines: [3], call: 'insertTopDown(0, B)' });
        ins++; tree = 'R → B → A'; note(anc ? ['B⇐A', 'R⇐A'] : ['A']);
        P('td2', { activeNodes: ['b', 'a'].concat(anc ? ['r'] : []), movingSignals: [{ edge: 'e2', tok: 'ui' }], lines: [3], call: 'down(B); insertTopDown(0, A)' });
        ins++; tree = 'R → B → (A, C)'; note(anc ? ['B⇐C', 'R⇐C'] : ['C']);
        P('td3', { activeNodes: ['b', 'c'].concat(anc ? ['r'] : []), movingSignals: [{ edge: 'e3', tok: 'ui' }], lines: [3], call: 'insertTopDown(1, C); up()' });
      } else {
        ins++; tree = 'R · B → A'; note(anc ? ['B⇐A'] : ['A']);
        P('bu1', { activeNodes: ['b', 'a'], movingSignals: [{ edge: 'e2', tok: 'ui' }], lines: [4], call: 'insertBottomUp(0, A)' });
        ins++; tree = 'R · B → (A, C)'; note(anc ? ['B⇐C'] : ['C']);
        P('bu2', { activeNodes: ['b', 'c'], movingSignals: [{ edge: 'e3', tok: 'ui' }], lines: [4], call: 'insertBottomUp(1, C)' });
        ins++; tree = 'R → B → (A, C)'; note(anc ? ['R⇐B'] : ['B', 'A', 'C']);
        P('bu3', { activeNodes: ['r', 'b'].concat(anc ? [] : ['a', 'c']), movingSignals: [{ edge: 'e1', tok: 'ui' }], lines: [4], call: 'up(); insertBottomUp(0, B)' });
      }
      var good = anc ? !td : td;
      P('end.' + (anc ? 'anc' : 'sub') + (td ? 'TD' : 'BU'), { type: good ? 'mechanism' : 'pitfall', activeNodes: ['r'], lines: td ? [3] : [4, 7], kind: 'observe',
        callouts: [{ kind: good ? 'mechanism' : 'pitfall', textKey: M(m, 'co.end.' + (anc ? 'anc' : 'sub')) }] });
      return out;
    }
    reg(m, {
      codeId: 'insertOrder',
      simpExtra: [M(m, 'simp.2')],
      controls: [
        { id: 'order', type: 'select', labelKey: M(m, 'ctl.order'), get: function (s) { return s.order; }, action: 'order', options: ['topDown', 'bottomUp'].map(function (v) { return { value: v, labelKey: M(m, 'ctl.order.' + v) }; }) },
        { id: 'notify', type: 'select', labelKey: M(m, 'ctl.notify'), get: function (s) { return s.notify; }, action: 'notify', options: ['ancestors', 'subtree'].map(function (v) { return { value: v, labelKey: M(m, 'ctl.notify.' + v) }; }) }
      ],
      init: function () { return { order: 'topDown', notify: 'ancestors' }; },
      act: function (s, a, v) { var o = { order: s.order, notify: s.notify }; if (a === 'order') o.order = v === 'bottomUp' ? 'bottomUp' : 'topDown'; else o.notify = v === 'subtree' ? 'subtree' : 'ancestors'; return o; },
      steps: steps,
      selfChecks: [{ name: 'đúng số thông báo trong KDoc của Applier: báo tổ tiên → top-down 5, bottom-up 3; báo cây con → top-down 3, bottom-up 5; luôn 3 lần chèn', run: function () {
        var last = function (o, nf) { var x = steps({ order: o, notify: nf }); return x[x.length - 1].metrics; };
        return last('topDown', 'ancestors').notifications === 5 && last('bottomUp', 'ancestors').notifications === 3 &&
          last('topDown', 'subtree').notifications === 3 && last('bottomUp', 'subtree').notifications === 5 && last('bottomUp', 'subtree').inserts === 3;
      } }]
    });
  })();

  /* ================= B7 (v2): đọc state ở phase nào thì phase đó chạy lại (Compose phases docs, đọc 2026-11-23) =================
     comp: đọc trong composition → mỗi frame cuộn: composition + layout + draw. layout: đọc trong lambda của Modifier.offset { } (placement)
     → layout + draw. draw: đọc trong drawBehind → chỉ draw. loop: onSizeChanged ghi state đọc trong composition → cần frame thứ hai,
     frame đầu vẽ chồng chữ lên ảnh. */
  (function () {
    var m = 'scroll';
    var SC = ['comp', 'layout', 'draw', 'loop'];
    function steps(s) {
      var sc = SC.indexOf(s.where) >= 0 ? s.where : 'comp', out = [], t = 0, c = { comp: 0, layout: 0, draw: 0, frames: 0 }, val = '0';
      var P = function (key, o) {
        o.id = key.replace(/\./g, '_') + out.length; o.type = o.type || 'mechanism';
        o.titleKey = M(m, 's.' + key + '.title'); o.explainKey = M(m, 's.' + key + '.explain');
        o.params = o.params || {}; o.params.f = c.frames;
        o.metrics = { comp: c.comp, layout: c.layout, draw: c.draw, frames: c.frames };
        o.stateAfter = [{ labelKey: M(m, 'st.value'), value: val }, { labelKey: M(m, 'st.ran'), value: o.ran || '—' }];
        delete o.ran;
        o.movingSignals = o.movingSignals || []; o.activeNodes = o.activeNodes || [];
        o.codeHighlight = { snippet: 'scroll_' + sc, lines: o.lines || [] }; delete o.lines;
        o.logEvents = [{ t: t += 4, kind: o.kind || 'frame', subject: o.activeNodes[0] || 'state', detailKey: M(m, 'ev.' + key), params: o.params }]; delete o.kind;
        out.push(o);
      };
      var LINE = { comp: [4, 5], layout: [4, 5], draw: [4, 5] };
      if (sc !== 'loop') {
        P('intro.' + sc, { type: 'scenario', activeNodes: ['state', sc === 'comp' ? 'comp' : sc === 'layout' ? 'layout' : 'draw'], lines: LINE[sc], kind: 'observe' });
        [1, 2, 3].forEach(function (i) {
          c.frames++; val = String(i * 40); var ran = [];
          if (sc === 'comp') { c.comp++; ran.push('composition'); }
          if (sc !== 'draw') { c.layout++; ran.push('layout'); }
          c.draw++; ran.push('draw');
          var act = ['state'].concat(sc === 'comp' ? ['comp', 'layout', 'draw'] : sc === 'layout' ? ['layout', 'draw'] : ['draw']);
          var sig = sc === 'comp' ? [{ edge: 'e1', tok: 'state' }, { edge: 'e4', tok: 'runtime' }, { edge: 'e5', tok: 'ui' }] : sc === 'layout' ? [{ edge: 'e2', tok: 'state' }, { edge: 'e5', tok: 'ui' }] : [{ edge: 'e3', tok: 'state' }];
          P(i === 1 ? 'frame1.' + sc : 'frame.' + sc, { activeNodes: act, movingSignals: sig, lines: LINE[sc], ran: ran.join(' → '), kind: sc === 'comp' ? 'recompose' : sc === 'layout' ? 'layout' : 'draw' });
        });
        P('end.' + sc, { type: sc === 'comp' ? 'pitfall' : 'mechanism', activeNodes: ['state'], lines: [], kind: 'observe', callouts: [{ kind: sc === 'comp' ? 'pitfall' : 'mechanism', textKey: M(m, 'co.end.' + sc) }] });
        return out;
      }
      // vòng lặp qua hai frame: onSizeChanged ghi imageHeightPx, Text đọc nó trong composition
      P('intro.loop', { type: 'scenario', activeNodes: ['state', 'comp'], lines: [2, 7, 8], kind: 'observe' });
      c.frames++; c.comp++; val = '0';
      P('l1comp', { activeNodes: ['comp'], movingSignals: [{ edge: 'e4', tok: 'runtime' }], lines: [12, 13], ran: 'composition', kind: 'recompose' });
      c.layout++; val = '200';
      P('l1layout', { type: 'pitfall', activeNodes: ['layout', 'state'], movingSignals: [{ edge: 'e6', tok: 'error' }], lines: [7, 8], ran: 'layout', kind: 'write' });
      c.draw++;
      P('l1draw', { type: 'pitfall', activeNodes: ['draw'], movingSignals: [{ edge: 'e5', tok: 'ui' }], lines: [], ran: 'draw', kind: 'draw', callouts: [{ kind: 'pitfall', textKey: M(m, 'co.overlap') }] });
      c.frames++; c.comp++; c.layout++; c.draw++;
      P('l2', { activeNodes: ['state', 'comp', 'layout', 'draw'], movingSignals: [{ edge: 'e1', tok: 'state' }, { edge: 'e4', tok: 'runtime' }, { edge: 'e5', tok: 'ui' }], lines: [12, 13], ran: 'composition → layout → draw', kind: 'recompose' });
      P('end.loop', { type: 'pitfall', activeNodes: ['state'], lines: [], kind: 'observe', callouts: [{ kind: 'pitfall', textKey: M(m, 'co.end.loop') }] });
      return out;
    }
    reg(m, {
      codeId: 'scroll_comp',
      simpExtra: [M(m, 'simp.2')],
      controls: [
        { id: 'where', type: 'select', labelKey: M(m, 'ctl.where'), get: function (s) { return s.where; }, action: 'where', options: SC.map(function (v) { return { value: v, labelKey: M(m, 'ctl.where.' + v) }; }) }
      ],
      init: function () { return { where: 'comp' }; },
      act: function (s, a, v) { return { where: SC.indexOf(v) >= 0 ? v : 'comp' }; },
      steps: steps,
      selfChecks: [{ name: '3 frame cuộn: đọc ở composition → 3/3/3 (composition/layout/draw); ở placement → 0/3/3; ở draw → 0/0/3; vòng lặp onSizeChanged cần 2 frame và 2 lượt composition', run: function () {
        var last = function (w) { var x = steps({ where: w }); return x[x.length - 1].metrics; };
        var a = last('comp'), b = last('layout'), d = last('draw'), l = last('loop');
        return a.comp === 3 && a.layout === 3 && a.draw === 3 && b.comp === 0 && b.layout === 3 && b.draw === 3 && d.comp === 0 && d.layout === 0 && d.draw === 3 && l.frames === 2 && l.comp === 2;
      } }]
    });
  })();
  /* ================= LO (v2): một lượt layout của Layout tùy chỉnh (Custom layouts, Intrinsic measurements docs, 2026-11-23; MeasurePolicy.kt, Measurable.kt, LayoutNodeLayoutDelegate.kt @296313a4) =================
     col: MyBasicColumn đo mỗi con một lần rồi đặt theo y. twice: đo cùng một Measurable hai lần → IllegalStateException (MeasuredTwiceErrorMessage).
     nointr: Row(Text, VerticalDivider.fillMaxHeight, Text) → divider cao bằng maxHeight. intr: Row.height(IntrinsicSize.Min) hỏi minIntrinsicHeight
     trước (48, 0, 72) rồi đo mỗi con một lần với chiều cao cố định 72. Số px là minh họa (cha cho 0..360 × 0..640). */
  (function () {
    var m = 'measure';
    var CASES = ['col', 'twice', 'nointr', 'intr'];
    function steps(s) {
      var cs = CASES.indexOf(s.which) >= 0 ? s.which : 'col', out = [], t = 0, c = { measured: 0, queries: 0, height: '—' }, cons = '0..360 × 0..640', last = '—', pos = '—';
      var snip = cs === 'col' ? 'measure_column' : cs === 'twice' ? 'measure_twice' : cs === 'nointr' ? 'measure_nointr' : 'measure_intr';
      var P = function (key, o) {
        o.id = key.replace(/\./g, '_') + out.length; o.type = o.type || 'mechanism';
        o.titleKey = M(m, 's.' + key + '.title'); o.explainKey = M(m, 's.' + key + '.explain');
        o.params = o.params || {};
        o.metrics = { measured: c.measured, queries: c.queries, height: c.height };
        o.stateAfter = [{ labelKey: M(m, 'st.cons'), value: cons }, { labelKey: M(m, 'st.last'), value: last }, { labelKey: M(m, 'st.pos'), value: pos }];
        o.movingSignals = o.movingSignals || []; o.activeNodes = o.activeNodes || [];
        o.codeHighlight = { snippet: snip, lines: o.lines || [] }; delete o.lines;
        o.logEvents = [{ t: t += 4, kind: o.kind || 'layout', subject: o.activeNodes[o.activeNodes.length - 1] || 'parent', detailKey: M(m, 'ev.' + key), params: o.params }]; delete o.kind;
        out.push(o);
      };
      var meas = function (key, node, size, lines, extra) {
        c.measured++; last = size;
        var o = { activeNodes: ['parent', node], movingSignals: [{ edge: 'e' + node.slice(1), tok: 'ui' }], lines: lines };
        for (var k in (extra || {})) o[k] = extra[k];
        P(key, o);
      };
      if (cs === 'col') {
        P('col.intro', { type: 'scenario', activeNodes: ['parent'], lines: [3], kind: 'observe' });
        meas('col.m1', 'k1', '360×40', [4]); meas('col.m2', 'k2', '360×40', [4]); meas('col.m3', 'k3', '360×60', [4]);
        c.height = 640;
        P('col.size', { activeNodes: ['parent'], lines: [5], kind: 'act' });
        pos = 'y = 0, 40, 80';
        P('col.place', { activeNodes: ['parent', 'k1', 'k2', 'k3'], movingSignals: [{ edge: 'e1', tok: 'state' }, { edge: 'e2', tok: 'state' }, { edge: 'e3', tok: 'state' }], lines: [7, 8, 9] });
        P('col.end', { activeNodes: ['parent'], lines: [], kind: 'observe', callouts: [{ kind: 'mechanism', textKey: M(m, 'co.single') }] });
        return out;
      }
      if (cs === 'twice') {
        P('tw.intro', { type: 'scenario', activeNodes: ['parent'], lines: [1], kind: 'observe' });
        meas('tw.m1', 'k1', '360×40', [2]);
        c.measured++;
        P('tw.again', { type: 'pitfall', activeNodes: ['parent', 'k1'], movingSignals: [{ edge: 'e1', tok: 'error' }], lines: [4, 6], kind: 'layout', callouts: [{ kind: 'pitfall', textKey: M(m, 'co.twice') }] });
        P('tw.end', { type: 'pitfall', activeNodes: ['parent'], lines: [6], kind: 'observe' });
        return out;
      }
      var tx = cs === 'intr';
      P((tx ? 'in' : 'no') + '.intro', { type: 'scenario', activeNodes: ['parent'], lines: [3], kind: 'observe' });
      if (tx) {
        [['q1', 'k1', '48', [4]], ['q2', 'k2', '0', [5]], ['q3', 'k3', '72', [6]]].forEach(function (q) {
          c.queries++; last = 'minIntrinsicHeight = ' + q[2];
          P('in.' + q[0], { activeNodes: ['parent', q[1]], movingSignals: [{ edge: 'e' + q[1].slice(1), tok: 'state' }], lines: q[3], kind: 'act' });
        });
        cons = '0..360 × 72';
        P('in.fixed', { activeNodes: ['parent'], lines: [3], kind: 'act' });
      }
      var h = tx ? 72 : 640;
      meas((tx ? 'in' : 'no') + '.m1', 'k1', '179×48', [4]);
      meas((tx ? 'in' : 'no') + '.m2', 'k2', '1×' + h, [5], tx ? { callouts: [{ kind: 'mechanism', textKey: M(m, 'co.noTwice') }] } : { type: 'pitfall' });
      meas((tx ? 'in' : 'no') + '.m3', 'k3', '179×72', [6]);
      c.height = h;
      P((tx ? 'in' : 'no') + '.size', { activeNodes: ['parent'], lines: [3], kind: 'act' });
      pos = 'x = 0, 179, 180';
      P((tx ? 'in' : 'no') + '.place', { activeNodes: ['parent', 'k1', 'k2', 'k3'], movingSignals: [{ edge: 'e1', tok: 'state' }, { edge: 'e2', tok: 'state' }, { edge: 'e3', tok: 'state' }], lines: [] });
      P((tx ? 'in' : 'no') + '.end', { type: tx ? 'mechanism' : 'pitfall', activeNodes: ['parent', 'k2'], lines: tx ? [3] : [5], kind: 'observe', callouts: [{ kind: tx ? 'mechanism' : 'pitfall', textKey: M(m, 'co.' + (tx ? 'intr' : 'nointr')) }] });
      return out;
    }
    reg(m, {
      codeId: 'measure_column',
      simpExtra: [M(m, 'simp.2')],
      controls: [
        { id: 'which', type: 'select', labelKey: M(m, 'ctl.which'), get: function (s) { return s.which; }, action: 'which', options: CASES.map(function (v) { return { value: v, labelKey: M(m, 'ctl.which.' + v) }; }) }
      ],
      init: function () { return { which: 'col' }; },
      act: function (s, a, v) { return { which: CASES.indexOf(v) >= 0 ? v : 'col' }; },
      steps: steps,
      selfChecks: [{ name: 'mỗi con đo đúng một lần: cột 3 lần đo, cao 640; đo lại cùng Measurable → bước pitfall; Row không intrinsic → divider 1×640; Row IntrinsicSize.Min → 3 lần hỏi, 3 lần đo, cao 72 = max(48, 0, 72)', run: function () {
        var last = function (w) { var x = steps({ which: w }); return x[x.length - 1]; };
        var a = last('col'), b = steps({ which: 'twice' }), n = last('nointr'), i = last('intr');
        var div = function (w) { return steps({ which: w }).filter(function (x) { return /_m2|m2/.test(x.id); })[0].stateAfter[1].value; };
        return a.metrics.measured === 3 && a.metrics.height === 640 && b[2].type === 'pitfall' && b[2].metrics.measured === 2 &&
          n.metrics.height === 640 && n.metrics.queries === 0 && div('nointr') === '1×640' &&
          i.metrics.queries === 3 && i.metrics.measured === 3 && i.metrics.height === 72 && div('intr') === '1×72';
      } }]
    });
  })();
  /* ================= MD (v2): chuỗi modifier sau recompose được khớp với chuỗi node cũ (NodeChain.updateFrom, actionForModifiers @296313a4) =================
     equal: element mới bằng (equals) element cũ → dùng lại node, không update. update: cùng lớp, khác dữ liệu (background Red → Blue) → update(node) + tự invalidate.
     insert: độ dài khác (then(if … else Modifier)) → diff cấu trúc: giữ 3 node, chèn 1 (onAttach). replace: cùng vị trí khác lớp (shadow → border) → bỏ diff tuyến tính,
     diff phần còn lại: gỡ 1 (onDetach), chèn 1, giữ 2. */
  (function () {
    var m = 'chain';
    var SC = ['equal', 'update', 'insert', 'replace'];
    var CH = {
      equal: ['padding · clip · background(Red) · size', 'padding · clip · background(Red) · size'],
      update: ['padding · clip · background(Red) · size', 'padding · clip · background(Blue) · size'],
      insert: ['padding · background · size', 'padding · border · background · size'],
      replace: ['padding · shadow · background · size', 'padding · border · background · size']
    };
    function steps(s) {
      var sc = SC.indexOf(s.which) >= 0 ? s.which : 'equal', out = [], t = 0, c = { reused: 0, updated: 0, inserted: 0, removed: 0 }, act = '—';
      var snip = sc === 'insert' ? 'chain_insert' : sc === 'replace' ? 'chain_replace' : 'chain_reuse';
      var P = function (key, o) {
        o.id = key.replace(/\./g, '_') + out.length; o.type = o.type || 'mechanism';
        o.titleKey = M(m, 's.' + key + '.title'); o.explainKey = M(m, 's.' + key + '.explain');
        o.params = o.params || {};
        o.metrics = { reused: c.reused, updated: c.updated, inserted: c.inserted, removed: c.removed };
        o.stateAfter = [{ labelKey: M(m, 'st.before'), value: CH[sc][0] }, { labelKey: M(m, 'st.after'), value: CH[sc][1] }, { labelKey: M(m, 'st.action'), value: act }];
        o.movingSignals = o.movingSignals || []; o.activeNodes = o.activeNodes || [];
        o.codeHighlight = { snippet: snip, lines: o.lines || [] }; delete o.lines;
        o.logEvents = [{ t: t += 4, kind: o.kind || 'apply', subject: o.activeNodes[o.activeNodes.length - 1] || 'layout', detailKey: M(m, 'ev.' + key), params: o.params }]; delete o.kind;
        out.push(o);
      };
      var EL = { equal: ['PaddingElement', 'clip', 'BackgroundElement', 'SizeElement'], update: ['PaddingElement', 'clip', 'BackgroundElement', 'SizeElement'],
        insert: ['PaddingElement', 'BorderModifierNodeElement', 'BackgroundElement', 'SizeElement'], replace: ['PaddingElement', 'BorderModifierNodeElement', 'BackgroundElement', 'SizeElement'] }[sc];
      var LN = sc === 'insert' || sc === 'replace' ? [5, 6, 7, 8] : [5, 6, 7, 8];
      var edge = function (i) { return i < 4 ? [{ edge: 'e' + i, tok: 'runtime' }] : [{ edge: 'e4', tok: 'runtime' }]; };
      var reuse = function (i, inDiff) { c.reused++; act = 'Reuse'; P(inDiff ? 'same' : 'reuse', { activeNodes: ['m' + i], movingSignals: edge(i), lines: [LN[i - 1]], params: { i: i, el: EL[i - 1] }, kind: 'skip' }); };
      P('intro.' + sc, { type: 'scenario', activeNodes: ['m1', 'm2', 'm3', 'm4', 'layout'], lines: [5, 6, 7, 8], kind: 'observe' });
      P('recompose.' + sc, { activeNodes: ['layout'], lines: [2], kind: 'recompose' });
      if (sc === 'equal' || sc === 'update') {
        reuse(1); reuse(2);
        if (sc === 'update') {
          c.updated++; act = 'Update';
          P('update', { activeNodes: ['m3'], movingSignals: [{ edge: 'e3', tok: 'state' }], lines: [7], params: { i: 3, el: 'BackgroundElement' }, kind: 'apply', callouts: [{ kind: 'mechanism', textKey: M(m, 'co.update') }] });
        } else reuse(3);
        reuse(4);
      } else if (sc === 'insert') {
        act = 'diff';
        P('diff', { type: 'pitfall', activeNodes: ['m1', 'm2', 'm3', 'm4'], lines: [6], params: { a: 3, b: 4 }, kind: 'act', callouts: [{ kind: 'mechanism', textKey: M(m, 'co.diff') }] });
        reuse(1, true);
        c.inserted++; act = 'insert';
        P('insert', { activeNodes: ['m2'], movingSignals: [{ edge: 'e1', tok: 'ui' }], lines: [6], params: { i: 2, el: EL[1] }, kind: 'apply' });
        reuse(3, true); reuse(4, true);
      } else {
        reuse(1);
        act = 'Replace';
        P('abort', { type: 'pitfall', activeNodes: ['m2'], movingSignals: [{ edge: 'e1', tok: 'error' }], lines: [6], params: { i: 2 }, kind: 'act' });
        c.removed++; act = 'remove';
        P('remove', { type: 'pitfall', activeNodes: ['m2'], lines: [6], params: { i: 2 }, kind: 'apply', callouts: [{ kind: 'pitfall', textKey: M(m, 'co.remove') }] });
        c.inserted++; act = 'insert';
        P('insert', { activeNodes: ['m2'], movingSignals: [{ edge: 'e1', tok: 'ui' }], lines: [6], params: { i: 2, el: EL[1] }, kind: 'apply' });
        reuse(3, true); reuse(4, true);
      }
      act = '—';
      P('end.' + sc, { type: sc === 'replace' ? 'pitfall' : 'mechanism', activeNodes: ['layout'], lines: [], kind: 'observe', callouts: [{ kind: sc === 'replace' ? 'pitfall' : 'mechanism', textKey: M(m, 'co.end.' + sc) }] });
      return out;
    }
    reg(m, {
      codeId: 'chain_reuse',
      simpExtra: [M(m, 'simp.2')],
      controls: [
        { id: 'which', type: 'select', labelKey: M(m, 'ctl.which'), get: function (s) { return s.which; }, action: 'which', options: SC.map(function (v) { return { value: v, labelKey: M(m, 'ctl.which.' + v) }; }) }
      ],
      init: function () { return { which: 'equal' }; },
      act: function (s, a, v) { return { which: SC.indexOf(v) >= 0 ? v : 'equal' }; },
      steps: steps,
      selfChecks: [{ name: 'actionForModifiers: equals → dùng lại 4/4; cùng lớp khác dữ liệu → 3 dùng lại + 1 update; thêm border có điều kiện → diff, 3 giữ + 1 chèn; shadow → border cùng vị trí → 3 giữ, 1 gỡ, 1 chèn', run: function () {
        var last = function (w) { return steps({ which: w }).slice(-1)[0].metrics; };
        var e = last('equal'), u = last('update'), i = last('insert'), r = last('replace');
        return e.reused === 4 && e.updated === 0 && u.reused === 3 && u.updated === 1 && i.reused === 3 && i.inserted === 1 && i.removed === 0 &&
          r.reused === 3 && r.removed === 1 && r.inserted === 1;
      } }]
    });
  })();
  /* ================= LZ (v2): lazy list compose theo nhu cầu và dùng lại slot (LazyLayout.kt, SubcomposeLayout.kt @296313a4; Lists docs) =================
     20 mục, viewport vừa 4. same: mọi mục cùng contentType → frame cuộn 1 compose mới (pool rỗng), mục rời màn hình vào pool; frame 2, 3 dùng lại slot.
     types: mục 0–3 "text", từ mục 4 "image" → slot "text" trong pool không tương thích → luôn compose mới. column: Column + verticalScroll compose cả 20 ngay
     từ đầu, cuộn không compose thêm. Bỏ qua prefetch. */
  (function () {
    var m = 'lazy';
    var SC = ['same', 'types', 'column'];
    function steps(s) {
      var sc = SC.indexOf(s.which) >= 0 ? s.which : 'same', out = [], t = 0, c = { composed: 0, fresh: 0, reused: 0, pool: 0 }, active = '—', pool = [], op = '—';
      var snip = sc === 'types' ? 'lazy_types' : sc === 'column' ? 'lazy_column' : 'lazy_same';
      var type = function (i) { return sc === 'types' ? (i < 4 ? 'text' : 'image') : 'row'; };
      var P = function (key, o) {
        o.id = key.replace(/\./g, '_') + out.length; o.type = o.type || 'mechanism';
        o.titleKey = M(m, 's.' + key + '.title'); o.explainKey = M(m, 's.' + key + '.explain');
        o.params = o.params || {};
        c.pool = pool.length;
        o.metrics = { composed: c.composed, fresh: c.fresh, reused: c.reused, pool: c.pool };
        o.stateAfter = [{ labelKey: M(m, 'st.active'), value: active }, { labelKey: M(m, 'st.pool'), value: pool.length ? '[' + pool.join(', ') + ']' : '—' }, { labelKey: M(m, 'st.op'), value: op }];
        o.movingSignals = o.movingSignals || []; o.activeNodes = o.activeNodes || [];
        o.codeHighlight = { snippet: snip, lines: o.lines || [] }; delete o.lines;
        o.logEvents = [{ t: t += 4, kind: o.kind || 'recompose', subject: o.activeNodes[o.activeNodes.length - 1] || 'measure', detailKey: M(m, 'ev.' + key), params: o.params }]; delete o.kind;
        out.push(o);
      };
      P('intro.' + sc, { type: 'scenario', activeNodes: ['data', 'measure'], lines: sc === 'column' ? [1, 2] : [1, 2], kind: 'observe' });
      if (sc === 'column') {
        c.composed = 20; c.fresh = 20; active = '0–19'; op = 'new ×20';
        P('col.first', { type: 'pitfall', activeNodes: ['data', 'measure', 'active'], movingSignals: [{ edge: 'e1', tok: 'state' }, { edge: 'e2', tok: 'runtime' }], lines: [2, 3] });
        [1, 2, 3].forEach(function (i) {
          op = 'offset'; P('col.scroll', { activeNodes: ['active'], lines: [1], params: { n: i }, kind: 'layout' });
        });
        op = '—';
        P('end.column', { type: 'pitfall', activeNodes: ['active'], lines: [], kind: 'observe', callouts: [{ kind: 'pitfall', textKey: M(m, 'co.end.column') }] });
        return out;
      }
      c.composed = 4; c.fresh = 4; active = '0–3'; op = 'new ×4';
      P('first', { activeNodes: ['data', 'measure', 'active'], movingSignals: [{ edge: 'e1', tok: 'state' }, { edge: 'e2', tok: 'runtime' }], lines: [2, 3] });
      [1, 2, 3].forEach(function (i) {
        var enter = i + 3, leave = i - 1, fromPool = -1;
        for (var k = 0; k < pool.length; k++) if (pool[k].split('·')[1] === type(enter)) { fromPool = k; break; }
        if (fromPool >= 0) {
          var slot = pool.splice(fromPool, 1)[0];
          c.reused++; op = 'reuse ' + slot.split('·')[0] + ' → #' + enter;
        } else { c.fresh++; c.composed++; op = 'new #' + enter; }
        if (fromPool >= 0) c.composed++;
        pool.push('#' + leave + '·' + type(leave));
        active = i + '–' + (i + 3);
        var reused = fromPool >= 0;
        P(reused ? 'reuse' : (i === 1 ? 'new1' : 'newType'), { type: reused ? 'mechanism' : (i === 1 ? 'mechanism' : 'pitfall'), activeNodes: reused ? ['measure', 'pool', 'active'] : ['measure', 'pool', 'active'],
          movingSignals: reused ? [{ edge: 'e3', tok: 'state' }, { edge: 'e4', tok: 'runtime' }] : [{ edge: 'e2', tok: 'runtime' }, { edge: 'e4', tok: 'runtime' }],
          lines: sc === 'types' ? [5, 7] : [2, 3], params: { enter: enter, leave: leave }, callouts: i === 2 ? [{ kind: reused ? 'mechanism' : 'pitfall', textKey: M(m, reused ? 'co.reuse' : 'co.types') }] : [] });
      });
      op = '—';
      P('end.' + sc, { type: 'mechanism', activeNodes: ['pool'], lines: [], kind: 'observe', callouts: [{ kind: 'mechanism', textKey: M(m, 'co.end.' + sc) }] });
      return out;
    }
    reg(m, {
      codeId: 'lazy_same',
      simpExtra: [M(m, 'simp.2')],
      controls: [
        { id: 'which', type: 'select', labelKey: M(m, 'ctl.which'), get: function (s) { return s.which; }, action: 'which', options: SC.map(function (v) { return { value: v, labelKey: M(m, 'ctl.which.' + v) }; }) }
      ],
      init: function () { return { which: 'same' }; },
      act: function (s, a, v) { return { which: SC.indexOf(v) >= 0 ? v : 'same' }; },
      steps: steps,
      selfChecks: [{ name: 'cùng contentType: 3 frame cuộn → 5 compose mới, 2 dùng lại, pool còn 1; khác contentType: 7 mới, 0 dùng lại, pool 3 slot text; Column + verticalScroll: 20 compose từ đầu, cuộn không compose thêm', run: function () {
        var last = function (w) { return steps({ which: w }).slice(-1)[0].metrics; };
        var a = last('same'), b = last('types'), col = last('column');
        return a.fresh === 5 && a.reused === 2 && a.pool === 1 && b.fresh === 7 && b.reused === 0 && b.pool === 3 && col.fresh === 20 && col.reused === 0;
      } }]
    });
  })();
})();
