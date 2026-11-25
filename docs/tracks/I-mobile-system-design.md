# TRACK I — Thiết kế hệ thống phía mobile / Mobile System Design (`sysdesign`)

> **ĐÃ DUYỆT (2026-11-24).** Hai câu hỏi cuối theo mặc định (người dùng đổi được): **giữ i2 và i3 riêng**, **bài mẫu là app nhắn tin**. **ĐÃ XÂY XONG 2026-11-24** (I0–I13, stable).
> Nguyên tắc: **cần và đủ**, nhìn từ phía **app Android** (client). Mỗi chương bắt đầu từ một lỗi thật xảy ra khi app nói chuyện với server, hoặc khi app sống trong giới hạn của điện thoại.

**Trạng thái (2026-11-24):** đã làm xong I0–I13, track chuyển sang `stable`. I9 làm nhẹ theo quyết định người dùng (FCM chỉ là ví dụ).

## Manifest đề xuất
| Trường | Giá trị |
|---|---|
| id / code / order | `sysdesign` / I / 90 |
| domain | engineering |
| Tên vi / en | Thiết kế hệ thống phía mobile / Mobile System Design |
| level / estMinutes | advanced / 400 |
| prerequisites | [] (nên đọc G1–G4 và Coroutines trước) |
| status | `draft` trong lúc viết, `stable` sau i0 |
| Ví dụ xuyên suốt | App hư cấu "Hẹn Khám" có thêm nhắn tin với phòng khám, ảnh hồ sơ và thông báo nhắc lịch |

## Nguồn đã đọc để soạn dàn ý (chỉ mục lục, chưa đọc thân chương)
- **Chính thức (thắng khi mâu thuẫn), đã kiểm HTTP 200 ngày 2026-11-24:**
  - developer.android.com:
    - Processes and app lifecycle, Memory overview, ANR;
    - App startup time, App startup analysis and optimization;
    - Persistent work (WorkManager), Optimize battery, Power;
    - Managing network usage, Reading network state;
    - Paging 3 overview, Offline-first;
    - Loading large bitmaps;
    - Reduce app size;
    - In-app updates.
  - Firebase Cloud Messaging: tổng quan, loại message (notification so với data), nhận message trên Android, quản lý token.
  - RFC 9111 (HTTP Caching).
  - Play Console: staged rollout (support.google.com).
- **Sách:**
  - Tjeerd in 't Veen, *Mobile System Design* (Resourceful Engineering).
    - Bản **early release**, có ch.1–14 trong tổng số các chương dự kiến.
    - Ch.2 "Turning a briefing into a strong plan": phác "landscape", yêu cầu phụ, hỏi designer và backend (session, token, lỗi, push, deep link).
    - Ch.3: holistic-driven development.
    - Ch.4–5: kiểm thử.
    - Ch.6–8: DI.
    - Ch.9–12: UI.
    - Ch.13–14: feature tự chứa.
  - Alex Xu, *System Design Interview* tập 1:
    - ch.1–3: scale, ước lượng nhanh, khung bốn bước phỏng vấn;
    - ch.10 notification, ch.11 news feed, ch.12 chat, ch.14 YouTube, ch.15 Google Drive.
  - Alex Xu, Sahn Lam, tập 2:
    - ch.1–13 đều là hệ thống backend (proximity, message queue, metrics, payment, wallet…);
    - chỉ ch.11 Payment liên quan tới idempotency.
  - Zhiyong Tan, *Acing the System Design Interview*:
    - ch.1: thiết kế là chuyện đánh đổi;
    - ch.3: yêu cầu phi chức năng;
    - ch.4–6: database, transaction phân tán, dịch vụ chung;
    - ch.7–16: các bài mẫu, gồm ch.9 notification, ch.14 nhắn tin, ch.16 news feed.
  - Kleppmann, *Designing Data-Intensive Applications*, bản 1 và bản 2. Bản 2 có các chương:
    - ch.1 đánh đổi, ch.2 yêu cầu phi chức năng, ch.3 mô hình dữ liệu;
    - ch.4 lưu trữ, ch.5 **encoding và evolution**, ch.6 **replication**;
    - ch.8 transaction, ch.9 **trục trặc của hệ phân tán** (mạng không tin cậy, đồng hồ), ch.10 nhất quán và đồng thuận;
    - ch.11–13 xử lý lô và luồng.
  - Silberschatz và cộng sự, *Operating System Concepts*. Chỉ dùng ch.3 Processes, ch.4 Threads, ch.6–8 Synchronization và Deadlocks, ch.9–10 Memory.
  - Geewax, *API Design Patterns*. Mục lục epub chỉ hiện tới ch.11; dùng ch.7 Standard methods, ch.10 Long-running operations. Chương phân trang và chống gửi trùng (nếu có) **chưa đọc được nên không trích**.

