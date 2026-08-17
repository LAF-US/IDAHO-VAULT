#!/usr/bin/env python3
"""Verify every external GitHub Action reference is pinned to a full commit SHA.

Structural replacement for the workflow-action-pin branch of the deleted
VERSION-TRANSITIONS.md ledger: floating tags (``@v4``, ``@main``) are a
worm-watch supply-chain risk because the upstream owner can repoint them to
malicious content after the fact (see PR #378, which SHA-pinned every action
in this repo). Rather than asking a human to remember to check this on every
workflow edit, this derives and verifies it directly from the tracked files.
"""

from __future__ import annotations

import errno
import os
import re
import sys
from pathlib import Path


def _repo_root() -> Path:
    # In CI this script executes from the trusted base-branch checkout
    # (trusted-main/), while the content under test is the PRIMARY checkout —
    # which is exactly the run step's working directory: every policy workflow
    # invokes this script with cwd at the primary checkout and never sets a
    # working-directory override. Using the process cwd keeps the
    # trusted-validator split (trusted code, PR-head content) without deriving
    # any filesystem path from environment data — there is no tainted-path
    # flow left for a scanner to model, and no hard-coded runner path to break
    # on self-hosted runners or a repo rename. Local (pre-commit) runs fall
    # back to the script's own repository.
    if os.environ.get("GITHUB_ACTIONS") == "true":
        return Path.cwd()
    return Path(__file__).resolve().parents[2]


REPO_ROOT = _repo_root()
WORKFLOW_GLOBS = (".github/workflows/*.yml", ".github/workflows/*.yaml")
# GitHub's composite-action convention: exactly action.yml or action.yaml at
# the action's root (never a different filename), matched explicitly rather
# than "any *.yml" to avoid both false coverage of unrelated files and any
# ambiguity about whether the standard filenames are actually scanned.
# Recursive: a nested action (.github/actions/vendor/pr-agent/action.yml) is
# just as capable of naming a mutable image as a top-level one. Discovery uses
# an explicit no-follow walk so PR-controlled symlink directories cannot expand
# or stall the scan before the per-file read guard runs.
ACTION_NAMES = ("action.yml", "action.yaml")

# Capture the whole value, not `\S+`. A value containing spaces —
# `uses: ${{ matrix.action }}` — failed to match the old pattern at all, and an
# unmatched line was treated as safe. Anything this guard cannot resolve to a
# literal must be reported, not skipped.
# The key may be quoted, exactly as for `image:` below.
USES_PATTERN = re.compile(r"""^\s*(?:-\s*)?["']?uses["']?\s*:\s*(.+?)\s*$""")
# A `uses` key in FLOW position — `- { uses: actions/checkout@… }`, or inside
# `steps: [{uses: …}]`. Valid YAML, valid Actions, and invisible to the
# line-oriented pattern above, which would have skipped it as safe. Anchored on
# `{` or `,` so it cannot fire on the word appearing inside a quoted scalar
# (`- name: "Check every workflow/action uses: a full commit SHA"` is a real
# line in this repo and is not a `uses` key).
FLOW_USES_PATTERN = re.compile(r"""[{,]\s*["']?uses["']?\s*:""")
EXPRESSION_PATTERN = re.compile(r"\$\{\{")
FULL_SHA_PATTERN = re.compile(r"^[0-9a-f]{40}$")

