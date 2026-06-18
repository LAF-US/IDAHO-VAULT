#!/usr/bin/env python3
"""Reconcile dotfolders between the user home directory and this vault.

The script is dry-run by default. Use ``--snapshot --apply`` to copy home
dotfolders into the vault. Use ``--retire --apply`` to move/clean home
dotfolders after they have been preserved.
"""

from __future__ import annotations

import argparse
import filecmp
import hashlib
import json
import re
import shutil
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parent
CACHE_PATH = REPO_ROOT / "!-dotfolder-hashcache.json"
STUB_TEXT = "¿!?"
SECRET_PATTERNS = tuple(
    re.compile(pattern)
    for pattern in (
        r"id_\w+$",
        r"id_\w+\.\w+$",
        r"id_ed25519$",
        r"id_ed25519\.pub$",
        r"allowed_signers$",
        r"known_hosts$",
        r"_signing",
        r"authorized_keys",
        r"1Password/config",
        r"auth\.json",
        r"accounts\.json",
        r"signal-cli/data/",
        r"_cacache/",
        r"\.pem$",
        r"\.key$",
        r"credentials\.json",
        r"token\.json",
        r"tokens\.json",
        r"oauth.*\.json",
        r"client_secret.*\.json",
        r"vault-courier-key\.json",
        r"page_id_routing_test\.ts$",
    )
)
SKIP_DOTDIRS = {
    ".ssh",
    ".npm",
    ".npm-cache",
    ".cache",
    ".ollama",
    ".local/share/signal-cli",
    ".local/share/opencode",
    ".config/1Password",
    ".pip-cache",
    ".uv-cache",
    ".pycache",
    ".pytest_cache",
    ".ruff_cache",
    ".venv",
    ".vscode",
    ".codex",
    ".ipynb_checkpoints",
    ".jupyter",
}


@dataclass(frozen=True)
class FileEntry:
    path: Path
    size: int
    mtime_ns: int


@dataclass
class ReconcileResult:
    dot: str
    files_home: int = 0
    files_vault: int = 0
    unique_to_home: int = 0
    unique_to_vault: int = 0
    identical: int = 0
    conflicts: int = 0
    refused_paths: int = 0
    scan_seconds: float = 0.0
    error: str | None = None


