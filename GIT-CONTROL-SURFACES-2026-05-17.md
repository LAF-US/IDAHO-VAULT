---
title: "Git Control Surfaces - Chronology and Policy"
date: 2026-05-17
status: active
authority: LOGAN
related:
  - .gitignore
  - .gitattributes
  - Git LFS
  - LAF-USB-OBJECT-MANIFEST-2026-05-08
  - HANDOFF-LFS-2GB-BLOCK-2026-05-08
  - LEVELSET-LFS-SHUTDOWN-2026-05-06
---

# Git Control Surfaces - Chronology and Policy

This note records the operating frame for `.gitignore`, `.gitattributes`,
Git LFS, and external object manifests in IDAHO-VAULT.

These files are control surfaces, not convenience filters. Treat `.gitignore`,
`.gitattributes`, `.githooks/`, and `.git/` state with respect and explicit
review. Do not use them as pressure valves during a dirty working-tree crisis.

## Principle

The vault records by default.

Exceptions must be explicit:

- secrets and credentials stay out of Git
- runtime caches and generated local state stay out of Git
- machine-local UI state stays out of Git
- source documents stay visible unless Logan explicitly routes them elsewhere
- over-limit payloads use external object manifests, not Git or Git LFS

## Chronology

The current state is not a clean design born all at once. It is a sequence of
attempts and corrections.

1. Earlier `.gitignore` policy kept broad binary/media/document classes out of
   Git to preserve repo mobility.
2. A later `.gitignore` refactor reopened binary source-document classes so
   vault source material could become visible to Git again.
3. `.gitattributes` / Git LFS then became the mitigation: track source
   documents, but route large binary classes through LFS.
4. That mitigation failed for 38 files above GitHub's hard 2 GB per-object LFS
   ceiling.
5. The current post-failure policy is: payloads over the GitHub LFS ceiling are
   external objects. They require manifest records, not Git objects and not LFS
   objects.
6. Later reconciliation and rebase work changed some commit identities. Handoff
   notes may name local or pre-reconciliation hashes. Read them as historical
   evidence, then verify against the currently reachable Merkle graph.

## Current Surfaces

`.gitignore` is a visibility gate. It should hide secrets, runtime/cache churn,
machine-local state, and explicitly private holding lanes. It should not hide
possible future source material just because the name is inconvenient.

`.gitattributes` is transport policy. It can route sub-limit binary source
documents through LFS, but it is not a universal large-file solution.

`.github/scripts/check_large_files.py` is current enforcement policy:

- files above 100 MB require LFS attributes
- files above GitHub's hard LFS ceiling require external storage and a vault
  note or manifest reference

`LAF-USB-OBJECT-MANIFEST-2026-05-08.json` is the current registry for the 38
known over-limit objects. Its status and routing fields are part of the
post-failure recovery path.

`.githooks/pre-commit` and `.githooks/pre-push` are guardrails. Do not bypass
them to make a blocked push succeed.

## Agent Rules

Agents must not:

- disable hooks or checks to make Git operations pass
- bypass LFS as a workaround
- remove files from history without Logan's explicit instruction
- run competing pushes while another tool is pushing
- treat `.gitignore` edits as harmless housekeeping
- treat `.gitattributes` edits as routine formatting

Agents should:

- preserve chronology when explaining Git state
- distinguish historical hashes from currently reachable hashes
- check handoff notes and the Merkle graph before acting
- prefer narrow, anchored ignore rules
- document why a Git control-surface rule exists
- ask Logan before destructive, history-rewriting, or transport-policy changes

## Pending Cleanup Frame

The 2026-05-17 `.gitignore` review identified several broad convenience rules
that could hide future source material:

- blanket source lockfile ignore via `*.lock`
- unanchored `build/` and `dist/`
- unanchored `BMO/` and `Tags/`
- unanchored private-lane patterns

The safe direction is to narrow those rules so future source material remains
visible by default. That cleanup should be committed only with this chronology
in mind.

###### The world is quiet here.
