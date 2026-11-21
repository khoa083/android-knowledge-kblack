# Nghiên cứu Track D: UX (P5, 2026-11-21)

Mọi URL dưới đây đã mở ngày 2026-11-21, HTTP 200, xác nhận **tiêu đề và nội dung** (không chỉ status). Design Council dùng URL đích `/resources/...` (global.md §3).

## Công thức (quant-model) và ví dụ kiểm chứng
| Model | Công thức | Nguồn | Ví dụ kiểm chứng |
|---|---|---|---|
| SUS | Câu lẻ: điểm − 1; câu chẵn: 5 − điểm; tổng × 2.5 → 0–100. **Không phải phần trăm.** Trung bình 68 (500 nghiên cứu, Sauro) | measuringu.com/sus (Sauro); NN/g measuring-perceived-usability | mọi câu = 3 → 50; mọi lẻ = 5, chẵn = 1 → 100 |
| Adjusted Wald (task success) | p̃ = (x + z²/2)/(n + z²); khoảng p̃ ± z·√(p̃(1−p̃)/(n + z²)); z = 1.96 (95%) | measuringu.com/wald (p̃); Wikipedia "Binomial proportion confidence interval", mục Agresti–Coull (dạng khoảng đầy đủ) | NN/g success-rate: 20/100 → 13–29% (mô hình: 13.3%–29.0%); MeasuringU: 9/10 → p̃ ≈ 11/14 |
| Đường cong phát hiện | found(n) = 1 − (1 − L)^n; L điển hình 31% "trung bình trên nhiều dự án" | NN/g why-you-only-need-to-test-with-5-users (Nielsen, 2000) | L = 0.31, n = 5 → 84.4% (bài ghi ~85%) |
| Severity | 0 không phải vấn đề · 1 thẩm mỹ · 2 nhỏ · 3 lớn · 4 thảm họa; yếu tố: tần suất, tác động, dai dẳng (+ tác động thị trường riêng); một người chấm không đáng tin, lấy trung bình ~3 người | NN/g how-to-rate-the-severity-of-usability-problems | — |

Giả định của đường cong (ghi trên giao diện): người dùng tương đồng dùng sản phẩm theo cách tương tự; vấn đề độc lập, L đồng đều; nhiều nhóm người dùng khác biệt cần test riêng; nghiên cứu định lượng cần nhiều người hơn (≥ 20, NN/g how-many-test-users).

## Khẳng định theo chương (nhãn)
- D0: UX bao trùm mọi tương tác với công ty, dịch vụ, sản phẩm; UI là một phần; usability là thuộc tính chất lượng của UI (definition-user-experience, `research`). 5 thành phần usability: learnability, efficiency, memorability, errors, satisfaction (usability-101). Double Diamond: Discover, Define, Develop, Deliver; quy trình là "lời mời" chứ không phải sổ tay, tổ chức thường quay lại đầu (Design Council, `author-framework`).
- D1: recognition dễ hơn recall vì có nhiều gợi ý truy xuất (recognition-and-recall). Trí nhớ ngắn hạn ~7 chunk, phai trong ~20 s; giới hạn menu 7 mục là hiểu lầm (short-term-memory-and-web-usability, `research`).
- D2: bảy giai đoạn hành động, vực thực thi/đánh giá: Norman, *DOET* (sách, chỉ dẫn chiếu, `author-framework`); heuristic #1 Visibility of System Status (ten-usability-heuristics).
- D3: slip = hành động không chủ ý, thường lúc tự động; mistake = mục tiêu sai do mô hình tư duy sai. Phòng slip: constraint, gợi ý, mặc định tốt, định dạng dễ dãi; phòng mistake: quy ước, signifier, xem trước kết quả; chung: giảm gánh nhớ, xác nhận trước thao tác phá hủy (quá nhiều → bấm qua), undo, cảnh báo trước (slips, user-mistakes). Thông báo lỗi: gần nguồn, không chỉ màu, ngôn ngữ dễ hiểu, chính xác, gợi ý cách sửa, không đổ lỗi, giữ dữ liệu đã nhập (error-message-guidelines).
- D4: 10 heuristic là "quy tắc kinh nghiệm rộng", không phải hướng dẫn cụ thể; 3–5 người đánh giá độc lập rồi gộp; không thay nghiên cứu người dùng (ten-usability-heuristics, how-to-conduct-a-heuristic-evaluation).
- D5: deceptive pattern (Brignull đặt tên 2010): obstruction, mẹo hình ảnh/chữ, nagging, confirmshaming, sneaking/preselection (deceptive-patterns) — chỉ dạy nhận diện. Hick: thời gian quyết định tăng theo số và độ phức tạp lựa chọn (lawsofux.com — **thứ cấp**, không có công thức log trên trang; nghiên cứu Hick & Hyman 1952); NN/g simplicity-vs-choice ủng hộ ít lựa chọn nhưng không nêu Hick; progressive disclosure: hơn 2 tầng thường kém. → trình bày định tính, `research`, có giới hạn. CREATE (Wendel): sách, `author-framework`.
- D6: ba trục thái độ↔hành vi, định tính↔định lượng, bối cảnh dùng (natural/scripted/limited/none) (which-ux-research-methods).
- D7: "test 5 người" cho nghiên cứu **định tính**; định lượng ≥ 20; nhiều nhóm → ~5 (hoặc 3–4) mỗi nhóm; nên chia ngân sách thành nhiều vòng nhỏ (how-many-test-users, why-you-only-need…).
- D8: báo cáo mỗi tỉ lệ kèm khoảng tin cậy; partial success là thứ bậc, không lấy trung bình nhãn số (success-rate). SUS cần ~20–30+ người cho so sánh định lượng (measuring-perceived-usability).
- D9: 4 chiều tone: formal↔casual, serious↔funny, respectful↔irreverent, matter-of-fact↔enthusiastic (tone-of-voice-dimensions). Per-app language: Android 13 (API 33), `LocaleManager.setApplicationLocales`; AndroidX `AppCompatDelegate.setApplicationLocales` (AppCompat ≥ 1.6.0) cho bản cũ (app-languages, `ds-guideline`/stable).
- D10: GV sprint 5 ngày: Thứ Hai map & mục tiêu, Thứ Ba sketch, Thứ Tư quyết định + storyboard, Thứ Năm prototype, Thứ Sáu test với khách hàng (gv.com/sprint). Biến thể Banfield et al. (sách *Design Sprint*): Understand/Diverge/Converge/Prototype/Test — chỉ dẫn chiếu sách, `author-framework`.

