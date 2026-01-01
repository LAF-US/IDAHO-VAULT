---
name: idaho-vault-storage-architecture
description: "IDAHO-VAULT's three-tier storage (git/LFS/annex), the per-clone LFS re-pin requirement, and the vault-as-home symlink pattern"
metadata: 
  node_type: memory
  type: project
  originSessionId: 9b5c47c2-4310-480f-b65a-5c266658dd92
  modified: 2026-08-18T02:32:14.200Z
---

IDAHO-VAULT (github.com/LAF-US/IDAHO-VAULT, branch logan/obsidian) runs three storage tiers in one repo, wired 2026-08-17:

- **git**: everything by default; markdown force-tracked via `!/**.md` — markdown must NEVER be annexed (locked annex files are read-only symlinks; breaks Obsidian).
- **LFS**: media extensions per `.gitattributes` (`*.mp4`, `*.mov`, `*.jpg`, `*.bin`, etc.). Content on GitHub's LFS store.
- **annex**: git-annex 10.20260717 **standalone build** at `~/.local/opt/git-annex.app` (symlinked into `~/.local/bin`). Homebrew build fails on macOS 12 (no ghc bottle; Cabal-7125). Repo uuid `9dd2465d…`, name `idaho-vault-mac`. `annex.largefiles` deliberately UNSET = explicit-only (`git add` → git/LFS; only `git annex add` annexes). No special remotes yet — annexed content is local-only until one is added.

**Critical per-clone step**: `git annex init` writes `* filter=annex` to `.git/info/attributes`, which outranks tracked `.gitattributes` and hijacks LFS. Fix (done on the Mac clone, must be repeated in every new clone): append the LFS `filter=lfs` lines AFTER the annex wildcard in `.git/info/attributes`. Verify with `git check-attr filter -- x.mp4 x.md` (expect lfs / annex-passthrough).

**Vault-as-home**: `~/.ssh`, `~/.npm`, `~/.local`, `~/.cache`, `~/.zsh_sessions`, `~/.temp` are symlinks INTO the vault; real data lives in the repo. Inverted/self-referential links (e.g. `repo/.local/.local -> ~/.local`) create 2-node cycles that break git pull — six were removed 2026-08-17; watch for their return. Related origin: Logan used Windows `mklink /J` junctions and some paths got inverted on the Mac side.

**Standing hazard**: a "sloppy agent" on Logan's Windows machine pushes commands over SSH (password auth; Remote Login intentionally left on). It has caused mass root-file deletions (2,082 files, restored from HEAD) and possibly the unexplained `id_ed25519 copy` keypair (created Aug 12). Mass `D` entries in git status = its fingerprint; content is always recoverable from HEAD.

macOS 12 + Homebrew 6: unsupported tier, bottles largely gone, installs fall back to hours-long source builds. `python3`/`pip3` were relinked to Homebrew `python@3.14` (was python.org 3.13; reversal targets in that session's scratchpad notes).
