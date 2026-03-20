#!/usr/bin/env python3
"""
state_manager.py — Minimal CLI for reading/writing swarm run state.

Usage:
    python swarm/tools/state_manager.py read
    python swarm/tools/state_manager.py update --section "CURRENT OBJECTIVE" --content "..."
    python swarm/tools/state_manager.py archive
"""

import argparse
import shutil
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
STATE_DIR = BASE_DIR / "state"
ARCHIVE_DIR = STATE_DIR / "archive"
RUN_STATE = STATE_DIR / "run_state.md"


def read_run_state():
    """Read and return current run state content."""
    if not RUN_STATE.exists():
        return ""
    return RUN_STATE.read_text(encoding="utf-8")


def write_run_state(content):
    """Write content to run_state.md with auto-updated timestamp."""
    # Strip any existing LAST UPDATED section, we'll add a fresh one
    sections = content.split("# LAST UPDATED")
    clean = sections[0].rstrip()
    timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    clean += f"\n\n# LAST UPDATED\n{timestamp}\n"
    RUN_STATE.write_text(clean, encoding="utf-8")


def update_section(section_title, new_content):
    """Update a single section in run_state.md by H1 header name."""
    text = read_run_state()
    if not text.strip():
        write_run_state(f"# {section_title}\n{new_content}\n")
        return

    lines = text.split("\n")
    result = []
    in_target = False
    replaced = False

    for line in lines:
        if line.startswith("# "):
            header = line[2:].strip()
            if header == section_title:
                result.append(f"# {section_title}")
                result.append(new_content)
                in_target = True
                replaced = True
                continue
            else:
                in_target = False

        if not in_target:
            result.append(line)

    if not replaced:
        # Section not found — append it
        result.append(f"\n# {section_title}")
        result.append(new_content)

    write_run_state("\n".join(result))


def archive_state():
    """Copy current run_state.md to archive with timestamp."""
    if not RUN_STATE.exists():
        print("No run_state.md to archive.")
        return

    ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%dT%H%M%S")
    dest = ARCHIVE_DIR / f"run_state-{timestamp}.md"
    shutil.copy2(RUN_STATE, dest)
    print(f"Archived to {dest.relative_to(BASE_DIR)}")


def main():
    parser = argparse.ArgumentParser(
        description="Swarm state manager — read, update, or archive run state."
    )
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("read", help="Print current run state")

    update_p = sub.add_parser("update", help="Update a section in run state")
    update_p.add_argument("--section", required=True, help="Section header (e.g. 'CURRENT OBJECTIVE')")
    update_p.add_argument("--content", required=True, help="New content for the section")

    sub.add_parser("archive", help="Archive current run state with timestamp")

    args = parser.parse_args()

    if args.command == "read":
        print(read_run_state())
    elif args.command == "update":
        update_section(args.section, args.content)
        print(f"Updated section: {args.section}")
    elif args.command == "archive":
        archive_state()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
