# OAuth Flow Configurator Skill

This skill handles OAuth flows for external services requiring user authorization.

## Supported Providers
- Google (Gmail, Calendar, Drive)
- GitHub (for CLI authentication)
- Slack (workspace apps)

## Process
1. Initiate OAuth flow via provider URL.
2. User authorizes and receives authorization code.
3. Exchange code for access/refresh tokens.
4. Store tokens securely in 1Password.

## Usage
```bash
# Example: GitHub CLI OAuth
gh auth login --web

# Example: Store token in 1Password
op create item login github-token --vault "Private" --fields "password=$TOKEN"
```

## Notes
- Never store OAuth tokens in plain text.
- Refresh tokens when access tokens expire.
- Use 1Password CLI for all token management.
