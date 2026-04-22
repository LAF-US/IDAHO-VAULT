#!/usr/bin/env python3
"""
tidy_daily_notes.py — one-off frontmatter normalization for IDAHO-VAULT daily notes.

Actions:
  - Standardizes frontmatter to match DAILY NOTE TEMPLATE.md
  - Removes non-standard fields: cmte, today, sunrise, sunset
  - Normalizes weekday to list format
  - Ensures tags: today, YYYY/MM/DD, dailynote (plus any preserved extras)
  - Resolves the git merge conflict in 2026-03-24.md
  - Merges most-complete duplicate content for 2026-03-19 and 2026-03-20
  - Deletes 8 stale conflict/duplicate files

Usage:
    python3 .github/scripts/tidy_daily_notes.py [--dry-run]
"""

import argparse
import re
import sys
from datetime import date, timedelta
from pathlib import Path

VAULT_ROOT = Path(__file__).resolve().parents[2]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _ordinal(n: int) -> str:
    if 11 <= (n % 100) <= 13:
        return f"{n}th"
    return f"{n}{['th', 'st', 'nd', 'rd', 'th'][min(n % 10, 4)]}"


def fmt_ts(d: date, time_str: str = "12:00:00 pm") -> str:
    return f"{d.strftime('%A')}, {d.strftime('%B')} {_ordinal(d.day)} {d.year}, {time_str}"


def get_body(content: str) -> str:
    """Return body text (everything after closing frontmatter ---), always starting with \\n."""
    if not content.startswith('---'):
        return '\n\n' + content.lstrip()
    m = re.search(r'\n---\n', content[3:])
    if not m:
        return '\n\n' + content.lstrip()
    end = 3 + m.end()
    body = content[end:]
    if not body.startswith('\n'):
        body = '\n' + body
    return body


def log(message: str = "") -> None:
    """Write stdout safely on terminals that cannot encode all Unicode glyphs."""
    text = f"{message}\n"
    encoding = sys.stdout.encoding or "utf-8"
    if hasattr(sys.stdout, "buffer"):
        sys.stdout.buffer.write(text.encode(encoding, errors="backslashreplace"))
        sys.stdout.buffer.flush()
    else:
        sys.stdout.write(text)


def build_fm(d: date, created: str, modified: str, extra_tags: list | None = None) -> str:
    yesterday = d - timedelta(days=1)
    tomorrow = d + timedelta(days=1)
    weekday = d.strftime("%A")
    tag_date = d.strftime("%Y/%m/%d")

    tags = ['today', tag_date, 'dailynote']
    if extra_tags:
        tags += [t for t in extra_tags if t not in tags]

    tag_lines = '\n'.join(f'  - {t}' for t in tags)

    return (
        f"---\n"
        f"title: {d}\n"
        f"aliases:\n"
        f"  - {d}\n"
        f"linter-yaml-title-alias: {d}\n"
        f"yesterday: {yesterday}\n"
        f"tomorrow: {tomorrow}\n"
        f"weekday:\n"
        f"  - {weekday}\n"
        f"tags:\n"
        f"{tag_lines}\n"
        f"date created: {created}\n"
        f"date modified: {modified}\n"
        f"---"
    )


# ---------------------------------------------------------------------------
# Per-date configuration
# ---------------------------------------------------------------------------

