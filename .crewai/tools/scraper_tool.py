#!/usr/bin/env python3
"""
CrewAI Tool: Idaho Legislature Bill Status Checker

Checks current bill status from the Idaho Legislature website.
Lightweight wrapper — uses the existing idaho_leg_scraper.py for
heavy scraping, but this tool provides quick status lookups.

LINUX }!{ — targets Linux-native execution.
"""

import re

from crewai.tools import BaseTool

try:
    import requests
    from bs4 import BeautifulSoup
    HAS_WEB = True
except ImportError:
    HAS_WEB = False


MINIDATA_URL = "https://legislature.idaho.gov/sessioninfo/2026/legislation/minidata/"
USER_AGENT = "IDAHO-VAULT CrewAI/1.0 (journalism research; github.com/loganfinney27/IDAHO-VAULT)"


class BillStatusTool(BaseTool):
    name: str = "bill_status_checker"
    description: str = (
        "Checks the current status of Idaho legislature bills by scraping "
        "the minidata page at legislature.idaho.gov. Provide a bill ID "
        "(e.g. 'H0847', 'S1361') or 'all' for the full listing."
    )

    def _run(self, query: str = "all") -> str:
        """Fetch current bill status from legislature.idaho.gov.

        Args:
            query: Bill ID (e.g. 'H0847') or 'all' for full listing.
        """
        if not HAS_WEB:
            return "Error: requests and beautifulsoup4 not installed. Cannot fetch live data."

        try:
            resp = requests.get(
                MINIDATA_URL,
                headers={"User-Agent": USER_AGENT},
                timeout=30,
            )
            resp.raise_for_status()
        except requests.RequestException as e:
            return f"Error fetching minidata page: {e}"

        soup = BeautifulSoup(resp.text, "html.parser")
        rows = soup.find_all("tr")

        bills = []
        for row in rows:
            cells = row.find_all("td")
            if len(cells) < 3:
                continue
            bill_id = cells[0].get_text(strip=True)
            title = cells[1].get_text(strip=True)
            status = cells[2].get_text(strip=True)
            vote = cells[3].get_text(strip=True) if len(cells) > 3 else ""

            if query.lower() != "all" and not bill_id.upper().startswith(query.upper()):
                continue

            bills.append(
                f"  {bill_id}: {title} | Status: {status}"
                + (f" | Vote: {vote}" if vote else "")
            )

        if not bills:
            return f"No bills found matching '{query}'" if query.lower() != "all" else "No bills found on minidata page"

        return f"Live bill status — {len(bills)} bills\n" + "\n".join(bills[:100])
