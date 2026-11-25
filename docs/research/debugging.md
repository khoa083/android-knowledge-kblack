# Nghiên cứu track L (Gỡ lỗi và hiệu năng Android)

> Track đã duyệt 2026-11-24, chưa xây. Dàn ý: `docs/tracks/L-debugging-performance.md`. Nguồn chính thức thắng khi mâu thuẫn.

## Đã đọc để soạn dàn ý (2026-11-24, chỉ mục lục)
- **Kodeco, *Android Debugging by Tutorials*:** ch.1–12, lấy từ bookmark PDF trong catalog. PDF không có lớp text nên khi viết phải đọc dạng ảnh trang.
- **Kodeco, *Android Test-Driven Development*:** ch.12–14.
- **URL kiểm HTTP 200 bằng curl ngày 2026-11-24:**
  - developer.android.com:
    - studio/debug, studio/debug/logcat, studio/debug/layout-inspector;
    - studio/inspect/task;
    - studio/profile, studio/profile/memory-profiler, studio/profile/record-traces, studio/debug/network-profiler;
    - topic/performance/tracing, topic/performance/vitals, topic/performance/vitals/anr, topic/performance/memory;
    - build/shrink-code, studio/command-line/retrace;
    - reference/android/os/StrictMode;
    - topic/performance/benchmarking/macrobenchmark-overview;
    - tools/adb, studio/debug/bug-report.
  - Ngoài developer.android.com: perfetto.dev/docs, square.github.io/leakcanary.
  - Trả 404: studio/inspect/database-inspector. Phải tìm đường dẫn mới.
- **Chưa xác minh:** Energy Profiler (ch.12 của sách) còn trong bản Android Studio hiện tại không.

## Bảng nguồn theo chương
Điền khi viết từng chương. Ghi phiên bản Android Studio đã đối chiếu.

### l1 Quy trình gỡ lỗi, adb và bug report (đọc 2026-11-25, trang không ghi ngày cập nhật)
| Ý trên site | Nguồn |
|---|---|
| adb gồm client, server (cổng TCP 5037), daemon adbd; USB debugging; gỡ lỗi không dây từ Android 11; adb devices, install, shell, pull, push; am start, am kill (chỉ đóng tiến trình đóng được an toàn) | developer.android.com/tools/adb |
| Bug report chứa log, stack trace, thông tin chẩn đoán; lấy bằng Take bug report, emulator, adb bugreport; ZIP với bugreport-*.txt gồm dumpsys, dumpstate, logcat; Play Console và Crashlytics thu crash, ANR của người dùng | developer.android.com/studio/debug/bug-report |
| Breakpoint trong Java, Kotlin, C/C++; xem biến, tính biểu thức; bật gỡ lỗi trên thiết bị; biến thể build debuggable | developer.android.com/studio/debug (trang ngắn; chi tiết breakpoint ở tài liệu IntelliJ IDEA, sẽ đọc cho l2) |
| **Của site:** vòng tái hiện, thu hẹp, giả thuyết, kiểm, khóa bằng test; 8 kịch bản thao tác, 4 làm màn hình bị tạo lại; Fragment nhận dữ liệu qua setter; khóa dọc còn 3 crash, phép kiểm isInitialized thành 3 màn trống; truyền id qua arguments và test FragmentScenario.recreate | — |
- Sách Android Debugging by Tutorials chưa đọc cho l1 (PDF không có lớp text); chương này chỉ dựa trên tài liệu chính thức.

