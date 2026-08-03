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
import subprocess  # nosec B404 -- see [tool.bandit] note in pyproject.toml
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parent
CACHE_PATH = REPO_ROOT / "!-dotfolder-hashcache.json"
DEFAULT_CONTAINMENT_MANIFEST = Path(".tmp/dotfolder-containment/manifest.local.json")
STUB_TEXT = "¿!?"
MAX_CONTENT_SCAN_BYTES = 1024 * 1024
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
CONTENT_SECRET_PATTERNS = {
    "github_token": re.compile(r"\b(?:ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9_]{30,}\b"),
    "openai_key": re.compile(r"\bsk-(?:proj-)?[A-Za-z0-9_-]{32,}\b"),
    "anthropic_key": re.compile(r"\bsk-ant-[A-Za-z0-9_-]{32,}\b"),
    "slack_token": re.compile(r"\bxox(?:b|p|o|a|r|s)-[A-Za-z0-9-]{20,}\b"),
    "private_key_block": re.compile(r"-----BEGIN (?:RSA |OPENSSH |EC |DSA )?PRIVATE KEY-----"),
    "google_api_key": re.compile(r"\bAIza[0-9A-Za-z_-]{35}\b"),
    "generic_secret_assignment": re.compile(
        r"""(?ix)
        ["']?\b(api[_-]?key|secret|token|password|passwd|pwd)\b["']?
        \s*[:=]\s*["']?[A-Za-z0-9_./+=:-]{24,}
        """
    ),
}
RUNTIME_DOTFOLDERS = {
    ".cache",
    ".ipynb_checkpoints",
    ".ollama",
    ".pycache",
    ".pytest_cache",
    ".ruff_cache",
    ".uv-cache",
    ".venv",
    ".vscode",
}
RUNTIME_PATH_PATTERNS = tuple(
    re.compile(pattern, re.IGNORECASE)
    for pattern in (
        r"(^|/)(cache|\.cache|tmp|\.tmp|log|logs|__pycache__)(/|$)",
        r"(^|/)(multi|node_modules|opencode)(/|$)",
        r"(^|/)(models/blobs|extensions|site-packages)(/|$)",
        r"(^|/)(sessions|archived_sessions|usage-data|computer-use|computer-use-turn-ended)(/|$)",
        r"(^|/)(plugins|shell-snapshots|worktrees|\.remote-plugin-install-staging)(/|$)",
        r"\.(sqlite|sqlite-shm|sqlite-wal|log|tmp|zip|exe|dll|pyd|bin)$",
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
    sensitive_paths: int = 0
    unavailable_paths: int = 0
    scan_seconds: float = 0.0
    error: str | None = None


@dataclass(frozen=True)
class ContainmentEntry:
    path: str
    dotfolder: str
    classification: str
    rules: tuple[str, ...]
    size: int


@dataclass(frozen=True)
class ContainmentReport:
    vault_root: Path
    include_ignored: bool
    entries: tuple[ContainmentEntry, ...]


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


def is_allowed_content_match(rule: str, line: str) -> bool:
    """Allow narrow generic placeholders without muting dedicated token rules."""
    if rule != "generic_secret_assignment":
        return False
    if "secret-pattern: allow" in line:
        return True
    return bool(
        re.search(r"\bprocess\.env\.[A-Z0-9_]+\b", line)
        or re.search(r"""(?i)["']?env:[A-Z][A-Z0-9_]*["']?""", line)
        or re.search(r"""(?i)["']?\$secretRef(?::[A-Za-z0-9_.:/-]+)?["']?""", line)
        or re.search(r"(?i)\breplace-with-[A-Za-z0-9_-]+\b", line)
    )


def content_secret_rules(path: Path) -> tuple[str, ...]:
    try:
        if path.stat().st_size > MAX_CONTENT_SCAN_BYTES:
            return ()
        data = path.read_bytes()
    except OSError:
        return ("unreadable",)
    if b"\x00" in data:
        return ()
    text = data.decode("utf-8", errors="replace")

    rules: set[str] = set()
    for line in text.splitlines():
        for rule, pattern in CONTENT_SECRET_PATTERNS.items():
            if pattern.search(line) and not is_allowed_content_match(rule, line):
                rules.add(rule)
    return tuple(sorted(rules))


def is_runtime_path(rel_path: str) -> bool:
    normalized = rel_path.replace("\\", "/")
    dotfolder = normalized.split("/", 1)[0]
    return dotfolder in RUNTIME_DOTFOLDERS or any(
        pattern.search(normalized) for pattern in RUNTIME_PATH_PATTERNS
    )


def is_publishable_path(dotfolder: str, rel_path: str, *, size: int) -> bool:
    if size > MAX_CONTENT_SCAN_BYTES:
        return False
    parts = rel_path.replace("\\", "/").split("/")
    name = parts[-1]
    if len(parts) > 1:
        return False
    if name == "stub.txt":
        return True
    expected_anchor = f"{dotfolder.lstrip('.').upper()}.md"
    if name == expected_anchor:
        return True
    if name.endswith((".md", ".txt")) and "secret" not in name.lower():
        return True
    return False


def git_ignored_paths(vault_root: Path, rel_paths: list[str]) -> set[str]:
    if not rel_paths or not (vault_root / ".git").exists():
        return set()
    try:
        result = subprocess.run(
            ["git", "check-ignore", "--stdin"],
            cwd=vault_root,
            input="\n".join(rel_paths),
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
            capture_output=True,
            timeout=30,
        )
    except (subprocess.TimeoutExpired, OSError):
        return set()
    if result.returncode not in {0, 1}:
        return set()
    return set(result.stdout.splitlines())


def iter_containment_tree(vault_root: Path, root: Path) -> list[tuple[str, Path]]:
    entries: list[tuple[str, Path]] = []
    try:
        children = sorted(root.iterdir(), key=lambda item: item.name.lower())
    except OSError:
        return entries
    for child in children:
        rel = child.relative_to(vault_root).as_posix()
        if child.is_dir():
            if is_runtime_path(rel):
                entries.append((rel, child))
            else:
                entries.extend(iter_containment_tree(vault_root, child))
        elif child.is_file():
            entries.append((rel, child))
    return entries


def iter_dotfolder_files(vault_root: Path, *, include_ignored: bool) -> list[tuple[str, Path]]:
    files: list[tuple[str, Path]] = []
    if not vault_root.exists():
        return files
    for dotfolder in sorted(vault_root.iterdir(), key=lambda item: item.name.lower()):
        if not dotfolder.is_dir() or not dotfolder.name.startswith("."):
            continue
        if dotfolder.name in {".git", ".pytest_cache", ".tmp"}:
            continue
        if dotfolder.name in RUNTIME_DOTFOLDERS:
            files.append((dotfolder.name, dotfolder))
            continue
        files.extend(iter_containment_tree(vault_root, dotfolder))
    if include_ignored:
        return files
    ignored = git_ignored_paths(vault_root, [rel for rel, _path in files])
    return [(rel, path) for rel, path in files if rel not in ignored]


def classify_containment_file(vault_root: Path, rel_path: str, path: Path) -> ContainmentEntry:
    normalized = rel_path.replace("\\", "/")
    dotfolder = normalized.split("/", 1)[0]
    inner = normalized.split("/", 1)[1] if "/" in normalized else ""
    path_rules = ("secret_path",) if is_secret_path(normalized) or is_secret_path(inner) else ()
    try:
        size = path.stat().st_size
    except OSError:
        size = 0

    if path_rules:
        classification = "secret"
        rules = path_rules
    elif is_runtime_path(normalized):
        classification = "runtime/cache"
        rules = ()
    else:
        content_rules = content_secret_rules(path)
        rules = tuple(sorted(set(content_rules)))
        if rules:
            classification = "secret"
        elif is_publishable_path(dotfolder, inner, size=size):
            classification = "publishable"
        else:
            classification = "private-preserve"

    return ContainmentEntry(
        path=normalized,
        dotfolder=dotfolder,
        classification=classification,
        rules=rules,
        size=size,
    )


def build_containment_report(vault_root: Path, *, include_ignored: bool) -> ContainmentReport:
    entries = tuple(
        classify_containment_file(vault_root, rel, path)
        for rel, path in iter_dotfolder_files(vault_root, include_ignored=include_ignored)
    )
    return ContainmentReport(vault_root=vault_root, include_ignored=include_ignored, entries=entries)


def containment_summary(report: ContainmentReport) -> dict[str, Any]:
    by_class: dict[str, int] = {}
    by_dotfolder: dict[str, dict[str, int]] = {}
    for entry in report.entries:
        by_class[entry.classification] = by_class.get(entry.classification, 0) + 1
        dot_counts = by_dotfolder.setdefault(entry.dotfolder, {})
        dot_counts[entry.classification] = dot_counts.get(entry.classification, 0) + 1
    return {"total": len(report.entries), "by_class": by_class, "by_dotfolder": by_dotfolder}


def containment_manifest(report: ContainmentReport) -> dict[str, Any]:
    return {
        "version": 1,
        "vault_root": str(report.vault_root),
        "include_ignored": report.include_ignored,
        "summary": containment_summary(report),
        "entries": [
            {
                "path": entry.path,
                "dotfolder": entry.dotfolder,
                "classification": entry.classification,
                "rules": list(entry.rules),
                "size": entry.size,
            }
            for entry in report.entries
        ],
    }


def write_containment_manifest(report: ContainmentReport, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(containment_manifest(report), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def default_containment_manifest_path(vault_root: Path) -> Path:
    return vault_root / DEFAULT_CONTAINMENT_MANIFEST


def print_containment_report(
    report: ContainmentReport, *, quiet: bool, show_secret_findings: bool = True
) -> None:
    summary = containment_summary(report)
    print("DOTFOLDER CONTAINMENT REPORT")
    print(f"  VAULT:           {report.vault_root}")
    print(f"  INCLUDE IGNORED: {str(report.include_ignored).lower()}")
    print(f"  ENTRIES:         {summary['total']}")
    print("-- BY CLASS --")
    for classification, count in sorted(summary["by_class"].items()):
        print(f"  {classification}: {count}")
    print("-- BY DOTFOLDER --")
    for dotfolder, counts in sorted(summary["by_dotfolder"].items()):
        rendered = ", ".join(f"{key}={value}" for key, value in sorted(counts.items()))
        print(f"  {dotfolder}: {rendered}")
    secrets = [entry for entry in report.entries if entry.classification == "secret"]
    if secrets and show_secret_findings:
        print(f"-- SECRET FINDINGS ({len(secrets)}) --")
        for entry in secrets:
            print(f"  {entry.path} [{', '.join(entry.rules)}]")
    elif secrets:
        print(f"[WARN] containment found {len(secrets)} secret-classified file(s); details suppressed")
    elif not quiet and show_secret_findings:
        print("-- SECRET FINDINGS (0) --")

def note_unavailable_path(root: Path, path: Path, unavailable: list[str] | None) -> None:
    if unavailable is None:
        return
    try:
        rel = path.relative_to(root).as_posix()
    except ValueError:
        rel = path.as_posix()
    unavailable.append(rel or ".")


def relative_file_map(root: Path, unavailable: list[str] | None = None) -> dict[str, FileEntry]:
    if not root.exists():
        return {}
    files: dict[str, FileEntry] = {}
    pending = [root]
    while pending:
        current = pending.pop()
        try:
            children = sorted(current.iterdir(), key=lambda item: item.name.lower())
        except OSError:
            note_unavailable_path(root, current, unavailable)
            continue
        for path in children:
            try:
                if path.is_dir():
                    pending.append(path)
                    continue
                if not path.is_file():
                    continue
                stat = path.stat()
            except OSError:
                note_unavailable_path(root, path, unavailable)
                continue
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


def preservation_target(src: Path, preferred: Path) -> Path:
    if not preferred.exists() or files_match(src, preferred):
        return preferred

    digest = hashlib.sha256()
    with src.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    candidate = preferred.with_name(f"{preferred.name}.{digest.hexdigest()[:12]}")
    if candidate.exists() and not files_match(src, candidate):
        raise FileExistsError(f"Refusing to overwrite existing destination: {candidate}")
    return candidate

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

    unavailable_paths: list[str] = []
    home_files = relative_file_map(home_dir, unavailable=unavailable_paths)
    vault_files = relative_file_map(vault_dir, unavailable=unavailable_paths)
    rel_paths = sorted(set(home_files) | set(vault_files))
    unique_home: list[str] = []
    unique_vault: list[str] = []
    identical: list[str] = []
    conflicts: list[str] = []
    sensitive_paths: list[str] = []
    for rel in rel_paths:
        if is_secret_path(rel):
            sensitive_paths.append(rel)

        in_home = rel in home_files
        in_vault = rel in vault_files
        if in_home and not in_vault:
            unique_home.append(rel)
        elif in_vault and not in_home:
            unique_vault.append(rel)
        elif home_files[rel].size != vault_files[rel].size:
            conflicts.append(rel)
        else:
            try:
                home_hash = cache.sha256(home_files[rel].path, f"home/{dot}/{rel}")
                vault_hash = cache.sha256(vault_files[rel].path, f"vault/{dot}/{rel}")
            except OSError:
                unavailable_paths.append(rel)
                continue
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
        sensitive_paths=len(sensitive_paths),
        unavailable_paths=len(unavailable_paths),
        scan_seconds=time.monotonic() - start,
    )

    print_summary(result, unique_home, unique_vault, identical, conflicts, sensitive_paths, unavailable_paths, quiet=quiet)
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
        try:
            home_dst = preservation_target(home_src, vault_dir / f"{rel}.home")
            display_dst = home_dst.relative_to(vault_dir).as_posix()
            if not quiet:
                action = "COPY" if snapshot else "MOVE"
                print(f"  PRESERVE vault version in place: {rel}")
                print(f"  {action} home version: {display_dst}")
            copy_or_move(home_src, home_dst, snapshot=snapshot)
        except OSError:
            unavailable_paths.append(rel)
            if not quiet:
                print(f"  [SKIP] unavailable home version: {rel}")

    for rel in unique_home:
        if not quiet:
            print(f"  {'COPY' if snapshot else 'MOVE'} {rel}")
        try:
            copy_or_move(home_files[rel].path, vault_dir / rel, snapshot=snapshot)
        except OSError:
            unavailable_paths.append(rel)
            if not quiet:
                print(f"  [SKIP] unavailable home file: {rel}")

    if not snapshot:
        for rel in identical:
            if not quiet:
                print(f"  DELETE identical home file {rel}")
            try:
                home_files[rel].path.unlink()
            except OSError:
                unavailable_paths.append(rel)
                if not quiet:
                    print(f"  [SKIP] unavailable identical home file: {rel}")
        remove_empty_dirs(home_dir)
    if prune and not snapshot and home_dir.exists():
        try:
            home_dir.rmdir()
            if not quiet:
                print(f"  PRUNE {home_dir}")
        except OSError:
            if not quiet:
                print(f"  [SKIP] {home_dir} is not empty")

    result.unavailable_paths = len(set(unavailable_paths))
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
    sensitive_paths: list[str],
    unavailable_paths: list[str],
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
    if sensitive_paths:
        print(f"-- SENSITIVE PATHS ({len(sensitive_paths)}) --")
        print("  Names suppressed; these paths are reconciled but must stay out of Git unless explicitly cleared.")
        print()
    if unavailable_paths:
        print(f"-- UNAVAILABLE PATHS ({len(set(unavailable_paths))}) --")
        print("  Some files could not be read or copied, usually because they are live locks or protected runtime state.")
        print()
    if not (unique_home or identical or conflicts or sensitive_paths or unavailable_paths):
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
    parser.add_argument("--containment-report", action="store_true", help="Classify hydrated vault dotfolder cargo without mutating files.")
    parser.add_argument("--include-ignored", action="store_true", help="Include Git-ignored files in --containment-report.")
    parser.add_argument("--manifest", type=Path, help="Optional JSON manifest path for --containment-report.")
    parser.add_argument("--no-containment", action="store_true", help="Skip automatic containment after snapshot/retire runs.")
    parser.add_argument(
        "--containment-manifest",
        type=Path,
        help="Override automatic containment manifest path; aliases --manifest for --containment-report.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.snapshot and args.retire:
        raise SystemExit("--snapshot and --retire cannot be combined")
    if args.manifest and args.containment_manifest:
        raise SystemExit("--manifest and --containment-manifest cannot be combined")
    if args.manifest and not args.containment_report:
        raise SystemExit("--manifest requires --containment-report")
    if args.containment_report and args.apply:
        raise SystemExit("--containment-report is non-mutating and cannot be combined with --apply")
    if args.apply and not (args.snapshot or args.retire):
        raise SystemExit("--apply requires an explicit mode: --snapshot or --retire")
    if args.prune and not args.retire:
        print("[WARN] --prune ignored unless --retire is set")
    if args.containment_report:
        report = build_containment_report(args.vault_root, include_ignored=args.include_ignored)
        print_containment_report(report, quiet=args.quiet)
        manifest_path = args.manifest or args.containment_manifest
        if manifest_path:
            write_containment_manifest(report, manifest_path)
        return 1 if any(entry.classification == "secret" for entry in report.entries) else 0
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
                f"{result.sensitive_paths} sensitive, {result.unavailable_paths} unavailable, "
                f"{result.scan_seconds:.1f}s{suffix}"
            )
    if not args.no_containment:
        report = build_containment_report(args.vault_root, include_ignored=True)
        print_containment_report(report, quiet=args.quiet, show_secret_findings=False)
        if args.apply:
            manifest_path = args.containment_manifest or default_containment_manifest_path(args.vault_root)
            write_containment_manifest(report, manifest_path)
            if not args.quiet:
                print(f"  MANIFEST: {manifest_path}")

    return 1 if any(result.error for result in results) else 0

if __name__ == "__main__":
    raise SystemExit(main())
