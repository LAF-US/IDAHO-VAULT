---
title: "POKA-YOKE"
updated: 2026-07-24
status: active
authority: "LOGAN"
aliases:
  - poka yoke
  - Poka-Yoke
  - mistake-proofing
  - error-proofing
tags:
  - doctrine
  - systems/quality
related:
  - VAULT-CONVENTIONS
  - CONSTITUTION
  - "!/WAKEUP.md"
  - "!-AGENT-GIT-GUARDRAILS"
---

# POKA-YOKE — Mistake-Proofing

## The Term

**Poka-yoke** (ポカヨケ) is any mechanism built into a process that helps the
person operating it avoid mistakes — by making the error impossible, or by
surfacing it the moment it occurs. From Japanese *poka* (inadvertent mistake)
+ *yokeru* (to avoid). Formalized by industrial engineer **Shigeo Shingo** in
the 1960s as part of the Toyota Production System.

Shingo originally called it *baka-yoke* — "fool-proofing" — and renamed it
after a worker objected. The rename carries the whole doctrine: inadvertent
error is natural and universal, not a measure of intelligence, and **the
responsibility for error lies in the design of the system, not in the person
who slipped**. Blame targeted at individuals is an ineffective countermeasure;
a simple mechanism that guides the process is an effective one.

Sources: [Wikipedia — Poka-yoke](https://en.wikipedia.org/wiki/Poka-yoke),
[Kaizen Institute — Poka Yoke: error-proof processes](https://kaizen.com/insights/poka-yoke-processes-error-proof/),
[TEEPTRAK — What is Poka-yoke?](https://teeptrak.com/en/what-is-poka-yoke-mistake-proofing-2026/).
(Web-search provenance, retrieved 2026-07-24; not primary Shingo texts.)

## Why It Is Named Here

This vault already operates on Shingo's premise without having named it.
`!-AGENT-GIT-GUARDRAILS.md` states the root cause of broken repos plainly:
agents misanalyze, then act — "the agents' analysis is often wrong." The
vault's answer has consistently been **system design, not blame**: hard gates,
wrapper scripts, firewalls, and recovery documents. This note names that
pattern so future machinery can be judged against it.

Two questions classify any device:

1. **Prevention or detection?** Does it make the wrong action impossible, or
   surface it immediately after?
2. **Block or warn?** Does it stop the line (hard gate), or advise (soft
   signal)?

Prevention > detection > documentation. A rule written in a governance file
that an agent must remember to follow is the weakest form; a gate that fails
closed is the strongest.

## Ledger — Existing Poka-Yoke Devices in This Vault

Grounded in `VAULT-CONVENTIONS.md` and files read this session:

| Device | Kind | Where it lives |
| --- | --- | --- |
| Secret pattern gate | Prevention, blocks | `.githooks/pre-commit` + `.github/scripts/check_secret_patterns.py`; blocking CI in `secret-pattern-policy.yml`; weekly sweep in `secret-pattern-full-scan.yml` |
| Portable path gate (NETWEB) | Prevention, blocks | `check-portable-paths.yml` — hard gate on every PR and push to `main`; `.gitignore` reserved-name patterns as the advisory layer |
| `_PREFIX` aliasing | Prevention, guides | `VAULT-CONVENTIONS.md` § NETWEB — reserved-name collisions get `_` prefix + `aliases:` so wikilinks never break |
| Character conformity gate | Detection, blocks | `check-character-conformity.yml` + `.github/scripts/check_character_conformity.py` — UTF-8/BOM enforcement per PR |
| `data.json` firewall | Prevention, blocks | `.gitignore` wildcard `.obsidian/plugins/*/data.json` — plugin credentials cannot reach the public repo without a deliberate `git add --force` |
| Git guard wrapper | Prevention, blocks | `scripts/git-guard.sh` / `scripts/Invoke-GitGuard.ps1` per `!-AGENT-GIT-GUARDRAILS.md` — intercepts history-rewriting and remote-destroying commands before they run |
| Merge queue entry gates | Prevention, blocks | Main Ruleset — signed commits, completed Copilot review, resolved threads required before a PR can even enter the queue (`VAULT-CONVENTIONS.md` § merge queue) |
| Risk-tier classification | Detection, guides | `.github/scripts/classify_paths.py` — changed files classified by risk tier in the auto-PR flow |
| Structure audit | Detection, warns | `.github/scripts/sort_audit.py` — weekly audit for misplaced files |
| The `*` wildcard | Prevention, guides | Epistemological rule (`.claude/CLAUDE.md`, PERSONAE ENGINE) — where provenance is absent, the honest output is `*`, not invented certainty |
| `!/WAKEUP.md` | Recovery, guides | Disorientation protocol — a fixed re-entry sequence so a confused agent reads before acting |
| "Plain Words Before the Lore" | Prevention, guides | `CLAUDE.md` / `.claude/CLAUDE.md` — names the persona-inflation failure mode up front, so feeling chosen is recognized as the bug, not a promotion |

The last three are **cognitive poka-yoke**: the process being mistake-proofed
is the agent's own reasoning. Same doctrine, different assembly line.

## Inventoried by Filename Only `*`

These workflows exist in `.github/workflows/` and their names suggest
poka-yoke intent, but they were not read when this note was written — their
actual behavior is unverified here: `large-file-policy.yml`,
`large-file-watchdog.yml`, `action-pin-policy.yml`,
`python-version-pin-policy.yml`, `redaction-damage-policy.yml`,
`check-dotfolder-anchors.yml`, `laf-usb-manifest-policy.yml`. A future pass
may promote them into the ledger with grounded descriptions.

## Design Rule Going Forward

When adding durable machinery to the vault, prefer the poka-yoke form:

- **Fail closed.** A gate that cannot run should block, not silently pass.
- **Make the wrong action impossible** rather than documented. Move rules
  down the stack: doctrine → checklist → warning → hard gate, as far as the
  matter warrants.
- **Blame the design, not the operator.** When an agent or human slips, the
  witness question is "what device was missing?" — consistent with the Repair
  axis: witness the error, restore order, then mistake-proof the path.
- **Do not over-engineer.** Per the Guiding Principles, only build what is
  needed now. A poka-yoke earns its place by catching a mistake that actually
  happens; a speculative gate is just friction.

## See Also

- `VAULT-CONVENTIONS.md` — NETWEB, secrets gating, merge queue, guiding principles
- `!-AGENT-GIT-GUARDRAILS.md` — the vault's founding poka-yoke case study
- `!/WAKEUP.md` — recovery protocol
- `CONSTITUTION.md` — governance authority over all of the above
