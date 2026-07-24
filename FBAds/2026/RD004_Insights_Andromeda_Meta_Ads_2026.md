# RD004 — ĐÚC KẾT KINH NGHIỆM META ADS 2026 (POST-ANDROMEDA)

> Nguồn: 258 video YouTube (~4,4MB transcript, lọc từ 344 video trong rd004), phân tích bởi 12 agent song song ngày 23/07/2026.
> Bao gồm: Ben Heath, Sam Piliero (Moonlighters), Charley (Disrupter School), Dara Denney, Chase Chappell, Alex Hormozi, Savannah Sanchez, Sabri Suby, Nick Theriot, Jon Loomer, Justin Lalonde, Jared Robinson, Tara Zirker, AC Hampton, Qn92 (VN)… cùng nhiều nguồn khác.
> ⚠️ Phần lớn là content của agency/coach có mục đích bán dịch vụ — các con số case study tự công bố, cần đối chiếu trước khi áp dụng.

---

## ⭐ 10 NGUYÊN TẮC VÀNG (đồng thuận cao nhất giữa các nguồn)

1. **Creative CHÍNH LÀ targeting.** Andromeda đọc toàn bộ nội dung ad (hình, lời thoại, copy, URL, landing page) để tự chọn người xem. Interest/lookalike/manual targeting gần như hết vai trò — chỉ giữ hard controls: location, min age, exclusions.
2. **Đa dạng creative thật sự, không phải biến thể nông.** Meta gom các ad "na ná nhau" (đổi headline/màu nền) vào cùng 1 entity và phạt CPM. Diversity = khác CONCEPT: format khác, angle khác, persona khác, awareness stage khác.
3. **Cấu trúc account ĐƠN GIẢN thắng.** Chuẩn phổ biến: 1 campaign prospecting (CBO) + 1 ad set broad + nhiều ads đa dạng; tách riêng retention/khách cũ; retargeting giờ là TÙY CHỌN. Consolidate để dồn conversion data thoát learning phase (~50 conversions/tuần).
4. **Tối ưu đúng event cuối cùng.** Thuật toán "hiểu theo nghĩa đen": chọn Traffic thì được người click, không phải người mua. Luôn optimize Purchase/Lead — không bao giờ ATC/checkout/link click. Ngân sách nhỏ tuyệt đối không chạy awareness.
5. **Đừng đụng vào account liên tục.** Mỗi chỉnh sửa reset learning. Chờ 48–72h sau launch, đánh giá trên trung bình 7 ngày, không panic vì 1 ngày xấu ("snow globe" — mỗi lần đụng là lắc quả cầu tuyết).
6. **Đánh giá ở cấp campaign/ad set, không tin ROAS từng ad.** Meta tự sequencing TOF→BOF trong 1 ad set: ad ROAS thấp + frequency thấp thường là "nhiên liệu" top-funnel; tắt nó thì ad "ngon" sụt theo. Frequency là chỉ báo vị trí phễu (1–1.3 = prospecting, 2+ = retargeting trá hình).
7. **CAPI là bắt buộc, và đối chiếu backend.** Pixel đơn thuần under-report 15–50%; Meta bỏ sót doanh thu recurring (case £58k/£96k không được ghi nhận). Nhìn số khách mới trong Shopify/CRM, blended MER/NCPA — không tin mù Ads Manager.
8. **Volume có hệ thống, không phải volume rác.** Chuẩn tham khảo: 1 ad mới/1.000$ spend/tháng (hoặc 1 ad/tuần cho mỗi $10k/tháng). Track angle + hook + format + kết quả từng ad — không track thì không tái tạo được winner.
9. **Ad không được giống ad.** UGC thô, founder ad quay iPhone, static "xấu mà thật" thắng production bóng bẩy. Native format + ngôn ngữ của chính khách hàng (đào Reddit, review, comment) là lợi thế lớn nhất.
10. **Scale từ từ và scale bằng chiều rộng concept.** Tăng budget ~20% mỗi 3–5 ngày; chấp nhận ROAS giảm khi scale (4x @$100k > 10x @$5k); mỗi angle/concept có trần scale riêng — giữ mọi concept trên ngưỡng hòa vốn thay vì dồn hết vào ROAS cao nhất.

