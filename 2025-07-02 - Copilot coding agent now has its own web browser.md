---
title: "Copilot coding agent now has its own web browser"
source: "https://github.blog/changelog/2025-07-02-copilot-coding-agent-now-has-its-own-web-browser/"
author:
  - "[[Allison]]"
published: 2025-07-02
created: 2026-06-03
description: >
  GitHub Copilot coding agent, available in public preview, now has access to a web
  browser out of the box, powered by the Playwright MCP server. This feature is in public…
updated: 2026-06-03
---

> **SOURCE ATTRIBUTION**  
> This content is a web-clipped excerpt from GitHub's official changelog: "Copilot coding agent now has its own web browser" (https://github.blog/changelog/2025-07-02-copilot-coding-agent-now-has-its-own-web-browser/).  
> Clipped for reference and internal documentation purposes. Original changelog is maintained by GitHub; refer to the source for licensing details.

[GitHub Copilot coding agent](https://docs.github.com/copilot/using-github-copilot/coding-agent), available in public preview, now has access to a web browser out of the box, powered by the [Playwright MCP server](https://github.com/microsoft/playwright-mcp). This feature is in public preview.

When you delegate a task to Copilot, the agent starts work in the background in its own development
environment.

Model Context Protocol (MCP) servers allow extending Copilot’s capabilities with new tools. You can [configure your own](https://docs.github.com/enterprise-cloud@latest/copilot/how-tos/agents/copilot-coding-agent/extending-copilot-coding-agent-with-mcp), but the GitHub MCP server and Playwright are enabled by default.

Thanks to the power of Playwright, Copilot can interact with a web app while it makes changes. This
allows Copilot to reproduce bugs and validate its work.

![Example of session logs showing Copilot validating its work](https://github.com/user-attachments/assets/d2fac9aa-8dfc-4682-8071-b26ad2400ceb)

Copilot can even share screenshots of what it has done in its pull request:

![Screenshot of Copilot coding agent including a screenshot it has captured in its pull request](https://github.com/user-attachments/assets/d6b740ce-f752-4f05-ad31-9b261f364952)

Copilot coding agent is available to all paid Copilot users. If you have Copilot Business or Copilot Enterprise, an administrator will need to [enable access](https://docs.github.com/en/enterprise-cloud@latest/copilot/how-tos/agents/copilot-coding-agent/enabling-copilot-coding-agent).

To find out more about Copilot coding agent and learn best practices, head to [our documentation](https://gh.io/copilot-coding-agent-docs).
