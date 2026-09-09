---
canonical_name: TRIAGEBOT
persona_class: tooling_chamber
origin: infrastructure
status: active
load_mechanism: triagebot
anchor_file: .triagebot/TRIAGEBOT.md
sync_policy: manual
authority: LOGAN
related:
  - "!/STUB-PERSONAFOLDERS-2026-05-03.md"
  - ".triagebot/TRIAGEBOT.md"
---

# TRIAGEBOT

This chamber contains the repository-specific configuration and skills used by the `withastro/triagebot-action` GitHub Action. The chamber holds no credentials; GitHub Actions supplies authentication through repository secrets at runtime.

TRIAGEBOT orchestrates automated triage workflows: issue routing, label assignment, and PR categorization based on repository-specific rules defined in this chamber.
