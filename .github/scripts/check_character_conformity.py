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
import subprocess  # nosec B404 -- see [tool.bandit] note in pyproject.toml
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


# --- layer 2: mojibake (double-decode artifacts) -----------------------------
#
# N4 ruling (Logan, 2026-07-08): bounded heuristics. In scope ONLY the closed
# family of double-decode artifacts — UTF-8 bytes once read as cp1252/latin-1
# and written back, leaving sequences like the cp1252 renderings of an
# em-dash's or e-acute's UTF-8 bytes as *valid UTF-8 text*. A repair is applied
# only where it round-trips: repaired.encode("utf-8").decode(charset) must
# reproduce the observed text exactly. Anything else is flagged, never touched.

# The closed garble families: charsets a UTF-8 byte stream has historically
# been misread through in this vault. cp1252/latin-1 (Windows text tools) and
# cp437/cp850 (DOS/PowerShell console) — each with its own artifact alphabet.
MOJIBAKE_FAMILIES = ("cp1252", "latin-1", "cp437", "cp850")


def _family_lead_re(codec: str) -> re.Pattern[str]:
    chars = []
    for b in range(0xC2, 0xF5):
        try:
            chars.append(re.escape(bytes([b]).decode(codec)))
        except UnicodeDecodeError:
            continue
    return re.compile("[" + "".join(chars) + "]")


_FAMILY_LEADS = {codec: _family_lead_re(codec) for codec in MOJIBAKE_FAMILIES}


def _family_bytes(segment: str, codec: str) -> bytes | None:
    try:
        return segment.encode(codec)
    except UnicodeEncodeError:
        return None


def _find_family_repairs(text: str, codec: str) -> list[tuple[int, int, str, str]]:
    """Provable double-decode repairs for one garble family."""
    repairs: list[tuple[int, int, str, str]] = []
    lead = _FAMILY_LEADS[codec]
    i = 0
    while i < len(text):
        match = lead.search(text, i)
        if not match:
            break
        start = match.start()
        end = start
        best: tuple[int, str] | None = None
        while end < len(text) and end - start < 64:
            end += 1
            raw = _family_bytes(text[start:end], codec)
            if raw is None:
                break
            try:
                candidate = raw.decode("utf-8")
            except UnicodeDecodeError as err:
                if err.reason == "unexpected end of data":
                    continue  # need more characters
                break
            if UTF8_MULTIBYTE.search(raw):
                best = (end, candidate)
        if best is None:
            i = match.start() + 1
            continue
        end, repaired = best
        observed = text[start:end]
        # Round-trip proof: the repair, re-garbled the same way, is the observation.
        if repaired.encode("utf-8").decode(codec, errors="strict") == observed:
            repairs.append((start, end, observed, repaired))
        i = end
    return repairs


def find_mojibake_repairs(text: str) -> list[tuple[int, int, str, str]]:
    """Return provable double-decode repairs as (start, end, observed, repaired).

    Families are tried in the precedence the adopted program document sets:
    cp1252/latin-1 are the *ruled* family ("UTF-8 read as cp1252/latin-1 and
    re-saved"); the DOS console pages are the secondary family and may only
    claim spans the ruled family cannot explain at all. Within that order, a
    lower-precedence claim overlapping an accepted higher-precedence span is
    discarded — precedence is textual (the ruling), not statistical guessing.
    """
    chosen: list[tuple[int, int, str, str]] = []
    claimed: list[tuple[int, int]] = []
    for codec in MOJIBAKE_FAMILIES:  # tuple order IS the precedence order
        for s, e, obs, rep in _find_family_repairs(text, codec):
            if any(s < ce and cs < e for cs, ce in claimed):
                continue  # territory already explained by a higher family
            chosen.append((s, e, obs, rep))
            claimed.append((s, e))
    chosen.sort()
    return chosen


def _apply_one_pass(text: str) -> tuple[str, int]:
    repairs = find_mojibake_repairs(text)
    if not repairs:
        return text, 0
    out: list[str] = []
    cursor = 0
    for start, end, _observed, repaired in repairs:
        out.append(text[cursor:start])
        out.append(repaired)
        cursor = end
    out.append(text[cursor:])
    return "".join(out), len(repairs)


# Generation bound for repeated garbling. Each pass strictly shrinks the text
# (every repair maps >=2 chars to fewer), so termination is guaranteed anyway;
# the bound only caps pathological synthetic input.
MAX_GARBLE_GENERATIONS = 10


