#!/bin/sh
# Tailscale variant switch — Phase 2 (after the reboot): install the
# open-source tailscaled as a LaunchDaemon and register the node.
# State lives in a root-owned file (no keychain involvement) so node identity
# and serve config finally persist across restarts.
#
# Run as logan (it sudo-prompts where needed):
#   sh 02-install-oss-daemon.sh
#
# Expect: the go build takes ~5-10 min on this machine; `tailscale up` prints
# a login URL at the end — open it in the browser (one-time auth, the LAST
# identity churn).
set -eux
export PATH=/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin

# Build the current release with the Go toolchain already on this Mac (1.26.2)
go install tailscale.com/cmd/tailscale@latest tailscale.com/cmd/tailscaled@latest

# Install as a system LaunchDaemon (copies tailscaled to /usr/local/bin,
# writes /Library/LaunchDaemons plist, starts the daemon)
sudo "$HOME/go/bin/tailscaled" install-system-daemon

# Matching CLI alongside the daemon (single source, no version drift)
sudo cp "$HOME/go/bin/tailscale" /usr/local/bin/tailscale

# Register — prints the auth URL
sudo /usr/local/bin/tailscale up

echo ""
echo "DONE. Tell Claude to run the verification pass (state-file perms, serve"
echo "persistence acceptance test, OpenClaw posture, then Pixel pairing)."
