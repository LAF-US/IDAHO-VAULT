"""Shared ``gh`` wrapper for the migrated PR and issue automation callers."""
# The first member of the Cluster A redesign shared lib (#600 §5), landed
# independently per #601 item 4. `review_feedback_loop._run`, `pr_lifecycle._run`,
# and `issue_reconciler.gh` were three copies of the same thing: run a command,
# capture stdout/stderr as text, and on a non-zero exit raise a ``RuntimeError``
# carrying the command and both streams. This is that one definition; the engines
# import it instead of each keeping their own.
#
# The run primitive is **private** (``_run``). Migrated callers do not hand it argv — they
# call a typed operation (`pr_edit`, `pr_merge`, `graphql`, `api_pr_files`, …) that
# builds argv here from literal verb and flag tokens, placing caller data only in
# value positions and only after conversion/validation (`str(int(...))` for numbers,
# `_slug` for owner/repo). A caller therefore cannot splice a flag, an option, or a
# second command into the command line, because a caller never writes one. That is
# the fix for "uncontrolled command line": the line is fully controlled by this
# module, and the sink is unreachable from outside it.
#
# Adding a new ``gh`` invocation for these callers means adding a function here, not exporting `_run`.

from __future__ import annotations

import subprocess
import tempfile
from contextlib import contextmanager
from pathlib import Path


# What every operation returns. Callers annotate against this instead of importing
# subprocess themselves — this module is the only one that needs it.
GhResult = subprocess.CompletedProcess[str]

_ALLOWED_EXECUTABLES: set[str] = {"gh"}


def _as_text(value: bytes | str | None) -> str:
    """Normalize a TimeoutExpired stream to str."""
    # Under ``text=True`` the main result streams are str, but
    # ``TimeoutExpired.stdout``/``.stderr`` come back as bytes.
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")
    return value or ""


def _slug(owner: str, repo: str) -> str:
    """Return ``owner/repo``, pinned to the one repository these engines govern."""
    # Every caller here is vault infrastructure for LAF-US/IDAHO-VAULT — the arbiter
    # scripts already refuse to run anywhere else, and the label vocabulary, merge-queue
    # norm and lifecycle states this module encodes are all this repo's. Naming the
    # repository instead of accepting one keeps a mistyped or injected `--owner` from
    # reaching the API at all, rather than reaching it and being wrong.
    if owner not in ("LAF-US",) or repo not in ("IDAHO-VAULT",):
        raise ValueError(
            f"These engines are scoped to LAF-US/IDAHO-VAULT, got: {owner!r}/{repo!r}"
        )
    return f"{owner}/{repo}"


def _num(value: int) -> str:
    """Render an issue or PR number as argv text, rejecting non-numbers."""
    number = int(value)
    if number <= 0:
        raise ValueError(f"Not a valid issue/PR number: {value!r}")
    return str(number)


def _label(name: str) -> str:
    """Return a label name that argv cannot mistake for a flag."""
    # `gh` is Cobra-based: a token starting with ``-`` is parsed as a flag before it is
    # considered as a positional or as a flag's value, so a dash-prefixed label name is
    # not "a label with an odd name" — it is a parse error or, worse, a different
    # command. Empty is rejected for the same reason: it disappears from the argv the
    # reader thinks they wrote.
    if not name or name.startswith("-"):
        raise ValueError(f"Not a valid label name: {name!r}")
    return name


@contextmanager
def _body_file(body: str):
    """Yield a path holding ``body``, so the text never becomes an argv element."""
    # `gh` takes either `--body` or `--body-file`. Comment bodies here are multi-line
    # attestations assembled at runtime, and argv is the wrong carrier for them twice
    # over: `ARG_MAX` truncates a long enough one at the exec layer, and every static
    # analyzer correctly reads caller text in a command line as caller text in a
    # command line. Writing it to a file and passing the path leaves argv holding only
    # tokens this module produced.
    with tempfile.TemporaryDirectory(prefix="gh-cli-body-") as tmp:
        path = Path(tmp) / "body.md"
        path.write_text(body, encoding="utf-8")
        yield str(path)


def _validate_cmd(cmd: list[str]) -> None:
    """Check the argv list this module built before handing it to the exec layer."""
    # Deliberately does NOT reject newlines/CRs in argv elements: `--body`,
    # `--description`, and similar flag values legitimately carry multi-line
    # markdown (PR comments, attestations, sortition posts -- this exact
    # check broke `review_feedback_loop.py`'s sync-pr/reconcile the moment it
    # landed, since every attestation/lifecycle comment is multi-line). A
    # newline inside one argv element is inert here regardless:
    # `subprocess.run` is always called with `shell=False`, so there is no
    # shell to reinterpret it. NUL is still rejected -- it truncates C
    # strings at the exec layer (CPython already raises ValueError on
    # embedded NULs; this just gives an earlier, clearer message from the
    # same guard as the rest of this check).
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
) -> GhResult:
    """Create or update a label. Verb and flags are literals; only values vary."""
    argv = [
        "gh", "label", "create", _label(name),
        "--color", color,
        "--description", description,
    ]
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
) -> GhResult:
    """Add and/or remove one label on a PR. ``pr_number`` is typed int, not text."""
    if add_label is None and remove_label is None:
        raise ValueError("pr_edit requires add_label and/or remove_label")
    argv = ["gh", "pr", "edit", _num(pr_number)]
    if add_label is not None:
        argv += ["--add-label", _label(add_label)]
    if remove_label is not None:
        argv += ["--remove-label", _label(remove_label)]
    return _run(argv, check=check)


