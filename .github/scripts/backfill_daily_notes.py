#!/usr/bin/env python3
"""
backfill_daily_notes.py - manual historical daily-note repair for IDAHO-VAULT.

Purpose:
  Repair a span of daily notes by carrying incomplete items forward day by day
  from the previous daily note while preserving the current live TO DO LIST.md
  surface.

This is intentionally separate from daily_rollover.py:
  - daily_rollover.py maintains the live active backlog and today's note
  - backfill_daily_notes.py repairs historical note continuity only

Usage:
    python3 .github/scripts/backfill_daily_notes.py --start YYYY-MM-DD --end YYYY-MM-DD [--dry-run]
"""

from __future__ import annotations

import argparse
import sys
from datetime import date, timedelta
from pathlib import Path

# Keep helper behavior in sync with the live rollover machinery.
sys.path.insert(0, str(Path(__file__).parent))
import daily_rollover


def _top_level_task_count(lines: list[str]) -> int:
    return len([line for line in lines if daily_rollover._is_top_level_task(line)])


def backfill_range(sta***REMOVED***date: date, end_date: date, dry_run: bool = False) -> None:
    if end_date < sta***REMOVED***date:
        raise ValueError("--end must be on or after --start")

    current_date = sta***REMOVED***date
    simulated_notes: dict[date, str] = {}
    while current_date <= end_date:
        source_date = current_date - timedelta(days=1)
        source_file = daily_rollover.VAULT_ROOT / f"{source_date}.md"

        daily_rollover.log(f"Backfilling: {source_date} -> {current_date}")

        if source_date in simulated_notes:
            source_content = simulated_notes[source_date]
        elif source_file.exists():
            source_content = source_file.read_text(encoding="utf-8")
        else:
            raise FileNotFoundError(
                f"Cannot backfill {current_date}: missing source daily note {source_file.name}"
            )

        carried = daily_rollover.carry_forward(
            daily_rollover.extract_todo_section(source_content)
        )

        if carried:
            daily_rollover.log(
                f"Carrying forward {_top_level_task_count(carried)} incomplete item(s):"
            )
            for line in carried:
                daily_rollover.log(f"  {line}")
        else:
            daily_rollover.log("No incomplete items found - note will be normalized only.")

        target_file = daily_rollover.VAULT_ROOT / f"{current_date}.md"
        base_content = target_file.read_text(encoding="utf-8") if target_file.exists() else None
        new_content = daily_rollover.build_today_note_content(
            current_date,
            carried,
            base_content=base_content,
        )

        if dry_run:
            simulated_notes[current_date] = new_content
            daily_rollover.log(f"\n--- {target_file.name} (dry run) ---")
            daily_rollover.log(new_content.rstrip("\n"))
        else:
            target_file.write_text(new_content, encoding="utf-8", newline="\n")
            daily_rollover.log(f"Updated {target_file.name}")
        current_date += timedelta(days=1)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Repair a historical range of daily notes without rewriting TO DO LIST.md"
    )
    parser.add_argument(
        "--start",
        required=True,
        help="First target date to repair (YYYY-MM-DD). Uses the day before as the source.",
    )
    parser.add_argument(
        "--end",
        required=True,
        help="Last target date to repair (YYYY-MM-DD), inclusive.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print output without writing files.",
    )
    args = parser.parse_args()

    sta***REMOVED***date = date.fromisoformat(args.start)
    end_date = date.fromisoformat(args.end)
    backfill_range(sta***REMOVED***date, end_date, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
