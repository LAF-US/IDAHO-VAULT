#!/usr/bin/env bash
# Compatibility wrapper for older root-level bootstrap calls.

set -euo pipefail

VAULT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CANONICAL_BOOTSTRAP="$VAULT_ROOT/!/agent.sh"

if [ ! -f "$CANONICAL_BOOTSTRAP" ]; then
  echo "[error] Canonical bootstrap entrypoint missing: !/agent.sh" >&2
  if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    exit 1
  else
    return 1
  fi
fi

# Intentionally source the canonical script so exports and git identity settings
# land in the current shell, just like the historical root entrypoint did.
source "$CANONICAL_BOOTSTRAP" "$@"
