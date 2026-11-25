/* Model track L (thuần, không DOM, không câu chữ; chỉ message key). MÔ HÌNH GIẢNG DẠY (simplified).
   Nguồn: docs/research/debugging.md (tài liệu chính thức developer.android.com, đọc từ 2026-11-25). */
(function () {
  'use strict';
  var K = 'track.debugging.';
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
    ADE.registerModel('debugging.' + m, def);
  }
  var sel = function (m, id, vals) { return { id: id, type: 'select', labelKey: M(m, 'ctl.' + id), get: function (s) { return s[id]; }, action: id, options: vals.map(function (v) { return { value: v, labelKey: M(m, 'ctl.' + id + '.' + v) }; }) }; };
  var setter = function (keys) { return function (s, a, v) { var n = {}; keys.forEach(function (k) { n[k] = s[k]; }); if (keys.indexOf(a) >= 0) n[a] = v; return n; }; };

  /* ================= l1: vòng gỡ lỗi: crash "thỉnh thoảng" ở màn chi tiết; đoán rồi sửa, hay tái hiện, thu hẹp, giả thuyết, kiểm =================
     CÀI THẬT: 8 kịch bản thao tác, mỗi cái có làm màn hình bị tạo lại không (xoay, giao diện tối, ngôn ngữ, tiến trình bị đóng rồi mở lại).
     Kết quả của một kịch bản với một bản sửa được TÍNH: không tạo lại → bình thường; tạo lại → crash, trừ khi bản sửa cố định dọc (xoay không còn
     tạo lại), phép kiểm isInitialized (thành màn trống) hay truyền id qua arguments (bình thường). Kịch bản và bản sửa là của site. */
  (function () {
    var m = 'loop', CASES = ['guess', 'method'], KS = ['s1', 's2', 's3', 's4'];
    // [id, làm màn hình bị tạo lại bằng cách nào: null | 'rotate' | 'config' | 'process']
    var SC = [['openBack', null], ['rotate', 'rotate'], ['scroll', null], ['dark', 'config'], ['home', null], ['kill', 'process'], ['lang', 'config'], ['wait', null]];
    function recreated(sc, patch) { return sc[1] !== null && !(sc[1] === 'rotate' && (patch === 'portrait' || patch === 'check')); }
    function outcome(sc, patch) {
      if (!recreated(sc, patch)) return 'ok';
      if (patch === 'args') return 'ok';
      return patch === 'check' ? 'blank' : 'crash';
    }
    var PATCH = { guess: ['portrait', 'check', 'check', 'check'], method: ['none', 'none', 'none', 'args'] };
    var RELEASES = { guess: [1, 2, 2, 3], method: [0, 0, 0, 1] };
    function tally(patch) { var c = 0, b = 0; SC.forEach(function (sc) { var o = outcome(sc, patch); if (o === 'crash') c++; if (o === 'blank') b++; }); return { crash: c, blank: b }; }
    // giả thuyết "crash khi và chỉ khi màn hình bị tạo lại" khớp mọi kịch bản khi chưa sửa
    function hypothesisHolds() { return SC.every(function (sc) { return (outcome(sc, 'none') === 'crash') === (sc[1] !== null); }); }
    ADE.dbgLoop = { SC: SC, outcome: outcome, recreated: recreated, PATCH: PATCH, tally: tally };
    var NODES = { guess: [[[], 'lock'], [[], 'lock'], [[], 'lock'], [[], 'lock']],
      method: [[['repro'], 'repro'], [['repro', 'narrow'], 'narrow'], [['hypo', 'check'], 'check'], [['check', 'lock'], 'lock']] };
    var EDGE = { method: ['e1', 'e1', 'e3', 'e5'] };
    var CODE = { guess: ['l1.guess', 'l1.guess', 'l1.guess', 'l1.guess'], method: ['l1.bug', 'l1.bug', 'l1.bug', 'l1.fix'] };
    var HL = { guess: [[1, 2], [7], [7], [2, 7]], method: [[5], [5], [3], [2, 5, 9]] };
    function steps(s) {
      var c = s.case;
      return KS.map(function (k, i) {
        var p = PATCH[c][i], t = tally(p), bad = c === 'guess', nd = NODES[c][i], ns = {};
        ns[nd[1]] = K + 'st.' + (bad ? 'surprise' : 'done');
        var o = S(m, c + '.' + k, { type: i === 0 ? 'scenario' : (bad ? 'pitfall' : 'mechanism'), activeNodes: nd[0], nodeStates: ns,
          params: { patch: p },
          metrics: { crash: t.crash, blank: t.blank, releases: RELEASES[c][i], known: M(m, c === 'method' && i >= 2 ? 'known.yes' : 'known.no') },
          codeHighlight: { snippet: CODE[c][i], lines: HL[c][i] },
          movingSignals: bad ? [] : [{ edge: EDGE.method[i], tok: 'state' }],
          logEvents: [{ t: i, kind: bad ? (t.crash ? 'exception' : 'skip') : (i === 3 ? 'complete' : (i === 0 ? 'observe' : 'run')), subject: nd[1] }] });
        var tryIt = i === 0 && c === 'guess';
        o.callouts = [{ kind: tryIt ? 'try' : (bad ? 'pitfall' : (i === 3 ? 'mechanism' : 'source')), textKey: tryIt ? M(m, 'co.try') : M(m, 'co.' + c + '.' + k) }];
        return o;
      });
    }
    var LEN = { 'l1.guess': 10, 'l1.bug': 7, 'l1.fix': 10 };
    reg(m, { controls: [sel(m, 'case', CASES)], init: function () { return { case: 'guess' }; }, act: setter(['case']), steps: steps,
      simpExtra: [M(m, 'simp.2')],
      selfChecks: [
        { name: 'chưa sửa: 4 trên 8 kịch bản crash (2, 4, 6, 7), không màn trống', run: function () { var t = tally('none'); return t.crash === 4 && t.blank === 0 && SC.length === 8 &&
          SC.map(function (sc, i) { return outcome(sc, 'none') === 'crash' ? i + 1 : 0; }).filter(Boolean).join() === '2,4,6,7'; } },
        { name: 'cố định dọc: còn 3 crash; thêm phép kiểm: 0 crash nhưng 3 màn trống; truyền id qua arguments: 0 và 0', run: function () {
          var a = tally('portrait'), b = tally('check'), c = tally('args'); return a.crash === 3 && a.blank === 0 && b.crash === 0 && b.blank === 3 && c.crash === 0 && c.blank === 0; } },
        { name: 'giả thuyết "crash khi và chỉ khi màn hình bị tạo lại" khớp cả 8 kịch bản', run: hypothesisHolds },
        { name: 'mỗi cách 4 bước; cách đoán tốn 3 bản phát hành, cách có phương pháp 1; mọi dòng tô sáng nằm trong đoạn mã', run: function () {
          return CASES.every(function (c) { return steps({ case: c }).length === 4 && HL[c].every(function (l, i) { return l.every(function (x) { return x >= 1 && x <= LEN[CODE[c][i]]; }); }); }) &&
            RELEASES.guess[3] === 3 && RELEASES.method[3] === 1; } }] });
  })();

  /* ================= l2: debugger: breakpoint thường, có điều kiện, chính sách All hay Thread, breakpoint chỉ ghi log =================
     Theo JetBrains IntelliJ IDEA 2026.3 Help (Breakpoints; Examine suspended program). CÀI THẬT: 500 lịch, phí = base × (100 − giảm giá) / 100;
     chỉ đơn 347 có giảm giá 120 % nên phí âm. Số lần dừng, bấm chạy tiếp, dòng log được đếm từ vòng lặp; luồng đồng bộ gửi nhịp mỗi giây,
     khoảng không nhịp dài nhất được tính từ thời gian dừng (mỗi lần dừng ngắn 1 giây, bước "xem biến" 30 giây); quá 10 giây là mất phiên.
     Danh sách lịch, mức giảm giá và hạn 10 giây là của site. */
  (function () {
    var m = 'bp', CASES = ['plain', 'cond', 'thread', 'logbp'], KS = ['s1', 's2', 's3'];
    var N = 500, BAD = 347, BASE = 200000, TIMEOUT = 10, LOOK = 30;
    var disc = function (i) { return i === BAD ? 120 : (i * 7) % 31; };
    var fee = function (i) { return BASE * (100 - disc(i)) / 100; };
    var negatives = function () { var r = []; for (var i = 0; i < N; i++) if (fee(i) < 0) r.push(i); return r; };
    // chạy vòng lặp tới bước k (0..2) với một kiểu breakpoint: chỉ số đang đứng, các lần dừng, số lần bấm chạy tiếp, số dòng log, khoảng không nhịp dài nhất
    function run(c, k) {
      var stops = [], logs = 0, at = 0, gap = 0, cond = c === 'cond' || c === 'thread', all = c !== 'thread';
      if (c === 'logbp') { logs = N; at = N - 1; }
      else if (c === 'plain') { var to = k === 0 ? 0 : BAD; for (var i = 0; i <= to; i++) stops.push(i); at = to; }
      else if (cond) { if (k === 0) at = BAD - 1; else { for (var j = 0; j < N; j++) if (fee(j) < 0) { stops.push(j); break; } at = BAD; } }
      if (c !== 'logbp' && all && stops.length) gap = k === 2 ? LOOK : 1;
      return { at: at, stops: stops.length, resumes: Math.max(0, stops.length - 1), logs: logs, filtered: c === 'logbp' && k >= 1 ? negatives().length : 0, gap: gap, expired: gap > TIMEOUT };
    }
    ADE.dbgBp = { N: N, BAD: BAD, BASE: BASE, disc: disc, fee: fee, run: run, TIMEOUT: TIMEOUT };
    var NODES = [[['report', 'bp'], 'bp', 'e1'], [['bp', 'vars'], 'vars', 'e2'], [['sync', 'server'], 'server', 'e4']];
    var HL = { plain: [[5], [5], [5]], cond: [[4, 5], [4, 5], [5]], thread: [[4, 5], [4, 5], [5]], logbp: [[5], [4, 5], [4]] };
    function steps(s) {
      var c = s.case;
      return KS.map(function (k, i) {
        var r = run(c, i), bad = (c === 'plain' && i >= 1) || r.expired, nd = NODES[i], ns = {};
        ns[nd[1]] = K + 'st.' + (bad ? 'surprise' : 'done');
        var o = S(m, c + '.' + k, { type: i === 0 ? 'scenario' : (bad ? 'pitfall' : 'mechanism'), activeNodes: nd[0], nodeStates: ns,
          metrics: { stops: r.stops, resumes: r.resumes, logs: r.logs, sync: M(m, i < 2 && c !== 'thread' && c !== 'logbp' ? 'sync.na' : (r.expired ? 'sync.expired' : 'sync.alive')) },
          codeHighlight: { snippet: 'l2.loop', lines: HL[c][i] },
          movingSignals: [{ edge: nd[2], tok: bad ? 'signal' : 'state' }],
          logEvents: [{ t: i, kind: bad ? 'exception' : (i === 2 ? 'complete' : (i === 0 ? 'observe' : 'run')), subject: nd[1] }] });
        var tryIt = i === 0 && c === 'plain';
        o.callouts = [{ kind: tryIt ? 'try' : (bad ? 'pitfall' : 'source'), textKey: tryIt ? M(m, 'co.try') : M(m, 'co.' + c + '.' + k) }];
        return o;
      });
    }
    reg(m, { controls: [sel(m, 'case', CASES)], init: function () { return { case: 'plain' }; }, act: setter(['case']), steps: steps,
      simpExtra: [M(m, 'simp.2')],
      selfChecks: [
        { name: 'trong 500 lịch chỉ đơn 347 có phí âm: 200.000 × (100 − 120) / 100 = −40.000', run: function () { var n = negatives(); return n.length === 1 && n[0] === 347 && fee(347) === -40000 && fee(0) === 200000; } },
        { name: 'breakpoint thường: 348 lần dừng, 347 lần bấm chạy tiếp; có điều kiện fee < 0: đúng 1 lần dừng, ở đơn 347', run: function () {
          var a = run('plain', 1), b = run('cond', 1); return a.stops === 348 && a.resumes === 347 && b.stops === 1 && b.at === 347 && b.resumes === 0; } },
        { name: 'xem biến 30 giây: dừng mọi luồng thì luồng đồng bộ lỡ 30 nhịp > 10, mất phiên; chỉ dừng một luồng thì 0 nhịp, còn phiên', run: function () {
          return run('plain', 2).expired && run('cond', 2).expired && !run('thread', 2).expired && run('thread', 2).gap === 0 && !run('plain', 1).expired; } },
        { name: 'breakpoint chỉ ghi log: 0 lần dừng, 500 dòng log, lọc phí âm còn 1 dòng; mỗi kiểu 3 bước, dòng tô sáng trong đoạn mã', run: function () {
          var r = run('logbp', 1); return r.stops === 0 && r.logs === 500 && r.filtered === 1 &&
            CASES.every(function (c) { return steps({ case: c }).length === 3 && HL[c].every(function (l) { return l.every(function (x) { return x >= 1 && x <= 8; }); }); }); } }] });
  })();

  /* ================= l3: Logcat: lọc dần để tìm dòng lỗi; log còn lại trong bản release =================
     Theo developer.android.com/studio/debug/logcat (truy vấn key:value: cùng key OR, khác key AND, level: là mức đó trở lên, package:mine),
     tools/logcat, reference Log, privacy-and-security/risks/log-info-disclosure (R8 -assumenosideeffects xóa v, d, i; giữ w, e).
     CÀI THẬT: 16 dòng log (của site); mỗi bước là một truy vấn có cấu trúc, áp thật lên 16 dòng; bản release bỏ mọi dòng V, D, I của app. */
  (function () {
    var m = 'logcat', CASES = ['find', 'release'], KS = ['s1', 's2', 's3', 's4'];
    var LV = { V: 2, D: 3, I: 4, W: 5, E: 6, A: 7 };
    var APP = 'vn.henkham';
    // [pid, mức, tag, package, nội dung, có số điện thoại]
    var LOGS = [
      [589, 'I', 'ActivityManager', 'system_server', 'Start proc 4120:vn.henkham', 0],
      [4120, 'D', 'BookingRepo', APP, 'load bookings page=1', 0],
      [1022, 'D', 'SystemUI', 'com.android.systemui', 'status bar updated', 0],
      [2211, 'I', 'GmsCore', 'com.google.android.gms', 'heartbeat ok', 0],
      [4120, 'I', 'Sync', APP, 'sync started', 0],
      [4120, 'D', 'BookingRepo', APP, 'saving booking for phone=0912345678', 1],
      [589, 'W', 'ActivityManager', 'system_server', 'slow operation: 120ms', 0],
      [4120, 'V', 'ListAdapter', APP, 'bind row 3', 0],
      [2211, 'D', 'GmsCore', 'com.google.android.gms', 'token refresh', 0],
      [4120, 'W', 'Sync', APP, 'retry 1 for phone=0912345678', 1],
      [1022, 'I', 'SystemUI', 'com.android.systemui', 'clock tick', 0],
      [4120, 'D', 'Sync', APP, 'server responded 409', 0],
      [4120, 'E', 'BookingRepo', APP, 'save failed: SQLiteConstraintException', 0],
      [589, 'I', 'ActivityManager', 'system_server', 'Displayed vn.henkham/.MainActivity', 0],
      [2211, 'W', 'GmsCore', 'com.google.android.gms', 'location timeout', 0],
      [4120, 'I', 'Sync', APP, 'sync finished: 1 failed', 0]];
    var ERR = 12, FIXED = 'retry 1 for booking id=42';
    // truy vấn có cấu trúc: { package: [...], level: 'W', tag: [...] }; cùng key OR (mảng), khác key AND
    function match(row, q) {
      if (q.package && q.package.indexOf(row[3]) < 0) return false;
      if (q.level && LV[row[1]] < LV[q.level]) return false;
      if (q.tag && q.tag.indexOf(row[2]) < 0) return false;
      return true;
    }
    var Q = { find: [{}, { package: [APP] }, { package: [APP], level: 'W' }, { package: [APP], tag: ['BookingRepo', 'Sync'] }],
      release: [{ package: [APP] }, { package: [APP] }, { package: [APP] }, { package: [APP] }] };
    var BUILD = { find: ['debug', 'debug', 'debug', 'debug'], release: ['debug', 'release', 'release', 'release'] };
    var stripped = function (row, build) { return build === 'release' && row[3] === APP && LV[row[1]] <= LV.I; };
    function view(c, i) {
      var q = Q[c][i], b = BUILD[c][i], fixed = c === 'release' && i === 3;
      var rows = LOGS.map(function (r, k) {
        var gone = stripped(r, b), shown = !gone && match(r, q), pii = shown && r[5] === 1 && !fixed;
        return { k: k, row: r, shown: shown, gone: gone, pii: pii, msg: fixed && r[5] && r[1] === 'W' ? FIXED : r[4] };
      });
      var shown = rows.filter(function (x) { return x.shown; });
      return { q: q, build: b, rows: rows, shown: shown.length, app: shown.filter(function (x) { return x.row[3] === APP; }).length,
        pii: rows.filter(function (x) { return x.pii; }).length, found: shown.some(function (x) { return x.k === ERR; }) && shown.length <= 8 };
    }
    // chuỗi truy vấn hiển thị (giữ nguyên cú pháp Logcat, không dịch)
    function qtext(q) {
      var p = [];
      if (q.package) p.push('package:mine');
      if (q.level) p.push('level:' + { W: 'WARN', E: 'ERROR', I: 'INFO' }[q.level]);
      (q.tag || []).forEach(function (t) { p.push('tag:' + t); });
      return p.join(' ');
    }
    ADE.dbgLogcat = { view: view, qtext: qtext, LOGS: LOGS };
    var NODES = { find: [[['others', 'logd', 'view'], 'view', 'e3'], [['app', 'view'], 'view', 'e4'], [['view'], 'view', 'e4'], [['app', 'view'], 'view', 'e4']],
      release: [[['app', 'logd'], 'logd', 'e2'], [['app', 'r8'], 'r8', 'e1'], [['logd', 'view'], 'view', 'e4'], [['app', 'view'], 'view', 'e4']] };
    var HL = { find: [[5], [3, 5], [5, 8], [3, 5, 8]], release: [[3, 8], [3], [8], [9]] };
    function steps(s) {
      var c = s.case;
      return KS.map(function (k, i) {
        var v = view(c, i), bad = (c === 'find' && i === 0) || (c === 'release' && (i === 0 || i === 2)), nd = NODES[c][i], ns = {};
        ns[nd[1]] = K + 'st.' + (bad ? 'surprise' : 'done');
        var o = S(m, c + '.' + k, { type: i === 0 ? 'scenario' : (bad ? 'pitfall' : 'mechanism'), activeNodes: nd[0], nodeStates: ns,
          metrics: { shown: v.shown, app: v.app, pii: v.pii, found: M(m, v.found ? 'found.yes' : 'found.no') },
          codeHighlight: { snippet: 'l3.log', lines: HL[c][i] },
          movingSignals: [{ edge: nd[2], tok: bad ? 'signal' : 'state' }],
          logEvents: [{ t: i, kind: bad ? 'exception' : (i === 3 ? 'complete' : (i === 0 ? 'observe' : 'run')), subject: nd[1] }] });
        var tryIt = i === 0 && c === 'find';
        o.callouts = [{ kind: tryIt ? 'try' : (bad ? 'pitfall' : 'source'), textKey: tryIt ? M(m, 'co.try') : M(m, 'co.' + c + '.' + k) }];
        return o;
      });
    }
    reg(m, { controls: [sel(m, 'case', CASES)], init: function () { return { case: 'find' }; }, act: setter(['case']), steps: steps,
      simpExtra: [M(m, 'simp.2')],
      selfChecks: [
        { name: 'không lọc 16 dòng; package:mine còn 8; thêm level:WARN còn 2 và có dòng lỗi', run: function () {
          var a = view('find', 0), b = view('find', 1), c = view('find', 2); return a.shown === 16 && b.shown === 8 && c.shown === 2 && c.found && !a.found; } },
        { name: 'tag:BookingRepo tag:Sync (cùng key nên OR) cùng package:mine còn 7 dòng', run: function () { return view('find', 3).shown === 7; } },
        { name: 'bản debug: 2 dòng lộ số điện thoại; release xóa V, D, I còn 2 dòng của app, vẫn 1 dòng lộ (Log.w); log id thì 0', run: function () {
          return view('release', 0).pii === 2 && view('release', 1).shown === 2 && view('release', 2).pii === 1 && view('release', 3).pii === 0; } },
        { name: 'mỗi cách 4 bước; dòng tô sáng nằm trong đoạn mã 9 dòng', run: function () {
          return CASES.every(function (c) { return steps({ case: c }).length === 4 && HL[c].every(function (l) { return l.every(function (x) { return x >= 1 && x <= 9; }); }); }); } }] });
  })();
})();
