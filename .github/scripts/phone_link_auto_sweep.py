#!/usr/bin/env python3
"""Watch the Phone Link drop folder and sweep files into the VAULT root."""

from __future__ import annotations

import argparse
import hashlib
import os
import shutil
import threading
import time
from datetime import datetime
from pathlib import Path


DEFAULT_SOURCES = (
    Path.home() / "Downloads" / "Mobile Devices",
    Path.home() / "Downloads" / "Phone Link",
)
IGNORED_NAMES = {"desktop.ini", "Thumbs.db"}
IGNORED_SUFFIXES = {".tmp", ".crdownload"}


def resolve_vault_root(explicit_root: Path | None = None) -> Path:
    """Resolve the VAULT root without host-specific hard-coded paths."""
    if explicit_root is not None:
        root = explicit_root.resolve()
    elif os.environ.get("IDAHO_VAULT_ROOT"):
        root = Path(os.environ["IDAHO_VAULT_ROOT"]).resolve()
    else:
        root = Path(__file__).resolve().parents[2]

    if not root.exists():
        raise RuntimeError(f"Vault root does not exist: {root}")
    if not root.is_dir():
        raise RuntimeError(f"Vault root is not a directory: {root}")
    return root


def resolve_source(source: Path) -> Path:
    resolved = source.expanduser().resolve()
    if not resolved.exists():
        raise RuntimeError(f"Phone Link source does not exist: {resolved}")
    if not resolved.is_dir():
        raise RuntimeError(f"Phone Link source is not a directory: {resolved}")
    return resolved


def resolve_sources(sources: list[Path]) -> list[Path]:
    resolved: list[Path] = []
    seen: set[Path] = set()
    for source in sources:
        path = resolve_source(source)
        if path not in seen:
            resolved.append(path)
            seen.add(path)
    return resolved


