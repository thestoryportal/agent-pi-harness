import ArgumentParser

@main
struct Steer: ParsableCommand {
    static let configuration = CommandConfiguration(
        commandName: "steer",
        abstract: "macOS GUI automation CLI for AI agents",
        version: "0.1.0",
        subcommands: [
            SeeCommand.self,
            ClickCommand.self,
            TypeCommand.self,
            HotkeyCommand.self,
            ScrollCommand.self,
            DragCommand.self,
            AppsCommand.self,
            ScreensCommand.self,
            WindowCommand.self,
            OCRCommand.self,
            FocusCommand.self,
            FindCommand.self,
            ClipboardCommand.self,
            WaitCommand.self,
        ]
    )
}
