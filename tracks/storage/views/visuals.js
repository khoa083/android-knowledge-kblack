/* Hình trực quan theo bước của track H (ADE.registerScreen với nhãn tab riêng). Sơ đồ node vẫn ở tab bên cạnh.
   H1: CÂY QUYẾT ĐỊNH dạng bậc thang (mỗi câu "có" rẽ sang một lá, "không" đi xuống câu tiếp), kèm bảng thuộc tính năm nơi lưu.
   Câu hỏi, câu trả lời và thuộc tính lấy từ ADE.storageChoose (models.js), không tính lại ở đây. */
(function () {
  'use strict';
  var K = 'track.storage.vz.', MC = 'track.storage.m.choose.';
  var T = function (k, p) { return ADE.t(K + k, p); };
  function esc(s) { return ADE.esc(String(s)); }
  // chữ monospace 11px rộng khoảng 6.6px mỗi ký tự; nhãn dài hơn chỗ trống thì ép vừa thay vì tràn
  function fitText(str, w) { return String(str).length * 6.6 > w ? ' textLength="' + w + '" lengthAdjust="spacingAndGlyphs"' : ''; }
  // vị trí bước của H1, tính từ id bước (<loại>.start | <loại>.<câu hỏi> | <loại>.leaf); số bước thay đổi theo tình huống
  function chooseIdx(ctx, C, ans) {
    if (!ctx.step) return ctx.pos > ctx.N ? ans.length + 1 : 0;
    var k = ctx.step.id.split('.').pop();
    return k === 'start' ? 0 : k === 'leaf' ? ans.length + 1 : C.Q.indexOf(k) + 1;
  }

  /* ---------- H1: cây quyết định chọn nơi lưu ---------- */
  ADE.registerScreen('storage.choose', function (box, ctx) {
    var h = ADE.ui.h, C = ADE.storageChoose, c = ctx.state.data, ans = C.ANS[c], leaf = C.leafOf(ans);
    var i = chooseIdx(ctx, C, ans), last = ans.length + 1, answered = Math.min(i, ans.length), done = i >= last;
    var leafBox = function (p, on) {
      return h('div', { class: 'vz-box vz-dt-leaf' + (on ? ' hl' : '') }, h('div', { class: 'vz-h', text: ADE.t(MC + 'place.' + p) }),
        h('div', { class: on ? null : 'dim', text: T('dt.chapter', { ch: C.CH[p].toUpperCase() }) }));
    };
    var rows = [];
    C.Q.forEach(function (q, k) {
      var asked = k < answered, cur = k === answered - 1 && !done, yes = asked && ans[k] === 1, no = asked && ans[k] === 0;
      var past = k >= ans.length;   // câu hỏi sau lá đã chọn: không đi tới
      rows.push(h('div', { class: 'vz-dt-row' + (past && done ? ' off' : '') },
        h('div', { class: 'vz-box' + (cur ? ' hl' : '') }, h('div', { class: 'vz-h', text: T('dt.q', { n: k + 1 }) }), h('div', { text: ADE.t(MC + 'q.' + q) })),
        h('div', { class: 'vz-dt-arr' + (yes ? ' on' : ''), text: (yes ? '▸ ' : '') + T('dt.yes') + ' →' }),
        leafBox(C.YES[q], yes && done)));
      rows.push(h('div', { class: 'vz-dt-no' + (no ? ' on' : ''), text: (no ? '▾ ' : '↓ ') + T('dt.no') }));
    });
    rows.push(h('div', { class: 'vz-dt-row' + (done && leaf !== C.LAST ? ' off' : '') }, h('div', { class: 'vz-dt-end', text: T('dt.end') }), h('div', { class: 'vz-dt-arr' + (leaf === C.LAST && done ? ' on' : ''), text: '→' }),
      leafBox(C.LAST, leaf === C.LAST && done)));
    // bảng thuộc tính năm nơi lưu (theo bảng so sánh của trang Data and file storage overview)
    var head = h('tr', null, h('th', { text: T('pt.place') }), ['other', 'uninstall', 'sysdel'].map(function (k) { return h('th', { text: T('pt.' + k) }); }));
    var tb = h('tbody');
    C.PLACES.forEach(function (p) {
      var on = done && p === leaf;
      tb.appendChild(h('tr', null, h('td', { class: on ? 'hl' : null, text: ADE.t(MC + 'place.' + p) }),
        C.PROPS[p].map(function (v, k) {
          var txt = T('pt.v.' + ['other', 'uninstall', 'sysdel'][k] + '.' + v);
          return h('td', { class: on ? 'hl' : (v === 'yes' ? 'ok' : null), text: txt });
        })));
    });
    box.appendChild(h('div', { class: 'vz' }, h('p', { class: 'vz-cap', text: T('dt.cap') }), h('div', { class: 'vz-dt' }, rows),
      h('p', { class: 'vz-cap', text: T('pt.cap') }), h('div', { class: 'vz-scroll' }, h('table', { class: 'vz-table' }, h('thead', null, head), tb)),
      h('div', { class: 'vz-legend', text: T('dt.legend') })));
  }, { labelKey: K + 'tab.dt', icon: 'diamond' });

  /* ---------- bảng làn thời gian: mỗi hàng là một làn, mỗi cột là một bước; chỉ cột của bước đang xem được viền ---------- */
  var KS = ['s1', 's2', 's3', 's4'];
  function idx(ctx) {
    if (ctx.step) return KS.indexOf(ctx.step.id.split('.').pop());
    return ctx.pos > ctx.N ? 3 : 0;
  }
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
          if (k < i && cls === 'hl') cls = '';
          tr.appendChild(h('td', { class: cls || null, text: T(p + '.cell.' + cell[0]) }));
        }
        tb.appendChild(tr);
      });
      box.appendChild(h('div', { class: 'vz' }, h('p', { class: 'vz-cap', text: T(p + '.cap') }),
        h('div', { class: 'vz-scroll' }, h('table', { class: 'vz-table vz-lanes' }, h('thead', null, head), tb)), h('div', { class: 'vz-legend', text: T(p + '.legend') })));
    }, { labelKey: K + tabKey, icon: 'clock' });
  }
  laneScreen('storage.file', function () { return ADE.storageFile; }, 'fl', 'tab.fl');   // H2: app, hệ thống, đĩa
  laneScreen('storage.prefs', function () { return ADE.storagePrefs; }, 'pf', 'tab.pf');  // H3: main thread, luồng IO, đĩa

  /* ---------- H4: dãy bốn tầng (DAO → mã sinh → SQLite → kết quả) và bảng "ghi vào bảng nào → truy vấn có chạy lại không" ---------- */
  ADE.registerScreen('storage.room', function (box, ctx) {
    var h = ADE.ui.h, R = ADE.storageRoom, c = ctx.state.case, i = idx(ctx), lit = R.lit(c, Math.max(0, i));
    var chain = h('div', { class: 'vz-legend' }, R.STAGES.map(function (st, k) {
      var on = lit.indexOf(st) >= 0;
      return h('span', null, h('span', { class: 'vz-chip' + (on ? ' hl' : ' dim'), text: T('rm.stage.' + st + (st === 'out' ? '.' + c : '')) }), k < R.STAGES.length - 1 ? ' → ' : '');
    }));
    var cols = ['write', 'table', 'rerun', 'changed', 'screen'];
    var head = h('tr', null, cols.map(function (k) { return h('th', { text: T('rm.col.' + k) }); }));
    var tb = h('tbody');
    R.WRITES.forEach(function (w, k) {
      var shown = k < i, cur = k === i - 1, v = R.W[c][w];
      if (!shown) { tb.appendChild(h('tr', null, cols.map(function (cc, j) { return h('td', { class: 'dim', text: j === 0 ? T('rm.w.' + w) : '·' }); }))); return; }
      var scr = v[2], scrCls = scr === 'stale' ? 'bad' : (scr === 'emitSame' ? 'bad' : (scr === 'emit' ? 'ok' : null));
      tb.appendChild(h('tr', null, h('td', { class: cur ? 'hl' : null, text: T('rm.w.' + w) }), h('td', { class: cur ? 'hl' : null, text: R.TABLE[w] }),
        h('td', { class: cur ? 'hl' : null, text: T('rm.yn.' + v[0]) }), h('td', { class: cur ? 'hl' : null, text: T('rm.yn.' + v[1]) }),
        h('td', { class: cur ? 'hl' : scrCls, text: T('rm.scr.' + scr) })));
    });
    box.appendChild(h('div', { class: 'vz' }, h('p', { class: 'vz-cap', text: T('rm.cap') }), chain,
      h('div', { class: 'vz-scroll' }, h('table', { class: 'vz-table' }, h('thead', null, head), tb)), h('div', { class: 'vz-legend', text: T('rm.legend') })));
  }, { labelKey: K + 'tab.rm', icon: 'grid' });

  /* ---------- H5: bảng appointment (dòng #7 đổi bác sĩ), kết quả ghép theo bác sĩ, bộ đếm truy vấn ---------- */
  ADE.registerScreen('storage.rel', function (box, ctx) {
    var h = ADE.ui.h, R = ADE.storageRel, c = ctx.state.case, i = idx(ctx), d = R.at(c, Math.max(0, i));
    var tb1 = h('tbody');
    Object.keys(R.BEFORE).forEach(function (id) {
      var doc = id === '7' && d.moved ? 'C' : R.BEFORE[id], ch = id === '7' && d.moved;
      tb1.appendChild(h('tr', null, h('td', { text: '#' + id }), h('td', { class: ch && i === 2 ? 'hl' : null, text: ch ? T('rl.moved', { from: 'B', to: 'C' }) : doc })));
    });
    var t1 = h('table', { class: 'vz-table' }, h('thead', null, h('tr', null, h('th', { text: 'id' }), h('th', { text: 'doctorId' }))), tb1);
    var seen = {}, tb2 = h('tbody');
    R.DOCS.forEach(function (doc) {
      var list = d.res[doc];
      tb2.appendChild(h('tr', null, h('td', { text: T('rl.doctor', { d: doc }) }), h('td', null, list ? list.map(function (id) {
        var dup = seen[id]; seen[id] = 1;
        return h('span', { class: 'vz-chip' + (dup ? ' bad' : ''), text: '#' + id + (dup ? ' ' + T('rl.dup') : '') });
      }) : h('span', { class: 'dim', text: T('rl.notyet') }))));
    });
    var t2 = h('table', { class: 'vz-table' }, h('thead', null, h('tr', null, h('th', { text: T('rl.col.doctor') }), h('th', { text: T('rl.col.appts') }))), tb2);
    var count = h('p', { class: 'vz-cap' }, h('b', { text: T('rl.q', { n: d.q }) }), ' ' + T('rl.formula.' + c));
    box.appendChild(h('div', { class: 'vz' }, h('p', { class: 'vz-cap', text: T('rl.cap') }),
      h('div', { class: 'vz-pair' }, h('div', null, h('p', { class: 'vz-cap', text: T('rl.t1') }), t1), h('div', null, h('p', { class: 'vz-cap', text: T('rl.t2') }), t2)),
      count, h('div', { class: 'vz-legend', text: T('rl.legend') })));
  }, { labelKey: K + 'tab.rl', icon: 'grid' });

  /* ---------- H6: dãy ô phiên bản schema v1 → v2 → v3; mỗi mũi tên là một migration có hay thiếu ---------- */
  ADE.registerScreen('storage.mig', function (box, ctx) {
    var h = ADE.ui.h, G = ADE.storageMig, c = ctx.state.case, i = idx(ctx), d = G.at(c, Math.max(0, i)), E = G.EDGES[c];
    var wiped = d.rows === 0;
    var row = h('div', { class: 'vz-mig' });
    [1, 2, 3].forEach(function (v, k) {
      var on = d.at === v, cls = 'vz-box vz-mig-v' + (on ? (wiped ? ' bad' : ' hl') : '');
      row.appendChild(h('div', { class: cls }, h('div', { class: 'vz-h', text: 'v' + v }), h('div', { text: T('mg.v' + v) }),
        h('div', { class: on ? null : 'dim', text: on ? T('mg.here', { n: d.rows }) : (v === 3 ? T('mg.target') : '·') })));
      if (k < 2) {
        var e = E[k], cur = d.edge === k;
        row.appendChild(h('div', { class: 'vz-mig-e ' + (e === 'missing' ? 'bad' : 'ok') + (cur ? ' cur' : '') }, h('span', { text: '→' }), h('span', { text: T('mg.e.' + e, { a: k + 1, b: k + 2 }) })));
      }
    });
    box.appendChild(h('div', { class: 'vz' }, h('p', { class: 'vz-cap', text: T('mg.cap') }), h('div', { class: 'vz-scroll' }, row),
      h('p', { class: 'vz-cap' }, h('b', { text: T('mg.status') + ' ' }), ADE.t('track.storage.m.mig.st.' + d.st)), h('div', { class: 'vz-legend', text: T('mg.legend') })));
  }, { labelKey: K + 'tab.mg', icon: 'grid' });

  /* ---------- H7: SƠ ĐỒ TUẦN TỰ (mới) — cột là các bên, hàng là tin nhắn theo thời gian; tin của bước đang xem được tô ----------
     Tin nhắn lấy từ ADE.storageSync (models.js). Tin tự gửi (từ = tới) vẽ thành vòng nhỏ bên phải đường đời. */
  var SQ_W = 600, SQ_COL = { app: 75, db: 225, wm: 375, server: 525 }, SQ_ROW = 34, SQ_TOP = 52;
  ADE.registerScreen('storage.sync', function (box, ctx) {
    var h = ADE.ui.h, Y = ADE.storageSync, c = ctx.state.case, i = idx(ctx);
    var uid = 'sq' + Math.random().toString(36).slice(2, 8), rows = [];
    for (var k = 0; k <= i; k++) Y.msgs(c, k).forEach(function (x) { rows.push({ x: x, cur: k === i, step: k }); });
    var H = SQ_TOP + Math.max(rows.length, 1) * SQ_ROW + 16;
    var svg = '<svg viewBox="0 0 ' + SQ_W + ' ' + H + '" class="vz-dg vz-sq" role="img" aria-label="' + esc(T('sq.cap')) + '"><title>' + esc(T('sq.cap')) + '</title><defs>' +
      ['n', 'c', 'b'].map(function (t) { return '<marker id="' + uid + t + '" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M1 1.5L9 5 1 8.5z" class="vz-sq-head ' + t + '"/></marker>'; }).join('') + '</defs>';
    Y.PARTS.forEach(function (p) {
      var x = SQ_COL[p];
      svg += '<line class="vz-sq-life" x1="' + x + '" y1="' + (SQ_TOP - 8) + '" x2="' + x + '" y2="' + (H - 6) + '"/>' +
        '<rect class="vz-sq-part" x="' + (x - 66) + '" y="6" width="132" height="30" rx="4"/><text class="vz-dg-t" x="' + x + '" y="26" text-anchor="middle"' + fitText(T('sq.p.' + p), 120) + '>' + esc(T('sq.p.' + p)) + '</text>';
    });
    rows.forEach(function (r, n) {
      var y = SQ_TOP + n * SQ_ROW + 20, a = SQ_COL[r.x[0]], b = SQ_COL[r.x[1]], bad = r.x[3] === 1, t = 'vz-sq-m' + (bad ? ' bad' : '') + (r.cur ? ' cur' : '');
      var mk = 'url(#' + uid + (bad ? 'b' : (r.cur ? 'c' : 'n')) + ')', label = esc(T('sq.m.' + r.x[2]));
      if (a === b) {
        svg += '<path class="' + t + '" d="M' + a + ' ' + (y - 10) + ' h 22 v 14 h -20" marker-end="' + mk + '"/>' +
          '<text class="vz-sq-l' + (bad ? ' bad' : '') + '" x="' + (a + 28) + '" y="' + (y + 1) + '"' + fitText(T('sq.m.' + r.x[2]), a > 450 ? 40 : 150 + (a < 100 ? 140 : 0)) + '>' + label + '</text>';
      } else {
        var dir = b > a ? 1 : -1, mid = (a + b) / 2, w = Math.abs(b - a) - 16;
        svg += '<line class="' + t + '" x1="' + (a + dir * 4) + '" y1="' + y + '" x2="' + (b - dir * 6) + '" y2="' + y + '" marker-end="' + mk + '"/>' +
          '<text class="vz-sq-l' + (bad ? ' bad' : '') + '" x="' + mid + '" y="' + (y - 6) + '" text-anchor="middle"' + fitText(T('sq.m.' + r.x[2]), w) + '>' + label + '</text>';
      }
    });
    svg += '</svg>';
    var q = Y.q(c, Math.max(0, i)), M7 = 'track.storage.m.sync.';
    var qt = h('table', { class: 'vz-table' }, h('thead', null, h('tr', null, ['appt', 'inDb', 'state', 'server'].map(function (k) { return h('th', { text: T('sq.qc.' + k) }); }))),
      h('tbody', null, h('tr', null, h('td', { text: '#9' }), h('td', { class: q[0] === 'no' ? 'bad' : 'ok', text: ADE.t(M7 + 'yn.' + q[0]) }),
        h('td', { class: q[1] === 'synced' ? 'ok' : (q[1] === 'none' ? 'dim' : null), text: ADE.t(M7 + 'q.' + q[1]) }),
        h('td', { class: q[2] === 'yes' ? 'ok' : null, text: ADE.t(M7 + 'yn.' + q[2]) }))));
    var holder = h('div', { class: 'vz-scroll' }); holder.innerHTML = svg;
    box.appendChild(h('div', { class: 'vz' }, h('p', { class: 'vz-cap', text: T('sq.cap') }), holder, h('p', { class: 'vz-cap', text: T('sq.qcap') }), h('div', { class: 'vz-scroll' }, qt),
      h('div', { class: 'vz-legend', text: T('sq.legend') })));
  }, { labelKey: K + 'tab.sq', icon: 'list' });

  /* ---------- H8: ma trận phiên bản Android × cách làm; cột đang chọn mở dần theo bước, ô đang xét có viền ---------- */
  ADE.registerScreen('storage.media', function (box, ctx) {
    var h = ADE.ui.h, D = ADE.storageMedia, c = ctx.state.case, i = idx(ctx), MM = 'track.storage.m.media.';
    var CLS = { ok: 'ok', perm: null, legacy: 'bad', slow: null, restricted: 'bad' };
    var head = h('tr', null, h('th', { text: T('md.ver') }), D.COLS.map(function (col) { return h('th', { class: col === c ? 'hl' : null, text: T('md.col.' + col) }); }));
    var tb = h('tbody');
    D.ROWS.forEach(function (r, k) {
      tb.appendChild(h('tr', null, h('th', { class: k === i ? 'hl' : null, text: ADE.t(MM + 'row.' + r) }), D.COLS.map(function (col) {
        var v = D.CELL[r][col], mine = col === c;
        if (mine && k > i) return h('td', { class: 'dim', text: '?' });
        return h('td', { class: mine && k === i ? 'hl' : (mine ? CLS[v] : 'dim'), text: ADE.t(MM + 'cell.' + v) });
      })));
    });
    box.appendChild(h('div', { class: 'vz' }, h('p', { class: 'vz-cap', text: T('md.cap') }), h('div', { class: 'vz-scroll' }, h('table', { class: 'vz-table' }, h('thead', null, head), tb)),
      h('div', { class: 'vz-legend', text: T('md.legend') })));
  }, { labelKey: K + 'tab.md', icon: 'grid' });
})();
