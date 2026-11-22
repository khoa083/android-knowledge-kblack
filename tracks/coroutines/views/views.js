/* View của các model track coroutines. Mỗi model chọn DẠNG HÌNH hợp với bản chất khái niệm:
   - lanes (hàng × thời gian): ai chiếm luồng lúc nào → suspend, builders, context, cancel, flowpipe, race, vtime
   - tree (cha trên, con dưới): cây Job, lan lỗi, coroutine gắn với composable → jobtree, exception, effects
   - pipeline (trái → phải): dòng dữ liệu → hotcold, lifecycle
   - cycle (vòng): một vòng bấm → render → full
   Lõi vẽ; ở đây chỉ khai báo node, cạnh, dải chỉ số và hàm suy ra thanh thời gian từ nhật ký. Mọi nhãn là message key. */
(function () {
  'use strict';
  var K = 'track.coroutines.';
  var N = function (m, id, x, y, icon, tok, extra) { var n = { id: id, x: x, y: y, icon: icon, tok: tok, labelKey: K + 'm.' + m + '.n.' + id }; if (extra) for (var k in extra) n[k] = extra[k]; return n; };
  var E = function (id, from, to, labelKey) { return { id: id, from: from, to: to, labelKey: labelKey }; };
  var T = function (m, id) { return { id: id, labelKey: K + 'm.' + m + '.met.' + id }; };
  var TIME = { id: 'time', labelKey: K + 'met.time' };
  var base = function (m) { return { titleKey: K + 'm.' + m + '.diagramTitle', descKey: K + 'm.' + m + '.diagramDesc', captionKey: K + 'cap.' + m, famKeys: { wait: K + 'fam.wait', block: K + 'fam.block', idle: K + 'fam.idle' } }; };
  function V(m, cfg) { var v = base(m); for (var k in cfg) v[k] = cfg[k]; ADE.registerView('coroutines.' + m, v); }

  /* ---------- trợ giúp dựng thanh thời gian (lanes) ---------- */
  function Lanes(pos) { this.bars = []; this.marks = []; this.open = {}; this.pos = pos; }
  Lanes.prototype.start = function (row, t, kind, label, step, until) {
    this.end(row, t);
    var b = { row: row, from: t, to: null, kind: kind, label: label, cur: step === this.pos, until: until };
    this.bars.push(b); this.open[row] = b; return b;
  };
  Lanes.prototype.end = function (row, t) { var b = this.open[row]; if (b) { b.to = t; delete this.open[row]; } };
  Lanes.prototype.mark = function (row, t, label, step) { this.marks.push({ row: row, t: t, label: label, cur: step === this.pos }); };
  // thanh còn mở kéo tới "bây giờ"; thanh có thời lượng biết trước (block/delay) vẽ phần còn lại mờ
  Lanes.prototype.finish = function (now) {
    var self = this;
    Object.keys(this.open).forEach(function (r) { var b = self.open[r]; if (b.until != null && b.until > now) self.bars.push({ row: r, from: Math.max(now, b.from), to: b.until, kind: b.kind, ghost: true, label: now - b.from < 8 ? b.label : '' }); });
    this.bars.forEach(function (b) { if (b.to == null) b.to = Math.max(b.from, now); });
    return this;
  };
  // thời điểm "bây giờ" và độ dài trục từ dải chỉ số của các bước
  function clock(step, opts, metric) {
    metric = metric || 'time';
    var all = (opts.steps || []).map(function (s) { return (s.metrics && typeof s.metrics[metric] === 'number') ? s.metrics[metric] : 0; });
    var tMax = Math.max.apply(null, all.concat([10]));
    var now = step && step.metrics && typeof step.metrics[metric] === 'number' ? step.metrics[metric] : (opts.pos === 0 ? 0 : tMax);
    return { now: now, tMax: tMax };
  }
  var fam = function (f) { return ADE.t('app.fam.' + f); };
  var MK = function (k, p) { return ADE.t(K + 'mark.' + k, p); };

  V('full', {
    layout: 'cycle',
    nodes: [N('full', 'ui', 0, 4, 'screen', 'ui'), N('full', 'vm', 0, 0, 'job', 'coroutine'), N('full', 'repo', 4, 0, 'queue', 'thread'), N('full', 'state', 4, 4, 'store', 'state')],
    edges: [E('e1', 'ui', 'vm'), E('e2', 'vm', 'repo'), E('e3', 'repo', 'vm'), E('e4', 'vm', 'state'), E('e5', 'state', 'ui')],
    metrics: [T('full', 'state')], scopeKey: K + 'col.scope'
  });

  /* A1: hàng coroutine + hàng luồng; delay = viền đứt (luồng rảnh), block = gạch chéo (luồng bận) */
  V('suspend', {
    layout: 'lanes',
    nodes: [N('suspend', 'a', 0, 0, 'job', 'coroutine'), N('suspend', 'b', 0, 4, 'job', 'coroutine'), { id: 'th0', x: 4, y: 0, icon: 'thread', tok: 'thread', labelKey: K + 'n.th0' }, { id: 'th1', x: 4, y: 4, icon: 'thread', tok: 'thread', labelKey: K + 'n.th1' }],
    edges: [], metrics: [TIME], scopeKey: K + 'col.thread',
    lanes: function (events, step, opts) {
      var c = clock(step, opts), L = new Lanes(opts.pos);
      var first = (opts.steps && opts.steps[0] && opts.steps[0].nodeStates) || {};
      var rows = [{ id: 'a', labelKey: K + 'm.suspend.n.a', group: K + 'lanes.co' }, { id: 'b', labelKey: K + 'm.suspend.n.b', group: K + 'lanes.co' }, { id: 'th0', labelKey: K + 'n.th0', group: K + 'lanes.th' }];
      if (first.th1 && String(first.th1).indexOf('unused') < 0) rows.push({ id: 'th1', labelKey: K + 'n.th1', group: K + 'lanes.th' });
      events.forEach(function (x) {
        var e = x.e, task = e.subject, T0 = e.t, P = e.params || {}, th = /thread\.(th\d)/.exec(e.scope || ''), thr = th && th[1];
        var who = String(task).toUpperCase();
        if (e.kind === 'launch') L.start(task, T0, 'ready', '', x.step);
        else if (e.kind === 'resume') { L.start(task, T0, 'run', thr ? ADE.t(K + 'thread.' + thr) : '', x.step); if (thr) L.start(thr, T0, 'run', who, x.step); }
        else if (e.kind === 'block') { L.start(task, T0, 'block', MK('block', { ms: P.ms }), x.step, T0 + P.ms); if (thr) L.start(thr, T0, 'block', who, x.step, T0 + P.ms); }
        else if (e.kind === 'suspend') { L.start(task, T0, 'wait', MK('wait', { ms: P.ms }), x.step, T0 + P.ms); if (thr) L.end(thr, T0); }
        else if (e.kind === 'complete') { L.end(task, T0); if (thr) L.end(thr, T0); L.mark(task, T0, fam('done'), x.step); }
      });
      L.finish(c.now);
      return { rows: rows, bars: L.bars, marks: L.marks, tMax: c.tMax, now: c.now };
    }
  });

  /* U2: sequence builder. Hàng main, hàng khối sequence, hàng luồng duy nhất: thấy luồng thực thi nhảy qua lại ở mỗi next()/yield.
     Trục ngang là thứ tự bước (không phải thời gian thật). */
  V('seq', {
    layout: 'lanes',
    nodes: [N('seq', 'main', 0, 0, 'job', 'coroutine'), N('seq', 'gen', 0, 4, 'queue', 'coroutine'), N('seq', 'th', 4, 0, 'thread', 'thread')],
    edges: [], metrics: [{ id: 'val', labelKey: K + 'm.seq.met.val' }, { id: 'out', labelKey: K + 'm.seq.met.out' }], scopeKey: K + 'col.thread',
    barKeys: { run: K + 'm.seq.bar.run', ready: K + 'm.seq.bar.call', wait: K + 'm.seq.bar.wait' },
    lanes: function (events, step, opts) {
      var c = clock(step, opts), L = new Lanes(opts.pos), cur = { main: null, gen: null };
      var rows = [{ id: 'main', labelKey: K + 'm.seq.n.main', group: K + 'm.seq.lanes.code' }, { id: 'gen', labelKey: K + 'm.seq.n.gen', group: K + 'm.seq.lanes.code' }, { id: 'th', labelKey: K + 'm.seq.n.th', group: K + 'lanes.th' }];
      var KIND = { run: 'run', call: 'ready', wait: 'wait' };
      var LBL = { run: '', call: ADE.t(K + 'm.seq.lbl.call'), wait: ADE.t(K + 'm.seq.lbl.wait') };
      events.forEach(function (x) {
        var e = x.e, P = e.params || {}, t0 = e.t - 10;
        [['main', P.m], ['gen', P.g]].forEach(function (rs) {
          var row = rs[0], st = rs[1];
          if (st === cur[row]) return;
          cur[row] = st;
          if (KIND[st]) L.start(row, t0, KIND[st], LBL[st], x.step); else L.end(row, t0);
          if (st === 'done') L.mark(row, t0, fam('done'), x.step);
        });
        var who = P.m === 'run' ? 'main' : P.g === 'run' ? 'gen' : null;
        if (who !== cur.th) { cur.th = who; if (who) L.start('th', t0, 'run', ADE.t(K + 'm.seq.n.' + who), x.step); else L.end('th', t0); }
        if (e.kind === 'suspend' && P.v) L.mark('gen', t0, 'yield(' + P.v + ')', x.step);
      });
      L.finish(c.now);
      return { rows: rows, bars: L.bars, marks: L.marks, tMax: c.tMax, now: c.now, axisKey: K + 'm.seq.axis' };
    }
  });

  /* U3: coroutine, luồng main và luồng phụ/scheduler. Coroutine đang suspend không có luồng nào; luồng nào gọi resume thì chạy phần tiếp theo
     (trong suspend fun main không có dispatcher). Thời gian là minh hoạ. */
  V('cont', {
    layout: 'lanes',
    nodes: [N('cont', 'co', 0, 0, 'job', 'coroutine'), N('cont', 'th0', 4, 0, 'thread', 'thread'), N('cont', 'th1', 4, 4, 'thread', 'thread')],
    edges: [], metrics: [TIME, { id: 'on', labelKey: K + 'm.cont.met.on' }, { id: 'out', labelKey: K + 'm.cont.met.out' }], scopeKey: K + 'col.thread',
    barKeys: { wait: K + 'm.cont.bar.wait', ready: K + 'm.cont.bar.timer' },
    lanes: function (events, step, opts) {
      var c = clock(step, opts), L = new Lanes(opts.pos), cur = { co: null, th0: null, th1: null, done: 0 };
      var rows = [{ id: 'co', labelKey: K + 'm.cont.n.co', group: K + 'lanes.co' }, { id: 'th0', labelKey: K + 'm.cont.n.th0', group: K + 'lanes.th' }, { id: 'th1', labelKey: K + 'm.cont.n.th1', group: K + 'lanes.th' }];
      var CO = ADE.t(K + 'm.cont.lbl.co');
      events.forEach(function (x) {
        var e = x.e, P = e.params || {}, t0 = e.t;
        var want = {
          co: P.co === 'run' ? ['run', P.on ? ADE.t(K + 'm.cont.n.' + P.on) : ''] : P.co === 'wait' ? ['wait', ADE.t(K + 'm.cont.lbl.wait')] : null,
          th0: P.on === 'th0' ? ['run', CO] : null,
          th1: P.on === 'th1' ? ['run', CO] : P.t1 === 'run' ? ['run', ''] : P.t1 === 'block' ? ['block', 'Thread.sleep'] : P.t1 === 'timer' ? ['ready', ADE.t(K + 'm.cont.lbl.timer')] : null
        };
        ['co', 'th0', 'th1'].forEach(function (row) {
          var w = want[row], sig = w ? w.join('|') : '';
          if (sig === cur[row]) return;
          cur[row] = sig;
          if (w) L.start(row, t0, w[0], w[1], x.step, w[0] === 'block' ? P.to : null); else L.end(row, t0);
        });
        if (P.co === 'done' && !cur.done) { cur.done = 1; L.mark('co', t0, fam('done'), x.step); }
        if (e.kind === 'resume') L.mark('co', t0, 'resume', x.step);
        if (e.kind === 'exception') L.mark('co', t0, 'throw', x.step);
      });
      L.finish(c.now);
      return { rows: rows, bars: L.bars, marks: L.marks, tMax: c.tMax, now: c.now, axisKey: K + 'm.cont.axis' };
    }
  });

  /* U4: state machine của printUser. Ba thẻ trạng thái (label 0, 1, 2) theo hàng ngang; thẻ continuation bên dưới hiện label hiện tại;
     thẻ "người gọi" (completion) bên trái. Dải chỉ số = các trường của continuation + giá trị trả về + trạng thái luồng. */
  V('sm', {
    layout: 'pipeline',
    nodes: [N('sm', 'call', 0, 0, 'job', 'coroutine', { col: 0, row: 0 }), N('sm', 'l0', 0, 0, 'diamond', 'coroutine', { col: 1, row: 0 }), N('sm', 'l1', 0, 0, 'diamond', 'coroutine', { col: 2, row: 0 }),
            N('sm', 'l2', 0, 0, 'diamond', 'coroutine', { col: 3, row: 0 }), N('sm', 'cont', 0, 0, 'store', 'state', { col: 2, row: 1 })],
    edges: [E('e1', 'call', 'l0', K + 'm.sm.e.call'), E('e2', 'l0', 'l1', K + 'm.sm.e.l1'), E('e3', 'l1', 'l2', K + 'm.sm.e.l2'), E('e4', 'l2', 'call', K + 'm.sm.e.done')],
    metrics: [{ id: 'label', labelKey: K + 'm.sm.met.label' }, { id: 'userId', labelKey: K + 'm.sm.met.userId' }, { id: 'result', labelKey: K + 'm.sm.met.result' },
              { id: 'ret', labelKey: K + 'm.sm.met.ret' }, { id: 'th', labelKey: K + 'm.sm.met.th' }],
    scopeKey: K + 'col.thread', zoom: false
  });

  /* A2: vòng đời Job. Sáu thẻ trạng thái; token chạy dọc mũi tên chuyển trạng thái ở mỗi bước. */
  V('jobstate', {
    layout: 'pipeline', zoom: false,
    nodes: [N('jobstate', 'new', 0, 0, 'square', 'job', { col: 0, row: 0 }), N('jobstate', 'active', 0, 0, 'play', 'job', { col: 1, row: 0 }),
            N('jobstate', 'completing', 0, 0, 'clock', 'job', { col: 2, row: 0 }), N('jobstate', 'completed', 0, 0, 'check', 'job', { col: 3, row: 0 }),
            N('jobstate', 'cancelling', 0, 0, 'cross', 'job', { col: 2, row: 1 }), N('jobstate', 'cancelled', 0, 0, 'forbidden', 'job', { col: 3, row: 1 })],
    edges: [E('e1', 'new', 'active', K + 'm.jobstate.e.start'), E('e2', 'active', 'completing', K + 'm.jobstate.e.body'), E('e3', 'completing', 'completed', K + 'm.jobstate.e.kids'),
            E('e4', 'active', 'cancelling', K + 'm.jobstate.e.cancel'), E('e5', 'completing', 'cancelling', K + 'm.jobstate.e.cancel'), E('e6', 'cancelling', 'cancelled', K + 'm.jobstate.e.clean')],
    metrics: [{ id: 'isActive', labelKey: K + 'm.jobstate.met.isActive' }, { id: 'isCompleted', labelKey: K + 'm.jobstate.met.isCompleted' },
              { id: 'isCancelled', labelKey: K + 'm.jobstate.met.isCancelled' }, { id: 'kids', labelKey: K + 'm.jobstate.met.kids' }],
    scopeKey: K + 'm.jobstate.col.state'
  });

  /* CH: producer, buffer của channel, consumer theo thời gian (ms của mã). Thanh "buffer" ghi số phần tử đang nằm trong channel. */
  V('chan', {
    layout: 'lanes',
    nodes: [N('chan', 'prod', 0, 0, 'job', 'coroutine'), N('chan', 'chan', 4, 0, 'queue', 'flow'), N('chan', 'cons', 8, 0, 'job', 'coroutine')],
    edges: [], metrics: [TIME, { id: 'n', labelKey: K + 'm.chan.met.n' }, { id: 'sent', labelKey: K + 'm.chan.met.sent' }, { id: 'recv', labelKey: K + 'm.chan.met.recv' }, { id: 'dropped', labelKey: K + 'm.chan.met.dropped' }],
    scopeKey: K + 'm.chan.col.mode',
    barKeys: { run: K + 'm.chan.bar.run', wait: K + 'm.chan.bar.wait', ready: K + 'm.chan.bar.ready' },
    lanes: function (events, step, opts) {
      var c = clock(step, opts), L = new Lanes(opts.pos), cur = { prod: null, chan: null, cons: null };
      var rows = [{ id: 'prod', labelKey: K + 'm.chan.n.prod', group: K + 'lanes.co' }, { id: 'chan', labelKey: K + 'm.chan.n.chan', group: K + 'm.chan.lanes.ch' }, { id: 'cons', labelKey: K + 'm.chan.n.cons', group: K + 'lanes.co' }];
      var LB = function (k) { return ADE.t(K + 'm.chan.lbl.' + k); };
      events.forEach(function (x) {
        var e = x.e, P = e.params || {}, t0 = e.t;
        var want = {
          prod: P.p === 'suspended' ? ['wait', LB('suspended')] : P.p === 'done' ? null : ['run', ''],
          chan: P.n > 0 ? ['ready', String(P.n)] : null,
          cons: P.c === 'waiting' ? ['wait', LB('waiting')] : P.c === 'delay' ? (t0 < 1000 && e.kind !== 'collect' ? ['run', LB('start')] : ['run', LB('process')]) : null
        };
        ['prod', 'chan', 'cons'].forEach(function (row) {
          var w = want[row], sig = w ? w.join('|') : '';
          if (sig === cur[row]) return;
          cur[row] = sig;
          if (w) L.start(row, t0, w[0], w[1], x.step); else L.end(row, t0);
        });
        if (e.kind === 'collect') L.mark('cons', t0, String(P.v), x.step);
        if (e.kind === 'skip') L.mark('chan', t0, '✕' + P.v, x.step);
        if (e.kind === 'complete' && e.subject === 'prod') L.mark('prod', t0, 'close', x.step);
      });
      L.finish(c.now);
      return { rows: rows, bars: L.bars, marks: L.marks, tMax: Math.max(c.tMax, 1000), now: c.now, axisKey: K + 'm.chan.axis' };
    }
  });

  /* FL: chuỗi lời gọi của Flow. Ba hàng: collect (terminal), map, flowOf (builder). Thanh liền = đang chạy mã của hàng đó;
     thanh "đợi lời gọi" = đang chờ một lời gọi lồng (emit hoặc collect) trả về. Trục ngang là thứ tự bước. */
  V('flowcall', {
    layout: 'lanes',
    nodes: [N('flowcall', 't', 0, 0, 'screen', 'coroutine'), N('flowcall', 'm', 4, 0, 'diamond', 'flow'), N('flowcall', 'b', 8, 0, 'queue', 'flow')],
    edges: [], metrics: [{ id: 'out', labelKey: K + 'm.flowcall.met.out' }, { id: 'depth', labelKey: K + 'm.flowcall.met.depth' }], scopeKey: K + 'm.flowcall.col',
    barKeys: { run: K + 'm.flowcall.bar.run', ready: K + 'm.flowcall.bar.call' },
    lanes: function (events, step, opts) {
      var c = clock(step, opts), L = new Lanes(opts.pos), cur = { t: null, m: null, b: null };
      var rows = [{ id: 't', labelKey: K + 'm.flowcall.n.t', group: K + 'm.flowcall.lanes.g' }, { id: 'm', labelKey: K + 'm.flowcall.n.m', group: K + 'm.flowcall.lanes.g' }, { id: 'b', labelKey: K + 'm.flowcall.n.b', group: K + 'm.flowcall.lanes.g' }];
      var KIND = { run: 'run', call: 'ready' };
      events.forEach(function (x) {
        var e = x.e, P = e.params || {}, t0 = e.t - 10;
        [['t', P.T], ['m', P.Mm], ['b', P.Bb]].forEach(function (rs) {
          var row = rs[0], s = rs[1];
          if (s === cur[row]) return;
          cur[row] = s;
          if (KIND[s]) L.start(row, t0, KIND[s], s === 'call' ? ADE.t(K + 'm.flowcall.lbl.call') : '', x.step); else L.end(row, t0);
          if (s === 'done') L.mark(row, t0, fam('done'), x.step);
        });
        if (e.kind === 'emit' && P.v) L.mark(e.subject === 't' ? 'm' : 'b', t0, 'emit(' + P.v + ')', x.step);
        if (e.kind === 'collect' && P.v) L.mark('t', t0, 'print ' + P.v, x.step);
      });
      L.finish(c.now);
      return { rows: rows, bars: L.bars, marks: L.marks, tMax: c.tMax, now: c.now, axisKey: K + 'm.flowcall.axis' };
    }
  });

  /* FP: hàng theo trạng thái trong params.st, đánh dấu theo params.mk. Nhãn ở hàng "out" chỉ hiện cho bước hiện tại (tránh chồng chữ). */
  function stLanes(m, ids, waitLbl, noOut) {
    return function (events, step, opts) {
      var c = clock(step, opts), L = new Lanes(opts.pos), cur = {};
      var rows = (noOut ? ids : ids.concat(['out'])).map(function (id) { return { id: id, labelKey: K + 'm.' + m + '.n.' + id, group: K + 'lanes.co' }; });
      events.forEach(function (x) {
        var e = x.e, P = e.params || {}, st = P.st || {};
        ids.forEach(function (r) {
          var s = st[r] || 'off';
          if (s === cur[r]) return;
          cur[r] = s;
          if (s === 'run') L.start(r, e.t, 'run', '', x.step);
          else if (s === 'wait') L.start(r, e.t, 'wait', ADE.t(K + 'm.' + m + '.lbl.' + waitLbl), x.step);
          else L.end(r, e.t);
        });
        (P.mk || []).forEach(function (k) { L.mark(k[0], e.t, k[0] === 'out' && x.step !== opts.pos ? '' : k[1], x.step); });
      });
      L.finish(c.now);
      return { rows: rows, bars: L.bars, marks: L.marks, tMax: c.tMax, now: c.now, axisKey: K + 'm.' + m + '.axis' };
    };
  }
  V('combine', {
    layout: 'lanes',
    nodes: [N('combine', 'f1', 0, 0, 'queue', 'flow'), N('combine', 'f2', 0, 2, 'queue', 'flow'), N('combine', 'out', 4, 0, 'job', 'coroutine')],
    edges: [], metrics: [TIME, { id: 'out', labelKey: K + 'm.combine.met.out' }],
    scopeKey: K + 'm.combine.col', barKeys: { run: K + 'm.combine.bar.run', wait: K + 'm.combine.bar.wait' },
    lanes: stLanes('combine', ['f1', 'f2'], 'waitPair')
  });
  V('flatmap', {
    layout: 'lanes',
    nodes: [N('flatmap', 'A', 0, 0, 'queue', 'flow'), N('flatmap', 'B', 0, 2, 'queue', 'flow'), N('flatmap', 'C', 0, 4, 'queue', 'flow'), N('flatmap', 'out', 4, 0, 'job', 'coroutine')],
    edges: [], metrics: [TIME, { id: 'out', labelKey: K + 'm.flatmap.met.out' }, { id: 'act', labelKey: K + 'm.flatmap.met.act' }],
    scopeKey: K + 'm.flatmap.col', barKeys: { run: K + 'm.flatmap.bar.run', wait: K + 'm.flatmap.bar.wait' },
    lanes: stLanes('flatmap', ['A', 'B', 'C'], 'queued')
  });

  V('sharein', {
    layout: 'lanes',
    nodes: [N('sharein', 'up', 0, 0, 'queue', 'flow'), N('sharein', 's1', 4, 0, 'screen', 'ui'), N('sharein', 's2', 4, 2, 'screen', 'ui'), N('sharein', 's3', 4, 4, 'screen', 'ui')],
    edges: [], metrics: [TIME, { id: 'subs', labelKey: K + 'm.sharein.met.subs' }, { id: 'runs', labelKey: K + 'm.sharein.met.runs' }, { id: 'emitted', labelKey: K + 'm.sharein.met.emitted' }],
    scopeKey: K + 'm.sharein.col', barKeys: { run: K + 'm.sharein.bar.run', wait: K + 'm.sharein.bar.wait' },
    lanes: stLanes('sharein', ['up', 's1', 's2', 's3'], 'idle', true)
  });

  /* FB: producer (tải trang) và consumer (kiểm user) theo thời gian của mã. */
  V('paging', {
    layout: 'lanes',
    nodes: [N('paging', 'prod', 0, 0, 'queue', 'flow'), N('paging', 'cons', 4, 0, 'job', 'coroutine')],
    edges: [], metrics: [TIME, { id: 'pages', labelKey: K + 'm.paging.met.pages' }, { id: 'checked', labelKey: K + 'm.paging.met.checked' }],
    scopeKey: K + 'm.paging.col', barKeys: { run: K + 'm.paging.bar.run', wait: K + 'm.paging.bar.wait' },
    lanes: function (events, step, opts) {
      var c = clock(step, opts), L = new Lanes(opts.pos), cur = { prod: null, cons: null };
      var rows = [{ id: 'prod', labelKey: K + 'm.paging.n.prod', group: K + 'lanes.co' }, { id: 'cons', labelKey: K + 'm.paging.n.cons', group: K + 'lanes.co' }];
      var T = function (k, p) { return ADE.t(K + 'm.paging.lbl.' + k, p); };
      events.forEach(function (x) {
        var e = x.e, P = e.params || {}, t0 = e.t;
        var want = {
          prod: P.p === 'fetch' ? ['run', T('page', { n: P.page != null ? P.page : '' }) + '|' + t0] : P.p === 'wait' ? ['wait', T('waitEmit')] : null,
          cons: P.c === 'check' ? ['run', T('check', { n: P.u }) + '|' + t0] : P.c === 'wait' ? ['wait', T('waitItem')] : null
        };
        ['prod', 'cons'].forEach(function (row) {
          var w = want[row], sig = w ? w.join('|') : '';
          if (row === 'prod' && P.page == null && P.p === 'fetch') return;   // sự kiện của consumer: producer giữ nguyên thanh đang tải
          if (row === 'cons' && P.u == null && P.c === 'check') return;
          if (sig === cur[row]) return;
          cur[row] = sig;
          if (w) L.start(row, t0, w[0], w[1].split('|')[0], x.step, w[0] === 'run' ? t0 + 1000 : null); else L.end(row, t0);
        });
        if (e.kind === 'complete') L.mark('cons', t0, 'User3', x.step);
      });
      L.finish(c.now);
      return { rows: rows, bars: L.bars, marks: L.marks, tMax: Math.max(c.tMax, 6000), now: c.now, axisKey: K + 'm.paging.axis' };
    }
  });

  V('jobtree', {
    layout: 'tree',
    nodes: [N('jobtree', 'root', -2, -2, 'job', 'job'), N('jobtree', 'c1', 0, 4, 'job', 'coroutine'), N('jobtree', 'c2', 2, 2, 'job', 'coroutine'), N('jobtree', 'c3', 4, 0, 'job', 'coroutine'), N('jobtree', 'g', 6, 6, 'job', 'coroutine')],
    edges: [E('e1', 'root', 'c1'), E('e2', 'root', 'c2'), E('e3', 'root', 'c3'), E('e4', 'c2', 'g')],
    metrics: [T('jobtree', 'active'), T('jobtree', 'cancelled'), T('jobtree', 'failed')], subjectKey: K + 'col.job'
  });

  /* A3: mỗi hàng một coroutine; tuần tự = hai thanh nối đuôi, song song = hai thanh chồng thời gian */
  V('builders', {
    layout: 'lanes',
    nodes: [N('builders', 'parent', 0, 0, 'job', 'job'), N('builders', 'profile', 0, 4, 'job', 'coroutine'), N('builders', 'settings', 4, 0, 'job', 'coroutine')],
    edges: [E('e1', 'parent', 'profile'), E('e2', 'parent', 'settings')], metrics: [TIME],
    lanes: function (events, step, opts) {
      var c = clock(step, opts), L = new Lanes(opts.pos);
      var rows = ['parent', 'profile', 'settings'].map(function (id) { return { id: id, labelKey: K + 'm.builders.n.' + id, group: K + 'lanes.co' }; });
      events.forEach(function (x) {
        var e = x.e, r = e.subject;
        if (e.kind === 'launch') L.start(r, e.t, 'run', '', x.step);
        else if (e.kind === 'suspend') L.start(r, e.t, 'wait', MK('await'), x.step);
        else if (e.kind === 'resume') L.start(r, e.t, 'run', '', x.step);
        else if (e.kind === 'complete') { L.end(r, e.t); L.mark(r, e.t, fam('done'), x.step); }
        else if (e.kind === 'exception') { L.end(r, e.t); L.mark(r, e.t, fam('fail'), x.step); }
        else if (e.kind === 'cancel') { L.end(r, e.t); L.mark(r, e.t, fam('cancel'), x.step); }
      });
      L.finish(c.now);
      return { rows: rows, bars: L.bars, marks: L.marks, tMax: c.tMax, now: c.now };
    }
  });

  /* A4: hàng = luồng; thanh cho biết coroutine đang chạy ở đâu (withContext chuyển hàng) */
  V('context', {
    layout: 'lanes',
    nodes: [N('context', 'co', 0, 0, 'job', 'coroutine'), N('context', 'main', 4, 0, 'screen', 'ui'), N('context', 'pool', 4, 4, 'queue', 'thread')],
    edges: [E('e1', 'main', 'pool'), E('e2', 'pool', 'main')], metrics: [TIME], scopeKey: K + 'col.scope',
    lanes: function (events, step, opts) {
      var c = clock(step, opts), L = new Lanes(opts.pos), co = ADE.t(K + 'm.context.n.co');
      var rows = [{ id: 'main', labelKey: K + 'm.context.n.main', group: K + 'lanes.th' }, { id: 'pool', labelKey: K + 'm.context.n.pool', group: K + 'lanes.th' }];
      var rowOf = function (scope) { return /pool/.test(scope || '') ? 'pool' : 'main'; };
      events.forEach(function (x) {
        var e = x.e, r = rowOf(e.scope);
        if (e.kind === 'launch') L.start(r, e.t, 'ready', '', x.step);
        else if (e.kind === 'resume') { L.end(r === 'main' ? 'pool' : 'main', e.t); L.start(r, e.t, 'run', co, x.step); }
        else if (e.kind === 'block') L.start(r, e.t, 'block', co, x.step);
        else if (e.kind === 'suspend') { L.end(r, e.t); if (e.to === 'pool') L.start('pool', e.t, 'ready', '', x.step); }
        else if (e.kind === 'complete') { L.end('main', e.t); L.end('pool', e.t); L.mark(r, e.t, fam('done'), x.step); }
      });
      L.finish(c.now);
      return { rows: rows, bars: L.bars, marks: L.marks, tMax: c.tMax, now: c.now };
    }
  });

  /* A5: hủy là hợp tác — coroutine vẫn chạy tiếp tới điểm kiểm tra kế tiếp */
  V('cancel', {
    layout: 'lanes',
    nodes: [N('cancel', 'caller', 0, 0, 'screen', 'ui'), N('cancel', 'job', 4, 0, 'job', 'coroutine'), N('cancel', 'cleanup', 4, 4, 'store', 'job')],
    edges: [E('e1', 'caller', 'job'), E('e2', 'job', 'cleanup')], metrics: [T('cancel', 'units'), TIME],
    lanes: function (events, step, opts) {
      var c = clock(step, opts), L = new Lanes(opts.pos), last = 0;
      var rows = ['caller', 'job', 'cleanup'].map(function (id) { return { id: id, labelKey: K + 'm.cancel.n.' + id }; });
      events.forEach(function (x) {
        var e = x.e, P = e.params || {};
        if (e.subject === 'job' && e.kind === 'launch') { last = e.t; }
        else if (e.subject === 'job' && e.kind === 'run') { L.bars.push({ row: 'job', from: e.t - 100, to: e.t, kind: 'run', label: '#' + P.i, cur: x.step === opts.pos }); last = e.t; }
        else if (e.subject === 'job' && e.kind === 'check') L.mark('job', e.t, MK('check'), x.step);
        else if (e.subject === 'caller') L.mark('caller', e.t, MK('cancel'), x.step);
        else if (e.subject === 'cleanup') { if (e.kind === 'run') L.bars.push({ row: 'cleanup', from: e.t - 50, to: e.t, kind: 'run', label: 'finally', cur: x.step === opts.pos }); else L.mark('cleanup', e.t, MK('skipped'), x.step); }
        else if (e.subject === 'job') L.mark('job', e.t, fam(e.kind === 'complete' && !/Ignored|Swallowed/.test(e.detailKey) ? 'done' : (e.kind === 'exception' ? 'fail' : 'cancel')), x.step);
      });
      // đơn vị đang chạy dở (chưa xong) tới "bây giờ"
      if (step && last < c.now && step.metrics && step.metrics.units < 5) L.bars.push({ row: 'job', from: last, to: c.now, kind: 'run', label: '', cur: false });
      return { rows: rows, bars: L.bars, marks: L.marks, tMax: c.tMax, now: c.now };
    }
  });

  V('exception', {
    layout: 'tree',
    nodes: [N('exception', 'root', 0, 0, 'job', 'job'), N('exception', 'c1', 0, 4, 'job', 'coroutine', { parent: 'root' }), N('exception', 'c2', 4, 0, 'job', 'coroutine', { parent: 'root' }), N('exception', 'sink', 4, 4, 'store', 'error', { parent: null })],
    edges: [E('e1', 'c1', 'root'), E('e2', 'c2', 'root'), E('e3', 'root', 'sink')], metrics: [T('exception', 'state')]
  });

  /* A7a: hàng producer / bộ đệm / collector; thấy được phần tử chờ, bị bỏ, bị hủy giữa chừng */
  V('flowpipe', {
    layout: 'lanes',
    nodes: [N('flowpipe', 'producer', -1.5, 5.5, 'queue', 'flow'), N('flowpipe', 'map', 1, 3, 'chip', 'flow'), N('flowpipe', 'buf', 3.5, 0.5, 'queue', 'thread'), N('flowpipe', 'collector', 6, -2, 'job', 'coroutine')],
    edges: [E('e1', 'producer', 'map'), E('e2', 'map', 'buf'), E('e3', 'buf', 'collector')],
    metrics: [T('flowpipe', 'emitted'), T('flowpipe', 'processed'), T('flowpipe', 'dropped'), T('flowpipe', 'cancelled')],
    barKeys: { ready: K + 'bar.queued' },
    lanes: function (events, step, opts) {
      var c = clock(step, opts), L = new Lanes(opts.pos);
      var rows = [{ id: 'producer', labelKey: K + 'm.flowpipe.n.producer' }, { id: 'buf', labelKey: K + 'm.flowpipe.n.buf' }, { id: 'collector', labelKey: K + 'm.flowpipe.n.collector' }];
      var waiting = {}, proc = {};
      events.forEach(function (x) {
        var e = x.e, P = e.params || {}, it = '#' + P.item, cur = x.step === opts.pos;
        if (e.kind === 'emit') { L.mark('producer', e.t, it, x.step); waiting[P.item] = { row: 'buf', from: e.t, to: null, kind: 'ready', label: it, cur: cur }; L.bars.push(waiting[P.item]); }
        else if (e.kind === 'collect') { if (waiting[P.item]) waiting[P.item].to = e.t; proc[P.item] = { row: 'collector', from: e.t, to: null, kind: 'run', label: it, cur: cur }; L.bars.push(proc[P.item]); }
        else if (e.kind === 'complete') { if (proc[P.item]) proc[P.item].to = e.t; }
        else if (e.kind === 'skip') { if (waiting[P.item]) waiting[P.item].to = e.t; L.mark('buf', e.t, MK('dropped', { item: it }), x.step); }
        else if (e.kind === 'cancel') { if (proc[P.item]) proc[P.item].to = e.t; L.mark('collector', e.t, MK('cancelledItem', { item: it }), x.step); }
      });
      // phần tử phát ra mà không chờ (vào thẳng collector) có thanh chờ dài 0: bỏ đi cho gọn
      L.bars = L.bars.filter(function (b) { return !(b.kind === 'ready' && b.to != null && b.to === b.from); });
      L.finish(c.now);
      return { rows: rows, bars: L.bars, marks: L.marks, tMax: c.tMax, now: c.now };
    }
  });

  V('hotcold', {
    layout: 'pipeline',
    nodes: [N('hotcold', 'flow', 0, 0, 'queue', 'flow'), N('hotcold', 'a', 4, 0, 'job', 'coroutine'), N('hotcold', 'b', 0, 4, 'job', 'coroutine')],
    edges: [E('e1', 'flow', 'a'), E('e2', 'flow', 'b')], metrics: [T('hotcold', 'a'), T('hotcold', 'b')]
  });
  V('lifecycle', {
    layout: 'pipeline',
    nodes: [N('lifecycle', 'screen', 0, 0, 'screen', 'ui', { col: 0, row: 0 }), N('lifecycle', 'vm', 4, 0, 'chip', 'runtime', { col: 0, row: 1 }), N('lifecycle', 'flow', 4, 4, 'store', 'flow', { col: 1, row: 1 }), N('lifecycle', 'collector', 0, 4, 'job', 'coroutine', { col: 2, row: 0.5 })],
    edges: [E('e1', 'screen', 'collector'), E('e2', 'flow', 'collector')], metrics: [T('lifecycle', 'hidden'), T('lifecycle', 'collecting')]
  });
  V('effects', {
    layout: 'tree',
    nodes: [N('effects', 'composable', 0, 0, 'screen', 'ui'), N('effects', 'effect', 4, 0, 'job', 'coroutine'), N('effects', 'scope', 0, 4, 'queue', 'coroutine')],
    edges: [E('e1', 'composable', 'effect'), E('e2', 'composable', 'scope')], metrics: [T('effects', 'launches'), T('effects', 'key')]
  });

  /* A9a: hai coroutine xen kẽ đọc/ghi bộ đếm; trục ngang là THỨ TỰ thao tác (không phải thời gian thật) */
  V('race', {
    layout: 'lanes',
    nodes: [N('race', 'a', 0, 0, 'job', 'coroutine'), N('race', 'b', 0, 4, 'job', 'coroutine'), N('race', 'counter', 5, 3, 'store', 'state')],
    edges: [E('e1', 'a', 'counter'), E('e2', 'b', 'counter')], metrics: [T('race', 'counter'), T('race', 'lost'), T('race', 'expected')],
    lanes: function (events, step, opts) {
      var L = new Lanes(opts.pos), tMax = 0;
      (opts.steps || []).forEach(function (s) { (s.logEvents || []).forEach(function (e) { tMax = Math.max(tMax, e.t); }); });
      var now = step ? step.logEvents[0].t : (opts.pos === 0 ? 0 : tMax);
      var rows = [{ id: 'a', labelKey: K + 'm.race.n.a' }, { id: 'b', labelKey: K + 'm.race.n.b' }, { id: 'counter', labelKey: K + 'm.race.n.counter' }];
      var held = {};
      events.forEach(function (x) {
        var e = x.e, key = String(e.detailKey).split('.').pop(), P = e.params || {}, who = e.subject;
        if (key === 'read') { L.mark(who, e.t, MK('read', { v: P.v }), x.step); held[who] = L.start(who + '-h', e.t, 'run', '', x.step); }
        else if (key === 'write' || key === 'writeLost') { L.mark(who, e.t, MK(key === 'writeLost' ? 'lost' : 'write', { v: P.v }), x.step); L.start('counter', e.t, key === 'writeLost' ? 'block' : 'run', String(P.v), x.step); }
        else if (key === 'atomicInc') { L.mark(who, e.t, MK('inc'), x.step); L.start('counter', e.t, 'run', String(P.c), x.step); }
        else if (key === 'waitLock') L.mark(who, e.t, MK('waitLock'), x.step);
        else if (key === 'lock' || key === 'gotLock') L.mark(who, e.t, MK('lock'), x.step);
        else if (key === 'unlock') L.mark(who, e.t, MK('unlock'), x.step);
        else if (key === 'finish') L.mark(who, e.t, fam('done'), x.step);
      });
      L.bars = L.bars.filter(function (b) { return b.row === 'counter'; });
      L.finish(now);
      return { rows: rows, bars: L.bars, marks: L.marks, tMax: Math.max(4, tMax), now: now, axisKey: K + 'lanes.ord' };
    },
    barKeys: { run: K + 'bar.counter', block: K + 'bar.counterLost' }
  });

  /* A9b: thời gian ẢO của runTest; delay là thanh viền đứt, vạch "bây giờ" nhảy tức thì */
  V('vtime', {
    layout: 'lanes',
    nodes: [N('vtime', 'a', 0, 0, 'job', 'coroutine'), N('vtime', 'b', 0, 4, 'job', 'coroutine'), N('vtime', 'clock', 5, 3, 'chip', 'anim')],
    edges: [E('e1', 'clock', 'a'), E('e2', 'clock', 'b')], metrics: [T('vtime', 'vtime'), T('vtime', 'real')],
    lanes: function (events, step, opts) {
      var c = clock(step, opts, 'vtime'), L = new Lanes(opts.pos);
      c.tMax = Math.max(c.tMax, 2500);
      var rows = [{ id: 'a', labelKey: K + 'm.vtime.n.a' }, { id: 'b', labelKey: K + 'm.vtime.n.b' }];
      var at = { a: 1000, b: 2500 };
      events.forEach(function (x) {
        var e = x.e;
        if (e.kind === 'suspend' && at[e.subject]) L.start(e.subject, e.t, 'wait', MK('delay', { ms: at[e.subject] }), x.step, at[e.subject]);
        else if (e.kind === 'complete' && at[e.subject]) { L.end(e.subject, e.t); L.mark(e.subject, e.t, fam('done'), x.step); }
      });
      L.finish(c.now);
      return { rows: rows, bars: L.bars, marks: L.marks, tMax: c.tMax, now: c.now, axisKey: K + 'lanes.vt' };
    }
  });
})();
