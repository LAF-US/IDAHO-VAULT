---
jupyter:
  jupytext:
    formats: ipynb,md
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.19.3
  kernelspec:
    display_name: Python 3 (ipykernel)
    language: python
    name: python3
---

# IR_CL_SCRAPER

Historical CourtListener scraper scaffold. This was an early first attempt from the
PyTutorial / CourtListener scraper repo handoff, built around parsing CourtListener HTML pages.

## Current Artifact Classification

This notebook is retained as provenance and as a Jupytext pairing test surface. It is not the
preferred implementation path for new CourtListener work.

Logan now has CourtListener API access. New work should prefer the official CourtListener REST API
or CourtListener MCP surface instead of scraping HTML. The API token must stay outside the repo:
resolve it at runtime from 1Password or an environment variable such as `COURTLISTENER_API_TOKEN`.

CourtListener's REST API v4.4 documentation recommends token authentication for programmatic API
access. The request header uses the `Token` authentication scheme, and authenticated use is also
the path that gives CourtListener enough information to monitor and support API behavior.

```python
# scraper/parser.py
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from datetime import datetime
import re
from scraper.fetch import fetch_entry_pages

def extract_entry_data(html, base_url):
    soup = BeautifulSoup(html, "html.parser")
    entry_div = soup.find("div", id=lambda x: x and x.startswith("entry-"))
    if not entry_div:
        return "N/A", "N/A"

    entry_text = entry_div.get_text(separator=" ", strip=True)
    date_match = re.search(r"[A-Z][a-z]{2}\.? \d{1,2}, \d{4}", entry_text)

    if date_match:
        raw_date = date_match.group(0).replace('.', '')
        try:
            parsed = datetime.strptime(raw_date, "%b %d, %Y")
            date = parsed.strftime("%b %d, %Y")
        except ValueError:
            date = raw_date
    else:
        date = "N/A"

    a_tag = entry_div.find("a", href=True)
    link = urljoin(base_url, a_tag["href"]) if a_tag else "N/A"

    return date, link

def parse_case_page(url, detail="", topic=""):
    base_url = "https://www.courtlistener.com"

    base_resp, first_resp, latest_resp = fetch_entry_pages(url)
    if not base_resp:
        return None  # Handle failure in main script

    soup = BeautifulSoup(base_resp.text, "html.parser")

    # ---- Case Title ----
    full_title = soup.title.string.strip() if soup.title else "N/A"
    title = re.split(r",\s*\d", full_title)[0]

    # ---- Court Name ----
    cou***REMOVED***h2 = soup.find("h2")
    court = cou***REMOVED***h2.get_text(strip=True) if cou***REMOVED***h2 else "N/A"

    orig_date, orig_link = (
        extract_entry_data(first_resp.text, base_url) if first_resp else ("N/A", "N/A")
    )
    latest_date, latest_link = (
        extract_entry_data(latest_resp.text, base_url) if latest_resp else ("N/A", "N/A")
    )

    return {
        "Case": f'<a href="{url}">{title}</a>',
        "Topic": topic,
        "Original": f'<a href="{orig_link}">{orig_date}</a>',
        "Latest":  f'<a href="{latest_link}">{latest_date}</a>',
        "Tag": detail,
    }

```

```python
# scraper/urls.py
import csv


def load_urls(filename="case_urls.csv"):
    with open(filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        return [row for row in reader]

```

```python
# scraper/pipeline.py
import csv
import os


def write_to_csv(new_rows, filename="output.csv"):
    if not new_rows:
        print("No data to write.")
        return

    fieldnames = ["Case", "Topic", "Original", "Latest", "Tag"]

    # Step 1: Load existing rows into a dict
    existing_data = {}
    if os.path.exists(filename):
        with open(filename, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                existing_data[row["Case"]] = row

    # Step 2: Update existing data only if the new value is not "N/A"
    for new_row in new_rows:
        case_key = new_row["Case"]
        old_row = existing_data.get(case_key, {})
        merged_row = {}

        for field in fieldnames:
            new_val = new_row.get(field, "N/A")
            old_val = old_row.get(field, "N/A")
            # Keep old if new is "N/A"
            merged_row[field] = new_val if new_val != "N/A" else old_val

        existing_data[case_key] = merged_row

    # Step 3: Write final rows
    with open(filename, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(existing_data.values())

    print(f"Saved {len(existing_data)} rows to {filename}")

```

```python
# main.py
import os
import csv
from scraper.urls import load_urls
from scraper.parser import parse_case_page
from scraper.pipeline import write_to_csv
from scraper.failures import log_failure
from scraper.commit import commit_and_push_outputs

def main():
    if os.path.exists("failed_urls.csv"):
        os.remove("failed_urls.csv")

    with open("failed_urls.csv", mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Topic", "URL", "Reason"])

    cases = load_urls()
    rows = []

    for case in cases:
        topic = case["topic"]
        url = case["url"]
        detail = case["detail"]

        row = parse_case_page(url, detail=detail, topic=topic)
        if row is None:
            reason = "Failed to fetch main case page"
            log_failure(topic, url, reason)
            print(f"Skipping {topic} ({url}) - {reason}")
            continue

        rows.append(row)

    write_to_csv(rows)
    commit_and_push_outputs()

if __name__ == "__main__":
    main()

```
