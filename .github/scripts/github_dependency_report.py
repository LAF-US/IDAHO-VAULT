#!/usr/bin/env python3
"""Build a read-only GitHub issue and pull request dependency census."""

from __future__ import annotations

import argparse
import html
import json
import os
import re
import sys
import time
from collections import defaultdict, deque
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Protocol
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

API_ROOT = "https://api.github.com"
FAILED_CHECK_STATES = {"ACTION_REQUIRED", "CANCELLED", "FAILURE", "STALE", "TIMED_OUT"}
EXTERNAL_MARKDOWN_LINK = re.compile(
    r"\[[^\]]*\]\(https://github\.com/([^/\s]+)/([^/\s)#]+)[^)]*\)",
    re.IGNORECASE,
)
EXTERNAL_HTML_LINK = re.compile(
    r"<a\b[^>]*href=[\"']https://(?:redirect\.)?github\.com/"
    r"([^/\"']+)/([^/\"'#?]+)[^\"']*[\"'][^>]*>.*?</a>",
    re.IGNORECASE | re.DOTALL,
)
FENCED_CODE = re.compile(r"```.*?```", re.DOTALL)
NON_REPOSITORY_NUMBER = re.compile(r"\b(?:xkcd)\s+#\d{1,7}\b", re.IGNORECASE)
REFERENCE_PATTERN = re.compile(r"(?<![\w])#(\d{1,7})(?!\d)")
FULL_REFERENCE_PATTERN = re.compile(
    r"(?<![\w.-])([A-Za-z0-9_.-]+)/([A-Za-z0-9_.-]+)#(\d{1,7})(?!\d)"
)
URL_REFERENCE_PATTERN = re.compile(
    r"https://github\.com/([A-Za-z0-9_.-]+)/([A-Za-z0-9_.-]+)/(?:issues|pull)/(\d+)"
)
LIFECYCLE_PATTERNS = (
    (
        "superseded_by",
        re.compile(r"\bsuperseded\s+by\s+(?:PR|issue)?\s*#(\d+)", re.IGNORECASE),
    ),
    (
        "replaces",
        re.compile(r"\b(?:this\s+PR\s+)?replaces\s+(?:PR|issue)?\s*#(\d+)", re.IGNORECASE),
    ),
    (
        "replacement_for",
        re.compile(r"\breplacement\s+for\s+(?:PR|issue)?\s*#(\d+)", re.IGNORECASE),
    ),
    (
        "implemented_by",
        re.compile(
            r"\b(?:implemented|implementation|completed|fixed)\s+"
            r"(?:is\s+)?(?:filed\s+)?(?:in|by|through)\s+(?:draft\s+)?PR\s*#(\d+)",
            re.IGNORECASE,
        ),
    ),
    (
        "implements",
        re.compile(
            r"\b(?:implements|resolves|completes|fixes)\s+(?:issue\s+)?#(\d+)",
            re.IGNORECASE,
        ),
    ),
)
PAYLOAD_TERMS = re.compile(
    r"\b(?:implementation|payload|carrier|record|replacement|supersed|salvage)\b",
    re.IGNORECASE,
)


@dataclass
class Node:
    number: int
    item_type: str
    state: str
    title: str
    url: str
    labels: list[str] = field(default_factory=list)
    branch: str | None = None
    files: list[str] = field(default_factory=list)
    checks: list[dict[str, str]] = field(default_factory=list)
    updated_at: str | None = None
    merged_at: str | None = None
    open_inventory: bool = False


@dataclass(frozen=True)
class Evidence:
    location: str
    snippet: str


@dataclass
class Edge:
    source: int
    target: int
    relation: str
    confidence: str
    detail: str
    evidence: list[Evidence] = field(default_factory=list)


@dataclass(frozen=True)
class TextSource:
    location: str
    text: str


@dataclass
class Snapshot:
    node: Node
    texts: list[TextSource] = field(default_factory=list)
    native: list[tuple[int, str]] = field(default_factory=list)
    timeline_sources: list[tuple[int, str]] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


class CensusClient(Protocol):
    def list_open_nodes(self) -> list[Node]: ...

    def fetch_snapshot(self, number: int) -> Snapshot: ...

    def fetch_context_node(self, number: int) -> Node | None: ...


