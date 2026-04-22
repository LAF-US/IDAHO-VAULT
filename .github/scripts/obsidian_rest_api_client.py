#!/usr/bin/env python3
"""Minimal Obsidian Local REST API client with vault guardrails.

This script targets the installed `obsidian-local-rest-api` plugin and is
intended as the first concrete transport layer for plugin-backed automation.

Key properties:
  - Uses the plugin's HTTPS API with Bearer authentication
  - Defaults to read-safe operations; note mutations require explicit opt-in
  - Emits structured MCP action logs for each request attempt
  - Supports dry-run planning for write paths

This client is useful for local execution and for any future environment where
the Obsidian API endpoint is reachable. GitHub-hosted runners cannot reach a
local desktop plugin endpoint unless an explicit relay layer is introduced.
"""

from __future__ import annotations

import argparse
import json
import ssl
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib import error, parse, request

from mcp_guardrails import MCPActionContext, emit_action_log, require_live_write, resolve_live_write


DEFAULT_BASE_URL = "https://127.0.0.1:27124"
DEFAULT_AGENT = "agent:copilot"
DEFAULT_RELATED_REF = ".github/scripts/obsidian_rest_api_client.py"


class ObsidianApiError(RuntimeError):
    """Raised when the Obsidian Local REST API returns an error."""


@dataclass(slots=True)
class ClientConfig:
    base_url: str
    api_key: str
    insecure: bool = False
    ca_cert: str | None = None


class ObsidianRestApiClient:
    """Thin client around the Obsidian Local REST API plugin."""

    def __init__(self, config: ClientConfig) -> None:
        self.config = config
        self.ssl_context = self._build_ssl_context(config)

    def status(self) -> Any:
        return self._request("GET", "/", auth_required=False)

    def list_root(self) -> Any:
        return self._request("GET", "/vault/")

    def read_note(self, path: str) -> Any:
        return self._request("GET", self._vault_path(path))

    def write_note(self, path: str, content: str) -> Any:
        return self._request(
            "PUT",
            self._vault_path(path),
            data=content.encode("utf-8"),
            headers={"Content-Type": "text/plain; charset=utf-8"},
        )

    def patch_note(
        self,
        path: str,
        *,
        operation: str,
        target_type: str,
        target: str,
        content: str,
        content_type: str,
    ) -> Any:
        return self._request(
            "PATCH",
            self._vault_path(path),
            data=content.encode("utf-8"),
            headers={
                "Content-Type": content_type,
                "Operation": operation,
                "Target-Type": target_type,
                "Target": target,
            },
        )

    def simple_search(self, query: str) -> Any:
        encoded = parse.urlencode({"query": query})
        return self._request("POST", f"/search/simple/?{encoded}")

    def _request(
        self,
        method: str,
        endpoint: str,
        *,
        data: bytes | None = None,
        headers: dict[str, str] | None = None,
        auth_required: bool = True,
    ) -> Any:
        merged_headers = dict(headers or {})
        if auth_required:
            merged_headers["Authorization"] = f"Bearer {self.config.api_key}"

        req = request.Request(
            url=f"{self.config.base_url.rstrip('/')}{endpoint}",
            method=method,
            headers=merged_headers,
            data=data,
        )

        try:
            with request.urlopen(req, context=self.ssl_context) as response:
                body = response.read()
                content_type = response.headers.get("Content-Type", "")
                return _decode_response(body, content_type)
        except error.HTTPError as exc:
            body = exc.read().decode("utf-8", errors="replace")
            raise ObsidianApiError(f"HTTP {exc.code}: {body}") from exc
        except error.URLError as exc:
            raise ObsidianApiError(f"Connection failed: {exc}") from exc

    @staticmethod
    def _build_ssl_context(config: ClientConfig) -> ssl.SSLContext:
        if config.insecure:
            return ssl._create_unverified_context()
        if config.ca_cert:
            return ssl.create_default_context(cafile=config.ca_cert)
        return ssl.create_default_context()

    @staticmethod
    def _vault_path(path: str) -> str:
        trimmed = path.lstrip("/")
        quoted = parse.quote(trimmed, safe="/-_.~")
        return f"/vault/{quoted}"


def _decode_response(body: bytes, content_type: str) -> Any:
    text = body.decode("utf-8", errors="replace")
    if "application/json" in content_type:
        return json.loads(text)
    if text:
        return text
    return {"ok": True}


def _load_content(args: argparse.Namespace) -> str:
    if args.content is not None:
        return args.content
    if args.content_file is not None:
        return Path(args.content_file).read_text(encoding="utf-8")
    raise ValueError("Write and patch operations require --content or --content-file.")


