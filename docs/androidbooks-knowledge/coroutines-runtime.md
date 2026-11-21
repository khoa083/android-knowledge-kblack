# Kotlin Coroutines — ghi chú cơ chế

## Mô hình cốt lõi

Coroutine là một computation có thể tạm dừng và tiếp tục. Nó không phải một OS/JVM thread. Trên JVM, thread vẫn là phương tiện để thực thi mã; compiler và coroutine library biểu diễn điểm tiếp tục bằng continuation/state-machine và lập lịch nó lên thread phù hợp. Nhiều coroutine có thể dùng chung thread; một hàm `suspend` cũng có thể hoàn tất ngay mà không suspend thật.

```text
Kotlin suspend code
  → compiler CPS/state machine
  → continuation giữ state qua điểm suspend
  → coroutine library/dispatcher điều phối resume
  → OS thread chạy đoạn code tiếp theo
```

### Đọc một suspension

Ví dụ do người viết tạo:

```kotlin
suspend fun loadProfile(id: Id): Profile {
    val token = readToken()       // suspension point 1
    val user = fetchUser(id, token) // suspension point 2
    return Profile(user)
}
```

Để có thể tiếp tục sau một điểm suspend, compiler phải biểu diễn trạng thái cần giữ: đang ở nhánh nào, kết quả/exception trả về từ lời gọi suspend, tham số/local nào còn được dùng sau đó, và continuation của caller. Đây là mô hình; tên field, số label, inline/crossinline optimization và bytecode thật phụ thuộc compiler/version.

Nếu lời gọi có thể suspend thật, kết quả đặc biệt `COROUTINE_SUSPENDED` là handshake giữa hàm được transform và caller runtime. Khi đó các frame bình thường unwind khỏi thread stack; continuation lưu đường đi để resume sau. Nếu callee trả kết quả đồng bộ, execution có thể đi tiếp ngay trên stack hiện tại. Khi resume, kết quả có thể thành value hoặc exception được ném tại điểm nối tương ứng.

Không nói “toàn bộ coroutine là một Continuation object” như định nghĩa chính xác: state-machine continuation là một phần quan trọng của triển khai suspend functions; builders/scopes/Jobs/dispatchers và library wrappers cũng tham gia vòng đời thực.

## Các lớp cần phân biệt

| Khái niệm | Trả lời câu hỏi | Không có nghĩa là |
|---|---|---|
| `suspend` / compiler support | Hàm có thể nhường và tiếp tục qua `Continuation` như thế nào? | Tự tạo thread, tự chọn IO hay tự chạy song song |
| `CoroutineContext` | Coroutine mang metadata/dispatcher/job/handler nào? | Bộ scheduler tự nó |
| `CoroutineDispatcher` | Tiếp tục thực thi ở đâu/khi nào được dispatch? | Chủ sở hữu lifecycle |
| `Job` / scope | Công việc thuộc cây nào; hoàn tất/hủy/lỗi ra sao? | OS thread handle |
| `Flow` | Dòng dữ liệu suspendable được collect và xử lý thế nào? | Coroutine tự chạy trước collector (đối với cold `flow {}`) |

`CoroutineContext + element` là phép ghép theo key: element bên phải thay element trùng key. Builder tạo coroutine con và nối Job với parent; không nên mô tả child relationship như hệ quả thuần túy của toán tử `+`. `withContext` là structured context switch đợi khối hoàn tất; nó không thay `launch`/`async` khi cần các nhánh concurrent.

## Structured concurrency, lỗi và hủy

- Parent đợi child hoàn tất. Hủy parent truyền xuống cây child.
- Child lỗi thông thường có thể làm hủy parent và sibling theo quy tắc Job; supervisor giới hạn lan truyền từ child lên parent nhưng vẫn có hành vi riêng với child thất bại.
- `launch` trả `Job`; exception không nằm trong call stack đồng bộ của câu lệnh gọi `launch`. `async` trả `Deferred`, exception quan sát qua `await`, nhưng lỗi child vẫn ảnh hưởng Job tree theo scope.
- Cancellation hợp tác. Suspension points có cancellation check; vòng lặp CPU không suspend cần tự kiểm tra `isActive`, `ensureActive()` hoặc `yield()`.
- `finally` thường chạy khi hủy; một suspend call trong vùng đã cancelled có thể lập tức ném `CancellationException`. Dùng `withContext(NonCancellable)` chỉ cho cleanup suspend ngắn cần thiết, không che cancellation chung.
- `CoroutineExceptionHandler` không thay `try/catch` và không phải “handler cục bộ” cho mọi child.

## Flow và backpressure

- Cold `flow {}` chạy theo collector; `emit` và operator thường đi tuần tự trong cùng pipeline cho tới khi operator như `buffer`/`flowOn` tạo ranh giới thực thi phù hợp.
- `emit` suspend tạo backpressure tự nhiên khi không có buffer: producer đợi consumer.
- `buffer`, `conflate`, `collectLatest`, `flowOn` có semantics khác nhau; không gộp chúng thành một “tăng tốc flow”.
- `StateFlow` giữ state mới nhất và conflates theo equality; `SharedFlow` phát theo cấu hình replay/capacity/overflow; `Channel` là primitive truyền phần tử với các policy capacity/receive.
- Flow context preservation và exception transparency là các quy tắc observable; dùng `flowOn` cho upstream, không phát tùy tiện từ context khác trong builder.

