"""Wave management — batched parallel dispatch in 4 modes.

Follows infinite-agentic-loop pattern: single, small_batch, large_batch, infinite.
Pure computation — no file I/O or agent spawning. Callers handle dispatch.
"""

from __future__ import annotations

from typing import Literal

WaveMode = Literal["single", "small_batch", "large_batch", "infinite"]
VALID_MODES = ("single", "small_batch", "large_batch", "infinite")
DEFAULT_BATCH_SIZE = 5
INFINITE_SENTINEL = -1


def chunk_items(items: list, size: int) -> list[list]:
    """Split items into sequential chunks of at most `size`."""
    return [items[i : i + size] for i in range(0, len(items), size)]


def infer_mode(count: int) -> WaveMode:
    """Infer wave mode from item count.

    count == -1 (sentinel) → 'infinite'
    count == 1 → 'single'
    2 ≤ count ≤ 5 → 'small_batch'
    count > 5 → 'large_batch'

    Raises ValueError if count is 0 or less than -1.
    """
    if count == INFINITE_SENTINEL:
        return "infinite"
    if count <= 0:
        raise ValueError(f"count must be positive or -1 (infinite), got {count}")
    if count == 1:
        return "single"
    if count <= DEFAULT_BATCH_SIZE:
        return "small_batch"
    return "large_batch"


def plan_waves(
    items: list,
    mode: str,
    batch_size: int = DEFAULT_BATCH_SIZE,
    max_waves: int | None = None,
) -> list[dict]:
    """Compute the wave execution plan for a list of items.

    Modes:
      single:       1 wave with first item only
      small_batch:  1 wave with up to batch_size items
      large_batch:  items chunked into groups of batch_size, one wave per chunk
      infinite:     1 item per wave; capped by min(len(items), max_waves)

    Note: this module operates on a finite item list. True infinite dispatch
    (unlimited waves) requires the caller to feed new items across iterations.
    When len(items) < max_waves, the plan stops at len(items).

    Raises ValueError if mode is unrecognized, items is empty, or batch_size < 1.
    """
    if mode not in VALID_MODES:
        raise ValueError(f"unknown mode {mode!r}, must be one of {VALID_MODES}")
    if not items:
        raise ValueError("items must not be empty")
    if batch_size < 1:
        raise ValueError(f"batch_size must be >= 1, got {batch_size}")

    waves: list[dict] = []

    if mode == "single":
        waves.append({
            "wave_number": 1,
            "mode": mode,
            "items": items[:1],
            "total_waves": 1,
        })

    elif mode == "small_batch":
        batch = items[:batch_size]
        waves.append({
            "wave_number": 1,
            "mode": mode,
            "items": batch,
            "total_waves": 1,
        })

    elif mode == "large_batch":
        chunks = chunk_items(items, batch_size)
        for i, chunk in enumerate(chunks, start=1):
            waves.append({
                "wave_number": i,
                "mode": mode,
                "items": chunk,
                "total_waves": len(chunks),
            })

    elif mode == "infinite":
        per_wave = [[item] for item in items]
        if max_waves is not None:
            per_wave = per_wave[:max_waves]
        for i, wave_items in enumerate(per_wave, start=1):
            waves.append({
                "wave_number": i,
                "mode": mode,
                "items": wave_items,
                "total_waves": None,
            })

    return waves
