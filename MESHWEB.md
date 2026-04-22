---
authority: LOGAN
related:
  - NETWEB
  - VAULT-CONVENTIONS
  - MCP
  - 1Password
  - AGENTS
  - Linear
  - CLOUD
date created: Sunday, April 12th 2026
status: active
---

# MESHWEB — Cloud-Local Runtime Portability Standard

NETWEB solved cross-platform **filesystem** portability (Windows / macOS / Linux / iOS).  
MESHWEB extends the same logic to cross-environment **runtime** portability.

---

## The Problem

IDAHO-VAULT operates across three distinct runtime environments. Each has different toolchain availability, secret access patterns, and process execution capabilities. Configs and scripts written for one environment silently fail in another.

This is the same class of problem NETWEB solved for filenames — different runtimes have different capabilities, and the lowest common denominator must be respected or gaps must be explicitly documented and handled.

---

## Runtime Environments

| Environment | ID | Description |
|---|---|---|
| Logan's Windows Desktop | `local` | Full machine access — `op` CLI, SSH agent, npm, MCP server process spawning, Obsidian |
| Cloud Claude Code (claude.ai/code) | `cloud` | Sandboxed agent — repo clone + npm available; no `op`, no SSH, no local process spawning beyond the sandbox |
| GitHub Actions CI | `ci` | Ephemeral runner — `op` via `OP_SERVICE_ACCOUNT_TOKEN`, npm, git; no interactive input, no Logan's local config |

---

## Capability Map

| Capability | `local` | `cloud` | `ci` |
|---|---|---|---|
| `op` CLI (1Password) | ✅ (after setup) | ❌ | ✅ (via service account) |
| `op://` secret references | ✅ (after setup) | ❌ | ✅ (via `op run`) |
| SSH agent / git signing | ✅ | ❌ | ❌ |
| MCP server process spawning | ✅ | ⚠️ sandbox-limited | ❌ |
| `npx` / `npm` | ✅ | ✅ | ✅ |
| Filesystem writes beyond repo | ✅ | ❌ | ❌ |
| Interactive input | ✅ | ✅ (via Logan) | ❌ |
| GitHub API (via MCP) | ✅ | ✅ | ✅ (via GITHUB_TOKEN) |
| Linear API (via MCP) | ✅ (local MCP server) | ❌ (no MCP spawn) | ⚠️ (via REST only) |
| Obsidian REST API | ✅ | ❌ | ❌ |

---

## Gap Conventions

### Convention 1 — Environment Annotation

Any config file, workflow, or script that is **not portable across all three environments** must declare its scope. Since JSON files cannot carry comments, use a companion annotation:

- For `.mcp.json`: companion `MESHWEB-MCP.md` in the same directory (or repo root)
- For `.github/workflows/*.yml`: add `# meshweb: ci-only` comment at top
- For shell scripts: add `# meshweb: local-only` shebang comment

### Convention 2 — Substitution Table

When a capability is unavailable in an environment, document the substitution:

| Capability Gap | `local` pattern | Cloud substitute | CI substitute |
|---|---|---|---|
| `op://` secret resolution | `op run -- <cmd>` | env var injected by Anthropic cloud infrastructure (if supported) OR manual paste by Logan | `OP_SERVICE_ACCOUNT_TOKEN` → `op item get` in workflow step |
| Linear API access | MCP server (`linear-mcp-server`) | Linear REST API via `curl` / SDK in script | Linear REST API via `curl` / SDK in workflow step |
| Vault filesystem writes | Claude Code file tools | Claude Code file tools (repo clone) | `git` commit in workflow |
| SSH git signing | 1Password SSH agent | N/A (commits unsigned from cloud) | N/A (GITHUB_TOKEN, not signed) |

### Convention 3 — The MESHWEB Registry

Env-scoped artifacts are listed below. Agents must check this registry before creating configs that use environment-specific capabilities.

| Artifact | Env scope | Gap documented | Substitute |
|---|---|---|---|
| `.mcp.json` | `local` | ✅ | Cloud: no MCP server spawn; use Linear REST or Logan pastes content |
| `.op/SETUP.md` | `local` | ✅ (template, pending Logan execution) | CI: `OP_SERVICE_ACCOUNT_TOKEN` in GitHub Secrets |
| `.github/workflows/1password-secret-template.yml` | `ci` | ✅ | Local: `op item get` directly |

---

## Agent Rules

1. **Before writing a config that uses `op`, an `op://` reference, a local process, or SSH**: check this capability map. If the artifact is not `cloud`-compatible, add it to the MESHWEB Registry with its scope and substitute.

2. **Cloud instance operational boundary**: The cloud Claude Code instance operates within the `cloud` row of the capability map above. It does not have `op`. It does not spawn MCP servers. It reads and writes the repo clone. It cannot access 1Password. It can use npx/npm within the sandbox.

3. **Do not assume `op` is available**: The NETWEB equivalent — just as agents must not create `AUX.md`, agents must not write configs that assume `op` is present without checking the runtime environment.

4. **Document the gap, don't paper over it**: If a capability doesn't port, say so explicitly. Undocumented gaps are the MESHWEB equivalent of silent filename collisions.

---

## Enforcement

| Layer | Mechanism | Scope |
|---|---|---|
| MESHWEB Registry (this file) | Manual audit by agents + Logan | Preventive |
| Agent discipline | Read MESHWEB before writing env-scoped configs | Preventive |
| CI gate | TBD — `check-meshweb-scope.yml` (future) | Hard gate (not yet implemented) |

---

## Relationship to NETWEB

| | NETWEB | MESHWEB |
|---|---|---|
| Dimension | Filesystem platform portability | Runtime environment portability |
| Problem | `AUX.md` fails on NTFS | `op run` fails in cloud |
| Solution | `_AUX.md` + `aliases: [AUX]` | Registry + substitution table + env annotation |
| Enforcement | `check-portable-paths.yml` CI gate | `check-meshweb-scope.yml` (TBD) |
| Lowest common denominator | NTFS restrictions | Cloud sandbox restrictions |

---

## Open Items

- [ ] CI workflow `check-meshweb-scope.yml` — automated detection of env-scoped patterns in PRs
- [ ] Cloud MCP server support — determine if `claude.ai/code` supports env var injection for MCP server configs
- [ ] Linear cloud access — determine best REST API pattern for cloud instance access to Linear when MCP is unavailable

---

*See also: `VAULT-CONVENTIONS.md` § "Portable Path Standard (NETWEB)"*
