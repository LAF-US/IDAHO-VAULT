---
title: "NOUS RESEARCH & HERMES AGENT"
subtitle: "Deep Research Report"
type: research
source: web-search-2026-04-28
tags:
- nous-research
- hermes-agent
- hermes-4
- psyche-network
- distributed-training
- open-source-ai
- autonomous-agents
created: 2026-04-28
author: Logan Finney
---

# NOUS RESEARCH & HERMES AGENT
## Deep Research Report

**Date:** April 28, 2026  
**Source:** Web research via Hermes Agent (this session)  
**Status:** Active research — Living document

---

## EXECUTIVE SUMMARY

**Nous Research** is a leader in the American open source AI movement. They train world-class open source language models and build infrastructure to coordinate distributed, unbiased training. Hermes Agent is their flagship autonomous AI agent product.

> *The world is quiet here.*

---

## NOUS RESEARCH ORGANIZATION

### Mission

> "Our mission is to advance human rights and freedoms by creating and proliferating open source language models, supporting their unrestricted availability and use, and furthering their scientific and popular understanding."

### Primary Focus Areas

- Model architecture
- Data synthesis
- Fine-tuning
- Reasoning

### Location

- **Website:** nousresearch.com
- **GitHub:** github.com/nousresearch (77 repos, 3,528 followers)
- **HuggingFace:** 126 models released

---

## PROJECT CATALOG

### Core Products

| Project | Type | Description |
|---------|------|-------------|
| **Hermes Agent** | AGENT | Autonomous agent that grows with use |
| **Hermes Models** | MODEL | Open source language model series |
| **Psyche Network** | TRAINING | Decentralized training infrastructure |
| **DisTrO** | FRAMEWORK | Low-bandwidth distributed training |
| **Atropos** | FRAMEWORK | RL training environments |
| **Nomos** | MODEL | Specialized mathematical reasoning |
| **Consilience 40B** | MODEL | Largest distributed training run ever |

---

## HERMES MODEL FAMILY

### Hermes 4 (August 2025)

| Model | Size | Notes |
|-------|------|-------|
| Hermes-4-Llama-3.1-405B | 802 GB | Frontier hybrid-mode reasoning |
| Hermes-4-Llama-3.1-70B | 140 GB | Same improvements, smaller footprint |
| Hermes-4.3-Seed-36B | 72 GB | **Post-trained entirely on Psyche network** |
| Hermes-4-14B | 28 GB | Dense, local-friendly |

> Hermes-4.3-Seed-36B achieves roughly equivalent performance to Hermes-4-70B at half the model size.

### Hermes 3 (August 2024)

- Hermes 3 405B — 812 GB
- Hermes 3 70B
- Hermes 3 Dataset (full pretraining corpus released publicly)

### Hermes 2 (2024)

- Hermes-2-Pro-Mistral-7B — Master function-calling model
- Hermes-2-Pro-Llama-3-8B
- Hermes-2-Mixtral-8x7B (SFT + DPO variants)
- Hermes-2-Yi-34B

### Hermes 1 (2023)

- Nous-Hermes-Llama2-13B
- Nous-Hermes-2-Mistral-7B-DPO

---

## HERMES AGENT

### What It Is

> *"Not a coding copilot tethered to an IDE or a chatbot wrapper around a single API. An autonomous agent that gets more capable the longer it runs."*

### Key Differentiators

| Feature | Description |
|---------|-------------|
| **Self-improving** | Creates skills from experience, persists knowledge |
| **Persistent Memory** | Cross-session memory, user profiling |
| **47 Built-in Tools** | Web, terminal, file, vision, delegation, cron |
| **MCP Integration** | Connect any MCP server |
| **15+ Platforms** | CLI, Telegram, Discord, Slack, WhatsApp, Signal, etc. |
| **Voice Mode** | Free STT via local faster-whisper |
| **6 Terminal Backends** | Local, Docker, SSH, Daytona, Modal, Singularity |
| **Cron Scheduling** | Natural language scheduling with platform delivery |

### Supported Providers (20+)

| Provider | Auth | Key Env Var |
|----------|------|-------------|
| OpenRouter | API key | `OPENROUTER_API_KEY` |
| Anthropic | API key | `ANTHROPIC_API_KEY` |
| Nous Portal | OAuth | `hermes auth` |
| OpenAI Codex | OAuth | `hermes auth` |
| Google Gemini | API key | `GOOGLE_API_KEY` |
| DeepSeek | API key | `DEEPSEEK_API_KEY` |
| xAI / Grok | API key | `XAI_API_KEY` |
| Hugging Face | Token | `HF_TOKEN` |
| Local Ollama | Config | `OLLAMA_HOST` |
| Custom endpoint | Config | Any OpenAI-format endpoint |

