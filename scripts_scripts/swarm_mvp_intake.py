#!/usr/bin/env python3
"""Create a gated Swarm MVP intake artifact from a GitHub-dispatched command."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path

SUPPORTED_COMMAND = "process document"
OUTPUT_ROOT = Path("INBOX") / "SWARM-MVP"
SAFE_TOKEN_RE = re.compile(r"[^A-Za-z0-9._-]+")


@dataclass(frozen=True)
class IntakeResult:
    output_path: Path
    relative_output_path: str
    title: str
    command: str
    run_id: str
    attempt: int
    manifest: str


def normalize_command(command: str) -> str:
    return " ".join(command.strip().lower().split())


def route_command(command: str) -> str:
    normalized = normalize_command(command)
    if normalized != SUPPORTED_COMMAND:
        raise ValueError(
            f"Unsupported command {command!r}. Swarm MVP v1 only supports {SUPPORTED_COMMAND!r}."
        )
    return normalized


def sanitize_token(value: str, *, field_name: str) -> str:
    token = SAFE_TOKEN_RE.sub("-", value.strip()).strip(".-_")
    if not token:
        raise ValueError(f"{field_name} must contain at least one safe filename character.")
    return token[:80]


def repo_relative_path(value: str | Path, *, field_name: str) -> Path:
    path = Path(value)
    if path.is_absolute():
        raise ValueError(f"{field_name} must be a repo-relative path, got {value!r}.")

    parts = []
    for part in path.parts:
        if part in {"", "."}:
            continue
        if part == "..":
            raise ValueError(f"{field_name} must not contain '..', got {value!r}.")
        parts.append(part)

    if not parts:
        raise ValueError(f"{field_name} must not be empty.")
    return Path(*parts)


def validate_output_root(value: str | Path) -> Path:
    output_root = repo_relative_path(value, field_name="output_root")
    if output_root.as_posix() != OUTPUT_ROOT.as_posix():
        raise ValueError(f"output_root must be {OUTPUT_ROOT.as_posix()!r}, got {value!r}.")
    return output_root


def next_output_path(output_root: Path, command: str, run_id: str) -> tuple[Path, int]:
    command_slug = route_command(command).replace(" ", "-")
    run_token = sanitize_token(run_id, field_name="run_id")
    stem = f"{command_slug}-{run_token}"

    for attempt in range(1, 1000):
        candidate = output_root / f"{stem}-{attempt}.md"
        if not candidate.exists():
            return candidate, attempt

    raise RuntimeError(f"No available output path for {stem!r} under {output_root}.")


def yaml_string(value: str) -> str:
    return json.dumps(value, ensure_ascii=True)


def render_frontmatter(fields: dict[str, str]) -> str:
    lines = ["---"]
    for key, value in fields.items():
        lines.append(f"{key}: {yaml_string(value)}")
    lines.append("---")
    return "\n".join(lines)


def indent_payload(payload: str) -> str:
    if not payload:
        return "    "
    return "\n".join(f"    {line}" if line else "    " for line in payload.splitlines())


def render_artifact(
    *,
    command: str,
    payload: str,
    run_id: str,
    run_at: str,
    agent_id: str,
    github_issue: str | None,
    linear_ref: str | None,
) -> tuple[str, str]:
    title = f"Swarm MVP intake - {command} - {run_id}"
    fields = {
        "title": title,
        "updated": run_at,
        "status": "staged",
        "authority": agent_id,
        "source_command": command,
        "github_run_id": run_id,
    }
    if github_issue:
        fields["github_issue"] = github_issue
    if linear_ref:
        fields["linear_ref"] = linear_ref

    body = [
        render_frontmatter(fields),
        "",
        f"# {title}",
        "",
        "## Command",
        "",
        command,
        "",
        "## Payload",
        "",
        indent_payload(payload),
        "",
        "## Routing",
        "",
        "- control_plane: github",
        "- artifact_root: INBOX/SWARM-MVP",
        "- connector_posture: satellites advisory only",
        "",
    ]
    return title, "\n".join(body)


def create_intake_artifact(
    *,
    command: str,
    payload: str,
    run_id: str,
    run_at: str,
    agent_id: str,
    manifest: str,
    output_root: str | Path,
    github_issue: str | None = None,
    linear_ref: str | None = None,
) -> IntakeResult:
    routed_command = route_command(command)
    run_token = sanitize_token(run_id, field_name="run_id")
    safe_agent_id = agent_id.strip()
    if not safe_agent_id:
        raise ValueError("agent_id must not be empty.")

    root = validate_output_root(output_root)
    path, attempt = next_output_path(root, routed_command, run_token)
    title, content = render_artifact(
        command=routed_command,
        payload=payload,
        run_id=run_token,
        run_at=run_at.strip(),
        agent_id=safe_agent_id,
        github_issue=(github_issue or "").strip() or None,
        linear_ref=(linear_ref or "").strip() or None,
    )

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")
    return IntakeResult(
        output_path=path,
        relative_output_path=path.as_posix(),
        title=title,
        command=routed_command,
        run_id=run_token,
        attempt=attempt,
        manifest=str(repo_relative_path(manifest, field_name="manifest")),
    )


def emit_github_outputs(result: IntakeResult) -> None:
    github_output = os.environ.get("GITHUB_OUTPUT")
    if not github_output:
        return
    with open(github_output, "a", encoding="utf-8") as fh:
        fh.write(f"output_path={result.relative_output_path}\n")
        fh.write(f"title={result.title}\n")
        fh.write(f"attempt={result.attempt}\n")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--command", required=True)
    parser.add_argument("--payload", required=True)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--run-at", required=True)
    parser.add_argument("--agent-id", required=True)
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--output-root", required=True)
    parser.add_argument("--github-issue", default="")
    parser.add_argument("--linear-ref", default="")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        result = create_intake_artifact(
            command=args.command,
            payload=args.payload,
            run_id=args.run_id,
            run_at=args.run_at,
            agent_id=args.agent_id,
            manifest=args.manifest,
            output_root=args.output_root,
            github_issue=args.github_issue,
            linear_ref=args.linear_ref,
        )
    except Exception as exc:
        print(f"swarm_mvp_intake.py failed: {exc}", file=sys.stderr)
        return 1

    emit_github_outputs(result)
    print(json.dumps(result.__dict__ | {"output_path": result.relative_output_path}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
