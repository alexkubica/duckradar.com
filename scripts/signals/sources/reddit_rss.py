from __future__ import annotations

import re
import time
import urllib.request
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from html import unescape
from re import sub
from typing import Callable

from scripts.signals.classify import classify_signal
from scripts.signals.db import SignalsDB


ATOM = "{http://www.w3.org/2005/Atom}"
ROBOTS_URL = "https://www.reddit.com/robots.txt"
USER_AGENT = (
    "DuckRadarResearch/0.1 "
    "(+https://duckradar.com; support@duckradar.com) "
    "RSS discovery; no login"
)


@dataclass(frozen=True)
class CollectResult:
    status: str
    entries_seen: int
    entries_inserted: int
    message: str


def default_fetcher(url: str) -> str:
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "application/atom+xml, application/rss+xml, text/xml;q=0.9, */*;q=0.8",
        },
    )
    with urllib.request.urlopen(request, timeout=20) as response:
        return response.read().decode("utf-8", errors="replace")


def robots_allows_direct_collection(robots_txt: str) -> tuple[bool, str]:
    blocks = re.split(r"(?im)^\s*User-agent:\s*", robots_txt)
    for block in blocks:
        lines = [line.strip() for line in block.splitlines() if line.strip()]
        if not lines:
            continue
        agent = lines[0].lower()
        if agent != "*":
            continue
        for line in lines[1:]:
            if re.match(r"(?i)^disallow:\s*/\s*$", line):
                return False, "robots.txt has User-agent: * with Disallow: /"
    return True, "robots.txt does not contain a global Disallow: / block"


def collect_group(
    db: SignalsDB,
    *,
    source_group: str,
    subreddits: list[str],
    fetcher: Callable[[str], str] = default_fetcher,
    delay_seconds: float = 3.0,
    limit_per_subreddit: int = 25,
) -> CollectResult:
    robots_txt = fetcher(ROBOTS_URL)
    allowed, reason = robots_allows_direct_collection(robots_txt)
    if not allowed:
        db.record_run(
            source="reddit_rss",
            source_group=source_group,
            status="aborted",
            message=reason,
        )
        return CollectResult(
            status="aborted",
            entries_seen=0,
            entries_inserted=0,
            message=reason,
        )

    before_count = db.count_entries()
    entries_seen = 0
    for index, subreddit in enumerate(subreddits):
        rss_url = f"https://www.reddit.com/r/{subreddit}/new/.rss"
        rss_text = fetcher(rss_url)
        for raw_entry in parse_atom_entries(rss_text, subreddit, limit_per_subreddit):
            entries_seen += 1
            db.upsert_entry({**raw_entry, "source_group": source_group})
        if index < len(subreddits) - 1 and delay_seconds > 0:
            time.sleep(delay_seconds)

    inserted = db.count_entries() - before_count
    message = f"Collected {entries_seen} RSS entries from {len(subreddits)} subreddits"
    db.record_run(
        source="reddit_rss",
        source_group=source_group,
        status="success",
        message=message,
        entries_seen=entries_seen,
        entries_inserted=inserted,
    )
    return CollectResult(
        status="success",
        entries_seen=entries_seen,
        entries_inserted=inserted,
        message=message,
    )


def parse_atom_entries(rss_text: str, subreddit: str, limit: int) -> list[dict[str, object]]:
    root = ET.fromstring(rss_text)
    entries = []
    for entry in root.findall(f"{ATOM}entry")[:limit]:
        title = clean_text(entry.findtext(f"{ATOM}title") or "")
        body = clean_text(entry.findtext(f"{ATOM}content") or entry.findtext(f"{ATOM}summary") or "")
        author_username = ""
        author = entry.find(f"{ATOM}author")
        if author is not None:
            author_username = clean_text(author.findtext(f"{ATOM}name") or "")
        url = ""
        for link_el in entry.findall(f"{ATOM}link"):
            if link_el.attrib.get("rel") in {"alternate", ""} or not url:
                url = link_el.attrib.get("href", url)
        entries.append(
            {
                "source": "reddit_rss",
                "community": subreddit,
                "external_id": id_from_url(url),
                "url": url,
                "permalink": url,
                "title": title,
                "body": body,
                "author_username": author_username,
                "created_at": entry.findtext(f"{ATOM}updated") or "",
                "entry_type": "rss_entry",
                "signal_type": classify_signal(title, body),
                "raw_json": {
                    "subreddit": subreddit,
                    "url": url,
                    "title": title,
                    "body": body,
                    "author_username": author_username,
                },
            }
        )
    return entries


def clean_text(value: str) -> str:
    value = unescape(value or "")
    value = sub(r"<[^>]+>", " ", value)
    value = sub(r"\s+", " ", value).strip()
    return value


def id_from_url(url: str) -> str:
    parts = [part for part in url.rstrip("/").split("/") if part]
    if "comments" in parts:
        index = parts.index("comments")
        if index + 1 < len(parts):
            return parts[index + 1]
    return url
