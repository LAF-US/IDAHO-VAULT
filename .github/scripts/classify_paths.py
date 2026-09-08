"""Classify changed file paths into the two-paired-flag risk scheme.

NEXT AGENT — the one fact that prevents breakage: the binary `tier` (low|high) is the ONLY
field any live consumer reads (`agent-auto-pr.yml` reads `['tier']`). `tier4`, `filetype`, and
the `clear` value are intentionally inert — nothing reads them yet. Do NOT wire a `tier4`
consumer that hardcodes `{low,med,high,nope}`; it will choke on `clear`. The two-sorter MODEL is
settled; the routing MECHANISM (lanes, flag lifecycle, grid-cell routes) is HELD for Logan — see
issue #626 + `WITNESS-THE-KEYS-ARE-THE-LEVERS-2026-06-21.md`. The grid is a model, not code.

Conceptualized in the planning session of 2026-06-21 and witnessed in
`WITNESS-THE-KEYS-ARE-THE-LEVERS-2026-06-21.md`; this is its first implementation,
replacing the prior binary (high|low, fail-safe-to-high) classifier.

THE SCHEME — two INDEPENDENT paired flags. A changeset carries either version of
each, or neither (per Logan, 2026-06-21):

  * filetype flag : — | low | med  — the "maze": WHAT KIND of file it is. Tags files
                                   OUTSIDE the `!` Nest, by the Architect's three blessed
                                   language circles (VAULT-CONVENTIONS § File Types), ONE
                                   circle per state (blueprint, 2026-06-22):
                                     Natural Language (.md, prose) -> `—` (None: no flag)
                                     Machine Documentation (.json/.yaml; + inert assets) -> low
                                     Computer Code (.py/.sh/...) -> med
  * depth flag    : high | nope  — the "labyrinth": HOW DEEP into the `!` Nest.
                                   Tags files INSIDE the `!` Nest, by the seven Levels
                                   (the Sierpinski spine ~/ root -> Esto Perpetua!).

Per Logan's correction: "low/med apply to filetypes; high/nope apply to depth."
So a maze file is tagged by filetype only; a Nest file is tagged by depth only —
depth supersedes filetype inside the labyrinth. A prose-only maze file carries NO
flag on EITHER axis: it is the `—/—` "clear" cell (the blueprint's auto-merge state).

JSON output — `tier` stays BINARY (low|high) to preserve the existing `risk/<tier>` label
contract: `agent-auto-pr.yml` stamps `--label risk/$tier` and `ensure-labels` only creates
`risk/low`/`risk/high`, so emitting `med`/`nope` here would break PR creation. The richer
result lives in the `tier4` field. NOTE (this step): `clear` collapses to binary `low`, so
introducing the `—` state changes NO binary-label behavior the live producer/consumer use
today — the new `—/—` distinction rides only in `tier4`/`filetype` for the consumer-wiring
step to come (see WITNESS-THE-KEYS-ARE-THE-LEVERS-2026-06-21.md and #626).
  {
    "tier": "low"|"high",                         # BINARY legacy label (risk/<tier>); clear+low -> low
    "tier4": "clear"|"low"|"med"|"high"|"nope",   # the result (nope>high>med>low>clear)
    "filetype": None|"low"|"med",                 # riskiest filetype touched; None = `—` (prose, or a
                                                  #   Nest/protected file tagged on the depth axis)
    "depth": "high"|"nope"|None,                  # deepest Nest reach among files touched
    "subtier": None,                              # TBD — next version (see "SUBTIERS" below)
    "by_file": [{"path","filetype","depth"}...],
    "high_risk_files": [...], "low_risk_files": [...]   # legacy aggregate buckets
  }

--- TUNABLE (Logan's pins still open; marked * in the witness) ---
* FILETYPE CUT: which blessed circle is `—` vs `low` vs `med`. Default (blueprint, 2026-06-22):
  Natural Language (prose) -> `—` (no flag); Machine Documentation + inert assets -> low;
  Computer Code (executes) -> med. Pulling Natural Language out to `—` is THIS step.
* DEPTH THRESHOLD: where `high` becomes `nope`. Default: only the canon core /
  still-point (Esto Perpetua!, Level 7 — "do not move, do not expire") is `nope`;
  all other Nest depth is `high`.
* DOTFOLDER / PROTECTED PIN — the nest-level angle (Logan, 2026-06-22): scrutiny scales with
  DEPTH (the deeper the level, the more scrutiny to alter; `nope` at the still-point). Persona/
  config dotfolders (`.claude/`, `.gemini/`, `.codex/`, `.op/`, ...), `.github/**`, and named root
  governance files are pinned `high` because their TRUE home is a deep `!` Nest layer — they sit at
  `~/` only because certain programs expect them there (a tooling MIRROR/shim), not because they are
  root corpus. Risk follows the source (deep `!`), not the mirror (root); this path-pin is a PROXY
  for that true depth. FUTURE: dotfolders live at a deep `!` layer and mirror out to `~/` as needed,
  at which point the pin becomes a true depth classification. (CODEOWNERS is a separate, complementary Key.)

--- SUBTIERS: TBD — NOT YET IMPLEMENTED (next version) ---
Logan outlined that each tier ALSO has subtiers: filetype subtiers = the three blessed
circles {Natural Language, Computer Code, Machine Documentation} + the "missing middle"
(Jupyter); depth subtiers = the seven Levels / Demesnes (bangdepth). Their exact values and
cut-points are "unique unspecified" and deferred (per Logan, 2026-06-21). This module emits
only the four TOP tiers and a `"subtier": None` placeholder; the cuts above are provisional.
"""

