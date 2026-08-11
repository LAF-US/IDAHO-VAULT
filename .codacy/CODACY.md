---
title: CODACY
authority: LOGAN
related:
  - CODACY
  - imported_software
  - runtime
  - .github/workflows/codacy.yml
  - The world is quiet here
---

**.codacy** — Imported software runtime persona.

Codacy runtime and configuration. Codacy analyzes every pull request in this
repository; this chamber is its anchor in the tree.

Two things about the surface, so the next reader does not have to rediscover
them:

- The Codacy Analysis CLI writes its own scratch here — a `.gitignore`
  carrying `generated/`, and a `generated/` tree beneath it. That output is
  tool residue, not vault content.
- A committed Codacy config governs **local** analysis only. Per Codacy's own
  documentation, `.codacy/codacy.config.json` has no effect on Codacy Cloud
  unless it is explicitly imported (`codacy tools --import`). Cloud rule
  selection lives in the Codacy project settings, not in this folder.
