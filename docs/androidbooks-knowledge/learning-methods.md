# Cách dạy để nhớ và hiểu sâu

## Nguyên tắc dùng trong mọi chương

1. **Retrieval practice:** trước khi đọc lời giải, yêu cầu người học tự kể lại data flow/state transition; phản hồi ngay sau câu trả lời. Không chỉ tô sáng hoặc đọc lại.
2. **Spaced practice:** quay lại khái niệm ở các buổi sau và ở đầu track kế tiếp; khoảng cách nên tăng khi trả lời vững và rút ngắn khi quên. Không tuyên bố có một lịch ngày cố định tối ưu cho mọi người.
3. **Worked example → fading:** xem một ví dụ hoàn chỉnh, sau đó một ví dụ khuyết bước, rồi giải bài mới. Với runtime/bytecode, bắt đầu từ code ngắn và chỉ thêm một suspension point/branch mỗi lần.
4. **Self-explanation/elaboration:** hỏi “vì sao thread không block?”, “ai đã đọc state?”, “vì sao key này đổi effect lifecycle?”; người học giải thích quan hệ nhân quả bằng lời của mình.
5. **Prediction before reveal:** yêu cầu chọn label/Job/phase/frame value trước khi Step; sau đó so dự đoán với trace.
6. **Dual coding có kỷ luật:** lời giải và sơ đồ cùng diễn tả một ý nhưng không lặp chi tiết gây nhiễu. Mỗi hình có tiêu đề “Bạn đang xem gì?” và legend.
7. **Giảm tải nhận thức:** chia sơ đồ thành lớp; luôn giữ một ví dụ xuyên chương; mở panel nâng cao khi người học đã hiểu đường cơ bản.
8. **Interleaving sau nền tảng:** trộn câu hỏi tương tự dễ nhầm (launch/async/withContext; composition/layout/draw; tween/spring) sau khi mỗi khái niệm đã được dạy riêng.
9. **Feynman-style explanation:** yêu cầu dạy lại bằng lời đơn giản rồi dùng thuật ngữ đúng. Xem đây là bài tự giải thích, không quảng bá như kỹ thuật thần kỳ độc lập.
10. **Transfer:** kết thúc mỗi phần bằng một bug chưa gặp y hệt; người học áp dụng nguyên lý lên triệu chứng mới.

## Khung micro-cycle

```text
Đoán → xem một bước → giải thích vì sao → kiểm tra bằng ví dụ khác → tự nhớ lại sau một khoảng nghỉ
```

Với một simulator: bắt đầu trạng thái nhỏ; chỉ hiện một bước/đường đi mỗi lần; cho phép pause/reset/back; đồng bộ code, sơ đồ và trạng thái. Cung cấp timeline toàn cảnh sau khi người học hiểu từng bước.

## Nguồn nghiên cứu

- Dunlosky et al. (2013), [Improving Students’ Learning With Effective Learning Techniques](https://journals.sagepub.com/stoken/rbtfl/Z10jaVH/60XQM/full) — review đánh giá practice testing và distributed practice có utility cao rộng rãi; self-explanation/elaborative interrogation/interleaving có hỗ trợ nhưng phụ thuộc điều kiện.
- Roediger & Karpicke (2006), [Test-Enhanced Learning](https://doi.org/10.1111/j.1467-9280.2006.01693.x) — retrieval/testing có thể cải thiện retention so với restudy trong các điều kiện nghiên cứu.
- Cepeda et al. (2006), [Distributed Practice in Verbal Recall Tasks: A Review and Quantitative Synthesis](https://pubmed.ncbi.nlm.nih.gov/16719566/) — meta-analysis về phân bổ thời gian giữa các lần học.
- Agarwal, Nunes & Blunt (2021), [Retrieval Practice Consistently Benefits Student Learning](https://doi.org/10.1146/annurev-psych-010419-051019) — review về bằng chứng retrieval trong môi trường giáo dục.
- Tài liệu về cognitive load/worked examples được chọn theo dạng bài; tránh tuyên bố “hình luôn tốt hơn chữ” hoặc “interleaving tốt cho mọi người/mọi lúc”.

## Ứng dụng cụ thể cho Android/Compose

- **Coroutines:** cho xem `suspend fun` trước, yêu cầu đoán call stack/thread; step tới `COROUTINE_SUSPENDED`; yêu cầu tự giải thích nơi giữ local state; tiếp đó thêm exception/cancellation.
- **Compose Runtime:** cho xem event/state trước; yêu cầu chỉ reader bị invalidated; step qua Composer/Applier; so sánh list có key và không key.
- **Animation:** yêu cầu dự đoán vị trí/vận tốc ở frame tiếp; so sánh target update giữa spring/tween; chọn state-read phase cho từng modifier.
- **Ôn cách quãng:** mỗi thẻ lưu câu hỏi ngắn + người học tự xếp “đúng / cần ôn sớm”; lịch có thể tăng/giảm theo câu trả lời và không lưu dữ liệu cá nhân nhạy cảm. Đây là đề xuất học tập; chưa triển khai website.