---

## 1. THUẬT TOÁN: ANDROMEDA / GEM / LATTICE

### Bản chất
- **Andromeda** = retrieval engine (công bố 02/12/2024, KHÔNG phải update mới cuối 2025 — "update tháng 10" phần lớn là hiệu ứng bầy đàn của content creator). Lọc hàng chục triệu ad candidates xuống vài nghìn cho từng người, chạy trên chip NVIDIA GH200/MTIA, model capacity tăng ~10.000 lần.
- **GEM** (Generative Ads Recommendation Model) = "bộ não" kiểu LLM dự đoán chuỗi hành vi user; **Lattice** = tầng ranking hợp nhất ra quyết định cuối (Meta công bố +13% CTR, +16% CVR).
- Ví von dễ nhớ: giống Netflix cá nhân hóa feed cho từng người — câu hỏi đảo từ "người này nên thấy ad nào" thành "ad nào xứng đáng hiện cho người này".

### Hệ quả vận hành
- **Entity bundling**: ads giống nhau về ngữ nghĩa/hình ảnh bị gom chung 1 entity ID — 30 biến thể cùng concept = mua 30 vé số cùng dãy. Chỉ được tính là ad khác khi **visual khác trong 3–5 giây đầu**.
- **Sequence learning**: Meta hiểu hành trình mua (mua vé ski → thấy ads đồ ski); tự dựng phễu TOF→MOF→BOF ngay trong 1 ad set — việc của bạn là cung cấp đủ creative cho cả 3 tầng (tỷ lệ sản xuất ~70% TOF / 20% MOF / 10% BOF).
- **Tín hiệu chất lượng mới**: watch time, rewatch, share, save, DM share (4,5 tỷ/ngày), thậm chí "scroll velocity deceleration". Nội dung gimmick/clickbait bị suppress; "behavioral echo" (click rồi bounce 2–5s) làm tăng CPM.
- **Phân phối thay đổi**: budget rải đều hơn cho nhiều ad (thay vì dồn 2–3 winner) — dấu hiệu setup đúng là spend phân bổ đều; advertiser phải tự tắt ad kém thủ công.
- **Custom audience giờ chỉ là "suggestion"** — Meta được phép vượt tệp; ranh giới cứng duy nhất nằm ở Audience Controls (location, min age, exclude, language). ~1/3 budget broad tự động đi vào retargeting.
- Cần **warm-up**: $300–600 (account nhỏ) tới $10–15k spend trước khi Andromeda vượt manual targeting; roll-out không đồng đều giữa các account.
- Meta có động cơ tài chính khiến bạn thắng — kết quả tụt thường do setup lỗi thời, đối thủ out-execute, macro hoặc mùa vụ, không phải "Meta phá account".

---

## 2. CREATIVE — CHIẾN TRƯỜNG DUY NHẤT CÒN LẠI

### Chiến lược
- Media buying đã bị tự động hóa; **arbitrage duy nhất còn lại là creative**: chiến lược → sản xuất → phân tích tạo flywheel. Ai dành thời gian cho creative nhiều hơn cấu trúc account kiếm nhiều hơn hẳn.
- **Concept = Persona × Angle × Offer (× Format)**. Thứ tự ưu tiên test: Angle (vô hạn) > Offer (nhanh cạn) > Persona (tạo bề rộng) > Format (ít tác động nhất) — đa số làm ngược.
- Persona phải cực cụ thể (vấn đề + desire + trigger), không phải "nữ 25–45": "mẹ đã thử 6 loại supplement vì con không chịu ăn rau".
- **Đa dạng theo 5 trục**: awareness stage, pain point, desire, avatar, angle — đưa hết vào 1 ad set để Meta tự sequencing.
- Không cần nhiều format: Hormozi chạy 420 ads với ~7 format. Cần nhiều MESSAGE + VISUAL.
- **Research là nền móng**: đào Reddit, Amazon reviews (Apify + Claude), comment trên chính ads mình, post-purchase survey, email CSKH đổ vào ChatGPT — dùng NGUYÊN VĂN ngôn ngữ khách. Brand nào "gọi tên" frustration đầu tiên bằng đúng từ khách dùng sẽ thắng.
- Mix pain vs desire: nghiêng 60–70% về PAIN — asset tốt nhất luôn đứng trên pain point.

