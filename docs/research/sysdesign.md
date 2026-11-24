# Nghiên cứu track I (Thiết kế hệ thống phía mobile)

> Track đã duyệt 2026-11-24, đang viết. Dàn ý: `docs/tracks/I-mobile-system-design.md`. Nguồn chính thức thắng khi mâu thuẫn.

## Đã đọc để soạn dàn ý (2026-11-24, chỉ mục lục)
- **Tjeerd in 't Veen, *Mobile System Design*:** bản early release, ch.1–14 (đọc mục lục bằng pdftotext các trang đầu).
- **Alex Xu, *System Design Interview*:**
  - tập 1 (PDF): ch.1–16;
  - tập 2 (epub): ch.1–13, đều là hệ thống backend.
- **Zhiyong Tan, *Acing the System Design Interview* (PDF):** ch.1–16. Tiêu đề lấy từ trang mục lục, vài chương đọc không trọn.
- **Kleppmann, *Designing Data-Intensive Applications*:**
  - bản 2 (PDF): ch.1–13, mục lục in thiếu dòng ch.7;
  - bản 1: chưa mở.
- **Silberschatz và cộng sự, *Operating System Concepts*:** ch.1–18 (trang mục lục).
- **Geewax, *API Design Patterns*:** mục lục epub chỉ hiện tới ch.11.
- **URL chính thức kiểm HTTP 200 bằng curl ngày 2026-11-24:**
  - developer.android.com:
    - process-lifecycle, memory-overview, vitals/anr;
    - vitals/launch-time, appstartup/analysis-optimization;
    - background-tasks/persistent, optimize-battery, performance/power;
    - network-ops/managing, reading-network-state;
    - paging/v3-overview, offline-first;
    - graphics/load-bitmap, reduce-apk-size;
    - playcore/in-app-updates.
  - firebase.google.com: cloud-messaging, set-message-type, android/receive-messages, manage-tokens.
  - Khác: rfc-editor.org/rfc/rfc9111; support.google.com (staged rollout, answer 6346149).
  - Đã đổi sang trang khác: `firebase.google.com/docs/cloud-messaging/concept-options` trả 404.

## Bảng nguồn theo chương
Điền khi viết từng chương. Ghi rõ chỗ nào là diễn giải của site từ sách backend sang phía client.

### I1 · Từ đề bài tới kế hoạch
Sách đọc bằng pdftotext ngày 2026-11-24 (Xu tập 1 ch.2 dòng "Tips", ch.3 bốn bước; Tjeerd ch.2 mục 2.4, 2.5.3, 2.5.4, 2.5.8, 2.6.1, 2.6.3, 2.6.7). URL nguồn sách kiểm 200: bytebytego.com, mobilesystemdesign.com.
| Khẳng định | Nguồn | Loại |
|---|---|---|
| Khung bốn bước; đừng trả lời ngay, hỏi và ghi giả định; thiết kế quá mức là dấu hiệu xấu | book-xu1 ch.3 | guideline |
| Ước lượng nhanh: quá trình hơn độ chính xác; làm tròn, ghi giả định, ghi đơn vị | book-xu1 ch.2 | guideline |
| Đừng mở IDE ngay, tìm yêu cầu phụ; thiết kế chỉ trường hợp đẹp, xin bản nội dung xấu nhất; bàn lỗi sớm, lỗi không chặn màn hình; không phải mọi phần ưu tiên như nhau | book-tjeerd ch.2 | guideline |
| Backend: phiên, token, timeout; mã lỗi để client dịch; thông báo đẩy và ngôn ngữ của máy | book-tjeerd ch.2 | guideline |
| Câu hỏi mất mạng / rỗng; mọi con số (2 ảnh, 4 MB, 300 KB, 240 / 18 MB) | site | simplified |

