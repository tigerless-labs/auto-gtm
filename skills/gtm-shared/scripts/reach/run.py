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
import backends  # noqa: E402

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
    "install": {
        "twscrape": "pip install twscrape",
        "rdt": "pipx install 'git+https://github.com/public-clis/rdt-cli.git'",
        "browser_cookie3": "pip install browser_cookie3",
    },
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
    merged["install"].update(data.get("install") or {})
    return merged


def platform_config(platform):
    cfg = _load_config()
    p = cfg["platforms"].get(platform)
    if p is None:
        raise KeyError(f"unknown platform: {platform}")
    return p


def plan_fetch(platform, available):
    """Ordered tiers to attempt. Authenticated first; then a platform-specific
    keyless tier (Reddit composite when opted in, X jina reader); the WebSearch
    floor is always last and marked approximate so it can never be mistaken for
    full coverage."""
    p = platform_config(platform)
    tiers = []
    if available.get("authenticated"):
        tiers.append({"tier": "authenticated", "backend": p["primary"], "approximate": False})
    if platform == "reddit" and p.get("keyless_composite"):
        # OPT-IN: unauthenticated shreddit/RSS/arctic scraping (higher compliance risk).
        tiers.append({"tier": "keyless-composite", "backend": "shreddit", "approximate": True})
    if platform == "x" and p.get("jina_reader", True):
        # Floor for a KNOWN tweet URL (X has no keyless search); content egress to jina.ai.
        tiers.append({"tier": "jina-reader", "backend": "r.jina.ai", "approximate": True, "url_only": True})
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


def _backend_availability(platform):
    if platform == "reddit":
        return backends.reddit_available()
    if platform == "x":
        return backends.x_available()
    return backends.Availability(True)


def missing_dependencies(platform, availability=None, chromium_available=None, sources=None):
    """Installable dependencies currently blocking a tier, in install order.

    Empty when the platform is already authenticated. The Chromium cookie
    helper is only reported when Chromium is in this OS's cookie source order.
    All three probes are injectable for tests.
    """
    a = availability if availability is not None else _backend_availability(platform)
    if a:
        return []
    missing = []
    if getattr(a, "missing", None):
        missing.append(a.missing)
    chrom_ok = (chromium_available if chromium_available is not None
                else session.chromium_extractor_available())
    if "chromium" in (sources or session.cookie_source_order()) and not chrom_ok:
        missing.append("browser_cookie3")
    return missing


def install_hints(missing):
    """Map missing dependency names to exact agent-runnable install commands.

    The commands live in config (DEFAULTS + data-layer.json), never inline in
    skill prose. Unknown names are dropped rather than guessed."""
    commands = _load_config()["install"]
    return [{"dependency": d, "install": commands[d]} for d in missing if d in commands]


def status(platform, available, hints=None):
    # Reports the tier and any install hints — never cookie values or any auth material.
    tier = "authenticated" if available.get("authenticated") else "keyless-floor"
    line = f"{platform} via {tier}"
    if hints:
        needs = "; ".join(h["install"] for h in hints)
        line += f"  (missing: {', '.join(h['dependency'] for h in hints)} — install: {needs})"
    return line


def authenticated_available(platform, probe=None):
    """Whether an authenticated session can be built for this platform.

    `probe` (a callable domain->bool) is injectable for tests. By default,
    dispatch to the platform's backend: Reddit is authenticated when `rdt`
    reports a session or the browser holds reddit cookies; X is authenticated
    when twikit is importable and the browser holds x cookies.
    """
    p = platform_config(platform)
    if probe is not None:
        return bool(probe(p["domain"]))
    if platform == "reddit":
        return backends.reddit_available() or bool(session.get_cookies(p["domain"])[1])
    if platform == "x":
        return backends.x_available() and bool(session.get_cookies(p["domain"])[1])
    _src, cookies = session.get_cookies(p["domain"])
    return bool(cookies)


def _degrade(tier_failed, next_tier, install=None, login=None, reason=""):
    """A structured single-tier degrade signal. Carries what is missing, what to
    install, and which tier the AGENT should try next — never any cookie value.
    The agent (not this script) walks to `next`, since the floor is a host tool
    and installs pass through the permission gate."""
    return {
        "degrade": True,
        "tier_failed": tier_failed,
        "next": next_tier,
        "install": install or [],
        "login": login,
        "reason": reason,
    }


