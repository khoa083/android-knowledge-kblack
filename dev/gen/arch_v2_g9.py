# Kiến trúc · G9: module hóa (Phần 2)
# Nguồn: developer.android.com Guide to Android app modularization, Common modularization patterns (đọc 2026-11-24);
# Kotlin Visibility modifiers. Nối G2 (hướng phụ thuộc), G6 (@Binds), track Mã sạch (nguyên lý thành phần).
# Trần: 8 mục, mục cơ chế ≤ 4 khối.

SEC_ORDER = {'g9': ['hook', 'types', 'talk', 'expose', 'bugs', 'ex', 'recall']}


def add(a):
    def B(ch, sec, n, field, vi, en=None):
        a('%s.sec.%s.b.%02d.%s' % (ch, sec, n, field), vi, vi if en is None else en)

    m = lambda k, vi, en=None: a('m.modules.' + k, vi, en)
    m('title', 'Đồ thị module của app Hẹn Khám', 'The ClinicBook module graph')
    m('overview', 'App được chia thành :app, :feature:booking, :feature:history và :core:data. Ba tình huống: (1) hai feature muốn mở màn của nhau nên phụ thuộc lẫn nhau; (2) feature dùng thẳng một lớp nội bộ của :core:data; (3) tách :core:data thành module interface và module cài đặt.',
      'The app is split into :app, :feature:booking, :feature:history and :core:data. Three cases: (1) two features want to open each other\'s screens and come to depend on each other; (2) a feature uses an internal class of :core:data directly; (3) :core:data is split into an interface module and an implementation module.')
    m('wrapup', 'Module hóa biến quy tắc kiến trúc thành ranh giới mà công cụ kiểm: module chỉ thấy những gì nó khai báo phụ thuộc, khai báo internal không ra khỏi module, và Gradle không build được vòng phụ thuộc. Feature không phụ thuộc nhau; app module giữ điều hướng và làm trung gian, truyền id chứ không truyền object. Module cao phụ thuộc module trừu tượng, không phụ thuộc chi tiết cài đặt.',
      'Modularization turns architecture rules into boundaries that tools check: a module sees only what it declares as dependencies, internal declarations stay inside the module, and Gradle cannot build a dependency cycle. Features do not depend on each other; the app module owns navigation and mediates, passing ids rather than objects. High-level modules depend on abstraction modules, not on implementation details.')
    m('simp.1', 'Bốn tới năm module đại diện; app thật có thêm module core cho UI, model, test.', 'Four or five representative modules; a real app has more core modules for UI, models and tests.')
    m('simp.2', 'Kết quả build mô tả cách Gradle và Kotlin xử lý phụ thuộc giữa module và từ khóa internal; site không chạy Gradle, và câu chữ lỗi thật có thể khác. Nguyên tắc theo tài liệu chính thức của Android và Kotlin (đọc ngày 2026-11-24). Chương chưa nói về convention plugin (bộ cấu hình build dùng chung), version catalog (danh mục phiên bản thư viện), module riêng cho từng loại thiết bị, và cách đo thời gian build.',
      'The build results describe how Gradle and Kotlin treat module dependencies and the internal keyword; the site does not run Gradle, and real error messages may differ. The principles follow the official Android and Kotlin docs (read on 2026-11-24). The chapter does not cover convention plugins (shared build configuration), version catalogs (a central list of library versions), per-device app modules, or measuring build times.')
    m('ctl.hint', 'Đổi tình huống rồi đi lại bốn bước; xem tab "Đồ thị module" và dòng Build.', 'Switch the case and walk the four steps again; watch the "Module graph" tab and the Build line.')
    m('ctl.case', 'Tình huống', 'Case')
    for k, vi, en in [('features', 'feature gọi feature', 'feature calling feature'), ('visibility', 'lớp nội bộ lộ ra ngoài', 'an internal class leaking out'), ('abstraction', 'module interface và module cài đặt', 'interface and implementation modules')]:
        m('ctl.case.' + k, vi, en)
    m('diagramTitle', 'App module, feature module, data module', 'App module, feature modules, data module')
    m('diagramDesc', 'Ba loại module theo hướng phụ thuộc: app → feature → data', 'Three kinds of module along the dependency direction: app → feature → data')
    for k, vi, en in [('app', 'App module', 'App module'), ('feat', 'Các feature module', 'Feature module'), ('data', 'Data module', 'Data module')]:
        m('n.' + k, vi, en)
    m('met.ff', 'Cạnh feature → feature', 'Feature → feature edges'); m('met.cycle', 'Có vòng phụ thuộc', 'Dependency cycle'); m('met.impl', 'Feature dính chi tiết cài đặt', 'Feature tied to implementation details')
    for k, vi, en in [('yes', 'có', 'yes'), ('no', 'không', 'no')]:
        m('yn.' + k, vi, en)
    a('cap.modules', 'Từ trái sang phải: app module, feature module, data module. Đây là sơ đồ rút gọn; tab "Đồ thị module" vẽ từng module và mọi cạnh, kể cả cạnh sai.',
      'Left to right: app module, feature modules, data module. This is a condensed view; the "Module graph" tab draws every module and every edge, including the wrong ones.')
    S = [
        ('features', 's1', 'Đồ thị ban đầu: app → feature → data', 'The starting graph: app → feature → data',
         ':app phụ thuộc hai feature; :feature:booking và :feature:history cùng phụ thuộc :core:data. Không feature nào biết feature kia.',
         ':app depends on both features; :feature:booking and :feature:history both depend on :core:data. Neither feature knows the other.'),
        ('features', 's2', 'Đặt lịch muốn mở Lịch sử: thêm phụ thuộc feature → feature', 'Booking wants to open History: add a feature → feature dependency',
         ':feature:booking thêm implementation(project(":feature:history")) để gọi thẳng màn Lịch sử. Build vẫn qua, nhưng hai feature đã dính vào nhau.',
         ':feature:booking adds implementation(project(":feature:history")) to call the History screen directly. The build still passes, but the two features are now coupled.'),
        ('features', 's3', 'Lịch sử muốn "đặt lại": vòng phụ thuộc', 'History wants "book again": a dependency cycle',
         ':feature:history thêm phụ thuộc ngược lại vào :feature:booking. Hai project phụ thuộc vòng; Gradle không build được.',
         ':feature:history adds the reverse dependency on :feature:booking. The two projects depend on each other in a cycle; Gradle cannot build it.'),
        ('features', 's4', 'Sửa: app module làm trung gian, truyền id', 'Fix: the app module mediates, passing ids',
         'Bỏ cả hai cạnh. :app giữ navigation graph; Đặt lịch chỉ gọi lambda kiểu onOpenHistory(patientId), :app điều hướng tới "history/$patientId". Lịch sử tự tải dữ liệu từ :core:data theo id.',
         'Remove both edges. :app owns the navigation graph; Booking only calls a lambda like onOpenHistory(patientId), and :app navigates to "history/$patientId". History loads its own data from :core:data by id.'),
        ('visibility', 's1', ':core:data lộ SlotRepository', ':core:data exposes SlotRepository',
         'SlotRepository là giao diện công khai của :core:data; bên trong nó dùng SlotDao của Room. :feature:booking gọi repository.',
         'SlotRepository is :core:data\'s public interface; inside, it uses Room\'s SlotDao. :feature:booking calls the repository.'),
        ('visibility', 's2', 'Feature dùng thẳng SlotDao', 'The feature uses SlotDao directly',
         'SlotDao mặc định là public, nên :feature:booking gọi thẳng nó để "nhanh hơn", bỏ qua repository và nguồn sự thật. Build vẫn qua.',
         'SlotDao is public by default, so :feature:booking calls it directly "to be quicker", bypassing the repository and the source of truth. The build still passes.'),
        ('visibility', 's3', 'Đánh dấu internal: lỗi biên dịch', 'Mark it internal: a compile error',
         'Đổi thành internal interface SlotDao. Khai báo internal chỉ thấy được trong module của nó, nên lời gọi từ :feature:booking thành lỗi biên dịch.',
         'Change it to internal interface SlotDao. Internal declarations are visible only inside their module, so the call from :feature:booking becomes a compile error.'),
        ('visibility', 's4', 'Chỉ repository còn công khai', 'Only the repository stays public',
         'Feature quay lại gọi SlotRepository. Mọi chi tiết cài đặt của :core:data là internal; giao diện công khai của module nhỏ nhất có thể.',
         'The feature goes back to calling SlotRepository. Every implementation detail of :core:data is internal; the module\'s public interface is as small as possible.'),
        ('abstraction', 's1', 'Feature phụ thuộc cả module cài đặt', 'The feature depends on the whole implementation module',
         ':core:data chứa cả interface lẫn cài đặt (Room, Retrofit). :feature:booking phụ thuộc nó, nên phụ thuộc gián tiếp vào mọi chi tiết cài đặt.',
         ':core:data holds both interfaces and implementation (Room, Retrofit). :feature:booking depends on it, so indirectly on every implementation detail.'),
        ('abstraction', 's2', 'Tách data-api và data-impl', 'Split data-api and data-impl',
         ':core:data-api chứa interface SlotRepository và mô hình; :core:data-impl chứa cài đặt bằng Room và Retrofit, và phụ thuộc data-api. Feature vẫn trỏ vào impl.',
         ':core:data-api holds the SlotRepository interface and models; :core:data-impl holds the Room and Retrofit implementation and depends on data-api. The feature still points at impl.'),
        ('abstraction', 's3', 'Feature chỉ phụ thuộc data-api; app nối cài đặt', 'The feature depends only on data-api; the app wires the implementation',
         ':feature:booking chỉ thấy interface. :app phụ thuộc data-impl và nối interface với cài đặt bằng @Binds của Hilt (chương G6).',
         ':feature:booking sees only the interface. :app depends on data-impl and binds the interface to the implementation with Hilt\'s @Binds (chapter G6).'),
        ('abstraction', 's4', 'Đổi cài đặt: feature không bị kéo theo', 'Change the implementation: the feature is not dragged along',
         'Sửa truy vấn Room trong data-impl. :feature:booking không phụ thuộc module đó, nên không cần biên dịch lại; feature cũng có thể test với một cài đặt giả của data-api.',
         'Edit a Room query in data-impl. :feature:booking does not depend on that module, so it need not be recompiled; the feature can also be tested against a fake implementation of data-api.'),
    ]
    for case, k, tv, te, xv, xe in S:
        sid = case + '.' + k
        m('s.%s.title' % sid, tv, te); m('s.%s.explain' % sid, xv, xe); m('ev.' + sid, tv, te)
    for k, vi, en in [
        ('try', 'Đi bốn bước của từng tình huống; xem cạnh đỏ trong "Đồ thị module" và dòng Build.', 'Walk the four steps of each case; watch the red edges in the "Module graph" and the Build line.'),
        ('features.s2', 'Tài liệu Android nói: feature module (module của một tính năng) phụ thuộc data module; app module là điểm vào và phụ thuộc feature. Không có cạnh feature → feature trong mô hình đó. [[src:ax-modularization-patterns]]', 'The Android docs say: feature modules (modules for one feature) depend on data modules; the app module is the entry point and depends on features. That model has no feature → feature edge. [[src:ax-modularization-patterns]]'),
        ('features.s3', 'Giao tiếp hai chiều trực tiếp giữa hai module là không thể vì phụ thuộc vòng; cần một module trung gian. [[src:ax-modularization-patterns]]', 'Direct two-way communication between two modules is impossible because of cyclic dependencies; a mediating module is needed. [[src:ax-modularization-patterns]]'),
        ('features.s4', 'Trung gian thường là module giữ navigation graph (app module). Đừng truyền object qua điều hướng; truyền id đơn giản để feature tự tải từ tầng data, giữ nguồn sự thật duy nhất. [[src:ax-modularization-patterns]]', 'The mediator is usually the module that owns the navigation graph (the app module). Do not pass objects as navigation arguments; pass simple ids so features load from the data layer, keeping a single source of truth. [[src:ax-modularization-patterns]]'),
        ('visibility.s2', 'Lớp trong Kotlin mặc định là public; không đánh dấu gì thì module khác dùng được.', 'Kotlin classes are public by default; unless marked otherwise, other modules can use them.'),
        ('visibility.s3', 'Tài liệu Kotlin nói: internal nghĩa là thấy được trong cùng module, tức tập file biên dịch cùng nhau. [[src:kt-visibility]]', 'The Kotlin docs say: internal means visible within the same module, the set of files compiled together. [[src:kt-visibility]]'),
        ('visibility.s4', 'Tài liệu Android nói: giao diện công khai của module nên nhỏ nhất có thể, không lộ chi tiết cài đặt; dùng private hay internal. [[src:ax-modularization-patterns]]', 'The Android docs say: a module\'s public interface should be minimal and leak no implementation details; use private or internal. [[src:ax-modularization-patterns]]'),
        ('abstraction.s2', 'Mẫu module trừu tượng: thay vì module cao phụ thuộc thẳng module thấp, cả module cao lẫn module cài đặt cùng phụ thuộc module trừu tượng. [[src:ax-modularization-patterns]]', 'The abstraction-module pattern: instead of high-level modules depending directly on low-level ones, both high-level and implementation modules depend on the abstraction module. [[src:ax-modularization-patterns]]'),
        ('abstraction.s3', 'Đây là đảo phụ thuộc của chương G2, đặt ở mức module: interface ở phía dùng, cài đặt trỏ vào nó.', 'This is chapter G2\'s dependency inversion at module level: the interface sits with the user, the implementation points at it.'),
        ('abstraction.s4', 'Tài liệu cũng khuyên dùng implementation thay vì api khi khai báo phụ thuộc, vì api lộ phụ thuộc bắc cầu cho module dùng nó; implementation giảm số module phải build lại. [[src:ax-modularization-patterns]]', 'The docs also advise implementation over api when declaring dependencies, because api exposes transitive dependencies to consumers; implementation reduces how many modules must be rebuilt. [[src:ax-modularization-patterns]]')]:
        m('co.' + k, vi, en)
    a('preset.modules', 'Kiến trúc · đồ thị module: feature gọi feature, internal, module trừu tượng', 'Architecture · module graph: feature calling feature, internal, abstraction modules')

    z = lambda k, vi, en=None: a('vz.' + k, vi, en)
    z('tab.md', 'Đồ thị module', 'Module graph')
    z('md.cap', 'Mỗi hộp là một module Gradle (hay một lớp, trong tình huống internal); mỗi mũi tên là một khai báo phụ thuộc. Mũi tên đỏ là phụ thuộc sai; mũi tên đỏ có chữ là chỗ công cụ chặn.', 'Each box is a Gradle module (or a class, in the internal case); each arrow is a declared dependency. A red arrow is a wrong dependency; a red arrow with a label is where the tools refuse.')
    z('md.build', 'Build')
    for k, vi, en in [('pass', 'qua', 'passes'), ('cycle', 'Gradle từ chối: :feature:booking và :feature:history phụ thuộc vòng', 'Gradle refuses: :feature:booking and :feature:history depend on each other'),
                      ('internal', 'lỗi biên dịch ở :feature:booking: SlotDao là internal của :core:data', 'compile error in :feature:booking: SlotDao is internal to :core:data'),
                      ('implOnly', 'qua; chỉ :core:data-impl và :app phải build lại', 'passes; only :core:data-impl and :app need rebuilding')]:
        z('md.b.' + k, vi, en)
    z('md.err.cycle', 'vòng phụ thuộc', 'dependency cycle'); z('md.err.internal', 'internal: bị chặn', 'internal: blocked')
    z('md.lg.dep', 'phụ thuộc (khai báo trong build.gradle.kts)', 'dependency (declared in build.gradle.kts)'); z('md.lg.bad', 'phụ thuộc sai hay bị chặn', 'wrong or refused dependency')
    z('md.g.dataBox', 'module :core:data', 'the :core:data module')
    for k, vi, en in [('app', ':app', ':app'), ('appNav', ':app (giữ navigation graph)', ':app (owns the navigation graph)'), ('book', ':feature:booking', ':feature:booking'), ('hist', ':feature:history', ':feature:history'),
                      ('data', ':core:data', ':core:data'), ('dataAll', ':core:data (interface + Room + Retrofit)', ':core:data (interfaces + Room + Retrofit)'),
                      ('dataApi', ':core:data-api (interface)', ':core:data-api (interfaces)'), ('dataImpl', ':core:data-impl (Room, Retrofit)', ':core:data-impl (Room and Retrofit)'),
                      ('dataImplChanged', ':core:data-impl (vừa sửa)', ':core:data-impl (just edited)'),
                      ('repoPublic', 'SlotRepository (công khai)', 'SlotRepository (public)'), ('daoPublic', 'SlotDao (mặc định public)', 'SlotDao (public by default)'), ('daoInternal', 'SlotDao (internal)', 'SlotDao (marked internal)')]:
        z('md.n.' + k, vi, en)

    C = 'g9'
    a(C + '.title', 'Module hóa', 'Modularization')
    a(C + '.essence', 'Module hóa chia mã thành các module Gradle. Module chỉ thấy những module nó khai báo phụ thuộc, nên ranh giới kiến trúc trở thành thứ công cụ kiểm chứ không chỉ là quy ước.\nBa loại chính: app module (điểm vào, giữ điều hướng), feature module (một phần chức năng, phụ thuộc data), data/core module. Feature không phụ thuộc nhau; app làm trung gian và truyền id.\nLộ ít nhất có thể: chi tiết cài đặt là internal, ưu tiên implementation hơn api, và để module cao phụ thuộc module trừu tượng thay vì module cài đặt.',
      'Modularization splits code into Gradle modules. A module sees only the modules it declares as dependencies, so architectural boundaries become something tools check, not just a convention.\nThree main kinds: the app module (entry point, owns navigation), feature modules (a part of the functionality, depending on data), and data/core modules. Features do not depend on each other; the app mediates and passes ids.\nExpose as little as possible: implementation details are internal, prefer implementation over api, and let high-level modules depend on abstraction modules rather than implementation modules.')
    a(C + '.goal.g1', 'Đã thấy Gradle từ chối vòng phụ thuộc', 'Saw Gradle refuse the dependency cycle')
    a(C + '.goal.g2', 'Đã đi hết bốn bước', 'Walked all four steps')
    a(C + '.sim.arch.modules', 'đồ thị module của app Hẹn Khám', 'the ClinicBook module graph')

    S_ = 'hook'
    a(C + '.sec.%s.title' % S_, 'Đoán trước khi đọc', 'Predict before reading')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'predict', ':feature:booking đã phụ thuộc :feature:history để mở màn Lịch sử. Giờ màn Lịch sử cần nút "Đặt lại", nên ai đó thêm phụ thuộc :feature:history → :feature:booking. Chuyện gì xảy ra khi build?',
      ':feature:booking already depends on :feature:history to open the History screen. Now History needs a "Book again" button, so someone adds a dependency :feature:history → :feature:booking. What happens on build?')
    B(C, S_, 1, 'ans', 'Gradle không build được: hai project phụ thuộc vòng. Cách sửa không phải tìm mẹo cho vòng đó, mà để app module làm trung gian điều hướng. Mô phỏng bên dưới đi qua tình huống này và hai tình huống khác. [[src:ax-modularization-patterns]]',
      'Gradle cannot build it: the two projects depend on each other in a cycle. The fix is not a trick around the cycle but letting the app module mediate navigation. The simulation below walks through this and two other cases. [[src:ax-modularization-patterns]]')

    S_ = 'types'
    a(C + '.sec.%s.title' % S_, 'Vì sao chia module, và các loại module', 'Why split into modules, and the kinds of module')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'p', 'Tài liệu nêu các lợi ích: dùng lại mã, kiểm soát chặt phần lộ ra (đánh dấu internal hay private mọi thứ trừ giao diện công khai), đóng gói, build nhanh hơn, mỗi module có người chịu trách nhiệm. Đổi lại là thêm cấu hình và phải nghĩ về ranh giới; app nhỏ có thể chưa cần. [[src:ax-modularization]]',
      'The docs list the benefits: reuse, strict visibility control (marking everything but the public interface internal or private), encapsulation, faster builds, and clear ownership per module. The cost is more configuration and thinking about boundaries; a small app may not need it yet. [[src:ax-modularization]]')
    B(C, S_, 2, 'p', 'Data module gói dữ liệu và logic nghiệp vụ của một miền, lộ repository. Feature module gói một phần chức năng, thường là một hay vài màn hình kèm ViewModel, và phụ thuộc data module. App module là điểm vào: phụ thuộc feature module và thường giữ điều hướng gốc. Ngoài ra có common/core module cho mã dùng chung và test module. [[src:ax-modularization-patterns]]',
      'Data modules wrap the data and business logic of a domain and expose repositories. Feature modules wrap a part of the functionality, usually one or a few screens with their ViewModels, and depend on data modules. The app module is the entry point: it depends on feature modules and usually provides root navigation. There are also common/core modules for shared code, and test modules. [[src:ax-modularization-patterns]]')

    S_ = 'talk'
    a(C + '.sec.%s.title' % S_, 'Hai feature trao đổi với nhau', 'Two features talking to each other')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'p', 'Module hiếm khi tách biệt hoàn toàn, nhưng nên giữ liên kết lỏng. Giao tiếp hai chiều trực tiếp giữa hai module là không thể khi thành vòng phụ thuộc, nên cần một module thứ ba làm trung gian, thường là module giữ navigation graph (app module). Feature nguồn chỉ báo "muốn mở màn X với id Y"; app điều hướng. [[src:ax-modularization-patterns]]',
      'Modules rarely live in total isolation, but coupling should stay low. Direct two-way communication between two modules is impossible when it forms a dependency cycle, so a third module mediates, usually the one owning the navigation graph (the app module). The source feature only says "open screen X with id Y"; the app navigates. [[src:ax-modularization-patterns]]')
    B(C, S_, 2, 'kt', '// :feature:booking không biết :feature:history\n@Composable fun BookingScreen(onOpenHistory: (patientId: String) -> Unit) { … }\n\n// :app giữ navigation graph và nối hai feature\ncomposable("booking") { BookingScreen(onOpenHistory = { id -> navController.navigate("history/$id") }) }\ncomposable("history/{patientId}") { HistoryScreen() }   // ViewModel đọc patientId từ SavedStateHandle',
      '// :feature:booking does not know :feature:history\n@Composable fun BookingScreen(onOpenHistory: (patientId: String) -> Unit) { … }\n\n// :app owns the navigation graph and connects the features\ncomposable("booking") { BookingScreen(onOpenHistory = { id -> navController.navigate("history/$id") }) }\ncomposable("history/{patientId}") { HistoryScreen() }   // the ViewModel reads patientId from SavedStateHandle')
    B(C, S_, 3, 'note', 'Truyền id đơn giản qua điều hướng, không truyền object: feature đích tự tải từ tầng data theo id, nên không vi phạm nguồn sự thật duy nhất (G2) và hai feature không phải dùng chung kiểu dữ liệu. [[src:ax-modularization-patterns]]', 'Pass simple ids through navigation, not objects: the destination feature loads from the data layer by id, so the single source of truth (G2) holds and the features need not share data types. [[src:ax-modularization-patterns]]')

    S_ = 'expose'
    a(C + '.sec.%s.title' % S_, 'Lộ ít nhất có thể', 'Expose as little as possible')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'p', 'Giao diện công khai của module nên nhỏ nhất có thể và không lộ chi tiết cài đặt. Dùng private hay internal cho mọi thứ khác: internal chỉ thấy được trong module của nó. Khi khai báo phụ thuộc, ưu tiên implementation hơn api: api lộ các phụ thuộc bắc cầu cho module dùng nó, còn implementation giảm số module phải build lại. [[src:ax-modularization-patterns]] [[src:kt-visibility]]',
      'A module\'s public interface should be as small as possible and leak no implementation details. Use private or internal for everything else: internal is visible only within its module. When declaring dependencies, prefer implementation over api: api exposes transitive dependencies to consumers, while implementation reduces how many modules must be rebuilt. [[src:ax-modularization-patterns]] [[src:kt-visibility]]')
    B(C, S_, 2, 'p', 'Mẫu module trừu tượng đẩy ý này xa hơn: module cao (feature) và module cài đặt (data-impl với Room, Retrofit) cùng phụ thuộc một module trừu tượng (data-api với interface). Feature không biết công nghệ lưu trữ, test được với cài đặt giả, và app module nối interface với cài đặt qua DI. Đây là đảo phụ thuộc của G2 ở mức module; nguyên lý thành phần (độ ổn định, cohesion) thuộc track Mã sạch. [[src:ax-modularization-patterns]]',
      'The abstraction-module pattern takes this further: the high-level module (feature) and the implementation module (data-impl with Room, Retrofit) both depend on an abstraction module (data-api with interfaces). The feature does not know the storage technology, can be tested with a fake implementation, and the app module binds interface to implementation through DI. This is G2\'s dependency inversion at module level; component principles (stability, cohesion) belong to the clean code track. [[src:ax-modularization-patterns]]')

    S_ = 'bugs'
    a(C + '.sec.%s.title' % S_, 'Hai lỗi hay gặp', 'Two common bugs')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'bug', 'Thêm nút "Đặt lại" ở màn Lịch sử thì build hỏng với lỗi vòng phụ thuộc giữa hai feature.', 'Adding "Book again" to History breaks the build with a cycle between two features.')
    B(C, S_, 1, 'cause', 'Hai feature phụ thuộc thẳng vào nhau để mở màn của nhau.', 'The two features depend on each other directly to open each other\'s screens.')
    B(C, S_, 1, 'fix', 'Bỏ cạnh feature → feature; feature lộ lambda điều hướng, app module giữ navigation graph và truyền id.', 'Remove the feature → feature edges; features expose navigation lambdas, the app module owns the navigation graph and passes ids.')
    B(C, S_, 2, 'bug', 'Màn Đặt lịch hiện giờ trống cũ dù repository đã làm mới.', 'Booking shows stale free slots even though the repository refreshed.')
    B(C, S_, 2, 'cause', 'Feature gọi thẳng SlotDao (public mặc định), bỏ qua repository và logic làm mới của nó.', 'The feature calls SlotDao directly (public by default), bypassing the repository and its refresh logic.')
    B(C, S_, 2, 'fix', 'Đánh dấu SlotDao và mọi chi tiết cài đặt là internal trong :core:data; chỉ repository công khai.', 'Mark SlotDao and every implementation detail internal in :core:data; only the repository is public.')

    S_ = 'ex'
    a(C + '.sec.%s.title' % S_, 'Bài tập', 'Exercise')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'ex', 'Vẽ đồ thị module cho Hẹn Khám có thêm tính năng Thanh toán: :app, :feature:booking, :feature:payment, :core:data-api, :core:data-impl, :core:ui (thành phần giao diện dùng chung). Màn Đặt lịch xong thì chuyển sang Thanh toán với mã lịch hẹn. Liệt kê mọi cạnh phụ thuộc, và chỉ ra cạnh nào nếu có sẽ là sai. (Bài tập của site, theo các mẫu trong Common modularization patterns.) [[src:ax-modularization-patterns]]',
      'Draw the module graph for ClinicBook with a new Payment feature: :app, :feature:booking, :feature:payment, :core:data-api, :core:data-impl, :core:ui (shared UI components). After booking, the app moves to Payment with the appointment id. List every dependency edge, and say which edges would be wrong if they existed. (The site\'s own exercise, after the patterns in Common modularization patterns.) [[src:ax-modularization-patterns]]')
    B(C, S_, 1, 'hint', 'Ai giữ điều hướng? Ai cần interface, ai cần cài đặt? Có module nào chỉ nên được app biết?', 'Who owns navigation? Who needs interfaces, who needs implementations? Is there a module only the app should know?')
    B(C, S_, 1, 'sol', 'Đúng: :app → booking, payment, data-impl; booking → data-api, ui; payment → data-api, ui; data-impl → data-api. :app điều hướng "payment/$appointmentId". Sai nếu có: booking → payment (feature → feature), booking hay payment → data-impl (dính cài đặt), data-api → bất kỳ feature nào (sai chiều, dễ thành vòng).',
      'Right: :app → booking, payment, data-impl; booking → data-api, ui; payment → data-api, ui; data-impl → data-api. :app navigates to "payment/$appointmentId". Wrong if present: booking → payment (feature → feature), booking or payment → data-impl (tied to implementation), data-api → any feature (wrong direction, easily a cycle).')

    S_ = 'recall'
    a(C + '.sec.%s.title' % S_, 'Tự trả lời', 'Answer it yourself')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'ask', 'Hai feature cần mở màn của nhau thì làm thế nào mà không thành vòng?', 'How do two features open each other\'s screens without a cycle?')
    B(C, S_, 1, 'ans', 'Để app module giữ navigation graph làm trung gian; feature chỉ truyền id.', 'Let the app module, which owns the navigation graph, mediate; features pass only ids.')
    B(C, S_, 2, 'ask', 'internal trong Kotlin giới hạn khả năng thấy ở mức nào?', 'What does internal limit visibility to in Kotlin?')
    B(C, S_, 2, 'ans', 'Trong cùng module, tức tập file biên dịch cùng nhau.', 'The same module: the set of files compiled together.')

    for q, qv, qe, av, ae, wv, we in [
        ('q1', 'Feature module nên phụ thuộc loại module nào?', 'What kind of module should a feature module depend on?', 'Data (hay core) module.', 'Data (or core) modules.', 'Không phụ thuộc feature khác.', 'Not on other features.'),
        ('q2', 'Module nào thường làm trung gian điều hướng giữa các feature?', 'Which module usually mediates navigation between features?', 'App module, nơi giữ navigation graph.', 'The app module, which owns the navigation graph.', 'Theo Common modularization patterns.', 'Per Common modularization patterns.'),
        ('q3', 'Nên truyền gì qua điều hướng giữa hai feature?', 'What should be passed through navigation between features?', 'Một id đơn giản, không phải object.', 'A simple id, not an object.', 'Feature đích tự tải từ tầng data.', 'The destination loads from the data layer.'),
        ('q4', 'Vì sao ưu tiên implementation hơn api?', 'Why prefer implementation over api?', 'api lộ phụ thuộc bắc cầu; implementation giảm số module phải build lại.', 'api exposes transitive dependencies; implementation reduces rebuilds.', 'Lộ ít nhất có thể.', 'Expose as little as possible.')]:
        a(C + '.quiz.%s.q' % q, qv, qe); a(C + '.quiz.%s.a' % q, av, ae); a(C + '.quiz.%s.why' % q, wv, we)
