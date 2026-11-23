/* Nguồn của track F (Kotlin). Trang kotlinlang.org đọc nội dung ngày 2026-11-23 (docs/research/kotlin.md); sách đọc chương liên quan. */
(function () {
  var D = 'https://kotlinlang.org/docs/';
  var s = function (id, title, url, org, label, vi, en) { return { id: id, title: title, url: url, org: org, tracks: ['kotlin'], label: label, lang: 'en', supports: { vi: vi, en: en } }; };
  ADE.addSources([
    s('kt-basic-syntax', 'Basic syntax', D + 'basic-syntax.html', 'Kotlin docs (JetBrains)', 'stable', 'val gán một lần, var gán lại được (K1).', 'val is assigned once, var can be reassigned (K1).'),
    s('kt-numbers', 'Numbers', D + 'numbers.html', 'Kotlin docs (JetBrains)', 'stable', 'Chia nguyên bỏ phần lẻ; chuyển kiểu phải tường minh; tràn số không báo lỗi; boxing và cache -128..127 trên JVM (K1).', 'Integer division drops the fraction; conversions are explicit; overflow is silent; boxing and the -128..127 cache on the JVM (K1).'),
    s('kt-control-flow', 'Conditions and loops', D + 'control-flow.html', 'Kotlin docs (JetBrains)', 'stable', 'if và when là biểu thức; nhánh khớp đầu tiên; when dạng biểu thức phải đủ trường hợp (K1).', 'if and when are expressions; the first matching branch wins; a when expression must be exhaustive (K1).'),
    s('kt-functions', 'Functions', D + 'functions.html', 'Kotlin docs (JetBrains)', 'stable', 'Tham số mặc định, đối số có tên, hàm một biểu thức; hàm override dùng giá trị mặc định của hàm gốc (K1).', 'Default parameters, named arguments, single-expression functions; overrides use the base defaults (K1).'),
    s('book-kt-essentials', 'Kotlin Essentials (Marcin Moskała)', 'https://leanpub.com/kotlin_developers', 'Kt. Academy (sách)', 'guideline', 'Biến, kiểu cơ bản, câu điều kiện, hàm; giá trị nào cũng là object, trình biên dịch tối ưu thành kiểu nguyên thủy (K1).', 'Variables, basic types, conditions, functions; every value is an object, optimised to primitives by the compiler (K1).'),
    s('book-effective-kotlin', 'Effective Kotlin: Best Practices (Marcin Moskała)', 'https://leanpub.com/effectivekotlin', 'Kt. Academy (sách)', 'guideline', 'Item 1: val không có nghĩa là bất biến (K1).', 'Item 1: val does not mean immutable (K1).'),
    s('book-kt-exercises', 'Kotlin Exercises (Marcin Moskała)', 'https://leanpub.com/kotlin_exercises', 'Kt. Academy (sách)', 'guideline', 'Nguồn bài tập của track, diễn đạt lại theo ứng dụng Hẹn Khám (K1: Pretty time display).', 'The track\'s exercise source, restated for the ClinicBook app (K1: Pretty time display).')
  ]);
})();
