# GUIDE cho Agent — Thêm trục "Market Sophistication / Awareness Stage" (Schwartz) vào Ads Studio App

**Mục tiêu:** thêm một trục mới `awarenessStage` (1–5 theo Eugene Schwartz) cho mỗi creative, để model tự nhận diện độ "chai" của thị trường và đẩy creative lên đúng tầng (ngành đông như chăn/thảm → mechanism + identity, bỏ claim thẳng đã chết).

**Phạm vi:** chỉ sửa `Sources/Models/Strategy.swift` (bắt buộc) + `Sources/Models/Models.swift` (1 dòng). KHÔNG đụng UI/kiến trúc. Rủi ro build = thấp (mọi field đều có default, decode tolerant).

**Nền lý thuyết (để agent hiểu, không cần chép vào code):** Schwartz 5 stages = mức độ thị trường đã thấy quảng cáo loại này. Stage 1 claim thẳng → 5 bán identity/cảm xúc. Thị trường bão hòa (bedding/rug/decor) ở stage 4–5; claim "đẹp, mềm" đã chết, phải bán cơ chế độc đáo (chất liệu/dệt = valueSignal) hoặc identity.

---

## SỬA 1 — Model `Creative` (Models.swift)
**File:** `Sources/Models/Models.swift`, struct `Creative` (~dòng 243–246, cạnh các axis tag khác).
Thêm 1 property mới ngay sau `valueSignal`:

```swift
var awarenessStage: Int = 3       // Schwartz 1–5: 1 direct-claim … 5 identity/emotion. Default 3 (mechanism).
```

> Vì `Creative` có `Codable` tự động và field có default, **không cần** sửa CodingKeys/decode thủ công ở Models.swift — Swift tự lo, project cũ thiếu field sẽ nhận default 3. Không vỡ.

---

## SỬA 2 — DTO decode (Strategy.swift)
**File:** `Sources/Models/Strategy.swift`, struct `CreativeDTO`.

**2a.** Thêm property (cạnh `valueSignal`, ~dòng 93):
```swift
let awarenessStage: Int
```

**2b.** Thêm vào enum `CodingKeys` (dòng `case emotionAxis, moment, messageStrategy, valueSignal`):
```swift
case emotionAxis, moment, messageStrategy, valueSignal, awarenessStage
```

**2c.** Thêm vào `init(from:)` (cạnh dòng decode `valueSignal`):
```swift
awarenessStage = (try? c.decode(Int.self, forKey: .awarenessStage)) ?? 3
```

---

## SỬA 3 — Map DTO → model (Strategy.swift, `makePersona`)
**File:** `Sources/Models/Strategy.swift`, trong `.map { idx, c in ... }` (khối gán `cr.emotionAxis = ...`).
Thêm 1 dòng cạnh các `cr.xxx = ...`:
```swift
cr.awarenessStage = c.awarenessStage
```
(clamp an toàn, tùy chọn: `cr.awarenessStage = min(5, max(1, c.awarenessStage))`)

---

## SỬA 4 — System prompt (Strategy.swift, `StrategyPrompt.system`)

**4a. Thêm MỤC MỚI — đặt NGAY TRƯỚC `# YOUR JOB`** (sau mục MENTAL MODEL / QUALITY OVER VOLUME nếu đã có):
```
# MARKET SOPHISTICATION (Eugene Schwartz — 5 stages; pick the right register)
First judge how SATURATED this product's market is: how long the category has existed, how \
many competitors, how ad-jaded the buyers are. Map to a stage and speak in its register:
  1 = brand-new market → a simple DIRECT claim is enough.
  2 = some competition → ENLARGE the claim (bigger/faster/better, specifics).
  3 = crowded, claims feel stale → lead with a UNIQUE MECHANISM (the how/why it works).
  4 = mechanism is also common → a STRONGER / differentiated mechanism.
  5 = fully jaded buyers → sell IDENTITY & EMOTION (who they become), not the product.
Saturated categories (bedding, blankets, rugs, home textiles, decor) are STAGE 4–5: plain \
claims like "beautiful / soft / high quality" are DEAD and waste spend. For such markets, \
keep MOST creatives at stage 4 (a unique mechanism — material, weave, craft, construction; \
this doubles as the `valueSignal`) and stage 5 (identity/emotion), and avoid stage 1–2 \
direct claims. Each creative's `bigIdea` must fit its declared `awarenessStage`.
```

**4b. Thêm 1 dòng vào Step 3** (cạnh chỗ liệt kê các field bắt buộc của creative):
```
Each creative also declares its `awarenessStage` (int 1–5, Schwartz). For saturated markets \
keep most creatives at 3–5 and avoid 1–2; the bigIdea, message and hooks must match that stage \
(stage 4 → mechanism-led; stage 5 → identity/emotion-led).
```

**4c. Thêm field vào JSON SCHEMA ở mục `# OUTPUT`** — trong object creative, thêm `"awarenessStage": int` (đặt cạnh `valueSignal`):
```
"emotionAxis": string, "moment": string, "messageStrategy": string, "valueSignal": string, "awarenessStage": int,
```

**4d. Thêm `awarenessStage` vào câu LANGUAGE** (danh sách field cần viết bằng `language`) — *không bắt buộc* vì nó là số, nhưng nếu muốn nhãn hiển thị tiếng Việt thì bỏ qua (giữ int). Khuyến nghị: giữ là **int**, không dịch.

---

## (TÙY CHỌN) SỬA 5 — Hiển thị badge trên thẻ creative
Nếu muốn thấy stage để lọc/duyệt: trong `Sources/Views/Results/CreativeCardView.swift`, cạnh chip Tệp A/B + imageStyle, thêm 1 chip nhỏ `S\(creative.awarenessStage)` (vd "S4"). Không bắt buộc cho chức năng; chỉ để bạn nhìn nhanh creative nào đang ở stage thấp (claim) để loại.

---

## KIỂM THỬ SAU KHI SỬA
1. Build (`xcodebuild ... build`) — phải xanh; nếu đỏ, kiểm 3 chỗ: CodingKeys (2b), thiếu dấu phẩy trong schema (4c), tên field model (1).
2. Chạy 1 product **ngành đông** (chăn/thảm), N=3, M=5.
3. Mở JSON / thẻ creative, soi:
   - Mỗi creative có `awarenessStage` 1–5.
   - **Phần lớn ở 3–5**, hầu như không có 1–2.
   - bigIdea & hook của creative stage-4 nói về **cơ chế/chất liệu** (không phải "đẹp, mềm"); stage-5 nói về **cảm xúc/identity**.
4. Nếu model vẫn ra nhiều stage 1–2 → tăng liều: thêm vào cuối Step 3: *"If you assign stage 1 or 2 to any creative in a saturated market, you are wrong — replace it with a stage 3–5 angle."*

## TÓM TẮT THAY ĐỔI
| Chỗ | File | Loại |
|--|--|--|
| 1 | Models.swift | +1 property `awarenessStage` (default 3) |
| 2a-c | Strategy.swift CreativeDTO | +property, +CodingKey, +decode |
| 3 | Strategy.swift makePersona | +1 dòng map |
| 4a-c | Strategy.swift prompt | +1 mục, +1 dòng Step 3, +field schema |
| 5 (tùy chọn) | CreativeCardView.swift | badge "S4" |

Tất cả là thêm-mới, không xóa/đổi logic cũ → an toàn, không phá tính năng hiện có.
