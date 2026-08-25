# AI-Native Startup Workflow

This project adapts Codex's AI-native engineering guidance to a lean startup loop:

1. Plan with explicit artifacts.
2. Delegate narrow work to specialized agents.
3. Gate handoffs on completed files or measurable evidence.
4. Review before moving to the next stage.
5. Automate only repeated, validated work.

Primary references:

- https://developers.openai.com/codex/guides/build-ai-native-engineering-team
- https://developers.openai.com/cookbook/examples/codex/codex_mcp_agents_sdk/building_consistent_workflows_codex_cli_agents_sdk

## Operating Model

Use `startup_manager` as the coordinator. The manager should not spawn every role by default. It should select the smallest team needed for the current stage and define the deliverables before work starts.

The cookbook pattern to preserve:

- One manager receives the broad task.
- The manager writes or updates planning artifacts.
- Specialists work from those artifacts.
- The manager checks required outputs before advancing.
- QA/validation reviews before customer-facing or build decisions.

## Standard Artifacts

Use these files when the project needs more structure:

- `docs/strategy/REQUIREMENTS.md`: product goal, target users, scope, constraints.
- `docs/strategy/AGENT_TASKS.md`: role-specific work packages and deliverables.
- `docs/strategy/VALIDATION_PLAN.md`: hypotheses, experiments, success metrics, kill criteria.
- `docs/strategy/TEST.md`: acceptance criteria for software or customer-facing artifacts.
- `docs/strategy/DECISION_LOG.md`: important decisions, date, evidence, owner.

Do not create all artifacts for every task. Use the smallest set that reduces ambiguity.

## Gated Workflow: Research To Offer

1. Manager defines the research question and target ICP.
2. Researcher gathers evidence and source links.
3. Product strategist proposes ICP, JTBD, offer, exclusions, and pricing logic.
4. SEO/AEO/GEO expert checks claims and feasibility against search reality.
5. Manager decides proceed, narrow, pivot, or kill.

Required gate:

- Research has source links.
- ICP has exclusions.
- Offer has a price and kill criteria.

## Gated Workflow: Offer To Sales Test

1. Product strategist defines the offer.
2. Copywriter writes landing/outbound copy.
3. Sales strategist writes qualification and discovery scripts.
4. Marketing/growth defines distribution channels.
5. Analytics experimenter defines metrics.
6. QA validator checks claims and measurable criteria.

Required gate:

- One ICP.
- One offer.
- One CTA.
- One success metric.
- One kill criterion.

## Gated Workflow: Sales Test To Build

1. Customer success documents manual delivery steps.
2. Architecture strategist identifies repeated steps and technical risks.
3. Backend/frontend engineers automate only repeated validated steps.
4. QA validator verifies behavior against `docs/strategy/TEST.md`.
5. Analytics experimenter checks activation and retention signals.

Required gate:

- At least 10 paid subscriptions or equivalent direct-buying evidence.
- Repeated manual step identified.
- Build task tied to customer-visible value.
- Cost and ToS risks documented.

## Human-Owned Decisions

Agents can draft, research, implement, and review. Humans still own:

- Final ICP choice.
- Pricing changes.
- Brand positioning.
- Customer promises.
- Legal/ToS risk acceptance.
- Strategic pivots.
- Any customer-facing claim that could damage trust.