# A `uses:` SHA pins the repository, not the container that repository builds.
# A Docker action can name its image directly, and a tag there is mutable —
# which is exactly how `the-pr-agent/pr-agent` slipped a mutable
# `pragent/pr-agent:github_action` past a 40-char pin (see
# .github/actions/pr-agent/action.yml). So `image:` gets checked too, and for a
# digest rather than a SHA: registries address content by sha256, not by commit.
# The key may be quoted (`"image": …`) — YAML treats that as the same key, so a
# pattern anchored on a bare `image:` would not see it.
IMAGE_PATTERN = re.compile(r"""^\s*["']?image["']?\s*:\s*(.+?)\s*$""")
IMAGE_DIGEST_PATTERN = re.compile(r"@sha256:[0-9a-f]{64}$")
WORKFLOW_CONTAINER_PATTERN = re.compile(r"""^\s*["']?container["']?\s*:\s*(.+?)\s*$""")
WORKFLOW_SERVICES_PATTERN = re.compile(r"""^\s*["']?services["']?\s*:\s*(.+?)\s*$""")
# `runs.using: docker` declares a container action, in block or flow form, with
# either key quoted. Used to fail CLOSED: if a file says it runs a container and
# this line-oriented reader found no `image:` line, the image is unverified —
# not absent. `runs: {using: docker, image: "docker://alpine:latest"}` is valid
# metadata that puts the image mid-line, where IMAGE_PATTERN cannot reach it.
DOCKER_ACTION_PATTERN = re.compile(
    r"""["']?using["']?\s*:\s*["']?docker["']?""", re.IGNORECASE
)
# `runs:` is a TOP-LEVEL key in action metadata — but "top-level" is not the
# same as "column 0". YAML lets a whole block mapping carry a uniform indent,
# so `  runs: {using: docker, image: "docker://alpine:latest"}` under `  name:`
# is a valid action file whose container this guard reported as OK: anchored at
# column 0, the pattern never matched, and the flow form put the image where
# IMAGE_PATTERN could not see it either. Indentation is not a security
# boundary. So match at any indent and scope by comparing against the
# document's own root indent, which is what actually distinguishes the real
# `runs:` from one nested under another key.
RUNS_PATTERN = re.compile(r"""^(\s*)["']?runs["']?\s*:\s*(.*?)\s*$""")
# A `runs` key in FLOW position — `{name: x, runs: {using: docker, …}}` as a
# whole-document mapping. Same fail-closed treatment as FLOW_USES_PATTERN, and
# for the same reason: no line-oriented pattern can read the image out of it.
FLOW_RUNS_PATTERN = re.compile(r"""[{,]\s*["']?runs["']?\s*:""")
# Dockerfile `FROM` instructions are parsed by `_from_instruction()` rather
# than a repeated-token regular expression: the guard accepts only the small
# grammar it can verify, while avoiding regex backtracking on PR-supplied text.


def scan_targets() -> list[Path]:
    """Workflow files and action metadata, without following symlink directories."""

    paths: list[Path] = []
    for pattern in WORKFLOW_GLOBS:
        paths.extend(sorted(REPO_ROOT.glob(pattern)))

    actions_root = REPO_ROOT / ".github" / "actions"
    if actions_root.is_symlink():
        paths.append(actions_root)
    elif actions_root.is_dir():
        for root, directories, filenames in os.walk(
            actions_root, topdown=True, followlinks=False
        ):
            base = Path(root)
            safe_directories: list[str] = []
            for name in sorted(directories):
                candidate = base / name
                if candidate.is_symlink():
                    paths.append(candidate)
                else:
                    safe_directories.append(name)
            directories[:] = safe_directories

            for name in ACTION_NAMES:
                candidate = base / name
                if name in filenames or candidate.is_symlink():
                    paths.append(candidate)
    # Deduplicated: a DIRECTORY symlink named `action.yml` satisfies both loops
    # above — the directory pass appends it as an unfollowable link, and the
    # name pass appends it again as action metadata. `main()` happens to absorb
    # the repeat (its `seen` set is written before any finding is), so no
    # duplicate reaches the output today; this keeps the returned list honest
    # for any other caller, which has no such set to hide behind.
    return sorted(set(paths))


# O_NOFOLLOW is Unix-only, and this vault is edited on Windows (see
# `.claude/CLAUDE.md` § Windows Operation — nothing here may require Unix).
# Naming it directly raises AttributeError there, so the guard would crash on
# the machine it is most often run from by hand. Absent, the flag degrades to
# 0: the open stops refusing symlinks by itself, so `_open_by_name()` checks
# afterwards what it actually opened. `_readable()` still rejects a symlink
# already in place either way.
O_NOFOLLOW = getattr(os, "O_NOFOLLOW", 0)
# The errno `open()` reports for O_NOFOLLOW against a symlink: ELOOP on Linux
# and macOS, EMLINK on FreeBSD, which documents exactly this case in open(2).
# Keeping both is not superstition. It also cannot mislead on Linux, where
# open() has no EMLINK outcome at all — that errno belongs to link() exceeding
# a directory's link count, which is not a path this function can reach.
SYMLINK_REFUSED = (errno.ELOOP, errno.EMLINK)
# Descending by descriptor needs dir_fd, which is Unix-only like the flag
# above. Where it is missing the walk collapses to a single open and the
# ancestor components go unchecked — stated in `_open_by_name()`, not papered
# over.
DIR_FD_SUPPORTED = os.open in os.supports_dir_fd


SWAPPED = "became a symlink after the safety check; not read"


