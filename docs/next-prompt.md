# Prompt để bắt đầu phiên tiếp theo (dán vào Claude Code, thư mục E:\AndroidDeepDiveExplorer)

Đọc CLAUDE.md, docs/progress.md và docs/roadmap-v2.md trước. Đây là lộ trình v2: viết lại nội dung thật chi tiết, đầy đủ và dễ hiểu cho người mới, tập trung vào bản chất và cơ chế để tôi tự sửa được bug. Không rút gọn, không ngại dài. Site chỉ để tôi tự học cá nhân, nên hãy tận dụng tối đa sách trong E:\AndroidBooks làm nguồn giảng chính, có thể tìm thêm cách giảng dễ hiểu trên mạng.

Minh hoạ và phương pháp học (áp dụng cho mọi chương):
- Hình minh hoạ và animation phải dễ hiểu với người mới: mỗi hình chỉ thể hiện một ý, có chú thích "bạn đang xem gì", đi từng bước (không chạy một mạch), dùng ẩn dụ đời thường trước rồi mới tới hình kỹ thuật, và hình phải khớp đúng với đoạn mã đang giảng.
- Trước khi viết, tìm hiểu các phương pháp tâm lý học / khoa học nhận thức giúp học sâu và ghi chúng vào docs/learning-methods.md, kèm nguồn. Ví dụ: retrieval practice (tự nhớ lại), spaced repetition (lặp lại ngắt quãng), elaboration (tự giải thích "vì sao"), dual coding (lời + hình), worked examples rồi mới làm bài, interleaving (trộn dạng bài), giảm cognitive load, Feynman technique, dự đoán trước khi xem kết quả. Sau đó áp dụng chúng vào khung chương: câu hỏi "đoán trước" trước mỗi sim, câu hỏi nhớ lại cuối mỗi mục, ôn lại chương cũ ở đầu chương mới, và nếu khả thi thì có thẻ ôn tập lặp lại ngắt quãng lưu trong localStorage.

Việc của phiên này: Coroutines v2 (ưu tiên số 1 trong roadmap).
1. Đọc mục lục thật của "E:\AndroidBooks\deep_dive_kotlin\kotlin\Kotlin Coroutines  Deep Dive.pdf" (các trang đầu) và sửa dàn chương Coroutines v2 trong roadmap cho khớp. Sau đó đọc kỹ từng chương sách trước khi viết chương tương ứng. Dùng thêm "Kotlin Coroutines by Tutorials.pdf" để lấy ví dụ Android.
2. Thiết kế khung chương dài trước (chỉ làm một lần, dùng lại cho mọi track): vấn đề → giảng từng bước có ví dụ và output → dưới mui xe → sim → bug thường gặp (triệu chứng → nguyên nhân → sửa) → bài tập có lời giải → tự kiểm. Viết bằng generator trong dev/gen. Giữ đúng ràng buộc: file://, không fetch, không ES module, song ngữ vi/en cùng cây key.
3. Viết lần lượt từng chương, bắt đầu từ Phần 1 (Vì sao cần coroutine; Sequence builder; Suspension hoạt động thế nào; Coroutine dưới mui xe: CPS và state machine). Hết mỗi chương: chạy kiểm tra (dev/report.html, dev/tools/track-check.js), cập nhật docs/progress.md, git commit.
4. Làm liên tục cho tới gần hết limit. Trước khi hết, commit và ghi vào progress.md đang dừng ở đâu.

Thứ tự sau Coroutines: Compose Runtime/Animation v2 → UX/UI v2 → các track mới (Kotlin, Clean Android Architecture, Saving Data, Mobile System Design, Clean Code, Functional Programming), như trong roadmap. Với mỗi track mới, đọc mục lục sách thật trước và làm theo E:\AndroidDeepDiveExplorer-Prompts\P-NEW-TRACK.md.
