#!/usr/bin/env python3
"""
Swarm Linear Gateway — Broker Script
=====================================
Single-choke-point broker for all swarm agent reads and writes to the Linear
GraphQL API. Implements the five gateway commands defined in:

  !/SPEC-LINEAR-GATEWAY-2026-03-29.md

Guardrails:
  - Dry-run default: all mutations require --live-write or MCP_LIVE_WRITE=true
  - All calls emit a vault-compliant MCP action log (see mcp_guardrails.py)
  - No credentials in vault files; LINEAR_API_KEY must be in environment
  - Role declaration is required (--role observer|executor|coordinator|secretary)
  - issue-id is required for all write commands

Usage examples:
  # Read an issue (dry-run safe — reads never mutate)
  python3 linear_gateway.py read_issue --issue-id LAF-7 \\
    --initiating-agent github-copilot --role observer

  # List all issues in a project
  python3 linear_gateway.py list_project_issues --project-id <id> \\
    --initiating-agent github-copilot --role observer

  # Post a comment (dry-run by default)
  python3 linear_gateway.py post_comment --issue-id LAF-7 \\
    --body "Agent checkpoint: work complete." \\
    --initiating-agent github-copilot --role secretary

  # Post a comment (live write)
  MCP_LIVE_WRITE=true python3 linear_gateway.py post_comment \\
    --issue-id LAF-7 --body "Deployed." \\
    --initiating-agent github-copilot --role executor --live-write

  # Update issue status (dry-run by default)
  python3 linear_gateway.py update_issue_status --issue-id LAF-7 \\
    --state-name "Done" --reason "PR merged and verified" \\
    --initiating-agent github-copilot --role executor

  # Link a PR to a Linear issue
  python3 linear_gateway.py link_pr_context --issue-id LAF-7 \\
    --pr-url https://github.com/loganfinney27/IDAHO-VAULT/pull/96 \\
    --pr-title "Add CHECKPOINT prompt" \\
    --initiating-agent github-copilot --role coordinator
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any

# ── Local guardrails import ────────────────────────────────────────────────────

_SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(_SCRIPT_DIR))

from mcp_guardrails import (
    MCPActionContext,
    emit_action_log,
    require_live_write,
    resolve_live_write,
)

# ── Constants ──────────────────────────────────────────────────────────────────

LINEAR_API_URL = "https://api.linear.app/graphql"

ALLOWED_ROLES = {"observer", "executor", "coordinator", "secretary"}

# Roles that may perform live writes
WRITE_ROLES = {"executor", "coordinator", "secretary"}


# ── GraphQL client ─────────────────────────────────────────────────────────────

def _gql(query: str, variables: dict[str, Any] | None = None, *, api_key: str) -> dict[str, Any]:
    """Execute a Linear GraphQL query or mutation. Returns the 'data' key."""
    import urllib.request

    payload = json.dumps({"query": query, "variables": variables or {}}).encode("utf-8")
    req = urllib.request.Request(
        LINEAR_API_URL,
        data=payload,
        headers={
            "Content-Type": "application/json",
            "Authorization": api_key,
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        body = json.loads(resp.read().decode("utf-8"))

    if "errors" in body:
        errors = "; ".join(e.get("message", str(e)) for e in body["errors"])
        raise RuntimeError(f"Linear API error: {errors}")

    return body.get("data", {})


def _get_api_key() -> str:
    key = os.environ.get("LINEAR_API_KEY", "")
    if not key:
        print("ERROR: LINEAR_API_KEY environment variable is not set.", file=sys.stderr)
        print("  Add it to GitHub repo secrets or export it locally.", file=sys.stderr)
        sys.exit(1)
    return key


# ── Permission helpers ─────────────────────────────────────────────────────────

def _assert_write_role(role: str, command: str) -> None:
    if role not in WRITE_ROLES:
        print(
            f"ERROR: Role '{role}' cannot perform '{command}'. "
            f"Write roles: {', '.join(sorted(WRITE_ROLES))}.",
            file=sys.stderr,
        )
        sys.exit(1)


# ── YAML output helper ─────────────────────────────────────────────────────────

def _dump_structured(data: dict[str, Any]) -> str:
    """Serialize data as YAML (via PyYAML if available) or JSON fallback.

    Using a real serializer ensures values containing `:`/newlines/booleans are
    safely quoted and the output is always machine-parseable.
    """
    try:
        import yaml  # type: ignore[import]
        return yaml.safe_dump(data, allow_unicode=True, sort_keys=False, default_flow_style=False)
    except ImportError:
        return json.dumps(data, indent=2, ensure_ascii=False)


# ── Issue identifier → UUID resolution ────────────────────────────────────────

def _resolve_issue(identifier: str, *, api_key: str) -> dict[str, Any]:
    """Resolve a human identifier (e.g. 'LAF-7') to the full issue object.

    The Linear GraphQL API supports fetching an issue directly by its human identifier
    via the top-level `issue(id: String!)` field.
    Returns the matching issue node (includes team + team states).
    Raises RuntimeError if no match is found.
    """
    query = """
    query GetIssueByIdentifier($id: String!) {
      issue(id: $id) {
        id
        identifier
        title
        description
        state { name type }
        assignee { name email }
        labels { nodes { name } }
        priority
        updatedAt
        url
        team {
          id
          name
          states { nodes { id name type } }
        }
      }
    }
    """
    data = _gql(query, {"id": identifier}, api_key=api_key)
    node = data.get("issue")
    if not node:
        raise RuntimeError(f"No Linear issue found for identifier '{identifier}'.")
    return node



def cmd_read_issue(args: argparse.Namespace) -> int:
    """Read a Linear issue and print its state to stdout."""
    api_key = _get_api_key()

    ctx = MCPActionContext(
        action_type="linear.read_issue",
        system_or_resource_id=args.issue_id,
        initiating_agent=args.initiating_agent,
        related_ref=args.related_ref,
        payload={"issue_id": args.issue_id},
        live_write=False,
    )

    try:
        issue = _resolve_issue(args.issue_id, api_key=api_key)

        print("---")
        print(_dump_structured({
            "issue": {
                "id": issue.get("identifier"),
                "title": issue.get("title"),
                "state": issue.get("state", {}).get("name"),
                "assignee": (issue.get("assignee") or {}).get("name"),
                "labels": [n["name"] for n in (issue.get("labels") or {}).get("nodes", [])],
                "priority": issue.get("priority"),
                "updated": issue.get("updatedAt"),
                "url": issue.get("url"),
            }
        }), end="")
        emit_action_log(ctx, outcome="success")
        return 0

    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        emit_action_log(ctx, outcome="failure")
        return 1


def cmd_list_project_issues(args: argparse.Namespace) -> int:
    """List all issues in a Linear project."""
    api_key = _get_api_key()

    ctx = MCPActionContext(
        action_type="linear.list_project_issues",
        system_or_resource_id=args.project_id,
        initiating_agent=args.initiating_agent,
        related_ref=args.related_ref,
        payload={"project_id": args.project_id},
        live_write=False,
    )

    query = """
    query GetProject($id: String!) {
      project(id: $id) {
        name
        issues {
          nodes {
            identifier
            title
            state { name }
            assignee { name }
            priority
            updatedAt
          }
        }
      }
    }
    """

    try:
        data = _gql(query, {"id": args.project_id}, api_key=api_key)
        project = data.get("project")
        if not project:
            print(f"ERROR: Project '{args.project_id}' not found.", file=sys.stderr)
            emit_action_log(ctx, outcome="failure")
            return 1

        issues = (project.get("issues") or {}).get("nodes", [])
        print(f"---\nproject: {project.get('name')}\nissues:")
        for issue in issues:
            print(f"  - id: {issue.get('identifier')}")
            print(f"    title: {issue.get('title')}")
            print(f"    state: {issue.get('state', {}).get('name')}")
            print(f"    assignee: {(issue.get('assignee') or {}).get('name')}")
            print(f"    priority: {issue.get('priority')}")

        emit_action_log(ctx, outcome="success")
        return 0

    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        emit_action_log(ctx, outcome="failure")
        return 1


def cmd_post_comment(args: argparse.Namespace) -> int:
    """Post a comment on a Linear issue. Dry-run by default."""
    _assert_write_role(args.role, "post_comment")

    live = resolve_live_write(args.live_write)

    ctx = MCPActionContext(
        action_type="linear.post_comment",
        system_or_resource_id=args.issue_id,
        initiating_agent=args.initiating_agent,
        related_ref=args.related_ref,
        payload={"issue_id": args.issue_id, "body": args.body},
        live_write=live,
    )

    if not live:
        print(f"[DRY RUN] Would post comment to {args.issue_id}:")
        print(f"  body: {args.body}")
        emit_action_log(ctx, outcome="success")
        return 0

    api_key = _get_api_key()
    require_live_write(ctx)

    mutation = """
    mutation PostComment($issueId: String!, $body: String!) {
      commentCreate(input: { issueId: $issueId, body: $body }) {
        success
        comment { id url }
      }
    }
    """

    try:
        issue = _resolve_issue(args.issue_id, api_key=api_key)
        issue_uuid = issue["id"]
        data = _gql(mutation, {"issueId": issue_uuid, "body": args.body}, api_key=api_key)
        result = data.get("commentCreate", {})
        if not result.get("success"):
            print("ERROR: commentCreate returned success=false.", file=sys.stderr)
            emit_action_log(ctx, outcome="failure")
            return 1

        comment = result.get("comment", {})
        print(f"Comment posted: {comment.get('url')}")
        emit_action_log(ctx, outcome="success")
        return 0

    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        emit_action_log(ctx, outcome="failure")
        return 1


def cmd_update_issue_status(args: argparse.Namespace) -> int:
    """Update a Linear issue's workflow state. Dry-run by default."""
    _assert_write_role(args.role, "update_issue_status")

    if not args.reason:
        print("ERROR: --reason is required for update_issue_status.", file=sys.stderr)
        return 1

    live = resolve_live_write(args.live_write)

    ctx = MCPActionContext(
        action_type="linear.update_issue_status",
        system_or_resource_id=args.issue_id,
        initiating_agent=args.initiating_agent,
        related_ref=args.related_ref,
        payload={"issue_id": args.issue_id, "state_name": args.state_name, "reason": args.reason},
        live_write=live,
    )

    if not live:
        print(f"[DRY RUN] Would update {args.issue_id} status to '{args.state_name}'")
        print(f"  reason: {args.reason}")
        emit_action_log(ctx, outcome="success")
        return 0

    api_key = _get_api_key()
    require_live_write(ctx)

    try:
        # Resolve identifier → UUID and fetch team states in one query
        issue = _resolve_issue(args.issue_id, api_key=api_key)
        issue_uuid = issue["id"]
        team = issue.get("team") or {}
        team_states = (team.get("states") or {}).get("nodes") or []

        if not team_states:
            print(
                f"ERROR: No workflow states found for issue '{issue.get('identifier')}' team '{team.get('name')}'.",
                file=sys.stderr,
            )
            emit_action_log(ctx, outcome="failure")
            return 1

        matching = [s for s in team_states if s.get("name", "").lower() == args.state_name.lower()]
        if not matching:
            available = [s.get("name") for s in team_states]
            print(
                f"ERROR: State '{args.state_name}' not found for team '{team.get('name')}'. "
                f"Available: {available}",
                file=sys.stderr,
            )
            emit_action_log(ctx, outcome="failure")
            return 1

        state_id = matching[0]["id"]

        # Update issue state
        update_mutation = """
        mutation UpdateIssue($id: String!, $stateId: String!) {
          issueUpdate(id: $id, input: { stateId: $stateId }) {
            success
            issue { id identifier state { name } }
          }
        }
        """
        update_data = _gql(update_mutation, {"id": issue_uuid, "stateId": state_id}, api_key=api_key)
        result = update_data.get("issueUpdate", {})
        if not result.get("success"):
            print("ERROR: issueUpdate returned success=false.", file=sys.stderr)
            emit_action_log(ctx, outcome="failure")
            return 1

        issue = result.get("issue", {})
        print(f"Issue {issue.get('identifier')} status updated to: {issue.get('state', {}).get('name')}")
        emit_action_log(ctx, outcome="success")
        return 0

    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        emit_action_log(ctx, outcome="failure")
        return 1


