# Prompt để bắt đầu phiên tiếp theo (dán vào Claude Code, thư mục E:\AndroidDeepDiveExplorer)

```
Đọc CLAUDE.md, docs/progress.md và docs/roadmap-v2.md trước. Đây là lộ trình v2: viết lại nội dung thật chi tiết, đầy đủ và dễ hiểu cho người mới, tập trung vào bản chất và cơ chế để tôi tự sửa được bug (kể cả những bug AI không nhìn ra). Không rút gọn, không ngại dài. Site chỉ để tôi tự học cá nhân, nên hãy tận dụng tối đa sách trong E:\AndroidBooks làm nguồn giảng chính.

Trách nhiệm nghiên cứu là của bạn:
- Bạn phải TỰ nghiên cứu: đọc kỹ chương sách liên quan, tài liệu chính thức (developer.android.com, kotlinlang.org, mã nguồn AndroidX/kotlinx.coroutines có ghi phiên bản/commit), và tìm trên internet các cách giảng dễ hiểu, các bài viết/bài giảng hay về cùng chủ đề, các nghiên cứu về cách học và cách làm minh hoạ/animation giảng dạy.
- Các tài liệu tôi đưa dưới đây chỉ là tham khảo, bổ trợ. Dùng chỗ nào giúp ích, kiểm chứng lại chỗ nào quan trọng, bổ sung chỗ còn thiếu. Không coi chúng là đủ hay là đúng tuyệt đối.

Tài liệu bổ trợ trong dự án:
- docs/visual-explainer-improvement-guide.md: khảo sát hai trang mẫu; quy tắc một bước học tốt (§3), chuyển động để giải thích (§4: một chuyển động chính + tối đa một tín hiệu phụ, tách thời gian mô phỏng với thời gian animation, dừng khi tab ẩn), điều khiển cho người mới (§5), checklist đánh giá mô phỏng (§8). Phần số liệu khảo sát là ghi chú có ngày, không phải hợp đồng. Anime.js: KHÔNG thêm (dự án cấm thư viện ngoài).
- docs/androidbooks-knowledge/learning-methods.md: khung micro-cycle "đoán → xem một bước → giải thích vì sao → kiểm tra bằng ví dụ khác → tự nhớ lại sau một khoảng nghỉ"; retrieval, spacing, worked example → fading, self-explanation, interleaving sau nền tảng, transfer bằng bug mới. Giữ đúng sắc thái bằng chứng (không tuyên bố quá mức).
- docs/androidbooks-knowledge/coroutines-runtime.md, compose-runtime.md, compose-animation.md: ghi chú cơ chế + bug thường gặp + chương sách đã đối chiếu.
- docs/androidbooks-knowledge/catalog.md: mục lục điều hướng (PDF bookmarks/EPUB spine, kèm số trang PDF) của toàn bộ 150 sách, mã B###. Dùng nó để tìm nhanh phạm vi trang của từng chương rồi đọc sách thật (Read với pages). Lưu ý các PDF gần như không có lớp text (vd. Functional Programming in Kotlin by Tutorials, Kotlin Multiplatform by Tutorials, Android Debugging by Tutorials): phải đọc dạng ảnh trang hoặc dùng bản epub nếu có.
- KHÔNG dùng docs/chatgpt-roadmap-v2.md (roadmap độc lập, dễ xung đột với docs/roadmap-v2.md).

Thứ tự ưu tiên khi có khác biệt: CLAUDE.md, E:/AndroidDeepDiveExplorer-Prompts/00-MASTER-PROMPT.md, STYLE-REFERENCE.md, track spec, docs/core-api.md và quyết định đã ghi trong docs/progress.md, docs/roadmap-v2.md đứng trên các ghi chú bổ trợ. Không sửa đặc tả hay roadmap chỉ để khớp với ghi chú ChatGPT. Khi dùng kết quả khảo sát, ghi rõ điều gì là quan sát, suy luận hay chưa xác minh.

Giữ nguyên: hai chế độ Guided Deep-Dive và Live Explorer (không thêm mode), bố cục ba vùng, chạy offline/file:// (không fetch, không ES module, không CDN/webfont, không thư viện ngoài, không build step), song ngữ vi/en cùng cây key, model thuần chỉ phát message key, lõi không chứa id track. Không sao chép mã, hình, câu chữ hay giao diện của hai trang mẫu.

Minh hoạ và phương pháp học (mọi chương):
- Hình và animation phải dễ hiểu với người mới: mỗi hình một ý, có "Bạn đang xem gì?" và chú giải; đi từng bước (Step trước, Play là tuỳ chọn); ẩn dụ đời thường trước rồi nói rõ phần nào của ẩn dụ khớp/không khớp với implementation; hình khớp đúng dòng mã đang giảng; tắt chuyển động vẫn hiểu được. Chuyển động và chuyển cảnh: làm theo docs/design-principles.md §5.1 (quyết định của người dùng 2026-11-22: site phải sinh động; KHÔNG gỡ các chuyển cảnh đã có; §5.1 thắng §4 của hướng dẫn bổ trợ khi mâu thuẫn). Sim mới phải có chuyển động thật giữa các bước (movingSignals, nodeStates đổi, thanh lanes chạy liên tục), không chỉ đổi chữ.
- Gắn phương pháp học vào khung chương: câu hỏi dự đoán trước Step; câu nhớ lại cuối mỗi mục; worked example rồi bài khuyết bước; hỏi "vì sao"; ôn chương cũ ở đầu chương mới; bug mới để chuyển giao. (Thẻ ôn lặp lại ngắt quãng lưu localStorage là việc RIÊNG, làm sau khi xong Coroutines v2.)

An toàn git: chạy git status trước khi sửa; chỉ git add đúng các file mình đã sửa (không dùng git add -A, không đưa file người dùng tự thêm vào commit); chỉ commit chương đã hoàn chỉnh và đã qua kiểm tra.

Việc của phiên này: Coroutines v2 (ưu tiên số 1).
0. Với mỗi chương, ghi bảng theo dõi nguồn vào docs/research/coroutines.md: sách/chương/trang đã đọc, tài liệu chính thức, phiên bản/commit mã nguồn, và claim nào dựa trên nguồn nào (phân biệt API ổn định với chi tiết implementation).
1. Lấy mục lục thật của "Kotlin Coroutines: Deep Dive" (catalog.md, rồi kiểm lại các trang đầu PDF) và sửa dàn chương Coroutines v2 trong docs/roadmap-v2.md cho khớp. Đọc kỹ từng chương sách, đối chiếu tài liệu chính thức và mã nguồn kotlinx.coroutines, tìm thêm cách giảng hay trên mạng, trước khi viết chương tương ứng. Dùng "Kotlin Coroutines by Tutorials.pdf" để lấy ví dụ Android.
2. Thiết kế khung chương dài một lần, dùng lại cho mọi track: vấn đề → giảng từng bước có ví dụ và output → dưới mui xe → sim → bug thường gặp (triệu chứng → nguyên nhân cơ chế → sửa) → bài tập có lời giải → tự kiểm. Phần sư phạm ghi vào docs/chapter-template-v2.md (không trộn vào core-api.md). Nếu cần loại key/mục mới (vd. sec.*.bug, sec.*.exercise, câu dự đoán), thêm hỗ trợ hiển thị vào lõi theo cách CHUNG cho mọi track (không id track trong js/core, app.js) và ghi quy ước key đó vào docs/core-api.md mục 2. Track Coroutines chưa có generator: xem các generator trong dev/gen rồi tạo dev/gen/coroutines_content.py theo cùng quy ước (cùng cây key vi/en, NFC); trước khi thay nội dung, kiểm generator tái tạo đúng content.*.js hiện tại hoặc ghi rõ phần nào được viết lại.
3. Viết lần lượt từng chương, bắt đầu từ Phần 1 (vì sao cần coroutine; sequence builder; suspension hoạt động thế nào; coroutine dưới mui xe: CPS, state machine, continuation). Hết mỗi chương: chạy kiểm tra (dev/report.html, dev/tools/track-check.js, routes-check, focus-check), xem ảnh chụp sơ đồ, cập nhật docs/progress.md, git commit.
Trước mỗi chương (bắt buộc): đọc nội dung tài liệu chính thức và mã nguồn liên quan (WebFetch trang API/docs, mã nguồn kotlinx.coroutines/stdlib trên GitHub, ghi commit/phiên bản), tìm thêm cách giảng trên mạng, đọc phần tương ứng của Kotlin Coroutines by Tutorials; ghi vào bảng nguồn. Đóng các mục "chưa xác minh" của U1–U4 trong docs/research/coroutines.md trước khi viết Phần 2.
4. Làm liên tục tới gần hết limit. Trước khi hết: commit và ghi vào progress.md đang dừng ở đâu.

Sau Coroutines: Compose Runtime/Animation v2 → UX/UI v2 → các track mới (Kotlin, Clean Android Architecture, Saving Data, Mobile System Design, Clean Code, Functional Programming) theo docs/roadmap-v2.md. Mỗi track mới: lấy mục lục sách thật trước (catalog.md), làm theo E:\AndroidDeepDiveExplorer-Prompts\P-NEW-TRACK.md.
```
