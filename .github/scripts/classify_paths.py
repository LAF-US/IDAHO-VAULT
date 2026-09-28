"""Classify changed file paths into the two-axis risk scheme."""
# Two independent axes, each scored for every file from its PATH alone:
#
#   * filetype  — WHAT the file is, by extension:
#       Natural Language (.md/.txt/...)             -> None  (no flag)
#       Machine Documentation (.json/.yaml/...; inert assets) -> "low"
#       Computer Code (.py/.sh/...)                 -> "med"
#       unrecognized extension                      -> "med" (conservative)
#   * filedepth — WHERE the file sits, by its literal directory prefix (see filedepth_flag):
#       repo root (not under "!/")                  -> None
#       inside "!/" (above the inner prefix)        -> "high"
#       inside "!/!/__!__/!/" and below             -> "nope"
#
# The two scores are independent and compose. Downstream, review_feedback_loop.py and
# agent-auto-pr.yml map the fields to flat labels: filetype -> risk/low|risk/med,
# filedepth -> risk/high|risk/nope; None on an axis stamps no label; None/None stamps none.
#
# JSON output (stdin: newline-separated paths):
#   {
#     "tier":  "low"|"high",                       # binary: SAFE_TIERS -> low, everything riskier -> high
#     "tier4": "clear"|"low"|"med"|"high"|"nope",  # composed read (nope>high>med>low>clear)
#     "filetype": None|"low"|"med",                # riskiest filetype across the changeset
#     "filedepth": None|"high"|"nope",             # riskiest filedepth across the changeset
#     "subtier":  None,                            # not implemented
#     "by_file":  [{"path","filetype","filedepth"}, ...],
#     "high_risk_files": [...], "low_risk_files": [...],
#   }
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


def combine(filetype, filedepth) -> str:
    """Collapse the (filetype, filedepth) pair to one tier by TIER_PRECEDENCE (riskiest wins)."""
    # "clear" when both are None.
    return riskiest(filetype, filedepth) or CLEAR_TIER


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
