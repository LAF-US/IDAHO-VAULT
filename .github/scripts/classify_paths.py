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

THE SCHEME — TWO INDEPENDENT PARALLEL ANALYSES, each scoring EVERY file on its own
axis (Logan's architecture bearing, #626 2026-06-22; restated 2026-07-06):

  * filetype path  : — | low | med   — WHAT KIND of file it is, by the Architect's three
                                     blessed language circles (VAULT-CONVENTIONS § File
                                     Types), ONE circle per state (blueprint, 2026-06-22):
                                       Natural Language (.md, prose) -> `—` (None: no flag)
                                       Machine Documentation (.json/.yaml; + inert assets) -> low
                                       Computer Code (.py/.sh/...) -> med
  * placement path : — | high | nope — WHERE it sits ("depth" is the narrow name;
                                     FILEPLACEMENT is the axis): the `!` Nest's seven
                                     Levels (high for 2-6, nope at the Level-7 still
                                     point) plus the protected surfaces pinned high
                                     (`.github/**`, root governance files, dotfolders).

Per Logan's correction: "low/med apply to filetypes; high/nope apply to depth." The two
verdicts COMPOSE into the grid — a Nest .py is ("med", "high"); a prose maze file is
(None, None), the `—/—` "clear" cell (the blueprint's auto-merge state). This supersedes
the earlier single pass where placement suppressed filetype.

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
    "filetype": None|"low"|"med",                 # riskiest filetype touched (scored for EVERY file,
                                                  #   Nest included); None = `—` (prose/NL)
    "depth": "high"|"nope"|None,                  # riskiest PLACEMENT touched (Nest depth + protected
                                                  #   pins); JSON key stays "depth" for consumers
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
import sys

# Tier precedence, riskiest -> safest. The single ordering read by riskiest() and combine().
TIER_PRECEDENCE = ("nope", "high", "med", "low", "clear")
CLEAR_TIER = "clear"                     # both axes None
SAFE_TIERS = ("clear", "low")            # fold to binary "low"; anything riskier -> binary "high"
# Fail loud on drift: the derived sets must be members of the one ordering.
assert CLEAR_TIER in TIER_PRECEDENCE, "CLEAR_TIER must be in TIER_PRECEDENCE"
assert set(SAFE_TIERS) <= set(TIER_PRECEDENCE), "SAFE_TIERS must be a subset of TIER_PRECEDENCE"

# filetype extension sets. To re-tier an extension, move it between these sets.
NATURAL_LANGUAGE = {".md", ".markdown", ".txt", ".rtf"}
MACHINE_DOC = {".json", ".yaml", ".yml", ".toml", ".csv",
               ".xml", ".ini", ".cfg", ".conf"}
COMPUTER_CODE = {".py", ".sh", ".bash", ".ps1", ".bat", ".cmd",
                 ".js", ".ts", ".ipynb"}
INERT_ASSET = {".pdf", ".png", ".jpg", ".jpeg", ".gif", ".svg",
               ".webp", ".ico", ".mp3", ".mp4", ".ics", ".mtl", ".obj"}

FILETYPE_NONE = NATURAL_LANGUAGE               # None (no flag)
FILETYPE_LOW = MACHINE_DOC | INERT_ASSET       # -> low
FILETYPE_MED = COMPUTER_CODE                   # -> med
FILETYPE_UNKNOWN_DEFAULT = "med"               # unrecognized extension -> conservative

# filedepth prefixes. A path scores by the deepest prefix it starts with; a path under
# neither prefix (repo root, including "!-…" flattened root files) scores None.
NOPE_PREFIX = "!/!/__!__/!/"   # this directory and below -> nope
HIGH_PREFIX = "!/"             # inside "!/" but above NOPE_PREFIX -> high


def filetype_flag(path: str) -> str | None:
    """Return None | "low" | "med" for a path, by its extension."""
    ext = posixpath.splitext(path)[1].lower()
    if ext in FILETYPE_MED:
        return "med"
    if ext in FILETYPE_LOW:
        return "low"
    if ext in FILETYPE_NONE:
        return None
    return FILETYPE_UNKNOWN_DEFAULT


def filedepth_flag(path: str) -> str | None:
    """Return "nope" | "high" | None for a path, by its literal directory prefix."""
    if path.startswith(NOPE_PREFIX):
        return "nope"
    if path.startswith(HIGH_PREFIX):
        return "high"
    return None


def classify_file(path: str) -> tuple:
    """Return (filetype_flag, filedepth_flag) for one path — two independent scores."""
    # Windows-style separators are normalized to '/' first so the filedepth prefixes match
    # regardless of input source (git/gh emit '/', but local/tooling input may use '\\').
    path = path.replace("\\", "/")
    return (filetype_flag(path), filedepth_flag(path))


def riskiest(*flags) -> str | None:
    """The riskiest non-None flag among `flags` by TIER_PRECEDENCE; None if all absent."""
    # Used both to aggregate one axis across files and to combine the two axes.
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
        ft, fd = classify_file(p)
        by_file.append({"path": p, "filetype": ft, "filedepth": fd})

    # Aggregate each axis to its riskiest reach across the changeset.
    filetype = riskiest(*(b["filetype"] for b in by_file))
    filedepth = riskiest(*(b["filedepth"] for b in by_file))
    tier4 = combine(filetype, filedepth)        # nope|high|med|low|clear
    tier = "low" if tier4 in SAFE_TIERS else "high"

    high_risk = [b["path"] for b in by_file if combine(b["filetype"], b["filedepth"]) not in SAFE_TIERS]
    low_risk = [b["path"] for b in by_file if combine(b["filetype"], b["filedepth"]) in SAFE_TIERS]

    print(json.dumps({
        "tier": tier,
        "tier4": tier4,
        "filetype": filetype,
        "filedepth": filedepth,
        "subtier": None,
        "by_file": by_file,
        "high_risk_files": high_risk,
        "low_risk_files": low_risk,
    }))


if __name__ == "__main__":
    main()
