# GUIDE cho Agent — Thêm "Campaign Structure (Testing/Scaling)" vào setupGuidance

**Mục tiêu:** thêm 1 field `structure` vào `setupGuidance`, để model khuyên đúng cấu trúc account hậu-Andromeda (1 Testing + 1 Scaling, broad CBO, consolidate) — gỡ vấn đề băm nhỏ nhiều campaign.

**Phạm vi:** sửa `Sources/Models/Strategy.swift` + `Sources/Models/Models.swift` + 1 dòng UI ở `Sources/Views/Inspector/InspectorView.swift`. Tất cả thêm-mới, có default → an toàn build.

**Nền lý thuyết (cho agent hiểu):** RD001 — post-Andromeda, brute-force volume & 3:2:2 chết; cấu trúc proven = **1 Testing campaign** (tung creative mới, broad CBO) + **1 Scaling campaign** (winner "tốt nghiệp" sang, ăn phần lớn ngân sách). Chạy nhiều CBO cùng broad + cùng ad = tự cạnh tranh, đội CAC. Consolidate thắng fragment.

---

## SỬA 1 — Model `SetupGuidance` (Models.swift, ~dòng 139)
Thêm 1 property (cuối struct):
```swift
struct SetupGuidance: Codable, Hashable {
    var pixelCapi: String = ""
    var valueRules: String = ""
    var lookalike: String = ""
    var targeting: String = ""
    var structure: String = ""        // post-Andromeda account structure: Testing + Scaling, broad CBO, consolidate
}
```
> Field có default "" → project cũ thiếu field tự nhận rỗng, không vỡ Codable.

---

## SỬA 2 — DTO (Strategy.swift, struct `SetupGuidanceDTO`, ~dòng 76)
**2a.** Thêm vào dòng khai báo property:
```swift
let pixelCapi: String; let valueRules: String; let lookalike: String; let targeting: String; let structure: String
```
**2b.** Thêm vào CodingKeys:
```swift
enum CodingKeys: String, CodingKey { case pixelCapi, valueRules, lookalike, targeting, structure }
```
**2c.** Thêm vào `init(from:)` (cạnh các dòng decode khác):
```swift
structure = (try? c.decode(String.self, forKey: .structure)) ?? ""
```

---

## SỬA 3 — Map DTO → model (Strategy.swift, ~dòng 151, khối `let sg = setupGuidance.map {`)
Thêm `structure:` vào khởi tạo `SetupGuidance`:
```swift
let sg = setupGuidance.map {
    SetupGuidance(pixelCapi: CopyText.clean($0.pixelCapi),
                  valueRules: CopyText.clean($0.valueRules),
                  lookalike: CopyText.clean($0.lookalike),
                  targeting: CopyText.clean($0.targeting),
                  structure: CopyText.clean($0.structure))
}
```

---

## SỬA 4 — System prompt (Strategy.swift)
**4a. Step 4** (`## Step 4 — Campaign setupGuidance`, ~dòng 311): thêm 1 gạch đầu dòng:
```
- `structure`: the post-Andromeda account structure to run — ONE broad CBO "Testing" \
campaign for unproven new creatives, and ONE broad CBO "Scaling" campaign where proven \
winners graduate and take the majority of budget. Consolidate; do NOT fragment into many \
campaigns/ad sets or run several broad CBOs with the same ads (they cannibalize each other \
and raise CAC). Brief, product-specific, actionable.
```
**4b. JSON schema** (`# OUTPUT`, dòng `"setupGuidance": { ... }`, ~dòng 397): thêm `"structure": string`:
```
"setupGuidance": { "pixelCapi": string, "valueRules": string, "lookalike": string, "targeting": string, "structure": string },
```
**4c. Câu LANGUAGE** (~dòng 390, danh sách field viết bằng `language`): thêm `structure` vào liệt kê (nó là văn bản tiếng Việt nên cần dịch):
```
... valueSignal, setupGuidance) ...   →  ... valueSignal, setupGuidance (incl. structure)) ...
```

---

## SỬA 5 — Hiện trong UI (InspectorView.swift, ~dòng 247–254)
Khối đang render các lensRow của setupGuidance. Thêm 1 dòng + nới điều kiện rỗng.

**5a.** Dòng ~248, thêm `&& sg.structure.isEmpty` vào điều kiện "tất cả rỗng":
```swift
!(sg.pixelCapi.isEmpty && sg.valueRules.isEmpty && sg.lookalike.isEmpty && sg.targeting.isEmpty && sg.structure.isEmpty) {
```
**5b.** Cạnh dòng `if !sg.targeting.isEmpty { lensRow("Targeting", sg.targeting) }`, thêm:
```swift
if !sg.structure.isEmpty { lensRow("Cấu trúc campaign", sg.structure) }
```

---

## KIỂM THỬ
1. Build phải xanh. Lỗi hay gặp: thiếu dấu `;` ở 2a, thiếu phẩy ở 3 (sau `targeting:`), thiếu phẩy schema 4b.
2. Chạy 1 project bất kỳ → mở Inspector → mục setup guidance phải có thêm dòng **"Cấu trúc campaign"** với nội dung kiểu "1 Testing CBO broad + 1 Scaling CBO broad, gộp lại, đừng băm nhỏ…".
3. Project cũ (đã lưu) mở lại không lỗi (structure = "" → dòng ẩn).

## TÓM TẮT
| # | File | Việc |
|--|--|--|
| 1 | Models.swift | +property `structure` (default "") |
| 2 | Strategy.swift DTO | +property, +CodingKey, +decode |
| 3 | Strategy.swift map | +`structure:` trong init SetupGuidance |
| 4 | Strategy.swift prompt | +gạch đầu dòng Step 4, +field schema, +LANGUAGE |
| 5 | InspectorView.swift | +điều kiện rỗng, +1 lensRow |

Toàn bộ thêm-mới, không xóa logic cũ → an toàn, không phá tính năng hiện có.
