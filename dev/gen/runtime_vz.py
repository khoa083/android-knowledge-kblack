# Runtime · chuỗi cho hình trực quan (tracks/runtime/views/visuals.js). Không có khẳng định mới.


def add(a):
    a('vz.tab.slots', 'Dãy group', 'Group sequence')
    a('vz.slots.cap', 'Mỗi ô là một group theo đúng thứ tự trong SlotTable. So hàng "cũ" với hàng "lần chạy mới gọi" từ trái sang phải để thấy chỗ khớp, chỗ lệch; hàng có viền vừa đổi ở bước này.',
      'Each chip is one group in SlotTable order. Compare the "old" row with the "new run calls" row left to right to see where they match and where they diverge; an outlined row just changed at this step.')
    a('vz.tab.chain', 'Đối chiếu chuỗi', 'Chain diff')
    a('vz.chain.cap', 'Mỗi hàng là một vị trí trong chuỗi modifier: phần tử cũ, phần tử mới, và việc Compose làm với node ở vị trí đó. Cột hành động hiện dần theo số đo của bước; ô viền là việc vừa làm.',
      'Each row is a position in the modifier chain: the old element, the new element, and what Compose does with the node there. The action column fills in with the metrics of each step; the outlined cell is the latest action.')
    for k, vi, en in [('colOld', 'Chuỗi cũ', 'Old chain'), ('colNew', 'Chuỗi mới', 'New chain'), ('colAct', 'Node được', 'The node is'),
                      ('reuse', 'giữ nguyên', 'reused'), ('update', 'cập nhật (update)', 'updated in place'), ('insert', 'tạo mới (onAttach)', 'created (onAttach)'), ('remove', 'gỡ (onDetach)', 'removed (onDetach)')]:
        a('vz.chain.' + k, vi, en)
