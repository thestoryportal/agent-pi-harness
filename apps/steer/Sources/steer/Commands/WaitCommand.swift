import AppKit
import ArgumentParser
import Foundation

struct WaitCommand: ParsableCommand {
    static let configuration = CommandConfiguration(
        commandName: "wait",
        abstract: "Wait for app launch or element to appear"
    )

    @Option(name: .long, help: "App name to wait for")
    var app: String?

    @Option(name: .long, help: "Text to wait for in elements")
    var `for`: String?

    @Option(name: .long, help: "Timeout in seconds (default: 30)")
    var timeout: Double = 30.0

    @Option(name: .long, help: "Polling interval in seconds (default: 1)")
    var interval: Double = 1.0

    @Flag(name: .long, help: "Output as JSON")
    var json = false

    func run() throws {
        // Validate inputs: --for requires --app so we can re-query the live AX tree.
        // Without --app the previous behavior read a stale on-disk snapshot that
        // never refreshed, leading to false positives or infinite spins.
        if app == nil && self.`for` == nil {
            printError("wait requires --app and/or --for")
        }
        if app == nil && self.`for` != nil {
            printError("--for requires --app (cannot search elements without an app context)")
        }

        // Floor the polling interval to prevent CPU exhaustion via small or
        // negative values. Each iteration walks the full AX tree (up to depth 40),
        // so an interval of 0 or 0.001 turns this into a tight spin that consumes
        // 100% CPU and stalls system-wide AX operations until --timeout fires.
        let effectiveInterval = max(interval, 0.1)

        let start = Date()
        let deadline = start.addingTimeInterval(timeout)

        // Loop structure: check the condition first, then sleep only if there's
        // time remaining. Previous loop structure (`while elapsed < timeout`)
        // checked the condition before the sleep, meaning the last iteration
        // started near `timeout - interval` and the deadline could be missed
        // by up to `interval` seconds.
        while true {
            guard let appName = app else { break }
            let running = NSWorkspace.shared.runningApplications
            let found = running.contains { $0.localizedName?.localizedCaseInsensitiveContains(appName) == true }

            if found {
                if let searchText = self.`for` {
                    // Re-query the live AX tree on every iteration to avoid stale state.
                    if let pid = AccessibilityHelper.findAppPID(name: appName) {
                        let elements = AccessibilityHelper.buildTree(pid: pid)
                        let q = searchText.lowercased()
                        let match = elements.contains {
                            ($0.label?.lowercased().contains(q) ?? false) ||
                            ($0.value?.lowercased().contains(q) ?? false)
                        }
                        if match {
                            outputSuccess(target: searchText, elapsed: Date().timeIntervalSince(start))
                            return
                        }
                    }
                } else {
                    outputSuccess(target: appName, elapsed: Date().timeIntervalSince(start))
                    return
                }
            }

            let now = Date()
            if now >= deadline { break }
            // Sleep for `effectiveInterval` or remaining time, whichever is
            // shorter, so we never overshoot the deadline.
            let remaining = deadline.timeIntervalSince(now)
            Thread.sleep(forTimeInterval: min(effectiveInterval, remaining))
        }

        let target = self.`for` ?? app ?? "unknown"
        struct TimeoutOutput: Codable {
            let waitedFor: String
            let found: Bool
            let elapsed: Double
            let error: String
        }
        let output = TimeoutOutput(waitedFor: target, found: false, elapsed: timeout, error: "timeout")
        if json {
            printJSON(output)
        } else {
            print("Timeout: '\(target)' not found after \(String(format: "%.1f", timeout))s")
        }
        throw ExitCode(1)
    }

    private func outputSuccess(target: String, elapsed: Double) {
        struct WaitOutput: Codable {
            let waitedFor: String
            let found: Bool
            let elapsed: Double
        }
        let output = WaitOutput(waitedFor: target, found: true, elapsed: elapsed)
        if json {
            printJSON(output)
        } else {
            print("Found '\(target)' after \(String(format: "%.1f", elapsed))s")
        }
    }
}
