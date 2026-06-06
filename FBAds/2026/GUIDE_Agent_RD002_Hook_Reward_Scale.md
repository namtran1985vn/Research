# GUIDE cho Agent — Áp 3 khám phá RD002 vào Ads Studio App
*(hook clarity · reward "chạm/dùng" · scaling discipline). Chỉ sửa TEXT trong `Sources/Models/Strategy.swift`. Không đụng schema/UI/kiến trúc → an toàn build.*

Đối chiếu code hiện tại (đã đọc):
- Hook spec ở dòng ~303: ép "4 hooks ≤6 words, scroll-stopping" — NHƯNG chưa ép **topic clarity + on-target curiosity** (điểm yếu chính).
- Human element ở dòng ~341: đã có "hands placing/using, feet stepping" — TỐT, chỉ cần nhấn mạnh *để kích reward*.
- `setupGuidance` CHƯA có field/lời khuyên scaling. (Nếu đã làm guide số 2 — thêm field `structure` — thì gộp phần scaling vào đó; nếu chưa, xem mục C.)

---

## A. HOOK = TOPIC CLARITY + ON-TARGET CURIOSITY (quan trọng nhất)
**Vì sao:** RD002 — hook chỉ thắng khi cho 2 thứ: (1) hiểu NGAY về cái gì + cho ai (clarity), (2) tin "dành cho tôi" + tò mò (curiosity). Lỗi #1 = mơ hồ/delay. Hook kiểu "Đẹp mọi góc nhìn" FAIL clarity (về cái gì? cho ai?).

**Sửa:** trong `StrategyPrompt.system`, tại spec `hooks` (dòng ~303), thay đoạn mô tả `hooks` bằng:
```
`hooks` (4 hooks ≤6 words each, best first — EACH must deliver BOTH (1) topic clarity: the \
viewer instantly grasps WHAT it's about and that it's FOR THEM, and (2) on-target curiosity: \
a reason to keep looking. A hook must stand alone WITHOUT the image; reject vague/mood-only \
hooks like "đẹp mọi góc nhìn" that say nothing about the product or the buyer. Lead with the \
concrete subject + a curiosity/benefit twist, e.g. "Phủ sofa khiến khách trầm trồ")
```

**Tùy chọn nhấn thêm** — vào mục `## AVOID these`:
```
- Vague mood-only hooks (no topic clarity, no clear "who it's for") — they read as filler and lose the scroll.
```

---

## B. KÍCH REWARD BẰNG "CHẠM / DÙNG" (nhẹ, đã có nền)
**Vì sao:** RD002 impulse — chỉ cần *thấy mình chạm/dùng* là não bật vùng phần thưởng (dopamine) TRƯỚC khi mua. App đã có "human element"; chỉ cần ghi rõ MỤC ĐÍCH + ưu tiên hành động chạm.

**Sửa:** dòng ~341 (mục HUMAN ELEMENT), nối thêm 1 câu:
```
- HUMAN ELEMENT when it fits (especially ugc / lifestyle / testimonial): hands placing or \
using the product, feet stepping onto it, or a person partly in frame — for relatability and \
attention. PREFER an active touch/use moment (a hand smoothing the throw, feet stepping onto \
the rug): seeing the product touched/used fires the buyer's reward/anticipation before purchase. \
Keep it natural, never a stiff stock pose.
```
*(chỉ thêm câu "PREFER an active touch/use moment … before purchase"; phần còn lại giữ nguyên.)*

---

## C. SCALING & LEARNING-PHASE DISCIPLINE (vào setupGuidance)
**Vì sao:** RD002 — quy tắc vàng: **tăng budget ≤20-30% mỗi 2-3 ngày**, KHÔNG nhảy mạnh; **không sửa 7 ngày đầu** trừ khi cháy; luôn test creative kế thừa trước khi winner fatigue.

**Hai trường hợp:**

**C1 — Nếu ĐÃ làm guide số 2 (đã có field `structure` trong setupGuidance):** chỉ cần nối nội dung scaling vào dòng prompt mô tả `structure` (Step 4). Sửa câu mô tả `structure` thành:
```
- `structure`: post-Andromeda account structure + scaling discipline — ONE broad CBO "Testing" \
campaign for new creatives and ONE broad CBO "Scaling" campaign where proven winners take most \
budget; consolidate, don't fragment. SCALING RULE: raise a winner's budget by at most 20–30% \
every 2–3 days (never double it — big jumps reset learning and kill winners). Don't edit in the \
first ~7 days unless on fire (CPA ≥3× breakeven). Always be testing replacement creatives before \
the current winner fatigues. Brief, product-specific, actionable.
```

**C2 — Nếu CHƯA làm guide số 2:** làm guide số 2 trước (thêm field `structure` đầy đủ: Models.swift + DTO + map + UI), rồi dùng nội dung C1 ở trên cho phần prompt. Xem `GUIDE_Agent_Add_CampaignStructure.md`.

---

## D. (TÙY CHỌN) AESTHETIC "AUTHENTIC > GLOSSY"
**Vì sao:** RD002 — "lofi UGC điện thoại đang đè bẹp video brand bóng bẩy; people don't want to be sold to." App đã có chỉ dẫn ugc=authentic; có thể nhấn thêm 1 dòng ở mục PROVEN FB AD IMAGE CRAFT:
```
- When in doubt, real-and-slightly-imperfect beats glossy-and-staged: authentic phone-shot \
realism out-converts over-polished brand visuals for cold feed traffic.
```

---

## KIỂM THỬ
1. Build phải xanh (toàn sửa text trong 1 string literal → khó vỡ; chú ý giữ dấu `\` nối dòng và `"` escape đúng).
2. Chạy 1 product, soi `hooks`: mỗi hook có nói **rõ sản phẩm/đối tượng** không (không còn kiểu "đẹp mọi góc nhìn" trống rỗng)?
3. Soi `imagePrompts` ugc/lifestyle: có cảnh **tay chạm/chân bước** không?
4. Mở Inspector → mục setup guidance/`structure`: có câu **"+20-30% mỗi 2-3 ngày, không sửa 7 ngày đầu"** không?

## TÓM TẮT
| Mục | Chỗ sửa | Loại |
|--|--|--|
| A Hook clarity | Strategy.swift ~303 + AVOID | text prompt |
| B Reward touch | Strategy.swift ~341 | text prompt (nối 1 câu) |
| C Scaling | Strategy.swift Step 4 `structure` | text prompt (cần field structure từ guide 2) |
| D Authentic | Strategy.swift IMAGE CRAFT | text prompt (tùy chọn) |

Tất cả là sửa text trong system prompt (trừ C cần field `structure` nếu chưa có) → an toàn, không phá tính năng.
