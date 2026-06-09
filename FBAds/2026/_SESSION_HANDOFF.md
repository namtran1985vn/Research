# SESSION HANDOFF — FB Ads Winner 2026 + App "Ad Creative Studio"
*Đọc file này đầu tiên ở session mới để nắm toàn bộ bối cảnh. Mọi file chi tiết nằm cùng thư mục `/Volumes/RAMDisk/Research/FBAds/2026/` (LƯU Ý: RAMDisk mất khi tắt máy — copy ra ổ thật để giữ).*

---

## 0. NGỮ CẢNH NGƯỜI DÙNG
- Bán **đồ trải/decor: chăn, thảm (cửa/phòng), khăn trải bàn/runner, phủ sofa** — phong cách thổ cẩm/vintage, nhiều họa tiết, nhiều SKU. Thị trường Việt Nam.
- Funnel chính: **inbox/messaging** (chốt đơn qua tin nhắn) — đây là nơi ra đơn.
- Mục tiêu: tạo creative ad Facebook/Meta thắng (2026, kỷ nguyên Andromeda), nhắm khách **giàu/sẵn chi**, mua theo **cảm xúc/dopamine**.
- Đang tự build **Mac app "Ad Creative Studio"** (SwiftUI) để sinh persona + creative + tạo ảnh hàng loạt.

## 1. NỀN TẢNG CHIẾN LƯỢC (đã chốt qua nhiều vòng research)
**Andromeda — 5 trục giao** mà thuật toán tối ưu: Người × Cảm xúc/intent × Thời điểm × **Creative cộng hưởng** × **Giá trị dự đoán**. Andromeda tạo "pool" ad, GEM chọn; ad **tự targeting bằng nội dung** → "creative IS targeting".
**Công thức đấu giá:** Total Value = Bid × Estimated Action Rate × Ad Quality → tiền KHÔNG cứu ad dở; nâng Quality/Relevance = rẻ hơn + thắng nhiều hơn.
**VOLUME ĐÃ CHẾT (rd001):** 3:2:2 hết thời, spam biến thể phá account. **Đa dạng = nhiều ANGLE/awareness, KHÔNG phải nhiều ảnh.** 1 creative angle-mới thắng 50 biến thể tầm thường.
**Niche đúng cách:** target RỘNG (Advantage+/broad) + Value Rules + Lookalike LTV cao; để **creative tự lọc** người giàu (KHÔNG bóp interest hẹp).
**Market Sophistication (Schwartz):** ngành chăn/thảm = **stage 4-5 (bão hòa)** → claim "đẹp/mềm" ĐÃ CHẾT. Phải bán **mechanism (chất liệu/dệt/craft)** + **identity/cảm xúc**.
**Cấu trúc account:** 1 Testing CBO broad + 1 Scaling CBO broad. Consolidate, đừng băm nhỏ.
**Scaling:** tăng budget **≤20-30% mỗi 2-3 ngày** (đừng gấp đôi). **Không sửa 7 ngày đầu** trừ khi cháy (CPA ≥3× breakeven). Luôn test creative kế thừa trước khi winner fatigue.
**DR có cảm xúc, không pushy:** desire-led không urgency-led; cấm "BUY NOW/đếm ngược/!!!" (đuổi người giàu). Ask nằm ở nút CTA.

## 2. TÂM LÝ NGƯỜI GIÀU (từ thư mục /psy + web)
- **Tự thưởng > khoe status** (self-reward ~57%, emotional fulfillment ~68% > status signaling).
- **Quiet luxury:** người giàu THẬT mua under-stated, "chỉ người sành nhận ra"; logo to/phô trương = middle-class muốn-trông-giàu. → 2 TỆP: **A (quiet luxury)** và **B (new money phô trương/nghiện dopamine)** — làm CẢ HAI, tách riêng ad set, khác aesthetic.
- Đòn bẩy: anticipation/khan hiếm thật, craftsmanship/heritage, perception=reality (placebo), Diderot (bán trọn bộ), self-expression.
- **CẤM** mọi tín hiệu rẻ/giảm-giá-sốc/thông số khô khan với hàng cao cấp.

