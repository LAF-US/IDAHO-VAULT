#!/bin/bash
# vault-charter-scanner.sh — Read CHARTER from daily notes

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VAULT_ROOT="$(dirname "${SCRIPT_DIR}")"

TODAY=$(date +%Y-%m-%d)
NOTE_FILE="${VAULT_ROOT}/${TODAY}.md"

echo "=== CHARTER SCAN ==="
echo "Date: ${TODAY}"
echo "Note: ${NOTE_FILE}"
echo ""

if [[ -f "${NOTE_FILE}" ]]; then
    echo "Incomplete tasks from Daily Queue:"
    grep -E '^\- \[ \]' "${NOTE_FILE}" 2>/dev/null | sed 's/^- \[ \] //' || echo "  (none)"
else
    echo "Daily note not found"
fi