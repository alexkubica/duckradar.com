# Local Signals Database Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a local SQLite-backed signals database with import, guarded collection, search, tagging, and an internal browser for DuckRadar ideation, leads, and market signals.

**Architecture:** Implement a small Python package under `scripts/signals/`. Use SQLite FTS5 for search and Python's standard-library HTTP server for the local UI to avoid adding deployment dependencies in V1. Source adapters normalize permitted RSS/API/provider/manual exports into a shared `entries` table.

**Tech Stack:** Python 3 standard library, SQLite/FTS5, `unittest`, local HTTP server.

---

## File Map

- Create `scripts/__init__.py`: make `scripts` importable for tests.
- Create `scripts/signals/__init__.py`: package marker.
- Create `scripts/signals/config.py`: subreddit source groups and default DB path.
- Create `scripts/signals/db.py`: SQLite schema, upserts, search, tags, run history.
- Create `scripts/signals/classify.py`: lightweight keyword classifier for signal types.
- Create `scripts/signals/sources/__init__.py`: source adapter package marker.
- Create `scripts/signals/sources/json_import.py`: import existing RSS/provider JSON captures.
- Create `scripts/signals/sources/reddit_rss.py`: guarded RSS collector that aborts if robots disallows direct collection.
- Create `scripts/signals/collect.py`: CLI for init, import, collect, and run status.
- Create `scripts/signals/serve.py`: local internal web UI.
- Create `tests/signals/test_db.py`: database behavior.
- Create `tests/signals/test_classify.py`: classifier behavior.
- Create `tests/signals/test_json_import.py`: fixture import behavior.
- Create `tests/signals/test_reddit_rss.py`: robots abort behavior.
- Modify `.gitignore`: ignore `data/`.

## Task 1: Database Core

**Files:**

- Create: `scripts/__init__.py`
- Create: `scripts/signals/__init__.py`
- Create: `scripts/signals/db.py`
- Create: `tests/signals/test_db.py`
- Modify: `.gitignore`

- [ ] Write failing tests for schema initialization, upsert dedupe, FTS search, tags, and run history.
- [ ] Run `python3 -m unittest tests.signals.test_db -v` and confirm it fails because `scripts.signals.db` does not exist.
- [ ] Implement `SignalsDB` with `init_schema`, `upsert_entry`, `search_entries`, `set_entry_tags`, `list_tags`, `record_run`, and `list_runs`.
- [ ] Run `python3 -m unittest tests.signals.test_db -v` and confirm it passes.
- [ ] Commit as `Add signals database core`.

## Task 2: Source Groups And Classifier

**Files:**

- Create: `scripts/signals/config.py`
- Create: `scripts/signals/classify.py`
- Create: `tests/signals/test_classify.py`

- [ ] Write failing tests that assert configured `seo`, `marketing`, and `sales` groups include the user-requested subreddits.
- [ ] Write failing tests that classify example records as `tool_pricing`, `agency_reporting`, `ai_search`, `sales_outreach`, `lead_source`, and `unknown`.
- [ ] Run `python3 -m unittest tests.signals.test_classify -v` and confirm failure.
- [ ] Implement config constants and `classify_signal(title, body)`.
- [ ] Run `python3 -m unittest tests.signals.test_classify -v` and confirm it passes.
- [ ] Commit as `Add signal groups and classifier`.

## Task 3: JSON Importer

**Files:**

- Create: `scripts/signals/sources/__init__.py`
- Create: `scripts/signals/sources/json_import.py`
- Create: `tests/signals/test_json_import.py`

- [ ] Write failing tests using a temporary RSS-style fixture with two entries and one duplicate.
- [ ] Run `python3 -m unittest tests.signals.test_json_import -v` and confirm failure.
- [ ] Implement `import_json_capture(db, path, source_group)` for the existing `.tmp/reddit-seo-rss-2026-06-01.json` format and generic `entries` arrays.
- [ ] Run `python3 -m unittest tests.signals.test_json_import -v` and confirm it passes.
- [ ] Commit as `Add signals JSON importer`.

## Task 4: Guarded Reddit RSS Adapter

**Files:**

- Create: `scripts/signals/sources/reddit_rss.py`
- Create: `tests/signals/test_reddit_rss.py`

- [ ] Write failing tests for `robots_allows_direct_collection` returning false when robots contains `User-agent: *` and `Disallow: /`.
- [ ] Write failing tests that `collect_group` records an aborted run and performs no subreddit fetches when robots disallows collection.
- [ ] Run `python3 -m unittest tests.signals.test_reddit_rss -v` and confirm failure.
- [ ] Implement the guarded RSS adapter using injected fetch functions for tests.
- [ ] Run `python3 -m unittest tests.signals.test_reddit_rss -v` and confirm it passes.
- [ ] Commit as `Add guarded Reddit RSS adapter`.

## Task 5: CLI

**Files:**

- Create: `scripts/signals/collect.py`
- Test through existing DB/import/RSS tests plus CLI smoke commands.

- [ ] Implement CLI commands:
  - `--init`
  - `--import-json PATH --group GROUP`
  - `--all-groups`
  - `--group GROUP`
  - `--runs`
  - `--db PATH`
- [ ] Run `python3 scripts/signals/collect.py --init --db .tmp/test-signals.sqlite`.
- [ ] Run `python3 scripts/signals/collect.py --import-json .tmp/reddit-seo-rss-2026-06-01.json --group seo --db .tmp/test-signals.sqlite`.
- [ ] Run `python3 scripts/signals/collect.py --runs --db .tmp/test-signals.sqlite`.
- [ ] Run all unit tests.
- [ ] Commit as `Add signals collector CLI`.

## Task 6: Internal Web UI

**Files:**

- Create: `scripts/signals/serve.py`

- [ ] Implement local HTTP server with:
  - `/` search/list page
  - `/entry?id=...` detail page
  - `/tag` POST endpoint for manual tags
  - `/runs` run history page
- [ ] Use restrained internal-tool HTML/CSS, no public landing page.
- [ ] Run local server on port `8787`.
- [ ] Verify search page loads and returns seeded entries.
- [ ] Commit as `Add local signals browser`.

## Task 7: Seed And Verify

**Files:**

- No new files expected.

- [ ] Initialize `data/signals.sqlite`.
- [ ] Import `.tmp/reddit-seo-rss-2026-06-01.json` as `seo`.
- [ ] Run the guarded hourly collector command and confirm it records an aborted run when Reddit robots disallow direct collection.
- [ ] Start the internal browser.
- [ ] Run `python3 -m unittest discover -s tests -v`.
- [ ] Commit any final docs or fixes.

## Notes

- Do not commit `data/`, `.tmp/`, API credentials, or provider exports.
- Store Reddit usernames only as attribution when present in permitted/imported data.
- Do not add Reddit usernames to outreach lists.
- Prefer importing API/provider/manual exports over direct collection until Reddit access is resolved.
