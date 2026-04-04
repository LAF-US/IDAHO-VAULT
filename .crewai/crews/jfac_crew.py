#!/usr/bin/env python3
"""
JFAC Crew — Idaho Joint Finance-Appropriations Committee Analysis

Three agents, five tasks, mapped to the 5 Ws:
  WHO:   Budget Scout identifies agencies, sponsors, committees
  WHAT:  Budget Scout reads what each bill proposes (appropriations, changes)
  WHEN:  Legislative Tracker builds the timeline (introduced, heard, passed)
  WHERE: Legislative Tracker maps committee/chamber routing
  WHY:   H911 Parser (Phase 2) analyzes bill text for intent and justification

Agents:
  1. Budget Scout    — ingests minidata CSV, identifies bill landscape
  2. Legislative Tracker — checks live status, builds timelines
  3. H911 Parser     — (stub) bill text analysis, activated Phase 2

Output: !/CREWAI/ for Logan's review.

LINUX }!{ — targets Linux-native execution.
"""

import os
import sys
from datetime import datetime, timezone
from pathlib import Path

from crewai import Agent, Crew, Process, Task

# Add project root to path for tool imports
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))

from dotenv import load_dotenv

load_dotenv(project_root / ".env")

from .tools.minidata_tool import MinidataTool
from .tools.timeline_tool import TimelineTool
from .tools.scraper_tool import BillStatusTool


# ── Output Configuration ─────────────────────────────────────────────────────

OUTPUT_DIR = project_root / "!" / "CREWAI"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def _vault_frontmatter(title: str, run_id: str) -> str:
    """Generate vault-compatible frontmatter (post-CHAINFIRE — no tags)."""
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    return f"""---
title: "{title}"
date created: "{now}"
authority: crewai/jfac-crew
doc_class: analysis
crew_run_id: "{run_id}"
---

"""


# ── Tools ─────────────────────────────────────────────────────────────────────

minidata_tool = MinidataTool()
timeline_tool = TimelineTool()
bill_status_tool = BillStatusTool()


# ── Agents (3) ────────────────────────────────────────────────────────────────

budget_scout = Agent(
    role="Budget Scout",
    goal=(
        "Ingest and analyze the JFAC minidata CSV to identify all tracked "
        "appropriations bills, their current status, sponsoring agencies, "
        "and financial scope. Answer WHO is requesting money and WHAT they want."
    ),
    backstory=(
        "You are a legislative budget analyst specializing in Idaho state "
        "appropriations. You read JFAC minidata spreadsheets and extract "
        "the key financial and organizational details from each bill."
    ),
    tools=[minidata_tool],
    verbose=True,
    allow_delegation=False,
)

legislative_tracker = Agent(
    role="Legislative Tracker",
    goal=(
        "Track the procedural journey of appropriations bills through the "
        "Idaho Legislature. Answer WHEN bills were introduced, heard, and "
        "voted on, and WHERE they are in the committee/chamber process."
    ),
    backstory=(
        "You are a legislative process expert who monitors bill status "
        "changes across committee hearings, floor votes, and chamber "
        "crossovers. You build timelines showing how bills move."
    ),
    tools=[timeline_tool, bill_status_tool],
    verbose=True,
    allow_delegation=False,
)

h911_parser = Agent(
    role="H911 Parser",
    goal=(
        "Analyze bill text to understand WHY appropriations are being "
        "requested — the policy intent, justification, and context behind "
        "each budget line item."
    ),
    backstory=(
        "You are a policy analyst who reads bill text and committee hearing "
        "materials to understand the rationale behind appropriations requests. "
        "You connect budget numbers to policy goals."
    ),
    tools=[],  # Phase 2: bill text scraper tool will be added here
    verbose=True,
    allow_delegation=False,
)


# ── Tasks (5) — mapped to the 5 Ws ───────────────────────────────────────────

task_who = Task(
    description=(
        "Read the minidata CSV and identify WHO is involved in each tracked "
        "appropriations bill: the sponsoring agency, relevant committee, "
        "and key legislators. List all bills with their organizational context."
    ),
    expected_output=(
        "A structured list of all tracked JFAC bills with: bill ID, title, "
        "sponsoring agency/entity, and committee assignment."
    ),
    agent=budget_scout,
)

task_what = Task(
    description=(
        "For each tracked appropriations bill, analyze WHAT is being proposed: "
        "the nature of the appropriation, the budget category, and any notable "
        "financial details visible in the minidata."
    ),
    expected_output=(
        "A summary of each bill's appropriation scope: what type of funding "
        "(general fund, dedicated, federal), what purpose, and any notable amounts."
    ),
    agent=budget_scout,
)

task_when = Task(
    description=(
        "Build a timeline for each tracked bill showing WHEN key events occurred: "
        "introduction date, committee hearings, floor votes, and current status "
        "as of the latest snapshot."
    ),
    expected_output=(
        "A chronological timeline for each tracked bill showing status changes "
        "across available minidata snapshots, with dates and status descriptions."
    ),
    agent=legislative_tracker,
)

task_where = Task(
    description=(
        "Map WHERE each tracked bill currently sits in the legislative process: "
        "which committee, which chamber, and whether it has crossed over. "
        "Check live status if available."
    ),
    expected_output=(
        "A routing map showing each bill's current location in the legislative "
        "process: committee assignment, chamber, and procedural status."
    ),
    agent=legislative_tracker,
)

task_why = Task(
    description=(
        "NOTE: This is a Phase 2 stub. For now, provide a brief summary of "
        "WHY each appropriation appears to be requested based on the bill title "
        "and any context available from the minidata. Full bill text analysis "
        "will be added when the H911 Parser tools are activated."
    ),
    expected_output=(
        "A preliminary intent analysis for each tracked bill based on title "
        "and available context. Flag bills that need full text analysis in Phase 2."
    ),
    agent=h911_parser,
)


# ── Crew Assembly ─────────────────────────────────────────────────────────────

def build_jfac_crew() -> Crew:
    """Assemble the JFAC Crew with all agents and tasks."""
    return Crew(
        agents=[budget_scout, legislative_tracker, h911_parser],
        tasks=[task_who, task_what, task_when, task_where, task_why],
        process=Process.sequential,
        verbose=True,
    )


def run() -> str:
    """Execute the JFAC Crew and write output to !/CREWAI/."""
    run_id = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    crew = build_jfac_crew()

    result = crew.kickoff()

    # Write output to staging directory
    output_path = OUTPUT_DIR / f"jfac-analysis-{run_id}.md"
    frontmatter = _vault_frontmatter(
        f"JFAC Appropriations Analysis — {run_id}", run_id
    )
    output_path.write_text(
        frontmatter + str(result),
        encoding="utf-8",
    )

    return f"JFAC Crew complete. Output: {output_path}"


if __name__ == "__main__":
    print(run())
