# Guide — Style / Màu Text-Hook Overlay Winner (Proven)
*Research web 2026 + đối chiếu ảnh thực tế (thảm). Dùng để chỉnh preset render chữ của app.*

---

## ⚠️ TRƯỚC TIÊN: CÓ 2 "WINNER" KHÁC NHAU — CHỌN ĐÚNG TỆP
Có **2 trường phái overlay đều proven nhưng cho 2 mục tiêu khác nhau**:

| | **DR đại trà / high-CTR** | **Quiet luxury / premium** |
|--|--|--|
| Mục tiêu | Chặn ngón tay, CTR tối đa | Cảm nhận đắt, lọc người giàu |
| Màu | Tương phản gắt, bright (đỏ/vàng/cam), box đen | Trung tính, trắng/kem/đen, tối giản |
| Box | Box đặc, viền dày, highlight chói | Không box hoặc box mờ nhẹ; nhiều khoảng trắng |
| Cảm giác | "Quảng cáo bán hàng" | "Tạp chí nội thất" |

→ **Ảnh thảm bạn đang để màu hồng neon + box đen dày (kiểu DR đại trà).** Với sản phẩm decor cao cấp + tệp người giàu, cái này **làm rớt giá trị cảm nhận** — đúng cảnh báo "tránh tín hiệu rẻ tiền". Nên nghiêng **cột phải (premium)**, chỉ mượn *kỹ thuật dễ đọc* của cột trái.

---

## I. NGUYÊN TẮC CHUNG (cả 2 tệp đều phải tuân — proven, không cãi)
1. **Tương phản ≥ 4.5:1** giữa chữ và nền. Trắng trên nền tối, hoặc đậm trên nền sáng. *(Chỉnh tương phản + đơn giản hóa màu → giảm tới 21% CPC.)*
2. **Chữ to, đậm, sans-serif** (Montserrat/Inter/SF Bold…). Đọc được khi lướt nhanh, tắt tiếng.
3. **Không bao giờ trắng trên nền sáng mà thiếu bảo vệ** → phải có **outline tối / shadow / gradient nền** phía sau.
4. **Ngắn:** 1 hook ≤ 6 từ. Highlight **1 từ khóa** (đổi màu/đậm) để dẫn mắt — proven tăng engagement.
5. **Vị trí:** đặt ở **1/3 trên** (bắt mắt nhanh nhất) hoặc 1/3 giữa-dưới; tránh sát mép (safe zone, không bị UI che).

## II. PRESET KHUYẾN NGHỊ CHO BẠN (premium, vẫn dễ đọc)
**Preset A — "Quiet Luxury" (mặc định cho Tệp A / decor cao cấp):**
- Chữ: **trắng tinh hoặc đen than**, font serif thanh lịch hoặc sans sạch, **nhẹ nét** (không siêu đậm).
- Nền chữ: **không box**, dùng **gradient tối mờ rất nhẹ** sau chữ để đủ tương phản (giữ ảnh "thở").
- Highlight: 1 từ đổi sang **tông trầm có gu** (terracotta, xanh rêu, vàng đồng) — **KHÔNG hồng neon/đỏ chói**.
- Cảm giác: như tiêu đề tạp chí Architectural Digest.

**Preset B — "Aspirational" (cho Tệp B / muốn nổi hơn, vẫn sang):**
- Chữ trắng đậm + **box bán trong suốt tối** (đen/nâu sẫm ~70%) bo góc mềm.
- Highlight 1 từ bằng **màu nhấn giàu** (vàng gold ấm, không phải vàng chanh).
- Tương phản mạnh hơn A nhưng **vẫn tránh neon/box viền dày kiểu sale**.

> Cả hai: highlight **đúng 1 từ**, phần còn lại nhẹ. Box (nếu có) bo góc, mờ, không viền dày.

## III. CẤM (làm rớt giá trị — đang dính ở ảnh mẫu)
- ❌ **Hồng/đỏ neon, vàng chanh chói** cho chữ — tín hiệu "sale rẻ tiền", đuổi người giàu.
- ❌ **Box đen đặc viền dày** kiểu meme/clickbait.
- ❌ Nhiều dòng chữ, nhiều màu, nhiều highlight cùng lúc.
- ❌ Chữ "New text" placeholder (lỗi để sót trong ảnh mẫu).
- ❌ Hô hào sáo: "đẹp hơn ngay" còn tạm, nhưng tránh "GIẢM SỐC/MUA NGAY".

## IV. ÁP DỤNG VÀO ẢNH THẢM ĐANG CÓ
- Đổi **hồng neon → trắng** (trên ngạch cửa tối) hoặc **đen than** (trên nền sáng), bỏ box dày.
- Highlight "đẹp" → đổi sang **terracotta/xanh rêu** (ăn theo màu hoa văn thảm), không hồng.
- Hook "Lối vào đẹp hơn ngay" ổn về độ ngắn — có thể nâng cấp gợi cảm xúc hơn: "Lối vào **đáng nhớ** từ bước đầu" (nhấn *đáng nhớ*).
- Đặt hook trong **safe zone giữa**, một dòng, nhiều khoảng trắng quanh.

## V. CHO APP (preset render chữ — cơ chế b)
Đề xuất Settings có **2 preset chọn theo Tệp A/B** (đã có audience A/B trong JSON → tự gán preset):
- Tệp A → Preset A (quiet luxury).
- Tệp B → Preset B (aspirational).
- Mỗi preset khai sẵn: font, cỡ (auto theo độ dài), màu chữ, màu highlight (bảng màu trầm có gu, **không neon**), kiểu nền (none/gradient/box-mờ), vị trí mặc định (1/3 trên hoặc giữa), outline/shadow auto khi nền sáng.
- **Quy tắc cứng:** luôn đảm bảo tương phản ≥4.5:1; chỉ highlight 1 từ; chữ < 1/4 khung.

---

### Nguồn
- overlaytext.com — Facebook Text Overlay Guide 2026 (CTR)
- leadenforce.com — Poor Contrast & Color Kill CTR / Text Overlays for Meta
- creativeos.com — Facebook Ad Design Guide 2026
- straightnorth.com — Meta Creative Best Practices
- capcut.com & blitzcutai.com — Caption/keyword-highlight styles 2026
- (đối chiếu) research luxury/quiet-luxury trong thư mục /psy
