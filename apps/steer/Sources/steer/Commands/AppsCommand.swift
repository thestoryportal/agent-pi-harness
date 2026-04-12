import AppKit
import ArgumentParser
import Foundation

struct AppsCommand: ParsableCommand {
    static let configuration = CommandConfiguration(
        commandName: "apps",
        abstract: "List, launch, or activate apps",
        subcommands: [ListApps.self, LaunchApp.self, ActivateApp.self],
        defaultSubcommand: ListApps.self
    )

    struct ListApps: ParsableCommand {
        static let configuration = CommandConfiguration(commandName: "list")

        @Flag(name: .long, help: "Output as JSON")
        var json = false

        func run() {
            let apps = NSWorkspace.shared.runningApplications
                .filter { $0.activationPolicy == .regular }

            struct AppInfo: Codable {
                let name: String
                let pid: Int32
                let bundle: String?
                let active: Bool
            }

            let infos = apps.map { app in
                AppInfo(
                    name: app.localizedName ?? "Unknown",
                    pid: app.processIdentifier,
                    bundle: app.bundleIdentifier,
                    active: app.isActive
                )
            }

            if json {
                printJSON(["apps": infos])
            } else {
                for app in infos {
                    let marker = app.active ? " *" : ""
                    print("\(app.name) (pid: \(app.pid))\(marker)")
                }
            }
        }
    }

    struct LaunchApp: ParsableCommand {
        static let configuration = CommandConfiguration(commandName: "launch")

        @Argument(help: "App name to launch")
        var name: String

        @Flag(name: .long, help: "Output as JSON")
        var json = false

        func run() throws {
            // Reject path traversal and shell metacharacters in app name.
            // Allowed: letters, numbers, spaces, hyphens, underscores, dots (but not "..").
            let allowedChars = CharacterSet.alphanumerics
                .union(CharacterSet(charactersIn: " -_."))
            if name.isEmpty || name.contains("/") || name.contains("\0")
                || name.contains("..") || name.hasPrefix(".")
                || name.unicodeScalars.contains(where: { !allowedChars.contains($0) }) {
                printError("Invalid app name: '\(name)' (must contain only letters, numbers, spaces, hyphens, underscores, dots; no path separators)")
            }

            let path = "/Applications/\(name).app"
            let resolvedURL = URL(fileURLWithPath: path).standardizedFileURL
            // Defense in depth: resolved path must still be inside /Applications
            if !resolvedURL.path.hasPrefix("/Applications/") {
                printError("App path escapes /Applications: \(resolvedURL.path)")
            }
            let url = resolvedURL

            let semaphore = DispatchSemaphore(value: 0)
            var launchError: Error?

            NSWorkspace.shared.openApplication(
                at: url,
                configuration: NSWorkspace.OpenConfiguration()
            ) { _, error in
                launchError = error
                semaphore.signal()
            }

            _ = semaphore.wait(timeout: .now() + 5.0)

            if let error = launchError {
                printError("Failed to launch \(name): \(error.localizedDescription)")
            }

            struct LaunchOutput: Codable {
                let action: String
                let app: String
            }

            if json {
                printJSON(LaunchOutput(action: "launch", app: name))
            } else {
                print("Launched \(name)")
            }
        }
    }

    struct ActivateApp: ParsableCommand {
        static let configuration = CommandConfiguration(commandName: "activate")

        @Argument(help: "App name to activate")
        var name: String

        @Flag(name: .long, help: "Output as JSON")
        var json = false

        func run() {
            let apps = NSWorkspace.shared.runningApplications
            guard let app = apps.first(where: {
                $0.localizedName?.localizedCaseInsensitiveContains(name) == true
            }) else {
                if json {
                    printError("App '\(name)' not found")
                } else {
                    print("Error: App '\(name)' not found")
                    return
                }
            }

            app.activate()

            struct ActivateOutput: Codable {
                let action: String
                let app: String
                let pid: Int32
            }

            if json {
                printJSON(ActivateOutput(action: "activate", app: app.localizedName ?? name, pid: app.processIdentifier))
            } else {
                print("Activated \(app.localizedName ?? name)")
            }
        }
    }
}