def _print_result(result: Any) -> None:
    if isinstance(result, (dict, list)):
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return
    print(result)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Obsidian Local REST API client")
    parser.add_argument(
        "command",
        choices=["status", "list-root", "read", "write", "patch", "search-simple"],
        help="Operation to perform against the Obsidian Local REST API.",
    )
    parser.add_argument("--path", help="Vault-relative file path for read/write/patch operations.")
    parser.add_argument("--query", help="Search query for search-simple.")
    parser.add_argument("--content", help="Inline content for write or patch operations.")
    parser.add_argument("--content-file", help="Path to a local file containing content to send.")
    parser.add_argument("--operation", choices=["append", "prepend", "replace"], help="Patch operation.")
    parser.add_argument("--target-type", choices=["heading", "block", "frontmatter"], help="Patch target type.")
    parser.add_argument("--target", help="Patch target value such as a heading name or frontmatter key.")
    parser.add_argument("--content-type", default="text/plain; charset=utf-8", help="Request content type.")
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL, help="Obsidian API base URL.")
    parser.add_argument("--api-key", help="Obsidian API key. Falls back to OBSIDIAN_REST_API_KEY.")
    parser.add_argument("--insecure", action="store_true", help="Disable TLS verification for the self-signed plugin certificate.")
    parser.add_argument("--ca-cert", help="Path to a trusted certificate for the Obsidian API.")
    parser.add_argument("--live-write", action="store_true", help="Allow write and patch requests to be sent.")
    parser.add_argument("--initiating-agent", default=DEFAULT_AGENT, help="Agent name for structured action logs.")
    parser.add_argument("--related-ref", default=DEFAULT_RELATED_REF, help="Related issue, PR, or file reference for structured action logs.")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    live_write = resolve_live_write(args.live_write)
    api_key = args.api_key or __impo***REMOVED***_("os").environ.get("OBSIDIAN_REST_API_KEY")
    needs_api_key = args.command in {"list-root", "read", "search-simple"} or (
        args.command in {"write", "patch"} and live_write
    )
    if needs_api_key and not api_key:
        print("ERROR: Missing API key. Use --api-key or set OBSIDIAN_REST_API_KEY.", file=sys.stderr)
        return 1

    config = ClientConfig(
        base_url=args.base_url,
        api_key=api_key or "",
        insecure=args.insecure,
        ca_cert=args.ca_cert,
    )
    client = ObsidianRestApiClient(config)

    payload = {
        "command": args.command,
        "path": args.path,
        "query": args.query,
        "operation": args.operation,
        "target_type": args.target_type,
        "target": args.target,
    }
    resource_id = args.path or args.base_url
    action_type = "write_resource" if args.command in {"write", "patch"} else "read_resource"
    context = MCPActionContext(
        action_type=action_type,
        system_or_resource_id=f"obsidian-local-rest-api:{resource_id}",
        initiating_agent=args.initiating_agent,
        related_ref=args.related_ref,
        payload=payload,
        live_write=live_write,
    )

    try:
        if args.command == "status":
            result = client.status()
        elif args.command == "list-root":
            result = client.list_root()
        elif args.command == "read":
            if not args.path:
                parser.error("read requires --path")
            result = client.read_note(args.path)
        elif args.command == "search-simple":
            if not args.query:
                parser.error("search-simple requires --query")
            result = client.simple_search(args.query)
        elif args.command == "write":
            if not args.path:
                parser.error("write requires --path")
            content = _load_content(args)
            if not live_write:
                result = {
                    "dry_run": True,
                    "method": "PUT",
                    "path": args.path,
                    "content_bytes": len(content.encode("utf-8")),
                    "idempotency_key": context.idempotency_key,
                    "correlation_id": context.correlation_id,
                }
            else:
                require_live_write(context)
                result = client.write_note(args.path, content)
        else:
            if not args.path:
                parser.error("patch requires --path")
            if not args.operation or not args.target_type or not args.target:
                parser.error("patch requires --operation, --target-type, and --target")
            content = _load_content(args)
            if not live_write:
                result = {
                    "dry_run": True,
                    "method": "PATCH",
                    "path": args.path,
                    "operation": args.operation,
                    "target_type": args.target_type,
                    "target": args.target,
                    "content_bytes": len(content.encode("utf-8")),
                    "idempotency_key": context.idempotency_key,
                    "correlation_id": context.correlation_id,
                }
            else:
                require_live_write(context)
                result = client.patch_note(
                    args.path,
                    operation=args.operation,
                    target_type=args.target_type,
                    target=args.target,
                    content=content,
                    content_type=args.content_type,
                )

        emit_action_log(context, outcome="success")
        _print_result(result)
        return 0
    except (ObsidianApiError, PermissionError, ValueError) as exc:
        emit_action_log(context, outcome="failure")
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())