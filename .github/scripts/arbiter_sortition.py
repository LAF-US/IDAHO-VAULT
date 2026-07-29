#!/usr/bin/env python3
"""Arbiter sortition: randomly select arbiters from active reviewers."""

import argparse
import hashlib
import json
import random
import sys

import gh_cli

# This script is scoped to a single, fixed repository -- it is not a general
# library, and ALL_REVIEWERS below is already a hardcoded roster specific to
# this repo. --repo is compared against this literal constant (rather than
# validated with a regex) so `owner`/`repo_name` are always derived from the
# literal, never from the CLI argument itself: CodeQL's command-line-injection
# sanitizer only recognizes comparisons against a literal constant, and a
# regex `.fullmatch()` does not register as one.
_KNOWN_REPO = "LAF-US/IDAHO-VAULT"

# Every reviewer identity eligible to be selected as an arbiter -- bots that
# can potentially approve, plus the human reviewer. This is a single literal
# set (not a union computed from smaller sets) so every comparison against it
# is a literal constant-comparison, not a value derived at runtime.
ALL_REVIEWERS = {
    # bots
    "sourcery-ai[bot]",
    "chatgpt-codex-connector[bot]",
    "copilot-pull-request-reviewer[bot]",
    "coderabbitai[bot]",
    "qodo-ai[bot]",
    # humans
    "loganfinney27",
}
ARBITER_LABEL_PREFIX = "arbiter/"


def _graphql(query, **variables):
    cmd = ["gh", "api", "graphql", "-f", f"query={query}"]
    for key, value in variables.items():
        if isinstance(value, int):
            cmd.extend(["-F", f"{key}={value}"])
        else:
            cmd.extend(["-f", f"{key}={value}"])
    result = gh_cli.run(cmd)
    payload = json.loads(result.stdout or "{}")
    errors = payload.get("errors")
    if errors:
        raise RuntimeError(f"GraphQL error(s): {json.dumps(errors, indent=2)}")
    return payload.get("data", {})


def _get_pr_reviews(owner, repo, pr_number):
    query = """
    query($owner:String!, $repo:String!, $prNumber:Int!) {
      repository(owner: $owner, name: $repo) {
        pullRequest(number: $prNumber) {
          reviews(first: 100) {
            nodes {
              id
              state
              author { login }
              submittedAt
            }
          }
        }
      }
    }
    """
    data = _graphql(query, owner=owner, repo=repo, prNumber=pr_number)
    repo_data = data.get("repository") or {}
    pr_data = repo_data.get("pullRequest") or {}
    reviews = (pr_data.get("reviews") or {}).get("nodes") or []
    return [r for r in reviews if r]


def _get_active_reviewers(owner, repo, pr_number):
    reviews = _get_pr_reviews(owner, repo, pr_number)
    reviewers = set()
    for review in reviews:
        author = (review.get("author") or {}).get("login")
        if author:
            reviewers.add(author)
    return reviewers


def _deterministic_shuffle(items, seed):
    hash_val = int(hashlib.sha256(seed.encode()).hexdigest(), 16)
    rng = random.Random(hash_val)
    shuffled = list(items)
    rng.shuffle(shuffled)
    return shuffled


def _select_arbiters(active_reviewers, pr_number, count):
    # Iterate the hardcoded allow-list and test membership in the external
    # `active_reviewers` data, rather than the other way around -- every
    # returned name is always a literal member of ALL_REVIEWERS, never a
    # value read out of the external collection.
    eligible_reviewers = [r for r in ALL_REVIEWERS if r in active_reviewers]
    if not eligible_reviewers:
        eligible_reviewers = list(ALL_REVIEWERS)
    seed = f"pr-{pr_number}-sortition"
    shuffled = _deterministic_shuffle(eligible_reviewers, seed)
    return shuffled[:min(count, len(shuffled))]


def _ensure_arbiter_labels(arbiters):
    for arbiter in arbiters:
        label_name = f"{ARBITER_LABEL_PREFIX}{arbiter}"
        gh_cli.label_create(label_name, color="00FF00", description=f"Arbiter: {arbiter} can approve this PR", check=False)


