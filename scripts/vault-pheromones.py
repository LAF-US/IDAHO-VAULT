#!/usr/bin/env python3
"""
vault-pheromones.py — SBP Phase 1: Shadow Layer

Demonstrates stigmergic coordination using a file-based blackboard.
Agents emit pheromones to a JSON file; others sense.
No coordination changes yet to existing systems.

Usage:
    python vault-pheromones.py emit <trail> <type> <intensity> [payload_json]
    python vault-pheromones.py sniff <trail>
    python vault-pheromones.py beat   # Emit agent heartbeat
    python vault-pheromones.py status # Show all active pheromones
"""

import sys
import time
import json
import os
from pathlib import Path

AGENT_NAME = "opencode"
BLACKBOARD = Path("!/sbp-blackboard.json")

TRAILS = [
    "vault.agent",
    "vault.signal",
    "vault.docket",
    "vault.security",
    "vault.branch",
    "vault.daily",
]

def load_blackboard():
    """Load blackboard from JSON file."""
    if BLACKBOARD.exists():
        with open(BLACKBOARD) as f:
            return json.load(f)
    return {"pheromones": {}, "trails": []}

def save_blackboard(data):
    """Save blackboard to JSON file."""
    BLACKBOARD.parent.mkdir(parents=True, exist_ok=True)
    with open(BLACKBOARD, "w") as f:
        json.dump(data, f, indent=2)

def emit(trail: str, pheromone_type: str, intensity: float, payload: dict = None):
    """Emit a pheromone to the blackboard."""
    data = load_blackboard()
    key = f"{trail}/{pheromone_type}"
    now = time.time()
    decay_seconds = 300  # 5 min decay

    if key in data["pheromones"]:
        existing = data["pheromones"][key]
        data["pheromones"][key] = {
            "trail": trail,
            "type": pheromone_type,
            "initial_intensity": intensity,
            "current_intensity": intensity,
            "last_reinforced": now,
            "emitted_at": existing.get("emitted_at", now),
            "payload": payload or existing.get("payload"),
            "decay_seconds": decay_seconds,
        }
    else:
        data["pheromones"][key] = {
            "trail": trail,
            "type": pheromone_type,
            "initial_intensity": intensity,
            "current_intensity": intensity,
            "last_reinforced": now,
            "emitted_at": now,
            "payload": payload,
            "decay_seconds": decay_seconds,
        }
        if trail not in data["trails"]:
            data["trails"].append(trail)

    save_blackboard(data)
    print(f"EMITTED: {trail}/{pheromone_type} intensity={intensity}")
    if payload:
        print(f"  payload: {payload}")

def current_intensity(p):
    """Calculate current intensity with exponential decay."""
    now = time.time()
    age = now - p["last_reinforced"]
    if age > p["decay_seconds"]:
        return 0
    half_life = p["decay_seconds"] / 2
    return p["initial_intensity"] * (0.5 ** (age / half_life))

def sniff(trail: str):
    """Sniff the blackboard for a trail's pheromones."""
    data = load_blackboard()
    found = []

    for key, p in data["pheromones"].items():
        # Match exact trail or prefix
        if p["trail"] == trail or p["trail"].startswith(trail + "."):
            intensity = current_intensity(p)
            if intensity > 0.01:
                found.append((key, p, intensity))

    print(f"SNIFF: {trail}")
    if found:
        for key, p, intensity in found:
            print(f"  {p['type']}: {intensity:.2f}")
            if p.get("payload"):
                print(f"    payload: {p['payload']}")
    else:
        print("  (no pheromones)")

def status():
    """Show all active pheromones across vault trails."""
    print("VAULT PHEROMONE STATUS:")
    data = load_blackboard()
    found = False

    for trail in TRAILS:
        trail_found = []
        for key, p in data["pheromones"].items():
            if p["trail"] == trail or p["trail"].startswith(trail + "."):
                intensity = current_intensity(p)
                if intensity > 0.01:
                    trail_found.append((key, p, intensity))

        if trail_found:
            found = True
            print(f"  {trail}:")
            for key, p, intensity in trail_found:
                print(f"    {p['type']}: {intensity:.2f}")
                if p.get("payload"):
                    print(f"      {p['payload']}")

    if not found:
        print("  (blackboard empty)")

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == "emit":
        if len(sys.argv) < 5:
            print("Usage: emit <trail> <type> <intensity> [payload_json]")
            sys.exit(1)
        trail = sys.argv[2]
        ptype = sys.argv[3]
        intensity = float(sys.argv[4])
        payload = None
        if len(sys.argv) > 5:
            payload = json.loads(sys.argv[5])
        emit(trail, ptype, intensity, payload)

    elif cmd == "sniff":
        if len(sys.argv) < 3:
            print("Usage: sniff <trail>")
            sys.exit(1)
        sniff(sys.argv[2])

    elif cmd == "beat":
        heartbeat()

    elif cmd == "status":
        status()

    else:
        print(f"Unknown command: {cmd}")
        print(__doc__)
        sys.exit(1)

if __name__ == "__main__":
    main()