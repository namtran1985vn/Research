# Review — AdsStudioApp (đối chiếu spec + research)

## KẾT LUẬN NGẮN
**Đi đúng hướng, chất lượng cao.** App (~7.5k dòng Swift) thực thi rất sát spec và toàn bộ research: phân cấp Campaign→Persona→Creative, chấm điểm chọn top, **5 trục Andromeda được mã hóa thẳng vào system prompt**, đa luồng có concurrency cap + retry, cơ chế chữ (b) (AI chừa chỗ → app render chữ Việt), giữ họa tiết sản phẩm qua `images/edits`. Có **1 khác biệt vs spec** và vài cơ hội nâng giá trị (không phải lỗi).

---

## ✅ LÀM ĐÚNG (điểm mạnh nổi bật)
1. **5 trục Andromeda nằm trong prompt** — system prompt khai báo rõ "match per-person × per-creative × per-moment, bid on predicted value", và bắt mỗi creative là tổ hợp DISTINCT `(emotionAxis × moment × imageStyle × messageStrategy)`. Đây chính là guide mình viết, đã code hóa.
2. **Coverage map trước creatives** — ép persona khai ≥4 emotion + ≥3 moment trước khi đẻ creative → đảm bảo đa dạng thật, chống "đổi caption". Rất tinh.
3. **valueSignal tách khỏi productDetail** — đúng tinh thần self-selecting + predicted value (trục 5).
4. **setupGuidance** (pixel/CAPI, value rules, lookalike, broad targeting) — đưa cả trục 1 & 5 vào output, không bỏ quên.
5. **Giữ sản phẩm:** dùng `images/edits` + `fidelitySuffix` ép "reproduce exactly… patterns/textures/engravings/logos". imagePrompt luôn kết "No text, no words, no logos. 4:5 vertical" → khớp cơ chế (b).
6. **Đa luồng chuẩn:** concurrency cap, exponential backoff khi 429, cancel, jitter, pump queue. Đúng nhu cầu "làm nhiều creative/ngày".
7. **4 biến thể mỗi hook/headline/primary/imagePrompt** — vượt spec, cho bạn nhiều đạn để test winner. Tốt.
8. **Chống lỗi JSON:** decode chịu lỗi (singular fallback, lọc persona well-formed, backfill thiếu) — thực dụng, ít vỡ.
9. **primaryText bắt 1-3 câu, mở bằng hook, đào sâu cảm xúc** — đúng hướng bán cảm xúc/dopamine.

## ⚠️ KHÁC BIỆT vs SPEC (cần bạn biết, không hẳn lỗi)
1. **Text engine = OpenAI GPT, KHÔNG phải Claude.** Spec & lựa chọn ban đầu của bạn là Claude cho text. App đã chuyển sang "OpenAI-only, 1 key cho cả text + ảnh". → Đơn giản hơn (1 key), nhưng **chất lượng chiến lược/tiếng Việt của Claude thường nhỉnh hơn cho loại task dài, nhiều sắc thái này**. *Quyết định: giữ OpenAI cho gọn, hay thêm tùy chọn Claude cho bước strategy?* (Khuyến nghị: thêm Claude như provider tùy chọn — strategy là "bộ não", đáng đầu tư.)
2. **Secrets.swift cho hardcode key** — tiện cho 1 người, nhưng rủi ro nếu lỡ commit/zip chia sẻ. Đảm bảo .gitignore + mặc định dùng Keychain.

---

## 🚀 ĐỀ XUẤT HIGH-VALUE (xếp theo lợi ích/đỗ công)