### Hook (quyết định 80% ad)
- Hook = copy hook + visual hook, chỉ có ~0,5–3 giây. 80–95% người xem không vượt qua hook → 2 body + 15 hook > 5 body + 2 hook.
- Khung chấm hook 5 tiêu chí: Clarity / Relevance / Novelty / Specificity / Credibility (cần 2–3 cái tốt).
- Hook đang thắng 2026: demographic call-out ("women over 40, listen up" — mạnh nhất, vừa là tín hiệu targeting; lưu ý rủi ro policy personal attributes), contrarian truth, specific proof, curiosity gap, truth-bomb giá ("Sản phẩm này $120. Đắt thật. Nhưng bán chạy nhất. Đây là lý do"), founder's letter high-stakes, ASMR/texture, before/after + mốc thời gian, "How do I know if…".
- Nói trực tiếp vào camera 3 giây đầu: +25% retention 10s, +9% sound-on.
- Hook mới = creative ID mới, không bị bundle → ad fatigue chỉ cần thay ~50 hook mới là chạy thêm được $100k spend.

### Format đang thắng
- **UGC thô/raw** (UGC trau chuốt là loại kém nhất), **founder ad** (origin story 1–2s giới thiệu + fact giáo dục; gần như miễn phí), **EGC**, street interview, podcast-style thật, mini VSL (hook cảm xúc → story → unique mechanism → risk reversal → testimonials), **static** (vẫn tạo 60–70% conversions trên Meta — "golden age" nhờ AI; benefit callout, us-vs-them, ugly ads/post-it, meme, advertorial/farticle, tweet-screenshot qua profile expert), carousel (save rate cao nhất), whitelisting/partnership ads (CPA −19%, CTR +13%; Meta khuyến nghị ≥50% ads là creator content).
- Ad phải xem được không tiếng, tỷ lệ 1:1 + 9:16 (nội dung quan trọng trong safe-zone 1:1 giữa khung 9:16 = 1 file cho mọi placement).
- Copy dài hoạt động như "prompt"/SEO cho thuật toán — copy nhiều tính từ mô tả thắng bản ngắn ~20%; thêm URL vào copy tăng ROAS 10–50% (nhưng test vị trí URL — đặt đầu copy có case CPA tăng gấp đôi).
- Copy 4 phần: Hook → Problem → Offer → CTA; viết trình độ lớp 5–7; hướng khách hàng (outcome) không hướng doanh nghiệp ("15 năm kinh nghiệm" = vứt). Công thức offer: "We do X for Y so you can Z without W".
- Fatigue: winner chết trong vài tuần (không còn hàng năm). Dấu hiệu: CPA +15–20%, CPMR leo thang, cột Delivery báo "Creative limited/fatigued". Refresh: account nhỏ hàng tháng, account lớn hàng tuần. Cùng 1 message thấy ≥4 lần → mất khách vĩnh viễn.

### Sản xuất volume
- Công thức Hook + Body + CTA tách rời: 10 body × 10 CTA × 70 hooks × pre-hooks × editors → hàng nghìn ads/1 buổi quay.
- Quy tắc 33%: nguồn creative = 33% in-house + 33% UGC army + 33% AI; đồng thời 33% TOF/MOF/BOF.
- Phân bổ effort: 50–60% nhân bản winner (đổi hook/format/persona — leverage cao nhất), 20–30% iterations, 20–30% concept mới. Vắt kiệt winner: 1 testimonial thắng → ~100 phiên bản.
- Ngân sách production: 30–100k$/tháng spend → ~25% media budget cho production; coi creative là revenue driver, không phải cost center.
- Team 3 vai tách biệt: Strategist (research, brief, đọc data) — Creator (raw footage; xin full rights vĩnh viễn từ ngày 1) — Editor.
- AI: mạnh nhất ở briefing/script + production (VSL AI, static AI ~90%); KHÔNG tự động hóa ideation và cẩn trọng với analysis. Test nhanh bằng Trial Reels (đăng organic đo retention trước khi tốn tiền).

---

## 3. CẤU TRÚC CAMPAIGN

