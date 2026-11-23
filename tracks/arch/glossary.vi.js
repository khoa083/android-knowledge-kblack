/* Thuật ngữ track arch (tiếng Việt). */
ADE.addGlossary('vi', 'arch', {
  "separation-of-concerns": { term: "tách mối quan tâm", def: "Chia app thành các phần (lớp, file, module, tầng) mà mỗi phần có một trách nhiệm rõ ràng; nguyên lý quan trọng nhất trong hướng dẫn kiến trúc của Android.", chapter: "arch/g1" },
  "configuration-change": { term: "thay đổi cấu hình", def: "Xoay màn hình, đổi ngôn ngữ, đổi cỡ chữ…: hệ thống hủy Activity hiện tại và tạo instance mới với cấu hình mới.", chapter: "arch/g1" },
  "state-holder": { term: "state holder (ViewModel)", def: "Lớp giữ và tạo state cho màn hình, tách khỏi Activity; ViewModel là state holder sống qua thay đổi cấu hình.", chapter: "arch/g1" }
});
