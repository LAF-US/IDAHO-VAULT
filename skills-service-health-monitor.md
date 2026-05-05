# Service Health Monitor Reference

This note maps service-health guidance to the live monitoring script.

## Monitored Services
- GitHub API (`https://api.github.com`)
- Linear API (`https://linear.app/api`)
- Slack Webhook (`https://hooks.slack.com`)
- OpenRouter API (`https://openrouter.ai/api/v1`)

## Usage
```bash
python3 scripts/health_monitor.py
python3 scripts/health_monitor.py --write-log
```

## Notes
- Run before initiating external integrations.
- Failed health checks should block automated workflows.
- `scripts/health_monitor.py` writes canonical snapshots to
  `!/MONITORING/health-log.md`.
- Treat this file as a reference note. The live check surface is the Python
  script.
