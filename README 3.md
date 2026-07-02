# Tailscale variant switch — runbook

Updated 2026-07-01 evening. Supersedes the chat-message version.

**Why:** the Standalone (macsys) GUI variant cannot persist anything to the System
keychain on macOS 12.7.6 — node identity re-mints on every restart (the `-1`
hostname churn, twice observed) and Tailscale Serve silently drops its config
while every surface reports success. The open-source `tailscaled` daemon stores
state in a root-owned file; both bugs die by construction.

**Why it gates Task IV (Pixel pairing):** the OpenClaw Android docs require
`wss://` for remote pairing — cleartext `ws://` is only accepted on private-LAN
/ `.local` addresses. So the endgame here (persistent Serve → TLS on 443) is
*required*, not cosmetic. Bonus: restoring `gateway.bind: "loopback"` also gives
local clients their socket back (CLI without env overrides, and the
`obsidianclaw` plugin pairing in the pinned Obsidian work).

## Context changes since first drafting

- OpenClaw's runtime moved to `/Users/logan/node_modules` (home-dir manifest,
  system node at `/usr/local/bin/node`) — deliberate idempotency-test shunt,
  completed and verified. Step-5 commands below use that path.
- FileVault is OFF (verified) — step 1 is the belt for the whole disk's
  credential surface, not just Tailscale.

## The six touchpoints (Logan)

1. **FileVault on** — System Preferences → Security & Privacy → FileVault →
   Turn On. Local recovery key → 1Password. No waiting needed afterward.
   (Never via agent shell — the recovery key must not enter a transcript.)
2. **Teardown** — `sudo sh ~/IDAHO-VAULT/scripts/tailscale-switch/01-teardown-gui-variant.sh`
3. **Reboot.** While rebooting, in https://login.tailscale.com/admin/machines
   delete BOTH stale machines: `logans-macbook-pro` AND `logans-macbook-pro-1`
   (frees the bare name for the fresh registration).
4. **Install** — `sh ~/IDAHO-VAULT/scripts/tailscale-switch/02-install-oss-daemon.sh`
   (~5–10 min go build; `tailscale up` prints the login URL — one browser auth,
   the last identity churn).
5. **Ping Claude** for the verification pass (below).
6. **Task IV** — pair the Pixel against the finally-stable identity.

Expected mid-process: the OpenClaw gateway crash-loops between steps 2 and 5
(it currently binds the tailnet interface, which won't exist until `up`).
Self-heals at step 5.

## Step 5 — agent verification pass (Claude)

- `tailscale status --self` → bare `logans-macbook-pro` name confirmed
- State file exists, root-owned, mode 0600/0700 dir (belt check)
- **Acceptance test:** `tailscale serve --bg 18789` → `serve status` shows it →
  restart daemon (`sudo launchctl kickstart -k system/com.tailscale.tailscaled`)
  → `serve status` STILL shows it (persistence = the whole point)
- Flip OpenClaw posture back: `gateway.bind: "loopback"` +
  `gateway.tailscale.mode: "serve"` via
  `~/node_modules/.bin/openclaw config patch --stdin`, kickstart gateway,
  verify `https://logans-macbook-pro.tail7453f8.ts.net` answers with TLS
- Final-values pass: `Secrets.kt` host → `https://logans-macbook-pro.tail7453f8.ts.net`
  (port 443 semantics), witnesses + session anchor updated once, never again
- Mac-side MagicDNS note: names resolve on the Mac only if `100.100.100.100`
  is set as a DNS server (optional — raw 100.x works for local probes; the
  Pixel resolves MagicDNS itself)

## Rollback

`sudo tailscaled uninstall-system-daemon`, reinstall the Standalone .pkg
(still in ~/Downloads), reboot. OpenClaw config backups in
`~/openclaw-preupdate-backups/` (`pre-tailnet-bind`, `pre-tailscale-serve`,
`pre-resolver-repoint`, plists).

## Related staging

- `IDAHO-VAULT/UPSTREAM-DRAFTS-2026-07-01.md` — three filing-ready reports (tailscale
  keychain-persist; openclaw CLI loopback dial; openclaw serve-enabled
  optimism). Filing gated on Logan, per-draft.
- Vault records: `OPENCLAW-BONJOUR-WORKAROUND-WITNESS-2026-07-01.md`,
  `VISIONCLAW-WITNESS-COMPANION-2026-07-01.md`,
  `.claude/MEMORY/SESSION-2026-06-29.md`.
