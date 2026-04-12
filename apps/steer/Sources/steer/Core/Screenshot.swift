import AppKit
import CoreGraphics
import Foundation

struct ScreenshotResult: Codable {
    let screenshot: String
    let width: Int
    let height: Int
}

enum ScreenCapture {
    static func captureScreen(_ screenIndex: Int) throws -> ScreenshotResult {
        if #available(macOS 14.0, *) {
            if !CGPreflightScreenCaptureAccess() {
                CGRequestScreenCaptureAccess()
            }
        }

        let screens = NSScreen.screens
        guard screenIndex >= 0, screenIndex < screens.count else {
            throw SteerError.invalidScreen(screenIndex, available: screens.count)
        }

        let screen = screens[screenIndex]
        guard let displayIDValue = screen.deviceDescription[NSDeviceDescriptionKey("NSScreenNumber")] as? CGDirectDisplayID else {
            throw SteerError.screenshotFailed("Could not get display ID for screen \(screenIndex)")
        }
        let displayID = displayIDValue

        guard let image = CGDisplayCreateImage(displayID) else {
            throw SteerError.screenshotFailed("CGDisplayCreateImage returned nil — Screen Recording permission may be required")
        }

        let path = "/tmp/steer_screen_\(screenIndex)_\(Int(Date().timeIntervalSince1970)).png"
        try writePNG(image, to: path)

        return ScreenshotResult(
            screenshot: path,
            width: image.width,
            height: image.height
        )
    }

    static func captureApp(_ name: String) throws -> ScreenshotResult {
        if #available(macOS 14.0, *) {
            if !CGPreflightScreenCaptureAccess() {
                CGRequestScreenCaptureAccess()
            }
        }

        let windowList = CGWindowListCopyWindowInfo([.optionOnScreenOnly, .excludeDesktopElements], kCGNullWindowID) as? [[String: Any]] ?? []

        let appWindows = windowList.filter { info in
            guard let owner = info[kCGWindowOwnerName as String] as? String else { return false }
            return owner.localizedCaseInsensitiveContains(name)
        }

        guard !appWindows.isEmpty else {
            throw SteerError.appNotFound(name)
        }

        let windowIDs = appWindows.compactMap { $0[kCGWindowNumber as String] as? CGWindowID }
        let idArray = windowIDs as CFArray

        guard let image = CGImage(
            windowListFromArrayScreenBounds: CGRect.null,
            windowArray: idArray,
            imageOption: .bestResolution
        ) else {
            throw SteerError.screenshotFailed("Failed to capture windows for \(name) — Screen Recording permission may be required")
        }

        let safeName = name.replacingOccurrences(of: " ", with: "_")
            .lowercased()
            .filter { $0.isLetter || $0.isNumber || $0 == "_" || $0 == "-" }
        let path = "/tmp/steer_app_\(safeName)_\(Int(Date().timeIntervalSince1970)).png"
        try writePNG(image, to: path)

        return ScreenshotResult(
            screenshot: path,
            width: image.width,
            height: image.height
        )
    }

    private static func writePNG(_ image: CGImage, to path: String) throws {
        let url = URL(fileURLWithPath: path)
        guard let dest = CGImageDestinationCreateWithURL(url as CFURL, "public.png" as CFString, 1, nil) else {
            throw SteerError.screenshotFailed("Failed to create image destination at \(path)")
        }
        CGImageDestinationAddImage(dest, image, nil)
        guard CGImageDestinationFinalize(dest) else {
            throw SteerError.screenshotFailed("Failed to write PNG to \(path)")
        }
    }
}
