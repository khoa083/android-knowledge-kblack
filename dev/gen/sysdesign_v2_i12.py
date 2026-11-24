# Thiết kế hệ thống phía mobile · I12: quan sát và phát hành an toàn (Phần 2)
# Nguồn: DDIA bản 2 ch.5 (mã cũ và mới cùng tồn tại; tương thích ngược, xuôi; thêm trường giữ tương thích; nhiều phiên bản API); Seemann,
# Code That Fits in Your Head 10.1 (feature flag), 10.3 (Semantic Versioning); Android vitals (1,09%, 0,47%, 8%); Play staged rollout,
# In-app updates (chỉ nhắc); kotlinx.serialization (khóa lạ mặc định gây lỗi; ignoreUnknownKeys). Đọc 2026-11-24.

SEC_ORDER = {'i12': ['hook', 'versions', 'rollout', 'flags', 'compat', 'bugs', 'ex']}


def add(a):
    def B(ch, sec, n, field, vi, en=None):
        a('%s.sec.%s.b.%02d.%s' % (ch, sec, n, field), vi, vi if en is None else en)

    # ---------- mô phỏng 1: phát hành ----------
    a('preset.rollout', 'Thiết kế hệ thống · phát hành bản 1.2.0', 'System design · releasing version 1.2.0')
    m = lambda k, vi, en=None: a('m.rollout.' + k, vi, en)
    m('title', 'Phát hành 100% một lần, theo phần trăm, hay sau feature flag', 'Release to 100% at once, by percentage, or behind a feature flag')
    m('overview', 'App có 100.000 người dùng. Bản 1.2.0 thêm màn đặt lịch mới, và màn đó crash trên 3% số máy (một hãng điện thoại), điều không ai thấy khi thử. Ba cách phát hành: 100% ngay ngày đầu; theo phần trăm, bắt đầu từ 1%; phát hành 100% nhưng giấu màn mới sau một feature flag (cờ tính năng: công tắc do server bật tắt). Tốc độ cài, số người, ngày là minh họa.',
      'The app has 100,000 users. Version 1.2.0 adds a new booking screen, which crashes on 3% of devices (one manufacturer), something nobody saw in testing. Three ways to release: 100% on day one; by percentage, starting at 1%; 100% but with the new screen hidden behind a feature flag (a switch the server turns on and off). Install speed, user counts and days are illustrative.')
    m('wrapup', 'Một bản đã cài thì không gỡ về được; chỉ thay bằng bản mới hơn, và người dùng cập nhật chậm. Phát hành 100% một lần để 8.550 người gặp crash trong một tuần. Phát hành từ 1% giới hạn số người chạy bản lỗi, và chỉ số crash vượt ngưỡng sớm báo hiệu; nhưng tạm dừng không gỡ bản khỏi máy đã cài. Feature flag tách "đã cài mã" khỏi "đã bật tính năng": tắt cờ là dừng ngay cho mọi người, không cần bản mới.',
      'An installed version cannot be pulled back; it can only be replaced by a newer one, and users update slowly. Releasing to 100% at once lets 8,550 people crash within a week. Starting at 1% limits who runs the bad version, and the crash rate crossing its threshold warns early; but halting does not remove the version from devices that have it. A feature flag separates "code installed" from "feature enabled": turning the flag off stops it for everyone at once, with no new release.')
    m('simp.1', '100.000 người dùng, 3% máy bị crash, tốc độ cài theo ngày và các bước tăng phần trăm là minh họa. Cờ trên thực tế chỉ có hiệu lực khi app lấy cấu hình mới, thường trong vài phút tới vài giờ.', 'The 100,000 users, 3% of devices crashing, daily install speed and the percentage steps are illustrative. In practice a flag takes effect when the app fetches new config, typically within minutes to hours.')
    m('simp.2', 'Ngưỡng crash 1,09%, ANR 0,47% và 8% của Android vitals lấy từ tài liệu đọc ngày 2026-11-24 và có thể đổi. Chương không bàn công cụ báo crash cụ thể, A/B testing (so sánh hai bản trên hai nhóm người dùng) hay quan sát phía server.', 'The Android vitals thresholds (1.09% crash, 0.47% ANR, 8%) come from docs read on 2026-11-24 and may change. The chapter does not cover specific crash-reporting tools, A/B testing (comparing two versions on two groups of users) or server-side observability.')
    m('ctl.hint', 'Đổi cách phát hành rồi đi lại; so tổng người gặp crash ở bước 4.', 'Switch the release approach and walk again; compare the total crashed users at step 4.')
    m('ctl.case', 'Cách phát hành', 'Release approach')
    for k, vi, en in [('bigbang', '100% ngay ngày đầu', '100% on day one'), ('staged', 'theo phần trăm, từ 1%', 'by percentage, from 1%'), ('flag', 'phát hành 100%, màn mới sau cờ', '100% release, new screen behind a flag')]:
        m('ctl.case.' + k, vi, en)
    m('diagramTitle', 'Play Console, máy người dùng, Android vitals', 'Play Console, users\' devices, Android vitals')
    m('diagramDesc', 'Bản mới đi từ Play Console (trang quản lý app trên Google Play) tới máy người dùng; crash quay về qua Android vitals (bảng chỉ số chất lượng của Google Play)', 'The release flows from Play Console (Google Play\'s app management page) to users\' devices; crashes come back through Android vitals (the Google Play quality dashboard)')
    for k, vi, en in [('console', 'Play Console', 'Play Console'), ('users', 'Máy người dùng', 'Users\' devices'), ('vitals', 'Android vitals (chỉ số chất lượng)', 'Android vitals (quality metrics)')]:
        m('n.' + k, vi, en)
    m('met.exposed', 'Nghìn người chạy mã lỗi', 'Thousand users on the bad code'); m('met.today', 'Người gặp crash hôm nay', 'Users crashing today'); m('met.total', 'Tổng người gặp crash', 'Total users crashed')
    a('cap.rollout', 'Bản mới đi từ trái sang phải; tín hiệu crash quay về Android vitals.', 'The release flows left to right; crash signals return to Android vitals.')
    S = [
        ('bigbang', 's1', 'Ngày 1: phát hành 1.2.0 cho 100%; 40.000 người cài', 'Day 1: 1.2.0 released to 100%; 40,000 install it', '1.200 người gặp crash ngay hôm đầu.', '1,200 people crash on the first day.'),
        ('bigbang', 's2', 'Ngày 2: 70.000 người đã cài; tỉ lệ crash vượt ngưỡng', 'Day 2: 70,000 have installed; the crash rate is over the threshold', 'Bản lỗi tiếp tục lan theo tự động cập nhật.', 'The bad version keeps spreading through auto-updates.'),
        ('bigbang', 's3', 'Ngày 3: phát hành 1.2.1 đã sửa; vẫn còn 85.000 người chạy 1.2.0', 'Day 3: fixed 1.2.1 released; 85,000 are still on 1.2.0', 'Không gỡ được bản đã cài; chỉ chờ người dùng cập nhật lên bản mới hơn.', 'An installed version cannot be removed; you wait for users to update to a newer one.'),
        ('bigbang', 's4', 'Ngày 4 tới 7: bản lỗi giảm dần; tổng 8.550 người gặp crash', 'Days 4 to 7: the bad version fades; 8,550 people crashed in total', 'Phần lớn thiệt hại xảy ra trước khi ai kịp làm gì.', 'Most of the damage happened before anyone could act.'),
        ('staged', 's1', 'Ngày 1: phát hành 1.2.0 cho 1%; 1.000 người cài', 'Day 1: 1.2.0 released to 1%; 1,000 install it', 'Play chọn ngẫu nhiên 1% người dùng.', 'Play randomly selects 1% of users.'),
        ('staged', 's2', 'Ngày 2: tỉ lệ crash trong nhóm 1% là 3%: tạm dừng phát hành', 'Day 2: the crash rate in the 1% group is 3%: halt the rollout', 'Không ai mới nhận bản lỗi, nhưng 1.000 người đã cài vẫn crash.', 'Nobody new gets the bad version, but the 1,000 who have it still crash.'),
        ('staged', 's3', 'Ngày 3: 1.2.1 đã sửa, lại bắt đầu từ 1%', 'Day 3: fixed 1.2.1, again starting at 1%', 'Nhóm đã cài 1.2.0 dần được thay bằng 1.2.1.', 'The group on 1.2.0 is gradually replaced by 1.2.1.'),
        ('staged', 's4', 'Ngày 4 tới 7: tăng lên 5%, 20%, 50%, 100%; tổng 90 người gặp crash', 'Days 4 to 7: raise to 5%, 20%, 50%, 100%; 90 people crashed in total', 'Ít hơn khoảng 95 lần so với phát hành một lần.', 'About 95 times fewer than the single release.'),
        ('flag', 's1', 'Ngày 1: phát hành 1.2.0 cho 100%, cờ màn mới đang tắt', 'Day 1: 1.2.0 released to 100% with the new screen\'s flag off', 'Mã mới đã nằm trên máy, nhưng không ai đi vào nó.', 'The new code is on devices, but nobody reaches it.'),
        ('flag', 's2', 'Ngày 2: bật cờ cho 1%; 30 người crash; tắt cờ trong vài giờ', 'Day 2: flag on for 1%; 30 people crash; flag off within hours', 'Tắt cờ dừng cho cả những máy đã có mã, không cần phát hành gì.', 'Turning the flag off stops it even on devices that have the code, without releasing anything.'),
        ('flag', 's3', 'Ngày 3: 1.2.1 sửa lỗi, cờ vẫn tắt', 'Day 3: 1.2.1 fixes the bug, flag still off', 'Sửa lỗi và bật tính năng là hai việc tách nhau.', 'Fixing the bug and enabling the feature are separate steps.'),
        ('flag', 's4', 'Ngày 4 tới 7: bật cờ 5%, 20%, 50%, 100%; tổng 30 người gặp crash', 'Days 4 to 7: flag on for 5%, 20%, 50%, 100%; 30 people crashed in total', 'Cờ còn cho phép bật tắt độc lập với tiến độ cài bản mới.', 'The flag also lets you ramp independently of install progress.'),
    ]
    for case, k, tv, te, xv, xe in S:
        sid = case + '.' + k
        m('s.%s.title' % sid, tv, te); m('s.%s.explain' % sid, xv, xe); m('ev.' + sid, tv, te)
    for k, vi, en in [
        ('try', 'Đi hết bốn bước của mỗi cách; theo dõi hàng "người gặp crash" theo ngày.', 'Walk all four steps of each approach; follow the "users crashing" row day by day.'),
        ('bigbang.s2', 'Android vitals (bảng chỉ số chất lượng của Google Play): tỉ lệ người dùng gặp crash vượt 1,09% là hành vi xấu; Play có thể giảm hiển thị app và hiện cảnh báo trên trang app. [[src:ax-vitals]]', 'Android vitals (the Google Play quality dashboard): a user-perceived crash rate above 1.09% is bad behaviour; Play may reduce the app\'s visibility and show a warning on its listing. [[src:ax-vitals]]'),
        ('bigbang.s3', 'Với app phía client, bạn phụ thuộc vào người dùng; họ có thể chưa cài bản cập nhật trong một thời gian. [[src:book-ddia2]]', 'With client-side applications you depend on the user, who may not install the update for some time. [[src:book-ddia2]]'),
        ('bigbang.s4', 'Bắt cập nhật ngay (in-app update kiểu immediate: màn chặn toàn phần bắt cập nhật) chỉ nên dùng khi bản cập nhật quan trọng với chức năng chính; nó vẫn cần người dùng mở app. [[src:ax-in-app-updates]]', 'Forcing an update (an immediate in-app update: a full-screen flow that demands the update) is for updates critical to core functionality; it still needs the user to open the app. [[src:ax-in-app-updates]]'),
        ('staged.s2', 'Trợ giúp Google Play: tạm dừng thì không thêm người nhận bản đó, nhưng người đã nhận vẫn giữ nó; có lỗi thì phát hành bản mới đã sửa. [[src:play-staged-rollout]]', 'Google Play help: halting stops new users from getting the release, but those who got it keep it; on problems, roll out a new fixed release. [[src:play-staged-rollout]]'),
        ('staged.s3', 'Android vitals tính trên 28 ngày gần nhất; nhóm 1% đủ để thấy tỉ lệ crash 3%, cao gần ba lần ngưỡng. [[src:ax-vitals]]', 'Android vitals uses the last 28 days; the 1% group is enough to see a 3% crash rate, nearly three times the threshold. [[src:ax-vitals]]'),
        ('staged.s4', 'Theo phần trăm không làm bản lỗi bớt lỗi; nó chỉ giới hạn số người gặp trước khi bạn biết.', 'A staged rollout does not make the bug less buggy; it only limits how many hit it before you know.'),
        ('flag.s2', 'Mark Seemann nhận xét: tách tính năng khỏi mã hiện thực nó; mã chưa xong vẫn triển khai được nếu hành vi bị ẩn sau feature flag. [[src:book-seemann]]', 'Mark Seemann notes: separate the feature from the code that implements it; incomplete code can be deployed if its behaviour is hidden behind a feature flag. [[src:book-seemann]]'),
        ('flag.s3', 'Cờ phải có giá trị mặc định an toàn trên máy (tắt), để khi không lấy được cấu hình thì app vẫn đi đường cũ. Đây là gợi ý của site.', 'A flag needs a safe on-device default (off), so when config cannot be fetched the app still takes the old path. This is the site\'s suggestion.'),
        ('flag.s4', 'Cờ là nợ: sau khi tính năng ổn định, hãy xóa cờ và đường mã cũ để mã không phình ra. Đây là gợi ý của site.', 'Flags are debt: once the feature is stable, remove the flag and the old code path so the code does not bloat. This is the site\'s suggestion.')]:
        m('co.' + k, vi, en)

    # ---------- mô phỏng 2: tương thích ----------
    a('preset.compat', 'Thiết kế hệ thống · đổi API khi app cũ còn đang chạy', 'System design · changing the API while old apps still run')
    u = lambda k, vi, en=None: a('m.compat.' + k, vi, en)
    u('title', 'Đổi tên trường, thêm trường, mở /v2, hay bắt cập nhật', 'Rename a field, add a field, open /v2, or force an update')
    u('overview', 'Server muốn đổi trường doctorName thành một đối tượng doctor có thêm ảnh và chuyên khoa. Ngoài kia đang có bốn phiên bản app: 1.0 (4% người dùng, giải mã JSON chặt: gặp tên trường lạ là báo lỗi), 1.1 (11%) và 1.2 (60%) giải mã có bỏ qua khóa lạ (tên trường JSON mà app không biết), và 1.3 (25%) đã biết trường mới. Bốn cách đổi: đổi tên ngay trên API cũ; thêm trường mới và giữ trường cũ; mở /v2 (đường dẫn API có số phiên bản) cho bản mới; thêm trường và bắt bản 1.0 cập nhật. Tỉ lệ phiên bản là minh họa.',
      'The server wants to turn the doctorName field into a doctor object with a photo and specialty. Four app versions are out there: 1.0 (4% of users, strict JSON decoding: an unknown field name is an error), 1.1 (11%) and 1.2 (60%) decoding with unknown keys (field names the app does not know) ignored, and 1.3 (25%) which knows the new field. Four ways to change: rename in place on the old API; add the new field and keep the old one; open /v2 (an API path carrying a version number) for the new version; add the field and force 1.0 to update. Version shares are illustrative.')
    u('wrapup', 'App cũ không biến mất khi server đổi. Đổi tên tại chỗ làm 75% người dùng lỗi. Thêm trường và giữ trường cũ thường an toàn, miễn là app cũ bỏ qua khóa lạ; bản 1.0 giải mã chặt vẫn vỡ. Mở /v2 thì không ai vỡ nhưng server phải giữ hai phiên bản. Bắt cập nhật biến crash thành một màn hình "hãy cập nhật": vẫn chặn người dùng, nhưng có chủ đích.',
      'Old apps do not vanish when the server changes. Renaming in place breaks 75% of users. Adding a field and keeping the old one is usually safe, as long as old apps ignore unknown keys; the strict 1.0 still breaks. Opening /v2 breaks nobody but the server keeps two versions. Forcing an update turns a crash into an "update please" screen: it still blocks users, but on purpose.')
    u('simp.1', 'Tỉ lệ phiên bản, bốn phiên bản app và việc chỉ có một trường đổi là minh họa.', 'The version shares, the four app versions and a single changed field are illustrative.')
    u('simp.2', 'Mô phỏng chỉ có một trường đổi và bốn bản app; ngoài đời có nhiều trường và nhiều cách giải mã dữ liệu hơn. Ví dụ giải mã dùng thư viện kotlinx.serialization.', 'The simulation has only one changed field and four app versions; real life has more fields and more ways to decode data. The decoding example uses the kotlinx.serialization library.')
    u('ctl.hint', 'Đổi cách thay đổi API rồi đi lại; xem cột "sau thay đổi" ở bước 3.', 'Switch the API change and walk again; look at the "after the change" column at step 3.')
    u('ctl.case', 'Cách đổi API', 'API change')
    for k, vi, en in [('rename', 'đổi tên ngay trên API cũ', 'rename in place'), ('additive', 'thêm trường, giữ trường cũ', 'add a field, keep the old one'), ('versioned', 'mở /v2 cho bản mới', 'open /v2 for the new version'), ('forced', 'thêm trường, bắt 1.0 cập nhật', 'add a field, force 1.0 to update')]:
        u('ctl.case.' + k, vi, en)
    u('diagramTitle', 'Các phiên bản app và API', 'App versions and the API')
    u('diagramDesc', 'Nhiều phiên bản app cùng gọi một server', 'Many app versions call one server')
    for k, vi, en in [('apps', 'App 1.0 tới 1.3', 'Apps 1.0 to 1.3'), ('server', 'API lịch hẹn', 'Bookings API')]:
        u('n.' + k, vi, en)
    u('met.broken', '% người dùng bị lỗi', '% of users broken'); u('met.forced', '% bị bắt cập nhật', '% forced to update'); u('met.apis', 'Phiên bản API phải giữ', 'API versions to maintain')
    a('cap.compat', 'Các phiên bản app bên trái cùng gọi API bên phải.', 'The app versions on the left all call the API on the right.')
    S = [
        ('rename', 's1', 'Bốn phiên bản app đang chạy, tất cả đọc doctorName', 'Four app versions running, all reading doctorName', '1.3 đã biết đối tượng doctor nhưng vẫn đọc được doctorName.', '1.3 knows the doctor object but can still read doctorName.'),
        ('rename', 's2', 'Server đổi doctorName thành doctor ngay trên /v1', 'The server renames doctorName to doctor on /v1 itself', 'Một thay đổi phá vỡ, triển khai một lần cho mọi phiên bản.', 'A breaking change, deployed once for every version.'),
        ('rename', 's3', '1.0, 1.1, 1.2 thiếu trường bắt buộc: lỗi giải mã', '1.0, 1.1, 1.2 miss a required field: decoding fails', '75% người dùng thấy lỗi ở màn lịch hẹn.', '75% of users see the bookings screen fail.'),
        ('rename', 's4', 'Không sửa được phía app: phải khôi phục API cũ', 'It cannot be fixed on the app side: the old API must be restored', 'Bản app cũ không đổi được nữa; chỉ server lùi lại được.', 'Old app versions cannot change any more; only the server can step back.'),
        ('additive', 's1', 'Bốn phiên bản app đang chạy', 'Four app versions are running', '1.0 dùng Json mặc định: khóa lạ là lỗi.', '1.0 uses the default Json: unknown keys are errors.'),
        ('additive', 's2', 'Server thêm doctor, vẫn giữ doctorName', 'The server adds doctor and keeps doctorName', 'Thay đổi thêm vào, không bỏ gì.', 'An additive change; nothing removed.'),
        ('additive', 's3', '1.1 tới 1.3 chạy bình thường; 1.0 gặp khóa lạ: lỗi', '1.1 to 1.3 work; 1.0 hits an unknown key: failure', 'Tương thích xuôi cần mã cũ bỏ qua phần được thêm.', 'Forward compatibility needs old code to ignore additions.'),
        ('additive', 's4', 'Chỉ 4% bị lỗi; lần sau, mọi bản đều bỏ qua khóa lạ', 'Only 4% break; from now on, every version ignores unknown keys', 'Đặt ignoreUnknownKeys (cấu hình bỏ qua tên trường lạ) từ bản đầu là chuẩn bị cho mọi thay đổi sau này.', 'Setting ignoreUnknownKeys (the setting that ignores unknown field names) from the first version prepares for every later change.'),
        ('versioned', 's1', 'Bốn phiên bản app đang chạy, gọi /v1', 'Four app versions running, calling /v1', 'Như các cách trên.', 'As before.'),
        ('versioned', 's2', 'Server giữ nguyên /v1, mở /v2 có doctor', 'The server keeps /v1 unchanged and opens /v2 with doctor', 'Thay đổi phá vỡ chỉ nằm ở phiên bản mới của API.', 'The breaking change lives only in the new API version.'),
        ('versioned', 's3', '1.0 tới 1.2 vẫn gọi /v1; 1.3 gọi /v2: không ai lỗi', '1.0 to 1.2 still call /v1; 1.3 calls /v2: nobody breaks', 'Cái giá ở phía server.', 'The price is on the server side.'),
        ('versioned', 's4', 'Server phải giữ hai phiên bản API tới khi bản cũ hết người dùng', 'The server maintains two API versions until old apps fade out', 'Có thể rất lâu, vì không ép được người dùng cập nhật.', 'Possibly for a long time, since users cannot be made to update.'),
        ('forced', 's1', 'Bốn phiên bản app đang chạy', 'Four app versions are still running', 'Server biết 1.0 giải mã chặt.', 'The server knows 1.0 decodes strictly.'),
        ('forced', 's2', 'Đặt phiên bản tối thiểu 1.1, rồi thêm trường doctor', 'Set the minimum version to 1.1, then add the doctor field', 'App hỏi server phiên bản tối thiểu mỗi lần mở.', 'The app asks the server for the minimum version on each launch.'),
        ('forced', 's3', '1.0 thấy màn "hãy cập nhật" thay vì crash; các bản khác chạy bình thường', '1.0 sees an "update please" screen instead of a crash; the others work', 'Vẫn chặn 4% người dùng, nhưng có lời giải thích và lối ra.', 'It still blocks 4% of users, but with an explanation and a way out.'),
        ('forced', 's4', 'Người dùng 1.0 cập nhật qua in-app update kiểu immediate', '1.0 users update through an immediate in-app update', 'Cơ chế "phiên bản tối thiểu" phải có từ bản đầu thì mới dùng được về sau.', 'The "minimum version" check must ship in the first version to be usable later.'),
    ]
    for case, k, tv, te, xv, xe in S:
        sid = case + '.' + k
        u('s.%s.title' % sid, tv, te); u('s.%s.explain' % sid, xv, xe); u('ev.' + sid, tv, te)
    for k, vi, en in [
        ('try', 'Đi hết bốn bước của mỗi cách; ở bước 3 xem hàng nào chuyển đỏ.', 'Walk all four steps of each approach; at step 3 see which rows turn red.'),
        ('rename.s2', 'Mã cũ và mới, dữ liệu cũ và mới có thể cùng tồn tại; cần tương thích ngược (mã mới đọc được dữ liệu cũ) và tương thích xuôi (mã cũ đọc được dữ liệu mới). [[src:book-ddia2]]', 'Old and new code, old and new data, may coexist; you need backward compatibility (new code reads old data) and forward compatibility (old code reads new data). [[src:book-ddia2]]'),
        ('rename.s3', 'Với API: server mới phải đọc được request kiểu cũ (tương thích ngược), và app cũ phải đọc được response kiểu mới (tương thích xuôi). Bỏ một trường mà app cũ cần là thay đổi phá vỡ (breaking change). [[src:book-ddia2]]', 'For APIs: the new server must read old-style requests (backward compatibility), and old apps must read new-style responses (forward compatibility). Removing a field old clients need is a breaking change. [[src:book-ddia2]]'),
        ('rename.s4', 'Mark Seemann nhắc: mỗi lần phá tương thích là buộc phía gọi phải xử lý; tốt hơn là tránh, hay ít ra báo trước. [[src:book-seemann]]', 'Mark Seemann reminds us: every breaking change forces callers to deal with it; better to avoid it, or at least warn in advance. [[src:book-seemann]]'),
        ('additive.s2', 'Với API REST (kiểu API dùng địa chỉ URL và phương thức HTTP), thêm tham số tùy chọn hay thêm trường vào response thường được coi là giữ tương thích. [[src:book-ddia2]]', 'For REST APIs (the style of API built on URLs and HTTP methods), adding optional request parameters or new response fields is usually considered compatible. [[src:book-ddia2]]'),
        ('additive.s3', 'Tài liệu kotlinx.serialization (thư viện đổi dữ liệu Kotlin sang JSON và ngược lại): mặc định, khóa lạ trong JSON gây lỗi khi giải mã; ignoreUnknownKeys = true thì bỏ qua. [[src:kx-json-config]]', 'kotlinx.serialization docs (the library that converts Kotlin data to and from JSON): by default, unknown keys in the JSON cause a decoding error; ignoreUnknownKeys = true ignores them. [[src:kx-json-config]]'),
        ('additive.s4', 'Tương thích xuôi khó hơn vì cần mã cũ bỏ qua phần mã mới thêm vào. [[src:book-ddia2]]', 'Forward compatibility is harder, because old code must ignore additions made by new code. [[src:book-ddia2]]'),
        ('versioned.s2', 'Martin Kleppmann nhận xét chưa có thống nhất về cách đánh phiên bản API; với REST, thường đặt số phiên bản trong URL hay header Accept (header cho biết định dạng mong muốn). [[src:book-ddia2]]', 'Martin Kleppmann notes there is no agreement on API versioning; for REST, a version number in the URL or the Accept header (which states the format wanted) is common. [[src:book-ddia2]]'),
        ('versioned.s3', 'Ở phía server, Semantic Versioning (cách đánh số phiên bản major.minor.patch) giúp nghĩ rõ đâu là thay đổi phá vỡ: chỉ tăng số major (số đầu) khi phá tương thích. [[src:book-seemann]]', 'On the server, Semantic Versioning (numbering versions as major.minor.patch) helps think clearly about breaking changes: increment major (the first number) only when compatibility breaks. [[src:book-seemann]]'),
        ('versioned.s4', 'Bên cung cấp thường không kiểm soát được client và không ép họ nâng cấp được, nên phải giữ tương thích lâu, có khi vô thời hạn. [[src:book-ddia2]]', 'The provider often cannot control clients or force upgrades, so compatibility must be kept for a long time, maybe indefinitely. [[src:book-ddia2]]'),
        ('forced.s2', 'Kiểm tra phiên bản tối thiểu là một cơ chế của site gợi ý, cần có từ bản đầu tiên; không có nó thì không ép được bản cũ.', 'A minimum version check is a mechanism the site suggests shipping from the first version; without it old versions cannot be forced.'),
        ('forced.s3', 'Cơ chế cập nhật trong app (in-app update) của Google Play: kiểu immediate là màn hình toàn phần bắt cập nhật và khởi động lại, hợp khi bản cập nhật quan trọng với chức năng chính. [[src:ax-in-app-updates]]', 'Google Play\'s in-app update mechanism: the immediate flow is a full-screen flow requiring update and restart, for updates critical to core functionality. [[src:ax-in-app-updates]]'),
        ('forced.s4', 'Bắt cập nhật là công cụ cuối cùng: nó chặn người dùng ở lúc họ đang cần app.', 'Forcing an update is the last resort: it blocks users right when they need the app.')]:
        u('co.' + k, vi, en)

    z = lambda k, vi, en=None: a('vz.' + k, vi, en)
    z('tab.ro', 'Phát hành theo ngày', 'Release by day')
    z('ro.cap', 'Mỗi cột là một ngày; cột có viền là ngày của bước hiện tại; ngày chưa tới để trống.', 'Each column is a day; outlined columns belong to the current step; days not reached are empty.')
    z('ro.col.day', 'Ngày', 'Day')
    for k, vi, en in [('offer', 'Đang phát', 'Rolling out'), ('bad', 'Người chạy mã lỗi', 'Users on bad code'), ('crash', 'Người gặp crash', 'Users crashing')]:
        z('ro.r.' + k, vi, en)
    for k, vi, en in [('o120_100', '1.2.0 · 100%', '1.2.0 at 100%'), ('o121_100', '1.2.1 · 100%', '1.2.1 at 100%'), ('o120_1', '1.2.0 · 1%', '1.2.0 at 1%'), ('halt', 'tạm dừng', 'halted'),
                      ('o121_1', '1.2.1 · 1%', '1.2.1 at 1%'), ('o121_5', '1.2.1 · 5%', '1.2.1 at 5%'), ('o121_20', '1.2.1 · 20%', '1.2.1 at 20%'), ('o121_50', '1.2.1 · 50%', '1.2.1 at 50%'),
                      ('o120_flagoff', '1.2.0 · 100%, cờ tắt', '1.2.0 at 100%, flag off'), ('flag1off', 'cờ bật 1%, rồi tắt', 'flag on at 1%, then off'), ('o121_flagoff', '1.2.1 · 100%, cờ tắt', '1.2.1 at 100%, flag off'),
                      ('flag5', 'cờ 5%', 'flag at 5%'), ('flag20', 'cờ 20%', 'flag at 20%'), ('flag50', 'cờ 50%', 'flag at 50%'), ('flag100', 'cờ 100%', 'flag at 100%')]:
        z('ro.o.' + k, vi, en)
    z('ro.vh', 'Ngưỡng của Android vitals', 'Android vitals thresholds')
    z('ro.vitals', 'Tỉ lệ người dùng gặp crash quá 1,09% (ANR quá 0,47%), hay 8% trên một mẫu điện thoại, là hành vi xấu; Play có thể giảm hiển thị app. Bản lỗi ở đây: 3%.', 'A user-perceived crash rate above 1.09% (ANR above 0.47%), or 8% on one phone model, is bad behaviour; Play may reduce the app\'s visibility. The bad version here: 3%.')
    z('ro.legend', 'Gạch đỏ: còn người chạy mã lỗi hay gặp crash. Chữ đậm: bằng không.', 'Red hatched: people still on the bad code or crashing. Bold: zero.')
    z('tab.cp', 'Ma trận phiên bản', 'Version matrix')
    z('cp.cap', 'Mỗi hàng là một phiên bản app đang được dùng; mỗi cột là API mà nó gọi.', 'Each row is an app version in use; each column is the API it calls.')
    z('cp.changeh', 'Thay đổi phía server', 'Server-side change')
    for k, vi, en in [('none', 'Chưa đổi gì.', 'Nothing changed yet.'), ('rename', 'Đổi doctorName thành doctor ngay trên /v1.', 'Rename doctorName to doctor on /v1 itself.'), ('additive', 'Thêm doctor vào /v1, vẫn giữ doctorName.', 'Add doctor to /v1, keeping doctorName.'),
                      ('versioned', 'Giữ /v1 như cũ; mở /v2 có doctor.', 'Keep /v1 as is; open /v2 with doctor.'), ('forced', 'Phiên bản tối thiểu 1.1; thêm doctor vào /v1.', 'Minimum version 1.1; add doctor to /v1.')]:
        z('cp.change.' + k, vi, en)
    for k, vi, en in [('app', 'Phiên bản app', 'App version'), ('share', 'Người dùng', 'Users'), ('before', '/v1 trước khi đổi', '/v1 before'), ('after', '/v1 sau khi đổi', '/v1 after'), ('v2', '/v2 (mới)', '/v2 (new)')]:
        z('cp.col.' + k, vi, en)
    for k, vi, en in [('v10', '1.0 (Json chặt)', '1.0 (strict Json)'), ('v11', '1.1 (bỏ qua khóa lạ)', '1.1 (ignores unknown keys)'), ('v12', '1.2 (bỏ qua khóa lạ)', '1.2 (ignores unknown keys)'), ('v13', '1.3 (biết doctor)', '1.3 (knows doctor)')]:
        z('cp.app.' + k, vi, en)
    for k, vi, en in [('ok', 'chạy', 'works'), ('same', 'chạy (không đổi)', 'works (unchanged)'), ('crash', 'lỗi giải mã', 'decoding fails'), ('update', 'màn "hãy cập nhật"', '"update please" screen'), ('na', 'không gọi', 'not called')]:
        z('cp.r.' + k, vi, en)
    z('cp.legend', 'Gạch đỏ: lỗi. Viền cam: bị bắt cập nhật. Dấu ?: bước chưa tới.', 'Red hatched: broken. Orange outline: forced to update. A ? means the step is not reached yet.')

    C = 'i12'
    a(C + '.title', 'Quan sát và phát hành an toàn', 'Observability and safe releases')
    a(C + '.essence', 'Bản app đã cài thì không gỡ về được; app cũ còn chạy rất lâu sau khi có bản mới. Vì vậy mọi thay đổi phải tính tới cả máy chưa cập nhật.\nPhát hành theo phần trăm, theo dõi tỉ lệ crash và ANR (app không phản hồi) trên Android vitals (bảng chỉ số chất lượng của Google Play), tạm dừng khi vượt ngưỡng; giấu tính năng mới sau feature flag (cờ tính năng, công tắc do server bật tắt) để tắt được ngay mà không cần bản mới.\nĐổi API theo kiểu thêm vào, để app cũ bỏ qua phần mới (cấu hình ignoreUnknownKeys: bỏ qua tên trường lạ); thay đổi phá vỡ thì đặt ở phiên bản API mới; có sẵn cơ chế phiên bản tối thiểu từ bản đầu.',
      'An installed app version cannot be pulled back; old apps keep running long after a new one ships. So every change must account for devices that have not updated.\nRelease by percentage, watch crash and ANR (app not responding) rates on Android vitals (the Google Play quality dashboard), halt when they cross thresholds; hide new features behind a feature flag (a switch the server turns on and off) so they can be switched off at once without a new release.\nChange APIs additively so old apps ignore what is new (the ignoreUnknownKeys setting: ignore unknown field names); put breaking changes in a new API version; ship a minimum-version mechanism from the first release.')
    a(C + '.goal.g1', 'Đã thấy tác động ở bước 3', 'Saw the impact at step 3')
    a(C + '.goal.g2', 'Đã thấy kết cục', 'Saw the outcome')
    a(C + '.sim.sysdesign.rollout', 'Phát hành', 'Releasing')
    a(C + '.sim.sysdesign.compat', 'Tương thích API', 'API compatibility')

    S_ = 'hook'
    a(C + '.sec.%s.title' % S_, 'Đoán trước khi đọc', 'Predict before reading')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'predict', 'Bạn phát hiện bản 1.2.0 crash trên một hãng điện thoại, hai ngày sau khi phát hành cho mọi người. Backend đề nghị "gỡ 1.2.0 và trả mọi người về 1.1.9". Làm vậy được không? Nếu không, lần sau bạn sẽ phát hành khác đi thế nào?',
      'You find that 1.2.0 crashes on one phone brand, two days after releasing it to everyone. Backend suggests "pull 1.2.0 and roll everyone back to 1.1.9". Can you? If not, how would you release differently next time?')
    B(C, S_, 1, 'ans', 'Không: bản đã cài không gỡ về được; chỉ có thể phát hành bản mới hơn đã sửa, và người dùng cập nhật dần. Lần sau: phát hành theo phần trăm, theo dõi tỉ lệ crash, tạm dừng khi vượt ngưỡng, và giấu tính năng mới sau feature flag để tắt được ngay. [[src:play-staged-rollout]] [[src:book-seemann]]',
      'No: an installed version cannot be pulled back; you can only release a newer fixed one, and users update gradually. Next time: release by percentage, watch the crash rate, halt at the threshold, and hide the new feature behind a flag so it can be switched off at once. [[src:play-staged-rollout]] [[src:book-seemann]]')

    S_ = 'versions'
    a(C + '.sec.%s.title' % S_, 'App cũ sống rất lâu', 'Old apps live a long time')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'p', 'Hãy đặt hai trường hợp cạnh nhau. Ở server, bạn triển khai dần từng máy, theo dõi, rồi đi tiếp. Ở app phía client, bạn phụ thuộc vào người dùng, họ có thể chưa cài bản cập nhật trong một thời gian. Vì vậy mã cũ và mới, dữ liệu cũ và mới, cùng tồn tại; cần tương thích ngược (mã mới đọc được dữ liệu cũ) và tương thích xuôi (mã cũ đọc được dữ liệu mới). [[src:book-ddia2]]',
      'Put two cases side by side. On servers, you roll out machine by machine, watch, then continue. With client-side apps, you depend on users, who may not install the update for some time. So old and new code, old and new data, coexist; you need backward compatibility (new code reads old data) and forward compatibility (old code reads new data). [[src:book-ddia2]]')
    B(C, S_, 2, 'p', 'Hệ quả của site cho mobile: một bản đã cài không gỡ về được, và mọi lỗi của nó tồn tại cho tới khi người dùng cập nhật. Thứ duy nhất bạn còn đổi được sau khi phát hành là server: cấu hình, cờ, và API. Thiết kế từ bản đầu để server có thể điều khiển những gì cần điều khiển.',
      'The site\'s consequence for mobile: an installed version cannot be recalled, and its bugs live until users update. The only thing you can still change after release is the server: config, flags and the API. Design from the first version so the server can control what needs controlling.')

    S_ = 'rollout'
    a(C + '.sec.%s.title' % S_, 'Phát hành theo phần trăm và quan sát', 'Staged rollouts and observation')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'p', 'Trên Google Play, một bản có thể chỉ tới một phần trăm người dùng chọn ngẫu nhiên, rồi tăng dần bằng tay. Tạm dừng thì không thêm ai nhận, nhưng ai đã nhận vẫn giữ bản đó; có lỗi thì phát hành bản mới đã sửa. Cơ chế cụ thể là của Play và có thể đổi; ý chính là giới hạn số người chạy bản mới tới khi có bằng chứng nó ổn. [[src:play-staged-rollout]]',
      'On Google Play, a release can reach only a percentage of randomly chosen users, raised by hand. Halting stops new users from getting it, but those who have it keep it; on problems, release a new fixed version. The exact mechanism is Play\'s and may change; the key idea is limiting who runs the new version until there is evidence it is fine. [[src:play-staged-rollout]]')
    B(C, S_, 2, 'p', 'Bằng chứng đó là chỉ số. Android vitals coi tỉ lệ người dùng gặp crash quá 1,09%, hay gặp ANR quá 0,47%, là hành vi xấu; với một mẫu điện thoại riêng, ngưỡng là 8%. Vượt ngưỡng thì Play có thể giảm hiển thị của app. Số liệu tính trên 28 ngày. Hãy đặt ngưỡng tăng phần trăm của riêng mình thấp hơn thế. [[src:ax-vitals]]',
      'That evidence is metrics. Android vitals treats a user-perceived crash rate above 1.09%, or ANR rate above 0.47%, as bad behaviour; for a single phone model the threshold is 8%. Exceeding them may reduce the app\'s Play visibility. Data covers 28 days. Set your own threshold for raising the percentage lower than that. [[src:ax-vitals]]')
    B(C, S_, 3, 'note', 'Crash theo một hãng hay một phiên bản Android thường chỉ lộ khi có đủ người dùng thật; vì vậy 1% của người dùng thật đáng giá hơn nhiều máy thử. Đây là nhận xét của site.', 'Crashes tied to one brand or Android version often only show with enough real users; that is why 1% of real users is worth more than many test devices. This is the site\'s observation.')
    B(C, S_, 3, 'kind', 'android')

    S_ = 'flags'
    a(C + '.sec.%s.title' % S_, 'Feature flag: tách cài mã khỏi bật tính năng', 'Feature flags: separate shipping code from enabling features')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'p', 'Mark Seemann đưa ra feature flag để tích hợp thường xuyên (gộp code vào nhánh chính liên tục): tách tính năng khỏi mã hiện thực nó; mã chưa xong vẫn triển khai được nếu hành vi bị ẩn sau cờ. Trên mobile, cờ do server điều khiển còn có thêm một giá trị: tắt được tính năng trên những máy đã cài, không cần chờ người dùng cập nhật. [[src:book-seemann]]',
      'Mark Seemann introduces feature flags for frequent integration (merging code into the main branch continually): separate the feature from the code that implements it; incomplete code can be deployed if its behaviour is hidden behind a flag. On mobile, a server-controlled flag adds one more value: switching a feature off on devices that already have it, without waiting for updates. [[src:book-seemann]]')
    B(C, S_, 2, 'p', 'Ba lưu ý của site. Giá trị mặc định trên máy phải an toàn (tắt), vì lần đầu mở app có thể chưa lấy được cấu hình. Cờ chỉ có hiệu lực khi app lấy cấu hình mới, nên không tức thì. Và cờ là nợ: xóa cờ cùng đường mã cũ khi tính năng đã ổn định. Dịch vụ cấu hình từ xa cụ thể (bên thứ ba hay tự làm) không quan trọng bằng ba điều này.',
      'Three notes from the site. The on-device default must be safe (off), since the first launch may not have fetched config yet. A flag only takes effect when the app fetches new config, so it is not instant. And flags are debt: remove the flag and the old code path once the feature is stable. Which remote config service you use (third-party or your own) matters less than these three points.')

    S_ = 'compat'
    a(C + '.sec.%s.title' % S_, 'Đổi API khi app cũ còn chạy', 'Changing the API while old apps still run')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'p', 'Với API REST, thêm tham số tùy chọn hay thêm trường vào response thường được coi là giữ tương thích; bỏ hay đổi tên một trường thì không. Vì bên cung cấp thường không ép được client nâng cấp, thay đổi phá vỡ thường dẫn tới giữ nhiều phiên bản API song song, đánh số trong URL hay header Accept. [[src:book-ddia2]]',
      'For REST APIs, adding optional parameters or response fields is usually considered compatible; removing or renaming a field is not. Since providers usually cannot force clients to upgrade, breaking changes often lead to several API versions side by side, numbered in the URL or the Accept header. [[src:book-ddia2]]')
    B(C, S_, 2, 'p', 'Phía app phải làm phần của mình: tương thích xuôi cần mã cũ bỏ qua phần mới. Với kotlinx.serialization, mặc định khóa lạ gây lỗi khi giải mã; đặt ignoreUnknownKeys = true từ bản đầu tiên. Mark Seemann khuyên nghĩ theo Semantic Versioning: chỉ tăng major khi phá tương thích, và cố ở lâu trên cùng một major. [[src:kx-json-config]] [[src:book-seemann]]',
      'The app must do its part: forward compatibility needs old code to ignore what is new. With kotlinx.serialization, unknown keys fail decoding by default; set ignoreUnknownKeys = true from the very first version. Mark Seemann recommends thinking in Semantic Versioning: increment major only for breaking changes, and try to stay on one major for a long time. [[src:kx-json-config]] [[src:book-seemann]]')
    B(C, S_, 3, 'kt', '{ "id": "b42", "doctorName": "BS. An" }                                 ← /v1 hôm qua\n{ "id": "b42", "doctorName": "BS. An",\n  "doctor": { "name": "BS. An", "specialty": "Da liễu" } }          ← thêm vào: bản cũ bỏ qua "doctor"\n{ "id": "b42", "doctor": { "name": "BS. An" } }                     ← đổi tên: bản cũ thiếu doctorName, lỗi',
      '{ "id": "b42", "doctorName": "Dr. An" }                                 ← /v1 yesterday\n{ "id": "b42", "doctorName": "Dr. An",\n  "doctor": { "name": "Dr. An", "specialty": "Dermatology" } }    ← additive: old apps ignore "doctor"\n{ "id": "b42", "doctor": { "name": "Dr. An" } }                      ← rename: old apps miss doctorName, fail')

    S_ = 'bugs'
    a(C + '.sec.%s.title' % S_, 'Hai lỗi hay gặp', 'Two common bugs')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'bug', 'Backend thêm một trường "notes" vào response; ngay sau đó một phần người dùng không mở được màn lịch hẹn.', 'Backend adds a "notes" field to the response; right after, some users cannot open the bookings screen.')
    B(C, S_, 1, 'cause', 'Những bản app cũ dùng Json mặc định: khóa lạ là lỗi giải mã. Thay đổi "chỉ thêm vào" vẫn phá app không bỏ qua khóa lạ.', 'Older app versions use the default Json: unknown keys are decoding errors. An "additive only" change still breaks apps that do not ignore unknown keys.')
    B(C, S_, 1, 'fix', 'Ngắn hạn: backend bỏ trường mới hay chỉ trả khi client đủ mới. Dài hạn: mọi bản app đặt ignoreUnknownKeys = true và có kiểm tra phiên bản tối thiểu. [[src:kx-json-config]]', 'Short term: backend drops the new field or sends it only to new enough clients. Long term: every app version sets ignoreUnknownKeys = true and has a minimum-version check. [[src:kx-json-config]]')
    B(C, S_, 2, 'bug', 'Đã tạm dừng phát hành bản lỗi, nhưng số crash vẫn không giảm trong nhiều ngày.', 'The bad release was halted, yet crashes do not drop for days.')
    B(C, S_, 2, 'cause', 'Tạm dừng chỉ ngăn người mới nhận bản đó; những máy đã cài vẫn chạy nó.', 'Halting only stops new users from getting it; devices that installed it still run it.')
    B(C, S_, 2, 'fix', 'Phát hành nhanh một bản sửa có versionCode (số phiên bản nội bộ Play dùng để biết bản nào mới hơn) cao hơn; lần sau giấu tính năng mới sau cờ để tắt được ngay trên máy đã cài. [[src:play-staged-rollout]]', 'Ship a fix with a higher versionCode (the internal version number Play uses to tell which build is newer) quickly; next time hide new features behind a flag so they can be switched off on installed devices. [[src:play-staged-rollout]]')

    S_ = 'ex'
    a(C + '.sec.%s.title' % S_, 'Bài tập', 'Exercise')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'ex', 'Bạn sắp làm lại màn thanh toán viện phí (thay cả API). Lên kế hoạch phát hành: (a) app cần có sẵn những cơ chế gì trước đó; (b) API đổi thế nào để bản cũ vẫn chạy; (c) mỗi bước tăng phần trăm dựa trên chỉ số gì; (d) khi nào được xóa API cũ và cờ.',
      'You are about to rebuild the hospital bill payment screen (replacing its API too). Plan the release: (a) what mechanisms the app must already have; (b) how the API changes so old versions keep working; (c) which metrics gate each percentage step; (d) when the old API and the flag may be removed.')
    B(C, S_, 1, 'hint', 'Nghĩ tới những gì không đổi được sau khi phát hành.', 'Think about what cannot change after release.')
    B(C, S_, 1, 'sol', '(a) Cờ do server điều khiển với mặc định tắt; ignoreUnknownKeys; kiểm tra phiên bản tối thiểu. (b) Mở API thanh toán mới song song (/v2), giữ /v1 cho bản cũ. (c) Tỉ lệ crash và ANR của nhóm bật cờ so với nhóm không bật, tỉ lệ thanh toán thành công, lỗi từ server; chỉ tăng khi không tệ hơn nhóm cũ. (d) Khi cờ đã 100% đủ lâu và số người dùng còn gọi /v1 đủ nhỏ để bắt cập nhật (immediate) là chấp nhận được; rồi xóa cờ và mã cũ ở bản kế.',
      '(a) A server-controlled flag defaulting to off; ignoreUnknownKeys; a minimum-version check. (b) Open the new payment API alongside (/v2), keeping /v1 for old versions. (c) Crash and ANR rates of the flagged group versus the rest, payment success rate, server errors; raise only when no worse than the old group. (d) Once the flag has been at 100% long enough and the users still calling /v1 are few enough that forcing an (immediate) update is acceptable; then remove the flag and old code in the next version.')

    for q, qv, qe, av, ae, wv, we in [
        ('q1', 'Tạm dừng một bản phát hành theo phần trăm có gỡ nó khỏi máy đã cài không?', 'Does halting a staged rollout remove it from devices that installed it?', 'Không. Chỉ ngăn người mới nhận; muốn thay phải phát hành bản mới hơn.', 'No. It only stops new users getting it; replacing it needs a newer release.', 'Feature flag thì tắt được trên máy đã cài.', 'A feature flag can switch it off on installed devices.'),
        ('q2', 'Vì sao thêm một trường vào response vẫn có thể làm app cũ lỗi?', 'Why can adding a response field still break old apps?', 'Nếu app cũ giải mã chặt, khóa lạ là lỗi (mặc định của kotlinx.serialization).', 'If the old app decodes strictly, unknown keys are errors (kotlinx.serialization\'s default).', 'Đặt ignoreUnknownKeys = true từ bản đầu.', 'Set ignoreUnknownKeys = true from the first version.'),
        ('q3', 'Ngưỡng tỉ lệ người dùng gặp crash của Android vitals là bao nhiêu?', 'What is Android vitals\' user-perceived crash rate threshold?', '1,09% trên toàn bộ (ANR: 0,47%); 8% trên một mẫu điện thoại.', '1.09% overall (ANR: 0.47%); 8% on a single phone model.', 'Vượt ngưỡng thì Play có thể giảm hiển thị app.', 'Exceeding it may reduce Play visibility.'),
        ('q4', 'Thay đổi API phá vỡ nên đặt ở đâu khi app cũ còn nhiều người dùng?', 'Where should a breaking API change go while old apps still have many users?', 'Ở phiên bản API mới (/v2), giữ phiên bản cũ cho app cũ.', 'In a new API version (/v2), keeping the old one for old apps.', 'Cái giá là server giữ hai phiên bản.', 'The price is the server maintaining two versions.')]:
        a(C + '.quiz.%s.q' % q, qv, qe); a(C + '.quiz.%s.a' % q, av, ae); a(C + '.quiz.%s.why' % q, wv, we)
