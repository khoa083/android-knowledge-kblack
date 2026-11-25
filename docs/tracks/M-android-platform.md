# TRACK M: Nền tảng Android: component và vòng đời / Android Platform Fundamentals: Components and Lifecycles (`platform`)

> **DÀN Ý, CHỜ NGƯỜI DÙNG DUYỆT (soạn 2026-11-25, người dùng đề xuất chủ đề).** Chưa xây. Năm câu hỏi ở cuối file đã có mặc định; người dùng đổi được.
>
> **Nguyên tắc: cần và đủ.**
> - Dạy **luật mà hệ thống áp lên app**: ai tạo component, ai giết process, khi nào callback được gọi, việc gì bị chặn theo phiên bản Android.
> - Không dạy cách gọi từng API cho thuộc lòng.
> - Mỗi chương bắt đầu từ một lỗi thật, ví dụ:
>   - xoay màn hình mất dữ liệu;
>   - bấm thông báo mở trùng màn hình;
>   - service bị giết khi lên Android 14;
>   - xin quyền lần hai thì hộp thoại không hiện nữa.
>
> **Theo lời dặn của người dùng khi làm track L:** không đi sâu vào IDE. Phần kiểm chứng dùng lệnh `adb` và mã, không dùng menu của Android Studio.

## Manifest đề xuất
| Trường | Giá trị |
|---|---|
| id / code / order | `platform` / M / **65**, tức là sau Kotlin (60) và trước Kiến trúc (70), vì G, H, I đều dựa trên các khái niệm của track này. Xem câu hỏi 1. Id `platform` không nằm trong danh sách cấm (`app`, `track`, `job`, `phase`, `step`, `badge`, `a11y`, `domain`, `shared`) |
| Id chương | `m0` … `m16`. Không trùng tiền tố khóa `m.<model>` vì luôn có số đi kèm |
| domain | engineering |
| Tên vi / en | Nền tảng Android: component và vòng đời / Android Platform Fundamentals: Components and Lifecycles |
| level / estMinutes | intermediate / khoảng 510 (17 chương, khoảng 30 phút mỗi chương) |
| prerequisites | [] (nên đọc Kotlin K1–K6 trước) |
| status | `draft` trong lúc viết, `stable` sau m0 |
| accent / icon | Chọn lúc xây, khác 12 màu đang dùng; icon `layers` hoặc `grid` |
| Ví dụ xuyên suốt | Tiếp tục dùng app hư cấu **Hẹn Khám**, thêm các tính năng gài lỗi (xem bảng bên dưới) |

### Tính năng của Hẹn Khám dùng trong track
| Tính năng | Component | Chương |
|---|---|---|
| Form đặt lịch qua một lần xoay màn hình | Activity, ViewModel, saved state | m4, m5 |
| Mở link `henkham://lich/123` từ SMS | Intent filter, deep link | m6, m7 |
| Chụp ảnh thẻ bảo hiểm bằng app Camera | Implicit intent, FileProvider, quyền URI | m6, m16 |
| Chỉ đường tới phòng khám khi màn hình tắt | Foreground service kiểu `location`, quyền vị trí | m11, m15 |
| Nhắc lịch trước 2 giờ | AlarmManager hoặc WorkManager, thông báo | m13, m14 |
| Đồng bộ lịch hẹn khi có mạng | WorkManager, giới hạn chạy nền | m10, m13 |
| Bắt sự kiện khởi động lại máy để đặt lại lời nhắc | BroadcastReceiver `BOOT_COMPLETED` | m12 |

## Nguồn đã đọc để soạn dàn ý (2026-11-25, chỉ mục lục)
- **Big Nerd Ranch, *Android Programming* bản 5** (EPUB, mục lục đầy đủ):
  - ch.3 vòng đời Activity (xoay màn hình, multi-window, mức log);
  - ch.4 giữ trạng thái UI (ViewModel, process death, instance state);
  - ch.7 Activity thứ hai (start, truyền dữ liệu, "How Android Sees Your Activities", nút Back);
  - ch.8 phiên bản SDK và tương thích;
  - ch.9 Fragment; ch.13 điều hướng giữa Fragment; ch.14 DialogFragment và truyền kết quả;
  - ch.16 implicit intent; ch.17 chụp ảnh qua intent (FileProvider, khai báo feature);
  - ch.18 bản địa hóa và bộ định tính cấu hình (configuration qualifier);
  - ch.22 WorkManager và thông báo;
  - ch.27 state trong Compose qua thay đổi cấu hình (chỉ để nối sang track Runtime).
