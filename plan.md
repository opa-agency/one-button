## Plan: Stripe Checkout + 1h Token Access (DRAFT)

Implement a token-based payment gate where POST to home creates a Stripe Checkout Session, access is granted only after webhook-confirmed success, and dashboard access lasts 1 hour. Based on your decisions: store one payment record per token in model user_payments (overwrite latest state), use Stripe Price ID from env, and prevent users with active paid access from seeing home by redirecting them to dashboard. The plan keeps token identity session-based (existing flow), persists payment/access state in DB, and validates access on every dashboard request. It also fixes the current hidden-input token mismatch in home template so frontend and backend stay consistent.

**Steps**
1. Add data model in [src/core/models.py](src/core/models.py) for user_payments keyed by token (unique), with fields for stripe checkout session id, payment status, paid_at, access_expires_at and timestamps;
2. Add Stripe configuration in [src/core/settings.py](src/core/settings.py): STRIPE_SECRET_KEY, STRIPE_WEBHOOK_SECRET, STRIPE_PRICE_ID, and app base URL for success/cancel/webhook construction.
3. Refactor home logic in [src/core/views.py](src/core/views.py):
- GET: if session token has active access in user_payments (now < access_expires_at and paid), redirect to dashboard.
- POST: ensure token exists, create/update user_payments as pending, create Stripe Checkout Session with token in metadata/client_reference_id, redirect to Stripe checkout URL.
4. Add Stripe webhook endpoint in [src/core/views.py](src/core/views.py) and route in [src/core/urls.py](src/core/urls.py):
- Verify Stripe signature using webhook secret.
- On checkout.session.completed, upsert user_payments for token, mark paid, set paid_at, set access_expires_at = paid_at + 1 hour.
- Record event id for idempotency and safe re-delivery handling.
5. Add success and cancel routes/views in [src/core/urls.py](src/core/urls.py) and [src/core/views.py](src/core/views.py):
- Success page behavior: no grant here; show “processing payment” and redirect/check access state.
- Cancel page behavior: return user to home with message.
6. Gate dashboard in [src/core/views.py](src/core/views.py):
- Read session token.
- Allow only if user_payments indicates paid and unexpired.
- Otherwise redirect to home with message.
7. Fix form-token consistency in [src/theme/templates/home.html](src/theme/templates/home.html) to use the same token context variable that backend sends; keep CSRF and POST target unchanged.
8. Update docs in [README.md](README.md) with required env vars, local webhook testing flow, and lifecycle: create checkout → webhook confirms → 1h access window.

**Verification**
- Run migrations and check model creation.
- Manual flow:
  - New session opens home.
  - POST home creates Stripe Checkout and redirects.
  - Webhook completion updates user_payments and expiry.
  - User can access dashboard for 1 hour.
  - While active, visiting home redirects to dashboard.
  - After expiry, dashboard redirects to home.
- Negative checks:
  - Invalid/missing webhook signature is rejected.
  - Replayed webhook does not duplicate/incorrectly mutate state.
  - Cancelled checkout does not grant access.

**Decisions**
- Access grant source: webhook confirmation only.
- Data shape: one row per token in user_payments (latest state).
- Pricing config: Stripe Price ID from environment.
- Home behavior: users with active token access are redirected to dashboard.
