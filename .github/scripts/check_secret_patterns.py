#!/usr/bin/env python3
"""Pre-commit/CI guard for accidental secret commits.

This checker is intentionally conservative about output: it reports only the
file path, line number, and rule name. It never prints matched secret text.
"""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


def _repo_root() -> Path:
    # In CI this script executes from the trusted base-branch checkout
    # (trusted-main/), while the changed-file list is computed against the
    # primary workspace (PR head / merge-group tree). File bytes must be read
    # from that workspace, not from the script's own checkout — otherwise
    # newly added files are silently skipped and modified files are scanned
    # at their base contents. Local (pre-commit) runs have no
    # GITHUB_WORKSPACE and fall back to the script's own repository.
    # Trust GITHUB_WORKSPACE only under a real Actions run (GITHUB_ACTIONS is
    # set by the runner): a stale GITHUB_WORKSPACE in a developer shell could
    # point at some other real directory, silently scanning the wrong tree.
    if os.environ.get("GITHUB_ACTIONS") == "true":
        workspace = os.environ.get("GITHUB_WORKSPACE", "")
        root = Path(workspace).resolve() if workspace else None
        if root is None or not root.is_dir():
            # Fail closed: a bogus workspace would make every scanned path
            # resolve nonexistent and be silently skipped — a false pass.
            raise SystemExit(f"GITHUB_WORKSPACE is not a directory: {workspace!r}")
        # Structural check, not just existence: confirm this actually is the
        # IDAHO-VAULT checkout before trusting it as a scan root, rather than
        # a bogus/foreign directory that happens to exist.
        if not (root / "AGENTS.md").is_file() or not (root / ".git").exists():
            raise SystemExit(f"GITHUB_WORKSPACE does not look like the IDAHO-VAULT repo root: {root}")
        return root
    return Path(__file__).resolve().parents[2]


REPO_ROOT = _repo_root()
WINDOWS_COPY_SUFFIX_RE = re.compile(r" \(\d+\)(?=$|\.)")
PRESERVED_COPY_SUFFIX_RE = re.compile(r"\.(?:home|vault)(?:\.[0-9a-f]{12})?$", re.IGNORECASE)
SECRET_PATH_PATTERNS = (
    re.compile(r"(^|/)\.env(\.|$)"),
    re.compile(r"(^|/)\.envrc$"),
    re.compile(r"(^|/)\.op(/|$)"),
    re.compile(r"(^|/)secrets?(/|$)", re.IGNORECASE),
    re.compile(r"(^|/)\.mcp-auth(/|$)"),
    re.compile(r"(^|/)(credentials?|tokens?|client_secret|oauth).*\.json$", re.IGNORECASE),
    re.compile(r"(^|/)\.credentials.*\.json$", re.IGNORECASE),
    re.compile(r"(^|/).*-key\.json$", re.IGNORECASE),
    re.compile(r"(^|/).*service-account\.json$", re.IGNORECASE),
    re.compile(r"(^|/)Google Passwords.*\.csv$", re.IGNORECASE),
    re.compile(r"(^|/).*passwords.*\.csv$", re.IGNORECASE),
    re.compile(r"(^|/).*recovery[-_]codes.*", re.IGNORECASE),
    re.compile(r"\.(pem|p12|pfx|key)$", re.IGNORECASE),
    re.compile(r"(^|/)(id_rsa|id_ed25519)(\.|$)"),
    re.compile(r"(^|/)(auth|accounts)\.json$", re.IGNORECASE),
    re.compile(r"(^|/)(known_hosts|allowed_signers)(\.|$)", re.IGNORECASE),
    re.compile(r"(^|/).*_signing(?:\.|$)", re.IGNORECASE),
    re.compile(r"(^|/)(\.npmrc|\.pypirc|\.netrc|rclone\.conf)$"),
)

