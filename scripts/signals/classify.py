from __future__ import annotations


SIGNAL_KEYWORDS: list[tuple[str, tuple[str, ...]]] = [
    (
        "tool_pricing",
        (
            "semrush",
            "ahrefs",
            "expensive",
            "pricing",
            "cheaper",
            "alternative",
            "enterprise tax",
            "tool stack",
        ),
    ),
    (
        "agency_reporting",
        (
            "client reporting",
            "report seo results",
            "monthly report",
            "monthly reporting",
            "client-ready",
            "dashboard",
            "looker studio",
            "agency",
        ),
    ),
    (
        "ai_search",
        (
            "chatgpt",
            "perplexity",
            "ai overview",
            "ai overviews",
            "ai search",
            "geo",
            "aeo",
            "citation",
            "llm",
        ),
    ),
    (
        "sales_outreach",
        (
            "cold email",
            "outbound",
            "deliverability",
            "sequence",
            "follow-up",
            "follow up",
            "spam",
        ),
    ),
    (
        "lead_source",
        (
            "lead generation",
            "find leads",
            "finding leads",
            "lead gen",
            "prospecting",
            "bookings",
            "pipeline",
        ),
    ),
    (
        "workflow",
        (
            "workflow",
            "process",
            "automation",
            "repetitive",
            "spreadsheet",
            "search console",
            "gsc",
        ),
    ),
]


def classify_signal(title: str, body: str = "") -> str:
    text = f"{title} {body}".lower()
    for signal_type, keywords in SIGNAL_KEYWORDS:
        if any(keyword in text for keyword in keywords):
            return signal_type
    return "unknown"
