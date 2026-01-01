---
name: vault-accumulated-cruft
description: "Inventory of agent-generated sediment in IDAHO-VAULT — 223 stray branches, 8 custom ref namespaces, nested git repos committed as files. What the single rewrite is meant to collapse; do not knock it out casually before then."
metadata:
  node_type: memory
  type: project
---

Surveyed 2026-09-01 on the MacBook clone. This is the "mess" the convergence +
single-rewrite exists to end. None of it is on fire — gc is off, everything is
reachable, nothing is being lost — but it is a fuller map than earlier notes gave.
Logan's framing: Ozymandian. Each artifact is some session's "definitive" work,
none coordinated, the authors gone by the next session. Do not re-survey from
scratch; do not clean casually before the tree is unified and the rewrite runs.

**228 local branches, only 5 intended.** By group:
  claude/ codex/ mistral/ gemini/ opencode/   138   agents each cutting own branches
  dated / bot rollovers                         31
  add-* (one note per branch)                    8
  agent/ agent-*                                 4
  logan/obsidian/*  (THE real structure)         5   macos, windows, android, linux, main
  backup/ archive/ stash                         3
The 223 non-structure branches are the two-/windows-branches coordination failure
at scale — sessions branching instead of coordinating. See
[[agent-failure-patterns]].

**8 custom ref namespaces (not branches/tags — bare pointers keeping severed
history reachable):**
  refs/replace/*    7    the grafts (reparent to 2024-12-17 root; local-only). [[vault-history-grafts]]
  refs/recovered/*  93   rescue shelf, refs dated back to 2026-04-08
  refs/prespill/*   17   e.g. antigravity-pullman-oidc-pipeline
  refs/reunify/*    7    a reconnection pass
  refs/premerge/*   1    macos-20260828 -> 280064b3de (pre-merge anchor)
  refs/quarantine/* 1    quarantine/main -> 0adf56fd16
  refs/laf79/*      1    pr-compatible-candidate -> ecb3083e45
  refs/annex/*      1    last-index -> 4ef30a73fd
~120 rescue pointers from at least four separate recovery episodes. What travels
on push/clone is only refs/heads/* and refs/tags/*; ALL of these stay local
unless named explicitly in a refspec.

**Entire nested git repos committed AS TRACKED FILES inside the vault** (worse
than the loose .git-spill already cleaned from the working root):
  THE-GEMSTONE.gitdir/      full git dir — HEAD, packed-refs, logs/, refs/ all tracked
  .hermes/checkpoints/store/    HEAD, packed-refs tracked
  .local/share/opencode/snapshot/.../   opencode snapshot repos, same pattern
These are why a bare `HEAD` was ambiguous ("both revision and filename"). Any git
command using an unqualified ref name in this repo must use `--` or a full
refname. See [[vault-repo-hazards]].

**Two empty .env files at root:** .env and .env__src_the-gemstone__ca7db971,
both 0 lines. The `__src_...__` suffix is the doctrinal_flatten signature.

**Cross-machine artifacts that drifted (Mac paths on Windows, etc.):** tracked in
both clones because ~ dotfolders symlink into the vault. See
[[vault-as-home-symlinks]].

**The point:** the single rewrite bakes grafts into real parentage (history
becomes portable), lets these namespaces retire, dedups the 86.6% redundancy, and
collapses the 223 stray branches. The cruft is load-bearing scaffolding NOW —
that is why it stays until the rewrite — but the end state needs none of it.
Related: [[vault-order-of-operations]], [[vault-repo-hazards]], [[never-discard-vault-content]].
