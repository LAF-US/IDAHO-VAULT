#!/usr/bin/env python3
"""Sync pull request lifecycle events into Linear issues.

Safeguards included:
- Issue identifier fallback from branch names (e.g., laf-123)
- Skip draft PRs until ready for review
- Optional Linear comment/linkback when PR opens or merges
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
    open_state_id: str
    merged_state_id: str
    post_linkback: bool


class LinearSyncError(RuntimeError):
    """Raised when the sync cannot continue safely."""


def log(message: str) -> None:
    print(f"[linear-pr-sync] {message}")


def read_json(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def find_issue_identifier(pr: Dict[str, Any]) -> Optional[str]:
    candidates = [
        pr.get("title", ""),
        pr.get("body", "") or "",
        pr.get("head", {}).get("ref", ""),
        pr.get("base", {}).get("ref", ""),
    ]
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
        }
      }
    }
    """
    data = linear_request(api_key, query, {"identifier": identifier})
    nodes = (data.get("issues") or {}).get("nodes") or []
    if not nodes:
        raise LinearSyncError(f"No Linear issue found for identifier '{identifier}'.")
    return nodes[0]


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
        raise LinearSyncError("Missing required env var LINEAR_API_KEY.")

    event_path = os.getenv("GITHUB_EVENT_PATH", "").strip()
    if not event_path:
        raise LinearSyncError("Missing required env var GITHUB_EVENT_PATH.")

    return Config(
        linear_api_key=linear_api_key,
        event_path=event_path,
        open_state_id=os.getenv("LINEAR_PR_OPEN_STATE_ID", "").strip(),
        merged_state_id=os.getenv("LINEAR_PR_MERGED_STATE_ID", "").strip(),
        post_linkback=os.getenv("LINEAR_POST_LINKBACK", "false").strip().lower() == "true",
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


def main() -> int:
    try:
        cfg = load_config()
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

        identifier = find_issue_identifier(pr)
        if not identifier:
            log("No Linear-style issue identifier found in title/body/branch. Skipping.")
            return 0
        log(f"Matched Linear identifier: {identifier}")

        issue = get_issue(cfg.linear_api_key, identifier)
        issue_id = issue["id"]
        log(f"Resolved Linear issue: {issue['identifier']} — {issue['title']}")

        if action in {"opened", "reopened", "ready_for_review"}:
            if cfg.open_state_id:
                log(f"Updating issue state -> LINEAR_PR_OPEN_STATE_ID ({cfg.open_state_id})")
                update_issue_state(cfg.linear_api_key, issue_id, cfg.open_state_id)
            else:
                log("LINEAR_PR_OPEN_STATE_ID not set; skipping state update for PR open event.")

        if action == "closed" and pr.get("merged"):
            if cfg.merged_state_id:
                log(f"Updating issue state -> LINEAR_PR_MERGED_STATE_ID ({cfg.merged_state_id})")
                update_issue_state(cfg.linear_api_key, issue_id, cfg.merged_state_id)
            else:
                log("LINEAR_PR_MERGED_STATE_ID not set; skipping state update for merged PR.")

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
        log(f"ERROR: {exc}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
