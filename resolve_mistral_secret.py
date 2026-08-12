#!/usr/bin/env python3
"""Resolve MISTRAL_API_KEY without storing it in OpenClaw config.

Clone of resolve_openrouter_secret.py (same contract) pointed at
.op/mistral.env — the Direct-Mistral escape bucket for the BEEFSTACK chain.
"""

from __future__ import annotations

import os
import pathlib
import re
import subprocess
import sys


REPO_ROOT = pathlib.Path(__file__).resolve().parents[0]
ENV_FILE = REPO_ROOT / ".op" / "mistral.env"
OP_BIN = pathlib.Path("/usr/local/bin/op")
KEY_RE = re.compile(r"^(?:export\s+)?MISTRAL_API_KEY=(.*)$")


def unquote(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        return value[1:-1]
    return value


def read_env_file() -> str:
    if not ENV_FILE.exists():
        raise RuntimeError(f"{ENV_FILE} not found")

    for raw_line in ENV_FILE.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        match = KEY_RE.match(line)
        if match:
            return unquote(match.group(1))

    raise RuntimeError(f"MISTRAL_API_KEY not found in {ENV_FILE}")


def resolve_op_ref(ref: str) -> str:
    try:
        completed = subprocess.run(
            [str(OP_BIN), "read", ref],
            check=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=10,
            env={k: v for k, v in os.environ.items() if k in {"OP_SERVICE_ACCOUNT_TOKEN"}},
        )
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as exc:
        message = getattr(exc, "stderr", "") or str(exc)
        raise RuntimeError(f"1Password resolution failed: {message.strip()}") from exc

    value = completed.stdout.strip()
    if not value:
        raise RuntimeError("1Password returned an empty Mistral key")
    return value


def main() -> int:
    try:
        value = os.environ.get("MISTRAL_API_KEY") or read_env_file()
        if value.startswith("op://"):
            value = resolve_op_ref(value)
        if len(value) < 20 or any(ch.isspace() for ch in value):
            raise RuntimeError("resolved Mistral key has unexpected format")
        sys.stdout.write(value)
        return 0
    except Exception as exc:
        print(f"resolve_mistral_secret.py: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
