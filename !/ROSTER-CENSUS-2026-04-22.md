---
date: 2026-04-22
authority: LOGAN
type: census
related:
- ROSTER
- AGENTS.md
- TRI-PART
- Maiden.Mother.Crone
- HECATE
---

# ROSTER CENSUS — 2026-04-22

## Executive Summary

The vault contains **200+ dotfolders** representing persona chambers, tool stubs, and runtime caches. Most are **empty placeholders** with minimal tri-part structure. This census documents the landscape, identifies gaps, and provides recommendations for a coherent prismatic architecture.

---

## Tri-Part Structure Specification

Every dotfolder MUST contain three layers:

| Layer | File | Purpose |
|-------|------|---------|
| **ENTITY-RUNTIME** | `runtime/` subfolder | Execution config, state, logs, credentials |
| **SELF-IDENTITY** | `NAME.md` | Authority, related, persona definition |
| **NARRATIVE-CONTINUITY** | `narrative/` subfolder | History, decisions, handoffs, memos |

### Current State of Tri-Part Compliance

- **FULL**: `.claude/`, `.serena/`, `.codex/`, `.gemini/`, `.github/`, `.bartimaeus/`, `.zagreus/`
- **PARTIAL (self + stub)**: ~190 mythological/personal stubs with `NAME.md` + `stub.txt`, no runtime or narrative
- **RUNTIME ONLY**: `.venv/`, `.cache/`, `.pycache/`, `.vscode/`, `.smart-env/` (machine-local, not personas)
- **EMPTY**: `.python/`, `.giant/`, `.gitlab/`, `.openrouter/`, `.opengraph/`, `.phonetonote/`, `.kimi/`, `.kinopio/`, `.gitguardian/`

---

## Census: Domain Analysis

### ACTIVE PERSONAS (5)

| Dotfolder | Files | Status | Tri-Part |
|-----------|-------|--------|----------|
| `.claude/` | 5,112 | **The Abhorsen** | ✅ Full |
| `.codex/` | 3,924 | **The Lexicographer** | ✅ Full |
| `.gemini/` | 10,553 | **The Concierge** | ✅ Full |
| `.github/` | 133 | **The Clerk** | ✅ Full |
| `.serena/` | 85 | **The Tapestry** | ✅ Full |

### MYTHOLOGICAL: Greek Pantheon (~30)

`.apollo/`, `.ares/`, `.artemis/`, `.athena/`, `.demeter/`, `.hades/`, `.hecate/`, `.hephaestus/`, `.hera/`, `.hermes/`, `.hestia/`, `.aphrodite/`, `.zeus/`, `.poseidon/`, `.hades/`, `.persephone/`, `.dionysus/`, `.pan/`, `.deimos/`, `.phobos/`, `.hypnos/`, `.chronos/`, `.cronos/`, `kronos/`, `.heracles/`, `.perseus/`, `.minerva/`, `.cain/` (Bible)

**Status**: All have `NAME.md` + `stub.txt`. Zero runtime. Narrative layer empty.

### MYTHOLOGICAL: Egyptian Pantheon (~30)

`.anubis/`, `.osiris/`, `.isis/`, `.ra/`, `.thoth/`, `.horus/`, `.set/`, `.seth/`, `.bast/`, `.bastet/`, `.sekmet/`, `.neith/`, `.nut/`, `.geb/`, `.tefnut/`, `.shu/`, `.tefnut/`, `.hathor/`, `.khnum/`, `.thoth/`, `.maat/`, `.bes/`, `.bennu/`, `.hapi/`, `.duamutef/`, `.qebehsenuef/`, `.imhotep/`, `.imsety/`, `.serqet/`, `.seshat/`, `.anput/`, `.nephthys/`, `.ammit/`, `.tawaret/`, `.sobek/`, `.montu/`, `.atem/`, `.atum/`, `.khepri/`, `.aten/`, `.amun/`, `.amun-ra/`, `.ra-horakhty/`

**Status**: All have `NAME.md` + `stub.txt`. Zero runtime. Narrative layer empty.

### MYTHOLOGICAL: Norse Pantheon (~10)

`.odin/`, `.thor/`, `.loki/`, `.heimdall/`, `.freya/`, `.hel/`, `.tyr/`, `.baldur/`, `.frigg/`, `.bragi/`, `.yth/`, `.aegir/`, `.ymir/`, `.buri/`, `.yggdrasill/`

