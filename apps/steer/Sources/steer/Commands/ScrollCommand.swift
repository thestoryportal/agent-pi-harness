import ArgumentParser
import Foundation

struct ScrollCommand: ParsableCommand {
    static let configuration = CommandConfiguration(
        commandName: "scroll",
        abstract: "Scroll up/down/left/right"
    )

    @Option(name: .long, help: "Direction: up, down, left, right")
    var direction: String = "down"

    @Option(name: .long, help: "Scroll amount in pixels (default: 3)")
    var amount: Int = 3

    @Option(name: .long, help: "App name (scroll in app's front window center)")
    var app: String?

    @Option(name: .long, help: "X coordinate")
    var x: Double?

    @Option(name: .long, help: "Y coordinate")
    var y: Double?

    @Flag(name: .long, help: "Output as JSON")
    var json = false

    func run() throws {
        try InputHelper.scroll(direction: direction, amount: amount, x: x, y: y)

        struct ScrollOutput: Codable {
            let action: String
            let direction: String
            let amount: Int
        }

        let output = ScrollOutput(action: "scroll", direction: direction, amount: amount)
        if json {
            printJSON(output)
        } else {
            print("Scrolled \(direction) by \(amount)")
        }
    }
}