### I2 · Tiến trình, bộ nhớ và cái chết của process
Đọc ngày 2026-11-24 qua agent web-fetch (các trang trả 200): process-lifecycle, activity-lifecycle, memory-overview, saving-states, training/basics/intents/result, reference ComponentCallbacks2, source.android.com lmkd; adb (curl, mục `am kill`). OS Concepts bản 10 đọc bằng pdftotext (mục 3.3.2.1, 9.5.3, OOM killer ở 10.x). URL sách os-book.com/OS10 trả 200.
| Khẳng định | Nguồn | Loại |
|---|---|---|
| Bốn bậc foreground, visible, service, cached và ví dụ từng bậc; giết cached trước, foreground là phương án cuối | ax-process-lifecycle | stable |
| Bind (BIND_AUTO_CREATE) hay ContentProvider: process được dùng quan trọng ít nhất bằng process dùng nó; Service chạy khoảng 30 phút trở lên có thể bị hạ xuống cached; thứ tự danh sách cached là chi tiết cài đặt | ax-process-lifecycle | stable |
| BroadcastReceiver mở luồng rồi trả về thì luồng có thể chết theo process; dùng JobService; Android 13: process cached có thể không được cấp thời gian chạy | ax-process-lifecycle | stable |
| Hệ thống không giết trực tiếp Activity, nó giết process; quay lại thì Activity được tạo lại từ dữ liệu đã lưu | ax-activity-lifecycle | stable |
| Vùng nhớ đã sửa luôn ở RAM, chỉ phần không sửa (mã) bị bỏ ra; process cached có thể bị giết bất cứ lúc nào | ax-memory-overview | stable |
| lmkd ở userspace (Android 9+), driver kernel bị gỡ từ kernel 4.12, PSI từ Android 10; ro.lmk.medium mặc định 800 (cached, dịch vụ không thiết yếu) | aosp-lmkd | version |
| Từ API 34 chỉ còn TRIM_MEMORY_UI_HIDDEN và TRIM_MEMORY_BACKGROUND; mức khác và onLowMemory() không được gọi, deprecated ở API 35; so sánh bằng >= | ax-trim-memory | version |
| ViewModel / saved state / lưu trữ bền: bảng sống qua đổi cấu hình, process death, người dùng đóng hẳn; saved state chỉ dữ liệu nhỏ, lưu lúc onStop, bản sao ngoài process | ax-saving-states | stable |
| Camera: process và Activity gần như chắc chắn bị hủy; đăng ký callback vô điều kiện mỗi lần tạo; lưu riêng trạng thái để xử lý kết quả | ax-activity-result | stable |
| `am kill <package>` chỉ giết process an toàn để giết | ax-adb | stable |
| Năm bậc process của Android (foreground, visible, service, background, empty); mobile không swap vì flash; Android giết process | book-osc 3.3.2.1, 9.5.3 | guideline |
| **Mâu thuẫn:** sách nói Android ghi trạng thái app ra flash trước khi giết; tài liệu nói bản sao saved state nằm trong bộ nhớ ngoài process. Site theo tài liệu | ax-saving-states thắng | — |
| RAM 4 GB, các khối MB, app khác bị giết trước; ví dụ form đặt lịch và thẻ bảo hiểm; mã minh họa | site | simplified |

