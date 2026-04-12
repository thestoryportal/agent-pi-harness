import ArgumentParser
import Foundation

struct OCRCommand: ParsableCommand {
    static let configuration = CommandConfiguration(
        commandName: "ocr",
        abstract: "Run Vision OCR on a screenshot"
    )

    @Option(name: .long, help: "App name to capture")
    var app: String?

    @Option(name: .long, help: "Screen index (default: 0)")
    var screen: Int = 0

    @Flag(name: .long, help: "Store results as clickable elements (O1, O2, etc.)")
    var store = false

    @Flag(name: .long, help: "Output as JSON")
    var json = false

    func run() throws {
        let result: ScreenshotResult
        if let appName = app {
            result = try ScreenCapture.captureApp(appName)
        } else {
            result = try ScreenCapture.captureScreen(screen)
        }

        let elements = try OCRHelper.runOCR(imagePath: result.screenshot)

        if store {
            try OCRHelper.storeElements(elements)
        }

        struct OCROutput: Codable {
            let screenshot: String
            let elements: [OCRElement]
        }

        let output = OCROutput(screenshot: result.screenshot, elements: elements)

        if json {
            printJSON(output)
        } else {
            print("Screenshot: \(result.screenshot)")
            for elem in elements {
                print("\(elem.id): \"\(elem.text)\" at (\(Int(elem.x)), \(Int(elem.y)))")
            }
        }
    }
}
