# Bổ sung nghiên cứu: minh họa, chuyển động và cách học tương tác

> **Cập nhật:** 2026-11-22  
> **Phạm vi:** ghi chú bổ trợ cho AndroidDeepDiveExplorer, tập trung vào cách làm sơ đồ và animation dễ hiểu hơn, mượt hơn, có ích cho việc học.  
> **Thứ tự ưu tiên:** tài liệu này không thay thế hay sửa CLAUDE.md, 00-MASTER-PROMPT.md, STYLE-REFERENCE.md, CONSTRAINTS-CHECKLIST.md, docs/design-principles.md hoặc hợp đồng lõi. Nếu có điểm xung đột, các tài liệu và ràng buộc đang có của dự án được ưu tiên. Đây là hướng dẫn diễn giải thêm, không phải lệnh tự ý đổi kiến trúc.

## Kết luận nhanh

- Hai trang tham khảo làm tốt hai việc khác nhau: Designed to Scale dẫn người học qua một câu chuyện theo từng bước; Protocol Explorer cho người học điều khiển một không gian tra cứu và xem cùng luồng dữ liệu dưới dạng mạng hoặc chuỗi thời gian.
- Khi áp dụng vào AndroidDeepDiveExplorer, giữ đúng hai chế độ đã chốt trong master prompt: **Guided Deep-Dive** và **Live Explorer**. Dùng nhịp giải thích từng bước để dẫn người mới; giữ bố cục ba vùng của Live Explorer theo STYLE-REFERENCE. Không thêm chế độ thứ ba tên Explore. Mỗi bước phải cho thấy một thay đổi có nguyên nhân, đồng bộ giữa sơ đồ, giải thích, mã và nhật ký.
- Animation nên chỉ ra thứ tự, quan hệ hoặc thay đổi trạng thái. Người học phải điều khiển được nó, dừng được ở một khung, phát lại được và vẫn hiểu nội dung khi tắt chuyển động.
- Anime.js có thể dùng trong một trang HTML tĩnh bằng bundle UMD cục bộ; nhưng hợp đồng dự án hiện tại cấm thư viện ngoài. Vì vậy **chưa nên thêm Anime.js vào site**. Có thể dùng các tài liệu của nó để tham khảo cách tổ chức timeline; chỉ xem xét tích hợp nếu người dùng chủ động sửa ràng buộc đó và một mẫu nhỏ đã qua kiểm tra file://, offline, reduced-motion, điều khiển bước và đồng bộ mô hình.

## 1. Cách khảo sát, kết quả kiểm kê và giới hạn

Khảo sát có hai lớp, cần phân biệt khi dùng tài liệu này:

1. **Quan sát giao diện chạy thật:** ngày 2026-11-21, mở hai URL trong trình duyệt. Với Designed to Scale, xem “How a Request Travels” ở viewport hẹp, bước đầu và bước DNS kế tiếp, HUD chỉ số, stepper, giải thích, checklist và điều khiển Back/Next. Với Protocol Explorer, xem HTTP ở viewport rộng, danh mục và bộ lọc, các nhãn bước, thuộc tính, Network/Sequence, packet log và điều khiển Step/Play/Reset. Bấm Step đưa panel từ tổng quan sang bước đầu; Sequence cho thấy lifeline và mũi tên sự kiện.
2. **Kiểm kê tĩnh bundle công khai:** ngày 2026-11-22, tải JavaScript/CSS production như văn bản rồi tìm và trích xuất metadata/schema. Mã JavaScript **không được thực thi** trong quá trình kiểm kê. Việc này mở rộng đáng kể độ phủ dữ liệu, nhưng không thay thế việc đọc từng lời giải và chạy từng tương tác trên giao diện.

### 1.1 Designed to Scale: kiểm kê cấu trúc khóa học

Trong bundle đã kiểm tra, catalog có **40 bài thuộc 9 module, tổng cộng 445 bước**. Mỗi bài có từ 8 đến 14 bước; không nên ép bài mới vào một số bước cố định. Phân bố module:

| Module | Số bài |
|---|---:|
| Foundations | 3 |
| Scaling | 5 |
| Data & Storage | 11 |
| Communication | 4 |
| Reliability | 4 |
| Architecture | 4 |
| Security | 3 |
| Shipping | 2 |
| Whole Systems | 4 |

Metadata của 445 bước phân thành bảy loại: `problem` 120, `technique` 106, `solution` 97, `recap` 40, `insight` 39, `setup` 23, `tradeoff` 20. Mỗi bài có một recap trong dữ liệu được trích xuất. Đây là bằng chứng về một nhịp sư phạm có chủ đích: nêu bối cảnh/vấn đề, đưa kỹ thuật hoặc phương án, cân nhắc trade-off, rồi kết tinh lại. Nó **không** chứng minh mọi bài đều dùng đúng cùng một thứ tự; số bước và thứ tự thực tế thay đổi.

Các định nghĩa bài chứa tiêu đề/tóm tắt, danh sách bước (nhãn ngắn, loại, tiêu đề, nội dung; một số bước có callout, thay đổi và metric), cùng cấu hình scene gồm entities, links và flows. Runtime dùng dữ liệu bước để dựng scene và cập nhật HUD; cấu trúc này gợi ý một nguyên tắc có thể chuyển giao: **một bước là dữ liệu có cấu trúc dùng chung cho lời giải, hình và số liệu**, thay vì viết ba bản mô tả rời nhau. Đây là phân tích thiết kế từ bundle, không phải khẳng định mọi trường đều bắt buộc cho mọi bước.

