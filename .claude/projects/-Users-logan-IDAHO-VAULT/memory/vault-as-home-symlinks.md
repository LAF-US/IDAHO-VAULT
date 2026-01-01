---
name: vault-as-home-symlinks
description: "Dotfolders in ~ are symlinks into IDAHO-VAULT — a dropped symlink silently breaks the tool, not the data. How to diagnose and restore."
metadata:
  node_type: memory
  type: project
---

Logan's home dotfolders are symlinks into the vault, so config is tracked and
travels between machines. Confirmed live: `~/.ssh` and `~/.claude` ->
`/Users/logan/IDAHO-VAULT/.ssh` and `/.claude`.

**Some links were dropped and he knows it.** He said so directly: "I knew I
messed up and dropped at least one or two of the symlinks back then." When a link
goes missing the DATA is still safe in the repo — the tool just cannot find it,
and fails in a way that looks like the data is gone.

**Worked example, colima (fixed 2026-08-31).** Docker Desktop will not run on
this macOS, so colima was installed as the substitute. It stopped working
2026-05-11 with SSH failures naming
`/Users/logan/.colima/_lima/_config/user` — a path that only resolves through the
symlink. `~/.colima` was simply absent. The whole thing was in the repo the entire
time: `.colima/default/colima.yaml` (runtime docker, qemu x86_64, 2 CPU, 6 GiB,
30 GiB), `.colima/_store/colima.json`, and the ACTUAL VM at
`.colima/_lima/colima/disk` (20 GiB sparse, ~1.5 GiB real). Recreating
`ln -s /Users/logan/IDAHO-VAULT/.colima /Users/logan/.colima` brought the instance
straight back — `colima list` shows `default  Stopped  x86_64  2  6GiB  30GiB
docker`. Not started yet.

**Gotcha when recreating:** if the tool has already auto-created an empty
`~/.foo`, `ln -s TARGET ~/.foo` puts the link INSIDE it rather than replacing it.
Check `[ -L ~/.foo ]` afterwards, not just that the path exists.

**Diagnostic pattern:** a tool that "lost its config" on this machine — check
whether its dotfolder is a symlink into the vault before concluding anything is
missing. `.gitignore` rules cover the sensitive parts (e.g. `id_ed*` at
.gitignore:46 on the Mac copy), so private keys stay untracked while the
surrounding config travels.

**Consequence worth remembering:** because `~/.ssh` resolves into the vault,
sshd's StrictModes walks the VAULT directory too. A group-writable
`/Users/logan/IDAHO-VAULT` made sshd refuse every key with
"bad ownership or modes for directory" while `.ssh` itself was correct at 700.

Related: [[idaho-vault-storage-architecture]], [[vault-repo-hazards]].
