#!/usr/bin/env bash
# Update open PR branches from a base branch using GitHub's native
# PUT /repos/{owner}/{repo}/pulls/{pull_number}/update-branch endpoint.
#
# Default mode is read-only. Pass --apply to request normal merge-based updates
# for clean, behind-base PR branches. It never rebases or force-pushes.
#
# Requires: gh (authenticated with pull-requests:write and contents:write), jq

set -uo pipefail

REPO="${REPO:-LAF-US/IDAHO-VAULT}"
BASE="${BASE:-main}"
APPLY=false
INCLUDE_DRAFTS=false
INCLUDE_FORKS=false
EXCLUDED_PRS=(980)
EXCLUDED_BRANCHES=("logan/obsidian")

usage() {
  cat <<'EOF'
Usage: update-open-pr-branches-from-main.sh [options]

Options:
  --repo OWNER/REPO       Repository to inspect (default: LAF-US/IDAHO-VAULT)
  --base BRANCH           Base branch to merge into PR heads (default: main)
  --apply                 Perform native GitHub branch updates. Default is dry-run.
  --include-drafts        Include draft pull requests. Default: skip drafts.
  --include-forks         Include fork-based pull requests. Default: skip forks.
  --exclude-pr NUMBER     Add a pull request number to the denylist (repeatable).
  --exclude-branch NAME   Add an exact source branch name to the denylist (repeatable).
  -h, --help              Show this help.

The script deduplicates PRs that share the same source repository and branch.
In --apply mode it sends expected_head_sha, so GitHub refuses the update if the
head moved after the script read it. A GitHub conflict or 422 response is logged
and leaves that branch unchanged.
EOF
}

while (($#)); do
  case "$1" in
    --repo) REPO="$2"; shift 2 ;;
    --base) BASE="$2"; shift 2 ;;
    --apply) APPLY=true; shift ;;
    --include-drafts) INCLUDE_DRAFTS=true; shift ;;
    --include-forks) INCLUDE_FORKS=true; shift ;;
    --exclude-pr) EXCLUDED_PRS+=("$2"); shift 2 ;;
    --exclude-branch) EXCLUDED_BRANCHES+=("$2"); shift 2 ;;
    -h|--help) usage; exit 0 ;;
    *) printf 'Unknown option: %s\n' "$1" >&2; usage >&2; exit 2 ;;
  esac
done

command -v gh >/dev/null || { echo 'gh is required.' >&2; exit 2; }
command -v jq >/dev/null || { echo 'jq is required.' >&2; exit 2; }
gh auth status >/dev/null || { echo 'gh is not authenticated.' >&2; exit 2; }

is_excluded() {
  local needle="$1"
  shift
  local item
  for item in "$@"; do
    [[ "$needle" == "$item" ]] && return 0
  done
  return 1
}

api_get() {
  gh api -H 'Accept: application/vnd.github+json' "$@"
}

printf 'Repository: %s\nBase branch: %s\nMode: %s\n\n' \
  "$REPO" "$BASE" "$([[ "$APPLY" == true ]] && echo APPLY || echo DRY-RUN)"
printf '%-7s %-48s %-25s %s\n' 'PR' 'SOURCE' 'BEHIND' 'RESULT'
printf '%-7s %-48s %-25s %s\n' '---' '------' '------' '------'

# The REST list response includes head SHA, branch, base, draft state, and
# source repository. The native endpoint merges the PR's BASE into its head,
# so this script enumerates all open PRs and explicitly skips anything whose
# base is not the requested branch. Slurping paginated arrays keeps it correct
# if the repository has more than 100 open PRs.
prs_json="$(api_get "repos/${REPO}/pulls?state=open&per_page=100" --paginate | jq -s 'add')"

seen_heads=()
updated=0
already_current=0
held=0
skipped=0
conflicted_or_rejected=0
failed=0

