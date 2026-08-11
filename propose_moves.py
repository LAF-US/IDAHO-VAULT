#!/usr/bin/env python3
"""
IDAHO-VAULT Propose Moves
Reads the latest sort audit report and generates:
  1. A shell script of git mv commands (.github/proposed-moves.sh)
  2. A markdown summary for the PR body (.github/proposed-moves-summary.md)

Only proposes moves for high-confidence cases — does NOT act on orphan warnings,
which require human judgment.
"""

import os
import re
import glob
from datetime import datetime, timezone
from pathlib import Path

VAULT_ROOT = Path(".")
ADMIN_DIR = VAULT_ROOT / "!ADMINISTRATION"
GITHUB_DIR = VAULT_ROOT / ".github"

# Only auto-propose moves for these specific high-confidence reasons
HIGH_CONFIDENCE_REASONS = {
    "looks like an Idaho bill",
    "looks like a US state",
    "looks like an organization, not a topic",
}

# Reasons that require human judgment — never auto-propose
SKIP_REASONS = {
    "looks like an Idaho county",  # Could be out-of-state
}


def find_latest_audit() -> Path | None:
    reports = sorted(ADMIN_DIR.glob("sort-audit-*.md"), reverse=True)
    return reports[0] if reports else None


def parse_misplaced(report_path: Path) -> list[dict]:
    """Extract misplaced file entries from the audit report table."""
    content = report_path.read_text(encoding="utf-8")

    # Find the misplaced files table
    section = re.search(
        r"## Likely Misplaced Files.*?\n(.*?)(?=\n---|\Z)",
        content, re.DOTALL
    )
    if not section:
        return []

    rows = []
    for line in section.group(1).splitlines():
        # Match table rows: | `file` | `folder` | `suggested` | reason |
        m = re.match(r"\|\s*`([^`]+)`\s*\|\s*`([^`]+)`\s*\|\s*`([^`]+)`\s*\|\s*(.+?)\s*\|", line)
        if m:
            rows.append({
                "file": m.group(1),
                "current": m.group(2),
                "suggested": m.group(3),
                "reason": m.group(4).strip(),
            })
    return rows


def generate_mv_command(file_path: str, suggested_folder: str) -> str | None:
    """Generate a git mv command, or None if the destination already exists."""
    src = VAULT_ROOT / file_path
    filename = Path(file_path).name
    dst_folder = VAULT_ROOT / suggested_folder
    dst = dst_folder / filename

    if not src.exists():
        return None
    if dst.exists():
        return None  # Would overwrite

    return f'git mv "{file_path}" "{suggested_folder}/{filename}"'


def main():
    report = find_latest_audit()
    if not report:
        print("No audit report found. Run sort_audit.py first.")
        return

    print(f"Reading audit report: {report}")
    misplaced = parse_misplaced(report)

    if not misplaced:
        print("No misplaced files found in report.")
        return

    now = datetime.now(timezone.utc)
    date_str = now.strftime("%Y-%m-%d")

    proposed = []
    skipped = []

    for entry in misplaced:
        reason = entry["reason"]
        if reason in SKIP_REASONS:
            skipped.append(entry)
            continue
        if reason not in HIGH_CONFIDENCE_REASONS:
            skipped.append(entry)
            continue

        cmd = generate_mv_command(entry["file"], entry["suggested"])
        if cmd:
            proposed.append({"entry": entry, "cmd": cmd})
        else:
            skipped.append(entry)

    # Write shell script
    GITHUB_DIR.mkdir(exist_ok=True)
    sh_path = GITHUB_DIR / "proposed-moves.sh"

    if proposed:
        lines = [
            "#!/bin/bash",
            f"# Proposed vault moves — {date_str}",
            f"# Generated from {report.name}",
            f"# {len(proposed)} moves proposed",
            "# Review carefully before running.",
            "",
        ]
        for p in proposed:
            lines.append(f"# {p['entry']['reason']}")
            lines.append(p["cmd"])
            lines.append("")

        sh_path.write_text("\n".join(lines), encoding="utf-8")
        sh_path.chmod(0o755)
        print(f"Wrote {len(proposed)} proposed moves to {sh_path}")
    else:
        # Remove stale script if nothing to propose
        if sh_path.exists():
            sh_path.unlink()
        print("No high-confidence moves to propose.")
        return

    # Write PR summary
    summary_path = GITHUB_DIR / "proposed-moves-summary.md"
    summary_lines = [
        f"# Proposed Vault Moves — {date_str}",
        "",
        f"_Generated from `{report.name}`_",
        "",
        f"**{len(proposed)} moves proposed** | **{len(skipped)} items require human review**",
        "",
        "---",
        "",
        "## Proposed Moves",
        "",
        "These moves are high-confidence based on filename pattern matching. "
        "Review the diff before merging.",
        "",
        "| File | From | To | Reason |",
        "|---|---|---|---|",
    ]
    for p in proposed:
        e = p["entry"]
        summary_lines.append(
            f"| `{Path(e['file']).name}` | `{e['current']}` | `{e['suggested']}` | {e['reason']} |"
        )

    if skipped:
        summary_lines += [
            "",
            "---",
            "",
            "## Requires Human Review",
            "",
            "These were flagged in the audit but not proposed automatically.",
            "",
            "| File | Reason |",
            "|---|---|",
        ]
        for s in skipped:
            summary_lines.append(
                f"| `{Path(s['file']).name}` | {s['reason']} |"
            )

    summary_lines += [
        "",
        "---",
        "",
        "_All moves require human review and approval before merging._",
    ]

    summary_path.write_text("\n".join(summary_lines), encoding="utf-8")
    print(f"Wrote PR summary to {summary_path}")


if __name__ == "__main__":
    main()