class GitHubClient:
    """Small bounded GitHub API client with no repository mutations."""

    def __init__(
        self,
        repo: str,
        *,
        token: str,
        timeout: int = 30,
        max_pages: int = 10,
        retries: int = 2,
    ) -> None:
        if "/" not in repo:
            raise ValueError("repository must be in owner/name form")
        self.repo = repo
        self.owner, self.name = repo.split("/", 1)
        self.token = token
        self.timeout = timeout
        self.max_pages = max_pages
        self.retries = retries

    def _request(
        self,
        path: str,
        *,
        method: str = "GET",
        payload: dict[str, object] | None = None,
        accept: str = "application/vnd.github+json",
    ) -> object:
        data = json.dumps(payload).encode("utf-8") if payload is not None else None
        headers = {
            "Accept": accept,
            "User-Agent": "idaho-vault-github-dependency-census",
            "X-GitHub-Api-Version": "2022-11-28",
        }
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        request = Request(
            path if path.startswith("http") else f"{API_ROOT}{path}",
            data=data,
            headers=headers,
            method=method,
        )
        for attempt in range(self.retries + 1):
            try:
                with urlopen(request, timeout=self.timeout) as response:  # noqa: S310
                    return json.load(response)
            except HTTPError as exc:
                if exc.code == 404:
                    raise FileNotFoundError(path) from exc
                if exc.code not in {429, 500, 502, 503, 504} or attempt >= self.retries:
                    raise RuntimeError(f"GitHub API {method} {path} failed: HTTP {exc.code}") from exc
            except URLError as exc:
                if attempt >= self.retries:
                    raise RuntimeError(f"GitHub API {method} {path} failed") from exc
            time.sleep(2**attempt)
        raise RuntimeError(f"GitHub API {method} {path} failed")

    def _pages(self, path: str, *, accept: str = "application/vnd.github+json") -> list[dict]:
        records: list[dict] = []
        separator = "&" if "?" in path else "?"
        for page in range(1, self.max_pages + 1):
            payload = self._request(
                f"{path}{separator}per_page=100&page={page}",
                accept=accept,
            )
            if not isinstance(payload, list):
                raise RuntimeError(f"Expected list response from {path}")
            records.extend(item for item in payload if isinstance(item, dict))
            if len(payload) < 100:
                return records
        raise RuntimeError(f"Pagination limit exceeded for {path}")

    def _keyed_pages(self, path: str, key: str) -> list[dict]:
        records: list[dict] = []
        separator = "&" if "?" in path else "?"
        for page in range(1, self.max_pages + 1):
            payload = self._request(f"{path}{separator}per_page=100&page={page}")
            if not isinstance(payload, dict) or not isinstance(payload.get(key), list):
                raise RuntimeError(f"Expected {key!r} list response from {path}")
            page_records = payload[key]
            records.extend(item for item in page_records if isinstance(item, dict))
            if len(page_records) < 100:
                return records
        raise RuntimeError(f"Pagination limit exceeded for {path}")

    @staticmethod
    def _node_from_issue(issue: dict, *, open_inventory: bool) -> Node:
        is_pr = isinstance(issue.get("pull_request"), dict)
        return Node(
            number=int(issue["number"]),
            item_type="pr" if is_pr else "issue",
            state=str(issue.get("state") or "unknown").lower(),
            title=str(issue.get("title") or ""),
            url=str(issue.get("html_url") or ""),
            labels=sorted(
                str(label.get("name"))
                for label in issue.get("labels", [])
                if isinstance(label, dict) and label.get("name")
            ),
            updated_at=issue.get("updated_at"),
            open_inventory=open_inventory,
        )

    def list_open_nodes(self) -> list[Node]:
        issues = self._pages(f"/repos/{self.repo}/issues?state=open")
        return [self._node_from_issue(issue, open_inventory=True) for issue in issues]

    def _native_relations(self, number: int) -> list[tuple[int, str]]:
        query = """
        query($owner:String!, $name:String!, $number:Int!) {
          repository(owner:$owner, name:$name) {
            issueOrPullRequest(number:$number) {
              ... on Issue {
                blockedBy(first:100) { nodes { number } }
                blocking(first:100) { nodes { number } }
                trackedInIssues(first:100) { nodes { number } }
                trackedIssues(first:100) { nodes { number } }
              }
              ... on PullRequest {
                closingIssuesReferences(first:100) { nodes { number } }
              }
            }
          }
        }
        """
        response = self._request(
            "/graphql",
            method="POST",
            payload={
                "query": query,
                "variables": {"owner": self.owner, "name": self.name, "number": number},
            },
        )
        if not isinstance(response, dict) or response.get("errors"):
            raise RuntimeError(f"GraphQL dependency query failed for #{number}")
        item = (
            response.get("data", {})
            .get("repository", {})
            .get("issueOrPullRequest")
        )
        if not isinstance(item, dict):
            return []
        relations: list[tuple[int, str]] = []
        fields = {
            "blockedBy": "blocked_by",
            "blocking": "blocks",
            "trackedInIssues": "tracked_in",
            "trackedIssues": "tracks",
            "closingIssuesReferences": "closes",
        }
        for field_name, relation in fields.items():
            connection = item.get(field_name)
            if not isinstance(connection, dict):
                continue
            for target in connection.get("nodes", []):
                if isinstance(target, dict) and target.get("number"):
                    relations.append((int(target["number"]), relation))
        return relations

    def _pull_details(self, node: Node) -> list[str]:
        warnings: list[str] = []
        pull = self._request(f"/repos/{self.repo}/pulls/{node.number}")
        if not isinstance(pull, dict):
            raise RuntimeError(f"Unexpected PR response for #{node.number}")
        node.branch = str(pull.get("head", {}).get("ref") or "") or None
        node.merged_at = pull.get("merged_at")
        if node.merged_at:
            node.state = "merged"
        node.files = sorted(
            str(item["filename"])
            for item in self._pages(f"/repos/{self.repo}/pulls/{node.number}/files")
            if item.get("filename")
        )
        sha = pull.get("head", {}).get("sha")
        if not sha:
            warnings.append(f"PR #{node.number}: head SHA unavailable; checks omitted.")
            return warnings
        check_runs = self._keyed_pages(
            f"/repos/{self.repo}/commits/{quote(str(sha), safe='')}/check-runs",
            "check_runs",
        )
        node.checks.extend(
            {
                "name": str(check.get("name") or ""),
                "state": str(check.get("conclusion") or check.get("status") or "").upper(),
                "url": str(check.get("html_url") or check.get("details_url") or ""),
            }
            for check in check_runs
            if isinstance(check, dict) and check.get("name")
        )
        statuses = self._pages(
            f"/repos/{self.repo}/commits/{quote(str(sha), safe='')}/statuses"
        )
        node.checks.extend(
            {
                "name": str(status.get("context") or ""),
                "state": str(status.get("state") or "").upper(),
                "url": str(status.get("target_url") or ""),
            }
            for status in statuses
            if isinstance(status, dict) and status.get("context")
        )
        node.checks.sort(key=lambda check: (check["name"].lower(), check["state"]))
        return warnings

    def fetch_snapshot(self, number: int) -> Snapshot:
        issue = self._request(f"/repos/{self.repo}/issues/{number}")
        if not isinstance(issue, dict):
            raise RuntimeError(f"Unexpected issue response for #{number}")
        node = self._node_from_issue(issue, open_inventory=True)
        warnings: list[str] = []
        if node.item_type == "pr":
            warnings.extend(self._pull_details(node))

        texts = [
            TextSource(
                location=f"{node.url}#body",
                text=str(issue.get("body") or ""),
            )
        ]
        for comment in self._pages(f"/repos/{self.repo}/issues/{number}/comments"):
            texts.append(
                TextSource(
                    location=str(comment.get("html_url") or f"{node.url}#comment"),
                    text=str(comment.get("body") or ""),
                )
            )
        if node.item_type == "pr":
            for comment in self._pages(f"/repos/{self.repo}/pulls/{number}/comments"):
                texts.append(
                    TextSource(
                        location=str(comment.get("html_url") or f"{node.url}#review-comment"),
                        text=str(comment.get("body") or ""),
                    )
                )
            for review in self._pages(f"/repos/{self.repo}/pulls/{number}/reviews"):
                texts.append(
                    TextSource(
                        location=str(review.get("html_url") or f"{node.url}#review"),
                        text=str(review.get("body") or ""),
                    )
                )

        timeline_sources: list[tuple[int, str]] = []
        try:
            timeline = self._pages(
                f"/repos/{self.repo}/issues/{number}/timeline",
                accept="application/vnd.github+json",
            )
            for event in timeline:
                if event.get("event") != "cross-referenced":
                    continue
                source = event.get("source", {}).get("issue", {})
                if source.get("number"):
                    timeline_sources.append(
                        (
                            int(source["number"]),
                            str(source.get("html_url") or source.get("pull_request", {}).get("html_url") or ""),
                        )
                    )
        except RuntimeError as exc:
            warnings.append(f"#{number}: timeline unavailable ({exc}).")

        try:
            native = self._native_relations(number)
        except RuntimeError as exc:
            native = []
            warnings.append(f"#{number}: native dependencies unavailable ({exc}).")
        return Snapshot(
            node=node,
            texts=texts,
            native=native,
            timeline_sources=timeline_sources,
            warnings=warnings,
        )

    def fetch_context_node(self, number: int) -> Node | None:
        try:
            issue = self._request(f"/repos/{self.repo}/issues/{number}")
        except FileNotFoundError:
            return None
        if not isinstance(issue, dict):
            return None
        node = self._node_from_issue(issue, open_inventory=False)
        if node.item_type == "pr":
            try:
                pull = self._request(f"/repos/{self.repo}/pulls/{number}")
            except (FileNotFoundError, RuntimeError):
                pull = None
            if isinstance(pull, dict):
                node.branch = str(pull.get("head", {}).get("ref") or "") or None
                node.merged_at = pull.get("merged_at")
                if node.merged_at:
                    node.state = "merged"
        return node


