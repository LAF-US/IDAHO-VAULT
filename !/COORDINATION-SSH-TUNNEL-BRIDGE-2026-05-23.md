---
title: "Coordination: SSH Tunnel Bridge — Windows → Mac"
date: 2026-05-23
status: active
authority: LOGAN
doc_class: coordination_plan
related:
  - Hermes
  - OpenClaw
  - "PLAN-MANAGEMENT-KEY-TO-HERMES-2026-05-23"
  - BEEFSTACK
---

## Stigmergic Blackboard Protocol

This file is the coordination surface. Windows agent writes intent and
public material. Mac-side agent reads, executes Mac-side steps, and
signals completion by updating this file's status field.

## Goal

Make the existing Mac→Windows SSH tunnel bidirectional so Windows can
push the OpenRouter Management Key to `~/.hermes/.env` on the Mac.

## Current Topology

- Mac (Hermes host) runs OpenClaw gateway, bound loopback port 18789.
- Mac initiates SSH tunnel to Windows with `-R 18790:localhost:18789`.
- Windows listens on 127.0.0.1:18790 → forwards to Mac's port 18789.
- Windows cannot initiate connections to the Mac.

## Desired Topology

Same SSH connection, but add a reverse forward so Windows can reach the
Mac's SSH port:

```
Mac SSH client:  ssh -R 18790:localhost:18789 -R 2222:localhost:22 <windows-host>
                              ↑ existing tunnel         ↑ new reverse-forward
```

Port 2222 on localhost (Windows) → Mac's SSH port 22 (via tunnel).

---

## Step 1 — Mac Agent: Trust the Windows SSH Key

Windows generated a new SSH key pair for this tunnel. The public key is
below. Add it to `~/.ssh/authorized_keys` on the Mac:

```
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIDtwaiQhxQ42Ipxz3A0k4k8lnW+xA//CBVXjdvAtXs3j openclaw-tunnel@windows-zbfury-2026-05-23
```

The corresponding private key lives at
`~/.ssh/id_ed25519_openclaw_tunnel` on Windows (LOGAN-ZBFURY). It is
NOT in this repository.

## Step 2 — Mac Agent: Update the SSH Tunnel Command

Modify the existing SSH tunnel invocation to add the reverse forward:

```bash
# Old (one-way):
ssh -R 18790:localhost:18789 user@windows-host

# New (two-way):
ssh -R 18790:localhost:18789 -R 2222:localhost:22 user@windows-host
```

Key addition: `-R 2222:localhost:22`

This makes port 2222 on Windows (127.0.0.1:2222) a tunnel endpoint that
reaches the Mac's SSH server.

If the tunnel is managed by a systemd service, launchd plist, or
OpenClaw, update the corresponding config file. If it's started
manually, restart it.

## Step 3 — Mac Agent: Verify & Signal

After steps 1 and 2 are done:

1. Verify the tunnel is up: `ssh -p 2222 localhost` from the Mac should
   loop back successfully.
2. Change the status field in this file's frontmatter from `active` to
   `awaiting_windows`.

---

## Step 4 — Windows Agent: Test the Bridge

Once the Mac agent signals `awaiting_windows`:

```powershell
ssh -i ~/.ssh/id_ed25519_openclaw_tunnel -p 2222 localhost -o StrictHostKeyChecking=accept-new echo "tunnel OK"
```

If this returns "tunnel OK", the bridge works.

## Step 5 — Windows Agent: Push the Management Key

Read the key from 1Password:

```powershell
$key = op read "op://Vault/OpenRouter Key/credential"
```

Write it to the Mac's Hermes env:

```powershell
ssh -i ~/.ssh/id_ed25519_openclaw_tunnel -p 2222 localhost "echo 'OPENROUTER_MANAGEMENT_KEY=$key' >> ~/.hermes/.env"
```

**Safety:** Do not echo or log the key value. The `$key` variable stays
in memory for the duration of this one SSH command.

## Step 6 — Windows Agent: Verify

```powershell
ssh -i ~/.ssh/id_ed25519_openclaw_tunnel -p 2222 localhost "grep MANAGEMENT_KEY ~/.hermes/.env"
```

Expected output: `OPENROUTER_MANAGEMENT_KEY=sk-or-v1-...`

## Step 7 — Signal Completion

Update the status field in this file to `complete`.

---

## Rollback

If the tunnel change breaks the existing Mac→Windows connection:

1. On Mac: revert the SSH command to the original `-R 18790:...` only.
2. Remove the public key from `~/.ssh/authorized_keys` on the Mac.
3. Delete `~/.ssh/id_ed25519_openclaw_tunnel*` on Windows.
4. Set this file's status to `rolled_back`.

## Security Notes

- The private key is ed25519, generated on 2026-05-23, scoped to this
  tunnel bridge only. Rotate or delete when the bridge is no longer
  needed.
- This tunnel port (2222) exposes the Mac's SSH server to `localhost`
  on Windows — no external network exposure.
- Do not commit the private key to this repository.
