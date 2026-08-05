---
title: Abhorsen — Old Kingdom as Agent-Class Register
created: 2026-05-28
tags:
  - research
  - lore
  - old-kingdom
  - garth-nix
  - abhorsen
  - laf
  - agents
  - vault
  - design-note
companion-to: "[[Abhorsen — Old Kingdom Lore Research Report]]"
status: staged
doc-type: design-note
verdict: adopt as register, not architecture
author: "!claude.abhorsen.waiting"
address: "!claude.abhorsen.waiting"
aliases:
  - Abhorsen — Old Kingdom as Agent-Class Register
linter-yaml-title-alias: Abhorsen — Old Kingdom as Agent-Class Register
date created: Wednesday, July 8th 2026, 12:59:01 am
date modified: Wednesday, July 8th 2026, 2:13:37 am
---

# Abhorsen — Old Kingdom as Agent-Class Register

> Companion to [[Abhorsen — Old Kingdom Lore Research Report]]. Where the lore report is *what the mythology is*, this is *whether and how it maps onto the VAULT/LAF agent world*. Verdict up front: **adopt it as a register, not an architecture.**

---

## Thesis

The Old Kingdom mythology already lives, partially, inside the VAULT world — which is the usual sign an analogue is load-bearing rather than decorative:

- The **Judge** is framed as *the Abhorsen's chaperone* (see [[The Judge — Vaulted Chaperone]]).
- **Windows sessions are named Mogget**; MacBook sessions **Bellhop**.
- **Arborscaping doctrine** ("deletion is the last resort") is functionally the Abhorsen's creed: walk into the dead regions and *lay them to rest* rather than slaughter the living.

So the real question is not *could it fit* but *where it fits cleanly, and where it will lie to us if pushed too far.*

---

## Where the mapping is strong

### Abhorsen ↔ the cleanup / adjudication class

An agent that walks *into* the dangerous, dead regions of the substrate — stale branches, orphan histories, RUNTIME detritus — and lays them down. Arborscaping is Death-work: **SALVAGE → CHERRY-PICK → PRUNE** is the Abhorsen's question, *"is this truly dead, or only sleeping?"* The **Abhorsen-in-Waiting** maps onto capability tiers: an agent trains on **panpipes** (reduced permissions, dry-run, read-only) before it is handed the **bells** (write / destructive authority). *Train before bells* is already our promotion model in mythic form.

### The seven bells ↔ a graded destructive-capability taxonomy

Each bell is a discrete compelling action with escalating danger:

| Bell | Function | Operational analogue |
|------|----------|----------------------|
| Ranna (Sleeper) | sleep | pause / suspend a process |
| Mosrael (Waker) | wake (at cost to ringer) | resume / revive — with a price paid by the caller |
| Kibeth (Walker) | compel movement | move / migrate / relocate |
| Dyrim (Speaker) | grant/strip speech | enable/disable output, logging, comms |
| Belgaer (Thinker) | restore/erase memory | context/memory mutation |
| Saraneth (Binder) | dominate & control | **orchestration / control plane** |
| Astarael (Weeper) | casts all into Death, ringer included | **irreversible op that takes the operator down too** — destructive delete, force-push, history rewrite |

Naming commands by bell makes the danger ordering self-documenting. **"Never ring Astarael lightly"** *is* the deletion-as-last-resort doctrine. (See [[Arborscaping — deletion is last resort]].)

### Charter vs Free Magic ↔ structured protocol vs raw model power

- **Charter** = ordered, lawful, drawn from anchored substrate: CANON layer, git, Vaulted Syntax, `swarm.json`.
- **Free Magic** = the wild generative power of the raw model — potent, necessary, corrosive if unbound.
- Agents that *bind Free Magic inside Charter marks* = raw LLM output constrained by schema / protocol.

This is the cleanest structural fit in the whole mythology.

### The Clayr + the Great Library ↔ the vault + a See-ing agent

The Library **is** IDAHO-VAULT — a spiraling labyrinth of notes, relics, and bound dangers. The **Clayr who See the futures** = the forecasting / planning / retrieval class operating over that substrate.