### I3 · Luồng, khóa, ANR và deadlock
Đọc ngày 2026-11-24 qua agent web-fetch (cả ba trang trả 200). Ghi lại để phiên sau viết ngay, không cần tải lại:
- **vitals/anr:** ANR khi không phản hồi sự kiện nhập trong 5 giây; startForegroundService mà không gọi startForeground trong 5 giây; BroadcastReceiver chưa xong trong 10 giây nếu app có Activity ở foreground (trang không ghi số cho trường hợp nền); Service onCreate/onStartCommand/onBind và JobService onStartJob/onStopJob "vài giây" (không có số). Nguyên nhân thường gặp: I/O chậm hay tính toán dài trên main thread, binder đồng bộ chậm, main thread chờ khối synchronized do luồng khác giữ lâu, deadlock (luồng A chờ tài nguyên B giữ, B chờ tài nguyên A giữ). Cách sửa gợi ý: thay khóa nguyên thủy bằng Mutex.withLock của coroutine (treo chứ không chặn UI thread); I/O qua withContext(Dispatchers.IO); onReceive ngắn, việc dài giao WorkManager. Công cụ: StrictMode, ApplicationExitInfo (Android 11+), trace trong /data/anr/.
- **kotlinx.coroutines Mutex (1.11.0):** không reentrant (coroutine đang giữ khóa gọi lock lần nữa thì tự treo); lock() là hàm suspend, không chặn luồng; withLock; tryLock trả false; unlock sai chủ thì IllegalStateException; trang không nói gì về tính công bằng.
- **processes-and-threads:** main thread (UI thread) phát sự kiện tới widget, chạy callback vòng đời; hai quy tắc: không chặn UI thread, không đụng UI toolkit từ luồng khác; chặn "vài giây" thì hiện hộp thoại ANR (trang không ghi số); lời gọi IPC (bound service, ContentProvider) chạy trên binder thread pool nên phải thread-safe.
- **Sách:** OS Concepts bản 10 ch.6 (race condition, critical section, mutex lock), ch.8 (bốn điều kiện cần của deadlock, đồ thị cấp phát tài nguyên, chống vòng chờ bằng thứ tự khóa toàn cục; đọc thân chương khi viết). Clean Code ch.13 (giới hạn phạm vi dữ liệu, dùng bản sao, giữ đoạn synchronized nhỏ, cẩn thận phụ thuộc giữa các phương thức synchronized) là nguồn phụ.
- **Dự định sim `sysdesign.lock`:** ba cách (main thread chờ khóa luồng nền giữ lâu → ANR ở mốc 5 giây; hai luồng lấy hai khóa ngược thứ tự → deadlock, đồ thị chờ có vòng; cùng thứ tự khóa hoặc Mutex.withLock → không vòng). Hình: làn thời gian hai luồng + đồ thị chờ (vẽ bằng SVG như `.vz-dg` của track G).
- **Đã viết (2026-11-24):** sim `sysdesign.lock` với ba cách `hold`, `cycle`, `order`; hình chính là làn thời gian SVG (`.vz-tl-*`), đồ thị chờ (`.vz-wf` dùng lại `.vz-dg-*`) và bảng bốn điều kiện. Dùng lại nguồn `ax-anr` (track H), `and-threads`, `kx-mutex` (track Coroutines); `book-osc` thêm ch.6, ch.8. Clean Code ch.13 không trích trên site (URL nhà xuất bản trả 403 với curl).
| Khẳng định | Nguồn | Loại |
|---|---|---|
| Ngưỡng ANR: nhập 5 giây; startForeground 5 giây; BroadcastReceiver 10 giây khi có Activity foreground; Service, JobService "vài giây". Nguyên nhân: I/O, tính toán, binder, chờ khóa, deadlock. Cách sửa: Mutex.withLock, Dispatchers.IO; công cụ StrictMode, ApplicationExitInfo, /data/anr | ax-anr | stable |
| Main thread = UI thread; đừng chặn UI thread; đừng đụng UI từ luồng khác; IPC chạy trên binder thread pool | and-threads | stable |
| Mutex không reentrant; lock() là suspend, không chặn luồng | kx-mutex | stable |
| Race condition, critical section; ví dụ hai mutex ngược thứ tự phụ thuộc lịch CPU; bốn điều kiện; đồ thị chờ; Linux, Windows bỏ qua deadlock của app; thứ tự khóa toàn cục | book-osc ch.6, 8.2, 8.3.1, 8.4, 8.5.4, 8.7.1 | guideline |
| Hai khóa cacheLock/dbLock, mọi mốc thời gian (chạm giây 1, ghi DB 6 giây, chờ 200 ms), bài tập ba khóa | site | simplified |

### I4 · Chọn kênh giao tiếp
Đọc ngày 2026-11-24 qua agent web-fetch (mọi trang trả 200): network-access-optimization, doze-standby, firebase cloud-messaging (tổng quan), android/message-priority, customize-messages/collapsible-message-types, MDN Using server-sent events, MDN WebSockets API. Xu tập 1 ch.12 đọc bằng pdftotext.
| Khẳng định | Nguồn | Loại |
|---|---|---|
| Gửi qua HTTP là đủ; nhận cần polling (tốn vì phần lớn rỗng), long polling (giữ tới khi có tin hay hết hạn; ba nhược điểm phía server), WebSocket (HTTP rồi nâng cấp, hai chiều, sống lâu; server phải quản lý kết nối) | book-xu1 ch.12 | guideline |
| Radio (ví dụ 3G): cao, thấp (~50%), chờ; thêm 5 giây cao + 12 giây thấp sau mỗi lần truyền (~18 giây); thức dậy >2 giây; ví dụ 3 lần/phút so với gom 1 lần; gom, tải trước, kiểm kết nối, dùng lại kết nối | ax-network-access | version |
| Doze: tạm dừng mạng, bỏ qua wake lock, hoãn alarm, JobScheduler, WorkManager; cửa sổ bảo trì thưa dần; App Standby; khuyên FCM thay kết nối riêng (một kết nối chung); RemoteNotification đánh thức app; Play hạn chế miễn trừ | ax-doze | stable |
| Payload ≤ 4096 byte; server/Cloud Functions gửi, app nhận qua dịch vụ nền tảng | fcm-overview | stable |
| Ưu tiên thường có thể chờ hết Doze; cao thì giao ngay, đánh thức, nên dẫn tới thông báo, nếu không có thể bị hạ; onMessageReceived vài giây | fcm-priority | version |
| Không bảo đảm thứ tự; gộp được: tối đa 4 khóa mỗi máy; không gộp: Android quá 100 thì bỏ hết, app phải đồng bộ lại | fcm-collapsible | stable |
| SSE một chiều, text/event-stream, tự nối lại, retry; WebSocket hai chiều, API không có backpressure | mdn-sse, mdn-websocket | stable |
| Chu kỳ 5 giây, tin ở giây 7, hạn chờ 30 giây, "gần như ngay", bảng so sánh, cách phối hợp WebSocket + FCM, độ trễ polling = nửa chu kỳ | site | simplified |
| Trang network-access-optimization **không** nói về polling hay FCM; khẳng định "dùng FCM thay kết nối riêng" lấy từ trang Doze | — | ghi chú |

