# Guide — Tối Ưu Cách Tạo Persona & Creative Cho Andromeda (chất lượng & giá trị thật)
*Không thêm tính năng. Chỉ nâng chất lượng output của bước sinh persona/creative. Dùng để chỉnh system prompt hiện có.*

---

## VẤN ĐỀ GỐC CẦN SỬA
Prompt hiện tại bắt model **đa dạng theo NHÃN** (chọn distinct emotionAxis / moment / imageStyle / messageStrategy). Nhưng **đa dạng nhãn ≠ đa dạng góc bán hàng**. Model dễ ra 5 creative "khác nhãn nhưng cùng một ý" → nhìn đủ trục mà không công phá, và Andromeda vẫn gộp làm 1.
→ Phải chuyển trọng tâm từ "đa dạng nhãn" sang **đa dạng Ý TƯỞNG BÁN HÀNG + bám chi tiết sản phẩm thật**.

---

## 6 NGUYÊN TẮC TỐI ƯU (đưa vào prompt)

### 1. MỖI CREATIVE = MỘT "BIG IDEA" RIÊNG (quan trọng nhất)
Trước khi chọn nhãn, ép model khai một **big idea**: một *góc nhìn/insight bán hàng cụ thể* tạo cảm giác "à há", không phải format.
- Hai creative trong cùng persona **không bao giờ được trùng big idea**.
- emotionAxis / moment / imageStyle chỉ **phục vụ** big idea, không phải là big idea.
- *Câu nhúng prompt:* "Each creative must lead with a DISTINCT bigIdea — a specific selling insight or 'aha' angle, NOT a format. No two creatives may share a bigIdea. The emotionAxis/moment/imageStyle then SERVE the bigIdea."
> Đây là thứ thật sự tạo đa dạng; nhãn chỉ là hệ quả. Sửa cái này là cải thiện lớn nhất.

### 2. MỘT CREATIVE = MỘT VIỆC (one job)
Creative yếu vì ôm đồm nhiều lợi ích. Ép mỗi ảnh truyền **đúng 1 thông điệp / 1 benefit / 1 emotion / 1 hook**.
- *Câu nhúng:* "Each creative communicates EXACTLY ONE message (one benefit, one emotion, one hook). Never stack multiple selling points in a single creative."
> Người giàu lướt nhanh — 1 ý sắc đánh trúng hơn 5 ý mờ.

### 3. BÁM CHI TIẾT SẢN PHẨM THẬT TỪ ẢNH (chống chung chung)
`productDetail` hiện dễ ra "chất liệu cao cấp" (vô nghĩa). Ép model **trích chi tiết quan sát được trong ảnh đính kèm** và mỗi creative phóng to **một chi tiết KHÁC nhau**.
- *Câu nhúng:* "productDetail MUST reference a SPECIFIC detail visible in the attached photo (exact color, the actual woven pattern, a real stitch/edge/finish) — never generic like 'premium material'. Each creative magnifies a DIFFERENT real detail."
> Chi tiết thật vừa tăng độ tin, vừa là bộ lọc tự nhiên cho người sành (trục 5).

### 4. HOOK PHẢI QUA "SCROLL TEST" (cụ thể, không sáo)
Thêm tiêu chuẩn cho `hooks`: cụ thể / gây tò mò / đi ngược kỳ vọng; **cấm cụm sáo rỗng** ("đẳng cấp", "sang trọng", "chất lượng vượt trội", "nâng tầm không gian"). Mỗi hook phải tự đứng được không cần ảnh.
- *Câu nhúng:* "Every hook must pass the scroll test: concrete, curiosity-inducing, or expectation-violating, and must stand alone WITHOUT the image. BANNED clichés: 'đẳng cấp', 'sang trọng', 'chất lượng vượt trội', 'nâng tầm', and any empty superlative."
> Hook sáo = ngón tay lướt qua = mất tiền ngay giây đầu.

### 5. valueSignal PHẢI "LỌC NGƯỜI" ĐƯỢC (không chỉ là tính từ)
Ép `valueSignal` là thứ **người sành nhận ra / người ham rẻ bỏ qua**: một chi tiết chế tác, một thuật ngữ trong nghề, một dấu hiệu khan hiếm CỤ THỂ. Cấm "giá trị cao", "đáng tiền".
- *Câu nhúng:* "valueSignal must be something an insider recognizes and a bargain-hunter ignores — a specific craftsmanship cue, an industry term, or a concrete scarcity marker. NOT a generic adjective. It silently self-selects high-value buyers (axis 5)."

### 6. TỰ-PHÊ-BÌNH TRƯỚC KHI XUẤT (chống đa dạng giả)
Cuối prompt, thêm bước kiểm tra bắt buộc: model phải tự rà xem 2 creative nào có thể bị Andromeda coi là "cùng một ad" không.
- *Câu nhúng:* "BEFORE output: verify no two creatives within a persona could be merged by Andromeda as 'the same ad' (same core idea / same visual / same offer). If any two are too close, REPLACE one with a genuinely different bigIdea. Diversity must be in the IDEA, not just the labels."
> Đây đúng chỗ Andromeda phạt nặng nhất (gộp ad + tăng CPM).

