#!/usr/bin/env python3
"""
CrewAI Tool: Minidata CSV Reader

Reads and normalizes the JFAC minidata CSV (appropriations bill tracking).
Wraps logic from .github/scripts/normalize_budget_data.py.

LINUX }!{ — targets Linux-native execution.
"""

import csv
from pathlib import Path

from crewai.tools import BaseTool
from pydantic import Field


class MinidataTool(BaseTool):
    name: str = "minidata_reader"
    description: str = (
        "Reads the JFAC minidata CSV file and returns structured bill data. "
        "Each row contains: bill_id, title, status, and vote information. "
        "Use this to analyze Idaho appropriations bills and their current status."
    )
    csv_path: str = Field(default="minidata-2026-04-01.csv")

    def _run(self, query: str = "") -> str:
        """Read and return minidata CSV contents as structured text.

        Args:
            query: Optional filter — a bill ID prefix (e.g. 'H08', 'S13')
                   or empty string for all bills.
        """
        vault_root = Path(__file__).resolve().parent.parent.parent
        path = vault_root / self.csv_path

        if not path.exists():
            return f"Error: minidata CSV not found at {path}"

        bills = []
        with path.open("r", encoding="cp1252", newline="") as f:
            for row in csv.reader(f):
                if not row or len(row) < 3:
                    continue
                bill_id = row[0].strip()
                title = row[1].strip()
                status = row[2].strip()
                vote = row[3].strip() if len(row) > 3 else ""

                if query and not bill_id.upper().startswith(query.upper()):
                    continue

                bills.append(
                    f"  {bill_id}: {title} | Status: {status}"
                    + (f" | Vote: {vote}" if vote else "")
                )

        if not bills:
            return f"No bills found matching '{query}'" if query else "No bills found in CSV"

        header = f"JFAC Minidata — {len(bills)} bills"
        if query:
            header += f" (filter: {query})"
        return header + "\n" + "\n".join(bills)
