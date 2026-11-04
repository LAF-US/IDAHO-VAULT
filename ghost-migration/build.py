#!/usr/bin/env python3
"""
build.py -- Discover, fetch, conform, and export Logan's bylined articles.

One script, one invocation: python3 build.py

Pipeline (separate jobs, one article at a time):
  1. DISCOVER    -- Paginate WordPress REST APIs; find posts whose byline
                    element credits Logan Finney (structural check, not
                    page-wide regex).
  2. CLASSIFY    -- Confirm the name is a byline, not a photo credit.
  3. FETCH       -- Pull each article's HTML via its outlet's REST API.
  4. PHOTOS      -- Identify Logan-credited photos from figure/caption
                    structure. Image and caption treated as one unit.
  5. CONFORM     -- Allowlist HTML; embeds to links (except Flourish /
                    Datawrapper / ArcGIS); promos, bios, chrome stripped.
  6. AP STYLE    -- Proofreader-style normalization on body text.
  7. EXPORT      -- Ghost 6 JSON + ZIP with only referenced images.

Rules (from the user's requirements):
  - Nothing hardcoded (sole exception: the Project FARE article seed --
    its live site is dead, so the Wayback lookup needs a starting URL).
  - Feature image: a kept Logan photo (cropped 1.91:1) or the outlet
    filler. Never a publisher/API featured image.
  - Body keeps only Logan-credited photos.
  - No modes, switches, or pass-throughs. No hand-edited output.
"""

import json
import re
import time
import hashlib
import html as htmlmod
import urllib.request
import urllib.error
import urllib.parse
from pathlib import Path
from urllib.parse import urlparse
from html.parser import HTMLParser
from PIL import Image, ImageOps

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0 Safari/537.36")

TITLE_SUFFIXES = [" - Idaho Reports", " | idahopublicradio",
                  " | F\u0101VS News", " - F\u0101VS News",
                  " \u2014 Project FARE", " - Project FARE"]

AUTHORY_URL = "https://authory.com/loganfinney"

OUTLET_META = {
    "Idaho Reports":      {"prefix": "idaho-reports",
                           "ghost_tag_slug": "idre",
                           "ghost_tag_name": "Logan Finney @ Idaho Reports",
                           "filler": "content/images/filler-idaho-reports.jpg",
                           "api": "https://blog.idahoreports.idahoptv.org",
                           "api_path": "/wp-json/wp/v2"},
    "Idaho Public Radio": {"prefix": "ipr",
                           "ghost_tag_slug": "ipub",
                           "ghost_tag_name": "Logan Finney @ Idaho Public Radio",
                           "filler": "content/images/filler-ipr.jpg",
                           "api": "https://public-api.wordpress.com/wp/v2/sites/"
                                  "idahopublicradio.wordpress.com",
                           "api_path": ""},
    "F\u0101VS News":     {"prefix": "favs",
                           "ghost_tag_slug": "favs",
                           "ghost_tag_name": "Logan Finney @ F\u0101VS News",
                           "filler": "content/images/filler-favs.jpg",
                           "api": "https://favs.news",
                           "api_path": "/wp-json/wp/v2"},
    "Project FARE":       {"prefix": "fare",
                           "ghost_tag_slug": "fare",
                           "ghost_tag_name": "Logan Finney @ Project FARE",
                           "filler": "content/images/fare-header-v3-defringe.jpg",
                           "api": None,  # live site dead; Wayback derived below
                           "api_path": None},
}

KEEP_IFRAME_HOSTS = ("flourish.studio", "flo.uri.sh", "datawrapper.dwcdn.net",
                      "arcgis.com")

# Publisher promo signatures: a paragraph matching ALL strings in a group
# is a publisher ask, not article text. Narrow distinctive sets, verified
# against source. Never matches promo words inside real reporting.
PROMO_SIGNATURES = (
    ("tax-deductible", "donat", "f\u0101vs"),
    ("f\u0101vs news daily newsletter",),
)

CC_URL = "https://creativecommons.org/licenses/by-nd/4.0/"

IMG_DIR = Path(__file__).resolve().parent / "import-zip" / "content" / "images"


# ----------------------------------------------------------------------
# Job 1: DISCOVER -- find candidate posts via WordPress APIs
# ----------------------------------------------------------------------

