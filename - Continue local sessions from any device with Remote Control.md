---
title: "Continue local sessions from any device with Remote Control"
source: "https://code.claude.com/docs/en/remote-control"
author: "Anthropic"
published:
created: 2026-06-03
description: "Reference pointer for Anthropic Claude Code Remote Control documentation; summarized for vault context instead of preserving a full vendor-doc copy."
doc_class: sources
status: archived
authority: LOGAN
tags:
  - claude-code
  - remote-control
  - source-capture
---
> **SOURCE ATTRIBUTION**  
> This content is adapted from Anthropic's official Claude Code documentation: "Continue local sessions from any device with Remote Control" (https://code.claude.com/docs/en/remote-control).  
> Adapted for reference and internal documentation purposes under fair use for educational/operational use. Some sections have been edited for clarity or brevity. Original documentation is maintained by Anthropic.

Remote Control is in research preview and available on all plans. On Team and Enterprise, it is off by default until an admin enables the Remote Control toggle in [Claude Code admin settings](https://claude.ai/admin-settings/claude-code).

# Continue local sessions from any device with Remote Control

This note points to Anthropic's Claude Code Remote Control documentation. The original PR draft contained a near-complete copy of the vendor page; this version keeps only a short vault-local summary and the source link.

## Vault-Relevant Summary

Remote Control is described by Anthropic as a way to steer a local Claude Code session from `claude.ai/code` or the Claude mobile app while the session continues to run on the user's machine.

For vault purposes, the important points to remember are:

- It exposes a remote steering surface for a local Claude Code process.
- It can help continue an in-progress local session from another device.
- It depends on Claude Code version, account eligibility, login state, workspace trust, and possible admin or device policy.
- It can create coordination risk if several agents act in the same checkout; use worktree or session isolation when that matters.
- The source page, not this capture, should be used for current setup, security, limitations, and troubleshooting details.

## Source

- Anthropic documentation: <https://code.claude.com/docs/en/remote-control>

## Capture Note

Captured for context on 2026-06-03. This is not a live copy of the vendor page and should not be treated as current product documentation.