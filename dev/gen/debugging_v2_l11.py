# Gỡ lỗi và hiệu năng · l11: mạng và pin (Phần 3: lỗi trên máy người dùng)
# Nguồn (chỉ ghi ở đây và docs/research/debugging.md), đọc 2026-11-25, trang không ghi ngày: developer.android.com/studio/debug/network-profiler
# (dòng thời gian dữ liệu gửi nhận; mỗi request có kích thước, loại, trạng thái, thời gian; Thread View cho biết luồng nào gửi; header, body, call stack;
# chỉ hỗ trợ HttpsURLConnection và OkHttp, Retrofit dùng OkHttp; Rules sửa phản hồi để thử), training/efficient-downloads/efficient-network-access
# (radio 3G điển hình: toàn công suất, công suất thấp tiết kiệm khoảng 50 %, chờ; mỗi kết nối mới đưa radio lên toàn công suất; 5 giây đuôi rồi 12 giây
# công suất thấp; mỗi phiên tốn ít nhất khoảng 18 giây; gom request; tải trước mỗi 2–5 phút, 1–5 MB; WorkManager khi sạc và Wi-Fi), topic/performance/
# vitals/wakelock (wake lock cục bộ cộng lại từ 2 giờ trong 24 giờ là quá mức, khi app ở nền hay chạy foreground service; quá 5 % phiên trong 28 ngày ảnh
# hưởng hiển thị trên Play), develop/connectivity/network-ops/managing (tải dữ liệu lớn khi có Wi-Fi). Ba request, 1,2 MB và thời điểm là của site.

SEC_ORDER = {'l11': ['hook', 'inspector', 'radio', 'dup', 'battery', 'bugs', 'ex', 'recall']}


