# GUIDE cho Agent — Thêm Layout "Problem-Solution Grid" (Vấn đề | Giải pháp)

**Ý tưởng:** lưới 2 cột — **cột 1 = Vấn đề**, **cột 2 = Giải pháp**. **Mỗi HÀNG = một cặp Vấn đề→Giải pháp**. Cột Giải pháp = ảnh sản phẩm thật của user (random từ input). Ô Vấn đề = AI sinh theo prompt user mô tả tình huống.

**Sức mạnh:** nhiều hàng = khoe **nhiều vấn đề sản phẩm giải quyết** trong 1 static (gộp objection). Hợp các SKU chức năng: **phủ sofa, thảm cửa, chăn**.

---

## SPEC (chốt theo yêu cầu user)
1. **Lưới 2 cột × N hàng**, N ∈ **{2, 3}** → 2×2 (4 ô) hoặc 2×3 (6 ô). Cột trái = Vấn đề, cột phải = Giải pháp.
2. **Cột Giải pháp**: app **random ảnh từ input** của user (ảnh sản phẩm thật) cho mỗi ô.
3. **Right-click lên 1 ô GIẢI PHÁP** → context menu có mục AI → user **nhập prompt mô tả tình huống Vấn đề** → AI **sinh ảnh cho ô VẤN ĐỀ cùng hàng** (ô bên trái).

---

## HẠ TẦNG ĐÃ CÓ (đã verify)
- Cơ chế lưới 2-cột có **divider + 2 nhãn cột** = **dùng chung với Comparison/Before-After Grid** (xem `GUIDE_Agent_Add_Comparison_Grid.md` / `GUIDE_Agent_Add_BeforeAfter_Grid.md`). Chỉ khác nhãn: trái "Vấn đề", phải "Giải pháp".
- `Creative.sampleRefs/sampleCols/sampleRows/sampleOffsets` (Models.swift), `GridComposer.compose(...)`, `AppStore.buildSampleGrid`.
- **`ImageProvider.generate(prompt:, references:[Data], target:)`** — nhận ảnh tham chiếu (Nano Banana multi-ref). Đây là thứ hành động "sinh ảnh Vấn đề" cần.

→ Problem-Solution = **(2-col grid + 2 nhãn) đã có ở Comparison** + **1 hành động right-click-sinh-ảnh** (giống Vary của Variant nhưng sinh ô CẶP thay vì đồng bộ).

---

## BƯỚC 1 — Model (Models.swift, `Creative`)
Mở rộng enum kiểu lưới (gộp chung với các type khác — đừng đẻ bool rời):
```swift
enum GridKind: String, Codable, Hashable {
    case standard, beforeAfter, comparison, variant, problemSolution
}
var gridKind: GridKind = .standard

// dùng chung với comparison/beforeAfter:
var splitLeftLabel: String = ""    // problemSolution → mặc định "Vấn đề"
var splitRightLabel: String = ""   // problemSolution → mặc định "Giải pháp"

// problemSolution-only (tùy chọn, để sinh lại): prompt tình huống vấn đề theo từng ô vấn đề
var psProblemPrompts: [String] = []   // song song sampleRefs; chỉ dùng ở ô cột trái
```
- `gridKind == .problemSolution` → khóa `sampleCols = 2`, `sampleRows ∈ {2,3}`.
- Index ô như cũ: `i = row*2 + col`. **col 0 = Vấn đề, col 1 = Giải pháp.**
- Nhãn mặc định khi field rỗng: trái "Vấn đề", phải "Giải pháp".
- CodingKeys (~390): thêm `gridKind, splitLeftLabel, splitRightLabel, psProblemPrompts`; decode default an toàn.

## BƯỚC 2 — Tạo grid: random ảnh Giải pháp, để trống ô Vấn đề (AppStore)
```swift
func makeProblemSolutionGrid(pid, cid, rows: Int /*2 hoặc 3*/) {
    // gridKind = .problemSolution; sampleCols = 2; sampleRows = rows
    let solutions = userInputImages.shuffled().prefix(rows)   // random ảnh sp thật cho cột Giải pháp
    // sampleRefs: với mỗi hàng r → [ "" (ô vấn đề, trống), solutions[r] (ô giải pháp) ]
    // ô Vấn đề để placeholder + hint "Right-click ô Giải pháp để tạo tình huống"
    buildSampleGrid(... cols: 2, rows: rows ...)
}
```
> Cột Giải pháp luôn là **ảnh thật** của user (không AI) → sản phẩm chuẩn 100%. Chỉ ô Vấn đề mới do AI sinh.

## BƯỚC 3 — Right-click ô GIẢI PHÁP → "Tạo tình huống Vấn đề (AI)…" (UI + AppStore)
UI: `.contextMenu` chỉ trên ô **cột phải (Giải pháp)** khi `gridKind == .problemSolution`:
- Mục **"Tạo tình huống Vấn đề (AI)…"** → mở ô nhập prompt (user gõ mô tả vấn đề, vd "sofa cũ sờn vải, vết xước, lông mèo bám").
- (sau khi đã có) thêm **"Sửa / tạo lại Vấn đề"**.

