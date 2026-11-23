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

## Chọn kiểu hình theo nội dung (2026-11-24)

Người dùng giao quyền (2026-11-23): mỗi chương, và mỗi phần trong chương, dùng kiểu hình dễ hình dung nhất cho đúng nội dung đó, không mặc định là luồng bốn khối. Riêng UI/UX đang tạm dừng nên không áp dụng ở đó. Sơ đồ node của sim vẫn giữ làm tab phụ, để dòng sự kiện và trạng thái node còn đó. Chương có hai cơ chế khác nhau thì có hai hình.

| Kiểu hình | Hợp với | Cách vẽ hiện có |
|---|---|---|
| Luồng (pipeline) | dữ liệu hay lời gọi đi qua các khâu theo một chiều | lõi `layout: 'pipeline'` |
| Làn thời gian (lanes) | nhiều luồng, tiến trình hay tác nhân chạy song song theo thời gian | lõi `layout: 'lanes'` (Coroutines) |
| Vòng (cycle) | vòng lặp: sự kiện lên, state xuống; red, green, refactor | lõi `layout: 'cycle'` |
| Cây (tree), cây quyết định | phân cấp; chọn A hay B theo câu hỏi | lõi `layout: 'tree'`; cây hộp lồng `.vz-box` (Animation C0) |
| Bảng, ma trận | so nhiều trường hợp theo hai chiều; bảng tra triệu chứng | `.vz-table` (Kotlin K4, K10, K0) |
| Bảng tính | công thức có số thay vào và ví dụ kiểm chứng | `.vz-table` |
| Hộp lồng | phạm vi lồng nhau: receiver, lõi và vỏ, scope | `.vz-box` (Kotlin K12) |
| Dãy ô (strip) | phần tử theo vị trí: danh sách, trang, khúc tệp, phiên bản | `.vz-chip` (Runtime B3, B4, LZ) |
| **Đồ thị phụ thuộc** | node có cạnh có hướng; cạnh sai chiều hay vòng phụ thuộc tô đỏ | **MỚI**: SVG tự vẽ trong `tracks/<t>/views/visuals.js`, không sửa lõi |
| **Sơ đồ tuần tự** | client, server và dịch vụ trao đổi theo thời gian; tin bị mất, trùng hay đến muộn | **MỚI**: như trên |
| **Đường ray (railway)** | hai đường thành công và lỗi; giá trị rẽ sang đường lỗi rồi đi tiếp tới cuối | **MỚI**: như trên |

Hình **MỚI** viết một lần trong track đầu tiên cần nó. Nếu track thứ hai cũng cần, chuyển lên `shared/` thay vì chép lại. Mỗi dàn ý track (`docs/tracks/*.md`) ghi rõ kiểu hình của từng chương ở cột "Hình chính".

## Nguồn nghiên cứu về cách học

- Dunlosky et al. (2013), *Improving Students' Learning With Effective Learning Techniques*, Psychological Science in the Public Interest 14(1).
- Roediger & Karpicke (2006), *Test-Enhanced Learning*, Psychological Science 17(3).
- Cepeda et al. (2006), *Distributed Practice in Verbal Recall Tasks*, Psychological Bulletin 132(3).
- Sweller, van Merriënboer & Paas (2019), *Cognitive Architecture and Instructional Design: 20 Years Later*, Educational Psychology Review 31: cho worked example, fading và giảm tải nhận thức.
- Mayer, *Multimedia Learning* (nguyên tắc coherence, signaling, segmenting, pre-training): cho hình và chữ đi cùng nhau, chia bước, nhấn đúng chỗ.