- **Späth, *Pro Android with Kotlin* bản 2** (EPUB, đọc đến mức h3):
  - ch.1 hệ thống; ch.2 Application (task, manifest);
  - ch.3 Activity (intent filter gồm action, category, data, extra, flag; vòng đời; giữ state);
  - ch.4 Service (foreground, background, bound, vòng đời);
  - ch.5 Broadcast (explicit và implicit, bảo mật, gửi bằng dòng lệnh);
  - ch.6 Content Provider (URI, cursor, cấp quyền, Documents Provider);
  - ch.7 Permission (loại quyền, quyền đặc biệt, quyền qua terminal);
  - ch.8 API (lên lịch bằng JobScheduler và AlarmManager; thông báo: kênh, direct reply, nhóm, badge);
  - ch.9 Handler, Fragment; ch.19 CLI (`am`, `pm`).
  - Sách có nhiều API đã cũ (AsyncTask, Loader, IntentService, LocalBroadcastManager). Chỉ dạy chúng như "mã cũ còn gặp", luôn kèm cái thay thế hiện hành.
- **Laurence và cộng sự, *Programming Android with Kotlin*** (EPUB):
  - ch.3 nền tảng Android (tầng của Android, Context, bốn component, back stack, started và bound service);
  - ch.4 concurrency trong Android (mô hình luồng, khung hình rơi, rò rỉ bộ nhớ).
- **Kickstart Modern Android Development** (PDF, lấy bookmark từ catalog):
  - ch.2 ViewModel và khôi phục sau process death do hệ thống;
  - ch.5 deep link trong Navigation;
  - ch.12 các component Lifecycle của Jetpack (tự viết component biết vòng đời).
- **Chính thức, đã kiểm HTTP 200 bằng curl ngày 2026-11-25** (developer.android.com):
  - guide/components/fundamentals, guide/topics/manifest/manifest-intro, guide/components/activities/process-lifecycle;
  - guide/components/activities/activity-lifecycle, .../state-changes, topic/libraries/architecture/saving-states, .../viewmodel/viewmodel-savedstate;
  - guide/topics/resources/runtime-changes, guide/topics/resources/providing-resources;
  - guide/components/intents-filters, .../intents-common, training/package-visibility, training/basics/intents/result, training/app-links;
  - guide/components/activities/tasks-and-back-stack;
  - guide/fragments/lifecycle, guide/fragments/fragmentmanager, guide/fragments/communicate;
  - topic/libraries/architecture/lifecycle;
  - guide/components/services, guide/components/foreground-services, develop/background-work/services/fgs/service-types, guide/components/bound-services;
  - about/versions/oreo/background, guide/components/broadcasts, develop/background-work/background-tasks/broadcasts;
  - guide/background, develop/background-work/background-tasks/persistent, training/scheduling/alarms;
  - training/monitoring-device-state/doze-standby, topic/performance/appstandby;
  - develop/ui/views/notifications, .../channels, .../notification-permission, .../navigation, reference/android/app/PendingIntent;
  - guide/topics/permissions/overview, training/permissions/requesting, training/permissions/usage-notes;
  - guide/topics/providers/content-providers, training/secure-file-sharing/setup-sharing, reference/androidx/core/content/FileProvider;
  - guide/topics/manifest/uses-sdk-element, guide/app-compatibility;
  - about/versions/14/behavior-changes-14, about/versions/15/behavior-changes-15, about/versions/16/behavior-changes-16;
  - reference/android/os/Looper, reference/android/os/TransactionTooLargeException, training/articles/perf-anr.
- **Mã nguồn AOSP** (ActivityThread, Looper, MessageQueue, Zygote) dùng cho mục "dưới mui xe". Khi viết phải ghi tag nhánh AOSP đã đọc.

