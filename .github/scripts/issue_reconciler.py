#!/usr/bin/env python3
"""Open, update, or close a recurring GitHub issue based on current findings."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from pathlib import Path

import gh_cli

FINGERPRINT_PREFIX = "<!-- issue-reconciler-fingerprint:"
FINGERPRINT_SUFFIX = " -->"


def _json(result: gh_cli.GhResult) -> list[dict] | dict | None:
    """Decode a gh JSON payload, returning None when there is nothing decodable."""
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        return None


def _repo() -> tuple[str, str]:
    """Split ``GITHUB_REPOSITORY`` into ``(owner, repo)``."""
    slug = os.environ.get("GITHUB_REPOSITORY", "")
    if slug not in ("LAF-US/IDAHO-VAULT",):
        raise RuntimeError(f"This reconciler is scoped to LAF-US/IDAHO-VAULT, got: {slug!r}")
    owner, _, name = slug.partition("/")
    return (owner, name)


def _recurring_title(title: str) -> str:
    """Return ``title`` if it names a recurring issue this reconciler owns."""
    # This is a find-or-create-by-title driver, so the title is an identifier rather
    # than free text — every workflow passes one of these five, and an unrecognized one
    # would open a stray issue nothing would ever reconcile or close. Adding a recurring
    # report means adding it here, which also keeps the set greppable in one place.
    #
    # The literals are written inline, and the checked value is what gets returned and
    # used, because that is the shape a comparison-against-constants takes: it is what
    # keeps an arbitrary title from travelling onward into a command line.
    if title not in (
        "[Branch Garden] Weekly report",
        "[Large File Watchdog] Weekly report",
        "[Looker Worklist] Review-thread triage census",
        "[Metadata Survey] Weekly report",
        "[PR Loop Watchdog] Reconciliation report",
    ):
        raise ValueError(f"Not a recurring issue this reconciler owns: {title!r}")
    return title


def _strip_fingerprint(body: str) -> str:
    lines = [
        line
        for line in body.splitlines()
        if not line.startswith(FINGERPRINT_PREFIX)
    ]
    return "\n".join(lines).rstrip()


def ensure_body_fingerprint(body_file: Path) -> str:
    """Stamp the body file with a digest of its own content and return the marker."""
    # The digest is taken over the body with any previous marker stripped, so an
    # unchanged report produces an unchanged marker — that is what lets the caller
    # tell a repeat finding from a new one without diffing prose.
    if ".." in body_file.parts:
        raise ValueError(f"Refusing a body path containing '..': {body_file}")
    body = body_file.read_text(encoding="utf-8")
    canonical_body = _strip_fingerprint(body)
    digest = hashlib.sha256(canonical_body.encode("utf-8")).hexdigest()
    marker = f"{FINGERPRINT_PREFIX}{digest}{FINGERPRINT_SUFFIX}"
    body_file.write_text(f"{canonical_body}\n\n{marker}\n", encoding="utf-8")
    return marker


def find_open_issue_number(title: str) -> int | None:
    """Return the open issue whose title matches exactly, or None."""
    # gh's search is fuzzy, so the exact-title check below is what actually decides;
    # the search only narrows the page.
    owner, repo = _repo()
    # A failed search is NOT "no such issue". Swallowing the error here would make the
    # caller open a duplicate on every transient gh/API blip, so the failure propagates
    # and the run stops — which is what this did before the gh_cli migration.
    result = gh_cli.issue_search_open(
        owner,
        repo,
        search=f'"{title}" in:title',
        json_fields="number,title",
    )
    issues = _json(result)
    if not isinstance(issues, list):
        return None
    for issue in issues:
        if issue.get("title") == title:
            return int(issue["number"])
    return None


def issue_has_fingerprint(issue_number: int, marker: str) -> bool:
    """Report whether this exact marker already appears in the issue body or comments."""
    owner, repo = _repo()
    try:
        issue = _json(
            gh_cli.issue_view(issue_number, owner=owner, repo=repo, json_fields="body")
        )
    except RuntimeError:
        issue = None
    if isinstance(issue, dict) and marker in str(issue.get("body") or ""):
        return True

    comments = gh_cli.api_issue_comments(
        owner, repo, issue_number, jq=".[].body", check=False
    )
    return comments.returncode == 0 and marker in comments.stdout


def create_issue(title: str, body_file: Path) -> int:
    """Open the issue and return its number, parsed from the URL gh prints."""
    owner, repo = _repo()
    result = gh_cli.issue_create(
        owner=owner, repo=repo, title=title,
        body=body_file.read_text(encoding="utf-8"),
    )
    issue_url = result.stdout.strip()
    if "/issues/" not in issue_url:
        raise RuntimeError(f"Could not parse issue URL from gh output: {issue_url}")
    return int(issue_url.rsplit("/issues/", 1)[1])


def comment_issue(issue_number: int, body_file: Path) -> None:
    """Append the current report to an existing issue as a comment."""
    # Passes the body's *text*, not this path. ``body_file`` arrives from the
    # ``--body-file`` command-line argument, so handing it to ``issue_comment_file``
    # would put caller-controlled input directly into argv — the "uncontrolled command
    # line" flow this PR exists to close. ``issue_comment`` writes the text to a
    # temp file `gh_cli` owns and passes *that* path instead, so argv carries only
    # tokens the module produced.
    owner, repo = _repo()
    gh_cli.issue_comment(
        issue_number, owner=owner, repo=repo,
        body=body_file.read_text(encoding="utf-8"),
    )


def close_issue(issue_number: int) -> None:
    """Close the issue as completed."""
    owner, repo = _repo()
    gh_cli.issue_close(issue_number, owner=owner, repo=repo)


def reconcile_issue(
    *,
    title: str,
    body_file: Path,
    has_findings: bool,
    resolved_comment: str,
) -> dict[str, object]:
    """Open, update, or close the recurring issue for ``title`` to match the findings."""
    # Four outcomes, reported as ``issue_action``: ``created`` (findings, no open issue),
    # ``commented`` (findings the issue has not already recorded), ``noop_duplicate``
    # (findings identical to what is already there, by fingerprint), and ``closed``
    # (no findings left). Writes both to ``GITHUB_OUTPUT`` when the workflow sets it.
    title = _recurring_title(title)
    issue_number = find_open_issue_number(title)
    issue_action = "noop"

    if has_findings:
        marker = ensure_body_fingerprint(body_file)
        if issue_number is None:
            issue_number = create_issue(title, body_file)
            issue_action = "created"
        elif issue_has_fingerprint(issue_number, marker):
            issue_action = "noop_duplicate"
        else:
            comment_issue(issue_number, body_file)
            issue_action = "commented"
    elif issue_number is not None:
        owner, repo = _repo()
        gh_cli.issue_comment(issue_number, owner=owner, repo=repo, body=resolved_comment)
        close_issue(issue_number)
        issue_action = "closed"

    result = {
        "title": title,
        "has_findings": has_findings,
        "issue_action": issue_action,
        "issue_number": issue_number,
    }
    github_output = os.environ.get("GITHUB_OUTPUT")
    if github_output:
        with open(github_output, "a", encoding="utf-8") as fh:
            fh.write(f"issue_action={issue_action}\n")
            fh.write(f"issue_number={issue_number or ''}\n")
    return result


def _parse_bool(raw: str) -> bool:
    normalized = raw.strip().lower()
    if normalized in {"true", "1", "yes"}:
        return True
    if normalized in {"false", "0", "no"}:
        return False
    raise argparse.ArgumentTypeError(f"Expected boolean value, got {raw!r}")


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI parser."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--title", required=True)
    parser.add_argument("--body-file", type=Path, required=True)
    parser.add_argument("--has-findings", type=_parse_bool, required=True)
    parser.add_argument(
        "--resolved-comment",
        default="Resolved automatically: the latest run found no current findings.",
    )
    return parser


def main() -> int:
    """Reconcile the issue named on the command line and print the report as JSON."""
    args = build_parser().parse_args()
    report = reconcile_issue(
        title=args.title,
        body_file=args.body_file,
        has_findings=args.has_findings,
        resolved_comment=args.resolved_comment,
    )
    print(json.dumps(report))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:  # pragma: no cover - workflow-facing failure path
        print(f"issue_reconciler.py failed: {exc}", file=sys.stderr)
        raise
