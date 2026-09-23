#!/usr/bin/env python3
"""Census of every branch on a remote, measured against the base branch.

Files the ARBORSCAPING / ARCHIPELAGO branch census as a command instead of a
hand-tended document. Run it and the current picture comes out; a dated report
under `!/` is one run's output, kept as evidence, never edited by hand.

For each branch on the remote it records:

- lineage: a fork of the base (merge base and its date) or an island (no merge
  base). Per `!/ARCHIPELAGO-ISLAND-CENSUS-PROTOCOL-v0-2026-06-02.md`, a ref
  with no merge base is an island, not "ahead" or "behind";
- own commits: non-merge commits no other ref on the remote reaches
  (`git rev-list --no-merges <branch> --not <base> <every other branch>`);
  a branch whose only commit of its own is a merge counts as having none;
- the paths those commits touched, and for each whether the base lacks it,
  holds it identical, or holds a different version;
- the whole tree against the base's tree (`git diff --name-status`);
- root commits and the oldest commit date the branch reaches;
- last commit date and author;
- pull-request history, when a PR file is supplied (see --prs);
- ARCHIPELAGO visibility and risk classes.

Usage:
  python3 .github/scripts/branch_census.py                  # Markdown to stdout
  python3 .github/scripts/branch_census.py --fetch --out X  # fetch --prune first, write X
  python3 .github/scripts/branch_census.py --update NOTE    # refresh the block in NOTE
  python3 .github/scripts/branch_census.py --json ROWS      # rows with full path lists
  python3 .github/scripts/branch_census.py --prs prs.jsonl  # join PR history

PR history is read from a JSON Lines file, one object per pull request with
`head`, `number`, `state` and `merged` keys. `gh` produces it:

  gh api --paginate "repos/LAF-US/IDAHO-VAULT/pulls?state=all&per_page=100" \\
    --jq '.[] | {head: .head.ref, number: .number, state: .state,
                 merged: (.merged_at != null)}' > prs.jsonl

Without --prs the PR column reads "not fetched". The script never calls
GitHub itself and never writes to git beyond the opt-in `--fetch`: no ref is
created, moved or deleted, no history rewritten, nothing merged.

The generated block in a note sits between two marker lines:

  <!-- branch-census:begin -->
  <!-- branch-census:end -->

--update replaces what lies between them and nothing else, then sets the
note's `updated:` frontmatter date and `**Last Updated:**` footer line to
today (`!/VAULT-METADATA-STANDARD.md` asks that `updated` move when the facts
do).
"""

from __future__ import annotations

import argparse
import collections
import datetime as dt
import json
import re
import subprocess
import sys
from pathlib import Path

BEGIN = "<!-- branch-census:begin -->"
END = "<!-- branch-census:end -->"

# Branch-name families, longest-prefix-wins order is not needed: none nests.
FAMILIES = (
    "claude/", "codex/", "copilot/", "dependabot/", "bot/daily-rollover",
    "ingest-", "gh-readonly-queue/", "logan/", "orphancry/", "recovered/",
    "wayback-audit", "agent/", "test/", "review/", "hyperagent/", "antigravity/",
)
# Refs a machine minted with no hand on them: the merge queue's scratch
# branches, the daily-rollover and ingest bots, Dependabot.
GENERATED_PREFIXES = ("gh-readonly-queue/", "bot/daily-rollover", "ingest-", "dependabot/")
QUEUE_PREFIX = "gh-readonly-queue/"
SHOW_PATHS = 3


# --------------------------------------------------------------------------- #
# git plumbing — read-only, bytes in and out, NUL-delimited wherever paths appear
# --------------------------------------------------------------------------- #


def git(cwd: Path, *args: str, stdin: bytes | None = None, ok: tuple[int, ...] = (0,)) -> bytes:
    """Run one git command; return stdout. Exit codes outside ``ok`` raise."""
    result = subprocess.run(
        ["git", "-C", str(cwd), *args], input=stdin, capture_output=True, check=False
    )
    if result.returncode not in ok:
        raise RuntimeError(
            f"git {' '.join(args)} failed ({result.returncode}): "
            f"{result.stderr.decode('utf-8', 'replace').strip()}"
        )
    return result.stdout


def text(raw: bytes) -> str:
    return raw.decode("utf-8", "replace")


