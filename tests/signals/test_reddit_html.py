import tempfile
import unittest
from pathlib import Path

from scripts.signals.db import SignalsDB
from scripts.signals.sources.reddit_html import import_reddit_html_capture, parse_reddit_html_capture


HTML_CAPTURE = """
<!-- saved from url=(0103)https://www.reddit.com/r/RankWithAI/comments/1tp7qsh/how_do_you_report_seo_results_to_clients_in_a_way/ -->
<html>
  <body>
    <shreddit-post
      permalink="/r/RankWithAI/comments/1tp7qsh/how_do_you_report_seo_results_to_clients_in_a_way/"
      content-href="https://www.reddit.com/r/RankWithAI/comments/1tp7qsh/how_do_you_report_seo_results_to_clients_in_a_way/"
      comment-count="5"
      created-timestamp="2026-05-27T14:46:08.056000+0000"
      id="t3_1tp7qsh"
      post-title="How do you report SEO results to clients in a way that accounts for AI search not just Google rankings?"
      score="3"
      subreddit-name="RankWithAI"
      author="RealisticPosition169">
      <h1 slot="title">How do you report SEO results to clients in a way that accounts for AI search not just Google rankings?</h1>
      <shreddit-post-text-body slot="text-body" post-id="t3_1tp7qsh">
        <div id="t3_1tp7qsh-post-rtjson-content" property="schema:articleBody">
          <p>SEO reports are now missing an important piece.</p>
          <ul>
            <li><p>Do you include AI Search metrics on client reports?</p></li>
            <li><p>How do you capture or estimate AI citation visibility?</p></li>
          </ul>
        </div>
      </shreddit-post-text-body>
    </shreddit-post>
    <shreddit-comment
      created="2026-05-28T09:30:05.431000+0000"
      author="mjain_entrepreneur"
      thingid="t1_ooc8j0l"
      permalink="/r/RankWithAI/comments/1tp7qsh/comment/ooc8j0l/"
      score="1"
      postid="t3_1tp7qsh">
      <div id="t1_ooc8j0l-comment-rtjson-content" slot="comment">
        <p>Yes, it is best to add AI visibility as its own section, separate from Google rankings.</p>
        <p>Track fixed buyer-intent prompts across ChatGPT, Perplexity, Gemini, AI Overviews/AI Mode.</p>
      </div>
    </shreddit-comment>
    <div id="t3_promoted-post-rtjson-content" property="schema:articleBody">
      <p>If it's not yours, say so.</p>
    </div>
  </body>
</html>
"""


class RedditHtmlTest(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        self.db = SignalsDB(self.root / "signals.sqlite")
        self.db.init_schema()

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_parse_reddit_html_capture_extracts_post_and_visible_comments(self):
        entries = parse_reddit_html_capture(HTML_CAPTURE, source_group="seo")

        self.assertEqual(2, len(entries))
        post = entries[0]
        comment = entries[1]
        self.assertEqual("post", post["entry_type"])
        self.assertEqual("comment", comment["entry_type"])
        self.assertEqual("RankWithAI", post["community"])
        self.assertEqual("t3_1tp7qsh", post["external_id"])
        self.assertEqual("RealisticPosition169", post["author_username"])
        self.assertIn("AI Search metrics", post["body"])
        self.assertEqual("agency_reporting", post["signal_type"])
        self.assertEqual("t1_ooc8j0l", comment["external_id"])
        self.assertEqual("mjain_entrepreneur", comment["author_username"])
        self.assertIn("buyer-intent prompts", comment["body"])
        self.assertEqual("ai_search", comment["signal_type"])

    def test_import_reddit_html_capture_dedupes_entries(self):
        capture_path = self.root / "thread.html"
        capture_path.write_text(HTML_CAPTURE, encoding="utf-8")

        first = import_reddit_html_capture(self.db, capture_path, source_group="seo")
        second = import_reddit_html_capture(self.db, capture_path, source_group="seo")

        self.assertEqual(2, first.seen)
        self.assertEqual(2, first.inserted)
        self.assertEqual(2, second.seen)
        self.assertEqual(0, second.inserted)
        self.assertEqual(2, self.db.count_entries())
        runs = self.db.list_runs()
        self.assertEqual("reddit_html", runs[0]["source"])
        self.assertEqual("manual_paste", self.db.search_entries("buyer-intent")[0]["raw_json"]["evidence_type"])


if __name__ == "__main__":
    unittest.main()
