---
title: "Survey - Mirroring/Syncing Methods vs Windows-Illegal Names (Canon Core Companion)"
date created: 2026-07-02
authority: developer-agent (Hyperagent, Claude Opus 4.8); account of record loganfinney27
doc_class: report
status: draft
related:
  - "!-DRAFT-ADR-CANON-CORE-VS-WINDOWS-PORTABILITY-2026-07-02.md"
  - "VAULT-CONVENTIONS.md"
  - "!/!/__!__/!/! The world is quiet here．/Esto Perpetua!/!README.md"
  - ".github/scripts/check_portable_paths.py"
---

# Survey - Mirroring/Syncing Methods vs Windows-Illegal Names

*Filed 2026-07-02, companion to the canon-core ADR. Online survey of primary sources
(vendor docs, maintainer statements, issue trackers). Doc-verified, not lab-tested here,
except where the vault's own trees were read. I propose; Logan inscribes.*

## The invariant that sorts every tool

NTFS **can store** a trailing-dot name (POSIX namespace); it is the **Win32 layer** that
cannot pass one through — it silently strips trailing dots/spaces, and `\\?\`-prefixed
paths bypass that parsing entirely (Microsoft "Naming Files"; superuser/grawity; ss64).
Every mirroring/sync method therefore lands in one of four families:

1. **REFUSE / EXCLUDE** — don't materialize the offending path on Windows.
2. **RENAME-IN-TRANSIT (map)** — materialize under a transformed, Windows-legal name.
3. **SIDESTEP WIN32** — use NT-native/POSIX pathways (Cygwin, WSL, `\\?\`) so the true
   name lands on disk — which Win32 apps (Explorer, **Obsidian**) then can't handle.
4. **NAMES-AS-IS** (plain Win32 copy tools) — strip/fail; not viable by definition.

## Tool-by-tool findings (sourced)

| Tool / method | Family | Verified behavior for trailing-dot names |
|---|---|---|
| **Git for Windows** | REFUSE | `core.protectNTFS=true` (default; CVE-2019-1353 hardening) rejects the path **even into the index** — sparse-checkout alone does NOT dodge it ("doesn't allow bad paths into the index at all, even if those paths are not being populated by the sparse-checkout" — git-for-windows #2777). Working pattern: `clone --no-checkout -c core.protectNTFS=false` + sparse-checkout excluding the paths (#2777, #2803, Atlassian KB). With protectNTFS off AND actual materialization attempted, Win32 strips the dot → truncated names / zero-byte files. |
| **git sparse-checkout** | EXCLUDE | The mechanism behind ADR Option A — but on Windows it must be paired with per-repo `core.protectNTFS=false` (above). Non-cone patterns can exclude a single prefix. |
| **rclone** | MAP (default!) | The local backend on Windows **by default** replaces Windows-illegal characters with fullwidth Unicode look-alikes, including *trailing* `.` → `．` (U+FF0E) and trailing space → `␠` — i.e. **rclone ships ADR Option C as its default behavior** (rclone.org/local, encoding table). Caveats: the encoding design has sharp edges (#7456 "counter-intuitive", #7760 VFS data-loss bug with CJK punctuation, FAQ regrets choosing fullwidth chars). |
| **Syncthing** | REFUSE | Explicitly errors per item: "name is invalid, must not end in space or period on Windows" (lib/fs, PRs #7011/#8969); offending items fail, rest of folder syncs — de facto exclusion with error noise. An encoder to map reserved names (PR #7876, fixes #1734) exists but is **not merged** per available sources. |
| **Dropbox** | MAP (local) | "Flexible file names": the desktop client **replaces the offending character with an underscore locally** while **the canonical name is preserved server-side** (help.dropbox.com/organize/file-names) — a vendor-managed two-representation system: canon upstream, transformed on Windows. |
| **OneDrive** | MAP-or-REFUSE | Auto-renames (underscore) names ending in a period when it can; otherwise the item does not sync until manually renamed (MS support). |
| **Obsidian / Obsidian Sync** | REFUSE (per-OS) | Deliberate policy: Obsidian validates names against **only the current OS** ("we are now only blocking forbidden characters from your current operating system" — staff, forum 2023; reaffirmed by lishid 2026: "expected behavior"). Cross-OS, invalid items are skipped with sync-log errors; fix is manual rename on a permissive device. Vaults/folders ending in "." on Windows: "uneditable, undeletable folder that saves nothing and isn't recognized" (bug report). |
| **Cygwin** | SIDESTEP | Uses NT-native APIs: "Cygwin applications can create and access files with trailing dots and spaces without problems" (Cygwin UG, Special filenames). Separately maps forbidden *characters* to Private-Use-Area U+F0xx (the Interix scheme). Result is on disk but broken for Win32 apps. |
| **WSL1/WSL2 (drvfs)** | SIDESTEP | Can create/access trailing-dot names on NTFS mounts unless mounted `windows_names`; inside WSL2 ext4 it is ordinary Linux. Win32 side still can't use the materialized names. |
| **`\\?\` prefix** | SIDESTEP | Raw NT namespace from Windows itself: `mkdir`/`del`/`ren` on `\\?\C:\…\dotatend.` works (superuser; ss64). Escape hatch for cleanup, not a workflow. |
| **ntfs-3g / ntfs3 `windows_names`** | (inverse knob) | Linux NTFS drivers can opt INTO Win32 strictness — blocks creating trailing-dot names at write time (ntfs-3g manpage; kernel ntfs3). |
| **robocopy / plain Win32 copy** | NAMES-AS-IS | Win32-layer tools; expected strip/fail (not lab-tested here). |

## The directory-vs-file nuance (matters for the canon)

Windows' rule bites **final path components without extensions** — i.e. directories.
An Obsidian **note** named `…here.` works even on Windows because it is stored as
`…here..md` (dot is no longer trailing; observed by Obsidian help contributors, 2025,
and consistent with the vault's own root file `The world is quiet here..md`). The canon
problem is specifically the **directory** `! The world is quiet here.` — no extension
ever rescues it. The extensionless *file* `Esto Perpetua!/! The world is quiet here`
(no trailing dot) is unaffected.

## What this does to the ADR options

1. **Option A (sparse-exclude) gains a required second ingredient on Windows:** per-repo
   `core.protectNTFS=false` alongside the sparse rule, because protectNTFS validates
   index entries even when skip-worktree excludes them (#2777). Narrow, documented, but
   it does relax the CVE-2019-1353 guard for that clone — worth stating in onboarding.
2. **Option C (homoglyph) has industrial precedent:** rclone's *default* Windows mapping
   is exactly trailing `.` → fullwidth `．` (U+FF0E), and Cygwin/Interix normalized the
   same class of problem into the PUA two decades ago. C is not exotic; it is what
   working sync systems already do.
3. **Option B (mirror) has a vendor exemplar:** Dropbox's flexible file names — canonical
   name upstream, transformed name on the Windows client only. A vault mirror could copy
   that shape (canon path in git; a transform layer only on Windows checkouts), though it
   inherits the same drift/ownership questions the ADR raises.
4. **The engine room's Obsidian cannot be rescued by SIDESTEP tricks:** even if Cygwin /
   WSL / `\\?\` materialize the true name, Obsidian-on-Windows (a Win32 app with per-OS
   validation) treats such a folder as broken. For the Windows desktop specifically, only
   EXCLUDE (A/D) or a rename (C/E) yields a usable vault.
5. **Syncthing/Obsidian-Sync-style "skip with errors" is the worst of both** — permanent
   error noise as canonical state. Supports the ADR's preference for a *deliberate*
   posture (A or E) over incidental tool behavior.

## Sources

- Microsoft: Naming Files, Paths, and Namespaces; Maximum Path Length (learn.microsoft.com)
- superuser: "Why does NTFS disallow trailing periods" (grawity); "Create a folder ending
  with a dot on NTFS in Linux"; ss64 filename syntax
- git-for-windows/git #2777, #2803; msysgit #317; Atlassian KB "invalid path on clone"
- rclone.org/local (encoding table); rclone #7456, #7760; PR 5635 (FAQ)
- syncthing PRs #7011, #8969, #7876; forum "must not end in space or period" (2021)
- help.dropbox.com/organize/file-names; Microsoft OneDrive invalid-names support page
- Obsidian forum: staff statements (2023, 2025, 2026), obsidian-help #1001, vault-names bug
- cygwin.com/cygwin-ug-net/using-specialnames.html; cygwin ML (Vinschen, 2008–2010)
- microsoft/WSL #2689 (incl. ntfs-3g `windows_names` manpage excerpt)

###### [["The world is quiet here."]]