def pr_view(
    pr_number: int,
    *,
    json_fields: str,
    owner: str | None = None,
    repo: str | None = None,
    check: bool = True,
) -> GhResult:
    """Read PR fields as JSON. ``json_fields`` is a gh field list, not a shell string."""
    # ``owner`` and ``repo`` are given together or not at all; omitted, gh resolves the
    # repository from the checkout it is run in.
    if (owner is None) != (repo is None):
        raise ValueError("pr_view takes owner and repo together, or neither")
    argv = ["gh", "pr", "view", _num(pr_number)]
    if owner is not None and repo is not None:
        argv += ["--repo", _slug(owner, repo)]
    argv += ["--json", json_fields]
    return _run(argv, check=check)


def pr_comment(
    pr_number: int, body: str, *, check: bool = True
) -> GhResult:
    """Post a PR comment. The body goes via a file, never through argv."""
    with _body_file(body) as path:
        return _run(
            ["gh", "pr", "comment", _num(pr_number), "--body-file", path], check=check
        )


def pr_merge(
    pr_number: int,
    *,
    method: str = "merge",
    auto: bool = False,
    disable_auto: bool = False,
    check: bool = True,
) -> GhResult:
    """Arm or disarm auto-merge. ``method`` is validated against the queue's norm."""
    # K5/#631: the merge queue's configured method is the single norm, and `--merge` is
    # the one canonical inert spelling. Rejecting anything else here keeps a divergent
    # method opinion from being expressible at all, rather than caught later by a test.
    if method != "merge":
        raise ValueError(f"merge method not allowed: {method!r} (the queue's method governs)")
    if auto and disable_auto:
        # Silently letting disable_auto win would leave a caller believing it armed a
        # PR that is now disarmed. Contradictory input is not resolved here, it is
        # refused — the same stance the method check above takes.
        raise ValueError("pr_merge: auto and disable_auto are mutually exclusive")
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
) -> GhResult:
    """List a repository's OPEN PRs as JSON."""
    # Open is the only state this repo's engines census, so it is fixed here rather than
    # parameterized — a state nobody asks for is a value position nobody can misuse.
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
) -> GhResult:
    """Search a repository's OPEN issues, returning the requested JSON fields."""
    # The reconciler's find-or-create is the only caller and only ever looks for an open
    # issue by title, so state and page size are fixed rather than parameterized.
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
) -> GhResult:
    """Read issue fields as JSON."""
    argv = [
        "gh", "issue", "view", _num(issue_number),
        "--repo", _slug(owner, repo),
        "--json", json_fields,
    ]
    return _run(argv, check=check)


def issue_create(
    *, owner: str, repo: str, title: str, body: str, check: bool = True
) -> GhResult:
    """Open a new issue. The body goes via a file this module writes, not argv."""
    with _body_file(body) as path:
        argv = [
            "gh", "issue", "create",
            "--repo", _slug(owner, repo),
            "--title", title,
            "--body-file", path,
        ]
        return _run(argv, check=check)


def issue_comment(
    issue_number: int, *, owner: str, repo: str, body: str, check: bool = True
) -> GhResult:
    """Comment on an issue. The body goes via a file, never through argv."""
    with _body_file(body) as path:
        return issue_comment_file(
            issue_number, owner=owner, repo=repo, body_file=path, check=check
        )


def issue_comment_file(
    issue_number: int, *, owner: str, repo: str, body_file: str, check: bool = True
) -> GhResult:
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
) -> GhResult:
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


def graphql(query: str, **variables: object) -> GhResult:
    """Execute a GraphQL document, passing ints with ``-F`` and everything else with ``-f``."""
    # Returns the raw ``CompletedProcess``; payload and GraphQL-error handling belong
    # to the caller, which knows what shape it asked for.
    argv = ["gh", "api", "graphql", "-f", f"query={query}"]
    for key, value in variables.items():
        if not key.isidentifier():
            raise ValueError(f"Not a valid GraphQL variable name: {key!r}")
        if isinstance(value, bool):
            # `-F` is the typed field, but gh only recognizes lowercase true/false —
            # Python's str(True) is "True", which gh would pass through as the STRING
            # "True" and a `Boolean!` variable would reject. Render it gh's way.
            argv += ["-F", f"{key}={'true' if value else 'false'}"]
        elif isinstance(value, int):
            argv += ["-F", f"{key}={int(value)}"]
        else:
            argv += ["-f", f"{key}={value}"]
    return _run(argv)


def api_pr_update_branch(
    owner: str, repo: str, pr_number: int, *, check: bool = True
) -> GhResult:
    """Merge the base branch into a PR's head (``PUT .../pulls/N/update-branch``)."""
    path = f"repos/{_slug(owner, repo)}/pulls/{_num(pr_number)}/update-branch"
    return _run(["gh", "api", "--method", "PUT", path], check=check)


def api_pr_files(
    owner: str, repo: str, pr_number: int, *, check: bool = True
) -> GhResult:
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
) -> GhResult:
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
) -> GhResult:
    """Run ``cmd``, capturing stdout/stderr as text."""
    # On a non-zero exit (when ``check`` is True), raise ``RuntimeError`` carrying the
    # command and both streams so the failure is never silent. ``timeout`` (seconds;
    # ~5 min default) guards against a stalled call hanging the workflow indefinitely —
    # a timeout raises the same ``RuntimeError`` surface.
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
