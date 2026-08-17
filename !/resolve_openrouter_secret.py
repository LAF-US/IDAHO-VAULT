#!/usr/bin/env python3
"""Materialize the OpenRouter runtime environment without printing credentials."""

from __future__ import annotations

import os
import pathlib
import re
import stat
import sys
import tempfile


REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
ENV_FILE = REPO_ROOT / ".op" / "openrouter.env"
KEY_RE = re.compile(r"^(?:export\s+)?([A-Z][A-Z0-9_]*)=(.*)$")
OP_REFERENCE_RE = re.compile(r"^op://[^/\r\n]+/[^/\r\n]+/[^/\r\n]+$")
SECRET_PLACEHOLDERS = frozenset(
    {
        "<OPENROUTER_SECRET_REF>",
        "CHANGE_TO_MANAGEMENT_KEY_OP_REF",
    }
)
PRIVATE_DIRECTORY_MODE = stat.S_IRWXU
PRIVATE_FILE_MODE = stat.S_IRUSR | stat.S_IWUSR


def unquote(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        return value[1:-1]
    return value


def validated_op_reference(value: str | None, variable_name: str) -> str:
    """Return a syntactically valid 1Password reference without exposing its value."""
    if value is None or not value.strip() or value.strip() in SECRET_PLACEHOLDERS:
        raise RuntimeError(f"{variable_name} is not configured with a 1Password op:// reference.")

    reference = unquote(value)
    if not OP_REFERENCE_RE.fullmatch(reference):
        raise RuntimeError(f"{variable_name} must be a valid 1Password op:// reference.")
    return reference


def read_env_reference(variable_name: str, path: pathlib.Path | None = None) -> str | None:
    """Read and validate one reference from the private environment file."""
    path = ENV_FILE if path is None else path
    if not path.exists():
        return None

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        match = KEY_RE.match(line)
        if match and match.group(1) == variable_name:
            return validated_op_reference(match.group(2), variable_name)
    return None


def openrouter_reference() -> str:
    """Select a validated reference from the environment or private runtime file."""
    environment_reference = os.environ.get("OPENROUTER_API_KEY")
    if environment_reference:
        return validated_op_reference(environment_reference, "OPENROUTER_API_KEY")

    file_reference = read_env_reference("OPENROUTER_API_KEY")
    if file_reference:
        return file_reference

    raise RuntimeError(
        "OPENROUTER_API_KEY is not configured. Copy .op/openrouter.env.template "
        "to .op/openrouter.env and replace <OPENROUTER_SECRET_REF> with a 1Password reference."
    )


def build_runtime_env(openrouter_ref: str) -> str:
    """Build the least-privilege aliases required by Codex and Claude launchers."""
    lines = [
        f"OPENROUTER_API_KEY={openrouter_ref}",
        f"OPENAI_API_KEY={openrouter_ref}",
        "OPENAI_BASE_URL=https://openrouter.ai/api/v1",
        "OPENAI_MODEL=openrouter/auto",
        f"ANTHROPIC_AUTH_TOKEN={openrouter_ref}",
        "ANTHROPIC_BASE_URL=https://openrouter.ai/api",
        f"ANTHROPIC_API_KEY={openrouter_ref}",
    ]
    return "\n".join(lines) + "\n"


def write_runtime_env(content: str, path: pathlib.Path | None = None) -> None:
    """Atomically write a private runtime environment file without logging its content."""
    path = ENV_FILE if path is None else path
    path.parent.mkdir(mode=PRIVATE_DIRECTORY_MODE, parents=True, exist_ok=True)
    os.chmod(path.parent, PRIVATE_DIRECTORY_MODE)
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{path.name}.",
        dir=path.parent,
        text=True,
    )
    try:
        os.fchmod(descriptor, PRIVATE_FILE_MODE)
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            handle.write(content)
        os.replace(temporary_name, path)
        os.chmod(path, PRIVATE_FILE_MODE)
    except BaseException:
        try:
            os.close(descriptor)
        except OSError:
            pass
        pathlib.Path(temporary_name).unlink(missing_ok=True)
        raise


def materialize_runtime_env() -> pathlib.Path:
    openrouter_ref = openrouter_reference()
    write_runtime_env(build_runtime_env(openrouter_ref))
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