# Preserved date created/modified from existing notes where known
NOTES = {
    date(2026, 3, 12): {
        'created':  fmt_ts(date(2026, 3, 12), "8:00:00 am"),
        'modified': fmt_ts(date(2026, 3, 12), "8:00:00 am"),
        'extra_tags': ['bills'],
    },
    date(2026, 3, 15): {
        'created':  fmt_ts(date(2026, 3, 15)),
        'modified': fmt_ts(date(2026, 3, 15)),
    },
    date(2026, 3, 16): {
        'created':  fmt_ts(date(2026, 3, 16)),
        'modified': fmt_ts(date(2026, 3, 16)),
    },
    date(2026, 3, 17): {
        'created':  fmt_ts(date(2026, 3, 17)),
        'modified': fmt_ts(date(2026, 3, 17)),
        'extra_tags': ['bills'],
    },
    date(2026, 3, 18): {
        'created':  fmt_ts(date(2026, 3, 18)),
        'modified': fmt_ts(date(2026, 3, 18)),
        'extra_tags': ['bills', 'budgets'],
    },
    date(2026, 3, 19): {
        'created':  fmt_ts(date(2026, 3, 19)),
        'modified': fmt_ts(date(2026, 3, 19)),
        'body_source': '2026-03-19 2.md',  # most complete: has YouTube/Publish + Spotify done
    },
    date(2026, 3, 20): {
        'created':  fmt_ts(date(2026, 3, 20)),
        'modified': fmt_ts(date(2026, 3, 20)),
        'body_source': '2026-03-20 2.md',  # canonical was empty; 2.md has all tasks resolved
    },
    date(2026, 3, 21): {
        'created':  fmt_ts(date(2026, 3, 21)),
        'modified': fmt_ts(date(2026, 3, 21)),
    },
    date(2026, 3, 22): {
        'created':  fmt_ts(date(2026, 3, 22)),
        'modified': fmt_ts(date(2026, 3, 22)),
    },
    date(2026, 3, 23): {
        'created':  "Monday, March 23rd 2026, 4:54:51 pm",
        'modified': "Friday, March 27th 2026, 11:34:34 am",
    },
    # 2026-03-24: merge conflict resolved manually below
    date(2026, 3, 24): {
        'created':  "Tuesday, March 24th 2026, 1:41:37 am",
        'modified': "Friday, March 27th 2026, 11:34:37 am",
        'body': (
            "\n"
            "[[TO DO LIST]]\n"
            "- [x] Senator Okuniewicz for panel\n"
            "- [ ] Data Center PKG elements\n"
            "\t- [ ] Lock voices\n"
            "\t- [ ] Get footage\n"
            "- [x] J Crane / social media podcast\n"
            "\t- [x] Create questions doc\n"
            "\t- [x] Review this year's bill\n"
            "- [ ] IDEX Artifacts triage state\n"
            "\t- [ ] Narrative segments\n"
            "\t- [ ] Assets census\n"
            "- [x] Update pharmacy to mail\n"
        ),
    },
    date(2026, 3, 25): {
        'created':  "Tuesday, March 24th 2026, 4:27:22 pm",
        'modified': "Friday, March 27th 2026, 11:34:35 am",
    },
    date(2026, 3, 26): {
        'created':  "Friday, March 27th 2026, 10:10:22 am",
        'modified': "Friday, March 27th 2026, 11:34:32 am",
    },
}

STALE = [
    "2026-03-19 (Conflicted copy LAPTOP-IdahoPTV 202603211454).md",
    "2026-03-19 1 1.md",
    "2026-03-19 1.md",
    "2026-03-19 2.md",
    "2026-03-20 1.md",
    "2026-03-20 2.md",
    "2026-03-24 (Conflicted copy Laptop (IdahoPTV) 202603251054).md",
    "2026-03-25 (Conflicted copy Laptop (IdahoPTV) 202603251054).md",
]


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description="Tidy IDAHO-VAULT daily note frontmatter")
    parser.add_argument('--dry-run', action='store_true', help="Print without writing")
    args = parser.parse_args()

    print("=== DAILY NOTE TIDY ===\n")
    divider = "-" * 60

    for d, cfg in sorted(NOTES.items()):
        f = VAULT_ROOT / f"{d}.md"
        if not f.exists():
            print(f"MISSING: {f.name} — skipping")
            continue

        # Determine body
        if 'body' in cfg:
            body = cfg['body']
        elif 'body_source' in cfg:
            src = VAULT_ROOT / cfg['body_source']
            body = (
                get_body(src.read_text(encoding="utf-8"))
                if src.exists()
                else get_body(f.read_text(encoding="utf-8"))
            )
        else:
            body = get_body(f.read_text(encoding="utf-8"))

        fm = build_fm(d, cfg['created'], cfg['modified'], cfg.get('extra_tags'))
        new_content = fm + body

        if args.dry_run:
            print(divider)
            print(f"  {f.name}")
            print(divider)
            log(new_content.rstrip("\n"))
            print()
        else:
            f.write_text(new_content, encoding="utf-8")
            print(f"  OK: {f.name}")

    print(f"\n=== STALE FILE CLEANUP ===\n")
    for name in STALE:
        p = VAULT_ROOT / name
        if args.dry_run:
            status = "exists - would delete" if p.exists() else "already gone"
            print(f"  {name}: {status}")
        else:
            if p.exists():
                p.unlink()
                print(f"  OK deleted: {name}")
            else:
                print(f"  already gone: {name}")


if __name__ == "__main__":
    main()
