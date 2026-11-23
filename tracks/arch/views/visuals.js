/* Hình trực quan theo bước của track G (ADE.registerScreen với nhãn tab riêng). Sơ đồ node vẫn ở tab bên cạnh.
   G2: ĐỒ THỊ PHỤ THUỘC giữa các tầng. Mũi tên nghĩa là "A biết về B" (A import B), không phải chiều dữ liệu.
   Cạnh, nhóm module và kết quả build lấy từ ADE.archLayers (models.js), không tính lại ở đây. */
(function () {
  'use strict';
  var K = 'track.arch.vz.';
  var T = function (k, p) { return ADE.t(K + k, p); };
  var NS = 'http://www.w3.org/2000/svg';
  var KS = ['s1', 's2', 's3', 's4'];
  function idx(ctx) {
    if (ctx.step) return KS.indexOf(ctx.step.id.split('.').pop());
    return ctx.pos > ctx.N ? 3 : 0;
  }
  function esc(s) { return ADE.esc(String(s)); }

  /* ---------- G2: đồ thị phụ thuộc giữa các tầng ---------- */
  var BW = 240, BH = 38;
  var POS = { ui: [270, 34], vm: [270, 104], uc: [270, 174], repo: [270, 244], api: [140, 318], dao: [400, 318] };
  ADE.registerScreen('arch.layers', function (box, ctx) {
    var h = ADE.ui.h, c = ctx.state.case, i = idx(ctx), d = ADE.archLayers.at(c, i);
    var uid = 'dg' + Math.random().toString(36).slice(2, 8);
    var inv = c === 'inverted' && i >= 1;
    var label = function (n) {
      if (n === 'uc' && inv) return [T('n.uc'), T('n.ucIface')];
      if (n === 'repo' && inv) return [T('n.repo'), T('n.repoImpl')];
      return [T('n.' + n), T('n.' + n + '.cls')];
    };
    var svg = '<svg viewBox="0 0 540 352" class="vz-dg" role="img" aria-label="' + esc(T('dg.cap')) + '"><title>' + esc(T('dg.cap')) + '</title>' +
      '<defs><marker id="' + uid + 'a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M1 1.5L9 5 1 8.5z" class="vz-dg-head"/></marker>' +
      '<marker id="' + uid + 'b" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M1 1.5L9 5 1 8.5z" class="vz-dg-head bad"/></marker>' +
      '<marker id="' + uid + 'd" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M1 1.5L9 5 1 8.5z" class="vz-dg-head data"/></marker></defs>';
    // nhóm module (tình huống tách module)
    if (d.mods) {
      var frame = { feature: [16, 10, 508, 132], domain: [16, 150, 508, 62], data: [16, 220, 508, 126] };
      d.mods.forEach(function (mo) {
        var f = frame[mo[0]];
        svg += '<rect class="vz-dg-mod" x="' + f[0] + '" y="' + f[1] + '" width="' + f[2] + '" height="' + f[3] + '" rx="8"/>' +
          '<text class="vz-dg-modt" x="' + (f[0] + f[2] - 8) + '" y="' + (f[1] + 15) + '" text-anchor="end">' + esc(T('mod.' + mo[0])) + '</text>';
      });
    }
    // dữ liệu đi ngược lên (chỉ một bước của tình huống chuẩn)
    if (d.dataUp) {
      svg += '<path class="vz-dg-data" d="M' + (POS.dao[0] - 40) + ' ' + (POS.dao[1] - BH / 2) + ' C 470 270, 470 120, ' + (POS.ui[0] + BW / 2 + 4) + ' ' + POS.ui[1] + '" marker-end="url(#' + uid + 'd)"/>' +
        '<text class="vz-dg-datat" x="476" y="196" text-anchor="middle">' + esc(T('dg.dataUp')) + '</text>';
    }
    // cạnh phụ thuộc
    d.edges.forEach(function (e) {
      var a = POS[e.from], b = POS[e.to], path, cls = 'vz-dg-e' + (e.bad ? ' bad' : '');
      if (e.bad) {
        path = 'M' + (a[0] - BW / 2) + ' ' + a[1] + ' C 40 ' + a[1] + ', 40 ' + b[1] + ', ' + (b[0] - BW / 2 - 2) + ' ' + b[1];
      } else if (a[1] > b[1]) {   // mũi tên đi lên (đảo phụ thuộc)
        path = 'M' + a[0] + ' ' + (a[1] - BH / 2) + ' L ' + b[0] + ' ' + (b[1] + BH / 2 + 2);
        cls += ' up';
      } else {
        var sx = a[0] + (b[0] - a[0]) * 0.25;
        path = 'M' + sx + ' ' + (a[1] + BH / 2) + ' L ' + b[0] + ' ' + (b[1] - BH / 2 - 2);
      }
      svg += '<path class="' + cls + '" d="' + path + '" marker-end="url(#' + uid + (e.bad ? 'b' : 'a') + ')"/>';
      if (e.bad) svg += '<text class="vz-dg-badt" x="36" y="' + ((a[1] + b[1]) / 2) + '" text-anchor="middle" transform="rotate(-90 36 ' + ((a[1] + b[1]) / 2) + ')">' + esc(T('dg.badEdge')) + '</text>';
    });
    // node
    Object.keys(POS).forEach(function (n) {
      var p = POS[n], skip = n === 'uc' && d.noUc, bad = d.edges.some(function (e) { return e.bad && (e.from === n || e.to === n); });
      var lb = label(n);
      svg += '<g class="vz-dg-n' + (skip ? ' skip' : '') + (bad ? ' bad' : '') + '"><rect x="' + (p[0] - BW / 2) + '" y="' + (p[1] - BH / 2) + '" width="' + BW + '" height="' + BH + '" rx="5"/>' +
        '<text x="' + p[0] + '" y="' + (p[1] - 3) + '" text-anchor="middle" class="vz-dg-t">' + esc(skip ? T('n.ucSkip') : lb[0]) + '</text>' +
        '<text x="' + p[0] + '" y="' + (p[1] + 12) + '" text-anchor="middle" class="vz-dg-s">' + esc(skip ? '' : lb[1]) + '</text></g>';
    });
    svg += '</svg>';
    var holder = h('div', { class: 'vz-scroll' }); holder.innerHTML = svg;
    var build = h('p', { class: 'vz-cap vz-dg-build' + (d.build === 'unresolved' || d.build === 'cycle' ? ' bad' : '') },
      h('b', { text: T('build.label') + ': ' }), h('span', { text: T('build.' + d.build) }));
    var legend = h('div', { class: 'vz-legend' },
      h('span', { class: 'vz-dg-lg' }, h('i', { class: 'e' }), h('span', { text: T('lg.dep') })),
      h('span', { class: 'vz-dg-lg' }, h('i', { class: 'e bad' }), h('span', { text: T('lg.bad') })),
      h('span', { class: 'vz-dg-lg' }, h('i', { class: 'e data' }), h('span', { text: T('lg.data') })),
      d.mods ? h('span', { class: 'vz-dg-lg' }, h('i', { class: 'm' }), h('span', { text: T('lg.mod') })) : null);
    box.appendChild(h('div', { class: 'vz' }, h('p', { class: 'vz-cap', text: T('dg.cap') }), holder, build, legend));
  }, { labelKey: K + 'tab.dg', icon: 'layers' });
})();