import json
import posixpath
import re
import sys

# ═════════════════════════════════════════════════════════════════════════════
# CONFIG — the tunable knobs. Tuning risk behavior should mean editing THIS block,
# never the logic below. In particular:
#   • To RE-TIER a filetype: MOVE its extension between the FILETYPE_* sets.
#       (e.g. make inert assets `—` instead of `low`: move INERT_ASSET from
#        FILETYPE_LOW into FILETYPE_NONE — one line, nothing else changes.)
#   • To PROTECT a new surface: add it to PROTECTED_EXACT / PROTECTED_PREFIXES.
#   • To REORDER risk tiers: edit TIER_PRECEDENCE — it is the single ordering the
#     aggregation and combine() both read.
# ═════════════════════════════════════════════════════════════════════════════

# Tier names, riskiest -> safest. The ONE ordering: both combine() and the per-axis
# aggregation read this, so there is no second place to keep in sync.
TIER_PRECEDENCE = ("nope", "high", "med", "low", "clear")
CLEAR_TIER = "clear"                    # the `—/—` cell — no flag on either axis
SAFE_TIERS = ("clear", "low")           # fold to binary `low`; everything riskier -> binary `high`
# Enforce the single source at import (fail loud, not silent drift): SAFE_TIERS and
# CLEAR_TIER must be members of the one ordering, so adding/reordering tiers can't desync them.
assert CLEAR_TIER in TIER_PRECEDENCE, "CLEAR_TIER must be in TIER_PRECEDENCE"
assert set(SAFE_TIERS) <= set(TIER_PRECEDENCE), "SAFE_TIERS must be a subset of TIER_PRECEDENCE"

# Nest / still-point markers (NETWEB: '-' aliases '/' in flattened root filenames).
NEST_PREFIX = "!"
STILL_POINT_SEGMENT = "Esto Perpetua!"
_PATH_SEGMENT_RE = r"[-/]"

# --- The Architect's three blessed language circles (VAULT-CONVENTIONS § File Types) ---
NATURAL_LANGUAGE = {".md", ".markdown", ".txt", ".rtf"}          # Logan's prose surface
MACHINE_DOC = {".json", ".yaml", ".yml", ".toml", ".csv",        # declarative: describes
               ".xml", ".ini", ".cfg", ".conf"}