## Android và Compose

- `viewModelScope` và lifecycle scopes xác định ownership; chọn `repeatOnLifecycle`/`collectAsStateWithLifecycle` theo API và UI lifecycle.
- Thiết kế suspend API main-safe: caller không cần nhớ dispatcher nội bộ; tác vụ blocking/CPU được chuyển đúng dispatcher tại tầng thực hiện.
- Trong Compose, `LaunchedEffect(keys)` gắn coroutine với vị trí composition và key; rời composition hoặc đổi key sẽ cancel/restart. Callback UI thường dùng `rememberCoroutineScope` khi coroutine chỉ cần bắt đầu từ event.
- Animation cũng dùng suspend/coroutine để lấy frame và tiến đến target; cancellation/restart của effect có thể tác động trực tiếp animation.

## Lỗi phổ biến: triệu chứng → cơ chế → sửa

| Triệu chứng | Cơ chế cần kiểm tra | Hướng sửa |
|---|---|---|
| Cancel rồi vòng lặp CPU vẫn chạy | Không có suspension/check cancellation | Thêm check hợp tác theo nhịp công việc |
| `try/catch` không bắt exception từ `launch` | Exception phát sinh sau khi `launch` trả về | Đặt handler/ownership đúng, dùng `async/await` chỉ khi phù hợp semantics |
| UI quay vòng sau khi rời màn | Scope sống lâu hơn lifecycle UI | Chọn scope/lifecycle owner đúng và cancel collection đúng lúc |
| Network block Main | API không main-safe hoặc blocking | Đưa blocking vào dispatcher phù hợp ở tầng repository/data source |
| Flow chạy nhiều lần | Cold flow được collect nhiều lần hoặc effect key đổi | Xác định collector count/lifecycle và sharing policy |
| `async` sibling bị hủy trước `await` | Child failure lan qua parent Job ngay | Dùng supervisor nếu nghiệp vụ thật sự yêu cầu cô lập lỗi; vẫn xử lý kết quả |

## Sách đã đối chiếu

### *Kotlin Coroutines: Deep Dive* — PDF trong `E:\AndroidBooks`

PDF outline ghi 4 phần: Understanding Kotlin Coroutines; Kotlin Coroutines library; Channel and Flow; Kotlin Coroutines in practice. Chương/điểm bắt đầu theo **số trang PDF trong bookmark** (trang in có thể lệch):

- Ch.1 “Why Kotlin Coroutines?” p.14; Ch.2 “Sequence builder” p.27; Ch.3 “How does suspension work?” p.33; Ch.4 “Coroutines under the hood” p.45; Ch.5 “built-in support vs library” p.63.
- Builders p.66; context p.82; jobs p.94; cancellation p.107; exception p.122; scope functions p.133; dispatchers p.153; scope construction p.173; shared state p.183; testing p.198.
- Channel p.235; select p.257; hot/cold p.263; Flow intro p.271; understanding/building/processing/lifecycle p.283–318; SharedFlow/StateFlow p.345; testing Flow p.359.
- Practice/use cases p.377; recipes p.402; language interoperability p.417; launching vs suspending p.430; best practices p.434.
- Nội dung CPS/state machine đã kiểm tra tại PDF pp.45–63 (printed book pp.39–57): spilled locals, `label`, continuation chain/call-stack analogy, resumed values/exceptions và ví dụ `BaseContinuationImpl` của Kotlin 1.5.30. Pseudocode trong sách tự ghi là simplified; implementation mẫu có version cũ.

### *Kotlin Coroutines by Tutorials* — PDF trong `E:\AndroidBooks`

- Ch.1 asynchronous programming pp.22–39; Ch.3 getting started p.52; Ch.4 suspend functions p.66; Ch.5 async/await p.89; context p.112; dispatch p.119; exception p.130; cancellation p.144.
- Sequence/iterators `yield` p.157; Flow p.171; SharedFlow/StateFlow p.185; testing p.199; Android p.211; UI lifecycle/flow collection p.234; networking p.244; persistence p.254; ViewModel/Compose/testing on Android p.267.
- Dùng làm ví dụ Android bổ trợ; xác minh API/lifecycle theo docs hiện hành trước khi dạy.

## Nguồn kiểm chứng

- [Kotlin Coroutines Guide](https://kotlinlang.org/docs/coroutines-guide.html), [basics](https://kotlinlang.org/docs/coroutines-basics.html), [context and dispatchers](https://kotlinlang.org/docs/coroutine-context-and-dispatchers.html), [cancellation](https://kotlinlang.org/docs/coroutines-cancellation.html), [Flow](https://kotlinlang.org/docs/coroutines-flow.html).
- [Coroutines on Android](https://developer.android.com/kotlin/coroutines), [best practices](https://developer.android.com/kotlin/coroutines/coroutines-best-practices).
- [Kotlin KEEP coroutine proposal](https://github.com/Kotlin/KEEP/blob/master/proposals/coroutines.md).
- [kotlinx.coroutines source](https://github.com/Kotlin/kotlinx.coroutines) — implementation only; inspect the tag/commit matching the dependency under discussion.
