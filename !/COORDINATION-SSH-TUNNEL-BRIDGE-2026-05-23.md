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
  - "RECOVERY-HERMES-CONFIG-2026-05-23"
  - BEEFSTACK
---

## Topology (Corrected)

The Mac and Windows machines are NOT connected by a persistent SSH
tunnel. The only live connection is OpenClaw node pairing over
WebSocket (Mac gateway → Windows node).

A raw SSH tunnel existed historically (circa May 17) via
`ssh -R 18790:localhost:18789` from Mac to Windows, but is
currently down. The relevant SSH config and host key are no longer
present on the Mac.

## Goal

Re-establish a bidirectional SSH tunnel so Windows can push the
OpenRouter Management Key to `~/.hermes/.env` on the Mac.

The tunnel flow will be:

```
Mac SSH client → ssh -R 2222:localhost:22 LOGAN-ZBFURY (192.168.0.121)
                  ↑                              ↑
            reverse-forward                  Windows SSH server
            port 2222 binds                   (needs install)
            on Windows localhost

Then from Windows:
  ssh -i ~/.ssh/id_ed25519_openclaw_tunnel -p 2222 localhost
  → reaches Mac SSH server through the tunnel
  → push the Management Key
```

## Prerequisites — Windows Side

### Step W1 — Install OpenSSH Server

Requires elevation. Run in PowerShell as Administrator:

```powershell
Add-WindowsCapability -Online -Name OpenSSH.Server~~~~0.0.1.0
Start-Service sshd
Set-Service sshd -StartupType 'Automatic'
New-NetFirewallRule -DisplayName 'OpenSSH Server' -Direction Inbound -Protocol TCP -LocalPort 22 -Action Allow
```

Verify:
```powershell
Get-Service sshd | Select-Object Name, Status, StartType
# Should show: sshd, Running, Automatic
```

### Step W2 — Enable SSH Key Auth

Ensure `C:\ProgramData\ssh\sshd_config` has:
```
PubkeyAuthentication yes
PasswordAuthentication yes  (or no, your call)
```

### Step W3 — Signal Ready

Update this file's `status` field from `active` to `awaiting_ssh_server`.

---

## Step 1 — Mac Agent: Establish SSH Tunnel

Once Windows signals `awaiting_ssh_server`:

```bash
ssh logan@192.168.0.121 -R 2222:localhost:22
```

- `logan` is the Windows username
- `192.168.0.121` is the Windows LAN IP
- `-R 2222:localhost:22` makes port 2222 on Windows → Mac's SSH port 22
- First connection will prompt for the Windows password and host key confirmation

If the tunnel breaks later, reconnect with the same command.

### Step 1a — Persist the Tunnel (Optional)

Add to `~/.ssh/config` on Mac:
```
Host logan-zbfury
    HostName 192.168.0.121
    User logan
    RemoteForward 2222 localhost:22
```

Then reconnect with: `ssh logan-zbfury`

## Step 2 — Mac Agent: Authorize the Windows SSH Key

Windows generated a key pair for this bridge. The public key is below.
Add it to `~/.ssh/authorized_keys` on the Mac:

```
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIDtwaiQhxQ42Ipxz3A0k4k8lnW+xA//CBVXjdvAtXs3j openclaw-tunnel@windows-zbfury-2026-05-23
```

The private key stays on Windows at
`~/.ssh/id_ed25519_openclaw_tunnel`. Not in the repo.

## Step 3 — Mac Agent: Verify & Signal

```bash
ssh -p 2222 localhost "echo tunnel_active"
```

Should return `tunnel_active`. Then update this file's `status` to
`awaiting_windows`.

---

## Step 4 — Windows Agent: Push the Management Key

Once the Mac signals `awaiting_windows`:

```powershell
ssh -i ~/.ssh/id_ed25519_openclaw_tunnel -p 2222 localhost -o StrictHostKeyChecking=accept-new "cat >> ~/.hermes/.env" < echo "OPENROUTER_MANAGEMENT_KEY=$(op read "op://Vault/OpenRouter Key/credential")"
```

**Safety:** This does not echo the key. The value is piped directly
into the remote `cat` command.

### Step 4a — Verify

```powershell
ssh -i ~/.ssh/id_ed25519_openclaw_tunnel -p 2222 localhost "grep MANAGEMENT_KEY ~/.hermes/.env"
```

Should return `OPENROUTER_MANAGEMENT_KEY=sk-or-v1-...`

## Step 5 — Signal Completion

Update this file's `status` to `complete`.

---

## Rollback

If the tunnel breaks Windows SSH:

1. On Windows: `Stop-Service sshd; Set-Service sshd -StartupType Disabled`
2. Remove the firewall rule
3. On Mac: Remove the Windows SSH key from `~/.ssh/authorized_keys`
4. Set status to `rolled_back`

## Security Notes

- Port 22 exposed on Windows LAN (192.168.0.0/24). The firewall rule can
  be narrowed to the Mac's IP if known.
- The tunnel port (2222) only binds to Windows localhost — no external
  exposure.
- The OpenSSH server only needs to run during the bridge operation; can
  be stopped and disabled afterward.
- Do not commit any private keys or passwords to the repo.
