#!/usr/bin/env python3
"""Validate that protected durable dotfolders have tracked anchor files.

The vault uses two different kinds of dotfolders:

1. durable identity/governance chambers that should persist across clones,
   branch switches, and tool changes
2. local runtime/cache/state folders that are intentionally ephemeral

This script only checks the durable class.
"""

from __future__ import annotations

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[2]

REQUIRED_ANCHORS = {
    ".claude": [".claude/CLAUDE.md"],
    ".gemini": [".gemini/GEMINI.md"],
    ".codex": [".codex/CODEX.md"],
    ".github": [".github/copilot-instructions.md"],
    ".crewai": [".crewai/MANIFEST.md"],
    ".grok": [".grok/GROK.md"],
    ".deepseek": [".deepseek/DEEPSEEK.md"],
    ".perplexity": [".perplexity/PERPLEXITY.md"],
    ".serena": [".serena/SERENA.md"],
    ".antigravity": [".antigravity/ANTIGRAVITY.md"],
    ".bartimaeus": [".bartimaeus/BARTIMAEUS.md"],
    ".zagreus": [".zagreus/ZAGREUS.md"],
    ".persephone": [".persephone/PERSEPHONE.md"],
    ".google": [".google/GOOGLE.md"],
    ".meta": [".meta/META.md"],
    ".microsoft": [".microsoft/MICROSOFT.md"],
    ".slack": [".slack/SLACK.md"],
    ".dionysus": [".dionysus/ZAGREUS.md"],
    ".abhorsen": [".abhorsen/README.md"],
}


def main() -> int:
    missing: list[str] = []

    for dotfolder, anchors in REQUIRED_ANCHORS.items():
        folder_path = ROOT / dotfolder
        if not folder_path.is_dir():
            missing.append(f"{dotfolder} (folder missing)")
            continue

        for anchor in anchors:
            anchor_path = ROOT / anchor
            if not anchor_path.is_file():
                missing.append(anchor)

    if missing:
        print("Missing durable dotfolder anchors:")
        for item in missing:
            print(f" - {item}")
        return 1

    print("All durable dotfolder anchors are present.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
