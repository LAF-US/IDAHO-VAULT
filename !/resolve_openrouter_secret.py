from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path


def ensure_op_available() -> None:
    if shutil.which("op") is None:
        raise SystemExit("1Password CLI 'op' is not installed or not on PATH.")


def ensure_op_signed_in() -> None:
    result = subprocess.run(
        ["op", "whoami"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    if result.returncode != 0:
        raise SystemExit(
            "1Password CLI is not signed in. Run 'op signin' or unlock desktop integration first."
        )


def can_read_secret(secret_ref: str) -> bool:
    result = subprocess.run(
        ["op", "read", secret_ref],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    return result.returncode == 0


def resolve_secret_reference(vault: str) -> str:
    candidates = [
        "op://Personal/API Credentials/credential",
        "op://Personal/OpenRouter/password",
        f"op://{vault}/openrouter-api-key/credential",
        f"op://{vault}/openrouter-api-key/password",
        f"op://{vault}/openrouter/credential",
        f"op://{vault}/openrouter/password",
        f"op://{vault}/openrouter-api/credential",
        f"op://{vault}/openrouter-api/password",
        f"op://{vault}/open-router-api-key/credential",
        f"op://{vault}/open-router-api-key/password",
    ]

    for candidate in candidates:
        if can_read_secret(candidate):
            return candidate

    raise SystemExit(f"Could not resolve any known OpenRouter secret reference in vault '{vault}'.")


def render_env(secret_ref: str) -> str:
    lines = [
        f"OPENROUTER_API_KEY={secret_ref}",
        f"OPENAI_API_KEY={secret_ref}",
        "OPENAI_BASE_URL=https://openrouter.ai/api/v1",
        "OPENAI_MODEL=openrouter/auto",
        f"ANTHROPIC_AUTH_TOKEN={secret_ref}",
        "ANTHROPIC_BASE_URL=https://openrouter.ai/api",
        "ANTHROPIC_API_KEY=",
    ]
    return "\r\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a local OpenRouter env file from 1Password refs.")
    parser.add_argument("--vault", default="vault-operations", help="1Password vault name to search")
    parser.add_argument("--out-file", default="", help="Destination env file path")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parent.parent
    out_file = Path(args.out_file) if args.out_file else repo_root / ".op" / "openrouter.env"
    out_file.parent.mkdir(parents=True, exist_ok=True)

    ensure_op_available()
    ensure_op_signed_in()
    secret_ref = resolve_secret_reference(args.vault)

    out_file.write_text(render_env(secret_ref), encoding="utf-8", newline="")
    print(f"Wrote {out_file} using {secret_ref}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
