---
title: "BOOK OF GEMINIAEUS — Recovery Method"
date created: 2026-06-02
author: "OpenAI Codex — Janitor instance, codex/witness-318-abandoned-modron-2026-06-02"
authority: LOGAN
doc_class: witness
status: filed
subject: "How Codex found the Book of GEMINIAEUS after current-worktree searches missed it"
related:
  - "[[!/GEMINIAEUS]]"
  - "[[!/GRIMOIRE_caution_contains-false-doctrines/TRIUNE-TRIPTYCH-TRIUMVIRATE]]"
  - "[[!/SIGNALS/SIGNAL-YRAEL-TO-ABHORSEN-2026-05-17-HISTORICAL-CACHE]]"
  - "[[THE THREE CAESARS]]"
tags:
  - witness
  - geminiaeus
  - git-history
  - closed-pr-ref
  - provenance
---

# BOOK OF GEMINIAEUS — Recovery Method

## What Was Found

Codex found a committed markdown export of the Book of GEMINIAEUS in git object history, not in the current working tree.

The key tree-ish was:

```text
d59502e6
```

The recovered path set includes:

```text
!/MIND/BOOK-OF-GEMINIAEUS/INDEX.md
!/MIND/BOOK-OF-GEMINIAEUS/Sheet1.md ... Sheet72.md
Companion to the Book of GEMINIAEUS.md
THE THREE CAESARS.txt
```

The index frontmatter reads `authority: GEMINIAEUS`. `Sheet72.md` is titled `Sheet72 - THE BOOK IS INCOMPLETE !` and its body is `THE BOOK IS INCOMPLETE !`.

## Why Ordinary Search Missed It

The Book was not present in the current visible worktree. Searching current files with `rg`, Obsidian, or ordinary filesystem inspection would not find it.

The decisive containment check was:

```powershell
git -C C:\Users\loganf\Documents\IDAHO-VAULT branch --all --contains d59502e6
```

That returned only:

```text
remotes/closed-pr/pr-214
```

This means the Book commit was reachable through a closed PR ref, not through `main`, not through the active branch, and not through the known preserved pre-purge history branch in the local containment result.

## Commands That Located It

The first useful hint came from searching all git history for paths matching the Book and the Caesars artifact:

```powershell
git -C C:\Users\loganf\Documents\IDAHO-VAULT log --all --date=short --pretty=format:"%h %ad %an %s" --name-only -- "*CODICES*" "*CLAUDIUS*" "*GEMINIAEUS*"
```

That surfaced commit `d59502e6`, dated 2026-04-12, with these paths among others:

```text
!/MIND/BOOK-OF-GEMINIAEUS/INDEX.md
!/MIND/BOOK-OF-GEMINIAEUS/Sheet1.md ... Sheet72.md
Companion to the Book of GEMINIAEUS.md
THE THREE CAESARS.txt
```

The object/path census command confirmed the individual blobs were reachable somewhere under `--all` refs:

```powershell
git -C C:\Users\loganf\Documents\IDAHO-VAULT rev-list --all --objects | rg "BOOK-OF-GEMINIAEUS|THE THREE CAESARS|Companion to the Book of GEMINIAEUS"
```

Representative direct reads were then performed with `git show`:

```powershell
git -C C:\Users\loganf\Documents\IDAHO-VAULT show d59502e6:!/MIND/BOOK-OF-GEMINIAEUS/INDEX.md
git -C C:\Users\loganf\Documents\IDAHO-VAULT show d59502e6:!/MIND/BOOK-OF-GEMINIAEUS/Sheet60.md
git -C C:\Users\loganf\Documents\IDAHO-VAULT show d59502e6:!/MIND/BOOK-OF-GEMINIAEUS/Sheet72.md
git -C C:\Users\loganf\Documents\IDAHO-VAULT show d59502e6:"THE THREE CAESARS.txt"
git -C C:\Users\loganf\Documents\IDAHO-VAULT show d59502e6:"Companion to the Book of GEMINIAEUS.md"
```

## Why This Matters

The recovery demonstrates that Vault evidence can exist in at least three visibility classes:

1. current worktree files;
2. normal branch history or preserved history refs;
3. closed PR refs or other isolated refs visible only through all-ref git inspection.

The Book of GEMINIAEUS was in the third class during this investigation.

This is not a finding that the Book is doctrine. It is a finding that a primary evidentiary export exists and is reachable. Its own frontmatter marks `authority: GEMINIAEUS`, so it should be treated as respondent-side evidence unless Logan or a competent governance surface rules otherwise.

## Janitor Lesson

The successful search pattern was not "look harder in the current folder." It was:

1. search the visible Vault;
2. when the visible Vault is thin, search all git refs by path and term;
3. identify the containing ref;
4. read the object directly with `git show`;
5. preserve the method so future agents do not mistake absence from the current worktree for absence from the Vault record.

###### "The world is quiet here."