def _api_get(base, path, params, api_path="/wp-json/wp/v2"):
    """GET a WordPress REST endpoint; return parsed JSON or raise."""
    qs = urllib.parse.urlencode(params)
    url = "%s%s%s?%s" % (base, api_path, path, qs)
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    last = None
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                if r.status != 200:
                    raise RuntimeError("HTTP %s" % r.status)
                return json.loads(r.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            last = e
            if e.code == 429 and attempt < 3:
                time.sleep(15 * (attempt + 1))
                continue
            raise
    raise last


def _fare_snapshot_url():
    """Derive the Project FARE article URL at build time via the Wayback
    CDX API (live site is dead). Returns the latest snapshot URL."""
    cdx = ("https://web.archive.org/cdx/search/cdx?"
           "url=projectfare.org/farmstories/snow-rain-patterns-water-agriculture"
           "&output=json&limit=1&filter=statuscode:200")
    req = urllib.request.Request(cdx, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        data = json.loads(r.read().decode("utf-8"))
    if len(data) < 2:
        raise RuntimeError("No Wayback snapshot found for Project FARE article")
    timestamp, original = data[1][1], data[1][2]
    return "https://web.archive.org/web/%s/%s" % (timestamp, original)


def discover_posts():
    """Return [(outlet, post_id, url, title)] for candidate posts.

    Uses each outlet's WordPress REST API. A post is a candidate when its
    rendered content contains Logan's name; classification (byline vs
    photo credit) happens in the next job against source structure.
    """
    found = []
    for outlet, meta in OUTLET_META.items():
        if outlet == "Project FARE":
            # Single article; URL derived at build time, classification
            # by its byline element in the fetch job.
            try:
                fare_url = _fare_snapshot_url()
            except Exception as e:
                print("Project FARE skipped (Wayback unavailable): %s" % e)
                continue
            found.append((outlet, None, fare_url, None))
            continue
        base = meta["api"]
        api_path = meta["api_path"]
        page = 1
        while True:
            try:
                posts = _api_get(base, "/posts", {
                    "per_page": 100, "page": page,
                    "_fields": "id,link,title,content",
                }, api_path)
            except Exception as e:
                print("Discovery failed for %s page %d: %s" % (outlet, page, e))
                break
            if not posts:
                break
            for p in posts:
                content = p.get("content", {}).get("rendered", "")
                if "finney" in content.lower():
                    title = htmlmod.unescape(
                        p.get("title", {}).get("rendered", "")).strip()
                    found.append((outlet, p["id"], p["link"], title))
            if len(posts) < 100:
                break
            page += 1
            time.sleep(0.5)
    return found


# ----------------------------------------------------------------------
# Job 2: CLASSIFY -- byline or photo credit? (source structure)
# ----------------------------------------------------------------------

class _BylineParser(HTMLParser):
    """Extract candidate byline elements: <p> blocks and known byline
    containers, preserving their text in document order."""

    BYLINE_CLASSES = ("byline", "author", "entry-meta", "post-meta",
                      "article-meta", "by-author")

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.candidates = []   # (tag, class, text)
        self._buf = None
        self._tag = None
        self._cls = ""

    def handle_starttag(self, tag, attrs):
        ad = dict(attrs)
        cls = ad.get("class", "")
        tag = tag.lower()
        if tag == "p" or any(b in cls.lower() for b in self.BYLINE_CLASSES):
            # Flush any open candidate first (handles nested/unclosed tags).
            if self._buf is not None:
                text = re.sub(r"\s+", " ", "".join(self._buf)).strip()
                if text:
                    self.candidates.append((self._tag, self._cls, text))
            self._buf = []
            self._tag = tag
            self._cls = cls

    def handle_endtag(self, tag):
        if self._buf is not None and tag.lower() == self._tag:
            text = re.sub(r"\s+", " ", "".join(self._buf)).strip()
            if text:
                self.candidates.append((self._tag, self._cls, text))
            self._buf = None

    def close(self):
        # Flush any unclosed candidate at end of input.
        if self._buf is not None:
            text = re.sub(r"\s+", " ", "".join(self._buf)).strip()
            if text:
                self.candidates.append((self._tag, self._cls, text))
            self._buf = None
        super().close()

    def handle_data(self, data):
        if self._buf is not None:
            self._buf.append(data)


_BYLINE_RE = re.compile(
    r"\bby\s+logan\s+(a\.\s*)?finney\b"
    r"|\blogan\s+(a\.\s*)?finney\s*,?\s+and\s+[A-Z][a-z]+"
    r"|\bby\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+)?\s+and\s+logan\s+"
    r"(a\.\s*)?finney\b"
    r"|\bstory\s+and\s+photos?\s+by\s+logan\s+(a\.\s*)?finney\b"
    r"|\breporter\s+logan\s+(a\.\s*)?finney\b",
    re.I)


def classify_byline(html):
    """Return True if Logan Finney is a byline author (not only a photo
    credit), based on byline-bearing elements in source structure.

    A photo credit ("Photo by Logan Finney") does not count. "Story and
    Photos by Logan Finney" does count -- it asserts authorship.
    """
    parser = _BylineParser()
    parser.feed(html)
    parser.close()
    for tag, cls, text in parser.candidates:
        # "Story and Photos by" asserts authorship: always a byline.
        if re.search(r"\bstory\s+and\s+photos?\s+by\s+logan\s+"
                     r"(a\.\s*)?finney\b", text, re.I):
            return True
        # Strip photo credits, then look for a byline in what remains.
        # Handles "By Logan Finney (Photo by Logan Finney)": the credit
        # is removed, the byline survives.
        stripped = re.sub(r"\(\s*photos?\s+by\s+[^)]+\)", "", text,
                          flags=re.I)
        stripped = re.sub(r"\bphotos?\s+by\s+logan\s+(a\.\s*)?finney\b",
                          "", stripped, flags=re.I)
        if _BYLINE_RE.search(stripped):
            return True
    return False


# ----------------------------------------------------------------------
# Job 3: FETCH -- pull one article's HTML via its outlet's REST API
# ----------------------------------------------------------------------

def fetch(url, retries=6):
    if retries < 1:
        raise ValueError("retries must be >= 1")
    last = None
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=30) as resp:
                if resp.status != 200:
                    raise RuntimeError("HTTP %s" % resp.status)
                raw = resp.read()
            charset = resp.headers.get_content_charset() or "utf-8"
            return raw.decode(charset, errors="replace")
        except urllib.error.HTTPError as e:
            last = e
            if e.code == 429 and attempt < retries - 1:
                time.sleep(30 * (attempt + 1))
                continue
            raise
        except (urllib.error.URLError, TimeoutError, ConnectionError) as e:
            last = e
            if attempt < retries - 1:
                time.sleep(30 * (attempt + 1))
                continue
            raise
    raise last


def _api_post(base, api_path, post_id, notes, tag):
    """Fetch one post by ID from a WordPress REST API. Returns
    (title, content_html, date_str). Featured media is deliberately NOT
    collected: the feature image must be a Logan-credited photo or the
    outlet filler, never a publisher image."""
    p = _api_get(base, "/posts/%d" % post_id,
                 {"_fields": "title,content,date"}, api_path)
    if not isinstance(p, dict) or "title" not in p:
        # Post deleted (or API error) between discovery and fetch.
        code = p.get("code", "unknown") if isinstance(p, dict) else "unknown"
        raise RuntimeError("API error for post %d: %s" % (post_id, code))
    title = _straight_quotes(
        htmlmod.unescape(p["title"]["rendered"]).strip())
    content = p["content"]["rendered"]
    date = p["date"]
    notes.append("%s REST API" % tag)
    if tag == "F\u0101VS":
        # F\u0101VS API repeats the title at the top of content; strip it.
        # Compare against the unescaped content to handle entities/curly
        # quotes in the raw HTML.
        t_esc = re.escape(title)
        t_raw = re.escape(htmlmod.unescape(
            p["title"]["rendered"]).strip())
        for t_pat in (t_esc, t_raw):
            content = re.sub(r"^\s*<(h1|h2)[^>]*>\s*%s\s*</\1>\s*" % t_pat,
                             "", content, flags=re.I)
            content = re.sub(r"^\s*<p[^>]*>\s*%s\s*</p>\s*" % t_pat,
                             "", content, flags=re.I)
    return title, content, date


def fetch_article(outlet, post_id, url, notes):
    """Fetch one article. Returns (title, body_html, published)."""
    meta = OUTLET_META[outlet]
    if outlet == "Project FARE":
        raw = fetch(url)
        time.sleep(1.0)
        title = extract_title(raw)
        body = extract_body(raw)
        published = extract_published(raw, url)
        return title, body, published
    tag = {"Idaho Reports": "IR", "Idaho Public Radio": "IPR",
           "F\u0101VS News": "F\u0101VS"}[outlet]
    title, content, date = _api_post(meta["api"], meta["api_path"],
                                     post_id, notes, tag)
    time.sleep(1.0)
    return title, content, date


def extract_title(html):
    m = re.search(r'<meta[^>]+property="og:title"[^>]+content="([^"]+)"',
                  html, re.I)
    if not m:
        m = re.search(r'<meta[^>]+content="([^"]+)"[^>]+property="og:title"',
                      html, re.I)
    title = m.group(1) if m else ""
    if not title:
        m = re.search(r"<title>(.*?)</title>", html, re.S | re.I)
        title = m.group(1).strip() if m else ""
    title = _straight_quotes(htmlmod.unescape(title))
    for suffix in TITLE_SUFFIXES:
        if title.endswith(suffix):
            title = title[: -len(suffix)]
            break
    return re.sub(r"\s+", " ", title).strip()


def extract_published(html, url=None):
    m = re.search(r'<meta[^>]+property="article:published_time"[^>]+'
                  r'content="([^"]+)"', html, re.I)
    if m:
        return m.group(1)
    m = re.search(r'<meta[^>]+itemprop="datePublished"[^>]+'
                  r'content="([^"]+)"', html, re.I)
    if m:
        return m.group(1)
    m = re.search(r'<time[^>]+datetime="([^"]+)"', html, re.I)
    if m:
        val = m.group(1).strip()
        mon = re.match(r"^([A-Za-z]{3})\s+(\d{1,2})$", val)
        if mon and url:
            wm = re.search(r"web\.archive\.org/web/(\d{4})", url)
            if wm:
                months = {"Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4,
                          "May": 5, "Jun": 6, "Jul": 7, "Aug": 8,
                          "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12}
                mno = months.get(mon.group(1).title(), 1)
                return "%s-%02d-%02dT00:00:00+00:00" % (
                    wm.group(1), mno, int(mon.group(2)))
        return val
    return None


def _extract_inner(html, tag, class_sub=None):
    """Inner HTML of first <tag> whose class contains class_sub (or first
    <tag> if None), with depth counting for nested same-tags."""
    if class_sub:
        pat = re.compile(r"<%s\b[^>]*?class=([\"'])[^>]*?%s[^>]*?\1[^>]*>"
                         % (tag, re.escape(class_sub)), re.I)
    else:
        pat = re.compile(r"<%s\b[^>]*>" % tag, re.I)
    m = pat.search(html)
    if not m:
        return None
    start, depth = m.end(), 1
    for tm in re.finditer(r"</?%s\b" % tag, html[start:], re.I):
        s = start + tm.start()
        if tm.group(0).startswith("</"):
            depth -= 1
            if depth == 0:
                return html[start:s]
        else:
            full = html[s:html.find(">", s) + 1]
            if not full.rstrip().endswith("/>"):
                depth += 1
    return None


def extract_body(html):
    for tag, class_sub in [
        ("div", "wp-block-post-content"),
        ("div", "entry-content"),
        ("div", "blog-item-content"),
        ("article", None),
        ("main", None),
    ]:
        body = _extract_inner(html, tag, class_sub)
        if body and len(body.strip()) > 200:
            return body
    return None


# ----------------------------------------------------------------------
# Job 4: PHOTOS -- identify Logan-credited photos (figure + caption units)
# ----------------------------------------------------------------------

def _is_logan_photo(figcaption_text):
    return "logan finney" in figcaption_text.lower()


def _img_src(img_tag):
    for attr in ("data-large-file", "data-src", "src"):
        m = re.search(r'%s=(["\'])(.*?)\1' % attr, img_tag, re.I)
        if m:
            return htmlmod.unescape(m.group(2))
    return ""


def _img_alt(img_tag):
    m = re.search(r'alt=(["\'])(.*?)\1', img_tag, re.I)
    return htmlmod.unescape(m.group(2)) if m else ""


def find_logan_photos(body_html, page_url=""):
    """Return [(img_src, alt, caption)] for figures whose caption credits
    Logan Finney. Image and caption treated as one atomic unit.
    Relative srcs are resolved against the article URL."""
    kept = []
    for m in re.finditer(r"<figure\b[^>]*>(.*?)</figure>", body_html,
                         re.S | re.I):
        inner = m.group(1)
        if "<img" not in inner.lower():
            continue
        cap = ""
        fc = re.search(r"<figcaption[^>]*>(.*?)</figcaption>", inner,
                       re.S | re.I)
        if fc:
            cap = re.sub(r"\s+", " ",
                         re.sub(r"<[^>]+>", "", fc.group(1))).strip()
        if not _is_logan_photo(cap):
            continue
        im = re.search(r"<img\b[^>]*>", inner, re.I)
        if not im:
            continue
        src = _img_src(im.group(0))
        if not src or src.startswith("data:"):
            continue
        if page_url and not re.match(r"https?://", src, re.I):
            src = urllib.parse.urljoin(page_url, src)
        kept.append((src, _img_alt(im.group(0)), cap))
    return kept


def download_image(remote_url, cache, retries=3):
    """Fetch a remote image into import-zip/content/images/. Downloads to a
    temp file first and validates content: a failed or corrupt download is
    a build error, never a silent poisoned cache entry."""
    if remote_url in cache:
        return cache[remote_url]
    ext = Path(urlparse(remote_url).path).suffix.lower() or ".jpg"
    if ext not in (".jpg", ".jpeg", ".png", ".gif", ".webp"):
        ext = ".jpg"
    name = "photo-%s%s" % (hashlib.md5(
        remote_url.encode()).hexdigest()[:12], ext)
    dest = IMG_DIR / name
    if not dest.exists():
        IMG_DIR.mkdir(parents=True, exist_ok=True)
        tmp = dest.with_suffix(dest.suffix + ".tmp")
        last = None
        for attempt in range(retries):
            try:
                req = urllib.request.Request(remote_url,
                                             headers={"User-Agent": UA})
                with urllib.request.urlopen(req, timeout=30) as r, \
                        open(tmp, "wb") as f:
                    ctype = r.headers.get_content_type() or ""
                    if not (ctype.startswith("image/") or
                            ctype == "application/octet-stream"):
                        raise RuntimeError(
                            "not an image (%s): %s" % (ctype, remote_url))
                    f.write(r.read())
                # Validate it's actually decodable image data.
                Image.open(tmp).verify()
                tmp.rename(dest)
                last = None
                break
            except Exception as e:
                last = e
                if tmp.exists():
                    tmp.unlink()
                if attempt < retries - 1:
                    time.sleep(5 * (attempt + 1))
        if last is not None:
            raise RuntimeError("image download failed: %s (%s)"
                               % (remote_url, last))
    cache[remote_url] = name
    return name


def make_feature_image(photo_name, cache):
    """Center-crop a kept photo to 1.91:1 (1200x628). Fails loudly."""
    if photo_name in cache:
        return cache[photo_name]
    src = IMG_DIR / photo_name
    if not src.exists():
        raise RuntimeError("feature source missing: %s" % src)
    feat = "%s-feature.jpg" % Path(photo_name).stem
    dest = IMG_DIR / feat
    if not dest.exists():
        im = ImageOps.exif_transpose(Image.open(src)).convert("RGB")
        w, h = im.size
        if w < 10 or h < 10:
            raise RuntimeError("image too small for feature crop: %s" % src)
        target = 1200 / 628
        if w / h > target:
            nw = int(h * target)
            x = (w - nw) // 2
            im = im.crop((x, 0, x + nw, h))
        else:
            nh = int(w / target)
            y = (h - nh) // 2
            im = im.crop((0, y, w, y + nh))
        im = im.resize((1200, 628), Image.LANCZOS)
        im.save(dest, "JPEG", quality=88)
    cache[photo_name] = feat
    return feat


# ----------------------------------------------------------------------
# Job 5: CONFORM -- allowlist HTML to the Ghost import spec
# ----------------------------------------------------------------------

def convert_twitter(html, notes):
    """Twitter embeds -> inline paragraph text (link preserved)."""

    def twitter_repl(m):
        inner = m.group(1)
        text = re.sub(r"<(?!/?a(\s|>))[^>]+>", "", inner, flags=re.I)
        text = re.sub(r"\s+", " ", text).strip()
        text = _straight_quotes(text)
        if not text:
            return ""
        notes.append("twitter->inline")
        return "<p>%s</p>" % text

    html = re.sub(r"<blockquote\b[^>]*class=\"[^\"]*twitter-tweet[^\"]*\""
                  r"[^>]*>(.*?)</blockquote>", twitter_repl, html,
                  flags=re.S | re.I)
    html = re.sub(r'<figure\b[^>]*class="[^"]*wp-block-embed-twitter[^"]*"'
                  r'[^>]*>(.*?)</figure>', twitter_repl, html, flags=re.S | re.I)
    return html


def convert_embeds(html, notes):
    """Keep Flourish/Datawrapper/ArcGIS iframes. Convert every other embed
    to a plain paragraph link with WCAG AAA link text."""

    def iframe_repl(m):
        full = m.group(0)
        # Extract just the opening tag for attribute parsing.
        tag = re.match(r"<iframe\b[^>]*>", full, re.I)
        tag = tag.group(0) if tag else full
        src = re.search(r'src=(["\'])(.*?)\1', tag)
        src = htmlmod.unescape(src.group(2)).strip() if src else ""
        # Protocol-relative URLs: assume https.
        if src.startswith("//"):
            src = "https:" + src
        if src and not re.match(r"https?://", src, re.I):
            notes.append("embed dropped: non-http src")
            return ""
        host = urlparse(src).netloc.lower()
        if any(h in host for h in KEEP_IFRAME_HOSTS):
            return '<iframe src="%s"></iframe>' % htmlmod.escape(src,
                                                                 quote=True)
        tm = re.search(r'title=(["\'])(.*?)\1', tag, re.I)
        frame_title = htmlmod.unescape(tm.group(2)).strip() if tm else ""
        frame_title = re.sub(r"\s*#\w+", "", frame_title).strip()
        url, text = src, None
        if "youtube.com/embed/" in src or "youtube-nocookie.com/embed/" in src:
            vid = src.split("/embed/")[1].split("?")[0].split("/")[0]
            url = "https://www.youtube.com/watch?v=" + vid
            text = frame_title or "Watch on YouTube"
        elif "videopress.com/embed/" in src:
            slug = src.split("/embed/")[1].split("?")[0]
            url = "https://videopress.com/v/" + slug
            text = frame_title or "Watch the video"
        elif "soundcloud.com/player" in src:
            text = frame_title or "Listen on SoundCloud"
        elif "pbs.org" in host:
            text = frame_title or "Watch the PBS video"
        elif not src:
            return ""
        if text is None:
            text = frame_title or ("View embedded content from %s" % host)
        notes.append("embed->link: " + host)
        return '<p><a href="%s">%s</a></p>' % (url, htmlmod.escape(text))

    # Match full iframe elements (incl. fallback text), not just open tags.
    html = re.sub(r"<iframe\b[^>]*>.*?</iframe>",
                  lambda m: iframe_repl(m), html, flags=re.S | re.I)
    html = re.sub(r"<iframe\b[^>]*>",
                  lambda m: iframe_repl(m), html, flags=re.I)
    return html


def conform_body(raw_body, notes, logan_photos, img_cache, outlet):
    """Conform article HTML via allowlist. Keeps: paragraphs, headings,
    quotes, lists, links, inline formatting, separators, Logan's photos
    (as Ghost image cards, from the pre-identified list), kept embeds.
    Everything else is dropped."""
    h = raw_body

    # Truncate at -END- (IPR end-of-content marker).
    end_match = re.search(r"<p[^>]*>\s*-END-", h, re.I)
    if end_match:
        h = h[:end_match.start()]
        notes.append("truncated at -END-")

    # Strip author bio columns (structural: wp-block-columns with /author/).
    def _strip_bio_columns(html):
        out, i = [], 0
        pat = re.compile(
            r'<div\b[^>]*class=([\"\'])[^>]*?wp-block-columns[^>]*?\1[^>]*>',
            re.I)
        while True:
            m = pat.search(html, i)
            if not m:
                out.append(html[i:])
                break
            depth, j = 1, m.end()
            end_pos = len(html)
            for tm in re.finditer(r"</?div\b", html[j:], re.I):
                s = j + tm.start()
                if tm.group(0).startswith("</"):
                    depth -= 1
                    if depth == 0:
                        end_pos = html.find(">", s) + 1
                        break
                else:
                    full = html[s:html.find(">", s) + 1]
                    if not full.rstrip().endswith("/>"):
                        depth += 1
            block = html[m.start():end_pos]
            if re.search(r'href="[^"]*/author/[^"]*"', block, re.I):
                # Only strip if we found a real closing tag; an unclosed
                # div to end-of-document is malformed HTML, not a bio.
                if end_pos < len(html):
                    out.append(html[i:m.start()])
                    i = end_pos
                    notes.append("author bio stripped")
                else:
                    out.append(html[i:m.end()])
                    i = m.end()
                    notes.append("unclosed columns div left intact")
            else:
                out.append(html[i:m.end()])
                i = m.end()
        return "".join(out)
    h = _strip_bio_columns(h)

    # Twitter embeds -> inline text (before figure processing, since
    # twitter figures are handled here, not by convert_embeds).
    h = convert_twitter(h, notes)

    # Figures as atomic units. Embed figures convert via embed rules.
    # Photo figures: Idaho Reports strips ALL (user 2026-10-17); other
    # outlets keep Logan-credited ones. Iframes still go through conversion.
    photo_cards = {}
    if outlet != "Idaho Reports":
        for src, alt, cap in logan_photos:
            local = download_image(src, img_cache)
            notes.append("his photo kept: " + local)
            figcap = ("<figcaption>%s</figcaption>" % htmlmod.escape(cap)) if cap else ""
            photo_cards[src] = (
                '<figure class="kg-card kg-image-card">'
                '<img src="__GHOST_URL__/content/images/%s" class="kg-image" alt="%s">'
                "%s</figure>" % (local, htmlmod.escape(alt, quote=True), figcap))

    def figure_repl(m):
        attrs, inner = m.group(1), m.group(2)
        low = inner.lower()
        if "<iframe" in low:
            im = re.search(r'<iframe\b[^>]*>', inner, re.I)
            if im:
                # Preserve the full iframe tag (incl. title) for conversion.
                return convert_embeds(im.group(0), notes)
            return ""
        if "<img" in low:
            im = re.search(r"<img\b[^>]*>", inner, re.I)
            src = _img_src(im.group(0)) if im else ""
            if src in photo_cards:
                return photo_cards[src]
            notes.append("figure+image stripped")
            return ""
        if "pullquote" in attrs.lower():
            bq = re.search(r"<blockquote[^>]*>(.*?)</blockquote>", inner,
                           re.S | re.I)
            if bq:
                return "<blockquote>%s</blockquote>" % bq.group(1)
            return ""
        notes.append("figure dropped (unknown type)")
        return ""

    h = re.sub(r"<figure\b([^>]*)>(.*?)</figure>", figure_repl,
               h, flags=re.S | re.I)

    KEEP = {"p", "h2", "h3", "h4", "blockquote", "ul", "ol", "li",
            "a", "strong", "em", "hr", "br", "cite",
            "figure", "figcaption", "img"}
    DROP_CONTENT = {"script", "style", "noscript", "object", "svg",
                    "form", "input", "select", "textarea", "nav",
                    "template", "button"}

    class P(HTMLParser):
        def __init__(self):
            super().__init__(convert_charrefs=False)
            self.out = []
            self.drop_depth = 0
            self.dead_a_depth = 0  # track <a> without href to skip

        def handle_starttag(self, tag, attrs):
            tag = tag.lower()
            if self.drop_depth:
                if tag in DROP_CONTENT:
                    self.drop_depth += 1
                return
            if tag in DROP_CONTENT:
                self.drop_depth = 1
                return
            if tag == "iframe":
                ad = dict(attrs)
                src = ad.get("src", "")
                host = urlparse(src).netloc.lower() if src else ""
                if src and any(x in host for x in KEEP_IFRAME_HOSTS):
                    self.out.append('<iframe src="%s"></iframe>'
                                    % htmlmod.escape(src, quote=True))
                elif src.startswith("http"):
                    self.out.append("EMBED::%s::" % src)
                self.drop_depth = 1
                return
            if tag == "img":
                ad = dict(attrs)
                src, alt, cls = ad.get("src", ""), ad.get("alt", ""), ad.get("class", "")
                # Keep only Ghost-card images (already vetted as Logan's).
                # Bare remote <img> tags bypass the photo filter: drop them.
                if src.startswith("__GHOST_URL__/content/images/"):
                    self.out.append(
                        '<img src="%s" class="%s" alt="%s">'
                        % (htmlmod.escape(src, quote=True),
                           htmlmod.escape(cls, quote=True),
                           htmlmod.escape(alt, quote=True)))
                elif src:
                    pass  # bare remote image: dropped
                return
            if tag in KEEP:
                if tag == "a":
                    href = dict(attrs).get("href", "")
                    if href:
                        self.out.append('<a href="%s">' % htmlmod.escape(href, quote=True))
                    else:
                        # Dead anchor (no href): skip the tags, keep the text
                        self.dead_a_depth += 1
                        return
                elif tag in ("hr", "br"):
                    self.out.append("<%s>" % tag)
                elif tag == "figure":
                    cls = dict(attrs).get("class", "")
                    self.out.append('<figure class="%s">'
                                    % htmlmod.escape(cls, quote=True))
                else:
                    self.out.append("<%s>" % tag)

        def handle_endtag(self, tag):
            tag = tag.lower()
            if self.drop_depth:
                if tag in DROP_CONTENT or tag == "iframe":
                    self.drop_depth -= 1
                return
            if tag == "a" and self.dead_a_depth > 0:
                self.dead_a_depth -= 1
                return
            if tag in KEEP and tag not in ("hr", "br"):
                self.out.append("</%s>" % tag)

        def handle_data(self, data):
            if not self.drop_depth:
                if self.out:
                    last = self.out[-1]
                    if last and last[-1].isalnum() and data and data[0].isalnum():
                        self.out.append(" ")
                self.out.append(data)

        def handle_entityref(self, name):
            # Preserve entities (&amp; &nbsp; &mdash; ...) instead of
            # silently dropping them.
            if not self.drop_depth:
                self.out.append("&%s;" % name)

        def handle_charref(self, name):
            if not self.drop_depth:
                self.out.append("&#%s;" % name)

        def handle_comment(self, data):
            pass

    parser = P()
    parser.feed(h)
    h = "".join(parser.out)

    def _embed_repl(m):
        return convert_embeds('<iframe src="%s"></iframe>' % m.group(1), notes)
    h = re.sub(r"EMBED::(.*?)::", _embed_repl, h)

    h = re.sub(r"\(\s*Photos?\s+by\s+[^)]+\)", "", h, flags=re.I)

    def _promo(m):
        t = re.sub(r"<[^>]+>", " ", m.group(0)).lower()
        if any(all(s in t for s in sig) for sig in PROMO_SIGNATURES):
            notes.append("promo stripped")
            return ""
        return m.group(0)
    h = re.sub(r"<p>.*?</p>", _promo, h, flags=re.S | re.I)

    h = re.sub(r"<p>\s*</p>", "", h)
    h = re.sub(r"<(h[2-4]|blockquote|li)>\s*</\1>", "", h)
    h = re.sub(r'<a\b[^>]*>\s*Read more by.*?</a>', "", h, flags=re.S | re.I)
    h = re.sub(r"<p>\s*</p>", "", h)
    h = htmlmod.unescape(h)
    h = re.sub(r"[ \t]+", " ", h)
    h = re.sub(r"\n\s*\n\s*\n+", "\n\n", h)
    return h.strip()


def slugify(text):
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")[:110] or "untitled"


# ----------------------------------------------------------------------
# Job 6: AP STYLE -- proofreader-style normalization (user-approved)
# ----------------------------------------------------------------------

_AP_MONTH_ABBR = {"January": "Jan.", "February": "Feb.", "August": "Aug.",
                  "September": "Sept.", "October": "Oct.",
                  "November": "Nov.", "December": "Dec."}
_AP_ONES = {"1": "one", "2": "two", "3": "three", "4": "four", "5": "five",
            "6": "six", "7": "seven", "8": "eight", "9": "nine"}
_AP_TENS = {10: "ten", 11: "eleven", 12: "twelve", 13: "thirteen",
            14: "fourteen", 15: "fifteen", 16: "sixteen", 17: "seventeen",
            18: "eighteen", 19: "nineteen", 20: "twenty", 30: "thirty",
            40: "forty", 50: "fifty", 60: "sixty", 70: "seventy",
            80: "eighty", 90: "ninety"}
_AP_ABBR = ("St", "Mr", "Mrs", "Ms", "Dr", "Ave", "Blvd", "Rd", "Jan",
            "Feb", "Aug", "Sept", "Oct", "Nov", "Dec", "Sen", "Rep",
            "Gov", "Mt", "Dist")


def _spell_small(v):
    if v < 10:
        return _AP_ONES[str(v)]
    if v in _AP_TENS:
        return _AP_TENS[v]
    if v < 100:
        return "%s-%s" % (_AP_TENS[v // 10 * 10], _AP_ONES[str(v % 10)])
    parts = []
    if v >= 1000000:
        parts.append(_spell_small(v // 1000000) + " million")
        v %= 1000000
    if v >= 1000:
        parts.append(_spell_small(v // 1000) + " thousand")
        v %= 1000
    if v >= 100:
        parts.append(_AP_ONES[str(v // 100)] + " hundred")
        v %= 100
    if v > 0:
        parts.append(_spell_small(v))
    return " ".join(parts)


def _straight_quotes(s):
    return (s.replace("\u201c", '"').replace("\u201d", '"')
             .replace("\u2018", "'").replace("\u2019", "'"))


def _digit_may_spell(before, after):
    # Idaho legislative abbreviations (legislature.idaho.gov):
    # H, S (bills); HCR, SCR (concurrent resolutions);
    # HJR, SJR (joint resolutions); HJM, SJM (joint memorials);
    # HR, SR (resolutions)
    if re.search(r"\b(HJR|HCR|SCR|SJR|HJM|SJM|HR|SR)\s*$", before, re.I):
        return False
    # Single H/S for House/Senate bills ("H 493", "S 1227")
    if re.search(r"\b[HS]\s*$", before, re.I):
        return False
    if re.search(r"(Section|Article|District|Stage|Chapter|Part|Rule|"
                 r"Amendment|Bill|Page|Measure|"
                 r"Initiative|Referendum|Resolution|Memorial)\s*$",
                 before, re.I):
        return False
    # Proposition is handled separately: conform to formal ballot use
    # ("Proposition One", not "Proposition 1") per Idaho statute 34-1810
    if re.search(r"\b(Proposition|Prop)\s*$", before, re.I):
        return False
    if after.startswith("-H"):
        return False
    if re.search(r"\d\s*-\s*$", before) or re.match(r"\s*-\s*\d", after):
        return False
    if re.match(r"\s*[ap]\.m\.", after, re.I):
        return False
    if before.endswith("$"):
        return False
    if re.match(r"\s*%", after):
        return False
    if re.match(r"\s*(million|billion|trillion)\b", after, re.I):
        return False
    if re.search(r"(January|February|March|April|May|June|July|August|"
                 r"September|October|November|December|Jan\.|Feb\.|"
                 r"Aug\.|Sept\.|Oct\.|Nov\.|Dec\.)\s*$", before, re.I):
        return False
    # List markers ("5. item", "4) item") stay figures; sentence-final
    # periods do not block spelling out.
    if re.match(r"\)", after):
        return False
    if re.match(r"\.\s*\S", after):
        return False
    # AP: ages always use figures ("5 years old", "a 5-year-old boy").
    if re.match(r"\s*(years?\s+old|year-old)\b", after, re.I):
        return False
    if re.match(r"\s*-\s*year-old\b", after, re.I):
        return False
    # AP: dimensions always use figures ("5 feet wide", "6 inches deep").
    if re.match(r"\s*(feet|foot|inches|inch|miles|mile|yards|yard|"
                r"meters|meter|kilometers|kilometer)\b", after, re.I):
        return False
    if re.search(r"\(\s*-\s*$", before):
        return False
    return True


def _ap_block_rules(block, _chg, notes, log):
    tagph = []
    h2 = re.sub(r"<[^>]+>",
                lambda m: tagph.append(m.group(0)) or
                "\ue000G%d\ue001" % (len(tagph) - 1), block)
    _abbr_re = re.compile(r"\b(?:%s)\.$" % "|".join(_AP_ABBR))
    h3 = h2

    def _sent_rep(m):
        dot, sp, num = m.group(1), m.group(2), m.group(3)
        before = h3[max(0, m.start() - 8):m.start() + 1]
        if _abbr_re.search(before):
            return m.group(0)
        if re.fullmatch(r"(19|20)\d{2}", num):
            return m.group(0)
        v = int(num.replace(",", ""))
        # 100+ stays as numerals at sentence start (user 2026-10-16)
        if v >= 100:
            return m.group(0)
        if v < 10 and not _digit_may_spell("", h3[m.end():m.end() + 40]):
            return m.group(0)
        return dot + sp + _chg("sentence-start", num,
                               _spell_small(v).capitalize())

    h3 = re.sub(r"([.!?])(\s+)(\d[\d,]*)", _sent_rep, h3)

    def _sent_start_rep(m):
        num = m.group(2)
        if re.fullmatch(r"(19|20)\d{2}", num):
            return m.group(0)
        v = int(num.replace(",", ""))
        # 100+ stays as numerals at sentence start (user 2026-10-16)
        if v >= 100:
            return m.group(0)
        if v < 10 and not _digit_may_spell("", h3[m.end():m.end() + 40]):
            return m.group(0)
        return m.group(1) + _chg("sentence-start", num,
                                 _spell_small(v).capitalize())

    h3 = re.sub(r"^((?:\ue000[QG]\d+\ue001|\s)*)(\d[\d,]*)",
                _sent_start_rep, h3)
    h2 = re.sub(r"\ue000G(\d+)\ue001",
                lambda m: tagph[int(m.group(1))], h3)

    parts = re.split(r"(<[^>]+>|\ue000Q\d+\ue001)", h2)
    for i in range(0, len(parts), 2):
        t = parts[i]
        if not t or re.fullmatch(r"(?:\ue000Q\d+\ue001|\s)*", t):
            continue

        def _mon(m):
            return _chg("month-abbr", m.group(0),
                        _AP_MONTH_ABBR[m.group(1)] + " " + m.group(2))
        t = re.sub(r"\b(January|February|August|September|October|"
                   r"November|December)\s+(\d{1,2})\b", _mon, t)

        def _ord(m):
            mon = m.group(1)
            abbr = _AP_MONTH_ABBR.get(mon, mon)
            return _chg("ordinal-date", m.group(0),
                        abbr + " " + m.group(2))
        t = re.sub(r"\b(January|February|March|April|May|June|July|"
                   r"August|September|October|November|December)\s+"
                   r"(\d{1,2})(?:st|nd|rd|th)\b", _ord, t)

        _word_to_num = {"one": "1", "two": "2", "three": "3", "four": "4",
                        "five": "5", "six": "6", "seven": "7", "eight": "8",
                        "nine": "9", "ten": "10", "eleven": "11",
                        "twelve": "12"}

        def _wordtime(m):
            return _chg("time", m.group(0),
                        _word_to_num[m.group(1).lower()] + ":" +
                        m.group(2) + " " + m.group(3).lower()[0] + ".m.")
        t = re.sub(r"\b(one|two|three|four|five|six|seven|eight|nine|ten|"
                   r"eleven|twelve):(\d{2})\s*(a\.?m\.?|p\.?m\.?)(?!\w)",
                   _wordtime, t, flags=re.I)

        def _time(m):
            hr, ap = m.group(1), m.group(2).lower()
            if hr == "12":
                return _chg("time", m.group(0),
                            "noon" if ap == "pm" else "midnight")
            return _chg("time", m.group(0), "%s %s.m." % (hr, ap[0]))
        t = re.sub(r"\b(\d{1,2})(?::00)?\s*(am|pm)\b", _time, t, flags=re.I)

        t = re.sub(r"\b(\d[\d,\.]*)\s+percent\b",
                   lambda m: _chg("percent", m.group(0), m.group(1) + "%"),
                   t, flags=re.I)

        def _dol(m):
            if re.fullmatch(r"(19|20)\d{2}", m.group(1)):
                return m.group(0)
            return _chg("dollars", m.group(0), "$" + m.group(1))
        t = re.sub(r"(?<!\$)\b(\d[\d,\.]*)\s+dollars\b", _dol, t, flags=re.I)
        t = re.sub(r"\b(\d+)-dollar\b",
                   lambda m: _chg("dollars", m.group(0), "$" + m.group(1)),
                   t, flags=re.I)

        t = re.sub(r"\bSenator\s+([A-Z])",
                   lambda m: _chg("sen-rep", m.group(0), "Sen. " + m.group(1)), t)
        t = re.sub(r"\bRepresentative\s+([A-Z])",
                   lambda m: _chg("sen-rep", m.group(0), "Rep. " + m.group(1)), t)
        t = re.sub(r"\bGovernor\s+([A-Z])",
                   lambda m: _chg("gov", m.group(0), "Gov. " + m.group(1)), t)

        t = re.sub(r"\b(Jan|Feb|Aug|Sept|Oct|Nov|Dec)\s+(\d{1,2})\b",
                   lambda m: _chg("month-abbr", m.group(0),
                                  m.group(1) + ". " + m.group(2)), t)

        t = re.sub(r",\s*ID\b",
                   lambda m: _chg("state", m.group(0), ", Idaho"), t)

        t = re.sub(r"\btowards\b",
                   lambda m: _chg("toward", m.group(0), "toward"), t)
        t = re.sub(r"\bTowards\b",
                   lambda m: _chg("toward", m.group(0), "Toward"), t)
        t = re.sub(r"--",
                   lambda m: _chg("emdash", m.group(0), "\u2014"), t)

        t = re.sub(r"^by (Logan Finney)",
                   lambda m: _chg("byline-cap", m.group(0), "By " + m.group(1)), t)
        t = re.sub(r"\b(Senate|House) (Minority|Majority) Leader Sen\. ",
                   lambda m: _chg("double-title", m.group(0),
                                  m.group(1) + " " + m.group(2) + " Leader "), t)
        t = re.sub(r"\bR-CDA\b",
                   lambda m: _chg("r-cda", m.group(0), "R-Coeur d'Alene"), t)

        def _prop_num(m):
            # Conform to formal ballot use: "Proposition One" per Idaho 34-1810
            word = _spell_small(int(m.group(2))).capitalize()
            return _chg("proposition", m.group(0),
                        m.group(1) + " " + word)
        t = re.sub(r"\b(Proposition|Prop)\s+(\d{1,2})\b",
                   _prop_num, t)

        def _digit(m):
            s = m.start(1)
            before, after = t[max(0, s - 40):s], t[m.end(1):m.end(1) + 40]
            if not _digit_may_spell(before, after):
                return m.group(0)
            return _chg("digit", m.group(0), _AP_ONES[m.group(1)])
        t = re.sub(r"(?<![\d\w\.\$,])([1-9])(?![\d\w]|,(?=\d)|\.\d|:(\d))",
                   _digit, t)
        parts[i] = t
    return "".join(parts)


_AP_QUOT_RE = re.compile(r"\u201c(?:[^\u201d]|\u201c)*?\u201d")
_AP_BLOCK_SPLIT = re.compile(
    r"(<(?:p|h[1-6]|li|blockquote|figcaption)\b.*?"
    r"</(?:p|h[1-6]|li|blockquote|figcaption)>)",
    re.S | re.I)


def ap_normalize(html, notes):
    """Apply approved AP Style rules to body text. Quotations masked
    (curly-aware); tables masked; block-by-block with stray-quote skip;
    every change logged."""
    log = []

    def _chg(cat, before, after):
        if before != after:
            log.append((cat, before, after))
        return after

    h = html
    tables = []

    def _table_m(m):
        tables.append(m.group(0))
        return "\ue000T%d\ue001" % (len(tables) - 1)
    h = re.sub(r"<table\b.*?</table>", _table_m, h, flags=re.S | re.I)

    def _dblq(m):
        q = m.group(0)
        notes.append("AP doubled quote fixed: ...%s..." %
                     h[max(0, m.start() - 30):m.end() + 30][:60])
        return q[0]
    # Fix doubled quote marks (typos) before masking, on raw HTML.
    h = re.sub(r'"{2,}', _dblq, h)
    h = re.sub(r"'{2,}", _dblq, h)
    h = re.sub(r"\u201c{2,}", _dblq, h)
    h = re.sub(r"\u201d{2,}", _dblq, h)

    quotes = []

    def _quote_m(m):
        quotes.append(m.group(0))
        return "\ue000Q%d\ue001" % (len(quotes) - 1)
    # Mask curly quotes FIRST (multi-paragraph aware), before straightening.
    h = _AP_QUOT_RE.sub(_quote_m, h)
    # Straight quotes: never cross a block boundary (</p>, </li>, etc.).
    _BLOCK_CLOSE = r"</(?:p|li|blockquote|h[1-6]|figcaption)>"
    h = re.sub(r'"((?:(?!%s)[^"])*)"' % _BLOCK_CLOSE, _quote_m, h,
               flags=re.S | re.I)

    h = _straight_quotes(h)

    _tagph = []
    h = re.sub(r"<[^>]+>",
               lambda m: _tagph.append(m.group(0)) or
               "\ue000G%d\ue001" % (len(_tagph) - 1), h)

    h = re.sub(r"\ue000G(\d+)\ue001",
               lambda m: _tagph[int(m.group(1))], h)

    h = _straight_quotes(h)
    quotes = [_straight_quotes(q) for q in quotes]

    chunks = _AP_BLOCK_SPLIT.split(h)
    for i, chunk in enumerate(chunks):
        if not chunk or not chunk.strip():
            continue
        text_only = re.sub(r"<[^>]+>", "", chunk)
        if text_only.count('"') % 2 == 1:
            notes.append("AP skipped block (stray quote): %s..." %
                         text_only.strip()[:60])
            continue
        chunks[i] = _ap_block_rules(chunk, _chg, notes, log)
    h = "".join(chunks)

    h = re.sub(r"\ue000Q(\d+)\ue001",
               lambda m: quotes[int(m.group(1))], h)
    h = re.sub(r"\ue000T(\d+)\ue001",
               lambda m: tables[int(m.group(1))], h)

    by_cat = {}
    for cat, b, a in log:
        by_cat.setdefault(cat, []).append((b, a))
    for cat, items in sorted(by_cat.items()):
        notes.append("AP %s: %d change(s)" % (cat, len(items)))
        for b, a in items[:3]:
            notes.append("  AP '%s' -> '%s'" % (b[:60], a[:60]))
    return h


# ----------------------------------------------------------------------
# Job 7: EXPORT -- footer, feature image, Ghost JSON, ZIP
# ----------------------------------------------------------------------

def fetch_authory_posts():
    """Pull Logan's Authory index at build time; group by headline to find
    downstream republications of his articles."""
    from html.parser import HTMLParser

    class P(HTMLParser):
        def __init__(self):
            super().__init__()
            self.posts = []
            self._a = None

        def handle_starttag(self, tag, attrs):
            if tag == "a":
                ad = dict(attrs)
                h = ad.get("href", "")
                if h.startswith("/loganfinney/") and h.count("/") == 2:
                    self._a = (h, [])

        def handle_endtag(self, tag):
            if tag == "a" and self._a:
                href, buf = self._a
                self._a = None
                txt = re.sub(r"\s+", " ", "".join(buf)).strip()
                if txt:
                    pub = None
                    m = re.search(r"\|([^|]*)$", txt)
                    if m:
                        pub = m.group(1).strip()
                        txt = txt[:m.start()].strip()
                    self.posts.append((href, txt, pub))

        def handle_data(self, d):
            if self._a:
                self._a[1].append(d)

    url = AUTHORY_URL
    html = fetch(url)
    time.sleep(0.5)
    groups = {}
    p = P()
    p.feed(html)
    seen_urls = {url}
    for _ in range(50):  # pagination cap: never loop forever
        m = re.search(r'href="(/loganfinney/[^"]+)"[^>]*>\s*Next\s*</a>',
                      html, re.I)
        if not m:
            break
        url = urllib.parse.urljoin(AUTHORY_URL, htmlmod.unescape(m.group(1)))
        if url in seen_urls:
            break
        seen_urls.add(url)
        html = fetch(url)
        time.sleep(0.5)
        p.feed(html)
    for href, txt, pub in p.posts:
        groups.setdefault(txt.lower(), []).append((href, pub))
    multi = {}
    for headline, items in groups.items():
        pubs = {pub for _, pub in items if pub}
        if len(pubs) >= 2:
            multi[headline] = items
    return multi


def _utm_url(url):
    """Append republication UTM tags to a source URL."""
    # Split off fragment so UTM params go before it
    if "#" in url:
        base, frag = url.split("#", 1)
        frag = "#" + frag
    else:
        base, frag = url, ""
    sep = "&" if "?" in base else "?"
    return (base + sep +
            "utm_source=thegemstone.org&utm_medium=republication"
            "&utm_campaign=archive" + frag)


def make_footer(outlet, url, repubs, notes):
    # Order: original link -> CC BY-ND 4.0 (IR only) -> republished links.
    parts = []
    parts.append(
        '<p>Originally published at <a href="%s">%s</a>.</p>'
        % (htmlmod.escape(_utm_url(url), quote=True),
           htmlmod.escape(outlet)))
    if outlet == "Idaho Reports":
        parts.append(
            '<p>This work is licensed under <a href="%s">'
            "CC BY-ND 4.0</a>.</p>" % CC_URL)
    if repubs:
        for href, pub in repubs:
            if not pub:
                continue
            parts.append(
                '<p>Also published in <a href="https://authory.com%s">%s</a>.</p>'
                % (htmlmod.escape(href, quote=True), htmlmod.escape(pub)))
    return "\n".join(parts)


def emit_post(outlet, title, body, url, published, notes,
              img_cache, slug_log, logan_photos, used_slugs):
    """Emit one Ghost post. Feature image: a kept Logan photo or the
    outlet filler -- never a publisher/API image."""
    meta = OUTLET_META[outlet]
    slug = meta["prefix"] + "-" + slugify(title)
    while slug in used_slugs:
        slug += "-x"
    used_slugs.add(slug)
    slug_log.append(slug)

    # Feature image: always the outlet filler (user 2026-10-17: no body
    # photos, feature is the filler only).
    feat_file = meta["filler"].split("content/images/")[-1]
    notes.append("feature: outlet filler -> " + feat_file)

    callout = (
        '<div class="kg-card kg-callout-card"><div class="kg-callout-text">'
        'This article <a href="%s">originally appeared at %s</a>.</div></div>'
        % (htmlmod.escape(_utm_url(url), quote=True),
           htmlmod.escape(outlet)))
    body = callout + "\n" + body

    body = re.sub(r"</?(html|body|head)[^>]*>", "", body)

    # No mobiledoc: let Ghost parse the HTML into native elements.
    # (A mobiledoc with a single HTML card imports as one HTML block.)
    post = {
        "id": hashlib.md5(slug.encode()).hexdigest()[:24],
        "title": title, "slug": slug, "mobiledoc": None,
        "html": body,
        "canonical_url": url,
        "created_at": published, "updated_at": published,
        "published_at": published, "published_by": None, "created_by": None,
        "updated_by": None, "author_id": 0,
        "type": "post", "status": "draft", "visibility": "public",
        "featured": 0, "page": 0,
        "feature_image": "__GHOST_URL__/content/images/" + feat_file,
        "og_image": None, "og_title": None, "og_description": None,
        "twitter_image": None, "twitter_title": None,
        "twitter_description": None, "meta_title": None,
        "meta_description": None, "email_only": False,
        "email_subject": None, "email_recipient_filter": "none",
        "newsletter_id": None,
        "tags": [{"slug": meta["ghost_tag_slug"],
                  "name": meta["ghost_tag_name"]}],
        "authors": [{"slug": "logan"}]}
    return post, slug


def build_ghost_json(posts):
    """Assemble the Ghost 6 import package."""
    # Map tag slugs to tag IDs for posts_tags relationships
    tag_list = [{"id": "t%d" % i, "name": m["ghost_tag_name"],
                 "slug": m["ghost_tag_slug"], "description": None,
                 "feature_image": None, "parent_id": None,
                 "visibility": "public", "og_image": None,
                 "og_title": None, "og_description": None,
                 "twitter_image": None, "twitter_title": None,
                 "twitter_description": None, "meta_title": None,
                 "meta_description": None, "codeinjection_head": None,
                 "codeinjection_foot": None, "canonical_url": None,
                 "accent_color": None}
                for i, m in enumerate(OUTLET_META.values())]
    slug_to_tag_id = {t["slug"]: t["id"] for t in tag_list}
    # Build posts_tags from inline post tags
    posts_tags = []
    for p in posts:
        for t in p.get("tags", []):
            tag_id = slug_to_tag_id.get(t["slug"])
            if tag_id:
                posts_tags.append({"post_id": p["id"], "tag_id": tag_id})
    # Build posts_authors: all posts by the single author (id 0)
    posts_authors = [{"post_id": p["id"], "author_id": 0} for p in posts]
    return {
        "meta": {"exported_on": int(time.time() * 1000),
                 "version": "6.0.0"},
        "data": {
            "posts": posts,
            "users": [{
                "id": 0, "name": "Logan Finney", "slug": "logan",
                "email": "loganfinney@proton.me",
                "profile_image": None, "cover_image": None,
                "bio": None, "website": None, "location": None,
                "facebook": None, "twitter": None, "accessibility": None,
                "status": "active", "language": "en-US", "meta_title": None,
                "meta_description": None, "tour": None,
                "last_seen": None, "created_at": 0, "updated_at": 0,
                "roles": ["Author"],
                "password": None}],
            "roles": [{"id": "r1", "name": "Author",
                       "description": "Authors",
                       "created_at": 0, "updated_at": 0}],
            "tags": tag_list,
            "posts_tags": posts_tags,
            "posts_authors": posts_authors,
        }
    }


def write_zip(out_dir, json_name, json_bytes, referenced_images):
    """Assemble the ZIP with the JSON plus ONLY referenced images."""
    import zipfile
    zip_path = out_dir / (json_name.replace(".json", ".zip"))
    img_dir = out_dir / "content" / "images"
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr(json_name, json_bytes)
        seen = set()
        for img in referenced_images:
            if img in seen:
                continue
            seen.add(img)
            p = img_dir / img
            if not p.exists():
                raise RuntimeError("referenced image missing from disk: %s"
                                   % img)
            z.write(p, "content/images/" + img)
    return zip_path


# ----------------------------------------------------------------------
# MAIN -- one article at a time through the full pipeline
# ----------------------------------------------------------------------

def main():
    base = Path(__file__).resolve().parent
    out_dir = base / "import-zip"
    out_dir.mkdir(exist_ok=True)
    (out_dir / "content" / "images").mkdir(parents=True, exist_ok=True)

    candidates = discover_posts()
    print("Discovered %d candidates" % len(candidates))
    if not candidates:
        raise RuntimeError("no candidates discovered; all APIs may be down")

    try:
        authory_multi = fetch_authory_posts()
    except Exception as e:
        print("Authory unavailable: %s (republication links skipped)" % e)
        authory_multi = {}

    posts, notes, img_cache, slug_log = [], [], {}, []
    used_slugs = set()
    referenced_images = set()

    # Resume: load progress from a prior interrupted run, if any.
    progress_path = base / "build-progress.json"
    done_urls = set()
    if progress_path.exists():
        try:
            saved = json.loads(progress_path.read_text(encoding="utf-8"))
            posts = saved.get("posts", [])
            notes = saved.get("notes", [])
            img_cache = saved.get("img_cache", {})
            used_slugs = set(saved.get("used_slugs", []))
            referenced_images = set(saved.get("referenced_images", []))
            done_urls = set(saved.get("done_urls", []))
            print("Resumed: %d articles already done, skipping" % len(done_urls))
        except Exception as e:
            print("Progress file unreadable, starting fresh: %s" % e)

    def _save_progress():
        try:
            progress_path.write_text(json.dumps({
                "posts": posts,
                "notes": notes,
                "img_cache": img_cache,
                "used_slugs": sorted(used_slugs),
                "referenced_images": sorted(referenced_images),
                "done_urls": sorted(done_urls),
            }, ensure_ascii=False), encoding="utf-8")
        except Exception as e:
            print("Progress save failed: %s" % e)

    for outlet, post_id, url, _disc_title in candidates:
        if url in done_urls:
            continue
        time.sleep(1.0)  # courtesy delay between article fetches
        title, body_html, published = fetch_article(outlet, post_id, url,
                                                   notes)
        if not body_html:
            notes.append("excluded (no body extracted): %s" % url)
            done_urls.add(url)
            _save_progress()
            continue
        if not published:
            # FARE via Wayback may lack date metadata; fall back to the
            # snapshot timestamp in the URL.
            wm = re.search(r"web\.archive\.org/web/(\d{4})(\d{2})(\d{2})",
                           url)
            if wm:
                published = "%s-%s-%sT00:00:00+00:00" % wm.groups()
                notes.append("[%s] date from Wayback snapshot: %s"
                             % (title[:60], published))
            else:
                notes.append("excluded (no publish date): %s" % url)
                done_urls.add(url)
                _save_progress()
                continue
        # Classify: byline author, not just a photo credit.
        if not classify_byline(body_html):
            notes.append("excluded (not a byline): %s" % url)
            done_urls.add(url)
            _save_progress()
            continue
        # Tag this article's notes with its title for the review file.
        notes.append("=== %s [%s] ===" % (title, outlet))
        # Photos: Logan-credited figure/caption units only.
        logan_photos = find_logan_photos(body_html, url)
        # Conform.
        body = conform_body(body_html, notes, logan_photos, img_cache, outlet)
        # AP style.
        body = ap_normalize(body, notes)
        # Footer.
        repubs = authory_multi.get(title.lower(), [])
        body += "\n" + make_footer(outlet, url, repubs, notes)
        post, slug = emit_post(outlet, title, body, url, published, notes,
                               img_cache, slug_log, logan_photos, used_slugs)
        posts.append(post)
        for m in re.finditer(r"content/images/([^\"]+)", post["html"]):
            referenced_images.add(m.group(1))
        referenced_images.add(post["feature_image"].split(
            "content/images/")[-1])
        print("  + %s: %s" % (outlet, title[:70]))
        done_urls.add(url)
        _save_progress()

    ghost = build_ghost_json(posts)
    json_bytes = json.dumps(ghost, ensure_ascii=False).encode("utf-8")
    json_name = "idahoreports-loganfinney.ghost.json"
    (out_dir / json_name).write_bytes(json_bytes)
    zip_path = write_zip(out_dir, json_name, json_bytes, referenced_images)
    # Build notes (AP flags, exclusions, conversions) go to a review file
    # alongside the output -- manual-rephrase flags live here.
    notes_path = out_dir / "build-notes.txt"
    notes_path.write_text("\n".join(notes) + "\n", encoding="utf-8")
    print("Wrote %d posts -> %s (%d images in zip)" %
          (len(posts), zip_path.name, len(referenced_images)))
    print("Wrote %d build notes -> %s" % (len(notes), notes_path.name))
    # Clean up progress file on successful completion.
    if progress_path.exists():
        progress_path.unlink()


if __name__ == "__main__":
    main()
