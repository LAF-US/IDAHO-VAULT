# Service Health Monitor Skill

This skill monitors external API health for services integrated with the vault.

## Monitored Services
- GitHub API (`https://api.github.com`)
- Linear API (`https://linear.app/api`)
- Slack Webhook (`https://hooks.slack.com`)
- OpenRouter API (`https://openrouter.ai/api/v1`)

## Usage
```bash
# Check GitHub API health
curl -s -o /dev/null -w "%{http_code}" https://api.github.com

# Check Linear API
curl -s -o /dev/null -w "%{http_code}" https://linear.app/api

# Full health report
python3 scripts/health_monitor.py
```

## Notes
- Run before initiating external integrations.
- Failed health checks should block automated workflows.
- Log results to `!/MONITORING/health-log.md`.
