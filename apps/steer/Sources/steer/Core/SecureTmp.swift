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
    /// Uses write-to-temp-then-rename. The temp file is opened with O_EXCL|O_NOFOLLOW
    /// so we never follow a symlink and never clobber an existing file. rename(2)
    /// is atomic and operates on directory entries — it does NOT follow symlinks
    /// at the destination, so a symlinked finalPath would be replaced (not written
    /// through) by the rename. No pre-rename lstat is needed.
    static func writeAtomic(_ data: Data, to filename: String) throws {
        let finalPath = try path(for: filename)
        let tmpPath = "\(finalPath).tmp.\(getpid())"

        // Remove any pre-existing temp file from a prior crashed run.
        unlink(tmpPath)

        // O_CREAT | O_EXCL | O_NOFOLLOW: fail if file exists or is a symlink.
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

        // rename(2) is atomic and replaces the destination directory entry.
        // It does not follow symlinks at the destination, so a symlinked
        // finalPath gets replaced by our regular file (not written through).
        if rename(tmpPath, finalPath) != 0 {
            let err = String(cString: strerror(errno))
            unlink(tmpPath)
            throw SteerError.screenshotFailed("Failed to rename \(tmpPath) → \(finalPath): \(err)")
        }
    }

    /// Read data from a file inside the secure directory, verifying it's a regular
    /// file owned by us. Closes the TOCTOU window by opening with O_NOFOLLOW and
    /// validating the file descriptor via fstat() before reading. Returns nil if
    /// the file does not exist or fails validation.
    static func readVerified(_ filename: String) -> Data? {
        guard let p = try? path(for: filename) else { return nil }

        // O_NOFOLLOW: fail with ELOOP if final component is a symlink.
        let fd = open(p, O_RDONLY | O_NOFOLLOW)
        if fd < 0 {
            return nil
        }
        defer { close(fd) }

        // fstat the OPEN descriptor (not the path) to ensure the verification
        // applies to the same inode we're about to read from. This closes the
        // lstat→open TOCTOU that the previous implementation had.
        var st = stat()
        guard fstat(fd, &st) == 0 else { return nil }

        let isRegular = (st.st_mode & S_IFMT) == S_IFREG
        if !isRegular || st.st_uid != getuid() {
            return nil
        }

        // Read the entire file from the verified descriptor.
        let size = Int(st.st_size)
        guard size >= 0 else { return nil }
        var data = Data(count: size)
        let readBytes = data.withUnsafeMutableBytes { buf -> Int in
            guard let base = buf.baseAddress else { return -1 }
            return read(fd, base, size)
        }
        if readBytes != size {
            return nil
        }
        return data
    }

    /// Build a path for an output file (screenshot, OCR PNG) that the agent will read.
    /// The path is inside the secure directory but the filename is unique per call.
    /// Both `prefix` and `ext` are filtered to alphanumerics + `_`/`-` to prevent
    /// any possibility of path component injection or log/JSON escape via the
    /// resulting filename being embedded in agent-visible output.
    static func outputPath(prefix: String, ext: String) throws -> String {
        try ensureDirectory()
        let uuid = UUID().uuidString.lowercased()
        let safeChars: (Character) -> Bool = { $0.isLetter || $0.isNumber || $0 == "_" || $0 == "-" }
        let safePrefix = prefix.filter(safeChars)
        let safeExt = ext.filter(safeChars)
        if safeExt.isEmpty {
            throw SteerError.invalidArgument("outputPath ext must contain at least one safe character")
        }
        return try path(for: "\(safePrefix)_\(uuid).\(safeExt)")
    }
}
