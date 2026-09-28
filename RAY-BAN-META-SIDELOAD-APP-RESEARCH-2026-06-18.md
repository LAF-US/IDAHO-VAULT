---
title: "Ray-Ban Meta Sideload App Research"
updated: 2026-06-18
status: draft
authority: LOGAN
author: Codex
doc_class: research_note
tags:
  - research/wearables
  - ai/smart-glasses
  - meta/ray-ban
  - visionclaw
---

# Ray-Ban Meta Sideload App Research

## Hardware Clarification

Logan has a pair of Meta Ray-Ban Wayfarer Gen I glasses. Treat this as the
ordinary Ray-Ban Meta / no-display path unless proven otherwise by exact model
metadata in the Meta AI app. That means the relevant build target is a companion
phone app using DAT camera/photo capabilities. Ray-Ban Display web apps and
right-lens display UI are not available on this hardware.

## Bottom Line

"Sideload the app onto the Ray-Bans" is mostly the wrong model for ordinary
Ray-Ban Meta glasses. The practical development path is:

1. Install or run a developer build of a phone app on iOS or Android.
2. Pair the glasses through the Meta AI companion app.
3. Enable Developer Mode for the linked glasses.
4. Have the phone app register with Meta AI and request device permissions.
5. Use Meta's Wearables Device Access Toolkit (DAT) to stream camera frames,
   capture photos, or, on Meta Ray-Ban Display, render display content.

For non-display Ray-Ban Meta glasses, the custom code lives in the companion
phone app, not on the glasses as a standalone app. For Meta Ray-Ban Display,
Meta opened a developer-preview path in May 2026 for both mobile-app display
extensions and web apps that can be deployed to the glasses.

## What Meta Exposes

Meta's public DAT repositories describe the toolkit as a developer-preview SDK
for "hands-free wearable experiences" in mobile apps. The public iOS and
Android repos say DAT can connect to Meta AI glasses and use capabilities such
as video streaming and photo capture. Both repositories also say developers can
create organizations and release channels to share integrations with test users.

The iOS public agent instructions describe four modules:

- `MWDATCore`: device discovery, registration, permissions, and selectors.
- `MWDATCamera`: streams, video frames, and photo capture.
- `MWDATDisplay`: display UI components, images, buttons, icons, and video.
- `MWDATMockDevice`: local testing without physical glasses.

The Android public agent instructions describe equivalent modules:

- `mwdat-core`
- `mwdat-camera`
- `mwdat-display`
- `mwdat-mockdevice`

The important architectural point is that camera access and display access are
capabilities attached to a phone-app session with a linked device.

## Developer Mode and Registration

The public DAT guidance says local development requires Developer Mode enabled
in the Meta AI app for the specific glasses pair. The iOS instructions give
this path as `Meta AI app > Settings > Your glasses > Developer Mode`. The
Android instructions say Developer Mode is required for development builds that
use `APPLICATION_ID = 0`.

Registration and permissions are separate steps:

- Registration connects the developer app to Meta AI.
- Device permissions are requested after registration, such as camera access.
- Permission grants happen through the Meta AI companion app.
- Camera access can be granted temporarily or persistently.
- Production builds use a real application ID and release-channel gating through
  the Wearables Developer Center.

The developer documentation pages themselves were login-gated when checked, but
Meta's public GitHub repos expose enough setup detail to establish the workflow.

## iOS Development Path

For iOS, DAT is added through Swift Package Manager using:

```text
https://github.com/facebook/meta-wearables-dat-ios
```

The public iOS repo and instructions require a real iOS device with the Meta AI
app, supported glasses or MockDeviceKit, Developer Mode for local builds, URL
scheme callback handling, and `Wearables.configure()` at app launch. During
Developer Mode, Meta's public instructions say to use `MetaAppID` value `0`.

This means an iOS "sideload" path is really normal Apple developer-device
installation: build and run the phone app from Xcode, distribute by TestFlight,
or ship through the App Store after Meta release-channel setup. It is not an
APK-style direct install onto the glasses.

## Android Development Path

For Android, DAT is distributed through GitHub Packages. The public Android repo
says a GitHub personal access token with `read:packages` scope is needed, either
as `GITHUB_TOKEN` or as `github_token` in `local.properties`. It then uses the
GitHub Packages Maven repository:

```text
https://maven.pkg.github.com/facebook/meta-wearables-dat-android
```

The developer build can be installed on a physical Android phone through Android
Studio or ADB. The Android instructions again require the Meta AI companion app,
Developer Mode, registration callbacks, and Bluetooth/camera permissions.

Android Studio is primarily the build, install, configuration, and debugging
tool for this non-Play-Store developer app. The expected customization is in
VisionClaw or the local Android project: local secrets, model endpoints, Meta
DAT app/developer settings, frame cadence, and optional tool backend URLs. Do
not fork or edit Meta's DAT SDK unless a specific upstream SDK bug is confirmed.

Android is the closest thing to a familiar "sideload" path because a debug APK
can be installed locally, but it still runs on the phone and connects to the
glasses through Meta's companion-app and DAT permission model.

## Meta Ray-Ban Display Path

The Display glasses are different from ordinary Ray-Ban Meta because they have
a right-lens display and Neural Band input. Secondary reporting on Meta's May
2026 developer preview says Meta opened two build paths:

- native mobile apps using DAT display components; and
- web apps using HTML, CSS, and JavaScript.

