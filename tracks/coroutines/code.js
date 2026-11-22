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
  add('pagingFlow', [
    'fun allUsersFlow(api: UserApi): Flow<User> = flow {',
    '    var page = 0',
    '    do {',
    '        val users = api.takePage(page++)      // 1000 ms',
    '        emitAll(users.asFlow())',
    '    } while (!users.isNullOrEmpty())',
    '}',
    '',
    'val user = allUsersFlow(api).first {',
    { vi: '    delay(1000); it.name == "User3"         // kiểm mỗi user 1000 ms', en: '    delay(1000); it.name == "User3"         // checking each user takes 1000 ms' },
    { vi: '}                                          // first hủy flow khi tìm thấy', en: '}                                          // first cancels the flow once found' }
  ]);
  add('pagingCh', [
    'fun allUsersFlow(api: UserApi): Flow<User> = channelFlow {',
    '    var page = 0',
    '    do {',
    { vi: '        val users = api.takePage(page++)      // 1000 ms, chạy song song với consumer', en: '        val users = api.takePage(page++)      // 1000 ms, runs concurrently with the consumer' },
    '        users.forEach { send(it) }',
    '    } while (!users.isNullOrEmpty())',
    '}',
    '',
    'val user = allUsersFlow(api).first {',
    '    delay(1000); it.name == "User3"',
    '}'
  ]);
  var CB = { cbMerge: ['merge(flow1, flow2)', '    .collect { println(it) }'], cbZip: ['flow1.zip(flow2) { a, b -> "${a}_$b" }', '    .collect { println(it) }'], cbCombine: ['flow1.combine(flow2) { a, b -> "${a}_$b" }', '    .collect { println(it) }'] };
  Object.keys(CB).forEach(function (id) {
    add(id, ['val flow1 = flowOf("A", "B", "C").onEach { delay(400) }', 'val flow2 = flowOf(1, 2, 3, 4).onEach { delay(1000) }', ''].concat(CB[id]));
  });
  var FM = { fmConcat: ['    .flatMapConcat { flowFrom(it) }'], fmMerge: ['    .flatMapMerge { flowFrom(it) }          // concurrency mặc định 16'], fmMerge2: ['    .flatMapMerge(concurrency = 2) { flowFrom(it) }'],
    fmLatest: [{ vi: '    .onEach { delay(1200) }               // phần tử ngoài đến cách nhau 1,2 giây', en: '    .onEach { delay(1200) }               // outer elements arrive 1.2 seconds apart' }, '    .flatMapLatest { flowFrom(it) }'] };
  FM.fmMerge[0] = { vi: '    .flatMapMerge { flowFrom(it) }          // concurrency mặc định 16', en: '    .flatMapMerge { flowFrom(it) }          // default concurrency 16' };
  Object.keys(FM).forEach(function (id) {
    add(id, ['fun flowFrom(elem: String) = flowOf(1, 2, 3)', '    .onEach { delay(1000) }', '    .map { "${it}_$elem" }', '', 'flowOf("A", "B", "C")'].concat(FM[id], ['    .collect { println(it) }']));
  });
  var SI = { siEager: 'SharingStarted.Eagerly', siLazy: 'SharingStarted.Lazily', siWs: 'SharingStarted.WhileSubscribed()', siWs5: 'SharingStarted.WhileSubscribed(5_000)' };
  Object.keys(SI).forEach(function (id) {
    add(id, ['val ticks = flow { var n = 0; while (true) { delay(1000); emit(++n) } }', '    .onStart { println("Started") }', '    .onCompletion { println("Finished") }',
      '    .shareIn(scope, ' + SI[id] + ', replay = 1)', '',
      { vi: 'ticks.collect { render(it) }   // màn hình vào 1,2 s; xoay 3,6 s; vào lại 4,3 s; ra nền 6,6 s; quay lại 12,4 s', en: 'ticks.collect { render(it) }   // screen enters 1.2 s; rotates 3.6 s; re-enters 4.3 s; backgrounded 6.6 s; returns 12.4 s' }]);
  });
  add('lsScope', [
    'class NotificationsSender(',
    '    private val client: NotificationsClient,',
    '    private val notificationScope: CoroutineScope,   // CoroutineScope(SupervisorJob() + handler)',
    ') {',
    '    fun sendNotifications(notifications: List<Notification>) {',
    '        for (n in notifications) notificationScope.launch { client.send(n) }',
    '    }',
    '}',
    { vi: 'val handler = CoroutineExceptionHandler { _, e -> log(e) }   // KHÔNG có handler: Android crash app', en: 'val handler = CoroutineExceptionHandler { _, e -> log(e) }   // WITHOUT a handler: Android crashes the app' },
    { vi: 'viewModelScope.launch { sender.sendNotifications(listOf(n1, n2, n3)); println("Tiếp tục") }', en: 'viewModelScope.launch { sender.sendNotifications(listOf(n1, n2, n3)); println("Continue") }' }
  ]);
  add('lsSusp', [
    'class NotificationsSender(',
    '    private val client: NotificationsClient,',
    ') {',
    '    suspend fun sendNotifications(notifications: List<Notification>) = supervisorScope {',
    '        for (n in notifications) launch(handler) { client.send(n) }',
    '    }',
    '}',
    '',
    { vi: 'val handler = CoroutineExceptionHandler { _, e -> log(e) }   // KHÔNG có handler: Android crash app', en: 'val handler = CoroutineExceptionHandler { _, e -> log(e) }   // WITHOUT a handler: Android crashes the app' },
    { vi: 'viewModelScope.launch { sender.sendNotifications(listOf(n1, n2, n3)); println("Tiếp tục") }', en: 'viewModelScope.launch { sender.sendNotifications(listOf(n1, n2, n3)); println("Continue") }' }
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
