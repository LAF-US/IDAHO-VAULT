"""Classify changed file paths into the two-paired-flag risk scheme.

Conceptualized in the planning session of 2026-06-21 and witnessed in
`WITNESS-THE-KEYS-ARE-THE-LEVERS-2026-06-21.md`; this is its first implementation,
replacing the prior binary (high|low, fail-safe-to-high) classifier.

THE SCHEME — two INDEPENDENT paired flags. A changeset carries either version of
each, or neither (per Logan, 2026-06-21):

  * filetype flag : low | med    — the "maze": WHAT KIND of file it is.
                                   Tags files OUTSIDE the `!` Nest, by the Architect's
                                   three blessed language circles (VAULT-CONVENTIONS
                                   § File Types).
  * depth flag    : high | nope  — the "labyrinth": HOW DEEP into the `!` Nest.
                                   Tags files INSIDE the `!` Nest, by the seven Levels
                                   (the Sierpinski spine ~/ root -> Esto Perpetua!).

Per Logan's correction: "low/med apply to filetypes; high/nope apply to depth."
So a maze file is tagged by filetype only; a Nest file is tagged by depth only —
depth supersedes filetype inside the labyrinth.

JSON output (backward-compatible: keeps `tier` + `*_risk_files` for agent-auto-pr):
  {
    "tier": "low"|"med"|"high"|"nope",   # derived single label: nope>high>med>low
    "filetype": "low"|"med"|None,        # riskiest filetype among maze files touched
    "depth": "high"|"nope"|None,         # deepest Nest reach among files touched
    "by_file": [{"path","filetype","depth"}...],
    "high_risk_files": [...], "low_risk_files": [...]   # legacy aggregate buckets
  }

--- TUNABLE (Logan's pins still open; marked * in the witness) ---
* FILETYPE CUT: which blessed circles are `med` vs `low`. Default: Computer Code
  (executes) -> med; Natural Language + Machine Documentation (prose/declarative) ->
  low. The "does it execute?" line.
* DEPTH THRESHOLD: where `high` becomes `nope`. Default: only the canon core /
  still-point (Esto Perpetua!, Level 7 — "do not move, do not expire") is `nope`;
  all other Nest depth is `high`.
* PROTECTED-SURFACE PIN: `.github/**`, named governance files, and persona dotfolders
  are NOT in the `!` Nest, so the pure model would tag them low/med — a DOWNGRADE of
  today's automation/governance protection. Pending Logan's decision to move that
  protection onto CODEOWNERS (a separate Key/Lever), they are kept pinned `high` here
  so this change introduces no safety regression.
"""

import json
import posixpath
import sys

# --- The Architect's three blessed language circles (VAULT-CONVENTIONS § File Types) ---
NATURAL_LANGUAGE = {".md", ".markdown", ".txt", ".rtf"}          # Logan's prose surface
MACHINE_DOC = {".json", ".yaml", ".yml", ".toml", ".csv",        # declarative: describes
               ".xml", ".ini", ".cfg", ".conf"}
COMPUTER_CODE = {".py", ".sh", ".bash", ".ps1", ".bat", ".cmd",  # imperative: executes
                 ".js", ".ts", ".ipynb"}  # .ipynb = the "missing middle"; reviewed via its .md twin
INERT_ASSET = {".pdf", ".png", ".jpg", ".jpeg", ".gif", ".svg",  # binary/asset content
               ".webp", ".ico", ".mp3", ".mp4", ".ics", ".mtl", ".obj"}

# TUNABLE filetype cut across the circles:
_LOW_TYPES = NATURAL_LANGUAGE | MACHINE_DOC | INERT_ASSET   # prose / declarative / inert -> low
_MED_TYPES = COMPUTER_CODE                                  # executes -> med
# unrecognized extension -> med (conservative within the maze axis)

# --- Protected-surface pin (safety override; TUNABLE -> delegate to CODEOWNERS) ---
PROTECTED_PREFIXES = (".github/workflows/", ".github/scripts/")
PROTECTED_EXACT = {
    "AGENTS.md", "CLAUDE.md", "CONSTITUTION.md", "DECISIONS.md", "LEVELSET.md",
    "VAULT-CONVENTIONS.md", "VAULT-TEMPLATES.md", "swarm.json", ".gitignore",
    ".github/CODEOWNERS", ".github/copilot-instructions.md",
}
# Probe/example sandboxes under the protected dirs stay low (explicit carve-out).
PROBE_PREFIXES = (".github/workflows/probe-", ".github/workflows/example-",
                  ".github/scripts/probe-", ".github/scripts/example-")


def in_nest(path: str) -> bool:
    """A path is in the `!` Swarmic Nest — nested `!/...` or a flattened `!`-prefixed
    root alias (NETWEB: '-' aliases '/'). VAULT-CONVENTIONS § Root Folder Semantics."""
    return path.startswith("!")


def is_still_point(path: str) -> bool:
    """The canon core / Level 7 — the inmost still point, `Esto Perpetua!`
    ('do not move, do not expire'), nested or in a flattened alias."""
    return "Esto Perpetua!" in path


def filetype_flag(path: str) -> str:
    """low | med for a maze (non-Nest) file, by its blessed-circle membership."""
    ext = posixpath.splitext(path)[1].lower()
    if ext in _MED_TYPES:
        return "med"
    if ext in _LOW_TYPES:
        return "low"
    return "med"  # unrecognized type: conservative (TUNABLE)


def classify_file(path: str) -> tuple:
    """Return (filetype_flag, depth_flag) for one path — exactly one axis is active.
    Maze files carry a filetype flag; Nest files carry a depth flag (depth supersedes)."""
    if is_still_point(path):
        return (None, "nope")
    if in_nest(path):
        return (None, "high")
    # Maze. Probe sandboxes stay low; protected surfaces are pinned high (safety override).
    if path.startswith(PROBE_PREFIXES):
        return ("low", None)
    if path in PROTECTED_EXACT or path.startswith(PROTECTED_PREFIXES):
        # No off-Nest 'high' exists in the pure model; pin via the depth axis to avoid
        # a protection downgrade. TUNABLE: delegate this gate to CODEOWNERS instead.
        return (None, "high")
    return (filetype_flag(path), None)


_FT_ORD = {None: 0, "low": 1, "med": 2}
_DP_ORD = {None: 0, "high": 1, "nope": 2}


def combine(filetype, depth) -> str:
    """Derive the single legacy `risk/<tier>` label: nope > high > med > low."""
    if depth == "nope":
        return "nope"
    if depth == "high":
        return "high"
    if filetype == "med":
        return "med"
    return "low"


def main():
    paths = [line.strip() for line in sys.stdin if line.strip()]
    by_file = []
    for p in paths:
        ft, dp = classify_file(p)
        by_file.append({"path": p, "filetype": ft, "depth": dp})

    filetype = max((b["filetype"] for b in by_file), key=lambda x: _FT_ORD[x], default=None)
    depth = max((b["depth"] for b in by_file), key=lambda x: _DP_ORD[x], default=None)
    tier = combine(filetype, depth)

    # Legacy aggregate buckets (high_risk = anything above low).
    high_risk = [b["path"] for b in by_file if combine(b["filetype"], b["depth"]) != "low"]
    low_risk = [b["path"] for b in by_file if combine(b["filetype"], b["depth"]) == "low"]

    print(json.dumps({
        "tier": tier,
        "filetype": filetype,
        "depth": depth,
        "by_file": by_file,
        "high_risk_files": high_risk,
        "low_risk_files": low_risk,
    }))


if __name__ == "__main__":
    main()
