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
        "generated_note": "Derived bootstrap index for !/agent.sh. Do not hand-edit.",
        "authority_chain": {
            "narrative_registry": control_plane["narrative_registry"],
            "machine_registry": "swarm.json",
            "bootstrap_index": control_plane["bootstrap_index"],
            "bootstrap_entrypoint": control_plane["bootstrap_entrypoint"],
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
        help="Path to the generated bootstrap index.",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Validate that the output file already matches the generated content.",
    )
    args = parser.parse_args()

    source_path = Path(args.source)
    output_path = Path(args.output)
    rendered = json.dumps(build_bootstrap_index(load_json(source_path)), indent=2) + "\n"

    if args.check:
        current = output_path.read_text(encoding="utf-8") if output_path.exists() else ""
        return 0 if current == rendered else 1

    output_path.write_text(rendered, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
