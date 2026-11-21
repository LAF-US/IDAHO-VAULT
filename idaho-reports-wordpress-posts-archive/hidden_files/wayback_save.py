#!/usr/bin/env python3
"""
Save Idaho Reports WordPress posts to Wayback Machine via Save Page Now.
Runs through post_list.json, saves each URL, logs results.
Rate-limited to 65 seconds between saves per IA guidelines.
"""
import json, time, urllib.request, urllib.parse, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
POST_LIST = os.path.join(HERE, 'post_list.json')
PROGRESS = os.path.join(HERE, 'wayback_progress.json')
LOG = os.path.join(HERE, 'wayback_log.txt')

SAVE_URL = 'https://web.archive.org/save/'

def log(msg):
    line = f'{time.strftime("%Y-%m-%d %H:%M:%S")} {msg}'
    print(line, flush=True)
    with open(LOG, 'a') as f:
        f.write(line + '\n')

def load_progress():
    if os.path.exists(PROGRESS):
        with open(PROGRESS) as f:
            return json.load(f)
    return {'done': [], 'failed': []}

def save_progress(prog):
    with open(PROGRESS, 'w') as f:
        json.dump(prog, f, indent=1)

def save_to_wayback(url):
    """Submit URL to Save Page Now. Returns True on success."""
    try:
        data = urllib.parse.urlencode({'url': url}).encode()
        req = urllib.request.Request(SAVE_URL, data=data, method='POST')
        req.add_header('User-Agent', 'IdahoReportsArchive/1.0 (preservation; contact: loganfinney)')
        with urllib.request.urlopen(req, timeout=120) as r:
            # Save Page Now returns 200 on accept
            return r.status in (200, 201, 202)
    except Exception as e:
        log(f'  ERROR: {e}')
        return False

def main():
    with open(POST_LIST) as f:
        posts = json.load(f)
    prog = load_progress()
    done_ids = set(prog['done'])
    
    remaining = [p for p in posts if p['id'] not in done_ids]
    log(f'Total: {len(posts)}, done: {len(done_ids)}, remaining: {len(remaining)}')
    
    for i, post in enumerate(remaining):
        url = post['link']
        log(f'[{i+1}/{len(remaining)}] Saving {url}')
        if save_to_wayback(url):
            prog['done'].append(post['id'])
            log(f'  OK')
        else:
            prog['failed'].append({'id': post['id'], 'url': url})
            log(f'  FAILED')
        save_progress(prog)
        # Rate limit: 65s between saves
        if i < len(remaining) - 1:
            time.sleep(65)
    
    log(f'Finished. Done: {len(prog["done"])}, failed: {len(prog["failed"])}')

if __name__ == '__main__':
    main()
