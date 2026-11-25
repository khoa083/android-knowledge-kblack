# Gỡ lỗi và hiệu năng · l5: R8 và stack trace bị làm rối (Phần 1: tìm ra lỗi)
# Nguồn (chỉ ghi ở đây và docs/research/debugging.md), đọc 2026-11-25, các trang không ghi ngày: developer.android.com/build/shrink-code
# (R8: thu gọn mã từ các điểm vào, tối ưu như inline và gộp lớp, làm rối tên, thu gọn tài nguyên; isMinifyEnabled, isShrinkResources;
# proguard-android-optimize.txt; DSL mới optimization { enable = true } từ AGP 9.3), studio/command-line/retrace (cú pháp retrace, đọc stdin, --verbose),
# topic/performance/app-optimization/troubleshoot-the-optimization (crash chỉ ở release thường do reflection; ClassNotFoundException, NoSuchMethodException…;
# configuration.txt; -whyareyoukeeping; mapping.txt bị ghi đè mỗi lần build, giữ bản cho mỗi phiên bản; mapping được gói vào AAB; Logcat mới tự dịch ngược),
# support.google.com/googleplay/android-developer/answer/9848633 (Play lấy mapping từ AAB với AGP 4.1+; thiếu mapping thì crash vẫn bị làm rối).
# Tên rối a.b.c, dòng mapping và lớp PaymentMethod tạo qua Class.forName là ví dụ của site.

SEC_ORDER = {'l5': ['hook', 'what', 'mapping', 'retrace', 'reflection', 'bugs', 'ex', 'recall']}