### 1.2 Protocol Explorer: kiểm kê catalog và event model

Catalog tĩnh có **39 protocol definitions, 231 bước**, mỗi protocol từ 4 đến 8 bước. Tên trong catalog: BGP, DHCP, DNS, DNSSEC, DNS over HTTPS, Ethernet, FTP, HTTP, HTTPS, ICMP, IGMP, IMAP, IP, IPsec, IPv6, Modbus, NTP, POP3, Captive Portal, PPPoE, HTTP Proxy, QUIC, RADIUS, Reverse Proxy, RTMP, RTSP, SIP, SMB, SMTP, SOCKS5, SSH, TCP, TLS/SSL, UDP, WebRTC, WebSocket, Wi-Fi, WireGuard và WPA3. Giao diện phân nhóm Core 11, Application 19 và Security 9.

Mỗi định nghĩa protocol có metadata như tên/tiêu đề, layer, node map, latency, legend, facts, phần mở đầu/kết thúc và các bước. Cả 231 bước đều có title, description, detail và trường `events`; event có thể chứa source/destination, protocol, thời điểm, thông tin, kích thước và các trường hiển thị wire/protocol tùy loại sự kiện. Không nên giả định tất cả event đều có cùng tập trường hoặc giá trị.

HTTP là luồng được xem trực tiếp. Bundle cho thấy mỗi protocol có cấu hình scene/flow riêng, còn shell điều khiển được dùng chung. Network và Sequence là hai cách chiếu của cùng mô hình sự kiện: một cách nhấn vào topology/đường đi, cách kia nhấn vào lifeline/thứ tự thời gian; packet log cung cấp bản ghi chi tiết. **Suy luận thiết kế:** khi làm mô phỏng Android, có thể dùng một event model làm nguồn sự thật cho sơ đồ, timeline và nhật ký, nhưng chỉ nên tạo nhiều view khi mỗi view trả lời một câu hỏi học khác nhau.

### 1.3 Tín hiệu triển khai nhìn thấy trong bundle

| Quan sát văn bản trong asset | Điều có thể kết luận | Điều không thể kết luận chỉ từ việc tìm chuỗi |
|---|---|---|
| Designed to Scale có SVG scene, `requestAnimationFrame`, chuyển frame/step; CSS có keyframes và breakpoint hẹp | Trang có renderer/loop trình bày tùy biến và có nhiều trạng thái đáp ứng | Không suy ra chính xác FPS, độ mượt trên mọi máy hay toàn bộ xử lý lifecycle |
| Protocol Explorer có `Element.animate`, `requestAnimationFrame`, SVG; CSS có keyframes | Trang kết hợp Web Animations API với logic trình bày tùy biến | Không chứng minh mọi hiệu ứng dùng cùng một engine hoặc cùng timing |
| Không tìm thấy identifier `animejs` trong hai bundle đã kiểm | Không có bằng chứng hai trang dùng Anime.js trong các bundle được kiểm | Không thể chứng minh một dependency không tồn tại ở mọi asset, phiên bản hoặc dịch vụ phụ trợ |
| Cả hai bundle có chuỗi/thuộc tính accessibility; CSS/JS có một số nhánh reduced-motion | Có các hỗ trợ accessibility và reduced-motion ở một số vị trí | Không chứng minh mọi chuyển động nội dung đều tôn trọng reduced-motion; site của ta phải rà từng loại motion |
| Không thấy xử lý chuỗi `visibilitychange` trong hai bundle chính | Chưa tìm thấy bằng chứng pause theo trạng thái tab trong hai bundle chính | Không kết luận chắc chắn rằng không có pause ở một module/asset khác |

Ở snapshot CSS: Designed to Scale có 14 khai báo `@keyframes`, 13 `@font-face`, breakpoint tại 639px/380px và nhánh `hover:none`; Protocol Explorer có 12 `@keyframes`, 24 `@font-face`, ba nhánh `prefers-reduced-motion` và một breakpoint desktop từ 1360px. Đây chỉ là dấu vân tay để mô tả asset, không phải token hay thông số nên chép. Hợp đồng AndroidDeepDiveExplorer vẫn cấm webfont và yêu cầu dùng token riêng.

Các gói kiểm tra chính (đường dẫn có thể đổi khi trang deploy lại):

