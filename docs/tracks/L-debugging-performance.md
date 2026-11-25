# TRACK L — Gỡ lỗi và hiệu năng Android / Android Debugging and Performance (`debugging`)

> **ĐÃ DUYỆT (2026-11-24, người dùng đề xuất chủ đề).** Hai câu hỏi cuối theo mặc định (người dùng đổi được): **xây sau K**, **gỡ lỗi coroutine gộp vào l2 và l4**. **ĐÃ XÂY XONG 2026-11-25** (L0–L12, stable); người dùng nhắc thêm: không đi sâu vào IDE.
> Khác với dàn ý: l4 dùng bảng phẳng thụt lề thay cho hộp lồng (quy tắc tránh hộp lồng sâu); Energy Profiler không còn là công cụ riêng (job, alarm, wakelock đã chuyển sang Background Task Inspector), nên l11 dạy pin qua mô hình radio và wake lock; Database Inspector ở đường dẫn studio/inspect/database.
> Nguyên tắc: **cần và đủ**. Dạy cách tìm ra nguyên nhân bằng công cụ, không dạy từng nút bấm của Android Studio. Mỗi chương bắt đầu từ một triệu chứng thật: crash không tái hiện được, stack trace toàn chữ a.b.c, app chậm dần rồi OOM, ANR trên máy người dùng.

## Manifest đề xuất
| Trường | Giá trị |
|---|---|
| id / code / order | `debugging` / L / 120. Không dùng `debug`, để khỏi nhầm với `dev` trong danh sách id cấm |
| domain | engineering |
| Tên vi / en | Gỡ lỗi và hiệu năng Android / Android Debugging and Performance |
| level / estMinutes | intermediate / 360 |
| prerequisites | [] (nên đọc Kotlin K6 và Coroutines A1–A4 trước) |
| status | `draft` trong lúc viết, `stable` sau l0 |
| Ví dụ xuyên suốt | App hư cấu "Hẹn Khám" với các lỗi gài sẵn: crash khi xoay, danh sách giật, rò rỉ Activity, ANR khi lưu |

## Nguồn đã đọc để soạn dàn ý
- **Kodeco, *Android Debugging by Tutorials*** (đọc mục lục từ bookmark PDF).
  - PDF **không có lớp text**, nên khi viết phải đọc dạng ảnh trang.
  - Giao diện Android Studio trong sách có thể đã cũ. Chỗ nào lệch, theo tài liệu hiện tại và ghi rõ.
  - Các chương:
    - ch.1 bắt đầu, debugger, adb;
    - ch.2 breakpoint (có điều kiện, breakpoint ghi log);
    - ch.3 Logcat;
    - ch.4 đọc stack trace (bắt và ném lại, Crashlytics, stack trace từ bên ngoài);
    - ch.5 watch và evaluate;
    - ch.6 Layout Inspector;
    - ch.7 Database Inspector;
    - ch.8 Background Task Inspector (WorkManager);
    - ch.9 CPU profiler, method trace và system trace, Perfetto;
    - ch.10 Memory profiler, churn và rò rỉ;
    - ch.11 Network Inspector;
    - ch.12 Energy profiler.
- **Kodeco, *Android Test-Driven Development*** (dùng một phần):
  - ch.12 vấn đề của app cũ;
  - ch.13 test cấp cao bằng Espresso cho app cũ;
  - ch.14 refactor có trọng tâm, thêm test bao quanh trước khi sửa.
- **Chính thức, đã kiểm HTTP 200 ngày 2026-11-24:**
  - developer.android.com:
    - Debug your app, Logcat, Layout Inspector, Background Task Inspector;
    - Profile your app, Memory profiler, Record traces, Network profiler, System tracing;
    - ANR, Android vitals, Manage your app's memory;
    - Shrink, obfuscate and optimize (R8), Retrace;
    - StrictMode (reference), Macrobenchmark overview;
    - adb, Bug report.
  - perfetto.dev (tài liệu Perfetto); square.github.io/leakcanary (LeakCanary, thư viện bên ngoài).
  - Trang Database Inspector ở đường dẫn cũ trả 404. Khi viết h4/l7 phải tìm đường dẫn mới.

