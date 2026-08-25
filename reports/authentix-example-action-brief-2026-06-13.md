# DuckRadar Example Action Brief: Authentix Israel

Site: https://www.authentix.co.il  
Date: 2026-06-13  
Prepared for: Authentix Israel  
Status: Public crawl plus search sample. GSC exports pending.

## Summary

Authentix now has a much stronger public SEO base than the older sample: a Hebrew RTL site, current sitemap with 11 URLs, commercial package page, portfolio page, three article pages, clean HTTPS, `www` canonicalization, and visible article navigation. The highest leverage next move is to connect Search Console query data to the right commercial page. Publicly, the strongest candidate is a focused money page around `ניהול סושיאל מדיה לעסקים` or `הפקת רילסים וטיקטוק לעסקים`, supported by the existing article, packages page, portfolio examples, and homepage internal links.

The report is not complete until GSC data is added. Without GSC, we cannot rank the real opportunities by impressions, clicks, CTR, or average position.

## What We Could Verify Publicly

Verified on 2026-06-13:

- `https://authentix.co.il/` redirects with `308` to `https://www.authentix.co.il/`.
- Homepage returns `200`.
- Robots allows crawling and points to `https://www.authentix.co.il/sitemap.xml`.
- Current sitemap lists 11 URLs.
- Current sitemap includes homepage, articles index, packages, portfolio, four legal pages, and three article pages.
- Pages use `lang="he"` and `dir="rtl"`.
- Homepage title is `אותנטיקס ישראל | שיווק דיגיטלי לעסקים בישראל`.
- Homepage description targets digital marketing, content, social media, landing pages, and WhatsApp lead flow.
- Homepage has index/follow robots meta and a canonical URL.
- Homepage and article pages expose JSON-LD in static HTML.
- Old indexed URLs `/משפיענים` and `/סדנאות` redirect to current pages.
- Old URL `/מיתוג` currently returns 404.

## Top 5 GSC Opportunities

Requires Google Search Console exports.

| Priority | Page | Query | Signal Needed | Recommended Action |
|---|---|---|---|---|
| 1 | Pending | Pending | Queries in positions 5 to 20 with impressions | Pick first page to refresh or expand |
| 2 | Pending | Pending | High impressions with low CTR | Rewrite title, description, and opening section |
| 3 | Pending | Pending | Page with impressions but no clear conversion path | Add CTA and internal links to packages |
| 4 | Pending | Pending | Old redirected or 404 URL with impressions | Redirect or rebuild based on query demand |
| 5 | Pending | Pending | Article receiving impressions for commercial query | Link it to the matching money page |

## Public Technical Findings

### 1. Current Sitemap Is Clean, But Legal Pages Are Included

The sitemap currently includes:

- Homepage
- Articles index
- Packages
- Portfolio
- Privacy
- Cookies
- Accessibility
- Terms
- Three article pages

This is not a major technical problem, but legal pages are low SEO value. If GSC shows them getting impressions, they may muddy reporting. Consider removing legal pages from the XML sitemap or setting them to `noindex` if there is no reason for them to appear in search.

### 2. Old URLs Need GSC Review

Google search still surfaced older URLs such as:

- `/משפיענים`
- `/סדנאות`

Both redirect correctly to relevant current pages:

- `/משפיענים` redirects to `/עבודות`
- `/סדנאות` redirects to `/חבילות`

The old `/מיתוג` URL returns `404`.

Recommended action:

Check GSC for impressions and clicks on these old URLs. If `/מיתוג` has any search demand or backlinks, redirect it to the closest current page or rebuild a branding page.

### 3. Packages Page Is The Main Commercial Page

The packages page has clear commercial intent and lists:

- Monthly social media management
- Reels and TikTok package
- Image and reputation content
- Paid campaign
- Brand video
- Stills

Recommended action:

Treat this as the first conversion page. Add short internal anchor links near the top so users and search engines can jump to each service section. Add one FAQ block around pricing, filming day, approval flow, deliverables, and whether content is adapted for TikTok, Instagram, and Facebook.

### 4. Articles Exist, But Need Stronger Money Page Support

The articles index and three articles are live:

- `digital-marketing-for-small-businesses`
- `social-media-management-for-businesses`
- `landing-page-seo-basics`

This is a good content base. The next step is not more generic articles. The next step is to use GSC to decide which article is already earning impressions, then add internal links from that article to the packages page or a focused service page.

### 5. Search Results Show Early Brand And Exact Topic Visibility

Search samples found Authentix pages for branded and exact topic searches, including the homepage, articles index, packages page, and portfolio page. For broader generic searches, competitor/service pages also appear, especially around landing page SEO and Reels production.

Recommended action:

Do not judge generic ranking from one manual search. Use GSC query rows to find where Authentix is already close to page one or already earning impressions for service terms.

## Competitor / SERP Gaps

