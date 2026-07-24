import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "scripts" / "reach"))
import reddit_keyless as rk  # noqa: E402

LISTING_HTML = (
    '<shreddit-post author="ClaudeOfficial" author-id="t2_abc" '
    'id="t3_1v5h6pr" subreddit-id="t5_dp6k3k" '
    'post-title="Introducing Claude Opus 5" score="1148" comment-count="316" '
    'permalink="/r/ClaudeCode/comments/1v5h6pr/introducing/" '
    'subreddit-prefixed-name="r/ClaudeCode">post body</shreddit-post>'
    '<shreddit-post author="someone" author-id="t2_def" id="t3_zzz" '
    'post-title="Tips &amp; tricks" score="42" comment-count="7" '
    'permalink="/r/ClaudeCode/comments/zzz/tips/" '
    'subreddit-prefixed-name="r/ClaudeCode">x</shreddit-post>'
)

COMMENTS_HTML = (
    '<shreddit-comment author="Top-Weakness-1311" score="4" depth="0" '
    'permalink="/r/x/comments/1/c/">a</shreddit-comment>'
    '<shreddit-comment author="other" score="2" depth="1" '
    'permalink="/r/x/comments/1/d/">b</shreddit-comment>'
)

RSS_XML = (
    '<feed><entry><title>Cool post</title>'
    '<link href="https://www.reddit.com/r/ClaudeCode/comments/abc123/cool/"/>'
    '<id>t3_abc123</id></entry></feed>'
)

ARCTIC_JSON = '{"data":[{"id":"abc123","score":99,"num_comments":5}]}'


class ParseListing(unittest.TestCase):
    def test_extracts_post_id_and_scores(self):
        posts = rk.parse_listing(LISTING_HTML)
        self.assertEqual(posts[0]["id"], "t3_1v5h6pr")            # not the t2_/t5_ ids
        self.assertEqual(posts[0]["author"], "ClaudeOfficial")   # not author-id
        self.assertEqual(posts[0]["score"], 1148)
        self.assertEqual(posts[0]["comments"], 316)
        self.assertEqual(posts[0]["title"], "Introducing Claude Opus 5")

    def test_unescapes_title(self):
        posts = rk.parse_listing(LISTING_HTML)
        self.assertEqual(posts[1]["title"], "Tips & tricks")


class ParseComments(unittest.TestCase):
    def test_attrs_and_limit(self):
        c = rk.parse_comments(COMMENTS_HTML, limit=1)
        self.assertEqual(len(c), 1)
        self.assertEqual(c[0]["author"], "Top-Weakness-1311")
        self.assertEqual(c[0]["score"], 4)
        self.assertEqual(c[0]["depth"], 0)


class ParseRss(unittest.TestCase):
    def test_extracts_id_and_link(self):
        posts = rk.parse_rss(RSS_XML)
        self.assertEqual(posts[0]["id"], "t3_abc123")
        self.assertTrue(posts[0]["permalink"].endswith("/cool/"))
        self.assertIsNone(posts[0]["score"])  # RSS carries no score


class Composite(unittest.TestCase):
    def test_sub_lane_uses_listing_scores(self):
        posts = rk.keyless_reddit(sub="ClaudeCode", getter=lambda url, timeout=20: LISTING_HTML)
        self.assertEqual(posts[0]["score"], 1148)

    def test_query_lane_backfills_score_from_arctic(self):
        def getter(url, timeout=20):
            if "search.rss" in url:
                return RSS_XML
            if "arctic-shift" in url:
                return ARCTIC_JSON
            return ""
        posts = rk.keyless_reddit(query="cool", getter=getter)
        self.assertEqual(posts[0]["id"], "t3_abc123")
        self.assertEqual(posts[0]["score"], 99)  # backfilled

    def test_best_effort_returns_empty_on_failure(self):
        # every probe fails (empty body) -> [] not an exception
        self.assertEqual(rk.keyless_reddit(sub="x", getter=lambda url, timeout=20: ""), [])
        self.assertEqual(rk.keyless_reddit(query="x", getter=lambda url, timeout=20: ""), [])


if __name__ == "__main__":
    unittest.main()
