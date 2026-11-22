/* syntax-check.js: chạy trong trang (cdp.js --eval). Tokenize mọi snippet đã đăng ký và mọi khối kt/exkt/fixkt/solkt trong nội dung,
   ở cả vi và en; báo dòng nào ghép lại không khớp chữ gốc (mất/thêm ký tự) và thống kê số token mỗi lớp. */
(function () {
  var bad = [], stat = {}, blocks = 0;
  function check(name, lines, lang) {
    var toks = ADE.syntax.tokenize(lines, lang); if (!toks) return; blocks++;
    toks.forEach(function (tl, i) {
      var j = tl.map(function (t) { return t.t; }).join('');
      if (j !== lines[i]) bad.push(name + ':' + (i + 1) + ' «' + lines[i] + '» ≠ «' + j + '»');
      tl.forEach(function (t) { var k = t.c || 'plain'; stat[k] = (stat[k] || 0) + 1; });
    });
  }
  ['vi', 'en'].forEach(function (L) {
    Object.keys(ADE.code).forEach(function (k) {
      var sn = ADE.code[k]; check(k + '/' + L, sn.lines.map(function (ln) { return typeof ln === 'string' ? ln : (ln[L] || ln.vi); }), sn.lang);
    });
    var dict = (ADE.strings && ADE.strings[L]) || {};
    Object.keys(dict).forEach(function (k) { if (/\.(kt|exkt|fixkt|solkt)$/.test(k)) check(k + '/' + L, String(dict[k]).split('\n'), 'kotlin'); });
  });
  return blocks + ' khối, sai=' + bad.length + ' | ' + JSON.stringify(stat) + (bad.length ? '\n' + bad.slice(0, 20).join('\n') : '');
})()
