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

## K3 · Class, interface, object và thứ tự khởi tạo (2026-11-23)

| Khẳng định | Nguồn | Loại |
|---|---|---|
| Khối init chạy theo thứ tự xuất hiện, xen với giá trị khởi tạo property | `kt-classes` (Initializer blocks) | stable |
| Class final mặc định; open/override | `kt-inheritance` | stable |
| Lớp cha khởi tạo là bước đầu, chỉ sau việc tính đối số cho constructor lớp cha; tránh dùng thành viên open trong constructor/initializer/init của lớp cha | `kt-inheritance` (Derived class initialization order) | stable |
| Constructor lớp cha gọi open member dùng trạng thái chưa khởi tạo là một nguồn NPE | `kt-null-safety` | stable |
| Interface có hàm có thân, không giữ trạng thái | `kt-interfaces` | stable |
| object declaration khởi tạo lười ở lần truy cập đầu, an toàn luồng; object expression ngay tại chỗ; companion khi lớp được nạp (như static initializer) | `kt-objects` | stable |
| Setter tự viết chạy mỗi lần gán, trừ lúc khởi tạo; field | `kt-properties` | stable |
| lateinit: var, không null, không nguyên thủy; ngoại lệ nêu tên property; isInitialized | `kt-properties` | stable |
| NPE cụ thể khi DetailScreen đọc title trong render() (field null trên JVM) | suy ra từ hai dòng trên; site chưa chạy | simplified |
| object giữ Activity gây rò rỉ bộ nhớ | kiến thức Android chung, không trích nguồn | guideline |
| Bài tập VaccineStock | dựa trên "Implementing the Product class", `book-kt-exercises`; lời giải tự viết | — |

Kiểm URL (curl, HTTP 200): classes, inheritance, interfaces, object-declarations, properties.

## K4 · Data class và bằng nhau (2026-11-23)

| Khẳng định | Nguồn | Loại |
|---|---|---|
| data class sinh equals/hashCode, toString, componentN, copy từ mọi property của constructor chính; constructor chính ≥ 1 tham số, đều val/var; property trong thân bị loại | `kt-data-classes` | stable |
| copy() là bản sao nông, tham chiếu dùng chung | `kt-data-classes` | stable |
| a == b dịch thành a?.equals(b) ?: (b === null); === là bằng nhau tham chiếu | `kt-equality` | stable |
| HashSet/HashMap là bảng băm; hợp đồng hashCode (ổn định, bằng nhau thì cùng hash); ví dụ FullName bị sửa sau khi add: contains false, first() == person true | `book-effective-kotlin` Item 43 | guideline |
| Hạn chế mutability; object bất biến an toàn làm phần tử set/key map | `book-effective-kotlin` Item 1 | guideline |
| Compose và StateFlow so state bằng equals | dẫn sang track Runtime B4/B8 và Coroutines A7 (nguồn ở các chương đó) | — |
| Bucket trong sim (tổng mã ký tự mod 4) | Minh họa | simp.1 |
| Bài tập Patient | dựa trên "Data class practice", `book-kt-exercises`; lời giải tự viết | — |

Kiểm URL (curl, HTTP 200): data-classes.html, equality.html.

## K5 · Enum, sealed và when (2026-11-23)

| Khẳng định | Nguồn | Loại |
|---|---|---|
| Kiểu con trực tiếp của sealed biết lúc biên dịch; cùng package và module; không thêm được sau khi module biên dịch | `kt-sealed` | stable |
| when với sealed: trình biên dịch kiểm phủ đủ, không cần else; ngoại lệ: when trên sealed expect trong mã chung multiplatform vẫn cần else | `kt-sealed` | stable |
| when dạng biểu thức phải phủ đủ; subject Boolean/enum/sealed có thể phủ đủ không cần else; when dạng câu lệnh không bắt buộc (nói chung) | `kt-control-flow` | stable |
| enum: name, ordinal (từ 0), entries; valueOf cần tên khớp chính xác, nếu không ném IllegalArgumentException; entries.getOrNull(index) | `kt-enum` | stable |
| Tránh else trên sealed/enum tự quản lý vì nó nuốt kiểu con mới | suy ra từ hai dòng trên | guideline |
| KHÔNG khẳng định quy tắc phủ đủ cho when dạng câu lệnh trên sealed (tài liệu không nêu ở trang đã đọc) | — | ghi trong mục trung thực |
| Bài tập ClinicDay | dựa trên "Days of the week enum", `book-kt-exercises`; lời giải tự viết | — |

Kiểm URL (curl, HTTP 200): sealed-classes.html, enum-classes.html.

## K6 · Ngoại lệ, require/check và use (2026-11-23)

