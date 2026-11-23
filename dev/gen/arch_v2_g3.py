# Kiến trúc · G3: UI layer: UiState, ViewModel, sự kiện (Phần 1)
# Nguồn: developer.android.com UI layer, UI events, State holders (đọc 2026-11-24);
# kotlinx.coroutines API 1.11.0: StateFlow (phát lại giá trị mới nhất cho subscriber mới), SharedFlow/MutableSharedFlow
# (không có subscriber thì chỉ giữ replay; MutableSharedFlow() không replay, emit trả về ngay khi không có subscriber).
# Trần: 8 mục, mục cơ chế ≤ 4 khối.

SEC_ORDER = {'g3': ['hook', 'uistate', 'events', 'oneoff', 'bugs', 'ex', 'recall', 'honest']}


def add(a):
    def B(ch, sec, n, field, vi, en=None):
        a('%s.sec.%s.b.%02d.%s' % (ch, sec, n, field), vi, vi if en is None else en)

    m = lambda k, vi, en=None: a('m.events.' + k, vi, en)
    m('title', 'Thông báo "Đã đặt lịch" qua một lần xoay màn hình', 'The "Booked" message through a screen rotation')
    m('overview', 'Bấm "Đặt lịch", ViewModel gọi repository rồi báo cho màn hình hiện thông báo "Đã đặt lịch 9:00". Ngay sau đó người dùng xoay điện thoại: Activity cũ bị hủy, Activity mới được tạo, ViewModel vẫn còn. Ba cách báo: (1) cờ showSuccess trong StateFlow không ai xóa; (2) sự kiện qua MutableSharedFlow(); (3) thông báo là một phần của UI state, UI báo lại khi đã hiện xong.',
      'Tap "Book": the ViewModel calls the repository, then tells the screen to show "Booked for 9:00". Right after, the user rotates the phone: the old Activity is destroyed, a new one is created, the ViewModel survives. Three ways to deliver the message: (1) a showSuccess flag in a StateFlow that nobody clears; (2) an event through MutableSharedFlow(); (3) the message as part of the UI state, with the UI reporting back once it has been shown.')
    m('wrapup', 'Thông báo hiện lại vì StateFlow phát lại giá trị mới nhất cho Activity mới; thông báo mất vì SharedFlow không replay bỏ giá trị khi lúc đó không ai thu thập. Hướng dẫn chính thức chọn cách thứ ba: sự kiện từ ViewModel luôn thành một cập nhật UI state, và việc UI đã hiện thông báo cũng là một sự kiện gửi ngược lên để xóa nó. Nhờ vậy thông báo hiện đúng một lần, kể cả khi xoay màn hình trước lúc kịp hiện.',
      'The message repeats because StateFlow replays its latest value to the new Activity; it is lost because a SharedFlow without replay drops the value when nobody is collecting at that moment. The official guide picks the third way: an event from the ViewModel always becomes a UI state update, and the UI having shown the message is itself an event sent back up to clear it. The message then shows exactly once, even if the screen rotates before it could be shown.')
    m('simp.1', 'Activity, ViewModel và kênh được rút còn vài dòng; app thật thu thập trong repeatOnLifecycle(STARTED) (track Coroutines A8). Thời điểm xoay và lúc request xong được đặt sẵn để thấy rõ từng trường hợp.', 'The Activity, ViewModel and channel are cut to a few lines; a real app collects inside repeatOnLifecycle(STARTED) (Coroutines track A8). The rotation and the moment the request finishes are placed on purpose to show each case.')
    m('simp.2', 'Hành vi của StateFlow và SharedFlow theo tài liệu API kotlinx.coroutines 1.11.0; MutableSharedFlow có buffer hay replay sẽ khác (chương nói ở mục "Sự kiện một lần").', 'StateFlow and SharedFlow behaviour follows the kotlinx.coroutines 1.11.0 API docs; a MutableSharedFlow with a buffer or replay behaves differently (see the "One-off events" section).')
    m('ctl.hint', 'Đổi cách báo rồi đi lại bốn bước; xem tab "Làn thời gian".', 'Switch the delivery approach and walk the four steps again; watch the "Timeline lanes" tab.')
    m('ctl.case', 'Cách báo thông báo', 'How the message is delivered')
    for k, vi, en in [('sticky', 'cờ trong StateFlow, không xóa', 'a flag in StateFlow, never cleared'), ('shared', 'sự kiện qua MutableSharedFlow()', 'an event through MutableSharedFlow()'), ('state', 'thông báo trong UI state, UI báo đã hiện', 'the message in UI state, the UI reports it shown')]:
        m('ctl.case.' + k, vi, en)
    m('diagramTitle', 'Activity, ViewModel, kênh, người dùng', 'Activity, ViewModel, channel, user')
    m('diagramDesc', 'Bấm đi từ Activity lên ViewModel; state hay sự kiện đi qua kênh về Activity; Activity hiện thông báo', 'A tap goes from the Activity up to the ViewModel; state or an event comes back through the channel; the Activity shows the message')
    for k, vi, en in [('act', 'Activity đang hiển thị', 'Visible Activity'), ('vm', 'BookingViewModel', 'BookingViewModel'), ('flow', 'Kênh (StateFlow / SharedFlow)', 'Channel (StateFlow / SharedFlow)'), ('toast', 'Thông báo người dùng thấy', 'Message the user sees')]:
        m('n.' + k, vi, en)
    m('met.shown', 'Số lần thông báo hiện', 'Times the message showed'); m('met.lost', 'Thông báo bị mất', 'Message lost'); m('met.truth', 'Thông báo nằm ở đâu', 'Where the message lives')
    for k, vi, en in [('na', 'chưa biết', 'not yet'), ('no', 'không', 'no'), ('yes', 'có', 'yes')]:
        m('lost.' + k, vi, en)
    for k, vi, en in [('flag', 'cờ trong state, không ai xóa', 'a state flag nobody clears'), ('stream', 'luồng sự kiện không replay', 'an event stream without replay'), ('state', 'UI state, có hàm xóa', 'UI state, with a clear function')]:
        m('truth.' + k, vi, en)
    a('cap.events', 'Vòng: Activity gửi cú bấm lên ViewModel, ViewModel đưa state hay sự kiện vào kênh, kênh đưa về Activity, Activity hiện thông báo. Khối viền đỏ là chỗ thông báo bị lặp hay bị mất. Tab "Làn thời gian" cho thấy Activity cũ và mới theo từng bước.',
      'A loop: the Activity sends the tap up to the ViewModel, the ViewModel puts state or an event into the channel, the channel brings it back to the Activity, the Activity shows the message. A red-outlined box is where the message repeats or gets lost. The "Timeline lanes" tab shows the old and new Activity step by step.')
    S = [
        ('sticky', 's1', 'Bấm Đặt: ViewModel bật cờ showSuccess', 'Tap Book: the ViewModel sets showSuccess',
         'repo.book() xong, ViewModel đặt showSuccess = true trong StateFlow. Activity đang thu thập nhận state mới và hiện Toast "Đã đặt lịch 9:00". Không ai đặt cờ về false.',
         'repo.book() finishes and the ViewModel sets showSuccess = true in its StateFlow. The collecting Activity receives the new state and shows the Toast "Booked for 9:00". Nobody sets the flag back to false.'),
        ('sticky', 's2', 'Xoay màn hình: Activity mới, ViewModel cũ', 'Rotate: a new Activity, the same ViewModel',
         'Hệ thống hủy Activity và tạo lại. ViewModel sống qua lần tái tạo này nên state vẫn còn nguyên, kể cả showSuccess = true.',
         'The system destroys and recreates the Activity. The ViewModel survives the recreation, so its state is intact, showSuccess = true included.'),
        ('sticky', 's3', 'Activity mới thu thập: Toast hiện lần nữa', 'The new Activity collects: the Toast shows again',
         'StateFlow phát lại giá trị mới nhất cho subscriber mới. Activity mới nhận state có showSuccess = true và hiện Toast lần thứ hai, dù người dùng không đặt thêm lịch nào.',
         'StateFlow replays its latest value to a new subscriber. The new Activity receives the state with showSuccess = true and shows the Toast a second time, although the user booked nothing new.'),
        ('sticky', 's4', 'Mỗi lần đổi cấu hình lại hiện', 'It repeats on every configuration change',
         'Xoay lại, đổi cỡ chữ, chuyển sáng/tối: mỗi lần Activity được tạo lại, thông báo "Đã đặt lịch" lại hiện. Lỗi nằm ở chỗ thông báo được giữ như một trạng thái kéo dài mãi.',
         'Rotate again, change the font size, switch light/dark: every time the Activity is recreated, "Booked" shows again. The bug is that the message is kept as a state that lasts forever.'),
        ('shared', 's1', 'Bấm Đặt: request đang chạy', 'Tap Book: the request is running',
         'ViewModel gọi repo.book() trong viewModelScope. Khi xong nó sẽ emit "booked" vào một MutableSharedFlow() không replay, không buffer.',
         'The ViewModel calls repo.book() in viewModelScope. When done it will emit "booked" into a MutableSharedFlow() with no replay and no buffer.'),
        ('shared', 's2', 'Xoay giữa chừng: chưa ai thu thập', 'Rotate midway: nobody is collecting',
         'Activity cũ đã bị hủy nên ngừng thu thập; Activity mới chưa tới lúc bắt đầu thu thập. Có một khoảng ngắn luồng sự kiện không có subscriber nào.',
         'The old Activity is destroyed and stops collecting; the new one has not started collecting yet. For a short window the event stream has no subscriber.'),
        ('shared', 's3', 'Request xong đúng lúc đó: emit bị bỏ', 'The request finishes right then: the emit is dropped',
         'Với MutableSharedFlow() không replay, emit khi không có subscriber trả về ngay và giá trị không được lưu ở đâu. Sự kiện "booked" biến mất.',
         'With a MutableSharedFlow() without replay, emitting with no subscribers returns at once and the value is not stored anywhere. The "booked" event is gone.'),
        ('shared', 's4', 'Activity mới không nhận gì: người dùng đặt lại', 'The new Activity receives nothing: the user books again',
         'Activity mới bắt đầu thu thập nhưng sự kiện đã qua. Người dùng không thấy xác nhận, tưởng chưa đặt được, bấm lại và có hai lịch.',
         'The new Activity starts collecting but the event is already gone. The user sees no confirmation, thinks the booking failed, taps again and ends up with two appointments.'),
        ('state', 's1', 'Bấm Đặt: thông báo vào UI state', 'Tap Book: the message goes into UI state',
         'repo.book() xong, ViewModel đặt userMessage = "Đã đặt lịch 9:00" trong UI state. Màn hình thấy userMessage khác null nên hiện Snackbar.',
         'repo.book() finishes and the ViewModel sets userMessage = "Booked for 9:00" in UI state. The screen sees a non-null userMessage and shows a Snackbar.'),
        ('state', 's2', 'Hiện xong: UI báo lại, ViewModel xóa', 'Shown: the UI reports back, the ViewModel clears it',
         'Khi Snackbar đóng, UI gọi vm.messageShown(). Đây là một sự kiện người dùng như mọi sự kiện khác: ViewModel cập nhật state, userMessage = null.',
         'When the Snackbar closes, the UI calls vm.messageShown(). This is a user event like any other: the ViewModel updates state, userMessage = null.'),
        ('state', 's3', 'Xoay màn hình: không hiện lại', 'Rotate: nothing repeats',
         'Activity mới nhận state hiện tại từ StateFlow, nhưng state đó không còn userMessage. Màn hình đúng với những gì đang có: không có thông báo nào đang chờ.',
         'The new Activity receives the current state from the StateFlow, but that state has no userMessage. The screen matches what is true: no message is pending.'),
        ('state', 's4', 'Biến thể: xoay trước khi kịp hiện', 'Variant: rotate before it could show',
         'Nếu xoay ngay khi userMessage vừa được đặt, Activity cũ chưa kịp hiện thì bị hủy. Thông báo vẫn nằm trong state, nên Activity mới nhận và hiện đúng một lần, rồi báo messageShown().',
         'If the rotation happens right after userMessage is set, the old Activity is destroyed before showing it. The message is still in state, so the new Activity receives it, shows it exactly once, then reports messageShown().'),
    ]
    for case, k, tv, te, xv, xe in S:
        sid = case + '.' + k
        m('s.%s.title' % sid, tv, te); m('s.%s.explain' % sid, xv, xe); m('ev.' + sid, tv, te)
    for k, vi, en in [
        ('try', 'Đi bốn bước của từng cách báo; đếm số lần thông báo hiện ở bước cuối.', 'Walk the four steps of each approach; count how often the message showed at the last step.'),
        ('sticky.s2', 'State holders: ViewModel giữ state và các thao tác qua việc Activity bị tạo lại. [[src:ax-stateholders]]', 'State holders: a ViewModel keeps its state and operations across Activity recreation. [[src:ax-stateholders]]'),
        ('sticky.s3', 'kotlinx.coroutines 1.11.0: StateFlow luôn có giá trị và phát lại một giá trị mới nhất cho subscriber mới. [[src:kx-stateflow-api]]', 'kotlinx.coroutines 1.11.0: a StateFlow always has a value and replays the most recent one to new subscribers. [[src:kx-stateflow-api]]'),
        ('sticky.s4', 'Cờ "đã thành công" là một sự kiện bị giữ như trạng thái kéo dài. Cách sửa không phải bỏ state, mà là cho UI báo lại để xóa nó (cách thứ ba).', 'A "succeeded" flag is an event held as a lasting state. The fix is not to drop state, but to let the UI report back and clear it (the third approach).'),
        ('shared.s2', 'UI events: khi ViewModel sống lâu hơn UI (như lúc xoay), Channel và các stream khác không bảo đảm sự kiện được giao và xử lý. [[src:ax-ui-events]]', 'UI events: when the ViewModel outlives the UI (as during rotation), Channels and other streams do not guarantee the event is delivered and processed. [[src:ax-ui-events]]'),
        ('shared.s3', 'kotlinx.coroutines 1.11.0: MutableSharedFlow() không replay, không buffer; emit trả về ngay nếu không có subscriber. Khi vắng subscriber chỉ các giá trị replay được giữ. [[src:kx-sharedflow]]', 'kotlinx.coroutines 1.11.0: MutableSharedFlow() has no replay or buffer; emit returns immediately when there are no subscribers. In the absence of subscribers only replay values are kept. [[src:kx-sharedflow]]'),
        ('shared.s4', 'Đây là lý do tài liệu gọi việc mất sự kiện là trải nghiệm không chấp nhận được: người dùng có thể bỏ lỡ thông tin quan trọng hay để app ở trạng thái không nhất quán. [[src:ax-ui-events]]', 'This is why the docs call losing events an unacceptable experience: the user may miss critical information or leave the app in an inconsistent state. [[src:ax-ui-events]]'),
        ('state.s2', 'UI events: việc người dùng đã xem thông báo (đóng nó hay hết giờ) được coi là đầu vào của người dùng, và ViewModel cần biết để cập nhật state. [[src:ax-ui-events]]', 'UI events: the user having consumed the message (dismissing it or after a timeout) is treated as user input, and the ViewModel needs to know so it can update state. [[src:ax-ui-events]]'),
        ('state.s3', 'Dù thông báo chỉ thoáng qua, UI state vẫn mô tả đúng màn hình ở mọi thời điểm: thông báo đang hiện, hoặc không. [[src:ax-ui-events]]', 'Even though the message is transient, the UI state faithfully describes the screen at every point: the message is shown, or it is not. [[src:ax-ui-events]]'),
        ('state.s4', 'Tài liệu: đưa sự kiện của ViewModel thành UI state giúp sự kiện tái hiện được sau thay đổi cấu hình và bảo đảm hành động UI không bị mất; muốn sống qua cả process death thì dùng SavedStateHandle. [[src:ax-ui-events]]', 'Docs: turning ViewModel events into UI state makes them reproducible after configuration changes and guarantees UI actions are not lost; to survive process death as well, use SavedStateHandle. [[src:ax-ui-events]]')]:
        m('co.' + k, vi, en)
    a('preset.events', 'Kiến trúc · thông báo một lần qua lần xoay màn hình', 'Architecture · a one-off message through a rotation')

    z = lambda k, vi, en=None: a('vz.' + k, vi, en)
    z('tab.ev', 'Làn thời gian', 'Timeline lanes')
    z('ev.cap', 'Mỗi hàng là một làn: Activity trước khi xoay, ViewModel, Activity sau khi xoay, và điều người dùng thấy. Mỗi cột là một bước; cột của bước đang xem được tô.', 'Each row is a lane: the Activity before rotating, the ViewModel, the Activity after rotating, and what the user sees. Each column is a step; the current step\'s column is highlighted.')
    z('ev.legend', 'Ô đỏ: thông báo bị lặp hay bị mất. Ô mờ: làn đó chưa tồn tại hay đã bị hủy.', 'Red cell: the message repeats or is lost. Faded cell: that lane does not exist yet or was destroyed.')
    z('ev.lane', 'Làn', 'Lane')
    for k, vi, en in [('a1', 'Activity lần 1', 'Activity #1'), ('vm', 'ViewModel', 'ViewModel'), ('a2', 'Activity lần 2 (sau xoay)', 'Activity #2 (after rotating)'), ('user', 'Người dùng thấy', 'User sees')]:
        z('ev.lane.' + k, vi, en)
    cols = {
        'sticky': [('Bấm Đặt', 'Tap Book'), ('Xoay', 'Rotate'), ('Thu thập lại', 'Collect again'), ('Xoay lần nữa', 'Rotate again')],
        'shared': [('Bấm Đặt', 'Tap Book'), ('Xoay giữa chừng', 'Rotate midway'), ('Request xong', 'Request done'), ('Activity mới thu thập', 'New Activity collects')],
        'state': [('Bấm Đặt', 'Tap Book'), ('Hiện xong, báo lại', 'Shown, reported'), ('Xoay', 'Rotate'), ('Biến thể: xoay sớm', 'Variant: early rotate')],
    }
    for c, lst in cols.items():
        for k, (vi, en) in enumerate(lst):
            z('ev.col.%s.%d' % (c, k), vi, en)
    for k, vi, en in [
        ('tap', 'bấm Đặt, gọi vm.book()', 'tap Book, call vm.book()'), ('none', 'chưa có', 'not created'), ('destroyed', 'đã bị hủy', 'destroyed'),
        ('created', 'vừa được tạo', 'just created'), ('collect', 'thu thập StateFlow: nhận showSuccess = true', 'collects the StateFlow: gets showSuccess = true'),
        ('rotateAgain', 'lại bị tạo mới, lại nhận showSuccess = true', 'recreated again, gets showSuccess = true again'),
        ('setMsg', 'đặt thông báo "Đã đặt lịch"', 'sets the "Booked" message'), ('keepMsg', 'vẫn giữ showSuccess = true', 'still holds showSuccess = true'),
        ('replay', 'StateFlow phát lại giá trị mới nhất', 'StateFlow replays the latest value'), ('request', 'repo.book() đang chạy', 'repo.book() running'),
        ('emitNoSub', 'emit("booked") lúc không có subscriber: bị bỏ', 'emit("booked") with no subscriber: dropped'), ('emptyFlow', 'luồng sự kiện trống', 'the event stream is empty'),
        ('notYet', 'chưa thu thập', 'not collecting yet'), ('collectNothing', 'thu thập: không nhận gì', 'collects: receives nothing'),
        ('shownCall', 'Snackbar đóng, gọi vm.messageShown()', 'Snackbar closed, calls vm.messageShown()'), ('cleared', 'đặt userMessage = null', 'sets userMessage = null'),
        ('noMsg', 'state không có thông báo', 'state has no message'), ('collectClean', 'thu thập: không có thông báo', 'collects: no message'),
        ('pendingMsg', 'userMessage vẫn chờ (chưa ai hiện)', 'userMessage still pending (not shown yet)'), ('collectPending', 'thu thập: nhận thông báo đang chờ', 'collects: gets the pending message'),
        ('toast1', 'thấy "Đã đặt lịch 9:00"', 'sees "Booked for 9:00"'), ('toast2', 'thấy lại lần 2', 'sees it a 2nd time'), ('toast3', 'thấy lại lần 3', 'sees it a 3rd time'),
        ('toastOnce', 'thấy đúng một lần', 'sees it exactly once'), ('nothing', 'không có gì', 'nothing'), ('waiting', 'đang chờ', 'waiting'),
        ('bookAgain', 'không thấy xác nhận, bấm Đặt lần nữa', 'no confirmation, taps Book again')]:
        z('ev.cell.' + k, vi, en)

    C = 'g3'
    a(C + '.title', 'UI layer: UiState, ViewModel và sự kiện', 'The UI layer: UiState, ViewModel and events')
    a(C + '.essence', 'UI state là bản chụp bất biến của mọi thứ màn hình cần hiển thị; ViewModel giữ và tạo ra nó, và sống qua việc Activity bị tạo lại.\nSự kiện từ người dùng đi lên ViewModel; sự kiện từ ViewModel (đặt xong, lỗi, điều hướng) phải thành một cập nhật UI state, không phải một tin nhắn bắn đi rồi quên.\nThông báo thoáng qua cũng là state: UI hiện nó, rồi báo lại cho ViewModel để xóa. Nhờ vậy nó không lặp lại sau khi xoay màn hình và không bị mất khi chưa ai thu thập.',
      'UI state is an immutable snapshot of everything the screen needs to display; the ViewModel holds and produces it, and survives Activity recreation.\nUser events go up to the ViewModel; events from the ViewModel (booked, error, navigate) must become a UI state update, not a message fired and forgotten.\nA transient message is state too: the UI shows it, then reports back to the ViewModel to clear it. It then neither repeats after rotation nor gets lost when nobody is collecting.')
    a(C + '.goal.g1', 'Đã thấy thông báo hiện lại sau khi xoay', 'Saw the message show again after rotating')
    a(C + '.goal.g2', 'Đã đi hết bốn bước', 'Walked all four steps')
    a(C + '.sim.arch.events', 'thông báo một lần qua lần xoay màn hình', 'a one-off message through a rotation')

    S_ = 'hook'
    a(C + '.sec.%s.title' % S_, 'Đoán trước khi đọc', 'Predict before reading')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'predict', 'ViewModel đặt showSuccess = true trong một StateFlow sau khi đặt lịch xong; Activity thu thập và hiện Toast khi thấy true. Người dùng xoay điện thoại. Toast có hiện lần nữa không?',
      'After booking, the ViewModel sets showSuccess = true in a StateFlow; the Activity collects it and shows a Toast when it sees true. The user rotates the phone. Does the Toast show again?')
    B(C, S_, 1, 'ans', 'Có. ViewModel sống qua lần xoay nên state vẫn có showSuccess = true, và StateFlow phát lại giá trị mới nhất cho Activity mới vừa bắt đầu thu thập. Mô phỏng bên dưới so cách này với hai cách khác. [[src:kx-stateflow-api]]',
      'Yes. The ViewModel survives the rotation, so its state still has showSuccess = true, and StateFlow replays its latest value to the new Activity that just started collecting. The simulation below compares this with two other approaches. [[src:kx-stateflow-api]]')

    S_ = 'uistate'
    a(C + '.sec.%s.title' % S_, 'UI state và state holder', 'UI state and its state holder')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'p', 'Vai trò của tầng UI là hiển thị dữ liệu của app và là điểm tương tác chính với người dùng. Tầng UI gồm phần tử UI (View hay hàm Compose) và state holder (ví dụ ViewModel) giữ dữ liệu, lộ nó cho UI và xử lý logic. UI state nên là kiểu bất biến, để chỉ một nơi được đổi nó và màn hình luôn khớp với một bản chụp nhất quán. [[src:ax-ui-layer]]',
      'The UI layer\'s role is to display the app\'s data and to be the main point of user interaction. It consists of UI elements (Views or Compose functions) and state holders (such as a ViewModel) that hold data, expose it to the UI and handle logic. UI state should be an immutable type, so that only one place changes it and the screen always matches one consistent snapshot. [[src:ax-ui-layer]]')
    B(C, S_, 2, 'p', 'ViewModel là cách được khuyến nghị để quản lý UI state ở mức màn hình khi cần truy cập tầng data, và nó tự sống qua thay đổi cấu hình. State holder bằng ViewModel giữ state và các thao tác đang chạy qua việc Activity bị tạo lại; khi tiến trình bị hệ thống giết, SavedStateHandle giữ phần dữ liệu tối thiểu để khôi phục. [[src:ax-ui-layer]] [[src:ax-stateholders]]',
      'ViewModel is the recommended way to manage screen-level UI state with access to the data layer, and it survives configuration changes automatically. A ViewModel state holder keeps state and running operations across Activity recreation; when the process is killed, SavedStateHandle keeps the minimum data needed to restore. [[src:ax-ui-layer]] [[src:ax-stateholders]]')
    B(C, S_, 3, 'kt', 'data class BookingUiState(\n    val slots: List<Slot> = emptyList(),\n    val isLoading: Boolean = false,\n    val userMessage: String? = null,      // thông báo thoáng qua cũng là state\n)\nclass BookingViewModel(private val repo: BookingRepository) : ViewModel() {\n    private val _state = MutableStateFlow(BookingUiState())\n    val state: StateFlow<BookingUiState> = _state     // UI chỉ đọc\n}',
      'data class BookingUiState(\n    val slots: List<Slot> = emptyList(),\n    val isLoading: Boolean = false,\n    val userMessage: String? = null,      // a transient message is state too\n)\nclass BookingViewModel(private val repo: BookingRepository) : ViewModel() {\n    private val _state = MutableStateFlow(BookingUiState())\n    val state: StateFlow<BookingUiState> = _state     // the UI only reads\n}')

    S_ = 'events'
    a(C + '.sec.%s.title' % S_, 'Sự kiện UI và sự kiện từ ViewModel', 'UI events and ViewModel events')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'p', 'Tài liệu chia hai loại. Sự kiện UI là hành động xử lý ngay ở tầng UI, như mở rộng một mục hay điều hướng do người dùng bấm. Sự kiện cần business logic (lưu, đặt lịch, làm mới) thì UI chuyển lên ViewModel; ViewModel quyết định và cập nhật state. [[src:ax-ui-events]]',
      'The docs distinguish two kinds. UI events are actions handled right in the UI layer, such as expanding an item or navigating because the user tapped. Events that need business logic (save, book, refresh) are passed up by the UI to the ViewModel, which decides and updates state. [[src:ax-ui-events]]')
    B(C, S_, 2, 'p', 'Quy tắc quan trọng nhất: sự kiện phát ra từ ViewModel luôn phải thành một cập nhật UI state. Đừng nghĩ "UI cần làm hành động gì", mà nghĩ "hành động đó làm UI state thay đổi ra sao". Ví dụ màn đăng nhập: không gửi lệnh "điều hướng", mà đặt isUserLoggedIn = true; UI thấy state đó thì tự điều hướng. [[src:ax-ui-events]]',
      'The most important rule: events originating from the ViewModel must always result in a UI state update. Do not think "what action must the UI take"; think "how does that action change the UI state". On a login screen, for example, do not send a "navigate" command; set isUserLoggedIn = true, and the UI navigates when it sees that state. [[src:ax-ui-events]]')
    B(C, S_, 3, 'p', 'Khi UI đã xử lý xong một phần state thoáng qua (đã hiện thông báo, người dùng đóng nó hay hết giờ), việc đó cũng là đầu vào của người dùng: UI gọi một hàm như messageShown(), ViewModel xóa thông báo khỏi state. Vòng này là UDF của chương G2, áp vào tầng UI. [[src:ax-ui-events]]',
      'Once the UI has handled a transient piece of state (the message was shown, dismissed or timed out), that too is user input: the UI calls a function such as messageShown(), and the ViewModel removes the message from state. This loop is G2\'s UDF, applied to the UI layer. [[src:ax-ui-events]]')

    S_ = 'oneoff'
    a(C + '.sec.%s.title' % S_, 'Vì sao không dùng Channel hay SharedFlow cho "sự kiện một lần"', 'Why not use a Channel or SharedFlow for "one-off events"')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'p', 'Nhiều app đưa sự kiện của ViewModel ra UI qua Channel hay stream khác. Tài liệu chỉ ra vấn đề: khi bên phát (ViewModel) sống lâu hơn bên nhận (UI), các cách này không bảo đảm sự kiện được giao và được xử lý. Hệ quả có thể là app rơi vào trạng thái không nhất quán, hay người dùng bỏ lỡ thông tin quan trọng. Lời khuyên: xử lý sự kiện ngay và rút nó thành UI state. [[src:ax-ui-events]]',
      'Many apps expose ViewModel events to the UI through a Channel or another stream. The docs point out the problem: when the producer (the ViewModel) outlives the consumer (the UI), these approaches do not guarantee the event is delivered and processed. The app may end up in an inconsistent state, or the user may miss critical information. The advice: handle the event right away and reduce it to UI state. [[src:ax-ui-events]]')
    B(C, S_, 2, 'p', 'Một trường hợp cụ thể, theo tài liệu API: MutableSharedFlow() mặc định không replay và không buffer; emit trả về ngay khi không có subscriber, và khi vắng subscriber chỉ các giá trị replay được giữ. Lúc xoay màn hình có một khoảng không ai thu thập, nên sự kiện phát đúng lúc đó mất. Ngược lại StateFlow phát lại giá trị mới nhất cho subscriber mới, nên một cờ không ai xóa sẽ hiện lại. [[src:kx-sharedflow]] [[src:kx-stateflow-api]]',
      'One concrete case, per the API docs: a default MutableSharedFlow() has no replay and no buffer; emit returns immediately when there are no subscribers, and in their absence only replay values are kept. During a rotation there is a window with nobody collecting, so an event emitted right then is lost. StateFlow, by contrast, replays its latest value to new subscribers, so a flag nobody clears shows again. [[src:kx-sharedflow]] [[src:kx-stateflow-api]]')
    B(C, S_, 3, 'note', 'Thêm replay hay buffer cho SharedFlow, hay dùng Channel có buffer, giúp không mất khi chưa có subscriber, nhưng vẫn có thể mất nếu Activity nhận sự kiện rồi bị hủy trước khi xử lý xong. Tài liệu cũng khuyên thu thập khi UI ở foreground (repeatOnLifecycle, track Coroutines A8). UI state với hàm báo đã xử lý tránh được cả hai.',
      'Adding replay or a buffer to the SharedFlow, or using a buffered Channel, avoids losing the event before a subscriber exists, but it can still be lost if the Activity receives it and is destroyed before finishing. The docs also advise collecting while the UI is in the foreground (repeatOnLifecycle, Coroutines track A8). UI state with a "handled" callback avoids both.')
    B(C, S_, 3, 'kind', 'pitfall')

    S_ = 'bugs'
    a(C + '.sec.%s.title' % S_, 'Hai lỗi hay gặp', 'Two common bugs')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'bug', 'Toast "Đặt lịch thành công" hiện lại mỗi khi xoay màn hình hay đổi sáng/tối.', 'The "Booked" Toast shows again on every rotation or light/dark switch.')
    B(C, S_, 1, 'cause', 'Thông báo nằm trong StateFlow dưới dạng cờ showSuccess không ai xóa; ViewModel sống qua lần tái tạo, và StateFlow phát lại giá trị mới nhất cho Activity mới.', 'The message sits in a StateFlow as a showSuccess flag nobody clears; the ViewModel survives the recreation, and StateFlow replays the latest value to the new Activity.')
    B(C, S_, 1, 'fix', 'Giữ thông báo trong UI state (userMessage) và cho UI gọi messageShown() sau khi hiện xong để ViewModel đặt về null.', 'Keep the message in UI state (userMessage) and have the UI call messageShown() once shown, so the ViewModel sets it back to null.')
    B(C, S_, 2, 'bug', 'Thỉnh thoảng đặt lịch xong không thấy xác nhận, người dùng bấm lại và có hai lịch.', 'Sometimes no confirmation appears after booking; the user taps again and gets two appointments.')
    B(C, S_, 2, 'cause', 'Xác nhận đi qua MutableSharedFlow() không replay; request xong đúng lúc đang xoay, không có subscriber, giá trị bị bỏ.', 'The confirmation goes through a MutableSharedFlow() without replay; the request finished mid-rotation with no subscriber, and the value was dropped.')
    B(C, S_, 2, 'fix', 'Rút sự kiện thành UI state như lỗi 1. Nút Đặt cũng nên tắt khi isLoading = true để không gửi hai lần.', 'Reduce the event to UI state as in bug 1. The Book button should also be disabled while isLoading = true, so it cannot submit twice.')

    S_ = 'ex'
    a(C + '.sec.%s.title' % S_, 'Bài tập', 'Exercise')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'ex', 'Màn Đăng nhập có: val navigate = Channel<Unit>() và val error = MutableSharedFlow<String>(). Đăng nhập xong thì navigate.send(Unit); sai mật khẩu thì error.emit("Sai mật khẩu"). Viết lại thành một LoginUiState và các hàm của ViewModel theo hướng dẫn chính thức, sao cho xoay màn hình không làm mất hay lặp lỗi và không điều hướng hai lần. (Bài tập của site, theo ví dụ màn đăng nhập trong trang UI events.) [[src:ax-ui-events]]',
      'A Login screen has: val navigate = Channel<Unit>() and val error = MutableSharedFlow<String>(). On success it calls navigate.send(Unit); on a wrong password error.emit("Wrong password"). Rewrite it as one LoginUiState plus ViewModel functions following the official guide, so that rotation neither loses nor repeats the error and never navigates twice. (The site\'s own exercise, after the login example on the UI events page.) [[src:ax-ui-events]]')
    B(C, S_, 1, 'hint', 'Mỗi sự kiện của ViewModel thành một trường của state; mỗi việc UI đã xử lý xong thành một hàm UI gọi ngược lên.', 'Each ViewModel event becomes a field of the state; each thing the UI has finished handling becomes a function the UI calls back.')
    B(C, S_, 1, 'sol', 'LoginUiState(isLoading, errorMessage: String?, isUserLoggedIn: Boolean). Đăng nhập đúng: isUserLoggedIn = true, UI thấy true thì điều hướng (trong LaunchedEffect theo state). Sai: errorMessage = "Sai mật khẩu", UI hiện rồi gọi errorShown() để đặt về null. Xoay màn hình chỉ làm UI đọc lại state hiện tại.',
      'LoginUiState(isLoading, errorMessage: String?, isUserLoggedIn: Boolean). On success: isUserLoggedIn = true, and the UI navigates when it sees true (in a LaunchedEffect keyed on state). On failure: errorMessage = "Wrong password"; the UI shows it, then calls errorShown() to set it back to null. A rotation only makes the UI read the current state again.')
    B(C, S_, 1, 'solkt', 'data class LoginUiState(val isLoading: Boolean = false, val errorMessage: String? = null, val isUserLoggedIn: Boolean = false)\n\nclass LoginViewModel(private val auth: AuthRepository) : ViewModel() {\n    val state = MutableStateFlow(LoginUiState())\n    fun login(u: String, p: String) = viewModelScope.launch {\n        state.update { it.copy(isLoading = true) }\n        val ok = auth.login(u, p)\n        state.update { if (ok) it.copy(isLoading = false, isUserLoggedIn = true) else it.copy(isLoading = false, errorMessage = "…") }\n    }\n    fun errorShown() = state.update { it.copy(errorMessage = null) }\n}')

    S_ = 'recall'
    a(C + '.sec.%s.title' % S_, 'Tự trả lời', 'Answer it yourself')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'ask', 'Vì sao cờ showSuccess trong StateFlow làm Toast hiện lại sau khi xoay?', 'Why does a showSuccess flag in a StateFlow make the Toast show again after rotating?')
    B(C, S_, 1, 'ans', 'ViewModel sống qua lần xoay nên cờ vẫn true, và StateFlow phát lại giá trị mới nhất cho Activity mới.', 'The ViewModel survives the rotation so the flag is still true, and StateFlow replays its latest value to the new Activity.')
    B(C, S_, 2, 'ask', 'Theo hướng dẫn chính thức, sự kiện từ ViewModel nên trở thành gì?', 'Per the official guide, what should events from the ViewModel become?')
    B(C, S_, 2, 'ans', 'Một cập nhật UI state; UI báo lại khi đã xử lý để ViewModel xóa phần thoáng qua.', 'A UI state update; the UI reports back once handled so the ViewModel clears the transient part.')

    S_ = 'honest'
    a(C + '.sec.%s.title' % S_, 'Chương này giản lược những gì', 'What this chapter simplifies')
    a(C + '.sec.%s.badge' % S_, 'simplified')
    B(C, S_, 1, 'p', 'Nguyên tắc theo các trang UI layer, UI events và State holders đọc ngày 2026-11-24; hành vi StateFlow và SharedFlow theo tài liệu API kotlinx.coroutines 1.11.0. Thời điểm xoay và lúc request xong trong mô phỏng được đặt sẵn để thấy từng trường hợp; trong app thật, lỗi mất sự kiện chỉ xảy ra khi hai việc trùng nhau, nên khó tái hiện. Mã rút gọn, bỏ phần thu thập theo vòng đời. Chương chưa nói về danh sách nhiều thông báo (tài liệu chỉ tới mẫu Jetsnack) và về lưu state qua process death chi tiết.',
      'The principles follow the UI layer, UI events and State holders pages as read on 2026-11-24; StateFlow and SharedFlow behaviour follows the kotlinx.coroutines 1.11.0 API docs. The moments of rotation and request completion in the simulation are placed on purpose to show each case; in a real app the lost-event bug happens only when the two coincide, which makes it hard to reproduce. The code is abridged and leaves out lifecycle-aware collection. The chapter does not cover lists of several messages (the docs point to the Jetsnack sample) or keeping state across process death in detail.')

    for q, qv, qe, av, ae, wv, we in [
        ('q1', 'StateFlow làm gì khi có subscriber mới?', 'What does a StateFlow do when a new subscriber arrives?', 'Phát lại giá trị mới nhất cho nó.', 'Replays its latest value to it.', 'StateFlow luôn có giá trị và replay một giá trị.', 'A StateFlow always has a value and replays one.'),
        ('q2', 'MutableSharedFlow() emit khi không có subscriber thì sao?', 'What happens when a MutableSharedFlow() emits with no subscribers?', 'Trả về ngay; giá trị bị bỏ.', 'It returns at once; the value is dropped.', 'Không replay, không buffer theo mặc định.', 'No replay and no buffer by default.'),
        ('q3', 'Sự kiện từ ViewModel nên thành gì?', 'What should an event from the ViewModel become?', 'Một cập nhật UI state.', 'A UI state update.', 'Đó là quy tắc chính của trang UI events.', 'That is the key rule of the UI events page.'),
        ('q4', 'ViewModel có sống qua việc hệ thống giết tiến trình không?', 'Does a ViewModel survive the system killing the process?', 'Không; dùng SavedStateHandle để khôi phục phần cần thiết.', 'No; use SavedStateHandle to restore what is needed.', 'ViewModel chỉ sống qua việc Activity bị tạo lại.', 'A ViewModel only survives Activity recreation.')]:
        a(C + '.quiz.%s.q' % q, qv, qe); a(C + '.quiz.%s.a' % q, av, ae); a(C + '.quiz.%s.why' % q, wv, we)
