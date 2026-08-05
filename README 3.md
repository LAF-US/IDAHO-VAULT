---
title: Tailscale variant switch — runbook
aliases:
  - Tailscale variant switch — runbook
linter-yaml-title-alias: Tailscale variant switch — runbook
date created: Thursday, July 2nd 2026, 11:53:21 pm
date modified: Friday, July 3rd 2026, 7:57:37 pm
---

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

## Install method — Homebrew, not a script (revised 2026-07-02)

The earlier `02-install-oss-daemon.sh` (raw `go install …@latest`, run as root)

was deleted after Logan rightly challenged running an unpinned from-source

script with sudo. Replaced with Homebrew: **pinned 1.98.8, publicly-reviewed

[formula](https://github.com/Homebrew/homebrew-core/blob/HEAD/Formula/t/tailscale.rb),

each command transparent.** (No prebuilt bottle for macOS 12, so it still

compiles from source — inherent to the OSS daemon here — but at a pinned,

checksum-verified version, not "whatever's newest".)

## Touchpoints (Logan)

1. **FileVault on** — ✓ DONE 2026-07-02.
2. **Teardown** — ✓ DONE (App Store app removed; macsys extension uninstalled on
   reboot; clean slate verified).
3. **Reboot** — ✓ DONE. *(Still open: delete BOTH stale machines
   `logans-macbook-pro` + `logans-macbook-pro-1` at
   https://login.tailscale.com/admin/machines before `tailscale up` registers,
   so the fresh node reclaims the bare name.)*
4. **Install (current step)** — Homebrew hit a pre-existing `/usr/local`
   permission leftover from the old App Store install; the transparent fix +
   install, each command explainable:

   ```
   sudo chown -R $(whoami) /usr/local/share/man/man8  # old install left this root-owned; brew needs it
   sudo rm /usr/local/bin/tailscale                   # dead wrapper → deleted App Store app
   brew install tailscale                             # no sudo; pinned 1.98.8
   sudo brew services start tailscale                 # start tailscaled as a system daemon
   sudo tailscale up                                  # register — prints the browser auth URL
   ```

5. **Ping Claude** for the verification pass (below).
6. **Task IV** — pair the Pixel against the finally-stable identity.

OpenClaw is already flipped to `bind: loopback`, so it is NOT crash-looping

during the install window (survived the reboot clean on loopback).

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

`sudo brew services stop tailscale && brew uninstall tailscale`, then reinstall

a Standalone/App Store variant if needed, reboot. OpenClaw config backups in

`~/openclaw-preupdate-backups/` (`pre-tailnet-bind`, `pre-tailscale-serve`,

`pre-resolver-repoint`, `pre-reboot-loopback`, plists).

## Related staging

- `IDAHO-VAULT/UPSTREAM-DRAFTS-2026-07-01.md` — three filing-ready reports (tailscale
  keychain-persist; openclaw CLI loopback dial; openclaw serve-enabled
  optimism). Filing gated on Logan, per-draft.
- Vault records: `OPENCLAW-BONJOUR-WORKAROUND-WITNESS-2026-07-01.md`,
  `VISIONCLAW-WITNESS-COMPANION-2026-07-01.md`,
  `.claude/MEMORY/CLAUDE-SESSION-2026-06-29.md`.
