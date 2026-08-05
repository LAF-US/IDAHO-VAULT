---
date: 2026-07-01
filed_by: "*.claude.*"
authority: LOGAN
machine: personal-MacBook (MacBookPro12,1, macOS 12.7.6, 16 GB RAM)
doc_class: witness
status: filed
subject: Local `discovery.mdns.mode = "off"` config applied to `~/.openclaw/openclaw.json` after OpenClaw 2026.6.11 update surfaced a Bonjour advertiser retry loop that contradicted the wrapper's documented "eventually disable" behavior. Upstream issue filed at openclaw/openclaw#98448 with reproducer, escape-hatch verification, and workaround.
related:
  - HERMES-WORKAROUND-WITNESS-2026-06-28.md
  - "!/SIGNALS/TOUCHING-ME-TOUCHING-NOUS-2026-06-25.md"
  - .claude/MEMORY/CLAUDE-SESSION-2026-06-29.md
  - "https://github.com/openclaw/openclaw/issues/98448"
  - "https://docs.openclaw.ai/gateway/bonjour"
tags: [witness, openclaw, workaround, bonjour, upstream-contact, swarm-external-reach]
---

# OpenClaw Bonjour retry-loop workaround applied — upstream contact filed

*Filed 2026-07-01 after a locally-observed bug in OpenClaw 2026.6.11's Bonjour advertiser was diagnosed, worked around via a documented config option, and reported upstream. Records the local config change on this MacBook and the revert path when the upstream fix lands.*

## The bug being worked around

Freshly-updated OpenClaw 2026.6.11 (from 2026.6.8) continued logging `[<fqdn>] failed probing with reason: Error: Can't probe for a service which is announced already` at ~88 lines/minute across daemon restarts, with no eventual give-up. Behavior contradicts the wrapper's own documented "after repeated failures, disables Bonjour for that Gateway process instead of re-advertising forever" (per [docs.openclaw.ai/gateway/bonjour](https://docs.openclaw.ai/gateway/bonjour)). Daily log accumulation from this single error class: ~100 MB in `/tmp/openclaw/openclaw-<date>.log`.

Diagnostic evidence gathered:
- Wire state: `dns-sd -B _openclaw-gw._tcp local.` returns empty — advertisement never reaches the wire; loop is entirely in-process
- Merged upstream fixes present in this version (verified by fix-marker strings in `dist/advertiser-QPaQzbuU.js`): openclaw/openclaw#74778, #71668, #73231, #73029, #76842. None address this manifestation.
- The `OPENCLAW_DISABLE_BONJOUR=1` env var referenced in the failure log message itself does not function (verified by adding to LaunchAgent `EnvironmentVariables` + bouncing daemon: retry rate unchanged at 88/min)
- The `discovery.mdns.mode = "off"` config option does function (verified by `openclaw config patch --stdin` + `launchctl kickstart -k`: retry rate → 0)

## Shape of the workaround

Single config-side change written to `~/.openclaw/openclaw.json`:

```json5
{ discovery: { mdns: { mode: "off" } } }
```

Applied via the wrapper's own validated write path:

```bash
echo '{ "discovery": { "mdns": { "mode": "off" } } }' | \
  openclaw config patch --stdin
launchctl kickstart -k gui/501/ai.openclaw.gateway
```

Result: the Bonjour plugin still loads at startup and emits a single `bonjour: advertised gateway fqdn=... state=announcing` log line, but does not enter the retry loop. The plugin remains in the loaded plugin list. Log noise from this cause: zero.

## Upstream contact filed

