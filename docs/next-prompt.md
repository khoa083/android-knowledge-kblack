# Prompt để bắt đầu phiên tiếp theo (dán vào Claude Code, thư mục E:\AndroidDeepDiveExplorer)

> Viết lại ngày 2026-11-26, thay bản ngày 2026-11-25. Phiên này đang dở đợt viết lại theo văn phong giảng dạy.

```
Đọc CLAUDE.md, docs/chapter-template-v2.md (mục "Quy tắc viết"), và docs/progress.md (dòng "TIẾP THEO" gần cuối mục "Việc còn lại") trước.

Trạng thái (2026-11-26):
- 10 track stable, 138 chương. Tạm dừng, KHÔNG đụng: D UX, E UI.
- M Nền tảng Android: đã duyệt dàn ý, XÂY SAU đợt viết lại.
- Đã viết lại THẬT theo văn phong giảng dạy: Kotlin (K0–K13), arch (G0–G11), storage (H0–H9), coroutines (toàn bộ, 2026-11-26).
- Trang chủ đã làm gọn cho người mới (mục "Bắt đầu từ đâu?", lộ trình `starter` trong shared/paths.js).

Việc của phiên này: làm tiếp đợt viết lại, từng chương một, commit sau mỗi chương, KHÔNG push.
1. runtime (19 chương; bỏ 38 chỗ nhắc tên sách), rồi animation (13 chương; bỏ 16 chỗ).
2. Rà nội dung với nguồn: P1–P4 và K1–K6 trước, rồi Mã sạch và Thiết kế hệ thống.
3. Chưa quyết: làm lại hình để bớt bảng (người dùng chê nhiều bảng, hình chưa mượt). Hỏi người dùng trước khi làm.

QUAN TRỌNG: người dùng đã phản đối lượt "sửa nhẹ" (thay từ máy móc). Phải viết lại THẬT từng đoạn p/note, overview, wrapup:
- câu ngắn, mỗi đoạn một ý; giải thích thuật ngữ ngay chỗ dùng;
- một hình ảnh đời thường; một dòng "Quy tắc dễ nhớ:" / "Rule of thumb:" cho mỗi mục chính;
- không tên sách, không số chương sách; tên tác giả chỉ khi là quan điểm riêng; nguồn ở chip [[src:id]];
- không mục "honest" (chuyển vào simp.*); nhắc chương khác bằng ID + tên trong ngoặc kép.

Quy trình mỗi chương (ví dụ mẫu: dev/tools/rewrite_example.py):
1. python dev/tools/list_paras.py dev/gen/<track>_v2_<id>.py 900 (runtime/animation: xem module có dạng S = hay S_ = để chọn block2 hay block)
2. Viết script dùng RW (dev/tools/rewrite_helper.py): block2(sec, n, 'p'|'note', vi, en) cho module coroutines; block(...) cho module dạng S_; call("m('wrapup'", vi, en, nth=None). Viết script bằng công cụ Write (heredoc làm hỏng tiếng Việt và dấu \).
3. Chạy script, rồi python dev/gen/<track>_content.py
4. python dev/tools/text-lint.py <track> <id>  (dương tính giả đã biết: book-aat, booking/bookmark, "Mục 0", "Rule 1", "built in and")
5. Report: node dev/tools/cdp.js "file:///E:/AndroidDeepDiveExplorer/dev/report.html" --wait 6000 --eval "document.querySelector('.summary').textContent"  → phải 0 lỗi (mốc 119 cảnh báo)
6. git add đúng file; commit "<Track> <ID>: teaching-voice pass".

Quy tắc đã chốt:
- Khi được bảo "làm tiếp" thì làm liền các chương, không dừng hỏi. Không cần quan tâm hạn mức.
- Không đặt hẹn giờ nếu người dùng không yêu cầu. Đang dùng Opus thì không gọi advisor.
- Chủ đề mới: liệt kê IN/OUT, chờ duyệt.
- Chạy offline file://: không ES module, fetch, CDN, webfont. Lõi không chứa id track.

Git: commit bằng khoa083, KHÔNG có dòng Co-Authored-By hay ghi công Claude/Anthropic. git add đúng file, không -A. CHỈ push origin main khi người dùng bảo push. Không force push.
```
