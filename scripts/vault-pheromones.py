#!/usr/bin/env python3
"""
vault-pheromones.py — SBP Phase 2 + 3: Stigmergic Coordination + Guard Layer

Path B: SQLite-backed field for cross-session continuity.
Path C: Capability-scoped access, authority boundaries, claims.

Usage:
    python vault-pheromones.py emit <trail> <type> <intensity> [payload_json]
    python vault-pheromones.py sniff <trail>
    python vault-pheromones.py beat              # Emit agent heartbeat
    python vault-pheromones.py status           # Show all pheromones
    python vault-pheromones.py register <scent_id> <trail> <operator> <value> <action>
    python vault-pheromones.py scents            # Show registered scents
    python vault-pheromones.py check           # Check triggers and fire actions
    python vault-pheromones.py watch           # Continuous monitoring mode
    python vault-pheromones.py arrive        # Register agent arrival
    python vault-pheromones.py claim <trail>  # Claim a trail for this agent
    python vault-pheromones.py depart          # Deregister this agent
    python vault-pheromones.py field         # Show field status
    
    # Path C: Guard layer
    python vault-pheromones.py grant <agent> <cap> <trail>  # Grant capability
    python vault-pheromones.py revoke <agent> <cap> <trail>   # Revoke capability
    python vault-pheromones.py perms <agent>    # Show agent capabilities
    python vault-pheromones.py trust          # Show trust relationships
    python vault-pheromones.py guard <action> <trail>       # Test guard
"""

import sys
import time
import json
import sqlite3
import subprocess
import os
from pathlib import Path

# Force unbuffered output on Windows
if sys.platform == 'win32':
    import msvcrt
    msvcrt.setmode(sys.stdout.fileno(), os.O_BINARY)
    msvcrt.setmode(sys.stderr.fileno(), os.O_BINARY)

AGENT_NAME = "opencode"
BLACKBOARD = Path("!/sbp-blackboard.json")
FIELD = Path("!/sbp-field.db")

TRAILS = [
    "vault.agent",
    "vault.signal",
    "vault.docket",
    "vault.security",
    "vault.branch",
    "vault.daily",
]

CAPABILITIES = ["read", "write", "execute"]

def get_db():
    """Get SQLite connection."""
    FIELD.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(FIELD))
    conn.row_factory = sqlite3.Row
    return conn

def init_field():
    """Initialize SQLite field schema."""
    conn = get_db()
    c = conn.cursor()
    
    c.execute('''CREATE TABLE IF NOT EXISTS pheromones (
        id INTEGER PRIMARY KEY,
        trail TEXT NOT NULL,
        ptype TEXT NOT NULL,
        initial_intensity REAL,
        current_intensity REAL,
        last_reinforced REAL,
        emitted_at REAL,
        payload TEXT,
        decay_seconds INTEGER DEFAULT 300,
        urgency INTEGER DEFAULT 1,
        risk INTEGER DEFAULT 1,
        confidence INTEGER DEFAULT 1,
        UNIQUE(trail, ptype)
    )''')
    
    c.execute('PRAGMA table_info(pheromones)')
    cols = [row[1] for row in c.fetchall()]
    if 'urgency' not in cols:
        c.execute('ALTER TABLE pheromones ADD COLUMN urgency INTEGER DEFAULT 1')
    if 'risk' not in cols:
        c.execute('ALTER TABLE pheromones ADD COLUMN risk INTEGER DEFAULT 1')
    if 'confidence' not in cols:
        c.execute('ALTER TABLE pheromones ADD COLUMN confidence INTEGER DEFAULT 1')
    
    c.execute('''CREATE TABLE IF NOT EXISTS scents (
        scent_id TEXT PRIMARY KEY,
        trail TEXT NOT NULL,
        operator TEXT NOT NULL,
        value REAL NOT NULL,
        action TEXT NOT NULL,
        registered_at REAL,
        last_triggered REAL
    )''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS agents (
        agent_id TEXT PRIMARY KEY,
        arrival REAL,
        last_seen REAL,
        claimed_trail TEXT,
        status TEXT DEFAULT 'active'
    )''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS capabilities (
        id INTEGER PRIMARY KEY,
        agent_id TEXT NOT NULL,
        capability TEXT NOT NULL,
        trail_pattern TEXT NOT NULL,
        granted_at REAL,
        granted_by TEXT,
        UNIQUE(agent_id, capability, trail_pattern)
    )''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS trust (
        id INTEGER PRIMARY KEY,
        trustee TEXT NOT NULL,
        trustor TEXT NOT NULL,
        trust_level INTEGER DEFAULT 1,
        scope TEXT,
        created_at REAL,
        UNIQUE(trustee, trustor)
    )''')
    
    c.execute('''CREATE INDEX IF NOT EXISTS idx_pheromones_trail ON pheromones(trail)''')
    c.execute('''CREATE INDEX IF NOT EXISTS idx_agents_status ON agents(status)''')
    
    conn.commit()
    return conn

