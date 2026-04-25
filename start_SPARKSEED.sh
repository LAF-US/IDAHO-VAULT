#!/usr/bin/env bash
#
# openclaw_startup_seed.sh (The Genesis Script)
#
# This script must be the FIRST command executed when working in the IDAHO-VAULT.
# It synchronizes the environment, starts all required services, and validates the
# operational status of the core OpenClaw agent components.
#
# INSTRUCTION: Never manually run 'openclaw' without running this script first.

set -e

REPO_ROOT="$(cd "$(dirname "$0")" && pwd)"
ENV_FILE="$REPO_ROOT/.op/openrouter.env"

echo "==================================================================================="
echo "Starting OpenClaw Vault Seed Execution"
echo "==================================================================================="

# 1. LOAD ENVIRONMENT (from .op/openrouter.env if op CLI unavailable)
echo ">>> [Step 1/4] Loading Environment Variables:"

if command -v op &> /dev/null; then
    echo "   1Password CLI available - loading secrets from vault..."
    export GATEWAY_TOKEN=$(op item get "OpenClaw Gateway Token" --field token 2>/dev/null || echo "")
    export DISCORD_BOT_TOKEN=$(op item get "OpenClaw Discord Bot" --field token 2>/dev/null || echo "")
    export DISCORD_APP_ID=$(op item get "OpenClaw Discord Bot" --field applicationId 2>/dev/null || echo "")
    export SIGNAL_NUMBER=$(op item get "OpenClaw Signal Account" --field number 2>/dev/null || echo "")
elif [ -f "$ENV_FILE" ]; then
    echo "   1Password CLI unavailable - loading from .op/openrouter.env..."
    set -a
    source "$ENV_FILE"
    set +a
else
    echo "   WARNING: 1Password CLI unavailable and .op/openrouter.env not found."
    echo "   Some secrets will not be available."
fi

echo "   Environment variables loaded."
echo "-----------------------------------------------------------------------------------"

# 2. VALIDATE OPENCLAW
echo ">>> [Step 2/4] Validating OpenClaw Installation:"

if ! command -v openclaw &> /dev/null; then
    echo "ERROR: 'openclaw' command not found. Install OpenClaw or add to PATH."
    exit 1
fi
echo "   OpenClaw found: $(openclaw --version 2>/dev/null || echo 'version unknown')"

# 3. START GATEWAY
echo ">>> [Step 3/4] Starting Gateway Service:"

if openclaw gateway start 2>/dev/null; then
    echo "   Gateway started successfully."
else
    GATEWAY_EXIT=$?
    echo "   WARNING: Gateway start returned exit code $GATEWAY_EXIT"
    echo "   This may be expected if gateway is already running or not configured."
fi

echo "-----------------------------------------------------------------------------------"

# 4. FINAL STATUS
echo ">>> [Step 4/4] Final Status:"

echo "==================================================================================="
echo "Seed execution complete."
echo "Run 'openclaw gateway' to start the gateway manually if needed."
echo "==================================================================================="

exit 0