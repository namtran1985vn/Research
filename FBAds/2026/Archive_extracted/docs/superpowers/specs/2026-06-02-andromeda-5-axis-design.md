# Andromeda 5-Axis Creative Strategy — Design Spec

**Date:** 2026-06-02
**Status:** Approved (user delegated all remaining decisions; "làm hết")
**Scope:** Brain (schema + prompt) + Display (Inspector) + Setup-guidance checklist

## 1. Goal

Make the generation brain produce ad-set creative that explicitly covers the
**5 intersecting axes of Andromeda** the user's guide describes, so the model
stops collapsing M creatives onto one emotion (guide §IX.2–3) and gives
Andromeda more winning intersections to match.

The five axes (from the guide):

1. **Người** (person) — Andromeda controls; app only keeps targeting broad.
2. **Cảm xúc / intent** — app *suggests* via creative.
3. **Khoảnh khắc / ngữ cảnh** (moment/context) — app *suggests* via creative.
4. **Creative cộng hưởng** (creative resonance) — the axis the app fully controls.
5. **Predicted value** — app *steers* via value signals + setup guidance.

The app fully owns axis 4, suggests 2 & 3, steers 5, and only *reminds* about 1 & 5
(campaign-side settings the app does not execute).

## 2. Key decisions

- **Architecture: persona-scoped, plan-then-fill (refined Hướng C).** Chosen for
  output quality, not simplicity. Because the user opted for *prompt-only*
  enforcement (no code coverage check), the **JSON generation order is the only
  diversity safety net** — so each persona must first *declare its coverage map*
  (the distinct emotions/moments it will span), then fill its M creatives, each
  into a distinct cell. Declaring the space before filling it is what prevents
  emotion collapse.
- **Per-persona, not per-campaign.** Each persona is its own emotional lens
  (guide §II). A campaign-wide palette would flatten persona distinctiveness, so
  the coverage map lives on the persona.
- **AI derives the axis vocabulary from the product + target customers** — no
  hardcoded enum. The guide's 9 emotional levers (§IV), 6 moments (§V), and 5
  message strategies are passed to the model as a *reference frame to adapt*, not
  a closed list. Labels are written in the project's content language.
- **No code-level coverage check / badge.** Prompt enforces coverage; the app
  displays the values but does not compute or gate on a coverage score.
- **Setup guidance (axes 1 & 5) is AI-tailored per campaign**, generated
  alongside the strategy (not a static checklist).
- **Backward compatible.** All new fields decode tolerantly (default empty), so
  projects saved before this change keep loading — matching the existing
  `Creative.init(from:)` / `Product.init(from:)` convention.

## 3. Schema changes (`StrategyResponse`, Sources/Models/Strategy.swift)

### 3.1 `PersonaDTO` — adds the §II lens + coverage map

```
coreEmotion: String     // §II.3 — the core emotion driving their purchase
selfImage:   String     // §II.5 — who they want to become when buying this
psychLever:  String     // §II.6 — the 1–2 main psychological levers (from §IV frame)
coverage:               // the per-persona diversity space, AI-derived from product/target
  emotions: [String]    // ≥4 distinct emotional axes this persona's creatives will span
  moments:  [String]    // ≥3 distinct moments/contexts (§V frame)
```

`coverage` is emitted **before** `creatives` in the JSON object so the model
commits to the space first (plan-then-fill).

### 3.2 `CreativeDTO` — adds 4 axis tags

```
emotionAxis:     String   // axis 2 — one emotion drawn from persona.coverage.emotions
moment:          String   // axis 3 — one moment drawn from persona.coverage.moments
messageStrategy: String   // one of {pain, proof, transformation, objection, desire} as a label, adapted/translated
valueSignal:     String   // axis 5 — the "self-pricing-high" cue that attracts value buyers and
                          //           repels bargain hunters (§VI.B). DISTINCT from productDetail
                          //           (which stays "what to keep sharp/accurate").
```

Each of the M creatives must be a **distinct combination** of
(emotionAxis × moment × imageStyle × messageStrategy).

### 3.3 `StrategyResponse` (campaign level) — adds setup guidance

```
setupGuidance:            // axes 1 & 5, outside the creative (§VI.A, §VIII) — AI-tailored
  pixelCapi:  String      // clean Pixel/CAPI reminder for this product
  valueRules: String      // which LTV segment to bias bids toward
  lookalike:  String      // which seed audience + percentile for the lookalike
  targeting:  String      // how to keep targeting broad / Advantage+
```

All new DTO fields decode with `try?` defaults (empty string / empty array),
exactly like the existing `CreativeDTO.init(from:)`.

## 4. App model changes (Sources/Models/Models.swift)

- **`Persona`** gains `coreEmotion`, `selfImage`, `psychLever`, and a nested
  `Coverage { emotions: [String]; moments: [String] }`. Persona switches to a
  tolerant `init(from:)` (mirroring `Creative`) so old projects load.
- **`Creative`** gains `emotionAxis`, `moment`, `messageStrategy`, `valueSignal`.
  Added to the existing `CodingKeys` + tolerant `init(from:)` with `try?` defaults.
