/* Nguồn của track J (Mã sạch và kỷ luật làm nghề). Sách đọc từ bản trong thư viện cá nhân từ 2026-11-24 (docs/research/cleancode.md).
   Code That Fits in Your Head (book-seemann) đã khai báo ở tracks/sysdesign/sources.js với tracks gồm cả cleancode. */
(function () {
  var s = function (id, title, url, org, label, vi, en) { return { id: id, title: title, url: url, org: org, tracks: ['cleancode'], label: label, lang: 'en', supports: { vi: vi, en: en } }; };
  ADE.addSources([
    s('book-cleancode', 'Clean Code: A Handbook of Agile Software Craftsmanship (Robert C. Martin, 2008)', 'https://www.informit.com/store/clean-code-a-handbook-of-agile-software-craftsmanship-9780132350884', 'Prentice Hall (sách)', 'guideline',
      'Ch.3: hàm nên nhỏ, và nhỏ hơn nữa; hiếm khi tới 20 dòng (tác giả thừa nhận không có nghiên cứu chứng minh, chỉ có kinh nghiệm); khối trong if, else, while nên dài một dòng; làm một việc; mọi câu lệnh ở cùng một mức trừu tượng; đọc từ trên xuống theo stepdown rule (J1). Ví dụ Java, site viết lại bằng Kotlin.',
      'Ch.3: functions should be small, then smaller than that; hardly ever 20 lines (the author admits no research shows this, only experience); blocks inside if, else, while should be one line; do one thing; every statement at one level of abstraction; read top-down by the stepdown rule (J1). Java examples, rewritten by the site in Kotlin.')
  ]);
})();