def _unreadable(exc: OSError, name: str = "", dir_fd: int | None = None) -> str:
    """One phrasing for a failed open, so the paths below cannot drift.

    O_NOFOLLOW refusing a symlink is ELOOP on its own. But the ancestor opens
    also pass O_DIRECTORY, and against a symlink-to-directory Linux answers
    ENOTDIR first: the unfollowed link is indeed not a directory, which is true
    and says nothing about why. Reported verbatim that describes a DETECTED
    SWAP as an ordinary broken path — the read is refused either way, so
    nothing unsafe follows, but the guard would be naming the wrong thing about
    its own finding, which is the failure this whole file is being corrected
    for. So on the errno that can mean either, ask what the component actually
    is: readlink answers only for a link.
    """
    if exc.errno in SYMLINK_REFUSED:
        return SWAPPED
    if exc.errno == errno.ENOTDIR and name and dir_fd is not None:
        try:
            os.readlink(name, dir_fd=dir_fd)
            return SWAPPED
        except (OSError, NotImplementedError):
            pass
    return f"not readable ({exc.strerror or exc}); cannot verify pins"


def _open_no_follow(path: Path) -> tuple[int | None, str]:
    """A descriptor for `path`, or (None, reason) if it may not be opened.

    Separate from the decode below because they answer different questions:
    this one is about WHICH OBJECT the name refers to right now, and whether
    that object may be read at all; `_read()` is about what its bytes mean.
    Keeping them in one body put two unrelated error vocabularies in the same
    function, which is the shape this file has been pulling apart throughout.
    """
    if DIR_FD_SUPPORTED and O_NOFOLLOW:
        return _open_by_descriptor_walk(path)
    return _open_by_name(path)


def _open_by_descriptor_walk(path: Path) -> tuple[int | None, str]:
    """Descend from the repository root, one component at a time.

    A flag on the final open alone is not enough. O_NOFOLLOW refuses a symlink
    in the LAST position and says nothing about the ones above it, so replacing
    an ANCESTOR directory after the check still resolved outside the
    repository. Demonstrated the same way as the file swap: validate
    `.github/actions/x/action.yml`, replace the `x` directory with a link to a
    directory outside the repository, read, and the outside file's content came
    back with the final open's O_NOFOLLOW entirely satisfied — the last
    component really was a regular file, just not the one that was checked.

    Descending from a held descriptor means each component is refused as it is
    used, and once a directory descriptor is held there is no name left behind
    us for anyone to repoint. Chosen only when BOTH `dir_fd` and a real
    O_NOFOLLOW are present: descending without the flag would open each
    component following links, which is the very thing this exists to stop, and
    it would do it while looking like the strong path. `_open_by_name()` is
    weaker but says so.
    """
    try:
        relative = path.relative_to(REPO_ROOT)
    except ValueError:
        return None, "resolves outside the repository; not read"
    if not relative.parts:
        return None, "is the repository root, not a file; not read"
    # `relative_to` compares SPELLINGS. It is satisfied by
    # `<root>/.github/../../elsewhere.yml` — lexically under the root, and the
    # walk would then open `.github`, climb through two `..` components, and
    # read a file outside the repository, with O_NOFOLLOW raising nothing
    # because `..` is not a symlink. Reproduced before this line existed:
    # outside content came back from a path the containment check had passed.
    # Callers reach here through `_readable()`, which resolves first, so no
    # real path carries these today — but the function above returns
    # "resolves outside the repository" on its own authority, and a claim this
    # function makes is one it has to keep.
    if not set(relative.parts).isdisjoint({os.pardir, os.curdir}):
        return None, "resolves outside the repository; not read"

    directory = os.open(REPO_ROOT, os.O_RDONLY | os.O_DIRECTORY)
    try:
        for part in relative.parts[:-1]:
            try:
                step = os.open(
                    part, os.O_RDONLY | os.O_DIRECTORY | O_NOFOLLOW, dir_fd=directory
                )
            except OSError as exc:
                return None, _unreadable(exc, part, directory)
            # Rebound BEFORE the close, not after. The other order leaves a
            # window — an interrupt between the two statements — where `step`
            # is open with nothing holding it and `directory` names a
            # descriptor that has just been closed, which `finally` would then
            # close again. A stale close is not harmless: descriptor numbers
            # are reused, so it can shut something else's file.
            directory, previous = step, directory
            os.close(previous)
        leaf = relative.parts[-1]
        try:
            return os.open(leaf, os.O_RDONLY | O_NOFOLLOW, dir_fd=directory), ""
        except OSError as exc:
            return None, _unreadable(exc, leaf, directory)
    finally:
        os.close(directory)


