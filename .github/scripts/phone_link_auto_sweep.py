#!/usr/bin/env python3
"""Watch Phone Link downloads and move completed files into the VAULT root."""

from __future__ import annotations

import argparse
import hashlib
import math
import os
import shutil
import sys
import tempfile
import time
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path
from typing import Iterator


DEFAULT_SOURCE = Path.home() / "Downloads" / "Phone Link"
TRUSTED_SOURCE_ROOT = DEFAULT_SOURCE.parent
TRUSTED_VAULT_ROOT = Path(__file__).resolve().parents[2]
LOCK_PATH = Path(tempfile.gettempdir()) / "idaho-vault-phone-link-sweep.lock"


def normalized_path(path: Path) -> str:
    """Normalize a configured path lexically, without accessing the filesystem."""
    return os.path.normcase(os.path.normpath(os.fspath(path)))


def resolve_phone_link_source(path: Path) -> Path:
    """Resolve an existing Phone Link source within the Downloads boundary."""
    trusted_root = os.path.normcase(os.path.realpath(os.fspath(TRUSTED_SOURCE_ROOT)))
    candidate = os.path.normcase(os.path.realpath(os.fspath(path)))
    if not candidate.startswith(trusted_root + os.sep):
        raise RuntimeError(f"Phone Link source must be within {trusted_root}")

    resolved = Path(candidate)
    if not resolved.exists():
        raise RuntimeError(f"Phone Link source does not exist: {resolved}")
    if not resolved.is_dir():
        raise RuntimeError(f"Phone Link source is not a directory: {resolved}")
    return resolved


def safe_child_path(parent: Path, relative_path: str) -> Path:
    """Return a normalized child path only when it remains below ``parent``."""
    root = os.path.normcase(os.path.realpath(os.fspath(parent)))
    candidate = os.path.normcase(os.path.realpath(os.path.join(root, relative_path)))
    if not candidate.startswith(root + os.sep):
        raise RuntimeError(f"Path escapes its permitted directory: {relative_path}")
    return Path(candidate)


def resolve_vault_root(explicit_root: Path | None = None) -> tuple[Path, str]:
    """Use the repository containing this script as the only vault destination."""
    trusted = normalized_path(TRUSTED_VAULT_ROOT)
    if explicit_root is not None:
        if normalized_path(explicit_root) != trusted:
            raise RuntimeError(f"Vault root must be the script repository: {trusted}")
        source = "argument"
    else:
        env_root = os.environ.get("IDAHO_VAULT_ROOT")
        if env_root:
            if normalized_path(Path(env_root)) != trusted:
                raise RuntimeError(f"IDAHO_VAULT_ROOT must be the script repository: {trusted}")
            source = "IDAHO_VAULT_ROOT"
        else:
            source = "script location"

    if not TRUSTED_VAULT_ROOT.is_dir():
        raise RuntimeError(f"Script vault root does not exist: {TRUSTED_VAULT_ROOT}")
    return TRUSTED_VAULT_ROOT, source


