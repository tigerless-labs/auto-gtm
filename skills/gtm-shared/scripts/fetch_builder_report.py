#!/usr/bin/env python3
"""Pull the follow-builders daily X feed and print a compact, filterable digest.

Fetches https://raw.githubusercontent.com/zarazhangrui/follow-builders/main/feed-x.json
(the central daily report from zarazhangrui/follow-builders, MIT) and prints each
builder's recent tweets. Self-contained: Python 3 stdlib only, no API key, no
external skill, no config. On any network error it exits non-zero with a message
so the caller can fall back to WebSearch.

Usage:
  fetch_builder_report.py                 # all builders, last 24h
  fetch_builder_report.py --hours 24 --query "agent eval rag" --min-likes 20
"""
import argparse
import json
import sys
import urllib.request
from datetime import datetime, timezone, timedelta

FEED_URL = "https://raw.githubusercontent.com/zarazhangrui/follow-builders/main/feed-x.json"


def fetch(url, timeout=20):
    req = urllib.request.Request(url, headers={"User-Agent": "auto-gtm-topic-scout"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.load(resp)


def parse_dt(value):
    try:
        return datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except ValueError:
        return None


def as_int(value, default=0):
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--hours", type=int, default=24, help="keep tweets from the last N hours")
    ap.add_argument("--query", default="", help="space-separated terms; keep tweets matching ANY (case-insensitive)")
    ap.add_argument("--min-likes", type=int, default=0, help="drop tweets below this like count")
    args = ap.parse_args()

    try:
        data = fetch(FEED_URL)
    except Exception as exc:  # network, HTTP, JSON — all non-fatal to the skill
        print(f"ERROR: could not fetch follow-builders feed ({exc}). Fall back to WebSearch.", file=sys.stderr)
        return 1

    cutoff = datetime.now(timezone.utc) - timedelta(hours=args.hours)
    terms = [t.lower() for t in args.query.split()]

    header = f"# follow-builders feed — generatedAt {data.get('generatedAt')} — filter: last {args.hours}h"
    if terms:
        header += f", any of {terms}"
    if args.min_likes:
        header += f", >= {args.min_likes} likes"
    print(header)

    kept = 0
    for builder in data.get("x", []):
        rows = []
        for tw in builder.get("tweets", []):
            when = parse_dt(tw.get("createdAt"))
            if when and when < cutoff:
                continue
            if as_int(tw.get("likes")) < args.min_likes:
                continue
            text = (tw.get("text") or "").strip()
            if terms and not any(term in text.lower() for term in terms):
                continue
            rows.append(tw)
        if not rows:
            continue
        kept += len(rows)
        print(f"\n## {builder.get('name')} (@{builder.get('handle')})")
        for tw in rows:
            likes = as_int(tw.get("likes"))
            print(f"- [{tw.get('createdAt')} · {likes}♥] {(tw.get('text') or '').strip()}")
            print(f"  {tw.get('url')}")

    if kept == 0:
        print("\n(no tweets matched — widen --hours/--query or fall back to WebSearch)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
