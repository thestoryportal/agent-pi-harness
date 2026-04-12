import Foundation

private let encoder: JSONEncoder = {
    let e = JSONEncoder()
    e.outputFormatting = [.prettyPrinted, .sortedKeys]
    return e
}()

func printJSON(_ value: some Encodable) {
    do {
        let data = try encoder.encode(value)
        let str = String(data: data, encoding: .utf8) ?? "{}"
        print(str)
    } catch {
        printError("Failed to encode JSON: \(error.localizedDescription)")
    }
}

func printError(_ message: String, code: Int32 = 1) -> Never {
    let obj: [String: Any] = ["error": message, "code": code]
    if let data = try? JSONSerialization.data(withJSONObject: obj, options: [.prettyPrinted, .sortedKeys]),
       let str = String(data: data, encoding: .utf8) {
        FileHandle.standardError.write(Data(str.utf8))
        FileHandle.standardError.write(Data("\n".utf8))
    }
    Foundation.exit(code)
}
