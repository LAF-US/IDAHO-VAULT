#!/usr/bin/env python3
"""Generate the local agent bootstrap index from swarm.json."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

REQUIRED_CONTEXT = [
    "!/README.md",
    "!/CONSTITUTION.md",
    "!/AGENTS.md",
    "!/DECISIONS.md",
    "!/VAULT-CONVENTIONS.md",
]

OPTIONAL_CONTEXT = [
    "!/LEVELSET.md",
]

BOOTSTRAP_FIELDS = [
    "invoke_as",
    "instructions_file",
    "git_author_name",
    "git_author_email",
    "git_author_suffix",
    "supports_local_bootstrap",
]


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def build_bootstrap_index(swarm: dict) -> dict:
    control_plane = swarm["control_plane"]
    agents: dict[str, dict] = {}

    for agent in swarm.get("agents", []):
        bootstrap = agent.get("bootstrap")
        if not bootstrap:
            continue

        missing = [field for field in BOOTSTRAP_FIELDS if field not in bootstrap]
        if missing:
            joined = ", ".join(missing)
            raise ValueError(f"Agent {agent['id']} missing bootstrap fields: {joined}")

        if not bootstrap["supports_local_bootstrap"]:
            continue

        invoke_as = bootstrap["invoke_as"]
        if invoke_as in agents:
            raise ValueError(f"Duplicate invoke_as '{invoke_as}': agent {agent['id']} conflicts with existing agent {agents[invoke_as]['id']}")

        agents[invoke_as] = {
            "id": agent["id"],
            "name": agent["name"],
            "vendor": agent["vendor"],
            "dotfolder": agent.get("dotfolder"),
            "capability_tier": agent["capability_tier"],
            "instructions_file": bootstrap["instructions_file"],
            "supports_local_bootstrap": True,
            "git_identity": {
                "name": bootstrap["git_author_name"],
                "email": bootstrap["git_author_email"],
                "suffix": bootstrap["git_author_suffix"],
            },
            "context": {
                "required": REQUIRED_CONTEXT,
                "optional": OPTIONAL_CONTEXT,
            },
        }

    return {
        "source_of_truth": "swarm.json",
        "status": "generated",
        "generated_note": "Derived bootstrap index for !/agent.sh and the root compatibility wrapper. Do not hand-edit.",
        "authority_chain": {
            "narrative_registry": control_plane["narrative_registry"],
            "machine_registry": "swarm.json",
            "bootstrap_index": control_plane["bootstrap_index"],
            "bootstrap_entrypoint": control_plane["bootstrap_entrypoint"],
            "compatibility_mirror": "agents.json",
            "compatibility_wrapper": "agent.sh",
        },
        "control_plane": {
            "coordination_hub_issue": control_plane["coordination_hub_issue"],
            "scoped_issue": control_plane["scoped_issue"],
            "system_roles": control_plane["system_roles"],
        },
        "agents": dict(sorted(agents.items())),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--source",
        default="swarm.json",
        help="Path to the canonical machine-readable swarm registry.",
    )
    parser.add_argument(
        "--output",
        default="!/agents.json",
        help="Path to the canonical generated bootstrap index.",
    )
    parser.add_argument(
        "--compat-output",
        default="agents.json",
        help="Optional path to the root compatibility mirror.",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Validate that the canonical index and compatibility mirror match the generated content.",
    )
    args = parser.parse_args()

    source_path = Path(args.source)
    rendered = json.dumps(build_bootstrap_index(load_json(source_path)), indent=2) + "\n"
    output_paths = [Path(args.output), Path(args.compat_output)]
    deduped_outputs: list[Path] = []

    for path in output_paths:
        if path not in deduped_outputs:
            deduped_outputs.append(path)

    if args.check:
        for output_path in deduped_outputs:
            current = output_path.read_text(encoding="utf-8") if output_path.exists() else ""
            if current != rendered:
                return 1
        return 0

    # Keep the canonical !/ index and the legacy root mirror byte-for-byte aligned.
    for output_path in deduped_outputs:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(rendered, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