## 3. CREATIVE — nguyên tắc tạo winner
- **Mỗi creative = 1 "bigIdea" riêng** (insight/angle, ≤12 từ); cấm 2 creative gộp được bởi Andromeda.
- Mỗi creative khai 5 trục: persona/tệp · emotionAxis · moment · imageStyle/layout · valueSignal.
- **Hook = topic clarity (về cái gì + cho ai) + on-target curiosity** trong ≤6 từ; CẤM mơ hồ kiểu "đẹp mọi góc nhìn".
- 4 primary text nên là **4 góc khác nhau** (cảm xúc/mechanism/proof/objection), không phải 4 cách nói cùng 1 ý.
- Ảnh: thumb-stop, thumbnail-legible, **giữ đúng họa tiết sản phẩm thật**, human element (tay chạm/chân bước = kích reward), 4:5 (1024×1280), chừa negative space cho chữ.
- **Authentic/lofi đè bẹp glossy** (rd002) — "people don't want to be sold to".

## 4. TEXT-ON-IMAGE (chữ overlay)
- Cơ chế (b): AI chừa chỗ, **app tự render chữ Việt** (chuẩn dấu 100%).
- Quy tắc: tương phản ≥4.5:1, hook ≤6 từ, **highlight đúng 1 từ**, chữ <1/4 khung.
- **2 trường phái:** Premium/quiet-luxury (trắng/đen/kem, highlight terracotta-gold, không box dày) vs DR/high-CTR (box tối, vàng/cam). CẤM neon (hồng/cyan/vàng-chanh) với hàng cao cấp.
- **Font:** Bold Block=sans đậm (Montserrat/SF Pro), Editorial=serif (Playfair/Georgia), Clean Float=sans mảnh. Tiếng Việt có dấu: Inter/Montserrat/Be Vietnam Pro/Playfair OK.
- **Hook styles "authentic" đã đề xuất:** Sticky Note (giấy note thật), Annotation/Arrow, Chat Bubble, Stamp — phải THẬT (PNG texture + nghiêng-lệch + bóng), không vector phẳng = lộ giả.

## 5. APP "AD CREATIVE STUDIO" — trạng thái
- Stack: SwiftUI macOS. Text engine: **OpenAI GPT** (đã đổi từ Claude — cân nhắc thêm Claude lại cho strategy). Ảnh: **GPT-image + NanoBananaImageProvider** (đã thêm).
- Cấu trúc: Campaign → Persona (N 1-6) → Creatives (M 3-10), chọn TOP theo điểm. JSON schema chặt trong `Sources/Models/Strategy.swift`.
- **Đã có:** bigIdea, DR-not-pushy, layout library, A/B aesthetic, parallel generation (concurrency cap+retry), text-on-image editor, sample grid (GridComposer), Nano Banana provider.
- Code đã giải nén tham chiếu ở `/sessions/.../outputs/adsapp2/` (zip gốc: `2026/Ads Studio App.zip`).