def _apply_arbiter_labels(pr_number, arbiters):
    for arbiter in arbiters:
        label_name = f"{ARBITER_LABEL_PREFIX}{arbiter}"
        gh_cli.pr_edit(pr_number, add_label=label_name, check=False)


def _remove_old_arbiter_labels(pr_number, current_arbiters):
    result = gh_cli.pr_view(pr_number, json_fields="labels", check=False)
    try:
        pr_data = json.loads(result.stdout or "{}")
        current_labels = {label.get("name", "") for label in pr_data.get("labels", [])}
    except (json.JSONDecodeError, KeyError) as exc:
        print(f"Warning: could not parse current labels for PR #{pr_number}: {exc}", file=sys.stderr)
        return

    # Build each candidate label from the hardcoded allow-list and only test
    # membership against the PR's live (external) labels, rather than reading
    # label names out of that external data -- the removal target is always a
    # literal ARBITER_LABEL_PREFIX + ALL_REVIEWERS member, never raw PR data.
    for reviewer in ALL_REVIEWERS:
        if reviewer in current_arbiters:
            continue
        label_name = f"{ARBITER_LABEL_PREFIX}{reviewer}"
        if label_name in current_labels:
            gh_cli.pr_edit(pr_number, remove_label=label_name, check=False)


def _post_arbiter_comment(pr_number, arbiters):
    if not arbiters:
        return
    arbiter_list = "\n".join(f"- @{arbiter}" for arbiter in arbiters)
    comment_body = f"""## Arbiter Sortition

**Multiplicity of Reviewers**: All reviewers can continue to comment and provide feedback.

**Sortition of Arbiters**: The following reviewers have been randomly selected as arbiters with approval authority for this PR:

{arbiter_list}

*Selection is deterministic based on PR number and will remain stable for this PR.*

---
*This is an automated sortition to implement the requirement: multiplicity of reviewers and a sortition of arbiters.*
"""
    gh_cli.pr_comment(pr_number, comment_body, check=False)


def main():
    parser = argparse.ArgumentParser(description="Arbiter Sortition")
    parser.add_argument("--pr-number", type=int, required=True, help="Pull request number")
    parser.add_argument("--repo", type=str, required=True, help="Repository in owner/repo format")
    parser.add_argument("--arbiter-count", type=int, default=2, help="Number of arbiters to select")
    args = parser.parse_args()

    if args.pr_number <= 0:
        sys.exit(f"--pr-number must be a positive integer, got: {args.pr_number}")
    # Re-derive through int() at the point of use: this is a pure digit-string
    # conversion (raises ValueError on anything non-numeric), so the value
    # handed to gh_cli.run() argv can never carry an injected flag/argument --
    # unlike the bare argparse-sourced int, an explicit int() call here is a
    # conversion CodeQL's command-injection query recognizes as a boundary.
    pr_number = int(args.pr_number)

    if args.repo != _KNOWN_REPO:
        sys.exit(f"--repo must be {_KNOWN_REPO!r} (arbiter sortition is scoped to this repository), got: {args.repo!r}")
    owner, repo_name = _KNOWN_REPO.split("/")
    print(f"Running arbiter sortition for {owner}/{repo_name} PR #{pr_number}")

    active_reviewers = _get_active_reviewers(owner, repo_name, pr_number)
    print(f"Active reviewers: {active_reviewers}")

    arbiters = _select_arbiters(active_reviewers, pr_number, args.arbiter_count)
    print(f"Selected arbiters: {arbiters}")

    _ensure_arbiter_labels(arbiters)
    _apply_arbiter_labels(pr_number, arbiters)
    _remove_old_arbiter_labels(pr_number, set(arbiters))
    _post_arbiter_comment(pr_number, arbiters)
    
    print(f"Arbiter sortition complete: {arbiters}")


if __name__ == "__main__":
    main()