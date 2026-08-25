# Search And AI Visibility Methodology

Last updated: 2026-06-14

Use this when preparing DuckRadar monthly action briefs.

## Diagnosis

DuckRadar briefs are GSC-first SEO decision memos. Standard GSC Performance data is the primary source for prioritizing work because it shows real Google Search clicks, impressions, CTR, average position, pages, and queries.

Google's Search Generative AI performance reports launched on 2026-06-03 and should be used when available, but they are not universal yet. If the report is missing, unavailable, or sparse, do not infer no AI visibility. Label the data state and continue with standard GSC plus a small directional prompt sample.

## Evidence Priority

1. Standard GSC Performance data: primary decision source.
2. GSC Generative AI report: first-party Google AI visibility signal when available.
3. Live Google/SERP observations: spot-check context only.
4. External AI prompt sampling: directional, non-exhaustive evidence.

## Monthly Data States

| Data State | How To Report It | How To Interpret It |
| --- | --- | --- |
| Standard GSC available | Use last 3 complete months, plus prior-period comparison where useful. | Prioritize pages and queries by impressions, CTR, average position, trend, and business value. |
| GSC Generative AI report available | Add a short subsection for AI Overviews or AI Mode impressions, top pages, country/device/date patterns. | Treat as Google AI-feature visibility evidence, not clicks, rankings, leads, or total AI visibility. |
| GSC Generative AI report sparse | Label it available but too sparse to trend. | Use as a watchlist only unless repeated across pages or dates. |
| GSC Generative AI report unavailable | Say the property does not currently show the report or enough data. | Do not treat this as zero AI visibility. Continue with standard GSC and prompt sampling. |
| External prompt sample run | Log exact prompt, platform, date, location/language, client status, competitors, cited sources. | Use to find source and content gaps, not to claim AI rankings. |

## Prompt Sampling Method

Use 10 prompts per subscribed site per month.

Keep 6 prompts fixed month to month and rotate 4 prompts based on current GSC opportunities, seasonality, or client priorities.

Recommended mix:

- 3 high-intent GSC queries tied to money pages.
- 2 close-to-page-one GSC opportunities, usually average position 5 to 20.
- 2 service or problem prompts, especially for local SEO.
- 1 competitor or comparison prompt.
- 1 brand or reputation prompt.
- 1 source-discovery prompt, such as `best [category] providers for [use case]`.

For each prompt, record:

- Exact prompt or query.
- Platform checked.
- Date checked.
- Country, city, and language context.
- Client status: `cited`, `mentioned`, `visible in source set`, or `absent`.
- Competitor status.
- Sources cited or surfaced.
- Recommended action.

## Local SEO Prompt Rules

Local prompts must include explicit service and geography. Do not rely on `near me` unless the test location is controlled and documented.

Examples:

- `best [service] in [city]`
- `who should I call for [problem] in [city]`
- `[business] vs [competitor] for [service] in [city]`
- `is [business] a good option for [service] in [city]`
- `top-rated [service] provider for [audience] in [city]`

For local clients, interpret prompt results through practical source gaps:

- GBP completeness
- Reviews
- Service pages
- Local directories
- Local listicles
- Citations
- Competitor pages
- Proof and case studies

## Recommended Actions

- If standard GSC shows a clear SEO opportunity, prioritize that over AI prompt noise.
- If GSC Generative AI impressions appear for specific pages, inspect those pages for clearer answers, stronger proof, better internal links, and matching visible structured data.
- If competitors are cited repeatedly outside Google, inspect the source pattern before acting. A directory/listicle gap needs a different action than a weak service page.
- If AI data is unavailable or sparse, keep the action plan grounded in GSC opportunities and treat AI checks as a watchlist.

## Client-Ready Section Template

```md
## AI / Search Visibility Snapshot

Data status: Standard Search Console data was available for this report. The GSC Generative AI performance report was [available / unavailable / available but too sparse to trend] for this property as of [date].

Interpretation: This section is a directional visibility check. Search Console remains the main decision source. AI/search observations are used to find content, source, and competitor gaps. They are not rankings and do not guarantee inclusion in AI answers.

| Prompt / Query | Client Status | Competitor / Source Pattern | Recommended Action |
| --- | --- | --- | --- |
| [prompt] | cited / mentioned / absent | [competitor/source] | [action] |
| [prompt] | cited / mentioned / absent | [competitor/source] | [action] |
| [prompt] | cited / mentioned / absent | [competitor/source] | [action] |

This month's useful signal: [one concise interpretation]

Recommended action: [one concise action]

Caveat: Missing or sparse GSC Generative AI data does not mean the site has no AI visibility. External prompt checks are sampled observations and may vary by location, personalization, model, and date.
```

## What Not To Claim

Do not claim:

- You rank in ChatGPT.
- The site has no AI visibility because a GSC AI report is missing.
- We can guarantee AI Overview, AI Mode, ChatGPT, or Perplexity inclusion.
- GEO hacks, special schema, `llms.txt`, chunking, or fake mentions are required for Google AI visibility.
- Manual prompt samples represent full market share, share of voice, or all user prompts.
- GSC Generative AI impressions equal clicks, leads, revenue, or rankings.

## Sources

- Google Search Central, Search Generative AI performance reports: https://developers.google.com/search/blog/2026/06/gen-ai-performance-reports
- Google Search Console Help, Generative AI performance report: https://support.google.com/webmasters/answer/16984139
- Google Search Central, AI features and your website: https://developers.google.com/search/docs/appearance/ai-features
- Google Search Central, optimizing for generative AI features: https://developers.google.com/search/docs/fundamentals/ai-optimization-guide
- Google Search Console Help, Performance report: https://support.google.com/webmasters/answer/7576553

