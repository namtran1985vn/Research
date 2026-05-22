# macOS RamDisk Manager App — Full Implementation Guide

## Goal

Build a native macOS app that lets the user manage RAM disks from a clean UI:

- Create RAM disks of custom sizes
- Delete/eject RAM disks
- Save RAM disk contents to a persistent disk image
- Restore RAM disk contents on demand
- Auto-create selected RAM disks at app launch
- Start the manager at macOS login
- Optionally restore previous RAM disk contents at startup

Recommended stack:

- Swift 5.9+
- SwiftUI
- AppKit where needed
- macOS 13+ target
- Sandboxing: preferably disabled for first version, because disk utilities and file-system access are easier without sandbox restrictions

---

## Core concept

macOS can create RAM disks using:

```bash
diskutil erasevolume HFS+ "RAMDisk" $(hdiutil attach -nomount ram://SIZE_IN_512_BYTE_BLOCKS)
```

The size parameter is in 512-byte blocks.

Formula:

```text
blocks = sizeInMB * 1024 * 1024 / 512
blocks = sizeInMB * 2048
```

Examples:

```bash
# 1 GB RAM disk
hdiutil attach -nomount ram://2097152

# Format it
 diskutil erasevolume APFS "RAMDisk" /dev/diskX
```

Use APFS for modern macOS unless you specifically need HFS+ compatibility.

---

## App architecture

Suggested modules:

```text
RamDiskManagerApp/
├── App/
│   ├── RamDiskManagerApp.swift
│   └── AppDelegate.swift
├── Models/
│   ├── RamDiskConfig.swift
│   ├── MountedRamDisk.swift
│   └── BackupConfig.swift
├── Services/
│   ├── ShellService.swift
│   ├── RamDiskService.swift
│   ├── BackupService.swift
│   ├── LoginItemService.swift
│   └── SettingsStore.swift
├── ViewModels/
│   └── RamDiskViewModel.swift
├── Views/
│   ├── ContentView.swift
│   ├── RamDiskListView.swift
│   ├── CreateRamDiskView.swift
│   ├── SettingsView.swift
│   └── BackupRestoreView.swift
└── Utilities/
    ├── SizeFormatter.swift
    └── DiskParser.swift
```

---

## Data models

### RamDiskConfig

```swift
import Foundation

struct RamDiskConfig: Codable, Identifiable, Equatable {
    var id: UUID = UUID()
    var name: String
    var sizeMB: Int
    var fileSystem: FileSystemType
    var autoCreateAtLaunch: Bool
    var autoRestoreAtLaunch: Bool
    var backupImagePath: String?
}

enum FileSystemType: String, Codable, CaseIterable, Identifiable {
    case apfs = "APFS"
    case hfsPlus = "HFS+"

    var id: String { rawValue }
}
```

### MountedRamDisk

```swift
import Foundation

struct MountedRamDisk: Identifiable, Equatable {
    var id: String { deviceIdentifier }
    let name: String
    let deviceIdentifier: String
    let mountPoint: String
    let sizeDescription: String?
}
```

---

## Shell execution service

Use `Process` to run native macOS tools.

```swift
import Foundation

struct ShellResult {
    let stdout: String
    let stderr: String
    let exitCode: Int32
}

final class ShellService {
    func run(_ launchPath: String, arguments: [String]) async throws -> ShellResult {
        try await withCheckedThrowingContinuation { continuation in
            let process = Process()
            process.executableURL = URL(fileURLWithPath: launchPath)
            process.arguments = arguments

            let stdoutPipe = Pipe()
            let stderrPipe = Pipe()
            process.standardOutput = stdoutPipe
            process.standardError = stderrPipe

            process.terminationHandler = { process in
                let stdoutData = stdoutPipe.fileHandleForReading.readDataToEndOfFile()
                let stderrData = stderrPipe.fileHandleForReading.readDataToEndOfFile()

                let stdout = String(data: stdoutData, encoding: .utf8) ?? ""
                let stderr = String(data: stderrData, encoding: .utf8) ?? ""

                continuation.resume(returning: ShellResult(
                    stdout: stdout,
                    stderr: stderr,
                    exitCode: process.terminationStatus
                ))
            }

            do {
                try process.run()
            } catch {
                continuation.resume(throwing: error)
            }
        }
    }
}
```

