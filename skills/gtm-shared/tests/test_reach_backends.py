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

    def test_nonzero_exit_raises(self):
        runner = runner_returning(FakeProc(returncode=1, stderr="boom"))
        with self.assertRaises(RuntimeError):
            backends.reddit_fetch("search", ["q"], runner=runner)


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


if __name__ == "__main__":
    unittest.main()
