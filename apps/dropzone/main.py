"""Drop Zone CLI — start file watchers from drops.yaml config."""

import time
from pathlib import Path

import click
from rich.console import Console
from rich.table import Table
from watchdog.observers import Observer
from watchdog.observers.api import BaseObserver

from apps.dropzone.config import DropsConfig, ensure_zone_dirs, load_drops_config
from apps.dropzone.watcher import DropZoneEventHandler


def start_watchers(
    config: DropsConfig, console: Console
) -> list[BaseObserver]:
    """Create and start a watchdog observer per zone."""
    observers: list[BaseObserver] = []
    for zone in config.drop_zones:
        handler = DropZoneEventHandler(zone, console)
        observer = Observer()
        for zone_dir in zone.zone_dirs:
            observer.schedule(handler, path=zone_dir, recursive=False)
        observer.start()
        observers.append(observer)
    return observers


@click.command()
@click.option(
    "--config", "config_path", default="drops.yaml",
    help="Path to drops.yaml configuration file.",
)
def watch(config_path: str) -> None:
    """Start drop zone file watchers."""
    console = Console()
    cfg = load_drops_config(Path(config_path))
    ensure_zone_dirs(cfg)

    # Startup banner
    table = Table(title="Drop Zones Active", show_lines=True)
    table.add_column("Zone", style="bold cyan")
    table.add_column("Patterns")
    table.add_column("Events")
    table.add_column("Agent")
    table.add_column("Dirs")
    for zone in cfg.drop_zones:
        table.add_row(
            zone.name,
            ", ".join(zone.file_patterns),
            ", ".join(zone.events),
            f"{zone.agent} ({zone.model})",
            ", ".join(zone.zone_dirs),
        )
    console.print(table)
    console.print("[bold green]Watching for file events... Ctrl+C to stop.[/]\n")

    observers = start_watchers(cfg, console)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        console.print("\n[bold yellow]Shutting down watchers...[/]")
        for obs in observers:
            obs.stop()
        for obs in observers:
            obs.join()
        console.print("[bold green]Done.[/]")


if __name__ == "__main__":
    watch()
