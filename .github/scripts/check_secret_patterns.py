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
    # (trusted-main/), while the content under test is the PRIMARY checkout —
    # which is exactly the run step's working directory: every policy workflow
    # invokes this script with cwd at the primary checkout and never sets a
    # working-directory override. Using the process cwd keeps the
    # trusted-validator split (trusted code, PR-head content) without deriving
    # any filesystem path from environment data — there is no tainted-path
    # flow left for a scanner to model, and no hard-coded runner path to break
    # on self-hosted runners or a repo rename. Local (pre-commit) runs fall
    # back to the script's own repository.
    if os.environ.get("GITHUB_ACTIONS") == "true":
        return Path.cwd()
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


# An assignment whose right-hand side is an UNQUOTED dotted identifier chain is
# code referring to code (`password → this.render_password_component`,
# `data.api_key ← provider.data.api_key`; arrows here, not `:`/`=`, so the
# generic rule on the CURRENT default branch cannot fire on this very comment
# while this file rides through review), never a secret VALUE — but only in a
# file whose format actually parses an unquoted RHS as an expression. The
# allowance is therefore PATH-GATED to expression-language sources (the
# JS/TS family, where every verified false positive lives); in YAML, JSON,
# Markdown, and every other format an unquoted dotted string is a data
# scalar, and no string-level fence can tell the two apart because YAML flow
# syntax mirrors JS object literals exactly (Copilot's third-round catch on
# #957: capital-and-underscore-bearing scalars defeat morphology alone).
# Within expression files, five fences keep real material caught:
# (1) a quoted RHS is a literal and never allowed here; (2) the chain must
# be followed by code punctuation — a call, separator, or closer — so a bare
# token dangling at end-of-line stays flagged; (3) a first segment starting
# with `eyJ` (base64 of `{"`, the prefix of every JWT header) is rejected
# outright, since JWT segments can otherwise satisfy the identifier grammar;
# (4) the chain must carry identifier MORPHOLOGY — at least one underscore,
# `$`, or capital letter — because long code references name things, and
# names carry word boundaries (camelCase, snake_case, or a `$`). Digits
# deliberately do NOT count as morphology — secrets are digit-rich, and `\w`
# already admits digits inside segments. Segments must each start with a
# letter/underscore, so base64 chunks with digits leading or -, +, /, =
# anywhere break the grammar. (5) the line PREFIX before the match must be
# plain code: any earlier quote, backtick, `//`, `/*`, or a leading `*`
# (JSDoc continuation) rejects the allowance, because the match may then sit
# inside comment or string TEXT, where a pasted credential is characters,
# not a code reference (Copilot's fourth-round catch on #957). The prefix
# check is deliberately parity-free and conservative — a CLOSED string
# earlier on the line also rejects, and noise is the correct direction for
# a secret gate to fail. Residual, documented: a line in the BODY of a
# multi-line template literal or block comment carries no marker of its own;
# closing that needs a real JS lexer, out of proportion for this guard.
_EXPRESSION_SOURCE_SUFFIXES = (".js", ".mjs", ".cjs", ".jsx", ".ts", ".tsx")
_JS_NONCODE_PREFIX = re.compile(r"""^\s*\*|["'`]|//|/\*""")


def _chain_allowance_applies(line: str, match: re.Match, path: str) -> bool:
    """True when this generic match is an identifier-chain code reference."""
    if not path.lower().endswith(_EXPRESSION_SOURCE_SUFFIXES):
        return False
    if _JS_NONCODE_PREFIX.search(line[: match.start()]):
        return False
    return bool(_UNQUOTED_IDENTIFIER_CHAIN_RHS.match(line, match.start()))