Use absolute paths:

```text
/usr/bin/hdiutil
/usr/sbin/diskutil
/bin/mkdir
/bin/rm
/bin/cp
/usr/bin/ditto
```

---

## Create RAM disk

### Steps

1. Convert size MB to 512-byte blocks.
2. Run `hdiutil attach -nomount ram://BLOCKS`.
3. Parse returned device path, e.g. `/dev/disk4`.
4. Format it with `diskutil erasevolume APFS NAME /dev/disk4`.
5. Return mount point, usually `/Volumes/NAME`.

### RamDiskService

```swift
import Foundation

final class RamDiskService {
    private let shell: ShellService

    init(shell: ShellService = ShellService()) {
        self.shell = shell
    }

    func createRamDisk(name: String, sizeMB: Int, fileSystem: FileSystemType) async throws -> MountedRamDisk {
        let blocks = sizeMB * 2048

        let attachResult = try await shell.run(
            "/usr/bin/hdiutil",
            arguments: ["attach", "-nomount", "ram://\(blocks)"]
        )

        guard attachResult.exitCode == 0 else {
            throw RamDiskError.commandFailed(attachResult.stderr)
        }

        let device = attachResult.stdout
            .split(separator: "\n")
            .first?
            .trimmingCharacters(in: .whitespacesAndNewlines)

        guard let device, device.hasPrefix("/dev/disk") else {
            throw RamDiskError.unableToParseDevice(attachResult.stdout)
        }

        let fs = fileSystem.rawValue

        let formatResult = try await shell.run(
            "/usr/sbin/diskutil",
            arguments: ["erasevolume", fs, name, device]
        )

        guard formatResult.exitCode == 0 else {
            throw RamDiskError.commandFailed(formatResult.stderr)
        }

        let mountPoint = "/Volumes/\(name)"

        return MountedRamDisk(
            name: name,
            deviceIdentifier: device,
            mountPoint: mountPoint,
            sizeDescription: "\(sizeMB) MB"
        )
    }

    func deleteRamDisk(deviceIdentifier: String) async throws {
        let result = try await shell.run(
            "/usr/sbin/diskutil",
            arguments: ["eject", deviceIdentifier]
        )

        guard result.exitCode == 0 else {
            throw RamDiskError.commandFailed(result.stderr)
        }
    }
}

enum RamDiskError: LocalizedError {
    case commandFailed(String)
    case unableToParseDevice(String)
    case mountPointNotFound(String)

    var errorDescription: String? {
        switch self {
        case .commandFailed(let message):
            return "Command failed: \(message)"
        case .unableToParseDevice(let output):
            return "Unable to parse RAM disk device from output: \(output)"
        case .mountPointNotFound(let name):
            return "Mount point not found for \(name)"
        }
    }
}
```

---

## List mounted RAM disks

You need to detect disks created from RAM.

Useful commands:

```bash
diskutil list
hdiutil info
mount
```

`hdiutil info` can show attached images and RAM disks. For MVP, track RAM disks created by your app in local settings. For a stronger version, parse system output and match `/Volumes/<name>`.

Simple practical approach:

- Keep app-created disks in memory after creation.
- Save configs in `UserDefaults`.
- On app launch, check if `/Volumes/<name>` exists.
- If it exists, treat it as mounted.

```swift
func volumeExists(name: String) -> Bool {
    FileManager.default.fileExists(atPath: "/Volumes/\(name)")
}
```

For a more robust check, run:

```bash
diskutil info /Volumes/RAMDisk
```

Then parse:

