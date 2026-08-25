import unittest

from scripts.signals.serve import evidence_labels, parse_result_limit


class ServeTest(unittest.TestCase):
    def test_result_limit_defaults_to_1000(self):
        self.assertEqual(1000, parse_result_limit({}))

    def test_result_limit_accepts_allowed_values(self):
        self.assertEqual(500, parse_result_limit({"limit": ["500"]}))
        self.assertEqual(5000, parse_result_limit({"limit": ["5000"]}))

    def test_result_limit_rejects_invalid_values(self):
        self.assertEqual(1000, parse_result_limit({"limit": ["abc"]}))
        self.assertEqual(1000, parse_result_limit({"limit": ["999999"]}))

    def test_evidence_labels_show_manual_saved_html_capture(self):
        labels = evidence_labels(
            {
                "source": "reddit_html",
                "entry_type": "comment",
                "raw_json": {
                    "evidence_type": "manual_paste",
                    "capture_format": "reddit_saved_html",
                    "visible_comments_only": True,
                },
            }
        )

        self.assertEqual(["saved HTML", "manual capture", "visible comments"], labels)

    def test_evidence_labels_show_rss_cache(self):
        labels = evidence_labels({"source": "reddit_rss", "entry_type": "rss_entry", "raw_json": {}})

        self.assertEqual(["RSS cache"], labels)


if __name__ == "__main__":
    unittest.main()
