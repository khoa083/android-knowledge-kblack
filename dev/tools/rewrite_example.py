# Ví dụ mẫu cho quy trình viết lại (chương A3 coroutines, đã xong): chỉ để xem cách dùng RW.block2, không cần chạy lại.
import sys
sys.path.insert(0, 'E:/AndroidDeepDiveExplorer/dev/tools')
from rewrite_helper import RW
r = RW('E:/AndroidDeepDiveExplorer/dev/gen/coroutines_v2_a3.py')
r.block2('runblocking', 1, 'p',
         'Quy tắc chung là coroutine không bao giờ chặn luồng, chỉ tạm dừng. Nhưng có chỗ cần chặn, như hàm `main`: nếu không chặn, chương trình kết thúc trước khi coroutine kịp chạy. `runBlocking` chạy một coroutine mới và chặn luồng hiện tại cho tới khi coroutine đó xong ([[src:kx-runblocking]]). Vì vậy `delay(1000L)` bên trong `runBlocking` đối với luồng gọi nó thì giống hệt `Thread.sleep(1000L)`.\n'
         'Quy tắc dễ nhớ: `runBlocking` là cái cửa từ thế giới chặn sang thế giới coroutine; chỉ mở nó ở `main` và trong test.',
         'The general rule is that coroutines never block a thread, they only suspend. But some places need blocking, such as `main`: without it, the program would end before the coroutine got a chance to run. `runBlocking` runs a new coroutine and blocks the current thread until that coroutine finishes ([[src:kx-runblocking]]). So for the thread that calls it, `delay(1000L)` inside `runBlocking` behaves exactly like `Thread.sleep(1000L)`.\n'
         'Rule of thumb: `runBlocking` is the door from the blocking world into the coroutine world; open it only in `main` and in tests.')
r.block2('async', 1, 'p',
         '`async` giống `launch`, nhưng được thiết kế để tạo ra một giá trị: giá trị ở dòng cuối của lambda. Nó trả về `Deferred<T>`, một "phiếu hẹn" cho giá trị sẽ có; hàm suspend `await()` trả giá trị khi nó sẵn sàng ([[src:kx-async]]).\n'
         'Giống `launch`, `async` khởi động coroutine NGAY khi được gọi. `Deferred` giữ giá trị sau khi có, nên gọi `await()` sau đó thì trả về ngay; gọi trước thì tạm dừng cho tới khi có.\n'
         'Hình dung: `async` là gửi đồ đi giặt và cầm phiếu; `await` là đưa phiếu ra lấy đồ, nếu chưa xong thì ngồi chờ.',
         '`async` is like `launch`, but designed to produce a value: the value on the lambda\'s last line. It returns a `Deferred<T>`, a "claim ticket" for a value to come; the suspending `await()` returns the value once it is ready ([[src:kx-async]]).\n'
         'Like `launch`, `async` starts the coroutine IMMEDIATELY when called. A `Deferred` keeps the value once it has it, so an `await()` afterwards returns at once; an earlier one suspends until the value is there.\n'
         'Picture it: `async` is dropping off laundry and getting a ticket; `await` is handing in the ticket to collect it, waiting if it is not ready yet.')
r.block2('async', 4, 'p',
         'Thay mọi `launch` bằng `async` thì mã vẫn chạy, nhưng đừng làm vậy. `async` nói với người đọc "ở đây có một giá trị". Không cần giá trị thì dùng `launch`.\n'
         'Cách dùng `async` điển hình là chạy song song hai nguồn dữ liệu rồi ghép lại. Việc chạy sau cùng không cần bọc `async`, vì coroutine hiện tại tự làm được.\n'
         'Quy tắc dễ nhớ: cần kết quả thì `async`, không cần thì `launch`.',
         'Replacing every `launch` with `async` still works, but do not do it. `async` tells the reader "there is a value here". If you do not need a value, use `launch`.\n'
         'The typical use of `async` is running two data sources in parallel and combining them. The last piece of work need not be wrapped in `async`, because the current coroutine can do it itself.\n'
         'Rule of thumb: need a result, use `async`; no result needed, use `launch`.')
r.block2('scopefn', 1, 'p',
         'Trong một hàm suspend, ta tạm dừng được, nhưng không có scope để gọi `async`. Truyền scope vào làm tham số không phải cách hay (chương "Scope functions" giải thích vì sao). Thay vào đó, dùng `coroutineScope { }`: một hàm suspend tạo scope cho lambda của nó và trả về giá trị của lambda, giống `let`, `run`, `runBlocking` ([[src:kx-coroutinescope]]). Nó chỉ xong khi mọi con bên trong đã xong.\n'
         'Quy tắc dễ nhớ: trong hàm suspend mà cần chạy song song thì mở `coroutineScope { }`.',
         'Inside a suspending function you can suspend, but you have no scope to call `async` on. Passing a scope in as a parameter is not a good idea (the "Scope functions" chapter explains why). Instead, use `coroutineScope { }`: a suspending function that creates a scope for its lambda and returns the lambda\'s value, like `let`, `run`, `runBlocking` ([[src:kx-coroutinescope]]). It finishes only when every child inside has finished.\n'
         'Rule of thumb: inside a suspending function, when you need parallel work, open a `coroutineScope { }`.')
r.save()
