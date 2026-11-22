# Coroutines v2 · Phần 2 · A3 Coroutine builders (Deep Dive, "Coroutine builders", tr. PDF 66–81).
# Viết sâu thêm vào chương A3 có sẵn (giữ id a3, sim coroutines.builders, mục v1 "when"). Khung: docs/chapter-template-v2.md.

SEC_ORDER = {'a3': ['recap', 'bridge', 'launch', 'runblocking', 'async', 'when', 'structured', 'bigger', 'scopefn', 'bugs', 'exercises', 'recall']}


def override(o):
    o('a3.title', 'Coroutine builders: launch, runBlocking, async', 'Coroutine builders: launch, runBlocking, async')
    o('a3.essence',
      'Hàm thường không gọi được hàm suspend, vậy chuỗi hàm suspend phải bắt đầu ở đâu đó. Chỗ bắt đầu là một coroutine builder: cây cầu từ thế giới thường sang thế giới suspend.\n'
      'Ba builder cốt lõi của kotlinx.coroutines: `launch` (khởi động một việc chạy độc lập, trả về `Job`), `async` (giống `launch` nhưng tạo ra một giá trị, trả về `Deferred<T>`, lấy bằng `await()`), và `runBlocking` (chặn luồng hiện tại cho tới khi coroutine bên trong xong; chỉ dùng ở `main` hoặc test).\n'
      '`launch` và `async` là extension của `CoroutineScope`. Gọi chúng trong scope của một coroutine khác thì chúng thành con của coroutine đó: đó là structured concurrency. Cha chờ con, hủy cha thì hủy con, lỗi ở con lan lên cha.',
      'An ordinary function cannot call a suspending function, so the chain of suspending functions has to start somewhere. It starts at a coroutine builder: the bridge from the normal world to the suspending world.\n'
      'The three core builders of kotlinx.coroutines: `launch` (starts an independent job and returns a `Job`), `async` (like `launch` but produces a value; it returns a `Deferred<T>` you read with `await()`), and `runBlocking` (blocks the current thread until the coroutine inside finishes; only for `main` or tests).\n'
      '`launch` and `async` are extensions on `CoroutineScope`. Called inside another coroutine\'s scope, they become that coroutine\'s children: that is structured concurrency. The parent waits for its children, cancelling the parent cancels the children, and a child\'s failure propagates to the parent.')
    o('a3.goal.g1', 'Đã so thời gian tuần tự với đồng thời (bật "đồng thời")', 'Compared sequential and concurrent timing (turn on "concurrent")')


