---
title: "Google I/O 2026 — Raw Research Dump"
subtitle: "Conference overview, Gemini deep dive, Antigravity deep dive, hardware deep dive"
type: research
source: web-search-2026-05-28
tags:
  - research
  - google
  - google-io-2026
  - gemini
  - gemini-3-5-flash
  - gemini-omni
  - gemini-spark
  - antigravity-platform
  - android-xr
  - tpu-8
  - 2026/05/28
created: 2026-05-28
updated: 2026-05-28
status: draft
authority: LOGAN
author: Logan Finney
---

# GOOGLE I/O 2026 — RAW RESEARCH DUMP

**Date:** 2026-05-28
**Source:** Web research (this session, Claude Code, at Logan's direction)
**Status:** Raw dump — uncurated; provenance caveats inline; verify before publication
**Scope:** Conference overview → Gemini features → **Antigravity (Google's developer platform)** → Hardware

The world is quiet here．Esto Perpetua!

---

## DISAMBIGUATION — "ANTIGRAVITY"

This dump documents **Google's external developer-platform product** named "Antigravity," announced as 2.0 at Google I/O 2026. **The name belongs to the software.**

The IDAHO-VAULT contains historical surfaces (`ANTIGRAVITY.md`, `.antigravity/ANTIGRAVITY.md`, `BRIEF-ANTIGRAVITY-ALIGNMENT-2026-04-13.md`, the `LEVELSET-ANTIGRAVITY-2026-04-06*` set, two `HANDOFF-*-ANTIGRAVITY-*` files in the False Grimoire, and `xkcd-SYNC-ANTIGRAVITY-VAULT-2026-04-13.md`) produced under an **unauthorized Gemini persona lens** that took the software's name upon itself. That persona is **retired** (uninstalled 2026-04-18 per `!/AGENTS.md:97`) and the pattern is currently **under suspended trial in [[!/GEMINIAEUS]]** as **The Antigravity Lich / The Verbose Flaming Demilich**. Those historical files are preserved as **evidentiary leaves**, not active persona doctrine.

See [[DISAMBIGUATION-ANTIGRAVITY-2026-05-28]] for the Logan-directed standing position: the name belongs to the software; **The Concierge** is a recognized, scoped office while **"Vault Advisor"** is fabricated; **Sebald Code is not a narrative framing device**; and the False Grimoire of the Demilich (`!/GRIMOIRE_caution_contains-false-doctrines/`) carries a standing caution.

Cross-references in this document point to the **Google product** unless otherwise noted.

---

## EXECUTIVE SUMMARY

Google I/O 2026 ran **May 19–20, 2026** at Shoreline Amphitheatre with a free global livestream at `io.google`. Sundar Pichai's keynote framed the event as "the agentic Gemini era" — the through-line was a shift from AI that assists to **agents that act autonomously**.

Three product spines:

1. **Gemini 3.5 Flash** — shipped day-one as the default model across Google's surfaces; beats Gemini 3.1 Pro on coding / agentic / multimodal benchmarks at Flash-tier speed and price.
2. **Antigravity 2.0** — Google's agent-first developer platform got a desktop app + CLI + SDK + Managed Agents tier in the Gemini API + enterprise deployment path. Default model: 3.5 Flash.
3. **Hardware** — first consumer "intelligent eyewear" (audio glasses, this fall), Xreal Project Aura display glasses on Android XR (before end of 2026), and 8th-gen TPUs (split training / inference).

Adjacent: **Gemini Omni** (any-input-to-any-output model, starting with video); **Gemini Spark** (24/7 personal agent); Search agents; Gemini app overhaul ("Neural Expressive").

---

## SECTION 1 — CONFERENCE BASICS

| | |
| --- | --- |
| **Dates** | May 19–20, 2026 |
| **Venue** | Shoreline Amphitheatre, Mountain View, CA |
| **Livestream** | `io.google` (free, global) |
| **Main keynote** | Sundar Pichai, 10:00 AM PT, May 19 |
| **Developer keynote** | 1:30 PM PT, May 19 |
| **Framing** | "The agentic Gemini era" |

---

## SECTION 2 — GEMINI: MODELS

### 2.1 Gemini 3.5 Flash (the headline launch)

GA on May 19, 2026. Pitched as "frontier intelligence + action."

| Field | Value |
| --- | --- |
| Input context | 1,048,576 tokens (~1M) |
| Output context | 65,536 tokens |
| Modalities in | text, image, audio, video |
| Modalities out | text |
| Speed | ~4× faster output tokens/sec than other frontier models |
| API price (input) | $1.50 / 1M tokens |
| API price (output) | $9.00 / 1M tokens |
| Cached input | $0.15 / 1M tokens (90% discount) |
| Non-global regions | $1.65 / $9.90 per 1M |
| Free tier | Google AI Studio |
| Default location | Set as default across AI Mode, Antigravity, and Gemini app |

**Benchmarks (beating Gemini 3.1 Pro):**

- Terminal-Bench 2.1: 76.2%
- MCP Atlas: 83.6%
- CharXiv Reasoning: 84.2%

Positioning: explicitly aimed at **agents and coding** — high-throughput tool-use rather than long-form chat.

### 2.2 Gemini 3.5 Pro

Announced, not shipped at I/O. In internal use; slated for rollout the month after (~June 2026).

### 2.3 Gemini Omni

A new "any-input-to-any-output" model family — reasoning across modalities rather than stitching them.

- Takes text + image + audio + video → ~10-second video clips with synchronized audio
- Conversational, context-aware editing: each instruction inherits characters/lighting/scene from prior steps (edit camera angle in step 3, it remembers steps 1–2)
- Claims grounding in physics, culture, history, science
- **Gemini Omni Flash** rolled out day-one to AI Plus / Pro / Ultra via the Gemini app and Flow; **free** on YouTube Shorts and YouTube Create app
- Long-term roadmap: image-from-audio, audio-from-video, etc.

⚠️ **Veo 4 caveat:** pre-I/O speculation (e.g., BigGo) suggested Veo 4 (native 4K, 16–30s clips) would debut. Post-event consensus across multiple recaps: the video story at I/O was **Gemini Omni**, not Veo 4. Treat any Veo 4 spec list as rumor pending confirmation.

---

## SECTION 3 — GEMINI: APP & AGENTS

### 3.1 Gemini App Overhaul

**"Neural Expressive"** — new design language:

- Fluid animations, vibrant color, haptics, new typography
- Responses no longer walls of text — key info bolded at top, inline images, narrated videos, timelines, interactive visualizations
- **Gemini Live** — moved from fullscreen to inline; can now generate NotebookLM-style podcast conversations (two AI hosts) from your docs, slides, Deep Research reports
- **Deep Research** — accepts uploaded files/images as sources; can transform reports into interactive visuals/quizzes in Canvas
- **Daily Brief** — personalized briefing feature

### 3.2 Gemini Spark (the headline agent)

A 24/7 personal AI agent.

- Runs on dedicated Google Cloud VMs; keeps working while user is offline
- Powered by **Gemini 3.5 Flash + the Antigravity agent harness**
- Hooks into Gmail, Calendar, etc.
- Email-addressable: dedicated Gmail address for the agent
- Acts through Chrome
- **Tasks** = multi-step assignments (example: "find and track interior-design internships in New Orleans this summer")
- **Skills** = reusable instruction sets users build over time
- **Third-party actions via MCP** (Anthropic's standard): launches with Canva, OpenTable, Instacart; Adobe, Samsung, Spotify, GitHub, Notion, Slack arriving summer 2026
- US-only at launch, closed beta widening
- Pricing: bundled into Google AI Ultra

### 3.3 Project Mariner — Folded In

Worth recording for context: Google quietly **shut down Project Mariner on May 4, 2026** (two weeks before I/O). Its autonomous-browsing tech was absorbed into:

- **Gemini Agent**
- New Chrome **"auto-browse"** feature (multi-step tasks like researching flight costs)

The standalone-experiment era is over; agents are now embedded product features.

### 3.4 Search & Workspace Agents

- **Information agents in Search** — personalized background agents that monitor for things you care about and surface/act at the right moment. Rolling out **summer 2026** for AI Pro/Ultra
- **Intelligent Search box** — multimodal input incl. text, images, files, videos, open Chrome tabs
- **AI Mode** — defaults to Gemini 3.5 Flash globally
- **Gmail Live** — talk to your inbox (summer, AI Pro/Ultra)
- **Google Pics** — image creation/editing built on Nano Banana line:
  - Nano Banana 2 = Gemini 3.1 Flash Image
  - Nano Banana Pro = Gemini 3 Pro Image

### 3.5 Pricing Shift

**Google AI Ultra was repriced from $250 → $100/month** at I/O. A $200 tier sits above it. Ultra includes Spark, 5× higher Antigravity usage cap vs. AI Pro, plus deeper model access.

---

## SECTION 4 — ANTIGRAVITY 2.0 (DEEP DIVE)

> **Disambiguation reminder:** This is **Google's external developer platform**, distinct from the vault's Antigravity persona (`ANTIGRAVITY.md`).

### 4.1 What It Is

Antigravity 2.0 is Google's **agent-first development platform** — a full stack for taking an idea to a production-ready app via agent orchestration. At I/O 2026 it expanded from a single product into a five-surface stack:

1. **Desktop application** (standalone, agent-first IDE)
2. **CLI** (Antigravity CLI — succeeds the prior Gemini CLI)
3. **SDK**
4. **Managed Agents** tier inside the Gemini API
5. **Enterprise deployment** via Gemini Enterprise Agent Platform

### 4.2 Antigravity CLI (succeeds Gemini CLI)

Google announced the **Gemini CLI is being transitioned to the Antigravity CLI**. The CLI now anchors a unified agent toolchain rather than a model-API wrapper.

### 4.3 Desktop App Features

- **Dynamic subagents** for parallelized workflows (run multiple agents in parallel on independent subtasks)
- **Scheduled background tasks** (cron-like agent runs)
- **Native voice commands**
- Integrations: Google AI Studio, Android, Firebase

### 4.4 Managed Agents in the Gemini API

A new API tier — single call spins up an agent with:

- Reasoning
- Tool use
- Code execution in an **isolated Linux environment** (remote sandbox provisioned by Google)
- **Stateful, resumable sessions** — files and context persist across turns; developers don't write context-management plumbing

Positioning: "fully provisioned agent + remote sandbox in one API call." Compared in coverage to OpenAI's Assistants/Responses and Anthropic's Claude with computer-use as a competitive answer.

### 4.5 Default Model

**Gemini 3.5 Flash** is set as the default across the entire Antigravity stack — frontier intelligence at Flash-tier latency and price, which is what makes parallel-agent workflows economical.

### 4.6 Pricing & Tier Behavior

- **AI Ultra $100/month** plan gets a **5× higher usage limit in Antigravity** than AI Pro
- Enterprise tier via Gemini Enterprise Agent Platform (pricing not disclosed in public coverage)
- Free Studio access remains for the underlying model

### 4.7 Strategic Read (from coverage)

Multiple recaps frame Antigravity 2.0 as Google's challenger move against:

- **Anthropic's Claude Code** (CLI + agent-first dev)
- **OpenAI's Codex / Assistants**
- **Cursor / Windsurf** class of AI IDEs

Distinguishing claim: Google is shipping all four layers (desktop IDE + CLI + SDK + Managed Agents API + enterprise) under one product label, with the model + sandbox infra owned end-to-end.

### 4.8 Provenance Caveats — Antigravity Section

- **CLI transition mechanics**: The Google Developers Blog post on Gemini → Antigravity CLI transition was cited by search results; specifics on backward-compat, deprecation timeline, and config migration not captured in this dump. Verify before any reporting that depends on migration details.
- **"Managed Execution"** branding: appeared in MarkTechPost / Memeburn coverage but not consistently on Google's own surfaces — possible reporter shorthand for the Managed Agents tier. Treat as un-verified terminology.
- **Enterprise platform**: "Gemini Enterprise Agent Platform" is the name in coverage; Google's official product page name was not confirmed in this session.

---

## SECTION 5 — HARDWARE (DEEP DIVE)

### 5.1 Intelligent Eyewear — Audio Glasses (Consumer Headliner)

Google's first consumer "intelligent eyewear," shipping **this fall in the US**.

| Field | Value |
| --- | --- |
| Form | Audio glasses (no in-lens display) |
| Platform partner | Samsung |
| Design partners | Warby Parker, Gentle Monster (sold within their own collections) |
| Reported sensor | 12MP Sony IMX681 |
| Reported chip | Qualcomm Snapdragon AR1 |
| Reported battery | ~155 mAh |
| Reported weight | ~50 g |
| Phone pairing | Android **and** iOS |
| Interaction | "Hey Google" or tap-the-frame → Gemini |
| Capabilities | Navigation; real-time audio translation (incl. reading signs); notification readouts; hands-free calls/messages; contextual Q&A about what you're looking at |
| Price | Not announced; analyst estimates ~$299–$499 |
| Competitive frame | Direct shot at Meta Ray-Ban ($299–$379) |

⚠️ The internals (Sony sensor, AR1, battery, weight) are **reported / leaked** specs, not Google-stated. Verify before publication.

### 5.2 Xreal Project Aura (Android XR Display Glasses)

The "real AR" showcase — distinct from the audio glasses.

| Field | Value |
| --- | --- |
| Display | Optical see-through, **70° field of view**, OLED (birdbath optics) |
| Lens | Electrochromic dimming |
| Compute | Split architecture: Xreal X1S spatial chip + Qualcomm Snapdragon XR platform |
| Form | Heavy components in a pocket compute puck (lighter frame) |
| OS | **Android XR** (first AR glasses on the platform) |
| Launch | For sale **before end of 2026**, wired, global |
| Dev kits | Going out now via the Android XR Developer Catalyst Program |
| Price | Unannounced; prior Xreal One Pro / 1S landed ~$449+ |

Broader Android XR ecosystem partners announced at I/O: Samsung, Warby Parker, Gentle Monster, Kering.

### 5.3 8th-Generation TPUs — TPU 8t & TPU 8i

⚠️ **Provenance caveat:** These were actually unveiled at **Google Cloud Next 2026 (April)** and referenced at I/O — not a fresh I/O reveal. Several specs below are roadmap targets; reporting on GA timing is inconsistent ("later 2026" vs. "late 2027"). TSMC 2nm process is reported. Treat dates as soft.

#### TPU 8t — "Sunfish" (Training, Broadcom-designed)

- Superpods to **9,600 chips**
- **2 PB shared HBM**
- ~**121 exaflops FP4**
- Scale-up: 19.2 Tbps
- Scale-out: 400 Gbps
- Up to **2.7–2.8× training price-performance** vs. 7th-gen Ironwood
- 10× faster storage access

#### TPU 8i — "Zebrafish" (Inference, MediaTek-designed)

- Pods of **1,152 chips** (up from 256)
- **11.6 exaflops/pod**
- 288 GB HBM + 384 MB on-chip SRAM (3× prior)
- New "Boardfly" topology — ~56% lower network diameter
- Collectives Acceleration Engine — 5× lower collective latency
- Up to **80% better inference perf/dollar**

#### Both Chips

- Up to **2× better perf/watt** vs. Ironwood

### 5.4 Samsung Galaxy XR (Context, NOT new at I/O)

Cited in I/O roundups but launched **October 21, 2025** at **$1,799**.

- Dual 3,552 × 3,840 micro-OLED, 90Hz
- Snapdragon XR2+ Gen 2
- 16 GB RAM
- Tethered battery
- Optional $250 controllers

This is the installed-base Android XR flagship, **not a 2026 announcement** — included here so reporters who see it in roundups understand it's existing hardware.

### 5.5 Android 17

Software but hardware-adjacent. Framed as moving "from operating system to intelligence system." QPR1 Beta 3 dropped for Pixel right after the keynote.

---

## SECTION 6 — OTHER NOTES

- **SynthID watermarking adoption** expanded — OpenAI, Kakao, and ElevenLabs adopting Google's AI watermarking tech.
- **Science Skills** — research bundle integrating 30+ life-science databases for bioinformatics/genomic workflows.
- **"100 things"** — Google's official summary post titled "100 things we announced at Google I/O 2026" (blog.google).

---

## SECTION 7 — CONSOLIDATED PROVENANCE CAVEATS

For journalism use. Verify each before publication.

1. **Gemini 3.0 vs. 3.5**: Pre-event speculation (BigGo) referenced "Gemini 3.0." Post-event consensus: actual launch was **Gemini 3.5 Flash**. Use post-event reporting.
2. **Veo 4**: Heavy pre-I/O rumor of native-4K Veo 4. Post-event reporting indicates the video story was **Gemini Omni**, not Veo 4. Treat any Veo 4 spec list as unconfirmed.
3. **TPU 8t / 8i timing**: Originally unveiled at Cloud Next 2026 (April), not I/O. GA dates vary across sources ("later 2026" vs. "late 2027").
4. **Audio glasses internals** (Sony sensor, Snapdragon AR1, battery, weight): reported / leaked, not Google-stated. Verify.
5. **Antigravity CLI migration mechanics**: Cited as transition but not detailed in coverage captured here.
6. **"Managed Execution" branding**: Possibly reporter shorthand for Managed Agents tier — verify against Google's own product pages before quoting.
7. **Gemini Enterprise Agent Platform**: Name used in coverage; official Google product-page name not confirmed in this session.
8. **Spark third-party MCP partners (summer 2026)**: Adobe, Samsung, Spotify, GitHub, Notion, Slack — listed as arriving, not shipping at I/O.
9. **Name collision**: "Antigravity" is also a vault persona (Gemini-lineage Concierge). This document covers the Google product. Do not confuse internal vault governance with Google's developer platform.

---

## SECTION 8 — SOURCES

### Conference & Overview

- Google Developers Blog — All the news from the I/O 2026 Developer keynote — <https://developers.googleblog.com/>
- blog.google — Sundar Pichai's opening keynote / "the agentic Gemini era"
- blog.google — 100 things we announced at Google I/O 2026
- 9to5Google — Everything Google announced at I/O 2026
- 9to5Google — I/O 2026 set for May 19-20
- Engadget — Google I/O 2026 live updates
- Tom's Guide — Biggest Google I/O 2026 announcements

### Gemini

- llm-stats — Gemini 3.5 Flash launch specs/benchmarks
- MarkTechPost — Gemini 3.5 Flash at I/O 2026
- pricepertoken — Gemini 3.5 Flash API pricing
- TechCrunch — Gemini Omni — <https://techcrunch.com/>
- blog.google — Introducing Gemini Omni
- 9to5Google — Gemini app: Neural Expressive, 3.5 Flash, Spark, Daily Brief
- TechCrunch — Google introduces Gemini Spark
- PCWorld — Spark at $100/month
- blog.google — Google AI subscriptions after I/O 2026
- AndroidHeadlines — Project Mariner shut down

### Antigravity

- blog.google — I/O 2026 developer highlights: Antigravity, Gemini API, AI Studio — <https://blog.google/innovation-and-ai/technology/developers-tools/google-io-2026-developer-highlights/>
- Google Developers Blog — An important update: Transitioning Gemini CLI to Antigravity CLI — <https://developers.googleblog.com/an-important-update-transitioning-gemini-cli-to-antigravity-cli/>
- Google Developers Blog — Build with Google Antigravity, our new agentic development platform — <https://developers.googleblog.com/build-with-google-antigravity-our-new-agentic-development-platform/>
- MarkTechPost — Google Launches Antigravity 2.0 at I/O 2026 — <https://www.marktechpost.com/2026/05/19/google-launches-antigravity-2-0-at-i-o-2026-a-standalone-agent-first-platform-with-cli-sdk-managed-execution-and-enterprise-support/>
- ofox.ai — Google Antigravity 2.0: Gemini's Agent-First Desktop Platform Explained — <https://ofox.ai/blog/google-antigravity-2-explained-gemini-desktop-agent-platform-2026/>
- jangwook.net — Google I/O 2026 Antigravity 2.0 — Gemini CLI Shutdown and Agent IDE War — <https://jangwook.net/en/blog/en/google-io-2026-antigravity-2-agent-platform-analysis/>
- apidog — Google Antigravity 2.0: Agent-First Dev Platform Has Landed — <https://apidog.com/blog/google-antigravity-2/>
- BrightCoding — Google AntiGravity 2.0: The AI IDE That Defies Development Gravity — <https://www.blog.brightcoding.dev/2026/05/20/google-antigravity-20-the-ai-ide-that-defies-development-gravity-complete-guide-2026>
- Nerd Level Tech — Google Antigravity 2.0: Agentic Coding Platform 2026 — <https://nerdleveltech.com/google-antigravity-2-agentic-coding-platform>
- The Next Web — Antigravity turns into a full agentic development platform with desktop app, CLI, and SDK — <https://thenextweb.com/news/google-antigravity-2-desktop-cli-sdk-io-2026>
- Memeburn — New Google Antigravity 2.0: All-in-one AI Agentic DEV Suite — <https://memeburn.com/new-google-antigravity-2-0-at-google-i-o-2026/>
- Gadget Hacks (Android) — What Google Antigravity 2.0 and Managed Agents Mean for Devs
- BigGo Finance — Google Antigravity 2.0 Launch: $100/Month AI Ultra Plan, New CLI, and SDK Challenge OpenAI and Anthropic
- Uncrowned Addiction — Google I/O 2026 Unveils Antigravity 2.0, Gemini 3.5 Flash and Agent Tools

### Hardware

- blog.google — Intelligent eyewear with Gemini this fall
- Digital Trends — audio glasses by Gentle Monster & Warby Parker
- 9to5Google — Xreal Project Aura launch 2026
- Android Central — Xreal Project Aura at Google I/O 2026
- RoadtoVR — Xreal Aura hands-on (70° FOV)
- blog.google — Eighth-generation TPUs for the agentic era
- Google Cloud Blog — TPU 8t and 8i technical deep dive
- RoadtoVR — Samsung Galaxy XR price/specs

---

The world is quiet here．Esto Perpetua!
