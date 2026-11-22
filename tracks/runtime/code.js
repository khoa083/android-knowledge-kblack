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
  [['grp', false], ['grpHypo', true]].forEach(function (c) {
    var hypo = c[1];
    add(c[0], [
      { vi: '// mã giả theo how-compose-works.md (tên hàm theo tài liệu); mã compiler thật khác', en: '// pseudo-code after how-compose-works.md (doc names); real compiler output differs' },
      'fun B(person: Person, $composer: Composer) {',
      '  $composer.startRestartGroup(4567)',
      hypo ? { vi: '  // ✗ GIẢ ĐỊNH: bỏ "val changed", gọi changed() trong điều kiện', en: '  // ✗ HYPOTHETICAL: no "val changed", changed() inside the condition' } : '  val changed = $composer.changed(person)',
      hypo ? '  if (!$composer.skipping || $composer.changed(person)) {' : '  if (changed || !$composer.skipping) {',
      '    A(person.givenName, $composer)',
      '    A(person.familyName, $composer)',
      '  } else {',
      '    $composer.skipToEndGroup()',
      '  }',
      '  $composer.endRestartGroup()?.updateScope { c -> B(person, c) }',
      '}',
      'fun A(text: String, $composer: Composer) {',
      '  $composer.startGroup(1234)',
      '  val data = remember($composer) { Data() }',
      '  val changed = $composer.changed(text)',
      '  if (changed || !$composer.skipping) Text(text, $composer)',
      '  else $composer.skipToEndGroup()',
      '  $composer.endGroup()',
      '}'
    ]);
  });
  add('structPerson', [
    '@Composable',
    'fun ShowPerson(person: Person) {',
    '  Column {',
    '    ShowName(person.name)',
    '    if (person.employed) {',
    '      ShowCompany(person.employer)',
    '    }',
    '    ShowEmail(person.email)',
    '  }',
    '}'
  ]);
  add('structMove', [
    { vi: '// thực tế chỉ key() tạo ra di chuyển; tài liệu dùng chuỗi group đảo thứ tự để minh họa', en: '// in practice only key() produces moves; the document reverses the group order to illustrate' },
    '@Composable',
    'fun Fields(order: List<Field>) {   // [Email, Company, Name]',
    '  Column {',
    '    for (f in order) key(f) { ShowField(f) }',
    '  }',
    '}'
  ]);
  [['structCounters', true], ['structCountersNo', false]].forEach(function (c) {
    add(c[0], [
      '@Composable',
      'fun Counters(showMiddle: Boolean) {',
      { vi: '  Counter()                 // count = 1', en: '  Counter()                 // count = 1' },
      c[1] ? { vi: '  if (showMiddle) {         // compiler bọc if trong một group', en: '  if (showMiddle) {         // the compiler wraps the if in a group' } : { vi: '  if (showMiddle) {         // GIẢ ĐỊNH: không có group quanh if', en: '  if (showMiddle) {         // HYPOTHETICAL: no group around the if' },
      { vi: '    Counter()               // count = 5', en: '    Counter()               // count = 5' },
      '  }',
      { vi: '  Counter()                 // count = 9', en: '  Counter()                 // count = 9' },
      '}'
    ]);
  });
  [['recPlus', true], ['recSet', false]].forEach(function (c) {
    add(c[0], [
      { vi: 'val count = mutableStateOf(0, policy)       // policy: structuralEqualityPolicy() hoặc counterPolicy()', en: 'val count = mutableStateOf(0, policy)       // policy: structuralEqualityPolicy() or counterPolicy()' },
      'val a = Snapshot.takeMutableSnapshot()',
      'val b = Snapshot.takeMutableSnapshot()',
      'a.enter { count.value += 10 }',
      c[1] ? 'b.enter { count.value += 20 }' : 'b.enter { count.value = 10 }',
      'val ra = a.apply()                          // Success',
      { vi: 'val rb = b.apply()                          // Success hoặc Failure (xung đột)', en: 'val rb = b.apply()                          // Success or Failure (conflict)' },
      'a.dispose(); b.dispose()'
    ]);
  });
  add('surviveCode', [
    { vi: '// năm nơi giữ cùng một chữ "Ana" người dùng gõ', en: '// five places holding the same "Ana" the user typed' },
    'var a by remember { mutableStateOf("") }',
    'var b by rememberSaveable { mutableStateOf("") }',
    { vi: 'val c by vm.draft.collectAsStateWithLifecycle()          // StateFlow trong ViewModel', en: 'val c by vm.draft.collectAsStateWithLifecycle()          // a StateFlow in the ViewModel' },
    { vi: 'val d by vm.savedDraft.collectAsStateWithLifecycle()     // savedStateHandle.getStateFlow("draft", "")', en: 'val d by vm.savedDraft.collectAsStateWithLifecycle()     // savedStateHandle.getStateFlow("draft", "")' },
    { vi: 'val e by vm.storedDraft.collectAsStateWithLifecycle()    // đọc từ DataStore/Room', en: 'val e by vm.storedDraft.collectAsStateWithLifecycle()    // read from DataStore/Room' }
  ]);
  add('frameLoop', [
    { vi: '// rút gọn từ Recomposer.runRecomposeAndApplyChanges() @296313a4', en: '// condensed from Recomposer.runRecomposeAndApplyChanges() @296313a4' },
    { vi: 'while (shouldKeepRecomposing) { awaitWorkAvailable()            // treo khi không có việc', en: 'while (shouldKeepRecomposing) { awaitWorkAvailable()            // suspended while idle' },
    { vi: '  if (!recordComposerModifications()) continue                  // không có việc theo frame', en: '  if (!recordComposerModifications()) continue                  // no frame work' },
    { vi: '  parentFrameClock.withFrameNanos { frameTime ->                // Android: Choreographer', en: '  parentFrameClock.withFrameNanos { frameTime ->                // Android: Choreographer' },
    '    if (hasBroadcastFrameClockAwaiters) {',
    { vi: '      broadcastFrameClock.sendFrame(frameTime)                  // animation, withFrameNanos trong effect', en: '      broadcastFrameClock.sendFrame(frameTime)                  // animations, withFrameNanos in effects' },
    '      Snapshot.sendApplyNotifications()',
    '    }',
    { vi: '    recordComposerModifications(); /* recompose các composition bị invalidate */', en: '    recordComposerModifications(); /* recompose invalidated compositions */' },
    '    /* composition.applyChanges() */',
    '  }',
    '}'
  ]);
  add('frameAnim', [
    'LaunchedEffect(Unit) {',
    { vi: '  val start = withFrameNanos { it }                 // chờ frame đầu', en: '  val start = withFrameNanos { it }                 // wait for the first frame' },
    '  while (true) {',
    { vi: '    val t = withFrameNanos { it }                   // chạy trong frame của Recomposer', en: '    val t = withFrameNanos { it }                   // runs inside the Recomposer\'s frame' },
    { vi: '    offset = (t - start) / 1_000_000f * speed       // ghi state', en: '    offset = (t - start) / 1_000_000f * speed       // a state write' },
    '    if (offset >= target) break',
    '  }',
    '}'
  ]);
  add('effCounter', [
    { vi: '// biến thể LaunchedEffectDemo của Kunneth (Ch.7): thêm DisposableEffect và SideEffect cùng chỗ', en: '// a variant of Kunneth\'s LaunchedEffectDemo (Ch.7): DisposableEffect and SideEffect added alongside' },
    'var clickCount by rememberSaveable { mutableStateOf(0) }',
    'var counter by rememberSaveable { mutableStateOf(0) }',
    { vi: 'Button(onClick = { clickCount += 1 }) { Text("Start / Restart") }', en: 'Button(onClick = { clickCount += 1 }) { Text("Start / Restart") }' },
    'Button(onClick = { clickCount = 0 }) { Text("Stop") }',
    { vi: 'if (clickCount > 0) {                          // nhánh rời composition khi Stop', en: 'if (clickCount > 0) {                          // the branch leaves composition on Stop' },
    '    DisposableEffect(clickCount) {',
    '        println("init $clickCount")',
    '        onDispose { println("dispose $clickCount") }',
    '    }',
    '    LaunchedEffect(clickCount) {',
    { vi: '        counter = 0                            // coroutine mới bắt đầu lại từ 0', en: '        counter = 0                            // a new coroutine starts again from 0' },
    '        while (isActive) {',
    '            counter += 1; delay(1000)',
    '        }',
    '    }',
    '}',
    { vi: 'SideEffect { analytics.setUserProperty("counter", counter) }   // sau mỗi lượt recompose thành công', en: 'SideEffect { analytics.setUserProperty("counter", counter) }   // after every successful recomposition' }
  ]);
  add('effStale', [
    '@Composable',
    'fun LandingScreen(onTimeout: () -> Unit) {',
    '    LaunchedEffect(true) {',
    '        delay(3000)',
    { vi: '        onTimeout()            // ✗ lambda bị bắt lúc launch, có thể đã cũ', en: '        onTimeout()            // ✗ the lambda captured at launch, possibly stale' },
    '    }',
    '}'
  ]);
  add('effUpdated', [
    '@Composable',
    'fun LandingScreen(onTimeout: () -> Unit) {',
    { vi: '    val currentOnTimeout by rememberUpdatedState(onTimeout)   // luôn là lambda mới nhất', en: '    val currentOnTimeout by rememberUpdatedState(onTimeout)   // always the latest lambda' },
    '    LaunchedEffect(true) {',
    '        delay(3000)',
    '        currentOnTimeout()     // ✓',
    '    }',
    '}'
  ]);
  [['localsDyn', false], ['localsStatic', true]].forEach(function (c) {
    add(c[0], [
      c[1] ? 'val LocalColor = staticCompositionLocalOf { Peach }' : 'val LocalColor = compositionLocalOf { Peach }',
      '@Composable fun C1() {',
      '    var dark by remember { mutableStateOf(false) }',
      '    Switch(checked = dark, onCheckedChange = { dark = it })',
      '    C2()                                                   // C2 → C4 → C6',
      '    CompositionLocalProvider(LocalColor provides if (dark) Brown else Peach) {',
      '        C3()                                               // C3 → C5 → C7, C8',
      '    }',
      '}',
      '@Composable fun C8() { Text("8", Modifier.background(LocalColor.current)) }',
      { vi: '@Composable fun C6() { Text("6", Modifier.background(LocalColor.current)) }   // nhánh khác: giá trị mặc định', en: '@Composable fun C6() { Text("6", Modifier.background(LocalColor.current)) }   // other branch: the default' }
    ]);
  });
  add('insertOrder', [
    { vi: '// Applier<N> (rút gọn, @296313a4): chèn ở MỘT trong hai hàm, không phải cả hai', en: '// Applier<N> (condensed, @296313a4): insert in ONE of the two functions, not both' },
    'interface Applier<N> { val current: N; fun down(node: N); fun up()',
    { vi: '  fun insertTopDown(index: Int, instance: N)    // gọi TRƯỚC khi con của instance được tạo', en: '  fun insertTopDown(index: Int, instance: N)    // called BEFORE instance\'s children are created' },
    { vi: '  fun insertBottomUp(index: Int, instance: N)   // gọi SAU khi mọi con đã được chèn vào nó', en: '  fun insertBottomUp(index: Int, instance: N)   // called AFTER all children are inserted into it' },
    '  fun remove(index: Int, count: Int); fun move(from: Int, to: Int, count: Int); fun clear() }',
    { vi: '// Compose UI trên Android:', en: '// Compose UI on Android:' },
    'internal class UiApplier(root: LayoutNode) : AbstractApplier<LayoutNode>(root) {',
    { vi: '  override fun insertTopDown(index: Int, instance: LayoutNode) { /* bỏ qua */ }', en: '  override fun insertTopDown(index: Int, instance: LayoutNode) { /* ignored */ }' },
    '  override fun insertBottomUp(index: Int, instance: LayoutNode) { current.insertAt(index, instance) }',
    '}'
  ]);
  var scrollHead = ['Box {', '    val listState = rememberLazyListState()'];
  add('scroll_comp', scrollHead.concat([
    '    Image(painter, null, Modifier.offset(',
    { vi: '        with(LocalDensity.current) {                       // ✗ đọc trong COMPOSITION', en: '        with(LocalDensity.current) {                       // ✗ read in COMPOSITION' },
    '            (listState.firstVisibleItemScrollOffset / 2).toDp() }',
    '    ))',
    '    LazyColumn(state = listState) { /* … */ }',
    '}'
  ]));
  add('scroll_layout', scrollHead.concat([
    '    Image(painter, null, Modifier.offset {',
    { vi: '        // ✓ lambda chạy ở bước PLACEMENT của layout', en: '        // ✓ the lambda runs in the PLACEMENT step of layout' },
    '        IntOffset(x = 0, y = listState.firstVisibleItemScrollOffset / 2)',
    '    })',
    '    LazyColumn(state = listState) { /* … */ }',
    '}'
  ]));
  add('scroll_draw', scrollHead.concat([
    '    Box(Modifier.fillMaxWidth().height(4.dp).drawBehind {',
    { vi: '        // ✓ đọc trong DRAW: thanh tiến độ cuộn', en: '        // ✓ read in DRAW: a scroll progress bar' },
    '        drawRect(Teal, size = size.copy(width = listState.firstVisibleItemScrollOffset.toFloat()))',
    '    })',
    '    LazyColumn(state = listState) { /* … */ }',
    '}'
  ]));
  add('scroll_loop', [
    'Box {',
    '    var imageHeightPx by remember { mutableIntStateOf(0) }',
    '    Image(',
    '        painter = painterResource(R.drawable.rectangle),',
    '        contentDescription = null,',
    '        modifier = Modifier.fillMaxWidth()',
    { vi: '            .onSizeChanged { size ->                      // ✗ đừng làm vậy', en: '            .onSizeChanged { size ->                      // ✗ don\'t do this' },
    '                imageHeightPx = size.height }',
    '    )',
    '    Text(',
    '        text = "I\'m below the image",',
    '        modifier = Modifier.padding(',
    '            top = with(LocalDensity.current) { imageHeightPx.toDp() })',
    '    )',
    '}'
  ]);
  add('measure_column', [
    '@Composable',
    'fun MyBasicColumn(modifier: Modifier = Modifier, content: @Composable () -> Unit) {',
    '    Layout(modifier = modifier, content = content) { measurables, constraints ->',
    { vi: '        val placeables = measurables.map { it.measure(constraints) }   // 1. đo mỗi con MỘT lần', en: '        val placeables = measurables.map { it.measure(constraints) }   // 1. measure each child ONCE' },
    { vi: '        layout(constraints.maxWidth, constraints.maxHeight) {        // 2. kích thước của chính nó', en: '        layout(constraints.maxWidth, constraints.maxHeight) {        // 2. its own size' },
    '            var yPosition = 0',
    '            placeables.forEach { placeable ->',
    { vi: '                placeable.placeRelative(x = 0, y = yPosition)         // 3. đặt con', en: '                placeable.placeRelative(x = 0, y = yPosition)         // 3. place the children' },
    '                yPosition += placeable.height',
    '            }',
    '        }',
    '    }',
    '}'
  ]);
  add('measure_twice', [
    'Layout(content = content) { measurables, constraints ->',
    '    val first = measurables[0].measure(constraints)',
    { vi: '    // ✗ "đo thử" lần nữa với constraints khác', en: '    // ✗ a second "trial" measurement with other constraints' },
    '    val again = measurables[0].measure(constraints.copy(maxWidth = first.width / 2))',
    '    layout(first.width, first.height) { again.placeRelative(0, 0) }',
    '}   // IllegalStateException: measure() may not be called multiple times on the same Measurable…'
  ]);
  [['measure_nointr', 'Row(modifier = modifier) {'], ['measure_intr', { vi: 'Row(modifier = modifier.height(IntrinsicSize.Min)) {   // ✓ hỏi intrinsic trước', en: 'Row(modifier = modifier.height(IntrinsicSize.Min)) {   // ✓ ask intrinsics first' }]].forEach(function (c) {
    add(c[0], [
      '@Composable',
      'fun TwoTexts(text1: String, text2: String, modifier: Modifier = Modifier) {',
      typeof c[1] === 'string' ? '    ' + c[1] : { vi: '    ' + c[1].vi, en: '    ' + c[1].en },
      '        Text(text1, Modifier.weight(1f).padding(start = 4.dp).wrapContentWidth(Alignment.Start))',
      '        VerticalDivider(color = Color.Black, modifier = Modifier.fillMaxHeight().width(1.dp))',
      '        Text(text2, Modifier.weight(1f).padding(end = 4.dp).wrapContentWidth(Alignment.End))',
      '    }',
      '}'
    ]);
  });
  add('chain_reuse', [
    '@Composable',
    { vi: 'fun Dot(color: Color, label: String) {          // chạy lại: tạo chuỗi element MỚI', en: 'fun Dot(color: Color, label: String) {          // re-runs: builds a NEW element chain' },
    '    Box(',
    '        Modifier',
    '            .padding(8.dp)                       // PaddingElement',
    '            .clip(CircleShape)',
    '            .background(color)                   // BackgroundElement(color, …)',
    '            .size(40.dp)',
    '    ) { Text(label) }',
    '}'
  ]);
  [['chain_insert', 'Modifier'], ['chain_replace', 'Modifier.shadow(4.dp)']].forEach(function (c) {
    add(c[0], [
      '@Composable',
      'fun Dot(color: Color, selected: Boolean) {',
      '    Box(',
      '        Modifier',
      '            .padding(8.dp)',
      '            .then(if (selected) Modifier.border(2.dp, Color.Black) else ' + c[1] + ')',
      '            .background(color)',
      '            .size(40.dp)',
      '    )',
      '}'
    ]);
  });
  add('lazy_same', [
    'LazyColumn {',
    '    items(messages, key = { it.id }) { message ->',
    '        MessageRow(message)',
    '    }',
    '}'
  ]);
  add('lazy_types', [
    'LazyColumn {',
    '    items(',
    '        elements,',
    '        key = { it.id },',
    { vi: '        contentType = { it.type }          // "text" hoặc "image"', en: '        contentType = { it.type }          // "text" or "image"' },
    '    ) { e ->',
    '        if (e.type == "image") ImageRow(e) else TextRow(e)',
    '    }',
    '}'
  ]);
  add('lazy_column', [
    'Column(Modifier.verticalScroll(rememberScrollState())) {',
    { vi: '    messages.forEach { message ->          // ✗ compose CẢ 20 mục ngay từ đầu', en: '    messages.forEach { message ->          // ✗ composes ALL 20 items up front' },
    '        MessageRow(message)',
    '    }',
    '}'
  ]);
})();
