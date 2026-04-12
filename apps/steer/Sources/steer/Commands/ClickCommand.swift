import ArgumentParser
import Foundation

struct ClickCommand: ParsableCommand {
    static let configuration = CommandConfiguration(
        commandName: "click",
        abstract: "Click by element ID, label, or coordinates"
    )

    @Option(name: .long, help: "Element ID (e.g., B1, T2, O3)")
    var id: String?

    @Option(name: .long, help: "Click element matching text label")
    var text: String?

    @Option(name: .long, help: "X coordinate")
    var x: Double?

    @Option(name: .long, help: "Y coordinate")
    var y: Double?

    @Flag(name: .long, help: "Output as JSON")
    var json = false

    func run() throws {
        let clickX: Double
        let clickY: Double

        if let elementID = id {
            guard let coords = SnapshotStore.resolveElement(id: elementID) else {
                printError("Element '\(elementID)' not found in current snapshot")
            }
            clickX = coords.x
            clickY = coords.y
        } else if let searchText = text {
            let matches = SnapshotStore.findByText(searchText)
            if let first = matches.first {
                clickX = first.x + first.width / 2
                clickY = first.y + first.height / 2
                try InputHelper.mouseClick(x: clickX, y: clickY)
                outputResult(x: clickX, y: clickY, element: first.id)
                return
            }
            // Try OCR store
            let ocrElements = OCRHelper.loadStoredElements()
            let q = searchText.lowercased()
            guard let ocrMatch = ocrElements.first(where: { $0.text.lowercased().contains(q) }) else {
                printError("No element matching '\(searchText)' found")
            }
            clickX = ocrMatch.x + ocrMatch.width / 2
            clickY = ocrMatch.y + ocrMatch.height / 2
            try InputHelper.mouseClick(x: clickX, y: clickY)
            outputResult(x: clickX, y: clickY, element: ocrMatch.id)
            return
        } else if let cx = x, let cy = y {
            clickX = cx
            clickY = cy
        } else {
            printError("Provide --id, --text, or --x/--y coordinates")
        }

        try InputHelper.mouseClick(x: clickX, y: clickY)
        outputResult(x: clickX, y: clickY, element: id)
    }

    private func outputResult(x: Double, y: Double, element: String?) {
        struct ClickOutput: Codable {
            let action: String
            let x: Double
            let y: Double
            let element: String?
        }
        let output = ClickOutput(action: "click", x: x, y: y, element: element)
        if json {
            printJSON(output)
        } else {
            print("Clicked at (\(Int(x)), \(Int(y)))")
        }
    }
}
