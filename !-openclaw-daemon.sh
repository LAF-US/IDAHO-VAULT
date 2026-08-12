#!/usr/bin/env bash
#
# openclaw-daemon.sh
# Start/restart the local OpenClaw gateway LaunchAgent.
#

set -e

echo "=== OpenClaw Gateway ==="

openclaw gateway status 2>/dev/null || echo "Gateway service not running"

echo "Starting/restarting gateway..."
openclaw gateway restart

sleep 3

if openclaw gateway status 2>/dev/null | grep -q "Connectivity probe: ok"; then
    echo "Gateway: LIVE"
else
    echo "Gateway: CHECK FAILED"
fi

echo "Dashboard: http://127.0.0.1:18789/"

exit 0
