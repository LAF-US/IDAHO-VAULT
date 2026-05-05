#!/usr/bin/env bash
#
# openclaw-daemon.sh
# Start/restart OpenClaw gateway as LaunchDaemon
#

set -e

GATEWAY_TOKEN="***REMOVED***"

echo "=== OpenClaw Gateway ==="

openclaw daemon status 2>/dev/null || echo "Daemon not running"

echo "Starting gateway..."
openclaw daemon start 2>/dev/null

sleep 3

if openclaw health 2>/dev/null | grep -q "ok"; then
    echo "Gateway: LIVE"
else
    echo "Gateway: CHECK FAILED"
fi

echo "Dashboard: http://127.0.0.1:18789/"

exit 0