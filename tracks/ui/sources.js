/* Nguồn của track E. Ngày đối chiếu 2026-11-21 (docs/research/ui.md). m3.material.io đọc bằng Chrome headless (trang SPA).
   Mục "đọc thêm" (pageOnly) chưa đọc nội dung lần này, chưa dùng cho khẳng định cụ thể. */
(function () {
  var W = 'https://www.w3.org/WAI/WCAG22/Understanding/', A = 'https://developer.android.com/', M3 = 'https://m3.material.io/', N = 'https://www.nngroup.com/articles/';
  var s = function (id, title, url, org, label, vi, en) { return { id: id, title: title, url: url, org: org, tracks: ['ui'], label: label, lang: 'en', supports: { vi: vi, en: en } }; };
  var more = function (id, url, title, org, label) { return { id: id, title: title, url: url, org: org, tracks: ['ui'], label: label, lang: 'en', pageOnly: true, supports: { vi: 'Đọc thêm (chưa dùng làm nguồn cho khẳng định cụ thể).', en: 'Further reading (not yet used as the source of a specific claim).' } }; };
  ADE.addSources([
    s('wcag22', 'Web Content Accessibility Guidelines (WCAG) 2.2', 'https://www.w3.org/TR/WCAG22/', 'W3C', 'normative', 'Relative luminance (ngưỡng 0.04045), contrast ratio, chữ lớn, các tiêu chí 1.4.1, 1.4.3, 1.4.4, 1.4.6, 1.4.11, 2.2.2, 2.3.3, 2.4.7, 2.5.5, 2.5.8 (E3, E5, E9, E10).', 'Relative luminance (0.04045 threshold), contrast ratio, large text, criteria 1.4.1, 1.4.3, 1.4.4, 1.4.6, 1.4.11, 2.2.2, 2.3.3, 2.4.7, 2.5.5, 2.5.8 (E3, E5, E9, E10).'),
    s('wai-principles', 'Accessibility Principles', 'https://www.w3.org/WAI/fundamentals/accessibility-principles/', 'W3C WAI', 'normative', 'Bốn nguyên tắc: perceivable, operable, understandable, robust (E10).', 'Four principles: perceivable, operable, understandable, robust (E10).'),
    s('and-wsc', 'Use window size classes', A + 'develop/ui/compose/layouts/adaptive/use-window-size-classes', 'Android Developers', 'stable', 'Breakpoint: compact < 600dp, medium < 840, expanded < 1200, large < 1600, extra-large (E4).', 'Breakpoints: compact < 600dp, medium < 840, expanded < 1200, large < 1600, extra-large (E4).'),
    s('and-canonical', 'Canonical layouts', A + 'develop/ui/compose/layouts/adaptive/canonical-layouts', 'Android Developers', 'stable', 'List-detail, supporting pane, feed; ListDetailPaneScaffold (E4).', 'List-detail, supporting pane, feed; ListDetailPaneScaffold (E4).'),
    s('and-design-a11y', 'Accessibility (Android design foundations)', A + 'design/ui/mobile/guides/foundations/accessibility', 'Android Developers', 'ds-guideline', 'Target ít nhất 48 dp; tương phản chữ 4.5:1, thành phần 3:1 (E5, E10).', 'Targets at least 48 dp; text contrast 4.5:1, components 3:1 (E5, E10).'),
    s('and-a11y-defaults', 'Accessibility API defaults', A + 'develop/ui/compose/accessibility/api-defaults', 'Android Developers', 'stable', 'minimumInteractiveComponentSize giữ ≥ 48 dp (E5).', 'minimumInteractiveComponentSize reserves ≥ 48 dp (E5).'),
    s('and-m3-compose', 'Material Design 3 in Compose', A + 'develop/ui/compose/designsystems/material3', 'Android Developers', 'stable', 'MaterialTheme(colorScheme, typography, shapes); dynamic color từ Android 12; NavigationBar/Rail/Drawer theo kích thước (E3, E4, E8).', 'MaterialTheme(colorScheme, typography, shapes); dynamic color from Android 12; NavigationBar/Rail/Drawer by size (E3, E4, E8).'),
    s('m3-type', 'Typography – type scale tokens', M3 + 'styles/typography/type-scale-tokens', 'Material Design 3 (Google)', 'ds-guideline', 'Cỡ, line height, tracking của 15 vai trò chữ; đọc 2026-11-21 (E2).', 'Size, line height and tracking of the 15 type roles; read 2026-11-21 (E2).'),
    s('m3-motion', 'Easing and duration – tokens & specs', M3 + 'styles/motion/easing-and-duration/tokens-specs', 'Material Design 3 (Google)', 'ds-guideline', 'Token easing (cubic-bezier) và duration 50–1000 ms; đọc 2026-11-21 (E9).', 'Easing (cubic-bezier) and duration tokens 50–1000 ms; read 2026-11-21 (E9).'),
    s('m3-states', 'States – state layers', M3 + 'foundations/interaction/states/state-layers', 'Material Design 3 (Google)', 'ds-guideline', 'State layer: hover 8%, focus 10%, press 10%, drag 16%; đọc 2026-11-21 (E6).', 'State layers: hover 8%, focus 10%, press 10%, drag 16%; read 2026-11-21 (E6).'),
    s('mdc-color', 'Color theming (Material Components for Android)', 'https://github.com/material-components/material-components-android/blob/master/docs/theming/Color.md', 'Material Components for Android', 'ds-guideline', 'Danh sách color role và cặp on-; site chỉ dùng tên vai trò (E3, E8).', 'The list of color roles and their on- pairs; the site uses role names only (E3, E8).'),
    s('nn-fitts', "Fitts's Law and Its Applications in UX", N + 'fitts-law/', 'Nielsen Norman Group (Budiu)', 'quant-model', 'Thời gian di chuyển phụ thuộc kích thước và khoảng cách; T = a + b·log2(2D/W) (E5).', 'Movement time depends on target size and distance; T = a + b·log2(2D/W) (E5).'),
    s('nn-response', 'Response Times: The 3 Important Limits', N + 'response-times-3-important-limits/', 'Nielsen Norman Group (Nielsen)', 'research', 'Mốc 0,1 s, 1 s, 10 s (E7).', 'The 0.1 s, 1 s and 10 s limits (E7).'),
    more('nn-gestalt', N + 'gestalt-proximity/', 'Proximity Principle in Visual Design', 'Nielsen Norman Group', 'research'),
    more('nn-aesthetic', N + 'aesthetic-usability-effect/', 'The Aesthetic-Usability Effect', 'Nielsen Norman Group', 'research'),
    more('nn-darkmode', N + 'dark-mode/', 'Dark Mode vs. Light Mode', 'Nielsen Norman Group', 'research'),
    more('nn-placeholders', N + 'form-design-placeholders/', 'Placeholders in Form Fields Are Harmful', 'Nielsen Norman Group', 'research'),
    more('nn-hamburger', N + 'hamburger-menus/', 'Hamburger Menus and Hidden Navigation', 'Nielsen Norman Group', 'research'),
    more('nn-designsystems', N + 'design-systems-101/', 'Design Systems 101', 'Nielsen Norman Group', 'research'),
    more('nn-animation', N + 'animation-purpose-ux/', 'The Role of Animation and Motion in UX', 'Nielsen Norman Group', 'research'),
    more('wcag-u-contrast', W + 'contrast-minimum.html', 'Understanding SC 1.4.3: Contrast (Minimum)', 'W3C WAI', 'normative'),
    more('wcag-u-target', W + 'target-size-minimum.html', 'Understanding SC 2.5.8: Target Size (Minimum)', 'W3C WAI', 'normative'),
    more('wcag-u-animation', W + 'animation-from-interactions.html', 'Understanding SC 2.3.3: Animation from Interactions', 'W3C WAI', 'normative')
  ]);
})();
