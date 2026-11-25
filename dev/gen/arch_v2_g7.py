# Kiến trúc · G7: MVVM và MVI (Phần 2)
# Nguồn: developer.android.com UI layer (một UI state cho state liên quan; một luồng hay nhiều luồng) (đọc 2026-11-24);
# Dumbravan, Clean Android Architecture ch.8 (MVVM) và ch.9 (MVI), đọc từ epub trong kho. Nối Kotlin K5 (sealed và when).
# Trần: 8 mục, mục cơ chế ≤ 4 khối.

SEC_ORDER = {'g7': ['hook', 'mvvm', 'single', 'mvi', 'bugs', 'ex', 'recall']}


def add(a):
    def B(ch, sec, n, field, vi, en=None):
        a('%s.sec.%s.b.%02d.%s' % (ch, sec, n, field), vi, vi if en is None else en)

    m = lambda k, vi, en=None: a('m.mvi.' + k, vi, en)
    m('title', 'Màn Lịch của tôi: đang tải, lỗi và dữ liệu', 'My appointments: loading, error and data')
    m('overview', 'Màn Lịch của tôi có ba thứ để hiện: đang tải, thông báo lỗi, danh sách lịch hẹn. Ba cách giữ chúng: (1) ba StateFlow riêng trong ViewModel; (2) một data class UiState trong một StateFlow (MVVM); (3) MVI: intent đi vào, reducer tạo một state thuộc sealed interface. Kịch bản: mở màn, tải lỗi vì mất mạng, bấm Thử lại, tải được.',
      'My appointments has three things to show: loading, an error message, the appointment list. Three ways to hold them: (1) three separate StateFlows in the ViewModel; (2) one UiState data class in one StateFlow (MVVM); (3) MVI: intents go in, a reducer produces a state from a sealed interface. Scenario: open the screen, the load fails offline, tap Retry, the load succeeds.')
    m('wrapup', 'Ba luồng state riêng có thể lệch nhau, nên màn hình rơi vào tổ hợp vô nghĩa như vừa đang tải vừa báo lỗi. Gộp vào một UiState, cập nhật một lần cho mỗi thay đổi, thì bớt phần lớn lỗi, nhưng kiểu dữ liệu vẫn cho phép tổ hợp sai. MVI đi thêm một bước: state là một sealed interface (kiểu chỉ có một số trường hợp đã liệt kê) chứa đúng các trạng thái hợp lệ, và mọi thay đổi đi qua một hàm reducer thuần (nhận state cũ và một sự kiện, trả state mới), test được bằng bảng đầu vào và đầu ra.\nQuy tắc dễ nhớ: nếu kiểu dữ liệu cho phép một trạng thái vô nghĩa, sớm muộn màn hình sẽ hiện nó.',
      'Separate state streams can drift apart, so the screen lands in meaningless combinations such as loading and erroring at once. Merging them into one UiState, updated once per change, removes most bugs, but the type still allows wrong combinations. MVI goes one step further: the state is a sealed interface (a type with only a listed set of cases) holding exactly the valid states, and every change goes through a pure reducer function (old state plus an event in, new state out), testable with a table of inputs and outputs.\nRule of thumb: if the type allows a meaningless state, sooner or later the screen will show it.')
    m('simp.1', 'Ba bit (đang tải, lỗi, dữ liệu) và năm tổ hợp hợp lệ là định nghĩa của site cho màn này; màn khác có thể có tập trạng thái khác. Reducer trong mô phỏng nhận kết quả (result) chứ không nhận intent trực tiếp; các thư viện MVI làm khác nhau. Chương chưa nói về side effect trong MVI (điều hướng, thông báo); phần đó nối với chương G3, "UI layer: UiState, ViewModel và sự kiện".',
      'The three bits (loading, error, data) and the five valid combinations are the site\'s definition for this screen; other screens may have other state sets. The reducer in the simulation takes results rather than intents directly; MVI libraries differ here. The chapter does not cover side effects in MVI (navigation, messages); that ties back to chapter G3, "The UI layer: UiState, ViewModel and events".')
    m('ctl.hint', 'Đổi cách giữ state rồi đi lại bốn bước; xem tab "Ma trận trạng thái".', 'Switch how state is held and walk the four steps again; watch the "State matrix" tab.')
    m('ctl.case', 'Cách giữ state', 'How state is held')
    for k, vi, en in [('streams', 'ba StateFlow riêng', 'three separate StateFlows'), ('single', 'một UiState (MVVM)', 'one UiState (MVVM)'), ('mvi', 'MVI: intent, reducer, state kiểu sealed', 'MVI: intent, reducer, sealed state')]:
        m('ctl.case.' + k, vi, en)
    m('diagramTitle', 'Màn hình, ViewModel, state', 'Screen, ViewModel, state')
    m('diagramDesc', 'Màn hình gửi sự kiện hay intent lên ViewModel; ViewModel tạo state; state quay về màn hình', 'The screen sends events or intents to the ViewModel; the ViewModel produces state; state returns to the screen')
    for k, vi, en in [('ui', 'Màn Lịch của tôi', 'My appointments'), ('vm', 'ViewModel (có reducer)', 'ViewModel (reducer)'), ('state', 'State', 'State')]:
        m('n.' + k, vi, en)
    m('met.streams', 'Số luồng state', 'State streams'); m('met.bad', 'Tổ hợp sai đã gặp', 'Wrong combinations seen'); m('met.repr', 'Số trạng thái kiểu cho phép', 'States the type allows')
    a('cap.mvi', 'Vòng: màn hình gửi sự kiện lên ViewModel, ViewModel tạo state, state quay về màn hình. Khối viền đỏ là chỗ màn hình đang ở một tổ hợp vô nghĩa. Tab "Ma trận trạng thái" liệt kê đủ tám tổ hợp.',
      'A loop: the screen sends events to the ViewModel, the ViewModel produces state, state returns to the screen. A red-outlined box marks the screen sitting in a meaningless combination. The "State matrix" tab lists all eight combinations.')
    S = [
        ('streams', 's1', 'Mở màn: isLoading = true', 'Open: isLoading = true',
         'ViewModel đặt isLoading.value = true. Hai luồng kia chưa đổi. Màn hình hiện vòng xoay.',
         'The ViewModel sets isLoading.value = true. The other two streams are unchanged. The screen shows a spinner.'),
        ('streams', 's2', 'Tải lỗi: vừa đang tải vừa báo lỗi', 'The load fails: loading and erroring at once',
         'catch đặt error = "Mất mạng" nhưng quên isLoading = false. Màn hình hiện vòng xoay cùng thông báo lỗi.',
         'catch sets error = "Offline" but forgets isLoading = false. The screen shows the spinner and the error together.'),
        ('streams', 's3', 'Thử lại thành công: danh sách kèm lỗi cũ', 'Retry succeeds: the list with a stale error',
         'Lần tải sau thành công: appointments có dữ liệu, isLoading = false. Không ai xóa error, nên danh sách hiện kèm dòng "Mất mạng".',
         'The next load succeeds: appointments has data, isLoading = false. Nobody clears error, so the list shows with an "Offline" banner.'),
        ('streams', 's4', 'Kéo làm mới: cả ba cùng bật', 'Pull to refresh: all three at once',
         'isLoading lại true trong khi error và danh sách vẫn còn. Ba luồng, mỗi luồng tự đúng, nhưng tổ hợp thì sai. Ba lần ra tổ hợp vô nghĩa.',
         'isLoading turns true again while error and the list remain. Three streams, each right on its own, but the combination is wrong. Three meaningless combinations so far.'),
        ('single', 's1', 'Mở màn: một lần cập nhật cả state', 'Open: one update for the whole state',
         'state.update { it.copy(isLoading = true, error = null) }: đặt đang tải và xóa lỗi trong cùng một lần.',
         'state.update { it.copy(isLoading = true, error = null) }: set loading and clear the error in one go.'),
        ('single', 's2', 'Tải lỗi: tắt tải và đặt lỗi cùng lúc', 'The load fails: stop loading and set the error together',
         'Nhánh lỗi tạo state mới với isLoading = false và error = "Mất mạng" trong một lần copy. Không có khoảnh khắc nào màn hình thấy nửa cũ nửa mới.',
         'The error branch builds a new state with isLoading = false and error = "Offline" in one copy. There is no moment where the screen sees half old, half new.'),
        ('single', 's3', 'Thử lại: lỗi được xóa ngay khi bắt đầu tải', 'Retry: the error is cleared as loading starts',
         'Cùng dòng update ở đầu load() vừa bật đang tải vừa xóa lỗi.',
         'The same update at the start of load() both turns loading on and clears the error.'),
        ('single', 's4', 'Thành công; nhưng kiểu vẫn cho phép tổ hợp sai', 'Success; but the type still allows wrong combinations',
         'Màn hình hiện danh sách. Không tổ hợp sai nào xuất hiện, nhưng ApptUiState(isLoading = true, error = "...") vẫn viết được: trình biên dịch không chặn, chỉ kỷ luật của người viết chặn.',
         'The screen shows the list. No wrong combination appeared, but ApptUiState(isLoading = true, error = "...") can still be written: the compiler does not stop it, only the author\'s discipline does.'),
        ('mvi', 's1', 'Intent Load: state thành Loading', 'Intent Load: state becomes Loading',
         'Màn hình gửi ApptIntent.Load. ViewModel đặt ApptState.Loading, một trong bốn trạng thái của sealed interface.',
         'The screen sends ApptIntent.Load. The ViewModel sets ApptState.Loading, one of the sealed interface\'s four states.'),
        ('mvi', 's2', 'Kết quả Failed: reducer trả Error', 'Result Failed: the reducer returns Error',
         'reduce(state, ApptResult.Failed("Mất mạng")) trả ApptState.Error. Loading và Error là hai kiểu khác nhau, không thể cùng lúc.',
         'reduce(state, ApptResult.Failed("Offline")) returns ApptState.Error. Loading and Error are different types and cannot coexist.'),
        ('mvi', 's3', 'Intent Retry: lại Loading', 'Intent Retry: Loading again',
         'Thử lại đi qua đúng con đường đó: intent vào, state ra. Lỗi cũ không còn vì Loading không có trường lỗi.',
         'Retry takes exactly the same path: intent in, state out. The old error is gone because Loading has no error field.'),
        ('mvi', 's4', 'Loaded: Content; chỉ 4 trạng thái tồn tại', 'Loaded: Content; only 4 states exist',
         'reduce trả ApptState.Content(items). Kiểu chỉ có Loading, Refreshing, Content, Error, nên các tổ hợp sai không viết ra được. when trên sealed interface buộc xử lý đủ bốn trường hợp (Kotlin K5).',
         'reduce returns ApptState.Content(items). The type has only Loading, Refreshing, Content and Error, so wrong combinations cannot be written. A when over the sealed interface must handle all four (Kotlin K5).'),
    ]
    for case, k, tv, te, xv, xe in S:
        sid = case + '.' + k
        m('s.%s.title' % sid, tv, te); m('s.%s.explain' % sid, xv, xe); m('ev.' + sid, tv, te)
    for k, vi, en in [
        ('try', 'Đi bốn bước của từng cách; xem ô "Xuất hiện ở bước" trong ma trận và số tổ hợp sai.', 'Walk the four steps of each approach; watch the "Seen at step" column in the matrix and the count of wrong combinations.'),
        ('streams.s2', 'Tài liệu Android nói: nếu hai phần liên quan nằm ở hai luồng khác nhau, có lúc một phần đã đổi còn phần kia chưa. [[src:ax-ui-layer]]', 'The Android docs say: if two related pieces live in two different streams, one may be updated while the other is not. [[src:ax-ui-layer]]'),
        ('streams.s3', 'Lỗi kiểu này khó thấy vì từng luồng đều đúng khi xem riêng; chỉ tổ hợp của chúng sai.', 'This kind of bug is hard to see because each stream is right on its own; only their combination is wrong.'),
        ('streams.s4', 'Tài liệu khuyên dùng một UI state cho các state liên quan nhau: ít lệch hơn, mã dễ hiểu hơn. [[src:ax-ui-layer]]', 'The docs advise a single UI state for related states: fewer inconsistencies and easier code. [[src:ax-ui-layer]]'),
        ('single.s2', 'Alexandru Dumbravan mô tả: trong MVVM, View phụ thuộc ViewModel, ViewModel phụ thuộc Model, và View quan sát dữ liệu ViewModel lộ ra. [[src:book-dumbravan]]', 'Alexandru Dumbravan describes it: in MVVM the View depends on the ViewModel, the ViewModel on the Model, and the View observes the data the ViewModel exposes. [[src:book-dumbravan]]'),
        ('single.s3', 'Một luồng có lợi là người dùng state luôn có thông tin mới nhất; tách luồng chỉ hợp khi các phần thật sự không liên quan hay đổi với tần suất rất khác nhau. [[src:ax-ui-layer]]', 'A single stream means consumers always have the latest information; separate streams fit only when the pieces are truly unrelated or change at very different rates. [[src:ax-ui-layer]]'),
        ('single.s4', 'Data class gồm Boolean và trường nullable có 2 × 2 × 2 = 8 tổ hợp; chỉ một phần trong đó có nghĩa với màn này.', 'A data class of a Boolean and nullable fields has 2 × 2 × 2 = 8 combinations; only some of them make sense for this screen.'),
        ('mvi.s2', 'Alexandru Dumbravan mô tả: MVI gộp dữ liệu bất biến thành một state mà UI quan sát; mọi thay đổi đi qua một luồng dữ liệu phản ứng tạo ra state mới. [[src:book-dumbravan]]', 'Alexandru Dumbravan describes it: MVI combines immutable data into one state the UI observes; every change goes through a reactive flow that produces a new state. [[src:book-dumbravan]]'),
        ('mvi.s3', 'Chữ Intent của MVI khác lớp android.content.Intent; ở đây nó là ý định của người dùng. MVI không thay ViewModel mà xây trên nó. [[src:book-dumbravan]]', 'MVI\'s Intent is not the android.content.Intent class; here it is what the user wants. MVI does not replace the ViewModel but builds on it. [[src:book-dumbravan]]'),
        ('mvi.s4', 'reduce là hàm thuần: cùng state và kết quả luôn cho cùng state mới, nên test bằng một bảng đầu vào và đầu ra, không cần coroutine hay mạng.', 'reduce is a pure function: the same state and result always give the same new state, so it is tested with a table of inputs and outputs, no coroutines or network needed.')]:
        m('co.' + k, vi, en)
    a('preset.mvi', 'Kiến trúc · ba luồng state so với một state duy nhất', 'Architecture · three state streams versus one single state')

    z = lambda k, vi, en=None: a('vz.' + k, vi, en)
    z('tab.mvi', 'Ma trận trạng thái', 'State matrix')
    z('mvi.cap', 'Tám tổ hợp của đang tải (L), lỗi (E) và dữ liệu (D). Cột cuối cho biết tổ hợp nào đã xuất hiện ở bước nào; tổ hợp sai đã xuất hiện tô đỏ.', 'The eight combinations of loading (L), error (E) and data (D). The last column shows which combination appeared at which step; wrong ones that appeared are red.')
    z('mvi.legend', 'Ô viền: tổ hợp của bước đang xem. Ô mờ: kiểu sealed không biểu diễn được tổ hợp đó.', 'Outlined: the current step\'s combination. Faded: the sealed type cannot represent that combination.')
    for k, vi, en in [('L', 'Đang tải', 'Loading'), ('E', 'Lỗi', 'Error'), ('D', 'Dữ liệu', 'Data'), ('screen', 'Màn hình hiện', 'Screen shows'), ('valid', 'Có nghĩa?', 'Meaningful?'), ('seen', 'Xuất hiện ở', 'Seen at')]:
        z('mvi.col.' + k, vi, en)
    z('mvi.yes', 'có', 'yes'); z('mvi.no', '·', '-')
    for k, vi, en in [('000', 'trống, chưa tải', 'empty, not loaded'), ('100', 'vòng xoay', 'a spinner'), ('101', 'danh sách, kèm thanh làm mới', 'the list with a refresh bar'), ('001', 'danh sách', 'the list'),
                      ('010', 'thông báo lỗi và nút Thử lại', 'an error and a Retry button'), ('110', 'vòng xoay cùng lỗi', 'a spinner with an error'), ('111', 'vòng xoay, lỗi và danh sách', 'spinner, error and list'), ('011', 'danh sách kèm lỗi cũ', 'the list with a stale error')]:
        z('mvi.screen.' + k, vi, en)
    z('mvi.ok', 'có nghĩa', 'meaningful'); z('mvi.wrong', 'vô nghĩa', 'meaningless'); z('mvi.impossible', 'không biểu diễn được', 'cannot be represented'); z('mvi.atStep', 'bước', 'step')

    C = 'g7'
    a(C + '.title', 'MVVM và MVI', 'MVVM and MVI')
    a(C + '.essence', 'MVVM: View quan sát state mà ViewModel lộ ra, và gửi sự kiện lên ViewModel. Đây là mô hình chương G3 đã dùng.\nCác phần state liên quan nhau (đang tải, lỗi, dữ liệu) nên nằm trong một UiState cập nhật một lần cho mỗi thay đổi; tách thành nhiều luồng thì chúng có thể lệch nhau.\nMVI thêm hai điều: state là kiểu chỉ có trạng thái hợp lệ (sealed interface), và mọi thay đổi đi qua một reducer thuần (state cũ + kết quả → state mới).',
      'MVVM: the View observes the state the ViewModel exposes and sends events up to it. This is the model chapter G3 used.\nRelated pieces of state (loading, error, data) should live in one UiState updated once per change; split into several streams, they can drift apart.\nMVI adds two things: the state is a type with only valid states (a sealed interface), and every change goes through a pure reducer (old state + result → new state).')
    a(C + '.goal.g1', 'Đã thấy vừa đang tải vừa báo lỗi', 'Saw loading and an error at once')
    a(C + '.goal.g2', 'Đã đi hết bốn bước', 'Walked all four steps')
    a(C + '.sim.arch.mvi', 'đang tải, lỗi và dữ liệu', 'loading, error and data')

    S_ = 'hook'
    a(C + '.sec.%s.title' % S_, 'Đoán trước khi đọc', 'Predict before reading')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'predict', 'ViewModel có ba StateFlow: isLoading, error, appointments. Khối catch đặt error nhưng quên isLoading = false. Mất mạng khi đang tải: màn hình hiện gì?',
      'The ViewModel has three StateFlows: isLoading, error, appointments. The catch block sets error but forgets isLoading = false. The network drops mid-load: what does the screen show?')
    B(C, S_, 1, 'ans', 'Vòng xoay và thông báo lỗi cùng lúc: mỗi luồng tự đúng, nhưng tổ hợp vô nghĩa. Mô phỏng bên dưới đếm các tổ hợp như vậy với ba cách giữ state. [[src:ax-ui-layer]]',
      'A spinner and an error at the same time: each stream is right on its own, but the combination is meaningless. The simulation below counts such combinations for three ways of holding state. [[src:ax-ui-layer]]')

    S_ = 'mvvm'
    a(C + '.sec.%s.title' % S_, 'MVVM trên Android', 'MVVM on Android')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'p', 'MVVM (Model, View, ViewModel) là một cách tách logic ra khỏi Activity và Fragment, như Alexandru Dumbravan mô tả. View (Activity, Fragment hay composable) phụ thuộc ViewModel, ViewModel phụ thuộc Model; quan hệ một chiều nên nhiều View dùng chung một ViewModel được. Để View cập nhật, ViewModel lộ dữ liệu dưới dạng quan sát được và View đăng ký theo dõi. Lớp ViewModel của Android Jetpack còn giải quyết chuyện vòng đời của Activity.\nQuy tắc dễ nhớ: View biết ViewModel, ViewModel không biết View nào đang nhìn nó. [[src:book-dumbravan]]',
      'MVVM (Model, View, ViewModel) is a way to pull logic out of Activities and Fragments, as Alexandru Dumbravan describes it. The View (Activity, Fragment or composable) depends on the ViewModel, the ViewModel on the Model; the relationship is one-way, so several Views can share a ViewModel. For the View to update, the ViewModel exposes observable data and the View subscribes. The Android Jetpack ViewModel class also handles the Activity lifecycle.\nRule of thumb: the View knows the ViewModel; the ViewModel does not know which View is looking at it. [[src:book-dumbravan]]')
    B(C, S_, 2, 'p', 'Hướng dẫn chính thức chính là MVVM cộng với các quy tắc của G2 và G3: UI state bất biến, sự kiện đi lên, state đi xuống. Câu hỏi còn lại của chương này là: giữ state trong một hay nhiều luồng, và kiểu của state cho phép những gì. [[src:ax-ui-layer]]',
      'The official guide is essentially MVVM plus the rules of G2 and G3: immutable UI state, events up, state down. The question left for this chapter is: hold state in one stream or several, and what does the state\'s type allow. [[src:ax-ui-layer]]')

    S_ = 'single'
    a(C + '.sec.%s.title' % S_, 'Một luồng hay nhiều luồng state', 'One state stream or several')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'p', 'Tài liệu khuyên dùng một UI state cho các state liên quan nhau: ít lệch hơn và mã dễ hiểu hơn. Nếu danh sách tin và số tin đã đánh dấu nằm ở hai luồng, có lúc một luồng đã cập nhật còn luồng kia chưa. Một luồng thì người dùng state luôn có thông tin mới nhất, và các thuộc tính suy ra (như "có hiện nút đánh dấu không") tính được từ mọi trường cùng lúc. [[src:ax-ui-layer]]',
      'The docs advise a single UI state for related states: fewer inconsistencies and easier code. If the news list and the bookmark count live in two streams, one may be updated while the other is not. With one stream, consumers always have the latest information, and derived properties (such as "show the bookmark button?") can be computed from all fields at once. [[src:ax-ui-layer]]')
    B(C, S_, 2, 'p', 'Tách luồng vẫn có chỗ dùng: khi các phần hoàn toàn không liên quan, hay một phần đổi rất thường xuyên so với phần kia. Một UiState nhiều trường sẽ phát lại mỗi khi một trường đổi, nên đôi khi cần distinctUntilChanged() ở phía dùng. [[src:ax-ui-layer]]',
      'Separate streams still have a place: when the pieces are completely unrelated, or one changes far more often than the other. A UiState with many fields emits whenever any field changes, so sometimes distinctUntilChanged() is needed on the consuming side. [[src:ax-ui-layer]]')
    B(C, S_, 3, 'note', 'Một data class gồm Boolean và trường nullable vẫn có 8 tổ hợp, kể cả tổ hợp vô nghĩa. Gộp vào một luồng giảm lỗi do cập nhật lệch nhau, không loại được tổ hợp sai do viết nhầm.', 'A data class of a Boolean and nullable fields still has 8 combinations, meaningless ones included. One stream removes bugs from out-of-step updates, not wrong combinations written by mistake.')
    B(C, S_, 3, 'kind', 'pitfall')

    S_ = 'mvi'
    a(C + '.sec.%s.title' % S_, 'MVI: intent, reducer, một state', 'MVI: intents, a reducer, one state')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'p', 'Alexandru Dumbravan đặt vấn đề: màn hình có nhiều trường thay đổi, giữ chúng bằng các biến sửa được thì dễ sai khi có thao tác chạy đồng thời hay về sai thứ tự. MVI (Model, View, Intent) gộp dữ liệu bất biến thành một state mà UI quan sát; mọi thay đổi (từ người dùng hay từ app) đi qua một luồng dữ liệu tạo ra state mới. Intent ở đây là ý định của người dùng, không phải lớp Intent của Android. MVI không thay ViewModel mà xây trên nó.\nHình dung: reducer giống máy bán nước. Cùng trạng thái máy, cùng đồng xu bỏ vào, thì luôn ra cùng một kết quả. [[src:book-dumbravan]]',
      'Alexandru Dumbravan frames the problem: a screen with many changing fields, held in changeable variables, goes wrong when operations run at the same time or arrive out of order. MVI (Model, View, Intent) combines immutable data into one state the UI observes; every change (from the user or the app) goes through a data flow that produces a new state. Intent here means what the user wants, not Android\'s Intent class. MVI does not replace the ViewModel; it builds on it.\nPicture a vending machine as the reducer: the same machine state and the same coin always give the same result. [[src:book-dumbravan]]')
    B(C, S_, 2, 'kt', 'sealed interface ApptState {\n    data object Loading : ApptState\n    data class Content(val items: List<Appt>) : ApptState\n    data class Refreshing(val items: List<Appt>) : ApptState\n    data class Error(val message: String) : ApptState\n}\nfun reduce(state: ApptState, result: ApptResult): ApptState = when (result) {\n    is ApptResult.Loaded -> ApptState.Content(result.items)\n    is ApptResult.Failed -> ApptState.Error(result.message)\n}',
      'sealed interface ApptState {\n    data object Loading : ApptState\n    data class Content(val items: List<Appt>) : ApptState\n    data class Refreshing(val items: List<Appt>) : ApptState\n    data class Error(val message: String) : ApptState\n}\nfun reduce(state: ApptState, result: ApptResult): ApptState = when (result) {\n    is ApptResult.Loaded -> ApptState.Content(result.items)\n    is ApptResult.Failed -> ApptState.Error(result.message)\n}')
    B(C, S_, 3, 'p', 'Hai thứ MVI mang lại. Kiểu sealed chỉ có các trạng thái có nghĩa, nên "đang tải mà cũng lỗi" không viết ra được, và when phải xử lý đủ các nhánh (track Kotlin K5). Reducer là hàm thuần, test bằng bảng: state cũ, kết quả, state mới mong đợi. Cái giá là nhiều kiểu hơn (intent, result, state) và mã chuyển đổi; với màn đơn giản, một UiState của MVVM thường đủ. Đây là đánh đổi theo quan điểm của Alexandru Dumbravan, không phải quy định của Google.',
      'MVI brings two things. A sealed type has only meaningful states, so "loading and erroring" cannot be written, and when must handle every branch (Kotlin track K5). The reducer is a pure function, tested with a table: old state, result, expected new state. The cost is more types (intent, result, state) and mapping code; for a simple screen, an MVVM UiState is usually enough. This is Alexandru Dumbravan\'s trade-off, not a Google rule.')

    S_ = 'bugs'
    a(C + '.sec.%s.title' % S_, 'Hai lỗi hay gặp', 'Two common bugs')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'bug', 'Màn Lịch của tôi vừa hiện vòng xoay vừa hiện "Mất mạng", không ai bấm được gì.', 'My appointments shows a spinner and "Offline" at once, and nothing can be tapped.')
    B(C, S_, 1, 'cause', 'isLoading và error là hai StateFlow riêng; nhánh lỗi chỉ cập nhật một trong hai.', 'isLoading and error are separate StateFlows; the error branch updates only one of them.')
    B(C, S_, 1, 'fix', 'Gộp vào một UiState và đổi cả hai trong một lần copy; tốt hơn, dùng sealed state để tổ hợp đó không tồn tại.', 'Merge into one UiState and change both in one copy; better, use a sealed state so that combination does not exist.')
    B(C, S_, 2, 'bug', 'Sau khi thử lại thành công, danh sách vẫn kèm dòng "Mất mạng".', 'After a successful retry, the list still carries the "Offline" banner.')
    B(C, S_, 2, 'cause', 'Không có chỗ nào xóa error khi bắt đầu tải lại; trường cũ sống sót qua lần cập nhật mới.', 'Nothing clears error when the reload starts; the old field survives the new update.')
    B(C, S_, 2, 'fix', 'Xóa lỗi cùng lúc bật đang tải; với sealed state, Loading không có trường lỗi nên lỗi tự mất.', 'Clear the error when turning loading on; with a sealed state, Loading has no error field, so the error disappears by itself.')

    S_ = 'ex'
    a(C + '.sec.%s.title' % S_, 'Bài tập', 'Exercise')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'ex', 'Viết bảng test cho reduce(state, result) của ApptState: ít nhất bốn hàng (state cũ, kết quả, state mới mong đợi). Thêm một intent Refresh khi đang có danh sách: nó nên đưa về Refreshing(items) thay vì Loading. Viết nhánh mới cho reducer. [[src:book-dumbravan]]',
      'Write a test table for ApptState\'s reduce(state, result): at least four rows (old state, result, expected new state). Add a Refresh intent while a list is shown: it should lead to Refreshing(items) instead of Loading. Write the new reducer branch. [[src:book-dumbravan]]')
    B(C, S_, 1, 'hint', 'Khi làm mới, state cũ là Content(items): giữ items lại trong Refreshing để màn hình không trống.', 'When refreshing, the old state is Content(items): keep the items in Refreshing so the screen does not go blank.')
    B(C, S_, 1, 'sol', 'Bảng: (Loading, Loaded(a)) → Content(a); (Loading, Failed(m)) → Error(m); (Refreshing(a), Loaded(b)) → Content(b); (Refreshing(a), Failed(m)) → Content(a) và một thông báo lỗi tạm (G3), để không mất danh sách. Khi nhận Refresh trong Content(items): state = Refreshing(items).',
      'Table: (Loading, Loaded(a)) → Content(a); (Loading, Failed(m)) → Error(m); (Refreshing(a), Loaded(b)) → Content(b); (Refreshing(a), Failed(m)) → Content(a) plus a transient error message (G3), so the list is not lost. On Refresh while in Content(items): state = Refreshing(items).')

    S_ = 'recall'
    a(C + '.sec.%s.title' % S_, 'Tự trả lời', 'Answer it yourself')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'ask', 'Vì sao ba StateFlow riêng có thể làm màn hình vừa tải vừa lỗi?', 'Why can three separate StateFlows make the screen load and error at once?')
    B(C, S_, 1, 'ans', 'Mỗi luồng cập nhật riêng; một nhánh mã có thể đổi luồng này mà quên luồng kia.', 'Each stream updates separately; one code path can change one stream and forget the other.')
    B(C, S_, 2, 'ask', 'MVI chặn tổ hợp sai bằng cách nào?', 'How does MVI rule out wrong combinations?')
    B(C, S_, 2, 'ans', 'State là sealed interface chỉ có các trạng thái có nghĩa, và mọi thay đổi đi qua reducer.', 'The state is a sealed interface with only meaningful states, and every change goes through the reducer.')

    for q, qv, qe, av, ae, wv, we in [
        ('q1', 'Tài liệu khuyên gì cho các state liên quan nhau?', 'What do the docs advise for related pieces of state?', 'Gộp vào một UI state.', 'Merge them into one UI state.', 'Ít lệch hơn, mã dễ hiểu hơn.', 'Fewer inconsistencies, easier code.'),
        ('q2', 'Khi nào tách nhiều luồng state là hợp lý?', 'When are several state streams reasonable?', 'Khi các phần không liên quan, hay đổi với tần suất rất khác nhau.', 'When the pieces are unrelated, or change at very different rates.', 'Theo mục single stream or multiple streams của trang UI layer.', 'Per the single-or-multiple-streams note on the UI layer page.'),
        ('q3', 'Intent trong MVI có phải android.content.Intent không?', 'Is the Intent in MVI android.content.Intent?', 'Không; nó là ý định của người dùng.', 'No; it is what the user wants.', 'Dumbravan ghi chú rõ điểm này.', 'Dumbravan calls this out explicitly.'),
        ('q4', 'Vì sao reducer dễ test?', 'Why is a reducer easy to test?', 'Vì nó là hàm thuần: cùng đầu vào, cùng đầu ra.', 'Because it is a pure function: same input, same output.', 'Test bằng bảng state cũ, kết quả, state mới.', 'Test with a table of old state, result, new state.')]:
        a(C + '.quiz.%s.q' % q, qv, qe); a(C + '.quiz.%s.a' % q, av, ae); a(C + '.quiz.%s.why' % q, wv, we)