## Điểm cần nói rõ trong track
- **Hành vi đổi theo phiên bản: đây là rủi ro lớn nhất của track.**
  - Mỗi khẳng định kiểu "bị chặn", "bắt buộc", "ném ngoại lệ" phải ghi kèm **API level của máy** và **targetSdk của app**.
  - Phải đọc trang behavior changes đúng phiên bản vào ngày viết, ghi ngày đọc.
- **Bốn cuốn sách in năm 2022–2023, nên chỉ cập nhật tới khoảng Android 12 hoặc 13.**
  - Các thay đổi của Android 14, 15, 16 chỉ lấy từ tài liệu chính thức. Ví dụ: kiểu foreground service bắt buộc; cờ exported khi đăng ký receiver trong mã; giới hạn thời gian của một số kiểu foreground service.
  - Chỗ nào sách lệch tài liệu, theo tài liệu và ghi rõ.
- **Mục "dưới mui xe" là chi tiết cài đặt, gắn nhãn giản lược.**
  - Gồm: Zygote, system_server, Binder, ActivityThread, Looper.
  - Ghi tag AOSP đã đọc.
  - Nói rõ app không được dựa vào các chi tiết này, chỉ dùng để hiểu vì sao luật như vậy.
- **Mọi con số phải có nguồn và phiên bản.**
  - Ví dụ: hạn của `onReceive`, hạn gọi `startForeground`, chu kỳ tối thiểu của periodic work, giới hạn kích thước Bundle khi qua Binder, ngưỡng ANR.
  - Không có nguồn thì không ghi số.
- **Compose và View:**
  - Ví dụ UI dùng Compose, kiểu một Activity duy nhất.
  - Chương Fragment (m8) dạy để đọc và sửa dự án View hoặc Fragment cũ (câu hỏi 2).
- **API cũ còn gặp trong mã thật, dạy như mã cũ và luôn nêu cái thay thế:**
  - `startActivityForResult` → Activity Result API;
  - IntentService → WorkManager;
  - LocalBroadcastManager → Flow;
  - AsyncTask → coroutine.

## IN (đưa vào) và lý do
| Nội dung | Lý do |
|---|---|
| Manifest, process, lớp Application, main thread (Looper, Handler, MessageQueue), thứ tự khởi tạo | Không hiểu "ai gọi `onCreate`, trên luồng nào" thì không hiểu được ANR, khởi động chậm hay crash do khởi tạo sai thứ tự |
| Context: các loại, ai sống bao lâu, việc nào cần loại nào; tài nguyên theo cấu hình | Dialog dùng Application context thì crash; singleton giữ Activity thì rò rỉ; chọn sai tài nguyên `-land`, `-night`, `-vi` |
| Phiên bản SDK: minSdk, targetSdk, compileSdk, kiểm tra phiên bản lúc chạy | targetSdk là công tắc bật luật mới; tăng targetSdk mà không đọc behavior changes thì app gãy |
| Vòng đời Activity: trạng thái, callback, thứ tự khi hai Activity chuyển nhau, multi-window | Thả listener ở sai callback; tưởng `onDestroy` luôn được gọi |
| Thay đổi cấu hình và giữ state: Activity được tạo lại, ViewModelStore, saved instance state và Bundle, SavedStateHandle, giới hạn kích thước | Xoay màn hình mất dữ liệu; nhét danh sách lớn vào Bundle thì TransactionTooLargeException |
| Intent và intent filter: explicit và implicit, ba phép thử của filter (action, category, data), Activity Result API, package visibility, `exported`, deep link và App Links | Không có app xử lý thì ActivityNotFoundException; Android 11 trở lên không thấy app khác nếu thiếu `<queries>` |
| Task và back stack: launch mode, cờ của Intent, `onNewIntent`, task affinity, Back | Bấm thông báo mở trùng màn hình; Back từ deep link thoát app |
| Fragment: vòng đời Fragment và vòng đời view, FragmentManager, back stack, truyền kết quả | Quan sát LiveData bằng `this` thì nhận dữ liệu hai lần; giữ binding sau `onDestroyView` thì rò rỉ |
| Lifecycle của Jetpack: Lifecycle, LifecycleOwner, observer, ProcessLifecycleOwner | Component tự bật và tắt theo vòng đời, thay vì nhớ gọi tay ở năm chỗ |
| Giới hạn chạy nền: Doze, App Standby bucket, giới hạn theo phiên bản | Biết vì sao Timer hay Handler "chạy mỗi 5 phút" ngừng khi màn hình tắt; là nền để chọn công cụ ở m11–m13 |
| Service: started, bound, foreground, kiểu foreground service, vòng đời, giá trị trả về của `onStartCommand` | Gọi `startService` từ nền thì crash; thiếu kiểu foreground service trên Android 14 thì crash |
| BroadcastReceiver: đăng ký trong manifest hay trong mã, implicit broadcast bị chặn, cờ exported, `onReceive` chạy trên main, `goAsync` | Receiver không bao giờ được gọi; gọi mạng trong `onReceive` thì bị giết |
| WorkManager và AlarmManager: chọn công cụ, ràng buộc, unique work, chuỗi việc, backoff, expedited, alarm chính xác và quyền của nó | Lời nhắc trễ 40 phút; worker chạy hai lần; periodic 5 phút không chạy như mong đợi |
| Thông báo: kênh và mức quan trọng, quyền POST_NOTIFICATIONS, PendingIntent (mutable và immutable, request code), mở đúng màn hình kèm back stack, nhóm, action | Thông báo không hiện trên Android 13; mọi thông báo mở cùng một lịch hẹn |
| Quyền: cài đặt, runtime, đặc biệt; luồng xin quyền, giải thích lý do, từ chối vĩnh viễn, quyền một lần, tự thu hồi; quyền vị trí nền; quyền tùy chỉnh để bảo vệ component | Xin quyền lần ba thì hộp thoại không hiện; xin vị trí nền cùng lúc với vị trí thường thì bị bỏ qua |
| ContentProvider và chia sẻ tệp: ContentResolver, URI `content://`, FileProvider, cấp quyền URI tạm thời; provider khởi tạo trước `Application.onCreate` | Camera không ghi được ảnh vì thiếu cờ cấp quyền; `file://` qua Intent thì FileUriExposedException |

