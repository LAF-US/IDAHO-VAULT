#!/usr/bin/env python3
"""
Address Space POC — Proof of Concept

Initializes 10 number stubs (100-109) as crew state neurons
and writes entity references to 10 letter stubs.

This demonstrates the content-addressable memory system:
  NUMBERS = crew state (run logs, status, cross-references)
  LETTERS = entity nodes (what the crew discovers about vault entities)

Usage:
  python .crewai/address_poc.py                # Dry run
  python .crewai/address_poc.py --execute      # Write to stubs

LINUX }!{ — targets Linux-native execution.
"""

import argparse
from datetime import datetime, timezone
from pathlib import Path


VAULT_ROOT = Path(__file__).resolve().parent.parent

# 10 number neurons (100-109) — crew state memory
NUMBER_STUBS = list(range(100, 110))

# Neuron assignments
NEURON_MAP = {
    100: ("JFAC Crew — Run Index", "Master index of all JFAC crew runs. Each run appends its ID and timestamp here."),
    101: ("Budget Scout — State", "Current state of the Budget Scout agent: last run, bills analyzed, errors."),
    102: ("Legislative Tracker — State", "Current state of the Legislative Tracker agent: last status check, bill count."),
    103: ("H911 Parser — State", "Current state of the H911 Parser agent (Phase 2 stub). Awaiting activation."),
    104: ("Minidata Snapshot Log", "Log of all minidata CSV snapshots ingested, with dates and bill counts."),
    105: ("Bill Status Changelog", "Tracked bills that changed status between snapshots. The delta record."),
    106: ("Crew Error Log", "Errors and exceptions encountered during crew runs. For debugging."),
    107: ("Entity Discovery Queue", "Letter stubs that the crew has identified as needing content population."),
    108: ("Cross-Reference Index", "Links between number neurons and letter entities. The connective tissue."),
    109: ("Voyager Record", "The crew's self-description: what it does, how it works, why it exists."),
}

# 10 letter entities — real entities from JFAC data
LETTER_STUBS = {
    "Idaho": "The state. All appropriations flow through the Idaho state government.",
    "Budget": "The central concept — JFAC manages the state budget through appropriations bills.",
    "Governor": "The Governor submits budget recommendations that JFAC reviews and modifies.",
    "General Fund": "Idaho's primary unrestricted revenue source. Most appropriations draw from here.",
    "Medicaid": "Major budget line item. Health and Welfare Department's largest program.",
    "Transportation": "Idaho Transportation Department. Roads, bridges, infrastructure spending.",
    "Public Schools": "K-12 education funding. Largest single category in the state budget.",
    "7929": "Voyager Record: The simplest triangle. A single geometric form. The beginning.",
    "7930": "Voyager Record: The Sierpinski triangle. Recursive self-similarity. The pattern.",
    "General Fund": "Idaho's primary unrestricted revenue source. Most appropriations draw from here.",
}

# Fix duplicate — replace General Fund duplicate with another entity
LETTER_STUBS["$"] = "The vault's special character entity. Money. The budget in its purest form."


def neuron_content(address: int, title: str, description: str, run_id: str) -> str:
    """Generate content for a number neuron stub."""
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    return f"""---
title: "{address} — {title}"
date created: "{now}"
authority: crewai/address-space
doc_class: neuron
neuron_id: {address}
---

# {address} — {title}

{description}

## Log

- **{run_id}**: Neuron initialized by address_poc.py

"""


def entity_content(name: str, description: str, run_id: str, existing: str) -> str:
    """Generate content for a letter entity stub."""
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    if existing.strip():
        # Append to existing content
        return existing.rstrip() + f"""

## CrewAI Entity Reference

{description}

*Registered by address_poc.py — run {run_id}, {now}*
"""
    else:
        # Initialize empty stub
        return f"""---
title: "{name}"
date created: "{now}"
authority: crewai/address-space
doc_class: entity
---

# {name}

{description}

*Registered by address_poc.py — run {run_id}, {now}*
"""


def main():
    parser = argparse.ArgumentParser(description="Address Space POC")
    parser.add_argument("--execute", action="store_true", help="Write to stubs (default: dry run)")
    args = parser.parse_args()

    run_id = datetime.now(timezone.utc).strftime("POC-%Y%m%d-%H%M%S")
    mode = "EXECUTING" if args.execute else "DRY RUN"
    print(f"Address Space POC — {mode}")
    print(f"Run ID: {run_id}")
    print(f"Vault root: {VAULT_ROOT}")
    print("=" * 60)

    # Number neurons
    print("\n== NUMBER NEURONS (100-109) ==")
    for addr in NUMBER_STUBS:
        path = VAULT_ROOT / f"{addr}.md"
        title, desc = NEURON_MAP[addr]
        if not path.exists():
            print(f"  SKIP {addr}.md — file does not exist")
            continue
        current = path.read_text(encoding="utf-8")
        if current.strip():
            print(f"  SKIP {addr}.md — already has content ({len(current)}B)")
            continue
        content = neuron_content(addr, title, desc, run_id)
        print(f"  {'WRITE' if args.execute else 'WOULD WRITE'}: {addr}.md — {title}")
        if args.execute:
            path.write_text(content, encoding="utf-8")

    # Letter entities
    print("\n== LETTER ENTITIES ==")
    for name, desc in LETTER_STUBS.items():
        path = VAULT_ROOT / f"{name}.md"
        if not path.exists():
            print(f"  SKIP {name}.md — file does not exist")
            continue
        current = path.read_text(encoding="utf-8")
        content = entity_content(name, desc, run_id, current)
        action = "APPEND" if current.strip() else "INIT"
        print(f"  {'WRITE' if args.execute else 'WOULD'} {action}: {name}.md")
        if args.execute:
            path.write_text(content, encoding="utf-8")

    print("\n" + "=" * 60)
    if not args.execute:
        print("DRY RUN complete. Run with --execute to write.")
    else:
        print(f"POC complete. {run_id}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