### l2 Debugger: breakpoint, watch, evaluate (đọc 2026-11-25)
| Ý trên site | Nguồn |
|---|---|
| Bốn loại breakpoint (dòng, hàm vào/ra, watchpoint trên trường, ngoại lệ); điều kiện tính mỗi lần chạm, có thể có side effect; Suspend tắt thì chỉ ghi log hay làm cò; chính sách All và Thread; Evaluate and log; Remove once hit; breakpoint phụ thuộc; pass count; breakpoint hàm được mô phỏng vì bản thật chậm | jetbrains.com/help/idea/using-breakpoints.html (IntelliJ IDEA 2026.3, ngày trang 17/11/2026) |
| Watch tính lại mỗi bước, có thể nặng; watch và evaluate chỉ chạy khi dừng ở breakpoint; evaluate tính mọi biểu thức kể cả gọi hàm; cảnh báo side effect; breakpoint trong hàm được gọi lúc evaluate bị bỏ qua | jetbrains.com/help/idea/examining-suspended-program.html |
| Chế độ debug của kotlinx-coroutines (tên coroutine, -Dkotlinx.coroutines.debug, -ea, chi phí không đáng kể); khôi phục stack trace, cause là ngoại lệ gốc, frame _COROUTINE._BOUNDARY; DebugProbes không chạy trên Android | kotlinlang.org/docs/coroutines-debugging.html (1.11.0, ngày trang 07/09/2026); kotlinx-coroutines-debug README |
| **Của site:** 500 lịch, đơn 347 giảm 120 % (phí −40.000); 348 lần dừng so với 1; luồng đồng bộ nhịp mỗi giây, hạn 10 giây, xem biến 30 giây | — |
- Trang kotlinlang.org/docs/debug-coroutines-using-intellij.html trả 404 (2026-11-25); trang developer.android.com/studio/debug không có chi tiết breakpoint.

### l3 Logcat (đọc 2026-11-25, các trang không ghi ngày)
| Ý trên site | Nguồn |
|---|---|
| Định dạng dòng; truy vấn key:value (tag, package, process, message, level, age), is:crash, is:stacktrace; - để loại, ~ cho regex; cùng key OR, khác key AND, & ưu tiên hơn |; level: là mức đó trở lên; package:mine; age theo đồng hồ máy tính; PROCESS ENDED/STARTED | developer.android.com/studio/debug/logcat |
| v, d, i, w, e, wtf; hằng số 2–7; wtf ở ASSERT kèm stack; isLoggable mặc định INFO, setprop log.tag.<TAG>; tag > 23 ký tự ném lỗi tới API 25; tạo chuỗi tốn cấp phát | developer.android.com/reference/android/util/Log |
| adb logcat tag:mức, V D I W E F S, *:S; -v threadtime mặc định; -b buffer; logd buffer vòng; bốn tầng lọc | developer.android.com/tools/logcat (trang không mô tả -s, -c, --pid) |
| Lộ thông tin qua log (MASVS-STORAGE); READ_LOGS từ API 16; làm sạch log bản không debug; R8 -assumenosideeffects xóa mọi mức trừ warning, error; chỉ log hằng số lúc biên dịch | developer.android.com/privacy-and-security/risks/log-info-disclosure |
| **Của site:** 16 dòng log, PID 4120 là app; 2 dòng lộ số điện thoại; lọc còn 8, 2, 7; release còn 2 dòng, 1 dòng lộ | — |
- Ghi chú: Logcat của Studio gọi mức cao nhất là FATAL, truy vấn level: dùng ASSERT, adb logcat dùng chữ F; site dùng tên của lớp Log (ASSERT).

