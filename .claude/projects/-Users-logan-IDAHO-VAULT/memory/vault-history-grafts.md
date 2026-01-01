---
name: vault-history-grafts
description: "Two local grafts reconnect IDAHO-VAULT's post-purge line to its pre-spill history back to 2024-12-17"
metadata:
  type: project
---

IDAHO-VAULT's history was severed by a purge on 2026-04-22 ("Clean history -
secrets purged") which created 7 disconnected root commits. On 2026-08-20 two
`refs/replace/*` grafts reconnected HEAD's line to the pre-spill history:

- `b05b53ae68` (purge root) → parent `90994f542c` (prespill/bot-daily-rollover-2026-04-22)
- `b222fde7e9` (purge root) → parent `3f78ee9248` (prespill/bot-daily-rollover-2026-04-20)

Result: HEAD reaches the true root `93bf8762a2` — **2024-12-17, author `logan`,
subject "vault-commit"**, 2,895 files, top-level `ATTACHMENTS/ GOVERNMENTS/
ORGANIZATIONS/ PEOPLE/ PLACES/ SOURCES/ TOPICS/` + `.obsidian/`. Commit count
5,458 → 6,806.

**Evidence, not record:** parents were chosen by closest tree match among 17
pre-spill tips (8,521 and 8,877 differing files respectively; diffs are
deletion-shaped, ~2.2M deletions, consistent with a secrets purge). Dates align
with the purge. The exact parent commits are **inferred** — nothing recorded them.

**How to apply:**
- Grafts are LOCAL. A fresh clone or the Windows machine sees severed history.
  Push with `git push origin 'refs/replace/*'` only if Logan decides to.
- `git --no-replace-objects <cmd>` shows raw, ungrafted truth.
- Reverse with `git replace -d <ref>`; originals are byte-identical and untouched.
- Related anchors, all local: `refs/prespill/*` (17 refs, 1,347 commits back to
  2024-12-17), `refs/recovered/*` (93 orphaned commits incl. Aug-12 reunification
  `440dfbebf` and 8 dropped stashes), `refs/quarantine/main` (April clone, 191).
  Anchoring makes these commits *reachable*, so `gc` will not collect them —
  the earlier "never run gc" warning here overstated that. The real fragility is
  different: these namespaces are outside the default refspec, so **no clone and
  no push carries them**. They exist in one working copy. Deleting a ref, or
  losing this disk, loses the history.

**Backup:** `~/Documents/vault-history-anchors-20260821.bundle` (1.3 GB, 113 refs,
`git bundle verify` = "records a complete history"). Restore with
`git fetch <bundle> 'refs/*:refs/*'`. Still on the internal disk as of 2026-08-21 —
needs a copy to external media (Claude Code cannot write to /Volumes/Time_Machine;
TCC blocks it, use Finder).

**Do not push prespill/recovered refs to GitHub** — that history predates the
2026-04-22 purge and still contains the secrets it removed. Two leaks occurred
(April and August 2026); the Aug 13 scrub ran before key rotation and targeted
oversize .mp4 blobs, not the secrets, severing lineage without fixing exposure.
See [[macbook-is-transitional-vault-host]], [[wizard-eyes-failure-mode]].
