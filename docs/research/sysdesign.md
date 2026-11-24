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

