import json
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "scripts" / "reach"))
import run  # noqa: E402
import backends  # noqa: E402


class FallbackOrder(unittest.TestCase):
    def test_authenticated_first_then_floor(self):
        tiers = run.plan_fetch("x", {"authenticated": True})
        self.assertEqual(tiers[0]["tier"], "authenticated")
        self.assertEqual(tiers[-1]["tier"], "keyless-floor")

    def test_floor_only_when_unauthenticated(self):
        tiers = run.plan_fetch("reddit", {"authenticated": False})
        self.assertEqual(len(tiers), 1)
        self.assertEqual(tiers[0]["tier"], "keyless-floor")

    def test_authenticated_tier_names_primary_backend(self):
        t = run.plan_fetch("reddit", {"authenticated": True})[0]
        self.assertEqual(t["backend"], "cookie-session")
        self.assertFalse(t["approximate"])


class KeylessTiers(unittest.TestCase):
    def test_x_has_jina_reader_between_auth_and_floor(self):
        tiers = run.plan_fetch("x", {"authenticated": True})
        names = [t["tier"] for t in tiers]
        self.assertEqual(names, ["authenticated", "jina-reader", "keyless-floor"])

    def test_reddit_composite_absent_by_default(self):
        # opt-in flag is off in config -> no composite tier
        tiers = run.plan_fetch("reddit", {"authenticated": True})
        self.assertNotIn("keyless-composite", [t["tier"] for t in tiers])

    def test_reddit_composite_present_when_opted_in(self):
        cfg = run._load_config()
        cfg["platforms"]["reddit"]["keyless_composite"] = True
        orig = run._load_config
        run._load_config = lambda: cfg
        try:
            tiers = run.plan_fetch("reddit", {"authenticated": True})
            names = [t["tier"] for t in tiers]
            self.assertEqual(names, ["authenticated", "keyless-composite", "keyless-floor"])
        finally:
            run._load_config = orig


class FloorInvariants(unittest.TestCase):
    def test_floor_is_always_approximate(self):
        # The floor must never be silently passed off as full coverage.
        for platform in ("x", "reddit"):
            for auth in (True, False):
                floor = run.plan_fetch(platform, {"authenticated": auth})[-1]
                self.assertTrue(floor["approximate"], (platform, auth))

    def test_degrade_result_labeled_approximate(self):
        r = run.degrade_result("reddit", reason="no session")
        self.assertTrue(r["approximate"])
        self.assertEqual(r["source"], "keyless-floor")
        self.assertTrue(r["floor_query"].startswith("site:reddit.com"))


class NoCredentialLeak(unittest.TestCase):
    def test_status_never_contains_cookie_values(self):
        s = run.status("reddit", {"authenticated": True, "_cookies": {"reddit_session": "SECRET"}})
        self.assertNotIn("SECRET", s)
        self.assertIn("reddit", s)

    def test_status_reports_tier(self):
        self.assertIn("keyless", run.status("x", {"authenticated": False}))
        self.assertIn("authenticated", run.status("x", {"authenticated": True}))


class AuthProbe(unittest.TestCase):
    def test_available_uses_injected_probe(self):
        self.assertTrue(run.authenticated_available("x", probe=lambda domain: True))
        self.assertFalse(run.authenticated_available("reddit", probe=lambda domain: False))

    def test_probe_receives_platform_domain(self):
        seen = {}
        run.authenticated_available("reddit", probe=lambda domain: seen.setdefault("d", domain))
        self.assertEqual(seen["d"], "reddit.com")


class _Availability:
    def __init__(self, ok, missing=None, login=None):
        self._ok = ok
        self.missing = missing
        self.login = login

    def __bool__(self):
        return self._ok


class InstallHints(unittest.TestCase):
    def test_known_dependencies_map_to_nonempty_install_commands(self):
        for dep in ("twscrape", "rdt", "browser_cookie3"):
            hints = run.install_hints([dep])
            self.assertEqual(len(hints), 1, dep)
            self.assertEqual(hints[0]["dependency"], dep)
            self.assertTrue(hints[0]["install"], dep)

    def test_unknown_dependency_yields_no_hint(self):
        self.assertEqual(run.install_hints(["left-pad"]), [])

    def test_missing_backend_dependency_is_collected(self):
        missing = run.missing_dependencies(
            "x", availability=_Availability(False, missing="twscrape"),
            chromium_available=True, sources=["firefox", "chromium"],
        )
        self.assertEqual(missing, ["twscrape"])

    def test_missing_chromium_helper_is_collected_when_in_source_order(self):
        missing = run.missing_dependencies(
            "x", availability=_Availability(False),
            chromium_available=False, sources=["firefox", "chromium"],
        )
        self.assertIn("browser_cookie3", missing)

    def test_chromium_helper_not_collected_outside_source_order(self):
        missing = run.missing_dependencies(
            "reddit", availability=_Availability(False, missing="rdt"),
            chromium_available=False, sources=["firefox"],
        )
        self.assertEqual(missing, ["rdt"])

    def test_nothing_missing_when_authenticated(self):
        missing = run.missing_dependencies(
            "reddit", availability=_Availability(True),
            chromium_available=False, sources=["firefox", "chromium"],
        )
        self.assertEqual(missing, [])

    def test_status_carries_install_hint_but_never_secrets(self):
        s = run.status(
            "x",
            {"authenticated": False, "_cookies": {"auth_token": "SECRET"}},
            hints=[{"dependency": "twscrape", "install": "pip install twscrape"}],
        )
        self.assertIn("twscrape", s)
        self.assertNotIn("SECRET", s)

    def test_hints_do_not_change_fallback_order(self):
        tiers = run.plan_fetch("x", {"authenticated": False})
        self.assertEqual(tiers[-1]["tier"], "keyless-floor")
        self.assertTrue(all(t["approximate"] for t in tiers))