```text
Device Node: /dev/disk4
Volume Name: RAMDisk
Mount Point: /Volumes/RAMDisk
```

---

## Save RAM disk contents

There are two main strategies.

### Strategy A: Save as folder copy

Pros:

- Simple
- Easy to inspect
- Easy to restore

Cons:

- Slower for many tiny files
- Does not preserve everything perfectly unless using `ditto`

Use:

```bash
ditto /Volumes/RAMDisk /path/to/backup/RAMDiskBackup
```

### Strategy B: Save as DMG

Pros:

- Single file
- Cleaner backup
- Easier to restore exactly

Cons:

- Slightly more complex

Create compressed DMG:

```bash
hdiutil create -srcfolder /Volumes/RAMDisk -format UDZO /path/to/RAMDiskBackup.dmg
```

For this app, use DMG as the main save format.

---

## BackupService

```swift
import Foundation

final class BackupService {
    private let shell: ShellService

    init(shell: ShellService = ShellService()) {
        self.shell = shell
    }

    func saveToDMG(volumePath: String, outputDMGPath: String) async throws {
        let result = try await shell.run(
            "/usr/bin/hdiutil",
            arguments: [
                "create",
                "-srcfolder", volumePath,
                "-format", "UDZO",
                outputDMGPath
            ]
        )

        guard result.exitCode == 0 else {
            throw RamDiskError.commandFailed(result.stderr)
        }
    }

    func restoreFromDMG(dmgPath: String, destinationVolumePath: String) async throws {
        let attachResult = try await shell.run(
            "/usr/bin/hdiutil",
            arguments: ["attach", dmgPath, "-nobrowse"]
        )

        guard attachResult.exitCode == 0 else {
            throw RamDiskError.commandFailed(attachResult.stderr)
        }

        let mountedPath = try parseMountedPath(from: attachResult.stdout)

        let copyResult = try await shell.run(
            "/usr/bin/ditto",
            arguments: [mountedPath, destinationVolumePath]
        )

        let _ = try await shell.run(
            "/usr/bin/hdiutil",
            arguments: ["detach", mountedPath]
        )

        guard copyResult.exitCode == 0 else {
            throw RamDiskError.commandFailed(copyResult.stderr)
        }
    }

    private func parseMountedPath(from output: String) throws -> String {
        let lines = output.split(separator: "\n").map(String.init)

        for line in lines {
            if let range = line.range(of: "/Volumes/") {
                return String(line[range.lowerBound...]).trimmingCharacters(in: .whitespacesAndNewlines)
            }
        }

        throw RamDiskError.mountPointNotFound(output)
    }
}
```

---

## Restore workflow

When restoring:

1. Create RAM disk first.
2. Attach backup DMG.
3. Copy DMG contents into RAM disk using `ditto`.
4. Detach DMG.

Pseudo-flow:

```swift
let ramDisk = try await ramDiskService.createRamDisk(
    name: config.name,
    sizeMB: config.sizeMB,
    fileSystem: config.fileSystem
)

if config.autoRestoreAtLaunch, let backupPath = config.backupImagePath {
    try await backupService.restoreFromDMG(
        dmgPath: backupPath,
        destinationVolumePath: ramDisk.mountPoint
    )
}
```

---

## Settings persistence

Use JSON file in Application Support instead of only UserDefaults.

Path:

```text
~/Library/Application Support/RamDiskManager/configs.json
```

### SettingsStore

```swift
import Foundation

final class SettingsStore {
    private var configURL: URL {
        let appSupport = FileManager.default.urls(for: .applicationSupportDirectory, in: .userDomainMask)[0]
        let dir = appSupport.appendingPathComponent("RamDiskManager", isDirectory: true)
        try? FileManager.default.createDirectory(at: dir, withIntermediateDirectories: true)
        return dir.appendingPathComponent("configs.json")
    }

    func loadConfigs() -> [RamDiskConfig] {
        guard let data = try? Data(contentsOf: configURL) else { return [] }
        return (try? JSONDecoder().decode([RamDiskConfig].self, from: data)) ?? []
    }

    func saveConfigs(_ configs: [RamDiskConfig]) {
        guard let data = try? JSONEncoder().encode(configs) else { return }
        try? data.write(to: configURL, options: .atomic)
    }
}
```

