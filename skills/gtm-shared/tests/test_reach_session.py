import sqlite3
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "scripts" / "reach"))
import session  # noqa: E402


def make_firefox_db(path, rows):
    con = sqlite3.connect(str(path))
    con.execute(
        "CREATE TABLE moz_cookies "
        "(id INTEGER PRIMARY KEY, host TEXT, name TEXT, value TEXT)"
    )
    con.executemany(
        "INSERT INTO moz_cookies (host, name, value) VALUES (?, ?, ?)", rows
    )
    con.commit()
    con.close()


class OsSourceOrder(unittest.TestCase):
    def test_windows_is_firefox_only(self):
        # Chromium v20 app-bound encryption is not legitimately extractable.
        self.assertEqual(session.cookie_source_order("windows"), ["firefox"])

    def test_unix_prefers_firefox_then_chromium(self):
        self.assertEqual(session.cookie_source_order("macos"), ["firefox", "chromium"])
        self.assertEqual(session.cookie_source_order("linux"), ["firefox", "chromium"])

    def test_current_os_is_known(self):
        self.assertIn(session.current_os(), {"windows", "macos", "linux"})


class FirefoxReader(unittest.TestCase):
    def setUp(self):
        self.root = tempfile.mkdtemp()
        self.db = Path(self.root) / "profile.default" / "cookies.sqlite"
        self.db.parent.mkdir(parents=True)
        make_firefox_db(
            self.db,
            [
                (".reddit.com", "reddit_session", "RS-SECRET"),
                (".reddit.com", "token_v2", "TOK"),
                ("www.reddit.com", "csrf_token", "CSRF"),
                (".x.com", "auth_token", "AT"),
                (".x.com", "ct0", "CT0"),
                (".example.com", "foo", "bar"),
                ("notreddit.com", "trap", "TRAP"),
            ],
        )

    def test_reads_only_matching_domain(self):
        c = session.read_firefox_cookies("reddit.com", str(self.db))
        self.assertEqual(c.get("reddit_session"), "RS-SECRET")
        self.assertIn("token_v2", c)
        self.assertIn("csrf_token", c)
        self.assertNotIn("foo", c)      # example.com excluded
        self.assertNotIn("trap", c)     # notreddit.com must NOT match reddit.com

    def test_get_cookies_via_firefox_root(self):
        src, c = session.get_cookies("x.com", order=["firefox"], firefox_root=self.root)
        self.assertEqual(src, "firefox")
        self.assertEqual(c.get("auth_token"), "AT")
        self.assertEqual(c.get("ct0"), "CT0")

    def test_no_cookies_returns_empty(self):
        src, c = session.get_cookies(
            "nonexistent.tld", order=["firefox"], firefox_root=self.root
        )
        self.assertEqual((src, c), ("", {}))

    def test_locked_db_is_read_via_copy(self):
        # A concurrent reader must not fail on a WAL/locked live DB: reading
        # should go through a temp copy, so an open connection doesn't block it.
        live = sqlite3.connect(str(self.db))
        live.execute("BEGIN")  # hold a transaction open
        try:
            c = session.read_firefox_cookies("reddit.com", str(self.db))
            self.assertEqual(c.get("reddit_session"), "RS-SECRET")
        finally:
            live.rollback()
            live.close()


class ChromiumExtractorAvailability(unittest.TestCase):
    def test_missing_helper_reports_unavailable(self):
        self.assertFalse(session.chromium_extractor_available(importer=lambda: None))

    def test_present_helper_reports_available(self):
        self.assertTrue(session.chromium_extractor_available(importer=lambda: object()))


if __name__ == "__main__":
    unittest.main()
