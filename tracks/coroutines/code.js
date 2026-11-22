/* Đoạn mã dùng chung cho cả hai ngôn ngữ. Tất cả là minh họa (illustrative): không phải mã mà mô phỏng chạy.
   Tên biến bằng tiếng Anh, comment tối thiểu. Số dòng được tham chiếu bởi codeHighlight trong các model. */
(function () {
  var add = function (id, lines) { ADE.addCode('coroutines', id, { lang: 'kotlin', illustrative: true, lines: lines }); };
  add('seq', [
    'val seq = sequence {',
    '    println("Generating first")',
    '    yield(1)',
    '    println("Generating second")',
    '    yield(2)',
    '    println("Generating third")',
    '    yield(3)',
    '    println("Done")',
    '}',
    '',
    'fun main() {',
    '    val iterator = seq.iterator()',
    '    println("Starting")',
    '    val first = iterator.next()',
    '    println("First: $first")',
    '    val second = iterator.next()',
    '    println("Second: $second")',
    { vi: '    val third = iterator.next()     // chỉ khi bật "gọi tới hết"', en: '    val third = iterator.next()     // only with "call to the end"' },
    '    println("Third: $third")',
    '    println(iterator.hasNext())',
    '}'
  ]);
  add('seqList', [
    'fun main() {',
    { vi: '    val list = buildList {          // chạy HẾT khối ngay tại đây', en: '    val list = buildList {          // runs the WHOLE block right here' },
    '        println("Generating first")',
    '        add(1)',
    '        println("Generating second")',
    '        add(2)',
    '        println("Generating third")',
    '        add(3)',
    '        println("Done")',
    '    }                                // [1, 2, 3]',
    '    val iterator = list.iterator()',
    '    println("Starting")',
    '    println("First: ${iterator.next()}")',
    '    println("Second: ${iterator.next()}")',
    '}'
  ]);
  add('full', [
    'Button(onClick = { viewModel.load() })',
    '',
    'class ArticlesViewModel(private val repo: Repo) : ViewModel() {',
    '  fun load() {',
    '    viewModelScope.launch {',
    '      _state.value = repo.fetch()',
    '    }',
    '  }',
    '}',
    '',
    'val state by vm.state.collectAsStateWithLifecycle()'
  ]);
  add('suspend', [
    'launch { // A',
    '  work(10)',
    '  delay(30)            // hoặc Thread.sleep(30)',
    '  work(10)',
    '}',
    '',
    'launch { // B',
    '  work(20)',
    '}'
  ]);
  add('jobtree', [
    'coroutineScope {          // hoặc supervisorScope',
    '  val c1 = launch { ... }',
    '  val c2 = launch { launch { ... } }',
    '  val c3 = launch { ... }',
    '}',
    'c1.cancel()',
    'launch { throw IllegalStateException() }',
    '// scope đợi mọi con rồi mới kết thúc'
  ]);
  add('builders', [
    'coroutineScope {',
    '  val profile = async { loadProfile() }',
    '  val settings = async { loadSettings() }',
    '  profile.await() to settings.await()',
    '}'
  ]);
  add('context', [
    'scope.launch(Dispatchers.Main + CoroutineName("load")) {',
    '  val input = readInput()',
    '  val data = withContext(Dispatchers.IO) {',
    '    heavyWork()',
    '  }',
    '  show(data)',
    '}'
  ]);
  add('cancel', [
    'val job = launch {',
    '  repeat(5) {',
    '    doUnitOfWork()',
    '    ensureActive()',
    '  }',
    '}',
    'try { ... } finally {',
    '  withContext(NonCancellable) { cleanup() }',
    '}',
    '// job.cancel() / withTimeout(250) { ... }'
  ]);
  add('exception', [
    'val handler = CoroutineExceptionHandler { _, e -> log(e) }',
    'scope.launch(handler) {',
    '  launch { throw IOException() }',
    '  launch { work() }',
    '}',
    'try { deferred.await() } catch (e: IOException) { ... }'
  ]);
  add('flowpipe', [
    'flow { repeat(5) { emit(it + 1); delay(100) } }',
    '  .map { it * 10 }',
    '  .buffer(2)          // hoặc .conflate()',
    '  .collect { slowWork(it) }',
    '// hoặc .collectLatest { slowWork(it) }'
  ]);
  add('hotcold', [
    'val cold = flow { emit(1); emit(2); emit(3) }',
    'cold.collect { ... }              // mỗi collector chạy lại',
    'val state = MutableStateFlow(0)',
    'val shared = MutableSharedFlow<Int>(replay = 1)',
    'val channel = Channel<Int>()'
  ]);
  add('lifecycle', [
    'lifecycleOwner.lifecycle.repeatOnLifecycle(Lifecycle.State.STARTED) {',
    '  flow.collect { render(it) }',
    '}',
    '',
    '',
    'class VM : ViewModel() {',
    '  init { viewModelScope.launch { flow.collect { ... } } }',
    '}',
    'scope.launch { flow.collect { render(it) } }',
    '// collect trực tiếp trong scope của màn hình'
  ]);
  add('effects', [
    'LaunchedEffect(key) {',
    '  collectSomething()',
    '}',
    'val scope = rememberCoroutineScope()',
    'Button(onClick = { scope.launch { save() } }) { ... }',
    ''
  ]);
  add('race', [
    'var counter = 0',
    'launch { repeat(3) { counter++ } }  // đọc → +1 → ghi',
    'mutex.withLock { counter++ }',
    '',
    '',
    'withContext(singleThread) { counter++ }',
    'val atomic = AtomicInteger(); atomic.incrementAndGet()'
  ]);
  add('vtime', [
    'runTest {',
    '  launch { delay(1000); a() }',
    '  launch { delay(2500); b() }',
    '  advanceTimeBy(1500)',
    '  advanceUntilIdle()',
    '  runCurrent()',
    '  assertEquals(...)',
    '}'
  ]);
})();
