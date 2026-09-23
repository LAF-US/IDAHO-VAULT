from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path


def _load_module():
    project_root = Path(__file__).resolve().parents[1]
    script_path = project_root / ".github" / "scripts" / "github_dependency_report.py"
    spec = importlib.util.spec_from_file_location("github_dependency_report_test_module", script_path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


census = _load_module()
REPO = "LAF-US/IDAHO-VAULT"


def node(
    number: int,
    *,
    item_type: str = "issue",
    state: str = "open",
    title: str | None = None,
    files: tuple[str, ...] = (),
    failed_checks: tuple[str, ...] = (),
    open_inventory: bool = True,
    merged_at: str | None = None,
):
    return census.Node(
        number=number,
        item_type=item_type,
        state=state,
        title=title or f"Item {number}",
        url=f"https://github.com/{REPO}/{'pull' if item_type == 'pr' else 'issues'}/{number}",
        files=list(files),
        checks=[
            {"name": check, "state": "FAILURE", "url": "https://example.test/check"}
            for check in failed_checks
        ],
        open_inventory=open_inventory,
        merged_at=merged_at,
    )


class FakeClient:
    def __init__(self, snapshots, context=None, failures=None):
        self.snapshots = snapshots
        self.context = context or {}
        self.failures = failures or {}

    def list_open_nodes(self):
        return [snapshot.node for snapshot in self.snapshots.values()]

    def fetch_snapshot(self, number):
        if number in self.failures:
            raise RuntimeError(self.failures[number])
        return self.snapshots[number]

    def fetch_context_node(self, number):
        return self.context.get(number)


class ReferenceExtractionTest(unittest.TestCase):
    def test_extracts_same_repo_references_without_external_or_large_ids(self):
        text = """
        Tracks #509 and LAF-US/IDAHO-VAULT#510.
        See https://github.com/LAF-US/IDAHO-VAULT/pull/400.
        External [#37](https://github.com/actions/upload-artifact/pull/37).
        <a href="https://redirect.github.com/1password/install-cli-action/issues/41">#41</a>
        GCP project #1091966715900.
        Cultural reference xkcd #927.
        """
        self.assertEqual(census.extract_references(text, REPO), {400, 509, 510})

    def test_lifecycle_edges_are_ranked_above_declared_references(self):
        edges = census.text_edges(
            478,
            census.TextSource("https://example.test/comment", "Superseded by #507. Related: #399."),
            REPO,
        )
        self.assertEqual(
            {(edge.target, edge.relation, edge.confidence, edge.detail) for edge in edges},
            {
                (507, "lifecycle", "high", "superseded_by"),
                (399, "declared", "medium", "references"),
            },
        )


class GraphConstructionTest(unittest.TestCase):
    def test_known_cluster_fixture_builds_all_relation_classes(self):
        snapshots = {
            400: census.Snapshot(
                node(400, item_type="pr", files=("CLAUDE.md",)),
                texts=[census.TextSource("https://example.test/400", "Outstanding work is in #446.")],
                timeline_sources=[(441, "https://example.test/441")],
            ),
            446: census.Snapshot(node(446)),
            501: census.Snapshot(node(501)),
            503: census.Snapshot(
                node(
                    503,
                    item_type="pr",
                    files=(".coderabbit.yaml",),
                    failed_checks=("policy-check",),
                ),
                texts=[census.TextSource("https://example.test/503", "Related to #399.")],
            ),
            507: census.Snapshot(
                node(
                    507,
                    item_type="pr",
                    files=(".github/workflows/opencode.yml",),
                    failed_checks=("check-version-transitions",),
                )
            ),
            509: census.Snapshot(
                node(509),
                texts=[
                    census.TextSource(
                        "https://example.test/509",
                        "Implementation filed in draft PR #510.",
                    )
                ],
            ),
            511: census.Snapshot(
                node(511, item_type="pr", files=("shared.md",), failed_checks=("policy-check",))
            ),
            512: census.Snapshot(
                node(512),
                native=[(511, "blocked_by")],
                texts=[census.TextSource("https://example.test/512", "Related PR #513.")],
            ),
            513: census.Snapshot(
                node(
                    513,
                    item_type="pr",
                    files=("shared.md",),
                    failed_checks=("check-version-transitions",),
                )
            ),
        }
        context = {
            399: node(399, open_inventory=False),
            441: node(441, item_type="pr", state="closed", open_inventory=False),
            510: node(
                510,
                item_type="pr",
                state="merged",
                open_inventory=False,
                merged_at="2026-06-11T19:43:51Z",
            ),
        }

        report = census.collect_census(FakeClient(snapshots, context), REPO)
        relations = {edge["relation"] for edge in report["edges"]}
        self.assertEqual(
            relations,
            {"native", "declared", "lifecycle", "structural", "gate", "context"},
        )
        self.assertIn(
            {"issue": 509, "pr": 510},
            report["highlights"]["open_issues_with_merged_implementation"],
        )
        self.assertIn(
            {"before": 511, "after": 512, "basis": "GitHub native blocked-by relation"},
            report["highlights"]["recommended_processing_order"],
        )
        self.assertIn(
            {"file": "shared.md", "prs": [511, 513]},
            report["highlights"]["shared_file_collisions"],
        )
        self.assertIn(
            {"check": "check-version-transitions", "prs": [507, 513]},
            report["highlights"]["shared_failed_gates"],
        )
        self.assertIn([511, 512], report["highlights"]["prerequisite_chains"])
        self.assertIn(501, report["highlights"]["isolated_open_items"])

    def test_one_hop_context_does_not_expand_context_body(self):
        snapshots = {
            509: census.Snapshot(
                node(509),
                texts=[census.TextSource("https://example.test/509", "Implemented by PR #510.")],
            )
        }
        context = {
            510: node(510, item_type="pr", state="merged", open_inventory=False),
            999: node(999, open_inventory=False),
        }
        client = FakeClient(snapshots, context)
        report = census.collect_census(client, REPO)
        self.assertEqual({item["number"] for item in report["nodes"]}, {509, 510})

    def test_cycle_handling_keeps_single_component(self):
        snapshots = {
            1: census.Snapshot(
                node(1),
                texts=[census.TextSource("https://example.test/1", "Related #2.")],
            ),
            2: census.Snapshot(
                node(2),
                texts=[census.TextSource("https://example.test/2", "Related #1.")],
            ),
        }
        report = census.collect_census(FakeClient(snapshots), REPO)
        self.assertEqual(report["components"], [[1, 2]])

    def test_missing_context_and_collection_failure_are_reported(self):
        snapshots = {
            1: census.Snapshot(
                node(1),
                texts=[census.TextSource("https://example.test/1", "Related #404.")],
            ),
            2: census.Snapshot(node(2)),
        }
        report = census.collect_census(
            FakeClient(snapshots, failures={2: "timeline timeout"}),
            REPO,
        )
        missing = next(item for item in report["nodes"] if item["number"] == 404)
        self.assertEqual(missing["state"], "missing")
        self.assertTrue(any("#2: detail collection failed" in warning for warning in report["warnings"]))

    def test_bounded_pagination_stops_on_short_page(self):
        client = census.GitHubClient(REPO, token="", max_pages=3)
        responses = {
            1: [{"number": index} for index in range(100)],
            2: [{"number": 101}],
        }

        def request(path, **_kwargs):
            page = int(path.rsplit("page=", 1)[1])
            return responses[page]

        client._request = request
        records = client._pages("/repos/example/issues?state=open")
        self.assertEqual(len(records), 101)

    def test_empty_body_is_safe(self):
        self.assertEqual(census.extract_references("", REPO), set())
        self.assertEqual(
            census.text_edges(1, census.TextSource("https://example.test/1", ""), REPO),
            [],
        )

    def test_closed_payload_reference_is_highlighted(self):
        snapshots = {
            424: census.Snapshot(
                node(424, item_type="pr"),
                texts=[
                    census.TextSource(
                        "https://example.test/424",
                        "This record was superseded by #490.",
                    )
                ],
            )
        }
        context = {490: node(490, item_type="pr", state="closed", open_inventory=False)}
        report = census.collect_census(FakeClient(snapshots, context), REPO)
        self.assertEqual(
            report["highlights"]["closed_or_missing_payload_references"],
            [
                {
                    "source": 424,
                    "target": 490,
                    "target_state": "closed",
                    "relation": "superseded_by",
                }
            ],
        )

    def test_markdown_contains_human_classification_section(self):
        snapshots = {
            512: census.Snapshot(
                node(512),
                texts=[census.TextSource("https://example.test/512", "Related to #511.")],
            ),
            511: census.Snapshot(node(511, item_type="pr")),
        }
        report = census.collect_census(FakeClient(snapshots), REPO)
        markdown = census.render_markdown(report)
        self.assertIn("## Human Classification Required", markdown)
        self.assertIn("#512 -> #511", markdown)


if __name__ == "__main__":
    unittest.main()
