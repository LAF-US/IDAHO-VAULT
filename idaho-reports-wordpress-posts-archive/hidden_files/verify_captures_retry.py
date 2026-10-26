#!/usr/bin/env python3
"""Retry verification for URLs that errored in the first pass."""
import json
import time
import urllib.request
import urllib.parse

OUT_FILE = '/home/hatch/workspace/goals/idaho-reports-wordpress-posts-archive/hidden_files/wayback_verification.json'

with open(OUT_FILE) as f:
    results = json.load(f)

to_retry = [r for r in results if r['error']]
print(f"Retrying {len(to_retry)} errored URLs...")

for i, entry in enumerate(to_retry):
    url = entry['url']
    cdx_url = (
        'http://web.archive.org/cdx/search/cdx?url='
        + urllib.parse.quote(url, safe='')
        + '&output=json&filter=statuscode:200&limit=1'
    )
    try:
        req = urllib.request.Request(cdx_url, headers={'User-Agent': 'Mozilla/5.0 (WaybackVerification/1.0)'})
        with urllib.request.urlopen(req, timeout=45) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            if len(data) > 1:
                header = data[0]
                row = data[1]
                ts_idx = header.index('timestamp') if 'timestamp' in header else 1
                entry['has_capture'] = True
                entry['timestamp'] = row[ts_idx]
                entry['error'] = None
            else:
                # No error, genuinely no capture
                entry['error'] = None
    except Exception as e:
        entry['error'] = str(e)[:200]
    if (i + 1) % 20 == 0:
        print(f"  {i + 1}/{len(to_retry)} retried")
        with open(OUT_FILE, 'w') as f:
            json.dump(results, f, indent=1)
    time.sleep(2.5)  # longer delay on retry

with open(OUT_FILE, 'w') as f:
    json.dump(results, f, indent=1)

have = sum(1 for r in results if r['has_capture'])
missing = sum(1 for r in results if not r['has_capture'] and not r['error'])
errors = sum(1 for r in results if r['error'])
print(f"\nDone: {have} have captures, {missing} confirmed missing, {errors} still erroring")
