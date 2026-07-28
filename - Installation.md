---
title: "Installation"
source: "https://docs.crewai.com/en/installation"
author:
published:
created: 2026-04-15
description: "Get started with CrewAI - Install, configure, and build your first AI crew"
date created: Wednesday, April 15th 2026, 9:06:55 pm
date modified: Wednesday, April 15th 2026, 9:07:18 pm
---

### Watch: Building CrewAI Agents & Flows with Coding Agent Skills

Install our coding agent skills (Claude Code, Codex, …) to quickly get your coding agents up and running with CrewAI.

You can install it with `npx skills add crewaiinc/skills`

<iframe frameborder="0" src="https://www.loom.com/embed/befb9f68b81f42ad8112bfdd95a780af"></iframe>

## Video Tutorial

Watch this video tutorial for a step-by-step demonstration of the installation process:

![](https://www.youtube.com/watch?v=-kSOTtYzgEw)

## Text Tutorial

**Python Version Requirements**

CrewAI requires `Python >=3.10 and <3.14`. Here’s how to check your version:

```shellscript
python3 --version
```

If you need to update Python, visit [python.org/downloads](https://python.org/downloads)

**OpenAI SDK Requirement**

CrewAI 0.175.0 requires `openai >= 1.13.3`. If you manage dependencies yourself, ensure your environment satisfies this constraint to avoid import/runtime issues.

CrewAI uses the `uv` as its dependency management and package handling tool. It simplifies project setup and execution, offering a seamless experience.

If you haven’t installed `uv` yet, follow **step 1** to quickly get it set up on your system, else you can skip to **step 2**.

## Creating a CrewAI Project

We recommend using the `YAML` template scaffolding for a structured approach to defining agents and tasks. Here’s how to get started:

## Enterprise Installation Options

For teams and organizations, CrewAI offers enterprise deployment options that eliminate setup complexity:

### CrewAI AMP (SaaS)

- Zero installation required - just sign up for free at [app.crewai.com](https://app.crewai.com/)
- Automatic updates and maintenance
- Managed infrastructure and scaling
- Build Crews with no Code

### CrewAI Factory (Self-hosted)

- Containerized deployment for your infrastructure
- Supports any hyperscaler including on prem deployments
- Integration with your existing security systems

## [Explore Enterprise Options](https://crewai.com/enterprise)

Learn about CrewAI’s enterprise offerings and schedule a demo

## Next Steps

## [Quickstart: Flow + agent](https://docs.crewai.com/en/quickstart)

Follow the quickstart to scaffold a Flow, run a one-agent crew, and produce a report.

## [Join the Community](https://community.crewai.com/)

Connect with other developers, get help, and share your CrewAI experiences.