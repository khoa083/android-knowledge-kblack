/* Model A7 (Flow), A8 (lifecycle, Compose), A9 (shared state, virtual time). Thuần, không DOM, không câu chữ.
   Mô hình giảng dạy: không mô phỏng scheduler thật; thời gian và thứ tự chỉ để minh họa (nhãn simplified). */
(function () {
  'use strict';
  var C = ADE.coro, K = C.K, step = C.step;
  var M = function (m, s) { return K + 'm.' + m + '.' + s; };

  /* ================= A7a: pipeline source → map → (buffer | conflate | collectLatest) → collect ================= */
  (function () {
    var m = 'flowpipe', N = 5, EVERY = 100, WORK = 250, CAP = 2;
    /* Quy tắc thời gian (nguồn: coroutines-flow, coroutines-flow-operators):
       - Mặc định producer và collector chạy tuần tự trong một coroutine: emit chỉ trả về khi collect xong.
       - buffer(n): producer chạy song song, chỉ suspend khi buffer đầy.
       - conflate = buffer(1, DROP_OLDEST): bỏ giá trị cũ khi collector còn bận, collector lấy giá trị mới nhất.
       - collectLatest: giá trị mới hủy xử lý đang chạy dở. */
    function simulate(op) {
      var ev = [], i, e = [], st = [], en = [], dropped = [], cancelled = [];
      if (op === 'none') {
        for (i = 1; i <= N; i++) { e[i] = i === 1 ? 0 : en[i - 1] + EVERY; st[i] = e[i]; en[i] = st[i] + WORK; }
      } else if (op === 'buffer') {
        for (i = 1; i <= N; i++) {
          e[i] = i === 1 ? 0 : e[i - 1] + EVERY;
          if (i - CAP - 1 >= 1) e[i] = Math.max(e[i], st[i - CAP - 1]);
          st[i] = Math.max(e[i], i === 1 ? 0 : en[i - 1]); en[i] = st[i] + WORK;
        }
      } else if (op === 'conflate') {
        for (i = 1; i <= N; i++) e[i] = (i - 1) * EVERY;
        var free = 0, next = 1, last = 0;
        while (next <= N) {
          // chọn giá trị mới nhất đã phát tới thời điểm collector rảnh; nếu chưa có thì đợi giá trị kế tiếp
          var t0 = Math.max(free, e[next]), pick = next;
          for (var j = next; j <= N && e[j] <= t0; j++) pick = j;
          for (j = next; j < pick; j++) dropped.push({ i: j, t: t0 });
          st[pick] = t0; en[pick] = t0 + WORK; free = en[pick]; next = pick + 1; last = pick;
        }
      } else {
        for (i = 1; i <= N; i++) { e[i] = (i - 1) * EVERY; st[i] = e[i]; en[i] = st[i] + WORK; }
        for (i = 1; i < N; i++) if (en[i] > e[i + 1]) { cancelled.push({ i: i, t: e[i + 1] }); en[i] = null; }
      }
      for (i = 1; i <= N; i++) {
        ev.push({ t: e[i], kind: 'emit', item: i, order: 0 });
        if (st[i] != null && !dropped.some(function (d) { return d.i === i; })) ev.push({ t: st[i], kind: 'collect', item: i, order: 1 });
        if (en[i] != null && st[i] != null) ev.push({ t: en[i], kind: 'complete', item: i, order: 2 });
      }
      dropped.forEach(function (d) { ev.push({ t: d.t, kind: 'skip', item: d.i, order: 1 }); });
      cancelled.forEach(function (c) { ev.push({ t: c.t, kind: 'cancel', item: c.i, order: 0 }); });
      ev.sort(function (a, b) { return a.t - b.t || a.order - b.order || a.item - b.item; });
      return ev;
    }
    function steps(s) {
      var ev = simulate(s.op), out = [], emitted = 0, done = 0, drop = 0, canc = 0, started = {};
      var NS = { producer: 'producer', map: 'map', buf: 'buf', collector: 'collector' };
      var P = { op: s.op, n: N, every: EVERY, work: WORK, cap: CAP };
      ev.forEach(function (x, idx) {
        var p = { item: x.item, v: x.item * 10, n: N, every: EVERY, work: WORK, cap: CAP }, key, subj, active, sig = [], kind = x.kind, type = 'mechanism';
        if (x.kind === 'emit') { emitted++; key = 'emit'; subj = 'producer'; active = ['producer', 'map']; sig = [{ edge: 'e1', tok: 'flow' }]; }
        else if (x.kind === 'collect') { started[x.item] = 1; key = 'collect'; subj = 'collector'; active = ['buf', 'collector']; sig = [{ edge: 'e3', tok: 'flow' }]; }
        else if (x.kind === 'complete') { done++; key = 'done'; subj = 'collector'; active = ['collector']; }
        else if (x.kind === 'skip') { drop++; key = 'drop'; subj = 'buf'; active = ['buf']; type = 'pitfall'; }
        else { canc++; key = 'cancel'; subj = 'collector'; active = ['collector']; type = 'pitfall'; }
        var o = step({
          id: 'e' + idx, type: idx === 0 ? 'scenario' : type, titleKey: M(m, 's.' + key + '.title'), explainKey: M(m, 's.' + key + '.' + (s.op === 'none' && key === 'emit' && x.item > 1 ? 'explainSeq' : 'explain')), params: p,
          activeNodes: active, movingSignals: sig, metrics: { emitted: emitted, processed: done, dropped: drop, cancelled: canc, time: x.t },
          nodeStates: { producer: emitted >= N ? K + 'st.done' : K + 'st.running', collector: done + canc >= N - drop ? K + 'st.done' : K + 'st.running', buf: s.op === 'none' || s.op === 'collectLatest' ? K + 'st.unused' : K + 'st.running' },
          codeHighlight: { snippet: 'flowpipe', lines: key === 'emit' ? [2, 3] : (key === 'cancel' || key === 'collect' || key === 'done' ? [5, 6] : [4]) },
          logEvents: [{ t: x.t, kind: kind, subject: subj, detailKey: M(m, 'ev.' + key), params: p }]
        });
        if (idx === 0) o.callouts = [{ kind: 'try', textKey: M(m, 'co.try') }];
        if (key === 'drop') { o.skipped = [{ whatKey: M(m, 'sk.drop.what'), whyKey: M(m, 'sk.drop.why') }]; o.changes = [{ op: 'remove', textKey: M(m, 'ch.drop'), params: p }]; o.callouts = [{ kind: 'mechanism', textKey: M(m, 'co.conflate') }]; }
        if (key === 'cancel') { o.changes = [{ op: 'remove', textKey: M(m, 'ch.cancel'), params: p }]; o.callouts = [{ kind: 'mechanism', textKey: M(m, 'co.latest') }]; }
        if (key === 'emit' && s.op === 'none' && x.item === 2) o.callouts = [{ kind: 'pitfall', textKey: M(m, 'co.seq') }];
        if (key === 'emit' && s.op === 'buffer' && x.item === 1) o.callouts = [{ kind: 'mechanism', textKey: M(m, 'co.buffer') }];
        out.push(o);
      });
      return out;
    }
    ADE.registerModel('coroutines.flowpipe', {
      kind: 'discrete', titleKey: M(m, 'title'), overviewKey: M(m, 'overview'), wrapupKey: M(m, 'wrapup'), codeId: 'flowpipe',
      simplificationKeys: [M(m, 'simp.1'), K + 'simp.sched', K + 'simp.time'], controlsHintKey: M(m, 'ctl.hint'),
      controls: [{ id: 'op', type: 'select', labelKey: M(m, 'ctl.op'), get: function (s) { return s.op; }, action: 'op', options: ['none', 'buffer', 'conflate', 'collectLatest'].map(function (v) { return { value: v, labelKey: M(m, 'ctl.op.' + v) }; }) }],
      init: function () { return { op: 'none' }; },
      act: function (s, a, v) { return { op: v }; },
      steps: steps,
      selfChecks: [
        { name: 'tuần tự: collector xong item 5 lúc 1650 ms; buffer: 1250 ms', run: function () {
          var end = function (op) { var e = simulate(op).filter(function (x) { return x.kind === 'complete'; }); return e[e.length - 1].t; };
          return end('none') === 1650 && end('buffer') === 1250;
        } },
        { name: 'conflate bỏ bớt giá trị và vẫn xử lý giá trị mới nhất (item 5)', run: function () {
          var e = simulate('conflate'), drops = e.filter(function (x) { return x.kind === 'skip'; }).length, done = e.filter(function (x) { return x.kind === 'complete'; });
          return drops > 0 && done[done.length - 1].item === 5 && drops + done.length === 5;
        } },
        { name: 'collectLatest: chỉ item cuối hoàn tất, các item trước bị hủy', run: function () {
          var e = simulate('collectLatest'), done = e.filter(function (x) { return x.kind === 'complete'; }), canc = e.filter(function (x) { return x.kind === 'cancel'; });
          return done.length === 1 && done[0].item === 5 && canc.length === 4;
        } }
      ]
    });
  })();

  /* ================= A7b: cold flow, SharedFlow, StateFlow, Channel với người nhận đến muộn ================= */
  (function () {
    var m = 'hotcold';
    /* Kịch bản: producer phát 1, 2, 3 lúc t=10, 20, 30; collector A đăng ký lúc t=0; collector B đăng ký lúc t=25.
       Quy tắc (nguồn: coroutines-flow, channels, stateflow-and-sharedflow):
       - cold: mỗi collector tự chạy lại flow từ đầu.
       - SharedFlow(replay=r): collector mới nhận r giá trị gần nhất rồi tới giá trị mới.
       - StateFlow: có giá trị hiện tại (khởi tạo 0); collector mới nhận giá trị hiện tại rồi giá trị mới.
       - Channel: mỗi phần tử chỉ tới MỘT receiver; phục vụ theo thứ tự invoke receive (FIFO, có nêu trong tài liệu). */
    function simulate(s) {
      var ev = [], P = [{ v: 1, t: 10 }, { v: 2, t: 20 }, { v: 3, t: 30 }];
      var got = { a: [], b: [] };
      var add = function (t, kind, who, v, key) { ev.push({ t: t, kind: kind, who: who, v: v, key: key }); };
      add(0, 'launch', 'a', null, 'subA');
      if (s.type === 'cold') {
        add(0, 'launch', 'flow', null, 'run1');
        P.forEach(function (x) { add(x.t, 'emit', 'flow', x.v, 'emit'); add(x.t, 'collect', 'a', x.v, 'recv'); got.a.push(x.v); });
        add(25, 'launch', 'b', null, 'subB'); add(25, 'launch', 'flow', null, 'run2');
        P.forEach(function (x) { add(25 + x.t, 'emit', 'flow', x.v, 'emit'); add(25 + x.t, 'collect', 'b', x.v, 'recv'); got.b.push(x.v); });
      } else if (s.type === 'state') {
        add(0, 'collect', 'a', 0, 'recvInit'); got.a.push(0);
        P.forEach(function (x) {
          add(x.t, 'emit', 'flow', x.v, 'emitState'); add(x.t, 'collect', 'a', x.v, 'recv'); got.a.push(x.v);
          if (x.t === 20) { add(25, 'launch', 'b', null, 'subB'); add(25, 'collect', 'b', 2, 'recvCurrent'); got.b.push(2); }
          if (x.t === 30) { add(30, 'collect', 'b', x.v, 'recv'); got.b.push(x.v); }
        });
      } else if (s.type === 'shared') {
        var cache = [];
        P.forEach(function (x) {
          add(x.t, 'emit', 'flow', x.v, 'emit'); add(x.t, 'collect', 'a', x.v, 'recv'); got.a.push(x.v); cache.push(x.v);
          if (x.t === 20) {
            add(25, 'launch', 'b', null, 'subB');
            var rep = s.replay > 0 ? cache.slice(-s.replay) : []; rep.forEach(function (v) { add(25, 'collect', 'b', v, 'recvReplay'); got.b.push(v); });
            if (!rep.length) add(25, 'suspend', 'b', null, 'noReplay');
          }
          if (x.t === 30) { add(30, 'collect', 'b', x.v, 'recv'); got.b.push(x.v); }
        });
      } else {
        // Channel: A xử lý mất 15 ms mỗi phần tử; B tới lúc 25
        add(0, 'suspend', 'a', null, 'waitA');
        add(10, 'emit', 'flow', 1, 'send'); add(10, 'collect', 'a', 1, 'recvOnly'); got.a.push(1);
        add(20, 'emit', 'flow', 2, 'send'); add(20, 'collect', 'a', 2, 'recvOnly'); got.a.push(2);
        add(25, 'launch', 'b', null, 'subB'); add(25, 'suspend', 'b', null, 'waitB');
        add(30, 'emit', 'flow', 3, 'send'); add(30, 'collect', 'b', 3, 'recvOnlyB'); got.b.push(3);
      }
      ev.sort(function (a, b) { return a.t - b.t; });
      return { ev: ev, got: got };
    }
    function steps(s) {
      var r = simulate(s), out = [], a = [], b = [];
      r.ev.forEach(function (e, i) {
        if (e.kind === 'collect' && e.who === 'a') a.push(e.v);
        if (e.kind === 'collect' && e.who === 'b') b.push(e.v);
        var p = { v: e.v, t: e.t, r: s.replay, type: s.type }, subj = e.who;
        var o = step({ id: 'e' + i, type: i === 0 ? 'scenario' : 'mechanism', titleKey: M(m, 's.' + e.key + '.title'), explainKey: M(m, 's.' + e.key + '.explain'), params: p,
          activeNodes: [subj === 'flow' ? 'flow' : subj], movingSignals: e.kind === 'collect' ? [{ edge: subj === 'a' ? 'e1' : 'e2', tok: 'flow', label: e.v }] : [],
          stateAfter: [{ labelKey: M(m, 'st.a'), value: a.length ? a.join(', ') : '–' }, { labelKey: M(m, 'st.b'), value: b.length ? b.join(', ') : '–' }],
          nodeStates: { a: K + 'st.running', b: r.ev.slice(0, i + 1).some(function (x) { return x.who === 'b'; }) ? K + 'st.running' : K + 'st.unused' },
          metrics: { a: a.length, b: b.length, time: e.t }, codeHighlight: { snippet: 'hotcold', lines: s.type === 'cold' ? [1, 2] : s.type === 'state' ? [3] : s.type === 'shared' ? [4] : [5] },
          logEvents: [{ t: e.t, kind: e.kind, subject: subj, detailKey: M(m, 'ev.' + e.key), params: p }] });
        if (i === 0) o.callouts = [{ kind: 'try', textKey: M(m, 'co.try') }];
        if (e.key === 'run2') o.callouts = [{ kind: 'mechanism', textKey: M(m, 'co.cold') }];
        if (e.key === 'recvCurrent') o.callouts = [{ kind: 'mechanism', textKey: M(m, 'co.state') }];
        if (e.key === 'recvReplay' || e.key === 'noReplay') o.callouts = [{ kind: 'mechanism', textKey: M(m, 'co.shared') }];
        if (e.key === 'recvOnlyB') o.callouts = [{ kind: 'source', textKey: M(m, 'co.channel') }];
        out.push(o);
      });
      return out;
    }
    ADE.registerModel('coroutines.hotcold', {
      kind: 'discrete', titleKey: M(m, 'title'), overviewKey: M(m, 'overview'), wrapupKey: M(m, 'wrapup'), codeId: 'hotcold',
      simplificationKeys: [M(m, 'simp.1'), K + 'simp.sched', K + 'simp.time'], controlsHintKey: M(m, 'ctl.hint'),
      controls: [
        { id: 'type', type: 'select', labelKey: M(m, 'ctl.type'), get: function (s) { return s.type; }, action: 'type', options: ['cold', 'shared', 'state', 'channel'].map(function (v) { return { value: v, labelKey: M(m, 'ctl.type.' + v) }; }) },
        { id: 'replay', type: 'select', labelKey: M(m, 'ctl.replay'), get: function (s) { return s.replay; }, action: 'replay', options: [0, 1, 2].map(function (v) { return { value: v, labelKey: M(m, 'ctl.replay.n'), params: { n: v } }; }) }
      ],
      init: function () { return { type: 'cold', replay: 1 }; },
      act: function (s, a, v) { return a === 'type' ? { type: v, replay: s.replay } : { type: s.type, replay: Math.max(0, Math.min(2, v | 0)) }; },
      steps: steps,
      selfChecks: [
        { name: 'B đến muộn: cold nhận 1,2,3; SharedFlow replay=1 nhận 2,3; replay=0 nhận 3; StateFlow nhận 2,3; Channel nhận 3', run: function () {
          var g = function (s) { return simulate(s).got.b.join(','); };
          return g({ type: 'cold', replay: 1 }) === '1,2,3' && g({ type: 'shared', replay: 1 }) === '2,3' && g({ type: 'shared', replay: 0 }) === '3' && g({ type: 'shared', replay: 2 }) === '1,2,3' && g({ type: 'state', replay: 1 }) === '2,3' && g({ type: 'channel', replay: 1 }) === '3';
        } },
        { name: 'Channel: mỗi phần tử chỉ tới một receiver', run: function () { var g = simulate({ type: 'channel', replay: 1 }).got; return g.a.length + g.b.length === 3 && g.a.every(function (v) { return g.b.indexOf(v) < 0; }); } }
      ]
    });
  })();

  /* ================= A8a: lifecycle của màn hình và nơi thu Flow ================= */
  (function () {
    var m = 'lifecycle';
    /* Quy tắc (nguồn: stateflow-and-sharedflow, architecture/coroutines):
       - repeatOnLifecycle(STARTED) chạy khối trong coroutine mới mỗi lần lifecycle ở STARTED trở lên và hủy khi STOPPED.
       - viewModelScope: coroutine bị hủy khi ViewModel bị clear.
       - collect trực tiếp trong scope của màn hình thì vẫn chạy khi STOPPED, tới khi scope bị hủy (ở DESTROYED, mô hình giản lược). */
    function run(s) {
      var lc = 'started', col = s.collector === 'repeat' ? 'running' : 'running', vm = 'job.active', hidden = 0, outEv = [];
      var snap = function () { return { lc: lc, col: col, vm: vm, hidden: hidden }; };
      var seq = [{ a: 'start' }].concat(s.acts);
      seq.forEach(function (act, i) {
        var ev = [], key = act.a;
        if (act.a === 'background') {
          if (lc === 'started') {
            lc = 'stopped';
            if (s.collector === 'repeat' && col === 'running') { col = 'cancelled'; ev.push({ kind: 'cancel', subject: 'collector', key: 'cancelByLc' }); }
            else if (col === 'running') { ev.push({ kind: 'collect', subject: 'collector', key: 'stillCollect' }); }
          } else key = 'noop';
        } else if (act.a === 'foreground') {
          if (lc === 'stopped') {
            lc = 'started';
            if (s.collector === 'repeat' && col === 'cancelled') { col = 'running'; ev.push({ kind: 'launch', subject: 'collector', key: 'relaunch' }); }
            else ev.push({ kind: 'collect', subject: 'collector', key: 'keepCollect' });
          } else key = 'noop';
        } else if (act.a === 'finish') {
          if (lc !== 'destroyed') { lc = 'destroyed'; vm = 'job.cancelled'; if (col === 'running') { col = 'cancelled'; ev.push({ kind: 'cancel', subject: 'collector', key: s.collector === 'viewmodel' ? 'cancelByVm' : 'cancelByScope' }); } }
          else key = 'noop';
        } else if (act.a === 'start') {
          ev.push({ kind: 'launch', subject: 'collector', key: s.collector === 'repeat' ? 'startRepeat' : (s.collector === 'viewmodel' ? 'startVm' : 'startPlain') });
        }
        if (lc === 'stopped' && col === 'running') hidden += 3;     // giá trị nhận được khi màn hình không hiện (minh họa: 3 giá trị mỗi bước)
        outEv.push({ key: key, ev: ev, state: snap(), act: act });
      });
      return outEv;
    }
    function steps(s) {
      var out = [], P = { c: s.collector };
      run(s).forEach(function (r, i) {
        var ns = { screen: K + 'st.lc.' + r.state.lc, vm: r.state.vm, collector: r.state.col === 'running' ? K + 'st.running' : K + 'st.cancelledS' , flow: r.state.col === 'running' ? K + 'st.active' : K + 'st.idleS' };
        var o = step({ id: 'a' + i, type: i === 0 ? 'scenario' : 'experiment', titleKey: M(m, 's.' + r.key + '.title'), explainKey: M(m, 's.' + r.key + (r.key === 'start' ? '.explain.' + s.collector : '.explain')), params: P,
          activeNodes: r.key === 'start' ? ['screen', 'collector'] : (r.act.a === 'finish' ? ['screen', 'vm', 'collector'] : ['screen', 'collector']), nodeStates: ns,
          metrics: { hidden: r.state.hidden, collecting: r.state.col === 'running' ? M(m, 'val.yes') : M(m, 'val.no') },
          codeHighlight: { snippet: 'lifecycle', lines: s.collector === 'repeat' ? [1, 2, 3, 4] : s.collector === 'viewmodel' ? [6, 7] : [9, 10] },
          logEvents: r.ev.map(function (e, j) { return { t: i * 10 + j, kind: e.kind, subject: e.subject, detailKey: M(m, 'ev.' + e.key), params: P }; }) });
        if (i === 0) o.callouts = [{ kind: 'try', textKey: M(m, 'co.try') }];
        if (r.key === 'cancelByLc' || (r.act.a === 'background' && s.collector === 'repeat')) o.callouts = [{ kind: 'source', textKey: M(m, 'co.repeat') }];
        if (r.act.a === 'background' && s.collector !== 'repeat') o.callouts = [{ kind: 'pitfall', textKey: M(m, 'co.waste') }];
        if (r.key === 'noop') { o.skipped = [{ whatKey: M(m, 'sk.noop.what'), whyKey: M(m, 'sk.noop.why') }]; }
        if (r.act.a === 'finish') o.callouts = [{ kind: 'android', textKey: M(m, 'co.finish') }];
        out.push(o);
      });
      return out;
    }
    var BTN = function (id, a, icon) { return { id: id, type: 'button', labelKey: M(m, 'ctl.' + id), action: 'add', payload: { a: a }, icon: icon }; };
    ADE.registerModel('coroutines.lifecycle', {
      kind: 'discrete', titleKey: M(m, 'title'), overviewKey: M(m, 'overview'), wrapupKey: M(m, 'wrapup'), codeId: 'lifecycle',
      simplificationKeys: [M(m, 'simp.1'), M(m, 'simp.2')], controlsHintKey: M(m, 'ctl.hint'),
      controls: [
        { id: 'collector', type: 'select', labelKey: M(m, 'ctl.collector'), get: function (s) { return s.collector; }, action: 'collector', options: ['plain', 'repeat', 'viewmodel'].map(function (v) { return { value: v, labelKey: M(m, 'ctl.collector.' + v) }; }) },
        BTN('background', 'background', 'pause'), BTN('foreground', 'foreground', 'play'), BTN('finish', 'finish', 'remove'),
        { id: 'undo', type: 'button', labelKey: M(m, 'ctl.undo'), action: 'undo', icon: 'prev' }
      ],
      sampleStates: function () {
        var out = [], A = function (a) { return { a: a }; };
        var seqs = [['background', 'foreground'], ['background', 'finish'], ['finish'], ['background', 'background'], ['foreground'], ['finish', 'background'], ['background', 'foreground', 'background', 'finish']];
        ['plain', 'repeat', 'viewmodel'].forEach(function (c) { seqs.forEach(function (q) { out.push({ collector: c, acts: q.map(A) }); }); });
        return out;
      },
      init: function () { return { collector: 'repeat', acts: [] }; },
      act: function (s, a, v) {
        var n = { collector: s.collector, acts: s.acts.slice() };
        if (a === 'collector') n.collector = v; else if (a === 'add') { if (n.acts.length < 6) n.acts.push(v); } else if (a === 'undo') n.acts.pop();
        return n;
      },
      steps: steps,
      selfChecks: [
        { name: 'repeatOnLifecycle hủy khi STOPPED và chạy lại khi STARTED; collect thường vẫn chạy khi STOPPED', run: function () {
          var seq = [{ a: 'background' }, { a: 'foreground' }];
          var r = run({ collector: 'repeat', acts: seq }), p = run({ collector: 'plain', acts: seq });
          return r[1].state.col === 'cancelled' && r[2].state.col === 'running' && r[1].state.hidden === 0 && p[1].state.col === 'running' && p[1].state.hidden === 3;
        } },
        { name: 'viewModelScope chỉ bị hủy khi ViewModel clear (finish)', run: function () {
          var r = run({ collector: 'viewmodel', acts: [{ a: 'background' }, { a: 'finish' }] });
          return r[1].state.col === 'running' && r[2].state.col === 'cancelled' && r[2].state.vm === 'job.cancelled';
        } }
      ]
    });
  })();

  /* ================= A8b: LaunchedEffect và rememberCoroutineScope ================= */
  (function () {
    var m = 'effects';
    /* Quy tắc (nguồn: compose/side-effects, architecture/coroutines):
       - LaunchedEffect chạy coroutine khi vào Composition; hủy khi rời Composition; key đổi thì hủy coroutine cũ rồi chạy mới.
       - rememberCoroutineScope: scope nhận biết Composition để launch từ sự kiện UI; coroutine bị hủy khi composable rời Composition.
       - Recomposition với key không đổi không chạy lại LaunchedEffect. */
    function run(acts) {
      var inComp = true, key = 1, eff = 'running', sc = 'idle', launches = 1, trail = [{ key: 'enter', ev: [{ kind: 'launch', subject: 'effect', key: 'launchEffect' }], st: { inComp: true, key: 1, eff: 'running', sc: 'idle', launches: 1 }, a: 'enter' }];
      acts.forEach(function (act) {
        var ev = [], k = act.a;
        if (act.a === 'recompose') { if (!inComp) k = 'noop'; else ev.push({ kind: 'resume', subject: 'composable', key: 'recomposed' }); }
        else if (act.a === 'changeKey') {
          if (!inComp) k = 'noop'; else { key++; ev.push({ kind: 'cancel', subject: 'effect', key: 'cancelOld' }, { kind: 'launch', subject: 'effect', key: 'launchNew' }); launches++; eff = 'running'; }
        } else if (act.a === 'click') {
          if (!inComp) k = 'noop'; else { sc = 'running'; ev.push({ kind: 'launch', subject: 'scope', key: 'launchScope' }); }
        } else if (act.a === 'leave') {
          if (!inComp) k = 'noop'; else {
            inComp = false;
            if (eff === 'running') { eff = 'cancelled'; ev.push({ kind: 'cancel', subject: 'effect', key: 'cancelLeave' }); }
            if (sc === 'running') { sc = 'cancelled'; ev.push({ kind: 'cancel', subject: 'scope', key: 'cancelScope' }); }
          }
        }
        trail.push({ key: k, ev: ev, st: { inComp: inComp, key: key, eff: eff, sc: sc, launches: launches }, a: act.a });
      });
      return trail;
    }
    function steps(s) {
      return run(s.acts).map(function (r, i) {
        var st = r.st;
        var o = step({ id: 'a' + i, type: i === 0 ? 'scenario' : 'experiment', titleKey: M(m, 's.' + r.key + '.title'), explainKey: M(m, 's.' + r.key + '.explain'), params: { key: st.key },
          activeNodes: r.a === 'click' ? ['scope'] : (r.a === 'recompose' ? ['composable'] : ['effect']),
          nodeStates: { composable: st.inComp ? K + 'st.inComp' : K + 'st.outComp', effect: st.eff === 'running' ? K + 'st.running' : K + 'st.cancelledS', scope: st.sc === 'running' ? K + 'st.running' : (st.sc === 'cancelled' ? K + 'st.cancelledS' : K + 'st.idle') },
          metrics: { launches: st.launches, key: st.key },
          stateAfter: [{ labelKey: M(m, 'st.key'), value: st.key }],
          codeHighlight: { snippet: 'effects', lines: r.a === 'click' ? [5, 6] : [1, 2] },
          logEvents: r.ev.map(function (e, j) { return { t: i * 10 + j, kind: e.kind, subject: e.subject, detailKey: M(m, 'ev.' + e.key), params: { key: st.key } }; }) });
        if (i === 0) o.callouts = [{ kind: 'try', textKey: M(m, 'co.try') }];
        if (r.key === 'recompose') { o.skipped = [{ whatKey: M(m, 'sk.restart.what'), whyKey: M(m, 'sk.restart.why') }]; o.changes = [{ op: 'skip', textKey: M(m, 'ch.noRestart') }]; }
        if (r.key === 'changeKey') o.callouts = [{ kind: 'source', textKey: M(m, 'co.key') }];
        if (r.key === 'noop') { o.skipped = [{ whatKey: M(m, 'sk.noop.what'), whyKey: M(m, 'sk.noop.why') }]; }
        return o;
      });
    }
    var BTN = function (id, a, icon) { return { id: id, type: 'button', labelKey: M(m, 'ctl.' + id), action: 'add', payload: { a: a }, icon: icon }; };
    ADE.registerModel('coroutines.effects', {
      kind: 'discrete', titleKey: M(m, 'title'), overviewKey: M(m, 'overview'), wrapupKey: M(m, 'wrapup'), codeId: 'effects',
      simplificationKeys: [M(m, 'simp.1')], controlsHintKey: M(m, 'ctl.hint'),
      controls: [BTN('recompose', 'recompose', 'refresh'), BTN('changeKey', 'changeKey', 'set'), BTN('click', 'click', 'play'), BTN('leave', 'leave', 'remove'), { id: 'undo', type: 'button', labelKey: M(m, 'ctl.undo'), action: 'undo', icon: 'prev' }],
      sampleStates: function () {
        var A = function (a) { return { a: a }; };
        return [['recompose'], ['changeKey'], ['click'], ['leave'], ['leave', 'click'], ['leave', 'changeKey'], ['leave', 'recompose'], ['leave', 'leave'], ['click', 'changeKey', 'leave'], ['recompose', 'changeKey', 'click', 'leave']].map(function (q) { return { acts: q.map(A) }; });
      },
      init: function () { return { acts: [] }; },
      act: function (s, a, v) { var n = { acts: s.acts.slice() }; if (a === 'add') { if (n.acts.length < 6) n.acts.push(v); } else if (a === 'undo') n.acts.pop(); return n; },
      steps: steps,
      selfChecks: [
        { name: 'recompose không chạy lại; đổi key hủy cũ rồi chạy mới; rời Composition hủy tất cả', run: function () {
          var r = run([{ a: 'recompose' }, { a: 'changeKey' }, { a: 'click' }, { a: 'leave' }]);
          return r[1].st.launches === 1 && r[2].st.launches === 2 && r[2].st.key === 2 && r[3].st.sc === 'running' && r[4].st.eff === 'cancelled' && r[4].st.sc === 'cancelled' && r[4].st.inComp === false;
        } }
      ]
    });
  })();

  /* ================= A9a: race và các chiến lược bảo vệ trạng thái chung ================= */
  (function () {
    var m = 'race', INC = 3;
    /* Mỗi coroutine tăng bộ đếm INC lần; mỗi lần tăng = đọc rồi ghi (đọc → +1 → ghi). Kết quả đúng là 2 × INC.
       Thứ tự xen kẽ (interleaving) do người đọc chọn chỉ để MINH HỌA; race thật có kết quả không xác định.
       Nguồn: shared-mutable-state-and-concurrency (volatile không bảo đảm tính nguyên tử của thao tác lớn; Mutex, confinement, thread-safe structures). */
    var PATTERN = {
      seq: ['a', 'a', 'a', 'a', 'a', 'a', 'b', 'b', 'b', 'b', 'b', 'b'],
      alt: ['a', 'b', 'a', 'b', 'a', 'b', 'a', 'b', 'a', 'b', 'a', 'b'],
      heavy: ['a', 'b', 'b', 'a', 'a', 'b', 'b', 'a', 'a', 'b', 'b', 'a']
    };
    function run(s) {
      var c = 0, ev = [], local = { a: null, b: null }, left = { a: INC, b: INC }, phase = { a: 'R', b: 'R' }, lock = null, waiting = {};
      var order = PATTERN[s.pattern].slice(), t = 0, guard = 0;
      var queue = order.slice();
      var rec = function (kind, who, key, extra) { var e = { t: t, kind: kind, who: who, key: key, c: c }; if (extra) for (var k in extra) e[k] = extra[k]; ev.push(e); };
      while (queue.length && guard++ < 200) {
        var who = queue.shift();
        if (left[who] === 0) continue;
        if (s.strategy === 'mutex' && phase[who] === 'R') {
          if (lock && lock !== who) { if (!waiting[who]) { waiting[who] = true; t += 1; rec('suspend', who, 'waitLock'); } queue.push(who); if (queue.every(function (q) { return q === who; }) || true) { /* tiếp tục vòng */ } continue; }
          lock = who; if (waiting[who]) { waiting[who] = false; t += 1; rec('resume', who, 'gotLock'); } else { t += 1; rec('resume', who, 'lock'); }
        }
        t += 1;
        if (s.strategy === 'atomic') { c += 1; left[who]--; rec('run', who, 'atomicInc'); if (left[who] === 0) { t += 1; rec('complete', who, 'finish'); } continue; }
        if (phase[who] === 'R') { local[who] = c; phase[who] = 'W'; rec('run', who, 'read', { v: local[who] }); }
        else {
          var lost = c !== local[who];     // người khác đã ghi giữa lúc đọc và ghi
          c = local[who] + 1; left[who]--; phase[who] = 'R';
          rec('run', who, lost ? 'writeLost' : 'write', { v: c, lost: lost });
          if (s.strategy === 'mutex' && lock === who) { lock = null; t += 1; rec('run', who, 'unlock'); }
          if (left[who] === 0) { t += 1; rec('complete', who, 'finish'); }
        }
        if (s.strategy === 'confine' && phase[who] === 'W') { /* confinement: không có điểm suspend giữa đọc và ghi → luôn xong cả cặp */
          t += 1; var l2 = c !== local[who]; c = local[who] + 1; left[who]--; phase[who] = 'R'; rec('run', who, l2 ? 'writeLost' : 'write', { v: c, lost: l2 });
          if (left[who] === 0) { t += 1; rec('complete', who, 'finish'); }
        }
      }
      return { ev: ev, final: c, expected: INC * 2 };
    }
    function steps(s) {
      var r = run(s), out = [], lost = 0;
      r.ev.forEach(function (e, i) {
        if (e.lost) lost++;
        var p = { who: e.who === 'a' ? 'A' : 'B', v: e.v, c: e.c };
        var o = step({ id: 'e' + i, type: i === 0 ? 'scenario' : (e.key === 'writeLost' ? 'pitfall' : 'mechanism'), titleKey: M(m, 's.' + e.key + '.title'), explainKey: M(m, 's.' + e.key + '.explain'), params: p,
          activeNodes: ['counter', e.who], movingSignals: e.key === 'read' ? [{ edge: e.who === 'a' ? 'e1' : 'e2', tok: 'state' }] : [],
          nodeStates: {}, metrics: { counter: e.c, lost: lost, expected: r.expected }, stateAfter: [{ labelKey: M(m, 'st.counter'), value: e.c }],
          codeHighlight: { snippet: 'race', lines: s.strategy === 'mutex' ? [3, 4] : (s.strategy === 'atomic' ? [7] : [1, 2]) },
          logEvents: [{ t: e.t, kind: e.kind, subject: e.who, detailKey: M(m, 'ev.' + e.key), params: p }] });
        if (i === 0) o.callouts = [{ kind: 'try', textKey: M(m, 'co.try') }];
        if (e.key === 'writeLost') { o.changes = [{ op: 'remove', textKey: M(m, 'ch.lost'), params: p }]; o.callouts = [{ kind: 'pitfall', textKey: M(m, 'co.lost') }]; }
        out.push(o);
      });
      var last = out[out.length - 1];
      if (last) { last.callouts = (last.callouts || []).concat([{ kind: 'mechanism', textKey: M(m, 'co.' + s.strategy) }]); }
      return out;
    }
    ADE.registerModel('coroutines.race', {
      kind: 'discrete', titleKey: M(m, 'title'), overviewKey: M(m, 'overview'), wrapupKey: M(m, 'wrapup'), codeId: 'race',
      simplificationKeys: [M(m, 'simp.1'), K + 'simp.sched'], controlsHintKey: M(m, 'ctl.hint'),
      controls: [
        { id: 'strategy', type: 'select', labelKey: M(m, 'ctl.strategy'), get: function (s) { return s.strategy; }, action: 'strategy', options: ['none', 'mutex', 'confine', 'atomic'].map(function (v) { return { value: v, labelKey: M(m, 'ctl.strategy.' + v) }; }) },
        { id: 'pattern', type: 'select', labelKey: M(m, 'ctl.pattern'), get: function (s) { return s.pattern; }, action: 'pattern', options: ['seq', 'alt', 'heavy'].map(function (v) { return { value: v, labelKey: M(m, 'ctl.pattern.' + v) }; }) }
      ],
      init: function () { return { strategy: 'none', pattern: 'alt' }; },
      act: function (s, a, v) { var n = { strategy: s.strategy, pattern: s.pattern }; n[a] = v; return n; },
      steps: steps,
      selfChecks: [
        { name: 'không bảo vệ + xen kẽ: mất cập nhật (kết quả < 6); xen kẽ tuần tự thì ra 6 (tình cờ)', run: function () {
          return run({ strategy: 'none', pattern: 'alt' }).final < 6 && run({ strategy: 'none', pattern: 'heavy' }).final < 6 && run({ strategy: 'none', pattern: 'seq' }).final === 6;
        } },
        { name: 'Mutex, confinement, atomic: luôn đủ 6 với mọi xen kẽ đã thử', run: function () {
          var ok = true; ['mutex', 'confine', 'atomic'].forEach(function (st) { ['seq', 'alt', 'heavy'].forEach(function (p) { if (run({ strategy: st, pattern: p }).final !== 6) ok = false; }); });
          return ok;
        } }
      ]
    });
  })();

  /* ================= A9b: runTest và virtual time ================= */
  (function () {
    var m = 'vtime';
    /* Nguồn: kotlin/coroutines/test: runTest điều khiển virtual time qua TestCoroutineScheduler; advanceUntilIdle chạy mọi coroutine còn lại;
       advanceTimeBy chạy các coroutine được lên lịch TRƯỚC thời điểm đó; nếu code chuyển sang dispatcher khác (withContext) thì delay không còn bị bỏ qua. */
    var TASKS = [{ id: 'a', at: 1000 }, { id: 'b', at: 2500 }];
    function steps(s) {
      var out = [], vt = 0, done = {}, P = { by: s.by, a: 1000, b: 2500 };
      var snap = function () { var o = {}; TASKS.forEach(function (x) { o[x.id] = done[x.id] ? K + 'st.done' : K + 'st.suspended'; }); return o; };
      var mk = function (id, type, key, extra, logs) {
        var o = step({ id: id, type: type, titleKey: M(m, 's.' + key + '.title'), explainKey: M(m, 's.' + key + '.explain'), params: P, nodeStates: snap(), metrics: { vtime: vt, real: s.real ? M(m, 'val.real') : M(m, 'val.instant') }, logEvents: logs || [], codeHighlight: { snippet: 'vtime', lines: [] } });
        if (extra) extra(o); return o;
      };
      out.push(mk('setup', 'scenario', 'setup', function (o) { o.activeNodes = ['a', 'b']; o.codeHighlight.lines = [1, 2, 3, 4]; o.callouts = [{ kind: 'try', textKey: M(m, 'co.try') }]; },
        [{ t: 0, kind: 'launch', subject: 'a', detailKey: M(m, 'ev.launchA'), params: P }, { t: 0, kind: 'launch', subject: 'b', detailKey: M(m, 'ev.launchB'), params: P }, { t: 0, kind: 'suspend', subject: 'a', detailKey: M(m, 'ev.delayA'), params: P }, { t: 0, kind: 'suspend', subject: 'b', detailKey: M(m, 'ev.delayB'), params: P }]));
      var target = s.adv === 'by' ? s.by : 2500;
      var key = s.adv === 'by' ? 'advanceBy' : 'advanceIdle';
      out.push(mk('advance', 'mechanism', s.real ? 'advanceReal' : key, function (o) {
        o.activeNodes = ['clock']; o.codeHighlight.lines = s.adv === 'by' ? [5] : [6]; o.stateBefore = [{ labelKey: M(m, 'st.vtime'), value: 0 }];
        o.callouts = s.real ? [{ kind: 'pitfall', textKey: M(m, 'co.real') }] : [{ kind: 'source', textKey: M(m, 'co.scheduler') }];
      }, []));
      var order = s.adv === 'by' ? TASKS.filter(function (x) { return x.at < target; }) : TASKS;
      order.forEach(function (x, i) {
        vt = x.at; done[x.id] = true;
        out.push(mk('run' + x.id, 'mechanism', 'wake', function (o) {
          o.activeNodes = [x.id, 'clock']; o.stateAfter = [{ labelKey: M(m, 'st.vtime'), value: vt }]; o.codeHighlight.lines = [x.id === 'a' ? 2 : 3];
          o.params = { by: s.by, v: vt, task: x.id.toUpperCase() };
        }, [{ t: vt, kind: 'resume', subject: x.id, detailKey: M(m, 'ev.wake'), params: { v: vt, task: x.id.toUpperCase() } }, { t: vt, kind: 'complete', subject: x.id, detailKey: M(m, 'ev.done'), params: { task: x.id.toUpperCase() } }]));
      });
      vt = target;
      var pend = TASKS.filter(function (x) { return !done[x.id]; });
      out.push(mk('end', pend.length ? 'pitfall' : 'mechanism', pend.length ? 'endPending' : 'endAll', function (o) {
        o.activeNodes = ['clock']; o.codeHighlight.lines = [7]; o.params = { by: s.by, left: pend.length };
        if (pend.length) { o.skipped = [{ whatKey: M(m, 'sk.pending.what'), whyKey: M(m, 'sk.pending.why') }]; o.callouts = [{ kind: 'pitfall', textKey: M(m, 'co.pending') }]; }
      }, [{ t: vt, kind: 'complete', subject: 'clock', detailKey: M(m, pend.length ? 'ev.endPending' : 'ev.endAll'), params: { left: pend.length, v: vt } }]));
      return out;
    }
    ADE.registerModel('coroutines.vtime', {
      kind: 'discrete', titleKey: M(m, 'title'), overviewKey: M(m, 'overview'), wrapupKey: M(m, 'wrapup'), codeId: 'vtime',
      simplificationKeys: [M(m, 'simp.1'), K + 'simp.time'], controlsHintKey: M(m, 'ctl.hint'),
      controls: [
        { id: 'adv', type: 'select', labelKey: M(m, 'ctl.adv'), get: function (s) { return s.adv; }, action: 'adv', options: ['by', 'idle'].map(function (v) { return { value: v, labelKey: M(m, 'ctl.adv.' + v) }; }) },
        { id: 'by', type: 'select', labelKey: M(m, 'ctl.by'), get: function (s) { return s.by; }, action: 'by', options: [500, 1500, 3000].map(function (v) { return { value: v, labelKey: M(m, 'ctl.by.n'), params: { n: v } }; }) },
        { id: 'real', type: 'toggle', labelKey: M(m, 'ctl.real'), get: function (s) { return s.real; }, action: 'real' }
      ],
      init: function () { return { adv: 'by', by: 1500, real: false }; },
      act: function (s, a, v) { var n = { adv: s.adv, by: s.by, real: s.real }; if (a === 'real') n.real = !!v; else n[a] = v; return n; },
      steps: steps,
      selfChecks: [
        { name: 'advanceTimeBy(1500): chỉ A (1000) chạy, B (2500) còn chờ; advanceUntilIdle: cả hai, virtual time 2500', run: function () {
          var d = ADE.models['coroutines.vtime'], a = d.steps({ adv: 'by', by: 1500, real: false }), b = d.steps({ adv: 'idle', by: 1500, real: false });
          var comp = function (st) { var n = 0; st.forEach(function (x) { x.logEvents.forEach(function (e) { if (e.kind === 'complete' && (e.subject === 'a' || e.subject === 'b')) n++; }); }); return n; };
          return comp(a) === 1 && comp(b) === 2 && b[b.length - 1].metrics.vtime === 2500 && a[a.length - 1].metrics.vtime === 1500;
        } }
      ]
    });
  })();
})();
