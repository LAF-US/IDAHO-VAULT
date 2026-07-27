#!/usr/bin/env python3
"""Check tracked Python files for corruption and automation hazards."""

from __future__ import annotations

import argparse
import ast
import hashlib
import itertools
import subprocess  # nosec B404 -- see [tool.bandit] note in pyproject.toml
import sys
from collections import defaultdict
from pathlib import Path


PURGE_MARKER = "***" + "REMOVED" + "***"
INTERACTIVE_TIMEOUT_MARKER = "timeout: interactive"
SUBPROCESS_TIMEOUT_FUNCTIONS = {
    "subprocess.call",
    "subprocess.check_call",
    "subprocess.check_output",
    "subprocess.run",
}


def dotted_name(node: ast.AST) -> str | None:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        base = dotted_name(node.value)
        if base:
            return f"{base}.{node.attr}"
    return None


def line_has_interactive_marker(lines: list[str], lineno: int) -> bool:
    indexes = [lineno - 1, lineno - 2]
    return any(
        0 <= index < len(lines) and INTERACTIVE_TIMEOUT_MARKER in lines[index]
        for index in indexes
    )


def _has_real_timeout(keywords: list[ast.keyword]) -> bool:
    for keyword in keywords:
        if keyword.arg != "timeout":
            continue
        # timeout=None disables the timeout entirely, same as omitting it.
        is_none = isinstance(keyword.value, ast.Constant) and keyword.value.value is None
        return not is_none
    return False


def missing_subprocess_timeout_findings(_path: Path, tree: ast.AST, lines: list[str]) -> list[str]:
    findings: list[str] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        func_name = dotted_name(node.func)
        if func_name not in SUBPROCESS_TIMEOUT_FUNCTIONS:
            continue
        if _has_real_timeout(node.keywords):
            continue
        if line_has_interactive_marker(lines, node.lineno):
            continue
        findings.append(f"subprocess call missing timeout on line {node.lineno}")
    return findings


# The timeout gate above only recognizes calls spelled `subprocess.<fn>`, so any
# other spelling of the same callables would silently bypass it. Rather than chase
# alias resolution, enforce the one canonical spelling: module aliasing and
# from-imports of the gated callables are themselves findings. Imports of
# non-spawning names (CompletedProcess, TimeoutExpired, PIPE, ...) stay legal.
GATED_SUBPROCESS_CALLABLES = frozenset(
    name.removeprefix("subprocess.") for name in SUBPROCESS_TIMEOUT_FUNCTIONS
)


def _aliased_import_findings(node: ast.Import) -> list[str]:
    findings: list[str] = []
    for alias in node.names:
        if alias.name == "subprocess" and alias.asname and alias.asname != "subprocess":
            findings.append(
                f"aliased subprocess import ('import subprocess as {alias.asname}') "
                f"on line {node.lineno} defeats the timeout gate; use plain 'import subprocess'"
            )
    return findings


def _import_from_findings(node: ast.ImportFrom) -> list[str]:
    findings: list[str] = []
    for alias in node.names:
        if alias.name == "*":
            findings.append(
                f"'from subprocess import *' on line {node.lineno} exposes gated "
                "callables as unqualified names, defeating the timeout gate; use "
                "plain 'import subprocess'"
            )
        elif alias.name in GATED_SUBPROCESS_CALLABLES:
            findings.append(
                f"'from subprocess import {alias.name}' on line {node.lineno} "
                f"defeats the timeout gate; call it as subprocess.{alias.name}"
            )
    return findings


def unsafe_subprocess_import_findings(tree: ast.AST) -> list[str]:
    findings: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            findings.extend(_aliased_import_findings(node))
        elif isinstance(node, ast.ImportFrom) and node.module == "subprocess":
            findings.extend(_import_from_findings(node))
    return findings


def python_file_findings(path: Path) -> list[str]:
    findings: list[str] = []
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        findings.append(f"not valid UTF-8: {exc}")
        return findings
    except OSError as exc:
        findings.append(f"could not read file: {exc}")
        return findings
    if PURGE_MARKER in text:
        findings.append("contains purge marker")
    try:
        tree = ast.parse(text, filename=str(path))
    except SyntaxError as exc:
        findings.append(f"syntax error on line {exc.lineno}: {exc.msg}")
        return findings
    findings.extend(unsafe_subprocess_import_findings(tree))
    findings.extend(missing_subprocess_timeout_findings(path, tree, text.splitlines()))
    return findings


