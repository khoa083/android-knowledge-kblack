# Coroutines v2 · U2 Sequence builder (Deep Dive, "Sequence builder", tr. PDF 27–32) + chuỗi của sim coroutines.seq.
# Được dev/gen/coroutines_content.py nạp. Khung: docs/chapter-template-v2.md.

def add(a):
    def B(ch, sec, n, field, vi, en=None):
        a('%s.sec.%s.b.%02d.%s' % (ch, sec, n, field), vi, vi if en is None else en)
    m = lambda k, vi, en=None: a('m.seq.' + k, vi, en)

    # ---------------- sim coroutines.seq ----------------
    m('title', 'Sequence: luồng thực thi nhảy giữa main và khối sequence', 'Sequence: execution jumps between main and the sequence block')
    m('overview', 'Một luồng duy nhất. Mỗi lần `main` gọi `iterator.next()`, luồng chạy vào khối `sequence { }` tới `yield` kế tiếp rồi quay lại `main` cùng giá trị. Bấm Step và để ý hàng "luồng": ai đang giữ luồng ở từng bước.',
      'A single thread. Each time `main` calls `iterator.next()`, the thread runs into the `sequence { }` block up to the next `yield`, then returns to `main` with the value. Press Step and watch the "thread" row: who holds the thread at each step.')
    m('wrapup', 'Khối sequence không chạy hết một lần: nó chạy từng đoạn, mỗi đoạn kết thúc ở một `yield`, và chỉ chạy tiếp khi có người hỏi phần tử kế. Việc "dừng giữa hàm rồi chạy tiếp đúng chỗ đó" chính là suspension. Bật "Dùng List" để so: `buildList` chạy hết khối ngay, mọi dòng "Generating" in ra trước "Starting".',
      'The sequence block does not run all at once: it runs in pieces, each piece ending at a `yield`, and continues only when someone asks for the next element. "Stopping in the middle of a function and later continuing from that exact point" is suspension. Turn on "Use a List" to compare: `buildList` runs the whole block immediately, and every "Generating" line prints before "Starting".')
    m('simp.1', 'Trục ngang là thứ tự bước, không phải thời gian thật.', 'The horizontal axis is step order, not real time.')
    m('simp.2', 'Mô hình không vẽ đối tượng continuation và iterator bên trong (học ở chương "Coroutine dưới mui xe"); ở đây chỉ thấy ai đang chạy.', 'The model does not draw the internal continuation and iterator objects (covered in "Coroutines under the hood"); here you only see who is running.')
    m('ctl.hint', 'Bật "gọi tới hết" để xem khối sequence kết thúc; bật "Dùng List" để so với cách tạo sẵn.', 'Turn on "call to the end" to see the sequence block finish; turn on "Use a List" to compare with building everything up front.')
    m('ctl.all', 'Gọi tới hết (next lần 3 + hasNext)', 'Call to the end (3rd next + hasNext)')
    m('ctl.eager', 'Dùng List (buildList) thay vì sequence', 'Use a List (buildList) instead of sequence')
    m('diagramTitle', 'Ai đang chạy: main hay khối sequence', 'Who is running: main or the sequence block')
    m('diagramDesc', 'Hai hàng mã (main, khối sequence) và một hàng luồng theo thứ tự bước', 'Two code rows (main, the sequence block) and one thread row, in step order')
    m('n.main', 'main()', 'main()')
    m('n.gen', 'khối sequence { }', 'sequence { } block')
    m('n.th', 'Luồng (chỉ có 1)', 'Thread (only 1)')
    m('lanes.code', 'Mã', 'Code')
    m('axis', 'thứ tự bước →', 'step order →')
    m('scope', 'cùng một luồng', 'the same thread')
    m('met.val', 'Giá trị main vừa nhận', 'Value main just received')
    m('met.out', 'Số dòng đã in', 'Lines printed')
    m('bar.run', 'đang chạy (giữ luồng)', 'running (holds the thread)')
    m('bar.call', 'đang đợi next() trả về', 'waiting for next() to return')
    m('bar.wait', 'dừng ở yield (không giữ luồng)', 'paused at yield (holds no thread)')
    m('lbl.call', 'đợi next()', 'awaits next()')
    m('lbl.wait', 'dừng ở yield', 'paused at yield')
    for k, vi, en in [('run', 'đang chạy', 'running'), ('call', 'đợi next() trả về', 'awaiting next()'), ('wait', 'dừng ở yield', 'paused at yield'),
                      ('idle', 'chưa chạy dòng nào', 'not started'), ('done', 'đã xong', 'finished'),
                      ('thMain', 'đang chạy main', 'running main'), ('thGen', 'đang chạy khối sequence', 'running the sequence block'), ('thFree', 'rảnh', 'free')]:
        m('st.' + k, vi, en)
    S = [
        ('start', 'Starting: chưa có phần tử nào được tạo', 'Starting: no element has been made yet',
         '`seq.iterator()` chỉ tạo iterator; khối `sequence { }` chưa chạy dòng nào. `main` in "Starting".', '`seq.iterator()` only creates the iterator; the `sequence { }` block has not run a single line. `main` prints "Starting".'),
        ('next1', 'next() lần 1: nhảy vào khối sequence', '1st next(): jump into the sequence block',
         '`main` gọi `iterator.next()`. Luồng rời `main` (main đứng đợi lời gọi trả về) và chạy khối sequence từ dòng đầu: in "Generating first".', '`main` calls `iterator.next()`. The thread leaves `main` (main waits for the call to return) and runs the sequence block from its first line: it prints "Generating first".'),
        ('yield1', 'yield(1): khối sequence dừng, 1 về tay main', 'yield(1): the block pauses, 1 goes to main',
         '`yield(1)` tạm dừng khối sequence ngay sau dòng này và trả 1 cho `next()`. Luồng quay về `main`: `first = 1`. Khối sequence không giữ luồng; nó chỉ nhớ chỗ đang dừng.', '`yield(1)` pauses the sequence block right after this line and returns 1 to `next()`. The thread goes back to `main`: `first = 1`. The block holds no thread; it only remembers where it stopped.'),
        ('print1', 'main in "First: 1"', 'main prints "First: 1"', '`main` tiếp tục bình thường. Khối sequence vẫn đang dừng ở `yield(1)`.', '`main` carries on as usual. The sequence block is still paused at `yield(1)`.'),
        ('next2', 'next() lần 2: chạy tiếp NGAY SAU yield(1)', '2nd next(): continue RIGHT AFTER yield(1)',
         'Lần này khối sequence không chạy lại từ đầu: nó tiếp tục đúng dòng sau `yield(1)` và in "Generating second". Đây là điều hàm thường không làm được.', 'This time the sequence block does not start over: it continues at the line right after `yield(1)` and prints "Generating second". This is something an ordinary function cannot do.'),
        ('yield2', 'yield(2): dừng lần nữa, 2 về tay main', 'yield(2): pause again, 2 goes to main', 'Khối sequence dừng sau `yield(2)`; `second = 2`.', 'The block pauses after `yield(2)`; `second = 2`.'),
        ('print2', 'main in "Second: 2"', 'main prints "Second: 2"', '`main` in giá trị thứ hai.', '`main` prints the second value.'),
        ('next3', 'next() lần 3: chạy tiếp sau yield(2)', '3rd next(): continue after yield(2)', 'Khối sequence chạy tiếp, in "Generating third".', 'The block continues and prints "Generating third".'),
        ('yield3', 'yield(3): 3 về tay main', 'yield(3): 3 goes to main', 'Khối sequence dừng sau `yield(3)`; `third = 3`.', 'The block pauses after `yield(3)`; `third = 3`.'),
        ('print3', 'main in "Third: 3"', 'main prints "Third: 3"', '`main` in giá trị thứ ba.', '`main` prints the third value.'),
        ('end', 'hasNext(): chạy tiếp tới cuối khối', 'hasNext(): run on to the end of the block',
         'Để biết còn phần tử không, `hasNext()` phải cho khối sequence chạy tiếp: nó in "Done" rồi kết thúc mà không `yield` thêm.', 'To know whether another element exists, `hasNext()` has to let the block continue: it prints "Done" and ends without another `yield`.'),
        ('finish', 'Khối sequence kết thúc; hasNext() = false', 'The block finishes; hasNext() = false', '`main` in `false` và kết thúc.', '`main` prints `false` and finishes.'),
        ('pause', 'main xong, khối sequence vẫn dừng ở yield(2)', 'main finishes; the block is still paused at yield(2)',
         '`main` không hỏi thêm, nên "Generating third" và "Done" không bao giờ được in. Phần còn lại của khối không chạy: đó là tính lười (lazy). Trạng thái dừng chỉ là một đối tượng nhỏ, bị thu gom khi không còn ai giữ iterator.', '`main` asks for nothing more, so "Generating third" and "Done" are never printed. The rest of the block never runs: that is laziness. The paused state is just a small object, garbage collected once nobody holds the iterator.'),
        ('eBuild', 'buildList chạy HẾT khối ngay', 'buildList runs the WHOLE block at once',
         'Với `buildList`, mọi dòng trong khối chạy liền một mạch: in đủ bốn dòng "Generating…/Done" trước khi `main` làm gì khác. Không có gì tạm dừng.', 'With `buildList`, every line of the block runs in one go: all four "Generating…/Done" lines print before `main` does anything else. Nothing pauses.'),
        ('eDone', 'List đã đủ [1, 2, 3]', 'The list is complete: [1, 2, 3]', 'Khối đã xong hẳn; danh sách nằm sẵn trong bộ nhớ.', 'The block is completely done; the list sits in memory.'),
        ('eStart', '"Starting" in SAU mọi dòng Generating', '"Starting" prints AFTER every Generating line', 'So với sequence: ở đây "Starting" đứng sau, vì mọi thứ đã được tạo trước.', 'Compare with sequence: here "Starting" comes after, because everything was built up front.'),
        ('eFirst', 'next() chỉ đọc phần tử có sẵn: {v}', 'next() just reads an existing element: {v}', 'Không nhảy vào khối nào; `next()` của List chỉ đọc phần tử kế tiếp.', 'No jump into any block; a List\'s `next()` just reads the next element.'),
        ('eSecond', 'Đọc tiếp: {v}', 'Read on: {v}', 'Vẫn chỉ đọc. Toàn bộ chi phí tạo đã trả từ đầu, kể cả nếu bạn chỉ cần phần tử đầu.', 'Still just reading. The whole cost of building was paid up front, even if you only needed the first element.'),
    ]
    for sid, tv, te, xv, xe in S:
        m('s.%s.title' % sid, tv, te); m('s.%s.explain' % sid, xv, xe)
    for k, vi, en in [
        ('start', 'Đoán trước: khi bấm Step tiếp, dòng nào được in?', 'Predict: when you press Step again, which line gets printed?'),
        ('enter', 'Hàm `next()` không tự tính giá trị: nó cho khối sequence chạy tới `yield` kế tiếp.', '`next()` does not compute the value itself: it lets the sequence block run to the next `yield`.'),
        ('yield', '`yield` là một hàm suspend: nó lưu chỗ đang dừng rồi trả quyền điều khiển cho người gọi `next()`.', '`yield` is a suspending function: it saves the stopping point and hands control back to whoever called `next()`.'),
        ('resume', 'Chạy tiếp từ giữa hàm: cần cơ chế suspension. Không có nó, muốn làm vậy phải dành riêng một luồng cho khối sequence.', 'Continuing from the middle of a function needs a suspension mechanism. Without it, you would need a dedicated thread for the sequence block.'),
        ('end', '`hasNext()` cũng phải cho khối chạy tiếp, vì chỉ khối đó biết còn `yield` nữa hay không.', '`hasNext()` also has to let the block continue, because only the block knows whether another `yield` is coming.'),
        ('pause', 'Phần khối không được hỏi tới thì không bao giờ chạy. Đó là lý do sequence có thể vô hạn.', 'The part of the block nobody asks for never runs. That is why a sequence can be infinite.'),
        ('eager', 'Cách tạo sẵn (eager): tạo hết, kể cả khi chỉ dùng phần tử đầu. Không thể dùng cho dãy vô hạn.', 'Eager building: everything is built, even if only the first element is used. It cannot work for an infinite sequence.')]:
        m('co.' + k, vi, en)
    for k, vi, en in [('eBuild', 'buildList: in 4 dòng, add 1, 2, 3', 'buildList: prints 4 lines, adds 1, 2, 3'), ('eDone', 'list = [1, 2, 3]', 'list = [1, 2, 3]'),
                      ('start', 'in "Starting"', 'prints "Starting"'), ('eRead', 'next() đọc {v}', 'next() reads {v}'),
                      ('enter', 'vào khối từ dòng đầu, in "Generating first"', 'enter the block at line 1, print "Generating first"'),
                      ('resume', 'chạy tiếp sau yield, in "Generating {w}"', 'continue after yield, print "Generating {w}"'),
                      ('yield', 'yield({v}): dừng, trả {v}', 'yield({v}): pause, return {v}'), ('got', 'next() trả về {v}', 'next() returns {v}'),
                      ('print', 'in giá trị {v}', 'print value {v}'), ('end', 'chạy tiếp, in "Done"', 'continue, print "Done"'),
                      ('finish', 'khối kết thúc', 'block finished'), ('mainDone', 'main kết thúc', 'main finished')]:
        m('ev.' + k, vi, en)
    a('cap.seq', 'Ba hàng theo thứ tự bước: hàm main, khối sequence, và luồng duy nhất. Thanh liền = đang chạy (giữ luồng); thanh viền đứt = dừng ở yield (không giữ luồng). Để ý hàng luồng đổi chủ ở mỗi next() và yield.',
      'Three rows in step order: the main function, the sequence block, and the only thread. Solid bar = running (holds the thread); dashed bar = paused at yield (holds no thread). Watch the thread row change owner at every next() and yield.')

    # ---------------- chương U2 ----------------
    C = 'u2'
    a(C + '.title', 'Sequence builder: lần đầu thấy suspension', 'The sequence builder: a first look at suspension')
    a(C + '.essence',
      'Trước khi học coroutine "thật", hãy xem suspension ở dạng đơn giản nhất: `sequence { … yield(x) … }`. Một hàm có thể dừng giữa chừng, trả một giá trị, rồi lát sau chạy tiếp đúng chỗ đó.\n'
      'Mọi thứ diễn ra trên một luồng duy nhất. Luồng thực thi nhảy qua lại giữa nơi dùng sequence và khối tạo ra nó. Khối tạo chỉ chạy khi có người hỏi phần tử kế tiếp.\n'
      'Hiểu được bước nhảy này là đã hiểu nửa đầu của coroutine: suspend nghĩa là lưu lại chỗ đang dừng, không phải giữ luồng để chờ.',
      'Before studying "real" coroutines, look at suspension in its simplest form: `sequence { … yield(x) … }`. A function can stop midway, hand back a value, and later continue from that exact point.\n'
      'Everything happens on a single thread. Execution jumps back and forth between the place that uses the sequence and the block that produces it. The producing block runs only when someone asks for the next element.\n'
      'Understanding this jump is understanding the first half of coroutines: suspending means saving where you stopped, not holding a thread while you wait.')
    a(C + '.goal.g1', 'Đã bấm tới bước 5 và đối chiếu output với câu đoán', 'Stepped to step 5 and compared the output with your prediction')
    a(C + '.goal.g2', 'Đã đi hết một lượt (nên bật thêm "Dùng List" để so)', 'Went through one full run (also try "Use a List" to compare)')

    S = 'recap'
    a(C + '.sec.%s.title' % S, 'Ôn nhanh chương trước', 'Quick review of the previous chapter')
    B(C, S, 1, 'ask', 'Trong lúc một coroutine đang `delay`, luồng của nó làm gì? Còn `Thread.sleep` thì sao?', 'While a coroutine is in `delay`, what does its thread do? What about `Thread.sleep`?')
    B(C, S, 1, 'ans', '`delay`: coroutine tạm dừng và thả luồng, luồng làm việc khác. `Thread.sleep`: luồng bị chặn, không ai dùng được.', '`delay`: the coroutine suspends and releases the thread, which does other work. `Thread.sleep`: the thread is blocked and nobody can use it.')

    S = 'what'
    a(C + '.sec.%s.title' % S, 'Sequence là gì: một collection tính lười', 'What a sequence is: a lazily evaluated collection')
    a(C + '.sec.%s.badge' % S, 'stable')
    B(C, S, 1, 'p',
      'Nhiều ngôn ngữ có dạng coroutine bị giới hạn: hàm async (async/await) và generator (hàm "nhả" từng giá trị một, như `yield` trong Python hay JavaScript). Kotlin không có từ khoá generator. Thay vào đó, thư viện chuẩn có hàm `sequence { }` để tạo một `Sequence`.\n'
      '`Sequence` giống `List` hay `Set` ở chỗ là một dãy phần tử, nhưng được tính lười: phần tử kế tiếp chỉ được tính khi cần ([[src:kt-seq]]). Vì vậy sequence làm ít thao tác nhất có thể, có thể vô hạn, và tiết kiệm bộ nhớ vì không phải giữ cả danh sách.',
      'Many languages have limited forms of coroutines: async functions (async/await) and generators (functions that "yield" values one at a time, like `yield` in Python or JavaScript). Kotlin has no generator keyword. Instead, the standard library has the `sequence { }` function to create a `Sequence`.\n'
      'A `Sequence` is like a `List` or a `Set` in that it is a series of elements, but it is evaluated lazily: the next element is computed only when needed ([[src:kt-seq]]). That is why a sequence does the fewest operations possible, can be infinite, and saves memory because it does not have to hold a whole list.')
    B(C, S, 2, 'kt', 'val seq = sequence {\n    yield(1)\n    yield(2)\n    yield(3)\n}\n\nfun main() {\n    for (num in seq) {\n        print(num)\n    } // 123\n}')
    B(C, S, 3, 'note',
      '`sequence { }` là một DSL nhỏ. Tham số của nó là lambda có receiver kiểu `suspend SequenceScope<T>.() -> Unit`. Bên trong, `this` là một `SequenceScope<T>`, nên `yield(1)` chính là `this.yield(1)`. Chữ `suspend` trong kiểu lambda là chìa khoá: khối này được phép tạm dừng.',
      '`sequence { }` is a small DSL. Its parameter is a lambda with a receiver of type `suspend SequenceScope<T>.() -> Unit`. Inside, `this` is a `SequenceScope<T>`, so `yield(1)` is really `this.yield(1)`. The word `suspend` in the lambda type is the key: this block is allowed to pause.')

    S = 'jump'
    a(C + '.sec.%s.title' % S, 'Theo dõi từng bước nhảy', 'Following every jump')
    a(C + '.sec.%s.badge' % S, 'stable')
    B(C, S, 1, 'p', 'Thêm lệnh in vào cả hai phía để thấy phần tử được tạo theo yêu cầu, không phải tạo trước:', 'Add print statements on both sides to see that elements are produced on demand, not in advance:')
    B(C, S, 2, 'kt', 'val seq = sequence {\n    println("Generating first")\n    yield(1)\n    println("Generating second")\n    yield(2)\n    println("Generating third")\n    yield(3)\n    println("Done")\n}\n\nfun main() {\n    for (num in seq) {\n        println("The next number is $num")\n    }\n}')
    B(C, S, 3, 'predict', 'Trước khi mở: bảy dòng sẽ được in theo thứ tự nào? "Generating…" in hết trước, hay xen kẽ với "The next number is…"?', 'Before opening: in what order are the seven lines printed? Do all the "Generating…" lines come first, or do they alternate with "The next number is…"?')
    B(C, S, 3, 'ans', 'Xen kẽ: Generating first → The next number is 1 → Generating second → The next number is 2 → Generating third → The next number is 3 → Done. Mỗi vòng `for` hỏi một phần tử, khối sequence chạy tới `yield` kế tiếp rồi dừng.', 'They alternate: Generating first → The next number is 1 → Generating second → The next number is 2 → Generating third → The next number is 3 → Done. Each `for` iteration asks for one element; the sequence block runs to the next `yield` and stops.')
    B(C, S, 4, 'p',
      'Phân tích: vòng `for` hỏi phần tử đầu, ta đi vào khối, in "Generating first" rồi `yield(1)`. Giá trị 1 quay về vòng lặp, in "The next number is 1". Rồi xảy ra điều quan trọng: khi hỏi phần tử kế, thực thi nhảy về đúng chỗ đã dừng trong khối (ngay sau `yield(1)`) chứ không chạy lại từ đầu.\n'
      'Một hàm bình thường không làm được vậy. Hàm thường chỉ có hai trạng thái: đang chạy, hoặc đã trả về và quên sạch biến cục bộ. Muốn dừng giữa hàm rồi chạy tiếp từ đúng điểm đó, cần một cơ chế suspension: lưu chỗ đang dừng và các biến cần nhớ ở đâu đó ngoài call stack.',
      'Analysis: the `for` loop asks for the first element, we enter the block, print "Generating first", then `yield(1)`. The value 1 goes back to the loop, which prints "The next number is 1". Then the crucial thing happens: when the next element is requested, execution jumps back to exactly where the block stopped (right after `yield(1)`) instead of starting over.\n'
      'An ordinary function cannot do that. An ordinary function has only two states: running, or returned with all its local variables forgotten. To stop in the middle of a function and later continue from that exact point, you need a suspension mechanism: something that stores the stopping point and the variables to remember somewhere outside the call stack.')
    B(C, S, 5, 'p', 'Để thấy rõ hơn, gọi iterator bằng tay (đây cũng là đoạn mã của mô phỏng ngay bên dưới):', 'To see it even more clearly, drive the iterator by hand (this is also the code of the simulation just below):')
    B(C, S, 6, 'kt', 'fun main() {\n    val iterator = seq.iterator()\n    println("Starting")\n    val first = iterator.next()\n    println("First: $first")\n    val second = iterator.next()\n    println("Second: $second")\n}')
    B(C, S, 7, 'predict', 'Output là gì? Đặc biệt: "Generating third" có được in không?', 'What is the output? In particular: does "Generating third" get printed?')
    B(C, S, 7, 'ans', 'Starting → Generating first → First: 1 → Generating second → Second: 2. "Generating third" và "Done" KHÔNG được in, vì không ai hỏi phần tử thứ ba. Bấm Step trong mô phỏng để kiểm từng bước.', 'Starting → Generating first → First: 1 → Generating second → Second: 2. "Generating third" and "Done" are NOT printed, because nobody asks for a third element. Press Step in the simulation to check each step.')

    S = 'why'
    a(C + '.sec.%s.title' % S, 'Vì sao cần suspension (và vì sao không dùng luồng)', 'Why suspension is needed (and why not a thread)')
    a(C + '.sec.%s.badge' % S, 'stable impl')
    B(C, S, 1, 'p',
      'Không có coroutine thì làm được không? Có thể: dành riêng một luồng cho khối sequence, luồng đó chạy tới `yield` thì ngủ chờ, `next()` đánh thức nó rồi đợi giá trị. Nhưng mỗi iterator sẽ tốn một luồng, phải đồng bộ hoá giữa hai luồng, và luồng bị bỏ dở sẽ treo mãi. Với suspension thì rẻ và đơn giản: iterator đang dừng chỉ là một đối tượng nhỏ, giữ bao lâu cũng gần như không tốn gì.',
      'Could you do it without coroutines? Possibly: dedicate a thread to the sequence block, have that thread sleep when it reaches `yield`, and have `next()` wake it up and wait for the value. But every iterator would cost a thread, the two threads would need synchronization, and an abandoned thread would hang forever. With suspension it is cheap and simple: a paused iterator is just a small object, and keeping it around costs almost nothing.')
    B(C, S, 2, 'note',
      'Bên trong (kotlin-stdlib, `SequenceBuilder.kt`, đã đối chiếu nhánh master ngày 2026-11-22): lớp `SequenceBuilderIterator` vừa là `Iterator`, vừa là `SequenceScope`, vừa là một `Continuation<Unit>`, đóng vai completion của khối. Khối được tạo thành coroutine bằng `createCoroutineUnintercepted(receiver = iterator, completion = iterator)` và cất ở trường `nextStep`. `yield(value)` cất giá trị, cất continuation hiện tại vào `nextStep`, rồi suspend. `hasNext()`/`next()` gọi `resume` trên `nextStep` để khối chạy tới `yield` kế tiếp. Không có luồng thứ hai nào. Đây là chi tiết implementation, có thể đổi giữa các phiên bản; cơ chế chung sẽ học kỹ ở chương "Coroutine dưới mui xe".',
      'Inside (kotlin-stdlib, `SequenceBuilder.kt`, checked against the master branch on 2026-11-22): the class `SequenceBuilderIterator` is at once an `Iterator`, a `SequenceScope`, and a `Continuation<Unit>` acting as the block\'s completion. The block is turned into a coroutine with `createCoroutineUnintercepted(receiver = iterator, completion = iterator)` and kept in the `nextStep` field. `yield(value)` stores the value, stores the current continuation in `nextStep`, then suspends. `hasNext()`/`next()` call `resume` on `nextStep` so the block runs to the next `yield`. There is no second thread. This is an implementation detail and may change between versions; the general mechanism is covered in depth in "Coroutines under the hood".')

    S = 'real'
    a(C + '.sec.%s.title' % S, 'Dùng thật: dãy vô hạn, dữ liệu sinh dần', 'Real uses: infinite sequences, generated data')
    a(C + '.sec.%s.badge' % S, 'stable')
    B(C, S, 1, 'p', 'Cách dùng điển hình nhất là sinh một dãy toán học, ví dụ Fibonacci. Vòng `while (true)` không treo máy, vì khối chỉ chạy tới `yield` kế tiếp mỗi khi được hỏi:', 'The most typical use is generating a mathematical sequence, such as Fibonacci. The `while (true)` loop does not hang, because the block only runs to the next `yield` each time it is asked:')
    B(C, S, 2, 'kt', 'val fibonacci: Sequence<BigInteger> = sequence {\n    var first = 0.toBigInteger()\n    var second = 1.toBigInteger()\n    while (true) {\n        yield(first)\n        val temp = first\n        first += second\n        second = temp\n    }\n}\n\nfun main() {\n    print(fibonacci.take(10).toList())\n}')
    B(C, S, 3, 'out', '[0, 1, 1, 2, 3, 5, 8, 13, 21, 34]')
    B(C, S, 4, 'ask', 'Biến `first` và `second` là biến cục bộ của khối. Sau mỗi `yield`, khối "thoát ra" về người gọi. Vậy giá trị của chúng được giữ ở đâu giữa hai lần `next()`?', 'The variables `first` and `second` are local variables of the block. After each `yield`, the block "leaves" to the caller. So where are their values kept between two `next()` calls?')
    B(C, S, 4, 'ans', 'Không nằm trên call stack (stack frame của khối đã bị bỏ khi quay về người gọi). Chúng được cất trong đối tượng continuation của khối, trên heap, cùng với "nhãn" cho biết đang dừng ở `yield` nào. Đây chính là điều chương "Coroutine dưới mui xe" sẽ mở ra.', 'Not on the call stack (the block\'s stack frame is dropped when it returns to the caller). They are stored in the block\'s continuation object, on the heap, together with a "label" saying which `yield` it stopped at. This is exactly what the chapter "Coroutines under the hood" will open up.')
    B(C, S, 5, 'p', 'Cũng dùng được để sinh số hoặc chuỗi ngẫu nhiên, mỗi lần một phần tử:', 'It also works for generating random numbers or strings, one element at a time:')
    B(C, S, 6, 'kt', 'fun randomNumbers(seed: Long = System.currentTimeMillis()): Sequence<Int> = sequence {\n    val random = Random(seed)\n    while (true) {\n        yield(random.nextInt())\n    }\n}')

    S = 'limits'
    a(C + '.sec.%s.title' % S, 'Giới hạn: trong sequence chỉ được yield', 'The limit: inside a sequence you may only yield')
    a(C + '.sec.%s.badge' % S, 'stable')
    B(C, S, 1, 'p',
      'Trong khối `sequence { }` không được gọi hàm suspend nào khác ngoài `yield`/`yieldAll`. Đây là luật của compiler, không chỉ là lời khuyên. `SequenceScope` được đánh dấu `@RestrictsSuspension`, nên trong khối chỉ gọi được các hàm suspend có receiver là `SequenceScope` ([[src:kt-restricts]]). Lý do: người tiêu thụ sequence gọi `next()` theo kiểu đồng bộ và chờ ngay lập tức. Nếu khối được phép `delay` hay chờ mạng, `next()` không biết phải làm gì trong lúc đó.\n'
      'Khi cần sinh phần tử mà phải chờ (tải từng trang từ API), dùng `Flow`. Builder của `flow { }` trông gần như y hệt, nhưng hỗ trợ mọi hàm suspend và các tính năng coroutine khác (học ở Phần 3).',
      'Inside a `sequence { }` block you may not call any suspending function other than `yield`/`yieldAll`. This is a compiler rule, not just advice. `SequenceScope` is annotated with `@RestrictsSuspension`, so inside the block you can only call suspending functions whose receiver is `SequenceScope` ([[src:kt-restricts]]). The reason: the consumer of a sequence calls `next()` synchronously and waits right there. If the block were allowed to `delay` or wait for the network, `next()` would have no idea what to do in the meantime.\n'
      'When producing elements requires waiting (loading pages one by one from an API), use `Flow`. The `flow { }` builder looks almost the same, but supports every suspending function and the other coroutine features (covered in Part 3).')
    B(C, S, 2, 'kt',
      'fun allUsersFlow(api: UserApi): Flow<User> = flow {\n    var page = 0\n    do {\n        val users = api.takePage(page++)   // suspend: được phép trong flow { }\n        emitAll(users)\n    } while (!users.isNullOrEmpty())\n}',
      'fun allUsersFlow(api: UserApi): Flow<User> = flow {\n    var page = 0\n    do {\n        val users = api.takePage(page++)   // suspend: allowed inside flow { }\n        emitAll(users)\n    } while (!users.isNullOrEmpty())\n}')
    B(C, S, 3, 'bug',
      'Bạn viết `sequence { val page = api.load(n); yieldAll(page) }` với `api.load` là hàm suspend. Code không biên dịch: compiler báo lỗi về "restricted suspending function" (nội dung thông báo có thể khác nhau giữa các phiên bản Kotlin).',
      'You write `sequence { val page = api.load(n); yieldAll(page) }` where `api.load` is a suspending function. It does not compile: the compiler reports an error about a "restricted suspending function" (the exact message may differ between Kotlin versions).')
    B(C, S, 3, 'cause', '`SequenceScope` có `@RestrictsSuspension`: khối chỉ được suspend qua `yield`/`yieldAll`, vì người dùng `Sequence` không có cách nào chờ một lời gọi mạng.', '`SequenceScope` has `@RestrictsSuspension`: the block may only suspend through `yield`/`yieldAll`, because a `Sequence` consumer has no way to wait for a network call.')
    B(C, S, 3, 'fix', 'Đổi sang `flow { … emit(…) }` và thu thập bằng `collect` trong một coroutine.', 'Switch to `flow { … emit(…) }` and collect it with `collect` inside a coroutine.')
    B(C, S, 4, 'bug',
      'Bạn tạo `val ids = sequence { … println("query DB") … yield(row) }` rồi gọi `ids.count()` và sau đó `ids.first()`. Log cho thấy cơ sở dữ liệu bị truy vấn nhiều lần.',
      'You create `val ids = sequence { … println("query DB") … yield(row) }` and then call `ids.count()` followed by `ids.first()`. The log shows the database being queried several times.')
    B(C, S, 4, 'cause', 'Mỗi thao tác cuối (`count`, `first`, `toList`, vòng `for`) lấy một iterator mới, và mỗi iterator chạy lại khối từ đầu. Sequence không tự nhớ kết quả.', 'Every terminal operation (`count`, `first`, `toList`, a `for` loop) gets a new iterator, and every iterator runs the block again from the start. A sequence does not cache its results.')
    B(C, S, 4, 'fix', 'Nếu cần dùng kết quả nhiều lần, gọi `toList()` một lần rồi dùng danh sách đó. Đừng để việc nặng hoặc có hiệu ứng phụ trong sequence bị duyệt nhiều lần.', 'If you need the results more than once, call `toList()` once and use that list. Do not put heavy or side-effecting work in a sequence that gets traversed several times.')

    S = 'exercises'
    a(C + '.sec.%s.title' % S, 'Bài tập', 'Exercises')
    a(C + '.sec.%s.badge' % S, 'stable')
    B(C, S, 1, 'ex', 'Đoán output (chú ý `take(2)`):', 'Predict the output (watch the `take(2)`):')
    B(C, S, 1, 'exkt', 'val s = sequence {\n    for (i in 1..5) {\n        println("make $i")\n        yield(i * 10)\n    }\n}\n\nfun main() {\n    println(s.take(2).toList())\n}')
    B(C, S, 1, 'hint', '`take(2)` chỉ hỏi đúng 2 phần tử. Có cần hỏi thêm để biết "hết chưa" không?', '`take(2)` asks for exactly 2 elements. Does it need to ask for more to know whether it is done?')
    B(C, S, 1, 'sol', 'make 1 → make 2 → [10, 20]. Khi đã có đủ 2 phần tử, `take` dừng hỏi, nên "make 3" không bao giờ được in. Vòng `for` của khối dừng ở `yield(20)` mãi mãi, và điều đó vô hại.', 'make 1 → make 2 → [10, 20]. Once it has 2 elements, `take` stops asking, so "make 3" is never printed. The block\'s `for` loop stays paused at `yield(20)` forever, and that is harmless.')
    B(C, S, 2, 'ex', 'Viết `fun powersOfTwo(): Sequence<Long>` sinh 1, 2, 4, 8, … vô hạn bằng `sequence { }`. Rồi in 5 phần tử đầu.', 'Write `fun powersOfTwo(): Sequence<Long>` that yields 1, 2, 4, 8, … forever using `sequence { }`. Then print the first 5 elements.')
    B(C, S, 2, 'sol', 'Biến `x` sống qua các lần `yield` nhờ được cất trong continuation.', 'The variable `x` survives across `yield` calls because it is stored in the continuation.')
    B(C, S, 2, 'solkt', 'fun powersOfTwo(): Sequence<Long> = sequence {\n    var x = 1L\n    while (true) {\n        yield(x)\n        x *= 2\n    }\n}\n\nfun main() = println(powersOfTwo().take(5).toList()) // [1, 2, 4, 8, 16]')
    B(C, S, 3, 'ex', 'Một bạn viết `val firstBig = (1..1_000_000).map { heavy(it) }.first { it > 100 }` và thấy chậm. Sửa thế nào? Vì sao nhanh hơn?', 'Someone writes `val firstBig = (1..1_000_000).map { heavy(it) }.first { it > 100 }` and finds it slow. How do you fix it? Why is it faster?')
    B(C, S, 3, 'sol', 'Thêm `.asSequence()` trước `map`. Với collection, `map` tính `heavy` cho cả triệu phần tử rồi mới tìm. Với sequence, từng phần tử đi qua `map` rồi `first`, và dừng ngay khi gặp phần tử thoả điều kiện. Chỉ tính đúng số phần tử cần.', 'Add `.asSequence()` before `map`. With a collection, `map` computes `heavy` for all million elements before searching. With a sequence, each element goes through `map` and then `first`, stopping as soon as one matches. Only the needed elements are computed.')
    B(C, S, 3, 'solkt', 'val firstBig = (1..1_000_000).asSequence()\n    .map { heavy(it) }\n    .first { it > 100 }')

    S = 'recall'
    a(C + '.sec.%s.title' % S, 'Tự trả lời', 'Answer it yourself')
    a(C + '.sec.%s.badge' % S, 'stable')
    B(C, S, 1, 'ask', 'Giải thích bằng lời của bạn: khi gọi `next()` lần thứ hai, khối sequence bắt đầu chạy từ dòng nào, và vì sao một hàm thường không làm được vậy?', 'Explain in your own words: on the second `next()` call, at which line does the sequence block start running, and why can an ordinary function not do that?')
    B(C, S, 1, 'ans', 'Từ dòng ngay sau `yield` lần trước. Hàm thường khi trả về thì mất stack frame và mọi biến cục bộ; muốn chạy tiếp từ giữa phải có chỗ cất "đang ở đâu" và "biến nào" ngoài stack. Đó là continuation.', 'From the line right after the previous `yield`. An ordinary function loses its stack frame and every local variable when it returns; to continue from the middle you need somewhere outside the stack to keep "where we are" and "which variables". That is a continuation.')
    B(C, S, 2, 'ask', 'Vì sao không được gọi `delay` trong `sequence { }`? Nên dùng gì thay thế?', 'Why can you not call `delay` inside `sequence { }`? What should you use instead?')
    B(C, S, 2, 'ans', '`SequenceScope` có `@RestrictsSuspension`, và người dùng sequence gọi `next()` đồng bộ nên không chờ được. Khi cần chờ, dùng `flow { }`.', '`SequenceScope` has `@RestrictsSuspension`, and a sequence consumer calls `next()` synchronously, so it cannot wait. When you need to wait, use `flow { }`.')
    for q, qv, qe, av, ae, wv, we in [
        ('q1', 'Khi nào dòng đầu tiên trong `sequence { }` được chạy?', 'When does the first line inside `sequence { }` run?',
         'Khi có người hỏi phần tử đầu tiên (`next()`/`hasNext()`), không phải lúc tạo sequence hay iterator.', 'When someone asks for the first element (`next()`/`hasNext()`), not when the sequence or the iterator is created.',
         'Sequence là lười: khối chỉ chạy tới `yield` kế tiếp khi được hỏi.', 'Sequences are lazy: the block runs to the next `yield` only when asked.'),
        ('q2', 'Sequence và khối tạo ra nó chạy trên mấy luồng?', 'How many threads do a sequence and its producing block run on?',
         'Một: luồng gọi `next()`.', 'One: the thread that calls `next()`.',
         'Thực thi nhảy qua lại trên cùng luồng; suspension không cần luồng thứ hai.', 'Execution jumps back and forth on the same thread; suspension needs no second thread.'),
        ('q3', 'Gọi `toList()` hai lần trên cùng một `sequence { }` thì khối chạy mấy lần?', 'Calling `toList()` twice on the same `sequence { }` runs the block how many times?',
         'Hai lần.', 'Twice.', 'Mỗi lần duyệt lấy một iterator mới và chạy khối từ đầu; sequence không lưu kết quả.', 'Each traversal gets a new iterator and runs the block from the start; a sequence does not cache results.')]:
        a(C + '.quiz.%s.q' % q, qv, qe); a(C + '.quiz.%s.a' % q, av, ae); a(C + '.quiz.%s.why' % q, wv, we)
