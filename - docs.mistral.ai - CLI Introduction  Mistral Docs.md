---
source: "https://docs.mistral.ai/mistral-vibe/terminal"
author:
published:
created: 2026-04-17
---
## CLI Introduction

**Mistral Vibe** is a command-line coding assistant powered by Mistral's models. It provides a conversational interface to your codebase, allowing you to use natural language to explore, modify, and interact with your projects through a built-in set of tools.

![vibe_logo](https://docs.mistral.ai/img/vibe-logo.svg)

The code is available on [GitHub](https://github.com/mistralai/mistral-vibe) under an Apache 2.0 license.

Features

- **Interactive Chat**: A conversational AI agent that understands your requests and breaks down complex tasks.
- **Built-in Toolset**: A suite of tools for file manipulation, code searching, version control, and command execution, right from the chat prompt.
	- Read, write, and patch files (read\_file, write\_file, search\_replace).
		- Execute shell commands in a stateful terminal (bash).
		- Recursively search code with grep (with ripgrep support).
		- Manage a todo list to track the agent's work.
- **Project-Aware Context**: Mistral Vibe automatically scans your project's file structure and Git status to provide relevant context to the agent, improving its understanding of your codebase.
- **Advanced CLI Experience**: Built with modern libraries for a smooth and efficient workflow.
	- Autocompletion for slash commands (/) and file paths (@).
		- Persistent command history.
		- Beautiful Themes.
- **Highly Configurable**: Customize models, providers, tool permissions, and UI preferences through a simple config.toml file.
- **Agents & Skills**: Create and manage multiple agents with different skills and permissions.
- **Safety First**: Features tool execution approval.

Learn More

Find how to install and use Mistral Vibe.

- [Installation](https://docs.mistral.ai/mistral-vibe/terminal/install): How to Install Mistral Vibe.
- [Quickstart](https://docs.mistral.ai/mistral-vibe/terminal/quickstart): A quickstart guide to using Mistral Vibe.
- [Configuration](https://docs.mistral.ai/mistral-vibe/terminal/configuration): How to Configure Mistral Vibe.
- [Agents & Skills](https://docs.mistral.ai/mistral-vibe/agents-skills): How to use Agents and Skills with Mistral Vibe.
- [Offline / Local](https://docs.mistral.ai/mistral-vibe/local): How to run Mistral Vibe with a local model.