### Đồng thuận: đơn giản + consolidate
- Chuẩn phổ biến: **1 campaign / 1 ad set broad / 15–30 ads** (không quá 50). Độ phức tạp account = độ phức tạp business.
- Chỉ tách campaign khi: location khác, dòng sản phẩm khác, chiến lược đặc thù, hoặc testing.
- **Tách khách cũ**: campaign Retention riêng (~$50/ngày, purchasers 180 ngày) + exclude purchasers khỏi prospecting (khai Audience Segments + customer list, match score ≥8.5). Nếu không, Meta âm thầm đốt phần lớn budget vào engaged/existing (case: tiết kiệm $1,2M/năm sau khi kiểm soát).
- Không tách TOF/MOF/BOF campaign nữa — điều khiển funnel bằng TỶ LỆ SẢN XUẤT creative trong cùng ad set.

### Các biến thể theo quy mô (chọn 1, đừng trộn)
- **Ngân sách nhỏ (<$100/ngày)**: 1 campaign – 1 ad set – 3–5 creative thật sự khác nhau (nhồi 20–50 ads sẽ pha loãng, AI "giết non" ad tốt); hoặc ABO 3 angle × 1 ad/ad set chia đều. Kỷ luật không đụng 7–21 ngày.
- **Testing + Scaling 2 campaign**: testing campaign có nhiệm vụ duy nhất là ÉP spend cho ads mới; winner graduate bằng POST ID (giữ social proof) sang scaling campaign/ASC — nhưng KHÔNG tắt bản gốc đang chạy.
- **Pack system (Sam Piliero, $50M+ spend)**: mỗi batch creative mới = 1 ad set ("pack") mới trong prospecting CBO, đặt tên pack#_avatar_concept, ad set minimum spend = 1× target CPA trong 7 ngày rồi gỡ (win-rate concept có case tăng 8% → 31%); không bao giờ nhét ad mới vào pack cũ.
- **One Campaign Method / 3-2-2 (Charley)**: 1 CBO gồm ad set Control (4–8 ads ổn định) + tối đa 2 ad set Test, mỗi test = 1 ad "3-2-2" (3 creatives CÙNG format + 2 headlines + 2 primary texts); test để thay "cầu thủ tệ nhất" trong control, không phải để scale riêng.
- Ad set setup chuẩn: performance goal = maximize conversions (hoặc value nếu AOV biến thiên), event = Purchase, attribution 7-day click (+1-day engaged view), CAPI bắt buộc, Advantage+ placements, đúng ngôn ngữ.
- Enhancements: quy tắc "thứ gì thay đổi BÊN TRONG ảnh/video thì tắt" (visual touch-up, music, background, AI image); overlay/text quanh ad thì được. **Tắt: site links, multi-advertiser, related media, auto-translate** — và recheck thường xuyên vì chúng TỰ BẬT LẠI.
- Value rules = nơi kiểm soát targeting thật: giảm bid 50–90% cho segment không muốn (giới tính/tuổi/placement/geo) thay vì narrow targeting.
- Local service: bán kính + tuổi + exclusion zones; lead form với 3–4 câu hỏi lọc (bắt gõ tay SĐT chống autofill); speed-to-lead 5 phút đầu quyết định tất cả.

---

## 4. TESTING