def add(a):
    def B(ch, sec, n, field, vi, en=None):
        a('%s.sec.%s.b.%02d.%s' % (ch, sec, n, field), vi, vi if en is None else en)

    a('preset.net', '''Gỡ lỗi · request trùng và radio tốn pin''', '''Debugging · duplicate requests and a battery-hungry radio''')
    m = lambda k, vi, en=None: a('m.net.' + k, vi, en)
    m('title', '''Mỗi lần mở màn, cùng một API bị gọi ba lần''', '''Every time the screen opens, the same API is called three times''')
    m('overview', '''Người dùng báo app Hẹn Khám hao pin và tốn dữ liệu. Network Inspector cho thấy mỗi lần mở màn lịch hẹn, GET /bookings được gọi ba lần, mỗi lần 1,2 MB. Cách 1 giữ nguyên ba request. Cách 2 dùng một nguồn dữ liệu chung và chỉ tải trang đầu. Ta đếm số request, lượng dữ liệu, và thời gian radio ở mức toàn công suất, theo mô hình radio của tài liệu Android.''',
      '''Users report that ClinicBook drains the battery and uses a lot of data. Network Inspector shows that every time the bookings screen opens, GET /bookings is called three times, 1.2 MB each. Way 1 keeps the three requests. Way 2 uses one shared data source and loads only the first page. We count requests, data, and the time the radio spends at full power, using the radio model from Android\'s documentation.''')
    m('wrapup', '''Ba request cách nhau vài giây giữ radio ở toàn công suất 13 giây cho mỗi lần mở màn, và tải 3,6 MB dù màn chỉ hiện 10 lịch. Một request chung, chỉ tải trang đầu 120 KB, đưa thời gian toàn công suất xuống 6 giây và dữ liệu xuống còn 1/30. Network Inspector chỉ ra request nào, ai gọi, to bao nhiêu; mô hình radio giải thích vì sao gom request lại tiết kiệm pin.''',
      '''Three requests a few seconds apart keep the radio at full power for 13 seconds per screen open, and download 3.6 MB although the screen shows 10 bookings. One shared request loading only the first page, 120 KB, brings full-power time down to 6 seconds and data to a thirtieth. Network Inspector shows which request, who called it and how big it is; the radio model explains why batching requests saves battery.''')
    m('simp.1', '''Mô hình radio là của mạng 3G điển hình trong tài liệu (5 giây đuôi, 12 giây công suất thấp); mạng 4G, 5G có thời gian khác nhưng cùng ý: mỗi phiên truyền kéo theo một khoảng radio thức.''',
      '''The radio model is the typical 3G network from the documentation (5 seconds of tail, 12 seconds of low power); 4G and 5G have other timings but the same idea: each transfer session drags a period of radio wake-time behind it.''')
    m('simp.2', '''Thời gian radio ở toàn công suất và công suất thấp được tính thật bằng JavaScript từ thời điểm và độ dài từng request, theo luật: toàn công suất khi truyền và 5 giây sau đó, rồi 12 giây công suất thấp.''',
      '''Time at full and low power is really computed in JavaScript from each request\'s start and duration, by the rule: full power while transferring and for 5 seconds after, then 12 seconds of low power.''')
    m('ctl.hint', '''Chọn cách tải rồi đi qua bốn bước; xem dải trạng thái radio dưới các request.''', '''Pick a loading approach and walk the four steps; watch the radio state strip under the requests.''')
    m('ctl.case', '''Cách tải dữ liệu''', '''How data is loaded''')
    m('ctl.case.dup', '''ba nơi tự gọi API''', '''three places call the API themselves'''); m('ctl.case.shared', '''một nguồn chung, chỉ trang đầu''', '''one shared source, first page only''')
    m('diagramTitle', '''Từ màn hình tới radio''', '''From the screen to the radio''')
    m('diagramDesc', '''Các thành phần gọi API; mỗi request đánh thức radio; radio thức thêm một lúc sau khi truyền xong''', '''Components call the API; each request wakes the radio; the radio stays awake for a while after the transfer''')
    for k, vi, en in [('ui', 'Màn lịch hẹn (3 thành phần)', 'Bookings screen (3 components)'), ('repo', 'Nguồn dữ liệu', 'Data source'), ('http', 'OkHttp (client HTTP)', 'OkHttp (HTTP client)'),
                      ('radio', 'Radio di động', 'Mobile radio'), ('ni', 'Network Inspector (xem mạng)', 'Network Inspector (network)')]:
        m('n.' + k, vi, en)
    m('met.req', '''Request mỗi lần mở''', '''Requests per open'''); m('met.kb', '''Dữ liệu tải (KB)''', '''Data downloaded (KB)''')
    m('met.high', '''Radio toàn công suất (giây)''', '''Radio at full power (s)'''); m('met.low', '''Radio công suất thấp (giây)''', '''Radio at low power (s)''')
    a('cap.net', '''Các thành phần gọi API qua OkHttp; mỗi request đưa radio lên toàn công suất. Ô đỏ: request trùng hay phản hồi quá lớn.''', '''Components call the API through OkHttp; each request takes the radio to full power. A red box: a duplicate request or an oversized response.''')
    S = [
        ('dup', 's1', 'Network Inspector: ba GET /bookings trong 8 giây', 'Network Inspector: three GET /bookings in 8 seconds',
         'Mở màn lịch hẹn một lần, dòng thời gian của Network Inspector có ba request giống hệt nhau tới GET /bookings, ở giây 0, 2 và 7. Mỗi request trả 1,2 MB, mất khoảng 1 giây.',
         'Open the bookings screen once, and Network Inspector\'s timeline shows three identical GET /bookings requests, at seconds 0, 2 and 7. Each returns 1.2 MB and takes about 1 second.'),
        ('dup', 's2', 'Call stack: ba người gọi khác nhau', 'Call stacks: three different callers',
         'Mở từng request, xem call stack: một từ BookingsViewModel.init, một từ BadgeWidget.onAttach (huy hiệu số lịch), một từ BookingsFragment.onResume (làm mới khi quay lại). Ba nơi tự gọi API, không ai biết nơi kia đã có dữ liệu.',
         'Open each request and look at its call stack: one from BookingsViewModel.init, one from BadgeWidget.onAttach (the booking count badge), one from BookingsFragment.onResume (refreshing on return). Three places call the API themselves, none aware the others already have the data.'),
        ('dup', 's3', 'Radio: 13 giây toàn công suất cho một lần mở', 'The radio: 13 seconds at full power for one open',
         'Mỗi request đưa radio lên toàn công suất, và radio ở đó thêm 5 giây sau khi truyền xong, rồi 12 giây công suất thấp. Ba request ở giây 0, 2, 7 nối các khoảng đó lại: radio ở toàn công suất từ giây 0 tới 13, công suất thấp tới giây 25.',
         'Each request takes the radio to full power, where it stays for 5 seconds after the transfer, then 12 seconds at low power. Three requests at seconds 0, 2 and 7 chain those periods together: full power from second 0 to 13, low power until second 25.'),
        ('dup', 's4', 'Phản hồi 1,2 MB cho 10 dòng trên màn', 'A 1.2 MB response for 10 rows on screen',
         'Body của phản hồi là toàn bộ lịch sử khám từ năm 2019, kèm ghi chú dài. Màn hình chỉ hiện 10 lịch sắp tới. Mỗi lần mở tải 3,6 MB, gần hết là dữ liệu không dùng.',
         'The response body is the whole visit history since 2019, with long notes. The screen shows only the 10 upcoming bookings. Each open downloads 3.6 MB, almost all of it unused.'),
        ('shared', 's1', 'Một nguồn dữ liệu chung: một request', 'One shared data source: one request',
         'BookingRepository giữ lịch hẹn trong một StateFlow; ViewModel, huy hiệu và màn khi quay lại đều đọc từ đó. Mở màn chỉ còn một GET /bookings.',
         'BookingRepository keeps bookings in a StateFlow; the ViewModel, the badge and the screen on return all read from it. Opening the screen now makes a single GET /bookings.'),
        ('shared', 's2', 'Call stack: chỉ BookingRepository gọi mạng', 'Call stack: only BookingRepository calls the network',
         'Request duy nhất đến từ BookingRepository.refresh. Quay lại màn trong vòng vài phút thì dùng dữ liệu đang có, không gọi lại.',
         'The only request comes from BookingRepository.refresh. Returning to the screen within a few minutes reuses the data at hand, with no new call.'),
        ('shared', 's3', 'Radio: 6 giây toàn công suất', 'The radio: 6 seconds at full power',
         'Một request 1 giây: toàn công suất từ giây 0 tới 6, công suất thấp tới 18, rồi về chờ. So với cách cũ, bớt 7 giây toàn công suất cho mỗi lần mở.',
         'One 1-second request: full power from second 0 to 6, low power until 18, then standby. Compared with before, 7 fewer seconds at full power per open.'),
        ('shared', 's4', 'Chỉ tải trang đầu: 120 KB', 'Load only the first page: 120 KB',
         'API nhận tham số trang và chỉ trả các trường màn cần: 10 lịch sắp tới, 120 KB. Lịch sử cũ tải khi người dùng cuộn tới. Dữ liệu mỗi lần mở giảm từ 3.600 KB xuống 120 KB.',
         'The API takes a page parameter and returns only the fields the screen needs: the 10 upcoming bookings, 120 KB. Older history loads when the user scrolls to it. Data per open drops from 3,600 KB to 120 KB.'),
    ]
    for case, k, tv, te, xv, xe in S:
        sid = case + '.' + k
        m('s.%s.title' % sid, tv, te); m('s.%s.explain' % sid, xv, xe); m('ev.' + sid, tv, te)
    for k, vi, en in [
        ('try', '''Mẹo đọc: hàng trên là các request theo thời gian (rộng theo thời lượng truyền); dải dưới là trạng thái radio: đỏ là toàn công suất, vàng là công suất thấp. Bảng liệt kê từng request, người gọi và kích thước.''',
         '''Reading tip: the top row is requests over time (as wide as the transfer); the strip below is the radio state: red is full power, amber is low power. The table lists each request, its caller and size.'''),
        ('dup.s2', '''Network Inspector cho xem header, body và call stack của mỗi request; Thread View cho biết luồng nào gửi request đó. [[src:ad-network-inspector]]''',
         '''Network Inspector shows each request\'s headers, body and call stack; Thread View tells which thread sent it. [[src:ad-network-inspector]]'''),
        ('dup.s3', '''Mỗi kết nối mới đưa radio lên toàn công suất; sau khi truyền xong, radio ở toàn công suất thêm 5 giây rồi công suất thấp thêm 12 giây (mô hình 3G điển hình). [[src:ad-efficient-network]]''',
         '''Every new connection takes the radio to full power; after the transfer it stays at full power for 5 more seconds, then 12 at low power (the typical 3G model). [[src:ad-efficient-network]]'''),
        ('dup.s4', '''Chỉ tải dữ liệu lớn khi có Wi-Fi là một chiến lược thường dùng: mạng di động thường bị đo lưu lượng và tốn tiền. [[src:ad-network-managing]]''',
         '''Only fetching large data on Wi-Fi is a common strategy: mobile data is often metered and can get expensive. [[src:ad-network-managing]]'''),
        ('shared.s1', '''Cùng một dữ liệu có một nguồn duy nhất là cách chống request trùng tận gốc; đây là ý "một nguồn sự thật" ở chương "Các tầng, hướng phụ thuộc, SSOT và UDF" của track Kiến trúc app Android.''',
         '''One source for the same data stops duplicate requests at the root; this is the "single source of truth" idea in "Layers, dependency direction, SSOT and UDF" in the Android App Architecture track.'''),
        ('shared.s2', '''HttpsURLConnection và hầu hết client HTTP như OkHttp mặc định dùng lại kết nối (connection pooling), nhưng mỗi phiên truyền vẫn đánh thức radio. [[src:ad-efficient-network]]''',
         '''HttpsURLConnection and most HTTP clients such as OkHttp pool connections by default, but each transfer session still wakes the radio. [[src:ad-efficient-network]]'''),
        ('shared.s3', '''Gom các lần truyền: một lần truyền 3 giây mỗi phút giữ radio thức khoảng 20 giây và để 40 giây chờ, trong khi ba lần 1 giây rải đều có thể giữ radio thức suốt. [[src:ad-efficient-network]]''',
         '''Bundle transfers: one 3-second transfer per minute keeps the radio awake for about 20 seconds and leaves 40 in standby, whereas three 1-second transfers spread out can keep it awake the whole time. [[src:ad-efficient-network]]'''),
        ('shared.s4', '''Tải dữ liệu lớn có thể hoãn tới khi máy đang sạc và có Wi-Fi bằng WorkManager, như ràng buộc ở chương "Dữ liệu và việc nền: Database Inspector, Background Task Inspector". [[src:ad-efficient-network]]''',
         '''Large downloads can be deferred until the device is charging and on Wi-Fi with WorkManager, using constraints as in "Data and background work: Database Inspector, Background Task Inspector". [[src:ad-efficient-network]]'''),
    ]:
        m('co.' + k, vi, en)

    z = lambda k, vi, en=None: a('vz.' + k, vi, en)
    z('tab.net', '''Request và trạng thái radio''', '''Requests and radio state''')
    z('nt.aria', '''{n} request; radio toàn công suất {h} giây, công suất thấp {l} giây''', '''{n} requests; radio at full power {h} s, low power {l} s''')
    z('nt.lane.req', '''request''', '''requests'''); z('nt.lane.radio', '''trạng thái radio''', '''radio state'''); z('nt.axis', '''giây 0 → 30''', '''second 0 → 30''')
    for k, vi, en in [('t', 'Giây', 'Second'), ('req', 'Yêu cầu', 'Request'), ('caller', 'Người gọi (call stack)', 'Caller (call stack)'), ('size', 'Kích thước', 'Size')]:
        z('nt.col.' + k, vi, en)
    z('nt.sub', '''{n} request, {kb} KB; radio toàn công suất {h} giây, công suất thấp {l} giây.''', '''{n} requests, {kb} KB; radio at full power {h} s, low power {l} s.''')
    z('nt.hidden', '''(mở call stack ở bước 2)''', '''(call stacks open at step 2)''')
    z('nt.legend', '''Dải radio: đỏ là toàn công suất, vàng là công suất thấp, trống là chờ. Hàng đỏ trong bảng: request trùng hay phản hồi quá lớn.''',
      '''Radio strip: red is full power, amber is low power, blank is standby. A red table row: a duplicate request or an oversized response.''')

    C = 'l11'
    a(C + '.title', '''Mạng và pin''', '''Network and battery''')
    a(C + '.essence', '''Mỗi lần app gửi request, radio di động lên mức toàn công suất, và ở đó thêm vài giây sau khi truyền xong rồi mới hạ dần. Nhiều request nhỏ rải rác giữ radio thức gần như liên tục; gom lại thành ít lần thì radio được nghỉ lâu hơn.\nNetwork Inspector trả lời: request nào được gửi, khi nào, to bao nhiêu, và ai gọi (call stack). Request trùng thường đến từ nhiều nơi tự gọi cùng một API; cách chữa tận gốc là một nguồn dữ liệu chung.\nPhản hồi to hơn những gì màn hình cần làm tốn dữ liệu và pin; chỉ tải trang đầu, tải dữ liệu lớn khi có Wi-Fi và đang sạc. Ngoài mạng, wake lock giữ máy thức quá lâu cũng làm hao pin và bị Android vitals theo dõi.''',
      '''Every time the app sends a request, the mobile radio goes to full power, stays there a few seconds after the transfer, and only then steps down. Many scattered small requests keep the radio awake almost constantly; batching them into fewer transfers lets it rest longer.\nNetwork Inspector answers: which requests were sent, when, how big, and who called them (the call stack). Duplicate requests usually come from several places calling the same API themselves; the root fix is one shared data source.\nResponses bigger than the screen needs waste data and battery; load only the first page, and large data on Wi-Fi while charging. Beyond the network, wake locks keeping the device awake too long also drain the battery and are tracked by Android vitals.''')
    a(C + '.goal.g1', '''Đã thấy ba request trùng và người gọi''', '''Saw the three duplicate requests and their callers''')
    a(C + '.goal.g2', '''Đã thấy radio và dữ liệu giảm''', '''Saw radio time and data drop''')
    a(C + '.sim.debugging.net', '''ba nơi tự gọi API, hay một nguồn chung''', '''three places calling the API, or one shared source''')

    S_ = 'hook'
    a(C + '.sec.%s.title' % S_, '''Đoán trước khi đọc''', '''Predict before reading''')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'predict', '''Ba request, mỗi cái truyền 1 giây, ở giây 0, 2 và 7. Theo mô hình radio của tài liệu (toàn công suất khi truyền và 5 giây sau đó), radio ở toàn công suất tổng cộng bao lâu: 3 giây hay lâu hơn?''',
      '''Three requests, each transferring for 1 second, at seconds 0, 2 and 7. By the documentation\'s radio model (full power while transferring and for 5 seconds after), how long is the radio at full power in total: 3 seconds, or longer?''')
    B(C, S_, 1, 'ans', '''13 giây: mỗi request kéo thêm 5 giây đuôi, và ba khoảng nối liền nhau từ giây 0 tới 13. Một request duy nhất chỉ tốn 6 giây. Mô phỏng ngay dưới tìm ra ba request trùng bằng Network Inspector và tính lại radio.''',
      '''13 seconds: each request drags 5 seconds of tail behind it, and the three periods join up from second 0 to 13. A single request costs only 6 seconds. The simulation just below finds the three duplicates with Network Inspector and recomputes the radio time.''')

    S_ = 'inspector'
    a(C + '.sec.%s.title' % S_, '''Network Inspector cho thấy gì''', '''What Network Inspector shows''')
    a(C + '.sec.%s.badge' % S_, 'version')
    B(C, S_, 1, 'p', '''Network Inspector hiện hoạt động mạng của app theo thời gian thực trên một dòng thời gian dữ liệu gửi và nhận. Với mỗi request: kích thước, loại, mã trạng thái, thời gian truyền; header và body của request lẫn phản hồi; call stack của nơi gửi; và theo luồng, luồng nào gửi request nào. Nó hỗ trợ HttpsURLConnection và OkHttp (nên cả Retrofit, vốn dùng OkHttp). Tính năng Rules cho phép sửa mã trạng thái, header hay body của phản hồi để thử app với phản hồi lạ mà không cần đổi máy chủ. [[src:ad-network-inspector]]''',
      '''Network Inspector shows the app\'s network activity in real time on a timeline of data sent and received. For each request: size, type, status code, transfer time; request and response headers and bodies; the sender\'s call stack; and by thread, which thread sent which request. It supports HttpsURLConnection and OkHttp (and so Retrofit, which uses OkHttp). The Rules feature lets you change a response\'s status code, headers or body to test the app against odd responses without touching the server. [[src:ad-network-inspector]]''')
    B(C, S_, 2, 'p', '''Câu hỏi khi xem: có request nào trùng (cùng URL, cùng lúc), ai gọi chúng (call stack), phản hồi có to hơn những gì màn hình dùng không, và request có rải rác hay gom lại. Network Inspector chỉ thấy app của bạn; muốn biết radio tốn bao nhiêu thì nghĩ theo mô hình ở mục sau.''',
      '''Questions while looking: are there duplicates (same URL, close in time), who calls them (the call stack), is the response bigger than what the screen uses, are requests scattered or batched. Network Inspector sees only your app; to reason about radio cost, think with the model in the next section.''')

    S_ = 'radio'
    a(C + '.sec.%s.title' % S_, '''Vì sao request rải rác tốn pin''', '''Why scattered requests drain the battery''')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'p', '''Radio di động có các mức: toàn công suất, công suất thấp (tiết kiệm khoảng một nửa), và chờ. Mỗi kết nối mới đưa radio lên toàn công suất; quay lên từ mức thấp mất khoảng 1,5 giây, từ chờ hơn 2 giây. Trong mô hình 3G điển hình của tài liệu, sau khi truyền xong radio ở toàn công suất thêm 5 giây, rồi công suất thấp thêm 12 giây: mỗi phiên truyền làm radio tốn năng lượng ít nhất khoảng 18 giây. [[src:ad-efficient-network]]''',
      '''The mobile radio has levels: full power, low power (saving about half), and standby. Each new connection takes the radio to full power; climbing back from low takes about 1.5 seconds, from standby over 2. In the documentation\'s typical 3G model, after a transfer the radio stays at full power for 5 more seconds, then at low power for 12: every transfer session costs radio energy for at least about 18 seconds. [[src:ad-efficient-network]]''')
    B(C, S_, 2, 'p', '''Vì vậy cách tiết kiệm là gom: ít phiên truyền dài hơn thay vì nhiều phiên ngắn. Tài liệu gợi ý tải trước sao cho chỉ cần tải lại mỗi 2 tới 5 phút, mỗi lần cỡ 1 tới 5 MB, và hoãn việc tải lớn bằng WorkManager tới khi máy đang sạc và có Wi-Fi. Tìm sóng di động cũng là một việc rất tốn pin, nên kiểm tra kết nối trước khi gửi. Các kiểu kênh giao tiếp và cache HTTP được nói kỹ ở chương "Chọn kênh giao tiếp" và "Cache: RAM, đĩa và HTTP" của track Thiết kế hệ thống phía mobile. [[src:ad-efficient-network]]''',
      '''So the saving comes from batching: fewer, longer sessions instead of many short ones. The documentation suggests prefetching so that you only need to download again every 2 to 5 minutes, about 1 to 5 MB each time, and deferring large downloads with WorkManager until the device is charging and on Wi-Fi. Searching for a cell signal is also very power-hungry, so check connectivity before sending. Communication channels and HTTP caching are covered in "Choosing a channel" and "Caching: memory, disk and HTTP" in the Mobile System Design track. [[src:ad-efficient-network]]''')

    S_ = 'dup'
    a(C + '.sec.%s.title' % S_, '''Request trùng và phản hồi quá lớn''', '''Duplicate requests and oversized responses''')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'p', '''Request trùng hiếm khi do một dòng mã sai; thường là nhiều thành phần cùng cần một dữ liệu và mỗi cái tự gọi API: ViewModel khi tạo, một widget khi gắn vào, màn hình khi quay lại. Sửa tận gốc bằng một nguồn dữ liệu chung giữ kết quả (ví dụ StateFlow trong repository), các nơi khác chỉ đọc. Phản hồi quá lớn sửa ở cả hai phía: API cho phân trang và chọn trường, app chỉ xin những gì màn hình dùng.''',
      '''Duplicate requests rarely come from one wrong line; usually several components need the same data and each calls the API itself: the ViewModel on creation, a widget on attach, the screen on return. The root fix is one shared data source holding the result (a StateFlow in a repository, for example) that the others only read. Oversized responses are fixed on both sides: the API offers paging and field selection, and the app asks only for what the screen uses.''')
    B(C, S_, 2, 'kt', '''class BookingRepository(private val api: BookingApi, private val scope: CoroutineScope) {
    private val _bookings = MutableStateFlow<List<Booking>>(emptyList())
    val bookings: StateFlow<List<Booking>> = _bookings       // ViewModel, huy hiệu, màn hình đều đọc ở đây
    private var lastLoad = 0L
    suspend fun refresh(now: Long) {
        if (now - lastLoad < 5 * 60_000) return                // dữ liệu còn mới: không gọi lại
        _bookings.value = api.upcoming(page = 0, size = 10)    // chỉ trang đầu
        lastLoad = now
    }
}''', '''class BookingRepository(private val api: BookingApi, private val scope: CoroutineScope) {
    private val _bookings = MutableStateFlow<List<Booking>>(emptyList())
    val bookings: StateFlow<List<Booking>> = _bookings       // the ViewModel, the badge and the screen all read here
    private var lastLoad = 0L
    suspend fun refresh(now: Long) {
        if (now - lastLoad < 5 * 60_000) return                // data still fresh: no new call
        _bookings.value = api.upcoming(page = 0, size = 10)    // first page only
        lastLoad = now
    }
}''')

    S_ = 'battery'
    a(C + '.sec.%s.title' % S_, '''Ngoài mạng: wake lock''', '''Beyond the network: wake locks''')
    a(C + '.sec.%s.badge' % S_, 'version')
    B(C, S_, 1, 'p', '''Wake lock giữ CPU thức để làm việc; giữ quá lâu thì máy không vào được các trạng thái tiết kiệm. Android vitals coi là quá mức khi tổng mọi wake lock cục bộ của app vượt 2 giờ trong 24 giờ, tính khi app ở nền hay chạy foreground service; wake lock của âm thanh, vị trí và job do người dùng khởi động được miễn. Nếu tình trạng này xảy ra ở hơn 5 % phiên trong 28 ngày, app có thể bị giảm hiển thị trên Play. Background Task Inspector (chương "Dữ liệu và việc nền: Database Inspector, Background Task Inspector") liệt kê wake lock, job và alarm của app. [[src:ad-wakelock]] [[src:ad-task-inspector]]''',
      '''A wake lock keeps the CPU awake to do work; holding one too long stops the device from entering power-saving states. Android vitals counts it as excessive when all of an app\'s partial wake locks together exceed 2 hours in 24 hours, counted while the app is in the background or running a foreground service; audio, location and user-initiated job wake locks are exempt. If this happens in more than 5% of sessions over 28 days, the app\'s visibility on Play may be affected. Background Task Inspector (the chapter "Data and background work: Database Inspector, Background Task Inspector") lists the app\'s wake locks, jobs and alarms. [[src:ad-wakelock]] [[src:ad-task-inspector]]''')

    S_ = 'bugs'
    a(C + '.sec.%s.title' % S_, '''Hai lỗi hay gặp''', '''Two common bugs''')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'bug', '''Một vòng hỏi máy chủ mỗi 30 giây để cập nhật số lượt còn lại; pin tụt nhanh dù màn hình tắt.''', '''A loop polls the server every 30 seconds to update the remaining visits; the battery drains fast even with the screen off.''')
    B(C, S_, 1, 'cause', '''Mỗi lần hỏi là một phiên truyền kéo theo khoảng 18 giây radio thức; 30 giây một lần giữ radio thức hơn nửa thời gian.''', '''Each poll is a transfer session dragging about 18 seconds of radio wake-time; every 30 seconds keeps the radio awake more than half the time.''')
    B(C, S_, 1, 'fix', '''Dừng hỏi khi màn hình không hiện; nhận thông báo đẩy từ máy chủ khi số lượt đổi, hay gom việc cập nhật vào lần đồng bộ định kỳ.''', '''Stop polling when the screen is not visible; receive a push from the server when the count changes, or fold the update into the periodic sync.''')
    B(C, S_, 2, 'bug', '''Bản thử nghiệm dùng Network Inspector không thấy request nào của thư viện thanh toán.''', '''Testing with Network Inspector shows no requests from the payment library.''')
    B(C, S_, 2, 'cause', '''Thư viện dùng một client HTTP khác, không phải HttpsURLConnection hay OkHttp, nên Network Inspector không ghi lại được.''', '''The library uses a different HTTP client, neither HttpsURLConnection nor OkHttp, so Network Inspector cannot record it.''')
    B(C, S_, 2, 'fix', '''Biết giới hạn của công cụ: kiểm phía máy chủ hay dùng proxy gỡ lỗi cho những request đó.''', '''Know the tool\'s limits: check on the server side or use a debugging proxy for those requests.''')

    S_ = 'ex'
    a(C + '.sec.%s.title' % S_, '''Bài tập''', '''Exercise''')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'ex', '''Theo mô hình trong chương (toàn công suất khi truyền và 5 giây sau, rồi 12 giây công suất thấp), so hai cách trong một phút: (a) ba request 1 giây ở giây 0, 20, 40; (b) một request 3 giây ở giây 0. Mỗi cách để radio ở toàn công suất bao lâu?''',
      '''By the chapter\'s model (full power while transferring and 5 seconds after, then 12 seconds of low power), compare two approaches within a minute: (a) three 1-second requests at seconds 0, 20 and 40; (b) one 3-second request at second 0. How long does each keep the radio at full power?''')
    B(C, S_, 1, 'hint', '''Mỗi request: thời lượng truyền + 5 giây; các khoảng không chạm nhau thì cộng lại.''', '''Each request: transfer time + 5 seconds; periods that do not touch add up.''')
    B(C, S_, 1, 'sol', '''(a) 3 × (1 + 5) = 18 giây toàn công suất, cộng 3 × 12 = 36 giây công suất thấp: radio gần như không được nghỉ. (b) 3 + 5 = 8 giây toàn công suất, 12 giây công suất thấp, còn 40 giây chờ. Gom lại tiết kiệm rõ rệt.''',
      '''(a) 3 × (1 + 5) = 18 seconds at full power, plus 3 × 12 = 36 at low power: the radio barely rests. (b) 3 + 5 = 8 seconds at full power, 12 at low power, leaving 40 seconds of standby. Batching saves a lot.''')

    S_ = 'recall'
    a(C + '.sec.%s.title' % S_, '''Tự trả lời''', '''Answer it yourself''')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'ask', '''Vì sao ba request 1 giây có thể tốn pin hơn một request 3 giây?''', '''Why can three 1-second requests cost more battery than one 3-second request?''')
    B(C, S_, 1, 'ans', '''Mỗi phiên truyền kéo theo vài giây radio ở toàn công suất và một quãng công suất thấp; nhiều phiên rải rác giữ radio thức lâu hơn nhiều.''', '''Each transfer session drags seconds of full-power radio and a stretch of low power behind it; scattered sessions keep the radio awake much longer.''')
    B(C, S_, 2, 'ask', '''Network Inspector cho biết gì để tìm request trùng?''', '''What does Network Inspector tell you to find duplicate requests?''')
    B(C, S_, 2, 'ans', '''URL, thời điểm, kích thước của từng request, và call stack của nơi gọi.''', '''Each request\'s URL, time, size, and the caller\'s call stack.''')

    for q, qv, qe, av, ae, wv, we in [
        ('q1', 'Network Inspector hỗ trợ những thư viện mạng nào?', 'Which networking libraries does Network Inspector support?', 'HttpsURLConnection và OkHttp (nên cả Retrofit).', 'HttpsURLConnection and OkHttp (and so Retrofit).',
         'Client khác thì không được ghi lại.', 'Other clients are not recorded.'),
        ('q2', 'Sửa request trùng tận gốc bằng gì?', 'What fixes duplicate requests at the root?', 'Một nguồn dữ liệu chung mà các nơi khác chỉ đọc.', 'One shared data source that the others only read.',
         'Mỗi nơi tự gọi API thì không ai biết nơi kia đã có dữ liệu.', 'When each place calls the API itself, none knows the others already have the data.'),
        ('q3', 'Android vitals coi wake lock là quá mức khi nào?', 'When does Android vitals consider wake locks excessive?', 'Khi tổng wake lock cục bộ vượt 2 giờ trong 24 giờ, lúc app ở nền hay chạy foreground service.', 'When the app\'s partial wake locks total more than 2 hours in 24, while in the background or running a foreground service.',
         'Âm thanh, vị trí và job do người dùng khởi động được miễn.', 'Audio, location and user-initiated jobs are exempt.')]:
        a(C + '.quiz.%s.q' % q, qv, qe); a(C + '.quiz.%s.a' % q, av, ae); a(C + '.quiz.%s.why' % q, wv, we)
