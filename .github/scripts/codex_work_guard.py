#!/usr/bin/env python3
"""Guard against Codex work escaping approved vault surfaces.

This script is intentionally local-first. CI can prove the guard itself works,
but only a local run can inspect machine temp folders for stranded checkouts or
smoke-test residue.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
FORBIDDEN_DIR_NAMES = {
    ".tmp",
    "tmp",
    "temp",
}
RESIDUE_NAME_PREFIXES = (
    "dotfolder-reconcile-smoke-",
    "codex-",
    "IDAHO-VAULT-",
)
REPO_NAME_MARKERS = (
    "IDAHO-VAULT",
    "idaho-vault",
)


@dataclass(frozen=True)
class Finding:
    severity: str
    code: str
    path: str
    message: str


def normalize(path: Path) -> Path:
    return path.expanduser().resolve()




def run_git(args: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=cwd,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        check=False,
        timeout=30,
    )


def git_toplevel(cwd: Path) -> Path | None:
    result = run_git(["rev-parse", "--show-toplevel"], cwd)
    if result.returncode != 0:
        return None
    return normalize(Path(result.stdout.strip()))


def default_forbidden_roots() -> list[Path]:
    roots: list[Path] = []
    for key in ("TEMP", "TMP"):
        value = os.environ.get(key)
        if value:
            roots.append(Path(value))

    local_app_data = os.environ.get("LOCALAPPDATA")
    if local_app_data:
        roots.append(Path(local_app_data) / "Temp")

    roots.extend([Path("C:/tmp"), Path("/tmp"), Path("/var/tmp")])

    deduped: list[Path] = []
    seen: set[str] = set()
    for root in roots:
        try:
            resolved = normalize(root)
        except OSError:
            continue
        key = os.path.normcase(str(resolved))
        if key not in seen:
            seen.add(key)
            deduped.append(resolved)
    return deduped


def path_parts(path: Path) -> tuple[str, ...]:
    return tuple(part.casefold() for part in path.parts)


def is_forbidden_work_root(path: Path, forbidden_roots: list[Path]) -> bool:
    resolved = normalize(path)
    if any(resolved.is_relative_to(root) for root in forbidden_roots if root.exists()):
        return True

    parts = path_parts(resolved)
    return any(part in FORBIDDEN_DIR_NAMES for part in parts)


def looks_like_repo_or_codex_residue(path: Path) -> bool:
    name = path.name
    if any(name.startswith(prefix) for prefix in RESIDUE_NAME_PREFIXES):
        return True
    if any(marker in name for marker in REPO_NAME_MARKERS):
        return True
    return (path / ".git").exists()


def direct_child_dirs(root: Path) -> list[Path]:
    if not root.exists() or not root.is_dir():
        return []
    try:
        return [child for child in root.iterdir() if child.is_dir()]
    except OSError:
        return []


def audit_current_root(cwd: Path, forbidden_roots: list[Path]) -> list[Finding]:
    findings: list[Finding] = []
    toplevel = git_toplevel(cwd)
    if toplevel is None:
        findings.append(
            Finding(
                severity="error",
                code="not_git_checkout",
                path=str(cwd),
                message="Codex guard must run from a Git checkout.",
            )
        )
        return findings

    if is_forbidden_work_root(toplevel, forbidden_roots):
        findings.append(
            Finding(
                severity="error",
                code="forbidden_checkout_root",
                path=str(toplevel),
                message="Current checkout is under a temp/scratch root; move durable work into the vault checkout or a declared repo worktree.",
            )
        )
    return findings


def audit_forbidden_roots(forbidden_roots: list[Path]) -> list[Finding]:
    findings: list[Finding] = []
    for root in forbidden_roots:
        for child in direct_child_dirs(root):
            if not looks_like_repo_or_codex_residue(child):
                continue
            findings.append(
                Finding(
                    severity="error",
                    code="forbidden_residue",
                    path=str(child),
                    message="Codex/repo-looking residue found in a temp/scratch root.",
                )
            )
    return findings


def finding_to_dict(finding: Finding) -> dict[str, str]:
    return {
        "severity": finding.severity,
        "code": finding.code,
        "path": finding.path,
        "message": finding.message,
    }


def print_findings(findings: list[Finding], *, as_json: bool) -> None:
    if as_json:
        print(json.dumps({"findings": [finding_to_dict(item) for item in findings]}, indent=2))
        return

    if not findings:
        print("codex-work guard: OK")
        return

    print("codex-work guard: forbidden Codex work surface detected.", file=sys.stderr)
    for finding in findings:
        print(f"- {finding.code}: {finding.path}", file=sys.stderr)
        print(f"  {finding.message}", file=sys.stderr)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--scan-forbidden-roots",
        action="store_true",
        help="also scan direct children of temp/scratch roots for Codex or repo residue",
    )
    parser.add_argument(
        "--forbidden-root",
        action="append",
        type=Path,
        default=[],
        help="extra forbidden root to check; may be passed more than once",
    )
    parser.add_argument("--json", action="store_true", help="emit JSON findings")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    forbidden_roots = default_forbidden_roots()
    forbidden_roots.extend(normalize(path) for path in args.forbidden_root)

    findings = audit_current_root(Path.cwd(), forbidden_roots)
    if args.scan_forbidden_roots:
        findings.extend(audit_forbidden_roots(forbidden_roots))

    print_findings(findings, as_json=args.json)
    return 1 if any(finding.severity == "error" for finding in findings) else 0


if __name__ == "__main__":
    raise SystemExit(main())