- Test như nhà khoa học: mỗi test 1 hypothesis, **1 biến mỗi lần**, giữ running board (Google Sheet: angle/hook/format/kết quả). Hit rate thực tế chỉ **5–10%** (1–3 winner trong 25–30 creatives) → cần ~20 ads/concept để kỳ vọng 1 winner.
- Thứ tự test theo tác động (Ben Heath): **OFFER → ANGLE → STYLE → HOOK → biến thể nhỏ** (biến thể nhỏ thắng cũng chỉ ±10%).
- Pipeline A/B: A = concepts mới, B = iterations của winner. Account bí winner → 70/30 nghiêng new; vừa có batch nóng → đảo 30/70. (Tương tự 70/20/10 của Hormozi.)
- Đánh giá: chờ tối thiểu 3 ngày (lý tưởng 7), spend tối thiểu ~$100 hoặc 2.000–4.000 impressions, trên data 7 ngày so với break-even CPA. Kill sớm khi hook rate <25%, CTR thảm, CPA "không đi đúng hướng". Late attribution: ad đã kill mà 2–3 ngày sau data về trong KPI → bật lại.
- Quy trình 3 bước đánh giá (Charley): (1) ad có "earn spend" không → (2) profit volume toàn campaign tăng không (tiêu chí duy nhất, không phải CPA/CTR lẻ) → (3) scale.
- **Creative Testing Tool** chính thống của Meta (ad level): test 2–5 ads, tách audience không chồng lấn, ép spend đều — giải quyết việc ad mới không được chia tiền; NHỚ đổi metric từ cost-per-engagement sang cost-per-purchase.
- Test concept khác biệt hoàn toàn: đặt vào AD SET RIÊNG (~20% budget) — ném thẳng vào campaign chính có thể chiếm hết spend và phá account.
- Đừng đoán winner bằng cảm tính — kể cả expert đoán sai thường xuyên; định nghĩa "bar 7/10", mọi ad vượt bar rồi để thuật toán chọn.
- Ads Library đối thủ: ad chạy ≥3–6 tháng liên tục gần như chắc chắn có lãi — model cấu trúc, không copy nguyên xi.

---

## 5. METRICS & TRACKING

### Hệ thống đo
- **CAPI + pixel song song (cùng event ID chống duplicate), EMQ ≥6**, kiểm tra Events Manager định kỳ. Dữ liệu conversion sạch = "pixel conditioning"; gửi lead rác về pixel là train máy tìm thêm rác — 1–2 event chất lượng/ngày > 50 conversion rác/tuần.
- Meta under-report 15–50% (recurring, sales cycle dài) → tracker bên thứ 3 (Hyros/Triple Whale) hoặc tối thiểu đối chiếu Shopify/CRM. Chốt "King Goal" duy nhất (CAC/MER/NCPA) và đo blended.
- Incremental attribution (Columns → Compare attribution): 72% incremental conversions của Meta bị gán nhầm kênh khác; spender lớn nên chuyển hẳn sang incremental + conversion lift/geo holdout.

### Đọc số
- Phân đôi metrics: **Primary** (spend, purchases, CPA, ROAS — để ra quyết định) vs **Diagnostics** (frequency, CPM, CTR, hook rate, hold rate — chỉ để giải thích "tại sao"). Không bao giờ tối ưu theo diagnostics; "không có tương quan giữa CPL thấp và CAC thấp — zero".
- **Framework 3 lớp (Camila, $100M spend)**: Spend = confidence score của Meta; Frequency = vị trí phễu (1–1.3 TOF / 1.3–2 MOF / 2+ = retargeting đội lốt winner — scale là chết); Engagement chỉ để chẩn đoán.
- **4PI (Charley)**: Spend / Frequency / CPM / CPR — prospecting tốt = spend cao + freq thấp + CPM thấp + CPR trên TB; red flag = CPR tệ mà vẫn hút spend lớn.
- **GPT (Gross Profit per Transaction) = AOV − CPA** thay ROAS: ROAS 2x có thể lời gấp đôi ROAS 4x. Break-even CPA = AOV × margin (hoặc giá bán − COGS − ship) — mốc so mọi quyết định.
- Custom metrics: Hook rate = 3s plays/impressions (mục tiêu >25–30%); Hold rate = ThruPlays/impressions (~7–12%); dùng link CTR/unique outbound (KHÔNG "clicks all" — chênh 10 lần).
- Benchmark tham khảo: link CTR >1% (ecom >1.5%), LPV/click ≥80%, LPV→ATC ≥10%, ATC→checkout ~50%, checkout→purchase ~50%, opt-in lead magnet 20–30%. Chẩn đoán: CPM cao = targeting/audience; CTR thấp = ad/offer; CTR tốt mà CVR thấp = landing page (congruence, tốc độ, review, phí ship bất ngờ).
- Quy tắc tắt/giữ theo frequency + ROAS: freq >2 & ROAS dưới target → tắt; freq <2 & ROAS dưới target nhưng tổng ad set trên target → GIỮ (top-funnel fuel). Retention curve video theo giây: chỗ dip = đoạn cần sửa.
- "Profit is found, not created": bóc tách campaign lỗ theo tranche/geo — thường có 1 lát cắt đang lời to làm hạt giống scale.

