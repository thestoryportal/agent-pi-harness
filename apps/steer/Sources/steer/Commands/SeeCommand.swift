import ArgumentParser
import Foundation

struct SeeCommand: ParsableCommand {
    static let configuration = CommandConfiguration(
        commandName: "see",
        abstract: "Take a screenshot and walk the accessibility tree"
    )

    @Option(name: .long, help: "App name to capture")
    var app: String?

    @Option(name: .long, help: "Screen index (default: 0)")
    var screen: Int = 0

    @Flag(name: .long, help: "Fall back to OCR when elements are empty")
    var ocr = false

    @Flag(name: .long, help: "Output as JSON")
    var json = false

    func run() throws {
        let result: ScreenshotResult
        if let appName = app {
            result = try ScreenCapture.captureApp(appName)
        } else {
            result = try ScreenCapture.captureScreen(screen)
        }

        var elements: [AXElement] = []
        if let appName = app, let pid = AccessibilityHelper.findAppPID(name: appName) {
            elements = AccessibilityHelper.buildTree(pid: pid)
        }

        var ocrElements: [OCRElement] = []
        if ocr && elements.isEmpty {
            ocrElements = (try? OCRHelper.runOCR(imagePath: result.screenshot)) ?? []
        }

        let snapshot = Snapshot(
            app: app,
            screenshot: result.screenshot,
            elements: elements,
            ocrElements: ocrElements
        )
        SnapshotStore.save(snapshot)

        struct SeeOutput: Codable {
            let screenshot: String
            let app: String?
            let elements: [AXElement]
            let ocrElements: [OCRElement]?
        }

        let output = SeeOutput(
            screenshot: result.screenshot,
            app: app,
            elements: elements,
            ocrElements: ocrElements.isEmpty ? nil : ocrElements
        )

        if json {
            printJSON(output)
        } else {
            print("Screenshot: \(result.screenshot)")
            print("Elements: \(elements.count)")
            if !ocrElements.isEmpty {
                print("OCR Elements: \(ocrElements.count)")
            }
        }
    }
}
