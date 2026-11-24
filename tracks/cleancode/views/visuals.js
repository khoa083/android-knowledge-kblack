/* Hình trực quan theo bước của track J (ADE.registerScreen với nhãn tab riêng). Sơ đồ node vẫn ở tab bên cạnh. */
(function () {
  'use strict';
  var K = 'track.cleancode.vz.';
  var T = function (k, p) { return ADE.t(K + k, p); };
  var KS = ['s1', 's2', 's3', 's4'], uidN = 0;
  var esc = function (x) { return String(x).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;'); };
  function fitText(str, w) { return String(str).length * 6.6 > w ? ' textLength="' + w + '" lengthAdjust="spacingAndGlyphs"' : ''; }
  function idx(ctx) {
    if (ctx.step) return KS.indexOf(ctx.step.id.split('.').pop());
    return ctx.pos > ctx.N ? 3 : 0;
  }

  /* ---------- J1: hai hàng ô "bộ nhớ làm việc" (đường đi, biến) với vạch ngưỡng 7; bảng đếm cyclomatic complexity ----------
     Hàng ô phẳng, không lồng hộp. Mỗi ô có data-k: khi đổi hàm, ô cùng tên TRƯỢT tới chỗ mới (ui.labMotion, FLIP);
     ô mới hiện dần một lần; không có chuyển động lặp. */
  ADE.registerScreen('cleancode.fits', function (box, ctx) {
    var h = ADE.ui.h, J = ADE.ccFits, c = ctx.state.case, i = Math.max(0, idx(ctx)), v = J.view(c, i);
    // hàng trên: đúng 7 ô (ngưỡng); hàng dưới chỉ có khi vượt: nhãn "vượt ngưỡng 7" rồi các ô đỏ
    function chip(it, over) {
      if (!it) return h('span', { class: 'vz-chip dim vz-slot', 'aria-hidden': 'true', text: T('fits.empty') });
      return h('span', { class: 'vz-chip vz-slot' + (over ? ' bad' : '') + (it.fresh ? ' hl' : ''), 'data-k': it.k }, h('span', { text: it.text }), it.sub ? h('small', { text: it.sub }) : null);
    }
    function slotRow(label, items) {
      var inside = [], extra = items.slice(J.LIMIT);
      for (var x = 0; x < J.LIMIT; x++) inside.push(chip(items[x], false));
      return h('div', { class: 'vz-slotrow' }, h('div', { class: 'vz-slot-l' + (extra.length ? ' bad' : ''), text: label }), h('div', { class: 'vz-slots' }, inside),
        extra.length ? h('div', { class: 'vz-slots' }, [h('span', { class: 'vz-limit', text: T('fits.limit') })].concat(extra.map(function (it) { return chip(it, true); }))) : null);
    }
    var pathItems = [{ k: 'p-start', text: T('fits.start') }].concat(v.br.map(function (b) { return { k: 'p' + b[0], text: 'L' + b[0] + ' ' + b[1], fresh: v.isNew(b[0]) }; }));
    var varItems = v.vars.map(function (x) { return { k: 'v-' + x[0], text: x[0], sub: T('fits.kind.' + x[1]), fresh: v.isNew(x[2]) }; });
    var overLines = v.lines > J.SEEMANN_LINES;

    // bảng đếm: mỗi hàm bắt đầu từ 1, mỗi if/for cộng 1; hàng mới (vừa đọc) có viền
    var tb = h('tbody');
    J.tableFns(c, i).forEach(function (f) {
      var fn = J.FN[f], cur = f === v.step.f, upTo = cur ? v.step.upTo : fn.to, sum = 1;
      tb.appendChild(h('tr', { 'data-k': 'r-' + fn.name + '-start' }, h('td', { text: fn.name }), h('td', { class: 'c dim', text: String(fn.from) }), h('td', { class: 'dim', text: T('fits.what.start') }), h('td', { class: 'c', text: '1' })));
      fn.br.filter(function (b) { return b[0] <= upTo; }).forEach(function (b) {
        sum++;
        var fresh = cur && v.isNew(b[0]);
        tb.appendChild(h('tr', { 'data-k': 'r-' + fn.name + '-' + b[1] + '-' + sum }, h('td', { 'aria-label': fn.name }), h('td', { class: 'c' + (fresh ? ' hl' : ''), text: String(b[0]) }),
          h('td', { class: fresh ? 'hl' : null, text: T('fits.what.' + b[1]) }), h('td', { class: 'c' + (sum > J.LIMIT ? ' bad' : (fresh ? ' hl' : '')), text: String(sum) })));
      });
    });
    var head = h('tr', null, ['fn', 'line', 'what', 'sum'].map(function (k) { return h('th', { text: T('fits.col.' + k) }); }));

    var out = [h('p', { class: 'vz-cap', text: T('fits.cap', { fn: v.fn.name }) }),
      slotRow(T('fits.row.paths', { n: v.paths }), pathItems),
      slotRow(T('fits.row.vars', { n: v.nVars }), varItems),
      h('p', { class: 'vz-note' + (overLines ? ' bad' : ''), text: T('fits.lines', { n: v.lines, verdict: T(overLines ? 'fits.lines.over' : 'fits.lines.ok') }) })];
    if (i === 3) out.push(h('p', { class: 'vz-note ' + (v.step.skip ? 'bad' : 'ok'), text: T(v.step.skip ? 'fits.skipped' : 'fits.kept', { line: v.fn.remind || J.FN.book.remind }) }));
    out.push(h('p', { class: 'vz-cap', text: T('fits.tcap') }), h('div', { class: 'vz-scroll' }, h('table', { class: 'vz-table' }, h('thead', null, head), tb)),
      h('div', { class: 'vz-legend', text: T('fits.legend') }));
    box.appendChild(h('div', { class: 'vz' }, out));
  }, { labelKey: K + 'tab.fits', icon: 'grid' });

  /* ---------- J2: bảng đối chiếu (chữ ký che tên → đoán → tên → việc thật → đọc hay ghi), cột mở dần theo bước;
     bước 4 thêm bảng hai lần gọi khi mất mạng. Hàng có data-k; cột mới mở hiện dần một lần. ---------- */
  ADE.registerScreen('cleancode.names', function (box, ctx) {
    var h = ADE.ui.h, J = ADE.ccNames, c = ctx.state.case, i = Math.max(0, idx(ctx));
    var cols = ['sig', 'guess', 'name', 'does', 'kind'], open = [1, 1, i >= 1, i >= 2, i >= 2], fresh = [i === 0, i === 0, i === 1, i === 2, i === 2];
    var head = h('tr', null, cols.map(function (k, n) { return h('th', { class: fresh[n] && i > 0 ? 'hl' : null, text: T('nm.col.' + k) }); }));
    var tb = h('tbody');
    J.ROWS[c].forEach(function (r) {
      var ok = J.right(r), kindKey = r[5];
      var cell = function (n, text, extra) { return h('td', { class: !open[n] ? 'dim c' : (extra || (fresh[n] && i > 0 ? 'hl' : null)), text: open[n] ? text : '?' }); };
      tb.appendChild(h('tr', { 'data-k': 'nm-' + r[0] },
        h('td', null, h('code', { text: r[1] })),
        cell(1, T('nm.g.' + r[2]), i >= 2 && !ok ? 'bad' : null),
        cell(2, r[3], null),
        cell(3, T('nm.d.' + r[4]), i >= 2 && !ok ? 'bad' : null),
        cell(4, T('nm.k.' + kindKey), i >= 2 ? (ok ? 'ok' : 'bad') : null)));
    });
    var out = [h('p', { class: 'vz-cap', text: T('nm.cap') }), h('div', { class: 'vz-scroll' }, h('table', { class: 'vz-table' }, h('thead', null, head), tb))];
    if (i === 3) {
      var cb = h('tbody');
      J.CALLS[c].forEach(function (x, n) {
        cb.appendChild(h('tr', { 'data-k': 'call' + n }, h('td', { text: T('nm.call.' + (n + 1)) }), h('td', { class: 'c ' + (x[0] === 0 ? 'bad' : 'ok'), text: T('nm.ret', { n: x[0] }) }), h('td', { class: 'c' + (x[1] === 0 ? ' bad' : ''), text: T('nm.cacheN', { n: x[1] }) })));
      });
      out.push(h('p', { class: 'vz-cap', text: T('nm.tcap') }), h('div', { class: 'vz-scroll' }, h('table', { class: 'vz-table' }, h('thead', null, h('tr', null, ['call', 'ret', 'cache'].map(function (k) { return h('th', { text: T('nm.tcol.' + k) }); }))), cb)));
    }
    out.push(h('div', { class: 'vz-legend', text: T('nm.legend') }));
    box.appendChild(h('div', { class: 'vz' }, out));
  }, { labelKey: K + 'tab.names', icon: 'list' });

  /* ---------- J3: dòng chảy phẳng thô → ranh giới → bên trong → gửi SMS (bảng, mỗi hàng một số điện thoại).
     Không lồng hộp: các chặng là cột đặt cạnh nhau, cột mở dần theo bước; số sai đi tiếp có gạch đỏ. ---------- */
  ADE.registerScreen('cleancode.parse', function (box, ctx) {
    var h = ADE.ui.h, P = ADE.ccParse, c = ctx.state.case, i = Math.max(0, idx(ctx));
    var cols = ['raw', 'edge', 'inside', 'sms'];
    var head = h('tr', null, cols.map(function (k, n) { return h('th', { class: n === i && i > 0 ? 'hl' : null, text: (n ? '→ ' : '') + T('ps.col.' + k) }); }));
    var tb = h('tbody');
    P.rows(c).forEach(function (r) {
      var cell = function (n, key, cls, extra) {
        if (n > i) return h('td', { class: 'dim c', text: '?' });
        return h('td', { class: cls || null }, h('span', { text: T('ps.v.' + key) }), extra ? h('small', { class: 'vz-sub', text: extra }) : null);
      };
      var leak = r.badLeak ? 'bad' : null;
      tb.appendChild(h('tr', { 'data-k': 'ps-' + r.from },
        h('td', null, h('code', { text: '"' + r.raw + '"' }), h('small', { class: 'vz-sub', text: T('ps.from.' + r.from) })),
        cell(1, r.edge, r.edge === 'parsed' ? 'ok' : (r.edge === 'rejected' ? 'hl' : leak), r.value ? '("' + r.value + '")' : null),
        cell(2, r.inside, r.inside === 'typed' ? 'ok' : (r.inside === 'stopped' ? 'dim' : leak)),
        cell(3, r.sms, r.sms === 'sent' ? 'ok' : (r.sms === 'failed' ? 'bad' : 'dim'))));
    });
    var nRules = i === 0 ? 0 : (c === 'validate' ? (i < 3 ? 3 : 4) : 1);
    box.appendChild(h('div', { class: 'vz' }, h('p', { class: 'vz-cap', text: T('ps.cap') }),
      h('div', { class: 'vz-scroll' }, h('table', { class: 'vz-table' }, h('thead', null, head), tb)),
      h('p', { class: 'vz-note' + (nRules > 1 ? ' bad' : (nRules === 1 ? ' ok' : '')), text: T('ps.rules', { n: nRules }) }),
      h('div', { class: 'vz-legend', text: T('ps.legend') })));
  }, { labelKey: K + 'tab.parse', icon: 'rail' });

  /* ---------- J4: vòng ba pha (SVG: đỏ, xanh, refactor; pha cuối của bước sáng, đổi bằng chuyển cảnh lớp) + bảng danh sách test.
     Không có chuyển động lặp: vòng chỉ đổi khi bước đổi. ---------- */
  ADE.registerScreen('cleancode.tdd', function (box, ctx) {
    var h = ADE.ui.h, D = ADE.ccTdd, c = ctx.state.case, i = Math.max(0, idx(ctx)), p = D.PLAN[c][i];
    var PH = ['red', 'green', 'refactor'], last = p.walk[p.walk.length - 1], R = 58, CX = 90, CY = 84;
    function arc(a0, a1) { var r = function (a) { return (a - 90) * Math.PI / 180; }; var x0 = CX + R * Math.cos(r(a0)), y0 = CY + R * Math.sin(r(a0)), x1 = CX + R * Math.cos(r(a1)), y1 = CY + R * Math.sin(r(a1));
      return 'M' + x0.toFixed(1) + ' ' + y0.toFixed(1) + ' A' + R + ' ' + R + ' 0 0 1 ' + x1.toFixed(1) + ' ' + y1.toFixed(1); }
    var svg = '<svg class="vz-ring" viewBox="0 0 180 176" role="img" aria-label="' + esc(T('td.aria', { ph: PH.indexOf(last) >= 0 ? T('td.ph.' + last) : '—' })) + '">';
    PH.forEach(function (ph, n) {
      var on = ph === last, walked = p.walk.indexOf(ph) >= 0, a0 = n * 120 + 4, a1 = n * 120 + 116, mid = (n * 120 + 60 - 90) * Math.PI / 180;
      svg += '<path class="vz-ring-seg ' + ph + (on ? ' on' : (walked ? ' walk' : '')) + '" d="' + arc(a0, a1) + '"/>';
      svg += '<text class="vz-ring-t' + (on ? ' on' : '') + '" x="' + (CX + (R + 0) * Math.cos(mid)).toFixed(1) + '" y="' + (CY + 4 + (R + 0) * Math.sin(mid)).toFixed(1) + '">' + esc(T('td.ph.' + ph)) + '</text>';
    });
    svg += '<text class="vz-ring-c" x="' + CX + '" y="' + (CY + 5) + '">' + esc(c === 'tdd' ? '#' + (i + 1) : '—') + '</text></svg>';
    var walkTxt = p.walk[0] === 'code' ? T('td.walk.code') : (p.walk[0] === 'prod' ? T('td.walk.prod') : T('td.walk', { path: p.walk.map(function (x) { return T('td.ph.' + x); }).join(' → ') }));
    var money = function (v) { return T('td.money', { v: (v * 1000).toLocaleString(ADE.lang === 'vi' ? 'de-DE' : 'en-US') }); };
    var tb = h('tbody');
    D.rows(c, i).forEach(function (r) {
      var now = r.prod ? T('td.st.prod', { v: money(r.got) }) : (r.written ? T('td.st.' + (r.pass ? 'pass' : 'fail')) : T('td.st.none'));
      var cls = r.prod && !r.pass ? 'bad' : (!r.written ? 'dim' : (r.pass ? 'ok' : 'bad'));
      tb.appendChild(h('tr', { 'data-k': 'td-' + r.k }, h('td', { class: r.fresh ? 'hl' : null, text: T('td.ex.' + r.k) }), h('td', { class: 'c', text: money(r.want) }),
        h('td', { class: 'c ' + cls, text: now }), h('td', { class: 'c ' + (!r.written ? 'dim' : (r.seen ? 'ok' : 'bad')), text: !r.written ? '—' : T(r.seen ? 'td.yes' : 'td.no') })));
    });
    box.appendChild(h('div', { class: 'vz' }, h('p', { class: 'vz-cap', text: T('td.cap') }),
      h('div', { class: 'vz-ringrow' }, h('div', { html: svg }), h('p', { class: 'vz-note' + (p.walk[0] === 'prod' ? ' bad' : ''), text: walkTxt })),
      h('p', { class: 'vz-cap', text: T('td.tcap') }),
      h('div', { class: 'vz-scroll' }, h('table', { class: 'vz-table' }, h('thead', null, h('tr', null, ['ex', 'want', 'now', 'seen'].map(function (k) { return h('th', { text: T('td.col.' + k) }); }))), tb)),
      h('div', { class: 'vz-legend', text: T('td.legend') })));
  }, { labelKey: K + 'tab.tdd', icon: 'refresh' });

  /* ---------- J5: đồ thị phụ thuộc test → mã (SVG, hai cột phẳng, không lồng hộp) + bảng từng test qua bốn bước.
     Cạnh nối vào thứ vừa đổi chuyển đỏ (đổi lớp → chuyển cảnh một lần); thứ đổi có khung đỏ. ---------- */
  ADE.registerScreen('cleancode.testDesign', function (box, ctx) {
    var h = ADE.ui.h, D = ADE.ccTestDesign, c = ctx.state.case, i = Math.max(0, idx(ctx));
    var broken = D.brokenAt(c, i), bug = i === D.BUG_STEP, caught = bug ? D.caught(c) : [], chg = D.CHANGE[i];
    var LX = 8, LW = 168, RX = 392, RW = 200, ty = function (n) { return 22 + n * 58; }, ny = function (n) { return 8 + n * 34; };
    var svg = '<svg class="vz-dg" viewBox="0 0 600 248" role="img" aria-label="' + esc(T('tg.aria', { e: D.edgeCount(c), b: broken.length })) + '">';
    D.TESTS.forEach(function (t, a) {
      D.EDGES[c][t].forEach(function (n) {
        var b = D.NODES.map(function (x) { return x[0]; }).indexOf(n), isBad = broken.indexOf(t) >= 0 && chg.indexOf(n) >= 0;
        svg += '<line class="vz-dg-e' + (isBad ? ' bad' : '') + '" data-k="e-' + t + '-' + n + '" x1="' + (LX + LW) + '" y1="' + (ty(a) + 15) + '" x2="' + RX + '" y2="' + (ny(b) + 13) + '"/>';
      });
    });
    D.TESTS.forEach(function (t, a) {
      var st = broken.indexOf(t) >= 0 ? ' bad' : (bug ? (caught.indexOf(t) >= 0 ? ' ok' : (t === 't2' ? ' bad' : '')) : '');
      var lb = T('tg.t.' + t);
      svg += '<g class="vz-dg-n' + st + '"><rect x="' + LX + '" y="' + ty(a) + '" width="' + LW + '" height="30" rx="4"/><text class="vz-dg-t" x="' + (LX + 8) + '" y="' + (ty(a) + 20) + '"' + fitText(lb, LW - 16) + '>' + esc(lb) + '</text></g>';
    });
    D.NODES.forEach(function (nd, b) {
      var used = D.TESTS.some(function (t) { return D.EDGES[c][t].indexOf(nd[0]) >= 0; }), changed = chg.indexOf(nd[0]) >= 0 && (nd[1] === 'int' || (nd[0] === 'FakeRepo' && D.fakeEdits(c, i)));
      var cls = changed ? ' bad' : (used ? '' : ' skip');
      svg += '<g class="vz-dg-n' + cls + '"><rect x="' + RX + '" y="' + ny(b) + '" width="' + RW + '" height="26" rx="4"/><text class="vz-dg-t" x="' + (RX + 8) + '" y="' + (ny(b) + 17) + '">' + esc(nd[0]) + '</text><text class="vz-dg-s" x="' + (RX + RW - 6) + '" y="' + (ny(b) + 17) + '" text-anchor="end">' + esc(T('tg.' + nd[1])) + '</text></g>';
    });
    svg += '</svg>';
    var stCell = function (t, col) {
      if (col > i) return h('td', { class: 'c dim', text: T('tg.st.na') });
      if (col === D.BUG_STEP) { var ok = caught.indexOf(t) >= 0; if (t !== 't2') return h('td', { class: 'c', text: T('tg.st.ok') }); return h('td', { class: 'c ' + (ok ? 'ok' : 'bad'), text: T(ok ? 'tg.st.caught' : 'tg.st.missed') }); }
      var b = D.brokenAt(c, col).indexOf(t) >= 0; return h('td', { class: 'c' + (b ? ' bad' : ''), text: T(b ? 'tg.st.broke' : 'tg.st.ok') });
    };
    var tb = h('tbody');
    D.TESTS.forEach(function (t) {
      tb.appendChild(h('tr', { 'data-k': 'tg-' + t }, h('td', { text: T('tg.t.' + t) }), h('td', { class: 'c', text: String(D.EDGES[c][t].length) }), stCell(t, 1), stCell(t, 2), stCell(t, 3)));
    });
    box.appendChild(h('div', { class: 'vz' }, h('p', { class: 'vz-cap', text: T('tg.cap') }), h('div', { class: 'vz-scroll', html: svg }),
      h('p', { class: 'vz-cap', text: T('tg.tcap') }),
      h('div', { class: 'vz-scroll' }, h('table', { class: 'vz-table' }, h('thead', null, h('tr', null, ['test', 'deps', 'a', 'b', 'bug'].map(function (k, n) { return h('th', { class: n >= 2 && n - 1 === i ? 'hl' : null, text: T('tg.col.' + k) }); }))), tb)),
      h('div', { class: 'vz-legend', text: T('tg.legend') })));
  }, { labelKey: K + 'tab.testDesign', icon: 'layers' });

  /* ---------- J6: dãy ô commit (bảng phẳng: mỗi cột một thay đổi, hàng test và hàng commit) + dòng trạng thái biên dịch/test ---------- */
  ADE.registerScreen('cleancode.refactor', function (box, ctx) {
    var h = ADE.ui.h, R = ADE.ccRefactor, c = ctx.state.case, i = Math.max(0, idx(ctx)), now = R.CELLS[c][i], fr = R.fresh(c, i);
    var num = function (k) { return k === 'c4b' ? '4′' : k.slice(1); };
    var head = h('tr', null, [h('th', null)].concat(R.COLS[c].map(function (k) { return h('th', { class: 'c' + (fr.indexOf(k) >= 0 ? ' hl' : ''), title: T('rf.c.' + k), text: num(k) }); })));
    var cell = function (k, part) {
      var v = now[k]; if (!v) return h('td', { class: 'c dim', 'data-k': 'rf-' + part + k, text: T('rf.st.none') });
      var st = v[part], cls = part === 0 ? (st === 'green' ? 'ok' : (st === 'gone' ? 'dim' : 'bad')) : (st === 'yes' ? 'ok' : (st === 'undo' ? 'bad' : 'dim'));
      return h('td', { class: 'c ' + cls, 'data-k': 'rf-' + part + k, text: T('rf.st.' + st) });
    };
    var tb = h('tbody', null, h('tr', null, [h('th', { text: T('rf.row.test') })].concat(R.COLS[c].map(function (k) { return cell(k, 0); }))),
      h('tr', null, [h('th', { text: T('rf.row.commit') })].concat(R.COLS[c].map(function (k) { return cell(k, 1); }))));
    var b = R.BUILD[c][i], red = R.RED[c][i], sus = R.suspects(c, i);
    var status = T('rf.status', { b: b ? T('rf.build.err', { n: b }) : T('rf.build.ok'), r: red == null ? '?' : red, s: sus });
    var names = R.COLS[c].map(function (k) { return num(k) + ' ' + T('rf.c.' + k); }).join(' · ');
    box.appendChild(h('div', { class: 'vz' }, h('p', { class: 'vz-cap', text: T('rf.cap') }),
      h('div', { class: 'vz-scroll' }, h('table', { class: 'vz-table vz-cells' }, h('thead', null, head), tb)),
      h('p', { class: 'vz-note', text: names }),
      h('p', { class: 'vz-note' + (b || sus || red ? ' bad' : ' ok'), text: status }),
      h('div', { class: 'vz-legend', text: T('rf.legend') })));
  }, { labelKey: K + 'tab.refactor', icon: 'grid' });

  /* ---------- J7: dãy 200 commit (lưới phẳng 20 × 10; ô đổi lớp khi bị loại → nháy một lần) + bảng các lần thử của bước ---------- */
  ADE.registerScreen('cleancode.bisect', function (box, ctx) {
    var h = ADE.ui.h, B = ADE.ccBisect, c = ctx.state.case, i = Math.max(0, idx(ctx)), st = B.state(c, i);
    var probed = {}; st.fresh.forEach(function (p) { probed[p[0]] = true; });
    var cells = [];
    for (var k = 1; k <= B.N; k++) {
      var cls = 'vz-cm' + (st.found === k ? ' cul' : (k <= st.lo ? ' g' : (k > st.hi ? ' x' : (st.found === null && k === st.hi && st.probes ? '' : '')))) + (probed[k] ? ' p' : '');
      cells.push(h('span', { class: cls, title: String(k) }, (k % 20 === 1 || probed[k] || st.found === k) ? String(k) : ''));
    }
    var tb = h('tbody'), rows = st.fresh, more = 0;
    if (rows.length > 6) { more = rows.length - 6; rows = rows.slice(-6); }
    if (more) tb.appendChild(h('tr', null, h('td', { class: 'dim', colspan: '4', text: T('bs.more', { n: more }) })));
    rows.forEach(function (p) {
      var n = st.all.indexOf(p) + 1;
      tb.appendChild(h('tr', { 'data-k': 'bs-' + p[0] }, h('td', { class: 'c', text: String(n) }), h('td', { class: 'c', text: String(p[0]) }), h('td', { class: 'c ' + (p[1] ? 'bad' : 'ok'), text: T(p[1] ? 'bs.bad' : 'bs.good') }),
        h('td', { class: 'c' + (p[3] - p[2] === 1 ? ' hl' : ''), text: p[3] - p[2] === 1 ? T('bs.found', { c: p[3] }) : T('bs.range', { a: p[2] + 1, b: p[3], n: p[3] - p[2] }) })));
    });
    var out = [h('p', { class: 'vz-cap', text: T('bs.cap') }),
      h('div', { class: 'vz-commits', role: 'img', 'aria-label': T('bs.aria', { n: st.found ? 1 : st.left, p: st.probes }) }, cells),
      h('p', { class: 'vz-note', text: T('bs.math') })];
    if (i === 0) out.push(h('p', { class: 'vz-note ok', text: T('bs.repro') }));
    else out.push(h('p', { class: 'vz-cap', text: T('bs.tcap') }), h('div', { class: 'vz-scroll' }, h('table', { class: 'vz-table' }, h('thead', null, h('tr', null, ['n', 'commit', 'res', 'range'].map(function (q) { return h('th', { text: T('bs.col.' + q) }); }))), tb)));
    out.push(h('div', { class: 'vz-legend', text: T('bs.legend') }));
    box.appendChild(h('div', { class: 'vz' }, out));
  }, { labelKey: K + 'tab.bisect', icon: 'grid' });

  /* ---------- J8: ma trận nguyên lý × (phát biểu, triệu chứng, ở thiết kế này), hàng mở dần; bước 4 thêm đồ thị phụ thuộc (SVG) cho thấy
     mũi tên giữa nghiệp vụ và chi tiết đổi chiều. Bảng phẳng, đồ thị hai tầng phẳng. ---------- */
  ADE.registerScreen('cleancode.solid', function (box, ctx) {
    var h = ADE.ui.h, D = ADE.ccSolid, c = ctx.state.case, i = Math.max(0, idx(ctx)), open = D.openRows(i), fresh = D.STEP_ROWS[i];
    var tb = h('tbody');
    D.ROWS.forEach(function (p) {
      var on = open.indexOf(p) >= 0, fr = fresh.indexOf(p) >= 0;
      tb.appendChild(h('tr', { 'data-k': 'sd-' + p }, h('th', { class: fr ? 'hl' : (on ? null : 'dim'), text: p.toUpperCase() }),
        h('td', { class: on ? null : 'dim', text: on ? T('sd.says.' + p) : '?' }), h('td', { class: on ? null : 'dim', text: on ? T('sd.sym.' + p) : '?' }),
        h('td', { class: on ? (c === 'switch' ? 'bad' : 'ok') : 'dim c', text: on ? T('sd.here.' + c + '.' + p) : '?' })));
    });
    var out = [h('p', { class: 'vz-cap', text: T('sd.cap') }),
      h('div', { class: 'vz-scroll' }, h('table', { class: 'vz-table' }, h('thead', null, h('tr', null, ['p', 'says', 'sym', 'here'].map(function (k) { return h('th', { text: T('sd.col.' + k) }); }))), tb))];
    if (i === 3) {
      var u = 'sdm' + (++uidN), P = { booking: [12, 52, 'BookingService'], port: [218, 8, 'PaymentGateway'], adapter: [218, 96, 'VnPayGateway'], sdk: [424, 52, 'VnPaySdkClient'] }, W = 164, H = 34;
      var used = {}; D.EDGES[c].forEach(function (e) { used[e[0]] = used[e[1]] = true; });
      var svg = '<svg class="vz-dg" viewBox="0 0 600 140" role="img" aria-label="' + esc(T('sd.aria', { d: D.EDGES[c].map(function (e) { return P[e[0]][2] + ' → ' + P[e[1]][2]; }).join(', ') })) + '"><defs>' +
        '<marker id="' + u + 'a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path class="vz-dg-head" d="M0,0 L10,5 L0,10 z"/></marker>' +
        '<marker id="' + u + 'b" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path class="vz-dg-head bad" d="M0,0 L10,5 L0,10 z"/></marker></defs>';
      D.EDGES[c].forEach(function (e) {
        var a = P[e[0]], b = P[e[1]], bd = D.POLICY.indexOf(e[0]) >= 0 && D.POLICY.indexOf(e[1]) < 0;
        var x1 = a[0] + (b[0] > a[0] ? W : (b[0] < a[0] ? 0 : W / 2)), y1 = a[1] + (b[0] === a[0] ? (b[1] > a[1] ? H : 0) : H / 2);
        var x2 = b[0] + (b[0] > a[0] ? 0 : (b[0] < a[0] ? W : W / 2)), y2 = b[1] + (b[0] === a[0] ? (b[1] > a[1] ? 0 : H) : H / 2);
        svg += '<line class="vz-dg-e' + (bd ? ' bad' : ' up') + '" data-k="' + e[0] + '-' + e[1] + '" x1="' + x1 + '" y1="' + y1 + '" x2="' + x2 + '" y2="' + y2 + '" marker-end="url(#' + u + (bd ? 'b' : 'a') + ')"/>';
      });
      Object.keys(P).forEach(function (k) {
        var q = P[k], pol = D.POLICY.indexOf(k) >= 0;
        svg += '<g class="vz-dg-n' + (used[k] ? (c === 'switch' && k === 'booking' ? ' bad' : '') : ' skip') + '"><rect x="' + q[0] + '" y="' + q[1] + '" width="' + W + '" height="' + H + '" rx="4"/><text class="vz-dg-t" x="' + (q[0] + 8) + '" y="' + (q[1] + 15) + '">' + esc(q[2]) + '</text><text class="vz-dg-s" x="' + (q[0] + 8) + '" y="' + (q[1] + 28) + '">' + esc(T(pol ? 'sd.g.policy' : 'sd.g.detail')) + '</text></g>';
      });
      svg += '</svg>';
      out.push(h('p', { class: 'vz-cap', text: T('sd.gcap') }), h('div', { class: 'vz-scroll', html: svg }));
    }
    out.push(h('div', { class: 'vz-legend', text: T('sd.legend') }));
    box.appendChild(h('div', { class: 'vz' }, out));
  }, { labelKey: K + 'tab.solid', icon: 'grid' });
})();