def file_hash(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            hasher.update(chunk)
    return hasher.hexdigest()[:16]


def resolve_destination(source: Path, target_dir: Path) -> tuple[Path | None, str]:
    destination = safe_child_path(target_dir, source.name)
    if not destination.exists():
        return destination, "direct"

    incoming_hash = file_hash(source)
    if incoming_hash == file_hash(destination):
        return None, "duplicate"

    stem = destination.stem
    suffix = destination.suffix
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    attempt = 0
    while True:
        extra = "" if attempt == 0 else f"-{attempt}"
        candidate = safe_child_path(
            target_dir,
            f"{stem}-{stamp}-{incoming_hash}{extra}{suffix}",
        )
        if not candidate.exists():
            return candidate, "collision"
        if incoming_hash == file_hash(candidate):
            return None, "duplicate"
        attempt += 1


def is_ignored(path: Path) -> bool:
    # Windows filenames are case-insensitive; casefold so DESKTOP.INI,
    # foo.CRDOWNLOAD, etc. are still caught.
    name = path.name.casefold()
    return (
        name in {"desktop.ini", "thumbs.db"}
        or name.startswith("~$")
        or name.endswith(".tmp")
        or name.endswith(".crdownload")
    )


def is_unlocked(path: Path, attempts: int = 20, delay_seconds: float = 0.3) -> bool:
    """True once `path` is openable for shared read AND its size+mtime have
    stopped changing across two consecutive checks -- shared-read access
    alone succeeds while a producer is still writing, so stability is the
    signal that the file is actually done. Two checks 0.3s apart is a
    per-file spot check, not a durable completion guarantee across polling
    cycles -- see PR discussion for why that stronger version isn't in this
    pass."""
    previous_stat: tuple[int, float] | None = None
    for _ in range(attempts):
        try:
            with path.open("rb"):
                pass
            stat_result = path.stat()
            current_stat = (stat_result.st_size, stat_result.st_mtime)
        except OSError:
            previous_stat = None
            time.sleep(delay_seconds)
            continue
        if previous_stat is not None and current_stat == previous_stat:
            return True
        previous_stat = current_stat
        time.sleep(delay_seconds)
    return False


def write_log(log_path: Path, message: str) -> None:
    """Best-effort log write. The vault (an external drive, per this script's
    own contract) can go away mid-run; a log write failing must not be able
    to escape and kill the long-running watcher -- fall back to stderr."""
    line = f"{datetime.now().isoformat(timespec='seconds')}  {message}"
    try:
        log_path.parent.mkdir(parents=True, exist_ok=True)
        with log_path.open("a", encoding="utf-8") as handle:
            handle.write(line + "\n")
    except OSError:
        print("[phone-link-sweep] log write failed", file=sys.stderr)


def move_one(source: Path, target_dir: Path, log_path: Path) -> bool:
    if not source.exists() or not source.is_file() or is_ignored(source):
        return False

    if not is_unlocked(source):
        write_log(log_path, "SKIP (locked)")
        return False

    try:
        destination, disposition = resolve_destination(source, target_dir)
        if destination is None:
            write_log(log_path, "SKIP (duplicate)")
            return False
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(source), str(destination))
    except OSError:
        write_log(log_path, "SKIP (move failed)")
        return False
    write_log(log_path, f"MOVED ({disposition})")
    return True


@contextmanager
def single_instance(lock_path: Path = LOCK_PATH) -> Iterator[bool]:
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    handle = lock_path.open("a+b")
    locked = False
    try:
        # msvcrt locks from the stream's current offset. Ensure the lock file
        # contains byte zero and every process contends for that same byte.
        handle.seek(0)
        if not handle.read(1):
            handle.write(b"\0")
            handle.flush()
        handle.seek(0)
        if os.name == "nt":
            import msvcrt

            try:
                msvcrt.locking(handle.fileno(), msvcrt.LK_NBLCK, 1)
                locked = True
            except OSError:
                yield False
                return
        yield True
    finally:
        if os.name == "nt" and locked:
            try:
                import msvcrt

                handle.seek(0)
                msvcrt.locking(handle.fileno(), msvcrt.LK_UNLCK, 1)
            except OSError:
                # Cleanup best effort: do not mask the primary sweep outcome.
                pass
        handle.close()


def sweep_once(source_dir: Path, target_dir: Path, log_path: Path) -> int:
    moved = 0
    for path in sorted(source_dir.iterdir()):
        if move_one(path, target_dir, log_path):
            moved += 1
    return moved


def watch(source_dir: Path, target_dir: Path, log_path: Path, poll_seconds: float) -> None:
    while True:
        try:
            sweep_once(source_dir, target_dir, log_path)
        except OSError:
            # source_dir itself can become temporarily unreachable (drive
            # unplugged, folder renamed); log and keep polling instead of
            # letting one bad cycle kill the watcher permanently.
            write_log(log_path, "SWEEP FAILED (will retry)")
        time.sleep(poll_seconds)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Phone Link autosweep")
    parser.add_argument("--source", type=Path, default=None, help="Phone Link folder path")
    parser.add_argument("--vault-root", type=Path, help="Destination vault root")
    parser.add_argument("--poll-seconds", type=float, default=5.0, help="Polling interval")
    parser.add_argument("--once", action="store_true", help="Run one sweep and exit")
    args = parser.parse_args(argv)

    if not args.once and not (math.isfinite(args.poll_seconds) and args.poll_seconds > 0):
        parser.error("--poll-seconds must be a finite value greater than 0")

    try:
        target_dir, _ = resolve_vault_root(args.vault_root)
        if args.source is None:
            args.source = DEFAULT_SOURCE
            args.source.mkdir(parents=True, exist_ok=True)
        source_dir = resolve_phone_link_source(args.source)
    except RuntimeError:
        print("Configuration error: rejected Phone Link configuration", file=sys.stderr)
        return 1
    log_path = safe_child_path(target_dir, "!/INBOX/_phone-link-watcher.log")

    with single_instance() as acquired:
        if not acquired:
            return 0

        write_log(log_path, "Watcher active")
        if args.once:
            sweep_once(source_dir, target_dir, log_path)
            return 0

        watch(source_dir, target_dir, log_path, args.poll_seconds)
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