Android Central reported that DAT provides display UI tools such as text,
images, lists, buttons, and video playback. The Verge reported that Meta opened
developer-preview app creation for Ray-Ban Display, including deployment of web
apps to the glasses. Tom's Hardware later covered a developer-built running web
app for Ray-Ban Display and reported that it ran directly on the device.

The safest wording is: ordinary Ray-Ban Meta integrations are phone-app
integrations; Meta Ray-Ban Display adds a developer-preview glasses app/web-app
surface.

## VisionClaw Relevance

VisionClaw uses the phone-app model. Its README says the app runs on iOS and
Android, pairs with Meta Ray-Ban glasses, streams the glasses camera to Gemini
Live at about one frame per second, and optionally routes tool calls to
OpenClaw. The paper says the system uses Meta Ray-Ban glasses, the Meta DAT SDK,
Gemini Live, and OpenClaw.

VisionClaw's setup instructions also describe enabling Developer Mode through
the Meta AI app before using glasses mode. Its iOS and Android apps can also
run in phone-camera mode without glasses, which is useful for testing the
Gemini/OpenClaw pipeline before relying on DAT hardware access.

## Security and Privacy Notes

This is the risk stack to keep visible:

- DAT access is gated by Meta AI registration, device permissions, Developer
  Mode, and production release channels.
- Meta's DAT public repos say Meta may collect information about how users'
  Meta devices communicate with the app unless analytics collection is opted
  out through platform-specific settings.
- VisionClaw-style systems add a second data plane: streamed egocentric
  camera/audio data to a model provider.
- OpenClaw-style execution adds a third data plane: a local or LAN-reachable
  gateway with access to apps, browsers, files, messaging, calendars, or other
  connected services.
- If OpenClaw is bound to LAN for a phone app, gateway token handling and
  network exposure become first-order security controls.
- Do not commit Gemini keys, GitHub package tokens, OpenClaw gateway tokens, or
  captured bystander footage to this public repo.

The bystander/privacy issue is not theoretical. Recent reporting says modified
Ray-Ban Meta glasses can disable the recording indicator light, and Meta told
TechRadar it removes violating ads/listings and pursues legal action when
appropriate. Separate recent reporting says Meta tested face-recognition
technology for smart glasses but removed the feature from test app builds after
press scrutiny. Those are adjacent to DAT development because any always-on or
agentic glasses prototype inherits the same public-trust problem.

## Practical Build Checklist

For a VisionClaw-style local experiment on Logan's Wayfarer Gen I pair:

1. Use phone-camera mode first, before involving glasses.
2. Keep secrets in local ignored files or a secret manager; do not add them to
   the vault.
3. Update Meta AI app and glasses firmware.
4. Enable Developer Mode for the specific glasses pair.
5. Register the app through Meta AI.
6. Request only the DAT permission needed for the test, usually camera.
7. Prefer the lowest useful frame rate and resolution; DAT frame quality is
   constrained by Bluetooth bandwidth.
8. If using OpenClaw from the phone, bind only as broadly as needed and require
   a strong gateway token.
9. Add an explicit visible UI state for "camera streaming active" and "agent
   execution active"; do not rely only on glasses-level cues.
10. Ignore Ray-Ban Display web-app and display-UI instructions for this pair;
    they are for different hardware.

## Open Questions

- Whether the goal is a VisionClaw build, a simpler DAT camera-streaming proof,
  or a custom DAT camera-streaming proof.
- Whether the app needs production release-channel distribution or only local
  developer-device testing.
- Whether the OpenClaw gateway should be reachable only on trusted Wi-Fi or
  through a more controlled tunnel.

## Sources

- Meta Wearables DAT iOS repository, public README and AGENTS guidance:
  <https://github.com/facebook/meta-wearables-dat-ios> and
  <https://raw.githubusercontent.com/facebook/meta-wearables-dat-ios/main/AGENTS.md>
- Meta Wearables DAT Android repository, public README and AGENTS guidance:
  <https://github.com/facebook/meta-wearables-dat-android> and
  <https://raw.githubusercontent.com/facebook/meta-wearables-dat-android/main/AGENTS.md>
- VisionClaw repository:
  <https://github.com/Intent-Lab/VisionClaw>
- VisionClaw paper:
  <https://arxiv.org/abs/2604.03486>
- Android Central, "Meta's Ray-Ban Display build for the future, opens its
  doors to developers," 2026-05-15:
  <https://www.androidcentral.com/gaming/virtual-reality/metas-ray-ban-display-build-for-the-future-opens-its-doors-to-developers>
- The Verge, "Meta brings virtual writing to everyone with Meta Ray-Ban Display
  glasses," 2026-05-14:
  <https://www.theverge.com/tech/930941/meta-ray-ban-display-virtual-neural-handwriting-apps-developer>
- Tom's Hardware, "Resourceful runner 'can race my own ghost' using homemade
  Meta Ray-Ban Display app," 2026-06-01:
  <https://www.tomshardware.com/peripherals/wearable-tech/resourceful-runner-can-race-my-own-ghost-using-homemade-meta-ray-ban-display-app-also-adds-bonus-coins-mini-leaderboard-and-more>
- TechRadar, "Modders are turning Meta Ray-Bans into spy glasses," 2026-06-12:
  <https://www.techradar.com/computing/virtual-reality-augmented-reality/modders-are-turning-meta-ray-bans-into-spy-glasses-its-not-cool-its-creepy-and-i-hate-it>
- Wired, "Meta Tapped a Pentagon Supplier to Prototype Face Recognition for Its
  Glasses," 2026-06-16:
  <https://www.wired.com/story/meta-rank-one-computing-face-recognition-smart-glasses>