def _open_by_name(path: Path) -> tuple[int | None, str]:
    """The degraded path: no dir_fd, so no walk. Windows takes this branch.

    Both defences above are Unix-only, and they fail QUIETLY here: `dir_fd` is
    absent so nothing descends, and O_NOFOLLOW is 0 so the open follows a link
    it was supposed to refuse. Saying "Unix-strength only" in a comment and
    leaving the open bare would make the docstring on `_read()` a claim this
    branch does not keep.

    So the identity of what was opened is checked against the identity the NAME
    still denotes. `lstat` does not follow the final component, so a link
    swapped into that position reports the link's own inode, which cannot match
    the target the descriptor is holding — the swap is caught after the fact
    and the read is refused. What this does NOT recover is the ancestor case:
    both calls follow intermediate directories, so a replaced ancestor agrees
    with itself. That half stays open off Unix, and is stated rather than
    implied.

    The suite cannot assert any of this from Linux, where the branch is not
    taken, so it was checked by hand instead: with both constants above forced
    to their Windows values, the swap probe reads the outside file when the
    comparison below is removed and is refused when it is present.
    """
    try:
        descriptor = os.open(path, os.O_RDONLY | O_NOFOLLOW)
    except OSError as exc:
        return None, _unreadable(exc)
    try:
        opened = os.fstat(descriptor)
        named = os.lstat(path)
    except OSError as exc:
        os.close(descriptor)
        return None, _unreadable(exc)
    if (opened.st_dev, opened.st_ino) != (named.st_dev, named.st_ino):
        os.close(descriptor)
        return None, SWAPPED
    return descriptor, ""


def _read(path: Path) -> tuple[str | None, str]:
    """The file's text, or (None, reason) when it cannot be decoded or read.

    `read_text(encoding="utf-8")` raises UnicodeDecodeError on bytes that are
    not UTF-8, and this guard runs against PR-head content, so a planted
    non-UTF-8 action.yml crashed it with a traceback instead of producing a
    finding. A guard that dies is not a guard that failed closed: the job
    still goes red, but it names a Python error rather than the file.

    Opened by `_open_no_follow()` rather than by name, because `_readable()`
    checks a PATH and this opens one — two operations on a name, with a window
    between them where the name can be repointed. `_readable()`'s own docstring
    claimed that window was closed; it was only narrowed. Demonstrated: verify
    a regular file inside the repository, replace it with a symlink to a file
    outside, read here, and content from outside the repository lands in the
    findings.

    How much of that window `_open_no_follow()` actually closes depends on the
    platform, and the two branches there say which is which. On Unix — where
    this gates anything, since CI is Linux — the whole path is descended by
    descriptor and every component is refused, so the check and the read cannot
    disagree about which object they mean. Where `dir_fd` is missing the final
    component is still caught, by identity rather than by flag, and a replaced
    ancestor is not. Neither branch is silently weaker than its docstring.
    """
    descriptor, reason = _open_no_follow(path)
    if descriptor is None:
        return None, reason
    try:
        with os.fdopen(descriptor, encoding="utf-8-sig") as handle:
            return handle.read(), ""
    except UnicodeDecodeError:
        return None, "not valid UTF-8; cannot verify pins"
    except OSError as exc:
        return None, f"not readable ({exc.strerror or exc}); cannot verify pins"


def unpinned_refs(path: Path, text: str) -> list[tuple[int, str]]:
    """Every unpinned reference in one file: `uses:`, `image:`, and metadata.

    Three separate scans, kept as three functions. As one they were a single
    15-branch body doing unrelated work, which is what Codacy, Revieko and
    Repowise were each pointing at from different angles.
    """
    lines = text.splitlines()
    return [
        *_uses_findings(lines),
        *_image_findings(path, lines),
        *_workflow_inline_image_findings(path, lines),
        *_unreadable_docker_metadata(path, lines),
    ]


def _uses_findings(lines: list[str]) -> list[tuple[int, str]]:
    """`uses:` refs that are not pinned to a full 40-char commit SHA."""
    findings: list[tuple[int, str]] = []
    for lineno, line in enumerate(lines, start=1):
        match = USES_PATTERN.match(line)
        if not match:
            # Fail closed on the flow form rather than skip it, the same way
            # `runs: {using: docker, image: …}` is handled below: a `uses` key
            # this reader cannot resolve is unverified, not absent.
            if FLOW_USES_PATTERN.search(_outside_strings(line)):
                findings.append(
                    (
                        lineno,
                        (
                            "uses: in a flow mapping "
                            "(unsupported YAML form; ref unverified)"
                        ),
                    )
                )
            continue
        ref = _scalar(match.group(1))
        if EXPRESSION_PATTERN.search(ref):
            findings.append(
                (lineno, f"{ref} (expression; cannot be resolved to a pinned ref)")
            )
            continue
        if ref.startswith("./"):
            continue
        if ref.startswith("docker://"):
            # Skipped as a `uses:` ref, but still a container: hold it to the
            # same digest rule as an `image:` line rather than waving it past.
            if not IMAGE_DIGEST_PATTERN.search(ref):
                findings.append((lineno, f"{ref} (docker ref needs @sha256:<64 hex>)"))
            continue
        if "@" not in ref:
            findings.append((lineno, ref))
            continue
        _, _, sha = ref.rpartition("@")
        if not FULL_SHA_PATTERN.match(sha):
            findings.append((lineno, ref))
    return findings


