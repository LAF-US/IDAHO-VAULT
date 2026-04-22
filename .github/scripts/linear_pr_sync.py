#!/usr/bin/env python3
"""Sync pull request lifecycle events into Linear issues.

Safeguards included:
- Issue identifier fallback from branch names (e.g., laf-123)
- Skip draft PRs until ready for review
- Optional Linear comment/linkback when PR opens or merges
- Dynamic team state resolution (no static state-id secrets)
- Clear logs and actionable failure output
"""

from __future__ import annotations

import json
import os
import re
import sys
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Any, Dict, Optional

LINEAR_API_URL = "https://api.linear.app/graphql"
ISSUE_RE = re.compile(r"\b([A-Z]+-\d+)\b", re.IGNORECASE)


@dataclass
class Config:
    linear_api_key: str
    event_path: str
    post_linkback: bool
    strict_mode: bool
    trusted_author_associations: set[str]


class LinearSyncError(RuntimeError):
    """Raised when the sync cannot continue safely."""


def log(message: str) -> None:
    print(f"[linear-pr-sync] {message}")


def read_json(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def _csv_env(name: str, default: str = "") -> set[str]:
    raw = os.getenv(name, default)
    return {item.strip().upper() for item in raw.split(",") if item.strip()}


def is_trusted_pr_source(pr: Dict[str, Any], *, trusted_author_associations: set[str]) -> tuple[bool, str]:
    head_repo = (pr.get("head") or {}).get("repo") or {}
    base_repo = (pr.get("base") or {}).get("repo") or {}

    head_full_name = str(head_repo.get("full_name") or "").lower()
    base_full_name = str(base_repo.get("full_name") or "").lower()
    if not head_full_name or not base_full_name or head_full_name != base_full_name:
        return False, "PR originates from an untrusted repository context; skipping secret-backed Linear sync."

    author_association = str(pr.get("author_association") or "").upper()
    if author_association not in trusted_author_associations:
        return (
            False,
            f"PR author association {author_association!r} is not trusted for secret-backed Linear sync.",
        )

    return True, ""


def find_issue_identifier(pr: Dict[str, Any], *, trusted_metadata: bool) -> Optional[str]:
    candidates = [pr.get("head", {}).get("ref", "")]
    if trusted_metadata:
        candidates.extend([pr.get("title", ""), pr.get("body", "") or ""])
    for text in candidates:
        match = ISSUE_RE.search(text)
        if match:
            return match.group(1).upper()
    return None


def linear_request(api_key: str, query: str, variables: Dict[str, Any]) -> Dict[str, Any]:
    payload = json.dumps({"query": query, "variables": variables}).encode("utf-8")
    req = urllib.request.Request(
        LINEAR_API_URL,
        data=payload,
        method="POST",
        headers={
            "Authorization": api_key,
            "Content-Type": "application/json",
        },
    )

    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            raw = response.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise LinearSyncError(f"Linear API HTTP {exc.code}: {body}") from exc
    except urllib.error.URLError as exc:
        raise LinearSyncError(f"Network error while contacting Linear API: {exc.reason}") from exc

    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise LinearSyncError(f"Failed to parse Linear API response as JSON: {raw[:300]}") from exc

    if parsed.get("errors"):
        raise LinearSyncError(f"Linear GraphQL errors: {parsed['errors']}")

    return parsed.get("data", {})


def get_issue(api_key: str, identifier: str) -> Dict[str, Any]:
    query = """
    query IssueByIdentifier($identifier: String!) {
      issues(filter: { identifier: { eq: $identifier } }) {
        nodes {
          id
          identifier
          title
          team {
            id
            key
            name
            states {
              nodes {
                id
                name
                type
              }
            }
          }
        }
      }
    }
    """
    data = linear_request(api_key, query, {"identifier": identifier})
    nodes = (data.get("issues") or {}).get("nodes") or []
    if not nodes:
        raise LinearSyncError(f"No Linear issue found for identifier '{identifier}'.")
    return nodes[0]


def resolve_target_state(issue: Dict[str, Any], action: str, merged: bool) -> Optional[Dict[str, Any]]:
    if action in {"opened", "reopened", "ready_for_review"}:
        desired_type = "started"
        desired_name = "In Progress"
    elif action == "closed" and merged:
        desired_type = "completed"
        desired_name = "Done"
    else:
        return None

    states = issue.get("team", {}).get("states", {}).get("nodes", [])
    target = next((s for s in states if s.get("type") == desired_type), None)
    if target:
        return target

    return next((s for s in states if (s.get("name") or "").lower() == desired_name.lower()), None)


def update_issue_state(api_key: str, issue_id: str, state_id: str) -> None:
    mutation = """
    mutation UpdateIssueState($issueId: String!, $stateId: String!) {
      issueUpdate(id: $issueId, input: { stateId: $stateId }) {
        success
      }
    }
    """
    data = linear_request(api_key, mutation, {"issueId": issue_id, "stateId": state_id})
    success = data.get("issueUpdate", {}).get("success")
    if not success:
        raise LinearSyncError("Linear issueUpdate returned success=false.")


def create_comment(api_key: str, issue_id: str, body: str) -> None:
    mutation = """
    mutation CommentOnIssue($issueId: String!, $body: String!) {
      commentCreate(input: { issueId: $issueId, body: $body }) {
        success
      }
    }
    """
    data = linear_request(api_key, mutation, {"issueId": issue_id, "body": body})
    success = data.get("commentCreate", {}).get("success")
    if not success:
        raise LinearSyncError("Linear commentCreate returned success=false.")


def load_config() -> Config:
    linear_api_key = os.getenv("LINEAR_API_KEY", "").strip()
    if not linear_api_key:
        raise LinearSyncError("LINEAR_API_KEY is not set.")

    event_path = os.getenv("GITHUB_EVENT_PATH", "").strip()
    if not event_path:
        raise LinearSyncError("Missing required env var GITHUB_EVENT_PATH.")

    strict_mode = os.getenv("LINEAR_SYNC_STRICT", "false").strip().lower() in {"1", "true", "yes", "on"}

    # Default linkback comments to ON so Linear shows visible progress by default.
    # Operators can still disable per-run via LINEAR_POST_LINKBACK=false.
    post_linkback_env = os.getenv("LINEAR_POST_LINKBACK", "true").strip().lower()

    return Config(
        linear_api_key=linear_api_key,
        event_path=event_path,
        post_linkback=post_linkback_env in {"1", "true", "yes", "on"},
        strict_mode=strict_mode,
        trusted_author_associations=_csv_env(
            "LINEAR_TRUSTED_AUTHOR_ASSOCIATIONS",
            "OWNER,MEMBER,COLLABORATOR",
        ),
    )


def build_comment(action: str, pr: Dict[str, Any]) -> Optional[str]:
    number = pr.get("number")
    title = pr.get("title", "")
    html_url = pr.get("html_url", "")

    if action in {"opened", "reopened", "ready_for_review"}:
        return f"PR opened: [#{number} {title}]({html_url})"

    if action == "closed" and pr.get("merged"):
        return f"PR merged: [#{number} {title}]({html_url})"

    return None


def soft_fail(cfg: Config, message: str) -> int:
    log(message)
    if cfg.strict_mode:
        log("LINEAR_SYNC_STRICT enabled; failing run.")
        return 1
    return 0


def main() -> int:
    try:
        cfg = load_config()
    except LinearSyncError as exc:
        # Secret not provisioned should not break all PR checks by default.
        log(f"{exc} Skipping sync.")
        return 0

    try:
        event = read_json(cfg.event_path)
        action = event.get("action", "")
        pr = event.get("pull_request") or {}
        if not pr:
            raise LinearSyncError("Event payload missing pull_request object.")

        log(f"Event action: {action}")
        log(f"PR #{pr.get('number')} on branch '{pr.get('head', {}).get('ref', '')}'")

        is_draft = bool(pr.get("draft"))
        if is_draft and action != "ready_for_review":
            log("Draft PR detected; skipping sync until ready_for_review.")
            return 0

        trusted_source, trust_reason = is_trusted_pr_source(
            pr,
            trusted_author_associations=cfg.trusted_author_associations,
        )
        if not trusted_source:
            log(trust_reason)
            return 0

        identifier = find_issue_identifier(pr, trusted_metadata=True)
        if not identifier:
            log("No trusted Linear-style issue identifier found in branch/title/body. Skipping.")
            return 0
        log(f"Matched Linear identifier: {identifier}")

        issue = get_issue(cfg.linear_api_key, identifier)
        issue_id = issue["id"]
        log(f"Resolved Linear issue: {issue['identifier']} — {issue['title']}")

        target_state = resolve_target_state(issue, action, bool(pr.get("merged")))
        if target_state:
            log(f"Updating issue state -> {target_state.get('name')} ({target_state.get('id')})")
            update_issue_state(cfg.linear_api_key, issue_id, target_state["id"])
        else:
            log("No state transition required for this event/action. Skipping state update.")

        if cfg.post_linkback:
            comment = build_comment(action, pr)
            if comment:
                log("Posting optional Linear linkback comment.")
                create_comment(cfg.linear_api_key, issue_id, comment)
            else:
                log("No comment template for this action; skipping comment.")
        else:
            log("LINEAR_POST_LINKBACK=false; skipping comment creation.")

        log("Sync completed successfully.")
        return 0

    except LinearSyncError as exc:
        return soft_fail(cfg, f"ERROR: {exc}")


if __name__ == "__main__":
    sys.exit(main())
