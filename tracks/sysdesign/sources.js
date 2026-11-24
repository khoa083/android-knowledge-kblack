/* Nguồn của track I (Thiết kế hệ thống phía mobile). Sách đọc từ bản trong thư viện cá nhân ngày 2026-11-24 (docs/research/sysdesign.md). */
(function () {
  var s = function (id, title, url, org, label, vi, en) { return { id: id, title: title, url: url, org: org, tracks: ['sysdesign'], label: label, lang: 'en', supports: { vi: vi, en: en } }; };
  ADE.addSources([
    s('book-xu1', 'System Design Interview: An Insider\'s Guide, vol. 1 (Alex Xu)', 'https://bytebytego.com/', 'ByteByteGo (sách)', 'guideline',
      'Ch.2: ước lượng nhanh là quá trình, không cần chính xác; làm tròn số, viết rõ giả định và đơn vị. Ch.3: khung bốn bước của Alex Xu (hiểu đề và khoanh phạm vi, đề xuất thiết kế tổng quát, đi sâu, tổng kết); đừng trả lời ngay, hãy hỏi để làm rõ yêu cầu và ghi lại giả định; thiết kế quá mức là dấu hiệu xấu (I1).',
      'Ch.2: back-of-the-envelope estimation is about the process, not precision; round numbers, write down assumptions and units. Ch.3: Alex Xu\'s four-step framework (understand the problem and scope, propose a high-level design, deep dive, wrap up); do not answer at once, ask to clarify requirements and write down assumptions; over-engineering is a red flag (I1).'),
    s('book-tjeerd', 'Mobile System Design (Tjeerd in \'t Veen), bản early release', 'https://www.mobilesystemdesign.com/', 'Resourceful Engineering (sách)', 'guideline',
      'Ch.2: đừng mở IDE ngay, hãy tìm yêu cầu phụ trước; thiết kế thường chỉ có trường hợp đẹp, hãy xin bản với nội dung xấu nhất; bàn sớm về lỗi và ưu tiên lỗi không chặn màn hình; thống nhất với backend về phiên, token, timeout, mã lỗi (client tự dịch theo mã) và thông báo đẩy theo ngôn ngữ của máy (I1).',
      'Ch.2: do not open the IDE yet, uncover secondary requirements first; designs usually show only the best case, ask for a worst-case content version; discuss errors early and prefer errors that do not block the screen; align with the backend on sessions, tokens, timeouts, error codes (the client localises by code) and push notifications in the device\'s language (I1).')
  ]);
})();
