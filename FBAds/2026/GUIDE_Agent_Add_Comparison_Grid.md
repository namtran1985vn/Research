# GUIDE cho Agent — Thêm Layout "Comparison Grid" (So sánh: Phổ thông ↔ Cao cấp bên mình)

**Yêu cầu user:** layout So Sánh dạng LƯỚI **2 cột × N hàng** (N = 1, 2, 3, 4) — **y hệt Before/After**, chỉ khác **nhãn cột**:
- **Cột trái = "Hàng phổ thông trên thị trường"**, **cột phải = "Hàng cao cấp bên mình"**.
- Mỗi HÀNG = một cặp so sánh (vd hàng 1 = ảnh macro đường họa tiết; hàng 2 = ảnh tổng thể sản phẩm…). Với gối thêu: cột trái có thể là 1 ảnh họa tiết **in phổ thông**; cột phải là **2 ảnh macro đường chỉ thêu nổi** + 1 ảnh tổng thể.
- User **tự thả ảnh thật** vào từng ô (như SampleGrid), pan canh khung.
- Nhãn 2 cột do app render (chữ Việt chuẩn) — chỉnh sửa được.

**Tin tốt:** giống Before/After, app ĐÃ có gần hết hạ tầng. `Creative` đã có `sampleRefs/sampleCols/sampleRows/sampleOffsets` (Models.swift ~dòng 272–322, đã Codable + CodingKeys ~dòng 390). `GridComposer.compose(images, size, gap, bg, cols, rows, offsets)` ghép ảnh vào canvas có pan từng ô. `SampleGridEditor` cho thả + pan. `AppStore.buildSampleGrid/reSample` dựng & dựng lại grid. **Comparison = grid cols=2, rows=N, + divider dọc + 2 nhãn cột.** KHÔNG xây từ đầu.

> ⚠️ **QUAN TRỌNG — đừng đẻ 2 cờ trùng nhau.** Before/After và Comparison **giống hệt nhau về cơ chế**, chỉ khác 2 chuỗi nhãn cột (+ tông nhãn mặc định). **Nếu áp cả guide này lẫn `GUIDE_Agent_Add_BeforeAfter_Grid.md`, hãy gộp thành MỘT enum `splitMode` duy nhất** thay vì 2 `Bool` (`isBeforeAfter` + `isComparison`). Đây là cách đúng, tránh nhân đôi code (khớp tinh thần "không bloat" của handoff). Guide dưới viết theo hướng enum gộp; nếu Before/After đã làm bằng `isBeforeAfter: Bool` rồi thì refactor nhẹ sang enum.

---

## TỔNG QUAN CÁCH LÀM
Tái dùng toàn bộ luồng SampleGrid, chỉ thêm:
1. Một "chế độ split" cho creative (cols khóa = 2, rows ∈ {1,2,3,4}) + **2 nhãn cột** (trái/phải).
2. `GridComposer` vẽ thêm **đường chia dọc giữa 2 cột** (+ tùy chọn divider ngang).
3. **2 nhãn cột** render bằng text layer (chữ Việt chuẩn) — với Comparison mặc định "Phổ thông trên thị trường" / "Cao cấp bên mình".
4. UI: nút chọn layout "So sánh (Comparison)" + số hàng (1–4) + sửa được 2 nhãn.

---

## BƯỚC 1 — Đánh dấu creative là "split grid" (Models.swift, struct `Creative`)
Thay vì thêm `Bool` riêng, dùng 1 enum gộp cho cả Before/After & Comparison:
```swift
enum SplitMode: String, Codable, Hashable {
    case none           // grid thường (mặc định)
    case beforeAfter    // nhãn "Trước" / "Sau"
    case comparison     // nhãn "Phổ thông trên thị trường" / "Cao cấp bên mình"
}

// trong struct Creative:
var splitMode: SplitMode = .none
var splitLeftLabel: String = ""   // override nhãn cột trái; rỗng = dùng mặc định theo splitMode
var splitRightLabel: String = ""  // override nhãn cột phải
```
- Khi `splitMode != .none`: ép `sampleCols = 2`, `sampleRows ∈ {1,2,3,4}`.
- Số ô = 2×rows; thứ tự thả khớp index hiện có `i = row*cols + col` (đã dùng trong GridComposer: `col = i % cols`, `row = i / cols`) → ô (hàng r, cột 0)=trái(Phổ thông), (hàng r, cột 1)=phải(Cao cấp).
- Nhãn mặc định khi override rỗng:
  - `.comparison` → trái `"Phổ thông trên thị trường"`, phải `"Cao cấp bên mình"`.
  - `.beforeAfter` → trái `"Trước"`, phải `"Sau"`.
