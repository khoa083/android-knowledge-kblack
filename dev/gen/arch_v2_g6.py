# Kiến trúc · G6: dependency injection thủ công và Hilt; scope và vòng đời (Phần 2)
# Nguồn: developer.android.com Dependency injection in Android, Manual dependency injection, Dependency injection with Hilt (đọc 2026-11-24).
# Trần: 8 mục, mục cơ chế ≤ 4 khối.

SEC_ORDER = {'g6': ['hook', 'why', 'manual', 'hilt', 'bugs', 'ex', 'recall']}


def add(a):
    def B(ch, sec, n, field, vi, en=None):
        a('%s.sec.%s.b.%02d.%s' % (ch, sec, n, field), vi, vi if en is None else en)

    m = lambda k, vi, en=None: a('m.di.' + k, vi, en)
    m('title', 'Ai tạo repository, và nó sống bao lâu', 'Who creates the repository, and how long it lives')
    m('overview', 'Hai màn Chọn giờ và Đổi lịch cần cùng một SlotRepository. Ba cách: (1) mỗi ViewModel tự tạo repository của nó, rồi sửa bằng một container dùng chung; (2) để Hilt tạo và chia sẻ qua scope @Singleton; (3) một container toàn cục giữ repository được tạo bằng Activity làm Context.',
      'Choose a time and Reschedule both need the same SlotRepository. Three approaches: (1) each ViewModel creates its own repository, then the fix with a shared container; (2) let Hilt create and share it through the @Singleton scope; (3) a global container holding a repository built with an Activity as its Context.')
    m('wrapup', 'Dependency injection nghĩa là lớp không tự tạo phụ thuộc mà nhận chúng từ bên ngoài. Ai tạo và giữ instance quyết định có bao nhiêu bản và chúng sống bao lâu. Hilt gắn mỗi binding vào một component có vòng đời rõ ràng; @Singleton cho một bản dùng chung suốt đời Application. Quy tắc an toàn: object sống lâu không được giữ object sống ngắn hơn, nhất là Activity.',
      'Dependency injection means a class does not create its dependencies but receives them from outside. Who creates and holds an instance decides how many copies exist and how long they live. Hilt ties each binding to a component with a clear lifetime; @Singleton gives one shared copy for the whole life of the Application. The safety rule: a long-lived object must not hold a shorter-lived one, an Activity above all.')
    m('simp.1', 'Mỗi dải chỉ vẽ vài object; app thật có nhiều binding hơn và có thêm ActivityRetainedComponent, ServiceComponent.', 'Each band shows only a few objects; a real app has many more bindings plus ActivityRetainedComponent and ServiceComponent.')
    m('simp.2', 'Lỗi biên dịch của Hilt ở bước cuối được suy ra từ bảng binding mặc định trong tài liệu Android (đọc ngày 2026-11-24): SingletonComponent chỉ có sẵn Application. Câu chữ thông báo thật của Dagger (thư viện mà Hilt dựa vào) có thể khác. Chương chưa nói chi tiết về module Hilt (@Module, @Provides, @Binds), qualifier tự định nghĩa, ActivityRetainedComponent, và Dagger dùng trực tiếp.',
      'The Hilt compile error in the last step is inferred from the default-bindings table in the Android docs (read on 2026-11-24): SingletonComponent only has Application available. The real message from Dagger (the library Hilt builds on) may be worded differently. The chapter does not cover Hilt modules (@Module, @Provides, @Binds) in detail, custom qualifiers, ActivityRetainedComponent, or using Dagger directly.')
    m('ctl.hint', 'Đổi cách tạo rồi đi lại bốn bước; xem tab "Sơ đồ phạm vi".', 'Switch the approach and walk the four steps again; watch the "Scope map" tab.')
    m('ctl.case', 'Cách tạo repository', 'How the repository is created')
    for k, vi, en in [('manual', 'tự tạo, rồi container thủ công', 'self-created, then a manual container'), ('hilt', 'Hilt với @Singleton', 'Hilt with @Singleton'), ('leak', 'singleton giữ Activity', 'a singleton holding an Activity')]:
        m('ctl.case.' + k, vi, en)
    m('diagramTitle', 'Activity, ViewModel, repository, cơ sở dữ liệu', 'Activity, ViewModel, repository, database')
    m('diagramDesc', 'Ai giữ tham chiếu tới ai, từ màn hình xuống database', 'Who holds a reference to whom, from the screen down to the database')
    for k, vi, en in [('act', 'Màn hình (Activity)', 'Screen (Activity)'), ('vm', 'ViewModel', 'ViewModel'), ('repo', 'SlotRepository', 'SlotRepository'), ('db', 'Cơ sở dữ liệu (Room)', 'Database (Room)')]:
        m('n.' + k, vi, en)
    m('met.inst', 'Số instance SlotRepository', 'SlotRepository instances'); m('met.hold', 'Giữ Activity đã hủy', 'Holds a destroyed Activity'); m('met.when', 'Lỗi lộ ra lúc', 'The error shows up')
    for k, vi, en in [('yes', 'có (rò rỉ)', 'yes (a leak)'), ('no', 'không', 'no')]:
        m('hold.' + k, vi, en)
    for k, vi, en in [('na', 'chưa có lỗi', 'no error yet'), ('runtime', 'lúc chạy, khó thấy', 'at runtime, hard to spot'), ('compile', 'lúc biên dịch', 'at compile time')]:
        m('when.' + k, vi, en)
    a('cap.di', 'Từ trái sang phải: màn hình, ViewModel, repository, database. Mũi tên là "giữ tham chiếu". Khối viền đỏ đang có nhiều bản không nên có, hay đang giữ thứ sống ngắn hơn nó. Tab "Sơ đồ phạm vi" xếp object theo thời gian sống.',
      'Left to right: screen, ViewModel, repository, database. Arrows mean "holds a reference". A red-outlined box exists in copies it should not have, or holds something that lives shorter than it does. The "Scope map" tab arranges objects by lifetime.')
    S = [
        ('manual', 's1', 'ViewModel tự tạo repository', 'The ViewModel creates its repository',
         'ChooseTimeViewModel gọi SlotRepository(SlotApi(), Room.databaseBuilder(...).build()). Repository và database sống cùng ViewModel này.',
         'ChooseTimeViewModel calls SlotRepository(SlotApi(), Room.databaseBuilder(...).build()). The repository and database live with this ViewModel.'),
        ('manual', 's2', 'Màn Đổi lịch chép cùng dòng tạo', 'Reschedule copies the same construction',
         'RescheduleViewModel tạo repository và database của riêng nó. Giờ có hai SlotRepository và hai instance database cho cùng một tệp.',
         'RescheduleViewModel creates its own repository and database. There are now two SlotRepository objects and two database instances for the same file.'),
        ('manual', 's3', 'Hai bộ nhớ đệm lệch nhau', 'Two in-memory caches drift apart',
         'Đặt lịch ở màn Chọn giờ cập nhật bộ nhớ đệm của repository #1. Repository #2 không biết, nên màn Đổi lịch vẫn thấy 9:30 còn trống. Lỗi chỉ lộ ra lúc chạy.',
         'Booking on Choose a time updates repository #1\'s in-memory cache. Repository #2 does not know, so Reschedule still sees 9:30 as free. The bug only shows at runtime.'),
        ('manual', 's4', 'Sửa: container dùng chung trong Application', 'Fix: a shared container in the Application',
         'AppContainer giữ một SlotRepository duy nhất; lớp Application tạo container và mọi ViewModel lấy repository từ đó. Đây là DI thủ công: ai cần gì thì nhận, không tự tạo.',
         'AppContainer holds a single SlotRepository; the Application class creates the container and every ViewModel gets the repository from it. This is manual DI: classes receive what they need instead of creating it.'),
        ('hilt', 's1', 'Khai báo: @Singleton và @Inject constructor', 'Declare: @Singleton and @Inject constructor',
         'Application có @HiltAndroidApp. SlotRepository có @Inject constructor để Hilt biết cách tạo, và @Singleton để gắn nó vào SingletonComponent, sống cùng Application.',
         'The Application has @HiltAndroidApp. SlotRepository has an @Inject constructor so Hilt knows how to build it, and @Singleton to tie it to SingletonComponent, which lives with the Application.'),
        ('hilt', 's2', 'ViewModel nhận repository qua constructor', 'The ViewModel receives the repository through its constructor',
         'ChooseTimeViewModel có @HiltViewModel và @Inject constructor(repo). Hilt tạo ViewModel và đưa repository vào; ViewModel không biết repository được tạo thế nào.',
         'ChooseTimeViewModel has @HiltViewModel and @Inject constructor(repo). Hilt builds the ViewModel and passes the repository in; the ViewModel does not know how the repository is made.'),
        ('hilt', 's3', 'Màn thứ hai nhận cùng một instance', 'The second screen gets the same instance',
         'RescheduleViewModel cũng yêu cầu SlotRepository. Binding có scope @Singleton nên Hilt trả lại instance đã tạo, không tạo mới.',
         'RescheduleViewModel also asks for SlotRepository. The binding is scoped @Singleton, so Hilt returns the existing instance instead of making a new one.'),
        ('hilt', 's4', 'Activity lấy ViewModel; mỗi thứ một vòng đời', 'The Activity gets its ViewModel; each has its own lifetime',
         'Activity có @AndroidEntryPoint và lấy ViewModel bằng by viewModels(). SingletonComponent sống từ Application.onCreate tới khi Application bị hủy; ViewModelComponent sống cùng ViewModel; ActivityComponent từ Activity.onCreate tới onDestroy.',
         'The Activity has @AndroidEntryPoint and gets its ViewModel with by viewModels(). SingletonComponent lives from Application.onCreate until the Application is destroyed; ViewModelComponent lives with the ViewModel; ActivityComponent from Activity.onCreate to onDestroy.'),
        ('leak', 's1', 'Container toàn cục nhận Activity làm Context', 'A global container receives an Activity as its Context',
         'object AppContainer giữ repository; trong ChooseTimeActivity.onCreate, ai đó viết AppContainer.repo = SlotRepository(this). this là Activity.',
         'object AppContainer holds the repository; in ChooseTimeActivity.onCreate someone writes AppContainer.repo = SlotRepository(this). this is the Activity.'),
        ('leak', 's2', 'Xoay màn hình: Activity cũ không được thu hồi', 'Rotate: the old Activity is never reclaimed',
         'Hệ thống hủy Activity #1 và tạo #2. Nhưng object sống suốt tiến trình vẫn giữ repository, và repository giữ Activity #1, cùng toàn bộ cây View của nó. Bộ nhớ tăng sau mỗi lần xoay.',
         'The system destroys Activity #1 and creates #2. But the process-long object still holds the repository, and the repository holds Activity #1, with its whole View tree. Memory grows with every rotation.'),
        ('leak', 's3', 'Sửa: dùng context của Application', 'Fix: use the Application context',
         'Repository nhận @ApplicationContext context: Context. Application sống ít nhất lâu bằng singleton, nên không còn object sống lâu giữ object sống ngắn.',
         'The repository takes @ApplicationContext context: Context. The Application lives at least as long as the singleton, so no long-lived object holds a short-lived one.'),
        ('leak', 's4', 'Nếu cố đưa Activity vào @Singleton: lỗi biên dịch', 'Forcing an Activity into a @Singleton: a compile error',
         'Thử viết @Singleton class SlotRepository @Inject constructor(activity: Activity). SingletonComponent chỉ có binding Application; Activity chỉ có trong ActivityComponent. Hilt báo lỗi khi biên dịch, trước khi kịp rò rỉ.',
         'Try @Singleton class SlotRepository @Inject constructor(activity: Activity). SingletonComponent only has an Application binding; Activity exists only in ActivityComponent. Hilt fails at compile time, before any leak can happen.'),
    ]
    for case, k, tv, te, xv, xe in S:
        sid = case + '.' + k
        m('s.%s.title' % sid, tv, te); m('s.%s.explain' % sid, xv, xe); m('ev.' + sid, tv, te)
    for k, vi, en in [
        ('try', 'Đi bốn bước của từng cách; đếm số instance và xem có mũi tên đỏ nào trong "Sơ đồ phạm vi".', 'Walk the four steps of each approach; count the instances and look for red arrows in the "Scope map".'),
        ('manual.s2', 'Tạo phụ thuộc ngay trong lớp dùng nó làm mã khó dùng lại và khó test; đó là vấn đề DI giải quyết. [[src:ax-di]]', 'Creating dependencies inside the class that uses them makes code hard to reuse and test; that is the problem DI solves. [[src:ax-di]]'),
        ('manual.s3', 'Đây là lỗi "hai nguồn sự thật" của chương G2, lần này do cách tạo object chứ không do cách viết repository.', 'This is chapter G2\'s "two sources of truth" bug, caused this time by how objects are created rather than how the repository is written.'),
        ('manual.s4', 'Tài liệu Android về DI thủ công khuyên: đặt container (object chứa và tạo các phụ thuộc) dùng chung trong lớp Application. AppContainer không phải singleton kiểu object; singleton làm test khó vì mọi test dùng chung một instance. [[src:ax-di-manual]]', 'The Android docs on manual DI advise: put a shared container (an object that creates and holds the dependencies) in the Application class. AppContainer is not an object singleton; singletons make testing harder because all tests share one instance. [[src:ax-di-manual]]'),
        ('hilt.s2', 'Hilt sinh component cho từng lớp Android có thể inject: SingletonComponent cho Application, ViewModelComponent cho ViewModel, ActivityComponent cho Activity. [[src:ax-hilt]]', 'Hilt generates a component for each injectable Android class: SingletonComponent for the Application, ViewModelComponent for ViewModels, ActivityComponent for Activities. [[src:ax-hilt]]'),
        ('hilt.s3', 'Mặc định binding không có scope: mỗi lần yêu cầu là một instance mới. Binding có scope chỉ được tạo một lần cho mỗi instance của component đó, và mọi yêu cầu dùng chung. [[src:ax-hilt]]', 'Bindings are unscoped by default: every request makes a new instance. A scoped binding is created once per instance of its component, and every request shares it. [[src:ax-hilt]]'),
        ('hilt.s4', 'Tài liệu nhắc: binding có scope nằm trong bộ nhớ tới khi component bị hủy, nên hạn chế dùng scope; chỉ dùng khi cần chia sẻ trạng thái hay đồng bộ. [[src:ax-hilt]]', 'The docs warn: a scoped binding stays in memory until its component is destroyed, so minimise scoping; use it when state must be shared or synchronised. [[src:ax-hilt]]'),
        ('leak.s2', 'Rò rỉ bộ nhớ là khi một object không còn dùng vẫn bị giữ tham chiếu nên không được thu hồi; track Gỡ lỗi (l8) dạy cách thấy chuỗi tham chiếu này trong heap dump.', 'A memory leak is an object no longer in use but still referenced, so it cannot be reclaimed; the Debugging track (l8) shows how to see this reference chain in a heap dump.'),
        ('leak.s3', 'Hilt có sẵn hai qualifier @ApplicationContext và @ActivityContext để chọn đúng loại Context. [[src:ax-hilt]]', 'Hilt provides the @ApplicationContext and @ActivityContext qualifiers to pick the right kind of Context. [[src:ax-hilt]]'),
        ('leak.s4', 'Bảng binding mặc định: SingletonComponent có Application; ActivityComponent có Application và Activity. Một binding chỉ dùng được phụ thuộc của component nó và các component cha. [[src:ax-hilt]]', 'Default bindings: SingletonComponent has Application; ActivityComponent has Application and Activity. A binding can only use dependencies from its own component and its parents. [[src:ax-hilt]]')]:
        m('co.' + k, vi, en)
    a('preset.di', 'Kiến trúc · hai instance repository và singleton giữ Activity', 'Architecture · two repository instances and a singleton holding an Activity')

    z = lambda k, vi, en=None: a('vz.' + k, vi, en)
    z('tab.di', 'Sơ đồ phạm vi', 'Scope map')
    z('di.cap', 'Ba dải xếp theo thời gian sống, dài nhất bên trái (dải Application là scope @Singleton). Mũi tên là "giữ tham chiếu"; mũi tên đỏ đi từ object sống lâu sang object sống ngắn hơn, tức một rò rỉ hay một lỗi.', 'Three bands ordered by lifetime, longest on the left (the Application band is the @Singleton scope). Arrows mean "holds a reference"; a red arrow goes from a long-lived object to a shorter-lived one, meaning a leak or an error.')
    for k, vi, en in [('app', 'sống cùng Application', 'lives with Application'), ('vm', 'sống cùng ViewModel', 'lives with ViewModel'), ('act', 'sống cùng Activity', 'lives with Activity')]:
        z('di.band.' + k, vi, en)
    z('di.compileErr', 'Hilt: lỗi lúc biên dịch', 'Hilt: compile-time error')
    z('di.lg.hold', 'giữ tham chiếu (an toàn)', 'holds a reference (safe)'); z('di.lg.leak', 'sống lâu giữ sống ngắn: rò rỉ hay lỗi', 'long-lived holds short-lived: a leak or an error')
    for k, vi, en in [
        ('vmChoose', 'ChooseTimeViewModel', 'ChooseTimeViewModel'), ('vmResched', 'RescheduleViewModel', 'RescheduleViewModel'),
        ('repo1', 'SlotRepository bản 1', 'SlotRepository #1'), ('repo2', 'SlotRepository bản 2', 'SlotRepository #2'),
        ('db1', 'Cơ sở dữ liệu #1', 'Database #1'), ('db2', 'Cơ sở dữ liệu #2', 'Database #2'),
        ('repo1Fresh', 'Repository #1: cache mới', 'Repository #1: fresh cache'), ('repo2Stale', 'Repository #2: cache cũ', 'Repository #2: stale cache'),
        ('appContainer', 'AppContainer (trong Application)', 'AppContainer (in Application)'), ('repoShared', 'SlotRepository (một bản)', 'SlotRepository (one copy)'), ('dbShared', 'Cơ sở dữ liệu (một bản)', 'Database (one copy)'),
        ('hiltApp', 'Application có @HiltAndroidApp', '@HiltAndroidApp Application'), ('repoSingleton', 'SlotRepository có @Singleton', '@Singleton SlotRepository'),
        ('vmChooseHilt', '@HiltViewModel Chọn giờ', '@HiltViewModel ChooseTime'), ('vmReschedHilt', '@HiltViewModel Đổi lịch', '@HiltViewModel Reschedule'),
        ('actEntry', 'Activity có @AndroidEntryPoint', '@AndroidEntryPoint Activity'),
        ('objectContainer', 'AppContainer kiểu object', 'object AppContainer'), ('repoCtx', 'SlotRepository(Activity)', 'SlotRepository(Activity)'),
        ('act1', 'Activity #1', 'Activity #1'), ('act1Dead', 'Activity #1 (đã hủy)', 'Activity #1 (destroyed)'), ('act2', 'Activity #2', 'Activity #2'),
        ('application', 'Application', 'Application'), ('repoAppCtx', 'SlotRepository(@ApplicationContext)', 'SlotRepository(@ApplicationContext)'),
        ('repoActInject', 'SlotRepository nhận Activity?', 'SlotRepository(activity: Activity)?')]:
        z('di.o.' + k, vi, en)

    C = 'g6'
    a(C + '.title', 'Dependency injection: thủ công và Hilt', 'Dependency injection: manual and Hilt')
    a(C + '.essence', 'Dependency injection: lớp nhận phụ thuộc từ bên ngoài (qua constructor) thay vì tự tạo. Nhờ vậy dễ dùng lại, dễ đổi cài đặt và dễ thay bằng bản giả khi test.\nNơi tạo và giữ instance quyết định có bao nhiêu bản và chúng sống bao lâu. DI thủ công dùng một container đặt trong Application; Hilt sinh container (component) theo vòng đời của Application, ViewModel, Activity và kiểm đồ thị phụ thuộc lúc biên dịch.\nQuy tắc an toàn: object sống lâu không giữ object sống ngắn hơn. Singleton cần Context thì dùng context của Application.',
      'Dependency injection: a class receives its dependencies from outside (through its constructor) instead of creating them. That makes code easier to reuse, to switch implementations, and to replace with fakes in tests.\nWhere instances are created and held decides how many copies exist and how long they live. Manual DI uses a container held by the Application; Hilt generates containers (components) following the lifetimes of the Application, ViewModels and Activities, and checks the dependency graph at compile time.\nThe safety rule: a long-lived object does not hold a shorter-lived one. A singleton that needs a Context uses the Application context.')
    a(C + '.goal.g1', 'Đã thấy hai instance repository', 'Saw two repository instances')
    a(C + '.goal.g2', 'Đã đi hết bốn bước', 'Walked all four steps')
    a(C + '.sim.arch.di', 'ai tạo repository, và nó sống bao lâu', 'who creates the repository, and how long it lives')

    S_ = 'hook'
    a(C + '.sec.%s.title' % S_, 'Đoán trước khi đọc', 'Predict before reading')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'predict', 'Màn Chọn giờ và màn Đổi lịch mỗi ViewModel tự viết SlotRepository(...) trong thân lớp. Repository có bộ nhớ đệm danh sách giờ. Đặt lịch ở màn Chọn giờ xong, màn Đổi lịch có thấy giờ đó đã kín không?',
      'Choose a time and Reschedule each create SlotRepository(...) in their ViewModel body. The repository caches the slot list in memory. After booking on Choose a time, does Reschedule see that slot as taken?')
    B(C, S_, 1, 'ans', 'Không. Mỗi ViewModel có một repository riêng với bộ nhớ đệm riêng. Mô phỏng bên dưới đếm số instance và sửa bằng container thủ công, rồi bằng Hilt. [[src:ax-di]]',
      'No. Each ViewModel has its own repository with its own cache. The simulation below counts the instances and fixes it with a manual container, then with Hilt. [[src:ax-di]]')

    S_ = 'why'
    a(C + '.sec.%s.title' % S_, 'Dependency injection là gì và vì sao', 'What dependency injection is, and why')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'p', 'Một lớp có thể có phụ thuộc theo ba cách: tự tạo (gọi constructor bên trong), lấy từ một nơi toàn cục, hay nhận từ bên ngoài. Cách thứ ba là dependency injection. Trên Android có hai kiểu chính: truyền qua constructor, và gán vào field (dùng cho lớp Android như Activity mà ta không tự tạo). [[src:ax-di]]',
      'A class can get its dependencies in three ways: create them itself (call constructors inside), fetch them from a global place, or receive them from outside. The third is dependency injection. On Android the two main forms are constructor injection, and field injection (for Android classes such as Activities that we do not instantiate ourselves). [[src:ax-di]]')
    B(C, S_, 2, 'p', 'Lợi ích tài liệu nêu: dùng lại mã và đổi cài đặt dễ; refactor dễ vì phụ thuộc là một phần của API, kiểm được lúc tạo object hay lúc biên dịch; test dễ vì có thể đưa vào bản giả. Chương G1 đã dùng đúng điều này: ViewModel nhận repository qua constructor nên test thay được bằng repository giả. [[src:ax-di]]',
      'The benefits the docs list: easier reuse and swapping implementations; easier refactoring because dependencies are part of the API, checkable at creation or compile time; easier testing because fakes can be passed in. Chapter G1 already relied on this: the ViewModel takes its repository through the constructor, so tests swap in a fake. [[src:ax-di]]')

    S_ = 'manual'
    a(C + '.sec.%s.title' % S_, 'DI thủ công: container trong Application', 'Manual DI: a container in the Application')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'p', 'Khi nhiều nơi cần cùng một instance, tài liệu tạo một container (AppContainer) giữ các phụ thuộc dùng chung, và để lớp Application giữ một instance của container. Activity và ViewModel lấy phụ thuộc từ container. AppContainer là một lớp thường có một instance trong Application, không phải object singleton; singleton làm test khó vì mọi test dùng chung instance đó. [[src:ax-di-manual]]',
      'When several places need the same instance, the docs create a container (AppContainer) holding the shared dependencies, and let the Application class hold one instance of it. Activities and ViewModels get dependencies from the container. AppContainer is a regular class with one instance in the Application, not an object singleton; singletons make testing harder because every test shares that instance. [[src:ax-di-manual]]')
    B(C, S_, 2, 'kt', 'class AppContainer(app: Application) {\n    private val db = AppDatabase.create(app)\n    val slotRepository = SlotRepository(SlotApi(), db.slotDao())\n}\nclass ClinicApp : Application() {\n    val container by lazy { AppContainer(this) }\n}\n// ViewModel nhận repository qua constructor; factory lấy từ container',
      'class AppContainer(app: Application) {\n    private val db = AppDatabase.create(app)\n    val slotRepository = SlotRepository(SlotApi(), db.slotDao())\n}\nclass ClinicApp : Application() {\n    val container by lazy { AppContainer(this) }\n}\n// the ViewModel takes the repository in its constructor; a factory gets it from the container')
    B(C, S_, 3, 'note', 'DI thủ công đủ cho app nhỏ, nhưng mã nối (factory cho ViewModel, container theo từng luồng màn hình) tăng nhanh khi app lớn. Đó là lý do có Hilt.', 'Manual DI is enough for small apps, but the wiring code (ViewModel factories, per-flow containers) grows fast as the app grows. That is why Hilt exists.')

    S_ = 'hilt'
    a(C + '.sec.%s.title' % S_, 'Hilt: component, scope và vòng đời', 'Hilt: components, scopes and lifetimes')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'p', 'Hilt sinh một component cho mỗi loại lớp Android inject được: SingletonComponent cho Application, ViewModelComponent cho ViewModel, ActivityComponent cho Activity, ServiceComponent cho Service. Mỗi component được tạo và hủy theo vòng đời của lớp tương ứng: SingletonComponent từ Application.onCreate tới khi Application bị hủy; ActivityComponent từ Activity.onCreate tới onDestroy; ViewModelComponent cùng ViewModel. [[src:ax-hilt]]',
      'Hilt generates a component for each kind of injectable Android class: SingletonComponent for the Application, ViewModelComponent for ViewModels, ActivityComponent for Activities, ServiceComponent for Services. Each component is created and destroyed with its class: SingletonComponent from Application.onCreate until the Application is destroyed; ActivityComponent from Activity.onCreate to onDestroy; ViewModelComponent with the ViewModel. [[src:ax-hilt]]')
    B(C, S_, 2, 'p', 'Mặc định mọi binding không có scope: mỗi lần yêu cầu Hilt tạo một instance mới. Gắn scope (@Singleton, @ViewModelScoped, @ActivityScoped) thì Hilt tạo binding một lần cho mỗi instance của component đó và mọi yêu cầu dùng chung. Binding có scope nằm trong bộ nhớ tới khi component bị hủy, nên tài liệu khuyên hạn chế dùng scope, chỉ dùng khi cần chia sẻ trạng thái. [[src:ax-hilt]]',
      'By default every binding is unscoped: each request makes Hilt create a new instance. With a scope (@Singleton, @ViewModelScoped, @ActivityScoped), Hilt creates the binding once per instance of that component and every request shares it. A scoped binding stays in memory until its component is destroyed, so the docs advise minimising scopes and using them when state must be shared. [[src:ax-hilt]]')
    B(C, S_, 3, 'p', 'Mỗi component có sẵn vài binding mặc định: SingletonComponent có Application; ViewModelComponent có SavedStateHandle; ActivityComponent có Application và Activity. Cần Context thì chọn bằng qualifier @ApplicationContext hay @ActivityContext. Vì một binding chỉ dùng được phụ thuộc của component nó và các component cha, đưa Activity vào một binding @Singleton sẽ không biên dịch được. [[src:ax-hilt]]',
      'Each component comes with a few default bindings: SingletonComponent has Application; ViewModelComponent has SavedStateHandle; ActivityComponent has Application and Activity. When you need a Context, pick it with the @ApplicationContext or @ActivityContext qualifier. Since a binding can only use dependencies from its own component and its parents, putting an Activity into a @Singleton binding does not compile. [[src:ax-hilt]]')

    S_ = 'bugs'
    a(C + '.sec.%s.title' % S_, 'Hai lỗi hay gặp', 'Two common bugs')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'bug', 'Đặt lịch ở màn Chọn giờ xong, màn Đổi lịch vẫn hiện giờ đó còn trống cho tới khi khởi động lại app.', 'After booking on Choose a time, Reschedule still shows the slot as free until the app restarts.')
    B(C, S_, 1, 'cause', 'Mỗi ViewModel tự tạo SlotRepository (hay binding Hilt thiếu scope), nên có hai instance với hai bộ nhớ đệm.', 'Each ViewModel creates its own SlotRepository (or the Hilt binding lacks a scope), so there are two instances with two caches.')
    B(C, S_, 1, 'fix', 'Một nơi tạo và giữ repository: container trong Application, hay @Singleton trong Hilt. Tốt hơn nữa, để database làm nguồn sự thật (chương G4).', 'Create and hold the repository in one place: a container in the Application, or @Singleton in Hilt. Better still, make the database the source of truth (chapter G4).')
    B(C, S_, 2, 'bug', 'Mỗi lần xoay màn hình, bộ nhớ của app tăng thêm vài MB và không giảm.', 'Each rotation adds a few MB to the app\'s memory that never goes away.')
    B(C, S_, 2, 'cause', 'Một singleton (object hay @Singleton) được tạo với Activity làm Context, nên giữ Activity đã hủy và toàn bộ cây View của nó.', 'A singleton (an object or @Singleton) was built with an Activity as its Context, so it holds the destroyed Activity and its whole View tree.')
    B(C, S_, 2, 'fix', 'Dùng context của Application (@ApplicationContext). Object chỉ cần Activity thì đặt ở scope Activity.', 'Use the Application context (@ApplicationContext). Objects that really need the Activity belong in the Activity scope.')

    S_ = 'ex'
    a(C + '.sec.%s.title' % S_, 'Bài tập', 'Exercise')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'ex', 'Chọn scope Hilt cho từng lớp và giải thích: (a) AppDatabase; (b) BookingFormState giữ dữ liệu một màn đặt lịch đang điền dở; (c) PermissionLauncher cần Activity để xin quyền; (d) PriceFormatter không có trạng thái. (Bài tập của site, theo bảng component và scope trong trang Hilt.) [[src:ax-hilt]]',
      'Pick a Hilt scope for each class and explain: (a) AppDatabase; (b) BookingFormState holding the half-filled data of one booking screen; (c) PermissionLauncher, which needs the Activity to request permissions; (d) PriceFormatter, which has no state. (The site\'s own exercise, after the components and scopes tables on the Hilt page.) [[src:ax-hilt]]')
    B(C, S_, 1, 'hint', 'Hỏi: có cần đúng một bản dùng chung không, và nó cần sống bao lâu, so với thứ nó phụ thuộc.', 'Ask: must there be exactly one shared copy, and how long must it live, compared with what it depends on?')
    B(C, S_, 1, 'sol', '(a) @Singleton: một bản cho cả app, sống cùng Application. (b) @ViewModelScoped (hay để trong ViewModel): sống qua xoay màn hình, mất khi rời màn. (c) @ActivityScoped hay không scope, cài trong ActivityComponent: cần Activity nên không được sống lâu hơn Activity. (d) Không scope: không có trạng thái để chia sẻ, tạo mới rẻ.',
      '(a) @Singleton: one copy for the app, living with the Application. (b) @ViewModelScoped (or inside the ViewModel): survives rotation, gone when leaving the screen. (c) @ActivityScoped or unscoped, installed in ActivityComponent: it needs the Activity, so it must not outlive it. (d) Unscoped: no state to share, cheap to create.')

    S_ = 'recall'
    a(C + '.sec.%s.title' % S_, 'Tự trả lời', 'Answer it yourself')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'ask', 'Binding Hilt không có scope thì mỗi lần yêu cầu nhận được gì?', 'What does each request get from an unscoped Hilt binding?')
    B(C, S_, 1, 'ans', 'Một instance mới.', 'A new instance.')
    B(C, S_, 2, 'ask', 'Singleton cần Context thì dùng Context nào, và vì sao?', 'Which Context should a singleton use, and why?')
    B(C, S_, 2, 'ans', 'Context của Application, vì nó sống ít nhất lâu bằng singleton; giữ Activity thì rò rỉ Activity đã hủy.', 'The Application context, because it lives at least as long as the singleton; holding an Activity leaks it once destroyed.')

    for q, qv, qe, av, ae, wv, we in [
        ('q1', 'SingletonComponent sống bao lâu?', 'How long does SingletonComponent live?', 'Từ Application.onCreate tới khi Application bị hủy.', 'From Application.onCreate until the Application is destroyed.', 'Theo bảng vòng đời component của Hilt.', 'Per Hilt\'s component lifetimes table.'),
        ('q2', '@Singleton làm gì với một binding?', 'What does @Singleton do to a binding?', 'Tạo một lần cho SingletonComponent; mọi yêu cầu dùng chung.', 'Creates it once for SingletonComponent; every request shares it.', 'Không scope thì mỗi lần một instance mới.', 'Unscoped, each request gets a new instance.'),
        ('q3', 'Binding mặc định nào có trong ActivityComponent?', 'Which default bindings does ActivityComponent have?', 'Application và Activity.', 'Application and Activity.', 'SingletonComponent chỉ có Application.', 'SingletonComponent has only Application.'),
        ('q4', 'Vì sao AppContainer của DI thủ công không nên là object?', 'Why should a manual-DI AppContainer not be an object?', 'Singleton làm test khó vì mọi test dùng chung instance.', 'Singletons make testing harder because all tests share the instance.', 'Tài liệu đặt nó làm một instance trong Application.', 'The docs keep it as one instance in the Application.')]:
        a(C + '.quiz.%s.q' % q, qv, qe); a(C + '.quiz.%s.a' % q, av, ae); a(C + '.quiz.%s.why' % q, wv, we)