## Điểm cần nói rõ trong track
- Công cụ của Android Studio đổi giao diện theo từng bản. Mỗi chương ghi **phiên bản Android Studio** đã đối chiếu, và dạy **câu hỏi công cụ trả lời** (luồng nào giữ khóa, ai còn giữ tham chiếu tới Activity) hơn là vị trí nút bấm.
- **Energy Profiler** trong sách cần kiểm lại với bản Android Studio hiện tại. Chưa xác minh nó còn hay đã được thay, nên chưa khẳng định gì.
- **LeakCanary là thư viện bên ngoài**: ghi phiên bản; cơ chế (heap dump, chuỗi tham chiếu) dạy độc lập với thư viện.
- Mọi số đo trong sim là minh họa. Phần đo thật (l12) dạy cách đo cho đúng, không đưa ra con số chung.

## IN (đưa vào) và lý do
| Nội dung | Lý do |
|---|---|
| Quy trình gỡ lỗi: tái hiện, thu hẹp, giả thuyết, kiểm; adb và bug report | Sửa theo đoán thì lỗi quay lại; không tái hiện được thì không biết đã sửa chưa |
| Debugger: breakpoint có điều kiện, breakpoint ghi log, evaluate, watch | Dừng đúng lần lặp có lỗi thay vì bấm Resume 500 lần; không phải thêm Log rồi build lại |
| Logcat: mức, tag, lọc; log trong bản release | Log quá nhiều thì không tìm thấy gì; log lộ dữ liệu người dùng |
| Đọc stack trace: chuỗi "Caused by", "... N more", suppressed, stack trace của coroutine | Sửa ở dòng đầu tiên thay vì nguyên nhân gốc |
| R8 và stack trace bị làm rối: mapping, retrace, keep rule | Crash trên Play Console chỉ hiện `a.b.c`; crash chỉ có ở bản release do reflection |
| Layout Inspector: cây giao diện, kích thước, thuộc tính | Nút bị che, chữ bị cắt, view chồng lên nhau |
| Database Inspector và Background Task Inspector | Dữ liệu "đã lưu" mà không thấy; worker bị kẹt ở trạng thái chờ |
| Bộ nhớ: allocation, churn, rò rỉ, heap dump, chuỗi tham chiếu | App chậm dần rồi OOM; Activity đã đóng vẫn nằm trong bộ nhớ |
| CPU và trace: method trace, system trace, Perfetto, khung hình giật | Danh sách giật mà không biết việc nào chiếm thời gian |
| ANR: đọc trace của các luồng, StrictMode bắt sớm | ANR trên máy người dùng; main thread chờ khóa hay đọc đĩa |
| Mạng và pin: Network Inspector, request trùng | Request gọi hai lần, tải dư dữ liệu, hao pin |
| Đo hiệu năng cho đúng: Macrobenchmark, lặp nhiều lần, so trước và sau | "Nhanh hơn" chỉ vì đo một lần trên máy nóng |

## OUT (bỏ ra hoặc chỉ nhắc) và lý do
| Nội dung | Lý do |
|---|---|
| Đếm recomposition, stability, baseline profile | Đã có ở track **Runtime** (PF, B8): chỉ dẫn link |
| Cơ chế deadlock, LMK, process death | Thuộc track **I** (i2, i3); ở đây chỉ phần đọc trace và dùng công cụ |
| Kiến trúc khởi động app (dời việc khỏi Application.onCreate) | Thuộc track **I** (i11); ở đây chỉ cách đo |
| Tái hiện bug bằng test, chia đôi commit (git bisect) | Thuộc track **J** (j7); l1 chỉ dẫn link |
| Viết và tối ưu keep rule chi tiết | Chỉ phần liên quan crash; tối ưu kích thước app thuộc track **I** (i11) |
| Thiết lập Firebase Crashlytics | Dịch vụ cụ thể; chỉ dạy đọc stack trace từ bên ngoài |
| Gỡ lỗi mã native (NDK, LLDB), đọc tombstone | Ít gặp trong app Kotlin thông thường; "đọc thêm" |
| Dịch ngược APK, kiểm tra bảo mật | Thuộc một chủ đề bảo mật riêng (chưa có trong lộ trình) |
| Test Espresso, refactor app cũ chi tiết | Thuộc track **G** (g10, g11) và **J** (j4–j6) |

