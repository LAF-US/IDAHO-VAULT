#!/usr/bin/env python3
"""
state_manager.py — Minimal read/write/update interface for swarm run state.

Usage:
    python swarm/tools/state_manager.py                          # Print current run state
    python swarm/tools/state_manager.py read                     # Print current run state
    python swarm/tools/state_manager.py update "SECTION" "content"  # Update a section
    python swarm/tools/state_manager.py snapshot                 # Archive current state
    python swarm/tools/state_manager.py archive                  # Archive current state (alias)
"""

import sys
import shutil
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parents[1]
STATE_DIR = BASE_DIR / "state"
ARCHIVE_DIR = STATE_DIR / "archive"
RUN_STATE = STATE_DIR / "run_state.md"


def read_run_state():
    if not RUN_STATE.exists():
        return ""
    return RUN_STATE.read_text()


def write_run_state(content: str):
    timestamp = datetime.now().isoformat()
    # Strip any existing LAST UPDATED section before appending new one
    lines = content.split("\n")
    cleaned = []
    skip = False
    for line in lines:
        if line.strip() == "# LAST UPDATED":
            skip = True
            continue
        if skip and line.startswith("# "):
            skip = False
        if not skip:
            cleaned.append(line)

    # Remove trailing blank lines
    while cleaned and cleaned[-1].strip() == "":
        cleaned.pop()

    cleaned.append("")
    cleaned.append("# LAST UPDATED")
    cleaned.append(timestamp)
    cleaned.append("")

    RUN_STATE.write_text("\n".join(cleaned))


def update_section(section_title: str, new_content: str):
    text = read_run_state()
    # Parse into list of (title, body) tuples
    sections = []
    current_title = None
    current_body = []

    for line in text.split("\n"):
        if line.startswith("# "):
            if current_title is not None:
                sections.append((current_title, "\n".join(current_body)))
            current_title = line[2:].strip()
            current_body = []
        else:
            current_body.append(line)

    if current_title is not None:
        sections.append((current_title, "\n".join(current_body)))

    # Replace or append
    found = False
    result_parts = []
    for title, body in sections:
        if title == section_title:
            result_parts.append(f"# {title}\n{new_content}\n")
            found = True
        else:
            result_parts.append(f"# {title}\n{body}")

    if not found:
        result_parts.append(f"# {section_title}\n{new_content}\n")

    write_run_state("\n".join(result_parts))


def snapshot():
    if not RUN_STATE.exists():
        print("No run_state.md to snapshot.")
        return

    ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    dest = ARCHIVE_DIR / f"run_state-{timestamp}.md"
    shutil.copy2(RUN_STATE, dest)
    print(f"Snapshot saved: {dest.name}")


def main():
    args = sys.argv[1:]

    if not args or args[0] == "read":
        print(read_run_state())
    elif args[0] == "update" and len(args) >= 3:
        section = args[1]
        content = args[2]
        update_section(section, content)
        print(f"Updated section: {section}")
    elif args[0] in ("snapshot", "archive"):
        snapshot()
    else:
        print(__doc__)


if __name__ == "__main__":
    main()
