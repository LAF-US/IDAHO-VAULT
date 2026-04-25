# OpenClaw 1Password Token Setup

## Problem

OpenClaw's Discord channel requires `DISCORD_OPENCLAW_TOKEN` env var, but the token lives in 1Password.

## Solution

When 1Password is **unlocked** (desktop app open + unlocked), run:

```powershell
# In PowerShell
$token = op item get "Discord OpenClaw" --field credential
$env:DISCORD_OPENCLAW_TOKEN = $token
[System.Environment]::SetEnvironmentVariable("DISCORD_OPENCLAW_TOKEN", $token, "User")
```

Then start OpenClaw - it will have Discord enabled automatically.

## Current Status

- Item "Discord OpenClaw" exists in 1Password ✓
- Field: `credential` (API Key type)
- Config: `channels.discord.token = "env:DISCORD_OPENCLAW_TOKEN"` ✓

## To Run

```powershell
# Set token permanently (run once when 1Password is unlocked)
$token = op item get "Discord OpenClaw" --field credential
[System.Environment]::SetEnvironmentVariable("DISCORD_OPENCLAW_TOKEN", $token, "User")

# Then OpenClaw works
openclaw gateway
```