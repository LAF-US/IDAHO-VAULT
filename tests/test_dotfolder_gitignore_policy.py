from __future__ import annotations

import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def is_ignored(path: str) -> bool:
    result = subprocess.run(
        ["git", "check-ignore", "--no-index", "--quiet", "--", path],
        cwd=ROOT,
        capture_output=True,
        check=False,
        timeout=30,
    )
    if result.returncode not in {0, 1}:
        raise AssertionError(result.stderr.decode("utf-8", errors="replace"))
    return result.returncode == 0


# A specimen test used to live here: 24 hardcoded salvage-variant paths asserted
# ignored, enforcing the retired 509-line .gitignore against the deliberate
# 2026-08-03 cut to 4 lines ("Simplify .gitignore", 3591a4bb3). An enumeration of
# one day's junk drawer is a ratchet, not a policy — it demanded a new line for
# every new specimen and re-fired whenever a file moved. Removed 2026-08-08 per
# Logan's ruling; the tracking policy is the .gitignore itself.


def test_publishable_anchor_names_remain_visible() -> None:
    paths = [
        ".claude/CLAUDE.md",
        ".codex/AGENTS.md",
        ".config/CONFIG.md",
    ]

    ignored = [path for path in paths if is_ignored(path)]
    assert not ignored, f"Expected visible anchors, but ignored: {ignored}"
