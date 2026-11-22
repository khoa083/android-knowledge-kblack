/* Model cho các chương v2 (Phần 1, theo Kotlin Coroutines: Deep Dive). Thuần, không DOM, không câu chữ (chỉ message key).
   Mọi mô hình là MÔ HÌNH GIẢNG DẠY (simplified); nguồn và giới hạn ở docs/research/coroutines.md. */
(function () {
  'use strict';
  var C = ADE.coro, K = C.K, step = C.step;
  var M = function (m, s) { return K + 'm.' + m + '.' + s; };

  /* ================= U2: sequence builder: luồng thực thi nhảy giữa main và khối sequence =================
     Một luồng duy nhất. Mỗi lần main gọi next(), luồng chạy vào khối sequence tới yield kế tiếp rồi quay lại main.
     Trạng thái mỗi hàng sau từng sự kiện nằm ở params: m (main), g (khối sequence) ∈ run | call | wait | idle | done.
     So sánh: chế độ "List" (buildList) chạy HẾT khối ngay từ đầu, không nhảy qua lại. */
  (function () {
    var m = 'seq';
    function steps(s) {
      var out = [], t = 0, last = '?', printed = 0;
      var push = function (id, o) {
        t += 10;
        var ps = o.ps || {};
        var ns = { main: M(m, 'st.' + ps.m), gen: M(m, 'st.' + ps.g), th: M(m, 'st.th' + (ps.m === 'run' ? 'Main' : ps.g === 'run' ? 'Gen' : 'Free')) };
        if (o.val != null) last = o.val;
        if (o.out) printed += o.out;
        var ev = (o.ev || []).map(function (e) { e.t = t; e.scope = M(m, 'scope'); e.params = e.params || {}; e.params.m = ps.m; e.params.g = ps.g; return e; });
        out.push(step({ id: id, type: o.type || 'mechanism', titleKey: M(m, 's.' + id + '.title'), explainKey: M(m, 's.' + id + '.explain'), params: o.params || {},
          activeNodes: [ps.m === 'run' ? 'main' : 'gen'], nodeStates: ns,
          metrics: { time: t, val: last, out: printed }, codeHighlight: { snippet: s.eager ? 'seqList' : 'seq', lines: o.lines },
          callouts: o.co ? [{ kind: o.co[0], textKey: M(m, 'co.' + o.co[1]) }] : [], logEvents: ev }));
      };
      var E = function (kind, subject, key, params) { var p = {}; for (var k in (params || {})) p[k] = params[k]; return { kind: kind, subject: subject, detailKey: M(m, 'ev.' + key), params: p }; };
      if (s.eager) {
        push('eBuild', { ps: { m: 'call', g: 'run' }, lines: [2, 3, 4, 5, 6, 7, 8, 9], out: 4, type: 'experiment', co: ['pitfall', 'eager'],
          ev: [E('run', 'gen', 'eBuild')] });
        push('eDone', { ps: { m: 'run', g: 'done' }, lines: [10], ev: [E('complete', 'gen', 'eDone')] });
        push('eStart', { ps: { m: 'run', g: 'done' }, lines: [11, 12], out: 1, ev: [E('run', 'main', 'start')] });
        push('eFirst', { ps: { m: 'run', g: 'done' }, lines: [13], val: 1, out: 1, params: { v: 1 }, ev: [E('collect', 'main', 'eRead', { v: 1 })] });
        push('eSecond', { ps: { m: 'run', g: 'done' }, lines: [14], val: 2, out: 1, params: { v: 2 }, ev: [E('collect', 'main', 'eRead', { v: 2 })] });
        return out;
      }
      push('start', { ps: { m: 'run', g: 'idle' }, lines: [12, 13], out: 1, co: ['try', 'start'], ev: [E('run', 'main', 'start')] });
      var words = ['first', 'second', 'third'];
      var n = s.all ? 3 : 2;
      for (var i = 0; i < n; i++) {
        var v = i + 1, P = { v: v, w: words[i] };
        push('next' + v, { ps: { m: 'call', g: 'run' }, lines: [14 + 2 * i, 2 + 2 * i], out: 1, params: P, co: i === 0 ? ['mechanism', 'enter'] : i === 1 ? ['mechanism', 'resume'] : null,
          ev: [E(i === 0 ? 'launch' : 'resume', 'gen', i === 0 ? 'enter' : 'resume', P)] });
        push('yield' + v, { ps: { m: 'run', g: 'wait' }, lines: [3 + 2 * i, 14 + 2 * i], val: v, params: P, co: i === 0 ? ['mechanism', 'yield'] : null,
          ev: [E('suspend', 'gen', 'yield', P), E('collect', 'main', 'got', P)] });
        push('print' + v, { ps: { m: 'run', g: 'wait' }, lines: [15 + 2 * i], out: 1, params: P, ev: [E('run', 'main', 'print', P)] });
      }
      if (s.all) {
        push('end', { ps: { m: 'call', g: 'run' }, lines: [20, 8, 9], out: 1, co: ['mechanism', 'end'], ev: [E('resume', 'gen', 'end')] });
        push('finish', { ps: { m: 'run', g: 'done' }, lines: [20, 21], out: 1, ev: [E('complete', 'gen', 'finish'), E('complete', 'main', 'mainDone')] });
      } else {
        push('pause', { ps: { m: 'done', g: 'wait' }, lines: [21], type: 'pitfall', co: ['mechanism', 'pause'], ev: [E('complete', 'main', 'mainDone')] });
      }
      return out;
    }
    ADE.registerModel('coroutines.seq', {
      kind: 'discrete', titleKey: M(m, 'title'), overviewKey: M(m, 'overview'), wrapupKey: M(m, 'wrapup'), codeId: 'seq',
      simplificationKeys: [M(m, 'simp.1'), M(m, 'simp.2')], controlsHintKey: M(m, 'ctl.hint'),
      controls: [
        { id: 'all', type: 'toggle', labelKey: M(m, 'ctl.all'), get: function (s) { return s.all; }, action: 'all' },
        { id: 'eager', type: 'toggle', labelKey: M(m, 'ctl.eager'), get: function (s) { return s.eager; }, action: 'eager' }
      ],
      init: function () { return { all: false, eager: false }; },
      act: function (s, a, v) { var n = { all: s.all, eager: s.eager }; n[a] = !!v; return n; },
      steps: steps,
      selfChecks: [
        { name: 'lazy 2 lần next: 8 bước, khối sequence dừng ở yield(2); đi hết: có Done; List: khối chạy hết trước Starting', run: function () {
          var d = ADE.models['coroutines.seq'], a = d.steps({ all: false, eager: false }), b = d.steps({ all: true, eager: false }), c = d.steps({ all: false, eager: true });
          var lastG = function (st) { return st[st.length - 1].logEvents[0].params.g; };
          return a.length === 8 && lastG(a) === 'wait' && b[b.length - 1].id === 'finish' && c[0].id === 'eBuild' && c[2].id === 'eStart';
        } }
      ]
    });
  })();
})();
