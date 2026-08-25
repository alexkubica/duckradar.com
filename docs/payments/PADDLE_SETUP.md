# PADDLE_SETUP

Goal: collect real `$49/site/mo` subscriptions for DuckRadar without building a full app.

Official references:

- Paddle subscriptions overview: https://developer.paddle.com/api-reference/subscriptions/overview
- Paddle checkout overview: https://developer.paddle.com/concepts/sell/self-serve-checkout/
- Paddle onboarding overview: https://developer.paddle.com/build/onboarding/overview/
- Default payment link: https://developer.paddle.com/build/transactions/default-payment-link
- Customer portal: https://developer.paddle.com/concepts/sell/customer-portal
- Supported countries: https://developer.paddle.com/concepts/sell/supported-countries-locales/
- Paddle seller handbook: https://www.paddle.com/seller-guides/seller-handbook

## Product

Name:

DuckRadar

Price:

`$49/site/mo`

Billing:

- Monthly recurring subscription.
- Cancel anytime.
- No setup fee during validation.

## Checkout Strategy

Use a real Paddle checkout, not a fake purchase button.

Primary landing page CTA:

> Start one site for $49/mo

Post-payment flow:

1. Customer pays through Paddle.
2. Customer lands on a thank-you/onboarding page.
3. Customer fills onboarding form or receives it by email.
4. Customer sends GSC export or grants read-only access.
5. First brief is delivered manually within 5 business days.

## Minimal Paddle Setup

1. Create or log into Paddle account.
2. Add business details and complete account review requirements.
3. Add approved website/domain for checkout.
4. Create product: `DuckRadar`.
5. Create recurring monthly price: `$49/mo`.
6. Set default payment link in Paddle checkout settings to an approved domain page that includes Paddle.js.
7. Create checkout/payment link for the product.
8. Add the checkout link to landing page CTA.
9. Configure customer emails/receipt settings.
10. Enable or link Paddle customer portal cancellation handling.
11. Set cancellation/refund/support language clearly.

## Landing Page Requirements For Approval / Trust

Include:

- Product name.
- Price and billing interval.
- What is included.
- What is not included.
- Delivery timeline.
- Cancellation policy.
- Refund policy.
- Privacy note for GSC data.
- Contact email.
- Terms / privacy links if available.

Support email:

`support@duckradar.com`

Use this for buyer support, policy requests, onboarding, and Paddle review.

Customer portal:

`https://customer-portal.paddle.com/cpl_01krv4zd2sqdnskxwpc2brwysg`

Status: completed on 2026-05-18. The website Terms identify the DuckRadar brand and support contact. Paddle's seller guidance says terms, refund policy, privacy policy, pricing, deliverables, and buyer support details must be clearly accessible, and asks sellers to include the company name or sole proprietor's brand in the Terms & Conditions, with legal name preferred for sole proprietors.

## Fulfillment Checklist After Payment

Send customer:

- `docs/fulfillment/ONBOARDING_FORM.md` questions.
- GSC export instructions from `docs/fulfillment/GSC_EXPORT_GUIDE.md`.
- Confirmation of delivery timeline.

Track:

- Paddle subscription ID.
- Customer email.
- Domain.
- Billing start date.
- First report due date.
- Renewal date.
- Cancellation/refund status.

## Risks

- Paddle account approval may take time.
- Paddle may require website, terms, privacy, and refund policy before checkout approval.
- Subscription payments can fail or become past due.
- Manual fulfillment must stay under 30 minutes/site/month after setup.
