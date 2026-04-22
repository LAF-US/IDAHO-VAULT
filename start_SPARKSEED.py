#!/usr/bin/env python
"""Repo-root wrapper for the Python-native SPARKSEED bootstrap."""

from __future__ import annotations

import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent
SRC_ROOT = REPO_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from idaho_vault import sparkseed


if __name__ == "__main__":
    raise SystemExit(sparkseed.main(sys.argv[1:]))
