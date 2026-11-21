/* Nguồn của track B. URL đã đọc trực tiếp ngày 2026-11-21 (HTTP 200, không chuyển hướng); xem docs/research/runtime.md. */
(function () {
  var s = function (id, title, url, org, label, vi, en) { return { id: id, title: title, url: url, org: org, tracks: ['runtime'], label: label, lang: 'en', supports: { vi: vi, en: en } }; };
  ADE.addSources([
    s('rt-how', 'How Compose works (runtime design document)', 'https://android.googlesource.com/platform/frameworks/support/+/refs/heads/androidx-main/compose/runtime/design/how-compose-works.md', 'AndroidX (android.googlesource.com)', 'impl',
      'Composer, SlotTable (group, slot, gap buffer), restart group, gộp thao tác Applier. Nhánh androidx-main, đọc 2026-11-21; tài liệu tự cảnh báo vài chi tiết có thể đã cũ (B0, B2, B3, B6).', 'Composer, SlotTable (groups, slots, gap buffer), restart groups, merged Applier operations. androidx-main branch, read 2026-11-21; the document itself warns some details may be outdated (B0, B2, B3, B6).'),
    s('rt-pkg', 'androidx.compose.runtime (package summary)', 'https://developer.android.com/reference/kotlin/androidx/compose/runtime/package-summary.html', 'Android Developers', 'stable',
      'Danh mục API của runtime, gồm CompositionLocal (B0).', 'The runtime API index, including CompositionLocal (B0).'),
    s('rt-snapshot', 'Snapshot', 'https://developer.android.com/reference/kotlin/androidx/compose/runtime/snapshots/Snapshot', 'Android Developers', 'stable',
      'Cách ly, apply nguyên tử, xung đột, read/write observer (B4, B10).', 'Isolation, atomic apply, conflicts, read/write observers (B4, B10).'),
    s('rt-applier', 'Applier', 'https://developer.android.com/reference/kotlin/androidx/compose/runtime/Applier', 'Android Developers', 'stable',
      'Applier<N> generic, các thao tác cây, onBeginChanges/onEndChanges (B6).', 'Generic Applier<N>, tree operations, onBeginChanges/onEndChanges (B6).'),
    s('rt-composeview', 'ComposeView', 'https://developer.android.com/reference/kotlin/androidx/compose/ui/platform/ComposeView', 'Android Developers', 'android-impl',
      'Thời điểm composition ban đầu: gắn window hoặc createComposition(); measure đầu (B1).', 'When the initial composition happens: attach or createComposition(); first measure (B1).'),
    s('rt-frameclock', 'MonotonicFrameClock', 'https://developer.android.com/reference/kotlin/androidx/compose/runtime/MonotonicFrameClock', 'Android Developers', 'stable',
      'withFrameNanos, thời điểm frame tăng nghiêm ngặt (B5, cầu nối X3).', 'withFrameNanos, strictly increasing frame times (B5, bridge X3).'),
    s('rt-recomposer', 'Recomposer', 'https://developer.android.com/reference/kotlin/androidx/compose/runtime/Recomposer', 'Android Developers', 'stable',
      'Bộ lập lịch recomposition; runRecomposeAndApplyChanges là suspend; pause/resume frame clock (B5).', 'The recomposition scheduler; runRecomposeAndApplyChanges is suspend; pause/resume of the frame clock (B5).'),
    s('cp-lifecycle', 'Lifecycle of composables', 'https://developer.android.com/develop/ui/compose/lifecycle', 'Android Developers', 'stable',
      'Identity theo call site, danh sách có/không key, điều kiện skip, kiểu stable (B3, B8).', 'Identity by call site, lists with/without keys, skip conditions, stable types (B3, B8).'),
    s('cp-mental', 'Thinking in Compose', 'https://developer.android.com/develop/ui/compose/mental-model', 'Android Developers', 'stable',
      'Recomposition skip tối đa, lạc quan, có thể bị hủy; composable không side effect (B8).', 'Recomposition skips as much as possible, is optimistic and can be cancelled; side-effect-free composables (B8).'),
    s('cp-phases', 'Jetpack Compose phases', 'https://developer.android.com/develop/ui/compose/phases', 'Android Developers', 'stable',
      'Ba phase, đọc state theo phase, vòng lặp phase (B7, cầu nối X1).', 'The three phases, state reads per phase, phase loops (B7, bridge X1).'),
    s('cp-stability', 'Stability in Compose', 'https://developer.android.com/develop/ui/compose/performance/stability', 'Android Developers', 'stable',
      'Stable/unstable, so sánh tham số, cảnh báo về chú thích (B8).', 'Stable/unstable, parameter comparison, cautions about annotations (B8).'),
    s('cp-strong', 'Strong skipping mode', 'https://developer.android.com/develop/ui/compose/performance/stability/strongskipping', 'Android Developers', 'version',
      'Bật mặc định từ Kotlin 2.0.20; unstable so bằng ===; memoize lambda (B8, B10).', 'On by default since Kotlin 2.0.20; unstable compared with ===; lambda memoization (B8, B10).'),
    s('cp-semantics', 'Semantics in Compose', 'https://developer.android.com/develop/ui/compose/accessibility/semantics', 'Android Developers', 'stable',
      'Semantics tree song song; merged và unmerged; ai dùng cây nào (B9).', 'The parallel semantics tree; merged and unmerged; who uses which tree (B9).'),
    s('rt-releases', 'Compose Runtime releases', 'https://developer.android.com/jetpack/androidx/releases/compose-runtime', 'Android Developers', 'version',
      'Chỉ dùng để xác định phiên bản (1.13.0 trong BOM 2026.11.01).', 'Used only to pin the version (1.13.0 in BOM 2026.11.01).')
  ]);
})();
