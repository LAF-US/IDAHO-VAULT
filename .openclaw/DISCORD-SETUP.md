# Discord Channel Setup for OpenClaw

> [!IMPORTANT]
> Hermes and OpenClaw channel assignments must be confirmed against their live
> runtimes before enabling or disabling either Discord channel. Do not persist
> resolved Discord credentials in user- or machine-scoped environment variables.

## Configuration Added

Discord has been added to `openclaw.json`:

```json
"discord": {
  "enabled": false,
  "token": null,
  "applicationId": null
}
```

## Setup Instructions

### 1. Create a Discord Bot

1. Go to https://discord.com/developers/applications
2. Click **"New Application"**
3. Give it a name (e.g., "OpenClaw Bot")
4. Go to **Bot** section → Click **"Add Bot"**
5. Copy the **Token** (keep this secret!)

### 2. Get Application ID

1. In the Discord Developer Portal, go to **General Information**
2. Copy the **Application ID**

### 3. Configure OpenClaw

Use a 1Password SecretRef in the local OpenClaw configuration:

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

### 4. Invite Bot to Server

1. In Developer Portal → OAuth2 → URL Generator
2. Select scopes: `bot`, `applications.commands`
3. Select bot permissions:
   - Read Messages/View Channels
   - Send Messages
   - Read Message History
   - Add Reactions
4. Copy the generated URL and open it in browser
5. Select your server and authorize

### 5. Enable Channel

```bash
openclaw channels login --channel discord
```

## Usage

The bot will respond to DMs and mentions in servers where it's invited.

## Security Notes

- Store your Discord token securely
- Use the SecretRef configuration above rather than placing a literal token in
  a tracked or user-persistent configuration surface.
- The tracked reference config currently uses an environment reference to avoid
  changing a possibly live channel before audit. For a process-scoped session:
  ```powershell
  $env:DISCORD_OPENCLAW_TOKEN = op item get "Discord OpenClaw" --field credential --reveal
  openclaw gateway
  Remove-Item Env:DISCORD_OPENCLAW_TOKEN -ErrorAction SilentlyContinue
  ```
