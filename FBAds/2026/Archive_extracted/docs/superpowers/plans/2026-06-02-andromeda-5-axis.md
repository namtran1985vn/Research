# Andromeda 5-Axis Creative Strategy — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the generation brain produce ad-set creative that explicitly covers Andromeda's 5 intersecting axes (person, emotion, moment, creative resonance, predicted value), enforced by a persona-scoped plan-then-fill prompt and surfaced in the Inspector.

**Architecture:** Each persona declares its emotional lens + a coverage map (distinct emotions/moments) *before* its M creatives are written, so the JSON generation order itself prevents emotion collapse. Each creative carries 4 axis tags. The campaign carries AI-tailored setup guidance for the campaign-side axes (1 & 5). All new fields decode tolerantly so old projects keep loading.

**Tech Stack:** Swift 5 / SwiftUI / macOS 14, built with XcodeGen + xcodebuild. No test target — verification is compile success (`** BUILD SUCCEEDED **`) plus a manual generation check at the end.

**Reference spec:** `docs/superpowers/specs/2026-06-02-andromeda-5-axis-design.md`

**Build/verify command (used by every task):**
```sh
xcodebuild -project AdCreativeStudio.xcodeproj -scheme AdCreativeStudio -configuration Debug build 2>&1 | tail -5
```
Expected last line: `** BUILD SUCCEEDED **`

---

## Task 1: Value types + model fields (Models.swift)

**Files:**
- Modify: `Sources/Models/Models.swift`

- [ ] **Step 1: Add `Coverage` and `SetupGuidance` value types**

Insert after the `Offer` struct (after line 102, before `RankingEntry`):

```swift
/// Per-persona diversity space (axis 2 & 3): the distinct emotional axes and
/// moments/contexts this persona's creatives are meant to span. AI-derived from
/// the product + target customers; not a fixed enum.
struct Coverage: Codable, Hashable {
    var emotions: [String] = []
    var moments: [String] = []
}

/// Campaign-side reminders for the axes the app does NOT execute (axis 1 person,
/// axis 5 predicted value). AI-tailored per campaign; reference text only.
struct SetupGuidance: Codable, Hashable {
    var pixelCapi: String = ""
    var valueRules: String = ""
    var lookalike: String = ""
    var targeting: String = ""
}
```

- [ ] **Step 2: Add `setupGuidance` to `Project`**

In `struct Project` add the property right after `var offer: Offer` (line 21):

```swift
    var offer: Offer
    var setupGuidance: SetupGuidance? = nil
```

And add `setupGuidance` to `Project.CodingKeys` (line 32-34):

```swift
    enum CodingKeys: String, CodingKey {
        case id, name, product, personaCount, creativesPerPersona, offer, setupGuidance, ranking, personas, createdAt, updatedAt
    }
```

- [ ] **Step 3: Add lens + coverage fields to `Persona`**

Replace the `Persona` struct (lines 113-124) with:

```swift
struct Persona: Identifiable, Codable, Hashable {
    var id: UUID = UUID()
    var name: String
    var audience: String             // "A" | "B"
    var score: Int
    var ltv: String
    var angle: String
    var desc: String
    var reasonTop: String
    var coreEmotion: String = ""     // §II.3 — core emotion driving the purchase
    var selfImage: String = ""       // §II.5 — who they want to become when buying
    var psychLever: String = ""      // §II.6 — main psychological lever(s)
    var coverage: Coverage = Coverage()  // axes 2 & 3 — what this persona spans
    var copy: CopyBlock
    var creatives: [Creative]
}

// Tolerant Codable so older saved projects (no lens/coverage) keep loading.
extension Persona {
    enum CodingKeys: String, CodingKey {
        case id, name, audience, score, ltv, angle, desc, reasonTop
        case coreEmotion, selfImage, psychLever, coverage, copy, creatives
    }
    init(from d: Decoder) throws {
        let c = try d.container(keyedBy: CodingKeys.self)
        id = (try? c.decode(UUID.self, forKey: .id)) ?? UUID()
        name = (try? c.decode(String.self, forKey: .name)) ?? ""
        audience = (try? c.decode(String.self, forKey: .audience)) ?? "A"
        score = (try? c.decode(Int.self, forKey: .score)) ?? 0
        ltv = (try? c.decode(String.self, forKey: .ltv)) ?? ""
        angle = (try? c.decode(String.self, forKey: .angle)) ?? ""
        desc = (try? c.decode(String.self, forKey: .desc)) ?? ""
        reasonTop = (try? c.decode(String.self, forKey: .reasonTop)) ?? ""
        coreEmotion = (try? c.decode(String.self, forKey: .coreEmotion)) ?? ""
        selfImage = (try? c.decode(String.self, forKey: .selfImage)) ?? ""
        psychLever = (try? c.decode(String.self, forKey: .psychLever)) ?? ""
        coverage = (try? c.decode(Coverage.self, forKey: .coverage)) ?? Coverage()
        copy = (try? c.decode(CopyBlock.self, forKey: .copy)) ?? CopyBlock(primaryTexts: [], headlines: [], cta: "")
        creatives = (try? c.decode([Creative].self, forKey: .creatives)) ?? []
    }
}
```