### I5 · Mạng không tin cậy
Đọc ngày 2026-11-24: DDIA bản 2 bằng pdftotext (ch.2 hộp "When an Overloaded System Won't Recover", ch.9 "Unreliable Networks", ch.12 idempotence); qua agent web-fetch: WorkManager define-work, bản nháp IETF Idempotency-Key 09 (200). Bài AWS của Marc Brooker: agent chỉ lấy được phần điều hướng, **chưa đọc thân bài**, chỉ nhắc qua lời dẫn của DDIA. RFC 9110 (rfc-editor, 200) dùng cho mục 9.2.2.
| Khẳng định | Nguồn | Loại |
|---|---|---|
| Không response thì không phân biệt được request mất, server sập, response mất; timeout vẫn không biết server đã nhận chưa | book-ddia2 ch.9 | guideline |
| Idempotent: làm nhiều lần như một lần; ví dụ xóa khóa và tăng bộ đếm; làm idempotent bằng siêu dữ liệu | book-ddia2 ch.12 | guideline |
| Retry storm, lỗi metastable; tăng và ngẫu nhiên hóa khoảng thử (exponential backoff), circuit breaker | book-ddia2 ch.2 | guideline |
| PUT, DELETE, phương thức an toàn là idempotent; không tự thử lại request không idempotent | rfc9110 9.2.2 | stable |
| Idempotency-Key: chuỗi duy nhất (UUID), POST/PATCH; không dùng lại cho nội dung khác; đã xong → response nhất quán; đang xử lý → 409; khác nội dung → 422 | ietf-idem-key (bản 09) | version |
| Result.retry(), LINEAR/EXPONENTIAL, mặc định EXPONENTIAL 30 giây, tối thiểu 10 giây, ví dụ ~20, 40, 80 giây | ax-define-work | stable |
| Key sinh một lần và lưu cùng bản nháp; timeout 10 giây; giá trị jitter; đỉnh trong nửa giây; bài tập 5 thao tác | site | simplified |

### I6 · Cache
Đọc ngày 2026-11-24: RFC 9111 và RFC 9110 qua agent web-fetch (200; mục 8.8.1, 8.8.3, 13.1.2 của RFC 9110 lấy theo bản tóm tắt của công cụ, chưa thấy nguyên văn); Xu tập 1 ch.1 "Considerations for using cache" bằng pdftotext.
| Khẳng định | Nguồn | Loại |
|---|---|---|
| Tươi/cũ; thứ tự s-maxage, max-age, Expires; heuristic, thường 10% từ Last-Modified; dùng bản cũ khi mất mạng trừ must-revalidate/no-cache | rfc9111 4.2, 4.2.1, 4.2.2, 4.2.4 | stable |
| If-None-Match ưu tiên hơn If-Modified-Since; 304 cập nhật và dùng lại bản lưu; 200 đầy đủ thì thay | rfc9111 4.3 | stable |
| max-age, no-cache (lưu nhưng kiểm tra lại), no-store (không lưu; không phải cơ chế bảo mật tin cậy), must-revalidate (mất mạng → lỗi, nên 504), private | rfc9111 5.2.2 | stable |
| ETag là validator, mạnh và yếu (W/); 304 không có nội dung | rfc9110 8.8, 15.4.5 | stable |
| Khi nào cache, chính sách hết hạn, nhất quán, LRU/LFU/FIFO | book-xu1 ch.1 | guideline |
| Ba tầng của app, OkHttp Cache, DB là nguồn sự thật khác cache HTTP, gợi ý header theo loại dữ liệu, mọi con số | site | simplified |
| immutable không có trong RFC 9111 (không nhắc) | — | ghi chú |