def apply_mojibake_repairs(text: str) -> tuple[str, int]:
    """Apply provable repairs to a fixed point. Returns (text, total_spans).

    Multi-generation garble (text garbled, then the garbled text garbled
    again) peels one generation per pass; the tool is not finished until no
    provable artifact remains, so it repeats until stable.
    """
    total = 0
    count = 0
    for _ in range(MAX_GARBLE_GENERATIONS):
        text, count = _apply_one_pass(text)
        if count == 0:
            break
        total += count
    else:
        if count:
            # Never silent: the bound should be unreachable on real data.
            print(
                f"NORMALIZATION (warning): generation bound {MAX_GARBLE_GENERATIONS} "
                "exhausted with repairs still being found; input needs human eyes",
                file=sys.stderr,
            )
    return text, total


def run_mojibake_sweep(write: bool) -> int:
    root = repo_root()
    tracked = git_tracked_files()
    attrs = git_text_attrs(tracked)
    repaired_files = 0
    total = 0
    for path in tracked:
        target = contained_path(root, path)
        if target is None:
            continue
        try:
            data = target.read_bytes()
        except (FileNotFoundError, IsADirectoryError, PermissionError):
            continue
        if classify(attrs.get(path, {}), data) != "text":
            continue
        try:
            text = (data[len(UTF8_BOM):] if data.startswith(UTF8_BOM) else data).decode("utf-8")
        except UnicodeDecodeError:
            continue  # layer-1 territory; the encoding sweep owns it
        fixed, count = apply_mojibake_repairs(text)
        if count == 0:
            continue
        repaired_files += 1
        total += count
        if write:
            prefix = UTF8_BOM if data.startswith(UTF8_BOM) else b""
            target.write_bytes(prefix + fixed.encode("utf-8"))
        print(f"  [{'wrote' if write else 'would write'}] {path}: {count} double-decode span(s) repaired")
    mode = "applied" if write else "dry-run (pass --write to apply)"
    print(f"Mojibake sweep {mode}: {total} span(s) across {repaired_files} file(s), every repair round-trip-proven.")
    return 0


# --- layer 3: homoglyphs (adjudicated in the #638 review) ---------------------
#
# The rule as adjudicated: a look-alike letter from one script hiding INSIDE a
# word of another script is disorder and is normalized to the surrounding
# script. The vault is not English-only, so the rule is symmetric and touches
# nothing else: a genuinely Cyrillic (Greek, Japanese, ...) word never mixes
# scripts and is never touched; a word that is ENTIRELY confusable (its script
# undecidable) is flagged for human eyes, never guessed.

# Identical-glyph pairs, Cyrillic->Latin and Greek->Latin (lower/upper).
_CONFUSABLE_TO_LATIN = {
    # Cyrillic lowercase / uppercase
    "а": "a", "е": "e", "о": "o", "р": "p", "с": "c", "у": "y", "х": "x",
    "і": "i", "ѕ": "s", "ј": "j", "ԁ": "d", "ɡ": "g",
    "А": "A", "В": "B", "Е": "E", "З": "3", "К": "K", "М": "M", "Н": "H",
    "О": "O", "Р": "P", "С": "C", "Т": "T", "Х": "X", "Ѕ": "S", "І": "I", "Ј": "J",
    # Greek
    "ο": "o", "ν": "v", "Α": "A", "Β": "B", "Ε": "E", "Ζ": "Z", "Η": "H",
    "Ι": "I", "Κ": "K", "Μ": "M", "Ν": "N", "Ο": "O", "Ρ": "P", "Τ": "T",
    "Υ": "Y", "Χ": "X",
}
_CONFUSABLE_FROM_LATIN = {v: k for k, v in _CONFUSABLE_TO_LATIN.items() if v.isalpha()}

_WORD_RE = re.compile(r"[^\W\d_]+", re.UNICODE)


def _script(ch: str) -> str:
    cp = ord(ch)
    if cp < 0x250:
        return "latin"
    if 0x370 <= cp <= 0x3FF:
        return "greek"
    if 0x400 <= cp <= 0x4FF:
        return "cyrillic"
    return "other"


