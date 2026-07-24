#!/usr/bin/env python3
"""OS-aware browser-cookie sourcing for the auth-first data layer.

Firefox works on every OS (plain-SQLite `cookies.sqlite`), so it is the first
source everywhere. Chromium (Chrome/Brave/Edge) is auto-extractable on
macOS/Linux only; on Windows its v20 app-bound encryption defeats legitimate
extraction, so the Windows source order is Firefox-only and Chromium must be
supplied manually. Stdlib only; Chromium extraction, when attempted, is
delegated to an optional helper and yields nothing when it is unavailable.

Cookie VALUES are returned to the caller for use as an auth session; they are
never logged, printed, or persisted by this module.
"""
import shutil
import sqlite3
import sys
import tempfile
from pathlib import Path


def current_os():
    if sys.platform.startswith("win"):
        return "windows"
    if sys.platform == "darwin":
        return "macos"
    return "linux"


def cookie_source_order(os_name=None):
    os_name = os_name or current_os()
    if os_name == "windows":
        return ["firefox"]
    return ["firefox", "chromium"]


def _domain_matches(host, domain):
    host = (host or "").lstrip(".").lower()
    domain = domain.lower()
    return host == domain or host.endswith("." + domain)


def read_firefox_cookies(domain, db_path):
    """Return {name: value} for `domain` from one Firefox cookies.sqlite.

    Reads through a temp copy so a live (locked/WAL) profile DB still works.
    """
    tmp = Path(tempfile.mkdtemp()) / "cookies.sqlite"
    try:
        shutil.copy2(db_path, tmp)
        con = sqlite3.connect(f"file:{tmp}?mode=ro", uri=True)
        try:
            rows = con.execute("SELECT host, name, value FROM moz_cookies").fetchall()
        finally:
            con.close()
    except (sqlite3.Error, OSError):
        return {}
    finally:
        shutil.rmtree(tmp.parent, ignore_errors=True)
    return {name: value for host, name, value in rows if _domain_matches(host, domain)}


def _firefox_cookie_dbs(root=None):
    if root is not None:
        yield from sorted(Path(root).rglob("cookies.sqlite"))
        return
    home = Path.home()
    roots = [
        home / ".mozilla" / "firefox",                                  # Linux
        home / "Library" / "Application Support" / "Firefox" / "Profiles",  # macOS
        home / "AppData" / "Roaming" / "Mozilla" / "Firefox" / "Profiles",  # Windows
    ]
    for base in roots:
        if base.exists():
            yield from sorted(base.rglob("cookies.sqlite"))


def firefox_cookies(domain, root=None):
    for db in _firefox_cookie_dbs(root):
        cookies = read_firefox_cookies(domain, str(db))
        if cookies:
            return cookies
    return {}


def chromium_cookies(domain):
    """Best-effort Chromium extraction, delegated to an optional helper.

    Returns {} when no extractor is importable (and always on Windows, where
    v20 app-bound encryption is not legitimately extractable).
    """
    if current_os() == "windows":
        return {}
    try:
        import browser_cookie3  # optional dependency
    except ImportError:
        return {}
    try:
        jar = browser_cookie3.chrome(domain_name=domain)
        return {c.name: c.value for c in jar}
    except Exception:
        return {}


def get_cookies(domain, order=None, firefox_root=None):
    """Return (source, {name: value}) from the first source that has cookies."""
    for src in (order or cookie_source_order()):
        if src == "firefox":
            cookies = firefox_cookies(domain, root=firefox_root)
        elif src == "chromium":
            cookies = chromium_cookies(domain)
        else:
            cookies = {}
        if cookies:
            return src, cookies
    return "", {}
