#!/usr/bin/env python3
"""Pull the follow-builders daily feeds (X + blogs + podcasts) and print a compact digest.

Fetches three public JSON feeds from zarazhangrui/follow-builders (MIT-declared, keyless):
feed-x.json, feed-blogs.json, feed-podcasts.json. Each is already recency-scoped upstream
(X ~24h, blogs ~72h, podcasts ~14d), so this prints whatever the feeds carry — no extra
time filter. Self-contained: Python 3 stdlib only, no API key, no external skill, no config.

The caller (topic-scout) applies its own concise digest instruction to this output. On a
total fetch failure (all three feeds unreachable) it exits non-zero so the caller can fall
back to keyless search.

Long bodies (podcast transcripts, blog articles) are passed through in full by default —
the caller's digest instruction needs the whole text to summarize from. --max-chars caps
each body when a compact dump is wanted.

Usage:
  fetch_builder_report.py                       # all three feeds, everything recent, full bodies
  fetch_builder_report.py --query "agent eval"  # keep only items matching ANY term
  fetch_builder_report.py --max-chars 600       # cap each long body at 600 chars
  fetch_builder_report.py --feed-dir ./fixtures # read local feed files (offline / tests)
"""
import argparse
import json
import os
import sys
import urllib.request

FEEDS = {
    "x": "https://raw.githubusercontent.com/zarazhangrui/follow-builders/main/feed-x.json",
    "blogs": "https://raw.githubusercontent.com/zarazhangrui/follow-builders/main/feed-blogs.json",
    "podcasts": "https://raw.githubusercontent.com/zarazhangrui/follow-builders/main/feed-podcasts.json",
}


def load_feed(key, feed_dir):
    if feed_dir:
        path = os.path.join(feed_dir, f"feed-{key}.json")
        try:
            with open(path, encoding="utf-8") as handle:
                return json.load(handle)
        except (OSError, ValueError):
            return None
    req = urllib.request.Request(FEEDS[key], headers={"User-Agent": "auto-gtm-topic-scout"})
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            return json.load(resp)
    except Exception:
        return None


def matches(text, terms):
    if not terms:
        return True
    blob = text.lower()
    return any(term in blob for term in terms)


def body(text, max_chars):
    text = (text or "").strip()
    if not max_chars:
        return text
    return " ".join(text.split())[:max_chars]


def render_x(feed, terms, out):
    kept = 0
    lines = ["## X / Twitter"]
    for builder in feed.get("x", []):
        rows = [tw for tw in builder.get("tweets", []) if matches(tw.get("text", ""), terms)]
        if not rows:
            continue
        kept += len(rows)
        lines.append(f"\n### {builder.get('name')} ({builder.get('handle')})")
        for tw in rows:
            lines.append(f"- [{tw.get('createdAt')} · {tw.get('likes', 0)}♥] {(tw.get('text') or '').strip()}")
            lines.append(f"  {tw.get('url')}")
    if kept == 0:
        lines.append("(none)")
    out.extend(lines)
    return kept


def render_blogs(feed, terms, max_chars, out):
    kept = 0
    lines = ["\n## Official blogs"]
    for post in feed.get("blogs", []):
        haystack = " ".join(str(post.get(k, "")) for k in ("title", "description", "content"))
        if not matches(haystack, terms):
            continue
        kept += 1
        author = post.get("author")
        head = f"\n### {post.get('name')} — {post.get('title')}"
        lines.append(head)
        lines.append(f"{post.get('publishedAt')}" + (f" · {author}" if author else ""))
        text = body(post.get("content") or post.get("description"), max_chars)
        if text:
            lines.append(text)
        lines.append(f"{post.get('url')}")
    if kept == 0:
        lines.append("(none)")
    out.extend(lines)
    return kept


def render_podcasts(feed, terms, max_chars, out):
    kept = 0
    lines = ["\n## Podcasts"]
    for ep in feed.get("podcasts", []):
        haystack = " ".join(str(ep.get(k, "")) for k in ("title", "transcript"))
        if not matches(haystack, terms):
            continue
        kept += 1
        lines.append(f"\n### {ep.get('name')} — {ep.get('title')}")
        lines.append(f"{ep.get('publishedAt')}")
        text = body(ep.get("transcript"), max_chars)
        if text:
            lines.append(text)
        lines.append(f"{ep.get('url')}")
    if kept == 0:
        lines.append("(none)")
    out.extend(lines)
    return kept


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--query", default="", help="space-separated terms; keep items matching ANY (case-insensitive)")
    ap.add_argument("--max-chars", type=int, default=0, help="cap each long body (transcript, article) at N chars; 0 = full text")
    ap.add_argument("--feed-dir", default="", help="read feed-*.json from this directory instead of the network")
    args = ap.parse_args()

    feeds = {key: load_feed(key, args.feed_dir) for key in FEEDS}
    if all(feed is None for feed in feeds.values()):
        where = args.feed_dir or "network"
        print(f"ERROR: could not load any follow-builders feed from {where}. Fall back to keyless search.", file=sys.stderr)
        return 1

    terms = [t.lower() for t in args.query.split()]
    gens = " ".join(f"{k}:{(feeds[k] or {}).get('generatedAt')}" for k in FEEDS)
    header = f"# Builder digest — recent — {gens}"
    if terms:
        header += f" — filter: any of {terms}"

    out = [header]
    total = 0
    total += render_x(feeds["x"] or {}, terms, out)
    total += render_blogs(feeds["blogs"] or {}, terms, args.max_chars, out)
    total += render_podcasts(feeds["podcasts"] or {}, terms, args.max_chars, out)
    print("\n".join(out))
    if total == 0:
        print("\n(no items matched — drop --query or fall back to keyless search)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
