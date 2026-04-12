import AppKit
import ArgumentParser
import Foundation

struct ClipboardCommand: ParsableCommand {
    static let configuration = CommandConfiguration(
        commandName: "clipboard",
        abstract: "Read/write system clipboard",
        subcommands: [ReadClipboard.self, WriteClipboard.self],
        defaultSubcommand: ReadClipboard.self
    )

    struct ReadClipboard: ParsableCommand {
        static let configuration = CommandConfiguration(commandName: "read")

        @Flag(name: .long, help: "Output as JSON")
        var json = false

        func run() {
            let content = NSPasteboard.general.string(forType: .string)

            if json {
                printJSON(["content": content])
            } else {
                print(content ?? "(empty clipboard)")
            }
        }
    }

    struct WriteClipboard: ParsableCommand {
        static let configuration = CommandConfiguration(commandName: "write")

        @Argument(help: "Text to write to clipboard")
        var text: String

        @Flag(name: .long, help: "Output as JSON")
        var json = false

        func run() {
            NSPasteboard.general.clearContents()
            NSPasteboard.general.setString(text, forType: .string)

            if json {
                printJSON(["written": text])
            } else {
                print("Copied to clipboard: \"\(text)\"")
            }
        }
    }
}
