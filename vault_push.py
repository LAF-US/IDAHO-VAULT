#!/usr/bin/env python3
"""
vault_push.py — Push a local file to IDAHO-VAULT on GitHub.

Usage:
    python vault_push.py <local_file> <repo_path> [--message "commit message"]

Examples:
    python vault_push.py sort_audit.py .github/scripts/sort_audit.py
    python vault_push.py sort_audit.py .github/scripts/sort_audit.py --message "fix orphan detection"

Config:
    Set your token in environment variable VAULT_TOKEN, or in a .env file
    in the same directory as this script:
        VAULT_TOKEN=github_pat_...
        VAULT_REPO=loganfinney27/IDAHO-VAULT
"""

import argparse
import base64
import json
import os
import sys
from pathlib import Path
from urllib import request, error

# ── Config ────────────────────────────────────────────────────────────────────

def load_env():
    """Load .env file from script directory if present."""
    env_path = Path(__file__).parent / ".env"
    if env_path.exists():
        for line in env_path.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, _, val = line.partition("=")
                os.environ.setdefault(key.strip(), val.strip())

load_env()

VAULT_TOKEN = os.environ.get("VAULT_TOKEN", "")
VAULT_REPO  = os.environ.get("VAULT_REPO", "loganfinney27/IDAHO-VAULT")
API_BASE    = "https://api.github.com"

# ── GitHub API helpers ────────────────────────────────────────────────────────

def gh_request(method: str, path: str, body: dict = None) -> dict:
    url = f"{API_BASE}{path}"
    headers = {
        "Authorization": f"Bearer {VAULT_TOKEN}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "Content-Type": "application/json",
    }
    data = json.dumps(body).encode() if body else None
    req = request.Request(url, data=data, headers=headers, method=method)
    try:
        with request.urlopen(req) as resp:
            return json.loads(resp.read())
    except error.HTTPError as e:
        body = e.read().decode()
        print(f"HTTP {e.code} {e.reason}: {body}", file=sys.stderr)
        sys.exit(1)


def get_file_sha(repo_path: str) -> str | None:
    """Return the blob SHA of an existing file, or None if it doesn't exist."""
    try:
        result = gh_request("GET", f"/repos/{VAULT_REPO}/contents/{repo_path}")
        return result.get("sha")
    except SystemExit:
        return None


def push_file(local_path: str, repo_path: str, message: str):
    content = Path(local_path).read_bytes()
    encoded = base64.b64encode(content).decode()

    sha = get_file_sha(repo_path)

    body = {
        "message": message,
        "content": encoded,
    }
    if sha:
        body["sha"] = sha
        action = "Updated"
    else:
        action = "Created"

    gh_request("PUT", f"/repos/{VAULT_REPO}/contents/{repo_path}", body)
    print(f"{action} {repo_path} in {VAULT_REPO}")

# ── CLI ───────────────────────────────────────────────────────────────────────

def main():
    if not VAULT_TOKEN:
        print("Error: VAULT_TOKEN not set. Add it to .env or set the environment variable.",
              file=sys.stderr)
        sys.exit(1)

    parser = argparse.ArgumentParser(description="Push a file to IDAHO-VAULT on GitHub.")
    parser.add_argument("local_file", help="Path to the local file to push")
    parser.add_argument("repo_path", help="Destination path in the repo (e.g. .github/scripts/sort_audit.py)")
    parser.add_argument("--message", "-m", default=None,
                        help="Commit message (default: 'update <repo_path>')")
    args = parser.parse_args()

    if not Path(args.local_file).exists():
        print(f"Error: local file '{args.local_file}' not found.", file=sys.stderr)
        sys.exit(1)

    message = args.message or f"update {args.repo_path}"
    push_file(args.local_file, args.repo_path, message)


if __name__ == "__main__":
    main()
