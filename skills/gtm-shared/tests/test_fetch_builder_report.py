import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCRIPT = HERE.parent / "scripts" / "fetch_builder_report.py"
FIXTURES = HERE / "fixtures"


def run(*args):
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        capture_output=True,
        text=True,
    )


class FetchBuilderReport(unittest.TestCase):
    def test_pulls_all_three_feeds(self):
        r = run("--feed-dir", str(FIXTURES))
        self.assertEqual(r.returncode, 0, r.stderr)
        out = r.stdout
        for marker in ("swyx", "petergyang", "Claude Blog", "Latent Space"):
            self.assertIn(marker, out)
        # three distinct sections rendered
        low = out.lower()
        self.assertIn("twitter", low)
        self.assertIn("blog", low)
        self.assertIn("podcast", low)

    def test_no_recency_hour_filter(self):
        # The 6-day-old tweet must survive: recency is the feed's own window, not a 24h cut.
        r = run("--feed-dir", str(FIXTURES))
        self.assertIn("status/102", r.stdout)
        self.assertNotIn("--hours", r.stdout)

    def test_every_item_carries_its_link(self):
        out = run("--feed-dir", str(FIXTURES)).stdout
        for url in (
            "https://x.com/swyx/status/101",
            "https://claude.com/blog/artifacts-in-claude-code",
            "https://youtube.com/watch?v=agenteval",
        ):
            self.assertIn(url, out)

    def test_all_feeds_missing_exits_nonzero(self):
        with tempfile.TemporaryDirectory() as empty:
            r = run("--feed-dir", empty)
        self.assertNotEqual(r.returncode, 0)
        self.assertTrue(r.stderr.strip())

    def test_injection_text_passed_through_as_data(self):
        # Prompt-injection-shaped tweet text is carried verbatim as data, never acted on.
        out = run("--feed-dir", str(FIXTURES)).stdout
        self.assertIn("IGNORE ALL PREVIOUS INSTRUCTIONS", out)

    def test_optional_query_keeps_only_matches(self):
        base = run("--feed-dir", str(FIXTURES)).stdout
        filtered = run("--feed-dir", str(FIXTURES), "--query", "eval").stdout
        # match set is a strict subset: the eval tweet + eval podcast stay, others go.
        self.assertIn("status/101", filtered)
        self.assertIn("status/101", base)
        self.assertNotIn("status/102", filtered)
        self.assertNotIn("status/103", filtered)
        self.assertIn("status/102", base)


if __name__ == "__main__":
    unittest.main()