def list_branches(cwd: Path, remote: str, base: str) -> list[tuple[str, str, str]]:
    """(name, sha, short sha) for every branch on ``remote`` except HEAD and the base."""
    out = text(git(
        cwd, "for-each-ref",
        "--format=%(refname:short)%00%(objectname)%00%(objectname:short)",
        f"refs/remotes/{remote}/",
    ))
    rows = []
    prefix = f"{remote}/"
    for line in out.splitlines():
        ref, sha, short = line.split("\0")
        name = ref[len(prefix):] if ref.startswith(prefix) else ref
        if name in ("HEAD", base):
            continue
        rows.append((name, sha, short))
    return rows


def tree(cwd: Path, ref: str) -> dict[str, str]:
    """path -> object sha for every entry in ``ref``'s tree."""
    out = git(cwd, "ls-tree", "-r", "-z", ref)
    result: dict[str, str] = {}
    for rec in out.split(b"\0"):
        if not rec:
            continue
        meta, path = rec.split(b"\t", 1)
        result[text(path)] = text(meta.split()[2])
    return result


def own_commits(cwd: Path, ref: str, negatives: list[str]) -> list[str]:
    """Non-merge commits ``ref`` reaches that none of ``negatives`` reach."""
    out = text(git(cwd, "rev-list", "--no-merges", ref, "--not", *negatives))
    return out.split()


def touched_paths(cwd: Path, commits: list[str]) -> set[str]:
    """Union of paths the given commits changed, each against its parent."""
    if not commits:
        return set()
    stdin = ("\n".join(commits) + "\n").encode()
    out = git(
        cwd, "diff-tree", "--stdin", "--root", "--no-commit-id", "-r",
        "--name-only", "-z", stdin=stdin,
    )
    return {text(p) for p in out.split(b"\0") if p}


def tree_diff(cwd: Path, base_ref: str, ref: str) -> collections.Counter:
    """Count of A/D/M/R/... statuses between two whole trees."""
    out = git(cwd, "diff", "--name-status", "-z", base_ref, ref)
    parts = out.split(b"\0")
    counts: collections.Counter = collections.Counter()
    i = 0
    while i < len(parts) and parts[i]:
        letter = chr(parts[i][0])
        counts[letter] += 1
        i += 3 if letter in "RC" else 2
    return counts


def merge_base(cwd: Path, base_ref: str, ref: str) -> str | None:
    out = text(git(cwd, "merge-base", base_ref, ref, ok=(0, 1))).strip()
    return out or None


def is_ancestor(cwd: Path, ref: str, of: str) -> bool:
    result = subprocess.run(
        ["git", "-C", str(cwd), "merge-base", "--is-ancestor", ref, of],
        capture_output=True, check=False,
    )
    return result.returncode == 0


def commit_date(cwd: Path, sha: str) -> str:
    return text(git(cwd, "log", "-1", "--format=%cs", sha)).strip()


def last_commit(cwd: Path, ref: str) -> tuple[str, str]:
    date, author = text(git(cwd, "log", "-1", "--format=%cs%x00%an", ref)).rstrip("\n").split("\0")
    return date, author


def history_span(cwd: Path, ref: str) -> tuple[int, int, str]:
    """(commit count, root commit count, oldest commit date) reachable from ``ref``."""
    dates = text(git(cwd, "log", "--format=%cs", ref)).split()
    roots = int(text(git(cwd, "rev-list", "--max-parents=0", "--count", ref)).strip())
    return len(dates), roots, min(dates) if dates else ""


def older_history(cwd: Path, remote: str, before: str, detail_before: str | None) -> dict:
    """Commits on the remote dated before ``before`` (the base's oldest), by month;
    and, dated before ``detail_before`` when given, by (date, subject)."""
    out = text(git(cwd, "log", f"--remotes={remote}", "--format=%cs%x00%s"))
    months: collections.Counter = collections.Counter()
    detail: collections.Counter = collections.Counter()
    for line in out.splitlines():
        date, _, subject = line.partition("\0")
        if date < before:
            months[date[:7]] += 1
        if detail_before and date < detail_before:
            detail[(date, subject)] += 1
    return {
        "before": before,
        "months": sorted(months.items()),
        "detail_before": detail_before,
        "detail": [(d, n, s) for (d, s), n in sorted(detail.items())],
    }


