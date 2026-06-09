# SPECS — Mac App "Ad Creative Studio" (FB Ads Winner 2026)
*Bản đặc tả để bàn — CHƯA code.*

Stack đã chốt: **Native macOS (SwiftUI)** · Text: **Claude API (Anthropic)** · Ảnh: **OpenAI GPT-image (gpt-image-1)**.

---

## 1. MỤC TIÊU APP (1 câu)
Input ảnh + mô tả sản phẩm → app dùng prompt chiến lược (đã xây) gọi Claude sinh **persona + ad creative (concept, hook, primary text, headline)** → bấm nút trên từng creative để gọi GPT-image **tạo ảnh quảng cáo** giữ đúng sản phẩm.

## 1b. PHÂN CẤP & ĐIỀU KHIỂN SỐ LƯỢNG (cốt lõi)
Cấu trúc: **Campaign → Persona → Creatives** (1 persona = 1 ad set).
Người dùng **tự nhập 2 con số** ở màn input:
- **Số lượng Persona** (vd 3) — app sẽ chọn ra **đúng TOP-N persona QUAN TRỌNG & GIÁ TRỊ NHẤT** cho sản phẩm, không phải persona ngẫu nhiên.
- **Số Creative mỗi Persona** (vd 5) — app chọn **TOP-M concept mạnh/đã-proven nhất** cho persona đó.

**Quy tắc "chọn top, không rải đều":** app yêu cầu Claude (1) **chấm điểm & xếp hạng** toàn bộ persona tiềm năng theo *giá trị mua (LTV/khả năng chi) + độ khớp sản phẩm + tiềm năng cảm xúc/dopamine*, rồi **chỉ lấy N persona điểm cao nhất**; (2) với mỗi persona, brainstorm nhiều concept rồi **chỉ giữ M concept điểm cao nhất** (theo độ proven + sức công phá cảm xúc + đa dạng để hợp Andromeda). Kèm **lý do vì sao lọt top** cho mỗi persona/creative (để bạn tin và duyệt).

## 2. LUỒNG NGƯỜI DÙNG (user flow)
1. **Nhập sản phẩm:** kéo-thả 1-3 ảnh sản phẩm + điền Tên, Mô tả, (tùy chọn) Giá, Thị trường, Mục tiêu (Sales/Leads), Ngân sách/ngày + **Số Persona (N)** + **Số Creative/Persona (M)**.
2. **Bấm "Phân tích & Tạo chiến lược":** app gửi ảnh + thông tin + N, M + system-prompt (prompt chiến lược) tới Claude → nhận JSON: offer đề xuất, **N persona top** (mỗi persona kèm điểm + lý do lọt top, gắn Tệp A/B), với mỗi persona là **M creative top** (concept, kiểu ảnh, message, hook, highlight, bố cục + image-prompt + lý do chọn), copy (4 primary text + 2-3 headline mỗi persona).
3. **Xem kết quả:** UI hiện Campaign → N Persona (ad set), mỗi persona là danh sách M thẻ creative đã xếp hạng (top trước). Mỗi thẻ: concept, hook, primary text, headline, mô tả ảnh, **badge "vì sao top"**.
4. **Tạo ảnh:** mỗi thẻ có nút **"Tạo ảnh"** → gọi GPT-image với image-prompt (kèm ảnh sản phẩm làm reference) → ảnh hiện ngay trong thẻ. Có nút "Tạo lại", "Lưu ảnh".
5. **Xuất:** nút "Xuất tất cả" → lưu ảnh + bảng copy (.csv) ra 1 folder; hoặc copy từng primary text/headline bằng 1 click.

## 3. MÀN HÌNH (screens) — tổng quan
- **S1 — Input/Project:** form sản phẩm + khu thả ảnh + ô nhập N, M + nút tạo chiến lược. Lưu nhiều project.
- **S2 — Strategy/Result:** 3 cột — sidebar Campaign→Persona | lưới thẻ creative | panel chi tiết. (chi tiết ở §3b)
- **S3 — Creative detail:** ảnh lớn + trình sửa text-on-image + toàn bộ copy + image-prompt (sửa được) + Tạo lại/Lưu.
- **S4 — Settings:** API key Claude + OpenAI (Keychain), chọn model, **concurrency cap** (số ảnh tạo song song tối đa), font/màu mặc định cho text-on-image, thư mục lưu mặc định.

---

# 3b. UI/UX DESIGN BRIEF (phần dành cho designer)

