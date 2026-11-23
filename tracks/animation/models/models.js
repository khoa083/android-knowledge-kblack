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
  TC.FRAME = 16;     // 16 ms theo KDoc của MainTestClock @296313a4 (JVM: Android và Desktop)
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

  /* ================= IF (v2, chương mới): lặp lại và vô hạn (AnimationSpec.kt, InfiniteTransition.kt @296313a4) =================
     restart3 / reverse3 / reverse2: repeatable(n, tween(300, Linear), mode); mỗi bước là một lượt. reverse2 (số chẵn) kết thúc ở 0, KDoc: có thể nhảy tới giá trị cuối.
     infinite: rememberInfiniteTransition + infiniteRepeatable(Reverse): 3 lượt, durationScale = 0 → skipToEnd và treo, tỉ lệ khác 0 → chạy lại từ 0, rời composition → hủy. */
  (function () {
    var m = 'repeat';
    var SC = ['restart3', 'reverse3', 'reverse2', 'infinite'];
    function steps(s) {
      var sc = SC.indexOf(s.which) >= 0 ? s.which : 'restart3', out = [], t = 0, ms = 0, iter = 0, val = 0;
      var inf = sc === 'infinite', n = sc === 'reverse2' ? 2 : 3, mode = sc === 'restart3' ? 'Restart' : 'Reverse';
      var P = function (key, o) {
        o.id = key.replace(/\./g, '_') + out.length; o.type = o.type || 'mechanism';
        o.titleKey = M(m, 's.' + key + '.title'); o.explainKey = M(m, 's.' + key + '.explain');
        o.params = o.params || {}; o.params.i = iter;
        o.metrics = { ms: ms, iter: iter, value: Math.round(val * 100) };
        o.stateAfter = [{ labelKey: M(m, 'st.value'), value: val.toFixed(1) }, { labelKey: M(m, 'st.iter'), value: iter + '/' + (inf ? '∞' : n) }, { labelKey: M(m, 'st.mode'), value: mode }];
        o.movingSignals = o.movingSignals || []; o.activeNodes = o.activeNodes || [];
        o.codeHighlight = { snippet: 'rep_' + sc, lines: o.lines || [] }; delete o.lines;
        o.logEvents = [{ t: t += 10, kind: o.kind || 'frame', subject: o.activeNodes[0] || 'spec', detailKey: M(m, 'ev.' + key), params: o.params }]; delete o.kind;
        out.push(o);
      };
      var sig = [{ edge: 'e1', tok: 'runtime' }, { edge: 'e2', tok: 'anim' }];
      if (!inf) {
        P('intro', { type: 'scenario', activeNodes: ['spec', 'value'], lines: [3, 4, 5], kind: 'observe', callouts: [{ kind: 'source', textKey: M(m, 'co.durationOnly') }] });
        for (var i = 1; i <= n; i++) {
          var back = mode === 'Reverse' && i % 2 === 0, from = back ? 1 : 0, to = back ? 0 : 1;
          iter = i; ms += 300; val = to;
          P(back ? 'iter.back' : (i > 1 && mode === 'Restart' ? 'iter.restart' : 'iter.fwd'), { activeNodes: ['spec', 'clock', 'value'], movingSignals: sig, lines: [5, 6], params: { from: from, to: to } });
        }
        if (mode === 'Reverse' && n % 2 === 0) {
          val = 1;
          P('jumpEnd', { type: 'pitfall', activeNodes: ['value'], movingSignals: [{ edge: 'e2', tok: 'error' }], lines: [4, 6], kind: 'settle', callouts: [{ kind: 'pitfall', textKey: M(m, 'co.odd') }] });
        }
        P('done', { activeNodes: ['value'], lines: [2], kind: 'settle', params: { to: val } });
        return out;
      }
      P('inf.start', { type: 'scenario', activeNodes: ['clock', 'spec'], lines: [1, 2], kind: 'observe', callouts: [{ kind: 'mechanism', textKey: M(m, 'co.frames') }] });
      for (var k = 1; k <= 3; k++) {
        var bk = k % 2 === 0; iter = k; ms += 300; val = bk ? 0 : 1;
        P('inf.iter', { activeNodes: ['clock', 'spec', 'value'], movingSignals: sig, lines: [5, 6, 7], params: { from: bk ? 1 : 0, to: bk ? 0 : 1 } });
      }
      val = 1;
      P('inf.scale0', { type: 'pitfall', activeNodes: ['policy', 'clock', 'value'], movingSignals: [{ edge: 'e3', tok: 'state' }], lines: [4], kind: 'skip', callouts: [{ kind: 'source', textKey: M(m, 'co.scale') }] });
      ms = 0; iter = 0; val = 0;
      P('inf.scaleBack', { activeNodes: ['policy', 'clock', 'spec'], movingSignals: [{ edge: 'e3', tok: 'state' }, { edge: 'e1', tok: 'runtime' }], lines: [3], kind: 'target-change' });
      P('inf.leave', { activeNodes: ['clock'], lines: [1], kind: 'interrupt', callouts: [{ kind: 'source', textKey: M(m, 'co.leave') }] });
      return out;
    }
    reg(m, {
      codeId: 'rep_restart3',
      simpExtra: [M(m, 'simp.2')],
      controls: [sel(m, 'which', SC)],
      init: function () { return { which: 'restart3' }; },
      act: setter(['which']),
      steps: steps,
      selfChecks: [{ name: 'repeatable 3 lượt = 900 ms, kết thúc ở 1; Reverse 2 lượt kết thúc lượt cuối ở 0 rồi nhảy tới 1; vô hạn: scale 0 → giá trị = đích, rồi chạy lại từ 0, rồi rời composition', run: function () {
        var a = steps({ which: 'restart3' }), b = steps({ which: 'reverse3' }), d = steps({ which: 'reverse2' }), f = steps({ which: 'infinite' });
        var la = a[a.length - 1], lb = b[b.length - 1];
        var jump = d.filter(function (x) { return /^jumpEnd/.test(x.id); });
        var s0 = f.filter(function (x) { return /^inf_scale0/.test(x.id); })[0], sb = f.filter(function (x) { return /^inf_scaleBack/.test(x.id); })[0];
        return la.metrics.ms === 900 && la.metrics.value === 100 && lb.metrics.value === 100 && !b.some(function (x) { return /^jumpEnd/.test(x.id); }) &&
          jump.length === 1 && d[d.indexOf(jump[0]) - 1].metrics.value === 0 && jump[0].metrics.value === 100 &&
          s0.metrics.value === 100 && sb.metrics.ms === 0 && /^inf_leave/.test(f[f.length - 1].id);
      } }]
    });
  })();

  /* ================= C6 (v2): Animatable loại trừ nhau, liên tục, luồng cử chỉ (Animatable.kt @296313a4, advanced docs) =================
     retarget: A animateTo(100) đang ở 40 thì B animateTo(0): A bị hủy (onArrived không chạy), B đi từ 40 với vận tốc hiện tại.
     back: stop → snapTo 60, 120 → thả 400 px/s, đích decay 190 ≤ 300 → animateTo(0, initialVelocity) → Finished.
     fling: như trên, thả 3000 px/s, đích 900 > 300 → updateBounds(±300) + animateDecay → kẹp ở 300, BoundReached, vận tốc về 0. Số liệu minh họa. */
  (function () {
    var m = 'mutex';
    var SC = ['retarget', 'back', 'fling'];
    function steps(s) {
      var sc = SC.indexOf(s.which) >= 0 ? s.which : 'retarget', out = [], t = 0, v = 0, vel = 0, run = 'false', reason = '—', target = 0, arrived = false;
      var P = function (key, o) {
        o.id = key.replace(/\./g, '_') + out.length; o.type = o.type || 'mechanism';
        o.titleKey = M(m, 's.' + key + '.title'); o.explainKey = M(m, 's.' + key + '.explain');
        o.params = { v: v, vel: vel, target: target };
        o.metrics = { value: v, velocity: vel };
        o.stateAfter = [{ labelKey: M(m, 'st.value'), value: v + ' px' }, { labelKey: M(m, 'st.running'), value: run }, { labelKey: M(m, 'st.reason'), value: reason }];
        o.movingSignals = o.movingSignals || []; o.activeNodes = o.activeNodes || [];
        o.codeHighlight = { snippet: sc === 'retarget' ? 'mutex_retarget' : 'mutex_swipe', lines: o.lines || [] }; delete o.lines;
        o.logEvents = [{ t: t += 16, kind: o.kind || 'frame', subject: o.activeNodes[0] || 'anim', detailKey: M(m, 'ev.' + key), params: o.params }]; delete o.kind;
        out.push(o);
      };
      var mv = [{ edge: 'e2', tok: 'anim' }];
      P('intro.' + sc, { type: 'scenario', activeNodes: ['anim', 'value'], lines: sc === 'retarget' ? [1] : [1], kind: 'observe' });
      if (sc === 'retarget') {
        run = 'true'; target = 100;
        P('a.start', { activeNodes: ['finger', 'anim'], movingSignals: [{ edge: 'e1', tok: 'state' }], lines: [3, 4], kind: 'act' });
        v = 40; vel = 250;
        P('a.frame', { activeNodes: ['anim', 'value'], movingSignals: mv, lines: [4] });
        reason = 'Cancelled (A)'; target = 0;
        P('b.call', { type: 'pitfall', activeNodes: ['finger', 'anim', 'job'], movingSignals: [{ edge: 'e1', tok: 'state' }, { edge: 'e3', tok: 'error' }], lines: [5, 8], kind: 'interrupt', callouts: [{ kind: 'source', textKey: M(m, 'co.mutex') }] });
        reason = '—';
        [[48, 60], [20, -180]].forEach(function (p, i) {
          v = p[0]; vel = p[1];
          P('b.frame', { activeNodes: ['anim', 'value'], movingSignals: mv, lines: [8], callouts: i === 0 ? [{ kind: 'source', textKey: M(m, 'co.continuous') }] : undefined });
        });
        v = 0; vel = 0; run = 'false'; reason = 'Finished';
        P('done.retarget', { activeNodes: ['value'], lines: [8], kind: 'settle' });
        out.arrived = arrived;
        return out;
      }
      P('down', { activeNodes: ['finger', 'anim'], movingSignals: [{ edge: 'e1', tok: 'state' }], lines: [1], kind: 'act', callouts: [{ kind: 'source', textKey: M(m, 'co.stop') }] });
      [60, 120].forEach(function (x) {
        v = x; vel = 0; target = x;
        P('drag', { activeNodes: ['finger', 'anim', 'value'], movingSignals: [{ edge: 'e1', tok: 'state' }, { edge: 'e2', tok: 'ui' }], lines: [2, 3, 4], kind: 'act' });
      });
      if (sc === 'back') {
        vel = 400; target = 190;
        P('release.back', { activeNodes: ['finger', 'anim'], lines: [6, 7, 8], kind: 'target-change', callouts: [{ kind: 'source', textKey: M(m, 'co.flow') }] });
        run = 'true';
        [[150, 150], [60, -300]].forEach(function (p) { v = p[0]; vel = p[1]; target = 0; P('back.frame', { activeNodes: ['anim', 'value'], movingSignals: mv, lines: [9] }); });
        v = 0; vel = 0; run = 'false'; reason = 'Finished';
        P('done.back', { activeNodes: ['value'], lines: [9], kind: 'settle' });
        return out;
      }
      vel = 3000; target = 900;
      P('release.fling', { activeNodes: ['finger', 'anim'], lines: [6, 7, 8], kind: 'target-change', callouts: [{ kind: 'source', textKey: M(m, 'co.flow') }] });
      run = 'true'; v = 220; vel = 1500;
      P('fling.frame', { activeNodes: ['anim', 'value'], movingSignals: mv, lines: [10] });
      v = 300; vel = 0; run = 'false'; reason = 'BoundReached';
      P('bound', { activeNodes: ['anim', 'value'], movingSignals: [{ edge: 'e2', tok: 'error' }], lines: [8, 10], kind: 'settle', callouts: [{ kind: 'mechanism', textKey: M(m, 'co.bound') }] });
      return out;
    }
    reg(m, {
      codeId: 'mutex_retarget',
      simpExtra: [M(m, 'simp.2')],
      controls: [sel(m, 'which', SC)],
      init: function () { return { which: 'retarget' }; },
      act: setter(['which']),
      steps: steps,
      selfChecks: [{ name: 'lời gọi B hủy A (onArrived không chạy) và đi tiếp từ 40 với vận tốc 250; thả chậm: về 0, Finished; hất mạnh: kẹp ở 300, BoundReached, vận tốc 0', run: function () {
        var a = steps({ which: 'retarget' }), b = steps({ which: 'back' }), f = steps({ which: 'fling' });
        var call = a.filter(function (x) { return /^b_call/.test(x.id); })[0], la = a[a.length - 1], lb = b[b.length - 1], lf = f[f.length - 1];
        return a.arrived === false && call.params.v === 40 && call.params.vel === 250 && call.type === 'pitfall' && la.metrics.value === 0 && la.stateAfter[2].value === 'Finished' &&
          lb.metrics.value === 0 && lb.stateAfter[2].value === 'Finished' && lf.metrics.value === 300 && lf.metrics.velocity === 0 && lf.stateAfter[2].value === 'BoundReached';
      } }]
    });
  })();

  /* ================= SE (v2, chương mới): shared element (SharedTransitionScope.kt @296313a4, shared-elements docs) =================
     match: cùng key → khớp, lookahead cho khung đích, bay trong overlay (16,64) → (0,360), xong về cây thường.
     nomatch: khác key → không khớp, chỉ fade của AnimatedContent. clip: clip trước sharedElement → góc vuông khi bay. Số liệu minh họa. */
  (function () {
    var m = 'shared';
    var SC = ['match', 'nomatch', 'clip'];
    function steps(s) {
      var sc = SC.indexOf(s.which) >= 0 ? s.which : 'match', out = [], t = 0, x = 16, w = 64, active = 0, match = 'false', drawn = 'tree', corner = '16dp';
      var P = function (key, o) {
        o.id = key.replace(/\./g, '_') + out.length; o.type = o.type || 'mechanism';
        o.titleKey = M(m, 's.' + key + '.title'); o.explainKey = M(m, 's.' + key + '.explain');
        o.params = { x: x, w: w };
        o.metrics = { x: x, w: w, active: active };
        o.stateAfter = [{ labelKey: M(m, 'st.match'), value: match }, { labelKey: M(m, 'st.drawn'), value: drawn }, { labelKey: M(m, 'st.corner'), value: corner }];
        o.movingSignals = o.movingSignals || []; o.activeNodes = o.activeNodes || [];
        o.codeHighlight = { snippet: 'shared_' + sc, lines: o.lines || [] }; delete o.lines;
        o.logEvents = [{ t: t += 16, kind: o.kind || 'frame', subject: o.activeNodes[0] || 'scope', detailKey: M(m, 'ev.' + key), params: o.params }]; delete o.kind;
        out.push(o);
      };
      P('intro.' + sc, { type: 'scenario', activeNodes: ['list'], lines: [3, 4, 5], kind: 'observe' });
      P('navigate', { activeNodes: ['list', 'detail'], movingSignals: [{ edge: 'e1', tok: 'state' }], lines: [2], kind: 'target-change' });
      if (sc === 'nomatch') {
        P('nomatchStep', { type: 'pitfall', activeNodes: ['scope', 'list', 'detail'], movingSignals: [{ edge: 'e1', tok: 'error' }], lines: [4], kind: 'skip', callouts: [{ kind: 'source', textKey: M(m, 'co.key') }] });
        x = 0; w = 360;
        P('fade', { activeNodes: ['list', 'detail'], lines: [2] });
        P('done.nomatch', { type: 'pitfall', activeNodes: ['detail'], lines: [4], kind: 'settle', callouts: [{ kind: 'source', textKey: M(m, 'co.match') }] });
        return out;
      }
      active = 1; match = 'true'; drawn = 'overlay';
      P('matched', { activeNodes: ['scope', 'list', 'detail'], movingSignals: [{ edge: 'e1', tok: 'state' }, { edge: 'e3', tok: 'state' }], lines: [4], kind: 'observe', callouts: [{ kind: 'source', textKey: M(m, 'co.key') }] });
      if (sc === 'clip') corner = '0';
      [[10, 160], [4, 280], [0, 360]].forEach(function (p, i) {
        x = p[0]; w = p[1];
        P(sc === 'clip' ? 'flyClip' : 'fly', { type: sc === 'clip' ? 'pitfall' : 'mechanism', activeNodes: ['overlay', 'scope'], movingSignals: [{ edge: 'e2', tok: sc === 'clip' ? 'error' : 'anim' }], lines: sc === 'clip' ? [4, 5] : [4, 6],
          callouts: i === 0 ? [{ kind: sc === 'clip' ? 'pitfall' : 'source', textKey: M(m, sc === 'clip' ? 'co.clip' : 'co.overlay') }] : undefined });
      });
      P('fade', { activeNodes: ['list', 'detail'], lines: [2] });
      active = 0; drawn = 'tree'; corner = '16dp';
      P('done.' + sc, { activeNodes: ['detail'], movingSignals: [{ edge: 'e4', tok: 'ui' }], lines: [5], kind: 'settle' });
      return out;
    }
    reg(m, {
      codeId: 'shared_match',
      simpExtra: [M(m, 'simp.2')],
      controls: [sel(m, 'which', SC)],
      init: function () { return { which: 'match' }; },
      act: setter(['which']),
      steps: steps,
      selfChecks: [{ name: 'cùng key: khớp, bay trong overlay tới 360, xong về cây thường; khác key: không khớp, không có bước bay; clip trước: góc 0 khi bay, 16dp khi xong', run: function () {
        var a = steps({ which: 'match' }), b = steps({ which: 'nomatch' }), c = steps({ which: 'clip' });
        var fa = a.filter(function (x) { return /^fly/.test(x.id); }), fc = c.filter(function (x) { return /^flyClip/.test(x.id); }), la = a[a.length - 1], lc = c[c.length - 1];
        return fa.length === 3 && fa[2].metrics.w === 360 && fa[0].stateAfter[1].value === 'overlay' && la.stateAfter[1].value === 'tree' && la.metrics.active === 0 &&
          !b.some(function (x) { return /^fly/.test(x.id); }) && b[b.length - 1].stateAfter[0].value === 'false' &&
          fc.length === 3 && fc[0].stateAfter[2].value === '0' && lc.stateAfter[2].value === '16dp';
      } }]
    });
  })();

  /* ================= CV (v2, chương mới): vẽ động và AVD (AnimatedVectorPainterResources.android.kt, Animator.kt, VectorPainter.kt @296313a4) =================
     canvas: progress → recompose 1 lần, sweep đọc trong Canvas → mỗi frame chỉ draw. forward: atEnd → true, updateTransition, giá trị đọc
     trong composition riêng của vector, mỗi frame vector + draw. back: atEnd → false, spec.reversed. Số liệu minh họa. */
  (function () {
    var m = 'avd';
    var SC = ['canvas', 'forward', 'back'];
    function steps(s) {
      var sc = SC.indexOf(s.which) >= 0 ? s.which : 'canvas', out = [], t = 0, n = 0, c = { comp: 0, vector: 0, draw: 0 }, val = sc === 'back' ? 180 : 0;
      var spec = sc === 'canvas' ? 'spring' : sc === 'back' ? 'keyframes.reversed' : 'keyframes', reader = sc === 'canvas' ? 'drawBehind' : 'vector composition';
      var P = function (key, o) {
        o.id = key.replace(/\./g, '_') + out.length; o.type = o.type || 'mechanism';
        o.titleKey = M(m, 's.' + key + '.title'); o.explainKey = M(m, 's.' + key + '.explain');
        o.params = { n: n, v: val };
        o.metrics = { comp: c.comp, vector: c.vector, draw: c.draw, val: val };
        o.stateAfter = [{ labelKey: M(m, 'st.val'), value: val + '°' }, { labelKey: M(m, 'st.spec'), value: spec }, { labelKey: M(m, 'st.reader'), value: reader }];
        o.movingSignals = o.movingSignals || []; o.activeNodes = o.activeNodes || [];
        o.codeHighlight = { snippet: sc === 'canvas' ? 'avd_canvas' : 'avd_vector', lines: o.lines || [] }; delete o.lines;
        o.logEvents = [{ t: t += 16, kind: o.kind || 'frame', subject: o.activeNodes[0] || 'anim', detailKey: M(m, 'ev.' + key), params: o.params }]; delete o.kind;
        out.push(o);
      };
      P('intro.' + sc, { type: 'scenario', activeNodes: ['state', 'anim'], lines: sc === 'canvas' ? [1, 2] : [1, 4], kind: 'observe', callouts: sc === 'canvas' ? undefined : [{ kind: 'source', textKey: M(m, 'co.transition') }] });
      c.comp++;
      P(sc === 'canvas' ? 'target.canvas' : 'target.avd', { activeNodes: ['state', 'anim'], movingSignals: [{ edge: 'e1', tok: 'state' }], lines: sc === 'canvas' ? [1] : [2, 6], kind: 'recompose' });
      var vals = sc === 'back' ? [120, 60, 0] : [60, 120, 180];
      vals.forEach(function (v, i) {
        n++; val = v; c.draw++; if (sc !== 'canvas') c.vector++;
        var key = sc === 'canvas' ? 'frame.canvas' : sc === 'back' ? 'frame.back' : 'frame.forward';
        var co = i !== 0 ? undefined : sc === 'canvas' ? [{ kind: 'source', textKey: M(m, 'co.draw') }] : sc === 'back' ? [{ kind: 'source', textKey: M(m, 'co.reversed') }] : [{ kind: 'mechanism', textKey: M(m, 'co.vector') }];
        P(key, { activeNodes: ['anim', 'reader', 'screen'], movingSignals: [{ edge: 'e2', tok: 'anim' }, { edge: 'e3', tok: 'ui' }], lines: sc === 'canvas' ? [5] : [4], callouts: co, kind: sc === 'canvas' ? 'draw' : 'recompose' });
      });
      P('done.' + sc, { activeNodes: ['screen'], lines: [], kind: 'settle' });
      return out;
    }
    reg(m, {
      codeId: 'avd_canvas',
      simpExtra: [M(m, 'simp.2')],
      controls: [sel(m, 'which', SC)],
      init: function () { return { which: 'canvas' }; },
      act: setter(['which']),
      steps: steps,
      selfChecks: [{ name: 'Canvas: 1 recompose, 3 lượt vẽ, 0 lượt composition của vector; AVD tới cuối: 3 lượt composition vector, kết thúc 180°; về đầu: spec đảo ngược, kết thúc 0°', run: function () {
        var a = steps({ which: 'canvas' }), f = steps({ which: 'forward' }), b = steps({ which: 'back' });
        var la = a[a.length - 1].metrics, lf = f[f.length - 1].metrics, lb = b[b.length - 1];
        return la.comp === 1 && la.draw === 3 && la.vector === 0 && lf.vector === 3 && lf.val === 180 && lb.metrics.val === 0 && lb.stateAfter[1].value === 'keyframes.reversed';
      } }]
    });
  })();

  /* ================= VM (v2, chương mới): một frame của animator (Property Animation docs: elapsed → TimeInterpolator → TypeEvaluator) =================
     0 → 40 px trong 40 ms, AccelerateDecelerate: f(t) = cos((t + 1)π)/2 + 0.5. property: ghi translationX thật; viewanim: chỉ dời hình vẽ
     (vùng chạm ở 0); compose: ghi state, offset { } đọc ở bước đặt. */
  (function () {
    var m = 'vframe';
    var SC = ['property', 'viewanim', 'compose'];
    var AD = function (t) { return Math.cos((t + 1) * Math.PI) / 2 + 0.5; };
    function steps(s) {
      var sc = SC.indexOf(s.which) >= 0 ? s.which : 'property', out = [], t = 0, ms = 0, e = 0, it = 0, v = 0;
      var writes = sc === 'property' ? 'translationX' : sc === 'viewanim' ? 'draw matrix' : 'State<Float>';
      var P = function (key, o) {
        o.id = key.replace(/\./g, '_') + out.length; o.type = o.type || 'mechanism';
        o.titleKey = M(m, 's.' + key + '.title'); o.explainKey = M(m, 's.' + key + '.explain');
        o.params = { ms: ms, e: Math.round(e * 100), i: Math.round(it * 100), v: v };
        o.metrics = { elapsed: Math.round(e * 100), interp: Math.round(it * 100), value: Math.round(v * 10) };
        o.stateAfter = [{ labelKey: M(m, 'st.drawn'), value: v + ' px' }, { labelKey: M(m, 'st.real'), value: (sc === 'viewanim' ? 0 : v) + ' px' }, { labelKey: M(m, 'st.writes'), value: writes }];
        o.movingSignals = o.movingSignals || []; o.activeNodes = o.activeNodes || [];
        o.codeHighlight = { snippet: 'vf_' + sc, lines: o.lines || [] }; delete o.lines;
        o.logEvents = [{ t: t += 10, kind: o.kind || 'frame', subject: o.activeNodes[0] || 'clock', detailKey: M(m, 'ev.' + key), params: o.params }]; delete o.kind;
        out.push(o);
      };
      var chain = [{ edge: 'e1', tok: 'runtime' }, { edge: 'e2', tok: 'anim' }, { edge: 'e3', tok: sc === 'viewanim' ? 'error' : 'ui' }];
      var tick = function (msNow, extra) {
        ms = msNow; e = ms / 40; it = AD(e); v = Math.round(40 * it * 10) / 10;
        P('tick', { activeNodes: ['clock', 'interp', 'eval', 'target'], movingSignals: chain, lines: sc === 'compose' ? [2, 3] : [2, 3], callouts: extra });
      };
      P('intro.' + sc, { type: 'scenario', activeNodes: ['target'], lines: [1], kind: 'observe' });
      tick(10, [{ kind: 'source', textKey: M(m, 'co.chain') }]);
      if (sc === 'property') P('write.property', { activeNodes: ['target'], lines: [4], kind: 'act' });
      else if (sc === 'viewanim') P('write.viewanim', { type: 'pitfall', activeNodes: ['target'], movingSignals: [{ edge: 'e3', tok: 'error' }], lines: [4], kind: 'draw', callouts: [{ kind: 'pitfall', textKey: M(m, 'co.viewanim') }] });
      else P('write.compose', { activeNodes: ['target'], lines: [4], kind: 'layout', callouts: [{ kind: 'source', textKey: M(m, 'co.phase') }] });
      [20, 30, 40].forEach(function (x) { tick(x); });
      P('tap.' + sc, { type: sc === 'viewanim' ? 'pitfall' : 'mechanism', activeNodes: ['target'], lines: sc === 'viewanim' ? [4] : [], kind: 'settle' });
      return out;
    }
    reg(m, {
      codeId: 'vf_property',
      simpExtra: [M(m, 'simp.2')],
      controls: [sel(m, 'which', SC)],
      init: function () { return { which: 'property' }; },
      act: setter(['which']),
      steps: steps,
      selfChecks: [{ name: 't = 10 ms: phân số 25% → khoảng 15% (tài liệu) → 5,9 px; cuối 40 px; view animation: vùng chạm vẫn 0 px; property: vùng chạm 40 px', run: function () {
        var p = steps({ which: 'property' }), va = steps({ which: 'viewanim' });
        var first = p[1], lp = p[p.length - 1], lv = va[va.length - 1];
        return first.metrics.elapsed === 25 && first.metrics.interp === 15 && first.params.v === 5.9 && lp.params.v === 40 && lp.stateAfter[1].value === '40 px' && lv.stateAfter[1].value === '0 px' && lv.stateAfter[0].value === '40 px';
      } }]
    });
  })();

  /* ================= C7 (v2): thứ tự trong một frame (Recomposer.kt, AndroidUiFrameClock, WindowRecomposer, SuspendAnimation @296313a4) =================
     body: vsync → awaiters (animation ghi giá trị) → notify → recompose → draw. layer: … notify → không recompose → draw.
     scale0: durationScale 0 → frame đầu đã là cuối (giá trị = đích, hết chạy). */
  (function () {
    var m = 'frameorder';
    var SC = ['body', 'layer', 'scale0'];
    function steps(s) {
      var sc = SC.indexOf(s.which) >= 0 ? s.which : 'body', out = [], t = 0, c = { recomp: 0, draw: 0 }, val = 0.4, running = 'true';
      var read = sc === 'layer' ? 'graphicsLayer { }' : 'body';
      var P = function (key, o) {
        o.id = key.replace(/\./g, '_') + out.length; o.type = o.type || 'mechanism';
        o.titleKey = M(m, 's.' + key + '.title'); o.explainKey = M(m, 's.' + key + '.explain');
        o.params = { v: val.toFixed(1) };
        o.metrics = { recomp: c.recomp, draw: c.draw, val: Math.round(val * 100) };
        o.stateAfter = [{ labelKey: M(m, 'st.val'), value: val.toFixed(1) }, { labelKey: M(m, 'st.running'), value: running }, { labelKey: M(m, 'st.read'), value: read }];
        o.movingSignals = o.movingSignals || []; o.activeNodes = o.activeNodes || [];
        o.codeHighlight = { snippet: sc === 'layer' ? 'fo_layer' : 'fo_body', lines: o.lines || [] }; delete o.lines;
        o.logEvents = [{ t: t += 2, kind: o.kind || 'frame', subject: o.activeNodes[0] || 'recomposer', detailKey: M(m, 'ev.' + key), params: o.params }]; delete o.kind;
        out.push(o);
      };
      P('intro.' + sc, { type: 'scenario', activeNodes: ['anim', 'ui'], lines: [1, 2], kind: 'observe', callouts: sc === 'scale0' ? [{ kind: 'source', textKey: M(m, 'co.scale') }] : undefined });
      P('vsync', { activeNodes: ['vsync', 'recomposer'], movingSignals: [{ edge: 'e1', tok: 'runtime' }], lines: [], kind: 'frame', callouts: [{ kind: 'source', textKey: M(m, 'co.choreo') }] });
      if (sc === 'scale0') { val = 1; running = 'false'; } else { val = 0.5; }
      P(sc === 'scale0' ? 'awaiters0' : 'awaiters', { type: sc === 'scale0' ? 'pitfall' : 'mechanism', activeNodes: ['recomposer', 'anim'], movingSignals: [{ edge: 'e2', tok: 'anim' }], lines: [1], kind: 'act', callouts: sc === 'scale0' ? undefined : [{ kind: 'source', textKey: M(m, 'co.order') }] });
      P('notify', { activeNodes: ['anim', 'recomposer'], movingSignals: [{ edge: 'e3', tok: 'state' }], lines: [], kind: 'observe' });
      if (sc === 'layer') {
        P('norecompose', { activeNodes: ['recomposer'], lines: [2], kind: 'skip', callouts: [{ kind: 'source', textKey: M(m, 'co.defer') }] });
      } else {
        c.recomp++;
        P('recompose', { activeNodes: ['recomposer', 'ui'], movingSignals: [{ edge: 'e4', tok: 'runtime' }], lines: [2], kind: 'recompose' });
      }
      c.draw++;
      P('draw', { activeNodes: ['ui'], movingSignals: [{ edge: 'e4', tok: 'ui' }], lines: [2], kind: 'draw' });
      P('done.' + sc, { activeNodes: ['ui'], lines: [], kind: 'settle' });
      return out;
    }
    reg(m, {
      codeId: 'fo_body',
      simpExtra: [M(m, 'simp.2')],
      controls: [sel(m, 'which', SC)],
      init: function () { return { which: 'body' }; },
      act: setter(['which']),
      steps: steps,
      selfChecks: [{ name: 'animation chạy trước recompose; đọc trong thân: 1 recompose + 1 vẽ; đọc trong graphicsLayer: 0 recompose + 1 vẽ; tỉ lệ 0: giá trị = đích và hết chạy ngay frame đầu', run: function () {
        var b = steps({ which: 'body' }), l = steps({ which: 'layer' }), z = steps({ which: 'scale0' });
        var ia = b.findIndex(function (x) { return /^awaiters/.test(x.id); }), ir = b.findIndex(function (x) { return /^recompose/.test(x.id); });
        var lb = b[b.length - 1].metrics, ll = l[l.length - 1].metrics, a0 = z.filter(function (x) { return /^awaiters0/.test(x.id); })[0];
        return ia > 0 && ir > ia && lb.recomp === 1 && lb.draw === 1 && ll.recomp === 0 && ll.draw === 1 && a0.metrics.val === 100 && a0.stateAfter[1].value === 'false';
      } }]
    });
  })();

  /* ================= C8 (v2): đồng hồ test và frame khởi động (MainTestClock.kt @296313a4) =================
     Frame 16 ms. manual: bật state → frame 16: recompose, lên lịch → frame 32: play 0 → advanceTimeBy(50) làm tròn 64 → play 64.
     ignore: advanceTimeBy(50, ignoreFrameDuration) → frame 16, 32, 48 → play 16. auto: chờ idle chạy tới cuối (play ≥ 250). */
  (function () {
    var m = 'clockstart';
    var SC = ['manual', 'ignore', 'auto'], FR = 16;
    function steps(s) {
      var sc = SC.indexOf(s.which) >= 0 ? s.which : 'manual', out = [], t = 0, clock = 0, frames = 0, play = -1, adv = 0, sees = '—';
      var P = function (key, o) {
        o.id = key.replace(/\./g, '_') + out.length; o.type = o.type || 'mechanism';
        o.titleKey = M(m, 's.' + key + '.title'); o.explainKey = M(m, 's.' + key + '.explain');
        o.params = { clock: clock, play: Math.max(play, 0), adv: adv };
        o.metrics = { clock: clock, frames: frames, play: Math.max(play, 0) };
        o.stateAfter = [{ labelKey: M(m, 'st.auto'), value: sc === 'auto' ? 'true' : 'false' }, { labelKey: M(m, 'st.play'), value: play < 0 ? '—' : play + ' ms' }, { labelKey: M(m, 'st.sees'), value: sees }];
        o.movingSignals = o.movingSignals || []; o.activeNodes = o.activeNodes || [];
        o.codeHighlight = { snippet: 'cs_' + sc, lines: o.lines || [] }; delete o.lines;
        o.logEvents = [{ t: t += 5, kind: o.kind || 'frame', subject: o.activeNodes[0] || 'clock', detailKey: M(m, 'ev.' + key), params: o.params }]; delete o.kind;
        out.push(o);
      };
      var frame = function () { frames++; clock += FR; if (play >= 0) play += FR; };
      P('intro.' + sc, { type: 'scenario', activeNodes: ['test', 'clock'], lines: [1], kind: 'observe', callouts: [{ kind: 'source', textKey: M(m, sc === 'auto' ? 'co.auto' : 'co.drives') }] });
      P('toggle', { activeNodes: ['test', 'recomposer'], movingSignals: [{ edge: 'e1', tok: 'state' }], lines: [2], kind: 'target-change' });
      if (sc === 'auto') {
        frame();               // frame 1: recompose, lên lịch
        frame(); play = 0;     // frame 2: play 0
        while (play < 250) frame();
        play = 250; sees = 'end';
        P('idle', { activeNodes: ['clock', 'anim', 'recomposer'], movingSignals: [{ edge: 'e2', tok: 'runtime' }, { edge: 'e3', tok: 'anim' }], lines: [3], kind: 'settle' });
        P('done.auto', { activeNodes: ['test'], lines: [3], kind: 'observe' });
        return out;
      }
      if (sc === 'manual') {
        frame();
        P('f1', { activeNodes: ['clock', 'recomposer'], movingSignals: [{ edge: 'e2', tok: 'runtime' }, { edge: 'e4', tok: 'runtime' }], lines: [3], kind: 'recompose' });
        frame(); play = 0; sees = 't=0';
        P('f2', { activeNodes: ['clock', 'anim'], movingSignals: [{ edge: 'e3', tok: 'anim' }], lines: [3], kind: 'frame', callouts: [{ kind: 'source', textKey: M(m, 'co.twoframes') }] });
        adv = Math.ceil(50 / FR) * FR;
        for (var k = 0; k < adv / FR; k++) frame();
        sees = 't=' + play + ' ms';
        P('adv', { activeNodes: ['clock', 'anim'], movingSignals: [{ edge: 'e3', tok: 'anim' }], lines: [4], kind: 'frame', callouts: [{ kind: 'source', textKey: M(m, 'co.round') }] });
        P('done.manual', { activeNodes: ['test'], lines: [5], kind: 'observe' });
        return out;
      }
      // ignore: tiến đúng 50 ms; frame chỉ ở 16, 32, 48
      frame(); frame(); play = 0; frame(); clock = 50; sees = 't=' + play + ' ms';
      P('advIgnore', { type: 'pitfall', activeNodes: ['clock', 'anim'], movingSignals: [{ edge: 'e3', tok: 'anim' }], lines: [3], kind: 'frame' });
      P('done.ignore', { type: 'pitfall', activeNodes: ['test'], lines: [4], kind: 'observe' });
      return out;
    }
    reg(m, {
      codeId: 'cs_manual',
      simpExtra: [M(m, 'simp.2')],
      controls: [sel(m, 'which', SC)],
      init: function () { return { which: 'manual' }; },
      act: setter(['which']),
      steps: steps,
      selfChecks: [{ name: 'tự tiến: sau 32 ms thời gian chơi = 0; advanceTimeBy(50) tiến 64 → thời gian chơi 64; bỏ làm tròn: đồng hồ 50, 3 frame, thời gian chơi 16; autoAdvance: test thấy giá trị cuối', run: function () {
        var a = steps({ which: 'manual' }), b = steps({ which: 'ignore' }), c = steps({ which: 'auto' });
        var f2 = a.filter(function (x) { return /^f2/.test(x.id); })[0], la = a[a.length - 1], lb = b[b.length - 1], lc = c[c.length - 1];
        return f2.metrics.clock === 32 && f2.metrics.play === 0 && la.params.adv === 64 && la.metrics.play === 64 &&
          lb.metrics.clock === 50 && lb.metrics.frames === 3 && lb.metrics.play === 16 && lc.stateAfter[2].value === 'end';
      } }]
    });
  })();

  /* ================= C0 (v2): đi theo cây quyết định của trang choose-api (cấu trúc đọc từ HTML 2026-11-23) =================
     Mỗi nhu cầu là một đường đi: danh sách [câu hỏi, có/không] rồi API. */
  (function () {
    var m = 'tree';
    var PATHS = {
      icon: [['art', 1], ['svg', 1]],
      spinner: [['art', 0], ['infinite', 1]],
      screen: [['art', 0], ['infinite', 0], ['layout', 1], ['switch', 1], ['nav', 1]],
      expand: [['art', 0], ['infinite', 0], ['layout', 1], ['switch', 0], ['appear', 0], ['size', 1]],
      together: [['art', 0], ['infinite', 0], ['layout', 0], ['multi', 1], ['indep', 0], ['together', 1]],
      swipe: [['art', 0], ['infinite', 0], ['layout', 0], ['multi', 0], ['target', 0], ['gesture', 1]]
    };
    var API = { icon: 'AnimatedVectorDrawable', spinner: 'rememberInfiniteTransition', screen: 'composable() + enter/exitTransition', expand: 'Modifier.animateContentSize', together: 'updateTransition', swipe: 'Animatable' };
    var CH = { icon: 'cv', spinner: 'if', screen: 'c4 · se', expand: 'c5', together: 'c3', swipe: 'c6' };
    var SC = Object.keys(PATHS);
    ADE.animTree = { PATHS: PATHS, API: API, CH: CH };   // cho hình cây quyết định (views/visuals.js)
    function steps(s) {
      var sc = PATHS[s.which] ? s.which : 'icon', out = [], t = 0, depth = 0, ans = '—', api = '—';
      var P = function (titleKey, explainKey, o) {
        o.id = 'st' + out.length; o.type = o.type || 'mechanism';
        o.titleKey = M(m, titleKey); o.explainKey = M(m, explainKey);
        o.params = o.params || {};
        o.metrics = { depth: depth };
        o.stateAfter = [{ labelKey: M(m, 'st.answer'), value: ans }, { labelKey: M(m, 'st.api'), value: api }];
        o.movingSignals = o.movingSignals || []; o.activeNodes = o.activeNodes || [];
        o.codeHighlight = { snippet: 'choose', lines: [] };
        o.logEvents = [{ t: t++, kind: o.kind || 'observe', subject: o.activeNodes[0] || 'need', detailKey: M(m, o.ev), params: o.params }]; delete o.kind; delete o.ev;
        out.push(o);
      };
      P('s.intro.' + sc + '.title', 's.intro.' + sc + '.explain', { type: 'scenario', activeNodes: ['need'], ev: 'ev.intro.' + sc, callouts: [{ kind: 'source', textKey: M(m, 'co.tree') }] });
      PATHS[sc].forEach(function (q, i) {
        depth++; ans = q[1] ? '✓' : '✗';
        P('s.q.' + q[0] + '.title', q[1] ? 's.ans.yes' : 's.ans.no', { activeNodes: ['need', 'question'], movingSignals: [{ edge: 'e1', tok: q[1] ? 'state' : 'runtime' }], kind: 'act', ev: 'ev.q.' + q[0] });
      });
      ans = '—'; api = API[sc];
      P('s.api.' + sc + '.title', 's.api.' + sc + '.explain', { activeNodes: ['api', 'chapter'], movingSignals: [{ edge: 'e2', tok: 'anim' }, { edge: 'e3', tok: 'ui' }], kind: 'settle', ev: 'ev.api.' + sc,
        params: { ch: CH[sc] }, callouts: sc === 'together' || sc === 'expand' ? [{ kind: 'mechanism', textKey: M(m, 'co.overlap') }] : undefined });
      return out;
    }
    reg(m, {
      codeId: 'choose',
      controls: [sel(m, 'which', SC)],
      init: function () { return { which: 'icon' }; },
      act: setter(['which']),
      steps: steps,
      selfChecks: [{ name: 'mỗi nhu cầu đi đúng số câu hỏi của cây rồi tới API; nút đổi nhiều thuộc tính → updateTransition qua 6 câu; thẻ kéo → Animatable', run: function () {
        return SC.every(function (k) { var x = steps({ which: k }); return x.length === PATHS[k].length + 2 && x[x.length - 1].stateAfter[1].value === API[k]; }) &&
          steps({ which: 'together' }).length === 8 && steps({ which: 'swipe' })[7].stateAfter[1].value === 'Animatable';
      } }]
    });
  })();
})();