def _strip_external_links(text: str, repo: str) -> str:
    owner, name = (part.lower() for part in repo.split("/", 1))

    def markdown_replacement(match: re.Match[str]) -> str:
        return match.group(0) if (match.group(1).lower(), match.group(2).lower()) == (owner, name) else ""

    def html_replacement(match: re.Match[str]) -> str:
        return match.group(0) if (match.group(1).lower(), match.group(2).lower()) == (owner, name) else ""

    text = EXTERNAL_MARKDOWN_LINK.sub(markdown_replacement, text)
    return EXTERNAL_HTML_LINK.sub(html_replacement, text)


def extract_references(text: str, repo: str) -> set[int]:
    """Extract same-repository references while excluding external GitHub links."""
    if not text:
        return set()
    owner, name = (part.lower() for part in repo.split("/", 1))
    references: set[int] = set()
    for match in URL_REFERENCE_PATTERN.finditer(text):
        if (match.group(1).lower(), match.group(2).lower()) == (owner, name):
            references.add(int(match.group(3)))
    for match in FULL_REFERENCE_PATTERN.finditer(text):
        if (match.group(1).lower(), match.group(2).lower()) == (owner, name):
            references.add(int(match.group(3)))
    scrubbed = FENCED_CODE.sub("", _strip_external_links(text, repo))
    scrubbed = NON_REPOSITORY_NUMBER.sub("", scrubbed)
    references.update(int(match.group(1)) for match in REFERENCE_PATTERN.finditer(scrubbed))
    return {number for number in references if number > 0}


