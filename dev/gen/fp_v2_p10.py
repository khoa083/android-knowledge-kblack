# Lập trình hàm · K10 (p10): FP trên Android: state bất biến và cập nhật lồng sâu (Phần 3: ứng dụng)
# Nguồn (chỉ ghi ở đây và docs/research/fp.md): Arrow immutable data intro, lens, setup (đọc 2026-11-25, bản 2.3.0: @optics, plugin biên dịch,
# companion object khi dùng KSP, get/set/modify, copy { set / transform }, lý do copy lồng rườm rà); Vermeulen, Bjarnason, Chiusano 3.3 (dùng chung dữ liệu);
# Carli ch.19 (Arrow, chỉ nhắc). Giọng văn dạy học.

SEC_ORDER = {'p10': ['hook', 'nested', 'sharing', 'flow', 'optics', 'bugs', 'ex', 'recall']}


def add(a):
    def B(ch, sec, n, field, vi, en=None):
        a('%s.sec.%s.b.%02d.%s' % (ch, sec, n, field), vi, vi if en is None else en)

    a('preset.optics', '''Lập trình hàm · cập nhật state lồng sâu''', '''Functional programming · updating deeply nested state''')
    m = lambda k, vi, en=None: a('m.optics.' + k, vi, en)
    m('title', '''Đổi một trường nằm sâu trong UI state''', '''Changing a field deep inside the UI state''')
    m('overview', '''Màn Hồ sơ của app Hẹn Khám giữ ProfileState gồm patient (tên, số điện thoại, mã thẻ, địa chỉ) và danh sách lịch. Hai thao tác: đổi thành phố sang Đà Nẵng, rồi thêm lịch 42. Cách 1 dựng lại Patient và sửa list tại chỗ; cách 2 dùng copy lồng và tạo list mới. Cây object sau mỗi thao tác cho thấy cái gì mới, cái gì dùng lại, cái gì mất.''',
      '''The ClinicBook Profile screen keeps a ProfileState with patient (name, phone, card, address) and a list of bookings. Two operations: change the city to Da Nang, then add booking 42. Way 1 rebuilds the Patient and changes the list in place; way 2 uses nested copy and a new list. The object tree after each operation shows what is new, what is reused and what is lost.''')
    m('wrapup', '''Dựng lại Patient làm mất số điện thoại và mã thẻ; sửa list tại chỗ làm StateFlow không phát và hỏng luôn bản cũ để hoàn tác. Copy lồng giữ đủ dữ liệu, chỉ tạo 3 object mới và dùng chung phần còn lại; list mới làm StateFlow phát. Optic cho cùng kết quả với một dòng ngắn hơn.''',
      '''Rebuilding the Patient loses the phone number and the card; changing the list in place stops StateFlow from emitting and also breaks the copy kept for undo. Nested copy keeps all the data, creates just 3 new objects and shares the rest; a new list makes StateFlow emit. An optic gives the same result in a shorter line.''')
    m('simp.1', '''Cây chỉ có ba tầng và một list; state thật có thể sâu hơn, và Compose còn có cơ chế riêng để biết khi nào vẽ lại.''',
      '''The tree has just three levels and one list; real state can be deeper, and Compose has its own mechanism for deciding when to redraw.''')
    m('simp.2', '''copy, việc dùng chung (===), giá trị mặc định và việc StateFlow chỉ phát khi giá trị khác nhau được làm thật bằng JavaScript trên một object lồng ba tầng; optic ở đây viết tay theo đường patient.address.city. API optics của Arrow theo tài liệu immutable data và lens (bản 2.3.0, đọc ngày 2026-11-25). Site không chạy Kotlin trong trang.''',
      '''copy, sharing (===), default values and StateFlow emitting only on a different value are really done in JavaScript on a three-level object; the optic here is hand-written for the path patient.address.city. Arrow\'s optics API follows its immutable data and lens docs (version 2.3.0, read on 2026-11-25). The site does not run Kotlin in the page.''')
    m('ctl.hint', '''Chọn cách cập nhật rồi đi qua bốn bước; xem ô nào trong cây chuyển đỏ, ô nào có viền, ô nào đậm.''', '''Pick a way of updating and walk the four steps; watch which tree boxes turn red, which are outlined and which are bold.''')
    m('ctl.case', '''Cách cập nhật state''', '''How the state is updated''')
    m('ctl.case.careless', '''dựng lại object, sửa list tại chỗ''', '''rebuild objects, change the list in place'''); m('ctl.case.careful', '''copy lồng, list mới''', '''nested copy, a new list''')
    m('diagramTitle', '''Thao tác, state mới, cây object, StateFlow, bản để hoàn tác''', '''Operation, new state, object tree, StateFlow, undo copy''')
    m('diagramDesc', '''Thao tác tạo state mới; cây cho thấy phần mới và phần dùng lại; StateFlow phát cho màn hình; bản cũ giữ để hoàn tác''', '''The operation creates a new state; the tree shows the new and the reused parts; StateFlow emits to the screen; the old copy is kept for undo''')
    for k, vi, en in [('action', 'Thao tác (đổi city, thêm lịch)', 'Operation (change city, add booking)'), ('state', 'State mới', 'New state'), ('tree', 'Cây object', 'Object tree'),
                      ('flow', 'StateFlow tới màn hình', 'StateFlow to the screen'), ('undo', 'Bản cũ để hoàn tác', 'Old copy for undo')]:
        m('n.' + k, vi, en)
    m('met.lost', '''Trường bị mất''', '''Fields lost'''); m('met.fresh', '''Object tạo mới''', '''New objects''')
    m('met.shared', '''Object dùng lại''', '''Reused objects'''); m('met.emitted', '''StateFlow có phát''', '''StateFlow emitted''')
    a('cap.optics', '''Thao tác tạo state mới; cây object cho thấy phần mới và phần dùng lại; StateFlow chỉ phát khi state đổi. Ô đỏ: dữ liệu mất, màn hình không cập nhật, hay bản cũ bị đổi.''',
      '''The operation creates a new state; the object tree shows the new and reused parts; StateFlow only emits when the state changes. A red box: lost data, a screen that does not update, or an old copy that changed.''')
    S = [
        ('careless', 's1', 'Dựng lại Patient: mất số điện thoại và mã thẻ', 'Rebuilding Patient: the phone and card are lost',
         'Người dùng đổi thành phố sang Đà Nẵng. Mã viết Patient(name = p.name, address = Address(p.address.street, "Đà Nẵng")): một Patient mới, chỉ điền những trường người viết nhớ tới. phone và card không được nhắc, nên nhận giá trị mặc định ("" và null). Mã vẫn biên dịch, và hồ sơ lặng lẽ mất số điện thoại cùng mã thẻ bảo hiểm.',
         'The user changes the city to Da Nang. The code writes Patient(name = p.name, address = Address(p.address.street, "Da Nang")): a new Patient filled only with the fields the writer remembered. phone and card are not mentioned, so they take their defaults ("" and null). The code still compiles, and the profile silently loses its phone number and insurance card.'),
        ('careless', 's2', 'Cây object: patient bị thay cả', 'The object tree: patient replaced wholesale',
         'Nhìn cây: patient và address là object mới, và hai trường phone, card chuyển đỏ vì đã mất giá trị. Lỗi không nằm ở việc tạo object mới, mà ở chỗ tạo lại từ đầu thay vì chép từ bản cũ.',
         'Look at the tree: patient and address are new objects, and the phone and card fields turn red because their values are gone. The bug is not creating new objects, but building them from scratch instead of copying from the old one.'),
        ('careless', 's3', 'Sửa list tại chỗ: màn hình không đổi', 'Changing the list in place: the screen does not change',
         'Thêm lịch 42 bằng state.bookings.add(42) rồi gán _state.value = state. state vẫn là đúng object cũ, nên StateFlow so giá trị mới với giá trị cũ, thấy bằng nhau và không phát. Màn hình vẫn hiện một lịch.',
         'Booking 42 is added with state.bookings.add(42), then _state.value = state. state is still the very same object, so StateFlow compares the new value with the old, finds them equal and does not emit. The screen still shows one booking.'),
        ('careless', 's4', 'Bản cũ để hoàn tác cũng bị đổi', 'The undo copy changes too',
         'val old = state chỉ đặt thêm một tên cho cùng object. Khi list bên trong bị sửa tại chỗ, old cũng thấy lịch 42, nên "hoàn tác" không đưa được về trạng thái trước. Đây là chuyện hai cái tên, một object ở chương "Bất biến, dữ liệu dùng chung và đệ quy".',
         'val old = state just gives the same object another name. When the inner list changes in place, old also sees booking 42, so "undo" cannot go back to the previous state. This is the "two names, one object" problem from the chapter "Immutability, data sharing and recursion".'),
        ('careful', 's1', 'Copy lồng ba tầng: chỉ đổi city', 'Nested copy across three levels: only city changes',
         'state.copy(patient = state.patient.copy(address = state.patient.address.copy(city = "Đà Nẵng"))). Mỗi tầng chép từ bản cũ và chỉ thay đúng một trường, nên phone, card, street giữ nguyên.',
         'state.copy(patient = state.patient.copy(address = state.patient.address.copy(city = "Da Nang"))). Each level copies from the old one and replaces exactly one field, so phone, card and street stay as they were.'),
        ('careful', 's2', 'Chỉ đường tới trường đổi là mới', 'Only the path to the changed field is new',
         'Cây cho thấy 3 object mới: ProfileState, patient, address, tức các object nằm trên đường từ gốc tới city. bookings không bị đụng tới, nên bản mới dùng chung đúng list cũ (cùng một object). Dữ liệu bất biến nên dùng chung là an toàn.',
         'The tree shows 3 new objects: ProfileState, patient, address, the objects on the path from the root to city. bookings is untouched, so the new state shares the very same list (the same object). The data is immutable, so sharing is safe.'),
        ('careful', 's3', 'List mới: StateFlow phát', 'A new list: StateFlow emits',
         'state.copy(bookings = state.bookings + 42) tạo một list mới và một ProfileState mới. Giá trị mới khác giá trị cũ, nên StateFlow phát và màn hình hiện hai lịch.',
         'state.copy(bookings = state.bookings + 42) builds a new list and a new ProfileState. The new value differs from the old, so StateFlow emits and the screen shows two bookings.'),
        ('careful', 's4', 'Optic: viết ngắn, cùng kết quả', 'An optic: shorter, same result',
         'Viết copy lồng ở nhiều chỗ thì dài và dễ sai. Arrow (thư viện bên ngoài) sinh sẵn optic cho mỗi trường: ProfileState.patient.address.city.set(state, "Đà Nẵng") cho đúng kết quả của dòng copy lồng. Không dùng Arrow thì gom dòng copy lồng vào một hàm có tên, như withCity().',
         'Writing nested copy in many places is long and error-prone. Arrow (an external library) generates an optic for each field: ProfileState.patient.address.city.set(state, "Da Nang") gives exactly the result of the nested copy line. Without Arrow, put the nested copy in a named function such as withCity().'),
    ]
    for case, k, tv, te, xv, xe in S:
        sid = case + '.' + k
        m('s.%s.title' % sid, tv, te); m('s.%s.explain' % sid, xv, xe); m('ev.' + sid, tv, te)
    for k, vi, en in [
        ('try', '''Mẹo đọc: cây là state sau thao tác; mỗi ô là một object hay một trường. Ô viền là object mới tạo hay trường vừa đổi, ô đậm là object dùng lại từ bản cũ, ô đỏ là trường bị mất hoặc chỗ có lỗi.''',
         '''Reading tip: the tree is the state after the operation; each box is an object or a field. An outlined box is a new object or a changed field, a bold box is an object reused from the old state, a red box is a lost field or a problem.'''),
        ('careless.s2', '''copy của data class chỉ chép nông: nó tạo object mới ở đúng tầng được gọi và giữ nguyên tham chiếu tới các object con (chương K4, "Data class và bằng nhau", của track Kotlin). Muốn đổi sâu thì phải copy từng tầng.''',
         '''A data class copy is shallow: it creates a new object at the level it is called on and keeps the references to the child objects (chapter K4, "Data classes and equality", of the Kotlin track). To change something deep, copy each level.'''),
        ('careless.s3', '''StateFlow chỉ phát khi giá trị mới khác giá trị cũ theo equals; gán lại chính object vừa sửa tại chỗ thì luôn bằng nhau. Dùng List chỉ đọc và tạo list mới thay cho MutableList bên trong state.''',
         '''StateFlow only emits when the new value differs from the old one by equals; assigning back the very object you just changed in place is always equal. Use a read-only List and build a new list instead of a MutableList inside the state.'''),
        ('careless.s4', '''Marco Vermeulen và cộng sự: dùng chung dữ liệu chỉ an toàn khi không ai sửa được nó; với dữ liệu sửa được, mỗi nơi giữ nó phải tự chép phòng xa. [[src:book-fp-manning]]''',
         '''Marco Vermeulen and co-authors: sharing data is only safe when nobody can modify it; with mutable data, every holder has to make its own defensive copy. [[src:book-fp-manning]]'''),
        ('careful.s1', '''Tài liệu Arrow nhận xét: Kotlin không có sẵn công cụ tốt để biến đổi giá trị lồng sâu; ta phải lặp tên trường và chép nhiều tầng dù chỉ đổi một trường. [[src:arrow-optics]]''',
         '''The Arrow docs observe: Kotlin has no great built-in tooling for transforming deeply nested values; you repeat field names and copy several levels even to touch one field. [[src:arrow-optics]]'''),
        ('careful.s2', '''Đây là dùng chung dữ liệu như ở chương "Bất biến, dữ liệu dùng chung và đệ quy": phần không đổi được dùng lại, không phải chép. [[src:book-fp-manning]]''',
         '''This is data sharing, as in the chapter "Immutability, data sharing and recursion": the unchanged parts are reused, not copied. [[src:book-fp-manning]]'''),
        ('careful.s3', '''Mỗi lần gán là một ProfileState mới, đầy đủ: màn hình không bao giờ thấy một state nửa cũ nửa mới.''',
         '''Each assignment is a new, complete ProfileState: the screen never sees a state that is half old, half new.'''),
        ('careful.s4', '''Arrow sinh optic cho lớp gắn @optics; theo tài liệu bản 2.3.0, nên dùng plugin biên dịch, còn khi dùng KSP thì mỗi lớp cần khai báo một companion object. Muốn đổi nhiều trường một lúc, dùng copy { … set … }. [[src:arrow-optics]]''',
         '''Arrow generates optics for classes annotated with @optics; per the 2.3.0 docs, the compiler plugin is recommended, and with KSP each class needs a companion object. To change several fields at once, use copy { … set … }. [[src:arrow-optics]]'''),
    ]:
        m('co.' + k, vi, en)

    z = lambda k, vi, en=None: a('vz.' + k, vi, en)
    z('tab.optics', '''Cây object của state''', '''The state's object tree''')
    z('optics.aria', '''Cây object của state; {f} object tạo mới, {l} trường bị mất''', '''The state's object tree; {f} new objects, {l} fields lost''')
    for k, vi, en in [('careless.0', 'Cách 1, sau khi đổi city: Patient được dựng lại từ đầu.', 'Way 1, after changing the city: the Patient is rebuilt from scratch.'),
                      ('careless.1', 'Cách 1: cây object sau khi đổi city.', 'Way 1: the object tree after changing the city.'),
                      ('careless.2', 'Cách 1, sau khi thêm lịch 42 bằng add() trên MutableList.', 'Way 1, after adding booking 42 with add() on a MutableList.'),
                      ('careful.0', 'Cách 2, sau khi đổi city bằng copy lồng.', 'Way 2, after changing the city with nested copy.'),
                      ('careful.1', 'Cách 2: cây object sau khi đổi city.', 'Way 2: the object tree after changing the city.'),
                      ('careful.2', 'Cách 2, sau khi thêm lịch 42 bằng bookings + 42.', 'Way 2, after adding booking 42 with bookings + 42.')]:
        z('optics.cap.' + k, vi, en)
    z('optics.sum', '''Object tạo mới: {f}; object dùng lại: {s}; trường bị mất: {l}.''', '''New objects: {f}; reused objects: {s}; fields lost: {l}.''')
    z('optics.emit.yes', '''StateFlow phát state mới: màn hình hiện hai lịch.''', '''StateFlow emits the new state: the screen shows two bookings.''')
    z('optics.emit.no', '''Cùng object nên bằng nhau: StateFlow không phát, màn hình vẫn hiện một lịch.''', '''The same object, so equal: StateFlow does not emit, and the screen still shows one booking.''')
    z('optics.undo.broken', '''Bản cũ giữ để hoàn tác cũng có lịch 42: hoàn tác không đưa về được trạng thái trước.''', '''The old copy kept for undo also has booking 42: undo cannot return to the previous state.''')
    z('optics.lens', '''ProfileState.patient.address.city.set(state, "Đà Nẵng") cho đúng kết quả của copy lồng.''', '''ProfileState.patient.address.city.set(state, "Da Nang") gives exactly the nested copy\'s result.''')
    z('optics.legend', '''Viền xanh: object tạo mới hay trường vừa đổi. Đậm: object dùng lại từ bản cũ (cùng object). Đỏ: trường bị mất, hoặc chỗ màn hình không cập nhật.''',
      '''Green outline: a new object or a changed field. Bold: an object reused from the old state (the same object). Red: a lost field, or where the screen does not update.''')

    C = 'p10'
    a(C + '.title', '''FP trên Android: state bất biến và cập nhật lồng sâu''', '''FP on Android: immutable state and deep updates''')
    a(C + '.essence', '''UI state thường lồng nhiều tầng. copy của data class chỉ chép nông, nên đổi một trường ở tầng ba cần copy ở cả ba tầng; dựng lại object bên trong từ đầu thì mọi trường không được nhắc lặng lẽ về giá trị mặc định.\nCopy lồng chỉ tạo mới các object trên đường tới trường đổi; mọi nhánh khác được dùng chung, nên rẻ và bản cũ còn nguyên.\nStateFlow chỉ phát khi giá trị đổi: sửa MutableList tại chỗ rồi gán lại cùng object thì màn hình đứng yên. Dùng kiểu chỉ đọc và thay cả state; copy lồng dài thì gom vào một hàm có tên, hoặc dùng optics của Arrow.''',
      '''UI state is often nested several levels deep. A data class copy is shallow, so changing a field three levels down needs a copy at all three levels; rebuilding an inner object from scratch silently resets every field you did not mention to its default.\nNested copy only creates new objects on the path to the changed field; every other branch is shared, so it is cheap and the old state stays intact.\nStateFlow only emits when the value changes: changing a MutableList in place and assigning the same object back leaves the screen frozen. Use read-only types and replace the whole state; put long nested copies in a named function, or use Arrow optics.''')
    a(C + '.goal.g1', '''Đã thấy cây object sau khi đổi city''', '''Saw the object tree after changing the city''')
    a(C + '.goal.g2', '''Đã thấy StateFlow phát hay không''', '''Saw whether StateFlow emitted''')
    a(C + '.sim.fp.optics', '''dựng lại object hay copy lồng''', '''rebuilding objects or nested copy''')

    S_ = 'hook'
    a(C + '.sec.%s.title' % S_, '''Đoán trước khi đọc''', '''Predict before reading''')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'predict', '''ProfileState chứa patient, patient chứa address. Dòng `state.copy(patient = Patient(name = p.name, address = Address(p.address.street, "Đà Nẵng")))` đổi thành phố, và mã biên dịch được. Nó còn làm gì khác?''',
      '''ProfileState holds patient, and patient holds address. The line `state.copy(patient = Patient(name = p.name, address = Address(p.address.street, "Da Nang")))` changes the city, and it compiles. What else does it do?''')
    B(C, S_, 1, 'ans', '''Nó làm mất số điện thoại và mã thẻ: Patient được dựng lại từ đầu, và hai trường không được nhắc nhận giá trị mặc định. Đổi sâu phải chép từng tầng từ bản cũ. Mô phỏng ngay dưới so hai cách và vẽ cây object sau mỗi thao tác.''',
      '''It loses the phone number and the card: the Patient is rebuilt from scratch, and the two fields not mentioned take their defaults. A deep change must copy each level from the old state. The simulation just below compares two ways and draws the object tree after each operation.''')

    S_ = 'nested'
    a(C + '.sec.%s.title' % S_, '''Đổi một trường nằm sâu: copy từng tầng''', '''Changing a deep field: copy each level''')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'p', '''UI state của một màn thường lồng nhiều tầng: ProfileState chứa Patient, Patient chứa Address. Vì mọi thứ bất biến (toàn val), muốn đổi city ta không sửa tại chỗ mà tạo bản mới. copy của data class tạo object mới với vài trường được đổi, nhưng nó chỉ chép nông: các object con vẫn là tham chiếu cũ (chương K4, "Data class và bằng nhau", của track Kotlin). Vì thế đổi một trường ở tầng ba cần copy ở cả ba tầng.''',
      '''A screen\'s UI state is often nested: ProfileState holds a Patient, and the Patient holds an Address. Because everything is immutable (all val), changing city means creating a new version rather than editing in place. A data class copy creates a new object with a few fields changed, but it is shallow: the child objects are still the old references (chapter K4, "Data classes and equality", of the Kotlin track). So changing a field three levels down needs a copy at all three levels.''')
    B(C, S_, 2, 'kt', '''data class Address(val street: String, val city: String)
data class Patient(val name: String, val phone: String = "", val card: String? = null, val address: Address)
data class ProfileState(val patient: Patient, val bookings: List<Long> = emptyList())

val moved = state.copy(patient = state.patient.copy(address = state.patient.address.copy(city = "Đà Nẵng")))''', '''data class Address(val street: String, val city: String)
data class Patient(val name: String, val phone: String = "", val card: String? = null, val address: Address)
data class ProfileState(val patient: Patient, val bookings: List<Long> = emptyList())

val moved = state.copy(patient = state.patient.copy(address = state.patient.address.copy(city = "Da Nang")))''')
    B(C, S_, 3, 'p', '''Lỗi hay gặp không phải là quên một tầng (khi đó mã thường không biên dịch), mà là dựng lại object bên trong từ đầu, như Patient(name = p.name, address = …). Trường nào không được nhắc sẽ nhận giá trị mặc định, và tham số mặc định càng nhiều thì càng dễ mất dữ liệu mà không có lỗi nào được báo.''',
      '''The common bug is not forgetting a level (that usually fails to compile), but rebuilding the inner object from scratch, as in Patient(name = p.name, address = …). Every field not mentioned takes its default, and the more default parameters there are, the easier it is to lose data with no error reported.''')

    S_ = 'sharing'
    a(C + '.sec.%s.title' % S_, '''Cây object: cái gì mới, cái gì dùng lại''', '''The object tree: what is new, what is reused''')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'p', '''Copy lồng chỉ tạo mới các object nằm trên đường từ gốc tới trường đổi: ProfileState, patient, address. Mọi nhánh khác, như list bookings, được dùng lại nguyên: bản mới và bản cũ cùng trỏ tới một object. Đây là dùng chung dữ liệu như ở chương "Bất biến, dữ liệu dùng chung và đệ quy" của track này, và nó an toàn vì không ai sửa được dữ liệu bất biến. [[src:book-fp-manning]]''',
      '''Nested copy only creates new objects on the path from the root to the changed field: ProfileState, patient, address. Every other branch, such as the bookings list, is reused as is: the new and the old state point to the same object. This is data sharing, as in this track\'s chapter "Immutability, data sharing and recursion", and it is safe because nobody can modify immutable data. [[src:book-fp-manning]]''')
    B(C, S_, 2, 'p', '''Nhờ vậy cập nhật sâu không tốn kém: số object mới bằng số tầng, dù state lớn tới đâu. Bản cũ vẫn còn nguyên, nên giữ lại để hoàn tác hay để so sánh là gần như miễn phí.''',
      '''That keeps deep updates cheap: the number of new objects equals the number of levels, however large the state is. The old state stays intact, so keeping it for undo or comparison costs almost nothing.''')

    S_ = 'flow'
    a(C + '.sec.%s.title' % S_, '''StateFlow chỉ phát khi giá trị đổi''', '''StateFlow only emits when the value changes''')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'p', '''Trên Android, ViewModel thường giữ UI state trong một StateFlow. StateFlow chỉ phát cho màn hình khi giá trị mới khác giá trị cũ (so bằng equals). Nếu state chứa một MutableList và bạn sửa list đó tại chỗ rồi gán lại cùng object, giá trị mới chính là giá trị cũ, nên không có gì được phát và màn hình đứng yên.''',
      '''On Android, a ViewModel usually keeps the UI state in a StateFlow. StateFlow only emits to the screen when the new value differs from the old one (compared with equals). If the state holds a MutableList and you change that list in place and assign the same object back, the new value is the old value, so nothing is emitted and the screen stays frozen.''')
    B(C, S_, 2, 'kt', '''// sai: sửa tại chỗ, gán lại cùng object
_state.value.bookings.add(42)          // bookings là MutableList
_state.value = _state.value             // bằng nhau: StateFlow không phát

// đúng: List chỉ đọc, tạo state mới
_state.update { it.copy(bookings = it.bookings + 42) }''', '''// wrong: change in place, assign the same object back
_state.value.bookings.add(42)          // bookings is a MutableList
_state.value = _state.value             // equal: StateFlow does not emit

// right: a read-only List, a new state
_state.update { it.copy(bookings = it.bookings + 42) }''')
    B(C, S_, 3, 'p', '''Quy tắc: trong UI state chỉ dùng kiểu chỉ đọc (List, Set, Map) và kiểu bất biến, rồi luôn thay cả state bằng một bản mới. Vì sao List chỉ đọc vẫn chưa hẳn là bất biến được nói ở chương K7, "Collection: read-only, mutable và xử lý", của track Kotlin.''',
      '''The rule: inside UI state, use only read-only types (List, Set, Map) and immutable types, and always replace the whole state with a new one. Why a read-only List is still not quite immutable is covered in chapter K7, "Collections: read-only, mutable and processing", of the Kotlin track.''')

    S_ = 'optics'
    a(C + '.sec.%s.title' % S_, '''Arrow optics, hoặc một hàm có tên''', '''Arrow optics, or a named function''')
    a(C + '.sec.%s.badge' % S_, 'version')
    B(C, S_, 1, 'p', '''Copy lồng ba tầng viết ở năm chỗ thì vừa dài vừa dễ sai. Tài liệu Arrow nói đúng điều đó: Kotlin không có sẵn công cụ tốt cho việc này, ta phải lặp tên trường và chép nhiều tầng dù chỉ đổi một trường. Cách nhẹ nhất, không cần thư viện: gom dòng copy lồng vào một hàm có tên, như `fun ProfileState.withCity(city: String) = copy(...)`. [[src:arrow-optics]]''',
      '''A three-level nested copy written in five places is both long and error-prone. The Arrow docs say exactly that: Kotlin lacks good built-in tooling for this, so you repeat field names and copy several levels even to change one field. The lightest fix needs no library: put the nested copy in a named function, such as `fun ProfileState.withCity(city: String) = copy(...)`. [[src:arrow-optics]]''')
    B(C, S_, 2, 'p', '''Arrow (thư viện bên ngoài, bản 2.3.0) sinh sẵn một optic cho mỗi trường của lớp gắn `@optics`. Lens (một loại optic) biết đọc và ghi một trường nằm sâu bằng `get`, `set`, `modify`. Theo tài liệu, nên dùng plugin biên dịch của Arrow; nếu dùng KSP thì mỗi lớp cần khai báo một companion object, kể cả rỗng. [[src:arrow-optics]]''',
      '''Arrow (an external library, version 2.3.0) generates an optic for each field of a class annotated with `@optics`. A lens (one kind of optic) can read and write a deep field with `get`, `set`, `modify`. Per the docs, Arrow\'s compiler plugin is recommended; with KSP, each class needs a companion object declaration, even an empty one. [[src:arrow-optics]]''')
    B(C, S_, 3, 'kt', '''@optics data class ProfileState(val patient: Patient, val bookings: List<Long>) { companion object }
// (Patient và Address cũng gắn @optics)

val moved = ProfileState.patient.address.city.set(state, "Đà Nẵng")
val both = state.copy {                              // đổi nhiều trường một lúc
    ProfileState.patient.address.city set "Đà Nẵng"
    ProfileState.patient.phone set "0909000111"
}''', '''@optics data class ProfileState(val patient: Patient, val bookings: List<Long>) { companion object }
// (Patient and Address are annotated with @optics too)

val moved = ProfileState.patient.address.city.set(state, "Da Nang")
val both = state.copy {                              // change several fields at once
    ProfileState.patient.address.city set "Da Nang"
    ProfileState.patient.phone set "0909000111"
}''')

    S_ = 'bugs'
    a(C + '.sec.%s.title' % S_, '''Hai lỗi hay gặp''', '''Two common bugs''')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'bug', '''Sau khi người dùng đổi địa chỉ, hồ sơ mất mã thẻ bảo hiểm.''', '''After the user changes the address, the profile loses its insurance card.''')
    B(C, S_, 1, 'cause', '''Mã cập nhật dựng lại Patient(name = …, address = …); card không được nhắc nên nhận mặc định null.''', '''The update code rebuilds Patient(name = …, address = …); card is not mentioned, so it takes the default null.''')
    B(C, S_, 1, 'fix', '''Chép từ bản cũ bằng state.patient.copy(…), hoặc dùng một hàm cập nhật có tên, hoặc một optic.''', '''Copy from the old value with state.patient.copy(…), or use a named update function, or an optic.''')
    B(C, S_, 2, 'bug', '''Bấm "Đặt lịch", lịch mới không hiện cho tới khi xoay màn hình.''', '''After tapping "Book", the new booking does not show until the screen is rotated.''')
    B(C, S_, 2, 'cause', '''bookings là MutableList trong state; mã gọi add() rồi gán lại cùng object, nên StateFlow không phát.''', '''bookings is a MutableList inside the state; the code calls add() and assigns the same object back, so StateFlow does not emit.''')
    B(C, S_, 2, 'fix', '''Dùng List chỉ đọc và _state.update { it.copy(bookings = it.bookings + id) }.''', '''Use a read-only List and _state.update { it.copy(bookings = it.bookings + id) }.''')

    S_ = 'ex'
    a(C + '.sec.%s.title' % S_, '''Bài tập''', '''Exercise''')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'ex', '''ProfileState có thêm `settings: Settings(reminder: Reminder(enabled: Boolean, minutesBefore: Int), language: String)`. Viết hàm thuần `fun ProfileState.withReminderMinutes(m: Int): ProfileState` đổi minutesBefore mà giữ nguyên mọi thứ khác. Rồi viết bài test kiểm ba điều: kết quả có minutesBefore mới; patient và bookings vẫn là cùng object với bản cũ (dùng ===); bản cũ không đổi.''',
      '''ProfileState gains `settings: Settings(reminder: Reminder(enabled: Boolean, minutesBefore: Int), language: String)`. Write a pure `fun ProfileState.withReminderMinutes(m: Int): ProfileState` that changes minutesBefore and keeps everything else. Then write a test checking three things: the result has the new minutesBefore; patient and bookings are still the same objects as in the old state (use ===); the old state is unchanged.''')
    B(C, S_, 1, 'hint', '''Copy ba tầng: state, settings, reminder. Dùng assertSame để kiểm "cùng object".''', '''Copy three levels: state, settings, reminder. Use assertSame to check "the same object".''')
    B(C, S_, 1, 'sol', '''Chỉ state, settings và reminder là object mới; patient và bookings được dùng chung, nên assertSame qua. Bản cũ vẫn giữ minutesBefore cũ.''', '''Only the state, settings and reminder are new objects; patient and bookings are shared, so assertSame passes. The old state keeps the old minutesBefore.''')
    B(C, S_, 1, 'solkt', '''fun ProfileState.withReminderMinutes(m: Int): ProfileState =
    copy(settings = settings.copy(reminder = settings.reminder.copy(minutesBefore = m)))

@Test fun changesOnlyTheReminder() {
    val old = sampleState()                       // minutesBefore = 60
    val new = old.withReminderMinutes(30)
    assertEquals(30, new.settings.reminder.minutesBefore)
    assertSame(old.patient, new.patient)
    assertSame(old.bookings, new.bookings)
    assertEquals(60, old.settings.reminder.minutesBefore)
}''')

    S_ = 'recall'
    a(C + '.sec.%s.title' % S_, '''Tự trả lời''', '''Answer it yourself''')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'ask', '''Vì sao dựng lại object bên trong nguy hiểm hơn quên một tầng copy?''', '''Why is rebuilding an inner object more dangerous than forgetting one level of copy?''')
    B(C, S_, 1, 'ans', '''Quên một tầng thường làm mã không biên dịch; dựng lại từ đầu thì biên dịch được, và mọi trường không được nhắc lặng lẽ về giá trị mặc định.''',
      '''Forgetting a level usually fails to compile; rebuilding from scratch compiles, and every field not mentioned silently resets to its default.''')
    B(C, S_, 2, 'ask', '''Vì sao sửa MutableList trong state rồi gán lại không cập nhật màn hình?''', '''Why does changing a MutableList in the state and assigning it back not update the screen?''')
    B(C, S_, 2, 'ans', '''StateFlow chỉ phát khi giá trị mới khác giá trị cũ; gán lại cùng object thì luôn bằng nhau.''', '''StateFlow only emits when the new value differs from the old one; assigning back the same object is always equal.''')

    for q, qv, qe, av, ae, wv, we in [
        ('q1', 'copy của data class chép nông hay sâu?', 'Is a data class copy shallow or deep?', 'Nông.', 'Shallow.',
         'Các object con vẫn là tham chiếu cũ; muốn đổi sâu phải copy từng tầng.', 'The child objects are still the old references; to change something deep, copy each level.'),
        ('q2', 'Đổi city bằng copy lồng ba tầng thì tạo bao nhiêu object mới?', 'How many new objects does changing city with a three-level nested copy create?', 'Ba: ProfileState, patient, address.', 'Three: ProfileState, patient, address.',
         'Chỉ các object trên đường từ gốc tới trường đổi.', 'Only the objects on the path from the root to the changed field.'),
        ('q3', 'Sau copy lồng, bookings của bản mới và bản cũ có là cùng object không?', 'After a nested copy, are the new and the old bookings the same object?', 'Có.', 'Yes.',
         'Nhánh không đổi được dùng chung.', 'Unchanged branches are shared.'),
        ('q4', 'Với Arrow optics dùng KSP, lớp gắn @optics cần thêm gì?', 'With Arrow optics on KSP, what else does an @optics class need?', 'Một companion object, kể cả rỗng.', 'A companion object, even an empty one.',
         'Tài liệu Arrow nói đó là do giới hạn của KSP; plugin biên dịch thì không cần.', 'The Arrow docs say this is a KSP limitation; the compiler plugin does not need it.')]:
        a(C + '.quiz.%s.q' % q, qv, qe); a(C + '.quiz.%s.a' % q, av, ae); a(C + '.quiz.%s.why' % q, wv, we)
