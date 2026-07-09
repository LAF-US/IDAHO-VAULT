---
name: project-dotdir-reconciliation
description: "Bidirectional sync between individual computers (their dotdirs — ~/.hermes/, ~/.openclaw/, ~/.ollama/, etc.) and the IDAHO-VAULT repo is in active development by a Codex agent authoring on Windows under Logan's direction to use Python + rsync/rclone (cross-platform tools, not net-new infrastructure). Tracked on GitHub. Paused as of 2026-06-24; resumes in a few days. Will likely need gentle Mac retooling at the edges (paths, service-mechanism translation, BSD-vs-GNU tool quirks) when it lands here."
metadata: 
  node_type: memory
  type: project
  originSessionId: 4f03d270-3e64-41cc-b325-30871ab76d55
---

A Codex agent is actively building **dotdir reconciliation** — bidirectional sync between per-machine dotdir state (e.g., `~/.hermes/`, `~/.openclaw/`, `~/.ollama/`) and the IDAHO-VAULT repo. The Codex is **authoring on Windows-ZBFURY** under Logan's direction to **stick to Python and existing cross-platform tools (rsync, rclone, etc.)** rather than rolling new infrastructure. **Current direction is machine-to-vault** (uploading local state into the vault as records) — *not* vault-to-machine yet. Implication: my local config edits will get witnessed into the vault when the sync runs; they will NOT be overwritten by a vault-to-machine push. Safe to make local config changes in the meantime. The work is **tracked on GitHub** (Logan didn't name the specific issue/PR; ask if needed) and is **paused as of 2026-06-24**, expected to resume in a few days. Logan flagged 2026-06-24 that **gentle Mac retooling may be required** once the Windows-authored work lands — likely at the edges: paths (`%APPDATA%`-ish assumptions vs `~/Library/...`), service-mechanism translation (Task Scheduler ↔ launchd plists), BSD-vs-GNU tool quirks (BSD sed lacks `\s`, GNU has it), and the fact that rsync is native on Mac but extra-install on Windows. The core tool choices (Python + rclone) are cross-platform-native so the retooling should be small.

**Why:** Drift between vault records and local machine state is a known problem (clearly visible in this session — Hermes' `config.yaml` drifted from BEEFSTACK records between 2026-05-19 and 2026-06-23 with no vault witness). The reconciliation work is the structural answer to that class of problem: instead of relying on Logan or any agent to file a vault witness every time a local config changes, the sync mechanism keeps the two layers in deliberate, traceable alignment. Confirmed by Logan 2026-06-24 in response to my drift diagnosis.

**How to apply:**
- **Do not propose competing sync mechanisms.** When I notice drift, surface it for awareness — don't try to design or implement a vault-↔-local sync of my own. The Codex's design is the one in flight; respect the boundary.
- **Don't pre-emptively reconcile records to local state** (or vice versa) outside of small, Logan-authorized edits. Wholesale reconciliation is the Codex's job.
- **When the Codex resumes** (mid-to-late June 2026), be ready either to coordinate via the swarm registry (`swarm.json` referenced in the 2026-06-24 manifest) or to stay out of its lane entirely — whichever Logan directs.
- **Be alert to the "dotdir" framing.** The unit of reconciliation is each machine's dotdir, not individual files. Suggestions that touch dotdir layout should consider how they'll interact with sync.
- **Find the GitHub tracking issue/PR** when needed — Logan didn't name it explicitly; ask before assuming a particular issue number.

**Per-machine dotdir state the reconciliation work needs to be aware of, this Mac:**

- `~/.hermes/.env` — bootstrap token (`OP_SERVICE_ACCOUNT_TOKEN`), `SUDO_PASSWORD`, plaintext config vars. Mode 600. Treat as containing secret material (the bootstrap token resolves anything else); should be gitignored on the vault side, never synced as plaintext.
- `~/.hermes/.env.op` — NEW FILE as of 2026-06-28. 23 op:// references for every secret-bearing env var. Mode 600. Contains *only* references (no secret values), so the reconciliation work could potentially sync this verbatim into the vault as a config record (similar to how `IDAHO-VAULT/.op/openrouter.env.template` already lives in the vault). Decision lives with Logan and the Codex.
- `~/.hermes/bin/hermes-gateway-launch.sh` — launcher shim, recently rewritten to support the op:// resolution workaround. Non-secret. Safe to sync.
- `~/.hermes/README-workaround.md` — operator-facing documentation of the workaround. Safe to sync.
- `~/.hermes/config.yaml` — non-secret config (model routing, provider declarations, provider_routing block). Safe to sync.
- `~/.hermes/sessions/` — session JSONs may contain secret-shaped content via tool calls, redaction warnings, debug output. Risky to sync verbatim; needs redaction pass first.
- `~/.openclaw/secrets/` — OpenClaw's structured secret store. Treat same as `.env` — don't sync plaintext.
- `~/Library/LaunchAgents/ai.hermes.gateway.plist`, `~/Library/LaunchAgents/ai.openclaw.gateway.plist` — service definitions, machine-mode-644. Safe to sync; useful as records of how this Mac launches its daemons.

The 2026-06-28 workaround witness at `IDAHO-VAULT/HERMES-WORKAROUND-WITNESS-2026-06-28.md` captures the current shape of this Mac's Hermes credential plumbing as of that date.

Related: [[defrag-project]] (broader "defrag Logan's life" initiative this fits inside), [[records-vs-doctrine]] (drift mode the reconciliation work addresses), [[openclaw-machine-policy]] (machine-scoped policy that reconciliation must respect — same dotdir name, different policy per machine).
