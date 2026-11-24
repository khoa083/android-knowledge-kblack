// Kiểm chuyển động của mọi hình trong một track (chạy bằng cdp.js --pre "window.__TRACK='<id>'" --eval "$(cat dev/tools/motion-check.js)").
// Tiêu chí (docs/design-principles.md §5.2, người dùng 2026-11-24: hợp UI/UX, không trang trí):
//   1. mỗi lần đổi bước làm hình ĐỔI (DOM khác) thì phải có chuyển cảnh ngay sau đó (animation đang chạy trong ~80 ms);
//   2. mỗi sim phải có chuyển động ở ít nhất một lúc (không có hình nào đứng yên suốt cả bài).
// Lab tự vẽ: đổi điều khiển đầu tiên rồi xem có chuyển cảnh. Track đang đóng thì bỏ qua. Chạy với giảm chuyển động TẮT.
(async () => {
  const wait = ms => new Promise(r => setTimeout(r, ms)), bad = [];
  const tid = window.__TRACK, t = ADE.getTrack(tid);
  if (!t) return 'NO TRACK ' + tid;
  if (!ADE.trackOpen(t)) return tid + ': track đang đóng (trang "sắp có"), bỏ qua';
  const running = el => el ? el.getAnimations({ subtree: true }).filter(a => a.playState === 'running' && !(a.effect && a.effect.pseudoElement)).length : 0;
  // so nội dung thật: bỏ lớp chuyển động tạm (mo-chg, mo-live) mà lần chuyển cảnh trước để lại
  const html = el => el ? el.innerHTML.replace(/\s?mo-(chg|live)/g, '').replace(/ class=""/g, '') : '';
  const vis = sel => [...document.querySelectorAll('#main ' + sel)].find(e => !e.hidden && e.offsetParent !== null);
  let sims = 0, changes = 0;
  for (const c of t.chapters) {
    for (let k = 0; k < Math.max(1, c.sims.length); k++) {
      location.hash = '#/vi/' + tid + '/' + c.id + '/1'; await wait(300);
      if (k > 0) { const tl = document.querySelectorAll('#main [role=tablist]')[0]; const tabs = tl ? [...tl.querySelectorAll('[role=tab]')] : []; if (tabs[k]) { tabs[k].click(); await wait(300); } }
      const mid = c.sims[k], def = ADE.models[mid]; if (!def) continue; sims++;
      if (def.kind === 'compute') {
        const slot = vis('.stage-slot'), before = html(slot);
        const ctl = slot && [...slot.querySelectorAll('select, input[type=range], input[type=checkbox], button')].find(x => !x.disabled);
        if (ctl) {
          if (ctl.tagName === 'SELECT' && ctl.options.length > 1) { ctl.selectedIndex = (ctl.selectedIndex + 1) % ctl.options.length; ctl.dispatchEvent(new Event('change', { bubbles: true })); }
          else if (ctl.type === 'range') { ctl.value = String(Math.min(+ctl.max, +ctl.value + (+ctl.step || 1) * 3)); ctl.dispatchEvent(new Event('input', { bubbles: true })); ctl.dispatchEvent(new Event('change', { bubbles: true })); }
          else ctl.click();
        }
        await wait(80);
        if (slot && html(slot) !== before && running(slot) < 1) bad.push(c.id + '#' + k + ' lab (' + mid + '): đổi mà không có chuyển cảnh');
        continue;
      }
      { const st = document.querySelector('[data-fk=start]'); if (st && !document.querySelector('[data-fk=nav-next]')) { st.click(); await wait(250); } }
      const next = () => document.querySelector('[data-fk=nav-next]');
      const box = () => vis('.view-screen') || vis('.view-diagram');
      let moved = running(box()) > 0, guard = 0;
      while (next() && !next().disabled && guard++ < 200) {
        const before = html(box());
        next().click(); await wait(80);
        const a = box(), n = running(a);
        if (n > 0) moved = true;
        const atWrap = !next() || next().disabled;   // sang trang tổng kết: hình giữ trạng thái bước cuối, không tính
        if (a && !atWrap && html(a) !== before) { changes++; if (n < 1) bad.push(c.id + '#' + k + ' bước ' + (guard + 1) + ' (' + mid + '): hình đổi mà không có chuyển cảnh'); }
        await wait(260);   // nhịp bấm như người thật; labMotion bỏ qua những lần vẽ dồn dập < 150 ms (coi là lab tự chạy)
      }
      if (!moved) bad.push(c.id + '#' + k + ' (' + mid + '): không có chuyển động suốt bài');
    }
  }
  return tid + ': ' + sims + ' sim, ' + changes + ' lần hình đổi, ' + bad.length + ' vấn đề\n' + bad.slice(0, 40).join('\n');
})()
