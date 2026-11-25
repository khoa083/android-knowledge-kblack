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

### l7 Dữ liệu và việc nền: Database Inspector, Background Task Inspector (đọc 2026-11-25)
| Ý trên site | Nguồn |
|---|---|
| Xem, truy vấn, sửa database khi app chạy; API 26+; Live updates chỉ đọc; Flow/LiveData thấy thay đổi ngay; chạy @Query của DAO; truy vấn tự do; giữ kết nối; offline chỉ đọc | developer.android.com/studio/inspect/database |
| WorkManager 2.5.0+, API 26+; danh sách, chi tiết (ràng buộc, trạng thái, chuỗi, đầu ra), Graph View, hủy worker; job, alarm, wakelock chuyển từ Energy profiler | developer.android.com/studio/inspect/task |
| Ý nghĩa sáu trạng thái; FAILED và CANCELLED lan xuống; isFinished | developer.android.com/reference/androidx/work/WorkInfo.State |
| Ràng buộc phải thỏa tất cả; UNMETERED; Result.retry, backoff EXPONENTIAL 30 giây mặc định, tối thiểu 10 giây | developer.android.com/develop/background-work/background-tasks/persistent/getting-started/define-work |
| **Của site:** bảng booking 4 dòng (39 CANCELLED, 40–41 COMPLETED, 42 PENDING), truy vấn CONFIRMED trả 0; chuỗi UploadPhotos (UNMETERED) → SyncBookings → NotifyUser trên 4G | — |
- Energy Profiler: trang Background Task Inspector nói phần job, alarm, wakelock đã chuyển từ Energy profiler sang đây; dùng điều này cho l11 (pin).

### l8 Bộ nhớ: churn, rò rỉ, heap dump (đọc 2026-11-25)
| Ý trên site | Nguồn |
|---|---|
| Heap dump: Shallow Size, Retained Size (cây dominator), Depth từ GC root, References, lọc Activity/Fragment rò | developer.android.com/studio/profile/memory-profiler |
| Heap phân thế hệ; GC có thể đẩy khung hình quá 16 ms; giới hạn heap, OOM; getMemoryClass | developer.android.com/topic/performance/memory-overview |
| Rò rỉ thường do biến static; churn gây nhiều GC; đối tượng tạm trong vòng lặp, recompose, khi vẽ; onTrimMemory | developer.android.com/topic/performance/memory/manage-app-memory |
| Ghi cấp phát kèm stack trace; Sampled so với Full; GC trên dòng thời gian | developer.android.com/studio/profile/record-java-kotlin-allocations |
| LeakCanary 2.14: bốn bước, tham chiếu yếu, chờ 5 giây, ngưỡng 5/1, leak trace; nguyên nhân hay gặp | square.github.io/leakcanary (thư viện bên ngoài) |
| **Của site:** nền 18 MB, 2,4 MB mỗi DetailActivity, giới hạn 64 MB, OOM ở lần mở 20 (66 MB); BookingEventBus giữ lambda giữ Activity | — |

### l9 CPU, trace và khung hình giật (đọc 2026-11-25)
| Ý trên site | Nguồn |
|---|---|
| 16/11/8 ms ở 60/90/120 fps; quá hạn thì Choreographer bỏ cả khung; khung chậm 16–700 ms, đứng 700 ms–5 s, ANR quá 5 s; Record View#draw và DrawFrame trên RenderThread; nguyên nhân; trace marker khoảng 10 µs, không gắn hàm dưới khoảng 200 µs; method trace cho giật giả | developer.android.com/topic/performance/vitals/render |
| System trace gom dữ liệu kernel; Perfetto từ Android 10; không cho chi tiết thực thi trong app | developer.android.com/topic/performance/tracing |
| trace("tên") { } của androidx.tracing, tự đóng; app phải profileable | developer.android.com/topic/performance/tracing/custom-events (trang không nói giới hạn độ dài tên hay yêu cầu cùng luồng) |
| System trace trong Android Studio: khung trên main và RenderThread | developer.android.com/studio/profile/record-traces |
| Perfetto mã nguồn mở, UI trong trình duyệt, SQL | perfetto.dev/docs |
| **Của site:** 12 khung, khung thường 4 + 2,5 ms, khung nạp trang parse 28 ms trên main (34,5 ms), bind 5 ms khi parse ở nền; công thức vsync lỡ ceil(t ÷ hạn) − 1 | — |

