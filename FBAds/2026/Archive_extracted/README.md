# Ad Creative Studio

A native **macOS (SwiftUI)** app that turns a product (photos + a short brief) into a ranked
Facebook/Meta ad-creative strategy and then generates the ad images — built to the spec in
[`APP_SPECS_AdCreativeStudio.md`](APP_SPECS_AdCreativeStudio.md) and the quiet-luxury design
handed off from Claude Design.

> Input product photos + description → **OpenAI GPT** (vision) ranks the top‑N personas and top‑M
> creatives per persona (with the *why*) → press generate to call **OpenAI gpt‑image‑1**, which
> keeps the real product accurate and leaves negative space → the app renders clean text on top.

**OpenAI only** — one API key powers everything (GPT for strategy/copy via Chat Completions, and
gpt‑image‑1 for images). No Anthropic/Claude.

## Highlights

- **Campaign → Persona → Creatives** hierarchy. You choose N personas (1–6) and M creatives each
  (3–10); GPT scores everything and returns only the top, with a transparent ranking sheet.
- **Real APIs** (no mocking): OpenAI Chat Completions (vision) for strategy/copy, OpenAI gpt‑image‑1
  (`images/edits` with your product photo as reference) for images. The key lives in the **Keychain**
  — or hardcode it in `Sources/Store/Secrets.swift` for single‑user convenience.
- **Parallel generation engine** — a concurrency‑capped queue (default 4, configurable 1–8) with
  per‑image status (idle / queued / generating / done / error), auto‑retry + exponential backoff
  on 429, "Generate all", "Generate this set", per‑card retry, and "Retry all".
- **Text‑on‑image editor** — drag text blocks over the AI render, tune font/size/color/highlight/
  alignment, and export a composited **1024 × 1280** PNG (clean Vietnamese or English type).
- **Export** all generated images + a `copy.csv` (persona, rank, hooks, headlines, primary text).
- **Multi‑project** local persistence (Application Support); the queue is durable across launches —
  interrupted in‑flight images reset to idle so you can resume without redoing finished ones.
- Power‑user shortcuts: ⌘N new · ⌘↵ run strategy · ⌘G generate all · ⌘R regenerate selected ·
  ⌘E export · ⌘, settings.

## Build & run

Requires Xcode 16+ (built with Xcode 26) and [`xcodegen`](https://github.com/yonyz/XcodeGen)
(`brew install xcodegen`).

The `AdCreativeStudio.xcodeproj` is already generated — just open it:

```sh
open AdCreativeStudio.xcodeproj          # then press ⌘R in Xcode
```

If you ever need to regenerate it from `project.yml`: `xcodegen generate`. CLI build:
`xcodebuild -project AdCreativeStudio.xcodeproj -scheme AdCreativeStudio -configuration Debug build`.

On first launch, open **Settings (⌘,)** and paste your **OpenAI** API key (or hardcode it in
`Sources/Store/Secrets.swift`). That one key is used for both GPT and gpt‑image.

## Project layout

```
project.yml                     XcodeGen spec (target, entitlements, deployment target)
Resources/                      Info.plist, entitlements (sandbox + network + keychain), assets
Sources/
  App/                          @main app + menu commands / keyboard shortcuts
  DesignSystem/Theme.swift      faithful port of the design's tokens.css
  Models/                       Project / Persona / Creative, status, Claude JSON contract + prompt
  Store/                        AppStore (state), ProjectStore (disk), AppSettings, Keychain, Secrets
  Generation/                   OpenAIStrategyClient (GPT), ImageProvider + OpenAIImageProvider, GenerationEngine
  TextOnImage/TextRenderer.swift  composites text layers → final PNG
  Views/                        Sidebar, Input (S1), Results+CreativeCard (S2), Inspector,
                                Editor (S3 text-on-image), Overlays (Settings, Ranking, Toast)
```

The `ImageProvider` protocol wraps the image backend so a future provider (e.g. Nano Banana) can
be swapped in without touching the engine or UI.