def cmd_link_pr_context(args: argparse.Namespace) -> int:
    """Attach a PR URL to a Linear issue. Dry-run by default."""
    _assert_write_role(args.role, "link_pr_context")

    live = resolve_live_write(args.live_write)

    ctx = MCPActionContext(
        action_type="linear.link_pr_context",
        system_or_resource_id=args.issue_id,
        initiating_agent=args.initiating_agent,
        related_ref=args.related_ref,
        payload={"issue_id": args.issue_id, "pr_url": args.pr_url, "pr_title": args.pr_title},
        live_write=live,
    )

    if not live:
        print(f"[DRY RUN] Would attach PR to {args.issue_id}:")
        print(f"  url:   {args.pr_url}")
        print(f"  title: {args.pr_title}")
        emit_action_log(ctx, outcome="success")
        return 0

    api_key = _get_api_key()
    require_live_write(ctx)

    mutation = """
    mutation LinkPR($issueId: String!, $url: String!, $title: String!) {
      attachmentCreate(input: {
        issueId: $issueId
        url: $url
        title: $title
        subtitle: "GitHub PR"
      }) {
        success
        attachment { id url }
      }
    }
    """

    try:
        issue = _resolve_issue(args.issue_id, api_key=api_key)
        issue_uuid = issue["id"]
        data = _gql(
            mutation,
            {"issueId": issue_uuid, "url": args.pr_url, "title": args.pr_title},
            api_key=api_key,
        )
        result = data.get("attachmentCreate", {})
        if not result.get("success"):
            print("ERROR: attachmentCreate returned success=false.", file=sys.stderr)
            emit_action_log(ctx, outcome="failure")
            return 1

        attachment = result.get("attachment", {})
        print(f"PR linked: {attachment.get('url')}")
        emit_action_log(ctx, outcome="success")
        return 0

    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        emit_action_log(ctx, outcome="failure")
        return 1


