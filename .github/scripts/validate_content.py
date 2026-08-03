#!/usr/bin/env python3
"""
Content Validation Gate
========================
Runs after content generation but before git commit in CI workflows.
Checks staged files for signs of injection, malformed frontmatter,
or unexpected content. Exits non-zero to halt the workflow on failure.

Usage:
  python3 validate_content.py [--scope bills|inbox|all]

Exit codes:
  0  All checks passed
  1  Validation failure (do NOT commit)
"""

import argparse
import re
import subprocess
import sys
from pathlib import Path

# ── Configuration ────────────────────────────────────────────────────────────

# Directories each scope is allowed to touch
SCOPE_ALLOWED_DIRS: dict[str, list[str]] = {
    "bills": [
        "GOVERNMENTS/IDAHO - LEGISLATIVE/BILLS/",
        "GOVERNMENTS/IDAHO - LEGISLATIVE/SESSIONS/",
        "GOVERNMENTS/IDAHO - LEGISLATIVE/IDAHO HOUSE/",
        "GOVERNMENTS/IDAHO - LEGISLATIVE/IDAHO SENATE/",
    ],
    "inbox": [
        "INBOX/",
    ],
    "all": [],  # no directory restriction
}

MAX_FILE_SIZE_BYTES = 50 * 1024  # 50 KB

# Patterns that should never appear in vault markdown
DANGEROUS_PATTERNS = [
    re.compile(r"<script", re.IGNORECASE),
    re.compile(r"javascript:", re.IGNORECASE),
    re.compile(r"on\w+=", re.IGNORECASE),  # onclick=, onerror=, etc.
    re.compile(r"<iframe", re.IGNORECASE),
    re.compile(r"<object", re.IGNORECASE),
    re.compile(r"<embed", re.IGNORECASE),
]

# Unrendered template placeholders must not persist in periodic notes or the
# carryforward list: they compound across rollover runs. These are the two
# delimiter families the vault's templates use, so they are what a failed
# expansion actually leaves behind -- Templater `<% ... %>` and core Obsidian
# Templates `{{...}}`. (This rule previously searched for [[YESTERDAY]] /
# [[TODAY]] / [[TOMORROW]], which no template emits, so it missed every real
# expansion failure while flagging hand-written wikilinks.)
TEMPLATER_PLACEHOLDER_RE = re.compile(r"<%")
BRACE_PLACEHOLDER_RE = re.compile(r"\{\{[^}\n]+\}\}")

# Periodic-note filenames, from the title formats in the five NOTE TEMPLATEs:
# day YYYY-MM-DD, week GGGG-[W]WW, month YYYY-MM, quarter YYYY-[Q]Q.
# Yearly (YYYY) is deliberately absent -- a bare four-digit name is not a
# reliable signal (`1000.md` exists at root and is not a year note), so yearly
# notes are picked up by their `period:` frontmatter key instead.
PERIODIC_NOTE_RE = re.compile(r"^\d{4}-(?:\d{2}-\d{2}|W\d{1,2}|Q[1-4]|\d{2})\.md$")
PERIOD_VALUES = {"day", "week", "month", "quarter", "year"}
# The templates themselves are written in this syntax and must never be flagged.
TEMPLATE_SUFFIX = " NOTE TEMPLATE.md"
CARRYFORWARD_FILE = "TO DO LIST.md"
FENCE_RE = re.compile(r"^\s*(```|~~~)")

# Sponsor names should be alphabetic with common punctuation
SPONSOR_NAME_RE = re.compile(r"^[A-Za-z\s.\-',()]+$")


# ── Helpers ──────────────────────────────────────────────────────────────────

def get_changed_files(base: str | None = None) -> list[Path]:
    """Get changed Markdown paths, including deletions."""
    command = ["git", "diff", "--name-only", "--diff-filter=ACMRD"]
    if base is None:
        command.insert(2, "--cached")
    else:
        command.append(f"{base}..HEAD")
    result = subprocess.run(
        command,
        capture_output=True, text=True
    )
    return [Path(f) for f in result.stdout.strip().splitlines() if f.endswith(".md")]


def parse_frontmatter(path: Path, content: str) -> tuple[dict | None, list[str]]:
    """Parse YAML frontmatter and return a mapping when present."""
    errors = []
    if not content.startswith("---"):
        return None, []  # no frontmatter to validate

    parts = content.split("---", 2)
    if len(parts) < 3:
        errors.append(f"{path}: Malformed frontmatter (missing closing ---)")
        return None, errors

    import yaml
    try:
        loaded = yaml.safe_load(parts[1])
    except yaml.YAMLError as e:
        errors.append(f"{path}: YAML frontmatter parse error: {e}")
        return None, errors

    if loaded is None:
        return {}, errors
    if not isinstance(loaded, dict):
        errors.append(f"{path}: YAML frontmatter must parse to a mapping")
        return None, errors
    return loaded, errors