### l10 ANR và StrictMode (đọc 2026-11-25)
| Ý trên site | Nguồn |
|---|---|
| ANR khi main không xử lý được input hay vẽ; 5 giây cho input; startForeground trong 5 giây; nguyên nhân (I/O, tính lâu, binder, chờ khóa, deadlock); /data/anr, bug report | developer.android.com/topic/performance/vitals/anr |
| Hạn mặc định AOSP/Pixel (input 5 s; service 20/200 s; broadcast 10/60 s tới Android 13, 10–20/60–120 s từ 14); Blocked, Waiting, held by; Mutex.withLock; nativePollOnce thường không hành động được | developer.android.com/topic/performance/anrs/diagnose-and-fix-anrs |
| StrictMode: công cụ cho nhà phát triển; ThreadPolicy, VmPolicy, detectAll, penaltyLog; không phải bảo mật, không bắt mọi truy cập | developer.android.com/reference/android/os/StrictMode (penaltyDeath không có trên trang chính; site chỉ nhắc như lỗi dùng sai) |
| **Của site:** khóa 0x0a1b, SyncWorker tid 24, sync lấy khóa 1 giây trước khi bấm, mạng 0,3 s / 9 s, chờ 8 s; StrictMode bắt đọc/ghi đĩa trong save | — |
- Trang vitals không ghi ngưỡng tỉ lệ ANR (0,47 %); site không dùng con số đó.

### l11 Mạng và pin (đọc 2026-11-25)
| Ý trên site | Nguồn |
|---|---|
| Network Inspector: dòng thời gian, kích thước, loại, trạng thái, thời gian; header, body, call stack; Thread View; chỉ HttpsURLConnection và OkHttp; Rules | developer.android.com/studio/debug/network-profiler (trang không ghi API tối thiểu) |
| Radio 3G điển hình: toàn công suất, thấp (khoảng −50 %), chờ; 5 s đuôi, 12 s thấp, mỗi phiên ≥ khoảng 18 s; gom request; tải trước 2–5 phút, 1–5 MB; WorkManager khi sạc và Wi-Fi; connection pooling | developer.android.com/training/efficient-downloads/efficient-network-access |
| Tải dữ liệu lớn khi có Wi-Fi | developer.android.com/develop/connectivity/network-ops/managing |
| Wake lock quá mức: tổng ≥ 2 giờ/24 giờ ở nền; miễn âm thanh, vị trí, job người dùng; > 5 % phiên trong 28 ngày ảnh hưởng hiển thị trên Play | developer.android.com/topic/performance/vitals/wakelock |
| **Của site:** 3 request GET /bookings ở giây 0, 2, 7, mỗi cái 1 s và 1,2 MB; radio 13 s / 12 s so với 6 s / 12 s; trang đầu 120 KB | — |
- Chưa đọc được trang tổng quan về pin (topic/performance/power trả về trang Connectivity); chưa có nguồn cho cache HTTP ở chương này, nên chỉ trỏ sang chương Cache của track Thiết kế hệ thống.

### l12 Đo hiệu năng cho đúng (đọc 2026-11-25)
| Ý trên site | Nguồn |
|---|---|
| Macrobenchmark: khởi động, cuộn, animation; module test riêng; app gần release, không debuggable, nên thu gọn, profileable; measureRepeated (packageName, metrics, iterations); COLD/WARM/HOT; compilationMode mặc định cài Baseline Profile; không khuyên emulator; lỗi khi debuggable, emulator, pin yếu; JSON và trace mỗi lần | developer.android.com/topic/performance/benchmarking/macrobenchmark-overview |
| StartupTimingMetric min/median/max, "luôn tập trung vào trung vị"; FrameTimingMetric P50–P99, nhìn P95, P99 | developer.android.com/topic/performance/benchmarking/macrobenchmark-metrics |
| TTID, TTFD (reportFullyDrawn), cold/warm/hot, tối ưu theo cold start, dòng Displayed | developer.android.com/topic/performance/vitals/launch-time (trang không ghi ngưỡng vitals) |
| **Của site:** 10 số đo mỗi bên; một lần 1.480 với 870 ms (41,2 %); trung vị 1.012,5 với 962,5 ms (4,9 %); bài tập 815/795 và trung bình 910/795 | — |
- Chưa đọc được nguồn chính thức về JIT, nhiệt độ, lockClocks; site chỉ nói "việc nền, nhiệt độ, pin" làm số đo dao động, dựa trên cảnh báo pin yếu và emulator của trang Macrobenchmark và lời khuyên giữ nhiệt độ ổn định của PowerMetric.
