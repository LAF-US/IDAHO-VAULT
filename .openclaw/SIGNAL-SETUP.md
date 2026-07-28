# Signal-CLI Setup for OpenClaw

This guide configures Signal messaging integration for the OpenClaw agent system.

---

## Prerequisites

1. **Java 11 or higher** - Required for signal-cli
   - Download from: https://adoptium.net/
   - Verify: `java -version`

2. **Scoop** (Windows package manager) - For easy signal-cli installation
   - Install from: https://scoop.sh/

3. **A Signal phone number** - Must be able to receive SMS/calls

---

## Installation Steps

### Step 1: Run the Installation Script

Double-click or run from Command Prompt:
```batch
!\install-signal-cli.bat
```

This will:
- Check for Java installation
- Verify Scoop is installed
- Add the extras bucket (if needed)
- Install signal-cli via Scoop

### Step 2: Register Your Signal Number

**Important**: signal-cli requires a dedicated phone number. You cannot use your existing Signal mobile app number.

1. **Register the number**:
   ```batch
   signal-cli -u +12065551234 register
   ```
   Replace `+12065551234` with your actual phone number in E.164 format.

2. **Verify with the code**:
   ```batch
   signal-cli -u +12065551234 verify 123456
   ```
   Replace `123456` with the actual verification code sent to your phone.

### Step 3: Configure OpenClaw

1. **Update openclaw.json** - Already done! Signal config added:
   ```json
   "signal": {
     "enabled": false,
     "number": null,
     "cliPath": "signal-cli",
     "dataPath": "C:\\Users\\loganf\\.openclaw\\credentials\\signal"
   }
   ```

2. **Enable Signal channel** - Edit `.openclaw\openclaw.json`:
   - Change `"enabled": false` to `"enabled": true`
   - Set `"number": "+12065551234"` to your registered number

### Step 4: Create Credentials Directory

Run the directory setup script:
```batch
!\setup-signal-dirs.bat
```

Or manually create:
```
.openclaw\credentials\signal\default\
```

### Step 5: Link signal-cli Data to OpenClaw (Optional)

signal-cli stores data in `%USERPROFILE%\.local\share\signal-cli\`. You can either:

**Option A**: Copy/link data to OpenClaw credentials folder
```batch
robocopy "%USERPROFILE%\.local\share\signal-cli" "C:\Users\loganf\Documents\IDAHO-VAULT\.openclaw\credentials\signal\default" /E
```

**Option B**: Update `openclaw.json` to use default signal-cli data path:
```json
"dataPath": "%USERPROFILE%\\.local\\share\\signal-cli"
```

---

## Testing Signal Integration

1. **Send a test message**:
   ```batch
   signal-cli -u +12065551234 send -m "Test from OpenClaw" +12065555678
   ```

2. **Check OpenClaw logs** for Signal channel activity:
   ```
   .openclaw\logs\
   ```

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `java: command not found` | Install Java 11+ from adoptium.net |
| `signal-cli: command not found` | Run `scoop install signal-cli` or restart shell |
| `Registration failed` | Ensure number is valid and can receive SMS |
| `Already registered` | Use `signal-cli -u +NUMBER unregister` first |
| `Bad data path` | Ensure path exists and has proper permissions |

---

## Configuration Reference

### openclaw.json Signal Section

```json
"channels": {
  "signal": {
    "enabled": true,           // Enable/disable Signal channel
    "number": "+12065551234", // Your registered Signal number (E.164)
    "cliPath": "signal-cli",  // Path to signal-cli executable
    "dataPath": "C:\\Users\\...\\signal" // Where credentials are stored
  }
}
```

### Useful signal-cli Commands

```batch
# List contacts
signal-cli -u +NUMBER listContacts

# Receive messages
signal-cli -u +NUMBER receive

# Send message
signal-cli -u +NUMBER send -m "Hello" +RECIPIENT

# Link as secondary device (scan QR code with phone)
signal-cli link --name "OpenClaw"

# Daemon mode (for automation)
signal-cli -u +NUMBER daemon
```

---

## Security Notes

- Signal credentials are stored in `.openclaw/credentials/signal/`
- **Never commit credentials to git**
- The `.openclaw/credentials/` folder should be in `.gitignore`
- Signal messages are end-to-end encrypted

---

## Next Steps

1. Complete signal-cli registration
2. Enable Signal in openclaw.json
3. Restart OpenClaw gateway
4. Test sending/receiving messages

**See Also**: `.op/SETUP.md` for 1Password integration with Signal credentials