## 6. GUIDE CHO AGENT SỬA APP (đã viết, chưa áp — file riêng trong thư mục)
1. `GUIDE_Agent_Add_AwarenessStage.md` — thêm trục Schwartz (awarenessStage 1-5). **Ưu tiên #1.**
2. `GUIDE_Agent_Add_CampaignStructure.md` — thêm field `structure` (Testing/Scaling) vào setupGuidance.
3. `GUIDE_Agent_RD002_Hook_Reward_Scale.md` — hook clarity + reward "chạm/dùng" + scaling discipline.
4. `GUIDE_Agent_Add_StickyNote_HookStyle.md` — hook style giấy note thật (phải thật, không lộ giả).
5. `GUIDE_Agent_Add_3_Authentic_HookStyles.md` — Annotation/Chat Bubble/Stamp.
6. `GUIDE_Agent_Add_BeforeAfter_Grid.md` — layout Before/After grid 2 cột × N hàng (ảnh thật, dùng engine SampleGrid).
7. `GUIDE_Agent_Add_Comparison_Grid.md` — **(MỚI, RD003)** lưới 2 cột: trái "Hàng phổ thông trên thị trường" / phải "Hàng cao cấp bên mình". Bán MECHANISM (in↔thêu). Sibling của Before/After.
8. `GUIDE_Agent_Add_Variant_Grid.md` — **(MỚI)** lưới biến thể CÙNG SKU, layout random {1×3,3×1,2×2,3×2}, ảnh random từ input. **Right-click ô → menu "Vary"**: ô đó thành GỐC bố cục, AI vẽ lại các ô khác cho cùng góc/cảnh, **mỗi ô GIỮ họa tiết riêng** (pin `variantPatternRefs`, không tam sao).
9. `GUIDE_Agent_Add_ProblemSolution_Grid.md` — **(MỚI)** lưới 2 cột × {2,3}: trái Vấn đề / phải Giải pháp. Cột Giải pháp = random ảnh thật; **right-click ô Giải pháp → nhập prompt → AI sinh ảnh Vấn đề** ô cùng hàng (ref = ảnh Giải pháp để cùng cảnh). Chỉ bật SKU chức năng (phủ sofa/thảm cửa/chăn).
> ⚠️ **4 guide grid (6–9) GỘP CHUNG 1 enum `GridKind {standard, beforeAfter, comparison, variant, problemSolution}`** + dùng chung divider/nhãn 2-cột + `splitLeftLabel/RightLabel`. ĐỪNG đẻ nhiều `Bool` rời. Comparison/Before-After/Problem-Solution chia sẻ cơ chế 2-cột; Variant & Problem-Solution chia sẻ hành động right-click-gọi-`ImageProvider.generate`.
> Nguyên tắc số 3 (angle>volume) cũng đã giải thích kỹ — nên gộp các sửa text-prompt cùng đụng `Strategy.swift` làm 1 lần.

## 7. RESEARCH ĐÃ TỔNG HỢP (file trong thư mục)
- `Phuong_phap_chien_thang_FB_Ads_2026.md`, `Creative_Winner_Playbook_2026.md`, `Toi_uu_bo_sung_Camp_2026.md`
- `Guide_Persona_Creative_5_Truc_Andromeda.md`, `Guide_Toi_Uu_Persona_Creative_Andromeda.md`
- `Psy_Insights_Ban_Cho_Nguoi_Giau.md`, `Thu_Vien_Layout_Winner_Cho_AI.md`, `Guide_Text_Hook_Overlay_Winner.md`
- `RD001_Insights_Auction_Diversity_Sophistication.md`, `RD002_Insights_Hook_Impulse_Scale_Learning.md`
- `Insights_Branded_DR_AdSize_Targeting.md`, `REVIEW_AdsStudioApp.md`
- Prompt tái dùng (nếu chạy thủ công): `PROMPT_ChatGPT_Tao_Camp_FB_Ads_Winner.md`

## 8. SỐ LIỆU ACCOUNT THẬT (1-5/6/2026) — việc cần làm
- ROAS tổng ~3,8x (đang LÃI). **Winner: ChanHe001 (16,8x), ThamCua002 (8,8x), ThamTron102 (7x), THOCAM01 (4,6x).**
- **Loser cần TẮT:** ChanLead004 (0,36x), SanLead004 (0,59x), SofaL004 (0 đơn), + 3 camp like/engagement (đốt ~3 triệu vô ích). Lead campaign = lỗ đen; **messaging + purchase mới ra tiền.**
- **Đang băm 13 camp** → gộp về 1 Testing + 1 Scaling/sản phẩm.
- **Scale winner +20-30%/2-3 ngày**, test creative kế thừa ngay.
- Format winner thực tế quan sát: **collage/grid nhiều mẫu** (Variant Grid) đang ra đơn.

