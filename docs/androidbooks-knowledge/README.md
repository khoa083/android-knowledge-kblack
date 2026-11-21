# AndroidBooks Knowledge Base

## Mục đích

Bộ ghi chú này giúp AI/người học tra nội dung Kotlin/Android/Compose từ `E:\AndroidBooks` mà không cần lập lại manifest hoặc dò lại toàn bộ mục lục. Đây là **knowledge base nguyên bản**, không phải bản sao toàn văn sách. Mỗi nhận định kỹ thuật quan trọng được giải thích bằng lời mới, có link tài liệu chính thức và/hoặc đường dẫn/chương/trang sách để kiểm tra.

## Đọc theo thứ tự

1. [ChatGPT roadmap v2](../chatgpt-roadmap-v2.md) — trình tự học và ranh giới với tài liệu Claude.
2. [Compose Runtime](compose-runtime.md) — state → invalidation → recomposition → apply.
3. [Kotlin Coroutines](coroutines-runtime.md) — suspension → continuation → scheduling/lifecycle.
4. [Compose Animation](compose-animation.md) — frame clock → math → state → phase.
5. [Learning methods](learning-methods.md) — cách trình bày và ôn tập có cơ sở nghiên cứu.
6. [Catalog](catalog.md) và [catalog.json](catalog.json) — danh sách tất cả nguồn và coverage.

## Quy tắc dùng cho AI kế tiếp

- Ưu tiên ghi chú này để có bản đồ và từ khóa; nếu cần chi tiết không có trong ghi chú, dùng `B###` trong catalog để tìm file gốc và phạm vi trang/chương.
- Không coi catalog/word-count là bằng chứng đã đọc hiểu mọi trang. Các PDF có lớp text được trích xuất toàn bộ, nhưng layout, code trong ảnh, sơ đồ, bảng, font lỗi và scans có thể mất.
- Với implementation/version-sensitive, kiểm tra nguồn Android Developers/Kotlin và AndroidX source hiện hành. Ghi nhánh/commit/ngày tra cứu.
- Không sửa `CLAUDE.md`, `docs/progress.md`, `docs/roadmap-v2.md`, `docs/research/*`, source, generator hoặc prompt files khi chỉ đang dùng knowledge base này.
- Tệp thư viện vẫn ở `E:\AndroidBooks`. Catalog lưu path tương đối bên trong kho cùng hash để định danh chính xác.

## Coverage lần quét

- Ngày lập manifest: **2026-11-21**.
- Đã tìm đệ quy và xử lý **150/150 tệp**: 76 PDF và 74 EPUB.
- Có **139 SHA-256 khác nhau**; 11 nhóm là các file trùng byte chính xác. Không tính mỗi bản trùng như một nguồn độc lập.
- Cả **76/76 PDF có outline/bookmarks** để lập bản đồ chương; EPUB dùng spine headings. Đây là mục lục điều hướng, không phải bằng chứng mọi trang đã được đọc thủ công.
- Trích xuất được khoảng **14,269,536 từ** nếu tính cả bản trùng; **13,661,831 từ** khi tính nội dung có SHA-256 trùng một lần. Con số này đo lượng text lấy ra được, không đo mức độ con người/AI đã đọc sâu.
- Có **một lỗi ở trang PDF p.70** của `design/Thinking with Type...pdf` do giới hạn token stream của parser; các tệp khác hoàn tất vòng trích xuất nhưng một số trang có text rỗng/font/diagram.
- Các mục PDF cần OCR/đối chiếu bổ sung vì gần như không có lớp text: `Android App Distribution.pdf` (274 trang, 19 từ; có bản trùng), `Android Debugging by Tutorials...pdf` (214 trang, 0 từ; có bản trùng), `The Designers Dictionary of Color...pdf` (257 trang, 0 từ), `Functional Programming in Kotlin by Tutorials...pdf` (567 trang, 139 từ; có bản trùng), `Kotlin Multiplatform by Tutorials.pdf` (400 trang, 85 từ; có bản trùng). `Understanding Distributed Systems, 2nd ed` có 43/346 trang ít text; `Laws of UX` có 19/186 trang ít text. Không có engine OCR cài sẵn trong môi trường ở lần quét này.
- Có **7 PDF nội dung duy nhất** được đánh dấu `PARTIAL` (11 file khi tính các bản trùng). Catalog ghi cụ thể số trang ít text và outline của từng file.
- EPUB/PDF bản trùng chính xác được liệt kê riêng. Những sách có hai định dạng khác nhau không bị gộp chỉ vì giống tiêu đề.

## Nguồn chủ đề chính

| Chủ đề | Nguồn sách trong kho | Vai trò |
|---|---|---|
| Coroutines core | `deep_dive_kotlin/kotlin/Kotlin Coroutines  Deep Dive.pdf`; `Kotlin Coroutines by Tutorials.pdf` | ToC, state machine/CPS, library, cancellation, Flow, testing và ví dụ Android |
| Compose basics/state/lifecycle | `Android UI Development with Jetpack Compose/...pdf`; `Jetpack Compose by Tutorials (Second Edition)/...pdf`; `Jetpack Compose 1.3 Essentials/...pdf` | Giảng từ declarative UI đến state/effects/accessibility/testing; các bản cũ dùng cho fundamentals |
| Android/Compose animation | `Android Animations by Tutorials...pdf`; ch.12 `Jetpack Compose by Tutorials` | Từ View animation để so sánh sang API Compose |
| Architecture/data/systems | Các sách trong `Clean Android Architecture`, `deep_dive_kotlin/system-design`, `distributed-systems`, `Fundamentals of Software Architecture` | Bối cảnh để nối concurrency/UI với lifecycle, persistence và thiết kế hệ thống |
| UX/accessibility/design | `Android Accessibility by Tutorials`, các sách `UX`, `UI`, `design` | Hỗ trợ semantics, khả năng tiếp cận, information hierarchy và bài học trực quan |
| Kotlin/software practice | `deep_dive_kotlin/kotlin`, các sách algorithms/testing/debugging/craft | Nền ngôn ngữ, reasoning, test và sửa bug |

Roadmap ChatGPT hiện có outline cho toàn bộ các track trong lộ trình, còn ghi chú chuyên sâu hiện ưu tiên Coroutines, Compose Runtime và Compose Animation. Catalog liệt kê đủ mọi file và mục lục điều hướng; nó không giả vờ rằng mọi sách đã được tóm tắt theo từng trang.