def load_blackboard():
    """Load blackboard from JSON file (legacy compatibility)."""
    if BLACKBOARD.exists():
        with open(BLACKBOARD) as f:
            return json.load(f)
    return {"pheromones": {}, "trails": [], "scents": {}}

def save_blackboard(data):
    """Save blackboard to JSON file (legacy compatibility)."""
    BLACKBOARD.parent.mkdir(parents=True, exist_ok=True)
    with open(BLACKBOARD, "w") as f:
        json.dump(data, f, indent=2)

def current_intensity(p):
    """Calculate current intensity with exponential decay."""
    now = time.time()
    age = now - p.get("last_reinforced", now)
    decay = p.get("decay_seconds", 300)
    if age > decay:
        return 0
    half_life = decay / 2
    return p.get("initial_intensity", 0) * (0.5 ** (age / half_life))

def pressure_score(p) -> float:
    """Calculate pressure score: urgency * risk * confidence weighting."""
    urgency = p.get("urgency", 1)
    risk = p.get("risk", 1)
    confidence = p.get("confidence", 1)
    return urgency * risk * confidence

def weighted_intensity(p) -> float:
    """Calculate intensity with pressure weighting."""
    base = current_intensity(p)
    pressure = pressure_score(p)
    return base * pressure

def emit(trail: str, ptype: str, intensity: float, payload: dict = None, urgency: int = 1, risk: int = 1, confidence: int = 1):
    """Emit a pheromone to the field (guarded with pressure scoring)."""
    if not check_capability(AGENT_NAME, "write", trail):
        print(f"GUARD DENIED: {AGENT_NAME} write on {trail}")
        return
    
    conn = init_field()
    c = conn.cursor()
    now = time.time()
    decay = 300
    
    c.execute('SELECT emitted_at FROM pheromones WHERE trail=? AND ptype=?', (trail, ptype))
    row = c.fetchone()
    existing_emitted_at = row[0] if row else now
    
    c.execute('''INSERT OR REPLACE INTO pheromones 
        (trail, ptype, initial_intensity, current_intensity, last_reinforced, emitted_at, payload, decay_seconds, urgency, risk, confidence)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
        (trail, ptype, intensity, intensity, now, existing_emitted_at, json.dumps(payload), decay, urgency, risk, confidence))
    
    conn.commit()
    print(f"EMITTED: {trail}/{ptype} intensity={intensity}")
    if urgency > 1 or risk > 1 or confidence > 1:
        print(f"  pressure: urgency={urgency}, risk={risk}, confidence={confidence}")
    if payload:
        print(f"  payload: {payload}")

def sniff(trail: str, verbose=True):
    """Sniff the field for a trail's pheromones."""
    conn = init_field()
    c = conn.cursor()
    now = time.time()
    
    c.execute('SELECT trail, ptype, initial_intensity, last_reinforced, emitted_at, payload, decay_seconds FROM pheromones WHERE trail=? OR trail LIKE ?', 
              (trail, trail + '.%'))
    rows = c.fetchall()
    
    found = []
    for row in rows:
        p = dict(row)
        intensity = current_intensity(p)
        if intensity > 0.01:
            found.append((p['trail'], p['ptype'], intensity, p.get('payload')))
    
    if verbose:
        print(f"SNIFF: {trail}")
        if found:
            for t, ttype, intensity, payload in found:
                print(f"  {ttype}: {intensity:.2f}")
                if payload:
                    print(f"    payload: {payload}")
        else:
            print("  (no pheromones)")
    return found

def heartbeat():
    """Emit agent heartbeat."""
    trail = f"vault.agent.{AGENT_NAME}"
    payload = {"agent": AGENT_NAME, "timestamp": int(time.time()), "status": "active"}
    emit(trail, "heartbeat", 0.8, payload)

def status():
    """Show all active pheromones across vault trails."""
    print("VAULT PHEROMONE STATUS:")
    conn = init_field()
    now = time.time()
    found = False
    
    for trail in TRAILS:
        c = conn.cursor()
        c.execute('SELECT trail, ptype, initial_intensity, last_reinforced, payload, decay_seconds FROM pheromones WHERE trail=? OR trail LIKE ?', 
                  (trail, trail + '.%'))
        rows = c.fetchall()
        
        if rows:
            found = True
            print(f"  {trail}:")
            for row in rows:
                p = dict(row)
                intensity = current_intensity(p)
                if intensity > 0.01:
                    print(f"    {p['ptype']}: {intensity:.2f}")
                    if p.get('payload'):
                        print(f"      {p['payload']}")
    
    if not found:
        print("  (field empty)")

def register(scent_id: str, trail: str, operator: str, value: float, action: str):
    """Register a scent condition."""
    sys.stderr.write(f"TRACE: register called with {scent_id}\n")
    sys.stderr.flush()
    conn = init_field()
    c = conn.cursor()
    now = time.time()
    
    c.execute('''INSERT OR REPLACE INTO scents (scent_id, trail, operator, value, action, registered_at, last_triggered)
        VALUES (?, ?, ?, ?, ?, ?, NULL)''',
        (scent_id, trail, operator, value, action, now))
    
    conn.commit()
    sys.stdout.write(f"REGISTERED: {scent_id}\n")
    sys.stdout.flush()
    return

def list_scents():
    """Show registered scents."""
    conn = init_field()
    c = conn.cursor()
    print("REGISTERED SCENTS:")
    
    c.execute('SELECT scent_id, trail, operator, value, action, last_triggered FROM scents')
    rows = c.fetchall()
    
    if rows:
        for row in rows:
            scent = dict(row)
            triggered = scent.get('last_triggered')
            triggered_str = time.strftime("%H:%M:%S", time.localtime(triggered)) if triggered else "never"
            print(f"  {scent['scent_id']}:")
            print(f"    trail: {scent['trail']}")
            print(f"    condition: {scent['operator']} {scent['value']}")
            print(f"    action: {scent['action']}")
            print(f"    last triggered: {triggered_str}")
    else:
        print("  (no scents registered)")

def check_triggers():
    """Check all scents and fire triggered actions."""
    conn = init_field()
    c = conn.cursor()
    now = time.time()
    fired = []
    
    c.execute('SELECT scent_id, trail, operator, value, action, last_triggered FROM scents')
    for scent_row in c.fetchall():
        scent = dict(scent_row)
        trail = scent['trail']
        operator = scent['operator']
        threshold = scent['value']
        action = scent['action']
        
        c.execute('SELECT initial_intensity, last_reinforced, decay_seconds FROM pheromones WHERE trail=? OR trail LIKE ?', 
                  (trail, trail + '.%'))
        max_intensity = 0
        for p_row in c.fetchall():
            p = dict(p_row)
            intensity = current_intensity(p)
            if intensity > max_intensity:
                max_intensity = intensity
        
        trigger = False
        if operator == ">=" and max_intensity >= threshold:
            trigger = True
        elif operator == ">" and max_intensity > threshold:
            trigger = True
        elif operator == "<=" and max_intensity <= threshold:
            trigger = True
        elif operator == "<" and max_intensity < threshold:
            trigger = True
        elif operator == "==" and max_intensity == threshold:
            trigger = True
        
        if trigger:
            last = scent.get('last_triggered') or 0
            if now - last > 60:
                c.execute('UPDATE scents SET last_triggered=? WHERE scent_id=?', (now, scent['scent_id']))
                fired.append((scent['scent_id'], action, max_intensity))
                print(f"TRIGGERED: {scent['scent_id']} (intensity={max_intensity:.2f})")
                print(f"  action: {action}")
    
    if fired:
        conn.commit()
    else:
        print("No triggers fired.")
    
    return fired

def arrive():
    """Register agent arrival in the field."""
    conn = init_field()
    c = conn.cursor()
    now = time.time()
    
    c.execute('''INSERT OR REPLACE INTO agents (agent_id, arrival, last_seen, status)
        VALUES (?, ?, ?, 'active')''',
        (AGENT_NAME, now, now))
    
    conn.commit()
    print(f"ARRIVED: {AGENT_NAME} at {time.strftime('%H:%M:%S')}")

def claim(trail: str):
    """Claim a trail for this agent."""
    conn = init_field()
    c = conn.cursor()
    now = time.time()
    
    c.execute('UPDATE agents SET claimed_trail=?, last_seen=? WHERE agent_id=?', 
              (trail, now, AGENT_NAME))
    
    if c.rowcount == 0:
        c.execute('''INSERT INTO agents (agent_id, arrival, last_seen, claimed_trail, status)
            VALUES (?, ?, ?, ?, 'active')''',
            (AGENT_NAME, now, now, trail))
    
    conn.commit()
    print(f"CLAIMED: {trail} by {AGENT_NAME}")

def depart():
    """Deregister this agent."""
    conn = init_field()
    c = conn.cursor()
    now = time.time()
    
    c.execute("UPDATE agents SET status='departed', last_seen=? WHERE agent_id=?", (now, AGENT_NAME))
    conn.commit()
    print(f"DEPARTED: {AGENT_NAME}")

def field_status():
    """Show full field status."""
    conn = init_field()
    c = conn.cursor()
    
    print("VAULT FIELD STATUS:")
    
    c.execute('SELECT COUNT(*) FROM pheromones')
    p_count = c.fetchone()[0]
    print(f"  pheromones: {p_count}")
    
    c.execute('SELECT COUNT(*) FROM scents')
    s_count = c.fetchone()[0]
    print(f"  scents: {s_count}")
    
    c.execute('SELECT COUNT(*) FROM agents WHERE status="active"')
    a_count = c.fetchone()[0]
    print(f"  active agents: {a_count}")
    
    c.execute('SELECT COUNT(*) FROM capabilities')
    cap_count = c.fetchone()[0]
    print(f"  capabilities: {cap_count}")
    
    c.execute("SELECT agent_id, arrival, claimed_trail, status FROM agents")
    for row in c.fetchall():
        agent = dict(row)
        arr = time.strftime("%H:%M:%S", time.localtime(agent['arrival']))
        print(f"    {agent['agent_id']}: arrived {arr}, claimed {agent.get('claimed_trail')}, status {agent['status']}")

def watch(interval=5):
    """Continuous monitoring mode."""
    print(f"Watching field (checking every {interval}s, Ctrl+C to stop)...")
    try:
        while True:
            print(f"\n[{time.strftime('%H:%M:%S')}] Checking...")
            check_triggers()
            status()
            time.sleep(interval)
    except KeyboardInterrupt:
        print("\nStopped.")

def check_capability(agent: str, capability: str, trail: str) -> bool:
    """Check if agent has capability for trail pattern."""
    conn = init_field()
    c = conn.cursor()
    
    c.execute("SELECT trail_pattern FROM capabilities WHERE agent_id=? AND capability=?",
             (agent, capability))
    for row in c.fetchall():
        pattern = row[0]
        if pattern == "*" or trail.startswith(pattern) or pattern == trail:
            return True
    return False

def grant(agent: str, capability: str, trail_pattern: str):
    """Grant capability to agent."""
    if capability not in CAPABILITIES:
        print(f"Invalid capability. Use: {', '.join(CAPABILITIES)}")
        return
    
    conn = init_field()
    c = conn.cursor()
    now = time.time()
    
    c.execute('''INSERT OR REPLACE INTO capabilities 
        (agent_id, capability, trail_pattern, granted_at, granted_by)
        VALUES (?, ?, ?, ?, ?)''',
        (agent, capability, trail_pattern, now, AGENT_NAME))
    
    conn.commit()
    print(f"GRANTED: {agent} {capability} on {trail_pattern}")

def revoke(agent: str, capability: str, trail_pattern: str):
    """Revoke capability from agent."""
    conn = init_field()
    c = conn.cursor()
    
    c.execute('''DELETE FROM capabilities 
        WHERE agent_id=? AND capability=? AND trail_pattern=?''',
        (agent, capability, trail_pattern))
    
    conn.commit()
    if c.rowcount > 0:
        print(f"REVOKED: {agent} {capability} on {trail_pattern}")
    else:
        print(f"NOT FOUND: {agent} {capability} on {trail_pattern}")

def list_perms(agent: str):
    """List agent capabilities."""
    conn = init_field()
    c = conn.cursor()
    
    print(f"CAPABILITIES: {agent}")
    c.execute('''SELECT capability, trail_pattern, granted_at FROM capabilities WHERE agent_id=?''', (agent,))
    rows = c.fetchall()
    
    if rows:
        for row in rows:
            print(f"  {row[0]}: {row[1]}")
    else:
        print("  (no capabilities)")

def list_trust():
    """Show trust relationships."""
    conn = init_field()
    c = conn.cursor()
    
    print("TRUST RELATIONSHIPS:")
    c.execute("SELECT trustee, trustor, trust_level, scope FROM trust")
    rows = c.fetchall()
    
    if rows:
        for row in rows:
            print(f"  {row[0]} -> {row[1]}: level {row[2]}, scope {row[3]}")
    else:
        print("  (no trust relationships)")

def show_pressure():
    """Show pheromones sorted by pressure score."""
    conn = init_field()
    c = conn.cursor()
    now = time.time()
    
    print("PRESSURE FIELD:")
    c.execute('SELECT trail, ptype, initial_intensity, last_reinforced, urgency, risk, confidence, decay_seconds FROM pheromones')
    rows = c.fetchall()
    
    scored = []
    for row in rows:
        p = dict(row)
        base = current_intensity(p)
        pressure = pressure_score(p)
        weighted = base * pressure
        trail, ptype = row[0], row[1]
        age = int(now - row[3])
        scored.append((trail, ptype, weighted, base, pressure, age))
    
    scored.sort(key=lambda x: x[2], reverse=True)
    for trail, ptype, weighted, base, pressure, age in scored:
        print(f"  {trail}/{ptype}: weighted={weighted:.2f} (base={base:.2f}, pressure={pressure:.1f}, {age}s old)")
    
    if not rows:
        print("  (no pheromones)")

def prune_stale():
    """Remove expired pheromones."""
    conn = init_field()
    c = conn.cursor()
    now = time.time()
    
    c.execute('SELECT id, trail, ptype, last_reinforced, decay_seconds FROM pheromones')
    rows = c.fetchall()
    
    removed = 0
    for row in rows:
        age = now - row[3]
        if age > row[4]:
            c.execute('DELETE FROM pheromones WHERE id=?', (row[0],))
            removed += 1
            print(f"PRUNED: {row[1]}/{row[2]} (expired)")
    
    if removed:
        conn.commit()
        print(f"Removed {removed} stale pheromones")
    else:
        print("No stale pheromones to remove")

def guard(action: str, trail: str):
    """Test guard: can agent perform action on trail?"""
    has_cap = check_capability(AGENT_NAME, action, trail)
    print(f"GUARD: {AGENT_NAME} {action} on {trail}: {'ALLOWED' if has_cap else 'DENIED'}")
    return has_cap

def arrival_snapshot():
    """Generate compact field briefing for new sessions."""
    conn = init_field()
    c = conn.cursor()
    now = time.time()
    
    print("=" * 50)
    print("VAULT FIELD BRIEFING")
    print("=" * 50)
    
    c.execute('SELECT COUNT(*) FROM pheromones')
    p_count = c.fetchone()[0]
    print(f"Active pheromones: {p_count}")
    
    c.execute('SELECT trail, ptype, initial_intensity, last_reinforced FROM pheromones ORDER BY last_reinforced DESC LIMIT 5')
    print("\nRecent activity:")
    for row in c.fetchall():
        age = int(now - row[3])
        print(f"  {row[0]}/{row[1]}: {row[2]:.2f} ({age}s ago)")
    
    c.execute('SELECT COUNT(*) FROM agents WHERE status="active"')
    a_count = c.fetchone()[0]
    print(f"\nActive agents: {a_count}")
    
    c.execute("SELECT agent_id, claimed_trail, last_seen FROM agents WHERE status='active'")
    for row in c.fetchall():
        print(f"  {row[0]}: claimed {row[1]}, last seen {int(now - row[2])}s ago")
    
    c.execute('SELECT COUNT(*) FROM capabilities')
    cap_count = c.fetchone()[0]
    print(f"\nCapability grants: {cap_count}")
    
    c.execute('SELECT COUNT(*) FROM scents')
    s_count = c.fetchone()[0]
    print(f"Registered scents: {s_count}")
    
    print("=" * 50)

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

    elif cmd == "register":
        if len(sys.argv) < 7:
            print("Usage: register <scent_id> <trail> <operator> <value> <action>")
            print("  operators: >=, >, <=, <, ==")
            sys.exit(1)
        scent_id = sys.argv[2]
        trail = sys.argv[3]
        operator = sys.argv[4]
        value = float(sys.argv[5])
        action = sys.argv[6]
        register(scent_id, trail, operator, value, action)

    elif cmd == "scents":
        list_scents()

    elif cmd == "check":
        check_triggers()

    elif cmd == "pressure":
        show_pressure()

    elif cmd == "prune":
        prune_stale()

    elif cmd == "arrive":
        arrive()

    elif cmd == "claim":
        if len(sys.argv) < 3:
            print("Usage: claim <trail>")
            sys.exit(1)
        claim(sys.argv[2])

    elif cmd == "depart":
        depart()

    elif cmd == "field":
        field_status()

    elif cmd == "watch":
        interval = int(sys.argv[2]) if len(sys.argv) > 2 else 5
        watch(interval)

    elif cmd == "grant":
        if len(sys.argv) < 5:
            print("Usage: grant <agent> <capability> <trail_pattern>")
            print(f"  capabilities: {', '.join(CAPABILITIES)}")
            sys.exit(1)
        grant(sys.argv[2], sys.argv[3], sys.argv[4])

    elif cmd == "revoke":
        if len(sys.argv) < 5:
            print("Usage: revoke <agent> <capability> <trail_pattern>")
            sys.exit(1)
        revoke(sys.argv[2], sys.argv[3], sys.argv[4])

    elif cmd == "perms":
        if len(sys.argv) < 3:
            print("Usage: perms <agent>")
            sys.exit(1)
        list_perms(sys.argv[2])

    elif cmd == "trust":
        list_trust()

    elif cmd == "guard":
        if len(sys.argv) < 4:
            print("Usage: guard <action> <trail>")
            print(f"  actions: {', '.join(CAPABILITIES)}")
            sys.exit(1)
        guard(sys.argv[2], sys.argv[3])

    elif cmd == "brief":
        arrival_snapshot()

    else:
        print(f"Unknown command: {cmd}")
        print(__doc__)
        sys.exit(1)

if __name__ == "__main__":
    main()