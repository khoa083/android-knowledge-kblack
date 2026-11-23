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
  // chữ monospace 11px rộng khoảng 6.6px mỗi ký tự; nhãn dài hơn hộp thì ép vừa hộp thay vì tràn ra ngoài
  function fitText(str, w) { return String(str).length * 6.6 > w ? ' textLength="' + w + '" lengthAdjust="spacingAndGlyphs"' : ''; }

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

  /* ---------- Làn thời gian (G3, G4): hàng là các làn, cột là bốn bước; cột sau bước hiện tại để trống ---------- */
  // src = { LANES, at(case, step) -> { lane: [mã ô, kiểu ô] } }; chuỗi: vz.<p>.cap, .legend, .lane, .lane.<làn>, .col.<case>.<k>, .cell.<mã>
  function laneScreen(modelId, getSrc, p, tabKey) {
    ADE.registerScreen(modelId, function (box, ctx) {
      var h = ADE.ui.h, c = ctx.state.case, i = idx(ctx), E = getSrc();
      var head = h('tr', null, h('th', { text: T(p + '.lane') }), [0, 1, 2, 3].map(function (k) { return h('th', { class: k === i ? 'hl' : null, text: T(p + '.col.' + c + '.' + k) }); }));
      var tb = h('tbody');
      E.LANES.forEach(function (ln) {
        var tr = h('tr', null, h('th', { text: T(p + '.lane.' + ln) }));
        for (var k = 0; k < 4; k++) {
          if (k > i) { tr.appendChild(h('td', { class: 'dim', text: '·' })); continue; }
          var cell = E.at(c, k)[ln], cls = cell[1] || '';
          if (k < i && cls === 'hl') cls = '';   // chỉ cột của bước đang xem được viền
          if (k === i && cls === '') cls = 'ok';
          tr.appendChild(h('td', { class: cls || null, text: T(p + '.cell.' + cell[0]) }));
        }
        tb.appendChild(tr);
      });
      var tbl = h('table', { class: 'vz-table vz-lanes' }, h('thead', null, head), tb);
      box.appendChild(h('div', { class: 'vz' }, h('p', { class: 'vz-cap', text: T(p + '.cap') }), h('div', { class: 'vz-scroll' }, tbl),
        h('div', { class: 'vz-legend', text: T(p + '.legend') })));
    }, { labelKey: K + tabKey, icon: 'clock' });
  }
  laneScreen('arch.events', function () { return ADE.archEvents; }, 'ev', 'tab.ev');       // G3: qua một lần xoay màn hình
  laneScreen('arch.offline', function () { return ADE.archOffline; }, 'off', 'tab.off');   // G4: mạng, database, repository, UI

  /* ---------- G5: bảng quy tắc theo nơi viết, và cây "có cần use case không" ---------- */
  ADE.registerScreen('arch.usecase', function (box, ctx) {
    var h = ADE.ui.h, c = ctx.state.case, i = Math.max(0, idx(ctx)), U = ADE.archUseCase, t = U.at(c, i);
    var head = h('tr', null, h('th', { text: T('uc.colRule') }), U.COLS.map(function (col) { return h('th', { text: T('uc.col.' + col) }); }));
    var tb = h('tbody');
    U.ROWS.forEach(function (row) {
      var tr = h('tr', null, h('th', { text: T('uc.row.' + row) }));
      U.COLS.forEach(function (col) {
        var v = t[col][row], cls = v === '-' ? 'dim' : null;
        if (row === 'lead' && v === '1h' && U.COLS.some(function (o) { return t[o].lead === '2h'; })) cls = 'bad';   // ngưỡng cũ còn sót
        if (row === 'ans' && (v === 'yes' || v === 'no') && U.COLS.some(function (o) { var w = t[o].ans; return (w === 'yes' || w === 'no') && w !== v; })) cls = 'bad';
        if (v === 'fwd') cls = 'bad';
        tr.appendChild(h('td', { class: cls, text: T('uc.v.' + v) }));
      });
      tb.appendChild(tr);
    });
    var tbl = h('table', { class: 'vz-table' }, h('thead', null, head), tb);
    // cây quyết định: hộp lồng, nhánh trên đường đi được viền
    var p = U.path(c), show = i >= 3 || c !== 'duplicated';
    var leaf = function (k, on) { return h('div', { class: 'vz-box' + (on ? ' hl' : '') }, h('span', { class: 'vz-h', text: T('uc.leaf.' + k) })); };
    var tree = h('div', { class: 'vz-box' }, h('span', { class: 'vz-h', text: T('uc.q.reuse') }),
      h('div', { class: 'vz-box' + (show && p.reuse === 'yes' ? ' hl' : '') }, h('span', { text: T('uc.yes') }), leaf('useCase', show && p.reuse === 'yes')),
      h('div', { class: 'vz-box' + (show && p.reuse === 'no' ? ' hl' : '') }, h('span', { text: T('uc.no') + ' · ' + T('uc.q.complex') }),
        h('div', { class: 'vz-box' }, h('span', { text: T('uc.yes') }), leaf('useCaseOrRepo', false)),
        h('div', { class: 'vz-box' + (show && p.complex === 'no' ? ' hl' : '') }, h('span', { text: T('uc.no') }), leaf('none', show && p.leaf === 'none'))));
    box.appendChild(h('div', { class: 'vz' }, h('p', { class: 'vz-cap', text: T('uc.cap') }), h('div', { class: 'vz-scroll' }, tbl),
      h('p', { class: 'vz-cap', text: T('uc.treeCap') }), tree, h('div', { class: 'vz-legend', text: T('uc.legend') })));
  }, { labelKey: K + 'tab.uc', icon: 'grid' });

  /* ---------- G6: sơ đồ phạm vi: ba dải sống lâu tới ngắn; mũi tên "giữ tham chiếu" ---------- */
  // Mũi tên từ dải sống lâu hơn sang dải sống ngắn hơn là rò rỉ (đỏ); mũi tên đứt đỏ là lỗi Hilt bắt lúc biên dịch.
  var BANDS = ['app', 'vm', 'act'], BX = { app: 8, vm: 204, act: 400 }, BWD = 188, RH = 44, OH = 34;
  ADE.registerScreen('arch.di', function (box, ctx) {
    var h = ADE.ui.h, c = ctx.state.case, i = Math.max(0, idx(ctx)), d = ADE.archDi.at(c, i);
    var uid = 'sc' + Math.random().toString(36).slice(2, 8), rows = 1;
    d.o.forEach(function (x) { rows = Math.max(rows, x.row + 1); });
    var H = 40 + rows * RH + 10, pos = {};
    var svg = '<svg viewBox="0 0 596 ' + H + '" class="vz-dg" role="img" aria-label="' + esc(T('di.cap')) + '"><title>' + esc(T('di.cap')) + '</title>' +
      '<defs><marker id="' + uid + 'a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M1 1.5L9 5 1 8.5z" class="vz-dg-head"/></marker>' +
      '<marker id="' + uid + 'b" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M1 1.5L9 5 1 8.5z" class="vz-dg-head bad"/></marker></defs>';
    BANDS.forEach(function (b) {
      svg += '<rect class="vz-dg-mod" x="' + BX[b] + '" y="6" width="' + BWD + '" height="' + (H - 12) + '" rx="8"/>' +
        '<text class="vz-dg-modt" x="' + (BX[b] + BWD / 2) + '" y="24" text-anchor="middle">' + esc(T('di.band.' + b)) + '</text>';
    });
    d.o.forEach(function (x) { pos[x.id] = [BX[x.band] + 10, 38 + x.row * RH, BWD - 20, OH]; });
    d.a.forEach(function (a) {
      var p = pos[a.from], q = pos[a.to]; if (!p || !q) return;
      var x1, y1 = p[1] + OH / 2, x2, y2 = q[1] + OH / 2;
      if (p[0] === q[0] && q[1] > p[1]) { x1 = p[0] + p[2] - 14; y1 = p[1] + OH; x2 = q[0] + q[2] - 14; y2 = q[1] - 2; }
      else if (p[0] === q[0]) { x1 = p[0] + p[2] - 14; y1 = p[1]; x2 = q[0] + q[2] - 14; y2 = q[1] + OH + 2; }
      else if (p[0] < q[0]) { x1 = p[0] + p[2]; x2 = q[0] - 2; }
      else { x1 = p[0]; x2 = q[0] + q[2] + 2; }
      svg += '<path class="vz-dg-e' + (a.cls ? ' bad' : '') + '" d="M' + x1 + ' ' + y1 + ' L ' + x2 + ' ' + y2 + '" marker-end="url(#' + uid + (a.cls ? 'b' : 'a') + ')"/>';
      if (a.cls === 'err') svg += '<text class="vz-dg-badt" x="' + ((x1 + x2) / 2) + '" y="' + (Math.min(y1, y2) - 6) + '" text-anchor="middle">' + esc(T('di.compileErr')) + '</text>';
    });
    d.o.forEach(function (x) {
      var p = pos[x.id];
      svg += '<g class="vz-dg-n' + (x.cls === 'bad' ? ' bad' : '') + '"><rect x="' + p[0] + '" y="' + p[1] + '" width="' + p[2] + '" height="' + p[3] + '" rx="5"/>' +
        '<text x="' + (p[0] + p[2] / 2) + '" y="' + (p[1] + 21) + '" text-anchor="middle" class="vz-dg-s"' + fitText(T('di.o.' + x.k), p[2] - 12) + '>' + esc(T('di.o.' + x.k)) + '</text></g>';
    });
    svg += '</svg>';
    var holder = h('div', { class: 'vz-scroll' }); holder.innerHTML = svg;
    box.appendChild(h('div', { class: 'vz' }, h('p', { class: 'vz-cap', text: T('di.cap') }), holder,
      h('div', { class: 'vz-legend' }, h('span', { class: 'vz-dg-lg' }, h('i', { class: 'e' }), h('span', { text: T('di.lg.hold') })),
        h('span', { class: 'vz-dg-lg' }, h('i', { class: 'e bad' }), h('span', { text: T('di.lg.leak') })))));
  }, { labelKey: K + 'tab.di', icon: 'layers' });

  /* ---------- G7: ma trận tổ hợp đang tải × lỗi × dữ liệu ---------- */
  ADE.registerScreen('arch.mvi', function (box, ctx) {
    var h = ADE.ui.h, c = ctx.state.case, i = Math.max(0, idx(ctx)), X = ADE.archMvi, seen = X.seen(c, i), sealed = X.repr(c) < 8;
    var head = h('tr', null, ['L', 'E', 'D', 'screen', 'valid', 'seen'].map(function (k) { return h('th', { text: T('mvi.col.' + k) }); }));
    var tb = h('tbody'), yn = function (b) { return T(b === '1' ? 'mvi.yes' : 'mvi.no'); };
    X.COMBOS.forEach(function (cb) {
      var ok = X.valid(cb), at = [];
      seen.forEach(function (x, k) { if (x === cb) at.push(String(k + 1)); });
      var gone = sealed && !X.inSealed(cb);   // kiểu sealed không có trạng thái này
      var now = seen[seen.length - 1] === cb, cls = !ok && at.length ? 'bad' : (now ? 'hl' : (gone ? 'dim' : null));
      tb.appendChild(h('tr', null, h('td', { class: cls, text: yn(cb[0]) }), h('td', { class: cls, text: yn(cb[1]) }), h('td', { class: cls, text: yn(cb[2]) }),
        h('td', { class: cls, text: T('mvi.screen.' + cb) }), h('td', { class: cls, text: gone ? T('mvi.impossible') : T(ok ? 'mvi.ok' : 'mvi.wrong') }),
        h('td', { class: cls, text: at.length ? T('mvi.atStep') + ' ' + at.join(', ') : '·' })));
    });
    box.appendChild(h('div', { class: 'vz' }, h('p', { class: 'vz-cap', text: T('mvi.cap') }), h('div', { class: 'vz-scroll' }, h('table', { class: 'vz-table' }, h('thead', null, head), tb)),
      h('div', { class: 'vz-legend', text: T('mvi.legend') })));
  }, { labelKey: K + 'tab.mvi', icon: 'grid' });

  /* ---------- G8: bảng ánh xạ lỗi qua các tầng ---------- */
  ADE.registerScreen('arch.failure', function (box, ctx) {
    var h = ADE.ui.h, c = ctx.state.case, i = Math.max(0, idx(ctx)), F = ADE.archFailure, order = F.order(c);
    var head = h('tr', null, ['src', 'repo', 'vm', 'user'].map(function (k) { return h('th', { text: T('fl.col.' + k) }); }));
    var tb = h('tbody');
    order.forEach(function (r, k) {
      var cell = F.cell(c, r), on = k === i, shown = k <= i;
      var cls = function (bad) { return !shown ? 'dim' : (bad ? 'bad' : (on ? 'hl' : null)); };
      tb.appendChild(h('tr', null, h('th', { class: on ? 'hl' : null, text: T('fl.row.' + r) }),
        h('td', { class: cls(false), text: shown ? T('fl.v.' + cell[0]) : '·' }),
        h('td', { class: cls(false), text: shown ? T('fl.v.' + cell[1]) : '·' }),
        h('td', { class: cls(cell[3] === 'bad'), text: shown ? T('fl.v.' + cell[2]) : '·' })));
    });
    box.appendChild(h('div', { class: 'vz' }, h('p', { class: 'vz-cap', text: T('fl.cap') }),
      h('div', { class: 'vz-scroll' }, h('table', { class: 'vz-table' }, h('thead', null, head), tb)), h('div', { class: 'vz-legend', text: T('fl.legend') })));
  }, { labelKey: K + 'tab.fl', icon: 'grid' });

  /* ---------- G9: đồ thị module (node, cạnh, khung lấy từ model; mũi tên = "phụ thuộc") ---------- */
  var MW = 190, MH = 36;
  function edgeEnds(a, b) {   // từ mép hộp a tới mép hộp b, theo đường nối hai tâm
    var dx = b.x - a.x, dy = b.y - a.y, len = Math.sqrt(dx * dx + dy * dy) || 1;
    var t = function (p) { return Math.min(Math.abs(dx) > 0 ? (MW / 2 + p) / Math.abs(dx) : 1e9, Math.abs(dy) > 0 ? (MH / 2 + p) / Math.abs(dy) : 1e9); };
    var ta = t(0), tb = t(3);
    return [a.x + dx * ta, a.y + dy * ta, b.x - dx * tb, b.y - dy * tb, len];
  }
  ADE.registerScreen('arch.modules', function (box, ctx) {
    var h = ADE.ui.h, c = ctx.state.case, i = Math.max(0, idx(ctx)), d = ADE.archModules.at(c, i), pos = {};
    var uid = 'md' + Math.random().toString(36).slice(2, 8);
    d.n.forEach(function (n) { pos[n.id] = n; });
    var svg = '<svg viewBox="0 0 540 310" class="vz-dg" role="img" aria-label="' + esc(T('md.cap')) + '"><title>' + esc(T('md.cap')) + '</title>' +
      '<defs><marker id="' + uid + 'a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M1 1.5L9 5 1 8.5z" class="vz-dg-head"/></marker>' +
      '<marker id="' + uid + 'b" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M1 1.5L9 5 1 8.5z" class="vz-dg-head bad"/></marker></defs>';
    d.g.forEach(function (g) { svg += '<rect class="vz-dg-mod" x="' + g[1] + '" y="' + g[2] + '" width="' + g[3] + '" height="' + g[4] + '" rx="8"/><text class="vz-dg-modt" x="' + (g[1] + g[3] - 8) + '" y="' + (g[2] + 15) + '" text-anchor="end">' + esc(T('md.g.' + g[0])) + '</text>'; });
    d.e.forEach(function (e) {
      var a = pos[e.from], b = pos[e.to]; if (!a || !b) return;
      var back = d.e.some(function (o) { return o.from === e.to && o.to === e.from; }), off = back ? (e.from < e.to ? 8 : -8) : 0;
      var p = edgeEnds(a, b), nx = -(p[3] - p[1]) / p[4] * off, ny = (p[2] - p[0]) / p[4] * off;
      svg += '<path class="vz-dg-e' + (e.cls ? ' bad' : '') + '" d="M' + (p[0] + nx).toFixed(1) + ' ' + (p[1] + ny).toFixed(1) + ' L ' + (p[2] + nx).toFixed(1) + ' ' + (p[3] + ny).toFixed(1) + '" marker-end="url(#' + uid + (e.cls ? 'b' : 'a') + ')"/>';
      if (e.cls === 'err') {   // nhãn đặt lệch khỏi đường, về phía trên (pháp tuyến hướng lên), để không đè lên hộp
        var ux = -(p[3] - p[1]) / p[4], uy = (p[2] - p[0]) / p[4];
        if (Math.abs(ux) > 0.3 ? ux > 0 : uy > 0) { ux = -ux; uy = -uy; }   // cạnh xiên: nhãn bên trái; cạnh ngang: nhãn phía trên
        svg += '<text class="vz-dg-badt" x="' + ((p[0] + p[2]) / 2 + ux * 14).toFixed(1) + '" y="' + ((p[1] + p[3]) / 2 + uy * 14).toFixed(1) + '" text-anchor="' + (Math.abs(ux) > 0.3 ? 'end' : 'middle') + '">' + esc(T('md.err.' + d.build)) + '</text>';
      }
    });
    d.n.forEach(function (n) {
      var lb = T('md.n.' + n.k);
      svg += '<g class="vz-dg-n' + (n.cls === 'bad' ? ' bad' : '') + '"><rect x="' + (n.x - MW / 2) + '" y="' + (n.y - MH / 2) + '" width="' + MW + '" height="' + MH + '" rx="5"' + (n.cls === 'hl' ? ' style="stroke:var(--focus);stroke-width:2.4"' : '') + '/>' +
        '<text x="' + n.x + '" y="' + (n.y + 4) + '" text-anchor="middle" class="vz-dg-s"' + fitText(lb, MW - 12) + '>' + esc(lb) + '</text></g>';
    });
    svg += '</svg>';
    var holder = h('div', { class: 'vz-scroll' }); holder.innerHTML = svg;
    box.appendChild(h('div', { class: 'vz' }, h('p', { class: 'vz-cap', text: T('md.cap') }), holder,
      h('p', { class: 'vz-cap vz-dg-build' + (d.build === 'cycle' || d.build === 'internal' ? ' bad' : '') }, h('b', { text: T('md.build') + ': ' }), h('span', { text: T('md.b.' + d.build) })),
      h('div', { class: 'vz-legend' }, h('span', { class: 'vz-dg-lg' }, h('i', { class: 'e' }), h('span', { text: T('md.lg.dep') })),
        h('span', { class: 'vz-dg-lg' }, h('i', { class: 'e bad' }), h('span', { text: T('md.lg.bad') })))));
  }, { labelKey: K + 'tab.md', icon: 'layers' });

  /* ---------- G10: ma trận tầng × cách chạy test ---------- */
  ADE.registerScreen('arch.testing', function (box, ctx) {
    var h = ADE.ui.h, c = ctx.state.case, i = Math.max(0, idx(ctx)), X = ADE.archTesting;
    var head = h('tr', null, ['layer', 'where', 'double', 'time', 'stable'].map(function (k) { return h('th', { text: T('ts.col.' + k) }); }));
    var tb = h('tbody');
    X.ROWS.forEach(function (r, k) {
      var cell = X.cell(c, r), shown = k <= i, on = k === i;
      var cls = function (bad) { return !shown ? 'dim' : (bad ? 'bad' : (on ? 'hl' : null)); };
      tb.appendChild(h('tr', null, h('th', { class: on ? 'hl' : null, text: T('ts.row.' + r) }),
        h('td', { class: cls(cell[4] === 'bad' && cell[0] === 'jvmNet'), text: shown ? T('ts.where.' + cell[0]) : '·' }),
        h('td', { class: cls(false), text: shown ? T('ts.double.' + cell[1]) : '·' }),
        h('td', { class: cls(false), text: shown ? T('ts.time.' + cell[2]) : '·' }),
        h('td', { class: cls(cell[3] === 'flaky'), text: shown ? T('ts.stable.' + cell[3]) : '·' })));
    });
    box.appendChild(h('div', { class: 'vz' }, h('p', { class: 'vz-cap', text: T('ts.cap') }),
      h('div', { class: 'vz-scroll' }, h('table', { class: 'vz-table' }, h('thead', null, head), tb)), h('div', { class: 'vz-legend', text: T('ts.legend') })));
  }, { labelKey: K + 'tab.ts', icon: 'grid' });

  /* ---------- G11: dãy ô tiến độ di trú (màn hình) hay tiến độ tính năng (tầng) ---------- */
  ADE.registerScreen('arch.feature', function (box, ctx) {
    var h = ADE.ui.h, c = ctx.state.case, i = Math.max(0, idx(ctx)), F = ADE.archFeature, rows = F.at(c, i), prev = i > 0 ? F.at(c, i - 1) : null;
    var CLS = { old: '', fixed: '', new: 'ok', tested: '', none: 'dim', missing: 'bad', dead: 'bad dim', stub: 'dim', todo: 'dim', done: 'ok' };
    var body = rows.map(function (r, ri) {
      var names = r[0] === 'layers' ? F.LAYERS : F.SCREENS;
      return h('div', { class: 'vz-box' }, h('span', { class: 'vz-h', text: T('ft.row.' + r[0]) }),
        h('div', null, r[1].map(function (st, k) {
          var changed = prev && prev[ri] && prev[ri][1][k] !== st;
          return h('span', { class: 'vz-chip ' + (CLS[st] || '') + (changed ? ' hl' : '') }, T('ft.item.' + names[k]) + ': ' + T('ft.st.' + st));
        })));
    });
    box.appendChild(h('div', { class: 'vz' }, h('p', { class: 'vz-cap', text: T('ft.cap.' + (c === 'newfeature' ? 'layers' : 'screens')) }), h('div', null, body),
      h('div', { class: 'vz-legend', text: T('ft.legend') })));
  }, { labelKey: K + 'tab.ft', icon: 'grid' });
})();