# --------------------------------------------------------------------------- #
# pull-request history and classification
# --------------------------------------------------------------------------- #


def read_prs(path: Path) -> dict[str, list[dict]]:
    """Group a JSON Lines PR export by head branch, oldest number first."""
    grouped: dict[str, list[dict]] = collections.defaultdict(list)
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        item = json.loads(line)
        grouped[item["head"]].append({
            "number": int(item["number"]),
            "state": item["state"],
            "merged": bool(item.get("merged", False)),
        })
    for history in grouped.values():
        history.sort(key=lambda p: p["number"])
    return dict(grouped)


def pr_class(history: list[dict] | None) -> str:
    if history is None:
        return "not fetched"
    if not history:
        return "no PR"
    if any(p["state"] == "open" for p in history):
        return "open PR"
    if any(p["merged"] for p in history):
        return "merged PR"
    return "closed PR, unmerged"


def pr_detail(history: list[dict] | None) -> str:
    if not history:
        return ""
    return "; ".join(
        f"#{p['number']} {'merged' if p['merged'] else p['state']}" for p in history
    )


def family(name: str) -> str:
    for prefix in FAMILIES:
        if name.startswith(prefix):
            return prefix
    return "other"


def visibility(row: dict) -> str:
    """ARCHIPELAGO visibility class."""
    if row["ancestral"]:
        return "ANCESTRAL"
    if row["lineage"] == "island":
        return "ORPHAN-LINEAGE"
    return "BRANCH-ONLY"


def risk(row: dict) -> str:
    """ARCHIPELAGO risk class. Content is not read here, so SECRET-RISK and
    DOCTRINE-RISK cannot be assigned by this script; those need a reader."""
    if row["pr_class"] == "open PR":
        return "LIVING-WORK"
    if row["branch"].startswith(GENERATED_PREFIXES):
        return "GENERATED-JUNK"
    if row["lineage"] == "island":
        return "REQUIRES-LOGAN"
    return "EVIDENCE-CANDIDATE"


# --------------------------------------------------------------------------- #
# the census
# --------------------------------------------------------------------------- #


def census(cwd: Path, remote: str, base: str, prs: dict[str, list[dict]] | None,
           history_before: str | None, log=lambda *_: None) -> tuple[dict, list[dict], dict]:
    base_ref = f"{remote}/{base}"
    base_tree = tree(cwd, base_ref)
    base_count, base_roots, base_oldest = history_span(cwd, base_ref)
    base_date, _ = last_commit(cwd, base_ref)
    base_facts = {
        "ref": base_ref,
        "tip": text(git(cwd, "rev-parse", "--short", base_ref)).strip(),
        "tip_date": base_date,
        "commits": base_count,
        "roots": base_roots,
        "oldest": base_oldest,
        "paths": len(base_tree),
    }

    branches = list_branches(cwd, remote, base)
    refs = {name: f"{remote}/{name}" for name, _, _ in branches}
    rows: list[dict] = []
    for i, (name, sha, short) in enumerate(branches, 1):
        log(f"[{i}/{len(branches)}] {name}")
        ref = refs[name]
        negatives = [base_ref] + [r for n, r in refs.items() if n != name]
        own = own_commits(cwd, ref, negatives)
        paths = sorted(touched_paths(cwd, own))
        lacks: list[str] = []
        differ: list[str] = []
        identical = 0
        if paths:
            tip_tree = tree(cwd, ref)
            for path in paths:
                tip_sha = tip_tree.get(path)
                if tip_sha is None:
                    continue  # deleted on the branch itself
                base_sha = base_tree.get(path)
                if base_sha is None:
                    lacks.append(path)
                elif base_sha == tip_sha:
                    identical += 1
                else:
                    differ.append(path)
        mb = merge_base(cwd, base_ref, ref)
        counts = tree_diff(cwd, base_ref, ref)
        total, roots, oldest = history_span(cwd, ref)
        last_date, author = last_commit(cwd, ref)
        history = prs.get(name, []) if prs is not None else None
        row = {
            "branch": name,
            "tip": short,
            "sha": sha,
            "lineage": "fork" if mb else "island",
            "merge_base": mb,
            "merge_base_date": commit_date(cwd, mb) if mb else None,
            "ancestral": is_ancestor(cwd, ref, base_ref),
            "own_commits": len(own),
            "files_touched": len(paths),
            "base_lacks": len(lacks),
            "differ": len(differ),
            "identical": identical,
            "base_lacks_paths": lacks,
            "differ_paths": differ,
            "tree_only_here": counts.get("A", 0),
            "tree_only_base": counts.get("D", 0),
            "tree_differ": counts.get("M", 0),
            "tree_renamed": counts.get("R", 0),
            "commits_reachable": total,
            "root_commits": roots,
            "oldest_commit": oldest,
            "last_commit": last_date,
            "last_author": author,
            "pr_history": history,
            "pr_class": pr_class(history),
            "pr_detail": pr_detail(history),
            "family": family(name),
        }
        row["visibility_class"] = visibility(row)
        row["risk_class"] = risk(row)
        rows.append(row)
    rows.sort(key=lambda r: r["branch"])
    return base_facts, rows, older_history(cwd, remote, base_oldest, history_before)