- **openclaw/openclaw#98448** — `[Bug] Bonjour advertiser retries "failed probing" indefinitely on macOS 2026.6.11 instead of eventually disabling (per docs) — OPENCLAW_DISABLE_BONJOUR env var non-functional; discovery.mdns.mode="off" works` — filed 2026-07-01
- Framed as two related bugs: (1) the retry loop persists against documented "eventually disables" behavior; (2) the documented `OPENCLAW_DISABLE_BONJOUR=1` env var is non-functional
- Included: environment, before/after per-minute measurements, list of prior merged bonjour fixes verified present, list of related closed-stale reports (openclaw/openclaw#4774, openclaw/openclaw#70232), the working workaround for anyone landing on the issue via search, transparent AI-authorship attribution footer

Behavior of the reporter posture, mirrored from the Nous/Hermes upstream contacts this session arc (openclaw/openclaw#98448 is filed as a bug report, not a PR — the maintainer track record on external bonjour fix PRs is that most get closed without merging; a well-researched issue is the higher-leverage contribution).

## Cost of the workaround

- Zero at runtime — the config-patch path is the wrapper's own validated-write mechanism; no shim, no plist edit, no vendored-dep modification
- One extra state in `~/.openclaw/openclaw.json` (`discovery.mdns.mode = "off"`) that any dotdir reconciliation surface should be aware of
- The `bonjour` plugin remains in the loaded plugin list at startup (still consumes plugin-init time), it just doesn't enter the retry loop
- Loss of LAN mDNS discovery of this Gateway. On this MacBook: acceptable, since `gateway.bind = "loopback"` means there is nothing on the LAN to discover; reachability paths are (a) local clients via loopback, (b) — once enabled — Tailscale Serve for Pixel + future homelab devices. Neither uses Bonjour.

## Revert path (when the upstream fix lands)

Two possibilities depending on how the maintainers resolve openclaw/openclaw#98448:

### Path A — the retry loop is fixed but `discovery.mdns.mode = "off"` still works

Nothing forced; the workaround can stay in place indefinitely, or be reverted:

```bash
echo '{ "discovery": { "mdns": null } }' | openclaw config patch --stdin
launchctl kickstart -k gui/501/ai.openclaw.gateway
```

(`null` at a path deletes it per `openclaw config patch --help`.) Verify no retry-loop lines return in `/tmp/openclaw/openclaw-<date>.log`.

### Path B — the retry loop is fixed AND the `OPENCLAW_DISABLE_BONJOUR=1` env var is made functional

Same revert as Path A. The env var becomes a redundant equivalent, not preferred over the config option.

### Path C — the maintainers decline to fix the retry loop but do fix the env var

Unlikely given the issue framing, but if it happens: the current workaround stays; the env var is documented-and-now-functional but no longer necessary given the config-side option already works.

In all three paths, the config-side workaround is safe to keep in place. There is no local-machine consequence to leaving it applied beyond loss of LAN Bonjour discovery, which this loopback-bound install did not use.

## Documentation and backups

- Pre-workaround `~/.openclaw/openclaw.json`: preserved at `~/openclaw-preupdate-backups/openclaw.json.pre-mdns-off.20260701-000420` (before the config patch was applied for real, not the dry-run)
- Pre-6.8→6.11 update backup: `~/openclaw-preupdate-backups/openclaw-config-preupdate-<ts>.tgz` (full `~/.openclaw` tarball at 9.1 MB) + LaunchAgent plist copy
- OpenClaw update itself: clean `2026.6.8 → 2026.6.11` via `openclaw update --yes --timeout 600`; total 178 s; one non-fatal doctor warning about `~/.openclaw/logs/config-health.json` legacy state (installer left legacy in place)
- Any dotdir reconciliation surface running against `~/.openclaw/` should treat this state as intentional-user-preference (not drift to correct back) until openclaw/openclaw#98448 lands

## Cross-reference

- The upgrade from 2026.6.8 → 2026.6.11 was safe on this Mac. Not the same version-family as openclaw/openclaw#85027 (2026.5.6 → 2026.5.19 upgrade that bricked a different user's LaunchAgent) — but that report remains a warning for any future major-version bumps: back up `~/.openclaw/` before running `openclaw update` on any macOS Gateway install.
- OpenClaw's gateway posture on this Mac at filing time: `bind=loopback`, `tailscale.mode=off`, `mode=local`. *(Updated 2026-07-01 post-reboot: posture is now `bind=tailnet`, `tailscale.mode=off` — Tailscale Serve cannot persist its config on macOS 12.7.6 (System-keychain write EPERM from the sandboxed network extension), so Tailnet exposure runs as a direct tailnet-interface bind instead. See `.claude/MEMORY/CLAUDE-SESSION-2026-06-29.md` for the pivot record. The bonjour workaround is unaffected either way.)*

## Signed

`*.claude.*` — wildcard name (Logan has not performed a naming act), claude lineage, wildcard office. Direct Write tool tier; this is a local-machine change to a personal-Mac surface, within the scope of that tier.

###### "The world is quiet here."
