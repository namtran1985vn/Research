# GUIDE cho Agent — Thêm Layout "Variant Grid" (lưới biến thể cùng SKU + nút **Vary**)

**Ý tưởng:** lưới khoe **nhiều họa tiết của CÙNG một loại sản phẩm** (vd cùng mẫu chăn, khác họa tiết). Sức mạnh = **kiểm soát biến**: mọi ô **giống hệt bố cục/góc/ánh sáng**, chỉ khác đúng 1 thứ — **họa tiết**. Mắt khách khóa thẳng vào họa tiết → so sánh trực tiếp được, "có nhiều lựa chọn đẹp" hiện ra tức thì.

**Khác 2 grid kia:**
| Layout | Cách tạo mỗi ô |
|--|--|
| Before/After Grid | User thả **ảnh thật rời** (2 cảnh khác) |
| Comparison Grid | User thả ảnh **nhiều sản phẩm khác** (so phổ thông ↔ cao cấp) |
| **Variant Grid (đây)** | App **tự random** vài họa tiết từ input của user → nút **Vary** bắt AI **đồng bộ bố cục mọi ô về ô #1**, **mỗi ô GIỮ NGUYÊN họa tiết của chính nó** |

---

## SPEC (chốt theo yêu cầu user)
1. **Bố cục lưới ngẫu nhiên** trong tập: **1×3, 3×1, 2×2, 3×2** (dòng × cột). App tự chọn 1 kiểu.
2. App **tự random các mẫu** (họa tiết) từ **input ảnh có sẵn của user** → mỗi ô 1 họa tiết.
3. Nút **"Vary"**: nhấn → AI **vẽ lại các gridcell sao cho GIỐNG bố cục & góc chụp của gridcell ĐẦU TIÊN**, **nhưng họa tiết ở ô nào thì giữ nguyên họa tiết của ô đó**. Sau Vary: mọi ô = cùng phòng/giường/góc/sáng của ô #1, chỉ khác họa tiết.

---

## HẠ TẦNG ĐÃ CÓ (đã verify trong code)
- `Creative` (Models.swift ~272): `sampleRefs/sampleCols/sampleRows/sampleOffsets`, Codable.
- `GridComposer.compose(images, size, gap, bg, cols, rows, offsets)` — ghép ảnh vào lưới.
- `AppStore.buildSampleGrid` (random-pick ảnh + compose), `reSample`, `reSampleCell`.
- **`ImageProvider.generate(prompt:, references:[Data], target:)`** — nhận **tối đa 4 ảnh tham chiếu** (Nano Banana đã ghép multi-ref). ⭐ Đây là thứ nút Vary cần.
- `ImageFidelity.suffix` đã ép "reproduce surface patterns/textures exactly… only scene/lighting/composition may change" — **gần đúng** cơ chế Vary (xem cảnh báo Bước 4).

→ Variant Grid = random layout (đã gần có) + **pin họa tiết theo ô** + **1 vòng lặp gọi `generate` để đồng bộ bố cục**. KHÔNG engine mới.

---

## BƯỚC 1 — Model (Models.swift, struct `Creative`)
Gộp chung với enum kiểu lưới (nếu đã làm `SplitMode` cho Before/After + Comparison thì mở rộng thành `GridKind`):
```swift
enum GridKind: String, Codable, Hashable {
    case standard, beforeAfter, comparison, variant
}
var gridKind: GridKind = .standard

// Variant-only:
var variantPatternRefs: [String] = []   // họa tiết GỐC (ảnh thật) PIN theo từng ô — KHÔNG đổi khi Vary
```
> **Không lưu ô gốc.** Gốc bố cục được chọn **ngay lúc Vary** qua right-click ô (truyền `anchorIndex` vào action), không phải state cố định.
- `sampleRefs[i]` = ảnh **đang hiển thị** ở ô i (trước Vary = ảnh gốc; sau Vary với i≠anchor = ảnh AI sinh).
- `variantPatternRefs[i]` = **ảnh họa tiết thật gốc** của ô i — nguồn để giữ họa tiết + để **Vary lại nhiều lần vẫn idempotent** (luôn lấy từ gốc, không tam sao).
- CodingKeys (~390): thêm `gridKind, variantPatternRefs`; decode default an toàn (project cũ → `.standard`).

