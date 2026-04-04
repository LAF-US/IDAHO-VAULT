"""Classify changed file paths by risk tier for auto-PR decisions.

Reads file paths from stdin (one per line) and outputs a JSON object:
  {"tier": "high"|"low", "high_risk_files": [...], "low_risk_files": [...]}

Rule: if ANY file is high-risk, the entire result is high-risk.
Unknown paths default to high-risk (fail-safe).
"""

import json
import re
import sys

# Daily note pattern: YYYY-MM-DD.md at repo root
_DAILY_NOTE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}\.md$")

HIGH_RISK_PREFIXES = (
    "!/",
    ".github/workflows/",
    ".github/scripts/",
)

HIGH_RISK_EXACT = {
    "CLAUDE.md",
    ".gitignore",
    ".github/copilot-instructions.md",
    # Note: governance files under !/ are covered by HIGH_RISK_PREFIXES ("!/")
    # Old !ADMIN/ and !ADMINISTRATION/ paths removed — those folders no longer exist
}

LOW_RISK_EXACT = {
    "TO DO LIST.md",
}

LOW_RISK_PREFIXES = (
    "SOURCES/",
    "TOPICS/",
    "PEOPLE/",
    "PLACES/",
    "ORGANIZATIONS/",
    "GOVERNMENTS/",
    "ATTACHMENTS/",
    ".github/swarm/",
    "!/swarm/",
)


def classify(path: str) -> str:
    """Return 'high' or 'low' for a single file path."""
    if path in HIGH_RISK_EXACT:
        return "high"
    for prefix in HIGH_RISK_PREFIXES:
        if path.startswith(prefix):
            return "high"
    if path in LOW_RISK_EXACT:
        return "low"
    if _DAILY_NOTE_RE.match(path):
        return "low"
    for prefix in LOW_RISK_PREFIXES:
        if path.startswith(prefix):
            return "low"
    # Unknown path → high risk (fail-safe)
    return "high"


def main():
    paths = [line.strip() for line in sys.stdin if line.strip()]
    if not paths:
        print(json.dumps({"tier": "low", "high_risk_files": [], "low_risk_files": []}))
        return

    high_risk = []
    low_risk = []

    for p in paths:
        if classify(p) == "high":
            high_risk.append(p)
        else:
            low_risk.append(p)

    tier = "high" if high_risk else "low"
    print(json.dumps({
        "tier": tier,
        "high_risk_files": high_risk,
        "low_risk_files": low_risk,
    }))


if __name__ == "__main__":
    main()
