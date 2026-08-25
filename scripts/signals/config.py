from __future__ import annotations

from pathlib import Path


DEFAULT_DB_PATH = Path("data/signals.sqlite")

SOURCE_GROUPS: dict[str, list[str]] = {
    "seo": [
        "Agentic_SEO",
        "GEO_optimization",
        "RankWithAI",
        "SEO",
        "SEO_Digital_Marketing",
        "SEOandBacklinks",
        "SEOorganic",
        "ShopifySEO",
        "TechSEO",
        "aeo",
        "bigseo",
        "juststart",
        "localseo",
        "seogrowth",
    ],
    "marketing": [
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
    ],
    "sales": [
        "LeadGenMarketplace",
        "LeadGeneration",
        "Sales_Professionals",
        "googleads",
        "sales",
        "salestechniques",
        "techsales",
    ],
}
