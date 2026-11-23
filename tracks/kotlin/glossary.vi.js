/* Thuật ngữ track kotlin (tiếng Việt). */
ADE.addGlossary('vi', 'kotlin', {
  "val-var": { term: "val / var", def: "val là tham chiếu chỉ gán một lần; var gán lại được. val không làm object bên trong bất biến: một val trỏ tới MutableList vẫn thêm phần tử được.", chapter: "kotlin/k1" },
  "type-inference": { term: "suy kiểu (type inference)", def: "Trình biên dịch tự xác định kiểu của biến hoặc biểu thức từ giá trị khởi tạo; kiểu được chốt lúc biên dịch, không đổi lúc chạy.", chapter: "kotlin/k1" },
  "integer-division": { term: "chia nguyên", def: "Phép chia giữa hai số nguyên trả về số nguyên, phần lẻ bị bỏ (5 / 2 = 2). Muốn có phần lẻ, một toán hạng phải là Double hoặc Float.", chapter: "kotlin/k1" },
  "smart-cast": { term: "smart cast", def: "Trình biên dịch tự coi biến là kiểu hẹp hơn (ví dụ String thay vì String?) sau một phép kiểm, chỉ khi chứng minh được biến không đổi giữa lúc kiểm và lúc dùng.", chapter: "kotlin/k2" },
  "platform-type": { term: "platform type (T!)", def: "Kiểu của giá trị đến từ Java không có chú thích nullability; nghĩa là T hoặc T?. Kotlin nới kiểm tra null cho nó, nên có thể NPE lúc chạy.", chapter: "kotlin/k2" },
  "elvis": { term: "Elvis ?:", def: "Toán tử trả về vế trái nếu khác null, ngược lại trả vế phải; vế phải có thể là return hoặc throw.", chapter: "kotlin/k2" },
  "lateinit": { term: "lateinit", def: "Đánh dấu một var không null sẽ được gán sau khi tạo object; đọc trước khi gán ném UninitializedPropertyAccessException. Không dùng cho kiểu nguyên thủy.", chapter: "kotlin/k3" },
  "companion-object": { term: "companion object", def: "object gắn với một class, chứa thành viên gọi qua tên lớp (như static của Java); khởi tạo khi lớp được nạp.", chapter: "kotlin/k3" },
  "data-class": { term: "data class", def: "Class có trình biên dịch sinh equals, hashCode, toString, componentN và copy từ các property của constructor chính.", chapter: "kotlin/k4" },
  "hash-table": { term: "bảng băm (hash table)", def: "Cấu trúc bên dưới HashSet/HashMap: mảng các bucket; hashCode chọn bucket, equals so trong bucket. Phần tử bị sửa sau khi thêm có thể nằm sai bucket.", chapter: "kotlin/k4" },
  "sealed": { term: "sealed class / interface", def: "Kiểu có tập kiểu con trực tiếp cố định, biết lúc biên dịch (cùng package và module); when trên nó có thể phủ đủ mà không cần else.", chapter: "kotlin/k5" },
  "exhaustive": { term: "phủ đủ (exhaustive)", def: "when xử lý mọi trường hợp có thể của subject; bắt buộc khi when là biểu thức.", chapter: "kotlin/k5" },
  "nothing-type": { term: "Nothing", def: "Kiểu của biểu thức không bao giờ hoàn tất bình thường, như throw hay TODO(); là kiểu con của mọi kiểu, nên dùng được sau ?: hay trong một nhánh when.", chapter: "kotlin/k6" },
  "precondition": { term: "require / check / error", def: "Hàm kiểm điều kiện của stdlib: require cho tham số (IllegalArgumentException), check cho trạng thái (IllegalStateException), error() ném IllegalStateException ngay.", chapter: "kotlin/k6" },
  "use-function": { term: "use", def: "Hàm mở rộng trên Closeable: chạy khối rồi luôn đóng tài nguyên, kể cả khi khối ném ngoại lệ; ngoại lệ vẫn được ném tiếp.", chapter: "kotlin/k6" },
  "read-only-collection": { term: "collection read-only", def: "Interface như List, Set, Map chỉ có thao tác đọc; nghĩa là không sửa được QUA tham chiếu này, không có nghĩa object bên dưới bất biến.", chapter: "kotlin/k7" },
  "map-values": { term: "mapValues / mapKeys", def: "Biến đổi value (hoặc key) của một Map và trả về Map mới; khác map, vốn trả về List.", chapter: "kotlin/k7" },
  "closure": { term: "closure", def: "Các biến ở phạm vi bên ngoài mà một lambda (hay hàm cục bộ, object expression) truy cập được; lambda giữ chúng sống chừng nào lambda còn sống.", chapter: "kotlin/k8" },
  "inline-function": { term: "hàm inline", def: "Hàm mà trình biên dịch chép thân (và các lambda truyền vào) vào chỗ gọi thay vì gọi; không tạo object hàm cho lambda và cho phép non-local return, reified.", chapter: "kotlin/k8" },
  "non-local-return": { term: "non-local return", def: "return trần nằm trong lambda nhưng thoát hàm bao ngoài; chỉ được phép khi lambda được inline.", chapter: "kotlin/k8" },
  "when-expression": { term: "biểu thức when", def: "when trả về giá trị của nhánh khớp đầu tiên; khi dùng như biểu thức, các nhánh phải phủ đủ mọi trường hợp (thường bằng else).", chapter: "kotlin/k1" }
});
