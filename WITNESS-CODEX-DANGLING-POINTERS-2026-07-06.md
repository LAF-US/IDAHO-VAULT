---
authority: LOGAN
agent: Codex
status: staged
date: 2026-07-06
related:
  - AGENTS
  - CONSTITUTION
  - WAKEUP
  - VAULT-CONVENTIONS
  - swarm
---

# WITNESS: Codex Dangling Pointers

## Scope

This witness records a broader debt class observed after the initial
`!/WAKEUP.md` path-drift witness.

The finding is not "one broken link." It is a family of dangling pointers across
Markdown governance, generated registries, Python packaging assumptions, and
historical compatibility reports.

No repairs were made in this pass.

## Definition

A dangling pointer is any reference that claims a routable file, folder, package,
registry, launcher, surface, or authority path, where the referenced target is
missing, flattened, renamed, archived, superseded, or otherwise no longer present
at the named location.

Not every dangling pointer is wrong in the same way. Some are historical
evidence. Some are compatibility shims waiting to be restored. Some are stale
machine assumptions that break execution.

## First Inventory: Wakeup And Swarm Routing

Observed targets:

| Pointer | Current state | Nearby survivor |
| --- | --- | --- |
| `!/WAKEUP.md` | missing | `WAKEUP.md`, `!-WAKEUP.md` |
| `!/AGENTS.md` | missing | `AGENTS.md`, `!-AGENTS.md` |
| `!/agents.json` | missing | `agents.json`, `!-agents.json` |
| `!/CREWAI` | missing | `!-CREWAI-*` flattened files |
| `!/README.md` | present | n/a |

Load-bearing references found:

- `AGENTS.md` directs disoriented agents to `!/WAKEUP.md`.
- `WAKEUP.md` still names `!/WAKEUP.md` in precedence and canonical startup
  language.
- `swarm.json` names `!/WAKEUP.md` as `wakeup_protocol.quick_start`.
- `swarm.json` names `!/WAKEUP.md` and `!/AGENTS.md` in boot order and conflict
  precedence.
- `.github/scripts/generate_agents_bootstrap.py` renders optional context
  entries for `!/WAKEUP.md` and `!/AGENTS.md`, and defaults its generated output
  to `!/agents.json`.

Reading: this looks like post-flattening routing debt. The nest still exists,
but several expected nest surfaces were flattened to `!-` files while generated
and governance surfaces kept pointing at the old nest addresses.

## Second Inventory: Python Package Topology

The checkout has flattened package files but many active or semi-active surfaces
still expect the old `src/idaho_vault/` package tree.

| Expected pointer | Current state | Flattened survivor |
| --- | --- | --- |
| `src/idaho_vault/crew.py` | missing | `src-idaho_vault-crew.py` |
| `src/idaho_vault/bootstrap_contract.py` | missing | `src-idaho_vault-bootstrap_contract.py` |
| `src/idaho_vault/main.py` | missing | `src-idaho_vault-main.py` |
| `src/idaho_vault/runtime.py` | missing | `src-idaho_vault-runtime.py` |
| `src/idaho_vault/config/agents.yaml` | missing | `src-idaho_vault-config-agents.yaml` |
| `src/idaho_vault/config/tasks.yaml` | missing | `src-idaho_vault-config-tasks.yaml` |

Load-bearing symptoms:

- `pyproject.toml` still declares console scripts like
  `idaho_vault = "idaho_vault.main:run"`.
- `pyproject.toml` still lists package inclusion as `src/idaho_vault`.
- `scripts-validate_bootstrap.py --format json` fails immediately with
  `ModuleNotFoundError: No module named 'idaho_vault'`.
- `bootstrap_contract.py` and `src-idaho_vault-bootstrap_contract.py` still
  check for old `src/idaho_vault/...` paths.

Reading: this is probably not only documentation drift. It affects executable
local validation and likely any command path relying on the package import name.

## Triage Categories

1. **Historical pointer:** leave as record; optionally annotate if it keeps
   misleading current agents.
2. **Routing pointer:** restore a small shim at the old address if governance
   still wants that address to be canonical.
3. **Generated pointer:** update source registry/generator first, then regenerate
   mirrors.
4. **Executable pointer:** repair import/package topology or script assumptions
   before touching reports.
5. **Bulk prose pointer:** inventory separately; avoid rewriting historical
   journalism, PR records, or witness text as if every old path claim were live.

## Suggested Next Safe Thread

Start with the wakeup/swarm routing cluster because it is narrow and central:
restore `!/WAKEUP.md`, `!/AGENTS.md`, and `!/agents.json` as explicit routing
shims or generated mirrors only after Logan approves the intended current
canonical address.

Handle the Python package topology as a separate code repair. Its blast radius is
larger because `pyproject.toml`, imports, tests, and local commands all agree or
disagree together.

## State

`staged`: a bounded inventory seed, not a canonical repair plan.