| Khẳng định | Nguồn | Loại |
|---|---|---|
| Kotlin coi mọi ngoại lệ là unchecked; ngoại lệ là lớp con của Exception/Throwable | `kt-exceptions-lang` | stable |
| require → IllegalArgumentException; check, error() → IllegalStateException; require/check cho phép smart cast sau khi kiểm | `kt-exceptions-lang`, API require | stable |
| Catch khớp đầu tiên theo kiểu hoặc lớp cha; xếp từ cụ thể tới chung; try-catch là biểu thức; finally luôn chạy, không đổi kết quả | `kt-exceptions-lang` | stable |
| throw có kiểu Nothing (kiểu con của mọi kiểu); TODO() ném NotImplementedError | `kt-exceptions-lang` | stable |
| Không tạo ngoại lệ bằng object vì stack trace gắn với chỗ tạo | `kt-exceptions-lang` (Kotlin Essentials có ví dụ dùng object; theo tài liệu chính thức, ghi trong mục trung thực) | stable |
| Ngoại lệ kết thúc hàm ngay, quá trình lặp lại ở hàm gọi cho tới try có catch phù hợp | `book-kt-essentials` | guideline |
| use đóng Closeable dù có ngoại lệ hay không | `kt-use` | stable |
| use bắt Throwable để nhớ rồi ném lại; closeFinally: lỗi của close() được addSuppressed vào lỗi chính | `kt-stdlib-closeable` (tag v2.1.0, đã đọc mã) | version |
| runCatching bắt mọi Throwable thành Result thất bại | `kt-runcatching` | stable |
| NumberFormatException là lớp con của IllegalArgumentException | `jdk-nfe` (Java SE 17 API) | stable |
| Đặt require/check ở đầu hàm, trước khi sửa trạng thái; ưu tiên lỗi chuẩn; đóng tài nguyên bằng use; GC dọn tài nguyên chưa đóng sau một thời gian | `book-effective-kotlin` Items 5, 6, 8 | guideline |
| catch rộng trong coroutine bắt cả CancellationException | chỉ trỏ sang track Coroutines, không khẳng định chi tiết ở đây | — |
| Bài tập slotOf/parseInput | dựa trên "Catching exceptions" và "Specify expectations", `book-kt-exercises`; lời giải tự viết | — |

Kiểm URL (curl, HTTP 200): exceptions.html, API use, require, run-catching; Closeable.kt ở tag v2.1.0 (raw và blob); trang Oracle NumberFormatException (Java 17). Id `kt-exceptions` đã dùng ở track Coroutines (trang Coroutine exceptions handling), nên trang ngôn ngữ dùng id `kt-exceptions-lang`.

## K7 · Collection: read-only, mutable và xử lý (2026-11-23)

| Khẳng định | Nguồn | Loại |
|---|---|---|
| Mỗi loại có interface read-only và Mutable; ưu tiên read-only khi nơi gọi không cần sửa; read-only khác bất biến (kotlinx-collections-immutable); Map không kế thừa Collection | `kt-collections-overview` (trang ghi 03 November 2026) | stable |
| So bằng: List theo thứ tự, Set và Map không xét thứ tự; mặc định ArrayList, LinkedHashSet, LinkedHashMap giữ thứ tự thêm; HashSet/HashMap không bảo đảm thứ tự, tốn ít bộ nhớ hơn | `kt-collection-types` | stable |
| Gán tạo tham chiếu mới tới cùng object; tham chiếu List tới MutableList thấy trạng thái hiện tại; toList/toMutableList là bản chụp nông | `kt-constructing-collections` | stable |
| map trả list kết quả cùng thứ tự; mapKeys/mapValues biến đổi key hoặc value của map | `kt-collection-transformations` | stable |
| Map<out K, V>.map(transform): List<R>; Map<out K, V>.mapValues(…): Map<K, R> (Maps.kt) | `kt-stdlib-maps` (tag v2.1.0, đã đọc chữ ký) | version |
| get trả null khi thiếu key, getValue ném, getOrDefault/getOrElse; filterKeys/filterValues trả map mới | `kt-map-operations` | stable |
| map/filter của stdlib tạo ArrayList rồi trả về kiểu List; down-cast listOf sang MutableList rồi add ném UnsupportedOperationException trên JVM (Arrays.ArrayList), không được bảo đảm về sau; dùng toMutableList | `book-effective-kotlin` Item 1 | guideline |
| Bài tập Pharmacy | dựa trên "Inventory management", `book-kt-exercises`; lời giải tự viết | — |

Kiểm URL (curl, HTTP 200): collections-overview, collection-types, constructing-collections, collection-transformations, map-operations; _Maps.kt ở tag v2.1.0 (raw và blob).

## K8 · Lambda, closure và inline (2026-11-23)

