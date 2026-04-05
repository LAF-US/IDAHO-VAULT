#!/usr/bin/env python3
"""
Crawler Crew — Post-CHAINFIRE Vault Mapping (LOCAL CARTOGRAPHER)
Part of the [STABILIZE }!{ IGNITE] v2 plan.

This script performs the initial mapping of the 23,202 root stubs.
To conserve API credits, this Phase 1 uses a local regex/path-walk 
to categorize the "Address Space" before the LLM Linker is ignited.

LINUX }!{ — targets Linux-native execution.
"""

import os
import re
from datetime import datetime, timezone
from pathlib import Path

# --- Configuration ---
VAULT_ROOT = Path(__file__).resolve().parent.parent.parent
NEURON_100 = VAULT_ROOT / "100.md"
EXCLUSIONS = ["!", "swarm", ".github", ".obsidian", "INBOX"]

# --- Local Mapping Logic ---

def scan_vault():
    """Walks the root directory and categorizes .md stubs."""
    stats = {
        "total_stubs": 0,
        "factual_notes": 0,
        "empty_stubs": 0,
        "governed_notes": 0, # Has frontmatter
        "newest_factual": [],
    }

    # Only scan the root-flat files (Phase 1 mapping)
    for item in VAULT_ROOT.iterdir():
        if item.is_file() and item.suffix == ".md" and not any(ex in item.parts for ex in EXCLUSIONS):
            stats["total_stubs"] += 1
            
            # Read content
            try:
                content = item.read_text(encoding="utf-8")
                size = len(content.strip())
                
                if size == 0:
                    stats["empty_stubs"] += 1
                else:
                    stats["factual_notes"] += 1
                    # Check for frontmatter
                    if content.startswith("---"):
                        stats["governed_notes"] += 1
                    
                    # Track some samples
                    if len(stats["newest_factual"]) < 5:
                        stats["newest_factual"].append(item.name)
            except Exception as e:
                print(f"Error reading {item.name}: {e}")

    return stats

def update_neuron_100(stats):
    """Writes the mapping results to Neuron 100.md."""
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    
    discovery_pct = (stats["factual_notes"] / stats["total_stubs"]) * 100 if stats["total_stubs"] > 0 else 0
    
    content = f"""
## Cartographer Snapshot — {now[:10]}

The local mapping of the root-flat Address Space is complete.

| Metric | Count |
|--------|-------|
| Total Stubs Scanned | {stats["total_stubs"]} |
| Factual Notes discovered | {stats["factual_notes"]} |
| Empty Stubs Remaining | {stats["empty_stubs"]} |
| Governed Notes (with frontmatter) | {stats["governed_notes"]} |
| **Discovery Percent** | **{discovery_pct:.2f}%** |

### Sample Factual Nodes
- {", ".join(stats["newest_factual"])}

---
*Updated by The Local Cartographer (Bartimaeus) at {now}*
"""
    
    if NEURON_100.exists():
        current_text = NEURON_100.read_text(encoding="utf-8")
        # Append or replace the section if common anchor exists
        if "## Cartographer Snapshot" in current_text:
            # Replace existing snapshot (simple version)
            new_text = re.sub(r"## Cartographer Snapshot.*---", content, current_text, flags=re.DOTALL)
        else:
            new_text = current_text.rstrip() + "\n\n" + content
        
        NEURON_100.write_text(new_text, encoding="utf-8")
        return f"Updated {NEURON_100.name}"
    else:
        # Create it if Claude's init didn't work for some reason
        header = f"""---
title: "100"
date created: "{now[:10]}"
authority: crewai
doc_class: neuron
---

# 100 (Address Space Controller)

{content}
"""
        NEURON_100.write_text(header, encoding="utf-8")
        return f"Created {NEURON_100.name}"

if __name__ == "__main__":
    print("Igniting The Local Cartographer...")
    results = scan_vault()
    print(f"Scan complete. Found {results['factual_notes']} factual notes out of {results['total_stubs']} total files.")
    log = update_neuron_100(results)
    print(log)
