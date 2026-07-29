"""
Shared ``gh`` wrapper — the only place in this repo that builds a ``gh`` command line.

The first member of the Cluster A redesign shared lib (#600 §5), landed
independently per #601 item 4. `review_feedback_loop._run`, `pr_lifecycle._run`,
and `issue_reconciler.gh` were three copies of the same thing: run a command,
capture stdout/stderr as text, and on a non-zero exit raise a ``RuntimeError``
carrying the command and both streams. This is that one definition; the engines
import it instead of each keeping their own.

The run primitive is **private** (``_run``). Callers do not hand it argv — they
call a typed operation (`pr_edit`, `pr_merge`, `graphql`, `api_pr_files`, …) that
builds argv here from literal verb and flag tokens, placing caller data only in
value positions and only after conversion/validation (`str(int(...))` for numbers,
`_slug` for owner/repo). A caller therefore cannot splice a flag, an option, or a
second command into the command line, because a caller never writes one. That is
the fix for "uncontrolled command line": the line is fully controlled by this
module, and the sink is unreachable from outside it.

Adding a new ``gh`` invocation means adding a function here, not exporting `_run`.
"""

from __future__ import annotations

import re
import subprocess


_ALLOWED_EXECUTABLES: set[str] = {"gh"}

# GitHub owner and repository names are ASCII word characters plus ``.``, ``-``,
# and ``_``, and every real one contains at least one alphanumeric. Anything else
# is not a name we can have been handed legitimately: a slash or a space would
# restructure the API path, a leading dash would be read as a flag, and a name of
# only dots (``.``, ``..``) would traverse it.
_SLUG_PART = re.compile(r"[A-Za-z0-9_.][A-Za-z0-9_.-]{0,99}")


def _as_text(value: bytes | str | None) -> str:
    """
    Normalize a TimeoutExpired stream to str.

    Under ``text=True`` the main result streams are str, but
    ``TimeoutExpired.stdout``/``.stderr`` come back as bytes.
    """
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")
    return value or ""


def _slug(owner: str, repo: str) -> str:
    """Return ``owner/repo``, rejecting anything that is not a GitHub name."""
    for part in (owner, repo):
        if not _SLUG_PART.fullmatch(part or ""):
            raise ValueError(f"Not a valid GitHub owner/repo name: {part!r}")
        if not any(char.isalnum() for char in part):
            raise ValueError(f"Not a valid GitHub owner/repo name: {part!r}")
    return f"{owner}/{repo}"


def _num(value: int) -> str:
    """Render an issue or PR number as argv text, rejecting non-numbers."""
    number = int(value)
    if number <= 0:
        raise ValueError(f"Not a valid issue/PR number: {value!r}")
    return str(number)