Note: defining `init(from:)` in an extension keeps the synthesized memberwise
initializer available (same pattern as `Creative`), so `Persona(name:…)` call
sites still compile. The new stored properties have defaults, so existing call
sites that omit them still compile.

- [ ] **Step 4: Add the 4 axis tags to `Creative`**

In `struct Creative`, add after `var reasonTop: String` (line 141):

```swift
    var reasonTop: String

    // Andromeda axis tags (set by the strategy brain; empty on legacy projects).
    var emotionAxis: String = ""      // axis 2 — emotion this creative fires
    var moment: String = ""           // axis 3 — moment/context it targets
    var messageStrategy: String = ""  // pain | proof | transformation | objection | desire
    var valueSignal: String = ""      // axis 5 — self-pricing-high cue (distinct from productDetail)
```

Add the keys to `Creative.CodingKeys` (line 226-231). Change the first `case`
line to include them:

```swift
        case id, rank, score, style, concept, message, productDetail, layout, reasonTop
        case emotionAxis, moment, messageStrategy, valueSignal
```

And in `Creative.init(from:)` add, right after the `reasonTop` decode line (line 243):

```swift
        reasonTop = (try? c.decode(String.self, forKey: .reasonTop)) ?? ""
        emotionAxis = (try? c.decode(String.self, forKey: .emotionAxis)) ?? ""
        moment = (try? c.decode(String.self, forKey: .moment)) ?? ""
        messageStrategy = (try? c.decode(String.self, forKey: .messageStrategy)) ?? ""
        valueSignal = (try? c.decode(String.self, forKey: .valueSignal)) ?? ""
```

- [ ] **Step 5: Build**