## BƯỚC 2 — Tạo Variant Grid: random layout + random họa tiết (AppStore)
Thêm hàm (mẫu theo `buildSampleGrid`):
```swift
static let variantLayouts: [(rows: Int, cols: Int)] = [(1,3),(3,1),(2,2),(3,2)]

func makeVariantGrid(pid: UUID, cid: UUID) {
    let (rows, cols) = Self.variantLayouts.randomElement()!   // random bố cục
    let cellCount = rows * cols
    let picks = userInputImages.shuffled().prefix(cellCount)  // random họa tiết từ input user
    // set: gridKind = .variant; sampleRows = rows; sampleCols = cols
    //      sampleRefs = picks; variantPatternRefs = picks (pin gốc)
    buildSampleGrid(... cols: cols, rows: rows ...)            // compose như cũ
}
```
Lưu ý: nếu input user ít hơn cellCount → giảm số ô hoặc cho lặp; UI báo "cần ≥ N ảnh họa tiết".

## BƯỚC 3 — **Right-click ô → menu "Vary"** (UI: SampleGridEditor / ResultsView) → action AppStore
**KHÔNG có ô gốc cố định, KHÔNG có nút Vary toàn cục.** Tương tác: user **right-click lên ô bất kỳ** → context menu hiện mục **"Vary"** → **chính ô đó thành gốc bố cục**, mọi ô khác vẽ lại theo bố cục/góc của ô đó. Trạng thái loading per-ô (tái dùng GenerationEngine/concurrency cap + retry đã có).

```swift
// UI: .contextMenu trên mỗi cell (khi gridKind == .variant)
//   Button("Vary") { store.varyVariantGrid(pid, cid, anchorIndex: thisCellIndex) }

func varyVariantGrid(pid: UUID, cid: UUID, anchorIndex: Int) async {  // anchor = ô vừa right-click
    let anchorImg = loadPNG(sampleRefs[anchorIndex])          // bố cục chuẩn = ô user chọn
    await withConcurrency(cap) {
      for i in cellIndices where i != anchorIndex {
        let patternImg = loadPNG(variantPatternRefs[i])       // họa tiết THẬT của ô i (gốc)
        let data = try await imageProvider.generate(
            prompt: Self.variantVaryPrompt,                   // xem Bước 4
            references: [anchorImg, patternImg],              // ref#1 = bố cục, ref#2 = họa tiết
            target: cellTargetSize)
        let name = imageStore.save(ImageCrop.normalizeToTarget(data))
        sampleRefs[i] = name                                  // chỉ đổi ảnh hiển thị; variantPatternRefs GIỮ NGUYÊN
      }
    }
    buildSampleGrid(... reuse sampleRefs, cols, rows, offsets ...)  // ghép lại lưới
}
```
- **Ô được right-click = gốc, KHÔNG đụng** → ô đó luôn giữ ảnh gốc thật (neo độ tin cậy). Right-click ô khác = đổi gốc, vary lại theo ô mới.
- `variantPatternRefs` không bao giờ ghi đè → Vary lại nhiều lần (kể cả đổi gốc) đều lấy đúng họa tiết gốc, không tam sao tích lũy.
- (tùy chọn) thêm mục **"Vary lại ô này"** trong cùng context menu để sinh lại RIÊNG ô đó theo gốc gần nhất — sửa ô hỏng.

## BƯỚC 4 — PROMPT cho Vary (mấu chốt chất lượng)
2 ref có VAI TRÒ khác nhau: **ref#1 = cảnh để sao chép, ref#2 = họa tiết để áp.** Prompt phải nói rõ:
```
Recreate the EXACT same scene as reference image 1: identical room, furniture/bed,
camera angle, framing, distance, depth of field and lighting. Place the SAME product
type in the SAME position, size and drape as in image 1.
Change ONLY the textile's pattern/motif: apply the pattern shown in reference image 2.
Reproduce that pattern faithfully and EXACTLY as a real product pattern — same motif,
colors, scale and weave/stitch — following the fabric's folds, perspective and shadows
from image 1. Do NOT invent, redraw, simplify or restyle the motif.
4:5, reserve calm negative space for text, write NO text.
```
> ⚠️ **Bẫy kỹ thuật:** provider đang **luôn append `ImageFidelity.suffix`** khi `references` không rỗng — suffix đó nói "Only the scene/lighting/composition may change" (coi 1 ref = 1 sản phẩm). Với Vary ta có **2 ref vai trò khác nhau** và muốn cảnh GIỮ nguyên. → Nên **thêm 1 tham số** cho `generate` để **tắt/đổi suffix mặc định** (vd `fidelity: ImageFidelity? = .default`), rồi truyền fidelity riêng cho Vary; hoặc làm prompt Vary đủ mạnh để áp đảo. KHÔNG để suffix mặc định "cãi nhau" với prompt Vary.

