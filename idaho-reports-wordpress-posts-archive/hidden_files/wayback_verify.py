#!/usr/bin/env python3
"""Verify Wayback Machine captures for Logan's 263 bylined posts.

Reads logan_bylined_posts.json, checks each URL against the Wayback CDX API,
writes results to wayback_verification.json. Resumable: skips URLs already
verified.
"""
import json
import os
import time
import urllib.parse
import urllib.request

BASE = '/home/hatch/workspace/goals/idaho-reports-wordpress-posts-archive/hidden_files'
POSTS_FILE = os.path.join(BASE, 'logan_bylined_posts.json')
OUT_FILE = os.path.join(BASE, 'wayback_verification.json')
LOG_FILE = os.path.join(BASE, 'wayback_verify_log.txt')

DELAY = 2  # seconds between requests


def log(msg):
    line = f"{time.strftime('%Y-%m-%d %H:%M:%S')}  {msg}"
    print(line, flush=True)
    with open(LOG_FILE, 'a') as f:
        f.write(line + '\n')


def check_url(url, retries=3):
    def cdx(params):
        api = ('http://web.archive.org/cdx/search/cdx?url='
               + urllib.parse.quote(url, safe='') + params)
        req = urllib.request.Request(api, headers={'User-Agent': 'Mozilla/5.0 (compatible; archive-verification)'})
        with urllib.request.urlopen(req, timeout=60) as resp:
            return json.loads(resp.read().decode('utf-8', errors='replace'))

    last_err = None
    for attempt in range(retries):
        try:
            # Any 200-status capture
            data = cdx('&output=json&filter=statuscode:200&limit=1')
            has_capture = isinstance(data, list) and len(data) > 1
            ts = data[1][1] if has_capture else None
            # Capture from our save pass window (Oct 8-9, 2026)
            recent = cdx('&output=json&filter=statuscode:200&from=20261008&to=20261010&limit=1')
            has_recent = isinstance(recent, list) and len(recent) > 1
            recent_ts = recent[1][1] if has_recent else None
            return {'url': url, 'has_capture': has_capture, 'timestamp': ts,
                    'save_pass_capture': has_recent, 'save_pass_timestamp': recent_ts,
                    'error': None}
        except Exception as e:
            last_err = str(e)
            time.sleep(5)
    return {'url': url, 'has_capture': False, 'timestamp': None,
            'save_pass_capture': False, 'save_pass_timestamp': None, 'error': last_err}


def main():
    with open(POSTS_FILE) as f:
        posts = json.load(f)
    urls = [p['link'] for p in posts]
    log(f"Total URLs: {len(urls)}")

    results = []
    if os.path.exists(OUT_FILE):
        with open(OUT_FILE) as f:
            results = json.load(f)
        log(f"Resuming: {len(results)} already verified")

    done_urls = {r['url'] for r in results}
    for i, url in enumerate(urls):
        if url in done_urls:
            continue
        r = check_url(url)
        results.append(r)
        if r['error']:
            status = 'ERROR'
        elif r['save_pass_capture']:
            status = 'NEWCAP'
        elif r['has_capture']:
            status = 'OLDCAP'
        else:
            status = 'NONE'
        log(f"[{len(results)}/{len(urls)}] {status} {url}")
        with open(OUT_FILE, 'w') as f:
            json.dump(results, f, indent=1)
        time.sleep(DELAY)

    yes = sum(1 for r in results if r['has_capture'])
    new = sum(1 for r in results if r.get('save_pass_capture'))
    no = sum(1 for r in results if not r['has_capture'] and not r['error'])
    err = sum(1 for r in results if r['error'])
    log(f"DONE: {yes} with any capture ({new} from Oct 8-9 save pass), {no} missing, {err} errors")


if __name__ == '__main__':
    main()
