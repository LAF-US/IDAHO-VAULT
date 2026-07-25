#!/usr/bin/env python3
"""Open, update, or close a recurring GitHub issue based on current findings."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

from gh_cli import run

FINGERPRINT_PREFIX = "<!-- issue-reconciler-fingerprint:"
FINGERPRINT_SUFFIX = " -->"


def gh(*args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    """Run a ``gh`` subcommand via the shared run-capture-raise primitive."""
    return run(["gh", *args], check=check)


def gh_json(*args: str) -> list[dict] | dict:
    result = gh(*args)
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"gh {' '.join(args)} returned invalid JSON") from exc


def _repo() -> str:
    repo = os.environ.get("GITHUB_REPOSITORY", "")
    if not repo:
        raise RuntimeError("GITHUB_REPOSITORY is required.")
    return repo


def _strip_fingerprint(body: str) -> str:
    lines = [
        line
        for line in body.splitlines()
        if not line.startswith(FINGERPRINT_PREFIX)
    ]
    return "\n".join(lines).rstrip()


def ensure_body_fingerprint(body_file: Path) -> str:
    if ".." in str(body_file):
        raise Exception("Invalid file path")
    body = body_file.read_text(encoding="utf-8")
    canonical_body = _strip_fingerprint(body)
    digest = hashlib.sha256(canonical_body.encode("utf-8")).hexdigest()
    marker = f"{FINGERPRINT_PREFIX}{digest}{FINGERPRINT_SUFFIX}"
    body_file.write_text(f"{canonical_body}\n\n{marker}\n", encoding="utf-8")
    return marker


def find_open_issue_number(title: str) -> int | None:
    issues = gh_json(
        "issue",
        "list",
        "--repo",
        _repo(),
        "--state",
        "open",
        "--search",
        f"\"{title}\" in:title",
        "--json",
        "number,title",
        "--limit",
        "20",
    )
    if not isinstance(issues, list):
        return None
    for issue in issues:
        if issue.get("title") == title:
            return int(issue["number"])
    return None


def issue_has_fingerprint(issue_number: int, marker: str) -> bool:
    issue = gh_json(
        "issue",
        "view",
        str(issue_number),
        "--repo",
        _repo(),
        "--json",
        "body",
    )
    if isinstance(issue, dict) and marker in str(issue.get("body") or ""):
        return True

    comments = gh(
        "api",
        "--paginate",
        f"repos/{_repo()}/issues/{issue_number}/comments",
        "--jq",
        ".[].body",
        check=False,
    )
    return comments.returncode == 0 and marker in comments.stdout


def create_issue(title: str, body_file: Path) -> int:
    result = gh(
        "issue",
        "create",
        "--repo",
        _repo(),
        "--title",
        title,
        "--body-file",
        str(body_file),
    )
    issue_url = result.stdout.strip()
    if "/issues/" not in issue_url:
        raise RuntimeError(f"Could not parse issue URL from gh output: {issue_url}")
    return int(issue_url.rsplit("/issues/", 1)[1])


def comment_issue(issue_number: int, body_file: Path) -> None:
    gh(
        "issue",
        "comment",
        str(issue_number),
        "--repo",
        _repo(),
        "--body-file",
        str(body_file),
    )


def close_issue(issue_number: int) -> None:
    gh(
        "issue",
        "close",
        str(issue_number),
        "--repo",
        _repo(),
        "--reason",
        "completed",
    )


def reconcile_issue(
    *,
    title: str,
    body_file: Path,
    has_findings: bool,
    resolved_comment: str,
) -> dict[str, object]:
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
        gh(
            "issue",
            "comment",
            str(issue_number),
            "--repo",
            _repo(),
            "--body",
            resolved_comment,
        )
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