def tracked_python_files(root: Path) -> list[Path]:
    try:
        result = subprocess.run(
            ["git", "ls-files", "*.py"],
            cwd=root,
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=30,
        )
    except subprocess.TimeoutExpired as exc:
        raise RuntimeError(f"git ls-files timed out after 30s in {root}") from exc
    except OSError as exc:
        raise RuntimeError(f"git ls-files could not run in {root}: {exc}") from exc
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "git ls-files failed")
    return [
        root / line
        for line in result.stdout.splitlines()
        if line and (root / line).is_file()
    ]


def _display_path(path: Path, root: Path) -> str:
    """Render ``path`` relative to ``root``, falling back to the raw path if
    it isn't actually under root (e.g. a symlinked or unrelated tree)."""
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return str(path)


def _digests_by_content(files: list[Path]) -> dict[str, list[Path]]:
    by_digest: dict[str, list[Path]] = defaultdict(list)
    for path in files:
        try:
            content = path.read_bytes()
        except OSError:
            # An unreadable file is already reported by python_file_findings();
            # skip it here rather than crash the duplicate-digest pass.
            continue
        by_digest[hashlib.sha256(content).hexdigest()].append(path)
    return by_digest


def _flattened_duplicate_pairs(root: Path, duplicates: list[Path]) -> list[tuple[Path, Path]]:
    """Pair each root-level flattened-name copy with each nested canonical copy
    sharing its content digest."""
    root_level = [path for path in duplicates if path.parent == root and "-" in path.name]
    nested = [path for path in duplicates if path.parent != root]
    return list(itertools.product(root_level, nested))


def flattened_duplicate_findings(root: Path, files: list[Path]) -> list[tuple[Path, str]]:
    findings: list[tuple[Path, str]] = []
    for duplicates in _digests_by_content(files).values():
        if len(duplicates) < 2:
            continue
        for flattened, canonical in _flattened_duplicate_pairs(root, duplicates):
            findings.append(
                (flattened, f"byte-identical flattened duplicate of {_display_path(canonical, root)}")
            )
    return findings


def collect_findings(root: Path, files: list[Path] | None = None) -> list[tuple[Path, str]]:
    """Return ``(path, message)`` findings for every tracked Python file."""
    if files is None:
        files = tracked_python_files(root)
    findings: list[tuple[Path, str]] = []
    for path in files:
        findings.extend((path, message) for message in python_file_findings(path))
    findings.extend(flattened_duplicate_findings(root, files))
    return findings


def _is_changed_path(path: Path, root: Path, changed: set[str] | None) -> bool:
    if changed is None:
        return True
    return path.relative_to(root).as_posix() in changed


def _changed_paths_from_stdin() -> set[str]:
    return {stripped for line in sys.stdin.read().splitlines() if (stripped := line.strip())}


def _partition_findings(
    findings: list[tuple[Path, str]], root: Path, changed: set[str] | None
) -> tuple[list[tuple[Path, str]], list[tuple[Path, str]]]:
    """Split findings into (gated, tree-only) by whether their path was changed."""
    gate_findings: list[tuple[Path, str]] = []
    tree_findings: list[tuple[Path, str]] = []
    for path, message in findings:
        target = gate_findings if _is_changed_path(path, root, changed) else tree_findings
        target.append((path, message))
    return gate_findings, tree_findings


def main(argv: list[str] | None = None) -> int:
    """Gate changed paths (fail) and report pre-existing tree violations (warn).

    Mirrors ``check_portable_paths.py``'s changed-vs-tree split: a PR is only
    responsible for what it introduces, so pre-existing integrity debt
    elsewhere in the tree must not fail an unrelated PR — it only warns.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--paths-from-stdin", action="store_true")
    args = parser.parse_args(argv)
    root = args.root.resolve()

    changed = _changed_paths_from_stdin() if args.paths_from_stdin else None

    try:
        all_files = tracked_python_files(root)
    except RuntimeError as exc:
        print(f"Python integrity check: {exc}", file=sys.stderr)
        return 1
    findings = collect_findings(root, all_files)

    gate_findings, tree_findings = _partition_findings(findings, root, changed)

    if tree_findings:
        print(
            f"Python integrity (report-only): {len(tree_findings)} pre-existing "
            "violation(s) outside this change — not failing this PR:",
            file=sys.stderr,
        )
        for path, message in tree_findings:
            print(f"  [warn] {_display_path(path, root)}: {message}", file=sys.stderr)

    if gate_findings:
        print("Python integrity check failed:")
        for path, message in gate_findings:
            print(f"- {_display_path(path, root)}: {message}")
        return 1

    print(f"Python integrity check passed for {len(all_files)} tracked files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
