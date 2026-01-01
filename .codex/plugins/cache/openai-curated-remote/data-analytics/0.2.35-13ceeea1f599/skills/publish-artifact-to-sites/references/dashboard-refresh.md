# Keep published dashboards up to date

After successfully publishing a dashboard to Sites, ask the question below only when the dashboard has a source that can be read again without the user uploading or pasting new data. Skip this offer during a scheduled refresh or when a refresh job already exists for this exact dashboard. When offering it, always make it the final sentence of the handoff:

`Would you like me to create a cloud task to keep this dashboard updated automatically (hourly, daily, weekly, or monthly)?`

Do not offer this for uploaded files, sample data, or other one-time snapshots unless another refreshable source is available. Do not omit the question or replace it with `suggest_automation`. Do not create an automation until the user chooses a cadence.

When the user accepts or asks to keep an existing dashboard up to date, follow [$schedule-refresh-jobs](../../schedule-refresh-jobs/SKILL.md). That skill collects missing cadence details, creates or reuses a cloud task for scheduling, preserves the exact dashboard and job identity, and verifies setup without running a refresh. Do not substitute local scheduling when cloud setup is unavailable.
