# Prompt để bắt đầu phiên tiếp theo (dán vào Claude Code, thư mục E:\AndroidDeepDiveExplorer)

> Viết lại ngày 2026-11-24. Bản cũ (giao việc Coroutines v2) đã hết hiệu lực: Coroutines, Runtime, Animation v2 và track Kotlin đều đã xong.

```
Đọc CLAUDE.md, docs/progress.md (mục cuối) và docs/roadmap-v2.md (bảng "Trạng thái các track") trước.

Trạng thái:
- Đã xong và stable: A Coroutines, B Runtime, C Animation (v2), F Kotlin (14 chương), G Kiến trúc (12 chương), H Lưu dữ liệu (10 chương).
- Tạm dừng, KHÔNG đụng tới: D UX, E UI ("Sắp ra mắt"). Phần SM dở dang của UX nằm trong git stash.
- Đã xong và stable: G Kiến trúc app Android (track `arch`, 12 chương G0–G11, 2026-11-24).
- Đã xong và stable: H Lưu dữ liệu (track `storage`, 10 chương H0–H9, 2026-11-24). Hình mới có thể dùng lại: cây quyết định bậc thang (.vz-dt), sơ đồ tuần tự SVG (.vz-sq, trong tracks/storage/views/visuals.js), dãy ô phiên bản (.vz-mig), hai bảng cạnh nhau (.vz-pair), cây thư mục trong bảng (.vz-tree-p).
- Đã duyệt dàn ý (2026-11-24), CHƯA xây, làm theo thứ tự: I docs/tracks/I-mobile-system-design.md → J docs/tracks/J-clean-code.md → K docs/tracks/K-functional-kotlin.md.
- Sau K: L Gỡ lỗi và hiệu năng Android docs/tracks/L-debugging-performance.md (đã duyệt 2026-11-24).

Quy tắc đã chốt với người dùng:
- Nội dung "cần và đủ": cơ chế sâu nhưng chọn lọc, không chép sách, không bám từng chương. Sách trong E:\AndroidBooks là nguồn giảng chính, cùng tài liệu chính thức; nguồn chính thức thắng khi mâu thuẫn.
- Chủ đề mới: liệt kê IN/OUT và dàn chương, rồi chờ người dùng duyệt bằng tay trước khi xây.
- Kiểu hình: tự chọn kiểu dễ hình dung nhất cho từng chương và từng phần (bảng, ma trận, cây, hộp lồng, dãy ô, làn thời gian, đồ thị phụ thuộc, sơ đồ tuần tự…), không cần hỏi. Trừ UI/UX. Xem docs/chapter-template-v2.md, mục "Chọn kiểu hình theo nội dung". Sơ đồ node của sim giữ làm tab phụ. Hình viết cẩn thận cho đúng nội dung, không cố dùng lại hàm có sẵn khi nó không hợp.
- Trung thực: chi tiết nội bộ có phiên bản hoặc commit; mô hình giản lược có nhãn; không bịa khẳng định; heuristic ghi tên tác giả; mọi khẳng định có nguồn trong docs/research/<track>.md.
- Chuỗi vi và en phải khác nhau (report cảnh báo "Nghi chưa dịch" nếu trùng).

Kỹ thuật:
- Chạy offline qua file://: không ES module, fetch, CDN, webfont, framework hay build step. Lõi (js/core, app.js) không chứa id track.
- Nội dung sinh bằng dev/gen/<track>_content.py, module từng chương dev/gen/<track>_v2_<id>.py. Hình trực quan đăng ký bằng ADE.registerScreen(modelId, fn, {labelKey, icon}) trong tracks/<t>/views/visuals.js, CSS .vz-*.
- Kiểm trước mỗi commit:
  - dev/report.html phải 0 lỗi; mốc hiện tại là 120 cảnh báo;
  - track-check cho từng track đang mở, ở --w 1280 và --w 360 (Coroutines có 4 lỗi cũ đã biết);
  - routes-check;
  - xem ảnh chụp của hình mới.

Git:
- Commit bằng khoa083, KHÔNG thêm dòng Co-Authored-By hay ghi công Claude/Anthropic.
- git add đúng file đã sửa (không -A).
- Commit sau mỗi phần xong; chỉ push origin main khi hạn mức 5 giờ sắp chạm giới hạn (ngay trước khi dừng). Không force push.
- Repo công khai: không đưa thông tin nhạy cảm, đường dẫn cục bộ hay email lên site.

Hạn mức: kiểm usage định kỳ, dừng ở khoảng 90–98% của cửa sổ 5 giờ. Trước khi dừng: commit, push, ghi vào docs/progress.md đang dừng ở đâu.

Việc tiếp theo: bắt đầu track I Thiết kế hệ thống phía mobile (`sysdesign`) theo docs/tracks/I-mobile-system-design.md (đã duyệt): dựng khung track theo mẫu track storage (dev/gen/storage_content.py, tracks/storage/), rồi viết i1 → i13, i0 cuối. Hình mỗi chương theo cột "Hình chính" của spec; sơ đồ tuần tự đã có ở track storage (H7) thì viết lại gọn trong track I hoặc chuyển thành hàm dùng chung nếu hợp lý (không đưa id track vào js/core). Trước khi viết mỗi chương: đọc trang chính thức liên quan (qua agent web-fetch) và ghi bảng nguồn vào docs/research/sysdesign.md.
```
