#!/bin/sh
# Tailscale variant switch — Phase 1: remove the Standalone (macsys) GUI variant.
# Why: its sandboxed system extension cannot persist to the System keychain on
# macOS 12.7.6 (node key + serve config lost every restart -> node churn).
#
# Run:   sudo sh 01-teardown-gui-variant.sh
# Then:  REBOOT. While it reboots, delete BOTH stale nodes in the admin console
#        (logans-macbook-pro AND logans-macbook-pro-1) so the fresh registration
#        can reclaim the bare name.
set -eux

# Stop the VPN and quit the menu-bar app (tolerate either already being gone)
/usr/local/bin/tailscale down || true
osascript -e 'quit app "Tailscale"' || true
sleep 2

# Ask the OS to drop the system extension now; if it refuses (SIP policy),
# deleting the app below queues deactivation for the reboot — same end state,
# and the reboot is already in this flow. (This ordering is what prevents a
# repeat of the orphan-extension mess from the App Store variant.)
systemextensionsctl uninstall W5364U7YZB io.tailscale.ipn.macsys.network-extension || true

# Remove the app and the CLI symlink the Standalone pkg shipped
rm -rf /Applications/Tailscale.app
rm -f /usr/local/bin/tailscale

echo ""
echo "DONE. Next: 1) Reboot.  2) During reboot: admin console -> Machines ->"
echo "delete logans-macbook-pro AND logans-macbook-pro-1.  3) After login,"
echo "run: sh ~/IDAHO-VAULT/scripts/tailscale-switch/02-install-oss-daemon.sh"