- **CodingKeys (~dòng 390):** thêm `splitMode, splitLeftLabel, splitRightLabel`. Decode an toàn với default (`(try? c.decode(...)) ?? .none`) để **project cũ mở vẫn chạy**.

## BƯỚC 2 — `GridComposer`: thêm divider (Sources/TextOnImage/GridComposer.swift)
`compose(...)` đã vẽ từng cell theo cols/rows + pan offset. Thêm 1 tham số (mặc định false → không đụng caller cũ):
```swift
static func compose(_ images: [NSImage], size: CGSize = CGSize(width: 1024, height: 1280),
                    gap: CGFloat = 12, bg: NSColor = NSColor(srgbHex: 0xFBFAF7),
                    cols explicitCols: Int? = nil, rows explicitRows: Int? = nil,
                    offsets: [CGPoint]? = nil,
                    split: Bool = false,
                    dividerColor: NSColor = NSColor(srgbHex: 0xEFE7D8)) -> NSImage? {
```
Sau vòng lặp `for (i, img) in images.enumerated()` (ngay trước `ctx.makeImage()`), nếu `split`:
- **Đường chia DỌC** giữa 2 cột: fill 1 rectangle mảnh (≈ `max(2, size.width*0.004)` px) tại `x = size.width/2`, full chiều cao, màu `dividerColor` (neutral kem/charcoal mờ).
- (tùy chọn) **đường chia NGANG** giữa các hàng cho gọn.
- Khi split nên để `gap` nhỏ (vd 6–8) để 2 vế sát nhau, tương phản đọc nhanh.
> Nhãn KHÔNG vẽ ở đây — để app render bằng text layer (Bước 3) cho chữ Việt chuẩn + chỉnh được. (Giống hệt Before/After.)

## BƯỚC 3 — 2 nhãn cột bằng text layer (cơ chế text-on-image sẵn có, dùng `TextRenderer`)
Khi tạo/đổi creative sang split, seed sẵn **2 TextLayer**:
- Layer trái — căn **trên-trái** (đỉnh cột Phổ thông); nội dung = `splitLeftLabel` (hoặc mặc định).
- Layer phải — căn **trên-phải** (đỉnh cột Cao cấp); nội dung = `splitRightLabel` (hoặc mặc định).
- Dùng đúng `TextRenderer` + hookStyle hiện có. **Tệp A (quiet-luxury): style nhẹ** (editorial/cleanFloat, kem/charcoal, **không box dày**). Tệp B: có thể đậm hơn.
- User chỉnh được vị trí/cỡ/nội dung như mọi text layer khác → đổi nhãn tự do.
> Khi `splitLeftLabel/RightLabel` đổi, cập nhật text 2 layer này (hoặc đơn giản: text layer là nguồn sự thật, 2 field chỉ là default seed).

## BƯỚC 4 — UI: chọn layout + số hàng + sửa nhãn (Sources/Views/Results/SampleGridEditor.swift + InspectorView.swift)
SampleGridEditor đã cho thả ảnh + đổi cols/rows. Thêm:
- **Picker "Kiểu lưới"**: Thường / Before-After / **So sánh (Comparison)** → set `splitMode`, khi ≠ none thì khóa `sampleCols = 2`.
- **Stepper số hàng (rows)**: 1–4 → set `sampleRows`. (Nhãn UI: "Số hàng so sánh".)
- **2 ô nhập nhãn cột** (hiện khi splitMode ≠ none): "Nhãn cột trái" / "Nhãn cột phải", placeholder = mặc định theo mode.
- **Nhãn ô khi thả:** ô cột 0 hiện mờ nhãn trái, cột 1 hiện mờ nhãn phải → user thả đúng chỗ.
- Giữ pan offset mỗi ô (đã có) — để canh 2 ảnh cùng khung/cùng góc.

## BƯỚC 5 — Dựng/Export (Sources/Store/AppStore.swift: `buildSampleGrid` / `reSample`)
- `buildSampleGrid` đang gọi `GridComposer.compose(pickedImgs, size: rs, cols: cols, rows: rows, offsets: offsets)`. Khi creative `splitMode != .none`, truyền thêm `split: true`.
- `reSample` / `reSampleCell` giữ nguyên (cols/rows lấy từ creative).
- Export giữ high-fidelity như sample grid hiện tại (`GridComposer.highResSize`) — cells không mờ.
- Persist: `splitMode` + `splitLeftLabel/RightLabel` + `sampleRows` lưu trong Project JSON (Creative đã Codable) → mở lại không mất.

