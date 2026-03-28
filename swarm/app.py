#!/usr/bin/env python3
"""IDAHO-VAULT minimal swarm execution loop (v0.1).

Usage:
    python swarm/app.py "process document"
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

VAULT_ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = VAULT_ROOT / "manifest.json"


class RouterAgent:
    """Stateless router that maps trigger text to an action."""

    def route(self, trigger: str) -> str:
        normalized = trigger.strip().lower()
        if "process document" in normalized:
            return "ingest"
        raise ValueError(f"No route found for trigger: {trigger}")


@dataclass
class ExecutorAgent:
    """Executes routed actions using file-based vault tools only."""

    agent_name: str = "executor"

    def execute(self, action: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
        payload = payload or {}
        if action != "ingest":
            raise ValueError(f"Unsupported action: {action}")

        timestamp = _utc_now_iso()
        safe_stamp = timestamp.replace(":", "-").replace(".", "-")
        path = payload.get("path", f"INBOX/ingest-{safe_stamp}.md")
        description = payload.get("description", "Raw ingested document")

        content = payload.get(
            "content",
            "\n".join(
                [
                    "# Ingested Document",
                    "",
                    f"- created_at: {timestamp}",
                    f"- action: {action}",
                    "",
                    "## Source",
                    "Manual trigger: process document",
                    "",
                    "## Notes",
                    "Placeholder ingest output (MVP loop).",
                    "",
                ]
            ),
        )

        write_file(path, content)
        entry = {
            "path": path,
            "last_modified": timestamp,
            "status": "open",
            "type": action,
            "description": description,
            "last_agent": self.agent_name,
        }
        update_manifest(entry)
        return entry


def read_manifest() -> dict[str, Any]:
    if not MANIFEST_PATH.exists():
        return {"files": []}
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


def write_file(path: str, content: str) -> None:
    full_path = VAULT_ROOT / path
    full_path.parent.mkdir(parents=True, exist_ok=True)
    full_path.write_text(content, encoding="utf-8")


def update_manifest(entry: dict[str, Any]) -> None:
    manifest = read_manifest()
    files = manifest.setdefault("files", [])

    for idx, existing in enumerate(files):
        if existing.get("path") == entry["path"]:
            files[idx] = entry
            break
    else:
        files.append(entry)

    MANIFEST_PATH.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def run(trigger: str) -> dict[str, Any]:
    router = RouterAgent()
    executor = ExecutorAgent()
    action = router.route(trigger)
    return executor.execute(action)


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the minimal IDAHO-VAULT swarm loop.")
    parser.add_argument("trigger", help='Trigger text, e.g. "process document"')
    args = parser.parse_args()

    entry = run(args.trigger)
    print(json.dumps({"status": "ok", "entry": entry}, indent=2))


if __name__ == "__main__":
    main()
