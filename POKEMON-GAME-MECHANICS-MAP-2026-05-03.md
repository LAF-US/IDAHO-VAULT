---
title: "Pokemon and Game Mechanics Map"
date: 2026-05-03
authority: LOGAN
authors:
  - Codex
status: active
type: research-note
tags:
  - pokemon
  - game-mechanics
  - vault-architecture
  - home-layer
---

# Pokemon and Game Mechanics Map

This note compresses the game-mechanics analogies LOGAN and GEMINIAEUS surfaced into a single vault map.

## Core mechanics

| Game mechanic | Vault analogue | Meaning |
|---|---|---|
| Pokemon Party | Active session context | Small, curated working set; 6-slot pressure maps to token/window limits. |
| Pokemon Center terminal | Session start / retrieval moment | The point where context is loaded from storage into the active party. |
| Pokemon PC / Boxes | Shared vault / repo corpus | Durable, organized, fixed-point storage for canonical work products. |
| Pokemon Bank | Bridge registry | Transitional cloud layer between cartridge-era storage and HOME. |
| Pokemon HOME | Missing artifact registry | Cross-session, machine-queryable persistence for outputs and decisions. |
| Ender Chest | Agent dotfolder | Identity-bound personal context that follows the agent across sessions. |
| Shulker Box | Nested context module | Portable sub-context packed inside the Ender Chest layer. |
| Nether Chest | Non-canonical error term | Explicitly rejected in the canonical study; the real mechanic is the Ender Chest. |
| MCP Broker | Access interface candidate | Proposed interface for making HOME-like persistence queryable by agents. |

## The architectural split

- **Party** is volatile and narrow.
- **PC** is shared and durable.
- **Ender Chest** is personal and identity-bound.
- **HOME** is the missing bridge that would let durable artifacts survive session death without Logan manually re-injecting them.

## Canonical conversation sources

- [0401 - The Concierge.md](/Users/logan/IDAHO-VAULT/0401%20-%20The%20Concierge.md:1944)
- [20260104 - The Clerk.md](/Users/logan/IDAHO-VAULT/20260104%20-%20The%20Clerk.md:130)
- [ASSAY-LANDSCAPE-GAME-MECHANICS-2026-04-02.md](/Users/logan/IDAHO-VAULT/ASSAY-LANDSCAPE-GAME-MECHANICS-2026-04-02.md:74)

## Working conclusion

The vault already has a strong PC layer and a functional Ender Chest layer. The open design problem is HOME: a structured artifact registry that any future session can query directly.
