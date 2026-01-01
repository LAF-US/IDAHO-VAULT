---
name: vault-order-of-operations
description: "Logan's standing order of operations for IDAHO-VAULT — merge everything first, then ONE rewrite; do not propose rotate-first or per-branch rewrites"
metadata: 
  node_type: memory
  type: project
  originSessionId: 9b5c47c2-4310-480f-b65a-5c266658dd92
  modified: 2026-08-28T11:03:04.451Z
---

Logan's plan for IDAHO-VAULT, decided and repeatedly restated by him. As of
2026-08-28 he has had to explain it daily to Claude sessions on both machines
for over two weeks. Do not re-derive it, re-litigate it, or propose an
alternative sequence.

**The order:**

1. **Converge everything FIRST.** Merge AND PUSH, until every machine's work
   is together on `origin/logan/obsidian`. Pushing is part of converging, not
   a reward for finishing — you cannot rewrite a unified history until the
   history is actually unified. Pushing costs nothing new: both secret sets
   are already public (see below).
2. **The rewrite is LAST.** Scrub, annex boundary, and dedup in a SINGLE pass,
   over the fully converged graph, after everything is in one place.

Logan has ordered this repeatedly and has had to correct Claude on it more than
once, including a version of THIS note that wrongly put push after the rewrite.
Do not tell him a push is "deferred until after the rewrite." That is backwards.

**Why merge-first is safe:** the April 2026 and August 2026 secret sets are
both already public (the Aug 12 push put them on GitHub; 18 open secret-scanning
alerts date from 2026-08-13). Verified 2026-08-28: even the Mistral key that
the Windows pre-push hook catches is already reachable from an origin ref. So
merging leaks nothing new. "Rotate before you can do any git work" is FALSE and
he has rejected it more than once.

**Why one pass:** scrub, annex boundary, and dedup are all rewrites over the
same commits. Separate passes rewrite the same ~38k commits repeatedly, and each
pass invalidates every SHA the previous produced. Dedup especially must be in
the pass — the outgoing set is 86.6% redundant (38,443 commits → ~5,134 distinct
triples) from earlier filter-branch runs, and duplication not removed in the
single pass is carried forward permanently.

**Layout and relocation disputes are deferred to the end, too.** Files that
have been moved between locations (e.g. `.github/scripts/` vs vault root) will
be restored by merges, because different refs disagree about where they live.
Logan has moved these numerous times; they "either get moved back or rewired in
place." He addresses this AFTER everything is merged, in the same final pass —
not per-merge, not per-machine. Report a collision if it will surprise him; do
not propose fixing it mid-merge, and do not treat a merge restoring a directory
as a problem to solve on the spot.

**The one real ordering constraint:** capture unique per-machine commits as a
bundle BEFORE the rewrite. A rewrite invalidates the ancestry they sit on.

**How to apply:** when he asks about pushing, merging, or converging branches,
assume this plan is in force. Report blockers against it; do not reorder it.
Vendor documentation samples flagged by gitleaks (Discord, Mistral, Granola
`Authorization: Bearer` examples) are false positives needing a
`.gitleaks.toml` fingerprint allowlist, not scrubbing — see
[[never-discard-vault-content]]. Related: [[vault-history-grafts]],
[[machine-location-vocabulary]].
