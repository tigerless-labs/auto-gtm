import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "scripts" / "reach"))
import run  # noqa: E402


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
