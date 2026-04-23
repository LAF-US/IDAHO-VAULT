#!/usr/bin/env python3
"""
Content Validation Gate
========================
Runs after content generation but before git commit in CI workflows.
Checks staged files for signs of injection, malformed frontmatter,
or unexpected content. Exits non-zero to halt the workflow on failure.

Usage:
  python3 validate_content.py [--scope bills|admin|all]

Exit codes:
  0  All checks passed
  1  Validation failure (do NOT commit)
"""

import argparse
import re
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
    "admin": [
        "!/",
    ],
    "generated": [
        "!/",
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

# Unresolved date-placeholder tokens must not persist in daily notes or the
# carryforward list. They compound across rollover runs (see PR for context).
DATE_PLACEHOLDER_RE = re.compile(r"\[\[(YESTERDAY|TOMORROW|TODAY)\]\]")
DAILY_NOTE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}\.md$")

# Sponsor names should be alphabetic with common punctuation
SPONSOR_NAME_RE = re.compile(r"^[A-Za-z\s.\-',()]+$")
ROOT_GOVERNED_FILES = {
    "AGENTS.md",
    "CONSTITUTION.md",
    "DECISIONS.md",
    "README.md",
    "VAULT-CONVENTIONS.md",
    "VAULT-METADATA-STANDARD.md",
    "VAULT-TEMPLATES.md",
}
REQUIRED_GOVERNED_FIELDS = ("title", "updated", "status", "authority")


# ── Helpers ──────────────────────────────────────────────────────────────────

def get_staged_files() -> list[Path]:
    """Get list of staged files from git."""
    import subprocess
    result = subprocess.run(
        ["git", "diff", "--cached", "--name-only", "--diff-filter=ACMR"],
        capture_output=True, text=True
    )
    return [Path(f) for f in result.stdout.strip().splitlines() if f.endswith(".md")]


def validate_frontmatter(path: Path, content: str) -> list[str]:
    """Check that YAML frontmatter parses cleanly."""
    _, errors = parse_frontmatter(path, content)
    return errors


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


def validate_date_placeholders(path: Path, content: str) -> list[str]:
    """Scope-limited check: no [[YESTERDAY]]/[[TOMORROW]]/[[TODAY]] in daily
    notes or TO DO LIST.md. Other files may legitimately mention the tokens
    in prose (VAULT-CONVENTIONS.md, agent instructions, etc.)."""
    name = path.name
    if not (DAILY_NOTE_RE.match(name) or name == "TO DO LIST.md"):
        return []
    errors = []
    for i, line in enumerate(content.splitlines(), 1):
        if DATE_PLACEHOLDER_RE.search(line):
            errors.append(f"{path}:{i}: unresolved date placeholder token")
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
    path_str = str(path)
    if not any(path_str.startswith(d) for d in allowed):
        errors.append(f"{path}: File outside allowed directories for scope '{scope}': {allowed}")
    return errors


def is_governed_note(path: Path, scope: str) -> bool:
    """Limit schema enforcement to the currently governed automation lane."""
    path_str = str(path).replace("\\", "/")
    if DAILY_NOTE_RE.match(path.name) or path.name == "TO DO LIST.md":
        return False
    if path.name in ROOT_GOVERNED_FILES:
        return True
    return scope in {"admin", "generated"} and path_str.startswith("!/")


def validate_governed_metadata(path: Path, frontmatter: dict | None, scope: str) -> list[str]:
    """Require doctrinal baseline fields for governed notes."""
    if not is_governed_note(path, scope):
        return []
    if frontmatter is None:
        return [f"{path}: Governed note missing YAML frontmatter"]

    missing = [field for field in REQUIRED_GOVERNED_FIELDS if not frontmatter.get(field)]
    if not missing:
        return []
    return [f"{path}: Governed note missing required frontmatter field(s): {', '.join(missing)}"]


# ── Main ─────────────────────────────────────────────────────────────────────

def main() -> int:
    parser = argparse.ArgumentParser(description="Validate staged content before commit")
    parser.add_argument("--scope", choices=["bills", "admin", "generated", "all"], default="all",
                        help="Which scope to validate (restricts allowed directories)")
    args = parser.parse_args()

    staged = get_staged_files()
    if not staged:
        print("validate_content: No staged markdown files to check.")
        return 0

    all_errors: list[str] = []
    for path in staged:
        all_errors.extend(validate_directory(path, args.scope))
        all_errors.extend(validate_file_size(path))

        if path.exists():
            content = path.read_text(encoding="utf-8", errors="replace")
            frontmatter, frontmatter_errors = parse_frontmatter(path, content)
            all_errors.extend(frontmatter_errors)
            all_errors.extend(validate_governed_metadata(path, frontmatter, args.scope))
            all_errors.extend(validate_content_safety(path, content))
            all_errors.extend(validate_date_placeholders(path, content))
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
