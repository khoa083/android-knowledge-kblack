# Prompt để bắt đầu phiên tiếp theo (dán vào Claude Code, thư mục E:\AndroidDeepDiveExplorer)

> Viết lại ngày 2026-11-25, thay bản ngày 2026-11-24 đã hết hiệu lực. Trong bản cũ, các track I, J, K, L còn là "chưa xây"; nay cả bốn đã xong.

```
Đọc CLAUDE.md, docs/progress.md (khối "Trạng thái hiện tại" ở đầu và mục "Việc còn lại" ở cuối) và docs/roadmap-v2.md (bảng "Trạng thái các track") trước.

Trạng thái (2026-11-25):
- 10 track stable, 138 chương: A Coroutines, B Runtime, C Animation, F Kotlin, G Kiến trúc, H Lưu dữ liệu, I Thiết kế hệ thống, J Mã sạch, K Lập trình hàm, L Gỡ lỗi và hiệu năng. Cầu nối X1–X35.
- Tạm dừng, KHÔNG đụng tới: D UX, E UI ("Sắp ra mắt"). Phần SM dở dang của UX nằm trong git stash.
- M Nền tảng Android (docs/tracks/M-android-platform.md): đã duyệt dàn ý ngày 2026-11-25, cả năm câu hỏi theo mặc định. Người dùng muốn XÂY SAU đợt viết lại.

Việc của phiên này: viết lại các chủ đề còn khó hiểu, theo thứ tự trong docs/progress.md, mục "Việc còn lại":
1. Track Kotlin: viết lại K7–K13 theo giọng dạy học, rồi K0 (K1–K6 đã xong).
2. Viết lại theo giọng dạy học: arch, storage, coroutines, runtime, animation.
   - arch: khi viết G0, thêm cầu nối X24–X27.
   - coroutines: thay chữ "chương FP" bằng tên đầy đủ của chương.
3. Rà nội dung các phần viết trước khi chuyển sang Opus: Lập trình hàm P1–P4 và Kotlin K1–K6 trước, sau đó Mã sạch và Thiết kế hệ thống. Đối chiếu từng khẳng định với nguồn.

Giọng dạy học, theo mẫu track L:
- giải thích thuật ngữ ngay lần đầu xuất hiện;
- câu ngắn;
- mỗi đoạn một ý;
- ví dụ trên app Hẹn Khám;
- không dẫn số chương sách trong bài giảng;
- nguồn đặt ở chip nguồn và mục "trung thực".
Kiểm bằng dev/tools/text-lint.py và text-terms.py.

Quy tắc đã chốt với người dùng:
- Nội dung "cần và đủ": cơ chế sâu nhưng chọn lọc. Sách trong E:\AndroidBooks là nguồn giảng chính, cùng tài liệu chính thức; khi mâu thuẫn, nguồn chính thức thắng.
- Không đi sâu vào IDE: dạy câu hỏi mà công cụ trả lời, không dạy đường dẫn menu.
- Chủ đề mới: liệt kê IN/OUT và dàn chương, rồi chờ người dùng duyệt trước khi xây.
- Kiểu hình: tự chọn kiểu dễ hình dung nhất, không cần hỏi (trừ UI/UX).
  - Mọi hình phải có chuyển động khi đổi bước (motion-check.js).
  - Không dùng hộp lồng sâu.
- Trung thực:
  - chi tiết nội bộ ghi phiên bản hoặc commit;
  - mô hình giản lược có nhãn;
  - mọi khẳng định có nguồn trong docs/research/<track>.md.
- Chuỗi vi và en phải khác nhau.
- Khi được bảo "làm tiếp" thì làm các chương liền nhau, không dừng lại để hỏi giữa chừng.
- Không đặt hẹn giờ chạy tiếp nếu người dùng không yêu cầu.
- Đang dùng Opus thì không gọi advisor.

Kỹ thuật:
- Chạy offline qua file://: không ES module, fetch, CDN, webfont, framework hay build step. Lõi (js/core, app.js) không chứa id track.
- Nội dung sinh bằng dev/gen/<track>_content.py. Mỗi chương là một module dev/gen/<track>_v2_<id>.py.
- Hình đăng ký bằng ADE.registerScreen trong tracks/<t>/views/visuals.js.
- Kiểm trước mỗi commit:
  - dev/report.html: 0 lỗi; mốc hiện tại là 120 cảnh báo;
  - track-check ở --w 1280 và --w 360;
  - motion-check;
  - routes-check;
  - ảnh chụp có --reduce.

Git:
- Commit bằng khoa083, KHÔNG thêm dòng Co-Authored-By hay ghi công Claude/Anthropic.
- git add đúng file đã sửa, không dùng -A. Commit sau mỗi phần xong.
- CHỈ push origin main khi người dùng bảo push trong tin nhắn, kể cả khi hạn mức sắp hết. Không force push.
- Repo công khai: không đưa thông tin nhạy cảm, đường dẫn cục bộ hay email lên site.

Hạn mức: dừng ở khoảng 95–98% của cửa sổ 5 giờ. Trước khi dừng: commit, rồi ghi vào docs/progress.md đang dừng ở đâu.
```
