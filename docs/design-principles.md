# Nguyên tắc thiết kế: checklist dùng ở mọi phase

> Rút gọn từ `STYLE-REFERENCE.md` mục 4.1–4.4 và master mục 5, kèm kết quả P0 (tương phản, font). Mức người dùng đã chọn: **"Gần mẫu hơn"** (Protocol Explorer), chốt ngày 2026-11-20.
> Giá trị màu đầy đủ và số đo ở `docs/research/global.md` mục 5.

## 1. Giữ gần mẫu (được dùng)

- [ ] Bố cục ba vùng: canvas trái có tab "Sơ đồ / Timeline"; panel ngữ cảnh phải (Tổng quan → Bước n/N → Tổng kết, thêm tab "Giải thích / Mã"); bảng nhật ký sự kiện full-width dưới, điều khiển và chú giải nằm trên header bảng; thanh công cụ trên cùng có tìm kiếm và chip ngữ cảnh.
- [ ] Giao diện monospace hệ thống; header panel và nhãn ngắn (≤ 40 ký tự) VIẾT HOA, giãn chữ 0.08–0.12em, đậm 700, `line-height ≥ 1.3`.
- [ ] Light "bản vẽ kỹ thuật" là mặc định khi OS không yêu cầu dark; dark ngang hàng; lần đầu mở theo `prefers-color-scheme`.
- [ ] Line-art isometric đơn sắc, tô nhạt cùng tông, nền lưới isometric mờ.
- [ ] Zoom vào node đang xử lý; gõ chữ cho chuỗi/mã ngắn; token chạy dọc cạnh; mũi tên timeline vẽ dần.
- [ ] Bảng sự kiện kiểu bắt gói tin (cột theo `logKinds`); bấm dòng để nhảy bước.
- [ ] Drawer catalog có chip domain kèm số đếm, accordion track → chương → bước.
- [ ] Thanh điều khiển dính đáy trên mobile (< 768px) với `env(safe-area-inset-bottom)`, không che nội dung cuối trang.

## 2. Bắt buộc khác (không được giống)

- [ ] **Mọi hình và icon tự vẽ**, chủ thể là Android (điện thoại, chip runtime, các lớp UI, hàng đợi, đồng hồ frame, cây Job, khung "Hẹn Khám"). Không vẽ lại laptop, router, server, đám mây hay hình nào của mẫu; không trace SVG.
- [ ] **Màu mực xanh-lục "Android ink"**, không navy. Không dùng bất kỳ mã màu nào của hai trang mẫu.
- [ ] **Không webfont** (kể cả font của mẫu). Chỉ system monospace; đoạn giải thích dài ≥ 3 câu ở Guided được dùng system sans, có tùy chọn bật/tắt.
- [ ] **Logo riêng:** điện thoại isometric có mũi tên đi xuống xuyên các lớp ("đào sâu"). Không lập phương, không khung ngoặc góc. Wordmark "ANDROID DEEP DIVE"; tagline "Hiểu Android từ bên trong" / "Understand Android from the inside".
- [ ] **Không có khối credit** hay link mạng xã hội của tác giả trang mẫu. Hai trang mẫu chỉ ở trang Nguồn, vai trò "cảm hứng UX".
- [ ] **Không sao chép** mã, CSS, SVG, icon, font, bảng màu, câu chữ, ví dụ bài học (PhotoShare, IP mẫu, chuỗi bài system design), tên gọi hay tagline của hai trang.
- [ ] Tên riêng của site: vùng ("Nhật ký sự kiện / Event log", "Tổng quan chương / Chapter overview", "Bước hiện tại / Current step", "Tổng kết / Wrap-up", "Mục tiêu / Goals", "Tình huống / Scenario"); loại bước (Tình huống, Cơ chế, Thử nghiệm, Bẫy, Ở Android, Tổng kết); callout (Cơ chế ⚙, Bẫy ⚠, Ở Android, Nguồn nói gì 📎, Thử ngay ▶ — icon tự vẽ).
- [ ] Công tắc ngôn ngữ dạng phân đoạn `VI │ EN`; panel viền mảnh, bo 4px.
- [ ] Bảng sự kiện trên mobile là **danh sách thẻ**, không phải bảng nhiều cột cuộn ngang.

## 3. Màu và tương phản

- [ ] Light và dark là hai bảng màu riêng (không đảo màu). Giá trị theo `global.md` mục 5.1.
- [ ] Ngưỡng: chữ ≥ 4.5:1 (WCAG 1.4.3), non-text ≥ 3:1 (1.4.11). Biên nội bộ: ≥ 4.55 chữ, ≥ 3.10 non-text.
- [ ] Chữ luôn là `--ink`, `--ink-2` hoặc `--ink-3` trên `paper/paper-2/paper-3`. Token ngữ nghĩa dùng làm chữ chỉ trên `paper`, `paper-2`, `paper-3`; **không** làm chữ trên tint của chính nó ở light.
- [ ] **Chip, chú giải log: chữ `--ink`; token chỉ ở icon, viền trái, nét.**
- [ ] `--line` chỉ trang trí. Viền control và nét sơ đồ có nghĩa dùng `--line-strong`.
- [ ] Dòng đang chọn: nền `--row-active` + vạch trái 3px `--brand` + dấu ▶.
- [ ] Một token một vai trò; track mới ánh xạ vào vai trò có sẵn, không thêm hue.
- [ ] Accent track **non-text only**; chữ trên thẻ track là `--ink`; accent **không bao giờ** nằm trong canvas, bảng log hay chú giải loại sự kiện.
- [ ] Không truyền tin chỉ bằng màu: luôn kèm icon, nhãn hoặc kiểu nét (current value nét đặc, velocity nét đứt). Đạt/không đạt: ✓/✗ + chữ.
- [ ] Mock UI: có viền `--line-strong` và nhãn "Giao diện mẫu / Sample UI"; token ngữ nghĩa không áp dụng bên trong khung.

