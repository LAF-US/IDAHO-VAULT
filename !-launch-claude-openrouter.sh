#!/usr/bin/env bash
set -e

ACTUAL_SCRIPT="$(readlink -f "$0" 2>/dev/null || echo "$0")"
SCRIPT_DIR="$(cd "$(dirname "$ACTUAL_SCRIPT")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
RESOLVER="$REPO_ROOT/!/resolve_openrouter_secret.py"

if [ ! -x "$RESOLVER" ]; then
    echo "Error: $RESOLVER not found or not executable"
    echo "Expected: $RESOLVER"
    echo "REPO_ROOT: $REPO_ROOT"
    exit 1
fi

export OPENROUTER_API_KEY="$("$RESOLVER")"

exec claude "$@"
