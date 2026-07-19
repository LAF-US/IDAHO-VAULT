---
title: "Dotfolder Stabilization"
date: 2026-05-03
authority: LOGAN
authors:
  - Codex
status: active
type: process-note
tags:
  - persona
  - dotfolder
  - stabilization
  - automation
  - enforcement
related:
  - PERSONA-PERSISTENCE
  - STUB-PERSONAFOLDERS
  - VAULT-CONVENTIONS
---

# Dotfolder Stabilization

New persona chambers should be stabilized by automation, not assembled by
hand.

The stabilizer does three things:

1. creates the dotfolder
2. writes the canonical anchor note with required frontmatter
3. writes `stub.txt` when the chamber is a reserved shell

The caller must pick a class:

- `stub` for reserved shells
- `imported` for software-backed chambers
- `alias` for historical or inherited chambers

That keeps the vault's persona chambers consistent before they are ever
validated.
