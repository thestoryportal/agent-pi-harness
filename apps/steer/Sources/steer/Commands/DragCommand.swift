import ArgumentParser
import Foundation

struct DragCommand: ParsableCommand {
    static let configuration = CommandConfiguration(
        commandName: "drag",
        abstract: "Drag between elements or coordinates"
    )

    @Option(name: .long, help: "Source element ID")
    var fromId: String?

    @Option(name: .long, help: "Destination element ID")
    var toId: String?

    @Option(name: .long, help: "Source X coordinate")
    var fromX: Double?

    @Option(name: .long, help: "Source Y coordinate")
    var fromY: Double?

    @Option(name: .long, help: "Destination X coordinate")
    var toX: Double?

    @Option(name: .long, help: "Destination Y coordinate")
    var toY: Double?

    @Option(name: .long, help: "Drag duration in seconds (default: 0.5)")
    var duration: Double = 0.5

    @Flag(name: .long, help: "Output as JSON")
    var json = false

    func run() throws {
        let sx: Double
        let sy: Double
        let dx: Double
        let dy: Double

        if let fid = fromId, let coords = SnapshotStore.resolveElement(id: fid) {
            sx = coords.x; sy = coords.y
        } else if let fx = fromX, let fy = fromY {
            sx = fx; sy = fy
        } else {
            printError("Provide --from-id or --from-x/--from-y")
        }

        if let tid = toId, let coords = SnapshotStore.resolveElement(id: tid) {
            dx = coords.x; dy = coords.y
        } else if let tx = toX, let ty = toY {
            dx = tx; dy = ty
        } else {
            printError("Provide --to-id or --to-x/--to-y")
        }

        try InputHelper.drag(fromX: sx, fromY: sy, toX: dx, toY: dy, duration: duration)

        struct DragOutput: Codable {
            struct Point: Codable { let x: Double; let y: Double }
            let action: String
            let from: Point
            let to: Point
        }

        let output = DragOutput(
            action: "drag",
            from: .init(x: sx, y: sy),
            to: .init(x: dx, y: dy)
        )
        if json {
            printJSON(output)
        } else {
            print("Dragged from (\(Int(sx)), \(Int(sy))) to (\(Int(dx)), \(Int(dy)))")
        }
    }
}