COMPUTER_CODE = {".py", ".sh", ".bash", ".ps1", ".bat", ".cmd",  # imperative: executes
                 ".js", ".ts", ".ipynb"}  # .ipynb = the "missing middle"; reviewed via its .md twin
INERT_ASSET = {".pdf", ".png", ".jpg", ".jpeg", ".gif", ".svg",  # binary/asset content
               ".webp", ".ico", ".mp3", ".mp4", ".ics", ".mtl", ".obj"}

# Filetype -> flag. THE knob: which extensions carry which filetype flag (blueprint,
# 2026-06-22 — one blessed circle per state). Built from the circles above for readability;
# these three sets are the operative config — move an extension between them to re-tier it.
FILETYPE_NONE = NATURAL_LANGUAGE               # `—` : prose carries NO flag (the `—/—` clear cell)
FILETYPE_LOW = MACHINE_DOC | INERT_ASSET       # declarative / inert -> low
FILETYPE_MED = COMPUTER_CODE                   # executes -> med
FILETYPE_UNKNOWN_DEFAULT = "med"               # unrecognized extension -> conservative

# Placement pins (the fileplacement axis; eventually the K1/K2 single source of truth).
# Add a surface here to protect it.
PROTECTED_PREFIXES = (".github/",)  # the whole GitHub control plane (probe carve-out below)
PROTECTED_EXACT = {
    "AGENTS.md", "CLAUDE.md", "CONSTITUTION.md", "DECISIONS.md", "LEVELSET.md",
    "VAULT-CONVENTIONS.md", "VAULT-TEMPLATES.md", "swarm.json", ".gitignore",
    ".github/CODEOWNERS", ".github/copilot-instructions.md",
}
# Probe/example sandboxes under the protected dirs stay low (explicit carve-out).
PROBE_PREFIXES = (".github/workflows/probe-", ".github/workflows/example-",
                  ".github/scripts/probe-", ".github/scripts/example-")

# Detects any top-level dotfolder: .claude/, .gemini/, .codex/, .op/, etc.
# Pinned high: true home is a deep ! Nest layer, mirrored to ~/ for tooling (Logan, 2026-06-22).
TOP_DOTFOLDER_RE = re.compile(r"^\.[a-zA-Z]")


def in_nest(path: str) -> bool:
    """A path is in the `!` Swarmic Nest — nested `!/...` or a flattened `!`-prefixed
    root alias (NETWEB: '-' aliases '/'). VAULT-CONVENTIONS § Root Folder Semantics."""
    return path.startswith(NEST_PREFIX)


def is_still_point(path: str) -> bool:
    """The canon core / Level 7 — the inmost still point, `Esto Perpetua!`
    ('do not move, do not expire'). Structural: `Esto Perpetua!` must appear as a path
    SEGMENT *inside the Nest* — nested `.../Esto Perpetua!/...` or the flattened `!`-alias
    form (NETWEB: '-' aliases '/') — not a bare substring, so a maze note merely *named*
    with the text is never `nope`. Within the Nest the segment match errs toward `nope`
    (over-protect) — the safe direction for the canon core."""
    return in_nest(path) and STILL_POINT_SEGMENT in re.split(_PATH_SEGMENT_RE, path)


def filetype_flag(path: str) -> str | None:
    """None | low | med for a maze (non-Nest) file, by its blessed-circle membership.
    None is the `—` state: Natural Language (prose) carries NO filetype flag, so a
    prose-only maze PR lands in the `—/—` clear cell. Machine Documentation / inert
    assets -> low; Computer Code -> med; unrecognized -> med (conservative)."""
    ext = posixpath.splitext(path)[1].lower()
    if ext in FILETYPE_MED:
        return "med"
    if ext in FILETYPE_LOW:
        return "low"
    if ext in FILETYPE_NONE:
        return None  # Natural Language -> the `—` state (no flag)
    return FILETYPE_UNKNOWN_DEFAULT  # unrecognized type: conservative (TUNABLE)


