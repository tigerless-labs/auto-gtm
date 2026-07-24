#!/usr/bin/env python3
"""Auth-first fetch orchestration for the auto-gtm data layer.

Encodes the fallback contract as code: try the authenticated tier; when it is
unavailable, hand back a clearly-labeled keyless-floor degrade signal. The
keyless floor itself (host WebSearch/WebFetch) is executed by the agent per the
data-layer contract — not here; this module covers the authenticated rungs and
the degrade decision.

Stdlib only. Knobs live in config/data-layer.json, with baked-in defaults so a
missing/invalid file never breaks a run. Cookie values never enter output.

Usage:
  run.py reddit           # human-readable plan for the current machine
  run.py x --json         # machine-readable {status, plan}
"""
import argparse
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import session  # noqa: E402

CONFIG_PATH = HERE.parent.parent / "config" / "data-layer.json"

DEFAULTS = {
    "platforms": {
        "x": {
            "domain": "x.com",
            "primary": "twikit",
            "floor_query": "site:x.com",
            "recency": {"topic": "~1 week", "reply": "same-day"},
        },
        "reddit": {
            "domain": "reddit.com",
            "primary": "cookie-session",
            "upgrade": "praw",
            "floor_query": "site:reddit.com",
            "recency": {"topic": "~1 week", "reply": "same-day"},
        },
    },
    "keyless_floor_enabled": True,
}


def _load_config():
    merged = json.loads(json.dumps(DEFAULTS))  # deep copy
    try:
        data = json.loads(CONFIG_PATH.read_text())
    except (FileNotFoundError, ValueError, OSError):
        return merged
    for name, patch in (data.get("platforms") or {}).items():
        merged["platforms"].setdefault(name, {}).update(patch)
    if "keyless_floor_enabled" in data:
        merged["keyless_floor_enabled"] = data["keyless_floor_enabled"]
    return merged


def platform_config(platform):
    cfg = _load_config()
    p = cfg["platforms"].get(platform)
    if p is None:
        raise KeyError(f"unknown platform: {platform}")
    return p


def plan_fetch(platform, available):
    """Ordered tiers to attempt. The keyless floor is always last and marked
    approximate so it can never be mistaken for full coverage."""
    p = platform_config(platform)
    tiers = []
    if available.get("authenticated"):
        tiers.append({"tier": "authenticated", "backend": p["primary"], "approximate": False})
    tiers.append({"tier": "keyless-floor", "query": p["floor_query"], "approximate": True})
    return tiers


def degrade_result(platform, reason=""):
    p = platform_config(platform)
    return {
        "source": "keyless-floor",
        "approximate": True,
        "platform": platform,
        "floor_query": p["floor_query"],
        "reason": reason,
    }


def status(platform, available):
    # Reports the tier only — never cookie values or any auth material.
    tier = "authenticated" if available.get("authenticated") else "keyless-floor"
    return f"{platform} via {tier}"


def authenticated_available(platform, probe=None):
    """Whether an authenticated session can be built for this platform.

    `probe` (a callable domain->bool) is injectable for tests; the default
    checks the user's own browser cookies via session sourcing.
    """
    p = platform_config(platform)
    if probe is not None:
        return bool(probe(p["domain"]))
    _src, cookies = session.get_cookies(p["domain"])
    return bool(cookies)


def main(argv=None):
    ap = argparse.ArgumentParser(description="auth-first fetch planner")
    ap.add_argument("platform", choices=sorted(DEFAULTS["platforms"]))
    ap.add_argument("--json", action="store_true", help="machine-readable plan")
    args = ap.parse_args(argv)
    avail = {"authenticated": authenticated_available(args.platform)}
    plan = plan_fetch(args.platform, avail)
    if args.json:
        print(json.dumps({"status": status(args.platform, avail), "plan": plan}))
    else:
        print(status(args.platform, avail))
        for t in plan:
            label = t.get("backend") or t.get("query")
            print(f"  - {t['tier']}: {label}" + ("  (approximate)" if t["approximate"] else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