def short_hash(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()[:16]


def is_ignored(path: Path) -> bool:
    name = path.name
    return (
        name in IGNORED_NAMES
        or name.startswith("~$")
        or path.suffix.lower() in IGNORED_SUFFIXES
    )


def is_ready(path: Path, settle_seconds: float) -> bool:
    """Return true when a file can be opened and its size is stable."""
    if not path.exists() or not path.is_file():
        return False

    try:
        first = path.stat()
        with path.open("rb"):
            pass
        if settle_seconds > 0:
            time.sleep(settle_seconds)
        second = path.stat()
        return first.st_size == second.st_size and first.st_mtime_ns == second.st_mtime_ns
    except OSError:
        return False


def resolve_destination(source: Path, vault_root: Path) -> tuple[Path | None, str]:
    target = vault_root / source.name
    if not target.exists():
        return target, "direct"

    incoming_hash = short_hash(source)
    if incoming_hash == short_hash(target):
        return None, "duplicate"

    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    attempt = 0
    while True:
        extra = "" if attempt == 0 else f"-{attempt}"
        candidate = vault_root / f"{target.stem}-{stamp}-{incoming_hash}{extra}{target.suffix}"
        if not candidate.exists():
            return candidate, "collision"
        if incoming_hash == short_hash(candidate):
            return None, "duplicate"
        attempt += 1


def write_log(log_path: Path, message: str) -> None:
    line = f"{datetime.now().isoformat(timespec='seconds')}  {message}"
    try:
        with log_path.open("a", encoding="utf-8") as handle:
            handle.write(line + "\n")
    except OSError:
        pass


def sweep_once(source_dir: Path, vault_root: Path, log_path: Path, settle_seconds: float) -> int:
    moved = 0
    for path in sorted(source_dir.iterdir(), key=lambda p: p.name.lower()):
        if not path.is_file() or is_ignored(path):
            continue
        if not is_ready(path, settle_seconds):
            write_log(log_path, f"SKIP (not ready): {path.name}")
            continue

        try:
            destination, disposition = resolve_destination(path, vault_root)
            if destination is None:
                path.unlink()
                write_log(log_path, f"DROPPED (duplicate already in vault): {path.name}")
                continue

            shutil.move(str(path), str(destination))
            moved += 1
            write_log(log_path, f"MOVED ({disposition}): {path.name} -> {destination.name}")
        except OSError as exc:
            write_log(log_path, f"ERROR: {path.name}: {exc}")
    return moved


def sweep_sources(source_dirs: list[Path], vault_root: Path, log_path: Path, settle_seconds: float) -> int:
    moved = 0
    for source_dir in source_dirs:
        moved += sweep_once(source_dir, vault_root, log_path, settle_seconds)
    return moved


def watch(source_dirs: list[Path], vault_root: Path, log_path: Path, poll_seconds: float, settle_seconds: float) -> None:
    source_text = "; ".join(str(source_dir) for source_dir in source_dirs)
    write_log(log_path, f"Watcher active. Sources='{source_text}' Target='{vault_root}'")
    sweep_sources(source_dirs, vault_root, log_path, settle_seconds)
    if os.name == "nt":
        watch_windows(source_dirs, vault_root, log_path, settle_seconds)
        return

    while True:
        time.sleep(poll_seconds)
        sweep_sources(source_dirs, vault_root, log_path, settle_seconds)


def watch_windows(source_dirs: list[Path], vault_root: Path, log_path: Path, settle_seconds: float) -> None:
    import ctypes
    from ctypes import wintypes

    kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
    create_file = kernel32.CreateFileW
    create_file.argtypes = [
        wintypes.LPCWSTR,
        wintypes.DWORD,
        wintypes.DWORD,
        wintypes.LPVOID,
        wintypes.DWORD,
        wintypes.DWORD,
        wintypes.HANDLE,
    ]
    create_file.restype = wintypes.HANDLE

    read_changes = kernel32.ReadDirectoryChangesW
    read_changes.argtypes = [
        wintypes.HANDLE,
        wintypes.LPVOID,
        wintypes.DWORD,
        wintypes.BOOL,
        wintypes.DWORD,
        ctypes.POINTER(wintypes.DWORD),
        wintypes.LPVOID,
        wintypes.LPVOID,
    ]
    read_changes.restype = wintypes.BOOL

    close_handle = kernel32.CloseHandle
    close_handle.argtypes = [wintypes.HANDLE]
    close_handle.restype = wintypes.BOOL

    invalid_handle = wintypes.HANDLE(-1).value
    def watch_one(source_dir: Path) -> None:
        handle = create_file(
            str(source_dir),
            0x0001,
            0x00000001 | 0x00000002 | 0x00000004,
            None,
            3,
            0x02000000,
            None,
        )
        if handle == invalid_handle:
            raise ctypes.WinError(ctypes.get_last_error())
        notify_filter = 0x00000001 | 0x00000002 | 0x00000004 | 0x00000008
        try:
            while True:
                buffer = ctypes.create_string_buffer(8192)
                bytes_returned = wintypes.DWORD()
                ok = read_changes(
                    handle,
                    buffer,
                    len(buffer),
                    False,
                    notify_filter,
                    ctypes.byref(bytes_returned),
                    None,
                    None,
                )
                if not ok:
                    raise ctypes.WinError(ctypes.get_last_error())
                sweep_sources(source_dirs, vault_root, log_path, settle_seconds)
                time.sleep(max(settle_seconds, 0.5))
                sweep_sources(source_dirs, vault_root, log_path, settle_seconds)
        finally:
            close_handle(handle)

    threads = [
        threading.Thread(target=watch_one, args=(source_dir,), daemon=False)
        for source_dir in source_dirs
    ]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Sweep Phone Link files into the VAULT root")
    parser.add_argument(
        "--source",
        type=Path,
        action="append",
        help="Drop folder to watch; may be supplied multiple times",
    )
    parser.add_argument("--vault-root", type=Path, help="Destination VAULT root")
    parser.add_argument("--log", type=Path, help="Log path")
    parser.add_argument("--once", action="store_true", help="Sweep once and exit")
    parser.add_argument("--poll-seconds", type=float, default=5.0, help="Non-Windows fallback polling interval")
    parser.add_argument("--settle-seconds", type=float, default=0.5, help="Delay used to confirm file stability")
    args = parser.parse_args(argv)

    vault_root = resolve_vault_root(args.vault_root)
    source_dirs = resolve_sources(args.source if args.source else list(DEFAULT_SOURCES))
    log_path = args.log.resolve() if args.log else vault_root / "_phone-link-watcher.log"

    if args.once:
        moved = sweep_sources(source_dirs, vault_root, log_path, args.settle_seconds)
        source_text = "; ".join(str(source_dir) for source_dir in source_dirs)
        print(f"Swept {moved} file(s) from {source_text} into {vault_root}")
        return 0

    watch(source_dirs, vault_root, log_path, args.poll_seconds, args.settle_seconds)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
