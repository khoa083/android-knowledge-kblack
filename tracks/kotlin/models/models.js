/* Model track F (thuần, không DOM, không câu chữ; chỉ message key). MÔ HÌNH GIẢNG DẠY (simplified).
   Nguồn: docs/research/kotlin.md (kotlinlang.org đọc ngày 2026-11-23; sách Kotlin Essentials, Effective Kotlin). */
(function () {
  'use strict';
  var K = 'track.kotlin.';
  var M = function (m, s) { return K + 'm.' + m + '.' + s; };
  function S(m, id, o) {
    o.id = id; o.type = o.type || 'mechanism';
    o.titleKey = o.titleKey || M(m, 's.' + id + '.title');
    o.explainKey = o.explainKey || M(m, 's.' + id + '.explain');
    o.params = o.params || {}; o.activeNodes = o.activeNodes || []; o.movingSignals = o.movingSignals || [];
    (o.logEvents || []).forEach(function (e) { if (!e.detailKey) e.detailKey = M(m, 'ev.' + id); if (!e.params) e.params = o.params; });
    return o;
  }
  function reg(m, def) {
    def.kind = 'discrete'; def.titleKey = M(m, 'title'); def.overviewKey = M(m, 'overview'); def.wrapupKey = M(m, 'wrapup');
    def.codeId = def.codeId || null; def.controlsHintKey = M(m, 'ctl.hint'); def.simplificationKeys = [M(m, 'simp.1')].concat(def.simpExtra || []);
    ADE.registerModel('kotlin.' + m, def);
  }
  var sel = function (m, id, vals) { return { id: id, type: 'select', labelKey: M(m, 'ctl.' + id), get: function (s) { return s[id]; }, action: id, options: vals.map(function (v) { return { value: v, labelKey: M(m, 'ctl.' + id + '.' + v) }; }) }; };
  var setter = function (keys) { return function (s, a, v) { var n = {}; keys.forEach(function (k) { n[k] = s[k]; }); if (keys.indexOf(a) >= 0) n[a] = v; return n; }; };

  /* ================= K1: một biểu thức đi từ mã nguồn qua suy kiểu (lúc biên dịch) tới giá trị (lúc chạy) =================
     Bốn trường hợp theo trang Numbers và Conditions and loops: chia nguyên, chia có Double, tràn Int, when có subject.
     Giá trị là kết quả tài liệu nêu (Int.MAX_VALUE + 1 = -2147483648), không tính bằng JavaScript. */
  (function () {
    var m = 'eval', CASES = ['intdiv', 'double', 'overflow', 'when'];
    // [kiểu kết quả, giá trị (số hoặc khóa chữ), loại bước cuối, dòng mã cho 4 bước]
    var C = {
      intdiv: { type: 'Int', value: 7, last: 'pitfall', lines: [[1, 2], [2], [2], [3]] },
      double: { type: 'Double', value: 7.5, last: 'mechanism', lines: [[1, 2], [2], [2], [3]] },
      overflow: { type: 'Int', value: -2147483648, last: 'pitfall', lines: [[1, 2], [2], [2], [3, 4]] },
      when: { type: 'String', value: M(m, 'val.pass'), last: 'mechanism', lines: [[1, 2], [2, 3, 4, 5], [3, 4], [2, 6]] }
    };
    function steps(s) {
      var c = C[s.case], sn = 'eval.' + s.case, typeKey = M(m, 'type.' + c.type);
      var hl = function (i) { return { snippet: sn, lines: c.lines[i] }; };
      return [
        S(m, s.case + '.code', { type: 'scenario', activeNodes: ['src'], codeHighlight: hl(0), callouts: [{ kind: 'try', textKey: M(m, 'co.try') }],
          logEvents: [{ t: 0, kind: 'observe', subject: 'src' }] }),
        S(m, s.case + '.types', { activeNodes: ['types'], movingSignals: [{ edge: 'e1', tok: 'state' }], codeHighlight: hl(1), metrics: { type: typeKey },
          nodeStates: { types: K + 'st.done' }, stateAfter: [{ labelKey: M(m, 'met.type'), valueKey: typeKey }],
          callouts: [{ kind: 'source', textKey: M(m, 'co.' + s.case + '.types') }], logEvents: [{ t: 1, kind: 'check', subject: 'types' }] }),
        S(m, s.case + '.run', { activeNodes: ['eval'], movingSignals: [{ edge: 'e2', tok: 'signal' }], codeHighlight: hl(2), metrics: { type: typeKey, value: c.value },
          nodeStates: { types: K + 'st.done', eval: K + 'st.done' }, logEvents: [{ t: 2, kind: 'run', subject: 'eval' }] }),
        S(m, s.case + '.result', { type: c.last, activeNodes: ['out'], movingSignals: [{ edge: 'e3', tok: 'state' }], codeHighlight: hl(3), metrics: { type: typeKey, value: c.value },
          nodeStates: { types: K + 'st.done', eval: K + 'st.done', out: K + (c.last === 'pitfall' ? 'st.surprise' : 'st.done') },
          callouts: [{ kind: c.last === 'pitfall' ? 'pitfall' : 'mechanism', textKey: M(m, 'co.' + s.case + '.result') }],
          logEvents: [{ t: 3, kind: 'write', subject: 'out' }] })
      ];
    }
    reg(m, { controls: [sel(m, 'case', CASES)], init: function () { return { case: 'intdiv' }; }, act: setter(['case']), steps: steps,
      simpExtra: [M(m, 'simp.2')],
      selfChecks: [
        { name: 'mỗi trường hợp có 4 bước; bước 2 (vị trí 2) luôn là suy kiểu', run: function () { return CASES.every(function (k) { var st = steps({ case: k }); return st.length === 4 && st[1].activeNodes[0] === 'types'; }); } },
        { name: 'chia nguyên cho 7, có Double cho 7.5; tràn Int cho -2147483648 (giá trị tài liệu)', run: function () { return C.intdiv.value === Math.trunc(15 / 2) && C.double.value === 15 / 2 && C.overflow.value === (2147483647 + 1) - 4294967296; } },
        { name: 'chia nguyên và tràn số là bẫy (bước cuối loại pitfall)', run: function () { return steps({ case: 'intdiv' })[3].type === 'pitfall' && steps({ case: 'overflow' })[3].type === 'pitfall' && steps({ case: 'double' })[3].type === 'mechanism'; } }] });
  })();

  /* ================= K3: thứ tự khởi tạo — lớp cha trước, khối init và property theo thứ tự khai báo, object khi truy cập lần đầu =================
     Theo kotlinlang.org: Inheritance (Derived class initialization order), Classes (Initializer blocks), Object declarations, Properties (lateinit). */
  (function () {
    var m = 'init', CASES = ['order', 'openCall', 'object', 'lateinit'];
    // mỗi bước: [node đang xét, trạng thái các node (hậu tố st.*), số khối khởi tạo đã chạy, loại bước, dòng mã, loại log]
    var P = {
      order: [[['trigger'], {}, 0, 'scenario', [9], 'observe'], [['parent'], { parent: 'running' }, 0, 'mechanism', [5, 9], 'run'],
        [['parent'], { parent: 'done' }, 2, 'mechanism', [2, 3], 'run'], [['child', 'use'], { parent: 'done', child: 'done', use: 'done' }, 4, 'mechanism', [6, 7], 'write']],
      openCall: [[['trigger'], {}, 0, 'scenario', [9], 'observe'], [['parent'], { parent: 'running' }, 0, 'mechanism', [2], 'run'],
        [['child'], { parent: 'running', child: 'crashed' }, 0, 'pitfall', [6, 7], 'run'], [['parent', 'child'], { parent: 'done', child: 'done' }, 2, 'mechanism', [2, 3], 'write']],
      object: [[['trigger'], { parent: 'skipped' }, 0, 'scenario', [6], 'observe'], [['child'], { parent: 'skipped', child: 'running' }, 0, 'mechanism', [7], 'run'],
        [['child', 'use'], { parent: 'skipped', child: 'done', use: 'done' }, 1, 'mechanism', [2, 3], 'write'], [['use'], { parent: 'skipped', child: 'done', use: 'done' }, 1, 'mechanism', [8], 'skip']],
      lateinit: [[['trigger'], { parent: 'skipped' }, 0, 'scenario', [1, 2], 'observe'], [['child'], { parent: 'skipped', child: 'done' }, 1, 'mechanism', [2, 6], 'run'],
        [['use'], { parent: 'skipped', child: 'done', use: 'crashed' }, 1, 'pitfall', [4, 6], 'run'], [['use'], { parent: 'skipped', child: 'done', use: 'done' }, 1, 'mechanism', [3, 7], 'write']]
    };
    ADE.kotlinInit = P;
    var EDGE = { trigger: null, parent: 'e1', child: 'e2', use: 'e3' };
    function steps(s) {
      var K4 = ['start', 'first', 'next', 'end'];
      return P[s.case].map(function (p, i) {
        var ns = {}; Object.keys(p[1]).forEach(function (n) { ns[n] = K + 'st.' + p[1][n]; });
        var e = EDGE[p[0][0]];
        var o = S(m, s.case + '.' + K4[i], { type: p[3], activeNodes: p[0], nodeStates: ns, metrics: { inits: p[2] }, codeHighlight: { snippet: 'init.' + s.case, lines: p[4] },
          movingSignals: e ? [{ edge: e, tok: p[3] === 'pitfall' ? 'signal' : 'state' }] : [], logEvents: [{ t: i, kind: p[5], subject: p[0][0] }] });
        if (i === 0) o.callouts = [{ kind: 'try', textKey: M(m, 'co.try') }];
        if (i === 2 || i === 3) o.callouts = [{ kind: p[3] === 'pitfall' ? 'pitfall' : 'source', textKey: M(m, 'co.' + s.case + '.' + K4[i]) }];
        return o;
      });
    }
    reg(m, { controls: [sel(m, 'case', CASES)], init: function () { return { case: 'order' }; }, act: setter(['case']), steps: steps,
      simpExtra: [M(m, 'simp.2')],
      selfChecks: [
        { name: 'mỗi tình huống có 4 bước; bước 2 (vị trí 2) là lúc khởi tạo bắt đầu', run: function () { return CASES.every(function (k) { var st = steps({ case: k }); return st.length === 4 && /running|done/.test(JSON.stringify(st[1].nodeStates)); }); } },
        { name: 'lớp cha khởi tạo xong (2 khối) trước khi lớp con chạy (thêm 2 khối)', run: function () { var st = steps({ case: 'order' }); return st[2].metrics.inits === 2 && st[3].metrics.inits === 4 && !st[2].nodeStates.child; } },
        { name: 'gọi hàm open trong init lớp cha và đọc lateinit trước khi gán đều là bẫy lúc chạy', run: function () { return steps({ case: 'openCall' })[2].type === 'pitfall' && steps({ case: 'lateinit' })[2].type === 'pitfall'; } }] });
  })();

  /* ================= K4: phần tử trong HashSet — hashCode chọn bucket, equals so trong bucket =================
     Bucket là MINH HỌA: tổng mã ký tự chia lấy dư 4 (HashSet thật trải và đổi kích thước bảng). Hành vi contains theo Effective Kotlin Item 43. */
  (function () {
    var m = 'hashset', CASES = ['mutate', 'copy', 'bodyProp', 'plain'];
    var bucket = function (s) { var t = 0; for (var i = 0; i < s.length; i++) t += s.charCodeAt(i); return t % 4; };
    ADE.kotlinBucket = bucket;
    var Y = M(m, 'yes'), N0 = M(m, 'no');
    // mỗi bước: [node, trạng thái node, số đo, loại bước, dòng mã, loại log]
    var b1 = bucket('Lan|Nguyen'), b2 = bucket('Lan|Tran'), bp = bucket('P01');
    var P = {
      mutate: [[['obj'], {}, { bucket: b1, size: 0 }, 'scenario', [1, 2], 'observe'], [['hash', 'bucket'], { hash: 'done', bucket: 'done' }, { bucket: b1, size: 1 }, 'mechanism', [3, 4], 'write'],
        [['obj', 'hash'], { hash: 'surprise', bucket: 'done' }, { bucket: b2, size: 1 }, 'pitfall', [5], 'write'], [['lookup', 'bucket'], { hash: 'surprise', bucket: 'done', lookup: 'broken' }, { bucket: b2, size: 1, found: N0 }, 'pitfall', [6, 7], 'check']],
      copy: [[['obj'], {}, { bucket: b1, size: 0 }, 'scenario', [1, 2], 'observe'], [['hash', 'bucket'], { hash: 'done', bucket: 'done' }, { bucket: b1, size: 1 }, 'mechanism', [3], 'write'],
        [['obj', 'hash'], { hash: 'done', bucket: 'done' }, { bucket: b2, size: 1 }, 'mechanism', [4, 5], 'write'], [['lookup', 'bucket'], { hash: 'done', bucket: 'done', lookup: 'done' }, { bucket: b2, size: 1, found: Y }, 'mechanism', [6], 'check']],
      bodyProp: [[['obj'], {}, { bucket: bp, size: 0 }, 'scenario', [1, 2, 3], 'observe'], [['hash'], { hash: 'done' }, { bucket: bp, size: 0 }, 'mechanism', [4, 5], 'check'],
        [['lookup'], { hash: 'done', lookup: 'done' }, { bucket: bp, size: 0, found: Y }, 'pitfall', [6], 'check'], [['bucket'], { hash: 'done', lookup: 'done', bucket: 'done' }, { bucket: bp, size: 1 }, 'mechanism', [7], 'write']],
      plain: [[['obj'], {}, { size: 0 }, 'scenario', [1, 2, 3], 'observe'], [['hash'], { hash: 'done' }, { size: 0 }, 'mechanism', [2, 3], 'check'],
        [['lookup'], { hash: 'done', lookup: 'broken' }, { size: 0, found: N0 }, 'pitfall', [4], 'check'], [['bucket'], { hash: 'done', lookup: 'broken', bucket: 'done' }, { size: 2 }, 'mechanism', [5], 'write']]
    };
    var EDGE = { obj: null, hash: 'e1', bucket: 'e2', lookup: 'e3' };
    function steps(s) {
      var K4 = ['start', 'first', 'next', 'end'];
      return P[s.case].map(function (p, i) {
        var ns = {}; Object.keys(p[1]).forEach(function (n) { ns[n] = K + 'st.' + p[1][n]; });
        var e = EDGE[p[0][0]];
        var o = S(m, s.case + '.' + K4[i], { type: p[3], activeNodes: p[0], nodeStates: ns, metrics: p[2], codeHighlight: { snippet: 'hash.' + s.case, lines: p[4] },
          movingSignals: e ? [{ edge: e, tok: p[3] === 'pitfall' ? 'signal' : 'state' }] : [], logEvents: [{ t: i, kind: p[5] === 'check' ? 'run' : p[5], subject: p[0][0] }] });   // so sánh trong set xảy ra lúc chạy
        if (i === 0) o.callouts = [{ kind: 'try', textKey: M(m, 'co.try') }];
        if (i >= 2) o.callouts = [{ kind: p[3] === 'pitfall' ? 'pitfall' : 'source', textKey: M(m, 'co.' + s.case + '.' + K4[i]) }];
        return o;
      });
    }
    reg(m, { controls: [sel(m, 'case', CASES)], init: function () { return { case: 'mutate' }; }, act: setter(['case']), steps: steps,
      simpExtra: [M(m, 'simp.2')],
      selfChecks: [
        { name: 'mỗi tình huống có 4 bước', run: function () { return CASES.every(function (k) { return steps({ case: k }).length === 4; }); } },
        { name: 'bucket minh họa trước và sau khi sửa khác nhau, nên contains không tìm thấy', run: function () { var st = steps({ case: 'mutate' }); return b1 !== b2 && st[1].metrics.bucket !== st[2].metrics.bucket && st[3].metrics.found === N0; } },
        { name: 'property trong thân không thuộc equals: set chỉ giữ 1; class thường: set giữ 2', run: function () { return steps({ case: 'bodyProp' })[3].metrics.size === 1 && steps({ case: 'plain' })[3].metrics.size === 2; } }] });
  })();

  /* ================= K5: sealed + when — trình biên dịch biết đủ các kiểu con, nên kiểm được when đã phủ hết chưa =================
     Theo Sealed classes and interfaces (kiểm exhaustive, không cần else) và Enum classes (valueOf ném IllegalArgumentException). */
  (function () {
    var m = 'sealed', CASES = ['exhaustive', 'withElse', 'valueOf'];
    // mỗi bước: [node, trạng thái node, số đo, loại bước, dòng mã, loại log]
    var P = {
      exhaustive: [[['def'], {}, { covered: 3, total: 3 }, 'scenario', [1, 2, 3, 4], 'observe'], [['when', 'compiler'], { compiler: 'done' }, { covered: 3, total: 3 }, 'mechanism', [6, 7, 8, 9, 10], 'check'],
        [['def', 'compiler'], { compiler: 'broken' }, { covered: 3, total: 4 }, 'mechanism', [5, 6], 'check'], [['when', 'screen'], { compiler: 'done', screen: 'done' }, { covered: 4, total: 4 }, 'mechanism', [6], 'write']],
      withElse: [[['def'], {}, { covered: 3, total: 3 }, 'scenario', [1, 2, 3, 4], 'observe'], [['when', 'compiler'], { compiler: 'done' }, { covered: 3, total: 3 }, 'mechanism', [6, 9], 'check'],
        [['def', 'compiler', 'screen'], { compiler: 'done', screen: 'surprise' }, { covered: 2, total: 4 }, 'pitfall', [5, 9], 'run'], [['when', 'compiler'], { compiler: 'broken', screen: 'done' }, { covered: 4, total: 4 }, 'mechanism', [9], 'write']],
      valueOf: [[['def'], {}, {}, 'scenario', [1, 2], 'observe'], [['when'], { when: 'running' }, {}, 'mechanism', [3], 'run'],
        [['screen'], { when: 'running', screen: 'crashed' }, {}, 'pitfall', [3, 4], 'run'], [['when', 'screen'], { when: 'done', screen: 'done' }, {}, 'mechanism', [5, 6], 'write']]
    };
    var EDGE = { def: null, when: 'e1', compiler: 'e2', screen: 'e3' };
    function steps(s) {
      var K4 = ['start', 'first', 'next', 'end'];
      return P[s.case].map(function (p, i) {
        var ns = {}; Object.keys(p[1]).forEach(function (n) { ns[n] = K + 'st.' + p[1][n]; });
        var e = EDGE[p[0][0]] || EDGE[p[0][1]];
        var o = S(m, s.case + '.' + K4[i], { type: p[3], activeNodes: p[0], nodeStates: ns, metrics: p[2], codeHighlight: { snippet: 'sealed.' + s.case, lines: p[4] },
          movingSignals: e ? [{ edge: e, tok: p[3] === 'pitfall' ? 'signal' : 'state' }] : [], logEvents: [{ t: i, kind: p[5], subject: p[0][0] }] });
        if (i === 0) o.callouts = [{ kind: 'try', textKey: M(m, 'co.try') }];
        if (i >= 2) o.callouts = [{ kind: p[3] === 'pitfall' ? 'pitfall' : 'source', textKey: M(m, 'co.' + s.case + '.' + K4[i]) }];
        return o;
      });
    }
    reg(m, { controls: [sel(m, 'case', CASES)], init: function () { return { case: 'exhaustive' }; }, act: setter(['case']), steps: steps,
      simpExtra: [M(m, 'simp.2')],
      selfChecks: [
        { name: 'mỗi tình huống có 4 bước', run: function () { return CASES.every(function (k) { return steps({ case: k }).length === 4; }); } },
        { name: 'không else: thêm kiểu con thì trình biên dịch báo (thiếu 1 nhánh); có else: biên dịch được nhưng sai lúc chạy', run: function () { var a = steps({ case: 'exhaustive' }), b = steps({ case: 'withElse' }); return a[2].metrics.covered < a[2].metrics.total && a[2].nodeStates.compiler === K + 'st.broken' && b[2].type === 'pitfall' && b[2].nodeStates.compiler === K + 'st.done'; } },
        { name: 'valueOf với tên không khớp chính xác là ngoại lệ lúc chạy', run: function () { return steps({ case: 'valueOf' })[2].nodeStates.screen === K + 'st.crashed'; } }] });
  })();

  /* ================= K6: ngoại lệ — ném, lan ngược qua chuỗi gọi tới catch khớp đầu tiên; finally / use đóng tài nguyên =================
     Theo trang Exceptions (try là biểu thức, catch khớp đầu tiên theo kiểu, finally luôn chạy) và hàm use của stdlib (tag v2.1.0, Closeable.kt). */
  (function () {
    var m = 'exception', CASES = ['uncaught', 'swallow', 'resource'];
    // mỗi bước: [node, trạng thái node, số đo, loại bước, dòng mã, loại log, chủ thể log]
    var P = {
      uncaught: [[['call'], {}, { exc: 'none', skipped: 0, closed: 'na' }, 'scenario', [3, 4], 'observe', 'call'],
        [['fn'], { fn: 'crashed' }, { exc: 'nfe', skipped: 1, closed: 'na' }, 'mechanism', [1], 'exception', 'fn'],
        [['fn', 'handler', 'call'], { fn: 'crashed', handler: 'skipped', call: 'crashed' }, { exc: 'nfe', skipped: 3, closed: 'na' }, 'pitfall', [2, 4, 5], 'exception', 'call'],
        [['handler', 'call'], { fn: 'crashed', handler: 'done', call: 'done' }, { exc: 'nfe', skipped: 2, closed: 'na' }, 'mechanism', [8, 9], 'write', 'handler']],
      swallow: [[['call'], {}, { exc: 'none', skipped: 0, closed: 'na' }, 'scenario', [1, 2, 3], 'observe', 'call'],
        [['fn'], { fn: 'crashed' }, { exc: 'nfe', skipped: 1, closed: 'na' }, 'mechanism', [3], 'exception', 'fn'],
        [['handler', 'call'], { fn: 'crashed', handler: 'surprise', call: 'surprise' }, { exc: 'nfe', skipped: 1, closed: 'na' }, 'pitfall', [4, 5, 7], 'run', 'handler'],
        [['handler', 'call'], { fn: 'crashed', handler: 'done', call: 'done' }, { exc: 'nfe', skipped: 1, closed: 'na' }, 'mechanism', [9, 10, 11], 'write', 'handler']],
      resource: [[['call', 'fn'], {}, { exc: 'none', skipped: 0, closed: 'no' }, 'scenario', [1, 2], 'observe', 'call'],
        [['fn'], { fn: 'crashed' }, { exc: 'ioe', skipped: 1, closed: 'no' }, 'mechanism', [3], 'exception', 'fn'],
        [['cleanup'], { fn: 'crashed', cleanup: 'surprise' }, { exc: 'ioe', skipped: 2, closed: 'no' }, 'pitfall', [4], 'skip', 'cleanup'],
        [['cleanup', 'call'], { fn: 'crashed', cleanup: 'done' }, { exc: 'ioe', skipped: 2, closed: 'yes' }, 'mechanism', [8], 'complete', 'cleanup']]
    };
    ADE.kotlinExc = P;
    var EDGE = { call: null, fn: 'e1', handler: 'e2', cleanup: 'e3' };
    function steps(s) {
      var K4 = ['start', 'first', 'next', 'end'];
      return P[s.case].map(function (p, i) {
        var ns = {}; Object.keys(p[1]).forEach(function (n) { ns[n] = K + 'st.' + p[1][n]; });
        var met = { exc: M(m, 'exc.' + p[2].exc), skipped: p[2].skipped, closed: M(m, 'closed.' + p[2].closed) };
        var e = EDGE[p[0][0]] || EDGE[p[0][1]], bad = p[5] === 'exception' || p[3] === 'pitfall';
        var o = S(m, s.case + '.' + K4[i], { type: p[3], activeNodes: p[0], nodeStates: ns, metrics: met, codeHighlight: { snippet: 'exc.' + s.case, lines: p[4] },
          movingSignals: e ? [{ edge: e, tok: bad ? 'signal' : 'state' }] : [], logEvents: [{ t: i, kind: p[5], subject: p[6] }] });
        if (i === 0) o.callouts = [{ kind: 'try', textKey: M(m, 'co.try') }];
        if (i >= 2) o.callouts = [{ kind: p[3] === 'pitfall' ? 'pitfall' : 'source', textKey: M(m, 'co.' + s.case + '.' + K4[i]) }];
        return o;
      });
    }
    reg(m, { controls: [sel(m, 'case', CASES)], init: function () { return { case: 'uncaught' }; }, act: setter(['case']), steps: steps,
      simpExtra: [M(m, 'simp.2')],
      selfChecks: [
        { name: 'mỗi tình huống có 4 bước; bước thứ hai là lúc ngoại lệ được ném', run: function () { return CASES.every(function (k) { var st = steps({ case: k }); return st.length === 4 && st[1].logEvents[0].kind === 'exception'; }); } },
        { name: 'không có catch khớp thì lan tới nơi gọi (crash); catch Exception thì không crash nhưng cho kết quả sai', run: function () { var a = steps({ case: 'uncaught' })[2], b = steps({ case: 'swallow' })[2]; return a.nodeStates.call === K + 'st.crashed' && a.metrics.skipped > 1 && b.nodeStates.call === K + 'st.surprise' && b.type === 'pitfall'; } },
        { name: 'close() viết tay bị bỏ qua khi có ngoại lệ; use đóng tài nguyên nhưng không nuốt ngoại lệ', run: function () { var r = steps({ case: 'resource' }); return r[2].metrics.closed === M(m, 'closed.no') && r[3].metrics.closed === M(m, 'closed.yes') && r[3].metrics.exc === M(m, 'exc.ioe') && r[3].metrics.skipped === 2; } }] });
  })();

  /* ================= K7: collection — tham chiếu read-only, ép kiểu sang Mutable, map trên Map =================
     Theo Create collections (tham chiếu List tới MutableList thấy trạng thái hiện tại; toList là bản chụp), Effective Kotlin Item 1
     (down-cast listOf trên JVM ném UnsupportedOperationException), _Maps.kt tag v2.1.0 (Map.map trả List). */
  (function () {
    var m = 'collections', CASES = ['view', 'downcast', 'mapOnMap'];
    // mỗi bước: [node, trạng thái node, số đo {size, seen, type}, loại bước, dòng mã, loại log, chủ thể log]
    var P = {
      view: [[['source', 'ref'], {}, { size: 2, seen: 2, type: 'listStr' }, 'scenario', [2, 3, 6], 'observe', 'source'],
        [['op', 'source', 'ref'], { op: 'done' }, { size: 3, seen: 3, type: 'listStr' }, 'mechanism', [4, 7, 8], 'write', 'op'],
        [['ref', 'result'], { op: 'done', result: 'surprise' }, { size: 3, seen: 3, type: 'listStr' }, 'pitfall', [9], 'run', 'result'],
        [['ref', 'result'], { op: 'done', result: 'done' }, { size: 3, seen: 2, type: 'listStr' }, 'mechanism', [10, 11], 'write', 'ref']],
      downcast: [[['source'], {}, { size: 2, seen: 2, type: 'listStr' }, 'scenario', [1], 'observe', 'source'],
        [['ref'], { ref: 'done' }, { size: 2, seen: 2, type: 'mutable' }, 'mechanism', [2, 3], 'run', 'ref'],
        [['ref', 'op'], { ref: 'done', op: 'crashed' }, { size: 2, seen: 2, type: 'mutable' }, 'pitfall', [3, 4], 'exception', 'op'],
        [['op', 'result'], { ref: 'done', op: 'done', result: 'done' }, { size: 2, seen: 3, type: 'mutable' }, 'mechanism', [5, 6], 'write', 'result']],
      mapOnMap: [[['source'], {}, { size: 2, seen: 2, type: 'mapInt' }, 'scenario', [1], 'observe', 'source'],
        [['op'], { op: 'done' }, { size: 2, seen: 2, type: 'listInt' }, 'mechanism', [2, 3], 'run', 'op'],
        [['op', 'result'], { op: 'done', result: 'broken' }, { size: 2, seen: 2, type: 'listInt' }, 'pitfall', [4], 'check', 'result'],
        [['op', 'result'], { op: 'done', result: 'done' }, { size: 2, seen: 2, type: 'mapInt' }, 'mechanism', [5, 6], 'write', 'op']]
    };
    ADE.kotlinColl = P;
    var EDGE = { source: null, ref: 'e1', op: 'e2', result: 'e3' };
    function steps(s) {
      var K4 = ['start', 'first', 'next', 'end'];
      return P[s.case].map(function (p, i) {
        var ns = {}; Object.keys(p[1]).forEach(function (n) { ns[n] = K + 'st.' + p[1][n]; });
        var met = { size: p[2].size, seen: p[2].seen, type: M(m, 'type.' + p[2].type) };
        var e = EDGE[p[0][0]] || EDGE[p[0][1]], bad = p[5] === 'exception' || p[3] === 'pitfall';
        var o = S(m, s.case + '.' + K4[i], { type: p[3], activeNodes: p[0], nodeStates: ns, metrics: met, codeHighlight: { snippet: 'coll.' + s.case, lines: p[4] },
          movingSignals: e ? [{ edge: e, tok: bad ? 'signal' : 'state' }] : [], logEvents: [{ t: i, kind: p[5], subject: p[6] }] });
        if (i === 0) o.callouts = [{ kind: 'try', textKey: M(m, 'co.try') }];
        if (i >= 2) o.callouts = [{ kind: p[3] === 'pitfall' ? 'pitfall' : 'source', textKey: M(m, 'co.' + s.case + '.' + K4[i]) }];
        return o;
      });
    }
    reg(m, { controls: [sel(m, 'case', CASES)], init: function () { return { case: 'view' }; }, act: setter(['case']), steps: steps,
      simpExtra: [M(m, 'simp.2')],
      selfChecks: [
        { name: 'mỗi tình huống có 4 bước', run: function () { return CASES.every(function (k) { return steps({ case: k }).length === 4; }); } },
        { name: 'tham chiếu List tới MutableList thấy phần tử mới; bản chụp toList thì không', run: function () { var v = steps({ case: 'view' }); return v[1].metrics.seen === v[1].metrics.size && v[1].metrics.size === 3 && v[3].metrics.seen === 2; } },
        { name: 'ép kiểu listOf sang MutableList rồi add là ngoại lệ lúc chạy; map trên Map cho List, mapValues giữ Map', run: function () { var d = steps({ case: 'downcast' }), mm = steps({ case: 'mapOnMap' }); return d[2].nodeStates.op === K + 'st.crashed' && mm[1].metrics.type === M(m, 'type.listInt') && mm[3].metrics.type === M(m, 'type.mapInt'); } }] });
  })();

  /* ================= K8: lambda và inline — chép thân vào chỗ gọi hay tạo object hàm; return thoát khỏi đâu; lambda bắt gì =================
     Theo Inline functions (inline chép hàm và lambda vào chỗ gọi; non-local return chỉ khi lambda được inline), Returns (return@label),
     Lambdas (closure), What's new in Kotlin 2.0.0 (lambda không inline sinh bằng invokedynamic). Rò rỉ Activity: suy luận từ closure + GC. */
  (function () {
    var m = 'inline', CASES = ['inlined', 'returnBug', 'stored'];
    // mỗi bước: [node, trạng thái node, số đo {objects, exit, captured}, loại bước, dòng mã, loại log, chủ thể log]
    var P = {
      inlined: [[['call'], {}, { objects: 0, exit: 'none', captured: 'taken' }, 'scenario', [1, 2], 'observe', 'call'],
        [['call', 'compile'], { compile: 'done' }, { objects: 0, exit: 'none', captured: 'taken' }, 'mechanism', [7, 8], 'check', 'compile'],
        [['lambda', 'exit'], { compile: 'done', lambda: 'done', exit: 'done' }, { objects: 0, exit: 'outer', captured: 'taken' }, 'mechanism', [3], 'run', 'lambda'],
        [['exit'], { compile: 'done', lambda: 'done', exit: 'done' }, { objects: 0, exit: 'outer', captured: 'taken' }, 'mechanism', [3, 5], 'complete', 'exit']],
      returnBug: [[['call'], {}, { objects: 0, exit: 'none', captured: 'cancelled' }, 'scenario', [1, 2, 3], 'observe', 'call'],
        [['call', 'compile'], { compile: 'done' }, { objects: 0, exit: 'none', captured: 'cancelled' }, 'mechanism', [2], 'check', 'compile'],
        [['lambda', 'exit'], { compile: 'done', lambda: 'done', exit: 'surprise' }, { objects: 0, exit: 'outer', captured: 'cancelled' }, 'pitfall', [3, 6], 'skip', 'exit'],
        [['lambda', 'exit'], { compile: 'done', lambda: 'done', exit: 'done' }, { objects: 0, exit: 'lambda', captured: 'cancelled' }, 'mechanism', [8, 9], 'write', 'lambda']],
      stored: [[['call'], {}, { objects: 0, exit: 'na', captured: 'none' }, 'scenario', [1, 2, 7], 'observe', 'call'],
        [['compile', 'lambda'], { compile: 'done' }, { objects: 1, exit: 'na', captured: 'activity' }, 'mechanism', [7], 'check', 'compile'],
        [['lambda', 'exit'], { compile: 'done', lambda: 'done', exit: 'surprise' }, { objects: 1, exit: 'na', captured: 'activity' }, 'pitfall', [2, 7], 'run', 'exit'],
        [['call', 'exit'], { compile: 'done', lambda: 'done', exit: 'done' }, { objects: 1, exit: 'na', captured: 'none' }, 'mechanism', [9, 10], 'write', 'call']]
    };
    ADE.kotlinInline = P;
    var EDGE = { call: null, compile: 'e1', lambda: 'e2', exit: 'e3' };
    function steps(s) {
      var K4 = ['start', 'first', 'next', 'end'];
      return P[s.case].map(function (p, i) {
        var ns = {}; Object.keys(p[1]).forEach(function (n) { ns[n] = K + 'st.' + p[1][n]; });
        var met = { objects: p[2].objects, exit: M(m, 'exit.' + p[2].exit), captured: M(m, 'cap.' + p[2].captured) };
        var e = EDGE[p[0][0]] || EDGE[p[0][1]], bad = p[3] === 'pitfall';
        var o = S(m, s.case + '.' + K4[i], { type: p[3], activeNodes: p[0], nodeStates: ns, metrics: met, codeHighlight: { snippet: 'inl.' + s.case, lines: p[4] },
          movingSignals: e ? [{ edge: e, tok: bad ? 'signal' : 'state' }] : [], logEvents: [{ t: i, kind: p[5], subject: p[6] }] });
        if (i === 0) o.callouts = [{ kind: 'try', textKey: M(m, 'co.try') }];
        if (i >= 2) o.callouts = [{ kind: p[3] === 'pitfall' ? 'pitfall' : 'source', textKey: M(m, 'co.' + s.case + '.' + K4[i]) }];
        return o;
      });
    }
    reg(m, { controls: [sel(m, 'case', CASES)], init: function () { return { case: 'returnBug' }; }, act: setter(['case']), steps: steps,
      simpExtra: [M(m, 'simp.2')],
      selfChecks: [
        { name: 'mỗi tình huống có 4 bước; bước thứ hai là lúc trình biên dịch quyết định', run: function () { return CASES.every(function (k) { var st = steps({ case: k }); return st.length === 4 && st[1].logEvents[0].kind === 'check'; }); } },
        { name: 'lambda truyền cho hàm inline không tạo object hàm và return trần thoát hàm bao ngoài; return@forEach chỉ thoát lambda', run: function () { var a = steps({ case: 'inlined' }), b = steps({ case: 'returnBug' }); return a[1].metrics.objects === 0 && a[2].metrics.exit === M(m, 'exit.outer') && b[2].type === 'pitfall' && b[3].metrics.exit === M(m, 'exit.lambda'); } },
        { name: 'lambda lưu vào property là object hàm và bắt this; gỡ tham chiếu thì hết giữ Activity', run: function () { var c = steps({ case: 'stored' }); return c[1].metrics.objects === 1 && c[2].metrics.captured === M(m, 'cap.activity') && c[3].metrics.captured === M(m, 'cap.none'); } }] });
  })();

  /* ================= K9: Sequence — xử lý từng phần tử qua cả chuỗi (lười) so với từng bước cho cả list (háo hức) =================
     Theo trang Sequences (Iterable tạo collection trung gian ở mỗi bước; Sequence chạy lười, từng phần tử, chỉ khi có thao tác cuối)
     và Effective Kotlin Item 54. Số lần chạy lambda đếm trên dữ liệu mẫu HOURS, selfCheck tính lại từ HOURS. */
  (function () {
    var m = 'sequence', CASES = ['list', 'sequence', 'noTerminal'];
    var HOURS = [8, 13, 9, 10, 15, 11, 16, 9], TAKE = 2;
    // mỗi bước: [node, trạng thái node, số đo {ops, inter, touched}, loại bước, dòng mã, loại log, chủ thể log]
    var P = {
      list: [[['source'], {}, { ops: 0, inter: 0, touched: 0 }, 'scenario', [1, 2], 'observe', 'source'],
        [['source', 'filter'], { filter: 'done' }, { ops: 8, inter: 1, touched: 8 }, 'mechanism', [3], 'run', 'filter'],
        [['filter', 'map'], { filter: 'done', map: 'done' }, { ops: 13, inter: 2, touched: 8 }, 'mechanism', [4], 'run', 'map'],
        [['map', 'terminal'], { filter: 'done', map: 'done', terminal: 'done' }, { ops: 13, inter: 2, touched: 8 }, 'mechanism', [5], 'complete', 'terminal']],
      sequence: [[['source', 'filter', 'map', 'terminal'], { filter: 'pending', map: 'pending', terminal: 'pending' }, { ops: 0, inter: 0, touched: 0 }, 'scenario', [2, 3, 4, 5], 'observe', 'source'],
        [['filter', 'map', 'terminal'], { filter: 'done', map: 'done', terminal: 'running' }, { ops: 2, inter: 0, touched: 1 }, 'mechanism', [6, 3, 4], 'run', 'filter'],
        [['source', 'filter'], { filter: 'done', map: 'done', terminal: 'running' }, { ops: 3, inter: 0, touched: 2 }, 'mechanism', [3], 'skip', 'filter'],
        [['filter', 'map', 'terminal'], { filter: 'done', map: 'done', terminal: 'done' }, { ops: 5, inter: 0, touched: 3 }, 'mechanism', [3, 4, 5], 'complete', 'terminal']],
      noTerminal: [[['source'], {}, { ops: 0, inter: 0, touched: 0 }, 'scenario', [1, 2], 'observe', 'source'],
        [['filter', 'map'], { filter: 'pending', map: 'pending' }, { ops: 0, inter: 0, touched: 0 }, 'mechanism', [2, 3, 4], 'observe', 'map'],
        [['terminal'], { filter: 'unused', map: 'unused', terminal: 'surprise' }, { ops: 0, inter: 0, touched: 0 }, 'pitfall', [4, 5], 'skip', 'terminal'],
        [['filter', 'map', 'terminal'], { filter: 'done', map: 'done', terminal: 'done' }, { ops: 13, inter: 0, touched: 8 }, 'mechanism', [6, 7], 'write', 'terminal']]
    };
    ADE.kotlinSeq = { P: P, HOURS: HOURS };
    var EDGE = { source: null, filter: 'e1', map: 'e2', terminal: 'e3' };
    function steps(s) {
      var K4 = ['start', 'first', 'next', 'end'];
      return P[s.case].map(function (p, i) {
        var ns = {}; Object.keys(p[1]).forEach(function (n) { ns[n] = K + 'st.' + p[1][n]; });
        var e = EDGE[p[0][0]] || EDGE[p[0][1]], bad = p[3] === 'pitfall';
        var o = S(m, s.case + '.' + K4[i], { type: p[3], activeNodes: p[0], nodeStates: ns, metrics: { ops: p[2].ops, inter: p[2].inter, touched: p[2].touched },
          codeHighlight: { snippet: 'seq.' + s.case, lines: p[4] }, movingSignals: e ? [{ edge: e, tok: bad ? 'signal' : 'state' }] : [], logEvents: [{ t: i, kind: p[5], subject: p[6] }] });
        if (i === 0) o.callouts = [{ kind: 'try', textKey: M(m, 'co.try') }];
        if (i >= 2) o.callouts = [{ kind: p[3] === 'pitfall' ? 'pitfall' : 'source', textKey: M(m, 'co.' + s.case + '.' + K4[i]) }];
        return o;
      });
    }
    // Đếm lại từ HOURS: list = filter mọi phần tử + map mọi phần tử qua lọc; sequence = dừng khi đủ TAKE phần tử.
    function eager() { var kept = HOURS.filter(function (h) { return h < 12; }); return HOURS.length + kept.length; }
    function lazy() { var ops = 0, got = 0, touched = 0; for (var i = 0; i < HOURS.length && got < TAKE; i++) { touched++; ops++; if (HOURS[i] < 12) { ops++; got++; } } return { ops: ops, touched: touched }; }
    reg(m, { controls: [sel(m, 'case', CASES)], init: function () { return { case: 'list' }; }, act: setter(['case']), steps: steps,
      simpExtra: [M(m, 'simp.2')],
      selfChecks: [
        { name: 'mỗi tình huống có 4 bước', run: function () { return CASES.every(function (k) { return steps({ case: k }).length === 4; }); } },
        { name: 'số lần chạy lambda khớp với dữ liệu mẫu: list chạy hết từng bước, sequence dừng khi take đủ', run: function () { var l = steps({ case: 'list' })[3].metrics, q = steps({ case: 'sequence' })[3].metrics, z = lazy(); return l.ops === eager() && l.inter === 2 && q.ops === z.ops && q.touched === z.touched && q.inter === 0; } },
        { name: 'không có thao tác cuối thì không lambda nào chạy', run: function () { var n = steps({ case: 'noTerminal' }); return n[2].metrics.ops === 0 && n[2].type === 'pitfall' && n[3].metrics.ops === eager(); } }] });
  })();

  /* ================= K10: variance — gán C<Doctor> cho C<Staff> (hay ngược lại) được không, tùy C khai báo out, in hay bất biến =================
     Theo Generics: in, out, where (declaration-site variance; quy tắc vị trí out/in; Java arrays → ClassCastException),
     builtins Collections.kt tag v2.1.0 (List<out E>, MutableList<E>), Flow.kt kotlinx.coroutines 1.9.0 (Flow<out T>). */
  (function () {
    var m = 'variance', CASES = ['outList', 'invariantMutable', 'inNotifier'];
    // mỗi bước: [node, trạng thái node, số đo {variance, assign, safe}, loại bước, dòng mã, loại log, chủ thể log]
    var P = {
      outList: [[['decl'], {}, { variance: 'out', assign: 'none', safe: 'na' }, 'scenario', [1, 2, 3], 'observe', 'decl'],
        [['assign', 'compiler'], { compiler: 'done' }, { variance: 'out', assign: 'ok', safe: 'na' }, 'mechanism', [4], 'check', 'compiler'],
        [['compiler', 'call'], { compiler: 'done', call: 'done' }, { variance: 'out', assign: 'ok', safe: 'yes' }, 'mechanism', [5, 6], 'run', 'call'],
        [['decl', 'compiler'], { compiler: 'done', call: 'done' }, { variance: 'out', assign: 'ok', safe: 'yes' }, 'mechanism', [7, 8], 'check', 'compiler']],
      invariantMutable: [[['decl'], {}, { variance: 'inv', assign: 'none', safe: 'na' }, 'scenario', [1, 2, 3], 'observe', 'decl'],
        [['assign', 'compiler'], { compiler: 'broken' }, { variance: 'inv', assign: 'error', safe: 'na' }, 'mechanism', [4], 'check', 'compiler'],
        [['compiler', 'call'], { compiler: 'broken', call: 'crashed' }, { variance: 'inv', assign: 'error', safe: 'cce' }, 'pitfall', [5, 6, 7], 'exception', 'call'],
        [['assign', 'compiler'], { compiler: 'done', call: 'done' }, { variance: 'inv', assign: 'ok', safe: 'yes' }, 'mechanism', [8, 9], 'write', 'assign']],
      inNotifier: [[['decl'], {}, { variance: 'in', assign: 'none', safe: 'na' }, 'scenario', [1, 2, 3], 'observe', 'decl'],
        [['assign', 'compiler'], { compiler: 'done' }, { variance: 'in', assign: 'ok', safe: 'na' }, 'mechanism', [4], 'check', 'compiler'],
        [['compiler', 'call'], { compiler: 'done', call: 'done' }, { variance: 'in', assign: 'ok', safe: 'yes' }, 'mechanism', [5], 'run', 'call'],
        [['assign', 'compiler'], { compiler: 'broken', call: 'done' }, { variance: 'in', assign: 'error', safe: 'yes' }, 'mechanism', [6, 7], 'check', 'compiler']]
    };
    ADE.kotlinVariance = P;
    var EDGE = { decl: null, assign: 'e1', compiler: 'e2', call: 'e3' };
    function steps(s) {
      var K4 = ['start', 'first', 'next', 'end'];
      return P[s.case].map(function (p, i) {
        var ns = {}; Object.keys(p[1]).forEach(function (n) { ns[n] = K + 'st.' + p[1][n]; });
        var met = { variance: M(m, 'v.' + p[2].variance), assign: M(m, 'a.' + p[2].assign), safe: M(m, 'safe.' + p[2].safe) };
        var e = EDGE[p[0][0]] || EDGE[p[0][1]], bad = p[3] === 'pitfall' || p[2].assign === 'error';
        var o = S(m, s.case + '.' + K4[i], { type: p[3], activeNodes: p[0], nodeStates: ns, metrics: met, codeHighlight: { snippet: 'var.' + s.case, lines: p[4] },
          movingSignals: e ? [{ edge: e, tok: bad ? 'signal' : 'state' }] : [], logEvents: [{ t: i, kind: p[5], subject: p[6] }] });
        if (i === 0) o.callouts = [{ kind: 'try', textKey: M(m, 'co.try') }];
        if (i >= 2) o.callouts = [{ kind: p[3] === 'pitfall' ? 'pitfall' : 'source', textKey: M(m, 'co.' + s.case + '.' + K4[i]) }];
        return o;
      });
    }
    reg(m, { controls: [sel(m, 'case', CASES)], init: function () { return { case: 'invariantMutable' }; }, act: setter(['case']), steps: steps,
      simpExtra: [M(m, 'simp.2')],
      selfChecks: [
        { name: 'mỗi tình huống có 4 bước; bước thứ hai là trình biên dịch kiểm phép gán', run: function () { return CASES.every(function (k) { var st = steps({ case: k }); return st.length === 4 && st[1].logEvents[0].kind === 'check'; }); } },
        { name: 'out: C<Doctor> gán được cho C<Staff>; bất biến: không; in: chỉ chiều ngược lại', run: function () { var A = function (k, i) { return steps({ case: k })[i].metrics.assign; }; return A('outList', 1) === M(m, 'a.ok') && A('invariantMutable', 1) === M(m, 'a.error') && A('inNotifier', 1) === M(m, 'a.ok') && A('inNotifier', 3) === M(m, 'a.error'); } },
        { name: 'lý do MutableList bất biến: nếu cho phép thì ghi được phần tử sai kiểu, lỗi lúc chạy', run: function () { var s2 = steps({ case: 'invariantMutable' })[2]; return s2.type === 'pitfall' && s2.metrics.safe === M(m, 'safe.cce'); } }] });
  })();

  /* ================= K11: delegation — đọc property đi qua getValue của delegate; ba chế độ của lazy khi hai luồng đọc lần đầu cùng lúc =================
     Theo Delegated properties (prop$delegate, getValue/setValue; lazy mặc định synchronized, PUBLICATION, NONE) và mã stdlib tag v2.1.0
     (LazyJVM.kt: SynchronizedLazyImpl khóa, SafePublicationLazyImpl compareAndSet, UnsafeLazyImpl không khóa; Lazy.kt: NONE "unspecified").
     Tình huống hai luồng là kịch bản xấu nhất CÓ THỂ xảy ra, không phải lần nào cũng vậy. */
  (function () {
    var m = 'delegate', CASES = ['synchronized', 'publication', 'none'];
    // mỗi bước: [node, trạng thái node, số đo {runs, instances}, loại bước, dòng mã, loại log, chủ thể log]
    var P = {
      synchronized: [[['access', 'delegate'], {}, { runs: 0, instances: 0 }, 'scenario', [2, 5, 6], 'observe', 'access'],
        [['access', 'delegate', 'init'], { delegate: 'running', init: 'running' }, { runs: 1, instances: 0 }, 'mechanism', [7, 2], 'run', 'init'],
        [['init', 'value'], { delegate: 'done', init: 'done', value: 'done' }, { runs: 1, instances: 1 }, 'mechanism', [2], 'write', 'value'],
        [['access', 'value'], { delegate: 'done', init: 'done', value: 'done' }, { runs: 1, instances: 1 }, 'mechanism', [6], 'complete', 'access']],
      publication: [[['access', 'delegate'], {}, { runs: 0, instances: 0 }, 'scenario', [1], 'observe', 'access'],
        [['delegate', 'init'], { delegate: 'running', init: 'running' }, { runs: 2, instances: 0 }, 'mechanism', [1, 2], 'run', 'init'],
        [['init', 'value'], { delegate: 'done', init: 'done', value: 'done' }, { runs: 2, instances: 1 }, 'mechanism', [3], 'write', 'value'],
        [['access', 'value'], { delegate: 'done', init: 'done', value: 'done' }, { runs: 2, instances: 1 }, 'mechanism', [4], 'complete', 'access']],
      none: [[['access', 'delegate'], {}, { runs: 0, instances: 0 }, 'scenario', [1], 'observe', 'access'],
        [['delegate', 'init'], { delegate: 'running', init: 'running' }, { runs: 2, instances: 0 }, 'mechanism', [1, 2], 'run', 'init'],
        [['init', 'value'], { delegate: 'done', init: 'done', value: 'surprise' }, { runs: 2, instances: 2 }, 'pitfall', [3], 'write', 'value'],
        [['delegate', 'value'], { delegate: 'done', init: 'done', value: 'done' }, { runs: 1, instances: 1 }, 'mechanism', [4, 5], 'write', 'delegate']]
    };
    ADE.kotlinDelegate = P;
    var EDGE = { access: null, delegate: 'e1', init: 'e2', value: 'e3' };
    function steps(s) {
      var K4 = ['start', 'first', 'next', 'end'];
      return P[s.case].map(function (p, i) {
        var ns = {}; Object.keys(p[1]).forEach(function (n) { ns[n] = K + 'st.' + p[1][n]; });
        var e = EDGE[p[0][0]] || EDGE[p[0][1]], bad = p[3] === 'pitfall';
        var o = S(m, s.case + '.' + K4[i], { type: p[3], activeNodes: p[0], nodeStates: ns, metrics: { mode: M(m, 'mode.' + s.case), runs: p[2].runs, instances: p[2].instances },
          codeHighlight: { snippet: 'del.' + s.case, lines: p[4] }, movingSignals: e ? [{ edge: e, tok: bad ? 'signal' : 'state' }] : [], logEvents: [{ t: i, kind: p[5], subject: p[6] }] });
        if (i === 0) o.callouts = [{ kind: 'try', textKey: M(m, 'co.try') }];
        if (i >= 2) o.callouts = [{ kind: p[3] === 'pitfall' ? 'pitfall' : 'source', textKey: M(m, 'co.' + s.case + '.' + K4[i]) }];
        return o;
      });
    }
    reg(m, { controls: [sel(m, 'case', CASES)], init: function () { return { case: 'synchronized' }; }, act: setter(['case']), steps: steps,
      simpExtra: [M(m, 'simp.2')],
      selfChecks: [
        { name: 'mỗi chế độ có 4 bước', run: function () { return CASES.every(function (k) { return steps({ case: k }).length === 4; }); } },
        { name: 'SYNCHRONIZED: initializer chạy đúng 1 lần, mọi luồng thấy 1 giá trị; PUBLICATION: có thể chạy nhiều lần nhưng chỉ 1 giá trị được dùng', run: function () { var a = steps({ case: 'synchronized' })[3].metrics, b = steps({ case: 'publication' })[3].metrics; return a.runs === 1 && a.instances === 1 && b.runs > 1 && b.instances === 1; } },
        { name: 'NONE với hai luồng: các luồng có thể nhận object khác nhau (bẫy)', run: function () { var c = steps({ case: 'none' })[2]; return c.type === 'pitfall' && c.metrics.instances > 1; } }] });
  })();

  /* ================= K12: scope function và DSL — một tên trong lambda được hiểu theo receiver gần nhất, rồi tới receiver bên ngoài =================
     Theo Scope functions (bảng this/it, giá trị trả về; khuyên tránh lồng), Type-safe builders (@DslMarker: chỉ receiver gần nhất),
     Null safety (?. và ?: — vế phải chạy khi vế trái null). */
  (function () {
    var m = 'scope', CASES = ['nestedApply', 'letElvis', 'dslMarker'];
    // mỗi bước: [node, trạng thái node, số đo {recv, res, out}, loại bước, dòng mã, loại log, chủ thể log]
    var P = {
      nestedApply: [[['name'], {}, { recv: 'none', res: 'none', out: 'none' }, 'scenario', [1, 2, 3, 4, 5, 6, 7, 8], 'observe', 'name'],
        [['name', 'near'], { near: 'done' }, { recv: 'booking', res: 'bookingTitle', out: 'titleOk' }, 'mechanism', [2, 3], 'write', 'near'],
        [['near', 'far', 'result'], { near: 'skipped', far: 'surprise', result: 'surprise' }, { recv: 'patient', res: 'bookingTitle', out: 'titleLost' }, 'pitfall', [4, 5, 6], 'write', 'far'],
        [['name', 'near', 'result'], { near: 'done', far: 'skipped', result: 'done' }, { recv: 'patientIt', res: 'patientSalutation', out: 'titleOk' }, 'mechanism', [9, 10, 11], 'write', 'near']],
      letElvis: [[['name'], {}, { recv: 'none', res: 'none', out: 'none' }, 'scenario', [1], 'observe', 'name'],
        [['name', 'near'], { near: 'done' }, { recv: 'itToken', res: 'none', out: 'none' }, 'mechanism', [1], 'run', 'near'],
        [['near', 'far', 'result'], { near: 'done', far: 'surprise', result: 'surprise' }, { recv: 'itToken', res: 'letNull', out: 'loggedOut' }, 'pitfall', [1, 2], 'run', 'far'],
        [['name', 'result'], { near: 'done', far: 'skipped', result: 'done' }, { recv: 'none', res: 'refreshNull', out: 'retry' }, 'mechanism', [3, 4, 5], 'write', 'result']],
      dslMarker: [[['name'], {}, { recv: 'none', res: 'none', out: 'none' }, 'scenario', [1, 2, 3, 4, 5, 6], 'observe', 'name'],
        [['name', 'near'], { near: 'done' }, { recv: 'section', res: 'none', out: 'none' }, 'mechanism', [3, 4], 'run', 'near'],
        [['near', 'far', 'result'], { near: 'skipped', far: 'surprise', result: 'surprise' }, { recv: 'section', res: 'formSection', out: 'wrongPlace' }, 'pitfall', [5], 'run', 'far'],
        [['near', 'far', 'result'], { near: 'done', far: 'broken', result: 'done' }, { recv: 'section', res: 'compileError', out: 'explicit' }, 'mechanism', [7, 8, 9], 'check', 'far']]
    };
    ADE.kotlinScope = P;
    var EDGE = { name: null, near: 'e1', far: 'e2', result: 'e3' };
    function steps(s) {
      var K4 = ['start', 'first', 'next', 'end'];
      return P[s.case].map(function (p, i) {
        var ns = {}; Object.keys(p[1]).forEach(function (n) { ns[n] = K + 'st.' + p[1][n]; });
        var met = { recv: M(m, 'recv.' + p[2].recv), res: M(m, 'res.' + p[2].res), out: M(m, 'out.' + p[2].out) };
        var e = EDGE[p[0][0]] || EDGE[p[0][1]], bad = p[3] === 'pitfall';
        var o = S(m, s.case + '.' + K4[i], { type: p[3], activeNodes: p[0], nodeStates: ns, metrics: met, codeHighlight: { snippet: 'scope.' + s.case, lines: p[4] },
          movingSignals: e ? [{ edge: e, tok: bad ? 'signal' : 'state' }] : [], logEvents: [{ t: i, kind: p[5], subject: p[6] }] });
        if (i === 0) o.callouts = [{ kind: 'try', textKey: M(m, 'co.try') }];
        if (i >= 2) o.callouts = [{ kind: p[3] === 'pitfall' ? 'pitfall' : 'source', textKey: M(m, 'co.' + s.case + '.' + K4[i]) }];
        return o;
      });
    }
    reg(m, { controls: [sel(m, 'case', CASES)], init: function () { return { case: 'nestedApply' }; }, act: setter(['case']), steps: steps,
      simpExtra: [M(m, 'simp.2')],
      selfChecks: [
        { name: 'mỗi tình huống có 4 bước; bước thứ ba là bẫy', run: function () { return CASES.every(function (k) { var st = steps({ case: k }); return st.length === 4 && st[2].type === 'pitfall'; }); } },
        { name: 'apply lồng: receiver gần nhất không có tên thì tên được hiểu theo receiver bên ngoài', run: function () { var a = steps({ case: 'nestedApply' })[2]; return a.metrics.recv === M(m, 'recv.patient') && a.metrics.res === M(m, 'res.bookingTitle') && a.nodeStates.near === K + 'st.skipped'; } },
        { name: '@DslMarker biến lời gọi ngầm tới receiver ngoài thành lỗi biên dịch', run: function () { var d = steps({ case: 'dslMarker' }); return d[2].metrics.res === M(m, 'res.formSection') && d[3].metrics.res === M(m, 'res.compileError'); } }] });
  })();

  /* ================= K13: Java interop — một khai báo Kotlin được trình biên dịch biến thành gì để Java gọi =================
     Theo Calling Kotlin from Java (companion → Companion, @JvmStatic; tham số mặc định chỉ thấy chữ ký đầy đủ, @JvmOverloads;
     hàm public kiểm null lúc chạy cho tham số non-null). */
  (function () {
    var m = 'jvm', CASES = ['companion', 'overloads', 'nullFromJava'];
    // mỗi bước: [node, trạng thái node, số đo {sig, call, annot}, loại bước, dòng mã, loại log, chủ thể log]
    var P = {
      companion: [[['kotlin'], {}, { sig: 'none', call: 'none', annot: 'none' }, 'scenario', [1, 2, 3, 4], 'observe', 'kotlin'],
        [['kotlin', 'compiler', 'jvm'], { compiler: 'done', jvm: 'done' }, { sig: 'companionInstance', call: 'none', annot: 'none' }, 'mechanism', [2, 3], 'check', 'compiler'],
        [['jvm', 'java'], { compiler: 'done', jvm: 'done', java: 'broken' }, { sig: 'companionInstance', call: 'compileError', annot: 'none' }, 'pitfall', [5, 6], 'check', 'java'],
        [['kotlin', 'jvm', 'java'], { compiler: 'done', jvm: 'done', java: 'done' }, { sig: 'staticFormat', call: 'ok', annot: 'jvmStatic' }, 'mechanism', [7, 8], 'write', 'kotlin']],
      overloads: [[['kotlin'], {}, { sig: 'none', call: 'none', annot: 'none' }, 'scenario', [1], 'observe', 'kotlin'],
        [['compiler', 'jvm'], { compiler: 'done', jvm: 'done' }, { sig: 'fullOnly', call: 'none', annot: 'none' }, 'mechanism', [1, 2], 'check', 'compiler'],
        [['jvm', 'java'], { compiler: 'done', jvm: 'done', java: 'broken' }, { sig: 'fullOnly', call: 'compileError', annot: 'none' }, 'pitfall', [3, 4], 'check', 'java'],
        [['kotlin', 'jvm', 'java'], { compiler: 'done', jvm: 'done', java: 'done' }, { sig: 'overloads', call: 'ok', annot: 'jvmOverloads' }, 'mechanism', [5, 6, 7], 'write', 'kotlin']],
      nullFromJava: [[['kotlin'], {}, { sig: 'none', call: 'none', annot: 'none' }, 'scenario', [1], 'observe', 'kotlin'],
        [['compiler', 'jvm'], { compiler: 'done', jvm: 'done' }, { sig: 'checked', call: 'none', annot: 'none' }, 'mechanism', [1, 2], 'check', 'compiler'],
        [['jvm', 'java'], { compiler: 'done', jvm: 'crashed', java: 'done' }, { sig: 'checked', call: 'npe', annot: 'none' }, 'pitfall', [3, 4], 'exception', 'jvm'],
        [['kotlin', 'jvm', 'java'], { compiler: 'done', jvm: 'done', java: 'done' }, { sig: 'nullableParam', call: 'ok', annot: 'nullable' }, 'mechanism', [5, 6], 'write', 'kotlin']]
    };
    ADE.kotlinJvm = P;
    var EDGE = { kotlin: null, compiler: 'e1', jvm: 'e2', java: 'e3' };
    function steps(s) {
      var K4 = ['start', 'first', 'next', 'end'];
      return P[s.case].map(function (p, i) {
        var ns = {}; Object.keys(p[1]).forEach(function (n) { ns[n] = K + 'st.' + p[1][n]; });
        var met = { sig: M(m, 'sig.' + p[2].sig), call: M(m, 'call.' + p[2].call), annot: M(m, 'annot.' + p[2].annot) };
        var e = EDGE[p[0][0]] || EDGE[p[0][1]], bad = p[3] === 'pitfall';
        var o = S(m, s.case + '.' + K4[i], { type: p[3], activeNodes: p[0], nodeStates: ns, metrics: met, codeHighlight: { snippet: 'jvm.' + s.case, lines: p[4] },
          movingSignals: e ? [{ edge: e, tok: bad ? 'signal' : 'state' }] : [], logEvents: [{ t: i, kind: p[5], subject: p[6] }] });
        if (i === 0) o.callouts = [{ kind: 'try', textKey: M(m, 'co.try') }];
        if (i >= 2) o.callouts = [{ kind: p[3] === 'pitfall' ? 'pitfall' : 'source', textKey: M(m, 'co.' + s.case + '.' + K4[i]) }];
        return o;
      });
    }
    reg(m, { controls: [sel(m, 'case', CASES)], init: function () { return { case: 'companion' }; }, act: setter(['case']), steps: steps,
      simpExtra: [M(m, 'simp.2')],
      selfChecks: [
        { name: 'mỗi tình huống có 4 bước; bước thứ ba là bẫy, bước cuối Java gọi được', run: function () { return CASES.every(function (k) { var st = steps({ case: k }); return st.length === 4 && st[2].type === 'pitfall' && st[3].metrics.call === M(m, 'call.ok'); } ); } },
        { name: 'không có chú thích: Java không gọi tĩnh được hàm companion và không thấy overload; có chú thích thì được', run: function () { var a = steps({ case: 'companion' }), b = steps({ case: 'overloads' }); return a[2].metrics.call === M(m, 'call.compileError') && a[3].metrics.annot === M(m, 'annot.jvmStatic') && b[2].metrics.sig === M(m, 'sig.fullOnly') && b[3].metrics.sig === M(m, 'sig.overloads'); } },
        { name: 'Java truyền null cho tham số non-null: kiểm tra Kotlin chèn vào ném NPE ngay khi gọi', run: function () { var c = steps({ case: 'nullFromJava' })[2]; return c.metrics.call === M(m, 'call.npe') && c.nodeStates.jvm === K + 'st.crashed'; } }] });
  })();

  /* ================= K2: smart cast — trình biên dịch có bảo đảm biến không đổi giữa lúc kiểm và lúc dùng không =================
     Điều kiện theo trang "Type checks and casts" (Smart cast prerequisites); platform type theo "Calling Java from Kotlin". */
  (function () {
    var m = 'smartcast', KINDS = ['localVal', 'varProp', 'openProp', 'lambdaVar', 'platform'];
    // smart: có smart cast không ('yes' | 'no' | 'na' = không cần, kiểu là platform type); fail: lỗi lúc nào ('none' | 'compile' | 'runtime')
    var R = {
      localVal: { smart: 'yes', fail: 'none', lines: [[2, 3], [3, 4], [4], [8]] },
      varProp: { smart: 'no', fail: 'compile', lines: [[1, 3], [3, 4], [4], [8]] },
      openProp: { smart: 'no', fail: 'compile', lines: [[1, 3], [3, 4], [4], [8]] },
      lambdaVar: { smart: 'no', fail: 'compile', lines: [[1, 2, 3], [2, 4], [4], [6]] },
      platform: { smart: 'na', fail: 'runtime', lines: [[1, 2], [2], [3], [4, 5]] }
    };
    ADE.kotlinSmart = R;
    function steps(s) {
      var r = R[s.kind], sn = 'smart.' + s.kind, hl = function (i) { return { snippet: sn, lines: r.lines[i] }; };
      var ruleSt = r.smart === 'yes' ? 'st.done' : r.smart === 'no' ? 'st.broken' : 'st.skipped';
      var useSt = r.fail === 'none' ? 'st.done' : r.fail === 'compile' ? 'st.broken' : 'st.crashed';
      var met = { smart: M(m, 'smart.' + r.smart), fail: M(m, 'fail.' + r.fail) };
      return [
        S(m, s.kind + '.code', { type: 'scenario', activeNodes: ['src', 'check'], codeHighlight: hl(0), callouts: [{ kind: 'try', textKey: M(m, 'co.try') }],
          logEvents: [{ t: 0, kind: 'observe', subject: 'src' }] }),
        S(m, s.kind + '.rule', { type: r.smart === 'no' ? 'pitfall' : 'mechanism', activeNodes: ['rule'], movingSignals: [{ edge: 'e2', tok: 'state' }], codeHighlight: hl(1),
          nodeStates: { rule: K + ruleSt }, metrics: { smart: met.smart }, stateAfter: [{ labelKey: M(m, 'met.smart'), valueKey: met.smart }],
          callouts: [{ kind: 'source', textKey: M(m, 'co.' + s.kind + '.rule') }], logEvents: [{ t: 1, kind: 'check', subject: 'rule' }] }),
        S(m, s.kind + '.use', { type: r.fail === 'none' ? 'mechanism' : 'pitfall', activeNodes: ['use'], movingSignals: [{ edge: 'e3', tok: r.fail === 'none' ? 'state' : 'signal' }], codeHighlight: hl(2),
          nodeStates: { rule: K + ruleSt, use: K + useSt }, metrics: met, logEvents: [{ t: 2, kind: r.fail === 'compile' ? 'check' : 'run', subject: 'use' }] }),
        S(m, s.kind + '.fix', { activeNodes: ['src', 'use'], codeHighlight: hl(3), nodeStates: { rule: K + ruleSt, use: K + 'st.done' }, metrics: met,
          callouts: [{ kind: 'mechanism', textKey: M(m, 'co.' + s.kind + '.fix') }], logEvents: [{ t: 3, kind: 'write', subject: 'src' }] })
      ];
    }
    reg(m, { controls: [sel(m, 'kind', KINDS)], init: function () { return { kind: 'varProp' }; }, act: setter(['kind']), steps: steps,
      simpExtra: [M(m, 'simp.2')],
      selfChecks: [
        { name: 'mỗi loại biến có 4 bước; bước 2 (vị trí 2) là luật smart cast', run: function () { return KINDS.every(function (k) { var st = steps({ kind: k }); return st.length === 4 && st[1].activeNodes[0] === 'rule'; }); } },
        { name: 'theo bảng điều kiện của tài liệu: val cục bộ được; var property, open property, var bị lambda sửa thì không', run: function () { return R.localVal.smart === 'yes' && R.varProp.smart === 'no' && R.openProp.smart === 'no' && R.lambdaVar.smart === 'no'; } },
        { name: 'platform type biên dịch được nhưng có thể NPE lúc chạy', run: function () { return R.platform.fail === 'runtime' && steps({ kind: 'platform' })[2].type === 'pitfall'; } }] });
  })();
})();
