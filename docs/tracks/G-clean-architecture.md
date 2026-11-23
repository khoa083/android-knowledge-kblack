# TRACK G — Kiến trúc app Android / Android App Architecture (`arch`)

> **ĐÃ DUYỆT (2026-11-23).** Người dùng duyệt dàn chương bên dưới. Hai câu hỏi cuối chưa có trả lời nên theo đề xuất: **giữ g11** và **chỉ dạy Hilt**. Người dùng có thể đổi hai điều này bất cứ lúc nào.
> Track id `arch`, mã G, order 70, đang viết: **G1 xong** (2026-11-23), **G2 xong** (2026-11-24), **G3 xong** (2026-11-24), **G4 xong** (2026-11-24), **G5 xong** (2026-11-24), hết Phần 1; **G6 xong**, **G7 xong**, **G8 xong**, **G9 xong**, **G10 xong** (2026-11-24); tiếp theo G11.
> Cập nhật 2026-11-24: thêm cột **Hình chính** cho từng chương. Kiểu hình nào hợp thì mình tự chọn (người dùng cho phép, xem `docs/chapter-template-v2.md`, mục "Chọn kiểu hình").
> Nguyên tắc chọn nội dung giống track Kotlin: **cần và đủ**, không bám từng chương sách. Mỗi chương bắt đầu từ một lỗi thật trên Android.

## Nguồn đã đọc để soạn dàn ý
- **Chính thức (thắng khi mâu thuẫn), đã kiểm HTTP 200.** Các trang trên developer.android.com:
  - Guide to app architecture (`topic/architecture`);
  - UI layer, UI events, State holders, Domain layer, Data layer;
  - Offline-first, Recommendations;
  - Dependency injection (`training/dependency-injection`);
  - Modularization (`topic/modularization`).
- **Sách (đã đọc mục lục thật):**
  - Dumbravan, *Clean Android Architecture* (Packt): data source (Retrofit, Room, DataStore), lifecycle và Compose, DI (Dagger 2, Hilt), domain, repository, data source, MVVM, MVI, nhiều module, kiểm thử instrumentation.
  - Boudjnah, *Clean Architecture for Android*:
    - nguyên lý và các tầng (domain, presentation, UI, data, navigation);
    - unit test, end-to-end test;
    - failure và exception;
    - thêm tính năng, di trú từ MVP/MVVM;
    - "bits and bobs" (trùng lặp, model dùng chung giữa các tầng…).
  - Dùng có chọn lọc:
    - *Dagger by Tutorials*: DI, Hilt.
    - *Advanced Android App Architecture* (RW, Kotlin 1.3, đã cũ): chỉ để đối chiếu MVP/MVVM/MVI.
    - *Fundamentals of Software Architecture*: chỉ phần đánh đổi kiến trúc.
    - Martin, *Clean Architecture*: chỉ Dependency Rule (ch.22). SOLID và nguyên lý thành phần thuộc track **J**.

## Điểm lệch cần nói rõ trong track
Hướng dẫn chính thức của Google và hai sách Clean Architecture không đặt trọng tâm giống nhau:
- **Google:** app có **ít nhất hai tầng (UI và data)**, **business logic nằm ở data layer**, còn **domain layer là tùy chọn**.
- **Hai sách:** đặt **domain (entity, use case) ở trung tâm**, và mọi phụ thuộc hướng vào nó.

Track dạy theo hướng dẫn chính thức. Cách của sách được trình bày như một lựa chọn, có ghi tên tác giả và nói rõ khi nào nó đáng với chi phí bỏ ra.

