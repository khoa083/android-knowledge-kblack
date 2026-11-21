// Chụp vùng sơ đồ của nhiều route để xem bằng mắt (dev). Dùng:
//   node dev/tools/shots.js <thư mục ra> <route>[@<tab sim>] ... [--dark] [--w 1280] [--el .canvas]
// route ví dụ: vi/coroutines/a1/4   (tab sim thứ 2 của chương: vi/coroutines/a7/3@1)
const { execFileSync } = require('child_process');
const path = require('path');
const args = process.argv.slice(2);
const out = args.shift();
const extra = []; const routes = [];
let el = '.canvas';
for (let i = 0; i < args.length; i++) {
  if (args[i] === '--dark' || args[i] === '--reduce' || args[i] === '--mobile') extra.push(args[i]);
  else if (args[i] === '--w' || args[i] === '--h') { extra.push(args[i], args[++i]); }
  else if (args[i] === '--el') el = args[++i];
  else routes.push(args[i]);
}
const root = 'file:///' + path.resolve(__dirname, '..', '..').replace(/\\/g, '/') + '/index.html#/';
routes.forEach(r => {
  const [route, tab] = r.split('@');
  const name = route.replace(/\//g, '_') + (tab ? '_t' + tab : '') + (extra.includes('--dark') ? '_dark' : '') + '.png';
  const ev = [];
  if (tab) {
    const pos = +route.split('/').pop();
    ev.push('--eval', `(function(){var b=document.querySelector('[role=tablist][aria-label="'+ADE.t('app.sims')+'"] [data-id="${tab}"]'); if(b) b.click(); return !!b;})()`);
    ev.push('--eval', `(function(){var l=document.querySelectorAll('.steplink'); if(l[${pos - 1}]) l[${pos - 1}].click(); return l.length;})()`);
  }
  const res = execFileSync('node', [path.join(__dirname, 'cdp.js'), root + route, '--el', el, '--shot', path.join(out, name), '--wait', '1600', ...extra, ...ev], { encoding: 'utf8' });
  const errs = res.split('\n').filter(l => /EXCEPTION|console\.error/.test(l));
  console.log(name + (errs.length ? '  ERR ' + errs.join(' | ') : ''));
});
