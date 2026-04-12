import ApplicationServices
import AppKit
import ArgumentParser
import Foundation

struct WindowCommand: ParsableCommand {
    static let configuration = CommandConfiguration(
        commandName: "window",
        abstract: "Move, resize, minimize, fullscreen, close windows",
        subcommands: [MoveWindow.self, ResizeWindow.self, MinimizeWindow.self, FullscreenWindow.self, CloseWindow.self]
    )

    struct MoveWindow: ParsableCommand {
        static let configuration = CommandConfiguration(commandName: "move")

        @Option(name: .long, help: "App name")
        var app: String

        @Option(name: .long, help: "X position")
        var x: Double

        @Option(name: .long, help: "Y position")
        var y: Double

        @Flag(name: .long, help: "Output as JSON")
        var json = false

        func run() throws {
            guard let window = getAppWindow(name: app) else {
                printError("No window found for '\(app)'")
            }
            var point = CGPoint(x: x, y: y)
            guard let value = AXValueCreate(.cgPoint, &point) else { return }
            AXUIElementSetAttributeValue(window, kAXPositionAttribute as CFString, value)

            struct MoveOutput: Codable { let action: String; let app: String; let x: Double; let y: Double }
            if json {
                printJSON(MoveOutput(action: "move", app: app, x: x, y: y))
            } else {
                print("Moved \(app) to (\(Int(x)), \(Int(y)))")
            }
        }
    }

    struct ResizeWindow: ParsableCommand {
        static let configuration = CommandConfiguration(commandName: "resize")

        @Option(name: .long, help: "App name")
        var app: String

        @Option(name: .long, help: "Width")
        var width: Double

        @Option(name: .long, help: "Height")
        var height: Double

        @Flag(name: .long, help: "Output as JSON")
        var json = false

        func run() throws {
            guard let window = getAppWindow(name: app) else {
                printError("No window found for '\(app)'")
            }
            var size = CGSize(width: width, height: height)
            guard let value = AXValueCreate(.cgSize, &size) else { return }
            AXUIElementSetAttributeValue(window, kAXSizeAttribute as CFString, value)

            struct ResizeOutput: Codable { let action: String; let app: String; let width: Double; let height: Double }
            if json {
                printJSON(ResizeOutput(action: "resize", app: app, width: width, height: height))
            } else {
                print("Resized \(app) to \(Int(width))x\(Int(height))")
            }
        }
    }

    struct MinimizeWindow: ParsableCommand {
        static let configuration = CommandConfiguration(commandName: "minimize")

        @Option(name: .long, help: "App name")
        var app: String

        @Flag(name: .long, help: "Output as JSON")
        var json = false

        func run() throws {
            guard let window = getAppWindow(name: app) else {
                printError("No window found for '\(app)'")
            }
            AXUIElementSetAttributeValue(window, kAXMinimizedAttribute as CFString, true as CFTypeRef)

            struct MinOutput: Codable { let action: String; let app: String }
            if json {
                printJSON(MinOutput(action: "minimize", app: app))
            } else {
                print("Minimized \(app)")
            }
        }
    }

    struct FullscreenWindow: ParsableCommand {
        static let configuration = CommandConfiguration(commandName: "fullscreen")

        @Option(name: .long, help: "App name")
        var app: String

        @Flag(name: .long, help: "Output as JSON")
        var json = false

        func run() throws {
            guard let window = getAppWindow(name: app) else {
                printError("No window found for '\(app)'")
            }
            var currentValue: CFTypeRef?
            AXUIElementCopyAttributeValue(window, "AXFullScreen" as CFString, &currentValue)
            let isFullscreen = (currentValue as? Bool) ?? false
            AXUIElementSetAttributeValue(window, "AXFullScreen" as CFString, (!isFullscreen) as CFTypeRef)

            struct FSOutput: Codable { let action: String; let app: String; let fullscreen: Bool }
            if json {
                printJSON(FSOutput(action: "fullscreen", app: app, fullscreen: !isFullscreen))
            } else {
                print("Toggled fullscreen for \(app)")
            }
        }
    }

    struct CloseWindow: ParsableCommand {
        static let configuration = CommandConfiguration(commandName: "close")

        @Option(name: .long, help: "App name")
        var app: String

        @Flag(name: .long, help: "Output as JSON")
        var json = false

        func run() throws {
            guard let window = getAppWindow(name: app) else {
                printError("No window found for '\(app)'")
            }
            var closeButtonRef: CFTypeRef?
            AXUIElementCopyAttributeValue(window, kAXCloseButtonAttribute as CFString, &closeButtonRef)
            if let closeButton = closeButtonRef {
                AXUIElementPerformAction(closeButton as! AXUIElement, kAXPressAction as CFString)
            }

            struct CloseOutput: Codable { let action: String; let app: String }
            if json {
                printJSON(CloseOutput(action: "close", app: app))
            } else {
                print("Closed \(app) window")
            }
        }
    }
}

private func getAppWindow(name: String) -> AXUIElement? {
    guard let pid = AccessibilityHelper.findAppPID(name: name) else { return nil }
    let app = AXUIElementCreateApplication(pid)
    var windowsRef: CFTypeRef?
    AXUIElementCopyAttributeValue(app, kAXWindowsAttribute as CFString, &windowsRef)
    guard let windows = windowsRef as? [AXUIElement], let first = windows.first else { return nil }
    return first
}
