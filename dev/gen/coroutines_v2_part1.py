# Coroutines v2, Phần 1 (theo bố cục Kotlin Coroutines: Deep Dive, Part 1). Được dev/gen/coroutines_content.py nạp.
# Khung chương: docs/chapter-template-v2.md. Loại khối: docs/core-api.md §2.1. Bảng nguồn: docs/research/coroutines.md.

def add(a):
    def B(ch, sec, n, field, vi, en=None):
        a('%s.sec.%s.b.%02d.%s' % (ch, sec, n, field), vi, vi if en is None else en)

    # =====================================================================
    # U1 · Vì sao cần coroutine?  (Deep Dive, "Why Kotlin Coroutines?", tr. PDF 14–26)
    # =====================================================================
    C = 'u1'
    a(C + '.title', 'Vì sao cần coroutine?', 'Why coroutines?')
    a(C + '.essence',
      'Ứng dụng Android chỉ có một luồng được vẽ giao diện và nhận thao tác: luồng Main. Luồng đó không được phép đứng chờ mạng hay ổ đĩa, nhưng kết quả chờ được lại phải quay về đúng luồng đó để hiện lên màn hình.\n'
      'Chương này đi qua bốn cách giải bài toán ấy (tự đổi luồng, callback, RxJava, coroutine) trên cùng một màn hình tin tức, để thấy mỗi cách trả giá ở đâu.\n'
      'Ý cốt lõi cần mang theo: coroutine có thể tạm dừng (suspend) ở một điểm rồi tiếp tục sau, và trong lúc tạm dừng nó KHÔNG giữ luồng. Nhờ vậy mã vẫn viết thẳng từ trên xuống như mã đồng bộ.',
      'An Android app has only one thread that draws the UI and receives input: the Main thread. That thread must not sit waiting for the network or the disk, yet the result of the wait has to come back to that very thread to be shown on screen.\n'
      'This chapter walks through four ways to solve that problem (switching threads by hand, callbacks, RxJava, coroutines) on the same news screen, to show where each one pays a price.\n'
      'The core idea to take away: a coroutine can pause (suspend) at a point and continue later, and while it is paused it does NOT hold a thread. That is why the code can still be written straight from top to bottom, like synchronous code.')
    a(C + '.goal.g1', 'Đã bấm Step và đối chiếu với câu đoán trước', 'Pressed Step and compared it with your prediction')
    a(C + '.goal.g2', 'Đã đi hết mô phỏng (nên thử cả `delay` và `Thread.sleep`)', 'Went through the whole simulation (try both `delay` and `Thread.sleep`)')

    # ---- 1. Vấn đề ----
    S = 'problem'
    a(C + '.sec.%s.title' % S, 'Bài toán: một màn hình tin tức', 'The problem: a news screen')
    a(C + '.sec.%s.badge' % S, 'stable')
    B(C, S, 1, 'p',
      'Phần lớn logic ở phía giao diện (Android, web, desktop) lặp lại một khuôn: (1) lấy dữ liệu từ đâu đó: API, cơ sở dữ liệu, preferences, một ứng dụng khác; (2) xử lý dữ liệu; (3) làm gì đó với kết quả: hiện lên màn hình, lưu lại, gửi đi.\n'
      'Ví dụ xuyên suốt phần này: lấy danh sách tin từ API, sắp xếp theo thời gian đăng, rồi hiện lên màn hình. Nếu được viết "như ý muốn", hàm trông thế này:',
      'Most UI-side logic (Android, web, desktop) repeats one pattern: (1) get data from somewhere: an API, a database, preferences, another app; (2) process the data; (3) do something with the result: show it, store it, send it.\n'
      'The running example for this part: fetch a list of news from an API, sort it by publish time, then show it on screen. Written "the way we wish", the function looks like this:')
    B(C, S, 2, 'kt',
      'fun onCreate() {\n    val news = getNewsFromApi()          // chờ mạng: có thể mất vài giây\n    val sortedNews = news\n        .sortedByDescending { it.publishedAt }\n    view.showNews(sortedNews)             // phải chạy trên luồng Main\n}',
      'fun onCreate() {\n    val news = getNewsFromApi()          // waits for the network: may take seconds\n    val sortedNews = news\n        .sortedByDescending { it.publishedAt }\n    view.showNews(sortedNews)             // must run on the Main thread\n}')
    B(C, S, 3, 'p',
      'Đoạn mã này không chạy được trên Android, và lý do nằm ở luồng Main (còn gọi là UI thread). Đây là luồng duy nhất xử lý chạm, vẽ khung hình và chạy vòng đời Activity. Bộ công cụ giao diện của Android không an toàn khi dùng từ nhiều luồng, nên chỉ luồng đã tạo cây view mới được sửa view ([[src:and-threads]]).\n'
      'Hai lựa chọn đều hỏng. Nếu chạy `onCreate` trên luồng Main, `getNewsFromApi()` đứng chờ mạng và giữ luôn luồng Main: không vẽ được, không nhận chạm. Thực tế Android còn chặn sớm hơn: gọi mạng trên luồng Main ném `NetworkOnMainThreadException` ([[src:and-nomain]]). Với việc chặn khác (đọc file lớn, tính toán nặng), nếu luồng Main không phản hồi một thao tác nhập trong khoảng 5 giây thì hệ thống hiện hộp thoại ANR ([[src:and-anr]]). Còn nếu chạy cả hàm trên luồng khác, đến dòng `view.showNews(...)` thì ứng dụng ném `CalledFromWrongThreadException`, vì luồng đó không được sửa view.',
      'This code does not work on Android, and the reason is the Main thread (also called the UI thread). It is the only thread that handles touches, draws frames and runs the Activity lifecycle. Android\'s UI toolkit is not safe to use from several threads, so only the thread that created the view hierarchy may change views ([[src:and-threads]]).\n'
      'Both options break. If `onCreate` runs on the Main thread, `getNewsFromApi()` waits for the network and holds the Main thread the whole time: nothing is drawn, no touch is handled. In practice Android stops you even earlier: a network call on the Main thread throws `NetworkOnMainThreadException` ([[src:and-nomain]]). For other blocking work (reading a large file, heavy computation), if the Main thread does not respond to an input event within about 5 seconds, the system shows an ANR dialog ([[src:and-anr]]). And if the whole function runs on another thread, the line `view.showNews(...)` throws `CalledFromWrongThreadException`, because that thread may not change views.')
    B(C, S, 4, 'note',
      'Hình dung luồng Main là người thu ngân duy nhất của một quán cà phê: vừa nhận order (chạm), vừa đưa đồ uống (vẽ màn hình). Nếu người đó đứng chờ máy pha xong một ly, cả hàng đứng theo (đứng giao diện, ANR). Nhưng đồ uống phải do chính người đó trao cho khách (chỉ luồng Main được sửa view).\n'
      'Chỗ khớp: chỉ có một người, và người đó không được đứng chờ. Chỗ không khớp: luồng Main không "đi làm việc khác rồi quay lại" một cách tự nhiên như người thật. Việc tạm gác một công việc rồi tiếp tục sau phải có cơ chế lo, và coroutine chính là một cơ chế như vậy.',
      'Picture the Main thread as the only cashier in a coffee shop: they take orders (touches) and hand over drinks (draw the screen). If that person stands waiting for the machine to finish one cup, the whole queue waits too (frozen UI, ANR). But the drink must be handed over by that same person (only the Main thread may change views).\n'
      'Where it matches: there is only one person, and they must not stand and wait. Where it does not: the Main thread does not naturally "go do something else and come back" the way a person does. Setting a job aside and resuming it later needs a mechanism, and coroutines are one such mechanism.')
    B(C, S, 4, 'kind', 'analogy')
    B(C, S, 6, 'predict',
      'Giả sử (bỏ qua `NetworkOnMainThreadException`) `getNewsFromApi()` chạy trên luồng Main và mất 3 giây. Trong 3 giây đó, người dùng thấy gì nếu họ chạm vào nút "Làm mới" và trên màn hình đang có một vòng xoay loading?',
      'Suppose (ignoring `NetworkOnMainThreadException`) that `getNewsFromApi()` runs on the Main thread and takes 3 seconds. During those 3 seconds, what does the user see if they tap the "Refresh" button while a loading spinner is on screen?')
    B(C, S, 6, 'ans',
      'Vòng xoay đứng yên và lần chạm không có phản hồi gì. Vẽ khung hình và xử lý chạm đều cần luồng Main, mà luồng Main đang bị giữ. Lần chạm nằm trong hàng đợi và chỉ được xử lý khi luồng Main rảnh. Nếu chờ quá khoảng 5 giây, hệ thống báo ANR.',
      'The spinner freezes and the tap gets no response. Drawing frames and handling touches both need the Main thread, and the Main thread is being held. The tap sits in a queue and is handled only once the Main thread is free. If the wait goes past about 5 seconds, the system reports an ANR.')

    # ---- 2. Tự đổi luồng ----
    S = 'threads'
    a(C + '.sec.%s.title' % S, 'Cách 1: tự đổi luồng', 'Approach 1: switching threads by hand')
    a(C + '.sec.%s.badge' % S, 'stable')
    B(C, S, 1, 'p',
      'Cách đầu tiên nghĩ tới: làm phần chờ trên một luồng khác (được phép chặn), xong thì nhảy về luồng Main để hiện kết quả.',
      'The first idea: do the waiting part on another thread (where blocking is allowed), then jump back to the Main thread to show the result.')
    B(C, S, 2, 'kt',
      'fun onCreate() {\n    thread {                                  // luồng mới: được phép chặn\n        val news = getNewsFromApi()\n        val sortedNews = news\n            .sortedByDescending { it.publishedAt }\n        runOnUiThread {                       // gửi phần cuối về luồng Main\n            view.showNews(sortedNews)\n        }\n    }\n}',
      'fun onCreate() {\n    thread {                                  // a new thread: blocking is allowed\n        val news = getNewsFromApi()\n        val sortedNews = news\n            .sortedByDescending { it.publishedAt }\n        runOnUiThread {                       // send the last part to the Main thread\n            view.showNews(sortedNews)\n        }\n    }\n}')
    B(C, S, 3, 'p',
      'Đoạn này chạy được, và vẫn còn gặp trong mã cũ. Nhưng nó có bốn vấn đề:\n'
      '1. Không có cơ chế hủy. Luồng đã chạy thì chạy tới cùng, kể cả khi màn hình đã đóng. Lambda trong `thread { }` giữ tham chiếu tới `view` (và qua đó tới Activity), nên Activity đã đóng vẫn không được thu gom: rò bộ nhớ.\n'
      '2. Luồng đắt. Mỗi luồng có stack riêng và được hệ điều hành lập lịch. Tạo nhiều luồng chỉ để ngồi chờ là lãng phí (xem mục "Luồng đắt, coroutine rẻ" bên dưới).\n'
      '3. Đổi luồng qua lại liên tục làm mã khó theo dõi: phần nào chạy ở luồng nào phải tự nhớ.\n'
      '4. Mã dài và lồng nhau hơn, càng nhiều bước càng rối.',
      'This works, and you still see it in older code. But it has four problems:\n'
      '1. There is no cancellation. Once a thread starts it runs to the end, even after the screen is closed. The lambda in `thread { }` holds a reference to `view` (and through it to the Activity), so a closed Activity cannot be garbage collected: a memory leak.\n'
      '2. Threads are expensive. Each thread has its own stack and is scheduled by the operating system. Creating many threads only to sit and wait is wasteful (see "Threads are expensive, coroutines are cheap" below).\n'
      '3. Switching threads back and forth makes the code hard to follow: you must remember which part runs on which thread.\n'
      '4. The code gets longer and more nested, and messier with every extra step.')
    B(C, S, 4, 'bug',
      'Người dùng mở màn hình tin tức rồi bấm Back ngay. Vài giây sau ứng dụng vẫn tiêu pin và mạng; thỉnh thoảng log có exception từ `showNews`, LeakCanary báo Activity bị rò.',
      'The user opens the news screen and presses Back immediately. A few seconds later the app is still using battery and network; now and then the log shows an exception from `showNews`, and LeakCanary reports a leaked Activity.')
    B(C, S, 4, 'cause',
      'Luồng tạo trong `onCreate` không biết màn hình đã đóng. Không có gì nối thời gian sống của luồng với vòng đời màn hình, nên nó chạy tiếp, giữ tham chiếu tới view và Activity cũ, rồi cố cập nhật một view không còn hiển thị.',
      'The thread created in `onCreate` does not know the screen was closed. Nothing ties the thread\'s lifetime to the screen\'s lifecycle, so it keeps running, holds references to the old view and Activity, and then tries to update a view that is no longer shown.')
    B(C, S, 4, 'fix',
      'Cần một cách gắn công việc nền với vòng đời, sao cho đóng màn hình là mọi việc con bị hủy. Đó chính là thứ `viewModelScope` và `lifecycleScope` cung cấp cho coroutine (structured concurrency, học kỹ ở chương A2). Với luồng thuần, bạn phải tự giữ danh sách luồng và tự ngắt (`interrupt`), một việc dễ sai.',
      'You need a way to tie background work to a lifecycle so that closing the screen cancels every child job. That is exactly what `viewModelScope` and `lifecycleScope` give coroutines (structured concurrency, covered in depth in chapter A2). With plain threads you have to keep a list of threads and interrupt them yourself, which is easy to get wrong.')

    # ---- 3. Callback ----
    S = 'callbacks'
    a(C + '.sec.%s.title' % S, 'Cách 2: callback', 'Approach 2: callbacks')
    a(C + '.sec.%s.badge' % S, 'stable')
    B(C, S, 1, 'p',
      'Ý tưởng của callback: hàm không chặn nữa mà trả về ngay; bạn đưa cho nó một hàm (callback) để gọi khi việc xong.',
      'The idea of a callback: the function no longer blocks but returns right away; you give it a function (the callback) to call when the work is done.')
    B(C, S, 2, 'kt',
      'fun onCreate() {\n    getNewsFromApi { news ->                 // trả về ngay; lambda chạy khi có dữ liệu\n        val sortedNews = news\n            .sortedByDescending { it.publishedAt }\n        view.showNews(sortedNews)\n    }\n}',
      'fun onCreate() {\n    getNewsFromApi { news ->                 // returns at once; the lambda runs when data arrives\n        val sortedNews = news\n            .sortedByDescending { it.publishedAt }\n        view.showNews(sortedNews)\n    }\n}')
    B(C, S, 3, 'p',
      'Bản này chưa hủy được. Muốn hủy, mỗi hàm callback phải được viết riêng để hỗ trợ hủy, và bạn phải tự gom mọi đối tượng đã khởi động để hủy từng cái:',
      'This version cannot be cancelled. To cancel, every callback function has to be written specially to support it, and you have to collect every started object yourself to cancel them one by one:')
    B(C, S, 4, 'kt',
      'fun onCreate() {\n    startedCallbacks += getNewsFromApi { news ->\n        val sortedNews = news\n            .sortedByDescending { it.publishedAt }\n        view.showNews(sortedNews)\n    }\n}\n// onDestroy: startedCallbacks.forEach { it.cancel() }')
    B(C, S, 5, 'p',
      'Bài toán thật thường khó hơn: cần cấu hình, rồi tin tức (cần cấu hình), và thông tin người dùng, từ ba endpoint:',
      'Real problems are usually harder: you need a config, then the news (which needs the config), and the user info, from three endpoints:')
    B(C, S, 6, 'kt',
      'fun showNews() {\n    getConfigFromApi { config ->\n        getNewsFromApi(config) { news ->\n            getUserFromApi { user ->\n                view.showNews(user, news)\n            }\n        }\n    }\n}')
    B(C, S, 7, 'p',
      'Mã này có bốn chỗ dở:\n'
      '1. Lấy tin và lấy người dùng vốn có thể chạy song song (người dùng không phụ thuộc tin), nhưng cấu trúc lồng nhau buộc chúng chạy lần lượt. Muốn song song bằng callback thì phải tự đếm xem cả hai đã xong chưa.\n'
      '2. Hủy cả chuỗi tốn công: phải hủy đúng callback đang chờ ở tầng nào.\n'
      '3. Mỗi bước thụt vào thêm một tầng ("callback hell"), càng nhiều bước càng khó đọc. Xử lý lỗi phải lặp lại ở từng tầng.\n'
      '4. Khó điều khiển thứ tự, như ví dụ dưới đây cho thấy.',
      'This code has four weak spots:\n'
      '1. Fetching news and fetching the user could run in parallel (the user does not depend on the news), but the nesting forces them to run one after another. To run them in parallel with callbacks, you have to count by hand whether both have finished.\n'
      '2. Cancelling the whole chain takes effort: you must cancel the right callback at whichever level is waiting.\n'
      '3. Each step indents one more level ("callback hell"), and the more steps there are, the harder it is to read. Error handling has to be repeated at every level.\n'
      '4. Order is hard to control, as the example below shows.')
    B(C, S, 8, 'kt',
      'fun onCreate() {\n    showProgressBar()\n    showNews()\n    hideProgressBar()   // ?\n}')
    B(C, S, 9, 'predict',
      'Với `showNews()` viết bằng callback như trên, thanh tiến trình bị ẩn lúc nào?',
      'With `showNews()` written with callbacks as above, when is the progress bar hidden?')
    B(C, S, 9, 'ans',
      'Gần như ngay lập tức, trước khi có tin. `showNews()` chỉ khởi động việc tải rồi trả về luôn, nên dòng kế tiếp `hideProgressBar()` chạy ngay. Muốn đúng, `showNews` cũng phải nhận một callback: `showNews { hideProgressBar() }`. Callback lan dần lên mọi hàm gọi nó.',
      'Almost immediately, before any news arrives. `showNews()` only starts the loading and returns at once, so the next line `hideProgressBar()` runs right away. To get it right, `showNews` must also take a callback: `showNews { hideProgressBar() }`. Callbacks spread up to every function that calls them.')

    # ---- 4. RxJava ----
    S = 'rx'
    a(C + '.sec.%s.title' % S, 'Cách 3: RxJava và reactive stream', 'Approach 3: RxJava and reactive streams')
    a(C + '.sec.%s.badge' % S, 'stable')
    B(C, S, 1, 'p',
      'RxJava (và Reactor bên backend) đưa mọi thao tác vào một dòng dữ liệu (stream) có thể khởi động, biến đổi và quan sát. Stream hỗ trợ đổi luồng và chạy đồng thời:',
      'RxJava (and Reactor on the backend) puts every operation inside a stream of data that can be started, transformed and observed. Streams support switching threads and running concurrently:')
    B(C, S, 2, 'kt',
      'fun onCreate() {\n    disposables += getNewsFromApi()              // Single<List<News>>\n        .subscribeOn(Schedulers.io())            // làm việc trên luồng IO\n        .observeOn(AndroidSchedulers.mainThread()) // nhận kết quả trên Main\n        .map { news -> news.sortedByDescending { it.publishedAt } }\n        .subscribe { sortedNews -> view.showNews(sortedNews) }\n}\n// onDestroy: disposables.dispose()  → hủy stream',
      'fun onCreate() {\n    disposables += getNewsFromApi()              // Single<List<News>>\n        .subscribeOn(Schedulers.io())            // do the work on an IO thread\n        .observeOn(AndroidSchedulers.mainThread()) // receive the result on Main\n        .map { news -> news.sortedByDescending { it.publishedAt } }\n        .subscribe { sortedNews -> view.showNews(sortedNews) }\n}\n// onDestroy: disposables.dispose()  → cancels the stream')
    B(C, S, 3, 'p',
      'Đây là bước tiến thật: không rò bộ nhớ, hủy được qua `disposables`, dùng luồng đúng chỗ. Cái giá là độ phức tạp. So với mã "như ý muốn" ở đầu chương, hai đoạn gần như không còn giống nhau. Bạn phải học `subscribeOn`, `observeOn`, `map`, `subscribe`; phải nhớ hủy; và mọi hàm phải trả về kiểu bọc như `Single<List<News>>` thay vì `List<News>`. Đưa RxJava vào thường kéo theo sửa cấu trúc mã rất nhiều. Bài ba endpoint còn phức tạp hơn nữa:',
      'This is real progress: no memory leaks, cancellation through `disposables`, threads used in the right places. The price is complexity. Compared with the "wished-for" code at the start of the chapter, the two have almost nothing in common. You have to learn `subscribeOn`, `observeOn`, `map`, `subscribe`; you must remember to dispose; and every function must return a wrapped type such as `Single<List<News>>` instead of `List<News>`. Bringing in RxJava usually means restructuring a lot of code. The three-endpoint problem is even more involved:')
    B(C, S, 4, 'kt',
      'fun showNews() {\n    disposables += Observable.zip(\n        getConfigFromApi().flatMap { getNewsFromApi(it) },\n        getUserFromApi(),\n        Function2 { news: List<News>, user: User -> Pair(news, user) })\n        .subscribeOn(Schedulers.io())\n        .observeOn(AndroidSchedulers.mainThread())\n        .subscribe { (news, user) -> view.showNews(user, news) }\n}')
    B(C, S, 5, 'p',
      'Đúng, song song thật, không rò, nhưng phải biết `zip`, `flatMap`, gói giá trị vào `Pair` rồi tách ra. Câu hỏi đặt ra: có cách nào giữ được dáng mã thẳng như ban đầu mà vẫn có các lợi ích này không?',
      'Correct, truly parallel, no leaks, but you need to know `zip` and `flatMap`, pack values into a `Pair` and unpack them. The question is: is there a way to keep the straight shape of the original code and still get these benefits?')

    # ---- 5. Coroutine ----
    S = 'coroutines'
    a(C + '.sec.%s.title' % S, 'Cách 4: coroutine', 'Approach 4: coroutines')
    a(C + '.sec.%s.badge' % S, 'stable')
    B(C, S, 1, 'p',
      'Khả năng cốt lõi mà Kotlin Coroutines mang lại là tạm dừng (suspend) một coroutine tại một điểm và tiếp tục (resume) nó sau. Nhờ vậy, mã có thể chạy trên luồng Main và tạm dừng khi chờ dữ liệu từ API. Khi coroutine đang tạm dừng, luồng KHÔNG bị chặn: nó được thả ra để vẽ giao diện hoặc chạy coroutine khác. Khi dữ liệu về, coroutine chờ tới lượt dùng luồng Main (thường gần như ngay, đôi khi có vài coroutine xếp hàng trước), rồi chạy tiếp đúng từ chỗ đã dừng.\n'
      'Theo định nghĩa, coroutine là thành phần có thể tạm dừng và tiếp tục. async/await hay generator ở JavaScript, Python, Rust, C# cũng dựa trên ý tưởng coroutine, nhưng Kotlin cho bạn nhiều quyền điều khiển hơn: hủy, cây cha–con, chọn luồng.',
      'The core ability Kotlin Coroutines bring is to pause (suspend) a coroutine at a point and continue (resume) it later. Thanks to that, code can run on the Main thread and suspend while it waits for data from an API. While a coroutine is suspended, the thread is NOT blocked: it is released to draw the UI or run other coroutines. When the data arrives, the coroutine waits for its turn on the Main thread (usually almost immediately, sometimes behind a few queued coroutines), then continues exactly where it stopped.\n'
      'By definition, a coroutine is a component that can be suspended and resumed. async/await and generators in JavaScript, Python, Rust and C# build on the coroutine idea too, but Kotlin gives you more control: cancellation, a parent–child tree, choosing the thread.')
    B(C, S, 2, 'note',
      'Coroutine giống một cuốn sách có kẹp trang. Đọc tới đoạn phải chờ (đợi mạng), bạn kẹp trang lại, đặt sách xuống và đôi tay (luồng) rảnh để làm việc khác. Có dữ liệu, bạn mở đúng trang đã kẹp và đọc tiếp.\n'
      'Chỗ khớp: chỗ đang dở (kẹp trang = nhãn vị trí) và những gì cần nhớ (biến cục bộ) được lưu lại; luồng không bị giữ. Chỗ không khớp: không ai "nhớ ra" để mở sách. Khi dữ liệu về, chính thư viện gọi `resume` trên một đối tượng `Continuation`, và dispatcher xếp lịch cho phần còn lại chạy trên luồng phù hợp. Cơ chế này học kỹ ở chương "Suspension hoạt động thế nào" và "Coroutine dưới mui xe".',
      'A coroutine is like a book with a bookmark. When you reach a part where you must wait (for the network), you put the bookmark in, set the book down, and your hands (the thread) are free for other work. When the data arrives, you open the book at the bookmark and read on.\n'
      'Where it matches: the place you stopped (the bookmark = a position label) and what you need to remember (local variables) are saved; the thread is not held. Where it does not: nobody "remembers" to open the book. When the data arrives, the library itself calls `resume` on a `Continuation` object, and the dispatcher schedules the rest to run on a suitable thread. This mechanism is covered in detail in the chapters "How suspension works" and "Coroutines under the hood".')
    B(C, S, 2, 'kind', 'analogy')
    B(C, S, 4, 'kt',
      'fun onCreate() {\n    viewModelScope.launch {                  // chạy trên Main (mặc định của viewModelScope)\n        val news = getNewsFromApi()          // suspend: luồng Main được thả ra trong lúc chờ\n        val sortedNews = news\n            .sortedByDescending { it.publishedAt }\n        view.showNews(sortedNews)            // đã ở lại trên Main: sửa view an toàn\n    }\n}',
      'fun onCreate() {\n    viewModelScope.launch {                  // runs on Main (viewModelScope\'s default)\n        val news = getNewsFromApi()          // suspend: the Main thread is released while waiting\n        val sortedNews = news\n            .sortedByDescending { it.publishedAt }\n        view.showNews(sortedNews)            // back on Main: safe to change views\n    }\n}')
    B(C, S, 5, 'p',
      'Mã gần như y hệt bản "như ý muốn"! Nó chạy trên luồng Main nhưng không bao giờ chặn luồng Main. Ở dòng `getNewsFromApi()`, coroutine tạm dừng chứ không chặn. Trong lúc đó luồng Main vẽ vòng xoay loading, nhận chạm, chạy coroutine khác. Dữ liệu về thì coroutine lấy lại luồng Main và chạy tiếp từ dòng `sortedByDescending`. `viewModelScope` còn tự hủy coroutine khi ViewModel bị xoá, nên không rò.\n'
      'Một điều kiện quan trọng: `getNewsFromApi` phải là hàm `suspend` thật sự nhả luồng khi chờ, ví dụ hàm của Retrofit hay Room có hỗ trợ suspend, hoặc tự chuyển việc chặn sang luồng khác bằng `withContext(Dispatchers.IO)`. Chữ `suspend` tự nó không đưa việc sang luồng khác (xem phần Bug bên dưới).',
      'The code is almost identical to the "wished-for" version! It runs on the Main thread yet never blocks it. At the line `getNewsFromApi()`, the coroutine suspends rather than blocks. Meanwhile the Main thread draws the loading spinner, handles touches and runs other coroutines. When the data arrives, the coroutine takes the Main thread back and continues from the `sortedByDescending` line. `viewModelScope` also cancels the coroutine automatically when the ViewModel is cleared, so nothing leaks.\n'
      'One important condition: `getNewsFromApi` must be a `suspend` function that really releases the thread while waiting, for example a Retrofit or Room function with suspend support, or one that moves the blocking work to another thread with `withContext(Dispatchers.IO)`. The word `suspend` by itself does not move work to another thread (see Bugs below).')
    B(C, S, 6, 'p',
      'Marcin Moskała minh hoạ ý này bằng hai hàm `updateNews` và `updateProfile` chạy trong hai coroutine trên cùng luồng Main. Khi `updateNews` chờ mạng, luồng Main được `updateProfile` dùng. Khi dữ liệu tin về, `updateNews` giành lại luồng Main và chạy tiếp ngay sau `getNewsFromApi()`. Mô phỏng ngay dưới đây là phiên bản của site cho đúng tình huống đó: hai coroutine A và B dùng chung một dispatcher (đặt 1 luồng để giống luồng Main).',
      'Marcin Moskała illustrates this with two functions, `updateNews` and `updateProfile`, running in two coroutines on the same Main thread. While `updateNews` waits for the network, `updateProfile` uses the Main thread. When the news data arrives, `updateNews` takes the Main thread back and continues right after `getNewsFromApi()`. The simulation just below is this site\'s version of that situation: two coroutines A and B share one dispatcher (set it to 1 thread to match the Main thread).')
    B(C, S, 7, 'predict',
      'Trong mô phỏng: A và B dùng chung 1 luồng, A cần chờ 30 ms ở giữa. (1) Nếu A chờ bằng `delay(30)`, B được chạy lúc nào? (2) Nếu A chờ bằng `Thread.sleep(30)`, B được chạy lúc nào? Hãy trả lời trước, rồi bấm Step để kiểm.',
      'In the simulation: A and B share 1 thread, and A has to wait 30 ms in the middle. (1) If A waits with `delay(30)`, when does B get to run? (2) If A waits with `Thread.sleep(30)`, when does B get to run? Answer first, then press Step to check.')
    B(C, S, 7, 'ans',
      '(1) Ngay khi A tạm dừng: `delay` suspend coroutine và thả luồng, nên B dùng luồng trong lúc A chờ. Hết 30 ms, A xếp hàng chờ luồng rồi chạy tiếp. (2) Chỉ sau khi A ngủ xong: `Thread.sleep` chặn luồng, A giữ luồng suốt 30 ms, B phải đợi. Đây chính là khác biệt suspend và chặn luồng.',
      '(1) As soon as A suspends: `delay` suspends the coroutine and releases the thread, so B uses the thread while A waits. After 30 ms, A queues for the thread and continues. (2) Only after A finishes sleeping: `Thread.sleep` blocks the thread, A holds it for the full 30 ms, and B has to wait. This is exactly the difference between suspending and blocking.')

    S = 'parallel'
    a(C + '.sec.%s.title' % S, 'Ba endpoint: tuần tự, rồi song song với async', 'Three endpoints: sequential, then parallel with async')
    a(C + '.sec.%s.badge' % S, 'stable')
    B(C, S, 1, 'kt',
      'fun showNews() {\n    viewModelScope.launch {\n        val config = getConfigFromApi()      // 1 s\n        val news = getNewsFromApi(config)    // 1 s, cần config\n        val user = getUserFromApi()          // 1 s, KHÔNG cần config\n        view.showNews(user, news)\n    }\n}',
      'fun showNews() {\n    viewModelScope.launch {\n        val config = getConfigFromApi()      // 1 s\n        val news = getNewsFromApi(config)    // 1 s, needs config\n        val user = getUserFromApi()          // 1 s, does NOT need config\n        view.showNews(user, news)\n    }\n}')
    B(C, S, 2, 'p',
      'Dễ đọc, nhưng chưa tối ưu. Trong một coroutine, các lời gọi suspend chạy tuần tự: lời gọi sau chỉ bắt đầu khi lời gọi trước xong. Nếu mỗi lời gọi mất 1 giây thì tổng cộng 3 giây, dù `user` không phụ thuộc gì và lẽ ra có thể tải cùng lúc. Thư viện có `async`: khởi động ngay một coroutine con chạy việc đó, trả về một `Deferred`; lát sau gọi `await()` để lấy kết quả (suspend nếu chưa xong) ([[src:kt-composing]]).',
      'Easy to read, but not optimal. Inside one coroutine, suspending calls run sequentially: the next call starts only after the previous one finishes. If each call takes 1 second, the total is 3 seconds, even though `user` depends on nothing and could have been loaded at the same time. The library has `async`: it immediately starts a child coroutine that does that work and returns a `Deferred`; later you call `await()` to get the result (suspending if it is not ready yet) ([[src:kt-composing]]).')
    B(C, S, 3, 'kt',
      'fun showNews() {\n    viewModelScope.launch {\n        val config = async { getConfigFromApi() }\n        val news = async { getNewsFromApi(config.await()) }\n        val user = async { getUserFromApi() }\n        view.showNews(user.await(), news.await())\n    }\n}')
    B(C, S, 4, 'ask',
      'Với mỗi lời gọi mất 1 giây, phiên bản `async` ở trên mất khoảng bao lâu: 1, 2 hay 3 giây? Vì sao?',
      'With each call taking 1 second, about how long does the `async` version above take: 1, 2 or 3 seconds? Why?')
    B(C, S, 4, 'ans',
      'Khoảng 2 giây. `config` và `user` bắt đầu cùng lúc. `news` cũng khởi động ngay nhưng việc đầu tiên của nó là `config.await()`, nên phải chờ `config` xong (1 s) rồi mới tải tin (thêm 1 s). `user` xong ở giây thứ 1 và chờ sẵn. Đường dài nhất là config → news = 2 giây. Không thể là 1 giây vì news phụ thuộc config.',
      'About 2 seconds. `config` and `user` start at the same time. `news` also starts right away, but its first action is `config.await()`, so it has to wait for `config` to finish (1 s) before loading the news (another 1 s). `user` finishes at second 1 and waits. The longest path is config → news = 2 seconds. It cannot be 1 second, because news depends on config.')
    B(C, S, 5, 'p',
      'Coroutine không bắt bạn bỏ vòng lặp hay hàm xử lý collection quen thuộc. Tải mọi trang cùng lúc, hoặc tải lần lượt từng trang, chỉ khác nhau vài dòng:',
      'Coroutines do not make you give up loops or familiar collection functions. Loading every page at once, or loading pages one by one, differs by only a few lines:')
    B(C, S, 6, 'kt',
      '// tải mọi trang cùng lúc\nfun showAllNews() {\n    viewModelScope.launch {\n        val allNews = (0 until getNumberOfPages())\n            .map { page -> async { getNewsFromApi(page) } }   // khởi động hết\n            .flatMap { it.await() }                            // rồi chờ từng kết quả\n        view.showAllNews(allNews)\n    }\n}\n\n// tải lần lượt, hiện dần từng trang\nfun showPagesFromFirst() {\n    viewModelScope.launch {\n        for (page in 0 until getNumberOfPages()) {\n            val news = getNewsFromApi(page)\n            view.showNextPage(news)\n        }\n    }\n}',
      '// load every page at once\nfun showAllNews() {\n    viewModelScope.launch {\n        val allNews = (0 until getNumberOfPages())\n            .map { page -> async { getNewsFromApi(page) } }   // start them all\n            .flatMap { it.await() }                            // then wait for each result\n        view.showAllNews(allNews)\n    }\n}\n\n// load one after another, showing each page as it arrives\nfun showPagesFromFirst() {\n    viewModelScope.launch {\n        for (page in 0 until getNumberOfPages()) {\n            val news = getNewsFromApi(page)\n            view.showNextPage(news)\n        }\n    }\n}')
    B(C, S, 7, 'p',
      'Bên backend cũng vậy: chuyển từ luồng sang coroutine phần lớn chỉ là thêm `suspend` và dùng `coroutineScope { async { … } }` khi cần song song. Dáng mã hầu như không đổi, khác hẳn khi đưa RxJava vào.',
      'The backend is the same: moving from threads to coroutines is mostly a matter of adding `suspend` and using `coroutineScope { async { … } }` where you need parallelism. The shape of the code barely changes, unlike bringing in RxJava.')

    # ---- 6. Chi phí ----
    S = 'cost'
    a(C + '.sec.%s.title' % S, 'Luồng đắt, coroutine rẻ', 'Threads are expensive, coroutines are cheap')
    a(C + '.sec.%s.badge' % S, 'stable impl')
    B(C, S, 1, 'p',
      'Ngoài chuyện dễ viết còn một lý do nữa: luồng tốn kém. Mỗi luồng của JVM là một luồng của hệ điều hành, có stack riêng. Stack được dành sẵn khi tạo luồng, kích thước mặc định đặt bằng tuỳ chọn `-Xss` (trên JVM 64-bit thường là 1 MB). Luồng còn phải được hệ điều hành lập lịch và chuyển ngữ cảnh. Bộ nhớ dành sẵn chưa chắc đã dùng hết thật, nhưng nhiều luồng chỉ để ngồi chờ vẫn là tốn bộ nhớ và CPU vô ích.\n'
      'Hai đoạn dưới mô phỏng 100 000 yêu cầu, mỗi yêu cầu chờ 1 giây (như chờ cơ sở dữ liệu):',
      'Besides being easier to write, there is another reason: threads are costly. Each JVM thread is an operating-system thread with its own stack. The stack is reserved when the thread is created; its default size is set with the `-Xss` option (on a 64-bit JVM it is commonly 1 MB). Threads must also be scheduled and context-switched by the operating system. Reserved memory is not necessarily all used, but many threads that only sit and wait still waste memory and CPU.\n'
      'The two snippets below simulate 100,000 requests, each waiting 1 second (like waiting for a database):')
    B(C, S, 2, 'kt',
      'fun main() {\n    repeat(100_000) {\n        thread {\n            Thread.sleep(1000L)   // chặn: mỗi yêu cầu giữ một luồng\n            print(".")\n        }\n    }\n}',
      'fun main() {\n    repeat(100_000) {\n        thread {\n            Thread.sleep(1000L)   // blocks: each request holds a thread\n            print(".")\n        }\n    }\n}')
    B(C, S, 3, 'kt',
      'fun main() = runBlocking {\n    repeat(100_000) {\n        launch {\n            delay(1000L)          // suspend: không giữ luồng nào trong lúc chờ\n            print(".")\n        }\n    }\n}',
      'fun main() = runBlocking {\n    repeat(100_000) {\n        launch {\n            delay(1000L)          // suspend: holds no thread while waiting\n            print(".")\n        }\n    }\n}')
    B(C, S, 4, 'predict',
      'Chạy hai đoạn trên máy tính bình thường. Đoạn nào in xong 100 000 dấu chấm sau khoảng 1 giây? Đoạn còn lại có thể gặp chuyện gì?',
      'Run both snippets on an ordinary computer. Which one prints all 100,000 dots after about 1 second? What might happen to the other one?')
    B(C, S, 4, 'ans',
      'Đoạn coroutine: chờ khoảng 1 giây rồi in hết. Cả 100 000 coroutine cùng `delay` trên một luồng duy nhất (luồng của `runBlocking`); lúc chờ, mỗi coroutine chỉ là một đối tượng nhỏ trên heap. Đoạn luồng: mất lâu hơn nhiều để in hết, hoặc dừng với `OutOfMemoryError: unable to create native thread`, tuỳ máy và giới hạn của hệ điều hành. Thời gian cụ thể phụ thuộc máy, đừng coi là số đo chuẩn. Đừng thử đoạn luồng trên điện thoại.',
      'The coroutine snippet: waits about 1 second, then prints everything. All 100,000 coroutines `delay` on a single thread (the `runBlocking` thread); while waiting, each coroutine is just a small object on the heap. The thread snippet: takes much longer to print everything, or stops with `OutOfMemoryError: unable to create native thread`, depending on the machine and operating-system limits. Exact timings depend on the machine, so do not treat them as a benchmark. Do not try the thread snippet on a phone.')
    B(C, S, 5, 'note',
      'Vì sao coroutine đang chờ lại rẻ? Một coroutine đang suspend không có stack riêng. Trạng thái của nó (đang dừng ở đâu, biến cục bộ nào cần giữ) được compiler cất vào một đối tượng continuation trên heap. Khi resume, đối tượng đó được gọi lại trên một luồng nào đó. Chương "Coroutine dưới mui xe" sẽ mở đối tượng này ra xem (state machine và `label`). Chi tiết dạng mã sinh ra là implementation của compiler Kotlin, có thể đổi giữa các phiên bản.',
      'Why is a waiting coroutine cheap? A suspended coroutine has no stack of its own. Its state (where it stopped, which local variables must be kept) is stored by the compiler in a continuation object on the heap. On resume, that object is invoked again on some thread. The chapter "Coroutines under the hood" opens this object up (the state machine and `label`). The exact shape of the generated code is a Kotlin compiler implementation detail and may change between versions.')

    # ---- 7. Bug ----
    S = 'bugs'
    a(C + '.sec.%s.title' % S, 'Bug thường gặp ở giai đoạn này', 'Common bugs at this stage')
    a(C + '.sec.%s.badge' % S, 'stable')
    B(C, S, 1, 'p',
      'Mỗi thẻ dưới đây có triệu chứng thật. Hãy tự đoán nguyên nhân trước khi mở.',
      'Each card below has a real symptom. Try to guess the cause before opening it.')
    B(C, S, 2, 'bug',
      'Bạn viết `suspend fun parseHugeJson(text: String): Data`, gọi nó trong `viewModelScope.launch`. Giao diện vẫn khựng 400 ms mỗi lần parse.',
      'You write `suspend fun parseHugeJson(text: String): Data` and call it inside `viewModelScope.launch`. The UI still stutters for 400 ms every time it parses.')
    B(C, S, 2, 'cause',
      'Từ khoá `suspend` chỉ cho phép hàm có điểm tạm dừng. Nó không chuyển hàm sang luồng khác. Hàm không gọi một hàm suspend nào thật sự nhả luồng, nên toàn bộ 400 ms tính toán chạy trên dispatcher của coroutine gọi nó. `viewModelScope` dùng `Dispatchers.Main.immediate`, nên chính là luồng Main.',
      'The `suspend` keyword only lets a function have suspension points. It does not move the function to another thread. The function never calls a suspending function that really releases the thread, so all 400 ms of computation run on the dispatcher of the calling coroutine. `viewModelScope` uses `Dispatchers.Main.immediate`, so that is the Main thread.')
    B(C, S, 2, 'fix',
      'Đưa việc nặng CPU sang `Dispatchers.Default` bên trong hàm, để hàm "an toàn khi gọi từ Main" (main-safe).',
      'Move the CPU-heavy work to `Dispatchers.Default` inside the function, so the function is "safe to call from Main" (main-safe).')
    B(C, S, 2, 'fixkt',
      'suspend fun parseHugeJson(text: String): Data =\n    withContext(Dispatchers.Default) { parser.parse(text) }')
    B(C, S, 3, 'bug',
      'Trong coroutine chạy trên Main, bạn dùng `Thread.sleep(2000)` để "chờ 2 giây rồi ẩn thông báo". Suốt 2 giây đó cả màn hình đứng.',
      'In a coroutine running on Main, you use `Thread.sleep(2000)` to "wait 2 seconds and then hide the message". The whole screen freezes for those 2 seconds.')
    B(C, S, 3, 'cause',
      '`Thread.sleep` chặn luồng hiện tại, ở đây là luồng Main. Coroutine không thể "làm cho" một lời gọi chặn trở thành tạm dừng; chỉ hàm suspend như `delay` mới thả luồng.',
      '`Thread.sleep` blocks the current thread, here the Main thread. A coroutine cannot turn a blocking call into a suspension; only suspending functions such as `delay` release the thread.')
    B(C, S, 3, 'fix',
      'Dùng `delay(2000)`. Gặp API chặn mà bạn không sửa được (thư viện cũ, I/O đồng bộ) thì bọc nó trong `withContext(Dispatchers.IO) { … }`.',
      'Use `delay(2000)`. For blocking APIs you cannot change (old libraries, synchronous I/O), wrap them in `withContext(Dispatchers.IO) { … }`.')
    B(C, S, 4, 'bug',
      'Bạn viết `val a = async { loadA() }.await(); val b = async { loadB() }.await()` để tải song song, nhưng tổng thời gian vẫn bằng tổng hai lời gọi.',
      'You write `val a = async { loadA() }.await(); val b = async { loadB() }.await()` to load in parallel, but the total time is still the sum of both calls.')
    B(C, S, 4, 'cause',
      '`await()` được gọi ngay sau khi khởi động, nên coroutine cha tạm dừng chờ A xong rồi mới khởi động B. Hai việc vẫn lần lượt, chỉ thêm chi phí tạo coroutine.',
      '`await()` is called right after starting, so the parent coroutine suspends until A finishes before it even starts B. The two jobs still run one after another, with the extra cost of creating coroutines.')
    B(C, S, 4, 'fix',
      'Khởi động hết trước, chờ sau.',
      'Start everything first, wait afterwards.')
    B(C, S, 4, 'fixkt',
      'val a = async { loadA() }\nval b = async { loadB() }\nuse(a.await(), b.await())')
    B(C, S, 5, 'bug',
      'Bạn dùng `GlobalScope.launch { … }` trong Activity để tải dữ liệu. Xoay màn hình vài lần, mỗi lần một lượt tải mới chạy chồng lên, và LeakCanary báo Activity cũ bị rò.',
      'You use `GlobalScope.launch { … }` in an Activity to load data. After rotating the screen a few times, each rotation starts another overlapping load, and LeakCanary reports that old Activities leaked.')
    B(C, S, 5, 'cause',
      '`GlobalScope` không gắn với vòng đời nào, nên coroutine sống tới khi tự xong, giống hệt luồng ở Cách 1. Lambda giữ tham chiếu tới Activity đã bị huỷ khi xoay.',
      '`GlobalScope` is not tied to any lifecycle, so the coroutine lives until it finishes on its own, exactly like the thread in Approach 1. The lambda holds a reference to the Activity that was destroyed on rotation.')
    B(C, S, 5, 'fix',
      'Dùng scope có vòng đời: `viewModelScope` (sống qua xoay màn hình, hủy khi ViewModel bị xoá) hoặc `lifecycleScope` (hủy khi Activity/Fragment bị huỷ). Chương A2 và A8 giải thích chi tiết.',
      'Use a lifecycle-aware scope: `viewModelScope` (survives rotation, cancelled when the ViewModel is cleared) or `lifecycleScope` (cancelled when the Activity/Fragment is destroyed). Chapters A2 and A8 explain the details.')

    # ---- 8. Bài tập ----
    S = 'exercises'
    a(C + '.sec.%s.title' % S, 'Bài tập', 'Exercises')
    a(C + '.sec.%s.badge' % S, 'stable')
    B(C, S, 1, 'ex',
      'Ví dụ có lời giải sẵn: chuyển đoạn callback sau sang coroutine. Giả sử đã có các hàm suspend `getConfig()`, `getNews(config)`, `getUser()`. Đọc kỹ lời giải, chú ý cái gì biến mất.',
      'A worked example: convert the callback code below to coroutines. Assume the suspending functions `getConfig()`, `getNews(config)` and `getUser()` already exist. Read the solution carefully and notice what disappears.')
    B(C, S, 1, 'exkt',
      'fun refresh() {\n    showProgress()\n    getConfig { config ->\n        getNews(config) { news ->\n            getUser { user ->\n                view.show(user, news)\n                hideProgress()\n            }\n        }\n    }\n}')
    B(C, S, 1, 'sol',
      'Mỗi tầng lồng nhau biến thành một dòng `val`. `hideProgress()` đứng ngay sau `view.show(...)` theo đúng thứ tự đọc. Hủy tự động khi ViewModel bị xoá. `try/finally` bảo đảm luôn ẩn tiến trình, kể cả khi lỗi hoặc bị hủy; với callback thì phải nhớ ẩn ở mọi nhánh lỗi.',
      'Each nesting level becomes one `val` line. `hideProgress()` sits right after `view.show(...)`, in reading order. Cancellation is automatic when the ViewModel is cleared. `try/finally` guarantees the progress is always hidden, even on failure or cancellation; with callbacks you have to remember to hide it in every error branch.')
    B(C, S, 1, 'solkt',
      'fun refresh() {\n    viewModelScope.launch {\n        showProgress()\n        try {\n            val config = getConfig()\n            val news = getNews(config)\n            val user = getUser()\n            view.show(user, news)\n        } finally {\n            hideProgress()\n        }\n    }\n}')
    B(C, S, 2, 'ex',
      'Bài khuyết bước: sửa lời giải trên để `getUser()` chạy song song với cặp config → news. Chỉ cần đổi khoảng ba dòng.',
      'A partly-solved exercise: change the solution above so that `getUser()` runs in parallel with the config → news pair. You only need to change about three lines.')
    B(C, S, 2, 'hint',
      'Việc nào không phụ thuộc việc nào? Khởi động việc độc lập bằng `async` trước, `await` ở chỗ cần kết quả.',
      'Which job does not depend on which? Start the independent job with `async` first, and `await` where you need the result.')
    B(C, S, 2, 'sol',
      'Dùng `async` cho `getUser()` ngay đầu khối. Config → news vẫn tuần tự vì news cần config. Tổng thời gian ≈ max(config + news, user) thay vì config + news + user.',
      'Use `async` for `getUser()` at the start of the block. Config → news stays sequential because news needs config. Total time ≈ max(config + news, user) instead of config + news + user.')
    B(C, S, 2, 'solkt',
      'viewModelScope.launch {\n    showProgress()\n    try {\n        val user = async { getUser() }       // khởi động trước\n        val config = getConfig()\n        val news = getNews(config)\n        view.show(user.await(), news)        // chờ ở chỗ cần\n    } finally {\n        hideProgress()\n    }\n}',
      'viewModelScope.launch {\n    showProgress()\n    try {\n        val user = async { getUser() }       // start it first\n        val config = getConfig()\n        val news = getNews(config)\n        view.show(user.await(), news)        // wait where it is needed\n    } finally {\n        hideProgress()\n    }\n}')
    B(C, S, 3, 'ex',
      'Đoán output, theo đúng thứ tự in:',
      'Predict the output, in the exact order it is printed:')
    B(C, S, 3, 'exkt',
      'fun main() = runBlocking {\n    launch {\n        delay(100)\n        println("A")\n    }\n    println("B")\n    delay(200)\n    println("C")\n}')
    B(C, S, 3, 'hint',
      '`launch` chỉ khởi động coroutine con rồi trả về ngay; nó không đợi con chạy xong.',
      '`launch` only starts the child coroutine and returns right away; it does not wait for the child to finish.')
    B(C, S, 3, 'sol',
      'B, A, C. `launch` trả về ngay nên "B" in trước. Cha gặp `delay(200)` thì tạm dừng và thả luồng duy nhất của `runBlocking`. Con chạy tới `delay(100)`, cũng tạm dừng. Ở mốc 100 ms con chạy tiếp và in "A"; ở mốc 200 ms cha in "C". Cả hai coroutine dùng chung một luồng; thứ tự đến từ việc ai tạm dừng lúc nào, không phải từ việc có nhiều luồng.',
      'B, A, C. `launch` returns at once, so "B" prints first. The parent reaches `delay(200)`, suspends and releases the single `runBlocking` thread. The child runs up to `delay(100)` and suspends too. At 100 ms the child continues and prints "A"; at 200 ms the parent prints "C". Both coroutines share one thread; the order comes from who suspends when, not from having several threads.')

    # ---- 9. Tự trả lời ----
    S = 'recall'
    a(C + '.sec.%s.title' % S, 'Tự trả lời trước khi sang chương sau', 'Answer these before the next chapter')
    a(C + '.sec.%s.badge' % S, 'stable')
    B(C, S, 1, 'p',
      'Không xem lại phần trên. Trả lời bằng lời của bạn (nói thành tiếng hoặc viết ra), rồi mới mở đáp án. Việc tự nhớ lại giúp nhớ lâu hơn đọc lại.',
      'Do not look back at the sections above. Answer in your own words (out loud or in writing), and only then open the answer. Recalling on your own helps you remember longer than re-reading does.')
    B(C, S, 2, 'ask',
      'Vì sao trên Android không thể vừa "chờ mạng trên luồng Main" vừa "sửa view ở luồng khác"? Nêu đúng hai ràng buộc.',
      'Why, on Android, can you neither "wait for the network on the Main thread" nor "change views from another thread"? State exactly the two constraints.')
    B(C, S, 2, 'ans',
      '(1) Luồng Main xử lý chạm và vẽ khung hình nên không được chặn: gọi mạng ở đó ném `NetworkOnMainThreadException`, chặn lâu thì sinh ANR. (2) Bộ công cụ UI không thread-safe nên chỉ luồng tạo cây view (luồng Main) được sửa view, nếu không sẽ có `CalledFromWrongThreadException`.',
      '(1) The Main thread handles touches and draws frames, so it must not be blocked: a network call there throws `NetworkOnMainThreadException`, and long blocking causes an ANR. (2) The UI toolkit is not thread-safe, so only the thread that created the view hierarchy (the Main thread) may change views, or you get `CalledFromWrongThreadException`.')
    B(C, S, 3, 'ask',
      'Giải thích bằng một câu cho người chưa học: "suspend" khác "chặn luồng" ở đâu?',
      'Explain in one sentence to someone who has not studied this: how does "suspending" differ from "blocking a thread"?')
    B(C, S, 3, 'ans',
      'Chặn luồng là luồng đứng chờ, không làm được việc gì khác. Suspend là coroutine cất lại chỗ đang dở rồi trả luồng cho việc khác, có kết quả thì tiếp tục từ chỗ đó.',
      'Blocking means the thread stands and waits and can do nothing else. Suspending means the coroutine saves where it was and hands the thread back for other work, then continues from that point when the result is ready.')
    B(C, S, 4, 'ask',
      'Mỗi cách (luồng thủ công, callback, RxJava) giải được gì và vướng ở đâu? Coroutine giữ được điểm mạnh nào của RxJava mà bỏ được điểm yếu nào?',
      'What does each approach (manual threads, callbacks, RxJava) solve, and where does it get stuck? Which RxJava strength do coroutines keep, and which weakness do they drop?')
    B(C, S, 4, 'ans',
      'Luồng thủ công: chạy được nhưng không hủy được, tốn luồng, rò. Callback: không chặn nhưng khó hủy, khó song song, lồng nhau, khó điều khiển thứ tự. RxJava: hủy được, đổi luồng đúng, song song tốt, nhưng phức tạp, phải học nhiều operator và đổi cấu trúc mã. Coroutine giữ được hủy, chọn luồng và song song (qua scope, dispatcher, `async`), nhưng bỏ được độ phức tạp vì mã vẫn thẳng như mã đồng bộ.',
      'Manual threads: work, but cannot be cancelled, waste threads and leak. Callbacks: non-blocking, but hard to cancel, hard to parallelize, nested, and hard to control order. RxJava: cancellable, correct thread switching, good parallelism, but complex, with many operators to learn and a restructured codebase. Coroutines keep cancellation, thread choice and parallelism (through scopes, dispatchers and `async`), but drop the complexity, because the code stays straight like synchronous code.')

    # ---- quiz ----
    for q, qv, qe, av, ae, wv, we in [
        ('q1', 'Thêm `suspend` vào một hàm tính toán nặng có làm nó chạy ngoài luồng Main không?', 'Does adding `suspend` to a heavy computation make it run off the Main thread?',
         'Không.', 'No.',
         '`suspend` chỉ cho phép có điểm tạm dừng. Luồng do dispatcher quyết định; muốn rời Main thì dùng `withContext(Dispatchers.Default)`.', '`suspend` only allows suspension points. The thread is decided by the dispatcher; to leave Main, use `withContext(Dispatchers.Default)`.'),
        ('q2', 'Trong lúc một coroutine đang `delay(1000)` trên luồng Main, luồng Main làm gì?', 'While a coroutine is in `delay(1000)` on the Main thread, what does the Main thread do?',
         'Nó rảnh để vẽ, nhận chạm và chạy coroutine khác.', 'It is free to draw, handle touches and run other coroutines.',
         'Coroutine đã tạm dừng và thả luồng; hết thời gian nó được xếp lịch chạy tiếp trên Main.', 'The coroutine has suspended and released the thread; when the time is up it is scheduled to continue on Main.'),
        ('q3', 'Ba lời gọi suspend độc lập, mỗi lời 1 giây, viết lần lượt trong một `launch`. Tổng thời gian? Làm sao giảm?', 'Three independent suspending calls, 1 second each, written one after another in one `launch`. Total time? How do you reduce it?',
         'Khoảng 3 giây; khởi động cả ba bằng `async` rồi mới `await` thì còn khoảng 1 giây.', 'About 3 seconds; start all three with `async` and only then `await`, and it drops to about 1 second.',
         'Trong một coroutine, lời gọi suspend chạy tuần tự; `async` tạo coroutine con chạy đồng thời.', 'Inside one coroutine, suspending calls run sequentially; `async` creates child coroutines that run concurrently.')]:
        a(C + '.quiz.%s.q' % q, qv, qe); a(C + '.quiz.%s.a' % q, av, ae); a(C + '.quiz.%s.why' % q, wv, we)
