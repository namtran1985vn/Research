# GUIDE cho Agent — Thêm Layout "Before/After Grid" (Cách B: ảnh thật user thả vào)

**Yêu cầu user:** layout Before/After dạng LƯỚI **2 cột × N hàng** (N = 2, 3, 4).
- **Cột trái = Before, cột phải = After.**
- **Mỗi HÀNG = một cặp Before/After khác nhau** (2 hàng = 2 cặp, 3 hàng = 3 cặp, 4 hàng = 4 cặp).
- User **tự thả ảnh thật** vào từng ô (giống SampleGrid hiện có), pan canh khung.
- Nhãn "Trước / Sau" do app render (chữ Việt chuẩn).

**Tin tốt:** app ĐÃ có gần hết hạ tầng — `GridComposer.compose()` ghép nhiều ảnh vào canvas với cols/rows/gap/bo-góc/pan-offset; `Creative` đã có `sampleRefs/sampleCols/sampleRows/sampleOffsets`; `SampleGridEditor` đã cho thả + pan từng ô. Before/After Grid = **một grid cols cố định = 2, rows = N, + divider + 2 nhãn cột**. KHÔNG xây từ đầu.

---

## TỔNG QUAN CÁCH LÀM
Tái dùng toàn bộ luồng SampleGrid, chỉ thêm:
1. Một "chế độ" beforeAfter cho creative (cols khóa = 2, rows ∈ {2,3,4}).
2. `GridComposer` vẽ thêm **đường chia dọc giữa 2 cột** + (tùy chọn) divider ngang giữa các hàng.
3. **2 nhãn cột "Trước"/"Sau"** (render 1 lần trên đỉnh, hoặc mỗi hàng) bằng text layer.
4. UI: nút chọn layout "Before/After" + chọn số hàng (2/3/4).

---

## BƯỚC 1 — Đánh dấu creative là "Before/After" (Models.swift, struct `Creative`)
Thêm 1 cờ + (đã có sẵn `sampleCols/sampleRows`):
```swift
var isBeforeAfter: Bool = false   // true → sample grid renders as 2-col Before|After with divider + labels
```
Khi bật: ép `sampleCols = 2`, `sampleRows ∈ {2,3,4}`. Số ô = 2×rows; thứ tự thả: ô (hàng r, cột 0)=Before, (hàng r, cột 1)=After — khớp index `i = row*cols + col` mà GridComposer đang dùng.

## BƯỚC 2 — `GridComposer`: thêm divider + nhãn (TextOnImage/GridComposer.swift)
Hàm `compose(...)` đã vẽ từng cell theo cols/rows. Thêm tham số:
```swift
static func compose(..., beforeAfter: Bool = false,
                    dividerColor: NSColor = NSColor(srgbHex: 0xF4EDE0)) -> NSImage? {
```
Sau vòng lặp vẽ cell, nếu `beforeAfter`:
- **Đường chia DỌC** giữa 2 cột: vẽ 1 rectangle mảnh (vd width 3–6px ở scale 1×, scale theo canvas) tại x = giữa canvas, full chiều cao — màu neutral (kem/charcoal mờ).
- (tùy chọn) **đường chia NGANG** mảnh giữa các hàng cho gọn.
- Giữ nguyên gap/bo-góc cũ (before/after nên gap nhỏ hoặc 0 để 2 vế sát nhau, tương phản rõ — cho `gap` nhỏ khi beforeAfter).
> Nhãn "Trước/Sau" KHÔNG vẽ ở đây — để app render bằng text layer (Bước 3) cho chữ Việt chuẩn + chỉnh được.