## OUT (bỏ ra hoặc chỉ nhắc) và lý do
| Nội dung | Lý do |
|---|---|
| Thứ hạng ưu tiên process, lmkd, thiết kế để sống sót sau process death | Đã có ở track **I** (i2). m5 chỉ dạy bảng "loại state nào sống qua sự kiện nào" rồi dẫn link |
| ViewModel và UiState theo góc kiến trúc, sự kiện một lần | Đã có ở **G** (g3). m5 chỉ dạy vì sao ViewModel sống qua lần xoay (ViewModelStore) |
| `repeatOnLifecycle`, `lifecycleScope`, thu thập Flow theo vòng đời | Đã có ở **Coroutines** (A8). m9 dẫn link |
| `remember` và `rememberSaveable` trong Compose | Đã có ở **Runtime**. m5 dẫn link |
| WorkManager dùng cho đồng bộ offline-first; đọc trạng thái worker bằng công cụ | Đã có ở **H** (h7) và **L** (l7). m13 dạy cơ chế và cách chọn |
| Thiết kế thông báo đẩy, FCM | Đã có ở **I** (i9), FCM chỉ làm nhẹ theo quyết định người dùng. m14 dạy phía app hiển thị thông báo |
| MediaStore, quyền đọc ảnh theo phiên bản, Room, DataStore | Đã có ở **H** (h8, h4, h3). m15 và m16 dẫn link |
| ANR, đọc trace, StrictMode, rò rỉ bộ nhớ | Đã có ở **L** (l8, l10). m1 và m2 dẫn link |
| Khởi động app nhanh, dời việc khỏi `Application.onCreate` | Đã có ở **I** (i11). m1 dạy thứ tự khởi tạo, i11 dạy tối ưu |
| Navigation (Compose hoặc Fragment) chi tiết, Material, layout, RecyclerView, custom view | Thuộc chủ đề "Compose UI thực hành" (chưa có). m6 và m7 chỉ dạy deep link ở mức Intent |
| Test component (Robolectric, ActivityScenario, test WorkManager) | Thuộc chủ đề "kiểm thử" (chưa có) |
| Hilt, mạng, Gradle, flavor, ký app | Thuộc G (g6) và các chủ đề mới chưa có. m1 chỉ nhắc manifest merger |
| Bảo mật sâu: tấn công component exported, intent redirection, chiếm PendingIntent | Thuộc chủ đề bảo mật (chưa có). Ở đây chỉ dùng làm lỗi minh họa cho `exported` và PendingIntent mutable |
| AIDL, Messenger, app nhiều process | Ít gặp trong app thường; m11 chỉ nhắc khi nói về bound service khác process |
| Camera, vị trí, cảm biến, Bluetooth, NFC, media | API theo chuyên đề; chỉ dùng làm ví dụ cho quyền và kiểu foreground service |
| App widget, Wear, TV, Auto, Instant App, Search framework, Contacts provider, sync adapter | Ngoài trọng tâm, hoặc API đã cũ |
| Chi tiết API predictive back, edge-to-edge | m7 chỉ nhắc ảnh hưởng tới Back; chi tiết thuộc chủ đề UI |

