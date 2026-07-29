"""Shared GitHub I/O plumbing for the review/merge engine.

GraphQL execution, the pull-request fetch, and the authenticated-actor lookup —
the I/O layer that both the review-state projector and the thread-witness looker
need (#600 §5 shared lib: "_fetch_pr, thread walking … imported by both"). Built
on ``gh_cli``'s typed operations; it depends on nothing in the engine, so both
engines import it and neither owns it. Moved verbatim from
``review_feedback_loop.py`` — no behavior change.
"""

from __future__ import annotations

import json

import gh_cli


def _graphql(query: str, **variables: object) -> dict:
    """Execute a GraphQL query via ``gh api graphql`` and return the ``data`` payload.

    Integer variables are passed with ``-F`` (typed); all others with ``-f`` (string).
    Raises ``RuntimeError`` if the response carries GraphQL ``errors``.
    """
    result = gh_cli.graphql(query, **variables)
    payload = json.loads(result.stdout or "{}")
    errors = payload.get("errors")
    if errors:
        max_len = 200

        truncated_query = query
        if len(truncated_query) > max_len:
            truncated_query = truncated_query[: max_len - 3] + "..."

        try:
            variables_repr = json.dumps(variables, default=str)
        except TypeError:
            variables_repr = repr(variables)

        if len(variables_repr) > max_len:
            variables_repr = variables_repr[: max_len - 3] + "..."

        raise RuntimeError(
            "GraphQL error(s): "
            f"{json.dumps(errors, indent=2)}\n"
            f"query: {truncated_query}\n"
            f"variables: {variables_repr}"
        )
    return payload.get("data", {})


def _fetch_pr(owner: str, name: str, number: int) -> dict:
    """Fetch a pull request's review state from the GitHub GraphQL API.

    Returns the ``pullRequest`` node including labels, review threads, and
    auto-merge status. Raises ``RuntimeError`` if the PR is not found.
    """
    query = """
    query($owner:String!, $name:String!, $number:Int!) {
      repository(owner: $owner, name: $name) {
        pullRequest(number: $number) {
          number
          url
          body
          state
          createdAt
          updatedAt
          isDraft
          reviewDecision
          autoMergeRequest {
            enabledAt
          }
          labels(first: 50) {
            nodes { name }
          }
          reviewThreads(first: 100) {
            pageInfo { hasNextPage }
            nodes {
              id
              isResolved
              isOutdated
              resolvedBy { login }
              comments(first: 100) {
                pageInfo { hasNextPage }
                nodes {
                  author { login __typename }
                  body
                  url
                }
              }
            }
          }
        }
      }
    }
    """
    data = _graphql(query, owner=owner, name=name, number=number)
    repo = data.get("repository") or {}
    pr = repo.get("pullRequest")
    if not pr:
        raise RuntimeError(f"Pull request #{number} was not found in {owner}/{name}.")
    return pr


def _viewer_login() -> str:
    """The login of the authenticated actor the GraphQL calls post as.

    The attestation is *self*-attested: the detector requires the marker's `by=`
    to equal the comment's own author. Since `_add_thread_reply` posts as this
    actor, a `looker` that differs from it would yield an undetectable attestation,
    so the resolve path verifies them against each other before writing.
    """
    viewer = _graphql("query { viewer { login } }").get("viewer") or {}
    login = (viewer.get("login") or "").strip()
    if not login:
        raise RuntimeError("Could not determine the authenticated GitHub actor.")
    return login
