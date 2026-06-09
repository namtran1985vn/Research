# GUIDE cho Agent — Thêm Hook Style "Sticky Note" (giấy note vàng + chữ tay)
*Winner thực chiến: ảnh sản phẩm thật + tờ giấy note vàng chữ viết tay ("Xả kho 250k"). Trông như chủ shop chụp, KHÔNG giống quảng cáo → hook rate cao (khớp rd002: "lofi/authentic đè bẹp glossy").*

**File chính:** `Sources/Models/Models.swift` (enum `HookStyle` + `HookPalette`). Tùy chọn: `TextOnImage/TextRenderer.swift` (hiệu ứng nghiêng/bóng tờ note) + bundle font viết tay. Pattern y hệt các case sẵn có → an toàn.

---

## A. (BẮT BUỘC) Thêm màu vào `HookPalette` (Models.swift ~dòng 424–438)
```swift
static let noteYellow: UInt = 0xFCEB8A   // sticky-note paper
static let inkBlue: UInt     = 0x1F3A5F   // handwriting ink (xanh mực) — tùy, có thể dùng charcoal
```

## B. (BẮT BUỘC) Thêm case vào enum `HookStyle` (Models.swift ~dòng 463)
Thêm 1 case (đặt sau `boldBlock` để nó nằm nhóm "đáng chú ý"):
```swift
case stickyNote // handwritten ink on a yellow sticky-note paper — authentic shop look
```
Rồi điền vào TẤT CẢ switch trong enum (mỗi switch thêm 1 dòng `case .stickyNote`):

| Computed prop | Giá trị cho `.stickyNote` |
|--|--|
| `label` | `return "Sticky Note"` |
| `boxHex` | `return HookPalette.noteYellow` |
| `textHex` | `return HookPalette.charcoal` (mực đen) |
| `highlightHex` | `return HookPalette.inkBlue` (hoặc terracotta) |
| `cornerRadiusFactor` | `return 0.04` (góc giấy gần vuông, hơi bo) |

- `drawsBox`: tự đúng (≠ cleanFloat → vẽ box). OK.
- `boxOpacity`: mặc định 1.0 (giấy đặc) — OK, không cần sửa nếu logic là `== .boldBlock ? 0.70 : 1.0`.
- `prefersBold`: `!= editorial && != cleanFloat` → `.stickyNote` sẽ = true (đậm). Chữ tay không nên quá đậm → **thêm `.stickyNote` vào nhóm không-bold**: đổi thành `var prefersBold: Bool { self != .editorial && self != .cleanFloat && self != .stickyNote }`.
- `preferredFont`: thêm `case .stickyNote: return "<font viết tay>"` — xem mục D.

## C. (BẮT BUỘC) Font viết tay CÓ DẤU TIẾNG VIỆT
Đây là điểm dễ vỡ nhất. Nhiều font handwriting **không có dấu tiếng Việt** (ô, ạ, ệ...).
- **An toàn nhất:** bundle **"Caveat"** (Google Font, hỗ trợ Vietnamese) qua `FontRegistration.swift` (app đã có cơ chế này). Hoặc **"Patrick Hand"** (cũng có Vietnamese).
- `preferredFont` cho stickyNote → trả tên font đã bundle (vd `"Caveat"`).
- **Fallback:** nếu không bundle kịp, dùng font hệ thống gần nhất có dấu (vd `"Bradley Hand"` — NHƯNG phải test dấu tiếng Việt; nếu vỡ thì đừng dùng). Khuyến nghị bundle Caveat cho chắc.

## D. ⭐ PHẢI THẬT — KHÔNG ĐƯỢC NHÌN LÀ BIẾT GIẢ (yêu cầu cứng của user)
Một box vàng vector + font phẳng do app vẽ sẽ **luôn trông "sạch quá" → giả**. Giấy thật có texture, mép cong, bóng thật; chữ tay có nét đậm/nhạt, nghiêng lệch không đều. PHẢI đạt mức này.

### D1. Dùng ẢNH PNG TỜ NOTE THẬT thay vì vẽ box vector (CÁCH ĐÚNG)
- Bundle **4-6 ảnh PNG tờ giấy note THẬT** (chụp/scan giấy thật: hơi nhăn, mép cong, bóng mềm, nền trong suốt alpha), mỗi tờ một góc xoay/biến dạng khác nhau. Lưu trong assets.
- Khi `hookStyle == .stickyNote`: renderer **vẽ 1 PNG note (chọn ngẫu nhiên/seed theo creative) làm nền cho chữ**, thay vì vẽ rectangle. Đây là thứ làm mắt KHÔNG phát hiện giả (texture giấy thật).
- Scale/đặt PNG vào vùng text-safe; render chữ tay lên TRÊN nó.
> Vector box phẳng = giả. PNG giấy thật = thật. Đây là khác biệt quyết định.

