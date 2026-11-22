# Khung chương v2 (dùng cho mọi track)

> Khung sư phạm cho chương dài, viết 2026-11-22. Phần kỹ thuật (key, loại khối) nằm ở `docs/core-api.md` §2.1.
>
> Cơ sở:
> - `docs/androidbooks-knowledge/learning-methods.md`, phần micro-cycle;
> - `docs/visual-explainer-improvement-guide.md` §3–§5, §8;
> - các nguồn nghiên cứu ghi ở cuối file này.
>
> Giữ đúng sắc thái của bằng chứng:
> - retrieval practice và distributed practice có hỗ trợ rộng;
> - self-explanation và interleaving phụ thuộc dạng bài.

## Thứ tự một chương

| # | Phần | Khối dùng | Vì sao |
|---|---|---|---|
| 0 | **Ôn chương trước**: 1–2 câu hỏi về chương trước, không phải chương đầu | `ask` | Nhớ lại có khoảng cách (spacing, retrieval) |
| 1 | **Bản chất**: 2–4 câu, nói chương trả lời câu hỏi gì | `essence` | Định hướng; người học biết mình đang tìm gì |
| 2 | **Vấn đề**: viết theo cách cũ thì đau ở đâu, có mã thật | `p`, `kt`, `bug` | Người học thấy cần khái niệm trước khi gặp nó |
| 3 | **Giảng từng bước** | `p`, `kt`, `out`, `note kind=analogy` | Mỗi đoạn mã ngắn, thêm một ý mỗi lần (giảm tải nhận thức). Ví von đi trước, ngay sau đó nói phần nào khớp và phần nào không khớp |
| 4 | **Đoán trước rồi xem**: câu đoán đặt trước sim hoặc trước output (`simAfter`) | `predict` → sim | Dự đoán trước khi lộ đáp án; đáp án không được nằm sẵn trên màn hình |
| 5 | **Dưới mui xe**: cơ chế thật, mã sau khi biến đổi, trích mã nguồn thư viện | `p`, `kt`, `note kind=mechanism` kèm phiên bản | Hiểu đủ sâu để tự sửa bug. Tách rõ hợp đồng API ổn định và chi tiết implementation |
| 6 | **Bug thường gặp**: triệu chứng → nguyên nhân cơ chế → sửa | `bug` | Chuyển giao (transfer): áp nguyên lý lên triệu chứng mới |
| 7 | **Bài tập**: worked example trước, rồi bài khuyết bước, rồi bài mới | `ex` (+ `hint`, `sol`) | Worked example rồi giảm dần phần làm sẵn (fading) |
| 8 | **Tự trả lời** cuối mỗi phần lớn và cuối chương | `ask`, `quiz` | Nhớ lại và tự giải thích "vì sao" |

## Quy tắc viết

- **Mỗi đoạn mã có output dự đoán được.** Nếu output phụ thuộc lịch chạy, ghi rõ đó là "một thứ tự có thể xảy ra".
- **Mỗi thuật ngữ mới:**
  - nói bằng lời thường trước;
  - rồi tên kỹ thuật;
  - rồi link glossary `[[term:id]]` nếu có.
- **Số liệu:**
  - ghi nguồn hoặc nhãn "minh hoạ";
  - con số trong sim không phải độ trễ thật.
- **Chi tiết implementation:**
  - phải có phiên bản hoặc commit, và nhãn `impl`;
  - không trình bày nó như API ổn định.
- **Ví dụ:** dùng một ví dụ xuyên chương (ví dụ: màn hình tin tức lấy dữ liệu từ API) để người học không phải học lại bối cảnh.
- **Bảng nguồn:** mỗi chương ghi vào `docs/research/<track>.md`, gồm:
  - sách, chương và trang đã đọc;
  - tài liệu chính thức;
  - phiên bản mã nguồn;
  - claim nào dựa trên nguồn nào.

## Minh hoạ trong chương

- Dùng sim có sẵn khi nó đúng câu hỏi. Thêm sim mới khi chương cần một hình chưa có, ví dụ state machine của continuation.
- **Mỗi hình:**
  - chỉ một ý;
  - có caption "Bạn đang xem gì";
  - có chú giải.
- **Chuyển động:**
  - mỗi bước chỉ một chuyển động chính, cộng tối đa một tín hiệu phụ;
  - tắt chuyển động vẫn hiểu được;
  - chuyển cảnh trang/bước/chỉ số/log do lõi lo, xem `docs/design-principles.md` §5.1. Sim mới phải dùng `movingSignals` hoặc `nodeStates` thay đổi giữa các bước để sơ đồ có chuyển động thật, không chỉ đổi chữ.

## Nguồn nghiên cứu về cách học

- Dunlosky et al. (2013), *Improving Students' Learning With Effective Learning Techniques*, Psychological Science in the Public Interest 14(1).
- Roediger & Karpicke (2006), *Test-Enhanced Learning*, Psychological Science 17(3).
- Cepeda et al. (2006), *Distributed Practice in Verbal Recall Tasks*, Psychological Bulletin 132(3).
- Sweller, van Merriënboer & Paas (2019), *Cognitive Architecture and Instructional Design: 20 Years Later*, Educational Psychology Review 31: cho worked example, fading và giảm tải nhận thức.
- Mayer, *Multimedia Learning* (nguyên tắc coherence, signaling, segmenting, pre-training): cho hình và chữ đi cùng nhau, chia bước, nhấn đúng chỗ.
