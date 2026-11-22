/* Đoạn mã track B. Tất cả là minh họa (illustrative). Mã giả sau transform KHÔNG phải mã compiler bảo đảm sinh ra.
   Số dòng được tham chiếu bởi codeHighlight trong models/models.js. */
(function () {
  var add = function (id, lines) { ADE.addCode('runtime', id, { lang: 'kotlin', illustrative: true, lines: lines }); };
  var c = function (vi, en) { return { vi: vi, en: en }; };
  add('map', [
    'ComposeView(context).setContent {',
    c('  CounterScreen()          // mã composable đã được compiler biến đổi', '  CounterScreen()          // composable code, transformed by the compiler'),
    '}'
  ]);
  add('setcontent', [
    'val view = ComposeView(context)',
    'view.setContent {',
    '  CounterScreen()',
    '}',
    c('parent.addView(view)            // gắn vào window → composition ban đầu', 'parent.addView(view)            // attached to a window → initial composition'),
    c('// hoặc gọi view.createComposition() trước khi gắn', '// or call view.createComposition() before attaching')
  ]);
  add('compiler', [
    '@Composable fun Greeting(name: String) { Text("Hi $name") }',
    c('// ↓ mã giả sau transform (minh họa, không phải mã compiler bảo đảm)', '// ↓ pseudo-code after the transform (illustrative, not guaranteed compiler output)'),
    'fun Greeting(name: String, $composer: Composer, $changed: Int) {',
    '  $composer.startRestartGroup(KEY)',
    '  if ($composer.changed(name) || !$composer.skipping) {',
    '    Text("Hi $name", $composer, ...)',
    '  } else {',
    '    $composer.skipToGroupEnd()',
    '  }',
    '  $composer.endRestartGroup()?.updateScope { c, _ -> Greeting(name, c, ...) }',
    '}'
  ]);
  add('keys', [
    c('// có key', '// with a key'),
    'for (movie in movies) {',
    '  key(movie.id) { MovieOverview(movie) }',
    '}',
    c('// không có key', '// without a key'),
    'for (movie in movies) {',
    '  MovieOverview(movie)',
    '}',
    '@Composable fun MovieOverview(movie: Movie) {',
    '  var expanded by remember { mutableStateOf(false) }',
    '  LaunchedEffect(movie.id) { loadImage(movie) }',
    '}'
  ]);
  add('snapshot', [
    'var count by mutableStateOf(0)',
    '@Composable fun Counter() {',
    c('  Text("Count: $count")     // đọc → scope được ghi nhận là phụ thuộc', '  Text("Count: $count")     // read → the scope is recorded as dependent'),
    '}',
    'val snap = Snapshot.takeMutableSnapshot()',
    c('snap.enter { count = 1 }    // chỉ thấy bên trong snapshot', 'snap.enter { count = 1 }    // visible only inside the snapshot'),
    c('snap.apply(); snap.dispose() // áp dụng nguyên tử vào global', 'snap.apply(); snap.dispose() // applied atomically to global'),
    c('count = 1                   // hoặc ghi thẳng (global snapshot)', 'count = 1                   // or write directly (global snapshot)')
  ]);
  add('recomposer', [
    c('// frame clock (minh họa)', '// frame clock (illustrative)'),
    'withFrameNanos { frameTimeNanos ->',
    c('  // việc cần thời điểm frame, ví dụ animation', '  // work that needs the frame time, e.g. an animation'),
    '}',
    c('recomposer.runRecomposeAndApplyChanges() // suspend: chờ, recompose, apply', 'recomposer.runRecomposeAndApplyChanges() // suspend: await, recompose, apply')
  ]);
  add('applier', [
    c('interface Applier<N> {        // trích lược', 'interface Applier<N> {        // abridged'),
    '  fun onBeginChanges() {}',
    '  fun insertTopDown(index: Int, instance: N)',
    '  fun insertBottomUp(index: Int, instance: N)',
    '  fun remove(index: Int, count: Int)',
    '  fun move(from: Int, to: Int, count: Int)',
    '  fun apply(block: N.(Any?) -> Unit, value: Any?)',
    '  fun onEndChanges() {}',
    '}'
  ]);
  add('phases', [
    'var value by remember { mutableStateOf(0) }',
    c('// 1) đọc trong composition', '// 1) read during composition'),
    'Text("Value: $value")',
    c('// 2) đọc trong layout (bước đặt vị trí)', '// 2) read during layout (placement)'),
    'Box(Modifier.offset { IntOffset(value, 0) })',
    c('// 3) đọc trong draw', '// 3) read during drawing'),
    'Box(Modifier.drawBehind { drawRect(colorFor(value)) })',
    c('// vòng lặp phase (không nên làm):', '// phase loop (avoid this):'),
    'Text("x", Modifier.onSizeChanged { h = it.height })',
    'Box(Modifier.padding(top = h.toDp()))'
  ]);
  add('skip', [
    '@Composable fun Parent(tick: Int) {',
    '  Text("tick $tick")',
    '  Child(data)',
    '}',
    c('data class Tag(val name: String)           // stable: val, kiểu stable', 'data class Tag(val name: String)           // stable: val of a stable type'),
    c('class Tags(var items: MutableList<String>) // unstable', 'class Tags(var items: MutableList<String>) // unstable'),
    '@Composable fun Child(data: Any) { /* ... */ }'
  ]);
  add('semantics', [
    c('Button(onClick = { }) {        // gộp con cháu', 'Button(onClick = { }) {        // merges descendants'),
    '  Icon(Icons.Default.Add, contentDescription = "Add")',
    '  Text("+1")',
    '}',
    c('// không gộp:', '// not merged:'),
    'Row(Modifier.semantics { }) { Icon(...); Text("+1") }'
  ]);
  add('counter', [
    '@Composable fun CounterScreen() {',
    '  var count by remember { mutableStateOf(0) }',
    '  Column {',
    '    Text("Count: $count")',
    '    if (count > 0) Text("Started!")',
    c('    Header(title = "Counter")   // hoặc Header(tags = listOf("a"))', '    Header(title = "Counter")   // or Header(tags = listOf("a"))'),
    '    Button(onClick = { count++ }) { Text("+1") }',
    '  }',
    '}'
  ]);
  [['runsBody', true, true], ['runsBodyAnim', true, true], ['runsCb', false, false], ['runsCbAnim', false, true]].forEach(function (c) {
    var body = c[1], anim = /Anim$/.test(c[0]);
    add(c[0], [
      { vi: 'var sentCount = 0                       // biến dùng chung bên ngoài (ví dụ bộ đếm analytics)', en: 'var sentCount = 0                       // shared state outside (e.g. an analytics counter)' },
      '@Composable',
      'fun Counter(count: Int, onIncrement: () -> Unit) {',
      body ? { vi: '    sentCount++                          // ✗ side effect TRONG THÂN', en: '    sentCount++                          // ✗ a side effect IN THE BODY' } : { vi: '    // thân chỉ mô tả UI, không ghi gì ra ngoài', en: '    // the body only describes UI, writes nothing outside' },
      anim ? '    val scale by animateFloatAsState(if (count % 2 == 0) 1f else 1.2f)' : { vi: '    val scale = 1f                        // (không có animation)', en: '    val scale = 1f                        // (no animation)' },
      '    Button(',
      body ? '        onClick = { onIncrement() },' : { vi: '        onClick = { sentCount++; onIncrement() },   // ✓ side effect trong callback', en: '        onClick = { sentCount++; onIncrement() },   // ✓ the side effect in a callback' },
      anim ? { vi: '        modifier = Modifier.scale(scale)     // đọc giá trị animation ngay trong composition', en: '        modifier = Modifier.scale(scale)     // reads the animated value during composition' } : '        modifier = Modifier.scale(scale)',
      '    ) { Text("Count: $count") }',
      '}'
    ]);
  });
})();