### l4 Đọc stack trace (đọc 2026-11-25)
| Ý trên site | Nguồn |
|---|---|
| Dòng đầu là toString (lớp, ": ", thông điệp); frame "at"; Caused by cho cause; "... n more" là n frame cuối trùng với ngoại lệ bọc ngoài; Suppressed từ try-with-resources; getCause, initCause | docs.oracle.com Java SE 21 Throwable |
| "--- beginning of crash", "FATAL EXCEPTION: main", "Process: …, PID: …"; loại ngoại lệ và chỗ ném là hai mảnh quan trọng; đi lên stack tìm chỗ truyền giá trị sai; không có mã app thì có thể do việc bất đồng bộ; NPE là nguyên nhân crash lớn nhất trên Google Play | developer.android.com/topic/performance/vitals/crash |
| Dán stack trace từ bên ngoài; mã nguồn phải cùng phiên bản với bản tạo ra stack trace | developer.android.com/studio/debug/stacktraces (trang không nói về retrace) |
| Khôi phục stack trace của coroutine, bản sao có cause là bản gốc, frame _COROUTINE._BOUNDARY | kotlinlang.org/docs/coroutines-debugging.html |
| **Của site:** crash ba tầng (RuntimeException ← IllegalStateException ← DateTimeParseException ngày 2026-11-31); "... 5 more", "... 8 more" tính từ đuôi chung; BookingMapper.kt:22; bài tập "150.000" với "... 6 more" | — |

### l5 R8 và stack trace bị làm rối (đọc 2026-11-25)
| Ý trên site | Nguồn |
|---|---|
| R8 thu gọn từ điểm vào, tối ưu (inline, gộp lớp), làm rối tên, thu gọn tài nguyên; isMinifyEnabled, isShrinkResources, proguard-android-optimize.txt; DSL mới từ AGP 9.3 | developer.android.com/build/shrink-code |
| Cú pháp retrace, đọc stdin, --verbose/--info/--quiet/--regex | developer.android.com/studio/command-line/retrace |
| Crash chỉ ở release do reflection; ClassNotFoundException…; keep rule, Jetpack Keep; configuration.txt; -whyareyoukeeping; mapping bị ghi đè mỗi lần build, gói vào AAB; Logcat mới tự dịch ngược (Studio Otter 3 Feature Drop, AGP 9.0) | developer.android.com/topic/performance/app-optimization/troubleshoot-the-optimization |
| Play lấy mapping từ AAB với AGP 4.1+; APK phải tự tải; chỉ crash sau khi tải mới được dịch | support.google.com/googleplay/android-developer/answer/9848633 |
| **Của site:** bản 1.6.0, mapping a.b → PaymentFactory (bản mới: BookingRepo); 2 frame sai mà hợp lý; Class.forName("vn.henkham.pay.MomoPayment"); keep rule theo interface PaymentMethod; bài tập dòng 5 → 22 | — |
- Chưa có nguồn chính thức cho định dạng dòng mapping (khoảng dòng "1:12:… :18:29 -> c"); site dùng dạng của R8 như ví dụ minh họa.

### l6 Layout Inspector: xem cây giao diện (đọc 2026-11-25, trang không ghi phiên bản Android Studio)
| Ý trên site | Nguồn |
|---|---|
| Component Tree thời gian thực, Attributes, có thể cần khởi động lại Activity; Deep Inspect: chọn vùng để thấy mọi thành phần; Show Only Subtree/Parents; cập nhật trực tiếp; đếm recomposition và skip; snapshot; chế độ nhúng | developer.android.com/studio/debug/layout-inspector |
| Hit test từ gốc xuống theo bounds; giữa anh em chỉ cái z cao nhất được hit (hai Button chồng trong Box); chuỗi hit giữ cho cả cử chỉ; clickable, Button tự tiêu thụ | developer.android.com/develop/ui/compose/touch-input/pointer-input/understand-gestures |
| onInterceptTouchEvent, cha thấy trước con, ACTION_CANCEL, requestDisallowInterceptTouchEvent, TouchDelegate | developer.android.com/develop/ui/views/touch-and-input/gestures/viewgroup (trang không nêu luật thứ tự z cho View) |
| **Của site:** màn đặt lịch 360 × 800, lớp phủ LoadingOverlay alpha 0 clickable, điểm chạm (180, 624), nút 48 → 64 dp; sửa bằng if (state.loading) | — |
- Alpha không ảnh hưởng hit test: suy ra từ việc hit test dựa trên bounds (trang Compose); trang không nói thẳng về alpha.
