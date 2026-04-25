#!/bin/bash
set -e

ACTUAL_SCRIPT="$(readlink -f "$0" 2>/dev/null || echo "$0")"
SCRIPT_DIR="$(cd "$(dirname "$ACTUAL_SCRIPT")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
ENV_FILE="$REPO_ROOT/.op/openrouter.env"

if [ ! -f "$ENV_FILE" ]; then
    echo "Error: $ENV_FILE not found"
    echo "Expected: $ENV_FILE"
    echo "REPO_ROOT: $REPO_ROOT"
    exit 1
fi

set -a
source "$ENV_FILE"
set +a

exec claude "$@"