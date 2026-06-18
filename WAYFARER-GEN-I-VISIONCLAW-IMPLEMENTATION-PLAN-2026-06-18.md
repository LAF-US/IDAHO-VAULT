---
title: "Wayfarer Gen I VisionClaw Implementation Plan"
updated: 2026-06-18
status: draft
authority: LOGAN
author: Codex
doc_class: implementation_plan
tags:
  - research/wearables
  - ai/smart-glasses
  - meta/ray-ban
  - visionclaw
  - openclaw
related:
  - RAY-BAN-META-SIDELOAD-APP-RESEARCH-2026-06-18.md
  - .openclaw/openclaw-live-ref.json
  - .openclaw/SECRETS-1PASSWORD.md
---

# Wayfarer Gen I VisionClaw Implementation Plan

## Scope

Target hardware: Logan's Meta Ray-Ban Wayfarer Gen I pair.

Working assumption: no Ray-Ban Display, no right-lens UI, no glasses-hosted web
app. The viable path is a companion phone app that talks to the glasses through
Meta's Wearables Device Access Toolkit (DAT).

## Current Local Constraints

The checked-in OpenClaw reference config shows:

- gateway mode: `local`
- gateway bind: `loopback`
- gateway port: `18789`
- gateway auth: token via `OPENCLAW_GATEWAY_TOKEN`
- OpenRouter key: environment-backed, not literal in the reference file

The local OpenClaw secrets note says the gateway was containment-stopped on
2026-05-26 and should not be started again until gateway and Discord
credentials are rotated and allowed Discord destinations are confirmed.

Therefore, the first Wayfarer proof should not require OpenClaw gateway access.
Treat OpenClaw as a later controlled integration step.

## Phase 0 - Hardware and Account Inventory

Goal: confirm exact device and account preconditions without writing secrets.

Checklist:

1. Confirm exact model name and firmware in the Meta AI app.
2. Confirm Meta AI app is current on the target phone.
3. Confirm the phone platform for first build: iOS physical device, Android
   physical device, iOS simulator, or Android emulator.
4. Confirm Developer Mode is visible for the glasses in Meta AI.
5. Confirm whether the Wearables Developer Center account and app record already
   exist.
6. Record only non-secret metadata in the vault.

Exit condition:

- A short device/account note exists with model, firmware, phone OS, and whether
  Developer Mode is available.

## Phase 1 - Phone-Camera Smoke Test

Goal: test the AI loop without DAT, glasses, or OpenClaw.

Use VisionClaw phone-camera mode or a minimal local equivalent. This reduces the
problem to:

- camera frame capture
- audio/text prompt path
- model request/response
- visible streaming-active state

Requirements:

- Gemini or alternate model credential stored outside the repo.
- No captured footage committed.
- No OpenClaw gateway.
- No glasses permissions.

Exit condition:

- The phone app can capture low-rate camera frames and produce a model response
  in a visible test UI.

## Phase 2 - DAT Camera Proof

Goal: replace the phone camera with Wayfarer camera access through DAT.

Build target:

- ordinary Ray-Ban Meta / Wayfarer Gen I
- DAT camera/photo capability only
- no display module assumptions

For Android, Android Studio is used to build/install/debug the phone app and
wire local secrets or endpoint settings. It is not expected to be an SDK-editing
surface; Meta's DAT SDK should remain an upstream dependency unless there is a
confirmed SDK defect.

Checklist:

1. Add the platform DAT SDK through Swift Package Manager or Android GitHub
   Packages.
2. Configure the development app ID mode required by Meta's DAT guidance.
3. Register the app through Meta AI.
4. Request only camera permission.
5. Start with still-photo or lowest-rate frame capture.
6. Add an in-app "glasses camera active" indicator.
7. Verify no frames, logs, or API keys are written into tracked files.

Exit condition:

- The app can acquire a Wayfarer-origin frame/photo through DAT and display or
  process it locally.

## Phase 3 - Model Loop With Wayfarer Frames

Goal: attach the Wayfarer-origin frame stream to the AI loop.

Constraints:

- Keep the frame rate low.
- Prefer still-photo or one-frame prompts before continuous streaming.
- Do not send bystander-sensitive test material to a remote provider.
- Keep API keys out of repo, chat, logs, and screenshots.

Exit condition:

- A controlled test frame from the glasses reaches the model and returns a
  response in the app.

## Phase 4 - OpenClaw Tool-Call Dry Run

Goal: validate the tool-call shape without exposing the gateway to the phone.

Because the checked-in OpenClaw posture is loopback-bound, a physical phone
cannot reach the gateway directly. Use one of these safer first options:

- iOS simulator on the Mac host if the app path supports simulator testing.
- Android emulator using the host gateway address pattern for emulator-to-host
  access.
- A local mock OpenClaw endpoint that validates request shape but performs no
  real action.

Do not start or expose the real OpenClaw gateway unless the credential rotation
and allowed-destination requirements in `.openclaw/SECRETS-1PASSWORD.md` are
satisfied.

Exit condition:

- The app can produce a tool-call request and receive a mock or loopback-gateway
  response without LAN exposure.

## Phase 5 - Physical Phone to OpenClaw

Goal: connect a real phone app to OpenClaw only after an explicit network and
credential decision.

Required decisions before this phase:

1. Whether to bind the gateway beyond loopback or use a tunnel.
2. Which network is trusted for the test.
3. Whether Discord/other channel destinations are disabled or allowlisted.
4. Which gateway token is active and where it is stored.
5. What audit note records the operation.

Hard constraints:

- No public exposure.
- No unauthenticated gateway.
- No plaintext tokens in tracked files.
- No broad tool permissions for the first physical-phone test.

Exit condition:

- Physical phone can issue a narrowly scoped authenticated tool call to OpenClaw
  and receive a response, with the operation recorded.

## Immediate Next Action

Start with Phase 0 and Phase 1. The fastest low-risk proof is phone-camera mode
with no glasses and no OpenClaw. After that works, move to DAT camera access on
the Wayfarer Gen I pair.

## Local Sources Read

- `RAY-BAN-META-SIDELOAD-APP-RESEARCH-2026-06-18.md`
- `.openclaw/openclaw-live-ref.json`
- `.openclaw/SECRETS-1PASSWORD.md`
- `!/SNAPSHOT-OPENROUTER-HERMES-BEEFSTACK-2026-05-18.md`
- `!/SNAPSHOT-OPENROUTER-HERMES-OPENCLAW-KEYS-2026-05-20.md`