## Chương (17)
Cột **Hình chính** là tab mặc định. Sơ đồ node của sim nằm ở tab phụ.

Track này nhiều chuyện "hệ thống quyết định theo luật", nên hình thường là một trong ba kiểu:
- **bảng loại dần**: ứng viên bị gạch qua từng phép thử;
- **làn thời gian**: callback xảy ra theo thứ tự;
- **ma trận**: phiên bản hoặc sự kiện, nhân với hành vi.

### Phần 1: App và hệ thống
| Id | Chương | Lỗi dẫn dắt | Sim | Hình chính (vì sao hợp) | Nguồn chính |
|---|---|---|---|---|---|
| m1 | Từ bấm icon tới khung hình đầu: manifest, process, Application, main thread | (1) SDK khởi tạo trong `Application.onCreate` chạy hai lần vì app có process phụ. (2) Gọi mạng trên main thì NetworkOnMainThreadException | `platform.boot`: launcher → system_server → Zygote fork → ActivityThread.main → Looper → ContentProvider → Application → Activity → khung hình đầu. Bật hoặc tắt: process phụ, việc nặng trong Application | (1) **Làn thời gian** các tiến trình và luồng, mỗi callback là một thanh. (2) **Bảng hàng đợi** MessageQueue: từng message lần lượt được xử lý, message dài chặn các message sau (nối sang ANR) | Programming Android ch.3–4; Pro Android ch.1–2, ch.9 (Handler); Application fundamentals; Manifest; Looper; AOSP (ghi tag); cầu nối L10, I11, Coroutines (Dispatchers.Main dựa trên Handler) |
| m2 | Context và tài nguyên | (1) Hiện dialog bằng Application context thì BadTokenException. (2) Màn hình tiếng Việt khi xoay ngang lại hiện chuỗi tiếng Anh, vì thiếu `values-vi-land` mà có `values-land` | Hai sim. `platform.context`: việc (mở Activity, inflate theo theme, hiện dialog, lấy system service, giữ trong singleton) × loại context. `platform.resources`: thuật toán chọn tài nguyên loại dần thư mục theo từng bộ định tính | (1) **Ma trận** việc × context, ô là "chạy", "cảnh báo" hoặc "crash". (2) **Bảng loại dần** thư mục tài nguyên, đúng theo thuật toán trong tài liệu | Programming Android ch.3 (Context); BNR ch.18; Providing resources; cầu nối L8 và G6 (singleton giữ Activity) |
| m3 | Phiên bản SDK: minSdk, targetSdk, compileSdk | (1) Gọi API 26 trên máy API 24 thì NoSuchMethodError. (2) Tăng targetSdk lên 31, cài app thất bại vì một Activity có intent filter mà thiếu `android:exported` | `platform.sdk`: chọn phiên bản máy × targetSdk → luật nào áp dụng | **Ma trận** phiên bản máy × targetSdk; mỗi ô ghi luật áp dụng (ví dụ quyền thông báo: hệ thống tự hỏi hay app phải xin) | BNR ch.8; uses-sdk; App compatibility; behavior changes 14/15/16 |