---

## 6. SCALING & NGÂN SÁCH

- Điều kiện scale: CPA ổn định 5–7 ngày + trả lời được "nếu CPA tăng 10–20% ngày mai tôi còn lãi không?". Trước khi tăng budget: tắt ads GPT tệ nhất (không quá 20% spend/ngày) — 9/10 lần vấn đề là cách Meta dùng tiền, không phải thiếu tiền.
- Tốc độ: +20% mỗi 3–5 ngày (hoặc +10%/tuần thận trọng; <$1k/ngày có thể +40%); scale down = nửa tốc độ scale up. Nhảy budget sốc ($20→$300) có thể bị flag account.
- 3 phương pháp (Charley): Linear (+$10–50/ngày bằng automated rules), Fractional (+2%/ngày → 6x trong 90 ngày), Marginal (tăng khi CPA 7 ngày < target). Automated rule "scale baby scale": +10%/ngày khi CPA 14 ngày < target, kèm max cap.
- Chase **profit volume, không chase ROAS %**; tính "willing to pay per customer" từ LTV — cap CPL quá thấp là lý do không scale nổi; tăng AOV (bundle) để trả CAC cao hơn = vũ khí thắng auction.
- Scale bằng chiều rộng: thêm persona/angle/format mở "pocket" audience mới; đa avatar hóa khi spend nghìn đô/ngày ("nếu bạn là athlete…, mẹ bận rộn…"). Weekly frequency account >4 → đừng tăng budget, bơm thêm ads top-funnel kéo frequency về 1–2 trước.
- $100k+/tháng: cost caps/bid caps, day-parting, incremental attribution. Q1 (tháng 1–3) là quý CPM rẻ nhất năm; chủ động descale khi mùa chậm; đừng bật/tắt liên tục — "cách duy nhất mất tiền là stop-start-stop-start".
- Ngân sách khởi điểm: chọn mức "mất được nhưng xót" (không cần đủ 50 conv/tuần mới có kết quả); local $10–20/ngày, ecom ≥$25–30/ngày, Tier-1 ≥$20/ngày; cần tối thiểu 6 tháng runway; daily budget, không lifetime.
- Kênh phụ: Meta là môi trường test creative cho mọi kênh; retargeting toàn nền tảng + PPC own-brand terms gần như luôn dương; email/SMS backend chiếm 30–35% doanh thu cho phép front-end hòa vốn.

---

## 7. SAI LẦM PHỔ BIẾN NHẤT (tần suất nhắc cao)

1. Chỉnh sửa liên tục / panic sau 1–3 ngày → reset learning mãi mãi ("day trading ad account").
2. Tắt ad ROAS thấp trong ad set đang đạt KPI → giết top-funnel fuel, ROAS tổng sụt.
3. Scale ad ROAS cao + frequency 2+ (retargeting trá hình) → chết ngay khi tăng budget.
4. Biến thể nông (đổi màu/headline) tưởng là diversity → bị bundle + phạt CPM.
5. Tối ưu theo CPL/CTR/CPC/hook rate thay vì CAC/ROAS/profit volume.
6. Chọn sai objective/performance goal (Traffic khi muốn sales; maximize leads → lead rác).
7. Volume quá thấp HOẶC volume rác không hệ thống — cả hai đều thua.
8. Phân mảnh budget (20–30 campaigns → 75%+ ngân sách kẹt learning phase).
9. Không exclude khách cũ → Meta đốt budget vào người sẽ mua anyway.
10. Ném concept mới thẳng vào campaign chính đang ổn.
11. Tin mù metrics in-platform / AI assistant của Meta (Manus đọc sai ROAS 14.25 vs 1.76 thực) / opportunity score / recommendations — "trust but verify".
12. Ads hướng doanh nghiệp thay vì khách hàng; ám ảnh ads đẹp; copy nguyên xi đối thủ.
13. Landing page chậm/không khớp ad — 90% nguyên nhân "camp tốt mà không convert".
14. Offer yếu/gimmick — không hack nào cứu nổi; Andromeda "phơi bày" business economics yếu.
15. Đổ lỗi Andromeda cho mọi drop — thường là macro, mùa vụ, đối thủ, hoặc setup của mình.

