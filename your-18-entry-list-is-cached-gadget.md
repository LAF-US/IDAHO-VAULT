# Reorientation — the stack is one recursive system, not disparate balls

## Context

Logan's correction, twice: *"too many disparate balls in the air"* → and when I
mis-sorted them into active/parked buckets → *"these tools all feed into each
other recursively — Tailscale for OpenClaw, OpenClaw for VisionClaw and Obsidian,
Obsidian for Hermes and OpenClaw, etc."*

The error was the frame. These are **not separate projects to triage** — they are
**one layered dependency stack with a feedback loop.** "Parked" was the wrong
word for most of it; the right word is **"waiting on its upstream layer."** The
significance of tonight: **the foundation layer (Tailscale → OpenClaw serve) just
closed**, and completing a foundation *cascades* — it unblocks everything sitting
on top of it. The task list must express that build order, not a flat to-do.

## The dependency stack (what carries what)

```
        ┌─────────────────────────────────────────────────────────┐
  L0    │ Tailscale (OSS daemon, serve, logans-mbp)   ✅ DONE tonight │  foundation: reachability + wss:// TLS
        └───────────────────────────┬─────────────────────────────┘
                                    ▼
  L1    ┌─────────────────────────────────────────────────────────┐
        │ OpenClaw gateway (bind=loopback + tailscale.mode=serve)  │  ✅ DONE — the hub
        └───┬───────────────────────────────────────────────┬─────┘
            ▼                                                 ▼
  L2   VisionClaw / Pixel (Task IV)                      Obsidian  ◀─┐
       needs OpenClaw serve wss:// + token               ├ obsidianclaw (→ OpenClaw)  │ feedback:
       ⇒ UNBLOCKED now                                   ├ mcp-tools (→ Hermes)       │ Obsidian
                                                          └ obsidian-CLI (→ OpenClaw ─┘ skill)
                                    │
                                    ▼
  L3    ┌─────────────────────────────────────────────────────────┐
        │ Hermes (channels, routing) ── mcp-tools stdio wiring     │  waits on Obsidian mcp-tools
        └───────────────────────────┬─────────────────────────────┘
                                    ▼
  L4    BEEFSTACK (Hermes capability router)  ── waits on Hermes + Logan's design calls
```

**Cross-cutting spine** (threads through every layer — the "ballet"):
- `gateway.auth.token` — one value, consumed by VisionClaw, obsidianclaw, Android app; also the last doctor security warning. Migrating it to a SecretRef touches all consumers at once.
- **hostname `logans-mbp`** — every tailnet client (VisionClaw, Android, any Obsidian-over-tailnet) resolves it; the old `logans-macbook-pro-1` refs are now stale everywhere.
- **1Password / secrets** — underlies Hermes (`.env` from `op`) *and* OpenClaw (resolver) *and* the token handling.

## Where we are in the stack

**L0–L1 CLOSED tonight** (records still say otherwise — must fix): Tailscale OSS
daemon, file-based root-owned state, **0 keychain items**, serve verified (HTTP
200, valid TLS, `serve status` shows config). OpenClaw on loopback+serve. Secret
leak fully resolved (scrubbed/verified/rotated). This is the cascade point.

**L2 is the live front** (its upstream just cleared):
- **VisionClaw / Pixel pairing (IV)** — unblocked; pair against `wss://logans-mbp…`.
- **obsidianclaw (VI)** — `data.json` empty again; needs URL + token + connect.
  Decision: loopback `http://127.0.0.1:18789` (works now) vs enable MagicDNS
  Mac-side so the tailnet name resolves (one `/etc/resolver` file).
- **Foundation closeout** feeding L2: sync hostname → `logans-mbp` in `Secrets.kt`
  + witnesses; delete stale console nodes; (optional) prove serve survives a
  daemon restart.

**L2→L3 feedback** (the recursion Logan named): once Obsidian's mcp-tools is
installed, wire its stdio server into `~/.hermes/config.yaml` (Hermes ← Obsidian);
and the official `obsidian` CLI becomes an OpenClaw skill (OpenClaw ← Obsidian).
Both need the L2 Obsidian layer stable first — which needs the Obsidian
substrate healthy (Templater misfire #714, sync-conflict blocker for tiered
capture).

**L3–L4 downstream:** Hermes is stable (1Password local pattern; WhatsApp gated
on Baileys patch); BEEFSTACK is the top of the stack, waiting on Hermes + Logan's
router-design decisions (#690). Genuinely async/external-gated (not "parked
out"): upstream drafts ×3 (per-draft filing gate), Book-of-Claudius/#725
(doctrine triage), dotdir reconciler (resume "in a few days").

## Execution (after approval)

1. **Fix the record** — session anchor entries: Tailscale OSS switch COMPLETE
   (serve works, `logans-mbp`, file-based) *superseding* the stale tailnet-bind
   entry; secret-leak RESOLVED (scrubbed/verified/rotated).
2. **Rebuild the task list to mirror the stack** — replace #1–14 (all BEEFSTACK)
   with dependency-ordered tasks, each tagged by layer:
   - `[L2·now]` sync hostname → logans-mbp (Secrets.kt host + witnesses)
   - `[L2·now]` obsidianclaw: decide URL, seed config, verify connect
   - `[L2·now]` Task IV — pair Pixel/VisionClaw against serve endpoint
   - `[L1·closeout]` stale console-node cleanup + serve-restart persistence proof
   - `[spine]` gateway.auth.token → SecretRef
   - `[L2→L3]` obsidian substrate health (Templater #714, sync conflicts) → then mcp-tools↔Hermes stdio wiring, obsidian-CLI OpenClaw skill
   - `[L4]` BEEFSTACK — waits on Hermes + Logan's design decisions (#690)
   - `[async]` upstream drafts (filing gate) · Book-of-Claudius #725 · WhatsApp/Baileys · dotdir reconciler
3. **Recommended immediate cascade step:** the L2 hostname sync (non-sudo, wraps
   L0 and feeds every L2 client).

## Open decisions for Logan
- obsidianclaw URL: loopback vs enable-MagicDNS Mac-side.
- After the record+task fix: drive the L2 front now, or stop for the night.

## Verification
- Anchor reflects live state; `openclaw status` + `tailscale serve status` corroborate L0–L1.
- Task list: 14 BEEFSTACK → dependency-ordered set, each tagged by stack layer, BEEFSTACK correctly at L4 (top), not the front.
- Hostname sync: `grep -rn logans-macbook-pro` across the named files returns only the historical `UPSTREAM-DRAFTS` file.