| Khẳng định | Nguồn | Loại |
|---|---|---|
| Kiểu hàm, lambda, it, trailing lambda, tham chiếu hàm; closure: lambda đọc và sửa được biến ở phạm vi ngoài | `kt-lambdas` | stable |
| Hàm bậc cao: mỗi hàm là object và bắt closure (cấp phát, lời gọi ảo); inline chép hàm và lambda vào chỗ gọi; noinline; crossinline cấm non-local return khi lambda gọi từ ngữ cảnh khác; reified chỉ ở hàm inline; cảnh báo khi không có gì để inline; inline làm mã lớn lên | `kt-inline` (trang ghi 23 June 2025) | stable |
| return trần chỉ thoát hàm có tên hoặc hàm ẩn danh; trong lambda là lỗi trừ khi lambda được inline (non-local return); return@forEach giống continue; giả lập break bằng run loop@ | `kt-returns` (trang ghi 29 September 2026), `kt-inline` | stable |
| Từ Kotlin 2.0.0 lambda mặc định sinh bằng invokedynamic (trước đó lớp ẩn danh, -Xlambdas=indy từ 1.5.0); -Xlambdas=class giữ cách cũ | `kt-whatsnew20` | version |
| forEach/map/filter/fold của stdlib là inline; lambda truyền vào không tạo object | `book-functional-kotlin` | guideline |
| Lambda lưu trong object toàn cục bắt this của Activity làm Activity không được giải phóng | suy luận từ closure (`kt-lambdas`) + cách GC giữ object còn tham chiếu; ghi rõ trong mục trung thực | simplified |
| Bài tập mapAll / firstOfOrNull | dựa trên "Implement map" và "Inline functions", `book-kt-exercises`; lời giải tự viết | — |

Đổi nhãn log `check` của track từ "kiểm kiểu (biên dịch)" thành "kiểm lúc biên dịch" để đúng cả với bước trình biên dịch quyết định inline.
Kiểm URL (curl, HTTP 200): lambdas, inline-functions, returns, whatsnew20, leanpub.com/kotlin_functional.

## K9 · Sequence và hiệu năng xử lý collection (2026-11-23)

| Khẳng định | Nguồn | Loại |
|---|---|---|
| Iterable xử lý háo hức, mỗi bước trả collection trung gian; Sequence lười, từng phần tử qua mọi bước; chỉ chạy khi kết quả cả chuỗi được yêu cầu; take đủ thì dừng; trung gian/cuối; phần tử chỉ lấy được bằng thao tác cuối; overhead đáng kể với collection nhỏ hay phép tính đơn giản; generateSequence, sequence { yield }; thao tác có trạng thái | `kt-sequences` (trang ghi 03 November 2026) | stable |
| Ưu tiên Sequence cho collection lớn có nhiều bước; filter không biết trước kích thước nên list có thể phải chép mảng khi lớn dần | `book-effective-kotlin` Item 54 | guideline |
| Giảm số thao tác: mapNotNull thay map + filterNotNull, filterNotNull thay lọc rồi ép non-null | `book-effective-kotlin` Item 57 (đã kiểm: sách KHÔNG nêu filterIsInstance, nên chương không nói) | guideline |
| Số lần chạy lambda (13 so với 5) và số phần tử đã đọc | tính trên dữ liệu mẫu, model tính lại trong selfCheck; không phải tỉ lệ tốc độ (ghi trong mục trung thực) | simplified |
| Bài tập dự đoán thứ tự in | dựa trên "Understanding sequences", `book-kt-exercises`; hàm và dữ liệu tự đặt | — |

Ghi chú sơ đồ (đã báo người dùng từ trước, không tự đổi): luồng Sequence có thể dễ hình dung hơn bằng sơ đồ dạng luồng từng phần tử; chương vẫn giữ sơ đồ node theo quy định, các node là đúng các bước filter → map → take.
Kiểm URL (curl, HTTP 200): sequences.html.

## K10 · Generics và variance (2026-11-23)

| Khẳng định | Nguồn | Loại |
|---|---|---|
| Suy luận kiểu tham số; upper bound (mặc định Any?), where; Java generic bất biến, ví dụ List<String> → List<Object> gây ClassCastException; out: chỉ vị trí trả ra, C<Base> là cha của C<Derived>; in: nghịch biến (Comparable<in T>); "Consumer in, Producer out"; type projection (Array<out Any>, Array<in String>), star-projection; type erasure, cấm is List<Int>, ép kiểu generic không được kiểm; reified là ngoại lệ | `kt-generics` | stable |
| Collection<out E>, List<out E>, MutableList<E>, Map<K, out V> | `kt-stdlib-collections` (builtins Collections.kt tag v2.1.0, dòng 39/124/179/295) | version |
| public interface Flow<out T> | `kx-flow-src` (kotlinx.coroutines 1.9.0, Flow.kt dòng 176) | version |
| Nothing là kiểu con của mọi kiểu, List<Nothing> hợp với mọi list; mẫu Response<out R, out E> với Success : Response<R, Nothing> | `book-advanced-kotlin` | guideline |
| Bài tập LoadResult | dựa trên "Generic Response", `book-kt-exercises`; tên và lời giải tự viết | — |
| Notifier<in T> | kiểu tự đặt cho ví dụ, chỉ dựa vào quy tắc in của tài liệu | — |

Kiểm URL (curl, HTTP 200): generics.html; Collections.kt (raw và blob, v2.1.0); Flow.kt (raw và blob, 1.9.0); leanpub.com/advanced_kotlin.