def _snippet(text: str, start: int, width: int = 220) -> str:
    flattened = re.sub(r"\s+", " ", html.unescape(text)).strip()
    if not flattened:
        return ""
    start = max(0, min(start, len(flattened)) - 80)
    return flattened[start : start + width]


def text_edges(source: int, text_source: TextSource, repo: str) -> list[Edge]:
    edges: list[Edge] = []
    text = text_source.text or ""
    lifecycle_targets: set[int] = set()
    for detail, pattern in LIFECYCLE_PATTERNS:
        for match in pattern.finditer(text):
            target = int(match.group(1))
            lifecycle_targets.add(target)
            edges.append(
                Edge(
                    source=source,
                    target=target,
                    relation="lifecycle",
                    confidence="high",
                    detail=detail,
                    evidence=[Evidence(text_source.location, _snippet(text, match.start()))],
                )
            )
    for target in sorted(extract_references(text, repo) - lifecycle_targets):
        marker = re.search(rf"(?<!\d)#{target}(?!\d)", text)
        edges.append(
            Edge(
                source=source,
                target=target,
                relation="declared",
                confidence="medium",
                detail="references",
                evidence=[
                    Evidence(
                        text_source.location,
                        _snippet(text, marker.start() if marker else 0),
                    )
                ],
            )
        )
    return edges


