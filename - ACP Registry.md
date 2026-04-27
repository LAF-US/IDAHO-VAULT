---
title: "ACP Registry"
source: "https://agentclientprotocol.com/get-started/registry"
author:
published:
created: 2026-04-26
description: "The easiest way to find and install ACP-compatible agents."
---
## Overview

The ACP Registry is an easy way for developers to distribute their ACP-compatible agents to any client that speaks the protocol.

This is a curated set of agents, including only the ones that [support authentication](https://agentclientprotocol.com/rfds/auth-methods).

Visit [the registry repository on GitHub](https://github.com/agentclientprotocol/registry) to learn more about it.

## Available Agents

## [Amp](https://github.com/tao12345666333/amp-acp)

ACP wrapper for Amp - the frontier coding agent

**0.7.0**,

## [Auggie CLI](https://www.augmentcode.com/)

Augment Code’s powerful software agent, backed by industry-leading context engine

**0.24.0**,

## [Autohand Code](https://www.autohand.ai/cli/)

Autohand Code - AI coding agent powered by Autohand AI

**0.2.1**,

## [Claude Agent](https://github.com/agentclientprotocol/claude-agent-acp)

ACP wrapper for Anthropic’s Claude

**0.31.0**,

## [Cline](https://cline.bot/cli)

Autonomous coding agent CLI - capable of creating/editing files, running commands, using the browser, and more

**2.17.0**,

## [Codebuddy Code](https://www.codebuddy.cn/cli/)

Tencent Cloud’s official intelligent coding tool

**2.93.6**

## [Codex CLI](https://github.com/zed-industries/codex-acp)

ACP adapter for OpenAI’s coding assistant

**0.12.0**,

## [Corust Agent](https://corust.ai/)

Co-building with a seasoned Rust partner.

**0.5.1**,

## [crow-cli](https://crow-ai.dev/)

Minimal ACP Native Coding Agent

**0.1.20**,

## [Cursor](https://cursor.com/docs/cli/acp)

Cursor’s coding agent

**2026.03.30**

## [DeepAgents](https://docs.langchain.com/oss/javascript/deepagents/overview)

Batteries-included AI coding and general purpose agent powered by LangChain.

**0.1.7**,

## [Factory Droid](https://factory.ai/product/cli)

Factory Droid - AI coding agent powered by Factory AI

**0.109.1**

## [fast-agent](https://fast-agent.ai/)

Code and build agents with comprehensive multi-provider support

**0.6.24**,

## [Gemini CLI](https://geminicli.com/)

Google’s official CLI for Gemini

**0.39.1**,

## [GitHub Copilot](https://github.com/features/copilot/cli/)

GitHub’s AI pair programmer

**1.0.36**,

## [goose](https://block.github.io/goose/)

A local, extensible, open source AI agent that automates engineering tasks

**1.32.0**,

## [Junie](https://junie.jetbrains.com/)

AI Coding Agent by JetBrains

**1417.47.0**,

## [Kilo](https://kilo.ai/)

The open source coding agent

**7.2.24**,

## [Kimi CLI](https://moonshotai.github.io/kimi-cli/)

Moonshot AI’s coding assistant

**1.39.0**,

## [Minion Code](https://github.com/femto/minion-code)

An enhanced AI code assistant built on the Minion framework with rich development tools

**0.1.44**,

## [Mistral Vibe](https://mistral.ai/products/vibe)

Mistral’s open-source coding assistant

**2.8.1**,

## [Nova](https://www.compassap.ai/portfolio/nova.html)

Nova by Compass AI - a fully-fledged software engineer at your command

**1.0.100**,

## [OpenCode](https://opencode.ai/)

The open source coding agent

**1.14.26**,

## [pi ACP](https://github.com/svkozak/pi-acp)

ACP adapter for pi coding agent

**0.0.26**,

## [Qoder CLI](https://qoder.com/)

AI coding assistant with agentic capabilities

**0.1.48**

## [Qwen Code](https://qwenlm.github.io/qwen-code-docs/en/users/overview)

Alibaba’s Qwen coding assistant

**0.15.3**,

## [Stakpak](https://stakpak.dev/)

Open-source DevOps agent in Rust with enterprise-grade security

**0.3.74**,

## Using the Registry

Clients can fetch the registry programmatically:

```shellscript
curl https://cdn.agentclientprotocol.com/registry/v1/latest/registry.json
```

The registry JSON contains all agent metadata including distribution information for automatic installation.

## Submit your Agent

To add your agent to the registry:

1. Fork the [registry repository on GitHub](https://github.com/agentclientprotocol/registry)
2. Create a folder with your agent’s ID (lowercase, hyphens allowed)
3. Add an `agent.json` file following [the schema](https://github.com/agentclientprotocol/registry/blob/main/agent.schema.json)
4. Optionally add an `icon.svg` (16x16 recommended)
5. Submit a pull request

See the [contributing guide](https://github.com/agentclientprotocol/registry/blob/main/CONTRIBUTING.md) for details.