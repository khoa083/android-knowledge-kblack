# TRACK G — Kiến trúc app Android / Android App Architecture (`arch`)

> **BẢN NHÁP – CHỜ DUYỆT (2026-11-23).** Chưa tạo manifest, model hay nội dung. Người dùng duyệt danh sách IN/OUT và dàn chương bên dưới trước khi bắt đầu.
> Nguyên tắc chọn nội dung giống track Kotlin: **cần và đủ**, không bám từng chương sách; mỗi chương bắt đầu từ một lỗi thật trên Android.

## Nguồn đã đọc để soạn dàn ý
- **Chính thức (thắng khi mâu thuẫn), đã kiểm HTTP 200:** developer.android.com: Guide to app architecture (`topic/architecture`), UI layer, UI events, State holders, Domain layer, Data layer, Offline-first, Recommendations, Dependency injection (`training/dependency-injection`), Modularization (`topic/modularization`).
- **Sách (đã đọc mục lục thật):**
  - Dumbravan, *Clean Android Architecture* (Packt): data source (Retrofit, Room, DataStore), lifecycle và Compose, DI (Dagger 2, Hilt), domain, repository, data source, MVVM, MVI, nhiều module, kiểm thử instrumentation.
  - Boudjnah, *Clean Architecture for Android*: nguyên lý và các tầng (domain, presentation, UI, data, navigation), unit test, end-to-end test, failure và exception, thêm tính năng, di trú từ MVP/MVVM, "bits and bobs" (trùng lặp, model dùng chung giữa các tầng…).
  - Dùng có chọn lọc: *Dagger by Tutorials* (DI, Hilt); *Advanced Android App Architecture* (RW, Kotlin 1.3, cũ: chỉ đối chiếu MVP/MVVM/MVI); *Fundamentals of Software Architecture* (chỉ phần đánh đổi kiến trúc).

## Điểm lệch cần nói rõ trong track
Hướng dẫn chính thức của Google: app có **ít nhất hai tầng (UI và data)**, **business logic nằm ở data layer**, **domain layer là tùy chọn**. Hai sách Clean Architecture đặt **domain (entity, use case) ở trung tâm** và mọi phụ thuộc hướng vào nó. Track dạy theo hướng dẫn chính thức, và trình bày cách của sách như một lựa chọn có ghi tên tác giả, kèm khi nào nó đáng chi phí.

## IN (đưa vào) và lý do
| Nội dung | Lý do |
|---|---|
| Tách mối quan tâm, SSOT, luồng dữ liệu một chiều (UDF), UI dẫn từ model | Nguyên lý chính thức; gốc của phần lớn lỗi "dữ liệu lệch" và "không test được" |
| UI layer: UiState, state holder (ViewModel), sự kiện UI | Lỗi hay gặp nhất: sự kiện một lần (Toast, điều hướng) bị phát lại hoặc mất khi xoay màn hình |
| Data layer: repository, data source, offline-first | Lỗi hai nguồn sự thật, cache và mạng lệch nhau |
| Domain layer tùy chọn và use case | Biết khi nào cần (logic dùng lại ở nhiều ViewModel) và khi nào chỉ là lớp chuyển tiếp thừa |
| Dependency injection: thủ công, rồi Hilt; scope và vòng đời | Lỗi scope sai: hai instance repository, giữ Activity trong singleton |
| MVVM và MVI | Lỗi trạng thái mâu thuẫn khi có nhiều luồng state riêng lẻ (đang tải mà cũng lỗi) |
| Lỗi và ngoại lệ đi qua các tầng | Crash do ngoại lệ mạng lọt lên UI; thông báo kỹ thuật lộ ra người dùng |
| Module hóa | Hướng dẫn chính thức; ranh giới giữa feature, vòng phụ thuộc giữa module |
| Kiểm thử theo tầng (fake, test ViewModel, end-to-end) | Lý do thật sự để có kiến trúc; test phụ thuộc mạng thật thì chập chờn |
| Thêm một tính năng từ đầu tới cuối, di trú dần dự án cũ | Gom mọi thứ lại; cách đổi kiến trúc mà không viết lại cả app |

