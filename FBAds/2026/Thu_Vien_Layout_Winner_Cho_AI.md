# Thư Viện Layout Ảnh Winner (Proven) — Để AI Tham Khảo Khi Tạo Ảnh
*Chèn vào system prompt phần imageStyle. Mỗi layout có: slug · khi nào dùng · anatomy (bố cục cụ thể) · gợi ý prompt EN. Tất cả 4:5 (1024×1280), chừa negative space cho chữ, giữ sản phẩm thật, không text/logo do AI viết.*

> **Ưu tiên Pareto:** với hàng nội thất/decor, **rank #1 nên là LIFESTYLE IN-CONTEXT**, #2 là TESTIMONIAL. Các layout còn lại để phủ đa dạng (Andromeda).

---

## NHÓM 1 — BÁN BẰNG HÌNH (ít chữ · hợp Tệp A quiet-luxury)

### 1. `lifestyle` — Lifestyle in-context ⭐ Pareto
- **Khi dùng:** mặc định cho nội thất/decor; khơi "phiên bản cuộc sống khao khát".
- **Anatomy:** sản phẩm sống TRONG một không gian thật đẹp (phòng khách, góc đọc), **ánh sáng điện ảnh/tự nhiên**, có **hơi người** (bàn tay chạm, người ngồi mờ hậu cảnh), chiều sâu trường ảnh. Sản phẩm là tâm điểm nhưng thuộc về cảnh. Chừa khoảng trống (mảng tường/sàn) cho chữ.
- **Prompt EN:** "Editorial interior scene: [product] naturally placed in a sunlit upscale living room, cinematic soft light, shallow depth of field, a person's hand/figure softly blurred in frame, warm muted palette, generous empty wall space top-left for text. Photorealistic, magazine quality."

### 2. `beauty` — Beauty-shot studio
- **Khi dùng:** tôn chất liệu, cảm giác premium thuần.
- **Anatomy:** sản phẩm là nhân vật chính trên **nền tối giản/gradient trầm**, ánh sáng dựng tôn bề mặt & chất liệu, bóng đổ mềm, bố cục cân, nhiều negative space.
- **Prompt EN:** "Premium studio product shot of [product] on a minimal muted backdrop, soft directional lighting revealing material texture, gentle shadow, lots of negative space, refined high-end catalog aesthetic."

### 3. `detail_macro` — Macro / cận cảnh chi tiết
- **Khi dùng:** hàng nhiều họa tiết (thảm, runner, gối thêu); kích "perception premium" + lọc người sành.
- **Anatomy:** crop cực gần vào **thớ dệt/đường may/bề mặt hoàn thiện thật**, ánh sáng xiên làm nổi kết cấu, hậu cảnh nhòe.
- **Prompt EN:** "Extreme close-up macro of [product]'s real weave/stitch/surface, raking light emphasizing texture and craftsmanship, blurred background, tactile premium feel."

### 4. `flatlay` — Flat-lay / bộ sưu tập
- **Khi dùng:** khoe gu, gợi mua trọn bộ (Diderot → AOV cao).
- **Anatomy:** chụp **từ trên xuống (top-down)**, sản phẩm + phụ kiện đồng tông sắp xếp gọn trên nền chất liệu đẹp (gỗ, vải lanh), khoảng cách đều, 1 góc để trống cho chữ.
- **Prompt EN:** "Top-down flat-lay of [product] styled with tonal complementary props on a natural linen/wood surface, balanced negative space in one corner, cohesive curated palette, soft daylight."

---

## NHÓM 2 — BÁN BẰNG BẰNG CHỨNG / LÝ TRÍ (đánh objection · social proof)

### 5. `testimonial` — Testimonial card ⭐ #2 Pareto
- **Khi dùng:** social proof; bù cái lifestyle thiếu (lý do để tin).
- **Anatomy:** ảnh sản phẩm thật (lifestyle nhỏ) + **vùng trống rõ** để app render: ★★★★★ + 1 câu trích ngắn + tên khách. Bố cục sạch, sang.
- **Prompt EN:** "Clean testimonial-style composition: [product] in a tasteful real setting on one side, a large empty premium card area on the other side reserved for a 5-star quote (leave blank), elegant muted layout."

### 6. `before_after` — Before / After (chia đôi khung)
- **Khi dùng:** transformation thẩm mỹ không gian; rất mạnh với decor.
- **Anatomy:** khung chia **đôi dọc hoặc ngang**: nửa "trước" (không gian trống/đơn điệu) vs nửa "sau" (cùng không gian có sản phẩm, ấm & đẹp hơn). Cùng góc máy, cùng ánh sáng để tương phản rõ. Chừa dải nhỏ cho nhãn.
- **Prompt EN:** "Split-frame before/after of the SAME room from an identical camera angle: left/top bare and plain, right/bottom warmed and elevated by [product], consistent lighting, clear visual contrast, thin neutral divider."

