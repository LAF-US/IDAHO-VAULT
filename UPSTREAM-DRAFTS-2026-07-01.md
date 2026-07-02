---
date: 2026-07-01
filed_by: "*.claude.*"
authority: LOGAN
doc_class: draft-records
status: staged — filing gated per-draft on Logan (external-contact protocol)
subject: Three filing-ready upstream reports drafted from the 2026-07-01 Tailscale/OpenClaw diagnostics. Nothing here is filed; each posts only on Logan's explicit per-draft go.
tags: [records, draft, upstream-contact-pending, tailscale, openclaw]
---

# Upstream report drafts — staged 2026-07-01

# DRAFT — for tailscale/tailscale (filing gated on Logan)

**Title:** macOS 12 (Monterey) + standalone/macsys 1.98.8: SecureStorage keychain writes fail with EPERM — serve config silently dropped, node re-registers as a new machine on every restart; CLI reports success

## Environment
- macOS 12.7.6 (Monterey, x86_64), MacBookPro12,1
- Tailscale Standalone (macsys) 1.98.8, system extension `io.tailscale.ipn.macsys.network-extension (1.98.8/101.98.8)` `[activated enabled]` — single extension, freshly rebooted host
- Single-user tailnet, MagicDNS + HTTPS certs enabled

## Symptoms
1. `tailscale serve --bg 18789` prints the full success banner ("Available within your tailnet: … Serve started and running in the background.") — but `tailscale serve status` immediately afterward reports `No serve config`. The config is applied transiently and dropped when persistence fails.
2. On every restart of the extension/host, the machine re-registers as a **new node** (name suffix churn: `hostname` → `hostname-1`, old record left offline-stale). Observed repeatedly; the stored login is reused so re-registration is silent.
3. `security dump-keychain /Library/Keychains/System.keychain | grep -ci tailscale` → **0** — nothing has ever persisted.

## Extension log (unified log, at serve-config write)
```
localapi: [POST] /localapi/v0/serve-config
[general] - SecureStorage.saveData: update tailscale-serve/3ae5 in keychain: no such item
[com.apple.securityd:atomicfile] create /Library/Keychains/System.keychain.sb-<id>: Operation not permitted
[general] - SecureStorage.saveData: add tailscale-serve/3ae5: failed to add item (137 bytes) to keychain: 100001: UNIX[Operation not permitted]
[general] - prefs_save failed: err("add tailscale-serve/3ae5: failed to add item (137 bytes) to keychain: 100001: UNIX[Operation not permitted]")
```
The `atomicfile create … Operation not permitted` is logged from within the extension process — the write appears to run in-process against the file-based System keychain and be denied by the extension sandbox (macOS 12 may lack the newer securityd path this flow expects).

## Impact
- Tailscale Serve unusable (silently: every UI/CLI surface reports success).
- Node identity churn on every restart: stale machine records accumulate; MagicDNS names change (`-1`, `-2`, …), breaking anything pinned to the name; key-expiry/ACL hygiene degraded.

## Repro
1. macOS 12.7.6 + Standalone 1.98.8, login normally.
2. `tailscale serve --bg <port>` → success banner.
3. `tailscale serve status` → `No serve config`.
4. Reboot → `tailscale status --self` shows a brand-new node with suffixed hostname; previous record offline.

## Notes
- macOS 12 is currently the documented minimum supported version; if this flow requires macOS 13+, a hard error (or documented floor bump) would be far better than silent success.
- Workaround adopted locally: switch to the open-source `tailscaled` variant (file-based state) — both symptoms disappear by construction.

---
*Report researched and drafted with AI assistance (Claude); observations reproduced live on the affected machine.*

---

# DRAFT — for openclaw/openclaw (filing gated on Logan)

**Title:** [Bug] CLI dials ws://127.0.0.1 when `gateway.bind: "tailnet"` — knows the bind mode, prints it in the error, still uses loopback

## Environment
- OpenClaw 2026.6.11 (e085fa1), macOS 12.7.6, node 24.15.0
- `gateway.bind: "tailnet"`, `gateway.auth.mode: "token"`, gateway healthy and listening on the tailnet address (verified `HTTP 200` via tailnet IP and MagicDNS name)

## Symptom
Any gateway-dialing CLI command (e.g. `openclaw devices list`) fails:

```
[openclaw] Could not start the CLI.
[openclaw] Reason: gateway closed (1006 abnormal closure (no close frame)): no close reason
Gateway target: ws://127.0.0.1:18789
Source: local loopback
...
Bind: tailnet
```

The error output itself reports `Bind: tailnet` while showing the dial target derived from `local loopback`. With `bind: "tailnet"` nothing listens on 127.0.0.1, so every local CLI invocation fails.

## Expected
When `gateway.bind` is `tailnet` (or any non-loopback bind), the CLI's local-gateway dial derivation should follow the bind mode (dial the tailnet address), or the failure should say explicitly that loopback is unavailable under this bind and name the override.

## Workaround (and a UX wrinkle)
`OPENCLAW_GATEWAY_URL="ws://<magicdns>:18789"` works but then **requires explicit credentials** (`gateway url override requires explicit credentials`) even though `gateway.auth.token` is present in the same config file the CLI already read — so the workaround needs both the URL *and* `OPENCLAW_GATEWAY_TOKEN` exported per invocation. Honoring the config token under a URL override (or a `--use-config-token` flag) would make the workaround one variable instead of two.

---
*Report researched and drafted with AI assistance (Claude); reproduced live.*

---

# DRAFT — for openclaw/openclaw (filing gated on Logan)

**Title:** [Bug] Gateway logs `[tailscale] serve enabled: https://…` without verifying the serve registration took — masks total Serve failure

## Environment
- OpenClaw 2026.6.11 (e085fa1), macOS 12.7.6
- `gateway.tailscale.mode: "serve"`, Tailscale Standalone (macsys) 1.98.8

## Symptom
On every gateway start, the log reports success:

```
[gateway] ready
[tailscale] serve enabled: https://<host>.ts.net/ (WS via wss://<host>.ts.net)
```

— while on the Tailscale side the serve-config write fails (macOS keychain persistence bug, reported separately to tailscale) and `tailscale serve status` shows `No serve config`. The HTTPS endpoint never exists; nothing in OpenClaw's logs or `openclaw status` reflects that. `openclaw status` likewise shows `Tailscale exposure: serve · <host> · https://<host>` — all derived from intent, not observation.

## Expected
After applying serve config, read it back (`tailscale serve status` / LocalAPI GET) and log/surface the verified state. If verification fails: log an error, and ideally surface it in `openclaw status` and doctor — a silent no-op on the primary remote-access path is expensive to diagnose (the failure only appears in the macOS unified log of the Tailscale extension).

## Repro
1. Any environment where `tailscale serve` cannot persist (e.g. macOS 12 + macsys 1.98.8, upstream keychain EPERM).
2. Set `gateway.tailscale.mode: "serve"`, restart gateway.
3. Gateway logs `serve enabled`; `tailscale serve status` → `No serve config`; the advertised URL is dead.

---
*Report researched and drafted with AI assistance (Claude); reproduced live.*