## Chương (13)
Cột **Hình chính** là tab mặc định; sơ đồ node của sim ở tab phụ. Track này nhiều chuyện "đọc một cấu trúc có sẵn" (stack trace, cây view, heap, trace của luồng), nên hình thường vẽ đúng cấu trúc đó: hộp lồng, cây, đồ thị tham chiếu, làn thời gian.

### Phần 1: Tìm ra lỗi
| Id | Chương | Lỗi dẫn dắt | Sim | Hình chính (vì sao hợp) | Nguồn chính |
|---|---|---|---|---|---|
| l1 | Quy trình gỡ lỗi, adb và bug report | Sửa theo đoán ba lần, crash vẫn quay lại | `debugging.loop`: tái hiện → thu hẹp → giả thuyết → kiểm → khóa bằng test | **Vòng** tái hiện, thu hẹp, giả thuyết, kiểm; vòng lặp lại khi giả thuyết sai | Debugging by Tutorials ch.1; adb; Bug report; Android TDD ch.12–13; cầu nối J j7 |
| l2 | Debugger: breakpoint, watch, evaluate | Lỗi chỉ ở lần lặp thứ 347; thêm Log rồi build lại mười lần | `debugging.breakpoint`: breakpoint thường, có điều kiện, ghi log không dừng; dừng một luồng hay mọi luồng | (1) **Làn thời gian** các luồng, chỗ dừng và luồng nào bị dừng. (2) **Bảng** biến tại điểm dừng | Debugging by Tutorials ch.2, ch.5; Debug your app |
| l3 | Logcat | 2 000 dòng log mỗi giây, không thấy dòng cần tìm; bản release in số điện thoại người dùng | `debugging.logcat`: lọc theo tag, mức, tiến trình; log nào còn trong release | **Bảng** log kiểu bắt gói tin, các hàng bị lọc mờ đi theo từng bộ lọc | Debugging by Tutorials ch.3; Logcat |
| l4 | Đọc stack trace | Sửa ở dòng đầu (`RuntimeException` của thư viện) trong khi nguyên nhân gốc nằm ở "Caused by" cuối | `debugging.trace`: một crash có ba tầng bọc; tìm frame của app và nguyên nhân gốc | **Hộp lồng**: ngoại lệ bọc ngoài → Caused by → nguyên nhân gốc; frame thuộc app được tô đậm, "... N more" mở ra được | Debugging by Tutorials ch.4; cầu nối Kotlin K6, Coroutines (stack trace của coroutine) |
| l5 | R8 và stack trace bị làm rối | Play Console báo `NullPointerException at a.b.c(Unknown Source)`; crash `ClassNotFoundException` chỉ có ở bản release | `debugging.retrace`: build release → mapping → retrace; lớp dùng qua reflection bị đổi tên | **Bảng đối chiếu** frame trước và sau retrace, kèm cột "dòng mapping đã dùng" | Shrink, obfuscate and optimize; Retrace |

