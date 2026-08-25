import tempfile
import unittest
from pathlib import Path

from scripts.signals.db import SignalsDB


class SignalsDBTest(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = Path(self.temp_dir.name) / "signals.sqlite"
        self.db = SignalsDB(self.db_path)
        self.db.init_schema()

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_upsert_dedupes_entries_by_source_and_external_id(self):
        entry = {
            "source": "reddit_rss",
            "source_group": "seo",
            "community": "SEO",
            "external_id": "abc123",
            "url": "https://www.reddit.com/r/SEO/comments/abc123/example/",
            "permalink": "https://www.reddit.com/r/SEO/comments/abc123/example/",
            "title": "SEO reporting pain",
            "body": "Client wants the next action, not another dashboard.",
            "author_username": "public_user",
            "created_at": "2026-06-02T10:00:00+00:00",
            "score": 4,
            "comments_count": 7,
            "entry_type": "rss_entry",
            "signal_type": "agency_reporting",
            "raw_json": {"id": "abc123"},
        }

        first_id = self.db.upsert_entry(entry)
        second_id = self.db.upsert_entry({**entry, "score": 9})

        self.assertEqual(first_id, second_id)
        rows = self.db.search_entries("reporting")
        self.assertEqual(1, len(rows))
        self.assertEqual(9, rows[0]["score"])

    def test_full_text_search_matches_title_and_body(self):
        self.db.upsert_entry(
            {
                "source": "manual",
                "source_group": "marketing",
                "community": "marketing",
                "external_id": "m1",
                "url": "https://example.com/m1",
                "title": "Cold email workflow",
                "body": "People complain about lead generation and outreach tooling.",
                "entry_type": "external_export",
                "signal_type": "sales_outreach",
            }
        )

        title_rows = self.db.search_entries("cold")
        body_rows = self.db.search_entries("outreach")

        self.assertEqual("Cold email workflow", title_rows[0]["title"])
        self.assertEqual("Cold email workflow", body_rows[0]["title"])

    def test_tags_can_be_set_and_listed(self):
        entry_id = self.db.upsert_entry(
            {
                "source": "manual",
                "source_group": "seo",
                "community": "SEO",
                "external_id": "tag-1",
                "url": "https://example.com/tag-1",
                "title": "AI visibility tool pricing",
                "body": "",
                "entry_type": "external_export",
                "signal_type": "tool_pricing",
            }
        )

        self.db.set_entry_tags(entry_id, ["idea", "tool_pricing"])

        self.assertEqual(["idea", "tool_pricing"], self.db.get_entry_tags(entry_id))
        self.assertEqual(["idea", "tool_pricing"], self.db.list_tags())

    def test_run_history_records_status_and_counts(self):
        self.db.record_run(
            source="reddit_rss",
            source_group="seo",
            status="aborted",
            message="robots disallowed direct collection",
            entries_seen=0,
            entries_inserted=0,
        )

        runs = self.db.list_runs()

        self.assertEqual(1, len(runs))
        self.assertEqual("aborted", runs[0]["status"])
        self.assertIn("robots", runs[0]["message"])


if __name__ == "__main__":
    unittest.main()
