from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from scripts.signals.classify import classify_signal
from scripts.signals.db import SignalsDB


@dataclass(frozen=True)
class ImportResult:
    seen: int
    inserted: int


def import_json_capture(db: SignalsDB, path: str | Path, source_group: str) -> ImportResult:
    capture_path = Path(path)
    payload = json.loads(capture_path.read_text(encoding="utf-8"))
    raw_entries = payload.get("entries", [])
    seen = 0
    inserted = 0
    before_count = db.count_entries()

    for raw_entry in raw_entries:
        seen += 1
        db.upsert_entry(_normalize_json_entry(raw_entry, source_group))

    after_count = db.count_entries()
    inserted = after_count - before_count
    db.record_run(
        source="json_import",
        source_group=source_group,
        status="success",
        message=f"Imported {seen} entries from {capture_path}",
        entries_seen=seen,
        entries_inserted=inserted,
    )
    return ImportResult(seen=seen, inserted=inserted)


def _normalize_json_entry(raw_entry: dict[str, Any], source_group: str) -> dict[str, Any]:
    title = str(raw_entry.get("title") or "")
    body = str(raw_entry.get("body") or raw_entry.get("summary") or "")
    url = str(raw_entry.get("url") or raw_entry.get("permalink") or "")
    external_id = str(raw_entry.get("id") or raw_entry.get("external_id") or _id_from_url(url))
    return {
        "source": str(raw_entry.get("source") or "reddit_rss"),
        "source_group": source_group,
        "community": str(raw_entry.get("community") or raw_entry.get("subreddit") or ""),
        "external_id": external_id,
        "url": url,
        "permalink": str(raw_entry.get("permalink") or url),
        "title": title,
        "body": body,
        "author_username": str(raw_entry.get("author_username") or raw_entry.get("author") or ""),
        "created_at": str(raw_entry.get("created_at") or raw_entry.get("updated_utc") or ""),
        "score": int(raw_entry.get("score") or 0),
        "comments_count": int(raw_entry.get("comments_count") or raw_entry.get("num_comments") or 0),
        "entry_type": str(raw_entry.get("entry_type") or "rss_entry"),
        "signal_type": str(raw_entry.get("signal_type") or classify_signal(title, body)),
        "raw_json": raw_entry,
    }


def _id_from_url(url: str) -> str:
    parts = [part for part in url.rstrip("/").split("/") if part]
    if "comments" in parts:
        index = parts.index("comments")
        if index + 1 < len(parts):
            return parts[index + 1]
    return url
