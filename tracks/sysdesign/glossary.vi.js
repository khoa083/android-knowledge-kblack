/* Thuật ngữ track sysdesign (tiếng Việt). */
ADE.addGlossary('vi', 'sysdesign', {
  "secondary-requirement": { term: "yêu cầu phụ", def: "Yêu cầu không hiện trên bản thiết kế màn hình nhưng app phải có: trạng thái lỗi, rỗng, mất mạng, hết phiên, ngôn ngữ của thông báo. Tìm ra bằng cách hỏi designer và backend trước khi viết mã.", chapter: "sysdesign/i1" },
  "back-of-envelope": { term: "ước lượng nhanh", def: "Tính áng chừng bằng số tròn để biết một thiết kế có đáp ứng yêu cầu không, ví dụ dung lượng ảnh mỗi ngày. Quan trọng là quá trình và giả định, không phải độ chính xác.", chapter: "sysdesign/i1" },
  "non-functional-requirement": { term: "yêu cầu phi chức năng", def: "Yêu cầu về chất lượng thay vì tính năng: độ trễ, pin, dữ liệu di động, chạy được khi mất mạng, kích thước app.", chapter: "sysdesign/i1" },
  "process-death": { term: "process bị giết", def: "Hệ thống kết thúc cả process của app, thường khi app đang ở nền và máy thiếu RAM. Mọi thứ trong bộ nhớ của process mất cùng lúc, kể cả ViewModel; người dùng quay lại thì có process mới.", chapter: "sysdesign/i2" },
  "cached-process": { term: "process cached", def: "Process hiện không cần, thường giữ Activity đã onStop(). Là nhóm bị giết đầu tiên khi thiếu bộ nhớ; app ở nhóm này nên dừng mọi việc.", chapter: "sysdesign/i2" },
  "lmkd": { term: "lmkd", def: "Low memory killer daemon: tiến trình hệ thống theo dõi áp lực bộ nhớ và giết những process ít cần thiết nhất, dựa trên điểm oom_adj của từng process.", chapter: "sysdesign/i2" },
  "saved-state": { term: "saved state", def: "Dữ liệu nhỏ (id, chữ nhập) app ghi qua SavedStateHandle hay rememberSaveable. Hệ thống giữ bản sao đã tuần tự hóa ngoài process, nên nó sống qua cả đổi cấu hình lẫn process bị giết.", chapter: "sysdesign/i2" },
  "offset-pagination": { term: "phân trang offset", def: "Xin trang bằng vị trí: bỏ qua N mục, lấy M mục (offset/limit, hay page/size). Danh sách đổi giữa hai trang thì vị trí trôi, gây mục lặp hoặc bị bỏ sót.", chapter: "sysdesign/i7" },
  "cursor-pagination": { term: "phân trang cursor", def: "Xin trang bằng nội dung: \"các mục sau mục này\" theo một khóa sắp xếp có thứ tự toàn phần, như (giờ đăng, id). Thay đổi phía trên không làm lệch trang sau.", chapter: "sysdesign/i7" },
  "page-token": { term: "page token", def: "Chuỗi mờ server trả trong next_page_token để app gửi lại khi xin trang kế. App không đọc hay tự tạo token; token rỗng nghĩa là hết danh sách.", chapter: "sysdesign/i7" }
});
