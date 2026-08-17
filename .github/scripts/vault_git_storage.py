#!/usr/bin/env python3
"""Guard and bootstrap the Vault's Git, Git LFS, and git-annex ownership lanes.

The default operation is read-only. ``init`` is deliberately explicit and
refuses dirty or detached checkouts because native Windows initialization can
temporarily enter an adjusted branch.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
ANNEX_POINTER_PREFIX = b"/annex/objects/"
LFS_POINTER_PREFIX = b"version https://git-lfs.github.com/spec/v1"


class StorageError(RuntimeError):
    """A storage ownership or bootstrap invariant failed."""


@dataclass(frozen=True)
class Entry:
    mode: str
    oid: str
    path: str


def _run(
    *args: str,
    check: bool = True,
    input_bytes: bytes | None = None,
) -> subprocess.CompletedProcess[bytes]:
    result = subprocess.run(
        list(args),
        cwd=ROOT,
        input=input_bytes,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if check and result.returncode != 0:
        detail = result.stderr.decode("utf-8", errors="replace").strip()
        raise StorageError(f"{' '.join(args)} failed: {detail}")
    return result


def _git(
    *args: str,
    check: bool = True,
    input_bytes: bytes | None = None,
) -> subprocess.CompletedProcess[bytes]:
    return _run("git", *args, check=check, input_bytes=input_bytes)


def _text(result: subprocess.CompletedProcess[bytes]) -> str:
    return result.stdout.decode("utf-8", errors="replace").strip()


def _require_tools() -> dict[str, str]:
    tools = {name: shutil.which(name) or "" for name in ("git", "git-lfs", "git-annex")}
    missing = [name for name, path in tools.items() if not path]
    if missing:
        raise StorageError(f"required tool(s) not on PATH: {', '.join(missing)}")
    _git("lfs", "version")
    _git("annex", "version", "--raw")
    return tools


def _entries(staged: bool, ref: str) -> list[Entry]:
    if staged:
        raw = _git("ls-files", "-s", "-z").stdout
        records = raw.split(b"\0")
        entries: list[Entry] = []
        for record in records:
            if not record:
                continue
            header, path_bytes = record.split(b"\t", 1)
            mode, oid, stage = header.decode("ascii").split()
            if stage != "0":
                raise StorageError("unmerged index entries prevent storage validation")
            entries.append(Entry(mode, oid, path_bytes.decode("utf-8", errors="surrogateescape")))
        return entries

    raw = _git("ls-tree", "-r", "-z", ref).stdout
    entries = []
    for record in raw.split(b"\0"):
        if not record:
            continue
        header, path_bytes = record.split(b"\t", 1)
        mode, object_type, oid = header.decode("ascii").split()
        if object_type == "blob":
            entries.append(Entry(mode, oid, path_bytes.decode("utf-8", errors="surrogateescape")))
    return entries


def _attributes(
    paths: list[str],
    staged: bool,
    ref: str | None,
) -> dict[str, dict[str, str]]:
    if not paths:
        return {}
    args = ["check-attr", "-z"]
    if staged:
        args.append("--cached")
    elif ref is not None:
        args.append(f"--source={ref}")
    args.extend(
        [
            "--stdin",
            "filter",
            "annex.largefiles",
            "annex.backend",
            "annex.numcopies",
            "annex.mincopies",
        ]
    )
    payload = b"\0".join(path.encode("utf-8", errors="surrogateescape") for path in paths) + b"\0"
    fields = _git(*args, input_bytes=payload).stdout.split(b"\0")
    values: dict[str, dict[str, str]] = {}
    for index in range(0, len(fields) - 2, 3):
        path = fields[index].decode("utf-8", errors="surrogateescape")
        attr = fields[index + 1].decode("utf-8", errors="replace")
        value = fields[index + 2].decode("utf-8", errors="replace")
        values.setdefault(path, {})[attr] = value
    return values


def _blob(oid: str) -> bytes:
    return _git("cat-file", "blob", oid).stdout


def _is_annex_pointer(entry: Entry, content: bytes) -> bool:
    if entry.mode == "120000":
        normalized = content.replace(b"\\", b"/")
        return b"/.git/annex/objects/" in normalized or normalized.startswith(
            b".git/annex/objects/"
        )
    return content.startswith(ANNEX_POINTER_PREFIX)


def _annex_pointer_paths(*, staged: bool, ref: str) -> set[str]:
    args = ["grep"]
    if staged:
        args.append("--cached")
    args.extend(["-z", "-l", "-e", "^/annex/objects/"])
    if not staged:
        args.append(ref)
    args.append("--")
    result = _git(*args, check=False)
    if result.returncode not in {0, 1}:
        detail = result.stderr.decode("utf-8", errors="replace").strip()
        raise StorageError(f"git {' '.join(args)} failed: {detail}")
    return {
        path.decode("utf-8", errors="surrogateescape")
        for path in result.stdout.split(b"\0")
        if path
    }


def check_ownership(*, staged: bool, ref: str) -> list[str]:
    entries = _entries(staged, ref)
    attrs = _attributes([entry.path for entry in entries], staged, ref)
    pointer_paths = _annex_pointer_paths(staged=staged, ref=ref)
    errors: list[str] = []

    for entry in entries:
        path_attrs = attrs.get(entry.path, {})
        largefiles = path_attrs.get("annex.largefiles", "unspecified")
        file_filter = path_attrs.get("filter", "unspecified")
        annex_owned = largefiles not in {"nothing", "unspecified", "unset"}
        pointer = entry.path in pointer_paths
        content: bytes | None = None

        if entry.mode == "120000" or annex_owned:
            content = _blob(entry.oid)
            pointer = pointer or _is_annex_pointer(entry, content)

        if file_filter == "lfs" and annex_owned:
            errors.append(f"{entry.path}: claimed by both Git LFS and git-annex")

        if not annex_owned:
            if pointer:
                errors.append(
                    f"{entry.path}: annex pointer lacks an explicit annex.largefiles opt-in"
                )
            continue

        expected = {
            "annex.backend": "SHA256E",
            "annex.numcopies": "2",
            "annex.mincopies": "1",
        }
        for name, wanted in expected.items():
            actual = path_attrs.get(name, "unspecified")
            if actual != wanted:
                errors.append(f"{entry.path}: {name}={actual}, expected {wanted}")

        assert content is not None
        if content.startswith(LFS_POINTER_PREFIX):
            errors.append(f"{entry.path}: LFS pointer found at annex-owned path")
        elif not pointer:
            errors.append(
                f"{entry.path}: annex-owned path contains a raw Git blob; use 'git annex add'"
            )

    return errors


def _annex_initialized() -> bool:
    return bool(_text(_git("config", "--get", "annex.uuid", check=False)))


def _branch() -> str:
    return _text(_git("symbolic-ref", "--quiet", "--short", "HEAD", check=False))


def _disable_global_annex_filter() -> Path:
    info_attributes = Path(_text(_git("rev-parse", "--git-path", "info/attributes")))
    if not info_attributes.is_absolute():
        info_attributes = ROOT / info_attributes
    existing = (
        info_attributes.read_text(encoding="utf-8", errors="replace").splitlines()
        if info_attributes.exists()
        else []
    )
    annex_filter_lines = {"* filter=annex"}
    kept = [line for line in existing if line.strip() not in annex_filter_lines]
    kept.append(
        "# IDAHO-VAULT: annex hydration is hook-driven; do not override Git LFS filters."
    )
    info_attributes.parent.mkdir(parents=True, exist_ok=True)
    temporary = info_attributes.with_name(f"{info_attributes.name}.vault-storage.tmp")
    temporary.write_text("\n".join(kept).rstrip() + "\n", encoding="utf-8", newline="\n")
    os.replace(temporary, info_attributes)
    return info_attributes


def initialize(description: str) -> None:
    _require_tools()
    branch = _branch()
    if not branch:
        raise StorageError("refusing annex initialization from detached HEAD")
    dirty = _text(_git("status", "--porcelain=v1", "--untracked-files=all"))
    if dirty:
        raise StorageError("refusing annex initialization in a dirty checkout")

    if not _annex_initialized():
        git_dir = Path(_text(_git("rev-parse", "--absolute-git-dir")))
        with tempfile.TemporaryDirectory(prefix="annex-bootstrap-hooks-", dir=git_dir) as hook_dir:
            _git(
                "-c",
                f"core.hooksPath={hook_dir}",
                "-c",
                "annex.addunlocked=true",
                "annex",
                "init",
                description,
            )

    _git("config", "annex.addunlocked", "true")
    _git("config", "annex.thin", "false")
    _git("config", "remote.origin.annex-sync", "false")
    _git("annex", "config", "--set", "annex.addunlocked", "true")
    _git("annex", "config", "--set", "annex.backend", "SHA256E")
    _git("annex", "numcopies", "2")
    _git("annex", "mincopies", "1")
    _disable_global_annex_filter()

    after = _branch()
    if after != branch:
        if _text(_git("status", "--porcelain=v1", "--untracked-files=all")):
            raise StorageError(
                f"git-annex entered {after!r} and left changes; "
                f"original branch {branch!r} was not restored"
            )
        _git("switch", branch)

    _git("annex", "smudge", "--update")

    print(f"git-annex initialized for {description!r}; active branch preserved as {branch!r}")


def doctor() -> int:
    tools = _require_tools()
    initialized = _annex_initialized()
    payload_attrs = _attributes(["example.txt", "example.png"], False, None)
    report = {
        "tools": tools,
        "git": _text(_git("--version")),
        "git_lfs": _text(_git("lfs", "version")),
        "git_annex": _text(_git("annex", "version", "--raw")),
        "annex_initialized": initialized,
        "branch": _branch() or "DETACHED",
        "attributes": payload_attrs,
        "committed_ownership_errors": check_ownership(staged=False, ref="HEAD"),
    }
    if initialized:
        report["annex_uuid"] = _text(_git("config", "--get", "annex.uuid"))
        report["annex_addunlocked"] = _text(_git("config", "--get", "annex.addunlocked"))
        report["annex_thin"] = _text(_git("config", "--get", "annex.thin"))
        report["origin_annex_sync"] = _text(
            _git("config", "--get", "remote.origin.annex-sync", check=False)
        )
    print(json.dumps(report, indent=2, sort_keys=True))
    return 1 if report["committed_ownership_errors"] else 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    check_parser = subparsers.add_parser("check", help="validate Git/LFS/annex ownership")
    check_parser.add_argument("--staged", action="store_true", help="validate the Git index")
    check_parser.add_argument(
        "--ref", default="HEAD", help="tree to validate when not using --staged"
    )
    subparsers.add_parser("doctor", help="report tool and repository integration")
    init_parser = subparsers.add_parser("init", help="initialize annex in a clean clone")
    init_parser.add_argument(
        "--description", required=True, help="stable device and OS description"
    )
    args = parser.parse_args(argv)

    try:
        if args.command == "check":
            errors = check_ownership(staged=args.staged, ref=args.ref)
            if errors:
                for error in errors:
                    print(f"storage ownership: {error}", file=sys.stderr)
                return 1
            print("storage ownership: OK")
            return 0
        if args.command == "doctor":
            return doctor()
        if args.command == "init":
            initialize(args.description)
            return 0
    except StorageError as exc:
        print(f"vault git storage: {exc}", file=sys.stderr)
        return 2
    raise AssertionError("unreachable")


if __name__ == "__main__":
    raise SystemExit(main())