ALLOW_PATH_PATTERNS = (
    re.compile(r"(^|/)\.env\.(example|template)$"),
    re.compile(r"\.env\.(example|template)$"),
    # .op/ in this vault is a governance/documentation chamber, not a live
    # 1Password CLI config dir. Allow top-level .op/ doc files (.md, .txt)
    # — [^/]+ intentionally excludes subdirectories — while still
    # flagging extensionless credential files like .op/config.
    re.compile(r"^\.op/(1password-hygiene-policy\.json|[^/]+\.(md|txt))$"),
)

SECRET_CONTENT_PATTERNS = {
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


@dataclass(frozen=True)
class Finding:
    path: str
    line: int | None
    rule: str


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


def run_git(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=REPO_ROOT,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        check=False,
    )


def staged_paths() -> list[str]:
    result = run_git(["diff", "--cached", "--name-only", "--diff-filter=ACMR", "-z"])
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "git diff failed")
    return [path for path in result.stdout.split("\0") if path]


def stdin_paths() -> list[str]:
    return [
        raw.decode("utf-8", errors="replace")
        for raw in sys.stdin.buffer.read().split(b"\0")
        if raw
    ]


def normalized_path_variants(path: str) -> set[str]:
    normalized = path.replace("\\", "/")
    variants = {normalized}

    windows_copy = "/".join(
        WINDOWS_COPY_SUFFIX_RE.sub("", segment) for segment in normalized.split("/")
    )
    variants.add(windows_copy)

    for candidate in tuple(variants):
        stripped = candidate
        while True:
            next_value = PRESERVED_COPY_SUFFIX_RE.sub("", stripped)
            if next_value == stripped:
                break
            stripped = next_value
            variants.add(stripped)
    return variants


def path_findings(path: str) -> list[Finding]:
    variants = normalized_path_variants(path)
    if any(
        pattern.search(candidate)
        for candidate in variants
        for pattern in ALLOW_PATH_PATTERNS
    ):
        return []
    if any(
        pattern.search(candidate)
        for candidate in variants
        for pattern in SECRET_PATH_PATTERNS
    ):
        return [Finding(path=path, line=None, rule="secret_path")]
    return []

def staged_file_bytes(path: str) -> bytes | None:
    result = subprocess.run(
        ["git", "show", f":{path}"],
        cwd=REPO_ROOT,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        return None
    return result.stdout


def worktree_file_bytes(path: str) -> bytes | None:
    full_path = REPO_ROOT / path
    if not full_path.is_file():
        return None
    return full_path.read_bytes()


def content_findings(path: str, data: bytes) -> list[Finding]:
    text = data.decode("utf-8", errors="replace")
    findings: list[Finding] = []
    for line_number, line in enumerate(text.splitlines(), start=1):
        for rule, pattern in SECRET_CONTENT_PATTERNS.items():
            if pattern.search(line):
                if is_allowed_content_match(rule, line):
                    continue
                findings.append(Finding(path=path, line=line_number, rule=rule))
    return findings


def findings_for_paths(paths: list[str], *, staged: bool) -> list[Finding]:
    findings: list[Finding] = []
    for path in paths:
        data = staged_file_bytes(path) if staged else worktree_file_bytes(path)
        if data is None:
            continue
        findings.extend(path_findings(path))
        findings.extend(content_findings(path, data))
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--staged", action="store_true", help="check staged files")
    parser.add_argument("--paths-from-stdin", action="store_true", help="check NUL-delimited changed paths from stdin")
    args = parser.parse_args()

    if args.staged and args.paths_from_stdin:
        parser.error("--staged and --paths-from-stdin are mutually exclusive")

    paths = stdin_paths() if args.paths_from_stdin else staged_paths()
    findings = findings_for_paths(paths, staged=args.staged)

    if not findings:
        print("secret-pattern guard: OK")
        return 0

    print("secret-pattern guard: possible secret material detected.", file=sys.stderr)
    print("No secret values are shown below; inspect the files locally.", file=sys.stderr)
    for finding in sorted(set(findings), key=lambda item: (item.path, item.line or 0, item.rule)):
        location = f"{finding.path}:{finding.line}" if finding.line is not None else finding.path
        print(f"  {location}  [{finding.rule}]", file=sys.stderr)
    print("Move secrets to 1Password or environment variables before committing.", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