def fetch_x(query=None, tweet_url=None, limit=20,
            x_available=None, get_cookies=None, x_fetch=None, x_read_jina=None):
    """Execute ONE X tier and return {data,...} or a degrade signal.

    `--query` runs the authenticated twscrape search; `--tweet-url` runs the
    keyless jina reader on a known URL. Never loops tiers — on failure it hands
    back a degrade signal for the agent to act on."""
    x_available = x_available or backends.x_available
    get_cookies = get_cookies or session.get_cookies
    x_fetch = x_fetch or backends.x_fetch
    x_read_jina = x_read_jina or backends.x_read_jina

    if tweet_url:
        text = x_read_jina(tweet_url)
        if text:
            return {"platform": "x", "tier": "jina-reader", "approximate": True, "data": text}
        return _degrade("jina-reader", "keyless-floor", reason="jina returned nothing")

    av = x_available()
    if not av:
        return _degrade("authenticated", "keyless-floor",
                        install=install_hints([av.missing] if av.missing else []),
                        reason="twscrape not importable")
    _src, cookies = get_cookies("x.com")
    if not cookies.get("auth_token") or not cookies.get("ct0"):
        return _degrade("authenticated", "keyless-floor",
                        reason="no x.com cookie (log into x.com in your browser)")
    tweets = x_fetch(query, cookies, limit=limit)
    if not tweets:
        return _degrade("authenticated", "keyless-floor", reason="search returned nothing")
    return {"platform": "x", "tier": "authenticated", "approximate": False, "data": tweets}


def fetch_reddit(command, args=None, reddit_available=None, reddit_fetch=None):
    """Execute ONE Reddit tier: a whitelisted `rdt` read, through the
    code-enforced read-only whitelist. A write command raises regardless of
    availability (guardrail first); a missing/unauthenticated backend returns a
    degrade signal."""
    reddit_available = reddit_available or backends.reddit_available
    reddit_fetch = reddit_fetch or backends.reddit_fetch

    if command not in backends.RDT_READ_WHITELIST:
        raise ValueError(f"refused non-whitelisted rdt command: {command!r}")

    av = reddit_available()
    if not av:
        return _degrade("authenticated", "keyless-floor",
                        install=install_hints([av.missing] if av.missing else []),
                        login=av.login,
                        reason="rdt not installed" if av.missing else "rdt not authenticated")
    out = reddit_fetch(command, args)
    if out is None:
        return _degrade("authenticated", "keyless-floor", reason="rdt returned nothing")
    return {"platform": "reddit", "tier": "authenticated", "approximate": False, "data": out}


def _main_fetch_x(argv):
    ap = argparse.ArgumentParser(prog="run.py fetch-x", description="execute one X tier")
    ap.add_argument("--query")
    ap.add_argument("--tweet-url")
    ap.add_argument("--limit", type=int, default=20)
    a = ap.parse_args(argv)
    r = fetch_x(query=a.query, tweet_url=a.tweet_url, limit=a.limit)
    print(json.dumps(r))
    return 1 if r.get("degrade") else 0


def _main_fetch_reddit(argv):
    ap = argparse.ArgumentParser(prog="run.py fetch-reddit",
                                 description="execute one whitelisted rdt read")
    ap.add_argument("rdt_command")
    ap.add_argument("rdt_args", nargs=argparse.REMAINDER)
    a = ap.parse_args(argv)
    r = fetch_reddit(a.rdt_command, a.rdt_args)
    print(json.dumps(r))
    return 1 if r.get("degrade") else 0


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    if argv and argv[0] == "fetch-x":
        return _main_fetch_x(argv[1:])
    if argv and argv[0] == "fetch-reddit":
        return _main_fetch_reddit(argv[1:])

    ap = argparse.ArgumentParser(description="auth-first fetch planner")
    ap.add_argument("platform", choices=sorted(DEFAULTS["platforms"]))
    ap.add_argument("--json", action="store_true", help="machine-readable plan")
    args = ap.parse_args(argv)
    avail = {"authenticated": bool(authenticated_available(args.platform))}
    hints = [] if avail["authenticated"] else install_hints(missing_dependencies(args.platform))
    plan = plan_fetch(args.platform, avail)
    if args.json:
        print(json.dumps({"status": status(args.platform, avail, hints), "install": hints, "plan": plan}))
    else:
        print(status(args.platform, avail, hints))
        for t in plan:
            label = t.get("backend") or t.get("query")
            print(f"  - {t['tier']}: {label}" + ("  (approximate)" if t["approximate"] else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
