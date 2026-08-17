#!/usr/bin/env python3
"""Materialize the OpenRouter runtime environment without printing credentials."""

from __future__ import annotations

import os
import pathlib
import re
import sys
import tempfile


REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
ENV_FILE = REPO_ROOT / ".op" / "openrouter.env"
KEY_RE = re.compile(r"^(?:export\s+)?([A-Z][A-Z0-9_]*)=(.*)$")
SECRET_PLACEHOLDERS = frozenset(
    {
        "<OPENROUTER_SECRET_REF>",
        "CHANGE_TO_MANAGEMENT_KEY_OP_REF",
    }
)


def unquote(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        return value[1:-1]
    return value


def parse_env_content(content: str) -> dict[str, str]:
    """Parse non-empty KEY=value lines without interpreting shell syntax."""
    values: dict[str, str] = {}
    for raw_line in content.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        match = KEY_RE.match(line)
        if match:
            values[match.group(1)] = unquote(match.group(2))
    return values


def _is_usable_secret_source(value: str | None) -> bool:
    return bool(value and value.strip() and value.strip() not in SECRET_PLACEHOLDERS)


def read_env_values(path: pathlib.Path | None = None) -> dict[str, str]:
    path = ENV_FILE if path is None else path
    if not path.exists():
        return {}
    return parse_env_content(path.read_text(encoding="utf-8"))


def select_secret_source(existing_values: dict[str, str]) -> str:
    """Choose an explicit runtime secret or 1Password reference without exposing it."""
    environment_value = os.environ.get("OPENROUTER_API_KEY")
    existing_value = existing_values.get("OPENROUTER_API_KEY")
    source = next(
        (
            value.strip()
            for value in (environment_value, existing_value)
            if _is_usable_secret_source(value)
        ),
        None,
    )
    if source is None:
        raise RuntimeError(
            "OPENROUTER_API_KEY is not configured. Copy .op/openrouter.env.template "
            "to .op/openrouter.env and replace <OPENROUTER_SECRET_REF> with a 1Password reference."
        )
    if not (source.startswith("op://") or source.startswith("sk-or-")):
        raise RuntimeError("OPENROUTER_API_KEY must be an op:// reference or an sk-or- API key.")
    return source


def build_runtime_env(secret_source: str, existing_values: dict[str, str]) -> str:
    """Build the aliases required by the Codex and Claude OpenRouter launchers."""
    management_key = existing_values.get("OPENROUTER_MANAGEMENT_KEY", "").strip()
    lines = [
        f"OPENROUTER_API_KEY={secret_source}",
        f"OPENAI_API_KEY={secret_source}",
        "OPENAI_BASE_URL=https://openrouter.ai/api/v1",
        "OPENAI_MODEL=openrouter/auto",
        f"ANTHROPIC_AUTH_TOKEN={secret_source}",
        "ANTHROPIC_BASE_URL=https://openrouter.ai/api",
        f"ANTHROPIC_API_KEY={secret_source}",
    ]
    if _is_usable_secret_source(management_key):
        lines.insert(1, f"OPENROUTER_MANAGEMENT_KEY={management_key}")
    return "\n".join(lines) + "\n"


def write_runtime_env(content: str, path: pathlib.Path | None = None) -> None:
    """Atomically write a private runtime environment file without logging its content."""
    path = ENV_FILE if path is None else path
    path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    os.chmod(path.parent, 0o700)
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{path.name}.",
        dir=path.parent,
        text=True,
    )
    try:
        os.fchmod(descriptor, 0o600)
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            handle.write(content)
        os.replace(temporary_name, path)
        os.chmod(path, 0o600)
    except BaseException:
        try:
            os.close(descriptor)
        except OSError:
            pass
        pathlib.Path(temporary_name).unlink(missing_ok=True)
        raise


def materialize_runtime_env() -> pathlib.Path:
    existing_values = read_env_values()
    secret_source = select_secret_source(existing_values)
    write_runtime_env(build_runtime_env(secret_source, existing_values))
    return ENV_FILE


def main() -> int:
    try:
        output_path = materialize_runtime_env()
        print(f"Materialized OpenRouter runtime environment at {output_path}")
        return 0
    except Exception as exc:
        print(f"resolve_openrouter_secret.py: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
