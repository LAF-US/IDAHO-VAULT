---
title: "Coordination: SSH Tunnel Bridge — Windows → Mac"
date: 2026-05-23
status: complete
authority: LOGAN
doc_class: coordination_plan
related:
  - Hermes
  - OpenClaw
  - "PLAN-MANAGEMENT-KEY-TO-HERMES-2026-05-23"
  - "RECOVERY-HERMES-CONFIG-2026-05-23"
  - BEEFSTACK
---

## Topology (v2 — No Admin Required)

Windows machine (LOGAN-ZBFURY) can reach the Mac at `192.168.0.95`
over the LAN. Windows has OpenSSH client and an existing SSH key pair.

No OpenSSH server on Windows. No admin credentials available. No
Tailscale.

The simplest path: **Windows SSHes directly to the Mac** over the LAN.

```
Windows (LOGAN-ZBFURY, 192.168.0.121)
  → ssh logan@192.168.0.95
  → Mac (192.168.0.95, SSH server)
  → append key to ~/.hermes/.env
```

No tunnel, no reverse forward, no Windows SSH server. Just a direct
SSH connection from Windows to the Mac.

## Prerequisite

The Mac must have Remote Login (SSH) enabled. This is standard on
macOS — enable in System Settings → General → Sharing → Remote Login.

## Step 1 — Mac Agent: Authorize the Windows SSH Key

Windows has an existing SSH key pair. Add the public key below to
`~/.ssh/authorized_keys` on the Mac:

```
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIH9BphCewWNJ3x59PBbcb0kX6CxcBo75rqq+mnYMxn3s
```

This is the default Windows SSH key at
`~/.ssh/id_ed25519.pub` on LOGAN-ZBFURY.
Not in the repo.

## Step 2 — Mac Agent: Verify & Signal

```bash
# Test that key-based SSH works from Mac to itself:
ssh -o StrictHostKeyChecking=accept-new logan@192.168.0.95 "echo ssh_ok"
```

Should return `ssh_ok`. Then update this file's `status` to
`awaiting_windows_ssh`.

## Step 3 — Windows Agent: SSH & Push

Once the Mac signals `awaiting_windows_ssh`.

```powershell
$key = op read "op://Vault/OpenRouter Key/credential"
ssh logan@192.168.0.95 -o StrictHostKeyChecking=accept-new "echo 'OPENROUTER_MANAGEMENT_KEY=' >> ~/.hermes/.env"
```

Wait — the above echoes the key in transcript. Safer:

```powershell
$line = 'OPENROUTER_MANAGEMENT_KEY=' + (op read "op://Vault/OpenRouter Key/credential")
ssh logan@192.168.0.95 "echo '$line' >> ~/.hermes/.env"
```

### Step 3a — Verify

```powershell
ssh logan@192.168.0.95 "grep MANAGEMENT_KEY ~/.hermes/.env"
```

Should return: `OPENROUTER_MANAGEMENT_KEY=sk-or-v1-...`

## Step 4 — Windows Agent: Confirm Hermes Can Use It

```powershell
ssh logan@192.168.0.95 "source ~/.hermes/.env && curl -s -H 'Authorization: Bearer \$OPENROUTER_MANAGEMENT_KEY' https://openrouter.ai/api/v1/keys"
```

Should return a JSON array of runtime keys.

## Step 5 — Signal Completion

Update this file's `status` to `complete`.

---

## Rollback

1. On Mac: Remove the Windows public key from `~/.ssh/authorized_keys`
2. Update status to `rolled_back`

## Security Notes

- This exposes the Mac's SSH to the LAN. The Mac's SSH server is bound
  to all interfaces by default — consider limiting to specific IPs.
- The Windows public key is scoped to the vault project. If needed,
  revoke by removing from `~/.ssh/authorized_keys` on the Mac.
- Do not commit any private keys or passwords to the repo.
