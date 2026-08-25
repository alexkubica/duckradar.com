#!/usr/bin/env python3
"""Collect recent Reddit subreddit RSS entries cautiously.

This script intentionally avoids credentials, Reddit JSON endpoints, comment
thread crawling, search RSS, browser automation, and bypass techniques.

It checks Reddit robots.txt before collection and aborts when direct collection
is disallowed.
"""

from __future__ import annotations

import argparse
import email.utils
import json
import re
import sys
import time
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from html import unescape
from pathlib import Path
from re import sub


ATOM = "{http://www.w3.org/2005/Atom}"
ROBOTS_URL = "https://www.reddit.com/robots.txt"
USER_AGENT = (
    "DuckRadarResearch/0.1 "
    "(+https://duckradar.com; support@duckradar.com) "
    "RSS discovery; no login"
)


def clean_text(value: str) -> str:
    value = unescape(value or "")
    value = sub(r"<[^>]+>", " ", value)
    value = sub(r"\s+", " ", value).strip()
    return value


def parse_dt(value: str) -> str:
    if not value:
        return ""
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        try:
            parsed = email.utils.parsedate_to_datetime(value)
        except (TypeError, ValueError):
            return value
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc).isoformat()


def fetch(url: str, timeout: int) -> bytes:
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "application/atom+xml, application/rss+xml, text/xml;q=0.9, */*;q=0.8",
        },
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return response.read()


def robots_allows_direct_collection(timeout: int) -> tuple[bool, str]:
    payload = fetch(ROBOTS_URL, timeout).decode("utf-8", errors="replace")
    blocks = re.split(r"(?im)^User-agent:\s*", payload)
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


def collect_subreddit(subreddit: str, timeout: int, limit: int) -> tuple[list[dict], str | None]:
    url = f"https://www.reddit.com/r/{subreddit}/new/.rss"
    try:
        payload = fetch(url, timeout)
    except urllib.error.HTTPError as exc:
        return [], f"HTTP {exc.code}"
    except urllib.error.URLError as exc:
        return [], f"URL error: {exc.reason}"
    except TimeoutError:
        return [], "timeout"

    root = ET.fromstring(payload)
    entries: list[dict] = []
    for entry in root.findall(f"{ATOM}entry")[:limit]:
        title = clean_text(entry.findtext(f"{ATOM}title") or "")
        updated = parse_dt(entry.findtext(f"{ATOM}updated") or "")
        summary = clean_text(entry.findtext(f"{ATOM}content") or entry.findtext(f"{ATOM}summary") or "")
        author_name = ""
        author = entry.find(f"{ATOM}author")
        if author is not None:
            author_name = clean_text(author.findtext(f"{ATOM}name") or "")
        link = ""
        for link_el in entry.findall(f"{ATOM}link"):
            if link_el.attrib.get("rel") in {"alternate", ""} or not link:
                link = link_el.attrib.get("href", link)
        entries.append(
            {
                "subreddit": subreddit,
                "title": title,
                "url": link,
                "updated_utc": updated,
                "author": author_name,
                "summary": summary[:700],
            }
        )
    return entries, None


def main() -> int:
    parser = argparse.ArgumentParser(description="Collect recent Reddit subreddit RSS entries.")
    parser.add_argument("--subreddits", nargs="+", required=True)
    parser.add_argument("--delay", type=float, default=3.0, help="Seconds to wait between requests.")
    parser.add_argument("--limit", type=int, default=25, help="Entries per subreddit to keep.")
    parser.add_argument("--timeout", type=int, default=20)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    allowed, reason = robots_allows_direct_collection(args.timeout)
    if not allowed:
        print(f"Direct Reddit collection aborted: {reason}", file=sys.stderr)
        return 2

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)

    all_entries: list[dict] = []
    errors: dict[str, str] = {}
    for index, subreddit in enumerate(args.subreddits):
        entries, error = collect_subreddit(subreddit, args.timeout, args.limit)
        if error:
            errors[subreddit] = error
            if error.startswith("HTTP 403") or error.startswith("HTTP 429"):
                print(f"Stopping after {subreddit}: {error}", file=sys.stderr)
                break
        else:
            all_entries.extend(entries)
        if index < len(args.subreddits) - 1:
            time.sleep(args.delay)

    result = {
        "collected_at_utc": datetime.now(timezone.utc).isoformat(),
        "method": "public subreddit RSS only; no credentials; no JSON endpoints; no comment crawling",
        "user_agent": USER_AGENT,
        "subreddit_count_requested": len(args.subreddits),
        "entry_count": len(all_entries),
        "errors": errors,
        "entries": all_entries,
    }
    output.write_text(json.dumps(result, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    print(f"Wrote {len(all_entries)} entries to {output}")
    if errors:
        print(json.dumps(errors, indent=2), file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
