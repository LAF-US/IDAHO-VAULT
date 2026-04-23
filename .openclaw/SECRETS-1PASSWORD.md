# 1Password Secrets Provider Setup for OpenClaw

This configures OpenClaw to use 1Password as a secrets provider for secure credential storage.

## Configuration Added

**`.openclaw\openclaw.json`** now includes:

```json
"secrets": {
  "providers": {
    "1password": {
      "enabled": false,
      "source": "exec",
      "command": "op",
      "args": ["item", "get", "--field", "password"],
      "env": {
        "OP_SERVICE_ACCOUNT_TOKEN": null
      }
    }
  },
  "defaultProvider": "1password"
}
```

## Setup Steps

### 1. Install 1Password CLI

```bash
scoop install 1password
op --version
```

### 2. Sign In to 1Password

**Option A: Interactive sign-in (for personal use)**
```bash
op account add --address my.1password.com --email your@email.com
op signin
```

**Option B: Service Account Token (for automation/GitHub Actions)**
```bash
# Create service account in 1Password web vault
# Export the token
export OP_SERVICE_ACCOUNT_TOKEN="ops_..."
```

### 3. Enable 1Password in OpenClaw

Edit `.openclaw\openclaw.json`:

```json
"secrets": {
  "providers": {
    "1password": {
      "enabled": true,
      "source": "exec",
      "command": "op",
      "args": ["item", "get", "--field", "password"],
      "env": {
        "OP_SERVICE_ACCOUNT_TOKEN": "${OP_SERVICE_ACCOUNT_TOKEN}"
      }
    }
  },
  "defaultProvider": "1password"
}
```

### 4. Store Channel Secrets in 1Password

Create items in your 1Password vault:

| Item Name | Type | Fields | Usage |
|-----------|------|--------|-------|
| `OpenClaw Discord Bot` | Password | `token`, `applicationId` | Discord bot credentials |
| `OpenClaw Signal Account` | Password | `number` | Signal phone number |
| `OpenClaw Telegram Bot` | Password | `token` | Telegram bot token |
| `OpenClaw Slack Bot` | Password | `bot_token`, `app_token` | Slack credentials |

### 5. Reference Secrets in OpenClaw

Instead of storing tokens in plaintext, use SecretRef:

**Before (plaintext):**
```json
"discord": {
  "enabled": true,
  "token": "MTAxMjM0NTY3ODkxMC4xMjM0NTY3ODkxMC4xMjM0NTY3ODkxMA..."
}
```

**After (1Password reference):**
```json
"discord": {
  "enabled": true,
  "token": {
    "$secretRef": {
      "provider": "1password",
      "id": "OpenClaw Discord Bot",
      "field": "token"
    }
  }
}
```

Or use CLI:
```bash
openclaw config set channels.discord.token --ref-provider 1password --ref-id "OpenClaw Discord Bot" --ref-field token
```

### 6. Test Configuration

```bash
# Verify 1Password is configured
openclaw secrets audit

# Reload secrets from 1Password
openclaw secrets reload
```

---

## Prerequisite Shell Setup

> [!IMPORTANT]
> **The `$secretRef` tags in `openclaw.json` are resolved at runtime.**
> The shell session that invokes `openclaw` MUST have the required environment
> variables exported BEFORE the command is run. The configuration is inert
> until the shell is seeded.

### Required Environment Variables

Before any `openclaw` command executes, the current shell must define:

| Variable | Purpose | Required For |
|----------|---------|--------------|
| `OP_SERVICE_ACCOUNT_TOKEN` | Authenticates the 1Password CLI provider | All `$secretRef` resolutions |
| `DISCORD_BOT_TOKEN` | Fallback Discord credential if 1Password is unreachable | Discord channel |
| `OPENCLAW_GATEWAY_TOKEN` | Authenticates the local gateway | Gateway startup |

### Golden Path: Export → Invoke

The execution sequence is explicit and non-negotiable:

**1. Export Secrets (seed the shell)**

PowerShell (Windows):
```powershell
$env:OP_SERVICE_ACCOUNT_TOKEN = "ops_..."
$env:DISCORD_BOT_TOKEN        = "MTAx..."
$env:OPENCLAW_GATEWAY_TOKEN   = "oc_gw_..."
```

Bash / Zsh (POSIX):
```bash
export OP_SERVICE_ACCOUNT_TOKEN="ops_..."
export DISCORD_BOT_TOKEN="MTAx..."
export OPENCLAW_GATEWAY_TOKEN="oc_gw_..."
```

cmd.exe (Windows legacy):
```cmd
set OP_SERVICE_ACCOUNT_TOKEN=ops_...
set DISCORD_BOT_TOKEN=MTAx...
set OPENCLAW_GATEWAY_TOKEN=oc_gw_...
```

**2. Verify the Shell is Seeded**

```bash
op whoami                         # confirms 1Password CLI is authenticated
echo $env:DISCORD_BOT_TOKEN       # PowerShell: confirms variable is set
echo $DISCORD_BOT_TOKEN           # Bash: confirms variable is set
```

**3. Run OpenClaw Command**

```bash
openclaw secrets audit
openclaw gateway start
openclaw run
```

### Why This Step is Mandatory

- `openclaw.json` contains `$secretRef` tags, not literal values.
- The 1Password provider is invoked as a subprocess (`op item get ...`) and
  inherits the parent shell's environment.
- If `OP_SERVICE_ACCOUNT_TOKEN` is absent, the provider fails authentication
  and every `$secretRef` resolution returns empty.
- If fallback variables (e.g. `DISCORD_BOT_TOKEN`) are absent, channels fail
  to initialize and the agent reports unreachable gateways.

### Automation: Seeding from a .env File

For repeatable sessions, source a local `.env` (never committed):

```bash
set -a
source .openclaw/.env.local
set +a
openclaw run
```

PowerShell equivalent:
```powershell
Get-Content .openclaw\.env.local | ForEach-Object {
  if ($_ -match '^\s*([^#=]+)=(.*)$') {
    [Environment]::SetEnvironmentVariable($Matches[1].Trim(), $Matches[2].Trim(), 'Process')
  }
}
openclaw run
```

### State Transition

This step is what moves the system from **configured** to **operational**:

| State | Meaning |
|-------|---------|
| Configured | `openclaw.json` contains valid `$secretRef` tags |
| **Operational** | Shell is seeded AND `openclaw` is invoked in that same shell |

Skipping the export step leaves the system configured but inert.

## Security Benefits

- ✅ **No plaintext tokens** in config files
- ✅ **Centralized secret management** in 1Password
- ✅ **Audit trail** of secret access
- ✅ **Automatic rotation** support via 1Password
- ✅ **Cross-machine sync** via 1Password cloud

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `op: command not found` | Run `scoop install 1password` |
| `authentication required` | Run `op signin` or set `OP_SERVICE_ACCOUNT_TOKEN` |
| `item not found` | Check exact item name in 1Password vault |
| `unauthorized` | Verify 1Password account has access to the vault |

## See Also

- `.op/SETUP.md` - Full 1Password CLI setup
- `SIGNAL-SETUP.md` - Signal channel setup
- `DISCORD-SETUP.md` - Discord channel setup
