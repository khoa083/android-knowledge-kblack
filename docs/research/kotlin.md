# Nghiên cứu track F (Kotlin)

Spec: `docs/tracks/F-kotlin.md`. Trang kotlinlang.org đọc nội dung ngày 2026-11-23 (trang không ghi phiên bản Kotlin ở đầu; khi trang đổi, đọc lại). Sách: Kotlin Essentials, Effective Kotlin, Kotlin Exercises (Moskała, bản PDF có trong thư viện của người dùng; chỉ đọc chương liên quan, diễn đạt lại). Máy không có `kotlinc`/`javap`: không có khẳng định bytecode nào tự kiểm.

## K1 · val, kiểu, hàm và biểu thức (2026-11-23)

| Khẳng định | Nguồn | Loại |
|---|---|---|
| val gán một lần, var gán lại được; khai báo trước gán sau phải ghi kiểu | `kt-basic-syntax` | stable |
| val không có nghĩa là bất biến (MutableList qua val vẫn sửa được) | `book-effective-kotlin` Item 1 | guideline |
| Chia hai số nguyên trả số nguyên, bỏ phần lẻ; một toán hạng Double/Float để giữ phần lẻ | `kt-numbers` (Integer division) | stable |
| Kiểu số không phải kiểu con của nhau; không chuyển ngầm khi gán/truyền đối số; biểu thức trộn kiểu lấy kiểu theo toán hạng (Int + Long = Long) | `kt-numbers` (Type conversion, Mixed numeric expressions) | stable |
| Đổi số thực sang số nguyên bỏ phần lẻ (9.99.toInt() = 9) | `kt-numbers` | stable |
| Tràn số nguyên quay vòng (Int.MAX_VALUE + 1 = -2147483648), trình biên dịch không tự báo lỗi | `kt-numbers` (Data overflow) | stable |
| Trên JVM số không-null lưu bằng kiểu nguyên thủy; Int? và generic thì boxing; Integer -128..127 được cache nên === "tình cờ" đúng; dùng == | `kt-numbers` (Boxing and caching), `book-kt-essentials` | stable / impl |
| if là biểu thức thì bắt buộc else; when so theo thứ tự, nhánh khớp đầu tiên thắng; when dạng biểu thức phải đủ trường hợp | `kt-control-flow` | stable |
| Tham số mặc định, đối số có tên, hàm một biểu thức; override dùng giá trị mặc định của hàm gốc, không khai báo lại | `kt-functions` | stable |
| Double theo IEEE 754 (tài liệu nêu); số như 0.1 không biểu diễn chính xác (hệ quả chung của số thực nhị phân); tiền nên dùng số nguyên đơn vị nhỏ nhất hoặc BigDecimal | `kt-numbers` (IEEE 754) + kiến thức chung | guideline |
| Bài tập timeLeftLabel | dựa trên "Pretty time display", `book-kt-exercises`; lời giải tự viết | — |
| Sim `kotlin.eval`: giá trị là kết quả tài liệu nêu, không chạy Kotlin trong trang | Minh họa | simp.1, simp.2 |

Kiểm URL (curl, HTTP 200): 4 trang kotlinlang.org; leanpub.com/kotlin_developers (tiêu đề "Kotlin Essentials"), /effectivekotlin, /kotlin_exercises (tiêu đề "Kotlin Exercises").

## K2 · Null safety, smart cast, platform type (2026-11-23)

| Khẳng định | Nguồn | Loại |
|---|---|---|
| Kiểu nullable, ?., chuỗi ?., ?:, !!, let, as?; danh sách nguyên nhân NPE (throw, !!, khởi tạo dở, Java interop) | `kt-null-safety` | stable |
| Bảng điều kiện smart cast: val cục bộ luôn (trừ local delegated); val property nếu private/internal/cùng module, không với open hay getter tự viết; var cục bộ nếu không sửa giữa chừng và không bị lambda sửa bắt giữ; var property không bao giờ | `kt-typecasts` (Smart cast prerequisites) | stable |
| Smart cast qua && / || và trong catch/finally | `kt-typecasts` | stable |
| Platform type T!, nới kiểm tra null; gán vào kiểu non-null thì trình biên dịch chèn kiểm tra (assertion) | `kt-java-interop` | stable |
| Các họ chú thích nullability, gồm Android (androidx.annotation, android.annotation, android.support.annotation) và JSpecify | `kt-java-interop` | stable |
| Loại bỏ platform type càng sớm càng tốt | `book-effective-kotlin` Item 3 | guideline |
| Bài tập patientLabel | dựa trên "Person details display", `book-kt-exercises`; lời giải tự viết | — |
| Sim `kotlin.smartcast`: ví dụ User/Patient/LegacyClinicApi hư cấu; khối "luật smart cast" gộp phân tích luồng dữ liệu | Minh họa | simp.1, simp.2 |

Kiểm URL (curl, HTTP 200): null-safety.html, typecasts.html, java-interop.html.