### D2. Chữ tay phải "người thật viết" (điểm tố cáo giả nhất)
Trong `TextRenderer.swift`, khi `.stickyNote`:
- **Xoay cả khối note −3° đến −6°** (dán lệch tay), + **bóng đổ mềm lệch 1 hướng** để note nổi khỏi ảnh.
- **Mỗi DÒNG chữ nghiêng lệch nhẹ khác nhau** (±1–2°), KHÔNG thẳng tăm tắp.
- **Cỡ chữ & khoảng cách hơi không đều** giữa các từ (jitter nhỏ) — người viết tay không đều.
- **Màu mực không đen tuyệt đối**: xanh mực `#1F3A5F` hoặc đen-hơi-phai; nếu render được, cho **độ đậm nét hơi dao động**.
- Font: handwriting tự nhiên CÓ DẤU VIỆT (Caveat/Patrick Hand) — xem mục C.

### D3. (Thay thế, nếu muốn thật nhất tổng thể) để AI vẽ note trong imagePrompt
Đưa tờ note vào imagePrompt để image model vẽ luôn (note + bóng + ánh sáng khớp cảnh, rất thật). NHƯNG **AI hay sai chữ tiếng Việt có dấu** → 2 lựa chọn:
- (a) AI vẽ note **TRỐNG** (chừa giấy trống) → app render chữ tay lên (kết hợp độ thật của D1 + chữ Việt chuẩn). **Khuyến nghị.**
- (b) AI viết luôn chữ → phải soi & loại ảnh sai chính tả. Chỉ khi chấp nhận rủi ro.

> **Đường tốt nhất = D1 (PNG note thật) + D2 (chữ tay nghiêng-lệch-mực thật).** Vừa thật vừa giữ chữ Việt chuẩn 100%.

## E. (KHÔNG cần làm gì) UI tự nhận
`HookStyle` là `CaseIterable` → picker style tự liệt kê case mới. Swatch màu cũng auto. Không phải sửa View.

---

## KIỂM THỬ
1. Build xanh (chú ý: điền ĐỦ mọi switch trong enum, thiếu 1 case Swift sẽ báo lỗi exhaustive — đây là cái hay quên).
2. Mở editor text-on-image → picker Style có "Sticky Note".
3. Gõ hook tiếng Việt có dấu nặng ("Xả kho 250k", "Khăn dệt thủ công") → **kiểm dấu hiển thị đúng** (ô, ạ, ệ). Nếu vỡ → font chưa hỗ trợ Vietnamese, đổi sang Caveat/Patrick Hand đã bundle.
4. Ảnh ra: tờ note vàng nghiêng nhẹ, chữ tay đen, nổi trên ảnh sản phẩm.

## LƯU Ý CHIẾN LƯỢC (để bạn dùng style này đúng)
- Sticky Note hợp **Tệp B / authentic / cảm giác "deal của shop"** và các hook kiểu thông báo (xả kho, mẫu mới về, số lượng có hạn). 
- **Cẩn thận với phân khúc quiet-luxury (Tệp A):** "Xả kho 250k" là tín hiệu **giá rẻ** — đúng cái research bảo *đuổi người giàu*. Style này tăng CTR & đơn cho tệp nhạy giá, nhưng đừng dùng cho dòng cao cấp. → Để nó là **1 lựa chọn**, không phải mặc định.
- Tận dụng đúng sức mạnh: chữ tay = "thật, người thật, không phải ad" → giảm cảm giác bị bán (rd002). Hook nên mộc, đời thường, không bóng bẩy.

## TÓM TẮT
| Bước | File | Việc |
|--|--|--|
| A | Models.swift | +2 màu palette |
| B | Models.swift | +case `stickyNote` vào enum + điền mọi switch + sửa `prefersBold` |
| C | FontRegistration.swift | bundle font viết tay có dấu Việt (Caveat) |
| D (tùy chọn) | TextRenderer.swift | xoay nhẹ + bóng tờ note |
| E | — | UI tự nhận, không sửa |
