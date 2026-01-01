# Repair the corrupt pack in IDAHO-VAULT

## Context

A single object in one pack of the MacBook clone is corrupt and has been for
days. It broke a `git fetch` from this repo (Windows aborted on it) and keeps
`git fsck` dirty. Cause: this Mac's disk was filled to 180 MiB free on 2026-08-28
while pushes were repacking, and a pack written during that out-of-disk window
got one object's zlib stream damaged.

- **Corrupt pack:** `.git/objects/pack/pack-37e2012216245ebc0a8cf29fe48ed11a31bce527.pack` (14 GiB) + its `.idx`
- **Corrupt object:** blob `89f439b3fae553ff685afcd5bb8b9813462c98ab` (6,862,398 bytes), at pack offset 15290714236. `git cat-file -p` on it fails: "inflate: data stream error (incorrect data check)".
- **Why it can't just be deleted:** the pack holds **100,168 objects, and zero of them exist in any of the other 1,015 packs.** Removing the pack orphans all of them. Only this one object is actually damaged; the other 100,167 read fine (that's why Windows' fetch got 229 branches across before tripping).
- **Why the obvious fix failed already:** `git hash-object -w` is inert while the pack is in place — git resolves via pack indexes first, sees the SHA listed, and writes nothing. The pack must stop being authoritative before a good copy can take effect.
- **Good copy source:** the Windows clone (`logan-zbfury`) has a clean copy — verified earlier: 6,862,398 bytes, sha256 `687f00c95dad97468dace6787f464392a31239ca3c67086db444bcd58e18b62e`, `git hash-object` → the exact needed SHA. The earlier delivered copy in `/tmp` was cleared by reboots and must be re-fetched.

Intended outcome: `git fsck --full` clean, the object readable, no history lost,
the 7 replace grafts and all other refs untouched.

## Preconditions (verify before starting)

- `gc.auto=0`, `gc.autoDetach=false`, `maintenance.auto=false`, `gc.pruneExpire=never` — all currently set; keep them. An auto-repack mid-repair is the exact failure that caused this. (See memory `vault-repo-hazards`.)
- Free disk ≥ ~40 GiB. Currently ~122 GiB. Unpacking a 14 GiB pack to loose objects needs headroom (loose is less delta-compressed; budget 15–25 GiB transient).
- No other git operation runs against this repo during the fragile window (steps 3–5), because 100,168 objects are temporarily "missing" then.
- The LAN link to Windows is up (Windows reachable, this Mac at `10.253.163.216`, key installed) so the good blob can be re-fetched.

## Why not "just get it from Windows"

Windows has the *objects* but not this pack file, and the link is push-only (the
Mac cannot pull from Windows). Git also can't replace one object inside a pack —
the whole pack must leave the store, orphaning all 100,168 at once. So the fix
splits by what each source can cheaply provide:

- **The 1 corrupt blob** — genuinely destroyed locally; only Windows has a clean
  copy. 6.8 MB over scp (proven earlier). This is the "get it from Windows" part.
- **The other 100,167** — still readable in the local pack; `git unpack-objects`
  recovers them locally in one step, for free, and crucially preserves any
  Mac-only objects Windows may not have. Re-sending ~14 GB from Windows would be
  slower, needs a working push (currently broken), and could miss Mac-only data.

## Procedure

### 1. Re-fetch the good blob from Windows (prerequisite)
On the Windows side (it has the object):
```
git cat-file -p 89f439b3fae553ff685afcd5bb8b9813462c98ab > 89f439b3.blob
certutil -hashfile 89f439b3.blob SHA256      # expect 687f00c9...
scp 89f439b3.blob logan@10.253.163.216:/Users/logan/IDAHO-VAULT/../89f439b3.blob
```
Land it at a path that is NOT inside the vault working tree (e.g.
`/Users/logan/89f439b3.blob` or the session scratchpad) so it is never swept
into a commit. On this Mac, verify before use:
```
shasum -a 256 <blob>            # must equal 687f00c9...5e18b62e
git hash-object <blob>          # must equal 89f439b3fae553ff685afcd5bb8b9813462c98ab
```
Do not proceed unless both match.