---

## LƯU Ý THẬT / CHẤT LƯỢNG (theo research RD003 §6 + handoff)
- **Đây là format bán MECHANISM** — hợp ngành thêu/dệt stage 4-5 (claim "đẹp/mềm" đã chết). So sánh = cho thấy craft, không nói suông.
- **Ảnh macro PHẢI là ảnh THẬT giữ đúng họa tiết** (handoff §3). Tuyệt đối **không để AI vẽ lại đường thêu** — sai mũi chỉ là lộ giả ngay với khách hàng thật, phá luôn lập luận "thủ công tinh xảo".
- **Khung cho khách giàu (cực quan trọng):** so sánh **theo LOẠI** (in công nghiệp ↔ thêu thủ công), giọng "con mắt người sành" / giáo dục — **KHÔNG bôi nhọ đối thủ cụ thể**, không "hàng chợ rẻ tiền!!!". Chê lộ liễu = tín hiệu middle-class, đuổi tệp A (handoff §2). Cấm urgency / dấu chấm than.
- **Highlight đúng 1 từ** ở hook nếu thêm (vd "**Thêu nổi** — sờ thấy được").
- Ô tổng thể nên có **human element** (tay chạm/đặt trên sofa) → kích reward (handoff §3).
- Cùng GÓC máy / cùng ÁNH SÁNG giữa 2 cột để so sánh công bằng, thuyết phục. UI nên có 1 dòng nhắc: "Chụp 2 vế cùng góc, cùng ánh sáng."
- Đây là loại creative **ảnh tự chụp đè bẹp AI** (rd002). Khuyến khích user chụp điện thoại + macro.
- **Funnel:** mạnh nhất ở MOF/BOF (giải objection "sao đắt hơn hàng ngoài"), cũng dùng được TOF (macro đẹp + phá niềm tin "thêu nào chẳng như nhau"). Khi đã thêm trục `funnelStage`/`awarenessStage`, gán Comparison mặc định MOF/BOF.

## KIỂM THỬ
1. Build xanh; project cũ (không có splitMode) mở vẫn chạy (decode default `.none`).
2. Tạo creative → Kiểu lưới = "So sánh", số hàng = 2 → lưới 2×2, mỗi ô hiện nhãn mờ đúng cột (trái Phổ thông / phải Cao cấp).
3. Thả 4 ảnh, pan canh → có đường chia dọc giữa 2 cột; 2 nhãn cột render đúng chữ Việt ("Phổ thông trên thị trường" / "Cao cấp bên mình").
4. Sửa nhãn cột (vd "In công nghiệp" / "Thêu thủ công") → cập nhật đúng.
5. Đổi số hàng 1/2/3/4 → lưới cập nhật đúng; đổi splitMode về Thường → mở khóa cols.
6. Export → ảnh 1024×1280, cells nét, divider + nhãn đúng; mở lại project giữ nguyên splitMode + nhãn.

## TÓM TẮT
| Bước | File | Việc |
|--|--|--|
| 1 | Sources/Models/Models.swift | +enum `SplitMode` + `splitMode/splitLeftLabel/splitRightLabel`; cols khóa 2, rows 1–4; CodingKeys + decode default |
| 2 | Sources/TextOnImage/GridComposer.swift | +tham số `split` → vẽ divider dọc (±ngang), gap nhỏ |
| 3 | (seed text layers) | 2 nhãn cột qua `TextRenderer` (mặc định Phổ thông/Cao cấp) |
| 4 | Sources/Views/Results/SampleGridEditor.swift + InspectorView.swift | Picker kiểu lưới + stepper số hàng + 2 ô nhập nhãn + nhãn ô |
| 5 | Sources/Store/AppStore.swift (buildSampleGrid/reSample) | truyền `split: true`, persist splitMode + nhãn + rows |

Tái dùng tối đa hạ tầng SampleGrid → ít code mới, ít rủi ro. **Comparison & Before/After dùng CHUNG 1 cơ chế `splitMode`, chỉ khác 2 nhãn cột.** Cột trái = Phổ thông thị trường, phải = Cao cấp bên mình; N hàng = N cặp so sánh.