def _validate_cmd(cmd: list[str]) -> None:
    """
    Check the argv list this module built before handing it to the exec layer.

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


# --------------------------------------------------------------------------- #
# Labels
# --------------------------------------------------------------------------- #


def label_create(
    name: str, *, color: str, description: str, force: bool = True, check: bool = True
) -> subprocess.CompletedProcess[str]:
    """Create or update a label. Verb and flags are literals; only values vary."""
    argv = ["gh", "label", "create", name, "--color", color, "--description", description]
    if force:
        argv.append("--force")
    return _run(argv, check=check)


# --------------------------------------------------------------------------- #
# Pull requests
# --------------------------------------------------------------------------- #


def pr_edit(
    pr_number: int,
    *,
    add_label: str | None = None,
    remove_label: str | None = None,
    check: bool = True,
) -> subprocess.CompletedProcess[str]:
    """Add and/or remove one label on a PR. ``pr_number`` is typed int, not text."""
    if add_label is None and remove_label is None:
        raise ValueError("pr_edit requires add_label and/or remove_label")
    argv = ["gh", "pr", "edit", _num(pr_number)]
    if add_label is not None:
        argv += ["--add-label", add_label]
    if remove_label is not None:
        argv += ["--remove-label", remove_label]
    return _run(argv, check=check)


def pr_view(
    pr_number: int,
    *,
    json_fields: str,
    owner: str | None = None,
    repo: str | None = None,
    check: bool = True,
) -> subprocess.CompletedProcess[str]:
    """
    Read PR fields as JSON. ``json_fields`` is a gh field list, not a shell string.

    ``owner`` and ``repo`` are given together or not at all; omitted, gh resolves the
    repository from the checkout it is run in.
    """
    if (owner is None) != (repo is None):
        raise ValueError("pr_view takes owner and repo together, or neither")
    argv = ["gh", "pr", "view", _num(pr_number)]
    if owner is not None and repo is not None:
        argv += ["--repo", _slug(owner, repo)]
    argv += ["--json", json_fields]
    return _run(argv, check=check)


def pr_comment(
    pr_number: int, body: str, *, check: bool = True
) -> subprocess.CompletedProcess[str]:
    """Post a PR comment. ``body`` is one argv element — multi-line markdown is fine."""
    return _run(["gh", "pr", "comment", _num(pr_number), "--body", body], check=check)


def pr_merge(
    pr_number: int,
    *,
    method: str = "merge",
    auto: bool = False,
    disable_auto: bool = False,
    check: bool = True,
) -> subprocess.CompletedProcess[str]:
    """
    Arm or disarm auto-merge. ``method`` is validated against the queue's norm.

    K5/#631: the merge queue's configured method is the single norm, and `--merge` is
    the one canonical inert spelling. Rejecting anything else here keeps a divergent
    method opinion from being expressible at all, rather than caught later by a test.
    """
    if method != "merge":
        raise ValueError(f"merge method not allowed: {method!r} (the queue's method governs)")
    argv = ["gh", "pr", "merge", _num(pr_number)]
    if disable_auto:
        argv.append("--disable-auto")
    else:
        argv.append(f"--{method}")
        if auto:
            argv.append("--auto")
    return _run(argv, check=check)


def pr_list_open(
    owner: str,
    repo: str,
    *,
    limit: int = 1000,
    json_fields: str = "number",
    check: bool = True,
) -> subprocess.CompletedProcess[str]:
    """
    List a repository's OPEN PRs as JSON.

    Open is the only state this repo's engines census, so it is fixed here rather than
    parameterized — a state nobody asks for is a value position nobody can misuse.
    """
    argv = [
        "gh", "pr", "list",
        "--repo", _slug(owner, repo),
        "--state", "open",
        "--limit", str(int(limit)),
        "--json", json_fields,
    ]
    return _run(argv, check=check)


# --------------------------------------------------------------------------- #
# Issues
# --------------------------------------------------------------------------- #


ISSUE_SEARCH_LIMIT = 20


def issue_search_open(
    owner: str, repo: str, *, search: str, json_fields: str, check: bool = True
) -> subprocess.CompletedProcess[str]:
    """
    Search a repository's OPEN issues, returning the requested JSON fields.

    The reconciler's find-or-create is the only caller and only ever looks for an open
    issue by title, so state and page size are fixed rather than parameterized.
    """
    argv = [
        "gh", "issue", "list",
        "--repo", _slug(owner, repo),
        "--state", "open",
        "--search", search,
        "--json", json_fields,
        "--limit", str(ISSUE_SEARCH_LIMIT),
    ]
    return _run(argv, check=check)


def issue_view(
    issue_number: int, *, owner: str, repo: str, json_fields: str, check: bool = True
) -> subprocess.CompletedProcess[str]:
    """Read issue fields as JSON."""
    argv = [
        "gh", "issue", "view", _num(issue_number),
        "--repo", _slug(owner, repo),
        "--json", json_fields,
    ]
    return _run(argv, check=check)


def issue_create(
    *, owner: str, repo: str, title: str, body_file: str, check: bool = True
) -> subprocess.CompletedProcess[str]:
    """Open a new issue whose body is read from ``body_file``."""
    argv = [
        "gh", "issue", "create",
        "--repo", _slug(owner, repo),
        "--title", title,
        "--body-file", body_file,
    ]
    return _run(argv, check=check)


def issue_comment(
    issue_number: int, *, owner: str, repo: str, body: str, check: bool = True
) -> subprocess.CompletedProcess[str]:
    """Comment on an issue with an inline body — one argv element, multi-line is fine."""
    argv = [
        "gh", "issue", "comment", _num(issue_number),
        "--repo", _slug(owner, repo),
        "--body", body,
    ]
    return _run(argv, check=check)


def issue_comment_file(
    issue_number: int, *, owner: str, repo: str, body_file: str, check: bool = True
) -> subprocess.CompletedProcess[str]:
    """Comment on an issue with a body read from ``body_file``."""
    argv = [
        "gh", "issue", "comment", _num(issue_number),
        "--repo", _slug(owner, repo),
        "--body-file", body_file,
    ]
    return _run(argv, check=check)


def issue_close(
    issue_number: int,
    *,
    owner: str,
    repo: str,
    reason: str = "completed",
    check: bool = True,
) -> subprocess.CompletedProcess[str]:
    """Close an issue with one of gh's own close reasons."""
    if reason not in {"completed", "not planned"}:
        raise ValueError(f"Not a valid close reason: {reason!r}")
    argv = [
        "gh", "issue", "close", _num(issue_number),
        "--repo", _slug(owner, repo),
        "--reason", reason,
    ]
    return _run(argv, check=check)


