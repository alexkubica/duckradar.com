# GSC_EXPORT_GUIDE

## Can We Work With GSC CSV Exports?

Yes.

For the manual MVP, a prospect can export CSVs from Google Search Console and send them to us. We do not need API/OAuth on day one.

The useful columns are:

- Query or Page.
- Clicks.
- Impressions.
- CTR.
- Position.
- Date, if trend data is exported.

## What The CSV Lets Us Find

### Quick Wins

Queries with:

- Position between 5 and 20.
- Meaningful impressions.
- Low CTR.

These are often pages worth refreshing, retitling, expanding, or better internally linking.

### CTR Problems

Queries/pages with:

- High impressions.
- Low clicks.
- Low CTR.

These often need better titles, descriptions, intent match, or richer page content.

### Decay

Date exports can show:

- Clicks falling.
- Impressions rising while CTR falls.
- Average position worsening.

### Page Prioritization

Page exports help decide:

- Which pages already have search demand.
- Which pages are underperforming.
- Which pages deserve a content refresh first.

## What The CSV Does Not Give Us

- Competitor rankings.
- SERP layout.
- AI Overview or AI answer citations.
- Backlinks.
- Content quality by itself.

We add those manually or through providers later.

## Manual Export Instructions For Customers

Ask the customer to do this:

1. Open Google Search Console.
2. Select the client property.
3. Go to `Performance` -> `Search results`.
4. Set date range to `Last 3 months`.
5. Click `Export`.
6. Send the exported `Queries`, `Pages`, and `Dates` files.
7. Optional: filter to each money page and export queries for that page.

## API Path Later

When we automate this, use the Search Console API Search Analytics query endpoint.

Official docs:

- https://developers.google.com/webmaster-tools/v1/searchanalytics/query
- https://support.google.com/webmasters/answer/7576553

