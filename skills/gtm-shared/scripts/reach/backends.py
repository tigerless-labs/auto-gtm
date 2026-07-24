#!/usr/bin/env python3
"""Authenticated read backends for the data layer.

Reddit: `rdt` (login-state CLI). The read-only command whitelist from
rdt-readonly.md is enforced here in code — a write command (comment/upvote/
subscribe/…) is refused at this layer, not merely by convention.

X: `twikit` (optional import) — used when present; otherwise the caller
degrades to the keyless floor. The twikit fetch body is not yet wired (it needs
twikit present to verify), so this module exposes availability detection only.

Read-only and drafts-only throughout. Stdlib only (twikit is an optional import).
"""
import subprocess

RDT_READ_WHITELIST = {
    "status", "search", "read", "sub", "sub-info", "popular",
    "all", "user", "user-posts", "user-comments", "export",
}
RDT_WRITE_DENY = {"comment", "upvote", "save", "subscribe", "logout"}


def _run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)


# ---------------------------------------------------------------- Reddit / rdt

def reddit_available(runner=_run):
    """True when `rdt` reports an authenticated session."""
    try:
        r = runner(["rdt", "status", "--yaml"])
    except (FileNotFoundError, OSError):
        return False
    if r.returncode != 0:
        return False
    for line in (r.stdout or "").splitlines():
        low = line.lower()
        if "authenticated" in low and "true" in low:
            return True
    return False


def reddit_fetch(command, args=None, runner=_run):
    """Run a whitelisted read-only `rdt` command and return its stdout.

    Refuses any command outside RDT_READ_WHITELIST — the drafts-only guardrail
    is enforced here, so a write command can never be issued through reach.
    """
    if command not in RDT_READ_WHITELIST:
        raise ValueError(f"refused non-whitelisted rdt command: {command!r}")
    r = runner(["rdt", command, *(args or [])])
    if r.returncode != 0:
        raise RuntimeError(f"rdt {command} failed: {(r.stderr or '').strip()[:200]}")
    return r.stdout


# ------------------------------------------------------------------- X / twikit

def _import_twikit():
    try:
        import twikit  # optional dependency
        return twikit
    except ImportError:
        return None


def x_available(importer=None):
    """True when the twikit library is importable (X authenticated path)."""
    imp = importer or _import_twikit
    return imp() is not None


X_SEARCH_PRODUCTS = ("Top", "Latest", "Media")


def _default_x_client(language="en-US"):
    import twikit
    return twikit.Client(language)


def _normalize_tweet(t):
    user = getattr(t, "user", None)
    return {
        "id": getattr(t, "id", None),
        "text": getattr(t, "text", None) or getattr(t, "full_text", None),
        "author": getattr(user, "screen_name", None),
        "likes": getattr(t, "favorite_count", None),
        "retweets": getattr(t, "retweet_count", None),
        "replies": getattr(t, "reply_count", None),
        "created_at": getattr(t, "created_at", None),
    }


def x_fetch(query, cookies, product="Latest", count=20, client_factory=None):
    """Authenticated X search via twikit — read-only (search only).

    `cookies` is a {name: value} dict from session sourcing (auth_token + ct0).
    `client_factory` is injectable for tests; the default builds a real twikit
    client. Returns a list of normalized tweet dicts. Never posts or mutates.
    """
    if product not in X_SEARCH_PRODUCTS:
        raise ValueError(f"invalid search product: {product!r}")
    import asyncio

    client = (client_factory or _default_x_client)()
    client.set_cookies(cookies)
    result = asyncio.run(client.search_tweet(query, product, count))
    return [_normalize_tweet(t) for t in result][:count]