def _edge_key(edge: Edge) -> tuple[int, int, str, str]:
    return edge.source, edge.target, edge.relation, edge.detail


def deduplicate_edges(edges: list[Edge]) -> list[Edge]:
    combined: dict[tuple[int, int, str, str], Edge] = {}
    for edge in edges:
        if edge.source == edge.target:
            continue
        key = _edge_key(edge)
        existing = combined.get(key)
        if existing is None:
            combined[key] = edge
            continue
        known = {(item.location, item.snippet) for item in existing.evidence}
        existing.evidence.extend(
            item for item in edge.evidence if (item.location, item.snippet) not in known
        )
    return sorted(
        combined.values(),
        key=lambda edge: (edge.source, edge.target, edge.relation, edge.detail),
    )


def add_structural_and_gate_edges(nodes: dict[int, Node], edges: list[Edge]) -> None:
    open_prs = [
        node
        for node in nodes.values()
        if node.open_inventory and node.item_type == "pr" and node.state == "open"
    ]
    by_file: dict[str, list[int]] = defaultdict(list)
    by_failed_check: dict[str, list[int]] = defaultdict(list)
    for node in open_prs:
        for path in node.files:
            by_file[path].append(node.number)
        for check in node.checks:
            if check.get("state", "").upper() in FAILED_CHECK_STATES:
                by_failed_check[check.get("name", "")].append(node.number)

    for path, numbers in sorted(by_file.items()):
        unique = sorted(set(numbers))
        for index, source in enumerate(unique):
            for target in unique[index + 1 :]:
                evidence = [Evidence(path, f"Both open PRs modify `{path}`.")]
                edges.append(Edge(source, target, "structural", "medium", "shared_file", evidence))

    for check_name, numbers in sorted(by_failed_check.items()):
        unique = sorted(set(numbers))
        if not check_name:
            continue
        for index, source in enumerate(unique):
            for target in unique[index + 1 :]:
                evidence = [Evidence(check_name, f"Both open PRs fail `{check_name}`.")]
                edges.append(Edge(source, target, "gate", "medium", "shared_failed_check", evidence))


def connected_components(nodes: dict[int, Node], edges: list[Edge]) -> list[list[int]]:
    adjacency: dict[int, set[int]] = {number: set() for number in nodes}
    for edge in edges:
        if edge.source in nodes and edge.target in nodes:
            adjacency[edge.source].add(edge.target)
            adjacency[edge.target].add(edge.source)
    components: list[list[int]] = []
    remaining = set(nodes)
    while remaining:
        root = min(remaining)
        queue = deque([root])
        component: list[int] = []
        remaining.remove(root)
        while queue:
            number = queue.popleft()
            component.append(number)
            for neighbor in sorted(adjacency[number]):
                if neighbor in remaining:
                    remaining.remove(neighbor)
                    queue.append(neighbor)
        components.append(sorted(component))
    return sorted(components, key=lambda component: (-len(component), component[0]))


def prerequisite_chains(processing: list[dict[str, object]]) -> list[list[int]]:
    adjacency: dict[int, set[int]] = defaultdict(set)
    indegree: dict[int, int] = defaultdict(int)
    for item in processing:
        before = int(item["before"])
        after = int(item["after"])
        if after in adjacency[before]:
            continue
        adjacency[before].add(after)
        indegree[after] += 1
        indegree.setdefault(before, 0)

    chains: set[tuple[int, ...]] = set()

    def walk(path: tuple[int, ...], current: int) -> None:
        next_nodes = sorted(adjacency.get(current, set()) - set(path))
        if not next_nodes:
            if len(path) > 1:
                chains.add(path)
            return
        for next_node in next_nodes:
            walk((*path, next_node), next_node)

    roots = sorted(number for number in indegree if indegree[number] == 0)
    for root in roots:
        walk((root,), root)
    return [list(chain) for chain in sorted(chains)]


def _edge_names_payload(edge: Edge) -> bool:
    if edge.relation == "lifecycle":
        return True
    target_marker = f"#{edge.target}"
    for item in edge.evidence:
        position = item.snippet.find(target_marker)
        if position < 0:
            continue
        sentence_start = item.snippet.rfind(".", 0, position) + 1
        sentence_end = item.snippet.find(".", position)
        if sentence_end < 0:
            sentence_end = len(item.snippet)
        sentence = item.snippet[sentence_start:sentence_end]
        if PAYLOAD_TERMS.search(sentence):
            return True
    return False


