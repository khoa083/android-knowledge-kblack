/* Màn hình mẫu theo bước của track D (ADE.registerScreen). Ứng dụng "Hẹn Khám / ClinicBook" là hư cấu.
   Mọi thứ vẽ ở đây là minh họa: chấm số (thứ tự mắt dừng) đi theo số đo của bước trong model, không phải dữ liệu eye tracking. */
(function () {
  'use strict';
  var K = 'track.ux.scr.glance.';
  var T = function (k, p) { return ADE.t(K + k, p); };
  function times(n) {
    var out = [];
    for (var i = 0; i < n; i++) { var mm = 12 * 60 + 15 * i; out.push(Math.floor(mm / 60) + ':' + ('0' + (mm % 60)).slice(-2)); }
    return out;
  }

  /* ---------- D1: ux.glance — mắt và trí nhớ làm việc trên màn Chọn giờ ---------- */
  ADE.registerScreen('ux.glance', function (box, ctx) {
    var h = ADE.ui.h, v = ctx.state.which, vs = ctx.viewState;
    var last = ctx.steps[ctx.steps.length - 1];
    var key = ctx.step ? ctx.step.id.split('.')[1] : (ctx.pos > ctx.N && last ? last.id.split('.')[1] : 'intro');
    var met = (ctx.step && ctx.step.metrics) || {};
    var hasDots = false;
    function dot(n, delay) { hasDots = true; return h('span', { class: 'mk-dot', 'aria-hidden': 'true', style: delay ? 'animation-delay:' + delay + 'ms' : null, text: String(n) }); }

    // lưới ô giờ: style 'pop' (ô trống khác hẳn) hoặc 'same' (mọi ô như nhau, chỉ thêm chữ "trống"); look: null | 'free' | 'serial'
    function grid(n, style, look, tap) {
      var free = n === 24 ? 17 : 8, g = h('div', { class: 'mk-grid' + (n > 12 ? ' dense' : '') });
      times(n).forEach(function (t, i) {
        var isFree = i === free, cls = 'mk-slot';
        if (style === 'pop') cls += isFree ? ' free-pop' : ' full-dim';
        if (isFree && tap) cls += ' tap';
        var el = h('div', { class: cls }, h('span', { text: t }), style === 'same' && isFree ? h('small', { text: T('free') }) : null);
        if (look === 'free' && isFree) el.appendChild(dot(1));
        if (look === 'serial' && i <= free) el.appendChild(dot(i + 1, ctx.reduced ? 0 : i * 70));
        g.appendChild(el);
      });
      return g;
    }
    function timeScreen(n, style, look, tap, promo) {
      var scr = [h('div', { class: 'mk-appbar', text: ADE.t('shared.mock.app') }), h('div', { class: 'mk-title', text: ADE.t('shared.mock.time.title') }),
        h('div', { class: 'mk-sub', text: T('sub') }), grid(n, style, look, tap)];
      if (promo) {
        var card = h('div', { class: 'mk-card' + (promo === 'unseen' ? ' mk-unseen' : ''), 'data-label': promo === 'unseen' ? T('unseen') : null },
          h('span', { class: 'mk-blob', 'aria-hidden': 'true' }), h('span', null, h('b', { text: T('promoHead') }), h('span', { text: T('promoBody') })));
        scr.push(card);
      }
      if (!promo) scr.push(h('div', { class: 'mk-btn', text: ADE.t('shared.mock.time.next') }));
      return scr;
    }
    function confirmScreen() {
      var row = h('div', { class: 'mk-row', text: T('confirmSvc') }), note = h('div', { class: 'mk-note', text: T('fastNote') });
      row.appendChild(dot(1)); note.appendChild(dot(2));
      return [h('div', { class: 'mk-appbar', text: ADE.t('shared.mock.app') }), h('div', { class: 'mk-title', text: ADE.t('shared.mock.confirm.title') }), row, note, h('div', { class: 'mk-btn', text: T('book') })];
    }
    function bookedScreen(snack, dotOnSnack) {
      var scr = [h('div', { class: 'mk-appbar', text: ADE.t('shared.mock.app') }), h('div', { class: 'mk-title', text: T('booked') }), h('div', { class: 'mk-ok', text: '✓ ' + T('bookedSum') })];
      if (snack === 'code') { var sn = h('div', { class: 'mk-snack' }, h('span', { text: T('snack') }), h('span', { class: 'mk-timer', 'aria-hidden': 'true' })); if (dotOnSnack) sn.appendChild(dot(1)); scr.push(sn); }
      if (snack === 'fixed') {
        var codeRow = h('div', { class: 'mk-row big' }, h('span', null, h('small', { text: T('codeLabel') }), h('span', { text: '4821 9307' })), h('span', { class: 'mk-btn ghost', text: T('copy') }));
        codeRow.appendChild(dot(1));
        scr.push(codeRow, h('div', { class: 'mk-snack' }, h('span', { text: T('copied') })));
      }
      return scr;
    }
    function chatScreen() {
      return [h('div', { class: 'mk-chat-h', text: T('chatTitle') }), h('div', { class: 'mk-bubble', text: T('chatClinic') }), h('div', { class: 'mk-input', text: T('chatInput') })];
    }
    // trí nhớ làm việc của Lan (dưới điện thoại): 8 chữ số, ô thứ 6 trở đi vượt mức 3–5 của Norman
    function memRow(mode) {
      if (mode === 'none') return h('p', { class: 'scr-cap', text: T('memNone') });
      var row = h('div', { class: 'scr-mem', role: 'img', 'aria-label': T('mem') + ' ' + (mode === 'lost' ? '4821????' : '48219307') }, h('span', { class: 'lbl', text: T('mem') }));
      '48219307'.split('').forEach(function (d, i) {
        if (i === 4) row.appendChild(h('span', { class: 'gap' }));
        var lost = mode === 'lost' && i >= 4;
        row.appendChild(h('span', { class: 'cell' + (i >= 5 ? ' over' : '') + (lost ? ' lost' : ''), text: lost ? '?' : d }));
      });
      return row;
    }

    var screen, below = [];
    if (v === 'popout') screen = timeScreen(key === 'double' ? 24 : 12, 'pop', key === 'intro' ? null : 'free', key === 'act');
    else if (v === 'nopop') screen = key === 'fix' ? timeScreen(12, 'pop', 'free', true) : timeScreen(key === 'double' ? 24 : 12, 'same', key === 'intro' ? null : 'serial');
    else if (v === 'sidenote') {
      if (key === 'fix') screen = confirmScreen();
      else screen = timeScreen(12, 'pop', key === 'intro' ? null : 'free', false, key === 'intro' ? 'card' : 'unseen');
      if (key === 'cost') below.push(h('p', { class: 'scr-out', text: T('cost') }));
    } else {
      if (key === 'gone') { screen = chatScreen(); below.push(memRow('lost'), h('p', { class: 'scr-out', text: T('gone') })); }
      else if (key === 'fix') { screen = bookedScreen('fixed'); below.push(memRow('none')); }
      else { screen = bookedScreen('code', key === 'read'); if (key === 'read') below.push(memRow('full'), h('p', { class: 'scr-cap', text: T('memLimit') })); }
    }

    var on = !!vs.attnView;
    box.appendChild(h('div', { class: 'scr-tools' }, h('button', { type: 'button', class: 'btn small toggle', 'data-fk': 'scr-attn', 'aria-pressed': on ? 'true' : 'false',
      onclick: function () { vs.attnView = !on; ctx.redraw(); } }, ADE.ui.icon('eye', { size: 14 }), h('span', { text: T('attn') }))));
    box.appendChild(h('div', { class: on ? 'scr-attn' : '' }, ADE.ui.mockFrame(h('div', null, screen))));
    below.forEach(function (el) { box.appendChild(el); });
    if (on) box.appendChild(h('p', { class: 'scr-cap', text: T('attnHint') }));
    else if (hasDots) box.appendChild(h('p', { class: 'scr-cap', text: T('dots') }));
    if (met.fix) box.appendChild(h('p', { class: 'sr-only', text: T('srFix', { n: met.fix }) }));
  });
})();