while IFS=$'\t' read -r number base_ref draft head_sha head_ref head_repo head_label; do
  [[ -z "$number" ]] && continue

  if [[ "$base_ref" != "$BASE" ]]; then
    printf '#%-6s %-48s %-25s %s\n' "$number" "$head_ref" '-' "SKIP: base is ${base_ref}"
    ((skipped += 1))
    continue
  fi

  if is_excluded "$number" "${EXCLUDED_PRS[@]}"; then
    printf '#%-6s %-48s %-25s %s\n' "$number" "$head_ref" '-' 'SKIP: denied PR'
    ((skipped += 1))
    continue
  fi
  if is_excluded "$head_ref" "${EXCLUDED_BRANCHES[@]}"; then
    printf '#%-6s %-48s %-25s %s\n' "$number" "$head_ref" '-' 'SKIP: denied branch'
    ((skipped += 1))
    continue
  fi
  if [[ "$draft" == true && "$INCLUDE_DRAFTS" != true ]]; then
    printf '#%-6s %-48s %-25s %s\n' "$number" "$head_ref" '-' 'SKIP: draft'
    ((skipped += 1))
    continue
  fi
  if [[ "$head_repo" != "$REPO" && "$INCLUDE_FORKS" != true ]]; then
    printf '#%-6s %-48s %-25s %s\n' "$number" "$head_ref" '-' 'SKIP: fork source'
    ((skipped += 1))
    continue
  fi

  head_key="${head_repo}:${head_ref}"
  if is_excluded "$head_key" "${seen_heads[@]}"; then
    printf '#%-6s %-48s %-25s %s\n' "$number" "$head_ref" '-' 'SKIP: shared source branch'
    ((skipped += 1))
    continue
  fi
  seen_heads+=("$head_key")

  compare_head="$head_ref"
  [[ "$head_repo" != "$REPO" ]] && compare_head="$head_label"
  comparison="$(api_get "repos/${REPO}/compare/${BASE}...${compare_head}" 2>&1)"
  if ! behind_by="$(jq -r '.behind_by // empty' <<<"$comparison" 2>/dev/null)"; then
    printf '#%-6s %-48s %-25s %s\n' "$number" "$head_ref" '-' 'ERROR: comparison JSON'
    ((failed += 1))
    continue
  fi
  if [[ -z "$behind_by" ]]; then
    printf '#%-6s %-48s %-25s %s\n' "$number" "$head_ref" '-' 'ERROR: comparison failed'
    ((failed += 1))
    continue
  fi
  if (( behind_by == 0 )); then
    printf '#%-6s %-48s %-25s %s\n' "$number" "$head_ref" '0' 'CURRENT'
    ((already_current += 1))
    continue
  fi

  if [[ "$APPLY" != true ]]; then
    printf '#%-6s %-48s %-25s %s\n' "$number" "$head_ref" "$behind_by" 'WOULD UPDATE'
    ((held += 1))
    continue
  fi

  # Native GitHub endpoint: GitHub merges the base head into the PR head. The
  # head SHA is an optimistic lock; if the source branch changes meanwhile the
  # endpoint returns 422 rather than touching a newer head unexpectedly.
  response_file="$(mktemp)"
  http_status="$(gh api --method PUT \
    -H 'Accept: application/vnd.github+json' \
    "repos/${REPO}/pulls/${number}/update-branch" \
    -f "expected_head_sha=${head_sha}" \
    --include >"$response_file" 2>&1; true)"

  if grep -qE '^HTTP/[0-9.]+ 202' "$response_file"; then
    printf '#%-6s %-48s %-25s %s\n' "$number" "$head_ref" "$behind_by" 'UPDATE ACCEPTED'
    ((updated += 1))
  elif grep -qE '^HTTP/[0-9.]+ 422' "$response_file"; then
    printf '#%-6s %-48s %-25s %s\n' "$number" "$head_ref" "$behind_by" 'HELD: conflict or changed head'
    ((conflicted_or_rejected += 1))
  else
    printf '#%-6s %-48s %-25s %s\n' "$number" "$head_ref" "$behind_by" 'ERROR: endpoint rejected request'
    sed 's/^/  /' "$response_file" >&2
    ((failed += 1))
  fi
  rm -f -- "$response_file"
done < <(
  jq -r '.[] | [.number, .base.ref, (.draft // false), .head.sha, .head.ref, (.head.repo.full_name // ""), .head.label] | @tsv' <<<"$prs_json"
)

printf '\nSummary: updated=%d current=%d would_update=%d held_or_conflicted=%d skipped=%d errors=%d\n' \
  "$updated" "$already_current" "$held" "$conflicted_or_rejected" "$skipped" "$failed"

# A dry-run is always successful unless API processing itself failed. Apply mode
# returns nonzero when an unexpected endpoint error occurred, but not for normal
# conflict/changed-head holds.
(( failed == 0 ))
