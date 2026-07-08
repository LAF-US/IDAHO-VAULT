#!/usr/bin/env python3
"""NORMALIZATION character-conformity guard (layer 1: encoding).

Norm (N1, ruled 2026-07-08): "BOM-aware UTF-8" — every tracked text file must
be valid UTF-8; a single leading byte-order mark is recognized as a BOM (not
content, not an offense) and the apparatus never adds one. Program document:
NORMALIZATION-CHARACTER-CONFORMITY-2026-07-07.md; tracking issue #794.

Text/binary discrimination is part of the contract, never guessed:
  gate 1 — a file whose .gitattributes `text` attribute is unset (`-text`) or
           that runs through an LFS filter is binary: skipped;
  gate 2 — a file is declared text only if its `text` attribute is set (the
           explicit extension list lives in .gitattributes, the single source
           of truth — no second hand-updated list here); anything unspecified
           is undeclared: skipped, but counted so the gap stays visible;
  gate 3 — a declared-text file containing a NUL byte in its first 8 KiB is
           AMBIGUOUS: flagged for a human, never silently reclassified.

Follows the NETWEB checker pattern (check_portable_paths.py): violations in a
PR's changed files FAIL; pre-existing tree debt is REPORT-ONLY so unrelated
PRs are never blocked by inherited disorder, and there is no grandfathering
list — the debt is printed, not hidden.

--sweep mode is the layer-1 sweeper for that debt: whole-file cp1252 → UTF-8
re-encode, applied only when the file contains no valid multibyte UTF-8
sequence (a mixed file gets flagged for a human, never guessed at) and only
when the decoded text re-encodes byte-identically to the original (the
round-trip proof). Dry-run by default; --write applies.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

NUL_PROBE_BYTES = 8 * 1024
UTF8_BOM = b"\xef\xbb\xbf"
UTF16_BOMS = {b"\xff\xfe": "UTF-16LE", b"\xfe\xff": "UTF-16BE"}
# Any well-formed UTF-8 multibyte sequence. Presence alongside invalid bytes
# means the file is mixed-encoding: whole-file cp1252 decode would mojibake
# the healthy sequences, so the sweeper must refuse.
UTF8_MULTIBYTE = re.compile(
    rb"(?:[\xC2-\xDF][\x80-\xBF]"
    rb"|[\xE0-\xEF][\x80-\xBF]{2}"
    rb"|[\xF0-\xF4][\x80-\xBF]{3})"
)


@dataclass
class Finding:
    path: str
    kind: str  # "encoding" | "ambiguous"
    detail: str

    def __str__(self) -> str:
        label = "AMBIGUOUS" if self.kind == "ambiguous" else "NOT VALID UTF-8"
        return f"{label}: {self.path} ({self.detail})"


def repo_root() -> Path:
    result = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        check=True,
        capture_output=True,
        text=True,
    )
    return Path(result.stdout.strip()).resolve()


def contained_path(root: Path, path: str) -> Path | None:
    """Resolve a candidate path and require it to live inside the repo root.

    Paths arrive on stdin (CI feeds `git diff --name-only`, which is always
    repo-relative), but the containment check is enforced here rather than
    assumed: anything resolving outside the root — traversal, absolute paths,
    symlinks pointing out — is refused, never read or written.
    """
    candidate = (root / path).resolve()
    if candidate == root or not candidate.is_relative_to(root):
        return None
    return candidate


def git_tracked_files() -> list[str]:
    result = subprocess.run(
        ["git", "-c", "core.quotePath=false", "ls-tree", "-r", "HEAD", "--name-only"],
        check=True,
        capture_output=True,
        text=True,
    )
    return [line for line in result.stdout.splitlines() if line]


def git_text_attrs(paths: list[str]) -> dict[str, dict[str, str]]:
    """Return {path: {"text": value, "filter": value}} via git check-attr.

    Values are git's own words: "set", "unset", "unspecified", or the
    attribute's string value (e.g. filter = "lfs").
    """
    if not paths:
        return {}
    payload = "\0".join(paths).encode() + b"\0"
    result = subprocess.run(
        ["git", "-c", "core.quotePath=false", "check-attr", "--stdin", "-z", "text", "filter"],
        input=payload,
        check=True,
        capture_output=True,
    )
    attrs: dict[str, dict[str, str]] = {}
    fields = result.stdout.decode().split("\0")
    # -z output is flat triples: path, attribute, value, path, attribute, value…
    for i in range(0, len(fields) - 2, 3):
        path, attribute, value = fields[i], fields[i + 1], fields[i + 2]
        attrs.setdefault(path, {})[attribute] = value
    return attrs


def classify(attrs: dict[str, str], head: bytes) -> str:
    """Apply the three gates: -> "binary" | "undeclared" | "ambiguous" | "text"."""
    if attrs.get("filter") == "lfs" or attrs.get("text") == "unset":
        return "binary"
    if attrs.get("text") != "set":
        return "undeclared"
    # A UTF-16 BOM is a charset declaration, not ambiguity: the file is text
    # in the wrong encoding (layer 1), despite the NUL bytes UTF-16 implies.
    if head[:2] in UTF16_BOMS:
        return "text"
    if b"\x00" in head[:NUL_PROBE_BYTES]:
        return "ambiguous"
    return "text"


def encoding_findings(path: str, data: bytes) -> list[Finding]:
    """Layer-1 conformity for one declared-text file (BOM-aware UTF-8)."""
    if data[:2] in UTF16_BOMS:
        return [
            Finding(
                path,
                "encoding",
                f"{UTF16_BOMS[data[:2]]} BOM where the declared encoding is BOM-aware UTF-8",
            )
        ]
    body = data[len(UTF8_BOM):] if data.startswith(UTF8_BOM) else data
    try:
        body.decode("utf-8")
        return []
    except UnicodeDecodeError as err:
        bad = body[err.start:err.end]
        gloss = bad.decode("cp1252", errors="replace")
        return [
            Finding(
                path,
                "encoding",
                f"byte {bad.hex()} at offset {err.start} is not UTF-8; "
                f"as cp1252 it would read {gloss!r}",
            )
        ]


def scan(
    paths: list[str], attrs: dict[str, dict[str, str]], root: Path
) -> tuple[list[Finding], int]:
    """Check paths; returns (findings, undeclared_count). Missing files skip."""
    findings: list[Finding] = []
    undeclared = 0
    for path in paths:
        target = contained_path(root, path)
        if target is None:
            print(f"  [refused] path escapes repository root, not read: {path}", file=sys.stderr)
            continue
        try:
            data = target.read_bytes()
        except (FileNotFoundError, IsADirectoryError, PermissionError):
            continue
        kind = classify(attrs.get(path, {}), data)
        if kind == "binary":
            continue
        if kind == "undeclared":
            undeclared += 1
            continue
        if kind == "ambiguous":
            findings.append(
                Finding(path, "ambiguous", "declared text by .gitattributes but contains NUL bytes")
            )
            continue
        findings.extend(encoding_findings(path, data))
    return findings, undeclared


# --- sweeper (layer 1 only) -------------------------------------------------

@dataclass
class SweepResult:
    path: str
    action: str  # "reencoded" | "skipped-clean" | "refused-mixed" | "refused-undecodable" | "refused-roundtrip"
    detail: str = ""


def sweep_file(path: str, data: bytes) -> tuple[SweepResult, bytes | None]:
    """Plan the layer-1 repair for one file. Returns (result, new_bytes|None)."""
    if data[:2] in UTF16_BOMS:
        # The BOM declares the charset; decode strictly and prove the round
        # trip (BOM + same-endianness re-encode reproduces the original bytes).
        codec = "utf-16-le" if data[:2] == b"\xff\xfe" else "utf-16-be"
        try:
            decoded = data[2:].decode(codec)
        except UnicodeDecodeError as err:
            return (
                SweepResult(path, "refused-undecodable", f"{UTF16_BOMS[data[:2]]} BOM but strict decode fails at offset {err.start}; needs human eyes"),
                None,
            )
        if data[:2] + decoded.encode(codec) != data:
            return (
                SweepResult(path, "refused-roundtrip", f"{UTF16_BOMS[data[:2]]} round-trip proof failed; needs human eyes"),
                None,
            )
        new = decoded.encode("utf-8")  # no BOM: tolerated on read, never added
        return SweepResult(path, "reencoded", f"{UTF16_BOMS[data[:2]]} → UTF-8"), new
    body = data[len(UTF8_BOM):] if data.startswith(UTF8_BOM) else data
    try:
        body.decode("utf-8")
        return SweepResult(path, "skipped-clean"), None
    except UnicodeDecodeError:
        pass
    if UTF8_MULTIBYTE.search(data):
        return (
            SweepResult(path, "refused-mixed", "contains valid UTF-8 multibyte sequences alongside invalid bytes; needs human eyes"),
            None,
        )
    try:
        decoded = data.decode("cp1252")
    except UnicodeDecodeError as err:
        return (
            SweepResult(path, "refused-undecodable", f"byte at offset {err.start} undefined in cp1252; needs human eyes"),
            None,
        )
    if decoded.encode("cp1252") != data:
        return (
            SweepResult(path, "refused-roundtrip", "cp1252 round-trip proof failed; needs human eyes"),
            None,
        )
    new = decoded.encode("utf-8")
    changed = sum(1 for b in data if b >= 0x80)
    return SweepResult(path, "reencoded", f"{changed} non-ASCII byte(s) re-encoded cp1252→UTF-8"), new


def run_sweep(write: bool) -> int:
    root = repo_root()
    tracked = git_tracked_files()
    attrs = git_text_attrs(tracked)
    repaired = refused = 0
    for path in tracked:
        target = contained_path(root, path)
        if target is None:
            print(f"  [refused] path escapes repository root, not touched: {path}", file=sys.stderr)
            continue
        try:
            data = target.read_bytes()
        except (FileNotFoundError, IsADirectoryError, PermissionError):
            continue
        if classify(attrs.get(path, {}), data) != "text":
            continue
        result, new = sweep_file(path, data)
        if result.action == "skipped-clean":
            continue
        if result.action == "reencoded":
            repaired += 1
            if write and new is not None:
                target.write_bytes(new)
            print(f"  [{'wrote' if write else 'would write'}] {path}: {result.detail}")
        else:
            refused += 1
            print(f"  [REFUSED] {path}: {result.detail}", file=sys.stderr)
    mode = "applied" if write else "dry-run (pass --write to apply)"
    print(f"Sweep {mode}: {repaired} file(s) re-encoded, {refused} refused for human review.")
    return 1 if refused else 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--paths-from-stdin", action="store_true")
    parser.add_argument("--sweep", action="store_true", help="layer-1 sweeper over the tracked tree")
    parser.add_argument("--write", action="store_true", help="apply sweep repairs (default: dry-run)")
    args = parser.parse_args()

    if args.sweep:
        return run_sweep(write=args.write)

    changed = [line for line in sys.stdin.read().splitlines() if line] if args.paths_from_stdin else []
    tracked = git_tracked_files()
    attrs = git_text_attrs(sorted(set(tracked) | set(changed)))

    root = repo_root()
    changed_set = set(changed)
    findings, _ = scan(changed, attrs, root)
    tree_findings, undeclared = scan([p for p in tracked if p not in changed_set], attrs, root)

    # Whole-tree pass is REPORT-ONLY: pre-existing offenders are visible debt,
    # not this PR's fault. No grandfathering list — the debt prints every run.
    if tree_findings:
        print(
            f"NORMALIZATION (report-only): {len(tree_findings)} pre-existing tracked-file "
            "violation(s) — not failing this PR; the layer-1 sweep owns this debt:",
            file=sys.stderr,
        )
        for finding in tree_findings:
            print(f"  [warn] {finding}", file=sys.stderr)
    if undeclared:
        print(
            f"NORMALIZATION (info): {undeclared} tracked file(s) have no text/binary "
            "declaration in .gitattributes and were skipped, not judged.",
            file=sys.stderr,
        )

    if findings:
        print("NORMALIZATION: character-conformity violations in changed files", file=sys.stderr)
        for finding in findings:
            print(f"  {finding}", file=sys.stderr)
        return 1

    print("All changed declared-text files conform (BOM-aware UTF-8).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
