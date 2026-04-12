"""Watchdog file monitor — event handler, pattern matching, archive."""

import fnmatch
import shutil
from pathlib import Path

from rich.console import Console
from rich.panel import Panel
from watchdog.events import FileSystemEventHandler

from apps.dropzone.backends import dispatch_backend
from apps.dropzone.config import DropZoneConfig
from apps.dropzone.prompts import load_and_render_prompt, sanitize_file_path


def matches_pattern(filename: str, patterns: list[str]) -> bool:
    """Check if filename matches any of the glob patterns."""
    return any(fnmatch.fnmatch(filename, p) for p in patterns)


def is_within_zone(file_path: Path, zone_dirs: list[str]) -> bool:
    """Verify resolved path is a child of one of the zone directories."""
    resolved = str(file_path.resolve())
    for zone_dir in zone_dirs:
        zone_resolved = str(Path(zone_dir).resolve())
        if resolved.startswith(zone_resolved + "/") or resolved == zone_resolved:
            return True
    return False


def archive_file(file_path: Path) -> Path:
    """Move processed file to archive/ subdirectory within its parent."""
    archive_dir = file_path.parent / "archive"
    archive_dir.mkdir(parents=True, exist_ok=True)
    dest = archive_dir / file_path.name
    shutil.move(str(file_path), str(dest))
    return dest


class DropZoneEventHandler(FileSystemEventHandler):
    """Watchdog handler for a single drop zone."""

    def __init__(self, zone: DropZoneConfig, console: Console) -> None:
        super().__init__()
        self.zone = zone
        self.console = console

    def on_created(self, event):
        self._handle_event(event, "created")

    def on_modified(self, event):
        self._handle_event(event, "modified")

    def on_deleted(self, event):
        self._handle_event(event, "deleted")

    def on_moved(self, event):
        self._handle_event(event, "moved")

    def _handle_event(self, event, event_type: str):
        if event.is_directory:
            return

        file_path = Path(event.src_path)

        if not matches_pattern(file_path.name, self.zone.file_patterns):
            return

        if event_type not in self.zone.events:
            return

        # Security: reject symlinks and paths that escape zone boundaries.
        # Note: TOCTOU window exists between is_symlink/is_within_zone/resolve —
        # accepted risk for a dev harness (requires local attacker with shell access).
        if file_path.is_symlink():
            self.console.print(
                f"[bold red]{self.zone.name}[/] — rejected symlink: {file_path}"
            )
            return

        if not is_within_zone(file_path, self.zone.zone_dirs):
            self.console.print(
                f"[bold red]{self.zone.name}[/] — rejected path outside zone: {file_path}"
            )
            return

        abs_path = str(file_path.resolve())

        try:
            sanitize_file_path(abs_path)
        except ValueError as e:
            self.console.print(f"[bold red]{self.zone.name}[/] — {e}")
            return

        self.console.print(
            f"[bold cyan]{self.zone.name}[/] — {event_type}: {abs_path}"
        )

        try:
            rendered = load_and_render_prompt(self.zone.reusable_prompt, abs_path)
            result = dispatch_backend(rendered, self.zone, abs_path)

            self.console.print(Panel(
                result.stdout or f"[dim](exit {result.exit_code})[/]",
                title=f"{self.zone.name} — {self.zone.agent}",
                border_style="green" if result.exit_code == 0 else "red",
            ))

            if result.stderr:
                self.console.print(f"[red]stderr:[/] {result.stderr}")

            # Archive processed file (skip if deleted — file is already gone)
            if event_type != "deleted" and file_path.exists():
                dest = archive_file(file_path)
                self.console.print(f"[dim]archived → {dest}[/]")
        except Exception as e:
            import sys
            msg = f"{self.zone.name} — error handling {abs_path}: {e}"
            self.console.print(f"[bold red]{msg}[/]")
            # Durable output to stderr for headless/redirected runs
            print(f"DROPZONE ERROR: {msg}", file=sys.stderr)
