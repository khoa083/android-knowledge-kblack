/* Model track H (thuần, không DOM, không câu chữ; chỉ message key). MÔ HÌNH GIẢNG DẠY (simplified).
   Nguồn: docs/research/storage.md (developer.android.com và mã AOSP đọc ngày 2026-11-24). */
(function () {
  'use strict';
  var K = 'track.storage.';
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
    ADE.registerModel('storage.' + m, def);
  }
  var sel = function (m, id, vals) { return { id: id, type: 'select', labelKey: M(m, 'ctl.' + id), get: function (s) { return s[id]; }, action: id, options: vals.map(function (v) { return { value: v, labelKey: M(m, 'ctl.' + id + '.' + v) }; }) }; };
  var setter = function (keys) { return function (s, a, v) { var n = {}; keys.forEach(function (k) { n[k] = s[k]; }); if (keys.indexOf(a) >= 0) n[a] = v; return n; }; };
  var nsOf = function (o) { var n = {}; Object.keys(o).forEach(function (k) { n[k] = K + 'st.' + o[k]; }); return n; };

  /* ================= H1: chọn nơi lưu theo loại dữ liệu — một cây quyết định bốn câu hỏi =================
     Theo Data and file storage overview (bốn lựa chọn, bảng so sánh, bốn câu hỏi khi chọn), App-specific storage
     (cache có thể bị hệ thống xóa khi thiếu dung lượng; file riêng bị xóa khi gỡ app), DataStore (dữ liệu nhỏ, không cập nhật
     từng phần hay ràng buộc tham chiếu; cần thì dùng Room). Thứ tự câu hỏi là của site: hỏi điều loại trừ được nhiều nhất trước.
     Cây là chuỗi: mỗi câu "có" kết thúc ở một lá, "không" đi xuống câu tiếp; hết câu thì là file riêng (filesDir). */
  (function () {
    var m = 'choose', CASES = ['appts', 'settings', 'photo', 'pdf', 'draft'];
    var Q = ['share', 'regen', 'kv', 'rows'];
    var YES = { share: 'media', regen: 'cache', kv: 'datastore', rows: 'room' }, LAST = 'files';
    var CH = { media: 'h8', cache: 'h2', datastore: 'h3', room: 'h4', files: 'h2' };
    // câu trả lời của từng loại dữ liệu theo thứ tự câu hỏi; dừng ở câu "có" đầu tiên
    var ANS = { appts: [0, 0, 0, 1], settings: [0, 0, 1], photo: [1], pdf: [0, 1], draft: [0, 0, 0, 0] };
    var PLACES = ['files', 'cache', 'datastore', 'room', 'media'];
    // thuộc tính theo bảng so sánh của trang Data and file storage overview: [app khác đọc được, còn sau khi gỡ app, hệ thống tự xóa khi thiếu chỗ]
    var PROPS = { files: ['no', 'no', 'no'], cache: ['no', 'no', 'yes'], datastore: ['no', 'no', 'no'], room: ['no', 'no', 'no'], media: ['yes', 'yes', 'no'] };
    function leafOf(ans) { for (var i = 0; i < ans.length; i++) if (ans[i]) return YES[Q[i]]; return LAST; }
    ADE.storageChoose = { Q: Q, YES: YES, LAST: LAST, CH: CH, ANS: ANS, PLACES: PLACES, PROPS: PROPS, leafOf: leafOf };
    function steps(s) {
      var c = s.data, ans = ANS[c], leaf = leafOf(ans), out = [];
      var met = function (done) { return { place: done ? M(m, 'place.' + leaf) : M(m, 'place.none'), chapter: done ? M(m, 'ch.' + CH[leaf]) : M(m, 'ch.none') }; };
      var a = S(m, c + '.start', { type: 'scenario', activeNodes: ['data'], nodeStates: {}, metrics: met(false), logEvents: [{ t: 0, kind: 'observe', subject: 'data' }] });
      a.callouts = [{ kind: 'try', textKey: M(m, 'co.try') }];
      out.push(a);
      ans.forEach(function (v, i) {
        out.push(S(m, c + '.' + Q[i], { type: 'mechanism', activeNodes: ['data', 'question'], nodeStates: nsOf({ data: 'done', question: v ? 'done' : 'skipped' }), metrics: met(false),
          params: { q: i + 1 }, movingSignals: [{ edge: 'e1', tok: 'state' }], logEvents: [{ t: i + 1, kind: v ? 'run' : 'skip', subject: 'question' }] }));
      });
      var z = S(m, c + '.leaf', { type: 'mechanism', activeNodes: ['place', 'chapter'], nodeStates: nsOf({ data: 'done', question: 'done', place: 'done', chapter: 'done' }), metrics: met(true),
        movingSignals: [{ edge: 'e2', tok: 'state' }, { edge: 'e3', tok: 'state' }], logEvents: [{ t: ans.length + 1, kind: 'complete', subject: 'place' }] });
      z.callouts = [{ kind: 'source', textKey: M(m, 'co.' + leaf) }];
      out.push(z);
      return out;
    }
    reg(m, { controls: [sel(m, 'data', CASES)], init: function () { return { data: 'appts' }; }, act: setter(['data']), steps: steps,
      simpExtra: [M(m, 'simp.2')],
      selfChecks: [
        { name: 'mỗi loại dữ liệu đi qua các câu hỏi đúng thứ tự, dừng ở câu "có" đầu tiên hay hết câu', run: function () { return CASES.every(function (c) { var a = ANS[c], k = a.indexOf(1); return k === -1 ? a.length === Q.length : k === a.length - 1; }); } },
        { name: 'năm loại dữ liệu mẫu rơi vào năm nơi lưu khác nhau', run: function () { var seen = {}; CASES.forEach(function (c) { seen[leafOf(ANS[c])] = 1; }); return Object.keys(seen).length === PLACES.length; } },
        { name: 'chỉ MediaStore còn sau khi gỡ app; chỉ cache bị hệ thống tự xóa (theo bảng của trang overview)', run: function () { return PLACES.every(function (p) { return (PROPS[p][1] === 'yes') === (p === 'media') && (PROPS[p][2] === 'yes') === (p === 'cache'); }); } },
        { name: 'bước cuối của mỗi loại có nơi lưu và chương', run: function () { return CASES.every(function (c) { var x = steps({ data: c }), z = x[x.length - 1]; return z.metrics.place !== M(m, 'place.none') && z.metrics.chapter !== M(m, 'ch.none'); }); } }] });
  })();

  /* ================= H2: file riêng của app — ghi thẳng, ghi qua AtomicFile, và file trong cache =================
     Theo App-specific storage (filesDir, cacheDir; cache có thể bị xóa khi thiếu bộ nhớ trong; kiểm file còn trước khi đọc),
     AtomicFile của androidx.core (ghi vào "<tên>.new", sync rồi đổi tên đè lên file gốc; finishWrite/failWrite), rename(2)
     (đổi tên đè lên file đích là nguyên tử). Mở FileOutputStream không ở chế độ nối thêm thì cắt file về 0 byte (Java SE).
     Cú kill là tình huống của site: tiến trình chết giữa lúc ghi (hệ thống thu hồi bộ nhớ, app crash, máy tắt nguồn). */
  (function () {
    var m = 'file', CASES = ['direct', 'atomic', 'cache'], KS = ['s1', 's2', 's3', 's4'];
    var LANES = ['app', 'sys', 'disk'];
    // mỗi bước: {app, sys, disk} = [khóa ô, lớp ô], số đo {file, lost}, loại bước, dòng mã, loại log, chủ thể, node sáng, trạng thái node
    var P = {
      direct: [
        [{ app: ['openOut', 'hl'], sys: ['idle', ''], disk: ['truncated', 'bad'] }, { file: 'empty', lost: 'none' }, 'scenario', [2], 'write', 'disk', ['app', 'disk'], { app: 'done', disk: 'surprise' }],
        [{ app: ['writeHalf', 'hl'], sys: ['idle', ''], disk: ['halfNew', 'bad'] }, { file: 'partial', lost: 'none' }, 'pitfall', [3], 'write', 'disk', ['app', 'disk'], { app: 'done', disk: 'surprise' }],
        [{ app: ['dead', 'bad'], sys: ['kill', 'hl'], disk: ['halfNew', 'bad'] }, { file: 'partial', lost: 'all' }, 'pitfall', [3], 'exception', 'sys', ['sys', 'app'], { app: 'broken', sys: 'done', disk: 'surprise' }],
        [{ app: ['readHalf', 'bad'], sys: ['restart', ''], disk: ['halfNew', 'bad'] }, { file: 'partial', lost: 'all' }, 'pitfall', [6, 7], 'observe', 'app', ['app', 'disk'], { app: 'broken', sys: 'done', disk: 'surprise' }]],
      atomic: [
        [{ app: ['startWrite', 'hl'], sys: ['idle', ''], disk: ['oldPlusNew', 'ok'] }, { file: 'intact', lost: 'none' }, 'scenario', [2, 3], 'write', 'disk', ['app', 'disk'], { app: 'done', disk: 'done' }],
        [{ app: ['writeHalf', 'hl'], sys: ['idle', ''], disk: ['oldPlusHalf', 'ok'] }, { file: 'intact', lost: 'none' }, 'mechanism', [4], 'write', 'disk', ['app', 'disk'], { app: 'done', disk: 'done' }],
        [{ app: ['dead', 'bad'], sys: ['kill', 'hl'], disk: ['oldPlusHalf', 'ok'] }, { file: 'intact', lost: 'edit' }, 'mechanism', [4], 'exception', 'sys', ['sys', 'app'], { app: 'broken', sys: 'done', disk: 'done' }],
        [{ app: ['readOld', 'ok'], sys: ['restart', ''], disk: ['oldOnly', 'ok'] }, { file: 'intact', lost: 'edit' }, 'mechanism', [7, 8, 9], 'complete', 'app', ['app', 'disk'], { app: 'done', sys: 'done', disk: 'done' }]],
      cache: [
        [{ app: ['download', 'hl'], sys: ['idle', ''], disk: ['pdfCached', 'ok'] }, { file: 'intact', lost: 'none' }, 'scenario', [2, 3], 'write', 'disk', ['app', 'disk'], { app: 'done', disk: 'done' }],
        [{ app: ['background', ''], sys: ['lowSpace', 'hl'], disk: ['pdfGone', 'bad'] }, { file: 'missing', lost: 'none' }, 'mechanism', [4], 'skip', 'sys', ['sys', 'disk'], { sys: 'done', disk: 'surprise' }],
        [{ app: ['openBlind', 'bad'], sys: ['idle', ''], disk: ['pdfGone', 'bad'] }, { file: 'missing', lost: 'crash' }, 'pitfall', [5], 'exception', 'app', ['app', 'disk'], { app: 'broken', sys: 'done', disk: 'surprise' }],
        [{ app: ['checkRefetch', 'ok'], sys: ['idle', ''], disk: ['pdfCached', 'ok'] }, { file: 'intact', lost: 'none' }, 'mechanism', [8, 9, 10], 'complete', 'app', ['app', 'disk'], { app: 'done', sys: 'done', disk: 'done' }]]
    };
    ADE.storageFile = { LANES: LANES, at: function (c, k) { return P[c][k][0]; } };
    function steps(s) {
      return P[s.case].map(function (p, i) {
        var met = { file: M(m, 'file.' + p[1].file), lost: M(m, 'lost.' + p[1].lost) }, bad = p[2] === 'pitfall';
        var o = S(m, s.case + '.' + KS[i], { type: p[2], activeNodes: p[6], nodeStates: nsOf(p[7]), metrics: met,
          codeHighlight: { snippet: 'h2.' + s.case, lines: p[3] },
          movingSignals: [{ edge: p[6][0] === 'sys' ? 'e2' : 'e1', tok: bad ? 'signal' : 'state' }], logEvents: [{ t: i, kind: p[4], subject: p[5] }] });
        if (i === 0) o.callouts = [{ kind: 'try', textKey: M(m, 'co.try') }];
        else o.callouts = [{ kind: bad ? 'pitfall' : 'source', textKey: M(m, 'co.' + s.case + '.' + KS[i]) }];
        return o;
      });
    }
    reg(m, { controls: [sel(m, 'case', CASES)], init: function () { return { case: 'direct' }; }, act: setter(['case']), steps: steps,
      simpExtra: [M(m, 'simp.2')],
      selfChecks: [
        { name: 'mỗi cách có 4 bước, mỗi bước đủ ba làn', run: function () { return CASES.every(function (c) { return P[c].length === 4 && P[c].every(function (p) { return LANES.every(function (l) { return !!p[0][l]; }); }); }); } },
        { name: 'ghi thẳng: sau cú kill file dở dang; AtomicFile: file gốc còn nguyên, chỉ mất lần sửa đang ghi', run: function () { var d = steps({ case: 'direct' })[3].metrics, a = steps({ case: 'atomic' })[3].metrics;
          return d.file === M(m, 'file.partial') && a.file === M(m, 'file.intact') && a.lost === M(m, 'lost.edit'); } },
        { name: 'cache: hệ thống xóa file; mở mà không kiểm thì lỗi, kiểm rồi tải lại thì có file', run: function () { var x = steps({ case: 'cache' }); return x[1].metrics.file === M(m, 'file.missing') && x[2].type === 'pitfall' && x[3].metrics.file === M(m, 'file.intact'); } }] });
  })();

  /* ================= H3: lưu một cài đặt bằng commit(), apply() và DataStore — main thread có bị chặn không =================
     Theo SharedPreferences.Editor (commit ghi đồng bộ, trả về kết quả; apply đổi bộ nhớ ngay, ghi đĩa bất đồng bộ, không báo lỗi;
     apply đang chờ có thể chặn main thread lúc chuyển vòng đời, nguồn ANR hay gặp), mã AOSP SharedPreferencesImpl (writeToFile
     ghi cả map rồi sync; apply xếp việc ghi qua QueuedWork), DataStore (đọc bằng Flow, ghi bằng hàm suspend theo giao dịch),
     ANRs (không phản hồi sự kiện nhập trong 5 giây). Độ chậm của đĩa là tình huống của site (máy rẻ, bộ nhớ đang bận). */
  (function () {
    var m = 'prefs', CASES = ['commit', 'apply', 'datastore'], KS = ['s1', 's2', 's3', 's4'];
    var LANES = ['main', 'io', 'disk'];
    // mỗi bước: làn {main, io, disk}, số đo {main, saved}, loại bước, dòng mã, loại log, chủ thể, node sáng, trạng thái node
    var P = {
      commit: [
        [{ main: ['tapCommit', 'hl'], io: ['none', ''], disk: ['idle', ''] }, { main: 'busy', saved: 'mem' }, 'scenario', [2], 'run', 'main', ['main'], { main: 'done' }],
        [{ main: ['waitDisk', 'bad'], io: ['none', ''], disk: ['writeAll', 'hl'] }, { main: 'blocked', saved: 'pending' }, 'pitfall', [2], 'write', 'disk', ['main', 'disk'], { main: 'surprise', disk: 'done' }],
        [{ main: ['waitSlow', 'bad'], io: ['none', ''], disk: ['slow', 'bad'] }, { main: 'anr', saved: 'pending' }, 'pitfall', [2], 'exception', 'main', ['main', 'disk'], { main: 'broken', disk: 'surprise' }],
        [{ main: ['commitTrue', 'ok'], io: ['none', ''], disk: ['saved', 'ok'] }, { main: 'free', saved: 'disk' }, 'mechanism', [3], 'complete', 'main', ['main'], { main: 'done', disk: 'done' }]],
      apply: [
        [{ main: ['tapApply', 'hl'], io: ['queued', ''], disk: ['idle', ''] }, { main: 'free', saved: 'mem' }, 'scenario', [2], 'run', 'main', ['main', 'io'], { main: 'done', io: 'done' }],
        [{ main: ['free', 'ok'], io: ['writing', 'hl'], disk: ['writeAll', 'hl'] }, { main: 'free', saved: 'pending' }, 'mechanism', [2], 'write', 'io', ['io', 'disk'], { main: 'done', io: 'done', disk: 'done' }],
        [{ main: ['onStopWait', 'bad'], io: ['writing', ''], disk: ['slow', 'bad'] }, { main: 'blocked', saved: 'pending' }, 'pitfall', [4], 'exception', 'main', ['main', 'io'], { main: 'surprise', io: 'done', disk: 'surprise' }],
        [{ main: ['free', ''], io: ['failSilent', 'bad'], disk: ['notSaved', 'bad'] }, { main: 'free', saved: 'unknown' }, 'pitfall', [5], 'observe', 'io', ['io', 'disk'], { main: 'done', io: 'broken', disk: 'surprise' }]],
      datastore: [
        [{ main: ['tapEdit', 'hl'], io: ['none', ''], disk: ['idle', ''] }, { main: 'free', saved: 'none' }, 'scenario', [6], 'run', 'main', ['main'], { main: 'done' }],
        [{ main: ['suspended', 'ok'], io: ['dsWrite', 'hl'], disk: ['writeAll', 'hl'] }, { main: 'free', saved: 'pending' }, 'mechanism', [7], 'write', 'io', ['io', 'disk'], { main: 'done', io: 'done', disk: 'done' }],
        [{ main: ['onStopFree', 'ok'], io: ['dsWrite', ''], disk: ['slow', ''] }, { main: 'free', saved: 'pending' }, 'mechanism', [7], 'observe', 'main', ['main', 'io'], { main: 'done', io: 'done', disk: 'done' }],
        [{ main: ['flowEmits', 'ok'], io: ['dsDone', 'ok'], disk: ['saved', 'ok'] }, { main: 'free', saved: 'disk' }, 'mechanism', [3, 4], 'complete', 'main', ['main', 'disk'], { main: 'done', io: 'done', disk: 'done' }]]
    };
    ADE.storagePrefs = { LANES: LANES, at: function (c, k) { return P[c][k][0]; } };
    function steps(s) {
      return P[s.case].map(function (p, i) {
        var met = { main: M(m, 'main.' + p[1].main), saved: M(m, 'saved.' + p[1].saved) }, bad = p[2] === 'pitfall';
        var o = S(m, s.case + '.' + KS[i], { type: p[2], activeNodes: p[6], nodeStates: nsOf(p[7]), metrics: met, codeHighlight: { snippet: 'h3.' + s.case, lines: p[3] },
          movingSignals: [{ edge: p[6].indexOf('io') >= 0 ? 'e2' : 'e1', tok: bad ? 'signal' : 'state' }], logEvents: [{ t: i, kind: p[4], subject: p[5] }] });
        o.callouts = [{ kind: i === 0 ? 'try' : (bad ? 'pitfall' : 'source'), textKey: i === 0 ? M(m, 'co.try') : M(m, 'co.' + s.case + '.' + KS[i]) }];
        return o;
      });
    }
    reg(m, { controls: [sel(m, 'case', CASES)], init: function () { return { case: 'commit' }; }, act: setter(['case']), steps: steps,
      simpExtra: [M(m, 'simp.2')],
      selfChecks: [
        { name: 'mỗi cách có 4 bước, mỗi bước đủ ba làn', run: function () { return CASES.every(function (c) { return P[c].length === 4 && P[c].every(function (p) { return LANES.every(function (l) { return !!p[0][l]; }); }); }); } },
        { name: 'commit chặn main thread lúc ghi; apply chặn lúc chuyển vòng đời và không báo lỗi', run: function () { var c = steps({ case: 'commit' }), a = steps({ case: 'apply' });
          return c[1].metrics.main === M(m, 'main.blocked') && a[0].metrics.main === M(m, 'main.free') && a[2].metrics.main === M(m, 'main.blocked') && a[3].metrics.saved === M(m, 'saved.unknown'); } },
        { name: 'DataStore không bao giờ chặn main thread', run: function () { return steps({ case: 'datastore' }).every(function (x) { return x.metrics.main === M(m, 'main.free'); }); } }] });
  })();

  /* ================= H4: Room — truy vấn một lần (suspend) so với truy vấn quan sát (Flow) qua ba lần ghi =================
     Theo Room (ba thành phần; kiểm SQL lúc biên dịch), Async queries (không truy cập database trên main thread; truy vấn một lần
     dùng suspend; truy vấn quan sát dùng Flow và chạy lại khi bảng được tham chiếu đổi, kể cả khi dòng đổi không nằm trong kết quả;
     dùng distinctUntilChanged để chỉ báo UI khi kết quả thật sự đổi), Accessing data (@Insert trả rowId; @Query kiểm lúc biên dịch).
     Ba lần ghi giống nhau ở hai cách: thêm lịch của bác sĩ A, sửa lịch của bác sĩ B, thêm một ghi chú (bảng khác). */
  (function () {
    var m = 'room', CASES = ['flow', 'oneshot'], KS = ['s1', 's2', 's3', 's4'];
    var WRITES = ['ins', 'updB', 'note'], TABLE = { ins: 'appointment', updB: 'appointment', note: 'note' };
    // theo từng lần ghi: [truy vấn chạy lại, kết quả đổi, màn hình nhận]
    var W = {
      flow: { ins: ['yes', 'yes', 'emit'], updB: ['yes', 'no', 'emitSame'], note: ['no', 'no', 'none'] },
      oneshot: { ins: ['no', 'yes', 'stale'], updB: ['no', 'no', 'none'], note: ['no', 'no', 'none'] }
    };
    // mỗi bước: tầng sáng trong luồng DAO → mã sinh → SQLite → kết quả, số đo {shown, runs}, loại bước, dòng mã, loại log, chủ thể
    var P = {
      flow: [[['dao', 'impl', 'sqlite', 'out'], { shown: 3, runs: 1 }, 'scenario', [3, 5], 'run', 'dao'],
        [['sqlite', 'impl', 'out'], { shown: 4, runs: 2 }, 'mechanism', [6, 7], 'write', 'sqlite'],
        [['sqlite', 'impl', 'out'], { shown: 4, runs: 3 }, 'mechanism', [8], 'write', 'sqlite'],
        [['sqlite'], { shown: 4, runs: 3 }, 'mechanism', [9], 'write', 'sqlite']],
      oneshot: [[['dao', 'impl', 'sqlite', 'out'], { shown: 3, runs: 1 }, 'scenario', [3, 4], 'run', 'dao'],
        [['sqlite'], { shown: 3, runs: 1 }, 'pitfall', [6, 7], 'write', 'sqlite'],
        [['sqlite'], { shown: 3, runs: 1 }, 'mechanism', [8], 'write', 'sqlite'],
        [['sqlite'], { shown: 3, runs: 1 }, 'pitfall', [9], 'observe', 'out']]
    };
    ADE.storageRoom = { WRITES: WRITES, TABLE: TABLE, W: W, STAGES: ['dao', 'impl', 'sqlite', 'out'], lit: function (c, k) { return P[c][k][0]; } };
    function steps(s) {
      return P[s.case].map(function (p, i) {
        var ns = {}; ['dao', 'impl', 'sqlite', 'out'].forEach(function (n) { ns[n] = K + 'st.' + (p[0].indexOf(n) >= 0 ? (p[2] === 'pitfall' && n !== 'sqlite' ? 'surprise' : 'done') : 'skipped'); });
        if (p[2] === 'pitfall') ns.out = K + 'st.surprise';
        var o = S(m, s.case + '.' + KS[i], { type: p[2], activeNodes: p[0], nodeStates: ns, metrics: { shown: p[1].shown, runs: p[1].runs }, codeHighlight: { snippet: 'h4.' + s.case, lines: p[3] },
          movingSignals: p[0].length > 1 ? [{ edge: 'e3', tok: p[2] === 'pitfall' ? 'signal' : 'state' }] : [], logEvents: [{ t: i, kind: p[4], subject: p[5] }] });
        o.callouts = [{ kind: i === 0 ? 'try' : (p[2] === 'pitfall' ? 'pitfall' : 'source'), textKey: i === 0 ? M(m, 'co.try') : M(m, 'co.' + s.case + '.' + KS[i]) }];
        return o;
      });
    }
    reg(m, { controls: [sel(m, 'case', CASES)], init: function () { return { case: 'flow' }; }, act: setter(['case']), steps: steps,
      simpExtra: [M(m, 'simp.2')],
      selfChecks: [
        { name: 'Flow chạy lại sau mọi lần ghi vào bảng appointment, kể cả khi kết quả không đổi; không chạy lại khi ghi bảng khác', run: function () {
          return WRITES.every(function (w) { return (W.flow[w][0] === 'yes') === (TABLE[w] === 'appointment'); }) && W.flow.updB[1] === 'no' && W.flow.updB[2] === 'emitSame'; } },
        { name: 'truy vấn một lần không bao giờ chạy lại: màn hình cũ sau khi thêm lịch', run: function () { return WRITES.every(function (w) { return W.oneshot[w][0] === 'no'; }) && steps({ case: 'oneshot' })[3].metrics.shown === 3; } },
        { name: 'số lần chạy truy vấn của Flow = 1 + số lần ghi vào bảng được tham chiếu', run: function () { return steps({ case: 'flow' })[3].metrics.runs === 1 + WRITES.filter(function (w) { return TABLE[w] === 'appointment'; }).length; } }] });
  })();

  /* ================= H5: đọc bác sĩ kèm lịch hẹn — vòng lặp N+1, @Relation + @Transaction, multimap JOIN =================
     Theo Define relationships between objects (multimap được khuyên nếu không có lý do dùng lớp trung gian; @Embedded, @Relation),
     One-to-many (@Relation cần Room chạy hai truy vấn nên thêm @Transaction để cả thao tác là nguyên tử), @Transaction reference
     (câu SELECT trong giao dịch có cái nhìn nhất quán; POJO có @Relation được truy vấn bằng các câu riêng). Lần ghi của đồng bộ nền
     chen giữa các truy vấn là tình huống của site: lịch #7 chuyển từ bác sĩ B sang bác sĩ C. */
  (function () {
    var m = 'rel', CASES = ['loop', 'relation', 'multimap'], KS = ['s1', 's2', 's3', 's4'];
    var DOCS = ['A', 'B', 'C'];
    var BEFORE = { 5: 'A', 6: 'B', 7: 'B', 8: 'C' };
    // mỗi bước: {q: số truy vấn đã chạy, res: kết quả đã ghép theo bác sĩ, moved: lịch #7 đã chuyển trong DB, rows: số dòng JOIN đã đọc}
    var P = {
      loop: [{ q: 1, res: {}, moved: false }, { q: 3, res: { A: [5], B: [6, 7] }, moved: false }, { q: 3, res: { A: [5], B: [6, 7] }, moved: true }, { q: 4, res: { A: [5], B: [6, 7], C: [7, 8] }, moved: true }],
      relation: [{ q: 1, res: {}, moved: false }, { q: 2, res: { A: [5], B: [6, 7], C: [8] }, moved: false }, { q: 2, res: { A: [5], B: [6, 7], C: [8] }, moved: true }, { q: 2, res: { A: [5], B: [6, 7], C: [8] }, moved: true }],
      multimap: [{ q: 1, res: {}, moved: false, rows: 4 }, { q: 1, res: { A: [5], B: [6, 7], C: [8] }, moved: false }, { q: 1, res: { A: [5], B: [6, 7], C: [8] }, moved: true }, { q: 1, res: { A: [5], B: [6, 7], C: [8] }, moved: true }]
    };
    // loại bước, dòng mã, loại log, chủ thể, node sáng
    var META = {
      loop: [['scenario', [1], 'run', 'doctors', ['doctors']], ['mechanism', [2, 3], 'run', 'appts', ['appts']], ['pitfall', [3], 'write', 'sync', ['sync', 'appts']], ['pitfall', [2, 3, 4], 'observe', 'result', ['appts', 'result']]],
      relation: [['scenario', [6, 7], 'run', 'doctors', ['doctors']], ['mechanism', [3, 4], 'run', 'appts', ['appts']], ['mechanism', [6], 'write', 'sync', ['sync']], ['mechanism', [8], 'complete', 'result', ['result']]],
      multimap: [['scenario', [1, 2], 'run', 'appts', ['doctors', 'appts']], ['mechanism', [3], 'run', 'result', ['result']], ['mechanism', [2], 'write', 'sync', ['sync']], ['mechanism', [3], 'complete', 'result', ['result']]]
    };
    function dupCount(res) { var seen = {}, d = 0; Object.keys(res).forEach(function (k) { res[k].forEach(function (id) { if (seen[id]) d++; seen[id] = 1; }); }); return d; }
    ADE.storageRel = { DOCS: DOCS, BEFORE: BEFORE, at: function (c, k) { return P[c][k]; }, dup: dupCount };
    function steps(s) {
      return P[s.case].map(function (p, i) {
        var mt = META[s.case][i], bad = mt[0] === 'pitfall';
        var ns = {}; ['doctors', 'appts', 'sync', 'result'].forEach(function (n) { if (mt[4].indexOf(n) >= 0) ns[n] = K + 'st.' + (bad && n !== 'sync' ? 'surprise' : 'done'); });
        var o = S(m, s.case + '.' + KS[i], { type: mt[0], activeNodes: mt[4], nodeStates: ns, metrics: { q: p.q, dup: dupCount(p.res) },
          codeHighlight: { snippet: 'h5.' + s.case, lines: mt[1] }, movingSignals: [{ edge: mt[4][0] === 'sync' ? 'e3' : (mt[4][0] === 'result' ? 'e2' : 'e1'), tok: bad ? 'signal' : 'state' }],
          logEvents: [{ t: i, kind: mt[2], subject: mt[3] }] });
        o.callouts = [{ kind: i === 0 ? 'try' : (bad ? 'pitfall' : 'source'), textKey: i === 0 ? M(m, 'co.try') : M(m, 'co.' + s.case + '.' + KS[i]) }];
        return o;
      });
    }
    reg(m, { controls: [sel(m, 'case', CASES)], init: function () { return { case: 'loop' }; }, act: setter(['case']), steps: steps,
      simpExtra: [M(m, 'simp.2')],
      selfChecks: [
        { name: 'vòng lặp chạy 1 + N truy vấn (N = 3 bác sĩ); @Relation chạy 2; multimap chạy 1', run: function () { return P.loop[3].q === 1 + DOCS.length && P.relation[3].q === 2 && P.multimap[3].q === 1; } },
        { name: 'chỉ vòng lặp không giao dịch mới đếm trùng lịch #7 khi đồng bộ chen giữa', run: function () { return dupCount(P.loop[3].res) === 1 && dupCount(P.relation[3].res) === 0 && dupCount(P.multimap[3].res) === 0; } },
        { name: 'kết quả nhất quán khớp đúng dữ liệu trước lần ghi', run: function () { var r = P.relation[3].res; return Object.keys(BEFORE).every(function (id) { return r[BEFORE[id]].indexOf(+id) >= 0; }); } }] });
  })();

  /* ================= H6: nâng app từ database v1 lên v3 — thiếu đường, xóa sạch, đủ đường =================
     Theo Migrating Room databases (Migration(start, end) và addMigrations; AutoMigration cần schema đã xuất; spec cho đổi tên hay xóa;
     thiếu đường migration thì IllegalStateException; fallbackToDestructiveMigration xóa vĩnh viễn mọi dữ liệu trong bảng; có cả
     migration tay và tự động cho cùng phiên bản thì Room dùng bản tay; Room kiểm schema sau khi chạy hết migration; MigrationTestHelper).
     Người dùng ở v1 với 12 lịch hẹn là tình huống của site. v2 thêm cột note; v3 thêm cột statusCode và điền từ cột status. */
  (function () {
    var m = 'mig', CASES = ['missing', 'destructive', 'complete'], KS = ['s1', 's2', 's3', 's4'];
    // hai mũi tên v1→v2, v2→v3: loại (auto | manual | missing)
    var EDGES = { missing: ['missing', 'manual'], destructive: ['missing', 'manual'], complete: ['auto', 'manual'] };
    // mỗi bước: {at: phiên bản DB đang có, edge: mũi tên đang xét (-1 không có), rows: số lịch còn, st: trạng thái}
    var P = {
      missing: [{ at: 1, edge: -1, rows: 12, st: 'old' }, { at: 1, edge: 0, rows: 12, st: 'search' }, { at: 1, edge: 0, rows: 12, st: 'crash' }, { at: 1, edge: 0, rows: 12, st: 'loop' }],
      destructive: [{ at: 1, edge: -1, rows: 12, st: 'old' }, { at: 1, edge: 0, rows: 12, st: 'search' }, { at: 3, edge: -1, rows: 0, st: 'wiped' }, { at: 3, edge: -1, rows: 0, st: 'empty' }],
      complete: [{ at: 1, edge: -1, rows: 12, st: 'old' }, { at: 2, edge: 0, rows: 12, st: 'step' }, { at: 3, edge: 1, rows: 12, st: 'step' }, { at: 3, edge: -1, rows: 12, st: 'valid' }]
    };
    // loại bước, dòng mã, loại log, chủ thể, node sáng
    var META = {
      missing: [['scenario', [1], 'run', 'app', ['app', 'db']], ['mechanism', [2, 3], 'observe', 'room', ['room', 'db']], ['pitfall', [2], 'exception', 'room', ['room']], ['pitfall', [1], 'exception', 'app', ['app', 'room']]],
      destructive: [['scenario', [1], 'run', 'app', ['app', 'db']], ['mechanism', [2, 3, 4], 'observe', 'room', ['room', 'db']], ['pitfall', [4], 'write', 'db', ['room', 'db']], ['pitfall', [1], 'observe', 'app', ['app', 'db']]],
      complete: [['scenario', [1], 'run', 'app', ['app', 'db']], ['mechanism', [2], 'write', 'db', ['room', 'db']], ['mechanism', [5, 7, 8], 'write', 'db', ['room', 'db']], ['mechanism', [9], 'complete', 'app', ['room', 'app']]]
    };
    ADE.storageMig = { EDGES: EDGES, at: function (c, k) { return P[c][k]; } };
    function steps(s) {
      return P[s.case].map(function (p, i) {
        var mt = META[s.case][i], bad = mt[0] === 'pitfall';
        var ns = {}; mt[4].forEach(function (n) { ns[n] = K + 'st.' + (bad ? (n === 'db' && p.rows === 0 ? 'broken' : 'surprise') : 'done'); });
        var o = S(m, s.case + '.' + KS[i], { type: mt[0], activeNodes: mt[4], nodeStates: ns, metrics: { ver: M(m, 'ver.' + p.at), rows: p.rows, st: M(m, 'st.' + p.st) },
          codeHighlight: { snippet: 'h6.' + s.case, lines: mt[1] }, movingSignals: [{ edge: mt[4][0] === 'app' ? 'e1' : 'e2', tok: bad ? 'signal' : 'state' }],
          logEvents: [{ t: i, kind: mt[2], subject: mt[3] }] });
        o.callouts = [{ kind: i === 0 ? 'try' : (bad ? 'pitfall' : 'source'), textKey: i === 0 ? M(m, 'co.try') : M(m, 'co.' + s.case + '.' + KS[i]) }];
        return o;
      });
    }
    reg(m, { controls: [sel(m, 'case', CASES)], init: function () { return { case: 'missing' }; }, act: setter(['case']), steps: steps,
      simpExtra: [M(m, 'simp.2')],
      selfChecks: [
        { name: 'thiếu mũi tên v1→v2: không cấu hình gì thì crash, có fallback thì mất hết dữ liệu', run: function () { return EDGES.missing[0] === 'missing' && P.missing[2].st === 'crash' && P.destructive[3].rows === 0; } },
        { name: 'đủ đường: đi qua từng phiên bản theo thứ tự và giữ nguyên 12 lịch', run: function () { var c = P.complete; return c[1].at === 2 && c[2].at === 3 && c.every(function (x) { return x.rows === 12; }) && EDGES.complete.indexOf('missing') < 0; } },
        { name: 'mỗi cách có 4 bước', run: function () { return CASES.every(function (c) { return steps({ case: c }).length === 4; }); } }] });
  })();

  /* ================= H7: đặt lịch lúc mất mạng rồi tắt app — ghi online, ghi local + coroutine, ghi lazy + WorkManager =================
     Theo Build an offline-first app (ba chiến lược ghi: online-only, queued, lazy; lazy là lựa chọn đúng khi dữ liệu quan trọng; hàng chờ
     có thể giữ trong Room và rút bằng WorkManager; enqueueUniqueWork với ExistingWorkPolicy.KEEP, NetworkType.CONNECTED, Result.retry
     thì WorkManager thử lại với backoff lũy thừa), Persistent work (công việc sống qua khởi động lại app và máy; lưu trong SQLite nội bộ;
     coroutine dừng ngay khi app đóng). Lịch #9 và thời điểm có mạng lại là tình huống của site. */
  (function () {
    var m = 'sync', CASES = ['online', 'coroutine', 'lazy'], KS = ['s1', 's2', 's3', 's4'];
    var PARTS = ['app', 'db', 'wm', 'server'];
    // tin nhắn: [từ, tới, khóa nhãn, xấu?]; từ = tới là tin tự gửi
    var MSG = {
      online: [[['app', 'server', 'post', 1]], [['server', 'app', 'ioerr', 1]], [['app', 'app', 'showErr', 0]], [['app', 'app', 'closed', 1]]],
      coroutine: [[['app', 'db', 'insertPending', 0], ['db', 'app', 'flowShow', 0]], [['app', 'app', 'retryLater', 0]], [['app', 'app', 'killedCo', 1]], [['db', 'db', 'stuck', 1]]],
      lazy: [[['app', 'db', 'insertPending', 0], ['app', 'wm', 'enqueue', 0]], [['app', 'app', 'closed', 0], ['wm', 'wm', 'persisted', 0]],
        [['wm', 'db', 'readPending', 0], ['wm', 'server', 'postWm', 0], ['server', 'wm', 'created', 0]], [['wm', 'db', 'markSynced', 0], ['db', 'app', 'flowSynced', 0]]]
    };
    // hàng chờ gửi của lịch #9 sau mỗi bước: [có trong DB, trạng thái, máy chủ có]
    var Q = {
      online: [['no', 'none', 'no'], ['no', 'none', 'no'], ['no', 'none', 'no'], ['no', 'none', 'no']],
      coroutine: [['yes', 'pending', 'no'], ['yes', 'pending', 'no'], ['yes', 'pending', 'no'], ['yes', 'pending', 'no']],
      lazy: [['yes', 'pending', 'no'], ['yes', 'pending', 'no'], ['yes', 'sending', 'yes'], ['yes', 'synced', 'yes']]
    };
    var TYPE = { online: ['scenario', 'pitfall', 'mechanism', 'pitfall'], coroutine: ['scenario', 'mechanism', 'pitfall', 'pitfall'], lazy: ['scenario', 'mechanism', 'mechanism', 'mechanism'] };
    var LINES = { online: [[2], [3], [4], [5]], coroutine: [[2, 3], [4, 5], [6], [6]], lazy: [[2, 3, 4], [5], [7, 8, 9], [10]] };
    ADE.storageSync = { PARTS: PARTS, msgs: function (c, k) { return MSG[c][k]; }, q: function (c, k) { return Q[c][k]; } };
    function steps(s) {
      return MSG[s.case].map(function (ms, i) {
        var type = TYPE[s.case][i], bad = type === 'pitfall', nodes = [];
        ms.forEach(function (x) { [x[0], x[1]].forEach(function (p) { if (nodes.indexOf(p) < 0) nodes.push(p); }); });
        var ns = {}; nodes.forEach(function (n) { ns[n] = K + 'st.' + (bad ? 'surprise' : 'done'); });
        var q = Q[s.case][i];
        var o = S(m, s.case + '.' + KS[i], { type: type, activeNodes: nodes, nodeStates: ns, metrics: { inDb: M(m, 'yn.' + q[0]), state: M(m, 'q.' + q[1]), server: M(m, 'yn.' + q[2]) },
          codeHighlight: { snippet: 'h7.' + s.case, lines: LINES[s.case][i] }, movingSignals: [], logEvents: [{ t: i, kind: bad ? 'exception' : (i === 3 ? 'complete' : 'run'), subject: nodes[0] }] });
        o.callouts = [{ kind: i === 0 ? 'try' : (bad ? 'pitfall' : 'source'), textKey: i === 0 ? M(m, 'co.try') : M(m, 'co.' + s.case + '.' + KS[i]) }];
        return o;
      });
    }
    reg(m, { controls: [sel(m, 'case', CASES)], init: function () { return { case: 'online' }; }, act: setter(['case']), steps: steps,
      simpExtra: [M(m, 'simp.2')],
      selfChecks: [
        { name: 'chỉ ghi lazy + WorkManager mới đưa được lịch #9 lên máy chủ sau khi app bị tắt', run: function () { return CASES.every(function (c) { return (Q[c][3][2] === 'yes') === (c === 'lazy'); }); } },
        { name: 'ghi online lúc mất mạng không lưu gì xuống máy; ghi local thì có lịch trong DB từ bước 1', run: function () { return Q.online.every(function (r) { return r[0] === 'no'; }) && Q.coroutine[0][0] === 'yes' && Q.lazy[0][0] === 'yes'; } },
        { name: 'mọi tin nhắn đi giữa bốn bên đã khai báo', run: function () { return CASES.every(function (c) { return MSG[c].every(function (ms) { return ms.every(function (x) { return PARTS.indexOf(x[0]) >= 0 && PARTS.indexOf(x[1]) >= 0; }); }); }); } }] });
  })();

  /* ================= H8: ảnh hồ sơ qua bốn đời Android — đường dẫn tệp, MediaStore, đọc ảnh app khác, photo picker =================
     Theo Access media files from shared storage (từ Android 10 không cần quyền để thêm và sửa media của chính app; Android 9 trở xuống
     cần READ/WRITE_EXTERNAL_STORAGE, WRITE khai maxSdkVersion 29; Android 10 tạm thoát scoped storage bằng requestLegacyExternalStorage;
     từ Android 11 dùng được File và fopen trên shared storage, đọc ghi ngẫu nhiên có thể chậm gấp đôi; READ_MEDIA_IMAGES bị giới hạn bởi
     chính sách Google Play, trang khuyên photo picker; IS_PENDING và RELATIVE_PATH từ Android 10), Photo picker (backport qua Google Play
     services tới Android 4.4; ACTION_OPEN_DOCUMENT khi không có). App giả định target SDK mới nhất. */
  (function () {
    var m = 'media', CASES = ['path', 'mediastore', 'read', 'picker'], KS = ['s1', 's2', 's3', 's4'];
    var ROWS = ['a9', 'a10', 'a11', 'a13'];
    // ô ma trận [phiên bản][cách]: ok | perm (cần quyền) | legacy (chỉ khi tạm thoát scoped storage) | slow (được, chậm hơn) | restricted (cần quyền bị Play giới hạn)
    var CELL = {
      a9: { path: 'perm', mediastore: 'perm', read: 'perm', picker: 'ok' },
      a10: { path: 'legacy', mediastore: 'ok', read: 'perm', picker: 'ok' },
      a11: { path: 'slow', mediastore: 'ok', read: 'perm', picker: 'ok' },
      a13: { path: 'slow', mediastore: 'ok', read: 'restricted', picker: 'ok' }
    };
    var BAD = { legacy: 1 }, WARN = { perm: 1, restricted: 1, slow: 1 };
    ADE.storageMedia = { ROWS: ROWS, COLS: CASES, CELL: CELL };
    var LINES = { path: [[1, 2], [2, 3], [3], [3]], mediastore: [[1, 2, 3, 4, 5, 6], [7, 8], [9], [9]], read: [[1, 2], [1, 2], [1, 2], [1, 2]], picker: [[1, 2], [3], [3], [3]] };
    function steps(s) {
      return ROWS.map(function (r, i) {
        var v = CELL[r][s.case], bad = !!BAD[v], warn = !!WARN[v];
        var ns = { app: K + 'st.done', api: K + 'st.' + (bad ? 'broken' : (warn ? 'surprise' : 'done')), store: K + 'st.' + (bad ? 'skipped' : 'done') };
        var o = S(m, s.case + '.' + KS[i], { type: i === 0 ? 'scenario' : (bad ? 'pitfall' : 'mechanism'), activeNodes: ['app', 'api', 'store'], nodeStates: ns,
          metrics: { ver: M(m, 'row.' + r), res: M(m, 'cell.' + v) }, codeHighlight: { snippet: 'h8.' + s.case, lines: LINES[s.case][i] },
          movingSignals: [{ edge: 'e1', tok: bad ? 'signal' : 'state' }, { edge: 'e2', tok: bad ? 'signal' : 'state' }], logEvents: [{ t: i, kind: bad ? 'exception' : 'run', subject: 'api' }] });
        o.callouts = [{ kind: i === 0 ? 'try' : (bad ? 'pitfall' : 'source'), textKey: i === 0 ? M(m, 'co.try') : M(m, 'co.' + s.case + '.' + KS[i]) }];
        return o;
      });
    }
    reg(m, { controls: [sel(m, 'case', CASES)], init: function () { return { case: 'path' }; }, act: setter(['case']), steps: steps,
      simpExtra: [M(m, 'simp.2')],
      selfChecks: [
        { name: 'photo picker không cần quyền ở mọi phiên bản', run: function () { return ROWS.every(function (r) { return CELL[r].picker === 'ok'; }); } },
        { name: 'từ Android 10, thêm ảnh của chính app qua MediaStore không cần quyền; Android 9 thì cần', run: function () { return CELL.a9.mediastore === 'perm' && ['a10', 'a11', 'a13'].every(function (r) { return CELL[r].mediastore === 'ok'; }); } },
        { name: 'đường dẫn tệp chỉ hỏng ở Android 10 (scoped storage, chưa có File trên shared storage)', run: function () { return ROWS.filter(function (r) { return BAD[CELL[r].path]; }).join() === 'a10'; } }] });
  })();
})();