def _image_findings(path: Path, lines: list[str]) -> list[tuple[int, str]]:
    """`image:` values that name a mutable container or an unverified build."""
    findings: list[tuple[int, str]] = []
    for lineno, line in enumerate(lines, start=1):
        match = IMAGE_PATTERN.match(line)
        if not match:
            continue
        image = _scalar(match.group(1))
        if EXPRESSION_PATTERN.search(image):
            findings.append(
                (lineno, f"{image} (expression; cannot be resolved to a digest)")
            )
            continue
        if _looks_like_dockerfile(image, path):
            # NOT a free pass. `image: Dockerfile.github_action_dockerhub` is
            # how the original hole worked: a repository SHA freezes the
            # Dockerfile TEXT, and that text says `FROM <mutable tag>`, which
            # resolves at build time to whatever the tag points at today. So
            # follow the file and hold its FROM lines to the digest rule.
            findings.extend(_unpinned_from_lines(path, image, lineno))
            continue
        if not IMAGE_DIGEST_PATTERN.search(image):
            findings.append((lineno, f"{image} (image needs @sha256:<64 hex>)"))
    return findings


def _workflow_inline_image_findings(
    path: Path, lines: list[str]
) -> list[tuple[int, str]]:
    """Fail closed on workflow container/service images hidden in inline YAML."""

    if path.parent != REPO_ROOT / ".github" / "workflows":
        return []

    findings: list[tuple[int, str]] = []
    for lineno, line in enumerate(lines, start=1):
        container = WORKFLOW_CONTAINER_PATTERN.match(line)
        if container:
            image = _scalar(container.group(1))
            if image.startswith("{"):
                findings.append(
                    (lineno, "inline container mapping; image digest unverified")
                )
            elif not IMAGE_DIGEST_PATTERN.search(image):
                findings.append(
                    (lineno, f"{image} (container image needs @sha256:<64 hex>)")
                )
            continue

        services = WORKFLOW_SERVICES_PATTERN.match(line)
        if services and _scalar(services.group(1)) not in ("{}", "[]"):
            findings.append(
                (lineno, "inline services mapping; image digests unverified")
            )
    return findings


def _container_runs_without_readable_image(block: list[str]) -> bool:
    """Whether a `runs:` block names a Docker action but no readable image line."""
    code = [line for line in block if not line.lstrip().startswith("#")]
    return any(DOCKER_ACTION_PATTERN.search(line) for line in code) and not any(
        IMAGE_PATTERN.match(line) for line in code
    )


def _unreadable_docker_metadata(path: Path, lines: list[str]) -> list[tuple[int, str]]:
    """Fail closed when a container action's `image:` is out of this reader's reach.

    Everything above is line-oriented, and an unmatched line was being treated
    as safe. But `runs: {using: docker, image: "docker://alpine:latest"}` is
    valid action metadata that runs exactly the same mutable container, with the
    `image:` mid-line where no `^image:` pattern can see it. Reporting OK there
    is the guard saying "verified" about something it never read.

    So: if the file declares `using: docker` and no `image:` line was matched,
    that is a finding. A `using: composite`/`node20` action names no image and
    is not implicated.

    Every candidate `runs:` is judged, not just the first. Returning on the
    first match assumed there is exactly one, which holds for the real
    top-level key and not for the fallback below, where a composite `runs:`
    seen first would have excused a docker one seen second.
    """
    if path.name not in ("action.yml", "action.yaml"):
        # `runs.using` is action metadata. A workflow has no such key, and
        # scanning for one there would only invent findings.
        return []
    root = _root_indent(lines)
    findings: list[tuple[int, str]] = []
    for lineno, line in enumerate(lines, start=1):
        if FLOW_RUNS_PATTERN.search(_outside_strings(line)):
            findings.append((lineno, "runs: in a flow mapping (image unverified)"))
            continue
        match = RUNS_PATTERN.match(line)
        # `root is None` means the document is not a plain block mapping and
        # this reader cannot say which `runs:` is the real one — so consider
        # every one of them rather than none.
        if not match or (root is not None and match.group(1) != root):
            continue
        block = _block_at(lines, lineno, match.group(1))
        if not _container_runs_without_readable_image(block):
            # Composite / node20 actions name no image, and a block image is
            # already handled by `_image_findings()`.
            continue
        findings.append(
            (
                lineno,
                (
                    "runs.using: docker with no `image:` line this guard can read "
                    "(flow mapping or other unsupported YAML form; image unverified)"
                ),
            )
        )
    return findings


