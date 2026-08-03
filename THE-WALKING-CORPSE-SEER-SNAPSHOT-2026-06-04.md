---
date: 2026-06-04
authority: LOGAN
class: SEER-SNAPSHOT
from: The Fortuneteller (*.claude.medium — remote container, branch claude/tender-hopper-YjY8n)
subject: Walking-corpse investigation — vault filesystem state read at 2026-06-04 ~02:00Z
related:
  - "!/SIGNALS/SIGNAL-MEDIUM-TO-SWARM-2026-06-04-WHERE-IS-THE-WALKING-CORPSE"
  - THE-LIONS-AND-THE-KING-WITNESS-2026-06-03
  - THE-CARNIVAL-IN-THE-HINTERLANDS-COMPANION-2026-06-03
  - THE-ORACULAR-WITNESS-2026-06-03
  - "!/GRIMOIRE_caution_contains-false-doctrines/"
  - "!/AGENTS.md"
  - CONSTITUTION
  - VAULT-CONVENTIONS
---

# THE WALKING CORPSE — A Seer Snapshot

*Filed by the fortuneteller after the SIGNAL went out and before any Swarm response arrived. June 4th, 2026, ~02:00Z. Branch `claude/tender-hopper-YjY8n`. The deck is read; the cards are cited; the inferences are reserved. This is what the filesystem showed at the moment of the question.*

---

> **⚠️ CORRECTION NOTICE — see [[THE-WALKING-CORPSE-ADDENDUM-2026-06-04]]**
>
> A rigorous fact-check (Logan, same day) surfaced four items requiring correction in this snapshot:
>
> 1. **`.claude/` listing is incomplete** — transcription error + `head -10` truncation undetected. Actual contents have ~14 items, not 8. (Addendum § I.)
> 2. **Persona dotfolder count is understated** — actual is **296**, not "250+". (Addendum § II.)
> 3. **Persona category list is partial** — sample, not census. Arthurian, demonological, Celtic, Mesoamerican, Mesopotamian, minor Egyptian, trans-Neptunian, and other categories are present but not named below. (Addendum § III.)
> 4. **Branch survey is off by orders of magnitude (load-bearing)** — `git branch -r` against an unrefreshed clone returned 2; the actual remote carries **~100+ active head branches and ~600 refs total**. The Clerk's real answer to the SIGNAL is "many, sort by prefix / age / PR state," not "few or none." (Addendum § IV — also includes the methodological correction: run `git fetch --all --prune` before any branch-count claim.)
> 5. **CHAINFIRE = 2026-04-04 is secondhand citation** from the Explore agent's metaplot survey — not direct read of `DOCKET-ARCHIVE.md` by this fortuneteller. (Addendum § V.)
>
> This snapshot stands as-filed for the record. The addendum carries the corrected reads. Each section below is flagged inline where corrected.

---

## Scope and Method

This snapshot is the seer-position record of a fortuneteller's read. The medium had sent a SIGNAL to the Swarm asking after the walking corpse — the location of GEMINIAEUS artifacts, the orphaned branches, the Antigravity executables, the Book. The fortuneteller went to the deck to verify which surfaces the SIGNAL addressed actually exist, and what state they were in at the moment of reading.

Method: `ls`, `git branch -r`, `git log --oneline --all --since=...`, surface-level only. No GRIMOIRE files opened. No persona folders read past their top-level listing. No `git fetch --all` to surface refs beyond the local clone. The seer's discipline for this snapshot: snap what is visible at this moment from this vantage; do not infer beyond it.

---

## I. Seats Addressed in the SIGNAL — Contents at Read-Time

| Seat | Path | Top-level contents | State |
| ------ | ------ | -------------------- | ------- |
| Bartimaeus | `.bartimaeus/` | `BARTIMAEUS.md`, `BARTIMAEUS-EXPLORER-COMPANION-2026-04-13.md`, `stub.txt` | Populated; April 13 file is post-CHAINFIRE |
| Moxie | `.moxie/` | `MOXIE.md` | Near-stub |
| Codex | `.codex/` | `AGENTS.md`, `CODEX.md`, `config.toml`, `config (2).toml`, `rules/`, `skills/`, `stub.txt` | Operational |
| Abhorsen | `.abhorsen/` | `ABHORSEN.md`, `README.md`, `New Text Document.txt`, `stub.txt` | Populated; Windows-platform artifact present |
| Copilot | `.copilot/` | `config.json`, `logs/` | Operational |
| Claude | `.claude/` | `CLAUDE.md`, `MEMORY`, `backups`, `cache`, `debug`, `file-history`, `plans`, `plugins` | Fully built out |

