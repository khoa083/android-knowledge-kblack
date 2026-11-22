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
  add('contNever', ['suspend fun main() {', '    println("Before")', '    suspendCoroutine<Unit> { continuation ->', '        println("Before too")', '    }', '    println("After")', '}']);
  add('contNow', ['suspend fun main() {', '    println("Before")', '    suspendCoroutine<Unit> { continuation ->', '        continuation.resume(Unit)', '    }', '    println("After")', '}']);
  add('contThread', ['suspend fun main() {', '    println("Before")', '    suspendCoroutine<Unit> { continuation ->', '        thread {', '            println("Suspended")', '            Thread.sleep(1000)', '            continuation.resume(Unit)', '            println("Resumed")', '        }', '    }', '    println("After")', '}']);
  add('contSched', ['private val executor = Executors.newSingleThreadScheduledExecutor {', '    Thread(it, "scheduler").apply { isDaemon = true }', '}', '', 'suspend fun delay(timeMillis: Long): Unit =', '    suspendCoroutine { cont ->', '        executor.schedule({ cont.resume(Unit) }, timeMillis, TimeUnit.MILLISECONDS)', '    }', '', 'suspend fun main() {', '    println("Before")', '    delay(1000)', '    println("After")', '}']);
  add('contExc', ['class MyException : Throwable("Just an exception")', '', 'suspend fun main() {', '    try {', '        suspendCoroutine<Unit> { cont ->', '            cont.resumeWithException(MyException())', '        }', '    } catch (e: MyException) {', '        println("Caught!")', '    }', '}']);
  add('smUser', [
    'fun printUser(token: String, continuation: Continuation<*>): Any {',
    '    val cont = continuation as? PrintUserContinuation',
    '        ?: PrintUserContinuation(continuation, token)',
    '    var result = cont.result',
    '    var userId = cont.userId',
    '    if (cont.label == 0) {',
    '        println("Before")',
    '        cont.label = 1',
    '        val res = getUserId(token, cont)',
    '        if (res == COROUTINE_SUSPENDED) return COROUTINE_SUSPENDED',
    '        result = Result.success(res)',
    '    }',
    '    if (cont.label == 1) {',
    '        userId = result!!.getOrThrow() as String',
    '        println("Got userId: $userId")',
    '        cont.label = 2',
    '        cont.userId = userId',
    '        val res = getUserName(userId, cont)',
    '        if (res == COROUTINE_SUSPENDED) return COROUTINE_SUSPENDED',
    '        result = Result.success(res)',
    '    }',
    '    if (cont.label == 2) {',
    '        val userName = result!!.getOrThrow() as String',
    '        println(User(userId as String, userName))',
    '        println("After")',
    '        return Unit',
    '    }',
    '    error("Impossible")',
    '}'
  ]);
  add('jobState', [
    'val parent = scope.launch(start = if (lazy) CoroutineStart.LAZY else CoroutineStart.DEFAULT) {',
    { vi: '    launch {                       // con', en: '    launch {                       // child' },
    '        try { work() }',
    { vi: '        finally { cleanup() }      // luôn chạy, kể cả khi bị hủy', en: '        finally { cleanup() }      // always runs, also when cancelled' },
    '    }',
    { vi: '    // thân của cha chạy xong ở đây → Completing (chờ con)', en: '    // the parent body ends here → Completing (waits for children)' },
    '}',
    { vi: 'parent.start()                     // chỉ cần khi lazy: New → Active', en: 'parent.start()                     // only needed when lazy: New → Active' },
    { vi: 'parent.cancel()                    // → Cancelling → Cancelled', en: 'parent.cancel()                    // → Cancelling → Cancelled' },
    { vi: 'parent.join()                      // chờ trạng thái cuối', en: 'parent.join()                      // wait for a final state' }
  ]);
  add('chanCap', [
    'suspend fun main(): Unit = coroutineScope {',
    { vi: '    val channel = produce(capacity = CAP) {   // CAP: RENDEZVOUS | 3 | UNLIMITED | CONFLATED | (2, DROP_OLDEST)', en: '    val channel = produce(capacity = CAP) {   // CAP: RENDEZVOUS | 3 | UNLIMITED | CONFLATED | (2, DROP_OLDEST)' },
    '        repeat(5) { index ->',
    '            send(index * 2)',
    '            delay(100)',
    '            println("Sent")',
    '        }',
    { vi: '    }                                          // produce đóng channel khi khối kết thúc', en: '    }                                          // produce closes the channel when the block ends' },
    '    delay(1000)',
    '    for (element in channel) {',
    '        println(element)',
    '        delay(1000)',
    '    }',
    '}'
  ]);
  add('flowCall', [
    'fun <T> flowOf(vararg elements: T): Flow<T> = flow {',
    '    for (element in elements) emit(element)',
    '}',
    '',
    'fun <T, R> Flow<T>.map(transform: suspend (T) -> R): Flow<R> = flow {',
    { vi: '    collect { value ->                 // collect flow phía trên', en: '    collect { value ->                 // collect the upstream flow' },
    { vi: '        emit(transform(value))         // phát xuống phía dưới', en: '        emit(transform(value))         // emit downstream' },
    '    }',
    '}',
    'flowOf("A", "B", "C").map { it.lowercase() }',
    { vi: '    .collect { println(it) }           // terminal: khởi động mọi thứ', en: '    .collect { println(it) }           // terminal: starts everything' },
    { vi: '// collect chỉ trả về khi builder chạy xong', en: '// collect returns only when the builder has finished' }
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
