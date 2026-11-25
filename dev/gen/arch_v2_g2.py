# Kiến trúc · G2: các tầng, hướng phụ thuộc, SSOT, UDF (Phần 1)
# Nguồn: developer.android.com Guide to app architecture, UI layer, Data layer, Domain layer, Modularization, Common modularization patterns
# (đọc 2026-11-24); kotlinlang Visibility modifiers; Boudjnah ch1 (Dependency Rule, đảo phụ thuộc) và ch2 (các tầng, domain có repository interface).
# Trần: 8 mục, mục cơ chế ≤ 4 khối.

SEC_ORDER = {'g2': ['hook', 'layers', 'direction', 'ssot', 'bugs', 'ex', 'recall']}


def add(a):
    def B(ch, sec, n, field, vi, en=None):
        a('%s.sec.%s.b.%02d.%s' % (ch, sec, n, field), vi, vi if en is None else en)

    # ---------------- sim G2a: đồ thị phụ thuộc ----------------
    m = lambda k, vi, en=None: a('m.layers.' + k, vi, en)
    m('title', 'Ai biết về ai: hướng phụ thuộc giữa các tầng', 'Who knows about whom: the direction of dependencies between layers')
    m('overview', 'Màn Chọn giờ có năm lớp: màn hình, ViewModel, use case (lớp chứa một quy tắc nghiệp vụ), repository và hai nguồn dữ liệu (mạng, database). Mỗi mũi tên nghĩa là "lớp này import và gọi lớp kia". Bốn tình huống: (1) theo hướng dẫn chính thức của Android; (2) repository import nhầm một lớp giao diện khi mọi thứ nằm trong một module; (3) cùng lỗi đó khi đã tách module Gradle; (4) đảo phụ thuộc theo cách của Robert C. Martin.',
      'The Choose a time screen has five classes: the screen, the ViewModel, a use case (a class holding one business rule), a repository and two data sources (network, database). Each arrow means "this class imports and calls that one". Four cases: (1) the official Android guide\'s layout; (2) the repository imports a UI class by mistake while everything is in one module; (3) the same mistake once the code is split into Gradle modules; (4) inverting the dependency the way Robert C. Martin does.')
    m('wrapup', 'Mũi tên phụ thuộc chỉ đi một chiều: tầng trên biết tầng dưới, tầng dưới không biết tầng trên. Dữ liệu vẫn đi ngược lên, qua giá trị trả về và Flow. Trong một module, không công cụ nào chặn một import sai chiều; tách module Gradle biến nó thành lỗi biên dịch, và Gradle không cho hai module phụ thuộc vòng. Robert C. Martin còn đảo mũi tên giữa domain và data bằng một interface, để domain không phụ thuộc gì.\nQuy tắc dễ nhớ: lời gọi đi xuống, dữ liệu đi lên, còn import thì không bao giờ đi lên.',
      'Dependency arrows point one way: upper layers know lower ones, lower layers do not know upper ones. Data still flows back up, through return values and Flows. Within one module, no tool stops an import in the wrong direction; splitting into Gradle modules turns it into a compile error, and Gradle refuses modules that depend on each other in a cycle. Robert C. Martin goes further and inverts the arrow between domain and data with an interface, so the domain depends on nothing.\nRule of thumb: calls go down, data comes up, and imports never go up.')
    m('simp.1', 'Mỗi tầng chỉ vẽ một lớp đại diện. App thật có nhiều repository, nhiều use case và có thể không có use case nào (domain là tùy chọn).', 'Each layer is drawn as one representative class. A real app has many repositories and use cases, and may have no use case at all (the domain layer is optional).')
    m('simp.2', 'Kết quả build là mô tả theo cách Kotlin và Gradle xử lý import và phụ thuộc giữa module; site không chạy Gradle, và thông báo lỗi thật có thể khác chữ. Nguyên lý theo tài liệu chính thức của Android và Kotlin (đọc ngày 2026-11-24). Chương chưa nói về các công cụ kiểm tra kiến trúc ngoài Gradle (lint tự viết, test kiến trúc) và cách chia module chi tiết (chương G9, "Module hóa").',
      'The build results describe how Kotlin and Gradle treat imports and module dependencies; the site does not run Gradle, and real error messages may be worded differently. The principles follow the official Android and Kotlin docs (read on 2026-11-24). The chapter does not cover architecture-checking tools beyond Gradle (custom lint, architecture tests) or detailed module design (chapter G9, "Modularization").')
    m('ctl.hint', 'Đổi tình huống rồi đi lại bốn bước; xem tab "Đồ thị phụ thuộc" và dòng Build bên dưới hình.', 'Switch the case and walk the four steps again; watch the "Dependency graph" tab and the Build line under it.')
    m('ctl.case', 'Tình huống', 'Case')
    for k, vi, en in [('google', 'theo hướng dẫn chính thức', 'the official guide'), ('wrong', 'một module, import sai chiều', 'one module, a wrong-way import'),
                      ('modules', 'tách module Gradle', 'separate Gradle modules'), ('inverted', 'đảo phụ thuộc (kiểu Robert C. Martin)', 'inverted dependency (Robert C. Martin style)')]:
        m('ctl.case.' + k, vi, en)
    m('diagramTitle', 'UI, ViewModel, use case, repository, nguồn dữ liệu', 'UI, ViewModel, use case, repository, data sources')
    m('diagramDesc', 'Các lớp của màn Chọn giờ từ trái sang phải; mũi tên là phụ thuộc', 'The Choose a time classes left to right; arrows are dependencies')
    for k, vi, en in [('ui', 'Màn hình', 'Screen'), ('vm', 'ViewModel', 'ViewModel'), ('uc', 'Use case', 'Use case'), ('repo', 'Repository', 'Repository'), ('api', 'Nguồn mạng', 'Network source'), ('dao', 'Cơ sở dữ liệu (DAO)', 'Database (DAO)')]:
        m('n.' + k, vi, en)
    m('met.wrong', 'Phụ thuộc sai chiều', 'Wrong-way dependencies'); m('met.caught', 'Ai bắt được', 'Caught by'); m('met.test', 'Test repository chạy ở', 'Repository tests run on')
    for k, vi, en in [('na', 'chưa build', 'not built yet'), ('none', 'không ai (build vẫn qua)', 'nobody (the build passes)'), ('compiler', 'trình biên dịch', 'the compiler'), ('gradle', 'Gradle (chặn vòng phụ thuộc)', 'Gradle (blocks the cycle)')]:
        m('caught.' + k, vi, en)
    for k, vi, en in [('jvm', 'máy phát triển (JVM)', 'your machine (JVM)'), ('device', 'cần Android (Context, tài nguyên)', 'needs Android (Context, resources)')]:
        m('test.' + k, vi, en)
    a('cap.layers', 'Từ trái sang phải: màn hình, ViewModel, use case, repository, rồi hai nguồn dữ liệu. Mỗi mũi tên là một phụ thuộc. Hạt chạy theo mũi tên là lời gọi; hạt chạy ngược là dữ liệu trả về. Khối viền đỏ dính vào phụ thuộc sai chiều. Tab "Đồ thị phụ thuộc" vẽ đủ các cạnh, kể cả cạnh sai.',
      'Left to right: screen, ViewModel, use case, repository, then the two data sources. Each arrow is a dependency. A dot moving along an arrow is a call; one moving against it is returned data. A red-outlined box is involved in a wrong-way dependency. The "Dependency graph" tab draws every edge, including the wrong one.')
    S = [
        ('google', 's1', 'Vẽ phụ thuộc: tầng trên biết tầng dưới', 'Draw the dependencies: upper layers know lower ones',
         'Màn hình nhận ViewModel, ViewModel nhận use case, use case nhận repository, repository nhận hai nguồn dữ liệu, tất cả qua constructor. Mũi tên đọc là "biết về": màn hình biết ViewModel, nhưng ViewModel không biết màn hình nào đang hiển thị nó.',
         'The screen receives the ViewModel, the ViewModel the use case, the use case the repository, the repository the two data sources, all through constructors. Read an arrow as "knows about": the screen knows the ViewModel, but the ViewModel does not know which screen displays it.'),
        ('google', 's2', 'Dữ liệu đi ngược chiều mũi tên', 'Data flows against the arrows',
         'Repository trả Flow<List<Slot>> lấy từ DAO; Flow đó đi lên qua use case và ViewModel tới màn hình. Không lớp dưới nào phải import lớp trên để dữ liệu đi lên: nó đi qua giá trị trả về.',
         'The repository returns a Flow<List<Slot>> from the DAO; that Flow travels up through the use case and the ViewModel to the screen. No lower class has to import an upper one for data to go up: it travels through return values.'),
        ('google', 's3', 'Domain là tùy chọn: bỏ use case', 'The domain layer is optional: drop the use case',
         'Nếu use case chỉ chuyển nguyên lời gọi, ViewModel có thể gọi thẳng repository. Hướng mũi tên vẫn giữ: UI → data. Hướng dẫn chính thức chỉ bắt buộc hai tầng UI và data.',
         'If the use case only forwards the call, the ViewModel can call the repository directly. The arrows keep their direction: UI → data. The official guide requires only the UI and data layers.'),
        ('google', 's4', 'Test repository trên máy, không cần thiết bị', 'Test the repository on your machine, no device',
         'Repository chỉ biết hai nguồn dữ liệu qua constructor, nên test đưa vào hai bản giả và chạy trên JVM. Nó không dính vào lớp UI hay Context nào.',
         'The repository knows only its two data sources, through its constructor, so a test passes in two fakes and runs on the JVM. It is not tied to any UI class or Context.'),
        ('wrong', 's1', 'Yêu cầu mới: hiện giờ dạng "Lúc 9:00"', 'A new request: show times as "At 9:00"',
         'Cả app nằm trong một module :app. Người viết repository muốn trả thẳng danh sách SlotChipUi, lớp mà màn hình dùng để vẽ các ô giờ, kèm chuỗi đã dịch.',
         'The whole app lives in one :app module. Whoever writes the repository wants to return a list of SlotChipUi, the class the screen uses to draw time chips, with translated text already in it.'),
        ('wrong', 's2', 'Repository import một lớp UI và nhận Context', 'The repository imports a UI class and takes a Context',
         'Thêm import com.henkham.ui.slots.SlotChipUi và một tham số Context để gọi getString. Giờ có một mũi tên đi ngược: repository → UI. Màn hình đã phụ thuộc repository (qua ViewModel), nên hai bên phụ thuộc nhau thành vòng.',
         'Add import com.henkham.ui.slots.SlotChipUi and a Context parameter to call getString. Now an arrow points the wrong way: repository → UI. The screen already depends on the repository (through the ViewModel), so the two now depend on each other in a loop.'),
        ('wrong', 's3', 'Build: vẫn qua, không ai báo gì', 'Build: still passes, nobody complains',
         'Trong cùng một module, mọi lớp public đều import được và vòng phụ thuộc giữa các lớp là hợp lệ với trình biên dịch. Không có công cụ mặc định nào biết rằng "repository không được biết UI"; quy tắc này chỉ nằm trong đầu người viết.',
         'Within one module every public class can be imported, and a loop between classes is legal for the compiler. No default tool knows that "a repository must not know the UI"; the rule lives only in people\'s heads.'),
        ('wrong', 's4', 'Hậu quả: test cần Android, sửa UI làm vỡ data', 'The cost: tests need Android, UI changes break data',
         'Test repository giờ phải có Context (đối tượng cho phép truy cập tài nguyên của app) và chuỗi văn bản, nên không chạy thuần trên JVM (máy ảo Java trên máy tính) được. Đổi giao diện ô giờ (SlotChipUi) bắt sửa cả repository. Ba màn hình khác dùng repository này cũng kéo theo lớp UI của màn Chọn giờ.',
         'Repository tests now need a Context (the object that gives access to the app\'s resources) and string resources, so they no longer run on the plain JVM (the Java virtual machine on your computer). Changing the chip design (SlotChipUi) forces a repository change. Three other screens that use this repository also drag in the Choose a time screen\'s UI class.'),
        ('modules', 's1', 'Tách ba module: feature, domain, data', 'Split into three modules: feature, domain, data',
         ':feature:slots chứa màn hình và ViewModel, :core:domain chứa use case, :core:data chứa repository và nguồn dữ liệu. Mỗi module khai báo nó phụ thuộc module nào trong build.gradle.kts; :core:data không khai báo :feature:slots.',
         ':feature:slots holds the screen and ViewModel, :core:domain the use case, :core:data the repository and data sources. Each module declares its dependencies in build.gradle.kts; :core:data does not declare :feature:slots.'),
        ('modules', 's2', 'Cùng import sai: lỗi biên dịch ngay', 'The same wrong import: an immediate compile error',
         'Khi biên dịch :core:data, các lớp của :feature:slots không nằm trên classpath của nó, nên import SlotChipUi báo Unresolved reference (không tìm thấy tên này). Quy tắc hướng phụ thuộc giờ do công cụ kiểm, không cần người review nhớ.',
         'When :core:data is compiled, the :feature:slots classes are not on its classpath, so importing SlotChipUi fails with Unresolved reference (this name cannot be found). The dependency rule is now checked by tools, not by a reviewer\'s memory.'),
        ('modules', 's3', '"Sửa" bằng cách thêm phụ thuộc: Gradle chặn vòng', '"Fixing" it by adding a dependency: Gradle blocks the cycle',
         'Thêm implementation(project(":feature:slots")) vào :core:data. Nhưng :feature:slots đã phụ thuộc :core:domain, và :core:domain phụ thuộc :core:data, nên ba module thành một vòng. Gradle không build được vòng phụ thuộc giữa các project.',
         'Add implementation(project(":feature:slots")) to :core:data. But :feature:slots already depends on :core:domain, which depends on :core:data, so the three modules form a loop. Gradle cannot build a dependency cycle between projects.'),
        ('modules', 's4', 'Sửa đúng: đổi sang mô hình UI ở ViewModel', 'The right fix: map to the UI model in the ViewModel',
         'Repository trả Slot (mô hình dữ liệu); ViewModel đổi Slot thành SlotChipUi bằng tài nguyên của tầng UI. Không còn cạnh sai chiều, build qua, và quy tắc vẫn được công cụ giữ cho các lần sửa sau.',
         'The repository returns Slot (a data model); the ViewModel turns Slot into SlotChipUi using UI-layer resources. No wrong-way edge remains, the build passes, and the tools keep enforcing the rule for future changes.'),
        ('inverted', 's1', 'Câu hỏi khác: domain có nên biết data?', 'Another question: should the domain know the data layer?',
         'Theo hướng dẫn chính thức, use case phụ thuộc repository: domain biết data. Eran Boudjnah theo Dependency Rule (quy tắc phụ thuộc) của Robert C. Martin: mũi tên phải hướng vào domain, tầng chứa quy tắc nghiệp vụ, để thay đổi ở API hay database không lan vào nó.',
         'In the official guide, the use case depends on the repository: the domain knows the data layer. Eran Boudjnah follows Robert C. Martin\'s Dependency Rule: arrows must point toward the domain, the layer holding business rules, so changes to the API or database do not reach it.'),
        ('inverted', 's2', 'Đặt interface repository vào domain', 'Put the repository interface in the domain',
         'Domain khai báo interface SlotRepository (bản mô tả các hàm, chưa có thân) cạnh use case. Data viết lớp OfflineFirstSlotRepository cài đặt interface đó. Lời gọi vẫn đi từ use case xuống cài đặt, nhưng mũi tên phụ thuộc giờ đi từ data lên domain.',
         'The domain declares interface SlotRepository (a list of functions with no bodies yet) next to the use case. The data layer writes OfflineFirstSlotRepository implementing it. Calls still go from the use case down to the implementation, but the dependency arrow now points from data up to the domain.'),
        ('inverted', 's3', 'Domain không phụ thuộc module nào', 'The domain depends on no module',
         'Domain chỉ còn use case, mô hình và interface, viết bằng Kotlin thuần. Nó có thể là một module không biết Android, Room hay Retrofit, và test được hoàn toàn trên JVM.',
         'The domain now holds only use cases, models and interfaces, in plain Kotlin. It can be a module that knows nothing of Android, Room or Retrofit, fully testable on the JVM.'),
        ('inverted', 's4', 'Giá phải trả: thêm interface và phần nối', 'The price: more interfaces and wiring',
         'Ai đó phải nối interface với cài đặt: module app, qua DI (dependency injection, chương G6). Mỗi repository có thêm một interface, thường thêm mapper giữa mô hình data và domain. Đáng giá khi domain lớn hay được nhiều nơi dùng; thừa với màn hình chỉ đọc một danh sách.',
         'Someone has to bind the interface to the implementation: the app module, through DI (dependency injection, chapter G6). Every repository gains an interface, and usually a mapper between data and domain models. Worth it when the domain is large or shared; overkill for a screen that reads one list.'),
    ]
    for case, k, tv, te, xv, xe in S:
        sid = case + '.' + k
        m('s.%s.title' % sid, tv, te); m('s.%s.explain' % sid, xv, xe); m('ev.' + sid, tv, te)
    for k, vi, en in [
        ('try', 'Đi bốn bước của từng tình huống; mở tab "Đồ thị phụ thuộc" để thấy mọi mũi tên và dòng Build.', 'Walk the four steps of each case; open the "Dependency graph" tab to see every arrow and the Build line.'),
        ('google.s2', 'Hướng dẫn kiến trúc của Android nói: mũi tên trong các sơ đồ là phụ thuộc giữa các lớp, ví dụ domain phụ thuộc lớp của data. [[src:ax-arch-guide]]', 'The Android architecture guide says: the arrows in its diagrams are dependencies between classes, for example the domain layer depends on data layer classes. [[src:ax-arch-guide]]'),
        ('google.s3', 'Tài liệu Android nói: domain là tầng tùy chọn nằm giữa UI và data; use case thường phụ thuộc repository. [[src:ax-domain-layer]]', 'The Android docs say: the domain layer is optional and sits between UI and data; use cases usually depend on repositories. [[src:ax-domain-layer]]'),
        ('google.s4', 'Tài liệu Android nói: repository là lối vào duy nhất của data layer; tầng khác không bao giờ dùng thẳng data source. [[src:ax-data-layer]]', 'The Android docs say: repositories are the only entry point to the data layer; other layers never use data sources directly. [[src:ax-data-layer]]'),
        ('wrong.s2', 'Eran Boudjnah đọc mũi tên là "biết về": Activity biết ViewModel, điều ngược lại thì không. Repository biết SlotChipUi là phá đúng quy tắc đó. [[src:book-boudjnah]]', 'Eran Boudjnah reads the arrows as "knows about": Activities know ViewModels, not the other way round. A repository that knows SlotChipUi breaks exactly that rule. [[src:book-boudjnah]]'),
        ('wrong.s3', 'Tài liệu Kotlin nói: module là tập file biên dịch cùng nhau; trong một module, khai báo public và internal đều thấy được ở mọi file. [[src:kt-visibility]]', 'The Kotlin docs say: a module is a set of files compiled together; inside one module, public and internal declarations are visible from every file. [[src:kt-visibility]]'),
        ('wrong.s4', 'Đây là lý do chương G1 nhấn mạnh tách mối quan tâm: lớp data dính vào UI thì mất cả khả năng test trên máy lẫn khả năng dùng lại.', 'This is why chapter G1 stresses separation of concerns: a data class tied to the UI loses both on-machine testing and reuse.'),
        ('modules.s2', 'Tài liệu Android về module hóa nói: module cho phép kiểm soát chặt phần lộ ra ngoài; đánh dấu internal mọi thứ trừ giao diện công khai. [[src:ax-modularization]]', 'The Android modularization guide says: modules give strict control over what is visible; mark everything but the public interface internal. [[src:ax-modularization]]'),
        ('modules.s3', 'Tài liệu Android nói: hai module không thể gọi thẳng lẫn nhau vì phụ thuộc vòng; cần một module trung gian. [[src:ax-modularization-patterns]]', 'The Android docs say: two modules cannot talk directly to each other because of cyclic dependencies; a mediating module is needed. [[src:ax-modularization-patterns]]'),
        ('modules.s4', 'Đổi mô hình data sang mô hình UI là việc của state holder ở tầng UI; chương G3 nói về UiState. [[src:ax-ui-layer]]', 'Turning data models into UI models is the UI-layer state holder\'s job; chapter G3 covers UiState. [[src:ax-ui-layer]]'),
        ('inverted.s2', 'Eran Boudjnah giải thích: để giữ Dependency Rule, không cho use case phụ thuộc repository cụ thể mà đưa vào interface repository, đặt cạnh use case; cài đặt nằm chỗ khác. [[src:book-boudjnah]]', 'Eran Boudjnah explains: to keep the Dependency Rule, use cases do not depend on concrete repositories; repository interfaces are defined next to the use cases and implemented elsewhere. [[src:book-boudjnah]]'),
        ('inverted.s3', 'Eran Boudjnah mô tả: domain là tầng trong cùng, chứa use case, mô hình domain và interface repository, và nên dựa vào càng ít thư viện càng tốt. [[src:book-boudjnah]]', 'Eran Boudjnah describes it: the domain is the innermost layer, holding use cases, domain models and repository interfaces, and should rely on as few libraries as possible. [[src:book-boudjnah]]'),
        ('inverted.s4', 'Tài liệu Android cũng dùng ý này ở mức module: module cao và module cài đặt cùng phụ thuộc một module trừu tượng. [[src:ax-modularization-patterns]]', 'The Android docs use the same idea at module level: high-level and implementation modules both depend on an abstraction module. [[src:ax-modularization-patterns]]')]:
        m('co.' + k, vi, en)
    a('preset.layers', 'Kiến trúc · hướng phụ thuộc và import sai chiều', 'Architecture · dependency direction and a wrong-way import')

    # chuỗi của hình đồ thị phụ thuộc (views/visuals.js)
    z = lambda k, vi, en=None: a('vz.' + k, vi, en)
    z('tab.dg', 'Đồ thị phụ thuộc', 'Dependency graph')
    z('dg.cap', 'Mỗi mũi tên nghĩa là "lớp này import và gọi lớp kia". Tầng trên ở trên cùng; mũi tên đỏ đứt nét là phụ thuộc sai chiều.', 'Each arrow means "this class imports and calls that one". Upper layers are at the top; a dashed red arrow is a wrong-way dependency.')
    z('dg.dataUp', 'dữ liệu đi lên (Flow)', 'data goes up (Flow)')
    z('dg.badEdge', 'import sai chiều', 'wrong-way import')
    for k, vi, en, cv, ce in [('ui', 'Màn hình (UI)', 'Screen (UI)', 'ChooseTimeScreen', 'ChooseTimeScreen'), ('vm', 'ViewModel (tầng UI)', 'ViewModel (UI)', 'ChooseTimeViewModel', 'ChooseTimeViewModel'),
                              ('uc', 'Use case (tầng domain)', 'Use case (domain)', 'GetFreeSlotsUseCase', 'GetFreeSlotsUseCase'), ('repo', 'Repository (tầng data)', 'Repository (data)', 'SlotRepository', 'SlotRepository'),
                              ('api', 'Nguồn mạng', 'Network source', 'SlotApi', 'SlotApi'), ('dao', 'Cơ sở dữ liệu', 'Database', 'SlotDao (dùng Room)', 'SlotDao (Room)')]:
        z('n.' + k, vi, en); z('n.%s.cls' % k, cv, ce)
    z('n.ucIface', 'use case và interface SlotRepository', 'use case + SlotRepository interface')
    z('n.repoImpl', 'OfflineFirstSlotRepository (cài đặt)', 'OfflineFirstSlotRepository : SlotRepository')
    z('n.ucSkip', '(không dùng use case)', '(no use case)')
    z('mod.feature', ':feature:slots', ':feature:slots'); z('mod.domain', ':core:domain', ':core:domain'); z('mod.data', ':core:data', ':core:data')
    z('build.label', 'Build', 'Build')
    for k, vi, en in [('na', 'chưa chạy', 'not run yet'), ('pass', 'qua', 'passes'), ('unresolved', 'lỗi biên dịch ở :core:data: Unresolved reference SlotChipUi', 'compile error in :core:data: Unresolved reference SlotChipUi'),
                      ('cycle', 'Gradle từ chối: phụ thuộc vòng :core:data → :feature:slots → :core:domain → :core:data', 'Gradle refuses: a dependency cycle :core:data → :feature:slots → :core:domain → :core:data')]:
        z('build.' + k, vi, en)
    z('lg.dep', 'phụ thuộc: A biết về B', 'dependency: A knows about B'); z('lg.bad', 'phụ thuộc sai chiều', 'wrong-way dependency')
    z('lg.data', 'dữ liệu đi ngược lên', 'data flowing back up'); z('lg.mod', 'module Gradle', 'Gradle module')

    # ---------------- sim G2b: SSOT và UDF ----------------
    m = lambda k, vi, en=None: a('m.ssot.' + k, vi, en)
    m('title', 'Một nguồn sự thật: hai màn hình, một danh sách lịch hẹn', 'One source of truth: two screens, one list of appointments')
    m('overview', 'Màn Chọn giờ đặt lịch, màn Lịch của tôi hiện và hủy lịch. Cách (1): mỗi nơi giữ một danh sách riêng và repository lộ ra một MutableList ai cũng sửa được. Cách (2): repository là nguồn sự thật duy nhất, lộ ra Flow chỉ đọc, và chỉ đổi dữ liệu qua hàm book() và cancel().',
      'Choose a time books appointments; My appointments shows and cancels them. Approach (1): each place keeps its own list and the repository exposes a MutableList anyone can change. Approach (2): the repository is the single source of truth, exposes a read-only Flow, and changes data only through book() and cancel().')
    m('wrapup', 'Khi một dữ liệu có nhiều bản và nhiều chỗ được sửa, các màn hình sớm muộn sẽ lệch nhau. Một nguồn sự thật (SSOT) giữ dữ liệu ở một chỗ, lộ nó ra dưới kiểu không sửa được, và nhận thay đổi qua hàm. Đi kèm là luồng một chiều (UDF): sự kiện đi lên nguồn sự thật, state đi xuống mọi màn hình đang quan sát.\nHình dung: một bảng tin chung ở sảnh. Ai muốn đổi lịch thì báo lễ tân, không ai tự sửa bản chép tay của mình.',
      'When a piece of data has several copies and several places that change it, screens drift apart sooner or later. A single source of truth (SSOT) keeps the data in one place, exposes it as a type that cannot be changed, and takes changes through functions. It comes with one-way flow (UDF): events go up to the source of truth, state comes down to every screen observing it.\nPicture a shared notice board in the lobby. Anyone who wants a change tells the front desk; nobody edits their own handwritten copy.')
    m('simp.1', 'Hai màn hình và một repository; app thật có database làm nguồn sự thật bên dưới repository (chương G4).', 'Two screens and one repository; a real app has a database as the source of truth under the repository (chapter G4).')
    m('ctl.hint', 'Đi hết bốn bước của mỗi cách; so ba số đo ở bước cuối.', 'Walk all four steps of each approach; compare the three metrics at the last step.')
    m('ctl.case', 'Cách giữ dữ liệu', 'How data is held')
    m('ctl.case.twowriters', 'nhiều bản, nhiều chỗ sửa', 'many copies, many writers'); m('ctl.case.ssot', 'một nguồn sự thật', 'single source of truth')
    m('diagramTitle', 'Hai màn hình quanh một repository', 'Two screens around one repository')
    m('diagramDesc', 'Sự kiện đi từ màn hình lên repository; state đi từ repository xuống màn hình', 'Events go from the screens up to the repository; state comes down from the repository to the screens')
    for k, vi, en in [('choose', 'Màn Chọn giờ', 'Choose a time'), ('repo', 'BookingRepository', 'BookingRepository'), ('mine', 'Màn Lịch của tôi', 'My appointments')]:
        m('n.' + k, vi, en)
    m('met.copies', 'Số bản danh sách', 'Copies of the list'); m('met.writers', 'Số chỗ sửa được', 'Places that can change it'); m('met.agree', 'Hai màn hình khớp nhau', 'The two screens agree')
    for k, vi, en in [('na', 'chưa xét', 'not yet'), ('yes', 'khớp', 'yes'), ('no', 'lệch', 'no, they differ')]:
        m('agree.' + k, vi, en)
    a('cap.ssot', 'Vòng: hai màn hình và repository nối nhau bằng mũi tên hai chiều. Hạt màu hồng là sự kiện đi lên repository; hạt màu vàng là state đi xuống màn hình. Khối viền đỏ đang giữ dữ liệu lệch.',
      'A loop: the two screens and the repository joined by arrows both ways. Pink dots are events going up to the repository; yellow dots are state coming down to the screens. A red-outlined box holds out-of-date data.')
    S = [
        ('twowriters', 's1', 'Chọn giờ đặt 9:00: ghi vào hai chỗ', 'Choose a time books 9:00: writes to two places',
         'ChooseTimeViewModel thêm lịch vào danh sách riêng của nó, rồi thêm vào repository.bookings, một MutableList công khai. Đã có hai bản.',
         'ChooseTimeViewModel adds the booking to its own list, then to repository.bookings, a public MutableList. There are already two copies.'),
        ('twowriters', 's2', 'Lịch của tôi vẫn hiện bản cũ', 'My appointments still shows an old copy',
         'Màn Lịch của tôi đã mở từ trước (nằm dưới trong back stack) và giữ bản chụp toList() lúc mở. Nó không thấy lịch 9:00. Giờ có ba bản.',
         'My appointments was opened earlier (it sits lower in the back stack) and keeps the toList() snapshot taken then. It does not see the 9:00 booking. There are now three copies.'),
        ('twowriters', 's3', 'Lịch của tôi hủy bằng cách sửa thẳng danh sách', 'My appointments cancels by editing the list directly',
         'cancel() gọi repository.bookings -= b. Không ai được báo về thay đổi này: danh sách riêng của Chọn giờ vẫn có lịch đó. Ba chỗ đều sửa được dữ liệu.',
         'cancel() calls repository.bookings -= b. Nobody is told about the change: Choose a time\'s own list still has the booking. Three places can now change the data.'),
        ('twowriters', 's4', 'Kết quả: ba bản, không bản nào chắc đúng', 'Result: three copies, none known to be right',
         'Chọn giờ coi 9:00 là đã đặt nên khóa ô đó; Lịch của tôi hiện danh sách khác; repository có bản thứ ba. Muốn biết bản nào đúng phải lần ngược mọi chỗ đã sửa.',
         'Choose a time treats 9:00 as booked and greys it out; My appointments shows another list; the repository holds a third. To know which is right you must trace every place that changed it.'),
        ('ssot', 's1', 'Chọn giờ gửi sự kiện: book(9:00)', 'Choose a time sends an event: book(9:00)',
         'ViewModel không tự giữ danh sách. Nó gọi repo.book(slot): sự kiện đi lên tới nguồn sự thật.',
         'The ViewModel keeps no list of its own. It calls repo.book(slot): the event goes up to the source of truth.'),
        ('ssot', 's2', 'Repository là chỗ duy nhất đổi dữ liệu', 'The repository is the only place data changes',
         'book() ghi vào database. Danh sách chỉ lộ ra dưới dạng Flow<List<Booking>>, không có hàm nào khác sửa được nó.',
         'book() writes to the database. The list is exposed only as a Flow<List<Booking>>; no other function can change it.'),
        ('ssot', 's3', 'State đi xuống cả hai màn hình', 'State comes down to both screens',
         'Flow phát danh sách mới; cả Chọn giờ và Lịch của tôi đang thu thập Flow đó nên cùng thấy lịch 9:00, kể cả màn đang nằm dưới back stack khi nó hiện lại.',
         'The Flow emits the new list; both Choose a time and My appointments collect that Flow, so both see the 9:00 booking, including the screen lower in the back stack when it shows again.'),
        ('ssot', 's4', 'Hủy từ màn khác: vẫn một vòng', 'Cancel from the other screen: the same loop',
         'Lịch của tôi gọi repo.cancel(id): sự kiện lên, database đổi, Flow phát lại, hai màn hình cùng cập nhật. Một bản, một chỗ sửa.',
         'My appointments calls repo.cancel(id): the event goes up, the database changes, the Flow emits again, both screens update. One copy, one place that changes it.'),
    ]
    for case, k, tv, te, xv, xe in S:
        sid = case + '.' + k
        m('s.%s.title' % sid, tv, te); m('s.%s.explain' % sid, xv, xe); m('ev.' + sid, tv, te)
    for k, vi, en in [
        ('try', 'Đi hết bốn bước của mỗi cách giữ dữ liệu; để ý ba số đo phía trên sơ đồ.', 'Walk all four steps of each approach; watch the three metrics above the diagram.'),
        ('twowriters.s2', 'Một bản chụp toList() là dữ liệu chết: nó không biết khi nguồn đổi. Chương K7 ("Collection: read-only, mutable và xử lý") của track Kotlin nói về bản chụp.', 'A toList() snapshot is dead data: it never learns when the source changes. Chapter K7 ("Collections: read-only, mutable and processing") of the Kotlin track covers snapshots.'),
        ('twowriters.s3', 'Hướng dẫn kiến trúc của Android nói: SSOT là chủ của dữ liệu và chỉ SSOT được sửa nó; vì vậy SSOT lộ dữ liệu dưới kiểu bất biến. [[src:ax-arch-guide]]', 'The Android architecture guide says: the SSOT owns the data and only the SSOT may modify it; that is why it exposes the data as an immutable type. [[src:ax-arch-guide]]'),
        ('twowriters.s4', 'Hướng dẫn nêu các lợi ích của SSOT: gom mọi thay đổi về một chỗ, bảo vệ dữ liệu khỏi bị sửa lung tung, và dễ lần ra lỗi. [[src:ax-arch-guide]]', 'The guide lists the benefits of an SSOT: all changes in one place, data protected from tampering, and bugs easier to trace. [[src:ax-arch-guide]]'),
        ('ssot.s2', 'Tài liệu Android nói: mỗi repository định nghĩa một nguồn sự thật; dữ liệu lộ ra phải bất biến để không lớp nào làm nó rơi vào trạng thái sai. [[src:ax-data-layer]]', 'The Android docs say: each repository defines a single source of truth; exposed data must be immutable so no class can put it in an inconsistent state. [[src:ax-data-layer]]'),
        ('ssot.s3', 'UDF: state đi một chiều từ nơi giữ state xuống UI; sự kiện đi chiều ngược lại tới SSOT. [[src:ax-arch-guide]] [[src:ax-ui-layer]]', 'UDF: state flows one way, from its holder down to the UI; events flow the other way, up to the SSOT. [[src:ax-arch-guide]] [[src:ax-ui-layer]]'),
        ('ssot.s4', 'Trong app offline-first, nguồn sự thật thường là database; chương G4 đi sâu vào phần này. [[src:ax-arch-guide]]', 'In an offline-first app, the source of truth is usually a database; chapter G4 goes deeper. [[src:ax-arch-guide]]')]:
        m('co.' + k, vi, en)

    # ---------------- chương ----------------
    C = 'g2'
    a(C + '.title', 'Các tầng, hướng phụ thuộc, SSOT và UDF', 'Layers, dependency direction, SSOT and UDF')
    a(C + '.essence', 'App chia thành tầng UI (giao diện) và tầng data (dữ liệu), có thể thêm tầng domain (quy tắc nghiệp vụ) ở giữa. Mũi tên giữa chúng là phụ thuộc, đọc là "A biết về B", và chỉ đi một chiều: tầng trên biết tầng dưới. Dữ liệu vẫn đi ngược lên qua giá trị trả về và Flow.\nQuy tắc hướng phụ thuộc chỉ được công cụ kiểm khi tách module Gradle; trong một module, import sai chiều vẫn biên dịch qua.\nMỗi loại dữ liệu có một nguồn sự thật duy nhất: chỉ nó sửa dữ liệu, và nó lộ dữ liệu ra dưới kiểu không sửa được. Sự kiện đi lên nguồn đó, state đi xuống giao diện.',
      'An app is split into a UI layer and a data layer, optionally with a domain layer (business rules) in between. The arrows between them are dependencies, read as "A knows about B", and point one way: upper layers know lower ones. Data still flows back up through return values and Flows.\nThe dependency rule is checked by tools only when the code is split into Gradle modules; within one module, a wrong-way import still compiles.\nEach type of data has a single source of truth: only it changes the data, and it exposes the data as a type that cannot be changed. Events go up to that source, state comes down to the UI.')
    a(C + '.goal.g1', 'Đã thấy bước build của import sai chiều', 'Saw the build step of the wrong-way import')
    a(C + '.goal.g2', 'Đã đi hết bốn bước', 'Walked all four steps')
    a(C + '.sim.arch.layers', 'hướng phụ thuộc giữa các tầng', 'the direction of dependencies between layers')
    a(C + '.sim.arch.ssot', 'một nguồn sự thật và luồng một chiều', 'single source of truth and one-way flow')

    S_ = 'hook'
    a(C + '.sec.%s.title' % S_, 'Đoán trước khi đọc', 'Predict before reading')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'predict', 'Cả app nằm trong một module. Ai đó thêm vào SlotRepository dòng import một lớp của màn hình (SlotChipUi). Build có báo lỗi không?',
      'The whole app is one module. Someone adds to SlotRepository an import of a screen class (SlotChipUi). Does the build fail?')
    B(C, S_, 1, 'ans', 'Không. Trong một module, lớp public nào cũng import được, và vòng phụ thuộc giữa các lớp là hợp lệ. Chỉ khi tách module Gradle mà :core:data không khai báo phụ thuộc vào module màn hình thì import đó mới thành lỗi biên dịch. Mô phỏng thứ nhất bên dưới đi qua cả bốn tình huống. [[src:kt-visibility]]',
      'No. Within one module any public class can be imported, and a loop between classes is legal. Only when the code is split into Gradle modules, and :core:data does not declare a dependency on the screen\'s module, does that import become a compile error. The first simulation below walks through all four cases. [[src:kt-visibility]]')
    B(C, S_, 2, 'predict', 'Màn Chọn giờ và màn Lịch của tôi mỗi màn giữ một bản danh sách lịch hẹn. Người dùng hủy một lịch ở Lịch của tôi rồi quay lại Chọn giờ. Ô giờ đó trống lại chưa?',
      'Choose a time and My appointments each keep their own copy of the appointment list. The user cancels one in My appointments, then goes back to Choose a time. Is that slot free again?')
    B(C, S_, 2, 'ans', 'Không, nếu không ai báo cho bản của Chọn giờ. Hai bản sửa độc lập sẽ lệch nhau. Mô phỏng thứ hai so cách này với một nguồn sự thật duy nhất. [[src:ax-arch-guide]]',
      'No, unless someone tells Choose a time\'s copy. Two copies changed independently drift apart. The second simulation compares this with a single source of truth. [[src:ax-arch-guide]]')

    S_ = 'layers'
    a(C + '.sec.%s.title' % S_, 'Tầng UI, data và domain tùy chọn', 'The UI and data layers, and the optional domain')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'p', 'Hướng dẫn chính thức yêu cầu mỗi app có ít nhất hai tầng. Tầng UI hiển thị dữ liệu lên màn hình. Tầng data chứa business logic (quy tắc nghiệp vụ, như "không đặt hai lịch cùng giờ") và lộ dữ liệu của app ra. Giữa hai tầng có thể thêm tầng domain để đơn giản hóa và dùng lại các tương tác giữa UI và data. Lớp trong tầng domain thường gọi là use case.\nHình dung: tầng UI là quầy lễ tân, tầng data là kho hồ sơ, tầng domain là cuốn quy định mà lễ tân tra khi cần. [[src:ax-arch-guide]] [[src:ax-domain-layer]]',
      'The official guide asks every app to have at least two layers. The UI layer displays data on screen. The data layer contains the business logic (business rules, such as "no two bookings at the same time") and exposes the app\'s data. A domain layer can be added between them to simplify and reuse interactions between UI and data; its classes are usually called use cases.\nPicture it: the UI layer is the front desk, the data layer is the records room, and the domain layer is the rulebook the desk looks things up in. [[src:ax-arch-guide]] [[src:ax-domain-layer]]')
    B(C, S_, 2, 'p', 'Mũi tên trong các sơ đồ của hướng dẫn là phụ thuộc giữa các lớp: "domain phụ thuộc lớp của data" nghĩa là use case import và gọi repository. Đây không phải chiều dữ liệu chạy. Dữ liệu đi xuống qua tham số và đi lên qua giá trị trả về hay Flow, nên tầng dưới không cần biết tầng trên. [[src:ax-arch-guide]]',
      'The arrows in the guide\'s diagrams are dependencies between classes: "the domain depends on data layer classes" means the use case imports and calls the repository. They are not the direction data travels. Data goes down as parameters and comes up as return values or Flows, so lower layers need not know upper ones. [[src:ax-arch-guide]]')
    B(C, S_, 3, 'p', 'Tài liệu Android về tầng data thêm hai luật cho chiều phụ thuộc: repository là lối vào duy nhất của tầng data, và ViewModel không bao giờ nhận thẳng một data source. Nhờ vậy có thể đổi cách lưu (mạng, database, cache) mà tầng trên không biết. [[src:ax-data-layer]]',
      'The Android docs on the data layer add two rules about direction: repositories are the only entry point to the data layer, and a ViewModel never takes a data source directly. That lets you change how data is stored (network, database, cache) without the upper layers knowing. [[src:ax-data-layer]]')

    S_ = 'direction'
    a(C + '.sec.%s.title' % S_, 'Ai giữ hướng phụ thuộc, và hai cách vẽ mũi tên', 'Who enforces the direction, and two ways to draw the arrows')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'p', 'Trình biên dịch Kotlin không biết lớp nào thuộc tầng nào. Trong một module, mọi khai báo public và internal đều thấy được ở mọi file, nên repository import một lớp UI vẫn biên dịch. Module ở đây là tập file biên dịch cùng nhau, ví dụ một Gradle source set.\nQuy tắc dễ nhớ: trong một module, hướng phụ thuộc chỉ là lời hứa giữa người với người. [[src:kt-visibility]]',
      'The Kotlin compiler does not know which class belongs to which layer. Within one module, every public and internal declaration is visible from every file, so a repository importing a UI class still compiles. A module here is a set of files compiled together, such as a Gradle source set.\nRule of thumb: inside one module, dependency direction is only a promise between people. [[src:kt-visibility]]')
    B(C, S_, 2, 'p', 'Tách thành module Gradle thì công cụ giữ hộ quy tắc. Module chỉ thấy các module nó khai báo phụ thuộc, nên import sai chiều thành lỗi biên dịch. Khai báo internal giấu thêm chi tiết khỏi module khác. Gradle cũng không build được hai module phụ thuộc nhau thành vòng: muốn hai bên trao đổi thì phải qua một module trung gian. [[src:ax-modularization]] [[src:ax-modularization-patterns]]',
      'Splitting into Gradle modules lets tools hold the rule for you. A module sees only the modules it declares as dependencies, so a wrong-way import becomes a compile error. internal hides further details from other modules. Gradle also cannot build modules that depend on each other in a cycle: for two of them to talk, they need a mediating module. [[src:ax-modularization]] [[src:ax-modularization-patterns]]')
    B(C, S_, 3, 'p', 'Có trường phái vẽ mũi tên khác Google. Eran Boudjnah theo Dependency Rule (quy tắc phụ thuộc) của Robert C. Martin, theo đó mọi mũi tên hướng vào domain, tầng chứa quy tắc nghiệp vụ. Để use case gọi được repository mà không phụ thuộc nó, domain khai báo interface repository, còn tầng data cài đặt interface đó (đảo phụ thuộc). Domain khi đó không phụ thuộc module nào. [[src:book-boudjnah]]',
      'One school draws the arrows differently from Google. Eran Boudjnah follows Robert C. Martin\'s Dependency Rule: every arrow points toward the domain, the layer holding business rules. For a use case to call a repository without depending on it, the domain declares a repository interface and the data layer implements it (dependency inversion). The domain then depends on no module. [[src:book-boudjnah]]')
    B(C, S_, 4, 'note', 'Track này theo hướng dẫn chính thức (domain phụ thuộc data, domain tùy chọn). Cách đảo phụ thuộc đáng chi phí khi domain lớn hay dùng chung giữa nhiều feature, vì mỗi repository sẽ có thêm một interface và một phần nối trong DI (chương G6). SOLID và nguyên lý đảo phụ thuộc ở mức lớp thuộc track Mã sạch và kỷ luật làm nghề.',
      'This track follows the official guide (the domain depends on data, and the domain is optional). Inverting is worth its cost when the domain is large or shared across features, since every repository gains an interface and some DI wiring (chapter G6). SOLID and dependency inversion at class level belong to the clean code track.')

    S_ = 'ssot'
    a(C + '.sec.%s.title' % S_, 'Một nguồn sự thật và luồng một chiều', 'Single source of truth and one-way flow')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'p', 'Mỗi loại dữ liệu mới nên có một nguồn sự thật duy nhất (SSOT): chủ của dữ liệu đó, và chỉ nó được sửa. SSOT lộ dữ liệu dưới kiểu bất biến; muốn đổi thì gọi hàm hay gửi sự kiện cho nó. Lợi ích: mọi thay đổi về một chỗ, dữ liệu không bị sửa lung tung, lỗi dễ lần ra. Trong app offline-first (app chạy được cả khi mất mạng), SSOT thường là database; có khi là ViewModel. [[src:ax-arch-guide]]',
      'Each new type of data should have a single source of truth (SSOT): the owner of that data, and the only one allowed to change it. The SSOT exposes the data as an immutable type; to change it you call its functions or send it events. Benefits: all changes in one place, data protected from tampering, bugs easier to trace. In an offline-first app (one that keeps working without a network) the SSOT is usually a database; sometimes it is a ViewModel. [[src:ax-arch-guide]]')
    B(C, S_, 2, 'p', 'SSOT thường đi cùng luồng dữ liệu một chiều (UDF): state đi một chiều từ phạm vi rộng xuống phạm vi hẹp, ví dụ từ nguồn dữ liệu tới UI; sự kiện như cú bấm đi chiều ngược lại tới SSOT, nơi dữ liệu được sửa rồi lộ ra lại. Ở tầng UI, vòng này là: UI báo sự kiện cho ViewModel, ViewModel xử lý và cập nhật state, state mới quay về UI.\nQuy tắc dễ nhớ: muốn đổi dữ liệu thì báo cho chủ của nó, đừng tự sửa bản của mình. [[src:ax-arch-guide]] [[src:ax-ui-layer]]',
      'An SSOT usually comes with unidirectional data flow (UDF): state flows one way, from wider scopes to narrower ones, for example from data sources to the UI; events such as taps flow the other way to the SSOT, where the data is changed and exposed again. In the UI layer the loop is: the UI notifies the ViewModel of events, the ViewModel handles them and updates state, and the new state flows back to the UI.\nRule of thumb: to change data, tell its owner; never edit your own copy. [[src:ax-arch-guide]] [[src:ax-ui-layer]]')
    B(C, S_, 3, 'kt', 'class BookingRepository(private val dao: BookingDao) {\n    val bookings: Flow<List<Booking>> = dao.observeAll()   // chỉ đọc\n    suspend fun book(slot: Slot) = dao.insert(Booking(slot)) // sửa chỉ qua đây\n}\n// SAI: val bookings = mutableListOf<Booking>()  // ai cũng sửa được, không ai được báo',
      'class BookingRepository(private val dao: BookingDao) {\n    val bookings: Flow<List<Booking>> = dao.observeAll()   // read-only\n    suspend fun book(slot: Slot) = dao.insert(Booking(slot)) // changes only here\n}\n// WRONG: val bookings = mutableListOf<Booking>()  // anyone can change it, nobody is told')

    S_ = 'bugs'
    a(C + '.sec.%s.title' % S_, 'Hai lỗi hay gặp', 'Two common bugs')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'bug', 'Test của SlotRepository bỗng đòi Robolectric (thư viện giả lập Android để chạy test trên máy tính); ba màn hình không liên quan phải build lại mỗi khi đổi giao diện ô giờ.', 'SlotRepository\'s tests suddenly need Robolectric (a library that simulates Android so tests can run on a computer); three unrelated screens rebuild whenever the time-chip design changes.')
    B(C, S_, 1, 'cause', 'Repository import SlotChipUi và nhận Context để lấy chuỗi: một phụ thuộc sai chiều, và vì cả app chung một module nên không công cụ nào bắt.', 'The repository imports SlotChipUi and takes a Context for strings: a wrong-way dependency, and with the whole app in one module no tool catches it.')
    B(C, S_, 1, 'fix', 'Repository trả mô hình dữ liệu (Slot); ViewModel đổi sang mô hình UI. Nếu muốn công cụ giữ quy tắc, tách tầng data thành module riêng không phụ thuộc module feature.', 'The repository returns a data model (Slot); the ViewModel maps it to the UI model. To have tools enforce the rule, move the data layer into its own module that does not depend on the feature module.')
    B(C, S_, 2, 'bug', 'Hủy lịch ở màn Lịch của tôi, quay lại Chọn giờ thì ô giờ đó vẫn bị khóa như đã đặt.', 'After cancelling in My appointments, the slot is still greyed out as booked when going back to Choose a time.')
    B(C, S_, 2, 'cause', 'Hai ViewModel mỗi cái giữ một bản danh sách và sửa bản của mình (hay sửa thẳng một MutableList công khai), nên không bản nào được báo khi bản kia đổi.', 'Each ViewModel keeps its own copy of the list and changes it (or edits a public MutableList directly), so neither copy hears when the other changes.')
    B(C, S_, 2, 'fix', 'Cho repository làm nguồn sự thật: lộ ra Flow chỉ đọc, chỉ đổi qua book() và cancel(); hai màn hình cùng thu thập Flow đó.', 'Make the repository the source of truth: expose a read-only Flow, change it only through book() and cancel(); both screens collect that Flow.')

    S_ = 'ex'
    a(C + '.sec.%s.title' % S_, 'Bài tập', 'Exercise')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'ex', 'App có bốn module: :app, :feature:booking, :core:domain, :core:data. Cho sáu import: (a) BookingViewModel import BookUseCase; (b) BookUseCase import BookingRepository; (c) BookingRepository import BookingScreenState; (d) RoomBookingDao import BookingViewModel; (e) :app import mọi module để nối DI; (f) BookUseCase import android.content.Context. Theo hướng dẫn chính thức, import nào sai chiều? Cái nào trình biên dịch sẽ bắt nếu mỗi module chỉ khai báo phụ thuộc đúng chiều? [[src:book-boudjnah]] [[src:ax-modularization]]',
      'An app has four modules: :app, :feature:booking, :core:domain, :core:data. Six imports: (a) BookingViewModel imports BookUseCase; (b) BookUseCase imports BookingRepository; (c) BookingRepository imports BookingScreenState; (d) RoomBookingDao imports BookingViewModel; (e) :app imports every module to wire DI; (f) BookUseCase imports android.content.Context. Following the official guide, which imports point the wrong way? Which would the compiler catch if each module declares only right-way dependencies? [[src:book-boudjnah]] [[src:ax-modularization]]')
    B(C, S_, 1, 'hint', 'Với mỗi import, hỏi: lớp được import nằm ở tầng trên hay tầng dưới, và module của lớp gọi có khai báo phụ thuộc vào module đó không.', 'For each import ask: is the imported class in an upper or lower layer, and does the caller\'s module declare a dependency on that module?')
    B(C, S_, 1, 'sol', '(a), (b), (e) đúng chiều: UI → domain → data, và :app là chỗ duy nhất được biết mọi module. (c) và (d) sai chiều (data biết UI) và trình biên dịch bắt được vì :core:data không phụ thuộc :feature:booking. (f) không sai chiều giữa các tầng của app, nhưng làm domain dính vào Android; trình biên dịch chỉ bắt nếu :core:domain là module Kotlin thuần không có Android trên classpath.',
      '(a), (b) and (e) point the right way: UI → domain → data, and :app is the one place allowed to know every module. (c) and (d) point the wrong way (data knowing UI), and the compiler catches them because :core:data does not depend on :feature:booking. (f) is not a wrong way between the app\'s layers, but it ties the domain to Android; the compiler catches it only if :core:domain is a plain Kotlin module without Android on its classpath.')

    S_ = 'recall'
    a(C + '.sec.%s.title' % S_, 'Tự trả lời', 'Answer it yourself')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'ask', 'Mũi tên "use case → repository" nói gì, và dữ liệu của repository về tới use case bằng cách nào?', 'What does the arrow "use case → repository" say, and how does the repository\'s data reach the use case?')
    B(C, S_, 1, 'ans', 'Use case biết về (import và gọi) repository. Dữ liệu đi ngược lên qua giá trị trả về hay Flow, không cần repository biết use case.', 'The use case knows about (imports and calls) the repository. Data comes back up as return values or a Flow, with no need for the repository to know the use case.')
    B(C, S_, 2, 'ask', 'Vì sao lộ ra Flow chỉ đọc thay vì một MutableList?', 'Why expose a read-only Flow instead of a MutableList?')
    B(C, S_, 2, 'ans', 'Để chỉ nguồn sự thật đổi được dữ liệu, và mọi nơi quan sát đều được báo khi nó đổi.', 'So that only the source of truth can change the data, and everyone observing is told when it changes.')

    for q, qv, qe, av, ae, wv, we in [
        ('q1', 'Trong sơ đồ của hướng dẫn kiến trúc, mũi tên nghĩa là gì?', 'In the architecture guide\'s diagrams, what does an arrow mean?', 'Một phụ thuộc giữa các lớp: lớp này biết về lớp kia.', 'A dependency between classes: one knows about the other.', 'Không phải chiều dữ liệu chạy; dữ liệu đi cả hai chiều.', 'Not the direction data travels; data flows both ways.'),
        ('q2', 'Cả app một module, repository import một lớp UI. Build ra sao?', 'Whole app in one module, the repository imports a UI class. What happens to the build?', 'Vẫn qua; không công cụ mặc định nào bắt.', 'It passes; no default tool catches it.', 'Chỉ module Gradle tách riêng mới biến nó thành lỗi biên dịch.', 'Only separate Gradle modules turn it into a compile error.'),
        ('q3', 'Ai được sửa dữ liệu khi có một nguồn sự thật?', 'With a single source of truth, who may change the data?', 'Chỉ nguồn sự thật đó, qua hàm hay sự kiện của nó.', 'Only that source of truth, through its functions or events.', 'Nó lộ dữ liệu dưới kiểu bất biến.', 'It exposes the data as an immutable type.'),
        ('q4', 'Trong cách đảo phụ thuộc của Robert C. Martin, interface repository nằm ở tầng nào?', 'In Robert C. Martin\'s inversion, which layer holds the repository interface?', 'Tầng domain, cạnh use case.', 'The domain layer, next to the use cases.', 'Tầng data cài đặt nó, nên mũi tên đi từ data vào domain.', 'The data layer implements it, so the arrow points from data into the domain.')]:
        a(C + '.quiz.%s.q' % q, qv, qe); a(C + '.quiz.%s.a' % q, av, ae); a(C + '.quiz.%s.why' % q, wv, we)