### 2. Archive the corrupt pack out of the object store (also the backup)
```
mkdir -p /Users/logan/IDAHO-VAULT-repair-20260902/corrupt-pack
mv .git/objects/pack/pack-37e2012216245ebc0a8cf29fe48ed11a31bce527.pack /Users/logan/IDAHO-VAULT-repair-20260902/corrupt-pack/
mv .git/objects/pack/pack-37e2012216245ebc0a8cf29fe48ed11a31bce527.idx  /Users/logan/IDAHO-VAULT-repair-20260902/corrupt-pack/
```
Move BOTH files together, to a location outside the vault. This starts the
fragile window: git now sees 100,168 objects as missing. It is fully reversible
— moving both files back restores the prior state exactly.

### 3. Write the good base object loose (now that no pack claims it)
```
git hash-object -w /Users/logan/89f439b3.blob    # writes now; verify it returns 89f439b3...
```
Doing this BEFORE the unpack makes the good base available so any objects stored
as deltas against it resolve during recovery.

### 4. Recover the other 100,167 objects from the archived pack
```
git unpack-objects -r < /Users/logan/IDAHO-VAULT-repair-20260902/corrupt-pack/pack-37e2012216245ebc0a8cf29fe48ed11a31bce527.pack
```
`-r` (recover) unpacks every readable object as loose and continues past the one
corrupt entry instead of dying on it. unpack-objects skips objects already
present, so the good blob from step 3 is preserved. Expect this to be SLOW on
this machine (100k objects) — run it in the background with a disk monitor, the
same pattern used for the transfer watch; stop if free space falls under ~15 GiB.

### 5. Verify integrity
```
git fsck --full --no-progress 2>&1 | tee /Users/logan/fsck-after-repair.log
git cat-file -p 89f439b3fae553ff685afcd5bb8b9813462c98ab | wc -c   # expect 6862398
```
Expected: 0 missing, 0 corrupt. Dangling objects are normal and fine.
- If fsck reports **missing** objects — these are delta-dependents whose base
  was the corrupt entry and couldn't be recovered. Fetch each missing SHA from
  Windows the same way as step 1, `git hash-object -w` it, re-run fsck. Windows
  holds the full history, so any gap is recoverable.
- If fsck reports **corrupt** — stop and reassess; do not repack.

### 6. Repack the recovered loose objects (only after a clean fsck)
```
git repack -d
```
`repack -d` consolidates reachable loose objects into a fresh clean pack and
drops now-redundant packs. **`-d` only — never `git gc` and never a prune here**:
the 7 `refs/replace` grafts and ~114k dangling objects must not be pruned (see
memory `vault-history-grafts`, `vault-accumulated-cruft`). Leaving the objects
loose instead is also acceptable if any doubt remains — correctness does not
require the repack, it is only tidiness/performance.

### 7. Disposition of the archived corrupt pack
Keep `IDAHO-VAULT-repair-20260902/corrupt-pack/` until fsck is confirmed clean
and has stayed clean across a session. Per the standing "never discard vault
content" rule, do not delete it reflexively — its 100,167 good objects are now
recovered into the repo, so it is genuinely redundant, but archive rather than
delete and let Logan make the final call.

## Rollback

At any point before step 6, undo by moving both pack files back:
```
mv /Users/logan/IDAHO-VAULT-repair-20260902/corrupt-pack/pack-37e2012216...{pack,idx} .git/objects/pack/
```
This restores the exact prior state (corrupt object included). Loose objects
written by steps 3–4 are harmless to leave; a later `git prune` (deliberate,
not now) would clear any that are unreferenced.

## Notes / out of scope

- The stalled Windows sync (`incoming/windows-zbfury` never created despite
  receive-pack completing; a 2.5 MB `pack-c9346c54...` landed 2026-09-02 15:43)
  is a SEPARATE issue — Windows must report the push result. Not part of this
  repair, though a completed sync would give an alternate source for any
  missing objects in step 5.
- After a successful repair, update memory `vault-repo-hazards` to record the
  corrupt-pack item as resolved.
