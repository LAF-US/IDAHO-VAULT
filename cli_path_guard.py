"""Containment guard for the calendar scripts' command-line path overrides.

Every cron_clock working-note script accepts optional path arguments. Those
arguments are untrusted input to the interpreter, so each one is normalized
and containment-checked here before any read or write: the resolved path
must live inside this repository. The normalize-then-prefix-check shape is
the RFC-recommended (and CodeQL-recognized) barrier against path injection.
"""

from __future__ import annotations

import os
from pathlib import Path

_REPO = Path(__file__).resolve().parent


def repo_path(argument: str, must_exist: bool = True) -> Path:
    resolved = os.path.realpath(argument)
    if not resolved.startswith(str(_REPO) + os.sep):
        raise SystemExit(
            f'Path override must name a file inside the repository: {argument!r}'
        )
    path = Path(resolved)
    if must_exist and not path.is_file():
        raise SystemExit(f'Path override names no existing file: {argument!r}')
    return path
