# Public Repository Boundary

DuckRadar's public repository may contain product code, the marketing site,
synthetic sample data, reusable report templates, and public-safe product
strategy.

It must not contain:

- prospect or customer names, email addresses, domains, or identifiers;
- outreach drafts tied to real people, approvals, send logs, or reply state;
- customer onboarding, fulfillment, subscription, or feedback records;
- mailbox, SMTP, IMAP, Paddle server, or deployment credentials;
- operator-specific scheduling files or absolute workstation paths;
- private GSC, GA4, or customer-site exports.

Those records belong in the private `alexkubica/duckradar-private` repository.

The Paddle token embedded in `site/checkout/index.html` is a browser-side client
token and is expected to be visible. Paddle API keys, webhook secrets, and
other server credentials must never be committed.

## Clean publication history

The pre-split history containing private outreach records is preserved only in
the private `alexkubica/duckradar-history-private` archive. The repository
intended for publication was recreated from the sanitized tree with one
parentless initial commit on 2026-08-25.

Keep both `duckradar-history-private` and `duckradar-private` private. Run a
full-history secret and personal-data scan before every visibility change.
