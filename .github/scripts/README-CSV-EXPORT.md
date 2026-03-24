# CSV Export for Flourish Budget Tracker

## Overview

The Idaho Legislature scraper can export bill data to CSV format for use with Flourish data visualizations and budget tracking dashboards.

## Usage

### Manual CSV Export

To generate a CSV export manually:

```bash
python3 .github/scripts/idaho_leg_scraper.py --year 2026 --csv-export minidata.csv
```

This will:
1. Fetch the current bill listing from legislature.idaho.gov
2. Export all bills to the specified CSV file
3. Include metadata: bill ID, type, number, alias, title, sponsor, committee, last action, URL, year, and export timestamp

### Automated Daily Export

The CSV export runs automatically via GitHub Actions:

**Workflow:** `.github/workflows/budget-tracker-csv-export.yml`

**Schedule:** Daily at 6:30 AM MT (13:30 UTC) — 30 minutes after the main bill scraper

**Output:**
- CSV file named `minidata-YYYY-MM-DD.csv`
- Uploaded as GitHub Actions artifact (90-day retention)
- Emailed to configured recipient

### Required GitHub Secrets

For email delivery, configure these repository secrets:

| Secret | Description | Example |
|---|---|---|
| `MAIL_USERNAME` | SMTP username (Gmail address) | `reporter@idahoptv.org` |
| `MAIL_PASSWORD` | Gmail App Password | (16-character app password) |
| `MAIL_TO` | Recipient email address | `producer@idahoptv.org` |

**Setting up Gmail App Password:**
1. Go to https://myaccount.google.com/apppasswords
2. Select "Mail" and "Other (Custom name)"
3. Name it "GitHub Actions - Idaho Vault"
4. Copy the 16-character password
5. Add to GitHub repository secrets as `MAIL_PASSWORD`

## CSV Format

The exported CSV contains these columns:

| Column | Description |
|---|---|
| `bill_id` | Idaho Legislature bill identifier (e.g. H0001, S0042, HCR001) |
| `bill_type` | Bill type abbreviation (HB, SB, HCR, SCR, etc.) |
| `number` | Bill number without leading zeros |
| `alias` | Display name (e.g. "HB 1", "SB 42") |
| `title` | Bill title/short description |
| `sponsor` | Primary sponsor or sponsor list |
| `committee` | Assigned committee |
| `last_action` | Most recent legislative action |
| `url` | Link to bill page on legislature.idaho.gov |
| `year` | Session year |
| `exported_at` | Export timestamp (YYYY-MM-DD HH:MM UTC) |

## Flourish Integration

To import into Flourish:

1. Log into Flourish studio
2. Open your Budget Tracker visualization
3. Click "Data" tab
4. Select "Upload data"
5. Upload the `minidata-YYYY-MM-DD.csv` file
6. Map columns to visualization fields
7. Publish

## Manual Workflow Trigger

To generate a CSV on-demand:

1. Go to GitHub repository → Actions tab
2. Select "Budget Tracker CSV Export" workflow
3. Click "Run workflow"
4. (Optional) Specify a different session year
5. Click "Run workflow" button

The CSV will be:
- Generated within ~30 seconds
- Available as a downloadable artifact
- Emailed to the configured recipient

## Troubleshooting

**CSV export fails with "Could not fetch bill list":**
- The legislature.idaho.gov site may be down or blocking requests
- Check the workflow run logs for HTTP error details
- The scraper includes retry logic with exponential backoff
- If persistent, contact LSO for direct data access (see tracking issue)

**Email delivery fails:**
- Verify GitHub secrets are configured correctly
- Check that Gmail App Password is valid (not regular password)
- Ensure "Less secure app access" is NOT enabled (use App Password instead)
- Review workflow logs for SMTP error messages

**CSV file is empty or missing data:**
- Verify the session year is correct
- Check that bills exist for the specified year
- Review scraper logs for parsing errors

## Files

| File | Purpose |
|---|---|
| `.github/scripts/idaho_leg_scraper.py` | Scraper script with CSV export |
| `.github/workflows/budget-tracker-csv-export.yml` | Daily automation workflow |
| `.github/scripts/requirements-scraper.txt` | Python dependencies |

## Related

- Main bill scraper workflow: `.github/workflows/idaho-leg-scraper.yml`
- Scraper runs daily at 6:00 AM MT (13:00 UTC)
- CSV export runs 30 minutes later to ensure fresh data
