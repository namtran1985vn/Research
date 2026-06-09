# GUIDE cho Agent — Thêm 3 Hook Style "Authentic": Annotation · Chat Bubble · Stamp
*Cùng họ với Sticky Note (lofi/authentic, trông như ảnh thật — rd002). Khác sticky note: 3 cái này cần VẼ HÌNH (mũi tên / bong bóng / con dấu), không chỉ đổi màu box → lift lớn hơn.*

**Kiến trúc chung:** thêm 3 case vào enum `HookStyle` (Models.swift) để tích hợp picker/UI sẵn có; phần "vẽ hình đặc thù" làm trong `TextOnImage/TextRenderer.swift` bằng nhánh `switch layer.hookStyle`. Mỗi style phải đạt "thật" (PNG texture / vẽ vector mềm + nghiêng-lệch + bóng), không phẳng-vector-giả.

> **Khuyến nghị thứ tự ưu tiên (làm dần, không cần cả 3 cùng lúc):**
> 1) Annotation/Arrow (đắt giá nhất cho thảm/chăn) · 2) Chat Bubble (khớp funnel messaging) · 3) Stamp (nâng dòng cao cấp).

---

## PHẦN CHUNG — thêm 3 case vào enum `HookStyle` (Models.swift)
Thêm 3 case (sau `stickyNote` nếu đã có, hoặc sau `boldBlock`):
```swift
case annotation  // handwritten note + hand-drawn arrow/circle pointing at a product detail
case chatBubble  // messenger/zalo-style chat bubble (customer question or review)
case stamp       // craft stamp / tag badge: "Dệt thủ công", "Limited" — premium, quiet
```
Điền vào MỌI switch của enum (Swift bắt exhaustive — thiếu 1 case là lỗi build). Gợi ý giá trị:

| prop | annotation | chatBubble | stamp |
|--|--|--|--|
| `label` | "Annotation" | "Chat Bubble" | "Stamp" |
| `boxHex` | none/transparent (vẽ riêng) | `0xFFFFFF` (bubble nhận) hoặc `0xEDEDED` | none (vẽ riêng) |
| `textHex` | charcoal (mực) | `0x1A1A1A` | charcoal/đỏ-tem |
| `highlightHex` | terracotta/inkBlue | accent xanh chat | đỏ-dấu `0x8B2E2E` |
| `cornerRadiusFactor` | 0 | 0.5 (bong bóng bo tròn) | 0.5 (badge tròn) |
| `prefersBold` | false (chữ tay) | false | true (chữ tem) |
| `preferredFont` | font viết tay (Caveat) | sans thường (SF Pro) | sans condensed/serif tem |

> Thêm cả 3 vào nhóm `prefersBold == false` nếu là chữ tay (annotation). Chat bubble & stamp tùy thiết kế.

---

## STYLE 1 — ANNOTATION / ARROW (ưu tiên #1)
**Mục tiêu:** mũi tên/vòng khoanh vẽ tay chỉ vào chi tiết sản phẩm + ghi chú tay ngắn. Như người bán chỉ tận tay → authentic + bắt mắt nhìn đúng valueSignal (chất liệu/họa tiết).

**Render (TextRenderer.swift, nhánh `.annotation`):**
- **Mũi tên vẽ tay:** vẽ bằng `NSBezierPath` đường cong nhẹ (không thẳng máy móc) + đầu mũi tên; stroke width dao động, màu mực. HOẶC dùng **PNG mũi tên vẽ tay thật** (4-5 biến thể hướng) cho thật hơn.
- **Vòng khoanh tùy chọn:** ellipse nguệch ngoạc (path hơi méo, không tròn hoàn hảo).
- **Chữ tay** đặt cạnh, nghiêng-lệch như sticky note (mỗi dòng ±1-2°, mực không đen tuyệt đối).
- **Vị trí:** app cho user kéo đặt đầu mũi tên vào chi tiết muốn chỉ (dùng TextLayerCanvas đã có để kéo-thả).
- **Bóng mềm** để nét nổi khỏi ảnh.
> Tránh giả: stroke phải có độ rung/không đều; PNG nét bút thật là an toàn nhất.

---

