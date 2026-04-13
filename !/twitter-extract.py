"""
Twitter Archive → IDAHO-VAULT Markdown Extractor
Converts tweets.js from a Twitter/X data export into individual
markdown notes in @/ (the social archive folder).

Output structure:
  @/tweets/YYYY/YYYY-MM-DD - @lfinneytweets - <truncated text>.md

Each note gets YAML frontmatter with metadata and the full tweet text.
"""

import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from html import unescape
import zipfile
import shutil

VAULT_ROOT = Path(r"c:\Users\loganf\Documents\IDAHO-VAULT")
TEMP_DIR = Path(os.environ["TEMP"]) / "twitter-extract"
OUTPUT_DIR = VAULT_ROOT / "@" / "tweets"

# --- Helpers ---

def load_twitter_js(filepath: Path) -> list:
    """Parse a Twitter archive .js file (strips the window.YTD assignment)."""
    if not filepath.exists():
        return []
    raw = filepath.read_text(encoding="utf-8")
    # Remove "window.YTD.<name>.part0 = " prefix
    json_text = re.sub(r'^window\.YTD\.\w+\.part\d+\s*=\s*', '', raw)
    return json.loads(json_text)


def get_existing_ids(output_dir: Path) -> set:
    """Scan the output directory for already extracted tweet IDs."""
    ids = set()
    print(f"Indexing existing tweets in {output_dir}...")
    for md_file in output_dir.glob("**/*.md"):
        try:
            content = md_file.read_text(encoding="utf-8")
            match = re.search(r'tweet_id: "(\d+)"', content)
            if match:
                ids.add(match.group(1))
        except Exception:
            continue
    print(f"Found {len(ids)} existing tweets.")
    return ids


def extract_metadata_from_zip(zip_path: Path, temp_dir: Path):
    """Extract only metadata JS files from the archive to save resources."""
    print(f"Extracting metadata from {zip_path.name}...")
    temp_dir.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zip_path, 'r') as z:
        for member in z.namelist():
            if member.endswith(('tweets.js', 'account.js')):
                # Archive structure is usually data/tweets.js
                filename = Path(member).name
                with z.open(member) as source, open(temp_dir / filename, "wb") as target:
                    shutil.copyfileobj(source, target)


def parse_date(twitter_date_str: str) -> datetime:
    """Parse Twitter's date format: 'Sat Mar 07 21:32:40 +0000 2026'"""
    return datetime.strptime(twitter_date_str, "%a %b %d %H:%M:%S %z %Y")


def clean_source(source_html: str) -> str:
    """Extract app name from source HTML like '<a href="...">Twitter for Android</a>'"""
    match = re.search(r'>([^<]+)<', source_html)
    return match.group(1) if match else source_html


def sanitize_filename(text: str, max_len: int = 60) -> str:
    """Create a safe filename from tweet text."""
    # Remove @mentions at the start (for replies)
    text = re.sub(r'^(@\w+\s*)+', '', text).strip()
    if not text:
        text = "reply"
    # Unescape HTML entities
    text = unescape(text)
    # Remove URLs
    text = re.sub(r'https?://\S+', '', text).strip()
    # Remove characters unsafe for filenames
    text = re.sub(r'[<>:"/\\|?*\n\r\t]', ' ', text)
    # Collapse whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    # Truncate
    if len(text) > max_len:
        text = text[:max_len].rsplit(' ', 1)[0] + '...'
    return text or "tweet"