# The key is either BARE or a PAIRED-quoted object key (`"password":`) —
# independent optional quotes would let the OPENING quote of a plain string
# literal (`"password: …`) be absorbed into the match, hiding it from the
# prefix fence; requiring the close-quote before the separator is what
# separates a quoted key from string text.
_UNQUOTED_IDENTIFIER_CHAIN_RHS = re.compile(
    r"""(?ix)
    (?:
      (?P<q>["'])(?:api[_-]?key|secret|token|password|passwd|pwd)(?P=q)
      |
      \b(?:api[_-]?key|secret|token|password|passwd|pwd)\b
    )
    \s*[:=]\s*
    (?!["'])
    (?!eyJ)
    (?-i:(?=[\w$.]*[_$A-Z]))
    [A-Za-z_$][\w$]*(?:\.[A-Za-z_$][\w$]*)+
    (?![\w$./+=:-])
    \s*[,;()}\]]
    """
)


def is_allowed_content_match(
    rule: str, line: str, match: re.Match | None = None, path: str | None = None
) -> bool:
    """Allow narrow generic placeholders without muting dedicated token rules.

    Every allowance except the explicit inline directive is SPAN-TIED: it
    clears only the specific generic-assignment match it inspects, never the
    whole line. On a minified one-line bundle, a benign `password:
    this.component,` — or an innocent `process.env.NAME` reference — must not
    make a real `token="..."` elsewhere on the same line invisible; each match
    is judged where it stands. The identifier-chain shape is re-anchored at
    the match's own start (positional, on the full line: its trailing
    code-punctuation fence must see the character AFTER the generic match,
    which lies outside the match text) and applies only when `path` names an
    expression-language source file whose line prefix is plain code — see
    `_chain_allowance_applies`. The placeholder shapes are searched within
    the matched text itself (keyword, separator, and RHS), which is strictly
    narrower than the line scope they used to get, and are path-independent
    — they are placeholder conventions, not syntax. Only `secret-pattern:
    allow` stays line-scoped — it is a deliberate human directive, not a
    shape heuristic.
    """
    if rule != "generic_secret_assignment":
        return False
    if "secret-pattern: allow" in line:
        return True
    if match is not None and path is not None and _chain_allowance_applies(line, match, path):
        return True
    scope = match.group(0) if match is not None else line
    return bool(
        re.search(r"\bprocess\.env\.[A-Z0-9_]+\b", scope)
        or re.search(r"""(?i)["']?env:[A-Z][A-Z0-9_]*["']?""", scope)
        or re.search(r"""(?i)["']?\$secretRef(?::[A-Za-z0-9_.:/-]+)?["']?""", scope)
        or re.search(r"(?i)\breplace-with-[A-Za-z0-9_-]+\b", scope)
    )


def run_git(args: list[str]) -> subprocess.CompletedProcess[str]:
    try:
        # Safe: git is hardcoded string literal; args come from internal callers only
        return subprocess.run(
            ["git", *args],
            cwd=REPO_ROOT,
            text=True,
            encoding="utf-8",
            errors="replace",
            capture_output=True,
            check=False,
            timeout=30,
        )
    except subprocess.TimeoutExpired as exc:
        raise RuntimeError(f"git {args[0]} timed out after 30s") from exc
    except OSError as exc:
        raise RuntimeError(f"git {args[0]} could not run: {exc}") from exc


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
    try:
        # Safe: git is hardcoded; path from git tracking only, no user interpolation
        result = subprocess.run(
            ["git", "show", f":{path}"],
            cwd=REPO_ROOT,
            capture_output=True,
            check=False,
            timeout=30,
        )
    except subprocess.TimeoutExpired as exc:
        raise RuntimeError(f"git show timed out after 30s ({path})") from exc
    except OSError as exc:
        raise RuntimeError(f"git show could not run: {exc}") from exc
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
            # Judge every match on the line, not just the first: a line is
            # clean only if each match is individually allowed. One finding
            # per rule per line, as before.
            for match in pattern.finditer(line):
                if is_allowed_content_match(rule, line, match, path):
                    continue
                findings.append(Finding(path=path, line=line_number, rule=rule))
                break
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

    try:
        paths = stdin_paths() if args.paths_from_stdin else staged_paths()
        findings = findings_for_paths(paths, staged=args.staged)
    except RuntimeError as exc:
        print(f"secret-pattern guard: {exc}", file=sys.stderr)
        return 1

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
