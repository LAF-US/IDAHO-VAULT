#!/usr/bin/env python3
"""Submit newly added source URLs to the Wayback Machine (Save Page Now).

Push-triggered sibling of ``wayback_audit.py``. Given the list of ``.md`` files
changed in a push, it pulls each note's ``URL:`` field, submits the live ones to
Save Page Now, and writes a preservation log under ``!/``.

The ``URL:`` field parsing and the SPN submission are imported from
``wayback_audit`` so both wayback lanes share one definition instead of the
inline-bash reimplementation this replaces (#601 item 3 — bash/script dedup).
Reusing ``wayback_audit.extract_url`` also adopts its stricter filtering
(archive hosts and ``null``/``n/a`` placeholders are skipped).
"""

from __future__ import annotations

import argparse
import time
from datetime import datetime, timezone
from pathlib import Path

from wayback_audit import extract_url, save_page_now

RATE_SAVE = 5.0  # Save Page Now is rate-limited; match wayback_audit's spacing.
ADMIN_DIR = Path("!")


def read_changed_files(list_file: Path) -> list[str]:
    """Read a newline-separated list of changed paths (the git-diff output the
    workflow hands us). A missing file means "nothing changed" — return []."""
    if not list_file.exists():
        return []
    return [line.strip() for line in list_file.read_text().splitlines() if line.strip()]


def collect_urls(changed_files: list[str]) -> list[tuple[Path, str]]:
    """First ``URL:`` of each changed, existing ``.md`` file. Order-preserving,
    one URL per note — matching the inline block this replaces. Archive-host and
    placeholder URLs are filtered by ``extract_url``."""
    found: list[tuple[Path, str]] = []
    for name in changed_files:
        path = Path(name)
        if path.suffix != ".md" or not path.exists():
            continue
        url = extract_url(path.read_text(errors="replace"))
        if url:
            found.append((path, url))
    return found


def preserve(urls: list[tuple[Path, str]]) -> list[tuple[str, str | None, bool]]:
    """Submit each URL to Save Page Now, spacing requests for the rate limit."""
    results: list[tuple[str, str | None, bool]] = []
    for _, url in urls:
        archived = save_page_now(url)
        ok = archived is not None
        print(f"  {'OK ' if ok else 'ERR'} {url[:70]}")
        if archived:
            print(f"       -> {archived}")
        results.append((url, archived, ok))
        time.sleep(RATE_SAVE)
    return results


def write_log(results: list[tuple[str, str | None, bool]], date_str: str) -> Path:
    """Append the run's results to the day's preservation log under ``!/`` (the
    workflow commits it on diff). The filename is date-only, so a second push on
    the same UTC day must *extend* the existing table rather than overwrite it —
    otherwise the earlier run's preservation record is lost from the tree."""
    ADMIN_DIR.mkdir(exist_ok=True)
    log_path = ADMIN_DIR / f"wayback-preserve-{date_str}.md"
    if log_path.exists():
        lines = log_path.read_text(encoding="utf-8").splitlines()
    else:
        lines = [
            f"# Wayback Preservation Log — {date_str}",
            "",
            "URLs submitted to Save Page Now on push to main.",
            "",
            "| URL | Archived | Status |",
            "|---|---|---|",
        ]
    for url, archived, ok in results:
        status = "✅" if ok else "❌"
        arc = f"[snapshot]({archived})" if archived else "failed"
        lines.append(f"| {url[:70]} | {arc} | {status} |")
    log_path.write_text("\n".join(lines), encoding="utf-8")
    return log_path


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Preserve new vault URLs via the Wayback Machine's Save Page Now."
    )
    parser.add_argument(
        "--changed-files",
        type=Path,
        required=True,
        help="Path to a newline-separated list of changed file paths.",
    )
    args = parser.parse_args()

    urls = collect_urls(read_changed_files(args.changed_files))
    print(f"Found {len(urls)} new URLs to preserve")
    if not urls:
        return 0

    print(f"Submitting {len(urls)} URLs to Save Page Now...")
    results = preserve(urls)

    date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    log_path = write_log(results, date_str)
    print(f"\nLog written to {log_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
