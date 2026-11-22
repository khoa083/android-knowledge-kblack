# Coroutines v2 · U4 Coroutine dưới mui xe (Deep Dive, "Coroutines under the hood" tr. PDF 45–62 và "built-in support vs library" tr. 63–64)
# + chuỗi của sim coroutines.sm. Được dev/gen/coroutines_content.py nạp. Khung: docs/chapter-template-v2.md.

def add(a):
    def B(ch, sec, n, field, vi, en=None):
        a('%s.sec.%s.b.%02d.%s' % (ch, sec, n, field), vi, vi if en is None else en)
    m = lambda k, vi, en=None: a('m.sm.' + k, vi, en)

    # ---------------- sim coroutines.sm ----------------
    m('title', 'printUser sau khi biên dịch: state machine với label', 'printUser after compilation: a state machine with a label')
    m('overview', 'Hàm `printUser(token)` có hai lời gọi suspend, nên compiler chia nó thành ba trạng thái (label 0, 1, 2). Bấm Step và theo dõi dải chỉ số: đó chính là các trường của đối tượng continuation (`label`, `userId`, `result`), cùng giá trị hàm trả về và trạng thái luồng.',
      'The function `printUser(token)` has two suspending calls, so the compiler splits it into three states (label 0, 1, 2). Press Step and watch the metric strip: those are the fields of the continuation object (`label`, `userId`, `result`), plus the value the function returns and the state of the thread.')
    m('wrapup', 'Mỗi lần suspend, hàm trả `COROUTINE_SUSPENDED` và luồng được thả; trạng thái nằm trọn trong continuation. Mỗi lần resume, continuation gọi lại CHÍNH hàm đó; nhờ `label`, hàm nhảy thẳng tới đoạn sau điểm suspend và lấy kết quả từ `result`. Xong thì continuation resume người gọi (completion).',
      'Each time it suspends, the function returns `COROUTINE_SUSPENDED` and the thread is released; the state lives entirely in the continuation. Each time it resumes, the continuation calls the SAME function again; thanks to `label`, the function jumps straight to the part after the suspension point and takes the result from `result`. When done, the continuation resumes its caller (the completion).')
    m('simp.1', 'Mã là bản giản lược của mã thật (theo cách trình bày của Deep Dive). Mã compiler sinh ra dùng `when`/`switch`, lớp ẩn danh kế thừa `ContinuationImpl` và nhiều tối ưu; xem bằng Tools › Kotlin › Show Kotlin Bytecode › Decompile.', 'The code is a simplified version of the real code (following Deep Dive\'s presentation). Compiler output uses `when`/`switch`, an anonymous class extending `ContinuationImpl`, and many optimizations; view it with Tools › Kotlin › Show Kotlin Bytecode › Decompile.')
    m('simp.2', 'Thẻ "người gọi" gộp cả chuỗi completion phía trên (coroutine builder hoặc hàm suspend gọi printUser).', 'The "caller" card stands for the whole completion chain above (the coroutine builder or the suspending function that called printUser).')
    m('ctl.hint', 'So ba trường hợp: cả hai lời gọi suspend; getUserId có kết quả ngay; getUserName lỗi.', 'Compare three cases: both calls suspend; getUserId has its result immediately; getUserName fails.')
    m('ctl.mode', 'Tình huống', 'Scenario')
    m('ctl.mode.suspend', 'Cả hai lời gọi đều suspend', 'Both calls suspend')
    m('ctl.mode.now', 'getUserId có kết quả ngay (cache)', 'getUserId returns at once (cache)')
    m('ctl.mode.fail', 'getUserName resume bằng exception', 'getUserName resumes with an exception')
    m('diagramTitle', 'State machine của printUser', 'The state machine of printUser')
    m('diagramDesc', 'Người gọi, ba trạng thái label 0 đến 2, và đối tượng continuation', 'The caller, three states label 0 to 2, and the continuation object')
    for k, vi, en in [('call', 'Người gọi (completion)', 'Caller (completion)'), ('l0', 'label 0: từ đầu tới getUserId', 'label 0: start to getUserId'),
                      ('l1', 'label 1: sau getUserId', 'label 1: after getUserId'), ('l2', 'label 2: sau getUserName', 'label 2: after getUserName'),
                      ('cont', 'PrintUserContinuation', 'PrintUserContinuation')]:
        m('n.' + k, vi, en)
    for k, vi, en in [('call', 'gọi', 'call'), ('l1', 'resume → label 1', 'resume → label 1'), ('l2', 'resume → label 2', 'resume → label 2'), ('done', 'completion.resumeWith', 'completion.resumeWith')]:
        m('e.' + k, vi, en)
    for k, vi, en in [('label', 'label', 'label'), ('userId', 'cont.userId', 'cont.userId'), ('result', 'cont.result', 'cont.result'), ('ret', 'printUser trả về', 'printUser returns'), ('th', 'Luồng', 'Thread')]:
        m('met.' + k, vi, en)
    for k, vi, en in [('none', '—', '—'), ('susp', 'COROUTINE_SUSPENDED', 'COROUTINE_SUSPENDED'), ('unit', 'Unit', 'Unit'), ('thrown', 'ném ApiException', 'throws ApiException'),
                      ('okId', 'success("u42")', 'success("u42")'), ('okName', 'success("Ana")', 'success("Ana")'), ('fail', 'failure(ApiException)', 'failure(ApiException)'),
                      ('id', '"u42"', '"u42"'), ('busy', 'đang chạy printUser', 'running printUser'), ('free', 'được thả (rảnh)', 'released (free)')]:
        m('v.' + k, vi, en)
    for k, vi, en in [('waiting', 'đang chờ', 'waiting'), ('resumed', 'được resume', 'resumed'), ('failed', 'nhận lỗi', 'got the failure'),
                      ('idle', 'chưa tới', 'not reached'), ('running', 'đang chạy', 'running'), ('suspended', 'suspended ở đây', 'suspended here'), ('done', 'đã qua', 'passed'),
                      ('label0', 'label = 0', 'label = 0'), ('label1', 'label = 1', 'label = 1'), ('label2', 'label = 2', 'label = 2')]:
        m('st.' + k, vi, en)
    m('scope.busy', 'luồng đang chạy', 'thread running')
    m('scope.free', 'luồng đã thả', 'thread released')
    S = [
        ('call', 'Gọi printUser: bọc continuation', 'Call printUser: wrap the continuation',
         'Lần gọi đầu, tham số `continuation` là của người gọi, chưa phải `PrintUserContinuation`, nên hàm tạo một `PrintUserContinuation` bọc nó (`label = 0`, giữ `token`).', 'On the first call, the `continuation` parameter belongs to the caller, not a `PrintUserContinuation`, so the function creates a `PrintUserContinuation` that wraps it (`label = 0`, keeping `token`).'),
        ('l0', 'label 0: in "Before", đặt label = 1 rồi gọi getUserId', 'label 0: print "Before", set label = 1, call getUserId',
         '`label` được đặt thành 1 TRƯỚC khi gọi hàm suspend, để lần resume sau bắt đầu ngay sau lời gọi này. Continuation của printUser được truyền xuống `getUserId` như tham số cuối.', '`label` is set to 1 BEFORE calling the suspending function, so the next resume starts right after this call. printUser\'s continuation is passed down to `getUserId` as the last parameter.'),
        ('susp1', 'getUserId trả COROUTINE_SUSPENDED → printUser cũng trả', 'getUserId returns COROUTINE_SUSPENDED → so does printUser',
         'Hàm thoát ra thật sự: call stack được giải phóng, luồng rảnh. Mọi thứ cần nhớ (label = 1, token) nằm trong continuation trên heap.', 'The function really exits: the call stack is unwound and the thread is free. Everything that needs remembering (label = 1, token) is in the continuation on the heap.'),
        ('l0now', 'getUserId trả "u42" ngay: rơi thẳng xuống label 1', 'getUserId returns "u42" at once: fall straight through to label 1',
         'Không có `COROUTINE_SUSPENDED`, nên hàm lưu `result = success("u42")` và đi tiếp vào khối `label == 1` trong CÙNG lần gọi. Luồng không bị thả; hàm cư xử như hàm thường.', 'There is no `COROUTINE_SUSPENDED`, so the function stores `result = success("u42")` and carries on into the `label == 1` block in the SAME call. The thread is never released; the function behaves like an ordinary one.'),
        ('resume1', 'Resume: continuation gọi lại printUser', 'Resume: the continuation calls printUser again',
         'getUserId xong và gọi `cont.resumeWith(success("u42"))`. `resumeWith` cất kết quả vào `result` rồi gọi lại `printUser(token, this)`. Lần này tham số đã là `PrintUserContinuation`, nên hàm dùng lại nó; đọc lại `result`, `userId`; `label == 1` nên bỏ qua khối đầu.', 'getUserId finishes and calls `cont.resumeWith(success("u42"))`. `resumeWith` stores the result in `result` and calls `printUser(token, this)` again. This time the parameter is already a `PrintUserContinuation`, so the function reuses it, reloads `result` and `userId`, and skips the first block because `label == 1`.'),
        ('l1', 'label 1: lấy userId, cất vào continuation, gọi getUserName', 'label 1: take userId, store it in the continuation, call getUserName',
         '`userId = result.getOrThrow()`. Vì `userId` còn cần ở trạng thái 2, nó được cất vào `cont.userId` trước khi suspend lần nữa. `label = 2`.', '`userId = result.getOrThrow()`. Because `userId` is still needed in state 2, it is stored in `cont.userId` before suspending again. `label = 2`.'),
        ('susp2', 'getUserName suspend → printUser trả COROUTINE_SUSPENDED', 'getUserName suspends → printUser returns COROUTINE_SUSPENDED', 'Luồng lại được thả. Continuation giữ label = 2 và userId = "u42".', 'The thread is released again. The continuation holds label = 2 and userId = "u42".'),
        ('resume2', 'Resume lần 2: label 2, in User', 'Second resume: label 2, print the User', '`result = success("Ana")`. Khối `label == 2` lấy tên, in `User(u42, Ana)` rồi "After".', '`result = success("Ana")`. The `label == 2` block takes the name, prints `User(u42, Ana)`, then "After".'),
        ('ret', 'Trả Unit → resume người gọi', 'Return Unit → resume the caller',
         'printUser trả `Unit` (không phải `COROUTINE_SUSPENDED`), nên `resumeWith` gọi `completion.resumeWith(success(Unit))`: người gọi chạy tiếp, theo đúng cơ chế đó, lên tới đỉnh.', 'printUser returns `Unit` (not `COROUTINE_SUSPENDED`), so `resumeWith` calls `completion.resumeWith(success(Unit))`: the caller continues, by the same mechanism, all the way to the top.'),
        ('resumeFail', 'Resume bằng failure: getOrThrow ném ra', 'Resume with a failure: getOrThrow throws',
         'getUserName gọi `resumeWith(failure(ApiException))`. Ở khối `label == 2`, `result.getOrThrow()` ném exception, đúng tại vị trí lời gọi suspend trong mã nguồn.', 'getUserName calls `resumeWith(failure(ApiException))`. In the `label == 2` block, `result.getOrThrow()` throws the exception, exactly at the suspending call\'s position in the source.'),
        ('completeFail', 'resumeWith bắt lỗi → người gọi nhận failure', 'resumeWith catches it → the caller gets a failure',
         'Exception thoát khỏi printUser; `resumeWith` bắt nó, bọc thành `Result.failure(e)` và gọi `completion.resumeWith(...)`. Ở hàm gọi, nó lại bị ném ra từ điểm suspend, giống hệt exception đi ngược call stack bình thường.', 'The exception escapes printUser; `resumeWith` catches it, wraps it as `Result.failure(e)` and calls `completion.resumeWith(...)`. In the calling function it is thrown again from the suspension point, just like an exception travelling up a normal call stack.'),
    ]
    for sid, tv, te, xv, xe in S:
        m('s.%s.title' % sid, tv, te); m('s.%s.explain' % sid, xv, xe); m('ev.' + sid, tv, te)
    for k, vi, en in [
        ('wrap', '"as? PrintUserContinuation ?: PrintUserContinuation(...)": lần đầu thì bọc, lần resume thì dùng lại. Đó là cách hàm biết mình đang bắt đầu hay đang chạy tiếp.', '"as? PrintUserContinuation ?: PrintUserContinuation(...)": wrap on the first call, reuse on resume. That is how the function knows whether it is starting or continuing.'),
        ('labelFirst', 'Đặt label trước khi gọi: nếu đợi tới sau lời gọi thì đã muộn, vì hàm có thể thoát ngay ở dòng đó.', 'Set the label before the call: after the call is too late, because the function may exit right at that line.'),
        ('unwind', 'COROUTINE_SUSPENDED truyền lên mọi hàm suspend phía trên cho tới builder hoặc hàm `resume`. Thế là cả chuỗi kết thúc và luồng tự do.', 'COROUTINE_SUSPENDED propagates up through every suspending function above it, until it reaches the builder or the `resume` function. The whole chain ends and the thread is free.'),
        ('fallThrough', 'Đây là vì sao hàm suspend có kết quả sẵn (cache) gần như rẻ như hàm thường: không suspend, không thả luồng.', 'This is why a suspending function whose result is ready (a cache) is almost as cheap as an ordinary function: no suspension, no thread release.'),
        ('reuse', 'Resume = gọi lại CÙNG hàm với CÙNG continuation. Không có "nhảy vào giữa hàm" bằng phép màu: chỉ là các khối `if (label == …)`.', 'Resuming = calling the SAME function with the SAME continuation. There is no magic "jump into the middle of a function": just `if (label == …)` blocks.'),
        ('store', 'Chỉ biến còn cần ở trạng thái sau mới được cất vào continuation. Biến không còn dùng sau điểm suspend thì không được giữ.', 'Only variables still needed in a later state are stored in the continuation. A variable no longer used after the suspension point is not kept.'),
        ('throwHere', 'Lỗi xuất hiện ở đúng dòng gọi hàm suspend, nên `try/catch` quanh lời gọi bắt được như mã đồng bộ.', 'The error appears at exactly the line that calls the suspending function, so a `try/catch` around the call catches it just like synchronous code.'),
        ('failUp', 'Exception đi ngược chuỗi continuation y như đi ngược call stack.', 'The exception travels back up the continuation chain exactly as it would up a call stack.'),
        ('completion', 'Chuỗi continuation đóng vai call stack: mỗi continuation giữ tham chiếu tới continuation của hàm đã gọi nó (completion).', 'The continuation chain plays the role of the call stack: each continuation holds a reference to the continuation of the function that called it (its completion).')]:
        m('co.' + k, vi, en)
    a('cap.sm', 'Ba thẻ hình thoi là ba trạng thái của printUser (label 0, 1, 2), đi từ trái sang phải; thẻ dưới là đối tượng continuation (ghi label hiện tại); thẻ trái là người gọi. Dải chỉ số phía trên là các trường của continuation. Đoán trước giá trị label và "printUser trả về" ở mỗi bước.',
      'The three diamond cards are printUser\'s three states (label 0, 1, 2), left to right; the card below is the continuation object (showing the current label); the left card is the caller. The metric strip above shows the continuation\'s fields. Predict the label and "printUser returns" values before each step.')

    # ---------------- chương U4 ----------------
    C = 'u4'
    a(C + '.title', 'Coroutine dưới mui xe: CPS, state machine, continuation', 'Coroutines under the hood: CPS, state machines, continuations')
    a(C + '.essence',
      'Không có phép màu: compiler biến mỗi hàm `suspend` thành một hàm thường nhận thêm tham số `Continuation` (continuation-passing style) và một state machine. Mỗi điểm suspend chia hàm thành một trạng thái; số hiệu trạng thái (`label`) và biến cục bộ còn cần dùng được cất trong đối tượng continuation.\n'
      'Khi suspend, hàm trả về giá trị đặc biệt `COROUTINE_SUSPENDED`, mọi hàm phía trên cũng trả về theo, và luồng được thả. Khi resume, continuation gọi lại chính hàm đó; nhờ `label`, hàm chạy tiếp từ sau điểm suspend.\n'
      'Mỗi continuation giữ tham chiếu tới continuation của hàm đã gọi nó, nên chuỗi continuation đóng vai call stack. Hiểu ba ý này là đọc được stack trace, bộ nhớ bị giữ và lý do một số biến "biến mất" trong debugger.',
      'There is no magic: the compiler turns each `suspend` function into an ordinary function that takes an extra `Continuation` parameter (continuation-passing style) and contains a state machine. Each suspension point splits the function into a state; the state number (`label`) and the local variables still needed are stored in the continuation object.\n'
      'When it suspends, the function returns the special value `COROUTINE_SUSPENDED`, every function above it returns too, and the thread is released. When it resumes, the continuation calls that same function again; thanks to `label`, the function continues after the suspension point.\n'
      'Each continuation holds a reference to the continuation of the function that called it, so the continuation chain plays the role of the call stack. Understand these three ideas and you can read stack traces, see what memory is retained, and know why some variables "disappear" in the debugger.')
    a(C + '.goal.g1', 'Đã thấy label được đặt TRƯỚC lời gọi suspend', 'Saw the label being set BEFORE the suspending call')
    a(C + '.goal.g2', 'Đã đi hết state machine tới khi người gọi được resume', 'Followed the state machine until the caller is resumed')

    S = 'recap'
    a(C + '.sec.%s.title' % S, 'Ôn nhanh chương trước', 'Quick review of the previous chapter')
    B(C, S, 1, 'ask', 'Lambda của `suspendCoroutine` nhận gì, chạy lúc nào? Không ai gọi `resume` thì sao?', 'What does the `suspendCoroutine` lambda receive, and when does it run? What happens if nobody calls `resume`?')
    B(C, S, 1, 'ans', 'Nhận continuation, chạy ngay trước khi suspend. Không ai resume thì coroutine dừng mãi (treo).', 'It receives the continuation and runs right before suspending. If nobody resumes, the coroutine stays stopped forever (hangs).')

    S = 'lessons'
    a(C + '.sec.%s.title' % S, 'Ba ý cần mang theo', 'Three ideas to take away')
    a(C + '.sec.%s.badge' % S, 'impl simplified')
    B(C, S, 1, 'p',
      'Chương này không giới thiệu công cụ mới; nó giải thích coroutine chạy thế nào, ở mức giản lược nhưng đúng bản chất. Ba ý chính:\n'
      '1. Hàm suspend giống một state machine: có một trạng thái ở đầu hàm và một trạng thái sau mỗi lời gọi hàm suspend.\n'
      '2. Số hiệu trạng thái (`label`) và dữ liệu cục bộ được giữ trong đối tượng continuation.\n'
      '3. Continuation của một hàm bọc (decorate) continuation của hàm gọi nó, nên cả chuỗi continuation biểu diễn call stack, được dùng khi resume hoặc khi một hàm đã resume chạy xong.',
      'This chapter introduces no new tools; it explains how coroutines work, simplified but true to the essence. The three key ideas:\n'
      '1. A suspending function is like a state machine: one state at the start of the function and one after each suspending call.\n'
      '2. The state number (`label`) and the local data are kept in the continuation object.\n'
      '3. A function\'s continuation decorates the continuation of its caller, so the whole chain of continuations represents the call stack, used when resuming or when a resumed function completes.')
    B(C, S, 2, 'note',
      'Mọi đoạn mã "dưới mui xe" trong chương là bản Kotlin giản lược của bytecode, theo cách trình bày của Deep Dive. Mã thật có thêm tối ưu và cơ chế khác (stack trace tốt hơn, interception, bỏ biến không dùng) và có thể đổi giữa các phiên bản compiler. Hãy dùng nó để hiểu cơ chế, không dựa vào tên lớp hay hình dạng mã cụ thể.',
      'All the "under the hood" code in this chapter is a simplified Kotlin rendering of bytecode, following Deep Dive\'s presentation. The real code has extra optimizations and mechanisms (better stack traces, interception, removal of unused variables) and can change between compiler versions. Use it to understand the mechanism; do not rely on specific class names or code shapes.')
    B(C, S, 2, 'kind', 'source')

    S = 'cps'
    a(C + '.sec.%s.title' % S, 'Continuation-passing style: tham số ẩn cuối cùng', 'Continuation-passing style: the hidden last parameter',)
    a(C + '.sec.%s.badge' % S, 'impl')
    B(C, S, 1, 'p',
      'Có nhiều cách hiện thực hàm suspend; đội Kotlin chọn continuation-passing style (CPS): continuation được truyền từ hàm này sang hàm khác như một tham số, theo quy ước ở vị trí cuối cùng ([[src:kt-design]]):',
      'There are several ways to implement suspending functions; the Kotlin team chose continuation-passing style (CPS): the continuation is passed from function to function as a parameter, by convention in the last position ([[src:kt-design]]):')
    B(C, S, 2, 'kt',
      'suspend fun getUser(): User?\nsuspend fun setUser(user: User)\nsuspend fun checkAvailability(flight: Flight): Boolean\n\n// dưới mui xe:\nfun getUser(continuation: Continuation<*>): Any?\nfun setUser(user: User, continuation: Continuation<*>): Any\nfun checkAvailability(flight: Flight, continuation: Continuation<*>): Any',
      'suspend fun getUser(): User?\nsuspend fun setUser(user: User)\nsuspend fun checkAvailability(flight: Flight): Boolean\n\n// under the hood:\nfun getUser(continuation: Continuation<*>): Any?\nfun setUser(user: User, continuation: Continuation<*>): Any\nfun checkAvailability(flight: Flight, continuation: Continuation<*>): Any')
    B(C, S, 3, 'predict', 'Để ý kiểu trả về đổi thành `Any`/`Any?`. Vì sao không giữ nguyên `User?` hay `Boolean`?', 'Notice the return type changes to `Any`/`Any?`. Why not keep `User?` or `Boolean`?')
    B(C, S, 3, 'ans', 'Vì hàm có thể suspend, và khi suspend nó không trả `User?` mà trả một dấu hiệu đặc biệt: `COROUTINE_SUSPENDED`. Kiểu trả về phải là kiểu cha gần nhất của `User?` và kiểu của dấu hiệu đó (`Any`), tức là `Any?`. Nếu Kotlin có union type, có thể viết là `User? | COROUTINE_SUSPENDED`.', 'Because the function may suspend, and when it does it returns not a `User?` but a special marker: `COROUTINE_SUSPENDED`. The return type must be the closest common supertype of `User?` and the marker\'s type (`Any`), which is `Any?`. If Kotlin had union types, it could be `User? | COROUTINE_SUSPENDED`.')
    B(C, S, 4, 'note',
      'Hệ quả thực tế: gọi hàm suspend từ Java thì thấy đúng chữ ký này, gồm tham số `Continuation` cuối cùng và kiểu `Object`. Vì vậy thư viện cho Java thường bọc hàm suspend thành `CompletableFuture` hoặc callback (Deep Dive, chương "Using coroutines from other languages").',
      'A practical consequence: calling a suspending function from Java shows exactly this signature, with a trailing `Continuation` parameter and an `Object` return type. That is why libraries for Java usually wrap suspending functions as a `CompletableFuture` or a callback (Deep Dive, chapter "Using coroutines from other languages").')
    B(C, S, 4, 'kind', 'android')

    S = 'simple'
    a(C + '.sec.%s.title' % S, 'Một hàm rất đơn giản: label và COROUTINE_SUSPENDED', 'A very simple function: label and COROUTINE_SUSPENDED')
    a(C + '.sec.%s.badge' % S, 'impl simplified')
    B(C, S, 1, 'kt', 'suspend fun myFunction() {\n    println("Before")\n    delay(1000) // suspend\n    println("After")\n}')
    B(C, S, 2, 'p',
      'Chữ ký dưới mui xe là `fun myFunction(continuation: Continuation<*>): Any`. Hàm cần continuation RIÊNG để nhớ trạng thái của nó; tạm gọi là `MyFunctionContinuation` (thật ra là một object ẩn danh). Đầu thân hàm, nó bọc continuation nhận vào, nhưng chỉ khi chưa bọc. Nếu tham số đã là `MyFunctionContinuation` thì đây là lần resume, phải dùng lại nguyên vẹn:',
      'The signature under the hood is `fun myFunction(continuation: Continuation<*>): Any`. The function needs its OWN continuation to remember its state; let us call it `MyFunctionContinuation` (really it is an anonymous object). At the start of its body it wraps the continuation it received, but only if it has not been wrapped yet. If the parameter is already a `MyFunctionContinuation`, this is a resume, and it must be reused unchanged:')
    B(C, S, 3, 'kt', 'val continuation = continuation as? MyFunctionContinuation\n    ?: MyFunctionContinuation(continuation)')
    B(C, S, 4, 'p',
      'Hàm có thể bắt đầu từ hai chỗ: từ đầu (lần gọi đầu) hoặc ngay sau điểm suspend (lần resume). Trường `label` cho biết chỗ nào: lúc đầu bằng 0; trước mỗi điểm suspend nó được đặt thành trạng thái kế tiếp. Bản giản lược hoàn chỉnh:',
      'The function can start from two places: the beginning (first call) or right after the suspension point (resume). The `label` field says which: it starts at 0, and before each suspension point it is set to the next state. The complete simplified version:')
    B(C, S, 5, 'kt',
      'fun myFunction(continuation: Continuation<Unit>): Any {\n    val continuation = continuation as? MyFunctionContinuation\n        ?: MyFunctionContinuation(continuation)\n\n    if (continuation.label == 0) {\n        println("Before")\n        continuation.label = 1\n        if (delay(1000, continuation) == COROUTINE_SUSPENDED) {\n            return COROUTINE_SUSPENDED\n        }\n    }\n    if (continuation.label == 1) {\n        println("After")\n        return Unit\n    }\n    error("Impossible")\n}\n\nclass MyFunctionContinuation(val completion: Continuation<Unit>) : Continuation<Unit> {\n    override val context: CoroutineContext get() = completion.context\n    var label = 0\n    var result: Result<Any>? = null\n\n    override fun resumeWith(result: Result<Unit>) {\n        this.result = result\n        val res = try {\n            val r = myFunction(this)\n            if (r == COROUTINE_SUSPENDED) return\n            Result.success(r as Unit)\n        } catch (e: Throwable) {\n            Result.failure(e)\n        }\n        completion.resumeWith(res)\n    }\n}')
    B(C, S, 6, 'p',
      'Mảnh quan trọng cuối: khi `delay` suspend, nó trả `COROUTINE_SUSPENDED`; `myFunction` trả lại đúng giá trị đó; hàm gọi `myFunction` cũng vậy, và cứ thế lên tới đỉnh: builder (`launch`…) hoặc hàm `resume`. Đó là cách suspension kết thúc cả chuỗi hàm và để luồng rảnh cho việc khác. Còn nếu `delay` (giả sử) trả `Unit` thì hàm chỉ đơn giản chạy tiếp sang trạng thái sau, như hàm thường.',
      'The last important piece: when `delay` suspends, it returns `COROUTINE_SUSPENDED`; `myFunction` returns that same value; so does the function that called `myFunction`, and so on up to the top: the builder (`launch`…) or the `resume` function. That is how suspension ends the whole chain of functions and leaves the thread free for other work. And if `delay` (hypothetically) returned `Unit`, the function would simply move on to the next state, like an ordinary function.')
    B(C, S, 7, 'ask', 'Trong `resumeWith` ở trên, chuyện gì xảy ra khi `myFunction(this)` trả `COROUTINE_SUSPENDED`? Khi trả `Unit`? Khi ném exception?', 'In the `resumeWith` above, what happens when `myFunction(this)` returns `COROUTINE_SUSPENDED`? When it returns `Unit`? When it throws?')
    B(C, S, 7, 'ans', '`COROUTINE_SUSPENDED`: `return` luôn, vì hàm lại suspend và sẽ có lần resume khác. `Unit`: hàm xong, gọi `completion.resumeWith(success(Unit))` để người gọi chạy tiếp. Exception: bắt lại, gọi `completion.resumeWith(failure(e))`, và người gọi sẽ thấy exception ném ra tại điểm suspend của nó.', '`COROUTINE_SUSPENDED`: `return` immediately, because the function suspended again and another resume will come. `Unit`: the function is done, so call `completion.resumeWith(success(Unit))` to let the caller continue. An exception: catch it and call `completion.resumeWith(failure(e))`, and the caller will see the exception thrown at its own suspension point.')
    B(C, S, 8, 'note', 'Tự xem: trong IntelliJ IDEA / Android Studio, mở file, chọn Tools › Kotlin › Show Kotlin Bytecode, rồi bấm Decompile để thấy mã Java tương đương. Bạn sẽ thấy `label`, `COROUTINE_SUSPENDED` và một `switch` trên label.', 'See for yourself: in IntelliJ IDEA / Android Studio, open the file, choose Tools › Kotlin › Show Kotlin Bytecode, then click Decompile to see equivalent Java. You will find `label`, `COROUTINE_SUSPENDED`, and a `switch` on the label.')
    B(C, S, 8, 'kind', 'try')

    S = 'state'
    a(C + '.sec.%s.title' % S, 'Biến cục bộ sống qua điểm suspend: cất vào continuation', 'Local variables that survive a suspension: stored in the continuation')
    a(C + '.sec.%s.badge' % S, 'impl simplified')
    B(C, S, 1, 'kt', 'suspend fun myFunction() {\n    println("Before")\n    var counter = 0\n    delay(1000) // suspend\n    counter++\n    println("Counter: $counter")\n    println("After")\n}')
    B(C, S, 2, 'p',
      '`counter` cần ở cả trạng thái 0 và 1, nên phải được giữ trong continuation. Nó được CẤT ngay trước khi suspend và NẠP LẠI ở đầu hàm:',
      '`counter` is needed in both state 0 and state 1, so it must be kept in the continuation. It is STORED right before suspending and RELOADED at the start of the function:')
    B(C, S, 3, 'kt',
      'fun myFunction(continuation: Continuation<Unit>): Any {\n    val continuation = continuation as? MyFunctionContinuation\n        ?: MyFunctionContinuation(continuation)\n    var counter = continuation.counter          // nạp lại\n\n    if (continuation.label == 0) {\n        println("Before")\n        counter = 0\n        continuation.counter = counter          // cất trước khi suspend\n        continuation.label = 1\n        if (delay(1000, continuation) == COROUTINE_SUSPENDED) return COROUTINE_SUSPENDED\n    }\n    if (continuation.label == 1) {\n        counter = (counter as Int) + 1\n        println("Counter: $counter")\n        println("After")\n        return Unit\n    }\n    error("Impossible")\n}',
      'fun myFunction(continuation: Continuation<Unit>): Any {\n    val continuation = continuation as? MyFunctionContinuation\n        ?: MyFunctionContinuation(continuation)\n    var counter = continuation.counter          // reload\n\n    if (continuation.label == 0) {\n        println("Before")\n        counter = 0\n        continuation.counter = counter          // store before suspending\n        continuation.label = 1\n        if (delay(1000, continuation) == COROUTINE_SUSPENDED) return COROUTINE_SUSPENDED\n    }\n    if (continuation.label == 1) {\n        counter = (counter as Int) + 1\n        println("Counter: $counter")\n        println("After")\n        return Unit\n    }\n    error("Impossible")\n}')

    S = 'value'
    a(C + '.sec.%s.title' % S, 'Hàm được resume với giá trị: printUser', 'A function resumed with a value: printUser')
    a(C + '.sec.%s.badge' % S, 'impl simplified')
    B(C, S, 1, 'kt', 'suspend fun printUser(token: String) {\n    println("Before")\n    val userId = getUserId(token)              // suspend\n    println("Got userId: $userId")\n    val userName = getUserName(userId, token)  // suspend\n    println(User(userId, userName))\n    println("After")\n}')
    B(C, S, 2, 'p',
      'Hai lời gọi suspend → ba trạng thái. Continuation phải giữ: `token` (cần ở trạng thái 0 và 1), `userId` (cần ở 1 và 2), và `result` kiểu `Result`, cho biết hàm được resume thế nào. Nếu là `Result.success(value)`, hàm lấy `value` dùng tiếp; nếu là `Result.failure(e)`, `getOrThrow()` ném `e` ra.',
      'Two suspending calls → three states. The continuation must keep: `token` (needed in states 0 and 1), `userId` (needed in 1 and 2), and `result` of type `Result`, which says how the function was resumed. If it is `Result.success(value)`, the function takes `value` and carries on; if it is `Result.failure(e)`, `getOrThrow()` throws `e`.')
    B(C, S, 3, 'predict',
      'Trước khi bấm Step trong mô phỏng bên dưới: ở mỗi lần suspend, `label` bằng bao nhiêu và `printUser` trả về gì? Nếu `getUserId` có kết quả ngay (cache), có bao nhiêu lần luồng được thả?',
      'Before pressing Step in the simulation below: at each suspension, what is `label`, and what does `printUser` return? If `getUserId` has its result immediately (a cache), how many times is the thread released?')
    B(C, S, 3, 'ans',
      'Lần suspend đầu: `label = 1`, trả `COROUTINE_SUSPENDED`. Lần hai: `label = 2`, trả `COROUTINE_SUSPENDED`. Cuối cùng trả `Unit`. Nếu `getUserId` trả ngay "u42" thì chỉ có MỘT lần luồng được thả (ở `getUserName`): hàm rơi thẳng từ khối label 0 xuống khối label 1 trong cùng lần gọi. Chọn "getUserId có kết quả ngay" để kiểm.',
      'First suspension: `label = 1`, returns `COROUTINE_SUSPENDED`. Second: `label = 2`, returns `COROUTINE_SUSPENDED`. Finally it returns `Unit`. If `getUserId` returns "u42" at once, the thread is released only ONCE (at `getUserName`): the function falls straight from the label-0 block into the label-1 block within the same call. Pick "getUserId returns at once" to check.')

    S = 'stack'
    a(C + '.sec.%s.title' % S, 'Chuỗi continuation thay cho call stack', 'The continuation chain replaces the call stack')
    a(C + '.sec.%s.badge' % S, 'impl simplified')
    B(C, S, 1, 'p',
      'Khi hàm `a` gọi `b`, máy ảo cất trạng thái của `a` và địa chỉ quay về trên call stack. Nhưng khi suspend, ta thả luồng, nên call stack bị dọn sạch; lúc resume, call stack cũ không còn. Thay vào đó, continuation đóng vai call stack. Mỗi continuation giữ: chỗ đang dừng (`label`), biến cục bộ và tham số (các trường), và tham chiếu tới continuation của hàm đã gọi nó (`completion`). Continuation này trỏ tới continuation khác, cứ thế: như một củ hành nhiều lớp.',
      'When function `a` calls `b`, the virtual machine stores `a`\'s state and the return address on the call stack. But when we suspend, we free the thread, so the call stack is cleared; at resume, the old call stack is gone. Instead, continuations play the role of the call stack. Each continuation keeps: where it stopped (`label`), local variables and parameters (fields), and a reference to the continuation of the function that called it (`completion`). That continuation points to another, and so on: like an onion with many layers.')
    B(C, S, 2, 'kt',
      'suspend fun a() {\n    val user = readUser()\n    b()\n    b()\n    b()\n    println(user)\n}\n\nsuspend fun b() {\n    for (i in 1..10) {\n        c(i)\n    }\n}\n\nsuspend fun c(i: Int) {\n    delay(i * 100L)\n    println("Tick")\n}')
    B(C, S, 3, 'kt', 'CContinuation(\n    i = 4,\n    label = 1,\n    completion = BContinuation(\n        i = 4,\n        label = 1,\n        completion = AContinuation(\n            label = 2,\n            user = User@1234,\n            completion = ...\n        )\n    )\n)')
    B(C, S, 4, 'predict', 'Nhìn chuỗi continuation trên (giả sử `readUser` không phải hàm suspend): "Tick" đã được in bao nhiêu lần?', 'Looking at the continuation chain above (assume `readUser` is not a suspending function): how many times has "Tick" been printed already?')
    B(C, S, 4, 'ans',
      '13 lần. `AContinuation` có `label = 2`: `a` đã qua lời gọi `b()` thứ nhất (label 1 = đang ở `b()` đầu, label 2 = đang ở `b()` thứ hai), nên một lượt `b` đã xong, tức 10 Tick. Trong `b` hiện tại `i = 4`, đang chờ `c(4)`, nên `c(1)`, `c(2)`, `c(3)` đã in 3 Tick. Tổng 13.',
      '13 times. `AContinuation` has `label = 2`: `a` is past the first `b()` call (label 1 = inside the first `b()`, label 2 = inside the second), so one run of `b` has finished, which is 10 Ticks. In the current `b`, `i = 4` and it is waiting in `c(4)`, so `c(1)`, `c(2)` and `c(3)` printed 3 Ticks. 13 in total.')
    B(C, S, 5, 'p',
      'Khi resume: continuation của `c` gọi lại hàm `c`; `c` xong thì continuation đó resume continuation của `b`, nó gọi lại `b`; `b` xong thì resume continuation của `a`… cho tới đỉnh. Exception cũng đi đường đó: exception không bắt được bị bắt trong `resumeWith`, bọc thành `Result.failure(e)`, rồi hàm gọi được resume với kết quả này.',
      'On resume: `c`\'s continuation calls `c` again; when `c` finishes, that continuation resumes `b`\'s continuation, which calls `b` again; when `b` finishes, it resumes `a`\'s continuation… up to the top. Exceptions travel the same road: an uncaught exception is caught in `resumeWith`, wrapped as `Result.failure(e)`, and the calling function is resumed with that result.')

    S = 'actual'
    a(C + '.sec.%s.title' % S, 'Mã thật và chi phí', 'The actual code and its cost')
    a(C + '.sec.%s.badge' % S, 'impl version')
    B(C, S, 1, 'p',
      'Mã thật phức tạp hơn vì có thêm: stack trace của exception đẹp hơn, cơ chế chặn (interception) để dispatcher can thiệp khi resume, và tối ưu ở nhiều mức (bỏ biến không dùng, tối ưu tail call). Trong `BaseContinuationImpl` (stdlib; Deep Dive trích bản Kotlin 1.5.30), `resumeWith` dùng một vòng `while (true)` thay vì đệ quy: chạy `invokeSuspend` của continuation hiện tại; nếu ra `COROUTINE_SUSPENDED` thì `return`; nếu xong thì chuyển sang `completion` và lặp lại. Nhờ vậy resume một chuỗi dài không làm call stack phình ra.',
      'The real code is more complex because it adds: better exception stack traces, an interception mechanism so a dispatcher can step in on resume, and optimizations at several levels (removing unused variables, tail-call optimization). In `BaseContinuationImpl` (stdlib; Deep Dive quotes the Kotlin 1.5.30 version), `resumeWith` uses a `while (true)` loop instead of recursion: it runs the current continuation\'s `invokeSuspend`; if that yields `COROUTINE_SUSPENDED` it `return`s; if it finishes, it moves on to `completion` and loops again. That way resuming a long chain does not grow the call stack.')
    B(C, S, 2, 'kt',
      '// rút gọn từ BaseContinuationImpl.resumeWith (kotlin-stdlib; mã thật có thêm debug probe và releaseIntercepted)\nvar current = this\nvar param = result\nwhile (true) {\n    val completion = current.completion!!\n    val outcome: Result<Any?> = try {\n        val o = current.invokeSuspend(param)\n        if (o === COROUTINE_SUSPENDED) return\n        Result.success(o)\n    } catch (e: Throwable) {\n        Result.failure(e)\n    }\n    if (completion is BaseContinuationImpl) {\n        current = completion; param = outcome      // lên một tầng, không đệ quy\n    } else {\n        completion.resumeWith(outcome); return      // tới đỉnh (coroutine)\n    }\n}',
      '// condensed from BaseContinuationImpl.resumeWith (kotlin-stdlib; the real code adds a debug probe and releaseIntercepted)\nvar current = this\nvar param = result\nwhile (true) {\n    val completion = current.completion!!\n    val outcome: Result<Any?> = try {\n        val o = current.invokeSuspend(param)\n        if (o === COROUTINE_SUSPENDED) return\n        Result.success(o)\n    } catch (e: Throwable) {\n        Result.failure(e)\n    }\n    if (completion is BaseContinuationImpl) {\n        current = completion; param = outcome      // up one level, no recursion\n    } else {\n        completion.resumeWith(outcome); return      // reached the top (the coroutine)\n    }\n}')
    B(C, S, 3, 'p',
      'Chi phí: chia hàm thành trạng thái rẻ (so số và nhảy gần như không tốn gì). Cất trạng thái vào continuation cũng rẻ: không sao chép dữ liệu, chỉ thêm tham chiếu trỏ tới cùng vùng nhớ. Thứ tốn kém duy nhất là tạo đối tượng continuation, và vẫn không đáng lo. Nếu bạn không lo hiệu năng của RxJava hay callback, thì càng không cần lo hiệu năng của hàm suspend.',
      'Cost: splitting a function into states is cheap (comparing a number and jumping cost almost nothing). Storing state in the continuation is cheap too: no data is copied, it just adds references to the same memory. The only thing that costs anything is creating the continuation object, and even that is no big deal. If you do not worry about the performance of RxJava or callbacks, you certainly need not worry about suspending functions.')

    S = 'library'
    a(C + '.sec.%s.title' % S, 'Hỗ trợ của ngôn ngữ và thư viện kotlinx.coroutines', 'Built-in language support vs the kotlinx.coroutines library')
    a(C + '.sec.%s.badge' % S, 'stable')
    B(C, S, 1, 'p',
      'Coroutine gồm hai phần khác hẳn nhau:\n'
      '• Hỗ trợ có sẵn trong ngôn ngữ: compiler (biến đổi CPS/state machine) cùng vài phần tử tối thiểu trong thư viện chuẩn, gói `kotlin.coroutines`: từ khoá `suspend`, `Continuation`, `suspendCoroutine`, `createCoroutine`… Rất ít, rất tự do, có thể dựng lại hầu như mọi phong cách lập trình đồng thời; nhưng khó dùng trực tiếp, chủ yếu dành cho người viết thư viện.\n'
      '• Thư viện `kotlinx.coroutines`: một dependency riêng, gói `kotlinx.coroutines`, xây trên phần hỗ trợ trên. Nó cung cấp `launch`, `async`, `Deferred`, `Job`, dispatcher, `Flow`… và một phong cách cụ thể (structured concurrency), dùng trực tiếp được.\n'
      'Hai phần gần như luôn đi cùng nhau, nhưng không bắt buộc. Đội Kotlin đã dùng phần hỗ trợ có sẵn để thử dựng lại phong cách đồng thời của nhiều ngôn ngữ (như goroutine của Go) trước khi chọn phong cách hiện tại. Từ chương sau, ta tập trung vào `kotlinx.coroutines`.',
      'Coroutines consist of two very different parts:\n'
      '• Built-in language support: the compiler (the CPS/state-machine transformation) plus a few minimal elements in the standard library, package `kotlin.coroutines`: the `suspend` keyword, `Continuation`, `suspendCoroutine`, `createCoroutine`… Very little, very free, able to reproduce almost any concurrency style; but hard to use directly, and meant mainly for library authors.\n'
      '• The `kotlinx.coroutines` library: a separate dependency, package `kotlinx.coroutines`, built on top of that support. It provides `launch`, `async`, `Deferred`, `Job`, dispatchers, `Flow`… and one concrete style (structured concurrency), ready for direct use.\n'
      'The two nearly always go together, but they do not have to. The Kotlin team used the built-in support to try reproducing the concurrency styles of many languages (such as Go\'s goroutines) before settling on the current style. From the next chapter on, we focus on `kotlinx.coroutines`.')

    S = 'bugs'
    a(C + '.sec.%s.title' % S, 'Bug mà hiểu "dưới mui xe" mới sửa được', 'Bugs you can only fix if you know what is under the hood')
    a(C + '.sec.%s.badge' % S, 'impl')
    B(C, S, 1, 'bug',
      'Màn hình xem ảnh tốn bộ nhớ bất thường: `val bitmap = decode(bytes)` rồi `val meta = api.loadMeta(id)` (suspend, mạng chậm) rồi `show(bitmap, meta)`. Heap dump cho thấy hàng chục bitmap lớn bị giữ khi người dùng lướt nhanh.',
      'An image screen uses unusually much memory: `val bitmap = decode(bytes)`, then `val meta = api.loadMeta(id)` (suspending, slow network), then `show(bitmap, meta)`. A heap dump shows dozens of large bitmaps retained when the user scrolls fast.')
    B(C, S, 1, 'cause', '`bitmap` còn được dùng SAU điểm suspend, nên compiler cất nó vào continuation. Suốt thời gian chờ mạng, mỗi coroutine đang suspend giữ một bitmap trên heap. Nhiều coroutine chờ cùng lúc thì giữ nhiều bitmap.', '`bitmap` is still used AFTER the suspension point, so the compiler stores it in the continuation. For the whole network wait, every suspended coroutine holds a bitmap on the heap. Many coroutines waiting at once hold many bitmaps.')
    B(C, S, 1, 'fix', 'Đổi thứ tự để dữ liệu lớn không "sống" qua điểm suspend: chờ mạng trước, decode sau. Hoặc hủy coroutine cũ khi item rời màn hình (`collectLatest`, hủy Job theo item).', 'Reorder so that large data does not "live" across the suspension point: wait for the network first, decode afterwards. Or cancel the old coroutine when the item leaves the screen (`collectLatest`, cancelling the per-item Job).')
    B(C, S, 1, 'fixkt', 'val meta = api.loadMeta(id)      // suspend trước\nval bitmap = decode(bytes)       // rồi mới tạo dữ liệu lớn\nshow(bitmap, meta)')
    B(C, S, 2, 'bug',
      'Đặt breakpoint sau một lời gọi suspend, debugger báo một biến cục bộ là "optimized out" hoặc không hiện, dù dòng trên vừa dùng nó.',
      'You set a breakpoint after a suspending call, and the debugger says a local variable is "optimized out" or does not show it, even though the line above just used it.')
    B(C, S, 2, 'cause', 'Biến đó không còn được dùng sau điểm suspend, nên compiler không cất nó vào continuation (tối ưu "bỏ biến không dùng"). Sau khi resume, giá trị của nó đơn giản là không còn.', 'That variable is not used after the suspension point, so the compiler does not store it in the continuation (the "remove unused variables" optimization). After resuming, its value simply no longer exists.')
    B(C, S, 2, 'fix', 'Hiểu rằng đây là hành vi đúng, không phải mất dữ liệu: vòng đời của biến đã được rút ngắn. Khi cần debug, tạm dùng biến đó sau điểm suspend (ví dụ log), hoặc bật tuỳ chọn compiler `-Xdebug` để tắt tối ưu này ([[src:kt-debugidea]]). Tài liệu Kotlin cảnh báo: KHÔNG dùng `-Xdebug` cho bản phát hành, vì nó có thể gây rò bộ nhớ (chính lý do ở bug phía trên: biến bị giữ lâu hơn).', 'Understand that this is correct behaviour, not data loss: the variable\'s lifetime was shortened. When debugging, temporarily use the variable after the suspension point (for example, log it), or enable the `-Xdebug` compiler option to turn this optimization off ([[src:kt-debugidea]]). The Kotlin docs warn: NEVER use `-Xdebug` for production builds, because it can cause memory leaks (the very reason behind the bug above: variables kept alive longer).')
    B(C, S, 3, 'bug',
      'Stack trace của một exception xảy ra sau `delay`/lời gọi mạng chỉ có vài khung kiểu `invokeSuspend`, `resumeWith`, `DispatchedTask.run`; không thấy hàm nghiệp vụ nào đã gọi tới đó.',
      'The stack trace of an exception thrown after a `delay`/network call shows only a few frames such as `invokeSuspend`, `resumeWith`, `DispatchedTask.run`; none of the business functions that led there appear.')
    B(C, S, 3, 'cause', 'Lúc suspend, call stack thật đã bị dọn. Khi resume, phần còn lại chạy trên một call stack mới, bắt đầu từ dispatcher. "Call stack" của coroutine nằm trong chuỗi continuation, không nằm trên stack của luồng.', 'When it suspended, the real call stack was cleared. On resume, the rest runs on a fresh call stack that starts at the dispatcher. The coroutine\'s "call stack" lives in the continuation chain, not on the thread\'s stack.')
    B(C, S, 3, 'fix', 'Bật chế độ debug của kotlinx.coroutines: truyền `-Dkotlinx.coroutines.debug` cho JVM, hoặc chạy với assertion bật (`-ea`; unit test mặc định đã bật). Chế độ debug thêm tên coroutine và mặc định bật khôi phục stack trace (stack trace recovery: tạo bản sao exception có thêm các khung của coroutine nhận lỗi). Dùng Coroutine Debugger của IntelliJ/Android Studio, hoặc `kotlinx-coroutines-debug`, để xem chuỗi continuation ([[src:kx-debug]]).', 'Enable kotlinx.coroutines debug mode: pass `-Dkotlinx.coroutines.debug` to the JVM, or run with assertions enabled (`-ea`; unit tests have them on by default). Debug mode adds coroutine names and turns on stack-trace recovery by default (it creates a copy of the exception with extra frames from the coroutine that received it). Use the IntelliJ/Android Studio Coroutine Debugger, or `kotlinx-coroutines-debug`, to inspect the continuation chain ([[src:kx-debug]]).')

    S = 'exercises'
    a(C + '.sec.%s.title' % S, 'Bài tập', 'Exercises')
    a(C + '.sec.%s.badge' % S, 'stable')
    B(C, S, 1, 'ex', 'Hàm dưới đây được chia thành mấy trạng thái (giá trị label)? Biến nào phải cất vào continuation?', 'How many states (label values) is the function below split into? Which variables must be stored in the continuation?')
    B(C, S, 1, 'exkt', 'suspend fun sync(id: Int) {\n    val local = db.read(id)          // không suspend\n    val remote = api.fetch(id)       // suspend\n    val merged = merge(local, remote)\n    api.push(merged)                 // suspend\n    db.write(merged)                 // suspend\n    log("done $id")\n}')
    B(C, S, 1, 'hint', 'Đếm lời gọi suspend, cộng 1. Với mỗi biến, hỏi: nó có được dùng ở trạng thái SAU một điểm suspend không?', 'Count the suspending calls and add 1. For each variable, ask: is it used in a state AFTER some suspension point?')
    B(C, S, 1, 'sol', 'Ba lời gọi suspend → 4 trạng thái (label 0..3). Cần cất: `id` (dùng tới cuối, trong `log`), `local` (dùng sau `fetch`), `merged` (dùng sau `push`, trong `db.write`). `remote` được dùng ngay trong cùng trạng thái nó được tạo (trước `push`) nên không cần sống qua điểm suspend nào sau đó.', 'Three suspending calls → 4 states (label 0..3). To store: `id` (used up to the end, in `log`), `local` (used after `fetch`), `merged` (used after `push`, in `db.write`). `remote` is used within the same state it is created in (before `push`), so it does not need to survive any later suspension point.')
    B(C, S, 2, 'ex', 'Bài khuyết bước: viết (giản lược) state machine cho hàm sau, theo mẫu `myFunction` có `counter`.', 'A partly-solved exercise: write the (simplified) state machine for the function below, following the `myFunction`-with-`counter` pattern.')
    B(C, S, 2, 'exkt', 'suspend fun twice(x: Int): Int {\n    delay(10)\n    val y = x * 2\n    delay(10)\n    return y\n}')
    B(C, S, 2, 'hint', 'Ba trạng thái. `x` cần ở trạng thái 1, `y` cần ở trạng thái 2. Kết quả trả về là `y`, không phải `Unit`.', 'Three states. `x` is needed in state 1, `y` in state 2. The return value is `y`, not `Unit`.')
    B(C, S, 2, 'sol', 'Mỗi `delay` là một điểm suspend; trước mỗi điểm, cất biến còn cần và đặt label kế tiếp.', 'Each `delay` is a suspension point; before each one, store the variables still needed and set the next label.')
    B(C, S, 2, 'solkt', 'fun twice(x: Int, continuation: Continuation<Int>): Any {\n    val c = continuation as? TwiceContinuation ?: TwiceContinuation(continuation, x)\n    if (c.label == 0) {\n        c.label = 1\n        if (delay(10, c) == COROUTINE_SUSPENDED) return COROUTINE_SUSPENDED\n    }\n    if (c.label == 1) {\n        c.y = c.x * 2\n        c.label = 2\n        if (delay(10, c) == COROUTINE_SUSPENDED) return COROUTINE_SUSPENDED\n    }\n    if (c.label == 2) return c.y\n    error("Impossible")\n}')
    B(C, S, 3, 'ex', 'Vì sao resume một chuỗi 10 000 hàm suspend lồng nhau không gây StackOverflowError ở bước "đi lên" (mỗi hàm xong thì resume hàm gọi nó)?', 'Why does resuming a chain of 10,000 nested suspending functions not cause a StackOverflowError on the way "up" (each function, when done, resumes its caller)?')
    B(C, S, 3, 'sol', '`BaseContinuationImpl.resumeWith` không gọi đệ quy `completion.resumeWith` cho các continuation do compiler sinh ra. Nó dùng vòng lặp: xong một tầng thì gán `current = completion` và lặp tiếp. Độ sâu call stack giữ nguyên dù chuỗi dài.', '`BaseContinuationImpl.resumeWith` does not recursively call `completion.resumeWith` for compiler-generated continuations. It loops instead: when a level finishes, it sets `current = completion` and loops again. Call-stack depth stays constant however long the chain is.')

    S = 'recall'
    a(C + '.sec.%s.title' % S, 'Tự trả lời', 'Answer it yourself')
    a(C + '.sec.%s.badge' % S, 'stable')
    B(C, S, 1, 'ask', 'Giải thích cho một người chưa học: làm sao một hàm "nhảy vào giữa" khi được resume?', 'Explain to someone who has not studied this: how does a function "jump into the middle" when resumed?')
    B(C, S, 1, 'ans', 'Không nhảy thật. Hàm được gọi lại từ đầu với continuation cũ; trong đó `label` cho biết đã qua tới đâu, nên các khối `if (label == …)` phía trước bị bỏ qua, và biến cũ được nạp lại từ continuation.', 'It does not really jump. The function is called again from the start with the old continuation; its `label` says how far it got, so the earlier `if (label == …)` blocks are skipped, and old variables are reloaded from the continuation.')
    B(C, S, 2, 'ask', 'COROUTINE_SUSPENDED đi đâu sau khi hàm sâu nhất trả nó?', 'Where does COROUTINE_SUSPENDED go after the deepest function returns it?')
    B(C, S, 2, 'ans', 'Mỗi hàm suspend phía trên trả lại đúng giá trị đó, cho tới builder hoặc hàm `resume`. Cả chuỗi thoát ra và luồng được thả.', 'Each suspending function above returns that same value, up to the builder or the `resume` function. The whole chain exits and the thread is released.')
    B(C, S, 3, 'ask', 'Vì sao giữ một object lớn qua điểm suspend có thể gây tốn bộ nhớ?', 'Why can keeping a large object across a suspension point waste memory?')
    B(C, S, 3, 'ans', 'Vì nó được cất trong continuation trên heap suốt thời gian coroutine suspend. Nhiều coroutine cùng chờ thì giữ nhiều object.', 'Because it is stored in the continuation on the heap for as long as the coroutine is suspended. Many coroutines waiting at once hold many objects.')
    for q, qv, qe, av, ae, wv, we in [
        ('q1', 'Hàm suspend có 2 lời gọi suspend có mấy trạng thái?', 'How many states does a suspending function with 2 suspending calls have?',
         'Ba (label 0, 1, 2).', 'Three (label 0, 1, 2).', 'Một trạng thái ở đầu và một sau mỗi lời gọi suspend.', 'One state at the start and one after each suspending call.'),
        ('q2', 'Khi resume, continuation gọi hàm nào?', 'On resume, which function does the continuation call?',
         'Gọi lại chính hàm suspend đó, với chính continuation đó.', 'That same suspending function, with that same continuation.',
         'Hàm thấy tham số đã là continuation của mình nên dùng lại, đọc `label` để chạy tiếp đúng chỗ.', 'The function sees the parameter is already its own continuation, reuses it, and reads `label` to continue in the right place.'),
        ('q3', '`suspend`, `Continuation`, `suspendCoroutine` thuộc ngôn ngữ hay thuộc kotlinx.coroutines? Còn `launch`?', 'Do `suspend`, `Continuation` and `suspendCoroutine` belong to the language or to kotlinx.coroutines? What about `launch`?',
         'Ba thứ đầu thuộc ngôn ngữ và stdlib (`kotlin.coroutines`); `launch` thuộc thư viện `kotlinx.coroutines`.', 'The first three belong to the language and stdlib (`kotlin.coroutines`); `launch` belongs to the `kotlinx.coroutines` library.',
         'Phần ngôn ngữ tối thiểu; thư viện xây phong cách structured concurrency trên đó.', 'The language part is minimal; the library builds the structured-concurrency style on top of it.')]:
        a(C + '.quiz.%s.q' % q, qv, qe); a(C + '.quiz.%s.a' % q, av, ae); a(C + '.quiz.%s.why' % q, wv, we)
