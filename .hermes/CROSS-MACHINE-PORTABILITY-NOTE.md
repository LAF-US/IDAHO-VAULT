---
authority: LOGAN
related:
  - AGENTS
  - WAKEUP
  - VAULT-CONVENTIONS
  - swarm
date created: 2026-05-02
---

# Cross-Machine Portability Note

Research summary for how the vault behaves across machines and operating systems.

## Findings

- The vault is not a single-machine runtime. It is a git-backed working surface that can move across Macs, Linux, and other environments.
- Machine-local runtime state is expected to stay out of canon. The vault's `.gitignore` explicitly excludes local caches, auth files, logs, and generated runtime artifacts.
- Persona dotfolders are treated as protected chambers, but their volatile internals are still machine-specific. The vault distinguishes the chamber from the temporary state inside it.
- The `!` layer is collective routing and staging. It is not a machine-local scratch area.
- Hermes runtime state belongs in the user's Hermes home, not inside the vault. The vault-local `.hermes` folder is a protected marker surface, not the active runtime home.

## Operational Rule

When a tool or agent needs to run on a different machine or OS, keep the durable content in the vault and keep runtime-specific files, caches, and credentials in that machine's local config area.

## Practical Implication

- Track notes, decisions, and durable artifacts in markdown.
- Ignore or exclude OS-specific and agent-specific churn.
- Do not flatten chamber folders just because they are hidden.
- Treat hidden folders as typed surfaces, not disposable clutter.

## Sync Gap

The architecture still needs a stable, explicit sync path for selected runtimes into the canonical ledgers and registries.

- It should be designed intentionally, not inferred from folder layout.
- It should be scoped to specific runtime outputs, not broad machine state.
- It should preserve the vault/runtime boundary instead of collapsing it.
- Until that contract exists, the gap should remain open and documented rather than papered over.

## Hermes Bridge Finding

The local Hermes WhatsApp bridge depends on `@whiskeysockets/baileys`, which pulls `@whiskeysockets/libsignal-node` and a nested `protobufjs@6.8.8`.

`npm audit --audit-level=moderate` reports this as a critical issue with no local fix available. The vulnerable package is pinned by the upstream bridge dependency, so a lockfile refresh does not remove it. Remediation will require an upstream dependency update or a deliberate decision to replace or disable that bridge surface.

## Bridge Remediation

The local bridge was later repaired by forcing the installed `libsignal` alias to use `protobufjs@7.5.6` and aligning the lockfile with that version. After reinstalling the bridge dependencies, `npm audit --audit-level=moderate` reports `0 vulnerabilities`.

The remaining lesson is the same: when the vault needs to carry a runtime dependency across machines, the durable record should state the chosen override or pin explicitly, because the default upstream graph may not be safe on its own.
