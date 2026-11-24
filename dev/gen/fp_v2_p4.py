# Lập trình hàm · K4 (p4): kiểu dữ liệu đại số (Phần 1: nền tảng)
# Nguồn (chỉ ghi ở đây và docs/research/fp.md): Carli, FP in Kotlin by Tutorials ch.10 (Exercise 10.1, 10.3, callback an toàn kiểu);
# tài liệu Kotlin Sealed classes. Giọng văn dạy học (2026-11-24).

SEC_ORDER = {'p4': ['hook', 'count', 'unrep', 'kotlin', 'bugs', 'ex', 'recall']}


def add(a):
    def B(ch, sec, n, field, vi, en=None):
        a('%s.sec.%s.b.%02d.%s' % (ch, sec, n, field), vi, vi if en is None else en)

    a('preset.adt', 'Lập trình hàm · đếm trạng thái với kiểu đại số', 'Functional programming · counting states with algebraic types')
    m = lambda k, vi, en=None: a('m.adt.' + k, vi, en)
    m('title', 'UiState ba trường, hay sealed interface', 'A three-field UiState, or a sealed interface')
    m('overview', 'Màn "Lịch trống" của app Hẹn Khám vào là tải danh sách giờ trống, rồi hiện lỗi hoặc danh sách. Ta mô tả trạng thái màn hình theo hai cách. Cách 1: một data class có ba trường độc lập (isLoading, error, slots). Cách 2: một sealed interface với ba kiểu con. Với mỗi cách, ta đếm xem nó cho phép bao nhiêu trạng thái, cái nào có nghĩa, rồi thử một lỗi thật và một yêu cầu mới.',
      'The ClinicBook "Free slots" screen loads the free slots on entry, then shows an error or the list. We describe the screen state two ways. Way 1: a data class with three independent fields (isLoading, error, slots). Way 2: a sealed interface with three subtypes. For each, we count how many states it allows and which make sense, then try a real bug and a new requirement.')
    m('wrapup', 'Data class ba trường cho phép 2 × 2 × 2 = 8 trạng thái, nhưng màn chỉ cần 3. Năm trạng thái thừa không ai muốn, vậy mà mã vẫn tạo ra được: quên tắt isLoading là màn quay mãi, để mặc định là crash. Sealed interface chỉ có 1 + 1 + 1 = 3 trạng thái, đúng bằng thiết kế. Khi thêm trạng thái mới, trình biên dịch chỉ ra mọi chỗ cần sửa thay vì để màn hình sai trong im lặng.',
      'The three-field data class allows 2 × 2 × 2 = 8 states, but the screen needs 3. Five extra states nobody wants, yet code can still produce them: forget to clear isLoading and the screen spins forever; leave the defaults and it crashes. The sealed interface has just 1 + 1 + 1 = 3 states, exactly the design. When a new state is added, the compiler points at every place to fix instead of letting screens go wrong silently.')
    m('simp.1', 'Ở đây ta đếm theo "dạng": trường có thể null chỉ tính là có hoặc không, không đếm mọi chuỗi hay danh sách có thể có.',
      'Here we count "shapes": a nullable field counts only as present or absent; every possible string or list is not counted.')
    m('simp.2', 'Thiết kế màn và ba màn dùng chung trạng thái là ví dụ; màn khác có thể cần thêm trạng thái như "chờ" hay "rỗng".',
      'The screen design and the three screens sharing the state are examples; other screens may need extra states such as "idle" or "empty".')
    m('ctl.hint', 'Chọn cách khai báo rồi bấm qua từng bước; so bảng đếm ở trên và bảng trạng thái ở dưới.', 'Pick a declaration and step through; compare the count table above with the state table below.')
    m('ctl.case', 'Cách khai báo UiState', 'UiState declared as')
    m('ctl.case.product', 'data class ba trường', 'a three-field data class'); m('ctl.case.sum', 'sealed interface', 'a sealed interface')
    m('diagramTitle', 'Kiểu, các trạng thái nó cho phép, màn hình', 'The type, the states it allows, the screens')
    m('diagramDesc', 'Kiểu quyết định trạng thái nào tồn tại; màn hình hiện từng trạng thái', 'The type decides which states exist; the screens show each one')
    for k, vi, en in [('type', 'Kiểu UiState', 'The UiState type'), ('states', 'Các trạng thái có thể có', 'Possible states'), ('screen', 'Ba màn dùng trạng thái', 'Three screens using it'), ('catch', 'Khối catch', 'The catch block')]:
        m('n.' + k, vi, en)
    m('met.combos', 'Số trạng thái kiểu cho phép', 'States the type allows'); m('met.invalid', 'Trạng thái vô nghĩa', 'Meaningless states')
    m('met.silent', 'Màn hiện sai mà không ai báo', 'Screens wrong with no warning'); m('met.flagged', 'Chỗ trình biên dịch chỉ ra', 'Places the compiler points to')
    a('cap.adt', 'Kiểu quyết định những trạng thái nào có thể tồn tại; khối catch ghi vào trạng thái; màn hình hiện từng trạng thái. Ô đỏ: trạng thái vô nghĩa lọt vào, hoặc màn hiện sai.',
      'The type decides which states can exist; the catch block writes the state; the screens show each state. A red box: a meaningless state slipped in, or a screen shows the wrong thing.')
    S = [
        ('product', 's1', 'Đếm: 2 × 2 × 2 = 8', 'Counting: 2 × 2 × 2 = 8',
         'Data class có ba trường độc lập: isLoading (đúng hoặc sai), error (có hoặc không), slots (có hoặc không). Mỗi trường chọn riêng, nên số trạng thái nhân lên: 2 × 2 × 2 = 8. Giống chọn áo, quần, giày: 2 áo, 2 quần, 2 đôi giày là 8 bộ đồ.',
         'The data class has three independent fields: isLoading (true or false), error (present or absent), slots (present or absent). Each is chosen on its own, so the states multiply: 2 × 2 × 2 = 8. Like picking a shirt, trousers and shoes: 2 of each make 8 outfits.'),
        ('product', 's2', 'Chỉ 3 trong 8 có nghĩa', 'Only 3 of 8 make sense',
         'Màn này vào là tải ngay, rồi ra lỗi hoặc danh sách. Chỉ 3 trạng thái có nghĩa: đang tải; có lỗi; có danh sách. 5 trạng thái còn lại vẫn tạo được: "không tải, không lỗi, không dữ liệu" làm slots!! crash; "đang tải mà có lỗi" thì lỗi bị che sau vòng quay.',
         'This screen loads on entry, then ends in an error or the list. Only 3 states make sense: loading; error; list. The other 5 can still be created: "not loading, no error, no data" makes slots!! crash; "loading with an error" hides the error behind the spinner.'),
        ('product', 's3', 'Khối catch quên tắt isLoading', 'The catch block forgets isLoading',
         'Mất mạng khi đang tải: khối catch gán error nhưng quên đặt isLoading = false. Trạng thái thành "đang tải mà có lỗi", một tổ hợp vô nghĩa mà kiểu vẫn cho phép. Màn hình xét isLoading trước, nên chỉ quay mãi; người dùng không bao giờ thấy lỗi.',
         'The network drops while loading: the catch block sets error but forgets isLoading = false. The state becomes "loading with an error", a meaningless combination the type still allows. The screen checks isLoading first, so it just spins forever; the user never sees the error.'),
        ('product', 's4', 'Thêm "tải lại, giữ dữ liệu cũ": trình biên dịch im lặng', 'Adding "refresh, keep old data": the compiler stays silent',
         'Thiết kế mới muốn tải lại mà vẫn hiện danh sách cũ. Tổ hợp "đang tải và có danh sách" vốn đã tồn tại, nên không có dòng nào báo lỗi. Cả 3 màn vẫn xét isLoading trước và giấu dữ liệu sau vòng quay. Lỗi chỉ lộ khi có người nhìn màn hình.',
         'The new design wants to refresh while still showing the old list. The combination "loading and has a list" already existed, so nothing reports an error. All 3 screens still check isLoading first and hide the data behind the spinner. The bug only shows when someone looks at the screen.'),
        ('sum', 's1', 'Đếm: 1 + 1 + 1 = 3', 'Counting: 1 + 1 + 1 = 3',
         'Sealed interface có ba kiểu con: Loading, Error(message), Success(slots). Mỗi lúc, trạng thái là đúng một trong ba, nên số trạng thái cộng lại: 1 + 1 + 1 = 3. Giống thực đơn chọn một món: phở, cơm hoặc bún, không thể vừa phở vừa cơm.',
         'The sealed interface has three subtypes: Loading, Error(message), Success(slots). At any moment the state is exactly one of them, so the states add up: 1 + 1 + 1 = 3. Like a set menu where you pick one dish: noodles, rice or soup, never two at once.'),
        ('sum', 's2', 'Trạng thái nào cũng có nghĩa', 'Every state makes sense',
         'Ba kiểu con khớp đúng ba trạng thái của thiết kế. Không có cách nào viết ra "vừa quay vừa lỗi" hay "không có gì". Khi hiện màn hình, when chỉ cần ba nhánh và không cần else.',
         'The three subtypes match the design\'s three states exactly. There is no way to write "spinning with an error" or "nothing at all". When drawing the screen, when needs just three branches and no else.'),
        ('sum', 's3', 'Khối catch chỉ có thể tạo Error', 'The catch block can only produce Error',
         'Khối catch viết _state.value = Error(message). Không có trường isLoading nào để quên. Màn hình hiện thông báo lỗi.',
         'The catch block writes _state.value = Error(message). There is no isLoading field to forget. The screen shows the error message.'),
        ('sum', 's4', 'Thêm Refreshing: trình biên dịch chỉ ra 3 chỗ', 'Adding Refreshing: the compiler points to 3 places',
         'Thêm kiểu con Refreshing(slots). Ba chỗ when trên trạng thái không còn đủ nhánh nên không biên dịch được, cho tới khi mỗi chỗ xử lý trạng thái mới. Mỗi màn buộc phải quyết định rõ: hiện dữ liệu cũ kèm dấu tải lại thế nào.',
         'Add a Refreshing(slots) subtype. The three when expressions on the state are no longer complete and stop compiling until each one handles the new state. Every screen must decide explicitly how to show the old data with a refresh indicator.'),
    ]
    for case, k, tv, te, xv, xe in S:
        sid = case + '.' + k
        m('s.%s.title' % sid, tv, te); m('s.%s.explain' % sid, xv, xe); m('ev.' + sid, tv, te)
    for k, vi, en in [
        ('try', 'Mẹo đọc: bảng trên đếm số trạng thái; bảng dưới cho biết trạng thái nào có nghĩa và màn hình hiện gì.', 'Reading tip: the top table counts the states; the bottom table shows which states make sense and what the screen shows.'),
        ('product.s2', 'Quy tắc đếm: kiểu "có cả A và B" (data class, Pair) có số giá trị bằng A nhân B. Kiểu có thể null thì cộng thêm đúng một giá trị: null. [[src:book-fp-tut]]',
         'The counting rule: a type that "has both A and B" (a data class, a Pair) has A times B values. A nullable type adds exactly one more value: null. [[src:book-fp-tut]]'),
        ('product.s3', 'Kiểu cho phép điều gì thì sớm muộn sẽ có dòng mã tạo ra điều đó. Muốn tránh trạng thái sai, cách chắc nhất là làm cho nó không viết ra được.',
         'Whatever the type allows, some line of code will eventually produce. The surest way to avoid a wrong state is to make it impossible to write.'),
        ('product.s4', 'Thêm một trạng thái vào data class không làm kiểu thay đổi, nên không có chỗ nào bị buộc phải xem lại.',
         'Adding a state to a data class does not change the type, so nothing is forced to be reviewed.'),
        ('sum.s1', 'Quy tắc đếm: kiểu "là A hoặc B" (sealed interface, Either) có số giá trị bằng A cộng B. [[src:book-fp-tut]]',
         'The counting rule: a type that "is A or B" (a sealed interface, an Either) has A plus B values. [[src:book-fp-tut]]'),
        ('sum.s2', 'Điều quan trọng không chỉ là kiểu cho bạn làm gì, mà còn là nó không cho bạn làm gì. Trạng thái vô nghĩa không viết ra được thì không thể lọt vào app. [[src:book-fp-tut]]',
         'What matters is not only what the type lets you do, but what it stops you doing. A meaningless state that cannot be written cannot reach the app. [[src:book-fp-tut]]'),
        ('sum.s3', 'Gán cả trạng thái bằng một kiểu con, thay vì sửa từng trường bằng copy: một lần gán, một trạng thái, không trường nào bị bỏ quên.',
         'Set the whole state to one subtype instead of patching fields with copy: one assignment, one state, no field forgotten.'),
        ('sum.s4', 'Kotlin biết hết các kiểu con của một sealed interface ngay lúc biên dịch, nên kiểm được when đã đủ nhánh chưa. Viết else là tự tắt lời nhắc này (track Kotlin, chương K5). [[src:kt-sealed]]',
         'Kotlin knows every subtype of a sealed interface at compile time, so it can check whether a when covers them all. Writing else switches this reminder off (Kotlin track, chapter K5). [[src:kt-sealed]]'),
    ]:
        m('co.' + k, vi, en)

    z = lambda k, vi, en=None: a('vz.' + k, vi, en)
    z('tab.adt', 'Đếm trạng thái và bảng trạng thái', 'Counting states and the state table')
    z('adt.ccap.product', 'Data class: số khả năng của các trường nhân với nhau. Trường có thể null tính hai khả năng: có hoặc không.', 'Data class: the fields\' possibilities multiply. A nullable field counts as two: present or absent.')
    z('adt.ccap.sum', 'Sealed interface: số khả năng của các kiểu con cộng với nhau. Mỗi kiểu con ở đây tính là một.', 'Sealed interface: the subtypes\' possibilities add up. Each subtype here counts as one.')
    for k, vi, en in [('part', 'Thành phần', 'Part'), ('type', 'Kiểu', 'Type'), ('count', 'Số khả năng', 'Possibilities'), ('combo', 'Ba trường (isLoading, error, slots)', 'The three fields (isLoading, error, slots)'),
                      ('variant', 'Kiểu con', 'Subtype'), ('mean', 'Có nghĩa?', 'Meaningful?'), ('ui', 'Màn hình hiện', 'The screen shows')]:
        z('adt.col.' + k, vi, en)
    z('adt.total', 'Tổng: {expr}', 'Total: {expr}')
    z('adt.mcap.product', 'Mọi tổ hợp của ba trường. Thiết kế của màn: vào là tải ngay, kết quả là lỗi hoặc danh sách; bước 4 thêm "tải lại, giữ dữ liệu cũ".', 'Every combination of the three fields. The screen\'s design: load on entry, ending in an error or the list; step 4 adds "refresh, keep old data".')
    z('adt.mcap.sum', 'Mọi kiểu con của sealed interface: chỉ những trạng thái thiết kế cần.', 'Every subtype of the sealed interface: only the states the design needs.')
    for k, vi, en in [('loading', 'đang tải', 'loading'), ('error', 'lỗi', 'error'), ('success', 'danh sách', 'list'), ('refresh', 'tải lại, giữ dữ liệu cũ', 'refreshing, keeping old data'), ('none', 'vô nghĩa', 'meaningless')]:
        z('adt.mean.' + k, vi, en)
    for k, vi, en in [('spinner', 'vòng quay', 'spinner'), ('error', 'thông báo lỗi', 'error message'), ('list', 'danh sách giờ trống', 'the slot list'), ('listRefreshing', 'danh sách kèm dấu tải lại', 'the list with a refresh indicator'), ('crash', 'crash: slots!! là null', 'crash: slots!! is null')]:
        z('adt.ui.' + k, vi, en)
    z('adt.sub.none', 'Bước 3 và 4 sẽ thêm một lỗi thật và một trạng thái mới.', 'Steps 3 and 4 add a real bug and a new state.')
    z('adt.sub.bug.product', 'Bước 3: khối catch gán error nhưng quên isLoading = false, tạo ra "đang tải mà có lỗi": màn chỉ hiện vòng quay, lỗi bị che.', 'Step 3: the catch block sets error but forgets isLoading = false, creating "loading with an error": the screen shows only the spinner, the error is hidden.')
    z('adt.sub.bug.sum', 'Bước 3: khối catch chỉ có thể tạo Error(message); không có trường nào để quên.', 'Step 3: the catch block can only produce Error(message); there is no field to forget.')
    z('adt.sub.v2.product', 'Bước 4: tổ hợp "tải lại" vốn đã tồn tại nên trình biên dịch không nói gì; {n} màn vẫn hiện vòng quay và giấu dữ liệu.', 'Step 4: the "refresh" combination already existed, so the compiler says nothing; {n} screens still show the spinner and hide the data.')
    z('adt.sub.v2.sum', 'Bước 4: thêm Refreshing làm {n} chỗ when thiếu nhánh; trình biên dịch báo lỗi cho tới khi mỗi chỗ xử lý trạng thái mới.', 'Step 4: adding Refreshing leaves {n} when expressions missing a branch; the compiler reports errors until each one handles the new state.')
    z('adt.legend', 'Đỏ gạch: tổ hợp vô nghĩa, hoặc màn hiện sai. Đậm: trạng thái thiết kế cần. Viền: tổ hợp hay kiểu con của bước này. "?": chưa tới bước đó.', 'Red hatched: a meaningless combination, or a screen showing the wrong thing. Bold: a state the design needs. Outlined: this step\'s combination or subtype. "?": that step has not come yet.')

    C = 'p4'
    a(C + '.title', 'Kiểu dữ liệu đại số', 'Algebraic data types')
    a(C + '.essence', 'Mỗi kiểu dữ liệu cho phép một số trạng thái nhất định, và ta đếm được. Kiểu "có cả A và B" (data class) thì nhân: A × B. Kiểu "là A hoặc B" (sealed interface) thì cộng: A + B. Kiểu có thể null là A + 1.\nUiState ba trường độc lập cho phép 8 trạng thái, trong khi màn thường chỉ cần 3. Năm trạng thái thừa là năm cách để mã đặt sai.\nQuy tắc dễ nhớ: mô tả thiết kế mà có chữ "hoặc" thì dùng sealed interface. Khi đó trạng thái vô nghĩa không viết ra được, và thêm trạng thái mới thì trình biên dịch chỉ ra mọi chỗ cần sửa.',
      'Every data type allows a certain number of states, and we can count them. A type that "has both A and B" (a data class) multiplies: A × B. A type that "is A or B" (a sealed interface) adds: A + B. A nullable type is A + 1.\nA UiState with three independent fields allows 8 states, while the screen usually needs 3. The five extra states are five ways for code to set things wrong.\nAn easy rule: if the design\'s description says "or", use a sealed interface. Then meaningless states cannot be written, and a new state makes the compiler point at every place to change.')
    a(C + '.goal.g1', 'Đã đếm số trạng thái và trạng thái vô nghĩa', 'Counted the states and the meaningless ones')
    a(C + '.goal.g2', 'Đã thấy trạng thái mới được xử lý thế nào', 'Saw how the new state is handled')
    a(C + '.sim.fp.adt', 'data class ba trường hay sealed interface', 'a three-field data class or a sealed interface')

    S_ = 'hook'
    a(C + '.sec.%s.title' % S_, 'Đoán trước khi đọc', 'Predict before reading')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'predict', 'UiState(isLoading: Boolean, error: String?, slots: List<Slot>?) cho phép bao nhiêu trạng thái, nếu mỗi trường có thể null chỉ tính là "có" hoặc "không"? Màn "Lịch trống" thật sự cần bao nhiêu trong số đó?',
      'How many states does UiState(isLoading: Boolean, error: String?, slots: List<Slot>?) allow, counting each nullable field only as "present" or "absent"? How many of them does the "Free slots" screen really need?')
    B(C, S_, 1, 'ans', '8 trạng thái (2 × 2 × 2). Màn chỉ cần 3: đang tải, lỗi, danh sách. 5 trạng thái còn lại vô nghĩa nhưng kiểu vẫn cho phép, và mỗi cái là một cách để mã đặt sai trạng thái.',
      '8 states (2 × 2 × 2). The screen needs only 3: loading, error, list. The other 5 are meaningless but the type still allows them, and each one is a way for code to set the wrong state.')

    S_ = 'count'
    a(C + '.sec.%s.title' % S_, 'Đếm trạng thái: "và" thì nhân, "hoặc" thì cộng', 'Counting states: "and" multiplies, "or" adds')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'p', 'Hãy coi mỗi kiểu là một túi các giá trị có thể có. Boolean có 2 giá trị. Một enum ba màu (đỏ, vàng, xanh) có 3. Khi một kiểu chứa cả Boolean và màu cùng lúc, như data class hay Pair, mỗi Boolean ghép được với mỗi màu: 2 × 3 = 6 giá trị. Vì số lượng nhân lên, người ta gọi đó là product type (kiểu tích). [[src:book-fp-tut]]',
      'Think of each type as a bag of possible values. Boolean has 2 values. A three-colour enum (red, yellow, green) has 3. When a type holds a Boolean and a colour together, like a data class or a Pair, every Boolean pairs with every colour: 2 × 3 = 6 values. Because the counts multiply, this is called a product type. [[src:book-fp-tut]]')
    B(C, S_, 2, 'p', 'Ngược lại, kiểu "là Boolean hoặc là màu" (một sealed interface có hai kiểu con) chỉ chứa một trong hai mỗi lúc: 2 + 3 = 5 giá trị. Số lượng cộng lại, nên gọi là sum type (kiểu tổng). Kiểu có thể null là trường hợp quen thuộc của phép cộng: mọi giá trị của A, cộng thêm đúng một giá trị null, tức A + 1. [[src:book-fp-tut]]',
      'By contrast, a type that "is a Boolean or a colour" (a sealed interface with two subtypes) holds just one of them at a time: 2 + 3 = 5 values. The counts add, so it is called a sum type. A nullable type is a familiar case of addition: every value of A plus exactly one more, null, which is A + 1. [[src:book-fp-tut]]')
    B(C, S_, 3, 'kt', '// "và": nhân\ndata class Filter(val onlyToday: Boolean, val sort: Sort)   // 2 × 3 = 6 (Sort có 3 giá trị)\n\n// "hoặc": cộng\nsealed interface Payment {                                   // 1 + 1 + 3 = 5\n    data object Cash : Payment\n    data object Insurance : Payment\n    data class Card(val brand: Brand) : Payment              // Brand có 3 giá trị\n}\n\n// có thể null: A + 1\nval brand: Brand? = null                                     // 3 + 1 = 4',
      '// "and": multiply\ndata class Filter(val onlyToday: Boolean, val sort: Sort)   // 2 × 3 = 6 (Sort has 3 values)\n\n// "or": add\nsealed interface Payment {                                   // 1 + 1 + 3 = 5\n    data object Cash : Payment\n    data object Insurance : Payment\n    data class Card(val brand: Brand) : Payment              // Brand has 3 values\n}\n\n// nullable: A + 1\nval brand: Brand? = null                                     // 3 + 1 = 4')
    B(C, S_, 4, 'p', 'Hai loại này gộp lại gọi là kiểu dữ liệu đại số, vì chúng cộng và nhân như đại số ở trường. Nhớ một câu là đủ: "và" thì nhân, "hoặc" thì cộng.',
      'Together these are called algebraic data types, because they add and multiply like school algebra. One sentence is enough to remember: "and" multiplies, "or" adds.')

    S_ = 'unrep'
    a(C + '.sec.%s.title' % S_, 'Làm cho trạng thái vô nghĩa không viết ra được', 'Making meaningless states impossible to write')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'p', 'Cách làm có ba bước. Một: viết bằng lời các trạng thái mà thiết kế cần, ví dụ "đang tải, hoặc có lỗi kèm thông báo, hoặc có danh sách". Hai: chỗ nào có chữ "hoặc" thì dùng sealed interface; chỗ nào có chữ "và" thì dùng data class. Ba: đếm lại để chắc số trạng thái của kiểu khớp với thiết kế. [[src:book-fp-tut]]',
      'There are three steps. One: write down in words the states the design needs, such as "loading, or an error with a message, or a list". Two: wherever it says "or", use a sealed interface; wherever it says "and", use a data class. Three: count again to make sure the type\'s states match the design. [[src:book-fp-tut]]')
    B(C, S_, 2, 'p', 'Data class vẫn là lựa chọn đúng khi các trường thật sự độc lập. Một bộ lọc gồm "chỉ hôm nay" và "cách sắp xếp" thì tổ hợp nào cũng có nghĩa. Câu hỏi cần đặt không phải "data class hay sealed", mà là "mọi tổ hợp có nghĩa không".',
      'A data class is still the right choice when the fields are truly independent. A filter with "today only" and "sort order" makes sense in every combination. The question to ask is not "data class or sealed" but "does every combination make sense".')
    B(C, S_, 3, 'note', 'Màn khác có thể cần thêm trạng thái: chờ trước khi tải, tải lại nhưng giữ dữ liệu cũ, danh sách rỗng. Đó là quyết định của thiết kế. Sealed interface buộc bạn ghi rõ nó thành một kiểu con có tên, thay vì để nó lẩn trong một tổ hợp trường.',
      'Other screens may need extra states: idle before loading, refreshing while keeping old data, an empty list. That is a design decision. A sealed interface makes you write it down as a named subtype, instead of letting it hide in a combination of fields.')
    B(C, S_, 3, 'kind', 'mechanism')

    S_ = 'kotlin'
    a(C + '.sec.%s.title' % S_, 'Trong Kotlin: sealed interface và when đủ nhánh', 'In Kotlin: sealed interfaces and a complete when')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'p', 'Khai báo một sealed interface (hoặc sealed class) với các kiểu con data object và data class. Vì Kotlin biết hết các kiểu con ngay lúc biên dịch, nó kiểm được when trên kiểu đó đã đủ nhánh chưa, không cần else. Track Kotlin chương K5 nói kỹ phần cú pháp; track Kiến trúc chương G7 dùng một UiState duy nhất cho mô hình MVI. [[src:kt-sealed]]',
      'Declare a sealed interface (or sealed class) with data object and data class subtypes. Because Kotlin knows every subtype at compile time, it can check whether a when on that type covers them all, with no else needed. The Kotlin track\'s chapter K5 covers the syntax in detail; the Architecture track\'s chapter G7 uses a single UiState for MVI. [[src:kt-sealed]]')
    B(C, S_, 2, 'kt', '_state.value = SlotsUiState.Loading\n_state.value = try {\n    SlotsUiState.Success(repo.slots())\n} catch (e: IOException) {\n    SlotsUiState.Error(e.message ?: "")\n}',
      '_state.value = SlotsUiState.Loading\n_state.value = try {\n    SlotsUiState.Success(repo.slots())\n} catch (e: IOException) {\n    SlotsUiState.Error(e.message ?: "")\n}')
    B(C, S_, 3, 'p', 'Để ý: mỗi lần đổi trạng thái là một phép gán trả về đúng một kiểu con. Không còn những dòng copy(isLoading = …) rải rác mà chỗ nào cũng phải nhớ tắt cờ.',
      'Notice: each state change is one assignment returning exactly one subtype. No more scattered copy(isLoading = …) lines where every place must remember to clear the flag.')

    S_ = 'bugs'
    a(C + '.sec.%s.title' % S_, 'Hai lỗi hay gặp', 'Two common bugs')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'bug', 'Mất mạng khi đang tải: màn quay mãi, không bao giờ hiện lỗi.', 'The network drops while loading: the screen spins forever and never shows the error.')
    B(C, S_, 1, 'cause', 'Khối catch gán error nhưng quên isLoading = false. Tổ hợp "đang tải mà có lỗi" vẫn hợp lệ với kiểu, và màn hình xét isLoading trước.', 'The catch block sets error but forgets isLoading = false. The combination "loading with an error" is valid for the type, and the screen checks isLoading first.')
    B(C, S_, 1, 'fix', 'Đổi UiState thành sealed interface; khối catch gán Error(message).', 'Turn UiState into a sealed interface; the catch block assigns Error(message).')
    B(C, S_, 2, 'bug', 'Crash NullPointerException ở slots!! ngay khi mở màn.', 'A NullPointerException at slots!! right as the screen opens.')
    B(C, S_, 2, 'cause', 'Trạng thái mặc định là "không tải, không lỗi, không dữ liệu", và màn hình rơi vào nhánh hiện danh sách.', 'The default state is "not loading, no error, no data", and the screen falls through to the list branch.')
    B(C, S_, 2, 'fix', 'Sealed interface không có trạng thái "không gì cả"; trạng thái ban đầu là Loading. Nếu thiết kế cần trạng thái chờ, thêm một kiểu con có tên như Idle.', 'The sealed interface has no "nothing at all" state; the initial state is Loading. If the design needs a waiting state, add a named subtype such as Idle.')

    S_ = 'ex'
    a(C + '.sec.%s.title' % S_, 'Bài tập', 'Exercise')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'ex', 'Đếm số trạng thái của ba kiểu dưới đây, rồi viết lại kiểu callback sao cho không còn trạng thái vô nghĩa.',
      'Count the states of the three types below, then rewrite the callback type so no meaningless state remains.')
    B(C, S_, 1, 'exkt', 'enum class Triage { RED, YELLOW, GREEN }\ndata class Visit(val urgent: Boolean, val triage: Triage)\nsealed interface Slot { data object Closed : Slot; data class Open(val triage: Triage) : Slot }\ntypealias OnBooked = (Booking?, Throwable?) -> Unit')
    B(C, S_, 1, 'hint', 'data class thì nhân, sealed thì cộng; mỗi tham số có thể null của callback tính là "có" hoặc "không".', 'A data class multiplies, a sealed type adds; each nullable callback parameter counts as "present" or "absent".')
    B(C, S_, 1, 'sol', 'Visit = 2 × 3 = 6. Slot = 1 + 3 = 4. OnBooked: (có hoặc không) × (có hoặc không) = 4, trong đó "không cả hai" và "có cả hai" đều vô nghĩa. Viết lại bằng "hoặc": callback nhận BookResult là Booked(booking) hoặc Failed(error), chỉ 1 + 1 = 2 trạng thái, cả hai đều có nghĩa.',
      'Visit = 2 × 3 = 6. Slot = 1 + 3 = 4. OnBooked: (present or absent) × (present or absent) = 4, where "neither" and "both" are meaningless. Rewrite it with "or": the callback takes a BookResult that is Booked(booking) or Failed(error), just 1 + 1 = 2 states, both meaningful.')
    B(C, S_, 1, 'solkt', 'sealed interface BookResult {\n    data class Booked(val booking: Booking) : BookResult\n    data class Failed(val error: Throwable) : BookResult\n}\ntypealias OnBooked = (BookResult) -> Unit')

    S_ = 'recall'
    a(C + '.sec.%s.title' % S_, 'Tự trả lời', 'Answer it yourself')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'ask', 'Trước khi viết một UiState, bạn tự hỏi câu gì để chọn giữa data class và sealed interface?', 'Before writing a UiState, what do you ask yourself to choose between a data class and a sealed interface?')
    B(C, S_, 1, 'ans', 'Mọi tổ hợp của các trường có nghĩa không? Nếu có, data class là đúng. Nếu thiết kế nói "cái này hoặc cái kia", dùng sealed interface để trạng thái vô nghĩa không viết ra được.', 'Does every combination of the fields make sense? If so, a data class is right. If the design says "this or that", use a sealed interface so meaningless states cannot be written.')

    for q, qv, qe, av, ae, wv, we in [
        ('q1', 'Một data class gồm một Boolean và một enum 3 giá trị có bao nhiêu giá trị?', 'How many values does a data class of a Boolean and a 3-value enum have?', 'Sáu (2 × 3).', 'Six (2 × 3).', '"Và" thì nhân.', '"And" multiplies.'),
        ('q2', 'Sealed interface có Loading, Error(msg), Success(list): bao nhiêu trạng thái?', 'A sealed interface with Loading, Error(msg), Success(list): how many states?', 'Ba (1 + 1 + 1).', 'Three (1 + 1 + 1).', '"Hoặc" thì cộng.', '"Or" adds.'),
        ('q3', 'Triage? (enum 3 giá trị, có thể null) có bao nhiêu giá trị?', 'How many values does Triage? (a 3-value enum, nullable) have?', 'Bốn.', 'Four.', 'A + 1: thêm đúng một giá trị null.', 'A + 1: exactly one extra value, null.'),
        ('q4', 'Vì sao nên tránh else trong when trên một sealed interface?', 'Why avoid else in a when on a sealed interface?', 'Để khi thêm kiểu con, trình biên dịch chỉ ra mọi chỗ chưa xử lý.', 'So that adding a subtype makes the compiler point at every unhandled place.', 'else nuốt mất kiểu con mới mà không báo gì.', 'else silently swallows the new subtype.')]:
        a(C + '.quiz.%s.q' % q, qv, qe); a(C + '.quiz.%s.a' % q, av, ae); a(C + '.quiz.%s.why' % q, wv, we)
