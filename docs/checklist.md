# Checklist chung (CONSTRAINTS-CHECKLIST §0–4, §10, §11) — vị trí và trạng thái

Cập nhật sau P8 (2026-11-21). Phạm vi đã kiểm: lõi + cả 5 track (A–E) + trang chung. Bảng bên dưới viết ở P3; các mục "P7" nay đã xong (xem cuối file). Mục riêng của track: `docs/research/coroutines.md`, `docs/research/runtime.md`.
Trạng thái: **đạt** (đã thấy và kiểm ở cả vi và en) · **một phần** · **P7/P8** (thuộc phase sau).

## §0 Kỹ thuật & sản phẩm
| Ràng buộc | Trạng thái | Ở đâu / cách kiểm |
|---|---|---|
| Thư mục đích dùng nguyên, không ghi đè | đạt | `docs/progress.md` (P0) |
| Chỉ ghi trong thư mục đích | đạt | Không file nào ngoài `E:\AndroidDeepDiveExplorer` (trừ ảnh kiểm trong scratchpad của phiên) |
| Chạy qua `file://`, không CDN/webfont | đạt | Mọi kiểm bằng `dev/tools/cdp.js` mở `file:///…/index.html`; gate tĩnh P1 |
| Không module/import/export | đạt | grep `type="module"|^import|^export` trong `app.js`, `js/`, `tracks/` = 0 |
| Không fetch/XHR | đạt | grep `fetch(|XMLHttpRequest` = 0 |
| Không framework/build step | đạt | `dev/gen/*.py` chỉ là công cụ phát triển sinh file `.js` tĩnh; site không cần nó |
| Có `README.md`, `sources.md` | P7 | Chưa có (P7 viết) |
| Model thuần, chỉ message key | đạt | `tracks/*/models/*.js`; report kiểm mọi khoá model phát ra có ở vi và en |
| Không lỗi console, không placeholder | đạt (A, B) | cdp.js trên 51 route: 0 lỗi console; track-check không thấy khoá lộ ra màn hình |
| Mọi nút tác động lên mô hình | đạt (A, B) | `dev/tools/controls-sweep.js`: không điều khiển chết ở mọi tổ hợp (ở các tổ hợp mà một điều khiển không áp dụng, model hiện ghi chú lý do) |
| `localStorage` bọc try/catch | đạt | `ADE.store` (P1) |
| Route có ngôn ngữ và bước; Back/Forward | đạt | `js/core/router.js`; track-check đổi ngôn ngữ giữ route |

## §1 Song ngữ
| Ràng buộc | Trạng thái | Ở đâu |
|---|---|---|
| Mọi chuỗi có vi và en | đạt (A, B); P7 cho README/sources.md | report: 0 khoá thiếu |
| Cùng cây key | đạt | report; track B sinh từ một nguồn `dev/gen/runtime_content.py` |
| Hai bản tương đương | đạt | viết song song từng cặp; report kiểm markup `[[src]]/[[term]]/[[badge]]` khớp |
| Đổi ngôn ngữ giữ route + trạng thái | đạt | track-check (mọi chương A, B) |
| Thuật ngữ en bọc `lang="en"`; mã `translate="no"` | đạt | `js/core/i18n.js` (term, code) |
| Giải thích thuật ngữ lần đầu | đạt | `[[term:…]]` link tới glossary |
| Số/đơn vị theo Intl | đạt | lõi P1 |
| Uppercase chỉ header ngắn, dấu không cắt | đạt (Windows/Chrome) | ảnh chụp các chương; Android font chưa kiểm |
| Rà câu tuyệt đối hai ngôn ngữ | đạt (A, B) | progress P2, P3 |

## §2 Registry
| Ràng buộc | Trạng thái | Ở đâu |
|---|---|---|
| Track tự đăng ký | đạt | `tracks/coroutines/manifest.js`, `tracks/runtime/manifest.js` |
| Lõi không rẽ nhánh theo id | đạt | grep `trackId ===|case '` trong `js/core`, `app.js` = 0; không sửa `js/core` ở P2/P3 |
| Namespace key | đạt | `track.coroutines.*`, `track.runtime.*` |
| Tài nguyên chung ở `shared/` | đạt | bridges, glossary chung |
| Catalog/nav/search… từ registry | đạt | track B tự xuất hiện, không sửa lõi |
| Domain mới tự thành nhóm | đạt | P1 (hello) |
| Track hello thử rồi gỡ | P7 | còn `tracks/hello` |
| README thêm track/ngôn ngữ | P7 | |

