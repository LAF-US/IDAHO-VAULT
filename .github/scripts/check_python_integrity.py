#!/usr/bin/env python3
"""Check tracked Python files for corruption and automation hazards."""

from __future__ import annotations

import argparse
import ast
import hashlib
import subprocess
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


def missing_subprocess_timeout_findings(path: Path, tree: ast.AST, lines: list[str]) -> list[str]:
    findings: list[str] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        func_name = dotted_name(node.func)
        if func_name not in SUBPROCESS_TIMEOUT_FUNCTIONS:
            continue
        if any(keyword.arg == "timeout" for keyword in node.keywords):
            continue
        if line_has_interactive_marker(lines, node.lineno):
            continue
        findings.append(f"{path}: subprocess call missing timeout on line {node.lineno}")
    return findings


def python_file_findings(path: Path) -> list[str]:
    findings: list[str] = []
    text = path.read_text(encoding="utf-8", errors="replace")
    if PURGE_MARKER in text:
        findings.append(f"{path}: contains purge marker")
    try:
        tree = ast.parse(text, filename=str(path))
    except SyntaxError as exc:
        findings.append(f"{path}: syntax error on line {exc.lineno}: {exc.msg}")
        return findings
    findings.extend(missing_subprocess_timeout_findings(path, tree, text.splitlines()))
    return findings


def tracked_python_files(root: Path) -> list[Path]:
    result = subprocess.run(
        ["git", "ls-files", "*.py"],
        cwd=root,
        check=False,
        capture_output=True,
        text=True,
        timeout=30,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "git ls-files failed")
    return [
        root / line
        for line in result.stdout.splitlines()
        if line and (root / line).is_file()
    ]


def flattened_duplicate_findings(root: Path, files: list[Path]) -> list[str]:
    by_digest: dict[str, list[Path]] = defaultdict(list)
    for path in files:
        by_digest[hashlib.sha256(path.read_bytes()).hexdigest()].append(path)

    findings: list[str] = []
    for duplicates in by_digest.values():
        if len(duplicates) < 2:
            continue
        root_level = [
            path
            for path in duplicates
            if path.parent == root and "-" in path.name
        ]
        nested = [path for path in duplicates if path.parent != root]
        for flattened in root_level:
            for canonical in nested:
                findings.append(
                    f"{flattened}: byte-identical flattened duplicate of {canonical}"
                )
    return findings


def collect_findings(root: Path) -> list[str]:
    files = tracked_python_files(root)
    findings: list[str] = []
    for path in files:
        findings.extend(python_file_findings(path))
    findings.extend(flattened_duplicate_findings(root, files))
    return findings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2])
    args = parser.parse_args(argv)
    root = args.root.resolve()

    findings = collect_findings(root)
    if findings:
        print("Python integrity check failed:")
        for finding in findings:
            print(f"- {finding}")
        return 1
    print(f"Python integrity check passed for {len(tracked_python_files(root))} tracked files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
