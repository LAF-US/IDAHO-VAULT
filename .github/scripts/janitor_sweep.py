#!/usr/bin/env python3
"""Janitor sweep: detect failed workflow runs and route structured alerts.

Hexagonal design:
  - Input adapter: GitHub workflow_run event payload parser.
  - Domain model: FailedRunEvent dataclass.
  - Output adapters: Slack webhook reporter.
"""

from __future__ import annotations

import json
import os
import sys
import urllib.parse
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


class SlackReporter:
    def __init__(self, webhook_url: str) -> None:
        # urlopen honours file:// and ftp://, so the scheme is checked where the
        # URL enters rather than trusted because it came from the environment.
        # A JANITOR_SLACK_WEBHOOK_URL set to file:///etc/passwd would otherwise
        # read local disk and report the result as a delivery failure.
        scheme = urllib.parse.urlparse(webhook_url).scheme
        if scheme != "https":
            raise ValueError(f"Slack webhook must be https, got {scheme!r}")
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
    setup_failures: list[dict[str, str | bool]] = []
    slack_webhook = os.environ.get("JANITOR_SLACK_WEBHOOK_URL", "").strip()
    if slack_webhook:
        # A misconfigured webhook is an unavailable sink, not a reason to abort.
        # The scheme guard raises, and letting that escape would kill the script
        # before it prints any JSON -- losing the failure report this run exists
        # to deliver. The scheme is NOT echoed back: the webhook URL is itself
        # the credential, and this output is a workflow log.
        try:
            reporters.append(SlackReporter(slack_webhook))
        except ValueError:
            setup_failures.append({
                "target": "SlackReporter",
                "ok": False,
                "detail": "JANITOR_SLACK_WEBHOOK_URL is not an https URL; sink skipped",
            })

    results: list[dict[str, str | bool]] = list(setup_failures)
    if not reporters and not setup_failures:
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
