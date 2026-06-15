from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from types import SimpleNamespace
from unittest.mock import patch

from .models import UserPreCheckout, PaymentCompleted


class AuthenticationTests(TestCase):
	def test_login_page_uses_project_template(self):
		response = self.client.get(reverse("login"))

		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, "registration/login.html")

	def test_user_can_login_with_username_and_password(self):
		get_user_model().objects.create_user(
			username="partner",
			password="strong-pass-123",
		)

		response = self.client.post(
			reverse("login"),
			{
				"username": "partner",
				"password": "strong-pass-123",
			},
		)

		self.assertEqual(response.status_code, 302)
		self.assertEqual(response.url, reverse("partner_dashboard"))

	def test_login_page_redirects_authenticated_user(self):
		user = get_user_model().objects.create_user(
			username="partner",
			password="strong-pass-123",
		)
		self.client.force_login(user)

		response = self.client.get(reverse("login"))

		self.assertEqual(response.status_code, 302)
		self.assertEqual(response.url, reverse("partner_dashboard"))

	def test_register_page_uses_project_template(self):
		response = self.client.get(reverse("register"))

		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, "registration/register.html")

	def test_user_can_register_with_username_and_password(self):
		response = self.client.post(
			reverse("register"),
			{
				"username": "newpartner",
				"password1": "strong-pass-123",
				"password2": "strong-pass-123",
			},
		)

		self.assertEqual(response.status_code, 302)
		self.assertEqual(response.url, reverse("partner_dashboard"))
		self.assertTrue(get_user_model().objects.filter(username="newpartner").exists())

	def test_register_page_redirects_authenticated_user_to_dashboard(self):
		user = get_user_model().objects.create_user(
			username="partner",
			password="strong-pass-123",
		)
		self.client.force_login(user)

		response = self.client.get(reverse("register"))

		self.assertEqual(response.status_code, 302)
		self.assertEqual(response.url, reverse("partner_dashboard"))

	def test_policy_shows_login_and_register_buttons_for_anonymous_user(self):
		response = self.client.get(reverse("home"), {"token": "policy-token"})

		self.assertContains(response, "Login partener")
		self.assertContains(response, "Register partener")
		self.assertNotContains(response, "Go to dashboard")

	def test_policy_shows_dashboard_button_for_authenticated_user(self):
		user = get_user_model().objects.create_user(
			username="partner",
			password="strong-pass-123",
		)
		self.client.force_login(user)

		response = self.client.get(reverse("home"), {"token": "policy-token"})

		self.assertContains(response, "Go to dashboard")
		self.assertNotContains(response, "Login partener")
		self.assertNotContains(response, "Register partener")