# --------------------------------------------------------------------------- #
# API — GraphQL and the handful of REST endpoints gh has no porcelain for
# --------------------------------------------------------------------------- #


def graphql(query: str, **variables: object) -> subprocess.CompletedProcess[str]:
    """
    Execute a GraphQL document, passing ints with ``-F`` and everything else with ``-f``.

    Returns the raw ``CompletedProcess``; payload and GraphQL-error handling belong
    to the caller, which knows what shape it asked for.
    """
    argv = ["gh", "api", "graphql", "-f", f"query={query}"]
    for key, value in variables.items():
        if not key.isidentifier():
            raise ValueError(f"Not a valid GraphQL variable name: {key!r}")
        if isinstance(value, int) and not isinstance(value, bool):
            argv += ["-F", f"{key}={int(value)}"]
        else:
            argv += ["-f", f"{key}={value}"]
    return _run(argv)


def api_pr_update_branch(
    owner: str, repo: str, pr_number: int, *, check: bool = True
) -> subprocess.CompletedProcess[str]:
    """Merge the base branch into a PR's head (``PUT .../pulls/N/update-branch``)."""
    path = f"repos/{_slug(owner, repo)}/pulls/{_num(pr_number)}/update-branch"
    return _run(["gh", "api", "--method", "PUT", path], check=check)


def api_pr_files(
    owner: str, repo: str, pr_number: int, *, check: bool = True
) -> subprocess.CompletedProcess[str]:
    """List a PR's changed file paths, one per line, across every page."""
    path = f"repos/{_slug(owner, repo)}/pulls/{_num(pr_number)}/files"
    return _run(["gh", "api", "--paginate", path, "--jq", ".[].filename"], check=check)


def api_issue_comments(
    owner: str,
    repo: str,
    issue_number: int,
    *,
    jq: str | None = None,
    check: bool = True,
) -> subprocess.CompletedProcess[str]:
    """Read an issue's (or PR's) issue-style comments across every page."""
    path = f"repos/{_slug(owner, repo)}/issues/{_num(issue_number)}/comments"
    argv = ["gh", "api", "--paginate", path]
    if jq is not None:
        argv += ["--jq", jq]
    return _run(argv, check=check)


# --------------------------------------------------------------------------- #
# The run primitive — private on purpose; see the module docstring
# --------------------------------------------------------------------------- #


def _run(
    cmd: list[str], check: bool = True, timeout: float | None = 300
) -> subprocess.CompletedProcess[str]:
    """
    Run ``cmd``, capturing stdout/stderr as text.

    On a non-zero exit (when ``check`` is True), raise ``RuntimeError`` carrying the
    command and both streams so the failure is never silent. ``timeout`` (seconds;
    ~5 min default) guards against a stalled call hanging the workflow indefinitely —
    a timeout raises the same ``RuntimeError`` surface.
    """
    # `cmd` is an argv list this module built from literal tokens, run with shell=False:
    # each element is passed as a literal argument, so there is no shell to inject into
    # and no caller-supplied flag can appear. _validate_cmd re-checks that invariant.
    _validate_cmd(cmd)
    try:
        result = subprocess.run(
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
