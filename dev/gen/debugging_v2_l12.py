# Gỡ lỗi và hiệu năng · l12: đo hiệu năng cho đúng (Phần 3: lỗi trên máy người dùng)
# Nguồn (chỉ ghi ở đây và docs/research/debugging.md), đọc 2026-11-25, trang không ghi ngày: developer.android.com/topic/performance/benchmarking/
# macrobenchmark-overview (đo khởi động, cuộn, animation; module com.android.test riêng; bản gần release, không debuggable, nên bật thu gọn; profileable;
# MacrobenchmarkRule.measureRepeated với packageName, metrics, iterations; startupMode COLD, WARM, HOT; compilationMode; không khuyên chạy trên emulator;
# báo lỗi khi app debuggable hay pin yếu; kết quả JSON và trace mỗi lần lặp), benchmarking/macrobenchmark-metrics (StartupTimingMetric: timeToInitialDisplayMs,
# timeToFullDisplayMs, min/median/max, "luôn tập trung vào trung vị"; FrameTimingMetric: P50, P90, P95, P99), vitals/launch-time (TTID, TTFD với
# reportFullyDrawn; cold, warm, hot; tối ưu theo giả định cold start; dòng Displayed trong Logcat). Mười số đo mỗi bên là của site.

SEC_ORDER = {'l12': ['hook', 'why', 'macro', 'startup', 'compare', 'bugs', 'ex', 'recall']}


