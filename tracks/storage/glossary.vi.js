/* Thuật ngữ track storage (tiếng Việt). */
ADE.addGlossary('vi', 'storage', {
  "app-specific-storage": { term: "bộ nhớ riêng của app", def: "Thư mục chỉ app của bạn dùng (filesDir, cacheDir và bản ngoài của chúng). Không cần quyền; bị xóa khi gỡ app; phần nội bộ được mã hóa từ Android 10.", chapter: "storage/h1" },
  "shared-storage": { term: "bộ nhớ chung (shared storage)", def: "Nơi lưu file người dùng muốn giữ và app khác thấy được: ảnh, video, âm thanh qua MediaStore; tài liệu qua Storage Access Framework. Không bị xóa khi gỡ app.", chapter: "storage/h1" },
  "cache-dir": { term: "thư mục cache (cacheDir)", def: "Thư mục riêng cho dữ liệu tạm. Khi máy thiếu dung lượng, hệ thống có thể xóa file ở đây, nên chỉ để thứ tạo lại hay tải lại được.", chapter: "storage/h1" },
  "datastore": { term: "DataStore", def: "Thư viện Jetpack lưu cặp khóa–giá trị (Preferences DataStore) hay đối tượng có kiểu (Proto DataStore): đọc bằng Flow, ghi bằng hàm suspend theo giao dịch. Thay thế được khuyên cho SharedPreferences, dành cho dữ liệu nhỏ.", chapter: "storage/h1" },
  "room": { term: "Room", def: "Thư viện Jetpack bọc SQLite: entity là bảng, DAO là các hàm truy vấn, câu SQL được kiểm lúc biên dịch. Dành cho dữ liệu có cấu trúc, nhiều bản ghi, cần truy vấn.", chapter: "storage/h1" },
  "atomicfile": { term: "AtomicFile", def: "Lớp của androidx.core ghi file an toàn: ghi bản mới sang file .new, sync rồi đổi tên đè lên file gốc, nên trên đĩa luôn có một bản trọn vẹn. Không khóa file.", chapter: "storage/h2" },
  "anr": { term: "ANR (ứng dụng không phản hồi)", def: "Hệ thống báo khi main thread bị chặn quá lâu, ví dụ không phản hồi một lần chạm trong 5 giây. Ghi đĩa trên main thread là nguyên nhân hay gặp.", chapter: "storage/h3" },
  "dao": { term: "DAO (đối tượng truy cập dữ liệu)", def: "Interface hay abstract class gắn @Dao, khai báo các hàm truy vấn, chèn, sửa, xóa; Room sinh phần cài đặt lúc build và kiểm câu SQL lúc biên dịch.", chapter: "storage/h4" },
  "observable-query": { term: "truy vấn quan sát", def: "Hàm DAO trả về Flow: Room chạy lại câu truy vấn mỗi khi một bảng nó tham chiếu bị ghi, rồi phát kết quả mới.", chapter: "storage/h4" }
});