## BƯỚC 3 — Nhãn "Trước / Sau" bằng text layer (cơ chế text-on-image sẵn có)
Khi tạo creative beforeAfter, seed sẵn **2 TextLayer**:
- Layer "Trước" — căn trên-trái (trên đỉnh cột trái).
- Layer "Sau" — căn trên-phải (trên đỉnh cột phải).
- Dùng đúng `TextRenderer` + hookStyle hiện có (gợi ý style nhẹ: editorial/cleanFloat — nhãn nhỏ, không che ảnh).
- User chỉnh được vị trí/cỡ như mọi text layer khác.
> Lý do: tái dùng pipeline chữ Việt sạch, không đụng GridComposer cho text.

## BƯỚC 4 — UI: chọn layout + số hàng (Views/Results/SampleGridEditor.swift + Inspector)
SampleGridEditor đã cho thả ảnh vào lưới + đổi cols/rows. Thêm:
- **Toggle/Picker "Before/After"** → set `isBeforeAfter = true`, khóa `sampleCols = 2`.
- **Stepper số cặp (rows)**: 2 / 3 / 4 → set `sampleRows`. (UI gợi ý nhãn "Số cặp Trước/Sau".)
- **Nhãn ô khi thả:** hiển thị mờ "Trước"/"Sau" trên mỗi ô trống để user biết thả đúng chỗ (ô cột 0 = Trước, cột 1 = Sau).
- Giữ pan offset mỗi ô (đã có) — quan trọng để user canh cho 2 ảnh cùng góc khớp khung.

## BƯỚC 5 — Lưu/Export (AppStore `buildSampleGrid` / `reSample`)
- `buildSampleGrid` đang gọi `GridComposer.compose(... cols, rows, offsets ...)`. Khi creative `isBeforeAfter`, truyền thêm `beforeAfter: true`.
- Export giữ high-fidelity như sample grid hiện tại (`highFidelitySize`) — cells không bị mờ.
- Persist: `isBeforeAfter` + `sampleRows` lưu trong Project JSON (Creative đã Codable) → mở lại không mất.

---

## LƯU Ý THẬT / CHẤT LƯỢNG (theo research)
- Before/After winner = **cùng GÓC máy, cùng ÁNH SÁNG, chỉ khác có/không sản phẩm**. → UI nên có 1 dòng nhắc user: "Chụp 2 ảnh cùng góc, cùng ánh sáng; ô Trước = phòng chưa có sản phẩm, ô Sau = đã có."
- Đây là loại creative **ảnh tự chụp đánh bại AI** (rd002: authentic > glossy). Khuyến khích user chụp điện thoại.
- Gap nhỏ + divider mảnh → tương phản trước/sau đọc nhanh (thumb-stop). Tránh viền dày loè loẹt.
- Nhãn "Trước/Sau" giữ nhỏ, tinh tế (Tệp A) — đừng để thành banner to.

## KIỂM THỬ
1. Build xanh.
2. Tạo creative → chọn "Before/After", số cặp = 3 → lưới 2×3, mỗi ô hiện nhãn mờ Trước/Sau đúng cột.
3. Thả 6 ảnh (3 cặp), pan canh → có đường chia dọc giữa 2 cột, nhãn "Trước/Sau" render đúng (chữ Việt chuẩn).
4. Đổi số cặp 2/3/4 → lưới cập nhật đúng.
5. Export → ảnh 1024×1280, cells nét, divider + nhãn đúng; mở lại project giữ nguyên.

## TÓM TẮT
| Bước | File | Việc |
|--|--|--|
| 1 | Models.swift | +`isBeforeAfter` (cols khóa 2, rows 2/3/4) |
| 2 | GridComposer.swift | +tham số `beforeAfter` → vẽ divider dọc (±ngang) |
| 3 | (seed text layers) | 2 nhãn "Trước/Sau" qua TextRenderer sẵn có |
| 4 | SampleGridEditor + Inspector | toggle Before/After + stepper số cặp + nhãn ô |
| 5 | AppStore buildSampleGrid/reSample | truyền `beforeAfter: true`, persist cờ + rows |

Tái dùng tối đa hạ tầng SampleGrid → ít code mới, ít rủi ro. Cột trái=Trước, phải=Sau, N hàng = N cặp.
