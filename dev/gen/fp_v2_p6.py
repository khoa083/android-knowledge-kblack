# Lập trình hàm · K6 (p6): map và flatMap: functor và monad qua ví dụ (Phần 2: lỗi, ngữ cảnh và state)
# Nguồn (chỉ ghi ở đây và docs/research/fp.md): Carli, FP in Kotlin by Tutorials ch.11 (functor giữ cấu trúc: đơn vị và ghép), ch.13 (hàm (A) -> M<B>,
# flatten M<M<A>> -> M<A>, flatMap từ map và flatten), ch.14 (Result có map nhưng không có flatMap); Vermeulen, Bjarnason, Chiusano, FP in Kotlin ch.11
# (functor tổng quát hóa map; monad là flatMap cùng unit; luật kết hợp và đơn vị); API kotlin.Result (2.4, đọc 2026-11-25). Giọng văn dạy học.

SEC_ORDER = {'p6': ['hook', 'map', 'nest', 'flat', 'chain', 'bugs', 'ex', 'recall']}


def add(a):
    def B(ch, sec, n, field, vi, en=None):
        a('%s.sec.%s.b.%02d.%s' % (ch, sec, n, field), vi, vi if en is None else en)

    a('preset.monad', '''Lập trình hàm · map và flatMap''', '''Functional programming · map and flatMap''')
    m = lambda k, vi, en=None: a('m.monad.' + k, vi, en)
    m('title', '''Ba loại hộp, cùng map và flatMap''', '''Three kinds of box, the same map and flatMap''')
    m('overview', '''Ba loại hộp trong app Hẹn Khám: List các bác sĩ, một bệnh nhân có thể không có (Patient?), và kết quả đọc số điện thoại có thể lỗi (Outcome). Trên mỗi hộp ta chạy cùng ba thao tác: map với một hàm thường, map với một hàm cũng trả hộp, và flatMap; rồi nối nhiều bước thành một chuỗi.''',
      '''Three kinds of box in the ClinicBook app: a List of doctors, a patient who may be missing (Patient?), and the result of reading a phone number, which may be an error (Outcome). On each box we run the same three operations: map with a plain function, map with a function that also returns a box, and flatMap; then we chain several steps.''')
    m('wrapup', '''map giữ nguyên cái hộp; khi hàm cũng trả hộp, map cho hộp trong hộp, còn flatMap gộp lại còn một tầng. List và Outcome lồng thật; kiểu nullable thì không, nên ?.let làm được cả hai việc nhưng mất lý do khi ra null. Nối các bước bằng flatMap cho một chuỗi không cần return, dừng ở lỗi đầu tiên.''',
      '''map keeps the box as it is; when the function also returns a box, map gives a box in a box, while flatMap merges it back into one level. List and Outcome really nest; nullable types do not, so ?.let does both jobs but loses the reason when it ends in null. Chaining steps with flatMap gives a chain with no return that stops at the first error.''')
    m('simp.1', '''Mỗi hộp chỉ dùng một ví dụ nhỏ; cách đếm "tầng hộp" ở đây không xét List rỗng hay null nằm giữa chừng.''',
      '''Each box uses one small example; counting "box levels" here ignores an empty List or a null partway through.''')
    m('simp.2', '''map, flatMap và flatten chạy thật trên dữ liệu bằng JavaScript; việc Result có map nhưng không có flatMap theo trang API của thư viện chuẩn Kotlin (bản 2.4, đọc ngày 2026-11-25). Outcome và Result.flatMap là mã tự viết của site. Site không chạy Kotlin trong trang.''',
      '''map, flatMap and flatten really run on the data in JavaScript; that Result has map but no flatMap follows the Kotlin standard library API page (version 2.4, read on 2026-11-25). Outcome and Result.flatMap are code the site writes itself. The site does not run Kotlin in the page.''')
    m('ctl.hint', '''Chọn một loại hộp rồi đi qua bốn bước; để ý ô viền đỏ có hai khung ở bước 2.''', '''Pick a kind of box and walk the four steps; watch for the red, double-framed box at step 2.''')
    m('ctl.case', '''Loại hộp''', '''Kind of box''')
    for k, vi, en in [('list', 'List (nhiều giá trị)', 'List (many values)'), ('nullable', 'kiểu nullable (có thể không có)', 'nullable type (may be missing)'), ('outcome', 'Outcome (có thể lỗi)', 'Outcome (may be an error)')]:
        m('ctl.case.' + k, vi, en)
    m('diagramTitle', '''Hộp, hàm, kết quả, flatten, chuỗi''', '''Box, function, result, flatten, chain''')
    m('diagramDesc', '''Hộp ban đầu đi qua hàm; kết quả có thể là hộp trong hộp; flatten gộp lại; nhiều bước nối thành chuỗi''', '''The starting box goes through the function; the result may be a box in a box; flatten merges it; several steps form a chain''')
    for k, vi, en in [('box', 'Hộp ban đầu', 'Starting box'), ('fn', 'Hàm truyền vào', 'The function passed in'), ('out', 'Kết quả', 'Result'), ('flat', 'flatten', 'flatten'), ('chain', 'Chuỗi nhiều bước', 'A chain of steps')]:
        m('n.' + k, vi, en)
    m('met.nest', '''Số tầng hộp''', '''Box levels'''); m('met.size', '''Số giá trị trong hộp''', '''Values in the box'''); m('met.calls', '''Số lần hàm chạy''', '''Times the function ran''')
    a('cap.monad', '''Hộp ban đầu đi qua hàm truyền vào; nếu hàm cũng trả một hộp, kết quả là hộp trong hộp, và flatten gộp lại còn một tầng. Ô đỏ: hộp lồng hai tầng.''',
      '''The starting box goes through the function passed in; if the function also returns a box, the result is a box in a box, and flatten merges it back into one level. A red box: two nested levels.''')
    S = [
        ('list', 's1', 'map giữ nguyên hình dạng hộp', 'map keeps the shape of the box',
         'doctors là một List 2 phần tử. map(f) chạy f = displayName cho từng phần tử và trả một List mới cũng 2 phần tử: [BS An, BS Bình]. map đổi giá trị bên trong, không đổi cái hộp: vẫn là List, vẫn 2 phần tử, vẫn đúng thứ tự.',
         'doctors is a 2-element List. map(f) runs f = displayName on each element and returns a new List that also has 2 elements: [Dr An, Dr Binh]. map changes the values inside, not the box: still a List, still 2 elements, still in order.'),
        ('list', 's2', 'Hàm trả List: hộp trong hộp', 'A function returning a List: a box in a box',
         'g = slotsToday trả về một List giờ trống cho mỗi bác sĩ. map(g) đặt mỗi List đó vào một ô, nên ra List<List<Slot>>: [[S12, S13], [S20]]. Muốn đếm tổng số giờ trống, bạn phải mở hai tầng.',
         'g = slotsToday returns a List of free slots for each doctor. map(g) puts each of those Lists into one cell, giving List<List<Slot>>: [[S12, S13], [S20]]. To count all free slots, you must open two levels.'),
        ('list', 's3', 'flatMap = map rồi flatten', 'flatMap = map, then flatten',
         'flatMap(g) chạy g cho từng bác sĩ rồi trải phẳng các list con: [S12, S13, S20]. Viết map(g).flatten() cũng ra đúng kết quả đó: flatMap chỉ là map rồi gộp bớt một tầng hộp.',
         'flatMap(g) runs g for each doctor and then flattens the inner lists: [S12, S13, S20]. Writing map(g).flatten() gives exactly the same result: flatMap is just map followed by removing one box level.'),
        ('list', 's4', 'Nối nhiều bước bằng flatMap', 'Chaining steps with flatMap',
         'Mọi bác sĩ, cả thứ Bảy và Chủ nhật: doctors.flatMap { d -> days.flatMap { day -> slotsOn(d, day) } }. Hàm bên trong chạy 4 lần (2 bác sĩ × 2 ngày), và kết quả vẫn là một List phẳng: [S12, S13, S20, S31].',
         'Every doctor, both Saturday and Sunday: doctors.flatMap { d -> days.flatMap { day -> slotsOn(d, day) } }. The inner function runs 4 times (2 doctors × 2 days), and the result is still one flat List: [S12, S13, S20, S31].'),
        ('nullable', 's1', '?.let là map của kiểu nullable', '?.let is the map of nullable types',
         'lan có kiểu Patient?. lan?.let { it.name } chạy hàm khi lan khác null và trả "Lan"; nếu lan là null thì cả biểu thức là null và hàm không chạy. Đó chính là map: đổi giá trị bên trong, giữ cái hộp "có thể không có".',
         'lan has type Patient?. lan?.let { it.name } runs the function when lan is not null and returns "Lan"; if lan is null, the whole expression is null and the function does not run. That is exactly map: change the value inside, keep the "may be missing" box.'),
        ('nullable', 's2', 'Không có hộp lồng', 'No nested box',
         'insuranceCard có kiểu String?, nên hàm g trả về một hộp nữa. Với List hay Outcome, ta sẽ có hộp trong hộp. Kotlin thì không có kiểu String?? riêng: null bên ngoài và null bên trong là cùng một null, nên kết quả vẫn là String? một tầng.',
         'insuranceCard has type String?, so g returns another box. With a List or an Outcome we would get a box in a box. Kotlin has no separate String?? type: the outer null and the inner null are the same null, so the result is still a one-level String?.'),
        ('nullable', 's3', '?.let vừa là map vừa là flatMap', '?.let is both map and flatMap',
         'Không có tầng lồng để gộp, nên flatMap cho cùng kết quả với map: "BHYT-4471". Cái giá là thông tin: với Minh (không có thẻ), findPatient(...)?.let { it.insuranceCard } cũng trả null, y như khi không tìm thấy bệnh nhân. Đây đúng là chuyện "mất lý do" ở chương "Lỗi là giá trị".',
         'There is no nested level to merge, so flatMap gives the same result as map: "BHYT-4471". The price is information: for Minh (who has no card), findPatient(...)?.let { it.insuranceCard } also returns null, exactly as when no patient is found. This is the "lost reason" problem from the chapter "Errors as values".'),
        ('nullable', 's4', 'Chuỗi ?.let', 'A chain of ?.let',
         'findPatient(phone)?.let { p -> p.insuranceCard?.let { coverageOf(it) } } đi qua hai bước có thể thiếu; bước nào ra null thì dừng ở đó. Với Lan, kết quả là 80 (phần trăm được chi trả).',
         'findPatient(phone)?.let { p -> p.insuranceCard?.let { coverageOf(it) } } goes through two steps that may be missing; whichever step gives null stops there. For Lan, the result is 80 (the percentage covered).'),
        ('outcome', 's1', 'map trên Outcome', 'map on an Outcome',
         'parsePhone trả Outcome<BookingError, Phone>. map { it.masked() } chỉ chạy khi đó là Ok: Ok("0901234567") thành Ok("090•••4567"). Nếu là Err, map trả lại chính Err đó và hàm không chạy.',
         'parsePhone returns Outcome<BookingError, Phone>. map { it.masked() } only runs on an Ok: Ok("0901234567") becomes Ok("090•••4567"). On an Err, map returns that same Err and the function does not run.'),
        ('outcome', 's2', 'Ok(Ok(Unit)): hộp trong hộp', 'Ok(Ok(Unit)): a box in a box',
         'ensureQuota(phone) cũng trả Outcome, vì kiểm lượt cũng có thể hỏng. phone.map { ensureQuota(it) } vì thế cho Outcome<E, Outcome<E, Unit>>: Ok(Ok(Unit)). Nơi dùng phải mở hai tầng và xử lý lỗi ở hai chỗ. Đây chính là lỗi Result<Result<T>> hay gặp.',
         'ensureQuota(phone) also returns an Outcome, because the quota check can fail too. So phone.map { ensureQuota(it) } gives Outcome<E, Outcome<E, Unit>>: Ok(Ok(Unit)). Callers must open two levels and handle errors in two places. This is the common Result<Result<T>> bug.'),
        ('outcome', 's3', 'flatMap gộp còn một tầng', 'flatMap merges it into one level',
         'phone.flatMap { ensureQuota(it) } cho Ok(Unit): nếu phone là Ok, lấy luôn kết quả của ensureQuota làm kết quả; nếu phone là Err, trả lại Err đó. Một tầng hộp, một chỗ xử lý lỗi.',
         'phone.flatMap { ensureQuota(it) } gives Ok(Unit): if phone is Ok, the result of ensureQuota becomes the result; if phone is Err, that Err comes back. One box level, one place to handle errors.'),
        ('outcome', 's4', 'Viết lại book bằng flatMap', 'Rewriting book with flatMap',
         'book giờ là parsePhone(raw).flatMap { p -> findFreeSlot(slotId).flatMap { s -> ensureQuota(p).map { save(p, s) } } }. Không còn return nào. Với giờ S07, findFreeSlot trả Err(SlotTaken("S07")) và hai bước sau không chạy: đúng đường ray ở chương "Lỗi là giá trị".',
         'book is now parsePhone(raw).flatMap { p -> findFreeSlot(slotId).flatMap { s -> ensureQuota(p).map { save(p, s) } } }. No return left. With slot S07, findFreeSlot returns Err(SlotTaken("S07")) and the next two steps do not run: the same railway as in the chapter "Errors as values".'),
    ]
    for case, k, tv, te, xv, xe in S:
        sid = case + '.' + k
        m('s.%s.title' % sid, tv, te); m('s.%s.explain' % sid, xv, xe); m('ev.' + sid, tv, te)
    for k, vi, en in [
        ('try', '''Mẹo đọc: hộp bên trái là giá trị ban đầu; ba nhánh bên phải là map với hàm thường (f), map với hàm trả hộp (g), và flatMap với cùng g. Hộp viền đỏ có hai khung là hộp trong hộp.''',
         '''Reading tip: the box on the left is the starting value; the three branches on the right are map with a plain function (f), map with a box-returning function (g), and flatMap with the same g. A red box with two frames is a box in a box.'''),
        ('list.s2', '''Massimo Carli gọi các hàm dạng (A) -> M<B> (trả về một giá trị đã bọc trong hộp M) là thứ cần một cách ghép riêng, vì map với chúng sinh ra M<M<B>>. [[src:book-fp-tut]]''',
         '''Massimo Carli singles out functions of the form (A) -> M<B> (returning a value already wrapped in a box M) as needing their own way to compose, because map with them produces M<M<B>>. [[src:book-fp-tut]]'''),
        ('list.s3', '''Carli định nghĩa flatten có kiểu M<M<A>> -> M<A>, và dựng flatMap từ map với flatten. [[src:book-fp-tut]]''',
         '''Carli defines flatten with the type M<M<A>> -> M<A>, and builds flatMap from map and flatten. [[src:book-fp-tut]]'''),
        ('list.s4', '''Luật thứ hai của functor, kiểm bằng ví dụ: map(f).map(g) cho cùng kết quả với map { g(f(it)) }. Luật chỉ đúng khi f và g thuần, như chương "Ghép hàm" của track này đã chỉ ra. [[src:book-fp-tut]]''',
         '''The second functor law, checked by example: map(f).map(g) gives the same result as map { g(f(it)) }. It only holds when f and g are pure, as this track\'s chapter "Composing functions" showed. [[src:book-fp-tut]]'''),
        ('nullable.s1', '''Marco Vermeulen và cộng sự chỉ ra rằng map của Option, của List và của nhiều kiểu khác có chữ ký chỉ khác nhau ở tên hộp; ý chung đó gọi là functor (kiểu có map giữ nguyên cấu trúc). [[src:book-fp-manning]]''',
         '''Marco Vermeulen and co-authors point out that the map of Option, of List and of many other types has a signature that differs only in the name of the box; that shared idea is called a functor (a type with a structure-preserving map). [[src:book-fp-manning]]'''),
        ('nullable.s2', '''Kiểu nullable của Kotlin không lồng được: làm nullable một kiểu đã nullable vẫn chỉ ra kiểu nullable đó. Vì vậy ?.let làm được cả hai việc.''',
         '''Kotlin\'s nullable types do not nest: making an already nullable type nullable again gives the same nullable type. That is why ?.let can do both jobs.'''),
        ('nullable.s3', '''Hai lý do (không có bệnh nhân, không có thẻ) cùng thành null. Khi màn hình cần nói rõ vì sao, dùng một kiểu lỗi riêng như Outcome.''',
         '''Two reasons (no patient, no card) both become null. When the screen must say why, use a custom error type such as Outcome.'''),
        ('nullable.s4', '''Chuỗi ?.let dừng ở null đầu tiên, giống cách "dừng sớm" (fail fast) ở chương "Lỗi là giá trị".''',
         '''A chain of ?.let stops at the first null, like fail fast in the chapter "Errors as values".'''),
        ('outcome.s1', '''Luật thứ nhất của functor, kiểm bằng ví dụ: map với hàm đồng nhất không đổi gì; Ok("0901234567").map { it } vẫn là Ok("0901234567"). [[src:book-fp-tut]]''',
         '''The first functor law, checked by example: map with the identity function changes nothing; Ok("0901234567").map { it } is still Ok("0901234567"). [[src:book-fp-tut]]'''),
        ('outcome.s2', '''Carli chỉ ra rằng Result của thư viện chuẩn có map nhưng không có flatMap; ghép hai hàm trả Result bằng map sẽ ra Result<Result<T>>. [[src:book-fp-tut]] [[src:kt-result]]''',
         '''Carli points out that the standard library\'s Result has map but no flatMap; composing two Result-returning functions with map gives Result<Result<T>>. [[src:book-fp-tut]] [[src:kt-result]]'''),
        ('outcome.s3', '''Vermeulen và cộng sự: một kiểu có flatMap cùng một cách bọc giá trị vào hộp (ở đây là Ok), và tuân theo vài luật đơn giản, thì gọi là monad. [[src:book-fp-manning]]''',
         '''Vermeulen and co-authors: a type with flatMap plus a way to wrap a value in the box (here, Ok) that obeys a few simple laws is called a monad. [[src:book-fp-manning]]'''),
        ('outcome.s4', '''Khối either { } của Arrow ở chương "Lỗi là giá trị" là cùng ý flatMap này nhưng viết phẳng: mỗi .bind() thay cho một tầng flatMap lồng nhau. [[src:arrow-typed-errors]]''',
         '''Arrow\'s either { } block from the chapter "Errors as values" is the same flatMap idea written flat: each .bind() replaces one nested flatMap. [[src:arrow-typed-errors]]'''),
    ]:
        m('co.' + k, vi, en)

    z = lambda k, vi, en=None: a('vz.' + k, vi, en)
    z('tab.monad', '''Hộp và giá trị''', '''Boxes and values''')
    z('monad.aria', '''Hộp ban đầu và ba nhánh map(f), map(g), flatMap(g); kết quả mới nhất có {n} tầng hộp''', '''The starting box and three branches map(f), map(g), flatMap(g); the latest result has {n} box levels''')
    z('monad.fg.list', '''f = tên hiển thị của bác sĩ; g = các giờ trống hôm nay của bác sĩ (trả về List).''', '''f = the doctor\'s display name; g = the doctor\'s free slots today (returns a List).''')
    z('monad.fg.nullable', '''f = tên bệnh nhân; g = thẻ bảo hiểm của bệnh nhân (trả về String?).''', '''f = the patient\'s name; g = the patient\'s insurance card (returns String?).''')
    z('monad.fg.outcome', '''f = che bớt số điện thoại; g = ensureQuota, kiểm lượt còn lại (trả về Outcome).''', '''f = mask the phone number; g = ensureQuota, the remaining-quota check (returns an Outcome).''')
    z('monad.nest', '''Kết quả mới nhất có {n} tầng hộp.''', '''The latest result has {n} box levels.''')
    z('monad.chain.list', '''Chuỗi (bước 4): mọi bác sĩ, thứ Bảy và Chủ nhật''', '''Chain (step 4): every doctor, Saturday and Sunday''')
    z('monad.chain.nullable', '''Chuỗi (bước 4): bệnh nhân → thẻ → mức chi trả (%)''', '''Chain (step 4): patient → card → coverage (%)''')
    z('monad.chain.outcome', '''Chuỗi (bước 4): book(…) với giờ S07''', '''Chain (step 4): book(…) with slot S07''')
    z('monad.chain.none', '''Bước 4 sẽ nối nhiều bước thành một chuỗi.''', '''Step 4 chains several steps together.''')
    z('monad.legend', '''Mỗi khung là một tầng hộp; hai khung lồng nhau là hộp trong hộp (viền đỏ). Viền xanh: nhánh của bước này. Nét đứt và "?": nhánh chưa tới.''',
      '''Each frame is one box level; two nested frames are a box in a box (red outline). Green outline: this step\'s branch. Dashed with "?": a branch not reached yet.''')

    C = 'p6'
    a(C + '.title', '''map và flatMap: functor và monad qua ví dụ''', '''map and flatMap: functors and monads by example''')
    a(C + '.essence', '''map áp một hàm thường lên giá trị trong hộp (List, T?, Result, Outcome) và giữ nguyên cái hộp; kiểu có map như vậy gọi là functor.\nKhi hàm cũng trả một hộp, map sinh ra hộp trong hộp (List<List<T>>, Outcome<E, Outcome<E, T>>). flatMap = map rồi flatten, gộp lại còn một tầng; kiểu có flatMap cùng một cách bọc giá trị vào hộp gọi là monad.\nNối nhiều bước có thể hỏng bằng flatMap thì không cần return, và bước hỏng dừng cả chuỗi. Riêng kiểu nullable không lồng được, nên ?.let vừa là map vừa là flatMap.''',
      '''map applies a plain function to the value inside a box (List, T?, Result, Outcome) and keeps the box as it is; a type with such a map is called a functor.\nWhen the function also returns a box, map produces a box in a box (List<List<T>>, Outcome<E, Outcome<E, T>>). flatMap = map then flatten, merging it back into one level; a type with flatMap and a way to wrap a value in the box is called a monad.\nChaining steps that can fail with flatMap needs no return, and a failing step stops the whole chain. Nullable types alone cannot nest, so ?.let is both map and flatMap.''')
    a(C + '.goal.g1', '''Đã thấy hộp trong hộp''', '''Saw a box in a box''')
    a(C + '.goal.g2', '''Đã nối nhiều bước bằng flatMap''', '''Chained several steps with flatMap''')
    a(C + '.sim.fp.monad', '''map và flatMap trên List, nullable và Outcome''', '''map and flatMap on List, nullable and Outcome''')

    S_ = 'hook'
    a(C + '.sec.%s.title' % S_, '''Đoán trước khi đọc''', '''Predict before reading''')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'predict', '''`doctors.map { slotsToday(it) }`, với slotsToday trả List<Slot>, cho ra kiểu gì? Còn `phone.map { ensureQuota(it) }`, với ensureQuota trả Outcome<BookingError, Unit>?''',
      '''What type does `doctors.map { slotsToday(it) }` give, with slotsToday returning List<Slot>? And `phone.map { ensureQuota(it) }`, with ensureQuota returning Outcome<BookingError, Unit>?''')
    B(C, S_, 1, 'ans', '''List<List<Slot>> và Outcome<BookingError, Outcome<BookingError, Unit>>: hộp trong hộp. map đặt kết quả của hàm vào lại cái hộp cũ; khi hàm đã trả một hộp, ta có hai tầng. flatMap là cách gộp lại còn một tầng. Mô phỏng ngay dưới chạy cùng ba thao tác trên ba loại hộp.''',
      '''List<List<Slot>> and Outcome<BookingError, Outcome<BookingError, Unit>>: a box in a box. map puts the function's result back into the original box; when the function already returns a box, you get two levels. flatMap is how to merge them into one. The simulation just below runs the same three operations on three kinds of box.''')

    S_ = 'map'
    a(C + '.sec.%s.title' % S_, '''map: đổi giá trị, giữ cái hộp''', '''map: change the value, keep the box''')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'p', '''List, kiểu nullable, Result và Outcome ở chương trước đều là những "hộp" chứa giá trị kèm một ngữ cảnh: nhiều giá trị, có thể không có, có thể là lỗi. map nhận một hàm thường (A) -> B, chạy nó trên giá trị bên trong và trả lại cùng loại hộp: List<A> thành List<B>, Outcome<E, A> thành Outcome<E, B>. Hộp rỗng hay hộp lỗi thì hàm không chạy và hộp giữ nguyên. [[src:book-fp-tut]]''',
      '''List, nullable types, Result and the previous chapter\'s Outcome are all "boxes" holding a value plus some context: many values, maybe missing, maybe an error. map takes a plain function (A) -> B, runs it on the value inside and returns the same kind of box: List<A> becomes List<B>, Outcome<E, A> becomes Outcome<E, B>. With an empty or error box, the function does not run and the box stays as it is. [[src:book-fp-tut]]''')
    B(C, S_, 2, 'p', '''Marco Vermeulen và cộng sự chỉ ra rằng chữ ký map của các hộp này chỉ khác nhau ở tên hộp. Kiểu có map như vậy gọi là functor: kiểu biết cách áp một hàm vào giá trị bên trong mà giữ nguyên cấu trúc. Hai luật, kiểm được bằng ví dụ (map của Outcome được viết ở mục "flatMap = map rồi flatten" bên dưới): `map { it }` không đổi gì; và `map(f).map(g)` bằng `map { g(f(it)) }`, miễn là f và g thuần (chương "Ghép hàm" của track này). [[src:book-fp-manning]] [[src:book-fp-tut]]''',
      '''Marco Vermeulen and co-authors point out that the map signatures of these boxes differ only in the box\'s name. A type with such a map is called a functor: a type that knows how to apply a function to the value inside while keeping its structure. Two laws, checkable by example (map for Outcome is written in the section "flatMap = map, then flatten" below): `map { it }` changes nothing; and `map(f).map(g)` equals `map { g(f(it)) }`, as long as f and g are pure (this track\'s chapter "Composing functions"). [[src:book-fp-manning]] [[src:book-fp-tut]]''')
    B(C, S_, 3, 'kt', '''doctors.map { it }                                  // == doctors
doctors.map(::displayName).map { it.length }        // == doctors.map { displayName(it).length }
Ok("0901234567").map { it }                         // == Ok("0901234567")''')

    S_ = 'nest'
    a(C + '.sec.%s.title' % S_, '''Khi hàm cũng trả một hộp''', '''When the function also returns a box''')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'p', '''Rắc rối bắt đầu khi hàm truyền vào cũng trả về một hộp, tức có dạng (A) -> M<B>. Với giờ trống: slotsToday(doctor) trả List<Slot>. Với đặt lịch: ensureQuota(phone) trả Outcome. map đặt kết quả đó vào lại hộp cũ, nên ra hộp trong hộp: List<List<Slot>>, Outcome<E, Outcome<E, Unit>>. Massimo Carli coi việc ghép các hàm dạng này là đúng bài toán mà monad giải. [[src:book-fp-tut]]''',
      '''Trouble starts when the function passed in also returns a box, that is, it has the form (A) -> M<B>. For free slots: slotsToday(doctor) returns List<Slot>. For booking: ensureQuota(phone) returns an Outcome. map puts that result back into the original box, so you get a box in a box: List<List<Slot>>, Outcome<E, Outcome<E, Unit>>. Massimo Carli treats composing such functions as exactly the problem monads solve. [[src:book-fp-tut]]''')
    B(C, S_, 2, 'p', '''Hộp lồng làm khổ nơi dùng: phải mở hai tầng, và với Outcome phải xử lý lỗi ở hai chỗ. Với Result của thư viện chuẩn, đây là lỗi Result<Result<T>> rất hay gặp, vì Result có map nhưng không có flatMap. [[src:book-fp-tut]] [[src:kt-result]]''',
      '''Nested boxes make life hard for callers: they must open two levels, and with Outcome handle errors in two places. With the standard library\'s Result, this is the very common Result<Result<T>> bug, because Result has map but no flatMap. [[src:book-fp-tut]] [[src:kt-result]]''')
    B(C, S_, 3, 'note', '''Kiểu nullable là trường hợp dễ chịu: Kotlin không có kiểu String?? riêng, nên ?.let với một hàm trả T? vẫn chỉ cho T?. ?.let vì thế đóng cả vai map lẫn flatMap. Đổi lại, null ở cuối không cho biết bước nào thiếu.''',
      '''Nullable types are the easy case: Kotlin has no separate String?? type, so ?.let with a function returning T? still gives just T?. So ?.let plays both map and flatMap. In exchange, a null at the end does not tell you which step was missing.''')
    B(C, S_, 3, 'kind', 'mechanism')

    S_ = 'flat'
    a(C + '.sec.%s.title' % S_, '''flatMap = map rồi flatten''', '''flatMap = map, then flatten''')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'p', '''flatten gộp hai tầng hộp làm một: List<List<A>> thành List<A>, Outcome<E, Outcome<E, A>> thành Outcome<E, A>. flatMap chỉ là map rồi flatten, gói lại thành một bước. Với List, `doctors.flatMap { slotsToday(it) }` cho đúng kết quả của `doctors.map { slotsToday(it) }.flatten()`. Outcome là kiểu tự viết nên ta viết flatMap cho nó; map viết lại được bằng flatMap. Result không có flatMap, nhưng thêm được bằng fold: [[src:book-fp-tut]]''',
      '''flatten merges two box levels into one: List<List<A>> becomes List<A>, Outcome<E, Outcome<E, A>> becomes Outcome<E, A>. flatMap is just map then flatten, packed into one step. With a List, `doctors.flatMap { slotsToday(it) }` gives exactly the result of `doctors.map { slotsToday(it) }.flatten()`. Outcome is our own type, so we write flatMap for it; map can then be written with flatMap. Result has no flatMap, but fold can add one: [[src:book-fp-tut]]''')
    B(C, S_, 2, 'kt', '''fun <E, A, B> Outcome<E, A>.flatMap(f: (A) -> Outcome<E, B>): Outcome<E, B> = when (this) {
    is Ok -> f(value)
    is Err -> this
}
fun <E, A, B> Outcome<E, A>.map(f: (A) -> B): Outcome<E, B> = flatMap { Ok(f(it)) }

// không có trong thư viện chuẩn; site tự viết
fun <T, R> Result<T>.flatMap(f: (T) -> Result<R>): Result<R> =
    fold(onSuccess = { f(it) }, onFailure = { Result.failure(it) })''', '''fun <E, A, B> Outcome<E, A>.flatMap(f: (A) -> Outcome<E, B>): Outcome<E, B> = when (this) {
    is Ok -> f(value)
    is Err -> this
}
fun <E, A, B> Outcome<E, A>.map(f: (A) -> B): Outcome<E, B> = flatMap { Ok(f(it)) }

// not in the standard library; written by the site
fun <T, R> Result<T>.flatMap(f: (T) -> Result<R>): Result<R> =
    fold(onSuccess = { f(it) }, onFailure = { Result.failure(it) })''')
    B(C, S_, 3, 'p', '''Kiểu có flatMap cùng một cách bọc giá trị vào hộp (listOf, Ok, Result.success) và tuân theo ba luật thì gọi là monad: kiểu biết cách nối các bước mà bước nào cũng trả một hộp. Ba luật, viết bằng ví dụ: `Ok(x).flatMap(f) == f(x)`; `m.flatMap { Ok(it) } == m`; và `m.flatMap(f).flatMap(g) == m.flatMap { f(it).flatMap(g) }`. Không cần nhớ tên luật; chỉ cần biết flatMap của List, Outcome hay Flow (dòng giá trị bất đồng bộ của coroutine) cư xử như nhau. [[src:book-fp-manning]]''',
      '''A type with flatMap plus a way to wrap a value in the box (listOf, Ok, Result.success) that obeys three laws is called a monad: a type that knows how to chain steps that each return a box. The three laws, by example: `Ok(x).flatMap(f) == f(x)`; `m.flatMap { Ok(it) } == m`; and `m.flatMap(f).flatMap(g) == m.flatMap { f(it).flatMap(g) }`. You need not remember their names; just know that flatMap on List, Outcome or Flow (an asynchronous stream of values from coroutines) behaves the same way. [[src:book-fp-manning]]''')

    S_ = 'chain'
    a(C + '.sec.%s.title' % S_, '''Nối các bước không cần return''', '''Chaining steps without return''')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'p', '''Ở chương này, các hàm phụ của quy trình đặt lịch trả Outcome, thay vì null hay Boolean như ở chương "Lỗi là giá trị":''',
      '''In this chapter the booking helpers return Outcome, instead of null or a Boolean as in the chapter "Errors as values":''')
    B(C, S_, 2, 'kt', '''fun parsePhone(raw: String): Outcome<BookingError, Phone>
fun findFreeSlot(id: String): Outcome<BookingError, Slot>
fun ensureQuota(phone: Phone): Outcome<BookingError, Unit>''')
    B(C, S_, 3, 'p', '''Giờ book là một chuỗi flatMap: `parsePhone(raw).flatMap { p -> findFreeSlot(slotId).flatMap { s -> ensureQuota(p).map { save(p, s) } } }`. Không còn return, và bước nào trả Err thì các bước sau không chạy, đúng đường ray đã thấy. Cái giá: mỗi bước thêm một tầng lambda thụt vào. Khối either { … .bind() } của Arrow là cùng ý đó viết phẳng; còn bản trả về sớm (`?: return Err(...)`) vẫn là lựa chọn tốt khi không muốn thêm thư viện. [[src:arrow-typed-errors]]''',
      '''Now book is a chain of flatMap: `parsePhone(raw).flatMap { p -> findFreeSlot(slotId).flatMap { s -> ensureQuota(p).map { save(p, s) } } }`. No return left, and whichever step returns Err stops the later steps, the same railway you saw. The price: every step adds one more indented lambda. Arrow\'s either { … .bind() } block is the same idea written flat; and the early-return version (`?: return Err(...)`) is still a good choice when you do not want an extra library. [[src:arrow-typed-errors]]''')
    B(C, S_, 4, 'p', '''Cùng ý này có ở nhiều chỗ bạn đã gặp: List.flatMap, chuỗi ?.let, và flatMapConcat của Flow (chương "Xử lý flow: map, filter, scan, merge/zip/combine, flatMap, retry, distinct" của track Kotlin Coroutines Explorer). Nhận ra hình dạng "hàm trả hộp, nối bằng flatMap" là đủ để đọc chúng như nhau.''',
      '''The same idea shows up in places you have already met: List.flatMap, chains of ?.let, and Flow\'s flatMapConcat (the chapter "Flow processing: map, filter, scan, merge/zip/combine, flatMap, retry, distinct" of the Kotlin Coroutines Explorer track). Recognising the shape "a function returning a box, chained with flatMap" is enough to read them all the same way.''')

    S_ = 'bugs'
    a(C + '.sec.%s.title' % S_, '''Hai lỗi hay gặp''', '''Two common bugs''')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'bug', '''Màn xác nhận báo "Đã đặt lịch" dù người dùng đã hết lượt trong tuần.''', '''The confirmation screen says "Booked" even though the user has no bookings left this week.''')
    B(C, S_, 1, 'cause', '''Mã gọi phone.map { ensureQuota(it) }, nên kết quả là Ok(Err(QuotaExceeded)): lỗi nằm ở tầng trong. when chỉ xét tầng ngoài, thấy Ok và chọn nhánh thành công; Err bên trong không ai nhìn tới.''',
      '''The code calls phone.map { ensureQuota(it) }, so the result is Ok(Err(QuotaExceeded)): the error sits in the inner level. The when only checks the outer level, sees Ok and takes the success branch; nobody looks at the inner Err.''')
    B(C, S_, 1, 'fix', '''Dùng flatMap khi hàm truyền vào trả Outcome; khi đó lỗi luôn nằm ở tầng ngoài, nơi when xét tới.''', '''Use flatMap when the function passed in returns an Outcome; then the error is always in the outer level, where the when looks.''')
    B(C, S_, 2, 'bug', '''Màn "Giờ trống cả tuần" chỉ hiện 2 dòng, mỗi dòng là cả một danh sách giờ.''', '''The "Free slots this week" screen shows only 2 rows, each row a whole list of slots.''')
    B(C, S_, 2, 'cause', '''doctors.map { slotsOn(it, day) } cho List<List<Slot>>, và danh sách hiển thị coi mỗi list con là một dòng.''', '''doctors.map { slotsOn(it, day) } gives List<List<Slot>>, and the list display treats each inner list as one row.''')
    B(C, S_, 2, 'fix', '''Dùng doctors.flatMap { … } để có một List<Slot> phẳng, mỗi giờ một dòng.''', '''Use doctors.flatMap { … } to get one flat List<Slot>, one slot per row.''')

    S_ = 'ex'
    a(C + '.sec.%s.title' % S_, '''Bài tập''', '''Exercise''')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'ex', '''Tự viết lại flatMap và map cho Outcome mà không nhìn mục trên. Rồi viết lại hàm cancel trong bài tập của chương "Lỗi là giá trị" thành một chuỗi flatMap, với ba hàm phụ: `findBooking(id): Outcome<CancelError, Booking>`, `ensureNotCancelled(b): Outcome<CancelError, Booking>`, `ensureNotTooLate(b, now): Outcome<CancelError, Booking>`.''',
      '''Write flatMap and map for Outcome again without looking at the section above. Then rewrite the cancel function from the exercise in the chapter "Errors as values" as a chain of flatMap, with three helpers: `findBooking(id): Outcome<CancelError, Booking>`, `ensureNotCancelled(b): Outcome<CancelError, Booking>`, `ensureNotTooLate(b, now): Outcome<CancelError, Booking>`.''')
    B(C, S_, 1, 'hint', '''Ba bước kiểm trả Outcome nên nối bằng flatMap; bước cuối repo.markCancelled trả giá trị thường nên dùng map.''', '''The three checks return Outcome, so chain them with flatMap; the last step, repo.markCancelled, returns a plain value, so use map.''')
    B(C, S_, 1, 'sol', '''Mỗi bước ở đây chỉ cần giá trị của bước ngay trước, nên chuỗi viết thẳng hàng được, không phải lồng lambda. Lỗi đầu tiên dừng cả chuỗi, giống bản dùng return.''',
      '''Each step here only needs the value of the step just before, so the chain can be written in a straight line, with no nested lambdas. The first error stops the whole chain, as in the version with return.''')
    B(C, S_, 1, 'solkt', '''fun cancel(id: Long, now: LocalDateTime): Outcome<CancelError, Unit> =
    findBooking(id)
        .flatMap { ensureNotCancelled(it) }
        .flatMap { ensureNotTooLate(it, now) }
        .map { repo.markCancelled(it.id) }''')

    S_ = 'recall'
    a(C + '.sec.%s.title' % S_, '''Tự trả lời''', '''Answer it yourself''')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'ask', '''Khi nào dùng map, khi nào dùng flatMap?''', '''When do you use map, and when flatMap?''')
    B(C, S_, 1, 'ans', '''Hàm truyền vào trả giá trị thường thì dùng map; hàm trả cùng loại hộp (List, Outcome, Result…) thì dùng flatMap, để không ra hộp trong hộp.''',
      '''If the function passed in returns a plain value, use map; if it returns the same kind of box (List, Outcome, Result…), use flatMap so you do not get a box in a box.''')
    B(C, S_, 2, 'ask', '''Vì sao ?.let làm được cả map lẫn flatMap?''', '''Why can ?.let act as both map and flatMap?''')
    B(C, S_, 2, 'ans', '''Kotlin không có kiểu T?? riêng: null bên ngoài và null bên trong là một, nên kết quả không bao giờ lồng.''', '''Kotlin has no separate T?? type: the outer null and the inner null are one and the same, so the result never nests.''')

    for q, qv, qe, av, ae, wv, we in [
        ('q1', '`listOf(1, 2).map { listOf(it, it) }` cho gì?', 'What does `listOf(1, 2).map { listOf(it, it) }` give?', 'Một list lồng: [[1, 1], [2, 2]].', 'A nested list: [[1, 1], [2, 2]].', 'map đặt mỗi list con vào một ô.', 'map puts each inner list into one cell.'),
        ('q2', '`listOf(1, 2).flatMap { listOf(it, it) }` cho gì?', 'What does `listOf(1, 2).flatMap { listOf(it, it) }` give?', 'Một list phẳng: [1, 1, 2, 2].', 'A flat list: [1, 1, 2, 2].', 'flatMap = map rồi flatten.', 'flatMap = map, then flatten.'),
        ('q3', '`Ok(3).map { it }` bằng gì?', 'What does `Ok(3).map { it }` equal?', 'Ok(3).', 'Ok(3).', 'Luật đơn vị của functor: map với hàm đồng nhất không đổi gì.', 'The functor identity law: map with the identity function changes nothing.'),
        ('q4', '`Err(e).flatMap(f)` có gọi f không?', 'Does `Err(e).flatMap(f)` call f?', 'Không, nó trả lại Err(e).', 'No, it returns Err(e).', 'flatMap chỉ chạy hàm khi hộp là Ok.', 'flatMap only runs the function when the box is Ok.')]:
        a(C + '.quiz.%s.q' % q, qv, qe); a(C + '.quiz.%s.a' % q, av, ae); a(C + '.quiz.%s.why' % q, wv, we)
