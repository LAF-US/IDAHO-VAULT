"""Bootstrap the local OpenClaw edge from repo-root vault state."""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from dataclasses import dataclass


class SparkseedError(RuntimeError):
    """Raised when the SPARKSEED bootstrap cannot complete honestly."""


@dataclass(frozen=True)
class SecretField:
    """One 1Password field that must be resolved into the process environment."""

    item: str
    field: str
    env_name: str
    fallback_fields: tuple[str, ...] = ()


REQUIRED_SECRET_FIELDS = (
    SecretField(item="OpenClaw Gateway Token", field="token", env_name="GATEWAY_TOKEN"),
    SecretField(item="OpenClaw Discord Bot", field="token", env_name="DISCORD_BOT_TOKEN"),
    SecretField(item="OpenClaw Discord Bot", field="applicationId", env_name="DISCORD_APP_ID"),
    SecretField(item="OpenClaw Signal Account", field="number", env_name="SIGNAL_NUMBER"),
    SecretField(item="Nostr (Orpheus)", field="password", env_name="NOSTR_PRIVATE_KEY"),
    SecretField(item="Nostr (Orpheus)", field="username", env_name="NOSTR_PUBLIC_KEY"),
    SecretField(item="GitHub", field="private key", env_name="GITHUB_SSH_KEY", fallback_fields=("password",)),
    SecretField(item="Linear API Key", field="credential", env_name="LINEAR_API_KEY", fallback_fields=("password",)),
    SecretField(item="Mistral", field="credential", env_name="MISTRAL_API_KEY", fallback_fields=("password",)),
    SecretField(item="Obsidian Sync", field="password", env_name="OBSIDIAN_SYNC_TOKEN"),
    SecretField(item="Claude", field="credential", env_name="ANTHROPIC_API_KEY", fallback_fields=("password",)),
    SecretField(item="Qodo API Key", field="credential", env_name="QODO_API_KEY", fallback_fields=("password",)),
)

OPENCLAW_BOOT_SEQUENCE = (
    ("gateway", "start"),
    ("secrets", "reload"),
    ("secrets", "audit"),
)


def _require_command(name: str) -> None:
    if shutil.which(name) is None:
        raise SparkseedError(f"Required command was not found on PATH: {name}")


def _format_command(command: list[str]) -> str:
    return " ".join(command)


def _run_capture(command: list[str]) -> subprocess.CompletedProcess[str]:
    try:
        return subprocess.run(command, capture_output=True, text=True, check=False)
    except OSError as exc:
        raise SparkseedError(f"Failed to start command '{_format_command(command)}': {exc}") from exc


def _run_stream(command: list[str], *, env: dict[str, str]) -> subprocess.CompletedProcess[str]:
    try:
        return subprocess.run(command, env=env, check=False)
    except OSError as exc:
        raise SparkseedError(f"Failed to start command '{_format_command(command)}': {exc}") from exc


def _check_success(result: subprocess.CompletedProcess[str], command: list[str]) -> None:
    if result.returncode == 0:
        return
    detail = ""
    if isinstance(result.stderr, str) and result.stderr.strip():
        detail = result.stderr.strip()
    elif isinstance(result.stdout, str) and result.stdout.strip():
        detail = result.stdout.strip()
    if detail:
        raise SparkseedError(f"Command failed ({_format_command(command)}): {detail}")
    raise SparkseedError(f"Command failed ({_format_command(command)}) with exit code {result.returncode}.")


def ensure_op_signed_in() -> None:
    """Confirm that the local 1Password CLI session is already available."""

    _require_command("op")
    if os.environ.get("OP_ACCOUNT"):
        command = ["op", "whoami"]
    else:
        command = ["op", "signin"]
        result = subprocess.run(
            command,
            env=os.environ.copy(),
            check=False,
        )
        if result.returncode != 0:
            command = ["op", "whoami"]
    result = _run_capture(command)
    _check_success(result, command)


def _resolve_secret(spec: SecretField) -> str:
    command = ["op", "item", "get", spec.item, "--field", spec.field]
    result = _run_capture(command)
    _check_success(result, command)
    value = result.stdout.strip()
    if not value:
        for fallback in spec.fallback_fields:
            command = ["op", "item", "get", spec.item, "--field", fallback]
            result = _run_capture(command)
            if result.returncode == 0 and result.stdout.strip():
                return result.stdout.strip()
        raise SparkseedError(
            f"1Password field resolved empty for '{spec.item}' field '{spec.field}'."
        )
    return value


def build_secret_env() -> dict[str, str]:
    """Resolve the required OpenClaw secrets into environment variables."""

    ensure_op_signed_in()
    return {spec.env_name: _resolve_secret(spec) for spec in REQUIRED_SECRET_FIELDS}


def _announce(message: str) -> None:
    print(message)


def run_sparkseed() -> None:
    """Run the SPARKSEED bootstrap in the same order as the legacy shell script."""

    _require_command("openclaw")
    _announce("=" * 83)
    _announce("SPARKSEED bootstrap: preparing the local OpenClaw edge from vault state.")
    _announce("=" * 83)
    _announce("")
    _announce("[1/4] Loading the required OpenClaw secrets from 1Password.")
    env = os.environ.copy()
    env.update(build_secret_env())
    _announce("Resolved gateway, Discord, and Signal values for this process.")
    _announce("-" * 83)

    for index, command_tail in enumerate(OPENCLAW_BOOT_SEQUENCE, start=2):
        command = ["openclaw", *command_tail]
        if command_tail == ("gateway", "start"):
            _announce(f"[{index}/4] Starting the gateway surface.")
        elif command_tail == ("secrets", "reload"):
            _announce(f"[{index}/4] Reloading the active secret manifest.")
        else:
            _announce(f"[{index}/4] Auditing the current secret view.")
        result = _run_stream(command, env=env)
        _check_success(result, command)
        if index < 4:
            _announce("-" * 83)

    _announce("=" * 83)
    _announce("SPARKSEED bootstrap complete. From here the machinery has to speak for itself.")
    _announce("=" * 83)


def main(argv: list[str] | None = None) -> int:
    """CLI entrypoint for the Python-native SPARKSEED bootstrap."""

    parser = argparse.ArgumentParser(
        prog="sta***REMOVED***SPARKSEED",
        description="Bootstrap the OpenClaw runtime from local 1Password-backed vault state.",
    )
    parser.parse_args(argv)
    try:
        run_sparkseed()
    except SparkseedError as exc:
        print(f"SPARKSEED failed: {exc}", file=sys.stderr)
        return 1
    return 0
