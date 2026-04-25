from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path


def ensure_op_available() -> None:
    if shutil.which("op") is None:
        raise SystemExit(
            "1Password CLI 'op' is not installed or not on PATH.\n"
            "If the env file already exists, you can continue. "
            "Otherwise, install 1Password CLI or provide the key manually."
        )


def ensure_op_signed_in() -> None:
    result = subprocess.run(
        ["op", "whoami"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    if result.returncode != 0:
        raise SystemExit(
            "1Password CLI is not signed in. Run 'op signin' or unlock desktop integration.\n"
            "If the env file already exists, you can continue. "
            "Otherwise, sign in to 1Password or provide the key manually."
        )


def can_read_secret(secret_ref: str) -> bool:
    result = subprocess.run(
        ["op", "read", secret_ref],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    return result.returncode == 0


def find_op_reference(vault: str) -> str:
    """Return a 1Password item reference path (op://...) for the OpenRouter API key.

    This function returns a reference path, not the actual secret value.
    The returned string is safe to store in a local .env file because it
    is resolved to the real credential only when a 1Password-aware tool
    reads the file (e.g. ``op run --env-file=...``).
    """
    candidates = [
        "op://Vault/OpenRouter API Key/credential",
        "op://Vault/OpenRouter API Key/password",
        f"op://{vault}/OpenRouter API Key/credential",
        f"op://{vault}/openrouter-api-key/credential",
        f"op://{vault}/openrouter-api-key/password",
        f"op://{vault}/openrouter/credential",
        f"op://{vault}/openrouter/password",
    ]

    for candidate in candidates:
        if can_read_secret(candidate):
            return candidate

    raise SystemExit(f"Could not resolve any known OpenRouter item reference in vault '{vault}'.")


def render_op_env_file(op_ref: str) -> str:
    """Render a .env file containing 1Password item references (op://...) for OpenRouter.

    The values are reference paths, not actual credentials.  Tools like
    ``op run --env-file=...`` resolve them at execution time.
    """
    lines = [
        f"OPENROUTER_API_KEY={op_ref}",
        f"OPENAI_API_KEY={op_ref}",
        "OPENAI_BASE_URL=https://openrouter.ai/api/v1",
        "OPENAI_MODEL=openrouter/auto",
        f"ANTHROPIC_AUTH_TOKEN={op_ref}",
        "ANTHROPIC_BASE_URL=https://openrouter.ai/api",
        "ANTHROPIC_API_KEY=",
    ]
    return "\r\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a local OpenRouter env file from 1Password refs.")
    parser.add_argument("--vault", default="Vault", help="1Password vault name to search")
    parser.add_argument("--out-file", default="", help="Destination env file path")
    parser.add_argument("--force", action="store_true", help="Force regeneration even if file exists")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parent.parent
    out_file = Path(args.out_file) if args.out_file else repo_root / ".op" / "openrouter.env"

    if out_file.exists() and not args.force:
        with open(out_file) as f:
            content = f.read()
        if "OPENROUTER_API_KEY=sk-" in content:
            print(f"Env file already exists at {out_file}. Use --force to regenerate.")
            return 0

    ensure_op_available()
    ensure_op_signed_in()
    op_ref = find_op_reference(args.vault)

    out_file.parent.mkdir(parents=True, exist_ok=True)
    out_file.write_text(render_op_env_file(op_ref), encoding="utf-8", newline="")
    print(f"Wrote {out_file} using item reference: {op_ref}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
