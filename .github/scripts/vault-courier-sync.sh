#!/bin/bash
# Project Courier: Vault Ledger Sync
# Part of LAF-18 Phase 2 (Promotion to Production)
# Synchronizes '!/' local directory to 'gs://the-ledger-bucket/ledger/'

set -e

# Configuration
SOURCE_DIR="!"
DEST_BUCKET="gs://the-ledger-bucket/ledger"
INITIATING_AGENT="agent:gemini"
CORRELATION_ID="LAF-18-$(date +%Y%m%d%H%M%S)"
RELATED_REF="!/__!__/!/! The world is quiet here/DOCKET.md"

echo "--- Project Courier: Syncing Ledger ---"

# Perform Rsync
# -r: recursive
# -d: delete files in destination that are not in source
# -n: dry-run (safety first - REMOVE for production after first pass)
DRY_RUN_FLAG=""
if [[ "$1" == "--dry-run" ]]; then
    DRY_RUN_FLAG="-n"
    echo "Mode: DRY RUN"
fi

OUTCOME="success"
RETRY_COUNT=0

if ! gcloud storage rsync $DRY_RUN_FLAG -r -d "$SOURCE_DIR" "$DEST_BUCKET"; then
    OUTCOME="failure"
fi

# Emit MCP Action Log (Mandatory per VAULT-CONVENTIONS.md)
cat <<EOF
mcp_action_log:
  action_type: "invoke_tool"
  system_or_resource_id: "$DEST_BUCKET"
  initiating_agent: "$INITIATING_AGENT"
  correlation_id: "$CORRELATION_ID"
  outcome: "$OUTCOME"
  retry_count: $RETRY_COUNT
  related_ref: "$RELATED_REF"
EOF

if [[ "$OUTCOME" == "failure" ]]; then
    exit 1
fi
