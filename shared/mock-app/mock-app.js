/* Ứng dụng mẫu HƯ CẤU "Hẹn Khám / ClinicBook" (dùng chung cho track D, E và các track sau). Không mô phỏng app hay thương hiệu có thật.
   ADE.mockApp.screen(id, opts) → phần tử DOM của một màn (đặt trong ADE.ui.mockFrame). Chữ lấy từ khoá shared.mock.* nên đổi theo ngôn ngữ site.
   opts: { spots: {spotId: true} (đánh dấu vùng), onSpot(id), variant: {...} } — dùng cho workbench heuristic và các bài tập. */
(function () {
  'use strict';
  var A = ADE.mockApp = {};
  var T = function (k, p) { return ADE.t('shared.mock.' + k, p); };
  A.SCREENS = ['home', 'services', 'time', 'confirm', 'mine', 'settings'];
  var CSS = '.ma{font:14px var(--sans,system-ui);color:#1b1b1b;display:flex;flex-direction:column;gap:8px;padding:10px;min-height:340px}' +
    '.ma h4{margin:0;font-size:16px}.ma .ma-bar{display:flex;justify-content:space-between;align-items:center;font-weight:700}' +
    '.ma .ma-card{border:1px solid #8a9a96;border-radius:12px;padding:8px 10px;display:flex;justify-content:space-between;gap:6px;align-items:center;background:#fff}' +
    '.ma .ma-btn{border:1px solid #1b1b1b;border-radius:20px;padding:8px 12px;text-align:center;font-weight:700;background:#fff;color:#1b1b1b}.ma .ma-btn.pri{background:#0b776d;color:#fff;border-color:#0b776d}' +
    '.ma .ma-btn.faint{opacity:.55;border-style:dashed}.ma .ma-muted{color:#545454;font-size:12px}.ma .ma-row{display:flex;gap:6px;flex-wrap:wrap}' +
    '.ma .ma-chip{border:1px solid #8a9a96;border-radius:8px;padding:6px 8px;font-size:13px}.ma .ma-chip.sel{outline:2px solid #0b776d}' +
    '.ma .ma-spot{position:relative;cursor:pointer}.ma .ma-spot.mark{outline:2px dashed #b0287a;outline-offset:2px}.ma .ma-spot:focus-visible{outline:2px solid var(--focus)}' +
    '.ma .ma-spot .ma-tag{position:absolute;top:-8px;right:-6px;background:#b0287a;color:#fff;border-radius:8px;font:700 10px var(--mono);padding:0 4px}' +
    '.ma .ma-err{color:#b3261e;font-size:12px}.ma input.ma-in{border:1px solid #8a9a96;border-radius:8px;padding:8px;font:inherit;background:#fff;color:#1b1b1b;width:100%;box-sizing:border-box}';
  function style() { if (document.getElementById('ma-style')) return; var s = document.createElement('style'); s.id = 'ma-style'; s.textContent = CSS; document.head.appendChild(s); }
  /* Màn mẫu luôn nền sáng (styles.css .mf-screen) nên dùng bảng màu cố định: chữ #1b1b1b, phụ #545454 (7.4:1), nút chính #0b776d chữ trắng (5.3:1), lỗi #b3261e (6.5:1). */
  /* spot: vùng có thể đánh dấu (heuristic workbench). Không có onSpot thì chỉ là phần tử thường. */
  function spot(h, o, id, el) {
    if (!o.onSpot) return el;
    var w = h('div', { class: 'ma-spot' + (o.spots && o.spots[id] ? ' mark' : ''), tabindex: '0', role: 'button', 'data-fk': 'spot-' + id, 'aria-pressed': o.spots && o.spots[id] ? 'true' : 'false', 'aria-label': T('spotLabel', { id: id.toUpperCase() }) }, el);
    if (o.spots && o.spots[id]) w.appendChild(h('span', { class: 'ma-tag', text: id.toUpperCase() }));
    var go = function (e) { e.preventDefault(); ADE.ui.withFocus(function () { o.onSpot(id); }); };
    w.addEventListener('click', go); w.addEventListener('keydown', function (e) { if (e.key === 'Enter' || e.key === ' ') go(e); });
    return w;
  }
  A.screen = function (id, o) {
    style(); o = o || {}; var h = ADE.ui.h, v = o.variant || {};
    var root = h('div', { class: 'ma', lang: ADE.lang });
    var bar = function (title, extra) { return h('div', { class: 'ma-bar' }, h('h4', { text: title }), extra || h('span')); };
    if (id === 'home') {
      root.appendChild(bar(T('app')));
      root.appendChild(h('p', { class: 'ma-muted', text: T('home.hello') }));
      root.appendChild(spot(h, o, 'h1', h('div', { class: 'ma-card' }, h('span', null, h('b', { text: T('home.next') }), h('br'), h('span', { class: 'ma-muted', text: T('home.nextWhen') })), h('span', { text: '›' }))));
      root.appendChild(spot(h, o, 'h2', h('div', { class: 'ma-btn pri', text: T('home.book') })));
      root.appendChild(spot(h, o, 'h3', h('div', { class: 'ma-row' }, h('span', { class: 'ma-chip', text: '⌂' }), h('span', { class: 'ma-chip', text: '☰' }), h('span', { class: 'ma-chip', text: '⚙' }))));
    } else if (id === 'services') {
      root.appendChild(spot(h, o, 's2', bar(T('services.title'))));
      if (v.recent) root.appendChild(h('p', { class: 'ma-muted', text: T('services.recent') }));
      var list = h('div', { class: 'ma', style: 'padding:0;min-height:0' });
      ['general', 'dental', 'eye', 'skin'].forEach(function (x) { list.appendChild(h('div', { class: 'ma-card' }, h('span', { text: T('svc.' + x) }), h('span', { class: 'ma-muted', text: T('svc.' + x + '.price') }))); });
      root.appendChild(spot(h, o, 's1', list));
    } else if (id === 'time') {
      root.appendChild(bar(T('time.title')));
      root.appendChild(spot(h, o, 't1', h('div', { class: 'ma-row' }, ['08:00', '08:30', '09:00', '09:30'].map(function (t, i) { return h('span', { class: 'ma-chip' + (i === 2 ? ' sel' : ''), text: t }); }))));
      root.appendChild(spot(h, o, 't2', h('p', { class: 'ma-muted', text: T('time.full') })));
      root.appendChild(spot(h, o, 't3', h('div', { class: 'ma-row' }, h('div', { class: 'ma-btn', text: T('time.back') }), h('div', { class: 'ma-btn', text: T('time.next') }))));
    } else if (id === 'confirm') {
      root.appendChild(bar(T('confirm.title')));
      root.appendChild(spot(h, o, 'c1', h('div', { class: 'ma-card' }, h('span', { text: T('confirm.summary') }))));
      root.appendChild(spot(h, o, 'c2', h('label', null, h('span', { class: 'ma-muted', text: T('confirm.phone') }), h('input', { class: 'ma-in', value: '0901 234 567', 'aria-label': T('confirm.phone'), readonly: 'readonly' }))));
      root.appendChild(spot(h, o, 'c3', h('p', { class: 'ma-err', text: T('confirm.error') })));
      root.appendChild(spot(h, o, 'c4', h('div', { class: 'ma-row' }, h('div', { class: 'ma-btn pri', text: T('confirm.ok') }), h('div', { class: 'ma-btn faint', text: T('confirm.cancel') }))));
    } else if (id === 'mine') {
      root.appendChild(bar(T('mine.title')));
      root.appendChild(h('div', { class: 'ma-card' }, h('span', { text: T('home.nextWhen') }), spot(h, o, 'm1', h('span', { class: 'ma-muted', text: T('mine.edit') }))));
      root.appendChild(spot(h, o, 'm3', h('div', { class: 'ma-btn', text: T('mine.cancelAppt') })));
      root.appendChild(h('p', { class: 'ma-muted', text: T('mine.past') }));
      root.appendChild(spot(h, o, 'm2', h('p', { class: 'ma-muted', text: T('mine.empty') })));
    } else {
      root.appendChild(bar(T('settings.title')));
      root.appendChild(h('div', { class: 'ma-card' }, h('span', { text: T('settings.autosave') }), h('span', { text: v.autosave ? '◉' : '○' })));
      root.appendChild(h('div', { class: 'ma-card' }, h('span', { text: T('settings.reminder') }), h('span', { text: '◉' })));
      root.appendChild(h('div', { class: 'ma-card' }, h('span', { text: T('settings.lang') }), h('span', { class: 'ma-muted', text: ADE.lang === 'vi' ? 'Tiếng Việt' : 'English' })));
    }
    return root;
  };
})();
