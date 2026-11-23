/* Model track C (thuần, không DOM, không câu chữ; chỉ message key). MÔ HÌNH GIẢNG DẠY (simplified).
   Nguồn và phiên bản: docs/research/animation.md (compose.animation 1.13.0, BOM 2026.11.01). */
(function () {
  'use strict';
  var K = 'track.animation.', Ph = ADE.animPhys;
  var M = function (m, s) { return K + 'm.' + m + '.' + s; };
  var ST = function (s) { return K + 'st.' + s; };
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
    def.codeId = def.codeId || m; def.controlsHintKey = M(m, 'ctl.hint'); def.simplificationKeys = [M(m, 'simp.1')].concat(def.simpExtra || []);
    ADE.registerModel('animation.' + m, def);
  }
  var sel = function (m, id, vals, act) { return { id: id, type: 'select', labelKey: M(m, 'ctl.' + id), get: function (s) { return s[id]; }, action: act || id, options: vals.map(function (v) { return { value: v, labelKey: M(m, 'ctl.' + id + '.' + v) }; }) }; };
  var tog = function (m, id) { return { id: id, type: 'toggle', labelKey: M(m, 'ctl.' + id), get: function (s) { return !!s[id]; }, action: id }; };
  var setter = function (keys) { return function (s, a, v) { var n = {}; keys.forEach(function (k) { n[k] = s[k]; }); if (keys.indexOf(a) >= 0) n[a] = typeof s[a] === 'boolean' ? !!v : v; return n; }; };

  /* ================= C0: chọn API (choose-api là gợi ý, không phải luật; có chồng lấp) ================= */
  (function () {
    var m = 'choose', NEEDS = ['one', 'many', 'visibility', 'content', 'size', 'list', 'gesture', 'infinite', 'lowlevel'];
    function steps(s) {
      var n = s.need, P = {};
      return [
        S(m, 'need', { type: 'scenario', explainKey: M(m, 'need.' + n), activeNodes: ['need'], callouts: [{ kind: 'try', textKey: M(m, 'co.try') }], codeHighlight: { snippet: 'choose', lines: [] },
          logEvents: [{ t: 0, kind: 'observe', subject: 'need', detailKey: M(m, 'ctl.need.' + n) }] }),
        S(m, 'api', { explainKey: M(m, 'api.' + n), activeNodes: ['api'], movingSignals: [{ edge: 'e1', tok: 'anim' }], stateAfter: [{ labelKey: M(m, 'st.api'), valueKey: M(m, 'apiName.' + n) }],
          callouts: [{ kind: 'source', textKey: M(m, 'co.source') }], logEvents: [{ t: 1, kind: 'act', subject: 'api', detailKey: M(m, 'apiName.' + n) }] }),
        S(m, 'alt', { explainKey: M(m, 'alt.' + n), activeNodes: ['alt'], movingSignals: [{ edge: 'e2', tok: 'anim' }], callouts: [{ kind: 'mechanism', textKey: M(m, 'co.notRule') }],
          logEvents: [{ t: 2, kind: 'observe', subject: 'alt' }] })
      ];
    }
    reg(m, { controls: [sel(m, 'need', NEEDS)], init: function () { return { need: 'one' }; }, act: setter(['need']), steps: steps,
      selfChecks: [{ name: 'mỗi nhu cầu có 3 bước', run: function () { return NEEDS.every(function (n) { return steps({ need: n }).length === 3; }); } }] });
  })();

  /* ================= C3: updateTransition — nhiều thuộc tính theo một state; mỗi child có spec riêng ================= */
  var PROPS = ['color', 'size', 'alpha'];
  (function () {
    var m = 'transition';
    function steps(s) {
      var to = s.dir === 'expand' ? 'Expanded' : 'Collapsed', from = s.dir === 'expand' ? 'Collapsed' : 'Expanded', P = { from: from, to: to }, out = [], t = 0;
      var ns = { state: ST('target'), transition: ST('running') };
      out.push(S(m, 'target', { type: 'scenario', params: P, activeNodes: ['state', 'transition'], movingSignals: [{ edge: 'e0', tok: 'state' }],
        stateBefore: [{ labelKey: M(m, 'st.current'), value: from }, { labelKey: M(m, 'st.targetS'), value: from }], stateAfter: [{ labelKey: M(m, 'st.current'), value: from }, { labelKey: M(m, 'st.targetS'), value: to }],
        nodeStates: ns, codeHighlight: { snippet: 'transition', lines: [1, 2] }, callouts: [{ kind: 'try', textKey: M(m, 'co.try') }],
        logEvents: [{ t: t, kind: 'target-change', subject: 'state' }] }));
      var dur = 0;
      PROPS.forEach(function (p, i) {
        var on = s[p], spec = s.dir === 'expand' ? (p === 'size' ? 'spring' : 'tween') : 'tween', d = on ? (spec === 'spring' ? 400 : 300) : 0; dur = Math.max(dur, d);
        var nsi = JSON.parse(JSON.stringify(ns)); nsi[p] = on ? ST('animating') : ST('snapped');
        var o = S(m, 'p' + p, { titleKey: M(m, 's.prop.' + p + '.title'), explainKey: M(m, on ? 's.prop.' + p + '.' + spec : 's.prop.off'), params: { prop: p }, activeNodes: [p], movingSignals: [{ edge: 'e' + (i + 1), tok: 'anim' }],
          nodeStates: nsi, affected: [p], codeHighlight: { snippet: 'transition', lines: [3 + i] }, changes: [{ op: on ? 'set' : 'skip', textKey: M(m, 'ch.' + p + (on ? '' : '.snap')) }],
          logEvents: [{ t: t += 1, kind: on ? 'frame' : 'skip', subject: p, detailKey: M(m, on ? 'ev.anim.' + spec : 'ev.snap'), params: { ms: d } }] });
        if (!on) o.skipped = [{ whatKey: M(m, 'sk.anim'), whyKey: M(m, 'sk.off') }];
        out.push(o);
      });
      out.push(S(m, 'settle', { params: { to: to, ms: dur }, activeNodes: ['transition'], nodeStates: { state: ST('target'), transition: ST('settled') },
        stateAfter: [{ labelKey: M(m, 'st.current'), value: to }, { labelKey: M(m, 'st.targetS'), value: to }], callouts: [{ kind: 'source', textKey: M(m, 'co.settle') }],
        logEvents: [{ t: dur, kind: 'settle', subject: 'transition' }] }));
      out[out.length - 1].metrics = { children: PROPS.filter(function (p) { return s[p]; }).length, ms: dur };
      return out;
    }
    reg(m, { controls: [sel(m, 'dir', ['expand', 'collapse']), tog(m, 'color'), tog(m, 'size'), tog(m, 'alpha')],
      init: function () { return { dir: 'expand', color: true, size: true, alpha: true }; }, act: setter(['dir', 'color', 'size', 'alpha']), steps: steps,
      selfChecks: [{ name: 'tắt một child: thuộc tính đó nhảy thẳng, các child khác vẫn animate', run: function () { var st = steps({ dir: 'expand', color: true, size: false, alpha: true }); return st[2].logEvents[0].kind === 'skip' && st[1].logEvents[0].kind === 'frame'; } }] });
  })();

  /* ================= C4: hiện/ẩn và đổi nội dung (composables-modifiers) =================
     AnimatedVisibility: nội dung rời Composition SAU khi exit kết thúc; animation animate*AsState ngoài Transition không được theo dõi.
     AnimatedContent/Crossfade: trong lúc chuyển, cả nội dung cũ và mới cùng có mặt. */
  (function () {
    var m = 'visibility';
    function steps(s) {
      var out = [], t = 0, api = s.api;
      if (api === 'visibility') {
        var hide = s.action === 'hide';
        out.push(S(m, 'vtrigger', { type: 'scenario', explainKey: M(m, hide ? 's.vtrigger.hide' : 's.vtrigger.show'), activeNodes: ['trigger'], nodeStates: { a: hide ? ST('inComp') : ST('outComp') },
          codeHighlight: { snippet: 'visibility', lines: [1, 2] }, callouts: [{ kind: 'try', textKey: M(m, 'co.try') }], logEvents: [{ t: t, kind: 'target-change', subject: 'trigger' }] }));
        if (hide) {
          out.push(S(m, 'exit', { activeNodes: ['transition', 'a'], movingSignals: [{ edge: 'e1', tok: 'anim' }], nodeStates: { a: ST('exiting') }, stateAfter: [{ labelKey: M(m, 'st.inComp'), valueKey: M(m, 'val.yes') }],
            codeHighlight: { snippet: 'visibility', lines: [3] }, logEvents: [{ t: t += 10, kind: 'frame', subject: 'a' }] }));
          if (s.outside) out.push(S(m, 'outside', { type: 'pitfall', activeNodes: ['a'], nodeStates: { a: ST('exiting') }, callouts: [{ kind: 'pitfall', textKey: M(m, 'co.outside') }],
            codeHighlight: { snippet: 'visibility', lines: [5] }, logEvents: [{ t: t += 5, kind: 'interrupt', subject: 'a' }] }));
          out.push(S(m, 'removed', { activeNodes: ['a'], nodeStates: { a: ST('outComp') }, stateBefore: [{ labelKey: M(m, 'st.inComp'), valueKey: M(m, 'val.yes') }], stateAfter: [{ labelKey: M(m, 'st.inComp'), valueKey: M(m, 'val.no') }],
            changes: [{ op: 'remove', textKey: M(m, 'ch.removed') }], callouts: [{ kind: 'source', textKey: M(m, 'co.notAlpha') }], logEvents: [{ t: t += 300, kind: 'settle', subject: 'a' }] }));
        } else {
          out.push(S(m, 'enter', { activeNodes: ['transition', 'a'], movingSignals: [{ edge: 'e1', tok: 'anim' }], nodeStates: { a: ST('entering') }, stateBefore: [{ labelKey: M(m, 'st.inComp'), valueKey: M(m, 'val.no') }], stateAfter: [{ labelKey: M(m, 'st.inComp'), valueKey: M(m, 'val.yes') }],
            changes: [{ op: 'add', textKey: M(m, 'ch.added') }], codeHighlight: { snippet: 'visibility', lines: [3] }, logEvents: [{ t: t += 10, kind: 'frame', subject: 'a' }] }));
          out.push(S(m, 'shown', { activeNodes: ['a'], nodeStates: { a: ST('inComp') }, logEvents: [{ t: t += 300, kind: 'settle', subject: 'a' }] }));
        }
      } else {
        var isCf = api === 'crossfade';
        out.push(S(m, 'ctrigger', { type: 'scenario', explainKey: M(m, isCf ? 's.ctrigger.crossfade' : 's.ctrigger.content'), activeNodes: ['trigger'], nodeStates: { a: ST('inComp'), b: ST('outComp') },
          codeHighlight: { snippet: 'visibility', lines: isCf ? [10] : [7, 8] }, callouts: [{ kind: 'try', textKey: M(m, 'co.try') }], logEvents: [{ t: t, kind: 'target-change', subject: 'trigger' }] }));
        out.push(S(m, 'both', { explainKey: M(m, isCf ? 's.both.crossfade' : 's.both.content'), activeNodes: ['a', 'b'], movingSignals: [{ edge: 'e1', tok: 'anim' }, { edge: 'e2', tok: 'anim' }], nodeStates: { a: ST('exiting'), b: ST('entering') },
          stateAfter: [{ labelKey: M(m, 'st.present'), value: 'A, B' }], changes: [{ op: 'add', textKey: M(m, 'ch.bAdded') }],
          callouts: isCf ? [] : [{ kind: 'pitfall', textKey: M(m, s.lambda ? 'co.lambdaOk' : 'co.lambdaWrong') }], logEvents: [{ t: t += 10, kind: 'frame', subject: 'b' }] }));
        out.push(S(m, 'swap', { activeNodes: ['a'], nodeStates: { a: ST('outComp'), b: ST('inComp') }, stateAfter: [{ labelKey: M(m, 'st.present'), value: 'B' }],
          explainKey: M(m, !isCf && !s.lambda ? 's.swap.wrong' : 's.swap.explain'), changes: [{ op: 'remove', textKey: M(m, 'ch.aRemoved') }], logEvents: [{ t: t += 300, kind: 'settle', subject: 'a' }] }));
      }
      return out;
    }
    reg(m, { controls: [sel(m, 'api', ['visibility', 'content', 'crossfade']), sel(m, 'action', ['hide', 'show']), tog(m, 'outside'), tog(m, 'lambda')],
      init: function () { return { api: 'visibility', action: 'hide', outside: false, lambda: true }; }, act: setter(['api', 'action', 'outside', 'lambda']),
      steps: function (s) {
        var out = steps(s);
        // điều khiển không áp dụng ở cấu hình này → ghi chú lý do
        var notes = [];
        if (s.api !== 'visibility' && s.action !== 'hide') notes.push('co.actionVisOnly');
        if (s.api !== 'visibility' && s.outside) notes.push('co.outsideVisOnly');
        if (s.api === 'visibility' && !s.lambda) notes.push('co.contentOnly');
        if (s.api === 'visibility' && s.action === 'show' && s.outside) notes.push('co.hideOnly');
        if (s.api === 'crossfade' && !s.lambda) notes.push('co.contentOnly');
        notes.forEach(function (n) { out[0].callouts.push({ kind: 'mechanism', textKey: M(m, n) }); });
        return out;
      },
      selfChecks: [{ name: 'ẩn: nội dung rời Composition ở bước cuối, sau exit (không phải ngay khi alpha bắt đầu giảm)', run: function () {
        var st = steps({ api: 'visibility', action: 'hide', outside: false, lambda: true }); return st[1].nodeStates.a === ST('exiting') && st[st.length - 1].nodeStates.a === ST('outComp');
      } }] });
  })();

  /* ================= C5: kích thước — animateContentSize (layout) và graphicsLayer/offset {} (draw/placement) ================= */
  (function () {
    var m = 'size';
    function steps(s) {
      var lay = s.how === 'contentSize', out = [], t = 0;
      out.push(S(m, 'toggle', { type: 'scenario', explainKey: M(m, 's.toggle.' + s.how), activeNodes: ['card'], codeHighlight: { snippet: 'size', lines: s.how === 'contentSize' ? [1, 2, 3] : s.how === 'scale' ? [5, 6] : [8] },
        callouts: [{ kind: 'try', textKey: M(m, 'co.try') }], logEvents: [{ t: t, kind: 'target-change', subject: 'card' }] }));
      for (var f = 1; f <= s.frames; f++) {
        var o = S(m, 'f' + f, { titleKey: M(m, 's.frame.title'), explainKey: M(m, 's.frame.' + (lay ? 'layout' : 'draw')), params: { n: f }, activeNodes: lay ? ['card', 'layout', 'sibling'] : ['card', 'draw'],
          nodeStates: { layout: lay ? ST('rerun') : ST('skipped'), draw: ST('rerun'), sibling: lay ? ST('moved') : ST('overlap') }, affected: lay ? ['card', 'sibling'] : ['card'],
          logEvents: (lay ? [{ t: t += 16, kind: 'layout', subject: 'layout', params: { n: f } }] : [{ t: t += 16, kind: 'skip', subject: 'layout', detailKey: M(m, 'ev.noLayout'), params: { n: f } }]).concat([{ t: t, kind: 'draw', subject: 'draw', detailKey: M(m, 'ev.draw'), params: { n: f } }]) });
        if (!lay) o.skipped = [{ whatKey: M(m, 'sk.layout'), whyKey: M(m, 'sk.drawOnly') }];
        o.metrics = { layouts: lay ? f : 0, draws: f };
        out.push(o);
      }
      out.push(S(m, 'result', { explainKey: M(m, 's.result.' + (lay ? 'layout' : 'draw')), activeNodes: ['sibling'], nodeStates: { sibling: lay ? ST('moved') : ST('overlap') },
        callouts: [{ kind: lay ? 'source' : 'pitfall', textKey: M(m, lay ? 'co.order' : 'co.overlap') }], logEvents: [{ t: t += 10, kind: 'settle', subject: 'card' }] }));
      return out;
    }
    reg(m, { simpExtra: [M(m, 'simp.2')], controls: [sel(m, 'how', ['contentSize', 'scale', 'offset']), sel(m, 'frames', [3, 5])],
      init: function () { return { how: 'contentSize', frames: 3 }; }, act: function (s, a, v) { return a === 'how' ? { how: v, frames: s.frames } : { how: s.how, frames: v === 5 ? 5 : 3 }; }, steps: steps,
      selfChecks: [{ name: 'animateContentSize chạy layout mỗi frame; graphicsLayer chỉ draw', run: function () {
        var a = steps({ how: 'contentSize', frames: 3 }), b = steps({ how: 'scale', frames: 3 }); return a[3].metrics.layouts === 3 && b[3].metrics.layouts === 0;
      } }] });
  })();

  /* ================= C7: đọc animated value ở phase nào (phases, quick-guide) ================= */
  var PR = ADE.animPhaseRead = function (where) { return { comp: where === 'composition', layout: where !== 'draw', draw: true }; };
  (function () {
    var m = 'phaseread';
    function steps(s) {
      var r = PR(s.where), out = [], t = 0, n = { comp: 0, layout: 0, draw: 0 };
      out.push(S(m, 'where', { type: 'scenario', explainKey: M(m, 's.where.' + s.where), activeNodes: ['anim'], codeHighlight: { snippet: 'phaseread', lines: s.where === 'composition' ? [3] : s.where === 'layout' ? [5] : [7] },
        callouts: [{ kind: 'try', textKey: M(m, 'co.try') }], logEvents: [{ t: t, kind: 'observe', subject: 'anim', detailKey: M(m, 'ev.where.' + s.where) }] }));
      for (var f = 1; f <= s.frames; f++) {
        ['comp', 'layout', 'draw'].forEach(function (ph) { if (r[ph]) n[ph]++; });
        var o = S(m, 'f' + f, { titleKey: M(m, 's.frame.title'), explainKey: M(m, 's.frame.' + s.where), params: { n: f }, activeNodes: ['anim'].concat(['comp', 'layout', 'draw'].filter(function (ph) { return r[ph]; })),
          movingSignals: [{ edge: 'e1', tok: 'anim' }], nodeStates: { comp: r.comp ? ST('rerun') : ST('skipped'), layout: r.layout ? ST('rerun') : ST('skipped'), draw: ST('rerun') },
          logEvents: [{ t: t += 16, kind: 'frame', subject: 'anim', detailKey: M(m, 'ev.frame'), params: { n: f } }].concat(['comp', 'layout', 'draw'].map(function (ph) { return { t: t, kind: r[ph] ? (ph === 'comp' ? 'recompose' : ph) : 'skip', subject: ph, detailKey: M(m, r[ph] ? 'ev.run' : 'ev.skip'), params: { n: f } }; })) });
        if (!r.comp) o.skipped = [{ whatKey: M(m, 'sk.comp'), whyKey: M(m, 'sk.notRead') }];
        o.metrics = { comp: n.comp, layout: n.layout, draw: n.draw };
        out.push(o);
      }
      out.push(S(m, 'measure', { activeNodes: ['anim'], callouts: [{ kind: 'mechanism', textKey: M(m, 'co.measure') }, { kind: 'source', textKey: M(m, 'co.x3') }], logEvents: [{ t: t += 5, kind: 'settle', subject: 'anim' }] }));
      return out;
    }
    reg(m, { simpExtra: [M(m, 'simp.2')], controls: [sel(m, 'where', ['composition', 'layout', 'draw']), sel(m, 'frames', [3, 5])],
      init: function () { return { where: 'composition', frames: 3 }; }, act: function (s, a, v) { return a === 'where' ? { where: v, frames: s.frames } : { where: s.where, frames: v === 5 ? 5 : 3 }; }, steps: steps,
      selfChecks: [{ name: 'đọc trong graphicsLayer: 0 recomposition; trong body: recomposition mỗi frame', run: function () {
        var a = steps({ where: 'draw', frames: 3 }), b = steps({ where: 'composition', frames: 3 }); return a[3].metrics.comp === 0 && b[3].metrics.comp === 3;
      } }] });
  })();

  /* ================= C8: test clock (testing) — autoAdvance; advanceTimeBy làm tròn LÊN bội số frame duration ================= */
  var TC = ADE.animTestClock = {};
  TC.FRAME = 16;     // khoảng frame MINH HỌA của mô hình (tài liệu không ghi con số)
  TC.round = function (ms) { return Math.ceil(ms / TC.FRAME) * TC.FRAME; };
  TC.value = function (ms) { return Ph.sample({ from: 0, to: 100, spec: { type: 'tween', duration: 300, easing: 'FastOutSlowIn' } }, ms).value; };
  (function () {
    var m = 'testclock';
    function steps(s) {
      var req = 300 * s.at / 100, real = TC.round(req), out = [], P = { req: req, real: real, v: Math.round(TC.value(real) * 10) / 10 };
      out.push(S(m, 'start', { type: 'scenario', activeNodes: ['test', 'clock'], codeHighlight: { snippet: 'testclock', lines: s.auto ? [1, 2] : [1, 3] }, params: P,
        callouts: [{ kind: 'try', textKey: M(m, 'co.try') }], logEvents: [{ t: 0, kind: 'target-change', subject: 'test' }] }));
      if (s.auto) {
        out.push(S(m, 'auto', { activeNodes: ['clock', 'anim'], movingSignals: [{ edge: 'e1', tok: 'anim' }], params: P, stateAfter: [{ labelKey: M(m, 'st.value'), value: '100' }],
          logEvents: [{ t: 300, kind: 'settle', subject: 'anim' }] }));
      } else {
        out.push(S(m, 'paused', { activeNodes: ['clock'], params: P, stateAfter: [{ labelKey: M(m, 'st.value'), value: '0' }], codeHighlight: { snippet: 'testclock', lines: [3] }, logEvents: [{ t: 0, kind: 'interrupt', subject: 'clock' }] }));
        out.push(S(m, 'advance', { activeNodes: ['clock', 'anim'], movingSignals: [{ edge: 'e1', tok: 'anim' }], params: P, codeHighlight: { snippet: 'testclock', lines: [4] },
          stateBefore: [{ labelKey: M(m, 'st.req'), value: req + ' ms' }], stateAfter: [{ labelKey: M(m, 'st.real'), value: real + ' ms' }, { labelKey: M(m, 'st.value'), value: String(P.v) }],
          callouts: real !== req ? [{ kind: 'source', textKey: M(m, 'co.round') }] : [], logEvents: [{ t: real, kind: 'frame', subject: 'clock' }] }));
        out.push(S(m, 'assert', { activeNodes: ['test'], params: P, codeHighlight: { snippet: 'testclock', lines: [5] }, logEvents: [{ t: real, kind: 'observe', subject: 'test' }] }));
      }
      out.push(S(m, 'limits', { activeNodes: ['test'], params: P, callouts: [{ kind: 'mechanism', textKey: M(m, 'co.limits') }, { kind: 'android', textKey: M(m, 'co.x6') }], logEvents: [{ t: 400, kind: 'observe', subject: 'test' }] }));
      out[out.length - 1].metrics = { value: s.auto ? 100 : P.v, clock: s.auto ? 300 : real };
      if (s.auto && s.at !== 50) out[0].callouts.push({ kind: 'mechanism', textKey: M(m, 'co.atIgnored') });
      return out;
    }
    reg(m, { simpExtra: [M(m, 'simp.2')], controls: [tog(m, 'auto'), sel(m, 'at', [0, 25, 50, 75, 100])],
      init: function () { return { auto: false, at: 50 }; }, act: function (s, a, v) { return a === 'auto' ? { auto: !!v, at: s.at } : { auto: s.auto, at: [0, 25, 50, 75, 100].indexOf(+v) >= 0 ? +v : s.at }; }, steps: steps,
      selfChecks: [{ name: 'advanceTimeBy(75 ms) được làm tròn lên 80 ms (frame minh họa 16 ms)', run: function () { return TC.round(75) === 80 && TC.round(0) === 0 && TC.round(300) === 304; } }] });
  })();

  /* ================= lab (model compute, view tự vẽ ở views/lab.js) ================= */
  function labModel(id, kind, checks) {
    ADE.registerModel('animation.' + id, {
      kind: 'compute', titleKey: M(id, 'title'), labKind: kind,
      compute: function (inp) { var r = Ph.sample(inp.seg, inp.t); return { outputs: r, assumptionKeys: [K + 'lab.simp.1', K + 'lab.simp.2'], sourceIds: ['an-customize'] }; },
      checks: checks
    });
  }
  var sp = function (z, k) { return { type: 'spring', damping: z, stiffness: k }; };
  labModel('retarget', 'retarget', [
    { name: 'đổi target giữa chừng với spring: tiếp tục từ current, giữ velocity (không nhảy)', inputs: { seg: { from: 0, to: 100, v0: 0, spec: sp(1, 1500) }, t: 60 }, expect: function (r) {
      var c = r.outputs, seg2 = { from: c.value, to: 30, v0: c.velocity, spec: sp(1, 1500) }, r0 = Ph.sample(seg2, 0), r1 = Ph.sample(seg2, 1);
      return Math.abs(r0.value - c.value) < 1e-6 && Math.abs(r0.velocity - c.velocity) / Math.max(1, Math.abs(c.velocity)) < 0.05 && Math.abs(r1.value - c.value) < 2;
    } }
  ]);
  labModel('spec', 'spec', [
    { name: 'spring mặc định (NoBouncy, StiffnessMedium) tới target trong 1 s', inputs: { seg: { from: 0, to: 100, v0: 0, spec: sp(Ph.DAMPING.NoBouncy, Ph.STIFFNESS.Medium) }, t: 1000 }, expect: function (r) { return r.outputs.done && r.outputs.value === 100; } },
    { name: 'tween mặc định 300 ms: t=300 bằng target', inputs: { seg: { from: 0, to: 100, spec: { type: 'tween', duration: Ph.DEFAULT_DURATION, easing: 'FastOutSlowIn' } }, t: 300 }, expect: function (r) { return r.outputs.value === 100 && r.outputs.velocity === null; } },
    { name: 'snap(delay=150): trước 150 ms là start', inputs: { seg: { from: 0, to: 100, spec: { type: 'snap', delay: 150 } }, t: 149 }, expect: function (r) { return r.outputs.value === 0; } }
  ]);
  labModel('gesture', 'gesture', [
    { name: 'thả với vận tốc nhỏ: đích dự đoán bằng decay nằm trong biên → quay về 0', inputs: { seg: { from: 20, to: 0, v0: 200, spec: sp(0.75, 400) }, t: 3000 }, expect: function (r) {
      return Math.abs(Ph.decayTarget(20, 200, 1)) <= 120 && Math.abs(r.outputs.value) < 0.5;
    } }
  ]);
  /* ================= C1 (v2): animate*AsState bên trong (AnimateAsState.kt @296313a4) =================
     Lần đầu: remember tạo AnimateAsState(Animatable(target)), không SideEffect, không animation. Sau đó mỗi lần recompose: SideEffect gọi update();
     target khác animatable.targetValue → restartAnimation: job cũ bị cancel, coroutineScope.launch(UNDISPATCHED) { animatable.animateTo(target, spec) }.
     same: target bằng → không làm gì. interrupt: target đổi giữa chừng → job cũ cancel, animateTo mới chạy từ value hiện tại (Animatable giữ velocity). Số là minh họa. */
  (function () {
    var m = 'aas';
    var SC = ['first', 'change', 'interrupt', 'same'];
    function steps(s) {
      var sc = SC.indexOf(s.which) >= 0 ? s.which : 'change', out = [], t = 0, c = { launched: 0, cancelled: 0 }, target = sc === 'same' ? '100' : '0', value = sc === 'same' ? '100' : '0', job = '—';
      var P = function (key, o) {
        o.id = key.replace(/\./g, '_') + out.length; o.type = o.type || 'mechanism';
        o.titleKey = M(m, 's.' + key + '.title'); o.explainKey = M(m, 's.' + key + '.explain');
        o.params = o.params || {};
        o.metrics = { launched: c.launched, cancelled: c.cancelled, value: value };
        o.stateAfter = [{ labelKey: M(m, 'st.target'), value: target }, { labelKey: M(m, 'st.value'), value: value }, { labelKey: M(m, 'st.job'), value: job }];
        o.movingSignals = o.movingSignals || []; o.activeNodes = o.activeNodes || [];
        o.codeHighlight = { snippet: 'aas_impl', lines: o.lines || [] }; delete o.lines;
        o.logEvents = [{ t: t += 16, kind: o.kind || 'observe', subject: o.activeNodes[o.activeNodes.length - 1] || 'comp', detailKey: M(m, 'ev.' + key), params: o.params }]; delete o.kind;
        out.push(o);
      };
      var frames = function (vals, key) { vals.forEach(function (v) { value = String(v); P(key, { activeNodes: ['anim', 'comp'], movingSignals: [{ edge: 'e4', tok: 'anim' }], lines: [17], kind: 'frame', params: { v: v } }); }); };
      P('intro.' + sc, { type: 'scenario', activeNodes: ['comp'], lines: [1, 2], kind: 'observe' });
      if (sc === 'first') {
        P('create', { activeNodes: ['comp', 'state', 'anim'], movingSignals: [{ edge: 'e1', tok: 'state' }], lines: [3, 4, 5], kind: 'act', callouts: [{ kind: 'source', textKey: M(m, 'co.noSide') }] });
        P('read', { activeNodes: ['state', 'comp'], lines: [9], kind: 'observe' });
        P('end.first', { activeNodes: ['comp'], lines: [], kind: 'settle' });
        return out;
      }
      if (sc === 'same') {
        P('recomposeSame', { activeNodes: ['comp', 'state'], movingSignals: [{ edge: 'e1', tok: 'state' }], lines: [6, 7], kind: 'observe' });
        P('noop', { activeNodes: ['state'], lines: [11], kind: 'skip', callouts: [{ kind: 'source', textKey: M(m, 'co.same') }] });
        P('end.same', { activeNodes: ['comp'], lines: [], kind: 'settle' });
        return out;
      }
      target = '100';
      P('recompose', { activeNodes: ['comp', 'state'], movingSignals: [{ edge: 'e1', tok: 'state' }], lines: [6, 7], kind: 'target-change' });
      c.launched++; job = 'Active';
      P('launch', { activeNodes: ['state', 'job', 'anim'], movingSignals: [{ edge: 'e2', tok: 'job' }, { edge: 'e3', tok: 'anim' }], lines: [11, 15, 16], kind: 'act', callouts: [{ kind: 'source', textKey: M(m, 'co.launch') }] });
      if (sc === 'change') {
        frames([38, 81], 'frame');
        value = '100'; job = 'Completed';
        P('settle', { activeNodes: ['anim', 'comp'], lines: [18], kind: 'settle' });
        P('end.change', { activeNodes: ['comp'], lines: [], kind: 'settle', callouts: [{ kind: 'mechanism', textKey: M(m, 'co.read') }] });
        return out;
      }
      frames([52], 'frame');
      target = '40'; c.cancelled++; c.launched++; job = 'Active';
      P('retarget', { type: 'pitfall', activeNodes: ['comp', 'state', 'job'], movingSignals: [{ edge: 'e1', tok: 'state' }, { edge: 'e2', tok: 'error' }], lines: [6, 11, 13, 14, 15, 16], kind: 'interrupt', callouts: [{ kind: 'mechanism', textKey: M(m, 'co.velocity') }] });
      frames([61, 43], 'frame2');
      value = '40'; job = 'Completed';
      P('settle', { activeNodes: ['anim', 'comp'], lines: [18], kind: 'settle' });
      P('end.interrupt', { activeNodes: ['comp'], lines: [], kind: 'settle' });
      return out;
    }
    reg(m, {
      codeId: 'aas_impl',
      simpExtra: [M(m, 'simp.2')],
      controls: [sel(m, 'which', SC)],
      init: function () { return { which: 'change' }; },
      act: setter(['which']),
      steps: steps,
      selfChecks: [{ name: 'lần đầu: không launch; đổi target: 1 job, xong ở 100; đổi target giữa chừng: 2 job, 1 bị cancel, xong ở 40; target không đổi: không launch', run: function () {
        var last = function (w) { return steps({ which: w }).slice(-1)[0]; };
        var f = last('first'), c = last('change'), i = last('interrupt'), s = last('same');
        return f.metrics.launched === 0 && c.metrics.launched === 1 && c.stateAfter[1].value === '100' && i.metrics.launched === 2 && i.metrics.cancelled === 1 && i.stateAfter[1].value === '40' && s.metrics.launched === 0;
      } }]
    });
  })();
  /* ================= C2 (v2): spec làm việc trên AnimationVector (AnimationSpec.kt, VectorConverters.kt, ColorVectorConverter.kt, Easing.kt @296313a4) =================
     dp: Dp → AnimationVector1D, tween 300 ms FastOutSlowIn; tại 150 ms fraction ≈ 0.776 → 77.6 dp.
     offset: Offset → AnimationVector2D, spring: mỗi thành phần chạy riêng (số minh họa 60, 24).
     color: Color → AnimationVector4D(alpha, L, a, b) trong Oklab; Red (L .628, a .225, b .126) → White (1, 0, 0); tween tại 150 ms → (1, .917, .050, .028).
     keyframes: 0f@0, 80f@100, 60f@200, kết thúc 100f@300, LinearEasing giữa các mốc → tại 150 ms = 70. */
  (function () {
    var m = 'vector';
    var SC = ['dp', 'offset', 'color', 'keyframes'];
    var D = {
      dp: { from: '0.dp', to: '100.dp', vFrom: '[0]', vTo: '[100]', dim: 1, spec: 'tween(300, FastOutSlowInEasing)', vMid: '[77.6]', mid: '77.6.dp' },
      offset: { from: 'Offset(0, 0)', to: 'Offset(100, 40)', vFrom: '[0, 0]', vTo: '[100, 40]', dim: 2, spec: 'spring()', vMid: '[60, 24]', mid: 'Offset(60, 24)' },
      color: { from: 'Color.Red', to: 'Color.White', vFrom: '[1, .628, .225, .126]', vTo: '[1, 1, 0, 0]', dim: 4, spec: 'tween(300, FastOutSlowInEasing)', vMid: '[1, .917, .050, .028]', mid: 'Oklab → sRGB' },
      keyframes: { from: '0f', to: '100f', vFrom: '[0]', vTo: '[100]', dim: 1, spec: 'keyframes { 80f at 100; 60f at 200 }', vMid: '[70]', mid: '70f' }
    };
    function steps(s) {
      var sc = SC.indexOf(s.which) >= 0 ? s.which : 'dp', d = D[sc], out = [], t = 0, val = d.from, vec = '—', spec = '—';
      var P = function (key, o) {
        o.id = key.replace(/\./g, '_') + out.length; o.type = o.type || 'mechanism';
        o.titleKey = M(m, 's.' + key + '.title'); o.explainKey = M(m, 's.' + key + '.explain');
        o.params = o.params || {};
        o.metrics = { dim: d.dim };
        o.stateAfter = [{ labelKey: M(m, 'st.value'), value: val }, { labelKey: M(m, 'st.vector'), value: vec }, { labelKey: M(m, 'st.spec'), value: spec }];
        o.movingSignals = o.movingSignals || []; o.activeNodes = o.activeNodes || [];
        o.codeHighlight = { snippet: 'vector_' + sc, lines: o.lines || [] }; delete o.lines;
        o.logEvents = [{ t: t += 50, kind: o.kind || 'observe', subject: o.activeNodes[o.activeNodes.length - 1] || 'value', detailKey: M(m, 'ev.' + key), params: o.params }]; delete o.kind;
        out.push(o);
      };
      P('intro.' + sc, { type: 'scenario', activeNodes: ['value'], lines: [1, 2], kind: 'target-change' });
      vec = d.vFrom + ' → ' + d.vTo;
      P('convert.' + sc, { activeNodes: ['value', 'conv', 'vec'], movingSignals: [{ edge: 'e1', tok: 'state' }, { edge: 'e2', tok: 'state' }], lines: [3], kind: 'act', callouts: sc === 'color' ? [{ kind: 'source', textKey: M(m, 'co.oklab') }] : [] });
      spec = d.spec;
      P('vectorize', { activeNodes: ['spec', 'vec'], movingSignals: [{ edge: 'e3', tok: 'anim' }], lines: [4], kind: 'act', params: { n: d.dim }, callouts: [{ kind: 'source', textKey: M(m, 'co.vectorize') }] });
      vec = d.vMid;
      P('frame.' + sc, { activeNodes: ['spec', 'vec'], movingSignals: [{ edge: 'e3', tok: 'anim' }], lines: [5], kind: 'frame' });
      val = d.mid;
      P('back.' + sc, { activeNodes: ['vec', 'conv', 'value'], movingSignals: [{ edge: 'e4', tok: 'anim' }], lines: [6], kind: 'frame' });
      val = d.to; vec = d.vTo;
      P('end.' + sc, { activeNodes: ['value'], lines: [], kind: 'settle', callouts: [{ kind: 'mechanism', textKey: M(m, 'co.end.' + sc) }] });
      return out;
    }
    reg(m, {
      codeId: 'vector_dp',
      simpExtra: [M(m, 'simp.2')],
      controls: [sel(m, 'which', SC)],
      init: function () { return { which: 'dp' }; },
      act: setter(['which']),
      steps: steps,
      selfChecks: [{ name: 'Dp → 1D, Offset → 2D, Color → 4D (Oklab); FastOutSlowIn(0.5) ≈ 0.776 nên Dp ở 150 ms ≈ 77.6; keyframes tuyến tính giữa 80@100 và 60@200 cho 70 ở 150 ms', run: function () {
        var bez = function (p1, p2, u) { return 3 * (1 - u) * (1 - u) * u * p1 + 3 * (1 - u) * u * u * p2 + u * u * u; };
        var lo = 0, hi = 1; for (var i = 0; i < 60; i++) { var mid = (lo + hi) / 2; if (bez(0.4, 0.2, mid) < 0.5) lo = mid; else hi = mid; }
        var y = bez(0, 1, lo), kf = 80 + (60 - 80) * (150 - 100) / 100;
        return Math.abs(y - 0.776) < 0.002 && kf === 70 && D.dp.dim === 1 && D.offset.dim === 2 && D.color.dim === 4 && steps({ which: 'color' }).length === 6;
      } }]
    });
  })();
  /* ================= C3 (v2): một Transition, nhiều con, currentState (Transition.kt @296313a4) =================
     expand: Collapsed → Expanded; con: alpha tween 150, color tween 300, height spring (~400 ms, minh họa). currentState giữ Collapsed tới khi MỌI con xong.
     reverse: tại 150 ms target đổi về Collapsed; các con đổi hướng; currentState vẫn Collapsed, xong thì isRunning = false.
     mutable: MutableTransitionState(Collapsed).apply { targetState = Expanded } → chạy ngay khi vào composition (updateTransition thì không). */
  (function () {
    var m = 'segment';
    var SC = ['expand', 'reverse', 'mutable'];
    function steps(s) {
      var sc = SC.indexOf(s.which) >= 0 ? s.which : 'expand', out = [], t = 0, run = 0, ms = 0, cur = 'Collapsed', tgt = 'Collapsed', running = 'false';
      var snip = sc === 'mutable' ? 'seg_mutable' : 'seg_update';
      var P = function (key, o) {
        o.id = key.replace(/\./g, '_') + out.length; o.type = o.type || 'mechanism';
        o.titleKey = M(m, 's.' + key + '.title'); o.explainKey = M(m, 's.' + key + '.explain');
        o.params = o.params || {};
        o.metrics = { running: run, ms: ms };
        o.stateAfter = [{ labelKey: M(m, 'st.target'), value: tgt }, { labelKey: M(m, 'st.current'), value: cur }, { labelKey: M(m, 'st.running'), value: running }];
        o.movingSignals = o.movingSignals || []; o.activeNodes = o.activeNodes || [];
        o.codeHighlight = { snippet: snip, lines: o.lines || [] }; delete o.lines;
        o.logEvents = [{ t: t = ms, kind: o.kind || 'frame', subject: o.activeNodes[o.activeNodes.length - 1] || 'state', detailKey: M(m, 'ev.' + key), params: o.params }]; delete o.kind;
        out.push(o);
      };
      var kids = [{ edge: 'e1', tok: 'anim' }, { edge: 'e2', tok: 'anim' }, { edge: 'e3', tok: 'anim' }];
      P('intro.' + sc, { type: 'scenario', activeNodes: ['state', 'transition'], lines: [1, 2], kind: 'observe' });
      tgt = 'Expanded'; run = 3; running = 'true';
      P(sc === 'mutable' ? 'enter' : 'target', { activeNodes: ['state', 'transition', 'alpha', 'color', 'height'], movingSignals: [{ edge: 'e0', tok: 'state' }].concat(kids), lines: sc === 'mutable' ? [1, 2] : [2], kind: 'target-change',
        callouts: sc === 'mutable' ? [{ kind: 'source', textKey: M(m, 'co.mutable') }] : [] });
      if (sc === 'reverse') {
        ms = 150; tgt = 'Collapsed';
        P('reverse', { type: 'pitfall', activeNodes: ['state', 'transition', 'alpha', 'color', 'height'], movingSignals: [{ edge: 'e0', tok: 'error' }].concat(kids), lines: [2], kind: 'interrupt', callouts: [{ kind: 'source', textKey: M(m, 'co.adjust') }] });
        ms = 300; run = 1;
        P('rev.mostDone', { activeNodes: ['transition', 'height'], movingSignals: [{ edge: 'e3', tok: 'anim' }], lines: [5, 6], kind: 'frame' });
        ms = 450; run = 0; running = 'false';
        P('rev.done', { activeNodes: ['transition', 'state'], lines: [8], kind: 'settle' });
        P('end.reverse', { activeNodes: ['state'], lines: [], kind: 'settle' });
        return out;
      }
      ms = 150; run = 2;
      P('alphaDone', { activeNodes: ['transition', 'alpha'], movingSignals: [{ edge: 'e1', tok: 'anim' }], lines: [7, 8], kind: 'settle', callouts: [{ kind: 'source', textKey: M(m, 'co.current') }] });
      ms = 300; run = 1;
      P('colorDone', { activeNodes: ['transition', 'color'], movingSignals: [{ edge: 'e2', tok: 'anim' }], lines: [3], kind: 'settle' });
      ms = 400; run = 0; cur = 'Expanded'; running = 'false';
      P('allDone', { activeNodes: ['transition', 'height', 'state'], movingSignals: [{ edge: 'e3', tok: 'anim' }], lines: [4, 5, 6, 8], kind: 'settle' });
      P('end.' + sc, { activeNodes: ['state'], lines: [], kind: 'settle', callouts: [{ kind: 'mechanism', textKey: M(m, 'co.end.' + sc) }] });
      return out;
    }
    reg(m, {
      codeId: 'seg_update',
      simpExtra: [M(m, 'simp.2')],
      controls: [sel(m, 'which', SC)],
      init: function () { return { which: 'expand' }; },
      act: setter(['which']),
      steps: steps,
      selfChecks: [{ name: 'currentState giữ Collapsed tới khi cả ba con xong (400 ms) rồi thành Expanded; đổi hướng giữa chừng: currentState vẫn Collapsed và cuối cùng isRunning = false; MutableTransitionState chạy ngay khi vào composition', run: function () {
        var x = steps({ which: 'expand' }), r = steps({ which: 'reverse' }), mu = steps({ which: 'mutable' });
        var byId = function (arr, p) { return arr.filter(function (o) { return o.id.indexOf(p) === 0; })[0]; };
        return byId(x, 'colorDone').stateAfter[1].value === 'Collapsed' && byId(x, 'allDone').stateAfter[1].value === 'Expanded' &&
          r[r.length - 1].stateAfter[1].value === 'Collapsed' && r[r.length - 1].stateAfter[2].value === 'false' && mu[1].metrics.running === 3;
      } }]
    });
  })();
  /* ================= C4 (v2): khi nào nội dung rời composition (AnimatedVisibility.kt @296313a4) =================
     builtin: visible → false: fadeOut + shrinkOut chạy (300 ms minh họa); nội dung còn trong composition tới khi xong rồi bị gỡ.
     custom: thêm animation tùy biến trên transition của AnimatedVisibilityScope (500 ms) → AnimatedVisibility chờ cả nó rồi mới gỡ.
     outside: animateFloatAsState trong content (500 ms) KHÔNG thuộc Transition → nội dung bị gỡ ở 300 ms, animation đó bị cắt. */
  (function () {
    var m = 'exitlife';
    var SC = ['builtin', 'custom', 'outside'];
    function steps(s) {
      var sc = SC.indexOf(s.which) >= 0 ? s.which : 'builtin', out = [], ms = 0, inComp = 'true', vis = 'true', run = '—';
      var P = function (key, o) {
        o.id = key.replace(/\./g, '_') + out.length; o.type = o.type || 'mechanism';
        o.titleKey = M(m, 's.' + key + '.title'); o.explainKey = M(m, 's.' + key + '.explain');
        o.params = o.params || {};
        o.metrics = { ms: ms, inComp: inComp === 'true' ? 1 : 0 };
        o.stateAfter = [{ labelKey: M(m, 'st.visible'), value: vis }, { labelKey: M(m, 'st.inComp'), value: inComp }, { labelKey: M(m, 'st.running'), value: run }];
        o.movingSignals = o.movingSignals || []; o.activeNodes = o.activeNodes || [];
        o.codeHighlight = { snippet: 'exit_' + sc, lines: o.lines || [] }; delete o.lines;
        o.logEvents = [{ t: ms, kind: o.kind || 'frame', subject: o.activeNodes[o.activeNodes.length - 1] || 'content', detailKey: M(m, 'ev.' + key), params: o.params }]; delete o.kind;
        out.push(o);
      };
      P('intro.' + sc, { type: 'scenario', activeNodes: ['flag', 'av', 'content'], lines: [1, 2], kind: 'observe' });
      vis = 'false'; run = sc === 'builtin' ? 'fadeOut + shrinkOut' : sc === 'custom' ? 'fadeOut + shrinkOut + custom' : 'fadeOut + shrinkOut | animateFloatAsState';
      P('hide', { activeNodes: ['flag', 'av', 'content'], movingSignals: [{ edge: 'e1', tok: 'state' }, { edge: 'e2', tok: 'anim' }], lines: [1, 3], kind: 'target-change', callouts: [{ kind: 'source', textKey: M(m, 'co.stillThere') }] });
      ms = 150;
      P('mid', { activeNodes: ['av', 'content'], movingSignals: [{ edge: 'e2', tok: 'anim' }], lines: [3], kind: 'frame' });
      ms = 300;
      if (sc === 'custom') {
        run = 'custom';
        P('waitCustom', { activeNodes: ['av', 'content'], movingSignals: [{ edge: 'e2', tok: 'anim' }], lines: [5, 6], kind: 'frame', callouts: [{ kind: 'source', textKey: M(m, 'co.waitAll') }] });
        ms = 500;
      }
      if (sc === 'outside') {
        inComp = 'false'; run = '—';
        P('cut', { type: 'pitfall', activeNodes: ['av', 'gone'], movingSignals: [{ edge: 'e3', tok: 'error' }], lines: [5, 6], kind: 'interrupt', callouts: [{ kind: 'pitfall', textKey: M(m, 'co.outside') }] });
      } else {
        inComp = 'false'; run = '—';
        P('removed', { activeNodes: ['av', 'gone'], movingSignals: [{ edge: 'e3', tok: 'runtime' }], lines: [3], kind: 'settle' });
      }
      P('end.' + sc, { type: sc === 'outside' ? 'pitfall' : 'mechanism', activeNodes: ['gone'], lines: [], kind: 'settle', callouts: [{ kind: sc === 'outside' ? 'pitfall' : 'mechanism', textKey: M(m, 'co.end.' + sc) }] });
      return out;
    }
    reg(m, {
      codeId: 'exit_builtin',
      controls: [sel(m, 'which', SC)],
      init: function () { return { which: 'builtin' }; },
      act: setter(['which']),
      steps: steps,
      selfChecks: [{ name: 'nội dung còn trong composition suốt exit; built-in: gỡ ở 300 ms; custom (500 ms) thuộc transition: gỡ ở 500 ms; animation ngoài transition: nội dung bị gỡ ở 300 ms dù animation đó chưa xong', run: function () {
        var last = function (w) { var x = steps({ which: w }); return x[x.length - 2]; };
        var mid = steps({ which: 'builtin' })[2];
        return mid.stateAfter[1].value === 'true' && last('builtin').metrics.ms === 300 && last('custom').metrics.ms === 500 && last('outside').metrics.ms === 300 && last('outside').type === 'pitfall';
      } }]
    });
  })();

  /* ================= C5 (v2): bên trong animateContentSize (AnimationModifier.kt @296313a4) =================
     expand: .animateContentSize().height(h): đo con 160, đích 160, báo giá trị hiện tại (40 → 85 → 128 → 152 → 160); mỗi frame chỉ layout.
     after: .height(h).animateContentSize(): constraints cố định → constraints.constrain ép về 160 ngay; animation vô hình vẫn làm đo lại.
     interrupt: đang mở ở 128 thì thu: startSize = 128, animateTo(40) hủy lần cũ (không gọi listener), listener(128 → 40). Số px là minh họa. */
  (function () {
    var m = 'acs';
    var SC = ['expand', 'after', 'interrupt'];
    function steps(s) {
      var sc = SC.indexOf(s.which) >= 0 ? s.which : 'expand', out = [], t = 0, c = { comp: 0, layout: 0, child: 40, reported: 40 }, target = 40, n = 0;
      var snip = sc === 'after' ? 'acs_after' : 'acs_expand';
      var P = function (key, o) {
        o.id = key.replace(/\./g, '_') + out.length; o.type = o.type || 'mechanism';
        o.titleKey = M(m, 's.' + key + '.title'); o.explainKey = M(m, 's.' + key + '.explain');
        o.params = o.params || {}; o.params.n = n; o.params.h = c.reported;
        o.metrics = { comp: c.comp, layout: c.layout, child: c.child, reported: c.reported };
        o.stateAfter = [{ labelKey: M(m, 'st.child'), value: c.child + ' px' }, { labelKey: M(m, 'st.reported'), value: c.reported + ' px' }, { labelKey: M(m, 'st.target'), value: target + ' px' }];
        o.movingSignals = o.movingSignals || []; o.activeNodes = o.activeNodes || [];
        o.codeHighlight = { snippet: snip, lines: o.lines || [] }; delete o.lines;
        o.logEvents = [{ t: t += 16, kind: o.kind || 'layout', subject: o.activeNodes[0] || 'node', detailKey: M(m, 'ev.' + key), params: o.params }]; delete o.kind;
        out.push(o);
      };
      var LA = sc === 'after' ? 6 : 5, LH = sc === 'after' ? 5 : 6, LN = [5, 6];
      c.layout = 1;
      P('intro.' + sc, { type: 'scenario', activeNodes: ['node', 'child'], lines: LN, kind: 'observe', callouts: [{ kind: 'source', textKey: M(m, sc === 'after' ? 'co.constrain' : 'co.first') }] });
      c.comp++;
      P('toggle', { activeNodes: ['state', 'child'], movingSignals: [{ edge: 'e1', tok: 'state' }], lines: [1, LH, 8], kind: 'recompose' });
      c.layout++; c.child = 160; target = 160;
      if (sc === 'after') {
        c.reported = 160;
        P('measure.after', { type: 'pitfall', activeNodes: ['node', 'parent'], movingSignals: [{ edge: 'e2', tok: 'ui' }, { edge: 'e3', tok: 'error' }], lines: [5, 6], kind: 'layout', callouts: [{ kind: 'pitfall', textKey: M(m, 'co.constrain') }] });
      } else {
        P('measure.anim', { activeNodes: ['node', 'child', 'parent'], movingSignals: [{ edge: 'e2', tok: 'ui' }, { edge: 'e3', tok: 'anim' }], lines: [5, 6], kind: 'layout', callouts: [{ kind: 'mechanism', textKey: M(m, 'co.clip') }] });
      }
      var fwd = sc === 'interrupt' ? [85, 128] : [85, 128, 152, 160], from = 40;
      fwd.forEach(function (v, i) {
        n++; c.layout++; if (sc !== 'after') c.reported = v;
        P(sc === 'after' ? 'frame.after' : 'frame.anim', { type: sc === 'after' ? 'pitfall' : 'mechanism', activeNodes: sc === 'after' ? ['node'] : ['node', 'parent'], movingSignals: sc === 'after' ? [] : [{ edge: 'e3', tok: 'anim' }], lines: [LA], kind: 'frame',
          callouts: i === 0 ? [{ kind: sc === 'after' ? 'pitfall' : 'source', textKey: M(m, sc === 'after' ? 'co.wasted' : 'co.layoutOnly') }] : undefined });
      });
      if (sc === 'interrupt') {
        c.comp++; c.child = 40; target = 40; from = c.reported;
        P('collapse', { type: 'pitfall', activeNodes: ['state', 'child', 'node'], movingSignals: [{ edge: 'e1', tok: 'state' }, { edge: 'e2', tok: 'ui' }], lines: [1, 6, 8], kind: 'interrupt' });
        [95, 62, 40].forEach(function (v) {
          n++; c.layout++; c.reported = v;
          P('frame.back', { activeNodes: ['node', 'parent'], movingSignals: [{ edge: 'e3', tok: 'anim' }], lines: [5], kind: 'frame' });
        });
      }
      var done = { activeNodes: ['node'], lines: [LA], kind: 'settle', params: { from: from, to: target } };
      if (sc === 'interrupt') done.callouts = [{ kind: 'source', textKey: M(m, 'co.interrupted') }];
      if (sc === 'after') done.type = 'pitfall';
      P('done.' + sc, done);
      return out;
    }
    reg(m, {
      codeId: 'acs_expand',
      simpExtra: [M(m, 'simp.2')],
      controls: [sel(m, 'which', SC)],
      init: function () { return { which: 'expand' }; },
      act: setter(['which']),
      steps: steps,
      selfChecks: [{ name: 'đúng thứ tự: bước đo sau khi chạm con 160 nhưng báo 40, cuối báo 160, 1 composition, 6 lượt layout; sai thứ tự: báo 160 ngay; ngắt ở 128: listener(128 → 40), 2 composition', run: function () {
        var a = steps({ which: 'expand' }), b = steps({ which: 'after' }), d = steps({ which: 'interrupt' });
        var la = a[a.length - 1], ld = d[d.length - 1];
        return a[2].metrics.child === 160 && a[2].metrics.reported === 40 && la.metrics.reported === 160 && la.metrics.comp === 1 && la.metrics.layout === 6 &&
          b[2].metrics.reported === 160 && ld.params.from === 128 && ld.params.to === 40 && ld.metrics.comp === 2 && ld.metrics.reported === 40;
      } }]
    });
  })();
})();
