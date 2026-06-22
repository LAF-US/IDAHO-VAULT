"""Classify changed file paths into the two-paired-flag risk scheme.

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
step to come (see WITNESS-THE-KEYS-ARE-THE-LEVERS-2026-06-22 and #626).
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

# --- The Architect's three blessed language circles (VAULT-CONVENTIONS § File Types) ---
NATURAL_LANGUAGE = {".md", ".markdown", ".txt", ".rtf"}          # Logan's prose surface
MACHINE_DOC = {".json", ".yaml", ".yml", ".toml", ".csv",        # declarative: describes
               ".xml", ".ini", ".cfg", ".conf"}
COMPUTER_CODE = {".py", ".sh", ".bash", ".ps1", ".bat", ".cmd",  # imperative: executes
                 ".js", ".ts", ".ipynb"}  # .ipynb = the "missing middle"; reviewed via its .md twin
INERT_ASSET = {".pdf", ".png", ".jpg", ".jpeg", ".gif", ".svg",  # binary/asset content
               ".webp", ".ico", ".mp3", ".mp4", ".ics", ".mtl", ".obj"}

# TUNABLE filetype cut across the circles. The blueprint (WITNESS-THE-KEYS-ARE-THE-LEVERS,
# 2026-06-22) gives the filetype axis a real `—` (None) state — one blessed circle per state:
#   Natural Language       -> `—` (None: prose carries NO flag)   <- THIS STEP pulls NL out of `low`
#   Machine Documentation  -> low   (declarative; + inert assets, provisionally — see witness `*`)
#   Computer Code          -> med   (executes)
# unrecognized extension   -> med   (conservative within the maze axis)
_NONE_TYPES = NATURAL_LANGUAGE                 # prose -> `—` (no filetype flag); the `—/—` clear cell
_LOW_TYPES = MACHINE_DOC | INERT_ASSET         # declarative / inert -> low
_MED_TYPES = COMPUTER_CODE                     # executes -> med

# --- Protected-surface pin (safety override; TUNABLE -> delegate to CODEOWNERS) ---
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
_TOP_DOTFOLDER_RE = re.compile(r"^\.[a-zA-Z]")


def in_nest(path: str) -> bool:
    """A path is in the `!` Swarmic Nest — nested `!/...` or a flattened `!`-prefixed
    root alias (NETWEB: '-' aliases '/'). VAULT-CONVENTIONS § Root Folder Semantics."""
    return path.startswith("!")


def is_still_point(path: str) -> bool:
    """The canon core / Level 7 — the inmost still point, `Esto Perpetua!`
    ('do not move, do not expire'). Structural: `Esto Perpetua!` must appear as a path
    SEGMENT *inside the Nest* — nested `.../Esto Perpetua!/...` or the flattened `!`-alias
    form (NETWEB: '-' aliases '/') — not a bare substring, so a maze note merely *named*
    with the text is never `nope`. Within the Nest the segment match errs toward `nope`
    (over-protect) — the safe direction for the canon core."""
    return in_nest(path) and "Esto Perpetua!" in re.split(r"[-/]", path)


def filetype_flag(path: str) -> str | None:
    """None | low | med for a maze (non-Nest) file, by its blessed-circle membership.
    None is the `—` state: Natural Language (prose) carries NO filetype flag, so a
    prose-only maze PR lands in the `—/—` clear cell. Machine Documentation / inert
    assets -> low; Computer Code -> med; unrecognized -> med (conservative)."""
    ext = posixpath.splitext(path)[1].lower()
    if ext in _MED_TYPES:
        return "med"
    if ext in _LOW_TYPES:
        return "low"
    if ext in _NONE_TYPES:
        return None  # Natural Language -> the `—` state (no flag)
    return "med"  # unrecognized type: conservative (TUNABLE)


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
    if "/" in path and _TOP_DOTFOLDER_RE.match(path):
        return (None, "high")
    return (filetype_flag(path), None)


_FT_ORD = {None: 0, "low": 1, "med": 2}
_DP_ORD = {None: 0, "high": 1, "nope": 2}


def combine(filetype, depth) -> str:
    """Collapse the (filetype, depth) pair to one descriptor: nope > high > med > low > clear.
    `clear` is the `—/—` state — NO flag on either axis (a prose-only maze file) — kept
    DISTINCT from `low` so a later auto-merge gate can key on it (blueprint: `—/—` auto-merges
    on open; `low` is a flag that holds). For the binary legacy `tier`, `clear` folds back into
    `low` (see main) so this distinction changes no current label behavior."""
    if depth == "nope":
        return "nope"
    if depth == "high":
        return "high"
    if filetype == "med":
        return "med"
    if filetype == "low":
        return "low"
    return "clear"  # —/— : neither sorter fired


def main():
    paths = [line.strip() for line in sys.stdin if line.strip()]
    by_file = []
    for p in paths:
        ft, dp = classify_file(p)
        by_file.append({"path": p, "filetype": ft, "depth": dp})

    filetype = max((b["filetype"] for b in by_file), key=lambda x: _FT_ORD[x], default=None)
    depth = max((b["depth"] for b in by_file), key=lambda x: _DP_ORD[x], default=None)
    tier4 = combine(filetype, depth)            # nope|high|med|low|clear
    # Binary legacy contract (risk/<tier>): the SAFE states (clear + low) -> low; everything
    # above -> high. `clear` folds into `low` here, so pulling Natural Language out to the `—`
    # state makes NO change to the binary label the live producer/consumer use today — the new
    # `—/—` distinction rides only in tier4/filetype, for the consumer-wiring step to come.
    _SAFE = ("clear", "low")
    tier = "low" if tier4 in _SAFE else "high"

    # Legacy aggregate buckets (high_risk = anything above the safe states).
    high_risk = [b["path"] for b in by_file if combine(b["filetype"], b["depth"]) not in _SAFE]
    low_risk = [b["path"] for b in by_file if combine(b["filetype"], b["depth"]) in _SAFE]

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
