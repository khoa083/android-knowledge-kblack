# Nghiên cứu track J (Mã sạch và kỷ luật làm nghề)

> Track đã duyệt 2026-11-24, đang viết. Dàn ý: `docs/tracks/J-clean-code.md`. Nguồn chính thức thắng khi mâu thuẫn.
> Mọi quy tắc trong track là heuristic của tác giả: ghi tên tác giả, nói vấn đề nó giải quyết và khi nào không nên áp dụng.
> Ví dụ Java/C# của sách được viết lại bằng Kotlin trên app Hẹn Khám; không chép mã hay câu chữ của sách.

## Đã đọc để soạn dàn ý (2026-11-24, chỉ mục lục)
- **Đọc mục lục epub bằng `tools/epub_toc.py`:**
  - Seemann, *Code That Fits in Your Head*: phần I–II và phụ lục A, 28 thực hành;
  - Martin, *Clean Craftsmanship*: ch.1–14;
  - Martin, *Clean Architecture*: ch.1–34;
  - Martin, *The Clean Coder*: ch.1–14;
  - Martin, *Clean Agile*: ch.1–5;
  - Mancuso, *The Software Craftsman*: ch.1–16.
- **Đọc trong catalog (bookmark PDF):**
  - Moskała, *Effective Kotlin*: Item 1–60;
  - Kodeco, *Android Test-Driven Development*: ch.1–18.
- **Cập nhật 2026-11-24 (người dùng bổ sung):**
  - Martin, *Clean Code* (2008), bản PDF trong `deep_dive_kotlin/ggplaybook/`. Đã đọc mục lục ch.1–17 bằng pdftotext. Ánh xạ chương ghi trong `docs/tracks/J-clean-code.md`.
  - Bản dịch tiếng Việt của cộng đồng, chỉ để đối chiếu thuật ngữ, không chép lên site: https://github.com/quoctinnguyen8/Clean-Code---Tieng-Viet và https://cleancode.tinnq.com/ (cả hai trả HTTP 200 ngày 2026-11-24).
- **URL kiểm HTTP 200 ngày 2026-11-24:** kotlinlang.org/docs/coding-conventions.html, developer.android.com/kotlin/style-guide, developer.android.com/training/testing/fundamentals, git-scm.com/docs/git-bisect.

## Sách (bản trong thư viện cá nhân; trên site chỉ ghi trang của nhà xuất bản hoặc tác giả)
| Id nguồn | Sách | Đã đọc thân chương |
|---|---|---|
| `book-seemann` (khai báo ở `tracks/sysdesign/sources.js`, tracks gồm cả cleancode) | Mark Seemann, *Code That Fits in Your Head* | 3.2.1, 5.2.3–5.2.4, 5.3, 5.3.1, 7.1.1–7.1.3, 7.2.1, 7.2.5, 7.2.7, 8.1.3–8.1.7, phụ lục A.2, A.7, A.8 (2026-11-24) |
| `book-cleancode` | Robert C. Martin, *Clean Code* (2008) | ch.2 (mục lục và Pick One Word per Concept); ch.3: Small!, Blocks and Indenting, Do One Thing, One Level of Abstraction, Stepdown Rule, Flag Arguments, Have No Side Effects, Output Arguments, Command Query Separation; ch.4 phần mở đầu (2026-11-24) |
| `book-effective-kotlin` (khai báo ở `tracks/kotlin/sources.js`, tracks gồm cả cleancode) | Marcin Moskała, *Effective Kotlin* | Item 15, Item 17 (2026-11-24) |
| `kt-conventions` | Kotlin coding conventions (kotlinlang.org) | Choose good names, Function names (curl 2026-11-24) |
| `kt-inline-classes` | Inline value classes (kotlinlang.org) | Members (init, require), Inline classes vs type aliases (curl 2026-11-24) |

URL kiểm HTTP 200 bằng curl ngày 2026-11-24: informit.com (Clean Code, ISBN 9780132350884), blog.ploeh.dk/code-that-fits-in-your-head/.

