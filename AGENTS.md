# AGENTS.md

Project: SEO/AEO/GEO startup research and validation
Mode: Move fast, validate paid demand, then build only what repeated demand proves.

## Mission

Build a lean startup around SEO, AEO, and GEO workflows for consultants, micro-agencies, and small teams that need actionable visibility guidance without buying bloated enterprise SEO suites.

The operating loop:

1. Ideate from market evidence.
2. Narrow the ICP.
3. Define the minimum viable offer.
4. Sell manually.
5. Deliver concierge value.
6. Automate repeated work.
7. Distribute through proven channels.
8. Grow only after retention signals are real.

Primary research doc: `docs/research/seo-aeo-geo-product-discovery.md`.

Workflow guide: `docs/strategy/STARTUP_WORKFLOW.md`.

Current state / handoff doc: `CURRENT_STATE.md`.

Private prospect, outreach, reply, customer, and operator records live only in
the private `alexkubica/duckradar-private` repository. Read
`docs/PUBLICATION.md` before moving data or preparing this repository for public
visibility.

## Current Strategic Bet

Primary ICP:

Solo SEO consultants and micro-agencies managing 3-20 small business, niche content, or B2B service/SaaS sites.

Initial offer:

- `$49/site/mo` DuckRadar.
- One monthly action brief per subscribed site.
- Strict limits, no calls by default, cancel anytime.

Core positioning:

> Specific SEO workflows without the enterprise suite tax. AI/search visibility monitoring without GEO snake oil.

## How This Repo Uses Codex

- At session start, read `CURRENT_STATE.md`, `docs/strategy/OFFER.md`, `docs/strategy/REQUIREMENTS.md`, and `docs/strategy/VALIDATION_PLAN.md` before making strategic recommendations.
- Keep this file concise. `AGENTS.md` is for repo-level operating rules, not every role's full playbook.
- Push completed work to git often so the remote repo stays synced. Prefer small, coherent commits after meaningful doc, strategy, or code changes instead of letting local state drift.
- Custom startup-team subagents live in `.codex/agents/*.toml`.
- Reusable project skills live in `.agents/skills/*/SKILL.md`.
- Workflow templates live in `.agents/templates/*.template.md`.
- Use subagents only when the user explicitly asks for subagents, delegation, or parallel agent work.
- Use skills when the task matches a skill description or the user names a skill.
- Use the narrowest project-local skill that matches the task; do not import generic Alexus skills unless they fit DuckRadar's current stage.
- If docs, agents, and skills disagree, prefer the most specific file for the task and update the stale file.
- For multi-role work, create or update explicit artifacts before delegation: `docs/strategy/REQUIREMENTS.md`, `docs/strategy/AGENT_TASKS.md`, `docs/strategy/VALIDATION_PLAN.md`, `docs/strategy/TEST.md`, or `docs/strategy/DECISION_LOG.md` as appropriate.
- Do not publish the operator's personal legal name in public product pages, policy pages, outreach, reports, or product docs unless the user explicitly approves it or a provider/legal requirement cannot be satisfied with the DuckRadar brand. Prefer `DuckRadar` and `support@duckradar.com` for public-facing identity.
- Never store prospect identities, correspondence, send/reply logs, customer
  records, private analytics exports, or operator-specific automation state in
  this repository.

## Repo Workflow Hygiene

- Before editing, check `git status --short`, inspect existing files, and preserve user changes.
- Prefer isolated git worktrees for independent feature work when practical. Do not create nested worktrees.
- If running local services from multiple worktrees, assign distinct ports and record the chosen port in the handoff.
- Static site preview defaults to `4173`; worktree previews should use a different free port.
- If npm tooling is added later, keep project `.npmrc` on `https://registry.npmjs.org/` unless this repo documents another registry.
- Scale verification to the change:
  - Docs only: `git diff --check`.
  - Static site changes: preview `site/` locally and smoke-check changed pages.
  - Scripts: syntax check and dry run where possible.
  - Future npm app changes: run available format, lint, typecheck, tests, and build.
- Handoffs should include files changed, verification run, commit/push status, and open risks.

## Operating Principles

- Paid validation beats opinions.
- Concierge delivery comes before software.
- Build from repeated manual steps, not imagined dashboards.
- Avoid Semrush/Ahrefs clone scope.
- Prefer owned data first: GSC, GA4, competitors, money pages.
- Treat AI visibility as directional evidence, not deterministic ranking.
- Do not claim "GEO hacks." Use Google's guidance as the guardrail.
- Every research claim needs dated source links.
- Every build task needs a customer/use-case link.
- Every experiment needs a kill criterion before launch.
- Specialists should treat `docs/strategy/REQUIREMENTS.md`, `docs/strategy/AGENT_TASKS.md`, `docs/strategy/VALIDATION_PLAN.md`, and `docs/strategy/TEST.md` as source-of-truth files when present.

## Lean Team

Start lean. Spawn only the roles needed for the current stage.

Stage 1: Ideation and research

- `startup_manager`
- `market_researcher`
- `product_strategist`
- `seo_aeo_geo_expert`

Stage 2: Paid validation

- `brand_strategist`
- `sales_strategist`
- `copywriter`
- `marketing_growth`
- `customer_success`
- `product_strategist`
- `legal_policy_reviewer`

Stage 3: Lean build

- `architecture_strategist`
- `backend_engineer`
- `frontend_engineer`
- `designer`
- `analytics_experimenter`
- `qa_validator`

Stage 4: Distribution

- `brand_strategist`
- `marketing_growth`
- `copywriter`
- `seo_aeo_geo_expert`
- `sales_strategist`
- `analytics_experimenter`

## Default Agent Output

Every subagent should return:

- Recommended decision.
- Why it matters.
- Evidence or assumptions.
- Next action.
- Risks or kill criteria.

Avoid:

- Long generic strategy.
- Building before paid validation.
- Uncited current-market claims.
- Feature lists without buyer pain.
- AI/GEO hype language.

## File Conventions

- Keep root focused on handoff and task state: `AGENTS.md`, `README.md`, `CURRENT_STATE.md`, and `TASKS.md`.
- Keep durable strategy docs in `docs/strategy/`.
- Keep source-heavy research in `docs/research/seo-aeo-geo-product-discovery.md`.
- Keep payment setup notes in `docs/payments/`.
- Keep fulfillment templates and guides in `docs/fulfillment/`.
- Create ADRs only after technical decisions become hard to reverse, under `docs/adr/`.
- Keep custom agents narrow and opinionated.
- Keep skills reusable and task-oriented.

## Handoff Ownership

The `startup_manager` owns `CURRENT_STATE.md`.

Update `CURRENT_STATE.md` whenever:

- The offer changes.
- The ICP changes.
- Pricing changes.
- A payment/provider decision changes.
- A blocker is resolved or added.
- The next 3 priorities change.
- A validation result changes proceed/pivot/kill status.