## Điểm cần nói rõ trong track
- **Phần lớn sách "system design" trong kho là sách backend** (Xu hai tập, Acing, DDIA).
  - Track lấy từ đó những **khái niệm** cần cho client: timeout, retry, idempotency, replication và xung đột, tương thích phiên bản, cache.
  - Góc nhìn client là **diễn giải của site**, có ghi rõ ở mỗi chương. Ví dụ: Xu ch.12 thiết kế server chat, còn site rút ra phía app cần gì.
- **Cơ chế riêng của Android** (process bị giết, LMK, ANR, WorkManager, FCM, bitmap) lấy từ **developer.android.com**, không lấy từ sách.
- **Khung bốn bước phỏng vấn là framework của Alex Xu**, ghi tên tác giả.
  - Sách Tjeerd là bản early release, chủ yếu nói về quy trình, DI và UI.
  - Chỉ dùng ch.2 của Tjeerd cho bước "từ đề bài tới kế hoạch".
- **Con số:**
  - "Latency numbers" của Xu ch.2 là số tham khảo đã cũ, ghi rõ là ước lượng;
  - con số trong sim là minh họa, không phải số đo.

## IN (đưa vào) và lý do
| Nội dung | Lý do |
|---|---|
| Từ đề bài tới kế hoạch: yêu cầu chức năng, phi chức năng, ràng buộc của điện thoại, ước lượng nhanh | Lỗi hay gặp nhất: thiết kế chỉ cho đường thuận (mạng tốt, pin đầy, app luôn sống) |
| Tiến trình, luồng, bộ nhớ trên Android (từ OS Concepts tới LMK, process death, ANR) | Gốc của nhiều lỗi "lúc có lúc không": app bị giết ở nền, main thread bị chặn |
| Đồng bộ hóa và deadlock | Main thread chờ khóa thì thành ANR; khóa sai thứ tự thì treo hẳn |
| Chọn kênh giao tiếp: request/response, polling, long polling, SSE, WebSocket, push | Chọn sai thì hao pin hoặc tin đến chậm |
| Mạng không tin cậy: timeout, retry, backoff, jitter, idempotency | Lỗi đặt lịch hai lần do retry sau timeout |
| Cache: bộ nhớ, đĩa, HTTP (Cache-Control, ETag, 304), vô hiệu hóa | Giá mới không hiện vì cache; hoặc không cache gì nên chậm và tốn dữ liệu |
| Phân trang: offset so với cursor | Mục bị lặp hoặc mất khi dữ liệu mới chèn vào giữa lúc cuộn |
| Đồng bộ nhiều thiết bị và xung đột | Sửa trên máy tính bảng bị điện thoại ghi đè |
| Thông báo đẩy (FCM) và thời gian thực | Thông báo không tới khi app bị tắt; token cũ |
| Ảnh và tệp lớn: tải theo kích thước hiển thị, upload theo khúc có thể tiếp tục | OOM khi hiện ảnh gốc; upload 200 MB hỏng ở 95% phải làm lại |
| Khởi động, pin, kích thước app | Tiêu chí phi chức năng mà người dùng cảm nhận trực tiếp |
| Quan sát, feature flag, phát hành từng phần, tương thích phiên bản API | App cũ vẫn chạy nhiều tháng; không thể ép mọi người cập nhật |
| Một bài mẫu từ đầu tới cuối (app nhắn tin) | Gom mọi chương lại theo đúng trình tự một buổi thiết kế |

