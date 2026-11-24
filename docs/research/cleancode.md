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
| `book-seemann` (khai báo ở `tracks/sysdesign/sources.js`, tracks gồm cả cleancode) | Mark Seemann, *Code That Fits in Your Head* | 3.2.1, 5.2.3–5.2.4, 5.3, 5.3.1, 7.1.1–7.1.3, 7.2.1, 7.2.5, 7.2.7, 8.1.3–8.1.7, 5.2.2, 6.2.2, 6.2.5, 11.2, phụ lục A.2, A.7, A.8, A.10, A.17 (2026-11-24) |
| `book-cleancode` | Robert C. Martin, *Clean Code* (2008) | ch.2 (mục lục và Pick One Word per Concept); ch.3: Small!, Blocks and Indenting, Do One Thing, One Level of Abstraction, Stepdown Rule, Flag Arguments, Have No Side Effects, Output Arguments, Command Query Separation; ch.4 phần mở đầu; ch.6 Data/Object Anti-Symmetry, Law of Demeter (đầu mục); ch.7 Don't Return Null, Don't Pass Null; ch.8 Using Third-Party Code; ch.9 The Three Laws of TDD, F.I.R.S.T. (2026-11-24) |
| `book-craft` | Robert C. Martin, *Clean Craftsmanship* (2021) | ch.2: The Three Laws of TDD, The Fourth Law; ch.3: Test Doubles, Mock, The TDD Uncertainty Principle, London versus Chicago; ch.4: The Fragile Test Problem, The One-to-One Correspondence, Breaking the Correspondence (2026-11-24); URL informit.com kiểm HTTP 200 |
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

### J4 TDD
| Ý trên site | Nguồn |
|---|---|
| Bản chất của TDD; ba luật (tác giả gọi là tùy ý; TCR của Kent Beck đạt cùng mục tiêu); luật thứ tư refactor; "make it work, then make it right" (Kent Beck); refactor liên tục, không lên lịch | Martin, Clean Craftsmanship ch.2 |
| Ba luật TDD (phát biểu ngắn); F.I.R.S.T. | Martin, Clean Code ch.9 |
| Red Green Refactor như checklist và như phương pháp khoa học | Seemann 5.2.2, A.17 |
| Devil's Advocate; trích Martin "test càng cụ thể, mã càng tổng quát"; đủ test chưa là đánh giá rủi ro; lỗi đã ra thật thì viết test tái hiện | Seemann 6.2.2, 6.2.5, A.10 |
| Đừng tin test chưa từng thấy đỏ; tạm phá mã để thấy test đỏ | Seemann 11.2 |
| Tên test có khoảng trắng chỉ cho test; Android runtime từ API 30 | Kotlin coding conventions |
| **Của site:** mức phí, ngày lễ 2/9, các ngày ví dụ (đã kiểm thứ trong lịch 2026), năm phiên bản hàm phí được cài thật trong model; không nêu số liệu nghiên cứu về hiệu quả TDD (chưa đọc nghiên cứu nào) | — |

### J5 Thiết kế test
| Ý trên site | Nguồn |
|---|---|
| Test dễ vỡ là vấn đề thiết kế; tương ứng một-một; Rule 12; hành vi quan trọng phải thấy qua giao diện | Martin, Clean Craftsmanship ch.4 |
| Năm loại test double (Meszaros); mock là spy biết kỳ vọng; spy/mock buộc test vào thuật toán; tác giả không thích công cụ mock | Martin, Clean Craftsmanship ch.3 |
| London (chắc chắn, outside-in, mock ở mọi ranh giới) và Chicago (linh hoạt, test giá trị và thuộc tính); tác giả nghiêng Chicago | Martin, Clean Craftsmanship ch.3 |
| Không có định nghĩa chung cho mock, stub | Seemann, chú thích ở ch.4 |
| Arrange Act Assert, dòng trống, Arrange quá lớn là mùi | Seemann 4.2.2, A.3 |
| Sửa test là sửa lưới an toàn; refactor an toàn của IDE; tách refactor test và mã | Seemann 11.1, 11.1.3 |
| **Của site:** BookingService và bốn cộng tác viên, 13 và 8 cạnh, hai refactor, lỗi phí cuối tuần; gợi ý "fake cho thứ ngoài tiến trình, code thật cho tính toán thuần" là diễn giải; cú pháp MockK minh họa | — |
