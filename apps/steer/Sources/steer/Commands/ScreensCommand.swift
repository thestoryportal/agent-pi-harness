import AppKit
import ArgumentParser
import Foundation

struct ScreensCommand: ParsableCommand {
    static let configuration = CommandConfiguration(
        commandName: "screens",
        abstract: "List displays with resolution and scale"
    )

    @Flag(name: .long, help: "Output as JSON")
    var json = false

    func run() {
        struct ScreenInfo: Codable {
            let index: Int
            let width: Int
            let height: Int
            let scale: Double
            let isMain: Bool
        }

        let screens = NSScreen.screens.enumerated().map { index, screen in
            ScreenInfo(
                index: index,
                width: Int(screen.frame.width),
                height: Int(screen.frame.height),
                scale: Double(screen.backingScaleFactor),
                isMain: screen == NSScreen.main
            )
        }

        if json {
            printJSON(["screens": screens])
        } else {
            for s in screens {
                let main = s.isMain ? " (main)" : ""
                print("Screen \(s.index): \(s.width)x\(s.height) @\(s.scale)x\(main)")
            }
        }
    }
}