## STYLE 2 — CHAT BUBBLE (ưu tiên #2, khớp funnel messaging của bạn)
**Mục tiêu:** bong bóng chat kiểu Messenger/Zalo — câu khách hỏi ("Còn mẫu đỏ không shop?") hoặc review. Social proof + authentic. Đây là style "sạch" được phép vì vốn là UI thật.

**Render (nhánh `.chatBubble`):**
- **Bong bóng:** rounded-rect bo tròn mạnh (cornerRadius lớn) + **đuôi tam giác nhỏ** 1 bên (vẽ path). Màu: xám nhạt `#EDEDED` (tin nhận) hoặc xanh `#0084FF` chữ trắng (tin gửi).
- **Avatar tròn** nhỏ cạnh bubble (tùy chọn — vẽ circle, hoặc để user gắn ảnh).
- **Chữ** sans thường, KHÔNG nghiêng (chat là gõ máy, phải "đúng UI" mới thật).
- (nâng cao) thêm dòng "Đang hoạt động" / dấu tích xanh nhỏ để giống thật.
> Đây là vector style — dễ làm nhất trong 3, không cần PNG. Chìa khóa "thật" = đúng tỉ lệ/bo góc/đuôi bong bóng như app chat thật.

**Lưu ý nội dung:** copy cho bubble nên là **câu hỏi/khen tự nhiên** (app prompt có thể sinh riêng), không phải khẩu hiệu. Vd "Mẫu này còn size lớn không ạ?" / "Mua lần 2 rồi, vẫn mê 😍".

---

## STYLE 3 — STAMP / TAG BADGE (ưu tiên #3, nâng dòng cao cấp)
**Mục tiêu:** tem tròn / con dấu mực / tag giấy buộc dây — "Dệt thủ công", "Limited", "Handmade". Truyền craftsmanship + exclusivity (stage 4-5) bằng hình, gần như không cần đọc. Sang, hợp Tệp A.

**Render (nhánh `.stamp`):**
- **Con dấu:** circle/ellipse viền kép + chữ cong theo vòng (text-on-path) — màu mực đỏ trầm `#8B2E2E` hoặc xanh-đen, **opacity ~85% + texture lốm đốm** (mực dấu không đều) để khỏi giả. PNG con dấu thật là an toàn nhất.
- **Hoặc tag giấy:** rounded-rect nhỏ + lỗ tròn + sợi dây (vẽ path cong) — như tag treo sản phẩm.
- **Chữ:** ngắn, in hoa nhẹ, font condensed/serif tem.
- **Vị trí:** 1 góc, KHÔNG che sản phẩm; nghiêng nhẹ.
> Tránh giả: tem phẳng nét sắc = giả. Cần texture mực + hơi mờ/lệch. PNG dấu thật scan vào là tốt nhất.

---

## ASSET CẦN CHUẨN BỊ (cho thật)
| Style | Asset |
|--|--|
| Annotation | 4-5 PNG mũi tên/vòng vẽ tay thật (nền trong suốt), nhiều hướng |
| Chat Bubble | không cần PNG — vẽ vector |
| Stamp | 3-4 PNG con dấu / tag thật (texture mực, nền trong suốt) |
> User có thể tự tạo PNG (vẽ tay/scan dấu thật) đưa agent bundle — sẽ thật hơn mọi thứ vẽ máy.

---

## KIỂM THỬ
1. Build xanh — điền đủ mọi switch trong enum cho 3 case.
2. Picker Style hiện 3 mục mới.
3. Mỗi style render đúng + **chữ tiếng Việt có dấu hiển thị chuẩn**.
4. Soi mắt: mũi tên/dấu có "thật" không (nét rung, texture, nghiêng-lệch) — nếu nhìn ra vẽ-máy thì chuyển sang dùng PNG asset thật.
5. Chat bubble: tỉ lệ/đuôi/bo góc có giống app chat thật không.

## TÓM TẮT
| Style | Độ khó | Cần PNG? | Hợp tệp |
|--|--|--|--|
| Annotation/Arrow | trung bình | nên có | A + B, hàng họa tiết |
| Chat Bubble | dễ (vector) | không | funnel messaging |
| Stamp/Badge | trung bình | nên có | A (cao cấp) |

Tất cả: thêm case enum + nhánh render riêng. Không phá style cũ. Ưu tiên Annotation → Chat → Stamp.
