# Local Signals Database Design

Date: 2026-06-02

## Purpose

Build a local-first signals database for DuckRadar research. The system should cache permitted Reddit-derived RSS/API/provider/manual-import data plus future marketing and sales signals, then provide an internal browser for ideation, lead-source discovery, buyer pain research, and offer validation.

This is an internal research tool, not a customer-facing product.

## Current Constraint

Direct Reddit collection must respect Reddit's current policy and robots posture.

As of the last preflight, `https://www.reddit.com/robots.txt` returned global disallow for all user agents. Therefore, the Reddit RSS adapter must check robots before every direct fetch and abort safely when collection is disallowed.

The app should still be useful with:

- existing `.tmp/` RSS captures,
- official Reddit API access if approved later,
- licensed provider exports such as Apify/Bright Data,
- manually saved/exported post/comment data.

## Scope

V1 is local-only:

- SQLite database under `data/signals.sqlite`.
- Local web UI at `http://localhost:8787`.
- Command-line collector/importer.
- No public deployment.
- No authentication.
- Cached raw/source data stays out of git.

Deployment, multi-user auth, hosted Postgres, and production scheduling are later decisions.

## Source Groups

The configured subreddit groups are:

### SEO

`Agentic_SEO`, `GEO_optimization`, `RankWithAI`, `SEO`, `SEO_Digital_Marketing`, `SEOandBacklinks`, `SEOorganic`, `ShopifySEO`, `TechSEO`, `aeo`, `bigseo`, `juststart`, `localseo`, `seogrowth`.

### Marketing

`AISEOforBeginners`, `AskMarketing`, `ColdEmailsForLiving`, `Coldemailing`, `DigitalMarketing`, `EmailOutreach`, `Emailmarketing`, `GEO_optimization`, `InstagramMarketing`, `PPC`, `SaaSMarketing`, `SocialMediaMarketing`, `b2bmarketing`, `coldemail`, `content_marketing`, `digital_marketing`, `marketing`.

### Sales

`LeadGenMarketplace`, `LeadGeneration`, `Sales_Professionals`, `googleads`, `sales`, `salestechniques`, `techsales`.

## Architecture

Use Python standard tooling plus a small web stack:

```text
scripts/signals/
  collect.py
  serve.py
  db.py
  classify.py
  sources/
    reddit_rss.py
    reddit_api.py
    apify_import.py
    json_import.py
```

Recommended dependencies:

- `fastapi`
- `uvicorn`
- `jinja2`

SQLite's built-in FTS5 handles search. Avoid a heavier search engine until local usage proves it is needed.

## Data Model

SQLite tables:

```text
source_groups
communities
entries
entry_fts
runs
tags
entry_tags
```

`entries` stores normalized records:

```text
id
source
source_group
community
external_id
url
permalink
title
body
author_username
created_at
fetched_at
score
comments_count
entry_type
signal_type
raw_json
```

`entry_type` values:

- `post`
- `comment`
- `rss_entry`
- `external_export`

`signal_type` values should start simple:

- `pain`
- `lead_source`
- `idea`
- `competitor`
- `workflow`
- `tool_pricing`
- `ai_search`
- `agency_reporting`
- `sales_outreach`
- `unknown`

Dedupe rule:

- Prefer `source + external_id` when available.
- Fall back to normalized `source + url + title`.

## Collection Behavior

The collector supports source adapters.

### Reddit RSS Adapter

Purpose: collect subreddit RSS entries only when current robots permits direct collection.

Rules:

- Fetch `https://www.reddit.com/robots.txt` before direct collection.
- Abort the run if robots has `User-agent: *` with `Disallow: /`.
- Do not use login cookies, browser sessions, proxies, CAPTCHA handling, `.json` endpoints, or Playwright.
- Add delays between allowed requests.
- Record aborted runs in `runs`.

### Reddit API Adapter

Purpose: use official OAuth if credentials are approved later.

Rules:

- Credentials live in `.env`, never committed.
- Use descriptive User-Agent.
- Respect rate-limit headers.
- Poll `/new` for focused subreddit groups.
- Fetch comments only for selected/relevant posts.

### Provider/Manual Import

Purpose: ingest Apify/Bright Data/manual JSON or CSV exports.

Rules:

- Preserve provider/source metadata.
- Normalize author usernames as source attribution only.
- Do not add Reddit usernames directly to outreach lists.

## Internal Web UI

The internal site should prioritize scanning and search:

- Search box using FTS.
- Filters: source group, community, source, date range, signal type, entry type.
- List view with title, community, date, source, author, snippet, tags.
- Detail view with full cached body, source URL, metadata, raw JSON toggle.
- Tag controls for manual classification.
- "Copy evidence note" action.
- Run history page showing successful, failed, and aborted runs.

No marketing-style landing page. The first screen should be the usable search/browse interface.

## Hourly Scheduling

Provide a local command:

```bash
python3 scripts/signals/collect.py --all-groups
```

The user can run this manually or wire it to cron/launchd. The app should not require a resident background process for V1.

If direct Reddit RSS is disallowed, the hourly job should:

- record an aborted run,
- exit non-zero or with a clear status,
- avoid making subreddit fetches,
- leave existing cached data intact.

## Safety And Compliance

- Cache data locally only.
- Do not commit `data/`, `.tmp/`, or exported raw datasets.
- Store usernames only as attribution where the source path is permitted.
- Do not use Reddit usernames as leads.
- Do not include bypass techniques.
- Keep provider/API credentials in `.env`.

## Tests

Use test-first implementation for core behavior:

- Database schema initializes cleanly.
- Entry upsert dedupes records.
- FTS search returns matching title/body records.
- Classifier assigns expected simple signal types.
- Reddit RSS adapter aborts when robots disallows direct collection.
- Importer ingests a fixture export into normalized entries.
- Web search endpoint returns filtered results.

## Acceptance Criteria

V1 is complete when:

- `data/signals.sqlite` can be initialized locally.
- Source groups and subreddits are configured.
- Existing RSS JSON captures can be imported.
- Search UI works locally.
- Tagging works.
- Run history is visible.
- Hourly collector command exists and aborts safely when Reddit direct collection is disallowed.
- Raw/cache data is ignored by git.

## Out Of Scope

- Hosted deployment.
- User accounts/auth.
- Public sharing.
- Reddit scraping through browser automation.
- Contact enrichment.
- Automated outreach.
- Full lead CRM.