## 9. FORMAT ẢNH — đã có & đang cân nhắc thêm
**App đã có (~12):** lifestyle, beauty, detail-macro, flat-lay, testimonial-card, before/after (chỉ trong prompt), comparison, news-card, listicle, ugc, founder, curated-offer.
**Đã viết guide thêm:** Before/After Grid (ảnh thật, 2 cột × N hàng).
**Đề xuất thêm (chưa làm), xếp giá trị:**
- **Variant Grid** — winner đã chứng minh của user (chính thức hóa từ SampleGrid). #1.
- **Review/Chat SCREENSHOT thật** (khác testimonial-card AI vẽ) — social proof native, hợp funnel inbox. Proven (transcript nhắc review/chat ~3000 lần).
- **Size/Scale Reference** — giải objection kích thước, giảm trả hàng 23-29%. NHƯNG là "closer" (proof/objection, rank thấp), KHÔNG phải hook cold.
- **Native Article/Editorial** — trông như bài báo, hợp tệp A cao cấp.
> ⚠️ CẢNH BÁO: app đang gom QUÁ NHIỀU format (~18). Theo rd001 "đa dạng ở angle, không phải số format". **Nên dừng thêm, chốt ~5-6 format trụ cột** cho ngành chăn/thảm: Variant Grid · Lifestyle · Review/Chat screenshot · Before/After hoặc Size Reference · Native Article. Đây là việc giá trị hơn việc tìm thêm format mới.

> **CẬP NHẬT RD003 (chốt format trụ cột — việc treo §10.1 ĐÃ giải quyết):** 6 trụ cột = (1) Variant Grid [TOF] · (2) Lifestyle human-element [TOF] · (3) **Review/Chat Screenshot THẬT** [MOF/BOF] · (4) Native IG-Story lofi [TOF/MOF] · (5) **Before/After HOẶC Comparison HOẶC Size Reference** [BOF/closer] · (6) Native Article [TOF tệp A]. Chi tiết: `RD003_Insights_Proven_Static_Formats_2026.md`.

## 10. VIỆC TIẾP THEO (gợi ý cho session mới)
1. **Chốt 5-6 format trụ cột** (đừng nhồi thêm) — quyết định quan trọng nhất đang treo.
2. Agent áp các guide vào app (ưu tiên: awarenessStage → hook clarity → structure/scale).
3. Hành động account thật: tắt loser, gộp camp, scale winner đúng nhịp.
4. (Nếu cần research thêm) cụm Pareto còn lại: creative teardown, Cialdini, Hormozi offer — nhưng research đã khá đủ; ưu tiên THỰC THI hơn research thêm.

## 11. RD003 + 4 GRID TYPE + PHÁT HIỆN CODE + FB API (session 8/6/2026)

### 11a. RD003 — format proven (file `RD003_Insights_Proven_Static_Formats_2026.md`)
- Nguồn: 5 video media buyer (Fraser/Fraggle, Jared/Creative Dawn, Anthony, Matt) trong `rd003/`.
- **Phát hiện lõi:** app có 2 loại format — **Loại A "prompt layout"** (14 cái, chỉ là dòng chữ cho AI vẽ, kể cả review/họa tiết GIẢ) vs **Loại B "ảnh thật"** (Variant Grid + 4 grid mới). **Blind spot:** format proven 2026 thắng nhờ TRÔNG NATIVE/THẬT; cụm proof/authentic của app chỉ có ở dạng thẻ AI bóng bẩy → phá đúng cơ chế. App mạnh "polished", yếu "native-realism" = cụm đang thắng.
- **Format proven bị sót, ưu tiên build (loại B):** #1 **Native Review/Chat Screenshot** (khung Messenger/Zalo/comment thật — hợp funnel inbox VN nhất, app CHỈ có testimonial-card AI, khác bản chất); #2 **Native IG-Story chrome**; #3 Variant Grid đa-SKU (Diderot bundle); #4 Bold color-block hero (chỉ tệp B).
- **Comparison (so với hàng thị trường) proven mạnh** (CTR 1.8-3%) & khớp lõi "bán mechanism" stage 4-5. App TRƯỚC ĐÓ chỉ có before/after + 1 dòng comparison generic trong prompt — KHÔNG có comparison-với-thị-trường thật → đã viết guide #7.

