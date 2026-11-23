# Nghiên cứu track G (Kiến trúc app Android)

Trang developer.android.com đọc ngày 2026-11-23. Sách: Dumbravan, *Clean Android Architecture* (Packt 2022; trang O'Reilly kiểm qua trình duyệt, trang Packt chặn bot nên không dùng); Boudjnah, *Clean Architecture for Android* (BPB). Nguồn chính thức thắng khi mâu thuẫn.

## G1 · Vì sao cần kiến trúc (2026-11-23)

| Khẳng định | Nguồn | Loại |
|---|---|---|
| Component có thể được khởi chạy riêng lẻ, không theo thứ tự, và bị hệ thống hay người dùng hủy bất cứ lúc nào; không giữ dữ liệu hay state trong component | `ax-arch-guide` | stable |
| Tách mối quan tâm là nguyên lý quan trọng nhất; UI dẫn từ model dữ liệu (tốt nhất là lưu bền); tối thiểu UI và data, domain tùy chọn | `ax-arch-guide` | stable |
| Đổi cấu hình: hệ thống gọi onDestroy, hủy Activity, tạo instance mới bằng onCreate | `ax-config-changes` | stable |
| ViewModel giữ state qua thay đổi cấu hình; sống tới khi ViewModelStoreOwner mất (Activity finish); SavedStateHandle giữ cả qua process death | `ax-viewmodel` | stable |
| Test local chạy trên máy phát triển, nhỏ và nhanh; instrumented chạy trên thiết bị thật hay giả lập | `ax-test-fundamentals` | stable |
| App cũ: HttpURLConnection, parse JSON, AsyncTask trong Activity; rò rỉ context; khó test, khó bảo trì khi lớn | `book-dumbravan` ch1 | guideline |
| Số file phải sửa (3 so với 1) | đếm trong app mẫu, ghi trong simp.1 và mục trung thực | simplified |

Kiểm URL: 4 trang developer.android.com HTTP 200 (curl); O'Reilly và BPB qua trình duyệt.

## G2 · Các tầng, hướng phụ thuộc, SSOT, UDF (2026-11-24)

| Khẳng định | Nguồn | Loại |
|---|---|---|
| Ít nhất hai tầng: UI hiển thị dữ liệu; data chứa business logic và lộ dữ liệu. Domain là tầng tùy chọn ở giữa, lớp gọi là use case | `ax-arch-guide`, `ax-domain-layer` | stable |
| Mũi tên trong sơ đồ của hướng dẫn là phụ thuộc giữa các lớp ("domain phụ thuộc lớp của data") | `ax-arch-guide` | stable |
| SSOT là chủ của dữ liệu, chỉ nó được sửa, lộ ra kiểu bất biến; lợi ích: gom thay đổi, bảo vệ dữ liệu, dễ lần lỗi; offline-first thường lấy database làm SSOT, có khi là ViewModel | `ax-arch-guide` | stable |
| UDF: state đi từ phạm vi rộng xuống phạm vi hẹp, sự kiện đi ngược lên tới SSOT | `ax-arch-guide` | stable |
| Vòng UDF ở tầng UI: ViewModel giữ và lộ state, UI báo sự kiện, ViewModel cập nhật state, state quay về UI | `ax-ui-layer` | stable |
| Repository là lối vào duy nhất của data layer; state holder không nhận thẳng data source; mỗi repository một SSOT; dữ liệu lộ ra bất biến | `ax-data-layer` | stable |
| Use case thường phụ thuộc repository | `ax-domain-layer` | stable |
| internal: thấy trong cùng module; module là tập file biên dịch cùng nhau (vd. Gradle source set) | `kt-visibility` | stable |
| Module cho phép kiểm soát chặt phần lộ ra (internal/private) | `ax-modularization` | stable |
| Hai module không thể gọi thẳng lẫn nhau vì phụ thuộc vòng, cần module trung gian; module cao và module cài đặt cùng phụ thuộc module trừu tượng | `ax-modularization-patterns` | stable |
| Dependency Rule: mũi tên là "biết về", hướng vào domain; đảo phụ thuộc bằng interface repository đặt cạnh use case, cài đặt nằm nơi khác | `book-boudjnah` ch1 | guideline |
| Domain là tầng trong cùng, gồm use case, mô hình domain, interface repository; nên dựa vào ít thư viện nhất có thể | `book-boudjnah` ch2 | guideline |
| Trong một module, import sai chiều vẫn biên dịch; khi tách module Gradle, import tới module không khai báo là lỗi biên dịch; Gradle không build vòng phụ thuộc giữa project | suy ra từ `kt-visibility` và `ax-modularization-patterns`; câu chữ lỗi trong sim là mô tả, không trích nguyên văn | simplified |

Kiểm URL: các trang developer.android.com và kotlinlang HTTP 200 (curl), tải về và đọc bản text ngày 2026-11-24. Boudjnah đọc từ epub trong kho (ch1, ch2).

## G3 · UI layer: UiState, ViewModel, sự kiện (2026-11-24)

| Khẳng định | Nguồn | Loại |
|---|---|---|
| Tầng UI gồm phần tử UI và state holder; UI state nên bất biến; ViewModel là cách khuyến nghị cho UI state mức màn hình, tự sống qua thay đổi cấu hình | `ax-ui-layer` | stable |
| ViewModel giữ state và thao tác qua tái tạo Activity; process death: SavedStateHandle giữ dữ liệu tối thiểu | `ax-stateholders` | stable |
| Sự kiện từ ViewModel luôn phải thành cập nhật UI state; tái hiện được sau thay đổi cấu hình, hành động UI không mất | `ax-ui-events` | stable |
| Thông báo đã được xem (đóng hay hết giờ) là đầu vào của người dùng; UI báo ViewModel để xóa userMessage | `ax-ui-events` | stable |
| Channel và stream khác không bảo đảm giao và xử lý khi ViewModel sống lâu hơn UI; nên thu thập khi UI ở foreground | `ax-ui-events` | stable |
| StateFlow luôn có giá trị, phát lại một giá trị mới nhất cho subscriber mới | `kx-stateflow-api` (kotlinx.coroutines 1.11.0) | stable |
| MutableSharedFlow() không replay, không buffer; emit trả về ngay khi không có subscriber; vắng subscriber chỉ giữ replay | `kx-sharedflow` (1.11.0) | stable |
| Thời điểm xoay và request xong trong sim | đặt sẵn để thấy từng trường hợp | simplified |

Kiểm URL: ui-layer/events, ui-layer/stateholders, ui-layer/state-production HTTP 200 (curl), đọc bản text 2026-11-24; trang API kotlinx (StateFlow, SharedFlow, MutableSharedFlow) HTTP 200, phiên bản ghi trên trang 1.11.0. Sách Boudjnah ch3 chưa đọc thân chương nên chưa trích.

## G4 · Data layer: repository, data source, offline-first (2026-11-24)

| Khẳng định | Nguồn | Loại |
|---|---|---|
| Tầng data gồm repository, mỗi cái gộp không hoặc nhiều data source; tầng khác không dùng thẳng data source; mỗi repository một nguồn sự thật | `ax-data-layer` | stable |
| App offline-first tối thiểu đọc được khi không có mạng; repository có mạng phải có nguồn cục bộ; ít nhất hai data source | `ax-offline-first` | stable |
| Nguồn cục bộ là nguồn sự thật chuẩn và là nơi duy nhất tầng trên đọc; nguồn mạng là trạng thái thật, hai bên có thể lệch nhau | `ax-offline-first` | stable |
| Đọc qua Flow từ nguồn cục bộ; chỉ báo người đọc bằng cách cập nhật nguồn cục bộ trước; ViewModel dùng stateIn | `ax-offline-first` | stable |
| Lỗi: catch trên Flow nguồn cục bộ; lỗi mạng thử lại với exponential backoff hay chờ có mạng | `ax-offline-first` | stable |
| Ghi qua suspend; ba chiến lược: chỉ online, hàng đợi, ghi lười; rút hàng đợi giao cho WorkManager | `ax-offline-first` | stable |
| Dữ liệu 9:00, 9:30, lịch 10:00 trong sim | ví dụ của site | simplified |

Kiểm URL: topic/architecture/data-layer/offline-first HTTP 200 (curl), đọc bản text 2026-11-24. Sách Dumbravan ch6–7 chưa đọc thân chương nên chưa trích.

## G5 · Domain layer (tùy chọn) và use case (2026-11-24)

| Khẳng định | Nguồn | Loại |
|---|---|---|
| Domain tùy chọn, gói logic phức tạp hay logic đơn giản dùng lại ở nhiều ViewModel; chỉ dùng khi cần | `ax-domain-layer` | stable |
| Lợi ích: tránh trùng lặp, dễ đọc, dễ test, tách lớp lớn | `ax-domain-layer` | stable |
| "Domain layer" của Android khác nghĩa domain trong Clean Architecture | `ax-domain-layer` | stable |
| Mỗi use case một việc, không chứa dữ liệu thay đổi; tên động từ + danh từ + UseCase; operator invoke; không có vòng đời riêng | `ax-domain-layer` | stable |
| Use case main-safe; việc nặng chuyển dispatcher hay để ở tầng data nếu cần cache | `ax-domain-layer` | stable |
| Gộp nhiều repository: use case; nếu Room tự gộp được thì repository riêng | `ax-domain-layer` | stable |
| Use case tốt hơn hàm tĩnh trong lớp Util | `ax-domain-layer` | guideline |
| Chặn UI truy cập data: lợi (không đi vòng analytics) và giá (use case chỉ chuyển tiếp); thêm khi cần | `ax-domain-layer` | guideline |
| Quy tắc giờ đặt được (60/120 phút, 7:00 tới 17:59) và cây quyết định | ví dụ và tóm tắt của site | simplified |

## G6 · Dependency injection: thủ công và Hilt (2026-11-24)

| Khẳng định | Nguồn | Loại |
|---|---|---|
| DI: nhận phụ thuộc từ ngoài (constructor, field); lợi: dùng lại, refactor, test; Hilt kiểm lúc biên dịch | `ax-di` | stable |
| DI thủ công: AppContainer dùng chung trong Application; không phải object singleton; singleton làm test khó | `ax-di-manual` | stable |
| Component Hilt theo lớp Android; vòng đời: Singleton (Application.onCreate tới hủy), Activity (onCreate tới onDestroy), ViewModel (cùng ViewModel) | `ax-hilt` | stable |
| Binding mặc định không scope (mỗi lần một instance); có scope thì một lần mỗi instance component; hạn chế scope | `ax-hilt` | stable |
| Binding mặc định: Singleton có Application; ViewModel có SavedStateHandle; Activity có Application, Activity; @ApplicationContext, @ActivityContext | `ax-hilt` | stable |
| Đưa Activity vào @Singleton thì lỗi biên dịch | suy ra từ bảng binding mặc định và quy tắc component cha con trong `ax-hilt` | simplified |

## G7 · MVVM và MVI (2026-11-24)

| Khẳng định | Nguồn | Loại |
|---|---|---|
| Một UI state cho các state liên quan: ít lệch hơn; hai luồng có thể một cái cập nhật, một cái chưa; thuộc tính suy ra từ nhiều trường | `ax-ui-layer` | stable |
| Một luồng hay nhiều luồng: tùy quan hệ; tách khi không liên quan hay khác tần suất; UiState nhiều trường có thể cần distinctUntilChanged | `ax-ui-layer` | stable |
| MVVM: View phụ thuộc ViewModel, ViewModel phụ thuộc Model, quan sát được; nhiều View dùng chung ViewModel | `book-dumbravan` ch.8 (epub, đọc 2026-11-24) | guideline |
| MVI: dữ liệu bất biến gộp thành một state; thay đổi qua luồng phản ứng; Intent khác android Intent; MVI xây trên ViewModel | `book-dumbravan` ch.9 | guideline |
| Tám tổ hợp L/E/D, năm tổ hợp có nghĩa, sealed state bốn trạng thái | định nghĩa của site cho màn Lịch của tôi | simplified |

## G8 · Lỗi qua các tầng (2026-11-24)

| Khẳng định | Nguồn | Loại |
|---|---|---|
| Tương tác với repository có thể thành công hay ném ngoại lệ; coroutine dùng try/catch khi phù hợp, Flow dùng catch; tầng data lộ lỗi bằng ngoại lệ riêng hay Result | `ax-data-layer` | stable |
| Lỗi trên màn hình là state, thường kèm thông điệp và hành động thử lại, mô hình bằng data class | `ax-ui-layer` | stable |
| Failure: dự đoán được, phục hồi được, xử lý như giá trị; exception: bất ngờ, cờ đỏ, ghi log và theo dõi; biết cách xử lý thì thành failure | `book-boudjnah` ch.6 (epub, đọc 2026-11-24) | guideline |
| Sealed class tốt hơn Boolean cho failure (đặt tên, mở rộng) | `book-boudjnah` ch.6 | guideline |
| catch (e: Exception) bắt cả CancellationException | sự thật về kiểu (CancellationException là một Exception); giải thích ở track Coroutines A5, Kotlin K6 | stable |
| HttpException, mã 409/500 | ví dụ với Retrofit | simplified |