- Designed to Scale: [`index-BeXJu_A0.js`](https://designed-to-scale.vercel.app/assets/index-BeXJu_A0.js), 784,539 ký tự văn bản đã giải mã; SHA-256 của nội dung UTF-8 đã giải mã: `475546d36e0549aecbc4d5e4557f7d5fecfd0b14f207ef7e0b5412c464b06fa0`. CSS [`index-CxX-BAVx.css`](https://designed-to-scale.vercel.app/assets/index-CxX-BAVx.css), 64,267 ký tự.
- Protocol Explorer: [`index-CNPseYOQ.js`](https://protocol-explorer-alpha.vercel.app/assets/index-CNPseYOQ.js), 504,344 ký tự văn bản đã giải mã; SHA-256 của nội dung UTF-8 đã giải mã: `19e285d11f5fa0b1411ec94aaea6cd04531872e8322bb8a46c80e4f92e262834`. CSS [`index-CwjpA-vk.css`](https://protocol-explorer-alpha.vercel.app/assets/index-CwjpA-vk.css), 75,991 ký tự.

Các `.js.map` tại vị trí dự đoán không trả về source map trong lần kiểm tra. Fingerprint ở đây chỉ giúp nhận diện snapshot đã khảo sát, không phải version/API contract của sản phẩm.

### 1.4 Ranh giới kiểm chứng

- Đã quan sát trực tiếp một luồng bài học mẫu ở Designed to Scale và luồng HTTP ở Protocol Explorer; **chưa diễn tập tương tác từng bước của cả 40 bài và cả 39 protocol trong browser**.
- Đã kiểm kê số lượng, tên, tiêu đề/metadata bước và schema của toàn bộ định nghĩa được tìm thấy trong hai bundle chính. **Chưa đọc thủ công từng đoạn body dài, từng payload event và mọi nhánh UI của tất cả 676 bước**. Vì vậy số đếm/schema đáng tin cậy hơn mọi nhận định về độ chính xác chuyên môn của từng protocol/lesson.
- Trang web có thể được deploy lại sau ngày khảo sát; tên bundle, hash và nội dung là snapshot ngày nêu trên. Khi cần xác nhận hành vi hiện tại, mở lại URL và kiểm tra trực tiếp.
- Số lượng trích xuất giúp Claude biết quy mô và hình dạng dữ liệu; không phải yêu cầu sao chép nội dung, cấu trúc câu chữ, hình, màu, asset hay code của các trang. Hãy giữ bảng khác biệt và nhận diện riêng đã chốt trong `STYLE-REFERENCE.md`.

Do đó, mô tả mức độ khảo sát chính xác là: **đã xem kỹ một mẫu tương tác trên mỗi site, đồng thời kiểm kê tĩnh toàn bộ catalog/metadata bước có trong bundle chính; chưa đọc hoặc phát toàn bộ từng bài và từng giao thức bằng trình duyệt**. Những nguyên tắc ở phần sau là bài học UX/kiến trúc rút ra từ dữ liệu đó, không phải tuyên bố rằng mọi chi tiết của cả hai website đã được xác minh bằng tay.

### 1.5 Cách Claude nên dùng phần khảo sát này

- Xem số liệu và asset fingerprint như **ghi chú khảo sát có ngày**, không như hợp đồng cho website đích. Khi triển khai, tuân thủ `CLAUDE.md`, `00-MASTER-PROMPT.md`, `STYLE-REFERENCE.md`, track spec và checklist hiện có.
- Chuyển giao ý tưởng ở mức nguyên tắc: dữ liệu bước có cấu trúc; event model duy nhất có thể nuôi sơ đồ/timeline/log; một bước biểu diễn một thay đổi có nhân quả; cho phép đứng yên để đọc và xem lại. Không chép mã, văn bản, minh họa, ví dụ hoặc theme từ các trang tham khảo.
- Gắn cách trình bày cụ thể vào hai chế độ đã có (`Guided Deep-Dive`, `Live Explorer`), schema step/model, router và registry đã quy định. Đây không phải đề xuất tạo mode mới hay thay đổi core.
- Xem các thiếu sót không xác minh được (ví dụ lifecycle khi tab ẩn, độ phủ reduced-motion của website mẫu) là khoảng trống khảo sát, không phải hành vi cần sao chép. Thiết kế site đích theo yêu cầu trợ năng/QA đã chốt.

## 2. Điều đáng học từ từng mẫu

| Mẫu | Hành vi đã quan sát | Điều có ích cho người học | Cách áp dụng vào dự án |
|---|---|---|---|
| Designed to Scale | Breadcrumb, số bài/bước, thời lượng và cấp độ; dải chỉ số bắt đầu ở trạng thái chưa biết; sơ đồ và chú giải; stepper có tên; giải thích từng bước; Back/Next; checklist mục tiêu; replay/pause | Có một con đường học rõ ràng; người học biết đang ở đâu, bước này giải quyết câu hỏi gì và điều gì vừa thay đổi | Guided mở đầu bằng một trạng thái ban đầu yên tĩnh. Mỗi lần Next nêu rõ bước kế tiếp và chỉ thêm một biến đổi quan trọng. Mục tiêu được đánh dấu theo hiểu biết đã đi qua, không chỉ theo số bước |
| Protocol Explorer | Danh mục có nhóm và bộ lọc; HTTP mở ra năm bước; chuyển Network/Sequence; panel tổng quan có thuộc tính; packet flow có Play/Step/Reset/tốc độ; chọn Step làm hiện chi tiết bước và trạng thái “chưa có packet” | Có thể chuyển giữa bản đồ không gian và thứ tự thời gian; chi tiết sự kiện có chỗ riêng; người học chọn được tốc độ và mức quan sát | Giữ hai cách nhìn khi chúng làm rõ hai câu hỏi khác nhau. Trong Compose Runtime, ví dụ là “các thành phần liên hệ ra sao?” so với “một lần state đổi đi qua các bước theo thứ tự nào?”. Đừng đưa mọi chi tiết nâng cao lên màn hình mặc định |
| Cả hai | Panel, tiến độ và sơ đồ cùng đổi theo bước; có điều khiển phát/dừng hoặc bước đơn | Giảm việc phải tự ghép thông tin từ nhiều vùng; người học kiểm tra lại nhân quả ở đúng thời điểm | Bước hiện tại, phần code được nhấn, node đang đổi và dòng nhật ký phải cùng biểu diễn một sự kiện trong model |

### Không nên bê nguyên mẫu

Hai mẫu có mục đích khác nhau. Một là bài giảng theo tuyến; một là explorer dày thông tin. Không nên trộn tất cả bộ lọc, bảng, danh mục, thuộc tính, shortcut và chuyển động vào từng màn Guided. Với người mới, cho thấy một “đường đi cơ bản” trước, rồi đặt các view phụ sau một nút rõ nghĩa như “Xem toàn cảnh”, “Mở chi tiết” hoặc tab Sequence.

Giữ lại pattern tương tác chung đã được chốt trong STYLE-REFERENCE.md, nhưng mọi hình, ví dụ, nhãn, màu, icon, logo, code và bố cục cụ thể tiếp tục theo nhận diện AndroidDeepDiveExplorer. Không trace hoặc sao chép asset/CSS/mã/câu chữ từ trang tham khảo.

## 3. Quy tắc một bước học tốt

Mỗi bước nên làm rõ một câu hỏi cụ thể:

1. **Người học đang ở trạng thái nào?** Giữ trạng thái cũ nhìn thấy được.
2. **Điều gì sắp xảy ra?** Đưa câu hỏi đoán trước, ví dụ “Nếu mutableStateOf đổi, phần nào có lý do chạy lại?”.
3. **Người học thực hiện gì?** Step hoặc Play tiến mô hình, không tự chuyển cảnh trước khi câu hỏi được nêu.
4. **Cơ chế nào tạo ra kết quả?** Hiện một luồng hoặc một thay đổi quan trọng; chú thích ngắn bằng ngôn ngữ đời thường rồi gắn tên kỹ thuật.
5. **Bằng chứng nằm ở đâu?** Cập nhật đúng dòng nhật ký, state trước/sau, mã nguồn liên quan và node trong sơ đồ.
6. **Điều gì không xảy ra?** Khi hữu ích, chỉ rõ phần bị bỏ qua, không invalidated, không recompose, hoặc chưa có packet/job/frame.
7. **Người học tự nói lại điều gì?** Đặt câu hỏi nhớ lại ngắn trước khi sang bước tiếp theo.

Không nhất thiết mọi bước đều cần đủ bảy thành phần trên màn hình. Mục đích là giữ mạch nhân quả; chỉ hiện chi tiết phục vụ câu hỏi của bước hiện tại. Phần nâng cao nên đóng/mở được thay vì dồn toàn bộ vào một khung.

### Hình và sơ đồ

- Mỗi hình có một mục tiêu đọc duy nhất, tiêu đề “Bạn đang xem gì?” và chú giải. Câu chú thích nói hình vẽ thành phần nào, mũi tên mang ý nghĩa gì, và người học nên quan sát điểm nào.
- Trước khi dùng thuật ngữ, có thể đưa một ẩn dụ đời thường ngắn. Ngay sau đó phải nói rõ phần nào của ẩn dụ tương ứng với implementation và phần nào không tương ứng. Không để ẩn dụ thay thế định nghĩa.
- Tên node, trạng thái và cạnh giữ cùng một nghĩa xuyên suốt bài. Phân biệt “đọc state”, “đánh dấu invalidation”, “chạy lại composition”, “apply changes”, “layout” và “draw”; không gom chúng thành một mũi tên mơ hồ “UI update”.
- Màu không phải tín hiệu duy nhất. Kết hợp nhãn, hình dạng, kiểu nét hoặc icon; dùng từ ngữ song ngữ của dự án.
- Đừng đưa toàn bộ code vào hình. Đánh dấu đúng dòng code đang giải thích; nếu code dài, thu gọn phần không liên quan.
- Khi có số, phân biệt số lấy từ nguồn/API, số do mô hình đặt ra và số chỉ để minh họa. Thời gian trong simulator không được làm người học hiểu nhầm là latency hoặc frame budget được bảo đảm.
- Giữ toàn cảnh để định hướng. Chỉ zoom vào vùng đang nói tới khi điều đó giải quyết vấn đề định vị; nếu zoom làm mất quan hệ giữa các node thì dùng viền nhấn hoặc lớp phủ thay thế.
- Một mô hình chỉ nên thể hiện đủ thành phần để giải thích câu hỏi. Cho phép mở lớp “nội bộ/chi tiết” khi người học sẵn sàng; không khởi đầu bằng kiến trúc đầy đủ nếu chưa có một đường đi cụ thể.

### Ví dụ áp dụng cho Android

**Compose Runtime:** bắt đầu từ thao tác đổi state. Hiện StateObject/record, nơi đọc state, vùng invalidated và bước kế tiếp của Recomposer. Sau đó cho người học bước qua Composer/SlotTable và Applier. Tách rõ “runtime phải làm gì theo hợp đồng” khỏi “chi tiết implementation hiện tại”; chi tiết implementation cần nhãn và phiên bản/commit theo chính sách của dự án. Nếu mô phỏng bỏ qua snapshot isolation hoặc scheduling, ghi điều đó ngay gần sơ đồ.

**Coroutines:** dùng một coroutine nhỏ và một suspension point. Trước khi hiện tiếp, hỏi người học thread có bị block không và phần local state được giữ ở đâu. Trên sơ đồ cây Job và timeline, phân biệt suspend, waiting, cancelled, completed bằng hình/nhãn nhất quán; không biểu diễn suspension là một thread đang ngủ nếu mô hình không nói điều đó.

**Compose Animation:** giữ riêng các giá trị current, target, velocity và thời gian mô phỏng. Người học chọn frame hoặc bấm Step Frame để thấy giá trị thay đổi; đổi target giữa chừng phải cho thấy animation tiếp tục từ giá trị/velocity nào theo mô hình đã công bố. Kèm state phase (composition/layout/draw) khi nó liên quan; không gắn nhãn “recomposition mỗi frame” nếu không đúng với vị trí đọc state.

Các quy tắc nội dung này bổ sung cho docs/androidbooks-knowledge/learning-methods.md, docs/research/animation.md và docs/core-api.md; không thay thế kết luận kỹ thuật trong các file đó.

## 4. Chuyển động dùng để giải thích, không để lấp chỗ trống

### Nhịp chuyển động nên có

- **Trước:** khung đầu cho thấy trạng thái cũ và câu hỏi.
- **Đang diễn ra:** chuyển động chỉ làm rõ một luồng, thay đổi hoặc quan hệ. Ví dụ: token chạy từ producer đến consumer; viền node đổi trạng thái; một cạnh được vẽ theo thứ tự.
- **Sau:** giữ trạng thái cuối đủ lâu để đọc được; cập nhật panel, code highlight, metric và event log cùng một bước.
- **Kết thúc:** người học có thể đứng ở khung đó, lùi, phát lại hoặc đi tiếp.

Không chạy liên tục khi người học chưa chọn Play. Không lặp vô hạn cho animation minh họa kiến thức. Tránh đồng thời zoom camera, phóng node, tô sáng nhiều cạnh, chạy token, gõ chữ và cập nhật cả panel. Hãy chọn một chuyển động chính và nhiều nhất một tín hiệu phụ; các yếu tố còn lại nên giữ ổn định.

### Đồng bộ thời gian

- Model là nguồn sự thật về state và thứ tự sự kiện. View chỉ trình bày một snapshot của model ở thời điểm đang xem.
- Phân biệt thời gian mô phỏng với thời gian animation trên màn hình. Nếu một bước giả lập 40 ms nhưng transition hiển thị mất 250 ms, nhãn phải cho người học biết đó là hai đồng hồ khác nhau.
- Với mô hình rời rạc, Next/Previous/Replay phải dựng lại chính xác trạng thái của step tương ứng. Không để một animation đang chạy ghi đè state của step sau.
- Với mô hình liên tục, Step Frame và thanh thời gian phải lấy từ virtual clock/model đã có; việc kéo về một thời điểm phải render đúng giá trị ở thời điểm đó. Animation trình bày không được tự trở thành một mô hình thứ hai.
- Khi đổi bước, đổi ngôn ngữ, đổi route, reset, chuyển tab hoặc tắt chuyển động: dừng transition đang chạy trước rồi dựng lại trạng thái đích. Không để hai hoạt ảnh cũ/mới cùng điều khiển một node.
- Khi tab trình duyệt bị ẩn, dừng hoặc pause phát tự động và giữ tiến độ có thể khôi phục; không “nhảy cóc” qua bước mà người học chưa nhìn thấy.

### Hiệu năng và cảm giác mượt

- Với hiệu ứng giao diện thông thường, ưu tiên thay đổi transform và opacity; các thuộc tính làm đổi layout hoặc yêu cầu vẽ lại lớn chỉ dùng khi cần giải thích chính thay đổi layout/paint. Dùng Chrome DevTools để tìm đúng bottleneck thay vì thêm will-change một cách mặc định. Tham khảo [hướng dẫn animation hiệu năng cao của web.dev](https://web.dev/articles/animations-guide).
- Với SVG, giới hạn số phần tử chuyển động đồng thời; tránh blur/filter lớn trên vùng rộng; không redraw toàn bộ sơ đồ nếu chỉ một token hoặc một node đổi.
- Các cạnh chạy theo đường dẫn cần giữ hướng và điểm đến rõ. Không để token chồng lên nhãn hoặc đi xuyên qua node mà không có ý nghĩa.
- Dùng easing và thời lượng nhất quán từ các token đã chốt trong docs/research/ui.md và docs/design-principles.md; không tự đặt một bộ duration thứ hai. Thời gian mô phỏng do track chọn phải có nhãn và giả định riêng.
- Đừng đánh giá “mượt” chỉ bằng việc animation chạy nhanh. Người mới cần chuyển động đủ chậm để đọc và đủ ngắn để không làm mất nhịp. Cho phép Step và Replay để người học tự chọn tốc độ quan sát.
- Trạng thái tĩnh phải tự giải thích được: nếu tắt animation, vẫn nhìn ra trạng thái đầu, trạng thái cuối, mũi tên/quan hệ và điều gì đã thay đổi.

## 5. Điều khiển và hỗ trợ người mới

- Bước đầu ưu tiên Step có giải thích; Play là tùy chọn để xem cả chuỗi sau khi người học đã hiểu nhịp.
- Nhãn điều khiển mô tả kết quả: “Bước tiếp: Composer ghi thay đổi” dễ hiểu hơn chỉ có icon mũi tên.
- Step, Next, Previous, Reset, Replay, Pause và tốc độ phải có trạng thái enable/disable đúng; nút disabled cần giải thích khi người học dễ hiểu nhầm.
- Tiến độ nên là “Bước 2/8 — tên bước”, không chỉ là một thanh không nhãn. Có thể bấm một bước đã qua để xem lại.
- Mỗi sơ đồ có chế độ “Chỉ sơ đồ/không zoom” như đã quy định. Đây là cách giữ ngữ cảnh, không thay cho nút giảm chuyển động.
- Dùng đúng hai chế độ trong master prompt, không thêm mode mới:
  - **Guided Deep-Dive:** tuyến học cho người mới, một câu hỏi và một thay đổi mỗi lần, có lời giải và retrieval check.
  - **Live Explorer:** mô phỏng theo spec với Step/Play/Pause/Reset/tốc độ. Có thể cung cấp góc nhìn sơ đồ/timeline và chi tiết event phù hợp với câu hỏi; không biến Live Explorer thành một catalog/drawer mode mới.
- Không bắt người học ghi nhớ shortcut. Phím tắt là đường nhanh phụ; luôn giữ nút và nhãn nhìn thấy được, và không cướp phím khi focus đang ở input/control.

### Trợ năng và reduced motion

- Tôn trọng prefers-reduced-motion và giữ nút bật/tắt chuyển động thủ công như thiết kế hiện có. Khi giảm chuyển động, bỏ camera zoom, parallax, typewriter, pulse và token chạy; chuyển thẳng tới state cuối của cùng bước. Vẫn cho Step, Previous, Next và Replay theo kiểu cập nhật tức thời.
- Không tự động phát một animation mang tính minh họa trước khi người học tương tác. Khi animation khởi động theo thao tác, luôn có cách dừng/tắt nếu đó không phải phần thiết yếu để hiểu hành động. WCAG 2.2 SC 2.3.3 nói về animation không thiết yếu do tương tác gây ra ở mức AAA; SC 2.2.2 xử lý một số nội dung chuyển động tự chạy kéo dài. Hãy mô tả chính xác mức chuẩn, không gọi mọi khuyến nghị là điều kiện WCAG bắt buộc.
- Bất kỳ thông tin nào truyền bằng chuyển động cũng cần tương đương tĩnh bằng nhãn hoặc trạng thái. Không dùng màu/nhấp nháy riêng lẻ để báo “đã hoàn tất”, “đang lỗi” hoặc “đang chạy”.
- Accessibility tree cần đọc được control, bước hiện tại và nội dung tĩnh của sơ đồ. SVG có title/description; trạng thái đổi bước được thông báo vừa phải, không phát thông báo screen reader mỗi frame. Với hàng nhật ký và stepper, cung cấp tên và vị trí trong tập hợp.
- Chuyển động không nên chiếm focus hay làm mất focus bàn phím. Kiểm tra Tab, Shift+Tab, Enter, Space, Escape và các shortcut hiện có.
- prefers-reduced-motion là tín hiệu ưu tiên của hệ điều hành/trình duyệt; xem [W3C Media Queries Level 5](https://www.w3.org/TR/mediaqueries-5/#prefers-reduced-motion) và [MDN: prefers-reduced-motion](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/@media/prefers-reduced-motion). Nội dung về tiêu chí chuyển động xem [WCAG 2.2 SC 2.3.3](https://www.w3.org/WAI/WCAG22/Understanding/animation-from-interactions.html) và [SC 2.2.2](https://www.w3.org/WAI/WCAG22/Understanding/pause-stop-hide.html).

## 6. Anime.js: đánh giá có điều kiện

### Anime.js làm được gì

Tài liệu Anime.js hiện tại mô tả thư viện như engine animation cho CSS, SVG, thuộc tính DOM và JavaScript objects. API có animate, createTimeline, ghép các animation/timer/callback, các phương thức phát/dừng/đảo/ngắt/khôi phục và khả năng điều khiển thời gian của timeline. Tài liệu cài đặt liệt kê bundle UMD dist/bundles/anime.umd.min.js; trang này cho ví dụ nạp bằng script và lấy API toàn cục anime. README/package chính thức ghi license MIT; package.json trên nhánh chính ghi 4.5.0 vào ngày khảo sát.

Vì vậy, xét riêng khả năng kỹ thuật, có thể đặt một bản đã tải về trong thư mục dự án và nạp cục bộ; cách này không cần ES module, CDN hoặc truy cập mạng khi chạy. Tuy nhiên, tài liệu Anime.js không tự chứng minh bundle tương thích với mọi cấu hình file:// của site. Phải kiểm tra trong chính browser mục tiêu trước khi tích hợp.

### Quyết định với dự án hiện tại

CLAUDE.md và master prompt hiện cấm cài hoặc dùng thư viện ngoài, package manager và build step. Một file Anime.js được vendored vẫn là thư viện bên thứ ba. Do đó:

1. Không thêm Anime.js vào index.html, js/core, track hay generator trong phạm vi ràng buộc hiện tại.
2. Có thể học từ docs của nó về timeline, labels, pause, seek, callback, cancel/revert; không cần thêm runtime dependency để áp dụng các ý tưởng đó.
3. Nếu người dùng về sau cho phép đổi ràng buộc, chỉ thử trên một bản demo riêng biệt trước; pin release/version cụ thể, giữ license/notice, lưu file cục bộ, không CDN. Sau đó kiểm tra file://, offline, console, reduced motion, reload, reset, đổi route, keyboard và đồng bộ với model. Không lấy nhánh master làm dependency không pin.
4. Kể cả khi được cho phép, Anime.js chỉ được điều khiển phần trình bày trong view. Không để callback animation ghi state vào model; model/virtual clock hiện tại tiếp tục là nguồn sự thật. Adapter phải có đường dựng trạng thái tĩnh chính xác và hủy sạch animation khi step/route đổi.
5. Trước khi thêm thư viện, so sánh lợi ích thực tế với CSS transitions, SVG và requestAnimationFrame/engine hiện hữu. Nếu chỉ cần một token đi trên cạnh hoặc vẽ một đường, giải pháp hiện có thường gọn hơn.

Kiểm kê tĩnh hai bundle ở §1.3 cũng không tìm thấy identifier `animejs`; một bundle cho thấy SVG/`requestAnimationFrame`, bundle còn lại có `Element.animate` cùng logic tùy biến. Đây chỉ là tín hiệu từ hai bundle chính, không phải chứng minh tuyệt đối về mọi asset. Dù vậy, nó cho thấy chuyển động chỉ dẫn không tự động đòi hỏi Anime.js; trước tiên cần một model có thể tua/lùi/reset ổn định và một adapter trình bày nhỏ.

**Kết luận:** Anime.js là lựa chọn khả thi về kỹ thuật sau khi bỏ ràng buộc “không thư viện ngoài”; theo hợp đồng hiện tại, chưa được tích hợp. Đây là đánh giá phạm vi, không phải yêu cầu Claude thay đổi master prompt.

Nguồn Anime.js: [installation và UMD/local bundle](https://animejs.com/documentation/getting-started/installation/), [animation API](https://animejs.com/documentation/animation/), [timeline](https://animejs.com/documentation/timeline/), [playback methods](https://animejs.com/documentation/animation/animation-methods/), [repository và MIT license](https://github.com/juliangarnier/anime).

## 7. Nguyên tắc học sâu cần gắn vào tương tác

Áp dụng cùng docs/androidbooks-knowledge/learning-methods.md; không cần tạo một lý thuyết học mới cho mỗi chương.

- **Prediction trước reveal:** cho chọn dự đoán trước Step; sau Step giải thích vì sao. Đừng cho câu hỏi mà đáp án đã lộ ra trong sơ đồ trước khi người học trả lời.
- **Retrieval practice:** sau một nhóm bước, ẩn panel giải thích và hỏi người học tự nhớ đường đi, rồi mới mở gợi ý/đáp án. Mục tiêu là tự nhớ và giải thích, không phải chỉ bấm đúng.
- **Worked example rồi rút gợi ý:** chương đầu cho một ví dụ trọn vẹn; ví dụ kế tiếp bỏ trống một cạnh, node hoặc giá trị; cuối mục đưa tình huống bug khác để chuyển giao.
- **Self-explanation:** hỏi “vì sao node này đổi?”, “bằng chứng nào cho thấy chỉ consumer này bị invalidated?”, “nếu đổi target giữa chừng thì giá trị kế tiếp lấy từ đâu?”.
- **Dual coding có kỷ luật:** sơ đồ và câu chữ cùng giải thích một ý nhưng mỗi kênh bổ sung thông tin riêng. Không thêm icon/texture/animation chỉ để làm trang sinh động.
- **Cognitive load:** mở đầu bằng ít node, một đường đi và một thuật ngữ mới mỗi nhịp. Thêm nhánh/ngoại lệ sau khi đường cơ bản đã hiểu; dùng cùng ví dụ xuyên chương để người học không phải học lại bối cảnh.
- **Interleaving sau khi đã học riêng:** trộn các cặp dễ nhầm (suspend/block, composition/recomposition, layout/draw, tween/spring) trong câu hỏi ôn, không đưa chúng vào sơ đồ đầu tiên cùng lúc.
- **Spacing:** ôn một câu hỏi cũ ở đầu bài/chương sau; nếu lưu thẻ ôn, tiếp tục dùng chính sách privacy của site, dữ liệu local và có thể xóa được. Không tuyên bố lịch ôn là tối ưu cho mọi người.

Bằng chứng và giới hạn của các phương pháp trên đã được ghi ở cuối docs/androidbooks-knowledge/learning-methods.md, gồm review Dunlosky et al. (2013), Roediger & Karpicke (2006), Cepeda et al. (2006) và Agarwal et al. (2021). Hãy giữ đúng sắc thái của các nguồn: retrieval/distributed practice có hỗ trợ rộng; self-explanation và interleaving phụ thuộc dạng bài/bối cảnh. Không tuyên bố animation tự nó làm người học nhớ lâu hơn.

## 8. Cách đánh giá một mô phỏng trước khi đưa vào bài

Đây là danh sách rà soát thủ công cho Claude/người làm nội dung; không có bài kiểm thử nào được chạy khi viết ghi chú này.

### Đúng kiến thức

- [ ] Mỗi mũi tên, nhãn, state và con số có nghĩa xác định.
- [ ] Nguồn cho claim nằm gần lời giải; nội dung nội bộ có nhãn/version như hợp đồng dự án yêu cầu.
- [ ] Mô phỏng ghi rõ điều giản lược, giả định và sự kiện không mô phỏng.
- [ ] Hình minh họa đúng với code/trace đang nói, không chỉ “trông giống”.
- [ ] Người học có thể tắt motion và vẫn giải thích được trạng thái.

### Dễ theo dõi

- [ ] Người mới biết họ đang ở đâu, cần nhìn điểm nào, điều gì vừa đổi và tại sao.
- [ ] Một step không cùng lúc đổi quá nhiều ý.
- [ ] Step/Next/Previous/Reset/Replay chạy đúng thứ tự và tái lập được cùng trạng thái.
- [ ] Sơ đồ, panel, code highlight và event log không mâu thuẫn.
- [ ] Có thể dừng ở trạng thái trung gian, đọc hết nhãn và khôi phục sau khi quay lại tab.
- [ ] Có câu hỏi dự đoán hoặc tự nhớ ở chỗ phù hợp, không biến mọi bước thành quiz gây gián đoạn.

### Đẹp và mượt có chủ đích

- [ ] Chuyển động có điểm đầu, mục tiêu và điểm dừng; không lặp vô hạn hoặc rung nhấp nháy.
- [ ] Không có hai camera/particle/zoom effects cạnh tranh nhau.
- [ ] Text không bị cắt khi vi/en, phóng to chữ, hoặc ở viewport hẹp.
- [ ] Trạng thái khởi tạo/đích đến hiện rõ khi animation bị tắt.
- [ ] Hiệu ứng không làm che cạnh, nhãn, focus ring hoặc điều khiển.
- [ ] Kiểm tra trên màn hẹp, desktop, light/dark, keyboard-only và reduced motion.

### Hợp đồng dự án

- [ ] Không thêm CDN, webfont, fetch, module, framework, package manager, build step hoặc thư viện ngoài nếu master prompt chưa đổi.
- [ ] Model vẫn thuần; view nằm đúng track; lõi không có nhánh đặc biệt cho một track.
- [ ] Cùng một state model phục vụ Guided Deep-Dive, Live Explorer, route restore và song ngữ.
- [ ] Toàn bộ chuỗi hiển thị vẫn có cặp vi/en cùng key; đổi ngôn ngữ giữ nguyên vị trí mô phỏng.
- [ ] Các quyết định mới không ghi đè design tokens, source-of-truth hoặc quyết định đã chốt trong Claude-owned docs.

## 9. Nguồn đã tham khảo

### Hai trang mẫu

- [Designed to Scale](https://designed-to-scale.vercel.app/)
- [Protocol Explorer](https://protocol-explorer-alpha.vercel.app/)

### Tài liệu chính thức Android/Compose

- [Animations in Compose — introduction](https://developer.android.com/develop/ui/compose/animation/introduction)
- [Quick guide to Animations in Compose](https://developer.android.com/develop/ui/compose/animation/quick-guide)
- [Advanced animation in Compose](https://developer.android.com/develop/ui/compose/animation/advanced)
- [Testing animations](https://developer.android.com/develop/ui/compose/animation/testing)
- [Compose performance](https://developer.android.com/develop/ui/compose/performance)
- [Compose semantics and accessibility](https://developer.android.com/develop/ui/compose/accessibility/semantics)

Các trang Android ở trên được dùng để giữ đúng cách nói về API/motion Compose. Hướng dẫn về chất lượng animation web lấy từ web.dev; không suy ra rằng animation của website sử dụng cùng runtime hay API với Compose.

### Motion, web performance và accessibility

- [How to create high-performance CSS animations — web.dev](https://web.dev/articles/animations-guide)
- [W3C Media Queries Level 5: prefers-reduced-motion](https://www.w3.org/TR/mediaqueries-5/#prefers-reduced-motion)
- [MDN: prefers-reduced-motion](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/@media/prefers-reduced-motion)
- [WCAG 2.2 SC 2.3.3: Animation from Interactions](https://www.w3.org/WAI/WCAG22/Understanding/animation-from-interactions.html)
- [WCAG SC 2.2.2: Pause, Stop, Hide](https://www.w3.org/WAI/WCAG22/Understanding/pause-stop-hide.html)

### Học sâu

- [Learning methods, evidence notes and application to Android tracks](androidbooks-knowledge/learning-methods.md)
- Dunlosky et al. (2013), [Improving Students’ Learning With Effective Learning Techniques](https://journals.sagepub.com/stoken/rbtfl/Z10jaVH/60XQM/full)
- Roediger & Karpicke (2006), [Test-Enhanced Learning](https://doi.org/10.1111/j.1467-9280.2006.01693.x)
- Cepeda et al. (2006), [Distributed Practice in Verbal Recall Tasks](https://pubmed.ncbi.nlm.nih.gov/16719566/)
- Agarwal, Nunes & Blunt (2021), [Retrieval Practice Consistently Benefits Student Learning](https://doi.org/10.1146/annurev-psych-010419-051019)

### Tài liệu dự án liên quan — chỉ đọc, không sửa trong tác vụ này

- CLAUDE.md
- docs/design-principles.md
- docs/core-api.md
- docs/checklist.md
- docs/research/ui.md, docs/research/animation.md, docs/research/global.md
- docs/androidbooks-knowledge/learning-methods.md
- E:/AndroidDeepDiveExplorer-Prompts/00-MASTER-PROMPT.md
- E:/AndroidDeepDiveExplorer-Prompts/STYLE-REFERENCE.md
- E:/AndroidDeepDiveExplorer-Prompts/CONSTRAINTS-CHECKLIST.md
