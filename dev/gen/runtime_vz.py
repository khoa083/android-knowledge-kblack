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
    a('vz.tab.records', 'Dãy bản ghi', 'Record list')
    a('vz.records.cap', 'Một state object giữ một danh sách bản ghi, mỗi bản ghi gắn id snapshot đã ghi nó. Hàng đầu là các bản ghi đang có; các hàng dưới là giá trị mà Global, snapshot A và snapshot B đọc thấy. Hàng có viền vừa đổi ở bước này.',
      'A state object holds a list of records, each tagged with the id of the snapshot that wrote it. The top row lists the current records; the rows below are the values Global, snapshot A and snapshot B read. An outlined row just changed at this step.')
    a('vz.tab.lazy', 'Cửa sổ danh sách', 'List window')
    a('vz.lazy.cap', 'Mỗi ô là một item theo chỉ số trong danh sách. Chỉ những item trong cửa sổ hiển thị mới được compose; item cuộn ra khỏi màn hình có thể vào pool để slot của nó được dùng lại cho item mới.',
      'Each chip is a list item by index. Only items inside the visible window are composed; an item scrolled off screen may go into the pool so its slot can be reused for a new item.')
    a('vz.lazy.op', 'Vừa làm', 'Just did')
    a('vz.lazy.legend', 'Ô viền: đang hiển thị (đã compose). ↺: nằm trong pool chờ dùng lại. Ô mờ: chưa compose, hoặc slot của nó đã được dùng lại cho mục mới hay bị bỏ.', 'Outlined: visible (composed). ↺: in the pool, waiting for reuse. Faded: not composed, or its slot was already reused for a new item or dropped.')