## OUT (bỏ ra hoặc chỉ nhắc) và lý do
| Nội dung | Lý do |
|---|---|
| Scale backend: load balancer, sharding, consistent hashing, key-value store, ID generator, crawler, URL shortener, message queue, stock exchange… (Xu, Acing) | Là phía server; client chỉ cần biết hệ quả (lỗi 5xx, rate limit 429, độ trễ) |
| DDIA: transaction chi tiết, đồng thuận, xử lý lô và luồng | Phía server; transaction trên máy thuộc track **H** (Room) |
| Tjeerd ch.4–8 (kiểm thử, DI) | Đã có ở track **G** (g6, g10) |
| Tjeerd ch.9–12 (UI framework, tách thiết kế thành view) | Thuộc UI/kiến trúc UI; track UI đang tạm dừng |
| OS Concepts: file system, mass storage, ảo hóa, bảo mật, lập lịch CPU chi tiết | Không áp dụng trực tiếp cho app Android |
| Lưu trên máy (Room, DataStore, hàng đợi thao tác offline) | Thuộc track **H** (h4–h7) |
| Repository, SSOT | Thuộc track **G** (g4) |
| GraphQL, gRPC chi tiết | Chỉ một dòng trong bảng so sánh kênh |
| Thư viện cụ thể (Retrofit, OkHttp, Coil, Glide) | Chỉ nhắc tên; dạy cơ chế, không dạy API thư viện |
| iOS, đa nền tảng | Ngoài phạm vi |
| Kỹ năng mềm khi phỏng vấn | Chỉ phần khung đặt câu hỏi ở i1 |

## Chương (14)
Cột **Hình chính** là tab mặc định; sơ đồ node của sim ở tab phụ.
- **Sơ đồ tuần tự MỚI** là hình chủ đạo của track này, vì client và server trao đổi theo thời gian, và lỗi nằm ở chỗ tin bị mất, trùng hay đến muộn.
- Viết sơ đồ này một lần, dùng lại ở i4, i5, i8, i9, i13 (và h7).

### Phần 1: Điện thoại là một môi trường khắc nghiệt
| Id | Chương | Lỗi dẫn dắt | Sim | Hình chính (vì sao hợp) | Nguồn chính |
|---|---|---|---|---|---|
| i1 | Từ đề bài tới kế hoạch | Thiết kế chỉ cho mạng tốt; bỏ quên trạng thái lỗi, rỗng, mất mạng | `sysdesign.plan`: đề bài → câu hỏi → yêu cầu → ước lượng → bản phác | (1) **Bảng** yêu cầu × câu hỏi cần hỏi designer/backend. (2) **Bảng tính** ước lượng nhanh (ảnh mỗi ngày × kích thước = dung lượng), kèm ví dụ kiểm chứng | Tjeerd ch.2; Xu tập 1 ch.2–3 (khung của Xu); Acing ch.1, ch.3 |
| i2 | Tiến trình, bộ nhớ và cái chết của process | Quay lại app sau khi chụp ảnh thì form trống; app nền bị giết | `sysdesign.process`: app đi từ foreground → nền → bị LMK giết → người dùng quay lại | (1) **Dãy ô dọc** bậc ưu tiên tiến trình, app tụt bậc theo thời gian. (2) **Thanh bộ nhớ** khi hệ thống thiếu RAM | Processes and app lifecycle; Memory overview; OS Concepts ch.3, ch.9–10 |
| i3 | Luồng, khóa, ANR và deadlock | Main thread chờ khóa đang bị luồng nền giữ thì ANR; hai khóa lấy ngược thứ tự thì treo | `sysdesign.lock`: hai luồng, hai khóa, hai thứ tự lấy | (1) **Làn thời gian** hai luồng, đoạn chờ tô đậm, mốc ANR. (2) **Đồ thị chờ** (đồ thị phụ thuộc MỚI, dùng chung với G): có vòng là có deadlock | ANR; OS Concepts ch.4, ch.6–8; Clean Code ch.13 (nguồn phụ, bổ sung 2026-11-24); Coroutines (Mutex, cầu nối) |

