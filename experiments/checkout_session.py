import stripe
from decouple import config

stripe.api_key = config("STRIPE_SECRET_KEY")
token = "example_token"
session = stripe.checkout.Session.create(
  success_url="https://example.com/success",
  line_items=[{"price": "price_1T7b6CBCvKPSP3kIuUK3U6iq", "quantity": 1}],
  mode="payment",
  metadata={"token": token},
)

print(session)