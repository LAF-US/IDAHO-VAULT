#!/bin/bash
# vault-dispatch.sh — UNIFIED SWARM DISPATCHER
# One command → coordinated execution across the vault

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VAULT_ROOT="$(dirname "${SCRIPT_DIR}")"

# === UNIFIED COMMANDS ===
case "${1:-help}" in
    status)
        echo "=== VAULT DISPATCH STATUS ==="
        echo ""
        echo "Components:"
        echo "  SPARKSEED:    $(command -v openclaw >/dev/null && echo '✅' || echo '❌')"
        echo "  Gateway:    $(pgrep -f openclaw-gateway >/dev/null && echo '✅' || echo '❌')"
        echo "  Bridge:    $([[ -x "${SCRIPT_DIR}/vault-openclaw-bridge.sh" ]] && echo '✅' || echo '❌')"
        echo "  Hook:      $([[ -x "${SCRIPT_DIR}/vault-pre-exec-hook.sh" ]] && echo '✅' || echo '❌')"
        echo ""
        echo "SBP Field:"
        cat "${VAULT_ROOT}/!/sbp-blackboard.json" 2>/dev/null || echo "  (empty)"
        ;;
        
    sniff)
        "${SCRIPT_DIR}/vault-pre-exec-hook.sh" sniff
        ;;
        
    emit)
        shift
        "${SCRIPT_DIR}/vault-openclaw-bridge.sh" emit "${1:-}" "${2:-}"
        ;;
        
    dispatch)
        shift
        TASK="${1:-}"
        if [[ -z "${TASK}" ]]; then
            echo "Usage: dispatch <task>"
            exit 1
        fi
        echo "Dispatching: ${TASK}"
        # Pre-exec: sniff vault context
        "${SCRIPT_DIR}/vault-pre-exec-hook.sh" run
        # Execute task (placeholder - OpenClaw would run here)
        echo "Executed: ${TASK}"
        # Post-exec: emit result
        "${SCRIPT_DIR}/vault-openclaw-bridge.sh" emit "DISPATCH_COMPLETE" "${TASK}"
        ;;
        
    help|*)
        echo "Vault Unified Dispatcher"
        echo ""
        echo "Commands:"
        echo "  status         — Show all component status"
        echo "  sniff          — Read vault stigmergy field"
        echo "  emit <sig> <p> — Emit signal to field"
        echo "  dispatch <t>   — Execute task with pre-exec sniff"
        echo ""
        echo "Examples:"
        echo "  ./vault-dispatch.sh status"
        echo "  ./vault-dispatch.sh sniff"
        echo "  ./vault-dispatch.sh dispatch my-task"
        ;;
esac