/* Thuật ngữ track arch (tiếng Việt). */
ADE.addGlossary('vi', 'arch', {
  "separation-of-concerns": { term: "tách mối quan tâm", def: "Chia app thành các phần (lớp, file, module, tầng) mà mỗi phần có một trách nhiệm rõ ràng; nguyên lý quan trọng nhất trong hướng dẫn kiến trúc của Android.", chapter: "arch/g1" },
  "configuration-change": { term: "thay đổi cấu hình", def: "Xoay màn hình, đổi ngôn ngữ, đổi cỡ chữ…: hệ thống hủy Activity hiện tại và tạo instance mới với cấu hình mới.", chapter: "arch/g1" },
  "state-holder": { term: "state holder (ViewModel)", def: "Lớp giữ và tạo state cho màn hình, tách khỏi Activity; ViewModel là state holder sống qua thay đổi cấu hình.", chapter: "arch/g1" },
  "ssot": {"term": "nguồn sự thật duy nhất (SSOT)", "def": "Chủ duy nhất của một loại dữ liệu: chỉ nó được sửa dữ liệu đó, lộ dữ liệu ra dưới kiểu bất biến và nhận thay đổi qua hàm hay sự kiện. App offline-first thường lấy database làm SSOT.", "chapter": "arch/g2"},
  "udf": {"term": "luồng dữ liệu một chiều (UDF)", "def": "State đi một chiều, từ nơi giữ state xuống UI; sự kiện đi chiều ngược lại, lên tới SSOT, nơi dữ liệu được sửa.", "chapter": "arch/g2"},
  "dependency-rule": {"term": "Dependency Rule", "def": "Quy tắc trung tâm của Clean Architecture (Robert C. Martin, Boudjnah trình bày cho Android): mũi tên phụ thuộc chỉ hướng vào trong, về domain; lớp bên trong không biết gì về lớp bên ngoài.", "chapter": "arch/g2"},
  "dependency-inversion": {"term": "đảo phụ thuộc", "def": "Đặt một interface ở phía cần dùng (ví dụ repository interface cạnh use case) và để lớp cài đặt phụ thuộc vào interface đó, nên mũi tên phụ thuộc đổi chiều so với chiều gọi.", "chapter": "arch/g2"},
  "ui-state": {"term": "UI state", "def": "Bản chụp bất biến của mọi thứ màn hình cần hiển thị, do state holder (thường là ViewModel) tạo ra; thông báo thoáng qua cũng là một phần của nó.", "chapter": "arch/g3"},
  "viewmodel-event": {"term": "sự kiện từ ViewModel", "def": "Hành động UI bắt nguồn từ ViewModel (đặt xong, lỗi, điều hướng). Theo hướng dẫn chính thức, nó luôn phải thành một cập nhật UI state.", "chapter": "arch/g3"},
  "use-case": {"term": "use case", "def": "Lớp ở tầng domain gói một việc nghiệp vụ duy nhất (ví dụ IsSlotBookableUseCase), không giữ dữ liệu thay đổi, gọi an toàn từ main thread. Chỉ thêm khi logic phức tạp hay được nhiều nơi dùng lại.", "chapter": "arch/g5"}
});
