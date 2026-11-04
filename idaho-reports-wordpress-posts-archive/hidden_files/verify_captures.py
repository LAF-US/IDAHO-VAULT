#!/usr/bin/env python3
"""Verify Wayback Machine captures for Logan's 263 bylined posts."""
import json
import time
import urllib.request
import urllib.parse

POSTS_FILE = '/home/hatch/workspace/goals/idaho-reports-wordpress-posts-archive/hidden_files/logan_bylined_posts.json'
OUT_FILE = '/home/hatch/workspace/goals/idaho-reports-wordpress-posts-archive/hidden_files/wayback_verification.json'

with open(POSTS_FILE) as f:
    posts = json.load(f)

urls = [p['link'] for p in posts]
print(f"Checking {len(urls)} URLs...")

results = []
for i, url in enumerate(urls):
    cdx_url = (
        'http://web.archive.org/cdx/search/cdx?url='
        + urllib.parse.quote(url, safe='')
        + '&output=json&filter=statuscode:200&limit=1'
    )
    entry = {'url': url, 'has_capture': False, 'timestamp': None, 'error': None}
    try:
        req = urllib.request.Request(cdx_url, headers={'User-Agent': 'Mozilla/5.0 (WaybackVerification/1.0)'})
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            # data[0] is header row, data[1] is first capture
            if len(data) > 1:
                # Find timestamp field index from header
                header = data[0]
                row = data[1]
                ts_idx = header.index('timestamp') if 'timestamp' in header else 1
                entry['has_capture'] = True
                entry['timestamp'] = row[ts_idx]
    except Exception as e:
        entry['error'] = str(e)[:200]
    results.append(entry)
    if (i + 1) % 25 == 0:
        print(f"  {i + 1}/{len(urls)} checked")
        # Save progress incrementally
        with open(OUT_FILE, 'w') as f:
            json.dump(results, f, indent=1)
    time.sleep(1.5)  # be respectful of the API

with open(OUT_FILE, 'w') as f:
    json.dump(results, f, indent=1)

have = sum(1 for r in results if r['has_capture'])
missing = sum(1 for r in results if not r['has_capture'] and not r['error'])
errors = sum(1 for r in results if r['error'])
print(f"\nDone: {have} have captures, {missing} missing, {errors} errors")
