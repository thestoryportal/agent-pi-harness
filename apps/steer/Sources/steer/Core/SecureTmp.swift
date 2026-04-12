import Darwin
import Foundation

/// Provides a secure per-UID directory under /tmp for steer state files.
///
/// Mitigates two attack classes:
///   1. Symlink-pre-create writes (S-01): an attacker creates /tmp/steer_snapshot.json
///      as a symlink before steer runs, redirecting writes to a sensitive file.
///   2. Snapshot poisoning (S-02): an attacker writes /tmp/steer_ocr_store.json with
///      crafted coordinates, then waits for the next click/type/drag to be steered.
///
/// Defense:
///   - All files live inside /tmp/steer-<uid>/, mode 0700
///   - Directory is verified to be owned by current uid and not a symlink
///   - File reads use lstat() to reject symlinks and foreign-owned files
///   - File writes use atomic rename via FileManager (write to .tmp, rename)
enum SecureTmp {
    static let directory: String = {
        let uid = getuid()
        return "/tmp/steer-\(uid)"
    }()

    /// Ensure the secure directory exists with correct ownership and mode.
    /// Throws if the path exists but is unsafe (symlink, wrong owner, wrong mode).
    static func ensureDirectory() throws {
        let path = directory
        var st = stat()

        if lstat(path, &st) == 0 {
            // Path exists — verify it's a real directory owned by us with mode 0700
            let isSymlink = (st.st_mode & S_IFMT) == S_IFLNK
            if isSymlink {
                throw SteerError.screenshotFailed("\(path) is a symlink — refusing to use")
            }
            let isDir = (st.st_mode & S_IFMT) == S_IFDIR
            if !isDir {
                throw SteerError.screenshotFailed("\(path) exists but is not a directory")
            }
            if st.st_uid != getuid() {
                throw SteerError.screenshotFailed("\(path) is not owned by current user")
            }
            // Tighten mode if needed
            let perms = st.st_mode & 0o777
            if perms != 0o700 {
                _ = chmod(path, 0o700)
            }
            return
        }

        // Doesn't exist — create with mode 0700
        if mkdir(path, 0o700) != 0 {
            let err = String(cString: strerror(errno))
            throw SteerError.screenshotFailed("Failed to create \(path): \(err)")
        }
    }

    /// Build a path inside the secure directory. Filename must not contain path separators.
    static func path(for filename: String) throws -> String {
        try ensureDirectory()
        guard !filename.contains("/"), !filename.contains("\0"), filename != "..", filename != "." else {
            throw SteerError.screenshotFailed("Invalid filename: \(filename)")
        }
        return "\(directory)/\(filename)"
    }

    /// Atomically write data to a file inside the secure directory.
    /// Uses write-to-temp-then-rename to avoid TOCTOU between create and write.
    static func writeAtomic(_ data: Data, to filename: String) throws {
        let finalPath = try path(for: filename)
        let tmpPath = "\(finalPath).tmp.\(getpid())"

        // Remove any pre-existing temp file (could be a symlink)
        unlink(tmpPath)

        // O_CREAT | O_EXCL | O_NOFOLLOW: fail if file exists or is a symlink
        let fd = open(tmpPath, O_WRONLY | O_CREAT | O_EXCL | O_NOFOLLOW, 0o600)
        if fd < 0 {
            let err = String(cString: strerror(errno))
            throw SteerError.screenshotFailed("Failed to create \(tmpPath): \(err)")
        }

        let written = data.withUnsafeBytes { buf -> Int in
            guard let base = buf.baseAddress else { return -1 }
            return write(fd, base, buf.count)
        }
        close(fd)

        if written != data.count {
            unlink(tmpPath)
            throw SteerError.screenshotFailed("Short write to \(tmpPath)")
        }

        // Verify the final path, if it exists, is not a symlink — then rename
        var st = stat()
        if lstat(finalPath, &st) == 0 {
            let isSymlink = (st.st_mode & S_IFMT) == S_IFLNK
            if isSymlink {
                unlink(tmpPath)
                throw SteerError.screenshotFailed("\(finalPath) is a symlink — refusing to overwrite")
            }
            if st.st_uid != getuid() {
                unlink(tmpPath)
                throw SteerError.screenshotFailed("\(finalPath) is owned by another user")
            }
        }

        if rename(tmpPath, finalPath) != 0 {
            let err = String(cString: strerror(errno))
            unlink(tmpPath)
            throw SteerError.screenshotFailed("Failed to rename \(tmpPath) → \(finalPath): \(err)")
        }
    }

    /// Read data from a file inside the secure directory, verifying it's a regular
    /// file owned by us. Returns nil if the file does not exist or fails validation.
    static func readVerified(_ filename: String) -> Data? {
        guard let p = try? path(for: filename) else { return nil }

        var st = stat()
        guard lstat(p, &st) == 0 else { return nil }

        // Reject symlinks, non-regular files, and foreign-owned files
        let isSymlink = (st.st_mode & S_IFMT) == S_IFLNK
        let isRegular = (st.st_mode & S_IFMT) == S_IFREG
        if isSymlink || !isRegular || st.st_uid != getuid() {
            return nil
        }

        return try? Data(contentsOf: URL(fileURLWithPath: p))
    }

    /// Build a path for an output file (screenshot, OCR PNG) that the agent will read.
    /// The path is inside the secure directory but the filename is unique per call.
    static func outputPath(prefix: String, ext: String) throws -> String {
        try ensureDirectory()
        let uuid = UUID().uuidString.lowercased()
        let safePrefix = prefix.filter { $0.isLetter || $0.isNumber || $0 == "_" || $0 == "-" }
        return try path(for: "\(safePrefix)_\(uuid).\(ext)")
    }
}
