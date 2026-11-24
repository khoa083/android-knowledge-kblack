/* Model track I (thuần, không DOM, không câu chữ; chỉ message key). MÔ HÌNH GIẢNG DẠY (simplified).
   Nguồn: docs/research/sysdesign.md (tài liệu chính thức và sách system design, đọc từ 2026-11-24). */
(function () {
  'use strict';
  var K = 'track.sysdesign.';
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
    ADE.registerModel('sysdesign.' + m, def);
  }
  var sel = function (m, id, vals) { return { id: id, type: 'select', labelKey: M(m, 'ctl.' + id), get: function (s) { return s[id]; }, action: id, options: vals.map(function (v) { return { value: v, labelKey: M(m, 'ctl.' + id + '.' + v) }; }) }; };
  var setter = function (keys) { return function (s, a, v) { var n = {}; keys.forEach(function (k) { n[k] = s[k]; }); if (keys.indexOf(a) >= 0) n[a] = v; return n; }; };
  var nsOf = function (o) { var n = {}; Object.keys(o).forEach(function (k) { n[k] = K + 'st.' + o[k]; }); return n; };


  /* ================= I1: từ đề bài tới kế hoạch — làm theo bản thiết kế so với hỏi trước rồi mới làm =================
     Theo Tjeerd in 't Veen, Mobile System Design ch.2 (tìm yêu cầu phụ trước khi mở IDE; xin bản thiết kế với nội dung xấu nhất;
     bàn về lỗi sớm, ưu tiên lỗi không chặn màn hình; thống nhất với backend về phiên, token, timeout, mã lỗi, thông báo đẩy theo
     ngôn ngữ) và Alex Xu, System Design Interview tập 1 ch.2–3 (ước lượng nhanh bằng số tròn, ghi giả định và đơn vị; khung bốn
     bước, hỏi trước khi trả lời). Câu hỏi về mất mạng và trạng thái rỗng là bổ sung của site. Mọi con số là giả định minh họa. */
  (function () {
    var m = 'plan', CASES = ['mockup', 'asked'], KS = ['s1', 's2', 's3', 's4'];
    var Q = [['d1', 'designer'], ['d2', 'designer'], ['d3', 'designer'], ['b1', 'backend'], ['b2', 'backend'], ['b3', 'backend']];
    // trạng thái từng câu hỏi sau mỗi bước: '' chưa | 'asked' đã hỏi, có yêu cầu | 'late' lộ ra sau khi phát hành
    function qState(c, i, q) {
      if (c === 'asked') { if (q[1] === 'designer') return i >= 1 ? 'asked' : ''; return i >= 2 ? 'asked' : ''; }
      return i >= 3 ? 'late' : '';
    }
    // ước lượng dữ liệu di động: [ảnh mỗi ngày, KB mỗi ảnh] → MB mỗi tháng (30 ngày, làm tròn)
    var EST = { mockup: { photos: 2, kb: 4000 }, asked: { photos: 2, kb: 300 } };
    function mbMonth(c) { return Math.round(EST[c].photos * 30 * EST[c].kb / 1000); }
    ADE.sysPlan = { Q: Q, qState: qState, EST: EST, mbMonth: mbMonth };
    var TYPE = { mockup: ['scenario', 'mechanism', 'mechanism', 'pitfall'], asked: ['scenario', 'mechanism', 'mechanism', 'mechanism'] };
    var NODES = [['brief'], ['brief', 'designer'], ['brief', 'backend'], ['plan']];
    function steps(s) {
      return KS.map(function (k, i) {
        var type = TYPE[s.case][i], bad = type === 'pitfall';
        var asked = Q.filter(function (q) { return qState(s.case, i, q) === 'asked'; }).length, late = Q.filter(function (q) { return qState(s.case, i, q) === 'late'; }).length;
        var nodes = s.case === 'mockup' && (i === 1 || i === 2) ? ['brief', 'plan'] : NODES[i];
        var ns = {}; nodes.forEach(function (n) { ns[n] = K + 'st.' + (bad ? 'surprise' : 'done'); });
        if (s.case === 'mockup' && i >= 1) { ns.designer = K + 'st.skipped'; ns.backend = K + 'st.skipped'; }
        var o = S(m, s.case + '.' + k, { type: type, activeNodes: nodes, nodeStates: ns,
          metrics: { asked: asked, late: late, data: i === 3 ? mbMonth(s.case) : 0 },
          movingSignals: [], logEvents: [{ t: i, kind: bad ? 'exception' : (i === 3 ? 'complete' : 'observe'), subject: nodes[nodes.length - 1] }] });
        o.callouts = [{ kind: i === 0 ? 'try' : (bad ? 'pitfall' : 'source'), textKey: i === 0 ? M(m, 'co.try') : M(m, 'co.' + s.case + '.' + k) }];
        return o;
      });
    }
    reg(m, { controls: [sel(m, 'case', CASES)], init: function () { return { case: 'mockup' }; }, act: setter(['case']), steps: steps,
      simpExtra: [M(m, 'simp.2')],
      selfChecks: [
        { name: 'hỏi trước: mọi câu hỏi có yêu cầu trước khi viết mã; làm theo bản thiết kế: mọi câu lộ ra sau khi phát hành', run: function () { return Q.every(function (q) { return qState('asked', 2, q) === 'asked' && qState('mockup', 3, q) === 'late'; }); } },
        { name: 'ước lượng: thu nhỏ ảnh trước khi gửi làm dữ liệu mỗi tháng giảm hơn 10 lần', run: function () { return mbMonth('mockup') > 10 * mbMonth('asked'); } },
        { name: 'mỗi cách có 4 bước', run: function () { return CASES.every(function (c) { return steps({ case: c }).length === 4; }); } }] });
  })();

  /* ================= I2: tiến trình, bộ nhớ và cái chết của process — form trong ViewModel so với saved state =================
     Theo developer.android.com: Processes and app lifecycle (bậc foreground, visible, service, cached; giết cached trước),
     Activity lifecycle (hệ thống giết process, không giết Activity), Save UI states (ViewModel mất khi process bị giết; saved state
     lưu lúc onStop, bản sao ngoài process), Get a result from an activity (camera: process gần như chắc chắn bị hủy),
     ComponentCallbacks2 (từ API 34 chỉ còn UI_HIDDEN, BACKGROUND); source.android.com lmkd. Số MB là minh họa (RAM 4 GB). */
  (function () {
    var m = 'process', CASES = ['vm', 'saved'], KS = ['s1', 's2', 's3', 's4'];
    // bậc của app và Camera ở mỗi bước ('' = không có process)
    var LV = { app: ['fg', 'cached', 'gone', 'fg'], cam: ['', 'fg', 'fg', 'cached'] };
    // RAM (MB): hệ thống, Camera, app khác ở nền, Hẹn Khám, trống — tổng 4000
    var MEM = [[1500, 0, 1400, 300, 800], [1500, 900, 1000, 300, 300], [1500, 1500, 600, 0, 400], [1500, 1500, 600, 300, 100]];
    // còn lại gì: [hàng, đang giữ, trạng thái] theo cách và bước
    var SURV = {
      vm: [[['vm', 'form', 'live'], ['saved', 'none', 'na'], ['disk', 'photo', 'nofile']],
           [['vm', 'form', 'live'], ['saved', 'none', 'na'], ['disk', 'photo', 'writing']],
           [['vm', 'form', 'lost'], ['saved', 'none', 'na'], ['disk', 'photo', 'kept']],
           [['vm', 'form', 'empty'], ['saved', 'none', 'na'], ['disk', 'photo', 'orphan']]],
      saved: [[['vm', 'form', 'live'], ['saved', 'ids', 'live'], ['disk', 'photo', 'nofile']],
              [['vm', 'form', 'live'], ['saved', 'ids', 'copied'], ['disk', 'photo', 'writing']],
              [['vm', 'form', 'lost'], ['saved', 'ids', 'kept'], ['disk', 'photo', 'pending']],
              [['vm', 'form', 'refilled'], ['saved', 'ids', 'restored'], ['disk', 'photo', 'attached']]]
    };
    var BAD = { lost: 1, empty: 1, orphan: 1 };
    function fields(c, i) { if (i === 3) return c === 'vm' ? 0 : 3; return i === 2 ? (c === 'vm' ? 0 : 2) : 2; }
    ADE.sysProcess = { LV: LV, MEM: MEM, SURV: SURV, BAD: BAD };
    var LINES = { vm: [[2, 3], [6, 7], [8], [4, 9]], saved: [[2, 3], [4, 6], [7], [8, 9]] };
    var NODES = [['app'], ['app', 'camera'], ['lmkd', 'app'], ['app', 'store']];
    var EDGE = ['', 'e1', 'e3', 'e4'];
    function steps(s) {
      return KS.map(function (k, i) {
        var bad = s.case === 'vm' && i === 3, type = i === 0 ? 'scenario' : (bad ? 'pitfall' : 'mechanism');
        var ns = { app: K + 'st.' + (i === 2 ? 'broken' : (bad ? 'surprise' : 'done')) };
        if (i >= 1) ns.camera = K + 'st.done';
        if (i >= 2) ns.lmkd = K + 'st.done';
        ns.store = K + 'st.' + (s.case === 'vm' ? 'skipped' : 'done');
        var o = S(m, s.case + '.' + k, { type: type, activeNodes: NODES[i], nodeStates: ns,
          metrics: { fields: fields(s.case, i), free: MEM[i][4], starts: i === 3 ? 2 : 1 },
          codeHighlight: { snippet: 'i2.' + s.case, lines: LINES[s.case][i] },
          movingSignals: EDGE[i] ? [{ edge: EDGE[i], tok: i === 2 || bad ? 'signal' : 'state' }] : [],
          logEvents: [{ t: i, kind: i === 2 ? 'exception' : (bad ? 'exception' : (i === 3 ? 'complete' : (i === 0 ? 'write' : 'observe'))), subject: NODES[i][0] }] });
        o.callouts = [{ kind: i === 0 ? 'try' : (bad ? 'pitfall' : 'source'), textKey: i === 0 ? M(m, 'co.try') : M(m, 'co.' + s.case + '.' + k) }];
        return o;
      });
    }
    reg(m, { controls: [sel(m, 'case', CASES)], init: function () { return { case: 'vm' }; }, act: setter(['case']), steps: steps,
      simpExtra: [M(m, 'simp.2')],
      selfChecks: [
        { name: 'RAM mỗi bước cộng lại đúng 4000 MB', run: function () { return MEM.every(function (r) { return r.reduce(function (x, y) { return x + y; }, 0) === 4000; }); } },
        { name: 'process bị giết ở bước 3: không còn RAM của app, ViewModel mất ở cả hai cách', run: function () { return MEM[2][3] === 0 && LV.app[2] === 'gone' && CASES.every(function (c) { return SURV[c][2][0][2] === 'lost'; }); } },
        { name: 'quay lại: chỉ ViewModel thì form rỗng và ảnh mồ côi; saved state thì đủ 3 ô', run: function () { return fields('vm', 3) === 0 && SURV.vm[3][2][2] === 'orphan' && fields('saved', 3) === 3 && SURV.saved[3][1][2] === 'restored'; } },
        { name: 'mỗi cách có 4 bước, dòng mã nằm trong đoạn mã', run: function () { return CASES.every(function (c) { return steps({ case: c }).length === 4 && LINES[c].every(function (l) { return l.every(function (n) { return n >= 1 && n <= (c === 'vm' ? 9 : 10); }); }); }); } }] });
  })();

  /* ================= I3: luồng, khóa, ANR và deadlock — giữ khóa lâu, hai khóa ngược thứ tự, một thứ tự chung =================
     Theo developer.android.com ANRs (sự kiện nhập 5 giây; main thread chờ khóa; deadlock; Mutex.withLock), Processes and threads
     overview (đừng chặn UI thread); kotlinx.coroutines Mutex; OS Concepts bản 10 ch.8 (bốn điều kiện, đồ thị chờ, thứ tự khóa).
     Mốc thời gian là minh họa: chạm ở giây 1, ANR ở giây 6. */
  (function () {
    var m = 'lock', CASES = ['hold', 'cycle', 'order'], KS = ['s1', 's2', 's3', 's4'];
    // làn thời gian: [bắt đầu, kết thúc (giây), loại, nhãn]
    var LANES = {
      hold: { main: [[1, 7, 'wait', 'waitC'], [7, 8, 'run', 'draw']], sync: [[0, 7, 'hold', 'holdC']] },
      cycle: { main: [[1, 2, 'run', 'ui'], [2, 3, 'hold', 'holdC2'], [3, 8, 'wait', 'waitD']], sync: [[0, 3, 'hold', 'holdD'], [3, 8, 'wait', 'waitC']] },
      order: { main: [[1.1, 1.3, 'wait', ''], [1.3, 1.4, 'hold', ''], [1.4, 2, 'run', 'draw']], sync: [[1, 1.3, 'hold', 'copy'], [1.3, 7, 'run', 'write']] }
    };
    var TS = { hold: [1, 3, 6, 8], cycle: [1, 2, 3, 8], order: [1.1, 1.3, 2, 8] };
    var ANR = { hold: 6, cycle: 6, order: null };
    var WF = { hold: [[], [['main', 'sync', 'cacheLock']], [['main', 'sync', 'cacheLock']], []],
      cycle: [[], [], [['main', 'sync', 'dbLock'], ['sync', 'main', 'cacheLock']], [['main', 'sync', 'dbLock'], ['sync', 'main', 'cacheLock']]],
      order: [[], [['main', 'sync', 'cacheLock']], [], []] };
    function blocked(c, i) { var t = TS[c][i]; return Math.round(LANES[c].main.reduce(function (acc, g) { return g[2] === 'wait' && g[0] < t ? acc + Math.min(g[1], t) - g[0] : acc; }, 0) * 1000); }
    function anr(c, i) { return ANR[c] !== null && TS[c][i] >= ANR[c] ? 1 : 0; }
    function cyc(c, i) { var e = WF[c][i]; return e.some(function (a) { return e.some(function (b) { return a[0] === b[1] && a[1] === b[0]; }); }) ? 1 : 0; }
    // bốn điều kiện tại bước: loại trừ, giữ và chờ, không tước, chờ vòng
    function conds(c, i) { var w = cyc(c, i) === 1; return { me: true, hw: c === 'cycle' && i >= 2, np: true, cw: w }; }
    ADE.sysLock = { LANES: LANES, TS: TS, ANR: ANR, WF: WF, blocked: blocked, conds: conds };
    var LINES = { hold: [[2, 3], [6], [6], [4, 7]], cycle: [[2], [6], [3, 7], [3, 7]], order: [[1, 2], [5], [3, 6], [7]] };
    var NODES = { hold: [['sync', 'cache'], ['main', 'cache'], ['main'], ['main', 'sync']], cycle: [['sync', 'db'], ['main', 'cache'], ['main', 'sync', 'cache', 'db'], ['main', 'sync']], order: [['sync', 'cache', 'db'], ['main', 'cache'], ['main', 'sync'], ['sync', 'db']] };
    var EDGE = { hold: ['e3', 'e1', 'e1', 'e1'], cycle: ['e4', 'e1', 'e2', 'e2'], order: ['e3', 'e1', 'e1', 'e4'] };
    function steps(s) {
      var c = s.case;
      return KS.map(function (k, i) {
        var bad = anr(c, i) === 1 || cyc(c, i) === 1, type = i === 0 ? 'scenario' : (bad ? 'pitfall' : 'mechanism');
        var ns = {}; NODES[c][i].forEach(function (n) { ns[n] = K + 'st.' + (bad && (n === 'main' || n === 'sync') ? 'surprise' : 'done'); });
        var o = S(m, c + '.' + k, { type: type, activeNodes: NODES[c][i], nodeStates: ns,
          metrics: { blocked: blocked(c, i), anr: anr(c, i), cycle: cyc(c, i) },
          codeHighlight: { snippet: 'i3.' + c, lines: LINES[c][i] },
          movingSignals: [{ edge: EDGE[c][i], tok: bad ? 'signal' : 'state' }],
          logEvents: [{ t: i, kind: bad ? 'exception' : (i === 3 ? 'complete' : 'run'), subject: NODES[c][i][0] }] });
        o.callouts = [{ kind: i === 0 ? 'try' : (bad ? 'pitfall' : 'source'), textKey: i === 0 ? M(m, 'co.try') : M(m, 'co.' + c + '.' + k) }];
        return o;
      });
    }
    reg(m, { controls: [sel(m, 'case', CASES)], init: function () { return { case: 'hold' }; }, act: setter(['case']), steps: steps,
      simpExtra: [M(m, 'simp.2')],
      selfChecks: [
        { name: 'giữ khóa lâu: ANR nhưng không có vòng chờ; main bị chặn 6 giây', run: function () { return anr('hold', 3) === 1 && [0, 1, 2, 3].every(function (i) { return cyc('hold', i) === 0; }) && blocked('hold', 3) === 6000; } },
        { name: 'ngược thứ tự: vòng chờ từ bước 3, đủ bốn điều kiện, rồi ANR', run: function () { var k = conds('cycle', 2); return cyc('cycle', 2) === 1 && k.me && k.hw && k.np && k.cw && anr('cycle', 3) === 1; } },
        { name: 'một thứ tự chung: không vòng, không ANR, main chờ dưới 1 giây', run: function () { return [0, 1, 2, 3].every(function (i) { return cyc('order', i) === 0 && anr('order', i) === 0 && blocked('order', i) < 1000; }); } },
        { name: 'mỗi cách 4 bước; dòng mã nằm trong đoạn mã', run: function () { var n = { hold: 8, cycle: 8, order: 7 }; return CASES.every(function (c) { return steps({ case: c }).length === 4 && LINES[c].every(function (l) { return l.every(function (x) { return x >= 1 && x <= n[c]; }); }); }); } }] });
  })();

  /* ================= I4: chọn kênh giao tiếp — polling, long polling, WebSocket, FCM cho cùng một tin =================
     Theo Alex Xu tập 1 ch.12; developer.android.com (Optimize network access: radio ~18 giây sau mỗi lần truyền; Doze tạm dừng mạng);
     Firebase (FCM overview, priority, collapsible); MDN (SSE, WebSocket). Tin tới server ở giây 7; chu kỳ 5 giây, hạn chờ 30 giây là minh họa. */
  (function () {
    var m = 'channel', CASES = ['poll', 'long', 'ws', 'push'], KS = ['s1', 's2', 's3', 's4'];
    var PARTS = { poll: ['app', 'server'], long: ['app', 'server'], ws: ['app', 'server'], push: ['app', 'fcm', 'server'] };
    // tin mỗi bước: [từ, tới, nhãn, 1 nếu phí hay không tới]
    var MSGS = {
      poll: [[['app', 'server', 'q0', 0], ['server', 'app', 'none', 1]], [['app', 'server', 'q5', 0], ['server', 'app', 'none', 1]],
             [['server', 'server', 'arrive', 0], ['app', 'server', 'q10', 0], ['server', 'app', 'one', 0]], [['app', 'server', 'more', 0], ['server', 'app', 'none4', 1]]],
      long: [[['app', 'server', 'lq0', 0]], [['server', 'server', 'hold', 0]], [['server', 'server', 'arrive', 0], ['server', 'app', 'lone', 0], ['app', 'server', 'lq7', 0]], [['server', 'app', 'ltimeout', 1], ['app', 'server', 'lq37', 0]]],
      ws: [[['app', 'server', 'up', 0], ['server', 'app', 'ok', 0]], [['app', 'server', 'send', 0]], [['server', 'server', 'arrive', 0], ['server', 'app', 'wpush', 0]], [['app', 'app', 'doze', 1], ['server', 'app', 'lost', 1]]],
      push: [[['app', 'fcm', 'token', 0], ['app', 'server', 'reg', 0]], [['app', 'app', 'idle', 0]], [['server', 'server', 'arrive', 0], ['server', 'fcm', 'fsend', 0], ['fcm', 'app', 'fdeliver', 0]], [['app', 'app', 'notify', 0], ['app', 'server', 'fetch', 0]]]
    };
    var REQS = { poll: [1, 2, 3, 7], long: [1, 1, 2, 3], ws: [1, 1, 1, 1], push: [1, 1, 1, 2] };
    var LAT = { poll: 3, long: 0, ws: 0, push: 0 };
    var BG = { poll: 0, long: 0, ws: 0, push: 1 };
    ADE.sysChannel = { PARTS: PARTS, MSGS: MSGS, ROWS: ['poll', 'long', 'sse', 'ws', 'push'] };
    var LINES = { poll: [[2], [4], [2, 3], [1, 4]], long: [[2], [2], [3], [2]], ws: [[1], [5], [2], [3, 6]], push: [[1], [2], [3, 4], [5]] };
    var NODES = { poll: ['app', 'server'], long: ['app', 'server'], ws: ['app', 'server'], push: ['app', 'fcm', 'server'] };
    function steps(s) {
      var c = s.case;
      return KS.map(function (k, i) {
        var bad = MSGS[c][i].some(function (x) { return x[3] === 1; }), type = i === 0 ? 'scenario' : (bad ? 'pitfall' : 'mechanism');
        var ns = {}; NODES[c].forEach(function (n) { ns[n] = K + 'st.' + (bad ? 'surprise' : 'done'); });
        if (c !== 'push') ns.fcm = K + 'st.skipped';
        var first = MSGS[c][i][0], edge = c === 'push' ? (first[1] === 'fcm' || first[0] === 'fcm' ? (first[0] === 'server' ? 'e3' : 'e2') : 'e1') : 'e1';
        var o = S(m, c + '.' + k, { type: type, activeNodes: NODES[c], nodeStates: ns,
          metrics: { reqs: REQS[c][i], latency: i >= 2 ? LAT[c] : 0, bg: BG[c] },
          codeHighlight: { snippet: 'i4.' + c, lines: LINES[c][i] },
          movingSignals: [{ edge: edge, tok: bad ? 'signal' : 'state' }],
          logEvents: [{ t: i, kind: bad ? 'skip' : (i === 3 ? 'complete' : 'run'), subject: first[0] }] });
        o.callouts = [{ kind: i === 0 ? 'try' : (bad ? 'pitfall' : 'source'), textKey: i === 0 ? M(m, 'co.try') : M(m, 'co.' + c + '.' + k) }];
        return o;
      });
    }
    reg(m, { controls: [sel(m, 'case', CASES)], init: function () { return { case: 'poll' }; }, act: setter(['case']), steps: steps,
      simpExtra: [M(m, 'simp.2')],
      selfChecks: [
        { name: 'polling: 7 lượt hỏi trong 30 giây (0, 5, …, 30), tin trễ 3 giây', run: function () { return REQS.poll[3] === 7 && LAT.poll === 3; } },
        { name: 'chỉ FCM nhận được khi app ở nền; WebSocket mất tin khi Doze', run: function () { return BG.push === 1 && BG.ws === 0 && MSGS.ws[3].every(function (x) { return x[3] === 1; }); } },
        { name: 'tin của mọi kênh chỉ dùng các bên của kênh đó', run: function () { return CASES.every(function (c) { return MSGS[c].every(function (r) { return r.every(function (x) { return PARTS[c].indexOf(x[0]) >= 0 && PARTS[c].indexOf(x[1]) >= 0; }); }); }); } },
        { name: 'mỗi kênh 4 bước; dòng mã nằm trong đoạn mã', run: function () { var n = { poll: 5, long: 4, ws: 6, push: 6 }; return CASES.every(function (c) { return steps({ case: c }).length === 4 && LINES[c].every(function (l) { return l.every(function (x) { return x >= 1 && x <= n[c]; }); }); }); } }] });
  })();

  /* ================= I5: mạng không tin cậy — request mất, response mất, Idempotency-Key, bão thử lại =================
     Theo DDIA bản 2 (ch.9 không phân biệt được; ch.12 idempotence; ch.2 retry storm, backoff), RFC 9110, bản nháp IETF Idempotency-Key 09,
     WorkManager define-work. Thời hạn chờ, khoảng thử và giá trị jitter là minh họa (jitter cố định để mô phỏng tất định). */
  (function () {
    var m = 'retry', CASES = ['reqlost', 'resplost', 'key', 'storm'], KS = ['s1', 's2', 's3', 's4'];
    var MSGS = {
      reqlost: [[['app', 'mid', 'book', 1], ['mid', 'mid', 'lostreq', 1]], [['app', 'app', 'timeout', 0]], [['app', 'server', 'retry', 0], ['server', 'server', 'c41', 0], ['server', 'app', 'r41', 0]], [['server', 'server', 'one', 0]]],
      resplost: [[['app', 'server', 'book', 0], ['server', 'server', 'c41', 0]], [['server', 'mid', 'lost41', 1], ['app', 'app', 'timeout', 0]], [['app', 'server', 'retry', 0], ['server', 'server', 'c42', 1], ['server', 'app', 'r42', 0]], [['server', 'server', 'two', 1]]],
      key: [[['app', 'app', 'genkey', 0], ['app', 'server', 'bookk', 0], ['server', 'server', 'c41k', 0]], [['server', 'mid', 'lost41', 1], ['app', 'app', 'timeout', 0]], [['app', 'server', 'retryk', 0], ['server', 'server', 'seen', 0], ['server', 'app', 'same', 0]], [['server', 'server', 'one', 0]]],
      storm: [[], [], [], []]
    };
    // lịch trên server sau mỗi bước: [id, key, trùng]
    var BOOK = {
      reqlost: [[], [], [['#41', '', 0]], [['#41', '', 0]]],
      resplost: [[['#41', '', 0]], [['#41', '', 0]], [['#41', '', 0], ['#42', '', 1]], [['#41', '', 0], ['#42', '', 1]]],
      key: [[['#41', 'k-7f3a', 0]], [['#41', 'k-7f3a', 0]], [['#41', 'k-7f3a', 0]], [['#41', 'k-7f3a', 0]]],
      storm: [[], [], [], []]
    };
    var ATT = { reqlost: [1, 1, 2, 2], resplost: [1, 1, 2, 2], key: [1, 1, 2, 2] };
    // bão thử lại: thời điểm gửi (giây) của 5 máy theo từng cách; 0 là lần gửi đầu cùng thất bại
    var EVERY2 = [2, 4, 6, 8, 10, 12, 14, 16], EXP = [1, 3, 7, 15];
    var JIT = [[0.1, 1.2, 3.9, 9.6], [0.3, 2.1, 4.6, 11.2], [0.55, 1.6, 5.3, 8.4], [0.7, 2.6, 3.1, 10.5], [0.95, 1.9, 5.6, 10.1]];
    var SCHED = { fail: [[], [], [], [], []], fixed: [EVERY2, EVERY2, EVERY2, EVERY2, EVERY2], exp: [EXP, EXP, EXP, EXP, EXP], jitter: JIT };
    var STORM_KIND = ['fail', 'fixed', 'exp', 'jitter'];
    function peak(kind) { var b = {}; SCHED[kind].forEach(function (ph) { ph.forEach(function (t) { var k = Math.floor(t * 2); b[k] = (b[k] || 0) + 1; }); }); var mx = 0; for (var k in b) if (b[k] > mx) mx = b[k]; return kind === 'fail' ? 5 : mx; }
    function sends(kind) { return 5 + SCHED[kind].reduce(function (a, ph) { return a + ph.length; }, 0); }
    ADE.sysRetry = { MSGS: MSGS, BOOK: BOOK, SCHED: SCHED, STORM_KIND: STORM_KIND, peak: peak };
    var LINES = { reqlost: [[3], [4], [2, 3], [3]], resplost: [[3], [4], [3], [2]], key: [[1, 3], [4], [3, 6], [6]], storm: [[1], [1, 2], [3, 4], [5]] };
    var SNIP = { reqlost: 'i5.nokey', resplost: 'i5.nokey', key: 'i5.key', storm: 'i5.storm' };
    function steps(s) {
      var c = s.case;
      return KS.map(function (k, i) {
        var bad = c === 'storm' ? (i >= 1 && peak(STORM_KIND[i]) >= 4) : (MSGS[c][i].some(function (x) { return x[3] === 1; }) || BOOK[c][i].some(function (b) { return b[2] === 1; }));
        if (c === 'storm' && i === 0) bad = false;
        var type = i === 0 ? 'scenario' : (bad ? 'pitfall' : 'mechanism');
        var nodes = c === 'storm' ? ['app', 'server'] : (i === 1 ? ['app', 'net'] : ['app', 'net', 'server']);
        var ns = {}; nodes.forEach(function (n) { ns[n] = K + 'st.' + (bad ? 'surprise' : 'done'); });
        var met = c === 'storm' ? { attempts: sends(STORM_KIND[i]), bookings: 0, peak: peak(STORM_KIND[i]) } : { attempts: ATT[c][i], bookings: BOOK[c][i].length, peak: 1 };
        var o = S(m, c + '.' + k, { type: type, activeNodes: nodes, nodeStates: ns, metrics: met,
          codeHighlight: { snippet: SNIP[c], lines: LINES[c][i] },
          movingSignals: [{ edge: i === 1 && c !== 'storm' ? 'e2' : 'e1', tok: bad ? 'signal' : 'state' }],
          logEvents: [{ t: i, kind: bad ? 'exception' : (i === 3 ? 'complete' : 'run'), subject: nodes[0] }] });
        o.callouts = [{ kind: i === 0 ? 'try' : (bad ? 'pitfall' : 'source'), textKey: i === 0 ? M(m, 'co.try') : M(m, 'co.' + c + '.' + k) }];
        return o;
      });
    }
    reg(m, { controls: [sel(m, 'case', CASES)], init: function () { return { case: 'resplost' }; }, act: setter(['case']), steps: steps,
      simpExtra: [M(m, 'simp.2')],
      selfChecks: [
        { name: 'response mất + thử lại không key: hai lịch; có key: một lịch', run: function () { return BOOK.resplost[3].length === 2 && BOOK.key[3].length === 1 && BOOK.reqlost[3].length === 1; } },
        { name: 'bão thử lại: cố định và exponential đỉnh 5, có jitter đỉnh 3', run: function () { return peak('fixed') === 5 && peak('exp') === 5 && peak('jitter') === 3; } },
        { name: 'jitter đầy đủ: mỗi khoảng chờ nằm trong [0, 2^n) giây', run: function () { return JIT.every(function (ph) { var prev = 0; return ph.every(function (t, n) { var d = t - prev; prev = t; return d >= 0 && d < Math.pow(2, n); }); }); } },
        { name: 'mỗi tình huống 4 bước; dòng mã nằm trong đoạn mã', run: function () { var n = { reqlost: 7, resplost: 7, key: 6, storm: 5 }; return CASES.every(function (c) { return steps({ case: c }).length === 4 && LINES[c].every(function (l) { return l.every(function (x) { return x >= 1 && x <= n[c]; }); }); }); } }] });
  })();

  /* ================= I6: cache — không cache, lưu mãi, max-age, max-age kèm ETag =================
     Theo RFC 9111 (độ tươi, kiểm tra lại, directive), RFC 9110 (ETag, If-None-Match, 304), Alex Xu tập 1 ch.1. Mở màn lúc 0:00, 0:02, 0:10, 0:30;
     giá đổi ở phút 20; process bị giết giữa phút 2 và 10 (cache bộ nhớ mất). Kích thước, giá, 1 KB cho 304 là minh họa. */
  (function () {
    var m = 'cache', CASES = ['none', 'forever', 'maxage', 'etag'], KS = ['s1', 's2', 's3', 's4'];
    // [bộ nhớ, đĩa, mạng], tầng trả lời, KB của bước, giá hiển thị là bản mới?
    var P = {
      none: [[['off', 'off', 'full'], 'net', 200, 0], [['off', 'off', 'full'], 'net', 200, 0], [['off', 'off', 'full'], 'net', 200, 0], [['off', 'off', 'full'], 'net', 200, 1]],
      forever: [[['miss', 'miss', 'full'], 'net', 200, 0], [['hit', 'skip', 'skip'], 'mem', 0, 0], [['miss', 'hit', 'skip'], 'disk', 0, 0], [['miss', 'hitold', 'skip'], 'disk', 0, 0]],
      maxage: [[['miss', 'miss', 'full'], 'net', 200, 0], [['fresh', 'skip', 'skip'], 'mem', 0, 0], [['miss', 'stale', 'full'], 'net', 200, 0], [['miss', 'stale', 'full'], 'net', 200, 1]],
      etag: [[['miss', 'miss', 'full7'], 'net', 200, 0], [['fresh', 'skip', 'skip'], 'mem', 0, 0], [['miss', 'stale', 'n304'], 'net', 1, 0], [['miss', 'stale', 'n200new'], 'net', 200, 1]]
    };
    var SERVER_NEW = [0, 0, 0, 1];   // giá trên server đã đổi ở bước 4 (phút 30)
    // ô "phí": tải lại dữ liệu không đổi; ô "sai": hiện giá cũ khi server đã đổi
    var WASTE = { none: [0, 1, 1, 0], forever: [0, 0, 0, 0], maxage: [0, 0, 1, 0], etag: [0, 0, 0, 0] };
    var HDR = { none: [], forever: [], maxage: ['maxage'], etag: ['maxage', 'etag', 'n304'] };
    function kb(c, i) { var t = 0; for (var k = 0; k <= i; k++) t += P[c][k][2]; return t; }
    function net(c, i) { var t = 0; for (var k = 0; k <= i; k++) if (P[c][k][0][2] !== 'skip' && P[c][k][0][2] !== 'off' || P[c][k][1] === 'net') t++; return t; }
    function right(c, i) { return P[c][i][3] === SERVER_NEW[i] ? 1 : 0; }
    ADE.sysCache = { P: P, SERVER_NEW: SERVER_NEW, WASTE: WASTE, HDR: HDR, right: right, HNAMES: { maxage: 'Cache-Control: max-age=N', nocache: 'Cache-Control: no-cache', nostore: 'Cache-Control: no-store', mustrev: 'Cache-Control: must-revalidate', private: 'Cache-Control: private', etag: 'ETag + If-None-Match', n304: '304 Not Modified' } };
    var SNIP = { none: 'i6.none', forever: 'i6.forever', maxage: 'i6.http', etag: 'i6.http' };
    var LINES = { none: [[1], [1], [1], [1]], forever: [[4], [2], [3], [3]], maxage: [[2, 4], [5], [4], [4]], etag: [[2, 4], [5], [6], [6]] };
    var TIER_NODE = { mem: 'mem', disk: 'disk', net: 'net' }, EDGE = { mem: 'e1', disk: 'e2', net: 'e3' };
    function steps(s) {
      var c = s.case;
      return KS.map(function (k, i) {
        var p = P[c][i], bad = !right(c, i) || WASTE[c][i] === 1, type = i === 0 ? 'scenario' : (bad ? 'pitfall' : 'mechanism');
        var nodes = ['ui', TIER_NODE[p[1]]], ns = {}; nodes.forEach(function (n) { ns[n] = K + 'st.' + (bad ? 'surprise' : 'done'); });
        var o = S(m, c + '.' + k, { type: type, activeNodes: nodes, nodeStates: ns,
          metrics: { kb: kb(c, i), right: right(c, i), net: net(c, i) },
          codeHighlight: { snippet: SNIP[c], lines: LINES[c][i] },
          movingSignals: [{ edge: EDGE[p[1]], tok: bad ? 'signal' : 'state' }],
          logEvents: [{ t: i, kind: bad ? 'exception' : (p[1] === 'net' ? 'run' : 'observe'), subject: TIER_NODE[p[1]] }] });
        o.callouts = [{ kind: i === 0 ? 'try' : (bad ? 'pitfall' : 'source'), textKey: i === 0 ? M(m, 'co.try') : M(m, 'co.' + c + '.' + k) }];
        return o;
      });
    }
    reg(m, { controls: [sel(m, 'case', CASES)], init: function () { return { case: 'forever' }; }, act: setter(['case']), steps: steps,
      simpExtra: [M(m, 'simp.2')],
      selfChecks: [
        { name: 'tổng KB: không cache 800, lưu mãi 200, max-age 600, ETag 401', run: function () { return kb('none', 3) === 800 && kb('forever', 3) === 200 && kb('maxage', 3) === 600 && kb('etag', 3) === 401; } },
        { name: 'bước 4: chỉ "lưu mãi" hiện giá cũ', run: function () { return right('forever', 3) === 0 && ['none', 'maxage', 'etag'].every(function (c) { return right(c, 3) === 1; }); } },
        { name: 'cache bộ nhớ mất sau khi process bị giết (bước 3)', run: function () { return CASES.every(function (c) { return P[c][2][0][0] !== 'hit' && P[c][2][0][0] !== 'fresh'; }); } },
        { name: 'mỗi cách 4 bước; dòng mã nằm trong đoạn mã', run: function () { var n = { none: 1, forever: 5, maxage: 6, etag: 6 }; return CASES.every(function (c) { return steps({ case: c }).length === 4 && LINES[c].every(function (l) { return l.every(function (x) { return x >= 1 && x <= n[c]; }); }); }); } }] });
  })();

  /* ================= I7: phân trang — offset khi có bài chèn lên đầu, offset khi có bài bị xóa, cursor =================
     Theo Zhiyong Tan, Acing the System Design Interview 12.7.1 (trang lệch khi thêm ở đầu; gửi mục cuối hiện có), AIP-158 (page_token mờ,
     next_page_token rỗng là hết), Paging 3 (PagingSource, LoadResult.Page, getRefreshKey, invalidate). Server có bài 20 → 9 (mới trước),
     trang 4 bài; ở bước 2 có bài 21 đăng lên đầu và/hoặc bài 18 bị xóa. Số bài, cỡ trang, token "tk1" là minh họa. */
  (function () {
    var m = 'paging', CASES = ['offset', 'offsetdel', 'cursor'], KS = ['s1', 's2', 's3', 's4'], LIM = 4;
    var BASE = [20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9];
    var EV = { offset: { ins: 1, del: 0 }, offsetdel: { ins: 0, del: 1 }, cursor: { ins: 1, del: 1 } };
    function srv(c, i) {
      if (i === 0) return BASE.slice();
      var l = BASE.filter(function (x) { return !(EV[c].del && x === 18); });
      return EV[c].ins ? [21].concat(l) : l;
    }
    function older(l, id, n) { return l.filter(function (x) { return x < id; }).slice(0, n); }
    // các trang app đã tải sau mỗi bước: [bước tải, nhãn, các bài]
    var PG = {
      offset: [[[0, 'p1', srv('offset', 0).slice(0, 4)]], null, [[2, 'p2', srv('offset', 2).slice(4, 8)]], []],
      offsetdel: [[[0, 'p1', srv('offsetdel', 0).slice(0, 4)]], null, [[2, 'p2', srv('offsetdel', 2).slice(4, 8)]], [[3, 'p3', srv('offsetdel', 3).slice(8, 12)]]],
      cursor: [[[0, 'p1', srv('cursor', 0).slice(0, 4)]], null, [[2, 'p2', older(srv('cursor', 2), 17, 4)]], 'refresh']
    };
    function pages(c, i) {
      var out = [];
      for (var k = 0; k <= i; k++) {
        var p = PG[c][k];
        if (p === 'refresh') out = [[k, 'rf', srv(c, k).slice(0, 8)]];
        else if (p) out = out.concat(p);
      }
      return out;
    }
    var REQ = {
      offset: ['GET /news?offset=0&limit=4', null, 'GET /news?offset=4&limit=4', null],
      offsetdel: ['GET /news?offset=0&limit=4', null, 'GET /news?offset=4&limit=4', 'GET /news?offset=8&limit=4'],
      cursor: ['GET /news?limit=4', null, 'GET /news?limit=4&page_token=tk1', 'GET /news?limit=8']
    };
    var CRASH = { offset: [0, 0, 0, 1], offsetdel: [0, 0, 0, 0], cursor: [0, 0, 0, 0] };
    // đánh dấu từng ô: app → 'dup' | 'gone' | ''; server → 'miss' | 'new' | ''
    function marks(c, i) {
      var s = srv(c, i), ps = pages(c, i), app = [], seen = {}, app_ = [];
      ps.forEach(function (p) { p[2].forEach(function (x) { app.push(x); }); });
      app.forEach(function (x) { app_.push(seen[x] ? 'dup' : (s.indexOf(x) < 0 ? 'gone' : '')); seen[x] = 1; });
      var hi = Math.max.apply(null, app), lo = Math.min.apply(null, app);
      var sv = s.map(function (x) { return seen[x] ? '' : (x > hi ? 'new' : (x > lo ? 'miss' : '')); });
      return { app: app, appMk: app_, srv: s, srvMk: sv };
    }
    function count(a, v) { return a.filter(function (x) { return x === v; }).length; }
    ADE.sysPaging = { LIM: LIM, srv: srv, pages: pages, marks: marks, REQ: REQ, CRASH: CRASH, EV: EV };
    var SNIP = { offset: 'i7.offset', offsetdel: 'i7.offset', cursor: 'i7.cursor' };
    var LINES = { offset: [[3, 4], [6], [4, 6], [10]], offsetdel: [[3, 4], [6], [4, 6], [4]], cursor: [[3, 5], [9], [3, 9], [7]] };
    var NODES = [['ui', 'pager', 'server'], ['editor', 'server'], ['ui', 'pager', 'server'], null];
    function steps(s) {
      var c = s.case;
      return KS.map(function (k, i) {
        var mk = marks(c, i), dup = count(mk.appMk, 'dup'), miss = count(mk.srvMk, 'miss'), gone = count(mk.appMk, 'gone');
        var bad = i >= 2 && (dup > 0 || miss > 0 || CRASH[c][i] === 1), type = i === 0 ? 'scenario' : (bad ? 'pitfall' : 'mechanism');
        var nodes = NODES[i] || (c === 'offset' ? ['ui'] : ['ui', 'pager', 'server']), ns = {};
        nodes.forEach(function (n) { ns[n] = K + 'st.' + (bad ? 'surprise' : 'done'); });
        var edge = i === 1 ? 'e3' : (i === 3 && c === 'offset' ? 'e1' : 'e2');
        var o = S(m, c + '.' + k, { type: type, activeNodes: nodes, nodeStates: ns,
          metrics: { dup: dup, miss: miss, gone: gone },
          codeHighlight: { snippet: SNIP[c], lines: LINES[c][i] },
          movingSignals: [{ edge: edge, tok: bad ? 'signal' : 'state' }],
          logEvents: [{ t: i, kind: bad ? 'exception' : (i === 1 ? 'write' : (REQ[c][i] ? 'run' : 'observe')), subject: nodes[nodes.length - 1] }] });
        o.callouts = [{ kind: i === 0 ? 'try' : (bad ? 'pitfall' : 'source'), textKey: i === 0 ? M(m, 'co.try') : M(m, 'co.' + c + '.' + k) }];
        return o;
      });
    }
    reg(m, { controls: [sel(m, 'case', CASES)], init: function () { return { case: 'offset' }; }, act: setter(['case']), steps: steps,
      simpExtra: [M(m, 'simp.2')],
      selfChecks: [
        { name: 'offset sau khi chèn bài 21: trang 2 bắt đầu bằng bài 17, lặp đúng một bài', run: function () { var k = marks('offset', 2); return pages('offset', 2)[1][2][0] === 17 && count(k.appMk, 'dup') === 1 && count(k.srvMk, 'miss') === 0; } },
        { name: 'offset sau khi xóa bài 18: bài 16 bị bỏ sót tới cuối danh sách', run: function () { var k = marks('offsetdel', 3); return k.app.indexOf(16) < 0 && count(k.srvMk, 'miss') === 1 && count(k.appMk, 'dup') === 0 && k.app[k.app.length - 1] === 9; } },
        { name: 'cursor: trang 2 là 16..13, không lặp không sót; làm mới thì có bài 21 và mất bài 18', run: function () { var k = marks('cursor', 2), r = marks('cursor', 3); return pages('cursor', 2)[1][2].join() === '16,15,14,13' && count(k.appMk, 'dup') + count(k.srvMk, 'miss') === 0 && r.app[0] === 21 && r.app.indexOf(18) < 0 && count(r.appMk, 'gone') === 0; } },
        { name: 'mỗi cách 4 bước; dòng mã nằm trong đoạn mã', run: function () { var n = { offset: 10, offsetdel: 10, cursor: 9 }; return CASES.every(function (c) { return steps({ case: c }).length === 4 && LINES[c].every(function (l) { return l.every(function (x) { return x >= 1 && x <= n[c]; }); }); }); } }] });
  })();

  /* ================= I8: nhiều thiết bị — ghi sau thắng (LWW), ghi có điều kiện (If-Match), gộp theo trường, cùng một trường =================
     Theo DDIA bản 2 ch.6 (mỗi thiết bị là một leader; LWW bỏ âm thầm ghi khác; gộp khóa-giá trị theo từng khóa), ch.8 (lost update, ghi có
     điều kiện, khóa lạc quan), ch.9 (LWW theo giờ client); RFC 9110 13.1.1 (If-Match, 412); Alex Xu tập 1 ch.15 (hiện cả hai bản cho người dùng).
     Máy tính bảng sửa lúc 10:02 và lưu; điện thoại mất mạng, sửa lúc 10:05 trên bản v1, có mạng lại lúc 10:20. Giờ, giá trị là minh họa. */
  (function () {
    var m = 'conflict', CASES = ['lww', 'ifmatch', 'field', 'same'], KS = ['s1', 's2', 's3', 's4'], F = ['symptom', 'allergy', 'memo'];
    var BASE = { symptom: 'cough', allergy: 'none', memo: 'empty' };
    function w(o, f, v) { var n = {}; F.forEach(function (k) { n[k] = o[k]; }); if (f) n[f] = v; return n; }
    var EDIT = { tab: { def: ['allergy', 'peni'], same: ['memo', 'late'] }, phn: { def: ['symptom', 'coughfever'], same: ['memo', 'pm'] } };
    function ed(c, who) { return EDIT[who][c === 'same' ? 'same' : 'def']; }
    // gộp theo trường so với bản gốc: chỉ một bên đổi → lấy bên đó; hai bên đổi khác nhau → xung đột
    function merge3(base, srv, mine) {
      var out = {}, cf = [];
      F.forEach(function (f) {
        if (mine[f] === base[f]) out[f] = srv[f]; else if (srv[f] === base[f] || srv[f] === mine[f]) out[f] = mine[f]; else { out[f] = srv[f]; cf.push(f); }
      });
      return { v: out, conflicts: cf };
    }
    // trạng thái sau mỗi bước: [máy tính bảng, server, điện thoại, phiên bản server, trường xung đột]
    function states(c) {
      var te = ed(c, 'tab'), pe = ed(c, 'phn'), A = w(BASE, te[0], te[1]), P = w(BASE, pe[0], pe[1]), out = [[BASE, BASE, BASE, 1, []], [A, A, P, 2, []]];
      if (c === 'lww') { out.push([A, P, P, 3, []]); out.push([P, P, P, 3, []]); }
      else if (c === 'ifmatch') { var R = w(A, pe[0], pe[1]); out.push([A, A, P, 2, []]); out.push([R, R, R, 3, []]); }
      else { var g = merge3(BASE, A, P);
        if (!g.conflicts.length) { out.push([A, g.v, P, 3, []]); out.push([g.v, g.v, g.v, 3, []]); }
        else { var U = w(A, g.conflicts[0], 'both'); out.push([A, A, P, 2, g.conflicts]); out.push([U, U, U, 3, []]); } }
      return out;
    }
    // thay đổi của người dùng bị mất (không còn trên server và không ai biết)
    function lost(c, i) {
      var st = states(c)[i], n = 0;
      if (i < 2) return 0;
      [ed(c, 'tab'), ed(c, 'phn')].forEach(function (e) { var v = st[1][e[0]]; if (v !== e[1] && v !== 'both' && st[4].indexOf(e[0]) < 0 && !(c === 'ifmatch' && i === 2)) n++; });
      return n;
    }
    var WRITES = { lww: [0, 1, 2, 2], ifmatch: [0, 1, 2, 3], field: [0, 1, 2, 2], same: [0, 1, 2, 3] };
    function ask(c, i) { return c === 'same' && i >= 2 ? 1 : 0; }
    // hành động trên làn thời gian: [máy tính bảng, server, điện thoại]
    var ACT = {
      lww: [['load', 'v1', 'load'], ['editA', 'v2', 'offS'], ['idle', 'lwwTake', 'putFull'], ['pullLost', 'keep3', 'show3']],
      ifmatch: [['load', 'v1', 'load'], ['editA', 'v2', 'offS'], ['idle', 'r412', 'putIf1'], ['pull3', 'ok3', 'retry']],
      field: [['load', 'v1', 'load'], ['editA', 'v2', 'offS'], ['idle', 'merge3', 'patchS'], ['pull3', 'keep3', 'pull3']],
      same: [['load', 'v1', 'load'], ['editM', 'v2', 'offM'], ['idle', 'conflict', 'patchM'], ['pull3', 'resolved', 'askUser']]
    };
    ADE.sysConflict = { F: F, BASE: BASE, states: states, lost: lost, ACT: ACT, ed: ed };
    var SNIP = { lww: 'i8.lww', ifmatch: 'i8.ifmatch', field: 'i8.field', same: 'i8.field' };
    var LINES = { lww: [[1], [2], [2, 3], [3]], ifmatch: [[2], [2], [4, 5], [4, 6]], field: [[1], [1, 3], [3, 4], [4]], same: [[1], [1, 3], [4, 5], [5]] };
    var NODES = { lww: [['tablet', 'server', 'phone'], ['tablet', 'server'], ['phone', 'server'], ['tablet', 'server']],
      ifmatch: [['tablet', 'server', 'phone'], ['tablet', 'server'], ['phone', 'server'], ['phone', 'server']],
      field: [['tablet', 'server', 'phone'], ['tablet', 'server'], ['phone', 'server'], ['tablet', 'server', 'phone']],
      same: [['tablet', 'server', 'phone'], ['tablet', 'server'], ['phone', 'server'], ['phone', 'server']] };
    function steps(s) {
      var c = s.case;
      return KS.map(function (k, i) {
        var lo = lost(c, i), bad = lo > 0, type = i === 0 ? 'scenario' : (bad ? 'pitfall' : 'mechanism'), nodes = NODES[c][i], ns = {};
        nodes.forEach(function (n) { ns[n] = K + 'st.' + (bad ? 'surprise' : 'done'); });
        var o = S(m, c + '.' + k, { type: type, activeNodes: nodes, nodeStates: ns,
          metrics: { lost: lo, writes: WRITES[c][i], ask: ask(c, i) },
          codeHighlight: { snippet: SNIP[c], lines: LINES[c][i] },
          movingSignals: [{ edge: nodes.indexOf('phone') >= 0 && i >= 2 ? 'e2' : 'e1', tok: bad ? 'signal' : 'state' }],
          logEvents: [{ t: i, kind: bad ? 'exception' : (i === 0 ? 'observe' : 'write'), subject: 'server' }] });
        o.callouts = [{ kind: i === 0 ? 'try' : (bad ? 'pitfall' : 'source'), textKey: i === 0 ? M(m, 'co.try') : M(m, 'co.' + c + '.' + k) }];
        return o;
      });
    }
    reg(m, { controls: [sel(m, 'case', CASES)], init: function () { return { case: 'lww' }; }, act: setter(['case']), steps: steps,
      simpExtra: [M(m, 'simp.2')],
      selfChecks: [
        { name: 'LWW: bản của điện thoại (giờ 10:05) đè cả bản ghi, dị ứng penicillin mất', run: function () { var f = states('lww')[3][1]; return f.allergy === 'none' && f.symptom === 'coughfever' && lost('lww', 3) === 1; } },
        { name: 'If-Match: lần đầu 412, server vẫn v2; làm lại trên v2 thì giữ cả hai thay đổi', run: function () { var s = states('ifmatch'); return s[2][3] === 2 && s[3][1].allergy === 'peni' && s[3][1].symptom === 'coughfever' && lost('ifmatch', 2) === 0; } },
        { name: 'gộp theo trường: hai trường khác nhau tự gộp; cùng một trường thì báo xung đột ở ghi chú', run: function () { var f = states('field')[2]; var g = states('same')[2]; return f[1].allergy === 'peni' && f[1].symptom === 'coughfever' && f[4].length === 0 && g[4].join() === 'memo' && states('same')[3][1].memo === 'both'; } },
        { name: 'mỗi cách 4 bước; dòng mã nằm trong đoạn mã', run: function () { var n = { lww: 3, ifmatch: 9, field: 5, same: 5 }; return CASES.every(function (c) { return steps({ case: c }).length === 4 && LINES[c].every(function (l) { return l.every(function (x) { return x >= 1 && x <= n[c]; }); }); }); } }] });
  })();

  /* ================= I9: thông báo đẩy như một tín hiệu — gửi nội dung, chỉ báo "có thay đổi", push bị mất, push tới hai lần =================
     Theo Alex Xu tập 1 ch.10 (trễ, đảo thứ tự nhưng không mất phía server; không đúng một lần, khử trùng theo id sự kiện), FCM (không bảo đảm
     thứ tự, message gộp, quá nhiều message chờ thì bỏ và app phải đồng bộ lại; callback vài giây) chỉ ở mức ví dụ. Dịch vụ đẩy ở đây là chung;
     trên Android thường là FCM. Giờ khám, id là minh họa. */
  (function () {
    var m = 'push', CASES = ['payload', 'tickle', 'lost', 'dup'], KS = ['s1', 's2', 's3', 's4'];
    // mỗi bước: các message [từ, tới, nhãn, xấu?] trên sơ đồ tuần tự server | dịch vụ đẩy | app
    var MSGS = {
      payload: [[['srv', 'push', 'sendA', 0]], [['srv', 'push', 'sendB', 0], ['push', 'push', 'hold', 0]], [['push', 'app', 'gotB', 0], ['push', 'app', 'gotA', 0]], [['app', 'app', 'showA', 1]]],
      tickle: [[['srv', 'push', 'tickA', 0]], [['srv', 'push', 'tickB', 0], ['push', 'push', 'collapse', 0]], [['push', 'app', 'gotT', 0], ['app', 'srv', 'fetch', 0]], [['srv', 'app', 'latest', 0]]],
      lost: [[['srv', 'push', 'tickA', 0]], [['push', 'push', 'drop', 1]], [['app', 'app', 'open', 0], ['app', 'srv', 'fetch', 0]], [['srv', 'app', 'latest', 0]]],
      dup: [[['srv', 'push', 'sendE', 0]], [['srv', 'srv', 'timeout', 0], ['srv', 'push', 'resend', 0]], [['push', 'app', 'gotE', 0], ['push', 'app', 'gotE2', 0]], [['app', 'app', 'dedupe', 0]]]
    };
    var MET = {   // [thông tin hiện đúng (-1: chưa có gì), số thông báo đã hiện, lần app tải từ server]
      payload: [[-1, 0, 0], [-1, 0, 0], [-1, 0, 0], [0, 2, 0]], tickle: [[-1, 0, 0], [-1, 0, 0], [-1, 0, 1], [1, 1, 1]],
      lost: [[-1, 0, 0], [-1, 0, 0], [-1, 0, 1], [1, 0, 1]], dup: [[-1, 0, 0], [-1, 0, 0], [-1, 0, 0], [1, 1, 0]]
    };
    // dịch vụ đẩy bảo đảm gì; hàng nổi bật theo tình huống
    var ROWS = ['order', 'once', 'arrive', 'size', 'when'], FOCUS = { payload: 'order', tickle: 'size', lost: 'arrive', dup: 'once' };
    function bad(c, i) { return MSGS[c][i].some(function (x) { return x[3] === 1; }) ? 1 : 0; }
    ADE.sysPush = { MSGS: MSGS, ROWS: ROWS, FOCUS: FOCUS, bad: bad, PARTS: ['srv', 'push', 'app'] };
    var CODE = { payload: ['i9.payload', [[1, 2], [2], [3], [4]]], tickle: ['i9.tickle', [[1, 2], [1, 2], [3, 4], [5]]], lost: ['i9.tickle', [[2], [6], [6], [5]]], dup: ['i9.dedupe', [[1], [1], [1], [2]]] };
    var EDGE = { 'srv-push': 'e1', 'push-srv': 'e1', 'push-app': 'e2', 'app-push': 'e2', 'app-srv': 'e3', 'srv-app': 'e3' };
    function steps(s) {
      var c = s.case;
      return KS.map(function (k, i) {
        var b = bad(c, i) === 1, type = i === 0 ? 'scenario' : (b ? 'pitfall' : 'mechanism'), ns = {}, nodes = [];
        MSGS[c][i].forEach(function (x) { [x[0], x[1]].forEach(function (n) { if (nodes.indexOf(n) < 0) nodes.push(n); }); });
        nodes.forEach(function (n) { ns[n] = K + 'st.' + (b ? 'surprise' : 'done'); });
        var x0 = MSGS[c][i][MSGS[c][i].length - 1], e = EDGE[x0[0] + '-' + x0[1]] || (x0[0] === 'srv' ? 'e1' : 'e2'), mt = MET[c][i];
        var o = S(m, c + '.' + k, { type: type, activeNodes: nodes, nodeStates: ns,
          metrics: { right: mt[0] < 0 ? 0 : mt[0], shown: mt[1], fetch: mt[2] },
          codeHighlight: { snippet: CODE[c][0], lines: CODE[c][1][i] },
          movingSignals: [{ edge: e, tok: b ? 'signal' : 'state' }],
          logEvents: [{ t: i, kind: b ? 'exception' : (x0[0] === x0[1] ? 'observe' : 'run'), subject: nodes[nodes.length - 1] }] });
        o.callouts = [{ kind: i === 0 ? 'try' : (b ? 'pitfall' : 'source'), textKey: i === 0 ? M(m, 'co.try') : M(m, 'co.' + c + '.' + k) }];
        return o;
      });
    }
    reg(m, { controls: [sel(m, 'case', CASES)], init: function () { return { case: 'payload' }; }, act: setter(['case']), steps: steps,
      simpExtra: [M(m, 'simp.2')],
      selfChecks: [
        { name: 'gửi nội dung: B tới trước A nên hiện giờ cũ 10:00, hai thông báo', run: function () { return MSGS.payload[2][0][2] === 'gotB' && MET.payload[3][0] === 0 && MET.payload[3][1] === 2 && bad('payload', 3) === 1; } },
        { name: 'chỉ báo có thay đổi: gộp còn một, app tải bản mới nhất, hiện đúng', run: function () { return MSGS.tickle[1][1][2] === 'collapse' && MET.tickle[3][0] === 1 && MET.tickle[3][1] === 1; } },
        { name: 'push mất: mở app vẫn đồng bộ và đúng; push hai lần: khử trùng còn một thông báo', run: function () { return MET.lost[3][0] === 1 && MET.lost[3][1] === 0 && MSGS.dup[2].length === 2 && MET.dup[3][1] === 1; } },
        { name: 'mỗi tình huống 4 bước; dòng mã nằm trong đoạn mã', run: function () { var n = { 'i9.payload': 4, 'i9.tickle': 6, 'i9.dedupe': 3 }; return CASES.every(function (c) { return steps({ case: c }).length === 4 && CODE[c][1].every(function (l) { return l.every(function (x) { return x >= 1 && x <= n[CODE[c][0]]; }); }); }); } }] });
  })();

  /* ================= I10a: bitmap — giải mã ảnh gốc so với giải mã theo kích thước hiển thị =================
     Theo Android: Loading large bitmaps (inJustDecodeBounds, inSampleSize lũy thừa của 2, calculateInSampleSize), Bitmap.Config (ARGB_8888 4 byte).
     Ảnh 4000×3000 từ camera, ô hiển thị 90 dp ở mật độ 3x = 270 px, 12 ảnh trên màn hình, giới hạn heap 256 MiB là minh họa (tùy máy). */
  (function () {
    var m = 'bitmap', CASES = ['full', 'sampled'], KS = ['s1', 's2', 's3', 's4'], W = 4000, H = 3000, REQ = 270, BPP = 4, N = 12, HEAP = 256, MIB = 1024 * 1024;
    function sample(w, h, rw, rh) { var s = 1; if (h > rh || w > rw) { var hh = h / 2, hw = w / 2; while (hh / s >= rh && hw / s >= rw) s *= 2; } return s; }
    function loop(w, h, rw, rh) { var out = [], s = 1, hh = h / 2, hw = w / 2; for (;;) { var go = hh / s >= rh && hw / s >= rw; out.push([s, hw / s, hh / s, go]); if (!go) break; s *= 2; } return out; }
    function calc(c) {
      var s = c === 'full' ? 1 : sample(W, H, REQ, REQ), dw = Math.floor(W / s), dh = Math.floor(H / s), one = dw * dh * BPP / MIB;
      return { s: s, dw: dw, dh: dh, one: one, total: one * N, oom: one * N > HEAP };
    }
    ADE.sysBitmap = { W: W, H: H, REQ: REQ, BPP: BPP, N: N, HEAP: HEAP, calc: calc, loop: function () { return loop(W, H, REQ, REQ); } };
    var LINES = { full: [['i10.full', [1]], ['i10.full', [1]], ['i10.full', [1]], ['i10.full', [2]]], sampled: [['i10.sampled', [1, 2]], ['i10.sampled', [3]], ['i10.sampled', [4, 5]], ['i10.sampled', [6]]] };
    var NODES = [['file', 'decoder'], ['decoder'], ['decoder', 'heap'], ['heap', 'screen']];
    function steps(st) {
      var c = st.case, k = calc(c);
      return KS.map(function (id, i) {
        var bad = c === 'full' && i === 3, type = i === 0 ? 'scenario' : (bad ? 'pitfall' : 'mechanism'), ns = {};
        NODES[i].forEach(function (n) { ns[n] = K + 'st.' + (bad ? 'surprise' : 'done'); });
        var mem = i < 2 ? 0 : (i === 2 ? k.one : k.total);
        var o = S(m, c + '.' + id, { type: type, activeNodes: NODES[i], nodeStates: ns,
          metrics: { one: i >= 2 ? Math.round(k.one * 100) / 100 : 0, total: Math.round(mem * 10) / 10, oom: bad ? 1 : 0 },
          codeHighlight: { snippet: LINES[c][i][0], lines: LINES[c][i][1] },
          movingSignals: [{ edge: ['e1', 'e1', 'e2', 'e3'][i], tok: bad ? 'signal' : 'state' }],
          logEvents: [{ t: i, kind: bad ? 'exception' : (i === 0 ? 'observe' : 'run'), subject: NODES[i][NODES[i].length - 1] }] });
        o.callouts = [{ kind: i === 0 ? 'try' : (bad ? 'pitfall' : 'source'), textKey: i === 0 ? M(m, 'co.try') : M(m, 'co.' + c + '.' + id) }];
        return o;
      });
    }
    reg(m, { controls: [sel(m, 'case', CASES)], init: function () { return { case: 'full' }; }, act: setter(['case']), steps: steps,
      simpExtra: [M(m, 'simp.2')],
      selfChecks: [
        { name: 'ví dụ của tài liệu: 2048×1536, đích 512×384 → inSampleSize 4, 0,75 MiB thay vì 12 MiB', run: function () { return sample(2048, 1536, 512, 384) === 4 && 512 * 384 * 4 / MIB === 0.75 && 2048 * 1536 * 4 / MIB === 12; } },
        { name: '4000×3000 cho ô 270 px: inSampleSize 8 → 500×375, khoảng 0,72 MiB; ảnh gốc 45,8 MiB', run: function () { var a = calc('sampled'), b = calc('full'); return a.s === 8 && a.dw === 500 && a.dh === 375 && Math.abs(a.one - 0.715) < 0.01 && Math.abs(b.one - 45.78) < 0.01; } },
        { name: '12 ảnh gốc vượt giới hạn 256 MiB; 12 ảnh đã thu nhỏ thì không', run: function () { return calc('full').oom && !calc('sampled').oom; } },
        { name: 'mỗi cách 4 bước; dòng mã nằm trong đoạn mã', run: function () { var n = { 'i10.full': 2, 'i10.sampled': 6 }; return CASES.every(function (c) { return steps({ case: c }).length === 4 && LINES[c].every(function (p) { return p[1].every(function (x) { return x >= 1 && x <= n[p[0]]; }); }); }); } }] });
  })();

  /* ================= I10b: upload tệp lớn — một request so với upload tiếp tục được, theo khúc =================
     Theo Alex Xu tập 1 ch.14–15 (chia khúc, upload tiếp tục được: lấy URL, gửi, đứt thì tiếp) và bản nháp IETF Resumable Uploads for HTTP
     (draft 16: POST → Location, HEAD → Upload-Offset, PATCH). Video 200 MB, khúc 10 MB, đứt khi đang gửi khúc 20 (195 MB) là minh họa.
     Giản lược: server trong mô phỏng chỉ giữ các khúc trọn vẹn; theo bản nháp, server có thể báo cả phần lẻ. */
  (function () {
    var m = 'upload', CASES = ['whole', 'resumable'], KS = ['s1', 's2', 's3', 's4'], NCH = 20, MB = 10;
    // mỗi hàng là một request (hay một lượt gửi); trạng thái từng khúc: '' chưa gửi | 'sent' đang gửi, server chưa giữ | 'ok' server đã giữ | 'lost' mất | 'part' gửi dở
    function fill(n, v) { var a = []; for (var k = 0; k < NCH; k++) a.push(k < n ? v : ''); return a; }
    function rowsOf(c, i) {
      if (c === 'whole') {
        var r1 = i === 0 ? fill(10, 'sent') : fill(19, 'lost'); if (i >= 1) r1[19] = 'part';
        var rows = [['r1', r1]];
        if (i >= 2) rows.push(['r2', i === 2 ? fill(10, 'sent') : fill(20, 'ok')]);
        return rows;
      }
      var f = i === 0 ? fill(10, 'ok') : fill(19, 'ok');
      if (i === 1 || i === 2) f[19] = 'part'; if (i === 3) f[19] = 'ok';
      return [['file', f]];
    }
    var WASTE = { whole: [0, 195, 195, 195], resumable: [0, 5, 5, 5] };   // MB đã gửi mà phải gửi lại
    var SENT = { whole: [100, 195, 295, 395], resumable: [100, 195, 195, 205] }, STORED = { whole: [0, 0, 0, 200], resumable: [100, 190, 190, 200] };
    var HTTP = {
      whole: [['POST /videos  (200 MB, Content-Length: 209715200)'], ['… 195 MB: connection reset'], ['POST /videos  (200 MB, again from byte 0)'], ['← 201 Created']],
      resumable: [['POST /uploads  (Upload-Complete: ?0)', '← 104, Location: /uploads/abc', 'PATCH /uploads/abc  (Upload-Offset: 0 … 90 MB)'], ['PATCH /uploads/abc  (Upload-Offset: 190 MB)', '… 195 MB: connection reset'], ['HEAD /uploads/abc', '← 204, Upload-Offset: 190 MB'], ['PATCH /uploads/abc  (Upload-Offset: 190 MB, Upload-Complete: ?1)', '← 201 Created']]
    };
    ADE.sysUpload = { NCH: NCH, MB: MB, rowsOf: rowsOf, SENT: SENT, STORED: STORED, HTTP: HTTP };
    var LINES = { whole: [['i10.whole', [1, 2]], ['i10.whole', [2]], ['i10.whole', [2]], ['i10.whole', [2]]], resumable: [['i10.resumable', [1, 3, 4, 5]], ['i10.resumable', [5]], ['i10.resumable', [2]], ['i10.resumable', [3, 5, 7]]] };
    var NODES = [['app', 'net', 'server'], ['net'], ['app', 'server'], ['app', 'server']];
    function steps(st) {
      var c = st.case;
      return KS.map(function (id, i) {
        var bad = (i === 1) || (c === 'whole' && i >= 2), type = i === 0 ? 'scenario' : (bad ? 'pitfall' : 'mechanism'), ns = {};
        NODES[i].forEach(function (n) { ns[n] = K + 'st.' + (bad ? 'surprise' : 'done'); });
        var o = S(m, c + '.' + id, { type: type, activeNodes: NODES[i], nodeStates: ns,
          metrics: { sent: SENT[c][i], stored: STORED[c][i], waste: WASTE[c][i] },
          codeHighlight: { snippet: LINES[c][i][0], lines: LINES[c][i][1] },
          movingSignals: [{ edge: i === 1 ? 'e1' : 'e2', tok: bad ? 'signal' : 'state' }],
          logEvents: [{ t: i, kind: bad ? 'exception' : (i === 3 ? 'complete' : 'run'), subject: NODES[i][NODES[i].length - 1] }] });
        o.callouts = [{ kind: i === 0 ? 'try' : (bad ? 'pitfall' : 'source'), textKey: i === 0 ? M(m, 'co.try') : M(m, 'co.' + c + '.' + id) }];
        return o;
      });
    }
    reg(m, { controls: [sel(m, 'case', CASES)], init: function () { return { case: 'whole' }; }, act: setter(['case']), steps: steps,
      simpExtra: [M(m, 'simp.2')],
      selfChecks: [
        { name: 'một request: đứt ở 195 MB thì gửi lại từ đầu, tổng 395 MB', run: function () { return SENT.whole[3] === 395 && STORED.whole[1] === 0 && rowsOf('whole', 3)[1][1].every(function (x) { return x === 'ok'; }); } },
        { name: 'tiếp tục được: HEAD báo 190 MB, chỉ gửi lại khúc 20, tổng 205 MB', run: function () { var f = rowsOf('resumable', 2)[0][1]; return f.slice(0, 19).every(function (x) { return x === 'ok'; }) && f[19] === 'part' && SENT.resumable[3] === 205 && STORED.resumable[2] === 19 * MB; } },
        { name: 'lãng phí cuối cùng: 195 MB so với 5 MB', run: function () { var w = steps({ case: 'whole' })[3].metrics.waste, r = steps({ case: 'resumable' })[3].metrics.waste; return w === 195 && r === 5; } },
        { name: 'mỗi cách 4 bước; dòng mã nằm trong đoạn mã', run: function () { var n = { 'i10.whole': 2, 'i10.resumable': 7 }; return CASES.every(function (c) { return steps({ case: c }).length === 4 && LINES[c].every(function (p) { return p[1].every(function (x) { return x >= 1 && x <= n[p[0]]; }); }); }); } }] });
  })();

  /* ================= I11: khởi động — cold start khởi tạo hết, cold start khởi tạo lười, warm start, hot start =================
     Theo Android: App startup time (cold, warm, hot; TTID, TTFD; khởi tạo nặng trong Application), Startup analysis (việc > 20 ms, đợi sau khung hình
     đầu), App Startup (Initializer, khởi tạo lười). Mọi con số mili giây là minh họa; máy thật khác nhiều. */
  (function () {
    var m = 'startup', CASES = ['heavy', 'lazy', 'warm', 'hot'], KS = ['s1', 's2', 's3', 's4'];
    // việc: [khóa, làn, bắt đầu ms, thời lượng ms, hiện từ bước]
    var IT = {
      heavy: [['proc', 'main', 0, 300, 0], ['crash', 'main', 300, 80, 1], ['analytics', 'main', 380, 300, 1], ['ads', 'main', 680, 900, 1], ['chat', 'main', 1580, 600, 1], ['img', 'main', 2180, 150, 1], ['db', 'main', 2330, 700, 1], ['act', 'main', 3030, 500, 2], ['load', 'bg', 3530, 400, 3]],
      lazy: [['proc', 'main', 0, 300, 0], ['crash', 'main', 300, 80, 1], ['db', 'bg', 380, 700, 1], ['act', 'main', 380, 500, 2], ['load', 'bg', 1080, 200, 3], ['analytics', 'bg', 1280, 300, 3]],
      warm: [['act', 'main', 0, 500, 2], ['load', 'bg', 500, 100, 3]],
      hot: [['resume', 'main', 0, 100, 2]]
    };
    var TTID = { heavy: 3530, lazy: 880, warm: 500, hot: 100 }, TTFD = { heavy: 3930, lazy: 1280, warm: 600, hot: 100 };
    function loadEnd(c) { var e = TTID[c]; IT[c].forEach(function (x) { if (x[0] === 'load') e = x[2] + x[3]; }); return e; }
    function init(c) { return IT[c].filter(function (x) { return x[1] === 'main' && ['crash', 'analytics', 'ads', 'chat', 'img', 'db'].indexOf(x[0]) >= 0; }).reduce(function (a, x) { return a + x[3]; }, 0); }
    function ends(c) { var e = 0; IT[c].forEach(function (x) { e = Math.max(e, x[2] + x[3]); }); return e; }
    ADE.sysStartup = { IT: IT, TTID: TTID, TTFD: TTFD, init: init, MAX: 4000 };
    var CODE = { heavy: ['i11.heavy', [[1], [4, 5, 6, 7, 8, 9], [2], [9]]], lazy: ['i11.lazy', [[1], [2, 8], [9], [9]]], warm: ['i11.lazy', [[1], [2], [9], [9]]], hot: ['i11.lazy', [[1], [2], [9], [9]]] };
    var NODES = [['proc'], ['app'], ['act'], ['act', 'frame']];
    function steps(st) {
      var c = st.case;
      return KS.map(function (k, i) {
        var bad = c === 'heavy' && (i === 1 || i === 3), type = i === 0 ? 'scenario' : (bad ? 'pitfall' : 'mechanism'), ns = {};
        NODES[i].forEach(function (n) { ns[n] = K + 'st.' + (bad ? 'surprise' : 'done'); });
        var o = S(m, c + '.' + k, { type: type, activeNodes: NODES[i], nodeStates: ns,
          metrics: { init: i >= 1 ? init(c) : 0, ttid: i >= 2 ? TTID[c] : 0, ttfd: i >= 3 ? TTFD[c] : 0 },
          codeHighlight: { snippet: CODE[c][0], lines: CODE[c][1][i] },
          movingSignals: [{ edge: ['e1', 'e1', 'e2', 'e3'][i], tok: bad ? 'signal' : 'state' }],
          logEvents: [{ t: i, kind: bad ? 'exception' : (i === 3 ? 'complete' : 'run'), subject: NODES[i][NODES[i].length - 1] }] });
        o.callouts = [{ kind: i === 0 ? 'try' : (bad ? 'pitfall' : 'source'), textKey: i === 0 ? M(m, 'co.try') : M(m, 'co.' + c + '.' + k) }];
        return o;
      });
    }
    reg(m, { controls: [sel(m, 'case', CASES)], init: function () { return { case: 'heavy' }; }, act: setter(['case']), steps: steps,
      simpExtra: [M(m, 'simp.2')],
      selfChecks: [
        { name: 'khởi tạo hết: 2730 ms trên luồng chính, TTID 3530 ms', run: function () { return init('heavy') === 2730 && TTID.heavy === 3530 && TTFD.heavy === loadEnd('heavy') && ends('heavy') === TTFD.heavy; } },
        { name: 'khởi tạo lười: chỉ 80 ms trong Application, TTID 880 ms, TTFD 1280 ms', run: function () { return init('lazy') === 80 && TTID.lazy === 300 + 80 + 500 && TTFD.lazy === loadEnd('lazy'); } },
        { name: 'warm và hot không tạo process, không chạy Application.onCreate', run: function () { return ['warm', 'hot'].every(function (c) { return IT[c].every(function (x) { return x[0] !== 'proc' && init(c) === 0; }); }) && TTID.hot < TTID.warm && TTID.warm < TTID.lazy; } },
        { name: 'mỗi cách 4 bước; dòng mã nằm trong đoạn mã', run: function () { var n = { 'i11.heavy': 11, 'i11.lazy': 9 }; return CASES.every(function (c) { return steps({ case: c }).length === 4 && CODE[c][1].every(function (l) { return l.every(function (x) { return x >= 1 && x <= n[CODE[c][0]]; }); }); }); } }] });
  })();

  /* ================= I12a: phát hành — 100% một lần, theo phần trăm, feature flag =================
     Theo Play staged rollout (chọn ngẫu nhiên; tạm dừng không gỡ bản đã cài), Android vitals (ngưỡng crash 1,09%), Seemann 10.1 (feature flag).
     100.000 người dùng; bản 1.2.0 crash ở 3% máy; tốc độ cài, số người, ngày là minh họa. */
  (function () {
    var m = 'rollout', CASES = ['bigbang', 'staged', 'flag'], KS = ['s1', 's2', 's3', 's4'], RATE = 0.03;
    // theo ngày 1..7: [chữ "đang phát", số người (nghìn) đang chạy mã lỗi]
    var D = {
      bigbang: [['o120_100', 40], ['o120_100', 70], ['o121_100', 85], ['o121_100', 50], ['o121_100', 25], ['o121_100', 10], ['o121_100', 5]],
      staged: [['o120_1', 1], ['halt', 1], ['o121_1', 0.6], ['o121_5', 0.3], ['o121_20', 0.1], ['o121_50', 0], ['o121_100', 0]],
      flag: [['o120_flagoff', 0], ['flag1off', 1], ['o121_flagoff', 0], ['flag5', 0], ['flag20', 0], ['flag50', 0], ['flag100', 0]]
    };
    var STEP_DAYS = [[0], [1], [2], [3, 4, 5, 6]];
    function crashOf(c, d) { return Math.round(D[c][d][1] * 1000 * RATE); }
    function total(c, upto) { var t = 0; for (var d = 0; d <= upto; d++) t += crashOf(c, d); return t; }
    ADE.sysRollout = { D: D, STEP_DAYS: STEP_DAYS, crashOf: crashOf, RATE: RATE };
    var CODE = { bigbang: ['i12.release', [[1], [1], [2], [2]]], staged: ['i12.release', [[1], [1], [2], [2]]], flag: ['i12.flag', [[1], [2, 3], [1], [3]]] };
    var NODES = [['console', 'users'], ['users', 'vitals'], ['console', 'users'], ['users', 'vitals']];
    function steps(st) {
      var c = st.case;
      return KS.map(function (k, i) {
        var last = STEP_DAYS[i][STEP_DAYS[i].length - 1], today = crashOf(c, STEP_DAYS[i][0]);
        var bad = (c === 'bigbang' && i <= 2) || (c === 'staged' && i === 1), type = i === 0 ? 'scenario' : (bad ? 'pitfall' : 'mechanism'), ns = {};
        NODES[i].forEach(function (n) { ns[n] = K + 'st.' + (bad ? 'surprise' : 'done'); });
        var o = S(m, c + '.' + k, { type: type, activeNodes: NODES[i], nodeStates: ns,
          metrics: { exposed: D[c][STEP_DAYS[i][0]][1], today: today, total: total(c, last) },
          codeHighlight: { snippet: CODE[c][0], lines: CODE[c][1][i] },
          movingSignals: [{ edge: i % 2 === 0 ? 'e1' : 'e2', tok: bad ? 'signal' : 'state' }],
          logEvents: [{ t: i, kind: bad ? 'exception' : (i === 3 ? 'complete' : 'run'), subject: NODES[i][NODES[i].length - 1] }] });
        o.callouts = [{ kind: i === 0 ? 'try' : (bad ? 'pitfall' : 'source'), textKey: i === 0 ? M(m, 'co.try') : M(m, 'co.' + c + '.' + k) }];
        return o;
      });
    }
    reg(m, { controls: [sel(m, 'case', CASES)], init: function () { return { case: 'bigbang' }; }, act: setter(['case']), steps: steps,
      simpExtra: [M(m, 'simp.2')],
      selfChecks: [
        { name: 'tổng người gặp crash sau 7 ngày: 100% một lần 8550, theo phần trăm 90, cờ 30', run: function () { return total('bigbang', 6) === 8550 && total('staged', 6) === 90 && total('flag', 6) === 30; } },
        { name: 'tạm dừng phát hành không gỡ bản đã cài: ngày 2 vẫn còn 1000 người chạy bản lỗi', run: function () { return D.staged[1][0] === 'halt' && D.staged[1][1] === 1 && crashOf('staged', 1) === 30; } },
        { name: 'tắt cờ thì ngày 3 không còn ai chạy mã lỗi, không cần bản mới để dừng', run: function () { return D.flag[2][1] === 0 && D.flag[1][1] === 1; } },
        { name: 'mỗi cách 4 bước; dòng mã nằm trong đoạn mã', run: function () { var n = { 'i12.release': 2, 'i12.flag': 3 }; return CASES.every(function (c) { return steps({ case: c }).length === 4 && CODE[c][1].every(function (l) { return l.every(function (x) { return x >= 1 && x <= n[CODE[c][0]]; }); }); }); } }] });
  })();

  /* ================= I12b: tương thích — đổi tên trường tại chỗ, thêm trường, API /v2, thêm trường + bắt cập nhật =================
     Theo DDIA bản 2 ch.5 (mã cũ và mới cùng tồn tại; tương thích xuôi cần mã cũ bỏ qua phần thêm; thêm trường thường giữ tương thích; phá vỡ thì giữ
     nhiều phiên bản API), kotlinx.serialization (khóa lạ mặc định gây lỗi; ignoreUnknownKeys), In-app updates (immediate). Tỉ lệ phiên bản là minh họa. */
  (function () {
    var m = 'compat', CASES = ['rename', 'additive', 'versioned', 'forced'], KS = ['s1', 's2', 's3', 's4'];
    var APPS = [['v10', 4, 'strict'], ['v11', 11, 'lenient'], ['v12', 60, 'lenient'], ['v13', 25, 'new']];   // [phiên bản, % người dùng, kiểu giải mã]
    // kết quả của từng phiên bản app với API "sau thay đổi": ok | crash | update (bị bắt cập nhật) | v2 (gọi /v2)
    function result(c, a) {
      if (c === 'rename') return a[2] === 'new' ? 'ok' : 'crash';
      if (c === 'additive') return a[2] === 'strict' ? 'crash' : 'ok';
      if (c === 'versioned') return a[2] === 'new' ? 'v2' : 'ok';
      return a[2] === 'strict' ? 'update' : 'ok';
    }
    function share(c, r) { return APPS.filter(function (a) { return result(c, a) === r; }).reduce(function (s, a) { return s + a[1]; }, 0); }
    var APIS = { rename: 1, additive: 1, versioned: 2, forced: 1 };
    ADE.sysCompat = { APPS: APPS, result: result, share: share, APIS: APIS };
    var CODE = { rename: [[1], [4], [1, 4], [4]], additive: [[1], [5], [2, 3], [3]], versioned: [[1], [5], [3], [3]], forced: [[1], [5], [2], [3]] };
    var NODES = [['apps'], ['server'], ['apps', 'server'], ['apps']];
    function steps(st) {
      var c = st.case;
      return KS.map(function (k, i) {
        var broken = i >= 2 ? share(c, 'crash') : 0, bad = broken > 0, type = i === 0 ? 'scenario' : (bad ? 'pitfall' : 'mechanism'), ns = {};
        NODES[i].forEach(function (n) { ns[n] = K + 'st.' + (bad ? 'surprise' : 'done'); });
        var o = S(m, c + '.' + k, { type: type, activeNodes: NODES[i], nodeStates: ns,
          metrics: { broken: broken, forced: i >= 2 ? share(c, 'update') : 0, apis: i >= 1 ? APIS[c] : 1 },
          codeHighlight: { snippet: 'i12.json', lines: CODE[c][i] },
          movingSignals: [{ edge: i === 1 ? 'e1' : 'e2', tok: bad ? 'signal' : 'state' }],
          logEvents: [{ t: i, kind: bad ? 'exception' : (i === 1 ? 'write' : 'observe'), subject: NODES[i][NODES[i].length - 1] }] });
        o.callouts = [{ kind: i === 0 ? 'try' : (bad ? 'pitfall' : 'source'), textKey: i === 0 ? M(m, 'co.try') : M(m, 'co.' + c + '.' + k) }];
        return o;
      });
    }
    reg(m, { controls: [sel(m, 'case', CASES)], init: function () { return { case: 'rename' }; }, act: setter(['case']), steps: steps,
      simpExtra: [M(m, 'simp.2')],
      selfChecks: [
        { name: 'đổi tên tại chỗ: 75% người dùng (1.0 tới 1.2) lỗi', run: function () { return share('rename', 'crash') === 75; } },
        { name: 'thêm trường: chỉ bản 1.0 giải mã chặt bị lỗi (4%)', run: function () { return share('additive', 'crash') === 4; } },
        { name: 'API /v2: không ai lỗi, nhưng server giữ hai phiên bản; bắt cập nhật: 4% thấy màn cập nhật thay vì crash', run: function () { return share('versioned', 'crash') === 0 && APIS.versioned === 2 && share('forced', 'update') === 4 && share('forced', 'crash') === 0; } },
        { name: 'mỗi cách 4 bước; dòng mã nằm trong đoạn mã', run: function () { return CASES.every(function (c) { return steps({ case: c }).length === 4 && CODE[c].every(function (l) { return l.every(function (x) { return x >= 1 && x <= 5; }); }); }); } }] });
  })();

  /* ================= I13: bài mẫu — một tin nhắn từ lúc gõ tới "đã xem", qua các chương trước =================
     Theo Alex Xu tập 1 ch.12 (message_id duy nhất, tăng theo thời gian; cur_max_message_id mỗi thiết bị; push khi người nhận offline) và
     Zhiyong Tan, Acing ch.14 (xác nhận đã nhận, đã xem; ghi ở message service trước; phía nhận kiểm tra trùng). Cách ghép các phần là của site.
     Sáu bước: gửi → chờ mạng → server nhận → giao → đã xem → thiết bị thứ hai đồng bộ. */
  (function () {
    var m = 'chat', CASES = ['online', 'offline', 'away'], KS = ['s1', 's2', 's3', 's4', 's5', 's6'];
    // thành phần của app và server cho đồ thị; cạnh [từ, tới]
    // ba hàng để không có đường cắt nhau: giao diện → repository → kết nối sống; Room, WorkManager; nhận push dưới WorkManager; server bên phải
    var COMP = { ui: [70, 40], vm: [200, 40], repo: [330, 40], ws: [460, 40], db: [330, 120], worker: [460, 120], push: [460, 200], server: [590, 120] };
    var EDGES = [['ui', 'vm'], ['vm', 'repo'], ['repo', 'db'], ['worker', 'db'], ['worker', 'server'], ['server', 'ws'], ['ws', 'repo'], ['server', 'push'], ['push', 'worker']];
    // mỗi bước: [thành phần sáng, cạnh sáng (chỉ số), cạnh lỗi, tin trên sơ đồ tuần tự [từ, tới, nhãn, xấu?], dấu tick 0..3, số bản tin trên server, máy người gửi đã có]
    var P = {
      online: [
        [['ui', 'vm', 'repo', 'db'], [0, 1, 2], [], [['a', 'a', 'pending', 0]], 0, 0, 1],
        [['worker', 'db'], [3], [], [['a', 'a', 'netok', 0]], 0, 0, 1],
        [['worker', 'server'], [4], [], [['a', 'srv', 'post', 0], ['srv', 'a', 'ack', 0]], 1, 1, 1],
        [['server', 'ws'], [5], [], [['srv', 'b', 'wsdeliver', 0], ['b', 'srv', 'delivered', 0], ['srv', 'a', 'ticks2', 0]], 2, 1, 1],
        [['ws', 'repo', 'ui'], [6], [], [['b', 'srv', 'read', 0], ['srv', 'a', 'seen', 0]], 3, 1, 1],
        [['server', 'repo', 'db'], [6, 2], [], [['a2', 'srv', 'sync', 0], ['srv', 'a2', 'syncres', 0]], 3, 1, 2]],
      offline: [
        [['ui', 'vm', 'repo', 'db'], [0, 1, 2], [], [['a', 'a', 'pending', 0]], 0, 0, 1],
        [['worker', 'db'], [3], [4], [['a', 'a', 'netwait', 1]], 0, 0, 1],
        [['worker', 'server'], [4], [], [['a', 'srv', 'post', 0], ['srv', 'srv', 'stored', 0], ['srv', 'a', 'lostack', 1], ['a', 'srv', 'retry', 0], ['srv', 'a', 'samekey', 0]], 1, 1, 1],
        [['server', 'ws'], [5], [], [['srv', 'b', 'wsdeliver', 0], ['b', 'srv', 'delivered', 0], ['srv', 'a', 'ticks2', 0]], 2, 1, 1],
        [['ws', 'repo', 'ui'], [6], [], [['b', 'srv', 'read', 0], ['srv', 'a', 'seen', 0]], 3, 1, 1],
        [['server', 'repo', 'db'], [6, 2], [], [['a2', 'srv', 'sync', 0], ['srv', 'a2', 'syncres', 0]], 3, 1, 2]],
      away: [
        [['ui', 'vm', 'repo', 'db'], [0, 1, 2], [], [['a', 'a', 'pending', 0]], 0, 0, 1],
        [['worker', 'db'], [3], [], [['a', 'a', 'netok', 0]], 0, 0, 1],
        [['worker', 'server'], [4], [], [['a', 'srv', 'post', 0], ['srv', 'a', 'ack', 0]], 1, 1, 1],
        [['server', 'push', 'worker'], [7, 8], [5], [['srv', 'b', 'wsnone', 1], ['srv', 'b', 'tickle', 0], ['b', 'srv', 'fetch', 0], ['b', 'srv', 'delivered', 0]], 2, 1, 1],
        [['ws', 'repo', 'ui'], [6], [], [['b', 'srv', 'read', 0], ['srv', 'a', 'seen', 0]], 3, 1, 1],
        [['server', 'repo', 'db'], [6, 2], [], [['a2', 'srv', 'sync', 0], ['srv', 'a2', 'syncres', 0]], 3, 1, 2]]
    };
    ADE.sysChat = { COMP: COMP, EDGES: EDGES, P: P, PARTS: ['a', 'a2', 'srv', 'b'] };
    var LINES = [[2, 3], [4], [6], [7], [8], [8]];
    var NODEMAP = { ui: 'phone', vm: 'phone', repo: 'phone', db: 'phone', worker: 'phone', ws: 'phone', push: 'phone', server: 'server' };
    function steps(st) {
      var c = st.case;
      return KS.map(function (k, i) {
        var p = P[c][i], bad = p[3].some(function (x) { return x[3] === 1; }), type = i === 0 ? 'scenario' : (bad ? 'pitfall' : 'mechanism'), ns = {};
        var nodes = []; p[0].forEach(function (x) { var n = NODEMAP[x]; if (nodes.indexOf(n) < 0) nodes.push(n); });
        if (p[3].some(function (x) { return x[0] === 'b' || x[1] === 'b'; })) nodes.push('peer');
        nodes.forEach(function (n) { ns[n] = K + 'st.' + (bad ? 'surprise' : 'done'); });
        var o = S(m, c + '.' + k, { type: type, activeNodes: nodes, nodeStates: ns,
          metrics: { ticks: p[4], copies: p[5], devices: p[6] },
          codeHighlight: { snippet: 'i13.send', lines: LINES[i] },
          movingSignals: [{ edge: nodes.indexOf('peer') >= 0 ? 'e2' : 'e1', tok: bad ? 'signal' : 'state' }],
          logEvents: [{ t: i, kind: bad ? 'exception' : (i === 5 ? 'complete' : 'run'), subject: nodes[nodes.length - 1] }] });
        o.callouts = [{ kind: i === 0 ? 'try' : (bad ? 'pitfall' : 'source'), textKey: i === 0 ? M(m, 'co.try') : M(m, 'co.' + c + '.' + k) }];
        return o;
      });
    }
    reg(m, { controls: [sel(m, 'case', CASES)], init: function () { return { case: 'online' }; }, act: setter(['case']), steps: steps,
      simpExtra: [M(m, 'simp.2')],
      selfChecks: [
        { name: 'mọi tình huống: dấu tick đi 0 → 1 → 2 → 3, server chỉ giữ một bản tin', run: function () { return CASES.every(function (c) { var t = P[c].map(function (p) { return p[4]; }); return t[0] === 0 && t[2] === 1 && t[3] === 2 && t[5] === 3 && P[c].every(function (p) { return p[5] <= 1; }); }); } },
        { name: 'mất mạng: response đầu mất, gửi lại cùng khóa, server không tạo bản thứ hai', run: function () { var m3 = P.offline[2][3].map(function (x) { return x[2]; }); return m3.indexOf('lostack') >= 0 && m3.indexOf('samekey') >= 0 && P.offline[2][5] === 1; } },
        { name: 'người nhận tắt app: không có WebSocket, push chỉ báo rồi app tự tải', run: function () { var m4 = P.away[3][3].map(function (x) { return x[2]; }); return m4.indexOf('wsnone') >= 0 && m4.indexOf('tickle') >= 0 && m4.indexOf('fetch') >= 0; } },
        { name: 'mỗi tình huống 6 bước; dòng mã nằm trong đoạn mã', run: function () { return CASES.every(function (c) { return steps({ case: c }).length === 6; }) && LINES.every(function (l) { return l.every(function (x) { return x >= 1 && x <= 8; }); }); } }] });
  })();
})();