---

## Start at login

Use `ServiceManagement`.

For modern macOS:

```swift
import ServiceManagement

final class LoginItemService {
    func enableLaunchAtLogin() throws {
        try SMAppService.mainApp.register()
    }

    func disableLaunchAtLogin() throws {
        try SMAppService.mainApp.unregister()
    }

    var isEnabled: Bool {
        SMAppService.mainApp.status == .enabled
    }
}
```

You need proper app signing for this to work reliably outside debug builds.

---

## Auto-create RAM disks at app launch

In your app startup:

```swift
@main
struct RamDiskManagerApp: App {
    @StateObject private var viewModel = RamDiskViewModel()

    var body: some Scene {
        WindowGroup {
            ContentView()
                .environmentObject(viewModel)
                .task {
                    await viewModel.handleAppLaunch()
                }
        }
    }
}
```

ViewModel:

```swift
import Foundation
import SwiftUI

@MainActor
final class RamDiskViewModel: ObservableObject {
    @Published var configs: [RamDiskConfig] = []
    @Published var mountedDisks: [MountedRamDisk] = []
    @Published var errorMessage: String?
    @Published var isWorking = false

    private let settingsStore = SettingsStore()
    private let ramDiskService = RamDiskService()
    private let backupService = BackupService()

    init() {
        configs = settingsStore.loadConfigs()
    }

    func handleAppLaunch() async {
        for config in configs where config.autoCreateAtLaunch {
            await createFromConfig(config)
        }
    }

    func createFromConfig(_ config: RamDiskConfig) async {
        isWorking = true
        defer { isWorking = false }

        do {
            let disk = try await ramDiskService.createRamDisk(
                name: config.name,
                sizeMB: config.sizeMB,
                fileSystem: config.fileSystem
            )

            mountedDisks.append(disk)

            if config.autoRestoreAtLaunch, let backupPath = config.backupImagePath {
                try await backupService.restoreFromDMG(
                    dmgPath: backupPath,
                    destinationVolumePath: disk.mountPoint
                )
            }
        } catch {
            errorMessage = error.localizedDescription
        }
    }

    func delete(_ disk: MountedRamDisk) async {
        do {
            try await ramDiskService.deleteRamDisk(deviceIdentifier: disk.deviceIdentifier)
            mountedDisks.removeAll { $0.id == disk.id }
        } catch {
            errorMessage = error.localizedDescription
        }
    }

    func saveConfigs() {
        settingsStore.saveConfigs(configs)
    }
}
```

---

## SwiftUI UI design

### Main screen

Show:

- Mounted RAM disks
- Saved RAM disk profiles
- Create button
- Save backup button
- Restore button
- Delete/eject button
- Settings button

### ContentView sketch

```swift
import SwiftUI

struct ContentView: View {
    @EnvironmentObject var viewModel: RamDiskViewModel
    @State private var showingCreateSheet = false

    var body: some View {
        NavigationSplitView {
            List {
                Section("Mounted RAM Disks") {
                    ForEach(viewModel.mountedDisks) { disk in
                        VStack(alignment: .leading) {
                            Text(disk.name).font(.headline)
                            Text(disk.mountPoint).font(.caption)
                        }
                    }
                }

                Section("Profiles") {
                    ForEach(viewModel.configs) { config in
                        VStack(alignment: .leading) {
                            Text(config.name).font(.headline)
                            Text("\(config.sizeMB) MB • \(config.fileSystem.rawValue)")
                                .font(.caption)
                        }
                    }
                }
            }
        } detail: {
            VStack(spacing: 20) {
                Text("RamDisk Manager")
                    .font(.largeTitle)
                    .bold()

                Button("Create RAM Disk") {
                    showingCreateSheet = true
                }

                if viewModel.isWorking {
                    ProgressView()
                }
            }
            .padding()
        }
        .sheet(isPresented: $showingCreateSheet) {
            CreateRamDiskView()
                .environmentObject(viewModel)
        }
        .alert("Error", isPresented: .constant(viewModel.errorMessage != nil)) {
            Button("OK") { viewModel.errorMessage = nil }
        } message: {
            Text(viewModel.errorMessage ?? "")
        }
    }
}
```

