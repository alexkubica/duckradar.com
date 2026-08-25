import unittest

from scripts.signals.classify import classify_signal
from scripts.signals.config import SOURCE_GROUPS


class SourceGroupConfigTest(unittest.TestCase):
    def test_config_includes_requested_source_groups(self):
        self.assertIn("seo", SOURCE_GROUPS)
        self.assertIn("marketing", SOURCE_GROUPS)
        self.assertIn("sales", SOURCE_GROUPS)

    def test_marketing_group_includes_requested_subreddits(self):
        for subreddit in [
            "AISEOforBeginners",
            "AskMarketing",
            "ColdEmailsForLiving",
            "Coldemailing",
            "DigitalMarketing",
            "EmailOutreach",
            "Emailmarketing",
            "GEO_optimization",
            "InstagramMarketing",
            "PPC",
            "SaaSMarketing",
            "SocialMediaMarketing",
            "b2bmarketing",
            "coldemail",
            "content_marketing",
            "digital_marketing",
            "marketing",
        ]:
            self.assertIn(subreddit, SOURCE_GROUPS["marketing"])

    def test_sales_group_includes_requested_subreddits(self):
        for subreddit in [
            "LeadGenMarketplace",
            "LeadGeneration",
            "Sales_Professionals",
            "googleads",
            "sales",
            "salestechniques",
            "techsales",
        ]:
            self.assertIn(subreddit, SOURCE_GROUPS["sales"])


class ClassifierTest(unittest.TestCase):
    def test_classifies_tool_pricing(self):
        self.assertEqual(
            "tool_pricing",
            classify_signal("Semrush is too expensive", "Looking for a cheaper Ahrefs alternative"),
        )

    def test_classifies_agency_reporting(self):
        self.assertEqual(
            "agency_reporting",
            classify_signal("How do you report SEO results to clients?", "Monthly client reporting is painful"),
        )

    def test_classifies_ai_search(self):
        self.assertEqual(
            "ai_search",
            classify_signal("ChatGPT visibility", "How do I show up in AI Overviews and Perplexity?"),
        )

    def test_classifies_sales_outreach(self):
        self.assertEqual(
            "sales_outreach",
            classify_signal("Cold email deliverability", "Outbound sequences are landing in spam"),
        )

    def test_classifies_lead_source(self):
        self.assertEqual(
            "lead_source",
            classify_signal("Where do agencies find leads?", "Looking for lead generation workflows"),
        )

    def test_classifies_unknown_when_no_keywords_match(self):
        self.assertEqual("unknown", classify_signal("General question", "Nothing specific here"))


if __name__ == "__main__":
    unittest.main()
