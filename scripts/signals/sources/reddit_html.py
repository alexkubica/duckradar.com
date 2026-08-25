from __future__ import annotations

import re
from dataclasses import dataclass
from html.parser import HTMLParser
from pathlib import Path
from typing import Any

from scripts.signals.classify import classify_signal
from scripts.signals.db import SignalsDB
from scripts.signals.sources.json_import import ImportResult

REDDIT_BASE_URL = "https://www.reddit.com"


@dataclass
class _Capture:
    kind: str
    thing_id: str
    depth: int
    chunks: list[str]


class _RedditHtmlParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.post_attrs: dict[str, str] = {}
        self.post_body = ""
        self.comment_attrs: list[dict[str, str]] = []
        self.comment_bodies: dict[str, str] = {}
        self._capture: _Capture | None = None

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr_map = {key: value or "" for key, value in attrs}

        if self._capture:
            self._capture.depth += 1
            if tag in {"p", "li", "br"}:
                self._capture.chunks.append("\n")
            return

        if tag == "shreddit-post":
            self.post_attrs = attr_map
            return

        if tag == "shreddit-comment":
            self.comment_attrs.append(attr_map)
            return

        element_id = attr_map.get("id", "")
        main_post_body_id = f"{self.post_attrs.get('id', '')}-post-rtjson-content"
        if tag == "div" and element_id == main_post_body_id:
            self._capture = _Capture(
                kind="post",
                thing_id=element_id.removesuffix("-post-rtjson-content"),
                depth=1,
                chunks=[],
            )
        elif tag == "div" and element_id.endswith("-comment-rtjson-content"):
            self._capture = _Capture(
                kind="comment",
                thing_id=element_id.removesuffix("-comment-rtjson-content"),
                depth=1,
                chunks=[],
            )

    def handle_endtag(self, tag: str) -> None:
        if not self._capture:
            return
        self._capture.depth -= 1
        if self._capture.depth > 0:
            return

        text = _normalize_text(" ".join(self._capture.chunks))
        if self._capture.kind == "post":
            self.post_body = text
        else:
            self.comment_bodies[self._capture.thing_id] = text
        self._capture = None

    def handle_data(self, data: str) -> None:
        if self._capture:
            self._capture.chunks.append(data)


def parse_reddit_html_capture(html_text: str, source_group: str) -> list[dict[str, Any]]:
    parser = _RedditHtmlParser()
    parser.feed(html_text)
    if not parser.post_attrs:
        return []

    post_entry = _post_entry(parser.post_attrs, parser.post_body, source_group)
    entries = [post_entry]
    for raw_comment in parser.comment_attrs:
        thing_id = raw_comment.get("thingid", "")
        body = parser.comment_bodies.get(thing_id, "")
        if body:
            entries.append(_comment_entry(raw_comment, body, post_entry, source_group))
    return entries


def import_reddit_html_capture(
    db: SignalsDB,
    path: str | Path,
    source_group: str,
) -> ImportResult:
    capture_path = Path(path)
    entries = parse_reddit_html_capture(capture_path.read_text(encoding="utf-8"), source_group)
    before_count = db.count_entries()
    for entry in entries:
        db.upsert_entry(entry)
    inserted = db.count_entries() - before_count
    db.record_run(
        source="reddit_html",
        source_group=source_group,
        status="success",
        message=f"Imported {len(entries)} entries from saved Reddit HTML {capture_path}",
        entries_seen=len(entries),
        entries_inserted=inserted,
    )
    return ImportResult(seen=len(entries), inserted=inserted)


def _post_entry(attrs: dict[str, str], body: str, source_group: str) -> dict[str, Any]:
    title = attrs.get("post-title", "")
    community = attrs.get("subreddit-name") or attrs.get("subreddit-prefixed-name", "").removeprefix("r/")
    external_id = attrs.get("id", "")
    url = _absolute_url(attrs.get("content-href") or attrs.get("permalink", ""))
    signal_type = classify_signal(title, body)
    return {
        "source": "reddit_html",
        "source_group": source_group,
        "community": community,
        "external_id": external_id,
        "url": url,
        "permalink": _absolute_url(attrs.get("permalink") or url),
        "title": title,
        "body": body,
        "author_username": attrs.get("author", ""),
        "created_at": _normalize_timestamp(attrs.get("created-timestamp", "")),
        "score": _to_int(attrs.get("score")),
        "comments_count": _to_int(attrs.get("comment-count")),
        "entry_type": "post",
        "signal_type": signal_type,
        "raw_json": {
            "evidence_type": "manual_paste",
            "capture_format": "reddit_saved_html",
            "visible_comments_only": True,
            "attrs": attrs,
        },
    }


def _comment_entry(
    attrs: dict[str, str],
    body: str,
    post_entry: dict[str, Any],
    source_group: str,
) -> dict[str, Any]:
    title = f"Comment on: {post_entry['title']}"
    return {
        "source": "reddit_html",
        "source_group": source_group,
        "community": post_entry["community"],
        "external_id": attrs.get("thingid", ""),
        "url": _absolute_url(attrs.get("permalink", "")),
        "permalink": _absolute_url(attrs.get("permalink", "")),
        "title": title,
        "body": body,
        "author_username": attrs.get("author", ""),
        "created_at": _normalize_timestamp(attrs.get("created", "")),
        "score": _to_int(attrs.get("score")),
        "comments_count": 0,
        "entry_type": "comment",
        "signal_type": classify_signal("", body),
        "raw_json": {
            "evidence_type": "manual_paste",
            "capture_format": "reddit_saved_html",
            "visible_comments_only": True,
            "post_external_id": post_entry["external_id"],
            "attrs": attrs,
        },
    }


def _absolute_url(url: str) -> str:
    if url.startswith("/"):
        return f"{REDDIT_BASE_URL}{url}"
    return url


def _normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def _normalize_timestamp(timestamp: str) -> str:
    if re.search(r"[+-]\d{4}$", timestamp):
        return f"{timestamp[:-5]}{timestamp[-5:-2]}:{timestamp[-2:]}"
    return timestamp


def _to_int(value: object) -> int:
    try:
        return int(value or 0)
    except (TypeError, ValueError):
        return 0
