#!/usr/bin/env python3
"""Small GitHub review feedback loop helpers for PR automation.

Modes:
  - acknowledge-apply: observe a trusted `@copilot apply changes` request
    and mark the PR as waiting on a GitHub-side Copilot follow-up push.
  - sync-pr: after PR updates land, auto-resolve outdated advisory threads
    from allowlisted review bots and keep merge-blocking thread state visible.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys


APPLY_RE = re.compile(r"@copilot\b[\s\S]*?\bapply changes\b", re.IGNORECASE)
DEFAULT_THREAD_LABEL = "review-threads-open"
DEFAULT_PENDING_LABEL = "copilot-apply-pending"


def _run(cmd: list[str], check: bool = True) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(cmd, capture_output=True, text=True)
    if check and result.returncode != 0:
        raise RuntimeError(
            f"Command failed ({result.returncode}): {' '.join(cmd)}\n"
            f"stdout:\n{result.stdout}\n"
            f"stderr:\n{result.stderr}"
        )
    return result


def _graphql(query: str, **variables: object) -> dict:
    cmd = ["gh", "api", "graphql", "-f", f"query={query}"]
    for key, value in variables.items():
        if isinstance(value, int):
            cmd.extend(["-F", f"{key}={value}"])
        else:
            cmd.extend(["-f", f"{key}={value}"])
    result = _run(cmd)
    payload = json.loads(result.stdout or "{}")
    errors = payload.get("errors")
    if errors:
        raise RuntimeError(f"GraphQL error(s): {json.dumps(errors, indent=2)}")
    return payload.get("data", {})


def _fetch_pr(owner: str, name: str, number: int) -> dict:
    query = """
    query($owner:String!, $name:String!, $number:Int!) {
      repository(owner: $owner, name: $name) {
        pullRequest(number: $number) {
          number
          url
          labels(first: 50) {
            nodes { name }
          }
          reviewThreads(first: 100) {
            nodes {
              id
              isResolved
              isOutdated
              comments(first: 20) {
                nodes {
                  author { login }
                  body
                  url
                }
              }
            }
          }
        }
      }
    }
    """
    data = _graphql(query, owner=owner, name=name, number=number)
    repo = data.get("repository") or {}
    pr = repo.get("pullRequest")
    if not pr:
        raise RuntimeError(f"Pull request #{number} was not found in {owner}/{name}.")
    return pr


def _resolve_thread(thread_id: str) -> None:
    mutation = """
    mutation($threadId: ID!) {
      resolveReviewThread(input: {threadId: $threadId}) {
        thread { id isResolved }
      }
    }
    """
    _graphql(mutation, threadId=thread_id)


def _ensure_label(name: str, color: str, description: str) -> None:
    _run(
        [
            "gh",
            "label",
            "create",
            name,
            "--color",
            color,
            "--description",
            description,
            "--force",
        ]
    )


def _edit_label(pr_number: int, *, add: str | None = None, remove: str | None = None) -> None:
    if add:
        _run(["gh", "pr", "edit", str(pr_number), "--add-label", add], check=False)
    if remove:
        _run(["gh", "pr", "edit", str(pr_number), "--remove-label", remove], check=False)


def _comment(pr_number: int, body: str) -> None:
    _run(["gh", "pr", "comment", str(pr_number), "--body", body])


def _csv_env(name: str, default: str = "") -> set[str]:
    raw = os.environ.get(name, default)
    return {item.strip() for item in raw.split(",") if item.strip()}


def _thread_authors(thread: dict) -> set[str]:
    authors: set[str] = set()
    for comment in (thread.get("comments") or {}).get("nodes") or []:
        author = (comment.get("author") or {}).get("login")
        if author:
            authors.add(author)
    return authors


def acknowledge_apply(args: argparse.Namespace) -> int:
    if not APPLY_RE.search(args.comment_body or ""):
        print("Comment does not match an @copilot apply request; nothing to do.")
        return 0

    trusted = _csv_env("TRUSTED_COMMENT_ASSOCIATIONS", "OWNER,MEMBER,COLLABORATOR")
    if args.author_association not in trusted:
        print(
            f"Comment author association {args.author_association!r} is not trusted; "
            "skipping acknowledgement."
        )
        return 0

    pr = _fetch_pr(args.owner, args.repo, args.pr_number)
    labels = {node["name"] for node in (pr.get("labels") or {}).get("nodes") or []}

    _ensure_label(
        DEFAULT_PENDING_LABEL,
        "5319E7",
        "Waiting for a GitHub Copilot apply-changes follow-up push.",
    )

    if DEFAULT_PENDING_LABEL not in labels:
        _edit_label(args.pr_number, add=DEFAULT_PENDING_LABEL)
        _comment(
            args.pr_number,
            (
                f"Observed a Copilot apply request from @{args.comment_author}. "
                f"Marked this PR as `{DEFAULT_PENDING_LABEL}`. "
                "When follow-up commits land, the review feedback loop will sweep "
                "outdated advisory threads automatically and keep any current "
                "unresolved threads visible."
            ),
        )
    else:
        print(f"{DEFAULT_PENDING_LABEL} already present; acknowledgement is already in place.")

    return 0


def sync_pr(args: argparse.Namespace) -> int:
    pr = _fetch_pr(args.owner, args.repo, args.pr_number)
    labels = {node["name"] for node in (pr.get("labels") or {}).get("nodes") or []}
    threads = (pr.get("reviewThreads") or {}).get("nodes") or []

    auto_resolve_reviewers = _csv_env(
        "AUTO_RESOLVE_REVIEWERS",
        "copilot-pull-request-reviewer",
    )
    completion_actors = _csv_env(
        "APPLY_COMPLETION_ACTORS",
        "Copilot,copilot-swe-agent[bot]",
    )

    resolved_count = 0
    remaining_unresolved = 0
    current_unresolved = 0

    for thread in threads:
        if thread.get("isResolved"):
            continue

        authors = _thread_authors(thread)
        if thread.get("isOutdated") and authors and authors.issubset(auto_resolve_reviewers):
            _resolve_thread(thread["id"])
            resolved_count += 1
            continue

        remaining_unresolved += 1
        if not thread.get("isOutdated"):
            current_unresolved += 1

    _ensure_label(
        DEFAULT_THREAD_LABEL,
        "FBCA04",
        "Unresolved review threads still need attention before merge.",
    )

    if remaining_unresolved > 0:
        if DEFAULT_THREAD_LABEL not in labels:
            _edit_label(args.pr_number, add=DEFAULT_THREAD_LABEL)
    elif DEFAULT_THREAD_LABEL in labels:
        _edit_label(args.pr_number, remove=DEFAULT_THREAD_LABEL)

    if args.sync_actor in completion_actors and DEFAULT_PENDING_LABEL in labels:
        _edit_label(args.pr_number, remove=DEFAULT_PENDING_LABEL)

    if resolved_count:
        live_note = (
            f"{current_unresolved} still current"
            if current_unresolved
            else "no current threads remain"
        )
        _comment(
            args.pr_number,
            (
                f"Auto-swept {resolved_count} outdated advisory review thread(s) after "
                f"new commits landed. {remaining_unresolved} unresolved thread(s) remain; "
                f"{live_note}."
            ),
        )

    print(
        json.dumps(
            {
                "resolved_outdated_threads": resolved_count,
                "remaining_unresolved_threads": remaining_unresolved,
                "current_unresolved_threads": current_unresolved,
            }
        )
    )
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", required=True, choices={"acknowledge-apply", "sync-pr"})
    parser.add_argument("--owner", required=True)
    parser.add_argument("--repo", required=True)
    parser.add_argument("--pr-number", required=True, type=int)
    parser.add_argument("--comment-author", default="")
    parser.add_argument("--author-association", default="")
    parser.add_argument("--comment-body", default="")
    parser.add_argument("--sync-actor", default="")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    if args.mode == "acknowledge-apply":
        return acknowledge_apply(args)
    return sync_pr(args)


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:  # pragma: no cover - workflow-facing failure path
        print(f"review_feedback_loop.py failed: {exc}", file=sys.stderr)
        raise