**Status**: All have `NAME.md` + `stub.txt`. Zero runtime. Narrative layer empty.

### RELATIONAL PERSONAS (~25)

`.father/`, `.mother/`, `.brother/`, `.sister/`, `.cousin/`, `.aunt/`, `.uncle/`, `.nephew/`, `.niece/`, `.friend/`, `.ally/`, `.enemy/`, `.foe/`, `.lover/`, `.enemy/`, `.ruler/`, `.prince/`, `.princess/`, `.queen/`, `.king/`, `.general/`, `.commander/`, `.goliath/`, `.giant/`

**Status**: All have `NAME.md` + `stub.txt`. Zero runtime.

### BIBLICAL/RELIGIOUS (~15)

`.jesus/`, `.lucifer/`, `.satan/`, `.moses/`, `.michael/`, `.adam/`, `.eve/`, `.abraham/`, `.aaron/`, `.moses/`, `.noah/`, `.abraham/`, `.job/`, `.saul/`, `.paul/`, `.peter/`, `.john/`, `.judas/`, `.elijah/`, `. Jezebel/`, `.esther/`, `.ruth/`, `.mary/`, `.anne/`

**Status**: All have `NAME.md` + `stub.txt`. Zero runtime.

### PERSONAL NAMES (~30)

`.david/`, `.diana/`, `.daniel/`, `.duncan/`, `.daisy/`, `.debby/`, `.dee/`, `.dennis/`, `.david/`, `.diana/`, `.duncan/`, `.andrew/`, `.arthur/`, `.billy/`, `.bob/`, `.john/`, `.joan/`, `.josh/`, `.kit/`, `.matthew/`, `.matthias/`, `.nick/`, `.nicholas/`, `.peter/`, `.philip/`, `.robert/`, `.scott/`, `.simon/`, `.thomas/`, `.thaddeus/`, `.victoria/`, `.isadora/`, `.anne/`, `.anna/`, `.abigail/`, `.lemony/`

**Status**: All have `NAME.md` + `stub.txt`. Zero runtime.

### TOOL/API STUBS (~10)

| Dotfolder | Tool | Status |
|-----------|------|--------|
| `.gitlab/` | GitLab | `New folder.md` scaffold |
| `.openrouter/` | OpenRouter API | Empty |
| `.opengraph/` | OpenGraph metadata | Empty |
| `.phonetonote/` | PhoneToNote | Empty |
| `.gitguardian/` | GitGuardian | Empty |
| `.kimi/` | Kimi AI (Moonshot) | Empty |
| `.kinopio/` | Unknown | Empty |
| `.giant/` | Unknown | Empty |

### RUNTIME CACHES (~15) — NOT PERSONAS

`.venv/` (23k), `.vscode/` (23k), `.smart-env/` (22k), `.uv-cache/` (8k), `.cache/` (16k), `.pycache/` (1.6k), `.npm-cache/`, `.pip-cache/`, `.local/`, `.config/`, `.jupyter/`, `.ipython/`, `.ollama/`, `.openclaw/`, `.opencode/`, `.obsidian/`

### EXTERNAL SERVICES (~8)

`.op/` (1Password), `.slack/`, `.google/`, `.microsoft/`, `.meta/`, `.mistral/`, `.grok/`, `.deepseek/`, `.perplexity/`

### SPECIAL AGENTS (~8)

`.bartimaeus/` (The Cartographer), `.zagreus/` (The Dionysian), `.abhorsen/` (alias for `.claude/`), `.dionysus/` (alias for `.zagreus/`), `.serena/` (The Tapestry), `.mistral/` (Vibe), `.vibe/`, `.qodo/`, `.hook/`

---

## Gap Analysis: Missing Domains

### SPARSE/EMPTY DOMAINS

