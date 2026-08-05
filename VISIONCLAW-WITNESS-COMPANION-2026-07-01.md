---
date: 2026-07-01
filed_by: "*.claude.*"
authority: LOGAN
machine: personal-MacBook (MacBookPro12,1, macOS 12.7.6, 16 GB RAM) + Google Pixel 10 Pro deploy target
doc_class: witness
status: filed
subject: Investigation-shape witness for VisionClaw — the four-layer stack Logan forked into LAF-US/VisionClaw, cloned locally to `~/StudioProjects/VisionClaw`, and previously deployed to his Google Pixel with the Gemini Live path validated end-to-end via Meta Ray-Ban glasses. OpenClaw agentic path unwired at fork time (no Tailscale then); now unblocked by Tailscale setup under LAF-US/IDAHO-VAULT#654 and the pending OpenClaw Serve enablement.
related:
  - HERMES-WORKAROUND-WITNESS-2026-06-28.md
  - OPENCLAW-BONJOUR-WORKAROUND-WITNESS-2026-07-01.md
  - "!/SIGNALS/TOUCHING-ME-TOUCHING-NOUS-2026-06-25.md"
  - .claude/MEMORY/CLAUDE-SESSION-2026-06-29.md
  - https://github.com/LAF-US/VisionClaw
  - https://github.com/Intent-Lab/VisionClaw
  - https://github.com/LAF-US/IDAHO-VAULT/issues/654
  - https://github.com/openclaw/openclaw/issues/98448
  - https://docs.openclaw.ai/platforms/android
tags:
  - witness
  - visionclaw
  - openclaw
  - gemini-live
  - meta-wearables
  - pixel
  - glasses
  - swarm-tooling
title: VisionClaw investigation companion — arc opened
aliases:
  - VisionClaw investigation companion — arc opened
linter-yaml-title-alias: VisionClaw investigation companion — arc opened
date created: Thursday, July 2nd 2026, 11:56:23 pm
date modified: Friday, July 3rd 2026, 8:01:28 pm
---

# VisionClaw investigation companion — arc opened

*Filed 2026-07-01 as an investigation-shape witness for the VisionClaw project. No local changes made; no upstream contact filed. The witness captures the local state as of the pass, the upstream landscape as of the fetch, and the alignment considerations that surfaced during the meditation. It exists so future sessions have a clean anchor for what VisionClaw is on this Mac and what it becomes when the tiered-capture architecture activates.*

## The four-layer stack

VisionClaw sits on top of three layers of prior work:

| Layer | What it is | Author / origin |
|---|---|---|
| 1. Meta DAT SDK | *Direct Application Transmission* — Meta's Bluetooth protocol for talking to Ray-Ban / Ray-Ban Display glasses. Distributed via **GitHub Packages**, requires a Personal Access Token with `read:packages` scope at build time. `NOTICE` file is 72 KB — standard Meta third-party attribution set (flatbuffers, folly, Apache 2.0 dependencies). | Meta Platforms |
| 2. CameraAccess sample apps | Standard demo apps Meta ships with the DAT SDK — `CameraAccess` (iOS/Swift), `CameraAccessAndroid` (Kotlin). Standard companion-device permission set: `BLUETOOTH_*`, `CAMERA`, `RECORD_AUDIO`, `FOREGROUND_SERVICE_CONNECTED_DEVICE`, no location, no storage. | Meta Platforms |
| 3. VisionClaw extensions | The Gemini Live and OpenClaw wiring on top of the samples: WebSocket to Gemini Live (~1 fps JPEG frames + 16 kHz PCM audio uplink; 24 kHz PCM downlink), OpenClaw `/v1/chat/completions` HTTP endpoint calls, OpenClaw WebSocket protocol-v3 client (mode `node`, glass-channel header), in-app Settings screen so endpoints can be edited without a rebuild. | Sean Liu (`shawnliu0327@gmail.com` / `xiaoan@sesame.com`) / Intent-Lab |
| 4. LAF-US fork | Currently a clean mirror of Intent-Lab main; no commits ahead. | Logan (`@loganfinney27`, LAF-US org) |