## IN (đưa vào) và lý do
| Nội dung | Lý do |
|---|---|
| Tách mối quan tâm, SSOT, luồng dữ liệu một chiều (UDF), UI dẫn từ model | Nguyên lý chính thức; gốc của lỗi "dữ liệu lệch" và "không test được" |
| UI layer: UiState, state holder (ViewModel), sự kiện UI | Lỗi hay gặp: sự kiện một lần (Toast, điều hướng) bị phát lại hoặc mất khi xoay màn hình |
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
| Room, DataStore, SQLite chi tiết | Thuộc track **H** (Saving Data); ở đây chỉ coi chúng là data source |
| Retrofit/OkHttp chi tiết | Thư viện mạng, không phải kiến trúc; chỉ nhắc như remote data source. Cache HTTP, retry, phân trang thuộc track **I** |
| Dagger 2 thuần (component, subcomponent, multibinding) | Hilt đủ cho app thông thường; Dagger thuần chỉ là "đọc thêm" |
| SOLID, nguyên lý thành phần (cohesion, coupling), TDD | Thuộc track **J** (Clean Code); G2 và G9 chỉ dẫn link |
| Coroutines, Flow, StateFlow, thu thập theo vòng đời | Đã có ở track **Coroutines** (A7, A8, A9): chỉ dẫn link |
| State hoisting trong Compose, kiểm thử UI Compose | Đã có ở track **Runtime** (SH, B9): chỉ dẫn link |
| `by viewModels()`, sealed UiState, ngoại lệ trong Kotlin | Đã có ở track **Kotlin** (K11, K5, K6): chỉ dẫn link |
| MVP, MVC, VIPER | Mẫu cũ; chỉ một đoạn lịch sử và phần di trú |
| Navigation-Compose chi tiết | Thư viện riêng; chỉ nói điều hướng là một sự kiện UI |
| Đa nền tảng (KMP), xử lý quyền (permission) | Ngoài phạm vi kiến trúc app Android |
| Kiểu kiến trúc hệ thống lớn (microservice, event-driven…) | Thuộc track **I** (Mobile System Design), và ở đó cũng chỉ ở phía client |

## Chương (12)
Cột **Hình chính** là tab mặc định của chương. Sơ đồ node của sim vẫn có ở tab phụ. Kiểu hình đánh dấu **MỚI** cần viết cách vẽ riêng (xem `docs/chapter-template-v2.md`).

### Phần 1: Nền tảng (người mới, đã đọc Kotlin K1–K7)
| Id | Chương | Lỗi dẫn dắt | Sim | Hình chính (vì sao hợp) | Nguồn chính |
|---|---|---|---|---|---|
| g1 ✅ | Vì sao cần kiến trúc | Activity làm mọi thứ: xoay màn hình mất dữ liệu, không test được, đổi API phải sửa khắp nơi | `arch.god` (đã làm) | Luồng: một thao tác đi qua Activity-làm-tất-cả so với các tầng, kèm số đo "chỗ phải sửa" | Guide to app architecture; Dumbravan ch1; Boudjnah ch1 |
| g2 ✅ | Các tầng, hướng phụ thuộc, SSOT, UDF | Repository import một lớp UI; hai nơi cùng sửa một dữ liệu | `arch.layers`: thêm một phụ thuộc sai chiều; hai nơi cùng ghi | (1) **Đồ thị phụ thuộc MỚI** cho phần tầng: cạnh sai chiều tô đỏ, vì hướng mũi tên mới là điều cần thấy. (2) **Vòng** cho phần UDF: sự kiện đi lên, state đi xuống | Guide to app architecture; Boudjnah ch2; Martin *Clean Architecture* ch22 (Dependency Rule) |
| g3 ✅ | UI layer: UiState, ViewModel, sự kiện | Toast "Đặt lịch thành công" hiện lại sau khi xoay màn hình | `arch.uiEvents`: sự kiện → ViewModel → state → UI qua một lần xoay màn hình; sự kiện là state so với Channel | **Làn thời gian**: làn UI, ViewModel, vòng đời Activity; thấy Activity cũ chết, Activity mới đọc lại state, và sự kiện "rơi" vào chỗ nào | UI layer; UI events; State holders; Boudjnah ch3 |
| g4 ✅ | Data layer: repository, data source, offline-first | Danh sách hiện dữ liệu cũ dù mạng đã trả mới | `arch.ssot`: đọc từ DB làm SSOT; làm mới từ mạng thì ghi vào DB; UI quan sát DB | **Làn thời gian** ba làn mạng, DB, UI: thấy UI chỉ đổi khi DB đổi | Data layer; Offline-first; Dumbravan ch6–7 |
| g5 ✅ | Domain layer (tùy chọn) và use case | Cùng một quy tắc "giờ hợp lệ" viết ở hai ViewModel và lệch nhau | `arch.useCase`: hai ViewModel tự viết quy tắc so với dùng chung một use case | (1) **Bảng**: quy tắc × nơi viết, ô lệch tô đỏ. (2) **Cây quyết định** "có cần use case không" | Domain layer; Dumbravan ch5; Boudjnah ch2 |

