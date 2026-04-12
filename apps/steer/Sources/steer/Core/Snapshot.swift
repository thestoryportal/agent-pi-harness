import Foundation

struct Snapshot: Codable {
    let app: String?
    let screenshot: String
    let elements: [AXElement]
    let ocrElements: [OCRElement]
}

enum SnapshotStore {
    private static let path = "/tmp/steer_snapshot.json"

    static func save(_ snapshot: Snapshot) {
        guard let data = try? JSONEncoder().encode(snapshot) else { return }
        try? data.write(to: URL(fileURLWithPath: path))
    }

    static func load() -> Snapshot? {
        guard let data = try? Data(contentsOf: URL(fileURLWithPath: path)),
              let snapshot = try? JSONDecoder().decode(Snapshot.self, from: data) else {
            return nil
        }
        return snapshot
    }

    static func resolveElement(id: String) -> (x: Double, y: Double)? {
        guard let snapshot = load() else { return nil }

        // Check AX elements
        if let elem = snapshot.elements.first(where: { $0.id == id }) {
            return (x: elem.x + elem.width / 2, y: elem.y + elem.height / 2)
        }

        // Check OCR elements
        if let elem = snapshot.ocrElements.first(where: { $0.id == id }) {
            return (x: elem.x + elem.width / 2, y: elem.y + elem.height / 2)
        }

        // Check OCR store file
        let stored = OCRHelper.loadStoredElements()
        if let elem = stored.first(where: { $0.id == id }) {
            return (x: elem.x + elem.width / 2, y: elem.y + elem.height / 2)
        }

        return nil
    }

    static func findByText(_ query: String) -> [AXElement] {
        guard let snapshot = load() else { return [] }
        let q = query.lowercased()
        return snapshot.elements.filter { elem in
            (elem.label?.lowercased().contains(q) ?? false) ||
            (elem.value?.lowercased().contains(q) ?? false)
        }
    }
}