---

## 8. POLICY & AN TOÀN TÀI KHOẢN

- **Không bao giờ xóa ad bị disapprove** (violation đã log; xóa = giảm trust score) — appeal qua Account Quality (~48h). **Không duplicate ad bị reject** để lách → strike system 4 tầng: shadow-throttle CPM → auto-reject asset → suspend → ban vĩnh viễn.
- Không sửa ad đang active vì lỗi nhỏ (1 ký tự cũng re-trigger review + reset learning).
- Special Ad Categories (BĐS, tín dụng, việc làm, chính trị): bắt buộc khai — không khai là đường nhanh nhất tới disable account, gần như không cứu được.
- Copy cấm: personal attributes ("Are you Christian?", "meet OTHER seniors"), tên riêng, before/after giảm cân + guarantee kết quả, claim chữa bệnh, get-rich-quick, nút play giả. Health/supplement/tài chính: target 18+.
- Landing page cũng bị review (không chặn geo IP, không auto-download, nội dung khớp ad); ad đã duyệt vẫn có thể bị gỡ nếu bị report/hide nhiều; AI review sai → request manual review.
- Hạ tầng chống rủi ro: Business Manager (không chạy trên personal account), nhiều ad account + backup pixel, backup payment method, không login/logout tạo nhiều asset trong thời gian ngắn, warm-up account mới 24h + engagement campaign nhẹ. Meta gần như không có support người thật — kể cả spender $1M/tuần.

---

## 9. ĐIỂM TRANH CÃI GIỮA CÁC NGUỒN (tự test cho account của mình)

| Chủ đề | Phe A | Phe B |
|---|---|---|
| Số ads/ad set | 15–50 ads broad (Ben Heath, Piliero, Jared) | 3–8 ads, "ít mà chất" cho budget nhỏ (Charley 3-2-2, James William, Christian Jamal) |
| Advantage+ audience | Dùng, rẻ hơn tới 33% (Meta, Jamal) | <$100/ngày thì bỏ; original + tắt expansion để kiểm soát (Heath, Nyback, AC Hampton) |
| Volume | Càng nhiều càng tốt (2.000/tháng, Skims 4.800/quý) | Andromeda phạt spam volume; chất lượng + vai trò khác nhau (Charley) — hoà giải: volume CÓ HỆ THỐNG, trên "bar chất lượng" |
| Retargeting riêng | Bỏ hẳn, Meta tự lo (Heath, Zirker) | Vẫn cần swim lanes/broad retargeting khi có trigger event (Piliero, Wes) |
| Kill ad | 21 ngày không đụng (Jamal) | Kill sau 2–3x CPA spend không có kết quả (nhiều nguồn) — hoà giải: theo conversion volume, không theo cảm xúc |
| Hook đánh giá | Hook rate là KPI sản xuất | Hook rate chỉ là diagnostic, CPA là vua (Nick Theriot, Justin Lalonde) |

---

## 10. CHECKLIST HÀNH ĐỘNG NHANH (áp dụng cho dự án)

- [ ] CAPI + pixel cùng event ID, EMQ ≥6; khai Audience Segments (engaged/existing).
- [ ] 1 CBO prospecting broad (exclude purchasers) + 1 campaign retention nhỏ.
- [ ] Batch creative mới theo pack: 3 angle × 5 format, đặt min spend = 1× CPA trong 7 ngày.
- [ ] Mỗi video: 3–5 hook variations (visual khác nhau 3 giây đầu).
- [ ] Tắt enhancements thay đổi bên trong creative + site links + multi-advertiser + related media; recheck hàng tuần.
- [ ] Custom metrics: hook rate, hold rate, GPT (AOV − CPA); dashboard đối chiếu backend.
- [ ] Running board: angle / hook / format / kết quả từng ad.
- [ ] Nhịp: launch thứ 4 → đọc thứ 6 + thứ 2 → quyết định trên 7-day; refresh 20% creative đáy mỗi tuần.
- [ ] Scale +20%/3–5 ngày khi CPA ổn; frequency account >4 → thêm TOF ads trước khi tăng tiền.
- [ ] Research kho ngôn ngữ khách: Reddit, reviews, comments — cập nhật hàng tháng.
