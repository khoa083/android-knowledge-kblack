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
})();
