// Quét điều khiển "chết": với mỗi model rời rạc, mỗi điều khiển toggle/select, và MỌI tổ hợp giá trị của các điều khiển khác,
// đổi giá trị điều khiển đó có làm đổi danh sách bước không. Chạy: node dev/tools/cdp.js "<index.html>" --eval "$(cat dev/tools/controls-sweep.js)"
// Tham số tuỳ chọn: window.__TRACK = '<id>' để chỉ quét một track.
(() => {
  const out = [];
  Object.keys(ADE.models).forEach(mid => {
    if (window.__TRACK && mid.indexOf(window.__TRACK + '.') !== 0) return;
    const def = ADE.models[mid];
    if (def.kind !== 'discrete' || !def.controls) return;
    const cs = def.controls.filter(c => c.type === 'toggle' || c.type === 'select');
    const vals = c => c.type === 'toggle' ? [false, true] : c.options.map(o => o.value);
    const sig = st => JSON.stringify(def.steps(st));
    const build = combo => { let st = def.init(); cs.forEach((c, i) => { st = def.act(st, c.action, combo[i]); }); return st; };
    // tích Descartes
    let combos = [[]];
    cs.forEach(c => { const n = []; combos.forEach(p => vals(c).forEach(v => n.push(p.concat([v])))); combos = n; });
    cs.forEach((c, ci) => {
      const dead = {};
      combos.forEach(combo => {
        const base = sig(build(combo)), other = vals(c).filter(v => v !== combo[ci]);
        const changed = other.some(v => { const cb = combo.slice(); cb[ci] = v; return sig(build(cb)) !== base; });
        if (!changed) { const k = cs.map((x, i) => i === ci ? null : x.id + '=' + combo[i]).filter(Boolean).join(','); dead[k] = 1; }
      });
      const ks = Object.keys(dead);
      if (ks.length) out.push(mid + ' · ' + c.id + ' không đổi gì khi: ' + ks.join(' | '));
    });
  });
  return out.length ? out.join('\n') : 'OK: không có điều khiển chết';
})()
