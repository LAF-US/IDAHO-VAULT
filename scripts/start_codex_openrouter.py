from __future__ import annotations

import sys

from openrouter_runtime import launch_agent


if __name__ == "__main__":
    raise SystemExit(launch_agent("codex", "codex", sys.argv[1:]))
