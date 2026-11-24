# Thiết kế hệ thống phía mobile · I1: từ đề bài tới kế hoạch (Phần 1)
# Nguồn: Tjeerd in 't Veen, Mobile System Design (early release) ch.2; Alex Xu, System Design Interview vol.1 ch.2–3 (đọc 2026-11-24).
# Phía client là diễn giải của site. Trần: 8 mục, mục cơ chế ≤ 4 khối.

SEC_ORDER = {'i1': ['hook', 'framework', 'secondary', 'backend', 'estimate', 'bugs', 'ex', 'honest']}


def add(a):
    def B(ch, sec, n, field, vi, en=None):
        a('%s.sec.%s.b.%02d.%s' % (ch, sec, n, field), vi, vi if en is None else en)

    a('preset.plan', 'Thiết kế hệ thống · từ đề bài tới kế hoạch', 'System design · from a brief to a plan')
    m = lambda k, vi, en=None: a('m.plan.' + k, vi, en)
    m('title', 'Làm theo bản thiết kế, hay hỏi trước rồi mới làm', 'Build from the mockup, or ask first and then build')
    m('overview', 'Đề bài: thêm màn nhắn tin với phòng khám vào app Hẹn Khám, gửi được chữ và ảnh. Designer gửi bản thiết kế đẹp. Hai cách bắt đầu: viết mã ngay theo bản thiết kế; hoặc hỏi designer ba câu và backend ba câu, rồi ước lượng nhanh dữ liệu ảnh trước khi viết mã.',
      'The brief: add a chat with the clinic to ClinicBook, sending text and photos. The designer sends a polished mockup. Two ways to start: code straight from the mockup; or ask the designer three questions and the backend three, then make a quick estimate of photo data before writing code.')
    m('wrapup', 'Bản thiết kế chỉ cho thấy trường hợp đẹp. Lỗi, nội dung xấu, mất mạng, hết phiên, mã lỗi và ngôn ngữ của thông báo đều là yêu cầu phụ: không hỏi trước thì chúng vẫn tới, chỉ là tới sau khi phát hành. Một ước lượng bằng số tròn cũng lộ ra yêu cầu phi chức năng mà màn hình không nói: gửi ảnh gốc tốn hơn mười lần dữ liệu so với ảnh đã thu nhỏ.',
      'A mockup only shows the best case. Errors, messy content, offline states, expired sessions, error codes and the language of notifications are all secondary requirements: if you do not ask first, they still arrive, just after release. An estimate with round numbers also reveals non-functional requirements the screen does not mention: sending original photos costs more than ten times the data of resized ones.')
    m('simp.1', 'Sáu câu hỏi là chọn lọc; một buổi thật có nhiều câu hơn. Số ảnh mỗi ngày và kích thước ảnh là giả định minh họa, làm tròn theo cách Alex Xu khuyên.', 'Six questions are a selection; a real session has more. Photos per day and photo sizes are illustrative assumptions, rounded the way Alex Xu advises.')
    m('simp.2', 'Các câu hỏi dựa trên Tjeerd in \'t Veen ch.2; câu về mất mạng và trạng thái rỗng là bổ sung của site. Khung và cách ước lượng theo Alex Xu tập 1 ch.2–3.', 'The questions are based on Tjeerd in \'t Veen ch.2; the offline and empty-state question is the site\'s addition. The framework and estimation follow Alex Xu vol. 1 ch.2–3.')
    m('ctl.hint', 'Đổi cách bắt đầu rồi đi lại; so cột "Yêu cầu rút ra" và số MB mỗi tháng ở bước cuối.', 'Switch the way you start and walk again; compare the "Requirement found" column and the MB per month at the last step.')
    m('ctl.case', 'Cách bắt đầu', 'How you start')
    for k, vi, en in [('mockup', 'viết mã ngay theo bản thiết kế', 'code straight from the mockup'), ('asked', 'hỏi designer và backend trước', 'ask the designer and backend first')]:
        m('ctl.case.' + k, vi, en)
    m('diagramTitle', 'Đề bài, designer, backend, kế hoạch', 'Brief, designer, backend, plan')
    m('diagramDesc', 'Từ đề bài, câu hỏi đi tới designer và backend; câu trả lời gom lại thành kế hoạch', 'From the brief, questions go to the designer and the backend; the answers come together as a plan')
    for k, vi, en in [('brief', 'Đề bài và bản thiết kế', 'Brief and mockup'), ('designer', 'Hỏi designer', 'Designer'), ('backend', 'Backend', 'Backend team'), ('plan', 'Kế hoạch', 'Plan')]:
        m('n.' + k, vi, en)
    m('met.asked', 'Yêu cầu phụ tìm ra trước', 'Secondary requirements found early'); m('met.late', 'Lộ ra sau phát hành', 'Found after release'); m('met.data', 'MB ảnh mỗi tháng, mỗi người', 'Photo MB per month, per user')
    a('cap.plan', 'Đề bài bên trái; câu hỏi đi tới designer (trên) và backend (dưới); kế hoạch bên phải. Khi hai khối giữa mờ, nghĩa là không ai được hỏi.', 'The brief on the left; questions go to the designer (top) and backend (bottom); the plan on the right. When the middle blocks are greyed out, nobody was asked.')
    S = [
        ('mockup', 's1', 'Nhận đề bài và bản thiết kế đẹp', 'Receive the brief and a polished mockup',
         'Màn chat trong bản thiết kế có tên ngắn, ảnh đẹp, mọi tin đều gửi thành công.', 'The chat screen in the mockup has short names, nice photos, and every message sent successfully.'),
        ('mockup', 's2', 'Mở IDE, dựng màn hình theo bản thiết kế', 'Open the IDE, build the screen from the mockup',
         'Mọi thứ trông giống bản thiết kế. Không ai hỏi chuyện gì xảy ra khi có sự cố.', 'Everything looks like the mockup. Nobody asks what happens when something goes wrong.'),
        ('mockup', 's3', 'Nối API, gửi ảnh gốc từ camera', 'Wire up the API, send camera photos as they are',
         'Gửi được chữ và ảnh trên mạng Wi-Fi của văn phòng. Tính năng được phát hành.', 'Text and photos send fine on the office Wi-Fi. The feature ships.'),
        ('mockup', 's4', 'Sau phát hành: sáu vấn đề lộ ra cùng lúc', 'After release: six problems surface at once',
         'Tên dài đè nút gửi, hộp thoại lỗi che màn chat, tin gửi lúc mất mạng biến mất, lỗi 401 hiện thô, câu lỗi tiếng Anh, thông báo sai ngôn ngữ. Và mỗi người tốn khoảng 240 MB dữ liệu di động mỗi tháng chỉ cho ảnh.', 'Long names cover the send button, an error dialog blocks the chat, offline messages vanish, raw 401 errors, English error text, notifications in the wrong language. And each user spends about 240 MB of mobile data a month on photos alone.'),
        ('asked', 's1', 'Nhận đề bài; chưa mở IDE', 'Receive the brief; do not open the IDE yet',
         'Ghi lại những gì bản thiết kế không nói, và ai có thể trả lời: designer hay backend.', 'Note what the mockup does not say, and who can answer: the designer or the backend.'),
        ('asked', 's2', 'Hỏi designer ba câu', 'Ask the designer three questions',
         'Nội dung xấu nhất, lỗi hiện ở đâu, mất mạng và trạng thái rỗng. Mỗi câu trả lời thành một yêu cầu cho màn hình.', 'Worst-case content, where errors show, offline and empty states. Each answer becomes a requirement for the screen.'),
        ('asked', 's3', 'Hỏi backend ba câu', 'Ask the backend three questions',
         'Phiên và timeout, định dạng lỗi, thông báo đẩy và ngôn ngữ. Mỗi câu trả lời thành một yêu cầu cho tầng mạng.', 'Sessions and timeouts, the error format, push notifications and language. Each answer becomes a requirement for the network layer.'),
        ('asked', 's4', 'Ước lượng nhanh, rồi chốt kế hoạch', 'A quick estimate, then settle the plan',
         'Hai ảnh mỗi ngày, thu nhỏ còn khoảng 300 KB: khoảng 18 MB mỗi tháng thay vì 240 MB. Thu nhỏ ảnh trước khi gửi thành một yêu cầu phi chức năng.', 'Two photos a day, resized to about 300 KB: about 18 MB a month instead of 240 MB. Resizing before sending becomes a non-functional requirement.'),
    ]
    for case, k, tv, te, xv, xe in S:
        sid = case + '.' + k
        m('s.%s.title' % sid, tv, te); m('s.%s.explain' % sid, xv, xe); m('ev.' + sid, tv, te)
    for k, vi, en in [
        ('try', 'Đi hết bốn bước của mỗi cách; để ý cột cuối của bảng câu hỏi.', 'Walk all four steps of each approach; watch the last column of the question table.'),
        ('mockup.s2', 'Tjeerd (ch.2): đừng mở IDE ngay; nếu cứ bắt tay làm mà không có kế hoạch, sau này sẽ phải làm lại khi lộ ra chi tiết chưa ai nghĩ tới. [[src:book-tjeerd]]', 'Tjeerd (ch.2): do not open the IDE yet; if you just start building without a plan, you will redo work later when a detail nobody thought of comes up. [[src:book-tjeerd]]'),
        ('mockup.s3', 'Mạng văn phòng là trường hợp đẹp nhất mà người dùng hiếm khi có.', 'The office network is the best case, one users rarely have.'),
        ('mockup.s4', 'Tjeerd (ch.2): thiết kế thường chỉ vẽ trường hợp đẹp; dữ liệu thật thì lộn xộn và không phải lúc nào cũng vừa thiết kế. [[src:book-tjeerd]]', 'Tjeerd (ch.2): designs usually show the best case; real data is messy and does not always fit them. [[src:book-tjeerd]]'),
        ('asked.s2', 'Tjeerd (ch.2): xin designer một bản với nội dung xấu nhất; bàn chuyện lỗi từ sớm và ưu tiên lỗi không chặn màn hình. [[src:book-tjeerd]]', 'Tjeerd (ch.2): ask the designer for a worst-case content version; discuss errors early and prefer errors that do not block the screen. [[src:book-tjeerd]]'),
        ('asked.s3', 'Tjeerd (ch.2): thống nhất với backend về phiên, token, timeout; về mã lỗi để app tự dịch; và về cách gửi ngôn ngữ của máy cho thông báo đẩy. [[src:book-tjeerd]]', 'Tjeerd (ch.2): align with the backend on sessions, tokens and timeouts; on error codes the app can localise; and on sending the device language for push notifications. [[src:book-tjeerd]]'),
        ('asked.s4', 'Alex Xu (tập 1 ch.2): ước lượng nhanh là chuyện quá trình; làm tròn số, ghi giả định và đơn vị. [[src:book-xu1]]', 'Alex Xu (vol. 1 ch.2): back-of-the-envelope estimation is about the process; round numbers, write down assumptions and units. [[src:book-xu1]]')]:
        m('co.' + k, vi, en)

    z = lambda k, vi, en=None: a('vz.' + k, vi, en)
    z('tab.pl', 'Câu hỏi và ước lượng', 'Questions and estimate')
    z('pl.cap', 'Mỗi hàng là một câu cần hỏi trước khi viết mã. Cột cuối: yêu cầu rút ra nếu đã hỏi, hay vấn đề lộ ra sau phát hành nếu không hỏi.', 'Each row is a question to ask before writing code. Last column: the requirement found if asked, or the problem that surfaces after release if not.')
    for k, vi, en in [('who', 'Hỏi ai', 'Ask'), ('q', 'Câu hỏi', 'Question'), ('req', 'Yêu cầu rút ra', 'Requirement found')]:
        z('pl.col.' + k, vi, en)
    z('pl.who.designer', 'Designer', 'designer'); z('pl.who.backend', 'Backend', 'backend')
    for k, q, r, late in [
        ('d1', ('Nội dung xấu nhất ra sao: tên dài, thiếu ảnh, tin 2.000 ký tự?', 'What does the worst content look like: long names, missing photos, a 2,000-character message?'),
         ('Bố cục chịu được nội dung xấu: cắt dòng, ảnh thay thế', 'A layout that survives bad content: truncation, placeholder images'), ('Tên dài đè lên nút gửi; ô ảnh trống', 'Long names cover the send button; empty photo boxes')),
        ('d2', ('Lỗi hiện ở đâu, có chặn màn hình không?', 'Where do errors show, and do they block the screen?'),
         ('Lỗi hiện tại chỗ cho từng tin, không dùng hộp thoại chặn', 'Inline errors per message, no blocking dialog'), ('Hộp thoại "Đã có lỗi" che cả màn chat', 'A "Something went wrong" dialog covers the chat')),
        ('d3', ('Lúc mất mạng, lúc chưa có tin nào, màn hình ra sao?', 'What does the screen look like offline, and with no messages yet?'),
         ('Trạng thái rỗng; tin "đang gửi" và "chưa gửi được, chạm để thử lại"', 'An empty state; "sending" and "not sent, tap to retry" messages'), ('Tin gửi lúc mất mạng biến mất không dấu vết', 'Messages sent offline vanish without a trace')),
        ('b1', ('Phiên, token, timeout: hết hạn thì server trả gì?', 'Sessions, tokens, timeouts: what does the server return when they expire?'),
         ('Làm mới token; hết phiên thì về đăng nhập, giữ bản nháp', 'Refresh the token; on session expiry go to sign-in, keep the draft'), ('Hết phiên giữa lúc gõ: lỗi 401 hiện thô', 'Session expires mid-typing: a raw 401 error')),
        ('b2', ('Lỗi trả về là câu chữ hay mã lỗi?', 'Are errors returned as sentences or as codes?'),
         ('Danh sách mã lỗi; app tự dịch theo mã', 'A list of error codes; the app localises by code'), ('Người dùng thấy câu lỗi tiếng Anh của server', 'Users see the server\'s English error text')),
        ('b3', ('Có thông báo đẩy không; ngôn ngữ của máy gửi lên thế nào?', 'Are there push notifications; how does the device language reach the server?'),
         ('Đăng ký thiết bị và gửi ngôn ngữ của app lên server', 'Register the device and send the app language to the server'), ('Thông báo tin nhắn mới đến bằng tiếng Anh', 'New-message notifications arrive in English'))]:
        z('pl.q.' + k, q[0], q[1]); z('pl.r.' + k, r[0], r[1]); z('pl.late.' + k, late[0], late[1])
    z('pl.ecap', 'Ước lượng nhanh dữ liệu di động cho ảnh (bước 4). Số tròn, giả định ghi rõ.', 'A quick estimate of mobile data for photos (step 4). Round numbers, assumptions stated.')
    z('pl.e.photos', 'Ảnh gửi mỗi ngày, mỗi người (giả định)', 'Photos sent per day, per user (assumed)')
    z('pl.e.size', 'Kích thước mỗi ảnh', 'Size of each photo')
    z('pl.e.month', 'Dữ liệu mỗi tháng (30 ngày)', 'Data per month (30 days)')
    z('pl.e.kb.mockup', 'ảnh gốc từ camera, khoảng {kb} KB', 'original camera photo, about {kb} KB')
    z('pl.e.kb.asked', 'thu nhỏ cạnh dài 1.600 px, khoảng {kb} KB', 'resized to 1,600 px on the long side, about {kb} KB')
    z('pl.e.mb', 'khoảng {n} MB', 'about {n} MB')
    z('pl.legend', 'Ô gạch đỏ: vấn đề lộ ra sau phát hành, hay một con số quá đắt cho dữ liệu di động.', 'Red hatched: a problem found after release, or a figure too costly for mobile data.')

    C = 'i1'
    a(C + '.title', 'Từ đề bài tới kế hoạch', 'From a brief to a plan')
    a(C + '.essence', 'Bản thiết kế màn hình chỉ cho thấy trường hợp đẹp. Trước khi viết mã, hỏi designer về nội dung xấu, lỗi, mất mạng; hỏi backend về phiên, timeout, mã lỗi, thông báo đẩy.\nMỗi câu trả lời là một yêu cầu phụ. Không hỏi thì chúng vẫn tới, chỉ là tới sau khi phát hành.\nƯớc lượng nhanh bằng số tròn (ảnh mỗi ngày × kích thước) làm lộ yêu cầu phi chức năng mà màn hình không nói, như dữ liệu di động và pin.',
      'A screen design only shows the best case. Before writing code, ask the designer about bad content, errors and offline states; ask the backend about sessions, timeouts, error codes and push notifications.\nEach answer is a secondary requirement. If you do not ask, they still arrive, just after release.\nA quick estimate with round numbers (photos per day × size) reveals non-functional requirements the screen does not mention, such as mobile data and battery.')
    a(C + '.goal.g1', 'Đã thấy câu hỏi gửi backend', 'Saw the questions for the backend')
    a(C + '.goal.g2', 'Đã thấy kết quả và ước lượng', 'Saw the outcome and the estimate')
    a(C + '.sim.sysdesign.plan', 'làm theo bản thiết kế hay hỏi trước', 'build from the mockup or ask first')

    S_ = 'hook'
    a(C + '.sec.%s.title' % S_, 'Đoán trước khi đọc', 'Predict before reading')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'predict', 'Bản thiết kế màn chat có tên bác sĩ ngắn, ảnh đẹp, mọi tin đều gửi thành công. Bạn dựng đúng như vậy và thử trên Wi-Fi văn phòng: hoàn hảo. Kể ra ba thứ bản thiết kế không nói mà người dùng sẽ gặp trong tuần đầu.',
      'The chat mockup has short doctor names, nice photos, and every message sent. You build exactly that and test on the office Wi-Fi: flawless. Name three things the mockup does not say that users will hit in the first week.')
    B(C, S_, 1, 'ans', 'Ví dụ: tin gửi lúc mất mạng (nó đi đâu?), phiên đăng nhập hết hạn giữa lúc gõ (server trả gì?), và một cái tên hay tin nhắn rất dài. Không cái nào hiện trên bản thiết kế; tất cả đều là yêu cầu phụ phải hỏi trước. Mô phỏng ngay dưới so hai cách bắt đầu. [[src:book-tjeerd]]',
      'For example: a message sent offline (where does it go?), a session expiring mid-typing (what does the server return?), and a very long name or message. None shows in the mockup; all are secondary requirements to ask about first. The simulation just below compares two ways to start. [[src:book-tjeerd]]')

    S_ = 'framework'
    a(C + '.sec.%s.title' % S_, 'Khung bốn bước của Alex Xu', 'Alex Xu\'s four-step framework')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'p', 'Alex Xu (System Design Interview tập 1, ch.3) đề xuất bốn bước cho một buổi thiết kế: (1) hiểu đề và khoanh phạm vi; (2) đề xuất thiết kế tổng quát và thống nhất; (3) đi sâu vào vài thành phần; (4) tổng kết, nêu điểm nghẽn và cải tiến. Đây là framework của tác giả, dùng cho phỏng vấn, nhưng bước 1 áp dụng nguyên cho việc thật. [[src:book-xu1]]',
      'Alex Xu (System Design Interview vol. 1, ch.3) proposes four steps for a design session: (1) understand the problem and set the scope; (2) propose a high-level design and agree on it; (3) deep dive into a few components; (4) wrap up with bottlenecks and improvements. It is the author\'s framework, meant for interviews, but step 1 applies unchanged to real work. [[src:book-xu1]]')
    B(C, S_, 2, 'p', 'Ở bước 1, Xu nhấn mạnh: đừng trả lời ngay; hỏi để làm rõ yêu cầu và giả định, và ghi giả định lại vì sẽ cần tới sau. Ông cũng coi thiết kế quá mức là một dấu hiệu xấu: say mê sự tinh khiết của thiết kế mà bỏ qua đánh đổi. [[src:book-xu1]]',
      'In step 1, Xu stresses: do not answer at once; ask to clarify requirements and assumptions, and write the assumptions down because you will need them later. He also treats over-engineering as a red flag: delighting in design purity while ignoring trade-offs. [[src:book-xu1]]')
    B(C, S_, 3, 'note', 'Track này nhìn từ phía app Android. Sách của Xu chủ yếu thiết kế server; những gì chương rút ra cho phía client là diễn giải của site.',
      'This track looks from the Android app\'s side. Xu\'s books mostly design servers; what this chapter draws out for the client is the site\'s interpretation.')
    B(C, S_, 3, 'kind', 'source')

    S_ = 'secondary'
    a(C + '.sec.%s.title' % S_, 'Yêu cầu phụ nằm ngoài bản thiết kế', 'Secondary requirements live outside the mockup')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'p', 'Tjeerd in \'t Veen (Mobile System Design, ch.2) khuyên đừng mở IDE ngay: việc đầu tiên là tìm yêu cầu phụ và trường hợp biên, không chỉ những gì thấy trên giao diện. Bắt tay làm mà không có kế hoạch thì sau này phải làm lại khi lộ ra một chi tiết chưa ai nghĩ tới, hoặc tệ hơn, làm những tính năng hóa ra không cần. [[src:book-tjeerd]]',
      'Tjeerd in \'t Veen (Mobile System Design, ch.2) advises not opening the IDE yet: the first job is to uncover secondary requirements and edge cases, not just what the UI shows. Building without a plan means redoing work when a detail nobody considered surfaces, or worse, building features nobody needed. [[src:book-tjeerd]]')
    B(C, S_, 2, 'p', 'Với designer, ba việc. Bản thiết kế thường chỉ chứa nội dung đẹp; dữ liệu thật thì lộn xộn: ảnh thiếu, mô tả quá dài, trường bỏ trống. Hãy xin một bản với nội dung xấu nhất. Bàn về lỗi từ sớm, vì thêm vào sau thì thường thành một hộp thoại "Đã có lỗi" chặn màn hình; ưu tiên lỗi tại chỗ không chặn giao diện. Và không phải mọi phần của bản thiết kế đều ưu tiên như nhau. [[src:book-tjeerd]]',
      'With the designer, three things. Designs usually hold only polished content; real data is messy: missing photos, overly long descriptions, empty fields. Ask for a worst-case content version. Discuss errors early, because added later they tend to become a blocking "Something went wrong" dialog; prefer inline errors that do not block the UI. And not every part of a design has equal priority. [[src:book-tjeerd]]')
    B(C, S_, 3, 'note', 'Site thêm một câu mà mọi app mobile nên hỏi: màn hình trông thế nào khi mất mạng và khi chưa có dữ liệu? Câu trả lời dẫn thẳng tới hàng chờ gửi ở track Lưu dữ liệu (H7).',
      'The site adds one question every mobile app should ask: what does the screen look like offline, and with no data yet? The answer leads straight to the upload queue in the Saving Data track (H7).')
    B(C, S_, 3, 'kind', 'android')

    S_ = 'backend'
    a(C + '.sec.%s.title' % S_, 'Những điều cần thống nhất với backend', 'What to agree with the backend')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'p', 'Tjeerd nêu các điểm cần thống nhất sớm. Phiên và token: lấy token thế nào, hết hạn thì sao, timeout trả lỗi gì. Lỗi: một lỗi chung hay lỗi chi tiết theo từng phần; và lỗi phải là mã, vì câu chữ tiếng Anh của server không phải để hiện cho người dùng, còn app cần dịch theo ngôn ngữ của mình. Thông báo đẩy: đăng ký thiết bị với backend, và gửi ngôn ngữ của người dùng để thông báo không tới sai tiếng. [[src:book-tjeerd]]',
      'Tjeerd lists points to agree early. Sessions and tokens: how to get a token, what happens on expiry, which error a timeout returns. Errors: one generic error or detailed ones per part; and errors must be codes, because the server\'s English sentences are not for users, and the app must localise them. Push notifications: register the device with the backend, and send the user\'s language so notifications do not arrive in the wrong language. [[src:book-tjeerd]]')
    B(C, S_, 2, 'kt', '// thỏa thuận mã lỗi với backend, app tự dịch\nwhen (error.code) {\n    11 -> R.string.err_list_unavailable      // "Không tải được danh sách"\n    12 -> R.string.err_session_expired       // về màn đăng nhập, giữ bản nháp\n    else -> R.string.err_generic             // lỗi tại chỗ, không chặn màn hình\n}',
      '// error codes agreed with the backend, localised by the app\nwhen (error.code) {\n    11 -> R.string.err_list_unavailable      // "Could not load the list"\n    12 -> R.string.err_session_expired       // go to sign-in, keep the draft\n    else -> R.string.err_generic             // inline error, never blocks the screen\n}')

    S_ = 'estimate'
    a(C + '.sec.%s.title' % S_, 'Ước lượng nhanh cho điện thoại', 'Quick estimates for a phone')
    a(C + '.sec.%s.badge' % S_, 'simplified')
    B(C, S_, 1, 'p', 'Alex Xu (tập 1, ch.2) mô tả ước lượng nhanh là tính áng chừng để biết thiết kế nào đáp ứng yêu cầu. Lời khuyên của ông: quan trọng là quá trình, không phải độ chính xác; làm tròn số; ghi giả định; ghi đơn vị. Sách tính cho server (QPS, dung lượng lưu trữ). [[src:book-xu1]]',
      'Alex Xu (vol. 1, ch.2) describes back-of-the-envelope estimation as rough calculation to see which designs meet the requirements. His advice: the process matters, not precision; round the numbers; write down assumptions; write the units. The book estimates for servers (QPS, storage). [[src:book-xu1]]')
    B(C, S_, 2, 'p', 'Phía điện thoại, các con số đáng ước lượng là dữ liệu di động mỗi tháng, dung lượng trên máy và số lần mạng phải bật. Ví dụ với giả định của site: 2 ảnh mỗi ngày × 4 MB ảnh gốc × 30 ngày ≈ 240 MB mỗi tháng; thu nhỏ còn 300 KB thì ≈ 18 MB. Một phép nhân đổi thành một yêu cầu: thu nhỏ ảnh trước khi gửi.',
      'On the phone side, the numbers worth estimating are mobile data per month, storage on the device, and how often the radio must wake. With the site\'s assumptions: 2 photos a day × 4 MB originals × 30 days ≈ 240 MB a month; resized to 300 KB, ≈ 18 MB. One multiplication becomes a requirement: resize photos before sending.')

    S_ = 'bugs'
    a(C + '.sec.%s.title' % S_, 'Hai lỗi hay gặp', 'Two common bugs')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'bug', 'Người dùng ở Việt Nam thấy "Could not load the conversation" khi mất mạng.', 'Users in Vietnam see "Could not load the conversation" when offline.')
    B(C, S_, 1, 'cause', 'App hiện thẳng câu lỗi server trả về; không ai thống nhất mã lỗi từ đầu.', 'The app shows the server\'s error sentence as is; nobody agreed on error codes at the start.')
    B(C, S_, 1, 'fix', 'Thống nhất danh sách mã lỗi với backend; app ánh xạ mã sang chuỗi đã dịch, và có một chuỗi chung cho mã lạ.', 'Agree on a list of error codes with the backend; the app maps codes to localised strings, with one generic string for unknown codes.')
    B(C, S_, 2, 'bug', 'Sau khi ra tính năng gửi ảnh, nhiều đánh giá phàn nàn app "ăn" dữ liệu di động.', 'After the photo feature ships, many reviews complain the app "eats" mobile data.')
    B(C, S_, 2, 'cause', 'App gửi ảnh gốc từ camera. Không ai ước lượng số MB mỗi tháng lúc lên kế hoạch.', 'The app sends original camera photos. Nobody estimated the MB per month during planning.')
    B(C, S_, 2, 'fix', 'Thu nhỏ và nén ảnh trước khi gửi; ước lượng lại với con số mới và ghi nó thành yêu cầu.', 'Resize and compress photos before sending; redo the estimate with the new figure and record it as a requirement.')

    S_ = 'ex'
    a(C + '.sec.%s.title' % S_, 'Bài tập', 'Exercise')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'ex', 'Đề bài mới: "Cho người dùng đính kèm kết quả xét nghiệm (PDF) vào lịch hẹn." Viết bốn câu hỏi cho designer, bốn câu cho backend, và một ước lượng nhanh có giả định và đơn vị. Với mỗi câu hỏi, ghi yêu cầu bạn mong rút ra.',
      'A new brief: "Let users attach lab results (PDF) to an appointment." Write four questions for the designer, four for the backend, and a quick estimate with assumptions and units. For each question, note the requirement you expect to get.')
    B(C, S_, 1, 'hint', 'Nghĩ về PDF rất lớn, mất mạng giữa lúc tải lên, file không phải PDF, xem trước, giới hạn kích thước, ai được xem, và tệp lưu ở đâu trên máy.', 'Think about very large PDFs, losing the network mid-upload, non-PDF files, previews, size limits, who may view it, and where the file lives on the device.')
    B(C, S_, 1, 'sol', 'Designer: PDF 30 trang hiện thế nào; tiến trình tải lên và lỗi tại chỗ; trạng thái "chưa gửi được, thử lại"; chọn file sai loại thì báo gì. Backend: giới hạn kích thước và loại file; tải lên có tiếp tục được không (chương I10); mã lỗi cho file quá lớn hay sai loại; quyền xem file (bác sĩ nào). Ước lượng: giả định 1 PDF mỗi lịch, 2 MB, 4 lịch mỗi tháng → khoảng 8 MB tải lên mỗi tháng mỗi người; trên máy, giữ bản tạm trong cache (H2) vì tải lại được.',
      'Designer: how a 30-page PDF displays; upload progress and inline errors; the "not sent, retry" state; what to say for a wrong file type. Backend: size and type limits; whether uploads can resume (chapter I10); error codes for too large or wrong type; who may view the file (which doctors). Estimate: assume 1 PDF per appointment, 2 MB, 4 appointments a month → about 8 MB uploaded per user per month; on the device, keep a temporary copy in the cache (H2) since it can be downloaded again.')

    S_ = 'honest'
    a(C + '.sec.%s.title' % S_, 'Chương này giản lược những gì', 'What this chapter simplifies')
    a(C + '.sec.%s.badge' % S_, 'simplified')
    B(C, S_, 1, 'p', 'Lời khuyên về yêu cầu phụ, designer và backend theo Tjeerd in \'t Veen, Mobile System Design ch.2 (bản early release); khung bốn bước và cách ước lượng theo Alex Xu, System Design Interview tập 1 ch.2–3; đọc ngày 2026-11-24, diễn đạt lại, không chép. Câu hỏi về mất mạng và trạng thái rỗng, mọi con số (ảnh mỗi ngày, 4 MB, 300 KB) và sáu vấn đề sau phát hành là của site. Chương không bàn kỹ năng phỏng vấn hay thiết kế phía server.',
      'Advice on secondary requirements, designers and the backend follows Tjeerd in \'t Veen, Mobile System Design ch.2 (early release); the four-step framework and estimation follow Alex Xu, System Design Interview vol. 1 ch.2–3; read on 2026-11-24, paraphrased, not copied. The offline and empty-state question, every number (photos per day, 4 MB, 300 KB) and the six post-release problems are the site\'s. The chapter does not cover interview skills or server-side design.')

    for q, qv, qe, av, ae, wv, we in [
        ('q1', 'Bước đầu tiên trong khung của Alex Xu là gì?', 'What is the first step in Alex Xu\'s framework?', 'Hiểu đề và khoanh phạm vi, bằng cách hỏi.', 'Understand the problem and set the scope, by asking.', 'Trả lời ngay mà chưa hiểu yêu cầu là dấu hiệu xấu.', 'Answering before understanding the requirements is a red flag.'),
        ('q2', 'Vì sao nên xin designer bản với nội dung xấu nhất?', 'Why ask the designer for a worst-case content version?', 'Vì bản thiết kế thường chỉ có nội dung đẹp; dữ liệu thật thì lộn xộn.', 'Because designs usually hold only polished content; real data is messy.', 'Bố cục phải chịu được tên dài, ảnh thiếu, trường trống.', 'The layout must survive long names, missing photos, empty fields.'),
        ('q3', 'Vì sao backend nên trả mã lỗi thay cho câu chữ?', 'Why should the backend return error codes instead of sentences?', 'Để app tự dịch theo ngôn ngữ của người dùng.', 'So the app can localise them in the user\'s language.', 'Câu tiếng Anh của server dùng để gỡ lỗi, không để hiện cho người dùng.', 'The server\'s English text is for debugging, not for users.'),
        ('q4', 'Ước lượng nhanh cần chính xác tới đâu?', 'How precise must a quick estimate be?', 'Không cần chính xác; làm tròn, ghi giả định và đơn vị.', 'Not precise; round, and state assumptions and units.', 'Quan trọng là quá trình (Alex Xu).', 'The process is what matters (Alex Xu).')]:
        a(C + '.quiz.%s.q' % q, qv, qe); a(C + '.quiz.%s.a' % q, av, ae); a(C + '.quiz.%s.why' % q, wv, we)
