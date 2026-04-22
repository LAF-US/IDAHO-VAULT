# Discord Channel Setup for OpenClaw

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

Edit `.openclaw\openclaw.json`:

```json
"discord": {
  "enabled": true,
  "token": "YOUR_BOT_TOKEN_HERE",
  "applicationId": "YOUR_APPLICATION_ID_HERE"
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
- Consider using 1Password CLI to inject the token:
  ```bash
  op item get "Discord Bot Token" --fields token
  ```
