"""Shared ``gh`` / subprocess wrapper — the single run-capture-raise primitive.

The first member of the Cluster A redesign shared lib (#600 §5), landed
independently per #601 item 4. `review_feedback_loop._run`, `pr_lifecycle._run`,
and `issue_reconciler.gh` were three copies of the same thing: run a command,
capture stdout/stderr as text, and on a non-zero exit raise a ``RuntimeError``
carrying the command and both streams. This is that one definition; the engines
import it instead of each keeping their own.
"""

from __future__ import annotations

import subprocess


def run(cmd: list[str], check: bool = True) -> subprocess.CompletedProcess[str]:
    """Run ``cmd``, capturing stdout/stderr as text. On a non-zero exit (when
    ``check`` is True), raise ``RuntimeError`` carrying the command and both
    streams so the failure is never silent."""
    result = subprocess.run(cmd, capture_output=True, text=True)
    if check and result.returncode != 0:
        raise RuntimeError(
            f"Command failed ({result.returncode}): {' '.join(cmd)}\n"
            f"stdout:\n{result.stdout}\n"
            f"stderr:\n{result.stderr}"
        )
    return result
