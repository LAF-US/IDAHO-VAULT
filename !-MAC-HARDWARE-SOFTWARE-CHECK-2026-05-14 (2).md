---
title: "Mac Hardware and Software Check - 2026-05-14"
authority: Codex
date created: 2026-05-14
status: current
related:
  - "[[!-MAC-SETUP-STATUS-2026-04-26]]"
  - "[[OPENROUTER-MESH-2026-04-24]]"
  - openclaw
  - ollama
  - OpenRouter
---

# Mac Hardware and Software Check - 2026-05-14

## Context

This note records the current hardware and software constraints for Logan's Mac
OpenClaw setup. It supersedes the inline 2026-05-14 hardware/runtime additions
that were briefly placed in [[!-MAC-SETUP-STATUS-2026-04-26]].

## Hardware

- **Machine:** Early 2015 MacBook Pro
- **Model identifier:** MacBookPro12,1
- **OS:** macOS 12.7.6 Monterey, Darwin 21.6.0, x86_64
- **CPU:** Intel Core i7 3.1 GHz, 2 cores / 4 threads
- **RAM:** 16 GB DDR3 1867 MHz, not upgradeable
- **GPU:** Intel Iris Graphics 6100, integrated, 1536 MB dynamic VRAM
- **Internal storage:** 1 TB APFS SSD, about 97 GiB free on 2026-05-14
- **Data volume:** about 90% used on 2026-05-14
- **SMART status:** Verified

## Runtime Versions

- **OpenClaw:** 2026.5.7
- **Node:** v24.15.0
- **npm:** 11.12.1
- **Python:** 3.13.7
- **Homebrew:** 5.1.11
- **Ollama client:** 0.21.2
- **Xcode:** 14.2
- **Apple clang:** 14.0.0
- **Git:** 2.45.2

## OpenClaw Routing Constraint

Active OpenClaw routing should remain hosted and follow Logan's preferred family
order:

1. Mistral
2. Claude
3. ChatGPT/OpenAI

Current active model routing is recorded in [[OPENROUTER-MESH-2026-04-24]].

## Local Model Findings

- Local Ollama remains installed, but no local Ollama model is active in OpenClaw routing.
- `codestral:latest` was tested and removed from active routing because it did not return promptly on this Mac.
- `devstral:latest` was tested and removed from active routing because it did not return promptly on this Mac.
- Larger local models are not practical active OpenClaw routes on this hardware.
- `phi3:mini`, Qwen, and Gemma are excluded by preference.
- Gemini is banned from active routing.

## Constraint Summary

This Mac can run OpenClaw, Node tooling, and the local gateway reliably. It is
not a good active local LLM host for OpenClaw. The limiting factors are the
Intel dual-core CPU, 16 GB shared memory, integrated graphics, high live system
load, and limited free disk headroom for large model artifacts.

The practical setup is cloud-first OpenRouter routing with local Ollama treated
as installed model storage, not as an active OpenClaw runtime path.

## Links

- Historical Mac setup snapshot: [[!-MAC-SETUP-STATUS-2026-04-26]]
- Current OpenRouter/OpenClaw mesh: [[OPENROUTER-MESH-2026-04-24]]
