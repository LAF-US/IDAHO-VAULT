#!/bin/bash
# vault-pre-exec-hook.sh — OpenClaw pre-execution hook
# Runs BEFORE OpenClaw agent executes
# Sniffs the stigmergy field for context

set -euo pipefail

# === CONFIG ===
VAULT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
SBP_BLACKBOARD="${VAULT_ROOT}/!/sbp-blackboard.json"
OPENCLAW_WORKSPACE="${HOME}/.openclaw/workspace"

# === SNIFF THE FIELD ===
sniff_field() {
    if [[ -f "${SBP_BLACKBOARD}" ]]; then
        cat "${SBP_BLACKBOARD}"
    else
        echo '{"signals":[]}'
    fi
}

# === INJECT CONTEXT INTO OPENCLAW ===
inject_context() {
    local context
    context=$(sniff_field)
    
    # Write to OpenClaw workspace for agent to read
    local context_file="${OPENCLAW_WORKSPACE}/.vault-context.json"
    echo "${context}" > "${context_file}"
    
    echo "Context injected: ${context_file}"
}

# === MAIN ===
case "${1:-run}" in
    run)
        inject_context
        ;;
    sniff)
        sniff_field
        ;;
    *)
        echo "Usage: {run|sniff}"
        exit 1
        ;;
esac