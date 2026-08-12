#!/usr/bin/env python3
"""Watch Phone Link downloads and move completed files into the VAULT root."""

from __future__ import annotations

import argparse
import hashlib
import math
import os
import shutil
import tempfile
import time
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path
from typing import Iterator


DEFAULT_SOURCE = Path.home() / "Downloads" / "Phone Link"
LEGACY_VAULT_ROOT = Path(r"C:\Users\loganf\Documents\IDAHO-VAULT")
LOCK_PATH = Path(tempfile.gettempdir()) / "idaho-vault-phone-link-sweep.lock"


def require_existing_dir(path: Path, label: str) -> Path:
    resolved = path.resolve()
    if not resolved.exists():
        raise RuntimeError(f"{label} does not exist: {resolved}")
    if not resolved.is_dir():
        raise RuntimeError(f"{label} is not a directory: {resolved}")
    return resolved


def resolve_vault_root(explicit_root: Path | None = None) -> tuple[Path, str]:
    """Resolve the destination root from explicit config, env var, then legacy fallback."""
    if explicit_root is not None:
        return require_existing_dir(explicit_root, "Vault root"), "argument"

    env_root = os.environ.get("IDAHO_VAULT_ROOT")
    if env_root:
        return require_existing_dir(Path(env_root), "IDAHO_VAULT_ROOT"), "IDAHO_VAULT_ROOT"

    if LEGACY_VAULT_ROOT.exists():
        return require_existing_dir(LEGACY_VAULT_ROOT, "Legacy vault root"), "legacy fallback"

    raise RuntimeError("No vault root configured. Pass --vault-root or set IDAHO_VAULT_ROOT.")


def file_hash(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            hasher.update(chunk)
    return hasher.hexdigest()[:16]


def resolve_destination(source: Path, target_dir: Path) -> tuple[Path | None, str]:
    destination = target_dir / source.name
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
        candidate = target_dir / f"{stem}-{stamp}-{incoming_hash}{extra}{suffix}"
        if not candidate.exists():
            return candidate, "collision"
        if incoming_hash == file_hash(candidate):
            return None, "duplicate"
        attempt += 1


def is_ignored(path: Path) -> bool:
    name = path.name
    return (
        name in {"desktop.ini", "Thumbs.db"}
        or name.startswith("~$")
        or name.endswith(".tmp")
        or name.endswith(".crdownload")
    )


def is_unlocked(path: Path, attempts: int = 20, delay_seconds: float = 0.3) -> bool:
    """True once `path` is openable for shared read AND its size has stopped
    changing across two consecutive checks -- shared-read access alone
    succeeds while a producer is still writing, so size stability is the
    signal that the file is actually done."""
    previous_size: int | None = None
    for _ in range(attempts):
        try:
            with path.open("rb"):
                pass
            current_size = path.stat().st_size
        except OSError:
            previous_size = None
            time.sleep(delay_seconds)
            continue
        if previous_size is not None and current_size == previous_size:
            return True
        previous_size = current_size
        time.sleep(delay_seconds)
    return False


def write_log(log_path: Path, message: str) -> None:
    log_path.parent.mkdir(parents=True, exist_ok=True)
    line = f"{datetime.now().isoformat(timespec='seconds')}  {message}"
    with log_path.open("a", encoding="utf-8") as handle:
        handle.write(line + "\n")


def move_one(source: Path, target_dir: Path, log_path: Path) -> bool:
    if not source.exists() or not source.is_file() or is_ignored(source):
        return False

    if not is_unlocked(source):
        write_log(log_path, f"SKIP (locked): {source.name}")
        return False

    try:
        destination, disposition = resolve_destination(source, target_dir)
        if destination is None:
            write_log(log_path, f"SKIP (duplicate): {source.name}")
            return False
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(source), str(destination))
    except OSError as exc:
        write_log(log_path, f"SKIP (move failed: {exc}): {source.name}")
        return False
    write_log(log_path, f"MOVED ({disposition}): {source.name} -> {destination}")
    return True


@contextmanager
def single_instance(lock_path: Path = LOCK_PATH) -> Iterator[bool]:
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    handle = lock_path.open("a+b")
    try:
        if os.name == "nt":
            import msvcrt

            try:
                msvcrt.locking(handle.fileno(), msvcrt.LK_NBLCK, 1)
            except OSError:
                yield False
                return
        yield True
    finally:
        if os.name == "nt":
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
        sweep_once(source_dir, target_dir, log_path)
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

    target_dir, root_source = resolve_vault_root(args.vault_root)
    if args.source is None:
        args.source = DEFAULT_SOURCE
        args.source.mkdir(parents=True, exist_ok=True)
    source_dir = require_existing_dir(args.source, "Phone Link source")
    log_path = target_dir / "!" / "INBOX" / "_phone-link-watcher.log"

    with single_instance() as acquired:
        if not acquired:
            return 0

        write_log(
            log_path,
            f"Watcher active. Source='{source_dir}' Target='{target_dir}' VaultRootSource='{root_source}'",
        )
        if args.once:
            sweep_once(source_dir, target_dir, log_path)
            return 0

        watch(source_dir, target_dir, log_path, args.poll_seconds)
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