def _missing_node(number: int, repo: str) -> Node:
    return Node(
        number=number,
        item_type="unknown",
        state="missing",
        title="Unavailable or outside accessible repository history",
        url=f"https://github.com/{repo}/issues/{number}",
    )


def collect_census(client: CensusClient, repo: str) -> dict[str, object]:
    open_nodes = client.list_open_nodes()
    nodes = {node.number: node for node in open_nodes}
    edges: list[Edge] = []
    warnings: list[str] = []

    for index, basic in enumerate(open_nodes, start=1):
        print(f"[{index}/{len(open_nodes)}] inspecting #{basic.number}", file=sys.stderr)
        try:
            snapshot = client.fetch_snapshot(basic.number)
        except Exception as exc:  # workflow should return a partial, explicit report
            warnings.append(f"#{basic.number}: detail collection failed ({exc}).")
            continue
        nodes[basic.number] = snapshot.node
        warnings.extend(snapshot.warnings)
        for target, detail in snapshot.native:
            edges.append(
                Edge(
                    source=basic.number,
                    target=target,
                    relation="native",
                    confidence="high",
                    detail=detail,
                    evidence=[Evidence(snapshot.node.url, f"GitHub native relation: {detail}.")],
                )
            )
        for source_number, source_url in snapshot.timeline_sources:
            edges.append(
                Edge(
                    source=source_number,
                    target=basic.number,
                    relation="context",
                    confidence="low",
                    detail="cross_referenced",
                    evidence=[
                        Evidence(
                            source_url or snapshot.node.url,
                            f"GitHub timeline cross-reference to #{basic.number}.",
                        )
                    ],
                )
            )
        for source_text in snapshot.texts:
            edges.extend(text_edges(basic.number, source_text, repo))

    edges = deduplicate_edges(edges)
    context_numbers = sorted(
        {
            endpoint
            for edge in edges
            for endpoint in (edge.source, edge.target)
            if endpoint not in nodes
        }
    )
    for number in context_numbers:
        try:
            context_node = client.fetch_context_node(number)
        except Exception as exc:
            warnings.append(f"#{number}: context lookup failed ({exc}).")
            context_node = None
        nodes[number] = context_node or _missing_node(number, repo)

    add_structural_and_gate_edges(nodes, edges)
    edges = deduplicate_edges(edges)
    components = connected_components(nodes, edges)
    return build_report(repo, nodes, edges, components, warnings)