## OUT (bỏ ra hoặc chỉ nhắc) và lý do
| Nội dung | Lý do |
|---|---|
| Room, DataStore, SQLite chi tiết | Thuộc track **Saving Data** (#6 lộ trình); ở đây chỉ coi chúng là data source |
| Retrofit/OkHttp chi tiết | Thư viện mạng, không phải kiến trúc; chỉ nhắc như remote data source |
| Dagger 2 thuần (component, subcomponent, multibinding) | Hilt đủ cho app thông thường; Dagger thuần chỉ là "đọc thêm" |
| Coroutines, Flow, StateFlow, thu thập theo vòng đời | Đã có ở track **Coroutines** (A7, A8, A9): chỉ dẫn link |
| State hoisting trong Compose, kiểm thử UI Compose | Đã có ở track **Runtime** (SH, B9): chỉ dẫn link |
| `by viewModels()`, sealed UiState, ngoại lệ trong Kotlin | Đã có ở track **Kotlin** (K11, K5, K6): chỉ dẫn link |
| MVP, MVC, VIPER | Mẫu cũ; chỉ một đoạn lịch sử và phần di trú |
| Navigation-Compose chi tiết | Thư viện riêng; chỉ nói điều hướng là một sự kiện UI |
| Đa nền tảng (KMP), xử lý quyền (permission) | Ngoài phạm vi kiến trúc app Android |
| Kiểu kiến trúc hệ thống lớn (microservice, event-driven…) | Thuộc track **Mobile System Design** (#7) |

## Chương (12)
### Phần 1: Nền tảng (người mới, đã đọc Kotlin K1–K7)
| Id | Chương | Lỗi dẫn dắt | Sim (sơ đồ node) | Nguồn chính |
|---|---|---|---|---|
| g1 | Vì sao cần kiến trúc | Activity làm mọi thứ: xoay màn hình mất dữ liệu, không test được, đổi API phải sửa khắp nơi | `arch.godActivity`: một thao tác "Đặt lịch" đi qua Activity-làm-tất-cả so với các tầng; đếm chỗ phải sửa khi đổi API | Guide to app architecture; Dumbravan ch1; Boudjnah ch1 |
| g2 | Các tầng, hướng phụ thuộc, SSOT, UDF | Repository import một lớp UI; hai nơi cùng sửa một dữ liệu | `arch.layers`: thêm một phụ thuộc sai chiều, trình biên dịch/module bắt hay không bắt | Guide to app architecture; Boudjnah ch2 |
| g3 | UI layer: UiState, ViewModel, sự kiện | Toast "Đặt lịch thành công" hiện lại sau khi xoay màn hình | `arch.uiEvents`: sự kiện → ViewModel → state → UI, qua một lần xoay màn hình; sự kiện như state so với Channel | UI layer; UI events; State holders; Boudjnah ch3 |
| g4 | Data layer: repository, data source, offline-first | Danh sách hiện dữ liệu cũ dù mạng đã trả mới | `arch.ssot`: đọc từ DB làm SSOT, làm mới từ mạng ghi vào DB, UI quan sát DB | Data layer; Offline-first; Dumbravan ch6–7 |
| g5 | Domain layer (tùy chọn) và use case | Cùng một quy tắc "giờ hợp lệ" viết ở hai ViewModel và lệch nhau | `arch.useCase`: hai ViewModel tự viết quy tắc so với dùng chung một use case; use case chỉ chuyển tiếp thì thừa | Domain layer; Dumbravan ch5; Boudjnah ch2 |
### Phần 2: Thực hành sâu
| Id | Chương | Lỗi dẫn dắt | Sim | Nguồn chính |
|---|---|---|---|---|
| g6 | Dependency injection: thủ công và Hilt | Hai instance repository khác nhau; singleton giữ Activity context | `arch.di`: đồ thị tạo object theo scope (Singleton, ViewModel, Activity) | Dependency injection (chính thức); Dagger by Tutorials; Dumbravan ch4 |
| g7 | MVVM và MVI | Màn hình vừa "đang tải" vừa "lỗi" | `arch.mvi`: intent → reducer → một state duy nhất, so với nhiều StateFlow riêng | Dumbravan ch8–9 |
| g8 | Lỗi qua các tầng | IOException lọt lên UI làm crash; "HTTP 500" hiện cho người dùng | `arch.failure`: ngoại lệ ở data source → đổi thành Failure ở repository → UiState.Error | Boudjnah ch6; Kotlin K6 (cầu nối) |
| g9 | Module hóa | Feature A dùng lớp nội bộ của feature B; vòng phụ thuộc giữa module | `arch.modules`: đồ thị module, thêm một phụ thuộc sai | Modularization (chính thức); Dumbravan ch8, ch10 |
| g10 | Kiểm thử theo tầng | Test ViewModel gọi mạng thật nên lúc qua lúc trượt | `arch.testing`: thay data source thật bằng fake ở từng tầng; test nào chạy nhanh, test nào cần thiết bị | Boudjnah ch4–5; Dumbravan ch10; Coroutines A9 (cầu nối) |
| g11 | Thêm tính năng mới và di trú dự án cũ | Viết lại cả app để đổi kiến trúc rồi bỏ dở | `arch.feature`: một tính năng "Hủy lịch" đi qua từng tầng; di trú từng màn từ MVVM cũ | Boudjnah ch7–8 |
| g0 | Bản đồ track (viết CUỐI) | Gặp triệu chứng X thì đọc chương nào | cây triệu chứng → chương | — |

Mỗi chương theo khuôn đã dùng ở Kotlin: tối đa 8 mục (đoán trước, 3 mục cơ chế, 2 lỗi thật, 1 bài tập, tự trả lời, mục trung thực), quiz 3–4 câu. Bài tập do site tự viết theo ý sách (không có sách bài tập riêng cho chủ đề này), ghi nguồn ý.

## Cầu nối dự kiến
- g3 ↔ Runtime SH (state hoisting), Coroutines A8 (thu thập theo vòng đời), Kotlin K5 (sealed UiState).
- g6 ↔ Kotlin K11 (`by viewModels()` là ViewModelLazy).
- g8 ↔ Kotlin K6 (ngoại lệ, catch quá rộng).
- g10 ↔ Coroutines A9 (kiểm thử coroutine), Runtime B9 (kiểm thử UI).

## Gợi ý kiểu sơ đồ (báo người dùng, chưa đổi)
g2 (hướng phụ thuộc giữa các tầng) và g9 (đồ thị module) là **đồ thị phụ thuộc**, không phải luồng bốn bước; có thể dễ hình dung hơn với bố cục đồ thị nhiều node thay cho pipeline bốn khối. Vẫn là sơ đồ node như quy định; chỉ đổi bố cục nếu người dùng đồng ý.

## Câu hỏi cần người dùng quyết
1. Có giữ g11 (thêm tính năng và di trú) không, hay gộp vào g0 để track còn 11 chương?
2. DI: chỉ Hilt (đề xuất), hay thêm một chương Dagger thuần?
