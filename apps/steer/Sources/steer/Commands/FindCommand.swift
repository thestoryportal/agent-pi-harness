import ArgumentParser
import Foundation

struct FindCommand: ParsableCommand {
    static let configuration = CommandConfiguration(
        commandName: "find",
        abstract: "Search elements by text in latest snapshot"
    )

    @Argument(help: "Text to search for")
    var query: String

    @Flag(name: .long, help: "Output as JSON")
    var json = false

    func run() {
        let matches = SnapshotStore.findByText(query)

        // Also check OCR store
        let ocrElements = OCRHelper.loadStoredElements()
        let q = query.lowercased()
        let ocrMatches = ocrElements.filter { $0.text.lowercased().contains(q) }

        struct FindOutput: Codable {
            let query: String
            let matches: [AXElement]
            let ocrMatches: [OCRElement]?
        }

        let output = FindOutput(
            query: query,
            matches: matches,
            ocrMatches: ocrMatches.isEmpty ? nil : ocrMatches
        )

        if json {
            printJSON(output)
        } else {
            if matches.isEmpty && ocrMatches.isEmpty {
                print("No matches for '\(query)'")
            } else {
                for m in matches {
                    print("\(m.id): \(m.role) — \(m.label ?? "")")
                }
                for o in ocrMatches {
                    print("\(o.id): \"\(o.text)\" at (\(Int(o.x)), \(Int(o.y)))")
                }
            }
        }
    }
}