## 4. Typography song ngữ

- [ ] `text-transform: uppercase` chỉ cho header panel, nhãn, tiêu đề bước/chương ngắn (≤ 40 ký tự). Đoạn giải thích luôn sentence case.
- [ ] Line-height chữ thân ≥ 1.5 (thân monospace 15px/1.6; nhãn 12–13px).
- [ ] Độ dài dòng giải thích tối đa ~70 ký tự.
- [ ] Không đặt chiều rộng cố định cho nút, nhãn, thẻ (vi dài hơn en); kiểm ở 360px.
- [ ] **Mọi chuỗi lưu NFC** (report kiểm `s === s.normalize('NFC')`).

### Kết quả kiểm font tiếng Việt (cập nhật qua các phase)

| Kiểm tra | Trạng thái | Ngày |
|---|---|---|
| Consolas phủ đủ glyph dựng sẵn chữ cái tiếng Việt (hoa, thường) | Đạt | 2026-11-20 |
| Courier New phủ đủ glyph dựng sẵn | Đạt | 2026-11-20 |
| Cascadia Mono / Cascadia Code | **Chưa kiểm** (không cài trên máy P0) | — |
| Roboto Mono / Noto Sans Mono (Android) | **Chưa kiểm** (không có thiết bị) | — |
| Chuỗi mẫu "TIẾNG VIỆT · ỨNG DỤNG · ĐỒNG THỜI · HỦY BỎ · CẬP NHẬT · NHẬT KÝ SỰ KIỆN" khi uppercase (`.caps`, line-height 1.45), light và dark, trong Chrome trên Windows 11 (`dev/report.html` mục 6) | **Đạt bằng mắt**: dấu mũ, dấu hỏi, dấu nặng không bị cắt hay lệch ở 14px và 22px. Chưa ghi được font cụ thể mà Chrome đã chọn trong stack | 2026-11-20 (P1) |

Nếu font đầu stack không đủ dấu, đưa font đủ dấu lên trước.

## 5. Chuyển động và truy cập

- [ ] Chuyển động chỉ để giải thích thứ tự, quan hệ, dữ liệu; không trang trí.
- [ ] `prefers-reduced-motion` + nút tắt thủ công (class `.reduced-motion`): zoom camera và gõ chữ **tắt hẳn**; animation dừng hoặc chuyển tức thời; Play chạy từng bước. Có nút "Chỉ sơ đồ / không zoom".
- [ ] Tab/Shift+Tab qua mọi điều khiển; Enter/Space kích hoạt; focus ring rõ (cam đậm/vàng, 2px + offset 2px, ≥ 3:1).
- [ ] Phím tắt mô phỏng (`←` `→` `Space` `R`, `1–9`, `[ ]`, `?`, `Ctrl+K` hoặc `/`) **bỏ qua** khi focus ở `button`, `input`, `select`, `textarea` hoặc slider; ghi chú trên giao diện bằng cả hai ngôn ngữ.
- [ ] Vùng chạm ≥ 44×44 CSS px. Không cuộn ngang ở 360px.
- [ ] `<html lang>` cập nhật khi đổi ngôn ngữ; thuật ngữ tiếng Anh trong bản vi bọc `lang="en"`; mã có `translate="no"`; `aria-live="polite"` cho bước hiện tại; SVG có `role="img"`, `<title>`, `<desc>`.

## 6. Hạn chế kỹ thuật (nhắc lại)

- [ ] Chạy offline khi bấm đúp `index.html` (`file://`): không ES module, không `fetch()`, không CDN, không framework, không build step; dữ liệu là `.js` cổ điển gắn vào `window.ADE`.
- [ ] `js/core` và `app.js` không chứa id track nào.
- [ ] `localStorage` có tiền tố `ade.` và bọc try/catch.
- [ ] Chỉ ghi file trong `E:\AndroidDeepDiveExplorer`.

## 7. Tự kiểm trước khi kết thúc mỗi phase (hỏi nhanh)

1. Có hình/icon/chuỗi nào có thể bị nhầm là của mẫu không?
2. Có màu nào là navy hay mã màu của mẫu không?
3. Có thông tin chỉ truyền bằng màu không?
4. Có chuỗi hiển thị nào thiếu bản vi hoặc en không?
5. Có `fetch`, `import`, CDN, webfont lọt vào không?
6. Zoom và gõ chữ đã tắt khi reduced-motion chưa?
