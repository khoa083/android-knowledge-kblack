# Prompt để bắt đầu phiên tiếp theo (dán vào Claude Code, thư mục E:\AndroidDeepDiveExplorer)

```
Đọc CLAUDE.md, docs/progress.md và docs/roadmap-v2.md trước. Đây là lộ trình v2: viết lại nội dung thật chi tiết, đầy đủ và dễ hiểu cho người mới, tập trung vào bản chất và cơ chế để tôi tự sửa được bug. Không rút gọn, không ngại dài. Site chỉ để tôi tự học cá nhân, nên hãy tận dụng tối đa sách trong E:\AndroidBooks làm nguồn giảng chính, có thể tìm thêm cách giảng dễ hiểu trên mạng.

Tài liệu bổ trợ (đọc trước khi làm):
- docs/visual-explainer-improvement-guide.md: kết quả khảo sát hai website, nguyên tắc thiết kế mô phỏng, animation và cách hỗ trợ học sâu.
- docs/androidbooks-knowledge/learning-methods.md: phương pháp học (đọc khi chỉnh cách dạy và ôn tập).
- Ghi chú AndroidBooks đúng chủ đề khi viết nội dung kỹ thuật: docs/androidbooks-knowledge/coroutines-runtime.md, compose-runtime.md, compose-animation.md (danh mục sách: docs/androidbooks-knowledge/catalog.md).
- KHÔNG dùng docs/chatgpt-roadmap-v2.md (roadmap độc lập, dễ xung đột với roadmap-v2.md).

Đây là tài liệu bổ trợ và ghi chú khảo sát, không phải lệnh thay thế đặc tả. Trước khi áp dụng, đối chiếu CLAUDE.md, docs/progress.md, docs/roadmap-v2.md, E:/AndroidDeepDiveExplorer-Prompts/00-MASTER-PROMPT.md, STYLE-REFERENCE.md và track spec liên quan. Khi có khác biệt, ưu tiên tài liệu đặc tả và quyết định hiện có của dự án. Tài liệu nghiên cứu phân biệt điều đã quan sát trên giao diện với metadata kiểm kê từ bundle tĩnh; không diễn đạt rằng mọi bước hoặc payload đã được kiểm chứng thủ công. Dùng kết quả như gợi ý UX, ghi rõ điều gì là quan sát, suy luận hoặc chưa xác minh. Không sửa tài liệu đặc tả hoặc roadmap chỉ để đồng bộ với ghi chú ChatGPT.

Giữ nguyên: hai chế độ Guided Deep-Dive và Live Explorer, bố cục ba vùng, ràng buộc chạy offline/file:// (không fetch, không ES module, không thư viện ngoài), các quy tắc song ngữ đã chốt (vi/en cùng cây key). Không tạo mode mới, không sao chép mã, hình, nội dung hay giao diện của trang tham khảo.

Minh hoạ và phương pháp học (áp dụng cho mọi chương):
- Hình minh hoạ và animation phải dễ hiểu với người mới: mỗi hình chỉ thể hiện một ý, có chú thích "bạn đang xem gì", đi từng bước (không chạy một mạch), dùng ẩn dụ đời thường trước rồi mới tới hình kỹ thuật, và hình phải khớp đúng với đoạn mã đang giảng.
- Áp dụng các phương pháp trong learning-methods.md vào khung chương, ví dụ: dự đoán trước khi xem sim, câu hỏi nhớ lại cuối mỗi mục, worked example rồi mới làm bài, tự giải thích "vì sao", ôn lại chương cũ ở đầu chương mới, và nếu khả thi thì thẻ ôn tập lặp lại ngắt quãng lưu trong localStorage.

Việc của phiên này: Coroutines v2 (ưu tiên số 1 trong roadmap).
1. Đọc mục lục thật của "E:\AndroidBooks\deep_dive_kotlin\kotlin\Kotlin Coroutines  Deep Dive.pdf" (các trang đầu) và sửa dàn chương Coroutines v2 trong roadmap cho khớp. Sau đó đọc kỹ từng chương sách (kèm coroutines-runtime.md) trước khi viết chương tương ứng. Dùng thêm "Kotlin Coroutines by Tutorials.pdf" để lấy ví dụ Android.
2. Thiết kế khung chương dài trước (chỉ làm một lần, dùng lại cho mọi track): vấn đề → giảng từng bước có ví dụ và output → dưới mui xe → sim → bug thường gặp (triệu chứng → nguyên nhân → sửa) → bài tập có lời giải → tự kiểm. Viết bằng generator trong dev/gen.
3. Viết lần lượt từng chương, bắt đầu từ Phần 1 (Vì sao cần coroutine; Sequence builder; Suspension hoạt động thế nào; Coroutine dưới mui xe: CPS và state machine). Hết mỗi chương: chạy kiểm tra (dev/report.html, dev/tools/track-check.js), cập nhật docs/progress.md, git commit.
4. Làm liên tục cho tới gần hết limit. Trước khi hết, commit và ghi vào progress.md đang dừng ở đâu.

Thứ tự sau Coroutines: Compose Runtime/Animation v2 → UX/UI v2 → các track mới (Kotlin, Clean Android Architecture, Saving Data, Mobile System Design, Clean Code, Functional Programming), như trong roadmap. Với mỗi track mới, đọc mục lục sách thật trước và làm theo E:\AndroidDeepDiveExplorer-Prompts\P-NEW-TRACK.md.
```
