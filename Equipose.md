# Equipose

> Your trainer's eye, every ride.

AI-powered riding position coach for equestrians. Record a ride, get instant feedback on your equitation — heels, hands, hip angle, eyes, two-point — like having your trainer in your pocket.

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Brand & Naming](#brand--naming)
3. [Status](#status)
4. [What It Does](#what-it-does)
5. [Architecture](#architecture)
6. [Tech Stack](#tech-stack)
7. [Project Structure](#project-structure)
8. [Prerequisites](#prerequisites)
9. [Getting Started](#getting-started)
10. [Development Workflow](#development-workflow)
11. [Full Build Guide (4 Weeks)](#full-build-guide-4-weeks)
12. [Cloudflare Worker Proxy](#cloudflare-worker-proxy)
13. [iOS Implementation Details](#ios-implementation-details)
14. [GPT-4o Prompt Design](#gpt-4o-prompt-design)
15. [Result UI](#result-ui)
16. [Paywall & Subscription](#paywall--subscription)
17. [Analytics Events](#analytics-events)
18. [App Store Launch](#app-store-launch)
19. [Cost Model](#cost-model)
20. [Roadmap](#roadmap)
21. [Privacy & Data](#privacy--data)
22. [Resources](#resources)

---

## Project Overview

Equipose is an iOS app that gives adult amateur equestrian riders AI-powered feedback on their riding position and form. The user records a video of themselves riding, the app analyzes it using Apple Vision (on-device) and GPT-4o (via a thin proxy), and returns coaching feedback in seconds.

**Target user:** Adult amateur hunter/jumper, dressage, and eventing riders who ride 3–4 times a week but only see their trainer once a week. They want objective, expert-level feedback between lessons.

**The pitch:** Like having your trainer in your pocket.

---

## Brand & Naming

- **Name:** Equipose (pronounced eh-kwuh-pohz)
- **Etymology:** *equi* (horse) + *pose* (what the AI analyzes), with a deliberate echo of *equipoise* (balance and composure — the core of good riding)
- **Tagline:** *"Your trainer's eye, every ride."*
- **Voice:** Knowledgeable, warm, never condescending. Like a good trainer — direct about what to fix, generous about what's working.
- **Visual identity:** Navy and gold (traditional equestrian show colors), serif display type, photography that's clean and sport-focused, never overproduced.
- **Backup names if Equipose is taken:** Stride, Pin, Riderly, TwoPoint
- **App Store category:** Health & Fitness → Sports

---

## Status

**Pre-launch MVP.** Targeting 4-week build to TestFlight beta, 6-week public App Store launch.

---

## What It Does

1. Rider records a video of their ride from ringside (phone on a tripod or held by a helper)
2. Apple Vision analyzes the footage on-device — body pose, hand pose, jump trajectory, motion
3. App computes objective measurements: heel angle, hip drift, eyes-up ratio, hand steadiness, jump-arc geometry
4. Measurements + 8 keyframes go to GPT-4o via a thin proxy
5. App returns a structured coaching report: overall score, per-category breakdown, per-jump feedback, top priority to work on

**Core value:** Adult amateurs ride 3–4 times a week but only see their trainer once. Equipose fills the gap between lessons with objective, instant, expert-level feedback.

---

## Architecture

```
iPhone (does 99% of the work)
  Camera capture (AVFoundation)
       │
       ▼
  Apple Vision (on-device, free, offline)
    ├─ VNDetectHumanBodyPoseRequest    → rider keypoints
    ├─ VNDetectHumanHandPoseRequest    → release / rein analysis
    ├─ VNDetectTrajectoriesRequest     → jump arc detection
    └─ VNTrackObjectRequest            → smooth tracking
       │
       ▼
  Swift measurement engine
    └─ 8 keyframes + measurements JSON (~500 KB)
       │
       ▼  HTTPS POST
  Cloudflare Worker proxy (~50 lines of TypeScript)
    ├─ App Attestation verification
    ├─ Per-device daily rate limit
    └─ Forward to OpenAI with secret API key
       │
       ▼
  OpenAI GPT-4o (vision + JSON mode)
       │
       ▼  structured JSON
  iPhone displays result
```

**No FastAPI. No GPU server. No database. The "backend" is one TypeScript file.**

---

## Tech Stack

| Layer | Choice | Why |
|---|---|---|
| iOS app | Swift 5.9, SwiftUI, iOS 17+ | Native, Apple Vision support |
| Video | AVFoundation, AVKit | Camera capture and playback |
| On-device ML | Apple Vision framework | Free, fast, optimized for Neural Engine |
| Persistence | SwiftData | Native, simple |
| Subscriptions | RevenueCat | Handles IAP without a server |
| Crash reporting | Sentry | Generous free tier |
| Analytics | PostHog | Open source, free tier |
| Proxy | Cloudflare Workers (TypeScript) | Free 100k req/day, edge network |
| Rate limit storage | Cloudflare KV | Native to Workers |
| AI | OpenAI GPT-4o | Best vision + text quality |
| Auth | Sign in with Apple + DCAppAttestService | No backend auth needed |

---

## Project Structure

```
equipose/
├── ios/
│   ├── Equipose.xcodeproj
│   ├── Equipose/
│   │   ├── App/
│   │   │   ├── EquiposeApp.swift           # @main entry
│   │   │   └── AppDelegate.swift
│   │   ├── Features/
│   │   │   ├── Onboarding/
│   │   │   │   ├── OnboardingView.swift
│   │   │   │   ├── CameraTutorialView.swift
│   │   │   │   └── DisciplineSelectView.swift
│   │   │   ├── Capture/
│   │   │   │   ├── CaptureView.swift
│   │   │   │   ├── CameraManager.swift
│   │   │   │   └── RecordingOverlay.swift
│   │   │   ├── Analysis/
│   │   │   │   ├── AnalysisView.swift
│   │   │   │   ├── VisionPipeline.swift
│   │   │   │   ├── MeasurementEngine.swift
│   │   │   │   ├── KeyframeExtractor.swift
│   │   │   │   └── Models/
│   │   │   │       ├── BodyPoseFrame.swift
│   │   │   │       ├── JumpMoment.swift
│   │   │   │       └── RideMeasurements.swift
│   │   │   ├── Result/
│   │   │   │   ├── ResultView.swift
│   │   │   │   ├── ScoreCardView.swift
│   │   │   │   ├── PerJumpBreakdownView.swift
│   │   │   │   └── CoachingFeedbackView.swift
│   │   │   ├── History/
│   │   │   │   ├── HistoryView.swift
│   │   │   │   └── RideDetailView.swift
│   │   │   ├── Paywall/
│   │   │   │   └── PaywallView.swift
│   │   │   └── Settings/
│   │   │       └── SettingsView.swift
│   │   ├── Core/
│   │   │   ├── Networking/
│   │   │   │   ├── APIClient.swift
│   │   │   │   ├── ProxyEndpoint.swift
│   │   │   │   └── AppAttestationService.swift
│   │   │   ├── Storage/
│   │   │   │   ├── RideRepository.swift     # SwiftData
│   │   │   │   └── Models/Ride.swift
│   │   │   ├── Subscription/
│   │   │   │   └── SubscriptionManager.swift # RevenueCat wrapper
│   │   │   └── Analytics/
│   │   │       └── Analytics.swift
│   │   ├── DesignSystem/
│   │   │   ├── Colors.swift
│   │   │   ├── Typography.swift
│   │   │   └── Components/
│   │   └── Resources/
│   │       ├── Assets.xcassets
│   │       └── Info.plist
│   └── EquiposeTests/
└── proxy/
    ├── src/worker.ts
    ├── wrangler.toml
    ├── package.json
    └── README.md
```

---

## Prerequisites

- **macOS** with Xcode 15+
- **iOS device** running iOS 17+ (Vision pose detection requires real hardware — simulator will not work)
- **Apple Developer account** ($99/year) for App Attestation and TestFlight
- **Node.js 20+** and `wrangler` CLI for the proxy
- **Cloudflare account** (free tier)
- **OpenAI API key** with GPT-4o access
- **RevenueCat account** (free)

---

## Getting Started

### 1. Clone and open

```bash
git clone https://github.com/YOUR_ORG/equipose.git
cd equipose
open ios/Equipose.xcodeproj
```

### 2. Deploy the proxy

```bash
cd proxy
npm install
npx wrangler login

# Create KV namespace for rate limiting
npx wrangler kv:namespace create RATE_LIMIT_KV
# Copy the returned id into wrangler.toml

# Set the OpenAI secret
npx wrangler secret put OPENAI_API_KEY
# Paste your key when prompted

# Deploy
npx wrangler deploy
# Note the deployed URL, e.g. https://equipose-proxy.YOUR.workers.dev
```

### 3. Configure the iOS app

Edit `ios/Equipose/Core/Networking/APIClient.swift`:

```swift
private let baseURL = URL(string: "https://equipose-proxy.YOUR.workers.dev")!
```

Add your RevenueCat API key in `ios/Equipose/Core/Subscription/SubscriptionManager.swift`.

### 4. Enable required capabilities in Xcode

In **Signing & Capabilities**:
- App Attestation (DCAppAttestService)
- Sign in with Apple
- In-App Purchase
- Push Notifications (optional, for re-engagement)

### 5. Info.plist permissions

```xml
<key>NSCameraUsageDescription</key>
<string>Equipose needs your camera to record your rides for AI analysis.</string>
<key>NSMicrophoneUsageDescription</key>
<string>Equipose records audio with your rides so you can hear your trainer's cues.</string>
<key>NSPhotoLibraryAddUsageDescription</key>
<string>Save analyzed rides to your photo library.</string>
```

### 6. Build and run on a real device

Plug in an iPhone running iOS 17+ and hit Run. The simulator will not work — Apple Vision body pose and camera both require physical hardware.

---

## Development Workflow

### Recommended first vertical slice (Day 1–3)

The smallest end-to-end test that proves the architecture works:

1. Camera screen that records a 30-second video
2. Send the video URL straight to GPT-4o Vision with no preprocessing
3. Show whatever GPT-4o returns on the next screen

If this works, layer Apple Vision and measurements on top. Don't build the full pipeline before you've seen one full round-trip in the simulator.

### Iterating on prompts

The GPT-4o system prompt lives in `Features/Analysis/Models/AnalyzeRequest.swift`. To tune scoring calibration, collect 20 sample videos with known ground-truth assessments and verify the model returns scores within ±1 point of expert judgment.

Cache GPT responses in development by hashing the request body — saves a lot of money when iterating on UI.

### Running tests

```bash
xcodebuild test -scheme Equipose -destination 'platform=iOS,name=YOUR_DEVICE'
```

---

## Full Build Guide (4 Weeks)

### Week 1 — Foundation

**Step 1.1 — Initialize project**

```bash
# In Xcode:
# - Template: iOS App
# - Interface: SwiftUI
# - Language: Swift
# - Minimum iOS: 17.0
# - Bundle ID: com.equipose.app
# - Include: SwiftData

# Create proxy:
mkdir proxy && cd proxy
npm create cloudflare@latest -- --type=hello-world --ts
```

**Step 1.2 — Add Swift Package Manager dependencies**

- `https://github.com/RevenueCat/purchases-ios`
- `https://github.com/getsentry/sentry-cocoa`
- `https://github.com/PostHog/posthog-ios`

**Step 1.3 — Deploy Cloudflare Worker proxy** (see Cloudflare Worker Proxy section)

**Step 1.4 — Networking layer** (see iOS Implementation Details section)

### Week 2 — Vision Pipeline

- Camera capture with AVFoundation
- VisionPipeline orchestrating body pose, hand pose, trajectory detection
- MeasurementEngine computing objective metrics
- KeyframeExtractor pulling 8 frames at jump moments

### Week 3 — AI Integration & UI

- AnalyzeRequest builder with prompt
- GPT-4o integration via proxy
- ResultView with score cards, per-jump breakdown
- History persistence with SwiftData

### Week 4 — Polish, Paywall, Launch

- Onboarding flow with camera tutorial (critical: teach side-view C/E)
- RevenueCat paywall
- Analytics events
- TestFlight beta with 10 real riders

### Build order checklist

| Week | Focus |
|---|---|
| 1 | Project setup, proxy deployed, networking layer, camera capture working |
| 2 | Apple Vision pipeline, measurement engine, keyframe extraction |
| 3 | GPT-4o integration, prompt iteration, result UI |
| 4 | Onboarding, paywall, polish, TestFlight beta with 10 real riders |

**First measurable milestone:** record a 30-second ride, get a real GPT-4o response back, display the score. Aim to hit this by end of Week 2.

---

## Cloudflare Worker Proxy

**`proxy/src/worker.ts`:**

```typescript
export interface Env {
  OPENAI_API_KEY: string;
  RATE_LIMIT_KV: KVNamespace;
}

const DAILY_LIMIT_FREE = 3;
const DAILY_LIMIT_PRO = 50;

export default {
  async fetch(req: Request, env: Env): Promise<Response> {
    if (req.method !== 'POST') {
      return new Response('Method not allowed', { status: 405 });
    }

    const url = new URL(req.url);
    if (url.pathname !== '/v1/analyze') {
      return new Response('Not found', { status: 404 });
    }

    // 1. Verify App Attestation (production)
    const attestation = req.headers.get('X-App-Attestation');
    const deviceId = req.headers.get('X-Device-ID');
    const tier = req.headers.get('X-User-Tier') ?? 'free';

    if (!deviceId) {
      return new Response('Missing device ID', { status: 401 });
    }

    // TODO: Verify attestation cryptographically in production
    // For MVP, presence check is acceptable

    // 2. Rate limit
    const today = new Date().toISOString().split('T')[0];
    const key = `rl:${deviceId}:${today}`;
    const countStr = await env.RATE_LIMIT_KV.get(key);
    const count = parseInt(countStr ?? '0');
    const limit = tier === 'pro' ? DAILY_LIMIT_PRO : DAILY_LIMIT_FREE;

    if (count >= limit) {
      return new Response(
        JSON.stringify({ error: 'Daily limit reached', limit, tier }),
        { status: 429, headers: { 'Content-Type': 'application/json' } }
      );
    }

    await env.RATE_LIMIT_KV.put(key, String(count + 1), { expirationTtl: 86400 });

    // 3. Forward to OpenAI
    const body = await req.text();
    const openaiRes = await fetch('https://api.openai.com/v1/chat/completions', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${env.OPENAI_API_KEY}`,
        'Content-Type': 'application/json',
      },
      body,
    });

    return new Response(openaiRes.body, {
      status: openaiRes.status,
      headers: {
        'Content-Type': openaiRes.headers.get('Content-Type') ?? 'application/json',
        'X-RateLimit-Remaining': String(limit - count - 1),
      },
    });
  },
};
```

**`proxy/wrangler.toml`:**

```toml
name = "equipose-proxy"
main = "src/worker.ts"
compatibility_date = "2024-11-01"

[[kv_namespaces]]
binding = "RATE_LIMIT_KV"
id = "REPLACE_AFTER_CREATING"
```

**Deploy:**

```bash
wrangler kv:namespace create RATE_LIMIT_KV
# Copy ID into wrangler.toml
wrangler secret put OPENAI_API_KEY
wrangler deploy
```

---

## iOS Implementation Details

### Networking Layer

**`Core/Networking/APIClient.swift`:**

```swift
import Foundation
import DeviceCheck

final class APIClient {
    static let shared = APIClient()
    private let baseURL = URL(string: "https://equipose-proxy.YOUR-SUBDOMAIN.workers.dev")!

    private let session: URLSession = {
        let config = URLSessionConfiguration.default
        config.timeoutIntervalForRequest = 60
        return URLSession(configuration: config)
    }()

    func analyze(request: AnalyzeRequest) async throws -> AnalyzeResponse {
        var urlRequest = URLRequest(url: baseURL.appendingPathComponent("/v1/analyze"))
        urlRequest.httpMethod = "POST"
        urlRequest.setValue("application/json", forHTTPHeaderField: "Content-Type")
        urlRequest.setValue(deviceID(), forHTTPHeaderField: "X-Device-ID")
        urlRequest.setValue(userTier(), forHTTPHeaderField: "X-User-Tier")

        if let attestation = try? await AppAttestationService.shared.attest() {
            urlRequest.setValue(attestation, forHTTPHeaderField: "X-App-Attestation")
        }

        urlRequest.httpBody = try JSONEncoder().encode(request)

        let (data, response) = try await session.data(for: urlRequest)
        guard let http = response as? HTTPURLResponse else {
            throw APIError.invalidResponse
        }

        if http.statusCode == 429 {
            throw APIError.rateLimited
        }
        guard (200..<300).contains(http.statusCode) else {
            throw APIError.serverError(http.statusCode)
        }

        return try JSONDecoder().decode(AnalyzeResponse.self, from: data)
    }

    private func deviceID() -> String {
        UIDevice.current.identifierForVendor?.uuidString ?? UUID().uuidString
    }

    private func userTier() -> String {
        SubscriptionManager.shared.isPro ? "pro" : "free"
    }
}

enum APIError: Error {
    case invalidResponse
    case rateLimited
    case serverError(Int)
}
```

### Camera Capture

**`Features/Capture/CameraManager.swift`:**

```swift
import AVFoundation
import SwiftUI

@MainActor
final class CameraManager: NSObject, ObservableObject {
    @Published var isRecording = false
    @Published var recordedVideoURL: URL?
    @Published var session = AVCaptureSession()

    private let movieOutput = AVCaptureMovieFileOutput()
    private var outputURL: URL?

    func setup() async {
        guard await requestPermission() else { return }
        session.sessionPreset = .high

        guard let camera = AVCaptureDevice.default(.builtInWideAngleCamera, for: .video, position: .back),
              let input = try? AVCaptureDeviceInput(device: camera) else { return }

        if let mic = AVCaptureDevice.default(for: .audio),
           let audioInput = try? AVCaptureDeviceInput(device: mic) {
            session.beginConfiguration()
            if session.canAddInput(input) { session.addInput(input) }
            if session.canAddInput(audioInput) { session.addInput(audioInput) }
            if session.canAddOutput(movieOutput) { session.addOutput(movieOutput) }

            // Lock to 1080p / 30fps for predictable Vision processing
            try? camera.lockForConfiguration()
            camera.activeFormat = camera.formats.first(where: {
                let dims = CMVideoFormatDescriptionGetDimensions($0.formatDescription)
                return dims.width == 1920 && dims.height == 1080
            }) ?? camera.activeFormat
            camera.unlockForConfiguration()

            session.commitConfiguration()
        }

        Task.detached { [session] in
            session.startRunning()
        }
    }

    func startRecording() {
        let url = FileManager.default.temporaryDirectory
            .appendingPathComponent("ride-\(Date().timeIntervalSince1970).mov")
        outputURL = url
        movieOutput.startRecording(to: url, recordingDelegate: self)
        isRecording = true
    }

    func stopRecording() {
        movieOutput.stopRecording()
    }

    private func requestPermission() async -> Bool {
        switch AVCaptureDevice.authorizationStatus(for: .video) {
        case .authorized: return true
        case .notDetermined: return await AVCaptureDevice.requestAccess(for: .video)
        default: return false
        }
    }
}

extension CameraManager: AVCaptureFileOutputRecordingDelegate {
    nonisolated func fileOutput(_ output: AVCaptureFileOutput, didFinishRecordingTo outputFileURL: URL,
                                 from connections: [AVCaptureConnection], error: Error?) {
        Task { @MainActor in
            self.recordedVideoURL = outputFileURL
            self.isRecording = false
        }
    }
}
```

### Vision Pipeline

**`Features/Analysis/VisionPipeline.swift`:**

```swift
import Vision
import AVFoundation
import CoreImage

struct RideAnalysis {
    let frames: [BodyPoseFrame]
    let jumpMoments: [JumpMoment]
    let handPoses: [HandPoseFrame]
    let keyframeImages: [KeyframeImage]
    let videoDuration: TimeInterval
}

final class VisionPipeline {
    func analyze(videoURL: URL) async throws -> RideAnalysis {
        let asset = AVURLAsset(url: videoURL)
        let duration = try await asset.load(.duration).seconds
        let reader = try AVAssetReader(asset: asset)

        guard let track = try await asset.loadTracks(withMediaType: .video).first else {
            throw VisionError.noVideoTrack
        }

        let outputSettings: [String: Any] = [
            kCVPixelBufferPixelFormatTypeKey as String: kCVPixelFormatType_32BGRA
        ]
        let output = AVAssetReaderTrackOutput(track: track, outputSettings: outputSettings)
        reader.add(output)
        reader.startReading()

        var bodyFrames: [BodyPoseFrame] = []
        var handFrames: [HandPoseFrame] = []
        var trajectorySequences: [VNTrajectoryObservation] = []
        var frameIndex = 0
        let sampleEvery = 2 // analyze every 2nd frame for performance

        let trajectoryRequest = VNDetectTrajectoriesRequest(
            frameAnalysisSpacing: .zero,
            trajectoryLength: 15
        ) { request, _ in
            if let results = request.results as? [VNTrajectoryObservation] {
                trajectorySequences.append(contentsOf: results)
            }
        }

        let sequenceHandler = VNSequenceRequestHandler()

        while let sampleBuffer = output.copyNextSampleBuffer() {
            defer { CMSampleBufferInvalidate(sampleBuffer) }
            frameIndex += 1
            guard frameIndex % sampleEvery == 0 else { continue }

            guard let pixelBuffer = CMSampleBufferGetImageBuffer(sampleBuffer) else { continue }
            let timestamp = CMSampleBufferGetPresentationTimeStamp(sampleBuffer).seconds

            let bodyRequest = VNDetectHumanBodyPoseRequest()
            let handRequest = VNDetectHumanHandPoseRequest()
            handRequest.maximumHandCount = 2

            let handler = VNImageRequestHandler(cvPixelBuffer: pixelBuffer, orientation: .right)

            try? handler.perform([bodyRequest, handRequest])
            try? sequenceHandler.perform([trajectoryRequest], on: pixelBuffer)

            if let body = bodyRequest.results?.first {
                bodyFrames.append(BodyPoseFrame(timestamp: timestamp, observation: body))
            }
            if let hands = handRequest.results {
                handFrames.append(HandPoseFrame(timestamp: timestamp, observations: hands))
            }
        }

        let jumpMoments = JumpDetector.extractMoments(from: trajectorySequences, totalDuration: duration)
        let keyframes = try await KeyframeExtractor.extract(from: videoURL, at: jumpMoments.map(\.timestamp))

        return RideAnalysis(
            frames: bodyFrames,
            jumpMoments: jumpMoments,
            handPoses: handFrames,
            keyframeImages: keyframes,
            videoDuration: duration
        )
    }
}

enum VisionError: Error {
    case noVideoTrack
}
```

### Measurement Engine

**`Features/Analysis/MeasurementEngine.swift`:**

```swift
import Vision
import CoreGraphics

struct RideMeasurements: Codable {
    let overall: OverallMetrics
    let perJump: [JumpMetrics]

    struct OverallMetrics: Codable {
        let avgHeelAngle: Double          // degrees, ideal 80-95
        let heelStabilityScore: Double    // 0-1, lower variance = higher
        let upperBodyDrift: Double        // shoulder lateral movement
        let eyesUpRatio: Double           // % of frames eyes-up estimate
        let handSteadiness: Double        // 0-1
    }

    struct JumpMetrics: Codable {
        let index: Int
        let timestamp: Double
        let hipAngleAtTakeoff: Double     // jump ahead detection
        let releaseType: String           // "crest", "automatic", "long"
        let twoPointDepth: Double
        let arcHeight: Double             // from Vision trajectory
        let arcLength: Double
    }
}

enum MeasurementEngine {
    static func compute(from analysis: RideAnalysis) -> RideMeasurements {
        let overall = computeOverall(frames: analysis.frames, hands: analysis.handPoses)
        let perJump = analysis.jumpMoments.enumerated().map { idx, moment in
            computeJumpMetrics(
                index: idx,
                moment: moment,
                frames: analysis.frames,
                hands: analysis.handPoses
            )
        }
        return RideMeasurements(overall: overall, perJump: perJump)
    }

    private static func computeOverall(frames: [BodyPoseFrame], hands: [HandPoseFrame]) -> RideMeasurements.OverallMetrics {
        let heelAngles = frames.compactMap { $0.heelAngle() }
        let avgHeel = heelAngles.isEmpty ? 0 : heelAngles.reduce(0, +) / Double(heelAngles.count)
        let heelVariance = variance(heelAngles)
        let heelStability = max(0, 1 - heelVariance / 100)

        let shoulderXs = frames.compactMap { $0.shoulderMidX() }
        let drift = (shoulderXs.max() ?? 0) - (shoulderXs.min() ?? 0)

        let eyesUp = frames.filter { $0.eyesLikelyUp() }.count
        let eyesRatio = frames.isEmpty ? 0 : Double(eyesUp) / Double(frames.count)

        let handSteady = computeHandSteadiness(hands: hands)

        return .init(
            avgHeelAngle: avgHeel,
            heelStabilityScore: heelStability,
            upperBodyDrift: drift,
            eyesUpRatio: eyesRatio,
            handSteadiness: handSteady
        )
    }

    private static func computeJumpMetrics(index: Int, moment: JumpMoment,
                                            frames: [BodyPoseFrame], hands: [HandPoseFrame]) -> RideMeasurements.JumpMetrics {
        let nearestFrame = frames.min(by: { abs($0.timestamp - moment.timestamp) < abs($1.timestamp - moment.timestamp) })
        let hipAngle = nearestFrame?.hipAngle() ?? 0

        let nearestHand = hands.min(by: { abs($0.timestamp - moment.timestamp) < abs($1.timestamp - moment.timestamp) })
        let releaseType = classifyRelease(handFrame: nearestHand, bodyFrame: nearestFrame)

        return .init(
            index: index,
            timestamp: moment.timestamp,
            hipAngleAtTakeoff: hipAngle,
            releaseType: releaseType,
            twoPointDepth: nearestFrame?.twoPointDepth() ?? 0,
            arcHeight: moment.arcHeight,
            arcLength: moment.arcLength
        )
    }

    private static func variance(_ values: [Double]) -> Double {
        guard values.count > 1 else { return 0 }
        let mean = values.reduce(0, +) / Double(values.count)
        return values.map { pow($0 - mean, 2) }.reduce(0, +) / Double(values.count)
    }

    private static func classifyRelease(handFrame: HandPoseFrame?, bodyFrame: BodyPoseFrame?) -> String {
        guard let hand = handFrame, let body = bodyFrame else { return "unknown" }
        let handHeightVsWither = hand.averageHeight() - body.witherEstimateY()
        if handHeightVsWither > 0.1 { return "long_crest" }
        if handHeightVsWither > 0.0 { return "crest" }
        return "automatic"
    }

    private static func computeHandSteadiness(hands: [HandPoseFrame]) -> Double {
        guard hands.count > 2 else { return 0.5 }
        let positions = hands.map { $0.averagePosition() }
        let xs = positions.map(\.x)
        let ys = positions.map(\.y)
        let varX = variance(xs.map(Double.init))
        let varY = variance(ys.map(Double.init))
        return max(0, 1 - (varX + varY) / 0.1)
    }
}
```

### Body Pose Frame Extensions

**`Features/Analysis/Models/BodyPoseFrame.swift`:**

```swift
import Vision

struct BodyPoseFrame {
    let timestamp: Double
    let observation: VNHumanBodyPoseObservation

    func heelAngle() -> Double? {
        guard let knee = try? observation.recognizedPoint(.rightKnee),
              let ankle = try? observation.recognizedPoint(.rightAnkle),
              knee.confidence > 0.3, ankle.confidence > 0.3 else { return nil }
        let dx = ankle.x - knee.x
        let dy = ankle.y - knee.y
        return atan2(dx, -dy) * 180 / .pi
    }

    func hipAngle() -> Double? {
        guard let shoulder = try? observation.recognizedPoint(.rightShoulder),
              let hip = try? observation.recognizedPoint(.rightHip),
              let knee = try? observation.recognizedPoint(.rightKnee),
              shoulder.confidence > 0.3, hip.confidence > 0.3, knee.confidence > 0.3 else { return nil }
        return angle(a: shoulder, b: hip, c: knee)
    }

    func shoulderMidX() -> Double? {
        guard let l = try? observation.recognizedPoint(.leftShoulder),
              let r = try? observation.recognizedPoint(.rightShoulder),
              l.confidence > 0.3, r.confidence > 0.3 else { return nil }
        return (l.x + r.x) / 2
    }

    func eyesLikelyUp() -> Bool {
        guard let neck = try? observation.recognizedPoint(.neck),
              let nose = try? observation.recognizedPoint(.nose),
              neck.confidence > 0.3, nose.confidence > 0.3 else { return false }
        return nose.y > neck.y - 0.05
    }

    func twoPointDepth() -> Double {
        guard let shoulder = try? observation.recognizedPoint(.rightShoulder),
              let hip = try? observation.recognizedPoint(.rightHip),
              shoulder.confidence > 0.3, hip.confidence > 0.3 else { return 0 }
        return Double(hip.y - shoulder.y)
    }

    func witherEstimateY() -> CGFloat {
        guard let hip = try? observation.recognizedPoint(.rightHip) else { return 0.5 }
        return hip.y - 0.1
    }

    private func angle(a: VNRecognizedPoint, b: VNRecognizedPoint, c: VNRecognizedPoint) -> Double {
        let ab = (x: a.x - b.x, y: a.y - b.y)
        let cb = (x: c.x - b.x, y: c.y - b.y)
        let dot = ab.x * cb.x + ab.y * cb.y
        let magAB = sqrt(ab.x * ab.x + ab.y * ab.y)
        let magCB = sqrt(cb.x * cb.x + cb.y * cb.y)
        return acos(dot / (magAB * magCB)) * 180 / .pi
    }
}
```

### Capture Flow

**`Features/Capture/CaptureView.swift`:**

```swift
import SwiftUI

struct CaptureView: View {
    @StateObject private var camera = CameraManager()
    @State private var analyzing = false
    @State private var result: RideAnalysisResult?

    var body: some View {
        ZStack {
            CameraPreview(session: camera.session)
                .ignoresSafeArea()

            VStack {
                Spacer()
                if camera.isRecording {
                    RecordingButton(stopAction: { camera.stopRecording() })
                } else {
                    StartButton(action: { camera.startRecording() })
                }
            }
            .padding(.bottom, 40)

            if analyzing {
                AnalyzingOverlay()
            }
        }
        .task { await camera.setup() }
        .onChange(of: camera.recordedVideoURL) { _, url in
            guard let url else { return }
            Task { await runAnalysis(videoURL: url) }
        }
        .fullScreenCover(item: $result) { res in
            NavigationStack {
                ResultView(result: res, videoURL: camera.recordedVideoURL!)
            }
        }
    }

    private func runAnalysis(videoURL: URL) async {
        analyzing = true
        defer { analyzing = false }
        do {
            let pipeline = VisionPipeline()
            let analysis = try await pipeline.analyze(videoURL: videoURL)
            let measurements = MeasurementEngine.compute(from: analysis)
            let request = AnalyzeRequest.build(
                measurements: measurements,
                keyframes: analysis.keyframeImages,
                discipline: UserDefaults.standard.string(forKey: "discipline") ?? "hunter"
            )
            let response = try await APIClient.shared.analyze(request: request)
            result = try response.parsed()

            await RideRepository.shared.save(
                videoURL: videoURL,
                result: result!,
                measurements: measurements
            )
        } catch {
            Analytics.track("analysis_failed", props: ["error": "\(error)"])
        }
    }
}

extension RideAnalysisResult: Identifiable {
    var id: String { coaching_summary }
}
```

---

## GPT-4o Prompt Design

**`Features/Analysis/Models/AnalyzeRequest.swift`:**

```swift
struct AnalyzeRequest: Encodable {
    let model = "gpt-4o"
    let messages: [Message]
    let response_format = ResponseFormat(type: "json_object")
    let temperature = 0.3

    struct Message: Encodable {
        let role: String
        let content: [Content]
    }

    enum Content: Encodable {
        case text(String)
        case image(base64: String)

        func encode(to encoder: Encoder) throws {
            var container = encoder.container(keyedBy: CodingKeys.self)
            switch self {
            case .text(let str):
                try container.encode("text", forKey: .type)
                try container.encode(str, forKey: .text)
            case .image(let b64):
                try container.encode("image_url", forKey: .type)
                try container.encode(["url": "data:image/jpeg;base64,\(b64)"], forKey: .image_url)
            }
        }

        enum CodingKeys: String, CodingKey { case type, text, image_url }
    }

    struct ResponseFormat: Encodable { let type: String }

    static func build(measurements: RideMeasurements, keyframes: [KeyframeImage], discipline: String) -> AnalyzeRequest {
        let system = """
        You are an experienced USEF-certified equitation coach reviewing a rider's video.
        You will receive:
        1. Quantitative measurements computed by Apple Vision (pose data)
        2. Up to 8 keyframe images from the ride

        Analyze RIDER position and form. Do NOT score the horse — focus on the human.
        Be specific, kind, and constructive — like a good trainer.

        Return JSON with this exact schema:
        {
          "overall_score": 1-10,
          "categories": {
            "heels": { "score": 1-10, "note": "..." },
            "upper_body": { "score": 1-10, "note": "..." },
            "eyes": { "score": 1-10, "note": "..." },
            "hands": { "score": 1-10, "note": "..." },
            "two_point": { "score": 1-10, "note": "..." }
          },
          "per_jump": [
            { "jump_index": 0, "highlight": "...", "improvement": "..." }
          ],
          "coaching_summary": "2-3 sentences as if speaking to the rider",
          "top_priority": "the ONE thing to work on next ride"
        }

        Score calibration:
        - 9-10: Professional level
        - 7-8: Strong amateur
        - 5-6: Solid intermediate
        - 3-4: Beginner with notable issues
        - 1-2: Major safety concerns
        """

        let measurementsJSON = (try? String(data: JSONEncoder().encode(measurements), encoding: .utf8)) ?? "{}"
        let userPrompt = """
        Discipline: \(discipline)

        Measurements from Apple Vision:
        \(measurementsJSON)

        Images attached: \(keyframes.count) keyframes captured at jump moments.

        Provide your analysis as JSON.
        """

        var content: [Content] = [.text(userPrompt)]
        for kf in keyframes.prefix(8) {
            content.append(.image(base64: kf.base64))
        }

        return AnalyzeRequest(messages: [
            .init(role: "system", content: [.text(system)]),
            .init(role: "user", content: content),
        ])
    }
}

struct AnalyzeResponse: Decodable {
    let choices: [Choice]

    struct Choice: Decodable {
        let message: ResponseMessage
    }

    struct ResponseMessage: Decodable {
        let content: String
    }

    func parsed() throws -> RideAnalysisResult {
        guard let json = choices.first?.message.content.data(using: .utf8) else {
            throw APIError.invalidResponse
        }
        return try JSONDecoder().decode(RideAnalysisResult.self, from: json)
    }
}

struct RideAnalysisResult: Codable {
    let overall_score: Double
    let categories: [String: CategoryScore]
    let per_jump: [JumpFeedback]
    let coaching_summary: String
    let top_priority: String

    struct CategoryScore: Codable {
        let score: Double
        let note: String
    }

    struct JumpFeedback: Codable {
        let jump_index: Int
        let highlight: String
        let improvement: String
    }
}
```

### Prompt Tuning Tips

1. **Always pass measurements first** — GPT relies on them more than images
2. **Use JSON mode** — guarantees parseable output
3. **Temperature 0.3** — consistent scoring across runs
4. **System prompt longer than user prompt** — sets the "voice"
5. **Test on 20 sample videos** before launch — verify scoring calibration
6. **Cache responses** — same video hash → same response, save money

---

## Result UI

**`Features/Result/ResultView.swift`:**

```swift
import SwiftUI

struct ResultView: View {
    let result: RideAnalysisResult
    let videoURL: URL

    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 24) {
                OverallScoreCard(score: result.overall_score, summary: result.coaching_summary)
                TopPriorityBanner(priority: result.top_priority)
                CategoryGrid(categories: result.categories)
                PerJumpBreakdownView(jumps: result.per_jump)
                ShareToTrainerButton(result: result, videoURL: videoURL)
            }
            .padding()
        }
        .navigationTitle("Your Ride")
        .navigationBarTitleDisplayMode(.inline)
    }
}

struct OverallScoreCard: View {
    let score: Double
    let summary: String

    var body: some View {
        VStack(alignment: .leading, spacing: 12) {
            HStack(alignment: .firstTextBaseline) {
                Text(String(format: "%.1f", score))
                    .font(.system(size: 64, weight: .bold, design: .rounded))
                Text("/ 10")
                    .font(.title2)
                    .foregroundStyle(.secondary)
            }
            Text(summary)
                .font(.body)
                .foregroundStyle(.primary)
        }
        .frame(maxWidth: .infinity, alignment: .leading)
        .padding()
        .background(RoundedRectangle(cornerRadius: 16).fill(.regularMaterial))
    }
}
```

---

## Paywall & Subscription

**`Features/Paywall/PaywallView.swift`:**

```swift
import SwiftUI
import RevenueCat

struct PaywallView: View {
    @State private var offerings: Offerings?
    @State private var purchasing = false
    @Environment(\.dismiss) private var dismiss

    var body: some View {
        VStack(spacing: 24) {
            Image(systemName: "figure.equestrian.sports")
                .font(.system(size: 64))
                .foregroundStyle(.tint)

            Text("Unlock Equipose Pro")
                .font(.largeTitle.bold())

            VStack(alignment: .leading, spacing: 12) {
                FeatureRow(icon: "checkmark.circle.fill", text: "50 ride analyses per day")
                FeatureRow(icon: "checkmark.circle.fill", text: "Per-jump breakdown")
                FeatureRow(icon: "checkmark.circle.fill", text: "Progress tracking")
                FeatureRow(icon: "checkmark.circle.fill", text: "Share to your trainer")
            }
            .padding()

            if let offering = offerings?.current {
                ForEach(offering.availablePackages, id: \.identifier) { pkg in
                    Button {
                        Task { await purchase(pkg) }
                    } label: {
                        PackageRow(package: pkg)
                    }
                    .disabled(purchasing)
                }
            }

            Button("Restore Purchases") {
                Task { try? await Purchases.shared.restorePurchases() }
            }
            .font(.footnote)
        }
        .padding()
        .task { offerings = try? await Purchases.shared.offerings() }
    }

    private func purchase(_ package: Package) async {
        purchasing = true
        defer { purchasing = false }
        do {
            let result = try await Purchases.shared.purchase(package: package)
            if result.customerInfo.entitlements["pro"]?.isActive == true {
                dismiss()
            }
        } catch { /* handle */ }
    }
}
```

### Subscription tiers

| Tier | Price | Daily limit |
|---|---|---|
| Free | $0 | 3 analyses/day |
| Pro Monthly | $14.99/mo | 50 analyses/day |
| Pro Annual | $119.99/yr | 50 analyses/day (33% savings) |

---

## Onboarding Flow

```swift
struct OnboardingView: View {
    @State private var step = 0

    var body: some View {
        TabView(selection: $step) {
            WelcomeStep().tag(0)
            DisciplineSelectView().tag(1)
            CameraTutorialView().tag(2)
            FirstRideCTAStep().tag(3)
        }
        .tabViewStyle(.page)
    }
}
```

**Critical: the camera tutorial must teach:**
1. Phone in landscape, on tripod or held by helper
2. Position at letter C or E of the ring (side view)
3. Full horse + rider in frame
4. Good lighting (no backlighting)
5. Record entire course, not edited clips

If the user does not follow these guidelines, Apple Vision pose detection will fail and the whole pipeline collapses. This step is non-negotiable.

---

## Analytics Events

```swift
Analytics.track("app_opened")
Analytics.track("onboarding_completed", props: ["discipline": discipline])
Analytics.track("video_recorded", props: ["duration_sec": dur])
Analytics.track("analysis_started")
Analytics.track("analysis_completed", props: ["overall_score": score, "duration_sec": dur])
Analytics.track("analysis_failed", props: ["error": err])
Analytics.track("paywall_shown", props: ["trigger": trigger])
Analytics.track("paywall_purchased", props: ["product": id])
Analytics.track("share_to_trainer_tapped")
Analytics.track("history_opened")
```

### Key funnels to monitor

1. Onboarding completion rate (target: >70%)
2. First ride recorded within 24 hours of install (target: >40%)
3. First analysis completed (target: >90% of recorded rides)
4. Free → Pro conversion (target: >5% within 7 days)
5. Day-7 retention (target: >30%)
6. Day-30 retention (target: >15%)

---

## App Store Launch

### Assets needed

- Icon: dressage-letter aesthetic, gold/navy palette
- Screenshots (6.7" required):
  1. Hero: phone with score + coaching summary
  2. Recording overlay with pose skeleton
  3. Per-jump breakdown
  4. Progress chart
  5. Share to trainer
- App preview video: 15s — record → wait → score appears
- Description hooks:
  - "Your trainer can't watch every ride. We can."
  - "Instant AI feedback on your equitation."
  - "Built by riders, for riders."

### Launch checklist

```
[ ] Cloudflare Worker deployed, OpenAI key set
[ ] App Attestation entitlement enabled
[ ] RevenueCat configured with App Store Connect IAP
[ ] Sentry crash reporting verified
[ ] PostHog events firing correctly
[ ] TestFlight beta with 10 real riders for 2 weeks
[ ] App Privacy questionnaire completed (Apple)
[ ] Marketing site: equipose.app with TestFlight link
[ ] Instagram account @equipose with 5 demo reels
[ ] Reach out to 20 equestrian micro-influencers (1k-10k followers)
[ ] Submit for App Store review (allow 2-3 days)
```

### Marketing positioning

**Do say:**
- "Get instant feedback on your position every ride."
- "Like having your trainer in your pocket."
- "Your trainer can't watch every ride. We can."

**Don't say:**
- "AI judges your hunter round with 95% accuracy" (false advertising — horse scoring is not in MVP)
- "Replaces your trainer" (it complements, not replaces)

---

## Cost Model

### Per ride
- Apple Vision: $0 (on-device)
- OpenAI GPT-4o: ~$0.10 (8 images + measurements + JSON response)
- Cloudflare Workers: $0 within free tier
- **Total: ~$0.10 / ride**

### Monthly (1,000 paying users at 5 rides/month)
- Revenue: $15,000
- OpenAI: $500
- RevenueCat: ~$150 (1% of revenue)
- Apple App Store cut: $4,500 (30%) or $2,250 (15% after year 1)
- Cloudflare: $0
- **Net: ~$9,800 — $11,800 / month**

### Hard caps to set
- OpenAI dashboard: $200/month spend limit during MVP
- Worker rate limit: 3 rides/day free, 50 rides/day Pro

### Build cost
- 1 senior iOS engineer freelance, 4 weeks: $8,000–$15,000
- Designer (part-time): $2,000
- OpenAI testing during dev: $200
- App Store + Apple Developer: $99/year
- **Total: $10,000–$18,000**

---

## Roadmap

### v1.0 — MVP launch
- Single rider position analysis
- Hunter / jumper / dressage / eventing disciplines
- Per-ride scoring and feedback
- Share to trainer (deep link)
- Subscription paywall

### v1.1 — Retention
- Progress tracking (weekly score trends)
- Side-by-side ride comparison
- Custom focus areas ("I'm working on my heels")

### v2.0 — Horse analysis
- Train custom horse-pose model
- Hunter round scoring (50–95 USEF scale)
- Per-jump form analysis (knees, bascule, takeoff distance)

### v2.5 — Live mode
- Real-time feedback while recording
- Apple Watch integration for haptic cues

### v3.0 — Community
- Trainer accounts with student roster
- Anonymous benchmarks ("how does my position compare to other adult amateurs?")
- Lesson scheduling integration

---

## Privacy & Data

- **Videos never leave the device unless you tap "Analyze."** Apple Vision pose detection runs entirely on-device.
- **Only 8 small keyframes** (not the full video) and numerical measurements are sent to the proxy.
- **No video is stored on Cloudflare or OpenAI.** The Worker forwards the request and returns the response — nothing is persisted.
- **OpenAI data retention:** Equipose uses the OpenAI API with default 30-day retention. We do not opt into training on user data.
- **No third-party trackers.** PostHog is self-hosted or EU-region only.

A full Privacy Policy must be published before App Store submission.

---

## Risks & Mitigations

| Risk | Mitigation |
|---|---|
| Apple Vision body pose noisy with dark backgrounds | Test extensively in indoor arenas; provide camera tutorial |
| GPT-4o inconsistent scoring | Return score ranges, focus on feedback text |
| Trajectory misses small jumps (crossrails) | Manual "tap jump moment" fallback |
| Bad camera angles break pipeline | Mandatory tutorial; reject videos with <60% pose confidence |
| OpenAI cost explosion from abuse | Hard cap $200/mo, App Attestation, device rate limits |
| Low conversion to Pro | First 3 free analyses generous enough to prove value |

---

## Resources

- Apple Vision: https://developer.apple.com/documentation/vision
- VNDetectHumanBodyPoseRequest: https://developer.apple.com/documentation/vision/vndetecthumanbodyposerequest
- VNDetectTrajectoriesRequest: https://developer.apple.com/documentation/vision/vndetecttrajectoriesrequest
- App Attestation: https://developer.apple.com/documentation/devicecheck
- Cloudflare Workers: https://developers.cloudflare.com/workers
- RevenueCat iOS: https://www.revenuecat.com/docs/ios
- OpenAI GPT-4o Vision: https://platform.openai.com/docs/guides/vision

---

## Next Instructions for AI Coding Agent

To start building, execute in this exact order:

1. Create Xcode project per Getting Started → step 1
2. Deploy Cloudflare Worker per Cloudflare Worker Proxy section — get the URL
3. Plug the URL into `APIClient.swift`
4. Build vertical slice: camera → record → upload → display response (Week 2)
5. Add Vision pipeline (Week 2-3)
6. Polish UI, paywall, onboarding (Week 4)

**At every step:** verify on real device (camera + Vision require it), not simulator.

**First measurable milestone:** record a 30-second ride, get a real GPT-4o response back, display the score. Aim to hit this by end of Week 2.

---

## Contact

- Product: [your-email]
- Engineering: [your-email]
- Beta access: equipose.app/beta
- Press: press@equipose.app

---

## License

Proprietary. All rights reserved.
