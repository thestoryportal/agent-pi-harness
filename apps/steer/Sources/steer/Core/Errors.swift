import Foundation

enum SteerError: LocalizedError {
    case invalidScreen(Int, available: Int)
    case screenshotFailed(String)
    case appNotFound(String)
    case accessibilityDenied
    case elementNotFound(String)
    case ocrFailed(String)
    case timeout(String)

    var errorDescription: String? {
        switch self {
        case .invalidScreen(let idx, let count):
            return "Screen index \(idx) out of range (available: \(count))"
        case .screenshotFailed(let msg):
            return msg
        case .appNotFound(let name):
            return "App '\(name)' not found in running applications"
        case .accessibilityDenied:
            return "Accessibility permission not granted. Grant in System Settings > Privacy & Security > Accessibility."
        case .elementNotFound(let id):
            return "Element '\(id)' not found in current snapshot"
        case .ocrFailed(let msg):
            return msg
        case .timeout(let msg):
            return "Timeout: \(msg)"
        }
    }
}
