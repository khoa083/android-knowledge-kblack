# Animation · chuỗi cho hình trực quan (tracks/animation/views/visuals.js). Không có khẳng định mới.


def add(a):
    a('vz.tab.tree', 'Cây quyết định', 'Decision tree')
    a('vz.tree.cap', 'Đường đi của nhu cầu đang chọn trên trang "Choose an animation API": mỗi hàng là một câu hỏi, câu trả lời đã chọn, và nhánh còn lại dẫn tới đâu. Câu hỏi hiện dần theo từng bước; hàng cuối là API.',
      'The path of the selected need through the "Choose an animation API" page: each row is a question, the answer chosen, and where the other branch leads. Questions appear step by step; the last row is the API.')
    a('vz.tree.tcap', 'Bảng tra sáu nhu cầu mẫu: API ở cuối đường đi, chương dạy API đó, và số câu hỏi phải trả lời.', 'Lookup for the six sample needs: the API at the end of the path, the chapter teaching it, and how many questions it takes.')
    a('vz.tree.else', 'nếu {ans} → {api}', 'if {ans} → {api}')
    a('vz.tree.elseQ', 'nếu {ans} → sang câu hỏi khác', 'if {ans} → a different question')
    a('vz.tree.thinking', 'đang xét…', 'deciding…')
    for k, vi, en in [('need', 'Nhu cầu', 'Need'), ('api', 'API', 'API to use'), ('ch', 'Chương', 'Chapter'), ('qs', 'Số câu hỏi', 'Questions')]:
        a('vz.tree.col.' + k, vi, en)
    a('vz.tree.yes', 'Có', 'Yes')
    a('vz.tree.no', 'Không', 'No')
    a('vz.tree.chapter', 'chương {ch}', 'chapter {ch}')