class ReferralTests(TestCase):
	def test_referral_query_is_preserved_when_token_is_created(self):
		partner = get_user_model().objects.create_user(
			username="partner",
			password="strong-pass-123",
		)

		response = self.client.get(reverse("home"), {"refferal": partner.id})

		self.assertEqual(response.status_code, 302)
		self.assertIn(f"refferal={partner.id}", response.url)
		self.assertIn("token=", response.url)

	@patch("application.views.stripe.checkout.Session.create")
	def test_checkout_links_payment_attempt_to_referral_user(self, create_session):
		partner = get_user_model().objects.create_user(
			username="partner",
			password="strong-pass-123",
		)
		create_session.return_value = SimpleNamespace(
			id="cs_referral",
			url="https://stripe.test/checkout",
		)

		response = self.client.post(
			f"{reverse('home')}?token=ref-token",
			{"token": "ref-token", "refferal": str(partner.id)},
		)

		self.assertEqual(response.status_code, 302)
		self.assertEqual(response.url, "https://stripe.test/checkout")
		pre_checkout = UserPreCheckout.objects.get(token="ref-token")
		self.assertEqual(pre_checkout.referral_user, partner)
		self.assertEqual(
			create_session.call_args.kwargs["metadata"]["referral_user_id"],
			str(partner.id),
		)

	def test_partner_dashboard_lists_referred_completed_payments(self):
		partner = get_user_model().objects.create_user(
			username="partner",
			password="strong-pass-123",
		)
		other_partner = get_user_model().objects.create_user(
			username="other",
			password="strong-pass-123",
		)
		referred_checkout = UserPreCheckout.objects.create(
			token="referred-token",
			referral_user=partner,
		)
		other_checkout = UserPreCheckout.objects.create(
			token="other-token",
			referral_user=other_partner,
		)
		PaymentCompleted.objects.create(
			user_pre_checkout=referred_checkout,
			stripe_payment_id="pi_referred",
		)
		PaymentCompleted.objects.create(
			user_pre_checkout=other_checkout,
			stripe_payment_id="pi_other",
		)
		self.client.force_login(partner)

		response = self.client.get(reverse("partner_dashboard"))

		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, "partner_dashboard.html")
		self.assertContains(response, f"refferal={partner.id}")
		self.assertContains(response, "Plati referral")
		self.assertContains(response, "Comision estimat")
		self.assertContains(response, "1 RON")
		self.assertContains(response, "Distribuie rapid")
		self.assertContains(response, "WhatsApp")
		self.assertContains(response, "Telegram")
		self.assertContains(response, "Facebook")
		self.assertContains(response, "Email")
		self.assertNotContains(response, "Intrari prin linkul tau")
		self.assertNotContains(response, "referred-token")
		self.assertNotContains(response, "pi_referred")
		self.assertNotContains(response, "other-token")
		self.assertEqual(response.context["referred_payments_count"], 1)

	def test_partner_dashboard_requires_login(self):
		response = self.client.get(reverse("partner_dashboard"))

		self.assertEqual(response.status_code, 302)
		self.assertIn(reverse("login"), response.url)


class DashboardAccessTests(TestCase):
	def test_dashboard_requires_token_query_param(self):
		response = self.client.get(reverse("dashboard"))
		self.assertEqual(response.status_code, 404)
		self.assertTemplateUsed(response, "missing_token.html")

	def test_dashboard_rejects_expired_payment_completed_token(self):
		user_pre_checkout = UserPreCheckout.objects.create(token="expired-token")
		payment_completed = PaymentCompleted.objects.create(
			user_pre_checkout=user_pre_checkout,
			stripe_payment_id="pi_expired",
		)
		payment_completed.created_at = timezone.now() - timezone.timedelta(minutes=4)
		payment_completed.save(update_fields=["created_at"])

		response = self.client.get(reverse("dashboard"), {"token": "expired-token"})
		self.assertEqual(response.status_code, 410)
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
		self.assertContains(response, "ARATĂ-LE")
		self.assertContains(response, "Eu am văzut statistica. Tu n-ai văzut-o.")
		self.assertContains(response, "Screenshot denied")

	def test_dashboard_post_renders_valid_recent_payment(self):
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

		self.assertEqual(response.status_code, 200)
		user_pre_checkout.refresh_from_db()
		self.assertIsNone(user_pre_checkout.username)
		self.assertIsNone(user_pre_checkout.message)

	def test_dashboard_admin_requires_login(self):
		response = self.client.get(reverse("dashboard_admin"))

		self.assertEqual(response.status_code, 302)
		self.assertIn(reverse("login"), response.url)

	def test_dashboard_admin_redirects_non_superuser_to_partner_dashboard(self):
		user = get_user_model().objects.create_user(
			username="partner",
			password="strong-pass-123",
		)
		self.client.force_login(user)

		response = self.client.get(reverse("dashboard_admin"))

		self.assertEqual(response.status_code, 302)
		self.assertEqual(response.url, reverse("partner_dashboard"))

	def test_dashboard_admin_renders_for_superuser(self):
		user = get_user_model().objects.create_superuser(
			username="admin",
			password="strong-pass-123",
		)
		self.client.force_login(user)

		response = self.client.get(reverse("dashboard_admin"))

		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, "dashboard.html")

	def test_dashboard_admin_disallows_post(self):
		response = self.client.post(reverse("dashboard_admin"))
		self.assertEqual(response.status_code, 405)
