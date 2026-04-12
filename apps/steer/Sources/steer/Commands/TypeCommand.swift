import ArgumentParser
import Foundation

struct TypeCommand: ParsableCommand {
    static let configuration = CommandConfiguration(
        commandName: "type",
        abstract: "Type text into focused element or a target"
    )

    @Argument(help: "Text to type")
    var text: String

    @Option(name: .long, help: "Element ID to click first, then type")
    var into: String?

    @Flag(name: .long, help: "Output as JSON")
    var json = false

    func run() throws {
        if let elementID = into {
            guard let coords = SnapshotStore.resolveElement(id: elementID) else {
                printError("Element '\(elementID)' not found in current snapshot")
            }
            try InputHelper.mouseClick(x: coords.x, y: coords.y)
            Thread.sleep(forTimeInterval: 0.1)
        }

        try InputHelper.typeText(text)

        // Do NOT echo the typed text in output. `steer type` is commonly used to
        // type passwords, API keys, and 2FA codes — embedding the value in JSON
        // would leak it to session logs, hook events, and stdout consumers.
        // Report only the length so callers can verify the type completed without
        // exposing the content.
        struct TypeOutput: Codable {
            let action: String
            let charsTyped: Int
            let into: String?
        }

        let output = TypeOutput(action: "type", charsTyped: text.count, into: into)
        if json {
            printJSON(output)
        } else {
            print("Typed \(text.count) character\(text.count == 1 ? "" : "s")")
        }
    }
}
