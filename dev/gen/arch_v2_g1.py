# Kiến trúc · G1: vì sao cần kiến trúc (Phần 1)
# Nguồn: developer.android.com Guide to app architecture, Handle configuration changes, ViewModel overview, Testing fundamentals (đọc 2026-11-23);
# Dumbravan ch1 (app cũ: mạng, parse JSON và UI trong Activity với AsyncTask); Boudjnah ch1. Trần: 8 mục, mục cơ chế ≤ 4 khối.

SEC_ORDER = {'g1': ['hook', 'lifecycle', 'concerns', 'cost', 'bugs', 'ex', 'recall', 'honest']}


def add(a):
    def B(ch, sec, n, field, vi, en=None):
        a('%s.sec.%s.b.%02d.%s' % (ch, sec, n, field), vi, vi if en is None else en)

    m = lambda k, vi, en=None: a('m.god.' + k, vi, en)
    m('title', 'Một Activity làm mọi thứ, qua bốn phép thử', 'An Activity that does everything, put through four tests')
    m('overview', 'Màn Chọn giờ của app Hẹn Khám được viết hai cách: (1) Activity tự gọi mạng, parse JSON, lưu cache và vẽ UI; (2) tách thành UI, ViewModel, repository và nguồn dữ liệu. Cả hai chạy đúng lần đầu. Ta đưa chúng qua bốn phép thử: bấm, xoay màn hình, máy chủ đổi API, viết test.',
      'The ClinicBook app\'s Choose a time screen is written two ways: (1) the Activity calls the network, parses JSON, caches and draws the UI itself; (2) it is split into UI, ViewModel, repository and data source. Both work the first time. We put them through four tests: a tap, a rotation, a server API change, and writing a test.')
    m('wrapup', 'Kiến trúc không làm app chạy đúng hơn ở lần bấm đầu tiên. Nó quyết định chuyện gì xảy ra sau đó: dữ liệu có sống qua xoay màn hình không, một thay đổi lan ra bao nhiêu file, và có test được trên máy hay phải chạy thiết bị. Nguyên lý gốc là tách mối quan tâm và không giữ dữ liệu trong component mà hệ thống có thể hủy bất cứ lúc nào.',
      'Architecture does not make the app work better on the first tap. It decides what happens next: whether data survives a rotation, how many files one change spreads to, and whether you can test on your machine or need a device. The root principles are separation of concerns and not keeping data in components the system can destroy at any time.')
    m('simp.1', 'Sơ đồ có bốn tầng cho dễ thấy; hướng dẫn chính thức chỉ yêu cầu tối thiểu UI và data (chương G2). Số file phải sửa là đếm trong app mẫu (ba màn hình cùng gọi API giờ trống).', 'The diagram shows four layers for clarity; the official guide requires only UI and data at minimum (chapter G2). The number of files to change is counted in the sample app (three screens calling the free-slot API).')
    m('simp.2', 'Hành vi khi xoay màn hình và của ViewModel theo tài liệu chính thức; site không chạy app thật.', 'Rotation and ViewModel behaviour follow the official docs; the site does not run a real app.')
    m('ctl.hint', 'Đổi cách viết rồi đi lại; so ba số đo ở bước cuối.', 'Switch the approach and walk again; compare the three metrics at the last step.')
    m('ctl.case', 'Cách viết', 'Approach')
    for k, vi, en in [('god', 'Activity làm mọi thứ', 'an Activity doing everything'), ('layered', 'tách tầng', 'split into layers')]:
        m('ctl.case.' + k, vi, en)
    m('diagramTitle', 'Màn hình, ViewModel, repository, nguồn dữ liệu', 'Screen, ViewModel, repository, data source')
    m('diagramDesc', 'Một thao tác đi từ màn hình qua state holder và repository tới nguồn dữ liệu; tầng không có thì mờ đi', 'An action goes from the screen through the state holder and repository to the data source; absent layers are greyed out')
    for k, vi, en in [('ui', 'Màn hình (Activity)', 'Screen (Activity)'), ('vm', 'Giữ state (ViewModel)', 'State holder (ViewModel)'), ('repo', 'Repository', 'Repository'), ('source', 'Nguồn dữ liệu (mạng, DB)', 'Data source (network, DB)')]:
        m('n.' + k, vi, en)
    m('met.keep', 'Dữ liệu còn sau khi xoay', 'Data survives rotation'); m('met.files', 'File phải sửa khi đổi API', 'Files to edit on an API change'); m('met.test', 'Test logic chạy ở', 'Logic tests run on')
    for k, vi, en in [('na', 'chưa xét', 'not yet'), ('yes', 'còn', 'yes'), ('no', 'mất, phải tải lại', 'lost, reloaded')]:
        m('keep.' + k, vi, en)
    for k, vi, en in [('na', 'chưa xét', 'not yet'), ('local', 'máy phát triển (local)', 'your machine (local)'), ('device', 'chỉ thiết bị (instrumented)', 'a device only (instrumented)')]:
        m('test.' + k, vi, en)
    a('cap.god', 'Từ trái sang phải: màn hình, state holder, repository, nguồn dữ liệu. Ở cách "Activity làm mọi thứ", ba tầng sau không có (mờ) và mọi việc dồn vào màn hình. Khối viền đỏ là chỗ phép thử lộ vấn đề.', 'Left to right: screen, state holder, repository, data source. In the "Activity doing everything" approach the last three are absent (greyed) and everything piles onto the screen. A red-outlined box is where a test exposes a problem.')
    S = [
        ('god', 'tap', 'Bấm "Xem giờ": Activity tự làm hết', 'Tap "See times": the Activity does it all', 'onBookClick gọi mạng, parse JSON, ghi cache vào SharedPreferences rồi vẽ danh sách. Lần đầu mọi thứ chạy đúng.', 'onBookClick calls the network, parses JSON, writes the cache to SharedPreferences and draws the list. The first time, everything works.'),
        ('god', 'rotate', 'Xoay màn hình: danh sách mất, tải lại', 'Rotate: the list is lost and reloaded', 'Hệ thống hủy Activity và tạo instance mới. Biến slots của instance cũ mất theo; màn hình mới phải gọi mạng lại. Một request đang chạy dở cũng gắn với instance đã bị hủy.', 'The system destroys the Activity and creates a new instance. The old instance\'s slots field is gone; the new screen calls the network again. An in-flight request is also tied to the destroyed instance.'),
        ('god', 'api', 'Máy chủ đổi tên trường: sửa 3 Activity', 'The server renames a field: edit 3 Activities', 'Ba màn hình (Chọn giờ, Lịch của tôi, Lịch sử) đều tự parse JSON giờ hẹn. Một thay đổi ở máy chủ lan ra cả ba, dễ sót một chỗ.', 'Three screens (Choose a time, My appointments, History) each parse the slot JSON themselves. One server change spreads to all three, and missing one is easy.'),
        ('god', 'test', 'Viết test: chỉ chạy được trên thiết bị', 'Write a test: it only runs on a device', 'Logic nằm trong Activity, dính với mạng thật và SharedPreferences, nên muốn test phải dựng Activity trên thiết bị hay giả lập: chậm và dễ chập chờn.', 'The logic lives in the Activity, tied to the real network and SharedPreferences, so testing it means starting the Activity on a device or emulator: slow and flaky.'),
        ('layered', 'tap', 'Bấm "Xem giờ": đi qua từng tầng', 'Tap "See times": through each layer', 'UI gửi sự kiện cho ViewModel; ViewModel hỏi repository; repository lấy từ nguồn dữ liệu; state đi ngược lên UI. Kết quả trên màn hình giống hệt cách kia.', 'The UI sends an event to the ViewModel; the ViewModel asks the repository; the repository fetches from the data source; state flows back to the UI. What appears on screen is identical.'),
        ('layered', 'rotate', 'Xoay màn hình: Activity mới, ViewModel cũ', 'Rotate: a new Activity, the same ViewModel', 'Activity vẫn bị hủy và tạo lại, nhưng ViewModel gắn với ViewModelStoreOwner nên vẫn còn; màn hình mới đọc ngay state đã có, không gọi mạng lại.', 'The Activity is still destroyed and recreated, but the ViewModel is scoped to its ViewModelStoreOwner and survives; the new screen reads the existing state at once, with no new network call.'),
        ('layered', 'api', 'Máy chủ đổi tên trường: sửa 1 chỗ', 'The server renames a field: edit 1 place', 'Chỉ nguồn dữ liệu từ xa biết hình dạng JSON. Đổi ở đó; repository, ViewModel và ba màn hình không cần biết.', 'Only the remote data source knows the JSON shape. Change it there; the repository, ViewModel and all three screens need not know.'),
        ('layered', 'test', 'Viết test: chạy trên máy trong vài mili giây', 'Write a test: it runs on your machine in milliseconds', 'ViewModel nhận repository qua constructor, nên test thay bằng một repository giả trả dữ liệu cố định. Test chạy trên máy phát triển, không cần thiết bị.', 'The ViewModel receives its repository through the constructor, so a test swaps in a fake repository returning fixed data. The test runs on the development machine, no device needed.'),
    ]
    for case, k, tv, te, xv, xe in S:
        sid = case + '.' + k
        m('s.%s.title' % sid, tv, te); m('s.%s.explain' % sid, xv, xe); m('ev.' + sid, tv, te)
    for k, vi, en in [
        ('try', 'Đi hết bốn bước của mỗi cách viết; để ý ba số đo phía trên sơ đồ.', 'Walk all four steps of each approach; watch the three metrics above the diagram.'),
        ('god.rotate', 'Tài liệu Handle configuration changes: khi đổi cấu hình, hệ thống gọi onDestroy, hủy instance Activity hiện có rồi tạo instance mới bằng onCreate. [[src:ax-config-changes]]', 'Handle configuration changes docs: on a configuration change, the system calls onDestroy, destroys the existing Activity instance and creates a new one with onCreate. [[src:ax-config-changes]]'),
        ('god.api', 'Dumbravan (ch1) mô tả đúng kiểu app cũ này: mạng, parse JSON và cập nhật UI dồn vào Activity; mỗi thay đổi về nguồn dữ liệu kéo theo sửa Activity. [[src:book-dumbravan]]', 'Dumbravan (ch1) describes exactly this kind of old app: networking, JSON parsing and UI updates packed into the Activity; every data-source change drags the Activity along. [[src:book-dumbravan]]'),
        ('god.test', 'Tài liệu Testing fundamentals: test instrumented chạy trên thiết bị thật hay giả lập; test local chạy trên máy phát triển, nhỏ và nhanh. [[src:ax-test-fundamentals]]', 'Testing fundamentals docs: instrumented tests run on a physical or emulated device; local tests run on the development machine and are small and fast. [[src:ax-test-fundamentals]]'),
        ('layered.rotate', 'Tài liệu ViewModel: ViewModel giữ state qua các thay đổi cấu hình như xoay màn hình, nên UI không phải tải lại dữ liệu. [[src:ax-viewmodel]]', 'ViewModel docs: a ViewModel keeps its state across configuration changes such as rotation, so the UI does not have to fetch data again. [[src:ax-viewmodel]]'),
        ('layered.api', 'Hướng dẫn kiến trúc: tách mối quan tâm thành lớp, file, module và tầng có trách nhiệm rõ ràng. [[src:ax-arch-guide]]', 'Architecture guide: separate concerns into classes, files, modules and layers with clearly defined responsibilities. [[src:ax-arch-guide]]'),
        ('layered.test', 'Truyền phụ thuộc qua constructor là điều kiện để thay bằng bản giả khi test; chương G6 (dependency injection) đi sâu hơn. [[src:ax-arch-guide]]', 'Passing dependencies through the constructor is what makes swapping in a fake for tests possible; chapter G6 (dependency injection) goes deeper. [[src:ax-arch-guide]]')]:
        m('co.' + k, vi, en)

    C = 'g1'
    a(C + '.title', 'Vì sao cần kiến trúc', 'Why architecture matters')
    a(C + '.essence', 'Activity, Fragment, Service là component do hệ thống quản lý: chúng có thể bị hủy bất cứ lúc nào (xoay màn hình, thiếu bộ nhớ, người dùng rời app). Vì vậy không giữ dữ liệu và state của app trong chúng.\nTách mối quan tâm: mỗi phần (lớp, file, module, tầng) có một trách nhiệm rõ ràng. UI chỉ vẽ state và gửi sự kiện; dữ liệu đến từ model độc lập với UI.\nKiến trúc tốt không làm lần chạy đầu đúng hơn; nó làm thay đổi, xoay màn hình và kiểm thử bớt đau.',
      'Activities, Fragments and Services are components managed by the system: they can be destroyed at any time (rotation, low memory, the user leaving). So do not keep app data and state in them.\nSeparation of concerns: each part (class, file, module, layer) has one clear responsibility. The UI only draws state and sends events; data comes from models independent of the UI.\nGood architecture does not make the first run more correct; it makes change, rotation and testing hurt less.')
    a(C + '.goal.g1', 'Đã thấy phép thử xoay màn hình', 'Saw the rotation test')
    a(C + '.goal.g2', 'Đã đi hết bốn phép thử', 'Walked all four tests')
    a(C + '.sim.arch.god', 'Activity làm mọi thứ và tách tầng', 'an all-in-one Activity versus layers')

    S_ = 'hook'
    a(C + '.sec.%s.title' % S_, 'Đoán trước khi đọc', 'Predict before reading')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'predict', 'Màn Chọn giờ tải danh sách giờ trống vào một biến `slots` khai báo trong Activity. Người dùng xoay điện thoại sang ngang. Biến `slots` còn dữ liệu không?',
      'The Choose a time screen loads the free slots into a `slots` field declared in the Activity. The user turns the phone sideways. Does `slots` still hold the data?')
    B(C, S_, 1, 'ans', 'Không. Xoay màn hình là một thay đổi cấu hình: hệ thống hủy Activity và tạo instance mới, nên mọi biến của instance cũ mất. Màn hình phải tải lại. Mô phỏng ngay dưới đưa cách viết này và cách tách tầng qua bốn phép thử. [[src:ax-config-changes]]',
      'No. Rotation is a configuration change: the system destroys the Activity and creates a new instance, so every field of the old instance is gone. The screen has to reload. The simulation just below puts this approach and a layered one through four tests. [[src:ax-config-changes]]')

    S_ = 'lifecycle'
    a(C + '.sec.%s.title' % S_, 'Component do hệ thống quản lý', 'Components the system manages')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'p', 'Một app Android được ghép từ các component (Activity, Fragment, Service, BroadcastReceiver, ContentProvider) mà hệ thống tạo và hủy theo ý nó. Hướng dẫn kiến trúc chính thức nói rõ: component có thể được khởi chạy riêng lẻ, không theo thứ tự, và hệ thống hay người dùng có thể hủy chúng bất cứ lúc nào; vì thế không nên giữ dữ liệu hay state của app trong component. [[src:ax-arch-guide]]',
      'An Android app is assembled from components (Activity, Fragment, Service, BroadcastReceiver, ContentProvider) that the system creates and destroys as it sees fit. The official architecture guide says it plainly: components can be launched individually and out of order, and the OS or the user can destroy them at any time; therefore do not keep app data or state in your components. [[src:ax-arch-guide]]')
    B(C, S_, 2, 'p', 'Trường hợp hay gặp nhất là thay đổi cấu hình (xoay màn hình, đổi ngôn ngữ, đổi cỡ chữ): hệ thống gọi onDestroy, hủy Activity rồi tạo instance mới bằng onCreate với cấu hình mới. ViewModel được thiết kế cho đúng chuyện này: nó sống qua thay đổi cấu hình, tới khi Activity thật sự kết thúc. [[src:ax-config-changes]] [[src:ax-viewmodel]]',
      'The most common case is a configuration change (rotation, a language change, a font-size change): the system calls onDestroy, destroys the Activity and creates a new instance with onCreate and the new configuration. ViewModel is designed for exactly this: it survives configuration changes, until the Activity really finishes. [[src:ax-config-changes]] [[src:ax-viewmodel]]')
    B(C, S_, 3, 'note', 'ViewModel sống qua xoay màn hình, nhưng không sống qua việc hệ thống giết tiến trình khi app nằm nền lâu. Phần đó cần SavedStateHandle hay lưu bền (track Lưu dữ liệu); chương G3 nói thêm. [[src:ax-viewmodel]]',
      'A ViewModel survives rotation, but not the system killing the process while the app sits in the background. That needs SavedStateHandle or persistent storage (the Saving Data track); chapter G3 says more. [[src:ax-viewmodel]]')
    B(C, S_, 3, 'kind', 'pitfall')

    S_ = 'concerns'
    a(C + '.sec.%s.title' % S_, 'Tách mối quan tâm và UI dẫn từ dữ liệu', 'Separation of concerns and UI driven by data')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'p', 'Hướng dẫn chính thức gọi tách mối quan tâm là nguyên lý quan trọng nhất: chia app thành lớp, file, package, module và tầng mà mỗi phần có trách nhiệm rõ ràng. Nguyên lý thứ hai: UI được dẫn từ model dữ liệu (tốt nhất là model lưu bền), độc lập với thành phần UI, nên không mất khi hệ thống hủy Activity. Từ đó ra kiến trúc gợi ý: tối thiểu một tầng UI và một tầng data, có thể thêm tầng domain ở giữa (chương G2). [[src:ax-arch-guide]]',
      'The official guide calls separation of concerns the most important principle: divide the app into classes, files, packages, modules and layers with clearly defined responsibilities. The second principle: drive the UI from data models (persistent ones, preferably), independent of UI elements, so nothing is lost when the system destroys an Activity. That leads to the recommended architecture: at least a UI layer and a data layer, optionally a domain layer in between (chapter G2). [[src:ax-arch-guide]]')
    B(C, S_, 2, 'kt', '// UI: chỉ vẽ state và gửi sự kiện\nsetContent { ChooseTime(state = vm.state.collectAsStateWithLifecycle().value, onDay = vm::load) }\n\n// state holder: giữ state, sống qua xoay màn hình\nclass ChooseTimeViewModel(private val repo: SlotRepository) : ViewModel() { … }\n\n// data: biết lấy dữ liệu ở đâu và hình dạng của nó\nclass SlotRepository(private val api: SlotApi, private val dao: SlotDao) { … }',
      '// UI: only draws state and sends events\nsetContent { ChooseTime(state = vm.state.collectAsStateWithLifecycle().value, onDay = vm::load) }\n\n// state holder: holds state, survives rotation\nclass ChooseTimeViewModel(private val repo: SlotRepository) : ViewModel() { … }\n\n// data: knows where data comes from and what it looks like\nclass SlotRepository(private val api: SlotApi, private val dao: SlotDao) { … }')
    B(C, S_, 3, 'p', 'Dumbravan (ch1) kể lại cách app Android từng được viết: Activity tự mở HttpURLConnection, parse JSON, dùng AsyncTask để về main thread, và nhận về rò rỉ context, mã khó test, và đội phải đông dần chỉ để giữ nguyên tốc độ khi app lớn lên. Boudjnah (ch1) mở đầu bằng cùng câu hỏi: làm sao để thay đổi chỗ này không làm vỡ chỗ khác. [[src:book-dumbravan]] [[src:book-boudjnah]]',
      'Dumbravan (ch1) recounts how Android apps used to be written: the Activity opened an HttpURLConnection, parsed JSON, used AsyncTask to get back to the main thread, and ended up with context leaks, hard-to-test code, and teams that had to keep growing just to keep the same pace as the app grew. Boudjnah (ch1) opens with the same question: how to change one part without breaking another. [[src:book-dumbravan]] [[src:book-boudjnah]]')

    S_ = 'cost'
    a(C + '.sec.%s.title' % S_, 'Kiến trúc cũng có giá', 'Architecture has a cost too')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'p', 'Nhiều tầng nghĩa là nhiều lớp, nhiều file và nhiều phép chuyển đổi model hơn. Hướng dẫn chính thức chỉ yêu cầu tối thiểu hai tầng (UI, data) và coi domain là tùy chọn; các sách Clean Architecture đặt domain ở trung tâm. Track này theo hướng dẫn chính thức và chỉ thêm tầng khi nó giải quyết một vấn đề cụ thể: logic dùng lại, thay đổi lan rộng, hay test khó viết. [[src:ax-arch-guide]] [[src:book-boudjnah]]',
      'More layers mean more classes, more files and more model conversions. The official guide requires only two layers (UI, data) and treats domain as optional; the Clean Architecture books put domain at the centre. This track follows the official guide and adds a layer only when it solves a concrete problem: reused logic, changes spreading widely, or tests that are hard to write. [[src:ax-arch-guide]] [[src:book-boudjnah]]')
    B(C, S_, 2, 'note', 'Một màn hình chỉ đọc một danh sách không cần use case, mapper và ba model gần giống nhau. Thêm tầng "cho đủ bộ" làm mã dài hơn mà không bớt lỗi nào.',
      'A screen that just reads a list does not need a use case, a mapper and three nearly identical models. Adding layers "for completeness" makes the code longer without removing a single bug.')
    B(C, S_, 2, 'kind', 'pitfall')

    S_ = 'bugs'
    a(C + '.sec.%s.title' % S_, 'Hai lỗi hay gặp', 'Two common bugs')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'bug', 'Người dùng xoay điện thoại giữa lúc đang tải giờ trống: danh sách nhấp nháy trống, tải lại, và đôi khi app crash vì cập nhật một màn hình đã bị hủy.', 'A user rotates the phone while free slots are loading: the list flickers empty, reloads, and sometimes the app crashes updating a destroyed screen.')
    B(C, S_, 1, 'cause', 'Dữ liệu và request nằm trong Activity. Xoay màn hình hủy instance đang giữ chúng; request cũ trả về cho một màn hình không còn nữa.', 'The data and the request live in the Activity. Rotation destroys the instance holding them; the old request answers a screen that no longer exists.')
    B(C, S_, 1, 'fix', 'Chuyển state và việc tải vào ViewModel (viewModelScope); Activity chỉ quan sát state.', 'Move the state and the loading into a ViewModel (viewModelScope); the Activity only observes state.')
    B(C, S_, 2, 'bug', 'Máy chủ đổi "start" thành "startTime"; màn Lịch của tôi đã sửa nhưng màn Lịch sử vẫn hiện giờ trống không.', 'The server renames "start" to "startTime"; My appointments was fixed but History still shows blank times.')
    B(C, S_, 2, 'cause', 'Mỗi màn hình tự parse JSON. Thay đổi ở máy chủ phải sửa nhiều nơi, và một nơi bị sót.', 'Each screen parses the JSON itself. A server change must be fixed in several places, and one was missed.')
    B(C, S_, 2, 'fix', 'Để một nguồn dữ liệu từ xa duy nhất biết hình dạng JSON và đổi nó sang model của app; các màn hình chỉ thấy model.', 'Let a single remote data source know the JSON shape and convert it into the app\'s model; screens only see the model.')

    S_ = 'ex'
    a(C + '.sec.%s.title' % S_, 'Bài tập', 'Exercise')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'ex', 'Activity Lịch sử khám làm sáu việc: (a) mở HttpURLConnection tới /history, (b) parse JSON thành danh sách lượt khám, (c) lọc các lượt đã hủy, (d) lưu bản sao vào SharedPreferences để dùng khi mất mạng, (e) giữ danh sách trong một biến, (f) vẽ RecyclerView. Xếp mỗi việc vào một chỗ: UI, ViewModel, repository, hay nguồn dữ liệu (từ xa hoặc cục bộ). Rồi viết chữ ký constructor của ViewModel và repository. (Bài tập của site, theo ý Dumbravan ch1.) [[src:book-dumbravan]]',
      'The Visit history Activity does six things: (a) opens an HttpURLConnection to /history, (b) parses JSON into a list of visits, (c) filters out cancelled visits, (d) saves a copy in SharedPreferences for offline use, (e) keeps the list in a field, (f) draws a RecyclerView. Put each job in one place: UI, ViewModel, repository, or a data source (remote or local). Then write the constructor signatures of the ViewModel and the repository. (The site\'s own exercise, after Dumbravan ch1.) [[src:book-dumbravan]]')
    B(C, S_, 1, 'hint', 'Hỏi với mỗi việc: nó cần biết gì (JSON, màn hình, quy tắc nghiệp vụ, nơi lưu) và nó có phải sống qua xoay màn hình không.', 'Ask of each job: what does it need to know (JSON, the screen, a business rule, where data is stored), and must it survive rotation?')
    B(C, S_, 1, 'sol', '(a) và (b): nguồn dữ liệu từ xa. (d): nguồn dữ liệu cục bộ (track Lưu dữ liệu sẽ đổi sang DataStore hay Room). (c): repository, hoặc một use case nếu nhiều màn hình cần cùng quy tắc (chương G5). (e): ViewModel, dưới dạng state. (f): UI. ViewModel chỉ biết repository; repository biết hai nguồn dữ liệu.',
      '(a) and (b): the remote data source. (d): the local data source (the Saving Data track will move it to DataStore or Room). (c): the repository, or a use case if several screens need the same rule (chapter G5). (e): the ViewModel, as state. (f): the UI. The ViewModel only knows the repository; the repository knows both data sources.')
    B(C, S_, 1, 'solkt', 'class HistoryRemoteSource(private val http: HttpClient) { suspend fun visits(): List<VisitDto> = … }\nclass HistoryLocalSource(private val prefs: SharedPreferences) { … }\n\nclass HistoryRepository(\n    private val remote: HistoryRemoteSource,\n    private val local: HistoryLocalSource,\n) {\n    suspend fun activeVisits(): List<Visit> = …   // lọc lượt đã hủy\n}\n\nclass HistoryViewModel(private val repo: HistoryRepository) : ViewModel() {\n    val state = MutableStateFlow<HistoryState>(HistoryState.Loading)\n}')

    S_ = 'recall'
    a(C + '.sec.%s.title' % S_, 'Tự trả lời', 'Answer it yourself')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'ask', 'Vì sao không nên giữ dữ liệu của app trong biến của Activity?', 'Why should app data not be kept in an Activity\'s fields?')
    B(C, S_, 1, 'ans', 'Vì hệ thống có thể hủy Activity bất cứ lúc nào, ví dụ khi xoay màn hình, và biến mất theo instance đó.', 'Because the system can destroy the Activity at any time, for example on rotation, and the fields go with that instance.')
    B(C, S_, 2, 'ask', 'Tách tầng giúp gì cho việc kiểm thử?', 'How does splitting into layers help testing?')
    B(C, S_, 2, 'ans', 'Logic nằm trong lớp thường nhận phụ thuộc qua constructor, nên test thay được bằng bản giả và chạy trên máy phát triển thay vì thiết bị.', 'The logic lives in plain classes that receive their dependencies through the constructor, so a test can swap in fakes and run on the development machine instead of a device.')

    S_ = 'honest'
    a(C + '.sec.%s.title' % S_, 'Chương này giản lược những gì', 'What this chapter simplifies')
    a(C + '.sec.%s.badge' % S_, 'simplified')
    B(C, S_, 1, 'p', 'Nguyên lý và hành vi theo các trang Guide to app architecture, Handle configuration changes, ViewModel và Testing fundamentals đọc ngày 2026-11-23. Số file phải sửa (3 so với 1) là đếm trong app mẫu, không phải số đo chung. Mã minh họa rút gọn, không biên dịch được nguyên văn. Chương chưa nói về cách tránh hủy Activity khi đổi cấu hình (android:configChanges), lưu state qua việc hệ thống giết tiến trình, và cách các tầng phụ thuộc nhau (chương G2).',
      'The principles and behaviour follow the Guide to app architecture, Handle configuration changes, ViewModel and Testing fundamentals pages as read on 2026-11-23. The number of files to edit (3 versus 1) is counted in the sample app, not a general measurement. The sample code is abridged and does not compile as is. The chapter does not yet cover avoiding Activity recreation (android:configChanges), keeping state across process death, or how the layers depend on each other (chapter G2).')

    for q, qv, qe, av, ae, wv, we in [
        ('q1', 'Khi xoay màn hình, Activity hiện tại ra sao?', 'What happens to the current Activity on rotation?', 'Bị hủy; hệ thống tạo instance mới.', 'It is destroyed; the system creates a new instance.', 'Xoay màn hình là thay đổi cấu hình.', 'Rotation is a configuration change.'),
        ('q2', 'ViewModel có bị tạo lại khi xoay màn hình không?', 'Is the ViewModel recreated on rotation?', 'Không; nó sống tới khi Activity kết thúc.', 'No; it lives until the Activity finishes.', 'ViewModel gắn với ViewModelStoreOwner, không với instance Activity.', 'A ViewModel is scoped to its ViewModelStoreOwner, not to an Activity instance.'),
        ('q3', 'Theo hướng dẫn chính thức, app tối thiểu có những tầng nào?', 'Per the official guide, which layers must an app have at minimum?', 'UI và data.', 'UI and data.', 'Domain là tùy chọn.', 'Domain is optional.'),
        ('q4', 'Test local chạy ở đâu?', 'Where do local tests run?', 'Trên máy phát triển (hay server), không cần thiết bị.', 'On the development machine (or a server), no device needed.', 'Test instrumented mới cần thiết bị thật hay giả lập.', 'Only instrumented tests need a physical or emulated device.')]:
        a(C + '.quiz.%s.q' % q, qv, qe); a(C + '.quiz.%s.a' % q, av, ae); a(C + '.quiz.%s.why' % q, wv, we)
