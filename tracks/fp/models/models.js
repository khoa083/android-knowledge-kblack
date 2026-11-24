/* Model track K (thuần, không DOM, không câu chữ; chỉ message key). MÔ HÌNH GIẢNG DẠY (simplified).
   Nguồn: docs/research/fp.md (sách của Carli, Vermeulen và cộng sự, Barbini, Seemann và tài liệu chính thức, đọc từ 2026-11-24). */
(function () {
  'use strict';
  var K = 'track.fp.';
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
    ADE.registerModel('fp.' + m, def);
  }
  var sel = function (m, id, vals) { return { id: id, type: 'select', labelKey: M(m, 'ctl.' + id), get: function (s) { return s[id]; }, action: id, options: vals.map(function (v) { return { value: v, labelKey: M(m, 'ctl.' + id + '.' + v) }; }) }; };
  var setter = function (keys) { return function (s, a, v) { var n = {}; keys.forEach(function (k) { n[k] = s[k]; }); if (keys.indexOf(a) >= 0) n[a] = v; return n; }; };

  /* ================= K1: hàm thuần và referential transparency: fee() đọc ngày hiện tại so với fee(date) =================
     Theo Carli, FP in Kotlin by Tutorials ch.3 (hai điều kiện của hàm thuần; RT; mô hình thay thế; println và biến đếm là side effect);
     Vermeulen và cộng sự, FP in Kotlin ch.1 (định nghĩa RT, thay bằng kết quả không đổi nghĩa chương trình); Seemann 13.1.3 (query phải tất định:
     không giờ trong ngày, ngày trong tháng). HÀM PHÍ CÀI THẬT dưới đây; mọi hàng thay thế, kết quả test theo ngày và chỉ số đều tính từ nó.
     Tuần 23–29/11/2026 (thứ Hai tới Chủ nhật) và hai mức phí là của site. */
  (function () {
    var m = 'pure', CASES = ['impure', 'pure'], KS = ['s1', 's2', 's3', 's4'];
    var WEEK = [['mon', 23], ['tue', 24], ['wed', 25], ['thu', 26], ['fri', 27], ['sat', 28], ['sun', 29]];   // tháng 11/2026
    var WEEKEND = ['sat', 'sun'], WEEKDAY_FEE = 200000, WEEKEND_FEE = 300000, TODAY = 'sat', RUN_FIRST = 'mon';
    var fee = function (day) { return WEEKEND.indexOf(day) >= 0 ? WEEKEND_FEE : WEEKDAY_FEE; };
    var kt = function (n) { return String(n).replace(/\B(?=(\d{3})+(?!\d))/g, '_'); };   // 200000 → 200_000 như trong mã Kotlin
    // số lần calls++ chạy: fee() + fee() gọi hai lần; val a = fee(); a + a gọi một lần
    var CALLS = { direct: 2, extracted: 1 };
    // hàng của bảng thế: [bước xuất hiện, mã, ok | bad | start, lý do]
    function rows(c) {
      if (c === 'impure') return [
        [0, 'total = fee() + fee()', 'start', 'start'],
        [0, 'total = ' + kt(fee(RUN_FIRST)) + ' + ' + kt(fee(RUN_FIRST)), 'bad', 'runMon'],
        [0, 'total = ' + kt(fee(TODAY)) + ' + ' + kt(fee(TODAY)), 'bad', 'runSat'],
        [1, 'val a = fee(); total = a + a', CALLS.direct === CALLS.extracted ? 'ok' : 'bad', 'calls']];
      var v = fee(TODAY);
      return [
        [0, 'total = fee(d) + fee(d)', 'start', 'start'],
        [0, 'total = fee(2026-11-28) + fee(2026-11-28)', 'ok', 'valD'],
        [1, 'total = (if (true) ' + kt(WEEKEND_FEE) + ' else ' + kt(WEEKDAY_FEE) + ') + (if (true) ' + kt(WEEKEND_FEE) + ' else ' + kt(WEEKDAY_FEE) + ')', 'ok', 'body'],
        [1, 'total = ' + kt(v) + ' + ' + kt(v), 'ok', 'eval'],
        [1, 'total = ' + kt(v + v), 'ok', 'sum'],
        [1, 'val a = fee(d); total = a + a', 'ok', 'same']];
    }
    // test chạy vào ngày nào cho kết quả gì: fee() phụ thuộc ngày chạy; fee(date) chỉ phụ thuộc ngày truyền vào
    function testPasses(c, runDay) { return c === 'impure' ? fee(runDay) === WEEKDAY_FEE : (fee('mon') === WEEKDAY_FEE && fee('sat') === WEEKEND_FEE); }
    function runDays(i) { return i < 2 ? [] : (i === 2 ? [RUN_FIRST] : WEEK.map(function (d) { return d[0]; })); }
    function view(c, i) {
      var shown = rows(c).filter(function (r) { return r[0] <= i; });
      var runs = runDays(i).map(function (d) { return [d, testPasses(c, d)]; });
      return { rows: shown, runs: runs, ok: shown.filter(function (r) { return r[2] === 'ok'; }).length, bad: shown.filter(function (r) { return r[2] === 'bad'; }).length,
        red: runs.filter(function (r) { return !r[1]; }).length };
    }
    ADE.fpPure = { WEEK: WEEK, fee: fee, rows: rows, view: view, testPasses: testPasses };
    var HL = { impure: [[4, 7], [3, 7], [8], [4, 8]], pure: [[5, 6], [1, 2, 3, 6], [7, 8], [9]] };
    var NODES = {
      impure: [[['call', 'world', 'value'], { world: 'surprise' }, 'e1'], [['call', 'world'], { world: 'surprise' }, 'e1'], [['value', 'test'], { test: 'done' }, 'e3'], [['world', 'test'], { world: 'surprise', test: 'surprise' }, 'e1']],
      pure: [[['call', 'value'], { value: 'done' }, 'e2'], [['call', 'value'], { value: 'done' }, 'e2'], [['value', 'test'], { test: 'done' }, 'e3'], [['world', 'call'], { world: 'done', call: 'done' }, 'e1']] };
    function steps(s) {
      var c = s.case, bad = c === 'impure';
      return KS.map(function (k, i) {
        var v = view(c, i), nd = NODES[c][i], warn = bad && (i !== 2), ns = {};
        Object.keys(nd[1]).forEach(function (n) { ns[n] = K + 'st.' + nd[1][n]; });
        var o = S(m, c + '.' + k, { type: i === 0 ? 'scenario' : (warn ? 'pitfall' : 'mechanism'), activeNodes: nd[0], nodeStates: ns,
          metrics: { subst: v.ok, opaque: v.bad, red: v.red },
          codeHighlight: { snippet: 'p1.' + c, lines: HL[c][i] },
          movingSignals: [{ edge: nd[2], tok: warn ? 'signal' : 'state' }],
          logEvents: [{ t: i, kind: warn ? 'exception' : (i === 3 ? 'complete' : (i === 2 ? 'run' : 'observe')), subject: nd[0][nd[0].length - 1] }] });
        o.callouts = [{ kind: i === 0 && bad ? 'try' : (warn ? 'pitfall' : 'source'), textKey: i === 0 && bad ? M(m, 'co.try') : M(m, 'co.' + c + '.' + k) }];
        return o;
      });
    }
    var LEN = { 'p1.impure': 8, 'p1.pure': 9 };
    reg(m, { controls: [sel(m, 'case', CASES)], init: function () { return { case: 'impure' }; }, act: setter(['case']), steps: steps,
      simpExtra: [M(m, 'simp.2')],
      selfChecks: [
        { name: 'lịch: 23/11/2026 là thứ Hai, 28/11/2026 là thứ Bảy; phí 200.000 từ thứ Hai tới thứ Sáu, 300.000 thứ Bảy và Chủ nhật', run: function () {
          var dow = function (d) { return new Date(Date.UTC(2026, 10, d)).getUTCDay(); };
          return WEEK.every(function (w, n) { return dow(w[1]) === (n + 1) % 7; }) && WEEK.filter(function (w) { return fee(w[0]) === WEEKDAY_FEE; }).length === 5 && fee('sat') === WEEKEND_FEE && fee('sun') === WEEKEND_FEE; } },
        { name: 'fee(): test ngày thường đỏ đúng hai ngày (thứ Bảy, Chủ nhật); fee(date): không ngày nào đỏ', run: function () {
          return view('impure', 3).red === 2 && view('impure', 3).runs.filter(function (r) { return !r[1]; }).map(function (r) { return r[0]; }).join() === 'sat,sun' && view('pure', 3).red === 0 && view('impure', 2).red === 0; } },
        { name: 'bảng thế: fee() có hàng không thay được ở bước 1 và 2; fee(d) mọi hàng thay được và tổng bằng hai lần phí thứ Bảy', run: function () {
          return view('impure', 0).bad === 2 && view('impure', 1).bad === 3 && view('pure', 3).bad === 0 && rows('pure')[4][1] === 'total = 600_000' && rows('impure')[1][1] === 'total = 200_000 + 200_000'; } },
        { name: 'mỗi cách 4 bước; mọi dòng tô sáng nằm trong đoạn mã', run: function () {
          return CASES.every(function (c) { return steps({ case: c }).length === 4 && HL[c].every(function (l) { return l.every(function (x) { return x >= 1 && x <= LEN['p1.' + c]; }); }); }); } }] });
  })();

  /* ================= K2: bất biến, dữ liệu dùng chung, đệ quy và tailrec =================
     Hai điều khiển độc lập: cách giữ danh sách (bước 1–2) và cách đệ quy (bước 3–4).
     Theo Vermeulen và cộng sự ch.3.3 (data sharing: thêm vào đầu trả Cons(x, xs), không chép xs; bỏ phần tử đầu là trả tail; persistent),
     ch.2 (tail call, tailrec, StackOverflowError), ch.3 Exercise 3.9 (foldRight không stack-safe); Carli ch.6 (tailrec thành vòng while), ch.7
     (immutable, functional, persistent); tài liệu Kotlin Functions (điều kiện tailrec). CÀI THẬT: một list persistent nhỏ (đếm nút được tạo,
     kiểm đuôi dùng chung bằng ===), một MutableList dùng chung tên, đệ quy thường có đếm độ sâu và tailrec như vòng lặp có tích lũy.
     Giới hạn 10.000 khung là con số minh họa của site: độ sâu thật tùy kích thước stack của luồng và của mỗi khung. */
  (function () {
    var m = 'persist', LISTS = ['mutable', 'persistent'], RECS = ['plain', 'tailrec'], KS = ['s1', 's2', 's3', 's4'];
    var N = 50000, FEE = 200000, LIMIT = 10000, MARKS = [0, 5000, 10000, 20000, 30000, 40000, 50000];
    var Nil = { nil: true }, made = 0;
    var cons = function (h, t) { made++; return { head: h, tail: t }; };
    var arr = function (xs) { var r = []; while (!xs.nil) { r.push(xs.head); xs = xs.tail; } return r; };
    // [booked, selected, rest] sau bước 1 và bước 2; shared: số nút của selected là nút của booked (cùng object)
    function listRun(kind) {
      if (kind === 'mutable') {
        var booked = ['b1', 'b2', 'b3'], selected = booked, out = [];
        selected.push('b4'); out.push({ booked: booked.slice(), selected: selected.slice(), rest: null, alias: selected === booked, nodes: 0, touched: 1, added: 'b4', lost: null });
        var lost = selected.splice(0, 1)[0]; out.push({ booked: booked.slice(), selected: selected.slice(), rest: null, alias: selected === booked, nodes: 0, touched: 2, added: 'b4', lost: lost });
        return out;
      }
      made = 0; var b = cons('b1', cons('b2', cons('b3', Nil))); made = 0;
      var sel = cons('b4', b), n1 = made, shared1 = sel.tail === b ? arr(b).length : 0;
      var rest = sel.tail, n2 = made;
      return [{ booked: arr(b), selected: arr(sel), rest: null, alias: false, nodes: n1, shared: shared1, touched: 0, added: 'b4', lost: null },
        { booked: arr(b), selected: arr(sel), rest: arr(rest), restIsBooked: rest === b, alias: false, nodes: n2, shared: shared1, touched: 0, added: 'b4', lost: null }];
    }
    // độ sâu stack tại các mốc; đệ quy thường: đi xuống trước, mỗi phần tử thêm một khung; tràn khi vượt LIMIT
    function stackRun(rec) {
      var at = {}, k;
      if (rec === 'plain') {
        for (k = 0; k <= N; k++) { var depth = k + 1; if (MARKS.indexOf(k) >= 0) at[k] = depth; if (depth > LIMIT) return { at: at, crash: k, total: null, max: LIMIT }; }
        return { at: at, crash: null, total: null, max: N + 1 };
      }
      var acc = 0;   // tailrec: trình biên dịch đổi thành vòng lặp, một khung suốt quá trình
      for (k = 0; k < N; k++) { if (MARKS.indexOf(k) >= 0) at[k] = 1; acc += FEE; }
      at[N] = 1;
      return { at: at, crash: null, total: acc, max: 1 };
    }
    function view(s, i) {
      var L = listRun(s.list), R = stackRun(s.rec), shown = i < 2 ? [] : MARKS.slice(0, i === 2 ? 2 : MARKS.length);
      var marks = MARKS.map(function (k) {
        if (shown.indexOf(k) < 0) return [k, null];
        if (R.crash !== null && k > R.crash) return [k, 'skip'];
        if (R.crash !== null && k === R.crash) return [k, 'crash'];
        return [k, R.at[k]];
      });
      var deepest = 0; marks.forEach(function (x) { if (typeof x[1] === 'number' && x[1] > deepest) deepest = x[1]; if (x[1] === 'crash') deepest = LIMIT; });
      return { list: L[Math.min(i, 1)], marks: marks, depth: deepest, crashed: i === 3 && R.crash !== null, total: i === 3 ? R.total : null };
    }
    ADE.fpPersist = { N: N, FEE: FEE, LIMIT: LIMIT, MARKS: MARKS, view: view, listRun: listRun, stackRun: stackRun };
    var HL = { mutable: [[2, 3], [2, 4]], persistent: [[4, 5], [6]], plain: [[3], [3]], tailrec: [[1, 3], [2]] };
    function steps(s) {
      return KS.map(function (k, i) {
        var v = view(s, i), listStep = i < 2, kind = listStep ? s.list : s.rec, bad = listStep ? s.list === 'mutable' : s.rec === 'plain';
        var nodes = listStep ? ['selected', 'booked'] : ['fold', 'stack'], ns = {};
        ns[nodes[1]] = K + 'st.' + (bad ? (i === 3 ? 'broken' : 'surprise') : 'done');
        var o = S(m, kind + '.' + k, { type: i === 0 ? 'scenario' : (bad ? 'pitfall' : 'mechanism'), activeNodes: nodes, nodeStates: ns,
          metrics: { touched: listStep ? v.list.touched : listRun(s.list)[1].touched, nodes: listStep ? v.list.nodes : listRun(s.list)[1].nodes, depth: v.depth },
          codeHighlight: { snippet: 'p2.' + kind, lines: HL[kind][i % 2] },
          movingSignals: [{ edge: listStep ? 'e1' : 'e3', tok: bad ? 'signal' : 'state' }],
          logEvents: [{ t: i, kind: bad && (i === 1 || i === 3) ? 'exception' : (i === 3 ? 'complete' : (listStep ? 'write' : 'run')), subject: nodes[1] }] });
        var tryIt = i === 0 && s.list === 'mutable';
        o.callouts = [{ kind: tryIt ? 'try' : (bad ? 'pitfall' : 'source'), textKey: tryIt ? M(m, 'co.try') : M(m, 'co.' + kind + '.' + k) }];
        return o;
      });
    }
    var LEN = { 'p2.mutable': 4, 'p2.persistent': 6, 'p2.plain': 4, 'p2.tailrec': 4 };
    reg(m, { controls: [sel(m, 'list', LISTS), sel(m, 'rec', RECS)], init: function () { return { list: 'mutable', rec: 'plain' }; }, act: setter(['list', 'rec']), steps: steps,
      simpExtra: [M(m, 'simp.2')],
      selfChecks: [
        { name: 'MutableList dùng chung tên: thêm b4 rồi bỏ phần tử đầu làm booked thành [b2, b3, b4]', run: function () {
          var r = listRun('mutable'); return r[0].alias && r[1].booked.join() === 'b2,b3,b4' && r[1].lost === 'b1' && r[1].touched === 2; } },
        { name: 'list persistent: thêm vào đầu tạo đúng 1 nút, 3 nút đuôi dùng chung (===); tail tạo 0 nút và chính là booked; booked không đổi', run: function () {
          var r = listRun('persistent'); return r[0].nodes === 1 && r[0].shared === 3 && r[1].nodes === 1 && r[1].restIsBooked && r[1].booked.join() === 'b1,b2,b3' && r[0].selected.join() === 'b4,b1,b2,b3'; } },
        { name: 'đệ quy thường tràn ở phần tử thứ 10.000 (giới hạn minh họa); tailrec giữ 1 khung và cộng đủ 50.000 × 200.000 = 10.000.000.000', run: function () {
          var p = stackRun('plain'), t = stackRun('tailrec'); return p.crash === LIMIT && p.total === null && t.max === 1 && t.total === 10000000000 && MARKS.every(function (k) { return t.at[k] === 1; }); } },
        { name: 'mọi tổ hợp 4 bước; bước 4 với đệ quy thường là tràn stack; mọi dòng tô sáng nằm trong đoạn mã', run: function () {
          return LISTS.every(function (l) { return RECS.every(function (r) { var x = steps({ list: l, rec: r }); return x.length === 4 && (r === 'plain') === view({ list: l, rec: r }, 3).crashed; }); }) &&
            Object.keys(HL).every(function (k) { return HL[k].every(function (l) { return l.every(function (x) { return x >= 1 && x <= LEN['p2.' + k]; }); }); }); } }] });
  })();
})();