### Phần 2: Nhìn vào bên trong app
| Id | Chương | Lỗi dẫn dắt | Sim | Hình chính (vì sao hợp) | Nguồn chính |
|---|---|---|---|---|---|
| l6 | Layout Inspector | Nút "Đặt lịch" bấm không ăn vì bị một view trong suốt che | `debugging.layout`: chọn node trong cây, xem kích thước, thứ tự vẽ, thuộc tính | **Cây** giao diện, node đang chọn có viền; node che lên tô đỏ | Debugging by Tutorials ch.6; Layout Inspector; cầu nối Runtime PF |
| l7 | Dữ liệu và việc nền: Database Inspector, Background Task Inspector | Lịch "đã lưu" mà danh sách trống; worker đồng bộ kẹt mãi ở trạng thái chờ | `debugging.inspect`: truy vấn bảng đang chạy; worker qua các trạng thái | (1) **Bảng** dòng dữ liệu đổi trực tiếp. (2) **Cây** trạng thái của worker (enqueued, running, blocked, succeeded, failed, cancelled), nhánh đang đứng có viền | Debugging by Tutorials ch.7–8; Background Task Inspector; cầu nối H h4, h7 |
| l8 | Bộ nhớ: churn, rò rỉ, heap dump | App chậm dần sau 20 lần mở màn hình rồi OOM | `debugging.leak`: mở và đóng màn hình; listener tĩnh giữ Activity; GC không thu được | **Đồ thị tham chiếu** (đồ thị phụ thuộc MỚI, dùng chung với G): GC root → … → Activity đã hủy; đường giữ lại tô đỏ, kèm **thanh** bộ nhớ theo lần mở | Debugging by Tutorials ch.10; Memory profiler; Manage your app's memory; LeakCanary (cơ chế) |
| l9 | CPU, trace và khung hình giật | Cuộn danh sách lịch hẹn bị giật | `debugging.jank`: system trace một lần cuộn; một khung hình vượt hạn vì parse JSON trên main | **Làn thời gian** main thread, RenderThread và các khung hình; khung trễ tô đỏ, có hạn khung hình làm mốc | Debugging by Tutorials ch.9; Record traces; System tracing; Perfetto |

### Phần 3: Lỗi trên máy người dùng
| Id | Chương | Lỗi dẫn dắt | Sim | Hình chính (vì sao hợp) | Nguồn chính |
|---|---|---|---|---|---|
| l10 | ANR và StrictMode | Android vitals báo ANR khi bấm "Lưu"; không tái hiện được trên máy dev | `debugging.anr`: đọc trace các luồng; main BLOCKED chờ khóa do luồng khác giữ; StrictMode bắt đọc đĩa trên main | (1) **Bảng** trace các luồng: luồng, trạng thái, đang chờ gì, đang giữ gì; dòng nối "chờ" → "giữ" được tô. (2) **Làn thời gian** có mốc hết hạn | ANR; StrictMode; Android vitals; cầu nối I i3 |
| l11 | Mạng và pin | Màn hình gọi cùng một API ba lần mỗi lần mở; app bị người dùng báo hao pin | `debugging.network`: request theo thời gian, request trùng, phản hồi quá lớn | **Dãy ô** các request theo thời gian, request trùng tô đỏ, kèm **bảng** kích thước phản hồi | Debugging by Tutorials ch.11–12; Network profiler; cầu nối I i4, i6 |
| l12 | Đo hiệu năng cho đúng | Tối ưu xong "nhanh hơn 40%", nhưng đó là do lần đo sau máy đã nóng | `debugging.measure`: đo một lần so với lặp nhiều lần; trung vị và phân vị; so trước và sau | **Bảng tính** các lần đo, trung vị, khoảng dao động; ví dụ kiểm chứng tính tay | Macrobenchmark overview; Android vitals; cầu nối Runtime PF, I i11 |
| l0 | Bản đồ track (viết CUỐI) | Gặp triệu chứng X thì mở công cụ nào, đọc chương nào | `debugging.map` | **Bảng tra** triệu chứng → công cụ → chương | — |

Khuôn mỗi chương như track Kotlin:
- tối đa 8 mục;
- 2 lỗi thật;
- 1 bài tập (đọc một stack trace, trace hay heap dump cho sẵn rồi tìm nguyên nhân);
- quiz 3–4 câu.

## Cầu nối dự kiến
- l1 ↔ J j7 (tái hiện bằng test, git bisect).
- l4 ↔ Kotlin K6 (ngoại lệ), Coroutines (stack trace của coroutine).
- l6, l9, l12 ↔ Runtime PF (recomposition, baseline profile).
- l7 ↔ H h4 (Room), h7 (WorkManager).
- l8 ↔ G g6 (singleton giữ Activity context), Kotlin K8 (lambda giữ tham chiếu).
- l10 ↔ I i3 (khóa, deadlock).
- l11 ↔ I i4, i6 (kênh giao tiếp, cache).

## Hai câu hỏi đã có mặc định (người dùng đổi được)
1. Xây sau K, cuối hàng đợi.
2. Gỡ lỗi coroutine (dump coroutine, debug agent) gộp vào l2 và l4, không có chương riêng.
