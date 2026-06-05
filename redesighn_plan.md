## Plan: Dark-theme UI + Real-time Dashboard

> **Design fidelity is non-negotiable.** The post-payment page (dashboard) must match `platesc10lei-dupa-plata.html` *pixel-perfectly* — same colors, fonts, spacing, animations, layout, copy, ticker behavior, share button, and timer block. The mock is the source of truth: copy its CSS variables (`--bg #0a0a0a`, `--surface #111`, `--accent #c8f135`, `--muted #2a2a2a`, `--text #f0f0f0`, `--sub #666`), its keyframes (`fadeUp`, `slideIn`, `fadeOut`, `pulse`, `lineGrow`, `bump`), its noise overlay SVG, its top-line bar, its Bebas Neue + DM Mono Google Fonts link, and its DOM structure verbatim. Any deviation needs an explicit reason. The first page (home) inherits the same visual system (palette, fonts, noise, top-line) so both pages feel like one product.

Re-skin the Django app to match the mock and turn the post-payment page into a live dashboard. The post-payment page shows the user's sequential order number (`#N`), live total payers + collected sum, the existing token-expiry timer (restyled to fit the mock's timer-block), a share button, and a bottom-left ticker that pops new payers as they happen. Liveness uses lightweight polling (≈4 s) against a new JSON endpoint — no infra change. The Stripe flow (token in URL → POST creates Checkout Session → `checkout/finalize/` → dashboard) stays exactly as it is today.

**Steps**

1. **Add live-stats JSON endpoint** in `src/application/views.py` and route in `src/core/urls.py`.
   - `live_stats_view` returns `{ "count": <int>, "total_lei": <int>, "latest": [{"id": <int>, "username": <str|null>, "message": <str|null>, "since_seconds": <int>}, ...] }` (latest 8, newest first).
   - Route at `/api/stats/`, GET-only, no auth, no CSRF concerns (read-only).
   - Reuses `PaymentCompleted` queries already used by `_dashboard_context`.

2. **Compute the user's order number** (sequential rank among completed payments).
   - Add `order_number` helper on `PaymentCompleted` in `src/application/models.py` computed as `PaymentCompleted.objects.filter(id__lte=self.id).count()` — no migration needed, deterministic, monotonic with PK.
   - In `dashboard_view` pass `order_number = payment_completed.order_number()` into the template context.

3. **Simplify `dashboard_view`** in `src/application/views.py`.
   - Drop `DashboardIdentityForm` handling, the POST branch, `show_profile_form`, and `username/message` writes. The form is removed per decision.
   - Keep token lookup, paid check, 10-min validity check, expired/invalid/missing template returns.
   - Trim `_dashboard_context` to only what the new template needs (`completed_payments_count`, `total_lei`, `recent_payments`, `order_number`, `token`, `token_expires_at`).

4. **Allow per-template body styling** in `src/theme/templates/base.html`.
   - Wrap the existing body classes in `{% block body_class %}min-h-screen text-gray-900 bg-slate-200{% endblock %}` so home/dashboard can override to the dark palette without affecting `applicationtwo/home.html`.

5. **Rewrite `src/theme/templates/home.html`** as the first page in the dark style.
   - Dark background (`#0a0a0a`), noise overlay, top-line accent, Bebas Neue + DM Mono fonts (same `<link>` as the mock).
   - Copy: short headline + 2–3 lines explaining the social experiment / human-curiosity angle (Romanian, in keeping with current tone). Show current live counter (`Au plătit deja N persoane`) by reading `completed_payments_count` from view context (small extension of context) — increases tension before paying. Optional: same `/api/stats/` poll on home to keep that number live.
   - Yellow accent CTA replaced by `--accent: #c8f135` button "PLĂTEȘTE 10 LEI" inside the existing `<form method="post" action="{% url 'home' %}?token={{ token|urlencode }}">` with `{% csrf_token %}` and `<input type="hidden" name="token">` — backend flow untouched.
   - Keep the two legally-required checkboxes (terms / digital-delivery waiver) and footer policy links / popup logic; restyled to fit the dark theme.
   - `home_page_view` GET branch updated to also pass `completed_payments_count` (one extra count query).

