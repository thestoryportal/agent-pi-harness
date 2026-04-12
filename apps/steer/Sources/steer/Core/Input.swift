import ApplicationServices
import CoreGraphics
import Foundation

enum InputHelper {
    static func ensureAccessibility() throws {
        guard AXIsProcessTrusted() else {
            throw SteerError.accessibilityDenied
        }
    }

    static func mouseClick(x: Double, y: Double, button: CGMouseButton = .left) throws {
        try ensureAccessibility()
        let point = CGPoint(x: x, y: y)
        let downType: CGEventType = button == .left ? .leftMouseDown : .rightMouseDown
        let upType: CGEventType = button == .left ? .leftMouseUp : .rightMouseUp

        guard let downEvent = CGEvent(mouseEventSource: nil, mouseType: downType, mouseCursorPosition: point, mouseButton: button),
              let upEvent = CGEvent(mouseEventSource: nil, mouseType: upType, mouseCursorPosition: point, mouseButton: button) else {
            return
        }

        downEvent.post(tap: .cghidEventTap)
        Thread.sleep(forTimeInterval: 0.05)
        upEvent.post(tap: .cghidEventTap)
    }

    static func typeText(_ text: String) throws {
        try ensureAccessibility()
        for char in text.utf16 {
            guard let downEvent = CGEvent(keyboardEventSource: nil, virtualKey: 0, keyDown: true),
                  let upEvent = CGEvent(keyboardEventSource: nil, virtualKey: 0, keyDown: false) else {
                continue
            }
            var chars = [char]
            downEvent.keyboardSetUnicodeString(stringLength: 1, unicodeString: &chars)
            upEvent.keyboardSetUnicodeString(stringLength: 1, unicodeString: &chars)
            downEvent.post(tap: .cghidEventTap)
            upEvent.post(tap: .cghidEventTap)
            Thread.sleep(forTimeInterval: 0.01)
        }
    }

    static func sendHotkey(combo: String) throws {
        try ensureAccessibility()
        let parts = combo.lowercased().split(separator: "+").map(String.init)
        var flags: CGEventFlags = []
        var keyCode: CGKeyCode = 0

        for part in parts {
            switch part {
            case "cmd", "command":
                flags.insert(.maskCommand)
            case "shift":
                flags.insert(.maskShift)
            case "ctrl", "control":
                flags.insert(.maskControl)
            case "alt", "option", "opt":
                flags.insert(.maskAlternate)
            default:
                keyCode = keyCodeFor(part)
            }
        }

        guard let downEvent = CGEvent(keyboardEventSource: nil, virtualKey: keyCode, keyDown: true),
              let upEvent = CGEvent(keyboardEventSource: nil, virtualKey: keyCode, keyDown: false) else {
            return
        }

        downEvent.flags = flags
        upEvent.flags = flags
        downEvent.post(tap: .cghidEventTap)
        Thread.sleep(forTimeInterval: 0.05)
        upEvent.post(tap: .cghidEventTap)
    }

    static func scroll(direction: String, amount: Int, x: Double? = nil, y: Double? = nil) throws {
        try ensureAccessibility()
        let (dx, dy): (Int32, Int32) = switch direction {
        case "up": (0, Int32(amount))
        case "down": (0, Int32(-amount))
        case "left": (Int32(amount), 0)
        case "right": (Int32(-amount), 0)
        default: (0, 0)
        }

        if let x = x, let y = y {
            let moveEvent = CGEvent(mouseEventSource: nil, mouseType: .mouseMoved, mouseCursorPosition: CGPoint(x: x, y: y), mouseButton: .left)
            moveEvent?.post(tap: .cghidEventTap)
            Thread.sleep(forTimeInterval: 0.05)
        }

        guard let scrollEvent = CGEvent(scrollWheelEvent2Source: nil, units: .pixel, wheelCount: 2, wheel1: dy, wheel2: dx, wheel3: 0) else {
            return
        }
        scrollEvent.post(tap: CGEventTapLocation.cghidEventTap)
    }

    static func drag(fromX: Double, fromY: Double, toX: Double, toY: Double, duration: Double = 0.5) throws {
        try ensureAccessibility()
        let from = CGPoint(x: fromX, y: fromY)
        let to = CGPoint(x: toX, y: toY)
        let steps = max(Int(duration / 0.016), 10)

        guard let downEvent = CGEvent(mouseEventSource: nil, mouseType: .leftMouseDown, mouseCursorPosition: from, mouseButton: .left) else { return }
        downEvent.post(tap: .cghidEventTap)

        for i in 1...steps {
            let t = Double(i) / Double(steps)
            let x = fromX + (toX - fromX) * t
            let y = fromY + (toY - fromY) * t
            let point = CGPoint(x: x, y: y)
            guard let dragEvent = CGEvent(mouseEventSource: nil, mouseType: .leftMouseDragged, mouseCursorPosition: point, mouseButton: .left) else { continue }
            dragEvent.post(tap: .cghidEventTap)
            Thread.sleep(forTimeInterval: duration / Double(steps))
        }

        guard let upEvent = CGEvent(mouseEventSource: nil, mouseType: .leftMouseUp, mouseCursorPosition: to, mouseButton: .left) else { return }
        upEvent.post(tap: .cghidEventTap)
    }

    private static func keyCodeFor(_ key: String) -> CGKeyCode {
        switch key {
        case "return", "enter": return 0x24
        case "escape", "esc": return 0x35
        case "tab": return 0x30
        case "space": return 0x31
        case "delete", "backspace": return 0x33
        case "up": return 0x7E
        case "down": return 0x7D
        case "left": return 0x7B
        case "right": return 0x7C
        case "f1": return 0x7A
        case "f2": return 0x78
        case "f3": return 0x63
        case "f4": return 0x76
        case "f5": return 0x60
        case "f6": return 0x61
        case "f7": return 0x62
        case "f8": return 0x64
        case "f9": return 0x65
        case "f10": return 0x6D
        case "f11": return 0x67
        case "f12": return 0x6F
        case "a": return 0x00
        case "b": return 0x0B
        case "c": return 0x08
        case "d": return 0x02
        case "e": return 0x0E
        case "f": return 0x03
        case "g": return 0x05
        case "h": return 0x04
        case "i": return 0x22
        case "j": return 0x26
        case "k": return 0x28
        case "l": return 0x25
        case "m": return 0x2E
        case "n": return 0x2D
        case "o": return 0x1F
        case "p": return 0x23
        case "q": return 0x0C
        case "r": return 0x0F
        case "s": return 0x01
        case "t": return 0x11
        case "u": return 0x20
        case "v": return 0x09
        case "w": return 0x0D
        case "x": return 0x07
        case "y": return 0x10
        case "z": return 0x06
        case "0": return 0x1D
        case "1": return 0x12
        case "2": return 0x13
        case "3": return 0x14
        case "4": return 0x15
        case "5": return 0x17
        case "6": return 0x16
        case "7": return 0x1A
        case "8": return 0x1C
        case "9": return 0x19
        case "-": return 0x1B
        case "=": return 0x18
        case "[": return 0x21
        case "]": return 0x1E
        case "\\": return 0x2A
        case ";": return 0x29
        case "'": return 0x27
        case ",": return 0x2B
        case ".": return 0x2F
        case "/": return 0x2C
        case "`": return 0x32
        default: return 0
        }
    }
}