### Bậc 1 — Đáng làm sớm (đòn bẩy lớn cho việc săn winner)
1. **Provider chọn được cho Strategy (OpenAI ↔ Claude).** "Bộ não" quyết định chất lượng toàn bộ output. ImageProvider đã tách lớp rồi — làm tương tự cho StrategyProvider, thêm Claude. Tiếng Việt + reasoning dài thường tốt hơn.
2. **Đánh dấu Winner + ghi kết quả thật (CTR/ROAS) ngược vào app.** Cả research nhấn "test để tìm 6% ad ăn tiền". Cho phép tag ảnh đã chạy + nhập số liệu → lần regenerate sau, feed lại cho prompt ("đây là concept đã thắng/thua") để model học theo winner. Đây là vòng lặp đẻ-winner mà transcript nói tới.
3. **Batch nhiều SẢN PHẨM = nhiều campaign trong 1 app.** Bạn có thảm/gối/phủ sofa/runner. Cho tạo nhiều project song song + dashboard tổng. Khớp câu hỏi tổ chức camp của bạn (1 sp = 1 camp).
4. **Kiểm tra ngân sách → gợi số ad set.** App đang cho N tự do; thêm trường "ngân sách/ngày + CPA mục tiêu" → cảnh báo nếu N ad set sẽ kẹt learning (công thức `CPA×50÷7`). Tránh bạn mở 6 persona mà ngân sách chỉ nuôi nổi 2.

### Bậc 2 — Tăng chất lượng đầu ra
5. **Tệp A/B điều khiển aesthetic ảnh, không chỉ gắn nhãn.** Hiện audience A/B có trong JSON; nên **bơm chỉ dẫn aesthetic theo tệp vào imagePrompt** (A=quiet luxury trầm/tối giản; B=rực rỡ/khoe). Để 2 tệp ra ảnh khác chất rõ rệt.
6. **Preset "loại sản phẩm".** Nội thất/decor có concept ăn khách riêng (lifestyle in-context, before/after không gian, flat-lay bộ). Cho chọn category → prompt thêm gợi ý concept hợp ngành.
7. **Xuất chuẩn Meta:** ngoài PNG + csv, xuất gói sẵn sàng up (đặt tên theo Camp/Persona/rank, kèm primary+headline ghép từng ảnh) để bạn import nhanh vào Ads Manager.
8. **Variant cho text-on-image (4 hook đã có) → xuất nhiều bản 1 ảnh** với hook khác nhau = thêm đạn test gần như miễn phí (cùng nền, khác chữ — nhưng lưu ý: Andromeda coi là gần giống, nên đây là biến thể nhẹ, không thay cho đa dạng concept).

### Bậc 3 — Nâng cao
9. **Cắm Nano Banana / Seedream làm ImageProvider thứ 2** (giữ họa tiết tốt hơn GPT-image, đặc biệt logo/hoa văn nhỏ — đúng điểm yếu bạn lo). Kiến trúc đã sẵn `ImageProvider`.
10. **Ước tính chi phí trước khi "Generate all"** (N×M×4 ảnh có thể tốn nhiều) — badge "~X ảnh ~$Y".
11. **Lưu lịch sử version mỗi project** để so sánh các lần regenerate.

---

## CỜ ĐỎ / KIỂM TRA TRƯỚC KHI CHẠY THẬT
- **gpt-image-1 giữ logo/chữ in trên sản phẩm tới đâu?** Đây là rủi ro lớn nhất với hàng có hoa văn (thảm Ba Tư, runner). Test 5 ảnh thật trước; nếu lệch → ưu tiên đề xuất #9 (Nano Banana).
- **Chi phí thật:** N=6 × M=10 × 4 imagePrompt = lý thuyết tới 240 ảnh/lần — kiểm soát bằng cảnh báo chi phí (#10).
- **Tiếng Việt trên ảnh:** đã giải đúng (app tự render, không để AI viết) — giữ nguyên hướng này.
- **Đừng để hardcode key lọt ra ngoài** khi chia sẻ zip.

---

## TÓM 1 DÒNG
App đúng hướng và thực thi tốt hơn mong đợi; ưu tiên 4 việc: **(1) thêm Claude cho strategy, (2) vòng lặp winner-feedback, (3) multi-product campaigns, (4) cảnh báo ngân sách/learning** — đây là chỗ tạo ra nhiều winner nhất với ít công nhất.