### Phần 2: Màn hình
| Id | Chương | Lỗi dẫn dắt | Sim | Hình chính (vì sao hợp) | Nguồn chính |
|---|---|---|---|---|---|
| m4 | Vòng đời Activity | Dừng cập nhật vị trí trong `onDestroy`, nhưng khi bị giết ở nền thì `onDestroy` không chạy, GPS bật mãi. Hoặc dừng ở `onPause` thì khi chia đôi màn hình, app vẫn hiện mà bản đồ đứng im (đúng với Android 7–9; từ Android 10 có multi-resume, phải kiểm lại khi viết) | `platform.lifecycle`: thao tác (mở, Home, Back, xoay, mở Activity B, Activity trong suốt che lên, multi-window, khóa màn hình, giết từ Recents) → chuỗi callback của A và B | **Làn thời gian** hai Activity A và B, có **thang trạng thái** (CREATED, STARTED, RESUMED); thấy A.onPause chạy trước B.onCreate và A.onStop chạy sau B.onResume | BNR ch.3, ch.7; Pro Android ch.3; Activity lifecycle; State changes |
| m5 | Thay đổi cấu hình và giữ state | (1) Xoay màn hình mất bộ lọc vừa chọn. (2) Lưu danh sách 2 000 lịch hẹn vào saved state thì TransactionTooLargeException khi app vào nền | `platform.state`: sự kiện (xoay, đổi ngôn ngữ, Back, process bị giết, cập nhật app) × nơi giữ state (biến trong Activity, ViewModel, SavedStateHandle, rememberSaveable, DB) | **Ma trận** nơi giữ × sự kiện; ô sáng dần theo từng bước, ô "mất" tô đỏ. Kèm **thanh** kích thước Bundle so với giới hạn | BNR ch.4; Kickstart ch.2; Runtime changes; Saving states; ViewModel SavedState; TransactionTooLargeException; cầu nối G3, I2, Runtime (rememberSaveable) |
| m6 | Intent và intent filter | (1) Bấm link `henkham://lich/123` trong SMS mà app không mở, vì filter thiếu category BROWSABLE. (2) Lên targetSdk 30, nút "Mở bản đồ" biến mất vì `resolveActivity` trả null khi thiếu `<queries>` | `platform.intent`: một Intent đi qua ba phép thử với từng filter đã khai báo trên máy | **Bảng loại dần**: hàng là filter của các app, cột là phép thử action, category, data; ô trượt tô đỏ, filter còn lại được chọn hoặc hiện bảng chọn app | BNR ch.7, ch.16; Pro Android ch.3; Kickstart ch.5; Intents and filters; Common intents; Package visibility; Activity result; App Links |
| m7 | Task và back stack | (1) Bấm thông báo ba lần thì có ba màn hình chi tiết chồng nhau. (2) Mở từ deep link, bấm Back thì thoát app thay vì về danh sách | `platform.task`: chuỗi lần mở với launch mode và cờ (NEW_TASK, CLEAR_TOP, SINGLE_TOP), rồi bấm Back | **Dãy ô dọc** các task, mỗi task một chồng Activity; Activity mới trượt vào và Back lấy ra từ đỉnh | BNR ch.7 (Back); Pro Android ch.2–3 (task, cờ); Tasks and back stack; Notifications navigation |
| m8 | Fragment: hai vòng đời | (1) Quan sát dữ liệu bằng `this` thay vì `viewLifecycleOwner`, quay lại từ back stack thì nhận cập nhật hai lần. (2) Giữ binding sau `onDestroyView` thì rò rỉ cả cây view | `platform.fragment`: replace kèm addToBackStack rồi Back; vòng đời Fragment và vòng đời view đi tách nhau | **Làn thời gian** hai làn: Fragment và view của nó; đoạn "Fragment còn sống nhưng view đã chết" được tô | BNR ch.9, ch.13–14; Pro Android ch.9; Fragment lifecycle; FragmentManager; Communicate |
| m9 | Component biết vòng đời: Lifecycle của Jetpack | Gọi tay `start()`/`stop()` ở năm màn hình, quên một chỗ; callback tới sau `onStop` rồi cập nhật UI đã ẩn | `platform.observer`: một observer tự bật ở STARTED và tắt khi xuống CREATED; ProcessLifecycleOwner báo cả app vào nền | **Sơ đồ trạng thái** (state và event của Lifecycle), node đang đứng có viền, observer đi theo | Kickstart ch.12; Lifecycle-aware components; cầu nối A8 (repeatOnLifecycle) |

