#!/usr/bin/env python3
"""Janitor sweep: detect failed workflow runs and route structured alerts.

Hexagonal design:
  - Input adapter: GitHub workflow_run event payload parser.
  - Domain model: FailedRunEvent dataclass.
  - Output adapters: Linear comment reporter + Slack webhook reporter.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol


@dataclass(frozen=True)
class FailedRunEvent:
    workflow_name: str
    workflow_url: str
    repository: str
    branch: str
    conclusion: str
    run_id: int


class Reporter(Protocol):
    def send(self, event: FailedRunEvent, body: str) -> tuple[bool, str]: ...


class LinearReporter:
    def __init__(self, issue_id: str, alias: str) -> None:
        self.issue_id = issue_id
        self.alias = alias

    def send(self, event: FailedRunEvent, body: str) -> tuple[bool, str]:
        script = Path(__file__).with_name("linear_gateway.py")
        cmd = [
            "python3",
            str(script),
            "post_comment",
            "--issue-id",
            self.issue_id,
            "--body",
            body,
            "--initiating-agent",
            self.alias,
            "--role",
            "secretary",
            "--live-write",
        ]
        env = {**os.environ, "MCP_LIVE_WRITE": "true"}
        try:
            proc = subprocess.run(cmd, capture_output=True, text=True, timeout=60, env=env)
        except subprocess.TimeoutExpired:
            return False, "linear failed: timeout while posting comment"
        if proc.returncode == 0:
            return True, "linear comment posted"
        detail = (proc.stderr or proc.stdout).strip()[-240:]
        return False, f"linear failed: {detail}"


class SlackReporter:
    def __init__(self, webhook_url: str) -> None:
        self.webhook_url = webhook_url

    def send(self, event: FailedRunEvent, body: str) -> tuple[bool, str]:
        payload = json.dumps({"text": body}).encode("utf-8")
        req = urllib.request.Request(
            self.webhook_url,
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=20) as resp:
                if 200 <= resp.status < 300:
                    return True, "slack posted"
                return False, f"slack http status {resp.status}"
        except Exception as exc:  # network or webhook errors
            return False, f"slack failed: {exc}"


def parse_failed_event(event_path: Path) -> FailedRunEvent | None:
    payload = json.loads(event_path.read_text(encoding="utf-8"))
    workflow_run = payload.get("workflow_run") or {}
    if workflow_run.get("conclusion") != "failure":
        return None

    repo = payload.get("repository") or {}
    return FailedRunEvent(
        workflow_name=workflow_run.get("name", "(unknown workflow)"),
        workflow_url=workflow_run.get("html_url", ""),
        repository=repo.get("full_name", ""),
        branch=workflow_run.get("head_branch", ""),
        conclusion=workflow_run.get("conclusion", ""),
        run_id=int(workflow_run.get("id") or 0),
    )


def build_message(event: FailedRunEvent) -> str:
    return (
        "🧹 Janitor Sweep: failed check detected\n"
        f"• Workflow: {event.workflow_name}\n"
        f"• Repo: {event.repository}\n"
        f"• Branch: {event.branch}\n"
        f"• Run: {event.workflow_url or event.run_id}\n"
        "• Next: inspect failed logs and open remediation PR."
    )


def main() -> int:
    event_path = Path(os.environ.get("GITHUB_EVENT_PATH", ""))
    if not event_path.exists():
        print("ERROR: GITHUB_EVENT_PATH is not available", file=sys.stderr)
        return 2

    event = parse_failed_event(event_path)
    if event is None:
        print(json.dumps({"status": "noop", "reason": "workflow conclusion is not failure"}))
        return 0

    message = build_message(event)
    alias = os.environ.get("JANITOR_ALIAS", "janitor-bot")

    reporters: list[Reporter] = []
    linear_issue = os.environ.get("JANITOR_LINEAR_ISSUE_ID", "").strip()
    if linear_issue and os.environ.get("LINEAR_API_KEY", "").strip():
        reporters.append(LinearReporter(issue_id=linear_issue, alias=alias))

    slack_webhook = os.environ.get("JANITOR_SLACK_WEBHOOK_URL", "").strip()
    if slack_webhook:
        reporters.append(SlackReporter(slack_webhook))

    results: list[dict[str, str | bool]] = []
    if not reporters:
        results.append({"target": "none", "ok": True, "detail": "no reporters configured"})
    else:
        for reporter in reporters:
            ok, detail = reporter.send(event, message)
            results.append({"target": reporter.__class__.__name__, "ok": ok, "detail": detail})

    structured = {
        "status": "processed",
        "event": {
            "workflow": event.workflow_name,
            "repository": event.repository,
            "branch": event.branch,
            "run_id": event.run_id,
            "conclusion": event.conclusion,
        },
        "outputs": results,
    }
    print(json.dumps(structured))

    # We intentionally do not fail the workflow if reporting sinks are unavailable.
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
