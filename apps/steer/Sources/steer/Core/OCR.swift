import AppKit
import Foundation
import Vision

struct OCRElement: Codable {
    let id: String
    let text: String
    let x: Double
    let y: Double
    let width: Double
    let height: Double
    let confidence: Float
}

enum OCRHelper {
    static func runOCR(imagePath: String) throws -> [OCRElement] {
        guard let image = NSImage(contentsOfFile: imagePath),
              let cgImage = image.cgImage(forProposedRect: nil, context: nil, hints: nil) else {
            throw SteerError.ocrFailed("Failed to load image at \(imagePath)")
        }

        let imageWidth = Double(cgImage.width)
        let imageHeight = Double(cgImage.height)

        let request = VNRecognizeTextRequest()
        request.recognitionLevel = .accurate
        request.usesLanguageCorrection = true

        let handler = VNImageRequestHandler(cgImage: cgImage, options: [:])
        try handler.perform([request])

        guard let observations = request.results else {
            return []
        }

        var elements: [OCRElement] = []
        for (index, observation) in observations.enumerated() {
            guard let candidate = observation.topCandidates(1).first else { continue }
            let box = observation.boundingBox
            // Vision returns normalized coords with origin at bottom-left; convert to top-left pixel coords
            let x = box.origin.x * imageWidth
            let y = (1.0 - box.origin.y - box.height) * imageHeight
            let w = box.width * imageWidth
            let h = box.height * imageHeight

            elements.append(OCRElement(
                id: "O\(index + 1)",
                text: candidate.string,
                x: x,
                y: y,
                width: w,
                height: h,
                confidence: candidate.confidence
            ))
        }

        return elements
    }

    static func storeElements(_ elements: [OCRElement]) throws {
        let data = try JSONEncoder().encode(elements)
        try data.write(to: URL(fileURLWithPath: "/tmp/steer_ocr_store.json"))
    }

    static func loadStoredElements() -> [OCRElement] {
        guard let data = try? Data(contentsOf: URL(fileURLWithPath: "/tmp/steer_ocr_store.json")),
              let elements = try? JSONDecoder().decode([OCRElement].self, from: data) else {
            return []
        }
        return elements
    }
}