### I7 · Phân trang
Đọc ngày 2026-11-24: Acing bằng pdftotext (12.7.1); AIP-158, ba trang Paging 3 và SubcomposeLayout.kt qua agent web-fetch (200). Xu tập 1 và DDIA bản 2 không có phần phân trang API (chỉ có offset của log), nên không trích. Phần cuối SubcomposeLayout.kt công cụ chỉ trả bản tóm tắt; thông điệp lỗi lấy nguyên văn, kiểu ngoại lệ (requirePrecondition) không nêu cụ thể.
| Khẳng định | Nguồn | Loại |
|---|---|---|
| Trang theo số lệch khi thêm ở đầu (trang 2 trả 10–19 thay vì 11–20); page_version chỉ đúng khi thay đổi ở đầu; tốt hơn là gửi previous_last / previous_first | book-acing 12.7.1 | guideline |
| page_size, page_token, next_page_token; token mờ, URL-safe, không đọc được (Base64 không đủ), không cấp quyền; next_page_token rỗng là cách duy nhất báo hết; trang ngắn hay rỗng chưa chắc là hết; đổi tham số khác → INVALID_ARGUMENT; token hết hạn khoảng 3 ngày; thêm phân trang sau là thay đổi không tương thích | aip-158 | stable |
| Paging 3.5.3: cache trong bộ nhớ, gộp request, làm mới, thử lại; PagingSource / Pager / PagingData / collectAsLazyPagingItems theo tầng; LoadResult.Page(prevKey, nextKey), null là hết; LoadResult.Error; getRefreshKey; nguồn bất biến, invalidate() → PagingSource mới | ax-paging | stable |
| RemoteMediator; database là nguồn sự thật; LoadType; bảng remote_keys ghi cùng transaction; initialize() SKIP/LAUNCH_INITIAL_REFRESH | ax-paging-db | stable |
| Key trùng trong lazy list → Key "…" was already used (subcompose, requirePrecondition) | ax-subcompose-src (commit 3fa4054, 2026-10-15) | impl |
| Key ổn định và duy nhất cho mỗi mục | cp-lists | stable |
| Phép đếm lặp/sót, SQL theo (published_at, id), số bài, cỡ trang 4, token "tk1", nhận xét khi nào offset còn dùng được | site | simplified |

### I8 · Nhiều thiết bị và xung đột
Đọc ngày 2026-11-24: DDIA bản 2 ch.6 (Sync Engines and Local-First Software; Dealing with Conflicting Writes), ch.8 (Preventing Lost Updates; Conditional writes), ch.9 (LWW và đồng hồ lệch) và Xu tập 1 ch.15 (Sync conflicts) từ bản text trong scratchpad; RFC 9110 và RFC 6585 qua agent web-fetch (200, đọc nguyên văn các mục 13.1.1, 13.1.2, 15.5.13; RFC 6585 §3, §7.1).
| Khẳng định | Nguồn | Loại |
|---|---|---|
| Mỗi thiết bị ghi được khi mất mạng là một leader; sync là sao chép nhiều leader bất đồng bộ; đồng thời = không bên nào biết bên kia | book-ddia2 ch.6 | guideline |
| LWW: chọn một bên thắng, âm thầm bỏ bên khác; ổn khi chỉ thêm với khóa duy nhất | book-ddia2 ch.6 | guideline |
| Gộp tay (siblings) tốn công; gộp tự động; map khóa-giá trị gộp theo từng khóa; giỏ hàng hợp tập hợp làm món đã xóa hiện lại; CRDT, OT | book-ddia2 ch.6 | guideline |
| Lost update (đọc, sửa, ghi); ghi có điều kiện, khóa lạc quan theo số phiên bản | book-ddia2 ch.8 | guideline |
| LWW theo giờ client làm mất ghi khi đồng hồ lệch, không báo lỗi | book-ddia2 ch.9 | guideline |
| If-Match chống lost update, so sánh mạnh; sai thì không thực hiện, trả 412 (hay 2xx nếu thay đổi đã được áp dụng); If-None-Match: * khi tạo; 412 | rfc9110 13.1.1, 13.1.2, 15.5.13 | stable |
| 428 Precondition Required; là tùy chọn, client không dựa vào được | rfc6585 §3, §7.1 | stable |
| Bản xử lý trước thắng, bản sau nhận xung đột, hiện cả hai bản cho người dùng | book-xu1 ch.15 | guideline |
| Làm lại ý định sau 412 (RFC không quy định), ba trường, mốc giờ, giá trị, lời khuyên bắt đầu bằng If-Match | site | simplified |
