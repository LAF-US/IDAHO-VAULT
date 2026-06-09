#!/usr/bin/env python3
"""Verify that arbiter approvals are present for a PR."""

import argparse
import json
import subprocess
import sys

ARBITER_LABEL_PREFIX = "arbiter/"


def _run(cmd, check=True):
    result = subprocess.run(cmd, capture_output=True, text=True)
    if check and result.returncode != 0:
        raise RuntimeError(f"Command failed ({result.returncode}): {' '.join(cmd)}\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}")
    return result


def _graphql(query, **variables):
    cmd = ["gh", "api", "graphql", "-f", f"query={query}"]
    for key, value in variables.items():
        if isinstance(value, int):
            cmd.extend(["-F", f"{key}={value}"])
        else:
            cmd.extend(["-f", f"{key}={value}"])
    result = _run(cmd)
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


def _get_arbiter_labels(pr_number):
    result = _run(["gh", "pr", "view", str(pr_number), "--json", "labels"], check=False)
    try:
        pr_data = json.loads(result.stdout or "{}")
        labels = [label.get("name", "") for label in pr_data.get("labels", [])]
        arbiters = set()
        for label in labels:
            if label.startswith(ARBITER_LABEL_PREFIX):
                arbiter_name = label[len(ARBITER_LABEL_PREFIX):]
                arbiters.add(arbiter_name)
        return arbiters
    except (json.JSONDecodeError, KeyError):
        return set()


def _get_approved_arbiters(owner, repo, pr_number, arbiters):
    reviews = _get_pr_reviews(owner, repo, pr_number)
    approved_arbiters = set()
    for review in reviews:
        state = review.get("state")
        author = (review.get("author") or {}).get("login")
        if state == "APPROVED" and author and author in arbiters:
            approved_arbiters.add(author)
    return approved_arbiters


def _check_requires_approval(owner, repo, pr_number):
    # For main branch, always require approval
    result = _run(["gh", "pr", "view", str(pr_number), "--json", "baseRefName"], check=False)
    try:
        pr_data = json.loads(result.stdout or "{}")
        base_ref = pr_data.get("baseRefName", "")
        return base_ref == "main"
    except (json.JSONDecodeError, KeyError):
        return True


def main():
    parser = argparse.ArgumentParser(description="Verify Arbiter Approvals")
    parser.add_argument("--pr-number", type=int, required=True, help="Pull request number")
    parser.add_argument("--repo", type=str, required=True, help="Repository in owner/repo format")
    parser.add_argument("--required-count", type=int, default=1, help="Required number of arbiter approvals")
    args = parser.parse_args()
    
    owner, repo_name = args.repo.split("/")
    print(f"Verifying arbiter approvals for {owner}/{repo_name} PR #{args.pr_number}")
    
    requires_approval = _check_requires_approval(owner, repo_name, args.pr_number)
    if not requires_approval:
        print("PR does not require approval")
        sys.exit(0)
    
    arbiters = _get_arbiter_labels(args.pr_number)
    print(f"Designated arbiters: {arbiters}")
    
    if not arbiters:
        print("No arbiters designated for this PR")
        sys.exit(1)
    
    approved_arbiters = _get_approved_arbiters(owner, repo_name, args.pr_number, arbiters)
    print(f"Approved arbiters: {approved_arbiters}")
    
    if len(approved_arbiters) >= args.required_count:
        print(f"{len(approved_arbiters)} of {args.required_count} required arbiter approvals present")
        sys.exit(0)
    else:
        print(f"Only {len(approved_arbiters)} of {args.required_count} required arbiter approvals present")
        print(f"Missing approvals from: {arbiters - approved_arbiters}")
        sys.exit(1)


if __name__ == "__main__":
    main()