### 11b. 4 GRID TYPE mới (guide #6–9 ở §6) — đều LOẠI B ảnh thật, gộp 1 `GridKind`
- Đã verify code & viết guide cho từng cái. Đây là việc THỰC THI chính đang chờ agent áp.

### 11c. PHÁT HIỆN CODE (đã verify trong `app.zip`, dùng cho mọi guide grid)
- `Creative` (Sources/Models/Models.swift ~272): `sampleRefs/sampleCols(=3)/sampleRows(=3)/sampleOffsets`, Codable, CodingKeys ~390. **CHƯA có** cờ split/variant nào — cả Before/After lẫn các grid mới đều chưa implement.
- `GridComposer.compose(images, size, gap, bg, cols, rows, offsets)` (Sources/TextOnImage/) — ghép ảnh + pan từng ô. Thêm `split:` để vẽ divider.
- **`ImageProvider.generate(prompt:, references:[Data], target:)`** — nhận **tối đa 4 ảnh ref** (Nano Banana ghép multi-ref). ⭐ Đây là nền cho nút Vary (Variant) & sinh ô Vấn đề (Problem-Solution).
- ⚠️ **BẪY:** provider **luôn tự append `ImageFidelity.suffix`** khi `references` không rỗng (ép "reproduce product exactly, only scene may change"). Với Vary (2 ref, giữ cảnh) & Problem-cell (không show sản phẩm) suffix này CÃI NHAU với prompt → cần thêm tham số tắt/đổi suffix.
- `AppStore.buildSampleGrid / reSample / reSampleCell` — random-pick ảnh + compose; tái dùng cho mọi grid.
- Schema strategy (Sources/Models/Strategy.swift): creative có `bigIdea, angle, messageStrategy, awarenessStage, layout, hooks[4], primaryTexts[4], imagePrompts[4]` + IMAGE LAYOUT LIBRARY (14 layout, đều loại A). Problem-Solution dạng ANGLE/copy thì làm được qua đây (awarenessStage problem-aware + layout Before/After) — nhưng user đã chọn làm Problem-Solution thành GRID TYPE riêng (guide #9).

### 11d. FB MARKETING API — app tự đăng camp lên FB Ads (research 8/6/2026)
- **CÓ.** Meta **Marketing API** (Graph API, ~v25 Q1/2026). Hierarchy + endpoint: upload ảnh `POST /act_{id}/adimages` → image hash; `POST /act_{id}/campaigns` → `/adsets` → `/adcreatives` → `/ads` (tạo theo thứ tự, lấy ID tầng trên).
- Auth: **System User token** (Business Manager). Quyền: `ads_management, ads_read, business_management`.
- **Rào cản theo use-case:** nếu app chỉ quản lý **account CỦA CHÍNH user** → dev mode + token của mình, **KHÔNG cần App Review công khai**, chỉ cần **Business Verification** cho Advanced Access. Nếu làm SaaS cho nhiều người → cần App Review đầy đủ. **(CÂU HỎI CÒN TREO: app dùng cho riêng user hay nhiều người? Quyết định này đổi hẳn độ phức tạp.)**
- Khuyến nghị: tạo camp ở trạng thái **PAUSED** để user review trước khi bật (tránh đốt tiền khi ảnh/prompt lỗi). Objective **Messages/click-to-Messenger** + CTA "Gửi tin nhắn" → khớp funnel inbox.

### 11e. BÀI HỌC PHƯƠNG PHÁP (để agent sau tránh lặp)
Đừng "đếm nhãn format" — một nhãn tồn tại ≠ năng lực tồn tại (vd app "có comparison" nhưng chỉ là 1 dòng prompt, không phải tính năng thật). Phân biệt format theo **CÁI NÓ BÁN** (mechanism / social proof / kết quả / identity), không theo hình dạng. Khi gặp bộ lọc "đừng bloat", kiểm tra kỹ cái-đã-có có THẬT phủ nhu cầu không, đừng loại sớm.
