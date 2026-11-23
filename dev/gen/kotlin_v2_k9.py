# Kotlin · K9: Sequence và hiệu năng xử lý collection (Phần 2)
# Nguồn: kotlinlang.org Sequences (đọc 2026-11-23, trang ghi 03 November 2026); Effective Kotlin Items 54, 57;
# Functional Kotlin (Sequences). Bài tập dựa trên "Understanding sequences" (Kotlin Exercises). Trần: 8 mục, mục cơ chế ≤ 4 khối.

SEC_ORDER = {'k9': ['hook', 'eager', 'lazy', 'choose', 'bugs', 'ex', 'recall', 'honest']}


def add(a):
    def B(ch, sec, n, field, vi, en=None):
        a('%s.sec.%s.b.%02d.%s' % (ch, sec, n, field), vi, vi if en is None else en)

    a('st.pending', 'đang chờ thao tác cuối', 'waiting for a terminal operation')
    a('st.unused', 'chưa chạy', 'never ran')
    a('fam.waiting', 'đang chờ (lười)', 'waiting (lazy)')
    a('fam.unused', 'không chạy', 'did not run')
    m = lambda k, vi, en=None: a('m.sequence.' + k, vi, en)
    m('title', 'Từng bước cho cả list, hay từng phần tử qua cả chuỗi', 'Step by step for the whole list, or element by element through the chain')
    m('overview', 'Phòng khám có 8 lịch hẹn trong ngày, giờ lần lượt 8, 13, 9, 10, 15, 11, 16, 9. Cần tên 2 bệnh nhân buổi sáng đầu tiên: filter (giờ < 12), map (lấy tên), take(2). So cách List và Sequence chạy chuỗi này, và xem chuyện gì xảy ra khi Sequence không có thao tác cuối.',
      'The clinic has 8 appointments today, at hours 8, 13, 9, 10, 15, 11, 16, 9. We need the names of the first 2 morning patients: filter (hour < 12), map (take the name), take(2). Compare how a List and a Sequence run this chain, and see what happens when a Sequence has no terminal operation.')
    m('wrapup', 'List chạy từng bước cho cả collection và tạo một list trung gian sau mỗi bước: 13 lần chạy lambda, 2 list trung gian. Sequence đưa từng phần tử qua cả chuỗi và dừng khi take đủ: 5 lần chạy lambda, chỉ đọc 3 phần tử. Nhưng Sequence lười: không có thao tác cuối thì không gì chạy cả. Với collection nhỏ, List đơn giản hơn và đủ nhanh.',
      'A List runs step by step for the whole collection and builds an intermediate list after each step: 13 lambda runs, 2 intermediate lists. A Sequence sends each element through the whole chain and stops once take is satisfied: 5 lambda runs, only 3 elements read. But a Sequence is lazy: with no terminal operation, nothing runs at all. For small collections, a List is simpler and fast enough.')
    m('simp.1', 'Sơ đồ chỉ đếm số lần chạy lambda filter/map và số list trung gian trên 8 phần tử mẫu; không đo thời gian hay bộ nhớ thật.', 'The diagram only counts filter/map lambda runs and intermediate lists over the 8 sample elements; it measures no real time or memory.')
    m('simp.2', 'Thứ tự chạy theo trang Sequences của tài liệu Kotlin; số đếm được model tính lại từ dữ liệu mẫu (selfCheck). Site không chạy Kotlin trong trang.', 'The execution order follows the Kotlin docs\' Sequences page; the counts are recomputed by the model from the sample data (selfCheck). The site does not run Kotlin in the page.')
    m('ctl.hint', 'So "lần chạy lambda" ở bước cuối của List (13) với Sequence (5).', 'Compare "lambda runs" at the last step for the List (13) and the Sequence (5).')
    m('ctl.case', 'Cách chạy', 'How it runs')
    for k, vi, en in [('list', 'List: háo hức, từng bước', 'List: eager, step by step'), ('sequence', 'Sequence: lười, từng phần tử', 'Sequence: lazy, element by element'), ('noTerminal', 'Sequence quên thao tác cuối', 'Sequence missing a terminal operation')]:
        m('ctl.case.' + k, vi, en)
    m('diagramTitle', 'Danh sách gốc, filter, map, take', 'Source list, filter, map, take')
    m('diagramDesc', 'Tám lịch hẹn đi qua filter (buổi sáng), map (tên bệnh nhân) và take(2) hoặc một thao tác cuối', 'Eight appointments go through filter (morning), map (patient name) and take(2) or a terminal operation')
    for k, vi, en in [('source', 'Danh sách gốc (8 lịch hẹn)', 'Source list (8 appointments)'), ('filter', 'filter: giờ < 12', 'filter: hour < 12'), ('map', 'map: lấy tên (hay gửi nhắc)', 'map: get name (or send reminder)'), ('terminal', 'take(2) / thao tác cuối', 'take(2) / terminal step')]:
        m('n.' + k, vi, en)
    m('met.ops', 'Lần chạy lambda filter/map', 'filter/map lambda runs'); m('met.inter', 'Collection trung gian', 'Intermediate collections'); m('met.touched', 'Phần tử gốc đã đọc', 'Source elements read')
    a('cap.sequence', 'Từ trái sang phải: tám lịch hẹn gốc, filter giữ buổi sáng, map lấy tên, take(2) hay một thao tác cuối. Với List, mỗi khối chạy xong cho cả danh sách rồi mới tới khối sau; với Sequence, từng phần tử chạy qua cả chuỗi. Khối viền đỏ là chỗ kết quả không như người viết mong.', 'Left to right: the eight source appointments, filter keeping the mornings, map taking names, take(2) or a terminal operation. With a List, each box finishes for the whole list before the next box starts; with a Sequence, each element runs through the whole chain. A red-outlined box is where the result is not what the author expected.')
    S = [
        ('list', 'start', '8 lịch hẹn, chuỗi filter → map → take(2)', '8 appointments, a filter → map → take(2) chain', 'Gọi trực tiếp trên List. Mỗi thao tác của Iterable chạy ngay (háo hức) và trả về một List mới.', 'Called directly on a List. Each Iterable operation runs at once (eagerly) and returns a new List.'),
        ('list', 'first', 'filter chạy cho cả 8 phần tử → List 5', 'filter runs on all 8 elements → a List of 5', 'filter xét hết 8 lịch hẹn (8 lần chạy lambda) và tạo list trung gian thứ nhất gồm 5 lịch buổi sáng.', 'filter looks at all 8 appointments (8 lambda runs) and builds the first intermediate list of 5 morning appointments.'),
        ('list', 'next', 'map chạy cho cả 5 → List 5 tên', 'map runs on all 5 → a List of 5 names', 'map lấy tên cho cả 5 lịch (thêm 5 lần, tổng 13) và tạo list trung gian thứ hai.', 'map takes the name for all 5 appointments (5 more runs, 13 in total) and builds the second intermediate list.'),
        ('list', 'end', 'take(2): giữ 2 tên, bỏ 3', 'take(2): keeps 2 names, discards 3', 'Kết quả đúng, nhưng 3 tên đã được tính rồi bỏ đi, và 2 list trung gian chỉ dùng một lần. Với 8 phần tử thì không sao; với hàng chục nghìn phần tử và nhiều bước thì đáng kể.', 'The result is right, but 3 names were computed and thrown away, and 2 intermediate lists were used only once. With 8 elements it does not matter; with tens of thousands and several steps it does.'),
        ('sequence', 'start', 'asSequence(): dựng chuỗi, chưa chạy gì', 'asSequence(): the chain is built, nothing runs yet', 'filter, map, take trên Sequence là thao tác trung gian: chúng chỉ trả về Sequence mới, chưa chạy lambda nào (0 lần).', 'filter, map and take on a Sequence are intermediate operations: they just return a new Sequence and run no lambda yet (0 runs).'),
        ('sequence', 'first', 'toList() kích hoạt: phần tử 8 giờ đi qua cả chuỗi', 'toList() triggers it: the 8 o\'clock element goes through the whole chain', 'Thao tác cuối toList() kéo phần tử đầu tiên: filter (qua) rồi map ngay, trước khi xét phần tử thứ hai. take đã có 1 tên.', 'The terminal toList() pulls the first element: filter (passes), then map at once, before the second element is looked at. take now has 1 name.'),
        ('sequence', 'next', 'Phần tử 13 giờ bị filter loại, không tới map', 'The 13 o\'clock element is rejected by filter and never reaches map', 'Chỉ 1 lần chạy filter cho phần tử này. map không chạy cho nó.', 'Only 1 filter run for this element. map does not run for it.'),
        ('sequence', 'end', 'Phần tử 9 giờ qua cả chuỗi: take đủ 2, dừng', 'The 9 o\'clock element passes the chain: take has 2, it stops', 'Tổng 5 lần chạy lambda, chỉ đọc 3/8 phần tử, không có list trung gian. 5 phần tử còn lại không bao giờ được xét.', '5 lambda runs in total, only 3 of 8 elements read, no intermediate list. The other 5 elements are never looked at.'),
        ('noTerminal', 'start', 'remindMorning: gửi nhắc lịch bằng Sequence', 'remindMorning: send reminders with a Sequence', 'Ý định: lọc lịch buổi sáng và gửi tin nhắc cho từng người, việc gửi đặt trong map.', 'The intent: filter the morning appointments and send each a reminder, with the sending inside map.'),
        ('noTerminal', 'first', 'filter và map chỉ dựng chuỗi', 'filter and map only build the chain', 'Hai thao tác trung gian trả về Sequence mới. Chưa lambda nào chạy, và hàm cũng không làm gì với Sequence đó.', 'Both intermediate operations return a new Sequence. No lambda has run, and the function does nothing with that Sequence either.'),
        ('noTerminal', 'next', 'Hàm kết thúc: không ai nhận được tin nhắc', 'The function ends: nobody gets a reminder', 'Không có thao tác cuối nên chuỗi không bao giờ chạy: 0 lần gọi sendReminder. Trình biên dịch không báo lỗi.', 'There is no terminal operation, so the chain never runs: sendReminder is called 0 times. The compiler reports no error.'),
        ('noTerminal', 'end', 'Sửa: kết thúc bằng forEach', 'Fix: end with forEach', 'forEach là thao tác cuối: cả chuỗi chạy, 8 lần filter và 5 lần gửi. Việc có tác dụng phụ (gửi tin, ghi log) nên đặt trong forEach, không đặt trong map.', 'forEach is a terminal operation: the whole chain runs, 8 filter runs and 5 sends. Side effects (sending, logging) belong in forEach, not in map.'),
    ]
    for case, k, tv, te, xv, xe in S:
        sid = case + '.' + k
        m('s.%s.title' % sid, tv, te); m('s.%s.explain' % sid, xv, xe); m('ev.' + sid, tv, te)
    for k, vi, en in [
        ('try', 'Đổi cách chạy rồi đi lại; để ý số lần chạy lambda và số collection trung gian.', 'Switch how it runs and walk again; watch the lambda runs and the intermediate collections.'),
        ('list.next', 'Tài liệu Sequences: với Iterable, mỗi bước xử lý chạy xong và trả về kết quả là một collection trung gian; bước sau chạy trên collection đó. [[src:kt-sequences]]', 'Sequences docs: with an Iterable, each processing step completes and returns its result, an intermediate collection; the next step runs on that collection. [[src:kt-sequences]]'),
        ('list.end', 'Effective Kotlin Item 54: ưu tiên Sequence cho collection lớn có nhiều bước xử lý; mỗi bước của Iterable tạo một collection mới. [[src:book-effective-kotlin]]', 'Effective Kotlin Item 54: prefer Sequence for big collections with more than one processing step; each Iterable step creates a new collection. [[src:book-effective-kotlin]]'),
        ('sequence.next', 'Tài liệu Sequences: Sequence thực hiện mọi bước lần lượt cho từng phần tử, còn Iterable làm xong một bước cho cả collection rồi mới sang bước sau. [[src:kt-sequences]]', 'Sequences docs: a Sequence performs all the steps one by one for every single element, while an Iterable completes each step for the whole collection before the next. [[src:kt-sequences]]'),
        ('sequence.end', 'Tài liệu Sequences: khi số phần tử kết quả đạt mức take yêu cầu, xử lý dừng lại. [[src:kt-sequences]]', 'Sequences docs: when the result size reaches what take asks for, processing stops. [[src:kt-sequences]]'),
        ('noTerminal.next', 'Tài liệu Sequences: việc tính toán thật chỉ xảy ra khi kết quả của cả chuỗi được yêu cầu; phần tử chỉ lấy ra được bằng thao tác cuối. [[src:kt-sequences]]', 'Sequences docs: actual computing happens only when the result of the whole chain is requested; elements can be retrieved only with terminal operations. [[src:kt-sequences]]'),
        ('noTerminal.end', 'toList(), first(), sum(), count(), forEach… là thao tác cuối; filter, map, take là thao tác trung gian. [[src:kt-sequences]]', 'toList(), first(), sum(), count(), forEach… are terminal operations; filter, map, take are intermediate. [[src:kt-sequences]]')]:
        m('co.' + k, vi, en)

    C = 'k9'
    a(C + '.title', 'Sequence và hiệu năng xử lý collection', 'Sequences and collection processing performance')
    a(C + '.essence', 'Thao tác trên List (Iterable) chạy háo hức: mỗi bước làm xong cho cả collection và tạo một collection trung gian.\nSequence chạy lười: từng phần tử đi qua cả chuỗi, có thể dừng sớm (take, first), không có collection trung gian, và chỉ chạy khi có thao tác cuối (toList, first, sum, forEach…).\nSequence có chi phí riêng: hợp với collection lớn và nhiều bước, không phải lúc nào cũng nhanh hơn.',
      'Operations on a List (Iterable) are eager: each step finishes for the whole collection and builds an intermediate collection.\nA Sequence is lazy: each element goes through the whole chain, it can stop early (take, first), there are no intermediate collections, and it runs only on a terminal operation (toList, first, sum, forEach…).\nA Sequence has its own overhead: it suits big collections with several steps and is not always faster.')
    a(C + '.goal.g1', 'Đã thấy bước xử lý đầu tiên chạy', 'Saw the first processing step run')
    a(C + '.goal.g2', 'Đã đi tới kết quả cuối', 'Reached the final result')
    a(C + '.sim.kotlin.sequence', 'List và Sequence', 'List and Sequence')

    S_ = 'hook'
    a(C + '.sec.%s.title' % S_, 'Đoán trước khi đọc', 'Predict before reading')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'predict', 'Có 8 lịch hẹn. Ta cần tên 2 bệnh nhân buổi sáng đầu tiên: `filter { it.hour < 12 }.map { it.patient }.take(2)`. Viết trên List và trên `asSequence()`, mỗi cách chạy lambda filter/map bao nhiêu lần?',
      'There are 8 appointments. We need the names of the first 2 morning patients: `filter { it.hour < 12 }.map { it.patient }.take(2)`. Written on a List and on `asSequence()`, how many times does each run the filter/map lambdas?')
    B(C, S_, 1, 'ans', 'Với giờ 8, 13, 9, 10, 15, 11, 16, 9: List chạy 13 lần (filter cả 8, map cả 5 lịch buổi sáng) và tạo 2 list trung gian. Sequence chạy 5 lần: 8 giờ (filter, map), 13 giờ (filter), 9 giờ (filter, map), rồi dừng vì take đã đủ 2. Mô phỏng ngay dưới đếm từng bước. [[src:kt-sequences]]',
      'With hours 8, 13, 9, 10, 15, 11, 16, 9: the List runs 13 times (filter on all 8, map on all 5 morning ones) and builds 2 intermediate lists. The Sequence runs 5 times: 8 o\'clock (filter, map), 13 (filter), 9 (filter, map), then stops because take has 2. The simulation just below counts each step. [[src:kt-sequences]]')

    S_ = 'eager'
    a(C + '.sec.%s.title' % S_, 'List: háo hức, từng bước cho cả collection', 'List: eager, one step for the whole collection')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'p', 'Khi xử lý một Iterable (List, Set) qua nhiều bước, mỗi bước chạy ngay và trả về kết quả là một collection trung gian; bước sau chạy trên collection đó. Thứ tự là "từng bước": filter cho mọi phần tử, rồi map cho mọi phần tử còn lại. Effective Kotlin chỉ ra chi phí: mỗi bước tạo một collection mới, và với filter thì không biết trước kích thước, nên list có thể phải chép mảng bên trong khi lớn dần. [[src:kt-sequences]] [[src:book-effective-kotlin]]',
      'When an Iterable (List, Set) is processed in several steps, each step runs at once and returns its result as an intermediate collection; the next step runs on that collection. The order is "step by step": filter for every element, then map for every remaining one. Effective Kotlin points out the cost: each step creates a new collection, and with filter the size is not known in advance, so the list may need to copy its internal array as it grows. [[src:kt-sequences]] [[src:book-effective-kotlin]]')
    B(C, S_, 2, 'kt', 'val names = appts\n    .filter { it.hour < 12 }     // List mới (trung gian 1)\n    .map { it.patient }          // List mới (trung gian 2)\n    .take(2)                     // List kết quả\n\nval valid = rawHours.mapNotNull { it.toIntOrNull() }   // 1 bước thay vì map rồi filterNotNull',
      'val names = appts\n    .filter { it.hour < 12 }     // a new List (intermediate 1)\n    .map { it.patient }          // a new List (intermediate 2)\n    .take(2)                     // the result List\n\nval valid = rawHours.mapNotNull { it.toIntOrNull() }   // 1 step instead of map then filterNotNull')
    B(C, S_, 3, 'p', 'Cách rẻ nhất để giảm chi phí là giảm số bước: Effective Kotlin Item 57 gợi ý gộp các cặp hay gặp, như `mapNotNull` thay cho `map` rồi `filterNotNull`, hay `filterNotNull()` thay cho lọc khác null rồi ép sang kiểu non-null. [[src:book-effective-kotlin]] [[src:kt-collection-transformations]]',
      'The cheapest way to cut cost is to cut steps: Effective Kotlin Item 57 suggests merging common pairs, such as `mapNotNull` instead of `map` then `filterNotNull`, or `filterNotNull()` instead of filtering out nulls and then casting to a non-null type. [[src:book-effective-kotlin]] [[src:kt-collection-transformations]]')

    S_ = 'lazy'
    a(C + '.sec.%s.title' % S_, 'Sequence: lười, từng phần tử qua cả chuỗi', 'Sequence: lazy, each element through the whole chain')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'p', 'Sequence không chứa phần tử mà sinh ra chúng khi duyệt. Thao tác trả về Sequence khác (filter, map, take) là thao tác TRUNG GIAN và chỉ dựng chuỗi; thao tác trả về thứ khác (toList, first, sum, forEach) là thao tác CUỐI, và chỉ lúc đó chuỗi mới chạy. Khi chạy, mỗi phần tử đi qua mọi bước rồi mới tới phần tử sau, nên chuỗi có thể dừng ngay khi đủ kết quả. [[src:kt-sequences]]',
      'A Sequence holds no elements; it produces them while iterating. Operations returning another Sequence (filter, map, take) are INTERMEDIATE and only build the chain; operations returning something else (toList, first, sum, forEach) are TERMINAL, and only then does the chain run. When it runs, each element goes through every step before the next element, so the chain can stop as soon as it has enough. [[src:kt-sequences]]')
    B(C, S_, 2, 'kt', 'val firstTwo = appts.asSequence()      // từ List\n    .filter { it.hour < 12 }\n    .map { it.patient }\n    .take(2)\n    .toList()                          // thao tác cuối\n\nval reminders = generateSequence(9) { it + 1 }   // vô hạn: 9, 10, 11, …\n    .take(3).toList()                            // [9, 10, 11]',
      'val firstTwo = appts.asSequence()      // from a List\n    .filter { it.hour < 12 }\n    .map { it.patient }\n    .take(2)\n    .toList()                          // terminal operation\n\nval reminders = generateSequence(9) { it + 1 }   // infinite: 9, 10, 11, …\n    .take(3).toList()                            // [9, 10, 11]')
    B(C, S_, 3, 'p', 'Vì lười, Sequence còn có thể vô hạn: `generateSequence(seed) { next }` hay `sequence { yield(…) }` sinh phần tử theo yêu cầu; chỉ cần giới hạn bằng take hay first trước thao tác cuối. Một số thao tác như `sorted` cần xem hết phần tử (thao tác có trạng thái), nên không dừng sớm được. [[src:kt-sequences]]',
      'Being lazy, a Sequence can even be infinite: `generateSequence(seed) { next }` or `sequence { yield(…) }` produce elements on demand; just limit it with take or first before the terminal operation. Some operations, such as `sorted`, need to see every element (stateful operations), so they cannot stop early. [[src:kt-sequences]]')

    S_ = 'choose'
    a(C + '.sec.%s.title' % S_, 'Khi nào dùng Sequence', 'When to use a Sequence')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'p', 'Tài liệu nói rõ: tính lười có chi phí riêng, có thể đáng kể với collection nhỏ hay phép tính đơn giản, nên phải cân nhắc từng trường hợp. Quy tắc thực tế từ Effective Kotlin: dùng Sequence khi collection lớn (hay nặng) VÀ có từ hai bước xử lý trở lên, hoặc khi cần dừng sớm (first, take) hay sinh phần tử vô hạn. Danh sách vài chục phần tử trên màn hình thì cứ dùng List. [[src:kt-sequences]] [[src:book-effective-kotlin]]',
      'The docs are explicit: laziness has its own overhead, which may be significant for small collections or simple computations, so decide case by case. The practical rule from Effective Kotlin: use a Sequence when the collection is big (or heavy) AND there are two or more processing steps, or when you need to stop early (first, take) or produce elements without end. For a list of a few dozen items on a screen, just use a List. [[src:kt-sequences]] [[src:book-effective-kotlin]]')
    B(C, S_, 2, 'note', 'Đặt tác dụng phụ (gửi tin, ghi log, sửa trạng thái) trong `forEach`, không trong `map` hay `filter`. Với Sequence, lambda của thao tác trung gian chỉ chạy khi và bao nhiêu lần chuỗi cần, nên việc gửi tin trong map có thể không bao giờ xảy ra. [[src:kt-sequences]]',
      'Put side effects (sending, logging, changing state) in `forEach`, not in `map` or `filter`. With a Sequence, an intermediate operation\'s lambda runs only when and as often as the chain needs it, so a send inside map may never happen. [[src:kt-sequences]]')
    B(C, S_, 2, 'kind', 'pitfall')

    S_ = 'bugs'
    a(C + '.sec.%s.title' % S_, 'Hai lỗi hay gặp', 'Two common bugs')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'bug', 'Tính năng "nhắc lịch buổi sáng" chạy không lỗi, có log "đã chạy remindMorning", nhưng không bệnh nhân nào nhận được tin.', 'The "morning reminder" feature runs without errors and logs "remindMorning ran", but no patient receives a message.')
    B(C, S_, 1, 'cause', '`appts.asSequence().filter { … }.map { sendReminder(it) }` không có thao tác cuối, nên chuỗi không bao giờ chạy.', '`appts.asSequence().filter { … }.map { sendReminder(it) }` has no terminal operation, so the chain never runs.')
    B(C, S_, 1, 'fix', 'Kết thúc bằng `forEach { sendReminder(it) }`; với vài chục lịch hẹn, bỏ hẳn asSequence() và dùng List.', 'End with `forEach { sendReminder(it) }`; with a few dozen appointments, drop asSequence() and use a List.')
    B(C, S_, 2, 'bug', 'Màn "Tìm phòng khám gần nhất" giật khi lọc danh sách 50 000 phòng khám, dù chỉ hiện 20 kết quả đầu.', 'The "Find the nearest clinic" screen stutters when filtering a list of 50,000 clinics, though only the first 20 results are shown.')
    B(C, S_, 2, 'cause', '`clinics.filter { it.isOpen }.map { toUiModel(it) }.take(20)` trên List: lọc và chuyển đổi cả danh sách, tạo hai list trung gian lớn, rồi bỏ gần hết.', '`clinics.filter { it.isOpen }.map { toUiModel(it) }.take(20)` on a List: filters and converts the whole list, builds two big intermediate lists, then throws almost everything away.')
    B(C, S_, 2, 'fix', 'Dùng `clinics.asSequence().filter { … }.map { … }.take(20).toList()`: chỉ xử lý tới khi đủ 20, không có list trung gian. (Việc lọc nặng vẫn nên chạy ngoài main thread, xem track Coroutines.)', 'Use `clinics.asSequence().filter { … }.map { … }.take(20).toList()`: it processes only until it has 20, with no intermediate lists. (Heavy filtering should still run off the main thread, see the Coroutines track.)')

    S_ = 'ex'
    a(C + '.sec.%s.title' % S_, 'Bài tập', 'Exercise')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'ex', 'Cho `fun f(h: Int): Boolean { print("f$h "); return h < 12 }`, `fun g(h: Int): String { print("g$h "); return "$h:00" }` và `val hours = listOf(13, 9, 10)`. Mỗi dòng sau in ra gì? (a) `hours.filter(::f).map(::g)` (b) `hours.asSequence().filter(::f).map(::g)` (c) `hours.asSequence().filter(::f).map(::g).first()` (d) `hours.asSequence().filter(::f).map(::g).toList()`. (Dựa trên bài "Understanding sequences" của Kotlin Exercises, diễn đạt lại.) [[src:book-kt-exercises]]',
      'Given `fun f(h: Int): Boolean { print("f$h "); return h < 12 }`, `fun g(h: Int): String { print("g$h "); return "$h:00" }` and `val hours = listOf(13, 9, 10)`, what does each line print? (a) `hours.filter(::f).map(::g)` (b) `hours.asSequence().filter(::f).map(::g)` (c) `hours.asSequence().filter(::f).map(::g).first()` (d) `hours.asSequence().filter(::f).map(::g).toList()`. (Based on the "Understanding sequences" exercise in Kotlin Exercises, restated.) [[src:book-kt-exercises]]')
    B(C, S_, 1, 'hint', 'List: hết bước này mới sang bước kia. Sequence: không in gì nếu không có thao tác cuối; có thì từng phần tử qua f rồi g.', 'List: one step entirely, then the next. Sequence: prints nothing without a terminal operation; with one, each element goes through f, then g.')
    B(C, S_, 1, 'sol', '(a) f13 f9 f10 g9 g10 (b) không in gì (c) f13 f9 g9 (d) f13 f9 g9 f10 g10', '(a) f13 f9 f10 g9 g10 (b) prints nothing (c) f13 f9 g9 (d) f13 f9 g9 f10 g10')

    S_ = 'recall'
    a(C + '.sec.%s.title' % S_, 'Tự trả lời', 'Answer it yourself')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'ask', 'Vì sao Sequence không có thao tác cuối thì không làm gì?', 'Why does a Sequence without a terminal operation do nothing?')
    B(C, S_, 1, 'ans', 'Thao tác trung gian chỉ dựng chuỗi và trả về Sequence mới; phần tử chỉ được sinh và xử lý khi một thao tác cuối yêu cầu kết quả.', 'Intermediate operations only build the chain and return a new Sequence; elements are produced and processed only when a terminal operation asks for a result.')
    B(C, S_, 2, 'ask', 'Khi nào List tốt hơn Sequence?', 'When is a List better than a Sequence?')
    B(C, S_, 2, 'ans', 'Khi collection nhỏ, chỉ có một bước, hay phép tính đơn giản: chi phí của tính lười khi đó lớn hơn lợi ích.', 'When the collection is small, there is just one step, or the computation is simple: the overhead of laziness then outweighs the benefit.')

    S_ = 'honest'
    a(C + '.sec.%s.title' % S_, 'Chương này giản lược những gì', 'What this chapter simplifies')
    a(C + '.sec.%s.badge' % S_, 'simplified')
    B(C, S_, 1, 'p', 'Thứ tự chạy và khái niệm trung gian/cuối theo trang Sequences đọc ngày 2026-11-23; lời khuyên chọn Sequence theo Effective Kotlin Items 54 và 57. Sơ đồ chỉ đếm số lần chạy lambda và số list trung gian trên 8 phần tử mẫu; nó không đo thời gian, bộ nhớ hay chi phí của chính Sequence, nên đừng coi "5 so với 13" là tỉ lệ tốc độ. Muốn biết nhanh hơn thật hay không thì đo bằng benchmark trên thiết bị. Chương bỏ qua Java Stream, xử lý song song, và chi tiết cài đặt của từng thao tác Sequence trong stdlib.',
      'The execution order and the intermediate/terminal distinction follow the Sequences page as read on 2026-11-23; the advice on choosing Sequence follows Effective Kotlin Items 54 and 57. The diagram only counts lambda runs and intermediate lists over 8 sample elements; it does not measure time, memory or the overhead of the Sequence itself, so do not read "5 versus 13" as a speed ratio. To know whether it is really faster, benchmark on a device. The chapter skips Java Streams, parallel processing, and the stdlib implementation details of each Sequence operation.')

    for q, qv, qe, av, ae, wv, we in [
        ('q1', '`listOf(1, 2, 3).asSequence().map { it * 2 }` đã chạy lambda chưa?', 'Has `listOf(1, 2, 3).asSequence().map { it * 2 }` run the lambda yet?', 'Chưa.', 'No.', 'map trên Sequence là thao tác trung gian; cần thao tác cuối.', 'map on a Sequence is intermediate; a terminal operation is needed.'),
        ('q2', 'Thao tác nào là thao tác cuối: filter, take, toList?', 'Which one is a terminal operation: filter, take, toList?', 'toList.', 'toList.', 'filter và take trả về Sequence mới.', 'filter and take return a new Sequence.'),
        ('q3', 'Trên List, `filter { … }.map { … }` tạo bao nhiêu list trung gian trước kết quả?', 'On a List, how many intermediate lists does `filter { … }.map { … }` build before the result?', 'Một (kết quả của filter); map trả về list kết quả.', 'One (filter\'s result); map returns the result list.', 'Mỗi bước của Iterable trả về một collection mới.', 'Each Iterable step returns a new collection.'),
        ('q4', 'Sequence có luôn nhanh hơn List không?', 'Is a Sequence always faster than a List?', 'Không.', 'No.', 'Tính lười có chi phí riêng, đáng kể với collection nhỏ hay phép tính đơn giản.', 'Laziness has its own overhead, noticeable for small collections or simple computations.')]:
        a(C + '.quiz.%s.q' % q, qv, qe); a(C + '.quiz.%s.a' % q, av, ae); a(C + '.quiz.%s.why' % q, wv, we)