def build_report(
    repo: str,
    nodes: dict[int, Node],
    edges: list[Edge],
    components: list[list[int]],
    warnings: list[str],
) -> dict[str, object]:
    implemented_merged: list[dict[str, object]] = []
    superseded_open: list[dict[str, object]] = []
    closed_carriers: list[dict[str, object]] = []
    human_review: list[dict[str, object]] = []
    processing: list[dict[str, object]] = []

    for edge in edges:
        source = nodes.get(edge.source)
        target = nodes.get(edge.target)
        if not source or not target:
            continue
        if (
            source.open_inventory
            and source.item_type == "issue"
            and source.state == "open"
            and edge.relation == "lifecycle"
            and edge.detail == "implemented_by"
            and target.state == "merged"
        ):
            implemented_merged.append({"issue": source.number, "pr": target.number})
        if (
            source.open_inventory
            and source.item_type == "pr"
            and source.state == "open"
            and edge.relation == "lifecycle"
            and edge.detail == "superseded_by"
        ):
            superseded_open.append({"pr": source.number, "replacement": target.number})
        if (
            source.open_inventory
            and target.state in {"closed", "merged", "missing"}
            and edge.relation in {"declared", "lifecycle"}
            and _edge_names_payload(edge)
        ):
            closed_carriers.append(
                {
                    "source": source.number,
                    "target": target.number,
                    "target_state": target.state,
                    "relation": edge.detail,
                }
            )
        if edge.relation in {"declared", "context"}:
            human_review.append(
                {
                    "source": edge.source,
                    "target": edge.target,
                    "relation": edge.relation,
                    "evidence": [asdict(item) for item in edge.evidence],
                }
            )
        if edge.relation == "native" and edge.detail == "blocked_by":
            processing.append(
                {
                    "before": edge.target,
                    "after": edge.source,
                    "basis": "GitHub native blocked-by relation",
                }
            )
        if edge.relation == "lifecycle" and edge.detail == "implemented_by":
            processing.append(
                {
                    "before": edge.target,
                    "after": edge.source,
                    "basis": "explicit implementation relation",
                }
            )

    isolated = [
        component[0]
        for component in components
        if len(component) == 1 and nodes[component[0]].open_inventory
    ]
    structural_groups: dict[str, set[int]] = defaultdict(set)
    gate_groups: dict[str, set[int]] = defaultdict(set)
    for edge in edges:
        if edge.relation == "structural":
            structural_groups[edge.evidence[0].location].update((edge.source, edge.target))
        if edge.relation == "gate":
            gate_groups[edge.evidence[0].location].update((edge.source, edge.target))
    structural = [
        {"file": path, "prs": sorted(numbers)}
        for path, numbers in sorted(structural_groups.items())
    ]
    shared_gates = [
        {"check": check, "prs": sorted(numbers)}
        for check, numbers in sorted(gate_groups.items())
    ]
    return {
        "schema_version": 1,
        "repository": repo,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "method": {
            "open_inventory": "all open issues and pull requests",
            "closed_expansion": "one hop from open inventory",
            "relation_classes": [
                "native",
                "declared",
                "lifecycle",
                "structural",
                "gate",
                "context",
            ],
            "authority_note": (
                "Observational transport-state census; textual references do not create authority."
            ),
        },
        "stats": {
            "open_items": sum(node.open_inventory for node in nodes.values()),
            "open_issues": sum(
                node.open_inventory and node.item_type == "issue" for node in nodes.values()
            ),
            "open_prs": sum(
                node.open_inventory and node.item_type == "pr" for node in nodes.values()
            ),
            "context_nodes": sum(not node.open_inventory for node in nodes.values()),
            "edges": len(edges),
            "components": len(components),
        },
        "nodes": [asdict(nodes[number]) for number in sorted(nodes)],
        "edges": [
            {
                **{key: value for key, value in asdict(edge).items() if key != "evidence"},
                "evidence": [asdict(item) for item in edge.evidence],
            }
            for edge in edges
        ],
        "components": components,
        "highlights": {
            "open_issues_with_merged_implementation": implemented_merged,
            "open_prs_explicitly_superseded": superseded_open,
            "closed_or_missing_payload_references": closed_carriers,
            "shared_file_collisions": structural,
            "shared_failed_gates": shared_gates,
            "isolated_open_items": isolated,
            "recommended_processing_order": processing,
            "prerequisite_chains": prerequisite_chains(processing),
            "human_classification_required": human_review,
        },
        "warnings": sorted(set(warnings)),
    }


def _node_link(node: Node) -> str:
    return f"[#{node.number}]({node.url}) {node.title}"


