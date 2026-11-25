import json, time, urllib.request, urllib.parse, os
from datetime import datetime

BASE = "/home/hatch/workspace/goals/idaho-reports-wordpress-posts-archive/hidden_files"
POSTS_FILE = os.path.join(BASE, "logan_bylined_posts.json")
PROGRESS_FILE = os.path.join(BASE, "wayback_logan_progress.json")
LOG_FILE = os.path.join(BASE, "wayback_logan_log.txt")

with open(POSTS_FILE) as f:
    posts = json.load(f)

# Load progress
if os.path.exists(PROGRESS_FILE):
    with open(PROGRESS_FILE) as f:
        progress = json.load(f)
else:
    progress = {"done": [], "failed": []}

done_ids = set(progress["done"])
remaining = [p for p in posts if p["id"] not in done_ids]

def log(msg):
    ts = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    line = f"{ts} {msg}"
    print(line, flush=True)
    with open(LOG_FILE, "a") as f:
        f.write(line + "\n")

def save_progress():
    with open(PROGRESS_FILE, "w") as f:
        json.dump(progress, f)

log(f"Total: {len(posts)}, done: {len(done_ids)}, remaining: {len(remaining)}")

for i, post in enumerate(remaining):
    url = post["link"]
    log(f"[{i+1}/{len(remaining)}] Saving {url}")
    try:
        save_url = "https://web.archive.org/save/" + url
        req = urllib.request.Request(save_url, headers={"User-Agent": "Mozilla/5.0 (compatible; archive-bot/1.0)"})
        with urllib.request.urlopen(req, timeout=120) as r:
            if r.status in (200, 302):
                log(f"  OK")
                progress["done"].append(post["id"])
            else:
                log(f"  HTTP {r.status}")
                progress["failed"].append(post["id"])
    except Exception as e:
        log(f"  FAILED: {e}")
        progress["failed"].append(post["id"])
    
    save_progress()
    # Respectful delay
    if i < len(remaining) - 1:
        time.sleep(65)

log("Done!")
