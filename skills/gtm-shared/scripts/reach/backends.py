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


# ----------------------------------------------------------------- X / twscrape
#
# twscrape is the working X backend as of 2026-07: twikit 2.3.3 (latest) fails
# X's anti-bot client-transaction-id handshake ("Couldn't get KEY_BYTE indices"),
# while twscrape returns live results from the same auth_token+ct0 cookies. Both
# are named in the design; empirically twscrape is the one that works now.

def _import_twscrape():
    try:
        import twscrape  # optional dependency
        return twscrape
    except ImportError:
        return None


def x_available(importer=None):
    """True when the twscrape library is importable (X authenticated path)."""
    imp = importer or _import_twscrape
    return imp() is not None


def _normalize_tweet(t):
    user = getattr(t, "user", None)
    return {
        "id": getattr(t, "id_str", None) or str(getattr(t, "id", "")),
        "text": getattr(t, "rawContent", None),
        "author": getattr(user, "username", None),
        "likes": getattr(t, "likeCount", None),
        "retweets": getattr(t, "retweetCount", None),
        "replies": getattr(t, "replyCount", None),
        "views": getattr(t, "viewCount", None),
        "created_at": str(getattr(t, "date", "")) or None,
        "url": getattr(t, "url", None),
    }


async def _x_search(api, cookie_str, query, limit):
    # Cookie-only account (active immediately, no login); read-only search.
    await api.pool.add_account("auto-gtm", "-", "auto-gtm@local", "-", cookies=cookie_str)
    out = []
    async for t in api.search(query, limit=limit):
        out.append(_normalize_tweet(t))
        if len(out) >= limit:
            break
    return out


def _default_x_api(db_path):
    from twscrape import API
    return API(db_path)


def x_fetch(query, cookies, limit=20, api_factory=None):
    """Authenticated X search via twscrape — read-only (search only, never posts).

    `cookies` is a {name: value} dict from session sourcing; auth_token + ct0 are
    required. `api_factory` (callable -> twscrape API) is injectable for tests;
    the default uses a throwaway accounts DB so the current cookies are always
    the ones used. Returns a list of normalized tweet dicts.
    """
    import asyncio
    import os
    import tempfile

    auth, ct0 = cookies.get("auth_token"), cookies.get("ct0")
    if not (auth and ct0):
        raise ValueError("missing X auth cookies (auth_token + ct0)")
    cookie_str = f"auth_token={auth}; ct0={ct0}"

    if api_factory is not None:
        return asyncio.run(_x_search(api_factory(), cookie_str, query, limit))

    fd, db = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    try:
        return asyncio.run(_x_search(_default_x_api(db), cookie_str, query, limit))
    finally:
        for path in (db, db + "-wal", db + "-shm"):
            try:
                os.remove(path)
            except OSError:
                pass
