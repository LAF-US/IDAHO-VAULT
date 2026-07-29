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


_ALLOWED_EXECUTABLES: set[str] = {"gh"}

# Allowed `gh` command SHAPES — the subcommand verb prefix, never the argument values.
# shell=False plus the executable allowlist already make injection inert, but the command
# INTENT was still assembled from caller-supplied pieces; CodeQL flags that as an
# uncontrolled command line. Pinning the verb prefix to this literal set means a caller
# can only ever invoke a family this automation already uses: dynamic values (PR numbers,
# label text, bodies, jq expressions) stay free, while `gh <something-else>` cannot be
# reached at all. Derived by enumerating every gh invocation across .github/**/*.py —
# including issue_reconciler's `gh(*args)` splat — so this is the observed surface, not a
# guess. ADD A LINE HERE when a script needs a new family; a missing entry fails loudly at
# the call rather than silently doing the wrong thing.
_ALLOWED_GH_PATTERNS: tuple[tuple[str, ...], ...] = (
    ("api",),                 # REST + `api graphql`; the query itself is an argument
    ("label", "create"),
    ("pr", "close"),
    ("pr", "comment"),
    ("pr", "edit"),
    ("pr", "list"),
    ("pr", "merge"),
    ("pr", "view"),
    ("issue", "list"),
    ("issue", "view"),
    ("issue", "create"),
    ("issue", "comment"),
    ("issue", "close"),
)


def _command_shape_allowed(args: list[str]) -> bool:
    """True if ``args`` (argv after the executable) opens with an allowed verb prefix."""
    return any(args[: len(pattern)] == list(pattern) for pattern in _ALLOWED_GH_PATTERNS)


def _as_text(value: bytes | str | None) -> str:
    """Normalize TimeoutExpired stream to str. Under text=True the main result
    streams are str, but TimeoutExpired.stdout/.stderr come back as bytes."""
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")
    return value or ""


def _validate_cmd(cmd: list[str]) -> None:
    """Validate argv-list commands before execution.

    Deliberately does NOT reject newlines/CRs in argv elements: `--body`,
    `--description`, and similar flag values legitimately carry multi-line
    markdown (PR comments, attestations, sortition posts -- this exact
    check broke `review_feedback_loop.py`'s sync-pr/reconcile the moment it
    landed, since every attestation/lifecycle comment is multi-line). A
    newline inside one argv element is inert here regardless:
    `subprocess.run` is always called with `shell=False`, so there is no
    shell to reinterpret it. NUL is still rejected -- it truncates C
    strings at the exec layer (CPython already raises ValueError on
    embedded NULs; this just gives an earlier, clearer message from the
    same guard as the rest of this check).
    """
    if not cmd:
        raise ValueError("Command must not be empty")
    if cmd[0] not in _ALLOWED_EXECUTABLES:
        raise ValueError(f"Executable not allowed: {cmd[0]}")
    for part in cmd:
        if not isinstance(part, str):
            raise ValueError("All command arguments must be strings")
        if "\x00" in part:
            raise ValueError("Command arguments must not contain NUL bytes")
    # Shape check LAST: the type/NUL loop above must have run first, so this only ever
    # compares strings. Argument VALUES stay unconstrained — only the verb prefix is pinned.
    if not _command_shape_allowed(cmd[1:]):
        raise ValueError(
            f"gh command shape not allowed: {' '.join(cmd[1:3])!r}. "
            f"Add it to _ALLOWED_GH_PATTERNS if this family is intended."
        )


def run(
    cmd: list[str], check: bool = True, timeout: float | None = 300
) -> subprocess.CompletedProcess[str]:
    """Run ``cmd``, capturing stdout/stderr as text. On a non-zero exit (when
    ``check`` is True), raise ``RuntimeError`` carrying the command and both
    streams so the failure is never silent. ``timeout`` (seconds; ~5 min default)
    guards against a stalled call hanging the workflow indefinitely — a timeout
    raises the same ``RuntimeError`` surface."""
    # `cmd` is argv-list form with shell=False — each element is passed as a literal
    # argument, so there is no shell to inject into. Validate executable + args to
    # prevent uncontrolled command construction across callers.
    _validate_cmd(cmd)
    try:
        result = subprocess.run(  # nosemgrep
            cmd, capture_output=True, text=True, timeout=timeout, check=False
        )
    except subprocess.TimeoutExpired as exc:
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