## Bảng nguồn theo chương
### J1 Mã phải vừa trong đầu
| Ý trên site | Nguồn |
|---|---|
| Trí nhớ ngắn hạn giữ khoảng 4–7 mẩu; 7 là con số tượng trưng, con số chính xác không quan trọng; đọc mã là chạy giả lập trong đầu | Seemann 3.2.1 (kèm chú thích 2) |
| Mã mục dần; đặt ngưỡng cho một chỉ số; vượt ngưỡng đôi khi là đúng nhưng phải đưa về lại; luật hậu quả ngoài ý muốn; khi thói quen đã đổi, luật thành thừa | Seemann 7.1, 7.1.1 |
| Cyclomatic complexity: bắt đầu 1, mỗi lệnh rẽ nhánh/lặp cộng 1, từ khóa tùy ngôn ngữ (ví dụ C# đếm cả `??`); = số test tối thiểu | Seemann 7.1.2, A.8 |
| Luật 80/24 (tùy ý, khung VT100; tác giả thấy khó chịu khi hàm C# gần 20 dòng) | Seemann 7.1.3, A.2 |
| Không quá bảy thứ trong một đoạn mã; kiến trúc fractal | Seemann 7.2.1, 7.2.6 |
| Đếm biến: cục bộ, tham số, field; gom tham số thành object | Seemann 7.2.7, A.7 |
| Hàm nhỏ, hiếm khi tới 20 dòng (không có nghiên cứu chứng minh); làm một việc; một mức trừu tượng; stepdown rule | Martin, Clean Code ch.3 |
| **Của site:** quy ước đếm cho Kotlin (if, for, while, do-while, mỗi nhánh when trừ else; ?:, &&, \|\| không dùng trong ví dụ vì công cụ đếm khác nhau); hàm 19 dòng và mọi con số; nhận xét "tách quá vụn cũng có giá", "when nhiều nhánh ngang hàng vẫn dễ đọc"; chú ý nghiên cứu trí nhớ không đo việc đọc mã | — |

### J2 Đặt tên, command và query
| Ý trên site | Nguồn |
|---|---|
| Viết cho người đọc; tên hàm tốt hơn comment; X out names (đoán từ kiểu; hàm không trả gì thì chỉ tên nói được; API nhiều String/Int thì kiểu không giúp) | Seemann 8.1.3–8.1.5 |
| CQS (Bertrand Meyer); biến cục bộ không tính là side effect; ưu tiên query; không nhầm với CQRS | Seemann 8.1.6, A.6; Martin ch.3 |
| Thứ bậc giao tiếp: kiểu, tên, comment, test, commit message, tài liệu | Seemann 8.1.7 |
| Tên lộ ý định, tránh thông tin sai, phân biệt có nghĩa, mỗi khái niệm một từ, tên theo miền | Martin ch.2 |
| Side effect là lời nói dối (checkPassword khởi tạo session); set trả Boolean; tham số cờ | Martin ch.3 |
| Comment bù cho việc chưa diễn đạt được bằng mã | Martin ch.4 |
| Property là trạng thái không phải hành vi, khi nào dùng hàm; phép thử get/set | Moskała Item 15 |
| Gọi tham số bằng tên, kiểu riêng mạnh hơn | Moskała Item 17 |
| Lớp danh từ, hàm động từ, sort/sorted, tránh Manager/Wrapper | Kotlin coding conventions |
| **Của site:** lớp AppointmentRepo hai phiên bản, "đoán đọc hay ghi" như một phép đếm, lỗi huy hiệu 0 khi mất mạng, lỗi property gọi mạng | — |

### J3 Đóng gói, bất biến, parse một lần
| Ý trên site | Nguồn |
|---|---|
| Đóng gói là hợp đồng (Design by Contract, Meyer), không phải getter/setter; định nghĩa trừu tượng của Martin | Seemann 5.2.3, 5.4 |
| Luật Postel diễn giải cho API: nhận chừng nào còn làm việc được, không thì fail fast; email khó kiểm, chỉ gửi thư mới biết | Seemann 5.2.4, A.16 |
| Hiểu biết sau khi kiểm bị mất khi gọi repository; luôn hợp lệ; object bất biến chỉ kiểm ở constructor | Seemann 5.3, 5.3.1 |
| Parse, don't validate (Validate trả Reservation?), trích ý Alexis King về parser | Seemann 7.2.5, A.15 |
| Đừng trả null, đừng truyền null | Martin ch.7 |
| Object và cấu trúc dữ liệu đối xứng nhau; Law of Demeter (chỉ nhắc) | Martin ch.6 |
| Ranh giới với mã bên thứ ba, bọc lại (ví dụ Map) | Martin ch.8 |
| Lợi ích của object bất biến (6 điểm), sửa phần tử trong Set | Moskała Item 1 |
| Value class: một property, init + require, khác typealias, biểu diễn lúc chạy | Kotlin docs inline-classes |
| **Của site:** luật số di động Việt Nam minh họa, ba luật rải rác cố ý khác nhau, ba số điện thoại; hình dòng chảy phẳng thay cho "hộp lồng" của dàn ý (quy tắc không lồng hộp) | — |
