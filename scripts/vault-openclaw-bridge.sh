#!/bin/bash
# vault-openclaw-bridge.sh — OpenClaw ↔ IDAHO-VAULT Bridge
# CONSTITUTIONAL: Explicit, Scoped, Reversible
# Authority: LOGAN (Human Sovereign)

set -euo pipefail

# === VAULT CONFIGURATION ===
VAULT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
SBP_BLACKBOARD="${VAULT_ROOT}/!/sbp-blackboard.json"
OPENCLAW_STATE="${HOME}/.openclaw"
OPENCLAW_WORKSPACE="${OPENCLAW_STATE}/workspace"

# === SCOPED ACCESS: What OpenClaw can read/write ===
READ_SCOPES=(
    "${VAULT_ROOT}/!/README.md"
    "${VAULT_ROOT}/!/AGENTS.md" 
    "${VAULT_ROOT}/swarm.json"
    "${VAULT_ROOT}/!/sbp-blackboard.json"
)

WRITE_SCOPES=(
    "${VAULT_ROOT}/!/sbp-blackboard.json"
)

# === FUNCTIONS ===

sniff() {
    # Read latest signals from SBP blackboard
    if [[ -f "${SBP_BLACKBOARD}" ]]; then
        cat "${SBP_BLACKBOARD}"
    else
        echo '{"signals":[]}'
    fi
}

emit() {
    # Write signal to SBP blackboard (scoped)
    local signal="${1}"
    local payload="${2}"
    local timestamp
    timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
    
    # Ensure directory exists
    mkdir -p "$(dirname "${SBP_BLACKBOARD}")"
    
    # Simple JSON write
    echo "{\"signals\":[{\"signal\":\"${signal}\",\"payload\":\"${payload}\",\"timestamp\":\"${timestamp}\"}]}" > "${SBP_BLACKBOARD}"
}

bridge-status() {
    echo "=== VAULT-OPENCLAW BRIDGE ==="
    echo "Vault Root: ${VAULT_ROOT}"
    echo "SBP Blackboard: ${SBP_BLACKBOARD}"
    echo "OpenClaw Workspace: ${OPENCLAW_WORKSPACE}"
    echo ""
    echo "=== CONFORMANCE ==="
    echo "CONSTITUTION Section II: Levels & Layers"
    echo "  - Explicit: Scope lists defined above"
    echo "  - Scoped: Limited file access"  
    echo "  - Reversible: Script can be removed"
    echo "  - Authority: LOGAN (Human Sovereign)"
}

case "${1:-status}" in
    sniff)
        sniff
        ;;
    emit)
        [[ -z "${2:-}" ]] && { echo "Usage: $0 emit <signal> <payload>"; exit 1; }
        emit "${2}" "${3:-}"
        ;;
    status)
        bridge-status
        ;;
    *)
        echo "Commands: sniff | emit <signal> <payload> | status"
        exit 1
        ;;
esac