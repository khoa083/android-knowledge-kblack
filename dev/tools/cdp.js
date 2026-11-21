// Công cụ kiểm thử: mở một URL file:// bằng Chrome headless, in lỗi console, chạy các biểu thức JS, chụp ảnh.
// Dùng: node cdp.js <url> [--el selector: chỉ chụp phần tử] [--w 1280] [--h 900] [--dark] [--reduce] [--eval "js"]... [--shot path.png] [--full] [--wait ms]
const { spawn } = require('child_process');
const fs = require('fs'); const os = require('os'); const path = require('path'); const http = require('http');
const args = process.argv.slice(2);
const url = args[0]; const opt = { w: 1280, h: 900, evals: [], shot: null, full: false, wait: 900, dark: false, reduce: false, mobile: false };
for (let i = 1; i < args.length; i++) {
  const a = args[i];
  if (a === '--w') opt.w = +args[++i]; else if (a === '--h') opt.h = +args[++i];
  else if (a === '--eval') opt.evals.push(args[++i]); else if (a === '--shot') opt.shot = args[++i];
  else if (a === '--full') opt.full = true; else if (a === '--wait') opt.wait = +args[++i];
  else if (a === '--pre') opt.pre = args[++i]; else if (a === '--dark') opt.dark = true; else if (a === '--reduce') opt.reduce = true; else if (a === '--mobile') opt.mobile = true; else if (a === '--el') opt.el = args[++i];
}
const port = 9300 + Math.floor(Math.random() * 500);
const prof = fs.mkdtempSync(path.join(os.tmpdir(), 'cdp-'));
const chrome = spawn(process.env.BROWSER_EXE || 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe', ['--headless=new', '--remote-debugging-port=' + port, '--user-data-dir=' + prof, '--no-first-run', '--disable-gpu', '--hide-scrollbars', `--window-size=${opt.w},${opt.h}`, 'about:blank'], { stdio: 'ignore' });
const sleep = ms => new Promise(r => setTimeout(r, ms));
const getJSON = u => new Promise((res, rej) => http.get(u, r => { let d = ''; r.on('data', c => d += c); r.on('end', () => { try { res(JSON.parse(d)); } catch (e) { rej(e); } }); }).on('error', rej));
(async () => {
  let targets;
  for (let i = 0; i < 50; i++) { try { targets = await getJSON(`http://127.0.0.1:${port}/json`); if (targets.length) break; } catch (e) { } await sleep(200); }
  const page = targets.find(t => t.type === 'page');
  const ws = new WebSocket(page.webSocketDebuggerUrl);
  await new Promise(r => ws.addEventListener('open', r));
  let id = 0; const pending = {}; const logs = [];
  ws.addEventListener('message', ev => {
    const m = JSON.parse(ev.data);
    if (m.id && pending[m.id]) { pending[m.id](m); delete pending[m.id]; return; }
    if (m.method === 'Runtime.consoleAPICalled') logs.push(`[console.${m.params.type}] ` + m.params.args.map(a => a.value !== undefined ? a.value : a.description).join(' '));
    if (m.method === 'Runtime.exceptionThrown') { const d = m.params.exceptionDetails; logs.push('[EXCEPTION] ' + (d.exception && d.exception.description || d.text) + ' @' + (d.url || '') + ':' + d.lineNumber); }
    if (m.method === 'Log.entryAdded') logs.push(`[log.${m.params.entry.level}] ${m.params.entry.text} ${m.params.entry.url || ''}`);
  });
  const send = (method, params = {}) => new Promise(r => { const i = ++id; pending[i] = r; ws.send(JSON.stringify({ id: i, method, params })); });
  await send('Runtime.enable'); await send('Log.enable'); await send('Page.enable');
  const feats = [];
  if (opt.dark) feats.push({ name: 'prefers-color-scheme', value: 'dark' });
  if (opt.reduce) feats.push({ name: 'prefers-reduced-motion', value: 'reduce' });
  if (feats.length) await send('Emulation.setEmulatedMedia', { features: feats });
  await send('Emulation.setDeviceMetricsOverride', { width: opt.w, height: opt.h, deviceScaleFactor: 1, mobile: opt.mobile });
  if (opt.pre) await send('Page.addScriptToEvaluateOnNewDocument', { source: opt.pre });
  await send('Page.navigate', { url });
  await sleep(opt.wait);
  for (const e of opt.evals) {
    const r = await send('Runtime.evaluate', { expression: e, awaitPromise: true, returnByValue: true });
    const v = r.result && r.result.result; const ex = r.result && r.result.exceptionDetails;
    console.log('> ' + e.slice(0, 90).replace(/\n/g, ' ') + '\n= ' + (ex ? 'EXC ' + (ex.exception && ex.exception.description || ex.text) : JSON.stringify(v && v.value !== undefined ? v.value : v && v.description)));
    await sleep(150);
  }
  if (opt.shot) {
    let clip;
    if (opt.full) { const m = await send('Page.getLayoutMetrics'); const c = m.result.cssContentSize || m.result.contentSize; clip = { x: 0, y: 0, width: c.width, height: Math.min(c.height, 6000), scale: 1 }; }
    if (opt.el) {
      const q = await send('Runtime.evaluate', { expression: `(function(){var e=document.querySelector(${JSON.stringify(opt.el)}); if(!e) return null; var r=e.getBoundingClientRect(); return [r.left+scrollX, r.top+scrollY, r.width, r.height];})()`, returnByValue: true });
      const b = q.result.result.value; if (b) clip = { x: b[0], y: b[1], width: Math.max(1, b[2]), height: Math.max(1, b[3]), scale: 1 };
    }
    const r = await send('Page.captureScreenshot', { format: 'png', clip, captureBeyondViewport: !!(opt.full || opt.el) });
    fs.writeFileSync(opt.shot, Buffer.from(r.result.data, 'base64')); console.log('shot ' + opt.shot);
  }
  console.log('--- console (' + logs.length + ')'); logs.forEach(l => console.log(l));
  ws.close(); chrome.kill(); setTimeout(() => process.exit(0), 300);
})().catch(e => { console.error('FAIL', e); chrome.kill(); process.exit(1); });
