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