## §3 UX, truy cập
| Ràng buộc | Trạng thái | Ở đâu |
|---|---|---|
| Không sao chép trang mẫu | đạt | sơ đồ, icon, câu chữ, ví dụ (counter, MovieOverview, A/B/C) tự viết |
| Mức "gần mẫu hơn" | đạt | lõi P1 |
| Không credit tác giả mẫu | đạt | chỉ ở trang Nguồn (inspo-*) |
| Pattern P1–P14 | đạt | lõi P1 |
| Light/dark, tương phản | một phần | token đo ở P0; màu node mới không thêm token |
| Giảm chuyển động tắt zoom/gõ | đạt | lõi; cdp `--reduce` → class `reduced-motion`; scene có class `still` (không token, không thanh `grow`, không nhịp) |
| Zoom vào node đang xử lý (gần mẫu) | đạt | `iso`: zoom vào node; dạng phẳng: đẩy camera vào nhẹ (thẻ đích + hàng xóm + chú thích, giữ ≥ 68% toàn cảnh, không cắt); lanes: vạch "bây giờ" + thanh vừa đổi |
| Hình và animation khác nhau theo bản chất khái niệm | đạt | `view.layout` iso/tree/pipeline/cycle/lanes, chú giải hình dạng, "Bạn đang xem", chú thích "trước → sau" trên hình (`docs/core-api.md` §4.1) |
| Không truyền tin chỉ bằng màu | đạt | trạng thái node có chữ `[…]`, log có icon + nhãn |
| 360px không cuộn ngang | đạt | routes-check 51 route; sửa `.field` ở P2 |
| Bàn phím, focus | đạt | focus-check; track-check "focus fell to BODY" = 0 |
| Điều khiển Reset/Trước/Tiếp/Phát/Tốc độ | đạt (A, B); Animation ở P4 | |
| SVG role/title/desc, aria-live | đạt | `js/core/diagram.js` |

## §4 Nội dung chung
| Ràng buộc | Trạng thái | Ở đâu |
|---|---|---|
| Cơ chế và nhân quả | đạt | mỗi bước có "vì sao" |
| Khuôn chương 7.2 | đạt (A, B) | essence, sim, sec có nguồn + badge, simp, quiz, cầu nối |
| Mô phỏng engineering hiện đủ 6 thứ | đạt (B, sau bổ sung P3); A: đa số model | stateBefore/After, affected, changes, skipped, simplificationKeys |
| Cầu nối viết một lần ở chủ sở hữu | đạt: X1 (B7), X2 (A8), X3 (B5); còn X4–X8 | |
| Tự kiểm tra tự soạn | đạt | |

## §10 Độ chính xác implementation
| Ràng buộc | Trạng thái | Ở đâu |
|---|---|---|
| Tách bảo đảm/nội bộ | đạt | badge `impl`, `android-impl` |
| Class nội bộ ghi phiên bản/commit | một phần | how-compose-works: nhánh androidx-main + ngày đọc; không có commit hash (trang không hiện) |
| Sơ đồ là mô hình giảng dạy | đạt | badge "mô phỏng khái niệm", `simp.*` |
| Không hard-code thread/frame/số recomposition | đạt | `simp.threads`, B5 không có số ms |
| Chi tiết không bảo đảm có nhãn hoặc loại | đạt | `$changed` chỉ nhắc tên |
| Không bịa | đạt | research ghi nguồn từng khẳng định |

## §11 Nguồn
| Ràng buộc | Trạng thái | Ở đâu |
|---|---|---|
| Link nguồn sát nội dung, hai ngôn ngữ | đạt | `[[src:…]]` trong đoạn văn |
| `sources.md` song ngữ | P7 | |
| Mọi URL bắt buộc có mặt; không URL 404 | đạt cho A, B | `tracks/*/sources.js`; report kiểm URL đã thay |
| Chính thức thắng thứ cấp | đạt | Grokking không dùng |
| Sách chỉ là nguồn phụ, không đường dẫn file | đạt | không có đường dẫn `E:\AndroidBooks` trên site |

## Cập nhật P7–P8 (2026-11-21)
| Mục | Trạng thái | Ở đâu |
|---|---|---|
| `README.md`, `sources.md` | đạt | thư mục gốc; `sources.md` sinh bằng `node dev/tools/sources-md.js` |
| Track hello thử ở P1, gỡ ở P7 | đạt | khối script, thư mục và `domain.sandbox` đã gỡ |
| Cầu nối X1–X8 viết một lần ở chủ sở hữu, link hai chiều | đạt | script kiểm hai chiều trong progress P7 |
| Mọi chuỗi có vi + en (cả D, E, mock app) | đạt | report 0 lỗi |
| Chữ hoa chỉ cho tiêu đề ≤ 40 ký tự | đạt | quét mọi route: 0 phần tử viết hoa > 40 ký tự (sau sửa `app.js` trang Nguồn và tiêu đề lab D1) |
| Gate tĩnh P8 (module, fetch, XHR, import/export, http, webfont, TODO, nhánh theo track) | đạt | progress P8 |
| Mô phỏng D/E: không số liệu thiếu nguồn; đo cá nhân không lưu/gửi | đạt | `docs/research/ux.md`, `docs/research/ui.md` (checklist mục 8, 9) |
| Firefox, Safari | **chưa xác minh** | không có trên máy |
| Font Android (Roboto/Noto) cho tiêu đề viết hoa có dấu | **chưa xác minh** | chỉ kiểm Windows (Chrome, Edge) |
| Đối chiếu `originals/01–06` | **không áp dụng được** | thư mục `originals/` không có trong `E:\AndroidDeepDiveExplorer-Prompts`; đã đối chiếu với `tracks/A–E-*.md` (được ghi là tổng hợp từ originals) |
