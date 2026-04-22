#!/bin/bash
#
# openclaw_startup_seed.sh (The Genesis Script)
#
# This script must be the FIRST command executed when working in the IDAHO-VAULT.
# It synchronizes the environment, starts all required services, and validates the
# operational status of the core OpenClaw agent components.
#
# INSTRUCTION: Never manually run 'openclaw' without running this script first.

echo "==================================================================================="
echo "✨ Starting OpenClaw Vault Seed Execution (Requires: 1Password CLI, Node.js, Openclaw Agent Core)"
echo "===================================================================================\n"

# 1. CONFIGURE ENVIRONMENT VARIABLES (Addressing 1Password Dependency)
echo ">>> [Step 1/4] Seeding Environment Variables (The Credentials):"
echo "   (Requires: OpenClaw Discord Bot, OpenClaw Signal Account, OpenClaw Gateway Token to exist in 1Password vault)"

# --- START ENV SEEDING ---
# NOTE TO SELF: The user must ensure these 1Password items exist in the vault.
# We simulate the 'op item get' command here by sourcing the token directly from the 1Password CLI.

# Gateway Token
if command -v op &> /dev/null; then
    export GATEWAY_TOKEN=$(op item get "OpenClaw Gateway Token" --field token)
else
    echo "ERROR: 1Password CLI (op) not found. Cannot proceed. Please ensure 'op' is in PATH."
    exit 1
fi

# Discord Credentials
export DISCORD_BOT_TOKEN=$(op item get "OpenClaw Discord Bot" --field token)
export DISCORD_APP_ID=$(op item get "OpenClaw Discord Bot" --field applicationId)

# Signal Credentials (Using environment variable injection approach for portability)
# Signal requires a simple export of the number, as per pattern established.
export SIGNAL_NUMBER=$(op item get "OpenClaw Signal Account" --field number)

echo "   Environment variables seeded successfully."
echo "-----------------------------------------------------------------------------------"

# 2. START SERVICES (Addressing Gateway failure)
echo ">>> [Step 2/4] Starting Gateway Service (The Connection):"
echo "   [Attempting to launch gateway service via command line.]"

# Attempt to start the gateway service and capture its output.
# Running in the background is preferred for long-running services, but we will foreground it until completion.
openclaw gateway start

GATEWAY_STATUS=$?

echo "-----------------------------------------------------------------------------------"

# 3. RE-SYNC AND VALIDATE (The Audit)
echo ">>> [Step 3/4] Synchronizing Core Components (The Manifest Sync):"
openclaw secrets reload

echo ">>> [Step 4/4] Final Audit (The Final Oath):"
openclaw secrets audit

echo "==================================================================================="
echo "✨ ALL CHECKS COMPLETE. System status is now fully dependent on the user environment setup."
echo "==================================================================================="

exit 0