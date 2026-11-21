/* Kho nguồn toàn cục (chỉ nguồn dùng chung cho cả site). Nguồn riêng của track nằm ở tracks/<id>/sources.js.
   URL là URL ĐÍCH sau khi chuyển hướng (docs/research/global.md mục 3). Tiêu đề giữ nguyên bản gốc. */
ADE.addSources([
  { id: 'inspo-protocol', title: 'Protocol Explorer', url: 'https://protocol-explorer-alpha.vercel.app/', org: 'Vercel (trang mẫu)', tracks: [], pageOnly: true, lang: 'en',
    supports: { vi: 'Cảm hứng UX: tinh thần explorer từng bước, chọn thành phần. Site chỉ học cách truyền đạt, không sao chép mã, hình hay chữ.', en: 'UX inspiration: the step-by-step explorer idea and picking a component. This site learns only the way of teaching and copies no code, image or text.' } },
  { id: 'inspo-dts', title: 'Designed to Scale', url: 'https://designed-to-scale.vercel.app/', org: 'Vercel (trang mẫu)', tracks: [], pageOnly: true, lang: 'en',
    supports: { vi: 'Cảm hứng UX: chia bài thành bước, sơ đồ có chuyển động. Chỉ học cách truyền đạt, không sao chép.', en: 'UX inspiration: splitting a lesson into steps and animated diagrams. Only the way of teaching is learned; nothing is copied.' } },
  { id: 'w3c-lang-decl', title: 'Declaring language in HTML', url: 'https://www.w3.org/International/questions/qa-html-language-declarations', org: 'W3C Internationalization', tracks: [], lang: 'en',
    supports: { vi: 'Khai báo ngôn ngữ trang bằng thuộc tính lang và đánh dấu ngôn ngữ cho từng đoạn văn bản.', en: 'Declaring the page language with the lang attribute and marking the language of text fragments.' } },
  { id: 'w3c-i18n', title: 'W3C Internationalization', url: 'https://www.w3.org/International/', org: 'W3C', tracks: [], lang: 'en',
    supports: { vi: 'Nguyên tắc quốc tế hóa chung cho web, làm nền cho cách tổ chức song ngữ của site.', en: 'General web internationalization principles behind how this site organizes two languages.' } },
  { id: 'wcag-lang-page', title: 'Understanding Success Criterion 3.1.1: Language of Page', url: 'https://www.w3.org/WAI/WCAG22/Understanding/language-of-page.html', org: 'W3C WAI (WCAG 2.2)', tracks: [], label: 'normative', lang: 'en',
    supports: { vi: 'Tiêu chí 3.1.1: ngôn ngữ của trang phải xác định được bằng phần mềm, nên site cập nhật lang khi đổi ngôn ngữ.', en: 'Success criterion 3.1.1: the page language must be programmatically determinable, so the site updates lang when you switch language.' } },
  { id: 'wcag-lang-parts', title: 'Understanding Success Criterion 3.1.2: Language of Parts', url: 'https://www.w3.org/WAI/WCAG22/Understanding/language-of-parts.html', org: 'W3C WAI (WCAG 2.2)', tracks: [], label: 'normative', lang: 'en',
    supports: { vi: 'Tiêu chí 3.1.2: đoạn văn bản khác ngôn ngữ trang cần được đánh dấu, nên thuật ngữ tiếng Anh trong bản tiếng Việt được bọc lang="en".', en: 'Success criterion 3.1.2: passages in another language should be marked, so English terms inside the Vietnamese text are wrapped in lang="en".' } },
  { id: 'mdn-lang', title: 'lang HTML global attribute', url: 'https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Global_attributes/lang', org: 'MDN Web Docs', tracks: [], lang: 'en',
    supports: { vi: 'Cú pháp và ý nghĩa của thuộc tính lang.', en: 'Syntax and meaning of the lang attribute.' } },
  { id: 'mdn-reduced-motion', title: 'prefers-reduced-motion CSS media feature', url: 'https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/@media/prefers-reduced-motion', org: 'MDN Web Docs', tracks: [], lang: 'en',
    supports: { vi: 'Đọc tùy chọn giảm chuyển động của hệ điều hành; site dùng thêm nút tắt thủ công.', en: 'Reads the operating-system reduced-motion preference; the site adds a manual switch on top.' } },
  { id: 'aria-apg', title: 'ARIA Authoring Practices Guide', url: 'https://www.w3.org/WAI/ARIA/apg/', org: 'W3C WAI', tracks: [], lang: 'en',
    supports: { vi: 'Mẫu tab, hộp thoại và phím tắt mà các thành phần giao diện của site tham khảo.', en: 'Tab, dialog and keyboard patterns that the site interface components follow.' } }
]);

// Phiên bản đã đối chiếu (docs/research/global.md mục 2). Các phase track thêm mục riêng vào ADE.versions.items.
ADE.setVersions({
  date: '2026-11-20',
  items: [
    { name: 'Kotlin', value: '2.4.21' },
    { name: 'kotlinx.coroutines', value: '1.11.0' },
    { name: 'Compose BOM', value: '2026.11.01 (runtime 1.13.0, ui 1.13.0, animation 1.13.0, material3 1.5.0)' },
    { name: 'Compose Compiler', value: 'org.jetbrains.kotlin.plugin.compose 2.4.21',
      note: { vi: 'Đi kèm Kotlin; strong skipping bật mặc định từ Kotlin 2.0.20.', en: 'Ships with Kotlin; strong skipping is on by default since Kotlin 2.0.20.' } },
    { name: 'AndroidX Lifecycle', value: '2.11.1' },
    { name: 'WCAG', value: '2.2 (W3C Recommendation 2024-12-12)' },
    { name: 'Material 3', value: '2026-11-20',
      note: { vi: 'Ngày đối chiếu. Giá trị token cụ thể được ghi ở track dùng đến.', en: 'Cross-check date. Specific token values are recorded in the track that uses them.' } },
    { name: 'Android design guidance', value: '2026-11-20',
      note: { vi: 'Ngày đối chiếu. Giá trị cụ thể được ghi ở track dùng đến.', en: 'Cross-check date. Specific values are recorded in the track that uses them.' } }
  ]
});