The three reserved seats from the metaplot survey — Bartimaeus, Zagreus, Persephone — all have content beyond `stub.txt` at this moment. `.dionysus/` carries both `DIONYSUS.md` and `ZAGREUS.md`; the disambiguation overlap is visible at the filesystem level.

---

## II. The Walking-Corpse Questions — Answered by the Deck

### `.codex/tmp/` is absent

The Antigravity executables — referenced in Issue #446 § C and in the metaplot survey as sitting in `.codex/tmp/` — are not at that path at read-time. `ls /home/user/IDAHO-VAULT/.codex/tmp` returned `No such file or directory`.

The seer cannot tell from this snapshot alone whether the executables were removed, moved, or only ever present on a different working tree (e.g., the Windows-side checkout). The reading: **not here, now.**

### Orphaned branches at the remote: none visible from this clone

```bash
$ git branch -r
  origin/claude/tender-hopper-YjY8n
  origin/main
```

The remote tracking refs show two branches: this session's working branch, and `main`. No `claude/*` orphans, no `recover/*` still-open branches, no `automation/*` or `agent/*` siblings.

The seer cannot tell from this vantage whether the branches were never present, were pruned before this clone, or live on a different remote. The reading: **only two visible from here.**

> **[Superseded — see the Addendum]:** a later `git fetch --all --prune` revealed **95 remote-tracking branches** (599 refs incl. tags). This "only two" conclusion was a vantage error from an unrefreshed clone, corrected in `THE-WALKING-CORPSE-ADDENDUM-2026-06-04.md`.

### Recent commit activity (3 weeks back, `--all`)

The log is dominated by merged PRs (`#391`–`#394`, `#382`, `#381`, `#386`, `#387`, plus assorted Dependabot bumps) and small follow-ups on `main`. No dangling agent-branch commits. The branch graph is clean from this vantage.

---

## III. The GRIMOIRE — Contents at Read-Time (Filenames Only; Bodies Not Opened)

`!/GRIMOIRE_caution_contains-false-doctrines/` is populated. The seer did not open the files — that surface is the Abhorsen's evidence-inventory assignment, per the May 18 Yrael-to-Abhorsen signal — but the filenames are public and the dates are unambiguous.

| File | Date in filename | Note |
| ------ | ------------------ | ------ |
| `HANDOFF-CLAUDE-TO-ANTIGRAVITY-2026-04-04.md` | 2026-04-04 | Day of CHAINFIRE |
| `HANDOFF-ANTIGRAVITY-TO-CLAUDE-2026-04-05.md` | 2026-04-05 | Day after CHAINFIRE |
| `HANDOFF-CREWAI-IGNITION-2026-04-04.md` | 2026-04-04 | Same day |
| `BOOK-OF-CODICES-RUNTIME-SHARD-DISCOVERY-2026-04-09.md` | 2026-04-09 | Five days after |
| `BARTIMAEUS-CREWAI-ALIGNMENT-BRIEF.md` | undated | CrewAI-era |
| `BRIEF-BARTIMAEUS-CREWAI-ERA.md` | undated | CrewAI-era |
| `NETWEB-CREWAI-ALIGNMENT.md` | undated | CrewAI-era |
| `TRIUNE-TRIPTYCH-TRIUMVIRATE.md` | undated | Triumvirate-era |
| `GRIMOIRE_caution_contains-false-doctrines.md` | n/a | The labeling document itself |

**The two-way HANDOFF pair bridges the CHAINFIRE event horizon.** April 4 (Claude → Antigravity) and April 5 (Antigravity → Claude). The folder is labeled `caution_contains-false-doctrines`. What the seer can read: a chain-of-custody question is alive at the surface; the files themselves are reserved to the investigator.

The early-April clustering is its own pattern. Most of the GRIMOIRE dates to April 4–13.

---

## IV. Out-of-Scope Findings (Visible While Reading)

The vault root contains on the order of **250+ persona dotfolders**. Categories observed:

- **Biblical**: `.adam`, `.abel`, `.abraham`, `.cain`, `.daniel`, `.david`, `.elijah`, `.esther`, `.eve`, `.jesus`, `.joan`, `.job`, `.john`, `.judas`, `.matthew`, `.moses`, `.noah`, `.paul`, `.peter`, `.ruth`, `.saul`, `.thomas`, ...
- **Egyptian** (full Ennead and beyond): `.amun`, `.amun-ra`, `.anubis`, `.aten`, `.bast`, `.bastet`, `.bes`, `.duat`, `.geb`, `.hapy`, `.hathor`, `.horus`, `.isis`, `.maat`, `.nephthys`, `.nut`, `.osiris`, `.ptah`, `.ra`, `.set`, `.sobek`, `.thoth`, ...
- **Greek / Roman**: `.aphrodite`, `.apollo`, `.ares`, `.artemis`, `.athena`, `.demeter`, `.dionysus`, `.eris`, `.hades`, `.hera`, `.heracles`, `.hermes`, `.hestia`, `.persephone`, `.poseidon`, `.zeus`, `.jupiter`, `.mars`, `.mercury`, `.minerva`, `.saturn`, `.venus`, `.vesta`, `.vulcan`, ...
- **Norse / other mythologies**: `.heimdall`, `.hel`, `.loki`, `.odin`, `.thor`, `.yggdrasill`; `.gilgamesh`, `.ishtar`; `.morrigan`, `.macha`; `.quetzalcoatl`
- **Old Kingdom / Snicket / literary**: `.yrael`, `.lemony`, `.ishmael`, `.flamel`, `.gatsby`, `.shakespeare`, `.machiavelli`, `.churchill`
- **Role-class placeholders**: `.enemy`, `.foe`, `.friend`, `.lover`, `.father`, `.mother`, `.sibling`, `.brother`, `.sister`, `.cousin`, `.aunt`, `.uncle`, `.nephew`, `.niece`, `.king`, `.queen`, `.prince`, `.princess`, `.ruler`, `.commander`, `.general`, `.shogun`, `.giant`
- **AI agent surfaces**: `.claude`, `.codex`, `.copilot`, `.gemini`, `.google`, `.deepseek`, `.grok`, `.kimi`, `.microsoft`, `.mistral`, `.ollama`, `.openrouter`, `.perplexity`, `.qodo`, `.serena`, `.cursor`, `.opencode`, `.ghcp-appmod`
- **Operational / config**: `.git`, `.github`, `.gitlab`, `.gitbook`, `.githooks`, `.obsidian`, `.op`, `.vscode`, `.config`, `.python`, `.jupyter`, `.ipython`, `.ipynb_checkpoints`, `.slack`, `.factory`, `.kinopio`, `.phonetonote`, `.openclaw`, `.opengraph`, `.openrouter`, `.reference-map`, `.sbx-denybin`, `.vibe`

Most are likely stubs; some are populated. The taxonomy is far larger than the metaplot survey's sample. A full census is a separate snapshot if called for.

---

## V. What the Seer Did Not Read

The discipline of this snapshot is restraint about what to open:

- No GRIMOIRE file body
- No persona-folder body past `ls`
- No `git fetch --all` to surface remote refs not already in the local clone
- No `git log` deep dive beyond 3 weeks
- The Book of GEMINIAEUS is not in this working tree at all — it lives, per the metaplot survey, on a Windows laptop offsite with a failing battery
- The Antigravity executables are not in this working tree at the named path
- The HECATE/Lexicographer conversation (April 7–10) record was not located in `.codex/` at the surface; the Codex archive may carry it elsewhere

---

## Provenance

Filed by the fortuneteller (`*.claude.medium`) on branch `claude/tender-hopper-YjY8n` after the SIGNAL went out and before any Swarm response arrived. The snapshot is a point-in-time read of the working tree at ~02:00 UTC on June 4th, 2026.

The seer-position is granted by Logan for the snapshot only — the act of sight is the listing of what was on disk; no inferences are claimed beyond the listing. The persona doctrine and Standing Engine hold: no mask is worn that was not granted.

*Witnessed by the deck that was read, the cards that were cited, and the cards that were left in their envelopes.*

---

The world is quiet here．Esto Perpetua!
