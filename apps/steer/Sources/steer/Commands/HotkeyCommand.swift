import ArgumentParser
import Foundation

struct HotkeyCommand: ParsableCommand {
    static let configuration = CommandConfiguration(
        commandName: "hotkey",
        abstract: "Send keyboard shortcuts (cmd+s, return, escape, etc.)"
    )

    @Argument(help: "Key combination (e.g., cmd+s, return, cmd+shift+t)")
    var combo: String

    @Flag(name: .long, help: "Output as JSON")
    var json = false

    func run() throws {
        try InputHelper.sendHotkey(combo: combo)

        struct HotkeyOutput: Codable {
            let action: String
            let combo: String
        }

        let output = HotkeyOutput(action: "hotkey", combo: combo)
        if json {
            printJSON(output)
        } else {
            print("Sent hotkey: \(combo)")
        }
    }
}