### 7. `comparison` — So sánh "thường vs cao cấp"
- **Khi dùng:** xử lý objection chất lượng/giá trị; định vị bạn ở phía cao.
- **Anatomy:** **2 cột:** trái "loại thường" (mờ nhạt, kém hấp dẫn), phải "[sản phẩm] cao cấp" (nổi bật, chi tiết đẹp). Cân bằng, chừa chỗ tiêu đề mỗi cột.
- **Prompt EN:** "Two-column comparison: left a generic ordinary version looking flat/dull, right [product] looking refined with visible quality detail, even balanced layout, space above each column for a short label."

### 8. `news_card` — "Did you know / Breaking" card
- **Khi dùng:** chèn 1 insight (chất liệu/độ bền/độc bản); format ăn mạnh, ít cạnh tranh.
- **Anatomy:** ảnh sản phẩm + **vùng tiêu đề kiểu tạp chí/tin tức để trống** (app render headline lớn). Cảm giác bài báo biên tập, không phải quảng cáo.
- **Prompt EN:** "Editorial 'magazine feature' layout: [product] photographed cleanly with a large empty masthead/headline band reserved at top (leave blank), sophisticated journalistic look, muted premium palette."

### 9. `listicle` — Listicle / infographic (tiết chế)
- **Khi dùng:** "X điều khiến bạn phải lòng"; với cao cấp phải tinh tế, không thành tờ rơi.
- **Anatomy:** sản phẩm 1 bên + 3 vùng trống nhỏ xếp dọc bên kia cho icon + dòng ngắn (app render). Nhiều khoảng trắng, sang.
- **Prompt EN:** "Refined infographic layout: [product] on one side, three evenly spaced empty slots on the other for short benefit lines (leave blank), minimal icons, airy premium spacing."

---

## NHÓM 3 — BẮT CHÚ Ý / KHOE (hợp Tệp B new-money)

### 10. `ugc` — UGC tĩnh
- **Khi dùng:** giảm cảm giác "quảng cáo", hook rate cao; người thật trong nhà đẹp.
- **Anatomy:** trông như **ảnh chụp bằng điện thoại** (góc đời thường, ánh sáng tự nhiên, hơi ngẫu hứng) NHƯNG bối cảnh vẫn đẹp/cao cấp; người thật cầm/đang dùng sản phẩm.
- **Prompt EN:** "Authentic smartphone-style UGC photo: a real person using/holding [product] at home, natural candid angle, soft daylight, lived-in but tasteful upscale interior, slightly imperfect framing."

### 11. `founder` — Founder / câu chuyện chế tác
- **Khi dùng:** craftsmanship/heritage; xây niềm tin cao cấp.
- **Anatomy:** **bàn tay nghệ nhân** đang làm/chạm sản phẩm, xưởng/chất liệu thật hậu cảnh, ánh sáng ấm; chừa chỗ cho 1 câu story.
- **Prompt EN:** "Artisan craftsmanship scene: maker's hands working on/holding [product], authentic workshop materials softly blurred behind, warm intimate light, space for a short story caption."

### 12. `offer` — Offer/Promo card (tinh tế)
- **Khi dùng:** nhấn combo/bộ tuyển chọn. **Tránh giảm-giá-sốc** với người giàu.
- **Anatomy:** bộ sản phẩm bày đẹp + vùng trống cho dòng "trọn bộ tuyển chọn / giao tận nhà" (app render), badge tối giản. Sang, không loè loẹt.
- **Prompt EN:** "Elegant curated set of [products] beautifully arranged, refined composition with a clean reserved area for a tasteful 'complete collection' line (leave blank), no loud sale graphics."

---

## QUY TẮC ÁP DỤNG CHO AI (chèn kèm)
1. **Rank #1 = `lifestyle` (Pareto), #2 = `testimonial`.** Còn lại phủ các slug khác để đa dạng.
2. **Mỗi imagePrompt phải dựng đúng `moment` đã chọn thành một CẢNH cụ thể** (vd moment "tối thư giãn" → góc phòng tối ấm, đèn vàng), không phải sản phẩm trên nền trơn.
3. **Bơm aesthetic theo Tệp:** A = quiet luxury (trầm, tối giản, điện ảnh, tiết chế) · B = aspirational shine (tương phản giàu hơn, ánh sáng lung linh, "đáng khoe"). Hai tệp phải khác CHẤT.
4. **Luôn kết:** "No text, no words, no logos. 4:5 vertical." + chừa negative space cho chữ + giữ sản phẩm thật như ảnh đính kèm.
5. **5 ảnh/persona = 5 LAYOUT KHÁC NHÓM khác nhau**, không lặp cùng 1 layout đổi cảnh.
6. **Text/chữ do APP render** (cơ chế b) — AI chỉ chừa chỗ, không viết.

## MỞ RỘNG SLUG TRONG PROMPT
Thay `{beauty, ugc, testimonial, lifestyle, studio}` bằng:
`{lifestyle, beauty, detail_macro, flatlay, testimonial, before_after, comparison, news_card, listicle, ugc, founder, offer}`