### Installation

```bash
curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash
source ~/.bashrc  # or ~/.zshrc
hermes             # start chatting!
```

### Key Commands

| Command | Purpose |
|---------|---------|
| `hermes` | Interactive CLI |
| `hermes model` | Choose provider/model |
| `hermes tools` | Configure toolsets |
| `hermes setup` | Full setup wizard |
| `hermes gateway` | Messaging platform gateway |
| `hermes doctor` | Diagnose issues |
| `hermes skills` | Browse/install skills |
| `hermes cron` | Schedule tasks |

### GitHub Stats

- **Stars:** 117,614+
- **License:** MIT
- **Latest:** v0.11.0 (April 23, 2026)

---

## PSYCHE NETWORK

### The Big Deal

Psyche is **open infrastructure democratizing AI development** by decentralizing training across underutilized hardware worldwide.

> *"Rather than requiring massive infrastructure with thousands of accelerators in a single location, Psyche coordinates training across distributed, heterogeneous hardware worldwide."*

### How It Works

1. **DisTrO Optimizer** — Reduces gradient communication by 3-4 orders of magnitude using DCT (Discrete Cosine Transform) — the same math as JPEG compression
2. **P2P Networking** — Uses Iroh for 90% direct UDP connections via hole-punching
3. **Solana Blockchain** — Coordinates training runs on-chain for fault tolerance

### Technical Innovation: DisTrO

> *"In large setups, thousands of accelerators compute and share gradients among the entire network. DisTrO is a family of optimizers that leverages unexpected properties of ML training to massively compress the information passed among accelerators."*

**The JPEG analogy:**
- Natural signals (images, sounds) have most information in low frequencies
- High frequencies can be discarded with minimal quality loss
- DisTrO applies DCT to optimizer momentum tensors, extracting top-k components
- Result: 3x+ bandwidth reduction via sign-only quantization

### Consilience 40B

**First production run on Psyche — largest distributed pretraining run ever over internet:**

| Spec | Value |
|------|-------|
| Parameters | 40B |
| Architecture | MLA (Multi-head Latent Attention) |
| Tokens | 20T |
| Dataset | FineWeb (14T) + FineWeb-2 (4T) + The Stack V2 (1T) |
| Trainable | Single H100/DGX |
| Runnable | Single RTX 3090 |

> *MLA is strictly more expressive than GQA (Llama architecture) — can fully represent GQA while GQA cannot represent MLA.*

---

## RELEVANT REPOSITORIES

| Repo | Stars | Description |
|------|-------|-------------|
| NousResearch/hermes-agent | 117k | The agent that grows with you |
| NousResearch/hermes-agent-self-evolution | 2.2k | Self-improvement via DSPy + GEPA |
| NousResearch/DisTrO | 1k | Distributed Training Over-The-Internet |
| NousResearch/atropos | 1.1k | RL Environments framework |
| NousResearch/hermes-paperclip-adapter | 982 | Paperclip company simulator |
| PsycheFoundation/psyche | 724 | Distributed training infrastructure |

---

## LOCAL OLLAMA SETUP FOR HERMES

### Current Local Models

| Model | Size | Purpose |
|-------|------|---------|
| qwen3.5:latest | 6.6 GB | General purpose, best quality |
| phi3:mini | 2.2 GB | Lightweight tasks |
| qwen2.5:3b | 1.9 GB | Minimal/quick tasks |
| devstral | ~14 GB | *(downloading)* Code understanding |
| codestral | ~14 GB | *(pending)* Code generation |
| mistral-large | ~14 GB | *(pending)* Complex reasoning |

### Hermes Config Update (Completed)

Primary provider set to `ollama-local` with `qwen3.5:latest` as default.

Fallback chain: Ollama Light → OpenRouter Free (Llama 3.2 3B)

---

## RESOURCES & LINKS

| Resource | URL |
|----------|-----|
| Hermes Agent Docs | hermes-agent.nousresearch.com/docs |
| Hermes GitHub | github.com/NousResearch/hermes-agent |
| Nous Research | nousresearch.com |
| Psyche Network | psyche.network |
| Psyche Docs | docs.psyche.network |
| Nous Discord | discord.gg/nous-ai |
| HuggingFace | huggingface.co/NousResearch |

---

## NOTES

- Hermes Agent compatible with Claude Code, Codex (OpenAI), and OpenClaw skill formats
- Skills follow agentskills.io open standard — portable and community-shareable
- Voice mode supports: Edge TTS (free), ElevenLabs, OpenAI, MiniMax, Mistral Voxtral
- STT supports: Local faster-whisper (free), Groq Whisper (free tier), OpenAI, Mistral

---

*Research conducted via Hermes Agent session — April 28, 2026*
