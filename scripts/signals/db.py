from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


class SignalsDB:
    def __init__(self, path: str | Path):
        self.path = Path(path)

    def connect(self) -> sqlite3.Connection:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(self.path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        return conn

    def init_schema(self) -> None:
        with self.connect() as conn:
            conn.executescript(
                """
                CREATE TABLE IF NOT EXISTS entries (
                    id INTEGER PRIMARY KEY,
                    source TEXT NOT NULL,
                    source_group TEXT NOT NULL DEFAULT '',
                    community TEXT NOT NULL DEFAULT '',
                    external_id TEXT,
                    dedupe_key TEXT NOT NULL UNIQUE,
                    url TEXT NOT NULL DEFAULT '',
                    permalink TEXT NOT NULL DEFAULT '',
                    title TEXT NOT NULL DEFAULT '',
                    body TEXT NOT NULL DEFAULT '',
                    author_username TEXT NOT NULL DEFAULT '',
                    created_at TEXT NOT NULL DEFAULT '',
                    fetched_at TEXT NOT NULL DEFAULT '',
                    score INTEGER NOT NULL DEFAULT 0,
                    comments_count INTEGER NOT NULL DEFAULT 0,
                    entry_type TEXT NOT NULL DEFAULT 'external_export',
                    signal_type TEXT NOT NULL DEFAULT 'unknown',
                    raw_json TEXT NOT NULL DEFAULT '{}'
                );

                CREATE VIRTUAL TABLE IF NOT EXISTS entry_fts USING fts5(
                    entry_id UNINDEXED,
                    title,
                    body,
                    community,
                    author_username
                );

                CREATE TABLE IF NOT EXISTS tags (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL UNIQUE
                );

                CREATE TABLE IF NOT EXISTS entry_tags (
                    entry_id INTEGER NOT NULL REFERENCES entries(id) ON DELETE CASCADE,
                    tag_id INTEGER NOT NULL REFERENCES tags(id) ON DELETE CASCADE,
                    PRIMARY KEY (entry_id, tag_id)
                );

                CREATE TABLE IF NOT EXISTS runs (
                    id INTEGER PRIMARY KEY,
                    source TEXT NOT NULL,
                    source_group TEXT NOT NULL DEFAULT '',
                    status TEXT NOT NULL,
                    message TEXT NOT NULL DEFAULT '',
                    entries_seen INTEGER NOT NULL DEFAULT 0,
                    entries_inserted INTEGER NOT NULL DEFAULT 0,
                    started_at TEXT NOT NULL,
                    finished_at TEXT NOT NULL
                );
                """
            )

    def upsert_entry(self, entry: dict[str, Any]) -> int:
        now = utc_now()
        normalized = self._normalize_entry(entry, now)
        with self.connect() as conn:
            existing = conn.execute(
                "SELECT id FROM entries WHERE dedupe_key = ?",
                (normalized["dedupe_key"],),
            ).fetchone()
            if existing:
                entry_id = int(existing["id"])
                assignments = ", ".join(f"{key} = ?" for key in normalized if key != "dedupe_key")
                values = [normalized[key] for key in normalized if key != "dedupe_key"]
                values.append(entry_id)
                conn.execute(f"UPDATE entries SET {assignments} WHERE id = ?", values)
            else:
                keys = list(normalized)
                placeholders = ", ".join("?" for _ in keys)
                columns = ", ".join(keys)
                cursor = conn.execute(
                    f"INSERT INTO entries ({columns}) VALUES ({placeholders})",
                    [normalized[key] for key in keys],
                )
                entry_id = int(cursor.lastrowid)

            self._replace_fts(conn, entry_id, normalized)
            return entry_id

    def search_entries(
        self,
        query: str = "",
        *,
        source_group: str | None = None,
        community: str | None = None,
        signal_type: str | None = None,
        entry_type: str | None = None,
        limit: int = 100,
    ) -> list[dict[str, Any]]:
        with self.connect() as conn:
            params: list[Any] = []
            filters = []
            if source_group:
                filters.append("e.source_group = ?")
                params.append(source_group)
            if community:
                filters.append("e.community = ?")
                params.append(community)
            if signal_type:
                filters.append("e.signal_type = ?")
                params.append(signal_type)
            if entry_type:
                filters.append("e.entry_type = ?")
                params.append(entry_type)

            if query.strip():
                sql = """
                    SELECT e.*
                    FROM entry_fts f
                    JOIN entries e ON e.id = f.entry_id
                    WHERE entry_fts MATCH ?
                """
                params = [self._fts_query(query), *params]
            else:
                sql = "SELECT e.* FROM entries e WHERE 1 = 1"

            if filters:
                sql += " AND " + " AND ".join(filters)
            sql += " ORDER BY e.created_at DESC, e.id DESC LIMIT ?"
            params.append(limit)
            return [self._row_to_dict(row) for row in conn.execute(sql, params).fetchall()]

    def get_entry(self, entry_id: int) -> dict[str, Any] | None:
        with self.connect() as conn:
            row = conn.execute("SELECT * FROM entries WHERE id = ?", (entry_id,)).fetchone()
            return self._row_to_dict(row) if row else None

    def set_entry_tags(self, entry_id: int, tags: list[str]) -> None:
        clean_tags = sorted({tag.strip() for tag in tags if tag.strip()})
        with self.connect() as conn:
            conn.execute("DELETE FROM entry_tags WHERE entry_id = ?", (entry_id,))
            for tag in clean_tags:
                conn.execute("INSERT OR IGNORE INTO tags (name) VALUES (?)", (tag,))
                tag_id = conn.execute("SELECT id FROM tags WHERE name = ?", (tag,)).fetchone()["id"]
                conn.execute(
                    "INSERT OR IGNORE INTO entry_tags (entry_id, tag_id) VALUES (?, ?)",
                    (entry_id, tag_id),
                )

    def get_entry_tags(self, entry_id: int) -> list[str]:
        with self.connect() as conn:
            rows = conn.execute(
                """
                SELECT t.name
                FROM tags t
                JOIN entry_tags et ON et.tag_id = t.id
                WHERE et.entry_id = ?
                ORDER BY t.name
                """,
                (entry_id,),
            ).fetchall()
            return [row["name"] for row in rows]

    def list_tags(self) -> list[str]:
        with self.connect() as conn:
            return [row["name"] for row in conn.execute("SELECT name FROM tags ORDER BY name")]

    def record_run(
        self,
        *,
        source: str,
        source_group: str,
        status: str,
        message: str = "",
        entries_seen: int = 0,
        entries_inserted: int = 0,
        started_at: str | None = None,
        finished_at: str | None = None,
    ) -> int:
        now = utc_now()
        with self.connect() as conn:
            cursor = conn.execute(
                """
                INSERT INTO runs (
                    source, source_group, status, message, entries_seen,
                    entries_inserted, started_at, finished_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    source,
                    source_group,
                    status,
                    message,
                    entries_seen,
                    entries_inserted,
                    started_at or now,
                    finished_at or now,
                ),
            )
            return int(cursor.lastrowid)

    def list_runs(self, limit: int = 50) -> list[dict[str, Any]]:
        with self.connect() as conn:
            rows = conn.execute(
                "SELECT * FROM runs ORDER BY id DESC LIMIT ?",
                (limit,),
            ).fetchall()
            return [self._row_to_dict(row) for row in rows]

    def count_entries(self) -> int:
        with self.connect() as conn:
            return int(conn.execute("SELECT COUNT(*) AS count FROM entries").fetchone()["count"])

    def list_communities(self) -> list[str]:
        with self.connect() as conn:
            rows = conn.execute(
                "SELECT DISTINCT community FROM entries WHERE community != '' ORDER BY community"
            ).fetchall()
            return [row["community"] for row in rows]

    def _normalize_entry(self, entry: dict[str, Any], fetched_at: str) -> dict[str, Any]:
        source = str(entry.get("source") or "unknown")
        external_id = str(entry.get("external_id") or "")
        url = str(entry.get("url") or "")
        title = str(entry.get("title") or "")
        dedupe_value = external_id or f"{url}::{title}"
        raw_json = entry.get("raw_json", {})
        if not isinstance(raw_json, str):
            raw_json = json.dumps(raw_json, sort_keys=True)
        return {
            "source": source,
            "source_group": str(entry.get("source_group") or ""),
            "community": str(entry.get("community") or entry.get("subreddit") or ""),
            "external_id": external_id,
            "dedupe_key": f"{source}::{dedupe_value}",
            "url": url,
            "permalink": str(entry.get("permalink") or url),
            "title": title,
            "body": str(entry.get("body") or entry.get("summary") or ""),
            "author_username": str(entry.get("author_username") or entry.get("author") or ""),
            "created_at": str(entry.get("created_at") or entry.get("updated_utc") or ""),
            "fetched_at": str(entry.get("fetched_at") or fetched_at),
            "score": int(entry.get("score") or 0),
            "comments_count": int(entry.get("comments_count") or entry.get("num_comments") or 0),
            "entry_type": str(entry.get("entry_type") or "external_export"),
            "signal_type": str(entry.get("signal_type") or "unknown"),
            "raw_json": raw_json,
        }

    def _replace_fts(self, conn: sqlite3.Connection, entry_id: int, entry: dict[str, Any]) -> None:
        conn.execute("DELETE FROM entry_fts WHERE entry_id = ?", (entry_id,))
        conn.execute(
            """
            INSERT INTO entry_fts (entry_id, title, body, community, author_username)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                entry_id,
                entry["title"],
                entry["body"],
                entry["community"],
                entry["author_username"],
            ),
        )

    def _row_to_dict(self, row: sqlite3.Row) -> dict[str, Any]:
        result = dict(row)
        if "raw_json" in result:
            try:
                result["raw_json"] = json.loads(result["raw_json"])
            except json.JSONDecodeError:
                pass
        return result

    def _fts_query(self, query: str) -> str:
        tokens = [token for token in query.replace('"', " ").split() if token]
        return " ".join(f'"{token}"' for token in tokens) if tokens else '""'