| Gap | Public Signal | Recommended Action |
|---|---|---|
| Reels production | Search samples surfaced dedicated Reels/video service pages from other providers. | Create or expand a focused page for `הפקת רילסים לעסקים` or `חבילת רילסים וטיקטוק לעסקים`. |
| Landing page SEO | Search samples showed multiple SEO specialists with dedicated landing page SEO articles. | Keep the current article, but link it to a clear landing-page-build offer if this is a service you want to sell. |
| Social media management | Authentix has both article and package content, but no single deep commercial service page. | Build a service page for `ניהול סושיאל מדיה לעסקים` if GSC shows impressions around this topic. |
| Portfolio proof | Portfolio has strong examples and logos, but examples are mostly grouped as media items. | Turn 2 to 3 best examples into mini case studies with client type, service, platform, and result context. |

## AI / Search Visibility Snapshot

Not run through an AI visibility provider. This section is directional only.

Suggested monthly prompts:

1. איזו סוכנות שיווק דיגיטלי מומלצת לעסקים בישראל?
2. מי עושה ניהול סושיאל מדיה לעסקים בישראל?
3. מי מפיק רילסים וטיקטוק לעסקים בישראל?
4. מי בונה דפי נחיתה לעסקים בישראל?
5. איזו סוכנות מתאימה לצילום ותוכן תדמיתי לעסק?
6. איך בוחרים חבילת סושיאל מדיה חודשית?
7. איך לבנות נוכחות דיגיטלית לעסק קטן?
8. מי עושה סרטון תדמית לעסק בישראל?
9. איך לשלב דף נחיתה עם SEO?
10. אותנטיקס ישראל

Caveat:

AI and search visibility checks are sampled evidence, not rankings. They should be used to spot source gaps and messaging gaps, not to promise inclusion in AI answers.

## 3 Actions For Next Month

1. Export GSC data and choose the first page to expand based on impressions and position.
2. Fix stale URL handling by redirecting `/מיתוג` or rebuilding it if GSC shows demand.
3. Create or expand one commercial service page around the strongest GSC theme, likely `ניהול סושיאל מדיה לעסקים` or `הפקת רילסים וטיקטוק לעסקים`.

## Content Brief

Page to create or expand:

`ניהול סושיאל מדיה לעסקים`

Search intent:

Business owner in Israel comparing providers for ongoing social media management across TikTok, Instagram, and Facebook.

Recommended structure:

- What monthly social media management includes.
- Who this is for: small businesses, clinics, service businesses, brands.
- Platforms: TikTok, Instagram, Facebook.
- Deliverables: content calendar, filming, Reels, posts, stories, creative, captions, chat response if included.
- Process: strategy, filming day, editing, approval, publishing, reporting.
- Examples from portfolio.
- Package links: monthly social media management and Reels/TikTok package.
- FAQ: price range, minimum commitment, posting frequency, filming location, who approves content, how WhatsApp leads are tracked.
- CTA: WhatsApp.

Internal links to add:

- Homepage service block to this page.
- Packages page monthly social package to this page.
- Article `social-media-management-for-businesses` to this page.
- Portfolio examples to this page where examples are relevant.

## GSC Data Needed To Complete The Real Report

Export these from Google Search Console:

1. `Performance` then `Search results`
2. Date range: `Last 3 months`
3. Export `Queries`
4. Export `Pages`
5. Export `Dates`
6. Optional but useful: filter to `/חבילות`, `/עבודות`, and each article, then export queries for each page
7. Also export or screenshot `Indexing` then `Pages`, especially not indexed and 404 rows

Put exports locally under:

`data/gsc/authentix/`

Suggested filenames:

- `queries.csv`
- `pages.csv`
- `dates.csv`
- `query_page.csv` if available
- `indexing-pages.csv` if available

Do not commit private GSC exports to git.

## Caveats

- This version uses public crawl data and manual search samples only.
- GSC data is required for the real top 5 opportunity ranking.
- Google data may be delayed or aggregated.
- AI/search visibility is directional and sampled.
- No rankings, traffic, leads, or AI answer inclusion are guaranteed.

## Sources

- Homepage: https://www.authentix.co.il/
- Robots: https://www.authentix.co.il/robots.txt
- Sitemap: https://www.authentix.co.il/sitemap.xml
- Articles: https://www.authentix.co.il/articles
- Packages: https://www.authentix.co.il/%D7%97%D7%91%D7%99%D7%9C%D7%95%D7%AA
- Portfolio: https://www.authentix.co.il/%D7%A2%D7%91%D7%95%D7%93%D7%95%D7%AA
- Google Search sample, `site:authentix.co.il אותנטיקס ישראל`, checked 2026-06-13
- Google Search sample, `ניהול סושיאל מדיה לעסקים אותנטיקס`, checked 2026-06-13
- Google Search sample, `דף נחיתה SEO אותנטיקס`, checked 2026-06-13