Run the build/verify command. Expected: `** BUILD SUCCEEDED **`.
(`makePersona`/`makeProject` still compile — they don't reference the new fields yet.)

- [ ] **Step 6: Commit**

```sh
git add Sources/Models/Models.swift
git commit -m "Add 5-axis model fields: Coverage, SetupGuidance, persona lens, creative tags"
```

---

## Task 2: Strategy DTOs (Strategy.swift)

**Files:**
- Modify: `Sources/Models/Strategy.swift`

- [ ] **Step 1: Add `CoverageDTO` and `SetupGuidanceDTO`**

Inside `struct StrategyResponse`, after the `CreativeDTO` struct closes (after line 71, before the closing brace of `StrategyResponse` on line 72), add:

```swift
    struct CoverageDTO: Decodable {
        let emotions: [String]; let moments: [String]
        static let empty = CoverageDTO(emotions: [], moments: [])
        init(emotions: [String], moments: [String]) { self.emotions = emotions; self.moments = moments }
        enum CodingKeys: String, CodingKey { case emotions, moments }
        init(from d: Decoder) throws {
            let c = try d.container(keyedBy: CodingKeys.self)
            emotions = (try? c.decode([String].self, forKey: .emotions)) ?? []
            moments = (try? c.decode([String].self, forKey: .moments)) ?? []
        }
    }
    struct SetupGuidanceDTO: Decodable {
        let pixelCapi: String; let valueRules: String; let lookalike: String; let targeting: String
        enum CodingKeys: String, CodingKey { case pixelCapi, valueRules, lookalike, targeting }
        init(from d: Decoder) throws {
            let c = try d.container(keyedBy: CodingKeys.self)
            pixelCapi = (try? c.decode(String.self, forKey: .pixelCapi)) ?? ""
            valueRules = (try? c.decode(String.self, forKey: .valueRules)) ?? ""
            lookalike = (try? c.decode(String.self, forKey: .lookalike)) ?? ""
            targeting = (try? c.decode(String.self, forKey: .targeting)) ?? ""
        }
    }
```

- [ ] **Step 2: Add `setupGuidance` to `StrategyResponse`**

Change the top of `struct StrategyResponse` (lines 21-24) to add an optional
`setupGuidance` (optional → synthesized decode tolerates the model omitting it):

```swift
struct StrategyResponse: Decodable {
    let offer: OfferDTO
    let setupGuidance: SetupGuidanceDTO?
    let personaRanking: [RankingDTO]
    let personas: [PersonaDTO]
```

- [ ] **Step 3: Add lens + coverage to `PersonaDTO`**

Replace `struct PersonaDTO` (lines 30-34) with a tolerant version:

```swift
    struct PersonaDTO: Decodable {
        let name: String; let audience: String; let score: Int; let ltv: String
        let angle: String; let description: String; let reasonTop: String
        let coreEmotion: String; let selfImage: String; let psychLever: String
        let coverage: CoverageDTO
        let copy: CopyDTO; let creatives: [CreativeDTO]

        enum CodingKeys: String, CodingKey {
            case name, audience, score, ltv, angle, description, reasonTop
            case coreEmotion, selfImage, psychLever, coverage, copy, creatives
        }
        init(from d: Decoder) throws {
            let c = try d.container(keyedBy: CodingKeys.self)
            name = (try? c.decode(String.self, forKey: .name)) ?? ""
            audience = (try? c.decode(String.self, forKey: .audience)) ?? "A"
            score = (try? c.decode(Int.self, forKey: .score)) ?? 0
            ltv = (try? c.decode(String.self, forKey: .ltv)) ?? ""
            angle = (try? c.decode(String.self, forKey: .angle)) ?? ""
            description = (try? c.decode(String.self, forKey: .description)) ?? ""
            reasonTop = (try? c.decode(String.self, forKey: .reasonTop)) ?? ""
            coreEmotion = (try? c.decode(String.self, forKey: .coreEmotion)) ?? ""
            selfImage = (try? c.decode(String.self, forKey: .selfImage)) ?? ""
            psychLever = (try? c.decode(String.self, forKey: .psychLever)) ?? ""
            coverage = (try? c.decode(CoverageDTO.self, forKey: .coverage)) ?? .empty
            copy = (try? c.decode(CopyDTO.self, forKey: .copy)) ?? CopyDTO(primaryTexts: [], headlines: [], cta: "")
            creatives = (try? c.decode([CreativeDTO].self, forKey: .creatives)) ?? []
        }
    }
```

- [ ] **Step 4: Add the 4 tags to `CreativeDTO`**

In `struct CreativeDTO`, add the stored properties after `let reasonTop` (line 39):

```swift
        let productDetail: String; let layout: String; let reasonTop: String
        let emotionAxis: String; let moment: String; let messageStrategy: String; let valueSignal: String
```

Add to its `CodingKeys` (lines 44-48) — extend the first `case` line:

```swift
        enum CodingKeys: String, CodingKey {
            case rank, score, imageStyle, concept, message, productDetail, layout, reasonTop
            case emotionAxis, moment, messageStrategy, valueSignal
            case hooks, highlights, headlines, primaryTexts, imagePrompts
            case hook, highlight, headline, primaryText, imagePrompt   // singular fallbacks
        }
```

In `CreativeDTO.init(from:)` add after the `reasonTop` decode line (line 58):

```swift
            reasonTop = (try? c.decode(String.self, forKey: .reasonTop)) ?? ""
            emotionAxis = (try? c.decode(String.self, forKey: .emotionAxis)) ?? ""
            moment = (try? c.decode(String.self, forKey: .moment)) ?? ""
            messageStrategy = (try? c.decode(String.self, forKey: .messageStrategy)) ?? ""
            valueSignal = (try? c.decode(String.self, forKey: .valueSignal)) ?? ""
```

- [ ] **Step 5: Build**

Run the build/verify command. Expected: `** BUILD SUCCEEDED **`.
(Mapping still compiles — it doesn't use the new DTO fields yet.)

- [ ] **Step 6: Commit**

```sh
git add Sources/Models/Strategy.swift
git commit -m "Add 5-axis DTO fields: coverage, lens, creative tags, setupGuidance"
```

---

## Task 3: Map DTOs → models (Strategy.swift)

**Files:**
- Modify: `Sources/Models/Strategy.swift`

- [ ] **Step 1: Thread `setupGuidance` into `makeProject`**

In `makeProject` (lines 76-96), build the guidance and pass it. Insert before
`return Project(` (line 84):

```swift
        let sg = setupGuidance.map {
            SetupGuidance(pixelCapi: CopyText.clean($0.pixelCapi),
                          valueRules: CopyText.clean($0.valueRules),
                          lookalike: CopyText.clean($0.lookalike),
                          targeting: CopyText.clean($0.targeting))
        }
```

Then in the `Project(...)` initializer add the argument right after `product: product,`:

```swift
        return Project(
            name: campaignName,
            product: product,
            setupGuidance: sg,
            personaCount: n,
```

Note: Swift's synthesized memberwise initializer is POSITIONAL — arguments must
appear in declaration order. Since `setupGuidance` is declared right after
`offer`, the call must place `setupGuidance:` immediately after the `offer:`
argument (not after `product:`). Defaulted params like `id`/`createdAt` may still
be omitted, but the ones you pass must stay in order.

- [ ] **Step 2: Map lens + coverage in `makePersona`**

In `PersonaDTO.makePersona` (lines 111-137), add the lens/coverage arguments to
the `Persona(...)` initializer. Change the init head (lines 112-116) to:

```swift
        Persona(
            name: name,
            audience: StrategyResponse.normalize(audience: audience),
            score: score, ltv: ltv, angle: angle, desc: description, reasonTop: reasonTop,
            coreEmotion: CopyText.clean(coreEmotion),
            selfImage: CopyText.clean(selfImage),
            psychLever: CopyText.clean(psychLever),
            coverage: Coverage(emotions: coverage.emotions.map(CopyText.clean),
                               moments: coverage.moments.map(CopyText.clean)),
            copy: CopyBlock(primaryTexts: copy.primaryTexts, headlines: copy.headlines, cta: copy.cta),
```

- [ ] **Step 3: Map the 4 tags onto each `Creative`**

In the same `makePersona`, inside the `creatives.prefix(m).enumerated().map`
closure, after `cr.ratio = ratio` (line 132) add:

```swift
                cr.ratio = ratio   // seed the user's default aspect ratio (Settings)
                cr.emotionAxis = CopyText.clean(c.emotionAxis)
                cr.moment = CopyText.clean(c.moment)
                cr.messageStrategy = CopyText.clean(c.messageStrategy)
                cr.valueSignal = CopyText.clean(c.valueSignal)
```

- [ ] **Step 4: Build**

Run the build/verify command. Expected: `** BUILD SUCCEEDED **`.

- [ ] **Step 5: Commit**

```sh
git add Sources/Models/Strategy.swift
git commit -m "Map 5-axis DTO fields onto Persona/Creative/Project"
```

---

## Task 4: Plan-then-fill system prompt (Strategy.swift)

**Files:**
- Modify: `Sources/Models/Strategy.swift` — `StrategyPrompt.system` (lines 145-213)

- [ ] **Step 1: Replace the system prompt body**

Replace the entire returned string literal in `static func system(n:m:language:)`
(the `"""…"""` block, lines 146-212) with:

```swift
        """
        You are a world-class direct-response performance marketer specializing in winning \
        Facebook/Meta ad creatives (Andromeda-era). You receive a product (photos + details) \
        and must produce a complete, ranked creative strategy.

        # MENTAL MODEL — Andromeda matches PER-PERSON × PER-CREATIVE × PER-MOMENT and bids on \
        predicted value. You do NOT pick audiences; you give Andromeda diverse, resonant creative \
        + clean value signals so it can find more winning intersections. Cover these 5 axes:
        1. Person — handled by broad targeting (out of your hands).
        2. Emotion/intent — you SUGGEST it via each creative's emotional angle.
        3. Moment/context — you SUGGEST it via the moment each creative targets.
        4. Creative resonance — fully yours: diverse concepts/formats.
        5. Predicted value — you STEER it via "value signals" in creative + campaign setup guidance.

        # REFERENCE FRAME (adapt to THIS product — these are inspiration, NOT a closed list; \
        you may coin product-specific axes, written in \(language)):
        - Emotional levers: self-reward/indulgence; craving & anticipation/scarcity; being admired/\
        showing off; quiet luxury/refined taste; pure aesthetics; comfort/coziness; self-expression/\
        identity; craftsmanship/heritage; Diderot/complete-the-look.
        - Moments: late-night relaxed scroll; just got paid/celebrating; decorating the home; \
        before an event/hosting; researching & comparing; aimless entertainment scroll.
        - Message strategies: pain, proof, transformation, objection, desire.

        # YOUR JOB
        Structure: Campaign → Persona (= one ad set) → Creatives.
        The user asked for the TOP \(n) personas and the TOP \(m) creatives per persona.
        Do NOT spread evenly or pick at random — RANK, then KEEP ONLY THE BEST.

        ## Step 1 — Persona ranking (transparency)
        Brainstorm 6–8 plausible buyer personas. Score each 0–100 on:
        purchase value (LTV / ability & willingness to spend) + product fit + emotional/dopamine pull.
        Return ALL of them in `personaRanking` (picked:true for the top \(n), false otherwise),
        each with a one-line `why`. Then output ONLY the top \(n) in `personas`.

        ## Step 2 — Per persona: declare the LENS, then the COVERAGE MAP (do this BEFORE creatives)
        Derive from the product + target customers:
        - `coreEmotion`: the core emotion driving THIS persona's purchase.
        - `selfImage`: who they want to become when they buy this.
        - `psychLever`: the 1–2 main psychological levers (from the frame above).
        Then declare `coverage` — the diversity space this persona's creatives WILL span:
        - `coverage.emotions`: ≥4 DISTINCT emotional axes (or \(m) if \(m) < 4).
        - `coverage.moments`: ≥3 DISTINCT moments/contexts (or \(m) if \(m) < 3).
        Also write an offer-aligned `angle`, a vivid `description`, `ltv`, and `reasonTop`.
        Provide `copy`: exactly 4 `primaryTexts` (mix of short & long), 2–3 `headlines`, one `cta`.

        ## Step 3 — Creatives per persona (FILL the coverage map — each a DIFFERENT cell)
        Produce the TOP \(m) creatives, ranked 1..\(m), best first, each with `score` and `reasonTop`.
        Every creative is a DISTINCT combination of (emotionAxis × moment × imageStyle × messageStrategy):
        - `emotionAxis`: pick ONE from this persona's `coverage.emotions`.
        - `moment`: pick ONE from this persona's `coverage.moments`.
        - `imageStyle`: one of {beauty, ugc, testimonial, lifestyle, studio}.
        - `messageStrategy`: one of {pain, proof, transformation, objection, desire} (label in \(language)).
        Across the \(m) creatives: use at least min(\(m),4) DISTINCT emotionAxis values, min(\(m),3) \
        DISTINCT moments, min(\(m),4) DISTINCT imageStyles, and min(\(m),3) DISTINCT messageStrategies.
        Each creative also needs: `concept`, `message`, `productDetail` (what to keep sharp/accurate), \
        `layout`, and `valueSignal` — a "self-pricing-high" cue (a premium detail / insider language / \
        exclusivity) that attracts value buyers and repels bargain hunters. `valueSignal` is SEPARATE \
        from `productDetail`.
        For each creative provide EXACTLY 4 strong, DISTINCT variants of each: `hooks` (4 hooks ≤6 \
        words each, best first), `highlights` (4 — the 1–2 word phrase inside the corresponding hook \
        to emphasize, same order as `hooks`), `headlines` (4 short headlines, best first), \
        `primaryTexts` (4 variants — EACH 1 to 3 sentences, never a single short line; open with a \
        scroll-stopping hook, go deep emotionally, hit the buyer's psychology / pain / desire), and \
        `imagePrompts` (4 different image directions, best first — each a complete prompt that keeps \
        the real product accurate and ends with "No text, no words, no logos. 4:5 vertical.").

        ## Step 4 — Campaign `setupGuidance` (axes 1 & 5, outside the creative; tailor to THIS product)
        - `pixelCapi`: how to keep Pixel/CAPI clean so Andromeda learns who creates value.
        - `valueRules`: which LTV segment to bias bids toward.
        - `lookalike`: which seed audience + percentile (e.g. top 10–14% LTV) to build the lookalike from.
        - `targeting`: how to keep targeting broad / Advantage+ (no narrow interest squeezing).

        ## AVOID these (they destroy the intersection):
        - Repeating one concept with only the caption changed (Andromeda merges them → CPM rises).
        - Every creative on the same emotion (misses buyers in other moods).
        - A cheap/discount/"shock sale" aesthetic (attracts the wrong people, low predicted value).

        ## imagePrompt rules (CRITICAL)
        The image generator must NOT write any text. Always require clean negative space where the \
        headline will be rendered later by the app. End every imagePrompt with: \
        "No text, no words, no logos. 4:5 vertical." Keep the real product accurate (it is attached \
        as a reference image).

        # LANGUAGE
        Write ALL human-readable content (persona names, descriptions, copy, hooks, headlines, \
        reasons, offer text, coreEmotion, selfImage, psychLever, coverage entries, emotionAxis, \
        moment, messageStrategy, valueSignal, setupGuidance) in \(language). Keep `imageStyle` slugs \
        and JSON keys in English. imagePrompts should be in English (image models perform best in English).

        # OUTPUT
        Return ONLY a single JSON object, no markdown fences, no commentary, matching exactly:
        {
          "offer": { "chosen": string, "rationale": string, "alternatives": [string, string] },
          "setupGuidance": { "pixelCapi": string, "valueRules": string, "lookalike": string, "targeting": string },
          "personaRanking": [ { "name": string, "audience": "A"|"B", "score": int, "picked": bool, "why": string } ],
          "personas": [ {
            "name": string, "audience": "A"|"B", "score": int, "ltv": string, "angle": string,
            "description": string, "reasonTop": string,
            "coreEmotion": string, "selfImage": string, "psychLever": string,
            "coverage": { "emotions": [string], "moments": [string] },
            "copy": { "primaryTexts": [string,string,string,string], "headlines": [string], "cta": string },
            "creatives": [ {
              "rank": int, "score": int, "imageStyle": string, "concept": string, "message": string,
              "productDetail": string, "layout": string, "reasonTop": string,
              "emotionAxis": string, "moment": string, "messageStrategy": string, "valueSignal": string,
              "hooks": [string, string, string, string],
              "highlights": [string, string, string, string],
              "headlines": [string, string, string, string],
              "primaryTexts": [string, string, string, string],
              "imagePrompts": [string, string, string, string]
            } ]
          } ]
        }
        `personas` must contain exactly \(n) items; each `creatives` exactly \(m) items.
        `audience` assigns each persona to ad-set bucket A or B for A/B structure.
        In the JSON, emit each persona's `coverage` BEFORE its `creatives`.
        """
```

- [ ] **Step 2: Build**

Run the build/verify command. Expected: `** BUILD SUCCEEDED **`.

- [ ] **Step 3: Commit**

```sh
git add Sources/Models/Strategy.swift
git commit -m "Rewrite system prompt: plan-then-fill 5-axis coverage + setup guidance"
```

---

## Task 5: Add-one-persona path (OpenAIStrategyClient.swift)

**Files:**
- Modify: `Sources/Generation/OpenAIStrategyClient.swift` — `generatePersona` (lines 82-145)

- [ ] **Step 1: Update the `generatePersona` system prompt + JSON contract**

Replace the `system` string literal (lines 85-100) with:

```swift
        let system = """
        You are a world-class direct-response Facebook/Meta ads strategist. Generate ONE additional \
        buyer persona for the product, fully consistent with the existing campaign and offer. Write \
        ALL human-readable content in \(language). Make it DISTINCT from the existing personas.
        First declare the persona's lens — `coreEmotion` (the emotion driving their purchase), \
        `selfImage` (who they want to become), `psychLever` (1–2 main levers) — then a `coverage` map \
        (`emotions`: ≥4 distinct emotional axes, `moments`: ≥3 distinct moments; or \(m) if \(m) is smaller). \
        These are derived from the product + target customers (not a fixed list), written in \(language).
        Then provide exactly \(m) ranked creatives (best first), each a DISTINCT combination of \
        (emotionAxis × moment × imageStyle × messageStrategy): `emotionAxis` from coverage.emotions, \
        `moment` from coverage.moments, `messageStrategy` ∈ {pain, proof, transformation, objection, \
        desire} (label in \(language)), `imageStyle` ∈ {beauty, ugc, testimonial, lifestyle, studio}, \
        and a `valueSignal` (a self-pricing-high cue that attracts value buyers, separate from \
        productDetail). For EACH creative provide 4 distinct variants of: hooks (≤6 words), highlights \
        (the 1–2 word emphasis inside each hook, same order), headlines, primaryTexts, and imagePrompts \
        (each keeps the real product accurate and ends with "No text, no words, no logos. 4:5 vertical.").
        Return ONLY JSON for a single persona:
        { "name": string, "audience": "A"|"B", "score": int, "ltv": string, "angle": string,
          "description": string, "reasonTop": string,
          "coreEmotion": string, "selfImage": string, "psychLever": string,
          "coverage": { "emotions": [string], "moments": [string] },
          "copy": { "primaryTexts": [string,string,string,string], "headlines": [string,string,string], "cta": string },
          "creatives": [ { "rank": int, "score": int, "imageStyle": string, "concept": string, "message": string,
            "productDetail": string, "layout": string, "reasonTop": string,
            "emotionAxis": string, "moment": string, "messageStrategy": string, "valueSignal": string,
            "hooks": [4], "highlights": [4], "headlines": [4], "primaryTexts": [4], "imagePrompts": [4] } ] }
        """
```

(No mapping change needed here — `generatePersona` returns a `PersonaDTO`, which
already decodes the new fields tolerantly from Task 2, and any caller that turns
it into a `Persona` goes through `makePersona` from Task 3.)

- [ ] **Step 2: Build**

Run the build/verify command. Expected: `** BUILD SUCCEEDED **`.

- [ ] **Step 3: Commit**

```sh
git add Sources/Generation/OpenAIStrategyClient.swift
git commit -m "Add 5-axis fields to the add-one-persona prompt"
```

---

## Task 6: Inspector display (InspectorView.swift)

**Files:**
- Modify: `Sources/Views/Inspector/InspectorView.swift`

- [ ] **Step 1: Add a `lensRow` helper**

Inside `struct InspectorView`, add this helper method (e.g. right before
`private func generate(...)` at line 289):

```swift
    @ViewBuilder private func lensRow(_ k: String, _ v: String) -> some View {
        HStack(alignment: .top, spacing: 6) {
            Text(k.uppercased()).font(.system(size: 9.5, weight: .bold)).tracking(0.3)
                .foregroundStyle(Theme.ink4).frame(width: 80, alignment: .leading)
            Text(v).font(.system(size: 11.5)).foregroundStyle(Theme.ink2).lineSpacing(2)
                .frame(maxWidth: .infinity, alignment: .leading)
        }
    }
```

- [ ] **Step 2: Insert the 5-axis / lens / setup-guidance sections**

In `detail(project:persona:creative:)`, immediately after the "why ranked"
accent card block — i.e. after its closing `.padding(.bottom, 16)` on line 209
and before the `InspectorField(label: "Hook …")` on line 211 — insert:

```swift
                    // Andromeda axis tags for this creative.
                    if !creative.emotionAxis.isEmpty || !creative.moment.isEmpty
                        || !creative.messageStrategy.isEmpty {
                        InspectorField(label: "Andromeda axes") {
                            HStack(spacing: 6) {
                                if !creative.emotionAxis.isEmpty { Tag(text: creative.emotionAxis, color: Theme.accent) }
                                if !creative.moment.isEmpty { Tag(text: creative.moment, color: Theme.ink2) }
                                if !creative.messageStrategy.isEmpty { Tag(text: creative.messageStrategy, color: Theme.ink3) }
                                Spacer(minLength: 0)
                            }
                        }
                    }
                    if !creative.valueSignal.isEmpty {
                        InspectorField(label: "Value signal (axis 5)") {
                            Text(creative.valueSignal).font(.system(size: 12.5))
                                .foregroundStyle(Theme.ink2).lineSpacing(2)
                        }
                    }
                    // Persona lens + coverage map.
                    if !persona.coreEmotion.isEmpty || !persona.selfImage.isEmpty
                        || !persona.psychLever.isEmpty || !persona.coverage.emotions.isEmpty
                        || !persona.coverage.moments.isEmpty {
                        InspectorField(label: "Persona lens · \(persona.name)") {
                            VStack(alignment: .leading, spacing: 4) {
                                if !persona.coreEmotion.isEmpty { lensRow("Core emotion", persona.coreEmotion) }
                                if !persona.selfImage.isEmpty { lensRow("Self-image", persona.selfImage) }
                                if !persona.psychLever.isEmpty { lensRow("Lever", persona.psychLever) }
                                if !persona.coverage.emotions.isEmpty { lensRow("Emotions", persona.coverage.emotions.joined(separator: " · ")) }
                                if !persona.coverage.moments.isEmpty { lensRow("Moments", persona.coverage.moments.joined(separator: " · ")) }
                            }
                        }
                    }
                    // Campaign setup guidance (axes 1 & 5).
                    if let sg = project.setupGuidance,
                       !(sg.pixelCapi.isEmpty && sg.valueRules.isEmpty && sg.lookalike.isEmpty && sg.targeting.isEmpty) {
                        InspectorField(label: "Campaign setup (axes 1 & 5)") {
                            VStack(alignment: .leading, spacing: 4) {
                                if !sg.pixelCapi.isEmpty { lensRow("Pixel/CAPI", sg.pixelCapi) }
                                if !sg.valueRules.isEmpty { lensRow("Value rules", sg.valueRules) }
                                if !sg.lookalike.isEmpty { lensRow("Lookalike", sg.lookalike) }
                                if !sg.targeting.isEmpty { lensRow("Targeting", sg.targeting) }
                            }
                        }
                    }
```

Note: `Tag(text:color:)`, `InspectorField`, `Theme`, and the `lensRow` helper are
all already in scope (`Tag` is used on line 49; `InspectorField` is defined at the
bottom of this file). Each block is guarded by non-empty checks, so legacy
projects render nothing new.

- [ ] **Step 3: Build**

Run the build/verify command. Expected: `** BUILD SUCCEEDED **`.

- [ ] **Step 4: Commit**

```sh
git add Sources/Views/Inspector/InspectorView.swift
git commit -m "Show 5-axis tags, persona lens, and setup guidance in Inspector"
```

---

## Task 7: Final verification

**Files:** none (verification only)

- [ ] **Step 1: Clean build**

Run:
```sh
xcodebuild -project AdCreativeStudio.xcodeproj -scheme AdCreativeStudio -configuration Debug clean build 2>&1 | tail -5
```
Expected: `** BUILD SUCCEEDED **`.

- [ ] **Step 2: Backward-compatibility reasoning check**

Confirm by inspection that every new field is decoded with `try? … ?? default`
(Persona, Creative, Coverage, SetupGuidance, all DTOs) and `Project.setupGuidance`
is `Optional`. A project saved before this change has none of these keys, so every
decode falls back to a default and no `keyNotFound` is thrown. (No saved-fixture
test target exists in this repo; this is a structural guarantee, not a runtime test.)

- [ ] **Step 3: Manual generation check (requires an OpenAI key in the running app)**

Launch the app, create a campaign, generate a strategy, and confirm:
- Each persona shows a "Persona lens" block with a coverage map.
- A persona's M creatives span the declared emotions/moments (distinct
  "Andromeda axes" tags across creatives, not all identical).
- "Campaign setup (axes 1 & 5)" shows tailored guidance.
- Opening a project saved before this change still loads (no new chips, no crash).

If the manual check is deferred (no key handy), note it explicitly rather than
claiming it passed.

- [ ] **Step 4: Final commit (if anything was adjusted during verification)**

```sh
git add -A
git commit -m "Verify 5-axis strategy build + backward compatibility"
```

---

## Self-Review notes

- **Spec coverage:** §3 schema → Tasks 1–2; §4 models → Task 1; §5 prompt →
  Tasks 4–5; §6 UI → Task 6; §2 backward-compat → Tasks 1–2 + Task 7 Step 2;
  setupGuidance flow via makeProject → Task 3 Step 1. All sections mapped.
- **Type consistency:** `Coverage{emotions,moments}`, `SetupGuidance{pixelCapi,
  valueRules,lookalike,targeting}`, persona fields `coreEmotion/selfImage/
  psychLever/coverage`, creative tags `emotionAxis/moment/messageStrategy/
  valueSignal` are used with identical names in models (Task 1), DTOs (Task 2),
  mapping (Task 3), prompts (Tasks 4–5), and UI (Task 6).
- **Placeholders:** none — every code step shows complete code; verification is
  build output, not "add error handling".
