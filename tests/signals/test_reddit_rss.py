import tempfile
import unittest
from pathlib import Path

from scripts.signals.db import SignalsDB
from scripts.signals.sources.reddit_rss import collect_group, robots_allows_direct_collection


class RedditRssTest(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db = SignalsDB(Path(self.temp_dir.name) / "signals.sqlite")
        self.db.init_schema()

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_robots_disallow_global_crawling(self):
        robots = """
        User-agent: *
        Disallow: /
        """

        allowed, reason = robots_allows_direct_collection(robots)

        self.assertFalse(allowed)
        self.assertIn("Disallow", reason)

    def test_collect_group_aborts_without_subreddit_fetches_when_robots_disallow(self):
        calls = []

        def fetcher(url: str) -> str:
            calls.append(url)
            return "User-agent: *\nDisallow: /\n"

        result = collect_group(
            self.db,
            source_group="seo",
            subreddits=["SEO", "bigseo"],
            fetcher=fetcher,
            delay_seconds=0,
        )

        self.assertEqual("aborted", result.status)
        self.assertEqual(0, result.entries_seen)
        self.assertEqual(["https://www.reddit.com/robots.txt"], calls)
        runs = self.db.list_runs()
        self.assertEqual("aborted", runs[0]["status"])

    def test_collect_group_imports_allowed_rss_entries(self):
        rss = """<?xml version="1.0" encoding="UTF-8"?>
        <feed xmlns="http://www.w3.org/2005/Atom">
          <entry>
            <title>SEO reporting workflow</title>
            <updated>2026-06-02T08:00:00Z</updated>
            <author><name>user_a</name></author>
            <link rel="alternate" href="https://www.reddit.com/r/SEO/comments/abc/reporting/" />
            <content>Client wants a brief, not a dashboard.</content>
          </entry>
        </feed>
        """

        def fetcher(url: str) -> str:
            if url.endswith("/robots.txt"):
                return "User-agent: *\nAllow: /\n"
            return rss

        result = collect_group(
            self.db,
            source_group="seo",
            subreddits=["SEO"],
            fetcher=fetcher,
            delay_seconds=0,
        )

        self.assertEqual("success", result.status)
        self.assertEqual(1, result.entries_seen)
        self.assertEqual(1, self.db.count_entries())
        row = self.db.search_entries("brief")[0]
        self.assertEqual("user_a", row["author_username"])


if __name__ == "__main__":
    unittest.main()
