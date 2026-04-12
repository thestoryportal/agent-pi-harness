import ArgumentParser
import Foundation

struct FocusCommand: ParsableCommand {
    static let configuration = CommandConfiguration(
        commandName: "focus",
        abstract: "Show currently focused element"
    )

    @Flag(name: .long, help: "Output as JSON")
    var json = false

    func run() {
        guard let element = AccessibilityHelper.getFocusedElement() else {
            if json {
                struct NoFocus: Codable { let focused: Bool }
                printJSON(NoFocus(focused: false))
            } else {
                print("No focused element found")
            }
            return
        }

        if json {
            printJSON(element)
        } else {
            print("\(element.id): \(element.role) — \(element.label ?? "(no label)")")
        }
    }
}