### Phần 3: Việc khi không có màn hình
| Id | Chương | Lỗi dẫn dắt | Sim | Hình chính (vì sao hợp) | Nguồn chính |
|---|---|---|---|---|---|
| m10 | Hệ thống hạn chế chạy nền: Doze, App Standby, giới hạn theo phiên bản | Handler "đồng bộ mỗi 5 phút" chạy tốt khi test, nhưng qua đêm gần như không chạy | `platform.doze`: máy nằm yên và tắt màn hình qua nhiều giờ; Doze vào sâu dần, có cửa sổ bảo trì; app nằm ở bucket khác nhau | **Làn thời gian** đêm dài: các đoạn Doze và cửa sổ bảo trì; việc nền chỉ chạy trong cửa sổ. Kèm **bảng** bucket → giới hạn (số liệu lấy từ tài liệu, ghi phiên bản) | Doze and standby; App Standby buckets; Oreo background limits; Background work overview |
| m11 | Service: started, bound, foreground | (1) `startService` khi app ở nền thì IllegalStateException (Android 8 trở lên). (2) Lên targetSdk 34, service chỉ đường crash vì thiếu kiểu `location` | `platform.service`: chuỗi start, bind, unbind, stop; khi nào `onDestroy` chạy; foreground cần thông báo và kiểu | (1) **Bảng** chuỗi thao tác → trạng thái service, ô "bị hủy" chỉ sáng khi đã stop và không còn client bind. (2) **Ma trận** kiểu foreground service × quyền cần | Pro Android ch.4; Programming Android ch.3; Services; Foreground services; FGS types; Bound services |
| m12 | BroadcastReceiver | (1) Receiver khai báo trong manifest cho một implicit broadcast không bao giờ được gọi (targetSdk 26 trở lên). (2) Gọi mạng trong `onReceive`, process bị giết giữa chừng | `platform.broadcast`: nguồn phát (hệ thống, app khác, chính app) × cách đăng ký → có được nhận không | **Ma trận** broadcast × cách đăng ký (manifest, trong mã, exported hay không), ô là "nhận", "bị chặn" hoặc "ngoại lệ được miễn" | Pro Android ch.5; Broadcasts; Background broadcasts; Oreo background limits |
| m13 | WorkManager và AlarmManager: chọn đúng công cụ | (1) Lời nhắc khám đặt bằng WorkManager tới trễ 40 phút. (2) Mỗi lần mở app lại enqueue một worker đồng bộ, nên có mười worker chạy song song | `platform.work`: (1) **cây quyết định** chọn công cụ; (2) một worker qua ràng buộc, retry với backoff, unique work (KEEP, REPLACE, APPEND) | (1) **Cây quyết định**: cần chạy khi app đóng? cần đúng giờ? có ràng buộc mạng? → coroutine, WorkManager, alarm chính xác, foreground service. (2) **Làn thời gian** các lần thử có backoff | BNR ch.22; Pro Android ch.8 (JobScheduler, AlarmManager); Persistent work; Alarms; cầu nối H7, L7 |
| m14 | Thông báo | (1) Trên Android 13, lời nhắc không bao giờ hiện vì chưa xin POST_NOTIFICATIONS. (2) Mọi thông báo đều mở cùng một lịch hẹn vì PendingIntent cùng request code | `platform.notify`: tạo kênh → xin quyền → dựng thông báo → người dùng bấm → PendingIntent → Activity kèm back stack | **Sơ đồ tuần tự** app, hệ thống thông báo, người dùng, Activity. Kèm **ma trận** mức quan trọng × hành vi (âm thanh, hiện nổi, thanh trạng thái) | BNR ch.22; Pro Android ch.8 (Notifications); Notifications; Channels; Notification permission; Navigation; PendingIntent; cầu nối I9 |