---

## TỐI ƯU THÊM CHO PERSONA (chất lượng chọn-top)

### 7. CHẤM ĐIỂM PERSONA THEO GIÁ TRỊ THẬT, KHÔNG THEO QUY MÔ
Đảm bảo tiêu chí "purchase value" được ưu tiên đúng — **người ít mà chi mạnh > đám đông chi ít**.
- *Câu nhúng:* "When scoring personas, weight PURCHASE VALUE (ability & willingness to spend, LTV, dopamine-spend tendency) above audience size. A small high-spend segment outranks a large bargain segment."

### 8. MỖI PERSONA PHẢI CÓ "MÂU THUẪN/KHÁT KHAO" RÕ, KHÔNG CHỈ NHÂN KHẨU
Persona mạnh = có tension cảm xúc, không phải "nữ 30-45, thu nhập cao". Ép khai một **khát khao chưa được thoả / nỗi sợ tinh tế** mà sản phẩm chạm tới.
- *Câu nhúng:* "Each persona must articulate ONE specific unmet desire or subtle fear the product resolves — an emotional tension, not just demographics. This tension drives coreEmotion and every creative's bigIdea."

### 9. COVERAGE PHẢI LÀ KHÔNG GIAN Ý TƯỞNG, KHÔNG PHẢI DANH SÁCH NHÃN
Giữ coverage map (tốt), nhưng yêu cầu mỗi mục coverage gắn với một **góc bán hàng**, để creative kế thừa ý chứ không kế thừa nhãn.
- *Câu nhúng:* "Each coverage entry must imply a concrete selling angle, so creatives inherit IDEAS, not just tags."

---

## TỐI ƯU CHO imagePrompt (giữ giá trị + đúng Andromeda)

### 10. AESTHETIC THEO TỆP A/B PHẢI VÀO TỪNG imagePrompt
Tệp A (quiet luxury) và B (new money) hiện chỉ là nhãn phân ad set. Ép **chỉ dẫn thẩm mỹ theo tệp đi thẳng vào imagePrompt** để 2 tệp ra ảnh khác CHẤT, không chỉ khác chữ.
- *Câu nhúng:* "Inject the persona's audience aesthetic into every imagePrompt — A = quiet luxury (muted, minimal, cinematic, restrained); B = aspirational shine (richer contrast, glow, 'worth showing off'). The two buckets must look visibly different in kind, not just in caption."

### 11. imagePrompt MÔ TẢ MỘT KHOẢNH KHẮC, KHÔNG PHẢI MỘT MÓN ĐỒ ĐẶT GIỮA KHUNG
Ảnh công phá cảm xúc khi gợi **một khoảnh khắc/đời sống** (trục 3), không phải product-on-background. Ép imagePrompt dựng một moment cụ thể khớp `moment` đã chọn.
- *Câu nhúng:* "Each imagePrompt must depict a specific MOMENT/scene that matches the creative's `moment` (e.g. late-night relaxed corner, a hosting scene), with the product living naturally inside it — not a product floating on a plain background."

---

## CÁCH ÁP DỤNG
Đây là **chỉ dẫn để chèn vào system prompt** (Step 2/3/4 + đoạn AVOID + đoạn OUTPUT-check). Không cần thêm field bắt buộc; nếu muốn dùng triệt để nguyên tắc #1, có thể thêm 1 field text `bigIdea` cho mỗi creative — nhưng kể cả không thêm field, vẫn nên ép model "khai bigIdea trong phần concept" và tuân thủ.

## CHECKLIST DUYỆT OUTPUT (đọc nhanh 1 persona)
- [ ] 5 creative có 5 **big idea** khác hẳn nhau (không chỉ khác nhãn)?
- [ ] Mỗi creative chỉ 1 thông điệp?
- [ ] Mỗi `productDetail` là chi tiết THẬT khác nhau từ ảnh?
- [ ] Hook nào cũng qua scroll test, không sáo?
- [ ] valueSignal có lọc được người sành/ham rẻ?
- [ ] Không có 2 creative nào Andromeda sẽ gộp làm 1?
- [ ] Persona có tension cảm xúc rõ, không chỉ nhân khẩu?
- [ ] imagePrompt khác chất theo Tệp A/B + dựng một khoảnh khắc?

## 3 LỖI LÀM MẤT GIÁ TRỊ (tránh)
1. Đa dạng nhãn nhưng cùng ý → Andromeda gộp, CPM tăng.
2. productDetail/valueSignal chung chung → mất độ tin & mất bộ lọc người giàu.
3. Hook sáo rỗng → chết ở giây đầu, mọi thứ phía sau vô nghĩa.
