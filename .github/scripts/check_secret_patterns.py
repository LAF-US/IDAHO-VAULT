#!/usr/bin/env python3
"""Pre-commit/CI guard for accidental secret commits.

This checker is intentionally conservative about output: it reports only the
file path, line number, and rule name. It never prints matched secret text.
"""

from __future__ import annotations

import argparse
import base64
import math
import os
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
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
    # Filenames that are ALWAYS credential material — a thin BELT behind the
    # content detectors (content_secret_findings), which are the real,
    # path-independent guard. Deliberately NOT whole dotfolders or ambiguous
    # config (`.dropbox/`, `.docker/config.json`, `.colima/ssh_config`): a secret
    # guard flags secret MATERIAL, not folder names — flagging a chamber by path
    # is theatre that both false-positives on non-secret persona-chamber content
    # and misses a secret the moment it is renamed. Added 2026-07-02.
    re.compile(r"(^|/)adbkey(\.pub)?$"),                        # Android debug key
    re.compile(r"(^|/)hostkeys$", re.IGNORECASE),              # Dropbox/app host key material
    re.compile(r"(^|/)\.subversion/auth(/|$)", re.IGNORECASE),  # SVN cached credentials
    re.compile(r"(^|/)\.cargo/credentials(\.toml)?$", re.IGNORECASE),  # crates.io token
    re.compile(r"(^|/)gradle\.properties$", re.IGNORECASE),    # commonly holds signing keys/tokens
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
    "openai_key": re.compile(
        r"\bsk-(?:proj-[A-Za-z0-9_-]{32,}|svcacct-[A-Za-z0-9_-]{32,}|[A-Za-z0-9]{32,})\b"
    ),
    "anthropic_key": re.compile(r"\bsk-ant-[A-Za-z0-9_-]{32,}\b"),
    "slack_token": re.compile(r"\bxox(?:b|p|o|a|r|s)-[A-Za-z0-9-]{20,}\b"),
    # Broadened 2026-07-02: the old alternation missed ENCRYPTED / PGP / SSH2 /
    # PuTTY variants and the "PRIVATE KEY BLOCK" (PGP) suffix — a PEM block in
    # closed_prs.json/unmerged_prs.json returned OK under the narrow form.
    "private_key_block": re.compile(r"-----BEGIN (?:[A-Z0-9]+ )*PRIVATE KEY(?: BLOCK)?-----"),
    "google_api_key": re.compile(r"\bAIza[0-9A-Za-z_-]{35}\b"),
    "generic_secret_assignment": re.compile(
        r"""(?ix)
        ["']?\b(api[_-]?key|secret|token|password|passwd|pwd)\b["']?
        \s*[:=]\s*["']?[A-Za-z0-9_./+=:-]{24,}
        """
    ),
}

PUBLIC_EMBED_ALLOW_PATTERNS = {
    "google_api_key": (
        re.compile(r"https://www\.google\.com/maps/embed/v1/"),
        re.compile(r"https://maps\.googleapis\.com/maps/api/staticmap\?"),
    ),
    "generic_secret_assignment": (
        re.compile(r"https://starter1\.preservica\.com/Render/render/external\?"),
    ),
}


@dataclass(frozen=True)
class Finding:
    path: str
    line: int | None
    rule: str


# ── Content detection (path-independent) ──────────────────────────────────────
# A secret guard must detect secret MATERIAL, not folder names. Path rules above
# are a belt; these are the guard. They fire on the bytes regardless of filename,
# so renaming hostkeys->data.bin or dropping a key in an unlisted dir cannot
# evade them. Added 2026-07-02 after a path-only pass let an unarmored ADB key,
# Dropbox host keys, and Docker auth through.

# ASN.1/DER object-identifier bytes that appear inside a DER-encoded private key
# whether or not the file carries "-----BEGIN ... KEY-----" PEM armor. ADB's
# adbkey is base64(DER) with no armor, so header regexes never saw it.
_DER_KEY_MARKERS = (
    bytes.fromhex("2a864886f70d010101"),  # rsaEncryption (PKCS#1 / PKCS#8 RSA)
    bytes.fromhex("2a8648ce3d0201"),      # ecPublicKey (EC private keys)
    bytes.fromhex("2b6570"),              # Ed25519
    bytes.fromhex("2b6571"),              # Ed448
)
_BASE64_RUN_RE = re.compile(rb"[A-Za-z0-9+/]{100,}={0,2}")
_DOCKER_AUTH_RE = re.compile(rb'"auth"\s*:\s*"([A-Za-z0-9+/]{8,}={0,2})"')
KNOWN_NON_SECRET_FILE_SIGNATURES = (
    b"\x89PNG", b"\xff\xd8\xff", b"GIF8", b"%PDF", b"\x1f\x8b",
    b"PK\x03\x04", b"SQLite format 3\x00", b"\x00asm", b"ID3", b"OggS",
    b"wOFF", b"wOF2",
)
# Text formats are scanned for embedded secrets by the content rules above; the
# raw-binary-blob heuristic must skip them, or unicode/base64-heavy notes trip it
# (measured: 12 .md + 27 .json false-positives). This is defense-in-depth, not
# exclusion — a key pasted into a .md is still caught by the key/token detectors.
_TEXT_EXTENSIONS = frozenset(
    ".md .markdown .txt .json .jsonl .yaml .yml .toml .xml .html .htm .csv .tsv"
    " .js .mjs .ts .py .sh .rb .go .rs .java .kt .c .h .cpp .css .svg .rtf .tex"
    " .ipynb .log .cfg .ini .conf .properties .gitignore".split()
)


