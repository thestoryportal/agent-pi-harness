"""Parallel command dispatch across tmux sessions via ThreadPoolExecutor."""

import logging
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

from apps.drive.runner import run_command
from apps.drive.session import create_session

logger = logging.getLogger(__name__)

DEFAULT_MAX_SESSIONS = 2


def _dispatch_one(target: str, cmd: str) -> dict:
    """Dispatch a command to a single session. Creates session if needed."""
    create_session(target)
    token = run_command(target, cmd)
    return {"target": target, "token": token, "status": "dispatched" if token else "failed"}


def dispatch_fanout(
    cmd: str,
    targets: list[str],
    max_sessions: int = DEFAULT_MAX_SESSIONS,
) -> dict[str, dict]:
    """Dispatch a command to multiple sessions in parallel.

    Uses a Semaphore + ThreadPoolExecutor to enforce the concurrency cap.
    """
    semaphore = threading.Semaphore(max_sessions)
    results = {}

    def _gated_dispatch(target: str, command: str) -> dict:
        acquired = semaphore.acquire(blocking=False)
        if not acquired:
            logger.info(f"[fanout] queuing: {target} (cap={max_sessions})")
            semaphore.acquire()
        try:
            return _dispatch_one(target, command)
        finally:
            semaphore.release()

    with ThreadPoolExecutor(max_workers=max_sessions) as executor:
        futures = {
            executor.submit(_gated_dispatch, target, cmd): target
            for target in targets
        }
        for future in as_completed(futures):
            target = futures[future]
            try:
                results[target] = future.result()
            except Exception as e:
                results[target] = {"target": target, "token": None, "status": f"error: {e}"}

    return results


def dispatch_fanout_from_file(
    filepath: str,
    max_sessions: int = DEFAULT_MAX_SESSIONS,
) -> dict[str, dict]:
    """Read commands from a file (one per line), dispatch each in its own session."""
    semaphore = threading.Semaphore(max_sessions)
    results = {}

    with open(filepath) as f:
        commands = [line.strip() for line in f if line.strip()]

    def _dispatch_line(index: int, cmd: str) -> dict:
        target = f"fanout-{index}"
        acquired = semaphore.acquire(blocking=False)
        if not acquired:
            logger.info(f"[fanout] queuing: {target} (cap={max_sessions})")
            semaphore.acquire()
        try:
            create_session(target)
            token = run_command(target, cmd)
            return {"target": target, "token": token, "status": "dispatched" if token else "failed"}
        finally:
            semaphore.release()

    with ThreadPoolExecutor(max_workers=max_sessions) as executor:
        futures = {
            executor.submit(_dispatch_line, i, cmd): f"fanout-{i}"
            for i, cmd in enumerate(commands)
        }
        for future in as_completed(futures):
            target = futures[future]
            try:
                results[target] = future.result()
            except Exception as e:
                results[target] = {"target": target, "token": None, "status": f"error: {e}"}

    return results
