#!/usr/bin/env python3
"""
CrewAI Tool: Appropriations Timeline Builder

Builds a status timeline from dated minidata CSV snapshots.
Wraps logic from .github/scripts/minidata_appropriations_timeline.py.

LINUX }!{ — targets Linux-native execution.
"""

import csv
from pathlib import Path

from crewai.tools import BaseTool


# Bills tracked for JFAC appropriations monitoring
TRACKED_BILLS = [
    "S1361", "S1363", "S1375", "S1373",
    "H0847", "H0848",
    "S1331", "S1380", "S1381", "S1382", "S1384", "S1385", "S1383",
    "S1362",
]


def _load_csv(path: Path) -> dict[str, tuple[str, str, str]]:
    """Load a minidata CSV into {bill_id: (title, status, vote)}."""
    data = {}
    with path.open("r", encoding="cp1252", newline="") as f:
        for row in csv.reader(f):
            if not row or len(row) < 3:
                continue
            bill_id = row[0].strip().upper()
            title = row[1].strip()
            status = row[2].strip()
            vote = row[3].strip() if len(row) > 3 else ""
            data[bill_id] = (title, status, vote)
    return data


class TimelineTool(BaseTool):
    name: str = "appropriations_timeline"
    description: str = (
        "Builds a status timeline for tracked JFAC appropriations bills "
        "by comparing multiple dated minidata CSV snapshots. Shows which bills "
        "changed status between snapshots. Use this to track bill progression."
    )

    def _run(self, query: str = "") -> str:
        """Build timeline from available minidata snapshots.

        Args:
            query: Optional — specific bill ID to focus on, or empty for all tracked bills.
        """
        vault_root = Path(__file__).resolve().parent.parent.parent

        # Find all minidata CSV files sorted by date
        csv_files = sorted(vault_root.glob("minidata-*.csv"))
        if not csv_files:
            return "Error: No minidata CSV snapshots found in vault root."

        snapshots = []
        for path in csv_files:
            if ".original" in path.name:
                continue
            # Extract date from filename: minidata-2026-04-01.csv -> 2026-04-01
            date = path.stem.replace("minidata-", "")
            snapshots.append((date, _load_csv(path)))

        bills_to_track = TRACKED_BILLS
        if query:
            query_upper = query.upper()
            bills_to_track = [b for b in TRACKED_BILLS if b == query_upper]
            if not bills_to_track:
                bills_to_track = [query_upper]

        lines = [f"Appropriations Timeline — {len(snapshots)} snapshot(s)"]
        lines.append(f"Snapshots: {', '.join(d for d, _ in snapshots)}")
        lines.append("")

        for bill_id in bills_to_track:
            lines.append(f"  {bill_id}:")
            prev_status = None
            for date, data in snapshots:
                row = data.get(bill_id)
                if row is None:
                    status = "(not found)"
                    title = ""
                else:
                    title, status, _vote = row
                changed = " ** CHANGED **" if prev_status and status != prev_status else ""
                lines.append(f"    {date}: {status}{changed}")
                prev_status = status
            if snapshots and bill_id in snapshots[-1][1]:
                title = snapshots[-1][1][bill_id][0]
                lines.append(f"    Title: {title}")
            lines.append("")

        return "\n".join(lines)