### CreateRamDiskView sketch

```swift
import SwiftUI

struct CreateRamDiskView: View {
    @EnvironmentObject var viewModel: RamDiskViewModel
    @Environment(\.dismiss) private var dismiss

    @State private var name = "RAMDisk"
    @State private var sizeMB = 4096
    @State private var fileSystem: FileSystemType = .apfs
    @State private var autoCreateAtLaunch = false
    @State private var autoRestoreAtLaunch = false

    var body: some View {
        Form {
            TextField("Name", text: $name)

            Stepper("Size: \(sizeMB) MB", value: $sizeMB, in: 128...65536, step: 128)

            Picker("File System", selection: $fileSystem) {
                ForEach(FileSystemType.allCases) { fs in
                    Text(fs.rawValue).tag(fs)
                }
            }

            Toggle("Auto-create at app launch", isOn: $autoCreateAtLaunch)
            Toggle("Auto-restore at app launch", isOn: $autoRestoreAtLaunch)

            HStack {
                Button("Cancel") { dismiss() }
                Spacer()
                Button("Create") {
                    let config = RamDiskConfig(
                        name: name,
                        sizeMB: sizeMB,
                        fileSystem: fileSystem,
                        autoCreateAtLaunch: autoCreateAtLaunch,
                        autoRestoreAtLaunch: autoRestoreAtLaunch,
                        backupImagePath: nil
                    )

                    viewModel.configs.append(config)
                    viewModel.saveConfigs()

                    Task {
                        await viewModel.createFromConfig(config)
                        dismiss()
                    }
                }
            }
        }
        .padding()
        .frame(width: 420)
    }
}
```

---

## Backup UI

Use `NSOpenPanel` and `NSSavePanel`.

### Select backup destination

```swift
import AppKit

func chooseSavePath(defaultName: String) -> String? {
    let panel = NSSavePanel()
    panel.nameFieldStringValue = "\(defaultName).dmg"
    panel.allowedContentTypes = [.diskImage]

    if panel.runModal() == .OK {
        return panel.url?.path
    }

    return nil
}
```

### Select DMG to restore

```swift
import AppKit
import UniformTypeIdentifiers

func chooseDMGPath() -> String? {
    let panel = NSOpenPanel()
    panel.allowedContentTypes = [.diskImage]
    panel.allowsMultipleSelection = false
    panel.canChooseDirectories = false

    if panel.runModal() == .OK {
        return panel.url?.path
    }

    return nil
}
```

---

## Permissions and app sandboxing

For easiest implementation:

- Disable App Sandbox in Signing & Capabilities for MVP.
- Sign the app with a Developer ID or local development certificate.
- Use hardened runtime later if distributing outside the App Store.

If sandboxed:

- You need security-scoped bookmarks for backup paths.
- Shelling out to system tools may become more restricted.
- Login item behavior may require additional configuration.

Recommendation:

- MVP: non-sandboxed app.
- Later: hardened runtime + notarization.

---

## Important edge cases

### 1. Duplicate volume names

If `/Volumes/RAMDisk` already exists, macOS may mount as:

```text
/Volumes/RAMDisk 1
```

Do not assume mount path. Parse `diskutil info` after creation or check actual volume path.

### 2. Not enough memory

Before creating a RAM disk, check memory pressure or available memory.

Use:

