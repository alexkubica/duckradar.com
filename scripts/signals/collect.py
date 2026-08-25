#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.signals.config import DEFAULT_DB_PATH, SOURCE_GROUPS
from scripts.signals.db import SignalsDB
from scripts.signals.sources.json_import import import_json_capture
from scripts.signals.sources.reddit_html import import_reddit_html_capture
from scripts.signals.sources.reddit_rss import collect_group


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Collect and import local DuckRadar signal data.")
    parser.add_argument("--db", default=str(DEFAULT_DB_PATH), help="SQLite database path.")
    parser.add_argument("--init", action="store_true", help="Initialize the database schema.")
    parser.add_argument("--import-json", help="Import a JSON capture file.")
    parser.add_argument("--import-reddit-html", help="Import a user-supplied saved Reddit HTML page.")
    parser.add_argument("--group", choices=sorted(SOURCE_GROUPS), help="Source group to collect/import.")
    parser.add_argument("--all-groups", action="store_true", help="Collect all configured groups.")
    parser.add_argument("--runs", action="store_true", help="Print recent run history.")
    parser.add_argument("--delay", type=float, default=3.0, help="Delay between allowed RSS requests.")
    parser.add_argument("--limit", type=int, default=25, help="Entries per subreddit for RSS collection.")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    db = SignalsDB(Path(args.db))

    if args.init:
        db.init_schema()
        print(f"Initialized {args.db}")

    if args.import_json:
        db.init_schema()
        if not args.group:
            print("--import-json requires --group", file=sys.stderr)
            return 2
        result = import_json_capture(db, args.import_json, args.group)
        print(f"Imported {result.inserted}/{result.seen} new entries from {args.import_json}")

    if args.import_reddit_html:
        db.init_schema()
        if not args.group:
            print("--import-reddit-html requires --group", file=sys.stderr)
            return 2
        result = import_reddit_html_capture(db, args.import_reddit_html, args.group)
        print(f"Imported {result.inserted}/{result.seen} new entries from {args.import_reddit_html}")

    if args.all_groups:
        db.init_schema()
        for group, subreddits in SOURCE_GROUPS.items():
            result = collect_group(
                db,
                source_group=group,
                subreddits=subreddits,
                delay_seconds=args.delay,
                limit_per_subreddit=args.limit,
            )
            print(f"{group}: {result.status} - {result.message}")

    if args.group and not args.import_json and not args.import_reddit_html and not args.all_groups:
        db.init_schema()
        result = collect_group(
            db,
            source_group=args.group,
            subreddits=SOURCE_GROUPS[args.group],
            delay_seconds=args.delay,
            limit_per_subreddit=args.limit,
        )
        print(f"{args.group}: {result.status} - {result.message}")

    if args.runs:
        db.init_schema()
        for run in db.list_runs():
            print(
                f"{run['id']}\t{run['finished_at']}\t{run['source_group']}\t"
                f"{run['source']}\t{run['status']}\t{run['entries_inserted']}/{run['entries_seen']}\t"
                f"{run['message']}"
            )

    if not any([args.init, args.import_json, args.import_reddit_html, args.all_groups, args.group, args.runs]):
        build_parser().print_help()
        return 2

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