Action:
```swift
func generateProblemCell(pid, cid, solutionIndex: Int, userPrompt: String) async {
    let problemIndex = solutionIndex - 1                  // ô vấn đề = ô bên trái cùng hàng (col0)
    let solutionImg  = loadPNG(sampleRefs[solutionIndex]) // dùng làm REF để giữ cùng phòng/góc
    let prompt = Self.problemScenePrompt(userPrompt)      // xem Bước 4
    let data = try await imageProvider.generate(
        prompt: prompt,
        references: [solutionImg],                        // ref = cảnh Giải pháp → Vấn đề cùng bối cảnh
        target: cellTargetSize)
    let name = imageStore.save(ImageCrop.normalizeToTarget(data))
    sampleRefs[problemIndex] = name
    psProblemPrompts[problemIndex] = userPrompt           // lưu để tạo lại
    buildSampleGrid(... reuse sampleRefs, cols: 2, rows, offsets ...)
}
```
- **Vì sao ref = ảnh Giải pháp:** để ô Vấn đề **cùng phòng/góc/sáng** với ô Giải pháp → cặp Vấn đề→Giải pháp ăn khớp (cú đấm before/after). Prompt user quyết ĐỊNH vấn đề gì; ảnh Giải pháp giữ bối cảnh nhất quán.

## BƯỚC 4 — PROMPT sinh ảnh Vấn đề
```
Using reference image 1 as the SAME room/scene/context/camera angle/lighting,
depict the "before / problem" state: <USER PROMPT>.
Show the pain/problem clearly and realistically, in the SAME setting as image 1
but WITHOUT our finished product/solution present. Tasteful and believable, not
exaggerated or gross. 4:5, reserve calm negative space for text, write NO text.
```
> ⚠️ Provider tự append `ImageFidelity.suffix` khi có reference (ép "reproduce product exactly") — **không hợp** ô Vấn đề (ta KHÔNG muốn show sản phẩm). → thêm tham số tắt/đổi suffix cho hành động này (vd `fidelity: nil`), hoặc dùng prompt đủ mạnh nói "WITHOUT our product".

## BƯỚC 5 — Divider, nhãn, persist, export
- **Divider dọc + 2 nhãn cột** "Vấn đề"/"Giải pháp": **tái dùng y hệt** Bước 2–3 của guide Comparison (GridComposer `split: true` + 2 TextLayer qua `TextRenderer`).
- Persist: `gridKind, sampleRefs, splitLeftLabel/Right, sampleRows, psProblemPrompts`.
- Export high-fidelity như sample grid.

---

## LƯU Ý CHẤT LƯỢNG (research RD003 + handoff)
- **Chỉ bật cho SKU chức năng** (phủ sofa, thảm cửa, chăn). Gối thêu/runner thuần thẩm mỹ → không có "vấn đề" mạnh, dùng Variant/Comparison.
- **Đóng khung mềm cho khách giàu** (handoff §1, §2): vấn đề là **khoảng-lệch/khó chịu tinh tế**, KHÔNG phô trương ghê-rợn, KHÔNG urgency/!!!. Tệp A nhẹ ("sofa lỗi nhịp căn phòng đẹp"), tệp B thẳng hơn.
- **Rủi ro lộ giả THẤP hơn Variant**: ô Vấn đề là cảnh "before" KHÔNG cần tái hiện họa tiết thật của sản phẩm → AI tự do hơn. Ô Giải pháp là ảnh thật → sản phẩm chuẩn.
- **Giữ cùng góc/sáng** giữa 2 ô mỗi hàng (đã đảm bảo bằng ref) → cặp đọc nhanh, thuyết phục.
- Mỗi hàng nên là **một vấn đề KHÁC nhau** (đa objection), đừng lặp 1 vấn đề 3 lần.
- **Funnel:** TOF cho người problem-aware + MOF xử objection (gán theo `awarenessStage`).

## KIỂM THỬ
1. Build xanh; project cũ mở vẫn chạy (gridKind default `.standard`).
2. Tạo Problem-Solution, rows=2 → lưới 2×2: cột phải có 2 ảnh sản phẩm thật random; cột trái 2 ô trống + hint; divider + nhãn "Vấn đề"/"Giải pháp" đúng.
3. Right-click ô Giải pháp hàng 1 → nhập "sofa cũ sờn, vết xước" → AI sinh ô Vấn đề hàng 1: **cùng phòng/góc với ô Giải pháp**, hiện sofa cũ KHÔNG có phủ.
4. Làm hàng 2 với vấn đề khác → 2 cặp Vấn đề→Giải pháp khác nhau.
5. "Sửa/tạo lại Vấn đề" → ô vấn đề sinh lại theo prompt mới; lưu prompt.
6. Đổi rows 2/3; export 1024×1280 nét; mở lại giữ gridKind + nhãn + prompt.

## TÓM TẮT
| Bước | File | Việc |
|--|--|--|
| 1 | Models.swift | `GridKind.problemSolution` + dùng chung `splitLeftLabel/Right` + `psProblemPrompts`; cols khóa 2, rows {2,3}; CodingKeys default |
| 2 | AppStore.swift | `makeProblemSolutionGrid`: cột Giải pháp = random ảnh thật; cột Vấn đề trống + hint |
| 3 | SampleGridEditor/ResultsView + AppStore | right-click ô **Giải pháp** → "Tạo tình huống Vấn đề (AI)…" nhập prompt → `generateProblemCell` sinh ô Vấn đề cùng hàng |
| 4 | ImageProvider/NanoBanana | prompt sinh cảnh Vấn đề (ref = ảnh Giải pháp) + **tắt `ImageFidelity.suffix`** (không show sản phẩm) |
| 5 | GridComposer + TextRenderer + ProjectStore | divider dọc + 2 nhãn (tái dùng Comparison); persist |

Cốt lõi: **cột phải = ảnh sản phẩm thật (random); right-click ô phải + nhập prompt → AI sinh ô trái (Vấn đề) cùng bối cảnh.** Mỗi hàng = 1 cặp Vấn đề→Giải pháp; 2–3 hàng = đa objection trong 1 static.