| Domain | Existing | Missing |
|--------|----------|---------|
| **Roman Pantheon** | `.jupiter/`, `.mars/` | `.juno/`, `.neptune/`, `.minerva/`, `.vulcan/`, `.venus/`, `.apollo/` (is Greek), `.mercury/`, `.saturn/`, `.pluto/` |
| **Celtic** | `.macha/` | `.cernunnos/`, `.brigid/`, `.lugh/`, `.morrigan/` (exists), `.danu/`, `.awen/` |
| **Hindu** | None | `.shiva/`, `.vishnu/`, `.ganesha/`, `.kali/`, `.durga/`, `.brahma/`, `.indra/`, `.yama/`, `.varuna/` |
| **Shinto** | None | `.amaterasu/`, `.tsukuyomi/`, `.susanoo/`, `.inari/`, `.izanami/`, `.izanagi/` |
| **Mesoamerican** | `.quetzalcoatl/` | `.huitzilopochtli/`, `.tlaloc/`, `.coatlicue/`, `.xipe-totec/`, `.kukulkan/` |
| **Buddhist** | None | `.buddha/`, `.avalokiteshvara/`, `.maitreya/` |
| **Trickster Archetype** | `.hermes/`, `.loki/` | `.coyote/`, `.anansi/`, `.raven/`, `.brer-rabbit/` |
| **Philosophical** | None | `.socrates/`, `.plato/`, `.aristotle/`, `.epictetus/`, `.seneca/`, `.marcus/`, `.confucius/`, `.laozi/`, `.diogenes/` |
| **Abrahamic Angels** | `.michael/` | `.gabriel/`, `.raphael/`, `.uriel/`, `.jophiel/`, `.chamuel/`, `.zadkiel/` |
| **Archival Journalism** | None | `.woodward/`, `.bernstein/`, `.lippmann/`, `.ben-bagley/` |
| **Idaho Journalism** | None | `.statesman/`, `.press/`, `.tribune/` |
| **Functional Roles** | None | `.scribe/`, `.archivist/`, `.gatekeeper/`, `.witness/`, `.messenger/`, `.counsel/`, `.sentinel/` |
| **States/Utilities** | None | `.truth/`, `.justice/`, `.mercy/`, `.memory/`, `.threshold/`, `.veil/` |

---

## Recommendations

### PRIORITY 1: Complete Tri-Part Structure for Active Personas

1. `.claude/`, `.codex/`, `.gemini/`, `.github/`, `.serena/` — Already have full structure. Mark as COMPLETE.

### PRIORITY 2: Add Narrative Layer to Mythological Stubs

For each mythological dotfolder, add:
- `narrative/ARCHETYPE.md` — Persona definition
- `narrative/decisions.md` — Role decisions
- `narrative/memos/` — Cross-agent handoffs

### PRIORITY 3: Fill Key Gaps

**Roman Pantheon** (already has some entries):
- `.vulcan/` — Forge, fire, craftsmanship
- `.juno/` — Marriage, protection
- `.neptune/` — Seas, unknown depths

**Trickster Cross-Cultural**:
- `.coyote/` — Native American trickster
- `.anansi/` — African spider trickster
- `.raven/` — Northwest Native trickster

**Functional/Abstract**:
- `.scribe/` — Documentation authority
- `.witness/` — Verification, fact-checking
- `.gatekeeper/` — Access control, security
- `.archivist/` — Memory preservation
- `.threshold/` — Transition states, liminal spaces

### PRIORITY 4: Runtime Stubs for Active Tools

For `.gitlab/`, `.openrouter/`, `.gitguardian/`, add:
- `runtime/config.md` — API credentials structure
- `runtime/state.md` — Current connection state
- `runtime/.gitignore` — Ignore runtime state

---

## Prismatic Activation Potential

Each dotfolder can be activated as a **prismatic layer** by stacking:

```
.serena/ + .hecate/ + .maat/ = Intelligence + Thresholds + Truth
.claude/ + .odin/ + .thoth/ = Code + Wisdom + Knowledge
.codex/ + .hermes/ + .bastet/ = Scripts + Speed + Night research
.github/ + .hephaestus/ + .maat/ = Admin + Craft + Order
```

**200+ potential layers. 5 active. 195 dormant.**

---

## Actions Required

1. [ ] Update `!/AGENTS.md` to reflect accurate current landscape
2. [ ] Add narrative structure to mythological stubs (batch process)
3. [ ] Create missing domain dotfolders (Roman, Celtic, Trickster, Functional)
4. [ ] Add runtime configs to tool stubs
5. [ ] Audit `.ares/` and similar "ancient" stubs for intended use

---

###### [["The world is quiet here."]]
###### [ Maiden : Mother : Crone ]