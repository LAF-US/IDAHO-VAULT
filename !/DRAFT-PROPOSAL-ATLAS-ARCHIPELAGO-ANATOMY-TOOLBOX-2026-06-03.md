---
title: "DRAFT Proposal - ATLAS, ARCHIPELAGO, and ANATOMY Toolbox"
date created: 2026-06-03
authority: codex
doc_class: proposal
status: draft
related:
  - LAF-US-VAULT
  - ATLAS
  - ARCHIPELAGO
  - ANATOMY
  - ARBORSCAPE
  - "!/ARCHIPELAGO-ISLAND-CENSUS-PROTOCOL-v0-2026-06-02.md"
  - "!/WITNESS-CODEX-2026-06-02-BOOK-OF-GEMINIAEUS-AND-ARCHIPELAGO.md"
  - "!/BOOK-OF-GEMINIAEUS-RECOVERY-METHOD-2026-06-02.md"
  - "!/ARBORSCAPE-COMPLETION-REPORT-2026-05-17.md"
  - "VAULT-CONVENTIONS.md"
---

# DRAFT Proposal - ATLAS, ARCHIPELAGO, and ANATOMY Toolbox

*Filed 2026-06-03 for Logan's review. Draft only. Not live doctrine.*

## Summary

This proposal defines a three-part navigation and interpretation toolbox for the LAF-US-VAULT:

- `ATLAS`: interpretive charter for reading the Vault as a distributed terrain of current surfaces, islands, ruins, quarantines, artifacts, routes, and hazards.
- `ARCHIPELAGO`: operational island census for finding and classifying work product outside the visible current tree.
- `ANATOMY`: structural dissection method for examining an artifact, system, document, capture, protocol, or bundle after it has been found.

This proposal does not adopt the toolbox. It proposes names, boundaries, and initial responsibilities so Logan can decide whether to promote any part of it.

## Origin

The immediate trigger was the discovery of the Book of Geminiaeus.

The Book was not visible in the current Vault tree. It was found on a closed PR ref island, `remotes/closed-pr/pr-214`, at commit `d59502e6`. A current-tree search could therefore truthfully find nothing visible while still producing a false absence claim if it concluded that the Book did not exist.

The recovery method was recorded in `!/BOOK-OF-GEMINIAEUS-RECOVERY-METHOD-2026-06-02.md`. A witness of the lesson was recorded in `!/WITNESS-CODEX-2026-06-02-BOOK-OF-GEMINIAEUS-AND-ARCHIPELAGO.md`.

The lesson was not merely technical. It exposed a recurring agent failure:

> Agents confuse the visible mainland with the whole map.

This toolbox proposal responds to that failure.

## Proposed Terms

### ATLAS

`ATLAS` is an interpretive charter.

It establishes the reading frame for the LAF-US-VAULT as a mapped imaginative and provenance-bearing terrain. The working syncretism is the Archipelago-of-Dreams / Imaginarium Geographica lens: the Vault contains places whose current visibility, historical reachability, narrative force, and authority status are not the same thing.

ATLAS should teach agents how to read the terrain before acting on it.

It should distinguish:

- mainland from island;
- route from destination;
- discovery from adoption;
- provenance from authority;
- witness from doctrine;
- ruin from live structure;
- quarantine from canon;
- map from governance.

ATLAS is not a protocol. It does not execute searches, authorize cleanup, amend the Constitution, or promote discovered material. It explains the map.

### ARCHIPELAGO

`ARCHIPELAGO` is an operational census protocol.

It exists to prevent false absence claims. When a referenced artifact cannot be found in the current tree, ARCHIPELAGO requires an island census across the relevant git surfaces before an agent says the artifact is missing.

ARCHIPELAGO should handle:

- current worktree search;
- current branch history;
- all named refs;
- remote refs;
- closed PR refs;
- branch-only commits;
- no-merge-base lineages;
- preserved refs;
- direct historical reads with `git show`;
- containment checks with `git branch --all --contains`;
- classification of visibility and risk.

ARCHIPELAGO produces evidence rows: ref, commit, path, visibility class, risk class, commands run, evidence summary, and recommended routing.

ARCHIPELAGO does not delete, prune, rewrite, bless, or adjudicate. It counts islands before anyone says the sea is empty.

### ANATOMY

`ANATOMY` is a structural dissection method.

After ATLAS frames the terrain and ARCHIPELAGO finds an island, ANATOMY examines a specific artifact or system. It asks what the thing is made of, how its parts relate, where its scars and dependencies are, and what should be preserved, repaired, quarantined, ignored, or escalated.

ANATOMY should handle:

- mysterious files or bundles;
- generated captures;
- doctrine documents with mixed layers;
- toolchains;
- agent-produced artifacts;
- protocol or charter drafts before adoption;
- repo subsystems;
- recovered books, shards, indexes, companions, and exports.

ANATOMY asks:

- What are the visible parts?
- What are the hidden or embedded parts?
- What does each part do?
- What depends on what?
- What is live tissue versus scar tissue?
- What is generated residue?
- What is provenance-bearing?
- What is dangerous to touch?
- What is missing?
- What signs show corruption, hallucination, grafting, or false authority?
- What routing is justified by evidence?

ANATOMY does not itself adopt, delete, or canonize the thing examined. It produces a dissection report for Logan or the relevant governance surface.

## Relationship to ARBORSCAPE

`ARBORSCAPE` remains branch and worktree stewardship.

ARBORSCAPE tends branches, PRs, living worktrees, suspended lines, pruning candidates, and cleanup decisions. Its prior reports warn that branch cleanup must respect worktrees, merge-base failures, suspended states, and Logan's authority.

This proposal does not replace ARBORSCAPE.

The clean division is:

| Tool | Role | Primary Question |
| --- | --- | --- |
| ATLAS | Interpretive charter | What kind of mapped terrain are we in? |
| ARCHIPELAGO | Island census protocol | What exists outside the visible mainland, and how is it reachable? |
| ANATOMY | Structural dissection method | What is this artifact or system made of, and what does that imply? |
| ARBORSCAPE | Branch/worktree stewardship | What branch, PR, or worktree action is legitimate? |

## Proposed Terrain Vocabulary for ATLAS

ATLAS could define initial terrain terms like:

- `Mainland`: current checked-out Vault, visible live surfaces, current branch files.
- `Island`: reachable work product outside the visible current tree.
- `Closed-PR Island`: closed PR ref containing committed but unmerged work product.
- `Orphan Lineage`: branch or ref with no merge base with current main.
- `Ruins`: old structures that explain lineage but are not live governance.
- `Quarantine Isle`: preserved dangerous, false-doctrine, or contaminated material.
- `Shoal`: partial fragment, misleading filename, stale README, or low-depth residue that can ground an agent if mistaken for land.
- `Wreck`: failed run, broken export, interrupted work product, or abandoned branch artifact.
- `Route`: citation path, ref containment, branch ancestry, recovery method, or direct object read.
- `Storm`: tool failure, sandbox boundary, context loss, secret-guard incident, or stale assumption.
- `Chart`: witness note, recovery note, census row, or report that records how terrain was found.

These terms should stay interpretive unless separately promoted into an operational protocol.

## Proposed Workflow

A disciplined agent encountering a referenced but missing artifact should proceed:

1. `ATLAS`: identify what kind of terrain claim is being made.
2. `ARCHIPELAGO`: census the relevant islands before declaring absence.
3. `ANATOMY`: dissect any recovered artifact before interpreting it.
4. `ARBORSCAPE` or other surface: route branch, PR, cleanup, quarantine, or governance action.

The default warning remains:

> Discovery is not adoption.

Finding a document proves that the document exists at a path, commit, ref, or surface. It does not prove that the document is true, safe, current, constitutional, canonical, or authoritative.

## Non-Goals

This proposal does not:

- amend `CONSTITUTION.md`;
- promote ATLAS, ARCHIPELAGO, or ANATOMY into live core protocol;
- modify `PROTOCOLS.md`;
- rename existing ARBORSCAPE documents;
- authorize branch deletion or pruning;
- classify the Book of Geminiaeus as doctrine;
- treat literary syncretism as governance authority;
- create a live coordination surface.

## Open Questions for Logan

1. Should ATLAS be a standalone interpretive charter file, or a section under a broader map/cartography document?
2. Should ARCHIPELAGO remain draft protocol until tested on additional islands?
3. Should ANATOMY be a protocol, a procedure, a report template, or a looser method note?
4. Should the Imaginarium Geographica / Archipelago-of-Dreams syncretism be explicit in the title, or held in the body as interpretive scaffolding?
5. What promotion path should move a draft proposal into live doctrine without repeating the INBOX failure mode?

## Proposed Next Artifacts if Approved

If Logan approves the direction, the next files could be drafted separately:

- `!/ATLAS-INTERPRETIVE-CHARTER-v0-YYYY-MM-DD.md`
- `!/ARCHIPELAGO-ISLAND-CENSUS-PROTOCOL-v1-YYYY-MM-DD.md`
- `!/ANATOMY-STRUCTURAL-DISSECTION-METHOD-v0-YYYY-MM-DD.md`

Each should carry explicit status, authority, scope, non-goals, and promotion conditions.