```bash
vm_stat
memory_pressure
```

MVP can simply warn if RAM disk size is too large.

Rule of thumb:

```text
Do not allow RAM disk larger than 50% of physical RAM by default.
```

### 3. Data loss

RAM disks are volatile. Show clear warning:

```text
Data in RAM disks is lost after restart, shutdown, crash, or eject unless saved.
```

### 4. Restore too large

Backup contents may exceed RAM disk size. Check size before restore.

Use:

```bash
du -sm /path/to/source
```

### 5. Eject failure

If files are open, `diskutil eject` may fail.

Show message:

```text
Cannot eject. Some files may still be in use.
```

Optional force detach:

```bash
hdiutil detach /dev/diskX -force
```

Only expose force eject behind confirmation.

---

## Menu bar app option

A RAM disk manager is useful as a menu bar utility.

Add:

```swift
MenuBarExtra("RamDisk", systemImage: "memorychip") {
    Button("Create RAM Disk") {}
    Button("Save All") {}
    Button("Restore All") {}
    Divider()
    Button("Quit") {
        NSApplication.shared.terminate(nil)
    }
}
```

This can live alongside the main window.

---

## Recommended MVP feature set

Build in this order:

1. Create RAM disk
2. Eject/delete RAM disk
3. Save RAM disk profile
4. Auto-create profile at app launch
5. Save RAM disk to DMG
6. Restore DMG into RAM disk
7. Launch at login
8. Menu bar control
9. Memory safety warnings
10. Force eject and advanced settings

---

## CLI commands reference

### Create raw RAM disk device

```bash
hdiutil attach -nomount ram://BLOCKS
```

### Format RAM disk

```bash
diskutil erasevolume APFS "RAMDisk" /dev/diskX
```

### Eject RAM disk

```bash
diskutil eject /dev/diskX
```

### Force detach

```bash
hdiutil detach /dev/diskX -force
```

### Save RAM disk to DMG

```bash
hdiutil create -srcfolder /Volumes/RAMDisk -format UDZO ~/Desktop/RAMDiskBackup.dmg
```

### Restore from mounted DMG

```bash
ditto /Volumes/BackupSource /Volumes/RAMDisk
```

### Check disk info

```bash
diskutil info /Volumes/RAMDisk
```

---

## Suggested UX copy

### Warning before creating

```text
RAM disks use real system memory. Creating a large RAM disk can reduce performance or cause swapping.
```

### Warning before deleting

```text
Deleting this RAM disk will immediately remove its contents unless you save a backup first.
```

### Auto-restore explanation

```text
When enabled, this profile will be recreated when the app launches and restored from its selected backup image.
```

---

## Testing checklist

Test these cases:

- Create 512 MB RAM disk
- Create 4 GB RAM disk
- Create duplicate name
- Eject mounted RAM disk
- Try eject while file is open
- Save to DMG
- Restore DMG into new RAM disk
- Restart app and auto-create profile
- Enable launch at login
- Reboot and confirm startup behavior
- Try oversized RAM disk
- Try missing backup path
- Try corrupted DMG

---

## Security notes

This app should never run arbitrary user-provided shell commands.

Only allow controlled commands with validated arguments:

- RAM disk name: sanitize characters
- Size: numeric range only
- File system: enum only
- Backup path: selected through panel or stored security-scoped bookmark if sandboxed

Name validation example:

```swift
func sanitizedVolumeName(_ input: String) -> String {
    input
        .filter { $0.isLetter || $0.isNumber || $0 == " " || $0 == "-" || $0 == "_" }
        .trimmingCharacters(in: .whitespacesAndNewlines)
}
```

---

## Final recommendation

For your first version, build a simple non-sandboxed SwiftUI app with:

- Profile-based RAM disk creation
- DMG backup/restore
- Launch at login
- Menu bar quick controls

Avoid overengineering system-wide disk discovery in v1. Track disks created by the app, and add advanced detection later.