def add(a):
    def B(ch, sec, n, field, vi, en=None):
        a('%s.sec.%s.b.%02d.%s' % (ch, sec, n, field), vi, vi if en is None else en)
    C = 'a3'

    S = 'recap'
    a(C + '.sec.%s.title' % S, 'Ôn nhanh Phần 1', 'Quick review of Part 1')
    B(C, S, 1, 'ask', 'Hàm suspend nhận thêm tham số ẩn nào? Vì sao một hàm thường không thể gọi nó?', 'What hidden parameter does a suspending function take? Why can an ordinary function not call it?')
    B(C, S, 1, 'ans', 'Một `Continuation` (tham số cuối, CPS). Hàm thường không có continuation nào để truyền, và cũng không xử lý được giá trị `COROUTINE_SUSPENDED`. Phải có một coroutine bắt đầu chuỗi: đó là việc của builder.', 'A `Continuation` (the last parameter, CPS). An ordinary function has no continuation to pass, and cannot handle the `COROUTINE_SUSPENDED` value either. Some coroutine has to start the chain: that is the builder\'s job.')

    S = 'bridge'
    a(C + '.sec.%s.title' % S, 'Builder: cầu nối từ thế giới thường sang thế giới suspend', 'Builders: the bridge from the normal world to the suspending world')
    a(C + '.sec.%s.badge' % S, 'stable')
    B(C, S, 1, 'p',
      'Hàm suspend truyền continuation cho nhau. Chúng gọi hàm thường thoải mái, nhưng hàm thường không gọi được hàm suspend. Mỗi hàm suspend phải được một hàm suspend khác gọi, và hàm đó lại được một hàm suspend khác gọi… Chuỗi này phải bắt đầu ở một coroutine builder.\n'
      '`suspend fun main()` có vẻ là ngoại lệ, nhưng thật ra Kotlin cũng khởi động nó bằng một builder, chỉ là bạn không thấy. Trên Android và backend, `suspend fun main` không giúp được gì: bạn luôn bắt đầu từ một builder trên một scope (`viewModelScope.launch`, `lifecycleScope.launch`…).',
      'Suspending functions pass continuations to each other. They call ordinary functions without any trouble, but ordinary functions cannot call suspending functions. Every suspending function must be called by another suspending function, which is called by yet another… That chain has to start at a coroutine builder.\n'
      '`suspend fun main()` seems like an exception, but Kotlin actually starts it with a builder too; you just do not see it. On Android and on the backend, `suspend fun main` does not help: you always start from a builder on a scope (`viewModelScope.launch`, `lifecycleScope.launch`…).')

    S = 'launch'
    a(C + '.sec.%s.title' % S, 'launch: bắn một quả pháo hoa', 'launch: setting off a firework')
    a(C + '.sec.%s.badge' % S, 'stable')
    B(C, S, 1, 'p',
      '`launch` về khái niệm giống khởi động một luồng mới: coroutine bắt đầu và chạy độc lập, như quả pháo hoa bắn lên trời. Dùng `launch` để khởi động một tiến trình mà bạn không cần lấy kết quả. Ví dụ dưới dùng `GlobalScope` để tạm né structured concurrency (mục sau giải thích vì sao không nên dùng nó trong dự án thật) ([[src:kx-launch]]):',
      '`launch` is conceptually like starting a new thread: the coroutine starts and runs independently, like a firework shot into the sky. Use `launch` to start a process whose result you do not need. The example below uses `GlobalScope` to sidestep structured concurrency for now (a later section explains why not to use it in real projects) ([[src:kx-launch]]):')
    B(C, S, 2, 'kt', 'fun main() {\n    GlobalScope.launch {\n        delay(1000L)\n        println("World!")\n    }\n    GlobalScope.launch {\n        delay(1000L)\n        println("World!")\n    }\n    println("Hello,")\n    Thread.sleep(2000L)\n}')
    B(C, S, 3, 'predict', 'Output là gì? Bỏ dòng `Thread.sleep(2000L)` thì sao?', 'What is the output? What if you remove the `Thread.sleep(2000L)` line?')
    B(C, S, 3, 'ans', '"Hello," rồi sau 1 giây hai dòng "World!". Bỏ `Thread.sleep` thì chỉ in "Hello," và chương trình kết thúc ngay: `delay` không chặn luồng nào, nên không có gì giữ chương trình chạy. Hai coroutine chưa kịp làm gì.', '"Hello,", then after 1 second two "World!" lines. Without `Thread.sleep`, only "Hello," is printed and the program ends immediately: `delay` blocks no thread, so nothing keeps the program alive. The two coroutines never get to do anything.')
    B(C, S, 4, 'note',
      '`launch` giống một daemon thread: cả hai chạy nền và không ngăn chương trình kết thúc. Chỗ khớp: cả hai khởi động một tiến trình độc lập, và cần gì đó giữ chương trình sống. Chỗ không khớp: luồng bị chặn thì tốn kém, còn coroutine đang suspend gần như miễn phí; và (khi không dùng `GlobalScope`) coroutine có cha, bị hủy cùng cha, điều luồng không có.',
      '`launch` is like a daemon thread: both run in the background and do not stop the program from ending. Where it matches: both start an independent process and need something to keep the program alive. Where it does not: a blocked thread is expensive while a suspended coroutine is almost free; and (when not using `GlobalScope`) a coroutine has a parent and is cancelled with it, which threads do not have.')
    B(C, S, 4, 'kind', 'analogy')
    B(C, S, 5, 'p', '`launch` trả về một `Job`: tay cầm để chờ (`join()`), hủy (`cancel()`) hoặc xem trạng thái của coroutine. Chương "Job và chờ con" sẽ đi sâu.', '`launch` returns a `Job`: a handle to wait for (`join()`), cancel (`cancel()`) or inspect the coroutine. The "Jobs and awaiting children" chapter goes deeper.')

    S = 'runblocking'
    a(C + '.sec.%s.title' % S, 'runBlocking: builder chặn luồng (rất đặc biệt)', 'runBlocking: the builder that blocks (very unusual)')
    a(C + '.sec.%s.badge' % S, 'stable')
    B(C, S, 1, 'p',
      'Quy tắc chung: coroutine không bao giờ chặn luồng, chỉ suspend. Nhưng có chỗ cần chặn, như `main`: không chặn thì chương trình kết thúc quá sớm. `runBlocking` chạy một coroutine mới và chặn luồng hiện tại (có thể bị ngắt) cho tới khi coroutine đó xong ([[src:kx-runblocking]]). Vì vậy `delay(1000L)` bên trong `runBlocking` cư xử như `Thread.sleep(1000L)` đối với luồng gọi nó.',
      'The general rule: coroutines never block threads, they only suspend. But some places need blocking, such as `main`: without it the program ends too early. `runBlocking` runs a new coroutine and blocks the current thread (interruptibly) until that coroutine completes ([[src:kx-runblocking]]). So `delay(1000L)` inside `runBlocking` behaves like `Thread.sleep(1000L)` as far as the calling thread is concerned.')
    B(C, S, 2, 'kt', 'fun main() {\n    runBlocking {\n        delay(1000L)\n        println("World!")\n    }\n    runBlocking {\n        delay(1000L)\n        println("World!")\n    }\n    println("Hello,")\n}')
    B(C, S, 3, 'predict', 'Output và thời điểm của từng dòng?', 'What is the output, and when does each line appear?')
    B(C, S, 3, 'ans', '(1 giây) World! → (1 giây) World! → Hello,. Mỗi `runBlocking` chặn `main` tới khi khối bên trong xong, nên mọi thứ chạy lần lượt, y như ba lời gọi `Thread.sleep`.', '(1 second) World! → (1 second) World! → Hello,. Each `runBlocking` blocks `main` until its block finishes, so everything runs one after another, exactly like `Thread.sleep` calls.')
    B(C, S, 4, 'p',
      'Hai chỗ dùng `runBlocking`: hàm `main` và unit test, vì cả hai đều cần chặn luồng để chương trình (hoặc test) không kết thúc sớm. Ngày nay, test thường dùng `runTest` (chạy trên thời gian ảo, học ở chương Testing), còn `main` thường viết thành `suspend fun main() = coroutineScope { … }`. Khác biệt quan trọng: `runBlocking` tạo một scope, nên `launch` bên trong nó là con của nó và nó tự chờ con.',
      'There are two places for `runBlocking`: the `main` function and unit tests, since both need to block a thread so the program (or the test) does not end early. Nowadays tests usually use `runTest` (which runs on virtual time, covered in the Testing chapter), and `main` is usually written as `suspend fun main() = coroutineScope { … }`. One important difference: `runBlocking` creates a scope, so a `launch` inside it is its child, and it waits for its children by itself.')

    S = 'async'
    a(C + '.sec.%s.title' % S, 'async: tạo ra một giá trị (Deferred và await)', 'async: producing a value (Deferred and await)')
    a(C + '.sec.%s.badge' % S, 'stable')
    B(C, S, 1, 'p',
      '`async` giống `launch` nhưng được thiết kế để tạo ra một giá trị: giá trị cuối cùng của lambda. Nó trả về `Deferred<T>`; hàm suspend `await()` trả giá trị khi đã sẵn sàng ([[src:kx-async]]). Giống `launch`, `async` khởi động coroutine NGAY khi được gọi. `Deferred` giữ giá trị sau khi có, nên `await()` gọi sau đó trả ngay; gọi trước thì suspend cho tới khi có.',
      '`async` is like `launch` but designed to produce a value: the last value of the lambda. It returns a `Deferred<T>`; the suspending function `await()` returns the value once it is ready ([[src:kx-async]]). Like `launch`, `async` starts the coroutine IMMEDIATELY when called. The `Deferred` keeps the value once it exists, so a later `await()` returns at once; an earlier one suspends until the value is there.')
    B(C, S, 2, 'kt', 'fun main() = runBlocking {\n    val res1 = GlobalScope.async { delay(1000L); "Text 1" }\n    val res2 = GlobalScope.async { delay(3000L); "Text 2" }\n    val res3 = GlobalScope.async { delay(2000L); "Text 3" }\n    println(res1.await())\n    println(res2.await())\n    println(res3.await())\n}')
    B(C, S, 3, 'predict', 'Mỗi dòng được in ở giây thứ mấy? Tổng thời gian là bao nhiêu?', 'At which second is each line printed? What is the total time?')
    B(C, S, 3, 'ans', 'Text 1 ở giây 1; Text 2 ở giây 3; Text 3 cũng ở giây 3 (ngay sau Text 2, vì res3 đã xong từ giây 2 và `await()` trả ngay). Tổng khoảng 3 giây, không phải 6, vì cả ba khởi động cùng lúc.', 'Text 1 at second 1; Text 2 at second 3; Text 3 also at second 3 (right after Text 2, because res3 was already done at second 2 and `await()` returns at once). About 3 seconds in total, not 6, because all three started at the same time.')
    B(C, S, 4, 'p',
      'Thay mọi `launch` bằng `async` thì mã vẫn chạy, nhưng đừng làm vậy. `async` nói với người đọc rằng "có một giá trị ở đây". Nếu không cần giá trị, dùng `launch`. Cách dùng `async` điển hình là chạy song song hai nguồn dữ liệu rồi ghép lại; việc chạy cuối không cần bọc `async` vì coroutine hiện tại tự làm được:',
      'Replace every `launch` with `async` and the code still works, but do not do that. `async` tells readers "there is a value here". If you do not need a value, use `launch`. The typical use of `async` is running two data sources in parallel and combining them; the last job needs no `async` wrapper because the current coroutine can do it itself:')
    B(C, S, 5, 'kt',
      'scope.launch {\n    val news = async {\n        newsRepo.getNews().sortedByDescending { it.date }\n    }\n    val newsSummary = newsRepo.getNewsSummary()   // bọc async ở đây là thừa\n    view.showNews(newsSummary, news.await())\n}',
      'scope.launch {\n    val news = async {\n        newsRepo.getNews().sortedByDescending { it.date }\n    }\n    val newsSummary = newsRepo.getNewsSummary()   // wrapping this in async would be redundant\n    view.showNews(newsSummary, news.await())\n}')
    B(C, S, 6, 'p', 'Mô phỏng ngay dưới cho thấy hai việc tải chạy tuần tự hay đồng thời (bật "đồng thời"), và chuyện gì xảy ra với việc còn lại khi một việc lỗi.', 'The simulation just below shows two loads running sequentially or concurrently (turn on "concurrent"), and what happens to the other job when one fails.')

    S = 'structured'
    a(C + '.sec.%s.title' % S, 'Structured concurrency: bỏ GlobalScope, để cha chờ con', 'Structured concurrency: drop GlobalScope, let the parent wait')
    a(C + '.sec.%s.badge' % S, 'stable')
    B(C, S, 1, 'kt', 'fun main() = runBlocking {\n    GlobalScope.launch { delay(1000L); println("World!") }\n    GlobalScope.launch { delay(2000L); println("World!") }\n    println("Hello,")\n}')
    B(C, S, 2, 'predict', 'Đoạn trên in gì? Đổi `GlobalScope.launch` thành `launch` thì sao?', 'What does the code above print? What changes if you write `launch` instead of `GlobalScope.launch`?')
    B(C, S, 2, 'ans', 'Chỉ "Hello,": coroutine trên `GlobalScope` không có cha, `runBlocking` không chờ chúng và chương trình kết thúc. Viết `launch` (tức `this.launch`) thì hai coroutine là con của `runBlocking`; cha chờ con nên in đủ: Hello, → (1 s) World! → (1 s) World!.', 'Only "Hello,": coroutines on `GlobalScope` have no parent, `runBlocking` does not wait for them, and the program ends. With `launch` (that is, `this.launch`), the two coroutines are children of `runBlocking`; the parent waits for its children, so everything prints: Hello, → (1 s) World! → (1 s) World!.')
    B(C, S, 3, 'p',
      'Vì sao lúc nãy phải viết `GlobalScope`? Vì `launch` và `async` là extension của `CoroutineScope`. Nhìn chữ ký, tham số `block` của `runBlocking`, `launch`, `async` đều có receiver là `CoroutineScope`. Nghĩa là bên trong một coroutine, `this` đã là một scope, nên gọi `launch` thẳng là đủ, và coroutine mới thành con của coroutine hiện tại:',
      'Why did we need `GlobalScope` earlier? Because `launch` and `async` are extensions on `CoroutineScope`. Look at the signatures: the `block` parameter of `runBlocking`, `launch` and `async` all has `CoroutineScope` as its receiver. So inside a coroutine, `this` is already a scope; calling `launch` directly is enough, and the new coroutine becomes a child of the current one:')
    B(C, S, 4, 'kt', 'fun <T> runBlocking(context: CoroutineContext = EmptyCoroutineContext, block: suspend CoroutineScope.() -> T): T\n\nfun CoroutineScope.launch(\n    context: CoroutineContext = EmptyCoroutineContext,\n    start: CoroutineStart = CoroutineStart.DEFAULT,\n    block: suspend CoroutineScope.() -> Unit\n): Job\n\nfun <T> CoroutineScope.async(\n    context: CoroutineContext = EmptyCoroutineContext,\n    start: CoroutineStart = CoroutineStart.DEFAULT,\n    block: suspend CoroutineScope.() -> T\n): Deferred<T>')
    B(C, S, 5, 'p',
      'Quan hệ cha–con này gọi là structured concurrency. Bốn hệ quả quan trọng nhất (mỗi cái có chương riêng):\n'
      '1. Con thừa hưởng context của cha (và có thể ghi đè), xem chương Context.\n'
      '2. Cha suspend cho tới khi mọi con xong, xem chương Job.\n'
      '3. Hủy cha thì mọi con bị hủy, xem chương Hủy.\n'
      '4. Con ném lỗi thì cha cũng bị phá, xem chương Exception.\n'
      '`runBlocking` không phải extension của `CoroutineScope`, nên nó không thể là con: nó chỉ làm gốc của một cây.',
      'This parent–child relationship is called structured concurrency. Its four most important effects (each has its own chapter):\n'
      '1. Children inherit their parent\'s context (and may override it); see the Context chapter.\n'
      '2. A parent suspends until all its children finish; see the Job chapter.\n'
      '3. Cancelling the parent cancels every child; see the Cancellation chapter.\n'
      '4. A child that throws destroys the parent too; see the Exceptions chapter.\n'
      '`runBlocking` is not an extension on `CoroutineScope`, so it cannot be a child: it can only be the root of a tree.')

    S = 'bigger'
    a(C + '.sec.%s.title' % S, 'Bức tranh lớn: một ứng dụng thật trông thế nào', 'The bigger picture: what a real app looks like')
    a(C + '.sec.%s.badge' % S, 'stable')
    B(C, S, 1, 'p',
      'Trong ứng dụng thật: repository chỉ có hàm `suspend` (gọi hàm suspend khác hoặc hàm thường). Scope do framework cung cấp (Android KTX: `viewModelScope`, `lifecycleScope`) hoặc do bạn tự dựng (chương "Tự dựng scope"). Builder đầu tiên được gọi trên scope đó; trong nó có thể gọi builder khác, và cứ thế:',
      'In a real app: repositories have only `suspend` functions (calling other suspending functions or ordinary ones). The scope is provided by the framework (Android KTX: `viewModelScope`, `lifecycleScope`) or built by you (chapter "Constructing a coroutine scope"). The first builder is called on that scope; inside it you can call other builders, and so on:')
    B(C, S, 2, 'kt',
      'class NetworkNewsRepository(private val api: NewsApi, private val settings: SettingsRepository) : NewsRepository {\n    override suspend fun getNews(): List<News> = api.getNews().map { it.toDomainNews() }\n    override suspend fun getNewsSummary(): List<News> = api.getNewsSummary(settings.getNewsSummaryType())\n}\n\nclass MainViewModel(private val userRepo: UserRepository, private val newsRepo: NewsRepository) : ViewModel() {\n    fun onCreate() {\n        viewModelScope.launch {\n            val user = userRepo.getUser()\n            _user.value = user\n        }\n        viewModelScope.launch {\n            val news = async { newsRepo.getNews().sortedByDescending { it.date } }\n            val summary = async { newsRepo.getNewsSummary() }\n            _news.value = NewsUi(summary.await(), news.await())\n        }\n    }\n}')

    S = 'scopefn'
    a(C + '.sec.%s.title' % S, 'Trong hàm suspend thì sao? coroutineScope', 'What about inside a suspending function? coroutineScope')
    a(C + '.sec.%s.badge' % S, 'stable')
    B(C, S, 1, 'p',
      'Trong một hàm suspend, ta suspend được nhưng không có scope để gọi `async`. Truyền scope vào làm tham số không phải giải pháp tốt (chương "Scope functions" giải thích). Thay vào đó dùng `coroutineScope { }`: một hàm suspend tạo scope cho lambda của nó và trả về giá trị của lambda, như `let`, `run`, `runBlocking` ([[src:kx-coroutinescope]]). Nó chỉ xong khi mọi con xong.',
      'Inside a suspending function we can suspend, but we have no scope to call `async` on. Passing a scope in as a parameter is not a good solution (the "Coroutine scope functions" chapter explains why). Instead use `coroutineScope { }`: a suspending function that creates a scope for its lambda and returns the lambda\'s value, like `let`, `run`, `runBlocking` ([[src:kx-coroutinescope]]). It finishes only when all its children have finished.')
    B(C, S, 2, 'kt',
      'suspend fun getArticlesForUser(userToken: String?): List<ArticleJson> = coroutineScope {\n    val articles = async { articleRepository.getArticles() }   // song song\n    val user = userService.getUser(userToken)\n    articles.await()\n        .filter { canSeeOnList(user, it) }\n        .map { toArticleJson(it) }\n}\n\n// main hiện đại: suspend main + coroutineScope thay cho runBlocking\nsuspend fun main(): Unit = coroutineScope {\n    launch { delay(1000L); println("World!") }\n    println("Hello,")\n}',
      'suspend fun getArticlesForUser(userToken: String?): List<ArticleJson> = coroutineScope {\n    val articles = async { articleRepository.getArticles() }   // in parallel\n    val user = userService.getUser(userToken)\n    articles.await()\n        .filter { canSeeOnList(user, it) }\n        .map { toArticleJson(it) }\n}\n\n// modern main: suspend main + coroutineScope instead of runBlocking\nsuspend fun main(): Unit = coroutineScope {\n    launch { delay(1000L); println("World!") }\n    println("Hello,")\n}')
    B(C, S, 3, 'note',
      'Tóm tắt bản đồ: bắt đầu từ một scope (hoặc `runBlocking` ở main/test) → gọi builder (`launch`/`async`) → trong đó gọi hàm suspend → trong hàm suspend cần đồng thời thì dùng `coroutineScope { }` rồi gọi builder bên trong. Không gọi builder trực tiếp trong hàm suspend mà không có scope.',
      'The map in short: start from a scope (or `runBlocking` in main/tests) → call a builder (`launch`/`async`) → call suspending functions inside it → when a suspending function needs concurrency, use `coroutineScope { }` and call builders inside. Do not call builders directly in a suspending function without a scope.')

    S = 'bugs'
    a(C + '.sec.%s.title' % S, 'Bug thường gặp với builder', 'Common bugs with builders')
    a(C + '.sec.%s.badge' % S, 'stable')
    B(C, S, 1, 'bug', 'Ứng dụng đứng hình (rồi ANR) khi mở màn hình. Code: `override fun onCreate(…) { val user = runBlocking { repo.loadUser() }; show(user) }`.', 'The app freezes (then ANRs) when a screen opens. Code: `override fun onCreate(…) { val user = runBlocking { repo.loadUser() }; show(user) }`.')
    B(C, S, 1, 'cause', '`runBlocking` chặn luồng gọi nó, ở đây là luồng Main, suốt thời gian tải. Tệ hơn, nếu bên trong có gì đó cần chạy trên `Dispatchers.Main` (như `withContext(Dispatchers.Main)`) thì nó chờ một luồng Main đang bị chính nó chặn: deadlock.', '`runBlocking` blocks the calling thread, here the Main thread, for the whole load. Worse, if anything inside needs to run on `Dispatchers.Main` (such as `withContext(Dispatchers.Main)`), it waits for a Main thread that it is itself blocking: a deadlock.')
    B(C, S, 1, 'fix', 'Không dùng `runBlocking` trong mã ứng dụng Android. Dùng `lifecycleScope.launch { … }` hoặc `viewModelScope.launch { … }` và cập nhật UI khi có dữ liệu.', 'Do not use `runBlocking` in Android app code. Use `lifecycleScope.launch { … }` or `viewModelScope.launch { … }` and update the UI when the data arrives.')
    B(C, S, 2, 'bug', 'Bạn dùng `GlobalScope.async { upload(file) }` để "chạy nền" mà không bao giờ `await()`. Upload thất bại nhưng không có log, không crash, không gì cả.', 'You use `GlobalScope.async { upload(file) }` to "run it in the background" and never call `await()`. The upload fails, yet there is no log, no crash, nothing.')
    B(C, S, 2, 'cause', 'Exception trong `async` được giữ trong `Deferred` để ném ra khi ai đó gọi `await()` ([[src:kt-exceptions]]). Không có cha (GlobalScope) và không ai `await`, nên exception không bao giờ lộ ra. Đây là lý do "đừng dùng async như launch".', 'An exception inside `async` is kept in the `Deferred` and thrown when someone calls `await()` ([[src:kt-exceptions]]). With no parent (GlobalScope) and nobody calling `await`, the exception never surfaces. This is why "do not use async like launch".')
    B(C, S, 2, 'fix', 'Không cần giá trị thì dùng `launch`, và gọi trên một scope có vòng đời thay vì `GlobalScope`. Cần giá trị thì luôn `await()` trong `try/catch`.', 'If you do not need a value, use `launch`, and call it on a lifecycle-aware scope instead of `GlobalScope`. If you need the value, always `await()` it inside a `try/catch`.')
    B(C, S, 3, 'bug', 'Hàm `suspend fun refresh(scope: CoroutineScope) { scope.launch { load() } }` trả về ngay; nơi gọi tưởng đã refresh xong nên đọc dữ liệu cũ, và lỗi trong `load()` không tới được nơi gọi.', 'The function `suspend fun refresh(scope: CoroutineScope) { scope.launch { load() } }` returns immediately; the caller thinks the refresh is done and reads stale data, and errors in `load()` never reach the caller.')
    B(C, S, 3, 'cause', 'Coroutine mới là con của `scope` được truyền vào, không phải của hàm `refresh`. Hàm không chờ nó, không nhận lỗi của nó.', 'The new coroutine is a child of the passed-in `scope`, not of the `refresh` function. The function neither waits for it nor receives its errors.')
    B(C, S, 3, 'fix', 'Trong hàm suspend, dùng `coroutineScope { launch { … } }`, hoặc đơn giản gọi `load()` trực tiếp. Khi đó hàm chỉ trả về khi việc thật sự xong, và lỗi đi ngược về nơi gọi.', 'Inside a suspending function, use `coroutineScope { launch { … } }`, or simply call `load()` directly. Then the function returns only when the work is really done, and errors travel back to the caller.')

    S = 'exercises'
    a(C + '.sec.%s.title' % S, 'Bài tập', 'Exercises')
    a(C + '.sec.%s.badge' % S, 'stable')
    B(C, S, 1, 'ex', 'Đoán output và thời điểm:', 'Predict the output and the timing:')
    B(C, S, 1, 'exkt', 'fun main() = runBlocking {\n    val a = async { delay(300); "A" }\n    launch { delay(100); println("L") }\n    println("start")\n    println(a.await())\n    println("end")\n}')
    B(C, S, 1, 'sol', 'start (0 ms) → L (100 ms) → A (300 ms) → end (300 ms). `async` và `launch` đều khởi động ngay, nhưng chạy khi cha suspend; cha in "start" trước, rồi suspend ở `await()`. Con `launch` in L ở 100 ms. Cha nhận A ở 300 ms, in A rồi end. `runBlocking` kết thúc sau khi mọi con xong.', 'start (0 ms) → L (100 ms) → A (300 ms) → end (300 ms). `async` and `launch` both start immediately but run once the parent suspends; the parent prints "start" first, then suspends at `await()`. The `launch` child prints L at 100 ms. The parent gets A at 300 ms, prints A, then end. `runBlocking` finishes once all children are done.')
    B(C, S, 2, 'ex', 'Bài khuyết bước: hàm sau tải avatar và profile tuần tự (2 giây). Sửa để chạy song song (khoảng 1 giây) mà vẫn đúng structured concurrency.', 'A partly-solved exercise: the function below loads the avatar and the profile sequentially (2 seconds). Make them run in parallel (about 1 second) while keeping structured concurrency.')
    B(C, S, 2, 'exkt', 'suspend fun loadScreen(id: String): Screen {\n    val avatar = api.avatar(id)     // 1 s\n    val profile = api.profile(id)   // 1 s\n    return Screen(avatar, profile)\n}')
    B(C, S, 2, 'hint', 'Cần một scope bên trong hàm suspend. Hàm nào tạo scope mà vẫn chờ con?', 'You need a scope inside a suspending function. Which function creates a scope and still waits for its children?')
    B(C, S, 2, 'sol', 'Bọc bằng `coroutineScope`, khởi động một việc bằng `async`. Nếu một việc lỗi, việc kia bị hủy và lỗi ném ra từ `loadScreen`.', 'Wrap it in `coroutineScope` and start one job with `async`. If one job fails, the other is cancelled and the error is thrown from `loadScreen`.')
    B(C, S, 2, 'solkt', 'suspend fun loadScreen(id: String): Screen = coroutineScope {\n    val avatar = async { api.avatar(id) }\n    val profile = api.profile(id)\n    Screen(avatar.await(), profile)\n}')
    B(C, S, 3, 'ex', 'Vì sao `runBlocking` không thể là con của coroutine khác, còn `launch` thì được?', 'Why can `runBlocking` not be a child of another coroutine, while `launch` can?')
    B(C, S, 3, 'sol', '`launch` là extension của `CoroutineScope`: nó được gọi TRÊN một scope và gắn vào Job của scope đó. `runBlocking` là hàm thường, không có receiver scope, nên nó luôn tạo một gốc mới. (Nó cũng chặn luồng, nên gọi trong coroutine là sai.)', '`launch` is an extension on `CoroutineScope`: it is called ON a scope and attaches to that scope\'s Job. `runBlocking` is an ordinary function with no scope receiver, so it always creates a new root. (It also blocks the thread, so calling it inside a coroutine is wrong.)')

    S = 'recall'
    a(C + '.sec.%s.title' % S, 'Tự trả lời', 'Answer it yourself')
    a(C + '.sec.%s.badge' % S, 'stable')
    B(C, S, 1, 'ask', 'So sánh `launch`, `async`, `runBlocking` theo ba câu: trả về gì, có chặn luồng không, dùng ở đâu.', 'Compare `launch`, `async` and `runBlocking` on three points: what it returns, whether it blocks a thread, where to use it.')
    B(C, S, 1, 'ans', '`launch`: trả `Job`, không chặn, khởi động việc không cần kết quả. `async`: trả `Deferred<T>`, không chặn, khi cần giá trị (thường để song song). `runBlocking`: trả giá trị của khối, CHẶN luồng gọi, chỉ ở `main`/test (hiện nay thường thay bằng `runTest`, `suspend main`).', '`launch`: returns a `Job`, does not block, for jobs whose result you do not need. `async`: returns a `Deferred<T>`, does not block, when you need a value (usually for parallelism). `runBlocking`: returns the block\'s value, BLOCKS the calling thread, only in `main`/tests (nowadays often replaced by `runTest`, `suspend main`).')
    B(C, S, 2, 'ask', 'Bốn hệ quả của quan hệ cha–con trong structured concurrency là gì?', 'What are the four effects of the parent–child relationship in structured concurrency?')
    B(C, S, 2, 'ans', 'Con thừa hưởng context; cha chờ mọi con; hủy cha thì hủy con; con lỗi thì cha bị phá (và các con khác bị hủy).', 'Children inherit the context; the parent waits for all children; cancelling the parent cancels the children; a failing child destroys the parent (and the other children are cancelled).')


def _check():
    pass