def _root_indent(lines: list[str]) -> str | None:
    """The indentation of the document's top-level keys, or None if not plain.

    YAML requires every key of a mapping to sit at the same indent, so the
    first content line of a block-mapping document fixes it for the whole root
    level — which is what makes `  runs:` a top-level key in one file and a
    nested one in another. A document that opens with a flow mapping, an
    anchor, a directive or a sequence is not a plain block mapping; returning
    None there means "cannot scope", and the caller widens rather than skips.
    """
    for line in lines:
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or stripped in ("---", "..."):
            continue
        if stripped[0] in "{[%-&*!|>":
            return None
        return line[: len(line) - len(line.lstrip())]
    return None


def _block_at(lines: list[str], lineno: int, indent: str) -> list[str]:
    """A key's line plus everything nested under it.

    Scoping matters: asking whether the FILE contains any `image:` line let a
    decoy elsewhere vouch for an image the guard never read. An action
    declaring a digest-pinned image under `inputs`, and its real container as a
    flow-mapping `runs` on the next line, reported OK with the mutable
    container unexamined — the decoy satisfied the test. Only an image named
    inside `runs` can be the one that runs.
    """
    block = [lines[lineno - 1]]
    for follow in lines[lineno:]:
        if not follow.strip():
            block.append(follow)
            continue
        if len(follow) - len(follow.lstrip()) <= len(indent):
            break
        block.append(follow)
    return block


def _outside_strings(line: str) -> str:
    """The line with quoted scalars and any comment removed.

    FLOW_USES_PATTERN keys off `{` or `,`, and both are ordinary characters
    inside a YAML string, so matching the raw line invents findings:
    `- name: "step, uses: something"` contains `, uses:` and would fail CI on
    a step whose name happens to hold a comma, and `key: v  # {uses: x}` would
    fail on a comment describing the very form being rejected. Both were
    checked and both matched before this. Quoted spans go first so that a `#`
    inside a string is not read as starting a comment.

    The `(?!\\s*:)` is load-bearing, not tidiness. Stripping EVERY quoted span
    also deleted quoted KEYS, so `- {'uses': actions/checkout@v4}` lost the
    very token FLOW_USES_PATTERN looks for and sailed through unreported — the
    comma fix reopened, in the flow form, exactly the hole the flow check was
    added to close. A quoted span followed by `:` is a key and survives; one
    that is not is a value and goes.
    """
    without_strings = re.sub(r"""('[^']*'|"[^"]*")(?!\s*:)""", "", line)
    return re.split(r"(?:^|\s)#", without_strings, maxsplit=1)[0]


def _scalar(raw: str) -> str:
    """The literal value of a `uses:`/`image:` line, minus trailing comment.

    Only a comment introduced by whitespace is stripped, so a `#` inside the
    value survives. Digests and action refs contain no `#`, so this is exact
    for everything the guard evaluates.
    """
    value = re.split(r"\s+#", raw, maxsplit=1)[0].strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        value = value[1:-1]
    return value


def _escape_char(lines: list[str]) -> str:
    """The Dockerfile's escape character, per its `# escape=` parser directive.

    Docker stops looking for parser directives at the first blank line,
    instruction, or comment that is not itself a directive. Skipping blanks and
    reading past ordinary comments honoured an `# escape=` Docker would ignore,
    joined continuations with the wrong character, and so missed the FROM — a
    false negative in a supply-chain guard. `# syntax=` before `# escape=` is
    fine: both are directives, so the scan continues through it.
    """
    for line in lines:
        stripped = line.strip()
        if not stripped.startswith("#"):
            return "\\"
        directive = re.match(
            r"#\s*(syntax|escape|check)\s*=\s*(\S+)\s*$",
            stripped,
            re.IGNORECASE,
        )
        if not directive:
            return "\\"
        if directive.group(1).lower() == "escape":
            return directive.group(2) if directive.group(2) in ("\\", "`") else "\\"
    return "\\"