class FetchXTier(unittest.TestCase):
    def test_authenticated_search_returns_tweets(self):
        r = run.fetch_x(
            query="agent eval", limit=5,
            x_available=lambda: backends.Availability(True),
            get_cookies=lambda d: ("firefox", {"auth_token": "A", "ct0": "C"}),
            x_fetch=lambda q, c, limit: [{"id": "t1", "text": "hi"}],
        )
        self.assertFalse(r.get("degrade"))
        self.assertEqual(r["tier"], "authenticated")
        self.assertFalse(r["approximate"])
        self.assertEqual(len(r["data"]), 1)

    def test_missing_twscrape_degrades_with_install_hint(self):
        r = run.fetch_x(
            query="q",
            x_available=lambda: backends.Availability(False, missing="twscrape"),
            get_cookies=lambda d: ("", {}),
            x_fetch=lambda *a, **k: [],
        )
        self.assertTrue(r["degrade"])
        self.assertIn("twscrape", [h["dependency"] for h in r["install"]])
        self.assertEqual(r["next"], "keyless-floor")

    def test_no_cookie_degrades_without_install(self):
        r = run.fetch_x(
            query="q",
            x_available=lambda: backends.Availability(True),
            get_cookies=lambda d: ("", {}),
            x_fetch=lambda *a, **k: [],
        )
        self.assertTrue(r["degrade"])
        self.assertEqual(r["install"], [])  # a browser login, not an install

    def test_tweet_url_uses_jina_reader(self):
        r = run.fetch_x(tweet_url="https://x.com/a/status/1", x_read_jina=lambda u: "TEXT")
        self.assertEqual(r["tier"], "jina-reader")
        self.assertTrue(r["approximate"])
        self.assertEqual(r["data"], "TEXT")

    def test_jina_empty_degrades_to_floor(self):
        r = run.fetch_x(tweet_url="u", x_read_jina=lambda u: "")
        self.assertTrue(r["degrade"])
        self.assertEqual(r["next"], "keyless-floor")

    def test_degrade_never_leaks_cookie_value(self):
        r = run.fetch_x(
            query="q",
            x_available=lambda: backends.Availability(True),
            get_cookies=lambda d: ("firefox", {"auth_token": "SECRET", "ct0": "C"}),
            x_fetch=lambda *a, **k: [],  # empty -> degrade
        )
        self.assertNotIn("SECRET", json.dumps(r))


class FetchRedditTier(unittest.TestCase):
    def test_whitelisted_passthrough(self):
        r = run.fetch_reddit(
            "search", ["q", "-t", "week"],
            reddit_available=lambda: backends.Availability(True),
            reddit_fetch=lambda cmd, args: "YAML OUT",
        )
        self.assertFalse(r.get("degrade"))
        self.assertEqual(r["tier"], "authenticated")
        self.assertEqual(r["data"], "YAML OUT")

    def test_write_command_refused_regardless_of_availability(self):
        for cmd in ("comment", "upvote", "subscribe"):
            with self.assertRaises(ValueError, msg=cmd):
                run.fetch_reddit(
                    cmd, ["x"],
                    reddit_available=lambda: backends.Availability(False, missing="rdt"),
                    reddit_fetch=lambda *a, **k: "should not run",
                )

    def test_missing_rdt_degrades_with_install(self):
        r = run.fetch_reddit(
            "search", ["q"],
            reddit_available=lambda: backends.Availability(False, missing="rdt"),
            reddit_fetch=lambda *a, **k: None,
        )
        self.assertTrue(r["degrade"])
        self.assertIn("rdt", [h["dependency"] for h in r["install"]])

    def test_unauthenticated_degrades_with_login(self):
        r = run.fetch_reddit(
            "search", ["q"],
            reddit_available=lambda: backends.Availability(False, login="rdt login"),
            reddit_fetch=lambda *a, **k: None,
        )
        self.assertTrue(r["degrade"])
        self.assertEqual(r["install"], [])
        self.assertEqual(r["login"], "rdt login")

    def test_runtime_none_degrades_to_floor(self):
        r = run.fetch_reddit(
            "read", ["t3_x"],
            reddit_available=lambda: backends.Availability(True),
            reddit_fetch=lambda cmd, args: None,  # rdt ran, empty
        )
        self.assertTrue(r["degrade"])
        self.assertEqual(r["next"], "keyless-floor")


class ConfigKnobs(unittest.TestCase):
    def test_platforms_have_floor_query(self):
        for platform in ("x", "reddit"):
            self.assertTrue(run.platform_config(platform)["floor_query"].startswith("site:"))

    def test_recency_window_present(self):
        self.assertIn("recency", run.platform_config("reddit"))

    def test_unknown_platform_raises(self):
        with self.assertRaises(KeyError):
            run.platform_config("linkedin")


if __name__ == "__main__":
    unittest.main()