def add(a):
    def B(ch, sec, n, field, vi, en=None):
        a('%s.sec.%s.b.%02d.%s' % (ch, sec, n, field), vi, vi if en is None else en)

    a('preset.measure', '''Gỡ lỗi · một lần đo hay lặp và so trung vị''', '''Debugging · one measurement, or repeat and compare medians''')
    m = lambda k, vi, en=None: a('m.measure.' + k, vi, en)
    m('title', '''"Khởi động nhanh hơn 41%", thật không?''', '''"Startup is 41% faster": is it?''')
    m('overview', '''Sau khi dời một việc khỏi Application.onCreate, có người báo app Hẹn Khám khởi động nhanh hơn 41 %. Cách 1 so một lần đo trước với một lần đo sau. Cách 2 đo lặp 10 lần mỗi bên ở chế độ cold start, trên bản build gần với release, rồi so trung vị và độ dao động. Mọi phép tính (phần trăm, trung vị, khoảng) được tính thật từ 10 số đo mỗi bên.''',
      '''After moving some work out of Application.onCreate, someone reports that ClinicBook starts 41% faster. Way 1 compares one measurement before with one after. Way 2 measures 10 times on each side in cold-start mode, on a release-like build, then compares medians and spread. Every figure (percentages, medians, ranges) is really computed from the 10 measurements on each side.''')
    m('wrapup', '''Con số 41 % đến từ việc so lần chạy đầu sau khi cài (chậm bất thường, 1.480 ms) với một lần chạy nhanh nhất bên kia (870 ms). Lặp 10 lần và so trung vị, mức cải thiện thật là khoảng 50 ms, tức 4,9 %, nhỏ hơn cả độ dao động giữa các lần đo. Một lần đo không nói được gì; trung vị của nhiều lần, cùng điều kiện, mới so được.''',
      '''The 41% came from comparing the first run after install (unusually slow, 1,480 ms) with the fastest run on the other side (870 ms). Repeating 10 times and comparing medians, the real improvement is about 50 ms, 4.9%, smaller than the spread between runs. One measurement says nothing; medians of many runs under the same conditions can be compared.''')
    m('simp.1', '''Mười số đo mỗi bên là của site, chọn để cho thấy một lần chạy đầu chậm và độ dao động thường gặp; số thật tùy máy và app.''',
      '''The 10 measurements per side are the site\'s, chosen to show a slow first run and typical spread; real numbers depend on the device and the app.''')
    m('simp.2', '''Phần trăm, trung vị, nhỏ nhất, lớn nhất được tính thật bằng JavaScript từ hai dãy 10 số; phần trăm cải thiện là (trước − sau) ÷ trước.''',
      '''Percentages, medians, minimums and maximums are really computed in JavaScript from the two lists of 10 numbers; the improvement percentage is (before − after) ÷ before.''')
    m('ctl.hint', '''Chọn cách đo rồi đi qua bốn bước; xem chấm nào được dùng để so và vạch trung vị.''', '''Pick a way of measuring and walk the four steps; watch which dots are used for the comparison and the median marks.''')
    m('ctl.case', '''Cách đo''', '''How it is measured''')
    m('ctl.case.once', '''một lần trước, một lần sau''', '''one run before, one after'''); m('ctl.case.repeat', '''lặp 10 lần, so trung vị''', '''10 runs, compare medians''')
    m('diagramTitle', '''Từ lần chạy tới kết luận''', '''From runs to a conclusion''')
    m('diagramDesc', '''Bản build gần release chạy nhiều lần; mỗi lần cho một số đo; gom lại thành trung vị và khoảng rồi mới so''', '''A release-like build runs many times; each run gives a measurement; they are summarised as median and range before comparing''')
    for k, vi, en in [('build', 'Bản build đo (gần release)', 'Measured build (release-like)'), ('runs', 'Các lần chạy (cold start)', 'Runs (cold start)'), ('stats', 'Trung vị, nhỏ nhất, lớn nhất', 'Median, min, max'),
                      ('claim', 'Kết luận', 'Conclusion'), ('noise', 'Nhiễu: lần đầu, nền, nhiệt, pin', 'Noise: first run, background, heat, battery')]:
        m('n.' + k, vi, en)
    m('met.runs', '''Số lần đo mỗi bên''', '''Runs per side'''); m('met.claim', '''Cải thiện báo cáo (%)''', '''Reported improvement (%)''')
    m('met.mb', '''Trung vị trước (ms)''', '''Median before (ms)'''); m('met.ma', '''Trung vị sau (ms)''', '''Median after (ms)''')
    a('cap.measure', '''Đo nhiều lần trên bản build gần release, gom thành trung vị và khoảng, rồi mới kết luận. Ô đỏ: kết luận rút từ một lần đo.''', '''Measure many times on a release-like build, summarise as median and range, then conclude. A red box: a conclusion drawn from one measurement.''')
    S = [
        ('once', 's1', 'Đo trước: một lần, ngay sau khi cài', 'Before: one run, right after installing',
         'Cài bản cũ rồi mở app ngay: khởi động mất 1.480 ms. Đây là lần chạy đầu sau khi cài, thường chậm bất thường vì nhiều thứ chưa sẵn sàng, nhưng người đo không biết điều đó.',
         'Install the old build and open the app straight away: startup takes 1,480 ms. This is the first run after installing, usually unusually slow because much is not ready yet, but the person measuring does not know that.'),
        ('once', 's2', 'Đo sau: một lần, 870 ms, "nhanh hơn 41%"', 'After: one run, 870 ms, "41% faster"',
         'Cài bản mới, mở vài lần cho chắc, lấy lần nhanh nhất: 870 ms. (1.480 − 870) ÷ 1.480 = 41 %. Con số nghe rất đẹp và được đưa vào ghi chú phát hành.',
         'Install the new build, open it a few times to be sure, take the fastest: 870 ms. (1,480 − 870) ÷ 1,480 = 41%. The number sounds great and goes into the release notes.'),
        ('once', 's3', 'Đo lại bản mới: 975 ms', 'Measure the new build again: 975 ms',
         'Một đồng nghiệp đo lại bản mới và được 975 ms, rồi 960 ms. Lần 870 ms là lần nhanh nhất trong cả loạt, không phải lần điển hình. Hai lần đo một bên đã chênh nhau hơn 100 ms.',
         'A colleague measures the new build again and gets 975 ms, then 960 ms. The 870 ms run was the fastest of the lot, not a typical one. Two runs on the same side already differ by more than 100 ms.'),
        ('once', 's4', 'Một lần đo không nói được gì', 'One measurement says nothing',
         'Khi độ dao động giữa các lần đo lớn hơn mức chênh muốn chứng minh, so một lần với một lần chỉ là so may với rủi. Kết luận 41 % không đứng được.',
         'When the spread between runs is bigger than the difference you want to show, comparing one run with one run is comparing luck with bad luck. The 41% claim does not stand.'),
        ('repeat', 's1', 'Lặp 10 lần mỗi bên, cold start, bản build gần release', '10 runs per side, cold start, a release-like build',
         'Dùng Macrobenchmark với StartupTimingMetric, startupMode COLD, 10 lần lặp, trên một build không debuggable, có thu gọn mã, chạy trên máy thật. Mỗi bên có 10 số đo.',
         'Use Macrobenchmark with StartupTimingMetric, startupMode COLD, 10 iterations, on a non-debuggable build with code shrinking, on a real device. Each side gets 10 measurements.'),
        ('repeat', 's2', 'So trung vị: 1.012,5 ms và 962,5 ms', 'Compare medians: 1,012.5 ms and 962.5 ms',
         'Trung vị không bị kéo bởi một lần chạy bất thường như 1.480 ms. Trung vị trước 1.012,5 ms, sau 962,5 ms: nhanh hơn 50 ms, tức 4,9 %.',
         'The median is not dragged by one unusual run such as 1,480 ms. Median before 1,012.5 ms, after 962.5 ms: 50 ms faster, 4.9%.'),
        ('repeat', 's3', 'Xem độ dao động: các khoảng chồng lên nhau', 'Look at the spread: the ranges overlap',
         'Bên trước từ 990 tới 1.480 ms, bên sau từ 870 tới 1.050 ms. Phần lớn các chấm của hai bên nằm lẫn vào nhau. Mức cải thiện có thật nhưng nhỏ, cùng cỡ với độ dao động.',
         'Before ranges from 990 to 1,480 ms, after from 870 to 1,050 ms. Most dots of the two sides are mixed together. The improvement is real but small, about the size of the spread.'),
        ('repeat', 's4', 'Kết luận trung thực: khoảng 5 %, đo lại trên máy khác', 'An honest conclusion: about 5%, measure again on another device',
         'Ghi "trung vị khởi động lạnh giảm khoảng 50 ms (5 %) trên máy X, 10 lần mỗi bên", kèm khoảng nhỏ nhất, lớn nhất. Muốn chắc hơn thì đo thêm lần, thêm máy, và giữ nguyên điều kiện cho cả hai bên.',
         'Write "median cold startup down about 50 ms (5%) on device X, 10 runs each", with the min and max. To be more confident, add runs and devices, and keep the conditions the same on both sides.'),
    ]
    for case, k, tv, te, xv, xe in S:
        sid = case + '.' + k
        m('s.%s.title' % sid, tv, te); m('s.%s.explain' % sid, xv, xe); m('ev.' + sid, tv, te)
    for k, vi, en in [
        ('try', '''Mẹo đọc: hai hàng chấm là các lần đo trước và sau trên trục mili giây; chấm viền đỏ là chấm được dùng để so; vạch dọc là trung vị của mỗi hàng.''',
         '''Reading tip: the two rows of dots are the runs before and after on a millisecond axis; red-outlined dots are the ones used for the comparison; the vertical mark is each row\'s median.'''),
        ('once.s2', '''Đo khởi động thì tài liệu khuyên tối ưu theo giả định cold start, tức app khởi động từ đầu; lần chạy ngay sau khi cài là một trường hợp đặc biệt của nó. [[src:ad-launch-time]]''',
         '''For startup, the documentation recommends optimising for a cold start, when the app starts from scratch; the run right after installing is a special case of it. [[src:ad-launch-time]]'''),
        ('once.s3', '''StartupTimingMetric báo nhỏ nhất, trung vị và lớn nhất của các lần lặp, và tài liệu nói rõ: luôn tập trung vào trung vị. [[src:ad-macro-metrics]]''',
         '''StartupTimingMetric reports the minimum, median and maximum of the iterations, and the documentation says plainly: always focus on median values. [[src:ad-macro-metrics]]'''),
        ('once.s4', '''Đây là vòng gỡ lỗi của chương "Quy trình gỡ lỗi, adb và bug report" áp cho hiệu năng: giả thuyết "nhanh hơn" phải được kiểm bằng phép đo lặp lại được.''',
         '''This is the debugging loop of "The debugging process, adb and bug reports" applied to performance: the hypothesis "it is faster" must be tested with a repeatable measurement.'''),
        ('repeat.s1', '''Macrobenchmark chạy trong một module test riêng; app được đo nên cấu hình gần bản release nhất có thể: không debuggable, nên bật thu gọn mã, và phải profileable. Tài liệu không khuyên chạy trên emulator. [[src:ad-macrobenchmark]]''',
         '''Macrobenchmark runs in a separate test module; the measured app should be configured as close to release as possible: non-debuggable, preferably with minification, and profileable. The documentation discourages running on an emulator. [[src:ad-macrobenchmark]]'''),
        ('repeat.s2', '''Trung vị là giá trị ở giữa khi xếp các số đo theo thứ tự; với số lần chẵn, là trung bình của hai số giữa. Nó ít bị một lần chạy bất thường kéo lệch hơn trung bình cộng.''',
         '''The median is the middle value when the measurements are sorted; with an even count, it is the average of the two middle ones. It is pulled less by one unusual run than the mean is.'''),
        ('repeat.s3', '''Với khung hình, FrameTimingMetric báo các phân vị P50, P90, P95, P99; tài liệu khuyên nhìn vào các khung tệ nhất ở P95 và P99. [[src:ad-macro-metrics]]''',
         '''For frames, FrameTimingMetric reports the P50, P90, P95 and P99 percentiles; the documentation advises looking at the worst frames, at P95 and P99. [[src:ad-macro-metrics]]'''),
        ('repeat.s4', '''Macrobenchmark báo lỗi khi app debuggable, khi chạy trên emulator hay khi pin yếu, vì những điều kiện đó làm sai số đo. [[src:ad-macrobenchmark]]''',
         '''Macrobenchmark reports errors for debuggable apps, emulators and low battery, because those conditions distort the measurements. [[src:ad-macrobenchmark]]'''),
    ]:
        m('co.' + k, vi, en)

    z = lambda k, vi, en=None: a('vz.' + k, vi, en)
    z('tab.measure', '''Các lần đo và trung vị''', '''Runs and medians''')
    z('ms.aria', '''Hai hàng 10 lần đo; trung vị trước {b} ms, sau {a} ms''', '''Two rows of 10 runs; median before {b} ms, after {a} ms''')
    z('ms.row.before', '''trước''', '''before'''); z('ms.row.after', '''sau''', '''after''')
    z('ms.claim.once', '''So {b} ms với {a} ms: nhanh hơn {p} %.''', '''{b} ms against {a} ms: {p}% faster.''')
    z('ms.claim.repeat', '''Trung vị {b} ms so với {a} ms: nhanh hơn {p} %.''', '''Median {b} ms against {a} ms: {p}% faster.''')
    z('ms.range', '''Trước: {b1}–{b2} ms. Sau: {a1}–{a2} ms.''', '''Before: {b1}–{b2} ms. After: {a1}–{a2} ms.''')
    z('ms.wait', '''(chưa có số đo bên sau)''', '''(no "after" measurement yet)''')
    z('ms.legend', '''Mỗi chấm là một lần khởi động lạnh. Chấm viền đỏ: số được dùng để so. Vạch dọc: trung vị của hàng.''',
      '''Each dot is one cold start. A red-outlined dot: a number used for the comparison. Vertical mark: the row\'s median.''')

    C = 'l12'
    a(C + '.title', '''Đo hiệu năng cho đúng''', '''Measuring performance properly''')
    a(C + '.essence', '''Mỗi lần đo cho một số khác: lần chạy đầu sau khi cài chậm bất thường, các lần sau dao động vì việc nền, nhiệt độ, pin. So một lần đo trước với một lần đo sau có thể cho "nhanh hơn 41 %" dù thật ra chỉ 5 %.\nĐo cho đúng: chạy trên bản build gần release (không debuggable, có thu gọn mã) trên máy thật, lặp nhiều lần ở cùng chế độ (ví dụ cold start), rồi so trung vị và nhìn độ dao động. Macrobenchmark làm việc đó và báo nhỏ nhất, trung vị, lớn nhất; với khung hình thì báo các phân vị P50 tới P99.\nKết luận nên nói rõ: cải thiện bao nhiêu ms, trên máy nào, bao nhiêu lần đo, khoảng dao động ra sao.''',
      '''Every measurement gives a different number: the first run after installing is unusually slow, later runs vary with background work, temperature, battery. Comparing one run before with one after can give "41% faster" when it is really 5%.\nMeasuring properly: run a release-like build (non-debuggable, with code shrinking) on a real device, repeat many times in the same mode (cold start, for example), then compare medians and look at the spread. Macrobenchmark does that and reports minimum, median and maximum; for frames it reports the P50 to P99 percentiles.\nA conclusion should say: how many ms of improvement, on which device, how many runs, and how wide the spread.''')
    a(C + '.goal.g1', '''Đã thấy một lần đo cho kết luận sai''', '''Saw one measurement give a wrong conclusion''')
    a(C + '.goal.g2', '''Đã so trung vị và độ dao động''', '''Compared medians and spread''')
    a(C + '.sim.debugging.measure', '''một lần đo, hay lặp và so trung vị''', '''one measurement, or repeat and compare medians''')

    S_ = 'hook'
    a(C + '.sec.%s.title' % S_, '''Đoán trước khi đọc''', '''Predict before reading''')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'predict', '''Bản cũ khởi động 1.480 ms (lần đầu sau khi cài), bản mới 870 ms (lần nhanh nhất trong vài lần thử). Nhanh hơn 41 %. Bạn có tin không, và cần thêm gì để tin?''',
      '''The old build starts in 1,480 ms (the first run after installing), the new one in 870 ms (the fastest of a few tries). 41% faster. Do you believe it, and what would you need to believe it?''')
    B(C, S_, 1, 'ans', '''Chưa nên tin: hai số đến từ hai lần chạy đặc biệt. Cần nhiều lần đo mỗi bên, cùng chế độ khởi động, cùng loại build, rồi so trung vị. Mô phỏng ngay dưới làm đúng như vậy, và con số còn khoảng 5 %.''',
      '''Not yet: both numbers come from special runs. You need many runs on each side, in the same startup mode, on the same kind of build, then compare medians. The simulation just below does exactly that, and the number drops to about 5%.''')

    S_ = 'why'
    a(C + '.sec.%s.title' % S_, '''Vì sao một lần đo không đủ''', '''Why one measurement is not enough''')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'p', '''Cùng một bản app, cùng một máy, mỗi lần khởi động cho một thời gian khác: lần đầu sau khi cài thường chậm bất thường, các lần sau dao động vì việc nền của hệ thống, nhiệt độ, mức pin. Bản debug còn chạy chậm hơn bản release nhiều, nên đo trên bản debug không nói gì về người dùng. Emulator cũng không phản ánh máy thật; Macrobenchmark báo lỗi khi gặp app debuggable, emulator hay pin yếu vì các lý do đó. [[src:ad-macrobenchmark]]''',
      '''The same build on the same device gives a different time on every launch: the first run after installing is usually unusually slow, later runs vary with system background work, temperature and battery level. A debug build is also much slower than a release build, so measuring a debug build says nothing about users. An emulator does not reflect a real device either; Macrobenchmark reports errors for debuggable apps, emulators and low battery for those reasons. [[src:ad-macrobenchmark]]''')
    B(C, S_, 2, 'p', '''Vì vậy hãy coi mỗi số đo là một mẫu, không phải "thời gian khởi động". Thứ so được là tóm tắt của nhiều mẫu: trung vị (giá trị giữa, ít bị một lần bất thường kéo lệch) và khoảng (nhỏ nhất tới lớn nhất). Mức chênh nhỏ hơn độ dao động thì cần thêm mẫu trước khi kết luận.''',
      '''So treat each number as one sample, not as "the startup time". What can be compared is a summary of many samples: the median (the middle value, pulled little by one unusual run) and the range (minimum to maximum). A difference smaller than the spread needs more samples before any conclusion.''')

    S_ = 'macro'
    a(C + '.sec.%s.title' % S_, '''Macrobenchmark: đo lặp tự động''', '''Macrobenchmark: automated repeated measurement''')
    a(C + '.sec.%s.badge' % S_, 'version')
    B(C, S_, 1, 'p', '''Macrobenchmark đo các thao tác lớn mà người dùng thấy: khởi động app, cuộn một danh sách, chạy animation. Nó chạy trong một module test riêng, điều khiển app được đo như người dùng. App được đo nên cấu hình gần bản release: không debuggable, nên bật thu gọn mã, và phải profileable. Kết quả in ra Android Studio và ghi vào tệp JSON, kèm một trace cho mỗi lần lặp, để mở bằng các công cụ ở chương "CPU, trace và khung hình giật". [[src:ad-macrobenchmark]]''',
      '''Macrobenchmark measures large user-visible interactions: app startup, scrolling a list, running animations. It runs in a separate test module and drives the measured app like a user. The measured app should be configured close to release: non-debuggable, preferably with minification, and profileable. Results are printed in Android Studio and written to a JSON file, with one trace per iteration, to open with the tools of "CPU, traces and janky frames". [[src:ad-macrobenchmark]]''')
    B(C, S_, 2, 'kt', '''@get:Rule val rule = MacrobenchmarkRule()

@Test fun coldStartup() = rule.measureRepeated(
    packageName = "vn.henkham",
    metrics = listOf(StartupTimingMetric()),
    iterations = 10,
    startupMode = StartupMode.COLD,          // tiến trình bị đóng trước mỗi lần đo
) {
    pressHome()
    startActivityAndWait()
}''', '''@get:Rule val rule = MacrobenchmarkRule()

@Test fun coldStartup() = rule.measureRepeated(
    packageName = "vn.henkham",
    metrics = listOf(StartupTimingMetric()),
    iterations = 10,
    startupMode = StartupMode.COLD,          // the process is killed before each measurement
) {
    pressHome()
    startActivityAndWait()
}''')
    B(C, S_, 3, 'p', '''StartupTimingMetric báo timeToInitialDisplayMs và timeToFullDisplayMs với nhỏ nhất, trung vị, lớn nhất; tài liệu khuyên luôn tập trung vào trung vị. FrameTimingMetric báo thời gian CPU của mỗi khung và phần quá hạn, theo phân vị P50, P90, P95, P99; nên nhìn các khung tệ nhất ở P95, P99. compilationMode điều khiển việc biên dịch trước (mặc định cài Baseline Profile nếu có), nên khi so trước và sau, giữ nguyên nó. [[src:ad-macro-metrics]] [[src:ad-macrobenchmark]]''',
      '''StartupTimingMetric reports timeToInitialDisplayMs and timeToFullDisplayMs with minimum, median and maximum; the documentation advises always focusing on the median. FrameTimingMetric reports each frame\'s CPU time and overrun, as P50, P90, P95 and P99 percentiles; look at the worst frames at P95 and P99. compilationMode controls ahead-of-time compilation (by default it installs a Baseline Profile if available), so keep it unchanged when comparing before and after. [[src:ad-macro-metrics]] [[src:ad-macrobenchmark]]''')

    S_ = 'startup'
    a(C + '.sec.%s.title' % S_, '''Đo khởi động: TTID, TTFD, cold, warm, hot''', '''Measuring startup: TTID, TTFD, cold, warm, hot''')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'p', '''TTID (time to initial display) là thời gian tới khung hình đầu tiên của giao diện. TTFD (time to full display) là thời gian tới khi app dùng được thật; nó chỉ được báo khi app gọi reportFullyDrawn. Cold start là khởi động từ đầu, ví dụ lần đầu sau khi bật máy hay sau khi hệ thống đóng app; warm start làm một phần các bước đó; hot start chỉ đưa Activity sẵn có lên trước. Tài liệu khuyên tối ưu theo giả định cold start. Logcat cũng in một dòng Displayed với thời gian, đủ để xem nhanh nhưng không thay cho đo lặp lại. [[src:ad-launch-time]]''',
      '''TTID (time to initial display) is the time to the first frame of the UI. TTFD (time to full display) is the time until the app is truly usable; it is reported only when the app calls reportFullyDrawn. A cold start begins from scratch, for example the first launch after boot or after the system killed the app; a warm start does a subset of those steps; a hot start only brings an existing Activity to the front. The documentation recommends optimising for a cold start. Logcat also prints a Displayed line with a time, fine for a quick look but no substitute for repeated measurement. [[src:ad-launch-time]]''')
    B(C, S_, 2, 'p', '''Muốn biết dời việc gì khỏi lúc khởi động và vì sao, đọc chương "Khởi động, pin và kích thước app" của track Thiết kế hệ thống phía mobile; cách Compose đo và giảm việc khi recompose ở chương "Hiệu năng và debug: đo trước, sửa sau" của track Compose Runtime. Chương này chỉ lo phần đo sao cho đúng.''',
      '''What to move out of startup and why is covered in "Startup, battery and app size" in the Mobile System Design track; how Compose measures and reduces recomposition work in "Performance and debugging: measure first, then fix" in the Compose Runtime track. This chapter only covers measuring correctly.''')

    S_ = 'compare'
    a(C + '.sec.%s.title' % S_, '''So trước và sau cho công bằng''', '''Comparing before and after fairly''')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'p', '''Giữ mọi thứ giống nhau trừ thay đổi muốn đo: cùng máy, cùng loại build, cùng chế độ khởi động, cùng chế độ biên dịch, cùng số lần lặp, pin đủ và máy không nóng. Đo cả hai bên trong cùng một buổi nếu được. So trung vị, và ghi khoảng nhỏ nhất, lớn nhất. Nếu khoảng của hai bên chồng nhiều lên nhau, mức chênh nhỏ: thêm lần đo, thêm máy trước khi kết luận. Đây cũng là bước "kiểm" của vòng gỡ lỗi, áp cho hiệu năng.''',
      '''Keep everything the same except the change you want to measure: same device, same kind of build, same startup mode, same compilation mode, same number of iterations, enough battery and a device that is not hot. Measure both sides in the same session if you can. Compare medians, and record the min and max. If the two ranges overlap a lot, the difference is small: add runs and devices before concluding. This is the "test it" step of the debugging loop, applied to performance.''')

    S_ = 'bugs'
    a(C + '.sec.%s.title' % S_, '''Hai lỗi hay gặp''', '''Two common bugs''')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'bug', '''Tối ưu cho bản debug nhanh hơn 30 %; bản release trên máy người dùng không nhanh hơn chút nào.''', '''An optimisation makes the debug build 30% faster; the release build on users\' phones is not faster at all.''')
    B(C, S_, 1, 'cause', '''Bản debug chạy chậm vì những lý do không có ở bản release; thứ được "tối ưu" là chi phí của chế độ debug.''', '''The debug build is slow for reasons the release build does not have; what was "optimised" was the cost of debug mode.''')
    B(C, S_, 1, 'fix', '''Chỉ đo trên build gần release (không debuggable, có thu gọn mã, profileable), như Macrobenchmark yêu cầu.''', '''Measure only on a release-like build (non-debuggable, with shrinking, profileable), as Macrobenchmark requires.''')
    B(C, S_, 2, 'bug', '''Báo cáo hiệu năng hằng tuần lúc tăng lúc giảm 15 % mà không ai đổi mã.''', '''A weekly performance report swings up and down by 15% while nobody changed the code.''')
    B(C, S_, 2, 'cause', '''Mỗi tuần chỉ đo 3 lần, trên các máy khác nhau, đôi khi lúc máy đang sạc và nóng.''', '''Only 3 runs a week, on different devices, sometimes while the device is charging and hot.''')
    B(C, S_, 2, 'fix', '''Cố định máy và điều kiện, tăng số lần lặp, so trung vị và theo dõi cả khoảng dao động thay vì một con số.''', '''Fix the device and conditions, increase iterations, compare medians and track the spread rather than one number.''')

    S_ = 'ex'
    a(C + '.sec.%s.title' % S_, '''Bài tập''', '''Exercise''')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'ex', '''Năm lần đo khởi động lạnh, trước: 820, 805, 1.300, 815, 810 ms; sau: 790, 800, 785, 795, 805 ms. Tính trung vị mỗi bên và phần trăm cải thiện. Nếu chỉ so trung bình cộng thì được bao nhiêu phần trăm, và vì sao khác?''',
      '''Five cold-start runs, before: 820, 805, 1,300, 815, 810 ms; after: 790, 800, 785, 795, 805 ms. Compute each side\'s median and the improvement percentage. Comparing means instead, what percentage do you get, and why does it differ?''')
    B(C, S_, 1, 'hint', '''Xếp thứ tự rồi lấy số giữa. Trung bình cộng bị kéo bởi lần 1.300 ms.''', '''Sort, then take the middle value. The mean is pulled by the 1,300 ms run.''')
    B(C, S_, 1, 'sol', '''Trung vị trước 815 ms, sau 795 ms: nhanh hơn (815 − 795) ÷ 815 ≈ 2,5 %. Trung bình trước 910 ms, sau 795 ms: "nhanh hơn" 12,6 %, vì một lần chạy bất thường 1.300 ms kéo trung bình bên trước lên. Trung vị cho bức tranh đúng hơn.''',
      '''Median before 815 ms, after 795 ms: (815 − 795) ÷ 815 ≈ 2.5% faster. Mean before 910 ms, after 795 ms: "12.6% faster", because one unusual 1,300 ms run drags the before mean up. The median gives the truer picture.''')

    S_ = 'recall'
    a(C + '.sec.%s.title' % S_, '''Tự trả lời''', '''Answer it yourself''')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'ask', '''Vì sao nên so trung vị thay vì một lần đo?''', '''Why compare medians rather than single measurements?''')
    B(C, S_, 1, 'ans', '''Mỗi lần đo dao động; một lần có thể là lần bất thường. Trung vị của nhiều lần ít bị một lần như vậy kéo lệch.''', '''Every run varies; one run may be an unusual one. The median of many runs is pulled little by such a run.''')
    B(C, S_, 2, 'ask', '''App được đo bằng Macrobenchmark nên cấu hình thế nào?''', '''How should an app measured with Macrobenchmark be configured?''')
    B(C, S_, 2, 'ans', '''Gần bản release: không debuggable, nên bật thu gọn mã, profileable; chạy trên máy thật, không phải emulator.''', '''Close to release: non-debuggable, preferably with minification, profileable; on a real device, not an emulator.''')

    for q, qv, qe, av, ae, wv, we in [
        ('q1', 'StartupTimingMetric báo những giá trị nào?', 'Which values does StartupTimingMetric report?', 'Nhỏ nhất, trung vị, lớn nhất của các lần lặp.', 'The minimum, median and maximum of the iterations.',
         'Tài liệu khuyên tập trung vào trung vị.', 'The documentation advises focusing on the median.'),
        ('q2', 'TTFD chỉ được báo khi nào?', 'When is TTFD reported?', 'Khi app gọi reportFullyDrawn.', 'When the app calls reportFullyDrawn.',
         'Không gọi thì không có giá trị TTFD.', 'Without the call, no TTFD value is reported.'),
        ('q3', 'Khi khoảng đo trước và sau chồng nhiều lên nhau, nên làm gì?', 'When the before and after ranges overlap a lot, what should you do?', 'Thêm lần đo, thêm máy trước khi kết luận.', 'Add runs and devices before concluding.',
         'Mức chênh nhỏ hơn độ dao động chưa đủ để kết luận.', 'A difference smaller than the spread is not enough to conclude.')]:
        a(C + '.quiz.%s.q' % q, qv, qe); a(C + '.quiz.%s.a' % q, av, ae); a(C + '.quiz.%s.why' % q, wv, we)