### Phần 4: Quyền và chia sẻ
| Id | Chương | Lỗi dẫn dắt | Sim | Hình chính (vì sao hợp) | Nguồn chính |
|---|---|---|---|---|---|
| m15 | Quyền | (1) Xin quyền camera mỗi lần mở; sau hai lần từ chối, hộp thoại không hiện nữa và nút chụp im lặng. (2) Xin vị trí nền cùng lúc với vị trí chính xác nên bị bỏ qua (Android 11 trở lên) | `platform.permission`: luồng kiểm tra → giải thích lý do → xin → cho phép, từ chối, hoặc từ chối vĩnh viễn; đổi phiên bản máy | (1) **Sơ đồ luồng** xin quyền, nhánh đang đi có viền. (2) **Bảng** các lần xin: lần, người dùng chọn gì, lần sau hệ thống còn hiện hộp thoại không | Pro Android ch.7; BNR ch.17 (khai báo feature); Permissions overview; Requesting; Usage notes; cầu nối H8 |
| m16 | ContentProvider và chia sẻ tệp | (1) Gửi `file://` cho Camera thì FileUriExposedException (targetSdk 24 trở lên). (2) Gửi `content://` nhưng thiếu cờ cấp quyền nên Camera không ghi được ảnh | `platform.share`: ba cách đưa đường dẫn ảnh cho Camera (file://, content:// thiếu cờ, content:// đủ cờ); cấp quyền URI hết hạn khi nào | **Sơ đồ tuần tự** Hẹn Khám, FileProvider, app Camera; quyền URI tạm thời hiện như một vé có hạn. Kèm **ghi chú** provider được tạo trước `Application.onCreate` (nối về m1) | BNR ch.17; Pro Android ch.6; Content providers; File sharing setup; FileProvider; cầu nối H8, I2 |
| m0 | Bản đồ track (viết CUỐI) | Gặp triệu chứng X thì xem chương nào | `platform.map` | **Bảng tra** triệu chứng → lộ ra ở đâu → chương, cùng mẫu với L0 và P0 | — |

Khuôn mỗi chương giống track L:
- tối đa 8 mục, gồm: vấn đề, giảng từng bước, dưới mui xe, kiểm chứng bằng `adb` (ví dụ `am start`, `am kill`, `dumpsys activity activities`, `dumpsys deviceidle force-idle`, `cmd jobscheduler`);
- 2 lỗi thật;
- 1 bài tập;
- quiz 3–4 câu.

Bài tập dự kiến:
- m4: đoán thứ tự callback;
- m6: filter nào khớp Intent này;
- m7: chồng Activity sau chuỗi lần mở;
- m11: khi nào service bị hủy;
- m13: chọn công cụ cho bốn việc;
- m15: lần xin thứ ba có hiện hộp thoại không.

## Cầu nối dự kiến (đánh số tiếp từ X36)
- m1 ↔ L l10 (main thread, ANR), I i11 (khởi động), Coroutines (Dispatchers.Main).
- m2 ↔ L l8, G g6 (singleton giữ Activity context).
- m5 ↔ G g3 (ViewModel, sự kiện), I i2 (process bị giết), Runtime (rememberSaveable).
- m9 ↔ Coroutines A8 (repeatOnLifecycle).
- m10, m13 ↔ H h7 (đồng bộ nền), L l7 (trạng thái worker), I i4 (polling và pin).
- m14 ↔ I i9 (thông báo đẩy).
- m15, m16 ↔ H h8 (MediaStore, quyền ảnh).

## Năm câu hỏi đã có mặc định (người dùng đổi được)
1. **Vị trí trong danh sách:** order 65, đặt sau Kotlin và trước Kiến trúc, vì G, H, I dựa trên nó. Cách khác là đặt cuối danh sách (order 130).
2. **Fragment (m8):** giữ một chương ở mức vừa phải, để đọc và sửa dự án View cũ. App mới dùng một Activity với Compose.
3. **Lifecycle của Jetpack (m9):** tách thành chương riêng. Cách khác là gộp vào m4 để track còn 16 chương.
4. **ContentProvider (m16):** đưa vào dù không có trong danh sách người dùng gửi, vì nó là một trong bốn component và chụp ảnh qua Camera cần FileProvider. Trọng tâm là FileProvider và quyền URI; viết provider riêng chỉ nói ngắn.
5. **Thứ tự xây:** m1 → m16 theo số, m0 cuối cùng, như các track trước.
