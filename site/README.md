# DuckRadar Website

Static website for Paddle domain review and early paid validation.

Current production deployment:

- https://duckradar.com/

Inspect deployment details in the linked Vercel project when needed.

Custom domain:

- `duckradar.com`
- `www.duckradar.com`

Spaceship DNS records for Vercel:

- Add apex `A` record: `@` -> `76.76.21.21`.
- Add `www` `CNAME` record: `www` -> `cname.vercel-dns-0.com`.

## Current checkout state

- Live checkout page: `https://duckradar.com/checkout/`
- Homepage and pricing CTAs point to the live checkout page.
- Support and sample-report requests still use `support@duckradar.com`.

## Vercel deployment

Create a Vercel project with:

- Project root: `site`
- Framework preset: Other
- Build command: empty
- Output directory: `.`

Then connect the custom domain in Vercel and submit that domain to Paddle.

The Vercel project is connected to `alexkubica/duckradar.com` on GitHub.
Pushes to `main` deploy production automatically from the `site/` root directory.

## Local preview

From the repo root:

```bash
python3 -m http.server 4173 --directory site
```

Open `http://localhost:4173`.

For parallel worktrees, do not reuse `4173`. Pick a free alternate port and run:

```bash
python3 -m http.server <port> --directory site
```

Record the chosen port in the handoff if a preview server is left running.
