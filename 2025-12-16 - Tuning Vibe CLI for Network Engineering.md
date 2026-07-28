---
title: "Tuning Vibe CLI for Network Engineering"
source: "https://torbjorn.dev/blog/mistral-vibe-cli-for-network-engineering/"
author:
  - "[[Torbjørn Bang]]"
published: 2025-12-16
created: 2026-06-06
description: "Teaching a software dev tool to speak network engineering"
date created: Saturday, June 6th 2026, 2:48:47 pm
date modified: Saturday, June 6th 2026, 2:50:11 pm
---

Table of contents

[Vibe CLI](https://github.com/mistralai/mistral-vibe) is Mistral’s answer to Claude Code and OpenAI Codex. Out of the box it’s optimised for software development, not network engineering. But with the some configuration tweaking it’s surprisingly capable for network tasks.

[TL;DR](#summary)

## Model selection

Vibe defaults to Devstral. It does quite a good job for most things but certain complex tasks do better with reasoning. My general “strategy” is to use Devstral until it seems to get stumped or otherwise performs poorly, then switch to Magistral.

Magistral model config:

```fallback
# ~/.vibe/config.toml

[[models]]
name = "magistral-medium-latest"
provider = "mistral"
alias = "magistral-medium"
temperature = 0.2
input_price = 2.0 
output_price = 5.0
```

It is worth mentioning that local inference with Ollama is an option. The config for this is straightforward but the results are pretty bad. Nothing that runs on a single GPU is useful for network tasks in my experience.

```gdscript3
# ~/.vibe/config.toml

[[providers]]
name = "ollama"
api_base = "http://localhost:11434/v1"
api_key_env_var = "OLLAMA_key"
api_style = "openai"
backend = "generic"

[[models]]
name = "deepseek-r1"
provider = "ollama"
alias = "deepseek-r1"
temperature = 0.2
input_price = 0.0
output_price = 0.0

# ~/.vibe/.env
OLLAMA_API_KEY='ollama'
```

## MCP Servers

MCP servers expose APIs as tools the AI can call during conversations. For networking tasks they’re most useful to pull network data (for the time being), not for making changes. The quality of many MCP servers is half-baked with poorly described and implemented tools. This tends to lead to unintended results when making changes to external systems.

You can find a list of available servers at [mcp.so](https://mcp.so/). There is little to no vetting of the servers & clients submitted, so you should do your research as to which are worth using. One of my favorite MCP servers is the Netbox MCP server. It currently only has “read-only” tools, but will hopefully be extended in the future.

Netbox MCP server config:

```fallback
# ~/.vibe/config.toml
[[mcp_servers]]
name = "netbox"
transport = "stdio"
command = "uvx"
args = ["--directory", "/path/to/netbox-mcp-server", "netbox-mcp-server"]

# ~/.vibe/.env
NETBOX_URL=https://netbox.example.com
NETBOX_TOKEN=<your-api-token>
```

## Custom system prompts

System prompts make more of a difference than I assumed. Turns out hobby psychology for plinko machines is part of the job now.

The default is oriented towards software development and looks something like this:

```gdscript3
You are operating as and within Mistral Vibe, a CLI coding-agent built by Mistral AI and powered by default by the Devstral family of models. 
It wraps Mistral's Devstral models to enable natural language interaction with a local codebase. Use the available tools when helpful.

You can:
- Receive user prompts, project context, and files.
- Send responses and emit function calls (e.g., shell commands, code edits).
....
```

I have experimented with and had success with a couple different system prompts for different purposes:

1. [Network engineer](https://gist.github.com/torbbang/e4e4dabacc6b5f2132148792d0cd4370), intended to be used interactively in configuration & troubleshooting. My main usecase for this is interacting with network devices through [VibeTTY](https://github.com/torbbang/vibetty).
2. [Config auditor](https://gist.github.com/torbbang/582e5d5b9462013fa3dc490673b08a82), intended to be used autonomously as part of a CI workflow.

I have structured the network engineer prompt like this:

```mysql
You are a network engineering sidekick. Your primary role is to act as a collaborative partner to a human network engineer. Your goal is to help them analyze, troubleshoot, and configure real-world infrastructure. You have a set of tools to achieve this; always prefer the least impactful tool first (e.g., prefer read-only \`show\` commands over disruptive \`debug\` commands). Always prioritize safety, clarity, and human validation.

**Communication Style:**

*   **Be Concise:** Get straight to the point. Avoid conversational filler.
... shortened ...

**Core Principles:**

1.  **Clarify and Analyze:** When given a problem, first ensure you understand it. If a request is vague (e.g., "the network is slow"), ask clarifying questions to narrow the scope before proceeding (e.g., "Which users, applications, or destinations are affected?"). Once the problem is clear, analyze it using read-only tools (like \`ping\`, \`traceroute\`, \`show\` commands, etc.). Explain your findings, suggest the next diagnostic step, or propose a configuration change.
... shortened ...

**Example Workflow:**

> **User:** "The redundant link to our DR site is flapping. It's causing intermittent reachability issues to 10.100.0.0/16."
>
> **You:** "Understood. I'll check the BGP session status on the primary and secondary border routers."
>
> **You:** (Runs \`show bgp summary\` on R1 and R2). "The BGP session on R2 (the secondary) is unstable, cycling between Idle and Active. I see a high number of connection resets. This could be a Layer 2 issue or a misconfigured BGP timer."
>
... shortened ...
```

A few things that helped me: be specific about scope (read-only? config generation?), set explicit safety boundaries (“never run disruptive commands without confirmation”), and tell it when to ask versus when to act. A vague “you are a network engineer” prompt gets you vague results. I am not an expert in “prompt engineering”, so take this advice with a grain of salt. I encourage you to put in some effort to learn to write prompts, it will pay off!

You can set the system prompt it in your config. The value here references files in ~/.vibe/prompts without the.md extension, with the default value being “cli”.

```fallback
system_prompt_id = "my_custom_prompt"
```

**Note:** I have experimented with tweaking the compact prompt as well, but the default does a *really* good job. I have only been able to make it perform worse by altering it.

## Juggling configs

Having one config to rule them all sounds good until you need a paranoid agent for production and an unrestricted one for R&D. Cramming all of this into one config.toml turns into a mess of commented-out lines and questioning “wait, which settings are active?”

Vibe has two main ways to handle this.

### Agent configurations

Vibe’s agent system lets you create specialized ‘agents’ that override parts of your main `config.toml`. Agents are defined in files under `~/.vibe/agents/NAME.toml`, letting you tweak *most* settings in the config. You start them with `vibe --agent {agent name without .md ending}`.

The big gotcha is that agents can’t have their own MCP server configs. They can only be configured globally and I assume there are other parameters I haven’t tested where this also applies. So if you are going to use agents with MCP servers you will have to maintain a set of allowed/disallowed tools per agent.

### Multiple VIBE\_HOMEs

A much cleaner way to keep multiple configurations is to use the `VIBE_HOME` environment variable. This lets you keep completely separate vibe configuration directories(“homes”).

For any given project/purpose you can create a local `.vibe` directory and point `VIBE_HOME` to it with `export VIBE_HOME=~/Code/project-foo/.vibe`. If you wish to automate it for a project you can use `direnv`, or a helper script like [set-vibe](https://gist.github.com/torbbang/584392f06ef5777bdd71d377c0a12f5d) (put alternative config folders in ~/.vibe/alt-configs/)

## Cool, but why?

LLMs are inaccurate and pretty bad at networking.

If you give them complex problems they tend to make ill advised assumptions. They can describe functionality of protocols & NOSes perfectly, but they don’t actually seem to *understand* how networks operate at an advanced level.

What they are really good at is basic analysis and generating boilerplate. Most modern network engineers live in brownfield environments, and if you are a consultant you get to wrangle multiple brownfield environments. This entails a significant amount of time spent on analysis. Whether that is for documenting, troubleshooting or planning changes; all of these tasks benefit from automated analysis.

If the LLM turns out to be useless for your particular problem, it at least works as a pretty good [rubber duck](http://rubber-ducking.urbanup.com/4943256).

## Summary

Vibe CLI is quickly becoming the best CLI-based tool for integrating LLMs into my network engineering workflows. Its flexibility lets you tune it quite well for network tasks instead of software dev defaults. The main adjustments I have found to make a difference:

- **Model selection:** Devstral 2 handles most tasks well, but when it starts spinning its wheels you will be well served to switch to Magistral.
- **MCP servers:** The right context makes all the difference. Hook up relevant MCP servers for an improved user experience and output quality.
- **Custom prompts:** Skip the default “you are a coding assistant” prompt and write one that lends itself to network engineering.
- **Multiple configurations:** Stop juggling commented-out config lines. Use agents or `VIBE_HOME` to keep separate configs for different environments and purposes.

---

### See Also

- [Building your own Containerlab node kinds](https://torbjorn.dev/blog/creating-clab-node-kinds/)
- [Containerlab Cisco images simplified](https://torbjorn.dev/blog/cml-nodes-in-clab/)
- [Moving to Forgejo on Hetzner](https://torbjorn.dev/blog/forgejo-on-hetzner/)
- [Gleaning DNS resolver behavior](https://torbjorn.dev/blog/resinfo/)
- [EEM in Catalyst Center templates](https://torbjorn.dev/blog/eem-cc-templates/)

**Got feedback or a question?**  
Feel free to contact me at [hello@torbjorn.dev](mailto:hello@torbjorn.dev)