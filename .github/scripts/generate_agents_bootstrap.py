#!/usr/bin/env python3
"""Generate the non-executable agent discovery index from swarm.json."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

REQUIRED_CONTEXT = [
    "CONSTITUTION.md",
    "DECISIONS.md",
    "VAULT-CONVENTIONS.md",
]

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from startup_surfaces import candidates, resolve_rel  # noqa: E402

# Resolved so the discovery index points at the file that is actually there;
# falls back to the canonical path when a surface is absent entirely.
OPTIONAL_CONTEXT = [
    resolve_rel("WAKEUP") or "!/WAKEUP.md",
    resolve_rel("NEST_AGENTS") or "!/AGENTS.md",
    "LEVELSET.md",
]


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def build_discovery_index(swarm: dict) -> dict:
    control_plane = swarm["control_plane"]
    crews = swarm.get("crews", {})
    agents: dict[str, dict] = {}

    for agent in swarm.get("agents", []):
        instructions_file = agent.get("autoload_file")
        if not instructions_file:
            continue

        agents[agent["id"]] = {
            "id": agent["id"],
            "name": agent["name"],
            "vendor": agent["vendor"],
            "dotfolder": agent.get("dotfolder"),
            "capability_tier": agent["capability_tier"],
            "instructions_file": instructions_file,
            "autoload": agent.get("autoload", False),
            "context": {
                "required": REQUIRED_CONTEXT,
                "optional": OPTIONAL_CONTEXT,
            },
        }

    return {
        "source_of_truth": "swarm.json",
        "status": "generated",
        "purpose": "discovery_index",
        "generated_note": "Derived orientation index for task-relevant discovery only. It is not a launcher or authority grant. Do not hand-edit.",
        "authority_chain": {
            "narrative_registry": control_plane["narrative_registry"],
            "machine_registry": "swarm.json",
            "discovery_index": control_plane["discovery_index"],
            "compatibility_mirror": "agents.json",
        },
        "wakeup_protocol": swarm.get("wakeup_protocol", {}),
        "control_plane": {
            "coordination_hub_issue": control_plane["coordination_hub_issue"],
            "scoped_issue": control_plane["scoped_issue"],
            "system_roles": control_plane["system_roles"],
            "scope_note": control_plane.get("scope_note"),
        },
        "crewai_layer": {
            "status": crews.get("status"),
            "manifest": crews.get("manifest"),
            "manifest_doc": crews.get("manifest_doc"),
            "output_dir": crews.get("output_dir"),
            "runtime_class": crews.get("runtime_class"),
            "authority_boundary": crews.get("authority_boundary"),
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
        help="Path to the canonical generated discovery index.",
    )
    parser.add_argument(
        "--compat-output",
        default="agents.json",
        help="Optional path to the root compatibility mirror.",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Validate that the canonical discovery index and compatibility mirror match generated content.",
    )
    args = parser.parse_args()

    source_path = Path(args.source)
    rendered = json.dumps(build_discovery_index(load_json(source_path)), indent=2) + "\n"
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

    # Keep the canonical discovery index and root mirror byte-for-byte aligned.
    for output_path in deduped_outputs:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(rendered, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
