# Nghiên cứu track G (Kiến trúc app Android)

Trang developer.android.com đọc ngày 2026-11-23. Sách: Dumbravan, *Clean Android Architecture* (Packt 2022; trang O'Reilly kiểm qua trình duyệt, trang Packt chặn bot nên không dùng); Boudjnah, *Clean Architecture for Android* (BPB). Nguồn chính thức thắng khi mâu thuẫn.

## G1 · Vì sao cần kiến trúc (2026-11-23)

| Khẳng định | Nguồn | Loại |
|---|---|---|
| Component có thể được khởi chạy riêng lẻ, không theo thứ tự, và bị hệ thống hay người dùng hủy bất cứ lúc nào; không giữ dữ liệu hay state trong component | `ax-arch-guide` | stable |
| Tách mối quan tâm là nguyên lý quan trọng nhất; UI dẫn từ model dữ liệu (tốt nhất là lưu bền); tối thiểu UI và data, domain tùy chọn | `ax-arch-guide` | stable |
| Đổi cấu hình: hệ thống gọi onDestroy, hủy Activity, tạo instance mới bằng onCreate | `ax-config-changes` | stable |
| ViewModel giữ state qua thay đổi cấu hình; sống tới khi ViewModelStoreOwner mất (Activity finish); SavedStateHandle giữ cả qua process death | `ax-viewmodel` | stable |
| Test local chạy trên máy phát triển, nhỏ và nhanh; instrumented chạy trên thiết bị thật hay giả lập | `ax-test-fundamentals` | stable |
| App cũ: HttpURLConnection, parse JSON, AsyncTask trong Activity; rò rỉ context; khó test, khó bảo trì khi lớn | `book-dumbravan` ch1 | guideline |
| Số file phải sửa (3 so với 1) | đếm trong app mẫu, ghi trong simp.1 và mục trung thực | simplified |

Kiểm URL: 4 trang developer.android.com HTTP 200 (curl); O'Reilly và BPB qua trình duyệt.
