/* Model rời rạc track E (thuần, không DOM, không câu chữ). */
(function () {
  'use strict';
  var K = 'track.ui.';
  var M = function (m, s) { return K + 'm.' + m + '.' + s; };
  function S(m, id, o) {
    o.id = id; o.type = o.type || 'mechanism'; o.titleKey = o.titleKey || M(m, 's.' + id + '.title'); o.explainKey = o.explainKey || M(m, 's.' + id + '.explain');
    o.params = o.params || {}; o.activeNodes = o.activeNodes || []; o.movingSignals = o.movingSignals || [];
    (o.logEvents || []).forEach(function (e) { if (!e.detailKey) e.detailKey = M(m, 'ev.' + id); if (!e.params) e.params = o.params; });
    return o;
  }
  function reg(m, def) { def.kind = 'discrete'; def.titleKey = M(m, 'title'); def.overviewKey = M(m, 'overview'); def.wrapupKey = M(m, 'wrapup'); def.controlsHintKey = M(m, 'ctl.hint'); def.simplificationKeys = [M(m, 'simp.1')]; ADE.registerModel('ui.' + m, def); }
  var sel = function (m, id, vals) { return { id: id, type: 'select', labelKey: M(m, 'ctl.' + id), get: function (s) { return s[id]; }, action: id, options: vals.map(function (v) { return { value: v, labelKey: M(m, 'ctl.' + id + '.' + v) }; }) }; };
  var tog = function (m, id) { return { id: id, type: 'toggle', labelKey: M(m, 'ctl.' + id), get: function (s) { return !!s[id]; }, action: id }; };
  var setter = function (keys) { return function (s, a, v) { var n = {}; keys.forEach(function (k) { n[k] = s[k]; }); if (keys.indexOf(a) >= 0) n[a] = typeof s[a] === 'boolean' ? !!v : v; return n; }; };

  /* E0: năm lớp token → component → pattern → màn hình → luồng */
  (function () {
    var m = 'layers', L = ['token', 'component', 'pattern', 'screen', 'flow'];
    function steps(s) {
      var P = {};
      return [S(m, 'what', { type: 'scenario', titleKey: M(m, 'l.' + s.layer + '.title'), explainKey: M(m, 'l.' + s.layer + '.what'), activeNodes: [s.layer], logEvents: [{ t: 0, kind: 'observe', subject: s.layer, detailKey: M(m, 'l.' + s.layer + '.title') }] }),
        S(m, 'example', { explainKey: M(m, 'l.' + s.layer + '.example'), activeNodes: [s.layer], logEvents: [{ t: 1, kind: 'act', subject: s.layer }] }),
        S(m, 'compose', { explainKey: M(m, 'l.' + s.layer + '.compose'), activeNodes: [s.layer], callouts: [{ kind: 'source', textKey: M(m, 'co.source') }], logEvents: [{ t: 2, kind: 'measure', subject: s.layer }] })];
    }
    reg(m, { controls: [sel(m, 'layer', L)], init: function () { return { layer: 'token' }; }, act: setter(['layer']), steps: steps,
      selfChecks: [{ name: 'mỗi lớp có 3 bước', run: function () { return L.every(function (l) { return steps({ layer: l }).length === 3; }); } }] });
  })();

  /* E7: chọn pattern theo bối cảnh (không có pattern "luôn đúng") */
  (function () {
    var m = 'patterns', ITEMS = { p1: 'bottomNav', p2: 'tabs', p3: 'stepper', p4: 'singlePage', p5: 'skeleton', p6: 'progressBar', p7: 'emptyCta', p8: 'contextual' };
    var OPTS = ['bottomNav', 'tabs', 'drawer', 'singlePage', 'stepper', 'skeleton', 'spinner', 'progressBar', 'emptyCta', 'contextual'];
    function steps(s) {
      var ok = ITEMS[s.item] === s.guess;
      return [S(m, 'situation', { type: 'scenario', titleKey: M(m, 'i.' + s.item + '.title'), explainKey: M(m, 'i.' + s.item + '.situation'), activeNodes: ['screen'], logEvents: [{ t: 0, kind: 'observe', subject: 'screen', detailKey: M(m, 'i.' + s.item + '.title') }] }),
        S(m, 'pick', { type: ok ? 'mechanism' : 'pitfall', titleKey: K + (ok ? 'c.right' : 'c.wrong'), explainKey: M(m, 'opt.' + s.guess + '.when'), activeNodes: ['user'], movingSignals: [{ edge: 'e1', tok: 'signal' }],
          stateAfter: [{ labelKey: K + 'c.yours', valueKey: M(m, 'ctl.guess.' + s.guess) }, { labelKey: K + 'c.expected', valueKey: M(m, 'ctl.guess.' + ITEMS[s.item]) }], logEvents: [{ t: 1, kind: 'decide', subject: 'user', detailKey: M(m, 'ctl.guess.' + s.guess) }] }),
        S(m, 'tradeoff', { titleKey: K + 'c.why', explainKey: M(m, 'i.' + s.item + '.why'), activeNodes: ['design'], callouts: [{ kind: 'mechanism', textKey: M(m, 'opt.' + ITEMS[s.item] + '.not') }], logEvents: [{ t: 2, kind: 'feedback', subject: 'design' }] })];
    }
    reg(m, { controls: [sel(m, 'item', Object.keys(ITEMS)), sel(m, 'guess', OPTS)], init: function () { return { item: 'p1', guess: 'bottomNav' }; }, act: setter(['item', 'guess']), steps: steps,
      selfChecks: [{ name: 'mỗi tình huống có 3 bước; đáp án tham khảo cho "khớp"', run: function () { return Object.keys(ITEMS).every(function (i) { var st = steps({ item: i, guess: ITEMS[i] }); return st.length === 3 && st[1].titleKey === K + 'c.right'; }); } }] });
  })();

  /* E7: form clinic — label thật, validate inline, lỗi cụ thể; lỗi minh họa trước/sau */
  (function () {
    var m = 'form';
    function steps(s) {
      var issues = (s.label ? 0 : 1) + (s.inline ? 0 : 1) + (s.specific ? 0 : 1), out = [];
      out.push(S(m, 'start', { type: 'scenario', activeNodes: ['screen'], callouts: [{ kind: 'try', textKey: M(m, 'co.try') }], logEvents: [{ t: 0, kind: 'observe', subject: 'screen' }] }));
      out.push(S(m, 'label', { type: s.label ? 'mechanism' : 'pitfall', explainKey: M(m, s.label ? 's.label.on' : 's.label.off'), activeNodes: ['screen'], logEvents: [{ t: 1, kind: s.label ? 'act' : 'error', subject: 'screen' }] }));
      out.push(S(m, 'validate', { type: s.inline ? 'mechanism' : 'pitfall', explainKey: M(m, s.inline ? 's.validate.on' : 's.validate.off'), activeNodes: ['user'], logEvents: [{ t: 2, kind: s.inline ? 'feedback' : 'error', subject: 'user' }] }));
      out.push(S(m, 'message', { type: s.specific ? 'mechanism' : 'pitfall', explainKey: M(m, s.specific ? 's.message.on' : 's.message.off'), activeNodes: ['design'], logEvents: [{ t: 3, kind: s.specific ? 'feedback' : 'error', subject: 'design' }],
        callouts: [{ kind: 'android', textKey: M(m, 'co.compose') }] }));
      out[out.length - 1].metrics = { issues: issues };
      return out;
    }
    reg(m, { controls: [tog(m, 'label'), tog(m, 'inline'), tog(m, 'specific')], init: function () { return { label: false, inline: false, specific: false }; }, act: setter(['label', 'inline', 'specific']), steps: steps,
      selfChecks: [{ name: 'bật cả ba thì không còn vấn đề', run: function () { var st = steps({ label: true, inline: true, specific: true }); return st[st.length - 1].metrics.issues === 0; } }] });
  })();

  /* E7: thời gian phản hồi — mốc 0,1 s / 1 s / 10 s (Nielsen); chỉ báo gợi ý theo độ trễ (minh họa) */
  var RT = ADE.uiResponse = { band: function (ms) { return ms <= 100 ? 'instant' : ms <= 1000 ? 'flow' : ms <= 10000 ? 'attention' : 'long'; } };
  (function () {
    var m = 'response', D = [80, 600, 4000, 15000];
    function steps(s) {
      var b = RT.band(s.delay);
      return [S(m, 'load', { type: 'scenario', params: { ms: s.delay }, activeNodes: ['screen'], logEvents: [{ t: 0, kind: 'act', subject: 'screen' }] }),
        S(m, 'band', { titleKey: M(m, 'band.' + b + '.title'), explainKey: M(m, 'band.' + b + '.explain'), params: { ms: s.delay }, activeNodes: ['user'], callouts: [{ kind: 'source', textKey: M(m, 'co.source') }], logEvents: [{ t: 1, kind: 'measure', subject: 'user', detailKey: M(m, 'band.' + b + '.title') }] }),
        S(m, 'indicator', { explainKey: M(m, 'ind.' + s.indicator + '.' + b), params: { ms: s.delay }, activeNodes: ['design'], logEvents: [{ t: 2, kind: 'feedback', subject: 'design', detailKey: M(m, 'ctl.indicator.' + s.indicator) }] })];
    }
    reg(m, { controls: [sel(m, 'delay', D), sel(m, 'indicator', ['none', 'spinner', 'skeleton', 'progress'])], init: function () { return { delay: 4000, indicator: 'spinner' }; },
      act: function (s, a, v) { return a === 'delay' ? { delay: D.indexOf(+v) >= 0 ? +v : s.delay, indicator: s.indicator } : { delay: s.delay, indicator: v }; }, steps: steps,
      selfChecks: [{ name: 'mốc: 100 ms tức thì, 1 s mạch suy nghĩ, 10 s giữ chú ý', run: function () { return RT.band(80) === 'instant' && RT.band(600) === 'flow' && RT.band(4000) === 'attention' && RT.band(15000) === 'long'; } }] });
  })();
})();
