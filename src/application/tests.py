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
		self.assertIn("profile_form", response.context)

	def test_dashboard_post_saves_username_and_message(self):
		user_pre_checkout = UserPreCheckout.objects.create(token="profile-token")
		PaymentCompleted.objects.create(
			user_pre_checkout=user_pre_checkout,
			stripe_payment_id="pi_profile",
		)

		response = self.client.post(
			reverse("dashboard"),
			{
				"token": "profile-token",
				"username": "Alex",
				"message": "Salut tuturor",
			},
		)

		self.assertEqual(response.status_code, 302)
		self.assertEqual(response.url, f"{reverse('dashboard')}?token=profile-token")
		user_pre_checkout.refresh_from_db()
		self.assertEqual(user_pre_checkout.username, "Alex")
		self.assertEqual(user_pre_checkout.message, "Salut tuturor")

	def test_dashboard_admin_renders_without_token(self):
		response = self.client.get(reverse("dashboard_admin"))
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, "dashboard.html")
		self.assertFalse(response.context["show_profile_form"])

	def test_dashboard_admin_disallows_post(self):
		response = self.client.post(reverse("dashboard_admin"))
		self.assertEqual(response.status_code, 405)
