import Foundation

struct Snapshot: Codable {
    let app: String?
    let screenshot: String
    let elements: [AXElement]
    let ocrElements: [OCRElement]
}

enum SnapshotStore {
    private static let filename = "snapshot.json"

    static func save(_ snapshot: Snapshot) {
        // Surface errors to stderr instead of silently dropping. A failed save
        // means the next `click --id B1` will report "element not found" with
        // no breadcrumb pointing to the actual cause (write permission, full
        // disk, secure tmp dir issue).
        do {
            let data = try JSONEncoder().encode(snapshot)
            try SecureTmp.writeAtomic(data, to: filename)
        } catch {
            let warning = "warning: snapshot save failed: \(error.localizedDescription)\n"
            FileHandle.standardError.write(Data(warning.utf8))
        }
    }

    static func load() -> Snapshot? {
        guard let data = SecureTmp.readVerified(filename),
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