def add(a):
    def B(ch, sec, n, field, vi, en=None):
        a('%s.sec.%s.b.%02d.%s' % (ch, sec, n, field), vi, vi if en is None else en)

    a('preset.retrace', '''Gỡ lỗi · dịch ngược stack trace của bản release''', '''Debugging · translating a release stack trace back''')
    m = lambda k, vi, en=None: a('m.retrace.' + k, vi, en)
    m('title', '''Crash chỉ có trong bản release, và stack trace toàn chữ a.b.c''', '''A crash only in the release build, and a stack trace full of a.b.c''')
    m('overview', '''Bản release của app Hẹn Khám bật R8, công cụ thu gọn và làm rối mã lúc build. Play Console báo một crash có stack trace như "at a.b.c(Unknown Source:4)". Cách 1 tra theo file mapping của bản build mới nhất trên máy. Cách 2 dùng đúng file mapping của phiên bản bị crash rồi chạy retrace. Ở cả hai, ta đếm số frame dịch đúng, và tìm ra crash thật: một lớp được tạo bằng tên qua reflection bị R8 đổi tên.''',
      '''ClinicBook\'s release build turns on R8, the tool that shrinks and obfuscates code at build time. Play Console reports a crash whose stack trace reads like "at a.b.c(Unknown Source:4)". Way 1 looks names up in the mapping file of the latest build on your machine. Way 2 uses the mapping file of exactly the crashing version, then runs retrace. In both we count how many frames translate correctly, and we find the real crash: a class created by name through reflection was renamed by R8.''')
    m('wrapup', '''File mapping là bảng đối chiếu tên rối với tên thật, và mỗi lần build lại có thể khác. Tra bằng mapping của bản khác thì tên dịch ra trông hợp lý mà sai. Dùng đúng mapping của phiên bản bị crash, retrace trả lại tên lớp, tên hàm và số dòng thật. Crash ở đây chỉ có trong release vì mã tạo lớp bằng tên qua Class.forName, mà R8 đã đổi tên lớp đó; một keep rule giữ nguyên tên nó.''',
      '''The mapping file is the table matching obfuscated names to real ones, and every build can produce a different one. Looking names up in another build\'s mapping gives translations that look plausible and are wrong. With the mapping of exactly the crashing version, retrace restores real class names, function names and line numbers. The crash here exists only in release because the code creates a class by name with Class.forName, and R8 renamed that class; a keep rule keeps its name.''')
    m('simp.1', '''File mapping thật có hàng nghìn dòng và còn ghi khoảng số dòng, hàm bị inline; ở đây chỉ giữ vài dòng cần cho ví dụ.''',
      '''A real mapping file has thousands of lines and also records line ranges and inlined functions; here only the few lines the example needs are kept.''')
    m('simp.2', '''Mỗi frame được dịch thật bằng JavaScript: tra tên lớp và tên hàm rối trong bảng mapping đang dùng; frame dịch đúng khi kết quả khớp tên thật của phiên bản bị crash.''',
      '''Each frame is really translated in JavaScript: the obfuscated class and function names are looked up in the mapping table in use; a frame is correct when the result matches the real name in the crashing version.''')
    m('ctl.hint', '''Chọn file mapping rồi đi qua bốn bước; xem cột "dịch ra" có khớp cột "thật" không.''', '''Pick a mapping file and walk the four steps; check whether the "translated" column matches the "real" column.''')
    m('ctl.case', '''File mapping dùng để dịch''', '''Mapping file used''')
    m('ctl.case.latest', '''của bản build mới nhất trên máy''', '''from the latest build on your machine'''); m('ctl.case.exact', '''của đúng phiên bản 1.6.0 bị crash''', '''from exactly the crashing version 1.6.0''')
    m('diagramTitle', '''Từ mã nguồn tới stack trace đọc được''', '''From source code to a readable stack trace''')
    m('diagramDesc', '''R8 đổi tên lúc build và ghi mapping; crash mang tên rối; retrace dùng mapping để dịch ngược''', '''R8 renames at build time and writes the mapping; the crash carries obfuscated names; retrace uses the mapping to translate back''')
    for k, vi, en in [('src', 'Mã nguồn', 'Source code'), ('r8', 'R8 lúc build release', 'R8 at release build time'), ('map', 'File mapping.txt', 'The mapping.txt file'),
                      ('crash', 'Stack trace từ Play Console', 'Stack trace from Play Console'), ('retrace', 'retrace', 'retrace')]:
        m('n.' + k, vi, en)
    m('met.ok', '''Frame dịch đúng (trên 4)''', '''Frames translated correctly (of 4)'''); m('met.wrong', '''Frame dịch sai mà trông hợp lý''', '''Frames translated wrongly but plausibly''')
    m('met.cause', '''Nguyên nhân''', '''Cause''')
    m('cause.none', '''chưa biết''', '''unknown'''); m('cause.wrong', '''đoán sai: lỗi trong BookingRepo''', '''wrong guess: a bug in BookingRepo''')
    m('cause.reflect', '''Class.forName tìm lớp đã bị đổi tên''', '''Class.forName looks for a renamed class'''); m('cause.kept', '''đã sửa bằng keep rule''', '''fixed with a keep rule''')
    a('cap.retrace', '''R8 đổi tên lúc build và ghi file mapping; stack trace từ người dùng mang tên rối; retrace cần đúng file mapping của phiên bản đó để dịch ngược. Ô đỏ: dịch bằng mapping sai.''',
      '''R8 renames at build time and writes a mapping file; stack traces from users carry obfuscated names; retrace needs that version\'s exact mapping to translate back. A red box: translating with the wrong mapping.''')
    S = [
        ('latest', 's1', 'Stack trace từ Play Console: toàn tên rối', 'The Play Console stack trace: all obfuscated names',
         'Bốn frame có dạng a.b.c(Unknown Source:4). Không đọc được lớp nào, hàm nào. Bản 1.6.0 đã phát hành tuần trước; trên máy bạn là bản build mới nhất của nhánh main.',
         'Four frames look like a.b.c(Unknown Source:4). No class or function can be read. Version 1.6.0 shipped last week; your machine has the latest build of the main branch.'),
        ('latest', 's2', 'Tra bằng mapping của bản build mới nhất', 'Looking up with the latest build\'s mapping',
         'File build/outputs/mapping/release/mapping.txt trên máy là của lần build gần nhất. Hai frame dịch ra tên trông hoàn toàn hợp lý: BookingRepo.save và BookingDao.insert.',
         'The build/outputs/mapping/release/mapping.txt on your machine belongs to the most recent build. Two frames translate to names that look perfectly reasonable: BookingRepo.save and BookingDao.insert.'),
        ('latest', 's3', 'Tên dịch ra là sai', 'The translated names are wrong',
         'Từ bản 1.6.0 tới nay đã có lớp mới được thêm, nên R8 gán lại tên khác: a.b trong bản 1.6.0 là PaymentFactory, nhưng trong bản mới là BookingRepo. Tên dịch sai mà trông hợp lý còn nguy hiểm hơn không dịch được.',
         'Classes have been added since 1.6.0, so R8 assigned names differently: a.b in 1.6.0 is PaymentFactory, but in the new build it is BookingRepo. A wrong translation that looks plausible is more dangerous than no translation.'),
        ('latest', 's4', 'Đi tìm lỗi trong BookingRepo cả buổi', 'An afternoon hunting a bug in BookingRepo',
         'Bạn đọc kỹ BookingRepo.save, không thấy gì sai, vì crash không nằm ở đó. File mapping bị ghi đè mỗi lần build; không giữ bản của 1.6.0 thì không dịch đúng được trên máy.',
         'You read BookingRepo.save closely and find nothing wrong, because the crash is not there. The mapping file is overwritten on every build; without a copy from 1.6.0, it cannot be translated correctly on your machine.'),
        ('exact', 's1', 'Cùng stack trace, lấy mapping của đúng bản 1.6.0', 'The same stack trace, with the mapping of exactly 1.6.0',
         'Bản 1.6.0 được phát hành dưới dạng App Bundle, nên file mapping của nó đã được gói vào bundle và lưu trên Play Console; nhóm cũng giữ một bản theo tag phát hành.',
         'Version 1.6.0 shipped as an App Bundle, so its mapping file was packed into the bundle and kept on Play Console; the team also keeps a copy per release tag.'),
        ('exact', 's2', 'Chạy retrace: cả 4 frame dịch đúng', 'Running retrace: all 4 frames translate correctly',
         'retrace mapping-1.6.0.txt trace.txt trả lại tên thật và số dòng: PaymentFactory.create, PaymentViewModel.pay, PayFragment.onPayClicked. Không frame nào là BookingRepo.',
         'retrace mapping-1.6.0.txt trace.txt gives back real names and line numbers: PaymentFactory.create, PaymentViewModel.pay, PayFragment.onPayClicked. No frame is BookingRepo.'),
        ('exact', 's3', 'Nguyên nhân: Class.forName tìm một tên không còn tồn tại', 'The cause: Class.forName looks for a name that no longer exists',
         'Dòng đầu là ClassNotFoundException: vn.henkham.pay.MomoPayment. PaymentFactory tạo cách thanh toán bằng tên lớp đọc từ cấu hình: Class.forName("vn.henkham.pay." + name). R8 đã đổi tên MomoPayment thành a.d, nên tên đó không còn trong app. Bản debug không bật R8, nên không bao giờ crash.',
         'The first line is ClassNotFoundException: vn.henkham.pay.MomoPayment. PaymentFactory creates payment methods from a class name read from config: Class.forName("vn.henkham.pay." + name). R8 renamed MomoPayment to a.d, so that name no longer exists in the app. The debug build does not run R8, so it never crashes.'),
        ('exact', 's4', 'Sửa: keep rule giữ tên các lớp thanh toán', 'Fix: a keep rule keeps the payment classes\' names',
         'Thêm -keep class vn.henkham.pay.** implements vn.henkham.pay.PaymentMethod { <init>(); } để R8 giữ tên và constructor của các lớp đó. Tốt hơn nữa là bỏ reflection: một map từ tên sang hàm tạo, R8 hiểu được và không cần keep rule.',
         'Add -keep class vn.henkham.pay.** implements vn.henkham.pay.PaymentMethod { <init>(); } so R8 keeps those classes\' names and constructors. Better still, drop reflection: a map from names to constructor functions, which R8 understands, needs no keep rule.'),
    ]
    for case, k, tv, te, xv, xe in S:
        sid = case + '.' + k
        m('s.%s.title' % sid, tv, te); m('s.%s.explain' % sid, xv, xe); m('ev.' + sid, tv, te)
    for k, vi, en in [
        ('try', '''Mẹo đọc: cột trái là frame rối như Play Console báo, cột giữa là tên dịch ra bằng file mapping đang chọn, cột phải là tên thật trong bản 1.6.0. Ô đỏ: dịch sai.''',
         '''Reading tip: the left column is the obfuscated frame as Play Console reports it, the middle is the name translated with the chosen mapping file, the right is the real name in version 1.6.0. A red cell: a wrong translation.'''),
        ('latest.s2', '''R8 làm rối tên bằng cách rút ngắn tên lớp, trường và hàm, ví dụ com.example.MyActivity có thể thành a.b.a. [[src:ad-shrink]]''',
         '''R8 obfuscates by shortening class, field and method names; for example, com.example.MyActivity could become a.b.a. [[src:ad-shrink]]'''),
        ('latest.s3', '''File mapping bị ghi đè mỗi lần bạn build project; hãy lưu một bản cho mỗi bản phát hành. [[src:ad-r8-troubleshoot]]''',
         '''The mapping file is overwritten every time you build the project; save a copy for each release. [[src:ad-r8-troubleshoot]]'''),
        ('latest.s4', '''Bài học của chương "Quy trình gỡ lỗi, adb và bug report" lặp lại: một giả thuyết dựa trên dữ liệu sai thì kiểm cách nào cũng không khớp.''',
         '''The lesson of "The debugging process, adb and bug reports" again: a hypothesis built on wrong data never matches however you test it.'''),
        ('exact.s1', '''Với App Bundle build bằng Android Gradle Plugin 4.1 trở lên, Play lấy file mapping từ chính bundle, nên crash trên Play Console được dịch ngược sẵn. Với APK thì phải tự tải lên cho từng phiên bản. [[src:play-deobfuscate]]''',
         '''For App Bundles built with Android Gradle Plugin 4.1 or later, Play takes the mapping file from the bundle itself, so crashes in Play Console are already translated back. For APKs you must upload it yourself for each version. [[src:play-deobfuscate]]'''),
        ('exact.s2', '''retrace nhận đường dẫn tới file mapping và tới file stack trace (không có thì đọc từ đầu vào chuẩn), rồi in stack trace đã dịch. [[src:ad-retrace]]''',
         '''retrace takes the path to the mapping file and to the stack trace file (or reads from standard input), then prints the translated stack trace. [[src:ad-retrace]]'''),
        ('exact.s3', '''Crash chỉ có ở bản release thường do reflection bị hỏng; các ngoại lệ cần để ý: ClassNotFoundException, NoSuchMethodException, NoSuchFieldException và các lỗi cùng họ. [[src:ad-r8-troubleshoot]]''',
         '''Release-only crashes are typically due to broken reflection; exceptions to look for: ClassNotFoundException, NoSuchMethodException, NoSuchFieldException and their relatives. [[src:ad-r8-troubleshoot]]'''),
        ('exact.s4', '''Cách sửa là thêm keep rule; nếu chính mã của bạn dùng reflection, có thể dùng chú thích Keep của Jetpack thay cho quy tắc viết tay. [[src:ad-r8-troubleshoot]]''',
         '''The fix is a keep rule; if your own code uses reflection, Jetpack Keep annotations can be used instead of hand-written rules. [[src:ad-r8-troubleshoot]]'''),
    ]:
        m('co.' + k, vi, en)

    z = lambda k, vi, en=None: a('vz.' + k, vi, en)
    z('tab.retrace', '''Bảng đối chiếu frame''', '''Frame comparison table''')
    z('rt.col.obf', '''Frame rối''', '''Obfuscated frame'''); z('rt.col.got', '''Dịch ra''', '''Translated'''); z('rt.col.real', '''Thật (bản 1.6.0)''', '''Real (version 1.6.0)''')
    z('rt.col.line', '''Dòng mapping đã dùng''', '''Mapping line used''')
    z('rt.map', '''File mapping: {f}''', '''Mapping file: {f}'''); z('rt.map.latest', '''mapping.txt của bản build mới nhất''', '''mapping.txt of the latest build''')
    z('rt.map.exact', '''mapping.txt của bản 1.6.0''', '''mapping.txt of version 1.6.0''')
    z('rt.q', '''?''', '''?'''); z('rt.count', '''{ok} trên 4 frame dịch đúng; {w} frame sai mà trông hợp lý.''', '''{ok} of 4 frames correct; {w} wrong but plausible.''')
    z('rt.head', '''Dòng đầu: {h}''', '''First line: {h}''')
    z('rt.legend', '''Ô đỏ: tên dịch ra khác tên thật. Ô "?": chưa dịch. Cột cuối là dòng của file mapping đã dùng để dịch frame đó. Tên lớp của app được bỏ tiền tố vn.henkham. cho gọn.''',
      '''A red cell: the translated name differs from the real one. A "?" cell: not translated yet. The last column is the line of the mapping file used for that frame. App class names drop the vn.henkham. prefix for brevity.''')

    C = 'l5'
    a(C + '.title', '''R8 và stack trace bị làm rối''', '''R8 and obfuscated stack traces''')
    a(C + '.essence', '''Bản release thường bật R8: nó bỏ mã không dùng tới, tối ưu, và đổi tên lớp, hàm thành tên ngắn như a.b.c. App nhỏ hơn, nhưng stack trace từ người dùng không đọc được nữa.\nLúc build, R8 ghi file mapping.txt: bảng đối chiếu tên rối với tên thật. Mỗi lần build có thể cho một mapping khác, và file trên máy bị ghi đè; phải dùng đúng mapping của phiên bản bị crash rồi chạy retrace, hoặc để Play Console dịch giúp từ App Bundle.\nCrash chỉ có ở bản release thường do reflection: mã tìm lớp, hàm hay trường bằng tên dạng chuỗi, mà R8 đã đổi tên hay bỏ đi. Keep rule báo R8 giữ nguyên những thứ đó.''',
      '''Release builds usually turn on R8: it removes unused code, optimises, and renames classes and functions to short names like a.b.c. The app is smaller, but stack traces from users are no longer readable.\nAt build time, R8 writes a mapping.txt file: the table matching obfuscated names to real ones. Each build can produce a different mapping, and the file on your machine is overwritten; use the exact mapping of the crashing version and run retrace, or let Play Console translate from the App Bundle.\nRelease-only crashes usually come from reflection: code looking up a class, function or field by a string name that R8 renamed or removed. A keep rule tells R8 to leave those alone.''')
    a(C + '.goal.g1', '''Đã thấy mapping sai cho tên dịch sai''', '''Saw a wrong mapping give wrong names''')
    a(C + '.goal.g2', '''Đã thấy nguyên nhân của crash chỉ có ở release''', '''Saw the cause of the release-only crash''')
    a(C + '.sim.debugging.retrace', '''dịch stack trace bằng mapping nào''', '''which mapping translates the stack trace''')

    S_ = 'hook'
    a(C + '.sec.%s.title' % S_, '''Đoán trước khi đọc''', '''Predict before reading''')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'predict', '''Play Console báo crash của bản 1.6.0 với frame "at a.b.c(Unknown Source:4)". Bạn tra a.b trong file mapping.txt trên máy, của bản build sáng nay, và thấy BookingRepo. Có tin được không?''',
      '''Play Console reports a crash in version 1.6.0 with the frame "at a.b.c(Unknown Source:4)". You look up a.b in the mapping.txt on your machine, from this morning\'s build, and find BookingRepo. Can you trust it?''')
    B(C, S_, 1, 'ans', '''Không. Mapping thuộc về từng lần build; sau 1.6.0 đã có lớp mới nên R8 gán tên khác, và a.b trong bản 1.6.0 là một lớp khác hẳn. Phải dùng mapping của đúng bản 1.6.0. Mô phỏng ngay dưới so hai cách.''',
      '''No. A mapping belongs to one build; classes were added after 1.6.0, so R8 assigned names differently, and version 1.6.0\'s a.b is a different class altogether. You need the mapping of exactly 1.6.0. The simulation just below compares the two.''')

    S_ = 'what'
    a(C + '.sec.%s.title' % S_, '''R8 làm gì với mã của bạn''', '''What R8 does to your code''')
    a(C + '.sec.%s.badge' % S_, 'version')
    B(C, S_, 1, 'p', '''R8 chạy khi build bản release và làm bốn việc. Thu gọn mã: bắt đầu từ các điểm vào như Activity và Service khai báo trong manifest, bỏ mọi mã không với tới được. Tối ưu: ví dụ inline hàm (chép thân hàm vào chỗ gọi) và gộp lớp. Làm rối tên: đổi tên lớp, trường, hàm thành tên ngắn. Thu gọn tài nguyên: bỏ ảnh, chuỗi không dùng. [[src:ad-shrink]]''',
      '''R8 runs when building the release version and does four things. Code shrinking: starting from entry points such as the Activities and Services declared in the manifest, it removes all unreachable code. Optimisation: for example inlining functions (copying a function body into the call site) and merging classes. Obfuscation: renaming classes, fields and functions to short names. Resource shrinking: removing unused images and strings. [[src:ad-shrink]]''')
    B(C, S_, 2, 'kt', '''android {
    buildTypes {
        release {
            isMinifyEnabled = true          // thu gọn, tối ưu, làm rối mã
            isShrinkResources = true        // thu gọn tài nguyên
            proguardFiles(getDefaultProguardFile("proguard-android-optimize.txt"), "proguard-rules.pro")
        }
    }
}''', '''android {
    buildTypes {
        release {
            isMinifyEnabled = true          // shrink, optimise, obfuscate code
            isShrinkResources = true        // shrink resources
            proguardFiles(getDefaultProguardFile("proguard-android-optimize.txt"), "proguard-rules.pro")
        }
    }
}''')
    B(C, S_, 3, 'note', '''Đây là cú pháp quen thuộc của Android Gradle Plugin; từ bản 9.3 có thêm cú pháp mới optimization { enable = true } và keep rule đặt trong file .keep. Tên cài đặt có thể đổi, còn cơ chế (thu gọn, tối ưu, làm rối, mapping) giữ nguyên. Tài liệu khuyên luôn bật tối ưu cho bản release. [[src:ad-shrink]]''',
      '''This is the familiar Android Gradle Plugin syntax; from version 9.3 there is also a new optimization { enable = true } syntax with keep rules in .keep files. The setting names may change; the mechanism (shrinking, optimising, obfuscating, mapping) stays the same. The documentation recommends always enabling optimisation for release builds. [[src:ad-shrink]]''')

    S_ = 'mapping'
    a(C + '.sec.%s.title' % S_, '''File mapping: bảng đối chiếu tên''', '''The mapping file: a name lookup table''')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'p', '''Mỗi lần build release, R8 ghi file mapping.txt trong build/outputs/mapping/. Mỗi lớp có một dòng "tên thật -> tên rối:", bên dưới là các trường và hàm của nó, kèm khoảng số dòng. Tên rối được gán theo những gì còn lại sau khi thu gọn, nên thêm hay bớt một lớp có thể làm đổi tên của các lớp khác. [[src:ad-r8-troubleshoot]]''',
      '''On every release build, R8 writes mapping.txt in build/outputs/mapping/. Each class has a line "real name -> obfuscated name:", with its fields and functions below, including line ranges. Obfuscated names are assigned from whatever remains after shrinking, so adding or removing one class can change other classes\' names. [[src:ad-r8-troubleshoot]]''')
    B(C, S_, 2, 'kt', '''vn.henkham.pay.PaymentFactory -> a.b:
    1:12:vn.henkham.pay.PaymentMethod create(java.lang.String):18:29 -> c
vn.henkham.pay.MomoPayment -> a.d:
vn.henkham.pay.PaymentViewModel -> a.e:
    1:20:void pay(java.lang.String):40:59 -> f''')
    B(C, S_, 3, 'p', '''File mapping bị ghi đè mỗi lần build, nên với mỗi bản phát hành hãy lưu một bản, gắn với tag phát hành. Nếu phát hành bằng App Bundle với Android Gradle Plugin 4.1 trở lên, file mapping được gói vào bundle và Play Console tự dùng nó để dịch ngược crash. Phiên bản nào thiếu mapping thì crash của phiên bản đó vẫn bị làm rối; tải lên sau thì chỉ crash mới được dịch. [[src:ad-r8-troubleshoot]] [[src:play-deobfuscate]]''',
      '''The mapping file is overwritten on every build, so keep a copy for each release, tied to the release tag. If you ship an App Bundle built with Android Gradle Plugin 4.1 or later, the mapping file is packed into the bundle and Play Console uses it to translate crashes. A version without a mapping keeps its crashes obfuscated; uploading later only translates new crashes. [[src:ad-r8-troubleshoot]] [[src:play-deobfuscate]]''')

    S_ = 'retrace'
    a(C + '.sec.%s.title' % S_, '''Dịch ngược bằng retrace''', '''Translating back with retrace''')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'kt', '''# retrace đường-dẫn-file-mapping [đường-dẫn-file-stack-trace] [tùy chọn]
retrace mapping-1.6.0.txt trace.txt
retrace --verbose mapping-1.6.0.txt trace.txt     # in thêm kiểu tham số và kiểu trả về''', '''# retrace path-to-mapping-file [path-to-stack-trace-file] [options]
retrace mapping-1.6.0.txt trace.txt
retrace --verbose mapping-1.6.0.txt trace.txt     # also prints parameter and return types''')
    B(C, S_, 2, 'p', '''retrace là công cụ dòng lệnh trong bộ command-line tools của Android SDK. Không đưa file stack trace thì nó đọc từ đầu vào chuẩn, nên có thể dán thẳng. Bản Android Studio và Android Gradle Plugin mới (Android Studio Otter 3 Feature Drop, AGP 9.0) còn tự dịch ngược stack trace trong Logcat; bản cũ hơn thì dùng retrace. [[src:ad-retrace]] [[src:ad-r8-troubleshoot]]''',
      '''retrace is a command-line tool in the Android SDK command-line tools. Without a stack trace file it reads from standard input, so you can paste directly. Recent Android Studio and Android Gradle Plugin versions (Android Studio Otter 3 Feature Drop, AGP 9.0) also translate stack traces in Logcat automatically; with older ones, use retrace. [[src:ad-retrace]] [[src:ad-r8-troubleshoot]]''')
    B(C, S_, 3, 'note', '''Stack trace sau khi dịch đọc như mọi stack trace khác: đếm tầng, đi tới Caused by cuối, tìm frame đầu của app (chương "Đọc stack trace"). Frame ghi "Unknown Source" là vì tên file nguồn đã bị bỏ khi làm rối. Nếu bản build còn giữ số dòng, như ở ví dụ này, retrace dùng số đó cùng khoảng dòng trong mapping để tìm lại dòng thật.''',
      '''Once translated, a stack trace reads like any other: count the layers, go to the last Caused by, find the first app frame (the chapter "Reading stack traces"). Frames say "Unknown Source" because the source file name was dropped during obfuscation. If the build still keeps line numbers, as in this example, retrace uses them with the line ranges in the mapping to find the real line.''')
    B(C, S_, 3, 'kind', 'mechanism')

    S_ = 'reflection'
    a(C + '.sec.%s.title' % S_, '''Crash chỉ có ở release: reflection và keep rule''', '''Release-only crashes: reflection and keep rules''')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'p', '''R8 chỉ biết những gì mã gọi trực tiếp. Mã tìm lớp hay hàm bằng chuỗi (Class.forName, ::class.constructors, các thư viện đọc JSON vào lớp bằng tên trường) thì R8 không thấy, nên có thể đổi tên hay bỏ đúng thứ đang được tìm. Bản debug không bật R8 nên chạy tốt; bản release thì ném ClassNotFoundException, NoSuchMethodException, NoSuchFieldException. [[src:ad-r8-troubleshoot]]''',
      '''R8 only knows what code calls directly. Code that finds a class or function by string (Class.forName, ::class.constructors, libraries reading JSON into classes by field name) is invisible to R8, so it may rename or remove exactly what is being looked for. The debug build does not run R8 and works fine; the release build throws ClassNotFoundException, NoSuchMethodException, NoSuchFieldException. [[src:ad-r8-troubleshoot]]''')
    B(C, S_, 2, 'kt', '''# proguard-rules.pro: giữ tên và constructor không tham số của mọi lớp thanh toán
-keep class vn.henkham.pay.** implements vn.henkham.pay.PaymentMethod { <init>(); }

# muốn biết vì sao R8 giữ một lớp (in đường đi từ một điểm vào tới nó):
-whyareyoukeeping class vn.henkham.pay.MomoPayment''', '''# proguard-rules.pro: keep the names and no-argument constructors of every payment class
-keep class vn.henkham.pay.** implements vn.henkham.pay.PaymentMethod { <init>(); }

# to see why R8 keeps a class (prints a path from an entry point to it):
-whyareyoukeeping class vn.henkham.pay.MomoPayment''')
    B(C, S_, 3, 'p', '''Keep rule càng hẹp càng tốt: giữ cả một package lớn làm app phình ra và mất phần lợi của R8. Muốn xem mọi quy tắc đang áp dụng, gồm cả quy tắc thư viện mang theo, đọc file configuration.txt trong build/outputs/mapping. Cách tốt nhất vẫn là tránh reflection ở mã của mình: một map từ tên sang hàm tạo vừa an toàn với R8, vừa được trình biên dịch kiểm. [[src:ad-r8-troubleshoot]]''',
      '''The narrower a keep rule the better: keeping a whole large package bloats the app and throws away R8\'s benefit. To see every rule in effect, including those libraries bring along, read configuration.txt in build/outputs/mapping. The best option is still to avoid reflection in your own code: a map from names to constructor functions is safe with R8 and checked by the compiler. [[src:ad-r8-troubleshoot]]''')

    S_ = 'bugs'
    a(C + '.sec.%s.title' % S_, '''Hai lỗi hay gặp''', '''Two common bugs''')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'bug', '''Crash của bản 1.5.2 trên Play Console vẫn toàn tên rối, các bản khác thì đọc được.''', '''Crashes from version 1.5.2 in Play Console are still obfuscated, while other versions are readable.''')
    B(C, S_, 1, 'cause', '''Bản 1.5.2 được phát hành dạng APK, và không ai tải file mapping của nó lên.''', '''Version 1.5.2 shipped as an APK, and nobody uploaded its mapping file.''')
    B(C, S_, 1, 'fix', '''Tải file mapping đã lưu của 1.5.2 lên; từ nay phát hành bằng App Bundle và lưu mapping theo tag.''', '''Upload the saved 1.5.2 mapping; from now on ship App Bundles and keep the mapping per tag.''')
    B(C, S_, 2, 'bug', '''Sau khi bật R8, màn lịch sử hiện mọi trường rỗng; không crash.''', '''After turning on R8, the history screen shows every field empty; no crash.''')
    B(C, S_, 2, 'cause', '''Thư viện đọc JSON ghép tên trường JSON với tên trường của lớp bằng reflection; R8 đổi tên trường thành a, b, c nên không trường nào khớp.''', '''The JSON library matches JSON field names to the class\'s field names by reflection; R8 renamed the fields to a, b, c, so none match.''')
    B(C, S_, 2, 'fix', '''Dùng thư viện sinh mã lúc biên dịch (không cần reflection), hoặc chú thích tên trường và thêm keep rule cho các lớp dữ liệu đó.''', '''Use a library that generates code at compile time (no reflection), or annotate the field names and add keep rules for those data classes.''')

    S_ = 'ex'
    a(C + '.sec.%s.title' % S_, '''Bài tập''', '''Exercise''')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'ex', '''Dùng đoạn mapping ở mục trên để dịch frame "at a.b.c(Unknown Source:5)" của bản 1.6.0. Rồi cho biết: nếu crash này đến từ bản 1.7.0, bạn có dùng đoạn mapping đó được không?''',
      '''Use the mapping excerpt in the section above to translate the frame "at a.b.c(Unknown Source:5)" from version 1.6.0. Then say: if this crash came from version 1.7.0, could you use that mapping excerpt?''')
    B(C, S_, 1, 'hint', '''Tìm dòng "-> a.b:" để biết lớp, rồi dòng hàm "-> c" bên dưới; số 5 nằm trong khoảng 1:12, ứng với khoảng dòng thật 18:29.''', '''Find the "-> a.b:" line for the class, then the "-> c" function line beneath it; 5 falls in the range 1:12, which maps to real lines 18:29.''')
    B(C, S_, 1, 'sol', '''a.b là PaymentFactory, c là create(String); dòng rối 5 ứng với dòng thật 22 (18 + 5 − 1). Với bản 1.7.0 thì không: mapping thuộc về từng lần build, phải lấy mapping của chính 1.7.0.''',
      '''a.b is PaymentFactory, c is create(String); obfuscated line 5 maps to real line 22 (18 + 5 − 1). For 1.7.0, no: a mapping belongs to one build, so you need 1.7.0\'s own mapping.''')

    S_ = 'recall'
    a(C + '.sec.%s.title' % S_, '''Tự trả lời''', '''Answer it yourself''')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'ask', '''Vì sao phải lưu file mapping cho từng bản phát hành?''', '''Why keep a mapping file for each release?''')
    B(C, S_, 1, 'ans', '''File trên máy bị ghi đè mỗi lần build, và tên rối có thể đổi giữa các bản; chỉ mapping của đúng bản đó mới dịch đúng.''', '''The file on your machine is overwritten on every build, and obfuscated names can change between versions; only that version\'s mapping translates correctly.''')
    B(C, S_, 2, 'ask', '''Vì sao một crash chỉ xuất hiện ở bản release?''', '''Why would a crash appear only in the release build?''')
    B(C, S_, 2, 'ans', '''Thường vì reflection: mã tìm lớp hay hàm bằng tên, mà R8 đã đổi tên hay bỏ đi; bản debug không chạy R8.''', '''Usually reflection: code looks up a class or function by name that R8 renamed or removed; the debug build does not run R8.''')

    for q, qv, qe, av, ae, wv, we in [
        ('q1', 'R8 làm những việc gì?', 'What does R8 do?', 'Thu gọn mã, tối ưu, làm rối tên, và thu gọn tài nguyên.', 'Shrinks code, optimises, obfuscates names, and shrinks resources.',
         'Bắt đầu từ các điểm vào trong manifest, bỏ những gì không với tới được.', 'It starts from the manifest\'s entry points and removes what cannot be reached.'),
        ('q2', 'retrace cần những gì?', 'What does retrace need?', 'File mapping của đúng phiên bản, và stack trace (file hay đầu vào chuẩn).', 'The mapping file of the exact version, and the stack trace (a file or standard input).',
         'Mapping sai cho tên dịch sai mà trông hợp lý.', 'A wrong mapping gives wrong but plausible names.'),
        ('q3', 'Ngoại lệ nào gợi ý crash do R8 và reflection?', 'Which exceptions hint at a crash caused by R8 and reflection?', 'ClassNotFoundException, NoSuchMethodException, NoSuchFieldException và họ hàng của chúng.', 'ClassNotFoundException, NoSuchMethodException, NoSuchFieldException and their relatives.',
         'Thứ được tìm bằng tên đã bị đổi tên hay bị bỏ.', 'What is looked up by name was renamed or removed.'),
        ('q4', 'Phát hành App Bundle với AGP 4.1 trở lên thì có phải tự tải mapping lên Play Console không?', 'Shipping an App Bundle with AGP 4.1 or later, must you upload the mapping to Play Console yourself?', 'Không; Play lấy nó từ bundle.', 'No; Play takes it from the bundle.',
         'APK thì phải tự tải lên cho từng phiên bản.', 'For APKs you must upload it for each version.')]:
        a(C + '.quiz.%s.q' % q, qv, qe); a(C + '.quiz.%s.a' % q, av, ae); a(C + '.quiz.%s.why' % q, wv, we)
