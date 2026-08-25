# DECISION_LOG

## Decision: Start Subscription-First

Date: 2026-05-17

Owner: Human + startup_manager

Decision:

Start with a small recurring subscription, not a one-time sprint.

## Context

The target customers complain that Semrush, Ahrefs, and similar tools are expensive. A `$399` one-time sprint may validate service demand, but it does not directly validate the desired business model: recurring revenue.

## Options Considered

- `$399` one-time Search Visibility Sprint.
- `$149` one-time smaller action brief.
- `$49/site/mo` recurring DuckRadar.
- `$99/mo` bundle for multiple sites.

## Decision

Use `$49/site/mo` as the first public validation offer.

## Evidence

- Customer pain centers on expensive broad SEO tools.
- Consultants can pass per-site cost to clients more easily than a large fixed subscription.
- Recurring subscription tests retention and monthly prioritization.
- Strict scope keeps the offer deliverable manually before automation.

Confidence: Medium. This still needs paid validation.

## Tradeoffs

Upside:

- Better aligned with recurring revenue goal.
- Lower friction than a one-time `$399` service.
- Per-site metric can expand with agency client count.

Downside:

- Low ARPU can become unprofitable if fulfillment takes too long.
- Low price may attract less serious customers.
- Requires tight scope and strong process discipline.

## Follow-Up

- Validate with 50 targeted outreaches.
- Sell 10 subscriptions.
- Track fulfillment time per site.
- Revisit pricing after first 10 paid customers.

## Decision: Keep Offer, Tighten Sales Angle After Reddit Scan

Date: 2026-05-18

Owner: Human + startup_manager

Decision:

Keep the `$49/site/mo` DuckRadar offer. Do not pivot to a GEO-only tool, local SEO dashboard, or Semrush alternative. Tighten the public/sales language around a monthly decision brief: what changed, why it matters, and what to do next.

## Context

Fresh Reddit review showed continued pain around expensive broad SEO tools, client reporting overload, GSC/CTR confusion, and uncertainty around AI citations. It also showed skepticism toward small SEO tools that claim to replace large data platforms.

## Evidence

- r/localseo: low-budget local SEO operators are cutting tool costs and preferring simple one-page summaries tied to calls, GBP visibility, rankings, and GSC/GA4 trends.
- r/SEOorganic and r/SEO: Semrush replacement discussions continue, but buyers still care about reliable data for client work.
- r/GEO_optimization: practitioners are discussing citation attribution, structured claims, and AI visibility measurement, but many claims are weak, promotional, or hard to verify.
- Google Search Central's 2026-05-15 generative AI guidance says AEO/GEO work for Google Search remains grounded in standard SEO, unique/non-commodity content, crawlability, and no special "GEO hacks."

Confidence: Medium. Reddit signal is directionally useful but noisy and promotion-heavy.

## Tradeoffs

Upside:

- Keeps validation focused on paid demand.
- Avoids overpromising AI visibility.
- Uses current pain language around decision clarity and tool bloat.

Downside:

- May miss buyers who want a dedicated local SEO reporting dashboard.
- `$49/site/mo` may be too high for operators charging very low client retainers.
- The AI visibility component remains directional and must be framed carefully.

## Follow-Up

- Prioritize prospects with real SEO retainers and 3-20 client sites.
- In outreach, say "monthly decision brief" before "report."
- Ask pricing qualification questions before assuming local SEO side-hustle operators can pay.
- Treat AI visibility as a sampled snapshot and recommendation input, not a guaranteed ranking/citation product.

## Decision: Keep Offer After Reddit RSS Workflow Scan

Date: 2026-06-01

Owner: Human + Codex

Decision:

Keep the `$49/site/mo` DuckRadar validation offer. Tighten sales language toward a GSC-backed monthly decision brief with a small AI/search visibility snapshot.

## Context

The user asked whether to continue validating DuckRadar and requested recent Reddit research across SEO/AEO/GEO subreddits, with caution to avoid account/IP issues. A cautious RSS-only collection gathered 350 recent entries from 14 subreddits without login, cookies, Reddit JSON endpoints, comment crawling, or bypass tactics.

Research artifact:

- `docs/research/reddit-seo-agency-workflows-2026-06-01.md`
- `docs/strategy/REDDIT_LEAD_SOURCE_LIST_2026-06-01.md`

## Evidence

Recent Reddit posts repeatedly surfaced:

- Client reporting uncertainty around AI search visibility.
- Repetitive multi-client GSC workflows.
- Desire for recommendations with visible evidence and source signals.
- Tool/pricing fatigue around broad SEO/GEO tools.
- Continued reliance on Google rankings and GSC, despite AI-search hype.

Confidence: Medium. This is community evidence from RSS summaries, not payment evidence.

## Tradeoffs

Upside:

- Keeps validation focused and sellable.
- Avoids overreacting to GEO hype.
- Matches current pain language around client-ready decisions, GSC, and tool bloat.

Downside:

- RSS evidence does not include full comment context.
- Reddit users may be more technical and skeptical than the target buyer.
- No direct willingness-to-pay proof yet.

## Follow-Up

- Use Reddit language to refine outreach, but do not change the offer before sending the first batch.
- Build prospect lists from public business identities outside Reddit, not Reddit usernames.
- Keep the first paid validation gate: 3 paid subscriptions after 50 targeted outreaches.

## Decision: Do Not Run Direct Reddit Comment Scrape

Date: 2026-06-01

Owner: Human + Codex

Decision:

Do not expand Reddit research by directly scraping posts/comments from reddit.com while Reddit's current `robots.txt` disallows crawling for all user agents.

## Context

The user asked to expand the Reddit scan to at least 1,000 entries, store Reddit usernames, and load posts/comments. A preflight check of `https://www.reddit.com/robots.txt` returned `User-agent: *` and `Disallow: /`.

The `reddit-research` skill and RSS collector were updated so direct collection checks robots first and aborts when global disallow is present.

## Evidence

- Reddit robots preflight on 2026-06-01: global disallow for all user agents.
- Reddit Public Content Policy says Reddit supports non-commercial learning/community uses but asks users to talk to Reddit for commercial purposes and describes restrictions around bulk public-content access.

Confidence: High for the collection decision. The current direct collection path is not appropriate.

## Follow-Up

- Use official Reddit API access, licensed provider exports, or user-supplied saved/exported files for comment-level research.
- Reddit usernames may be stored as source attribution only when the source path is permitted.
- Do not use Reddit usernames as sales leads without public business identity and non-Reddit contact evidence.
