/* controls.js — thanh điều khiển dùng chung và phím tắt.
   Phím tắt mô phỏng chỉ có hiệu lực khi focus nằm trong vùng mô phỏng và BỊ BỎ QUA khi focus ở
   button, input, select, textarea, slider (master 5.5). Phím toàn cục (?, /, Ctrl+K) bỏ qua khi đang gõ. */
(function () {
  'use strict';
  var ADE = window.ADE = window.ADE || {};
  var h = function () { return ADE.ui.h.apply(null, arguments); };
  var icon = function (n, o) { return ADE.ui.icon(n, o); };
  var SPEEDS = [0.5, 1, 2, 4];
  var FRAMES = [8, 16, 33, 50];            // khoảng frame minh hoạ (ms), người đọc chọn

  var NO_KEYS = 'button,input,select,textarea,[role=slider],[role=tab],[contenteditable=true],a[href],summary';

  function bar(S) {
    var disc = S.kind === 'discrete';
    var el = h('div', { class: 'controls', role: 'group', 'aria-label': ADE.t('app.controls') });
    var pos = h('span', { class: 'pos', 'aria-hidden': 'true' });
    var bReset = h('button', { type: 'button', class: 'btn icon', 'aria-label': ADE.t('app.reset'), title: ADE.t('app.reset'), onclick: function () { S.reset(); } }, icon('reset'));
    var bPrev = disc ? h('button', { type: 'button', class: 'btn icon', 'aria-label': ADE.t('app.prev'), title: ADE.t('app.prev') + ' (←)', onclick: function () { S.prev(); } }, icon('prev')) : null;
    var bPlay = h('button', { type: 'button', class: 'btn primary play', onclick: function () { S.toggle(); } });
    var bNext = disc ? h('button', { type: 'button', class: 'btn', title: ADE.t('app.next') + ' (→)', onclick: function () { S.next(); } }, h('span', { text: ADE.t('app.next') }), icon('next')) : null;
    var bFrame = !disc ? h('button', { type: 'button', class: 'btn', onclick: function () { S.stepFrame(); } }, icon('frame'), h('span', { text: ADE.t('app.stepFrame') })) : null;
    var bRestart = !disc ? h('button', { type: 'button', class: 'btn', onclick: function () { S.restart(); } }, icon('replay'), h('span', { text: ADE.t('app.restart') })) : null;
    var bReplay = disc ? h('button', { type: 'button', class: 'btn icon', 'aria-label': ADE.t('app.replayStep'), title: ADE.t('app.replayStep'), onclick: function () { S.replayStep(); } }, icon('refresh')) : null;
    var selSpeed = h('select', { class: 'sel', id: 'spd-' + Math.random().toString(36).slice(2, 7), 'aria-label': ADE.t('app.speed'), onchange: function () { S.setSpeed(parseFloat(selSpeed.value)); } });
    SPEEDS.forEach(function (s) { selSpeed.appendChild(h('option', { value: String(s), selected: S.speed === s ? true : null, text: ADE.num(s) + '×' })); });
    var selFrame = !disc ? h('select', { class: 'sel', 'aria-label': ADE.t('app.frameInterval'), onchange: function () { S.setFrameMs(parseFloat(selFrame.value)); } }) : null;
    if (selFrame) FRAMES.forEach(function (f) { selFrame.appendChild(h('option', { value: String(f), selected: S.frameMs === f ? true : null, text: ADE.num(f) + ' ms' })); });
    el.appendChild(bReset); if (bPrev) el.appendChild(bPrev);
    el.appendChild(bPlay); if (bNext) el.appendChild(bNext); if (bFrame) el.appendChild(bFrame); if (bRestart) el.appendChild(bRestart); if (bReplay) el.appendChild(bReplay);
    el.appendChild(h('label', { class: 'field inline' }, h('span', { text: ADE.t('app.speed') }), selSpeed));
    if (selFrame) el.appendChild(h('label', { class: 'field inline' }, h('span', { text: ADE.t('app.frameInterval') }), selFrame));
    el.appendChild(pos);
    function update() {
      var reduced = ADE.motionReduced();
      var playing = S.playing;
      bPlay.innerHTML = '';
      var label = reduced ? ADE.t('app.stepOnce') : (playing ? ADE.t('app.pause') : (disc && S.pos > S.N ? ADE.t('app.replay') : ADE.t('app.play')));
      bPlay.appendChild(icon(reduced ? 'next' : (playing ? 'pause' : 'play'), { size: 16 }));
      bPlay.appendChild(h('span', { text: label }));
      bPlay.setAttribute('aria-pressed', playing ? 'true' : 'false');
      bPlay.title = reduced ? ADE.t('app.reducedPlayHint') : label + ' (Space)';
      if (disc) {
        bPrev.disabled = S.pos <= 0; bNext.disabled = S.pos > S.N;
        pos.textContent = S.pos === 0 ? ADE.t('app.overview') : (S.pos > S.N ? ADE.t('app.wrapup') : S.pos + '/' + S.N);
      } else { pos.textContent = ADE.t('app.frameNo', { n: S.frame }); }
    }
    return { el: el, update: update };
  }

  function keys(root, S) {
    root.addEventListener('keydown', function (e) {
      if (e.defaultPrevented || e.ctrlKey || e.metaKey || e.altKey) return;
      if (e.target.closest && e.target.closest(NO_KEYS)) return;
      var disc = S.kind === 'discrete', k = e.key, used = true;
      if (k === 'ArrowRight') { if (disc) S.next(); else S.stepFrame(); }
      else if (k === 'ArrowLeft') { if (disc) S.prev(); else used = false; }
      else if (k === ' ') S.toggle();
      else if (k === 'r' || k === 'R') S.reset();
      else if (disc && /^[1-9]$/.test(k)) S.goto(parseInt(k, 10));
      else if (k === '[' || k === ']') {
        var i = SPEEDS.indexOf(S.speed); if (i < 0) i = 1;
        i = Math.max(0, Math.min(SPEEDS.length - 1, i + (k === ']' ? 1 : -1))); S.setSpeed(SPEEDS[i]);
      } else used = false;
      if (used) e.preventDefault();
    });
  }

  // Phím toàn cục: ? bảng phím tắt · / hoặc Ctrl+K tìm kiếm · Esc đóng drawer. Bỏ qua khi đang gõ.
  function global(hooks) {
    document.addEventListener('keydown', function (e) {
      var t = e.target, typing = t && t.closest && t.closest('input,textarea,select,[contenteditable=true]');
      if ((e.ctrlKey || e.metaKey) && (e.key === 'k' || e.key === 'K')) { e.preventDefault(); hooks.openSearch(); return; }
      if (typing || e.ctrlKey || e.metaKey || e.altKey) return;
      if (document.querySelector('dialog[open]')) return;
      if (e.key === '/') { e.preventDefault(); hooks.openSearch(); }
      else if (e.key === '?') { e.preventDefault(); hooks.openHelp(); }
      else if (e.key === 'Escape' && hooks.closeDrawer) hooks.closeDrawer();
    });
  }

  function helpBody() {
    var groups = [
      ['app.keys.controls', [['←  →', 'app.keys.prevNext'], ['Space', 'app.keys.playPause'], ['R', 'app.keys.reset'], ['1 – 9', 'app.keys.jump'], ['[  ]', 'app.keys.speed']]],
      ['app.keys.view', [['Esc', 'app.keys.esc'], ['Tab', 'app.keys.tab']]],
      ['app.keys.find', [['Ctrl K  /  /', 'app.keys.search'], ['?', 'app.keys.help']]],
      ['app.keys.log', [['Enter', 'app.keys.rowJump']]]
    ];
    var wrap = h('div', { class: 'keys' });
    groups.forEach(function (g) {
      var dl = h('dl');
      g[1].forEach(function (p) { dl.appendChild(h('div', null, h('dt', null, p[0].split('  ').map(function (k) { return k ? h('kbd', { text: k }) : null; })), h('dd', { text: ADE.t(p[1]) }))); });
      wrap.appendChild(h('section', null, h('h3', { class: 'caps', text: ADE.t(g[0]) }), dl));
    });
    wrap.appendChild(h('p', { class: 'hint', text: ADE.t('app.keys.note') }));
    return wrap;
  }

  ADE.controls = { bar: bar, keys: keys, global: global, helpBody: helpBody, SPEEDS: SPEEDS };
})();
