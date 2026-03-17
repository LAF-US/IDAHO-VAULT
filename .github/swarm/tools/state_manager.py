"""Minimal state manager for session persistence.

Reads and writes structured markdown state files so that
successive Claude Code sessions can pick up where the last left off.
"""

from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parents[1]
STATE_DIR = BASE_DIR / "state"
RUN_STATE = STATE_DIR / "run_state.md"


def read_run_state():
    """Print the current run state."""
    if not RUN_STATE.exists():
        return ""
    return RUN_STATE.read_text()


def write_run_state(content: str):
    """Write full run state with automatic timestamp."""
    timestamp = datetime.now().isoformat()
    content += f"\n\n# LAST UPDATED\n{timestamp}\n"
    RUN_STATE.write_text(content)


def update_section(section_title: str, new_content: str):
    """Replace a single section in run_state.md by heading match."""
    text = read_run_state()
    sections = text.split("# ")

    updated = []
    found = False

    for section in sections:
        if section.startswith(section_title):
            updated.append(f"# {section_title}\n{new_content}\n")
            found = True
        else:
            if section.strip():
                updated.append("# " + section)

    if not found:
        updated.append(f"# {section_title}\n{new_content}\n")

    result = "\n".join(updated)

    # Auto-update timestamp
    timestamp = datetime.now().isoformat()
    final_sections = result.split("# ")
    final = []
    ts_found = False
    for s in final_sections:
        if s.startswith("LAST UPDATED"):
            final.append(f"# LAST UPDATED\n{timestamp}\n")
            ts_found = True
        else:
            if s.strip():
                final.append("# " + s)
    if not ts_found:
        final.append(f"# LAST UPDATED\n{timestamp}\n")

    RUN_STATE.write_text("\n".join(final))


if __name__ == "__main__":
    state = read_run_state()
    if state.strip():
        print(state)
    else:
        print("(run_state.md is empty)")
