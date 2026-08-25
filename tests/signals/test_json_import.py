import json
import tempfile
import unittest
from pathlib import Path

from scripts.signals.db import SignalsDB
from scripts.signals.sources.json_import import import_json_capture


class JsonImportTest(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        self.db = SignalsDB(self.root / "signals.sqlite")
        self.db.init_schema()

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_imports_rss_capture_and_dedupes_entries(self):
        capture_path = self.root / "capture.json"
        capture_path.write_text(
            json.dumps(
                {
                    "collected_at_utc": "2026-06-01T16:47:45+00:00",
                    "entries": [
                        {
                            "subreddit": "SEO",
                            "title": "How do you report AI search to clients?",
                            "url": "https://www.reddit.com/r/SEO/comments/a/reporting/",
                            "updated_utc": "2026-06-01T10:00:00+00:00",
                            "author": "user_a",
                            "summary": "Client reports are missing AI search visibility.",
                        },
                        {
                            "subreddit": "PPC",
                            "title": "Cold email leads",
                            "url": "https://www.reddit.com/r/PPC/comments/b/leads/",
                            "updated_utc": "2026-06-01T11:00:00+00:00",
                            "author": "user_b",
                            "summary": "Looking for lead generation workflow ideas.",
                        },
                        {
                            "subreddit": "SEO",
                            "title": "How do you report AI search to clients?",
                            "url": "https://www.reddit.com/r/SEO/comments/a/reporting/",
                            "updated_utc": "2026-06-01T10:00:00+00:00",
                            "author": "user_a",
                            "summary": "Duplicate should update, not insert.",
                        },
                    ],
                }
            ),
            encoding="utf-8",
        )

        result = import_json_capture(self.db, capture_path, source_group="seo")

        self.assertEqual(3, result.seen)
        self.assertEqual(2, result.inserted)
        self.assertEqual(2, self.db.count_entries())
        rows = self.db.search_entries("AI")
        self.assertEqual(1, len(rows))
        self.assertEqual("user_a", rows[0]["author_username"])
        self.assertEqual("ai_search", rows[0]["signal_type"])


if __name__ == "__main__":
    unittest.main()