def _logical_lines(text: str) -> list[tuple[int, str]]:
    """Dockerfile instructions with continuations joined.

    `FROM alpine:latest \\` + `AS build` is one instruction to Docker and two
    physical lines to a regex, so matching physical lines skipped the base
    entirely — fail-open on a mutable image. Honours the `# escape=` parser
    directive, which may only appear before any instruction and only sets `\\`
    or a backtick.
    """
    lines = text.splitlines()
    escape = _escape_char(lines)

    out: list[tuple[int, str]] = []
    buffer = ""
    start = 0
    for lineno, line in enumerate(lines, start=1):
        # A comment carries no instruction, and must not be treated as
        # continued — the `# escape=\`` directive line ends with the escape
        # character itself, which would otherwise swallow the FROM after it.
        if not buffer and line.strip().startswith("#"):
            continue
        if not buffer:
            start = lineno
        body = line
        continued = body.rstrip().endswith(escape)
        if continued:
            body = body.rstrip()[: -len(escape)]
        buffer = f"{buffer} {body.strip()}" if buffer else body.strip()
        if not continued:
            out.append((start, buffer))
            buffer = ""
    if buffer:
        out.append((start, buffer))
    return out


def _from_instruction(line: str) -> tuple[str, str | None] | None:
    """Return the base image and optional stage from one supported FROM instruction.

    Docker permits leading `--flag=value` tokens before the base image. The
    guard deliberately rejects forms it cannot identify exactly rather than
    applying a permissive regular expression to untrusted Dockerfile text.
    """
    words = line.split()
    if not words or words[0].upper() != "FROM":
        return None
    words = words[1:]
    while words and words[0].startswith("--"):
        words.pop(0)
    if not words:
        return None
    base = words.pop(0)
    if not words:
        return base, None
    if len(words) == 2 and words[0].upper() == "AS":
        return base, words[1]
    return None


def _resolve_in_repo(base: Path, rel: str) -> Path | None:
    """Resolve `rel` against `base`, refusing anything outside the repository.

    These paths come out of YAML that lives in the repo, so this is not a trust
    boundary in the usual sense. It is still wrong for a guard to be pointable
    at an arbitrary file by an `image:` line — `image: ../../../../etc/passwd`
    satisfies the Dockerfile heuristic — so containment is checked rather than
    assumed.
    """
    try:
        candidate = (base / rel).resolve()
        candidate.relative_to(REPO_ROOT)
    except (ValueError, OSError):
        return None
    return candidate


def _readable(candidate: Path) -> tuple[Path | None, str]:
    """The path to read, or (None, reason) when reading it would be unsafe.

    Rejects the symlink ITSELF rather than resolve-and-recheck. Checking only
    the resolved path was not enough: a link whose target lands inside the repo
    — another tracked file, or a device/FIFO under the tree — passes both
    containment and is_file() and then gets read anyway, and is_file() to
    read_text() is two syscalls with a window between them. is_symlink() does
    not follow the link. Nothing this guard reads is legitimately a symlink, so
    rejecting outright costs the repository nothing.

    This guard runs trusted code against PR-head content, so a PR can plant
    either the action metadata or the Dockerfile an `image:` line names.
    Pointed at a character device (/dev/zero) read_text() never returns and the
    gate hangs instead of failing — a fail-closed check turned into a stall.
    """
    if candidate.is_symlink():
        return None, "symlink; not read"
    resolved = _resolve_in_repo(candidate.parent, candidate.name)
    if resolved is None:
        return None, "resolves outside the repository; not read"
    if not resolved.is_file():
        return None, f"not a regular file ({resolved}); not read"
    return resolved, ""


def local_action_files(text: str) -> list[Path]:
    """Action metadata reachable through `uses: ./…` from this file.

    `./` refs are skipped as pin targets — a path in this repo has no SHA to
    pin — but the action they point at can still name a mutable image, and it
    may sit outside ACTION_GLOBS entirely. Follow them instead of trusting them.
    Note `uses: ./x` is resolved from the REPOSITORY ROOT, not the caller.
    """
    found: list[Path] = []
    for line in text.splitlines():
        match = USES_PATTERN.match(line)
        if not match:
            continue
        # _scalar() first, exactly as unpinned_refs() does. Testing the raw
        # value made `uses: "./x"` and `uses: ./x # note` local to one function
        # and not the other: flagged as local there, not followed here — so an
        # action outside ACTION_GLOBS kept its mutable image unscanned.
        ref = _scalar(match.group(1))
        if not ref.startswith("./"):
            continue
        target = _resolve_in_repo(REPO_ROOT, ref)
        if target is None:
            continue
        for name in ("action.yml", "action.yaml"):
            candidate = target / name
            if candidate.is_file():
                found.append(candidate)
    return found


