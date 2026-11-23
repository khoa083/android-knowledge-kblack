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