## A. NGUYÊN TẮC THIẾT KẾ
1. **Tốc độ là tính năng số 1.** User làm *hàng chục creative/ngày* để săn winner → mọi thao tác lặp phải ≤ 1-2 click; ưu tiên thao tác hàng loạt (bulk), phím tắt, và phản hồi tức thì. Không có bước thừa.
2. **Native macOS, không phải web port.** Tuân thủ macOS HIG: toolbar chuẩn, sidebar dạng `NavigationSplitView` 3 cột, hỗ trợ Dark/Light, trackpad gestures, phím tắt, menu bar, drag-and-drop hệ thống.
3. **Trạng thái luôn rõ ràng.** Vì chạy song song nhiều API call: mỗi item phải hiện rõ idle / queued / generating / done / error. Không bao giờ để user "đoán app đang làm gì".
4. **Thẩm mỹ "quiet luxury".** Bản thân app phục vụ ads cao cấp → UI nên tinh tế, nhiều khoảng trắng, typography sạch, màu trầm/trung tính, không loè loẹt. App trông "đắt" tạo niềm tin vào output.
5. **Tin tưởng & minh bạch.** App "tự chọn top persona/creative" → phải cho user thấy **vì sao** (điểm số, lý do) để họ tin và duyệt nhanh.

## B. KIẾN TRÚC GIAO DIỆN (layout)
**S2 dùng `NavigationSplitView` 3 cột (đây là màn hình chính, ở đây 80% thời gian):**
- **Cột trái (sidebar ~240px):** danh sách Project ở trên; dưới là cây **Campaign → các Persona** của project đang mở. Mỗi persona: tên, **badge Tệp A/B** (màu khác nhau), **điểm số** (vd ⭐ 92), mini progress ("4/5 ảnh").
- **Cột giữa (content — lưới creative):** lưới thẻ creative của persona đang chọn, **xếp hạng top trước** (rank #1 nổi bật). Đây là khu làm việc chính.
- **Cột phải (inspector ~320px, ẩn/hiện được):** chi tiết creative đang chọn — ảnh lớn, copy, image-prompt sửa được, lý do top.
- **Toolbar trên cùng:** nút "＋ Project mới", "⚡ Tạo tất cả ảnh", thanh tiến độ tổng ("12/20 ảnh"), nút Export, nút Settings.

## C. ANATOMY CỦA THẺ CREATIVE (component quan trọng nhất — thiết kế kỹ)
Mỗi thẻ trong lưới gồm:
- **Khung ảnh 4:5** ở trên: chiếm phần lớn thẻ; là nơi hiện ảnh hoặc placeholder.
- **Badge góc:** `#rank` + điểm; chip **Tệp A/B**; chip **kiểu ảnh** (beauty/UGC/testimonial…).
- **Hook (≤6 từ)** in đậm + 1 dòng concept phụ.
- **Trạng thái:** chip nhỏ (Chưa tạo / Đang xếp hàng / Đang tạo… spinner / Xong / Lỗi ⚠️).
- **Hàng nút (hover hiện hoặc luôn hiện):** **Tạo ảnh** · Tạo lại · Lưu · ♡ Đánh dấu winner · ⓘ Vì sao top.
- **Dưới cùng (thu gọn được):** preview Primary text + Headline + nút Copy nhanh từng cái.
**5 trạng thái thị giác của thẻ** (designer vẽ đủ): (1) chưa có ảnh, (2) đang queue, (3) đang generate (skeleton + spinner), (4) ảnh xong, (5) lỗi (overlay đỏ + nút Thử lại).

## D. MÀN S1 — INPUT (thiết kế để nhập nhanh)
- Khu **drag-drop ảnh sản phẩm** lớn, rõ (1-3 ảnh, có preview thumbnail + xóa).
- Form gọn: Tên*, Mô tả* (textarea), Giá, Thị trường, Mục tiêu (segmented Sales/Leads), Ngân sách/ngày.
- **2 stepper nổi bật:** "Số Persona (N)" [1-6] và "Số Creative/Persona (M)" [3-10], có gợi ý mặc định 3×5 + hiển thị tổng "= 15 creative".
- Nút chính lớn: **"Phân tích & Tạo chiến lược"** (primary, có loading state).
- Tôn trọng: nút mờ đi nếu thiếu field bắt buộc; Enter để submit.

## E. MÀN S2 — KẾT QUẢ & THAO TÁC HÀNG LOẠT
- **Header phân tích (thu gọn được):** Offer được chọn + 2-3 phương án; link "Xem bảng xếp hạng persona" (mở sheet `personaRanking` minh bạch).
- **Streaming:** persona/creative xuất hiện dần khi Claude trả về (skeleton trước, điền sau) — không màn hình trắng chờ.
- **Bulk actions:** "Tạo tất cả ảnh" (toàn campaign) · "Tạo ảnh cho persona này" · chọn nhiều thẻ rồi tạo/lưu/xóa hàng loạt.
- **Thanh tiến độ tổng** luôn thấy khi đang chạy; cho **Hủy cả mẻ**; khu "Ảnh lỗi (n)" gom riêng + nút **Thử lại tất cả**.
- **Lọc/sắp xếp:** theo Tệp A/B, theo điểm, "chỉ winner đã đánh dấu", "chỉ ảnh đã xong".

## F. MÀN S3 — CREATIVE DETAIL + TRÌNH SỬA TEXT-ON-IMAGE
Vì chọn cơ chế (b) — app tự render chữ Việt lên ảnh AI (ảnh AI đã chừa khoảng trống):
- **Canvas ảnh lớn** + **các khối chữ kéo-thả** (Hook, dòng phụ) đã auto-điền từ JSON.
- Panel chỉnh chữ: font (gợi ý sẵn vài font quiet-luxury), cỡ, màu, **từ-highlight** (đổi màu/đậm 1-2 từ), canh lề, đổ bóng nhẹ tùy chọn.
- **Snap vào vùng trống** mà ảnh AI chừa ra; cảnh báo nếu chữ phủ > ngưỡng (giữ < 1/4 diện tích).
- Sửa **image-prompt** + nút **Tạo lại** ngay tại đây; nút **Lưu PNG** (ghép ảnh + chữ thành 1 file 1024×1280).
- Hiện toàn bộ Primary text (ngắn/dài) + Headline + CTA, mỗi cái nút Copy.

## G. HỆ THỐNG TRẠNG THÁI & PHẢN HỒI
- Toast nhẹ cho thành công/lỗi; không popup chặn trừ lỗi nghiêm trọng (key sai, hết quota).
- Empty states có hướng dẫn (chưa có project → CTA tạo mới).
- Lỗi API: thông điệp người-đọc-hiểu + gợi ý xử lý (vd "Hết quota OpenAI — kiểm tra billing").

## H. PHÍM TẮT (cho power user)
⌘N project mới · ⌘↵ chạy chiến lược · ⌘G tạo tất cả ảnh · ⌘R tạo lại thẻ đang chọn · Space xem nhanh ảnh lớn · ⌘E export · ⌘, settings · phím mũi tên di chuyển giữa thẻ.

## I. DELIVERABLE MONG ĐỢI TỪ DESIGNER
1. Wireframe lo-fi 4 màn (S1-S4) + luồng chính.
2. Hi-fi mockup S1, S2 (trạng thái đang-chạy-song-song), S3 (trình sửa text), thẻ creative đủ 5 trạng thái.
3. Design tokens: bảng màu (light/dark), typography scale, spacing, component (thẻ, badge, chip trạng thái, nút).
4. Empty/loading/error states.
5. (tùy chọn) prototype bấm được luồng S1→S2→tạo ảnh.

## J. RÀNG BUỘC & LƯU Ý CHO DESIGN
- Tỉ lệ ảnh hiển thị **4:5 cố định** (1024×1280) — thiết kế lưới quanh tỉ lệ dọc này.
- App có thể hiện **rất nhiều thẻ** (vd 6×10 = 60) → lưới phải cuộn mượt, có thể thu gọn thẻ.
- Mọi text trong app + output là **tiếng Việt**; chừa đủ chỗ cho chữ Việt có dấu (dài hơn tiếng Anh ~15%).
- Chạy song song → cần ngôn ngữ thị giác cho "queued vs generating" khác nhau rõ.

## 4. DỮ LIỆU APP TRẢ VỀ (cấu trúc, để 2 API ăn khớp)
Claude trả **JSON cố định** để app render được. Khung rút gọn (N personas, M creatives mỗi persona):
```
Project
 ├─ offer: { phân tích, 2-3 phương án, offer chọn }
 ├─ personaRanking: [ danh sách persona đã chấm điểm + lý do ]  ← để minh bạch việc chọn top
 ├─ personas: [ N phần tử — đã lọc top ]
 │    ├─ persona: { tên, tệp:"A"|"B", mô tả, giáTrịMua, angle, score, lýDoLọtTop }
 │    ├─ copy: { primaryTexts:[4], headlines:[2-3], cta }
 │    └─ creatives: [ M phần tử — đã xếp hạng, top trước ]
 │         ├─ id, rank, score, lýDoChọn
 │         ├─ concept, kiểuAnh, message, hook(≤6 từ), highlight
 │         ├─ chiTietSanPhamPhongTo
 │         ├─ moTaBoCuc + aesthetic theo tệp
 │         └─ imagePrompt   ← dùng để gọi GPT-image
```
> App truyền N (personaCount) và M (creativesPerPersona) vào prompt; Claude phải xếp hạng rồi chỉ trả đúng N và M phần tử top.
> Vì sao JSON: app cần parse để dựng UI + biết gọi ảnh bằng prompt nào. (Prompt chiến lược của bạn sẽ được "gói" thành system prompt + yêu cầu Claude xuất đúng schema này.)

## 4b. XỬ LÝ ĐA LUỒNG (concurrency) — ƯU TIÊN TỐC ĐỘ
Mục tiêu: làm nhiều creative/ngày, **không ngồi chờ tuần tự**. Nguyên tắc: cái gì độc lập thì chạy song song.

**Chỗ song song được (áp dụng hết):**
- **Tạo ảnh hàng loạt:** N×M ảnh độc lập nhau → chạy **song song nhiều ảnh cùng lúc** (không chờ ảnh này xong mới làm ảnh kia). Có nút **"Tạo tất cả ảnh"** → bung song song toàn campaign; mỗi thẻ có spinner riêng, ảnh nào xong hiện trước.
- **Nhiều project cùng lúc:** đang đợi ảnh project A thì vẫn thao tác/tạo project B được (UI không bị khóa).
- **Tạo lại / biến thể:** bấm "tạo lại" nhiều thẻ cùng lúc, không phải đợi từng cái.
- **Async toàn bộ:** dùng Swift `async/await` + `TaskGroup`; UI luôn mượt (không block main thread), có thể hủy từng tác vụ.

**Giới hạn để không bị nhà cung cấp chặn (rate limit):**
- **Hàng đợi có giới hạn đồng thời (concurrency cap):** vd tối đa 4-6 ảnh chạy song song một lúc (chỉnh trong Settings). Vượt thì xếp hàng, xong cái nào thả cái mới vào — luôn "đầy ống" nhưng không quá tải.
- **Auto-retry + backoff** khi gặp lỗi 429/timeout (thử lại sau, không làm hỏng cả mẻ).
- **Hàng đợi bền:** đóng app/lỗi mạng giữa chừng → mẻ đang chạy được lưu trạng thái, mở lại tiếp tục cái còn thiếu (không làm lại cái đã xong).

**Phần KHÔNG song song (có phụ thuộc):**
- Bước Claude sinh chiến lược phải xong trước (vì nó đẻ ra danh sách creative + image-prompt) → rồi mới bung song song tạo ảnh. Nhưng có thể **stream**: persona/creative nào Claude trả xong trước thì hiện ngay, không đợi cả JSON.

**Trải nghiệm:** thanh tiến độ tổng ("12/20 ảnh xong") + trạng thái từng thẻ; cho phép **hủy cả mẻ** hoặc từng ảnh; ảnh lỗi gom riêng để retry 1 chạm.

## 5. TÍCH HỢP API
**Claude (text):**
- Endpoint Messages API; gửi kèm ảnh (base64) + system prompt (prompt chiến lược) + yêu cầu trả JSON schema ở mục 4.
- Xử lý: streaming hoặc 1 lần; retry khi lỗi; giới hạn token.

**OpenAI GPT-image (gpt-image-1) — KHÓA CỨNG ở bản này, bọc qua lớp `ImageProvider`:**
- Tạo ảnh từ `imagePrompt`. **Quan trọng:** truyền **ảnh sản phẩm làm reference** (images.edit) để giữ họa tiết — app đính ảnh gốc vào request.
- Image-prompt **yêu cầu chừa khoảng trống cho chữ** (không để AI viết text-on-image) → app render chữ Việt sau (mục 6.2).
- Kích thước: gần 4:5 nhất; app tự crop/scale về **1024×1280**.
- Mỗi lần 1 ảnh/creative (1 file riêng, không collage); **gọi song song nhiều ảnh** theo concurrency cap (mục 4b).

## 6. QUYẾT ĐỊNH ĐÃ CHỐT
1. **Ngôn ngữ:** toàn bộ persona, copy, hook, text-on-image bằng **tiếng Việt**.
2. **Chữ tiếng Việt trên ảnh — chọn (b):** GPT-image **chừa khoảng trống** cho vùng chữ (image-prompt yêu cầu "negative space, no text / để trống vùng tiêu đề"), rồi **app tự render text-on-image bằng layer chữ riêng** (Core Text/SwiftUI) → chữ Việt sạch 100%, đúng dấu, đúng font quiet-luxury, chỉnh được vị trí/cỡ/màu. *(Tránh hẳn lỗi sai dấu của AI.)*
   - Hệ quả: app cần **trình sửa text-on-image nhẹ** (kéo thả khối chữ, đổi font/cỡ/màu, canh lề) trên ảnh AI trả về. Hook + từ-highlight đã có sẵn trong JSON nên auto-điền, người dùng chỉ tinh chỉnh.
3. **Nhà cung cấp ảnh — KHÓA CỨNG GPT-image (gpt-image-1) ở bản này.** *Nhưng* code vẫn bọc qua 1 lớp `ImageProvider` mỏng (chỉ 1 implementation) để sau cắm Nano Banana không phải đập kiến trúc — không tốn thêm công ở MVP.
4. **Số persona/creative:** người dùng nhập N, M; app chọn top. Đề nghị giới hạn **N 1-6, M 3-10** (chặn tốn chi phí ngoài ý muốn) — *bạn duyệt con số này?*

5. **Giới hạn số lượng:** N persona **1-6**, M creative/persona **3-10** (chặn chi phí ngoài ý muốn). Mặc định 3×5.

## 6b. CÒN TREO (nhỏ, không chặn thiết kế — để v1.1)
- Badge ước tính chi phí "~X ảnh, ~$Y" trước khi tạo loạt.
- Lưu trữ project local (JSON + ảnh trong folder); đổi tên/nhân bản/lịch sử.

## 7. PHI CHỨC NĂNG
- API key lưu **Keychain**, không hardcode.
- Hoạt động offline-first cho dữ liệu đã tạo; chỉ cần mạng khi gọi API.
- macOS 14+; build bằng Xcode; không cần server (gọi API trực tiếp từ máy).
- Xử lý lỗi rõ ràng (hết quota, key sai, mạng lỗi) + trạng thái loading từng ảnh.

## 8. ĐỀ XUẤT PHẠM VI MVP (bản 1)
Đủ dùng, làm nhanh:
- S1 input + S2 kết quả + nút tạo ảnh từng creative + Settings (API key).
- **Người dùng nhập N persona × M creative; app chọn top quan trọng & giá trị nhất** (kèm lý do). Mặc định gợi ý 3×5.
- 1 nhà cung cấp ảnh: **GPT-image (khóa cứng)**, bọc qua `ImageProvider` để v2 cắm Nano Banana.
- Cơ chế chữ (b): GPT-image chừa chỗ → **app render text-on-image tiếng Việt** (trình sửa chữ nhẹ: font/cỡ/màu/vị trí).
- Xuất ảnh + .csv copy.
- **Có sẵn từ MVP:** tạo ảnh **song song** (concurrency cap chỉnh được) + nút "Tạo tất cả ảnh" + retry ảnh lỗi — vì đây là thứ tiết kiệm thời gian chính khi làm nhiều creative/ngày.
**Để sau (v2):** đa nhà cung cấp ảnh (Nano Banana), ước tính chi phí, lịch sử project, A/B variant, hàng đợi bền qua phiên.

---

## 9. GHI CHÚ BÀN GIAO CHO DESIGNER
- Đây là **product + UX spec**, chưa phải bản code. Designer tập trung **§3b (UI/UX Design Brief)** — phần còn lại là context để hiểu vì sao.
- 2 màn hình quan trọng nhất cần đầu tư: **S2 (kết quả + chạy song song)** và **thẻ creative 5 trạng thái** — đây là nơi user sống cả ngày.
- Tinh thần chủ đạo: **nhanh, rõ trạng thái, thẩm mỹ quiet-luxury.**
- Output strings và mọi nội dung mẫu nên dùng **tiếng Việt thật** (không lorem) để test độ dài có dấu.