def classify_file(path: str) -> tuple:
    """Return (filetype_flag, depth_flag) for one path — at most one axis is active.
    Maze files carry a filetype flag; Nest files carry a depth flag (depth supersedes). A
    prose (Natural Language) maze file carries NEITHER — `(None, None)`, the `—/—` clear cell.
    (That a Nest file carries *only* a depth flag is an interpretation of "either version of
    both or neither" at PR granularity — flagged for Logan; see the module docstring.)"""
    if in_nest(path):
        return (None, "nope" if is_still_point(path) else "high")
    # Maze. Probe sandboxes stay low; protected surfaces are pinned high (safety override).
    if path.startswith(PROBE_PREFIXES):
        return ("low", None)
    if path in PROTECTED_EXACT or path.startswith(PROTECTED_PREFIXES):
        # No off-Nest 'high' exists in the pure model; pin via the depth axis to avoid
        # a protection downgrade. TUNABLE: delegate this gate to CODEOWNERS instead.
        return (None, "high")
    # Persona/config dotfolders (.claude/, .gemini/, .codex/, .op/, etc.) are pinned high.
    # Editing agent config surfaces must not be auto-labeled risk/low.
    if "/" in path and TOP_DOTFOLDER_RE.match(path):
        return (None, "high")
    return (filetype_flag(path), None)


def riskiest(*flags) -> str | None:
    """The riskiest non-None flag among `flags`, ranked by TIER_PRECEDENCE; None if all
    absent. The single ordering primitive — used both to aggregate an axis across files
    and to combine the two axes — so there is no second copy of the tier order to drift."""
    present = [f for f in flags if f is not None]
    return min(present, key=TIER_PRECEDENCE.index) if present else None


def combine(filetype, depth) -> str:
    """Collapse the (filetype, depth) pair to one tier by TIER_PRECEDENCE (riskiest wins):
    nope > high > med > low. `clear` is the `—/—` state — NO flag on either axis (a prose-only
    maze file) — kept DISTINCT from `low` so a later auto-merge gate can key on it (blueprint:
    `—/—` auto-merges on open; `low` is a flag that holds). For the binary legacy `tier`,
    `clear` folds back into `low` (see main), so this distinction changes no current behavior."""
    return riskiest(filetype, depth) or CLEAR_TIER


def main():
    paths = [line.strip() for line in sys.stdin if line.strip()]
    by_file = []
    for p in paths:
        ft, dp = classify_file(p)
        by_file.append({"path": p, "filetype": ft, "depth": dp})

    # Aggregate each axis to its riskiest reach across the changeset (same ordering primitive).
    filetype = riskiest(*(b["filetype"] for b in by_file))
    depth = riskiest(*(b["depth"] for b in by_file))
    tier4 = combine(filetype, depth)            # nope|high|med|low|clear
    # Binary legacy contract (risk/<tier>): the SAFE states (clear + low) -> low; everything
    # above -> high. `clear` folds into `low` here, so pulling Natural Language out to the `—`
    # state makes NO change to the binary label the live producer/consumer use today — the new
    # `—/—` distinction rides only in tier4/filetype, for the consumer-wiring step to come.
    tier = "low" if tier4 in SAFE_TIERS else "high"

    # Legacy aggregate buckets (high_risk = anything above the safe states).
    high_risk = [b["path"] for b in by_file if combine(b["filetype"], b["depth"]) not in SAFE_TIERS]
    low_risk = [b["path"] for b in by_file if combine(b["filetype"], b["depth"]) in SAFE_TIERS]

    print(json.dumps({
        "tier": tier,        # binary low|high — keeps risk/<tier> label creation working
        "tier4": tier4,      # nope|high|med|low|clear (clear = —/—; for the consumer-wiring increment)
        "filetype": filetype,
        "depth": depth,
        "subtier": None,  # TBD — next version (filetype circles / depth Levels); not implemented
        "by_file": by_file,
        "high_risk_files": high_risk,
        "low_risk_files": low_risk,
    }))


if __name__ == "__main__":
    main()