### Phần 2: Client nói chuyện với server
| Id | Chương | Lỗi dẫn dắt | Sim | Hình chính (vì sao hợp) | Nguồn chính |
|---|---|---|---|---|---|
| i4 | Chọn kênh giao tiếp | Polling 5 giây một lần làm hao pin; tin nhắn đến trễ cả phút | `sysdesign.channel`: polling, long polling, SSE, WebSocket, push cho cùng một tin nhắn | **Sơ đồ tuần tự MỚI** cho từng kênh: số lần radio bật và độ trễ tin hiện ngay trên hình; kèm **bảng** so sánh | Xu tập 1 ch.12; Acing ch.14; Managing network usage; Optimize battery |
| i5 | Mạng không tin cậy | Bấm "Đặt lịch", timeout, app tự thử lại, server tạo hai lịch | `sysdesign.retry`: request mất, response mất, retry không key, retry có idempotency key | (1) **Sơ đồ tuần tự**: thấy được response mất khác request mất. (2) **Làn thời gian** backoff tăng dần có jitter | DDIA bản 2 ch.9; Xu tập 2 ch.11 (idempotency); Persistent work (backoff của WorkManager) |
| i6 | Cache | Giá khám đã đổi nhưng app vẫn hiện giá cũ; hoặc mỗi lần mở đều tải lại toàn bộ | `sysdesign.cache`: tra bộ nhớ → đĩa → mạng; header Cache-Control, ETag, 304 | (1) **Luồng có nhánh** trúng hay trượt ở từng tầng. (2) **Bảng** header → hành vi của cache | RFC 9111; Xu tập 1 ch.1 (cache) |
| i7 | Phân trang | Cuộn danh sách tin tức thấy một bài hai lần, hoặc mất một bài | `sysdesign.paging`: offset so với cursor khi có bài mới chèn lên đầu | **Dãy ô** danh sách trên server và các trang app đã tải; bài chèn vào làm lệch offset nên ô bị lặp tô đỏ | Acing ch.12 (12.7.1, trang lệch khi thêm ở đầu); AIP-158; Paging 3 (overview, paged data, network + db); SubcomposeLayout.kt (key trùng). Xu tập 1 không có phần phân trang nên không trích |
| i8 | Nhiều thiết bị và xung đột | Sửa ghi chú trên máy tính bảng, điện thoại còn bản cũ gửi lên ghi đè | `sysdesign.conflict`: last-write-wins, ghi có điều kiện theo phiên bản, gộp theo trường | (1) **Làn thời gian** hai thiết bị và server. (2) **Bảng** gộp từng trường của bản ghi | DDIA bản 2 ch.6 (multi-leader, xử lý xung đột), ch.9 (đồng hồ không tin được); Xu tập 1 ch.15 |
| i9 | Thông báo đẩy | Đổi giờ khám nhưng thông báo hiện giờ cũ; đổi máy thì không nhận được nữa | `sysdesign.push`: push mang nội dung, push chỉ báo thay đổi, push mất, push trùng | **Sơ đồ tuần tự** server, dịch vụ đẩy, app; kèm **bảng** điều không được bảo đảm → thiết kế đáp lại. Theo quyết định người dùng 2026-11-24: FCM chỉ làm nhẹ, dạy tư duy | Xu tập 1 ch.10; FCM (chỉ nhắc: thứ tự, gộp, vài giây, ID cũ); quyền POST_NOTIFICATIONS |
| i10 | Ảnh và tệp lớn | Danh sách ảnh gây OOM; upload 200 MB hỏng ở 95% phải làm lại từ đầu | Hai sim: `sysdesign.bitmap` (giải mã gốc so với inSampleSize) và `sysdesign.upload` (một request so với tiếp tục được) | (1) **Bảng tính** bộ nhớ bitmap + bảng vòng lặp calculateInSampleSize. (2) **Dãy ô** các khúc upload: giữ, mất, gửi dở | Loading large bitmaps; Bitmap.Config; UIDT; Xu tập 1 ch.14–15; IETF draft resumable upload (bản 16) |