def _shannon_entropy(data: bytes) -> float:
    if not data:
        return 0.0
    counts = [0] * 256
    for byte in data:
        counts[byte] += 1
    total = len(data)
    return -sum((c / total) * math.log2(c / total) for c in counts if c)


def _looks_binary(data: bytes) -> bool:
    if b"\x00" in data:
        return True
    printable = sum(1 for b in data if 9 <= b <= 13 or 32 <= b <= 126)
    return bool(data) and printable / len(data) < 0.85


def content_secret_findings(path: str, data: bytes) -> list[Finding]:
    """Detect secret material by content — filename-independent."""
    findings: list[Finding] = []

    # 1. DER private key (armored OR unarmored base64) — decode long base64 runs
    #    and look for private-key OIDs in the DER.
    for match in _BASE64_RUN_RE.finditer(data):
        try:
            decoded = base64.b64decode(match.group(0), validate=True)
        except Exception:
            continue
        # PKCS#8 / EC / Ed carry a key OID; PKCS#1 RSAPrivateKey (what `adbkey`
        # and `openssl genrsa` emit, unarmored) has none, so match its DER prefix:
        # SEQUENCE(30 82 ..) INTEGER version 0 (02 01 00) INTEGER modulus (02 82 ..).
        is_pkcs1 = decoded[:4].startswith(b"\x30\x82") and decoded[4:9] == b"\x02\x01\x00\x02\x82"
        if decoded[:1] == b"\x30" and (is_pkcs1 or any(mk in decoded for mk in _DER_KEY_MARKERS)):
            findings.append(Finding(path=path, line=None, rule="der_private_key"))
            break

    # 2. Docker/containers-style base64 auth blob decoding to "user:secret".
    for match in _DOCKER_AUTH_RE.finditer(data):
        try:
            if b":" in base64.b64decode(match.group(1), validate=True):
                findings.append(Finding(path=path, line=None, rule="base64_auth_blob"))
                break
        except Exception:
            continue

    # 3. Small high-entropy RAW binary blob (host keys, raw key material). Can't
    #    be told from any small binary by content alone, so scope tightly: skip
    #    text extensions (scanned above) and known file signatures; require true
    #    binary (NUL byte present).
    ext = os.path.splitext(path)[1].lower()
    if (
        ext not in _TEXT_EXTENSIONS
        and 16 <= len(data) <= 4096
        and b"\x00" in data
        and not any(data.startswith(signature) for signature in KNOWN_NON_SECRET_FILE_SIGNATURES)
        and _shannon_entropy(data) >= 4.3
    ):
        findings.append(Finding(path=path, line=None, rule="high_entropy_binary"))

    return findings


def is_allowed_content_match(rule: str, line: str) -> bool:
    """Allow narrow generic placeholders without muting dedicated token rules."""
    if any(pattern.search(line) for pattern in PUBLIC_EMBED_ALLOW_PATTERNS.get(rule, ())):
        return True
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


def git_ref_file_bytes_for_paths(ref: str, paths: list[str]) -> dict[str, bytes]:
    if not paths:
        return {}

    process = subprocess.Popen(
        ["git", "cat-file", "--batch"],
        cwd=REPO_ROOT,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    request = b"".join(
        f"{ref}:{path}\n".encode("utf-8", errors="surrogateescape")
        for path in paths
    )
    stdout, stderr = process.communicate(request)
    if process.returncode != 0:
        message = stderr.decode("utf-8", errors="replace").strip()
        raise RuntimeError(message or "git cat-file failed")

    blobs: dict[str, bytes] = {}
    offset = 0
    for path in paths:
        header_end = stdout.find(b"\n", offset)
        if header_end < 0:
            break
        header = stdout[offset:header_end]
        offset = header_end + 1

        if header.endswith(b" missing"):
            continue

        parts = header.split()
        if len(parts) != 3:
            continue
        object_type = parts[1]
        try:
            size = int(parts[2])
        except ValueError:
            continue

        data = stdout[offset : offset + size]
        offset += size
        if stdout[offset : offset + 1] == b"\n":
            offset += 1

        if object_type == b"blob":
            blobs[path] = data

    return blobs


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


def findings_for_paths(paths: list[str], *, staged: bool, git_ref: str | None = None) -> list[Finding]:
    findings: list[Finding] = []
    ref_blobs = git_ref_file_bytes_for_paths(git_ref, paths) if git_ref is not None else {}
    for path in paths:
        # Path-based detection must NOT depend on reading the file: a secret is
        # named by its path regardless of whether the bytes are present or
        # decodable (binary key blobs, or a path removed from the worktree but
        # still in the commit). Only content scanning needs the data.
        findings.extend(path_findings(path))
        if staged:
            data = staged_file_bytes(path)
        elif git_ref is not None:
            data = ref_blobs.get(path)
        else:
            data = worktree_file_bytes(path)
        if data is None:
            continue
        findings.extend(content_findings(path, data))
        findings.extend(content_secret_findings(path, data))
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--staged", action="store_true", help="check staged files")
    parser.add_argument("--paths-from-stdin", action="store_true", help="check NUL-delimited changed paths from stdin")
    parser.add_argument("--git-ref", help="read file bytes from this Git ref when checking stdin paths")
    args = parser.parse_args()

    if args.staged and args.paths_from_stdin:
        parser.error("--staged and --paths-from-stdin are mutually exclusive")
    if args.git_ref and not args.paths_from_stdin:
        parser.error("--git-ref requires --paths-from-stdin")

    paths = stdin_paths() if args.paths_from_stdin else staged_paths()
    findings = findings_for_paths(paths, staged=args.staged, git_ref=args.git_ref)

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
