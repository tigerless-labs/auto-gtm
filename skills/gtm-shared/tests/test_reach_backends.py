import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "scripts" / "reach"))
import backends  # noqa: E402


class FakeProc:
    def __init__(self, returncode=0, stdout="", stderr=""):
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = stderr


def runner_returning(proc):
    calls = []

    def _runner(cmd):
        calls.append(cmd)
        return proc

    _runner.calls = calls
    return _runner


class ReadOnlyWhitelist(unittest.TestCase):
    def test_write_commands_are_refused(self):
        for cmd in ("comment", "upvote", "save", "subscribe", "logout"):
            with self.assertRaises(ValueError, msg=cmd):
                backends.reddit_fetch(cmd, ["x"], runner=runner_returning(FakeProc()))

    def test_unknown_command_refused(self):
        with self.assertRaises(ValueError):
            backends.reddit_fetch("delete-account", runner=runner_returning(FakeProc()))

    def test_whitelisted_command_runs(self):
        runner = runner_returning(FakeProc(stdout="subscribers: 42"))
        out = backends.reddit_fetch("sub-info", ["ClaudeCode", "--yaml"], runner=runner)
        self.assertIn("subscribers", out)
        self.assertEqual(runner.calls[0][:2], ["rdt", "sub-info"])

    def test_refused_command_never_invokes_runner(self):
        runner = runner_returning(FakeProc())
        try:
            backends.reddit_fetch("comment", ["t3_x", "hi"], runner=runner)
        except ValueError:
            pass
        self.assertEqual(runner.calls, [])  # nothing shelled out

    def test_nonzero_exit_is_best_effort_none(self):
        runner = runner_returning(FakeProc(returncode=1, stderr="boom"))
        self.assertIsNone(backends.reddit_fetch("search", ["q"], runner=runner))

    def test_missing_binary_is_best_effort_none(self):
        def boom(cmd):
            raise FileNotFoundError("rdt")
        self.assertIsNone(backends.reddit_fetch("search", ["q"], runner=boom))


class RedditAvailability(unittest.TestCase):
    def test_authenticated_true(self):
        runner = runner_returning(FakeProc(stdout='  "authenticated": !!bool "true"'))
        self.assertTrue(backends.reddit_available(runner=runner))

    def test_authenticated_false(self):
        runner = runner_returning(FakeProc(stdout='  "authenticated": !!bool "false"'))
        self.assertFalse(backends.reddit_available(runner=runner))

    def test_missing_binary_is_false(self):
        def boom(cmd):
            raise FileNotFoundError("rdt")

        self.assertFalse(backends.reddit_available(runner=boom))


class XAvailability(unittest.TestCase):
    def test_available_when_importable(self):
        self.assertTrue(backends.x_available(importer=lambda: object()))

    def test_unavailable_when_not_importable(self):
        self.assertFalse(backends.x_available(importer=lambda: None))


class MissingDependencyHints(unittest.TestCase):
    def test_x_missing_names_twscrape(self):
        a = backends.x_available(importer=lambda: None)
        self.assertFalse(a)
        self.assertEqual(a.missing, "twscrape")

    def test_x_present_has_no_missing(self):
        a = backends.x_available(importer=lambda: object())
        self.assertTrue(a)
        self.assertIsNone(a.missing)

    def test_reddit_missing_binary_names_rdt(self):
        def boom(cmd):
            raise FileNotFoundError("rdt")

        a = backends.reddit_available(runner=boom)
        self.assertFalse(a)
        self.assertEqual(a.missing, "rdt")

    def test_reddit_present_but_unauthenticated_needs_login_not_install(self):
        runner = runner_returning(FakeProc(stdout='  "authenticated": !!bool "false"'))
        a = backends.reddit_available(runner=runner)
        self.assertFalse(a)
        self.assertIsNone(a.missing)
        self.assertEqual(a.login, "rdt login")

    def test_reddit_authenticated_has_no_hints(self):
        runner = runner_returning(FakeProc(stdout='  "authenticated": !!bool "true"'))
        a = backends.reddit_available(runner=runner)
        self.assertTrue(a)
        self.assertIsNone(a.missing)
        self.assertIsNone(a.login)


class _FakeUser:
    username = "swyx"


class _FakeTweet:
    def __init__(self, i):
        self.id = i
        self.id_str = f"t{i}"
        self.rawContent = f"tweet {i}"
        self.user = _FakeUser()
        self.likeCount = i
        self.retweetCount = 0
        self.replyCount = 0
        self.viewCount = 10
        self.date = "2026-07-24"
        self.url = f"https://x.com/swyx/status/{i}"


class _FakePool:
    def __init__(self):
        self.added = None

    async def add_account(self, username, password, email, email_password, cookies=None):
        self.added = {"username": username, "cookies": cookies}


class _FakeApi:
    def __init__(self, n=3):
        self._n = n
        self.pool = _FakePool()
        self.searched = None

    async def search(self, q, limit=-1, kv=None):
        self.searched = (q, limit)
        for i in range(self._n):
            yield _FakeTweet(i)


class XJinaReader(unittest.TestCase):
    def test_builds_jina_url_and_returns_text(self):
        captured = {}

        def getter(url, timeout=25):
            captured["url"] = url
            return "TWEET TEXT + conversation"

        out = backends.x_read_jina("https://x.com/swyx/status/1", getter=getter)
        self.assertEqual(captured["url"], "https://r.jina.ai/https://x.com/swyx/status/1")
        self.assertIn("TWEET TEXT", out)

    def test_best_effort_empty_on_failure(self):
        self.assertEqual(backends.x_read_jina("https://x.com/x/status/1", getter=lambda u, timeout=25: ""), "")


class XFetch(unittest.TestCase):
    def test_requires_auth_cookies(self):
        with self.assertRaises(ValueError):
            backends.x_fetch("q", {"ct0": "C"}, api_factory=lambda: _FakeApi())  # no auth_token

    def test_search_wires_cookies_and_normalizes(self):
        fake = _FakeApi(n=3)
        out = backends.x_fetch(
            "agent eval", {"auth_token": "AT", "ct0": "C"},
            limit=10, api_factory=lambda: fake,
        )
        self.assertEqual(fake.pool.added["cookies"], "auth_token=AT; ct0=C")
        self.assertEqual(fake.searched, ("agent eval", 10))
        self.assertEqual(out[0]["author"], "swyx")
        self.assertEqual(out[0]["text"], "tweet 0")
        self.assertIn("likes", out[0])
        self.assertTrue(out[0]["url"].startswith("https://x.com/"))

    def test_limit_caps_results(self):
        fake = _FakeApi(n=50)
        out = backends.x_fetch("q", {"auth_token": "A", "ct0": "C"}, limit=5, api_factory=lambda: fake)
        self.assertEqual(len(out), 5)


if __name__ == "__main__":
    unittest.main()