## Điểm chưa xác minh / xử lý
- Các trang NN/g còn lại trong spec (ux-writing-study-guide, journey-mapping-101, persona…): đã có HTTP 200 ở P0, chưa đọc nội dung lần này → chỉ dùng làm "đọc thêm", không làm nguồn cho khẳng định cụ thể.
- m3.material.io (content design): chưa đọc nội dung (P6) → chưa dùng làm nguồn ở D9.
- Sách (DOET, Wendel, Podmajersky, Greever, Banfield): không đọc epub trong lần chạy này; chỉ nêu tên framework + tác giả ở mức đã biết công khai, gắn `author-framework`, không trích nội dung. Ghi là điểm cần bổ sung.
- "7±2": trang NN/g không nêu tên Miller → site không gán tên tác giả gốc cho con số.

## Checklist mục 8 (Track D) — tick 2026-11-21

| Mục | Ở đâu |
|---|---|
| UX ≠ UI ≠ usability từ D0 | D0 essence, `sec.def`, sim `ux.classify`, misconception `ux-is-ui` |
| Không đổ lỗi; slip ≠ mistake | D3 essence + `sec.err`, model `ux.errors`, misconception `user-fault` |
| Thái độ (nói) ≠ hành vi (làm) | D6 `sec.ax`, model `ux.session` (ống kính "nói"/"làm"), misconception `ask-users` |
| Không số liệu thiếu nguồn | mọi số có `[[src:]]` cạnh: 31%, 85%, 68, 20–30 người, 13–29%, 7 chunk/20 s; số minh họa (lỗi 4→1/3, CREATE) gắn nhãn minh họa |
| "Định luật" gắn nhãn + giới hạn; lawsofux thứ cấp | D1 `sec.mem` (7±2), D5 `sec.hick` (ghi rõ thứ cấp, định tính), nguồn `lawsofux-hick` ghi "NGUỒN THỨ CẤP" |
| Framework tác giả gắn `author-framework` + tên | Double Diamond (Design Council), Six Minds (Whalen), bảy giai đoạn (Norman), CREATE (Wendel), voice chart (Podmajersky), Metts & Welfle, Greever, GV, Banfield et al. |
| SUS, adjusted Wald, đường cong: công thức có nguồn, kiểm chứng, giả định; SUS không phải % | `models/quant.js` + 3 registerCheck; lab `sus.warn`, `success.formula`, `curve.assume` |
| Đo cá nhân: nhãn, không lưu, không gửi | lab D1 `recall.privacy` hiển thị trên giao diện; dữ liệu chỉ trong `ADE.uxLab.store` (bộ nhớ trang) |
| Deceptive pattern chỉ để nhận diện/tránh | model `ux.deceptive` (bước "cách làm trung thực", `co.ethics`) |
| Hẹn Khám/ClinicBook hư cấu | `shared/mock-app/` (comment đầu file), glossary/misconceptions dùng tên hư cấu |
| Hiểu lầm ≥ 10, có nguồn | 11 mục |

Ghi chú: sách (DOET, Wendel, Podmajersky, Greever, Banfield) chưa đọc epub trong lần chạy này — chỉ nêu tên framework và tác giả, không trích nội dung. Các nguồn NN/g "đọc thêm" (`pageOnly`) chưa được dùng cho khẳng định cụ thể.
