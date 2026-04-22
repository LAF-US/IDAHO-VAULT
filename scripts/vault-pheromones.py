#!/usr/bin/env python3
"""
vault-pheromones.py — SBP Phase 1: Shadow Layer

Demonstrates stigmergic coordination without modifying existing systems.
Agents emit pheromones; others sense. No coordination changes yet.

Usage:
    python vault-pheromones.py emit <trail> <type> <intensity>
    python vault-pheromones.py sniff <trail>
    python vault-pheromones.py beat   # Emit agent heartbeat
    python vault-pheromones.py status # Show all active pheromones
    python vault-pheromones.py register <trail> <condition>  # Register scent trigger
"""

import sys
import time
from sbp import SbpClient, SbpAgent, run_agent

AGENT_NAME = "opencode"

def emit(trail: str, pheromone_type: str, intensity: float, payload: dict = None):
    """Emit a pheromone to the blackboard."""
    with SbpClient(local=True) as client:
        result = client.emit(trail, pheromone_type, intensity, payload=payload or {})
        print(f"EMITTED: {trail}/{pheromone_type} intensity={intensity}")
        if payload:
            print(f"  payload: {payload}")
        return result

def sniff(trail: str):
    """Sniff the blackboard for a trail's pheromones."""
    with SbpClient(local=True) as client:
        result = client.sniff(trails=[trail])
        print(f"SNIFF: {trail}")
        if result.pheromones:
            for p in result.pheromones:
                print(f"  {p.type}: {p.current_intensity:.2f} (initial: {p.initial_intensity})")
        else:
            print("  (no pheromones)")
        return result

def heartbeat():
    """Emit agent heartbeat pheromone."""
    trail = f"vault.agent.{AGENT_NAME}"
    return emit(trail, "heartbeat", 0.8, {
        "agent": AGENT_NAME,
        "timestamp": int(time.time()),
        "status": "active"
    })

def status():
    """Show all active pheromones in the vault trail namespace."""
    with SbpClient(local=True) as client:
        result = client.sniff(trails=["vault/"])
        print("VAULT STATUS:")
        if result.pheromones:
            by_trail = {}
            for p in result.pheromones:
                if p.trail not in by_trail:
                    by_trail[p.trail] = []
                by_trail[p.trail].append(p)
            for trail, pheromones in by_trail.items():
                print(f"  {trail}")
                for p in pheromones:
                    print(f"    {p.type}: {p.current_intensity:.2f}")
        else:
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