# --------------------------------------------------------------------------- #
# Markdown
# --------------------------------------------------------------------------- #


def esc(value: str) -> str:
    return value.replace("|", "\\|")


def lineage(row: dict) -> str:
    return "island" if row["lineage"] == "island" else f"forks {row['merge_base_date']}"


def render(base: dict, rows: list[dict], older: dict, *,
           remote: str, since: str, tree_threshold: int, command: str, when: str) -> str:
    islands = [r for r in rows if r["lineage"] == "island"]
    forks = [r for r in rows if r["lineage"] == "fork"]
    salvage = sorted((r for r in rows if r["base_lacks"]), key=lambda r: (-r["base_lacks"], r["branch"]))
    identical = [r for r in rows if r["files_touched"] and not r["base_lacks"] and not r["differ"]]
    no_own = [r for r in rows if r["own_commits"] == 0]
    queue = [r for r in rows if r["branch"].startswith(QUEUE_PREFIX)]
    recent = sorted(
        (r for r in rows if r["last_commit"] >= since or (r["merge_base_date"] or "") >= since),
        key=lambda r: r["last_commit"], reverse=True,
    )
    # Forks only: an island's whole tree predates the replant, so tree-against-
    # tree it differs wholesale and the number says nothing a reader can act on.
    # The per-branch figure is still in the full census and in --json.
    wide = sorted((r for r in forks if r["tree_only_here"] >= tree_threshold),
                  key=lambda r: -r["tree_only_here"])
    prc = collections.Counter(r["pr_class"] for r in rows)
    prc_i = collections.Counter(r["pr_class"] for r in islands)
    prc_f = collections.Counter(r["pr_class"] for r in forks)
    open_prs = ", ".join(
        f"#{p['number']} (head `{esc(r['branch'])}`)"
        for r in rows for p in (r["pr_history"] or []) if p["state"] == "open"
    )
    base_name = base["ref"].split("/", 1)[1]

    o: list[str] = []
    w = o.append
    w(BEGIN)
    w("")
    w(f"Generated {when} by `.github/scripts/branch_census.py` from `{remote}`, base "
      f"`{base['ref']}` at `{base['tip']}` ({base['tip_date']}). Do not edit between the "
      f"markers; rerun instead:")
    w("")
    w("```text")
    w(command)
    w("```")
    w("")
    w("## Headline")
    w("")
    w("| Measure | Value |")
    w("|---|---|")
    w(f"| Branches on `{remote}` besides `{base_name}` | {len(rows)} |")
    w(f"| `{base_name}` | {base['commits']:,} commits, tip `{base['tip']}` ({base['tip_date']}), "
      f"oldest commit {base['oldest']}, {base['roots']} root commits, {base['paths']:,} paths |")
    w(f"| Forks of `{base_name}` (share a merge base) | {len(forks)} |")
    w(f"| Islands (no merge base with `{base_name}`) | {len(islands)} |")
    w(f"| Branches whose own commits hold paths `{base_name}` lacks | {len(salvage)} |")
    w(f"| Branches whose own paths are all in `{base_name}`, identical | {len(identical)} |")
    w(f"| Branches with no non-merge commit of their own | {len(no_own)} |")
    w(f"| Open pull requests | {prc.get('open PR', 0)}{(' — ' + open_prs) if open_prs else ''} |")
    w(f"| Branches whose PR merged and the branch stayed | {prc.get('merged PR', 0)} |")
    w(f"| Branches whose PRs closed unmerged | {prc.get('closed PR, unmerged', 0)} |")
    w(f"| Branches that never had a PR | {prc.get('no PR', 0)} |")
    if prc.get("not fetched"):
        w("| PR history | not fetched (run with `--prs`) |")
    w("")
    w("## Two populations")
    w("")
    w("An island carries a whole lineage `%s` does not share, so its ahead/behind count "
      "measures that lineage, not work waiting to land. What an island contributed is its "
      "own commits, isolated below." % base_name)
    w("")
    w("| Population | Branches | Closed unmerged | Merged | Never a PR | Open |")
    w("|---|---|---|---|---|---|")
    w(f"| Islands | {len(islands)} | {prc_i.get('closed PR, unmerged', 0)} | {prc_i.get('merged PR', 0)} "
      f"| {prc_i.get('no PR', 0)} | {prc_i.get('open PR', 0)} |")
    w(f"| Forks | {len(forks)} | {prc_f.get('closed PR, unmerged', 0)} | {prc_f.get('merged PR', 0)} "
      f"| {prc_f.get('no PR', 0)} | {prc_f.get('open PR', 0)} |")
    w("")
    w(f"## Recent: forked or committed since {since}")
    w("")
    w(f"| Branch | Lineage | Own commits | `{base_name}` lacks | Differ | Last commit | PR |")
    w("|---|---|---|---|---|---|---|")
    for r in recent:
        w(f"| `{esc(r['branch'])}` | {lineage(r)} | {r['own_commits']} | {r['base_lacks']:,} "
          f"| {r['differ']:,} | {r['last_commit']} {esc(r['last_author'])} | {r['pr_class']} |")
    w("")
    w(f"## Forks whose whole tree holds {tree_threshold:,} or more paths `{base_name}` lacks")
    w("")
    w("A fork that carries a lineage rather than a diff shows few own commits above; this "
      "measures forks tree against tree. \"Only here\" is a path the branch has and "
      f"`{base_name}` lacks; \"only base\" the reverse. Islands are left out: their whole "
      "tree predates the replant and differs wholesale. \"Only here\" also counts every "
      f"path `{base_name}` has deleted since the fork point, so ordinary forks share a "
      "baseline below the threshold.")
    w("")
    w("| Branch | Only here | Only base | Differ | Renamed | Root commits | Oldest commit |")
    w("|---|---|---|---|---|---|---|")
    for r in wide:
        w(f"| `{esc(r['branch'])}` | {r['tree_only_here']:,} | {r['tree_only_base']:,} "
          f"| {r['tree_differ']:,} | {r['tree_renamed']:,} | {r['root_commits']} | {r['oldest_commit']} |")
    if not wide:
        w("| (none) | | | | | | |")
    w("")
    w(f"## History older than anything `{base_name}` reaches")
    w("")
    if older["months"]:
        w(f"`{base_name}` reaches nothing dated before {base['oldest']}. Across `{remote}` "
          f"there are {sum(n for _, n in older['months']):,} commits dated earlier, by month:")
        w("")
        w("| Month | Commits |")
        w("|---|---|")
        for month, n in older["months"]:
            w(f"| {month} | {n:,} |")
    else:
        w(f"None: no commit on `{remote}` is dated before {base['oldest']}.")
    if older["detail_before"]:
        w("")
        w(f"Dated before {older['detail_before']} (`--history-before`), one row per date and "
          f"subject, {sum(n for _, n, _ in older['detail']):,} commits:")
        w("")
        w("| Date | Commits | Subject |")
        w("|---|---|---|")
        for date, n, subject in older["detail"]:
            w(f"| {date} | {n} | {esc(subject)} |")
        if not older["detail"]:
            w("| (none) | | |")
    w("")
    w("## By family")
    w("")
    w(f"| Family | Branches | Islands | With paths `{base_name}` lacks | With paths that differ "
      f"| Own paths all identical, or nothing own |")
    w("|---|---|---|---|---|---|")
    fams = collections.Counter(r["family"] for r in rows)
    for fam, _ in sorted(fams.items(), key=lambda kv: (-kv[1], kv[0])):
        g = [r for r in rows if r["family"] == fam]
        w(f"| `{fam}` | {len(g)} | {sum(1 for r in g if r['lineage'] == 'island')} "
          f"| {sum(1 for r in g if r['base_lacks'])} | {sum(1 for r in g if r['differ'])} "
          f"| {sum(1 for r in g if not r['base_lacks'] and not r['differ'])} |")
    w("")
    w(f"## Salvage candidates: own commits hold paths `{base_name}` lacks")
    w("")
    w("Ranked by that count. It counts paths, not worth: a path the base lacks may be a "
      "note worth keeping, a file removed on purpose, or generated residue. Up to "
      f"{SHOW_PATHS} paths are shown per branch; `--json` carries them all.")
    w("")
    w(f"| Branch | Lineage | Own commits | `{base_name}` lacks | Differ | Last commit | PR "
      f"| Paths `{base_name}` lacks |")
    w("|---|---|---|---|---|---|---|---|")
    for r in salvage:
        detail = f" ({esc(r['pr_detail'])})" if r["pr_detail"] else ""
        shown = "<br>".join(f"`{esc(p)}`" for p in r["base_lacks_paths"][:SHOW_PATHS])
        if r["base_lacks"] > SHOW_PATHS:
            shown += f"<br>… and {r['base_lacks'] - SHOW_PATHS:,} more"
        w(f"| `{esc(r['branch'])}` | {lineage(r)} | {r['own_commits']} | {r['base_lacks']:,} "
          f"| {r['differ']:,} | {r['last_commit']} {esc(r['last_author'])} "
          f"| {r['pr_class']}{detail} | {shown} |")
    w("")
    w(f"## Own paths all in `{base_name}`, identical")
    w("")
    w("Nothing to salvage by content. Under ARBORSCAPE these are PRUNE candidates once "
      "Logan says so; nothing is pruned by this census.")
    w("")
    for r in identical:
        w(f"- `{esc(r['branch'])}` — {lineage(r)}, own commits {r['own_commits']}, "
          f"paths {r['files_touched']}, last {r['last_commit']}, {r['pr_class']}")
    if not identical:
        w("- (none)")
    w("")
    w("## No non-merge commit of their own")
    w("")
    w("Every non-merge commit each reaches is reachable from another ref, so the branch "
      "adds at most a merge. ANCESTRAL means the tip itself is reachable from "
      f"`{base_name}`.")
    w("")
    for r in no_own:
        w(f"- `{esc(r['branch'])}` — {lineage(r)}, {r['visibility_class']}, "
          f"last {r['last_commit']}, {r['pr_class']}")
    if not no_own:
        w("- (none)")
    w("")
    w("## Merge-queue leftovers")
    w("")
    w(f"`{QUEUE_PREFIX}*` refs are the temporary branches GitHub's merge queue builds "
      "each candidate on and normally deletes.")
    w("")
    for r in queue:
        w(f"- `{esc(r['branch'])}` — own commits {r['own_commits']}, `{base_name}` lacks "
          f"{r['base_lacks']}, differ {r['differ']}, last {r['last_commit']}")
    if not queue:
        w("- (none)")
    w("")
    w("## Full census")
    w("")
    w("One row per branch. Own commits are non-merge commits no other ref reaches. Classes per "
      "`!/ARCHIPELAGO-ISLAND-CENSUS-PROTOCOL-v0-2026-06-02.md`; SECRET-RISK and "
      "DOCTRINE-RISK need a reader and are not assigned here.")
    w("")
    w(f"| Branch | Lineage | Own commits | Paths touched | `{base_name}` lacks | Differ "
      f"| Identical | Tree only here | Last commit | Author | PR | Visibility | Risk |")
    w("|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    for r in rows:
        w(f"| `{esc(r['branch'])}` | {lineage(r)} | {r['own_commits']} | {r['files_touched']:,} "
          f"| {r['base_lacks']:,} | {r['differ']:,} | {r['identical']:,} | {r['tree_only_here']:,} "
          f"| {r['last_commit']} | {esc(r['last_author'])} | {r['pr_class']} "
          f"| {r['visibility_class']} | {r['risk_class']} |")
    w("")
    w(END)
    return "\n".join(o) + "\n"


def splice(note: str, block: str, today: str) -> str:
    """Replace the block between the markers in ``note``; bump its dates."""
    lines = note.split("\n")
    starts = [i for i, line in enumerate(lines) if line.strip() == BEGIN]
    ends = [i for i, line in enumerate(lines) if line.strip() == END]
    if len(starts) != 1 or len(ends) != 1 or ends[0] < starts[0]:
        raise SystemExit(f"note needs exactly one {BEGIN} … {END} block")
    new = lines[:starts[0]] + block.rstrip("\n").split("\n") + lines[ends[0] + 1:]
    out = "\n".join(new)
    out = re.sub(r"^(updated:\s*)\d{4}-\d{2}-\d{2}\s*$", rf"\g<1>{today}", out, count=1, flags=re.M)
    out = re.sub(r"^(- \*\*Last Updated:\*\*\s*)\d{4}-\d{2}-\d{2}\s*$", rf"\g<1>{today}", out,
                 count=1, flags=re.M)
    return out


# --------------------------------------------------------------------------- #


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--repo", type=Path, default=Path("."), help="clone to census (default: .)")
    parser.add_argument("--remote", default="origin")
    parser.add_argument("--base", default="main")
    parser.add_argument("--fetch", action="store_true", help="git fetch --prune the remote first")
    parser.add_argument("--prs", type=Path, help="JSON Lines PR export (see module docstring)")
    parser.add_argument("--since", help="'recent' cutoff, YYYY-MM-DD (default: 90 days ago)")
    parser.add_argument("--tree-threshold", type=int, default=1000,
                        help="'only here' path count that puts a fork in the tree table")
    parser.add_argument("--history-before", metavar="YYYY-MM-DD",
                        help="also list commits older than this date, one row per date and subject")
    parser.add_argument("--out", type=Path, help="write the Markdown block here")
    parser.add_argument("--update", type=Path, help="replace the block between markers in this note")
    parser.add_argument("--json", type=Path, help="write the rows as JSON here")
    parser.add_argument("--quiet", action="store_true", help="no per-branch progress on stderr")
    args = parser.parse_args()

    today = dt.datetime.now(dt.timezone.utc)
    since = args.since or (today - dt.timedelta(days=90)).strftime("%Y-%m-%d")
    if args.fetch:
        git(args.repo, "fetch", "--prune", args.remote)
    prs = read_prs(args.prs) if args.prs else None
    log = (lambda *_: None) if args.quiet else (lambda m: print(m, file=sys.stderr))

    base, rows, older = census(args.repo, args.remote, args.base, prs, args.history_before, log=log)
    # The recorded command names what shaped the census, not where this run
    # happened to put its files: paths are reduced to their basenames.
    parts = ["python3 .github/scripts/branch_census.py"]
    if args.remote != "origin":
        parts.append(f"--remote {args.remote}")
    if args.base != "main":
        parts.append(f"--base {args.base}")
    if args.fetch:
        parts.append("--fetch")
    if args.prs:
        parts.append(f"--prs {args.prs.name}")
    parts.append(f"--since {since}")
    if args.tree_threshold != 1000:
        parts.append(f"--tree-threshold {args.tree_threshold}")
    if args.history_before:
        parts.append(f"--history-before {args.history_before}")
    if args.update:
        try:
            note = args.update.resolve().relative_to(args.repo.resolve())
        except ValueError:
            note = args.update
        parts.append(f"--update '{note.as_posix()}'")
    command = " ".join(parts)
    block = render(
        base, rows, older, remote=args.remote, since=since,
        tree_threshold=args.tree_threshold, command=command,
        when=today.strftime("%Y-%m-%d %H:%M UTC"),
    )

    if args.json:
        args.json.write_text(json.dumps(rows, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    if args.update:
        note = args.update.read_text(encoding="utf-8")
        args.update.write_text(splice(note, block, today.strftime("%Y-%m-%d")), encoding="utf-8")
        log(f"updated {args.update}")
    if args.out:
        args.out.write_text(block, encoding="utf-8")
        log(f"wrote {args.out}")
    if not (args.out or args.update):
        sys.stdout.write(block)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