# ── Argument parser ────────────────────────────────────────────────────────────

def _common_args(parser: argparse.ArgumentParser) -> None:
    """Add shared arguments to a subcommand parser."""
    parser.add_argument(
        "--initiating-agent",
        required=True,
        help="Agent name (e.g. github-copilot, claude-code). Logged in MCP action log.",
    )
    parser.add_argument(
        "--role",
        required=True,
        choices=sorted(ALLOWED_ROLES),
        help="Agent role for this invocation.",
    )
    parser.add_argument(
        "--related-ref",
        default=os.environ.get("GITHUB_REF", "unknown"),
        help="Git ref or branch name for MCP log correlation.",
    )
    parser.add_argument(
        "--live-write",
        action="store_true",
        default=False,
        help="Enable live writes. Also controlled by MCP_LIVE_WRITE env var.",
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Swarm Linear Gateway — broker for all swarm agent reads/writes to Linear",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # read_issue
    p_read = sub.add_parser("read_issue", help="Read a Linear issue")
    p_read.add_argument("--issue-id", required=True, help="Linear issue identifier (e.g. LAF-7)")
    _common_args(p_read)

    # list_project_issues
    p_list = sub.add_parser("list_project_issues", help="List issues in a Linear project")
    p_list.add_argument("--project-id", required=True, help="Linear project UUID")
    _common_args(p_list)

    # post_comment
    p_comment = sub.add_parser("post_comment", help="Post a comment on a Linear issue")
    p_comment.add_argument("--issue-id", required=True, help="Linear issue identifier")
    p_comment.add_argument("--body", required=True, help="Comment body text")
    _common_args(p_comment)

    # update_issue_status
    p_status = sub.add_parser("update_issue_status", help="Update a Linear issue's workflow state")
    p_status.add_argument("--issue-id", required=True, help="Linear issue identifier")
    p_status.add_argument("--state-name", required=True, help="Target state name (e.g. 'In Progress', 'Done')")
    p_status.add_argument("--reason", required=True, help="Why this status change is happening (required)")
    _common_args(p_status)

    # link_pr_context
    p_link = sub.add_parser("link_pr_context", help="Attach a GitHub PR to a Linear issue")
    p_link.add_argument("--issue-id", required=True, help="Linear issue identifier")
    p_link.add_argument("--pr-url", required=True, help="Full GitHub PR URL")
    p_link.add_argument("--pr-title", required=True, help="PR title for the attachment label")
    _common_args(p_link)

    return parser


# ── Entry point ────────────────────────────────────────────────────────────────

COMMANDS = {
    "read_issue": cmd_read_issue,
    "list_project_issues": cmd_list_project_issues,
    "post_comment": cmd_post_comment,
    "update_issue_status": cmd_update_issue_status,
    "link_pr_context": cmd_link_pr_context,
}


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    handler = COMMANDS.get(args.command)
    if not handler:
        print(f"ERROR: Unknown command '{args.command}'", file=sys.stderr)
        return 1
    return handler(args)


if __name__ == "__main__":
    sys.exit(main())