class HashCache:
    def __init__(self, path: Path, *, disabled: bool, read_only: bool = False) -> None:
        self.path = path
        self.disabled = disabled
        self.read_only = read_only
        self.dirty = False
        self.data: dict[str, dict[str, Any]] = {}

    def load(self) -> None:
        if self.disabled or not self.path.exists():
            return
        try:
            raw = json.loads(self.path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return
        if isinstance(raw, dict):
            self.data = {
                str(key): value
                for key, value in raw.items()
                if isinstance(value, dict)
            }

    def save(self) -> None:
        if self.disabled or self.read_only or not self.dirty:
            return
        self.path.write_text(
            json.dumps(self.data, sort_keys=True, separators=(",", ":")),
            encoding="utf-8",
        )

    def sha256(self, path: Path, key: str) -> str:
        stat = path.stat()
        cached = self.data.get(key)
        if (
            isinstance(cached, dict)
            and cached.get("size") == stat.st_size
            and cached.get("mtime_ns") == stat.st_mtime_ns
            and isinstance(cached.get("sha256"), str)
        ):
            return cached["sha256"]

        digest = hashlib.sha256()
        with path.open("rb") as handle:
            for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                digest.update(chunk)
        value = digest.hexdigest()
        self.data[key] = {
            "size": stat.st_size,
            "mtime_ns": stat.st_mtime_ns,
            "sha256": value,
        }
        self.dirty = True
        return value


def normalize_dot(raw: str) -> str:
    dot = raw[1:] if raw.startswith(".") else raw
    if not dot or "/" in dot or "\\" in dot:
        raise ValueError(f"Invalid dotfolder name: {raw!r}")
    return dot


def is_secret_path(rel_path: str) -> bool:
    normalized = rel_path.replace("\\", "/")
    return any(pattern.search(normalized) for pattern in SECRET_PATTERNS)


def relative_file_map(root: Path) -> dict[str, FileEntry]:
    if not root.exists():
        return {}
    files: dict[str, FileEntry] = {}
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        stat = path.stat()
        rel = path.relative_to(root).as_posix()
        files[rel] = FileEntry(path=path, size=stat.st_size, mtime_ns=stat.st_mtime_ns)
    return files


def write_stub_files(dot: str, vault_dir: Path, *, quiet: bool) -> list[str]:
    created: list[str] = []
    if not vault_dir.exists():
        vault_dir.mkdir(parents=True)
        created.append(f"directory .{dot}")

    stub_path = vault_dir / "stub.txt"
    if not stub_path.exists():
        stub_path.write_text(STUB_TEXT, encoding="utf-8")
        created.append("stub.txt")
        if not quiet:
            print(f"  [NEW] .{dot}/stub.txt")

    name_path = vault_dir / f"{dot.upper()}.md"
    if not name_path.exists():
        name_path.write_text(
            "\n".join(
                [
                    "---",
                    "authority: LOGAN",
                    "related:",
                    f"  - {dot.upper()}",
                    "  - imported_software",
                    "  - runtime",
                    "---",
                    "",
                    f"**.{dot}** - Imported software runtime persona.",
                    "",
                    f"{dot} runtime and configuration.",
                    "",
                ]
            ),
            encoding="utf-8",
        )
        created.append(name_path.name)
        if not quiet:
            print(f"  [NEW] .{dot}/{name_path.name}")
    return created


def remove_empty_dirs(root: Path) -> None:
    if not root.exists():
        return
    for path in sorted((p for p in root.rglob("*") if p.is_dir()), reverse=True):
        try:
            path.rmdir()
        except OSError:
            # Non-empty directories, races, and permissions are safe to ignore here.
            pass


def files_match(left: Path, right: Path) -> bool:
    if not right.exists() or not right.is_file():
        return False
    try:
        return left.stat().st_size == right.stat().st_size and filecmp.cmp(
            left, right, shallow=False
        )
    except OSError:
        return False


def copy_or_move(src: Path, dst: Path, *, snapshot: bool) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    if dst.exists():
        if not files_match(src, dst):
            raise FileExistsError(f"Refusing to overwrite existing destination: {dst}")
        if not snapshot:
            src.unlink()
        return
    if snapshot:
        shutil.copy2(src, dst)
    else:
        shutil.move(str(src), str(dst))


def reconcile_dot(
    dot: str,
    *,
    home_root: Path,
    vault_root: Path,
    cache: HashCache,
    apply: bool,
    snapshot: bool,
    prune: bool,
    stub: bool,
    force: bool,
    quiet: bool,
) -> ReconcileResult:
    home_dir = home_root / f".{dot}"
    vault_dir = vault_root / f".{dot}"
    start = time.monotonic()

    if not quiet:
        mode = "SNAPSHOT" if snapshot else "RETIRE"
        if stub and not apply and not snapshot:
            mode = "STUB"
        elif stub:
            mode = f"{mode} + STUB"
        print("-" * 60)
        print(f"DOTFOLDER: .{dot}")
        print(f"  MODE:   {mode}{' + PRUNE' if prune and not snapshot else ''}")
        print(f"  HOME:   {home_dir}")
        print(f"  VAULT:  {vault_dir}")

    if stub and apply:
        write_stub_files(dot, vault_dir, quiet=quiet)

    if not home_dir.exists():
        if not quiet:
            print(f"[SKIP] {home_dir} does not exist.")
        return ReconcileResult(dot=dot, scan_seconds=time.monotonic() - start)

    home_files = relative_file_map(home_dir)
    vault_files = relative_file_map(vault_dir)
    rel_paths = sorted(set(home_files) | set(vault_files))
    unique_home: list[str] = []
    unique_vault: list[str] = []
    identical: list[str] = []
    conflicts: list[str] = []
    refused_paths: list[str] = []

    for rel in rel_paths:
        if is_secret_path(rel):
            refused_paths.append(rel)
            if force and not quiet:
                print("  [DENIED] credential-like path refused; details suppressed")
            continue

        in_home = rel in home_files
        in_vault = rel in vault_files
        if in_home and not in_vault:
            unique_home.append(rel)
        elif in_vault and not in_home:
            unique_vault.append(rel)
        elif home_files[rel].size != vault_files[rel].size:
            conflicts.append(rel)
        else:
            home_hash = cache.sha256(home_files[rel].path, f"home/{dot}/{rel}")
            vault_hash = cache.sha256(vault_files[rel].path, f"vault/{dot}/{rel}")
            if home_hash == vault_hash:
                identical.append(rel)
            else:
                conflicts.append(rel)

    result = ReconcileResult(
        dot=dot,
        files_home=len(home_files),
        files_vault=len(vault_files),
        unique_to_home=len(unique_home),
        unique_to_vault=len(unique_vault),
        identical=len(identical),
        conflicts=len(conflicts),
        refused_paths=len(refused_paths),
        scan_seconds=time.monotonic() - start,
    )

    print_summary(result, unique_home, unique_vault, identical, conflicts, refused_paths, quiet=quiet)
    if not apply:
        if unique_home or (identical and not snapshot) or conflicts:
            hint = "--snapshot --apply" if snapshot else "--retire --apply"
            print(f"--- DRY RUN -- pass {hint} to execute ---")
        return result

    print("--- APPLYING ---")
    if unique_home or conflicts or stub:
        write_stub_files(dot, vault_dir, quiet=quiet)

    for rel in conflicts:
        home_src = home_files[rel].path
        home_dst = vault_dir / f"{rel}.home"
        if not quiet:
            action = "COPY" if snapshot else "MOVE"
            print(f"  PRESERVE vault version in place: {rel}")
            print(f"  {action} home version: {rel}.home")
        copy_or_move(home_src, home_dst, snapshot=snapshot)

    for rel in unique_home:
        if not quiet:
            print(f"  {'COPY' if snapshot else 'MOVE'} {rel}")
        copy_or_move(home_files[rel].path, vault_dir / rel, snapshot=snapshot)

    if not snapshot:
        for rel in identical:
            if not quiet:
                print(f"  DELETE identical home file {rel}")
            home_files[rel].path.unlink()
        remove_empty_dirs(home_dir)

    if prune and not snapshot and home_dir.exists():
        try:
            home_dir.rmdir()
            if not quiet:
                print(f"  PRUNE {home_dir}")
        except OSError:
            if not quiet:
                print(f"  [SKIP] {home_dir} is not empty")

    print("--- DONE ---")
    return result


def print_group(title: str, values: list[str], marker: str, *, quiet: bool) -> None:
    if not values:
        return
    print(f"-- {title} ({len(values)}) --")
    if quiet:
        print(f"  ({len(values)} files)")
    else:
        for value in values:
            print(f"  {marker} {value}")
    print()


def print_summary(
    result: ReconcileResult,
    unique_home: list[str],
    unique_vault: list[str],
    identical: list[str],
    conflicts: list[str],
    refused_paths: list[str],
    *,
    quiet: bool,
) -> None:
    if not quiet:
        print()
        print(f"  HOME:  {result.files_home} file(s)")
        print(f"  VAULT: {result.files_vault} file(s)")
        print(f"  SCAN:  {result.scan_seconds:.1f}s")
        print()
    print_group("UNIQUE TO HOME", unique_home, "+", quiet=quiet)
    print_group("IDENTICAL", identical, "=", quiet=quiet)
    print_group("CONFLICT", conflicts, "!", quiet=quiet)
    print_group("UNIQUE TO VAULT", unique_vault, "-", quiet=quiet)
    if refused_paths:
        print(f"-- REFUSED PATHS ({len(refused_paths)}) --")
        print("  Details suppressed because the filenames match credential-like patterns.")
        print()
    if not (unique_home or identical or conflicts or refused_paths):
        print(f"  Nothing to reconcile for .{result.dot}.")


def iter_home_dotdirs(home_root: Path, *, force: bool) -> list[str]:
    dots: list[str] = []
    for path in sorted(home_root.iterdir(), key=lambda item: item.name.lower()):
        if not path.is_dir() or not path.name.startswith(".") or path.name.startswith(".."):
            continue
        if not force and path.name in SKIP_DOTDIRS:
            continue
        dots.append(normalize_dot(path.name))
    return dots


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("dot_name", nargs="?", help="Dotfolder name, with or without leading dot.")
    parser.add_argument("--apply", action="store_true", help="Execute changes. Default is dry-run.")
    parser.add_argument(
        "--snapshot",
        action="store_true",
        help="Copy home files into vault while leaving home files in place.",
    )
    parser.add_argument(
        "--retire",
        action="store_true",
        help="Move/clean home files after preserving them in the vault.",
    )
    parser.add_argument("--prune", action="store_true", help="Remove empty home dotfolder after --retire.")
    parser.add_argument("--stub", action="store_true", help="Create vault anchor stub files.")
    parser.add_argument("--all", action="store_true", help="Process all home dotfolders.")
    parser.add_argument("--no-cache", action="store_true", help="Skip persistent hash cache.")
    parser.add_argument("--force", action="store_true", help="Include normally skipped cache/runtime dirs.")
    parser.add_argument("--quiet", action="store_true", help="Suppress per-file output.")
    parser.add_argument("--home-root", type=Path, default=Path.home(), help="Home root to scan.")
    parser.add_argument("--vault-root", type=Path, default=REPO_ROOT, help="Vault root to write.")
    parser.add_argument("--cache-path", type=Path, default=CACHE_PATH, help="Hash cache path.")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.snapshot and args.retire:
        raise SystemExit("--snapshot and --retire cannot be combined")
    if args.apply and not (args.snapshot or args.retire):
        raise SystemExit("--apply requires an explicit mode: --snapshot or --retire")
    if args.prune and not args.retire:
        print("[WARN] --prune ignored unless --retire is set")

    cache = HashCache(args.cache_path, disabled=args.no_cache, read_only=not args.apply)
    cache.load()
    results: list[ReconcileResult] = []
    try:
        dots = iter_home_dotdirs(args.home_root, force=args.force) if args.all else []
        if not args.all:
            if not args.dot_name:
                raise SystemExit("dot_name is required unless --all is used")
            dots = [normalize_dot(args.dot_name)]

        for index, dot in enumerate(dots, start=1):
            if args.all:
                print(f"[{index}/{len(dots)}] Processing .{dot}...")
            try:
                results.append(
                    reconcile_dot(
                        dot,
                        home_root=args.home_root,
                        vault_root=args.vault_root,
                        cache=cache,
                        apply=args.apply,
                        snapshot=not args.retire,
                        prune=args.prune,
                        stub=args.stub,
                        force=args.force,
                        quiet=args.quiet,
                    )
                )
            except Exception as exc:
                print(f"[ERROR] Failed to process .{dot}: {exc}")
                results.append(ReconcileResult(dot=dot, error=str(exc)))
    finally:
        cache.save()

    if args.all:
        print("=" * 60)
        print(f"ALL RESULTS ({len(results)} dot-dir(s))")
        print("=" * 60)
        for result in results:
            suffix = f", error={result.error}" if result.error else ""
            print(
                f"  .{result.dot}: {result.files_home} home, {result.files_vault} vault, "
                f"{result.unique_to_home} to-sync, {result.conflicts} conflicts, "
                f"{result.refused_paths} refused, {result.scan_seconds:.1f}s{suffix}"
            )
    return 1 if any(result.error for result in results) else 0


if __name__ == "__main__":
    raise SystemExit(main())
