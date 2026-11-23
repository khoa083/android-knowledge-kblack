/* Model track G (thuần, không DOM, không câu chữ; chỉ message key). MÔ HÌNH GIẢNG DẠY (simplified).
   Nguồn: docs/research/arch.md (developer.android.com đọc ngày 2026-11-23; sách Dumbravan, Boudjnah). */
(function () {
  'use strict';
  var K = 'track.arch.';
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
    ADE.registerModel('arch.' + m, def);
  }
  var sel = function (m, id, vals) { return { id: id, type: 'select', labelKey: M(m, 'ctl.' + id), get: function (s) { return s[id]; }, action: id, options: vals.map(function (v) { return { value: v, labelKey: M(m, 'ctl.' + id + '.' + v) }; }) }; };
  var setter = function (keys) { return function (s, a, v) { var n = {}; keys.forEach(function (k) { n[k] = s[k]; }); if (keys.indexOf(a) >= 0) n[a] = v; return n; }; };

  /* ================= G1: Activity làm mọi thứ so với tách tầng — bốn phép thử: bấm, xoay màn hình, đổi API, kiểm thử =================
     Theo Guide to app architecture (component có thể bị hủy bất cứ lúc nào; tách mối quan tâm), Handle configuration changes
     (Activity bị hủy và tạo lại), ViewModel overview (giữ state qua thay đổi cấu hình), Testing fundamentals (local và instrumented).
     Số file phải sửa là đếm trong app mẫu Hẹn Khám (ba màn hình cùng gọi API giờ trống), chỉ để minh họa. */
  (function () {
    var m = 'god', CASES = ['god', 'layered'];
    var NODES = ['ui', 'vm', 'repo', 'source'];
    // mỗi bước: [node sáng, trạng thái node, số đo {keep, files, test}, loại bước, dòng mã, loại log, chủ thể]
    var P = {
      god: [[['ui'], { ui: 'done', vm: 'skipped', repo: 'skipped', source: 'skipped' }, { keep: 'na', files: 0, test: 'na' }, 'scenario', [1, 2, 3, 4, 5, 6, 7], 'run', 'ui'],
        [['ui'], { ui: 'surprise', vm: 'skipped', repo: 'skipped', source: 'skipped' }, { keep: 'no', files: 0, test: 'na' }, 'pitfall', [1, 2], 'observe', 'ui'],
        [['ui'], { ui: 'surprise', vm: 'skipped', repo: 'skipped', source: 'skipped' }, { keep: 'no', files: 3, test: 'na' }, 'pitfall', [4, 5], 'write', 'ui'],
        [['ui'], { ui: 'surprise', vm: 'skipped', repo: 'skipped', source: 'skipped' }, { keep: 'no', files: 3, test: 'device' }, 'pitfall', [3, 4, 5, 6], 'observe', 'ui']],
      layered: [[['ui', 'vm', 'repo', 'source'], { ui: 'done', vm: 'done', repo: 'done', source: 'done' }, { keep: 'na', files: 0, test: 'na' }, 'scenario', [1, 2, 3, 4, 5, 6, 7, 8], 'run', 'vm'],
        [['ui', 'vm'], { ui: 'done', vm: 'done', repo: 'done', source: 'done' }, { keep: 'yes', files: 0, test: 'na' }, 'mechanism', [2, 5, 6], 'observe', 'vm'],
        [['repo', 'source'], { ui: 'done', vm: 'done', repo: 'done', source: 'done' }, { keep: 'yes', files: 1, test: 'na' }, 'mechanism', [8, 9], 'write', 'source'],
        [['vm', 'repo'], { ui: 'done', vm: 'done', repo: 'done', source: 'done' }, { keep: 'yes', files: 1, test: 'local' }, 'mechanism', [10, 11, 12], 'complete', 'vm']]
    };
    ADE.archGod = P;
    var EDGE = { ui: null, vm: 'e1', repo: 'e2', source: 'e3' };
    function steps(s) {
      var K4 = ['tap', 'rotate', 'api', 'test'];
      return P[s.case].map(function (p, i) {
        var ns = {}; Object.keys(p[1]).forEach(function (n) { ns[n] = K + 'st.' + p[1][n]; });
        var met = { keep: M(m, 'keep.' + p[2].keep), files: p[2].files, test: M(m, 'test.' + p[2].test) };
        var e = EDGE[p[0][0]] || EDGE[p[0][1]], bad = p[3] === 'pitfall';
        var o = S(m, s.case + '.' + K4[i], { type: p[3], activeNodes: p[0], nodeStates: ns, metrics: met, codeHighlight: { snippet: 'g1.' + s.case, lines: p[4] },
          movingSignals: e ? [{ edge: e, tok: bad ? 'signal' : 'state' }] : [], logEvents: [{ t: i, kind: p[5], subject: p[6] }] });
        if (i === 0) o.callouts = [{ kind: 'try', textKey: M(m, 'co.try') }];
        if (i >= 1) o.callouts = [{ kind: bad ? 'pitfall' : 'source', textKey: M(m, 'co.' + s.case + '.' + K4[i]) }];
        return o;
      });
    }
    reg(m, { controls: [sel(m, 'case', CASES)], init: function () { return { case: 'god' }; }, act: setter(['case']), steps: steps,
      simpExtra: [M(m, 'simp.2')],
      selfChecks: [
        { name: 'mỗi cách có 4 bước: bấm, xoay màn hình, đổi API, kiểm thử', run: function () { return CASES.every(function (k) { return steps({ case: k }).length === 4; }); } },
        { name: 'Activity làm mọi thứ: mất dữ liệu khi xoay, phải sửa nhiều file, chỉ test được trên thiết bị', run: function () { var g = steps({ case: 'god' })[3].metrics; return g.keep === M(m, 'keep.no') && g.files > 1 && g.test === M(m, 'test.device'); } },
        { name: 'tách tầng: giữ dữ liệu qua xoay, sửa 1 file, test được trên máy (local)', run: function () { var l = steps({ case: 'layered' })[3].metrics; return l.keep === M(m, 'keep.yes') && l.files === 1 && l.test === M(m, 'test.local'); } }] });
  })();
  /* ================= G2a: hướng phụ thuộc giữa các tầng (đồ thị "A biết về B") =================
     Theo Guide to app architecture (mũi tên trong hướng dẫn là phụ thuộc giữa các lớp; domain phụ thuộc data), Domain layer
     (use case phụ thuộc repository), Modularization và Common modularization patterns (internal ẩn khai báo khỏi module khác;
     giao tiếp hai chiều trực tiếp giữa hai module là không thể vì phụ thuộc vòng), Kotlin Visibility modifiers (module là tập file
     biên dịch cùng nhau), Boudjnah ch1–2 (Dependency Rule: mũi tên hướng vào domain; đảo phụ thuộc bằng interface repository đặt
     cạnh use case). Cạnh của từng bước nằm ở ADE.archLayers để hình đồ thị (views/visuals.js) và model dùng chung một dữ liệu. */
  (function () {
    var m = 'layers', CASES = ['google', 'wrong', 'modules', 'inverted'], KS = ['s1', 's2', 's3', 's4'];
    var BASE = [['ui', 'vm'], ['vm', 'uc'], ['uc', 'repo'], ['repo', 'api'], ['repo', 'dao']];
    var NOUC = [['ui', 'vm'], ['vm', 'repo'], ['repo', 'api'], ['repo', 'dao']];
    var INV = [['ui', 'vm'], ['vm', 'uc'], ['repo', 'uc'], ['repo', 'api'], ['repo', 'dao']];
    var BAD = BASE.concat([['repo', 'ui']]);
    var MODS = [['feature', ['ui', 'vm']], ['domain', ['uc']], ['data', ['repo', 'api', 'dao']]];
    var ok = { ui: 'done', vm: 'done', uc: 'done', repo: 'done', api: 'done', dao: 'done' };
    var st = function (o) { var n = {}, k; for (k in ok) n[k] = ok[k]; for (k in o) n[k] = o[k]; return n; };
    // mỗi bước: [cạnh, nhóm module (null = một module), kết quả build, node sáng, trạng thái node, số đo {wrong, caught, test}, loại bước, dòng mã, loại log, chủ thể, dữ liệu đi ngược lên]
    var P = {
      google: [
        [BASE, null, 'na', ['ui', 'vm', 'uc', 'repo'], ok, { wrong: 0, caught: 'na', test: 'jvm' }, 'scenario', [1, 2, 3, 4, 5, 6, 7], 'observe', 'ui', false],
        [BASE, null, 'na', ['dao', 'repo', 'uc', 'vm', 'ui'], ok, { wrong: 0, caught: 'na', test: 'jvm' }, 'mechanism', [7, 8], 'run', 'repo', true],
        [NOUC, null, 'na', ['vm', 'repo'], st({ uc: 'skipped' }), { wrong: 0, caught: 'na', test: 'jvm' }, 'mechanism', [3, 5], 'write', 'vm', false],
        [BASE, null, 'na', ['repo', 'api', 'dao'], ok, { wrong: 0, caught: 'na', test: 'jvm' }, 'mechanism', [10, 11], 'complete', 'repo', false]],
      wrong: [
        [BASE, null, 'na', ['repo'], ok, { wrong: 0, caught: 'na', test: 'jvm' }, 'scenario', [3, 4, 5, 6], 'observe', 'repo', false],
        [BAD, null, 'na', ['repo', 'ui'], st({ repo: 'surprise' }), { wrong: 1, caught: 'na', test: 'jvm' }, 'pitfall', [1, 2, 3, 4, 5], 'write', 'repo', false],
        [BAD, null, 'pass', ['repo', 'ui'], st({ repo: 'surprise' }), { wrong: 1, caught: 'none', test: 'jvm' }, 'pitfall', [7], 'run', 'repo', false],
        [BAD, null, 'pass', ['ui', 'vm', 'uc', 'repo'], st({ repo: 'surprise', ui: 'surprise' }), { wrong: 1, caught: 'none', test: 'device' }, 'pitfall', [3, 8], 'observe', 'repo', false]],
      modules: [
        [BASE, MODS, 'na', ['ui', 'vm', 'uc', 'repo'], ok, { wrong: 0, caught: 'na', test: 'jvm' }, 'scenario', [1, 2], 'observe', 'repo', false],
        [BAD, MODS, 'unresolved', ['repo', 'ui'], st({ repo: 'broken' }), { wrong: 1, caught: 'compiler', test: 'jvm' }, 'mechanism', [3, 4], 'exception', 'repo', false],
        [BAD, MODS, 'cycle', ['repo', 'ui', 'vm', 'uc'], st({ repo: 'broken', ui: 'broken' }), { wrong: 1, caught: 'gradle', test: 'jvm' }, 'pitfall', [5, 6, 7], 'exception', 'repo', false],
        [BASE, MODS, 'pass', ['vm', 'repo'], ok, { wrong: 0, caught: 'gradle', test: 'jvm' }, 'mechanism', [8, 9], 'complete', 'vm', false]],
      inverted: [
        [BASE, null, 'na', ['uc', 'repo'], ok, { wrong: 0, caught: 'na', test: 'jvm' }, 'scenario', [1, 2, 3], 'observe', 'uc', false],
        [INV, null, 'na', ['uc', 'repo'], ok, { wrong: 0, caught: 'na', test: 'jvm' }, 'mechanism', [1, 2, 4, 5], 'write', 'repo', false],
        [INV, null, 'na', ['uc'], ok, { wrong: 0, caught: 'na', test: 'jvm' }, 'mechanism', [1, 2, 3], 'run', 'uc', false],
        [INV, null, 'pass', ['repo', 'uc'], ok, { wrong: 0, caught: 'na', test: 'jvm' }, 'mechanism', [6, 7], 'complete', 'repo', false]]
    };
    ADE.archLayers = {
      CASES: CASES,
      at: function (c, i) {
        var p = P[c][i];
        return { edges: p[0].map(function (x) { return { from: x[0], to: x[1], bad: x[0] === 'repo' && x[1] === 'ui' }; }), mods: p[1], build: p[2], dataUp: p[10], noUc: p[0] === NOUC };
      }
    };
    var EDGE = { 'ui>vm': 'e1', 'vm>uc': 'e2', 'uc>repo': 'e3', 'repo>api': 'e4', 'repo>dao': 'e5' };
    function steps(s) {
      return P[s.case].map(function (p, i) {
        var ns = {}; Object.keys(p[4]).forEach(function (n) { ns[n] = K + 'st.' + p[4][n]; });
        var met = { wrong: p[5].wrong, caught: M(m, 'caught.' + p[5].caught), test: M(m, 'test.' + p[5].test) };
        var sig;
        if (p[10]) sig = [{ edge: 'e5', tok: 'state', reverse: true }, { edge: 'e3', tok: 'state', reverse: true }, { edge: 'e2', tok: 'state', reverse: true }, { edge: 'e1', tok: 'state', reverse: true }];
        else if (s.case === 'inverted' && i >= 1) sig = [{ edge: 'e3', tok: 'state', reverse: true }];
        else sig = [{ edge: EDGE[p[3][0] + '>' + p[3][1]] || 'e1', tok: p[6] === 'pitfall' ? 'signal' : 'state' }];
        var o = S(m, s.case + '.' + KS[i], { type: p[6], activeNodes: p[3], nodeStates: ns, metrics: met, codeHighlight: { snippet: 'g2.' + s.case, lines: p[7] },
          movingSignals: sig, logEvents: [{ t: i, kind: p[8], subject: p[9] }] });
        o.callouts = [{ kind: i === 0 ? 'try' : (p[6] === 'pitfall' ? 'pitfall' : 'source'), textKey: i === 0 ? M(m, 'co.try') : M(m, 'co.' + s.case + '.' + KS[i]) }];
        return o;
      });
    }
    reg(m, { controls: [sel(m, 'case', CASES)], init: function () { return { case: 'google' }; }, act: setter(['case']), steps: steps,
      simpExtra: [M(m, 'simp.2')],
      selfChecks: [
        { name: 'mỗi tình huống có 4 bước', run: function () { return CASES.every(function (k) { return steps({ case: k }).length === 4; }); } },
        { name: 'một module: phụ thuộc sai vẫn biên dịch qua, không ai bắt', run: function () { var a = ADE.archLayers.at('wrong', 2); return a.build === 'pass' && a.edges.some(function (x) { return x.bad; }) && steps({ case: 'wrong' })[2].metrics.caught === M(m, 'caught.none'); } },
        { name: 'tách module: trình biên dịch bắt import sai, Gradle chặn vòng phụ thuộc', run: function () { return ADE.archLayers.at('modules', 1).build === 'unresolved' && ADE.archLayers.at('modules', 2).build === 'cycle'; } },
        { name: 'đảo phụ thuộc: repository trỏ vào domain, domain không trỏ ra ngoài', run: function () { var ed = ADE.archLayers.at('inverted', 3).edges; return ed.some(function (x) { return x.from === 'repo' && x.to === 'uc'; }) && !ed.some(function (x) { return x.from === 'uc'; }); } }] });
  })();

  /* ================= G2b: một nguồn sự thật (SSOT) và luồng dữ liệu một chiều (UDF) =================
     Theo Guide to app architecture (SSOT là chủ của dữ liệu, chỉ SSOT được sửa, lộ ra kiểu bất biến; UDF: state đi xuống,
     sự kiện đi lên tới SSOT), Data layer (mỗi repository định nghĩa một SSOT; dữ liệu lộ ra phải bất biến), UI layer (vòng UDF). */
  (function () {
    var m = 'ssot', CASES = ['twowriters', 'ssot'], KS = ['s1', 's2', 's3', 's4'];
    // mỗi bước: [node sáng, trạng thái node, số đo {copies, writers, agree}, loại bước, dòng mã, loại log, chủ thể, tín hiệu]
    var P = {
      twowriters: [
        [['choose'], { choose: 'done', mine: 'done', repo: 'done' }, { copies: 2, writers: 2, agree: 'na' }, 'scenario', [2, 3], 'write', 'choose', [{ edge: 'e1', tok: 'signal' }]],
        [['mine'], { choose: 'done', mine: 'surprise', repo: 'done' }, { copies: 3, writers: 2, agree: 'no' }, 'pitfall', [4], 'observe', 'mine', [{ edge: 'e4', tok: 'state' }]],
        [['mine', 'repo'], { choose: 'done', mine: 'surprise', repo: 'surprise' }, { copies: 3, writers: 3, agree: 'no' }, 'pitfall', [5], 'write', 'mine', [{ edge: 'e3', tok: 'signal' }]],
        [['choose', 'mine', 'repo'], { choose: 'surprise', mine: 'surprise', repo: 'surprise' }, { copies: 3, writers: 3, agree: 'no' }, 'pitfall', [1, 2, 4], 'observe', 'choose', [{ edge: 'e2', tok: 'state' }]]],
      ssot: [
        [['choose', 'repo'], { choose: 'done', mine: 'done', repo: 'done' }, { copies: 1, writers: 1, agree: 'na' }, 'scenario', [3, 6], 'write', 'choose', [{ edge: 'e1', tok: 'signal' }]],
        [['repo'], { choose: 'done', mine: 'done', repo: 'done' }, { copies: 1, writers: 1, agree: 'na' }, 'mechanism', [1, 2, 3], 'run', 'repo', [{ edge: 'e1', tok: 'signal' }]],
        [['repo', 'choose', 'mine'], { choose: 'done', mine: 'done', repo: 'done' }, { copies: 1, writers: 1, agree: 'yes' }, 'mechanism', [2, 7, 8], 'observe', 'repo', [{ edge: 'e2', tok: 'state' }, { edge: 'e4', tok: 'state' }]],
        [['mine', 'repo', 'choose'], { choose: 'done', mine: 'done', repo: 'done' }, { copies: 1, writers: 1, agree: 'yes' }, 'mechanism', [4, 8], 'complete', 'mine', [{ edge: 'e3', tok: 'signal' }, { edge: 'e2', tok: 'state' }]]]
    };
    function steps(s) {
      return P[s.case].map(function (p, i) {
        var ns = {}; Object.keys(p[1]).forEach(function (n) { ns[n] = K + 'st.' + p[1][n]; });
        var met = { copies: p[2].copies, writers: p[2].writers, agree: M(m, 'agree.' + p[2].agree) };
        var o = S(m, s.case + '.' + KS[i], { type: p[3], activeNodes: p[0], nodeStates: ns, metrics: met, codeHighlight: { snippet: 'g2.' + s.case, lines: p[4] },
          movingSignals: p[7], logEvents: [{ t: i, kind: p[5], subject: p[6] }] });
        o.callouts = [{ kind: i === 0 ? 'try' : (p[3] === 'pitfall' ? 'pitfall' : 'source'), textKey: i === 0 ? M(m, 'co.try') : M(m, 'co.' + s.case + '.' + KS[i]) }];
        return o;
      });
    }
    reg(m, { controls: [sel(m, 'case', CASES)], init: function () { return { case: 'twowriters' }; }, act: setter(['case']), steps: steps,
      selfChecks: [
        { name: 'mỗi tình huống có 4 bước', run: function () { return CASES.every(function (k) { return steps({ case: k }).length === 4; }); } },
        { name: 'nhiều nơi giữ và sửa dữ liệu: hai màn hình lệch nhau', run: function () { var x = steps({ case: 'twowriters' })[3].metrics; return x.copies > 1 && x.writers > 1 && x.agree === M(m, 'agree.no'); } },
        { name: 'một nguồn sự thật: một bản, một chỗ sửa, hai màn hình khớp', run: function () { var x = steps({ case: 'ssot' })[3].metrics; return x.copies === 1 && x.writers === 1 && x.agree === M(m, 'agree.yes'); } }] });
  })();
  /* ================= G3: thông báo "Đã đặt lịch" qua một lần xoay màn hình =================
     Theo UI events (ViewModel event phải thành cập nhật UI state; UI báo lại khi đã hiện thông báo; Channel và stream khác
     không bảo đảm giao khi ViewModel sống lâu hơn UI), State holders (ViewModel sống qua tái tạo Activity), kotlinx.coroutines
     1.11.0 API: StateFlow phát lại giá trị mới nhất cho subscriber mới; MutableSharedFlow() không replay, emit trả về ngay khi
     không có subscriber (giá trị bị bỏ). Bốn cột của hình "Làn thời gian" lấy từ ADE.archEvents. */
  (function () {
    var m = 'events', CASES = ['sticky', 'shared', 'state'], KS = ['s1', 's2', 's3', 's4'];
    // mỗi ô: [mã chuỗi, kiểu ô] — kiểu: '' bình thường, 'hl' đang xảy ra, 'bad' lỗi, 'dim' không còn/không có
    // hàng: a1 = Activity lần 1, a2 = Activity lần 2 (sau xoay), vm = ViewModel, user = người dùng thấy
    var LANES = ['a1', 'vm', 'a2', 'user'];
    var G = {
      sticky: [
        { a1: ['tap', 'hl'], vm: ['setMsg', 'hl'], a2: ['none', 'dim'], user: ['toast1', ''] },
        { a1: ['destroyed', 'dim'], vm: ['keepMsg', 'bad'], a2: ['created', 'hl'], user: ['nothing', 'dim'] },
        { a1: ['destroyed', 'dim'], vm: ['replay', 'bad'], a2: ['collect', 'hl'], user: ['toast2', 'bad'] },
        { a1: ['destroyed', 'dim'], vm: ['keepMsg', 'bad'], a2: ['rotateAgain', 'hl'], user: ['toast3', 'bad'] }],
      shared: [
        { a1: ['tap', 'hl'], vm: ['request', 'hl'], a2: ['none', 'dim'], user: ['waiting', ''] },
        { a1: ['destroyed', 'dim'], vm: ['request', ''], a2: ['notYet', 'dim'], user: ['nothing', 'dim'] },
        { a1: ['destroyed', 'dim'], vm: ['emitNoSub', 'bad'], a2: ['notYet', 'dim'], user: ['nothing', 'dim'] },
        { a1: ['destroyed', 'dim'], vm: ['emptyFlow', 'bad'], a2: ['collectNothing', 'hl'], user: ['bookAgain', 'bad'] }],
      state: [
        { a1: ['tap', 'hl'], vm: ['setMsg', 'hl'], a2: ['none', 'dim'], user: ['toast1', ''] },
        { a1: ['shownCall', 'hl'], vm: ['cleared', 'hl'], a2: ['none', 'dim'], user: ['toast1', 'dim'] },
        { a1: ['destroyed', 'dim'], vm: ['noMsg', ''], a2: ['collectClean', 'hl'], user: ['nothing', ''] },
        { a1: ['destroyed', 'dim'], vm: ['pendingMsg', 'hl'], a2: ['collectPending', 'hl'], user: ['toastOnce', ''] }]
    };
    // số đo theo bước: {shown, lost, truth}
    var MET = {
      sticky: [{ shown: 1, lost: 'no', truth: 'flag' }, { shown: 1, lost: 'no', truth: 'flag' }, { shown: 2, lost: 'no', truth: 'flag' }, { shown: 3, lost: 'no', truth: 'flag' }],
      shared: [{ shown: 0, lost: 'na', truth: 'stream' }, { shown: 0, lost: 'na', truth: 'stream' }, { shown: 0, lost: 'yes', truth: 'stream' }, { shown: 0, lost: 'yes', truth: 'stream' }],
      state: [{ shown: 1, lost: 'no', truth: 'state' }, { shown: 1, lost: 'no', truth: 'state' }, { shown: 1, lost: 'no', truth: 'state' }, { shown: 1, lost: 'no', truth: 'state' }]
    };
    var STEP = {   // [node sáng, trạng thái node, loại bước, dòng mã, loại log, chủ thể, tín hiệu]
      sticky: [[['act', 'vm', 'flow', 'toast'], { act: 'done', vm: 'done', flow: 'done', toast: 'done' }, 'scenario', [2, 3, 6], 'write', 'vm', [{ edge: 'e1', tok: 'signal' }, { edge: 'e2', tok: 'state' }]],
        [['act', 'vm'], { act: 'skipped', vm: 'done', flow: 'done', toast: 'skipped' }, 'mechanism', [1, 2], 'observe', 'act', []],
        [['flow', 'act', 'toast'], { act: 'done', vm: 'done', flow: 'surprise', toast: 'surprise' }, 'pitfall', [5, 6], 'observe', 'act', [{ edge: 'e2', tok: 'state' }, { edge: 'e3', tok: 'signal' }]],
        [['flow', 'toast'], { act: 'done', vm: 'done', flow: 'surprise', toast: 'surprise' }, 'pitfall', [5, 6], 'observe', 'toast', [{ edge: 'e3', tok: 'signal' }]]],
      shared: [[['act', 'vm'], { act: 'done', vm: 'done', flow: 'done', toast: 'skipped' }, 'scenario', [2, 3], 'write', 'vm', [{ edge: 'e1', tok: 'signal' }]],
        [['act'], { act: 'skipped', vm: 'done', flow: 'done', toast: 'skipped' }, 'mechanism', [1], 'observe', 'act', []],
        [['vm', 'flow'], { act: 'skipped', vm: 'done', flow: 'surprise', toast: 'skipped' }, 'pitfall', [3, 4], 'skip', 'flow', []],
        [['act', 'flow', 'toast'], { act: 'done', vm: 'done', flow: 'surprise', toast: 'surprise' }, 'pitfall', [7], 'observe', 'toast', [{ edge: 'e2', tok: 'state' }]]],
      state: [[['act', 'vm', 'flow', 'toast'], { act: 'done', vm: 'done', flow: 'done', toast: 'done' }, 'scenario', [3, 5, 7], 'write', 'vm', [{ edge: 'e1', tok: 'signal' }, { edge: 'e2', tok: 'state' }]],
        [['toast', 'act', 'vm'], { act: 'done', vm: 'done', flow: 'done', toast: 'done' }, 'mechanism', [4, 8], 'write', 'act', [{ edge: 'e1', tok: 'signal' }]],
        [['flow', 'act'], { act: 'done', vm: 'done', flow: 'done', toast: 'done' }, 'mechanism', [1, 3], 'observe', 'act', [{ edge: 'e2', tok: 'state' }]],
        [['flow', 'act', 'toast'], { act: 'done', vm: 'done', flow: 'done', toast: 'done' }, 'mechanism', [7, 8], 'complete', 'toast', [{ edge: 'e2', tok: 'state' }, { edge: 'e3', tok: 'signal' }]]]
    };
    ADE.archEvents = { LANES: LANES, at: function (c, i) { return G[c][i]; } };
    function steps(s) {
      return STEP[s.case].map(function (p, i) {
        var ns = {}; Object.keys(p[1]).forEach(function (n) { ns[n] = K + 'st.' + p[1][n]; });
        var x = MET[s.case][i];
        var o = S(m, s.case + '.' + KS[i], { type: p[2], activeNodes: p[0], nodeStates: ns,
          metrics: { shown: x.shown, lost: M(m, 'lost.' + x.lost), truth: M(m, 'truth.' + x.truth) },
          codeHighlight: { snippet: 'g3.' + s.case, lines: p[3] }, movingSignals: p[6], logEvents: [{ t: i, kind: p[4], subject: p[5] }] });
        o.callouts = [{ kind: i === 0 ? 'try' : (p[2] === 'pitfall' ? 'pitfall' : 'source'), textKey: i === 0 ? M(m, 'co.try') : M(m, 'co.' + s.case + '.' + KS[i]) }];
        return o;
      });
    }
    reg(m, { controls: [sel(m, 'case', CASES)], init: function () { return { case: 'sticky' }; }, act: setter(['case']), steps: steps,
      simpExtra: [M(m, 'simp.2')],
      selfChecks: [
        { name: 'mỗi tình huống có 4 bước', run: function () { return CASES.every(function (k) { return steps({ case: k }).length === 4; }); } },
        { name: 'cờ trong StateFlow không xóa: thông báo hiện lại sau mỗi lần xoay', run: function () { var a = steps({ case: 'sticky' }); return a[3].metrics.shown > a[0].metrics.shown; } },
        { name: 'SharedFlow không replay, phát lúc không có subscriber: thông báo mất', run: function () { var x = steps({ case: 'shared' })[3].metrics; return x.shown === 0 && x.lost === M(m, 'lost.yes'); } },
        { name: 'thông báo là UI state, UI báo đã hiện: đúng một lần, không mất', run: function () { return steps({ case: 'state' }).every(function (s) { return s.metrics.shown === 1 && s.metrics.lost === M(m, 'lost.no'); }); } }] });
  })();
  /* ================= G4: data layer offline-first: database là nguồn sự thật =================
     Theo Build an offline-first app (đọc chỉ từ nguồn cục bộ, là nguồn sự thật chuẩn; ghi cập nhật vào nguồn cục bộ trước để nó
     báo cho người đọc; đọc qua Flow; ghi qua suspend; ba chiến lược ghi: chỉ online, hàng đợi, ghi lười với WorkManager),
     Data layer (mỗi repository một SSOT). Hàng của hình "Làn thời gian" lấy từ ADE.archOffline. */
  (function () {
    var m = 'offline', CASES = ['mixed', 'ssot', 'lazy'], KS = ['s1', 's2', 's3', 's4'];
    var LANES = ['net', 'db', 'repo', 'ui'];
    var G = {
      mixed: [
        { net: ['idle', 'dim'], db: ['oldList', ''], repo: ['readDb', 'hl'], ui: ['showOld', ''] },
        { net: ['returnsNew', 'hl'], db: ['stillOld', 'bad'], repo: ['passThrough', 'bad'], ui: ['showNew', 'hl'] },
        { net: ['idle', 'dim'], db: ['stillOld', 'bad'], repo: ['readDb', ''], ui: ['showOldAgain', 'bad'] },
        { net: ['offline', 'dim'], db: ['stillOld', 'bad'], repo: ['readDb', ''], ui: ['showOldOffline', 'bad'] }],
      ssot: [
        { net: ['idle', 'dim'], db: ['oldList', ''], repo: ['readDb', 'hl'], ui: ['showOld', ''] },
        { net: ['returnsNew', 'hl'], db: ['written', 'hl'], repo: ['writeDb', 'hl'], ui: ['showOld', 'dim'] },
        { net: ['idle', 'dim'], db: ['emits', 'hl'], repo: ['flowEmits', ''], ui: ['showNew', 'hl'] },
        { net: ['offline', 'dim'], db: ['keepNew', ''], repo: ['refreshFail', 'hl'], ui: ['showNewOffline', 'hl'] }],
      lazy: [
        { net: ['offline', 'dim'], db: ['markPending', 'hl'], repo: ['writeLocalFirst', 'hl'], ui: ['tapCancel', ''] },
        { net: ['offline', 'dim'], db: ['emitsPending', ''], repo: ['flowEmits', ''], ui: ['showPending', 'hl'] },
        { net: ['offline', 'dim'], db: ['pending', ''], repo: ['queued', 'hl'], ui: ['showPending', ''] },
        { net: ['receivesCancel', 'hl'], db: ['clearPending', 'hl'], repo: ['workerRuns', 'hl'], ui: ['showSynced', 'hl'] }]
    };
    var MET = {   // {src, ui, db}: UI đọc từ đâu, UI có bản mới nhất không, DB có bản mới nhất không
      mixed: [{ src: 'db', ui: 'no', db: 'no' }, { src: 'net', ui: 'yes', db: 'no' }, { src: 'db', ui: 'no', db: 'no' }, { src: 'db', ui: 'no', db: 'no' }],
      ssot: [{ src: 'db', ui: 'no', db: 'no' }, { src: 'db', ui: 'no', db: 'yes' }, { src: 'db', ui: 'yes', db: 'yes' }, { src: 'db', ui: 'yes', db: 'yes' }],
      lazy: [{ src: 'db', ui: 'no', db: 'yes' }, { src: 'db', ui: 'yes', db: 'yes' }, { src: 'db', ui: 'yes', db: 'yes' }, { src: 'db', ui: 'yes', db: 'yes' }]
    };
    var STEP = {   // [node sáng, trạng thái node, loại bước, dòng mã, loại log, chủ thể, tín hiệu]
      mixed: [[['ui', 'repo', 'db'], { ui: 'done', repo: 'done', db: 'done', net: 'skipped' }, 'scenario', [1, 2], 'observe', 'ui', [{ edge: 'e2', tok: 'state', reverse: true }]],
        [['repo', 'net', 'ui'], { ui: 'done', repo: 'surprise', db: 'surprise', net: 'done' }, 'pitfall', [3, 6], 'run', 'repo', [{ edge: 'e3', tok: 'state', reverse: true }, { edge: 'e1', tok: 'state', reverse: true }]],
        [['ui', 'db'], { ui: 'surprise', repo: 'done', db: 'surprise', net: 'skipped' }, 'pitfall', [2, 7], 'observe', 'ui', [{ edge: 'e2', tok: 'state', reverse: true }]],
        [['ui', 'db'], { ui: 'surprise', repo: 'done', db: 'surprise', net: 'broken' }, 'pitfall', [2], 'observe', 'ui', [{ edge: 'e2', tok: 'state', reverse: true }]]],
      ssot: [[['ui', 'repo', 'db'], { ui: 'done', repo: 'done', db: 'done', net: 'skipped' }, 'scenario', [2, 8], 'observe', 'ui', [{ edge: 'e2', tok: 'state', reverse: true }]],
        [['repo', 'net', 'db'], { ui: 'done', repo: 'done', db: 'done', net: 'done' }, 'mechanism', [3, 4, 5], 'write', 'repo', [{ edge: 'e3', tok: 'state', reverse: true }, { edge: 'e2', tok: 'signal' }]],
        [['db', 'repo', 'ui'], { ui: 'done', repo: 'done', db: 'done', net: 'done' }, 'mechanism', [5, 8], 'observe', 'db', [{ edge: 'e2', tok: 'state', reverse: true }, { edge: 'e1', tok: 'state', reverse: true }]],
        [['repo', 'net', 'ui'], { ui: 'done', repo: 'done', db: 'done', net: 'broken' }, 'mechanism', [2, 4], 'exception', 'net', [{ edge: 'e2', tok: 'state', reverse: true }]]],
      lazy: [[['ui', 'repo', 'db'], { ui: 'done', repo: 'done', db: 'done', net: 'broken' }, 'scenario', [1, 2], 'write', 'ui', [{ edge: 'e1', tok: 'signal' }, { edge: 'e2', tok: 'signal' }]],
        [['db', 'ui'], { ui: 'done', repo: 'done', db: 'done', net: 'broken' }, 'mechanism', [2], 'observe', 'ui', [{ edge: 'e2', tok: 'state', reverse: true }, { edge: 'e1', tok: 'state', reverse: true }]],
        [['repo'], { ui: 'done', repo: 'done', db: 'done', net: 'broken' }, 'mechanism', [3, 4, 5], 'skip', 'repo', []],
        [['repo', 'net', 'db', 'ui'], { ui: 'done', repo: 'done', db: 'done', net: 'done' }, 'mechanism', [7], 'complete', 'net', [{ edge: 'e3', tok: 'signal' }, { edge: 'e2', tok: 'signal' }]]]
    };
    ADE.archOffline = { LANES: LANES, at: function (c, i) { return G[c][i]; } };
    function steps(s) {
      return STEP[s.case].map(function (p, i) {
        var ns = {}; Object.keys(p[1]).forEach(function (n) { ns[n] = K + 'st.' + p[1][n]; });
        var x = MET[s.case][i];
        var o = S(m, s.case + '.' + KS[i], { type: p[2], activeNodes: p[0], nodeStates: ns,
          metrics: { src: M(m, 'src.' + x.src), ui: M(m, 'fresh.' + x.ui), db: M(m, 'fresh.' + x.db) },
          codeHighlight: { snippet: 'g4.' + s.case, lines: p[3] }, movingSignals: p[6], logEvents: [{ t: i, kind: p[4], subject: p[5] }] });
        o.callouts = [{ kind: i === 0 ? 'try' : (p[2] === 'pitfall' ? 'pitfall' : 'source'), textKey: i === 0 ? M(m, 'co.try') : M(m, 'co.' + s.case + '.' + KS[i]) }];
        return o;
      });
    }
    reg(m, { controls: [sel(m, 'case', CASES)], init: function () { return { case: 'mixed' }; }, act: setter(['case']), steps: steps,
      selfChecks: [
        { name: 'mỗi tình huống có 4 bước', run: function () { return CASES.every(function (k) { return steps({ case: k }).length === 4; }); } },
        { name: 'trả thẳng kết quả mạng cho UI: DB vẫn cũ, mở lại màn thấy bản cũ', run: function () { var x = steps({ case: 'mixed' }); return x[1].metrics.ui === M(m, 'fresh.yes') && x[2].metrics.ui === M(m, 'fresh.no') && x[2].metrics.db === M(m, 'fresh.no'); } },
        { name: 'DB là nguồn sự thật: UI chỉ đọc DB và có bản mới sau khi DB được ghi', run: function () { var x = steps({ case: 'ssot' }); return x.every(function (s) { return s.metrics.src === M(m, 'src.db'); }) && x[2].metrics.ui === M(m, 'fresh.yes'); } },
        { name: 'ghi lười: UI thấy thay đổi ngay cả khi mất mạng', run: function () { return ADE.archOffline.at('lazy', 1).net[0] === 'offline' && steps({ case: 'lazy' })[1].metrics.ui === M(m, 'fresh.yes'); } }] });
  })();
  /* ================= G5: domain layer tùy chọn và use case =================
     Theo Domain layer (domain tùy chọn; gói logic phức tạp hay logic đơn giản dùng lại ở nhiều ViewModel; mỗi use case một việc,
     không giữ dữ liệu thay đổi; main-safe; đặt tên động từ + danh từ + UseCase; chỉ thêm khi cần; giới hạn truy cập tầng data
     có thể buộc viết use case chỉ chuyển tiếp). Bảng quy tắc và cây quyết định của hình "Quy tắc và nơi viết" lấy từ ADE.archUseCase.
     Ví dụ: lúc 8:00 xem giờ 9:30; quy tắc cũ "đặt trước ít nhất 1 giờ", quy tắc mới "ít nhất 2 giờ". */
  (function () {
    var m = 'usecase', CASES = ['duplicated', 'shared', 'passthrough'], KS = ['s1', 's2', 's3', 's4'];
    // bảng: cột choose, resched, uc; mỗi ô {past, hours, lead, ans} — giá trị: 'y' có kiểm, '1h'/'2h' ngưỡng đặt trước, 'use' dùng use case, '-' không có, 'fwd' chỉ chuyển tiếp
    var COLS = ['choose', 'resched', 'uc'];
    var R = function (p, h, l, a) { return { past: p, hours: h, lead: l, ans: a }; };
    var NONE = R('-', '-', '-', '-'), USE = function (a) { return R('use', 'use', 'use', a); };
    var T = {
      duplicated: [{ choose: R('y', 'y', '1h', 'yes'), resched: NONE, uc: NONE },
        { choose: R('y', 'y', '1h', 'yes'), resched: R('y', 'y', '1h', 'yes'), uc: NONE },
        { choose: R('y', 'y', '2h', 'no'), resched: R('y', 'y', '1h', 'yes'), uc: NONE },
        { choose: R('y', 'y', '2h', 'no'), resched: R('y', 'y', '1h', 'yes'), uc: NONE }],
      shared: [{ choose: USE('yes'), resched: NONE, uc: R('y', 'y', '1h', '-') },
        { choose: USE('yes'), resched: USE('yes'), uc: R('y', 'y', '1h', '-') },
        { choose: USE('no'), resched: USE('no'), uc: R('y', 'y', '2h', '-') },
        { choose: USE('no'), resched: USE('no'), uc: R('y', 'y', '2h', '-') }],
      passthrough: [{ choose: NONE, resched: NONE, uc: R('fwd', 'fwd', 'fwd', '-') },
        { choose: R('use', 'use', 'use', '-'), resched: NONE, uc: R('fwd', 'fwd', 'fwd', '-') },
        { choose: R('use', 'use', 'use', '-'), resched: NONE, uc: R('fwd', 'fwd', 'fwd', '-') },
        { choose: NONE, resched: NONE, uc: NONE }]
    };
    // đường đi trong cây quyết định: reuse (dùng lại ở nhiều nơi?), complex (phức tạp, gộp nhiều repository?) -> lá
    var PATH = { duplicated: { reuse: 'yes', leaf: 'useCase' }, shared: { reuse: 'yes', leaf: 'useCase' }, passthrough: { reuse: 'no', complex: 'no', leaf: 'none' } };
    var MET = {
      duplicated: [{ copies: 1, agree: 'na', extra: 0 }, { copies: 2, agree: 'yes', extra: 0 }, { copies: 2, agree: 'no', extra: 0 }, { copies: 2, agree: 'no', extra: 0 }],
      shared: [{ copies: 1, agree: 'na', extra: 0 }, { copies: 1, agree: 'yes', extra: 0 }, { copies: 1, agree: 'yes', extra: 0 }, { copies: 1, agree: 'yes', extra: 0 }],
      passthrough: [{ copies: 0, agree: 'na', extra: 1 }, { copies: 0, agree: 'na', extra: 1 }, { copies: 0, agree: 'na', extra: 1 }, { copies: 0, agree: 'na', extra: 0 }]
    };
    var STEP = {   // [node sáng, trạng thái node, loại bước, dòng mã, loại log, chủ thể, tín hiệu]
      duplicated: [[['choose', 'repo'], { choose: 'done', resched: 'skipped', uc: 'skipped', repo: 'done' }, 'scenario', [1, 2], 'write', 'choose', [{ edge: 'e4', tok: 'signal' }]],
        [['resched', 'repo'], { choose: 'done', resched: 'done', uc: 'skipped', repo: 'done' }, 'mechanism', [4, 5], 'write', 'resched', [{ edge: 'e5', tok: 'signal' }]],
        [['choose', 'resched'], { choose: 'done', resched: 'surprise', uc: 'skipped', repo: 'done' }, 'pitfall', [2, 5], 'write', 'choose', []],
        [['choose', 'resched'], { choose: 'done', resched: 'surprise', uc: 'skipped', repo: 'done' }, 'pitfall', [7], 'observe', 'resched', []]],
      shared: [[['uc', 'choose'], { choose: 'done', resched: 'skipped', uc: 'done', repo: 'done' }, 'scenario', [1, 2, 3, 5], 'write', 'uc', [{ edge: 'e1', tok: 'signal' }]],
        [['choose', 'resched', 'uc'], { choose: 'done', resched: 'done', uc: 'done', repo: 'done' }, 'mechanism', [5, 6], 'write', 'resched', [{ edge: 'e1', tok: 'signal' }, { edge: 'e2', tok: 'signal' }]],
        [['uc'], { choose: 'done', resched: 'done', uc: 'done', repo: 'done' }, 'mechanism', [3], 'write', 'uc', []],
        [['uc', 'choose', 'resched'], { choose: 'done', resched: 'done', uc: 'done', repo: 'done' }, 'mechanism', [7, 8], 'complete', 'uc', [{ edge: 'e1', tok: 'state', reverse: true }, { edge: 'e2', tok: 'state', reverse: true }]]],
      passthrough: [[['uc', 'repo'], { choose: 'skipped', resched: 'skipped', uc: 'surprise', repo: 'done' }, 'scenario', [1, 2, 3], 'write', 'uc', [{ edge: 'e3', tok: 'signal' }]],
        [['choose', 'uc', 'repo'], { choose: 'done', resched: 'skipped', uc: 'surprise', repo: 'done' }, 'pitfall', [4], 'run', 'choose', [{ edge: 'e1', tok: 'signal' }, { edge: 'e3', tok: 'signal' }]],
        [['uc'], { choose: 'done', resched: 'skipped', uc: 'surprise', repo: 'done' }, 'mechanism', [1, 4], 'observe', 'uc', []],
        [['choose', 'repo'], { choose: 'done', resched: 'skipped', uc: 'skipped', repo: 'done' }, 'mechanism', [5, 6], 'complete', 'choose', [{ edge: 'e4', tok: 'signal' }]]]
    };
    ADE.archUseCase = { COLS: COLS, ROWS: ['past', 'hours', 'lead', 'ans'], at: function (c, i) { return T[c][i]; }, path: function (c) { return PATH[c]; } };
    function steps(s) {
      return STEP[s.case].map(function (p, i) {
        var ns = {}; Object.keys(p[1]).forEach(function (n) { ns[n] = K + 'st.' + p[1][n]; });
        var x = MET[s.case][i];
        var o = S(m, s.case + '.' + KS[i], { type: p[2], activeNodes: p[0], nodeStates: ns,
          metrics: { copies: x.copies, agree: M(m, 'agree.' + x.agree), extra: x.extra },
          codeHighlight: { snippet: 'g5.' + s.case, lines: p[3] }, movingSignals: p[6], logEvents: [{ t: i, kind: p[4], subject: p[5] }] });
        o.callouts = [{ kind: i === 0 ? 'try' : (p[2] === 'pitfall' ? 'pitfall' : 'source'), textKey: i === 0 ? M(m, 'co.try') : M(m, 'co.' + s.case + '.' + KS[i]) }];
        return o;
      });
    }
    reg(m, { controls: [sel(m, 'case', CASES)], init: function () { return { case: 'duplicated' }; }, act: setter(['case']), steps: steps,
      selfChecks: [
        { name: 'mỗi tình huống có 4 bước', run: function () { return CASES.every(function (k) { return steps({ case: k }).length === 4; }); } },
        { name: 'quy tắc chép ở hai ViewModel: đổi một chỗ thì hai màn trả lời khác nhau', run: function () { var t = ADE.archUseCase.at('duplicated', 3); return t.choose.ans !== t.resched.ans && steps({ case: 'duplicated' })[3].metrics.agree === M(m, 'agree.no'); } },
        { name: 'dùng chung một use case: một chỗ viết, hai màn cùng đáp án', run: function () { var t = ADE.archUseCase.at('shared', 3); return t.choose.ans === t.resched.ans && steps({ case: 'shared' })[3].metrics.copies === 1; } },
        { name: 'use case chỉ chuyển tiếp: bỏ đi thì bớt một lớp, không mất quy tắc nào', run: function () { var a = steps({ case: 'passthrough' }); return a[0].metrics.extra === 1 && a[3].metrics.extra === 0 && ADE.archUseCase.path('passthrough').leaf === 'none'; } }] });
  })();
  /* ================= G6: dependency injection thủ công và Hilt; scope và vòng đời =================
     Theo Dependency injection in Android (DI giúp dùng lại, refactor, test; Hilt kiểm phụ thuộc lúc biên dịch), Manual DI (container
     dùng chung đặt trong Application, không phải singleton kiểu object), Hilt (component theo lớp Android và vòng đời của chúng;
     binding mặc định không scope: mỗi lần yêu cầu là một instance mới; binding có scope tạo một lần cho mỗi instance component;
     binding mặc định: SingletonComponent có Application, ActivityComponent có Application và Activity; @ApplicationContext).
     Ô và mũi tên của hình "Sơ đồ phạm vi" lấy từ ADE.archDi. */
  (function () {
    var m = 'di', CASES = ['manual', 'hilt', 'leak'], KS = ['s1', 's2', 's3', 's4'];
    // ô: [id, mã nhãn, dải (app | vm | act), hàng, kiểu ('', 'bad', 'dim')]; mũi tên: [từ, tới, kiểu ('', 'bad', 'err')]
    var O = function (id, k, band, row, cls) { return { id: id, k: k, band: band, row: row, cls: cls || '' }; };
    var A = function (f, t, cls) { return { from: f, to: t, cls: cls || '' }; };
    var D = {
      manual: [
        { o: [O('vm1', 'vmChoose', 'vm', 0), O('repo1', 'repo1', 'vm', 1), O('db1', 'db1', 'vm', 2)], a: [A('vm1', 'repo1'), A('repo1', 'db1')] },
        { o: [O('vm1', 'vmChoose', 'vm', 0), O('repo1', 'repo1', 'vm', 1), O('db1', 'db1', 'vm', 2), O('vm2', 'vmResched', 'vm', 3), O('repo2', 'repo2', 'vm', 4), O('db2', 'db2', 'vm', 5)], a: [A('vm1', 'repo1'), A('repo1', 'db1'), A('vm2', 'repo2'), A('repo2', 'db2')] },
        { o: [O('vm1', 'vmChoose', 'vm', 0), O('repo1', 'repo1Fresh', 'vm', 1), O('db1', 'db1', 'vm', 2), O('vm2', 'vmResched', 'vm', 3), O('repo2', 'repo2Stale', 'vm', 4, 'bad'), O('db2', 'db2', 'vm', 5)], a: [A('vm1', 'repo1'), A('repo1', 'db1'), A('vm2', 'repo2'), A('repo2', 'db2')] },
        { o: [O('cont', 'appContainer', 'app', 0), O('repo', 'repoShared', 'app', 1), O('db', 'dbShared', 'app', 2), O('vm1', 'vmChoose', 'vm', 0), O('vm2', 'vmResched', 'vm', 1)], a: [A('cont', 'repo'), A('repo', 'db'), A('vm1', 'repo'), A('vm2', 'repo')] }],
      hilt: [
        { o: [O('app', 'hiltApp', 'app', 0), O('repo', 'repoSingleton', 'app', 1), O('db', 'dbShared', 'app', 2)], a: [A('repo', 'db')] },
        { o: [O('app', 'hiltApp', 'app', 0), O('repo', 'repoSingleton', 'app', 1), O('db', 'dbShared', 'app', 2), O('vm1', 'vmChooseHilt', 'vm', 0)], a: [A('repo', 'db'), A('vm1', 'repo')] },
        { o: [O('app', 'hiltApp', 'app', 0), O('repo', 'repoSingleton', 'app', 1), O('db', 'dbShared', 'app', 2), O('vm1', 'vmChooseHilt', 'vm', 0), O('vm2', 'vmReschedHilt', 'vm', 1)], a: [A('repo', 'db'), A('vm1', 'repo'), A('vm2', 'repo')] },
        { o: [O('app', 'hiltApp', 'app', 0), O('repo', 'repoSingleton', 'app', 1), O('db', 'dbShared', 'app', 2), O('vm1', 'vmChooseHilt', 'vm', 0), O('vm2', 'vmReschedHilt', 'vm', 1), O('act', 'actEntry', 'act', 0)], a: [A('repo', 'db'), A('vm1', 'repo'), A('vm2', 'repo'), A('act', 'vm1')] }],
      leak: [
        { o: [O('cont', 'objectContainer', 'app', 0), O('repo', 'repoCtx', 'app', 1, 'bad'), O('act1', 'act1', 'act', 0)], a: [A('cont', 'repo'), A('repo', 'act1', 'bad')] },
        { o: [O('cont', 'objectContainer', 'app', 0), O('repo', 'repoCtx', 'app', 1, 'bad'), O('act1', 'act1Dead', 'act', 0, 'bad'), O('act2', 'act2', 'act', 1)], a: [A('cont', 'repo'), A('repo', 'act1', 'bad')] },
        { o: [O('appCtx', 'application', 'app', 0), O('repo', 'repoAppCtx', 'app', 1), O('act2', 'act2', 'act', 1)], a: [A('repo', 'appCtx')] },
        { o: [O('appCtx', 'application', 'app', 0), O('repo', 'repoActInject', 'app', 1, 'bad'), O('act2', 'act2', 'act', 1)], a: [A('repo', 'appCtx'), A('repo', 'act2', 'err')] }]
    };
    var MET = {   // {inst: số instance SlotRepository, hold: giữ Activity đã hủy, when: lỗi lộ ra lúc}
      manual: [{ inst: 1, hold: 'no', when: 'na' }, { inst: 2, hold: 'no', when: 'na' }, { inst: 2, hold: 'no', when: 'runtime' }, { inst: 1, hold: 'no', when: 'na' }],
      hilt: [{ inst: 1, hold: 'no', when: 'na' }, { inst: 1, hold: 'no', when: 'na' }, { inst: 1, hold: 'no', when: 'na' }, { inst: 1, hold: 'no', when: 'na' }],
      leak: [{ inst: 1, hold: 'no', when: 'na' }, { inst: 1, hold: 'yes', when: 'runtime' }, { inst: 1, hold: 'no', when: 'na' }, { inst: 1, hold: 'no', when: 'compile' }]
    };
    var STEP = {   // [node sáng, trạng thái node, loại bước, dòng mã, loại log, chủ thể, tín hiệu]
      manual: [[['vm', 'repo'], { act: 'done', vm: 'done', repo: 'done', db: 'done' }, 'scenario', [1, 2], 'write', 'vm', [{ edge: 'e2', tok: 'signal' }]],
        [['vm', 'repo', 'db'], { act: 'done', vm: 'done', repo: 'surprise', db: 'surprise' }, 'pitfall', [3, 4], 'write', 'repo', [{ edge: 'e2', tok: 'signal' }, { edge: 'e3', tok: 'signal' }]],
        [['repo'], { act: 'done', vm: 'done', repo: 'surprise', db: 'done' }, 'pitfall', [5], 'observe', 'repo', []],
        [['repo', 'vm'], { act: 'done', vm: 'done', repo: 'done', db: 'done' }, 'mechanism', [6, 7, 8], 'complete', 'repo', [{ edge: 'e2', tok: 'signal' }]]],
      hilt: [[['repo', 'db'], { act: 'done', vm: 'done', repo: 'done', db: 'done' }, 'scenario', [1, 2, 3], 'write', 'repo', []],
        [['vm', 'repo'], { act: 'done', vm: 'done', repo: 'done', db: 'done' }, 'mechanism', [4, 5], 'run', 'vm', [{ edge: 'e2', tok: 'signal' }]],
        [['vm', 'repo'], { act: 'done', vm: 'done', repo: 'done', db: 'done' }, 'mechanism', [5, 6], 'run', 'vm', [{ edge: 'e2', tok: 'signal' }]],
        [['act', 'vm', 'repo'], { act: 'done', vm: 'done', repo: 'done', db: 'done' }, 'mechanism', [7, 8], 'complete', 'act', [{ edge: 'e1', tok: 'signal' }, { edge: 'e2', tok: 'signal' }]]],
      leak: [[['repo', 'act'], { act: 'done', vm: 'skipped', repo: 'surprise', db: 'done' }, 'scenario', [1, 2, 3], 'write', 'act', [{ edge: 'e4', tok: 'signal' }]],
        [['act', 'repo'], { act: 'surprise', vm: 'skipped', repo: 'surprise', db: 'done' }, 'pitfall', [4], 'observe', 'act', []],
        [['repo'], { act: 'done', vm: 'skipped', repo: 'done', db: 'done' }, 'mechanism', [5, 6], 'write', 'repo', []],
        [['repo', 'act'], { act: 'done', vm: 'skipped', repo: 'broken', db: 'done' }, 'mechanism', [7, 8], 'exception', 'repo', []]]
    };
    ADE.archDi = { at: function (c, i) { return D[c][i]; } };
    function steps(s) {
      return STEP[s.case].map(function (p, i) {
        var ns = {}; Object.keys(p[1]).forEach(function (n) { ns[n] = K + 'st.' + p[1][n]; });
        var x = MET[s.case][i];
        var o = S(m, s.case + '.' + KS[i], { type: p[2], activeNodes: p[0], nodeStates: ns,
          metrics: { inst: x.inst, hold: M(m, 'hold.' + x.hold), when: M(m, 'when.' + x.when) },
          codeHighlight: { snippet: 'g6.' + s.case, lines: p[3] }, movingSignals: p[6], logEvents: [{ t: i, kind: p[4], subject: p[5] }] });
        o.callouts = [{ kind: i === 0 ? 'try' : (p[2] === 'pitfall' ? 'pitfall' : 'source'), textKey: i === 0 ? M(m, 'co.try') : M(m, 'co.' + s.case + '.' + KS[i]) }];
        return o;
      });
    }
    reg(m, { controls: [sel(m, 'case', CASES)], init: function () { return { case: 'manual' }; }, act: setter(['case']), steps: steps,
      simpExtra: [M(m, 'simp.2')],
      selfChecks: [
        { name: 'mỗi tình huống có 4 bước', run: function () { return CASES.every(function (k) { return steps({ case: k }).length === 4; }); } },
        { name: 'mỗi ViewModel tự tạo repository: hai instance; container dùng chung: một', run: function () { var a = steps({ case: 'manual' }); return a[1].metrics.inst === 2 && a[3].metrics.inst === 1; } },
        { name: 'Hilt @Singleton: hai ViewModel nhận cùng một instance', run: function () { return steps({ case: 'hilt' }).every(function (s) { return s.metrics.inst === 1; }); } },
        { name: 'singleton giữ Activity: sau khi xoay vẫn giữ Activity đã hủy; @ApplicationContext thì không', run: function () { var a = steps({ case: 'leak' }); return a[1].metrics.hold === M(m, 'hold.yes') && a[2].metrics.hold === M(m, 'hold.no'); } },
        { name: 'mũi tên đỏ chỉ đi từ dải sống lâu hơn sang dải sống ngắn hơn', run: function () {
          var rank = { app: 0, vm: 1, act: 2 };
          return CASES.every(function (c) { return [0, 1, 2, 3].every(function (i) { var d = D[c][i], band = {}; d.o.forEach(function (x) { band[x.id] = x.band; });
            return d.a.every(function (x) { return x.cls === '' ? rank[band[x.from]] >= rank[band[x.to]] : rank[band[x.from]] < rank[band[x.to]]; }); }); }); } }] });
  })();
  /* ================= G7: MVVM và MVI: một trạng thái duy nhất =================
     Theo UI layer (dùng một UI state cho các state liên quan nhau để tránh lệch; một luồng hay nhiều luồng tùy quan hệ giữa các
     phần), Dumbravan ch.8 (MVVM: View phụ thuộc ViewModel, ViewModel phụ thuộc Model, quan sát được) và ch.9 (MVI: dữ liệu bất biến
     gộp thành một state; intent đổi state qua một luồng dữ liệu phản ứng; MVI xây trên ViewModel, không thay nó).
     Ba bit của tổ hợp: L = đang tải, E = có lỗi, D = có dữ liệu. Hợp lệ (theo màn Lịch của tôi): 000, 100, 101, 001, 010. */
  (function () {
    var m = 'mvi', CASES = ['streams', 'single', 'mvi'], KS = ['s1', 's2', 's3', 's4'];
    var COMBOS = ['000', '100', '101', '001', '010', '110', '111', '011'];
    var VALID = { '000': 1, '100': 1, '101': 1, '001': 1, '010': 1 };
    var SEEN = { streams: ['100', '110', '011', '111'], single: ['100', '010', '100', '001'], mvi: ['100', '010', '100', '001'] };
    var REPR = { streams: 8, single: 8, mvi: 4 };
    var SEALED = { '100': 1, '101': 1, '001': 1, '010': 1 };   // Loading, Refreshing, Content, Error
    ADE.archMvi = { COMBOS: COMBOS, valid: function (c) { return !!VALID[c]; }, inSealed: function (c) { return !!SEALED[c]; }, seen: function (c, i) { return SEEN[c].slice(0, i + 1); }, repr: function (c) { return REPR[c]; } };
    var STEP = {   // [node sáng, trạng thái node, loại bước, dòng mã, loại log, chủ thể, tín hiệu]
      streams: [[['ui', 'vm', 'state'], { ui: 'done', vm: 'done', state: 'done' }, 'scenario', [1, 5], 'write', 'vm', [{ edge: 'e1', tok: 'signal' }, { edge: 'e2', tok: 'state' }]],
        [['vm', 'state', 'ui'], { ui: 'surprise', vm: 'done', state: 'surprise' }, 'pitfall', [7], 'exception', 'vm', [{ edge: 'e2', tok: 'state' }, { edge: 'e3', tok: 'state' }]],
        [['vm', 'state', 'ui'], { ui: 'surprise', vm: 'done', state: 'surprise' }, 'pitfall', [2, 6], 'write', 'vm', [{ edge: 'e1', tok: 'signal' }, { edge: 'e3', tok: 'state' }]],
        [['state', 'ui'], { ui: 'surprise', vm: 'done', state: 'surprise' }, 'pitfall', [1, 2, 5], 'observe', 'ui', [{ edge: 'e3', tok: 'state' }]]],
      single: [[['ui', 'vm', 'state'], { ui: 'done', vm: 'done', state: 'done' }, 'scenario', [1, 2, 4], 'write', 'vm', [{ edge: 'e1', tok: 'signal' }, { edge: 'e2', tok: 'state' }]],
        [['vm', 'state', 'ui'], { ui: 'done', vm: 'done', state: 'done' }, 'mechanism', [5, 6], 'exception', 'vm', [{ edge: 'e2', tok: 'state' }, { edge: 'e3', tok: 'state' }]],
        [['ui', 'vm'], { ui: 'done', vm: 'done', state: 'done' }, 'mechanism', [4], 'write', 'ui', [{ edge: 'e1', tok: 'signal' }]],
        [['vm', 'state', 'ui'], { ui: 'done', vm: 'done', state: 'surprise' }, 'mechanism', [6, 7], 'complete', 'state', [{ edge: 'e3', tok: 'state' }]]],
      mvi: [[['ui', 'vm'], { ui: 'done', vm: 'done', state: 'done' }, 'scenario', [3, 8], 'write', 'ui', [{ edge: 'e1', tok: 'signal' }]],
        [['vm', 'state'], { ui: 'done', vm: 'done', state: 'done' }, 'mechanism', [4, 5, 7, 9], 'exception', 'vm', [{ edge: 'e2', tok: 'state' }]],
        [['ui', 'vm'], { ui: 'done', vm: 'done', state: 'done' }, 'mechanism', [3, 8], 'write', 'ui', [{ edge: 'e1', tok: 'signal' }]],
        [['vm', 'state', 'ui'], { ui: 'done', vm: 'done', state: 'done' }, 'mechanism', [1, 2, 6], 'complete', 'state', [{ edge: 'e2', tok: 'state' }, { edge: 'e3', tok: 'state' }]]]
    };
    var STREAMS = { streams: 3, single: 1, mvi: 1 };
    function steps(s) {
      return STEP[s.case].map(function (p, i) {
        var ns = {}; Object.keys(p[1]).forEach(function (n) { ns[n] = K + 'st.' + p[1][n]; });
        var bad = ADE.archMvi.seen(s.case, i).filter(function (c) { return !VALID[c]; }).length;
        var o = S(m, s.case + '.' + KS[i], { type: p[2], activeNodes: p[0], nodeStates: ns,
          metrics: { streams: STREAMS[s.case], bad: bad, repr: REPR[s.case] },
          codeHighlight: { snippet: 'g7.' + s.case, lines: p[3] }, movingSignals: p[6], logEvents: [{ t: i, kind: p[4], subject: p[5] }] });
        o.callouts = [{ kind: i === 0 ? 'try' : (p[2] === 'pitfall' ? 'pitfall' : 'source'), textKey: i === 0 ? M(m, 'co.try') : M(m, 'co.' + s.case + '.' + KS[i]) }];
        return o;
      });
    }
    reg(m, { controls: [sel(m, 'case', CASES)], init: function () { return { case: 'streams' }; }, act: setter(['case']), steps: steps,
      selfChecks: [
        { name: 'mỗi tình huống có 4 bước', run: function () { return CASES.every(function (k) { return steps({ case: k }).length === 4; }); } },
        { name: 'ba luồng riêng: tổ hợp sai xuất hiện (đang tải cùng lỗi)', run: function () { return steps({ case: 'streams' })[3].metrics.bad >= 2 && SEEN.streams.indexOf('110') >= 0; } },
        { name: 'một UiState: không tổ hợp sai trong kịch bản, nhưng kiểu vẫn biểu diễn được 8 tổ hợp', run: function () { var x = steps({ case: 'single' })[3].metrics; return x.bad === 0 && x.repr === 8; } },
        { name: 'MVI với sealed state: chỉ 4 trạng thái biểu diễn được, đều hợp lệ', run: function () { var x = steps({ case: 'mvi' })[3].metrics; return x.bad === 0 && x.repr === 4; } }] });
  })();
  /* ================= G8: lỗi đi qua các tầng =================
     Theo Data layer (tầng data hiểu các loại lỗi và lộ chúng bằng ngoại lệ riêng hay kiểu Result), UI layer (lỗi trên màn hình là
     state có kèm thông điệp và hành động thử lại), Boudjnah ch.6 (failure: dự đoán được, phục hồi được, xử lý như giá trị bằng sealed
     class; exception: bất ngờ, không có cách phục hồi rõ, ghi log và theo dõi). Bảng ánh xạ của hình lấy từ ADE.archFailure. */
  (function () {
    var m = 'failure', CASES = ['raw', 'mapped', 'swallow'], KS = ['s1', 's2', 's3', 's4'];
    var ROWS = ['io', 'conflict', 'server', 'cancel', 'bug'];
    // mỗi hàng: [repository, ViewModel, người dùng thấy, kiểu ô người dùng ('', 'bad')]
    var MAP = {
      raw: { io: ['rethrow', 'noCatch', 'crash', 'bad'], server: ['rethrow', 'catchAllMsg', 'http500', 'bad'], conflict: ['rethrow', 'catchAllMsg', 'http409', 'bad'], bug: ['rethrow', 'catchAllMsg', 'nullText', 'bad'] },
      mapped: { io: ['toOffline', 'msgFor', 'offlineMsg', ''], conflict: ['toTaken', 'msgFor', 'takenMsg', ''], server: ['toServer', 'msgFor', 'serverMsg', ''], bug: ['notCaught', 'notCaught', 'crashReport', ''] },
      swallow: { io: ['emptyList', 'showsList', 'noSlots', 'bad'], conflict: ['returnFalse', 'genericFail', 'genericMsg', 'bad'], cancel: ['caughtCancel', 'keepsRunning', 'afterLeave', 'bad'], bug: ['emptyList', 'showsList', 'silent', 'bad'] }
    };
    var ORDER = { raw: ['io', 'server', 'conflict', 'bug'], mapped: ['io', 'conflict', 'server', 'bug'], swallow: ['io', 'conflict', 'cancel', 'bug'] };
    ADE.archFailure = { ROWS: ROWS, order: function (c) { return ORDER[c]; }, cell: function (c, r) { return MAP[c][r] || null; } };
    var MET = {   // {crash, text: lộ chữ kỹ thuật, hidden: lỗi bị giấu}
      raw: [{ crash: 'yes', text: 'no', hidden: 'no' }, { crash: 'no', text: 'yes', hidden: 'no' }, { crash: 'no', text: 'yes', hidden: 'no' }, { crash: 'no', text: 'yes', hidden: 'yes' }],
      mapped: [{ crash: 'no', text: 'no', hidden: 'no' }, { crash: 'no', text: 'no', hidden: 'no' }, { crash: 'no', text: 'no', hidden: 'no' }, { crash: 'report', text: 'no', hidden: 'no' }],
      swallow: [{ crash: 'no', text: 'no', hidden: 'yes' }, { crash: 'no', text: 'no', hidden: 'yes' }, { crash: 'no', text: 'no', hidden: 'yes' }, { crash: 'no', text: 'no', hidden: 'yes' }]
    };
    var STEP = {   // [node sáng, trạng thái node, loại bước, dòng mã, loại log, chủ thể, tín hiệu]
      raw: [[['source', 'repo', 'vm', 'ui'], { source: 'broken', repo: 'done', vm: 'surprise', ui: 'broken' }, 'pitfall', [1, 2, 3], 'exception', 'source', [{ edge: 'e3', tok: 'error', reverse: true }, { edge: 'e2', tok: 'error', reverse: true }, { edge: 'e1', tok: 'error', reverse: true }]],
        [['vm', 'ui'], { source: 'broken', repo: 'done', vm: 'surprise', ui: 'surprise' }, 'pitfall', [5, 6], 'exception', 'vm', [{ edge: 'e1', tok: 'error', reverse: true }]],
        [['vm', 'ui'], { source: 'broken', repo: 'done', vm: 'surprise', ui: 'surprise' }, 'pitfall', [6, 7], 'exception', 'vm', [{ edge: 'e1', tok: 'error', reverse: true }]],
        [['vm', 'ui'], { source: 'broken', repo: 'done', vm: 'surprise', ui: 'surprise' }, 'pitfall', [6, 7], 'exception', 'vm', [{ edge: 'e1', tok: 'error', reverse: true }]]],
      mapped: [[['source', 'repo'], { source: 'broken', repo: 'done', vm: 'done', ui: 'done' }, 'scenario', [1, 2, 3, 4], 'exception', 'source', [{ edge: 'e3', tok: 'error', reverse: true }, { edge: 'e2', tok: 'state', reverse: true }]],
        [['repo', 'vm', 'ui'], { source: 'broken', repo: 'done', vm: 'done', ui: 'done' }, 'mechanism', [5, 7], 'run', 'repo', [{ edge: 'e2', tok: 'state', reverse: true }, { edge: 'e1', tok: 'state', reverse: true }]],
        [['repo', 'vm', 'ui'], { source: 'broken', repo: 'done', vm: 'done', ui: 'done' }, 'mechanism', [5, 6, 7], 'run', 'vm', [{ edge: 'e1', tok: 'state', reverse: true }]],
        [['source', 'repo'], { source: 'broken', repo: 'done', vm: 'done', ui: 'done' }, 'mechanism', [8], 'exception', 'source', [{ edge: 'e3', tok: 'error', reverse: true }]]],
      swallow: [[['repo', 'ui'], { source: 'broken', repo: 'surprise', vm: 'done', ui: 'surprise' }, 'pitfall', [1, 2], 'skip', 'repo', [{ edge: 'e2', tok: 'state', reverse: true }]],
        [['repo', 'ui'], { source: 'broken', repo: 'surprise', vm: 'done', ui: 'surprise' }, 'pitfall', [3], 'skip', 'repo', [{ edge: 'e2', tok: 'state', reverse: true }]],
        [['repo', 'vm'], { source: 'done', repo: 'surprise', vm: 'surprise', ui: 'skipped' }, 'pitfall', [3, 4, 5], 'skip', 'repo', []],
        [['source', 'repo'], { source: 'broken', repo: 'surprise', vm: 'done', ui: 'surprise' }, 'pitfall', [1, 2, 6], 'skip', 'repo', []]]
    };
    function steps(s) {
      return STEP[s.case].map(function (p, i) {
        var ns = {}; Object.keys(p[1]).forEach(function (n) { ns[n] = K + 'st.' + p[1][n]; });
        var x = MET[s.case][i];
        var o = S(m, s.case + '.' + KS[i], { type: p[2], activeNodes: p[0], nodeStates: ns,
          metrics: { crash: M(m, 'crash.' + x.crash), text: M(m, 'yn.' + x.text), hidden: M(m, 'yn.' + x.hidden) },
          codeHighlight: { snippet: 'g8.' + s.case, lines: p[3] }, movingSignals: p[6], logEvents: [{ t: i, kind: p[4], subject: p[5] }] });
        o.callouts = [{ kind: i === 0 ? 'try' : (p[2] === 'pitfall' ? 'pitfall' : 'source'), textKey: i === 0 ? M(m, 'co.try') : M(m, 'co.' + s.case + '.' + KS[i]) }];
        return o;
      });
    }
    reg(m, { controls: [sel(m, 'case', CASES)], init: function () { return { case: 'raw' }; }, act: setter(['case']), steps: steps,
      selfChecks: [
        { name: 'mỗi tình huống có 4 bước', run: function () { return CASES.every(function (k) { return steps({ case: k }).length === 4; }); } },
        { name: 'không bắt: mất mạng làm crash; bắt tất cả rồi hiện message: lộ chữ kỹ thuật', run: function () { var a = steps({ case: 'raw' }); return a[0].metrics.crash === M(m, 'crash.yes') && a[1].metrics.text === M(m, 'yn.yes'); } },
        { name: 'ánh xạ ở repository: không crash, không lộ chữ kỹ thuật; lỗi lập trình vẫn được báo', run: function () { var a = steps({ case: 'mapped' }); return a.every(function (s) { return s.metrics.text === M(m, 'yn.no'); }) && a[3].metrics.crash === M(m, 'crash.report'); } },
        { name: 'bắt Exception rộng: mọi lỗi bị giấu, kể cả hủy coroutine', run: function () { return steps({ case: 'swallow' }).every(function (s) { return s.metrics.hidden === M(m, 'yn.yes'); }) && ORDER.swallow.indexOf('cancel') >= 0; } }] });
  })();
  /* ================= G9: module hóa: đồ thị module =================
     Theo Guide to Android app modularization (kiểm soát chặt phần lộ ra bằng internal/private) và Common modularization patterns
     (feature module phụ thuộc data module; app module là điểm vào, giữ điều hướng gốc; hai module không gọi thẳng nhau được khi thành
     vòng, cần module trung gian, thường là app module giữ navigation graph; truyền id chứ không truyền object; lộ ít nhất có thể,
     ưu tiên implementation hơn api; module cao và module cài đặt cùng phụ thuộc module trừu tượng).
     Node, cạnh và khung của hình "Đồ thị module" lấy từ ADE.archModules. */
  (function () {
    var m = 'modules', CASES = ['features', 'visibility', 'abstraction'], KS = ['s1', 's2', 's3', 's4'];
    var N = function (id, k, x, y, cls) { return { id: id, k: k, x: x, y: y, cls: cls || '' }; };
    var E = function (f, t, cls) { return { from: f, to: t, cls: cls || '' }; };
    var APP = N('app', 'app', 270, 40), BOOK = N('book', 'book', 115, 140), HIST = N('hist', 'hist', 425, 140), DATA = N('data', 'data', 270, 250);
    var BASE = [E('app', 'book'), E('app', 'hist'), E('book', 'data'), E('hist', 'data')];
    var G = {
      features: [
        { n: [APP, BOOK, HIST, DATA], e: BASE, g: [], build: 'pass' },
        { n: [APP, N('book', 'book', 115, 140, 'bad'), HIST, DATA], e: BASE.concat([E('book', 'hist', 'bad')]), g: [], build: 'pass' },
        { n: [APP, N('book', 'book', 115, 140, 'bad'), N('hist', 'hist', 425, 140, 'bad'), DATA], e: BASE.concat([E('book', 'hist', 'bad'), E('hist', 'book', 'err')]), g: [], build: 'cycle' },
        { n: [N('app', 'appNav', 270, 40), BOOK, HIST, DATA], e: BASE, g: [], build: 'pass' }],
      visibility: [
        { n: [N('book', 'book', 140, 60), N('repo', 'repoPublic', 340, 170), N('dao', 'daoPublic', 340, 270)], e: [E('book', 'repo'), E('repo', 'dao')], g: [['dataBox', 220, 128, 300, 182]], build: 'pass' },
        { n: [N('book', 'book', 140, 60, 'bad'), N('repo', 'repoPublic', 340, 170), N('dao', 'daoPublic', 340, 270, 'bad')], e: [E('book', 'repo'), E('repo', 'dao'), E('book', 'dao', 'bad')], g: [['dataBox', 220, 128, 300, 182]], build: 'pass' },
        { n: [N('book', 'book', 140, 60, 'bad'), N('repo', 'repoPublic', 340, 170), N('dao', 'daoInternal', 340, 270)], e: [E('book', 'repo'), E('repo', 'dao'), E('book', 'dao', 'err')], g: [['dataBox', 220, 128, 300, 182]], build: 'internal' },
        { n: [N('book', 'book', 140, 60), N('repo', 'repoPublic', 340, 170), N('dao', 'daoInternal', 340, 270)], e: [E('book', 'repo'), E('repo', 'dao')], g: [['dataBox', 220, 128, 300, 182]], build: 'pass' }],
      abstraction: [
        { n: [APP, BOOK, N('data', 'dataAll', 140, 250, 'bad')], e: [E('app', 'book'), E('book', 'data', 'bad')], g: [], build: 'pass' },
        { n: [APP, BOOK, N('api', 'dataApi', 140, 250), N('impl', 'dataImpl', 400, 250)], e: [E('app', 'book'), E('book', 'impl', 'bad'), E('impl', 'api')], g: [], build: 'pass' },
        { n: [APP, BOOK, N('api', 'dataApi', 140, 250), N('impl', 'dataImpl', 400, 250)], e: [E('app', 'book'), E('app', 'impl'), E('book', 'api'), E('impl', 'api')], g: [], build: 'pass' },
        { n: [APP, BOOK, N('api', 'dataApi', 140, 250), N('impl', 'dataImplChanged', 400, 250, 'hl')], e: [E('app', 'book'), E('app', 'impl'), E('book', 'api'), E('impl', 'api')], g: [], build: 'implOnly' }]
    };
    ADE.archModules = { at: function (c, i) { return G[c][i]; } };
    var MET = {   // {ff: số cạnh feature → feature, cycle, impl: feature dính chi tiết cài đặt}
      features: [{ ff: 0, cycle: 'no', impl: 'no' }, { ff: 1, cycle: 'no', impl: 'yes' }, { ff: 2, cycle: 'yes', impl: 'yes' }, { ff: 0, cycle: 'no', impl: 'no' }],
      visibility: [{ ff: 0, cycle: 'no', impl: 'no' }, { ff: 0, cycle: 'no', impl: 'yes' }, { ff: 0, cycle: 'no', impl: 'no' }, { ff: 0, cycle: 'no', impl: 'no' }],
      abstraction: [{ ff: 0, cycle: 'no', impl: 'yes' }, { ff: 0, cycle: 'no', impl: 'yes' }, { ff: 0, cycle: 'no', impl: 'no' }, { ff: 0, cycle: 'no', impl: 'no' }]
    };
    var STEP = {   // [node sáng, trạng thái node, loại bước, dòng mã, loại log, chủ thể]
      features: [[['app', 'feat', 'data'], { app: 'done', feat: 'done', data: 'done' }, 'scenario', [1, 2, 3], 'observe', 'app'],
        [['feat'], { app: 'done', feat: 'surprise', data: 'done' }, 'pitfall', [4], 'write', 'feat'],
        [['feat'], { app: 'done', feat: 'broken', data: 'done' }, 'pitfall', [5, 6], 'exception', 'feat'],
        [['app', 'feat'], { app: 'done', feat: 'done', data: 'done' }, 'mechanism', [7, 8], 'complete', 'app']],
      visibility: [[['feat', 'data'], { app: 'skipped', feat: 'done', data: 'done' }, 'scenario', [1, 2], 'observe', 'data'],
        [['feat', 'data'], { app: 'skipped', feat: 'surprise', data: 'surprise' }, 'pitfall', [3, 4], 'write', 'feat'],
        [['feat', 'data'], { app: 'skipped', feat: 'broken', data: 'done' }, 'mechanism', [5, 6], 'exception', 'feat'],
        [['feat', 'data'], { app: 'skipped', feat: 'done', data: 'done' }, 'mechanism', [1, 5, 7], 'complete', 'data']],
      abstraction: [[['feat', 'data'], { app: 'done', feat: 'surprise', data: 'surprise' }, 'scenario', [1, 2], 'observe', 'feat'],
        [['data'], { app: 'done', feat: 'surprise', data: 'done' }, 'mechanism', [3, 4], 'write', 'data'],
        [['app', 'feat', 'data'], { app: 'done', feat: 'done', data: 'done' }, 'mechanism', [5, 6], 'write', 'feat'],
        [['data'], { app: 'done', feat: 'done', data: 'done' }, 'mechanism', [7], 'complete', 'data']]
    };
    function steps(s) {
      return STEP[s.case].map(function (p, i) {
        var ns = {}; Object.keys(p[1]).forEach(function (n) { ns[n] = K + 'st.' + p[1][n]; });
        var x = MET[s.case][i];
        var o = S(m, s.case + '.' + KS[i], { type: p[2], activeNodes: p[0], nodeStates: ns,
          metrics: { ff: x.ff, cycle: M(m, 'yn.' + x.cycle), impl: M(m, 'yn.' + x.impl) },
          codeHighlight: { snippet: 'g9.' + s.case, lines: p[3] }, movingSignals: [{ edge: 'e1', tok: 'signal' }], logEvents: [{ t: i, kind: p[4], subject: p[5] }] });
        o.callouts = [{ kind: i === 0 ? 'try' : (p[2] === 'pitfall' ? 'pitfall' : 'source'), textKey: i === 0 ? M(m, 'co.try') : M(m, 'co.' + s.case + '.' + KS[i]) }];
        return o;
      });
    }
    reg(m, { controls: [sel(m, 'case', CASES)], init: function () { return { case: 'features' }; }, act: setter(['case']), steps: steps,
      simpExtra: [M(m, 'simp.2')],
      selfChecks: [
        { name: 'mỗi tình huống có 4 bước', run: function () { return CASES.every(function (k) { return steps({ case: k }).length === 4; }); } },
        { name: 'feature phụ thuộc feature theo hai chiều: Gradle từ chối vòng; app làm trung gian thì hết', run: function () { return G.features[2].build === 'cycle' && steps({ case: 'features' })[3].metrics.ff === 0; } },
        { name: 'đánh dấu internal: feature dùng DAO thành lỗi biên dịch', run: function () { return G.visibility[2].build === 'internal' && G.visibility[2].e.some(function (x) { return x.cls === 'err'; }); } },
        { name: 'module trừu tượng: feature chỉ phụ thuộc data-api, không phụ thuộc data-impl', run: function () { var e = G.abstraction[2].e; return e.some(function (x) { return x.from === 'book' && x.to === 'api'; }) && !e.some(function (x) { return x.from === 'book' && x.to === 'impl'; }); } }] });
  })();
})();
