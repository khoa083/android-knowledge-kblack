// Kiểm một track trong trang (chạy bằng cdp.js --pre "window.__TRACK='<id>'" --eval "$(cat dev/tools/track-check.js)").
// Với mỗi chương, mỗi tab sim: đi qua mọi vị trí (0..N+1), thử mọi điều khiển sandbox, đổi ngôn ngữ giữa chừng.
// Báo: khoá lộ ra màn hình (track.*), cuộn ngang, điều khiển không đổi gì, đổi ngôn ngữ làm mất route/bước.
(async () => {
  const wait = ms => new Promise(r => setTimeout(r, ms)), out = [], bad = [];
  const tid = window.__TRACK, t = ADE.getTrack(tid);
  if (!t) return 'NO TRACK ' + tid;
  const leak = () => { const m = document.getElementById('main').innerText.match(/\btrack\.[a-z0-9]+\.[\w.]+/g); return m ? [...new Set(m)].slice(0, 5).join(' ') : ''; };
  const ovf = () => { const d = document.documentElement; return d.scrollWidth > d.clientWidth + 1; };
  const sig = () => { const s = document.getElementById('main'); return (s ? s.innerText : '').length + ':' + (s ? s.innerText : '').slice(-400); };
  const lang = () => location.hash.split('/')[1];
  for (const c of t.chapters) {
    const nSims = Math.max(1, c.sims.length);
    for (let k = 0; k < nSims; k++) {
      location.hash = '#/' + lang() + '/' + tid + '/' + c.id + '/1'; await wait(250);
      if (k > 0) { const tabs = [...document.querySelectorAll('#main [role=tablist]')[0].querySelectorAll('[role=tab]')]; if (tabs[k]) { tabs[k].click(); await wait(250); } }
      // đổi tab bỏ số bước trên URL (app.js): tab mới mở ở trang tổng quan → bấm "Bắt đầu"
      { const st = document.querySelector('[data-fk=start]'); if (st && !document.querySelector('[data-fk=nav-next]')) { st.click(); await wait(150); } }
      const nextBtn = () => document.querySelector('[data-fk=nav-next]');
      let pos = 1, guard = 0, maxN = 0;
      while (nextBtn() && !nextBtn().disabled && guard++ < 200) {
        nextBtn().click(); await wait(40); pos++;
        const l = leak(); if (l) bad.push(c.id + '#' + k + ' pos' + pos + ' leak ' + l);
        if (ovf() && window.innerWidth <= 400) bad.push(c.id + '#' + k + ' pos' + pos + ' overflowX');
      }
      maxN = pos;
      const isCompute = ADE.models[c.sims[k]] && ADE.models[c.sims[k]].kind === 'compute';
      if (maxN < 2 && !isCompute) bad.push(c.id + '#' + k + ' could not step');
      if (isCompute) { const btns = [...document.querySelectorAll('#main .alab button, #main .alab select, #main .uxl button, #main .uxl select, #main .uxl input[type=checkbox], #main .uil button, #main .uil select, #main .uil input[type=checkbox]')]; for (const b of btns) { if (b.tagName === 'SELECT') { for (const o of [...b.options]) { b.value = o.value; b.dispatchEvent(new Event('change', { bubbles: true })); await wait(20); } } else { b.click(); await wait(20); } const l = leak(); if (l) bad.push(c.id + ' lab ' + (b.dataset.fk || '') + ' leak ' + l); } if (ovf() && window.innerWidth <= 400) bad.push(c.id + ' lab overflowX'); }
      // điều khiển ở mức model: mỗi giá trị của điều khiển phải làm đổi danh sách bước
      const mid = c.sims[k], def = ADE.models[mid];
      if (def && def.kind === 'discrete' && def.controls) {
        for (const cc of def.controls) {
          const S = ADE.engine.create(mid), base = JSON.stringify(S.steps);
          let vals = cc.type === 'toggle' ? [!cc.get(S.state)] : cc.type === 'select' ? cc.options.map(o => o.value).filter(v => v !== cc.get(S.state)) : [cc.payload];
          let diff = false;
          for (const v of vals) { const S2 = ADE.engine.create(mid); S2.act(cc.action, v); if (JSON.stringify(S2.steps) !== base) diff = true; }
          if (!diff) bad.push(c.id + '#' + k + ' model control ' + cc.id + ' does not change steps (from initial state)');
        }
      }
      // điều khiển sandbox (DOM)
      const ctl = [...document.querySelectorAll('.sandbox [data-fk^=sb-]')];
      let changed = 0, same = [];
      for (const el of ctl) {
        const fk = el.dataset.fk;
        if (el.tagName === 'SELECT') {
          const opts = [...el.options].map(o => o.value); let any = false;
          for (const v of opts) {
            const e2 = document.querySelector('[data-fk="' + fk + '"]'); if (!e2) break;
            if (e2.value === v) continue;
            const before = sig(); e2.value = v; e2.dispatchEvent(new Event('change', { bubbles: true })); await wait(60);
            if (sig() !== before) any = true;
            const l = leak(); if (l) bad.push(c.id + '#' + k + ' ' + fk + '=' + v + ' leak ' + l);
          }
          any ? changed++ : same.push(fk);
        } else {
          const before = sig(); el.click(); await wait(60);
          sig() !== before ? changed++ : same.push(fk);
          const l = leak(); if (l) bad.push(c.id + '#' + k + ' ' + fk + ' leak ' + l);
        }
      }
      // focus sau khi bấm Tiếp
      location.hash = '#/' + lang() + '/' + tid + '/' + c.id + '/1'; await wait(200);
      if (k > 0) { const tabs = [...document.querySelectorAll('#main [role=tablist]')[0].querySelectorAll('[role=tab]')]; if (tabs[k]) { tabs[k].click(); await wait(200); } }
      { const st = document.querySelector('[data-fk=start]'); if (st && !document.querySelector('[data-fk=nav-next]')) { st.click(); await wait(150); } }
      const nb = nextBtn(); let focusOk = true;
      if (nb && !nb.disabled) { nb.focus(); nb.click(); await wait(60); focusOk = document.activeElement && document.activeElement.tagName !== 'BODY'; }
      // đổi ngôn ngữ giữa chừng
      const h0 = location.hash, other = lang() === 'vi' ? 'en' : 'vi';
      const lb = document.querySelector('[data-fk=lang-' + other + ']'); if (lb) { lb.click(); await wait(200); }
      const h1 = location.hash, keep = h1.replace('/' + other + '/', '/' + lang() + '/') === h0 || h1.split('/').slice(2).join('/') === h0.split('/').slice(2).join('/');
      if (!keep) bad.push(c.id + '#' + k + ' lang switch lost route ' + h0 + ' -> ' + h1);
      const l2 = leak(); if (l2) bad.push(c.id + '#' + k + ' after-lang leak ' + l2);
      const lb2 = document.querySelector('[data-fk=lang-' + (other === 'vi' ? 'en' : 'vi') + ']'); if (lb2) { lb2.click(); await wait(150); }
      if (!focusOk) bad.push(c.id + '#' + k + ' focus fell to BODY');
      if (same.length) out.push('  (info) DOM text unchanged at last position for: ' + same.join(','));
      out.push(c.id + '#' + k + ': N=' + (maxN - 1) + ' controls=' + ctl.length + ' changed=' + changed);
    }
  }
  // preset
  for (const p of t.presets) {
    location.hash = '#/' + lang() + '/live?preset=' + p.id + '&step=2'; await wait(250);
    const l = leak(); if (l) bad.push('preset ' + p.id + ' leak ' + l);
    if (!document.querySelector('#main .stage, #main .sim, #main svg')) bad.push('preset ' + p.id + ' no stage');
  }
  return out.join('\n') + '\n--- problems (' + bad.length + ')\n' + bad.join('\n');
})()
