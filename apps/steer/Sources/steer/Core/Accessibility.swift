import ApplicationServices
import AppKit
import Foundation

struct AXElement: Codable {
    let id: String
    let role: String
    let label: String?
    let value: String?
    let x: Double
    let y: Double
    let width: Double
    let height: Double
}

enum AccessibilityHelper {
    static func checkPermission() -> Bool {
        AXIsProcessTrusted()
    }

    static func findAppPID(name: String) -> pid_t? {
        let apps = NSWorkspace.shared.runningApplications
        return apps.first { app in
            app.localizedName?.localizedCaseInsensitiveContains(name) == true ||
            app.bundleIdentifier?.localizedCaseInsensitiveContains(name) == true
        }?.processIdentifier
    }

    static func buildTree(pid: pid_t) -> [AXElement] {
        let app = AXUIElementCreateApplication(pid)
        var elements: [AXElement] = []
        var counters: [String: Int] = [:]
        walkElement(app, elements: &elements, counters: &counters, depth: 0)
        return elements
    }

    static func getFocusedElement() -> AXElement? {
        let systemWide = AXUIElementCreateSystemWide()
        var focusedRef: CFTypeRef?
        let result = AXUIElementCopyAttributeValue(systemWide, kAXFocusedUIElementAttribute as CFString, &focusedRef)
        guard result == .success, let focused = focusedRef else { return nil }
        // CFTypeRef → AXUIElement: AXUIElement is a CFTypeRef alias, so this cast is safe
        // but we guard it anyway for robustness
        let elem = focused as! AXUIElement  // swiftlint:disable:this force_cast
        var counters: [String: Int] = [:]
        return extractElement(elem, counters: &counters)
    }

    private static func walkElement(_ element: AXUIElement, elements: inout [AXElement], counters: inout [String: Int], depth: Int) {
        guard depth < 20 else { return }

        if let axElem = extractElement(element, counters: &counters) {
            elements.append(axElem)
        }

        var childrenRef: CFTypeRef?
        let result = AXUIElementCopyAttributeValue(element, kAXChildrenAttribute as CFString, &childrenRef)
        guard result == .success, let children = childrenRef as? [AXUIElement] else { return }

        for child in children {
            walkElement(child, elements: &elements, counters: &counters, depth: depth + 1)
        }
    }

    private static func extractElement(_ element: AXUIElement, counters: inout [String: Int]) -> AXElement? {
        var roleRef: CFTypeRef?
        AXUIElementCopyAttributeValue(element, kAXRoleAttribute as CFString, &roleRef)
        let role = (roleRef as? String) ?? "AXUnknown"

        var labelRef: CFTypeRef?
        AXUIElementCopyAttributeValue(element, kAXTitleAttribute as CFString, &labelRef)
        let label = labelRef as? String

        var descRef: CFTypeRef?
        AXUIElementCopyAttributeValue(element, kAXDescriptionAttribute as CFString, &descRef)
        let desc = descRef as? String

        var valueRef: CFTypeRef?
        AXUIElementCopyAttributeValue(element, kAXValueAttribute as CFString, &valueRef)
        let value = valueRef as? String

        var posRef: CFTypeRef?
        AXUIElementCopyAttributeValue(element, kAXPositionAttribute as CFString, &posRef)
        var position = CGPoint.zero
        if let posVal = posRef {
            // AXValue is a CFTypeRef; use unsafeBitCast since conditional cast is not allowed
            let axValue = unsafeBitCast(posVal, to: AXValue.self)
            AXValueGetValue(axValue, .cgPoint, &position)
        }

        var sizeRef: CFTypeRef?
        AXUIElementCopyAttributeValue(element, kAXSizeAttribute as CFString, &sizeRef)
        var size = CGSize.zero
        if let sizeVal = sizeRef {
            let axValue = unsafeBitCast(sizeVal, to: AXValue.self)
            AXValueGetValue(axValue, .cgSize, &size)
        }

        let prefix = rolePrefix(for: role)
        let count = (counters[prefix] ?? 0) + 1
        counters[prefix] = count
        let id = "\(prefix)\(count)"

        let displayLabel = label ?? desc

        return AXElement(
            id: id,
            role: role,
            label: displayLabel,
            value: value,
            x: Double(position.x),
            y: Double(position.y),
            width: Double(size.width),
            height: Double(size.height)
        )
    }

    private static func rolePrefix(for role: String) -> String {
        switch role {
        case "AXButton": return "B"
        case "AXTextField", "AXTextArea": return "T"
        case "AXStaticText": return "S"
        case "AXImage": return "I"
        case "AXCheckBox": return "C"
        case "AXLink": return "L"
        case "AXMenuItem", "AXMenuBarItem": return "M"
        default: return "X"
        }
    }
}