### Phần 2: Thực hành sâu
| Id | Chương | Lỗi dẫn dắt | Sim | Hình chính (vì sao hợp) | Nguồn chính |
|---|---|---|---|---|---|
| g6 ✅ | Dependency injection: thủ công và Hilt | Hai instance repository khác nhau; singleton giữ Activity context | `arch.di`: đồ thị tạo object theo scope (Singleton, ViewModel, Activity) | (1) **Đồ thị phụ thuộc MỚI** (dùng lại của g2), node tô màu theo scope; cạnh "dài hơn vòng đời" tô đỏ. (2) **Dãy ô** vòng đời của từng scope theo thời gian | Dependency injection (chính thức); Dagger by Tutorials; Dumbravan ch4 |
| g7 ✅ | MVVM và MVI | Màn hình vừa "đang tải" vừa "lỗi" | `arch.mvi`: intent → reducer → một state duy nhất, so với nhiều StateFlow riêng | (1) **Ma trận** tổ hợp loading × error × data: 8 ô, ô vô nghĩa tô đỏ. Ma trận cho thấy vì sao một state duy nhất loại được chúng. (2) **Vòng** intent, reducer, state | Dumbravan ch8–9 |
| g8 ✅ | Lỗi qua các tầng | IOException lọt lên UI làm crash; "HTTP 500" hiện cho người dùng | `arch.failure`: ngoại lệ ở data source → đổi thành Failure ở repository → UiState.Error | **Luồng** qua bốn tầng, kèm **bảng ánh xạ** ngoại lệ → Failure → câu cho người dùng | Boudjnah ch6; Kotlin K6 (cầu nối) |
| g9 ✅ | Module hóa | Feature A dùng lớp nội bộ của feature B; vòng phụ thuộc giữa module | `arch.modules`: đồ thị module, thêm một phụ thuộc sai | **Đồ thị phụ thuộc MỚI**: module là node; vòng phụ thuộc và cạnh feature → feature tô đỏ | Modularization (chính thức); Dumbravan ch8, ch10 |
| g10 ✅ | Kiểm thử theo tầng | Test ViewModel gọi mạng thật nên lúc qua lúc trượt | `arch.testing`: thay data source thật bằng fake ở từng tầng | **Ma trận** tầng × loại test (chạy ở JVM hay thiết bị, nhanh hay chậm, cần fake gì) | Boudjnah ch4–5; Dumbravan ch10; Coroutines A9 (cầu nối) |
| g11 | Thêm tính năng mới và di trú dự án cũ | Viết lại cả app để đổi kiến trúc rồi bỏ dở | `arch.feature`: tính năng "Hủy lịch" đi qua từng tầng; di trú từng màn từ MVVM cũ | (1) **Luồng** tính năng qua các tầng. (2) **Dãy ô** các màn hình được chuyển dần sang kiến trúc mới | Boudjnah ch7–8 |
| g0 | Bản đồ track (viết CUỐI) | Gặp triệu chứng X thì đọc chương nào | `arch.map` | **Bảng tra** triệu chứng → chương (giống K0) | — |

Mỗi chương theo khuôn đã dùng ở Kotlin:
- tối đa 8 mục: đoán trước, 3 mục cơ chế, 2 lỗi thật, 1 bài tập, tự trả lời, mục trung thực;
- quiz 3–4 câu.

Bài tập do site tự viết theo ý sách, vì không có sách bài tập riêng cho chủ đề này, và có ghi nguồn ý.

## Cầu nối dự kiến
- g2 ↔ J (SOLID, DIP): G dạy hướng phụ thuộc giữa các tầng, J dạy nguyên lý ở mức lớp.
- g3 ↔ Runtime SH (state hoisting), Coroutines A8 (thu thập theo vòng đời), Kotlin K5 (sealed UiState).
- g4 ↔ H h7 (đồng bộ nền): G dạy vai trò của repository, H dạy cơ chế lưu và đồng bộ.
- g6 ↔ Kotlin K11 (`by viewModels()` là ViewModelLazy).
- g8 ↔ Kotlin K6 (ngoại lệ, catch quá rộng).
- g9 ↔ J (nguyên lý thành phần, độ bất ổn định).
- g10 ↔ Coroutines A9 (kiểm thử coroutine), Runtime B9 (kiểm thử UI), J (TDD, thiết kế test).

## Hai câu hỏi đã có mặc định (người dùng đổi được)
1. Giữ g11 (thêm tính năng và di trú), track 12 chương.
2. DI chỉ dạy Hilt; Dagger thuần là "đọc thêm".