## BƯỚC 5 — Persist/Export
- Lưu `gridKind, sampleRefs, variantPatternRefs, variantAnchorIndex, sampleCols/Rows, sampleOffsets` trong Project JSON.
- Export high-fidelity như sample grid hiện tại.

---

## ⚠️ GIỚI HẠN THẬT — phải nói thẳng (handoff §3: sai họa tiết = lộ giả)
- **Pattern-swap chuẩn nhất với họa tiết IN/DỆT lặp** (thổ cẩm, in hoa). **Khó nhất với THÊU NỔI tinh xảo** — AI dễ làm phẳng/biến dạng mũi chỉ → lộ giả ngay với mắt khách hàng thật.
- Khuyến nghị giảm rủi ro:
  1. **Ô anchor luôn là ảnh THẬT** (đã đảm bảo ở Bước 3) → ít nhất 1 ô chuẩn 100%.
  2. **Bắt buộc review từng ô sau Vary**; cho nút **"Vary lại ô này"** (per-cell) như `reSampleCell` để sửa ô hỏng.
  3. Với hàng thêu cận cảnh, cân nhắc ít ô (2×2) thay vì 6 ô; hoặc giữ Variant Grid cho ảnh **tổng thể/đặt phòng** (góc xa, họa tiết đọc tổng thể) — không dùng cho macro đường chỉ (macro để format Detail/Comparison lo).
- **KHÔNG để AI tự chế họa tiết** — họa tiết LUÔN đến từ `variantPatternRefs` (ảnh thật user). Đây là ranh giới sống còn.

## KIỂM THỬ
1. Build xanh; project cũ mở vẫn chạy (gridKind default `.standard`).
2. Tạo Variant Grid → layout rơi vào 1 trong {1×3,3×1,2×2,3×2}; ô được điền họa tiết random từ input user.
3. **Right-click 1 ô → menu "Vary"** → ô đó giữ nguyên; các ô khác sinh lại: **cùng phòng/giường/góc/sáng của ô đó**, **mỗi ô vẫn đúng họa tiết của nó**.
4. Right-click ô KHÁC → "Vary" → đổi gốc, các ô vary lại theo ô mới; họa tiết vẫn lấy từ gốc (không trôi/tam sao).
5. "Vary lại ô này" trên 1 ô → chỉ ô đó đổi.
6. Export 1024×1280 nét; mở lại project giữ gridKind + pin họa tiết.

## TÓM TẮT
| Bước | File | Việc |
|--|--|--|
| 1 | Models.swift | `GridKind.variant` + `variantPatternRefs` (pin họa tiết); CodingKeys default |
| 2 | AppStore.swift | `makeVariantGrid`: random layout {1×3,3×1,2×2,3×2} + random họa tiết từ input |
| 3 | SampleGridEditor/ResultsView + AppStore | **right-click ô → menu "Vary"** (ô đó = gốc) → vòng lặp `generate([anchor, pattern])`, đổi `sampleRefs`, giữ `variantPatternRefs`, recompose |
| 4 | ImageProvider/NanoBanana | prompt Vary 2-ref + **tùy chọn tắt `ImageFidelity.suffix` mặc định** |
| 5 | ProjectStore | persist gridKind + pin họa tiết |

Cốt lõi: **right-click ô nào → ô đó thành neo bố cục (giữ ảnh gốc thật); các ô khác sinh lại theo bố cục ô đó nhưng GIỮ họa tiết riêng**. Họa tiết luôn từ ảnh thật của user, không bao giờ để AI bịa.
