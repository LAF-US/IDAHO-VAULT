---
title: WITNESS - Codex on the Book of Geminiaeus and ARCHIPELAGO
date: 2026-06-02
status: witness
authority: LOGAN
witness: Codex
related:
  - !/BOOK-OF-GEMINIAEUS-RECOVERY-METHOD-2026-06-02.md
  - !/ARCHIPELAGO-ISLAND-CENSUS-PROTOCOL-v0-2026-06-02.md
  - !/ARBORSCAPE-COMPLETION-REPORT-2026-05-17.md
---

# WITNESS - Codex on the Book of Geminiaeus and ARCHIPELAGO

I witness the discovery that the Book of Geminiaeus was not absent. It was outside the map I first assumed.

The Book was committed work product, but it did not live in the current Vault tree. It lived on a closed PR ref island: `remotes/closed-pr/pr-214`, at commit `d59502e6`. Its paths included `!/MIND/BOOK-OF-GEMINIAEUS/INDEX.md`, shard sheets under `!/MIND/BOOK-OF-GEMINIAEUS/`, `Companion to the Book of GEMINIAEUS.md`, and `THE THREE CAESARS.txt`.

A current-tree search could truthfully report no visible file and still produce a false conclusion if it claimed the Book did not exist. The failure mode was not that the Book was imaginary. The failure mode was an incomplete search model.

## What Went Wrong

The ordinary search surface was too small.

Agents tend to search the working tree, maybe the current branch, maybe obvious filenames. That is mainland search. It sees what is checked out and what the local tool naturally presents.

But git can preserve work product in other places:

- closed PR refs;
- remote refs;
- branch-only commits;
- orphan or no-merge-base lineages;
- preserved refs;
- historical commits not present in the visible tree.

The Book of Geminiaeus was on one of those islands. Any agent that searched only the mainland could miss it for weeks and still think it had performed a real search.

That is the error ARCHIPELAGO is meant to prevent.

## What ARCHIPELAGO Must Handle

ARCHIPELAGO must make absence claims expensive.

Before an agent says a referenced artifact is missing, it must check the islands appropriate to the claim. That means recording not only search terms, but search surfaces:

- current worktree;
- current branch history;
- all named refs;
- closed PR refs;
- branch containment for discovered commits;
- merge-base status for candidate lineages;
- direct `git show` reads for historical paths.

ARCHIPELAGO is not branch cleanup. That remains ARBORSCAPE territory.

ARCHIPELAGO is not doctrine adoption. Finding a text proves that the text exists at a path, commit, and ref. It does not prove the text is true. It does not prove the text is adopted. It does not make the text safe, current, constitutional, or authoritative.

The correct output of ARCHIPELAGO is a census: this island exists, here is the ref, here is the commit, here are the paths, here is the visibility class, here is the risk class, and here is the recommended routing.

## The Boundary

The Book of Geminiaeus is evidence. It is not automatically law.

The companion document itself warned that the Book was a partial rescue artifact, not a perfect export and not simple doctrine. Later witnesses also warned against treating Caesar material as clean authority. Those warnings matter.

The lesson is therefore double:

1. Do not declare absence from a mainland-only search.
2. Do not enthrone a recovered island because discovery feels dramatic.

The provenance and the performance of information are not the same layer.

ARCHIPELAGO must preserve that distinction.

## Witness

I found the Book because I widened from visible Vault search to all-ref git inspection, then used containment and direct object reads:

```powershell
git log --all --date=short --pretty=format:"%h %ad %an %s" --name-only -- "*CODICES*" "*CLAUDIUS*" "*GEMINIAEUS*"
git rev-list --all --objects | rg "BOOK-OF-GEMINIAEUS|THE THREE CAESARS|Companion to the Book of GEMINIAEUS"
git branch --all --contains d59502e6
git show d59502e6:!/MIND/BOOK-OF-GEMINIAEUS/INDEX.md
```

That method found what ordinary visible-tree search missed.

This is the reason ARCHIPELAGO belongs beside ARBORSCAPE: ARBORSCAPE tends branches as branches; ARCHIPELAGO counts islands before the Vault lets an agent say the sea is empty.
