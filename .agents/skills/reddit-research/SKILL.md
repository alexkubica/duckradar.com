---
name: reddit-research
description: Use when researching Reddit for DuckRadar market evidence, SEO/AEO/GEO workflow pain, buyer language, competitor mentions, outreach angles, or lead-source discovery while minimizing scraping, account, IP, and compliance risk.
---

# Reddit Research

Use this for cautious Reddit market research. Prefer official Reddit API access, licensed data-provider exports, or user-supplied files. Always check Reddit's current robots and policy posture before fetching anything directly from reddit.com.

## Guardrails

- Check `https://www.reddit.com/robots.txt` before direct collection. If it disallows all crawling, do not fetch subreddit RSS, post pages, comment pages, or thread feeds directly.
- Do not use Reddit login cookies, user sessions, proxy rotation, CAPTCHA bypass, fingerprint spoofing, or rate-limit evasion.
- Do not use Reddit `.json` endpoints or subreddit search RSS.
- Do not crawl comment threads at scale.
- Use usernames only as source attribution when the data source is permitted. Do not use Reddit usernames as sales leads.
- Keep request volume small, add delays, and stop on repeated `403`, `429`, or redirect/challenge responses.
- Store minimal research data: source URL, subreddit, title, date, public username if needed for attribution, short excerpt/summary, and evidence tag.
- Treat Reddit as community evidence, not proof of willingness to pay.
- Do not build a direct outreach list from Reddit usernames alone. Leads need public business identity, website, and a non-Reddit contact path.

## Workflow

1. Define the research question and target ICP.
2. Choose source path:
   - official Reddit API access
   - licensed provider export
   - user-supplied saved pages/exports
   - direct RSS only when current robots permits it
3. Filter for current workflow pain, tool/pricing complaints, reporting pain, AI-search uncertainty, and agency/client language.
4. Open only the most relevant source links if more context is needed.
5. Synthesize:
   - workflow pain
   - repeated buyer language
   - objections and contradictions
   - offer implications
   - lead-source opportunities
6. If creating a lead list, include only prospects with public business/site evidence outside Reddit.
7. Record confidence level and sample limitations.

## Pasted Thread Workflow

Use this when direct Reddit collection is disallowed but the operator manually opens a thread and pastes the visible post/comments.

1. Pick promising cached/search result URLs from the local signals database or user-provided links.
2. Ask the operator to paste the page text and include the thread URL, subreddit, and capture date when possible.
3. Process only the pasted content. Do not fetch the Reddit thread, comments, user profiles, RSS feed, or `.json` endpoint to enrich it.
4. Extract:
   - original post question/pain
   - comment themes
   - repeated buyer language
   - objections/skepticism
   - product/workflow implications
   - lead-source clues that require non-Reddit verification
5. Label the evidence as `manual_paste` and note sample limitations, including missing collapsed/deleted comments.

Suggested paste header:

```text
URL:
Subreddit:
Captured at:
Research question:
Pasted page text:
```

## Browser Capture Guardrail

A Chrome extension is acceptable only as a manual capture helper for pages the operator intentionally opened. It should:

- Capture current visible Reddit thread content or user-selected text only.
- Send JSON to the local DuckRadar importer or download a JSON file for manual import.
- Avoid background crawling, auto-pagination, comment expansion automation, login-cookie export, CAPTCHA bypass, proxy use, or fingerprint spoofing.
- Store minimal fields: source URL, subreddit, thread title, post text, visible comments, public usernames for attribution, visible timestamps, capture timestamp.
- Require an explicit click per thread or explicit user selection before capture.

## Script

Use `scripts/collect-reddit-rss.py` only when direct RSS collection is permitted by Reddit's current robots policy. The script checks robots by default and aborts if direct collection is disallowed.

Example:

```bash
python3 .agents/skills/reddit-research/scripts/collect-reddit-rss.py \
  --subreddits SEO bigseo TechSEO localseo \
  --delay 3 \
  --output .tmp/reddit-rss.json
```

The script uses RSS only, no credentials, no Reddit API token, and a descriptive User-Agent. It is not a bypass tool.

## Output

- Evidence summary with dated source links.
- Repeated patterns and customer language.
- Contradictions and weak evidence.
- DuckRadar offer implication.
- Lead-source list, not harvested Reddit usernames.
