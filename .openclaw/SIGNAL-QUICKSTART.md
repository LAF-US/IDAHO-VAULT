# Quick Signal Configuration for OpenClaw

## What's Been Done

1. ✅ Updated `openclaw.json` with Signal channel configuration
2. ✅ Created installation script: `!\install-signal-cli.bat`
3. ✅ Created setup documentation: `.openclaw\SIGNAL-SETUP.md`
4. ✅ Created directory setup script: `!\setup-signal-dirs.bat`

## What You Need To Do

### 1. Install signal-cli

Run in Command Prompt or PowerShell:
```batch
scoop bucket add extras
scoop install signal-cli
```

Or run: `!\install-signal-cli.bat`

### 2. Register Your Phone Number

```batch
# Register
signal-cli -u +12065551234 register

# Verify with code received
signal-cli -u +12065551234 verify 123456
```

### 3. Enable Signal in OpenClaw

Edit `.openclaw\openclaw.json`:

```json
"channels": {
  "whatsapp": {
    "enabled": true
  },
  "signal": {
    "enabled": true,
    "number": "+12065551234",
    "cliPath": "signal-cli",
    "dataPath": "C:\\Users\\loganf\\.openclaw\\credentials\\signal"
  }
}
```

### 4. Create Credentials Directory

Run: `!\setup-signal-dirs.bat`

---

## Verification

Test signal-cli is working:
```batch
signal-cli --version
signal-cli -u +12065551234 listContacts
```

---

**Full documentation**: `.openclaw\SIGNAL-SETUP.md`
