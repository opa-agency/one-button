from uuid import uuid4
from urllib.parse import urlencode
from datetime import timedelta

from django.shortcuts import render, redirect
from django.http import HttpResponseNotAllowed, HttpResponse, JsonResponse
from django.urls import reverse
from django.utils import timezone
from requests import request
from decouple import config
import stripe

from .models import UserPreCheckout, PaymentCompleted
from .messages import random_payment_message

STRIPE_SECRET_KEY = config("STRIPE_SECRET_KEY")
STRIPE_PRICE_ID = config("STRIPE_PRICE_ID")
BASE_URL = config("BASE_URL")
stripe.api_key = STRIPE_SECRET_KEY


def _dashboard_context(token_expires_at=None, token=None, order_number=None, share_host=""):
	completed_payments_count = PaymentCompleted.objects.count()
	recent_payments = (
		PaymentCompleted.objects.select_related("user_pre_checkout")
		.order_by("-created_at")[:8]
	)
	return {
		"completed_payments_count": completed_payments_count,
		"total_lei": completed_payments_count * 10,
		"token_expires_at": token_expires_at,
		"recent_payments": recent_payments,
		"token": token,
		"order_number": order_number,
		"share_host": share_host,
	}


def home_page_view(request):
	token = request.GET.get("token") or request.POST.get("token")
	if request.method == "GET":
		if not token:
			token = uuid4().hex
			return redirect(f"/?{urlencode({'token': token})}")
		return render(request, "home.html", {"token": token})

	elif request.method == "POST":
		if not token:
			return HttpResponseNotAllowed("No token in query parameter")
		success_url = f"{BASE_URL}/checkout/finalize/?{urlencode({'token': token})}"
		stripe_session = stripe.checkout.Session.create(
			success_url=success_url,
			line_items=[{"price": STRIPE_PRICE_ID, "quantity": 1}],
			mode="payment",
			metadata={"token": token},
		)

		UserPreCheckout.objects.update_or_create(
			token=token,
			defaults={"checkout_session_id": stripe_session.id},
			create_defaults={
				"checkout_session_id": stripe_session.id,
				"message": random_payment_message(),
			},
		)

		return redirect(stripe_session.url)


def checkout_finalize_view(request):
	token = request.GET.get('token')
	user_pre_checkout = UserPreCheckout.objects.filter(token=token).first()
	if not user_pre_checkout:
		return HttpResponse("Invalid token")
	session = stripe.checkout.Session.retrieve(
		user_pre_checkout.checkout_session_id
	)
	print(f"Stripe session metadata token: {session.metadata.token}")
	payment_status = session.payment_status
	print(f"Stripe session payment status: {payment_status}")
	if payment_status == "paid":
		print("Payment successful!")
		PaymentCompleted.objects.update_or_create(
			user_pre_checkout=user_pre_checkout,
			defaults={"stripe_payment_id": session.payment_intent},
		)
	return redirect(f"{reverse('dashboard')}?{urlencode({'token': token})}")


def dashboard_view(request):
	token = request.GET.get("token") or request.POST.get("token")
	if not token:
		return render(request, "missing_token.html", status=404)

	payment_completed = PaymentCompleted.objects.select_related("user_pre_checkout").filter(
		user_pre_checkout__token=token
	).first()
	if not payment_completed:
		return render(request, "invalid_token.html", status=404)

	valid_until = payment_completed.created_at + timedelta(minutes=10)
	if timezone.now() > valid_until:
		return render(request, "expired_token.html", status=410)

	return render(
		request,
		"dashboard.html",
		_dashboard_context(
			token_expires_at=valid_until.isoformat(),
			token=token,
			order_number=payment_completed.order_number(),
			share_host=request.get_host(),
		),
	)


def dashboard_admin_view(request):
	if request.method != "GET":
		return HttpResponseNotAllowed(["GET"])

	return render(request, "dashboard.html", _dashboard_context(share_host=request.get_host()))


def live_stats_view(request):
	if request.method != "GET":
		return HttpResponseNotAllowed(["GET"])

	count = PaymentCompleted.objects.count()
	recent = (
		PaymentCompleted.objects.select_related("user_pre_checkout")
		.order_by("-created_at")[:8]
	)
	now = timezone.now()
	latest = []
	for payment in recent:
		created = payment.created_at or now
		latest.append({
			"id": payment.id,
			"order_number": payment.order_number(),
			"message": payment.user_pre_checkout.message,
			"since_seconds": int((now - created).total_seconds()),
		})
	return JsonResponse({
		"count": count,
		"total_lei": count * 10,
		"latest": latest,
	})
