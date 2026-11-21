# Android Deep Dive Explorer: hướng dẫn cho phiên triển khai

Thư mục này là **thư mục đích** của một website học tập tương tác, **song ngữ Việt–Anh**, chạy offline. Site gồm 5 track ban đầu:
- **Engineering:** Kotlin Coroutines, Compose Runtime, Compose Animation.
- **Design:** UX, UI.

Site được thiết kế để **thêm chủ đề mới** mà không phải sửa phần lõi.

## Đặc tả nằm ở đâu

Thư mục `E:\AndroidDeepDiveExplorer-Prompts\` chứa toàn bộ đặc tả. Chỉ **đọc**, không sửa.

| File | Vai trò |
|---|---|
| `00-MASTER-PROMPT.md` | Hợp đồng chung, là nguồn sự thật cao nhất |
| `STYLE-REFERENCE.md` | Phân tích hai trang mẫu, pattern được học theo, **bảng khác biệt bắt buộc** (tránh bản quyền), design tokens |
| `I18N-STYLE-GUIDE.md` | Quy ước song ngữ, bảng thuật ngữ |
| `tracks/A…E-*.md` | Spec chi tiết từng track |
| `CONSTRAINTS-CHECKLIST.md` | Checklist nghiệm thu, phải đạt toàn bộ |
| `SOURCES.md`, `REFERENCE-BOOKS.md` | Nguồn đã kiểm tra; ánh xạ sách (nguồn phụ, không chép) |
| `phases/P0…P8`, `P-TRACK-quy-trinh-chung.md`, `P-NEW-TRACK.md` | Trình tự thực thi |
| `TRACK-TEMPLATE.md` | Cách thêm track mới hoặc ngôn ngữ mới |
| `tools/epub_toc.py` | Đọc mục lục sách epub |

## Cách làm việc

1. Đọc master, `STYLE-REFERENCE` và `I18N-STYLE-GUIDE` trước khi viết bất kỳ file nào.
2. Làm tuần tự P0 → P8. Hết mỗi phase:
   - tự kiểm tra;
   - cập nhật `docs/progress.md`;
   - báo ngắn cho người dùng.
3. Nếu phiên bị ngắt: đọc `docs/progress.md` và làm tiếp, không làm lại từ đầu.

## Ràng buộc không được quên

- **Chạy offline khi bấm đúp `index.html` (`file://`).**
  - Không ES module, không `fetch()`, không CDN, không webfont, không framework, không build step.
  - Dữ liệu là file `.js` cổ điển gắn vào `window.ADE`.
  - Kiểm thử bằng `file://`, không dùng dev server.
- **Song ngữ:**
  - Mọi chuỗi hiển thị có bản vi và en, cùng cây key, cùng khẳng định, cùng nguồn.
  - Model chỉ phát message key.
  - Đổi ngôn ngữ giữ nguyên route và trạng thái mô phỏng.
- **Registry:** `js/core` và `app.js` không chứa id track nào. Mọi track tự đăng ký qua `manifest.js`.
- **Phong cách: "Gần mẫu hơn" so với Protocol Explorer** (người dùng đã chọn). Chi tiết ở `STYLE-REFERENCE.md` mục 4.1.
  - **Giữ gần mẫu:**
    - bố cục ba vùng;
    - giao diện monospace hệ thống, header viết hoa (đã kiểm tra dấu tiếng Việt);
    - light "bản vẽ kỹ thuật" và dark;
    - line-art isometric;
    - zoom vào node đang xử lý;
    - bảng sự kiện kiểu bắt gói tin.
  - **Bắt buộc khác:**
    - mọi hình và icon **tự vẽ** với chủ thể Android, không vẽ lại hay trace hình của mẫu;
    - màu mực xanh-lục, không dùng navy;
    - không webfont;
    - logo riêng, không có credit;
    - tên vùng, loại bước, callout, câu chữ và ví dụ đều của riêng site.
  - Không sao chép mã, CSS, SVG hay asset của hai trang mẫu.
- **Trung thực:**
  - Site là mô hình giảng dạy, phải gắn nhãn giản lược.
  - Chi tiết nội bộ phải có phiên bản hoặc commit.
  - Design: không bịa số liệu; "định luật" là heuristic có giới hạn; framework của tác giả phải ghi tên tác giả; công thức có ví dụ kiểm chứng; dữ liệu đo trong sandbox không gửi đi đâu.
- **Nguồn:** nguồn chính thức hoặc chuẩn luôn thắng. Sách chỉ là nguồn phụ: không chép, không ghi đường dẫn file cục bộ lên site.
- Chỉ ghi file trong thư mục này.
