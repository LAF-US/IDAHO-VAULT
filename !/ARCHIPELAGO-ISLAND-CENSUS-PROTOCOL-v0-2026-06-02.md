---
title: ARCHIPELAGO - Island Census Protocol v0
date: 2026-06-02
status: draft
doc_class: protocol-companion
authority: LOGAN
directed_by: LOGAN
filed_by: Codex
companion_to:
  - ARBORSCAPE
related:
  - !/ARBORSCAPING-REPORT-2026-04-16.md
  - !/ARBORSCAPE-COMPLETION-REPORT-2026-05-17.md
  - !/ARBORSCAPING-INVESTIGATION-RETURN-2026-05-24.md
  - !/BOOK-OF-GEMINIAEUS-RECOVERY-METHOD-2026-06-02.md
---

# ARCHIPELAGO - Island Census Protocol v0

ARCHIPELAGO is a companion sibling to ARBORSCAPE.

ARBORSCAPE tends the visible branch landscape: branches, PR expansions, living worktrees, suspended branches, and cleanup decisions made under explicit authority.

ARCHIPELAGO counts islands before anyone declares the sea empty.

Its job is to census isolated or non-obvious work product in git history: closed PR refs, orphan lineages, no-merge-base branches, branch-only artifacts, preserved refs, and other named landmasses that current-worktree search cannot see.

This document is draft protocol. It records a working method directed by Logan. It does not amend the Constitution, promote itself into core governance, authorize deletion, or convert discovered text into doctrine.

## Trigger

Run ARCHIPELAGO when any of these conditions appear:

- A referenced artifact cannot be found in the current worktree.
- A visible witness points to older work product, rescue exports, sealed books, branch-only records, or closed PR material.
- ARBORSCAPE is considering deletion, pruning, or classification of a branch or PR ref.
- A branch has no merge base with main or otherwise behaves like a separate landmass.
- An agent is tempted to say an artifact does not exist after only current-tree search.

## Scope

ARCHIPELAGO inventories reachability and provenance. It answers:

- Which refs contain the artifact?
- Is the artifact current, ancestral, branch-only, closed-PR-only, orphaned, or unreachable by normal refs?
- What paths, commits, and containment evidence prove the answer?
- What should be read, preserved, quarantined, escalated, or ignored?

ARCHIPELAGO does not:

- delete branches;
- prune refs;
- rewrite history;
- bless discovered files as canonical;
- adjudicate doctrine;
- quote suspected secrets;
- override ARBORSCAPE, REPO-SLIMMING, constitutional governance, or Logan.

## Visibility Classes

Use these classes when reporting a census result:

- `CURRENT`: visible in the current checked-out tree.
- `ANCESTRAL`: reachable through main/current ancestry, but not currently checked out.
- `BRANCH-ONLY`: reachable through a named branch or remote branch, but not merged into main/current.
- `CLOSED-PR-ISLAND`: reachable only through a closed PR ref or similar isolated ref.
- `ORPHAN-LINEAGE`: ref has no merge base with main/current and must not be judged by ahead/behind counts alone.
- `PRESERVED-REF`: intentionally retained named ref, archive ref, or signal ref.
- `OBJECT-ONLY`: object discovered outside named refs. This is a forensic condition, not a normal ARCHIPELAGO target; route separately before relying on it.
- `ABSENT-AFTER-CENSUS`: not found after visible tree, all named refs, and relevant path/object searches were checked and recorded.

## Minimal Census Pass

A minimal ARCHIPELAGO pass records the exact commands run and their result classes.

Recommended command sequence:

```powershell
# 1. Search current tree first.
rg -n "TERM|PATH|ALIAS" .

# 2. Search all named refs by path and content-bearing object listing.
git log --all --date=short --pretty=format:"%h %ad %an %s" --name-only -- "*TERM*" "*PATH*"
git rev-list --all --objects | rg "TERM|PATH|ALIAS"

# 3. Identify containment for a discovered commit or object.
git branch --all --contains <commit>

# 4. Read without checkout when provenance matters.
git show <commit>:<path>

# 5. For candidate islands, test relationship to main/current.
git merge-base main <ref>
git ls-tree -r --name-only <ref>
```

If `git merge-base main <ref>` fails, do not describe the ref as merely ahead or behind. That is an island or foreign lineage until investigated.

## Census Row Schema

Each island census entry should include:

- `date`;
- `agent`;
- `search_terms`;
- `ref`;
- `commit_or_object`;
- `path`;
- `visibility_class`;
- `merge_base_with_main`;
- `unique_or_notable_paths`;
- `risk_class`;
- `commands_run`;
- `evidence_summary`;
- `recommended_next_action`.

Recommended next actions are limited to verbs like `read`, `preserve`, `index`, `quarantine`, `ask Logan`, `route to ARBORSCAPE`, `route to REPO-SLIMMING`, or `ignore with evidence`. Deletion is not an ARCHIPELAGO action.

## Risk Classes

Use risk labels before quoting or promoting contents:

- `EVIDENCE-CANDIDATE`: may matter as witness or historical record.
- `DOCTRINE-RISK`: found text may assert authority it does not possess.
- `SECRET-RISK`: possible credential, token, private data, or protected material. Stop quoting and route to secret handling.
- `GENERATED-JUNK`: likely generated residue or abandoned build product.
- `LIVING-WORK`: tied to an active worktree, active branch, or ongoing lane. Route to ARBORSCAPE.
- `REQUIRES-LOGAN`: disposition cannot be inferred safely by an agent.

## Example: Book of GEMINIAEUS

The Book of GEMINIAEUS was not found by current-worktree search. It was found by widening to all named refs and object/path listings.

Census entry:

- `date`: 2026-06-02
- `agent`: Codex
- `search_terms`: `BOOK-OF-GEMINIAEUS`, `THE THREE CAESARS`, `Companion to the Book of GEMINIAEUS`
- `ref`: `remotes/closed-pr/pr-214`
- `commit_or_object`: `d59502e6`
- `paths`: `!/MIND/BOOK-OF-GEMINIAEUS/INDEX.md`, `!/MIND/BOOK-OF-GEMINIAEUS/Sheet1.md` through `Sheet72.md`, `Companion to the Book of GEMINIAEUS.md`, `THE THREE CAESARS.txt`
- `visibility_class`: `CLOSED-PR-ISLAND`
- `risk_class`: `EVIDENCE-CANDIDATE`, `DOCTRINE-RISK`
- `recommended_next_action`: preserve recovery method, read by direct `git show`, do not adopt authority claims merely because the text exists.

The recovery method is recorded in `!/BOOK-OF-GEMINIAEUS-RECOVERY-METHOD-2026-06-02.md`.

## Doctrine Boundary

A found island is not a throne.

ARCHIPELAGO exists because useful and dangerous work product can survive outside the visible tree. Finding it proves reachability and provenance. It does not prove truth, authority, adoption, or fitness for live use.

The provenance and the performance of information are not the same layer.
