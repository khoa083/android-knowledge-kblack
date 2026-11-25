// Sinh sources.md song ngữ từ registry (ADE.sourceList, ADE.versions). Chạy: node dev/tools/sources-md.js
// Mở index.html bằng Chrome headless qua cdp.js, lấy markdown, ghi ra sources.md ở thư mục gốc. Sách chỉ ghi tên, tác giả (không đường dẫn file).
const { execFileSync } = require('child_process'); const fs = require('fs'); const path = require('path');
const root = path.resolve(__dirname, '..', '..');
const BOOKS = [
  ['Kotlin Coroutines: Deep Dive', 'Marcin Moskała', 'A'], ['Advanced Kotlin; Effective Kotlin', 'Marcin Moskała', 'A, B'], ['Android Animations by Tutorials', 'Filip Babić, Prateek Prasad, Alex Sullivan', 'C'],
  ['The Design of Everyday Things (Revised & Expanded)', 'Don Norman', 'D'], ["Don't Make Me Think, Revisited", 'Steve Krug', 'D, E'], ['Design for How People Think', 'John Whalen', 'D'],
  ['Measuring the User Experience (3rd ed.)', 'Bill Albert, Tom Tullis', 'D'], ['Strategic Writing for UX', 'Torrey Podmajersky', 'D'], ['Writing Is Designing', 'Michael Metts, Andy Welfle', 'D, E'],
  ['Articulating Design Decisions', 'Tom Greever', 'D'], ['Designing for Behavior Change (2nd ed.)', 'Stephen Wendel', 'D'], ['Design Sprint', 'Richard Banfield, C. Todd Lombardo, Trace Wax', 'D'],
  ['The Design Thinking Playbook', 'Michael Lewrick, Patrick Link, Larry Leifer', 'D'], ['Designing Interfaces (3rd ed.)', 'Jenifer Tidwell, Charles Brewer, Aynne Valencia', 'E'],
  ['Mobile Design Pattern Gallery', 'Theresa Neil', 'E'], ['Practical UI Patterns for Design Systems', 'Diana MacDonald', 'E'], ["The Non-Designer's Design Book", 'Robin Williams', 'E'],
  ['Kotlin Coroutines by Tutorials', 'Kodeco', 'A'], ['Android UI Development with Jetpack Compose', 'Thomas Künneth', 'B'], ['Jetpack Compose by Tutorials', 'Kodeco', 'B'], ['Jetpack Compose 1.3 Essentials', 'Neil Smyth', 'B'],
  ['Kotlin Essentials; Effective Kotlin; Kotlin Exercises', 'Marcin Moskała', 'F'],
  ['Clean Android Architecture', 'Alexandru Dumbravan', 'G'], ['Clean Architecture for Android', 'Eran Boudjnah', 'G'], ['Saving Data on Android', 'raywenderlich.com (Kodeco)', 'H'],
  ['Mobile System Design', "Tjeerd in 't Veen", 'I'], ['Designing Data-Intensive Applications', 'Martin Kleppmann', 'I'], ['System Design Interview (vol. 1, 2)', 'Alex Xu', 'I'],
  ['Acing the System Design Interview', 'Zhiyong Tan', 'I'], ['Operating System Concepts (10th ed.)', 'Abraham Silberschatz, Peter B. Galvin, Greg Gagne', 'I'], ['API Design Patterns', 'JJ Geewax', 'I'],
  ['Clean Code; The Clean Coder; Clean Architecture; Clean Craftsmanship; Clean Agile', 'Robert C. Martin', 'J'], ['The Software Craftsman', 'Sandro Mancuso', 'J'],
  ['Code That Fits in Your Head', 'Mark Seemann', 'J, K'], ['Android Test-Driven Development', 'Kodeco', 'J'],
  ['From Objects to Functions', 'Uberto Barbini', 'K'], ['Functional Programming in Kotlin', 'Marco Vermeulen, Rúnar Bjarnason, Paul Chiusano', 'K'], ['Functional Programming in Kotlin by Tutorials', 'Kodeco', 'K'], ['Functional Kotlin', 'Marcin Moskała', 'K']
];
const expr = `(() => {
  const L = [], tr = id => { const t = ADE.getTrack(id); return t ? t.code : id; };
  L.push('# Nguồn / Sources', '', 'Sinh tự động từ registry của site (dev/tools/sources-md.js). Generated from the site registry. Ngày đối chiếu / checked: 2026-11-20 … 2026-11-25.', '');
  L.push('## Phiên bản và ngày đối chiếu / Versions and check dates', '');
  (ADE.versions && ADE.versions.items || []).forEach(v => L.push('- ' + v.name + ': ' + v.value + (v.note ? ' — ' + (v.note.vi || '') + ' / ' + (v.note.en || '') : '')));
  L.push('', '## Nguồn chính thức, chuẩn và thứ cấp / Official, normative and secondary sources', '',
    'Nguồn chính thức hoặc chuẩn luôn thắng khi mâu thuẫn với nguồn thứ cấp (ví dụ lawsofux.com chỉ là nguồn thứ cấp). Official or normative sources win over secondary ones (for example lawsofux.com is secondary only). Mục "đọc thêm" chưa được dùng làm nguồn cho khẳng định cụ thể / "Further reading" items are not yet the source of a specific claim.', '');
  const groups = {};
  ADE.sourceList.forEach(s => { const k = (s.tracks && s.tracks.length) ? s.tracks.map(tr).join(', ') : 'shared'; (groups[k] = groups[k] || []).push(s); });
  Object.keys(groups).sort().forEach(k => {
    L.push('### ' + (k === 'shared' ? 'Chung / Shared' : 'Track ' + k), '');
    groups[k].forEach(s => {
      L.push('- **' + s.title + '** — ' + (s.org || '') + (s.label ? ' · \`' + s.label + '\`' : '') + (s.pageOnly ? ' · đọc thêm / further reading' : ''));
      L.push('  ' + s.url);
      if (s.supports) { L.push('  - vi: ' + (s.supports.vi || '')); L.push('  - en: ' + (s.supports.en || '')); }
    });
    L.push('');
  });
  return L.join('\\n');
})()`;
const out = execFileSync('node', [path.join(__dirname, 'cdp.js'), 'file:///' + path.join(root, 'index.html').replace(/\\/g, '/') + '#/vi/', '--wait', '2500', '--eval', expr], { encoding: 'utf8', maxBuffer: 20 * 1024 * 1024 });
const line = out.split('\n').find(l => l.startsWith('= '));
let md = JSON.parse(line.slice(2));
md += '\n## Sách tham khảo / Reference books\n\nSách là nguồn giảng dạy cùng tài liệu chính thức; khi mâu thuẫn, tài liệu chính thức thắng. Bài giảng viết lại bằng lời của site và không dẫn số chương sách. Framework của tác giả ghi tên tác giả. Books are teaching sources alongside the official documentation; when they conflict, the official documentation wins. Lessons are written in the site\'s own words and do not cite book chapter numbers. Named frameworks credit their authors.\n\n';
BOOKS.forEach(b => { md += '- *' + b[0] + '* — ' + b[1] + ' (track ' + b[2] + ')\n'; });
md += '\n## Cảm hứng UX / UX inspiration\n\nHai trang mẫu chỉ là cảm hứng UX (bố cục, cách xem theo bước); site không sao chép mã, CSS, SVG, câu chữ hay ví dụ của chúng. The two sample sites are UX inspiration only; no code, CSS, SVG, wording or examples are copied. Xem trang Nguồn của site / see the site\'s Sources page.\n';
fs.writeFileSync(path.join(root, 'sources.md'), md, 'utf8');
console.log('sources.md: ' + md.length + ' chars, ' + (md.match(/^- \*\*/gm) || []).length + ' sources');
