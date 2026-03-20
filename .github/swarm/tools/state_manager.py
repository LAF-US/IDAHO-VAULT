"""Minimal state manager for session persistence.

Reads and writes structured markdown state files used to pass context
between independent Claude Code sessions (dead-drop pattern).
"""

from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parents[1]
STATE_DIR = BASE_DIR / "state"
RUN_STATE = STATE_DIR / "run_state.md"


def read_run_state():
    """Print the current run state file contents."""
    if not RUN_STATE.exists():
        return ""
    return RUN_STATE.read_text()


def write_run_state(content: str):
    """Write full run state content with an auto-appended timestamp."""
    timestamp = datetime.now().isoformat()
    content += f"\n\n# LAST UPDATED\n{timestamp}\n"
    RUN_STATE.write_text(content)


def update_section(section_title: str, new_content: str):
    """Replace or append a single section in run_state.md by heading title."""
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

    timestamp = datetime.now().isoformat()
    final = []
    for s in updated:
        if not s.startswith("# LAST UPDATED"):
            final.append(s)
    final.append(f"# LAST UPDATED\n{timestamp}\n")

    RUN_STATE.write_text("\n".join(final))


if __name__ == "__main__":
    print(read_run_state())
