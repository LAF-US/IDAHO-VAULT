# 1Password Local CLI Quick Start

## Status

1Password CLI is now **enabled** for local use with OpenClaw.

## Installation

Run the setup script:
```batch
!\setup-1password-cli.bat
```

Or manually:
```batch
scoop install 1password
```

## Quick Commands

### Sign In
```batch
op account add --address my.1password.com --email your@email.com
op signin
```

### Basic Usage
```batch
# List vaults
op vault list

# List items
op item list

# Get a password
op item get "Item Name" --field password

# Get a specific field
op item get "Discord Bot" --field token
```

## Using with OpenClaw

### Method 1: Direct CLI
Store your Discord token in 1Password, then use it:

```batch
# Get token from 1Password
set DISCORD_TOKEN=$(op item get "OpenClaw Discord Bot" --field token)

# Use with OpenClaw
openclaw config set channels.discord.token %DISCORD_TOKEN%
```

### Method 2: Secret References (Recommended)

Store credentials in 1Password with specific field names, then reference them in OpenClaw config.

**1Password Item: "OpenClaw Discord Bot"**
- Field: `token` = Your Discord bot token
- Field: `applicationId` = Your Discord app ID

**openclaw.json:**
```json
"discord": {
  "enabled": true,
  "token": {
    "$secretRef": {
      "provider": "1password",
      "id": "OpenClaw Discord Bot",
      "field": "token"
    }
  },
  "applicationId": {
    "$secretRef": {
      "provider": "1password", 
      "id": "OpenClaw Discord Bot",
      "field": "applicationId"
    }
  }
}
```

### Method 3: OpenClaw Secrets Commands

```batch
# Interactive setup
openclaw secrets configure

# Reload secrets from providers
openclaw secrets reload

# Audit secret references
openclaw secrets audit

# Check which secrets are resolved
openclaw secrets audit --json
```

## Store Channel Credentials

### Discord
```batch
# Create item in 1Password
op item create --category=login \
  --title="OpenClaw Discord Bot" \
  --vault="Private" \
  token="YOUR_DISCORD_BOT_TOKEN" \
  applicationId="YOUR_APPLICATION_ID"
```

### Signal
```batch
op item create --category=login \
  --title="OpenClaw Signal" \
  --vault="Private" \
  number="+12086279028"
```

### Telegram
```batch
op item create --category=login \
  --title="OpenClaw Telegram Bot" \
  --vault="Private" \
  token="YOUR_TELEGRAM_BOT_TOKEN"
```

## Environment Variables

Set these in your shell profile for convenience:

```batch
set OP_CONFIG_DIR=%USERPROFILE%\.op
```

For automation (service accounts):
```batch
set OP_SERVICE_ACCOUNT_TOKEN=ops_...
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `op: command not found` | Run `scoop install 1password` |
| `not currently signed in` | Run `op signin` |
| `item not found` | Check exact item name with `op item list` |
| Permission denied | Run terminal as Administrator |

## Next Steps

1. ✅ Install 1Password CLI: `!\setup-1password-cli.bat`
2. ⏳ Sign in: `op account add` then `op signin`
3. ⏳ Store Discord token in 1Password
4. ⏳ Enable Discord in OpenClaw
5. ⏳ Test: `openclaw secrets audit`

**Full guide**: `.openclaw\SECRETS-1PASSWORD.md`