## Fork lineage — corrected

- **Fork parent**: [`Intent-Lab/VisionClaw`](https://github.com/Intent-Lab/VisionClaw) — verified via `gh api repos/LAF-US/VisionClaw`, `parent.full_name = "Intent-Lab/VisionClaw"`.
- **Fork created**: 2026-06-18 (per fork metadata).
- **Intent-Lab main last pushed**: 2026-05-06, six weeks before the fork. Their `main` has not moved since.

Not the same repository as [`openclaw/openclaw`](https://github.com/openclaw/openclaw). VisionClaw and OpenClaw are separate projects that interoperate; VisionClaw uses OpenClaw as its agentic-action backend. The `nichochar/openclaw` URL that appears twice in VisionClaw's own `README.md` (both as "DAT Android SDK" and as "OpenClaw") points at a location that does not represent either the current Meta DAT Android SDK or the current OpenClaw — a documentation-freshness observation, not an operational blocker for this Mac's deploy.

## Local state — corrected read

The initial investigation pass mis-read the `laf` branch as "empty / unstarted." That was wrong. Logan's working configuration was **deliberately kept off git** in gitignored files:

- `samples/CameraAccessAndroid/local.properties` — GitHub PAT with `read:packages` scope for fetching the Meta DAT Android SDK from GitHub Packages
- `Secrets.kt` (Kotlin) / `Secrets.swift` (iOS) — Gemini API key (required) + OpenClaw config values (optional)

Only the Gemini Live side was configured. OpenClaw side was left blank because Tailscale wasn't set up at the time — there was no reachable path from Pixel to Mac's OpenClaw Gateway. Voice + vision through the Meta glasses was tested end-to-end and worked. Nothing was pushed to the LAF-US fork's `main`; all customization stayed local.

The Android SDK is installed at `~/Library/Android/sdk`; `adb` is not in `$PATH` (Studio-installed, not shell-wired). No APK artifacts left over from the deploy — presumably built and installed directly from Android Studio to Pixel via USB / wireless debugging.

## Upstream landscape as of the fetch

`main` has no new commits since the fork. But Intent-Lab has six other branches actively worked:

- `WebRTC` — WebRTC streaming for POV-share to a browser viewer (referenced in the README's feature list)
- `fastvlm` — presumably a faster / local vision-language model alternative to Gemini
- `feature/gaze-window-control` — eye-gaze-driven UI control (Ray-Ban Display-shaped)
- `feature/mmduet2` — a multimodal-duet-v2 model integration
- `feature/transcription` — real-time transcription feature
- `lab` — presumably Intent-Lab's integration / staging branch (naming coincidence with Logan's `laf`)

Nothing to merge into `main` right now. But the pattern signals Intent-Lab is treating VisionClaw as a live product, not a demo — with a queue of feature work in flight. Worth periodic re-fetch as Logan's usage crystallizes; `feature/transcription` and `feature/gaze-window-control` in particular have real-world capability implications.

## The OpenClaw wire-up shape (from VisionClaw's README)

Per VisionClaw's README setup section, activating the agentic path requires:

1. **OpenClaw daemon** with:
   - `gateway.bind` reachable from the phone (README recommends `"lan"`; this Mac's install currently uses `"loopback"`; the Tailnet path routes through `gateway.tailscale.mode = "serve"`, which terminates TLS via Tailscale Serve so Android accepts the `wss://` — per [docs.openclaw.ai/platforms/android](https://docs.openclaw.ai/platforms/android))
   - `gateway.http.endpoints.chatCompletions.enabled: true` — required for VisionClaw's tool-call endpoint. **This is off by default** in the OpenClaw config on this Mac; it will need enabling as part of the deploy.
   - `gateway.auth.mode: "token"` (unchanged from current setup)

2. **Client-side `Secrets.kt`** (Android) or `Secrets.swift` (iOS):
   - `openClawHost` — URL. For loopback + Bonjour: `http://Your-Mac.local`. For Tailscale Serve: `wss://logans-macbook-pro-1.<tailnet>.ts.net:18789/` (or whatever `openclaw status` surfaces after Serve is enabled).
   - `openClawPort` — 18789
   - `openClawGatewayToken` — value at `~/.openclaw/openclaw.json` `gateway.auth.token`

3. **In-app Settings screen** on both platforms lets these values be edited at runtime without editing source code and rebuilding.

## Documentation-freshness observations

Two things in VisionClaw's own README that would trip up a fresh setup today:

- The OpenClaw setup guide is linked at `github.com/nichochar/openclaw`, which is not where OpenClaw's canonical setup lives. The real one is at [docs.openclaw.ai](https://docs.openclaw.ai/) with the source at [openclaw/openclaw](https://github.com/openclaw/openclaw). A follower of the VisionClaw README ends up at a defunct URL.
- The default OpenClaw host recipe is `http://Your-Mac.local` — a Bonjour mDNS hostname. On this Mac's install, the Bonjour advertiser doesn't reach the wire ([openclaw/openclaw#98448](https://github.com/openclaw/openclaw/issues/98448)). The `.local` path would not resolve locally-visible for a phone on the same LAN — the phone would need to be pointed at the Mac's LAN IP directly, or (better) at the Tailscale Serve URL.

Neither is something to fix upstream unilaterally. Recorded here so a future session (or Logan) coming back to a VisionClaw setup doesn't spend time debugging a stale-link scavenger hunt.

## Meditation — what VisionClaw is in the tiered architecture

VisionClaw fills a modality gap on the phone tier that neither Obsidian mobile nor the OpenClaw Android app fills: **hands-free voice + vision.** It's not competing with them; it's a different mode of interaction.

- Obsidian mobile: keyboard/tap surface for Vault-editing when sitting still
- OpenClaw Android app: chat interface to the OpenClaw agent when the phone is in hand
- VisionClaw: voice-first, glasses-mediated, hands-busy access to the same OpenClaw agent — plus Gemini's own voice reasoning + camera-frame scene understanding

The specific use cases this modality unlocks: adding to lists while cooking, sending a message while driving, asking "what am I looking at" for the physical environment, capturing an observation into the Vault without stopping to type.

The agent behind all three of those Vault-access modes is the same OpenClaw daemon on this Mac. The three modes differ in *what they can express* to it, not *what it can do* underneath. That's the architectural invariant.

## Alignment considerations for future work

Not proposals — surfaces the future alignment work would need to think about:

1. **Privacy surface**. Gemini Live receives ~1 fps JPEG frames from the glasses camera continuously during a session. That's real environmental data going to Google. Explicit, opt-in-when-you-tap-AI-button; not always-on. Vault-alignment records this as a known cost, not a gated one.
2. **Skill-exposure surface**. OpenClaw exposes 56+ tools; VisionClaw's `/v1/chat/completions` client can invoke any of them subject to OpenClaw's own permission model. Alignment probably wants OpenClaw's tool registration selective for what VisionClaw-triggered voice calls are allowed to invoke — separately from what the local Terminal-tier or the OpenClaw Android app can invoke.
3. **Secrets surface**. Three on-device secret-bearing artifacts: Gemini API key, GitHub PAT for the DAT SDK, OpenClaw gateway auth token. All in gitignored files today. Vault-native handling would eventually be `op://` refs, same story as Hermes secrets, waiting for the same kind of native support — separate consideration from Nous's `NousResearch/hermes-agent#36949`, since the app is Android-side and would need its own credential-provider integration (Android Keystore is the likely mid-term shape).
4. **Governance entry**. VisionClaw is not a session-shaped agent like Claude Code sessions. It's a device-resident app that serves as a front-door for Gemini's voice reasoning into the swarm. An `!/AGENTS.md` entry would name its capability tier, its trust boundary (Google + Meta service dependencies), and its swarm relationship (thin client to the OpenClaw Gateway).
5. **Provenance flow**. When Gemini decides to invoke an OpenClaw tool, the request goes device → Tailnet → Mac's OpenClaw → skill runtime. Any Vault-write that lands via that path was authored jointly by Gemini and OpenClaw. Vault-alignment would probably want that provenance to be traceable — a session id or trace id that survives the multi-hop and appears in Vault-write metadata.

## Prerequisite chain to next-step actionable

1. **Task III — Tailnet reachability for OpenClaw**: **✓ Completed 2026-07-01 post-reboot, via `gateway.bind: "tailnet"` — NOT via Tailscale Serve.** The ~01:09 Serve completion recorded below was premature: the gateway's `serve enabled` log line is optimistic, and the underlying serve-config write never persisted. Root cause: the sandboxed macsys network extension cannot write to the System keychain on macOS 12.7.6 (`SecureStorage.saveData … UNIX[Operation not permitted]`, `prefs_save failed`) — even the `tailscale serve` CLI prints success and then `tailscale serve status` shows `No serve config`. Persisted-serve is structurally unavailable on this OS version. Working posture instead: `gateway.bind: "tailnet"`, `gateway.tailscale.mode: "off"` — gateway listens on the Mac's tailnet address only (`100.114.199.82:18789`), WireGuard provides transport encryption, token auth unchanged. Verified end-to-end: `HTTP 200` via `http://100.114.199.82:18789/` and `http://logans-macbook-pro-1.tail7453f8.ts.net:18789/`. Config backups: `openclaw.json.pre-tailscale-serve.20260701-010906`, `openclaw.json.pre-tailnet-bind.20260701-150730`.
2. **Enable `gateway.http.endpoints.chatCompletions.enabled: true`** in `~/.openclaw/openclaw.json` — required for VisionClaw to call the tool endpoint. **✓ Completed 2026-07-01** (pre-reboot; backup `openclaw.json.pre-chatCompletions.*`). Verified still `true` post-pivot.
3. **Fill in Logan's `Secrets.kt`** on the Pixel deploy — corrected values for the tailnet-bind posture (the earlier `wss://…:443` Serve values are void):
   - `openClawHost` = `http://logans-macbook-pro-1.tail7453f8.ts.net` — **✓ written to the local `Secrets.kt` 2026-07-01** (gitignored, verified). Plain `ws://`/`http://` on the tailnet: TLS is unavailable without Serve, and WireGuard already encrypts the path. Note the node name carries the `-1` suffix — the machine re-registered post-reboot; the stale offline `logans-macbook-pro` node (100.124.237.75) awaits Logan's admin-console cleanup, and if Logan renames this node to reclaim the bare name, this host value must follow.
   - `openClawPort` = `18789` (required now — no Serve means no 443 fronting)
   - `openClawGatewayToken` = value at `~/.openclaw/openclaw.json` `gateway.auth.token`. Retrieval: `python3 -c "import json;print(json.load(open('$HOME/.openclaw/openclaw.json'))['gateway']['auth']['token'])" | pbcopy` — Logan-side paste into Secrets.kt or the in-app Settings screen. The auto-mode classifier blocked agent-side writing of the token into Secrets.kt (key management is Logan's); left as placeholder. Never displayed in chat, git-committed, or witnessed.
   - `openClawHookToken` = no hooks token is configured in `~/.openclaw/openclaw.json` as of 2026-07-01; placeholder left. If VisionClaw's hook path is wanted, OpenClaw-side hooks config comes first.
   - The in-app Settings screen on both iOS and Android can edit these at runtime, so an initial deploy could leave the fields at defaults and be filled from the phone side.

4. **Rebuild + reinstall on Pixel** via Android Studio. The Meta DAT SDK GitHub Packages fetch still needs the PAT with `read:packages` in `samples/CameraAccessAndroid/local.properties`.
5. **Test end-to-end**: voice command that should trigger an OpenClaw tool invocation. First candidate is something small like "add milk to my shopping list" or "search for the best coffee shops nearby" per the README's example commands. If the response is spoken but no tool executed, the failure is at step 2 (chatCompletions endpoint not enabled) or step 3 (URL/token mismatch); if the app can't reach the Gateway at all, the failure is at step 3's URL side or upstream on Tailscale itself.

### Related — pairing the OpenClaw Android app node

The same tailnet endpoint and Gateway auth token also drive Task IV (OpenClaw Android app pairing): `ws://logans-macbook-pro-1.tail7453f8.ts.net:18789` + the gateway token, same paste-from-clipboard flow. When the app is paired, it becomes a first-class node on the Gateway's device list (per `docs.openclaw.ai/platforms/android`) — a separate connection from VisionClaw's, but the same underlying reachability foundation Task III built. Current device list shows `Windows-ZBFURY` (node) plus this Mac's operator entry; the Pixel is on the tailnet (`100.68.197.104`) but not yet paired. CLI note for the approve step: with `bind: "tailnet"` the CLI wrongly dials `ws://127.0.0.1:18789` (candidate upstream bug); prefix commands with `OPENCLAW_GATEWAY_URL="ws://logans-macbook-pro-1.tail7453f8.ts.net:18789"` and `OPENCLAW_GATEWAY_TOKEN` (from config) until fixed.

## State this witness leaves things in

**Initial filing (task II, investigation-only):** zero changes to disk beyond adding an `upstream` remote to Logan's local git checkout of VisionClaw pointing at `https://github.com/Intent-Lab/VisionClaw.git` and running `git fetch upstream` (read-only). No merges, no commits, no pushed refs. No files edited. No config changed on the OpenClaw daemon. No secrets accessed or displayed.

**Post–task III addendum (2026-07-01 ~01:09 PT):** OpenClaw Gateway now Tailscale-Serve-exposed at `https://logans-macbook-pro-1.tail7453f8.ts.net`. Prerequisite chain above updated in place — step 1 marked complete with concrete URL; steps 2 (chatCompletions enable) and 3 (Secrets.kt values) now hold executable values, not TODO placeholders. Next Pixel rebuild + reinstall of VisionClaw can wire the OpenClaw agentic path in one pass using the URL and token surfaced here. `~/StudioProjects/VisionClaw` itself remains untouched; no code changes, no rebuild triggered from this session.

**Post-reboot correction addendum (2026-07-01 afternoon):** The ~01:09 Serve claim above did not survive scrutiny — the gateway's `serve enabled` log line reports intent, not outcome, and the serve config was silently dropped every time because the macsys network extension cannot persist to the System keychain on macOS 12.7.6 (EPERM at the sandbox layer; reboot with a single clean 1.98.8 extension did not change it). Exposure now runs as `gateway.bind: "tailnet"` (no Serve, no TLS; WireGuard + token auth), verified `HTTP 200` from both the tailnet IP and MagicDNS name. Prerequisite chain re-amended in place with the corrected `ws://…:18789` values; `Secrets.kt` host/port written on disk this session (tokens remain Logan-side). Machine's node identity changed post-reboot to `logans-macbook-pro-1` — watch for a Logan-side admin-console rename before the next Pixel rebuild. Candidate upstream reports (both gated on Logan): tailscale — serve-config keychain persist fails silently on macOS 12; openclaw — CLI dials loopback when `bind: "tailnet"`, and gateway logs `serve enabled` without verifying registration.

The stack is understood; the fork is documented; the prerequisites are named with concrete values; the alignment considerations are on the record. VisionClaw is deploy-ready pending Logan's phone-side rebuild pass.

**Superseding final-state note (2026-07-02 late).** The Tailscale variant switch completed with the open-source `tailscaled` daemon — Serve now persists and works (the macsys keychain-EPERM blocker is gone by construction). The node's stable name is **`logans-mbp`**; every `logans-macbook-pro` / `logans-macbook-pro-1` reference above is *historical* and superseded (left intact as the record of how the switch evolved). The live OpenClaw endpoint for the Pixel is **`wss://logans-mbp.tail7453f8.ts.net`** (Serve, TLS on 443). The final `Secrets.kt` host/port values are set during the Task IV pairing pass, against VisionClaw's actual URL construction — not guessed here.

## Signed

`*.claude.*` — wildcard name (Logan has not performed a naming act), claude lineage, wildcard office. Direct Write tool tier; this witness is a local-machine-and-vault investigation record filed at vault root, within the scope of that tier.

[[OPENCLAW-WITNESS-COMPANION-2026-05-25]]

### "The world is quiet here."