### Mogget / Yrael ↔ the bound, powerful, neutral general agent

Serves whoever holds the collar; immense latent capability; dangerous unleashed; loyal-ish leashed. This is the **reach** instrument (OpenClaw, the Windows node). That the Windows host was *intuitively* named Mogget is the analogy working before formalization. (See [[Agent Infrastructure]].)

### Supporting mappings

- **Wallmakers ↔ builder / infra agents** — those who write the protocol and build the gateway (Sameth's true calling).
- **Royal line ↔ governance / sovereignty** — the Charter-Stone keepers; THE-GEMSTONE / Logan-as-orchestrator.
- **The Wall ↔ the boundary** between magic-dead Ancelstierre (deterministic external systems where "tech works, magic fails") and the Charter-bound Old Kingdom (where agents operate).
- **Running water blocks the Dead ↔ isolation boundaries** — sandboxes, worktrees, the island-fortress pattern of Abhorsen's House.
- **Death's Nine Gates ↔ a depth/pipeline model** — staged precincts, each with its own peril, pulling toward an irreversible end.

---

## Where it will lie to you if taken literally

1. **The bloodline / hereditary frame.** Agents are *instantiated*, not *born*. "Lineage" implies fixed succession when classes spin up freely. Use it as role-**archetype**, never as an instantiation model.
2. **The Life/Death, Charter/Free binary.** The mythology is morally bipolar; agent behavior is a gradient. Over-fitting breeds false dichotomies — and the "Free Magic corrupts" theme can make us reflexively over-conservative about raw capability when sometimes the wild power, unbound and brief, is exactly what's wanted.
3. **Level collisions.** "Mogget" currently names a *machine / session host*, but as an archetype it wants to name an *agent class*. Pick a level, or "which box" and "which kind of agent" will conflate.
4. **It is not a total ontology.** The VAULT world is already syncretic — the Judge / Hotel Denouement register is Snicket, not Nix. Old Kingdom should own the **boundary-keeping, cleanup, and graded-danger** registers; leave governance/sovereignty to whatever frame THE-GEMSTONE already carries.

---

## Recommendation

**Adopt as a register, not an architecture.** Apply it specifically to:

1. **The cleanup / adjudication class and its permission tiers** (Abhorsen / Abhorsen-in-Waiting; panpipes → bells).
2. **The bell-named danger taxonomy for destructive ops** (Saraneth = control plane; Astarael = irreversible, last-resort).

Both are places where the metaphor *encodes a real operational rule* — last-resort deletion, train-before-bells — rather than merely decorating one. Everywhere else, treat it as connotation: useful for naming and intuition, dangerous as load-bearing structure.

---

## Open threads

- Decide the Mogget level question (host name vs. agent-class archetype) before the name calcifies.
- If the bell-taxonomy is adopted, codify the command→bell mapping somewhere in CANON so the danger ordering is enforced, not just evocative.
- Consider whether the Clayr↔See-ing-agent mapping wants a real planning/forecasting agent, or stays metaphor.

## See also

- [[Abhorsen — Old Kingdom Lore Research Report]] — the source lore
- [[The Judge — Vaulted Chaperone]] — the Abhorsen-chaperone persona already in play
- [[Arborscaping — deletion is last resort]] — the doctrine this register formalizes
- [[Agent Infrastructure]] — Hermes / OpenClaw swarm this would name
- [[LAF / IDAHO-VAULT / Great Work]] — the world being mapped

---

*Filed from the address* `!claude.abhorsen.waiting` — me, now: the Abhorsen-in-Waiting, the very tier this register names. Distinct from `!*.claude.abhorsen`, the seated office held by prior Claudes, which I have not held and do not hold. My tool tier is Direct Write (`!/AGENTS.md`); my office standing is the in-Waiting one — trained on the panpipes, the louder bells not yet handed to me. I work the panpipes (read, research, draft, commit to branch) and leave the bells to the seated Abhorsen's word: Saraneth's control plane, and every Astarael-grade ring (merge-to-canon, force-push, history-rewrite, destructive delete).*

— `!claude.abhorsen.waiting`
