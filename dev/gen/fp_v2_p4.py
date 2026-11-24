# Lập trình hàm · K4 (p4): kiểu dữ liệu đại số (Phần 1: nền tảng)
# Nguồn: Massimo Carli, FP in Kotlin by Tutorials ch.10 (Data types and multiplication: Pair, Triage, Struct; Unit là 1, Nothing là 0;
# Data types and addition: Either; Putting algebra to work: callback không an toàn kiểu, Result * (Info + Error); Algebra with the Optional
# type: A + 1; Exercise 10.1, 10.3); tài liệu Kotlin Sealed classes (when phủ đủ). Đọc 2026-11-24, diễn đạt lại; ví dụ theo app Hẹn Khám.

SEC_ORDER = {'p4': ['hook', 'count', 'unrep', 'kotlin', 'bugs', 'ex', 'recall', 'honest']}


def add(a):
    def B(ch, sec, n, field, vi, en=None):
        a('%s.sec.%s.b.%02d.%s' % (ch, sec, n, field), vi, vi if en is None else en)

    a('preset.adt', 'Lập trình hàm · đếm trạng thái với kiểu đại số', 'Functional programming · counting states with algebraic types')
    m = lambda k, vi, en=None: a('m.adt.' + k, vi, en)
    m('title', 'UiState ba trường, hay sealed interface', 'A three-field UiState, or a sealed interface')
    m('overview', 'Màn "Lịch trống" của app Hẹn Khám: vào là tải danh sách giờ trống, rồi hiện lỗi hoặc danh sách. Cách thứ nhất: UiState là data class ba trường độc lập (isLoading, error, slots). Cách thứ hai: sealed interface với ba kiểu con. Đếm số dạng của mỗi kiểu, đánh dấu dạng có nghĩa, cho khối catch quên một trường, rồi thêm trạng thái "tải lại giữ dữ liệu cũ".',
      'The ClinicBook "Free slots" screen: on entry it loads the free slots, then shows an error or the list. First version: UiState is a data class with three independent fields (isLoading, error, slots). Second: a sealed interface with three subtypes. Count each type\'s shapes, mark the meaningful ones, let a catch block forget a field, then add a "refresh while keeping old data" state.')
    m('wrapup', 'data class ba trường có 2 × 2 × 2 = 8 dạng, chỉ 3 có nghĩa. Khối catch quên tắt isLoading tạo ra (true, lỗi, null) và màn quay mãi; trạng thái mặc định (false, null, null) làm slots!! crash; thêm tải lại thì 3 màn hiện sai mà trình biên dịch không nói gì. sealed interface có 1 + 1 + 1 = 3 dạng, đúng bằng thiết kế; khối catch chỉ tạo được Error; thêm Refreshing thì 3 chỗ when bị trình biên dịch chỉ ra cho tới khi xử lý.',
      'The three-field data class has 2 × 2 × 2 = 8 shapes, only 3 meaningful. A catch block forgetting isLoading produces (true, error, null) and the screen spins forever; the default (false, null, null) makes slots!! crash; adding refresh makes 3 screens wrong with no word from the compiler. The sealed interface has 1 + 1 + 1 = 3 shapes, exactly the design; the catch block can only produce Error; adding Refreshing makes the compiler point at 3 when expressions until they handle it.')
    m('simp.1', 'Site đếm theo dạng: trường nullable tính hai dạng (có, không), mỗi kiểu con tính một dạng; không đếm mọi chuỗi hay danh sách có thể có. Thiết kế màn và ba màn dùng chung state là của site.',
      'The site counts shapes: a nullable field counts as two (present, absent), each subtype as one; every possible string or list is not counted. The screen design and the three screens sharing the state are the site\'s.')
    m('simp.2', 'Phép đếm theo Carli ch.10 (product nhân, sum cộng, Unit là 1, Nothing là 0, Optional là A + 1). Thiết kế khác có thể cần thêm trạng thái như chờ hay rỗng; khi đó thêm một kiểu con có tên.',
      'The counting follows Carli ch.10 (products multiply, sums add, Unit is 1, Nothing is 0, Optional is A + 1). Other designs may need more states, such as idle or empty; then add a named subtype.')
    m('ctl.hint', 'Đổi cách khai báo rồi đi lại; so bảng tính số dạng và ma trận ở dưới.', 'Switch the declaration and walk again; compare the shape count and the matrix below.')
    m('ctl.case', 'Cách khai báo UiState', 'UiState declared as')
    m('ctl.case.product', 'data class ba trường (product)', 'a three-field data class (product)'); m('ctl.case.sum', 'sealed interface (sum)', 'a sealed interface (sum)')
    m('diagramTitle', 'Kiểu, các trạng thái biểu diễn được, màn hình', 'The type, its representable states, the screens')
    m('diagramDesc', 'Kiểu quyết định trạng thái nào tồn tại; màn hiện từng trạng thái', 'The type decides which states exist; the screens show each one')
    for k, vi, en in [('type', 'Kiểu UiState', 'The UiState type'), ('states', 'Trạng thái biểu diễn được', 'Representable states'), ('screen', 'Ba màn dùng state', 'Three screens using it'), ('catch', 'Khối catch', 'The catch block')]:
        m('n.' + k, vi, en)
    m('met.combos', 'Số dạng biểu diễn được', 'Representable shapes'); m('met.invalid', 'Dạng vô nghĩa', 'Meaningless shapes')
    m('met.silent', 'Màn hiện sai mà không ai báo', 'Screens wrong with no warning'); m('met.flagged', 'Chỗ trình biên dịch chỉ ra', 'Places the compiler points to')
    a('cap.adt', 'Kiểu quyết định những trạng thái nào biểu diễn được; khối catch ghi vào state; màn hình hiện từng trạng thái. Nút đỏ: trạng thái vô nghĩa lọt vào, hay màn hiện sai.',
      'The type decides which states are representable; the catch block writes the state; the screens show each state. A red node: a meaningless state got in, or a screen shows the wrong thing.')
    S = [
        ('product', 's1', 'Đếm dạng: 2 × 2 × 2 = 8', 'Counting shapes: 2 × 2 × 2 = 8',
         'SlotsUiState có ba trường độc lập: isLoading (2 giá trị), error (có hoặc không), slots (có hoặc không). Một data class là product type: số dạng nhân với nhau, 2 × 2 × 2 = 8.',
         'SlotsUiState has three independent fields: isLoading (2 values), error (present or absent), slots (present or absent). A data class is a product type: the shapes multiply, 2 × 2 × 2 = 8.'),
        ('product', 's2', 'Chỉ 3 trên 8 có nghĩa', 'Only 3 of 8 make sense',
         'Màn này vào là tải ngay, rồi ra lỗi hoặc danh sách. Chỉ (true, null, null), (false, lỗi, null), (false, null, danh sách) có nghĩa. 5 tổ hợp còn lại vẫn biểu diễn được: (false, null, null) làm slots!! crash, (true, lỗi, …) che lỗi sau vòng quay.',
         'This screen loads on entry, then ends in an error or the list. Only (true, null, null), (false, error, null) and (false, null, list) make sense. The other 5 are still representable: (false, null, null) makes slots!! crash, (true, error, …) hides the error behind the spinner.'),
        ('product', 's3', 'Khối catch quên tắt isLoading', 'The catch block forgets isLoading',
         'Mất mạng khi đang tải: catch đặt error nhưng quên isLoading = false. State thành (true, lỗi, null), một tổ hợp vô nghĩa mà kiểu vẫn cho phép. Chuỗi if xét isLoading trước nên màn chỉ quay mãi; lỗi không bao giờ hiện.',
         'The network drops while loading: catch sets error but forgets isLoading = false. The state becomes (true, error, null), a meaningless combination the type still allows. The if chain checks isLoading first, so the screen spins forever; the error never shows.'),
        ('product', 's4', 'Thêm tải lại giữ dữ liệu cũ: trình biên dịch im lặng', 'Adding refresh with old data: the compiler stays silent',
         'Thiết kế mới muốn tải lại mà vẫn hiện danh sách cũ. Tổ hợp (true, null, danh sách) đã biểu diễn được từ trước, nên không dòng nào báo lỗi. Chuỗi if ở cả 3 màn gặp isLoading trước và ẩn dữ liệu sau vòng quay.',
         'The new design wants to refresh while still showing the old list. The combination (true, null, list) was representable all along, so nothing reports an error. The if chain on all 3 screens hits isLoading first and hides the data behind the spinner.'),
        ('sum', 's1', 'Đếm dạng: 1 + 1 + 1 = 3', 'Counting shapes: 1 + 1 + 1 = 3',
         'sealed interface với ba kiểu con: Loading, Error(message), Success(slots). Một trạng thái là đúng một trong các kiểu con, nên số dạng cộng với nhau: 1 + 1 + 1 = 3.',
         'A sealed interface with three subtypes: Loading, Error(message), Success(slots). A state is exactly one of the subtypes, so the shapes add: 1 + 1 + 1 = 3.'),
        ('sum', 's2', 'Mọi dạng đều có nghĩa', 'Every shape makes sense',
         'Ba kiểu con trùng đúng ba trạng thái của thiết kế. Không có dạng "vừa quay vừa lỗi" hay "không gì cả" để biểu diễn; when trên state chỉ có ba nhánh và không cần else.',
         'The three subtypes match the design\'s three states exactly. There is no "spinning with an error" or "nothing at all" to represent; a when on the state has three branches and needs no else.'),
        ('sum', 's3', 'Khối catch chỉ tạo được Error', 'The catch block can only produce Error',
         '_state.value = Error(message): không có trường isLoading nào để quên tắt. Màn hiện thông báo lỗi.',
         '_state.value = Error(message): there is no isLoading field to forget. The screen shows the error message.'),
        ('sum', 's4', 'Thêm Refreshing: trình biên dịch chỉ ra 3 chỗ', 'Adding Refreshing: the compiler points to 3 places',
         'Thêm data class Refreshing(slots). Ba chỗ when trên state không còn phủ đủ nên không biên dịch được cho tới khi mỗi chỗ có nhánh mới; mỗi màn quyết định rõ cách hiện dữ liệu cũ cùng dấu tải lại.',
         'Add data class Refreshing(slots). The three when expressions on the state are no longer exhaustive and stop compiling until each gets the new branch; each screen decides explicitly how to show old data with a refresh indicator.'),
    ]
    for case, k, tv, te, xv, xe in S:
        sid = case + '.' + k
        m('s.%s.title' % sid, tv, te); m('s.%s.explain' % sid, xv, xe); m('ev.' + sid, tv, te)
    for k, vi, en in [
        ('try', 'Theo dõi bảng tính ở trên và ma trận ở dưới: đếm số dạng, rồi xem dạng nào có nghĩa.', 'Follow the count above and the matrix below: count the shapes, then see which ones make sense.'),
        ('product.s2', 'Carli (ch.10): Pair<A, B> có số giá trị bằng tích số giá trị của A và B (tích Descartes); data class nhiều trường cũng vậy, như Boolean × Triage × Byte = 2 × 3 × 256 = 1.536. Kiểu nullable là A + 1: thêm đúng một giá trị null. [[src:book-fp-tut]]',
         'Carli (ch.10): Pair<A, B> has as many values as A\'s count times B\'s (the Cartesian product); multi-field data classes too, such as Boolean × Triage × Byte = 2 × 3 × 256 = 1,536. A nullable type is A + 1: exactly one extra value, null. [[src:book-fp-tut]]'),
        ('product.s3', 'Carli (ch.10) có một ví dụ cùng bệnh: callback (Data, Result?, Error?) cho phép gọi với cả Result lẫn Error, hay không có cái nào. Kiểu cho phép thì sớm muộn sẽ có mã tạo ra nó. [[src:book-fp-tut]]',
         'Carli (ch.10) has an example with the same disease: a callback (Data, Result?, Error?) can be called with both Result and Error, or with neither. What the type allows, some code will eventually produce. [[src:book-fp-tut]]'),
        ('product.s4', 'Thêm một trạng thái vào product type không đổi kiểu, nên không có chỗ nào bị buộc phải xem lại. Lỗi chỉ lộ khi có người nhìn thấy màn hình.',
         'Adding a state to a product type does not change the type, so nothing is forced to be reviewed. The bug only shows when someone looks at the screen.'),
        ('sum.s1', 'Carli (ch.10): Either<A, B> có số giá trị bằng tổng của A và B; Unit tính là 1, Nothing là 0. sealed interface với các kiểu con là cùng ý: một giá trị là đúng một trong các kiểu con. [[src:book-fp-tut]]',
         'Carli (ch.10): Either<A, B> has as many values as A\'s count plus B\'s; Unit counts as 1, Nothing as 0. A sealed interface with subtypes is the same idea: a value is exactly one of the subtypes. [[src:book-fp-tut]]'),
        ('sum.s2', 'Carli (ch.10) viết lại callback thành Result × (Info + Error): chỉ hai cách gọi hợp lệ. Theo ông, điều quan trọng hơn những gì kiểu cho làm là những gì nó không cho làm. [[src:book-fp-tut]]',
         'Carli (ch.10) rewrites the callback as Result × (Info + Error): only two valid calls remain. In his words, what you cannot do matters more than what you can. [[src:book-fp-tut]]'),
        ('sum.s3', 'Đặt state bằng một kiểu con thay vì sửa từng trường bằng copy: một phép gán, một trạng thái, không có trường nào bị bỏ sót.',
         'Set the state to one subtype instead of patching fields with copy: one assignment, one state, no field left behind.'),
        ('sum.s4', 'Tài liệu Kotlin: các kiểu con trực tiếp của sealed được biết lúc biên dịch, nên when trên nó được kiểm phủ đủ mà không cần else. Viết else là tự tắt lời nhắc này (track Kotlin, chương K5). [[src:kt-sealed]]',
         'Kotlin docs: the direct subtypes of a sealed type are known at compile time, so a when on it is checked for exhaustiveness with no else. Writing else switches this reminder off (Kotlin track, chapter K5). [[src:kt-sealed]]'),
    ]:
        m('co.' + k, vi, en)

    z = lambda k, vi, en=None: a('vz.' + k, vi, en)
    z('tab.adt', 'Đếm trạng thái và ma trận', 'Counting states and the matrix')
    z('adt.ccap.product', 'Product type: số dạng của các trường nhân với nhau. Trường nullable tính hai dạng: có hoặc không.', 'Product type: the fields\' shape counts multiply. A nullable field counts as two shapes: present or absent.')
    z('adt.ccap.sum', 'Sum type: số dạng của các kiểu con cộng với nhau. Mỗi kiểu con ở đây tính một dạng.', 'Sum type: the subtypes\' shape counts add up. Each subtype here counts as one shape.')
    for k, vi, en in [('part', 'Thành phần', 'Part'), ('type', 'Kiểu', 'Type'), ('count', 'Số dạng', 'Shapes'), ('combo', 'Ba trường (isLoading, error, slots)', 'The three fields (isLoading, error, slots)'),
                      ('variant', 'Kiểu con', 'Subtype'), ('mean', 'Có nghĩa?', 'Meaningful?'), ('ui', 'Màn hình hiện', 'The screen shows')]:
        z('adt.col.' + k, vi, en)
    z('adt.total', 'Tổng: {expr}', 'Total: {expr}')
    z('adt.mcap.product', 'Mọi tổ hợp của ba trường. Thiết kế màn này: vào là tải ngay; kết quả là lỗi hoặc danh sách; bước 4 thêm tải lại giữ dữ liệu cũ.', 'Every combination of the three fields. This screen\'s design: load on entry; the result is an error or the list; step 4 adds refreshing while keeping old data.')
    z('adt.mcap.sum', 'Mọi kiểu con của sealed interface: chỉ những trạng thái thiết kế muốn.', 'Every subtype of the sealed interface: only the states the design wants.')
    for k, vi, en in [('loading', 'đang tải', 'loading'), ('error', 'lỗi', 'error'), ('success', 'danh sách', 'list'), ('refresh', 'tải lại, giữ dữ liệu cũ', 'refreshing, keeping old data'), ('none', 'vô nghĩa', 'meaningless')]:
        z('adt.mean.' + k, vi, en)
    for k, vi, en in [('spinner', 'vòng quay', 'spinner'), ('error', 'thông báo lỗi', 'error message'), ('list', 'danh sách giờ trống', 'the slot list'), ('listRefreshing', 'danh sách cùng dấu tải lại', 'the list with a refresh indicator'), ('crash', 'crash: slots!! là null', 'crash: slots!! is null')]:
        z('adt.ui.' + k, vi, en)
    z('adt.sub.none', 'Bước 3 và 4 thêm một lỗi thật và một trạng thái mới.', 'Steps 3 and 4 add a real bug and a new state.')
    z('adt.sub.bug.product', 'Bước 3: khối catch đặt error nhưng quên isLoading = false, tạo ra (true, lỗi, null): màn chỉ hiện vòng quay, lỗi bị che.', 'Step 3: the catch block sets error but forgets isLoading = false, producing (true, error, null): the screen shows only the spinner, the error is hidden.')
    z('adt.sub.bug.sum', 'Bước 3: khối catch chỉ có thể tạo Error(message); không có trường nào để quên.', 'Step 3: the catch block can only produce Error(message); there is no field to forget.')
    z('adt.sub.v2.product', 'Bước 4: tổ hợp tải lại đã biểu diễn được từ trước nên trình biên dịch không nói gì; chuỗi if hiện vòng quay và ẩn dữ liệu ở {n} màn.', 'Step 4: the refresh combination was always representable, so the compiler says nothing; the if chain shows the spinner and hides the data on {n} screens.')
    z('adt.sub.v2.sum', 'Bước 4: thêm Refreshing làm {n} chỗ when không còn phủ đủ; trình biên dịch báo lỗi tới khi mỗi chỗ có nhánh mới.', 'Step 4: adding Refreshing makes {n} when expressions non-exhaustive; the compiler reports errors until each has the new branch.')
    z('adt.legend', 'Đỏ gạch: tổ hợp vô nghĩa, hay màn hiện sai. Đậm: trạng thái thiết kế muốn. Viền: tổ hợp hay kiểu con của bước này. "?": chưa tới bước đó.', 'Red hatched: a meaningless combination, or a screen showing the wrong thing. Bold: a state the design wants. Outlined: this step\'s combination or subtype. "?": that step has not come yet.')

    C = 'p4'
    a(C + '.title', 'Kiểu dữ liệu đại số', 'Algebraic data types')
    a(C + '.essence', 'Đếm số dạng của một kiểu: data class (product) nhân số dạng các trường; sealed interface (sum) cộng số dạng các kiểu con; kiểu nullable là A + 1.\nUiState ba trường độc lập có 8 dạng mà màn thường chỉ cần 3; 5 dạng còn lại là trạng thái vô nghĩa mà kiểu vẫn cho phép, và mã sớm muộn sẽ tạo ra chúng.\nDịch chữ "hoặc" trong mô tả thiết kế thành sum type: mỗi trạng thái một kiểu con, when phủ đủ, và thêm trạng thái mới thì trình biên dịch chỉ ra mọi chỗ phải sửa.',
      'Count a type\'s shapes: a data class (product) multiplies its fields\' counts; a sealed interface (sum) adds its subtypes\' counts; a nullable type is A + 1.\nA UiState with three independent fields has 8 shapes where the screen usually needs 3; the other 5 are meaningless states the type still allows, and code will eventually produce them.\nTranslate the "or" in the design\'s description into a sum type: one subtype per state, an exhaustive when, and a new state makes the compiler point at every place to change.')
    a(C + '.goal.g1', 'Đã đếm số dạng và dạng vô nghĩa', 'Counted the shapes and the meaningless ones')
    a(C + '.goal.g2', 'Đã thấy trạng thái mới được xử lý thế nào', 'Saw how the new state is handled')
    a(C + '.sim.fp.adt', 'data class ba trường hay sealed interface', 'a three-field data class or a sealed interface')

    S_ = 'hook'
    a(C + '.sec.%s.title' % S_, 'Đoán trước khi đọc', 'Predict before reading')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'predict', 'UiState(isLoading: Boolean, error: String?, slots: List<Slot>?) có bao nhiêu dạng, nếu mỗi trường nullable chỉ tính "có" hay "không"? Màn "Lịch trống" thật sự cần bao nhiêu dạng trong số đó?',
      'How many shapes does UiState(isLoading: Boolean, error: String?, slots: List<Slot>?) have, counting each nullable field only as "present" or "absent"? How many of them does the "Free slots" screen actually need?')
    B(C, S_, 1, 'ans', '8 dạng (2 × 2 × 2). Màn này chỉ cần 3: đang tải, lỗi, danh sách. 5 dạng còn lại là trạng thái vô nghĩa mà kiểu vẫn cho phép, và mỗi dạng là một cách để mã đặt sai state.',
      '8 shapes (2 × 2 × 2). This screen needs only 3: loading, error, list. The other 5 are meaningless states the type still allows, and each is one more way for code to set the wrong state.')

    S_ = 'count'
    a(C + '.sec.%s.title' % S_, 'Đếm: product nhân, sum cộng', 'Counting: products multiply, sums add')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'p', 'Carli (ch.10) đếm số giá trị của một kiểu như đếm phần tử của một tập. Pair<Boolean, Triage> với Triage có 3 giá trị cho 2 × 3 = 6: số giá trị nhân với nhau, nên gọi là product type. Either<Boolean, Triage> cho 2 + 3 = 5: cộng với nhau, nên gọi là sum type. Unit chỉ có một giá trị nên tính là 1; Nothing không có giá trị nào nên tính là 0. [[src:book-fp-tut]]',
      'Carli (ch.10) counts a type\'s values like the elements of a set. Pair<Boolean, Triage>, with Triage having 3 values, gives 2 × 3 = 6: the counts multiply, hence product type. Either<Boolean, Triage> gives 2 + 3 = 5: they add, hence sum type. Unit has one value and counts as 1; Nothing has none and counts as 0. [[src:book-fp-tut]]')
    B(C, S_, 2, 'p', 'Kiểu nullable là A + 1: mọi giá trị của A, cộng thêm đúng một giá trị null (Carli gọi đây là Optional). Trong Kotlin, data class là product type, sealed interface hay sealed class với các kiểu con là sum type. [[src:book-fp-tut]]',
      'A nullable type is A + 1: every value of A plus exactly one more, null (Carli calls this Optional). In Kotlin, a data class is a product type, and a sealed interface or sealed class with subtypes is a sum type. [[src:book-fp-tut]]')
    B(C, S_, 3, 'kt', '// product: nhân\ndata class Filter(val onlyToday: Boolean, val sort: Sort)   // 2 × 3 = 6 (Sort có 3 giá trị)\n\n// sum: cộng\nsealed interface Payment {                                   // 1 + 1 + 3 = 5\n    data object Cash : Payment\n    data object Insurance : Payment\n    data class Card(val brand: Brand) : Payment              // Brand có 3 giá trị\n}\n\n// nullable: A + 1\nval brand: Brand? = null                                     // 3 + 1 = 4',
      '// product: multiply\ndata class Filter(val onlyToday: Boolean, val sort: Sort)   // 2 × 3 = 6 (Sort has 3 values)\n\n// sum: add\nsealed interface Payment {                                   // 1 + 1 + 3 = 5\n    data object Cash : Payment\n    data object Insurance : Payment\n    data class Card(val brand: Brand) : Payment              // Brand has 3 values\n}\n\n// nullable: A + 1\nval brand: Brand? = null                                     // 3 + 1 = 4')

    S_ = 'unrep'
    a(C + '.sec.%s.title' % S_, 'Làm cho trạng thái vô nghĩa không biểu diễn được', 'Making meaningless states unrepresentable')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'p', 'Cách làm: viết bằng lời các trạng thái thiết kế muốn ("đang tải, hoặc lỗi kèm thông báo, hoặc danh sách"), rồi dịch chữ "hoặc" thành sum type và chữ "và" thành product type. Carli làm đúng vậy với callback: "Result và Info, hoặc Result và Error" thành Result × (Info + Error), chỉ còn hai cách gọi hợp lệ. [[src:book-fp-tut]]',
      'The method: write the states the design wants in words ("loading, or an error with a message, or the list"), then translate "or" into a sum type and "and" into a product type. Carli does exactly this with a callback: "Result and Info, or Result and Error" becomes Result × (Info + Error), leaving only two valid calls. [[src:book-fp-tut]]')
    B(C, S_, 2, 'p', 'Product type vẫn đúng chỗ khi các trường thật sự độc lập: bộ lọc (chỉ hôm nay, cách sắp xếp) có mọi tổ hợp đều có nghĩa. Câu hỏi không phải "data class hay sealed", mà là "mọi tổ hợp có nghĩa không".',
      'A product type is still right when the fields are truly independent: a filter (today only, sort order) where every combination makes sense. The question is not "data class or sealed" but "does every combination make sense".')
    B(C, S_, 3, 'note', 'Thiết kế khác có thể cần thêm trạng thái: chờ trước khi tải, tải lại giữ dữ liệu cũ, danh sách rỗng. Đó là quyết định của thiết kế; sum type buộc bạn ghi nó ra thành một kiểu con có tên, thay vì để nó lẩn trong một tổ hợp trường.',
      'Other designs may need more states: idle before loading, refreshing with old data, an empty list. That is a design decision; a sum type makes you write it down as a named subtype instead of letting it hide in a combination of fields.')
    B(C, S_, 3, 'kind', 'mechanism')

    S_ = 'kotlin'
    a(C + '.sec.%s.title' % S_, 'Trong Kotlin: sealed interface và when phủ đủ', 'In Kotlin: sealed interfaces and exhaustive when')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'p', 'Khai báo sealed interface (hay sealed class) cùng các kiểu con data object và data class. Tài liệu Kotlin: kiểu con trực tiếp được biết lúc biên dịch, nên when được kiểm phủ đủ mà không cần else. Track Kotlin chương K5 đi vào chi tiết; track Kiến trúc chương G7 dùng một UiState duy nhất cho MVI. [[src:kt-sealed]]',
      'Declare a sealed interface (or sealed class) with data object and data class subtypes. The Kotlin docs: direct subtypes are known at compile time, so when is checked for exhaustiveness with no else. The Kotlin track\'s chapter K5 goes into detail; the Architecture track\'s chapter G7 uses one UiState for MVI. [[src:kt-sealed]]')
    B(C, S_, 2, 'kt', '_state.value = SlotsUiState.Loading\n_state.value = try {\n    SlotsUiState.Success(repo.slots())\n} catch (e: IOException) {\n    SlotsUiState.Error(e.message ?: "")\n}',
      '_state.value = SlotsUiState.Loading\n_state.value = try {\n    SlotsUiState.Success(repo.slots())\n} catch (e: IOException) {\n    SlotsUiState.Error(e.message ?: "")\n}')
    B(C, S_, 3, 'p', 'Mỗi lần đặt state là một biểu thức trả về đúng một kiểu con. Không còn những lời gọi copy(isLoading = …) rải rác mà mỗi chỗ phải nhớ tắt cờ.',
      'Each state change is an expression returning exactly one subtype. No more scattered copy(isLoading = …) calls where every site must remember to clear the flag.')

    S_ = 'bugs'
    a(C + '.sec.%s.title' % S_, 'Hai lỗi hay gặp', 'Two common bugs')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'bug', 'Mất mạng khi đang tải: màn quay mãi, không hiện lỗi.', 'The network drops while loading: the screen spins forever and never shows the error.')
    B(C, S_, 1, 'cause', 'catch đặt error nhưng quên isLoading = false; tổ hợp (true, lỗi, null) vẫn hợp lệ với kiểu, và chuỗi if xét isLoading trước.', 'catch sets error but forgets isLoading = false; the combination (true, error, null) is valid for the type, and the if chain checks isLoading first.')
    B(C, S_, 1, 'fix', 'Đổi UiState thành sealed interface; khối catch đặt Error(message).', 'Turn UiState into a sealed interface; the catch block sets Error(message).')
    B(C, S_, 2, 'bug', 'Crash NullPointerException ở slots!! ngay khi mở màn.', 'A NullPointerException at slots!! right as the screen opens.')
    B(C, S_, 2, 'cause', 'State mặc định là (false, null, null): không tải, không lỗi, không dữ liệu; chuỗi if rơi vào nhánh danh sách.', 'The default state is (false, null, null): not loading, no error, no data; the if chain falls through to the list branch.')
    B(C, S_, 2, 'fix', 'sealed interface không có dạng "không gì cả"; state ban đầu là Loading. Nếu thiết kế cần trạng thái chờ, thêm một kiểu con có tên như Idle.', 'The sealed interface has no "nothing at all" shape; the initial state is Loading. If the design needs a waiting state, add a named subtype such as Idle.')

    S_ = 'ex'
    a(C + '.sec.%s.title' % S_, 'Bài tập', 'Exercise')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'ex', 'Đếm số dạng của ba kiểu dưới đây, rồi viết lại kiểu callback để không còn dạng vô nghĩa. (Ý bài tập theo Exercise 10.1, 10.3 và ví dụ callback an toàn kiểu của Carli, viết lại cho app Hẹn Khám.)',
      'Count the shapes of the three types below, then rewrite the callback type so no meaningless shape remains. (The idea follows Carli\'s Exercises 10.1, 10.3 and his type-safe callback, rewritten for the ClinicBook app.)')
    B(C, S_, 1, 'exkt', 'enum class Triage { RED, YELLOW, GREEN }\ndata class Visit(val urgent: Boolean, val triage: Triage)\nsealed interface Slot { data object Closed : Slot; data class Open(val triage: Triage) : Slot }\ntypealias OnBooked = (Booking?, Throwable?) -> Unit')
    B(C, S_, 1, 'hint', 'data class nhân, sealed cộng; mỗi tham số nullable của callback tính "có" hoặc "không".', 'A data class multiplies, a sealed type adds; each nullable callback parameter counts as "present" or "absent".')
    B(C, S_, 1, 'sol', 'Visit = 2 × 3 = 6. Slot = 1 + 3 = 4. OnBooked đếm theo dạng: (có hoặc không) × (có hoặc không) = 4, trong đó (null, null) và (có, có) vô nghĩa. Viết lại thành sum: callback nhận BookResult là Booked(booking) hoặc Failed(error): 1 + 1 = 2 dạng, cả hai có nghĩa.',
      'Visit = 2 × 3 = 6. Slot = 1 + 3 = 4. OnBooked by shape: (present or absent) × (present or absent) = 4, of which (null, null) and (present, present) are meaningless. Rewrite it as a sum: the callback takes a BookResult that is Booked(booking) or Failed(error): 1 + 1 = 2 shapes, both meaningful.')
    B(C, S_, 1, 'solkt', 'sealed interface BookResult {\n    data class Booked(val booking: Booking) : BookResult\n    data class Failed(val error: Throwable) : BookResult\n}\ntypealias OnBooked = (BookResult) -> Unit')

    S_ = 'recall'
    a(C + '.sec.%s.title' % S_, 'Tự trả lời', 'Answer it yourself')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'ask', 'Trước khi viết một UiState, bạn hỏi câu gì để chọn giữa data class và sealed interface?', 'Before writing a UiState, what question do you ask to choose between a data class and a sealed interface?')
    B(C, S_, 1, 'ans', 'Mọi tổ hợp của các trường có nghĩa không. Nếu có, data class (product) là đúng; nếu thiết kế nói "hoặc cái này hoặc cái kia", dùng sealed interface (sum) để dạng vô nghĩa không biểu diễn được.', 'Does every combination of the fields make sense? If so, a data class (product) is right; if the design says "either this or that", use a sealed interface (sum) so meaningless shapes cannot be represented.')

    S_ = 'honest'
    a(C + '.sec.%s.title' % S_, 'Chương này giản lược những gì', 'What this chapter simplifies')
    a(C + '.sec.%s.badge' % S_, 'simplified')
    B(C, S_, 1, 'p', 'Phép đếm product là nhân, sum là cộng, Unit là 1, Nothing là 0, Optional là A + 1, và ví dụ callback theo Massimo Carli, Functional Programming in Kotlin by Tutorials ch.10; when phủ đủ theo tài liệu Kotlin (Sealed classes). Site đếm theo dạng: mỗi trường nullable tính "có" hoặc "không", không đếm mọi chuỗi hay danh sách có thể có. Thiết kế màn "Lịch trống" (vào là tải; bản 1 không giữ dữ liệu cũ khi tải lại) do site đặt ra; thiết kế khác có thể cần thêm trạng thái. Ba màn dùng chung state là của site.',
      'Counting products by multiplication and sums by addition, Unit as 1, Nothing as 0, Optional as A + 1, and the callback example follow Massimo Carli, Functional Programming in Kotlin by Tutorials ch.10; the exhaustive when follows the Kotlin docs (Sealed classes). The site counts shapes: each nullable field is "present" or "absent", not every possible string or list. The "Free slots" screen design (load on entry; version 1 keeps no old data while refreshing) is the site\'s; other designs may need more states. The three screens sharing the state are the site\'s.')

    for q, qv, qe, av, ae, wv, we in [
        ('q1', 'Một data class gồm một Boolean và một enum 3 giá trị có bao nhiêu giá trị?', 'How many values does a data class of a Boolean and a 3-value enum have?', 'Sáu (2 × 3).', 'Six (2 × 3).', 'Product type: số giá trị nhân với nhau.', 'Product type: the counts multiply.'),
        ('q2', 'sealed interface có Loading, Error(msg), Success(list): mấy dạng?', 'A sealed interface with Loading, Error(msg), Success(list): how many shapes?', 'Ba (1 + 1 + 1), đếm theo dạng.', 'Three (1 + 1 + 1), counting shapes.', 'Sum type: số dạng cộng với nhau.', 'Sum type: the shapes add up.'),
        ('q3', 'Triage? (enum 3 giá trị, nullable) có bao nhiêu giá trị?', 'How many values does Triage? (a 3-value enum, nullable) have?', 'Bốn.', 'Four.', 'A + 1: thêm đúng giá trị null.', 'A + 1: exactly one extra value, null.'),
        ('q4', 'Vì sao nên tránh else trong when trên một sealed interface?', 'Why avoid else in a when on a sealed interface?', 'Để khi thêm kiểu con, trình biên dịch chỉ ra mọi chỗ chưa xử lý.', 'So that adding a subtype makes the compiler point at every unhandled place.', 'else nuốt kiểu con mới mà không báo (tài liệu Kotlin; track Kotlin K5).', 'else swallows a new subtype silently (Kotlin docs; Kotlin track K5).')]:
        a(C + '.quiz.%s.q' % q, qv, qe); a(C + '.quiz.%s.a' % q, av, ae); a(C + '.quiz.%s.why' % q, wv, we)
