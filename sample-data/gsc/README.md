# GSC Sample Data

These are synthetic Google Search Console-style CSV exports for testing the DuckRadar workflow.

Official data shape:

- Search Console Performance reports expose clicks, impressions, CTR, and average position.
- Data can be grouped by dimensions such as query, page, country, device, and date.
- The Search Console API response uses `clicks`, `impressions`, `ctr`, and `position`; UI CSV exports usually show similar columns with CTR formatted as a percent.

Official references:

- https://support.google.com/webmasters/answer/7576553
- https://developers.google.com/webmaster-tools/v1/searchanalytics/query

## How A Prospect Can Export This Manually

1. Open Google Search Console.
2. Select the property.
3. Go to `Performance` -> `Search results`.
4. Set date range to `Last 3 months`.
5. Click `Export`.
6. Choose Google Sheets, Excel, or CSV.
7. Send the exported `Queries`, `Pages`, and `Dates` sheets/files.

Better export if available:

- Filter to a specific important page.
- Export the queries for that page.
- Repeat for 3 money pages.

## Files

- `queries.csv`: query-level performance.
- `pages.csv`: page-level performance.
- `query_page.csv`: query + page performance, similar to what the API can return when grouped by query and page.
- `dates.csv`: daily performance for trend/decay checks.

## What We Can Do With This

- Find rank 5-20 opportunities.
- Find high-impression, low-CTR queries.
- Find pages with impressions but weak clicks.
- Detect obvious decay if date data is available.
- Prioritize which page to refresh or create.

## What This Does Not Cover

- Competitor data.
- AI/search visibility checks.
- Backlinks.
- Full technical crawling.
- Implementation inside Wix, WordPress, or another CMS.