- **`Project`** gains `setupGuidance: SetupGuidance?` (optional → synthesized
  decode tolerates its absence) plus the key in `Project.CodingKeys`.
- **`StrategyResponse.makeProject` / `PersonaDTO.makePersona`** map the new DTO
  fields onto the models. Because `makeProject` is a method on `StrategyResponse`,
  it reads `self.setupGuidance` directly and sets it on the new `Project` — no
  threading through the engine is required. `CopyText.clean` is applied to the
  human-readable axis labels (emotionAxis, moment, messageStrategy, valueSignal,
  coverage entries, coreEmotion, selfImage, psychLever) the same way other copy
  is cleaned.

## 5. Prompt changes (`StrategyPrompt`, Sources/Models/Strategy.swift)

Restructure `StrategyPrompt.system` to:

1. **Reference frame block** — list the guide's 9 emotional levers (§IV), 6
   moments (§V), and 5 message strategies as *inspiration to adapt to this
   product*, explicitly stating they are a frame, not a closed list, and the
   model may coin product-specific axes. Labels in the content language.
2. **Step 2 (per persona)** — derive `coreEmotion`, `selfImage`, `psychLever`
   from the product + target customers, then **declare `coverage`**: pick ≥4
   distinct emotions + ≥3 distinct moments relevant to *this* persona.
3. **Step 3 (creatives)** — produce M creatives, **each a DISTINCT combination**
   of (emotionAxis × moment × imageStyle × messageStrategy), drawing emotionAxis
   from `coverage.emotions` and moment from `coverage.moments`. Hard rules:
   across the M creatives, emotionAxis uses `min(M,4)+` distinct values, moments
   `min(M,3)+` distinct, imageStyle `min(M,4)+` distinct (cap at the 5 styles),
   messageStrategy `min(M,3)+` distinct. Each creative also emits `valueSignal`
   (self-pricing-high cue), separate from `productDetail`.
4. **Anti-patterns block** — explicitly forbid the guide's §IX mistakes (repeat a
   concept with only the caption changed; every creative on one emotion;
   discount/cheap aesthetic).
5. **Campaign `setupGuidance`** — generate the four tailored reminders.
6. **OUTPUT schema** — update the JSON contract to the new shape, with
   `coverage` placed before `creatives`, and `setupGuidance` at the top level.

`StrategyPrompt.userMessage` stays largely the same (it already forwards
`targetCustomers` as strong guidance, which now also feeds axis derivation).

The **add-one-persona path** (`OpenAIStrategyClient.generatePersona`) gets the
same persona-level additions (coreEmotion/selfImage/psychLever/coverage + the 4
creative tags) so manually-added personas are consistent.

## 6. UI changes (Sources/Views/Inspector/InspectorView.swift)

Following existing `InspectorField` / `Tag` / `Theme` patterns (no new design system):

- **Per-creative axis row** — under the sticky header (next to the imageStyle
  `Tag`), show small tags for `emotionAxis`, `moment`, `messageStrategy`. Show
  `valueSignal` as an `InspectorField` ("Tín hiệu giá trị") near "Concept".
- **Persona lens block** — a collapsible/section showing `coreEmotion`,
  `selfImage`, `psychLever`, and the `coverage` map (emotions / moments chips) so
  the user can see the persona's emotional coverage at a glance.
- **Setup guidance panel** — a campaign-level card (shown in the inspector
  header area or as a section when a creative is selected) listing the four
  AI-tailored reminders (Pixel/CAPI, Value Rules, Lookalike, Targeting). Read-only
  reference; styled like the existing "WHY IT RANKED" accent card.

Empty new fields render nothing (old projects show no new chips), preserving the
current look for legacy data.

## 7. Out of scope (YAGNI)

- No coverage scoring / badge / auto-redo on insufficient diversity.
- No campaign-wide palette (kept per-persona).
- No changes to image generation, text-on-image editor, or export.
- No targeting automation — setup guidance is reference text only.

## 8. Touched files

- `Sources/Models/Strategy.swift` — DTOs, mapping, prompt.
- `Sources/Models/Models.swift` — Persona, Creative, Project, new `Coverage` /
  `SetupGuidance` types + tolerant decode.
- `Sources/Generation/OpenAIStrategyClient.swift` — `generatePersona` schema for
  the add-one-persona path.
- `Sources/Views/Inspector/InspectorView.swift` — display.

No `GenerationEngine` / `AppStore` changes are needed for `setupGuidance` (it
flows through `makeProject` on `StrategyResponse`); they are only touched if the
add-one-persona mapping needs the new persona fields surfaced.

## 9. Verification

- `xcodegen` + build the app (the project builds via xcodegen per the app spec);
  fix any compile errors.
- Decode an existing saved project to confirm backward compatibility (no new
  fields → no crash, empty chips).
- Generate a fresh strategy and confirm: each persona has a coverage map; the M
  creatives span the declared emotions/moments; setupGuidance is populated; the
  Inspector shows the new chips.
