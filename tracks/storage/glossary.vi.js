/* Thuật ngữ track storage (tiếng Việt). */
ADE.addGlossary('vi', 'storage', {
  "app-specific-storage": { term: "bộ nhớ riêng của app", def: "Thư mục chỉ app của bạn dùng (filesDir, cacheDir và bản ngoài của chúng). Không cần quyền; bị xóa khi gỡ app; phần nội bộ được mã hóa từ Android 10.", chapter: "storage/h1" },
  "shared-storage": { term: "bộ nhớ chung (shared storage)", def: "Nơi lưu file người dùng muốn giữ và app khác thấy được: ảnh, video, âm thanh qua MediaStore; tài liệu qua Storage Access Framework. Không bị xóa khi gỡ app.", chapter: "storage/h1" },
  "cache-dir": { term: "thư mục cache (cacheDir)", def: "Thư mục riêng cho dữ liệu tạm. Khi máy thiếu dung lượng, hệ thống có thể xóa file ở đây, nên chỉ để thứ tạo lại hay tải lại được.", chapter: "storage/h1" },
  "datastore": { term: "DataStore", def: "Thư viện Jetpack lưu cặp khóa–giá trị (Preferences DataStore) hay đối tượng có kiểu (Proto DataStore): đọc bằng Flow, ghi bằng hàm suspend theo giao dịch. Thay thế được khuyên cho SharedPreferences, dành cho dữ liệu nhỏ.", chapter: "storage/h1" },
  "room": { term: "Room", def: "Thư viện Jetpack bọc SQLite: entity là bảng, DAO là các hàm truy vấn, câu SQL được kiểm lúc biên dịch. Dành cho dữ liệu có cấu trúc, nhiều bản ghi, cần truy vấn.", chapter: "storage/h1" }
});
