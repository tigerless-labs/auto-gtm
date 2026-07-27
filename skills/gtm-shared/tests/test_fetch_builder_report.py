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

    def test_podcast_transcript_passed_in_full(self):
        out = run("--feed-dir", str(FIXTURES)).stdout
        self.assertIn("END-OF-TRANSCRIPT-SENTINEL", out)

    def test_blog_content_passed_in_full(self):
        out = run("--feed-dir", str(FIXTURES)).stdout
        self.assertIn("END-OF-BLOG-SENTINEL", out)

    def test_optional_max_chars_truncates(self):
        full = run("--feed-dir", str(FIXTURES)).stdout
        capped = run("--feed-dir", str(FIXTURES), "--max-chars", "200").stdout
        self.assertNotIn("END-OF-TRANSCRIPT-SENTINEL", capped)
        self.assertNotIn("END-OF-BLOG-SENTINEL", capped)
        self.assertLess(len(capped), len(full))
        # the capped body is a prefix of the full body, not different text
        transcript_head = "Today we get into how you actually evaluate coding agents"
        self.assertIn(transcript_head, capped)
        self.assertIn(transcript_head, full)

    def test_x_builder_bio_passed_through(self):
        # The digest rules open each builder with role/company taken from the feed's bio,
        # so the bio has to survive collection — dropping it silently degrades the summary.
        out = run("--feed-dir", str(FIXTURES)).stdout
        for bio in ("AI engineer", "writes about product"):
            self.assertIn(bio, out)

    def test_x_builder_without_bio_renders_cleanly(self):
        r = run("--feed-dir", str(FIXTURES))
        self.assertEqual(r.returncode, 0, r.stderr)
        heading = next(
            line for line in r.stdout.splitlines() if "nobiobuilder" in line
        )
        self.assertIn("No Bio Builder", heading)
        # no dangling separator where the missing bio would have gone
        self.assertFalse(heading.rstrip().endswith("—"))
        self.assertNotIn("None", heading)

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
