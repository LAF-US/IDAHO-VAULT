#!/usr/bin/env python3
"""Reusable guardrails for MCP-mediated automation.

This module standardizes three pieces of behavior required by the vault's
MCP rollout plan:

1. Explicit live-write opt-in
2. Stable correlation and idempotency keys
3. Structured YAML-like action logs

The helpers are transport-agnostic and are intended for scripts under
`.github/scripts/` that broker external systems or local plugin APIs.
"""

from __future__ import annotations

import hashlib
import json
import os
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any


def _canonical_json(value: Any) -> str:
    """Serialize a value deterministically for hashing and debug output."""
    return json.dumps(value, so***REMOVED***keys=True, separators=(",", ":"), ensure_ascii=True)


def _truthy(value: str | None) -> bool:
    """Interpret common truthy environment values."""
    if value is None:
        return False
    return value.strip().lower() in {"1", "true", "yes", "on"}


def resolve_live_write(explicit_live_write: bool = False, env_var: str = "MCP_LIVE_WRITE") -> bool:
    """Return whether a script is allowed to perform live writes."""
    return explicit_live_write or _truthy(os.environ.get(env_var))


def make_idempotency_key(*, action_type: str, system_or_resource_id: str, payload: Any, scope: str = "daily") -> str:
    """Build a deterministic idempotency key for a logical action.

    The key is deterministic for the supplied payload and scope. Daily scope is
    the default because the current implementation plan calls for a conservative,
    bounded retry window rather than indefinite replay suppression.
    """
    components = {
        "action_type": action_type,
        "system_or_resource_id": system_or_resource_id,
        "payload": payload,
        "scope": scope,
        "date": datetime.now(timezone.utc).strftime("%Y-%m-%d") if scope == "daily" else scope,
    }
    digest = hashlib.sha256(_canonical_json(components).encode("utf-8")).hexdigest()
    return digest[:24]


def make_correlation_id(*, initiating_agent: str, action_type: str, system_or_resource_id: str, payload: Any) -> str:
    """Build a stable correlation ID for log aggregation and replay tracing."""
    seed = {
        "initiating_agent": initiating_agent,
        "action_type": action_type,
        "system_or_resource_id": system_or_resource_id,
        "payload": payload,
    }
    digest = hashlib.sha256(_canonical_json(seed).encode("utf-8")).hexdigest()[:12]
    date_part = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    return f"{date_part}-{digest}"


@dataclass(slots=True)
class MCPActionContext:
    """Normalized metadata for a single MCP-mediated action attempt."""

    action_type: str
    system_or_resource_id: str
    initiating_agent: str
    related_ref: str
    payload: Any
    live_write: bool = False
    retry_count: int = 0
    correlation_id: str | None = None
    idempotency_key: str | None = None

    def __post_init__(self) -> None:
        if self.correlation_id is None:
            self.correlation_id = make_correlation_id(
                initiating_agent=self.initiating_agent,
                action_type=self.action_type,
                system_or_resource_id=self.system_or_resource_id,
                payload=self.payload,
            )
        if self.idempotency_key is None:
            self.idempotency_key = make_idempotency_key(
                action_type=self.action_type,
                system_or_resource_id=self.system_or_resource_id,
                payload=self.payload,
            )


def emit_action_log(context: MCPActionContext, *, outcome: str) -> None:
    """Emit the vault's required MCP action log template to stdout."""
    if outcome not in {"success", "failure"}:
        raise ValueError("outcome must be 'success' or 'failure'")

    log = {
        "mcp_action_log": {
            "action_type": context.action_type,
            "system_or_resource_id": context.system_or_resource_id,
            "initiating_agent": context.initiating_agent,
            "correlation_id": context.correlation_id,
            "outcome": outcome,
            "retry_count": context.retry_count,
            "related_ref": context.related_ref,
            "idempotency_key": context.idempotency_key,
            "live_write": context.live_write,
        }
    }
    print(_yaml_dump(log))


def require_live_write(context: MCPActionContext) -> None:
    """Fail closed when a write path is attempted without explicit opt-in."""
    if not context.live_write:
        raise PermissionError(
            "Live write blocked. Re-run with --live-write or set MCP_LIVE_WRITE=true."
        )


def _yaml_scalar(value: Any) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, int):
        return str(value)
    return json.dumps(str(value), ensure_ascii=True)


def _yaml_dump(value: Any, indent: int = 0) -> str:
    if isinstance(value, dict):
        lines: list[str] = []
        prefix = " " * indent
        for key, item in value.items():
            if isinstance(item, (dict, list)):
                lines.append(f"{prefix}{key}:")
                lines.append(_yaml_dump(item, indent + 2))
            else:
                lines.append(f"{prefix}{key}: {_yaml_scalar(item)}")
        return "\n".join(lines)
    if isinstance(value, list):
        lines = []
        prefix = " " * indent
        for item in value:
            if isinstance(item, (dict, list)):
                lines.append(f"{prefix}-")
                lines.append(_yaml_dump(item, indent + 2))
            else:
                lines.append(f"{prefix}- {_yaml_scalar(item)}")
        return "\n".join(lines)
    return f"{' ' * indent}{_yaml_scalar(value)}"