def build_tweet_markdown(tweet: dict) -> str:
    """Convert a single tweet object into a markdown note."""
    dt = parse_date(tweet["created_at"])
    date_str = dt.strftime("%Y-%m-%d")
    time_str = dt.strftime("%H:%M:%S")
    full_text = unescape(tweet.get("full_text", ""))
    tweet_id = tweet["id_str"]
    source = clean_source(tweet.get("source", ""))
    retweet_count = tweet.get("retweet_count", "0")
    fav_count = tweet.get("favorite_count", "0")
    lang = tweet.get("lang", "en")

    # Determine tweet type
    is_retweet = full_text.startswith("RT @")
    is_reply = tweet.get("in_reply_to_status_id_str") is not None
    reply_to = tweet.get("in_reply_to_screen_name", "")

    if is_retweet:
        tweet_type = "retweet"
    elif is_reply:
        tweet_type = "reply"
    else:
        tweet_type = "original"

    # Extract mentions
    entities = tweet.get("entities", {})
    mentions = [m["screen_name"] for m in entities.get("user_mentions", [])]
    hashtags = [h["text"] for h in entities.get("hashtags", [])]
    urls = [u.get("expanded_url", u.get("url", "")) for u in entities.get("urls", [])]

    # Extract media URLs if present
    media = tweet.get("extended_entities", {}).get("media", [])
    if not media:
        media = entities.get("media", [])
    media_urls = [m.get("media_url_https", m.get("media_url", "")) for m in media]

    # Build frontmatter
    fm_lines = [
        "---",
        f"date: {date_str}",
        f"time: {time_str}",
        f"tweet_id: \"{tweet_id}\"",
        f"type: {tweet_type}",
        f"source: \"{source}\"",
        f"retweets: {retweet_count}",
        f"favorites: {fav_count}",
        f"lang: {lang}",
        "authority: LOGAN",
    ]
    if is_reply and reply_to:
        fm_lines.append(f"reply_to: \"@{reply_to}\"")
    if mentions:
        fm_lines.append("mentions:")
        for m in mentions:
            fm_lines.append(f"  - \"@{m}\"")
    if hashtags:
        fm_lines.append("hashtags:")
        for h in hashtags:
            fm_lines.append(f"  - \"{h}\"")

    # Related tags for vault linking
    related = ["Twitter", "lfinneytweets"]
    if hashtags:
        related.extend(hashtags[:5])
    fm_lines.append("related:")
    for r in related:
        fm_lines.append(f"  - {r}")

    fm_lines.append("---")

    # Build body
    body_lines = [full_text]

    if urls:
        body_lines.append("")
        body_lines.append("## Links")
        for url in urls:
            body_lines.append(f"- {url}")

    if media_urls:
        body_lines.append("")
        body_lines.append("## Media")
        for mu in media_urls:
            body_lines.append(f"- ![]({mu})")

    if is_reply and reply_to:
        body_lines.append("")
        body_lines.append(f"*In reply to [@{reply_to}](https://twitter.com/{reply_to})*")

    # Permalink
    body_lines.append("")
    body_lines.append(f"[View on Twitter](https://twitter.com/lfinneytweets/status/{tweet_id})")

    return "\n".join(fm_lines) + "\n\n" + "\n".join(body_lines) + "\n"


def main():
    if len(sys.argv) < 2:
        print(f"Usage: python {sys.argv[0]} <twitter-archive.zip>")
        # Look for the default archive if not provided
        default_zip = VAULT_ROOT / "!" / "twitter-archive-2026-04-08.zip"
        if default_zip.exists():
            zip_path = default_zip
            print(f"No archive provided, using default: {zip_path}")
        else:
            sys.exit(1)
    else:
        zip_path = Path(sys.argv[1])

    if not zip_path.exists():
        print(f"Error: Archive not found at {zip_path}")
        sys.exit(1)

    # 1. Targeted Extraction
    extract_metadata_from_zip(zip_path, TEMP_DIR)

    # 2. Build de-duplication index
    existing_ids = get_existing_ids(OUTPUT_DIR)

    print("Loading tweets.js...")
    tweets_data = load_twitter_js(TEMP_DIR / "tweets.js")
    if not tweets_data:
        print("No tweets found in archive.")
        return
    print(f"Loaded {len(tweets_data)} tweets from archive")

    # Sort by date (oldest first)
    tweets_data.sort(key=lambda t: parse_date(t["tweet"]["created_at"]))

    # Stats
    years = {}
    types = {"original": 0, "reply": 0, "retweet": 0}
    created = 0
    skipped = 0

    for item in tweets_data:
        tweet = item["tweet"]
        dt = parse_date(tweet["created_at"])
        year = dt.strftime("%Y")
        month = dt.strftime("%m")
        date_str = dt.strftime("%Y-%m-%d")
        full_text = unescape(tweet.get("full_text", ""))
        tweet_id = tweet["id_str"]

        # De-duplication check
        if tweet_id in existing_ids:
            skipped += 1
            continue

        # Determine type for stats
        is_retweet = full_text.startswith("RT @")
        is_reply = tweet.get("in_reply_to_status_id_str") is not None
        if is_retweet:
            types["retweet"] += 1
        elif is_reply:
            types["reply"] += 1
        else:
            types["original"] += 1

        years[year] = years.get(year, 0) + 1

        # Build filename
        slug = sanitize_filename(full_text)
        filename = f"{date_str} - @lfinneytweets - {slug}.md"

        # Create year directory
        year_dir = OUTPUT_DIR / year
        year_dir.mkdir(parents=True, exist_ok=True)

        filepath = year_dir / filename

        # Handle duplicate filenames (multiple tweets same day, similar text)
        if filepath.exists():
            filepath = year_dir / f"{date_str} - @lfinneytweets - {slug} ({tweet_id[-6:]}).md"

        # Write
        try:
            content = build_tweet_markdown(tweet)
            filepath.write_text(content, encoding="utf-8")
            created += 1
        except Exception as e:
            print(f"  ERROR on tweet {tweet_id}: {e}")
            skipped += 1

    # Print summary
    print(f"\n{'='*50}")
    print(f"EXTRACTION COMPLETE")
    print(f"{'='*50}")
    print(f"Total tweets processed: {len(tweets_data)}")
    print(f"Files created: {created}")
    print(f"Skipped/errors: {skipped}")
    print(f"\nBy type:")
    for t, c in sorted(types.items()):
        print(f"  {t}: {c}")
    print(f"\nBy year:")
    for y in sorted(years.keys()):
        print(f"  {y}: {years[y]}")
    print(f"\nOutput: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
