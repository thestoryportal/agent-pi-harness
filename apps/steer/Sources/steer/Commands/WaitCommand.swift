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
        let start = Date()

        while Date().timeIntervalSince(start) < timeout {
            if let appName = app {
                let running = NSWorkspace.shared.runningApplications
                let found = running.contains { $0.localizedName?.localizedCaseInsensitiveContains(appName) == true }

                if found {
                    if let searchText = self.`for` {
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
            } else if let searchText = self.`for` {
                // Search without app context — use stored snapshot
                let matches = SnapshotStore.findByText(searchText)
                if !matches.isEmpty {
                    outputSuccess(target: searchText, elapsed: Date().timeIntervalSince(start))
                    return
                }
            }

            Thread.sleep(forTimeInterval: interval)
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