def find_homoglyph_repairs(text: str) -> tuple[list[tuple[int, str, str]], list[tuple[int, str]]]:
    """Return (repairs, flags) for mixed-script words.

    repairs: (offset, observed_word, repaired_word) where a minority of
    confusable letters is normalized to the word's dominant script.
    flags: (offset, word) where every letter is confusable — script
    undecidable, so it is reported, never repaired.
    """
    repairs: list[tuple[int, str, str]] = []
    flags: list[tuple[int, str]] = []
    for match in _WORD_RE.finditer(text):
        word = match.group()
        scripts = {_script(c) for c in word}
        if len(scripts) < 2 or "other" in scripts:
            continue  # single-script or beyond our table: never touched
        latinish = sum(1 for c in word if _script(c) == "latin")
        foreign = len(word) - latinish
        if latinish and foreign and all(
            (c in _CONFUSABLE_TO_LATIN) if _script(c) != "latin" else (c in _CONFUSABLE_FROM_LATIN)
            for c in word
        ) and (latinish == foreign):
            flags.append((match.start(), word))  # perfectly balanced + all-confusable: undecidable
            continue
        if latinish >= foreign:
            fixed = "".join(_CONFUSABLE_TO_LATIN.get(c, c) if _script(c) != "latin" else c for c in word)
        else:
            fixed = "".join(_CONFUSABLE_FROM_LATIN.get(c, c) if _script(c) == "latin" else c for c in word)
        if fixed != word and len({_script(c) for c in fixed}) == 1:
            repairs.append((match.start(), word, fixed))
        elif fixed != word:
            flags.append((match.start(), word))  # normalization did not yield one script: human eyes
        else:
            flags.append((match.start(), word))  # mixed but not confusable-mappable: human eyes
    return repairs, flags


def run_homoglyph_sweep(write: bool) -> int:
    root = repo_root()
    tracked = git_tracked_files()
    attrs = git_text_attrs(tracked)
    repaired_files = total = flagged = 0
    for path in tracked:
        target = contained_path(root, path)
        if target is None:
            continue
        try:
            data = target.read_bytes()
        except (FileNotFoundError, IsADirectoryError, PermissionError):
            continue
        if classify(attrs.get(path, {}), data) != "text":
            continue
        try:
            text = (data[len(UTF8_BOM):] if data.startswith(UTF8_BOM) else data).decode("utf-8")
        except UnicodeDecodeError:
            continue
        repairs, flags = find_homoglyph_repairs(text)
        # Table-cell guard (structural, not a file list): a mixed-script word
        # that is the ENTIRE content of a table cell is data in key position
        # (e.g. a correction dictionary mapping look-alike misspellings to
        # fixes; the look-alike IS the payload and "repairing" it destroys
        # the entry). Whole-cell occupants flag; words inside prose repair.
        kept_repairs = []
        for off, observed, fixed in repairs:
            line_start = text.rfind("\n", 0, off) + 1
            line_end = text.find("\n", off)
            line = text[line_start:line_end if line_end != -1 else len(text)]
            if re.search(r"\|\s*" + re.escape(observed) + r"\s*\|", line):
                flags.append((off, observed))
            else:
                kept_repairs.append((off, observed, fixed))
        repairs = kept_repairs
        for off, word in flags:
            flagged += 1
            print(f"  [FLAG] {path}@{off}: {word!r} mixed-script; correction-table key or undecidable; needs human eyes", file=sys.stderr)
        if not repairs:
            continue
        repaired_files += 1
        total += len(repairs)
        if write:
            out = text
            for off, observed, fixed in sorted(repairs, reverse=True):
                out = out[:off] + fixed + out[off + len(observed):]
            prefix = UTF8_BOM if data.startswith(UTF8_BOM) else b""
            target.write_bytes(prefix + out.encode("utf-8"))
        for _off, observed, fixed in repairs:
            print(f"  [{'wrote' if write else 'would write'}] {path}: {observed!r} -> {fixed!r}")
    mode = "applied" if write else "dry-run (pass --write to apply)"
    print(f"Homoglyph sweep {mode}: {total} word(s) across {repaired_files} file(s); {flagged} flagged for human eyes.")
    return 0


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
    parser.add_argument("--sweep-mojibake", action="store_true", help="layer-2 sweeper (double-decode artifacts, N4 bounds)")
    parser.add_argument("--sweep-homoglyphs", action="store_true", help="layer-3 sweeper (mixed-script look-alikes, #638 rule)")
    parser.add_argument("--write", action="store_true", help="apply sweep repairs (default: dry-run)")
    args = parser.parse_args()

    if args.sweep:
        return run_sweep(write=args.write)
    if args.sweep_mojibake:
        return run_mojibake_sweep(write=args.write)
    if args.sweep_homoglyphs:
        return run_homoglyph_sweep(write=args.write)

    requested = set(sys.stdin.read().splitlines()) - {""} if args.paths_from_stdin else set()
    tracked = git_tracked_files()
    # Taint boundary: stdin names only SELECT from git's tracked list — the
    # path strings that reach the filesystem are git's own output, never
    # stdin's. A fabricated or untracked stdin path selects nothing (deleted
    # files are already excluded upstream by --diff-filter=ACMRT).
    changed = [p for p in tracked if p in requested]
    attrs = git_text_attrs(tracked)

    root = repo_root()
    findings, _ = scan(changed, attrs, root)
    tree_findings, undeclared = scan([p for p in tracked if p not in requested], attrs, root)

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
