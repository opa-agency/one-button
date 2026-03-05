from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import UserPreCheckout, PaymentCompleted


class DashboardAccessTests(TestCase):
	def test_dashboard_requires_token_query_param(self):
		response = self.client.get(reverse("dashboard"))
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, "missing_token.html")

	def test_dashboard_rejects_expired_payment_completed_token(self):
		user_pre_checkout = UserPreCheckout.objects.create(token="expired-token")
		payment_completed = PaymentCompleted.objects.create(
			user_pre_checkout=user_pre_checkout,
			stripe_payment_id="pi_expired",
		)
		payment_completed.created_at = timezone.now() - timezone.timedelta(minutes=11)
		payment_completed.save(update_fields=["created_at"])

		response = self.client.get(reverse("dashboard"), {"token": "expired-token"})
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, "expired_token.html")

	def test_dashboard_allows_valid_recent_payment_completed_token(self):
		user_pre_checkout = UserPreCheckout.objects.create(token="valid-token")
		PaymentCompleted.objects.create(
			user_pre_checkout=user_pre_checkout,
			stripe_payment_id="pi_valid",
		)

		response = self.client.get(reverse("dashboard"), {"token": "valid-token"})
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, "dashboard.html")
		self.assertIn("token_expires_at", response.context)