def render_markdown(report: dict[str, object]) -> str:
    nodes = {int(node["number"]): Node(**node) for node in report["nodes"]}
    highlights = report["highlights"]
    stats = report["stats"]
    lines = [
        "# GitHub Dependency Census",
        "",
        f"Generated: `{report['generated_at']}`",
        "",
        (
            f"Open inventory: **{stats['open_items']}** "
            f"({stats['open_issues']} issues, {stats['open_prs']} PRs); "
            f"one-hop context: **{stats['context_nodes']}**; "
            f"edges: **{stats['edges']}**; components: **{stats['components']}**."
        ),
        "",
        "> Observational transport-state census. Textual references do not create authority.",
        "",
        "## Actionable Highlights",
        "",
    ]

    sections = (
        (
            "Open issues with merged implementation",
            highlights["open_issues_with_merged_implementation"],
            lambda item: (
                f"- {_node_link(nodes[item['issue']])} has merged implementation "
                f"{_node_link(nodes[item['pr']])}."
            ),
        ),
        (
            "Open PRs explicitly superseded",
            highlights["open_prs_explicitly_superseded"],
            lambda item: (
                f"- {_node_link(nodes[item['pr']])} is superseded by "
                f"{_node_link(nodes[item['replacement']])}."
            ),
        ),
        (
            "Closed or missing payload references",
            highlights["closed_or_missing_payload_references"],
            lambda item: (
                f"- {_node_link(nodes[item['source']])} references "
                f"{_node_link(nodes[item['target']])} "
                f"(`{item['target_state']}`, `{item['relation']}`)."
            ),
        ),
        (
            "Shared-file collision risks",
            highlights["shared_file_collisions"],
            lambda item: (
                f"- `{item['file']}`: "
                + ", ".join(f"#{number}" for number in item["prs"])
            ),
        ),
        (
            "Shared failed gates",
            highlights["shared_failed_gates"],
            lambda item: (
                f"- `{item['check']}`: "
                + ", ".join(f"#{number}" for number in item["prs"])
            ),
        ),
        (
            "Prerequisite chains",
            highlights["prerequisite_chains"],
            lambda item: "- " + " -> ".join(f"#{number}" for number in item),
        ),
        (
            "Recommended processing order",
            highlights["recommended_processing_order"],
            lambda item: (
                f"- #{item['before']} before #{item['after']} "
                f"({item['basis']})."
            ),
        ),
    )
    any_highlight = False
    for title, items, renderer in sections:
        if not items:
            continue
        any_highlight = True
        lines.extend([f"### {title}", "", *(renderer(item) for item in items), ""])
    if not any_highlight:
        lines.extend(["No actionable dependency findings.", ""])

    lines.extend(["## Connected Components", ""])
    for index, component in enumerate(report["components"], start=1):
        open_members = [
            number for number in component if nodes[number].open_inventory
        ]
        context_members = [
            number for number in component if not nodes[number].open_inventory
        ]
        ordered_members = open_members + context_members
        display_limit = 30
        displayed = ordered_members[:display_limit]
        links = ", ".join(
            f"[#{number}]({nodes[number].url})" for number in displayed
        )
        remainder = len(ordered_members) - len(displayed)
        if remainder:
            links += f", +{remainder} more (full membership in JSON)"
        lines.append(
            f"{index}. **{len(component)} nodes** "
            f"({len(open_members)} open): {links}"
        )
    lines.append("")

    lines.extend(["## Human Classification Required", ""])
    ambiguous = highlights["human_classification_required"]
    if ambiguous:
        markdown_limit = 100
        for item in ambiguous[:markdown_limit]:
            evidence = item["evidence"][0] if item["evidence"] else {}
            lines.append(
                f"- #{item['source']} -> #{item['target']} (`{item['relation']}`): "
                f"{evidence.get('snippet', '')} "
                f"([evidence]({evidence.get('location', '')}))"
            )
        if len(ambiguous) > markdown_limit:
            lines.append(
                f"- {len(ambiguous) - markdown_limit} additional ambiguous relationships "
                "are retained in the JSON artifact."
            )
    else:
        lines.append("No ambiguous declared or timeline-only relationships.")
    lines.append("")

    lines.extend(["## Isolated Open Items", ""])
    isolated = highlights["isolated_open_items"]
    lines.extend(
        (_node_link(nodes[number]) for number in isolated),
    )
    if not isolated:
        lines.append("None.")
    lines.append("")

    if report["warnings"]:
        lines.extend(["## Collection Warnings", ""])
        lines.extend(f"- {warning}" for warning in report["warnings"])
        lines.append("")
    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--repo",
        default=os.environ.get("GITHUB_REPOSITORY", ""),
        help="GitHub repository in owner/name form",
    )
    parser.add_argument("--markdown-path", type=Path, required=True)
    parser.add_argument("--json-path", type=Path, required=True)
    parser.add_argument("--timeout", type=int, default=30)
    parser.add_argument("--max-pages", type=int, default=10)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    if not args.repo:
        print("--repo or GITHUB_REPOSITORY is required", file=sys.stderr)
        return 2
    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN") or ""
    client = GitHubClient(
        args.repo,
        token=token,
        timeout=args.timeout,
        max_pages=args.max_pages,
    )
    try:
        report = collect_census(client, args.repo)
    except Exception as exc:
        print(f"github dependency census failed: {exc}", file=sys.stderr)
        return 1
    args.json_path.write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    args.markdown_path.write_text(render_markdown(report), encoding="utf-8")
    print(json.dumps(report["stats"], sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