def validate_content_safety(path: Path, content: str) -> list[str]:
    """Check for dangerous content patterns."""
    errors = []
    for pattern in DANGEROUS_PATTERNS:
        match = pattern.search(content)
        if match:
            errors.append(f"{path}: Dangerous pattern found: {match.group()!r}")
    return errors


def validate_file_size(path: Path) -> list[str]:
    """Check file is not abnormally large."""
    errors = []
    if path.exists() and path.stat().st_size > MAX_FILE_SIZE_BYTES:
        size_kb = path.stat().st_size / 1024
        errors.append(f"{path}: File too large ({size_kb:.1f} KB > {MAX_FILE_SIZE_BYTES // 1024} KB limit)")
    return errors


def is_periodic_surface(path: Path, frontmatter: dict | None) -> bool:
    """True for the surfaces a failed template expansion can propagate through:
    any periodic note (day/week/month/quarter/year) or the carryforward list.

    The five `* NOTE TEMPLATE.md` files are excluded and must stay excluded --
    they are written in the very syntax this check hunts for, so bringing them
    into scope would make the check fail on itself."""
    name = path.name
    if name.endswith(TEMPLATE_SUFFIX):
        return False
    if name == CARRYFORWARD_FILE or PERIODIC_NOTE_RE.match(name):
        return True
    if isinstance(frontmatter, dict):
        period = frontmatter.get("period")
        if isinstance(period, str) and period.strip().lower() in PERIOD_VALUES:
            return True
    return False


def validate_template_placeholders(
    path: Path, content: str, frontmatter: dict | None = None
) -> list[str]:
    """Scope-limited check: no unrendered template placeholders in periodic
    notes or TO DO LIST.md. Other files may legitimately show the syntax in
    prose or examples (VAULT-CONVENTIONS.md, agent instructions, the templates
    themselves), and fenced blocks are skipped for the same reason."""
    if not is_periodic_surface(path, frontmatter):
        return []
    errors = []
    in_fence = False
    for i, line in enumerate(content.splitlines(), 1):
        if FENCE_RE.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if TEMPLATER_PLACEHOLDER_RE.search(line):
            errors.append(
                f"{path}:{i}: unrendered Templater placeholder (<% ... %>)"
            )
        elif BRACE_PLACEHOLDER_RE.search(line):
            errors.append(
                f"{path}:{i}: unrendered template placeholder ({{{{...}}}})"
            )
    return errors


def validate_sponsor_names(path: Path, content: str) -> list[str]:
    """Check sponsor names in frontmatter look reasonable."""
    errors = []
    in_sponsors = False
    for line in content.splitlines():
        if line.strip() == "sponsor:":
            in_sponsors = True
            continue
        if in_sponsors:
            if line.startswith("  - "):
                name = line.strip().removeprefix("- ").strip('"').strip()
                # Remove wikilink wrapping for validation
                name = name.removeprefix("[[").removesuffix("]]")
                if name and not SPONSOR_NAME_RE.match(name):
                    errors.append(f"{path}: Suspicious sponsor name: {name!r}")
            else:
                in_sponsors = False
    return errors


def validate_directory(path: Path, scope: str) -> list[str]:
    """Check file is in an allowed directory for this scope."""
    allowed = SCOPE_ALLOWED_DIRS.get(scope, [])
    if not allowed:
        return []
    errors = []
    path_str = str(path).replace("\\", "/")
    if not any(path_str.startswith(d) for d in allowed):
        errors.append(f"{path}: File outside allowed directories for scope '{scope}': {allowed}")
    return errors


# ── Main ─────────────────────────────────────────────────────────────────────

def main() -> int:
    parser = argparse.ArgumentParser(description="Validate staged content before commit")
    parser.add_argument("--scope", choices=["bills", "inbox", "all"], default="all",
                        help="Which scope to validate (restricts allowed directories)")
    parser.add_argument("--base", help="Validate the committed diff from BASE through HEAD instead of staged files")
    args = parser.parse_args()

    staged = get_changed_files(args.base)
    if not staged:
        print("validate_content: No staged markdown files to check.")
        return 0

    all_errors: list[str] = []
    for path in staged:
        all_errors.extend(validate_directory(path, args.scope))
        all_errors.extend(validate_file_size(path))

        if not path.exists():
            continue

        content = path.read_text(encoding="utf-8", errors="replace")
        frontmatter, frontmatter_errors = parse_frontmatter(path, content)
        all_errors.extend(frontmatter_errors)
        all_errors.extend(validate_content_safety(path, content))
        all_errors.extend(validate_template_placeholders(path, content, frontmatter))
        all_errors.extend(validate_sponsor_names(path, content))

    if all_errors:
        print(f"validate_content: {len(all_errors)} error(s) found:", file=sys.stderr)
        for err in all_errors:
            print(f"  ERROR: {err}", file=sys.stderr)
        return 1

    print(f"validate_content: {len(staged)} file(s) passed all checks.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
