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

  /* ================= K3: ghép hàm: lời gọi lồng nhau và hàm 6 tham số so với compose và partial application =================
     Theo Carli ch.8 (compose, after, curry, pipe, partial application, đặt tham số ít đổi lên trước, quá nhiều tham số là thói quen xấu);
     Vermeulen và cộng sự ch.2 (partial1, curry, compose: chữ ký dẫn đường, closure giữ a). CÀI THẬT: bốn hàm parse, assign, price, format
     chạy trên một lịch hẹn, compose và partial viết bằng JS; bốn chỗ gọi tính ra chuỗi thật; đếm đối số từ danh sách đối số của từng chỗ gọi.
     Múi giờ chỉ có hai: giờ phòng khám (UTC+7) và UTC. Lịch hẹn, bác sĩ, phí là của site. */
  (function () {
    var m = 'compose', CASES = ['nested', 'composed'], KS = ['s1', 's2', 's3', 's4'];
    var ZONES = { clinic: 7, utc: 0 }, DOW = ['CN', 'T2', 'T3', 'T4', 'T5', 'T6', 'T7'];
    var RAW = 'an|2026-11-28T02:00Z';
    var pad = function (n) { return (n < 10 ? '0' : '') + n; };
    // bốn bước của luồng, mỗi bước một hàm một tham số
    var parse = function (raw) { var p = raw.split('|'), t = p[1]; return { doctor: p[0], y: +t.slice(0, 4), mo: +t.slice(5, 7), d: +t.slice(8, 10), h: +t.slice(11, 13), mi: +t.slice(14, 16) }; };
    var assign = function (r) { return { doctor: 'BS ' + r.doctor.charAt(0).toUpperCase() + r.doctor.slice(1), utc: Date.UTC(r.y, r.mo - 1, r.d, r.h, r.mi) }; };
    var local = function (utc, zone) { var x = new Date(utc + ZONES[zone] * 3600000); return { dow: x.getUTCDay(), d: x.getUTCDate(), mo: x.getUTCMonth() + 1, h: x.getUTCHours(), mi: x.getUTCMinutes() }; };
    var price = function (b) { var w = local(b.utc, 'clinic').dow; return { booking: b, fee: (w === 0 || w === 6) ? 300000 : 200000 }; };   // phí theo ngày ở phòng khám (chương K1)
    var money = function (n) { return String(n).replace(/\B(?=(\d{3})+(?!\d))/g, '.') + ' đ'; };
    var format = function (locale, currency, zone, b, fee, compact) {
      var t = local(b.utc, zone), when = DOW[t.dow] + ' ' + pad(t.d) + '/' + pad(t.mo) + ' ' + pad(t.h) + ':' + pad(t.mi);
      return compact ? when : when + ' · ' + b.doctor + ' · ' + money(fee);
    };
    var compose = function (f, g) { return function (a) { return g(f(a)); }; };
    var formatFor = function (locale, currency, zone) { return function (p, compact) { return format(locale, currency, zone, p.booking, p.fee, compact); }; };
    var SITES = ['list', 'detail', 'reminder', 'receipt'], COMPACT = { list: true, detail: false, reminder: false, receipt: false };
    // đối số ở từng chỗ gọi (để đếm); nested: 6 đối số, ba cái đầu là cấu hình; chỗ nhắc lịch chép UTC từ test
    function calls(c) {
      return SITES.map(function (site) {
        if (c === 'nested') { var zone = site === 'reminder' ? 'utc' : 'clinic'; return { site: site, args: ['VI', 'VND', zone === 'utc' ? 'UTC' : 'CLINIC_ZONE', 'b', 'price(b)', String(COMPACT[site])], config: 3, zone: zone }; }
        return { site: site, args: ['toPriced(raw)', String(COMPACT[site])], config: 0, zone: 'clinic' };
      });
    }
    function render(c) {
      if (c === 'nested') { var b = assign(parse(RAW)); return calls(c).map(function (x) { return format('vi', 'VND', x.zone, b, price(b).fee, COMPACT[x.site]); }); }
      var toPriced = compose(compose(parse, assign), price), show = formatFor('vi', 'VND', 'clinic');
      return SITES.map(function (site) { return show(toPriced(RAW), COMPACT[site]); });
    }
    // luồng: giá trị sau từng hàm, kiểu vào và ra
    function stages() {
      var r = parse(RAW), b = assign(r), p = price(b);
      return [['parse', 'String', 'Request', r.doctor + ' · ' + r.y + '-' + pad(r.mo) + '-' + pad(r.d) + ' ' + pad(r.h) + ':' + pad(r.mi) + 'Z'],
        ['assign', 'Request', 'Booking', b.doctor + ' · ' + format('vi', 'VND', 'clinic', b, 0, true)],
        ['price', 'Booking', 'Priced', money(p.fee)],
        ['format', 'Priced', 'String', format('vi', 'VND', 'clinic', b, p.fee, false)]];
    }
    // số đối số phải sửa khi thêm một tham số cấu hình (ví dụ đồng hồ 24 giờ): mọi chỗ gọi có truyền cấu hình, hay chỉ một lần dựng show
    var EDITS = { nested: SITES.length, composed: 1 };
    function count(c) {
      var cs = calls(c), out = render(c), good = render('composed');
      return { args: cs.reduce(function (n, x) { return n + x.args.length; }, 0), repeated: cs.reduce(function (n, x) { return n + x.config; }, 0),
        wrong: out.filter(function (s, k) { return s !== good[k]; }).length, edits: EDITS[c] };
    }
    ADE.fpCompose = { RAW: RAW, SITES: SITES, calls: calls, render: render, stages: stages, count: count };
    var HL = { nested: [[4], [5, 6, 7, 8], [7], [1, 2]], composed: [[1, 2], [3, 4, 5], [8], [5]] };
    var NODES = [[['raw', 'pipe'], 'pipe', 'e1'], [['config', 'screens'], 'screens', 'e3'], [['pipe', 'screens'], 'screens', 'e2'], [['config', 'screens'], 'config', 'e3']];
    function steps(s) {
      var c = s.case, bad = c === 'nested', n = count(c);
      return KS.map(function (k, i) {
        var nd = NODES[i], ns = {}; ns[nd[1]] = K + 'st.' + (bad && i > 0 ? (i === 2 ? 'broken' : 'surprise') : 'done');
        var o = S(m, c + '.' + k, { type: i === 0 ? 'scenario' : (bad ? 'pitfall' : 'mechanism'), activeNodes: nd[0], nodeStates: ns,
          metrics: { args: i >= 1 ? n.args : 0, repeated: i >= 1 ? n.repeated : 0, wrong: i >= 2 ? n.wrong : 0, edits: i >= 3 ? n.edits : 0 },
          codeHighlight: { snippet: 'p3.' + c, lines: HL[c][i] },
          movingSignals: [{ edge: nd[2], tok: bad && i > 0 ? 'signal' : 'state' }],
          logEvents: [{ t: i, kind: bad && i === 2 ? 'exception' : (i === 3 ? 'complete' : (i === 0 ? 'observe' : 'run')), subject: nd[1] }] });
        o.callouts = [{ kind: i === 0 && bad ? 'try' : (bad && i > 0 ? 'pitfall' : 'source'), textKey: i === 0 && bad ? M(m, 'co.try') : M(m, 'co.' + c + '.' + k) }];
        return o;
      });
    }
    var LEN = { 'p3.nested': 8, 'p3.composed': 9 };
    reg(m, { controls: [sel(m, 'case', CASES)], init: function () { return { case: 'nested' }; }, act: setter(['case']), steps: steps,
      simpExtra: [M(m, 'simp.2')],
      selfChecks: [
        { name: 'luồng: 02:00Z ngày 28/11/2026 là 09:00 thứ Bảy ở phòng khám (UTC+7), phí cuối tuần 300.000 đ', run: function () {
          var st = stages(); return st[3][3] === 'T7 28/11 09:00 · BS An · 300.000 đ' && st.map(function (x) { return x[0]; }).join() === 'parse,assign,price,format'; } },
        { name: 'ghép compose(parse, assign, price) rồi show cho cùng chuỗi với lời gọi lồng nhau ở mọi chỗ gọi đúng múi giờ', run: function () {
          var a = render('nested'), b = render('composed'); return a[0] === b[0] && a[1] === b[1] && a[3] === b[3] && b[0] === 'T7 28/11 09:00'; } },
        { name: 'đếm: lồng nhau 24 đối số, 12 là cấu hình lặp lại, 1 chỗ sai giờ (02:00), thêm tham số sửa 4 chỗ; ghép: 8 đối số, 0 lặp, 0 sai, sửa 1 chỗ', run: function () {
          var a = count('nested'), b = count('composed'); return a.args === 24 && a.repeated === 12 && a.wrong === 1 && a.edits === 4 && render('nested')[2].indexOf('02:00') > 0 && b.args === 8 && b.repeated === 0 && b.wrong === 0 && b.edits === 1; } },
        { name: 'mỗi cách 4 bước; mọi dòng tô sáng nằm trong đoạn mã', run: function () {
          return CASES.every(function (c) { return steps({ case: c }).length === 4 && HL[c].every(function (l) { return l.every(function (x) { return x >= 1 && x <= LEN['p3.' + c]; }); }); }); } }] });
  })();

  /* ================= K4: kiểu dữ liệu đại số: UiState ba trường độc lập (product) so với sealed interface (sum) =================
     Theo Carli ch.10 (Pair là tích Descartes: số giá trị nhân nhau; Either là tổng; Unit là 1, Nothing là 0; Optional là A + 1;
     callback (Data, Result?, Error?) không an toàn kiểu, viết lại thành Result * (Info + Error)); tài liệu Kotlin Sealed classes (when phủ đủ).
     CÀI THẬT: liệt kê mọi tổ hợp của ba trường, luật "có nghĩa" theo thiết kế màn hình đã nói rõ (bản 1: tải, lỗi, danh sách; bản 2 thêm
     tải lại giữ dữ liệu cũ), chạy chuỗi if của màn hình trên từng tổ hợp, mô phỏng khối catch quên tắt isLoading. Đếm theo dạng:
     mỗi trường nullable tính "có" hoặc "không" (A + 1 với A tính là 1 dạng). Ba màn dùng state là của site. */
  (function () {
    var m = 'adt', CASES = ['product', 'sum'], KS = ['s1', 's2', 's3', 's4'], SCREENS = ['slots', 'home', 'summary'];
    var FIELDS = [['isLoading', [true, false]], ['error', ['msg', null]], ['slots', ['list', null]]];
    function combos() {   // tích Descartes của ba trường: 2 × 2 × 2
      var out = [[]];
      FIELDS.forEach(function (f) { var nx = []; out.forEach(function (c) { f[1].forEach(function (v) { nx.push(c.concat([v])); }); }); out = nx; });
      return out.map(function (c) { return { l: c[0], e: c[1], d: c[2] }; });
    }
    var VARIANTS = function (v2) { return v2 ? ['Loading', 'Error', 'Success', 'Refreshing'] : ['Loading', 'Error', 'Success']; };
    // thiết kế màn: bản 1 có ba trạng thái; bản 2 (bước 4) thêm tải lại giữ dữ liệu cũ
    function meaning(x, v2) {
      if (x.l && !x.e && !x.d) return 'loading';
      if (!x.l && x.e && !x.d) return 'error';
      if (!x.l && !x.e && x.d) return 'success';
      if (v2 && x.l && !x.e && x.d) return 'refresh';
      return null;
    }
    var WANT = { loading: 'spinner', error: 'error', success: 'list', refresh: 'listRefreshing' };
    // chuỗi if của màn hình (dòng 7 của p4.product)
    function productUi(x) { if (x.l) return 'spinner'; if (x.e) return 'error'; return x.d ? 'list' : 'crash'; }
    function sumUi(v) { return { Loading: 'spinner', Error: 'error', Success: 'list', Refreshing: 'listRefreshing' }[v]; }
    // khối catch: từ Loading, đặt lỗi; product quên tắt isLoading
    function afterCatch(c) { if (c === 'product') { var s = { l: true, e: null, d: null }; s.e = 'msg'; return s; } return 'Error'; }
    function view(c, i) {
      var v2 = i === 3;
      if (c === 'product') {
        var rows = combos().map(function (x) { var mn = meaning(x, v2), ui = productUi(x); return { x: x, meaning: mn, ui: ui, wrong: mn ? ui !== WANT[mn] : true }; });
        var invalid = rows.filter(function (r) { return !r.meaning; }).length, silent = v2 ? rows.filter(function (r) { return r.meaning && r.wrong; }).length * SCREENS.length : 0;
        return { rows: rows, combos: rows.length, invalid: invalid, silent: silent, flagged: 0, bug: i >= 2 ? afterCatch(c) : null };
      }
      var vs = VARIANTS(v2).map(function (v) { return { v: v, ui: sumUi(v), meaning: v.toLowerCase() === 'refreshing' ? 'refresh' : v.toLowerCase() }; });
      return { rows: vs, combos: vs.length, invalid: 0, silent: 0, flagged: v2 ? SCREENS.length : 0, bug: i >= 2 ? afterCatch(c) : null };
    }
    ADE.fpAdt = { FIELDS: FIELDS, SCREENS: SCREENS, combos: combos, meaning: meaning, productUi: productUi, view: view, WANT: WANT };
    var HL = { product: [[1, 2, 3, 4, 5], [7], [6], [7]], sum: [[1, 2, 3, 4, 6], [8], [7], [5, 8]] };
    var NODES = [[['type', 'states'], 'states', 'e1'], [['states', 'screen'], 'screen', 'e2'], [['catch', 'states'], 'states', 'e3'], [['states', 'screen'], 'screen', 'e2']];
    function steps(s) {
      var c = s.case, bad = c === 'product';
      return KS.map(function (k, i) {
        var v = view(c, i), nd = NODES[i], ns = {}; ns[nd[1]] = K + 'st.' + (bad && i > 0 ? (i === 2 ? 'broken' : 'surprise') : 'done');
        var o = S(m, c + '.' + k, { type: i === 0 ? 'scenario' : (bad ? 'pitfall' : 'mechanism'), activeNodes: nd[0], nodeStates: ns,
          metrics: { combos: v.combos, invalid: i >= 1 ? v.invalid : 0, silent: v.silent, flagged: v.flagged },
          codeHighlight: { snippet: 'p4.' + c, lines: HL[c][i] },
          movingSignals: [{ edge: nd[2], tok: bad && i > 0 ? 'signal' : 'state' }],
          logEvents: [{ t: i, kind: bad && i >= 2 ? 'exception' : (i === 3 ? 'complete' : (i === 2 ? 'run' : 'observe')), subject: nd[1] }] });
        o.callouts = [{ kind: i === 0 && bad ? 'try' : (bad && i > 0 ? 'pitfall' : 'source'), textKey: i === 0 && bad ? M(m, 'co.try') : M(m, 'co.' + c + '.' + k) }];
        return o;
      });
    }
    var LEN = { 'p4.product': 7, 'p4.sum': 8 };
    reg(m, { controls: [sel(m, 'case', CASES)], init: function () { return { case: 'product' }; }, act: setter(['case']), steps: steps,
      simpExtra: [M(m, 'simp.2')],
      selfChecks: [
        { name: 'product: 2 × 2 × 2 = 8 tổ hợp, đúng 3 có nghĩa ở bản 1 (5 vô nghĩa), 4 ở bản 2; sum: 3 rồi 4 kiểu con, không tổ hợp vô nghĩa', run: function () {
          var a = view('product', 0), b = view('product', 3), s1 = view('sum', 0), s4 = view('sum', 3);
          return a.combos === 8 && a.invalid === 5 && b.invalid === 4 && s1.combos === 3 && s4.combos === 4 && s1.invalid === 0; } },
        { name: 'chuỗi if: (false, null, null) làm slots!! crash; khối catch quên tắt isLoading tạo (true, lỗi, null), màn chỉ hiện spinner', run: function () {
          var bug = afterCatch('product'); return productUi({ l: false, e: null, d: null }) === 'crash' && bug.l && bug.e && !meaning(bug, false) && productUi(bug) === 'spinner' && afterCatch('sum') === 'Error'; } },
        { name: 'bước 4: tải lại giữ dữ liệu cũ bị chuỗi if hiện thành spinner ở 3 màn mà không ai báo; sealed: 3 chỗ when bị trình biên dịch chỉ ra, 0 sai im lặng', run: function () {
          var b = view('product', 3), s4 = view('sum', 3); return productUi({ l: true, e: null, d: 'list' }) === 'spinner' && b.silent === 3 && s4.flagged === 3 && s4.silent === 0; } },
        { name: 'mỗi cách 4 bước; mọi dòng tô sáng nằm trong đoạn mã', run: function () {
          return CASES.every(function (c) { return steps({ case: c }).length === 4 && HL[c].every(function (l) { return l.every(function (x) { return x >= 1 && x <= LEN['p4.' + c]; }); }); }); } }] });
  })();

  /* ================= K5: lỗi là giá trị: cùng luồng đặt lịch viết bằng ngoại lệ, nullable, Result và kiểu lỗi riêng =================
     Theo Vermeulen và cộng sự ch.4 (ngoại lệ phá referential transparency, kiểu hàm không nói gì về lỗi, giá trị đặc biệt như null
     để lỗi lặng lẽ đi tiếp); Carli ch.14 (đưa side effect vào kiểu trả về; dừng ở lỗi đầu tiên; Result<T> của Kotlin, lỗi là Throwable);
     Barbini ch.7 (null ổn khi lý do hiển nhiên; ngoại lệ chỉ cho việc không cứu được; kiểu kết quả sealed); API kotlin.Result và
     runCatching (bắt mọi Throwable). CÀI THẬT: bốn bước parse, slot, quota, save chạy trên bốn tình huống; mỗi cách viết quyết định
     lỗi đi đâu (giá trị, ngoại lệ bị bắt, hay không ai bắt) và màn hình hiện gì. Số điện thoại, mã giờ, ngày nghỉ là của site. */
  (function () {
    var m = 'errors', CASES = ['throw', 'nullable', 'result', 'typed'], KS = ['s1', 's2', 's3', 's4'];
    var SCEN = ['ok', 'taken', 'bug', 'closed'], STEPS = ['parse', 'slot', 'quota', 'save'];
    // bước hỏng và loại lỗi của từng tình huống: lỗi nghiệp vụ (biz) hay lỗi lập trình (bug: quotas[phone]!! với số mới)
    var FAIL = { ok: null, taken: { at: 'slot', kind: 'biz' }, bug: { at: 'quota', kind: 'bug' }, closed: { at: 'slot', kind: 'biz' } };
    var OK_VAL = { parse: 'Phone("0901234567")', slot: 'Slot("S12")', quota: 'quotaLeft = 2', save: 'Booking(41)' };
    var ERR_VAL = {
      throw: { taken: 'SlotTakenException("S07")', bug: 'NullPointerException', closed: 'ClinicClosedException' },
      nullable: { taken: 'null', bug: 'NullPointerException', closed: 'null' },
      result: { taken: 'Result.failure(SlotTakenException)', bug: 'Result.failure(NullPointerException)', closed: 'Result.failure(ClinicClosedException)' },
      typed: { taken: 'Err(SlotTaken("S07"))', bug: 'NullPointerException', closed: 'Err(ClinicClosed)' } };
    var SIG = { throw: 'Booking', nullable: 'Booking?', result: 'Result<Booking>', typed: 'Outcome<BookingError, Booking>' };
    // ai bắt lỗi lập trình: catch (e: Exception) và runCatching bắt mọi thứ; nullable và kiểu lỗi riêng không bắt
    var CATCHES_ALL = { throw: true, nullable: false, result: true, typed: false };
    // màn hình đọc kết quả thế nào (dòng cuối của mỗi đoạn mã)
    function screen(c, scen) {
      var f = FAIL[scen];
      if (!f) return 'booked';
      if (f.kind === 'bug') return CATCHES_ALL[c] ? 'failed' : 'crash';
      if (scen === 'taken') return (c === 'result' || c === 'typed') ? 'taken' : 'failed';
      return c === 'typed' ? 'compile' : 'failed';   // closed: lỗi mới; chỉ when không else trên sealed bị trình biên dịch chặn
    }
    function run(c, scen) {
      var f = FAIL[scen], hit = false, rows = STEPS.map(function (st) {
        if (hit) return { step: st, rail: 'skip', val: null };
        if (f && f.at === st) { hit = true; var crash = f.kind === 'bug' && !CATCHES_ALL[c]; return { step: st, rail: crash ? 'crash' : 'err', val: ERR_VAL[c][scen] }; }
        return { step: st, rail: 'ok', val: st === 'parse' && scen === 'bug' ? 'Phone("0987654321")' : OK_VAL[st] };
      });
      var sc = screen(c, scen);
      return { rows: rows, screen: sc, ran: rows.filter(function (r) { return r.rail !== 'skip'; }).length,
        reason: (sc === 'taken' || sc === 'compile') ? 1 : 0, hidden: (f && f.kind === 'bug' && CATCHES_ALL[c]) ? 1 : 0, flagged: sc === 'compile' ? 1 : 0 };
    }
    ADE.fpErrors = { STEPS: STEPS, SCEN: SCEN, SIG: SIG, run: run, screen: screen };
    var HL = { throw: [[2, 6, 8], [4, 9], [5, 9], [4, 9]], nullable: [[1, 5, 7], [3, 8], [4], [3, 8]],
      result: [[1, 5, 8], [3, 9], [1, 4, 9], [3, 9]], typed: [[6, 10, 13], [8, 16], [9], [1, 14]] };
    var STATE = { booked: 'done', taken: 'done', compile: 'done', failed: 'surprise', crash: 'broken' };
    function steps(s) {
      var c = s.case;
      return KS.map(function (k, i) {
        var r = run(c, SCEN[i]), st = STATE[r.screen], bad = st !== 'done', crash = r.screen === 'crash';
        var nodes = i === 0 ? ['input', 'chain', 'screen'] : (crash ? ['chain', 'screen'] : ['chain', 'rail', 'screen']);
        var ns = { screen: K + 'st.' + st }; if (crash) ns.chain = K + 'st.broken';
        var o = S(m, c + '.' + k, { type: i === 0 ? 'scenario' : (bad ? 'pitfall' : 'mechanism'), activeNodes: nodes, nodeStates: ns,
          metrics: { ran: r.ran, reason: r.reason, hidden: r.hidden, flagged: r.flagged },
          codeHighlight: { snippet: 'p5.' + c, lines: HL[c][i] },
          movingSignals: [{ edge: i === 0 ? 'e2' : (crash ? 'e1' : 'e3'), tok: bad ? 'signal' : 'state' }],
          logEvents: [{ t: i, kind: bad ? 'exception' : (i === 0 ? 'run' : (i === 3 ? 'complete' : 'observe')), subject: 'screen' }] });
        var tryIt = i === 0 && c === 'throw';
        o.callouts = [{ kind: tryIt ? 'try' : (bad ? 'pitfall' : 'source'), textKey: tryIt ? M(m, 'co.try') : M(m, 'co.' + c + '.' + k) }];
        return o;
      });
    }
    var LEN = { 'p5.throw': 9, 'p5.nullable': 8, 'p5.result': 9, 'p5.typed': 19 };
    reg(m, { controls: [sel(m, 'case', CASES)], init: function () { return { case: 'throw' }; }, act: setter(['case']), steps: steps,
      simpExtra: [M(m, 'simp.2')],
      selfChecks: [
        { name: 'đường đi đúng: lỗi ở bước nào thì các bước sau bị bỏ qua; đường thành công chạy đủ 4 bước', run: function () {
          return CASES.every(function (c) { var a = run(c, 'ok'), b = run(c, 'taken'), d = run(c, 'bug');
            return a.ran === 4 && b.ran === 2 && b.rows[2].rail === 'skip' && b.rows[3].rail === 'skip' && d.ran === 3 && d.rows[3].rail === 'skip'; }); } },
        { name: 'giờ đã có người đặt: chỉ Result (có kiểm is) và kiểu lỗi riêng cho màn biết lý do; ngoại lệ bắt chung và null thì không', run: function () {
          return run('throw', 'taken').reason === 0 && run('nullable', 'taken').reason === 0 && run('result', 'taken').reason === 1 && run('typed', 'taken').reason === 1; } },
        { name: 'lỗi lập trình: catch (e: Exception) và runCatching giấu nó; nullable và kiểu lỗi riêng để nó lộ ra (crash khi test)', run: function () {
          return run('throw', 'bug').hidden === 1 && run('result', 'bug').hidden === 1 && run('nullable', 'bug').screen === 'crash' && run('typed', 'bug').screen === 'crash' && run('typed', 'bug').rows[2].rail === 'crash'; } },
        { name: 'thêm lỗi ClinicClosed: chỉ kiểu lỗi riêng bị trình biên dịch chỉ ra (1 chỗ when); ba cách kia im lặng hiện "thất bại"', run: function () {
          return run('typed', 'closed').flagged === 1 && ['throw', 'nullable', 'result'].every(function (c) { return run(c, 'closed').flagged === 0 && run(c, 'closed').screen === 'failed'; }); } },
        { name: 'mỗi cách 4 bước; mọi dòng tô sáng nằm trong đoạn mã', run: function () {
          return CASES.every(function (c) { return steps({ case: c }).length === 4 && HL[c].every(function (l) { return l.every(function (x) { return x >= 1 && x <= LEN['p5.' + c]; }); }); }); } }] });
  })();

})();