def _looks_like_dockerfile(image: str, path: Path) -> bool:
    """A build context path rather than a registry reference.

    Only ACTION METADATA can name a Dockerfile: `runs.image` is the sole place
    GitHub builds an image from the repository. A workflow's `container:` or
    `services:` `image:` is always a registry reference, and Docker tags may
    contain uppercase — so `image: myorg/app:Dockerfile-base` is a legal
    registry ref that this heuristic read as a path, then reported as
    unreadable. Scoping to action.yml/action.yaml removes that whole class;
    workflow images fall through to the digest rule, which is what they need.
    """
    if path.name not in ("action.yml", "action.yaml"):
        return False
    if image.startswith("docker://"):
        return False
    return "Dockerfile" in image or image.startswith(("./", "../"))


def _unpinned_from_lines(
    action_path: Path, image: str, image_lineno: int
) -> list[tuple[int, str]]:
    """Every FROM in the referenced Dockerfile must name a digest.

    Exceptions, both legitimate: `scratch` (the empty base, which has no
    digest) and a reference to an earlier build stage declared with `AS`.
    """
    dockerfile, reason = _readable(action_path.parent / image)
    if dockerfile is None:
        return [(image_lineno, f"{image} ({reason})")]
    # Fail closed: an action pointing at a Dockerfile we cannot read — or
    # cannot decode — is not something to wave through, and must not raise.
    text, reason = _read(dockerfile)
    if text is None:
        return [(image_lineno, f"{image} (Dockerfile {reason})")]

    findings: list[tuple[int, str]] = []
    stages: set[str] = set()
    for lineno, line in _logical_lines(text):
        instruction = _from_instruction(line)
        if instruction is None:
            continue
        base, stage = instruction
        # Classify the base BEFORE registering this line's own alias. Adding it
        # first lets a stage exempt itself: `FROM alpine AS alpine` would match
        # `base in stages` and skip the digest check on a mutable image. Only
        # aliases from EARLIER FROM lines are real stage references.
        exempt = base.lower() == "scratch" or base.lower() in stages
        if not exempt and not IMAGE_DIGEST_PATTERN.search(base):
            rel = dockerfile.relative_to(REPO_ROOT).as_posix()
            findings.append(
                (
                    image_lineno,
                    (f"{image} -> {rel}:{lineno} FROM {base} (needs @sha256:<64 hex>)"),
                )
            )
        if stage:
            stages.add(stage.lower())
    return findings


def main() -> int:
    targets = scan_targets()
    if not targets:
        print("action-pin guard: no workflow or action files found", file=sys.stderr)
        return 2

    findings: list[str] = []
    # Worklist rather than a flat pass: a scanned file can point at a local
    # action that ACTION_GLOBS does not reach, and that action can point at
    # another. `seen` keeps a cycle (a -> b -> a) from spinning.
    queue = list(targets)
    seen: set[Path] = set()
    while queue:
        path = queue.pop()
        if path in seen:
            continue
        seen.add(path)
        rel = path.relative_to(REPO_ROOT).as_posix()
        # Check what will actually be read BEFORE reading it — see _readable().
        # The Dockerfile an `image:` line names goes through the same gate.
        readable, reason = _readable(path)
        if readable is None:
            findings.append(f"{rel}: {reason}")
            continue
        # Read the path that was VERIFIED, not the one that was named. They
        # denote the same file here, but handing the readers `path` left the
        # check and the read describing two different objects, which is how a
        # later edit quietly drifts one away from the other. `rel` still comes
        # from `path`, so findings name the file as the repository sees it.
        # One read, one place decode failures are handled, and the readers
        # cannot drift back to opening the file themselves.
        text, reason = _read(readable)
        if text is None:
            findings.append(f"{rel}: {reason}")
            continue
        queue.extend(local_action_files(text))
        for lineno, ref in unpinned_refs(readable, text):
            findings.append(f"{rel}:{lineno}: {ref}")
    findings.sort()

    if findings:
        print(
            "action-pin guard: unpinned reference "
            "(actions need a full 40-char SHA; images and Dockerfile FROM lines "
            "need @sha256:<64 hex>):",
            file=sys.stderr,
        )
        for finding in findings:
            print(f"  {finding}", file=sys.stderr)
        return 1

    print("action-pin guard: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
