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


def _as_text(stream: object) -> str:
    """Coerce a captured stream to text. ``TimeoutExpired`` may hand back bytes
    even under ``text=True``, so decode those; ``None`` becomes ``""``."""
    if isinstance(stream, bytes):
        return stream.decode(errors="replace")
    return stream or ""


def run(
    cmd: list[str], check: bool = True, timeout: float | None = 300
) -> subprocess.CompletedProcess[str]:
    """Run ``cmd``, capturing stdout/stderr as text. On a non-zero exit (when
    ``check`` is True), raise ``RuntimeError`` carrying the command and both
    streams so the failure is never silent. ``timeout`` (seconds; ~5 min default)
    guards against a stalled call hanging the workflow indefinitely — a timeout
    raises the same ``RuntimeError`` surface."""
    # `cmd` is argv-list form with shell=False — each element is passed as a literal
    # argument, so there is no shell to inject into. The audit rule fires on any
    # non-literal argv; vetted safe for this wrapper (callers build cmd[0] from a
    # fixed program name, never user text). See PR #691.
    try:
        result = subprocess.run(  # nosemgrep
            cmd, capture_output=True, text=True, timeout=timeout
        )
    except subprocess.TimeoutExpired as exc:
        # exc carries whatever the child wrote before the deadline; surface it so a
        # stalled call still leaves its partial logs (mirrors the non-zero-exit branch).
        raise RuntimeError(
            f"Command timed out after {timeout}s: {' '.join(cmd)}\n"
            f"stdout:\n{_as_text(exc.stdout)}\n"
            f"stderr:\n{_as_text(exc.stderr)}"
        ) from exc
    if check and result.returncode != 0:
        raise RuntimeError(
            f"Command failed ({result.returncode}): {' '.join(cmd)}\n"
            f"stdout:\n{result.stdout}\n"
            f"stderr:\n{result.stderr}"
        )
    return result
