#!/usr/bin/env python3
"""Keyless Reddit composite — OPT-IN, higher compliance risk.

Unauthenticated reads of Reddit's shreddit SVC endpoints + per-sub listing RSS
+ the arctic-shift archive. Rich (real upvote scores and comment counts) and
login-free, BUT it is unauthenticated scraping of endpoints Reddit is actively
litigating over — so it is OFF by default and gated by an explicit opt-in in the
data-layer config. Prefer the authenticated path (rdt / PRAW) unless the user
knowingly enables this.

Best-effort: every probe returns [] / {} on failure and never raises. All
network access goes through the shared token bucket (5 req/s, burst 5).

Surfaces (verified live 2026-07): shreddit listing 200 (real score +
comment-count), per-sub listing RSS 200, arctic 200; global search.rss is now
429-throttled, so the query lane is unreliable while the sub lane is strong.
"""
import html as _html
import re
import sys
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ratelimit import shared_bucket  # noqa: E402

_UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/131.0 Safari/537.36"
)
_LISTING = "https://www.reddit.com/svc/shreddit/community-more-posts/{sort}/?name={sub}"
_COMMENTS = "https://www.reddit.com/svc/shreddit/comments/r/{sub}/{t3}?sort=top"
_SUB_RSS = "https://www.reddit.com/r/{sub}/{sort}.rss?t=month"
_SEARCH_RSS = "https://www.reddit.com/search.rss?q={q}"
_ARCTIC = "https://arctic-shift.photon-reddit.com/api/posts/ids?ids={ids}"


def _get(url, timeout=20):
    shared_bucket().acquire()
    req = urllib.request.Request(url, headers={"User-Agent": _UA})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.read().decode("utf-8", "replace")
    except Exception:
        return ""


def _attr(tag, name):
    m = re.search(name + r'="([^"]*)"', tag)
    return m.group(1) if m else None


def _int(v):
    try:
        return int(v)
    except (TypeError, ValueError):
        return None


_POST_TAG = re.compile(r"<shreddit-post\b[^>]*>", re.I)
_COMMENT_TAG = re.compile(r"<shreddit-comment\b[^>]*>", re.I)


def parse_listing(html_text):
    """Parse a shreddit listing/HTML into posts with real scores. Pure.

    The listing repeats a `<shreddit-post>` shell per post (multiple view
    contexts); dedupe by post id, keeping the richest entry (one with a title).
    """
    seen = {}
    for tag in _POST_TAG.findall(html_text):
        pid = re.search(r'\bid="(t3_[^"]+)"', tag)
        if not pid:
            continue
        pid = pid.group(1)
        title = _attr(tag, "post-title")
        entry = {
            "id": pid,
            "title": _html.unescape(title) if title else None,
            "score": _int(_attr(tag, "score")),
            "comments": _int(_attr(tag, "comment-count")),
            "permalink": _attr(tag, "permalink"),
            "author": _attr(tag, "author"),
            "subreddit": _attr(tag, "subreddit-prefixed-name"),
        }
        if pid not in seen or (title and not seen[pid]["title"]):
            seen[pid] = entry
    return list(seen.values())


def parse_comments(html_text, limit=10):
    """Parse shreddit comment tags into {author, score, depth, permalink}. Pure.

    Bodies are intentionally not extracted here (fragile HTML); the authenticated
    path (rdt) is the source for full comment text.
    """
    out = []
    for tag in _COMMENT_TAG.findall(html_text):
        out.append({
            "author": _attr(tag, "author"),
            "score": _int(_attr(tag, "score")),
            "depth": _int(_attr(tag, "depth")),
            "permalink": _attr(tag, "permalink"),
        })
        if len(out) >= limit:
            break
    return out


def parse_rss(xml_text):
    """Parse a Reddit RSS/Atom feed into posts (breadth; no scores). Pure."""
    posts = []
    for m in re.finditer(r"<entry\b.*?</entry>", xml_text, re.S | re.I):
        entry = m.group(0)
        link = re.search(r'<link[^>]*href="([^"]+)"', entry)
        title = re.search(r"<title[^>]*>(.*?)</title>", entry, re.S)
        ident = re.search(r"<id>[^<]*?(t3_[A-Za-z0-9]+)", entry)
        perma = link.group(1) if link else None
        if not ident and perma:
            slug = re.search(r"/comments/([a-z0-9]+)/", perma)
            ident = ("t3_" + slug.group(1)) if slug else None
        else:
            ident = ident.group(1) if ident else None
        posts.append({
            "id": ident,
            "title": _html.unescape(title.group(1).strip()) if title else None,
            "permalink": perma,
            "score": None,
        })
    return posts


def shreddit_listing(sub, sort="hot", limit=25, getter=_get):
    posts = [p for p in parse_listing(getter(_LISTING.format(sort=sort, sub=sub))) if p["title"]]
    return posts[:limit]


def shreddit_comments(sub, t3_id, limit=10, getter=_get):
    return parse_comments(getter(_COMMENTS.format(sub=sub, t3=t3_id)), limit=limit)


def arctic_scores(ids, getter=_get):
    """Backfill {t3_id: score} from arctic-shift for base36 ids. Best-effort."""
    if not ids:
        return {}
    base36 = [i.split("_", 1)[-1] for i in ids]
    text = getter(_ARCTIC.format(ids=",".join(base36)))
    scores = {}
    for m in re.finditer(r'"id"\s*:\s*"([a-z0-9]+)".*?"score"\s*:\s*(\d+)', text, re.S):
        scores["t3_" + m.group(1)] = int(m.group(2))
    return scores


def keyless_reddit(sub=None, query=None, sort="hot", limit=25, getter=_get):
    """Composite: per-sub listing (scored, strong) or global RSS search (breadth,
    arctic-backfilled, currently throttled). Best-effort — [] on total failure."""
    if sub:
        posts = shreddit_listing(sub, sort=sort, limit=limit, getter=getter)
        if posts:
            return posts
    if query:
        from urllib.parse import quote_plus
        posts = parse_rss(getter(_SEARCH_RSS.format(q=quote_plus(query))))
        ids = [p["id"] for p in posts if p.get("id")]
        scores = arctic_scores(ids, getter=getter) if ids else {}
        for p in posts:
            if not p.get("score") and p["id"] in scores:
                p["score"] = scores[p["id"]]
        return posts[:limit]
    return []