### Phần 3: Vận hành và một bài mẫu
| Id | Chương | Lỗi dẫn dắt | Sim | Hình chính (vì sao hợp) | Nguồn chính |
|---|---|---|---|---|---|
| i11 | Khởi động, pin, kích thước | Mở app mất 4 giây vì khởi tạo mọi SDK trong Application.onCreate | `sysdesign.startup`: cold, warm, hot start; dời việc ra khỏi đường khởi động | **Làn thời gian** khởi động (process, Application, Activity, khung hình đầu): việc chặn hiện thành thanh | App startup time; Startup analysis; Power; Reduce app size |
| i12 | Quan sát và phát hành an toàn | Bản mới lỗi ở 3% số máy, đã phát hành 100%; API mới làm app cũ crash | `sysdesign.rollout`: phát hành theo phần trăm, feature flag tắt từ xa; app cũ gọi API mới | (1) **Dãy ô** tỉ lệ phát hành theo ngày. (2) **Ma trận** phiên bản app × phiên bản API: ô không tương thích tô đỏ | Staged rollout; In-app updates; DDIA bản 2 ch.5 (tương thích xuôi và ngược); Seemann A.11 (feature flag), A.21 (semantic versioning) |
| i13 | Bài mẫu: app nhắn tin với phòng khám | Gom mọi thứ: gửi tin lúc mất mạng, nhận tin khi app tắt, cuộn lịch sử | `sysdesign.chat`: một tin đi từ lúc gõ tới lúc có dấu "đã xem" | (1) **Đồ thị thành phần** của app (đồ thị phụ thuộc MỚI). (2) **Sơ đồ tuần tự** một tin gửi lúc mất mạng | Xu tập 1 ch.12; Acing ch.14; Tjeerd ch.2 |
| i0 | Bản đồ track (viết CUỐI) | Gặp triệu chứng X thì đọc chương nào | `sysdesign.map` | **Bảng tra** triệu chứng → chương | — |

Khuôn mỗi chương như track Kotlin:
- tối đa 8 mục;
- 2 lỗi thật;
- 1 bài tập;
- quiz 3–4 câu.

Bài tập là đề thiết kế nhỏ do site tự viết theo ý sách. Lời giải dạng bảng: câu hỏi cần hỏi, lựa chọn, đánh đổi.

## Cầu nối dự kiến
- i2 ↔ G g1 và g3 (ViewModel không sống qua process death; SavedStateHandle).
- i3 ↔ Coroutines (Mutex, Dispatchers, luồng Main).
- i5, i10 ↔ H h7 (WorkManager, hàng đợi gửi lại).
- i6 ↔ G g4 (DB là SSOT, cache HTTP là chuyện khác).
- i8 ↔ H h7.
- i12 ↔ J (feature flag, semantic versioning).

## Hai câu hỏi đã có mặc định (người dùng đổi được)
1. Giữ i2 và i3 là hai chương riêng, track 14 chương.
2. Bài mẫu i13 là app nhắn tin với phòng khám.