6. **Rewrite `src/theme/templates/dashboard.html`** to mirror `platesc10lei-dupa-plata.html`.
   - Sections in this order: order-number block (`#{{ order_number }}`), stats row (Total plătitori = `completed_payments_count`, Total colectat = `total_lei` RON), restyled token-expiry timer block driven by `token_expires_at` (reuse the existing JS countdown logic, just re-themed — fulfills the "Keep token expiry visible, restyled" decision), ironic message paragraph, share button, ticker container.
   - Server-rendered initial values come from context so the page is meaningful before JS runs.
   - Inline JS:
     - Polls `/api/stats/` every 4 s.
     - Updates `count` and `total_lei` with the bump animation from the mock.
     - Diffs the returned `latest[].id` array against a `Set` of already-seen ids; for each new id pushes a tick into the bottom-left ticker (`<dot> {username|"Cineva"} a plătit acum`). Falls back to the generic mock messages when no username/message present.
     - Web Share API with clipboard fallback for the share button. Share text uses the user's `order_number` and a configurable site URL (use `request.get_host()` or hardcode `platesc10lei.ro` matching the mock — pass via context as `share_host`).

7. **Restyle the small status pages** (`expired_token.html`, `invalid_token.html`, `missing_token.html`) to the dark palette so the experience is consistent. Minimal markup: same noise/top-line, short message, link back to `/` with a fresh token.

8. **Wire the new URL** in `src/core/urls.py`: `path("api/stats/", live_stats_view, name="live_stats")`.

**Relevant files**

- `src/application/views.py` — add `live_stats_view`; simplify `dashboard_view` (drop form branch and trim `_dashboard_context`); extend `home_page_view` GET to include `completed_payments_count`.
- `src/application/models.py` — add `order_number()` method on `PaymentCompleted`.
- `src/core/urls.py` — register `api/stats/`.
- `src/theme/templates/home.html` — full rewrite, dark theme + social-experiment copy, keep existing form action, CSRF, hidden token, two consent checkboxes, policy popups.
- `src/theme/templates/dashboard.html` — full rewrite, mirrors `platesc10lei-dupa-plata.html`, drops profile form, adds polling + ticker JS, keeps countdown timer logic restyled.
- `src/theme/templates/base.html` — add `{% block body_class %}` so home/dashboard override the body palette without touching `applicationtwo/home.html`.
- `src/theme/templates/expired_token.html`, `invalid_token.html`, `missing_token.html` — restyle to dark palette.
- `platesc10lei-dupa-plata.html` — reference only, not modified.

**Verification**

1. `python manage.py runserver` (in `src/`) and `python manage.py tailwind start` in another shell.
2. Open `/` in a fresh private window → dark home renders, "Au plătit deja N persoane" matches DB count, token appears in URL, terms checkboxes work, popups still open/close.
3. Click "Plătește 10 lei" → redirected to Stripe Checkout (existing flow, untouched).
4. Use Stripe test card `4242 4242 4242 4242` → returns to `/checkout/finalize/?token=…` → lands on dashboard.
5. Dashboard shows: correct `#N` matching `PaymentCompleted` count for that payment, total payers and total RON consistent (`count*10`), countdown ticking down from ~10:00, share button copies/shares text containing `#N`.
6. Open a second private window, complete another payment; within ≤4 s the first window's counters bump up and a tick appears bottom-left.
7. Hit `/api/stats/` directly in browser → JSON shape matches contract; no auth required.
8. Negative checks: visit `/dashboard/` with no token → restyled `missing_token.html`; with bogus token → restyled `invalid_token.html`; with paid token after 10 min → restyled `expired_token.html`.
9. Confirm `applicationtwo` home (`/home-two/`) still renders in its original light style (body block default preserved).

**Decisions**

- Real-time mechanism: polling `/api/stats/` every ~4 s (no Channels, no SSE).
- Dark theme applied to BOTH home and post-payment pages.
- "Transaction id" displayed as sequential order number (`#N`), computed from `PaymentCompleted` PK rank — no schema change.
- Keep the 10-minute token-expiry timer, just restyled to fit the dark theme.
- Drop the username/message profile form entirely. Ticker shows generic messages when payer is anonymous (which is now always).
- Stripe / token / webhook flow is unchanged — no migrations, no settings changes.

**Further considerations**

1. Polling load: at ~4 s an idle page is ~15 req/min/user. If traffic spikes, switch to SSE later (single endpoint, no client change beyond `EventSource`). Keep the JSON contract stable so swapping the transport is mechanical. *Recommendation: ship polling first, revisit only if load is observed.*
2. Race in `order_number()`: two payments inserted in the same millisecond both call `filter(id__lte=self.id).count()` — each gets a distinct number because PKs are distinct. Safe. *No action needed.*
3. Share host: the mock hardcodes `platesc10lei.ro`. Pass via context (e.g. `request.get_host()` or a `SHARE_HOST` setting) so it's correct in dev and prod without editing templates. *Recommendation: read from `request.get_host()` and fall back to a setting.*
